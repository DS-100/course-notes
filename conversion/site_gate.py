#!/usr/bin/env python3
"""
Repo-level gates: run once per batch, not once per chapter.

    G14 repo-invariants   nothing changed outside the chapter sources agents are allowed to edit
    G15 site-build        the rendered site is the deliverable, so build it and read it

G14 exists because the cheapest way for an agent to make a build go green is to stop building
the thing that fails: drop a chapter from the TOC, regenerate a 26 MB asset, edit a workflow.
Those changes are invisible in a notebook review and enormous in the diff, and 469 MB of data
plus 494 images sit in easy reach. Freezing them costs one `git diff --name-only`.

G15's size clause is the anti-vacuous-pass rule applied to the build: mystmd exits 0 on a page
that failed to render -- the page just comes out tiny. Comparing page sizes against a captured
baseline turns "the build succeeded" into "the build produced the site it produced before".
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

import chapters as ch
import nb_baseline

BUILD_DIR = Path("_build/html")
BASELINE_SITE = Path("conversion/baseline_site.json")
BASELINE_WARNINGS = Path("conversion/baseline_warnings.txt")
ALLOWLIST_PATH = Path("conversion/conversion_allowlist.yml")

# Paths no conversion agent has any business touching. `content/eda/ds100_utils.py` is here
# because it is dead -- zero references from any notebook -- so an edit to it is always
# either a mistake or an agent inventing work.
FROZEN = [
    "content/*/data/*",
    "content/*/images/*",
    ".github/*",
    "content/eda/ds100_utils.py",
    "assets/*",
]

# Changeable, but only with a recorded reason: the TOC moves when tier-D chapters are
# renamed, and requirements.txt gains the polars pin.
NEEDS_REASON = ["myst.yml", "requirements.txt"]

SHRINK_TOLERANCE = 0.5
PANDAS_DOCS = "pandas.pydata.org"
WARNING_RE = re.compile(r"^.*?\b(warn|warning|error)\b.*$", re.I | re.M)

# Jupyter Book v2 does not emit pre-rendered page HTML. `_build/html/<slug>.json` carries the
# content and the .html files are the React shell that hydrates from it -- so the pandas repr
# reaches the reader as JSON-escaped `class=\"dataframe\"`, and a search for the literal
# `class="dataframe"` finds nothing at all. Measured on the unconverted tree: 147 reprs across
# 16 pages that the literal form scored as zero. A gate written the obvious way would have read
# green from the first run to the last.
PANDAS_REPR_RE = re.compile(r'class=\\?"dataframe')


def git(*args: str) -> str:
    out = subprocess.run(["git", *args], capture_output=True, text=True, check=False)
    if out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {out.stderr.strip()}")
    return out.stdout


def repo_allowlist() -> Dict[str, str]:
    if not ALLOWLIST_PATH.exists():
        return {}
    data = yaml.safe_load(ALLOWLIST_PATH.read_text()) or {}
    entries = (data.get("_repo") or {}).get("changed_paths", []) or []
    return {e["path"]: e.get("reason", "") for e in entries}


def changed_paths(baseline_sha: str) -> List[str]:
    """Every path that differs from the baseline, committed or not."""
    tracked = git("diff", "--name-only", baseline_sha).splitlines()
    untracked = git("ls-files", "--others", "--exclude-standard").splitlines()
    return sorted(set(p for p in tracked + untracked if p.strip()))


def matches(path: str, patterns: List[str]) -> bool:
    return any(Path(path).match(p) for p in patterns)


def gate_repo_invariants(baseline_sha: str) -> Tuple[bool, List[str]]:
    allowed = repo_allowlist()
    changed = changed_paths(baseline_sha)
    problems = []

    for p in changed:
        if p in allowed:
            continue
        if matches(p, FROZEN):
            problems.append(f"frozen path modified: {p}")
        elif p in NEEDS_REASON:
            problems.append(
                f"{p} changed with no recorded reason -- add it under `_repo: changed_paths:` "
                "in conversion_allowlist.yml"
            )

    detail = problems or [
        f"{len(changed)} path(s) changed, none of them frozen"
        + (f"; {len(allowed)} allowlisted" if allowed else "")
    ]
    return not problems, detail


def build_site(capture: bool = False) -> Tuple[bool, str, List[str]]:
    """Run the same command the deploy workflow runs."""
    proc = subprocess.run(
        ["jupyter-book", "build", "--html"], capture_output=True, text=True, check=False
    )
    log = proc.stdout + proc.stderr
    warnings = sorted(
        set(
            re.sub(r"^\s*", "", line).strip()
            for line in WARNING_RE.findall(log)
            if line.strip()
        )
    )
    if capture:
        BASELINE_WARNINGS.write_text("\n".join(warnings) + ("\n" if warnings else ""))
    return proc.returncode == 0, log, warnings


def page_sizes() -> Dict[str, int]:
    if not BUILD_DIR.exists():
        return {}
    return {
        str(p.relative_to(BUILD_DIR)): p.stat().st_size
        for p in sorted(BUILD_DIR.rglob("*"))
        if p.is_file()
    }


def scan_rendered() -> Tuple[int, int]:
    """Count pandas artifacts as they actually reach a reader. Returns (reprs, doc links)."""
    reprs = links = 0
    for p in list(BUILD_DIR.rglob("*.json")) + list(BUILD_DIR.rglob("*.html")):
        text = p.read_text(errors="ignore")
        reprs += len(PANDAS_REPR_RE.findall(text))
        links += text.count(PANDAS_DOCS)
    return reprs, links


def gate_site_build(capture: bool) -> Tuple[bool, List[str]]:
    ok, log, warnings = build_site(capture=capture)
    problems = []

    if not ok:
        tail = "\n".join(log.strip().splitlines()[-6:])
        return False, [f"jupyter-book build --html exited non-zero:\n{tail}"]

    sizes = page_sizes()
    reprs, links = scan_rendered()

    if capture:
        BASELINE_SITE.write_text(
            json.dumps(
                {"artifacts": sizes, "pandas_reprs": reprs, "pandas_doc_links": links},
                indent=2,
                sort_keys=True,
            )
        )
        return True, [
            f"captured {len(sizes)} artifact(s) and {len(warnings)} warning(s) as the baseline",
            f"baseline site carries {reprs} pandas repr(s) and {links} pandas doc link(s) -- "
            "the detectors must find these, or they are not looking in the right place",
        ]

    # (b) one artifact per TOC entry, none of them suspiciously small
    if not BASELINE_SITE.exists():
        problems.append("no baseline site capture; run --capture-baseline on a clean tree first")
        capture_data = {}
    else:
        capture_data = json.loads(BASELINE_SITE.read_text())
        baseline = capture_data.get("artifacts", {})
        renames = ch.load_chapter_map()
        for path, size in baseline.items():
            if any(old in path for old in renames.values()):
                continue  # the chapter moved on purpose; the rename map records it
            now = sizes.get(path)
            if now is None:
                problems.append(f"artifact no longer rendered: {path}")
            elif now < size * SHRINK_TOLERANCE:
                problems.append(f"{path} shrank {size} -> {now} bytes; the page likely failed to render")

    toc = ch.toc_files()
    if not sizes:
        problems.append(f"{BUILD_DIR} is empty after a successful build")
    elif len(sizes) < len(toc):
        problems.append(f"{len(sizes)} artifact(s) for {len(toc)} TOC entries")

    # (c) no new warnings
    if BASELINE_WARNINGS.exists():
        known = set(BASELINE_WARNINGS.read_text().splitlines())
        new = [w for w in warnings if w not in known]
        for w in new[:5]:
            problems.append(f"new build warning: {w[:110]}")

    # (d,e) the rendered site is the deliverable: read what a reader receives, not the source.
    #
    # Rule 2 applied to a repo-level gate. A detector that finds zero is only good news if it
    # found something on the baseline; otherwise "0 pandas reprs" means the scanner is looking
    # in the wrong place, which is exactly what happened when this searched for the unescaped
    # `class="dataframe"` in .html files that carry no content at all.
    base_reprs = capture_data.get("pandas_reprs")
    base_links = capture_data.get("pandas_doc_links")
    if base_reprs is not None and base_reprs == 0 and base_links == 0:
        problems.append(
            "the baseline capture found no pandas anywhere in the rendered site, which cannot "
            "be true -- re-capture, and check PANDAS_REPR_RE against the build layout"
        )
    if reprs:
        problems.append(f"{reprs} pandas dataframe repr(s) reach the reader (baseline had {base_reprs})")
    if links:
        problems.append(f"{links} link(s) to {PANDAS_DOCS} reach the reader (baseline had {base_links})")

    detail = problems or [
        f"built {len(sizes)} artifact(s) for {len(toc)} TOC entries; {len(warnings)} warning(s), "
        f"none new; 0 pandas reprs and 0 pandas doc links reach the reader "
        f"(baseline had {base_reprs} and {base_links})"
    ]
    return not problems, detail


def main() -> None:
    ap = argparse.ArgumentParser(description="Repo-level conversion gates.")
    ap.add_argument("--capture-baseline", action="store_true",
                    help="Build a clean tree and record page sizes + warnings as the reference")
    ap.add_argument("--skip-build", action="store_true", help="Run G14 only")
    args = ap.parse_args()

    lock = nb_baseline.read_lock()
    print(f"\n{'=' * 78}\n  repo gates (baseline {lock['main_sha'][:12]})\n{'=' * 78}")

    results = []

    if not args.capture_baseline:
        ok, details = gate_repo_invariants(lock["main_sha"])
        results.append(("repo-invariants", ok, details))

    if not args.skip_build:
        ok, details = gate_site_build(capture=args.capture_baseline)
        results.append(("site-build", ok, details))

    for name, ok, details in results:
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}")
        for d in details[:10]:
            for line in str(d).splitlines():
                print(f"           {line}")

    failed = [n for n, ok, _ in results if not ok]
    print("-" * 78)
    print(f"  {'REPO GATES PASSED' if not failed else 'REPO GATES FAILED: ' + ', '.join(failed)}\n")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
