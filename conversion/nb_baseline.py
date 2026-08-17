#!/usr/bin/env python3
"""
Materialize the pandas baseline every gate compares against.

The baseline is a git commit, not a checked-in copy of the content tree. The sibling repo
needed a committed `pytext/pandas/` tree because its baseline came from a *different*
repository; here the baseline is a direct ancestor on this branch, so committing a second
copy of 24 notebooks would duplicate ~7 MB git already stores and create a second source
of truth that can silently drift from `main`.

Two things make that safe:

  * `conversion/baseline.lock` pins the sha. If course staff push to `main` mid-conversion,
    every gate's expected values would otherwise shift underneath the work and a green
    chapter would change verdict with no code change. `--refresh` bumps the pin and prints
    what moved, so a baseline bump is an explicit, reviewed event.

  * The cache key includes a digest of `nb_pytext.py`. Baseline and converted `.py` must be
    produced by the same writer, or `gate_structure` reports converter-version artifacts as
    structural drift.

Because tier-D chapters are renamed (`pandas_1` -> `polars_1`), lookups go through
`conversion/chapter_map.yml`; without it the baseline for `polars_1` would not exist in a
commit that has never heard of that directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import chapters as ch
import nb_pytext

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

LOCK_PATH = Path("conversion/baseline.lock")
CACHE_ROOT = Path("conversion/.baseline")
CONVERTER = Path("conversion/nb_pytext.py")


def git(*args: str) -> str:
    out = subprocess.run(
        ["git", *args], capture_output=True, text=True, check=False
    )
    if out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {out.stderr.strip()}")
    return out.stdout


def converter_digest() -> str:
    return hashlib.sha1(CONVERTER.read_bytes()).hexdigest()[:12]


def read_lock() -> Dict[str, str]:
    if not LOCK_PATH.exists():
        raise SystemExit(
            "conversion/baseline.lock is missing. Run:  python conversion/nb_baseline.py --init"
        )
    return json.loads(LOCK_PATH.read_text())


def write_lock(main_sha: str) -> Dict[str, str]:
    lock = {
        "main_sha": main_sha,
        "converter_sha": converter_digest(),
        "captured_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOCK_PATH.write_text(json.dumps(lock, indent=2) + "\n")
    return lock


def cache_dir(lock: Dict[str, str]) -> Path:
    return CACHE_ROOT / f"{lock['main_sha'][:12]}-{lock['converter_sha']}"


def baseline_source(sha: str, chapter_name: str) -> Optional[str]:
    """The repo-relative path of a chapter's source file as of `sha`."""
    base = ch.baseline_name(chapter_name)
    listing = git("ls-tree", "--name-only", sha, f"content/{base}/")
    files = [
        line
        for line in listing.splitlines()
        if line.endswith((".ipynb", ".md")) and ".ipynb_checkpoints" not in line
    ]
    if len(files) == 1:
        return files[0]
    if not files:
        return None
    raise RuntimeError(f"{base} has {len(files)} source files at {sha[:12]}: {files}")


def materialize(chapter: ch.Chapter, lock: Dict[str, str], force: bool = False) -> Optional[Path]:
    """Write the chapter's baseline source (and .py, for notebooks) into the cache.

    Returns the cached source path, or None when the chapter has no baseline at all --
    which is the correct answer for a newly authored tier-D chapter, not an error.
    """
    sha = lock["main_sha"]
    if chapter.name == "index":
        rel = "content/index.md"
        if not git("ls-tree", "--name-only", sha, rel).strip():
            return None
    else:
        rel = baseline_source(sha, chapter.name)
        if rel is None:
            return None

    dest = cache_dir(lock) / rel
    if dest.exists() and not force:
        return dest

    dest.parent.mkdir(parents=True, exist_ok=True)
    blob = subprocess.run(
        ["git", "show", f"{sha}:{rel}"], capture_output=True, check=True
    ).stdout
    dest.write_bytes(blob)

    if dest.suffix == ".ipynb":
        py_dest = dest.with_suffix(".py")
        problems = nb_pytext.ipynb_to_py(dest, py_dest, verify=True)
        if problems:
            # A baseline that cannot round-trip cannot anchor a gate. Fail loudly here
            # rather than letting every downstream gate report phantom drift.
            dest.unlink(missing_ok=True)
            raise RuntimeError(
                f"{rel} does not round-trip cleanly at {sha[:12]}: {problems[0]}"
            )
    return dest


def cached_paths(chapter: ch.Chapter, lock: Dict[str, str]) -> Dict[str, Optional[Path]]:
    """What the gates ask for: the baseline .ipynb and .py for a chapter."""
    src = materialize(chapter, lock)
    if src is None:
        return {"source": None, "pytext": None}
    return {"source": src, "pytext": src.with_suffix(".py") if src.suffix == ".ipynb" else None}


def refresh(new_sha: Optional[str]) -> None:
    """Re-pin the baseline and report what moved, so the bump is a reviewed decision."""
    old = read_lock()
    target = new_sha or git("rev-parse", "main").strip()
    if target == old["main_sha"] and converter_digest() == old["converter_sha"]:
        logger.info(f"baseline already at {target[:12]}; nothing to do")
        return

    if target != old["main_sha"]:
        diff = git("diff", "--stat", f"{old['main_sha']}..{target}", "--", "content", "myst.yml")
        print(f"\nBaseline {old['main_sha'][:12]} -> {target[:12]}")
        print(diff or "  (no changes under content/ or myst.yml)")
    if converter_digest() != old["converter_sha"]:
        print(f"\nConverter changed: {old['converter_sha']} -> {converter_digest()}")
        print("  every cached baseline .py will be regenerated")

    lock = write_lock(target)
    logger.info(f"pinned baseline to {lock['main_sha'][:12]} / converter {lock['converter_sha']}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Materialize the pinned pandas baseline.")
    ap.add_argument("--init", action="store_true", help="Create baseline.lock from current main")
    ap.add_argument("--refresh", action="store_true", help="Re-pin the baseline and show what moved")
    ap.add_argument("--sha", help="Explicit sha for --init/--refresh (default: main)")
    ap.add_argument("--chapter", action="append", help="Chapter to materialize (repeatable)")
    ap.add_argument("--all", action="store_true", help="Materialize every chapter")
    ap.add_argument("--force", action="store_true", help="Rewrite cached files that already exist")
    args = ap.parse_args()

    if args.init:
        sha = args.sha or git("rev-parse", "main").strip()
        lock = write_lock(sha)
        logger.info(f"wrote {LOCK_PATH}: main {lock['main_sha'][:12]}, converter {lock['converter_sha']}")
        return

    if args.refresh:
        refresh(args.sha)
        return

    lock = read_lock()
    if converter_digest() != lock["converter_sha"]:
        raise SystemExit(
            f"nb_pytext.py has changed since the baseline was pinned "
            f"({lock['converter_sha']} -> {converter_digest()}).\n"
            "Baseline and converted .py must come from the same writer, or structure gates\n"
            "report converter drift as conversion drift. Run:  --refresh"
        )

    targets: List[ch.Chapter] = ch.resolve(args.chapter) if args.chapter else (
        ch.resolve(None) if args.all else []
    )
    if not targets:
        raise SystemExit("nothing to do: pass --chapter <name>, --all, --init, or --refresh")

    made, absent = 0, []
    for chapter in targets:
        try:
            path = materialize(chapter, lock, force=args.force)
        except RuntimeError as e:
            logger.error(f"{chapter.name}: {e}")
            sys.exit(1)
        if path is None:
            absent.append(chapter.name)
        else:
            made += 1
    print(f"\nbaseline {lock['main_sha'][:12]}: {made} chapter(s) materialized into {cache_dir(lock)}")
    if absent:
        print(f"  no baseline (new chapters): {', '.join(absent)}")


if __name__ == "__main__":
    main()
