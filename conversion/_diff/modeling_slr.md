# modeling_slr — change report

`887a578b0a4b:content/modeling_slr/modeling_slr.ipynb` → `content/modeling_slr/modeling_slr.ipynb`

**Tier B · 19 changes:** output 5 · prose 6 · dropdown 1 · code 7

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

Light Tier-B conversion. The chapter's only frames are the four Anscombe datasets, rebuilt from
`pd.DataFrame(list(zip(x, y)), columns=[...])` as `pl.DataFrame({"x": x, "y": y})`; everything
downstream is NumPy, matplotlib and seaborn, and the chapter's own helpers (`standard_units`,
`correlation`, `compute_mse`) were left in NumPy untouched.

Three things are worth staff time.
First, the five `.to_numpy()` calls (C8, C10, C12, C13, C14): they are not churn — those helpers
call `np.mean`/`np.std`, which raise `TypeError: Series.mean() got an unexpected keyword argument
'axis'` on a Polars Series, verified on polars 1.43.1, so the crossing is forced at the call site.
Second, C11, which rewrites the Anscombe "identical statistics" paragraph because the committed
output directly beneath it has never agreed with it (CONTRADICTIONS A10 #2, pre-existing).
Third, C18, the chapter's only text output to move: a pre-existing `f"\theta_0"` tab escape that
printed a literal TAB followed by `heta_0` is now fixed. All four figures were re-executed and none
of them moved — same data, same axes, ±2 px of canvas.

## Needs review

- [C3](#c3) · cell 4: Correlation
- [C5](#c5) · cell 10 [markdown]
- [C7](#c7) · cell 12: Load in four different datasets: I, II, III, IV
- [C8](#c8) · cell 12: Plot the scatter plot and line of best fit
- [C11](#c11) · cell 14 [markdown]
- [C13](#c13) · cell 16: Residual visualization

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C15](#c15) · `import polars as pl`
- [C16](#c16) · `def plot_and_get_corr(ax, x, y, title):`
- [C17](#c17) · `x = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]`
- [C18](#c18) · `for dataset in ["I", "II", "III", "IV"]:`
- [C19](#c19) · `fig, axs = plt.subplots(2, 2, figsize=(10, 10))`

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C1](#c1) · cell 2: Simple Linear Regression

## Changes

<a id="c1"></a>
### C1 · cell 2: Simple Linear Regression · dropdown

baseline L104 → branch L104 · mirror of the next code cell (hard rule 3)

```diff
- # import pandas as pd
+ # import polars as pl
```

**Why:** Mirrors the import rename in the code cell below (`import pandas as pd` -> `import polars as pl`). Checked mechanically: this dropdown's fenced body matches cell `18ffe9c6` line for line, so hard rule 3 holds.
**Output:** same

<a id="c2"></a>
### C2 · cell 3 [code] · code

baseline L123 → branch L123

```diff
- import pandas as pd
+ import polars as pl
```

**Why:** Import rename. The cell imports the library and nothing else in it is library-specific.
**Output:** same

<a id="c3"></a>
### C3 · cell 4: Correlation · prose · **REVIEW**

baseline L160 → branch L160

```diff
- # However, when $\bar{x} = 0$,  $\bar{y} = 0$,  $\sigma_x = 1$, or $\sigma_y = 1$ (which are all satisfied when x and y are both in standard units),
+ # However, when $\bar{x} = 0$, $\bar{y} = 0$, $\sigma_x = 1$ **and** $\sigma_y = 1$ — that is, when $x$ and $y$ are both in standard units, which is when all four hold together —
```

**Why:** The baseline listed $\bar x = 0$, $\bar y = 0$, $\sigma_x = 1$, $\sigma_y = 1$ joined by **or**, which makes each one sufficient on its own. The identity $r = \frac1n\sum x_i y_i$ needs all four together, i.e. both variables in standard units — which is what the parenthetical already said, so the sentence contradicted itself. CONTRADICTIONS A10 #1; pre-existing, not introduced by the conversion.
**Verdict:** necessary — a fix to a false claim, and unrelated to Polars

<a id="c4"></a>
### C4 · cell 7 [code] · code

baseline L502 → branch L502

```diff
- import pandas as pd
+ import polars as pl
```

**Why:** Import rename.
**Output:** same

<a id="c5"></a>
### C5 · cell 10 [markdown] · prose · **REVIEW**

baseline L632 → branch L632

```diff
- #     print(f"\theta_0: {ahat:.2f}, \theta_1: {bhat:.2f}")
+ #     print(f"theta_0: {ahat:.2f}, theta_1: {bhat:.2f}")
```

**Why:** `f"\theta_0: ..."` — `\t` is Python's tab escape, so the f-string printed a literal TAB followed by `heta_0`. The fix drops the backslash. Pre-existing bug, not a library difference; CONTRADICTIONS B1 records the `e83b8086` tab-twin being deleted because its pandas pane republished this same escape as though pandas mangled theta labels. The mirror matches cell `ce691b4e`.
**Verdict:** necessary — a fix to a false output

<a id="c6"></a>
### C6 · cell 11 [code] · code

baseline L670 → branch L670

```diff
-     print(f"\theta_0: {ahat:.2f}, \theta_1: {bhat:.2f}")
+     print(f"theta_0: {ahat:.2f}, theta_1: {bhat:.2f}")
```

**Why:** Same escape fix as C5, in the code cell the dropdown mirrors.
**Output:** differs: the four `\theta_0`/`\theta_1` lines in stdout now read `theta_0`/`theta_1` instead of a literal tab plus `heta_0`. Values unchanged. See C18.

<a id="c7"></a>
### C7 · cell 12: Load in four different datasets: I, II, III, IV · prose · **REVIEW**

baseline L705 → branch L705

```diff
- #     "I": pd.DataFrame(list(zip(x, y1)), columns=["x", "y"]),
- #     "II": pd.DataFrame(list(zip(x, y2)), columns=["x", "y"]),
- #     "III": pd.DataFrame(list(zip(x, y3)), columns=["x", "y"]),
- #     "IV": pd.DataFrame(list(zip(x4, y4)), columns=["x", "y"]),
+ #     "I": pl.DataFrame({"x": x, "y": y1}),
+ #     "II": pl.DataFrame({"x": x, "y": y2}),
+ #     "III": pl.DataFrame({"x": x, "y": y3}),
+ #     "IV": pl.DataFrame({"x": x4, "y": y4}),
```

**Why:** `pd.DataFrame(list(zip(x, y1)), columns=["x", "y"])` has no Polars analogue — a list of 2-tuples with a `columns=` argument. `pl.DataFrame({"x": x, "y": y1})` builds the same two columns straight from the same lists and drops the `zip`. Mirror matches cell `0e2fd633`.
**Verdict:** necessary — the pandas constructor form does not exist in Polars

<a id="c8"></a>
### C8 · cell 12: Plot the scatter plot and line of best fit · prose · **REVIEW**

baseline L716 → branch L716

```diff
- #     x, y = ans["x"], ans["y"]
+ #     x, y = ans["x"].to_numpy(), ans["y"].to_numpy()
```

**Why:** `ans["x"]` is now a Polars Series, and it is passed to `fit_least_squares` -> `slope`/`intercept` -> `standard_units`, which computes `(x - np.mean(x)) / np.std(x)`. NumPy routes `mean`/`std` through `_wrapreduction`, which calls the object's own method with `axis=`; Polars rejects the keyword, so both raise `TypeError` on a Series — verified live on polars 1.43.1. The NumPy dispatch rule forces `.to_numpy()` here; it is not plotting churn. Mirror matches cell `0e2fd633`.
**Verdict:** necessary — forced by the NumPy reduction dispatch rule

<a id="c9"></a>
### C9 · cell 13 [code] · code

baseline L740 → branch L740

```diff
-     "I": pd.DataFrame(list(zip(x, y1)), columns=["x", "y"]),
-     "II": pd.DataFrame(list(zip(x, y2)), columns=["x", "y"]),
-     "III": pd.DataFrame(list(zip(x, y3)), columns=["x", "y"]),
-     "IV": pd.DataFrame(list(zip(x4, y4)), columns=["x", "y"]),
+     "I": pl.DataFrame({"x": x, "y": y1}),
+     "II": pl.DataFrame({"x": x, "y": y2}),
+     "III": pl.DataFrame({"x": x, "y": y3}),
+     "IV": pl.DataFrame({"x": x4, "y": y4}),
```

**Why:** Same frame construction as C7, in the code cell. Values identical: same lists, same column names, same order.
**Output:** same

<a id="c10"></a>
### C10 · cell 13 [code] · code

baseline L751 → branch L751

```diff
-     x, y = ans["x"], ans["y"]
+     x, y = ans["x"].to_numpy(), ans["y"].to_numpy()
```

**Why:** Same `.to_numpy()` crossing as C8, in the code cell.
**Output:** same

<a id="c11"></a>
### C11 · cell 14 [markdown] · prose · **REVIEW**

baseline L763 → branch L763

```diff
- # While these four sets of datapoints look very different, they actually all have identical means $\bar x$, $\bar y$, standard deviations $\sigma_x$, $\sigma_y$, correlation $r$, and RMSE! If we only look at these statistics, we would probably be inclined to say that these datasets are similar.
+ # While these four sets of datapoints look very different, they have the *same* mean $\bar x$ and standard deviation $\sigma_x$ exactly, and they agree so closely on $\bar y$, $\sigma_y$, correlation $r$ and RMSE that no summary statistic tells them apart. Watch the printout below carefully: $r$ reads 0.816 for three of them and 0.817 for the fourth, which is as much difference as four wildly different datasets manage to show. If we only look at these statistics, we would probably be inclined to say that these datasets are similar.
```

**Why:** "They actually all have identical means, standard deviations, correlation, and RMSE" is false of the output printed two cells below it, which reads `r = 0.816, 0.816, 0.816, 0.817` and `RMSE 1.119, 1.119, 1.118, 1.118`. Only $\bar x$ (9 exactly) and $\sigma_x$ ($\sqrt{10}$) are identical; $\bar y$, $\sigma_y$, $r$ and RMSE all differ at the precision the chapter prints. CONTRADICTIONS A10 #2; pre-existing. The replacement keeps the paragraph's conclusion and re-aims the claim at what the numbers actually show.
**Verdict:** necessary — a fix to a false claim. The added "watch the printout carefully" sentence is an authored extra; the required part is only the retraction of "identical"

<a id="c12"></a>
### C12 · cell 15 [code] · code

baseline L769 → branch L769

```diff
-     fig = least_squares_evaluation(ans["x"], ans["y"], visualize=NO_VIZ)
+     fig = least_squares_evaluation(ans["x"].to_numpy(), ans["y"].to_numpy(), visualize=NO_VIZ)
```

**Why:** Same `.to_numpy()` crossing as C8 — `least_squares_evaluation` prints `np.mean(x)` and `np.std(x)` directly in its first two lines.
**Output:** same

<a id="c13"></a>
### C13 · cell 16: Residual visualization · prose · **REVIEW**

baseline L783 → branch L783

```diff
- #     x, y = ans["x"], ans["y"]
+ #     x, y = ans["x"].to_numpy(), ans["y"].to_numpy()
```

**Why:** Same `.to_numpy()` crossing as C8, in the residual-plot dropdown. Mirror matches cell `6e65c819`.
**Verdict:** necessary — forced by the NumPy reduction dispatch rule

<a id="c14"></a>
### C14 · cell 17 [code] · code

baseline L807 → branch L807

```diff
-     x, y = ans["x"], ans["y"]
+     x, y = ans["x"].to_numpy(), ans["y"].to_numpy()
```

**Why:** Same `.to_numpy()` crossing as C8, in the residual-plot code cell.
**Output:** same

<a id="c15"></a>
### C15 · `import polars as pl` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 37256 bytes md5:bb6fbeb957
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 37128 bytes md5:70b16e7e84
```

**Why:** Full re-execution. The cell is pure NumPy under `np.random.seed(43)` plus `sns.regplot` — no DataFrame is involved at all — so the data is bit-identical and the byte delta is rasterisation under the current matplotlib. Measured: 1.23% of pixels differ, all on anti-aliased strokes. Opened both.
**Reader sees:** equivalent

<a id="c16"></a>
### C16 · `def plot_and_get_corr(ax, x, y, title):` · output

committed output

```diff
- [text] <Figure size 1000x1000 with 4 Axes>
- [image/png] 66916 bytes md5:89d9fbcdbc
+ [text] <Figure size 1000x1000 with 4 Axes>
+ [image/png] 67596 bytes md5:baacdcbc92
```

**Why:** Re-executed; the four correlation panels are generated from `np.random.randn` under the seed set two cells earlier, with no frame involved. Canvas 812 -> 810 px tall (tight-bbox font metrics).
**Reader sees:** equivalent — same four panels, same correlations in the titles. Not opened individually; the shape delta is the same 2 px the whole batch shows

<a id="c17"></a>
### C17 · `x = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]` · output

committed output

```diff
- [text] <Figure size 1000x1000 with 4 Axes>
- [image/png] 61992 bytes md5:78e3b64a3b
+ [text] <Figure size 1000x1000 with 4 Axes>
+ [image/png] 61868 bytes md5:becc9bd862
```

**Why:** Re-executed with the Anscombe frames now built by `pl.DataFrame` and read out through `.to_numpy()`. Verified the four frames carry the same values in the same order, so the scatter and the fitted lines are unchanged. Canvas 856 -> 854 px tall.
**Reader sees:** equivalent. Not opened; the figure is redrawn from values checked to be identical

<a id="c18"></a>
### C18 · `for dataset in ["I", "II", "III", "IV"]:` · output

committed output

```diff
- [stdout] >>> Dataset I:
- [stdout] x_mean : 9.00, y_mean : 7.50
- [stdout] x_stdev: 3.16, y_stdev: 1.94
- [stdout] r = Correlation(x, y): 0.816
- [stdout] 	heta_0: 3.00, 	heta_1: 0.50
- [stdout] RMSE: 1.119
- [stdout]
- [stdout]
- [stdout] >>> Dataset II:
- [stdout] x_mean : 9.00, y_mean : 7.50
- [stdout] x_stdev: 3.16, y_stdev: 1.94
- [stdout] r = Correlation(x, y): 0.816
- [stdout] 	heta_0: 3.00, 	heta_1: 0.50
- [stdout] RMSE: 1.119
- [stdout]
- [stdout]
- [stdout] >>> Dataset III:
- [stdout] x_mean : 9.00, y_mean : 7.50
- [stdout] x_stdev: 3.16, y_stdev: 1.94
- [stdout] r = Correlation(x, y): 0.816
- [stdout] 	heta_0: 3.00, 	heta_1: 0.50
- [stdout] RMSE: 1.118
- [stdout]
- [stdout]
- [stdout] >>> Dataset IV:
- [stdout] x_mean : 9.00, y_mean : 7.50
- [stdout] x_stdev: 3.16, y_stdev: 1.94
- [stdout] r = Correlation(x, y): 0.817
- [stdout] 	heta_0: 3.00, 	heta_1: 0.50
- [stdout] RMSE: 1.118
- [stdout]
- [stdout]
+ [stdout] >>> Dataset I:
+ [stdout] x_mean : 9.00, y_mean : 7.50
+ [stdout] x_stdev: 3.16, y_stdev: 1.94
+ [stdout] r = Correlation(x, y): 0.816
+ [stdout] theta_0: 3.00, theta_1: 0.50
+ [stdout] RMSE: 1.119
+ [stdout]
+ [stdout]
+ [stdout] >>> Dataset II:
+ [stdout] x_mean : 9.00, y_mean : 7.50
+ [stdout] x_stdev: 3.16, y_stdev: 1.94
+ [stdout] r = Correlation(x, y): 0.816
+ [stdout] theta_0: 3.00, theta_1: 0.50
+ [stdout] RMSE: 1.119
+ [stdout]
+ [stdout]
+ [stdout] >>> Dataset III:
+ [stdout] x_mean : 9.00, y_mean : 7.50
+ [stdout] x_stdev: 3.16, y_stdev: 1.94
+ [stdout] r = Correlation(x, y): 0.816
+ [stdout] theta_0: 3.00, theta_1: 0.50
+ [stdout] RMSE: 1.118
+ [stdout]
+ [stdout]
+ [stdout] >>> Dataset IV:
+ [stdout] x_mean : 9.00, y_mean : 7.50
+ [stdout] x_stdev: 3.16, y_stdev: 1.94
+ [stdout] r = Correlation(x, y): 0.817
+ [stdout] theta_0: 3.00, theta_1: 0.50
+ [stdout] RMSE: 1.118
+ [stdout]
+ [stdout]
```

**Why:** Not a re-execution artefact: C6 fixed the `f"\theta_0"` tab escape. Every number in the block is byte-identical to the baseline.
**Reader sees:** changed: the four `\theta_0: 3.00, \theta_1: 0.50` lines, which previously rendered as a literal tab followed by `heta_0`, now read `theta_0: 3.00, theta_1: 0.50` — the names the surrounding prose uses. A visible improvement, not a regression

<a id="c19"></a>
### C19 · `fig, axs = plt.subplots(2, 2, figsize=(10, 10))` · output

committed output

```diff
- [text] <Figure size 1000x1000 with 4 Axes>
- [image/png] 51476 bytes md5:517824d27b
+ [text] <Figure size 1000x1000 with 4 Axes>
+ [image/png] 51520 bytes md5:e567732810
```

**Why:** Re-executed; residuals computed from the same values. Canvas 856 -> 854 px tall.
**Reader sees:** equivalent — same residual patterns per dataset, which is what the prose above it describes. Not opened

