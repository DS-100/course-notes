#!/usr/bin/env python3
"""
Triage every chapter into a conversion tier and write the orchestrator's work queue.

The tier decides two things: who does the writing, and how much review the result gets.
Measured from the *baseline*, so a tier never depends on how far a conversion has already
got.

    A  verify-only  no pandas at all -- the predicate is an empty diff, and any change fails
    B  translate    converter + gates + the blocking output reviewer
    C  heavy        adds the prose reviewer
    D  author       the chapter is *about* pandas; it gets rewritten, not translated

What separates D from C is not volume, it is subject. `prose_api_density` -- pandas API
vocabulary per line of prose -- splits them without a hand-maintained list, and the gap is
wide: the three tutorial chapters sit around 0.32-0.36 and the next chapter down is 0.13.
A chapter that merely *uses* pandas can be translated. A chapter that *teaches* `Index` and
`.loc` has to be re-aimed at what Polars does instead, and pretending otherwise is how a
conversion ends up as a syntax find-replace that leaves the pedagogy behind.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List

import nbformat

import chapters as ch
import nb_baseline

STATE_PATH = Path("conversion/state.json")

TIER_D_PROSE_DENSITY = 0.20
TIER_C_SITES = 25
TIER_C_OUTPUTS = 8
TIER_C_RESHAPE = 5

WRITER = {"A": None, "B": "notes-converter", "C": "notes-converter", "D": "chapter-author"}
REVIEWERS = {
    "A": [],
    "B": ["notes-output-reviewer"],
    "C": ["notes-output-reviewer", "notes-prose-reviewer"],
    "D": ["notes-output-reviewer", "notes-prose-reviewer"],
}

NETWORK_RE = re.compile(r"requests\.get|urlretrieve|urlopen|gdown|fetch_and_cache")


def measure(base_path: Path) -> Dict:
    """Six features, all read from the baseline."""
    if base_path.suffix == ".md":
        text = base_path.read_text()
        md_text, code_text, cells = text, "", []
    else:
        nb = nbformat.read(str(base_path), as_version=4)
        cells = nb.cells
        code_text = "\n".join(c.get("source", "") for c in cells if c.cell_type == "code")
        md_text = "\n".join(c.get("source", "") for c in cells if c.cell_type == "markdown")

    md_lines = max(1, md_text.count("\n"))
    output_surface = sum(
        1
        for c in cells
        if c.cell_type == "code"
        and any('class="dataframe"' in "".join(o.get("data", {}).get("text/html", ""))
                for o in c.get("outputs", []))
    )
    full = code_text + "\n" + md_text
    return {
        "code_sites": len(ch.PANDAS_ONLY.findall(code_text)),
        "mirror_sites": len(ch.markdown_pandas_sites(md_text)),
        "reshape_sites": len(ch.RESHAPE_SITES.findall(code_text)),
        "output_surface": output_surface,
        "fig_surface": len(re.findall(r"\{image\}", full)) + len(re.findall(r"#\|\s*fig-alt", full)),
        "prose_api_density": round(len(ch.PROSE_API.findall(md_text)) / md_lines, 3),
        "needs_network": bool(NETWORK_RE.search(code_text)),
    }


def assign_tier(m: Dict) -> str:
    if m["prose_api_density"] >= TIER_D_PROSE_DENSITY:
        return "D"
    if m["code_sites"] + m["mirror_sites"] == 0:
        return "A"
    if (
        m["code_sites"] + m["mirror_sites"] > TIER_C_SITES
        or m["output_surface"] > TIER_C_OUTPUTS
        or m["reshape_sites"] > TIER_C_RESHAPE
    ):
        return "C"
    return "B"


def triage(include_archived: bool = True) -> List[Dict]:
    lock = nb_baseline.read_lock()
    rows = []
    for chapter in ch.resolve(None, include_archived=include_archived):
        paths = nb_baseline.cached_paths(chapter, lock)
        base = paths["source"]
        if base is None:
            rows.append({
                "chapter": chapter.name,
                "tier": "D",
                "state": "PENDING",
                "note": "no baseline -- newly authored chapter",
                "writer": "chapter-author",
                "reviewers": REVIEWERS["D"],
                "attempts": 0,
                "debt_history": [],
            })
            continue

        m = measure(base)
        tier = assign_tier(m)
        rows.append({
            "chapter": chapter.name,
            "source": str(chapter.source),
            "baseline": str(base),
            "pytext": str(chapter.pytext) if chapter.is_notebook else None,
            "tier": tier,
            "writer": WRITER[tier],
            "reviewers": REVIEWERS[tier],
            "state": "PENDING",
            "attempts": 0,
            "debt_history": [],
            "reviewer_verdicts": [],
            "baseline_sha": lock["main_sha"],
            "in_toc": chapter.in_toc,
            "archived": chapter.archived,
            "is_notebook": chapter.is_notebook,
            **m,
        })

    # intro_lec names pandas as an ecosystem tool rather than teaching it, so it lands in B
    # by the numbers while still carrying prose a reviewer should read. One recorded
    # exception beats loosening the density threshold for everyone.
    for row in rows:
        if row["chapter"] == "intro_lec":
            row["prose_note"] = "ecosystem_mentions"
            if "notes-prose-reviewer" not in row["reviewers"]:
                row["reviewers"] = row["reviewers"] + ["notes-prose-reviewer"]

    rows.sort(key=lambda r: ("ABCD".index(r["tier"]), -(r.get("code_sites", 0) + r.get("mirror_sites", 0))))
    return rows


def merge_state(rows: List[Dict]) -> List[Dict]:
    """Keep orchestrator-owned progress fields when re-running triage."""
    if not STATE_PATH.exists():
        return rows
    prior = {r["chapter"]: r for r in json.loads(STATE_PATH.read_text())}
    for row in rows:
        old = prior.get(row["chapter"])
        if not old:
            continue
        for key in ("state", "attempts", "debt_history", "reviewer_verdicts", "blocked_reason"):
            if key in old:
                row[key] = old[key]
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description="Triage chapters into conversion tiers.")
    ap.add_argument("--json", default=str(STATE_PATH), help=f"Where to write the queue (default: {STATE_PATH})")
    ap.add_argument("--no-write", action="store_true", help="Print the table without writing state.json")
    ap.add_argument("--skip-archived", action="store_true")
    args = ap.parse_args()

    rows = merge_state(triage(include_archived=not args.skip_archived))

    hdr = f"{'chapter':<38} {'tier':<5} {'code':>5} {'mirr':>5} {'resh':>5} {'out':>4} {'fig':>4} {'dens':>6}  writer"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(
            f"{r['chapter']:<38} {r['tier']:<5} {r.get('code_sites', 0):>5} "
            f"{r.get('mirror_sites', 0):>5} {r.get('reshape_sites', 0):>5} "
            f"{r.get('output_surface', 0):>4} {r.get('fig_surface', 0):>4} "
            f"{r.get('prose_api_density', 0):>6}  {r.get('writer') or '-'}"
        )
    counts = {t: sum(1 for r in rows if r["tier"] == t) for t in "ABCD"}
    print("-" * len(hdr))
    print(
        f"{len(rows)} chapters   A(verify) {counts['A']}   B {counts['B']}   "
        f"C {counts['C']}   D(author) {counts['D']}"
    )
    net = [r["chapter"] for r in rows if r.get("needs_network")]
    if net:
        print(f"needs network to execute: {', '.join(net)}")

    if not args.no_write:
        Path(args.json).write_text(json.dumps(rows, indent=2) + "\n")
        print(f"wrote {args.json}")


if __name__ == "__main__":
    main()
