# sampling — change report

`887a578b0a4b:content/sampling/sampling.ipynb` → `content/sampling/sampling.ipynb`

**Tier B · 36 changes:** output 11 · prose 4 · tab-twins 8 · code 11 · metadata 2

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

Mechanical in its code — `.iloc[idx]` becomes `.gather(idx)`, in-place column assignment becomes `with_columns`, and eight cells were hidden and re-published as synced Polars/pandas tab pairs. Two of CONTRADICTIONS §A6's three pre-existing errors are fixed here: the off-by-one `high=n_votes-1` (C7, C9) and `polls` → `poll` (C15, C16). Three things for staff. C6 adds new pedagogical content the conversion did not require — a correct claim (verified: one repeated voter in 89.5 samples) but a new one staff now own. C7 changes every simulated number downstream. And C32–C35 are the only place in this batch where the reader loses information: Polars elides middle columns that pandas printed in full.

## Needs review

- [C5](#c5) · cell 14 [markdown]
- [C6](#c6) · cell 14 [markdown]
- [C15](#c15) · cell 30: 🥞 Post-stratification with Literary Digest responses from 19
- [C16](#c16) · cell 30: 🥞 Post-stratification with Literary Digest responses from 19

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C26](#c26) · `with zipfile.ZipFile("data/1936_votes.zip", 'r') as z:`
- [C27](#c27) · `votes['voted_dem'].sample(1000).mean()`
- [C28](#c28) · `rng = np.random.default_rng()`
- [C29](#c29) · `for _ in range(10):`
- [C30](#c30) · `nrep = 10000   # number of simulations`
- [C31](#c31) · `plt.figure(figsize=(12, 3))`
- [C32](#c32) · `poll = pl.read_csv('data/literary-digest-summary-data.csv')`
- [C33](#c33) · `poll = poll.with_columns(`
- [C34](#c34) · `poll = poll.with_columns(`
- [C35](#c35) · `poll = poll.with_columns(`
- [C36](#c36) · `poll = poll.with_columns(`

## Changes

<a id="c1"></a>
### C1 · cell 3 [code] · code

baseline L224 → branch L224

```diff
- import pandas as pd
+ import polars as pl
```

**Why:** Import rename.
**Output:** same.

<a id="c2"></a>
### C2 · cell 4 [code] · metadata

baseline L231 → branch L231

```diff
- # %%
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c3"></a>
### C3 · cell 4 [code] · code

baseline L234 → branch L234

```diff
-         votes = pd.read_csv(csv_file)
+         votes = pl.read_csv(csv_file)
```

**Why:** `pl.read_csv` reads the same zip member handle; no other argument was needed.
**Output:** same 44,430,549 rows (verified); the head repr changes (C26).

<a id="c4"></a>
### C4 · cell 4 [code] · tab-twins

baseline L237 → branch L237 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 85fabb88 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # with zipfile.ZipFile("data/1936_votes.zip", 'r') as z:
+ #     with z.open("1936_votes.csv") as csv_file:
+ #         votes = pl.read_csv(csv_file)
+ #
+ # votes.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 1)
+ # ┌───────────┐
+ # │ voted_dem │
+ # │ ---       │
+ # │ i64       │
+ # ╞═══════════╡
+ # │ 1         │
+ # │ 1         │
+ # │ 0         │
+ # │ 1         │
+ # │ 1         │
+ # └───────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # with zipfile.ZipFile("data/1936_votes.zip", 'r') as z:
+ #     with z.open("1936_votes.csv") as csv_file:
+ #         votes = pd.read_csv(csv_file)
+ #
+ # votes.head()
+ # ```
+ #
+ … 11 more lines
```

**Why:** The cell was hidden (`remove-input`, `remove-output`) and its output re-published as a synced Polars/pandas tab pair, so the reader can compare the two `read_csv` idioms rather than seeing only the converted one.
**Output:** differs by repr only — same five values (C26).

<a id="c5"></a>
### C5 · cell 14 [markdown] · prose · **REVIEW**

baseline L274 → branch L325

```diff
- # Note that the cell above is a little slow, since we're sampling from a `DataFrame` with almost 45 million rows.
+ # We can also pick the row positions ourselves. `NumPy` draws 1,000 random row numbers and `.gather` pulls out the values sitting at those positions. This is the form we'll reuse below when we repeat the sample thousands of times.
```

**Why:** The baseline motivated the NumPy loop by calling `.sample()` “a little slow” on 45 million rows and offering NumPy as the speed-up. The replacement instead says what the code does: `rng.integers` picks the positions and `.gather` takes the values at them, `.gather` being the Polars form of `.iloc[idx]` (C8).
**Verdict:** optional — the conversion required renaming `.iloc` to `.gather`, not re-authoring the paragraph. Timing was not re-measured, so whether the original speed claim still holds under Polars is unverified.
**Minimal alternative:** “We can also pick the row positions ourselves with `NumPy`:” in place of the two baseline sentences, leaving the rest of the section as it was.

<a id="c6"></a>
### C6 · cell 14 [markdown] · prose · **REVIEW**

baseline L276 → branch L327

```diff
- # We can speed up the sampling using `NumPy`:
+ # Note that this is *not* an SRS. `rng.integers` draws each number independently, so the same voter can come up twice — it is the uniform random sample **with** replacement from earlier in the chapter. With 1,000 draws from 44 million voters a repeat turns up in roughly one sample in ninety, which is why the two schemes give such similar answers here.
```

**Why:** Adds the observation that `rng.integers` draws independently and so samples *with* replacement, making this not an SRS — which the baseline's “we can speed up the sampling” framing implied it was. The arithmetic checks out: with 44,430,549 voters, 1,000 draws repeat a voter with probability 0.0112, or one sample in 89.5 (verified).
**Verdict:** questionable — it does correct an implied equivalence, but it is new course content, it is not one of CONTRADICTIONS §A6's three entries, and the “one in ninety” figure is a claim staff now own.
**Minimal alternative:** one sentence — “Note that `rng.integers` samples *with* replacement, so this is the uniform random sample rather than an SRS” — and drop the birthday-problem estimate.

<a id="c7"></a>
### C7 · cell 15 [code] · code

baseline L286 → branch L337

```diff
- idx = rng.integers(low=0, high=n_votes-1, size=1000)
+ idx = rng.integers(low=0, high=n_votes, size=1000)
```

**Why:** `numpy.random.Generator.integers` is half-open on `high`, so `high=n_votes-1` excluded the last voter — the comment above it named exactly the index the call left out, and the sibling cell already used `high=n_votes`. CONTRADICTIONS §A6 #2 — pre-existing.
**Output:** differs: the printed value is a new draw either way (the RNG is unseeded), and the sampled population is now the full 44,430,549 rather than all but the last row.

<a id="c8"></a>
### C8 · cell 15 [code] · code

baseline L288 → branch L339

```diff
- votes['voted_dem'].iloc[idx].mean()
+ votes['voted_dem'].gather(idx).mean()
```

**Why:** `.iloc[idx]` → `.gather(idx)`. Polars addresses rows by position only, and `gather` is the positional take on a Series.
**Output:** differs only as a new random draw — the RNG is unseeded on both sides, so this number was never reproducible (C27, C28).

<a id="c9"></a>
### C9 · cell 17 [code] · code

baseline L297 → branch L348

```diff
-   idx = rng.integers(low=0, high=n_votes-1, size=1000)
-   print(votes['voted_dem'].iloc[idx].mean())
+   idx = rng.integers(low=0, high=n_votes, size=1000)
+   print(votes['voted_dem'].gather(idx).mean())
```

**Why:** Same two changes as C7 and C8, inside the ten-iteration demo loop.
**Output:** differs: ten new draws (C29).

<a id="c10"></a>
### C10 · cell 19 [code] · metadata

baseline L303 → branch L354

```diff
- # %%
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c11"></a>
### C11 · cell 19 [code] · code

baseline L310 → branch L361

```diff
-     results.append(votes['voted_dem'].iloc[idx].mean())
+     results.append(votes['voted_dem'].gather(idx).mean())
```

**Why:** Same `.iloc` → `.gather` rename inside the 10,000-iteration simulation loop.
**Output:** differs: the simulation is re-run, so all 10,000 values are new (C30, C31).

<a id="c12"></a>
### C12 · cell 19 [code] · tab-twins

baseline L314 → branch L365 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin ba3f14e4 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # nrep = 10000   # number of simulations
+ # n = 1000       # size of our sample
+ # results = []   # list to store the sampling results
+ #
+ # for i in range(0, nrep):
+ #     idx = rng.integers(low=0, high=n_votes, size=1000)
+ #     results.append(votes['voted_dem'].gather(idx).mean())
+ #
+ # # First 10 simulated sample proportions
+ # results[:10]
+ # ```
+ #
+ # ```text
+ # [0.631, 0.627, 0.63, 0.62, 0.651, 0.622, 0.617, 0.604, 0.604, 0.601]
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # nrep = 10000   # number of simulations
+ # n = 1000       # size of our sample
+ # results = []   # list to store the sampling results
+ #
+ # for i in range(0, nrep):
+ #     idx = rng.integers(low=0, high=n_votes, size=1000)
+ #     results.append(votes['voted_dem'].iloc[idx].mean())
+ #
+ # # First 10 simulated sample proportions
+ # results[:10]
+ # ```
+ #
+ # ```text
+ … 5 more lines
```

**Why:** Tab pair for the simulation cell; the Polars tab carries the newly executed output and the pandas tab the baseline's.
**Output:** differs: both tabs show ten draws from the same distribution, from different runs.

<a id="c13"></a>
### C13 · cell 24 [code] · code

baseline L355 → branch L451

```diff
- # %%
- poll = pd.read_csv('data/literary-digest-summary-data.csv')
+ # %% tags=["remove-input", "remove-output"]
+ poll = pl.read_csv('data/literary-digest-summary-data.csv')
```

**Why:** `pl.read_csv`, and the cell hidden for the tab pair below it.
**Output:** differs: Polars repr, and the head no longer prints all ten columns — see C32.

<a id="c14"></a>
### C14 · cell 24 [code] · tab-twins

baseline L358 → branch L454 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin cc6b2fcf -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # poll = pl.read_csv('data/literary-digest-summary-data.csv')
+ # poll.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 10)
+ # ┌───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬──────────┐
+ # │ state     ┆ electoral ┆ actual_de ┆ actual_re ┆ … ┆ actual_de ┆ actual_re ┆ ld_dem_19 ┆ ld_rep_1 │
+ # │ ---       ┆ _votes    ┆ m_1936    ┆ p_1936    ┆   ┆ m_1932    ┆ p_1932    ┆ 32        ┆ 932      │
+ # │ str       ┆ ---       ┆ ---       ┆ ---       ┆   ┆ ---       ┆ ---       ┆ ---       ┆ ---      │
+ # │           ┆ i64       ┆ i64       ┆ i64       ┆   ┆ i64       ┆ i64       ┆ i64       ┆ i64      │
+ # ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪══════════╡
+ # │ Alabama   ┆ 11        ┆ 238196    ┆ 35358     ┆ … ┆ 207910    ┆ 34675     ┆ 9828      ┆ 1589     │
+ # │ Arizona   ┆ 3         ┆ 86722     ┆ 33433     ┆ … ┆ 79264     ┆ 36104     ┆ 2202      ┆ 1679     │
+ # │ Arkansas  ┆ 9         ┆ 146765    ┆ 32049     ┆ … ┆ 189602    ┆ 28467     ┆ 7608      ┆ 1566     │
+ # │ Californi ┆ 22        ┆ 1766836   ┆ 836431    ┆ … ┆ 1324157   ┆ 847902    ┆ 69720     ┆ 80525    │
+ # │ a         ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆          │
+ # │ Colorado  ┆ 6         ┆ 295021    ┆ 181267    ┆ … ┆ 250877    ┆ 189617    ┆ 9970      ┆ 13619    │
+ # └───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴──────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # poll = pd.read_csv('data/literary-digest-summary-data.csv')
+ # poll.head()
+ # ```
+ #
+ # ```text
+ #         state  electoral_votes  actual_dem_1936  actual_rep_1936  ld_rep_1936  \
+ # 0     Alabama               11           238196            35358         3060
+ # 1     Arizona                3            86722            33433         2337
+ … 14 more lines
```

**Why:** Tab pair for the Literary Digest load.
**Output:** differs: the Polars tab elides middle columns where the pandas tab wraps and shows all ten.

<a id="c15"></a>
### C15 · cell 30: 🥞 Post-stratification with Literary Digest responses from 19 · prose · **REVIEW**

baseline L408 → branch L558

```diff
- # The population cells are already in `polls`: `actual_dem_1932` and `actual_rep_1932` provide the actual vote counts for each party and state in 1932.
+ # The population cells are already in `poll`: `actual_dem_1932` and `actual_rep_1932` provide the actual vote counts for each party and state in 1932.
```

**Why:** The frame is bound as `poll` and called `poll` in all eleven code cells; a reader typing `polls` gets a `NameError`. CONTRADICTIONS §A6 #1 — pre-existing.
**Verdict:** necessary — a fix to a false claim (a name that does not exist).

<a id="c16"></a>
### C16 · cell 30: 🥞 Post-stratification with Literary Digest responses from 19 · prose · **REVIEW**

baseline L410 → branch L560

```diff
- # The sample cells are also in `polls`: `ld_dem_1932` and `ld_rep_1932` provide the number of responses to the 1932 Literary Digest poll, among 1936 poll respondents, for each party.
+ # The sample cells are also in `poll`: `ld_dem_1932` and `ld_rep_1932` provide the number of responses to the 1932 Literary Digest poll, among 1936 poll respondents, for each party.
```

**Why:** The second half of the same `polls` → `poll` fix. CONTRADICTIONS §A6 #1 — pre-existing.
**Verdict:** necessary — a fix to a false claim.

<a id="c17"></a>
### C17 · cell 31 [code] · code

baseline L420 → branch L570

```diff
- # %%
- poll['dem_reweight_factor'] = poll['actual_dem_1932'] / poll['ld_dem_1932']
- poll['rep_reweight_factor'] = poll['actual_rep_1932'] / poll['ld_rep_1932']
+ # %% tags=["remove-input", "remove-output"]
+ poll = poll.with_columns(
+     (pl.col('actual_dem_1932') / pl.col('ld_dem_1932')).alias('dem_reweight_factor'),
+     (pl.col('actual_rep_1932') / pl.col('ld_rep_1932')).alias('rep_reweight_factor'),
+ )
```

**Why:** Two `poll[col] = ...` assignments become one `with_columns` with `alias`; Polars frames are immutable, so the frame is rebound rather than mutated.
**Output:** same reweight factors (verified).

<a id="c18"></a>
### C18 · cell 31 [code] · tab-twins

baseline L424 → branch L576 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 270e983e -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # poll = poll.with_columns(
+ #     (pl.col('actual_dem_1932') / pl.col('ld_dem_1932')).alias('dem_reweight_factor'),
+ #     (pl.col('actual_rep_1932') / pl.col('ld_rep_1932')).alias('rep_reweight_factor'),
+ # )
+ # poll.tail()
+ # ```
+ #
+ # ```text
+ # shape: (5, 12)
+ # ┌───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬──────────┐
+ # │ state     ┆ electoral ┆ actual_de ┆ actual_re ┆ … ┆ ld_dem_19 ┆ ld_rep_19 ┆ dem_rewei ┆ rep_rewe │
+ # │ ---       ┆ _votes    ┆ m_1936    ┆ p_1936    ┆   ┆ 32        ┆ 32        ┆ ght_facto ┆ ight_fac │
+ # │ str       ┆ ---       ┆ ---       ┆ ---       ┆   ┆ ---       ┆ ---       ┆ r         ┆ tor      │
+ # │           ┆ i64       ┆ i64       ┆ i64       ┆   ┆ i64       ┆ i64       ┆ ---       ┆ ---      │
+ # │           ┆           ┆           ┆           ┆   ┆           ┆           ┆ f64       ┆ f64      │
+ # ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪══════════╡
+ # │ Virginia  ┆ 11        ┆ 234980    ┆ 98336     ┆ … ┆ 16194     ┆ 6817      ┆ 12.595961 ┆ 13.14903 │
+ # │           ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆ 9        │
+ # │ Washingto ┆ 8         ┆ 459579    ┆ 206892    ┆ … ┆ 16223     ┆ 17122     ┆ 21.775257 ┆ 12.18578 │
+ # │ n         ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆ 4        │
+ # │ West      ┆ 8         ┆ 502582    ┆ 325358    ┆ … ┆ 10818     ┆ 11338     ┆ 37.449066 ┆ 29.17013 │
+ # │ Virginia  ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆ 6        │
+ # │ Wisconsin ┆ 12        ┆ 802984    ┆ 380828    ┆ … ┆ 24073     ┆ 25731     ┆ 29.386034 ┆ 13.51447 │
+ # │           ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆ 7        │
+ # │ Wyoming   ┆ 3         ┆ 62624     ┆ 38739     ┆ … ┆ 1654      ┆ 2072      ┆ 32.871826 ┆ 19.10376 │
+ # │           ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆ 4        │
+ # └───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴──────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ … 30 more lines
```

**Why:** Tab pair for the reweight-factor cell.
**Output:** differs by repr only — same factors; the Polars tab wraps long values onto continuation rows where pandas wrapped by column block.

<a id="c19"></a>
### C19 · cell 34 [code] · code

baseline L440 → branch L662

```diff
- # %%
- poll['pred_dem_1936'] = round(poll['ld_dem_1936'] * poll['dem_reweight_factor'])
- poll['pred_rep_1936'] = round(poll['ld_rep_1936'] * poll['rep_reweight_factor'])
+ # %% tags=["remove-input", "remove-output"]
+ poll = poll.with_columns(
+     (pl.col('ld_dem_1936') * pl.col('dem_reweight_factor')).round().alias('pred_dem_1936'),
+     (pl.col('ld_rep_1936') * pl.col('rep_reweight_factor')).round().alias('pred_rep_1936'),
+ )
```

**Why:** Same in-place-to-`with_columns` move, and the built-in `round(Series)` becomes `.round()` on the expression.
**Output:** same predicted counts (verified).

<a id="c20"></a>
### C20 · cell 34 [code] · tab-twins

baseline L444 → branch L668 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 2ffa1838 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # poll = poll.with_columns(
+ #     (pl.col('ld_dem_1936') * pl.col('dem_reweight_factor')).round().alias('pred_dem_1936'),
+ #     (pl.col('ld_rep_1936') * pl.col('rep_reweight_factor')).round().alias('pred_rep_1936'),
+ # )
+ # poll.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 14)
+ # ┌───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬──────────┐
+ # │ state     ┆ electoral ┆ actual_de ┆ actual_re ┆ … ┆ dem_rewei ┆ rep_rewei ┆ pred_dem_ ┆ pred_rep │
+ # │ ---       ┆ _votes    ┆ m_1936    ┆ p_1936    ┆   ┆ ght_facto ┆ ght_facto ┆ 1936      ┆ _1936    │
+ # │ str       ┆ ---       ┆ ---       ┆ ---       ┆   ┆ r         ┆ r         ┆ ---       ┆ ---      │
+ # │           ┆ i64       ┆ i64       ┆ i64       ┆   ┆ ---       ┆ ---       ┆ f64       ┆ f64      │
+ # │           ┆           ┆           ┆           ┆   ┆ f64       ┆ f64       ┆           ┆          │
+ # ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪══════════╡
+ # │ Alabama   ┆ 11        ┆ 238196    ┆ 35358     ┆ … ┆ 21.154864 ┆ 21.821901 ┆ 213283.0  ┆ 66775.0  │
+ # │ Arizona   ┆ 3         ┆ 86722     ┆ 33433     ┆ … ┆ 35.996367 ┆ 21.503276 ┆ 71093.0   ┆ 50253.0  │
+ # │ Arkansas  ┆ 9         ┆ 146765    ┆ 32049     ┆ … ┆ 24.921399 ┆ 18.178161 ┆ 189602.0  ┆ 49517.0  │
+ # │ Californi ┆ 22        ┆ 1766836   ┆ 836431    ┆ … ┆ 18.992499 ┆ 10.529674 ┆ 1.467076e ┆ 942574.0 │
+ # │ a         ┆           ┆           ┆           ┆   ┆           ┆           ┆ 6         ┆          │
+ # │ Colorado  ┆ 6         ┆ 295021    ┆ 181267    ┆ … ┆ 25.16319  ┆ 13.922975 ┆ 252261.0  ┆ 222058.0 │
+ # └───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴──────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # poll['pred_dem_1936'] = round(poll['ld_dem_1936'] * poll['dem_reweight_factor'])
+ # poll['pred_rep_1936'] = round(poll['ld_rep_1936'] * poll['rep_reweight_factor'])
+ # poll.head()
+ # ```
+ … 26 more lines
```

**Why:** Tab pair for the prediction cell.
**Output:** differs by repr only — same values; `1467076.0` prints as `1.467076e6` under Polars.

<a id="c21"></a>
### C21 · cell 39 [code] · code

baseline L468 → branch L758

```diff
- # %%
- poll['pred_total_1936'] = poll['pred_dem_1936'] + poll['pred_rep_1936']
- poll['actual_total_1932'] = poll['actual_dem_1932'] + poll['actual_rep_1932']
- poll['correction_factor'] = poll['actual_total_1932'] / poll['pred_total_1936']
+ # %% tags=["remove-input", "remove-output"]
+ poll = poll.with_columns(
+     (pl.col('pred_dem_1936') + pl.col('pred_rep_1936')).alias('pred_total_1936'),
+     (pl.col('actual_dem_1932') + pl.col('actual_rep_1932')).alias('actual_total_1932'),
+ ).with_columns(
+     (pl.col('actual_total_1932') / pl.col('pred_total_1936')).alias('correction_factor')
+ )
```

**Why:** Same move, but it needs two chained `with_columns` calls: `correction_factor` reads `pred_total_1936` and `actual_total_1932`, and expressions inside a single `with_columns` cannot see columns created in that same call.
**Output:** same correction factors (verified).

<a id="c22"></a>
### C22 · cell 40 [markdown] · tab-twins

baseline L474 → branch L767 · spans code and prose

```diff
- # %%
- poll['pred_dem_1936_corrected'] = poll['pred_dem_1936'] * poll['correction_factor']
- poll['pred_rep_1936_corrected'] = poll['pred_rep_1936'] * poll['correction_factor']
+ # %% [markdown]
+ # <!-- tab-twins:begin 1df8f9d3 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # poll = poll.with_columns(
+ #     (pl.col('pred_dem_1936') + pl.col('pred_rep_1936')).alias('pred_total_1936'),
+ #     (pl.col('actual_dem_1932') + pl.col('actual_rep_1932')).alias('actual_total_1932'),
+ # ).with_columns(
+ #     (pl.col('actual_total_1932') / pl.col('pred_total_1936')).alias('correction_factor')
+ # )
+ # poll.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 17)
+ # ┌───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬──────────┐
+ # │ state     ┆ electoral ┆ actual_de ┆ actual_re ┆ … ┆ pred_rep_ ┆ pred_tota ┆ actual_to ┆ correcti │
+ # │ ---       ┆ _votes    ┆ m_1936    ┆ p_1936    ┆   ┆ 1936      ┆ l_1936    ┆ tal_1932  ┆ on_facto │
+ # │ str       ┆ ---       ┆ ---       ┆ ---       ┆   ┆ ---       ┆ ---       ┆ ---       ┆ r        │
+ # │           ┆ i64       ┆ i64       ┆ i64       ┆   ┆ f64       ┆ f64       ┆ i64       ┆ ---      │
+ # │           ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆ f64      │
+ # ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪══════════╡
+ # │ Alabama   ┆ 11        ┆ 238196    ┆ 35358     ┆ … ┆ 66775.0   ┆ 280058.0  ┆ 242585    ┆ 0.866196 │
+ # │ Arizona   ┆ 3         ┆ 86722     ┆ 33433     ┆ … ┆ 50253.0   ┆ 121346.0  ┆ 115368    ┆ 0.950736 │
+ # │ Arkansas  ┆ 9         ┆ 146765    ┆ 32049     ┆ … ┆ 49517.0   ┆ 239119.0  ┆ 218069    ┆ 0.911969 │
+ # │ Californi ┆ 22        ┆ 1766836   ┆ 836431    ┆ … ┆ 942574.0  ┆ 2.40965e6 ┆ 2172059   ┆ 0.9014   │
+ # │ a         ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆          │
+ # │ Colorado  ┆ 6         ┆ 295021    ┆ 181267    ┆ … ┆ 222058.0  ┆ 474319.0  ┆ 440494    ┆ 0.928687 │
+ # └───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴──────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # poll['pred_total_1936'] = poll['pred_dem_1936'] + poll['pred_rep_1936']
+ # poll['actual_total_1932'] = poll['actual_dem_1932'] + poll['actual_rep_1932']
+ # poll['correction_factor'] = poll['actual_total_1932'] / poll['pred_total_1936']
+ … 41 more lines
```

**Why:** Tab pair for the correction-factor cell.
**Output:** differs by repr only — same values.

<a id="c23"></a>
### C23 · cell 41 [code] · tab-twins

baseline L479 → branch L850 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin a950633d -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # poll = poll.with_columns(
+ #     (pl.col('pred_dem_1936') * pl.col('correction_factor')).alias('pred_dem_1936_corrected'),
+ #     (pl.col('pred_rep_1936') * pl.col('correction_factor')).alias('pred_rep_1936_corrected'),
+ # )
+ #
+ # poll['pred_dem_1936_corrected'].sum() / (poll['pred_dem_1936_corrected'].sum() + poll['pred_rep_1936_corrected'].sum())
+ # ```
+ #
+ # ```text
+ # 0.5419440974611632
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # poll['pred_dem_1936_corrected'] = poll['pred_dem_1936'] * poll['correction_factor']
+ # poll['pred_rep_1936_corrected'] = poll['pred_rep_1936'] * poll['correction_factor']
+ #
+ # poll['pred_dem_1936_corrected'].sum() / (poll['pred_dem_1936_corrected'].sum() + poll['pred_rep_1936_corrected'].sum())
+ # ```
+ #
+ # ```text
+ # 0.5419440974611633
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** Tab pair for the corrected-prediction cell.
**Output:** differs in the last unit in the last place of the printed proportion — see C36.

<a id="c24"></a>
### C24 · cell 46 [code] · code

baseline L500 → branch L906

```diff
- # %%
- poll['dem_wins'] = poll['pred_dem_1936'] > poll['pred_rep_1936']
+ # %% tags=["remove-input", "remove-output"]
+ poll = poll.with_columns((pl.col('pred_dem_1936') > pl.col('pred_rep_1936')).alias('dem_wins'))
```

**Why:** `poll[col] = ...` → `with_columns` with `alias` for the boolean column.
**Output:** same.

<a id="c25"></a>
### C25 · cell 46 [code] · tab-twins

baseline L507 → branch L913 · spans code and prose

```diff
- print(( (1-poll['dem_wins']) * poll['electoral_votes'] ).sum())
+ print(( (~poll['dem_wins']) * poll['electoral_votes'] ).sum())
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin a4c9e44f -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # poll = poll.with_columns((pl.col('pred_dem_1936') > pl.col('pred_rep_1936')).alias('dem_wins'))
+ #
+ # print('Total predicted Roosevelt electoral votes:')
+ # print(( poll['dem_wins'] * poll['electoral_votes'] ).sum())
+ #
+ # print('Total predicted Landon electoral votes:')
+ # print(( (~poll['dem_wins']) * poll['electoral_votes'] ).sum())
+ # ```
+ #
+ # ```text
+ # Total predicted Roosevelt electoral votes:
+ # 380
+ # Total predicted Landon electoral votes:
+ # 151
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # poll['dem_wins'] = poll['pred_dem_1936'] > poll['pred_rep_1936']
+ #
+ # print('Total predicted Roosevelt electoral votes:')
+ # print(( poll['dem_wins'] * poll['electoral_votes'] ).sum())
+ #
+ # print('Total predicted Landon electoral votes:')
+ # print(( (1-poll['dem_wins']) * poll['electoral_votes'] ).sum())
+ # ```
+ #
+ # ```text
+ # Total predicted Roosevelt electoral votes:
+ # 380
+ … 6 more lines
```

**Why:** `1 - poll['dem_wins']` raises in Polars — verified: `cannot do arithmetic with Series of dtype: Boolean and argument of type: 'bool'` — so the negation is written as `~`. `~bool * int` then multiplies as expected.
**Output:** same — 380 and 151 electoral votes on both sides (verified).

<a id="c26"></a>
### C26 · `with zipfile.ZipFile("data/1936_votes.zip", 'r') as z:` · output

committed output

```diff
- [text]    voted_dem
- [text] 0          1
- [text] 1          1
- [text] 2          0
- [text] 3          1
- [text] 4          1
+ [text] shape: (5, 1)
+ [text] ┌───────────┐
+ [text] │ voted_dem │
+ [text] │ ---       │
+ [text] │ i64       │
+ [text] ╞═══════════╡
+ [text] │ 1         │
+ [text] │ 1         │
+ [text] │ 0         │
+ [text] │ 1         │
+ [text] │ 1         │
+ [text] └───────────┘
```

**Why:** Polars repr for the votes head.
**Reader sees:** equivalent — same five values plus a dtype row; the 0–4 row labels are gone.

<a id="c27"></a>
### C27 · `votes['voted_dem'].sample(1000).mean()` · output

committed output

```diff
- [text] 0.626
+ [text] 0.633
```

**Why:** The RNG is unseeded in both versions, so this is a new draw from the same population; `.sample(1000)` is without replacement on both sides.
**Reader sees:** equivalent — 0.626 → 0.633, both ordinary draws around the population's 0.6246.

<a id="c28"></a>
### C28 · `rng = np.random.default_rng()` · output

committed output

```diff
- [text] 0.627
+ [text] 0.615
```

**Why:** New draw, and now over the full population after C7's off-by-one fix.
**Reader sees:** equivalent — 0.627 → 0.615, within the sampling spread the next cell goes on to illustrate.

<a id="c29"></a>
### C29 · `for _ in range(10):` · output

committed output

```diff
- [stdout] 0.637
- [stdout] 0.626
- [stdout] 0.602
- [stdout] 0.621
- [stdout] 0.65
- [stdout] 0.633
- [stdout] 0.621
- [stdout] 0.618
- [stdout] 0.627
- [stdout] 0.622
+ [stdout] 0.604
+ [stdout] 0.612
+ [stdout] 0.623
+ [stdout] 0.627
+ [stdout] 0.649
+ [stdout] 0.606
+ [stdout] 0.622
+ [stdout] 0.611
+ [stdout] 0.617
+ [stdout] 0.625
```

**Why:** Ten new unseeded draws from the loop in C9.
**Reader sees:** equivalent — same 0.60–0.65 band, same point: repeated samples wobble around the truth.

<a id="c30"></a>
### C30 · `nrep = 10000   # number of simulations` · output

committed output

```diff
- [text] [0.646, 0.632, 0.627, 0.618, 0.619, 0.64, 0.645, 0.643, 0.636, 0.627]
+ [text] [0.631, 0.627, 0.63, 0.62, 0.651, 0.622, 0.617, 0.604, 0.604, 0.601]
```

**Why:** The 10,000-iteration simulation was re-run; the first ten values are new draws.
**Reader sees:** equivalent.

<a id="c31"></a>
### C31 · `plt.figure(figsize=(12, 3))` · output

committed output

```diff
- [text] <Figure size 1200x300 with 1 Axes>
- [image/png] 36788 bytes md5:e738e92178
+ [text] <Figure size 1200x300 with 1 Axes>
+ [image/png] 35940 bytes md5:a9d701786a
```

**Why:** Histogram of the 10,000 fresh simulated proportions.
**Reader sees:** equivalent — pixel-diffed, 17.9% of pixels differ, all of it bar heights and the KDE; the centre and spread are unchanged.

<a id="c32"></a>
### C32 · `poll = pl.read_csv('data/literary-digest-summary-data.csv')` · output

committed output

```diff
- [text]         state  electoral_votes  actual_dem_1936  actual_rep_1936  ld_rep_1936  \
- [text] 0     Alabama               11           238196            35358         3060
- [text] 1     Arizona                3            86722            33433         2337
- [text] 2    Arkansas                9           146765            32049         2724
- [text] 3  California               22          1766836           836431        89516
- [text] 4    Colorado                6           295021           181267        15949
- [text]
- [text]    ld_dem_1936  actual_dem_1932  actual_rep_1932  ld_dem_1932  ld_rep_1932
- [text] 0        10082           207910            34675         9828         1589
- [text] 1         1975            79264            36104         2202         1679
- [text] 2         7608           189602            28467         7608         1566
- [text] 3        77245          1324157           847902        69720        80525
- [text] 4        10025           250877           189617         9970        13619
+ [text] shape: (5, 10)
+ [text] ┌───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬──────────┐
+ [text] │ state     ┆ electoral ┆ actual_de ┆ actual_re ┆ … ┆ actual_de ┆ actual_re ┆ ld_dem_19 ┆ ld_rep_1 │
+ [text] │ ---       ┆ _votes    ┆ m_1936    ┆ p_1936    ┆   ┆ m_1932    ┆ p_1932    ┆ 32        ┆ 932      │
+ [text] │ str       ┆ ---       ┆ ---       ┆ ---       ┆   ┆ ---       ┆ ---       ┆ ---       ┆ ---      │
+ [text] │           ┆ i64       ┆ i64       ┆ i64       ┆   ┆ i64       ┆ i64       ┆ i64       ┆ i64      │
+ [text] ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪══════════╡
+ [text] │ Alabama   ┆ 11        ┆ 238196    ┆ 35358     ┆ … ┆ 207910    ┆ 34675     ┆ 9828      ┆ 1589     │
+ [text] │ Arizona   ┆ 3         ┆ 86722     ┆ 33433     ┆ … ┆ 79264     ┆ 36104     ┆ 2202      ┆ 1679     │
+ [text] │ Arkansas  ┆ 9         ┆ 146765    ┆ 32049     ┆ … ┆ 189602    ┆ 28467     ┆ 7608      ┆ 1566     │
+ [text] │ Californi ┆ 22        ┆ 1766836   ┆ 836431    ┆ … ┆ 1324157   ┆ 847902    ┆ 69720     ┆ 80525    │
+ [text] │ a         ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆          │
+ [text] │ Colorado  ┆ 6         ┆ 295021    ┆ 181267    ┆ … ┆ 250877    ┆ 189617    ┆ 9970      ┆ 13619    │
+ [text] └───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴──────────┘
```

**Why:** Polars repr. pandas wrapped all ten columns across two blocks; Polars prints four columns, an ellipsis, then four.
**Reader sees:** changed: `ld_rep_1936` and `ld_dem_1936` — the poll counts the rest of the section works with — are no longer visible in the head. `pl.Config.set_tbl_cols(-1)` would restore parity if staff want it.

<a id="c33"></a>
### C33 · `poll = poll.with_columns(` · output

committed output

```diff
- [text]             state  electoral_votes  actual_dem_1936  actual_rep_1936  \
- [text] 43       Virginia               11           234980            98336
- [text] 44     Washington                8           459579           206892
- [text] 45  West Virginia                8           502582           325358
- [text] 46      Wisconsin               12           802984           380828
- [text] 47        Wyoming                3            62624            38739
- [text]
- [text]     ld_rep_1936  ld_dem_1936  actual_dem_1932  actual_rep_1932  ld_dem_1932  \
- [text] 43        10223        16783           203979            89637        16194
- [text] 44        21370        15300           353260           208645        16223
- [text] 45        13660        10235           405124           330731        10818
- [text] 46        33796        20781           707410           347741        24073
- [text] 47         2526         1533            54370            39583         1654
- [text]
- [text]     ld_rep_1932  dem_reweight_factor  rep_reweight_factor
- [text] 43         6817            12.595961            13.149039
- [text] 44        17122            21.775257            12.185784
- [text] 45        11338            37.449066            29.170136
- [text] 46        25731            29.386034            13.514477
- [text] 47         2072            32.871826            19.103764
+ [text] shape: (5, 12)
+ [text] ┌───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬──────────┐
+ [text] │ state     ┆ electoral ┆ actual_de ┆ actual_re ┆ … ┆ ld_dem_19 ┆ ld_rep_19 ┆ dem_rewei ┆ rep_rewe │
+ [text] │ ---       ┆ _votes    ┆ m_1936    ┆ p_1936    ┆   ┆ 32        ┆ 32        ┆ ght_facto ┆ ight_fac │
+ [text] │ str       ┆ ---       ┆ ---       ┆ ---       ┆   ┆ ---       ┆ ---       ┆ r         ┆ tor      │
+ [text] │           ┆ i64       ┆ i64       ┆ i64       ┆   ┆ i64       ┆ i64       ┆ ---       ┆ ---      │
+ [text] │           ┆           ┆           ┆           ┆   ┆           ┆           ┆ f64       ┆ f64      │
+ [text] ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪══════════╡
+ [text] │ Virginia  ┆ 11        ┆ 234980    ┆ 98336     ┆ … ┆ 16194     ┆ 6817      ┆ 12.595961 ┆ 13.14903 │
+ [text] │           ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆ 9        │
+ [text] │ Washingto ┆ 8         ┆ 459579    ┆ 206892    ┆ … ┆ 16223     ┆ 17122     ┆ 21.775257 ┆ 12.18578 │
+ [text] │ n         ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆ 4        │
+ [text] │ West      ┆ 8         ┆ 502582    ┆ 325358    ┆ … ┆ 10818     ┆ 11338     ┆ 37.449066 ┆ 29.17013 │
+ [text] │ Virginia  ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆ 6        │
+ [text] │ Wisconsin ┆ 12        ┆ 802984    ┆ 380828    ┆ … ┆ 24073     ┆ 25731     ┆ 29.386034 ┆ 13.51447 │
+ [text] │           ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆ 7        │
+ [text] │ Wyoming   ┆ 3         ┆ 62624     ┆ 38739     ┆ … ┆ 1654      ┆ 2072      ┆ 32.871826 ┆ 19.10376 │
+ [text] │           ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆ 4        │
+ [text] └───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴──────────┘
```

**Why:** Polars repr of the 12-column frame, with long float values wrapped onto continuation rows.
**Reader sees:** changed: six of the twelve columns are elided where pandas printed all twelve. The two columns the cell creates are still shown, so the cell still demonstrates what it is for.

<a id="c34"></a>
### C34 · `poll = poll.with_columns(` · output

committed output

```diff
- [text]         state  electoral_votes  actual_dem_1936  actual_rep_1936  ld_rep_1936  \
- [text] 0     Alabama               11           238196            35358         3060
- [text] 1     Arizona                3            86722            33433         2337
- [text] 2    Arkansas                9           146765            32049         2724
- [text] 3  California               22          1766836           836431        89516
- [text] 4    Colorado                6           295021           181267        15949
- [text]
- [text]    ld_dem_1936  actual_dem_1932  actual_rep_1932  ld_dem_1932  ld_rep_1932  \
- [text] 0        10082           207910            34675         9828         1589
- [text] 1         1975            79264            36104         2202         1679
- [text] 2         7608           189602            28467         7608         1566
- [text] 3        77245          1324157           847902        69720        80525
- [text] 4        10025           250877           189617         9970        13619
- [text]
- [text]    dem_reweight_factor  rep_reweight_factor  pred_dem_1936  pred_rep_1936
- [text] 0            21.154864            21.821901       213283.0        66775.0
- [text] 1            35.996367            21.503276        71093.0        50253.0
- [text] 2            24.921399            18.178161       189602.0        49517.0
- [text] 3            18.992499            10.529674      1467076.0       942574.0
- [text] 4            25.163190            13.922975       252261.0       222058.0
+ [text] shape: (5, 14)
+ [text] ┌───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬──────────┐
+ [text] │ state     ┆ electoral ┆ actual_de ┆ actual_re ┆ … ┆ dem_rewei ┆ rep_rewei ┆ pred_dem_ ┆ pred_rep │
+ [text] │ ---       ┆ _votes    ┆ m_1936    ┆ p_1936    ┆   ┆ ght_facto ┆ ght_facto ┆ 1936      ┆ _1936    │
+ [text] │ str       ┆ ---       ┆ ---       ┆ ---       ┆   ┆ r         ┆ r         ┆ ---       ┆ ---      │
+ [text] │           ┆ i64       ┆ i64       ┆ i64       ┆   ┆ ---       ┆ ---       ┆ f64       ┆ f64      │
+ [text] │           ┆           ┆           ┆           ┆   ┆ f64       ┆ f64       ┆           ┆          │
+ [text] ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪══════════╡
+ [text] │ Alabama   ┆ 11        ┆ 238196    ┆ 35358     ┆ … ┆ 21.154864 ┆ 21.821901 ┆ 213283.0  ┆ 66775.0  │
+ [text] │ Arizona   ┆ 3         ┆ 86722     ┆ 33433     ┆ … ┆ 35.996367 ┆ 21.503276 ┆ 71093.0   ┆ 50253.0  │
+ [text] │ Arkansas  ┆ 9         ┆ 146765    ┆ 32049     ┆ … ┆ 24.921399 ┆ 18.178161 ┆ 189602.0  ┆ 49517.0  │
+ [text] │ Californi ┆ 22        ┆ 1766836   ┆ 836431    ┆ … ┆ 18.992499 ┆ 10.529674 ┆ 1.467076e ┆ 942574.0 │
+ [text] │ a         ┆           ┆           ┆           ┆   ┆           ┆           ┆ 6         ┆          │
+ [text] │ Colorado  ┆ 6         ┆ 295021    ┆ 181267    ┆ … ┆ 25.16319  ┆ 13.922975 ┆ 252261.0  ┆ 222058.0 │
+ [text] └───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴──────────┘
```

**Why:** Polars repr of the 14-column frame.
**Reader sees:** changed: middle columns elided, and California's prediction prints as `1.467076e6` rather than `1467076.0`. The two new columns are the last two, so both remain visible.

<a id="c35"></a>
### C35 · `poll = poll.with_columns(` · output

committed output

```diff
- [text]         state  electoral_votes  actual_dem_1936  actual_rep_1936  ld_rep_1936  \
- [text] 0     Alabama               11           238196            35358         3060
- [text] 1     Arizona                3            86722            33433         2337
- [text] 2    Arkansas                9           146765            32049         2724
- [text] 3  California               22          1766836           836431        89516
- [text] 4    Colorado                6           295021           181267        15949
- [text]
- [text]    ld_dem_1936  actual_dem_1932  actual_rep_1932  ld_dem_1932  ld_rep_1932  \
- [text] 0        10082           207910            34675         9828         1589
- [text] 1         1975            79264            36104         2202         1679
- [text] 2         7608           189602            28467         7608         1566
- [text] 3        77245          1324157           847902        69720        80525
- [text] 4        10025           250877           189617         9970        13619
- [text]
- [text]    dem_reweight_factor  rep_reweight_factor  pred_dem_1936  pred_rep_1936  \
- [text] 0            21.154864            21.821901       213283.0        66775.0
- [text] 1            35.996367            21.503276        71093.0        50253.0
- [text] 2            24.921399            18.178161       189602.0        49517.0
- [text] 3            18.992499            10.529674      1467076.0       942574.0
- [text] 4            25.163190            13.922975       252261.0       222058.0
- [text]
- [text]    pred_total_1936  actual_total_1932  correction_factor
- [text] 0         280058.0             242585           0.866196
- [text] 1         121346.0             115368           0.950736
- [text] 2         239119.0             218069           0.911969
- [text] 3        2409650.0            2172059           0.901400
- [text] 4         474319.0             440494           0.928687
+ [text] shape: (5, 17)
+ [text] ┌───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬──────────┐
+ [text] │ state     ┆ electoral ┆ actual_de ┆ actual_re ┆ … ┆ pred_rep_ ┆ pred_tota ┆ actual_to ┆ correcti │
+ [text] │ ---       ┆ _votes    ┆ m_1936    ┆ p_1936    ┆   ┆ 1936      ┆ l_1936    ┆ tal_1932  ┆ on_facto │
+ [text] │ str       ┆ ---       ┆ ---       ┆ ---       ┆   ┆ ---       ┆ ---       ┆ ---       ┆ r        │
+ [text] │           ┆ i64       ┆ i64       ┆ i64       ┆   ┆ f64       ┆ f64       ┆ i64       ┆ ---      │
+ [text] │           ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆ f64      │
+ [text] ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪══════════╡
+ [text] │ Alabama   ┆ 11        ┆ 238196    ┆ 35358     ┆ … ┆ 66775.0   ┆ 280058.0  ┆ 242585    ┆ 0.866196 │
+ [text] │ Arizona   ┆ 3         ┆ 86722     ┆ 33433     ┆ … ┆ 50253.0   ┆ 121346.0  ┆ 115368    ┆ 0.950736 │
+ [text] │ Arkansas  ┆ 9         ┆ 146765    ┆ 32049     ┆ … ┆ 49517.0   ┆ 239119.0  ┆ 218069    ┆ 0.911969 │
+ [text] │ Californi ┆ 22        ┆ 1766836   ┆ 836431    ┆ … ┆ 942574.0  ┆ 2.40965e6 ┆ 2172059   ┆ 0.9014   │
+ [text] │ a         ┆           ┆           ┆           ┆   ┆           ┆           ┆           ┆          │
+ [text] │ Colorado  ┆ 6         ┆ 295021    ┆ 181267    ┆ … ┆ 222058.0  ┆ 474319.0  ┆ 440494    ┆ 0.928687 │
+ [text] └───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴──────────┘
```

**Why:** Polars repr of the 17-column frame.
**Reader sees:** changed: nine of seventeen columns elided where pandas printed all of them; the three new columns are last and stay visible.

<a id="c36"></a>
### C36 · `poll = poll.with_columns(` · output

committed output

```diff
- [text] 0.5419440974611633
+ [text] 0.5419440974611632
```

**Why:** A sum-order difference: pandas' `.sum()` and Polars' `.sum()` over the same 48 corrected values differ in the last unit in the last place (verified side by side — `...633` vs `...632`).
**Reader sees:** equivalent — the sixteenth significant figure of a proportion the chapter reads to three.

