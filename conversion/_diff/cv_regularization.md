# cv_regularization — change report

`887a578b0a4b:content/cv_regularization/cv_reg.ipynb` → `content/cv_regularization/cv_reg.ipynb`

**Tier B · 14 changes:** output 4 · prose 3 · dropdown 2 · tab-twins 1 · code 4

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

Mostly mechanical: one seaborn-sourced frame wrapped in `pl.from_pandas`, a chained `X["hp^k"] = ...` build collapsed into one `select`, and four committed outputs reprinted. The real weight is in the prose — four of CONTRADICTIONS §A3's six pre-existing errors are corrected here (C5, C6, C9, C10). Staff should read C7 first: the LASSO paragraph now denies the claim and then keeps the baseline's “In other words” sentence, which reasserts it. Second, C11 and C14 are not Polars effects at all — re-run in the pinned env the pandas code produces the branch's numbers exactly, so those two are environment drift in the baseline.

## Needs review

- [C5](#c5) · cell 7: Some Cross-Validation Pitfalls
- [C7](#c7) · cell 9 [markdown]
- [C9](#c9) · cell 14: L2 (Ridge) Regularization

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C11](#c11) · `import sklearn.linear_model as lm`
- [C12](#c12) · `X_train.head()`
- [C13](#c13) · `pl.DataFrame({"Feature":X_train.columns, "Parameter":lasso_model.coef_`
- [C14](#c14) · `ridge_model = lm.Ridge(alpha=1)`

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C1](#c1) · cell 2: Test Sets
- [C2](#c2) · cell 2: Load the dataset and construct the design matrix

## Changes

<a id="c1"></a>
### C1 · cell 2: Test Sets · dropdown

baseline L67 → branch L67 · mirror of the next code cell (hard rule 3)

```diff
- # import pandas as pd
+ # import polars as pl
```

**Why:** Mirrors the import in the code cell below it (C3).
**Output:** same — no output; the mirrored copy matches the code cell it mirrors line for line.

<a id="c2"></a>
### C2 · cell 2: Load the dataset and construct the design matrix · dropdown

baseline L74 → branch L74 · mirror of the next code cell (hard rule 3)

```diff
- # vehicles = sns.load_dataset("mpg").rename(columns={"horsepower":"hp"}).dropna()
- # X = vehicles[["hp"]]
- # X["hp^2"] = vehicles["hp"]**2
- # X["hp^3"] = vehicles["hp"]**3
- # X["hp^4"] = vehicles["hp"]**4
+ # vehicles = pl.from_pandas(sns.load_dataset("mpg")).rename({"horsepower":"hp"}).drop_nulls()
+ # X = vehicles.select(
+ #     pl.col("hp"),
+ #     (pl.col("hp")**2).alias("hp^2"),
+ #     (pl.col("hp")**3).alias("hp^3"),
+ #     (pl.col("hp")**4).alias("hp^4"),
+ # )
```

**Why:** Mirrors the design-matrix cell below it (C4).
**Output:** same — no output; the mirrored copy matches C4 exactly, including the new `select` block.

<a id="c3"></a>
### C3 · cell 3 [code] · code

baseline L85 → branch L87

```diff
- import pandas as pd
+ import polars as pl
```

**Why:** Import rename.
**Output:** same.

<a id="c4"></a>
### C4 · cell 3 [code] · code

baseline L92 → branch L94

```diff
- vehicles = sns.load_dataset("mpg").rename(columns={"horsepower":"hp"}).dropna()
- X = vehicles[["hp"]]
- X["hp^2"] = vehicles["hp"]**2
- X["hp^3"] = vehicles["hp"]**3
- X["hp^4"] = vehicles["hp"]**4
+ vehicles = pl.from_pandas(sns.load_dataset("mpg")).rename({"horsepower":"hp"}).drop_nulls()
+ X = vehicles.select(
+     pl.col("hp"),
+     (pl.col("hp")**2).alias("hp^2"),
+     (pl.col("hp")**3).alias("hp^3"),
+     (pl.col("hp")**4).alias("hp^4"),
+ )
```

**Why:** `sns.load_dataset` returns a pandas frame, so `pl.from_pandas` is required rather than churn (the chapter adds no `.to_pandas()` anywhere). `rename(columns=)` → `rename({})`, `dropna` → `drop_nulls`, and the four in-place `X["hp^k"] = ...` assignments become one `select` because Polars frames are immutable.
**Output:** same — 392 rows survive `drop_nulls` on both sides, the 313-row training split is the same split, and every fitted coefficient below is unchanged (verified side by side).

<a id="c5"></a>
### C5 · cell 7: Some Cross-Validation Pitfalls · prose · **REVIEW**

baseline L236 → branch L240

```diff
- # While this may sound complicated to implement? Fortunately, libraries such as `scikit-learn` provide built-in tools to handle these scenarios. An example of this can be found in the [`TimeSeriesSplit`](https://scikit-learn.org/stable/modules/cross_validation.html#time-series-split) function.
+ # This may sound complicated to implement. Fortunately, libraries such as `scikit-learn` provide built-in tools to handle these scenarios. An example of this can be found in the [`TimeSeriesSplit`](https://scikit-learn.org/stable/modules/cross_validation.html#time-series-split) cross-validator.
```

**Why:** `TimeSeriesSplit` is a cross-validator class, not a function (`inspect.isclass` is `True`); the same edit also repairs the baseline's stray question mark in “While this may sound complicated to implement?”. CONTRADICTIONS §A3 #6 — pre-existing.
**Verdict:** necessary — a fix to a false claim. The grammar repair rides along in the same sentence.

<a id="c6"></a>
### C6 · cell 8 [code] · code

baseline L377 → branch L381

```diff
- # The alpha parameter represents our lambda term
+ # sklearn's alpha is not quite our lambda: Lasso minimizes
+ # (1/(2n))||Y - X.theta||^2 + alpha*||theta||_1, so alpha = lambda/2
```

**Why:** sklearn's `Lasso` minimises `(1/(2n))‖Y-Xθ‖² + alpha·‖θ‖1` while the chapter's objective has no 1/2, so `alpha = λ/2` and the baseline comment (“alpha represents our lambda”) was wrong. CONTRADICTIONS §A3 #1 — pre-existing.
**Output:** same — comment only; `lasso_model.coef_` is unchanged.

<a id="c7"></a>
### C7 · cell 9 [markdown] · prose · **REVIEW**

baseline L384 → branch L389

```diff
- # Notice that all model coefficients are very small in magnitude. In fact, some of them are so small that they are essentially 0. An important characteristic of L1 regularization is that many model parameters are set to 0. In other words, LASSO effectively **selects only a subset** of the features. The reason for this comes back to our loss surface and allowed "diamond" regions from earlier – we can often get closer to the lowest loss contour at a corner of the diamond than along an edge.
+ # An important characteristic of L1 regularization is that it drives model parameters to exactly 0, which is what makes it useful for feature selection. That is not what happened here: none of these four coefficients is zero, and the `hp` coefficient is *larger* than its unregularized value. The coefficients look small only because `hp^2` through `hp^4` are enormous — which is the problem the next section fixes. In other words, LASSO effectively **selects only a subset** of the features. The reason for this comes back to our loss surface and allowed "diamond" regions from earlier – we can often get closer to the lowest loss contour at a corner of the diamond than along an edge.
```

**Why:** The baseline claimed of this output that all coefficients are “essentially 0” and that many parameters are set to 0. Neither holds: 0 of 4 coefficients are zero, and `hp` grew and flipped sign against the unregularised fit (−0.2549 vs +0.0597) — re-verified in the pinned env. CONTRADICTIONS §A3 #5 — pre-existing.
**Verdict:** questionable — the correction is right, but it kept the baseline's closing sentences, so the paragraph now reads “That is not what happened here … In other words, LASSO effectively **selects only a subset** of the features,” which reasserts what the sentence before it just denied.
**Minimal alternative:** keep the new first three sentences and re-point the inherited one — “In general, L1 selects only a subset of the features, and the reason comes back to …” — so the closing claim is about L1 rather than about this output.

<a id="c8"></a>
### C8 · cell 12 [code] · tab-twins

baseline L400 → branch L405 · spans code and prose

```diff
- # %%
- pd.DataFrame({"Feature":X_train.columns, "Parameter":lasso_model.coef_})
+ # %% tags=["remove-input", "remove-output"]
+ pl.DataFrame({"Feature":X_train.columns, "Parameter":lasso_model.coef_})
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 051dcedb -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # pl.DataFrame({"Feature":X_train.columns, "Parameter":lasso_model.coef_})
+ # ```
+ #
+ # ```text
+ # shape: (4, 2)
+ # ┌─────────┬────────────┐
+ # │ Feature ┆ Parameter  │
+ # │ ---     ┆ ---        │
+ # │ str     ┆ f64        │
+ # ╞═════════╪════════════╡
+ # │ hp      ┆ -0.254932  │
+ # │ hp^2    ┆ -0.000949  │
+ # │ hp^3    ┆ 0.000009   │
+ # │ hp^4    ┆ -1.2287e-8 │
+ # └─────────┴────────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # pd.DataFrame({"Feature":X_train.columns, "Parameter":lasso_model.coef_})
+ # ```
+ #
+ # ```text
+ #   Feature     Parameter
+ # 0      hp -2.549321e-01
+ # 1    hp^2 -9.485972e-04
+ # 2    hp^3  8.919763e-06
+ # 3    hp^4 -1.228723e-08
+ # ```
+ … 3 more lines
```

**Why:** `pd.DataFrame` → `pl.DataFrame`; the cell was hidden and its output re-published as a synced Polars/pandas tab pair.
**Output:** differs: same four coefficients, but Polars formats per column rather than in uniform scientific notation, so `hp^3` prints as `0.000009` where pandas printed `8.919763e-06`.

<a id="c9"></a>
### C9 · cell 14: L2 (Ridge) Regularization · prose · **REVIEW**

baseline L448 → branch L494

```diff
- # In `sklearn`, we perform L2 regularization using the `Ridge` class. It runs gradient descent to minimize the L2 objective function. Notice that we scale the data before regularizing.
+ # In `sklearn`, we perform L2 regularization using the `Ridge` class. Unlike LASSO, L2 has a closed-form solution, and `Ridge` uses it: with the default `solver="auto"` on a dense problem it performs a direct Cholesky solve rather than iterating. Notice that we do **not** scale the data here, which is what the next section is about — the four features span `hp` in the tens and `hp^4` in the tens of millions.
```

**Why:** Two false claims in one sentence. `Ridge(alpha=1).fit(...).solver_` resolves to `cholesky` with `n_iter_` of `None` — a direct solve of the closed form printed four lines above, not gradient descent (verified) — and the chapter scales nothing, with no `StandardScaler` anywhere in it. CONTRADICTIONS §A3 #3 and #4 — both pre-existing.
**Verdict:** necessary — a fix to two false claims. The replacement also points forward to the scaling section, which is where the baseline sentence was trying to point.

<a id="c10"></a>
### C10 · cell 15 [code] · code

baseline L451 → branch L497

```diff
- ridge_model = lm.Ridge(alpha=1) # alpha represents the hyperparameter lambda
+ # Ridge minimizes ||Y - X.theta||^2 + alpha*||theta||^2 with no 1/n,
+ # so alpha = n*lambda -- alpha=1 here is lambda = 1/313
+ ridge_model = lm.Ridge(alpha=1)
```

**Why:** `Ridge` minimises `‖Y-Xθ‖² + alpha·‖θ‖²` with no 1/n, so `alpha = nλ`; the training set here has 313 rows (verified), making `alpha=1` equal to λ = 1/313. CONTRADICTIONS §A3 #2 — pre-existing.
**Output:** same — comment only; `ridge_model.coef_` is unchanged by it.

<a id="c11"></a>
### C11 · `import sklearn.linear_model as lm` · output

committed output

```diff
- [stdout] Training error: 17.85851684101209
- [stdout] Test error: 23.192405630290637
+ [stdout] Training error: 17.85851684101209
+ [stdout] Test error: 23.19240563000083
```

**Why:** Not a Polars effect. Re-run in the pinned env, the *pandas* code prints `Test error: 23.19240563000083` as well (verified side by side), so the baseline's `...290637` is drift from the environment the baseline was executed in, not from the conversion. The training error is byte-identical on both sides.
**Reader sees:** equivalent — the value moves in its eleventh significant figure.

<a id="c12"></a>
### C12 · `X_train.head()` · output

committed output

```diff
- [text]         hp     hp^2       hp^3         hp^4
- [text] 259   85.0   7225.0   614125.0   52200625.0
- [text] 129   67.0   4489.0   300763.0   20151121.0
- [text] 207  102.0  10404.0  1061208.0  108243216.0
- [text] 302   70.0   4900.0   343000.0   24010000.0
- [text] 71    97.0   9409.0   912673.0   88529281.0
+ [text] shape: (5, 4)
+ [text] ┌───────┬─────────┬────────────┬──────────────┐
+ [text] │ hp    ┆ hp^2    ┆ hp^3       ┆ hp^4         │
+ [text] │ ---   ┆ ---     ┆ ---        ┆ ---          │
+ [text] │ f64   ┆ f64     ┆ f64        ┆ f64          │
+ [text] ╞═══════╪═════════╪════════════╪══════════════╡
+ [text] │ 85.0  ┆ 7225.0  ┆ 614125.0   ┆ 5.2200625e7  │
+ [text] │ 67.0  ┆ 4489.0  ┆ 300763.0   ┆ 2.0151121e7  │
+ [text] │ 102.0 ┆ 10404.0 ┆ 1.061208e6 ┆ 1.08243216e8 │
+ [text] │ 70.0  ┆ 4900.0  ┆ 343000.0   ┆ 2.401e7      │
+ [text] │ 97.0  ┆ 9409.0  ┆ 912673.0   ┆ 8.8529281e7  │
+ [text] └───────┴─────────┴────────────┴──────────────┘
```

**Why:** Polars repr, and `hp^3`/`hp^4` cross the magnitude threshold where Polars switches to scientific notation.
**Reader sees:** changed: the same five rows and the same values, but the shuffled pandas row labels (259, 129, 207, 302, 71) are gone — Polars has no index, so the head no longer shows that the training set is a shuffle of the original rows. `52200625.0` now prints as `5.2200625e7`.

<a id="c13"></a>
### C13 · `pl.DataFrame({"Feature":X_train.columns, "Parameter":lasso_model.coef_` · output

committed output

```diff
- [text]   Feature     Parameter
- [text] 0      hp -2.549321e-01
- [text] 1    hp^2 -9.485972e-04
- [text] 2    hp^3  8.919763e-06
- [text] 3    hp^4 -1.228723e-08
+ [text] shape: (4, 2)
+ [text] ┌─────────┬────────────┐
+ [text] │ Feature ┆ Parameter  │
+ [text] │ ---     ┆ ---        │
+ [text] │ str     ┆ f64        │
+ [text] ╞═════════╪════════════╡
+ [text] │ hp      ┆ -0.254932  │
+ [text] │ hp^2    ┆ -0.000949  │
+ [text] │ hp^3    ┆ 0.000009   │
+ [text] │ hp^4    ┆ -1.2287e-8 │
+ [text] └─────────┴────────────┘
```

**Why:** `pl.DataFrame` repr with per-column formatting instead of a single scientific format for the whole column.
**Reader sees:** changed: same four coefficients, but `hp^3` now reads `0.000009` rather than `8.919763e-06`, which loses the magnitude of the very coefficient the paragraph above (C7) is arguing about.

<a id="c14"></a>
### C14 · `ridge_model = lm.Ridge(alpha=1)` · output

committed output

```diff
- [text] array([ 5.89130560e-02, -6.42445916e-03,  4.44468157e-05, -8.83981945e-08])
+ [text] array([ 5.89130559e-02, -6.42445915e-03,  4.44468157e-05, -8.83981945e-08])
```

**Why:** Environment drift again, not a library difference: today's pandas path returns `5.89130559e-02` too (verified), and `solver_` is `cholesky` on both sides.
**Reader sees:** equivalent — the leading coefficient moves in its ninth significant figure.

