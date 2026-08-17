#!/usr/bin/env python3
"""
Notebook <-> Python-text converter.

Converts a chapter notebook (.ipynb) to a plain .py file in jupytext "percent" format
that an agent can edit safely, and back again. Wraps jupytext with the one thing it does
not provide: stable cell IDs across repeated round trips, because jupytext's .py writer
silently drops `cell.id`.

Every notebook in this repo is nbformat 4.5 with an id on every cell, and all 24 were
verified to round-trip losslessly (one `# %%` marker per cell, no marker collisions).
That is what lets the whole harness align on cell id rather than position: `gate_structure`
compares id sequences, `splice_outputs` matches by id, and a reviewer's finding can name a
cell that survives an edit above it.

Agents edit the .py, never the .ipynb. A JSON diff is unreadable; a percent-format diff is
the artifact course staff can actually review.
"""

from __future__ import annotations

import argparse
import copy
import logging
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import jupytext
import nbformat
from nbformat.v4 import upgrade as nbformat_upgrade

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

FMT = "py:percent"
CELL_ID_KEY = "id"
SKIP_DIR_PARTS = {".ipynb_checkpoints"}

# A markdown/raw line that becomes a cell marker once jupytext prefixes it with "# ".
PERCENT_MARKER_COLLISION_RE = re.compile(r"^\s*%%(%*)\s")


def stash_cell_ids(nb) -> None:
    """Copy each cell's `id` into cell.metadata['id'] so jupytext's .py writer
    (which ignores cell.id) carries it through as a `# %%` header key."""
    for cell in nb.cells:
        cell_id = cell.get("id")
        if cell_id is not None:
            cell["metadata"][CELL_ID_KEY] = cell_id


def restore_cell_ids(nb) -> None:
    """Reverse of stash_cell_ids. Cells with no stashed id (added by hand in the .py)
    keep whatever id nbformat assigns."""
    for cell in nb.cells:
        if CELL_ID_KEY in cell["metadata"]:
            cell["id"] = cell["metadata"].pop(CELL_ID_KEY)


def normalize_cell_sources(nb) -> int:
    """Normalize line endings and strip trailing whitespace at the end of each cell.

    jupytext does both on the way through, so without doing it up front the round-trip
    check reports diffs on cells that are in fact fine. Neither change is visible to
    Python or to a markdown renderer. Returns the number of cells changed.
    """
    changed = 0
    for cell in nb.cells:
        normalized = cell.source.replace("\r\n", "\n").replace("\r", "\n").rstrip()

        # jupytext also strips trailing space off a cell magic while commenting it out
        # (`%%sql ` -> `%%sql`). A cell magic is only valid as line 0 of a code cell, so
        # it cannot be inside a string literal and the whitespace cannot be significant.
        if cell.cell_type == "code" and normalized.startswith("%%"):
            head, sep, tail = normalized.partition("\n")
            normalized = head.rstrip() + sep + tail

        if normalized != cell.source:
            cell.source = normalized
            changed += 1
    return changed


def load_notebook(ipynb_path: Path):
    """Read a notebook, normalize cell sources, and guarantee every cell has a stable id."""
    nb = nbformat.read(str(ipynb_path), as_version=4)
    nb = nbformat_upgrade(nb, from_minor=nb.nbformat_minor)
    normalize_cell_sources(nb)
    nbformat.validate(nb)
    return nb


def notebook_to_py_text(nb) -> str:
    stash_cell_ids(nb)
    return jupytext.writes(nb, fmt=FMT)


def py_text_to_notebook(text: str):
    nb = jupytext.reads(text, fmt=FMT)
    restore_cell_ids(nb)
    nb = nbformat_upgrade(nb, from_minor=nb.nbformat_minor)
    nbformat.validate(nb)
    return nb


def describe_marker_collisions(nb) -> List[str]:
    r"""Find markdown/raw lines jupytext's percent reader will mistake for a cell marker.

    Commenting a line like `    %% sql` yields `#     %% sql`, which matches the reader's
    `^\s*#\s*%%(%*)\s(.*)$` and silently splits the cell in two. `%%sql` with no space
    after the percents does NOT collide, which is why the 34 `%%sql` code cells in
    sql_I/sql_II are safe.
    """
    hits = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "code":
            continue
        for line_no, line in enumerate(cell.source.split("\n")):
            if PERCENT_MARKER_COLLISION_RE.match(line):
                hits.append(
                    f"cell {i} ({cell.cell_type}) line {line_no} reads as a cell marker: {line!r}"
                )
    return hits


def roundtrip_mismatches(nb, text: str) -> List[str]:
    """Parse the generated .py back and compare. Empty means the conversion was lossless
    for everything the harness aligns on: cell order, type, source, and id."""
    back = py_text_to_notebook(text)
    problems: List[str] = []

    if len(nb.cells) != len(back.cells):
        problems.append(f"cell count changed: {len(nb.cells)} -> {len(back.cells)}")
        problems.extend(describe_marker_collisions(nb))
        return problems

    for i, (a, b) in enumerate(zip(nb.cells, back.cells)):
        if a.cell_type != b.cell_type:
            problems.append(f"cell {i}: type {a.cell_type} -> {b.cell_type}")
        if a.get("id") != b.get("id"):
            problems.append(f"cell {i}: id {a.get('id')} -> {b.get('id')}")
        if a.source != b.source:
            problems.append(f"cell {i} ({a.cell_type}): source differs")
            for line_no, (x, y) in enumerate(zip(a.source.split("\n"), b.source.split("\n"))):
                if x != y:
                    problems.append(f"    line {line_no}: {x!r} -> {y!r}")
                    break
    return problems


def ipynb_to_py(ipynb_path: Path, py_path: Path, verify: bool = True) -> List[str]:
    """Convert a notebook to a percent-format .py file.

    Returns round-trip mismatches. Nothing is written when there are any: a .py that does
    not survive the trip back would silently corrupt the notebook it rebuilds.
    """
    nb = load_notebook(ipynb_path)
    text = notebook_to_py_text(nb)

    problems = roundtrip_mismatches(nb, text) if verify else []
    if problems:
        return problems

    py_path.parent.mkdir(parents=True, exist_ok=True)
    py_path.write_text(text)
    return []


def splice_outputs(nb, original_path: Path) -> Tuple[int, int]:
    """Restore cell outputs from the original notebook, matched by cell id.

    The percent format carries no outputs, so a round trip drops every one. In this repo
    that matters more than usual: CI never executes notebooks, so committed outputs are
    what ships. A rebuild without either this splice or a full execution would publish a
    site of code with no results.

    An output is restored only when the cell's source is byte-identical. A cell the
    conversion touched keeps nothing, because its committed output shows a *pandas*
    result: preserving it would publish visibly wrong output under Polars code.

    Matching is by id, not position. Every cell here already carries a stable id, so an
    id match survives an edit that adds or removes a cell above it, where position would
    silently pair the wrong cells.

    Returns (preserved, dropped).
    """
    original = load_notebook(original_path)
    prior_by_id = {c.get("id"): c for c in original.cells if c.get("id")}

    preserved = dropped = 0
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        prior = prior_by_id.get(cell.get("id"))
        if prior is None or prior.cell_type != "code":
            continue
        if prior.source != cell.source:
            if prior.get("outputs"):
                dropped += 1
            continue

        # execution_count is restored even for a cell that produced no output. Skipping those
        # nulls the count on every import and assignment cell, which shows up as a diff on
        # lines the conversion never touched -- noise in exactly the review that has to be
        # readable to be worth running.
        cell["execution_count"] = prior.get("execution_count")
        if prior.get("outputs"):
            cell["outputs"] = copy.deepcopy(prior["outputs"])
            preserved += 1
    return preserved, dropped


def splice_metadata(nb, original_path: Path) -> None:
    """Restore notebook-level metadata that the round trip does not carry.

    jupytext writes its own provenance block into `metadata.jupytext` and does not round-trip
    `language_info`. Left alone, every rebuilt notebook loses its language metadata and gains a
    jupytext stanza -- a diff on all 24 chapters that has nothing to do with the conversion.
    """
    original = load_notebook(original_path)
    nb.metadata.pop("jupytext", None)
    for key, value in original.metadata.items():
        if key not in nb.metadata:
            nb.metadata[key] = copy.deepcopy(value)


def py_to_ipynb(py_path: Path, ipynb_path: Path, outputs_from: Optional[Path] = None) -> None:
    """Convert a percent-format .py file back to a validated .ipynb."""
    nb = py_text_to_notebook(py_path.read_text())
    nb.metadata.pop("jupytext", None)
    if outputs_from is not None:
        preserved, dropped = splice_outputs(nb, outputs_from)
        splice_metadata(nb, outputs_from)
        logger.info(f"outputs: {preserved} preserved, {dropped} dropped as converted")
    ipynb_path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, str(ipynb_path))


def batch_to_py(source_root: Path, dest_root: Path, verify: bool) -> int:
    """Mirror every notebook under source_root into a .py tree. Returns failure count."""
    notebooks = [
        p
        for p in sorted(source_root.rglob("*.ipynb"))
        if not SKIP_DIR_PARTS & set(p.parts)
    ]
    logger.info(f"Found {len(notebooks)} notebooks under {source_root}")

    converted, failed = [], []
    for nb_path in notebooks:
        rel = nb_path.relative_to(source_root)
        try:
            nb = load_notebook(nb_path)
            text = notebook_to_py_text(nb)
            problems = roundtrip_mismatches(nb, text) if verify else []
        except Exception as e:  # noqa: BLE001 - report and continue over the batch
            logger.error(f"FAIL {rel}: {e}")
            failed.append((rel, str(e)))
            continue

        if problems:
            logger.error(f"FAIL {rel}: round-trip check failed, not written")
            for p in problems[:8]:
                logger.error(f"      {p}")
            failed.append((rel, problems[0]))
            continue

        py_path = (dest_root / rel).with_suffix(".py")
        py_path.parent.mkdir(parents=True, exist_ok=True)
        py_path.write_text(text)
        logger.info(f"ok   {rel} -> {py_path} ({len(nb.cells)} cells)")
        converted.append(rel)

    logger.info("-" * 68)
    logger.info(f"Converted: {len(converted)}   Failed: {len(failed)}")
    for rel, msg in failed:
        logger.warning(f"  {rel}: {msg}")
    return len(failed)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert notebooks to/from jupytext percent-format .py, preserving cell ids."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    to_py = sub.add_parser("to-py", help="Convert one .ipynb to a .py file")
    to_py.add_argument("--input", required=True)
    to_py.add_argument("--output", help="Output .py path (default: swap extension)")
    to_py.add_argument("--no-verify", action="store_true", help="Skip the round-trip check")

    to_ipynb = sub.add_parser("to-ipynb", help="Convert one .py file to a .ipynb")
    to_ipynb.add_argument("--input", required=True)
    to_ipynb.add_argument("--output", help="Output .ipynb path (default: swap extension)")
    to_ipynb.add_argument(
        "--outputs-from",
        dest="outputs_from",
        help="Original .ipynb to restore outputs from. Kept only where the cell source is "
        "unchanged; a converted cell keeps none, since its output shows pandas.",
    )

    batch = sub.add_parser("batch-to-py", help="Mirror a notebook tree into a .py tree")
    batch.add_argument("--source-root", default="content")
    batch.add_argument("--dest-root", default="conversion/pytext/polars")
    batch.add_argument("--no-verify", action="store_true")

    args = parser.parse_args()

    try:
        if args.command == "batch-to-py":
            failures = batch_to_py(
                Path(args.source_root), Path(args.dest_root), verify=not args.no_verify
            )
            sys.exit(1 if failures else 0)

        input_path = Path(args.input)
        if not input_path.exists():
            logger.error(f"Input not found: {input_path}")
            sys.exit(1)

        if args.command == "to-py":
            output_path = Path(args.output) if args.output else input_path.with_suffix(".py")
            problems = ipynb_to_py(input_path, output_path, verify=not args.no_verify)
            if problems:
                logger.error(f"{len(problems)} round-trip mismatch(es); nothing written:")
                for p in problems[:20]:
                    logger.error(f"  {p}")
                sys.exit(1)
            logger.info(f"Wrote {output_path}")
        else:
            output_path = Path(args.output) if args.output else input_path.with_suffix(".ipynb")
            outputs_from = Path(args.outputs_from) if args.outputs_from else None
            if outputs_from is not None and not outputs_from.exists():
                logger.error(f"--outputs-from not found: {outputs_from}")
                sys.exit(1)
            py_to_ipynb(input_path, output_path, outputs_from=outputs_from)
            logger.info(f"Wrote {output_path}")

    except Exception as e:  # noqa: BLE001 - CLI boundary
        logger.error(f"Conversion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
