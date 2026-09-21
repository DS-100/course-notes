# visualization_1 — change report

`887a578b0a4b:content/visualization_1/visualization_1.ipynb` → `content/visualization_1/visualization_1.ipynb`

**Tier B · 48 changes:** output 29 · prose 2 · mixed 2 · dropdown 3 · tab-twins 5 · code 6 · mechanical 1

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

The heaviest chapter in this batch by figure count (26 images, all re-rendered) but a shallow
conversion: `wb` becomes `pl.read_csv(...).drop("")`, the two `.loc`-mask column assignments become
chained `when/then`, `gdp[~gdp.isna()]` becomes `.drop_nulls()`, and `value_counts` returns a
two-column DataFrame. There is no `.to_pandas()` and no `.to_numpy()` in the chapter —
`sns.countplot`, `histplot`, `boxplot` and `violinplot` all take the Polars frame in `data=`.

Three things deserve staff attention. **(1)** The "Plotting in Pandas" section is gone (C4, C6, C7):
Polars has no `.plot(kind=)`, and the `.plot` namespace it does have is Altair-backed, which the
course-wide visualization decision excludes — so the bar plot is now built twice in matplotlib
instead of once each in pandas, matplotlib and seaborn. The code change is forced; the two
paragraphs written to replace the deleted explanation are not, which is why C6 is the chapter's one
`questionable`. **(2)** C16 rewrites the whiskers definition, re-measured live in the d100 env:
fences at -3.125 and 9.075, whiskers actually drawn at -3.1 and 8.5 (CONTRADICTIONS A9 #2,
pre-existing). **(3)** C21 is the only figure whose *content* changed — it is a different cell, not
a re-render. The other 25 are the same plots with 1–2 px of canvas drift and anti-aliasing noise.

## Needs review

- [C4](#c4) · cell 5 [markdown]
- [C6](#c6) · cell 6 [code]
- [C7](#c7) · cell 9 [markdown]
- [C16](#c16) · cell 36 [markdown]

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C20](#c20) · `import polars as pl`
- [C21](#c21) · `import matplotlib.pyplot as plt # matplotlib is typically given the al`
- [C22](#c22) · `plt.bar(continent['Continent'], continent['count'])`
- [C23](#c23) · `import seaborn as sns # seaborn is typically given the alias sns`
- [C24](#c24) · `wb.head(5)`
- [C25](#c25) · `sns.countplot(data = wb, x = 'Gross national income per capita, Atlas `
- [C26](#c26) · `gni = wb["Gross national income per capita, Atlas method: $: 2016"]`
- [C27](#c27) · `sns.histplot(data=wb, x="Gross national income per capita, Atlas metho`
- [C28](#c28) · `sns.histplot(data=wb, x="Gross national income per capita, Atlas metho`
- [C29](#c29) · `densities, bins, _ = plt.hist(gni, density=True, edgecolor="white", bi`
- [C30](#c30) · `sns.histplot(data = wb, x = 'Gross national income per capita, Atlas m`
- [C31](#c31) · `sns.histplot(data = wb, x = 'Access to an improved water source: % of `
- [C32](#c32) · `wb = wb.rename({'Antiretroviral therapy coverage: % of people living w`
- [C33](#c33) · `sns.histplot(data=wb, x="HIV rate", stat="density", bins=10)`
- [C34](#c34) · `sns.histplot(data=wb, x ="HIV rate", stat="density", bins=20)`
- [C35](#c35) · `gdp = wb['Gross domestic product: % growth : 2016'].drop_nulls()`
- [C36](#c36) · `sns.boxplot(data=wb, y='Gross domestic product: % growth : 2016');`
- [C37](#c37) · `sns.boxplot(data=wb, x="Continent", y='Gross domestic product: % growt`
- [C38](#c38) · `sns.violinplot(data=wb, y="Gross national income per capita, Atlas met`
- [C39](#c39) · `import polars as pl`
- [C40](#c40) · `import seaborn as sns`
- [C41](#c41) · `data = [2.2, 2.8, 3.7, 5.3, 5.7]`
- [C42](#c42) · `plt.xlabel("Data")`
- [C43](#c43) · `plt.xlabel("Data")`
- [C44](#c44) · `def gaussian_kernel(x, z, a):`
- [C45](#c45) · `def create_kde(kernel, pts, a):`
- [C46](#c46) · `plt.xlim(-3, 10)`
- [C47](#c47) · `plt.xlim(-3, 10)`
- [C48](#c48) · `def boxcar_kernel(alpha, x, z):`

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C12](#c12) · cell 32: Quartiles
- [C13](#c13) · cell 32: Quartiles
- [C17](#c17) · cell 40: KDE Theory

## Changes

<a id="c1"></a>
### C1 · cell 2: Qualitative Variables: Bar Plots · tab-twins

baseline L113 → branch L113 · spans code and prose

```diff
+ # import polars as pl
+ # import numpy as np
+ #
+ # # The file's first column is an unnamed row label, which we drop
+ # wb = pl.read_csv("data/world_bank.csv").drop("")
+ # wb.head()
+ # ```
+ # ````
+ 
+ # %% tags=["remove-input", "remove-output"]
+ import polars as pl
+ import numpy as np
+ 
+ # The file's first column is an unnamed row label, which we drop
+ wb = pl.read_csv("data/world_bank.csv").drop("")
+ wb.head()
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 2dd2b048 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # import polars as pl
+ # import numpy as np
+ #
+ # # The file's first column is an unnamed row label, which we drop
+ # wb = pl.read_csv("data/world_bank.csv").drop("")
+ # wb.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 47)
+ # ┌───────────┬──────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬───────────┐
+ # │ Continent ┆ Country  ┆ Primary   ┆ Primary   ┆ … ┆ Children  ┆ Children  ┆ Tuberculo ┆ Tuberculo │
+ # │ ---       ┆ ---      ┆ completio ┆ completio ┆   ┆ sleeping  ┆ with      ┆ sis:      ┆ sis:      │
+ # │ str       ┆ str      ┆ n rate:   ┆ n rate:   ┆   ┆ under     ┆ fever     ┆ Treatment ┆ Cases     │
+ # │           ┆          ┆ Male:…    ┆ Femal…    ┆   ┆ treate…   ┆ receiving ┆ succes…   ┆ detection │
+ # │           ┆          ┆ ---       ┆ ---       ┆   ┆ ---       ┆ …         ┆ ---       ┆ …         │
+ # │           ┆          ┆ f64       ┆ f64       ┆   ┆ f64       ┆ ---       ┆ f64       ┆ ---       │
+ … 14 more lines
```

**Why:** The setup cell was converted: `pl.read_csv("data/world_bank.csv").drop("")` replaces `pd.read_csv(..., index_col=0)` — the CSV's first header field is empty, so pandas moved that column out of the column set and Polars names it `""`; nothing downstream reads it, so dropping it is the faithful translation. `warnings.filterwarnings("ignore", "use_inf_as_na")` goes with it: that pandas deprecation has no Polars counterpart. The surrounding block is the tab-twin publishing the Polars source and output beside the baseline pandas pair. The cell carries `remove-input, remove-output`, so the twin is the only place either pane renders — a layout pairing, not a silenced cell (checked: both `remove-output` cells in this chapter have a matching tab-twins block).
**Output:** differs: the Polars pane shows the `shape: (5, 47)` table repr, the pandas pane the baseline's 47-column wrapped block. Both are real executed output of their own code

<a id="c2"></a>
### C2 · cell 4: The file's first column is an unnamed row label, which we dr · tab-twins

baseline L115 → branch L169

```diff
- # import warnings
+ # import warnings
```

**Why:** The pandas half of the twin reproduces the baseline cell verbatim, `import warnings` included; the line is unchanged and only its location moved into the tab block.
**Output:** same

<a id="c3"></a>
### C3 · cell 4: The file's first column is an unnamed row label, which we dr · tab-twins

baseline L122 → branch L176 · spans code and prose

```diff
- # ````
- 
- # %% tags=["remove-input"]
- import pandas as pd
- import numpy as np
- import warnings
- 
- warnings.filterwarnings("ignore", "use_inf_as_na") # Supresses distracting deprecation warnings
- 
- wb = pd.read_csv("data/world_bank.csv", index_col=0)
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

**Why:** Same twin as C1 — the removed lines are the baseline code cell, now inside the pandas tab, and the added lines are that cell's own committed output rendered as a `text` block.
**Output:** same — it is the baseline's output, republished

<a id="c4"></a>
### C4 · cell 5 [markdown] · mixed · **REVIEW**

baseline L135 → branch L318 · spans code and prose

```diff
- # We can visualize the distribution of the `Continent` column using a bar plot. There are a few ways to do this.
- #
- # ### Plotting in Pandas
- 
- # %%
- #| fig-alt: A bar plot with each continent on the x-axis. The heights of the bars correspond to the value count for each continent. Africa has the tallest bar and S. America has the shortest.
- wb['Continent'].value_counts().plot(kind='bar');
- 
- # %% [markdown]
- # Recall that `.value_counts()` returns a `Series` with the total count of each unique value. We call `.plot(kind='bar')` on this result to visualize these counts as a bar plot.
- #
- # Plotting methods in `pandas` are the least preferred and not supported in Data 100, as their functionality is limited. Instead, future examples will focus on other libraries built specifically for visualizing data. The most well-known library here is `matplotlib`.
+ # We can visualize the distribution of the `Continent` column using a bar plot. We will build it twice: once with `matplotlib`, which asks us to do the counting and the labelling ourselves, and once with `seaborn`, which does both from the raw `DataFrame`.
```

**Why:** Deletes the `### Plotting in Pandas` heading, the `wb['Continent'].value_counts().plot(kind='bar')` cell and the two paragraphs describing it, and replaces the lead-in with a sentence announcing two builds instead of three. There is nothing to convert this into: Polars has no pandas-style `.plot(kind=)`, and the `DataFrame.plot` namespace it does have is Altair-backed, while the course-wide visualization decision in the `pandas-to-polars` skill keeps matplotlib/seaborn/plotly and excludes Altair and hvPlot.
**Verdict:** necessary — pandas-specific content that could not survive

<a id="c5"></a>
### C5 · cell 6 [code] · code

baseline L151 → branch L323

```diff
- #| fig-alt: A bar plot with each continent on the x-axis and count on the y-axis. The heights of the bars correspond to the value count for each continent. Africa has the tallest bar and S. America has the shortest.
+ #| fig-alt: A bar plot with each continent on the x-axis. The heights of the bars correspond to the value count for each continent. Africa has the tallest bar and S. America has the shortest.
```

**Why:** The two fig-alt texts swapped because the cells did. Cell `bf7276ef`, which used to hold the pandas plot, now holds the first (unlabelled) matplotlib build, so it takes the alt text that does not mention axis labels; the labelled build keeps the one that does. Both texts are still true of the figure they sit on.
**Output:** differs: the cell's figure is a different plot now — see C21

<a id="c6"></a>
### C6 · cell 6 [code] · mixed · **REVIEW**

baseline L154 → branch L326 · spans code and prose

```diff
- continent = wb['Continent'].value_counts()
- plt.bar(continent.index, continent)
+ continent = wb['Continent'].value_counts(sort=True)
+ plt.bar(continent['Continent'], continent['count']);
+ 
+ # %% [markdown]
+ # `.value_counts(sort=True)` returns a `DataFrame` with one row per unique value: a `Continent` column holding the categories, and a `count` column holding how many times each one appears. `sort=True` orders the rows from the most common continent to the least, so the tallest bar comes first. We then hand those two columns to `plt.bar` as the labels and the heights of the bars.
+ #
+ # `matplotlib` draws what we give it and nothing more, so the plot above carries no axis labels. We add them ourselves with `plt.xlabel` and `plt.ylabel`.
+ 
+ # %%
+ #| fig-alt: A bar plot with each continent on the x-axis and count on the y-axis. The heights of the bars correspond to the value count for each continent. Africa has the tallest bar and S. America has the shortest.
+ plt.bar(continent['Continent'], continent['count'])
```

**Why:** `value_counts()` returns a DataFrame in Polars, not a Series, so `continent.index` and the bare `continent` are both gone; the columns are `Continent` and `count`, and `sort=True` restores pandas' descending order (all six counts are distinct — 47, 43, 34, 18, 13, 11 — so there is no tie-break to worry about). That part is forced. The rest is authored: because C4 deleted the paragraph explaining what `.value_counts()` returns, the explanation was re-homed here, and the matplotlib example was split into an unlabelled build plus a labelled one so the "matplotlib draws what we give it and nothing more" point has a figure to point at. Both new figures were opened and the claim holds.
**Verdict:** questionable — the code edit is forced, the cell split and the two new paragraphs are a judgement call
**Minimal alternative:** keep the single matplotlib cell with its `plt.xlabel`/`plt.ylabel`, and add only one sentence naming the `Continent` and `count` columns

<a id="c7"></a>
### C7 · cell 9 [markdown] · prose · **REVIEW**

baseline L160 → branch L341

```diff
- # While more code is required to achieve the same result, `matplotlib` is often used over `pandas` for its ability to plot more complex visualizations, some of which are discussed shortly.
- #
- # However, note how we needed to label the axes with `plt.xlabel` and `plt.ylabel`, as `matplotlib` does not support automatic axis labeling. To get around these inconveniences, we can use a more efficient plotting library: `seaborn`.
+ # `matplotlib` gives us control over every element of a figure, which is what makes it the right tool for the more complex visualizations discussed shortly. The cost is verbosity: every label is its own call. To get around these inconveniences, we can use a more efficient plotting library: `seaborn`.
```

**Why:** The opening clause compared `matplotlib` against `pandas` plotting, and C4 removed the pandas plot it compared to, so it could not stay. The closing sentence is the baseline's, unchanged.
**Verdict:** necessary — the pandas comparison could not survive. Note that only the first sentence had to go; the middle clause ("gives us control over every element") is a rewrite of a sentence that was still true, and staff can revert it to the baseline wording without breaking anything

<a id="c8"></a>
### C8 · cell 11 [markdown] · mechanical

baseline L178 → branch L357

```diff
- # By now, you'll have noticed that each of these plotting libraries have a very different syntax. As with `pandas`, we'll teach you the important methods in `matplotlib` and `seaborn`, but you'll learn more through documentation.
+ # By now, you'll have noticed that each of these plotting libraries have a very different syntax. As with `polars`, we'll teach you the important methods in `matplotlib` and `seaborn`, but you'll learn more through documentation.
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c9"></a>
### C9 · cell 19 [code] · code

baseline L255 → branch L434

```diff
- wb.loc[wb["Continent"].isin(north), "Hemisphere"] = "Northern"
- wb.loc[wb["Continent"].isin(south), "Hemisphere"] = "Southern"
+ wb = wb.with_columns(
+     pl.when(pl.col("Continent").is_in(north)).then(pl.lit("Northern"))
+       .when(pl.col("Continent").is_in(south)).then(pl.lit("Southern"))
+       .alias("Hemisphere")
+ )
```

**Why:** Two chained `wb.loc[mask, "Hemisphere"] = value` assignments — label-mask assignment that creates a column — have no Polars form; they become one `with_columns` with a chained `when/then`. Verified that `north` and `south` between them cover all six continents in the file, so the absent `.otherwise()` leaves no nulls, matching pandas, where every row got a value and the intermediate NaN never survived.
**Output:** same

<a id="c10"></a>
### C10 · cell 26 [code] · code

baseline L304 → branch L486

```diff
- #| fig-alt: Distribution with a long right tail. The highest bars are on the very right of the graph and as you progress to the left side of the graph, the bars are short.
+ #| fig-alt: Distribution with a long left tail. The highest bars are on the very right of the graph and as you progress to the left side of the graph, the bars are short.
```

**Why:** The alt text opened "Distribution with a long right tail" on the chapter's left-skew example. The cell's own `plt.title` two lines below reads "long left tail", the markdown above introduces it as the left-skew case, and the column's skew is -1.425 with mean 88.8 below median 96.0. The rest of the alt text was already correct. CONTRADICTIONS A9 #1; pre-existing, unrelated to Polars.
**Output:** same — alt text is not a committed output, and the figure is unchanged apart from the re-render at C32

<a id="c11"></a>
### C11 · cell 28 [code] · code

baseline L320 → branch L502

```diff
- wb = wb.rename(columns={'Antiretroviral therapy coverage: % of people living with HIV: 2015':"HIV rate"})
+ wb = wb.rename({'Antiretroviral therapy coverage: % of people living with HIV: 2015':"HIV rate"})
```

**Why:** `rename(columns={...})` -> `rename({...})`; Polars takes the mapping positionally and has no `columns=`.
**Output:** same

<a id="c12"></a>
### C12 · cell 32: Quartiles · dropdown

baseline L367 → branch L549 · mirror of the next code cell (hard rule 3)

```diff
- # gdp = wb['Gross domestic product: % growth : 2016']
- # gdp = gdp[~gdp.isna()]
+ # gdp = wb['Gross domestic product: % growth : 2016'].drop_nulls()
```

**Why:** `gdp[~gdp.isna()]` — a boolean-mask index applied to a Series — becomes `.drop_nulls()`, which says what it does and needs no intermediate. Mirror matches its code cell; checked mechanically, all 12 dropdowns in this chapter match the cell they front, so hard rule 3 holds throughout.
**Output:** same

<a id="c13"></a>
### C13 · cell 32: Quartiles · dropdown

baseline L372 → branch L553 · mirror of the next code cell (hard rule 3)

```diff
- # wb_quartiles = wb.copy()
- # wb_quartiles['category'] = None
- # wb_quartiles.loc[(wb_quartiles['Gross domestic product: % growth : 2016'] < q1) | (wb_quartiles['Gross domestic product: % growth : 2016'] > q3), 'category'] = 'Outside of the middle 50%'
- # wb_quartiles.loc[(wb_quartiles['Gross domestic product: % growth : 2016'] > q1) & (wb_quartiles['Gross domestic product: % growth : 2016'] < q3), 'category'] = 'In the middle 50%'
+ # growth = pl.col('Gross domestic product: % growth : 2016')
+ # wb_quartiles = wb.with_columns(
+ #     pl.when((growth < q1) | (growth > q3)).then(pl.lit('Outside of the middle 50%'))
+ #       .when((growth > q1) & (growth < q3)).then(pl.lit('In the middle 50%'))
+ #       .alias('category')
+ # )
```

**Why:** `.copy()` disappears because Polars frames are immutable, and the two `.loc[mask, 'category'] = ...` assignments become one chained `when/then`; the `growth = pl.col(...)` binding keeps the long column name from being spelled four times. Both versions use strict inequalities, so a row sitting exactly on q1 or q3 stays unlabelled under either — `None` in pandas, `null` in Polars. Mirror matches its code cell.
**Output:** same

<a id="c14"></a>
### C14 · cell 33 [code] · code

baseline L384 → branch L567

```diff
- gdp = wb['Gross domestic product: % growth : 2016']
- gdp = gdp[~gdp.isna()]
+ gdp = wb['Gross domestic product: % growth : 2016'].drop_nulls()
```

**Why:** Same rewrite as C12, in the code cell.
**Output:** same

<a id="c15"></a>
### C15 · cell 33 [code] · code

baseline L389 → branch L571

```diff
- wb_quartiles = wb.copy()
- wb_quartiles['category'] = None
- wb_quartiles.loc[(wb_quartiles['Gross domestic product: % growth : 2016'] < q1) | (wb_quartiles['Gross domestic product: % growth : 2016'] > q3), 'category'] = 'Outside of the middle 50%'
- wb_quartiles.loc[(wb_quartiles['Gross domestic product: % growth : 2016'] > q1) & (wb_quartiles['Gross domestic product: % growth : 2016'] < q3), 'category'] = 'In the middle 50%'
+ growth = pl.col('Gross domestic product: % growth : 2016')
+ wb_quartiles = wb.with_columns(
+     pl.when((growth < q1) | (growth > q3)).then(pl.lit('Outside of the middle 50%'))
+       .when((growth > q1) & (growth < q3)).then(pl.lit('In the middle 50%'))
+       .alias('category')
+ )
```

**Why:** Same rewrite as C13, in the code cell.
**Output:** same

<a id="c16"></a>
### C16 · cell 36 [markdown] · prose · **REVIEW**

baseline L418 → branch L602

```diff
- # The **whiskers** of a box-plot are the two points that lie at the \[$1^{st}$ Quartile $-$ ($1.5\times$ IQR)\], and the \[$3^{rd}$ Quartile $+$ ($1.5\times$ IQR)\]. They are the lower and upper ranges of "normal" data (the points excluding outliers).
+ # The \[$1^{st}$ Quartile $-$ ($1.5\times$ IQR)\] and \[$3^{rd}$ Quartile $+$ ($1.5\times$ IQR)\] are the **fences**. The **whiskers** are drawn to the most extreme data point that still falls inside them, so they land *on observed values* rather than on the fences themselves — for the plot above, at $-3.1$ and $8.5$ rather than at $-3.125$ and $9.075$. They are the lower and upper ranges of "normal" data (the points excluding outliers).
```

**Why:** The sentence called Q1 - 1.5*IQR and Q3 + 1.5*IQR the **whiskers**. They are the **fences**; seaborn/matplotlib draw each whisker to the most extreme observation still inside them. Re-measured on this chapter's own boxplot in the d100 env (polars 1.43.1): fences at -3.125 and 9.075, whisker caps drawn at -3.1 and 8.5 — the upper one off by 0.575, which is visible on the axis. CONTRADICTIONS A9 #2; pre-existing, unrelated to Polars. The baseline's next sentence was already what is true of the drawn whiskers and is kept.
**Verdict:** necessary — a fix to a false claim

<a id="c17"></a>
### C17 · cell 40: KDE Theory · dropdown

baseline L480 → branch L664 · spans code and prose; mirror of the next code cell (hard rule 3)

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
+ # <!-- tab-twins:begin e2b36270 -->
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

**Why:** The KDE section's setup cell was converted exactly as C1 (`read_csv(...).drop("")`, the `rename` mapping positional, the `warnings` filter dropped) and the dropdown mirror follows it. Mirror matches its code cell. This cell is also `remove-input, remove-output` with a matching tab-twin.
**Output:** differs: Polars table repr in place of the pandas wrapped block, same as C1

<a id="c18"></a>
### C18 · cell 42: The file's first column is an unnamed row label, which we dr · tab-twins

baseline L484 → branch L734

```diff
- # import warnings
+ # import warnings
```

**Why:** As C2 — the pandas pane of the KDE-section twin carries the baseline's `import warnings` unchanged.
**Output:** same

<a id="c19"></a>
### C19 · cell 42: The file's first column is an unnamed row label, which we dr · tab-twins

baseline L493 → branch L743 · spans code and prose

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
- warnings.filterwarnings("ignore", "use_inf_as_na") # Supresses distracting deprecation warnings
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

**Why:** As C3 — the baseline code cell and its committed output moved verbatim into the pandas tab.
**Output:** same — it is the baseline's output, republished

<a id="c20"></a>
### C20 · `import polars as pl` · output

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

**Why:** Re-executed with a Polars frame, so `.head()` prints Polars' table repr. Same file, same rows: verified (166, 47) both ways.
**Reader sees:** changed: the five rows arrive as a `shape: (5, 47)` line plus eight columns with dtypes and `null`, where pandas wrapped all 47 columns over ~130 lines with `NaN`. The pandas row labels (0, 1, 2, 3, 5) are gone because Polars has no index. This cell is tagged `remove-input, remove-output`, so on the page the output is visible only inside the tab-twin — see C24 for the copy that does render

<a id="c21"></a>
### C21 · `import matplotlib.pyplot as plt # matplotlib is typically given the al` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 15148 bytes md5:90f6da3a62
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 11432 bytes md5:ff33fc5bdb
```

**Why:** Not a re-render: the cell id was reused. The baseline's `wb['Continent'].value_counts().plot(kind='bar')` became the first matplotlib build when C4 removed the pandas-plotting section. Opened both PNGs.
**Reader sees:** changed: same six bars in the same descending order at the same heights (Africa 47 ... S. America 11), but the tick labels are horizontal instead of rotated 90 degrees, the bars are wider, and the `Continent` x-axis label that pandas supplied from the index name is gone. The new paragraph beside it says exactly that, and C22's labelled build restores the label — so the missing label is the point being made, not a regression

<a id="c22"></a>
### C22 · `plt.bar(continent['Continent'], continent['count'])` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 14084 bytes md5:d2ed182bb7
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 14180 bytes md5:8c2e2e8646
```

**Why:** Re-executed after `continent.index`/`continent` became the two DataFrame columns. Canvas 432x562 -> 432x563 px. Opened both.
**Reader sees:** equivalent — same bars, same order, same axis labels

<a id="c23"></a>
### C23 · `import seaborn as sns # seaborn is typically given the alias sns` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 14072 bytes md5:1a2adf06ca
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 14160 bytes md5:e46cc7f74b
```

**Why:** Full re-execution. The plotted values are unchanged — `wb` was verified to hold the same 166 rows and 47 columns as the pandas baseline — so the byte delta is rasterisation under the current matplotlib/seaborn. `sns.countplot(data=wb, x='Continent', hue='Continent')` takes the Polars frame directly, no `.to_pandas()`. Canvas 432x562 -> 432x563 px.
**Reader sees:** equivalent. Not opened individually

<a id="c24"></a>
### C24 · `wb.head(5)` · output

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

**Why:** Re-executed; `wb.head(5)` now prints the Polars repr. Unlike C20 this copy renders on the page.
**Reader sees:** changed: same five rows and 47 columns as a shape line plus a truncated, dtype-annotated table with `null` for missing, instead of pandas' wrapped block with `NaN` and row labels. No prose reads the labels or the hidden columns

<a id="c25"></a>
### C25 · `sns.countplot(data = wb, x = 'Gross national income per capita, Atlas ` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 19084 bytes md5:282a40c1ae
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 19344 bytes md5:f00a16ee5b
```

**Why:** Full re-execution. The plotted values are unchanged — `wb` was verified to hold the same 166 rows and 47 columns as the pandas baseline — so the byte delta is rasterisation under the current matplotlib/seaborn. 2.56% of pixels differ, concentrated in the dense band of overlapping tick labels. Opened both.
**Reader sees:** equivalent — the deliberately unreadable "countplot on a continuous variable" demo is unchanged, which is what the prose around it needs

<a id="c26"></a>
### C26 · `gni = wb["Gross national income per capita, Atlas method: $: 2016"]` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 21864 bytes md5:813f67a6c9
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 21168 bytes md5:d975e4785c
```

**Why:** Full re-execution. The plotted values are unchanged — `wb` was verified to hold the same 166 rows and 47 columns as the pandas baseline — so the byte delta is rasterisation under the current matplotlib/seaborn. Canvas 455 -> 453 px tall.
**Reader sees:** equivalent. Not opened individually

<a id="c27"></a>
### C27 · `sns.histplot(data=wb, x="Gross national income per capita, Atlas metho` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 30264 bytes md5:e788c0ba03
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 28748 bytes md5:a040a3e0e0
```

**Why:** Full re-execution. The plotted values are unchanged — `wb` was verified to hold the same 166 rows and 47 columns as the pandas baseline — so the byte delta is rasterisation under the current matplotlib/seaborn. `sns.histplot(data=wb, ...)` on the Polars frame. Canvas 455 -> 453 px tall. Opened both as a spot check on the seaborn-takes-Polars claim.
**Reader sees:** equivalent — identical bar heights, identical axis ranges

<a id="c28"></a>
### C28 · `sns.histplot(data=wb, x="Gross national income per capita, Atlas metho` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 29264 bytes md5:49219134db
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 28676 bytes md5:c215518c2a
```

**Why:** Full re-execution. The plotted values are unchanged — `wb` was verified to hold the same 166 rows and 47 columns as the pandas baseline — so the byte delta is rasterisation under the current matplotlib/seaborn. Canvas 455 -> 453 px tall.
**Reader sees:** equivalent. Not opened individually

<a id="c29"></a>
### C29 · `densities, bins, _ = plt.hist(gni, density=True, edgecolor="white", bi` · output

committed output

```diff
- [stdout] First bin has width 16410.0 and height 4.7741589911386953e-05
- [stdout] This corresponds to 16410.0 * 4.7741589911386953e-05 = 78.343949044586% of the data
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 14704 bytes md5:20043d4556
+ [stdout] First bin has width 16410.0 and height 4.7741589911386953e-05
+ [stdout] This corresponds to 16410.0 * 4.7741589911386953e-05 = 78.343949044586% of the data
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 14248 bytes md5:eec9f55f53
```

**Why:** Re-executed. `plt.hist(gni, ...)` takes the Polars Series directly, and the two printed lines are byte-identical to the baseline (bin width 16410.0, density 4.774e-05, 78.343949044586%), which is the strongest evidence in the chapter that the binning did not move. 0.42% of pixels differ.
**Reader sees:** equivalent

<a id="c30"></a>
### C30 · `sns.histplot(data = wb, x = 'Gross national income per capita, Atlas m` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 28432 bytes md5:2f1ba15ffb
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 26756 bytes md5:9af508cf69
```

**Why:** Full re-execution. The plotted values are unchanged — `wb` was verified to hold the same 166 rows and 47 columns as the pandas baseline — so the byte delta is rasterisation under the current matplotlib/seaborn. Canvas 455 -> 453 px tall.
**Reader sees:** equivalent. Not opened individually

<a id="c31"></a>
### C31 · `sns.histplot(data = wb, x = 'Access to an improved water source: % of ` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 24012 bytes md5:44b83ff462
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 23796 bytes md5:532ad1953d
```

**Why:** Full re-execution. The plotted values are unchanged — `wb` was verified to hold the same 166 rows and 47 columns as the pandas baseline — so the byte delta is rasterisation under the current matplotlib/seaborn. Canvas 455 -> 453 px tall.
**Reader sees:** equivalent. Not opened individually

<a id="c32"></a>
### C32 · `wb = wb.rename({'Antiretroviral therapy coverage: % of people living w` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 22840 bytes md5:f44bee6a2f
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 22084 bytes md5:b7fae21aee
```

**Why:** Full re-execution. The plotted values are unchanged — `wb` was verified to hold the same 166 rows and 47 columns as the pandas baseline — so the byte delta is rasterisation under the current matplotlib/seaborn. This is the left-skew figure whose alt text C10 corrected; the figure itself is unchanged. Canvas 455x593 -> 453x594 px.
**Reader sees:** equivalent. Not opened individually

<a id="c33"></a>
### C33 · `sns.histplot(data=wb, x="HIV rate", stat="density", bins=10)` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 17520 bytes md5:4e1ea2199f
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 16844 bytes md5:808b0e0034
```

**Why:** Full re-execution. The plotted values are unchanged — `wb` was verified to hold the same 166 rows and 47 columns as the pandas baseline — so the byte delta is rasterisation under the current matplotlib/seaborn. Canvas 455x584 -> 453x585 px.
**Reader sees:** equivalent. Not opened individually

<a id="c34"></a>
### C34 · `sns.histplot(data=wb, x ="HIV rate", stat="density", bins=20)` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 21500 bytes md5:bd590b945f
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 20468 bytes md5:5b0d8b0d76
```

**Why:** Full re-execution. The plotted values are unchanged — `wb` was verified to hold the same 166 rows and 47 columns as the pandas baseline — so the byte delta is rasterisation under the current matplotlib/seaborn. Canvas 455x584 -> 453x585 px.
**Reader sees:** equivalent. Not opened individually

<a id="c35"></a>
### C35 · `gdp = wb['Gross domestic product: % growth : 2016'].drop_nulls()` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 24120 bytes md5:c0c3694ad8
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 24176 bytes md5:e5d6ea3835
```

**Why:** Re-executed after `gdp[~gdp.isna()]` became `.drop_nulls()` (C14) — same values, same count. Canvas 432x562 -> 432x563 px.
**Reader sees:** equivalent. Not opened individually

<a id="c36"></a>
### C36 · `sns.boxplot(data=wb, y='Gross domestic product: % growth : 2016');` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 15328 bytes md5:0936c65851
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 15456 bytes md5:338b063f0c
```

**Why:** Re-executed. This is the boxplot C16's rewritten paragraph now describes; I re-derived its fences (-3.125, 9.075) and whisker caps (-3.1, 8.5) from the chapter's own data in the d100 env, so the prose and the picture agree. 0.11% of pixels differ — the smallest delta in the chapter.
**Reader sees:** equivalent

<a id="c37"></a>
### C37 · `sns.boxplot(data=wb, x="Continent", y='Gross domestic product: % growt` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 24284 bytes md5:b2ff288aca
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 24316 bytes md5:04a0f79e56
```

**Why:** Full re-execution. The plotted values are unchanged — `wb` was verified to hold the same 166 rows and 47 columns as the pandas baseline — so the byte delta is rasterisation under the current matplotlib/seaborn. `sns.boxplot(data=wb, x="Continent", ...)` on the Polars frame. 0.27% of pixels differ.
**Reader sees:** equivalent. Not opened individually

<a id="c38"></a>
### C38 · `sns.violinplot(data=wb, y="Gross national income per capita, Atlas met` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 35128 bytes md5:30d4ad91fc
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 35344 bytes md5:beeadf8b2e
```

**Why:** Full re-execution. The plotted values are unchanged — `wb` was verified to hold the same 166 rows and 47 columns as the pandas baseline — so the byte delta is rasterisation under the current matplotlib/seaborn. `sns.violinplot(data=wb, ...)` on the Polars frame. Canvas 397x597 -> 397x598 px.
**Reader sees:** equivalent. Not opened individually

<a id="c39"></a>
### C39 · `import polars as pl` · output

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

**Why:** The KDE section's setup cell, re-executed; same repr change as C20. This cell is also `remove-input, remove-output`, so the output renders only inside its tab-twin.
**Reader sees:** changed: Polars table repr in place of pandas' wrapped 47-column block, with the row labels gone. Same data — verified (166, 47) both ways

<a id="c40"></a>
### C40 · `import seaborn as sns` · output

committed output

```diff
- [text] <Figure size 500x500 with 1 Axes>
- [image/png] 30832 bytes md5:fae5003ffd
+ [text] <Figure size 500x500 with 1 Axes>
+ [image/png] 29888 bytes md5:b8e3810be8
```

**Why:** Full re-execution. The plotted values are unchanged — `wb` was verified to hold the same 166 rows and 47 columns as the pandas baseline — so the byte delta is rasterisation under the current matplotlib/seaborn. Canvas 512x489 -> 510x490 px.
**Reader sees:** equivalent. Not opened individually

<a id="c41"></a>
### C41 · `data = [2.2, 2.8, 3.7, 5.3, 5.7]` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 11884 bytes md5:c6be6a5333
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 11928 bytes md5:8410105d53
```

**Why:** Re-executed. From here to the end of the chapter the cells are pure NumPy and matplotlib KDE theory with no frame involved at all, so nothing but rasterisation can have moved. 0.30% of pixels differ.
**Reader sees:** equivalent. Not opened individually

<a id="c42"></a>
### C42 · `plt.xlabel("Data")` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 21132 bytes md5:9c48dd67f1
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 21192 bytes md5:36285db6ef
```

**Why:** Re-executed; NumPy/matplotlib only, no frame involved. 1.00% of pixels differ, on anti-aliased curves.
**Reader sees:** equivalent. Not opened individually

<a id="c43"></a>
### C43 · `plt.xlabel("Data")` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 21300 bytes md5:d182dd4572
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 21352 bytes md5:02131472b3
```

**Why:** Re-executed; NumPy/matplotlib only. 1.03% of pixels differ.
**Reader sees:** equivalent. Not opened individually

<a id="c44"></a>
### C44 · `def gaussian_kernel(x, z, a):` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 21460 bytes md5:cdd881b0e3
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 21552 bytes md5:87ec9df8e6
```

**Why:** Re-executed; NumPy/matplotlib only. 0.86% of pixels differ.
**Reader sees:** equivalent. Not opened individually

<a id="c45"></a>
### C45 · `def create_kde(kernel, pts, a):` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 59228 bytes md5:f104f3b2b7
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 59388 bytes md5:133a2b36d1
```

**Why:** Re-executed; NumPy/matplotlib only. 3.09% of pixels differ — the largest in the chapter, because the figure is five overlapping thin curves and anti-aliasing touches every one of them. Opened both.
**Reader sees:** equivalent — five Gaussian kernels at the same centres, same peak density 0.4, same axis ranges

<a id="c46"></a>
### C46 · `plt.xlim(-3, 10)` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 32260 bytes md5:0b75e07d26
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 32320 bytes md5:552d36e690
```

**Why:** Re-executed; NumPy/matplotlib only. 1.10% of pixels differ.
**Reader sees:** equivalent. Not opened individually

<a id="c47"></a>
### C47 · `plt.xlim(-3, 10)` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 21052 bytes md5:7000c73f32
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 21256 bytes md5:c592a20a25
```

**Why:** Re-executed; NumPy/matplotlib only. 0.68% of pixels differ.
**Reader sees:** equivalent. Not opened individually

<a id="c48"></a>
### C48 · `def boxcar_kernel(alpha, x, z):` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 12492 bytes md5:84d9967069
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 12828 bytes md5:f860b5fd84
```

**Why:** Re-executed; NumPy/matplotlib only (the boxcar kernel demo). 0.82% of pixels differ.
**Reader sees:** equivalent. Not opened individually

