#!/usr/bin/env python3
"""
Gate battery for newly authored chapters -- the ones with no pandas baseline.

`nb_validate.py` diffs every chapter against the pinned pre-conversion commit, so a chapter
that did not exist at that commit comes back INCONCLUSIVE and can never go green. That is the
right answer for the conversion battery and useless for authoring `new_eda_1` ... `new_eda_5`.
This battery checks absolute properties of the artifact instead, so it needs no baseline:

    A1  frontmatter        cell 0 opens with the title block, then a Learning Outcomes note of `*` bullets
    A2  executed           every code cell ran in one clean pass under the pinned polars, witness present
    A3  no-pandas-code     no pandas in code cells; `.to_pandas()` only where allowlisted
    A4  fences             every markdown cell's fences and ::: directives close
    A5  alt-text           figure outputs carry a non-empty `#| fig-alt`; every `#|` block parses as
                           YAML the way MyST parses it; images have alt and exist
    A6  tags               only remove-input / remove-output / remove-cell
    A7  dropdown-mirror    a `Click to see the code` dropdown matches the next cell, which hides its input
    A8  repr-leak          no `<Axes: ...>` / `<seaborn...>` text rendered as a cell result
    A9  conventions        fa26-course-conventions.md lint, plus nulls surfacing after a sort
    A10 sql                every ```sql block parses in DuckDB
    A11 residue            transcript residue, doubled words, first-person singular, known typos

The collector is `nb_validate.Result`, so the anti-vacuous-pass contract carries over: a gate
that expected items and examined none is INCONCLUSIVE, never PASS.

`--self-test` is the negative control. It runs the battery on `main`'s unrevised `new_eda_1`
draft, which is known to carry an unclosed fence, a `hide-input` tag, no fig-alt, leaked Axes
reprs, `ORDER BY ... DSC`, transcript residue and no witness, and asserts that each of those
gates FAILS. It then runs the structural gates on `polars_2`, an authored chapter already
signed off, and asserts they stay quiet. A battery that passes the draft is broken.

    python conversion/authored_validate.py --self-test
    python conversion/authored_validate.py --chapter new_eda_1 [--chapter new_eda_2 ...] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List

import nbformat

sys.path.insert(0, str(Path(__file__).resolve().parent))

import chapters as ch  # noqa: E402
from nb_validate import (  # noqa: E402
    FAIL,
    FIG_ALT_RE,
    PASS,
    Result,
    alt_is_empty,
    allow,
    code_cells,
    md_cells,
    mirror_normalize,
    strip_pandas_tabs,
)

PINNED_POLARS = "1.43.1"
ALLOWED_TAGS = {"remove-input", "remove-output", "remove-cell"}
DROPDOWN_TITLE = "Click to see the code"

PANDAS_CODE_RE = re.compile(r"^\s*(import pandas|from pandas)|\bpd\.", re.M)
TO_PANDAS_RE = re.compile(r"\.to_pandas\(")
LEAK_RE = re.compile(r"^(<(Axes|Figure|seaborn\.|matplotlib\.)|\[<matplotlib|Text\()")
IMAGE_BLOCK_RE = re.compile(r"^(`{3,}|:{3,})\s*\{image\}\s*(\S+)\s*\n(.*?)^\1\s*$", re.M | re.S)
MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)")
ALT_RE = re.compile(r"^:alt:(.*)$", re.M)
SQL_BLOCK_RE = re.compile(r"^(`{3,})sql\s*\n(.*?)^\1\s*$", re.M | re.S)

# Convention lint -- each pattern is a spelling fa26-course-conventions.md says not to write.
CONVENTION_LINT = [
    (re.compile(r"\bpl\.count\(\)"), "pl.count() -- the course writes pl.len()"),
    (re.compile(r"\blen\(\s*\w+\.group_by\("), "len(df.group_by(...)) -- use .n_unique() for distinct values"),
    (re.compile(r"maintain_order\s*=\s*True"), "maintain_order=True -- follow group_by with an explicit .sort()"),
    (re.compile(r"\bpolars_random\b|\bimport\s+polars_random"), "polars_random is not in requirements.txt -- use a seeded numpy rng"),
    (re.compile(r"\bpd\.read_csv\b"), "pd.read_csv in a Polars chapter (L02 S31's slide bug)"),
    (re.compile(r"\.sum,"), "`.sum,` without parentheses (L04 S37's slide bug)"),
]

RESIDUE_RE = [
    (re.compile(r"\b(uh|um|uhm)\b", re.I), "transcript filler"),
    (re.compile(r"\b(\w{2,})\s+\1\b", re.I), "doubled word"),
    (re.compile(r"(?<!EDA )(?<!Part )(?<!Lecture )(?<!Polars )(?<!Pandas )(?<![A-Za-z`'\"])I(?= [a-z])"), "first-person singular"),
    (re.compile(r"\bmy\b(?! own)"), "first-person singular"),
]
# Typos found in the draft of new_eda_1 and the Fa26 decks. Kept literal on purpose: a spelling
# model would flag every column name in the book.
KNOWN_TYPOS = [
    "featue", "freshmmen", "ethncity", "Latana", "usign", "Provenence", "providence", "nubmer",
    "resepctively", "donwloadable", "columnn", "additonal", "Acess", "mmin", "polar code",
    "who who", "The the",
]


def strip_code(md: str) -> str:
    """Markdown with fenced blocks and inline code removed -- prose only."""
    md = re.sub(r"^(`{3,}).*?^\1\s*$", "", md, flags=re.M | re.S)
    return re.sub(r"`[^`\n]*`", "", md)


def text_outputs(cell, kinds=("execute_result",)) -> List[str]:
    out = []
    for o in cell.get("outputs", []):
        if o.get("output_type") in kinds:
            out.append("".join(o.get("data", {}).get("text/plain", "")))
        elif o.get("output_type") == "stream" and "stream" in kinds:
            out.append("".join(o.get("text", "")))
    return out


def has_figure(cell) -> bool:
    return any("image/png" in o.get("data", {}) or "image/svg+xml" in o.get("data", {})
               for o in cell.get("outputs", []))


CELL_OPTION_PREFIX = re.compile(r"^#\s?\| ")
IPYTHON_MAGIC = re.compile(r"^%%")


def cell_options_error(src: str):
    """Parse a code cell's leading `#| ` lines the way MyST does, or say why it can't.

    Mirrors myst-cli's `metadataFromCode`: an optional `%%` magic first, then `#| ` lines up to the
    first non-blank line of code, loaded as one YAML document. When that YAML fails to load, MyST
    logs "Invalid code cell metadata" and *drops every option on the cell*, so a `fig-alt` that
    contains an unquoted `: ` silently vanishes from the page while the source still shows it.
    `FIG_ALT_RE` alone cannot see this: it matches the line, not what MyST makes of it.
    """
    import yaml

    meta, expect_magic = [], True
    for line in src.split("\n"):
        if expect_magic and IPYTHON_MAGIC.match(line):
            expect_magic = False
        elif CELL_OPTION_PREFIX.match(line):
            meta.append(CELL_OPTION_PREFIX.sub("", line))
        elif line.strip():
            break
    if not meta:
        return None
    try:
        yaml.safe_load("\n".join(meta))
    except yaml.YAMLError as e:
        return str(e).splitlines()[0]
    return None


# ------------------------------------------------------------------ gates


def gate_frontmatter(nb, res: Result) -> None:
    src = nb.cells[0].get("source", "") if nb.cells else ""
    problems = []
    m = re.match(r"\A---\n(.*?)\n---\n", src, re.S)
    if not m or not re.search(r"^title:\s*\S", m.group(1), re.M):
        problems.append("cell 0 does not open with a --- title: --- block")
    lo = re.search(r"^:::\s*\{note\}\s*Learning Outcomes\s*\n(.*?)^:::", src, re.M | re.S)
    if not lo:
        problems.append("no `::: {note} Learning Outcomes` block in cell 0")
    else:
        body = [l for l in lo.group(1).splitlines() if l.strip() and not l.startswith(":")]
        bad = [l for l in body if not l.startswith("* ")]
        if not body:
            problems.append("Learning Outcomes block is empty")
        if bad:
            problems.append(f"{len(bad)} Learning Outcomes line(s) are not `* ` bullets, e.g. {bad[0][:50]!r}")
    res.add("frontmatter", not problems, 1, 1, problems or ["title block and Learning Outcomes intact"])


def gate_executed(nb, res: Result) -> None:
    cells = [c for c in code_cells(nb) if c.get("source", "").strip()]
    w = nb.metadata.get("polars_conversion") or {}
    problems = []
    if not w:
        problems.append("no execution witness: run nb_execute.py --chapter <ch> first")
    else:
        if w.get("polars") != PINNED_POLARS:
            problems.append(f"witness says polars {w.get('polars')}, pinned {PINNED_POLARS} -- wrong env")
        if w.get("n_executed") != w.get("n_code_cells"):
            problems.append(f"witness: only {w.get('n_executed')}/{w.get('n_code_cells')} cells executed")
    counts = [c.get("execution_count") for c in cells]
    missing = [c.get("id") for c in cells if c.get("execution_count") is None]
    present = [x for x in counts if x is not None]
    if missing:
        problems.append(f"{len(missing)} code cell(s) never executed, e.g. {missing[0]}")
    elif present != list(range(1, len(present) + 1)):
        problems.append("execution_counts are not 1..n -- not one clean top-to-bottom run")
    errs = [c.get("id") for c in cells for o in c.get("outputs", []) if o.get("output_type") == "error"]
    allowed = allow(res.chapter, "expected_errors")
    errs = [e for e in errs if e not in allowed]
    if errs:
        problems.append(f"{len(errs)} cell(s) raised without an expected_errors entry, e.g. {errs[0]}")
    res.add("executed", not problems, len(cells) if present else 0, len(cells),
            problems or [f"{len(cells)} code cells, one clean run, polars {w.get('polars')}"])


def gate_no_pandas(nb, res: Result) -> None:
    allowed = allow(res.chapter, "interop")
    problems = []
    for c in code_cells(nb):
        s = c.get("source", "")
        if PANDAS_CODE_RE.search(s):
            problems.append(f"{c.get('id')}: pandas in a code cell")
        if TO_PANDAS_RE.search(s) and c.get("id") not in allowed:
            problems.append(f"{c.get('id')}: .to_pandas() with no interop allowlist entry")
    for c in md_cells(nb):
        # A comparison tab's pandas pane is pandas on purpose; the Polars pane is still scanned.
        md, _ = strip_pandas_tabs(c.get("source", ""))
        for body in ch.markdown_code_blocks(md):
            if PANDAS_CODE_RE.search(body):
                problems.append(f"{c.get('id')}: pandas inside a markdown code block")
    n = len(code_cells(nb))
    res.add("no-pandas-code", not problems, n, n, problems or [f"{n} code cells, no pandas"])


def fence_problems(text: str) -> List[str]:
    """Stack-walk backtick fences and ::: directives, CommonMark closing rules."""
    stack: List[tuple] = []
    for line in text.splitlines():
        m = ch.MD_FENCE_LINE.match(line)
        if m:
            ticks, info = len(m.group(1)), m.group(2)
            if stack and stack[-1][0] == "`" and info == "" and ticks >= stack[-1][1]:
                stack.pop()
            elif not stack or stack[-1][0] != "`" or info.startswith("{"):
                stack.append(("`", ticks, line.strip()))
            continue
        if stack and stack[-1][0] == "`" and not stack[-1][2].lstrip("`").startswith("{"):
            continue  # inside a literal code block, colons are content
        d = re.match(r"^(:{3,})\s*(\S*)", line)
        if d:
            colons, info = len(d.group(1)), d.group(2)
            if stack and stack[-1][0] == ":" and info == "" and colons >= stack[-1][1]:
                stack.pop()
            elif info:
                stack.append((":", colons, line.strip()))
    return [f"unclosed {kind * n} opened by {opener[:40]!r}" for kind, n, opener in stack]


def gate_fences(nb, res: Result) -> None:
    problems = []
    cells = md_cells(nb)
    for c in cells:
        problems += [f"{c.get('id')}: {p}" for p in fence_problems(c.get("source", ""))]
    res.add("fences", not problems, len(cells), len(cells), problems or [f"{len(cells)} markdown cells balanced"])


def gate_alt_text(nb, chapter_dir: Path, res: Result) -> None:
    problems, checked, expected = [], 0, 0
    for c in code_cells(nb):
        bad_yaml = cell_options_error(c.get("source", ""))
        if bad_yaml:
            problems.append(f"{c.get('id')}: `#|` options are not valid YAML ({bad_yaml}) -- MyST drops "
                            "them all, fig-alt included; quote the value or remove the stray ': '")
        if not has_figure(c):
            continue
        expected += 1
        m = FIG_ALT_RE.search(c.get("source", ""))
        if not m or alt_is_empty(m.group(1)):
            problems.append(f"{c.get('id')}: figure output with no non-empty #| fig-alt")
        else:
            checked += 1
    for c in md_cells(nb):
        src = c.get("source", "")
        for m in IMAGE_BLOCK_RE.finditer(src):
            expected += 1
            path, opts = m.group(2), m.group(3)
            alt = ALT_RE.search(opts)
            if not alt or alt_is_empty(alt.group(1)):
                problems.append(f"{c.get('id')}: {{image}} {path} has no :alt:")
            elif not (chapter_dir / path).exists():
                problems.append(f"{c.get('id')}: {{image}} {path} does not exist")
            else:
                checked += 1
        for m in MD_IMAGE_RE.finditer(src):
            expected += 1
            if alt_is_empty(m.group(1)):
                problems.append(f"{c.get('id')}: ![]({m.group(2)}) has empty alt")
            elif not m.group(2).startswith("http") and not (chapter_dir / m.group(2)).exists():
                problems.append(f"{c.get('id')}: {m.group(2)} does not exist")
            else:
                checked += 1
    res.add("alt-text", not problems, checked, expected,
            problems or [f"{checked} figure(s)/image(s), all with alt text"])


def gate_tags(nb, res: Result) -> None:
    problems = []
    for c in nb.cells:
        bad = set(c.get("metadata", {}).get("tags", []) or []) - ALLOWED_TAGS
        if bad:
            problems.append(f"{c.get('id')}: tag(s) {sorted(bad)} -- the book uses only {sorted(ALLOWED_TAGS)}")
    res.add("tags", not problems, len(nb.cells), len(nb.cells), problems or ["only sanctioned tags"])


def gate_dropdown_mirror(nb, res: Result) -> None:
    cells, problems, expected, checked = nb.cells, [], 0, 0
    for i, c in enumerate(cells):
        if c.cell_type != "markdown" or DROPDOWN_TITLE not in c.get("source", ""):
            continue
        blocks = [mirror_normalize(b) for b in ch.markdown_code_blocks(c.get("source", ""))]
        blocks = [b for b in blocks if b]
        if not blocks:
            continue
        expected += 1
        nxt = next((cells[j] for j in range(i + 1, min(i + 3, len(cells))) if cells[j].cell_type == "code"), None)
        if nxt is None:
            problems.append(f"{c.get('id')}: dropdown with no code cell after it")
            continue
        if blocks[-1] != mirror_normalize(nxt.get("source", "")):
            problems.append(f"{c.get('id')} -> {nxt.get('id')}: dropdown code differs from the cell it mirrors")
        elif "remove-input" not in (nxt.get("metadata", {}).get("tags", []) or []):
            problems.append(f"{nxt.get('id')}: mirrored cell lacks remove-input -- its code prints twice")
        else:
            checked += 1
    res.add("dropdown-mirror", not problems, checked, expected,
            problems or [f"{checked} dropdown/cell pair(s) identical" if expected else "no dropdowns"])


def gate_repr_leak(nb, res: Result) -> None:
    problems = []
    for c in code_cells(nb):
        for t in text_outputs(c):
            if LEAK_RE.match(t.strip()):
                problems.append(f"{c.get('id')}: renders {t.strip()[:40]!r} -- end the cell with `;`")
    n = len(code_cells(nb))
    res.add("repr-leak", not problems, n, n, problems or ["no plot object reprs leak"])


def gate_conventions(nb, res: Result) -> None:
    problems = []
    for c in code_cells(nb):
        s = c.get("source", "")
        for rx, why in CONVENTION_LINT:
            if rx.search(s):
                problems.append(f"{c.get('id')}: {why}")
        # Nulls sort first in Polars. A sort whose rendered head/tail shows null is exactly the
        # silent-null-row defect AGENTS rule 8 names; checking the output beats guessing nullability.
        if re.search(r"\.sort\(", s) and "nulls_last" not in s and re.search(r"\.(head|tail)\(", s):
            if any(re.search(r"(┆|│)\s*null\s*(┆|│)", t) for t in text_outputs(c)):
                problems.append(f"{c.get('id')}: sort then head/tail renders null rows -- pass nulls_last=True")
    for c in md_cells(nb):
        for body in ch.markdown_code_blocks(c.get("source", "")):
            for rx, why in CONVENTION_LINT:
                if rx.search(body):
                    problems.append(f"{c.get('id')} (markdown code): {why}")
    n = len(nb.cells)
    res.add("conventions", not problems, n, n, problems or ["conventions lint clean"])


def gate_sql(nb, res: Result) -> None:
    import duckdb

    problems, blocks = [], []
    for c in md_cells(nb):
        blocks += [(c.get("id"), m.group(2)) for m in SQL_BLOCK_RE.finditer(c.get("source", ""))]
    for cid, body in blocks:
        try:
            duckdb.extract_statements(body)
        except Exception as e:  # duckdb.ParserException, but keep the gate honest on anything
            problems.append(f"{cid}: {str(e).splitlines()[0][:90]}")
            continue
        # DuckDB accepts a SELECT alias inside WHERE; standard SQL (and the SQL chapters) do not.
        aliases = re.findall(r"\bAS\s+(\w+)", body, re.I)
        where = re.search(r"\bWHERE\b(.*?)(\bGROUP\b|\bORDER\b|\bLIMIT\b|$)", body, re.I | re.S)
        if where and any(re.search(rf"\b{a}\b", where.group(1)) for a in aliases):
            problems.append(f"{cid}: SELECT alias used in WHERE -- not portable SQL")
    res.add("sql", not problems, len(blocks), len(blocks),
            problems or [f"{len(blocks)} SQL block(s) parse" if blocks else "no SQL blocks"])


def gate_residue(nb, res: Result) -> None:
    problems = []
    cells = md_cells(nb)
    for c in cells:
        prose = strip_code(c.get("source", ""))
        prose = re.sub(r"\A---\n.*?\n---\n", "", prose, flags=re.S)
        # A quoted or rhetorical question in the reader's voice ("What do I do when I get a
        # dataset?") is house style, not the author slipping into first person.
        voiced = re.sub(r'"[^"\n]*"|“[^”\n]*”', "", prose)
        voiced = "\n".join(l for l in voiced.splitlines() if not l.rstrip().endswith("?"))
        for rx, why in RESIDUE_RE:
            target = voiced if why == "first-person singular" else prose
            for m in rx.finditer(target):
                problems.append(f"{c.get('id')}: {why}: {target[max(0, m.start() - 20):m.end() + 20]!r}")
        for t in KNOWN_TYPOS:
            # Whole-word match: a bare substring test flagged "mmin" inside "programming" and
            # "a a " inside "data are". Multi-word entries are matched the same way at both ends.
            if re.search(rf"(?<![A-Za-z]){re.escape(t.strip())}(?![A-Za-z])", prose):
                problems.append(f"{c.get('id')}: known typo {t.strip()!r}")
    res.add("residue", not problems, len(cells), len(cells), problems or ["no residue or known typos"])


# ------------------------------------------------------------------ driver


def validate_path(name: str, nb_path: Path, chapter_dir: Path) -> Result:
    nb = nbformat.read(str(nb_path), as_version=4)
    res = Result(name)
    gate_frontmatter(nb, res)
    gate_executed(nb, res)
    gate_no_pandas(nb, res)
    gate_fences(nb, res)
    gate_alt_text(nb, chapter_dir, res)
    gate_tags(nb, res)
    gate_dropdown_mirror(nb, res)
    gate_repr_leak(nb, res)
    gate_conventions(nb, res)
    gate_sql(nb, res)
    gate_residue(nb, res)
    return res


def validate(chapter: ch.Chapter) -> Result:
    return validate_path(chapter.name, chapter.source, chapter.dir)


def self_test() -> bool:
    ok = True
    raw = subprocess.run(["git", "show", "main:content/new_eda_1/new_eda_1.ipynb"],
                         capture_output=True, text=True, check=True).stdout
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "new_eda_1.ipynb"
        p.write_text(raw)
        res = validate_path("new_eda_1@main", p, Path("content/new_eda_1"))
    res.report()
    must_fail = ["frontmatter", "executed", "fences", "alt-text", "tags", "repr-leak", "sql", "residue"]
    must_pass = ["no-pandas-code"]
    for g in must_fail:
        v = res.get(g).verdict
        if v != FAIL:
            ok = False
            print(f"  SELF-TEST BROKEN: {g} is {v} on the unrevised draft; it must FAIL")
    for g in must_pass:
        v = res.get(g).verdict
        if v != PASS:
            ok = False
            print(f"  SELF-TEST BROKEN: {g} is {v} on the unrevised draft; it must PASS")

    # Planted defect: EDA II shipped a fig-alt with an unquoted ": ", which MyST rejected while every
    # gate stayed green. A one-cell notebook carrying exactly that must fail A5.
    planted = nbformat.v4.new_notebook()
    planted.cells = [nbformat.v4.new_code_cell(
        "#| fig-alt: B and C look nearly identical: large points\nplt.plot([1, 2]);",
        outputs=[nbformat.v4.new_output("display_data", data={"image/png": "iVBORw0KGgo="})])]
    res_p = Result("planted-fig-alt")
    gate_alt_text(planted, Path("."), res_p)
    if res_p.get("alt-text").verdict != FAIL:
        ok = False
        print("  SELF-TEST BROKEN: a fig-alt that MyST cannot parse passed alt-text")

    # False-alarm control: an authored, signed-off chapter must not trip the structural gates.
    ctl = ch.resolve(["polars_2"])[0]
    res2 = validate(ctl)
    for g in ["no-pandas-code", "fences", "tags", "dropdown-mirror", "repr-leak", "sql"]:
        v = res2.get(g).verdict
        if v != PASS:
            ok = False
            print(f"  SELF-TEST BROKEN: {g} is {v} on polars_2; details: {res2.get(g).details[:3]}")
    print(f"\n  self-test {'PASSED' if ok else 'FAILED'}: negative control on main's draft, "
          "false-alarm control on polars_2\n")
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[1])
    ap.add_argument("--chapter", action="append", default=[])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--json", action="store_true", help="print machine-readable results")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(0 if self_test() else 1)
    if not args.chapter:
        ap.error("--chapter or --self-test required")
    results = [validate(c) for c in ch.resolve(args.chapter)]
    if args.json:
        print(json.dumps([r.to_dict() for r in results], indent=2))
    else:
        for r in results:
            r.report()
    sys.exit(0 if all(r.ok for r in results) else 1)


if __name__ == "__main__":
    main()
