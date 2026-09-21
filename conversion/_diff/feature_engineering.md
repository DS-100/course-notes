# feature_engineering — change report

`887a578b0a4b:content/feature_engineering/feature_engineering.ipynb` → `content/feature_engineering/feature_engineering.ipynb`

**Tier B · 26 changes:** output 7 · dropdown 5 · tab-twins 5 · code 7 · metadata 2

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

The cleanest conversion of the batch: no prose changed at all, and CONTRADICTIONS records the chapter as clean on every claim. Three idioms move — `sns.load_dataset` wrapped in `pl.from_pandas` (required; seaborn hands back pandas), `df.copy()` plus in-place column assignment collapsed into `with_columns`/`select`, and `np.mean(...)` rewritten as `(...).mean()` because NumPy's reduction dispatch rejects a Polars Series. No `.to_pandas()` was added anywhere, including for seaborn, which takes the Polars frame directly here. Worth a look: C13, where a pandas index-join became `hstack`, and the two MSE digits that are quoted in fig-alt text (C15, C17, C23, C24).

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C20](#c20) · `import plotly.graph_objects as go`
- [C21](#c21) · `contour = go.Contour(x=u[0], y=v[:, 0], z=np.reshape(MSE, u.shape))`
- [C22](#c22) · `import numpy as np`
- [C23](#c23) · `from sklearn.preprocessing import OneHotEncoder`
- [C24](#c24) · `from sklearn.linear_model import LinearRegression`
- [C25](#c25) · `vehicles = pl.from_pandas(sns.load_dataset("mpg")).drop_nulls().rename`
- [C26](#c26) · `X = vehicles[["hp"]].with_columns((pl.col("hp") ** 2).alias("hp^2"))`

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C1](#c1) · cell 2: Gradient Descent on Multi-Dimensional Models
- [C3](#c3) · cell 4 [markdown]
- [C4](#c4) · cell 4 [markdown]
- [C7](#c7) · cell 8: One-Hot Encoding
- [C15](#c15) · cell 17: Polynomial Features

## Changes

<a id="c1"></a>
### C1 · cell 2: Gradient Descent on Multi-Dimensional Models · dropdown

baseline L54 → branch L54 · mirror of the next code cell (hard rule 3)

```diff
- # df = sns.load_dataset("tips")
+ # import polars as pl
+ # df = pl.from_pandas(sns.load_dataset("tips"))
```

**Why:** Mirrors the code cell below it (C2); the import had to be added because the dropdown's block is self-contained.
**Output:** same — no output; the mirrored copy matches C2.

<a id="c2"></a>
### C2 · cell 3 [code] · code

baseline L61 → branch L62

```diff
- df = sns.load_dataset("tips")
+ import polars as pl
+ df = pl.from_pandas(sns.load_dataset("tips"))
```

**Why:** `sns.load_dataset` returns a pandas DataFrame, so it is a pandas site no `import pandas` scan would find; `pl.from_pandas` is the documented wrap, not churn.
**Output:** same values. The head repr changes (C20) and the four pandas `category` columns show as Polars `cat`.

<a id="c3"></a>
### C3 · cell 4 [markdown] · dropdown

baseline L71 → branch L73 · mirror of the next code cell (hard rule 3)

```diff
- #     return np.mean((y_hat - y_obs) ** 2)
+ #     return ((y_hat - y_obs) ** 2).mean()
```

**Why:** Mirrors C5.
**Output:** same — no output; the mirrored copy matches C5.

<a id="c4"></a>
### C4 · cell 4 [markdown] · dropdown

baseline L73 → branch L75 · mirror of the next code cell (hard rule 3)

```diff
- # tips_with_bias = df.copy()
- # tips_with_bias["bias"] = 1
- # tips_with_bias = tips_with_bias[["bias", "total_bill"]]
+ # tips_with_bias = df.with_columns(pl.lit(1).alias("bias")).select(["bias", "total_bill"])
```

**Why:** Mirrors C6.
**Output:** same — no output; the mirrored copy matches C6.

<a id="c5"></a>
### C5 · cell 5 [code] · code

baseline L111 → branch L111

```diff
-     return np.mean((y_hat - y_obs) ** 2)
+     return ((y_hat - y_obs) ** 2).mean()
```

**Why:** `np.mean` on a Polars Series raises (NumPy routes it through `_wrapreduction`, which passes `axis=`). The method form also survives every mix this helper is called with — Series minus ndarray, ndarray minus Series, and ndarray minus ndarray all return something with `.mean()`.
**Output:** same to 15 significant figures; see C24 for the one digit that moves.

<a id="c6"></a>
### C6 · cell 5 [code] · code

baseline L113 → branch L113

```diff
- tips_with_bias = df.copy()
- tips_with_bias["bias"] = 1
- tips_with_bias = tips_with_bias[["bias", "total_bill"]]
+ tips_with_bias = df.with_columns(pl.lit(1).alias("bias")).select(["bias", "total_bill"])
```

**Why:** No `.copy()` (frames are immutable), no in-place assignment. `pl.lit(1)` broadcasts the bias column and `select` fixes the column order, so three statements become one.
**Output:** same.

<a id="c7"></a>
### C7 · cell 8: One-Hot Encoding · dropdown

baseline L451 → branch L449 · spans code and prose; mirror of the next code cell (hard rule 3)

```diff
+ # import polars as pl
+ # import sklearn.linear_model as lm
+ # tips = pl.from_pandas(sns.load_dataset("tips"))
+ # tips.head()
+ # ```
+ # ````
+ 
+ # %% tags=["remove-input", "remove-output"]
+ import numpy as np
+ import seaborn as sns
+ import polars as pl
+ import sklearn.linear_model as lm
+ tips = pl.from_pandas(sns.load_dataset("tips"))
+ tips.head()
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 3afb0822 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # import numpy as np
+ # import seaborn as sns
+ # import polars as pl
+ # import sklearn.linear_model as lm
+ # tips = pl.from_pandas(sns.load_dataset("tips"))
+ # tips.head()
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
+ … 10 more lines
```

**Why:** Mirrors the setup cell below it, which became Polars; the cell was hidden and re-published as a synced Polars/pandas tab pair.
**Output:** differs: Polars repr for `tips.head()` (C20), with `sex`/`smoker`/`day`/`time` shown as `cat`. The mirrored copy matches the code cell it mirrors.

<a id="c8"></a>
### C8 · cell 10 [markdown] · tab-twins

baseline L456 → branch L504 · spans code and prose

```diff
- # ````
- 
- # %% tags=["remove-input"]
- import numpy as np
- import seaborn as sns
- import pandas as pd
- import sklearn.linear_model as lm
- tips = sns.load_dataset("tips")
- tips.head()
+ #
+ # ```text
+ #    total_bill   tip     sex smoker  day    time  size
+ # 0       16.99  1.01  Female     No  Sun  Dinner     2
+ # 1       10.34  1.66    Male     No  Sun  Dinner     3
+ # 2       21.01  3.50    Male     No  Sun  Dinner     3
+ # 3       23.68  3.31    Male     No  Sun  Dinner     2
+ # 4       24.59  3.61  Female     No  Sun  Dinner     4
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** The pandas half of the same tab pair: the baseline cell body and its baseline output are kept as the `pandas` tab rather than deleted.
**Output:** differs: this is the baseline's pandas table, preserved for comparison.

<a id="c9"></a>
### C9 · cell 12 [code] · metadata

baseline L490 → branch L541

```diff
- # %%
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c10"></a>
### C10 · cell 12 [code] · code

baseline L501 → branch L552

```diff
- encoded_day_df = pd.DataFrame(encoded_day, columns=ohe.get_feature_names_out())
+ encoded_day_df = pl.DataFrame(encoded_day, schema=list(ohe.get_feature_names_out()))
```

**Why:** `pd.DataFrame(arr, columns=...)` → `pl.DataFrame(arr, schema=list(...))`. The `list(...)` is load-bearing: `schema=` rejects the ndarray that `get_feature_names_out()` returns.
**Output:** same four one-hot columns, same names and values.

<a id="c11"></a>
### C11 · cell 12 [code] · tab-twins

baseline L504 → branch L555 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 88a7f85b -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # from sklearn.preprocessing import OneHotEncoder
+ #
+ # # Initialize a OneHotEncoder object
+ # ohe = OneHotEncoder()
+ #
+ # # Fit the encoder
+ # ohe.fit(tips[["day"]])
+ #
+ # # Use the encoder to transform the raw "day" feature
+ # encoded_day = ohe.transform(tips[["day"]]).toarray()
+ # encoded_day_df = pl.DataFrame(encoded_day, schema=list(ohe.get_feature_names_out()))
+ #
+ # encoded_day_df.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 4)
+ # ┌─────────┬─────────┬─────────┬──────────┐
+ # │ day_Fri ┆ day_Sat ┆ day_Sun ┆ day_Thur │
+ # │ ---     ┆ ---     ┆ ---     ┆ ---      │
+ # │ f64     ┆ f64     ┆ f64     ┆ f64      │
+ # ╞═════════╪═════════╪═════════╪══════════╡
+ # │ 0.0     ┆ 0.0     ┆ 1.0     ┆ 0.0      │
+ # │ 0.0     ┆ 0.0     ┆ 1.0     ┆ 0.0      │
+ # │ 0.0     ┆ 0.0     ┆ 1.0     ┆ 0.0      │
+ # │ 0.0     ┆ 0.0     ┆ 1.0     ┆ 0.0      │
+ # │ 0.0     ┆ 0.0     ┆ 1.0     ┆ 0.0      │
+ # └─────────┴─────────┴─────────┴──────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ … 27 more lines
```

**Why:** Tab pair for the one-hot cell; the Polars tab carries the newly executed output, the pandas tab the baseline's.
**Output:** differs by repr only — same 5×4 values (C21).

<a id="c12"></a>
### C12 · cell 15 [code] · metadata

baseline L523 → branch L641

```diff
- # %%
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c13"></a>
### C13 · cell 15 [code] · code

baseline L525 → branch L643

```diff
- data_w_ohe = tips[["total_bill", "size", "day"]].join(encoded_day_df).drop(columns = "day")
+ data_w_ohe = tips.select(["total_bill", "size"]).hstack(encoded_day_df)
```

**Why:** pandas `.join` aligned on the row index; Polars has no index, so positional concatenation has to be said out loud. `hstack` is the form that works on every Polars in play — `pl.concat(how="horizontal")` is deprecated on the 1.43.1 pin and `horizontal_extend` does not exist below ~1.4x. Selecting the two columns up front also removes the need for the trailing `drop(columns="day")`.
**Output:** same — the six fitted coefficients are unchanged to six decimals (C22), which is the check that the rows still line up.

<a id="c14"></a>
### C14 · cell 15 [code] · tab-twins

baseline L529 → branch L647 · spans code and prose

```diff
- pd.DataFrame({"Feature":data_w_ohe.columns, "Model Coefficient":ohe_model.coef_})
+ pl.DataFrame({"Feature":data_w_ohe.columns, "Model Coefficient":ohe_model.coef_})
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 1a0cbb95 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # from sklearn.linear_model import LinearRegression
+ # data_w_ohe = tips.select(["total_bill", "size"]).hstack(encoded_day_df)
+ # ohe_model = lm.LinearRegression(fit_intercept=False) #Tell sklearn to not add an additional bias column. Why?
+ # ohe_model.fit(data_w_ohe, tips["tip"])
+ #
+ # pl.DataFrame({"Feature":data_w_ohe.columns, "Model Coefficient":ohe_model.coef_})
+ # ```
+ #
+ # ```text
+ # shape: (6, 2)
+ # ┌────────────┬───────────────────┐
+ # │ Feature    ┆ Model Coefficient │
+ # │ ---        ┆ ---               │
+ # │ str        ┆ f64               │
+ # ╞════════════╪═══════════════════╡
+ # │ total_bill ┆ 0.092994          │
+ # │ size       ┆ 0.187132          │
+ # │ day_Fri    ┆ 0.745787          │
+ # │ day_Sat    ┆ 0.621129          │
+ # │ day_Sun    ┆ 0.732289          │
+ # │ day_Thur   ┆ 0.668294          │
+ # └────────────┴───────────────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # from sklearn.linear_model import LinearRegression
+ # data_w_ohe = tips[["total_bill", "size", "day"]].join(encoded_day_df).drop(columns = "day")
+ # ohe_model = lm.LinearRegression(fit_intercept=False) #Tell sklearn to not add an additional bias column. Why?
+ # ohe_model.fit(data_w_ohe, tips["tip"])
+ … 16 more lines
```

**Why:** `pd.DataFrame` → `pl.DataFrame` for the coefficient table, plus the tab pair.
**Output:** differs by repr only — same six features and coefficients.

<a id="c15"></a>
### C15 · cell 17: Polynomial Features · dropdown

baseline L562 → branch L735 · spans code and prose; mirror of the next code cell (hard rule 3)

```diff
- # #| fig-alt: "MSE of model with (hp) feature: 23.943662938603104"
- # pd.options.mode.chained_assignment = None
+ # #| fig-alt: "MSE of model with (hp) feature: 23.943662938603108"
+ # vehicles = pl.from_pandas(sns.load_dataset("mpg")).drop_nulls().rename({"horsepower": "hp"}).sort("hp")
+ #
+ # X = vehicles[["hp"]]
+ # Y = vehicles["mpg"]
+ #
+ # hp_model = lm.LinearRegression()
+ # hp_model.fit(X, Y)
+ # hp_model_predictions = hp_model.predict(X)
+ #
+ # import matplotlib.pyplot as plt
+ #
+ # sns.scatterplot(data=vehicles, x="hp", y="mpg")
+ # plt.plot(vehicles["hp"], hp_model_predictions, c="tab:red");
+ #
+ # print(f"MSE of model with (hp) feature: {((Y - hp_model_predictions)**2).mean()}")
+ # ```
+ # ````
+ 
+ # %% tags=["remove-input"]
+ #| fig-alt: "MSE of model with (hp) feature: 23.943662938603108"
+ vehicles = pl.from_pandas(sns.load_dataset("mpg")).drop_nulls().rename({"horsepower": "hp"}).sort("hp")
+ 
+ X = vehicles[["hp"]]
+ Y = vehicles["mpg"]
+ 
+ hp_model = lm.LinearRegression()
+ hp_model.fit(X, Y)
+ hp_model_predictions = hp_model.predict(X)
+ 
+ import matplotlib.pyplot as plt
+ 
+ sns.scatterplot(data=vehicles, x="hp", y="mpg")
+ plt.plot(vehicles["hp"], hp_model_predictions, c="tab:red");
+ 
+ print(f"MSE of model with (hp) feature: {((Y - hp_model_predictions)**2).mean()}")
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin edc98ac8 -->
+ # :::::{tab-set}
+ … 30 more lines
```

**Why:** Mirrors the polynomial-feature cell below it. `pd.options.mode.chained_assignment = None` disappears: it existed only to silence pandas' `SettingWithCopyWarning` from `X["hp^2"] = ...`, which has no Polars counterpart. `sort_values` → `sort` (ascending is the default on both sides, so no sense flip), `np.mean(...)` → `(...).mean()`, and `sns.scatterplot` keeps `data=vehicles` as a Polars frame.
**Output:** differs: the MSE in the fig-alt text moves from `...104` to `...108`, which is why the alt text was edited with the code. The mirrored copy matches the code cell it mirrors.

<a id="c16"></a>
### C16 · cell 19 [markdown] · tab-twins

baseline L580 → branch L821 · spans code and prose

```diff
- # ````
- 
- # %% tags=["remove-input"]
- #| fig-alt: "MSE of model with (hp) feature: 23.943662938603104"
- pd.options.mode.chained_assignment = None
- vehicles = sns.load_dataset("mpg").dropna().rename(columns = {"horsepower": "hp"}).sort_values("hp")
- 
- X = vehicles[["hp"]]
- Y = vehicles["mpg"]
- 
- hp_model = lm.LinearRegression()
- hp_model.fit(X, Y)
- hp_model_predictions = hp_model.predict(X)
- 
- import matplotlib.pyplot as plt
- 
- sns.scatterplot(data=vehicles, x="hp", y="mpg")
- plt.plot(vehicles["hp"], hp_model_predictions, c="tab:red");
- 
- print(f"MSE of model with (hp) feature: {np.mean((Y-hp_model_predictions)**2)}")
+ #
+ # ```text
+ # MSE of model with (hp) feature: 23.943662938603104
+ # <Figure size 640x480 with 1 Axes>
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** The pandas half of the same tab pair: the baseline cell and its output are kept as the `pandas` tab.
**Output:** differs: the pandas tab preserves the baseline's `...104`, which is the number that build printed.

<a id="c17"></a>
### C17 · cell 21 [code] · code

baseline L609 → branch L838

```diff
- # %%
- #| fig-alt: "Untransformed data. MSE of model with (hp^2) feature: 18.98476890761722"
+ # %% tags=["remove-input"]
+ #| fig-alt: "Untransformed data. MSE of model with (hp^2) feature: 18.984768907617216"
```

**Why:** Fig-alt text re-quoted from the re-executed cell, and the cell hidden for the tab pair below it.
**Output:** differs: the quoted MSE gains three digits (`18.98476890761722` → `18.984768907617216`) — see C24.

<a id="c18"></a>
### C18 · cell 21 [code] · code

baseline L612 → branch L841

```diff
- X = vehicles[["hp"]]
- X["hp^2"] = vehicles["hp"]**2
+ X = vehicles[["hp"]].with_columns((pl.col("hp") ** 2).alias("hp^2"))
```

**Why:** Chained assignment into a slice of `X` becomes `with_columns`. This is the exact line the `chained_assignment` option removed in C15 existed to silence.
**Output:** same design matrix, same fit.

<a id="c19"></a>
### C19 · cell 21 [code] · tab-twins

baseline L623 → branch L851 · spans code and prose

```diff
- print(f"MSE of model with (hp^2) feature: {np.mean((Y-hp2_model_predictions)**2)}")
+ print(f"MSE of model with (hp^2) feature: {((Y - hp2_model_predictions)**2).mean()}")
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 21180eea -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Add a hp^2 feature to the design matrix
+ # X = vehicles[["hp"]].with_columns((pl.col("hp") ** 2).alias("hp^2"))
+ #
+ # # Use sklearn to fit the model
+ # hp2_model = lm.LinearRegression()
+ # hp2_model.fit(X, Y)
+ # hp2_model_predictions = hp2_model.predict(X)
+ #
+ # sns.scatterplot(data=vehicles, x="hp", y="mpg")
+ # plt.plot(vehicles["hp"], hp2_model_predictions, c="tab:red");
+ #
+ # print(f"MSE of model with (hp^2) feature: {((Y - hp2_model_predictions)**2).mean()}")
+ # ```
+ #
+ # ```text
+ # MSE of model with (hp^2) feature: 18.984768907617216
+ # <Figure size 640x480 with 1 Axes>
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # Add a hp^2 feature to the design matrix
+ # X = vehicles[["hp"]]
+ # X["hp^2"] = vehicles["hp"]**2
+ #
+ # # Use sklearn to fit the model
+ # hp2_model = lm.LinearRegression()
+ # hp2_model.fit(X, Y)
+ # hp2_model_predictions = hp2_model.predict(X)
+ #
+ … 13 more lines
```

**Why:** `np.mean(...)` → `(...).mean()` (same dispatch reason as C5), plus the tab pair.
**Output:** differs in the last digit of the printed MSE — see C24.

<a id="c20"></a>
### C20 · `import plotly.graph_objects as go` · output

committed output

```diff
- [plotly] figure md5:97d33ad201
- [plotly] trace 0 surface
- [plotly] trace 1 scatter3d name='Optimal Point' x: n=1 min=1.11111 max=1.11111 y: n=1 min=0.1 max=0.1 z: n=1 min=1.04637 max=1.04637
+ [plotly] figure md5:1be6452ebb
+ [plotly] trace 0 surface
+ [plotly] trace 1 scatter3d name='Optimal Point' x: n=1 min=1.11111 max=1.11111 y: n=1 min=0.1 max=0.1 z: n=1 min=1.04637 max=1.04637
```

**Why:** The MSE grid behind the surface is now computed with `((y_hat - y_obs) ** 2).mean()` instead of `np.mean(...)`, which changes the float accumulation order; the 10x10 `z` grid moves by at most 1.07e-14 (relative 2.6e-16). The `Optimal Point` marker is untouched — same grid cell at (1.11111, 0.1, 1.04637).
**Reader sees:** equivalent.

<a id="c21"></a>
### C21 · `contour = go.Contour(x=u[0], y=v[:, 0], z=np.reshape(MSE, u.shape))` · output

committed output

```diff
- [plotly] figure md5:bf5d0c064d
- [plotly] trace 0 contour
+ [plotly] figure md5:4b8b1d44a7
+ [plotly] trace 0 contour
```

**Why:** The same MSE grid feeds the contour, with the same 1.07e-14 worst-case movement. Nothing else in the payload differs but plotly's `[0, 1]` -> `[0.0, 1.0]` layout formatting.
**Reader sees:** equivalent — identical contour rings at identical levels.

<a id="c22"></a>
### C22 · `import numpy as np` · output

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

**Why:** Polars repr for the tips head.
**Reader sees:** equivalent — same five rows and values, plus a dtype row in which the pandas `category` columns read `cat`; the 0–4 row labels are gone.

<a id="c23"></a>
### C23 · `from sklearn.preprocessing import OneHotEncoder` · output

committed output

```diff
- [text]    day_Fri  day_Sat  day_Sun  day_Thur
- [text] 0      0.0      0.0      1.0       0.0
- [text] 1      0.0      0.0      1.0       0.0
- [text] 2      0.0      0.0      1.0       0.0
- [text] 3      0.0      0.0      1.0       0.0
- [text] 4      0.0      0.0      1.0       0.0
+ [text] shape: (5, 4)
+ [text] ┌─────────┬─────────┬─────────┬──────────┐
+ [text] │ day_Fri ┆ day_Sat ┆ day_Sun ┆ day_Thur │
+ [text] │ ---     ┆ ---     ┆ ---     ┆ ---      │
+ [text] │ f64     ┆ f64     ┆ f64     ┆ f64      │
+ [text] ╞═════════╪═════════╪═════════╪══════════╡
+ [text] │ 0.0     ┆ 0.0     ┆ 1.0     ┆ 0.0      │
+ [text] │ 0.0     ┆ 0.0     ┆ 1.0     ┆ 0.0      │
+ [text] │ 0.0     ┆ 0.0     ┆ 1.0     ┆ 0.0      │
+ [text] │ 0.0     ┆ 0.0     ┆ 1.0     ┆ 0.0      │
+ [text] │ 0.0     ┆ 0.0     ┆ 1.0     ┆ 0.0      │
+ [text] └─────────┴─────────┴─────────┴──────────┘
```

**Why:** `pl.DataFrame` repr for the one-hot frame.
**Reader sees:** equivalent — same 5×4 values.

<a id="c24"></a>
### C24 · `from sklearn.linear_model import LinearRegression` · output

committed output

```diff
- [text]       Feature  Model Coefficient
- [text] 0  total_bill           0.092994
- [text] 1        size           0.187132
- [text] 2     day_Fri           0.745787
- [text] 3     day_Sat           0.621129
- [text] 4     day_Sun           0.732289
- [text] 5    day_Thur           0.668294
+ [text] shape: (6, 2)
+ [text] ┌────────────┬───────────────────┐
+ [text] │ Feature    ┆ Model Coefficient │
+ [text] │ ---        ┆ ---               │
+ [text] │ str        ┆ f64               │
+ [text] ╞════════════╪═══════════════════╡
+ [text] │ total_bill ┆ 0.092994          │
+ [text] │ size       ┆ 0.187132          │
+ [text] │ day_Fri    ┆ 0.745787          │
+ [text] │ day_Sat    ┆ 0.621129          │
+ [text] │ day_Sun    ┆ 0.732289          │
+ [text] │ day_Thur   ┆ 0.668294          │
+ [text] └────────────┴───────────────────┘
```

**Why:** `pl.DataFrame` repr for the coefficient table; the numbers come from the same fit.
**Reader sees:** equivalent — all six coefficients identical to six decimals, which also confirms the `hstack` in C13 aligned the rows the way the index-join did.

<a id="c25"></a>
### C25 · `vehicles = pl.from_pandas(sns.load_dataset("mpg")).drop_nulls().rename` · output

committed output

```diff
- [stdout] MSE of model with (hp) feature: 23.943662938603104
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 41940 bytes md5:207e81a653
+ [stdout] MSE of model with (hp) feature: 23.943662938603108
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 41224 bytes md5:bda0dbb81e
```

**Why:** Not the reduction change: re-run in the pinned env the *pandas* code prints `23.943662938603108` too (verified), so the baseline's `...104` is drift from the environment the baseline was executed in. The figure was re-rendered; pixel-diffed against the baseline it is the same scatter and the same red line, on a canvas one pixel wider.
**Reader sees:** equivalent.

<a id="c26"></a>
### C26 · `X = vehicles[["hp"]].with_columns((pl.col("hp") ** 2).alias("hp^2"))` · output

committed output

```diff
- [stdout] MSE of model with (hp^2) feature: 18.98476890761722
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 44344 bytes md5:928f55e1e8
+ [stdout] MSE of model with (hp^2) feature: 18.984768907617216
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 43660 bytes md5:f62bcd5b19
```

**Why:** Here the digit genuinely is the reduction: with `hp^2` in the design matrix, `((Y - pred)**2).mean()` on a Polars Series gives `18.984768907617216` where `np.mean` over the pandas Series gives `18.98476890761722` (verified side by side) — a 4e-15 difference from summation order. Figure re-rendered and pixel-identical apart from the same one-pixel canvas width.
**Reader sees:** equivalent.

