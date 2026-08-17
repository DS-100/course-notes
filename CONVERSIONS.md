# Conversion log — pandas → Polars

Status of every chapter in the Data 100 course notes, and what changed in each conversion. **This is
the orchestrator's state file in prose and the record for course staff.**

Refresh the measurements with `python conversion/nb_triage.py`; check a chapter with
`python conversion/nb_validate.py --chapter <ch>`. The machine-readable queue is
`conversion/state.json` — this file is the part a human reads.

## Conventions

**Tier** routes who writes and how much review the result gets:

| Tier | Meaning | Writer | Reviewers |
|---|---|---|---|
| **A** | no pandas at all — the predicate is an *empty diff*, and any change fails | none | none |
| **B** | ordinary translation | `notes-converter` | `notes-output-reviewer` |
| **C** | heavy translation | `notes-converter` | + `notes-prose-reviewer` |
| **D** | the chapter is *about* pandas; it gets rewritten | `chapter-author` | + human sign-off |

`notes-a11y-reviewer` is added to any chapter whose figure outputs changed, which under full
re-execution is most chapters that have figures.

**State:** `PENDING → BASELINED → CONVERTING → BUILT → EXECUTED → GATED → REVIEWED → DONE`, or
`NEEDS_HUMAN_REVIEW` when the loop exits without clearing the bar, or `BLOCKED_UPSTREAM` when
something outside the conversion prevents progress. Nothing ships below the bar silently.

**Gate** is all of `nb_validate.py`'s G1–G13 green (G8 is advisory), plus `site_gate.py`'s G14 and
G15 green for the batch.

**The loop has a floor.** Three attempts maximum; a `debt` score that fails to decrease strictly
between attempts bails immediately; an identical failure fingerprint twice in a row bails. Three
consecutive chapters reaching `NEEDS_HUMAN_REVIEW` halts the batch, because that pattern means
something systemic rather than something chapter-specific.

## Global decisions

- **Full re-execution.** Every output is regenerated so it provably came from Polars. The cost is
  churn — 77 PNG blobs, 41 plotly blobs, and everything downstream of 44 randomness sites against
  only 10 seeds move on every run. Gate G8 reports which outputs moved without their source moving so
  reviewers can skip them; it does not block.
- **`.to_pandas()` only where Polars genuinely cannot go in directly**, each site allowlisted with a
  reason. seaborn's `data=` handoff is the expected case.
- **`pandas_1/2/3` become `polars_1/2/3`**, moved with `git mv` so history follows and the 146 MB of
  data under `pandas_2/` is not duplicated. The TOC entries move in the same commit.
- **Archived `_`-prefixed chapters are in scope.** They are absent from the TOC so the site gates
  cannot see them, but no pandas should survive anywhere under `content/`.
- **`content/sql_II/data/imdb_duck.db` is gitignored and absent**, so `sql_II` cannot be executed
  locally.

## Status

Measured from the baseline pinned in `conversion/baseline.lock` (`887a578b`). `code` and `mirror`
are pandas sites in code cells and in fenced blocks inside markdown; `out` is code cells carrying a
committed pandas dataframe repr; `dens` is pandas API references per line of prose.

| Chapter | Tier | code | mirror | reshape | out | dens | State |
|---|---|---|---|---|---|---|---|
| index | A | 0 | 0 | 0 | 0 | 0.000 | PENDING |
| case_study_HCE | A | 0 | 0 | 0 | 0 | 0.000 | PENDING |
| clustering | A | 0 | 0 | 0 | 0 | 0.000 | PENDING |
| probability_1 | A | 0 | 0 | 0 | 0 | 0.000 | PENDING |
| probability_2 | A | 0 | 0 | 0 | 0 | 0.000 | PENDING |
| sql_I | A | 0 | 0 | 0 | 0 | 0.062 | PENDING |
| visualization_1 | B | 9 | 7 | 4 | 3 | 0.020 | PENDING |
| inference_causality | B | 7 | 8 | 0 | 4 | 0.017 | PENDING |
| visualization_2 | B | 6 | 5 | 0 | 1 | 0.013 | PENDING |
| constant_model_loss_transformations | B | 6 | 4 | 4 | 0 | 0.002 | PENDING |
| gradient_descent | B | 7 | 3 | 0 | 4 | 0.013 | PENDING |
| feature_engineering | B | 6 | 3 | 0 | 3 | 0.002 | PENDING |
| regex | B | 5 | 3 | 0 | 6 | 0.109 | PENDING |
| logistic_regression_1 | B | 5 | 2 | 0 | 1 | 0.006 | PENDING |
| modeling_slr | B | 6 | 1 | 0 | 0 | 0.009 | PENDING |
| sampling | B | 6 | 0 | 3 | 5 | 0.006 | PENDING |
| cv_regularization | B | 3 | 2 | 0 | 2 | 0.008 | PENDING |
| intro_lec | B | 4 | 0 | 0 | 0 | 0.188 | PENDING |
| logistic_regression_2 | B | 2 | 2 | 0 | 1 | 0.003 | PENDING |
| _pca_1 | B | 2 | 1 | 0 | 1 | 0.000 | PENDING |
| _decision_tree | B | 2 | 0 | 0 | 3 | 0.003 | PENDING |
| ols | B | 2 | 0 | 0 | 2 | 0.007 | PENDING |
| sql_II | B | 0 | 2 | 0 | 0 | 0.046 | PENDING |
| _case_study_climate | B | 0 | 1 | 0 | 0 | 0.006 | PENDING |
| pca | C | 32 | 28 | 7 | 10 | 0.016 | PENDING |
| _pca_2 | C | 30 | 21 | 7 | 9 | 0.016 | PENDING |
| eda | C | 22 | 1 | 0 | 21 | 0.097 | PENDING |
| pandas_3 → polars_3 | D | 45 | 16 | 8 | 33 | 0.608 | PENDING |
| pandas_1 → polars_1 | D | 36 | 0 | 20 | 23 | 0.738 | PENDING |
| pandas_2 → polars_2 | D | 22 | 7 | 8 | 25 | 0.440 | PENDING |

30 chapters: 6 verify-only, 18 translate, 3 heavy, 3 authored.

### Notes on the table

- **`sql_II` and `_case_study_climate` have zero pandas in code and still land in tier B.** Their
  pandas lives entirely inside fenced code blocks in markdown, where no code-cell scanner looks.
  Between them and the other 12 affected chapters, 88 pandas sites repo-wide are prose-only.
- **`intro_lec` sits at density 0.188, just under the 0.20 tier-D threshold.** It names pandas as an
  ecosystem tool rather than teaching it, so translating is correct — but it is flagged
  `prose_note: ecosystem_mentions` in `state.json` and gets the prose reviewer regardless of tier.
- **`_pca_2` duplicates the live `pca` chapter** — identical data directory, near-identical content,
  and it is not in the TOC. Convert `pca` first and check whether `_pca_2` should simply be deleted
  rather than converted. That is a question for course staff, recorded below.

# Per-chapter records

*None yet — the harness is built, no content has been converted.*

Each record, once written, carries: **Code changes** → **Accepted behaviour differences** →
**Constants changed** (a `| Where | Old | New | Why |` table, all regenerated by executing the Polars
code, never reasoned out) → **Prose re-authored** → **Defects found and fixed during conversion** →
**Review** (output reviewer BLOCK/PASS, prose score) → **Open items**.

# Harness build notes

Recorded because both were vacuous-pass bugs caught by building the negative control first, and both
are the kind that stay green forever once shipped.

1. **The self-test's own probe was blind.** It checked for a stale pandas repr by searching the
   baseline `.ipynb` for `class="dataframe"`. Inside notebook JSON that string is stored escaped as
   `class=\"dataframe\"`, so the probe found nothing and `outputs-fresh` was never exercised on any
   chapter. Fixed by probing the parsed notebook. The gate itself was correct throughout — it was the
   test of the gate that was broken, which is the harder version to notice.
2. **The site gate was looking in the wrong files.** Jupyter Book v2 does not emit pre-rendered page
   HTML; `_build/html/<slug>.json` carries the content and the `.html` files are a React shell. The
   gate searched `.html` for the unescaped repr and scored a site carrying **294** of them as zero.
   Fixed with an escape-tolerant pattern, and the baseline capture now records the pandas counts it
   found so a detector that finds nothing is reported as broken rather than passing.

The general rule both incidents support: **a detector that reports zero is only good news if it found
something on the baseline.** Every removal gate in this harness is paired with that check.

# Open questions for course staff

1. **`content/_pca_2/` duplicates `content/pca/`** — same 31 MB data directory, same
   `iframe_figures/figure_45.html`, near-identical content, not in the TOC. Should it be deleted
   rather than converted?
2. **The `pandas_1/2/3` concept diagrams.** `images/gb.png`, `agg.png`, `pivot.png`, and the `.loc`
   graphic draw pandas semantics — index alignment, the GroupBy object, hierarchical pivot columns.
   No agent can redraw them. Which are still accurate for Polars, which need redrawing, and which
   should go?
3. **Renaming `pandas_1/2/3` changes their published URLs** (`/pandas-1` → `/polars-1`). Does anything
   outside this repo link to them — a syllabus, a Piazza post, an assignment?
4. **`content/eda/ds100_utils.py` is dead** — it defines `fetch_and_cache` and `head`, and no
   notebook imports it. The two chapters that cache downloads define the function inline instead.
   Delete it, or reconnect the inline copies to it?
5. **`content/pandas_3/babynamesbystate.zip` sits outside `data/`** — a 22 MB duplicate of
   `content/pandas_3/data/babynamesbystate.zip`. Safe to delete?
6. **`content/sql_II/data/imdb_duck.db` is gitignored and absent**, so `sql_II` cannot be executed
   locally. It has no pandas in its code cells, so the conversion does not need to run it — but no
   one can verify its outputs either. Is that acceptable, or should the file be made available?
7. **44 randomness sites are covered by only 10 `seed()` calls.** Under full re-execution the
   unseeded ones produce different numbers on every build, and any prose quoting them goes stale
   silently. Should the conversion add seeds, or is the churn acceptable?
