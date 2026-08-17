#!/usr/bin/env python3
"""
Chapter discovery for the course-notes conversion harness.

Every other script in `conversion/` addresses work by *chapter*, and a chapter is a
directory under `content/` holding exactly one `.ipynb` or `.md`. The directory name is
the key, not the file stem, because the two disagree often enough to matter:

    content/cv_regularization/cv_reg.ipynb
    content/logistic_regression_1/logistic_reg_1.ipynb
    content/constant_model_loss_transformations/loss_transformations.ipynb
    content/intro_lec/introduction.ipynb

`content/index.md` is the one file that lives at the content root; it is exposed as the
chapter `index` so the TOC and the gate battery can both address it.

Chapters prefixed with `_` are archived: they are absent from `myst.yml`'s TOC and so are
never rendered. They are still in scope for conversion (no pandas should survive anywhere
in `content/`), but the site gates cannot check them, so they are flagged rather than
silently treated like live chapters.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import yaml

CONTENT = Path("content")
MYST_YML = Path("myst.yml")
CHAPTER_MAP = Path("conversion/chapter_map.yml")
PYTEXT_ROOT = Path("conversion/pytext/polars")


@dataclass(frozen=True)
class Chapter:
    """One unit of conversion work."""

    name: str  # directory name under content/, e.g. "pandas_3"
    source: Path  # content/pandas_3/pandas_3.ipynb
    is_notebook: bool  # False for the prose-only .md chapters
    in_toc: bool  # present in myst.yml
    archived: bool  # directory name starts with "_"

    @property
    def dir(self) -> Path:
        return self.source.parent

    @property
    def pytext(self) -> Path:
        """Where the agent-editable jupytext file lives. Notebooks only."""
        return PYTEXT_ROOT / self.name / f"{self.source.stem}.py"

    @property
    def data_dir(self) -> Path:
        return self.dir / "data"


def toc_files() -> List[str]:
    """Every `file:` entry in myst.yml's toc, in order, as repo-relative strings."""
    cfg = yaml.safe_load(MYST_YML.read_text()) or {}
    entries = ((cfg.get("project") or {}).get("toc")) or []
    out = []
    for entry in entries:
        if isinstance(entry, dict) and "file" in entry:
            out.append(entry["file"])
    return out


def discover() -> Dict[str, Chapter]:
    """All chapters under content/, keyed by directory name."""
    toc = set(toc_files())
    found: Dict[str, Chapter] = {}

    root_index = CONTENT / "index.md"
    if root_index.exists():
        found["index"] = Chapter(
            name="index",
            source=root_index,
            is_notebook=False,
            in_toc=str(root_index) in toc,
            archived=False,
        )

    for d in sorted(p for p in CONTENT.iterdir() if p.is_dir()):
        # Anything without a source file at the top level of the directory is an asset
        # folder (images/, data/), not a chapter.
        sources = sorted(
            [p for p in d.glob("*.ipynb") if ".ipynb_checkpoints" not in p.parts]
            + list(d.glob("*.md"))
        )
        if not sources:
            continue
        if len(sources) > 1:
            raise RuntimeError(
                f"{d} holds {len(sources)} source files ({', '.join(s.name for s in sources)}); "
                "a chapter must hold exactly one so gates can address it unambiguously"
            )
        src = sources[0]
        found[d.name] = Chapter(
            name=d.name,
            source=src,
            is_notebook=src.suffix == ".ipynb",
            in_toc=str(src) in toc,
            archived=d.name.startswith("_"),
        )
    return found


def load_chapter_map() -> Dict[str, str]:
    """Converted chapter name -> baseline chapter name.

    Needed because tier-D chapters are renamed (`pandas_1` becomes `polars_1`) via
    `git mv`. Without the map, `nb_baseline.py` would look for `content/polars_1/` in a
    baseline commit that has never heard of it, and every id-aligned gate would report
    the whole chapter as new rather than converted.
    """
    if not CHAPTER_MAP.exists():
        return {}
    data = yaml.safe_load(CHAPTER_MAP.read_text()) or {}
    return dict(data.get("renames") or {})


def load_absorbed_chapters() -> List[str]:
    """Chapters that stopped existing rather than moving.

    A rename has a destination and the gates can follow it. An absorbed chapter has none: its
    material was folded into another chapter and its rendered pages simply stop existing. The
    site gate has to tell that apart from a page that failed to build, which looks identical
    from the outside.
    """
    if not CHAPTER_MAP.exists():
        return []
    data = yaml.safe_load(CHAPTER_MAP.read_text()) or {}
    return list(data.get("absorbed") or [])


def baseline_name(chapter: str) -> str:
    return load_chapter_map().get(chapter, chapter)


def resolve(names: Optional[List[str]] = None, include_archived: bool = True) -> List[Chapter]:
    """Resolve chapter names to Chapter objects; no names means all of them."""
    all_ch = discover()
    if names:
        missing = [n for n in names if n not in all_ch]
        if missing:
            raise SystemExit(
                f"unknown chapter(s): {', '.join(missing)}\n"
                f"known: {', '.join(sorted(all_ch))}"
            )
        return [all_ch[n] for n in names]
    return [c for c in all_ch.values() if include_archived or not c.archived]


# --------------------------------------------------------------- shared text scanners
#
# These live here rather than in nb_validate.py because nb_triage.py measures the same
# surfaces to assign tiers. One definition, so a tier and the gate that checks it can
# never disagree about what counts as a pandas site.

# Constructs with no Polars equivalent spelled the same way. Their presence in a
# converted file means the conversion is unfinished. Deliberately excludes idioms both
# libraries share (`.agg(`, `.str.`, `value_counts`, `.melt(`).
#
# `.to_frame(` was in this list and has been removed: **Polars spells it exactly the same way**
# (`pl.Series.to_frame()` returns a DataFrame), so it violates the rule this pattern states one
# line above and can never discriminate. It fired on correct Polars code in `polars_1` and would
# have fired on every future chapter that used it.
#
# `.astype(` and `.tolist(` stay, and the difference is worth naming: Polars spells those `.cast()`
# and `.to_list()`, so they *do* discriminate against Polars even though NumPy shares them. They
# cost the occasional rewrite of ndarray code (harness note 8) but never fire on correct Polars.
PANDAS_ONLY = re.compile(
    r"\bpd\.|\bimport pandas\b|\bfrom pandas\b|\.iloc\[|\.loc\[|\.groupby\("
    r"|\.astype\(|inplace\s*=|ascending\s*=|reset_index\(|set_index\("
    r"|\.isna\(|\.isnull\(|\.fillna\(|\.dropna\(|\.tolist\(|pivot_table\("
    r"|left_index|right_index|select_dtypes|\.sort_values\("
)

# Restructures rather than renames: these must go to an agent, never a regex pass.
RESHAPE_SITES = re.compile(
    r"groupby\([^)]*\)\.filter|pivot_table|\.loc\[|\.iloc\[|set_index"
    r"|agg\(\s*\{[^}]*\[|left_index|right_index|\.str\.split\([^)]*expand|\.stack\(|\.unstack\("
)

# pandas API vocabulary as it appears in *prose*. Used only to measure how much a chapter
# is about pandas, which is what separates a translation from a rewrite.
PROSE_API = re.compile(
    r"\bpandas\b|\bDataFrame\b|\bSeries\b|\bIndex\b|\bMultiIndex\b|\bGroupBy\b"
    r"|`\.loc`|`\.iloc`|`\.groupby|`pd\.|\bgroupby\b",
    re.I,
)

# One fence line: its backtick run and its info string ({dropdown}, python, or empty).
#
# This replaced a single regex that paired an opening fence with a closing one lazily:
#
#     r"^`{3,}[ \t]*(?:python|py)?[ \t]*\n(.*?)^`{3,}[ \t]*$"
#
# Because its language tag was optional, that pattern matched a *closing* fence as an
# opening one, and it got the answer wrong in both directions. In a prose chapter built
# from ```{image} blocks -- whose openers it correctly ignores -- it paired each block's
# closer with the next block's closer and scanned the *prose* in between as if it were
# code, reporting `_case_study_climate`'s narrative mention of xarray's `.groupby()` as an
# unconverted pandas site. And because `finditer` does not overlap, a single mispairing
# consumed the text after it and skipped real blocks: `modeling_slr` scanned as 1 site
# when it has 5, `eda` as 1 when it has 2.
#
# The second half is the dangerous half. A prose false positive gets argued with by
# whoever reads the diff; a missed fenced block means G3 reports a chapter clean while
# the published page still shows pandas -- the vacuous pass this battery exists to catch.
MD_FENCE_LINE = re.compile(r"^(`{3,})[ \t]*(\S*)")

# Info strings whose body is code. Bare ``` and ```python both are; ```{dropdown} is a
# container, and its *nested* python block is what carries the code.
CODE_FENCE_INFO = ("", "python", "py")

# The sanctioned interop escape. Polars goes straight to seaborn/plotly/sklearn wherever
# it works; a surviving .to_pandas() needs an allowlist entry with a written reason.
INTEROP = re.compile(r"\.to_pandas\(\)")


def normalize_source(src: str) -> str:
    """Match nb_pytext.normalize_cell_sources.

    The round trip normalizes line endings and strips trailing whitespace, so the first rebuild
    of a chapter produces a whitespace-only diff on cells nobody edited -- 20 of the 24 notebooks
    carry at least one such line. Comparing raw sources would report every one of them as a
    converted cell, which buries the real changes in the review.
    """
    src = src.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in src.split("\n")).strip()


def markdown_code_blocks(text: str) -> List[str]:
    """The bodies of fenced *code* blocks in markdown, nesting included.

    Fences are tracked with a stack rather than paired by regex, following CommonMark:
    a fence closes only on a run at least as long as the one that opened it *and* an
    empty info string. That is what lets the repo's 4-backtick ```{dropdown} wrap a
    3-backtick ```python block -- the inner ``` cannot close the outer fence, so the
    nesting survives, and a ```{image} block's closer can never be mistaken for the
    start of a code block.
    """
    blocks: List[str] = []
    stack: List[tuple] = []          # (backtick count, info string)
    bodies: List[List[str]] = []

    for line in text.splitlines():
        m = MD_FENCE_LINE.match(line)
        if m:
            ticks, info = len(m.group(1)), m.group(2)
            if stack and info == "" and ticks >= stack[-1][0]:
                _, opener = stack.pop()
                body = "\n".join(bodies.pop())
                if opener in CODE_FENCE_INFO:
                    blocks.append(body)
                continue
            stack.append((ticks, info))
            bodies.append([])
            continue
        if bodies:
            bodies[-1].append(line)

    # An unclosed fence is a MyST hazard in its own right, and its body is still content
    # the reader sees. Scan what we have rather than dropping it on the floor.
    while bodies:
        _, opener = stack.pop()
        body = "\n".join(bodies.pop())
        if opener in CODE_FENCE_INFO:
            blocks.append(body)
    return blocks


def markdown_pandas_sites(text: str) -> List[str]:
    """pandas sites inside fenced code blocks in markdown.

    88 sites across 12 chapters live here and nowhere else. A scanner that reads only
    code cells reports the chapter clean while the rendered page still shows pandas.
    """
    hits = []
    for body in markdown_code_blocks(text):
        for line in body.splitlines():
            if PANDAS_ONLY.search(line):
                hits.append(line.strip()[:80])
    return hits
