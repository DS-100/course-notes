# gradient_descent — change report

`887a578b0a4b:content/gradient_descent/gradient_descent.ipynb` → `content/gradient_descent/gradient_descent.ipynb`

**Tier B · 39 changes:** output 10 · prose 9 · dropdown 5 · tab-twins 4 · code 10 · metadata 1

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

Three Polars sites, and a large content correction riding along with them. Seven of the nine prose reviews are §A1 fixes to pre-existing false claims rather than conversion fallout, and the biggest of them rewrites the chapter's motivation: the baseline asserted four times that `sklearn` and `scipy` run gradient descent, and neither does. Three things to look at: C10/C11/C16/C17, the closed-form reframing (§A1 1–4, all pre-existing — a content decision staff may prefer to take against `main`); C22/C26, where the off-by-one docstring fix left an ungrammatical sentence that ships to the reader; and C32–C34, three committed numbers that moved in their last digits although CONVERSIONS.md's entry for this chapter records "Constants changed: None".

## Needs review

- [C3](#c3) · cell 3: 1. Choose a model
- [C7](#c7) · cell 8 [markdown]
- [C10](#c10) · cell 15 [markdown]
- [C11](#c11) · cell 17 [markdown]
- [C14](#c14) · cell 35 [markdown]
- [C16](#c16) · cell 39 [markdown]
- [C17](#c17) · cell 39 [markdown]
- [C18](#c18) · cell 41: Algorithm Attempt 1
- [C19](#c19) · cell 41: Algorithm Attempt 1

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C30](#c30) · `import polars as pl`
- [C31](#c31) · `Y_hat = X @ theta_hat`
- [C32](#c32) · `my_model.intercept_`
- [C33](#c33) · `from sklearn.metrics import mean_squared_error`
- [C34](#c34) · `two_feature_model = LinearRegression()`
- [C35](#c35) · `pl.DataFrame({"Y_hat from OLS":np.squeeze(Y_hat), "Y_hat from sklearn"`
- [C36](#c36) · `xs = np.linspace(1, 7, 200)`
- [C37](#c37) · `import plotly.graph_objects as go`
- [C38](#c38) · `df = pl.from_pandas(sns.load_dataset("tips"))`
- [C39](#c39) · `def gradient_descent(df, initial_guess, alpha, n):`

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C4](#c4) · cell 3: Implementing Derived Formulas in Code
- [C22](#c22) · cell 44 [markdown]
- [C23](#c23) · cell 44 [markdown]
- [C24](#c24) · cell 44 [markdown]
- [C25](#c25) · cell 44 [markdown]

## Changes

<a id="c1"></a>
### C1 · cell 2 [code] · code

baseline L28 → branch L28

```diff
- import pandas as pd
+ import polars as pl
```

**Why:** Import swap; `pl` is the course alias.
**Output:** same — no output.

<a id="c2"></a>
### C2 · cell 2 [code] · code

baseline L34 → branch L34

```diff
- pd.options.mode.chained_assignment = None  # default='warn'
```

**Why:** `pd.options.mode.chained_assignment` silences pandas' `SettingWithCopyWarning`, which has no Polars counterpart: frames are immutable, so the chained-assignment hazard the option covers cannot arise. Deleted rather than translated.
**Output:** same — the line printed nothing.

<a id="c3"></a>
### C3 · cell 3: 1. Choose a model · prose · **REVIEW**

baseline L55 → branch L54

```diff
- # :alt:""
+ # :alt: Two diagrams. On the left, "The Data": an n-by-p covariate matrix X of features beside
+ #   an n-by-1 response vector Y. On the right, the equation Y-hat = X-theta, drawn as an n-by-1
+ #   vector Y-hat equal to the n-by-p matrix X times a p-by-1 parameter vector theta.
```

**Why:** The baseline shipped `:alt:""` — an empty alt on the figure that introduces X, Y and theta. Filled in with a description of both panels. CONVERSIONS.md lists this and two other empty alts in this chapter as pre-existing content debt.
**Verdict:** optional — an accessibility fix the conversion did not require.
**Minimal alternative:** Restore `:alt:""` as in the baseline. The cost is that a screen-reader user gets nothing at all for the chapter's defining diagram.

<a id="c4"></a>
### C4 · cell 3: Implementing Derived Formulas in Code · dropdown

baseline L122 → branch L123 · spans code and prose; mirror of the next code cell (hard rule 3)

```diff
+ # import polars as pl
+ # import seaborn as sns
+ # import numpy as np
+ #
+ # penguins = pl.from_pandas(sns.load_dataset("penguins"))
+ # penguins = penguins.filter(pl.col("species") == "Adelie").drop_nulls()
+ # penguins.head()
+ # ```
+ # ````
+ 
+ # %% tags=["remove-input", "remove-output"]
+ import polars as pl
+ import seaborn as sns
+ import numpy as np
+ 
+ penguins = pl.from_pandas(sns.load_dataset("penguins"))
+ penguins = penguins.filter(pl.col("species") == "Adelie").drop_nulls()
+ penguins.head()
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 4fb8031e -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # import polars as pl
+ # import seaborn as sns
+ # import numpy as np
+ #
+ # penguins = pl.from_pandas(sns.load_dataset("penguins"))
+ # penguins = penguins.filter(pl.col("species") == "Adelie").drop_nulls()
+ # penguins.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 7)
+ # ┌─────────┬───────────┬────────────────┬───────────────┬───────────────────┬─────────────┬────────┐
+ # │ species ┆ island    ┆ bill_length_mm ┆ bill_depth_mm ┆ flipper_length_mm ┆ body_mass_g ┆ sex    │
+ # │ ---     ┆ ---       ┆ ---            ┆ ---           ┆ ---               ┆ ---         ┆ ---    │
+ # │ str     ┆ str       ┆ f64            ┆ f64           ┆ f64               ┆ f64         ┆ str    │
+ … 13 more lines
```

**Why:** Dropdown mirror of the setup cell, converted in the same pass as its code cell (hard rule 3). Verified: the dropdown's `python` block matches the code cell verbatim. `sns.load_dataset` returns a **pandas** frame, so `pl.from_pandas` is the crossing point — a pandas site that no `pd.` grep finds; `.dropna()` → `.drop_nulls()`.
**Output:** differs — repr only; the same five Adelie rows survive the filter.

<a id="c5"></a>
### C5 · cell 5 [markdown] · tab-twins

baseline L130 → branch L184 · spans code and prose

```diff
- # ````
- 
- # %% tags=["remove-input"]
- import pandas as pd
- import seaborn as sns
- import numpy as np
- 
- penguins = sns.load_dataset("penguins")
- penguins = penguins[penguins["species"] == "Adelie"].dropna()
- penguins.head()
+ #
+ # ```text
+ #   species     island  bill_length_mm  bill_depth_mm  flipper_length_mm  \
+ # 0  Adelie  Torgersen            39.1           18.7              181.0
+ # 1  Adelie  Torgersen            39.5           17.4              186.0
+ # 2  Adelie  Torgersen            40.3           18.0              195.0
+ # 4  Adelie  Torgersen            36.7           19.3              193.0
+ # 5  Adelie  Torgersen            39.3           20.6              190.0
+ #
+ #    body_mass_g     sex
+ # 0       3750.0    Male
+ # 1       3800.0  Female
+ # 2       3250.0  Female
+ # 4       3450.0  Female
+ # 5       3650.0    Male
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** Twin `4fb8031e`'s pandas pane. One operation on both sides: filter to Adelie, drop incomplete rows, show five.
**Output:** differs — Polars prints `shape: (5, 7)` and a dtype row; pandas prints the surviving original row labels 0, 1, 2, 4, 5, which is the only information the Polars pane does not carry.

<a id="c6"></a>
### C6 · cell 7 [code] · code

baseline L146 → branch L209

```diff
- penguins["bias"] = np.ones(len(penguins), dtype=int)
+ penguins = penguins.with_columns(pl.Series("bias", np.ones(len(penguins), dtype=int)))
```

**Why:** `penguins["bias"] = np.ones(...)` has no in-place form. `with_columns(pl.Series("bias", ...))` builds a full-length `Series` because Polars will not broadcast a scalar into a new column.
**Output:** same — `X` is built with `.to_numpy()` immediately afterwards and is unchanged.

<a id="c7"></a>
### C7 · cell 8 [markdown] · prose · **REVIEW**

baseline L170 → branch L233

```diff
- # * To take a transpose, call the `.T` attribute of an `NumPy` array or `DataFrame`
+ # * To take a transpose, call the `.T` attribute of a `NumPy` array
```

**Why:** Pre-existing text that the library change made false: `pl.DataFrame` has no `.T`, and by this point `X` is already an ndarray, so `.T` is only ever seen on NumPy. CONTRADICTIONS.md records this among the three pre-existing errors the conversion repaired in passing.
**Verdict:** necessary — a fix to a claim that would be false as written (pre-existing text, newly false: pandas frames do have `.T`).

<a id="c8"></a>
### C8 · cell 11 [code] · metadata

baseline L184 → branch L247

```diff
- # %%
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c9"></a>
### C9 · cell 11 [code] · tab-twins

baseline L186 → branch L249 · spans code and prose

```diff
- pd.DataFrame(Y_hat).head()
+ pl.DataFrame(Y_hat).head()
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin b53a37f9 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # Y_hat = X @ theta_hat
+ # pl.DataFrame(Y_hat).head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 1)
+ # ┌───────────┐
+ # │ column_0  │
+ # │ ---       │
+ # │ f64       │
+ # ╞═══════════╡
+ # │ 18.322561 │
+ # │ 18.445578 │
+ # │ 17.721412 │
+ # │ 17.997254 │
+ # │ 18.263268 │
+ # └───────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # Y_hat = X @ theta_hat
+ # pd.DataFrame(Y_hat).head()
+ # ```
+ #
+ # ```text
+ #            0
+ # 0  18.322561
+ # 1  18.445578
+ # 2  17.721412
+ … 6 more lines
```

**Why:** Twin `b53a37f9`. `pd.DataFrame(Y_hat)` → `pl.DataFrame(Y_hat)`; the frame exists only to print the first five predictions.
**Output:** differs — Polars names the single column `column_0` where pandas named it `0`. No prose names the column (grepped repo-wide), so no `.rename()` was added to force the pandas label back.

<a id="c10"></a>
### C10 · cell 15 [markdown] · prose · **REVIEW**

baseline L247 → branch L355

```diff
- # Before the model can make predictions, we will need to fit it to our training data. When we fit the model, `sklearn` will run gradient descent behind the scenes to determine the optimal model parameters. It will then save these model parameters to our model instance for future use.
+ # Before the model can make predictions, we will need to fit it to our training data. When we fit the model, `sklearn` solves for the optimal model parameters directly: for `LinearRegression` it hands the problem to a least-squares solver, `scipy.linalg.lstsq`, which computes the answer in one shot rather than searching for it. It will then save these model parameters to our model instance for future use.
```

**Why:** §A1 #1, **pre-existing** — verbatim in the baseline. Verified in the d100 env: `inspect.getsource(LinearRegression.fit)` calls `scipy.linalg.lstsq`, a one-shot least-squares solve. The class exposes no learning rate, no `max_iter` and no `n_iter_`.
**Verdict:** necessary — a fix to a claim that was false. Provenance is pre-existing course content, so staff may prefer the fix against `main`.

<a id="c11"></a>
### C11 · cell 17 [markdown] · prose · **REVIEW**

baseline L263 → branch L371

```diff
- # And in just three lines of code, our model has run gradient descent to determine the optimal model parameters! Our single-feature model takes the form:
+ # And in just three lines of code, our model has found the optimal model parameters! Our single-feature model takes the form:
```

**Why:** §A1 #2, pre-existing — the same claim in the summary sentence, reduced to what the three lines actually did.
**Verdict:** necessary — a fix to a claim that was false (pre-existing).

<a id="c12"></a>
### C12 · cell 27 [code] · code

baseline L323 → branch L431

```diff
- # %%
- pd.DataFrame({"Y_hat from OLS":np.squeeze(Y_hat), "Y_hat from sklearn":Y_hat_two_features}).head()
+ # %% tags=["remove-input", "remove-output"]
+ pl.DataFrame({"Y_hat from OLS":np.squeeze(Y_hat), "Y_hat from sklearn":Y_hat_two_features}).head()
```

**Why:** `pd.DataFrame` → `pl.DataFrame`, plus tags so the tab-set below carries the display.
**Output:** differs — repr only; both columns agree to six decimals under either library.

<a id="c13"></a>
### C13 · cell 28 [markdown] · tab-twins

baseline L326 → branch L434

```diff
+ # %% [markdown]
+ # <!-- tab-twins:begin 716464e0 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # pl.DataFrame({"Y_hat from OLS":np.squeeze(Y_hat), "Y_hat from sklearn":Y_hat_two_features}).head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 2)
+ # ┌────────────────┬────────────────────┐
+ # │ Y_hat from OLS ┆ Y_hat from sklearn │
+ # │ ---            ┆ ---                │
+ # │ f64            ┆ f64                │
+ # ╞════════════════╪════════════════════╡
+ # │ 18.322561      ┆ 18.322561          │
+ # │ 18.445578      ┆ 18.445578          │
+ # │ 17.721412      ┆ 17.721412          │
+ # │ 17.997254      ┆ 17.997254          │
+ # │ 18.263268      ┆ 18.263268          │
+ # └────────────────┴────────────────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # pd.DataFrame({"Y_hat from OLS":np.squeeze(Y_hat), "Y_hat from sklearn":Y_hat_two_features}).head()
+ # ```
+ #
+ # ```text
+ #    Y_hat from OLS  Y_hat from sklearn
+ # 0       18.322561           18.322561
+ # 1       18.445578           18.445578
+ # 2       17.721412           17.721412
+ # 3       17.997254           17.997254
+ # 4       18.263268           18.263268
+ # ```
+ # ::::
+ … 2 more lines
```

**Why:** Twin `716464e0`. The cell's job is to show that the hand-derived OLS predictions and sklearn's agree, and both panes show that.
**Output:** differs — repr only; identical values.

<a id="c14"></a>
### C14 · cell 35 [markdown] · prose · **REVIEW**

baseline L377 → branch L527

```diff
- # This process is essentially the same as before where we made a graphical plot, it's just that we're only looking at 20 selected points.
+ # This process is essentially the same as before where we made a graphical plot, it's just that we're only looking at five selected points.
```

**Why:** §A1 #6, pre-existing — the plot below the sentence is `sparse_xs = np.linspace(1, 7, 5)`, five points, not twenty. Verified against the branch cell.
**Verdict:** necessary — a fix to a claim that was false (pre-existing). Staff note: §A1 also observes that the `simple_minimize` cell above uses six guesses; this sentence is about the plot below it, so that neighbouring count is untouched and may want its own look.

<a id="c15"></a>
### C15 · cell 38 [code] · code

baseline L422 → branch L572

```diff
- # takes a function f and a starting point x0 and returns a readout
- # with the optimal input value of x which minimizes f
+ # takes a function f and a starting point x0 and returns a readout with an
+ # input value of x where f is at a minimum -- note it walks downhill from x0,
+ # so it finds the *local* minimum near 2.39, not the global one near 5.33
```

**Why:** §A1 #5, pre-existing — the comment promised "the optimal input value of x which minimizes f" above a cell that prints `x: [2.393]`, a local minimum, while the prose two cells earlier says the minimum is around 5.3. Rewritten to say which minimum is found and why. The cell's tab twin (`ae89e84d`) was deleted rather than published, because its pandas pane would have republished the uncorrected comment under a heading claiming a library difference in a cell containing no pandas (§B1b).
**Output:** same — the printed `x` is unchanged; only the comment above it moved.

<a id="c16"></a>
### C16 · cell 39 [markdown] · prose · **REVIEW**

baseline L427 → branch L578

```diff
- # `scipy.optimize.minimize` is great. It may also seem a bit magical. How could you write a function that can find the minimum of any mathematical function? There are a number of ways to do this, which we'll explore in today's lecture, eventually arriving at the important idea of **gradient descent**, which is the principle that `scipy.optimize.minimize` uses.
+ # `scipy.optimize.minimize` is great. It may also seem a bit magical. How could you write a function that can find the minimum of any mathematical function? There are a number of ways to do this, which we'll explore in today's lecture, eventually arriving at the important idea of **gradient descent**. `scipy.optimize.minimize` does not use gradient descent itself — with no gradient supplied it defaults to BFGS, a close relative that also walks downhill but sizes each step using an approximation of the curvature. Gradient descent is the simpler idea underneath it, and the one worth understanding first.
```

**Why:** §A1 #4, pre-existing. Verified: with no gradient supplied, `scipy.optimize.minimize` defaults to BFGS — the returned object carries `hess_inv`. Its step is −H⁻¹∇f, with no learning rate, which is the defining feature the chapter's very next line describes.
**Verdict:** necessary — a fix to a claim that was false (pre-existing).

<a id="c17"></a>
### C17 · cell 39 [markdown] · prose · **REVIEW**

baseline L429 → branch L580

```diff
- # It turns out that under the hood, the `fit` method for `LinearRegression` models uses gradient descent. Gradient descent is also how much of machine learning works, including even advanced neural network models.
+ # `LinearRegression` does not actually need gradient descent: ordinary least squares has a closed-form solution, so `fit` can call a least-squares solver and be done. That is exactly why gradient descent matters — most models have no such formula, and then searching for the minimum is the only option available. It is how much of machine learning works, including even advanced neural network models.
```

**Why:** §A1 #3, pre-existing, and the load-bearing one: the section argues that closed forms need strong assumptions and gradient descent is the alternative, then claimed the closed-form estimator it had just derived was secretly the iterative one. Rewritten to the closed-form motivation — OLS has a formula, and that is exactly why gradient descent matters for the models that do not.
**Verdict:** necessary — a fix to a claim that was false. Largest content change across these four chapters and the one most worth a content owner's sign-off.

<a id="c18"></a>
### C18 · cell 41: Algorithm Attempt 1 · prose · **REVIEW**

baseline L531 → branch L682

```diff
- # :alt: ""
+ # :alt: Three panels labelled Step 1, Step 2 and Step 3. Each shows the same loss curve, which
+ #   has a shallow local dip near x=3 and a deeper global minimum near x=5. A filled green dot
+ #   marks the current guess and a hollow one the previous guess; across the three steps the
+ #   guess moves right, from about 4.3 to 5.1 to 5.6, descending into the global minimum.
```

**Why:** Baseline `:alt: ""` on `grad_descent_1.png`. Filled in from the figure.
**Verdict:** optional — accessibility, not conversion.
**Minimal alternative:** Restore `:alt: ""` as in the baseline.

<a id="c19"></a>
### C19 · cell 41: Algorithm Attempt 1 · prose · **REVIEW**

baseline L537 → branch L691

```diff
- # :alt: ""
+ # :alt: Two further panels, Step 4 and Step 5. The guess has reached the bottom of the global
+ #   minimum and now overshoots it: at Step 4 the filled dot sits just left of the previous
+ #   guess, at Step 5 just right of it. The guesses bounce back and forth across the minimum
+ #   instead of settling on it.
```

**Why:** Baseline `:alt: ""` on `grad_descent_2.png`. Filled in from the figure; this is the one that shows the guesses overshooting the minimum.
**Verdict:** optional — accessibility, not conversion.
**Minimal alternative:** Restore `:alt: ""` as in the baseline.

<a id="c20"></a>
### C20 · cell 42 [code] · code

baseline L616 → branch L773

```diff
- # %%
- df = sns.load_dataset("tips")
+ # %% tags=["remove-input", "remove-output"]
+ df = pl.from_pandas(sns.load_dataset("tips"))
```

**Why:** `sns.load_dataset` returns pandas, so this is a pandas site with no `pd.` in it; wrapped in `pl.from_pandas`.
**Output:** differs — repr, plus a dtype row in which `sex`, `smoker`, `day` and `time` read `cat`, because seaborn's categoricals survive the conversion.

<a id="c21"></a>
### C21 · cell 43 [markdown] · tab-twins

baseline L620 → branch L777

```diff
+ # %% [markdown]
+ # <!-- tab-twins:begin 46a06ec5 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # df = pl.from_pandas(sns.load_dataset("tips"))
+ # df.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 7)
+ # ┌────────────┬──────┬────────┬────────┬─────┬────────┬──────┐
+ # │ total_bill ┆ tip  ┆ sex    ┆ smoker ┆ day ┆ time   ┆ size │
+ # │ ---        ┆ ---  ┆ ---    ┆ ---    ┆ --- ┆ ---    ┆ ---  │
+ # │ f64        ┆ f64  ┆ cat    ┆ cat    ┆ cat ┆ cat    ┆ i64  │
+ # ╞════════════╪══════╪════════╪════════╪═════╪════════╪══════╡
+ # │ 16.99      ┆ 1.01 ┆ Female ┆ No     ┆ Sun ┆ Dinner ┆ 2    │
+ # │ 10.34      ┆ 1.66 ┆ Male   ┆ No     ┆ Sun ┆ Dinner ┆ 3    │
+ # │ 21.01      ┆ 3.5  ┆ Male   ┆ No     ┆ Sun ┆ Dinner ┆ 3    │
+ # │ 23.68      ┆ 3.31 ┆ Male   ┆ No     ┆ Sun ┆ Dinner ┆ 2    │
+ # │ 24.59      ┆ 3.61 ┆ Female ┆ No     ┆ Sun ┆ Dinner ┆ 4    │
+ # └────────────┴──────┴────────┴────────┴─────┴────────┴──────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # df = sns.load_dataset("tips")
+ # df.head()
+ # ```
+ #
+ # ```text
+ #    total_bill   tip     sex smoker  day    time  size
+ # 0       16.99  1.01  Female     No  Sun  Dinner     2
+ # 1       10.34  1.66    Male     No  Sun  Dinner     3
+ # 2       21.01  3.50    Male     No  Sun  Dinner     3
+ # 3       23.68  3.31    Male     No  Sun  Dinner     2
+ # 4       24.59  3.61  Female     No  Sun  Dinner     4
+ … 4 more lines
```

**Why:** Twin `46a06ec5`. The same five rows of `tips` on both panes.
**Output:** differs — repr and the `cat` dtypes; same values.

<a id="c22"></a>
### C22 · cell 44 [markdown] · dropdown

baseline L639 → branch L840 · mirror of the next code cell (hard rule 3)

```diff
- #     """Performs n steps of gradient descent on df using learning rate alpha starting
+ #     """Performs n-1 update steps of gradient descent, counting the starting guess on df using learning rate alpha starting
```

**Why:** Dropdown mirror of the `gradient_descent` docstring, moved with its code cell (hard rule 3). **The mirror does match the code cell it mirrors** — verified verbatim, including the defect. §A1 #7, pre-existing: the loop is `while len(guesses) < n` seeded with the initial guess, so `n=100` performs 99 updates and returns 100 guesses. But the replacement sentence is ungrammatical as it ships — "Performs n-1 update steps of gradient descent, counting the starting guess on df using learning rate alpha starting from initial_guess" — because the inserted clause landed in the middle of "on df using learning rate alpha". The fact is right; the sentence is not, and it is student-facing in both copies.
**Output:** same — a docstring; nothing prints it.

<a id="c23"></a>
### C23 · cell 44 [markdown] · dropdown

baseline L654 → branch L855 · mirror of the next code cell (hard rule 3)

```diff
- #     return np.mean((y_hat - y_obs) ** 2)
+ #     return ((y_hat - y_obs) ** 2).mean()
```

**Why:** Mirror of the MSE helper, moved with its code cell; verified identical to it. `np.mean` raises on a Polars `Series`, so the reduction moves onto the expression — this form also survives being handed a `Series` or an ndarray, which the helper is.
**Output:** same.

<a id="c24"></a>
### C24 · cell 44 [markdown] · dropdown

baseline L662 → branch L863 · mirror of the next code cell (hard rule 3)

```diff
- #     return np.mean(2 * (y_hat - y_obs) * x)
+ #     return (2 * (y_hat - y_obs) * x).mean()
```

**Why:** Same edit in the derivative helper, same reason; mirror verified identical to its code cell.
**Output:** same.

<a id="c25"></a>
### C25 · cell 44 [markdown] · dropdown

baseline L664 → branch L865 · mirror of the next code cell (hard rule 3)

```diff
- # loss_df = pd.DataFrame({"theta_1":np.linspace(-1.5, 1), "MSE":[mse_single_arg(theta_1) for theta_1 in np.linspace(-1.5, 1)]})
+ # loss_df = pl.DataFrame({"theta_1":np.linspace(-1.5, 1), "MSE":[mse_single_arg(theta_1) for theta_1 in np.linspace(-1.5, 1)]})
```

**Why:** `pd.DataFrame` → `pl.DataFrame` for the loss curve's frame; mirror verified identical to its code cell.
**Output:** same — the frame only feeds a plot.

<a id="c26"></a>
### C26 · cell 45 [code] · code

baseline L681 → branch L882

```diff
-     """Performs n steps of gradient descent on df using learning rate alpha starting
+     """Performs n-1 update steps of gradient descent, counting the starting guess on df using learning rate alpha starting
```

**Why:** The code-cell half of C22. The mirror and the cell are identical; the sentence is ungrammatical in both and should be re-worded.
**Output:** same.

<a id="c27"></a>
### C27 · cell 45 [code] · code

baseline L696 → branch L897

```diff
-     return np.mean((y_hat - y_obs) ** 2)
+     return ((y_hat - y_obs) ** 2).mean()
```

**Why:** Code-cell half of C23 — `np.mean` raises on a `Series`.
**Output:** same — the trajectory endpoint the cell prints is unchanged to all 17 digits.

<a id="c28"></a>
### C28 · cell 45 [code] · code

baseline L704 → branch L905

```diff
-     return np.mean(2 * (y_hat - y_obs) * x)
+     return (2 * (y_hat - y_obs) * x).mean()
```

**Why:** Code-cell half of C24.
**Output:** same.

<a id="c29"></a>
### C29 · cell 45 [code] · code

baseline L706 → branch L907

```diff
- loss_df = pd.DataFrame({"theta_1":np.linspace(-1.5, 1), "MSE":[mse_single_arg(theta_1) for theta_1 in np.linspace(-1.5, 1)]})
+ loss_df = pl.DataFrame({"theta_1":np.linspace(-1.5, 1), "MSE":[mse_single_arg(theta_1) for theta_1 in np.linspace(-1.5, 1)]})
```

**Why:** Code-cell half of C25.
**Output:** same.

<a id="c30"></a>
### C30 · `import polars as pl` · output

committed output

```diff
- [text]   species     island  bill_length_mm  bill_depth_mm  flipper_length_mm  \
- [text] 0  Adelie  Torgersen            39.1           18.7              181.0
- [text] 1  Adelie  Torgersen            39.5           17.4              186.0
- [text] 2  Adelie  Torgersen            40.3           18.0              195.0
- [text] 4  Adelie  Torgersen            36.7           19.3              193.0
- [text] 5  Adelie  Torgersen            39.3           20.6              190.0
- [text]
- [text]    body_mass_g     sex
- [text] 0       3750.0    Male
- [text] 1       3800.0  Female
- [text] 2       3250.0  Female
- [text] 4       3450.0  Female
- [text] 5       3650.0    Male
+ [text] shape: (5, 7)
+ [text] ┌─────────┬───────────┬────────────────┬───────────────┬───────────────────┬─────────────┬────────┐
+ [text] │ species ┆ island    ┆ bill_length_mm ┆ bill_depth_mm ┆ flipper_length_mm ┆ body_mass_g ┆ sex    │
+ [text] │ ---     ┆ ---       ┆ ---            ┆ ---           ┆ ---               ┆ ---         ┆ ---    │
+ [text] │ str     ┆ str       ┆ f64            ┆ f64           ┆ f64               ┆ f64         ┆ str    │
+ [text] ╞═════════╪═══════════╪════════════════╪═══════════════╪═══════════════════╪═════════════╪════════╡
+ [text] │ Adelie  ┆ Torgersen ┆ 39.1           ┆ 18.7          ┆ 181.0             ┆ 3750.0      ┆ Male   │
+ [text] │ Adelie  ┆ Torgersen ┆ 39.5           ┆ 17.4          ┆ 186.0             ┆ 3800.0      ┆ Female │
+ [text] │ Adelie  ┆ Torgersen ┆ 40.3           ┆ 18.0          ┆ 195.0             ┆ 3250.0      ┆ Female │
+ [text] │ Adelie  ┆ Torgersen ┆ 36.7           ┆ 19.3          ┆ 193.0             ┆ 3450.0      ┆ Female │
+ [text] │ Adelie  ┆ Torgersen ┆ 39.3           ┆ 20.6          ┆ 190.0             ┆ 3650.0      ┆ Male   │
+ [text] └─────────┴───────────┴────────────────┴───────────────┴───────────────────┴─────────────┴────────┘
```

**Why:** Re-executed after `pl.from_pandas` + `.filter` + `.drop_nulls`.
**Reader sees:** equivalent — the same five Adelie rows and seven columns. The only thing lost is the original row numbering (0, 1, 2, 4, 5), which no prose mentions.

<a id="c31"></a>
### C31 · `Y_hat = X @ theta_hat` · output

committed output

```diff
- [text]            0
- [text] 0  18.322561
- [text] 1  18.445578
- [text] 2  17.721412
- [text] 3  17.997254
- [text] 4  18.263268
+ [text] shape: (5, 1)
+ [text] ┌───────────┐
+ [text] │ column_0  │
+ [text] │ ---       │
+ [text] │ f64       │
+ [text] ╞═══════════╡
+ [text] │ 18.322561 │
+ [text] │ 18.445578 │
+ [text] │ 17.721412 │
+ [text] │ 17.997254 │
+ [text] │ 18.263268 │
+ [text] └───────────┘
```

**Why:** `pl.DataFrame(Y_hat)` names an unnamed column `column_0`.
**Reader sees:** equivalent — the same five predictions; only the column heading differs, and nothing refers to it.

<a id="c32"></a>
### C32 · `my_model.intercept_` · output

committed output

```diff
- [text] 7.297305899612299
+ [text] 7.297305899612301
```

**Why:** `LinearRegression` was fitted from a Polars-derived design matrix, so float accumulation order differs and the intercept moves in its last two digits (…299 → …301).
**Reader sees:** equivalent — the same intercept to 15 significant figures. Staff note: CONVERSIONS.md's `gradient_descent` entry states "Constants changed: None"; that holds for `theta_hat` and the trajectory endpoint, but not for this printed value or C33/C34.

<a id="c33"></a>
### C33 · `from sklearn.metrics import mean_squared_error` · output

committed output

```diff
- [stdout] The MSE of the model is 1.333877879980637
+ [stdout] The MSE of the model is 1.3338778799806374
```

**Why:** Same cause — the printed MSE gains a digit (1.333877879980637 → 1.3338778799806374).
**Reader sees:** equivalent — the same MSE to 15 significant figures; no prose quotes it.

<a id="c34"></a>
### C34 · `two_feature_model = LinearRegression()` · output

committed output

```diff
- [stdout] The MSE of the model is 0.9764070438844
+ [stdout] The MSE of the model is 0.9764070438843998
```

**Why:** Same cause, two-feature model (0.9764070438844 → 0.9764070438843998).
**Reader sees:** equivalent — the same MSE to 13 significant figures; no prose quotes it. It reads noisier than the baseline's shorter repr.

<a id="c35"></a>
### C35 · `pl.DataFrame({"Y_hat from OLS":np.squeeze(Y_hat), "Y_hat from sklearn"` · output

committed output

```diff
- [text]    Y_hat from OLS  Y_hat from sklearn
- [text] 0       18.322561           18.322561
- [text] 1       18.445578           18.445578
- [text] 2       17.721412           17.721412
- [text] 3       17.997254           17.997254
- [text] 4       18.263268           18.263268
+ [text] shape: (5, 2)
+ [text] ┌────────────────┬────────────────────┐
+ [text] │ Y_hat from OLS ┆ Y_hat from sklearn │
+ [text] │ ---            ┆ ---                │
+ [text] │ f64            ┆ f64                │
+ [text] ╞════════════════╪════════════════════╡
+ [text] │ 18.322561      ┆ 18.322561          │
+ [text] │ 18.445578      ┆ 18.445578          │
+ [text] │ 17.721412      ┆ 17.721412          │
+ [text] │ 17.997254      ┆ 17.997254          │
+ [text] │ 18.263268      ┆ 18.263268          │
+ [text] └────────────────┴────────────────────┘
```

**Why:** Re-executed; Polars table repr.
**Reader sees:** equivalent — the two columns still agree row for row, which is the cell's point.

<a id="c36"></a>
### C36 · `xs = np.linspace(1, 7, 200)` · output

committed output

```diff
- [plotly] figure md5:27a984a2f4
- [plotly] trace 0 scatter
- [plotly] trace 1 scatter
+ [plotly] figure md5:d1021e4441
+ [plotly] trace 0 scatter
+ [plotly] trace 1 scatter
```

**Why:** Nothing in the data moved. Both traces — the `arbitrary` curve over 200 points and the 5 sparse markers — decode byte-identical to the baseline, and no Polars reaches this cell at all. The md5 changes because the plotly that wrote the committed baseline emitted integer axis domains where the pinned 6.1.2 writes `[0.0, 1.0]`.
**Reader sees:** equivalent — a re-serialization, not a redraw.

<a id="c37"></a>
### C37 · `import plotly.graph_objects as go` · output

committed output

```diff
- [plotly] figure md5:91d63526bc
- [plotly] trace 0 scatter name='f'
- [plotly] trace 1 scatter name='df'
- [plotly] trace 2 scatter name='df = zero'
+ [plotly] figure md5:502229ab35
+ [plotly] trace 0 scatter name='f'
+ [plotly] trace 1 scatter name='df'
+ [plotly] trace 2 scatter name='df = zero'
```

**Why:** Same story: `f`, `df` and the three `df = zero` roots are byte-identical, and the cell is pure NumPy. Only plotly's int-to-float layout formatting differs.
**Reader sees:** equivalent.

<a id="c38"></a>
### C38 · `df = pl.from_pandas(sns.load_dataset("tips"))` · output

committed output

```diff
- [text]    total_bill   tip     sex smoker  day    time  size
- [text] 0       16.99  1.01  Female     No  Sun  Dinner     2
- [text] 1       10.34  1.66    Male     No  Sun  Dinner     3
- [text] 2       21.01  3.50    Male     No  Sun  Dinner     3
- [text] 3       23.68  3.31    Male     No  Sun  Dinner     2
- [text] 4       24.59  3.61  Female     No  Sun  Dinner     4
+ [text] shape: (5, 7)
+ [text] ┌────────────┬──────┬────────┬────────┬─────┬────────┬──────┐
+ [text] │ total_bill ┆ tip  ┆ sex    ┆ smoker ┆ day ┆ time   ┆ size │
+ [text] │ ---        ┆ ---  ┆ ---    ┆ ---    ┆ --- ┆ ---    ┆ ---  │
+ [text] │ f64        ┆ f64  ┆ cat    ┆ cat    ┆ cat ┆ cat    ┆ i64  │
+ [text] ╞════════════╪══════╪════════╪════════╪═════╪════════╪══════╡
+ [text] │ 16.99      ┆ 1.01 ┆ Female ┆ No     ┆ Sun ┆ Dinner ┆ 2    │
+ [text] │ 10.34      ┆ 1.66 ┆ Male   ┆ No     ┆ Sun ┆ Dinner ┆ 3    │
+ [text] │ 21.01      ┆ 3.5  ┆ Male   ┆ No     ┆ Sun ┆ Dinner ┆ 3    │
+ [text] │ 23.68      ┆ 3.31 ┆ Male   ┆ No     ┆ Sun ┆ Dinner ┆ 2    │
+ [text] │ 24.59      ┆ 3.61 ┆ Female ┆ No     ┆ Sun ┆ Dinner ┆ 4    │
+ [text] └────────────┴──────┴────────┴────────┴─────┴────────┴──────┘
```

**Why:** `pl.from_pandas(sns.load_dataset("tips"))`.
**Reader sees:** equivalent — the same five rows. The dtype row now shows `cat` for the four categorical columns, which pandas' `head()` did not display.

<a id="c39"></a>
### C39 · `def gradient_descent(df, initial_guess, alpha, n):` · output

committed output

```diff
- [stdout] Final guess for theta_1: 0.14369554654231262
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 28068 bytes md5:685364515e
+ [stdout] Final guess for theta_1: 0.14369554654231262
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 27744 bytes md5:96fc25b98d
```

**Why:** Re-rendered figure. The stdout line above it — the final guess `0.14369554654231262`, which the cell's `fig-alt` quotes — is byte-identical, so the curve is the same; the PNG differs only as a re-render (28068 → 27744 bytes).
**Reader sees:** equivalent — same plot, same quoted number. Pixel comparison not re-run in this pass; CONVERSIONS.md records a reviewer doing it.

