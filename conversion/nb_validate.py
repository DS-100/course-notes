#!/usr/bin/env python3
"""
Conversion gate battery.

Deterministic checks that a converted chapter is safe to publish. Every check is
pass/fail/inconclusive -- no judgment, no scoring. Judgment belongs to the reviewer agents,
which run after this exits 0.

    G1  structure           cell id sequence identical to baseline
    G2  no-pandas-code      no pandas in code cells, bar allowlisted interop
    G3  prose-code-blocks   no pandas in fenced code blocks inside markdown
    G4  dropdown-mirror     every baseline dropdown/code pair still byte-identical
    G5  myst-fences         per-cell fence and directive counts unchanged
    G6  outputs-fresh       no pandas reprs; corroborated execution witness
    G7  outputs-coverage    a cell that had output still has output
    G8  output-churn        ADVISORY: outputs that moved without their source moving
    G9  error-outputs       erroring cells match baseline in both directions
    G10 tags                per-cell tag sets unchanged
    G11 frontmatter         cell 0 title block intact
    G12 alt-text            {image} and fig-alt counts preserved, none empty
    G13 doc-links           pandas docs repointed, not deleted

A chapter whose baseline contains no pandas at all is checked by a different predicate
entirely: its content must be byte-identical to the baseline. sql_I, sql_II and the five
prose-only .md chapters need no conversion, so any change to them is a defect, and asserting
that is a far stronger check than running thirteen gates that all pass vacuously.

## The anti-vacuous-pass contract

The sibling repo shipped two green-but-meaningless passes: a crashed build satisfied every
gate, and a gate computed a finding it never folded into its verdict. Five rules, enforced
here in the collector rather than trusted to each gate's prose:

  1. Denominators come from the baseline, never from the artifact under test.
  2. `n_checked == 0` while `n_expected > 0` is INCONCLUSIVE, never PASS. There is no code
     path from "found nothing to check" to a green gate.
  3. A missing artifact is FAIL, never SKIP.
  4. Alignment is a precondition: if G1 fails, every id-aligned gate returns INCONCLUSIVE
     rather than reporting on cells it cannot trust it has paired correctly.
  5. Every removal gate is paired with a presence gate, so deleting content is never a way
     to pass.

`--self-test` is the negative control: it runs the battery against the pandas baseline and
asserts the removal gates FAIL while the structural gates PASS. A battery that passes on
pandas is broken, and so is one that flags an artifact as changed when nothing changed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import nbformat
import yaml

import chapters as ch
import nb_baseline

ALLOWLIST_PATH = Path("conversion/conversion_allowlist.yml")

PASS, FAIL, INCONCLUSIVE = "PASS", "FAIL", "INCONCLUSIVE"

# Gates whose verdict never blocks. G8 exists to orient a reviewer inside a large diff,
# not to stop the pipeline.
ADVISORY = {"output-churn"}

DATAWRANGLER_MIME = "application/vnd.microsoft.datawrangler.viewer.v0+json"

# `class="dataframe"` is NOT a pandas marker: polars emits the same class on its own HTML
# table, so a detector built on it flags every correctly-converted chapter and can never reach
# zero. The two libraries differ in where they put the alignment style -- pandas writes it
# inline on the header row, polars in a <style> block -- and polars prefixes the table with a
# shape header that pandas has no equivalent for. Either one discriminates; using both means a
# chapter that hides the shape header via pl.Config is still classified correctly.
PANDAS_HTML_REPR = '<tr style="text-align: right;'
POLARS_HTML_REPR = "<small>shape: ("
PANDAS_DOCS = "pandas.pydata.org"
POLARS_DOCS = "pola.rs"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\s*$", re.S | re.M)
IMAGE_DIRECTIVE_RE = re.compile(r"^`{3,}\{image\}", re.M)
FIG_ALT_RE = re.compile(r"^\s*#\|\s*fig-alt\s*:(.*)$", re.M)
ALT_OPTION_RE = re.compile(r"^:alt:(.*)$", re.M)


def alt_is_empty(raw: str) -> bool:
    """Is this alt text actually absent?

    `.strip()` alone is not enough. `:alt:""` captures the two literal quote characters,
    which strip to a two-character string and read as present -- so the gate reported
    "all non-empty" on `gradient_descent`, which carries three empty alts (`ols_matrices_new.png`,
    `grad_descent_1.png`, `grad_descent_2.png`). A presence gate that cannot see an absence is
    the same failure as a removal gate that cannot see a survivor.
    """
    return not raw.strip().strip("\"'").strip()


# ------------------------------------------------------------------ collector


@dataclass
class GateResult:
    name: str
    verdict: str
    n_checked: int
    n_expected: int
    details: List[str] = field(default_factory=list)

    @property
    def blocking(self) -> bool:
        return self.name not in ADVISORY


@dataclass
class Result:
    chapter: str
    gates: List[GateResult] = field(default_factory=list)

    def add(
        self,
        name: str,
        ok: bool,
        n_checked: int,
        n_expected: int,
        details: Optional[Sequence[str]] = None,
    ) -> GateResult:
        """Record a gate. Rule 2 is applied here so no gate can opt out of it."""
        if n_expected > 0 and n_checked == 0:
            verdict = INCONCLUSIVE
            details = list(details or []) + [
                f"examined 0 of {n_expected} expected items -- scanner found nothing to check"
            ]
        else:
            verdict = PASS if ok else FAIL
        g = GateResult(name, verdict, n_checked, n_expected, list(details or []))
        self.gates.append(g)
        return g

    def inconclusive(self, name: str, reason: str) -> None:
        self.gates.append(GateResult(name, INCONCLUSIVE, 0, 0, [reason]))

    def get(self, name: str) -> Optional[GateResult]:
        return next((g for g in self.gates if g.name == name), None)

    @property
    def ok(self) -> bool:
        return all(g.verdict == PASS for g in self.gates if g.blocking)

    def debt(self) -> int:
        """A machine-computed scalar for the orchestrator's monotonic-improvement check.

        Deliberately not a reviewer score: a reviewer that tires of a chapter can talk
        itself into a better number, and the loop then grinds on a chapter that is not
        actually improving.
        """
        blocked = [g for g in self.gates if g.blocking]
        score = 5 * sum(1 for g in blocked if g.verdict == FAIL)
        score += 5 * sum(1 for g in blocked if g.verdict == INCONCLUSIVE)
        for name in ("no-pandas-code", "prose-code-blocks", "dropdown-mirror"):
            g = self.get(name)
            if g and g.verdict != PASS:
                score += len(g.details)
        return score

    def fingerprint(self) -> str:
        """Stable hash of the failure set, so a loop that 'improves' by shuffling stops."""
        failures = sorted(
            f"{g.name}:{d}" for g in self.gates if g.verdict != PASS and g.blocking for d in g.details
        )
        return hashlib.sha1("\n".join(failures).encode()).hexdigest()[:12]

    def report(self) -> None:
        print(f"\n{'=' * 78}\n  {self.chapter}\n{'=' * 78}")
        for g in self.gates:
            tag = f"[{g.verdict}]".ljust(15)
            scope = f"{g.n_checked}/{g.n_expected}" if g.n_expected else "-"
            flag = "" if g.blocking else "  (advisory)"
            print(f"  {tag} {g.name:<20} {scope:>9}{flag}")
            for d in g.details[:10]:
                print(f"                  {d}")
            if len(g.details) > 10:
                print(f"                  ... and {len(g.details) - 10} more")
        print("-" * 78)
        print(f"  {'ALL GATES PASSED' if self.ok else 'GATES FAILED'}   debt={self.debt()}   fp={self.fingerprint()}\n")

    def to_dict(self) -> Dict:
        return {
            "chapter": self.chapter,
            "ok": self.ok,
            "debt": self.debt(),
            "fingerprint": self.fingerprint(),
            "gates": [
                {
                    "name": g.name,
                    "verdict": g.verdict,
                    "n_checked": g.n_checked,
                    "n_expected": g.n_expected,
                    "details": g.details,
                }
                for g in self.gates
            ],
        }


# ------------------------------------------------------------------ helpers


def allow(chapter: str, section: str) -> Dict[str, str]:
    if not ALLOWLIST_PATH.exists():
        return {}
    data = yaml.safe_load(ALLOWLIST_PATH.read_text()) or {}
    entries = (data.get(chapter) or {}).get(section, []) or []
    out = {}
    for e in entries:
        key = e.get("cell_id") or e.get("tag") or e.get("line") or e.get("path") or "*"
        out[key] = e.get("reason", "")
    return out


def read_nb(path: Path):
    return nbformat.read(str(path), as_version=4)


def code_cells(nb) -> List:
    return [c for c in nb.cells if c.cell_type == "code"]


def md_cells(nb) -> List:
    return [c for c in nb.cells if c.cell_type == "markdown"]


def source_of(path: Path) -> str:
    """Full text of a chapter source, notebook or markdown."""
    if path.suffix == ".md":
        return path.read_text()
    nb = read_nb(path)
    return "\n".join(c.get("source", "") for c in nb.cells)


def markdown_text(path: Path) -> str:
    if path.suffix == ".md":
        return path.read_text()
    return "\n".join(c.get("source", "") for c in md_cells(read_nb(path)))


def outputs_digest(cell) -> str:
    """Hash a cell's outputs, ignoring execution_count (which moves on every run)."""
    payload = []
    for o in cell.get("outputs", []):
        o = dict(o)
        o.pop("execution_count", None)
        payload.append(o)
    return hashlib.sha1(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:12]


CELL_DIRECTIVE_RE = re.compile(r"^\s*#\|")


def mirror_normalize(src: str) -> str:
    """A mirror's text, ignoring cell directives the dropdown never repeats.

    A code cell often opens with `#| fig-alt: ...`, which its dropdown copy omits -- the
    directive configures the cell, it is not part of the code being shown. Pairing on exact
    equality therefore *failed to register those pairs at all*, and an unregistered pair is
    never checked: 4 of modeling_slr's 5 mirrors and 1 of visualization_1's were invisible
    to the gate that exists to catch exactly this defect. Since the pair list is built from
    the baseline, the miss was permanent rather than something a conversion could trip.

    `#| fig-alt` content is not going unchecked -- G12 owns it.
    """
    lines = [l for l in src.strip().splitlines() if not CELL_DIRECTIVE_RE.match(l)]
    return "\n".join(lines).strip()


def mirror_pairs(nb) -> Dict[Tuple[str, str], str]:
    """(markdown cell id, code cell id) -> the shared text, for verbatim mirrors.

    The repo's documented pattern: a `{dropdown}` in a markdown cell repeats the source of
    the next code cell, which carries `remove-input` so only its output renders. 82 such
    pairs exist, 31 of them carrying pandas. Convert the code cell alone and the page shows
    pandas source above Polars output -- the single highest-probability silent defect here,
    and one no code-cell scanner can see.
    """
    cells = nb.cells
    pairs: Dict[Tuple[str, str], str] = {}
    for i, c in enumerate(cells):
        if c.cell_type != "markdown":
            continue
        for block in ch.markdown_code_blocks(c.get("source", "")):
            body = mirror_normalize(block)
            if not body:
                continue
            nxt = next(
                (cells[j] for j in range(i + 1, min(i + 3, len(cells))) if cells[j].cell_type == "code"),
                None,
            )
            if nxt is not None and body == mirror_normalize(nxt.get("source", "")):
                pairs[(c.get("id"), nxt.get("id"))] = body
    return pairs


def fence_profile(text: str) -> Tuple[int, int, int, int, int]:
    """The shape of a markdown cell that must survive editing.

    An edit inside a 4-backtick `{dropdown}` that wraps a 3-backtick `python` block can
    unbalance the nesting. MyST then renders the remainder of the cell as a code block --
    and exits 0. Nothing else in the pipeline notices.
    """
    return (
        len(re.findall(r"^`{4,}", text, re.M)),
        len(re.findall(r"^`{3}(?!`)", text, re.M)),
        len(re.findall(r"^:::", text, re.M)),
        len(re.findall(r"\{image\}", text)),
        len(re.findall(r"\{dropdown\}", text)),
    )


# ------------------------------------------------------------------ gates


def gate_structure(base_nb, conv_nb, res: Result) -> bool:
    base_seq = [(c.get("id"), c.cell_type) for c in base_nb.cells]
    conv_seq = [(c.get("id"), c.cell_type) for c in conv_nb.cells]
    details = []
    if len(base_seq) != len(conv_seq):
        details.append(f"cell count changed: {len(base_seq)} -> {len(conv_seq)}")
    base_ids = {i for i, _ in base_seq}
    conv_ids = {i for i, _ in conv_seq}
    for missing in sorted(base_ids - conv_ids)[:6]:
        details.append(f"cell removed: {missing}")
    for added in sorted(conv_ids - base_ids)[:6]:
        details.append(f"cell added: {added}")
    if base_seq != conv_seq and not details:
        details.append("cell order or type changed with no add/remove -- cells were reordered")
    ok = base_seq == conv_seq
    if ok:
        details.append(f"{len(base_seq)} cells, id sequence identical")
    res.add("structure", ok, len(conv_seq), len(base_seq), details)
    return ok


def gate_no_pandas_code(chapter: ch.Chapter, conv_nb, base_nb, res: Result) -> None:
    interop = allow(chapter.name, "interop")
    cells = code_cells(conv_nb)
    hits = []
    sanctioned = 0
    for c in cells:
        for line in c.get("source", "").splitlines():
            if ch.INTEROP.search(line):
                cid = c.get("id")
                if cid in interop or "*" in interop:
                    sanctioned += 1
                    continue
                hits.append(f"{cid}: unallowlisted .to_pandas() -- {line.strip()[:64]}")
                continue
            if ch.PANDAS_ONLY.search(line):
                hits.append(f"{c.get('id')}: {line.strip()[:64]}")
    details = hits[:8] if hits else [
        f"{len(cells)} code cells clean"
        + (f"; {sanctioned} allowlisted interop site(s)" if sanctioned else "")
    ]
    res.add("no-pandas-code", not hits, len(cells), len(code_cells(base_nb)), details)


TWIN_REGION_RE = re.compile(
    r"<!-- tab-twins:begin .*?-->(.*?)<!-- tab-twins:end -->", re.S
)
PANDAS_TAB_RE = re.compile(
    r"::::\s*\{tab-item\}\s*pandas\b(.*?)(?=\n::::(?!:)|\Z)", re.S | re.I
)


def strip_pandas_tabs(md: str) -> Tuple[str, int]:
    """Blank out the pandas half of each comparison tab, and count how many were blanked.

    Course staff added Pandas/Polars comparison tabs, so pandas now appears in fenced blocks on
    purpose. The exemption is deliberately narrow: only inside an explicit
    `tab-twins:begin/end` region, and only within the `{tab-item} pandas` half of it. The Polars
    half of the same tab is still scanned -- pandas leaking into a tab labelled Polars is a real
    defect, and blanketing the whole region would hide it.
    """
    n = 0

    def blank_region(m: re.Match) -> str:
        nonlocal n
        body = m.group(1)

        def blank_tab(t: re.Match) -> str:
            nonlocal n
            n += 1
            return "\n".join("" for _ in t.group(0).splitlines())

        return PANDAS_TAB_RE.sub(blank_tab, body)

    return TWIN_REGION_RE.sub(blank_region, md), n


def gate_prose_code_blocks(chapter: ch.Chapter, conv_path: Path, base_path: Path, res: Result) -> None:
    conv_md = markdown_text(conv_path)
    base_md = markdown_text(base_path)
    scanned, n_exempt = strip_pandas_tabs(conv_md)
    n_base = len(ch.markdown_code_blocks(base_md))
    n_conv = len(ch.markdown_code_blocks(scanned))
    hits = ch.markdown_pandas_sites(scanned)
    note = f"; {n_exempt} pandas comparison tab(s) exempt" if n_exempt else ""
    details = hits[:8] if hits else [
        f"{n_conv} fenced block(s) in markdown, none carrying pandas{note}"
    ]
    res.add("prose-code-blocks", not hits, n_conv, n_base, details)


def gate_dropdown_mirror(base_nb, conv_nb, res: Result) -> None:
    base_pairs = mirror_pairs(base_nb)
    conv_by_id = {c.get("id"): c for c in conv_nb.cells}
    broken, missing = [], []
    checked = 0

    for (md_id, code_id) in base_pairs:
        md_cell, code_cell = conv_by_id.get(md_id), conv_by_id.get(code_id)
        if md_cell is None or code_cell is None:
            missing.append(f"pair {md_id}/{code_id}: a cell no longer exists")
            continue
        checked += 1
        blocks = [mirror_normalize(b) for b in ch.markdown_code_blocks(md_cell.get("source", ""))]
        code_src = mirror_normalize(code_cell.get("source", ""))
        if code_src not in blocks:
            broken.append(
                f"{md_id} no longer mirrors {code_id}: the dropdown shows different code "
                "than the cell that produces the output"
            )

    details = (broken + missing)[:8] if (broken or missing) else [
        f"{checked} dropdown/code pair(s) still byte-identical"
    ]
    res.add("dropdown-mirror", not (broken or missing), checked, len(base_pairs), details)


def gate_myst_fences(base_nb, conv_nb, res: Result) -> None:
    base_md = {c.get("id"): c.get("source", "") for c in md_cells(base_nb)}
    conv_md = {c.get("id"): c.get("source", "") for c in md_cells(conv_nb)}
    problems, checked = [], 0
    for cid, base_src in base_md.items():
        if cid not in conv_md:
            continue
        checked += 1
        b, c = fence_profile(base_src), fence_profile(conv_md[cid])
        if b != c:
            labels = ("4-backtick", "3-backtick", ":::", "{image}", "{dropdown}")
            moved = [f"{lab} {x}->{y}" for lab, x, y in zip(labels, b, c) if x != y]
            problems.append(f"{cid}: {', '.join(moved)}")
    details = problems[:8] if problems else [f"{checked} markdown cell(s), fence profile unchanged"]
    res.add("myst-fences", not problems, checked, len(base_md), details)


def gate_outputs_fresh(chapter: ch.Chapter, base_nb, conv_nb, res: Result) -> None:
    cells = code_cells(conv_nb)
    base_with_df = sum(
        1
        for c in code_cells(base_nb)
        for o in c.get("outputs", [])
        if PANDAS_HTML_REPR in "".join(o.get("data", {}).get("text/html", ""))
    )

    stale_df, stale_dw, polars_reprs = [], [], 0
    for c in cells:
        for o in c.get("outputs", []):
            html = "".join(o.get("data", {}).get("text/html", ""))
            text = "".join(o.get("data", {}).get("text/plain", ""))
            if PANDAS_HTML_REPR in html:
                stale_df.append(f"{c.get('id')}: pandas HTML repr still committed")
            if DATAWRANGLER_MIME in o.get("data", {}):
                stale_dw.append(f"{c.get('id')}: VS Code Data Wrangler mime -- cell was not re-executed")
            if POLARS_HTML_REPR in html or "shape: (" in text:
                polars_reprs += 1

    w = conv_nb.metadata.get("polars_conversion") or {}
    problems = stale_df[:4] + stale_dw[:4]

    # The witness is verified against the artifact, never trusted as a claim. A forged
    # stamp cannot make execution_counts strictly increasing across every code cell.
    if not w:
        problems.append("no execution witness: run nb_execute.py before validating")
    else:
        if w.get("n_executed") != w.get("n_code_cells"):
            problems.append(f"witness: only {w.get('n_executed')}/{w.get('n_code_cells')} cells executed")
        counts = [c.get("execution_count") for c in cells if c.get("source", "").strip()]
        missing = [c.get("id") for c in cells if c.get("source", "").strip() and c.get("execution_count") is None]
        present = [x for x in counts if x is not None]
        if missing:
            problems.append(f"{len(missing)} code cell(s) carry no execution_count, e.g. {missing[0]}")
        elif present != sorted(present) or len(set(present)) != len(present):
            problems.append("execution_counts are not strictly increasing -- not a single clean run")
        if w.get("baseline_sha") != nb_baseline.read_lock()["main_sha"]:
            problems.append("witness was produced against a different baseline; re-execute")

    # Pair-gate for the two removal checks above: deleting every output would satisfy
    # "no pandas repr" trivially. Polars reprs have to show up in their place.
    if base_with_df and polars_reprs == 0:
        problems.append(
            f"baseline had {base_with_df} dataframe output(s) and the conversion has none -- "
            "outputs were dropped rather than regenerated"
        )

    details = problems[:8] if problems else [
        f"{len(cells)} code cells executed under polars {w.get('polars')}; "
        f"{polars_reprs} polars repr(s), 0 pandas reprs"
    ]
    res.add("outputs-fresh", not problems, len(cells), len(code_cells(base_nb)), details)


def gate_outputs_coverage(base_nb, conv_nb, res: Result) -> None:
    conv_by_id = {c.get("id"): c for c in code_cells(conv_nb)}
    expected = [c for c in code_cells(base_nb) if c.get("outputs")]
    lost, checked = [], 0
    for c in expected:
        target = conv_by_id.get(c.get("id"))
        if target is None:
            continue
        checked += 1
        if not target.get("outputs"):
            lost.append(f"{c.get('id')}: had output in the baseline, has none now")
    details = lost[:8] if lost else [f"{checked} cell(s) that carried output still do"]
    res.add("outputs-coverage", not lost, checked, len(expected), details)


def gate_output_churn(base_nb, conv_nb, res: Result) -> None:
    """Advisory. Under full re-execution this is the reviewer's map of what to ignore."""
    base_by_id = {c.get("id"): c for c in code_cells(base_nb)}
    churned = []
    for c in code_cells(conv_nb):
        prior = base_by_id.get(c.get("id"))
        if prior is None:
            continue
        source_changed = ch.normalize_source(prior.get("source", "")) != ch.normalize_source(
            c.get("source", "")
        )
        output_changed = outputs_digest(prior) != outputs_digest(c)
        if output_changed and not source_changed:
            churned.append(f"{c.get('id')}: output changed, source did not")
    details = churned[:10] if churned else ["no output moved without its source moving"]
    res.add("output-churn", True, len(code_cells(conv_nb)), len(base_by_id), details)


def gate_error_outputs(chapter: ch.Chapter, base_nb, conv_nb, res: Result) -> None:
    def errs(nb):
        return {
            c.get("id"): o.get("ename", "?")
            for c in code_cells(nb)
            for o in c.get("outputs", [])
            if o.get("output_type") == "error"
        }

    base, conv = errs(base_nb), errs(conv_nb)
    allow_new = allow(chapter.name, "expected_errors")
    allow_gone = allow(chapter.name, "resolved_errors")

    problems = []
    for cid, ename in conv.items():
        if cid not in base and cid not in allow_new:
            problems.append(f"{cid}: new error {ename}")
    for cid, ename in base.items():
        if cid not in conv and cid not in allow_gone:
            problems.append(
                f"{cid}: baseline raised {ename}, now silent -- the prose around it "
                "describes an error the reader will not see"
            )
    if problems:
        details = problems[:8]
    elif len(conv) == len(base):
        details = [f"{len(conv)} erroring cell(s), matching the baseline's {len(base)}"]
    else:
        # Counts differ and nothing was flagged, so the allowlist is what carried it. Say so:
        # "0 erroring cell(s), matching the baseline's 1" is self-contradictory on its face and
        # would sit in gate logs indefinitely, reading like a bug in the gate rather than a
        # recorded decision.
        resolved = sorted(cid for cid in base if cid not in conv)
        added = sorted(cid for cid in conv if cid not in base)
        via = []
        if resolved:
            via.append(f"{len(resolved)} resolved via allowlist ({', '.join(resolved)})")
        if added:
            via.append(f"{len(added)} expected via allowlist ({', '.join(added)})")
        details = [f"{len(conv)} erroring cell(s); baseline had {len(base)} -- " + "; ".join(via)]
    res.add("error-outputs", not problems, len(code_cells(conv_nb)), len(code_cells(base_nb)), details)


def gate_tags(chapter: ch.Chapter, base_nb, conv_nb, res: Result) -> None:
    allowed = allow(chapter.name, "tag_changes")
    conv_by_id = {c.get("id"): c for c in conv_nb.cells}
    problems, checked = [], 0
    for c in base_nb.cells:
        target = conv_by_id.get(c.get("id"))
        if target is None:
            continue
        checked += 1
        b = set(c.get("metadata", {}).get("tags", []) or [])
        n = set(target.get("metadata", {}).get("tags", []) or [])
        if b == n or c.get("id") in allowed:
            continue
        added, removed = sorted(n - b), sorted(b - n)
        note = []
        if added:
            note.append(f"added {', '.join(added)}")
        if removed:
            note.append(f"removed {', '.join(removed)}")
        problems.append(f"{c.get('id')}: {'; '.join(note)}")
    details = problems[:8] if problems else [f"{checked} cell(s), tag sets unchanged"]
    res.add("tags", not problems, checked, len(base_nb.cells), details)


def gate_frontmatter(chapter: ch.Chapter, base_path: Path, conv_path: Path, res: Result) -> None:
    def first_block(path: Path) -> Optional[str]:
        if path.suffix == ".md":
            text = path.read_text()
        else:
            cells = read_nb(path).cells
            text = cells[0].get("source", "") if cells else ""
        m = re.match(r"\A---\n(.*?)\n---", text, re.S)
        return m.group(1) if m else None

    base_block, conv_block = first_block(base_path), first_block(conv_path)
    allowed = allow(chapter.name, "frontmatter")
    problems = []

    if base_block is None:
        res.add("frontmatter", True, 0, 0, ["baseline carries no frontmatter block"])
        return
    if conv_block is None:
        problems.append(
            "the --- title block is no longer the first construct; MyST will silently "
            "fall back to the filename for the page title and still exit 0"
        )
    else:
        try:
            b, c = yaml.safe_load(base_block) or {}, yaml.safe_load(conv_block) or {}
        except yaml.YAMLError as e:
            problems.append(f"frontmatter no longer parses: {e}")
            b = c = {}
        if b != c and not allowed:
            problems.append(f"frontmatter changed: {b} -> {c} (allowlist it if intended)")

    details = problems if problems else [f"title block intact: {conv_block.strip()[:60] if conv_block else ''}"]
    res.add("frontmatter", not problems, 1, 1, details)


def gate_alt_text(chapter_name: str, base_path: Path, conv_path: Path, res: Result) -> None:
    base_text, conv_text = source_of(base_path), source_of(conv_path)
    b_img, c_img = len(IMAGE_DIRECTIVE_RE.findall(base_text)), len(IMAGE_DIRECTIVE_RE.findall(conv_text))
    b_alt, c_alt = len(FIG_ALT_RE.findall(base_text)), len(FIG_ALT_RE.findall(conv_text))

    # Losing an accessibility surface is the defect; adding one is the goal. An authored tier-D
    # chapter writes new figures and gives each a `#| fig-alt`, which under an equality check reads
    # as a failure for doing exactly the right thing -- polars_2 went 0 -> 6 and failed. So the
    # gate is one-sided: a decrease fails, an increase is reported and passes. Emptiness is still
    # checked separately below, so this cannot be gamed by adding blank alts.
    problems = []
    # A figure may legitimately be dropped -- `polars_2` removed a screenshot of a *pandas*
    # traceback that no code gate can see inside. That needs a recorded reason, like every other
    # removal in this harness, so it is an allowlist entry rather than a silent count change.
    dropped_ok = len(allow(chapter_name, "removed_figures"))
    if c_img < b_img - dropped_ok:
        problems.append(f"{{image}} directives {b_img} -> {c_img}: a figure lost its directive")
    if c_alt < b_alt:
        problems.append(f"#| fig-alt comments {b_alt} -> {c_alt}: a figure lost its alt text")
    gained = (c_img - b_img) + (c_alt - b_alt)
    # Empties are counted on both sides rather than merely detected on one. Several chapters
    # carry empty alts in the baseline -- gradient_descent has three -- and failing a
    # conversion for content debt it inherited would block work on a defect it did not cause.
    # What must never happen is the conversion *emptying* one, so the comparison is the gate
    # and the pre-existing count is reported rather than swallowed.
    def empties(text: str) -> Tuple[int, int]:
        return (
            sum(1 for m in FIG_ALT_RE.finditer(text) if alt_is_empty(m.group(1))),
            sum(1 for m in ALT_OPTION_RE.finditer(text) if alt_is_empty(m.group(1))),
        )

    b_efa, b_ealt = empties(base_text)
    c_efa, c_ealt = empties(conv_text)
    if c_efa > b_efa:
        problems.append(f"conversion emptied a #| fig-alt ({b_efa} -> {c_efa}): a11y.yml fails this in CI")
    if c_ealt > b_ealt:
        problems.append(f"conversion emptied an :alt: option on an {{image}} ({b_ealt} -> {c_ealt})")

    inherited = c_efa + c_ealt
    details = problems if problems else [
        f"{c_img} {{image}} + {c_alt} fig-alt"
        + (f"; {gained} added" if gained > 0 else "")
        + (f"; {inherited} empty in the baseline too, none emptied here" if inherited
           else ", all non-empty")
    ]
    res.add("alt-text", not problems, c_img + c_alt, b_img + b_alt, details)


def gate_doc_links(chapter: ch.Chapter, base_path: Path, conv_path: Path, res: Result) -> None:
    base_text, conv_text = source_of(base_path), source_of(conv_path)
    b_pandas = base_text.count(PANDAS_DOCS)
    c_pandas = conv_text.count(PANDAS_DOCS)
    c_polars = conv_text.count(POLARS_DOCS)
    allowed = allow(chapter.name, "doc_links")

    problems = []
    if c_pandas and not allowed:
        problems.append(f"{c_pandas} link(s) still point at {PANDAS_DOCS}")
    # Pair-gate: repointing is required, deleting is not an acceptable substitute.
    # Reading documentation is a course outcome, so a vanished link is also a defect.
    if b_pandas and c_polars < b_pandas - c_pandas and not allowed:
        problems.append(
            f"baseline had {b_pandas} pandas doc link(s); the conversion has {c_polars} "
            f"polars link(s) -- links were deleted rather than repointed"
        )
    details = problems if problems else [
        f"{b_pandas} pandas doc link(s) repointed; {c_polars} link(s) to {POLARS_DOCS}"
    ]
    res.add("doc-links", not problems, c_polars + c_pandas, b_pandas, details)


def gate_unchanged(chapter: ch.Chapter, base_path: Path, conv_path: Path, res: Result) -> None:
    """The whole battery for a chapter that has no pandas to begin with.

    sql_I and sql_II are pure %%sql/jupysql/duckdb; the five prose-only .md chapters carry
    no executable code at all. None of them needs converting, so the useful predicate is not
    "did the conversion go well" but "did anything change at all" -- and any change is a
    defect. Running the other thirteen gates on them would produce thirteen vacuous passes.
    """
    base_bytes = base_path.read_bytes()
    conv_bytes = conv_path.read_bytes()
    if base_bytes == conv_bytes:
        res.add("unchanged", True, 1, 1, ["byte-identical to the baseline, as required"])
        return

    base_nb_text = source_of(base_path)
    conv_nb_text = source_of(conv_path)
    detail = "file differs from the baseline"
    if base_nb_text != conv_nb_text:
        detail += "; cell sources changed"
    else:
        detail += "; sources match, so outputs or metadata moved"
    res.add(
        "unchanged",
        False,
        1,
        1,
        [detail, "this chapter has no pandas and must not be edited"],
    )


# ------------------------------------------------------------------ driver


def baseline_has_pandas(base_path: Path) -> bool:
    """Does this chapter need converting at all?

    Derived from the baseline rather than configured, so a chapter can never be routed to
    the wrong predicate by a stale tier in a state file.
    """
    if base_path.suffix == ".md":
        text = base_path.read_text()
        return bool(ch.PANDAS_ONLY.search(text) or ch.markdown_pandas_sites(text))
    nb = read_nb(base_path)
    for c in code_cells(nb):
        if ch.PANDAS_ONLY.search(c.get("source", "")):
            return True
    return bool(ch.markdown_pandas_sites(markdown_text(base_path)))


def validate(chapter: ch.Chapter, self_test: bool = False) -> Result:
    res = Result(chapter.name)
    lock = nb_baseline.read_lock()
    try:
        paths = nb_baseline.cached_paths(chapter, lock)
    except RuntimeError as e:
        res.inconclusive("baseline", str(e))
        return res

    base_path = paths["source"]
    if base_path is None:
        res.inconclusive(
            "baseline",
            f"no baseline for '{chapter.name}' at {lock['main_sha'][:12]}. A newly authored "
            "chapter has nothing to diff against; review it by hand and record it in CONVERSIONS.md.",
        )
        return res

    # --self-test runs the battery against the baseline itself: the negative control.
    conv_path = base_path if self_test else chapter.source
    if not conv_path.exists():
        res.add("artifact", False, 0, 1, [f"missing: {conv_path}"])
        return res

    if not baseline_has_pandas(base_path) and not self_test:
        gate_unchanged(chapter, base_path, conv_path, res)
        return res

    if not chapter.is_notebook:
        # A prose-only chapter that does mention pandas in fenced blocks: only the text
        # gates apply, and they are the whole story for it.
        gate_prose_code_blocks(chapter, conv_path, base_path, res)
        gate_frontmatter(chapter, base_path, conv_path, res)
        gate_alt_text(chapter.name, base_path, conv_path, res)
        gate_doc_links(chapter, base_path, conv_path, res)
        return res

    base_nb, conv_nb = read_nb(base_path), read_nb(conv_path)

    aligned = gate_structure(base_nb, conv_nb, res)

    gate_no_pandas_code(chapter, conv_nb, base_nb, res)
    gate_prose_code_blocks(chapter, conv_path, base_path, res)
    gate_frontmatter(chapter, base_path, conv_path, res)
    gate_alt_text(chapter.name, base_path, conv_path, res)
    gate_doc_links(chapter, base_path, conv_path, res)

    # Rule 4: everything below pairs cells by id. If the id sequence itself moved, those
    # pairings are untrustworthy, and a gate reporting on them would be guessing.
    if not aligned:
        for name in (
            "dropdown-mirror",
            "myst-fences",
            "outputs-fresh",
            "outputs-coverage",
            "output-churn",
            "error-outputs",
            "tags",
        ):
            res.inconclusive(name, "structure gate failed; cell pairing is not trustworthy")
        return res

    gate_dropdown_mirror(base_nb, conv_nb, res)
    gate_myst_fences(base_nb, conv_nb, res)
    gate_outputs_fresh(chapter, base_nb, conv_nb, res)
    gate_outputs_coverage(base_nb, conv_nb, res)
    gate_output_churn(base_nb, conv_nb, res)
    gate_error_outputs(chapter, base_nb, conv_nb, res)
    gate_tags(chapter, base_nb, conv_nb, res)
    return res


def self_test(chapter: ch.Chapter) -> bool:
    """Negative control: the battery run against the pandas baseline.

    Both directions matter. The removal gates must FAIL where the baseline actually has the
    surface they police -- a gate whose regex silently matches nothing would otherwise report
    green forever. And the structural gates must PASS on an identical pair, or they are
    flagging drift that does not exist and every real conversion inherits the false alarm.
    """
    res = validate(chapter, self_test=True)
    lock = nb_baseline.read_lock()
    base_path = nb_baseline.cached_paths(chapter, lock)["source"]
    if base_path is None:
        print(f"  {chapter.name}: no baseline, skipped")
        return True

    must_pass = ["structure", "dropdown-mirror", "myst-fences", "outputs-coverage", "tags", "frontmatter"]
    problems = []

    for name in must_pass:
        g = res.get(name)
        if g and g.verdict != PASS:
            problems.append(f"{name} reported {g.verdict} on an identical pair -- false alarm")

    # Conditional: a removal gate is only obliged to fire where the surface exists.
    #
    # These probes read the *parsed* notebook, not its raw text. Inside .ipynb JSON the
    # pandas repr is stored escaped as `class=\"dataframe\"`, so a substring search over the
    # file finds nothing and the outputs-fresh check would silently never be exercised --
    # exactly the class of bug this whole self-test exists to catch.
    is_nb = base_path.suffix == ".ipynb"
    base_nb = read_nb(base_path) if is_nb else None
    surfaces = {
        "no-pandas-code": bool(
            is_nb and any(ch.PANDAS_ONLY.search(c.get("source", "")) for c in code_cells(base_nb))
        ),
        "prose-code-blocks": bool(ch.markdown_pandas_sites(markdown_text(base_path))),
        "outputs-fresh": bool(
            is_nb
            and any(
                PANDAS_HTML_REPR in "".join(o.get("data", {}).get("text/html", ""))
                or DATAWRANGLER_MIME in o.get("data", {})
                for c in code_cells(base_nb)
                for o in c.get("outputs", [])
            )
        ),
        "doc-links": PANDAS_DOCS in source_of(base_path),
    }
    for name, present in surfaces.items():
        g = res.get(name)
        if not present or g is None:
            continue
        if g.verdict == PASS:
            problems.append(f"{name} passed on the pandas baseline -- the gate is not firing")

    status = "OK" if not problems else "BROKEN"
    checked = ", ".join(n for n, p in surfaces.items() if p) or "none"
    print(f"  [{status}] {chapter.name:<38} surfaces present: {checked}")
    for p in problems:
        print(f"           {p}")
    return not problems


def main() -> None:
    ap = argparse.ArgumentParser(description="Run the conversion gate battery.")
    ap.add_argument("--chapter", action="append", help="Chapter name (repeatable)")
    ap.add_argument("--all", action="store_true", help="Validate every chapter")
    ap.add_argument("--self-test", action="store_true",
                    help="Negative control: run the battery against the pandas baseline")
    ap.add_argument("--json", help="Write results to this path as JSON")
    ap.add_argument("--quiet", action="store_true", help="Only print the summary line")
    args = ap.parse_args()

    targets = ch.resolve(args.chapter) if args.chapter else (ch.resolve(None) if args.all else [])
    if not targets:
        raise SystemExit("nothing to do: pass --chapter <name> or --all")

    if args.self_test:
        print(f"\nSelf-test: the battery must fail on pandas and stay quiet on an identical pair\n")
        broken = [c.name for c in targets if not self_test(c)]
        print()
        if broken:
            print(f"BATTERY BROKEN on {len(broken)} chapter(s): {', '.join(broken)}")
            sys.exit(1)
        print(f"Battery sound across {len(targets)} chapter(s).")
        return

    results = []
    for chapter in targets:
        res = validate(chapter)
        results.append(res)
        if not args.quiet:
            res.report()

    failed = [r for r in results if not r.ok]
    print(f"{len(results) - len(failed)}/{len(results)} chapter(s) passed")
    for r in failed:
        bad = [g.name for g in r.gates if g.blocking and g.verdict != PASS]
        print(f"  FAIL {r.chapter}: {', '.join(bad)}")

    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps([r.to_dict() for r in results], indent=2))

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
