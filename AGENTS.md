# Standing rules — Data 100 course notes, pandas → Polars

Always in effect. Detail lives in `.claude/skills/`; this file is versions, hard constraints, and
commands only.

## Pinned versions

`polars==1.43.1` · Python 3.11 · conda env + Jupyter kernel `d100` · `jupyter-book` v2 (node) ·
baseline commit pinned in `conversion/baseline.lock`

```bash
export PATH="/Users/jedwin321/miniforge3/envs/d100/bin:$PATH"
```

**Export this before running anything, including a one-off `python3 -c` used to check a mapping.**
Several conda envs on this machine carry different Polars versions (`d100` 1.43.1, `cp101` 1.42.1,
`data6` 1.38.1, base 1.38.0), and the system `python3` is 3.9 with no polars at all. Verifying
against the wrong version is silent: the code runs, the answer looks right, and it does not describe
the environment the notebook will be executed in. Start any verification by printing
`polars.__version__` and confirming it reads 1.43.1.

The site build needs node on the PATH too:
`export PATH="/Users/jedwin321/.nvm/versions/node/v18.20.8/bin:$PATH"`.

## Hard rules

1. **Committed outputs are the deliverable.** CI runs `jupyter-book build --html` with no
   `--execute` and no pip install, so MyST publishes whatever outputs are committed. A converted cell
   whose output was not regenerated ships Polars code above a pandas table, and nothing in CI will
   ever catch it.
2. **Keep Polars-native output — move the prose to it, never the reverse.** No `.alias()`,
   `.rename()`, or `.sort()` whose only purpose is reproducing a pandas artifact. The bar is
   pedagogical equivalence, not identical output.
3. **The dropdown and the code cell are one edit.** 82 markdown blocks repeat the next code cell
   verbatim inside `` ```{dropdown} Click to see the code ``. Convert both or neither.
4. **`.to_pandas()` is a last resort and needs a written reason.** Polars goes to plotly, sklearn,
   scipy **and matplotlib** directly — `.to_numpy()` is needed only where NumPy's reduction dispatch
   refuses it, which the `pandas-to-polars` skill spells out. Every surviving `.to_pandas()` is
   allowlisted in `conversion/conversion_allowlist.yml`.
5. **Never silence a cell.** `remove-input` and `remove-cell` are layout. Using either to hide a cell
   that misbehaves is a hard failure, and so is deleting an output to make a gate pass.
6. **A cell that raises on purpose must keep raising.** Two exist: `eda` cell `a3fde967` and
   `pandas_2` cell `ccf796ec`, both `ValueError`. A demo that goes quiet leaves the paragraph above
   it describing something the reader will never see.
7. **Reshapes go to an agent, renames may go to regex.** `.loc`/`.iloc`, `groupby().filter()`,
   `pivot_table`, `set_index`, and dict-agg-with-lists are all reshapes.
8. **`sort` sense is inverted** — pandas `ascending=True` ↔ Polars `descending=False` — **and Polars
   sorts nulls first.** Any `.head()` after a sort on a nullable column silently gains a null row.
9. **Never edit `content/*/data/**`, `content/*/images/**`, `.github/**`, `assets/**`, or
   `content/eda/ds100_utils.py`.** `myst.yml` and `requirements.txt` change only with an allowlist
   entry. The repo-invariants gate enforces all of this.
10. **Never edit `conversion/.baseline/**`** — it is the diff baseline, regenerated from git.
    Edit `conversion/pytext/polars/**`.

## Convert a chapter

```bash
export PATH="/Users/jedwin321/miniforge3/envs/d100/bin:$PATH"

python conversion/nb_baseline.py --chapter <ch>          # materialize the pinned baseline
# dispatch notes-converter (tier B/C) or chapter-author (tier D) on conversion/pytext/polars/<ch>/

python conversion/nb_pytext.py to-ipynb \
    --input  conversion/pytext/polars/<ch>/<file>.py \
    --output content/<ch>/<file>.ipynb \
    --outputs-from conversion/.baseline/<sha>/content/<ch>/<file>.ipynb

python conversion/nb_execute.py --chapter <ch>           # full re-execution; serial only
python conversion/nb_validate.py --chapter <ch>          # gate battery G1-G13
# dispatch reviewers per tier, then once per batch:
python conversion/site_gate.py                           # G14 + G15
```

**Execution is serial.** One kernel per notebook, Polars uses all cores, and several chapters read
20–150 MB. Run them ordered by data size ascending so failures surface in the first minute.
Converters and reviewers may run in parallel; execution may not.

## Before every batch

```bash
python conversion/nb_validate.py --all --self-test
```

The negative control. It runs the battery against the pandas baseline and asserts the removal gates
fail while the structural gates stay quiet. Ten seconds, and it catches the entire class of bug where
a scanner silently matches nothing — which has already happened twice in this harness: the self-test
probe missed `class=\"dataframe\"` escaped inside notebook JSON, and the site gate missed the same
string escaped inside MyST's page JSON.

## Where things live

| Path | What |
|---|---|
| `AGENTS.md` | this file — versions, rules, commands |
| `CONVERSIONS.md` | per-chapter record and open questions for course staff |
| `.claude/skills/` | the conversion conventions |
| `.claude/agents/` | the writer and reviewer contracts |
| `conversion/` | the toolchain, the gates, the allowlist, and `state.json` |
| `README.md` | the site build, for course staff who are not converting anything |

## Which prose skill to reach for

Three overlap and are not interchangeable:

- **`data100-textbook-voice`** — does this read like *this book*? Chapter skeleton, admonitions, the
  dropdown pattern. Load before writing any student-facing text.
- **`no-ai-slop`** — does this read like a person wrote it? An editor persona with a pass/fail
  `eval.md`. Load when a draft feels generic, or to check whether writing reads as AI.
- **`humanizer`** — a pattern catalogue from Wikipedia's "Signs of AI writing". Use to *name* a
  specific tell; `no-ai-slop` is the one that edits.

`pandas-to-polars` carries the **NumPy dispatch rule**, which decides every `.to_numpy()` boundary.
It was reconciled against the sister repo's corpus-wide cleanup: matplotlib, plotly, scipy and
sklearn take Polars directly, and the conversions that added `.to_numpy()` there were churn.


## Orchestration — the waves

Conversion runs in waves. The ordering is not a style preference; two of the constraints are hard.

| Wave | What | Parallel? |
|---|---|---|
| 0 | `nb_baseline` · `nb_triage` · **`nb_validate --all --self-test`** | serial, cheap |
| 1 | `notes-converter` / `chapter-author` per chapter; `tab_twins --from-baseline` needs no agent | yes, cap ~6 |
| 2 | `nb_execute` per chapter | **NO — strictly serial** |
| 3 | `nb_validate` per chapter | yes |
| 4 | reviewer fan-out, per tier | yes, across chapters *and* reviewers |
| 5 | one refuter per blocking finding | yes |
| 6 | fix list back to the converter, re-enter at wave 2 | — |

**The negative control runs first, every time.** A battery that passes on the pandas baseline is
broken, and every result after it is meaningless.

**Wave 2 must not be parallelised.** One kernel at a time: Polars takes all cores and several
chapters read 20–150 MB. Order by data size ascending so failures surface in the first minute.

**A chapter that fails wave 3 never reaches wave 4.** Reviewer attention is the expensive resource;
mechanical defects must never consume it.

### Who reviews what

| Tier | Reviewers |
|---|---|
| A | none — the predicate is an empty diff, and any change is the defect |
| B | `notes-output-reviewer` + `notes-claim-verifier` + `notes-render-reviewer` |
| C | + `notes-prose-reviewer` |
| D | + `notes-prose-reviewer` + human sign-off |

`notes-a11y-reviewer` joins wherever figure outputs moved — under full re-execution, most chapters
with figures.

### Wave 5, and why it exists

Every **blocking** finding goes to an independent agent told to *refute* it; the finding survives
only if refutation fails. This is not ceremony. Reviewers on this project reported a BLAS attribution
that was environmental drift, a "pixel-identical" claim that differed in 1.4% of pixels, and "two win
rates moved" that was three — each caught only because something re-derived it. A converter sent
chasing a finding that was never true burns an attempt against the floor.

Refuting is also how the *real* defect gets found. A render review reported all 28 of `eda`'s
comparison tabs as duplicating their code cell; checking it showed mystmd 1.6.6 records
`remove-input`/`remove-output` on a block's **code and output children**, leaving the block itself
`visibility: "show"` — so 23 were correctly hidden and 5 were not, and those 5 were a real bug in a
different place. The finding was wrong, the instinct behind it was right, and only re-deriving it
separated the two.

### The floor

Three attempts per chapter. `debt` must fall strictly between them. An identical failure fingerprint
twice running bails. Three consecutive `NEEDS_HUMAN_REVIEW` halts the batch — that pattern means the
problem is systemic, not chapter-specific.

### What each layer can and cannot see

Worth keeping in view when deciding whether a layer is missing:

- **Gates** read files. They cannot see meaning, and they cannot see the rendered page.
- **The executor** refuses to write a notebook that lost an error demo. It cannot see anything that
  executes cleanly.
- **Reviewers** read the notebook and its outputs. Until `notes-claim-verifier` they never executed a
  *sentence*, and until `notes-render-reviewer` nobody opened the built artifact.

All three defects that reached course staff — a chapter's title silently unrendering, a comment
whose own output disproved it, and tab density — lived in one of those blind spots.

## The gates are migration-time only

`.github/workflows/conversion-gates.yml` was removed when the conversion finished. It existed only on
this branch, never on `main`, and deleting it restored `.github/` to its baseline state.

The reason is structural rather than convenience: **every gate in `nb_validate.py` diffs a chapter
against a pinned pre-conversion commit.** Once this branch merges, that comparison is frozen history
— each chapter differs from `887a578b` permanently and by design — so the battery would report the
same diffs forever and guard nothing. It is an instrument for performing a migration, not for
maintaining one.

Run it locally while the conversion is live:

```bash
python conversion/nb_validate.py --all --self-test   # negative control, first
python conversion/nb_validate.py --all
python conversion/site_gate.py
```

`deploy.yml` and `a11y.yml` are untouched and stay: the a11y workflow runs on every PR and is the
durable accessibility check, which matters more here than usual because several chapters carry alt
text that quotes computed values.

**If ongoing protection is ever wanted, the one check worth lifting out is `site_gate.py`'s
"0 pandas reprs reach the reader".** That claim is absolute rather than relative to a baseline, so
unlike the rest of the battery it would keep its meaning after the merge.
