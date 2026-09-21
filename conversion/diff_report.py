#!/usr/bin/env python3
"""Per-chapter change reports: the pinned pandas baseline -> this branch.

One report per chapter under `conversion/_diff/`, indexed by `CHANGES.md` at the repo root.
Every difference is a numbered change carrying a category, a `**Why:**`, and a verdict slot a
reviewer fills by hand.  Re-running keeps what is already written; only `--force` overwrites.

Two things are diffed, because in this repo they can disagree:

  source   the notebook as text.  Both sides go through `nb_pytext.to-py`, so the comparison is
           the same percent-format view a writer agent edits, with cell ids ignored.
  outputs  the committed outputs.  CI never executes (AGENTS.md hard rule 1), so a cell whose
           output was not regenerated ships Polars code above a pandas table and no gate sees it.
           A source diff cannot see this at all, which is why it gets its own pass.

Markdown chapters have no notebook; they are diffed directly.

Categories:

  output      a committed cell output moved -- what the reader actually sees
  code        inside a code cell
  dropdown    inside a ```{dropdown} Click to see the code block (hard rule 3: the dropdown and
              its code cell are one edit, so these are cross-checked against the code changes)
  tab-twins   inside a tab-twins marker pair
  prose       markdown re-authored beyond a library rename -- the REVIEW category
  mixed       one hunk spanning code and prose -- also REVIEW
  mechanical  wording whose only differences are library renames
  metadata    cell tags / notebook metadata
  whitespace  blank lines only

Usage (from the repo root, with the d100 env on PATH):

    python conversion/diff_report.py                 # write missing reports, rebuild the index
    python conversion/diff_report.py --force         # overwrite reports (loses hand-written text)
    python conversion/diff_report.py --index         # rebuild CHANGES.md only
    python conversion/diff_report.py --chapter eda   # one chapter
"""

from __future__ import annotations

import argparse
import collections
import difflib
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONVERSION = ROOT / "conversion"
OUT = CONVERSION / "_diff"
INDEX = ROOT / "CHANGES.md"
STATE = CONVERSION / "state.json"
LOCK = CONVERSION / "baseline.lock"
CHAPTER_MAP = CONVERSION / "chapter_map.yml"

REVIEW = {"prose", "mixed"}

MECHANICAL = [
    (re.compile(r"\bpandas\b|\bPandas\b|\bPANDAS\b"), "Polars"),
    (re.compile(r"\bpolars\b"), "Polars"),
    (re.compile(r"\bpd\."), "pl."),
    (re.compile(r"\b[Dd]ata[Ff]rames?\b"), "DataFrame"),
    (re.compile(r"\bgroupby\b"), "group_by"),
    (re.compile(r"\bpivot_table\b"), "pivot"),
    (re.compile(r"\bsort_values\b"), "sort"),
    (re.compile(r"\bpython\b"), "Python"),
    (re.compile(r"\s+"), " "),
]


def norm(s: str) -> str:
    s = s.strip()
    for pat, repl in MECHANICAL:
        s = pat.sub(repl, s)
    return s.strip()


def baseline_sha() -> str:
    return json.loads(LOCK.read_text())["main_sha"]


def renames() -> dict[str, str]:
    """Converted chapter dir -> baseline chapter dir (tier D chapters were `git mv`d)."""
    out: dict[str, str] = {}
    if not CHAPTER_MAP.exists():
        return out
    in_block = False
    for line in CHAPTER_MAP.read_text().splitlines():
        if re.match(r"^renames:\s*$", line):
            in_block = True
            continue
        if in_block:
            m = re.match(r"^\s+(\w+):\s*(\w+)\s*$", line)
            if m:
                out[m.group(1)] = m.group(2)
            elif line.strip() and not line.startswith((" ", "\t", "#")):
                break
    return out


def absorbed() -> list[str]:
    """Chapters that stopped existing rather than moving (chapter_map.yml `absorbed:`).

    A renamed chapter still has a report, because its baseline is reachable through the rename
    map. A chapter that was dissolved into another one has no current path at all, so nothing in
    state.json points at it and it would otherwise vanish from the index entirely -- which is the
    wrong outcome for what is usually the largest content decision on a branch.
    """
    out: list[str] = []
    if not CHAPTER_MAP.exists():
        return out
    in_block = False
    for line in CHAPTER_MAP.read_text().splitlines():
        if re.match(r"^absorbed:\s*$", line):
            in_block = True
            continue
        if in_block:
            m = re.match(r"^\s+-\s*(\S+)\s*$", line)
            if m:
                out.append(m.group(1))
            elif line.strip() and not line.startswith((" ", "\t", "#")):
                break
    return out


def sections(nb: dict) -> list[tuple[int, str, str]]:
    """(level, heading, body text) for each markdown heading in a notebook."""
    out: list[tuple[int, str, list[str]]] = []
    for c in nb.get("cells", []):
        if c.get("cell_type") != "markdown":
            continue
        for line in "".join(c["source"]).splitlines():
            m = re.match(r"^(#{2,4})\s+(.+)$", line.strip())
            if m:
                out.append((len(m.group(1)), m.group(2).strip(), []))
            elif out:
                out[-1][2].append(line)
    return [(lvl, h, "\n".join(body)) for lvl, h, body in out]


def sentences(text: str, min_words: int = 8) -> list[str]:
    flat = re.sub(r"\s+", " ", text)
    return [x.strip() for x in re.split(r"(?<=[.!?]) ", flat)
            if len(x.split()) >= min_words]


def render_absorbed(name: str, src: str, host: str, base_nb: dict, host_nb: dict,
                    assets: dict) -> str:
    """Report for a chapter that was dissolved into another one."""
    base_secs = sections(base_nb)
    host_text = re.sub(r"\s+", " ", " ".join(
        "".join(c["source"]) for c in host_nb.get("cells", []) if c.get("cell_type") == "markdown"))
    host_heads = [h for _, h, _ in sections(host_nb)]
    md = sum(1 for c in base_nb.get("cells", []) if c.get("cell_type") == "markdown")
    code = sum(1 for c in base_nb.get("cells", []) if c.get("cell_type") == "code")
    words = sum(len("".join(c["source"]).split())
                for c in base_nb.get("cells", []) if c.get("cell_type") == "markdown")

    L = [f"# {name} — removed chapter report", "",
         f"`{src}` → dissolved into `{host}`", "",
         f"**{md} markdown cells · {code} code cells · ~{words} words of prose.** This chapter was "
         "not converted and not renamed. It was taken apart: some of it was carried into the host "
         "chapter and the rest was dropped with the concept it taught. It has no entry anywhere "
         "else, so this is the only record of what a reader loses.", ""]
    L.append("Per section, *kept verbatim* counts sentences of eight words or more that survive "
             "word-for-word in the host chapter. A low count is not by itself a loss — prose was "
             "re-authored throughout — so the verdict is the judgement, not the number.")
    L.append("")
    L.append("| section | sentences | kept verbatim | heading in host |")
    L.append("|---|---|---|---|")
    rows = []
    for lvl, head, body in base_secs:
        sents = sentences(body)
        kept = sum(1 for x in sents if x in host_text)
        # Exact match only. A fuzzy match here invents a correspondence ("From a Dictionary"
        # -> "From a CSV File") that reads as fact in a table; where the mapping is real but not
        # literal, the annotator states it in `Became:`.
        norm_head = head.lower().replace("`", "").strip()
        near = next((h for h in host_heads
                     if h.lower().replace("`", "").strip() == norm_head), "")
        rows.append((head, len(sents), kept, near or "—"))
        L.append(f"| {'&nbsp;' * 2 * (lvl - 2)}{head} | {len(sents)} | {kept} | {near or '—'} |")
    L.append("")
    if assets:
        L.append("## Assets")
        L.append("")
        for k, v in assets.items():
            L.append(f"- **{k}** — {v}")
        L.append("")
    L += ["## Summary", "", "_(to fill)_", "",
          "## Sections", ""]
    for i, (head, n, kept, near) in enumerate(rows, 1):
        L.append(f'<a id="s{i}"></a>')
        L.append(f"### S{i} · {head}")
        L.append("")
        L.append(f"{n} sentences, {kept} kept verbatim, host heading: {near}")
        L.append("")
        L.append("**Became:** _(to fill)_")
        L.append("**Reader loses:** _(nothing | what)_")
        L.append("")
    return "\n".join(L) + "\n"


def baseline_path(rel: str, ren: dict[str, str]) -> str:
    """content/polars_1/polars_1.ipynb -> content/pandas_2/pandas_2.ipynb"""
    parts = rel.split("/")
    if len(parts) >= 2 and parts[0] == "content" and parts[1] in ren:
        old = ren[parts[1]]
        parts[1] = old
        parts[-1] = re.sub(r"^[^.]+", old, parts[-1])
    return "/".join(parts)


def git_show(sha: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "show", f"{sha}:{path}"], cwd=ROOT, capture_output=True)
    return r.stdout if r.returncode == 0 else None


# ----------------------------------------------------------------------------- source view


def to_py(nb_path: Path, dest: Path) -> list[str] | None:
    """Percent-format view of a notebook, via the repo's own converter."""
    r = subprocess.run(
        [sys.executable, str(CONVERSION / "nb_pytext.py"), "to-py",
         "--input", str(nb_path), "--output", str(dest), "--no-verify"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if r.returncode != 0 or not dest.exists():
        print(f"  to-py failed for {nb_path}: {r.stderr.strip()[:200]}", file=sys.stderr)
        return None
    return strip_ids(dest.read_text().splitlines())


def strip_ids(lines: list[str]) -> list[str]:
    return [re.sub(r'\s+id="[0-9a-fA-F-]+"', "", l) for l in lines]


CELL_RE = re.compile(r"^# %%(?: \[(\w+)\])?(.*)$")


@dataclass
class LineInfo:
    cell: str = "code"
    section: str = ""
    in_code: bool = False
    dropdown: bool = False
    twins: bool = False


def annotate(lines: list[str], kind: str = "notebook") -> list[LineInfo]:
    """Percent-format notebooks carry cell markers; a plain .md chapter does not, so there
    everything is prose except what sits inside a fenced code block."""
    if kind == "markdown":
        return annotate_markdown(lines)
    info: list[LineInfo] = []
    cell = "code"
    section = "(top)"
    n = 0
    dropdown = twins = False
    for line in lines:
        stripped = line.strip()
        m = CELL_RE.match(line)
        if m:
            cell = m.group(1) or "code"
            n += 1
            dropdown = twins = False
            section = f"cell {n} [{cell}]"
        if cell == "markdown":
            h = re.match(r"^# (#+ .+)$", line.rstrip())
            if h:
                section = f"cell {n}: {h.group(1).lstrip('# ').strip()[:60]}"
            if "```{dropdown}" in line:
                dropdown = True
            elif dropdown and stripped in ("# ```", "#```"):
                dropdown = False
            if "tab-twins:begin" in line:
                twins = True
            elif "tab-twins:end" in line:
                twins = False
        info.append(LineInfo(cell=cell, section=section, in_code=(cell == "code"),
                             dropdown=dropdown, twins=twins))
    return info


def annotate_markdown(lines: list[str]) -> list[LineInfo]:
    info: list[LineInfo] = []
    fence = False
    section = "(top)"
    dropdown = twins = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            info.append(LineInfo(cell="markdown", section=section, in_code=True,
                                 dropdown=dropdown, twins=twins))
            if not fence and "{dropdown}" in stripped:
                dropdown = True
            elif fence and dropdown:
                dropdown = False
            fence = not fence
            continue
        if not fence:
            h = re.match(r"^(#+)\s+(.+)$", stripped)
            if h:
                section = h.group(2).strip()[:60]
            if "tab-twins:begin" in line:
                twins = True
            elif "tab-twins:end" in line:
                twins = False
        info.append(LineInfo(cell="markdown", section=section, in_code=fence,
                             dropdown=dropdown, twins=twins))
    return info


@dataclass
class Change:
    idx: int
    tag: str
    old: list[str]
    new: list[str]
    old_start: int
    new_start: int
    section: str
    category: str = ""
    notes: list[str] = field(default_factory=list)


def classify(ch: Change, old_i: list[LineInfo], new_i: list[LineInfo]) -> None:
    oi = old_i[ch.old_start - 1: ch.old_start - 1 + len(ch.old)]
    ni = new_i[ch.new_start - 1: ch.new_start - 1 + len(ch.new)]
    infos = oi + ni
    stripped = [l.strip() for l in ch.old + ch.new]

    if not any(stripped):
        ch.category = "whitespace"
        return
    # Only true cell/metadata markers. `# -` and `# +` are jupytext cell delimiters and stand
    # alone; `# - Understand ...` is a markdown bullet, which is prose and must reach review.
    meta = re.compile(r'^#\s*%%|^#\s*[+-]\s*$|^#\s*---\s*$|^#\s*(jupyter|kernelspec|jupytext|'
                      r'language_info|name|display_name|version|codemirror_mode|file_extension|'
                      r'mimetype|nbconvert_exporter|pygments_lexer|text_representation|'
                      r'extension|format_name|format_version|jupytext_version)\s*:')
    if all(meta.match(s) for s in stripped if s):
        ch.category = "metadata"
        return

    side = ni if ni else oi
    if any(i.in_code for i in infos):
        ch.category = "code" if all(i.in_code for i in infos) else "mixed"
        if any(i.in_code for i in infos) and not all(i.in_code for i in infos):
            ch.notes.append("spans code and prose")
        if ch.category == "code":
            return
    if any(i.dropdown for i in side):
        ch.category = "dropdown"
        ch.notes.append("mirror of the next code cell (hard rule 3)")
        return
    if any(i.twins for i in side):
        ch.category = "tab-twins"
        return
    if ch.category == "mixed":
        return

    old_n = [norm(l) for l in ch.old if l.strip()]
    new_n = [norm(l) for l in ch.new if l.strip()]
    if old_n == new_n:
        ch.category = "mechanical"
        return
    ch.category = "prose"
    if ch.tag == "replace" and len(old_n) == len(new_n):
        same = sum(a == b for a, b in zip(old_n, new_n))
        if same:
            ch.notes.append(f"{same}/{len(old_n)} lines are pure renames")


def source_changes(old: list[str], new: list[str], kind: str = "notebook") -> list[Change]:
    old_i, new_i = annotate(old, kind), annotate(new, kind)
    sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
    out: list[Change] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        ref = new_i[j1] if (tag != "delete" and j1 < len(new_i)) else old_i[min(i1, len(old_i) - 1)]
        ch = Change(len(out) + 1, tag, old[i1:i2], new[j1:j2], i1 + 1, j1 + 1, ref.section)
        classify(ch, old_i, new_i)
        out.append(ch)
    return out


# ----------------------------------------------------------------------------- output view


def summarize_outputs(cell: dict) -> list[str]:
    """One readable line per output payload; images collapse to a digest so a re-render shows."""
    lines: list[str] = []
    for o in cell.get("outputs", []):
        t = o.get("output_type")
        if t == "stream":
            lines += [f"[{o.get('name', 'stdout')}] {l.rstrip()}"
                      for l in "".join(o.get("text", [])).splitlines()]
        elif t == "error":
            lines.append(f"[error] {o.get('ename')}: {o.get('evalue')}")
        elif t in ("execute_result", "display_data"):
            data = o.get("data", {})
            for mime in ("text/plain", "text/html"):
                if mime in data:
                    txt = "".join(data[mime])
                    if mime == "text/html":
                        klass = "dataframe" if 'class="dataframe"' in txt else "html"
                        lines.append(f"[{klass}] {len(txt)} chars"
                                     + (" · PANDAS REPR" if 'class="dataframe"' in txt else ""))
                    else:
                        lines += [f"[text] {l.rstrip()}" for l in txt.splitlines()]
                    break
            for mime in ("image/png", "image/jpeg", "image/svg+xml"):
                if mime in data:
                    blob = "".join(data[mime]).encode()
                    lines.append(f"[{mime}] {len(blob)} bytes "
                                 f"md5:{hashlib.md5(blob).hexdigest()[:10]}")
            if "application/vnd.plotly.v1+json" in data:
                lines += summarize_plotly(data["application/vnd.plotly.v1+json"])
    return lines


def summarize_plotly(payload) -> list[str]:
    """Describe a plotly figure in terms a reviewer can act on.

    Plotly figures here carry no text or raster fallback, so without this they are invisible to
    the diff: both sides summarize to nothing and a changed figure reports no change. The digest
    covers the whole payload; the per-trace lines say *what* moved, since a shifted point matters
    and a re-serialization does not.
    """
    if isinstance(payload, list):
        payload = json.loads("".join(payload))
    blob = json.dumps(payload, sort_keys=True).encode()
    out = [f"[plotly] figure md5:{hashlib.md5(blob).hexdigest()[:10]}"]
    fig = payload.get("data", payload) if isinstance(payload, dict) else payload
    traces = fig if isinstance(fig, list) else fig.get("data", []) if isinstance(fig, dict) else []
    for i, tr in enumerate(traces if isinstance(traces, list) else []):
        if not isinstance(tr, dict):
            continue
        bits = [f"[plotly] trace {i} {tr.get('type', '?')}"]
        if tr.get("name"):
            bits.append(f"name={tr['name']!r}")
        for axis in ("x", "y", "z"):
            v = tr.get(axis)
            if isinstance(v, list) and v:
                nums = [q for q in v if isinstance(q, (int, float))]
                if nums:
                    bits.append(f"{axis}: n={len(v)} min={min(nums):.6g} max={max(nums):.6g}")
                else:
                    bits.append(f"{axis}: n={len(v)}")
        out.append(" ".join(bits))
    layout = payload.get("layout") if isinstance(payload, dict) else None
    if isinstance(layout, dict):
        title = layout.get("title")
        if isinstance(title, dict):
            title = title.get("text")
        if title:
            out.append(f"[plotly] title={title!r}")
    return out


def cell_label(cell: dict) -> str:
    src = "".join(cell.get("source", [])).strip().splitlines()
    first = next((l for l in src if l.strip() and not l.strip().startswith("#")), src[0] if src else "")
    return first.strip()[:70]


def output_changes(base_nb: dict, cur_nb: dict, start_idx: int) -> list[Change]:
    """Pair code cells by id, and fall back to position only when the notebooks are plainly
    the same notebook edited in place.

    An authored rewrite shares almost no cell ids with its baseline, and pairing those by
    position invents a correspondence between cells that have nothing to do with each other —
    the `-` half of every hunk would belong to an unrelated cell. Where that is the case the
    baseline side is left empty and the change is marked unpaired instead.
    """
    def codecells(nb):
        return [c for c in nb.get("cells", []) if c.get("cell_type") == "code"]

    b, c = codecells(base_nb), codecells(cur_nb)
    by_id = {x.get("id"): x for x in b if x.get("id")}
    shared = sum(1 for x in c if x.get("id") in by_id)
    positional = shared >= 0.5 * min(len(b), len(c)) if b and c else False

    used, pairs = set(), []
    for n, cur in enumerate(c):
        cid = cur.get("id")
        if cid and cid in by_id:
            pairs.append((by_id[cid], cur, True)); used.add(cid)
        elif positional and n < len(b) and b[n].get("id") not in used:
            pairs.append((b[n], cur, True)); used.add(b[n].get("id"))
        else:
            pairs.append((None, cur, False))

    out: list[Change] = []
    for old_cell, cur, paired in pairs:
        ob = summarize_outputs(old_cell) if old_cell else []
        nb_ = summarize_outputs(cur)
        if ob == nb_:
            continue
        ch = Change(start_idx + len(out), "replace", ob, nb_, 0, 0,
                    f"`{cell_label(cur)}`", category="output")
        if any("PANDAS REPR" in l for l in nb_):
            ch.notes.append("**still renders a pandas table**")
        if not paired:
            ch.notes.append("no matching baseline cell — compare against the chapter, not the hunk")
        elif ob and not nb_:
            ch.notes.append("output disappeared")
        elif not ob and nb_:
            ch.notes.append("output appeared")
        out.append(ch)
    return out


# ----------------------------------------------------------------------------- rendering

AUTO_WHY = {
    "whitespace": "Blank-line change only.",
    "metadata": "Notebook or cell metadata (jupytext header, tags). Not reader-visible.",
    "mechanical": "Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.",
}
PROSE_SLOT = "**Why:** _(to fill)_\n**Verdict:** _(necessary | optional | questionable)_"
CODE_SLOT = "**Why:** _(to fill)_\n**Output:** _(same | differs: how)_"
OUTPUT_SLOT = "**Why:** _(to fill)_\n**Reader sees:** _(equivalent | changed: what)_"


def diff_block(ch: Change, limit: int = 40) -> str:
    out = ["```diff"]
    for l in ch.old[:limit]:
        out.append("- " + l.rstrip())
    if len(ch.old) > limit:
        out.append(f"- … {len(ch.old) - limit} more lines")
    for l in ch.new[:limit]:
        out.append("+ " + l.rstrip())
    if len(ch.new) > limit:
        out.append(f"+ … {len(ch.new) - limit} more lines")
    out.append("```")
    return "\n".join(out)


def render(chapter: str, tier: str, src: str, dst: str, changes: list[Change],
           rewrite: bool = False) -> str:
    counts = collections.Counter(ch.category for ch in changes)
    order = ["output", "prose", "mixed", "dropdown", "tab-twins", "code",
             "mechanical", "metadata", "whitespace"]
    summary = " · ".join(f"{k} {counts[k]}" for k in order if counts[k])
    review = [ch for ch in changes if ch.category in REVIEW]
    outputs = [ch for ch in changes if ch.category == "output"]
    drops = [ch for ch in changes if ch.category == "dropdown"]

    L = [f"# {chapter} — change report", "",
         f"`{src}` → `{dst}`", "",
         f"**Tier {tier} · {len(changes)} changes:** {summary or 'none'}", ""]
    L.append("Categories: **output** = a committed cell output moved, which is what the reader sees. "
             "**prose** / **mixed** = wording re-authored beyond a library rename → review. "
             "**dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. "
             "**mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that "
             "cannot survive as-is), *optional* (style edit the conversion did not require; safe to "
             "revert), *questionable* (reviewer should decide).")
    L.append("")
    if rewrite:
        L.append("> **Authored rewrite.** This chapter was renamed and re-written rather than converted "
                 "cell by cell, so the diff below is not a cell-for-cell correspondence — whole "
                 "sections were dropped, merged from another chapter, or written fresh. Read it as an "
                 "inventory of what the reader gains and loses, not as a list of edits. "
                 "`conversion/chapter_map.yml` records the lineage.")
        L.append("")
    if changes and not all(ch.category in AUTO_WHY for ch in changes):
        L += ["## Summary", "", "_(to fill)_", ""]
    if not changes:
        L.append("_No differences._")
        return "\n".join(L) + "\n"
    if review:
        L += ["## Needs review", ""]
        L += [f"- [C{ch.idx}](#c{ch.idx}) · {ch.section}" for ch in review]
        L.append("")
    if outputs:
        L += ["## Outputs that changed", "",
              "What the reader sees. CI never executes, so these ship exactly as committed.", ""]
        for ch in outputs:
            flag = " · " + "; ".join(ch.notes) if ch.notes else ""
            L.append(f"- [C{ch.idx}](#c{ch.idx}) · {ch.section}{flag}")
        L.append("")
    if drops:
        L += ["## Dropdown mirrors", "",
              "Hard rule 3: each of these repeats a code cell verbatim and must move with it.", ""]
        L += [f"- [C{ch.idx}](#c{ch.idx}) · {ch.section}" for ch in drops]
        L.append("")

    L += ["## Changes", ""]
    for ch in changes:
        flag = " · **REVIEW**" if ch.category in REVIEW else ""
        L.append(f'<a id="c{ch.idx}"></a>')
        L.append(f"### C{ch.idx} · {ch.section} · {ch.category}{flag}")
        L.append("")
        where = ("committed output" if ch.category == "output"
                 else f"baseline L{ch.old_start} → branch L{ch.new_start}")
        L.append(where + (f" · {'; '.join(ch.notes)}" if ch.notes else ""))
        L.append("")
        L.append(diff_block(ch))
        L.append("")
        if ch.category in AUTO_WHY:
            L.append(f"**Why:** {AUTO_WHY[ch.category]}")
        elif ch.category == "output":
            L.append(OUTPUT_SLOT)
        elif ch.category in REVIEW:
            L.append(PROSE_SLOT)
        else:
            L.append(CODE_SLOT)
        L.append("")
    return "\n".join(L) + "\n"


# ----------------------------------------------------------------------------- drivers


def build(force: bool, only: str | None) -> list[tuple[str, str, Path, list[Change]]]:
    sha = baseline_sha()
    ren = renames()
    records = json.loads(STATE.read_text())
    results = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for rec in records:
            ch_name = rec["chapter"]
            if only and ch_name != only:
                continue
            cur_path = ROOT / rec["source"]
            rel = rec["source"]
            if not cur_path.exists():
                print(f"skip (missing): {rel}", file=sys.stderr)
                continue
            base_rel = baseline_path(rel, ren)
            raw = git_show(sha, base_rel)
            if raw is None and base_rel != rel:
                raw = git_show(sha, rel)
            if raw is None:
                print(f"skip (not in baseline {sha[:12]}): {rel}", file=sys.stderr)
                continue
            rewrite = base_rel != rel

            if rec["is_notebook"]:
                base_nb_path = tmp / f"{ch_name}-base.ipynb"
                base_nb_path.write_bytes(raw)
                old = to_py(base_nb_path, tmp / f"{ch_name}-base.py")
                new = to_py(cur_path, tmp / f"{ch_name}-cur.py")
                if old is None or new is None:
                    continue
                changes = source_changes(old, new)
                changes += output_changes(json.loads(raw), json.loads(cur_path.read_text()),
                                          len(changes) + 1)
            else:
                old = raw.decode().splitlines()
                new = cur_path.read_text().splitlines()
                changes = source_changes(old, new, kind="markdown")

            report = OUT / f"{ch_name}.md"
            text = render(ch_name, rec["tier"], f"{sha[:12]}:{base_rel}", rel, changes,
                          rewrite=rewrite)
            if force or not report.exists():
                report.parent.mkdir(parents=True, exist_ok=True)
                report.write_text(text)
            results.append((ch_name, rec["tier"], report, changes))

        # chapters that were dissolved rather than converted
        ren_inv = {v: k for k, v in ren.items()}
        for gone in absorbed():
            if only and gone != only:
                continue
            base_rel = f"content/{gone}/{gone}.ipynb"
            raw = git_show(sha, base_rel)
            if raw is None:
                print(f"skip (absorbed chapter not in baseline): {gone}", file=sys.stderr)
                continue
            host = None
            for cur_dir, base_dir in ren.items():
                if (ROOT / "content" / cur_dir).is_dir():
                    host = cur_dir
                    break
            host_rel = f"content/{host}/{host}.ipynb" if host else None
            if not host_rel or not (ROOT / host_rel).exists():
                print(f"skip (no host chapter for {gone})", file=sys.stderr)
                continue
            base_files = subprocess.run(
                ["git", "ls-tree", "-r", "--name-only", sha, f"content/{gone}/"],
                cwd=ROOT, capture_output=True, text=True).stdout.split()
            imgs = [Path(f).name for f in base_files if Path(f).suffix.lower()
                    in (".png", ".jpg", ".jpeg", ".svg")]
            data = [Path(f).name for f in base_files if "/data/" in f]
            assets = {}
            if imgs:
                assets["images"] = f"{len(imgs)} deleted with the chapter: " + ", ".join(sorted(imgs))
            if data:
                assets["data"] = ", ".join(sorted(data))
            report = OUT / f"{gone}.md"
            text = render_absorbed(gone, f"{sha[:12]}:{base_rel}", host_rel,
                                   json.loads(raw), json.loads((ROOT / host_rel).read_text()),
                                   assets)
            if force or not report.exists():
                report.parent.mkdir(parents=True, exist_ok=True)
                report.write_text(text)
            results.append((gone, f"removed:{host}", report, []))
    return results


UNFILLED = re.compile(r"_\(to fill\)_")
VERDICT = re.compile(r"\*\*Verdict:\*\*\s*`?(necessary|optional|questionable)")


def build_index(results) -> None:
    sha = baseline_sha()
    rows, tot = [], collections.Counter()
    for ch_name, tier, report, changes in results:
        body = report.read_text() if report.exists() else ""
        review = sum(c.category in REVIEW for c in changes)
        outs = sum(c.category == "output" for c in changes)
        code = sum(c.category in ("code", "dropdown", "tab-twins") for c in changes)
        v = collections.Counter(VERDICT.findall(body))
        unfilled = len(UNFILLED.findall(body))
        tot.update({"changes": len(changes), "review": review, "outputs": outs, "code": code,
                    "unfilled": unfilled, **{k: v[k] for k in v}})
        verdicts = (f"{v['necessary']} / {v['optional']} / {v['questionable']}") if review else ""
        link = f"[{ch_name}]({report.relative_to(ROOT)})"
        if tier.startswith("removed:"):
            # A dissolved chapter has no diff to count; counting it as 0 changes would file it
            # under "identical", which is the opposite of what happened to it.
            host = tier.split(":", 1)[1]
            rows.append((10 ** 6, 0, ch_name,
                         f"| {link} | — | — | — | — | — | | {unfilled} | "
                         f"**removed** — dissolved into `{host}` |"))
            continue
        note = "identical" if not changes else ""
        rows.append((review, outs, ch_name,
                     f"| {link} | {tier} | {len(changes)} | {outs} | {code} | {review} | "
                     f"{verdicts} | {unfilled} | {note} |"))
    rows.sort(key=lambda r: (-r[0], -r[1], r[2]))

    text = [
        "# Change report — pandas → Polars, course notes",
        "",
        f"One report per chapter under [`conversion/_diff/`](conversion/_diff/), generated by",
        "`conversion/diff_report.py` and annotated by hand. Every difference between the pinned",
        f"pre-conversion commit `{sha[:12]}` and this branch appears as a numbered change with a",
        "category, a **Why**, and a verdict.",
        "",
        "Two passes feed each report. The **source** pass diffs the notebook as percent-format text,",
        "the same view a writer agent edits, with cell ids ignored. The **outputs** pass diffs the",
        "committed outputs, because CI builds without executing (AGENTS.md hard rule 1) — so a cell",
        "whose output was never regenerated ships Polars code above a pandas table, and a source diff",
        "cannot see it. Markdown chapters have no notebook and are diffed directly.",
        "",
        "**How to review:** open a chapter and read *Outputs that changed* and *Needs review* first.",
        "Each prose change carries a verdict: *necessary* (pandas-specific content that could not",
        "survive), *optional* (a style edit the conversion did not require; revert if you prefer the",
        "original wording), or *questionable* (a judgment call for course staff).",
        "",
        "Related: [`CONVERSIONS.md`](CONVERSIONS.md) is the per-chapter record,",
        "[`CONTRADICTIONS.md`](CONTRADICTIONS.md) lists claims that turned out to be false.",
        "Cross-chapter items worth a decision are in",
        "[`conversion/_diff/HIGHLIGHTS.md`](conversion/_diff/HIGHLIGHTS.md).",
        "",
        f"**Totals:** {tot['changes']} changes · {tot['outputs']} output changes · {tot['code']} code "
        f"· {tot['review']} prose rewrites to review (verdicts: {tot['necessary']} necessary / "
        f"{tot['optional']} optional / {tot['questionable']} questionable)"
        + (f" · {tot['unfilled']} reasons still unfilled" if tot["unfilled"] else ""),
        "",
        "| chapter | tier | changes | outputs | code | prose review | necessary / optional / questionable | unfilled | note |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    text += [r[3] for r in rows]
    text += ["",
             "Regenerate skeletons with `python conversion/diff_report.py` (existing reports are kept;",
             "`--force` overwrites them, `--index` rebuilds only this table)."]
    INDEX.write_text("\n".join(text) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--index", action="store_true")
    ap.add_argument("--chapter")
    args = ap.parse_args()
    results = build(force=args.force and not args.index, only=args.chapter)
    if args.chapter:
        # keep the index whole: re-read every chapter's existing report for the table
        results = build(force=False, only=None)
    build_index(results)
    n_rev = sum(sum(c.category in REVIEW for c in ch) for _, _, _, ch in results)
    n_out = sum(sum(c.category == "output" for c in ch) for _, _, _, ch in results)
    print(f"{len(results)} reports, {sum(len(c) for _, _, _, c in results)} changes, "
          f"{n_out} output changes, {n_rev} to review → {INDEX}")


if __name__ == "__main__":
    main()
