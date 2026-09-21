# logistic_regression_1 — change report

`887a578b0a4b:content/logistic_regression_1/logistic_reg_1.ipynb` → `content/logistic_regression_1/logistic_reg_1.ipynb`

**Tier B · 14 changes:** output 6 · dropdown 3 · tab-twins 1 · code 4

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

Mechanical apart from one real rewrite: `pd.cut` has no Polars equivalent, so the 20-bin graph of averages is now built by hand (C5). No prose changed, and CONTRADICTIONS records the chapter clean across its 23 claims. The four moved figures differ only in `sns.stripplot`'s unseeded jitter — pixel-diffed against the baseline, every overlaid curve coincides. The one thing to check is C5: the new binning closes bins on the left where `pd.cut` closed them on the right, which moves a handful of games between adjacent bins and two plotted win rates in the third decimal.

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C9](#c9) · `import warnings`
- [C10](#c10) · `import seaborn as sns`
- [C11](#c11) · `import sklearn.linear_model as lm`
- [C12](#c12) · `n_bins = 20`
- [C13](#c13) · `import plotly.graph_objects as go`
- [C14](#c14) · `xs = np.linspace(-0.3, 0.3)`

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C1](#c1) · cell 1: The Logistic Regression Model
- [C3](#c3) · cell 6 [markdown]
- [C7](#c7) · cell 12: We'll discuss the `LogisticRegression` class next time

## Changes

<a id="c1"></a>
### C1 · cell 1: The Logistic Regression Model · dropdown

baseline L96 → branch L96 · spans code and prose; mirror of the next code cell (hard rule 3)

```diff
+ # import polars as pl
+ # import numpy as np
+ # np.seterr(divide='ignore')
+ #
+ # games = pl.read_csv("data/games").drop_nulls()
+ # games.head()
+ # ```
+ # ````
+ 
+ # %% tags=["remove-input", "remove-output"]
+ import warnings
+ warnings.filterwarnings("ignore")
+ 
+ import polars as pl
+ import numpy as np
+ np.seterr(divide='ignore')
+ 
+ games = pl.read_csv("data/games").drop_nulls()
+ games.head()
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 838394a9 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # import warnings
+ # warnings.filterwarnings("ignore")
+ #
+ # import polars as pl
+ # import numpy as np
+ # np.seterr(divide='ignore')
+ #
+ # games = pl.read_csv("data/games").drop_nulls()
+ # games.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 6)
+ # ┌──────────┬───────────────────┬─────────────┬─────┬───────────┬─────┐
+ … 19 more lines
```

**Why:** Mirrors the setup cell below it, which became `pl.read_csv` + `drop_nulls`; the cell was hidden and re-published as a synced Polars/pandas tab pair.
**Output:** differs: Polars repr for `games.head()` (C9). The mirrored copy matches the code cell it mirrors.

<a id="c2"></a>
### C2 · cell 3 [markdown] · tab-twins

baseline L103 → branch L162 · spans code and prose

```diff
- # ````
- 
- # %% tags=["remove-input"]
- import warnings
- warnings.filterwarnings("ignore")
- 
- import pandas as pd
- import numpy as np
- np.seterr(divide='ignore')
- 
- games = pd.read_csv("data/games").dropna()
- games.head()
+ #
+ # ```text
+ #     GAME_ID          TEAM_NAME      MATCHUP  WON  GOAL_DIFF  AST
+ # 0  21701216   Dallas Mavericks  DAL vs. PHX    0     -0.251   20
+ # 1  21700846       Phoenix Suns    PHX @ GSW    0     -0.237   13
+ # 2  21700071  San Antonio Spurs    SAS @ ORL    0     -0.234   19
+ # 3  21700221    New York Knicks    NYK @ TOR    0     -0.234   17
+ # 4  21700306         Miami Heat    MIA @ NYK    0     -0.222   21
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** The pandas half of the same tab pair: the baseline cell body and its output are kept as the `pandas` tab rather than deleted.
**Output:** differs: this is the baseline's pandas table, preserved for comparison.

<a id="c3"></a>
### C3 · cell 6 [markdown] · dropdown

baseline L154 → branch L213 · mirror of the next code cell (hard rule 3)

```diff
- # plt.plot(X.squeeze(), regression_model.predict(X), "k")
+ # plt.plot(X.to_series(), regression_model.predict(X), "k")
```

**Why:** Mirrors C4.
**Output:** same — no output; the mirrored copy matches C4.

<a id="c4"></a>
### C4 · cell 7 [code] · code

baseline L168 → branch L227

```diff
- plt.plot(X.squeeze(), regression_model.predict(X), "k")
+ plt.plot(X.to_series(), regression_model.predict(X), "k")
```

**Why:** `X` is a one-column Polars DataFrame and Polars has no `.squeeze()`. `.to_series()` is the direct replacement and keeps the x-values a named Series, which matplotlib takes directly — no `.to_numpy()` is needed or added.
**Output:** same line, same data.

<a id="c5"></a>
### C5 · cell 9 [code] · code

baseline L185 → branch L244

```diff
- # bucket the GOAL_DIFF data into 20 bins
- bins = pd.cut(games["GOAL_DIFF"], 20)
- games["bin"] = [(b.left + b.right) / 2 for b in bins]
- win_rates_by_bin = games.groupby("bin")["WON"].mean()
+ # bucket the GOAL_DIFF data into 20 bins of equal width
+ n_bins = 20
+ lo, hi = games["GOAL_DIFF"].min(), games["GOAL_DIFF"].max()
+ width = (hi - lo) / n_bins
+ 
+ # label each game with the center of the bin its GOAL_DIFF falls into
+ # clip keeps the largest value in the last bin instead of in a bin of its own
+ bin_number = ((pl.col("GOAL_DIFF") - lo) / width).floor().clip(0, n_bins - 1)
+ games = games.with_columns((lo + (bin_number + 0.5) * width).alias("bin"))
+ 
+ # compute the average WON value in each bin, ordered by bin so the curve plots left to right
+ win_rates_by_bin = games.group_by("bin").agg(pl.col("WON").mean()).sort("bin")
```

**Why:** Polars has no `pd.cut`. The replacement computes the bin width explicitly, floors each value into a bin number, clips the maximum into the last bin, and labels the row with the bin centre; the group mean then needs an explicit `.sort("bin")` because Polars does not guarantee group order and the curve has to plot left to right.
**Output:** differs: verified on all 1230 games, `pd.cut` closes its bins on the right and this construction closes them on the left, so a few games per boundary change bins — the largest count shift is 5 (174→169, 156→161) and two plotted win rates move in the third decimal (0.5057→0.5030, 0.7051→0.7019). Bin centres also differ by ≤3e-4 because `pd.cut` rounds its interval labels to three decimals. 19 non-empty bins either way.

<a id="c6"></a>
### C6 · cell 9 [code] · code

baseline L192 → branch L259

```diff
- plt.plot(win_rates_by_bin.index, win_rates_by_bin, c="tab:red")
+ plt.plot(win_rates_by_bin["bin"], win_rates_by_bin["WON"], c="tab:red")
```

**Why:** `win_rates_by_bin` is a two-column DataFrame in Polars, not a Series carrying the bin as its index, so both axes become named columns.
**Output:** same curve, drawn from the same two vectors.

<a id="c7"></a>
### C7 · cell 12: We'll discuss the `LogisticRegression` class next time · dropdown

baseline L320 → branch L387 · mirror of the next code cell (hard rule 3)

```diff
- # plt.plot(win_rates_by_bin.index, win_rates_by_bin, lw=2, c="tab:red", label="Graph of averages")
+ # plt.plot(win_rates_by_bin["bin"], win_rates_by_bin["WON"], lw=2, c="tab:red", label="Graph of averages")
```

**Why:** Mirrors C8 — the same index-to-column change.
**Output:** same — no output; the mirrored copy matches C8.

<a id="c8"></a>
### C8 · cell 13 [code] · code

baseline L337 → branch L404

```diff
- plt.plot(win_rates_by_bin.index, win_rates_by_bin, lw=2, c="tab:red", label="Graph of averages")
+ plt.plot(win_rates_by_bin["bin"], win_rates_by_bin["WON"], lw=2, c="tab:red", label="Graph of averages")
```

**Why:** Same as C6: the graph-of-averages vectors are now columns.
**Output:** same curve.

<a id="c9"></a>
### C9 · `import warnings` · output

committed output

```diff
- [text]     GAME_ID          TEAM_NAME      MATCHUP  WON  GOAL_DIFF  AST
- [text] 0  21701216   Dallas Mavericks  DAL vs. PHX    0     -0.251   20
- [text] 1  21700846       Phoenix Suns    PHX @ GSW    0     -0.237   13
- [text] 2  21700071  San Antonio Spurs    SAS @ ORL    0     -0.234   19
- [text] 3  21700221    New York Knicks    NYK @ TOR    0     -0.234   17
- [text] 4  21700306         Miami Heat    MIA @ NYK    0     -0.222   21
+ [text] shape: (5, 6)
+ [text] ┌──────────┬───────────────────┬─────────────┬─────┬───────────┬─────┐
+ [text] │ GAME_ID  ┆ TEAM_NAME         ┆ MATCHUP     ┆ WON ┆ GOAL_DIFF ┆ AST │
+ [text] │ ---      ┆ ---               ┆ ---         ┆ --- ┆ ---       ┆ --- │
+ [text] │ i64      ┆ str               ┆ str         ┆ i64 ┆ f64       ┆ i64 │
+ [text] ╞══════════╪═══════════════════╪═════════════╪═════╪═══════════╪═════╡
+ [text] │ 21701216 ┆ Dallas Mavericks  ┆ DAL vs. PHX ┆ 0   ┆ -0.251    ┆ 20  │
+ [text] │ 21700846 ┆ Phoenix Suns      ┆ PHX @ GSW   ┆ 0   ┆ -0.237    ┆ 13  │
+ [text] │ 21700071 ┆ San Antonio Spurs ┆ SAS @ ORL   ┆ 0   ┆ -0.234    ┆ 19  │
+ [text] │ 21700221 ┆ New York Knicks   ┆ NYK @ TOR   ┆ 0   ┆ -0.234    ┆ 17  │
+ [text] │ 21700306 ┆ Miami Heat        ┆ MIA @ NYK   ┆ 0   ┆ -0.222    ┆ 21  │
+ [text] └──────────┴───────────────────┴─────────────┴─────┴───────────┴─────┘
```

**Why:** Polars repr for the games head.
**Reader sees:** changed: same five rows and values plus a dtype row, but the 0–4 row labels are gone — Polars has no index.

<a id="c10"></a>
### C10 · `import seaborn as sns` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 52736 bytes md5:b4234f8b13
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 52432 bytes md5:a76c5c0d0e
```

**Why:** Re-executed. `sns.stripplot` jitters its points with an unseeded RNG, so the cloud redraws every time; `data=games` is passed as a Polars frame, with no `.to_pandas()` added.
**Reader sees:** equivalent — pixel-diffed against the baseline, 6.4% of pixels differ and all of it is in the jittered point cloud.

<a id="c11"></a>
### C11 · `import sklearn.linear_model as lm` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 61620 bytes md5:52f9773f30
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 62136 bytes md5:427cdb8796
```

**Why:** Same stripplot jitter, with the regression line drawn over it from `.to_series()` (C4).
**Reader sees:** equivalent — 6.2% of pixels differ, confined to the jitter; the black regression line overlays the baseline's.

<a id="c12"></a>
### C12 · `n_bins = 20` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 79096 bytes md5:edfa5cc133
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 79564 bytes md5:7c18d1391c
```

**Why:** Same stripplot jitter, plus the red graph of averages now built by the hand-rolled binning in C5.
**Reader sees:** equivalent — 10.8% of pixels differ in the jittered cloud; the red curve carries the ≤0.003 win-rate shift from C5, which is about one pixel of vertical movement in two bins.

<a id="c13"></a>
### C13 · `import plotly.graph_objects as go` · output

committed output

```diff
- [plotly] figure md5:b02ea28976
- [plotly] trace 0 surface
- [plotly] title='Sigmoid with two inputs'
+ [plotly] figure md5:b9c06b4a56
+ [plotly] trace 0 surface
+ [plotly] title='Sigmoid with two inputs'
```

**Why:** The sigmoid surface is built entirely from `np.linspace` and `np.meshgrid`, so no Polars reaches it: `x`, `y` and the 100x100 `z` grid all decode byte-identical to the baseline. The md5 moves on plotly's axis-domain re-serialization alone.
**Reader sees:** equivalent.

<a id="c14"></a>
### C14 · `xs = np.linspace(-0.3, 0.3)` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 82604 bytes md5:a0d566848d
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 83112 bytes md5:482404ea9c
```

**Why:** Same stripplot jitter; the logistic curve and the graph of averages are both redrawn.
**Reader sees:** equivalent — 9.7% of pixels differ in the cloud; the logistic curve and the red curve still coincide, which is the point the caption makes.

