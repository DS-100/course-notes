# constant_model_loss_transformations — change report

`887a578b0a4b:content/constant_model_loss_transformations/loss_transformations.ipynb` → `content/constant_model_loss_transformations/loss_transformations.ipynb`

**Tier B · 28 changes:** output 7 · prose 6 · dropdown 7 · code 7 · metadata 1

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

A shallow code conversion carrying a deep content correction. Only four code sites moved
(`pl.read_csv`, `np.mean(series)` -> `.mean()`, `.iloc[:, i]` -> `.to_series(i).to_numpy()`,
`dugongs[col]` -> `.to_numpy()`); everything else in the chapter is NumPy and matplotlib. All six
`.to_numpy()` sites are forced, not churn: the helpers they feed call `np.std` and `np.mean`, which
raise `TypeError: Series.std() got an unexpected keyword argument 'axis'` on a Polars Series
(verified, polars 1.43.1). `dugongs.csv` has no nulls, so nothing changes numerically.

What staff should actually read is the prose block: six of the report's changes (C13-C17, C20, plus
the C21 entry the generator miscategorised as metadata) are fixes to pre-existing false or broken
statements recorded in CONTRADICTIONS A4 — an outlier sentence that described code doing something
else, two alt texts that read the MAE curve's y-value as its x-parameter, a summary-table row that
contradicted the row two above it, a `\|` that silently split a MyST table cell, and a `#` where a
math delimiter belonged. None of them is a Polars question, and CONTRADICTIONS itself records that
four of these were reported fixed once and never written to disk, so they are worth re-checking
against the tree. All seven figures were re-executed and none moved.

## Needs review

- [C13](#c13) · cell 20 [markdown]
- [C14](#c14) · cell 24 [markdown]
- [C15](#c15) · cell 24 [markdown]
- [C16](#c16) · cell 24 [markdown]
- [C17](#c17) · cell 24 [markdown]
- [C20](#c20) · cell 30: Bonus: Calculating Constant Model MSE Using an Algebraic Tri

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C22](#c22) · `plt.style.use('default') # Revert style to default mpl`
- [C23](#c23) · `def mse_linear(theta_0, theta_1, data_linear):`
- [C24](#c24) · `sns.set_theme()`
- [C25](#c25) · `sns.set_theme()`
- [C26](#c26) · `x = dugongs["Length"].to_numpy()`
- [C27](#c27) · `z = np.log(y)`
- [C28](#c28) · `plt.figure(dpi=120, figsize=(4, 3))`

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C1](#c1) · cell 3 [markdown]
- [C2](#c2) · cell 3 [markdown]
- [C5](#c5) · cell 7: Optimal point
- [C7](#c7) · cell 9: SLR + MSE
- [C8](#c8) · cell 9: Optimal point
- [C11](#c11) · cell 13: In case we're in a weird style state
- [C18](#c18) · cell 24: `std` finds the standard deviation

## Changes

<a id="c1"></a>
### C1 · cell 3 [markdown] · dropdown

baseline L175 → branch L175 · mirror of the next code cell (hard rule 3)

```diff
- # import pandas as pd
+ # import polars as pl
```

**Why:** Mirrors the import rename in the code cell below. Checked mechanically: all ten dropdowns in this chapter match the cell they front line for line, so hard rule 3 holds throughout.
**Output:** same

<a id="c2"></a>
### C2 · cell 3 [markdown] · dropdown

baseline L181 → branch L181 · mirror of the next code cell (hard rule 3)

```diff
- # dugongs = pd.read_csv("data/dugongs.csv")
+ # dugongs = pl.read_csv("data/dugongs.csv")
```

**Why:** Mirrors the `pd.read_csv` -> `pl.read_csv` rename. The file has no NA tokens and no index column, so the call needs no extra arguments.
**Output:** same

<a id="c3"></a>
### C3 · cell 4 [code] · code

baseline L189 → branch L189

```diff
- import pandas as pd
+ import polars as pl
```

**Why:** Import rename.
**Output:** same

<a id="c4"></a>
### C4 · cell 4 [code] · code

baseline L195 → branch L195

```diff
- dugongs = pd.read_csv("data/dugongs.csv")
+ dugongs = pl.read_csv("data/dugongs.csv")
```

**Why:** `pd.read_csv` -> `pl.read_csv`. Verified in the d100 env: (27, 2), zero nulls in both columns, and `Length`/`Age` values equal to the pandas read element for element.
**Output:** same

<a id="c5"></a>
### C5 · cell 7: Optimal point · dropdown

baseline L263 → branch L263 · mirror of the next code cell (hard rule 3)

```diff
- # thetahat = np.mean(data_constant)
+ # thetahat = data_constant.mean()
```

**Why:** `np.mean(data_constant)` -> `data_constant.mean()`. `np.mean` routes through `_wrapreduction`, which calls `Series.mean(axis=...)`; Polars rejects the keyword and raises `TypeError`, so the native reduction is the only form that works — and it is the idiom the skill prefers anyway. Same value (10.9444...), verified against the pandas read. Mirror matches its code cell.
**Output:** same

<a id="c6"></a>
### C6 · cell 8 [code] · code

baseline L289 → branch L289

```diff
- thetahat = np.mean(data_constant)
+ thetahat = data_constant.mean()
```

**Why:** Same rewrite as C5, in the code cell.
**Output:** same

<a id="c7"></a>
### C7 · cell 9: SLR + MSE · dropdown

baseline L301 → branch L301 · mirror of the next code cell (hard rule 3)

```diff
- #     data_x, data_y = data_linear.iloc[:, 0], data_linear.iloc[:, 1]
+ #     data_x, data_y = (
+ #         data_linear.to_series(0).to_numpy(),
+ #         data_linear.to_series(1).to_numpy(),
+ #     )
```

**Why:** `data_linear.iloc[:, 0]` is positional column selection, which Polars spells `to_series(0)`. The `.to_numpy()` on top is forced, not churn: the very next lines call `np.std(data_y)` and `np.mean(data_y)`, both of which raise on a Polars Series under the NumPy reduction dispatch rule (verified live). Mirror matches its code cell.
**Output:** same

<a id="c8"></a>
### C8 · cell 9: Optimal point · dropdown

baseline L316 → branch L319 · mirror of the next code cell (hard rule 3)

```diff
- # data_x, data_y = data_linear.iloc[:, 0], data_linear.iloc[:, 1]
+ # data_x, data_y = data_linear.to_series(0).to_numpy(), data_linear.to_series(1).to_numpy()
```

**Why:** Same rewrite as C7, one line lower in the same dropdown — the `theta_1_hat`/`theta_0_hat` computation that feeds `np.corrcoef`, `np.std` and `np.mean`.
**Output:** same

<a id="c9"></a>
### C9 · cell 10 [code] · code

baseline L357 → branch L360

```diff
-     data_x, data_y = data_linear.iloc[:, 0], data_linear.iloc[:, 1]
+     data_x, data_y = (
+         data_linear.to_series(0).to_numpy(),
+         data_linear.to_series(1).to_numpy(),
+     )
```

**Why:** Same rewrite as C7, in the code cell.
**Output:** same

<a id="c10"></a>
### C10 · cell 10 [code] · code

baseline L372 → branch L378

```diff
- data_x, data_y = data_linear.iloc[:, 0], data_linear.iloc[:, 1]
+ data_x, data_y = data_linear.to_series(0).to_numpy(), data_linear.to_series(1).to_numpy()
```

**Why:** Same rewrite as C8, in the code cell.
**Output:** same

<a id="c11"></a>
### C11 · cell 13: In case we're in a weird style state · dropdown

baseline L439 → branch L445 · mirror of the next code cell (hard rule 3)

```diff
- # sns.rugplot(yobs, height=0.25, lw=2) ;
+ # sns.rugplot(x=yobs, height=0.25, lw=2) ;
```

**Why:** `sns.rugplot(yobs, ...)` -> `sns.rugplot(x=yobs, ...)`. Worth knowing that this was **not required**: I rendered both forms against a Polars Series on seaborn 0.13.2 and they produce byte-identical PNGs, with no warning either way. It is a defensive clarification, safe to revert. Mirror matches its code cell.
**Output:** same — verified pixel-identical between the positional and keyword forms

<a id="c12"></a>
### C12 · cell 14 [code] · code

baseline L455 → branch L461

```diff
- sns.rugplot(yobs, height=0.25, lw=2) ;
+ sns.rugplot(x=yobs, height=0.25, lw=2) ;
```

**Why:** Same edit as C11, in the code cell.
**Output:** same — the figure at C24 moved only by re-execution, not by this change

<a id="c13"></a>
### C13 · cell 20 [markdown] · prose · **REVIEW**

baseline L603 → branch L609

```diff
- # How do outliers affect each cost function? Imagine we replace the largest value in the dataset with 1000. The mean of the data increases substantially, while the median is nearly unaffected.
+ # How do outliers affect each cost function? Imagine we add a sixth, wildly out-of-scale value of 1033 to the dataset. The mean of the data increases substantially — from 25 to 193 — while the median barely moves, from 22 to 25.5.
```

**Why:** "Replace the largest value with 1000" describes neither what the code does nor what the output beneath it shows. `np.append(drinks, 1033)` **adds** a sixth element and leaves 33 in place, and the committed output two lines down reads `[20, 21, 22, 29, 33, 1033]`. The distinction is load-bearing: under the old sentence n stays odd and the median is exactly unchanged (22 -> 22), which is what "nearly unaffected" wants; under the code n flips to even and the median moves to 25.5. Re-derived: mean 25 -> 193, median 22 -> 25.5. CONTRADICTIONS A4 #1; pre-existing.
**Verdict:** necessary — a fix to a false claim, and unrelated to Polars

<a id="c14"></a>
### C14 · cell 24 [markdown] · prose · **REVIEW**

baseline L633 → branch L639

```diff
- # :alt: MAE is shown with theta close to 5.
+ # :alt: MAE plotted against theta-nought from 0 to 40. The curve falls steeply, flattens into a horizontal segment between about 22 and 29 at an MAE of roughly 5.7, then rises again. A dot marks a minimising theta of about 25.5 in the middle of that flat segment.
```

**Why:** "MAE is shown with theta close to 5" reads the curve's y-value as its x-parameter. I opened `images/mae_loss_infinite.png`: the x-axis is $\theta_0$ running 0-40, the flat minimum spans about 22-29, and the marked dot sits at roughly 25.5; the 5 is the MAE value on the y-axis. A screen-reader user was being handed the loss value labelled as the parameter, contradicting the paragraph three lines above. CONTRADICTIONS A4 #2; pre-existing.
**Verdict:** necessary — a fix to a false claim, and an accessibility defect

<a id="c15"></a>
### C15 · cell 24 [markdown] · prose · **REVIEW**

baseline L640 → branch L646

```diff
- # | Loss Function                  | $\hat{R}(\theta) = \frac{1}{n}\sum^{n}_{i=1} (y_i - \theta_0)^2$                                            | $\hat{R}(\theta) = \frac{1}{n}\sum^{n}_{i=1}$ |y_i - \theta_0|$                                               |
+ # | Loss Function                  | $\hat{R}(\theta) = \frac{1}{n}\sum^{n}_{i=1} (y_i - \theta_0)^2$                                            | $\hat{R}(\theta) = \frac{1}{n}\sum^{n}_{i=1} \lvert y_i - \theta_0 \rvert$                                               |
```

**Why:** The MAE cell's absolute-value bars fell outside math mode and the trailing `$` was unbalanced. Worse, a bare `\|` inside a MyST table cell is a **column separator**, so the row split and the formula the reader saw was not the MAE at all. `\lvert ... \rvert` inside the math span fixes both. CONTRADICTIONS A4 #5; pre-existing.
**Verdict:** necessary — a fix to broken markup that published the wrong formula

<a id="c16"></a>
### C16 · cell 24 [markdown] · prose · **REVIEW**

baseline L642 → branch L648

```diff
- # | Loss Surface           | ![MSE is shown with theta=26.7](images/mse_loss_26.png)  | ![MAE is shown with theta close to 5.](images/mae_loss_infinite.png)    |
+ # | Loss Surface           | ![MSE is shown with theta=26.7](images/mse_loss_26.png)  | ![MAE plotted against theta-nought, with a flat minimum between about 22 and 29 at an MAE of roughly 5.7.](images/mae_loss_infinite.png)    |
```

**Why:** The same wrong alt text as C14, on the copy embedded in the summary table. Replaced with a description of what the figure actually draws (verified by opening it). CONTRADICTIONS A4 #2; pre-existing.
**Verdict:** necessary — a fix to a false claim

<a id="c17"></a>
### C17 · cell 24 [markdown] · prose · **REVIEW**

baseline L645 → branch L651

```diff
- # | $\hat{\theta_0}$ Uniqueness | **Unique** $\hat{\theta_0}$                              | **Infinitely many** $\hat{\theta_0}$s                                    |
+ # | $\hat{\theta_0}$ Uniqueness | **Unique** $\hat{\theta_0}$                              | **Not always unique** — a single $\hat{\theta_0}$ when $n$ is odd, an interval of them when $n$ is even                                    |
```

**Why:** "**Infinitely many** $\hat{\theta_0}$s" is false for odd $n$: on the chapter's own 5-point dataset the MAE minimiser is the single point 22.0, and the interval only appears when $n$ is even. The row also contradicted the row two above it, which gives MAE's optimum as `median(y)`. The chapter's prose already carried the hedged version ("not guaranteed to have a single unique solution"); only the table dropped it. CONTRADICTIONS A4 #3; pre-existing.
**Verdict:** necessary — a fix to a false claim

<a id="c18"></a>
### C18 · cell 24: `std` finds the standard deviation · dropdown

baseline L677 → branch L683 · mirror of the next code cell (hard rule 3)

```diff
- # x = dugongs["Length"]
- # y = dugongs["Age"]
+ # x = dugongs["Length"].to_numpy()
+ # y = dugongs["Age"].to_numpy()
```

**Why:** `dugongs["Length"]` is a Polars Series and the next three lines call `np.corrcoef`, `np.std` and `np.mean` on it. `np.corrcoef` would take the Series (it routes through `asarray`), but `np.std` and `np.mean` raise, so the crossing has to happen at the assignment. Forced, not plotting churn. Mirror matches its code cell.
**Output:** same

<a id="c19"></a>
### C19 · cell 25 [code] · code

baseline L699 → branch L705

```diff
- x = dugongs["Length"]
- y = dugongs["Age"]
+ x = dugongs["Length"].to_numpy()
+ y = dugongs["Age"].to_numpy()
```

**Why:** Same rewrite as C18, in the code cell. Verified that `np.std`/`np.mean`/`np.corrcoef` over the `.to_numpy()` arrays give exactly the pandas values (7.7224220597644, 10.944444444444445, 0.8296474554906) — the column has no nulls, so there is no skipna-versus-NaN divergence to worry about.
**Output:** same

<a id="c20"></a>
### C20 · cell 30: Bonus: Calculating Constant Model MSE Using an Algebraic Tri · prose · **REVIEW**

baseline L851 → branch L857

```diff
- # Since variance can't be negative, we know that our first term, $\sigma_y^2$ is greater than or equal to $0$. Also note, that **the first term doesn't involve $\theta$ at all**, meaning changing our model won't change this value. For the purposes of determining $\hat{\theta}#, we can then essentially ignore this term.
+ # Since variance can't be negative, we know that our first term, $\sigma_y^2$ is greater than or equal to $0$. Also note, that **the first term doesn't involve $\theta$ at all**, meaning changing our model won't change this value. For the purposes of determining $\hat{\theta}$, we can then essentially ignore this term.
```

**Why:** `$\hat{\theta}#` — a `#` where the closing `$` belongs. The math delimiter never closed, so the rest of the sentence was swallowed into math mode. CONTRADICTIONS A4 #6; pre-existing.
**Verdict:** necessary — a fix to broken markup

<a id="c21"></a>
### C21 · cell 30: Bonus: Calculating Constant Model MSE Using an Algebraic Tri · prose · **REVIEW**
baseline L863 → branch L869

```diff
- # - **Bias Squared, $(\bar{y} - \theta)^2$**: This term captures the bias of the estimator, defined as the square of the difference between the mean of the data points, $\bar{y}$, and the parameter $\theta$. The bias quantifies the systematic error introduced when estimating $\theta$. Minimizing this term is essential for improving the accuracy of the estimator. When $\theta = \bar{y}$, the bias is $0$, indicating that the estimator is unbiased for the parameter it estimates. This highlights a critical principle in statistical estimation: choosing $\theta$ to be the sample mean, $\bar{y}$, minimizes the average loss, rendering the estimator both efficient and unbiased for the population mean.
+ # - **Bias Squared, $(\bar{y} - \theta)^2$**: This term captures the bias of the estimator, defined as the square of the difference between the mean of the data points, $\bar{y}$, and the parameter $\theta$. The bias quantifies the systematic error introduced when estimating $\theta$. Minimizing this term is essential for improving the accuracy of the estimator. When $\theta = \bar{y}$, the bias is $0$, indicating that the estimator is unbiased for the parameter it estimates. This highlights a critical principle in statistical estimation: choosing $\theta$ to be the sample mean, $\bar{y}$, minimizes the average loss, rendering the estimator unbiased for the population mean. (Unbiased, but not necessarily *efficient*: for a heavy-tailed population the sample median can have the lower variance of the two.)
```

**Why:** The sentence claimed that choosing $\theta = \bar{y}$ renders the estimator "both efficient and unbiased". Unbiasedness holds; efficiency does not outside the Gaussian case — over 200,000 draws of n=25 from a Laplace population, Var(sample mean) = 0.0796 against Var(sample median) = 0.0536. The conversion dropped "efficient" and added a parenthetical naming the heavy-tailed counterexample, so the surviving claim is the one that is true. CONTRADICTIONS §A4 #4; pre-existing course content, not introduced by the conversion — the same text is in the `887a578b0a4b` baseline.
**Verdict:** necessary — a fix to a claim that was false. The parenthetical is an addition rather than a deletion, so staff who want the minimum change can cut it and leave "rendering the estimator unbiased for the population mean".

<a id="c22"></a>
### C22 · `plt.style.use('default') # Revert style to default mpl` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 34924 bytes md5:f4c173b103
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 36056 bytes md5:c563862477
```

**Why:** Full re-execution. `dugongs.csv` reads identically under Polars (27 rows, no nulls, verified), so the plotted values are unchanged and the byte delta is rasterisation under the current matplotlib/seaborn. Canvas 448x608 -> 453x610 px (tight-bbox font metrics under the current matplotlib).
**Reader sees:** equivalent — the constant-model loss surface with its minimum marked at the same $\hat\theta_0$. Not opened individually

<a id="c23"></a>
### C23 · `def mse_linear(theta_0, theta_1, data_linear):` · output

committed output

```diff
- [text] <Figure size 700x500 with 2 Axes>
- [image/png] 123396 bytes md5:d8bad0482b
+ [text] <Figure size 700x500 with 2 Axes>
+ [image/png] 124700 bytes md5:e13dd05a1e
```

**Why:** Full re-execution. `dugongs.csv` reads identically under Polars (27 rows, no nulls, verified), so the plotted values are unchanged and the byte delta is rasterisation under the current matplotlib/seaborn. The 3D MSE surface, now indexed through `to_series(i).to_numpy()`; the values reaching `mse_linear` are the same floats. Canvas 448x557 -> 453x560 px.
**Reader sees:** equivalent. Not opened individually

<a id="c24"></a>
### C24 · `sns.set_theme()` · output

committed output

```diff
- [text] <Figure size 800x150 with 1 Axes>
- [image/png] 9940 bytes md5:b72c45372c
+ [text] <Figure size 800x150 with 1 Axes>
+ [image/png] 9248 bytes md5:9799e13e69
```

**Why:** Full re-execution. `dugongs.csv` reads identically under Polars (27 rows, no nulls, verified), so the plotted values are unchanged and the byte delta is rasterisation under the current matplotlib/seaborn. This is the rugplot whose call gained `x=` (C12); I confirmed separately that the positional and keyword forms render byte-identically, so the 1.45% pixel delta is re-execution alone.
**Reader sees:** equivalent. Not opened individually

<a id="c25"></a>
### C25 · `sns.set_theme()` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 29424 bytes md5:7b86420ff4
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 29484 bytes md5:e8b1beba7e
```

**Why:** Full re-execution. `dugongs.csv` reads identically under Polars (27 rows, no nulls, verified), so the plotted values are unchanged and the byte delta is rasterisation under the current matplotlib/seaborn. `sns.scatterplot(x=xs, y=yobs)` takes the Polars Series directly. 1.13% of pixels differ.
**Reader sees:** equivalent. Not opened individually

<a id="c26"></a>
### C26 · `x = dugongs["Length"].to_numpy()` · output

committed output

```diff
- [text] <Figure size 1600x600 with 2 Axes>
- [image/png] 67852 bytes md5:bc50d394f6
+ [text] <Figure size 1600x600 with 2 Axes>
+ [image/png] 68648 bytes md5:57e94cfe86
```

**Why:** Full re-execution. `dugongs.csv` reads identically under Polars (27 rows, no nulls, verified), so the plotted values are unchanged and the byte delta is rasterisation under the current matplotlib/seaborn. The two-panel Length/Age scatter, drawn from the `.to_numpy()` arrays of C19. Canvas 620x1407 -> 622x1408 px.
**Reader sees:** equivalent. Not opened individually

<a id="c27"></a>
### C27 · `z = np.log(y)` · output

committed output

```diff
- [text] <Figure size 1600x600 with 2 Axes>
- [image/png] 59148 bytes md5:277b5f3839
+ [text] <Figure size 1600x600 with 2 Axes>
+ [image/png] 59460 bytes md5:4801f33183
```

**Why:** Full re-execution. `dugongs.csv` reads identically under Polars (27 rows, no nulls, verified), so the plotted values are unchanged and the byte delta is rasterisation under the current matplotlib/seaborn. The log-transformed panel pair, derived from the same arrays. Canvas 620x1389 -> 622x1389 px.
**Reader sees:** equivalent. Not opened individually

<a id="c28"></a>
### C28 · `plt.figure(dpi=120, figsize=(4, 3))` · output

committed output

```diff
- [text] <Figure size 480x360 with 1 Axes>
- [image/png] 23920 bytes md5:9878dd0334
+ [text] <Figure size 480x360 with 1 Axes>
+ [image/png] 23928 bytes md5:c6891096d7
```

**Why:** Full re-execution. `dugongs.csv` reads identically under Polars (27 rows, no nulls, verified), so the plotted values are unchanged and the byte delta is rasterisation under the current matplotlib/seaborn. The back-transformed prediction curve. 0.98% of pixels differ.
**Reader sees:** equivalent. Not opened individually

