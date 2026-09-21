# visualization_2 — change report

`887a578b0a4b:content/visualization_2/visualization_2.ipynb` → `content/visualization_2/visualization_2.ipynb`

**Tier B · 23 changes:** output 13 · prose 2 · dropdown 3 · tab-twins 3 · code 2

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

Small Tier-B conversion of a figure-heavy chapter. Only two code sites actually moved: the
`wb` setup (`pl.read_csv(...).drop("")` in place of `index_col=0`) and the `df` construction, where
`pd.DataFrame(index=wb.index)` plus three assignments plus `dropna(inplace=True)` collapses into one
`wb.select(...).drop_nulls()`. Verified in the d100 env that both produce a (129, 2) frame with
identical `lit` and `inc` values. No `.to_pandas()` and no `.to_numpy()` anywhere: `sns.scatterplot`,
`lmplot`, `jointplot`, `kdeplot` and `sklearn.LinearRegression` all take the Polars frame directly.

Staff should look at C6, which fixes a pre-existing paragraph that put gross national income on the
y-axis when the plot puts it on x (CONTRADICTIONS A13, pre-existing); at C11, the one output whose
form changed rather than its content; and at the twelve figures, all of which are the same plot
re-rendered — canvas shrinks 455 -> 453 px or 1–2.5% of pixels differ on anti-aliased strokes, with
nothing moving on any axis.

## Needs review

- [C6](#c6) · cell 20: Linearization and Applying Transformations
- [C10](#c10) · cell 29: Additional Remarks

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C11](#c11) · `import polars as pl`
- [C12](#c12) · `plt.scatter(wb["per capita: % growth: 2016"], \`
- [C13](#c13) · `sns.scatterplot(data = wb, x = "per capita: % growth: 2016", \`
- [C14](#c14) · `np.random.seed(150)`
- [C15](#c15) · `sns.lmplot(data = wb, x = "per capita: % growth: 2016", \`
- [C16](#c16) · `sns.jointplot(data = wb, x = "per capita: % growth: 2016", \`
- [C17](#c17) · `sns.jointplot(data = wb, x = "per capita: % growth: 2016", \`
- [C18](#c18) · `sns.kdeplot(data = wb, x = "per capita: % growth: 2016", \`
- [C19](#c19) · `df = wb.select(`
- [C20](#c20) · `plt.scatter(np.log(df["inc"]), df["lit"])`
- [C21](#c21) · `plt.scatter(np.log(df["inc"]), df["lit"]**4)`
- [C22](#c22) · `from sklearn.linear_model import LinearRegression`
- [C23](#c23) · `plt.scatter(df["inc"], df["lit"], label="Untransformed data")`

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C1](#c1) · cell 2: Scatter Plots
- [C4](#c4) · cell 18: Some data cleaning to help with the next example
- [C7](#c7) · cell 24: The code below fits a linear regression model. We'll discuss

## Changes

<a id="c1"></a>
### C1 · cell 2: Scatter Plots · dropdown

baseline L46 → branch L46 · spans code and prose; mirror of the next code cell (hard rule 3)

```diff
+ # import polars as pl
+ # import numpy as np
+ # import matplotlib.pyplot as plt
+ # import seaborn as sns
+ #
+ # # The file's first column is an unnamed row label, which we drop
+ # wb = pl.read_csv("data/world_bank.csv").drop("")
+ # wb = wb.rename({'Antiretroviral therapy coverage: % of people living with HIV: 2015':"HIV rate",
+ #                 'Gross national income per capita, Atlas method: $: 2016':'gni'})
+ # wb.head()
+ # ```
+ # ````
+ 
+ # %% tags=["remove-input", "remove-output"]
+ import polars as pl
+ import numpy as np
+ import matplotlib.pyplot as plt
+ import seaborn as sns
+ 
+ # The file's first column is an unnamed row label, which we drop
+ wb = pl.read_csv("data/world_bank.csv").drop("")
+ wb = wb.rename({'Antiretroviral therapy coverage: % of people living with HIV: 2015':"HIV rate",
+                 'Gross national income per capita, Atlas method: $: 2016':'gni'})
+ wb.head()
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 48397013 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # import polars as pl
+ # import numpy as np
+ # import matplotlib.pyplot as plt
+ # import seaborn as sns
+ #
+ # # The file's first column is an unnamed row label, which we drop
+ # wb = pl.read_csv("data/world_bank.csv").drop("")
+ # wb = wb.rename({'Antiretroviral therapy coverage: % of people living with HIV: 2015':"HIV rate",
+ #                 'Gross national income per capita, Atlas method: $: 2016':'gni'})
+ … 26 more lines
```

**Why:** The setup cell was converted — `pl.read_csv("data/world_bank.csv").drop("")` replaces `pd.read_csv(..., index_col=0)` (the first header field is empty, so pandas moved it out of the column set and Polars names it `""`), and `warnings.filterwarnings("ignore", "use_inf_as_na")` goes with it because that pandas deprecation has no Polars counterpart. The surrounding block is the tab-twin that publishes the Polars source and output beside the baseline pandas pair. The cell carries `remove-input, remove-output` so the twin is the only place either pane renders — a layout pairing, not a silenced cell (checked: every `remove-output` cell in this chapter has a matching tab-twins block).
**Output:** differs: the Polars pane prints the `shape: (5, 47)` table repr; the pandas pane prints the baseline's 47-column wrapped block. Both are genuine executed output of their own code

<a id="c2"></a>
### C2 · cell 4: The file's first column is an unnamed row label, which we dr · tab-twins

baseline L50 → branch L116

```diff
- # import warnings
+ # import warnings
```

**Why:** The pandas half of the twin reproduces the baseline cell verbatim, `import warnings` included. The line itself is unchanged; only its location moved into the tab block.
**Output:** same

<a id="c3"></a>
### C3 · cell 4: The file's first column is an unnamed row label, which we dr · tab-twins

baseline L59 → branch L125 · spans code and prose

```diff
- # ````
- 
- # %% tags=["remove-input"]
- import pandas as pd
- import numpy as np
- import matplotlib.pyplot as plt
- import seaborn as sns
- import warnings
- 
- warnings.filterwarnings("ignore", "use_inf_as_na") # Suppresses distracting deprecation warnings
- 
- wb = pd.read_csv("data/world_bank.csv", index_col=0)
- wb = wb.rename(columns={'Antiretroviral therapy coverage: % of people living with HIV: 2015':"HIV rate",
-                        'Gross national income per capita, Atlas method: $: 2016':'gni'})
- wb.head()
+ #
+ # ```text
+ #   Continent   Country  \
+ # 0    Africa   Algeria
+ # 1    Africa    Angola
+ # 2    Africa     Benin
+ # 3    Africa  Botswana
+ # 5    Africa   Burundi
+ #
+ #    Primary completion rate: Male: % of relevant age group: 2015  \
+ # 0                                              106.0
+ # 1                                                NaN
+ # 2                                               83.0
+ # 3                                               98.0
+ # 5                                               58.0
+ #
+ #    Primary completion rate: Female: % of relevant age group: 2015  \
+ # 0                                              105.0
+ # 1                                                NaN
+ # 2                                               73.0
+ # 3                                              101.0
+ # 5                                               66.0
+ #
+ #    Lower secondary completion rate: Male: % of relevant age group: 2015  \
+ # 0                                               68.0
+ # 1                                                NaN
+ # 2                                               50.0
+ # 3                                               86.0
+ # 5                                               35.0
+ #
+ #    Lower secondary completion rate: Female: % of relevant age group: 2015  \
+ # 0                                               85.0
+ # 1                                                NaN
+ # 2                                               37.0
+ # 3                                               87.0
+ # 5                                               30.0
+ #
+ #    Youth literacy rate: Male: % of ages 15-24: 2005-14  \
+ # 0                                               96.0
+ # 1                                               79.0
+ … 100 more lines
```

**Why:** Same twin as C1 — the removed lines are the baseline code cell, which now sits inside the pandas tab, and the added lines are that cell's own committed output rendered as a `text` block.
**Output:** same — it is the baseline's output, republished

<a id="c4"></a>
### C4 · cell 18: Some data cleaning to help with the next example · dropdown

baseline L204 → branch L395 · mirror of the next code cell (hard rule 3)

```diff
- # df = pd.DataFrame(index=wb.index)
- # df['lit'] = wb['Adult literacy rate: Female: % ages 15 and older: 2005-14'] \
- #             + wb["Adult literacy rate: Male: % ages 15 and older: 2005-14"]
- # df['inc'] = wb['gni']
- # df.dropna(inplace=True)
+ # df = wb.select(
+ #     (pl.col('Adult literacy rate: Female: % ages 15 and older: 2005-14')
+ #      + pl.col("Adult literacy rate: Male: % ages 15 and older: 2005-14")).alias("lit"),
+ #     pl.col('gni').alias("inc"),
+ # ).drop_nulls()
```

**Why:** `pd.DataFrame(index=wb.index)` seeds an empty frame from a row index that Polars does not have; the three column assignments and `dropna(inplace=True)` (no `inplace=` in Polars) collapse into a single `wb.select(...).drop_nulls()`. Verified against the baseline in the d100 env: both give (129, 2) with `lit` and `inc` equal element for element. Mirror matches the code cell it fronts (checked mechanically for all four dropdowns in this chapter).
**Output:** same

<a id="c5"></a>
### C5 · cell 19 [code] · code

baseline L221 → branch L412

```diff
- df = pd.DataFrame(index=wb.index)
- df['lit'] = wb['Adult literacy rate: Female: % ages 15 and older: 2005-14'] \
-             + wb["Adult literacy rate: Male: % ages 15 and older: 2005-14"]
- df['inc'] = wb['gni']
- df.dropna(inplace=True)
+ df = wb.select(
+     (pl.col('Adult literacy rate: Female: % ages 15 and older: 2005-14')
+      + pl.col("Adult literacy rate: Male: % ages 15 and older: 2005-14")).alias("lit"),
+     pl.col('gni').alias("inc"),
+ ).drop_nulls()
```

**Why:** Same rewrite as C4, in the code cell.
**Output:** same

<a id="c6"></a>
### C6 · cell 20: Linearization and Applying Transformations · prose · **REVIEW**

baseline L253 → branch L444

```diff
- # Let's start by considering the gross national income variable in our plot above. Looking at the y values in the scatter plot, we can see that many large y values are all clumped together, compressing the vertical axis. The scale of the horizontal axis is also being distorted by the few large outlying x values on the right.
+ # Let's start by considering the gross national income variable in our plot above. It sits on the *horizontal* axis, and looking along it we can see that most countries are crushed against the left edge while a handful of very large incomes stretch the axis out to the right. The scale of the horizontal axis is also being distorted by the few large outlying x values on the right.
```

**Why:** The middle clause put gross national income on the y-axis. It is on x — the cell is `plt.scatter(df["inc"], df["lit"])` with `plt.xlabel("Gross national income per capita")` — and the skews confirm which variable is which (`inc` +3.325, right-skewed, gets the log; `lit` -1.25, left-skewed, gets a power). The paragraph then continues correctly about the horizontal axis, so the clause was describing the *next* paragraph's variable. CONTRADICTIONS A13 #1; pre-existing, unrelated to Polars.
**Verdict:** necessary — a fix to a false claim

<a id="c7"></a>
### C7 · cell 24: The code below fits a linear regression model. We'll discuss · dropdown

baseline L325 → branch L516 · mirror of the next code cell (hard rule 3)

```diff
- # df = df.sort_values("inc")
+ # df = df.sort("inc")
```

**Why:** `sort_values("inc")` -> `sort("inc")`, with the `ascending`/`descending` sense not in play because the baseline took the default. `inc` has no nulls at this point (C4's `drop_nulls` ran), so Polars' nulls-first ordering cannot bite. Mirror matches its code cell.
**Output:** same

<a id="c8"></a>
### C8 · cell 25 [code] · code

baseline L346 → branch L537

```diff
- df = df.sort_values("inc")
+ df = df.sort("inc")
```

**Why:** Same rename as C7, in the code cell.
**Output:** same

<a id="c9"></a>
### C9 · cell 25 [code] · tab-twins

baseline L352 → branch L543 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 38ca2d00 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # The code below fits a linear regression model. We'll discuss it at length in a future lecture
+ # from sklearn.linear_model import LinearRegression
+ #
+ # model = LinearRegression()
+ # model.fit(np.log(df[["inc"]]), df["lit"]**4)
+ # m, b = model.coef_[0], model.intercept_
+ #
+ # print(f"The slope, m, of the transformed data is: {m}")
+ # print(f"The intercept, b, of the transformed data is: {b}")
+ #
+ # df = df.sort("inc")
+ # plt.scatter(np.log(df["inc"]), df["lit"]**4, label="Transformed data")
+ # plt.plot(np.log(df["inc"]), m*np.log(df["inc"])+b, c="red", label="Linear regression")
+ # plt.xlabel("Log(gross national income per capita)")
+ # plt.ylabel("Adult literacy rate (4th power)")
+ # plt.legend();
+ # ```
+ #
+ # ```text
+ # The slope, m, of the transformed data is: 336400693.43172693
+ # The intercept, b, of the transformed data is: -1802204836.0479977
+ # <Figure size 640x480 with 1 Axes>
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # The code below fits a linear regression model. We'll discuss it at length in a future lecture
+ # from sklearn.linear_model import LinearRegression
+ #
+ # model = LinearRegression()
+ # model.fit(np.log(df[["inc"]]), df["lit"]**4)
+ … 21 more lines
```

**Why:** The cell's Polars source and output are published beside the baseline pandas pair as a tab-twin. The two panes differ only in `sort_values`/`sort` and in the last two digits of the printed slope and intercept.
**Output:** differs: the two panes' printed floats disagree in the 15th significant digit (`...43172693` vs `...43172705`), which is float accumulation order inside sklearn, not a library difference a reader should draw anything from

<a id="c10"></a>
### C10 · cell 29: Additional Remarks · prose · **REVIEW**

baseline L415 → branch L667

```diff
- # This class primarily uses `seaborn` and `matplotlib`, but `pandas` also has basic built-in plotting methods. Many other visualization libraries exist, and `plotly` is one of them.
+ # This class primarily uses `seaborn` and `matplotlib`. Many other visualization libraries exist, and `plotly` is one of them.
```

**Why:** The chapter no longer uses pandas, so the clause offering `pandas`' built-in plotting as an option had to go. Polars' own `DataFrame.plot` is not a like-for-like replacement to name here: it is Altair-backed, and the course-wide visualization decision keeps matplotlib/seaborn/plotly and excludes Altair and hvPlot. The rest of the sentence is the baseline's, unchanged.
**Verdict:** necessary — pandas-specific content that could not survive

<a id="c11"></a>
### C11 · `import polars as pl` · output

committed output

```diff
- [text]   Continent   Country  \
- [text] 0    Africa   Algeria
- [text] 1    Africa    Angola
- [text] 2    Africa     Benin
- [text] 3    Africa  Botswana
- [text] 5    Africa   Burundi
- [text]
- [text]    Primary completion rate: Male: % of relevant age group: 2015  \
- [text] 0                                              106.0
- [text] 1                                                NaN
- [text] 2                                               83.0
- [text] 3                                               98.0
- [text] 5                                               58.0
- [text]
- [text]    Primary completion rate: Female: % of relevant age group: 2015  \
- [text] 0                                              105.0
- [text] 1                                                NaN
- [text] 2                                               73.0
- [text] 3                                              101.0
- [text] 5                                               66.0
- [text]
- [text]    Lower secondary completion rate: Male: % of relevant age group: 2015  \
- [text] 0                                               68.0
- [text] 1                                                NaN
- [text] 2                                               50.0
- [text] 3                                               86.0
- [text] 5                                               35.0
- [text]
- [text]    Lower secondary completion rate: Female: % of relevant age group: 2015  \
- [text] 0                                               85.0
- [text] 1                                                NaN
- [text] 2                                               37.0
- [text] 3                                               87.0
- [text] 5                                               30.0
- [text]
- [text]    Youth literacy rate: Male: % of ages 15-24: 2005-14  \
- [text] 0                                               96.0
- [text] 1                                               79.0
- [text] 2                                               55.0
- [text] 3                                               96.0
- … 94 more lines
+ [text] shape: (5, 47)
+ [text] ┌───────────┬──────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬───────────┐
+ [text] │ Continent ┆ Country  ┆ Primary   ┆ Primary   ┆ … ┆ Children  ┆ Children  ┆ Tuberculo ┆ Tuberculo │
+ [text] │ ---       ┆ ---      ┆ completio ┆ completio ┆   ┆ sleeping  ┆ with      ┆ sis:      ┆ sis:      │
+ [text] │ str       ┆ str      ┆ n rate:   ┆ n rate:   ┆   ┆ under     ┆ fever     ┆ Treatment ┆ Cases     │
+ [text] │           ┆          ┆ Male:…    ┆ Femal…    ┆   ┆ treate…   ┆ receiving ┆ succes…   ┆ detection │
+ [text] │           ┆          ┆ ---       ┆ ---       ┆   ┆ ---       ┆ …         ┆ ---       ┆ …         │
+ [text] │           ┆          ┆ f64       ┆ f64       ┆   ┆ f64       ┆ ---       ┆ f64       ┆ ---       │
+ [text] │           ┆          ┆           ┆           ┆   ┆           ┆ f64       ┆           ┆ f64       │
+ [text] ╞═══════════╪══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪═══════════╡
+ [text] │ Africa    ┆ Algeria  ┆ 106.0     ┆ 105.0     ┆ … ┆ null      ┆ null      ┆ 88.0      ┆ 80.0      │
+ [text] │ Africa    ┆ Angola   ┆ null      ┆ null      ┆ … ┆ 25.9      ┆ 28.3      ┆ 34.0      ┆ 64.0      │
+ [text] │ Africa    ┆ Benin    ┆ 83.0      ┆ 73.0      ┆ … ┆ 72.7      ┆ 25.9      ┆ 89.0      ┆ 61.0      │
+ [text] │ Africa    ┆ Botswana ┆ 98.0      ┆ 101.0     ┆ … ┆ null      ┆ null      ┆ 77.0      ┆ 62.0      │
+ [text] │ Africa    ┆ Burundi  ┆ 58.0      ┆ 66.0      ┆ … ┆ 53.8      ┆ 25.4      ┆ 91.0      ┆ 51.0      │
+ [text] └───────────┴──────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴───────────┘
```

**Why:** Re-executed with a Polars frame, so `.head()` prints Polars' table repr instead of pandas'.
**Reader sees:** changed: the same five rows and 47 columns now arrive as a `shape: (5, 47)` line plus eight columns with dtypes and `null` for missing, where pandas wrapped all 47 columns over ~130 lines with `NaN`. The pandas row labels (0, 1, 2, 3, 5 — which incidentally revealed that row 4 had been dropped upstream) are gone, because Polars has no index. Nothing in the prose reads those labels

<a id="c12"></a>
### C12 · `plt.scatter(wb["per capita: % growth: 2016"], \` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 30828 bytes md5:14960cf5f1
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 31188 bytes md5:23ca682313
```

**Why:** Full re-execution. The plotted values are unchanged (the frames were verified identical), so the byte delta is rasterisation under the current matplotlib/seaborn. Canvas 455 -> 453 px tall.
**Reader sees:** equivalent. Not opened individually

<a id="c13"></a>
### C13 · `sns.scatterplot(data = wb, x = "per capita: % growth: 2016", \` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 63328 bytes md5:bd15a0dab4
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 63580 bytes md5:060065a6e9
```

**Why:** Full re-execution. The plotted values are unchanged (the frames were verified identical), so the byte delta is rasterisation under the current matplotlib/seaborn. `sns.scatterplot(data=wb, ...)` takes the Polars frame directly — no `.to_pandas()`. Canvas 455 -> 453 px tall.
**Reader sees:** equivalent. Not opened individually

<a id="c14"></a>
### C14 · `np.random.seed(150)` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 30792 bytes md5:d62d4fc5bf
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 31192 bytes md5:ef2c931955
```

**Why:** Full re-execution. The plotted values are unchanged (the frames were verified identical), so the byte delta is rasterisation under the current matplotlib/seaborn. The jitter is drawn under `np.random.seed(150)`, which is unchanged, so the jittered points land in the same places. Canvas 455 -> 453 px tall.
**Reader sees:** equivalent. Not opened individually

<a id="c15"></a>
### C15 · `sns.lmplot(data = wb, x = "per capita: % growth: 2016", \` · output

committed output

```diff
- [text] <Figure size 500x500 with 1 Axes>
- [image/png] 48316 bytes md5:719ded7a6b
+ [text] <Figure size 500x500 with 1 Axes>
+ [image/png] 48120 bytes md5:1995eaf0ee
```

**Why:** Full re-execution. The plotted values are unchanged (the frames were verified identical), so the byte delta is rasterisation under the current matplotlib/seaborn. `sns.lmplot(data=wb, ...)` — the one seaborn entry point in the batch that could have needed `.to_pandas()` and does not. Canvas 512x489 -> 510x490 px.
**Reader sees:** equivalent. Not opened individually

<a id="c16"></a>
### C16 · `sns.jointplot(data = wb, x = "per capita: % growth: 2016", \` · output

committed output

```diff
- [text] <Figure size 600x600 with 3 Axes>
- [image/png] 39576 bytes md5:895e97beef
+ [text] <Figure size 600x600 with 3 Axes>
+ [image/png] 40092 bytes md5:9281aeb95e
```

**Why:** Full re-execution. The plotted values are unchanged (the frames were verified identical), so the byte delta is rasterisation under the current matplotlib/seaborn. 1.36% of pixels differ, all on anti-aliased strokes of the marginal histograms.
**Reader sees:** equivalent. Not opened individually

<a id="c17"></a>
### C17 · `sns.jointplot(data = wb, x = "per capita: % growth: 2016", \` · output

committed output

```diff
- [text] <Figure size 600x600 with 3 Axes>
- [image/png] 54856 bytes md5:23cec49fd1
+ [text] <Figure size 600x600 with 3 Axes>
+ [image/png] 55096 bytes md5:280c2e09a3
```

**Why:** Full re-execution. The plotted values are unchanged (the frames were verified identical), so the byte delta is rasterisation under the current matplotlib/seaborn. 1.45% of pixels differ, same anti-aliasing pattern as C16.
**Reader sees:** equivalent. Not opened individually

<a id="c18"></a>
### C18 · `sns.kdeplot(data = wb, x = "per capita: % growth: 2016", \` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 35328 bytes md5:ef4b8e503f
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 35672 bytes md5:767aa6b931
```

**Why:** Full re-execution. The plotted values are unchanged (the frames were verified identical), so the byte delta is rasterisation under the current matplotlib/seaborn. `sns.kdeplot(data=wb, ...)` on the Polars frame. Canvas 455 -> 453 px tall.
**Reader sees:** equivalent. Not opened individually

<a id="c19"></a>
### C19 · `df = wb.select(` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 33636 bytes md5:d3c33e68be
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 33660 bytes md5:17c28664b3
```

**Why:** Re-executed after C5 rebuilt `df`. Verified that the Polars and pandas `df` hold the same 129 rows with equal `lit` and `inc`, so the scatter is the same. Canvas 455 -> 453 px tall.
**Reader sees:** equivalent. Not opened individually

<a id="c20"></a>
### C20 · `plt.scatter(np.log(df["inc"]), df["lit"])` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 33792 bytes md5:3b0eea89b6
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 34264 bytes md5:2d5a8ec00e
```

**Why:** Full re-execution. The plotted values are unchanged (the frames were verified identical), so the byte delta is rasterisation under the current matplotlib/seaborn. `np.log` is routed through `asarray`, so it takes the Polars Series directly; `inc` has no nulls after `drop_nulls`, so no divide-by-zero stderr appears. Canvas 455 -> 453 px tall.
**Reader sees:** equivalent. Not opened individually

<a id="c21"></a>
### C21 · `plt.scatter(np.log(df["inc"]), df["lit"]**4)` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 38664 bytes md5:57d9e351b9
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 38916 bytes md5:d4a99c681f
```

**Why:** Full re-execution. The plotted values are unchanged (the frames were verified identical), so the byte delta is rasterisation under the current matplotlib/seaborn. 1.75% of pixels differ.
**Reader sees:** equivalent. Not opened individually

<a id="c22"></a>
### C22 · `from sklearn.linear_model import LinearRegression` · output

committed output

```diff
- [stdout] The slope, m, of the transformed data is: 336400693.43172705
- [stdout] The intercept, b, of the transformed data is: -1802204836.0479987
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 45740 bytes md5:06bf8711db
+ [stdout] The slope, m, of the transformed data is: 336400693.43172693
+ [stdout] The intercept, b, of the transformed data is: -1802204836.0479977
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 45640 bytes md5:b62cf0e3bb
```

**Why:** Re-executed. `LinearRegression().fit(np.log(df[["inc"]]), df["lit"]**4)` takes the Polars frame and Series directly. The printed slope and intercept moved in the 15th significant digit (336400693.43172705 -> ...693, -1802204836.0479987 -> ...977) — float accumulation order inside sklearn after the frame was rebuilt, not a different fit. No prose quotes these numbers.
**Reader sees:** equivalent. The figure was opened: same 129 points, same red regression line, same axis ranges; 2.55% of pixels differ on anti-aliased marker edges

<a id="c23"></a>
### C23 · `plt.scatter(df["inc"], df["lit"], label="Untransformed data")` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 38320 bytes md5:cf21f2c062
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 38028 bytes md5:06859fd512
```

**Why:** Full re-execution. The plotted values are unchanged (the frames were verified identical), so the byte delta is rasterisation under the current matplotlib/seaborn. 1.88% of pixels differ.
**Reader sees:** equivalent. Not opened individually

