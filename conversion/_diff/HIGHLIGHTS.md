# Highlights — items that need a decision

Pulled from the per-chapter reports. Each line links to the change; the report carries the diff, the
reason, and a minimal alternative where one applies. Ordered by what it costs a reader.

## Committed output that does not reproduce

CI builds without executing, so whatever is committed is exactly what ships. These three commit a
table that re-running would not produce.

- [polars_2 C125](polars_2.md#c125): a deliberately unordered `group_by("Year")` table, declared in `OUTPUT_CHURNS`. Run four times in the pinned env it gave four different year sets, none of them the committed one.
- [polars_1 C155](polars_1.md#c155): a committed `unique()` ordering that two runs disagreed on.
- [polars_1 C150 / C152](polars_1.md#c150): two cells that shipped no output in the baseline now commit a random sample.

## Rules the branch does not currently satisfy

- [eda: the retired error demo](eda.md#c12). AGENTS.md hard rule 6 names cell `a3fde967` as a demo that must keep raising. It no longer raises — `pl.read_json` returns a (1, 3) frame — so the chapter's only error demo now survives solely inside the pandas pane of a comparison tab. It rests on an allowlist entry plus a staff decision recorded in CONVERSIONS.md.
- [_case_study_climate C1 / C2](_case_study_climate.md#c1). Tier A's predicate is an empty diff, so any change is by definition the defect. This archived Xarray chapter, which contains no pandas at all, picked up backticks and an added possessive. The reviewer recommends reverting both.

## Claims that are wrong, or newly at risk

- [polars_1 C28 / C149](polars_1.md#c28): a new sentence in a `.describe()` comparison is true of the Polars pane only, and the pandas pane also lacks the row the next paragraph reads from. This is the same defect class `CONTRADICTIONS.md` §B1 documents, but this instance is not yet logged there.
- [polars_2 C46](polars_2.md#c46): the rewrite silently fixed a pre-existing defect that is also not logged. The old text defined the ratio against 2022 while the code used each name's last year present — false for 10,080 of 13,782 names.
- [_decision_tree C4](_decision_tree.md#c4): the stated threshold holds only because of a fixed random seed; an unseeded refit splits on a different feature. The error is pre-existing and unlogged. The same chapter rebinds a model variable in a way that discards the seeded classifier.
- [cv_regularization C7](cv_regularization.md#c7): the LASSO correction denies the claim and then retains the baseline sentence that reasserts it.
- [gradient_descent](gradient_descent.md): CONVERSIONS.md records "Constants changed: None" for this chapter while three constants moved.

## Comparison tabs that mislead

The two-pane tabs are the chapter's claim that two things are the same operation, so a mismatched
pair teaches a false equivalence.

- [polars_2 C74 / C82](polars_2.md#c74): both pandas panes are valid pandas but neither is the pandas the old chapter taught, so the reader is shown a migration from something they never saw. One pane also published an alphabetically sorted table where the Polars side does not sort.
- [polars_1 C66 / C67 / C164](polars_1.md#c66): the two panes show five wholly different rows, caused by tie-breaking rather than by any library difference, and are presented as a library difference.
- [eda C44](eda.md#c44): an unseeded `sample(3)` makes the panes show three different rows. [eda C38 / C105](eda.md#c38): a ragged-line flag makes the Polars pane discard every field but the first, where pandas kept all fourteen.
- [intro_lec C19](intro_lec.md#c19): a pairing `CONTRADICTIONS.md` §B1 already lists as false, kept deliberately.

## Teaching that moved with the output

- [polars_2 C137 / C139](polars_2.md#c137): the nuisance-column lesson lost the artifact it was built on, because the aggregate no longer carries the column of 1.0s.
- [polars_2 C146 / C149](polars_2.md#c146) and [C151](polars_2.md#c151): ordering by best result rather than alphabetically changes which ten parties appear; the group-to-row-label mapping is gone with the index.
- [polars_1 C149](polars_1.md#c149): `describe()` drops pandas' `top` and `freq`, so the sentence naming the most common value and its count is gone.
- [polars_1 C95 / C108 / C110](polars_1.md#c95): the chapter now reads a 182-row elections file ending at 2020 where the old chapter ran through 2024. Already open in CONVERSIONS.md.
- [sampling C32–C35](sampling.md#c32): Polars elides middle columns pandas printed in full, and two columns the section goes on to use vanish from the displayed head.
- [logistic_regression_1 C5](logistic_regression_1.md#c5): hand-rolled bins close on the opposite side from `pd.cut`, moving up to five games per bin and shifting two win rates in the third decimal.
- [visualization_1 C4 / C6](visualization_1.md#c4): a section was deleted and replaced with authored prose plus a cell split.
- [gradient_descent C17](gradient_descent.md#c17): the largest single content change in the tier B set, and arguably belongs against `main` rather than in a conversion branch.

## Not actually the conversion

Worth knowing before anyone spends time on them.

- [pca C79–C81](pca.md#c79) and the `_pca_2` twins: identical for pandas and Polars input when re-run. The movement is this machine's linear-algebra backend on a matrix with a zero singular value.
- [cv_regularization C11 / C14](cv_regularization.md#c11) and [feature_engineering C23](feature_engineering.md#c23): today's pandas in the pinned environment prints the branch's numbers exactly. The baseline's committed outputs carry environment drift.
- Figure byte differences across the figure-heavy chapters are re-render noise; the reviewer pixel-diffed 51 of them and found canvas and anti-aliasing deltas only. Two Fashion-MNIST grids are the exception: all twenty garments redraw.

## What came out clean

- No output anywhere still renders a pandas table. That confirms, independently, the absolute claim `site_gate.py` makes.
- Every dropdown mirror checked matches the code cell it mirrors, so hard rule 3 holds across the branch.
- All seven tier A chapters are byte-identical to the baseline except the archived climate case study noted above.
- The only surviving `.to_pandas()` is the allowlisted `sns.pairplot` call, and it was verified to reject Polars. Every `.to_numpy()` site checked is forced by a NumPy reduction that raises on a Polars Series.

## Scale

| | count |
|---|---|
| chapters | 29 |
| changes | 1058 |
| output changes | 315 |
| prose rewrites reviewed | 225 |
| reader sees: equivalent | 157 |
| reader sees: changed | 71 |
| reader sees: new | 8 |
| verdict: necessary | 134 |
| verdict: optional | 41 |
| verdict: questionable | 16 |

Most prose verdicts trace to `CONTRADICTIONS.md` section A, which is pre-existing course content
rather than conversion work. Staff decide whether those fixes ship inside this branch or as their own
change against `main`.
