# Contradicted claims found during the Polars migration

Every chapter of the course notes was read by an agent whose only job was to take each factual
assertion about library behaviour, mathematics, or the chapter's own data, **run it**, and report
what came back. This file records every claim that turned out to be false, where it came from, and
why it is false.

The reason to read it: **most of these predate this branch.** The migration was not supposed to be a
content audit and became one. Course staff should decide what to do with the pre-existing half —
whether the fixes ship inside a Polars diff or as their own change against `main`.

- **Environment:** every check ran against the pin — `polars 1.43.1`, `pandas 2.3.0`,
  `numpy 1.26.4`, `scikit-learn 1.7.0`, `seaborn 0.13.2`, Python 3.11 (conda env `d100`).
- **Provenance** was decided by diffing against the pinned pre-conversion commit
  `887a578b0a4b` (`conversion/.baseline/887a578b0a4b-1a27d5e2b015/`). A claim is "pre-existing" only
  if the same text is in that baseline.
- **Every fix was independently re-verified** before it was made — by re-running the code, or by
  opening the figure. Two reported errors did not survive that check in the form reported; both are
  recorded in the last section.

A handful of entries below were classed non-blocking by the reviewer that found them —
wording that is loose rather than false, or a statement the next sentence hedges. They are
listed here anyway, and flagged where they occur, because the distinction is a judgement call
and course staff should make it rather than inherit mine.

## Totals

| | claims decided | contradicted |
|---|---|---|
| 18 notebook chapters | ~1,150 | **79** |

| Provenance | count | who owns it |
|---|---|---|
| **A. Pre-existing course content** | **52** | course staff |
| **B. Introduced by the conversion** | **27** | this branch — all fixed |

Two chapters came back with nothing: **`logistic_regression_1`** (23 claims) and
**`feature_engineering`** (all claims supported). **`polars_1`** was clean on its 90-claim sweep.

Three chapters recorded the conversion *repairing* a pre-existing error in passing:

| chapter | was | now |
|---|---|---|
| `gradient_descent` | "the `.T` attribute of a NumPy array **or DataFrame**" | DataFrame dropped — Polars frames have no `.T` |
| `modeling_slr` | `print(f"\theta_0: …")` — `\t` is Python's tab escape, so the label rendered as a TAB plus `heta_0` | f-string repaired |
| `ols` | "the same convention as used when calling `.iloc` and `.loc`" | rewritten to `df[:, i]`, which is accurate under Polars |

---

# A. Pre-existing course content (52)

Present verbatim in `887a578b0a4b`. Fixed on this branch, but the errors are not this branch's.

## A1 · `gradient_descent` — 7

The chapter that teaches gradient descent asserts four times that things which do not use gradient
descent use gradient descent.

| # | Claim, as written | Why it is false |
|---|---|---|
| 1 | "When we fit the model, `sklearn` will run gradient descent behind the scenes" | `inspect.getsource(LinearRegression.fit)` calls `scipy.linalg.lstsq` — a one-shot SVD least-squares solve. The class exposes no learning rate, no `max_iter`, no `n_iter_`; its full constructor is `fit_intercept, copy_X, tol, n_jobs, positive`. |
| 2 | "in just three lines of code, our model has run gradient descent" | Same. |
| 3 | "under the hood, the `fit` method for `LinearRegression` models uses gradient descent" | Same — and this one is load-bearing. The section opens by arguing that closed forms only work under strong assumptions and gradient descent is the alternative, then claims the closed-form estimator it just derived is secretly the iterative one. |
| 4 | "gradient descent … is the principle that `scipy.optimize.minimize` uses" | With no gradient supplied, `minimize` defaults to **BFGS**, a quasi-Newton method — the returned object carries `hess_inv`, which proves the path taken. Its step is `−H⁻¹∇f`, not `−α∇f`; there is no learning rate, which is gradient descent's defining feature and what the chapter's very next line describes. |
| 5 | Code comment: "returns … the optimal input value of x which **minimizes f**" | The cell prints `x: [2.393]`. That is a **local** minimum with `f = −0.138`; the global minimiser is `x ≈ 5.326` with `f ≈ −0.691`, five times deeper — and the prose two cells earlier says "the minimum is somewhere around 5.3". The page contains its own refutation. |
| 6 | "we're only looking at **20** selected points" | `sparse_xs = np.linspace(1, 7, 5)` — five. The `simple_minimize` cell before it uses six. Neither is 20. |
| 7 | Docstring: "Performs **n** steps of gradient descent … Returns … all guesses over time" | The loop is `while len(guesses) < n` and seeds the list with the initial guess, so `n=100` performs 99 updates and returns 100 guesses. Internally inconsistent: *n* steps would give *n+1* guesses. |

**Fixed as:** the closed-form framing, which motivates the chapter better than the false one —
OLS has a closed form, and *that is exactly why* gradient descent matters for the models that don't.

## A2 · `logistic_regression_2` — 7

| # | Claim | Why it is false |
|---|---|---|
| 1 | "There is both a global minimum and a (barely perceptible) **local minimum** in the loss surface" | Scanning the exact function the cell plots over θ ∈ [−60, 20]: exactly **one** interior local minimum (the global one at θ ≈ 0.545) and one interior local **maximum** at θ ≈ −2.09. The "barely perceptible" feature is the maximum. Left of it the surface is monotone, falling toward the asymptote 2/3 as θ → −∞ — so descent from there **stalls on a plateau** (|∇| ≈ 7.4e−6); it does not converge on a second minimum. |
| 2 | Its alt text: "showing two possible minima" | Same. |
| 3 | PR curves: "the worst with an AUC = 0.5" | 0.5 is the **ROC** baseline. A random classifier's PR-AUC equals the positive-class rate — measured 0.50 / 0.20 / 0.05 at prevalences 0.5 / 0.2 / 0.05, while random ROC-AUC stayed 0.500 throughout. Worst placed exactly where it matters: the section exists to handle imbalance, and on the chapter's own 5%-spam example the floor is 0.05. |
| 4 | "The loss incurred … is infinite: $-(y\log p + (1-y)\log(1-p)) = 1 \cdot \log(0)$" | `1*np.log(0)` is **−inf**. The right-hand side contradicts the sentence above it. Needs `−1 · log(0)`. |
| 5 | Bonus identity: `… = y_i φ(x_i)^T + log(σ(−φ(x_i)^Tθ))` | The θ is dropped from the first term, making it a vector rather than a scalar. Checked numerically: with θ the identity reproduces the cross-entropy terms exactly; as printed it does not. |
| 6 | Bonus gradient: `−(1/n) Σ (y_i − σ(φ(x_i)^Tθ)φ(x_i))` | The bracket closes in the wrong place. Against a central-difference gradient: the correct form `(y_i − σ(·))φ(x_i)` matches; as parenthesised it does not. |
| 7 | "Say we add a new point $(x, y) = (-0.5, 1)$" | The figure it introduces labels that point **(−1, 1)** — confirmed by opening the image. Prose and figure disagree on the coordinates. |

Also fixed there, not counted as contradictions: nine `:width:800` options missing the space after
the colon, which MyST does not parse as options at all.

## A3 · `cv_regularization` — 6

The most immediately actionable set: three of these would mislead a student who typed the code.

| # | Claim | Why it is false |
|---|---|---|
| 1 | `# The alpha parameter represents our lambda term` above `lm.Lasso(alpha=2)` | sklearn's `Lasso` minimises `(1/(2n))‖y−Xw‖² + alpha·‖w‖₁`; the chapter's objective is `(1/n)‖·‖² + λ‖θ‖₁`. So **alpha = λ/2**, and `alpha=2` is λ = 4. Confirmed on an orthonormal design where the soft-threshold solution is exact. |
| 2 | `# alpha represents the hyperparameter lambda` above `lm.Ridge(alpha=1)` | `Ridge` minimises `‖y−Xw‖² + alpha·‖w‖²` with **no 1/n**, so **alpha = nλ**. The chapter prints the formula that disproves its own comment four lines earlier: `θ̂ = (XᵀX + nλI)⁻¹XᵀY`. Numerically, sklearn's coefficients match the chapter's formula at λ = 1/313, not λ = 1. |
| 3 | "`Ridge` … **runs gradient descent** to minimize the L2 objective function" | `Ridge(alpha=1).fit(...).solver_` resolves to **`cholesky`** — a direct linear solve of the closed form printed four lines above. `n_iter_` is `None`. Nothing iterative runs. |
| 4 | "Notice that we **scale the data** before regularizing." | The chapter scales nothing. `grep` for `StandardScaler|Scaler|standardiz|zscore` returns zero calls. `Ridge` is fed raw `X_train` whose columns run from `hp` in the tens to `hp^4` at 5.2e7. The sentence sits immediately before the section that exists to explain why scaling is needed. |
| 5 | "Notice that all model coefficients are very small … many model parameters are set to 0." | `(lasso_model.coef_ == 0).sum()` is **0 of 4**, and the `hp` coefficient *grew* and flipped sign against the unregularised fit (−0.2549 vs +0.0597). The general claim about L1 is true; anchored by "Notice that…" to this output it is false, and it teaches feature selection off an example that performs none. |
| 6 | "found in the `TimeSeriesSplit` **function**" | `inspect.isclass` → `True`. It is a cross-validator class. |

## A4 · `constant_model_loss_transformations` — 6

| # | Claim | Why it is false |
|---|---|---|
| 1 | "Imagine we **replace** the largest value in the dataset with **1000**." | The code is `np.append(drinks, 1033)` — it **adds** a sixth element and leaves 33 in place, and the value is 1033. The committed output `[20, 21, 22, 29, 33, 1033]` sits directly beneath the sentence. This changes the next clause: under the prose the median is *exactly* unchanged (n stays odd, 22 → 22), which is what "nearly unaffected" wants; under the code it moves 22 → 25.5 because n flips to even. |
| 2 | Alt text: "MAE is shown with **theta close to 5**" | Opening the figure: the x-axis is θ₀ running 0–40, the flat minimum spans ≈22–29, and the marked dot is at ≈25.5. The **5** is on the *y*-axis — it is the MAE value (exactly 5.667 across the flat segment). A screen-reader user is handed the loss value labelled as the parameter, contradicting the paragraph three lines above. |
| 3 | Summary table: MAE has "**Infinitely many** θ̂₀s" | False for odd *n*. On the chapter's own 5-point dataset the MAE minimiser is the single point 22.0; the interval appears only when *n* is even. The row also contradicts the row two above it, which gives MAE's optimum as `median(y)`. The correctly hedged version is already in the prose ("not guaranteed to have a single unique solution") — the table drops the hedge. |
| 4 | "rendering the estimator both **efficient** and unbiased" | Unbiasedness holds. Efficiency does not, outside the Gaussian case: over 200,000 draws of n=25 from a Laplace population, Var(sample mean) = 0.0796 against Var(sample median) = 0.0536. |
| 5 | MAE formula in the summary table | `$…\sum^{n}_{i=1}$ \|y_i - \theta_0\|$` — the absolute-value bars fall **outside** math mode and the trailing `$` is unbalanced. Worse, a bare `\|` inside a MyST table cell is a **column separator**, so the row splits and the formula the reader sees is not the MAE. |
| 6 | "For the purposes of determining $\hat{\theta}**#**" | `#` where `$` belongs. The math delimiter never closes, so the rest of the sentence is swallowed into math mode. |

## A5 · `inference_causality` — 5

| # | Claim | Why it is false |
|---|---|---|
| 1 | "Suppose we collected a sample of **20 cars**" | All four `sample_size` assignments in the chapter are `100`, and the cell's own committed output prints `Sample Size: 100` two lines below the sentence. |
| 2 | "using only a single random sample of **20 cars**" | Same. The only `20` in the code is `mpg_pop.sample(20)`, which draws *fresh* samples from the population — not the sample being bootstrapped. |
| 3 | "our bootstrapped sample distribution … is relatively close" to the population sampling distribution | The bootstrap resamples **100** (the sample size); the population curve beside it is built from draws of **20**. Measured over 2,000 reps: bootstrap sd 0.00046 / CI width 0.0018, against population-draws-of-20 sd 0.0011 / CI width 0.0043. The bootstrap distribution is **2.4× narrower**, and is close to the *n=100* population curve instead. The chapter states the rule it breaks two sections earlier: "New samples must be the same size as the original sample." |
| 4 | `print("RMSE", ((Y - model.predict(X)) ** 2).mean())` | That is the MSE. Printed 0.0455; the RMSE is 0.2132. |
| 5 | `rmse = mean_squared_error(Y, model.predict(X)); print(f'RMSE of Original Model: {rmse}')` | The pinned sklearn's signature is `(y_true, y_pred, *, sample_weight, multioutput)` — there is no `squared=` parameter, so it returns MSE unconditionally. The variable is even *named* `rmse`. |

## A6 · `sampling` — 3

| # | Claim | Why it is false |
|---|---|---|
| 1 | "The population cells are already in `polls`" / "The sample cells are also in `polls`" | The frame is bound as `poll` and referred to as `poll` in all eleven code cells and the surrounding prose. A reader typing `polls` gets `NameError`. (Two other uses of the word in the chapter are ordinary English, not variable references.) |
| 2 | `# Generate 1000 random integers from 0 to (number of votes - 1)` above `rng.integers(low=0, high=n_votes-1, …)` | `numpy.random.Generator.integers` is **half-open** on `high`. With `high = n_votes-1` the draws run `0 … n_votes-2`, so the comment names exactly the one index the call excludes. The sibling cell already uses `high=n_votes`. |
| 3 | "we are still off by almost **10** percentage points" | The gap is 62.459 − 54.223 = **8.24**. Left as wording rather than changed. |

## A7 · `pca` — 5

| # | Claim | Why it is false |
|---|---|---|
| 1 | "If an $m\times n$ matrix $Q$ has orthonormal columns, $QQ^T = I_m$ and $Q^TQ = I_n$" | Only the second holds in general. $QQ^T = I_m$ requires $m \le n$. |
| 2 | "$UU^T = I_n$ and $U^TU = I_d$" | The same error restated for the chapter's own $U$, which is $100 \times 4$ under `full_matrices=False`. Measured: `U.T@U == I_4` is **True**; `U@U.T == I_100` is **False** — it is a rank-4 projector whose diagonal runs 0.83, 0.14, 0.01, 0.04, 0.09. The identity holds only for the *full* SVD, which the chapter explicitly tells the reader not to use. |
| 3 | Component-score proof: `(1/n)X̃ᵀX̃ = (1/n)V S Vᵀ` on three consecutive lines | The square is dropped. On the **centered** SVD: `X̃ᵀX̃/n == V(S²/n)Vᵀ` is True, `V(S/n)Vᵀ` is False (diagonals 7.7, 5.3, 338.7, 50.8 against 0.16, 0.14, 1.75, 0.43). The line directly above derives $VS^2V^T$ correctly, and the line below reads $\frac1n S_j^2$ — so the three bad lines are an anomaly, not a belief. |
| 4 | "There are several ways to scale biplot vectors — in this course, **we plot the direction itself**." | The biplot cell plots `sqrt(s[0])*vt[0]` and `sqrt(s[1])*vt[1]`. Because the two axes are scaled by *different* positive constants, this is anisotropic and rotates each arrow — by up to **19°**, median 10°. The plotted arrows are not $(v_{1j}, v_{2j})$. |
| 5 | Alt text: "**Dataset 3** has **three columns**: height (in), weight (kg), weight (lbs), and age" | Opening `dataset4.png`: it has **four** columns, its own caption reads "**Dataset 4**", and the alt text lists four immediately after saying three. The surrounding prose called it Dataset 3 as well. |

## A8 · `eda` — 4

| # | Claim | Why it is false |
|---|---|---|
| 1 | "The number of months should have 62 or 61 instances (**March 1957**–August 2019)" | The file starts **1958-03**. The chapter states the correct range fifteen lines earlier, and 1957 would give 63 for months 3–8. |
| 2 | pandas pane comment: `# 2. Replace NaN with -99.99` above `co2.replace(-99.99, np.nan)` | It does the reverse. Inherited from the pandas original; the conversion corrected the Polars side, so the two tabs described opposite operations. |
| 3 | fig-alt: "A lineplot of the monthly averages **from the 1960s to the 1980s**" | The cell is `sns.lineplot(x='DecDate', y='Avg', data=co2)` with no filter; `DecDate` runs **1958.2 → 2019.6**. The alt hands a screen-reader user a 20-year window on a 62-year chart and truncates the "larger as time goes on" story at 1984. |
| 4 | fig-alt: "**Most of the data is near 400**" | Binning the column the figure actually plots: the mass spans 310–415 with the tallest bars in the low 320s (counts 78, 116, 88, 80, 89, 70, 61, 61, 52, 36), plus one isolated bin below zero for the seven −99.99 sentinels. |

## A9 · `visualization_1` — 2

| # | Claim | Why it is false |
|---|---|---|
| 1 | fig-alt: "Distribution with a **long right tail**" | The cell's own `plt.title` two lines below reads "Distribution with a long **left** tail", and the markdown above introduces it as the left-skew example. Measured: skew **−1.425**, mean 88.8 *below* median 96.0. The alt text's second sentence is correct; only the opening clause is wrong — it looks copied from the neighbouring right-skew figure, where the same sentence is true. |
| 2 | "The **whiskers** of a box-plot are the two points that lie at [Q1 − 1.5·IQR] and [Q3 + 1.5·IQR]" | Those are the **fences**. seaborn/matplotlib draw each whisker to the most extreme *observed* value still inside them. Measured on the chapter's own figure: fences at −3.125 and 9.075; whiskers drawn at **−3.1 and 8.5**. The upper one is off by 0.575, visible on the axis. The chapter's next sentence is what is actually true of the drawn whiskers. |

## A10 · `modeling_slr` — 2

| # | Claim | Why it is false |
|---|---|---|
| 1 | "when $\bar x = 0$, $\bar y = 0$, $\sigma_x = 1$, **or** $\sigma_y = 1$ … $r = \frac1n\sum x_i y_i$" | The identity needs all four **together** (i.e. both variables in standard units), which is what the parenthetical then says. Satisfying one branch alone: with $\bar x = 0$ only, $r = 0.8$ while $\frac1n\sum x_iy_i = 1.6$ — off by a factor of two. |
| 2 | Anscombe's quartet: "they actually all have **identical** means, standard deviations, correlation, and RMSE!" | Only $\bar x$ (9 exactly) and $\sigma_x$ ($\sqrt{10}$ exactly) are identical. $\bar y$, $\sigma_y$, $r$ and RMSE all differ — **and they differ at the precision the chapter prints**. The committed output directly beneath reads `r = 0.816, 0.816, 0.816, 0.817` and `RMSE 1.119, 1.119, 1.118, 1.118`. A reader told to compare the statistics sees the mismatch. |

## A11 · `ols` — 2

| # | Claim | Why it is false |
|---|---|---|
| 1 | "`FG`, the average number of **(2-point)** field goals per game" | `FG` is **total** field goals, threes included: `2P + 3P − FG` is 0 for every row to within 0.1 rounding, and the dataset has a separate `2P` column. The points identity settles it — `PTS = 2·FG + 3P + FT` reconstructs `PTS` with mean error **0.05**, while the 2-point reading (`2·FG + 3·3P + FT`) misses by **1.77** per game, up to 10.2. This is load-bearing: the fitted coefficient on `FG` is **2.517**, not 2, precisely because threes are in there, and a student told otherwise cannot read it. |
| 2 | "The subscript 2 indicates that we are computing the L2, or **squared norm**." | The definition two lines above is $\sqrt{\sum(a_i-b_i)^2}$ — a square root. The chapter draws the distinction itself eleven lines later ("the superscript 2 outside the parentheses means we are *squaring* the norm"). If $\|\cdot\|_2$ were already squared, the MSE formula would be a fourth power. |

## A12 · `regex` — 2

| # | Claim | Why it is false |
|---|---|---|
| 1 | Reference table lists `5005005` under "**Doesn't Match**" for `5.*?5` | `re.fullmatch(r"5.*?5", "5005005")` returns a match. Backtracking lets the lazy quantifier expand to satisfy the anchor-free full match; lazy and greedy differ in *which* match, not *whether*. Every other row of that table and the two before it is correct. Replaced with `500` and `005`, both verified non-matching. |
| 2 | Mapping table pairs `'_' in s` with `ser.str.contains(_)` | Correct as an operation mapping, but `contains` is **regex by default**, exactly like `replace_all` — which the chapter does warn about. `pl.Series(["cowscom"]).str.contains("cow.com")` is `True`; `literal=True` gives `False`. |

## A13 · `visualization_2` — 1

| # | Claim | Why it is false |
|---|---|---|
| 1 | "considering the gross national income variable … **looking at the y values** … compressing the **vertical** axis" | Gross national income is on the **x**-axis (`plt.scatter(df["inc"], df["lit"])`, `plt.xlabel("Gross national income per capita")`). The skew is on the axis the sentence doesn't name: `inc` skew **+3.325** (right-skewed, gets the log), `lit` skew **−1.25** (left-skewed, gets a power). The paragraph then continues correctly about "the horizontal axis" and the next cell applies `np.log` to x — so the middle clause belongs to the *following* paragraph, which repeats the reasoning for y. |

---

# B. Introduced by the conversion (27)

All fixed. They fall into four causes, and the comparison tabs account for twenty of them.

## B1 · A comparison tab asserted that two things are the same operation — 13

Most chapters carry pandas/Polars comparison tab-sets. They are paired **by cell id**: the pandas
half is the same cell's source and committed output from before the conversion. That assumes the
conversion changed how a cell is *spelled*, not what it *does*. Where that assumption broke, the two
panes sit under one heading asserting an equivalence that is false — and **no gate can see it**,
because both halves are real, executed output of real code.

| chapter · cell | Polars pane | pandas pane | Why the pairing is false |
|---|---|---|---|
| `intro_lec` · `fba44498` | `pl.Series("ratings", [...])` — names a Series | `pd.Series([...], index=["a","b","c"])` — labels its rows | Different operations. The prose above says "a name can be passed as the first argument"; followed literally on the pandas tab that gives `pd.Series("ratings", [-1,10,2])`, where the string becomes the **values** and the list becomes the index. Nothing raises. |
| `intro_lec` · `cb6cff88` | `s.cast(pl.Float64)` | `s.index = [...]` | The prose says the call returns a new Series and changes the data type. The pandas half mutates in place and changes no dtype — its own committed output still reads `dtype: int64`. |
| `intro_lec` · `53a863ee` | `s.dtype` | `s.index` | One reads a data type, the other reads row labels. |
| `intro_lec` · `3117fc63` | `.to_list()` → `list` | `.values` → `ndarray` | Under a shared comment asserting they are the same call. This is the **first** pandas/Polars pair in the book, so `.values ≡ .to_list()` is the mapping a reader carries out of it. The honest twin is `.tolist()`. |
| `intro_lec` · `12449aec` | name and dtype | a bare `s.index` | Prints `Index(['a','b','c'])` — labels that came from `fba44498`'s pandas half, which is no longer on the page. |
| `eda` · `b432c276` | `dt.weekday()` — Monday = 1 … Sunday = 7 | `dt.dayofweek` — Monday = 0 … Sunday = 6 | The prose above **both** tabs announces "Monday = 1", so the pandas pane prints an output that contradicts the sentence introducing it. Off by one for every row. |
| `eda` · `719dc1a4` | `read_csv(has_header=False, skip_rows=72)` → `(738, 1)`, one string column | `read_csv(..., sep=r'\s+')` → `(738, 7)`, split and typed | The prose below says "each record is still one long string … **We need to do more EDA**". False on the pandas tab, where the parsing is already finished before the section starts. |
| `eda` · `ef3fe041` | `# 2. Replace -99.99 with null` | `# 2. Replace NaN with -99.99` | The Polars comment was corrected during conversion; the pandas one is the original's error. The tab published two comments describing opposite operations under one heading. |
| `regex` · `1ba6f098` | `extract_groups(...).struct.unnest()` — each group's **first** match, non-matching rows kept as null | `str.extractall(...)` — **every** match, non-matching rows dropped, MultiIndex | The row for `"forty"` appears in one pane and not the other; the second SSN on line 2 appears in one and not the other. The conversion deliberately moved this cell from all-matches to first-match, and the chapter teaches all-matches separately at another cell. |
| `pca` · `a4377823` | `U` column 4 = `0.894121, -0.353004, …` | `0.967868, -0.151231, …` | `rectangle` has **rank 3**, so the fourth singular value is ~1e−14 and its singular vector spans the null space — LAPACK picks it arbitrarily. Verified `np.array_equal(U, U_pandas)` is **True**: the two libraries agree exactly. What differs is the run, not the library, and the tab invited the reader to conclude otherwise. |
| `pca` · `f5849357` | `Vt` row 3 = `-5.27e-17` | `-8.70e-17` | Same null-space arbitrariness; `np.array_equal(Vt, Vt_pandas)` is also True. |
| `modeling_slr` · `e83b8086` | `theta_0: 3.00, theta_1: 0.50` | a literal TAB then `heta_0: 3.00` | The pandas pane republishes the `f"\theta_0"` escape bug that **the conversion fixed**, framing it as a pandas/Polars difference. pandas does not mangle theta labels. This was the chapter's only twinnable cell, so it now carries none. |
| `polars_1` · `9ed57619` / `82a35df6` | Polars sorts nulls **first** | pandas sorts `NaN` **last** | The prose read "Sorting from highest to lowest put the missing count at the top" — false of what a reader on the pandas tab is looking at, and the next cell's pandas pane is byte-identical to the previous one, so a pandas reader watches nothing move under a sentence about `nulls_last=True`. Fixed by naming the library in the sentence, since the contrast is the lesson. |

## B1b · A comparison tab republished an error the conversion had just fixed — 7

Found by auditing this document against the tree. When the conversion's *only* change to a cell was
correcting a wrong comment, a mislabelled `print`, or an off-by-one, pairing on cell id put the
corrected Polars code beside the **uncorrected pandas code** — under a heading saying "pandas", as
though the libraries differed. They do not. In four of these the cell contains no pandas at all, so
the tab invented a library difference out of a bug fix, and kept the false statement on the page,
which is exactly what fixing it was for. Four of the seven twins existed *only* because of those
comment edits.

| chapter · cell | What the pandas pane still said | Why that is not a library difference |
|---|---|---|
| `gradient_descent` · `ae89e84d` | "returns … the optimal input value of x which **minimizes f**" | The cell is `scipy.optimize.minimize`. No pandas, and the claim is false in both — it prints 2.393, a local minimum. |
| `gradient_descent` · `cac7a125` | docstring "Performs **n** steps" | Off-by-one; the loop performs n−1 and returns n guesses. |
| `cv_regularization` · `d4521d3e` | "The alpha parameter represents our lambda term" | `alpha` is sklearn's parameter, identical from either library — and it is λ/2, not λ. |
| `cv_regularization` · `469bfd8e` | "alpha represents the hyperparameter lambda" | Same; Ridge's alpha is *n*λ. |
| `inference_causality` · `ce1d6713` | two MSEs printed under an `RMSE` label | The conversion corrected the labels; the pane kept them wrong. |
| `sampling` · `04510ea5` · `b37cf863` | `rng.integers(low=0, high=n_votes-1, …)` | Both panes call `numpy.random.Generator.integers`. The tab showed one numpy call two ways because one side had the pre-existing off-by-one. |

All seven twins removed, with the reason recorded in `conversion/tab_twins_data.py`. Counts after:
`gradient_descent` 4, `cv_regularization` 1, `inference_causality` 7, `sampling` 8.

## B2 · Tooling made a page assert something false — 5

| # | What the page said | Why it was false |
|---|---|---|
| 1 | Four pandas panes printed `<class 'pandas.core.groupby.generic.DataFrameGroupBy'>`, and long results did not wrap | The pane generator rendered with `repr`. A notebook renders through IPython's pretty printer, which drops the `<class '…'>` wrapper and wraps at 79 columns — and the Polars pane beside it, taken from a real executed cell, showed the notebook form. So the tab claimed pandas prints something it does not. |
| 2 | `pca` · `5880e99c`'s pane showed `(441, 42)` and nothing else | The pane generator returned only the **first** output that carried text. A cell that prints *and* returns a value has two, so the pivoted table vanished — under prose reading "Each legislator becomes one row … and each roll call becomes a column of 0s and 1s", which nothing visible then showed. |
| 3 | `inference_causality` · `add45dc7`'s pane ended in `print("RMSE", …)` above an output block with no printed line | Same truncation. |
| 4 | `regex` · `533afe7f`'s pane showed one of the two frames a `display(); display()` cell renders | Same truncation — and it broke the section's argument, which is that two differently-spelled county columns canonicalise to the same value. The reader saw one side of the match. |
| 5 | `polars_2` published the same `read_csv` tab-set **twice**, byte-identical | A marker rename left the old block behind: the replace looked for the new spelling, missed, and inserted a second copy. |

## B3 · Prose written during the conversion — 2

| # | Claim | Why it was false |
|---|---|---|
| 1 | `polars_2`: "`elections.filter(pl.col("%") < 45)` … would keep Lincoln while **discarding the winners of every other year**" | It keeps **117 rows across 44 years**, including **five** winners (1824, 1860, 1912, 1968, 1992). Rewritten around what actually happens: it keeps John Quincy Adams's 42.8% from 1824 while throwing away Andrew Jackson's 57.2% in the same election — the row that gives the number its meaning. |
| 2 | `sampling`: "We can **also take a sample** by choosing the row positions ourselves", under an **SRS** heading | `rng.integers` draws independently, so the same voter can be picked twice. That is the *uniform random sample with replacement* the chapter defines twenty lines earlier — the other scheme, introduced as though it were the same one. (The pre-conversion text made a claim about speed and asserted nothing about the sampling scheme.) |

---

# How four of these fixes were reported done and were not

Worth recording, because it is the same failure this project spent a week finding in its own
tooling.

Four `constant_model_loss_transformations` fixes — the 1000-vs-1033 sentence, both MAE alt texts,
and the "infinitely many" table row — were **reported as applied and never written to disk**. The
script that made them ran its substitutions into a string and called `write()` at the *end*. The
fifth substitution raised an `AssertionError` on a LaTeX string that did not match, so the function
exited before the write — discarding the four edits that had already succeeded, **after printing a
success line for each one**. A second script then fixed only the remaining three items and never
went back.

The verification afterwards ran the gate battery, which was green, because none of those four
sentences is anything a gate can see. It took auditing this document string-by-string against the
tree to find them, four days and one commit later.

The correction: every fix in this file is now verified by searching the tree for its post-fix text,
and the scripts write after each substitution rather than at the end, so a later failure cannot
discard an earlier success.

# Two reported errors that did not survive checking

Recorded because the discipline is the point: a reviewer's finding is a hypothesis until something
re-derives it.

| Reported | What checking showed |
|---|---|
| `eda`'s histogram alt text is wrong because "the mass is at the low end" | The reviewer binned `Avg > 0`. The figure is `sns.displot(co2, x='Avg')`, which plots the **whole** column including the seven `−99.99` sentinels, stretching the axis to −100. The alt text *is* wrong — but so was the correction. The replacement was written from the binning of what is actually drawn. |
| `pca`'s component-score proof drops a square | Correct — but my own first check said **both** forms were false, which would have made the reviewer wrong. I had taken the SVD of the *uncentered* matrix and multiplied it against the centered one. Redone properly, `X̃ᵀX̃/n == V(S²/n)Vᵀ` is True and `V(S/n)Vᵀ` is False. I nearly reported the opposite. |

---

# What this leaves open

- **The pre-existing half is 52 of 79 and belongs to whoever owns the course content.** Fixed here,
  but buried inside a 160-path Polars diff, no content owner will see them as content decisions.
  Splitting them into their own change against `main` is worth considering.
- **Claims that need a source we cannot reach** were recorded as unverifiable rather than guessed:
  documentation URLs (the symbol half is executable, the URL half is not), the Anthropic RCT
  described in `inference_causality`, the "5–8% of the world is red-green colour blind" figure, the
  Excel row/column limits, and the Gallup and *Literary Digest* historical claims.
- **Wording left alone deliberately:** `sampling`'s "almost 10 percentage points" for a gap of 8.24,
  `pca`'s "our matrix is linearly independent" where the argument wants *dependent* (the sentence is
  true as written), `pca`'s "most of the data is explained by the first two or three dimensions"
  (46.7% and 52.8%), and `logistic_regression_2`'s "precision and recall are inversely related",
  which the next sentence hedges.
- **`eda`'s `data_year(data, year)` ignores its `year` parameter** and hardcodes 1958. Inherited from
  the pandas original, and it is only ever called with 1958, so the figure is right today.
