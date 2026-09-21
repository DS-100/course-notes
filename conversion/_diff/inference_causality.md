# inference_causality — change report

`887a578b0a4b:content/inference_causality/inference_causality.ipynb` → `content/inference_causality/inference_causality.ipynb`

**Tier B · 48 changes:** output 15 · prose 7 · dropdown 3 · tab-twins 7 · code 13 · metadata 3

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

The one chapter in this batch where the numbers genuinely moved. Seeding crosses libraries here:
`np.random.seed(...)` becomes `pl.set_random_seed(...)` and `.sample(frac=1, replace=True)` becomes
`.sample(fraction=1, with_replacement=True)`, and Polars' sampler runs its own RNG stream, so every
bootstrap figure in the chapter is a different valid draw. Six committed values moved with it
(C34, C35, C36, C39, C40, C45), plus three plotly figures this report does not list; all of it is
Monte-Carlo noise over 10,000 reps, none crosses a threshold the prose reasons about, and the one number the prose
quotes — the $	heta_1$ interval — was regenerated with it ($[-0.259, 1.103]$ -> $[-0.265, 1.124]$,
verified in the tree).

Three things for staff. **(1)** This chapter holds the batch's only surviving `.to_pandas()`, at C28:
`sns.pairplot` type-checks its `data` argument and rejects a Polars frame outright, which the
allowlist records; every other seaborn call in these five chapters takes Polars directly, and there
is no `.to_numpy()` anywhere in the chapter. **(2)** Four REVIEW items (C12-C15) rewrite code that
sits inside an HTML comment — the skipped PurpleAir section — so it is never rendered and never
executed. The conversion is right to do it (it would otherwise be pandas shipping inside a Polars
book) but it is **unverified**, and one of the rewrites is arguably better than the original: the
pandas version reassigned `full_df.columns` positionally where the Polars version renames by name.
**(3)** Three plotly figures re-rendered off the new RNG stream and this report does not list them,
because the output diff only tracks text, stdout and PNG: cells `b241cb77` (the sample scatter with
its OLS trendline), `1c2f637d` (the bootstrap histogram) and `820d5c88` (bootstrap vs population).

Separately, five pre-existing false claims were fixed (CONTRADICTIONS A5): two "20 cars" sentences
against a `sample_size` of 100, the bootstrap-versus-population comparison, and two MSEs printed
under an RMSE label.

## Needs review

- [C1](#c1) · cell 2: Example: Bootstrapping a Regression Coefficient
- [C4](#c4) · cell 9 [markdown]
- [C11](#c11) · cell 20 [markdown]
- [C12](#c12) · cell 20: Inverse Model Derivation
- [C13](#c13) · cell 20: big font helper
- [C14](#c14) · cell 20: big font helper
- [C15](#c15) · cell 20: big font helper

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C34](#c34) · `import numpy as np`
- [C35](#c35) · `model = lm.LinearRegression().fit(mpg_sample[['weight']], mpg_sample['`
- [C36](#c36) · `bs_thetas = bootstrap(mpg_sample, estimator, 10000)`
- [C37](#c37) · `def bootstrap_ci(bootstrap_samples, confidence_level=95):`
- [C38](#c38) · `mpg_pop = pl.from_pandas(sns.load_dataset('mpg'))`
- [C39](#c39) · `thetas = pl.DataFrame({"bs_thetas": bs_thetas, "thetas": theta_est})`
- [C40](#c40) · `import polars as pl`
- [C41](#c41) · `from sklearn.linear_model import LinearRegression`
- [C42](#c42) · `import numpy as np`
- [C43](#c43) · `pl.set_random_seed(1337)`
- [C44](#c44) · `import seaborn as sns`
- [C45](#c45) · `from sklearn.linear_model import LinearRegression`
- [C46](#c46) · `import matplotlib.pyplot as plt`
- [C47](#c47) · `from sklearn.metrics import mean_squared_error`
- [C48](#c48) · `lower_int = np.percentile(estimates_int, 2.5)`

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C2](#c2) · cell 2: Example: Bootstrapping a Regression Coefficient
- [C6](#c6) · cell 15: Comparing to the Population CIs
- [C9](#c9) · cell 18 [markdown]

## Changes

<a id="c1"></a>
### C1 · cell 2: Example: Bootstrapping a Regression Coefficient · prose · **REVIEW**

baseline L93 → branch L93

```diff
- # Suppose we collected a sample of 20 cars from a population. For the purposes of this demo, we will assume that the `seaborn`'s `mpg` dataset represents the entire population. The following is a visualization of our sample:
+ # Suppose we collected a sample of 100 cars from a population. For the purposes of this demo, we will assume that the `seaborn`'s `mpg` dataset represents the entire population. The following is a visualization of our sample:
```

**Why:** `sample_size` is `100` at all four assignment sites and the cell's own committed output prints `Sample Size: 100` two lines below the sentence. The only `20` in the chapter is `mpg_pop.sample(20)`, which draws fresh samples from the population and is not the sample being bootstrapped. CONTRADICTIONS A5 #1; pre-existing, unrelated to Polars.
**Verdict:** necessary — a fix to a false claim

<a id="c2"></a>
### C2 · cell 2: Example: Bootstrapping a Regression Coefficient · dropdown

baseline L96 → branch L96 · spans code and prose; mirror of the next code cell (hard rule 3)

```diff
+ # ```python
+ # import numpy as np
+ # import polars as pl
+ # import plotly.express as px
+ # import sklearn.linear_model as lm
+ # import seaborn as sns
+ #
+ # pl.set_random_seed(42)
+ # sample_size = 100
+ # mpg = pl.from_pandas(sns.load_dataset('mpg'))
+ # print("Full Data Size:", len(mpg))
+ # mpg_sample = mpg.sample(sample_size)
+ # print("Sample Size:", len(mpg_sample))
+ # px.scatter(mpg_sample, x='weight', y='mpg', trendline='ols', width=800)
+ # ```
+ # ````
+ 
+ # %% tags=["remove-input"]
+ import numpy as np
+ import polars as pl
+ import plotly.express as px
+ import sklearn.linear_model as lm
+ import seaborn as sns
+ 
+ pl.set_random_seed(42)
+ sample_size = 100
+ mpg = pl.from_pandas(sns.load_dataset('mpg'))
+ print("Full Data Size:", len(mpg))
+ mpg_sample = mpg.sample(sample_size)
+ print("Sample Size:", len(mpg_sample))
+ px.scatter(mpg_sample, x='weight', y='mpg', trendline='ols', width=800)
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin b241cb77 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # import numpy as np
+ # import polars as pl
+ … 21 more lines
```

**Why:** The setup cell was converted: `pl.from_pandas(sns.load_dataset('mpg'))` because `load_dataset` returns a *pandas* frame, `pl.set_random_seed(42)` in place of `np.random.seed(42)` because Polars' `.sample()` does not ride the NumPy stream, and `px.scatter` takes the Polars frame directly. The surrounding block is the tab-twin. Mirror matches the code cell below it (checked mechanically; all five dropdowns in this chapter match).
**Output:** differs: the sample of 100 cars is a different draw, so the scatter and its OLS trendline move. The printed `Full Data Size: 398 / Sample Size: 100` is unchanged

<a id="c3"></a>
### C3 · cell 4 [markdown] · tab-twins

baseline L111 → branch L172 · spans code and prose

```diff
- # ````
- 
- # %% tags=["remove-input"]
- import numpy as np
- import pandas as pd
- import plotly.express as px
- import sklearn.linear_model as lm
- import seaborn as sns
- 
- np.random.seed(42)
- sample_size = 100
- mpg = sns.load_dataset('mpg')
- print("Full Data Size:", len(mpg))
- mpg_sample = mpg.sample(sample_size)
- print("Sample Size:", len(mpg_sample))
- px.scatter(mpg_sample, x='weight', y='mpg', trendline='ols', width=800)
+ #
+ # ```text
+ # Full Data Size: 398
+ # Sample Size: 100
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** Same twin as C2 — the removed lines are the baseline code cell, now inside the pandas tab, and the added lines are its committed output as a `text` block.
**Output:** same — it is the baseline's output, republished. Both panes print `Full Data Size: 398`, `Sample Size: 100`

<a id="c4"></a>
### C4 · cell 9 [markdown] · prose · **REVIEW**

baseline L151 → branch L204

```diff
- # The code below uses `df.sample` [(documentation)](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sample.html) to generate a bootstrap sample that is the same size as the original sample.
+ # The code below uses `df.sample` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.sample.html) to generate a bootstrap sample that is the same size as the original sample.
```

**Why:** The prose links to `pandas.DataFrame.sample` documentation for a call that is now `polars.DataFrame.sample`. Leaving it would point a student at the wrong signature — the keywords differ (`frac`/`fraction`, `replace`/`with_replacement`, `random_state`/`seed`), which is exactly what C5 changes in the cell below.
**Verdict:** necessary — a pandas-specific link that could not survive

<a id="c5"></a>
### C5 · cell 10 [code] · code

baseline L163 → branch L216

```diff
-         bootstrap_sample = sample.sample(frac=1, replace=True)
+         bootstrap_sample = sample.sample(fraction=1, with_replacement=True)
```

**Why:** Polars' `sample` renames two keywords: `frac=` -> `fraction=` and `replace=` -> `with_replacement=`. This is also the point where the RNG stream changes hands — Polars' sampler does not read NumPy's seed, which is why C22/C25/C31 switch to `pl.set_random_seed`.
**Output:** differs: every bootstrap statistic downstream is a different valid draw. See C34, C35, C39, C40, C45

<a id="c6"></a>
### C6 · cell 15: Comparing to the Population CIs · dropdown

baseline L229 → branch L282 · mirror of the next code cell (hard rule 3)

```diff
- # mpg_pop = sns.load_dataset('mpg')
+ # mpg_pop = pl.from_pandas(sns.load_dataset('mpg'))
```

**Why:** `sns.load_dataset` returns a **pandas** frame, so it is a pandas site no `pd.`/`import pandas` scan would find; `pl.from_pandas(...)` wraps it. Mirror matches its code cell.
**Output:** same

<a id="c7"></a>
### C7 · cell 16 [code] · code

baseline L235 → branch L288

```diff
- # %% tags=["remove-input"]
- mpg_pop = sns.load_dataset('mpg')
+ # %% tags=["remove-input", "remove-output"]
+ mpg_pop = pl.from_pandas(sns.load_dataset('mpg'))
```

**Why:** Same `pl.from_pandas` wrap as C6, plus `remove-output` added because the tab-twin below now publishes this cell's output in both panes. The cell's Polars source and output are published beside the baseline pandas pair as a tab-twin. The cell itself gained `remove-output` so the same block does not render twice — checked that every `remove-output` cell in this chapter has a matching `tab-twins` id, so none of them is a silenced cell.
**Output:** differs: the printed CI moved from `[-0.01019291 -0.00573015]` to `[-0.01014361 -0.00571021]` — 10,000 draws of 20 from the same population on a different RNG stream. See C36

<a id="c8"></a>
### C8 · cell 16 [code] · tab-twins

baseline L239 → branch L292 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 68454791 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # mpg_pop = pl.from_pandas(sns.load_dataset('mpg'))
+ # theta_est = [estimator(mpg_pop.sample(20)) for i in range(10000)]
+ # print(bootstrap_ci(theta_est))
+ # ```
+ #
+ # ```text
+ # [-0.01014361 -0.00571021]
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # mpg_pop = sns.load_dataset('mpg')
+ # theta_est = [estimator(mpg_pop.sample(20)) for i in range(10000)]
+ # print(bootstrap_ci(theta_est))
+ # ```
+ #
+ # ```text
+ # [-0.01019291 -0.00573015]
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** The tab-twin for the population-CI cell. Worth a look: the two panes run the *same* computation, and the only real difference between them is which RNG produced the 10,000 draws. The gap (`[-0.01014, -0.00571]` vs `[-0.01019, -0.00573]`) is Monte-Carlo noise, not a library behaviour a reader should generalise from — the same category CONTRADICTIONS B1 flagged for `pca`'s null-space vectors.
**Output:** differs: fourth-decimal disagreement between the panes, from the RNG stream and nothing else

<a id="c9"></a>
### C9 · cell 18 [markdown] · dropdown

baseline L245 → branch L329 · mirror of the next code cell (hard rule 3)

```diff
- # thetas = pd.DataFrame({"bs_thetas": bs_thetas, "thetas": theta_est})
- # px.histogram(thetas.melt(), x='value', facet_row='variable',
+ # thetas = pl.DataFrame({"bs_thetas": bs_thetas, "thetas": theta_est})
+ # px.histogram(thetas.unpivot(), x='value', facet_row='variable',
```

**Why:** `pd.DataFrame({...})` -> `pl.DataFrame({...})`, and `melt()` -> `unpivot()` — renamed in Polars, with the same long-form `variable`/`value` output that `px.histogram(..., x='value', facet_row='variable')` reads. Mirror matches its code cell.
**Output:** same

<a id="c10"></a>
### C10 · cell 19 [code] · code

baseline L252 → branch L336

```diff
- thetas = pd.DataFrame({"bs_thetas": bs_thetas, "thetas": theta_est})
- px.histogram(thetas.melt(), x='value', facet_row='variable',
+ thetas = pl.DataFrame({"bs_thetas": bs_thetas, "thetas": theta_est})
+ px.histogram(thetas.unpivot(), x='value', facet_row='variable',
```

**Why:** Same rewrite as C9, in the code cell. `px.histogram` takes the Polars frame directly.
**Output:** differs: the `bs_thetas` facet is drawn from the new bootstrap stream. This is one of the three plotly outputs the report does not list — see the Summary

<a id="c11"></a>
### C11 · cell 20 [markdown] · prose · **REVIEW**

baseline L257 → branch L341

```diff
- # Although our bootstrapped sample distribution does not exactly match the sampling distribution of the population, we can see that it is relatively close. This demonstrates the benefit of bootstrapping — without knowing the actual population distribution, we can still roughly approximate the true slope for the model by using only a single random sample of 20 cars.
+ # Although our bootstrapped sample distribution does not exactly match the sampling distribution of the population, we can see that it is relatively close. Read the two carefully, though: the bootstrap resamples 100 cars, because that is the size of the sample we drew, while the population curve beside it is built from repeated draws of 20. Resample size has to match the original sample — that is the rule stated two sections above — so the narrower bootstrap spread is a consequence of the larger $n$, not evidence that bootstrapping understates the variability. This demonstrates the benefit of bootstrapping — without knowing the actual population distribution, we can still roughly approximate the true slope for the model by using only a single random sample of 100 cars.
```

**Why:** Two problems in one paragraph. The "20 cars" is the same error as C1 (`sample_size` is 100). And the "relatively close" comparison is between distributions built at different $n$: the bootstrap resamples 100, while the population curve beside it draws 20, so the bootstrap is about 2.4x narrower and is close to the *n=100* population curve, not the one plotted. The chapter states the rule it breaks two sections earlier ("New samples must be the same size as the original sample"). CONTRADICTIONS A5 #2 and #3; pre-existing. The replacement keeps the conclusion and names the $n$ mismatch instead of hiding it.
**Verdict:** necessary — a fix to a false claim. The explanatory clause is long for a fix; a shorter version naming the two sample sizes would also do, but the sentence has to say something, since the figure it describes is still drawn at two different $n$

<a id="c12"></a>
### C12 · cell 20: Inverse Model Derivation · prose · **REVIEW**

baseline L290 → branch L374

```diff
- # import pandas as pd
+ # import polars as pl
```

**Why:** Import rename inside the chapter's skipped **PurpleAir** section, which is wrapped in an HTML comment — it never renders on the page and is never executed. Converting it is still right: an uncommented pandas block sitting in a Polars chapter is a defect waiting for whoever restores the section.
**Verdict:** necessary — pandas-specific content. **Unverified**: the code is inside `<!-- -->` and was never run

<a id="c13"></a>
### C13 · cell 20: big font helper · prose · **REVIEW**

baseline L321 → branch L405

```diff
- # full_df = (pd.read_csv(csv_file, usecols=usecols, parse_dates=['Date'])
- #         .dropna())
- # full_df.columns = ['date', 'id', 'region', 'pm25aqs', 'pm25pa', 'temp', 'rh', 'dew']
- # full_df = full_df.loc[(full_df['pm25aqs'] < 50)]
+ # new_names = ['date', 'id', 'region', 'pm25aqs', 'pm25pa', 'temp', 'rh', 'dew']
+ # full_df = (pl.read_csv(csv_file, columns=usecols, null_values='NA', try_parse_dates=True)
+ #         .drop_nulls()
+ #         .rename(dict(zip(usecols, new_names))))
+ # full_df = full_df.filter(pl.col('pm25aqs') < 50)
```

**Why:** Same commented-out PurpleAir block. `pd.read_csv(usecols=, parse_dates=['Date'])` becomes `pl.read_csv(columns=, try_parse_dates=True)`, `null_values='NA'` is added because Polars has no default NA-token set and would raise on an `NA` in a numeric column, `.dropna()` -> `.drop_nulls()`, and the positional `full_df.columns = [...]` assignment becomes a `rename` mapping built from `zip(usecols, new_names)`. Note the rename is **by name**, where the pandas original assigned **by position** — so it is correct even if `columns=` returns the columns in file order rather than `usecols` order, which the pandas version silently depended on.
**Verdict:** necessary — none of `usecols`, `parse_dates`, positional column assignment or `dropna` exists in Polars. **Unverified**: inside an HTML comment, never executed

<a id="c14"></a>
### C14 · cell 20: big font helper · prose · **REVIEW**

baseline L327 → branch L412

```diff
- # bad_dates = ['2019-08-21', '2019-08-22', '2019-09-24']
- # GA = full_df.loc[(full_df['id'] == 'GA1') & (~full_df['date'].isin(bad_dates)) , :]
+ # bad_dates = pl.Series(['2019-08-21', '2019-08-22', '2019-09-24']).str.to_date()
+ # GA = full_df.filter((pl.col('id') == 'GA1') & ~pl.col('date').is_in(bad_dates))
```

**Why:** Same commented-out block. `.loc[mask, :]` -> `.filter(...)`, `isin` -> `is_in`. The `bad_dates` list had to become a parsed `pl.Series` of dates: `try_parse_dates=True` types `date` as a Date column, and `is_in` over a list of strings against a Date column would not match.
**Verdict:** necessary — `.loc` has no Polars analogue and the dtype comparison forces the parse. **Unverified**: inside an HTML comment, never executed

<a id="c15"></a>
### C15 · cell 20: big font helper · prose · **REVIEW**

baseline L331 → branch L416

```diff
- # pd.DataFrame(PA).head()
+ # PA.to_frame().head()
```

**Why:** Same commented-out block. `pd.DataFrame(PA)` wrapped a Series into a one-column frame; `PA.to_frame()` is the Polars spelling.
**Verdict:** necessary — pandas constructor form. **Unverified**: inside an HTML comment, never executed

<a id="c16"></a>
### C16 · cell 21 [code] · code

baseline L529 → branch L614

```diff
- # %%
- import pandas as pd
- eggs = pd.read_csv("data/snowy_plover.csv")
+ # %% tags=["remove-input", "remove-output"]
+ import polars as pl
+ eggs = pl.read_csv("data/snowy_plover.csv")
```

**Why:** `pd.read_csv` -> `pl.read_csv` on `snowy_plover.csv`, plus `remove-input, remove-output` because the tab-twin at C17 now publishes this cell in both panes. The cell's Polars source and output are published beside the baseline pandas pair as a tab-twin. The cell itself gained `remove-output` so the same block does not render twice — checked that every `remove-output` cell in this chapter has a matching `tab-twins` id, so none of them is a silenced cell.
**Output:** differs: the same five rows print as Polars' table repr instead of pandas'. See C37

<a id="c17"></a>
### C17 · cell 21 [code] · tab-twins

baseline L533 → branch L618 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin b6d91c04 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # import polars as pl
+ # eggs = pl.read_csv("data/snowy_plover.csv")
+ # eggs.head(5)
+ # ```
+ #
+ # ```text
+ # shape: (5, 4)
+ # ┌────────────┬────────────┬─────────────┬─────────────┐
+ # │ egg_weight ┆ egg_length ┆ egg_breadth ┆ bird_weight │
+ # │ ---        ┆ ---        ┆ ---         ┆ ---         │
+ # │ f64        ┆ f64        ┆ f64         ┆ f64         │
+ # ╞════════════╪════════════╪═════════════╪═════════════╡
+ # │ 7.4        ┆ 28.8       ┆ 21.84       ┆ 5.2         │
+ # │ 7.7        ┆ 29.04      ┆ 22.45       ┆ 5.4         │
+ # │ 7.9        ┆ 29.36      ┆ 22.48       ┆ 5.6         │
+ # │ 7.5        ┆ 30.1       ┆ 21.71       ┆ 5.3         │
+ # │ 8.3        ┆ 30.17      ┆ 22.75       ┆ 5.9         │
+ # └────────────┴────────────┴─────────────┴─────────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # import pandas as pd
+ # eggs = pd.read_csv("data/snowy_plover.csv")
+ # eggs.head(5)
+ # ```
+ #
+ # ```text
+ #    egg_weight  egg_length  egg_breadth  bird_weight
+ # 0         7.4       28.80        21.84          5.2
+ # 1         7.7       29.04        22.45          5.4
+ … 7 more lines
```

**Why:** The tab-twin for the `snowy_plover` head. Both panes read the same file; only the repr differs.
**Output:** differs: `shape: (5, 4)` plus a dtype-annotated table on the Polars side, an indexed block on the pandas side. Values identical

<a id="c18"></a>
### C18 · cell 24 [code] · metadata

baseline L550 → branch L682

```diff
- # %%
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c19"></a>
### C19 · cell 24 [code] · code

baseline L564 → branch L696

```diff
- display(pd.DataFrame(
-   [model.intercept_] + list(model.coef_),
-   columns=['theta_hat'],
-   index=['intercept', 'egg_weight', 'egg_length', 'egg_breadth']
- ))
+ display(pl.DataFrame({
+   "parameter": ['intercept', 'egg_weight', 'egg_length', 'egg_breadth'],
+   "theta_hat": [model.intercept_] + list(model.coef_),
+ }))
```

**Why:** `pd.DataFrame(data, columns=['theta_hat'], index=[...])` used the index to carry the parameter names, and Polars has no index — so the names become an ordinary `parameter` column. The Polars name is kept rather than reconstructed (output-equivalence policy); nothing downstream reads this frame.
**Output:** same

<a id="c20"></a>
### C20 · cell 24 [code] · tab-twins

baseline L570 → branch L701 · spans code and prose

```diff
- print("RMSE", np.mean((Y - model.predict(X)) ** 2))
+ print("MSE", ((Y - model.predict(X)) ** 2).mean())
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin add45dc7 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # from sklearn.linear_model import LinearRegression
+ # import numpy as np
+ #
+ # X = eggs[["egg_weight", "egg_length", "egg_breadth"]]
+ # Y = eggs["bird_weight"]
+ #
+ # model = LinearRegression()
+ # model.fit(X, Y)
+ #
+ # # This gives an array containing the fitted model parameter estimates
+ # thetas = model.coef_
+ #
+ # # Put the parameter estimates in a nice table for viewing
+ # display(pl.DataFrame({
+ #   "parameter": ['intercept', 'egg_weight', 'egg_length', 'egg_breadth'],
+ #   "theta_hat": [model.intercept_] + list(model.coef_),
+ # }))
+ #
+ # print("MSE", ((Y - model.predict(X)) ** 2).mean())
+ # ```
+ #
+ # ```text
+ # shape: (4, 2)
+ # ┌─────────────┬───────────┐
+ # │ parameter   ┆ theta_hat │
+ # │ ---         ┆ ---       │
+ # │ str         ┆ f64       │
+ # ╞═════════════╪═══════════╡
+ # │ intercept   ┆ -4.60567  │
+ # │ egg_weight  ┆ 0.431229  │
+ # │ egg_length  ┆ 0.06657   │
+ # │ egg_breadth ┆ 0.215914  │
+ … 41 more lines
```

**Why:** Two things. `np.mean((Y - model.predict(X)) ** 2)` becomes `((...) ** 2).mean()`, because `model.predict(X)` returns an ndarray and `Y` is a Polars Series, so the subtraction yields a Series and `np.mean` on it raises — the method form survives every combination. And the label was wrong: the expression is the MSE, printed as 0.0455, where the RMSE is 0.2132 (CONTRADICTIONS A5 #4, pre-existing). The tab-twin below republishes both panes; CONTRADICTIONS B1b records that the *first* attempt at this twin kept the wrong `RMSE` label on the pandas pane.
**Output:** differs: the stdout line now reads `MSE 0.04547085380275759` instead of `RMSE 0.04547085380275775`. The label is corrected and the value moved in its 15th significant digit from the reordered reduction. See C38

<a id="c21"></a>
### C21 · cell 27 [code] · metadata

baseline L580 → branch L791

```diff
- # %%
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c22"></a>
### C22 · cell 27 [code] · code

baseline L584 → branch L795

```diff
- np.random.seed(1337)
+ pl.set_random_seed(1337)
```

**Why:** `np.random.seed(1337)` -> `pl.set_random_seed(1337)`. The seed governs `eggs.sample(...)` two lines down, and Polars' sampler does not read NumPy's stream, so seeding NumPy here would have left the bootstrap unseeded and non-reproducible. `np.percentile` further down still uses NumPy, but it is deterministic.
**Output:** differs: a different but equally valid bootstrap stream. See C39

<a id="c23"></a>
### C23 · cell 27 [code] · code

baseline L596 → branch L807

```diff
-     bootstrap_resample = eggs.sample(n, replace=True)
+     bootstrap_resample = eggs.sample(n, with_replacement=True)
```

**Why:** `replace=True` -> `with_replacement=True`; Polars' keyword name.
**Output:** differs: see C39 — the resulting CI moved from (-0.2586, 1.1034) to (-0.2651, 1.1240)

<a id="c24"></a>
### C24 · cell 28 [markdown] · tab-twins

baseline L615 → branch L826

```diff
- # Our bootstrapped 95% confidence interval for $\theta_1$ is $[-0.259, 1.103]$. Immediately, we can see that 0 *is* indeed contained in this interval – this means that we *cannot* conclude that $\theta_1$ is non-zero! More formally, we fail to reject the null hypothesis (that $\theta_1$ is 0) at a 5% cutoff.
+ # <!-- tab-twins:begin fec55157 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Set a random seed so you generate the same random sample as staff
+ # # In the "real world", we wouldn't do this
+ # import numpy as np
+ # pl.set_random_seed(1337)
+ #
+ # # Set the sample size of each bootstrap sample
+ # n = len(eggs)
+ #
+ # # Create a list to store all the bootstrapped estimates
+ # estimates = []
+ #
+ # # Generate a bootstrap resample from `eggs` and find an estimate for theta_1 using this sample.
+ # # Repeat 10000 times.
+ # for i in range(10000):
+ #     # draw a bootstrap sample
+ #     bootstrap_resample = eggs.sample(n, with_replacement=True)
+ #     X_bootstrap = bootstrap_resample[["egg_weight", "egg_length", "egg_breadth"]]
+ #     Y_bootstrap = bootstrap_resample["bird_weight"]
+ #
+ #     # use bootstrapped sample to fit a model
+ #     bootstrap_model = LinearRegression()
+ #     bootstrap_model.fit(X_bootstrap, Y_bootstrap)
+ #     bootstrap_thetas = bootstrap_model.coef_
+ #
+ #     # record the result for theta_1
+ #     estimates.append(bootstrap_thetas[0])
+ #
+ # # calculate the 95% confidence interval
+ # lower = np.percentile(estimates, 2.5, axis=0)
+ # upper = np.percentile(estimates, 97.5, axis=0)
+ # conf_interval = (lower, upper)
+ # conf_interval
+ # ```
+ #
+ # ```text
+ … 50 more lines
```

**Why:** The prose sentence quoting the interval was replaced in the diff by the tab-twin block that now precedes it. The sentence itself survives one cell later and **was** regenerated: it reads $[-0.265, 1.124]$ in the tree, matching the new committed output. Confirmed by reading the branch notebook.
**Output:** differs: the twin's two panes show CIs from two RNG streams. The conclusion the paragraph draws — that 0 lies inside the interval, so we fail to reject — holds on both, with room to spare

<a id="c25"></a>
### C25 · cell 30 [code] · code

baseline L619 → branch L919

```diff
- # %%
- np.random.seed(1337)
+ # %% tags=["remove-input", "remove-output"]
+ pl.set_random_seed(1337)
```

**Why:** Same `pl.set_random_seed` swap as C22, plus `remove-input, remove-output` for the tab-twin at C27. The cell's Polars source and output are published beside the baseline pandas pair as a tab-twin. The cell itself gained `remove-output` so the same block does not render twice — checked that every `remove-output` cell in this chapter has a matching `tab-twins` id, so none of them is a silenced cell.
**Output:** differs: new bootstrap stream. See C40

<a id="c26"></a>
### C26 · cell 30 [code] · code

baseline L629 → branch L929

```diff
-     bootstrap_resample = eggs.sample(n, replace=True)
+     bootstrap_resample = eggs.sample(n, with_replacement=True)
```

**Why:** Same `with_replacement=` rename as C23.
**Output:** differs: see C40

<a id="c27"></a>
### C27 · cell 30 [code] · tab-twins

baseline L649 → branch L949 · spans code and prose

```diff
- pd.DataFrame({"lower":[theta_0_lower, theta_1_lower, theta_2_lower, theta_3_lower], "upper":[theta_0_upper, \
-                 theta_1_upper, theta_2_upper, theta_3_upper]}, index=["theta_0", "theta_1", "theta_2", "theta_3"])
+ pl.DataFrame({"parameter":["theta_0", "theta_1", "theta_2", "theta_3"],
+               "lower":[theta_0_lower, theta_1_lower, theta_2_lower, theta_3_lower],
+               "upper":[theta_0_upper, theta_1_upper, theta_2_upper, theta_3_upper]})
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 2fda0b71 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # pl.set_random_seed(1337)
+ #
+ # theta_0_estimates = []
+ # theta_1_estimates = []
+ # theta_2_estimates = []
+ # theta_3_estimates = []
+ #
+ #
+ # for i in range(10000):
+ #     bootstrap_resample = eggs.sample(n, with_replacement=True)
+ #     X_bootstrap = bootstrap_resample[["egg_weight", "egg_length", "egg_breadth"]]
+ #     Y_bootstrap = bootstrap_resample["bird_weight"]
+ #
+ #     bootstrap_model = LinearRegression()
+ #     bootstrap_model.fit(X_bootstrap, Y_bootstrap)
+ #     bootstrap_theta_0 = bootstrap_model.intercept_
+ #     bootstrap_theta_1, bootstrap_theta_2, bootstrap_theta_3 = bootstrap_model.coef_
+ #
+ #     theta_0_estimates.append(bootstrap_theta_0)
+ #     theta_1_estimates.append(bootstrap_theta_1)
+ #     theta_2_estimates.append(bootstrap_theta_2)
+ #     theta_3_estimates.append(bootstrap_theta_3)
+ #
+ # theta_0_lower, theta_0_upper = np.percentile(theta_0_estimates, 2.5), np.percentile(theta_0_estimates, 97.5)
+ # theta_1_lower, theta_1_upper = np.percentile(theta_1_estimates, 2.5), np.percentile(theta_1_estimates, 97.5)
+ # theta_2_lower, theta_2_upper = np.percentile(theta_2_estimates, 2.5), np.percentile(theta_2_estimates, 97.5)
+ # theta_3_lower, theta_3_upper = np.percentile(theta_3_estimates, 2.5), np.percentile(theta_3_estimates, 97.5)
+ #
+ # # Make a nice table to view results
+ # pl.DataFrame({"parameter":["theta_0", "theta_1", "theta_2", "theta_3"],
+ … 65 more lines
```

**Why:** `pd.DataFrame({...}, index=[...])` -> `pl.DataFrame` with the parameter names as an ordinary `parameter` column, since Polars has no index. Published as a tab-twin.
**Output:** differs: the Polars pane prints a four-row table with a `parameter` column and the new bootstrap bounds; the pandas pane keeps the baseline's indexed frame and its bounds. All four intervals still contain 0, which is the point the next paragraph makes

<a id="c28"></a>
### C28 · cell 33 [code] · code

baseline L662 → branch L1065

```diff
- sns.pairplot(eggs[["egg_length", "egg_breadth", "egg_weight", 'bird_weight']]);
+ sns.pairplot(eggs[["egg_length", "egg_breadth", "egg_weight", 'bird_weight']].to_pandas());
```

**Why:** The batch's only surviving `.to_pandas()`, and it is allowlisted (`inference_causality: interop`, cell `fcd8d006`). `sns.pairplot` type-checks its `data` argument and raises `TypeError: 'data' must be pandas DataFrame object` on a Polars frame — seaborn 0.13.2. It is the one seaborn entry point in these chapters that rejects Polars outright, and there is no cheaper rung: pairplot draws a grid over the whole frame, so there is no per-Series or `.to_numpy()` form of the call. Justified.
**Output:** same — the figure re-rendered (1.18% of pixels, anti-aliasing), but it is the same 4x4 grid over the same four columns

<a id="c29"></a>
### C29 · cell 35 [code] · metadata

baseline L681 → branch L1084

```diff
- # %%
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c30"></a>
### C30 · cell 35 [code] · tab-twins

baseline L694 → branch L1097 · spans code and prose

```diff
- pd.DataFrame({"theta_hat":[model_int.intercept_, thetas_int[0]]}, index=["theta_0", "theta_1"])
+ pl.DataFrame({"parameter":["theta_0", "theta_1"],
+               "theta_hat":[model_int.intercept_, thetas_int[0]]})
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin bcb9100f -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # from sklearn.linear_model import LinearRegression
+ # X_int = eggs[["egg_weight"]]
+ # Y_int = eggs["bird_weight"]
+ #
+ # model_int = LinearRegression()
+ #
+ # model_int.fit(X_int, Y_int)
+ #
+ # # This gives an array containing the fitted model parameter estimates
+ # thetas_int = model_int.coef_
+ #
+ # # Put the parameter estimates in a nice table for viewing
+ # pl.DataFrame({"parameter":["theta_0", "theta_1"],
+ #               "theta_hat":[model_int.intercept_, thetas_int[0]]})
+ # ```
+ #
+ # ```text
+ # shape: (2, 2)
+ # ┌───────────┬───────────┐
+ # │ parameter ┆ theta_hat │
+ # │ ---       ┆ ---       │
+ # │ str       ┆ f64       │
+ # ╞═══════════╪═══════════╡
+ # │ theta_0   ┆ -0.058272 │
+ # │ theta_1   ┆ 0.718515  │
+ # └───────────┴───────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ … 24 more lines
```

**Why:** `pd.DataFrame({...}, index=["theta_0", "theta_1"])` -> `pl.DataFrame` with a `parameter` column; same index-has-no-analogue rewrite as C19 and C27. Published as a tab-twin.
**Output:** differs: shape and column names differ between the panes (a `parameter` column versus an index). The two `theta_hat` values are identical to six decimals on both sides — this fit is deterministic, unlike the bootstraps

<a id="c31"></a>
### C31 · cell 37 [code] · code

baseline L702 → branch L1168

```diff
- np.random.seed(1337)
+ pl.set_random_seed(1337)
```

**Why:** Same `pl.set_random_seed` swap as C22, for the interpretable-model bootstrap.
**Output:** differs: see C45

<a id="c32"></a>
### C32 · cell 37 [code] · code

baseline L713 → branch L1179

```diff
-     bootstrap_resample_int = eggs.sample(n, replace=True)
+     bootstrap_resample_int = eggs.sample(n, with_replacement=True)
```

**Why:** Same `with_replacement=` rename as C23.
**Output:** differs: see C45

<a id="c33"></a>
### C33 · cell 39 [code] · code

baseline L734 → branch L1200

```diff
- rmse = mean_squared_error(Y, model.predict(X))
- rmse_int = mean_squared_error(Y_int, model_int.predict(X_int))
- print(f'RMSE of Original Model: {rmse}')
- print(f'RMSE of Interpretable Model: {rmse_int}')
+ mse = mean_squared_error(Y, model.predict(X))
+ mse_int = mean_squared_error(Y_int, model_int.predict(X_int))
+ print(f'MSE of Original Model: {mse}')
+ print(f'MSE of Interpretable Model: {mse_int}')
```

**Why:** The variables were named `rmse` and printed under an `RMSE` label, but the pinned sklearn's `mean_squared_error` signature is `(y_true, y_pred, *, sample_weight, multioutput)` — there is no `squared=` parameter, so it returns the MSE unconditionally. Renaming the variables and the labels is the minimal honest fix. CONTRADICTIONS A5 #5; pre-existing, and identical in both libraries.
**Output:** differs: both printed lines now say `MSE`. The original model's value also moved in its 15th significant digit. See C44

<a id="c34"></a>
### C34 · `import numpy as np` · output

committed output

```diff
- [stdout] Full Data Size: 398
- [stdout] Sample Size: 100
- [plotly] figure md5:646665ccbf
- [plotly] trace 0 scatter
- [plotly] trace 1 scatter
+ [stdout] Full Data Size: 398
+ [stdout] Sample Size: 100
+ [plotly] figure md5:1b85efca83
+ [plotly] trace 0 scatter
+ [plotly] trace 1 scatter
```

**Why:** The mpg-against-weight scatter of the 100-car sample, redrawn. The cell's two printed sizes are unchanged (398 full, 100 sampled) and both scatter traces survive, but `pl.set_random_seed(42)` with Polars' `.sample(100)` draws a different hundred cars than the NumPy-seeded pandas version did, so every plotted point moves and the figure digest changes with them.
**Reader sees:** equivalent: a scatter of one 100-car sample with its fitted line, showing the same negative mpg-weight relationship. It is a different hundred cars, which is the point the section goes on to make about sampling variability. No prose quotes a coordinate.

<a id="c35"></a>
### C35 · `model = lm.LinearRegression().fit(mpg_sample[['weight']], mpg_sample['` · output

committed output

```diff
- [text] -0.007305965155512159
+ [text] -0.007799062916110054
```

**Why:** Re-executed on the new RNG stream: `pl.set_random_seed(42)` plus Polars' `.sample(100)` draws a different 100 cars than NumPy-seeded pandas did, so the fitted slope differs.
**Reader sees:** equivalent: -0.00731 -> -0.00780, both small negative slopes of mpg on weight. No prose quotes the number (checked), and the section's point — that a single sample gives one estimate whose uncertainty we then bootstrap — is untouched

<a id="c36"></a>
### C36 · `bs_thetas = bootstrap(mpg_sample, estimator, 10000)` · output

committed output

```diff
- [plotly] figure md5:54bb78b346
- [plotly] trace 0 histogram name='0'
- [plotly] title='Bootstrap Distribution of the Slope'
+ [plotly] figure md5:18400369c5
+ [plotly] trace 0 histogram name='0'
+ [plotly] title='Bootstrap Distribution of the Slope'
```

**Why:** The 10,000 bootstrap slopes are drawn from the new 100-car sample (C35) on Polars' RNG stream, so the whole distribution moves with the sample slope: mean -0.00732 -> -0.00781, sd 0.00042 -> 0.00046, range [-0.00899, -0.00562] -> [-0.00967, -0.00617].
**Reader sees:** changed: the histogram sits about 0.0005 further left and is marginally wider. Same unimodal, roughly normal shape, still entirely below zero — the only property the surrounding prose reads off it.

<a id="c37"></a>
### C37 · `def bootstrap_ci(bootstrap_samples, confidence_level=95):` · output

committed output

```diff
- [stdout] [-0.00814752 -0.00653232]
+ [stdout] [-0.00875528 -0.00696179]
```

**Why:** The bootstrap CI for that slope, recomputed from the new sample on the new stream.
**Reader sees:** equivalent: `[-0.00815, -0.00653]` -> `[-0.00876, -0.00696]`. Same width to within 10%, same sign, still excludes 0. Nothing in the prose quotes it

<a id="c38"></a>
### C38 · `mpg_pop = pl.from_pandas(sns.load_dataset('mpg'))` · output

committed output

```diff
- [stdout] [-0.01019291 -0.00573015]
+ [stdout] [-0.01014361 -0.00571021]
```

**Why:** The population CI, 10,000 draws of 20 on Polars' RNG rather than NumPy's.
**Reader sees:** equivalent: `[-0.01019, -0.00573]` -> `[-0.01014, -0.00571]`, a fourth-decimal shift. This is the cell whose twin (C8) now shows both numbers side by side

<a id="c39"></a>
### C39 · `thetas = pl.DataFrame({"bs_thetas": bs_thetas, "thetas": theta_est})` · output

committed output

```diff
- [plotly] figure md5:301faa0eea
- [plotly] trace 0 histogram
- [plotly] trace 1 histogram
- [plotly] title='Distribution of the Slope'
+ [plotly] figure md5:91068e5d6a
+ [plotly] trace 0 histogram
+ [plotly] trace 1 histogram
+ [plotly] title='Distribution of the Slope'
```

**Why:** The top facet is C36's bootstrap distribution and shifts with it. The bottom facet is `theta_est`, 10,000 slopes refitted on fresh samples of the population, which is simply a different draw from the same distribution: mean -0.0077621 -> -0.0077615, sd 0.001127 -> 0.001111.
**Reader sees:** changed: only the bootstrap facet moves, about 0.0005 to the left; the population facet is visually the same. The comparison the figure exists to make — the bootstrap spread is narrower than the true sampling distribution — reads the same, and the two centres now line up slightly more closely than in the baseline.

<a id="c40"></a>
### C40 · `import polars as pl` · output

committed output

```diff
- [text]    egg_weight  egg_length  egg_breadth  bird_weight
- [text] 0         7.4       28.80        21.84          5.2
- [text] 1         7.7       29.04        22.45          5.4
- [text] 2         7.9       29.36        22.48          5.6
- [text] 3         7.5       30.10        21.71          5.3
- [text] 4         8.3       30.17        22.75          5.9
+ [text] shape: (5, 4)
+ [text] ┌────────────┬────────────┬─────────────┬─────────────┐
+ [text] │ egg_weight ┆ egg_length ┆ egg_breadth ┆ bird_weight │
+ [text] │ ---        ┆ ---        ┆ ---         ┆ ---         │
+ [text] │ f64        ┆ f64        ┆ f64         ┆ f64         │
+ [text] ╞════════════╪════════════╪═════════════╪═════════════╡
+ [text] │ 7.4        ┆ 28.8       ┆ 21.84       ┆ 5.2         │
+ [text] │ 7.7        ┆ 29.04      ┆ 22.45       ┆ 5.4         │
+ [text] │ 7.9        ┆ 29.36      ┆ 22.48       ┆ 5.6         │
+ [text] │ 7.5        ┆ 30.1       ┆ 21.71       ┆ 5.3         │
+ [text] │ 8.3        ┆ 30.17      ┆ 22.75       ┆ 5.9         │
+ [text] └────────────┴────────────┴─────────────┴─────────────┘
```

**Why:** Re-executed with `pl.read_csv`; `.head(5)` prints Polars' table repr.
**Reader sees:** changed: the same five rows and four columns arrive as a `shape: (5, 4)` line plus a dtype-annotated table instead of an indexed pandas block. Values identical, and the row numbers pandas showed are not referenced anywhere

<a id="c41"></a>
### C41 · `from sklearn.linear_model import LinearRegression` · output

committed output

```diff
- [text]              theta_hat
- [text] intercept    -4.605670
- [text] egg_weight    0.431229
- [text] egg_length    0.066570
- [text] egg_breadth   0.215914
- [stdout] RMSE 0.04547085380275775
+ [text] shape: (4, 2)
+ [text] ┌─────────────┬───────────┐
+ [text] │ parameter   ┆ theta_hat │
+ [text] │ ---         ┆ ---       │
+ [text] │ str         ┆ f64       │
+ [text] ╞═════════════╪═══════════╡
+ [text] │ intercept   ┆ -4.60567  │
+ [text] │ egg_weight  ┆ 0.431229  │
+ [text] │ egg_length  ┆ 0.06657   │
+ [text] │ egg_breadth ┆ 0.215914  │
+ [text] └─────────────┴───────────┘
+ [stdout] MSE 0.04547085380275759
```

**Why:** Two causes in one output. The parameter table lost its index and gained a `parameter` column (C19), and the `RMSE` label was corrected to `MSE` (C20). The float moved in its last two digits because the reduction was rewritten as a method on the Series.
**Reader sees:** changed: the four $\hat\theta$ values are byte-identical (-4.60567, 0.431229, 0.06657, 0.215914) but now sit in a two-column Polars table; and the printed line reads `MSE 0.0454708538027576` where it read `RMSE 0.0454708538027578`. The label change is a correction, not a regression — the number was always the MSE

<a id="c42"></a>
### C42 · `import numpy as np` · output

committed output

```diff
- [text] (-0.25864811956848743, 1.1034243854204049)
+ [text] (-0.26512011103620964, 1.1239590856397368)
```

**Why:** Not a figure — the eggs $\theta_1$ bootstrap CI. `np.random.seed(1337)` plus `.sample(n, replace=True)` became `pl.set_random_seed(1337)` plus `.sample(n, with_replacement=True)`, and Polars' sampler runs its own stream, so these are 10,000 different but equally valid resamples.
**Reader sees:** changed: $(-0.2586, 1.1034)$ -> $(-0.2651, 1.1240)$. The prose quoting it was regenerated to $[-0.265, 1.124]$, and the conclusion it draws — 0 lies inside, so we fail to reject — is unchanged and nowhere near the boundary.

<a id="c43"></a>
### C43 · `pl.set_random_seed(1337)` · output

committed output

```diff
- [text]              lower     upper
- [text] theta_0 -15.278542  5.161473
- [text] theta_1  -0.258648  1.103424
- [text] theta_2  -0.099138  0.208557
- [text] theta_3  -0.257141  0.758155
+ [text] shape: (4, 3)
+ [text] ┌───────────┬────────────┬──────────┐
+ [text] │ parameter ┆ lower      ┆ upper    │
+ [text] │ ---       ┆ ---        ┆ ---      │
+ [text] │ str       ┆ f64        ┆ f64      │
+ [text] ╞═══════════╪════════════╪══════════╡
+ [text] │ theta_0   ┆ -15.419956 ┆ 5.454488 │
+ [text] │ theta_1   ┆ -0.26512   ┆ 1.123959 │
+ [text] │ theta_2   ┆ -0.10361   ┆ 0.213618 │
+ [text] │ theta_3   ┆ -0.267844  ┆ 0.757189 │
+ [text] └───────────┴────────────┴──────────┘
```

**Why:** The four-parameter CI table: new bootstrap stream (C25/C26) plus the index-to-column rewrite (C27).
**Reader sees:** changed: the bounds all move in the second or third decimal, and the layout changes from an indexed pandas frame to a Polars table with a `parameter` column. The property the next paragraph depends on — that all four intervals contain 0 — still holds on every row, with the nearest bound (theta_2 lower, -0.104) well clear

<a id="c44"></a>
### C44 · `import seaborn as sns` · output

committed output

```diff
- [text] <Figure size 1000x1000 with 20 Axes>
- [image/png] 80900 bytes md5:11c8f3d0da
+ [text] <Figure size 1000x1000 with 20 Axes>
+ [image/png] 80312 bytes md5:c094d208a3
```

**Why:** Re-executed; this is the `sns.pairplot` figure, drawn through the allowlisted `.to_pandas()` (C28). The data is deterministic — no RNG involved — so only rasterisation moved. 1.18% of pixels differ, all on anti-aliased marker edges.
**Reader sees:** equivalent. Not opened individually

<a id="c45"></a>
### C45 · `from sklearn.linear_model import LinearRegression` · output

committed output

```diff
- [text]          theta_hat
- [text] theta_0  -0.058272
- [text] theta_1   0.718515
+ [text] shape: (2, 2)
+ [text] ┌───────────┬───────────┐
+ [text] │ parameter ┆ theta_hat │
+ [text] │ ---       ┆ ---       │
+ [text] │ str       ┆ f64       │
+ [text] ╞═══════════╪═══════════╡
+ [text] │ theta_0   ┆ -0.058272 │
+ [text] │ theta_1   ┆ 0.718515  │
+ [text] └───────────┴───────────┘
```

**Why:** The single-predictor fit table: index-to-`parameter`-column rewrite (C30). The fit itself is deterministic.
**Reader sees:** changed: same two values to six decimals (-0.058272, 0.718515), now in a Polars table with a `parameter` column instead of a pandas index

<a id="c46"></a>
### C46 · `import matplotlib.pyplot as plt` · output

committed output

```diff
- [text] <Figure size 768x576 with 1 Axes>
- [image/png] 22148 bytes md5:7a90d6e20f
+ [text] <Figure size 768x576 with 1 Axes>
+ [image/png] 21336 bytes md5:6f103bab63
```

**Why:** Re-executed. The figure is matplotlib over deterministic values, so nothing moved but the raster. Canvas 565x666 -> 559x663 px (tight-bbox font metrics under the current matplotlib).
**Reader sees:** equivalent. Not opened individually

<a id="c47"></a>
### C47 · `from sklearn.metrics import mean_squared_error` · output

committed output

```diff
- [stdout] RMSE of Original Model: 0.04547085380275775
- [stdout] RMSE of Interpretable Model: 0.046493941375556846
+ [stdout] MSE of Original Model: 0.04547085380275759
+ [stdout] MSE of Interpretable Model: 0.046493941375556846
```

**Why:** The `RMSE` -> `MSE` label correction (C33). The values are the numbers `mean_squared_error` always returned.
**Reader sees:** changed: both lines now read `MSE`, correctly. The interpretable model's value is byte-identical; the original model's moved in its 15th significant digit, from the reduction rewrite at C20. The comparison the paragraph draws — original 0.0455 against interpretable 0.0465 — is unchanged

<a id="c48"></a>
### C48 · `lower_int = np.percentile(estimates_int, 2.5)` · output

committed output

```diff
- [text] (0.6029335250209633, 0.8208401738546206)
+ [text] (0.6011923623702372, 0.81913763511023)
```

**Why:** The interpretable model's $\theta_1$ CI, recomputed on Polars' RNG stream (C31/C32).
**Reader sees:** equivalent: (0.6029, 0.8208) -> (0.6012, 0.8191), a third-decimal shift. The section's conclusion is that this interval does **not** contain zero, which holds by a wide margin on both

