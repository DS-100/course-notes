#!/usr/bin/env python3
"""Pandas/Polars comparison tabs, and the check that keeps them honest.

Course staff chose frozen output for the pandas side: the tab shows code plus its result as
static text, because live tab execution would require the deploy build to run `--execute`, which
this repo deliberately does not do (`deploy.yml` is node-only; outputs are committed instead).

Frozen output is exactly the defect class this conversion existed to remove -- a result that no
longer has to come from the code above it. So nothing here is written by hand:

  --emit    executes every pandas snippet in the pinned env and writes the tab markdown,
            taking the Polars half verbatim from the live notebook cell and its committed output.
  --verify  re-executes every pandas snippet and re-reads every live Polars cell, then diffs
            all three against what is on the page.

`--verify` is what makes the frozen copies checkable rather than merely plausible. Run it after
any edit to a tabbed chapter, and after any change to the pinned polars/pandas versions.
"""
from __future__ import annotations
import argparse, ast, io, json, os, re, sys, contextlib
from pathlib import Path
import nbformat

MARK_BEGIN = "<!-- tab-twins:begin {cell} -->"
MARK_END = "<!-- tab-twins:end -->"

from tab_twins_data import TWINS, OUTPUT_CHURNS


def repr_of(code: str, env: dict) -> str:
    """The text a notebook would display for this snippet's final expression.

    Parsed with `ast` rather than split on newlines, so a final expression may span several
    lines -- which the more readable pandas snippets generally do.
    """
    tree = ast.parse(code.strip())
    if not tree.body:
        return ""
    *head, last = tree.body
    if head:
        exec(compile(ast.Module(body=head, type_ignores=[]), "<twin>", "exec"), env)
    if not isinstance(last, ast.Expr):
        exec(compile(ast.Module(body=[last], type_ignores=[]), "<twin>", "exec"), env)
        return ""
    val = eval(compile(ast.Expression(body=last.value), "<twin>", "eval"), env)
    if val is None:
        return ""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        print(val if hasattr(val, "to_string") else repr(val))
    return buf.getvalue().rstrip("\n")


def committed_output(cell) -> str:
    """The text a live notebook cell already carries, as committed.

    Errors count. A cell that raises on purpose is still showing the reader something, and for the
    `and`-instead-of-`&` demo the two libraries reject the same mistake in different words -- which
    is the most useful pair on the page. Rendering only `ename: evalue` keeps the traceback's file
    paths and line numbers, which move on every run, out of a frozen block.
    """
    for o in cell.get("outputs", []):
        if o.get("output_type") == "error":
            return f"{o.get('ename', '?')}: {o.get('evalue', '')}".rstrip()
        d = o.get("data", {})
        if "text/plain" in d:
            t = d["text/plain"]
            return ("".join(t) if isinstance(t, list) else t).rstrip("\n")
        if o.get("output_type") == "stream":
            t = o.get("text", "")
            return ("".join(t) if isinstance(t, list) else t).rstrip("\n")
    return ""


def raises(cell) -> bool:
    """Does the live Polars cell raise? Then its pandas twin is expected to raise too."""
    return any(o.get("output_type") == "error" for o in cell.get("outputs", []))


def polars_source(cell) -> str:
    """The live cell's source, minus MyST/quarto directive lines."""
    return "\n".join(
        l for l in (cell.source or "").splitlines() if not l.strip().startswith("#|")
    ).strip()


def build_block(cell_id: str, pl_code: str, pl_out: str, pd_code: str, pd_out: str) -> str:
    def pane(code, out):
        # Trailing whitespace is stripped on the way into the jupytext `.py` (every line is
        # written as `("# " + line).rstrip()`), so a block generated with it can never equal the
        # block that comes back off the page -- `--verify` would report STALE forever on any
        # pandas output with padded columns, which is most of them. Normalize here, at the one
        # place both paths share.
        def clean(s):
            return "\n".join(l.rstrip() for l in s.splitlines())
        s = f"```python\n{clean(code)}\n```"
        if out:
            s += f"\n\n```text\n{clean(out)}\n```"
        return s
    # The marker is an HTML comment and must stay on one line: `apply_to_pytext` recovers it with
    # `block.splitlines()[0]`, so a cell id containing a newline -- which a locator taken from a
    # multi-line cell does -- would be silently truncated, and two twins whose first lines match
    # would then share a marker and overwrite each other.
    cell_id = " ".join(str(cell_id).split())
    return (
        f"{MARK_BEGIN.format(cell=cell_id)}\n"
        ":::::{tab-set}\n"
        ":::: {tab-item} Polars\n"
        ":sync: pl\n"
        f"{pane(pl_code, pl_out)}\n"
        "::::\n\n"
        ":::: {tab-item} pandas\n"
        ":sync: pd\n"
        f"{pane(pd_code, pd_out)}\n"
        "::::\n"
        ":::::\n"
        f"{MARK_END}"
    )


# Polars guarantees no row order for these unless the cell asks for one. A frozen tab cannot
# mirror a cell whose output legitimately changes on every execution, so twinning one produces a
# block that reports STALE at random -- which trains people to ignore `--verify`, the one check
# that makes the frozen copies trustworthy. Measured on the babynames data: `value_counts` gave 2
# distinct row orders in 6 runs, and `unique()` gave 6 distinct results in 6.
ORDER_UNSTABLE = re.compile(r"\.(value_counts|unique|group_by|sample)\(")
# `sort=True` counts: verified stable over 8 runs on both the babynames column and a tied
# three-value column, so it fixes the order as surely as a following `.sort()`.
ORDER_FIXED = re.compile(r"\.sort\(|maintain_order|sort\s*=\s*True|\bseed\b")


def order_unstable(pl_code: str) -> bool:
    """Does this cell's output have an order Polars does not promise to reproduce?

    Judged on what the cell *displays*, not on what it mentions. A cell may build a GroupBy and
    then print only its type -- the class name is fixed no matter how the groups came out -- so
    the last expression decides.
    """
    lines = [l for l in pl_code.splitlines() if l.strip() and not l.strip().startswith("#")]
    if lines and lines[-1].strip().startswith("type("):
        return False
    return bool(ORDER_UNSTABLE.search(pl_code)) and not ORDER_FIXED.search(pl_code)


def baseline_code_cells(chapter: str) -> dict:
    """The pinned pre-conversion notebook's code cells, keyed by cell id.

    Resolved through `chapter_map.yml`, so a renamed chapter (`polars_2` -> `pandas_3`) still
    finds its baseline.
    """
    import nb_baseline, chapters as ch_mod
    lock = nb_baseline.read_lock()
    root = (Path("conversion/.baseline")
            / f"{lock['main_sha'][:12]}-{lock['converter_sha']}"
            / "content" / ch_mod.baseline_name(chapter))
    nbs = sorted(root.glob("*.ipynb"))
    if not nbs:
        return {}
    nb = nbformat.read(str(nbs[0]), as_version=4)
    return {c.get("id"): c for c in nb.cells if c.cell_type == "code"}


def locator_for(pl_code: str) -> str:
    """A line of the Polars source distinctive enough to find the cell in the jupytext `.py`.

    The `.py` carries no cell ids -- jupytext mints fresh ones on every build -- so a block has
    to be placed by matching code. The longest line is the most likely to be unique; `apply`
    reports it if it is not found.
    """
    lines = [l.strip() for l in pl_code.splitlines() if l.strip() and not l.strip().startswith("#")]
    return max(lines, key=len) if lines else pl_code.strip()


def _same_operation(pd_code: str, pl_code: str) -> bool:
    """Do these two panes say the same thing, ignoring the frame's name?

    The pandas twins name their frames `elections_pd`, `babynames_pd` and so on, so a pair like
    `elections.shape` / `elections_pd.shape` is never byte-identical even though a reader learns
    nothing from seeing both. Compare with the suffix removed, and with comments dropped, so the
    check measures the operation rather than the bookkeeping.
    """
    def norm(s: str) -> str:
        body = "\n".join(l for l in s.splitlines() if not l.strip().startswith("#"))
        return body.replace("_pd", "").strip()
    return norm(pd_code) == norm(pl_code)


def collect_handwritten(chapter: str, code_cells: list):
    """Declared twins as (page_index, cell, locator, pandas_code), **in page order**.

    The sort is load-bearing, not tidiness. The pandas snippets share one namespace so the
    pandas column reads as a continuous session, which means a twin that uses a frame an earlier
    twin built must run after it. Declaration order in `tab_twins_data.py` is not page order --
    measured, and wrong in both chapters -- so iterating the dict directly would run a
    later-page twin first and either raise `NameError` or, worse, silently read a stale frame
    left behind by an earlier cell and produce plausible wrong output.
    """
    items, problems = [], []
    for key, pd_code in TWINS[chapter]["cells"].items():
        hits = [(i, c) for i, c in enumerate(code_cells) if key in (c.source or "")]
        if len(hits) != 1:
            problems.append(f"{key[:40]!r}: matched {len(hits)} cells, expected exactly 1")
            continue
        i, cell = hits[0]
        if order_unstable(polars_source(cell)) and key not in OUTPUT_CHURNS.get(chapter, set()):
            problems.append(
                f"{key[:40]!r}: the Polars cell's row order is not guaranteed, so a frozen tab "
                "would go STALE at random -- sort the cell or drop the twin"
            )
            continue
        items.append((i, cell, key, pd_code))
    items.sort(key=lambda t: t[0])
    return items, problems


def collect_from_baseline(chapter: str, code_cells: list):
    """Twins paired by cell id against the pinned baseline -- no authoring, no execution.

    A *translated* chapter keeps its cell ids: G1 fails the whole battery otherwise. So the
    pandas half of every comparison is already on disk in `conversion/.baseline/`, together with
    the pandas output it produced when the book still ran on pandas. Pairing on id therefore
    yields a twin for free, and yields the *published* pandas output rather than a re-execution
    of pandas in today's environment -- which is both more honest for a tab captioned "pandas"
    and deterministic, which `--verify` needs.

    A pair is only worth showing where the conversion actually changed the code and both sides
    carry committed output. This does not work for `polars_1`/`polars_2`: those were rewritten,
    so no cell id survives and there is nothing to pair against.
    """
    bmap = baseline_code_cells(chapter)
    if not bmap:
        return [], [f"{chapter}: no baseline notebook to pair against"]
    items = []
    for i, cell in enumerate(code_cells):
        b = bmap.get(cell.get("id"))
        if b is None:
            continue
        pd_code, pl_code = polars_source(b), polars_source(cell)
        if pd_code == pl_code:
            continue                      # the conversion left this cell alone
        pd_out, pl_out = committed_output(b), committed_output(cell)
        if not pd_out or not pl_out:
            continue                      # nothing to compare on one side
        items.append((i, cell, locator_for(pl_code), pd_code, pd_out))
    return items, []


def run(chapter: str, verify: bool, from_baseline: bool = False) -> int:
    nbp = Path(f"content/{chapter}/{chapter}.ipynb")
    if not nbp.exists():
        print(f"  {chapter}: no built notebook")
        return 0, {}
    nb = nbformat.read(str(nbp), as_version=4)
    code_cells = [c for c in nb.cells if c.cell_type == "code"]
    blocks: dict[str, str] = {}
    identical = 0

    if from_baseline:
        items, problems = collect_from_baseline(chapter, code_cells)
        for _, cell, locator, pd_code, pd_out in items:
            blocks[locator] = build_block(
                cell.get("id"), polars_source(cell), committed_output(cell), pd_code, pd_out
            )
    else:
        spec = TWINS.get(chapter)
        if not spec or not spec["cells"]:
            print(f"  {chapter}: no twins declared yet")
            return 0, {}
        items, problems = collect_handwritten(chapter, code_cells)
        env: dict = {}
        cwd = os.getcwd()
        os.chdir(nbp.parent)          # snippets read the chapter's own data
        try:
            exec(spec["prelude"], env)
            for _, cell, locator, pd_code in items:
                pl_code, pl_out = polars_source(cell), committed_output(cell)
                # An empty output is fine and sometimes the point -- the import tab is one line of
                # code per library and nothing else. Only a *data* cell with no output is odd, and
                # that shows up as an empty pandas pane a reviewer will notice.
                want_raise = raises(cell)
                try:
                    pd_out = repr_of(pd_code, env)
                except Exception as e:
                    if not want_raise:
                        problems.append(
                            f"{locator[:40]!r}: pandas snippet raised {type(e).__name__}: {e}"
                        )
                        continue
                    # Expected: the Polars cell raises, so its twin must too. Render it the way
                    # `committed_output` renders the live cell's error, so the two panes match in
                    # shape and the frozen block carries no traceback paths.
                    pd_out = f"{type(e).__name__}: {e}"
                else:
                    if want_raise:
                        problems.append(
                            f"{locator[:40]!r}: the Polars cell raises but the pandas twin did not -- "
                            "the tab would claim both libraries accept this"
                        )
                        continue
                # A tab whose two panes are byte-identical shows the reader nothing. Counted rather
                # than silently dropped, so "how many operations are literally the same in both
                # libraries" stays a number someone can look at.
                if _same_operation(pd_code, pl_code) and pd_out == pl_out:
                    identical += 1
                    continue
                blocks[locator] = build_block(locator, pl_code, pl_out, pd_code, pd_out)
        finally:
            os.chdir(cwd)

    if verify:
        text = "\n".join(c.source for c in nb.cells if c.cell_type == "markdown")
        churners = OUTPUT_CHURNS.get(chapter, set())
        code_only = 0
        for locator, want in blocks.items():
            if locator in churners:
                # The output was never going to hold still, so check what can be checked: the
                # marker is present and both code panes are verbatim. Reported, not hidden.
                code_only += 1
                panes = re.findall(r"```python\n(.*?)\n```", want, re.S)
                missing = [pane for pane in panes if pane not in text]
                if want.splitlines()[0] not in text or missing:
                    problems.append(f"{locator[:40]!r}: the tab block's code does not match a fresh run")
                continue
            if want not in text:
                problems.append(f"{locator[:40]!r}: the tab block on the page does not match a fresh run")
        note = f", {code_only} checked code-only (output churns by design)" if code_only else ""
        print(f"  {chapter}: {len(blocks)} twin(s), {'STALE' if problems else 'fresh'}{note}")
    else:
        note = f", {identical} identical pair(s) skipped" if identical else ""
        print(f"  {chapter}: {len(blocks)} block(s) generated{note}")
    for p_ in problems[:8]:
        print(f"    {p_}")
    return (1 if problems else 0), blocks


def apply_to_pytext(chapter: str, blocks: dict) -> int:
    """Write the tab blocks into the jupytext source, and hide the live cell they mirror.

    The live Polars cell keeps executing -- that is what proves the Polars code still runs and
    what `outputs-fresh` checks -- but it is hidden, because the tab beneath it shows the same
    code and the same output. Note `remove-cell` does *not* work in mystmd 1.6.6; only
    `remove-input` and `remove-output` set visibility, so hiding a whole cell needs both.
    """
    path = Path(f"conversion/pytext/polars/{chapter}/{chapter}.py")
    text = path.read_text()
    added = 0
    for key, block in blocks.items():
        # The dict key locates the cell in the `.py`; the marker names it in the page. They are
        # the same string for a hand-written twin and deliberately differ for a baseline-paired
        # one, whose marker is the cell id -- which the `.py` does not carry. So read the marker
        # off the block rather than assuming it equals the key.
        marker = block.splitlines()[0]
        commented = "\n".join(("# " + l).rstrip() for l in block.splitlines())
        existing = re.search(
            re.escape("# " + marker) + r".*?" + re.escape("# " + MARK_END),
            text, re.S,
        )
        if existing:
            text = text[:existing.start()] + commented + text[existing.end():]
            added += 1
            continue
        # locate the live cell containing the key, and the start of the next cell
        idx = text.find(key)
        if idx == -1:
            print(f"    {key[:44]!r}: not found in pytext")
            continue
        head = text.rfind("\n# %%", 0, idx)
        nxt = text.find("\n# %%", idx)
        if head == -1 or nxt == -1:
            print(f"    {key[:44]!r}: could not bound the cell")
            continue
        # tag the live cell so it stays executable but stops rendering
        line_end = text.find("\n", head + 1)
        header = text[head + 1:line_end]
        # A locator can match inside prose -- a `{dropdown}` repeats its cell's code verbatim, and
        # the chapter intro quotes the loader. Walking back from such a match lands on a *markdown*
        # header, and tagging that wrecks it: `# %% [markdown]` becomes
        # `# %% tags=[...] [markdown]`, which jupytext no longer reads as markdown, so the cell
        # renders as code. That is how the Polars II title stopped rendering and the frontmatter
        # showed up as comments on the page. Never tag a markdown cell; report instead.
        if "[markdown]" in header:
            print(f"    {key[:44]!r}: matched inside a markdown cell -- pick a locator that only "
                  "appears in the live code cell")
            continue
        if "tags=" not in header:
            header = header.replace("# %%", '# %% tags=["remove-input", "remove-output"]', 1)
            text = text[:head + 1] + header + text[line_end:]
            nxt = text.find("\n# %%", text.find(key))
        text = text[:nxt] + "\n\n# %% [markdown]\n" + commented + "\n" + text[nxt:]
        added += 1
    path.write_text(text)
    print(f"  {chapter}: applied {added} block(s) to {path}")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--emit", action="store_true", help="Execute and write the tab blocks")
    ap.add_argument("--verify", action="store_true", help="Re-execute and diff against the page")
    ap.add_argument("--apply", action="store_true", help="Write the blocks into the jupytext source")
    ap.add_argument("--chapter", action="append")
    ap.add_argument("--from-baseline", action="store_true",
                    help="Pair the pandas half by cell id against the pinned baseline, instead of "
                         "executing hand-written snippets. Works for translated chapters only.")
    a = ap.parse_args()
    if not (a.emit or a.verify or a.apply):
        ap.error("pass --emit, --apply or --verify")
    rc = 0
    default = list(TWINS)
    if a.from_baseline and not a.chapter:
        import json as _json
        default = [c["chapter"] for c in _json.load(open("conversion/state.json"))
                   if c["tier"] not in ("A", "D") and c["source"].endswith(".ipynb")]
    for ch in (a.chapter or default):
        # The blocks are handed straight from generation to application, in memory. They are
        # deliberately never written to disk in between: the .py and the executed .ipynb are
        # already the two places this content lives, and a third copy on disk would be one more
        # thing that can go stale -- the exact failure `--verify` exists to catch.
        code, blocks = run(ch, verify=a.verify, from_baseline=a.from_baseline)
        rc |= code
        if a.apply:
            rc |= apply_to_pytext(ch, blocks)
    sys.exit(rc)


if __name__ == "__main__":
    main()
