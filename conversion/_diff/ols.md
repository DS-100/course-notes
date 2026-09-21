# ols — change report

`887a578b0a4b:content/ols/ols.ipynb` → `content/ols/ols.ipynb`

**Tier B · 7 changes:** output 2 · prose 3 · tab-twins 1 · code 1

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

Mechanical conversion of a short chapter: one `read_csv`, one column selection, and two committed tables reprinted in Polars' repr. The substance is in the prose, where two pre-existing factual errors are corrected (CONTRADICTIONS §A11) and one `.iloc`/`.loc` analogy is re-aimed at a form Polars has. Three things for staff: C1, where `index_col=0` became `.drop('Rk')`, so the rank numbers the reader used to see down the left edge of `nba.head(5)` are gone; C2, the `FG` correction, which is load-bearing because the fitted `FG` coefficient of 2.517 is only readable if threes are known to be in there; and C5, which replaces a pandas-only analogy rather than deleting it.

## Needs review

- [C2](#c2) · cell 5 [markdown]
- [C4](#c4) · cell 8: Mean Squared Error
- [C5](#c5) · cell 8: Geometric Derivation

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C6](#c6) · `nba.head(5)`
- [C7](#c7) · `nba.select(['FG', 'AST', '3PA', 'PTS']).head()`

## Changes

<a id="c1"></a>
### C1 · cell 3 [code] · code

baseline L45 → branch L45

```diff
- import pandas as pd
- nba = pd.read_csv('data/nba18-19.csv', index_col=0)
- nba.index.name = None # Drops name of index (players are ordered by rank)
+ import polars as pl
+ nba = pl.read_csv('data/nba18-19.csv').drop('Rk') # Drops the rank column (players are ordered by rank)
```

**Why:** pandas read the rank column into the index and then blanked its name. Polars has no index, so the faithful move is to drop the column outright — nothing downstream reads it (`Rk` occurs exactly once in the notebook, on this line). Column count is unchanged at 29 either way.
**Output:** differs: the head tables lose the leading 1–5 rank labels (C6, C7). All 29 remaining columns and every value are unchanged.

<a id="c2"></a>
### C2 · cell 5 [markdown] · prose · **REVIEW**

baseline L57 → branch L56

```diff
- # * `FG`, the average number of (2-point) field goals per game
+ # * `FG`, the average number of field goals made per game — all of them, three-pointers included, so `FG` is `2P` plus `3P`
```

**Why:** `FG` is *total* field goals with threes included, not 2-point field goals; the dataset carries a separate `2P` column and `PTS = 2·FG + 3P + FT` reconstructs points to within 0.05 per game. CONTRADICTIONS §A11 #1 — pre-existing, present verbatim in the baseline.
**Verdict:** necessary — a fix to a false claim, and a load-bearing one: the chapter later fits a coefficient of 2.517 on `FG`, which is unreadable under the 2-point reading.

<a id="c3"></a>
### C3 · cell 6 [code] · tab-twins

baseline L61 → branch L60 · spans code and prose

```diff
- # %%
- nba[['FG', 'AST', '3PA', 'PTS']].head()
+ # %% tags=["remove-input", "remove-output"]
+ nba.select(['FG', 'AST', '3PA', 'PTS']).head()
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 2ff5030e -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # nba.select(['FG', 'AST', '3PA', 'PTS']).head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 4)
+ # ┌─────┬─────┬─────┬──────┐
+ # │ FG  ┆ AST ┆ 3PA ┆ PTS  │
+ # │ --- ┆ --- ┆ --- ┆ ---  │
+ # │ f64 ┆ f64 ┆ f64 ┆ f64  │
+ # ╞═════╪═════╪═════╪══════╡
+ # │ 1.8 ┆ 0.6 ┆ 4.1 ┆ 5.3  │
+ # │ 0.4 ┆ 0.8 ┆ 1.5 ┆ 1.7  │
+ # │ 1.1 ┆ 1.9 ┆ 2.2 ┆ 3.2  │
+ # │ 6.0 ┆ 1.6 ┆ 0.0 ┆ 13.9 │
+ # │ 3.4 ┆ 2.2 ┆ 0.2 ┆ 8.9  │
+ # └─────┴─────┴─────┴──────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # nba[['FG', 'AST', '3PA', 'PTS']].head()
+ # ```
+ #
+ # ```text
+ #     FG  AST  3PA   PTS
+ # 1  1.8  0.6  4.1   5.3
+ # 2  0.4  0.8  1.5   1.7
+ # 3  1.1  1.9  2.2   3.2
+ # 4  6.0  1.6  0.0  13.9
+ … 5 more lines
```

**Why:** `df[[cols]]` → `.select([cols])`. The cell was then hidden (`remove-input`, `remove-output`) and its output re-published as a synced Polars/pandas tab pair, so the reader sees both idioms side by side instead of only the converted one.
**Output:** differs: Polars' box repr with a dtype row (C7). Same five rows, same four columns, same values.

<a id="c4"></a>
### C4 · cell 8: Mean Squared Error · prose · **REVIEW**

baseline L191 → branch L233

```diff
- # The double bars are mathematical notation for the norm. The subscript 2 indicates that we are computing the L2, or squared norm.
+ # The double bars are mathematical notation for the norm. The subscript 2 indicates that we are computing the L2, or Euclidean, norm.
```

**Why:** The definition two lines above is $\sqrt{\sum(a_i-b_i)^2}$ — a square root — and the chapter itself draws the distinction eleven lines later. If $\|\cdot\|_2$ were already squared, the MSE formula would be a fourth power. CONTRADICTIONS §A11 #2 — pre-existing.
**Verdict:** necessary — a fix to a false claim. Nothing about it is library-specific, so staff may prefer to land it against `main` as well.

<a id="c5"></a>
### C5 · cell 8: Geometric Derivation · prose · **REVIEW**

baseline L277 → branch L319

```diff
- # Up until now, we've mostly thought of our model as a scalar product between horizontally stacked observations and the parameter vector. We can also think of $\hat{\mathbb{Y}}$ as a **linear combination of feature vectors**, scaled by the **parameters**. We use the notation $\mathbb{X}_{:, i}$ to denote the $i$th column of the design matrix. You can think of this as following the same convention as used when calling `.iloc` and `.loc`. ":" means that we are taking all entries in the $i$th column.
+ # Up until now, we've mostly thought of our model as a scalar product between horizontally stacked observations and the parameter vector. We can also think of $\hat{\mathbb{Y}}$ as a **linear combination of feature vectors**, scaled by the **parameters**. We use the notation $\mathbb{X}_{:, i}$ to denote the $i$th column of the design matrix. You can think of this as following the same convention as used when indexing a `DataFrame` with `df[:, i]`. ":" means that we are taking all entries in the $i$th column.
```

**Why:** `.iloc` and `.loc` do not exist in Polars, so the analogy pointed at nothing a reader could try. `df[:, i]` is the Polars form and does return column $i$ (verified: `nba[:, 1]` is `Pos`). CONTRADICTIONS lists this under the conversion repairing a pre-existing inaccuracy in passing.
**Verdict:** necessary — pandas-specific content that could not survive as written.

<a id="c6"></a>
### C6 · `nba.head(5)` · output

committed output

```diff
- [text]                    Player Pos  Age   Tm   G  GS    MP   FG   FGA    FG%  ...  \
- [text] 1  Álex Abrines\abrinal01  SG   25  OKC  31   2  19.0  1.8   5.1  0.357  ...
- [text] 2      Quincy Acy\acyqu01  PF   28  PHO  10   0  12.3  0.4   1.8  0.222  ...
- [text] 3  Jaylen Adams\adamsja01  PG   22  ATL  34   1  12.6  1.1   3.2  0.345  ...
- [text] 4  Steven Adams\adamsst01   C   25  OKC  80  80  33.4  6.0  10.1  0.595  ...
- [text] 5   Bam Adebayo\adebaba01   C   21  MIA  82  28  23.3  3.4   5.9  0.576  ...
- [text]
- [text]      FT%  ORB  DRB  TRB  AST  STL  BLK  TOV   PF   PTS
- [text] 1  0.923  0.2  1.4  1.5  0.6  0.5  0.2  0.5  1.7   5.3
- [text] 2  0.700  0.3  2.2  2.5  0.8  0.1  0.4  0.4  2.4   1.7
- [text] 3  0.778  0.3  1.4  1.8  1.9  0.4  0.1  0.8  1.3   3.2
- [text] 4  0.500  4.9  4.6  9.5  1.6  1.5  1.0  1.7  2.6  13.9
- [text] 5  0.735  2.0  5.3  7.3  2.2  0.9  0.8  1.5  2.5   8.9
- [text]
- [text] [5 rows x 29 columns]
+ [text] shape: (5, 29)
+ [text] ┌────────────────────────┬─────┬─────┬─────┬───┬─────┬─────┬─────┬──────┐
+ [text] │ Player                 ┆ Pos ┆ Age ┆ Tm  ┆ … ┆ BLK ┆ TOV ┆ PF  ┆ PTS  │
+ [text] │ ---                    ┆ --- ┆ --- ┆ --- ┆   ┆ --- ┆ --- ┆ --- ┆ ---  │
+ [text] │ str                    ┆ str ┆ i64 ┆ str ┆   ┆ f64 ┆ f64 ┆ f64 ┆ f64  │
+ [text] ╞════════════════════════╪═════╪═════╪═════╪═══╪═════╪═════╪═════╪══════╡
+ [text] │ Álex Abrines\abrinal01 ┆ SG  ┆ 25  ┆ OKC ┆ … ┆ 0.2 ┆ 0.5 ┆ 1.7 ┆ 5.3  │
+ [text] │ Quincy Acy\acyqu01     ┆ PF  ┆ 28  ┆ PHO ┆ … ┆ 0.4 ┆ 0.4 ┆ 2.4 ┆ 1.7  │
+ [text] │ Jaylen Adams\adamsja01 ┆ PG  ┆ 22  ┆ ATL ┆ … ┆ 0.1 ┆ 0.8 ┆ 1.3 ┆ 3.2  │
+ [text] │ Steven Adams\adamsst01 ┆ C   ┆ 25  ┆ OKC ┆ … ┆ 1.0 ┆ 1.7 ┆ 2.6 ┆ 13.9 │
+ [text] │ Bam Adebayo\adebaba01  ┆ C   ┆ 21  ┆ MIA ┆ … ┆ 0.8 ┆ 1.5 ┆ 2.5 ┆ 8.9  │
+ [text] └────────────────────────┴─────┴─────┴─────┴───┴─────┴─────┴─────┴──────┘
```

**Why:** Re-executed under Polars: box-drawing repr with an added dtype row, and no index column because C1 dropped `Rk` rather than hiding it in an index.
**Reader sees:** changed: the 1–5 rank labels down the left edge are gone. Both reprs elide middle columns, and every value shown is identical to the baseline's.

<a id="c7"></a>
### C7 · `nba.select(['FG', 'AST', '3PA', 'PTS']).head()` · output

committed output

```diff
- [text]     FG  AST  3PA   PTS
- [text] 1  1.8  0.6  4.1   5.3
- [text] 2  0.4  0.8  1.5   1.7
- [text] 3  1.1  1.9  2.2   3.2
- [text] 4  6.0  1.6  0.0  13.9
- [text] 5  3.4  2.2  0.2   8.9
+ [text] shape: (5, 4)
+ [text] ┌─────┬─────┬─────┬──────┐
+ [text] │ FG  ┆ AST ┆ 3PA ┆ PTS  │
+ [text] │ --- ┆ --- ┆ --- ┆ ---  │
+ [text] │ f64 ┆ f64 ┆ f64 ┆ f64  │
+ [text] ╞═════╪═════╪═════╪══════╡
+ [text] │ 1.8 ┆ 0.6 ┆ 4.1 ┆ 5.3  │
+ [text] │ 0.4 ┆ 0.8 ┆ 1.5 ┆ 1.7  │
+ [text] │ 1.1 ┆ 1.9 ┆ 2.2 ┆ 3.2  │
+ [text] │ 6.0 ┆ 1.6 ┆ 0.0 ┆ 13.9 │
+ [text] │ 3.4 ┆ 2.2 ┆ 0.2 ┆ 8.9  │
+ [text] └─────┴─────┴─────┴──────┘
```

**Why:** Same cell body under Polars' repr.
**Reader sees:** equivalent — same 5×4 values; the frame gains a shape line and a dtype row and loses the row labels.

