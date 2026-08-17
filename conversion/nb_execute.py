#!/usr/bin/env python3
"""
Execute a converted chapter in place, regenerating every output.

Outputs are content in this repo. `.github/workflows/deploy.yml` runs
`jupyter-book build --html` with no `--execute` and no pip install, so MyST renders the
*committed* outputs and never runs a line of code. A converted notebook whose outputs were
not regenerated publishes Polars source above pandas HTML tables.

Full re-execution is the chosen policy: every output provably came from Polars. The cost is
churn -- 77 PNG blobs, 41 plotly blobs, and everything downstream of 44 randomness sites
against only 10 seeds all change on every run, whether or not the conversion touched them.
`nb_validate.py`'s G8 reports that churn so a reviewer can tell a conversion effect from RNG
noise; it does not block.

Errors are checked in BOTH directions against the baseline. A new error means the conversion
is broken. A *vanished* error means an intentional "this line raises on purpose" demo stopped
demonstrating, and the prose above it now lies -- the sibling repo only checked one direction
and could not have caught that.
"""

from __future__ import annotations

import argparse
import logging
import sys
import uuid
from pathlib import Path
from typing import Dict, List, Set, Tuple

import nbformat
import yaml
from nbclient import NotebookClient

import chapters as ch
import nb_baseline

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

ALLOWLIST_PATH = Path("conversion/conversion_allowlist.yml")


def load_allow(chapter: str, section: str) -> Dict[str, str]:
    if not ALLOWLIST_PATH.exists():
        return {}
    data = yaml.safe_load(ALLOWLIST_PATH.read_text()) or {}
    entries = (data.get(chapter) or {}).get(section, []) or []
    return {e["cell_id"]: e.get("reason", "") for e in entries}


def error_cells(nb) -> Dict[str, str]:
    """Cell id -> exception name, for every cell carrying an error output."""
    out = {}
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        for o in cell.get("outputs", []):
            if o.get("output_type") == "error":
                out[cell.get("id")] = o.get("ename", "?")
    return out


def baseline_errors(chapter: ch.Chapter) -> Dict[str, str]:
    lock = nb_baseline.read_lock()
    paths = nb_baseline.cached_paths(chapter, lock)
    if paths["source"] is None:
        return {}
    return error_cells(nbformat.read(str(paths["source"]), as_version=4))


def write_witness(nb, chapter: ch.Chapter, kernel: str) -> Dict:
    """Corroborated evidence that this notebook really was executed end to end.

    The sibling stamped a single boolean and let it short-circuit its whole stale-output
    check. A boolean is unverifiable; these fields are checked against the artifact by G6,
    so a forged witness cannot satisfy them simultaneously.
    """
    import polars as pl  # imported here so the script still runs for --help without polars

    code_cells = [c for c in nb.cells if c.cell_type == "code" and c.get("source", "").strip()]
    counts = [c.get("execution_count") for c in code_cells]
    executed = [c for c in counts if c is not None]

    witness = {
        "run_id": str(uuid.uuid4()),
        "baseline_sha": nb_baseline.read_lock()["main_sha"],
        "polars": pl.__version__,
        # The kernel actually used, not the one the notebook declares. Every notebook here
        # declares `python3`, so recording the declaration would say nothing about which of the
        # machine's four polars-bearing environments produced these outputs.
        "kernel": kernel,
        "declared_kernel": nb.metadata.get("kernelspec", {}).get("name"),
        "n_code_cells": len(code_cells),
        "n_executed": len(executed),
        "exec_counts_monotonic": executed == sorted(executed) and len(set(executed)) == len(executed),
    }
    nb.metadata["polars_conversion"] = witness
    return witness


def execute(chapter: ch.Chapter, kernel: str, timeout: int) -> int:
    path = chapter.source
    nb = nbformat.read(str(path), as_version=4)

    logger.info(f"{chapter.name}: executing {len(nb.cells)} cells (kernel={kernel}, cwd={chapter.dir})")
    NotebookClient(
        nb,
        kernel_name=kernel,
        timeout=timeout,
        allow_errors=True,
        # Run from the chapter's own directory: every data path is notebook-relative
        # (`pd.read_csv("data/elections.csv")`), so any other cwd fails on file not found.
        resources={"metadata": {"path": str(chapter.dir)}},
    ).execute()

    base_errs = baseline_errors(chapter)
    now_errs = error_cells(nb)
    allow_new = load_allow(chapter.name, "expected_errors")
    allow_gone = load_allow(chapter.name, "resolved_errors")

    new = {cid: en for cid, en in now_errs.items() if cid not in base_errs and cid not in allow_new}
    gone = {cid: en for cid, en in base_errs.items() if cid not in now_errs and cid not in allow_gone}
    kept = {cid: en for cid, en in now_errs.items() if cid in base_errs}

    for cid, ename in kept.items():
        was = base_errs[cid]
        note = f"{was} -> {ename}" if was != ename else ename
        print(f"    kept error   {cid}: {note}")
    for cid in allow_new:
        if cid in now_errs:
            print(f"    allowed      {cid}: {now_errs[cid]} -- {allow_new[cid]}")
    for cid, ename in new.items():
        print(f"    NEW ERROR    {cid}: {ename}")
    for cid, ename in gone.items():
        print(f"    LOST ERROR   {cid}: baseline raised {ename}, now silent")

    if new or gone:
        print(f"\n  {len(new)} new / {len(gone)} lost error(s) -- notebook NOT written.")
        if new:
            print("  Fix the conversion, or list the cell under `expected_errors:` with a reason.")
        if gone:
            print("  A demo that raised on purpose no longer raises: the prose around it now")
            print("  describes an error the reader will not see. Re-aim the prose, or list the")
            print("  cell under `resolved_errors:` with a reason.")
        return 1

    witness = write_witness(nb, chapter, kernel)
    if witness["n_executed"] != witness["n_code_cells"]:
        print(
            f"\n  only {witness['n_executed']}/{witness['n_code_cells']} code cells executed "
            "-- notebook NOT written."
        )
        return 1

    nbformat.write(nb, str(path))
    n_out = sum(1 for c in nb.cells if c.cell_type == "code" and c.get("outputs"))
    print(
        f"  wrote {path}: {witness['n_executed']}/{witness['n_code_cells']} cells executed, "
        f"{n_out} carry output, polars {witness['polars']}"
    )
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="Execute a converted chapter in place.")
    ap.add_argument("--chapter", required=True, help="Chapter directory name, e.g. regex")
    ap.add_argument("--kernel", default="d100")
    ap.add_argument("--timeout", type=int, default=600,
                    help="Per-cell timeout; pandas_2 reads 146 MB (default: 600)")
    args = ap.parse_args()

    chapter = ch.resolve([args.chapter])[0]
    if not chapter.is_notebook:
        print(f"{chapter.name} is a prose-only .md chapter; nothing to execute")
        sys.exit(0)
    sys.exit(execute(chapter, args.kernel, args.timeout))


if __name__ == "__main__":
    main()
