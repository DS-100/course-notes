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
| index | A | 0 | 0 | 0 | 0 | 0.000 | DONE |
| case_study_HCE | A | 0 | 0 | 0 | 0 | 0.000 | DONE |
| clustering | A | 0 | 0 | 0 | 0 | 0.000 | DONE |
| probability_1 | A | 0 | 0 | 0 | 0 | 0.000 | DONE |
| probability_2 | A | 0 | 0 | 0 | 0 | 0.000 | DONE |
| sql_I | A | 0 | 0 | 0 | 0 | 0.062 | DONE |
| sql_II | A | 0 | 0 | 0 | 0 | 0.046 | DONE |
| _case_study_climate | A | 0 | 0 | 0 | 0 | 0.006 | DONE |
| visualization_1 | B | 9 | 7 | 4 | 3 | 0.020 | PENDING |
| visualization_2 | B | 6 | 5 | 0 | 1 | 0.013 | PENDING |
| constant_model_loss_transformations | B | 6 | 4 | 4 | 0 | 0.002 | DONE |
| gradient_descent | B | 7 | 3 | 0 | 4 | 0.013 | DONE |
| feature_engineering | B | 6 | 3 | 0 | 3 | 0.002 | DONE |
| modeling_slr | B | 6 | 5 | 0 | 0 | 0.009 | DONE |
| regex | B | 5 | 3 | 0 | 6 | 0.109 | DONE |
| logistic_regression_1 | B | 5 | 2 | 0 | 1 | 0.006 | PENDING |
| inference_causality | B | 7 | 2 | 0 | 4 | 0.017 | PENDING |
| sampling | B | 6 | 0 | 3 | 5 | 0.006 | PENDING |
| cv_regularization | B | 3 | 2 | 0 | 2 | 0.008 | DONE |
| intro_lec | B | 4 | 0 | 0 | 0 | 0.188 | DONE |
| logistic_regression_2 | B | 2 | 2 | 0 | 1 | 0.003 | DONE |
| _pca_1 | B | 2 | 1 | 0 | 1 | 0.000 | DONE |
| _decision_tree | B | 2 | 0 | 0 | 3 | 0.003 | DONE |
| ols | B | 2 | 0 | 0 | 2 | 0.007 | PENDING |
| pca | C | 32 | 26 | 7 | 10 | 0.016 | DONE |
| eda | C | 22 | 2 | 0 | 21 | 0.097 | DONE |
| _pca_2 | C | 30 | 21 | 7 | 9 | 0.016 | GATED |
| pandas_2 **+ pandas_1** → polars_1 | D | 22 + 36 | 7 | 8 + 20 | 25 + 23 | 0.440 | REVIEWED |
| pandas_3 → polars_2 | D | 45 | 10 | 8 | 33 | 0.608 | REVIEWED |
| pandas_1 (absorbed) | D | 36 | 0 | 20 | 23 | 0.738 | RETAINED |

30 chapters: **8 verify-only, 16 translate, 3 heavy, 3 authored** — re-measured after the fence
detector was fixed (harness build note 4), which moved `sql_II` and `_case_study_climate` into
verify-only and corrected the mirror counts on six other chapters. The baseline carries 105 mirror
sites.

**The conversion is complete: 29 chapters `DONE`, 1 `RETAINED`.** Tier D was cut from three chapters
to two: `pandas_2` + `pandas_1` → `polars_1` ("Polars I"), `pandas_3` → `polars_2` ("Polars II").

**The site serves zero pandas.** `site_gate.py` reports **0 dataframe reprs and 0 doc links reach the
reader, against a baseline of 146 and 150** — G15 green.

**`content/pandas_1/` was deleted** once its material had been carried into `polars_1`. Checked
before deleting rather than after: its `elections.csv` is byte-identical to
`content/polars_2/data/elections.csv` (md5 `47b93a15`), and of its eight images the only filename
shared with a surviving chapter is `df_elections.png`, of which `intro_lec` holds its own copy. The
other seven are Index/`.loc` diagrams that die with the concept. Recoverable from git at `4f842ef7`.

**29 chapters, all `DONE`.** The two authored chapters still fail `structure` because their cell ids
are new, which cascades every id-aligned gate to INCONCLUSIVE by design — that is what tier-D human
sign-off replaces, and course staff have accepted the cell-id churn.

### One thing the deletion surfaced, still open

**`polars_1` and `polars_2` teach the same named dataset with different contents.** There were three
copies of `elections.csv` in the tree and they were not all the same file:

| Copy | Rows | Through | md5 |
|---|---|---|---|
| `pandas_1` (deleted) | 187 | 2024 | `47b93a15` |
| `polars_2` | 187 | 2024 | `47b93a15` |
| **`polars_1`** | **182** | **2020** | `c1cc9083` |

`polars_1`'s front half was written from `pandas_1`'s material, which taught against the 187-row file
— but the merged chapter lives in the directory that came from `pandas_2` and so executes against
the 182-row one. The chapter is internally consistent (its prose says "182 rows and 6 columns", and
every constant was verified against what it actually reads), but **Polars I now stops at 2020 while
Polars II covers 2024**, and the material that moved lost the 2024 election in transit.

This predates the merge — `pandas_1` and `pandas_2` always carried different files — but the merge
is what made it a contradiction between adjacent chapters rather than a quirk of two separate ones.

Fixing it means copying `polars_2`'s file into `polars_1`, re-executing, and updating every constant
the reviewer verified against the 182-row data (182 → 187, the 60M-vote count, the OR-filter row
count, Johnson's position, and others). That is a re-review, not an edit, so it is recorded here for
course staff rather than done unilaterally.

Course staff set the priority rule partway through: **what ships in `myst.yml`'s TOC comes first,
along with anything a shipping notebook depends on.** The dependent-file half was checked and is
empty — `content/eda/ds100_utils.py` is the only `.py` under `content/`, it carries no pandas, and
nothing imports it. That check mattered more than it looked: the gate battery walks chapters, not the
import graph, so a shipping notebook importing a pandas-carrying helper would leave pandas in the
published book with all 15 gates green.

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

## Tier A — index, case_study_HCE, clustering, probability_1, probability_2, sql_I

All six `DONE`, no edits. The predicate for a chapter with no pandas is an *empty diff*, so the work
is asserting that nothing changed rather than changing anything:

```bash
python conversion/nb_validate.py --chapter index --chapter case_study_HCE \
    --chapter clustering --chapter probability_1 --chapter probability_2 --chapter sql_I
```

Six `unchanged` PASSes, `debt=0`. Worth noting that the routing is derived rather than configured:
`nb_validate.baseline_has_pandas()` reads the baseline and picks the predicate itself, so a chapter
cannot be sent down the wrong path by a stale tier in `state.json`. `sql_I` is pure `%%sql`/jupysql;
the other five carry no executable code at all.

Each record carries: **Code changes** → **Accepted behaviour differences** → **Constants changed**
(a `| Where | Old | New | Why |` table, all regenerated by executing the Polars code, never reasoned
out) → **Prose re-authored** → **Defects found and fixed during conversion** → **Review** (output
reviewer BLOCK/PASS, prose score) → **Open items**.

## _pca_1 — PCA I (archived)

Tier B, `DONE`. 3 lines changed, 1 attempt, debt 0. All 13 gates green.

### Code changes

- `import pandas as pd` → `import polars as pl`. The `pd` name was **dead** — it appeared once and
  was never used — so this is a dead import removed and a needed one added. `np` and `sp` are also
  dead here; left alone, since pruning non-pandas imports is a content decision.
- **The site no `pd.` scan can find:** `sns.load_dataset("mpg")` returns a *pandas* DataFrame, so the
  chapter carried pandas with no pandas token in it. Now
  `pl.from_pandas(sns.load_dataset("mpg")).drop_nulls()`, applied as a single edit spanning both the
  code cell (`31f16bc4`) and its dropdown mirror (`fdf19f0b`) so the two could not drift apart.

### Accepted behaviour differences

- `mpg.head()` renders the Polars `shape: (5, 9)` header and a dtype row, with no index column. No
  prose describes the index — verified by grep for `index`, row counts, `.loc`, "the table above".

### Constants changed

None. The row count is **398 → 392**, identical to pandas `.dropna()`: `pl.from_pandas` defaults to
`nan_to_null=True`, so the 6 NaN `horsepower` values arrive as nulls and `drop_nulls()` removes
exactly those rows. Had that default gone the other way the frame would have silently kept all 398.
The quoted figures 402.56 and 389.52 describe a static PNG, not computed output — and the adjacent
sentence names `np.var`, which is correct to leave alone: swapping it for Polars `.var()` flips ddof
0 → 1 and would move the quoted totals.

### Review

`notes-output-reviewer`: **PASS**. It base64-decoded the `bdata` arrays of every trace in all five
plotly figures and found them numerically equal to the baseline's, 392 points each, with the
`usa`/`japan`/`europe` split intact at 245/79/68. The only layout differences are JSON int-vs-float
serialization (`[0, 1]` → `[0.0, 1.0]`), which is churn. All five plotly calls take the Polars frame
directly — no `.to_pandas()`, nothing allowlisted.

### Open items

- 19 of 20 `{image}` directives have no `:alt:`, and the chapter carries a standing note that alt text
  must be added before publication. Pre-existing, and presumably why it is outside the TOC.

## logistic_regression_2 — Logistic Regression II

Tier B, `DONE`. 7 lines across 3 mirrored pairs, 1 attempt, debt 0. All 13 gates green.

### Code changes

- `import pandas as pd` → `import polars as pl`, `pd.DataFrame` → `pl.DataFrame`, each with its
  dropdown mirror in the same pass.
- Two `np.mean(...)` calls became `(...).mean()`. **Required, not stylistic:** `np.mean` on a Polars
  Series raises `TypeError: Series.mean() got an unexpected keyword argument 'axis'`.

### Accepted behaviour differences

- **The `x` literal is now written as floats** — `[-4.0, -2.0, -0.5, 1.0, 3.0, 5.0]`. Polars types the
  column `Int64` from the first element under strict inference and then rejects `-0.5`; pandas
  silently inferred `float64`. This makes explicit what pandas inferred, and stores the same values
  the baseline's committed output already showed. Not pandas-matching.
- `toy_df.head()` gains the `shape: (5, 2)` header and dtype row. Nothing in the prose narrates the
  table's shape or index — checked by grep.

### Constants changed

None, and that is a measured result rather than an assumption: both 100-point loss surfaces were
recomputed under pandas and Polars. MSE and mean cross-entropy are **bit-identical**, `inf` positions
included, with argmin unmoved at θ = 0.7576. So "nothing like the parabola", "a global minimum and a
(barely perceptible) local minimum", and "our loss function is now convex" all still describe what is
drawn.

### Prose re-authored

One illustrative snippet that never executes: `np.mean(model.predict(X) == Y)` → `... == Y.to_numpy()`.
Without it the snippet is a lie — `predict` returns an ndarray, and ndarray-vs-Polars-Series
comparison raises in *both* directions. A student copying the baseline line into a Polars notebook
hits a wall the page gave them no way to anticipate, and no gate can catch it because the block
never runs.

### Review

`notes-output-reviewer`: **PASS**, having rendered both PNG pairs and compared them visually as well
as numerically. Zero `.to_pandas()`, zero `pl.Config` calls — nothing forced to look like pandas.

### Open items

- Pre-existing baseline warts, noted so they are not mistaken for conversion damage: cell `50b345fc`'s
  dropdown mirror carries one blank line the code cell lacks, and the accuracy snippet declares
  `def accuracy(X, Y)` then calls `model.score(X, y)` with a lowercase `y`.

## _case_study_climate — Case Study in Climate and Physical Data (archived)

**Tier A on the corrected triage**, `DONE`. Two prose lines changed. All four applicable gates green.

This chapter is the reason harness build note 4 exists. Triage reported "1 pandas site in a fenced
code block"; **both halves were false.** The site is not in a fenced block — the fence detector was
pairing `{image}` closers and scanning the prose between them — and it is not pandas. It is
`xarray`'s `groupby`, and the reviewer confirmed that independently two ways: the argument
`"time.month"` is xarray's virtual-variable syntax, on which pandas raises `KeyError`; and the next
line does `weighted_mean.groupby("time.month") - annual_cycle`, a GroupBy binary broadcast that
pandas does not implement at all. All six code-bearing slide images are xarray, NumPy, and
matplotlib. There is no pandas in this chapter.

### Prose re-authored

`.groupby()` → ``Xarray's `.groupby()` ``, and `` `.weighted()` ``/`` `.mean()` `` backticked to match.
With the detector fixed no gate requires this, and it was kept deliberately: in a course that now
teaches Polars, a bare unattributed `.groupby()` is exactly the token a student reads as "the
DataFrame method I just learned" — except Polars spells it `group_by`. Naming the library removes an
ambiguity **the conversion itself introduced**, which is prose moving to match the content.

### Review

`notes-output-reviewer`: **PASS**. No outputs exist to compare; all 14 figures are frozen PNGs, and
git confirms only the `.md` moved.

### Open items

- Pre-existing typos left alone rather than swept into a conversion diff: "Xarrry" (L145), "Locatoin"
  in a heading (L166), "IPOC" for IPCC (L57), and two malformed learning outcomes (L7–8).

## modeling_slr — Simple Linear Regression

Tier B, `DONE`. 1 attempt, debt 0. All 13 gates green. **Every committed output is byte-identical to
the baseline** — the strongest evidence of a clean conversion available, and the reason to be careful
about "improving" anything here.

### Code changes

- Both `import pandas as pd` statements (cells `18ffe9c6`, `b6d427ac`) → `import polars as pl`.
- Anscombe's quartet: `pd.DataFrame(list(zip(x, y1)), columns=["x", "y"])` → `pl.DataFrame({"x": x,
  "y": y1})`. The `list(zip(...))` existed only to feed pandas' row-oriented constructor.
- **Five NumPy handoffs** — the real hazard, invisible to a `pd.` grep. The chapter's stats helpers
  are pure NumPy, and `np.mean`/`np.std` on a Polars Series raise
  `TypeError: Series.mean() got an unexpected keyword argument 'axis'`. Each column crosses at the
  call site with `.to_numpy()`.

### Accepted behaviour differences

None. No frame is ever displayed, so no shape or dtype header enters the page.

### Constants changed

**None, and preserving that took a deliberate choice.** The helpers were *not* rewritten to native
Polars methods, because `np.std` is ddof=0 — which is what these population-statistics formulas
require and what the chapter's own displayed math defines — while `Series.std()` defaults to ddof=1.
The reviewer computed the counterfactual:

| | shipped | had the helpers gone native |
|---|---|---|
| x_stdev | 3.16 | 3.32 |
| y_stdev | 1.94 | 2.03 |
| r | 0.816 | 0.742 |
| θ₀, θ₁ | 3.00, 0.50 | 3.41, 0.45 |
| RMSE | 1.119 | 1.128 |

θ₀ = 3, θ₁ = 0.5 are the canonical Anscombe values. Going native would have silently contradicted the
chapter's own formulas while every gate stayed green.

### Prose re-authored

None needed. The chapter names no pandas method and all five doc links are Wikipedia or Data 8.

### Review

`notes-output-reviewer`: **PASS**, having md5-matched the stream output and pixel-compared all four
figures.

### Open items

All pre-existing, none conversion-caused, all for course staff:

- Cell `6f72a412`'s dropdown has a closing ` ``` ` with no opener, so **MyST renders the helper source
  as markdown** — headings, stripped indentation, smart quotes on `plt.style.use("default")`.
  Confirmed in the built AST, not inferred. A live rendering defect on the published page.
- Cell `06d9c0af` says the four datasets have "identical" r and RMSE against output showing
  0.816/0.817 and 1.119/1.118. Fixing it by changing print precision would destroy the byte-identity
  that is currently the best evidence this chapter converted cleanly — so it should be a prose edit
  if anything.
- `#| fig-alt` typo "roughlu" in cell `18ffe9c6`.

### Defects found and fixed during conversion

**A tab escape was corrupting the published output.** Cell `ce691b4e` printed
`f"\theta_0: {ahat:.2f}, \theta_1: {bhat:.2f}"`, where `\t` is Python's tab escape — so the page
showed a tab followed by `heta_0`, not `\theta_0`. The cell has no `remove-input`, so every reader
saw it. The sibling lines in the same function print plain labels (`x_mean`, `y_stdev`, `RMSE`),
which is what makes the intent unambiguous: it was meant to read `theta_0`. Fixed in the code cell
and its dropdown mirror in one substitution, and the regenerated output now reads
`theta_0: 3.00, theta_1: 0.50` — the canonical Anscombe values, so the fix is visible and the
conversion's byte-identity elsewhere is undisturbed.

## feature_engineering — Feature Engineering

Tier B, `DONE`. 1 attempt, debt 0. All 13 gates green.

### Code changes

- `sns.load_dataset("mpg")` → `pl.from_pandas(...)` then `.drop_nulls().rename({"horsepower": "hp"})
  .sort("hp")`. `drop_nulls()` runs **before** the sort, so Polars' nulls-first ordering never
  applies — verified, 0 nulls and 0 NaNs reach `sort`, 392 rows out.
- `pd.options.mode.chained_assignment = None` **deleted, not translated.** It silenced pandas'
  `SettingWithCopyWarning` from a slice assignment that is now `with_columns`, so it had nothing left
  to suppress. No prose referenced it.
- A pandas **index** join → `tips.select(["total_bill", "size"]).hstack(encoded_day_df)`, dropping the
  baseline's select-then-drop detour. Verified bit-identical: shape `(244, 6)`, column order matching
  the θ₁…θ₆ ordering in the prose, 0 misaligned OHE rows of 244.
- Three `np.mean(...)` → `(...).mean()`; `.to_numpy()` at the matplotlib boundary.

### Constants changed

| Where | Old | New | Why |
|---|---|---|---|
| `#| fig-alt`, cell `edc98ac8` | 23.943662938603104 | 23.943662938603108 | **Interpreter drift, not Polars** |
| `#| fig-alt`, cell `21180eea` | 18.98476890761722 | 18.984768907617216 | same |

Recorded precisely because it is easy to misattribute: the reviewer ran the **baseline pandas code**
in this env and got `...603108` too. The move is Python 3.11.13 → 3.11.15, not the conversion. The
alt-text edit was still required — alt text must agree with the committed output — and both strings
were verified digit-for-digit against the regenerated stream by two reviewers.

### Review

`notes-output-reviewer`: **PASS** (base64-decoded the plotly payloads; `z` differs by max 1.07e-14,
markers bit-identical). `notes-a11y-reviewer`: **PASS** on all 24 figure surfaces.

### Open items

- Pre-existing: cell `18c377cc` says "a high (poor) value of **RMSE**" while the cell prints MSE.
- The two `#| fig-alt` strings quote 17-significant-digit floats, which couples alt text to the
  interpreter version. A rounded, descriptive alt ("MSE ≈ 23.94") would be better alt text *and*
  stable. Pre-existing pattern, worth a pass across the book.

## constant_model_loss_transformations — Constant Model, Loss, and Transformations

Tier B, `DONE`. 1 attempt, debt 0. All 13 gates green. The only chapter in the batch with reshape
sites.

### Code changes

- Four `.iloc[:, n]` → `to_series(n).to_numpy()`. `to_series(i)` and `df[:, i]` are indistinguishable
  here (`.equals()` True), so the choice was made downstream: `np.std`/`np.mean` consume these, and
  both raise on a Polars Series.
- `np.mean(data_constant)` → `data_constant.mean()`; two `dugongs[col]` → `.to_numpy()`.
- `sns.rugplot(yobs, ...)` → `sns.rugplot(x=yobs, ...)`.

### Accepted behaviour differences

- **The rugplot keyword is chart content, not pandas-matching.** Verified on the pin: passing
  positionally gives `xlabel=''` with a Polars Series but `xlabel='Age'` with a pandas one — seaborn's
  positional slot is `data=`, and only pandas gets wide-form name inference. The plot would have
  silently lost its axis label with nothing failing. `x=`/`y=` is already the chapter's own idiom.

### Constants changed

None — all 14 numeric outputs are **bit-identical**, verified as IEEE-754 hex, including the 80×80
loss grid (sum `4167d3183a91b3e8`).

Worth recording: the native path was tried first and produced a **1-ulp** difference. `std_y/std_x`
cancels ddof exactly, but the cell is written `corr * std_y / std_x`, so the intermediate rounds
differently under ddof=1. The ddof trap surfacing as rounding rather than as a visibly wrong number.

### Correction to the converter's report

The converter reported the four figures as "pixel-identical". **They are not.** Raster dimensions
moved (448×608 → 453×610) and same-shape pairs differ in ~1.4% of pixels — but so do three cells
whose source never changed, which is the tell: matplotlib/font rendering drift between baseline
capture and re-execution. Content is unmoved: same series, axes, scales, markers, colorbar range.
Recorded so the next reviewer is not primed to hunt a defect that is not there.

### Review

`notes-output-reviewer`: **PASS**. `notes-a11y-reviewer`: **PASS** on all 14 `#| fig-alt` and 6
`{image}`, with the `error.png` and `outliers.png` numeric claims re-derived from the cells.

## gradient_descent — Gradient Descent

Tier B, `DONE`. 1 attempt, debt 0. All 13 gates green. 16 asserted substitutions applied atomically.

### Code changes

- `pd.options.mode.chained_assignment = None` deleted; `sns.load_dataset("penguins")` wrapped in
  `pl.from_pandas`, then `.filter(pl.col("species") == "Adelie").drop_nulls()`.
- `penguins["bias"] = np.ones(...)` → `with_columns(pl.Series("bias", np.ones(...)))`.
- Two `np.mean(...)` reductions moved onto the expression — required; they raise on a Series.

### Accepted behaviour differences

- `pl.DataFrame(Y_hat).head()` labels its column **`column_0`** where pandas gave `0`. No prose names
  it — confirmed by repo-wide grep — so no `.rename()` was added to force the pandas label back.

### Constants changed

None. `theta_hat`, both MSEs, and the trajectory endpoint all reproduce bit-identically. That last
one matters most: the `#| fig-alt` on cell `cac7a125` **quotes** `0.14369554654231262`, and an
iterative solver is exactly where drift would appear. Two reviewers checked it independently to all
17 digits.

### Prose re-authored

One bullet: "the `.T` attribute of a NumPy array or DataFrame" → NumPy array only. Polars frames have
no `.T`, and by that point `X` is already an ndarray, so the reader only ever sees `.T` on NumPy.

### Review

`notes-output-reviewer`: **PASS**. `notes-a11y-reviewer`: **PASS**, all 14 figure surfaces.

### Open items

- Three `:alt:` attributes are **empty in the baseline** (`ols_matrices_new.png`, `grad_descent_1.png`,
  `grad_descent_2.png`). Pre-existing content debt — and the reason harness build note 6 exists, since
  the alt-text gate could not see them.
- The `cac7a125` alt text says "The plot is titled '…'", but the figure has no `plt.title()`; the
  value is a stdout line above it. Pre-existing, but a screen-reader user is sent looking for a title
  that is not there.

## cv_regularization — Cross-Validation and Regularization

Tier B, `DONE`. 1 attempt, debt 0. All 13 gates green.

### Code changes

- `pl.from_pandas(sns.load_dataset("mpg"))`, `.rename({...})`, `.drop_nulls()`; four
  `X["hp^k"] = ...` assignments collapsed into one `select` with `.alias()` calls. Those aliases name
  genuinely new derived columns — `hp^2`, `hp^3`, `hp^4` are quoted by name in the prose — not a
  pandas artifact.
- `pd.DataFrame(...)` → `pl.DataFrame(...)` for the coefficient table.

### Accepted behaviour differences

- **Float formatting changed and was deliberately left alone.** `hp^4` prints as `5.2200625e7`
  rather than `52200625.0`, and the `hp^3` parameter as `0.000009` rather than `8.919763e-06`. Adding
  `pl.Config.set_float_precision` to restore pandas' uniform `%e` column would be exactly the
  cosmetic matching the policy forbids. Both prose claims still read correctly — "orders of magnitude
  larger" against `85.0` vs `5.2200625e7`, and "much larger in magnitude" against `-0.254932` vs
  `-1.2287e-8`.

### Constants changed

| Where | Old | New | Why |
|---|---|---|---|
| test error, `bd6df169` | 23.192405630290637 | 23.19240563000083 | **Environmental, not Polars** |
| ridge coef, `469bfd8e` | 5.89130560e-02 | 5.89130559e-02 | same |
| ridge coef, `469bfd8e` | -6.42445916e-03 | -6.42445915e-03 | same |

The converter attributed these to BLAS accumulation order over a differently-laid-out container. The
reviewer checked and **corrected it**: the pandas path in this env produces the identical drifted
values, so the cause is the environment, not Polars input. No prose quotes any of these digits.

### Review

`notes-output-reviewer`: **PASS**, having rebuilt both paths and confirmed `train_test_split(
random_state=220)` selects byte-equal splits (392 / 313 / 79).

### Open items

- Pre-existing: "Notice that we scale the data before regularizing" — no scaling happens anywhere in
  the chapter. Byte-identical to the baseline.

## _decision_tree — Decision Trees (archived)

Tier B, `DONE`. 1 attempt, debt 0. All 13 gates green. Executed only after `python-graphviz` was
installed into `d100` — it is declared in `requirements.txt` but was absent from the env, so the two
tree-render cells had never run.

### Code changes

`import pandas as pd` → `polars as pl`; `pd.read_csv` → `pl.read_csv`; a boolean mask → `.filter()`
with `pl.col` expressions. Deliberately unchanged: `iris_data[["petal_length", "petal_width"]]` is
valid Polars selection and sklearn populates `feature_names_in_` from it, and
`sns.scatterplot(data=iris_data, ...)` takes the Polars frame directly — verified identical legend
labels, colours, and all 150 point offsets.

### Accepted behaviour differences

- `classes_.dtype` moved from `object` to `<U10`: sklearn derives it from the label container, and a
  Polars string Series gives `<U10`. No prose references it.
- Three `sample()` cells are unseeded and legitimately differ. No prose quotes a sampled row.

### Constants changed

None from the conversion. Accuracy `0.9933333333333333` matches exactly, and the `.filter()` returns
the same 3 rows in the same order, so "1 versicolor and 2 virginicas" still holds.

### Review

`notes-output-reviewer`: **PASS**, with the root-split finding recorded as open question 8.

### Defects found and fixed during conversion

**The root split was a coin flip, and the chapter shipped a sentence naming it.** Both
`DecisionTreeClassifier(criterion='entropy')` constructors carried no `random_state`.
`petal_length <= 2.45` and `petal_width <= 0.8` both perfectly isolate setosa, so they tie on
information gain and sklearn broke the tie differently on every fit — measured **31/29 over 60 fits**,
identically under pandas, so not a conversion effect. Cell `aa8c2851` read "if the `petal_length` …
is less than or equal to **1.75** … `setosa`", which had the right feature and the wrong threshold in
the baseline; the re-executed tree rooted on `petal_width` and made it wrong twice over.

Fixed by pinning `random_state=42` on both constructors — chosen by measurement, not convention:
seed 42 reproduces the **baseline's own root**, `petal_length <= 2.45`, so the tree the chapter was
written against is restored rather than a new one imposed. Verified stable over 10 refits, and the
committed SVG now roots on `petal_length <= 2.45`. Accuracy is unchanged at `0.9933333333333333`.

Two things fall back into place as a result: the prose threshold is now correct as `2.45`, and the
`petal_length > 2.45 & petal_width > 1.75 & petal_length <= 4.85` derivation in cell `905838d9`
traces a real path through the tree again — it lands on the 3-sample virginica node, which is the
"problematic node" the section is about.

This is a narrow, measured seed on one archived chapter, not the book-wide seeding pass of open
question 7, which stays open.

### Open items

- Pre-existing: two of four dropdowns do not match their cells in the baseline either; `d268ac35`
  rebinds the petal model instead of fitting the freshly constructed sepal one.
- The sepal tree's own splits are now deterministic too, but the "we will get around 0.65" validation
  claim in `d62b1563` is still computed by no cell, so it remains unverifiable.

## intro_lec — Introduction (Data 100)

Tier B, `DONE`. **2 attempts** — the only chapter in the batch to fail review. All 13 gates green on
both. Prose score **8.5** (clarity 8.0, idiomatic Polars 8.5, book voice 9.0).

This chapter is flagged `ecosystem_mentions` at density 0.188, just under the tier-D threshold, and it
is the course's first chapter, so it sets the voice for everything after it.

### Code changes

The `pd.Series` demos were **re-aimed rather than translated**. Polars Series carry a name and a dtype
instead of an index, so:

- `s.values` → `s.to_list()`; `s.index` → `s.name, s.dtype`.
- `pd.Series([-1,10,2], index=["a","b","c"])` → `pl.Series("ratings", [-1, 10, 2])` — the
  constructor's optional first argument is the real analogue of the optional `index=`.
- "Indices can also be changed after initialization" → **the data type** can, via `s.cast(pl.Float64)`.
  A translator would have deleted that cell and left a gap; keeping it structurally parallel is what
  makes the section still teach something.
- Selection became position-based. Load-bearing finding: `s[s > 0]` **raises**
  `TypeError: selecting rows by passing a boolean mask to __getitem__ is not supported`, so
  `.filter()` is the only form, not a stylistic preference.

### Prose re-authored

Extensive. "Three fundamental data structures" → **two**, shortened rather than refilled — and
deliberately not refilled with `Expr`, which is the honest third Polars object but one the chapter
never shows. Ecosystem mentions became `polars` where they promise what the chapter teaches. One
`pandas` mention was **kept**: the "long-established standard … inspiration for Petey, our panda bear
mascot" sentence, because the industry-standard claim is not true of Polars and the mascot is a real
course artifact.

### Defects found and fixed during conversion

**Attempt 1 was BLOCKed, and the defect is the interesting kind.** The conversion scrubbed every
editable mention of the index — a grep for `index|indices|label` across all 22 cells returned zero
hits — which is exactly what created the problem. `images/df_elections.png` is a **frozen pandas
artifact** that cannot be edited (`content/*/images/**` is gate-protected), and it says, in 18-point
type with callout boxes drawn around the digits:

> `Index of the elections DataFrame` · `Index of the Result Series` · `Name: Result, dtype: object`

So the figure became the *only* surviving assertion in the chapter that Polars has an index, sitting
directly under a paragraph that carefully avoids the word, in chapter one. The caption had been
rewritten to describe those same labels as "position", which reads as the text contradicting the
picture. Both reviewers found it independently. **Every one of the 13 gates passed on attempt 1** —
no deterministic check can compare a sentence against pixels.

Attempt 2 names the diagram as a pandas rendering *before* the image, then reconciles the labels
underneath: the boxed column is what pandas calls the index, Polars stores no such column and reaches
rows by position counting from 0 — which hands off directly into the Selection section. The
`dtype: object` footer is reconciled to `String`, the word cell `9371d026` actually prints. The alt
text now describes what is drawn rather than what the prose wishes were drawn.

Also removed: "the numbers running down the left-hand side from 0 to 4", which is false for Polars —
verified that neither a Series nor a DataFrame prints row numbering, and the very next cell renders a
Series with nothing down the left.

### Review

`notes-output-reviewer`: **BLOCK** on attempt 1, **PASS** on attempt 2, having re-verified all four
findings and cross-checked the new prose against every regenerated output. `notes-prose-reviewer`:
8.5, above the 8.0 bar, so it did not consume a retry.

One further edit came out of the re-review: the sentence flagging the diagram originally ended "…
which we sort out just below the figure", which narrates the document rather than the data and spends
`pandas` twice in thirteen words. Trimmed to "It is drawn with `pandas`, so a few of its labels carry
that library's vocabulary" — the reconciliation underneath already does the teaching. The chapter
names `pandas` 5 times against 14 for `polars`, down from 12 in the baseline.

### Open items

- **`images/df_elections.png` and `images/row_col.png` should be redrawn from Polars renders.** This
  is open question 2 territory but higher priority than the `pandas_1/2/3` diagrams, because these are
  in chapter one. The prose fix is honest but it is a caption apologising for a picture.
- **Forward constraint on `polars_1`:** this chapter has now committed the book to *two* data
  structures and to addressing rows by position. `pandas_1` currently opens with "Learn more key data
  structures: `DataFrame` and `Index`" — it must not reintroduce `Index`, and its `.loc`/`.iloc`/`[]`
  section has to collapse rather than be refilled.
- ~~Suggested one-sentence improvement: `.cast()` returns a *new* Series.~~ **Applied.** The prose
  reviewer called it the highest-value addition available here, and it is: this is the first place in
  the course a student meets the return-a-new-object habit that every later chapter depends on. Now
  reads "`.cast()` returns a new `Series`, so we assign the result back to `s`."

## ols — Ordinary Least Squares

Tier B, 1 attempt, debt 0. All 13 gates green. 3 sites.

### Code changes

- **`pd.read_csv('data/nba18-19.csv', index_col=0)` → `pl.read_csv(...).drop('Rk')`.** `index_col`
  moves a column *out of the column set* into the index; Polars has no index, so the faithful
  conversion is to drop it. Settled by reading the file rather than by rule: `Rk` is a
  basketball-reference rank counter with **duplicate values** (traded players share a rank), read by
  no cell. Verified `(708, 29)` and an identical column list against pandas. Keeping it would have
  put a meaningless counter in column 0 of every printed table, in a chapter whose subject is which
  columns are features of a design matrix.
- `nba[['FG','AST','3PA','PTS']].head()` → `.select([...]).head()`.

### Prose re-authored

The gloss on the $\mathbb{X}_{:, i}$ notation pointed at `.iloc`/`.loc`; it now points at `df[:, i]`,
which is the real Polars spelling of that notation.

### Constants changed

None — the chapter's prose quotes nothing from its two output cells.

### Review

`notes-output-reviewer`: **PASS**. It confirmed `Rk` has **178 duplicated values** — traded players
get a `TOT` row plus one per team, all sharing a rank (`Rk=16` appears three times) — so it is not a
usable key, and every cell value matches pandas with the 6 nulls in `FG%` landing in the same rows.

### Open items

- ~~`nba.head(5)` renders only 8 of 29 columns, truncating `FG`/`AST`/`3PA`.~~ **False — retracted.**
  The committed HTML carries **all 29 `<th>` headers**. See the note on repr truncation under
  `sampling`; nothing is hidden and no `pl.Config` change is warranted.
- Pre-existing: the display equation numbers columns from 1 ($\theta_0 \mathbb{X}_{:,1}$) while
  `df[:, i]` is 0-based — exactly as `.iloc` was.

## logistic_regression_1 — Logistic Regression I

Tier B, 1 attempt, debt 0. All 13 gates green.

### Code changes

- `pl.read_csv("data/games").drop_nulls()`, with its dropdown mirror. `drop_nulls()` is a no-op on
  1230 rows, exactly as `dropna()` was.
- `plt.plot(X.squeeze(), ...)` → `X.to_series().to_numpy()`.
- **The graph of averages (cell `a8b571dc`) was rewritten, not translated.** `pd.cut` returns
  `Interval` objects whose `.left`/`.right` the code averaged to get bin midpoints; Polars `cut`
  returns categorical **string labels**, so parsing them back into numbers would be worse than doing
  the arithmetic. Replaced with explicit equal-width binning — subtract `lo`, divide by width,
  `.floor()`, `.clip(0, n_bins-1)`, back to a bin centre. A shorter round-to-nearest-multiple form
  was tried and rejected: it yields 21 bins and a `-0.0` label.
- **`groupby("bin")["WON"].mean()` → `group_by("bin").agg(pl.col("WON").mean()).sort("bin")`.** The
  pandas Series *index* was load-bearing — both consumers plot `win_rates_by_bin.index` as x — so
  both call sites now read the columns explicitly.

### Accepted behaviour differences

- **`.sort("bin")` rather than `maintain_order=True`, and the reasoning is the point.**
  `maintain_order` gives order of first appearance, which is monotonic here only by accident:
  `data/games` happens to be sorted by `GOAL_DIFF`. Relying on that would make the red curve's
  correctness a property of the input file rather than of the code. `.sort("bin")` states the actual
  requirement — a line plot needs a monotonic x-axis — and survives any reordering of the data. This
  is the legitimate kind of sort, not the forbidden cosmetic kind, and an inline comment says so.

  The reviewer put it more strongly and is right to: **the sort is load-bearing.** `plt.plot`
  connects points in array order, so an unsorted aggregate draws a zigzag instead of the S-curve the
  next paragraph describes. `games["GOAL_DIFF"].is_sorted()` is `True` today, so `maintain_order=True`
  would work — and would fail silently the day the file is re-sorted.

### Review

`notes-output-reviewer`: **PASS**, having re-executed both binning paths and corrected the constants
table above.

### Open items

- Cell `a8b571dc` is one of the few code cells here **without** `remove-input`, so students read this
  code, and it grew from 4 lines to 11. The prose above it still describes it accurately, and the
  explicit equal-width arithmetic arguably teaches the Data 8 binning concept better than an opaque
  `pd.cut` call — but the visibility is why its inline comments need to stay as clear as they are.

### Constants changed

| Where | Old | New | Why |
|---|---|---|---|
| bin midpoint, first bin | -0.2380 | -0.2377 | `pd.cut` nudges the *left edge* by 0.1% (`adj/2 = 0.000266`) |
| every other bin midpoint | uneven spacing | `lo + (k+0.5)·0.0266` | `pd.cut` **rounds its interval labels** before `.left`/`.right` are read |
| win rate, bin at 0.0283 | 0.705128 | 0.701863 | 5 games at `GOAL_DIFF == 0.015` sit exactly on an interior edge |
| win rate, bin at -0.2377 | 0.033898 | 0.033333 | 1 game at `-0.118` sits exactly on an edge |
| win rate, bin at 0.1081 | 0.505747 | 0.502959 | 1 game at `0.148` sits exactly on an edge |

**Both halves of this table were corrected by the reviewer, which is worth recording because the
converter's account was plausible and wrong in a way no gate could catch.** It reported *two* win
rates moving; the true count is **three** — the five games at `GOAL_DIFF == 0.015` leave bin 9 for
bin 10, so both bins' means change, not one. And it attributed all the midpoint drift to the 0.1%
left-edge nudge, which in fact explains only the first bin. The rest is `pd.cut` rounding its
interval labels, which leaves *pandas'* midpoints unevenly spaced — successive gaps of 0.0270,
0.0265, 0.0265, 0.0265, 0.0268 — where the explicit arithmetic produces exactly even ones. **The new
x-positions are the more correct of the two.**

Exactly 7 rows of 1230 change bins, all sitting precisely on an interior edge: pandas `cut` is
right-closed `(l, r]`, the arithmetic form left-closed. Reproducing the pandas convention would need
either a special-cased comparison or `pl.col(...).cut()`, which returns string labels you would then
parse back into floats — both purely to recover a pandas artifact. The cell's only output is a
figure, no win rate is printed anywhere, and the affected means move in the third decimal, which is
sub-pixel on the curve.

## sampling — Sampling

Tier B, 1 attempt, debt 0. All 13 gates green. 46 MB of data, the slowest chapter in the batch.

### Code changes

- Three `votes['voted_dem'].iloc[idx]` → `.gather(idx)`. `Series.gather` accepts a NumPy `int64`
  ndarray directly — no `.tolist()`, no cast.
- **`1 - poll['dem_wins']` → `~poll['dem_wins']`.** Polars raises
  `TypeError: cannot do arithmetic with Series of dtype: Boolean and argument of type: 'bool'`.
  `bool_series * int_series` still works and is unchanged.
- **`round(series)` → `.round()`.** The builtin raises `type Series doesn't define __round__`.
  Verified Polars rounds half-to-even like pandas, and `pred_dem_1936` stays `213283.0`.
- Cell `1df8f9d3` needs **two chained `with_columns`**: `correction_factor` depends on columns
  created in the same statement, and expressions inside one `with_columns` all see the pre-existing
  frame.
- `pl.read_csv` reads the `zipfile.ZipExtFile` handle directly, so the zipfile idiom is untouched.

### Prose re-authored

**One paragraph whose premise the conversion falsified.** Cell `b7e78842` said "the cell above is a
little slow, since we're sampling from a `DataFrame` with almost 45 million rows. We can speed up the
sampling using `NumPy`." The reviewer re-measured independently on the real 44.4M-row column, 7 reps:

| | pandas | Polars |
|---|---|---|
| `s.sample(1000).mean()` | 1.028 / 1.064 / 1.150 s | 0.0018 / 0.0020 / 0.0035 s |
| NumPy idx + `iloc`/`gather` | 0.0005 / 0.0006 / 0.0013 s | 0.0014 / 0.0016 / 0.0026 s |

`.sample` went from ~1.06 s to sub-millisecond — roughly **1700×**. "A little slow" is not defensible
at 0.6 ms. Note also that the NumPy route was an ~1800× speedup under pandas and is ~3× under Polars,
on a sub-millisecond baseline — so *rescaling* the claim ("still 3× faster!") would have been wrong
too. A 0.4 ms saving is not a thing to teach. The paragraph now describes what the cell actually
demonstrates: choosing row positions yourself, and that this is the form reused in the
repeated-sampling cells below. That forward claim was verified in the source, not inferred.

### Constants changed

None. Every deterministic value reproduces exactly: `44430549`, `0.6245897614274358`,
`0.4289439704056572`, `42058418.0`, `380`/`151`, Arizona `35.996`/`21.503`. One 1-ulp drift on the
corrected proportion (`...633` → `...632`), quoted in prose as "54%".

### Open items

- **All randomness in this chapter is unseeded** — `np.random.default_rng()` and `Series.sample(1000)`
  both without a seed. Five outputs change on every execution. No literal number is quoted in prose,
  but two claims ride on the draws: "both of the estimates above are pretty close to 62.5%"
  (SE ≈ 0.0153, so a 1000-draw proportion lands in ~0.59–0.66) and "within about 3 percentage points"
  (1.96 × 0.0153 ≈ 0.030). Both structurally stable, neither guaranteed. Open question 7.
- ~~Polars elides the middle columns, so `poll`'s wide tables hide headers.~~ **False — retracted,
  and this one nearly propagated.** The claim described Polars' `text/plain` repr, which does
  truncate. **MyST publishes `text/html`, and the Polars HTML repr does not truncate at all.** The
  committed outputs carry every header: 10, 12, 14 and 17 `<th>` for cells `cc6b2fcf`, `270e983e`,
  `2ffa1838` and `1df8f9d3`. Nothing is hidden on the page and `pl.Config.set_tbl_cols(-1)` is not
  the book-wide question this record originally made it.

  Recorded prominently because the same wrong claim independently reached the `ols` record, and the
  rationale was about to be reused on `eda` and the tier-D chapters — all of which have wide frames.
  **Judge a published table from the `text/html` output, never from `text/plain`.**

- **A pre-existing SRS mismatch that the prose rewrite now leans on harder.** The section is headed
  "Simple Random Sample (SRS)" and the chapter defines SRS as sampling *without* replacement, but all
  three `rng.integers` cells draw **with** replacement. This is identical in the baseline —
  `iloc[idx]` was equally with-replacement — so it is not a conversion defect. But the old prose
  framed the NumPy form as a speed detour, and the new prose promotes it to "the form we'll reuse".
  With the speed justification gone, the honest fix is for the three loops to call
  `.sample(1000).mean()`, which would be a real SRS and would delete the NumPy detour entirely. That
  is a course-staff content decision. Related and immaterial: `04510ea5`/`b37cf863` pass
  `high=n_votes-1` where `rng.integers` treats `high` as exclusive, so they can never draw the last
  row — one in 44.4 million, pre-existing.
- Float formatting on the published page: California renders `1.467076e6` where pandas rendered
  `1467076.0`. Values are exact and no prose quotes them, so this stays — **it must not be "fixed" by
  matching pandas.** Recorded because it sits in a table whose purpose is comparing vote counts.

## visualization_2 — Visualization II

Tier B, 1 attempt, debt 0. All 13 gates green. 38 figure surfaces.

### Code changes

- **`index_col=0` → `.drop("")`.** The first CSV field has an **empty header**, and its values are
  non-contiguous — `[0, 1, 2, 3, 5, 6, 8, 9, 10, 13, 15, 16, …]`. It is a stale positional index left
  behind when a pandas filter dropped rows *before this file was written*; the gaps are the dropped
  rows. Verified `(166, 47)` and an identical column list against `pd.read_csv(..., index_col=0)`.
  The one place the pandas index was used, `pd.DataFrame(index=wb.index)`, was alignment scaffolding
  rather than a data read, so the Polars rewrite builds the frame directly.
- `.sort_values("inc")` → `.sort("inc")`.
- **Deleted `warnings.filterwarnings("ignore", "use_inf_as_na")`.** `use_inf_as_na` is a *pandas
  option name*; the filter can no longer match anything. Re-ran every seaborn call and the sklearn
  fit under `warnings.simplefilter("always")` with the filter absent: zero warnings. Leaving a
  pandas-option suppression in student-visible dropdown source would read as a typo.

### Accepted behaviour differences

- **The nulls-first sort hazard does not apply here, checked rather than assumed:** `.drop_nulls()`
  runs immediately before, so `inc` has `null_count() == 0` at the sort site, and no `.head()` or
  positional slice follows. `descending` was never passed, so the inverted-sense trap is moot.
- **8 distinct tied `inc` values spanning 17 rows**, leaving 9 row *positions* ordered differently
  from pandas. The `(inc, lit)` multiset is identical, so the scatter draws the same points and the
  regression line — which depends on `inc` alone — is invariant by construction.

  **The attribution here was backwards in the first draft of this record, and the correction matters:
  Polars is the stable side.** Its order is identical to `sort("inc", maintain_order=True)` and
  reproduces across 200 in-process sorts and `POLARS_MAX_THREADS` 1–5; it is *pandas'* default
  quicksort that permutes ties. Forcing a different tie order by shuffling first and re-rendering
  changes 4 pixels at max channel delta 1/255, from antialiasing blend order — so even the
  pathological case cannot churn the PNG visibly.

### Prose re-authored

"This class primarily uses `seaborn` and `matplotlib`, but `pandas` also has basic built-in plotting
methods" — the clause was dropped rather than repointed. Polars *has* a `.plot` namespace, but on
this pin it raises `ModuleUpgradeRequiredError: altair>=5.4.0 is required`, so naming it would send
students at an error.

### Constants changed

| Where | Old | New | Why |
|---|---|---|---|
| slope, cell `38ca2d00` | 336400693.43172705 | 336400693.43172693 | **Environmental, not Polars** |
| intercept, cell `38ca2d00` | -1802204836.0479987 | -1802204836.0479977 | same |

The first draft of this record said "unchanged", which was wrong — the committed bytes did move. The
reviewer caught it and ran the **baseline pandas code verbatim in this env**, getting exactly the new
values, so the cause is sklearn/BLAS drift rather than the conversion. Recorded rather than glossed,
because a future reviewer diffing this notebook would otherwise attribute a real byte change to
Polars. No prose quotes either number. `df.shape` is `(129, 2)` under both libraries.

### Review

`notes-output-reviewer`: **PASS**, having rendered all 12 figures side by side and verified the
`(166, 47)` frame column-for-column against pandas.

### Open items

- **Nine matplotlib data calls** — 7 `plt.scatter` and 2 `plt.plot` — were left **without**
  `.to_numpy()`. Verified rather than assumed: `np.asarray(series)` equals `series.to_numpy()` bit
  for bit on both nullable columns including null→NaN, `Series + ndarray` returns a Polars Series
  with nulls preserved, and `np.log(Series)` returns a Series. The chapter's subject is
  `plt.scatter`, and `.to_numpy()` on every argument would also land in three dropdown mirrors as
  unexplained noise. Settled, not merely flagged.

### Carried to later chapters

`np.log` on a Polars Series that **does** contain nulls emits
`RuntimeWarning: divide by zero encountered in log` — the ufunc runs over the raw buffer, where
nulls hold `0.0`. Values and nullity come out correct, but the warning would land as a committed
stderr line. It does not fire in this chapter because `np.log` only touches `df["inc"]` after
`.drop_nulls()`. **Any later chapter that logs a nullable column needs this checked** — `eda` and
`pca` both do transformations of this shape.

## inference_causality — Inference and Causality

Tier B, 1 attempt, debt 0. All 13 gates green. **The first chapter to need an allowlist entry.**

### Code changes

- Four `pl.from_pandas(sns.load_dataset(...))` crossings. `nan_to_null=True` turns the 6 NaN
  `horsepower` values into nulls; **no `drop_nulls()` follows in this chapter** and `weight`/`mpg`
  have none missing, so the frame stays 398 rows exactly as in the baseline.
- `.melt()` → `.unpivot()`, keeping the `variable`/`value` names that `x=` and `facet_row=` reference.
- `sample(frac=1, replace=True)` → `sample(fraction=1, with_replacement=True)`.
- `np.random.seed(...)` → `pl.set_random_seed(...)` at all four sites.
- The parameter/CI tables become Polars frames with the former pandas index as an explicit
  `parameter` column.
- `np.mean((Y - model.predict(X)) ** 2)` → `((...) ** 2).mean()` — the NumPy form raises on a Polars
  Series. Value bit-identical at `0.04547085380275759`.
- Doc link repointed from `pandas.DataFrame.sample` to the Polars equivalent (verified HTTP 200).

### Constants changed

| Where | Old | New | Why |
|---|---|---|---|
| 95% CI for θ₁, `fec55157` | [-0.259, 1.103] | **[-0.265, 1.124]** | different RNG draws a different bootstrap sample |
| plotly OLS hover, `b241cb77` | `-0.00730597 · weight + 44.9995`, R²=0.733007 | `-0.00779906 · weight + 47.2341`, R²=0.716467 | same |

Confirmed against the committed output of cell `fec55157`:
`(-0.26512011103620964, 1.1239590856397368)`. Everything else holds: θ̂₁ = 0.431 unchanged, 0 still
inside every parameter's CI, the interpretable model still "almost as well" (0.045471 vs 0.046494),
and the θ₁ CI that must exclude zero still does at (0.601, 0.819).

The hover-text row is in this table because a reader can surface it by hovering, even though no prose
or alt text quotes it — it would otherwise be an unrecorded content change on the page.

**That the CI move is noise rather than a defect was established statistically, not asserted.** The
reviewer re-ran both bootstraps at 10,000 reps and compared the whole distributions: two-sample
KS **p = 0.367**, mean difference 0.64 SE, and both distributions sitting the same small distance
below θ̂₁. Across 8 Polars and 4 NumPy seeds the lower endpoint ranges over [-0.274, -0.246] and the
upper over [1.103, 1.135] — the new interval sits mid-range in both, and **the baseline's 1.103 was
the extreme value of that set.** The resampling was separately confirmed to be a correct iid
multinomial bootstrap: 20,000 resamples of n=44 give 28.007 mean distinct rows against a theoretical
27.999, uniform per-row draw frequency (χ², p = 0.26), and multiplicity matching Binomial(44, 1/44)
(p = 0.13).

### The allowlist entry

`sns.pairplot` (cell `fcd8d006`) **type-checks its argument** and raises
`TypeError: 'data' must be pandas DataFrame object` on a Polars frame — verified live on seaborn
0.13.2. It is the only seaborn entry point in either batch that does this; `scatterplot`,
`jointplot`, `kdeplot`, `lmplot`, `stripplot` and `rugplot` all take Polars directly and render
pixel-identically. No cheaper rung exists because `pairplot` draws a grid over the whole frame.

### Defects found and fixed during conversion

An illustrative block inside an **HTML comment** (cell `a30378ef`) never renders and never executes.
It was converted anyway, and verifying it live caught two errors that would otherwise have shipped as
broken teaching code: `pl.read_csv` needs `null_values='NA'` or it raises `ComputeError` on the
`TempC` column, and `is_in` on date literals raises `InvalidOperationError` without
`str.to_date()`. Row counts then match the pandas original exactly (12241 after filter, 176 in `GA`).

### Open items

- The mpg loop in cell `68454791` is **not independently seeded** — it draws from the global stream
  left by earlier cells, so it is deterministic on a clean top-to-bottom run but not on a single-cell
  re-run. The reviewer demonstrated this symmetrically rather than taking it on trust: burning 500
  draws before the cell moves its printed CI from `-0.01014361` to `-0.01012088`, and running the
  **pandas baseline** with the same burn moves it from `-0.01019291` to `-0.01017419` while the
  independently-seeded cells stay put in both. Carried over, not introduced.

### Review

`notes-output-reviewer`: **PASS**. The three eggs-bootstrap cells reproduce bit-identically to 17
digits across three independent processes — clean, under `POLARS_MAX_THREADS=1`, and with a
deliberately contaminated RNG history — and the stream is invariant to pool size at
`POLARS_MAX_THREADS` 2, 4 and 16.

One note on the allowlist entry, which the reviewer confirmed and refined: `sns.PairGrid` *does*
accept a Polars frame, but it is a different API rather than a lower rung on the interop ladder, and
using it would turn one teaching line into three `map_*` calls. The entry stands as written.
- Pre-existing: two sites print the label "RMSE" while computing MSE; baseline line 414 has
  `:alt:Illustration…` with no space after the colon, which MyST likely does not parse as an option;
  and the prose says "a sample of 20 cars" twice while the code sets `sample_size = 100`.

## visualization_1 — Visualization I

Tier B, 1 attempt, debt 0. All 13 gates green. The heaviest tier-B chapter in the book: 30 code
cells, 12 dropdown mirrors, 51 figure surfaces. Prose score **8.33**.

### Code changes

- **`index_col=0` → `.drop("")`**, matching `visualization_2` on the same file. Both chapters reached
  this independently; had they disagreed, any prose quoting `wb.shape` would conflict across two
  adjacent chapters.
- **Two `.loc[mask, col] = value` conditional assignments → `with_columns` + `when/then`.**
  For `Hemisphere`, no `.otherwise` — unmatched rows get null, matching pandas' implicit NaN. The
  branch is unreachable anyway: `Continent` has zero nulls and its six values are exactly
  `north ∪ south`, giving `Northern 95 / Southern 71 / 0 null`, same as pandas.
- **The `wb_quartiles` category assignment**, where the null hazard is real and lands correctly.
  `Gross domestic product: % growth : 2016` has 7 nulls; under Kleene logic both compound masks
  evaluate to **null** there, `when` treats a null predicate as false, and those rows fall through to
  the implicit null category — which is exactly what pandas' `category = None` initialisation left
  them as. Counts match at **78 / 78 / 10 null** (10 rather than 7, because 3 more rows sit exactly
  on a quartile boundary and match neither mask — true in the baseline too).
- `warnings.filterwarnings("ignore", "use_inf_as_na")` deleted as a dead pandas-only filter, as in
  `visualization_2`.

### Accepted behaviour differences

- No `.to_numpy()` was added at the matplotlib boundary. Verified on matplotlib 3.10.0 that
  `plt.hist` on a Float64 Series carrying 9 nulls returns bins and densities bit-identical to pandas,
  and `plt.bar` takes a string Series for positions. Rung 1 of the interop ladder works, so the
  teaching cells stay clean.

### Prose re-authored

**A section was restructured rather than translated, and this is the largest prose change in either
batch.** The baseline's first bar-plot subsection was `### Plotting in Pandas`, which existed to
demonstrate `.value_counts().plot(kind='bar')` and then advise students against it. Polars' `.plot`
accessor is Altair-backed, altair is not installed, and the course excludes it — so there is nothing
to demonstrate *and* nothing to warn against. The cell could not be deleted, because the cell-id
sequence is frozen by G1.

The organising idea changed from **which library draws the chart** (pandas → matplotlib → seaborn) to
**how much work the library does for you**: you count and plot by hand, you label by hand, then
seaborn does all three from the raw frame. The prose reviewer's judgment on whether this is teaching
or padding is worth quoting in substance — the old arc motivated matplotlib only *negatively*
("pandas plotting is not supported"), whereas the new one describes the actual conceptual difference
between the libraries, and it makes the untouched baseline sentence in `4f3a5c0e` ("the general
structure of a `seaborn` call involves passing in an entire `DataFrame`") read as the payoff of a
setup rather than a stray observation.

What made it fit: the two committed `#| fig-alt` strings already distinguished these cells on exactly
the axis-label axis — `bf7276ef` says "each continent on the x-axis", `fea17420` says "…**and count
on the y-axis**" — so both survive unedited and stay accurate.

### Defects found and fixed during conversion

**The re-authoring armed a contradiction that had been dormant.** The new prose named the chapter's
own best-practice bullet ("sort by count, high to low") and claimed the figure complied — but
`sns.countplot` two cells later orders continents by order of appearance, which for this CSV is
alphabetical. In the baseline nothing pointed at the bullet, so no reader connected it to a figure; a
student who took the new pointer seriously would compare the two figures, see Asia and Europe swap,
and conclude the rule was decorative. Fixed by describing what `sort=True` does and dropping the
compliance claim. **The pre-existing tension is unchanged; only the claim about it is gone.**

Three smaller prose fixes in the same pass: the section opened straight into a deliberately
*unlabeled* chart with no signpost, so the intro now says the plot is built twice and why; "there are
a few ways to do this" headed two ways; and "labels, titles, and legends are each a separate call"
named two things the section never demonstrates, in a rule-of-three construction that appears nowhere
else in `content/`.

### Review

`notes-prose-reviewer`: **8.33** (clarity 8.0, idiomatic Polars 9.0, book voice 8.0) — above the 8.0
bar, so it did not consume a retry. `notes-output-reviewer`: **BLOCK** on attempt 1, and the block is
worth recording because **the orchestrator caused it**, not the converter.

The three prose fixes above were staged in the jupytext source and written into this file as *done*
before the notebook was rebuilt from that source. The reviewer read the notebook, found the old
prose, and blocked — correctly. Everything else it checked was clean: it re-derived the quartile
counts row by row, confirmed rung-1 interop at every matplotlib site (including that
`16410.0 * 4.7741589911386953e-05 = 78.343949044586%` reproduces bit-identically), and established a
pure-churn pixel floor from the cells whose source is NumPy over a literal list.

**The lesson is the harness's own first rule pointed at the log instead of the outputs: committed
artifacts are the deliverable, and the record must follow the artifact rather than lead it.** A
conversion record that documents an intended edit reads exactly like one that documents a landed
edit. Rebuild, then write.

**PASS** on attempt 2. Two of its closing judgments are worth keeping:

- The `positions` → `labels` wording change was filed as a nit and is not one. matplotlib's
  categorical unit converter maps the strings to positions `0..n-1` and installs them as tick
  labels — so the strings are *not* the positions, and the original sentence was wrong about the
  mechanism it was teaching.
- The signpost says "build it twice" while the section renders **three** figures, and that is
  correct rather than a miscount: the two *builds* are matplotlib and seaborn, and the matplotlib
  build takes two renders because the signpost's own clause ("asks us to do the labelling
  ourselves") makes labelling a separate step. Saying "three times" would flatten the two-vs-one
  structure the section is built on.

### Open items

- **The countplot ordering itself — and the reviewer's argument for *not* hedging the bullet.** The
  applied fix removes the false claim. What remains is a general best-practice bullet ("sort by
  count, high to low") and one figure that departs from it. **The bullet should not be softened**,
  because the chapter already has an established habit for this exact situation: the same list says
  "use color sparingly if the data has natural groups", and `c22e7e3c` paints six categories six
  colors that encode nothing — yet the bullet stands unhedged and `4f3a5c0e` instead *volunteers*
  the departure right after the figure ("the color scheme of this particular bar plot is
  arbitrary — it encodes no additional information"). The house pattern is **name the departure, do
  not weaken the rule.**

  So the ordering departure is the one the chapter fails to self-annotate — an asymmetry in its own
  habit, not a false claim, and not blocking. Two editorial resolutions, both course-staff work and
  neither required: pass `order=continent['Continent']` and turn the contradiction into the lesson
  (re-renders a figure), or add a half-sentence beside the existing color caveat in `4f3a5c0e`
  noting that seaborn counts categories in the order it meets them unless told otherwise
  (re-renders nothing, touches no output). Not applied here: removing a false claim is a defect fix,
  but adding new pedagogical caveats is editorial content and belongs to course staff.
- **The "don't use dataframe-attached plotting" advice is gone and should not be restored here.**
  A student who tries Polars' `.plot` gets an `ImportError`, not a limited chart, so the warning would
  describe a hazard they cannot encounter. If the course wants students to recognise
  `.plot(kind='bar')` in code they find online, that belongs in `intro_lec`, whose subject genuinely
  is the ecosystem.
- Pre-existing: the first dropdown in `6eab6cca` opens with a bare ` ``` ` instead of ` ```python `,
  so the first code block a reader sees has no syntax highlighting.

## polars_1 — Polars I *(authored; replaces `pandas_1` + `pandas_2`)*

Tier D, 2 attempts. 153 cells, 80 code. Reviewed `PASS`; **awaiting human sign-off**, which is what
tier D carries in place of a structural diff.

Course staff cut tier D from three chapters to two. `pandas_1` was about two-thirds Index; with that
concept deleted, what remained was not a chapter's worth, so it opens this one. Its DataFrame
construction, attributes, `.head`/`.tail` and `[]` extraction survive **in full** — only the Index
itself is gone.

### How it was written

Not designed from scratch. The sister repo (`DS-100/polars-ver`) had already converted the lectures
these chapters mirror, and the notes and lectures were verified to be genuinely mirrored: same
datasets, same section names in the same order, same three custom-sort approaches *by name*. The
notes are the expanded prose version — they add sections the lecture has no time for and drop its
Slido interludes. So the job was to re-expand decisions already made, which is also what keeps
textbook and lecture from teaching different spellings of the same operation.

### Structure

Front half from `pandas_1`/lec02: `DataFrame`s and `Series` (four construction routes), attributes
(`columns`, `dtypes`, `schema`, `shape`), `.head`/`.tail`, `[]` kept rich (`df[row, col]`, lists,
list + column slice, `:`, single-name → Series), `select`/`filter` replacing `.loc`, Boolean
Operators with the precedence warning, and `with_row_index` as the honest answer to "Working with
the Index".

Back half from `pandas_2`/lec03: utility functions, adding/removing/modifying columns, sorting, and
**all three custom-sort approaches** — kept, renamed to "Create a Temporary Column", "Sorting on an
Expression", "Sorting with `map_elements`". The equivalence of *kinds of things demonstrated* was the
brief, and collapsing them would have failed it.

### Defects found and fixed

**The executor refused to write the notebook.** `nb_execute` reported
`0 new / 1 lost error(s) -- notebook NOT written`: `pandas_2`'s deliberate erroring cell `ccf796ec`,
which showed that Python's `and` fails on a Series, had been dropped and survived only as prose. The
lesson works in Polars — `TypeError: the truth value of an Expr is ambiguous` — so the cell was
restored **under the baseline's own id**, which makes G9 align naturally instead of needing two
allowlist entries. The hard stop did its job on a chapter that was otherwise finished.

**`pl.Series.head()` defaults to 10; `pl.DataFrame.head()` defaults to 5.** The chapter teaches
"called with no argument at all, `.head` gives us five" — and two later cells called `.head()` on a
*Series*, committing outputs with ten values. The sentence whose only job is to teach the default was
contradicted by the page's own output. Fixed with explicit `.head(5)`; the reviewer then audited all
22 `.head()` call sites and confirmed the remaining 14 are all DataFrames rendering 5.

Two smaller ones: the null-sort rule was stated unconditionally while six of the chapter's own
sort-then-head cells omit it (both datasets are null-free, so the fix is a clause on the rule, not
six edits), and "the two lines Polars prints above the data" is three — the column-names row sits
between `shape:` and the dtypes.

### Open items

- **Cell ids regenerate on every rebuild** — all 153 except `ccf796ec`, which survives only because
  it is hardcoded into the jupytext source. Course staff have **accepted this**, so it is recorded
  rather than fixed. The costs, for whoever hits them next: no tier-D review can diff against a
  previously-reviewed state, ids cited in one review will not resolve in the next, and `ccf796ec` is
  the single thread anchoring G9 and G10 to the baseline. If a future pass wants stability, the fix
  is to write ids back into the `.py` after the first build rather than letting jupytext mint new
  ones each time.
- `content/polars_1/images/` holds three `pandas_3` groupby diagrams that arrived with the `git mv`.
  They are unreferenced here and byte-duplicates of the copies in `polars_2/images/`, where the cells
  that use them live, so they can be deleted outright.

## polars_2 — Polars II *(authored; replaces `pandas_3`)*

Tier D, 3 attempts. 79 cells, 41 code. Reviewed `PASS`; **awaiting human sign-off**.

Follows lec04's spine: `group_by().agg()`, counting rows, filtering by group with `.over()`, the
group_by puzzle with its attempts and alternatives, `GroupBy` objects, multi-column grouping,
`pivot` and `pivot` with multiple values, and joins. The notes-only sections were restored: Summary
of `group_by()`, Nuisance Columns, Renaming Columns After Grouping, Some Data Science Payoff.

**This chapter now owns the join-coalescing explanation**, which `eda` had been carrying inline
because nowhere else covered it.

### Two judgement calls that came out right

**`map_batches`, not `map_elements`.** The brief asked for one example of when `map_elements` is
still needed. Inside `.agg()` it is element-wise — it hands the UDF an `int`, not a Series — so it
cannot carry a group-level example at all. The group-level escape hatch is
`map_batches(..., returns_scalar=True)`, which is also what the lecture uses; `map_elements` is named
as the per-value counterpart with its `PolarsInefficientMapWarning`.

**"Nuisance Columns" kept rather than deleted.** The concept does not exist in Polars, but a student
who has heard the term deserves to learn what happened to it. The section explains why the expression
model dissolves the problem, and points at `pl.all()` as the one construct that still bites.

### Defects found and fixed

**`images/error.png` was a pandas traceback rendered as pixels** — `return series.iloc[-1] /
np.max(series)` raising `TypeError: unsupported operand type(s) for /: 'str' and 'str'`. It was the
last pandas artifact reaching a reader, and **no code gate can see inside a PNG.** Three things were
wrong at once: the prose described a *sum* failing while the image showed a *division* failing; the
image's function is named `ratio_to_peak`, which this chapter defines two sections later with a
different body — same name, two bodies, one of them pandas; and its `:alt:` described the prose's
claim rather than what is drawn, so a screen-reader user and a sighted reader were told different
things.

The reference was removed (allowlisted under `removed_figures` with the redraw spec) and the prose
now states the verified message. It also gained the more useful half: `pl.all().mean()` does **not**
raise on that frame — it leaves `null` in the text columns, which is the more dangerous behaviour
because nothing announces it.

**Then the replacement sentence published mangled, and that one was the orchestrator's.** It nested
single backticks inside a single-backtick span, so CommonMark split it into two disjoint code spans
with the message broken across them. Fixed with a padded double-backtick span and verified in the
**built artifact** rather than the source.

**The class is worth carrying forward: `prose-code-blocks` walks *fenced* blocks, so inline-span
damage is invisible to every gate here.** Twice in this chapter the claim was true and the page was
wrong — the exact failure mode a gate cannot reach, and the reason tier D carries a human read.

Also applied: `merged.columns` in its own cell, because the join's repr elided `First Name` — the
coalesced key that bullet 2 is *about* — behind `…`, making a schema claim unverifiable in the one
section that exists to prevent that surprise. And `maintain_order="left"` on the anti join, which the
chapter had been relying on by luck one paragraph after telling readers joins carry no ordering
guarantee.

### Open items

- `images/error.png` needs retaking. **It must use `sum`** — `mean` does not raise, so a screenshot
  of it would show no error at all.

## pca — Principal Component Analysis

Tier C, 1 attempt, debt 0. All 13 gates green. 82 cells, 40 code cells, 31 MB of data, 26 dropdown
mirrors. **The hardest reshape work in the book outside the tier-D rewrites** — the pandas version
was built on the index at nearly every step.

### Code changes — the seven reshapes

1. **`pivot_table(aggfunc=was_yes)` → `pivot(aggregate_function=…)`.** The custom aggregate stops
   being a function and becomes an expression: `was_yes(s): return 1 if s.iloc[0] == "Yes" else 0`
   → `(pl.element().first() == "Yes").cast(pl.Int64)`. Identical 0/1 matrix, and the singular values
   match pandas to 8 significant figures (`55.79323305, 14.27972677, …`).
2. **Mean-centering — the site where a silent error would have destroyed the chapter.**
   `vote_pivot.select(pl.exclude("member") - pl.exclude("member").mean())`. The `member` identifier
   is now ordinary data rather than an index, so centering it along with the 41 vote columns would
   have corrupted the SVD and every figure downstream **with all gates green**. Kept in Polars rather
   than crossed to NumPy because three downstream sites need a frame, and because "subtract the mean
   of each attribute column" is step 1 of the procedure the section teaches. `np.linalg.svd` accepts
   the frame directly.
3. `pd.DataFrame(index=…)` → an ordinary `member` column.
4. **The index-alignment join.** `.join(legs.set_index("leg_id")).dropna()` →
   `.join(legs, left_on="member", right_on="leg_id", how="inner", maintain_order="left")`. The
   `.dropna()` was indeed doing an inner join's work — **439 rows either way**, and `legs` has no
   duplicate `leg_id` and no nulls, so nothing else was being dropped. `maintain_order="left"` is
   load-bearing: three `np.random.normal` jitter columns are added **positionally** immediately
   after, so a row-order change would attach jitter to the wrong legislators.
5. `groupby("member").size()` → `.filter(...).group_by("member").agg(pl.len().alias("num votes"))`,
   435 rows, same as pandas.
6. **The transpose disappeared.** `.T.reset_index().rename().melt()` existed only to get roll calls
   into rows so `melt` could work; `unpivot(index="party", …)` does it in one step. 123 rows
   (3 parties × 41 calls), same as pandas. `.sort("party")` added because Polars group order is not
   guaranteed and this drives facet-row order on a published figure.
7. `legs.set_index("leg_id")` and `legs.sort_index()` were **no-ops in the baseline** — both returned
   new frames that were discarded. Deleted rather than translated.

### Accepted behaviour differences

- **`sort_columns=True` on the pivot is chart content, not index-matching.** Roll calls 515–555 are an
  ordinal sequence of votes across September 2019 and form the x-axis of two bar charts; without it
  Polars emits them in CSV order, 555 first, descending.
- **`.sort("member")` on the pivot is also chart content — and it was missed on the first pass.**
  See below.
- **`.alias("num votes")`** kept rather than accepting Polars' default `len`, because that string is a
  plotly hover/legend label on a published figure — the default would print a bare "len" on the page.

### Constants changed

| Where | Old | New | Why |
|---|---|---|---|
| `print(vote_pivot.shape)` | (441, 41) | **(441, 42)** | `member` is now a column rather than an index |
| 4th singular value, `rectangle_data` SVD | 1.75309971e-14 | 9.92685575e-15 | float noise on a value that is mathematically zero |

The a11y reviewer corrected my placement of that second row: the near-zero value belongs to the
**`rectangle_data`** SVD, not the scree plot on the voting data. The nearby prose says "so small
($10^{-15}$) that it's practically $0$" — which was *already* loose in the baseline, quoting
$10^{-15}$ against a committed $10^{-14}$. The conversion moved the value from `e-14` to `e-15` and
so, incidentally, made the sentence more accurate than it was. "Practically 0" holds either way.

### Review

`notes-a11y-reviewer`: **PASS** — all 11 `{image}`/`:alt:` pairs byte-identical to the baseline, no
empty alts in either version. Worth recording *why* the unseeded Fashion-MNIST figure is safe despite
redrawing different garments every run: it carries **no alt text at all**, and its facet titles are
generated at render time from `images["class"]`, so whichever garments are sampled, their labels are
correct by construction. The one static alt naming Fashion-MNIST is generic and names no garment.

`notes-prose-reviewer`: **8.83** (clarity 8.5, idiomatic Polars 9.0, book voice 9.0).

### Defects found and fixed during conversion

**The student-visible cell lost the comment its hidden twins kept.** The "two images per class"
expression appears three times; the two copies inside `remove-input` cells carry
`# keep two rows drawn at random from each class`, but the one cell a reader actually sees
(`3ec83d53`) did not — leaving an undocumented shuffled-rank window filter,
`images.filter(pl.int_range(pl.len()).shuffle().over("class") < 2)`, in a chapter where sampling is
not the subject. The baseline's visible line was `groupby('class', as_index=False).sample(2)`, which
was self-documenting. Comment added.

The tempting wrong fix, flagged by the prose reviewer and not taken: `group_by("class").head(2)` reads
better but would make the two figures **identical**, since it drops the shuffle.

**But the comment was the least of what was wrong with that line, and the output reviewer caught both
of the real defects — attempt 1 was BLOCKed.**

**(a) The figure silently lost its class grouping.** pandas `groupby("class").sample(2)` returns rows
in sorted key order, two adjacent per group, so the published grid read *Ankle boot, Ankle boot, Bag,
Bag, Coat, Coat…*. The Polars window filter returns rows in **original frame order**, scattering each
class's pair across the grid — Ankle boot at slots 13 and 16, Shirt at 5 and 19. The prose directly
above still said "let's break this down further and **look at it by class**", and the figure no
longer did. Fixed with `.sort("class")`. That sort is required by the sentence introducing the
figure; it is not cosmetic pandas-matching.

Note how nearly this was missed: the a11y review had already cleared the figure on the grounds that
its facet titles "are correct by construction". That is true — and it is a statement about the
*labels*, not the *layout*. Two reviewers looking at the same figure for different properties is what
caught it.

**(b) The conversion un-seeded a previously reproducible figure — and I filed that wrongly.** I first
logged this under open question 7 as pre-existing churn. It is not: the baseline's `.sample(2)` rode
NumPy's global RNG under `np.random.seed(23)`, so the figure *was* deterministic. `.shuffle()` uses
Polars' RNG, which `np.random.seed` does not govern — so the seed line survived the conversion intact
while quietly ceasing to control anything. A regression introduced by the conversion, not inherited.
Fixed with `.shuffle(seed=23)`, keeping the baseline's seed value.

Verified after rebuilding, by paper position rather than annotation list order (list order is
misleading here): the committed grid's display sequence is now **identical to the baseline's**, all
10 pairs grouped, in both cells.

**Do not delete the `.sort("class")`.** An earlier draft of this record explained the match by saying
`class` is a numeric code and the layout orders facets by label. Both halves were wrong, and the
reviewer flagged that the wrong version would lead someone to conclude the sort is redundant and
remove it, reintroducing the defect. The truth:

- **`class` is a `str` column** — `labels` is the `u8` code. `.sort("class")` therefore sorts
  *alphabetically*, which is exactly why the order matches pandas: `groupby("class")` sorts string
  keys alphabetically too. There is no coincidence to explain.
- **The layout does not order facets by label.** `px.imshow(facet_col=0)` orders facets by array
  index — that is, by data row position — and `for_each_annotation` then overwrites each label by
  positional lookup. The proof is the pre-fix output: identical labelling code, scattered grid. The
  grouping comes from `.sort("class")` on the frame, and nothing else.

Two smaller fixes in the same pass: `pl.exclude` is now named in the prose — it appears in this
chapter and **nowhere else in the book**, so a student had a pattern to copy but no term to search
for — and a sentence that stated "subtract the mean from each column" three different ways lost its
third.

### The sign flip — found only when `_pca_2` was converted, after `pca` was already marked DONE

**Row order fixes the sign of every principal component, and the conversion changed row order.**
`pivot_table` returned members sorted; Polars' `pivot` returns them in order of first appearance
(`A000374` first). The centred matrix is the same either way — `max|A_sorted − pandas| = 0.0` — but
the row permutation flips LAPACK's sign choice:

```
member-sorted (baseline)   vt[0][:4] = [-0.028833 -0.113373 -0.184168 -0.183628]
appearance order (shipped) vt[0][:4] = [ 0.028833  0.113373  0.184168  0.183628]
```

Not environmental (the pandas frame in this env still gives the baseline sign) and not
nondeterministic (stable across runs and thread counts). **The live biplot became the mirror image of
the chapter's static figures of the same data.** Democrats moved to positive PC1 and Republicans to
negative, all 20 loading arrows were negated, and the PC1 bar chart flipped which party facet it
correlates with — +0.9998 against Democrat where it had been Republican.

**Two static images were contradicted, not one.** `images/slide17_2.png` is the biplot the prose walks
through arrow by arrow (*"the purple arrow labeled '520' here… we would infer that $v_1$ is
positive"*). Separately, `images/pca_plot.png` carries the orientation **in its alt text** — "blue for
Democrat (on the left of the graph), red for Republican (on the right side)". That second one is the
sharper failure: a screen-reader user would have been told left-and-right while the figure beside it
showed the opposite, and no gate reads alt text against pixels.

Fixed with `.sort("member")` on the pivot in **both chapters and both dropdown mirrors**. Verified
after rebuilding: PC1 sums by party are now identical to the baseline
(`Republican, M +525.3 … Democrat, F −217.6`), so the live figure agrees with the slide again.

**The justification is agreement with the figures the section analyses, not agreement with pandas** —
the same class of reason as `sort_columns=True`, and the mechanism is in an inline comment so a
reviewer does not strip it as cosmetic. (`member` has no nulls, 441/441, so no `nulls_last` is
needed.)

A side effect worth recording: the sort makes the singular values **literally bit-identical** to the
pandas path (`np.array_equal` True), which they were not before — matching row order restores the
float accumulation order in the column means. The earlier "bit-identical to 8 significant figures"
caveat in this record is now simply "identical".

Two things worth keeping about how this was caught. **It surfaced only because `_pca_2` was converted
after `pca` had already passed review and been marked DONE** — the second chapter's reviewer compared
the live figure against the static slide, which `pca`'s reviewer had not thought to do. And the
chapters are near-identical, so the defect was in both; converting the "redundant" archived chapter is
what found the bug in the live one.

Left for course staff: a sentence noting that a principal component's sign is arbitrary, so a reader
who re-runs the notebook may see the axes mirrored. That is a genuine and teachable fact, but adding
it is editorial rather than conversion work.

### Open items

- **A pre-existing defect left in place:** the biplot dropdown (markdown cell 57) **contains its code
  cell's source twice** — student-visible, ~40 lines pasted twice with a stray `fig` mid-listing.
  True in the baseline, and it is why the mirror gate never registered the pair: the same blind spot
  as harness note 7, arriving by a different route. Both copies were converted identically.
- The Fashion-MNIST `load_data` dropdown closes with 4-space-indented fences, exceeding CommonMark's
  3-space limit for a closing fence. Pre-existing.
- Fashion-MNIST figures redraw with different garments each run — `.shuffle()` carries no `seed=`,
  where the baseline's `.sample(2)` inherited NumPy's seeded global RNG. Open question 7.
- The chapter introduces `.pivot` with an aggregate expression, `.unpivot`, `pl.exclude` and
  `.over()`, and offers **no `docs.pola.rs` link** for any of them. Not a regression — the baseline
  had zero pandas doc links, so nothing was deleted — but one link on the pivot paragraph would be
  cheap and on-outcome.

## eda — Data Cleaning and EDA

Tier C, 1 attempt, debt 0. All 13 gates green. 110 cells, 54 code cells, **51 carrying output — the
highest output surface in the book**, 48 MB of data, 8 doc links repointed.

### Code changes

- **The `%Y%W%w` date parse had no equivalent and was rebuilt from arithmetic.** chrono rejects that
  format — `2021520` crosses a year boundary — affecting 10 rows. Replaced with "first Monday of the
  year plus `7*(WEEK-1)+6` days", and verified **bit-identical across all 5380 values** against
  `pd.to_datetime(..., format='%Y%W%w')`. This column is the chapter's join key, so an off-by-one
  would have corrupted everything downstream.
- **The whitespace-delimited CO₂ read is the one genuine reshape.** Polars `read_csv` has no regex
  separator and the file is ragged (30–32 space-split fields per line), so `sep=r'\s+'` has no
  argument-level equivalent. Now: read each record whole into one column, split on `\S+`, name the
  fields via `list.to_struct`, unnest, cast. Matches the committed pandas output exactly — 738×7,
  with `-99.99` preserved.
- `dt.to_period("M").dt.to_timestamp()` → `dt.truncate("1mo")`; join keys line up at 1820 rows.
- `.merge(...)` → `.join(...)`; `value_counts().sort_index()` and `groupby('Yr').mean()` given
  explicit sorts, since Polars guarantees no order and both feed plots.
- The naive ILINet read needs `truncate_ragged_lines=True` or it raises — which G9 would have flagged
  as a *new* error. With the flag it reproduces the pandas teaching moment: 5381 rows, one column,
  labelled with the title line.

### Accepted behaviour differences

- **`.dt.dayofweek` → `.dt.weekday()`: Monday 0–6 becomes Monday 1–7.** Sample values shift
  `3,3,0,5,0` → `4,4,1,6,1`. Nothing downstream keys on the number and the prose now states the
  convention. The new values coincide with the dataset's own `CVDOW` column *except on Sundays* —
  noted but deliberately not claimed as equal.
- **The join lost two columns, 22 → 20.** Polars coalesces the right-side join keys, so `HHS Region`
  and `month_dt` do not survive and the figure's `hue` moved to `REGION`. Row count is unchanged at
  1820. A sentence about key-folding was added rather than passing `coalesce=False` to reproduce the
  pandas shape.
- `week_start` is a `Date`, not `datetime64[ns]`; the `<M8[ns]`/nanoseconds paragraph was rewritten.
- **`NaN` → `null` throughout the prose**, including a section heading and a figure panel title
  ("2. Missing Set to Null"), both halves of the mirrored dropdown changed together. Polars
  distinguishes `null` from `NaN`, and this chapter is *about* missing data, so the distinction is
  load-bearing rather than terminological.

### The deliberate error was retired, by a course-staff decision

Cell `a3fde967` raised `ValueError: Mixing dicts with non-Series may lead to ambiguous ordering` from
`pd.read_json`, and the section existed to show that failure. **Polars has no equivalent failure:**
`pl.read_json` reads this file fine, returning `(1, 3)` with all **54** members packed into one
`list[struct]` cell.

The first conversion kept a raising cell by switching to `pl.read_ndjson`, which fails only because
the file is not newline-delimited. **Both reviewers independently flagged that as the chapter's
weakest seam** — it demonstrates a format mismatch rather than the structural point the section is
about, and it calls `read_ndjson` a "reasonable first guess" eight cells after the chapter has
already shown `read_json` working on `elections.json`. Worse, the interesting lesson was left
asserted in a bullet and never shown.

Course staff chose to show `pl.read_json` succeeding instead. The cell now displays the
rectangularized `(1, 3)` result, and the prose reads it: the whole object was flattened, `pagination`
and `request` sit beside `members`, and a row is one API response where it should be one member of
Congress — which is exactly why the chapter goes on to build from `congress_json['members']`.
`read_ndjson` survives as a one-sentence aside with its documentation link.

Three things this buys, beyond a better demo: it redeems cell `e438f962`'s forward reference ("we'll
see the implications of this inconsistency in the next section") with **executed output** rather than
prose; it gives the `.struct` paragraph three cells later the setup it previously lacked; and it
teaches the more valuable failure mode — a reader who meets silent wrong granularity is better served
than one who meets a loud exception, because silence is what they will actually encounter.

The cost, recorded honestly: **the chapter now has no cell that raises at all**, and "reading a file
can fail" is worth a student seeing once. That was the trade staff made.

Recorded in `conversion/conversion_allowlist.yml` under `eda: resolved_errors:`, which is the
sanctioned path — G9's own failure text names the hazard it guards against ("the prose around it
describes an error the reader will not see"), and that hazard does not arise here precisely because
the prose was rewritten to describe a result. G9 now reports `0 erroring cell(s), matching the
baseline's 1` and passes on the entry.

### Constants changed

None quoted in prose moved. Verified against the regenerated outputs: 15 columns after
`skip_rows=1`; the naive ILINet read at `(5381, 1)`; 738 months with 7 null `Avg` (<1%); the
Jan/Feb/Sep/Oct/Nov/Dec 61-vs-62 split unchanged; `ili_vax` at 1820 rows.

### Cross-chapter obligation, discharged

The heading became **"Temporality with the `polars` `dt` namespace"**, anchor
`#temporality-with-the-polars-dt-namespace`, verified in `_build/html/eda.json` rather than derived
from the heading text. `regex` was repointed at it and rebuilt in the same pass. See open question 9.

## regex — Regular Expressions

Tier B, `DONE`. 21 substitutions, 2 attempts, debt 5 → 0. All 13 gates green.
Pilot chapter: chosen because it is small, reads 12 KB of data, needs no network, and has one
dropdown mirror — enough to exercise the whole pipeline in about a minute per iteration.

### Code changes

- `import pandas as pd` → `import polars as pl`; both `pd.read_csv(f)` calls → `pl.read_csv(f)`.
  Polars reads from an open file handle directly, so the surrounding `with open(...)` blocks are
  unchanged — worth keeping, since the chapter's subject is text handling.
- `canonicalize_county_series`: `.str.lower()` → `.str.to_lowercase()`, and all five
  `.str.replace(...)` → `.str.replace_all(..., literal=True)`. **Both halves of that are load-bearing.**
  Polars `.str.replace()` replaces only the first match where pandas replaced all, and
  `.str.replace_all('.', '')` without `literal=True` reads `.` as a regex and returns empty strings
  for every row. Verified live: `['stjohnthebaptist', 'dewitt', 'lacquiparle']` with the flag,
  `['', '', '']` without it.
- Column assignment → `with_columns`, and the column renamed `clean_county_pandas` →
  `clean_county_polars`.
- `pd.DataFrame(data)` → `pl.DataFrame(data)` in both `html_data` and `ssn_data`.
- `.str.replace(pattern, '', regex=True)` → `.str.replace_all(pattern, '')` — regex is the Polars
  default, so the keyword disappears rather than being translated.
- `.str.findall(pattern)` → `.str.extract_all(pattern)`.
- `.str.extract` / `.str.extractall` → `.str.extract_groups`, with the capture groups **named** in the
  pattern (`(?<area>...)`) so the struct fields carry meaning.

### Accepted behaviour differences

- `extract_all` returns a `list[str]` column: the row for `"forty"` is an empty list where pandas
  gave an empty list too, but the column type is now visibly a list. The prose says so.
- `extract_groups` returns a **struct**, and `.struct.unnest()` spreads it into columns. pandas
  numbered the columns `0, 1, 2`; the named groups produce `area`, `group`, `serial`.
- No constants changed — this chapter quotes no numbers from its outputs.

### Prose re-authored

- The Python-vs-library string-methods table: the `Pandas (Series)` column became `Polars (Series)`
  with the real method names (`to_lowercase`, `replace_all`, `slice`, `len_chars`). Two rows needed
  more than a rename, so a short paragraph was added under the table: `str.slice` takes a **length**,
  not a stop, and `replace_all` treats its pattern as a regex by default. Both are genuine Polars
  behaviours and both are on-topic in a chapter about regular expressions.
- "Canonicalization with Pandas Series Methods" → "with Polars Series Methods". The old paragraph's
  point was that the method names match Python's built-ins — which is no longer true, so the
  paragraph now makes the opposite and more useful point: the Polars names are more explicit, and
  `replace_all` says what it does.
- The `extract`/`extractall` passage leaned on a **multi-indexed DataFrame**, which Polars has no
  equivalent for and no reason to want. Re-aimed at the two structures Polars actually returns —
  struct columns and list columns — both of which the rest of the course builds on. This is the one
  section that was restructured rather than translated.
- `.str` described as a **namespace** rather than an accessor, matching Polars' own vocabulary.
- Learning-outcome bullet, two section headings, and the summary bullet updated.

### Defects found and fixed during conversion

- **Prose/output order mismatch.** The rewritten passage introduces the struct first and
  `.struct.unnest()` second, but the two cells showed the unnested frame first. Caught on review,
  fixed by swapping the two cell *sources* — the cell ids and their order are untouched, so the
  structure gate stays green. This is exactly the category the output reviewer exists for: every gate
  passed while the page contradicted itself.

### Review

`notes-output-reviewer`: **BLOCK** on attempt 1 (the ordering defect above), **PASS** on attempt 2.
No prose reviewer — tier B. No a11y reviewer — the chapter has no figures.

### Open items

- **Cross-chapter link.** The `.str` namespace note links to
  `https://ds100.org/course-notes/eda/#temporality-with-pandas-dt-accessors`. That anchor is
  generated from a heading in the `eda` chapter which will change when `eda` is converted, breaking
  this link. It is an absolute URL to the published site, not a MyST cross-reference, so **no gate in
  this harness can catch it.** Whoever converts `eda` must update this link in `regex` in the same
  pass. Recorded as open question 8 below.

# Harness build notes

The first three were vacuous-pass bugs caught by building the negative control first, and all three
are the kind that stay green forever once shipped. The fourth is the opposite case, recorded because
it is what a guard working correctly looks like from the inside.

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

3. **`class="dataframe"` is not a pandas marker.** Both gates used it to detect a stale pandas HTML
   repr. **Polars puts the same class on its own HTML table**, so the detector fired on correctly
   converted output — the `regex` pilot failed `outputs-fresh` on two cells that were perfectly
   converted, and `site-build` could never have reached zero no matter how much was converted. The
   real discriminator is where the two libraries put the alignment style: pandas writes
   `<tr style="text-align: right;">` inline on the header row, polars puts it in a `<style>` block
   and prefixes the table with `<small>shape: (R, C)</small>`. Both gates now key on that, and the
   recorded baseline count fell from 294 to **146** once it was measuring the right thing.

4. **The markdown fence detector was wrong in both directions, and the dangerous direction was
   silent.** `MD_CODE_FENCE` paired an opening fence with a closing one using a lazy regex whose
   language tag was optional — so a *closing* ` ``` ` matched as an opening one. Two consequences,
   found while converting `_case_study_climate`:

   *False positives.* In a chapter built from ` ```{image} ` blocks — whose openers the pattern
   correctly ignores — it paired each block's closer with the next block's closer and scanned the
   **prose in between** as if it were code. That reported a narrative sentence about xarray's
   `.groupby()` as an unconverted pandas site, in a chapter with no pandas in it at all.

   *False negatives, which matter more.* `finditer` does not overlap, so one mispairing consumed the
   text after it and skipped real blocks. `modeling_slr` scanned as **1** fenced pandas site when it
   has **5**; `eda` as 1 when it has 2. A missed fenced block means G3 reports a chapter clean while
   the published page still shows pandas — precisely the vacuous pass this battery exists to catch,
   and it would have stayed green forever.

   Replaced with `markdown_code_blocks()`, a stack-based scanner following CommonMark: a fence closes
   only on a run at least as long as the one that opened it *and* an empty info string. That is what
   makes the repo's 4-backtick ` ```{dropdown} ` wrap a 3-backtick ` ```python ` correctly — the inner
   fence cannot close the outer one. Verified on that exact nesting, then across the book: the
   baseline carries **105** mirror sites.

   Two chapters re-tier as a result. **`sql_II` and `_case_study_climate` drop from B to A** — their
   only "sites" were phantoms, so both are verify-only and both pass `unchanged`. Tier A goes 6 → 8,
   tier B 18 → 16. This also dissolves open question 6: `sql_II` needs no conversion, so the absent
   `imdb_duck.db` no longer blocks anything.

   The lesson is the mirror of the first three. Those were detectors that found nothing and were
   believed; this one *found something*, and the finding was wrong in a way that made the counts look
   plausible. A detector needs testing against the structure it will actually meet — here, nested
   fences and directive blocks — not just against a positive and a negative case.

5. **`baseline.lock` shipped pinning a converter that had already moved.** The lock recorded
   `converter_sha: 9ed6a4a3036f` while `nb_pytext.py` as committed hashed to `1a27d5e2b015` — the
   lock was captured mid-session and both were committed together in the harness commit. The guard
   worked exactly as designed: `nb_baseline.py` refused to materialize anything and said to run
   `--refresh`. Two things made this cheap rather than expensive. The cache key is
   `<main_sha>-<converter_sha>`, so the stale and fresh baselines live in different directories and
   could never be silently mixed; and the digest check runs only in `main()`, so `nb_validate.py`
   kept working throughout — the guard blocks new baselines rather than freezing the harness.
   Re-pinned with `--refresh --sha 887a578b...`, which held the baseline commit fixed and moved only
   the converter digest. `regex` and the `--all --self-test` negative control were both re-run
   afterward and stayed green, which is what proves the re-pin changed nothing but the cache path.
   The old writer is not recoverable from git — `887a578b` predates the file — so refreshing was the
   only path forward, not a preference.

6. **The alt-text gate could not see an empty alt.** `gate_alt_text` tested `m.group(1).strip()`, but
   `:alt:""` captures the two literal quote characters, which strip to a two-character string and
   read as present. So the gate reported "12 {image} + 2 fig-alt, **all non-empty**" on
   `gradient_descent`, which carries three empty alts. A presence gate that cannot see an absence is
   the same failure as a removal gate that cannot see a survivor. Fixed with `alt_is_empty()`, which
   strips quotes as well as whitespace.

   The fix also had to avoid a second mistake. Those three empties are in the **baseline** — failing
   the conversion for content debt it inherited would block work on a defect it did not cause. So the
   gate now counts empties on both sides and fails only when the conversion *emptied* one, reporting
   the inherited count rather than swallowing it.

7. **The dropdown-mirror gate was checking 96 of 101 pairs, and the 5 it missed it could never have
   found.** Pairs are registered by exact equality between a dropdown's body and the next code cell's
   source. But a code cell often opens with `#| fig-alt: ...` that its dropdown copy omits — the
   directive configures the cell, it is not part of the code being shown. Those pairs therefore never
   entered the pair list at all, and **an unregistered pair is never checked**: 4 of `modeling_slr`'s
   5 mirrors and 1 of `visualization_1`'s were invisible to the gate whose own docstring calls this
   "the single highest-probability silent defect here."

   Because the pair list is built from the baseline, the miss was permanent — not something a
   conversion could trip and not something a retry would surface. `modeling_slr` shipped through this
   batch with the gate reporting a confident `1/1`. Its output reviewer compared all six by hand and
   found them correct, which is luck plus a good reviewer, not a working gate. Fixed with
   `mirror_normalize()`, which drops `#|` directive lines on both sides; `#| fig-alt` content is not
   going unchecked, since G12 owns it.

8. **`no-pandas-code` fires on NumPy, and this is the one incident where the gate erring is
   *acceptable*.** `PANDAS_ONLY` is a line regex, so it cannot see the receiver: it matches
   `.astype(` and `.tolist(` whether they sit on a pandas object or a NumPy array. In `pca` it
   flagged `train_images[sample_idx].astype(np.int16)` and `img_mat.tolist()`, neither of which was
   ever pandas, and the converter rewrote both to satisfy it.

   Verified directly — `.astype(` on a NumPy receiver matches, `np.mean(arr, axis=0)` does not, and
   Polars' `.cast()` does not.

   **Left unfixed deliberately**, because the two error directions are not symmetric. A false
   positive costs one rewrite of working code and is visible to whoever makes it. A false negative
   ships pandas into a published textbook with every gate green — which is the entire failure mode
   this harness exists to prevent. `.astype(` is also a genuinely strong pandas signal in a converted
   chapter, since Polars spells it `.cast()`. Loosening the pattern to check the receiver would need
   real parsing, and would trade a cheap, loud failure for a silent one.

   Worth knowing when reading a conversion diff: **not every change a converter makes to
   NumPy-looking code is gratuitous.** In `pca` both rewrites were improvements anyway — passing the
   3D array straight to `pl.DataFrame` types the column as a real `Array(f64, (28,28))`, which is
   what let `images["images"].to_numpy()` replace `np.array(….to_list())` at two later sites.

The general rule the first three incidents support: **a detector that reports zero is only good news if it
found something on the baseline** — and a detector that reports a hit is only bad news if it cannot
also fire on the correct answer. Every removal gate here is paired with the first check; the third
incident is what added the second.

# Open questions for course staff

1. **`content/_pca_2/` duplicates `content/pca/` — recommend deletion, but it will be converted
   anyway at the back of the queue.** Course staff have set the priority rule: **what ships in
   `myst.yml`'s TOC comes first, along with anything a shipping notebook depends on.** `_pca_2` is
   still in scope, just last.

   The evidence for deletion, gathered rather than assumed:

   - All four `_`-prefixed chapters were created in **one commit** — `4f842ef7` "jb2 and no duckdb
     headache", 2026-01-09 — and **none has been touched since**. It is a bulk archive snapshot, not
     maintained content.
   - `content/pca` has had **five commits in that window**, including "PCA Notes update", "PCA Note
     Ready" and "Change dates to Spring 26". None of those propagated to `_pca_2`.
   - Titles say it outright: `pca` is **"PCA"**, while `_pca_1`/`_pca_2` are **"PCA I (Summer 2025)"**
     and **"PCA II (Summer 2025)"** — the old two-part lecture, superseded by the merged chapter.
     Cell counts agree (19 + 69 ≈ 82), and **27 of `_pca_2`'s 36 headings already appear in `pca`**.
   - The two share **zero cell ids**, so they have fully diverged; the 31 MB data directory is
     byte-identical to `pca`'s; and nothing anywhere references `_pca_2` outside this conversion's
     own bookkeeping.

   **There is nothing deletion would lose. The earlier draft of this record was wrong on exactly
   this point, and the correction removes the only argument against deleting.**

   That draft said the 9 headings not carried into `pca` were unique linear-algebra scaffolding —
   covariance matrix, orthonormality, diagonal matrices — and that they existed "here and nowhere
   else". They do not. **All three are in the live `pca` chapter**, in cell `57d541ec`, written as
   `::: {tip} [Linear Algebra Review] …` admonitions rather than `###` headings. The comparison that
   produced the wrong answer counted only `#`-prefixed headings, so it could not see content
   formatted as an admonition — a reminder that a structural diff is only as good as its notion of
   structure.

   `pca` in fact carries **more** of this material than `_pca_2` does: it adds "Linear Algebra
   Review: Matrix Multiplication", "SVD: Geometric Perspective" and a "[Summary] Terminology" block
   that `_pca_2` has no counterpart for. 39 of `_pca_2`'s 43 headings are shared with `pca`, and the
   remaining 4 are these admonition-formatted duplicates.

   Two further findings from converting it, both pointing the same way:

   - `_pca_2` writes those blocks as `::: {.callout-tip}` with an `###` heading inside — **quarto-era
     syntax that MyST does not render as an admonition** (3 occurrences). So even the duplicated
     material is in worse shape here than in `pca`.
   - All 19 `{image}` directives carry **no `:alt:`**, and the chapter says so itself in cell
     `b910225f`: "alt text must be added to images before this page can be published." If the chapter
     is kept rather than deleted, that is its blocker — and it is authoring work, not conversion.

   Note that leaving `_pca_2` unconverted **blocks no gate**: it is absent from the TOC, so it is
   never built and G15 cannot see it. The only cost is the "no pandas anywhere under `content/`"
   goal.

2. **The `pandas_1/2/3` concept diagrams.** `images/gb.png`, `agg.png`, `pivot.png`, and the `.loc`
   graphic draw pandas semantics — index alignment, the GroupBy object, hierarchical pivot columns.
   No agent can redraw them. Which are still accurate for Polars, which need redrawing, and which
   should go?
3. **Renaming `pandas_1/2/3` changes their published URLs** (`/pandas-1` → `/polars-1`). Does anything
   outside this repo link to them — a syllabus, a Piazza post, an assignment?
4. ~~**`content/eda/ds100_utils.py` is dead.**~~ **Half-answered, and narrower than it looked.** It is
   the **only** `.py` file under `content/`, and it contains **no pandas at all** — it imports just
   `requests`, `pathlib`, `time` and `itertools`. So it was never a conversion question, only a
   dead-code one: delete it, or reconnect the inline copies to it? That half is still for staff.

   Checked explicitly rather than assumed, because **helper modules are invisible to every gate in
   this harness** — the battery walks chapters, not the import graph. A shipping notebook that
   imported a pandas-carrying `utils.py` would leave pandas in the published book with all 15 gates
   green. There is no such file in this repo, and now that is on the record.
5. **`content/pandas_3/babynamesbystate.zip` sits outside `data/`** — a 22 MB duplicate of
   `content/pandas_3/data/babynamesbystate.zip`. Safe to delete?
6. **`content/sql_II/data/imdb_duck.db` is gitignored and absent**, so `sql_II` cannot be executed
   locally. It has no pandas in its code cells, so the conversion does not need to run it — but no
   one can verify its outputs either. Is that acceptable, or should the file be made available?
7. **44 randomness sites are covered by only 10 `seed()` calls.** Under full re-execution the
   unseeded ones produce different numbers on every build, and any prose quoting them goes stale
   silently. Should the conversion add seeds, or is the churn acceptable?
8. ~~**`_decision_tree` roots on a coin flip.**~~ **RESOLVED** — see the `_decision_tree` record.
   Both `DecisionTreeClassifier(criterion='entropy')` constructors are now pinned with
   `random_state=42`, and the prose threshold is corrected. Left here because the *general* version
   of the question — question 7 — is still open, and because the reasoning is worth keeping: a
   sentence naming a specific split cannot be made durable by editing the sentence.

9. **Absolute intra-site links — the `regex` → `eda` instance is now RESOLVED, the general question
   stands.** `eda`'s heading became "Temporality with the `polars` `dt` namespace", so the anchor is
   `#temporality-with-the-polars-dt-namespace`. `regex` was repointed at it in the same batch and
   rebuilt. The anchor was **verified in the built page** (`_build/html/eda.json`) rather than
   derived from the heading text, because deriving a slug is exactly the step that silently produces
   a dead link.

   The handoff worked because it was made an explicit deliverable: the `eda` converter was told to
   report its chosen heading and *not* to touch `regex`, so the dependency was carried by the
   orchestrator rather than left to two agents that cannot see each other. That is the pattern for
   the remaining instances — **no gate can see any of them.**

   Worth noting the vocabulary now agrees across chapters by design: `regex` says "`.str` is a
   **namespace**, similar to the `.dt` namespace", so `eda` uses "namespace" rather than "accessors".

   The original question, unchanged: `regex` links
   to `https://ds100.org/course-notes/eda/#temporality-with-pandas-dt-accessors`; that anchor dies
   when `eda` is converted. These are absolute URLs to the published site rather than MyST
   cross-references, so nothing checks them. There are a handful across the book — should they be
   converted to MyST cross-references (`(label)=` targets), which *would* be checkable, as part of
   this work or as a separate pass?
