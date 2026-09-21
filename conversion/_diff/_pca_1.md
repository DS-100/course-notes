# _pca_1 — change report

`887a578b0a4b:content/_pca_1/pca_1.ipynb` → `content/_pca_1/pca_1.ipynb`

**Tier B · 9 changes:** output 6 · prose 1 · code 2

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

Tier B and almost nothing to it: three source lines and one committed output. The
only real edit is that `sns.load_dataset("mpg")` returns a *pandas* DataFrame, so this chapter carried
pandas with no pandas token for a scanner to find; it is now
`pl.from_pandas(sns.load_dataset("mpg")).drop_nulls()`, applied to the code cell and its dropdown
mirror in one pass. **The chapter is not in `myst.yml`'s TOC** — only `content/pca/pca.ipynb` is — so
none of this reaches a reader, and CONVERSIONS.md recommends deleting the `_`-prefixed archive
directories outright. Worth one look: the row count is unchanged at 392, which depends on
`pl.from_pandas` defaulting to `nan_to_null=True`; had that gone the other way the frame would have
silently kept all 398 rows and every gate would still be green.

## Needs review

- [C2](#c2) · cell 6 [markdown]

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C4](#c4) · `mpg = pl.from_pandas(sns.load_dataset("mpg")).drop_nulls()`
- [C5](#c5) · `px.histogram(mpg, x="displacement")`
- [C6](#c6) · `px.scatter(mpg, x="displacement", y="horsepower")`
- [C7](#c7) · `fig = px.scatter_3d(mpg, x="displacement", y="horsepower", z="weight",`
- [C8](#c8) · `fig = px.scatter_3d(mpg, x="displacement",`
- [C9](#c9) · `fig = px.scatter_3d(mpg, x="displacement",`

## Changes

<a id="c1"></a>
### C1 · cell 5 [code] · code

baseline L40 → branch L40

```diff
- import pandas as pd
+ import polars as pl
```

**Why:** The chapter's one library import. `pd` was **dead** here — it appeared once and was never used — so this removes a dead import and adds a needed one.
**Output:** same — import cell, no committed output.

<a id="c2"></a>
### C2 · cell 6 [markdown] · prose · **REVIEW**

baseline L50 → branch L50

```diff
- # mpg = sns.load_dataset("mpg").dropna()
+ # mpg = pl.from_pandas(sns.load_dataset("mpg")).drop_nulls()
```

**Why:** Dropdown mirror of the next code cell; classified `prose` only because the whole cell is markdown. `sns.load_dataset` hands back a pandas DataFrame, so the line was a pandas site no `pd.`/`import pandas` scan can find. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Verdict:** necessary

<a id="c3"></a>
### C3 · cell 7 [code] · code

baseline L57 → branch L57

```diff
- mpg = sns.load_dataset("mpg").dropna()
+ mpg = pl.from_pandas(sns.load_dataset("mpg")).drop_nulls()
```

**Why:** Code half of C2: `pl.from_pandas(...)` wraps the seaborn loader and `dropna()` → `drop_nulls()`.
**Output:** differs — Polars render; see C4. The row count is unchanged at 392, because `pl.from_pandas` defaults to `nan_to_null=True`, so the six NaN `horsepower` values arrive as nulls and `drop_nulls()` drops exactly the rows `dropna()` dropped. Verified live (polars 1.43.1): `(392, 9)` both ways.

<a id="c4"></a>
### C4 · `mpg = pl.from_pandas(sns.load_dataset("mpg")).drop_nulls()` · output

committed output

```diff
- [text]     mpg  cylinders  displacement  horsepower  weight  acceleration  \
- [text] 0  18.0          8         307.0       130.0    3504          12.0
- [text] 1  15.0          8         350.0       165.0    3693          11.5
- [text] 2  18.0          8         318.0       150.0    3436          11.0
- [text] 3  16.0          8         304.0       150.0    3433          12.0
- [text] 4  17.0          8         302.0       140.0    3449          10.5
- [text]
- [text]    model_year origin                       name
- [text] 0          70    usa  chevrolet chevelle malibu
- [text] 1          70    usa          buick skylark 320
- [text] 2          70    usa         plymouth satellite
- [text] 3          70    usa              amc rebel sst
- [text] 4          70    usa                ford torino
+ [text] shape: (5, 9)
+ [text] ┌──────┬───────────┬─────────────┬────────────┬───┬─────────────┬────────────┬────────┬────────────┐
+ [text] │ mpg  ┆ cylinders ┆ displacemen ┆ horsepower ┆ … ┆ acceleratio ┆ model_year ┆ origin ┆ name       │
+ [text] │ ---  ┆ ---       ┆ t           ┆ ---        ┆   ┆ n           ┆ ---        ┆ ---    ┆ ---        │
+ [text] │ f64  ┆ i64       ┆ ---         ┆ f64        ┆   ┆ ---         ┆ i64        ┆ str    ┆ str        │
+ [text] │      ┆           ┆ f64         ┆            ┆   ┆ f64         ┆            ┆        ┆            │
+ [text] ╞══════╪═══════════╪═════════════╪════════════╪═══╪═════════════╪════════════╪════════╪════════════╡
+ [text] │ 18.0 ┆ 8         ┆ 307.0       ┆ 130.0      ┆ … ┆ 12.0        ┆ 70         ┆ usa    ┆ chevrolet  │
+ [text] │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ chevelle   │
+ [text] │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ malibu     │
+ [text] │ 15.0 ┆ 8         ┆ 350.0       ┆ 165.0      ┆ … ┆ 11.5        ┆ 70         ┆ usa    ┆ buick      │
+ [text] │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ skylark    │
+ [text] │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ 320        │
+ [text] │ 18.0 ┆ 8         ┆ 318.0       ┆ 150.0      ┆ … ┆ 11.0        ┆ 70         ┆ usa    ┆ plymouth   │
+ [text] │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ satellite  │
+ [text] │ 16.0 ┆ 8         ┆ 304.0       ┆ 150.0      ┆ … ┆ 12.0        ┆ 70         ┆ usa    ┆ amc rebel  │
+ [text] │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ sst        │
+ [text] │ 17.0 ┆ 8         ┆ 302.0       ┆ 140.0      ┆ … ┆ 10.5        ┆ 70         ┆ usa    ┆ ford       │
+ [text] │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ torino     │
+ [text] └──────┴───────────┴─────────────┴────────────┴───┴─────────────┴────────────┴────────┴────────────┘
```

**Why:** The cell now returns a Polars DataFrame, so `.head()` renders Polars' box table — a `shape:` line, a dtype row, no index column, and the long `name` strings wrapped inside the cell.
**Reader sees:** equivalent — the same five cars, the same nine columns, the same values. No prose in the chapter mentions the index, a row count, `.loc`, or "the table above". The chapter's five plotly figures are pixel-identical to the baseline; their only JSON difference is plotly serialising axis-domain `0` as `0.0`.

<a id="c5"></a>
### C5 · `px.histogram(mpg, x="displacement")` · output

committed output

```diff
- [plotly] figure md5:ab8afc0d59
- [plotly] trace 0 histogram
+ [plotly] figure md5:35d30e84ee
+ [plotly] trace 0 histogram
```

**Why:** `mpg` comes from `pl.from_pandas(sns.load_dataset("mpg")).drop_nulls()` and goes straight to `px.histogram`; the decoded 392 `x` values are byte-identical to the baseline's. Only plotly's axis-domain serialization moved, `[0, 1]` -> `[0.0, 1.0]`.
**Reader sees:** equivalent. The chapter is not in the TOC, so it is never built either way.

<a id="c6"></a>
### C6 · `px.scatter(mpg, x="displacement", y="horsepower")` · output

committed output

```diff
- [plotly] figure md5:3db8377a21
- [plotly] trace 0 scatter
+ [plotly] figure md5:e18d0a4cea
+ [plotly] trace 0 scatter
```

**Why:** Same hand-off over the same 392 rows; `x` and `y` decode byte-identical. Layout re-serialization only.
**Reader sees:** equivalent.

<a id="c7"></a>
### C7 · `fig = px.scatter_3d(mpg, x="displacement", y="horsepower", z="weight",` · output

committed output

```diff
- [plotly] figure md5:420df07eac
- [plotly] trace 0 scatter3d
+ [plotly] figure md5:a71fb2d35c
+ [plotly] trace 0 scatter3d
```

**Why:** All three coordinate arrays are byte-identical to the baseline; `scene.domain` integers became floats.
**Reader sees:** equivalent.

<a id="c8"></a>
### C8 · `fig = px.scatter_3d(mpg, x="displacement",` · output

committed output

```diff
- [plotly] figure md5:f465d7f7ff
- [plotly] trace 0 scatter3d
+ [plotly] figure md5:a4f3064e96
+ [plotly] trace 0 scatter3d
```

**Why:** As C7, with the `model_year` colour axis whose colorscale stops re-serialized the same way. No coordinate and no colour value changed.
**Reader sees:** equivalent.

<a id="c9"></a>
### C9 · `fig = px.scatter_3d(mpg, x="displacement",` · output

committed output

```diff
- [plotly] figure md5:5141f07c79
- [plotly] trace 0 scatter3d name='usa'
- [plotly] trace 1 scatter3d name='japan'
- [plotly] trace 2 scatter3d name='europe'
+ [plotly] figure md5:5049f00008
+ [plotly] trace 0 scatter3d name='usa'
+ [plotly] trace 1 scatter3d name='japan'
+ [plotly] trace 2 scatter3d name='europe'
```

**Why:** Three origin traces in the same order with the same memberships and byte-identical coordinates; layout float formatting only.
**Reader sees:** equivalent.

