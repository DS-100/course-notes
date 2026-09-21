# polars_2 — change report

`887a578b0a4b:content/pandas_3/pandas_3.ipynb` → `content/polars_2/polars_2.ipynb`

**Tier D · 163 changes:** output 41 · prose 37 · mixed 13 · dropdown 6 · tab-twins 45 · code 20 · metadata 1

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

> **Authored rewrite.** This chapter was renamed and re-written rather than converted cell by cell, so the diff below is not a cell-for-cell correspondence — whole sections were dropped, merged from another chapter, or written fresh. Read it as an inventory of what the reader gains and loses, not as a list of edits. `conversion/chapter_map.yml` records the lineage.

## Summary

`pandas_3` was replaced rather than converted: the chapter now follows lec04's spine (`group_by().agg()`, `.over()`, the `group_by` puzzle, `pivot`, joins), restores the four notes-only sections, and publishes 35 pandas/Polars comparison tab-sets — 36 of its 41 code cells carry `remove-input, remove-output`, so almost everything a reader sees is a tab pane rather than a raw cell output. A reader of the old chapter loses all MultiIndex material (multi-index `group_by` output, `pivot_table`'s hierarchical columns), the `.groups`/`get_group` tour of `DataFrameGroupBy` in its original form, `groupby.filter` with a lambda, the `.agg(lambda x: x.iloc[0])` framing of custom aggregation, the per-`Year` min/max/mean cells, the bulleted list of pandas `GroupBy` methods with their documentation links, and the `images/error.png` traceback screenshot; in exchange the chapter gains `.over()`, `map_batches(returns_scalar=True)`, `with_row_index`/`arg_max`, an explicit `merged.columns` cell, the five join strategies including `semi`/`anti`, and the join-coalescing explanation `eda` had been carrying. Three things are worth staff attention: (1) `p2-agg-unsorted` (C125) deliberately ships an unordered `group_by("Year")` result — 1971, 2004, 1992, 1998, 1995 — whose year labels carry no meaning and will not reproduce on re-execution; it is declared in `OUTPUT_CHURNS`, but it is the one committed table on the page that is not reproducible, and the tab beside it shows pandas returning 1910–1914 every time. (2) Several pandas twin panes were re-written to the closest analogue of the Polars code rather than to the pandas the old chapter actually taught — C74 pairs `.over()` with `groupby(...).transform("max")` where the baseline used `groupby().filter(lambda sf: ...)`, and C82 pairs `group_by(..., maintain_order=True).head(1)` with `groupby("Party", sort=False).head(1)` where the baseline used `agg(lambda x: x.iloc[0])` and published an alphabetically sorted table; both panes are true pandas, neither is the pandas the reader is migrating from. (3) Nine `.sort(...)` calls were added for determinism because Polars does not guarantee group order (`p2-agg-min`, `p2-agg-multiple-code`, `p2-first-letter-agg`, `p2-groupby-multi`, `p2-puzzle-attempt1`, `p2-puzzle-alt1a`, `p2-puzzle-alt1c`, `p2-puzzle-alt2`, `p2-rtp-table`); only `p2-puzzle-attempt1` says so in a comment, and under hard rule 2 a reviewer needs to be able to tell each of them from cosmetic pandas-matching. Two smaller notes: `ccf796ec` is **not** in this chapter — it lives in `content/polars_1/polars_1.ipynb`, where it now raises `TypeError: the truth value of an Expr is ambiguous`; `polars_2` and its baseline both commit zero error outputs, so there is no intentional-error cell here to protect. And cell 1 of the branch notebook (`46704fe4`) is an **empty markdown cell** introduced by the rewrite (see C8), and C75 is mislabelled `metadata` by the report generator when its diff is plainly prose, so it carries no review slot.

## Needs review

- [C2](#c2) · cell 1 [markdown]
- [C3](#c3) · cell 1 [markdown]
- [C4](#c4) · cell 1 [markdown]
- [C5](#c5) · cell 1 [markdown]
- [C8](#c8) · cell 1: We won't cover it explicitly in this class, but you are welc
- [C11](#c11) · cell 4 [markdown]
- [C12](#c12) · cell 4: Aggregating Data with `group_by`
- [C13](#c13) · cell 4: Aggregating Data with `group_by`
- [C15](#c15) · cell 6 [markdown]
- [C16](#c16) · cell 6 [markdown]
- [C17](#c17) · cell 6 [markdown]
- [C18](#c18) · cell 6 [markdown]
- [C21](#c21) · cell 12 [markdown]
- [C22](#c22) · cell 12: Aggregation Functions
- [C23](#c23) · cell 12: Aggregation Functions
- [C29](#c29) · cell 15 [markdown]
- [C32](#c32) · cell 18 [markdown]
- [C33](#c33) · cell 19 [code]
- [C39](#c39) · cell 21 [markdown]
- [C41](#c41) · cell 36: Plotting Birth Counts
- [C44](#c44) · cell 38 [markdown]
- [C45](#c45) · cell 38: Summary of `group_by()`
- [C48](#c48) · cell 54 [code]
- [C53](#c53) · cell 58 [markdown]
- [C56](#c56) · cell 60 [markdown]
- [C61](#c61) · cell 63 [markdown]
- [C62](#c62) · cell 63 [markdown]
- [C63](#c63) · cell 63 [markdown]
- [C64](#c64) · cell 63 [markdown]
- [C65](#c65) · cell 63 [markdown]
- [C71](#c71) · cell 66 [markdown]
- [C75](#c75) · cell 72 [markdown]
- [C76](#c76) · cell 72 [markdown]
- [C77](#c77) · cell 72 [markdown]
- [C78](#c78) · cell 72 [markdown]
- [C83](#c83) · cell 77 [markdown]
- [C84](#c84) · cell 77 [markdown]
- [C85](#c85) · cell 77: Alternative Solutions
- [C86](#c86) · cell 77: Alternative Solutions
- [C87](#c87) · cell 77: Alternative Solutions
- [C88](#c88) · cell 77: Alternative Solutions
- [C91](#c91) · cell 95: `group_by` with Multiple Columns
- [C92](#c92) · cell 95: `group_by` with Multiple Columns
- [C98](#c98) · cell 98 [markdown]
- [C99](#c99) · cell 98: `pivot`
- [C105](#c105) · cell 101 [markdown]
- [C110](#c110) · cell 104 [markdown]
- [C116](#c116) · cell 109 [markdown]
- [C121](#c121) · cell 117: Parting Note
- [C122](#c122) · cell 117: Parting Note

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C123](#c123) · `import polars as pl` · no matching baseline cell — compare against the chapter, not the hunk
- [C124](#c124) · `babynames.group_by("Year")` · no matching baseline cell — compare against the chapter, not the hunk
- [C125](#c125) · `babynames.group_by("Year").agg(pl.col("Count").sum()).head(5)` · no matching baseline cell — compare against the chapter, not the hunk
- [C126](#c126) · `babies_by_year = babynames.group_by("Year").agg(pl.col("Count").sum())` · no matching baseline cell — compare against the chapter, not the hunk
- [C127](#c127) · `babynames.group_by("Name").agg(pl.col("Count").min()).sort("Name").hea` · no matching baseline cell — compare against the chapter, not the hunk
- [C128](#c128) · `babynames.group_by("Name").agg(` · no matching baseline cell — compare against the chapter, not the hunk
- [C129](#c129) · `babynames_new = babynames.with_columns(` · no matching baseline cell — compare against the chapter, not the hunk
- [C130](#c130) · `babynames_new.group_by("Name").agg(` · no matching baseline cell — compare against the chapter, not the hunk
- [C131](#c131) · `df = pl.DataFrame({"letter": ["A", "A", "B", "C", "C", "C"],` · no matching baseline cell — compare against the chapter, not the hunk
- [C132](#c132) · `df.group_by("letter", maintain_order=True).len()` · no matching baseline cell — compare against the chapter, not the hunk
- [C133](#c133) · `df.group_by("letter", maintain_order=True).agg(pl.all().count())` · no matching baseline cell — compare against the chapter, not the hunk
- [C134](#c134) · `df["letter"].value_counts(sort=True)` · no matching baseline cell — compare against the chapter, not the hunk
- [C135](#c135) · `fig = px.line(babies_by_year, x="Year", y="Count")` · no matching baseline cell — compare against the chapter, not the hunk
- [C136](#c136) · `f_babynames = babynames.filter(pl.col("Sex") == "F").sort("Year")` · no matching baseline cell — compare against the chapter, not the hunk
- [C137](#c137) · `jenn_counts = f_babynames.filter(pl.col("Name") == "Jennifer")["Count"` · no matching baseline cell — compare against the chapter, not the hunk
- [C138](#c138) · `rtp_table = f_babynames.group_by("Name").agg(` · no matching baseline cell — compare against the chapter, not the hunk
- [C139](#c139) · `def ratio_to_peak(series):` · no matching baseline cell — compare against the chapter, not the hunk
- [C140](#c140) · `rtp_table.sort("Count RTP").head()` · no matching baseline cell — compare against the chapter, not the hunk
- [C141](#c141) · `fig = px.line(f_babynames.filter(pl.col("Name") == "Debra"), x="Year",` · no matching baseline cell — compare against the chapter, not the hunk
- [C142](#c142) · `top10 = rtp_table.sort("Count RTP").head(10)["Name"].to_list()` · no matching baseline cell — compare against the chapter, not the hunk
- [C143](#c143) · `fig = px.line(` · no matching baseline cell — compare against the chapter, not the hunk
- [C144](#c144) · `elections = pl.read_csv("data/elections.csv")` · no matching baseline cell — compare against the chapter, not the hunk
- [C145](#c145) · `df.filter(pl.len().over("letter") >= 2)` · no matching baseline cell — compare against the chapter, not the hunk
- [C146](#c146) · `elections.filter(pl.col("%").max().over("Year") < 45).head(9)` · no matching baseline cell — compare against the chapter, not the hunk
- [C147](#c147) · `elections.group_by("Party").max().sort("Party").head(10)` · no matching baseline cell — compare against the chapter, not the hunk
- [C148](#c148) · `elections_sorted_by_percent = elections.sort("%", descending=True)` · no matching baseline cell — compare against the chapter, not the hunk
- [C149](#c149) · `best_per_party = elections_sorted_by_percent.group_by("Party", maintai` · no matching baseline cell — compare against the chapter, not the hunk
- [C150](#c150) · `best_positions = (` · no matching baseline cell — compare against the chapter, not the hunk
- [C151](#c151) · `elections[best_positions["position"]].sort("Party").head()` · no matching baseline cell — compare against the chapter, not the hunk
- [C152](#c152) · `best_per_party2 = elections.sort("%").unique(subset=["Party"], keep="l` · no matching baseline cell — compare against the chapter, not the hunk
- [C153](#c153) · `grouped_by_party = elections.group_by("Party")` · no matching baseline cell — compare against the chapter, not the hunk
- [C154](#c154) · `groups = dict(grouped_by_party)` · no matching baseline cell — compare against the chapter, not the hunk
- [C155](#c155) · `groups[("Socialist",)]` · no matching baseline cell — compare against the chapter, not the hunk
- [C156](#c156) · `babynames.group_by(["Year", "Sex"]).agg(pl.col("Count").sum()).sort(["` · no matching baseline cell — compare against the chapter, not the hunk
- [C157](#c157) · `babynames.pivot(` · no matching baseline cell — compare against the chapter, not the hunk
- [C158](#c158) · `babynames.pivot(` · no matching baseline cell — compare against the chapter, not the hunk
- [C159](#c159) · `elections = elections.with_columns(` · no matching baseline cell — compare against the chapter, not the hunk
- [C160](#c160) · `babynames_2022 = babynames.filter(pl.col("Year") == 2022)` · no matching baseline cell — compare against the chapter, not the hunk
- [C161](#c161) · `merged = elections.join(` · no matching baseline cell — compare against the chapter, not the hunk
- [C162](#c162) · `merged.columns` · no matching baseline cell — compare against the chapter, not the hunk
- [C163](#c163) · `elections.join(babynames_2022, left_on="First Name", right_on="Name", ` · no matching baseline cell — compare against the chapter, not the hunk

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C6](#c6) · cell 1: We won't cover it explicitly in this class, but you are welc
- [C7](#c7) · cell 1: We won't cover it explicitly in this class, but you are welc
- [C42](#c42) · cell 36: Plotting Birth Counts
- [C47](#c47) · cell 53 [markdown]
- [C54](#c54) · cell 58 [markdown]
- [C57](#c57) · cell 60: Filtering by Group

## Changes

<a id="c1"></a>
### C1 · cell 1 [markdown] · metadata

baseline L15 → branch L15

```diff
- # %% [markdown]
+ # %% [markdown] id="p2-intro"
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c2"></a>
### C2 · cell 1 [markdown] · prose · **REVIEW**

baseline L17 → branch L17

```diff
- # title: Pandas III
+ # title: Polars II
```

**Why:** Chapter renamed with the `content/pandas_3` -> `content/polars_2` move; allowlisted under `polars_2: frontmatter`. The numbered-title convention (`Pandas I/II/III` -> `Polars I/II`) is the deliberate exception to the book's descriptive titles.
**Verdict:** necessary

<a id="c3"></a>
### C3 · cell 1 [markdown] · prose · **REVIEW**

baseline L21 → branch L21

```diff
- # * Perform advanced aggregation using `.groupby()`
- # * Use the `pd.pivot_table` method to construct a pivot table
- # * Perform simple merges between DataFrames using `pd.merge()`
+ # * Aggregate rows into groups using `.group_by()` and `.agg()`
+ # * Write aggregations as expressions, including ones of your own design
+ # * Select rows by a property of the group they belong to using `.over()`
+ # * Restructure a grouped result with `.pivot()`
+ # * Combine two `DataFrame`s with `.join()`
```

**Why:** The three baseline objectives name `.groupby()`, `pd.pivot_table` and `pd.merge()` by API. The five replacements name the Polars entry points and add the two topics the rewrite introduces that pandas had no separate objective for: writing aggregations as expressions, and selecting rows by a property of their group (`.over()`).
**Verdict:** necessary

<a id="c4"></a>
### C4 · cell 1 [markdown] · prose · **REVIEW**

baseline L26 → branch L28

```diff
- # We will introduce the concept of aggregating data – we will familiarize ourselves with `GroupBy` objects and used them as tools to consolidate and summarize a `DataFrame`. In this lecture, we will explore working with the different aggregation functions and dive into some advanced `.groupby` methods to show just how powerful of a resource they can be for understanding our data. We will also introduce other techniques for data aggregation to provide flexibility in how we manipulate our tables.
+ # We will introduce the idea of aggregating data: gathering rows that belong together, then computing a single summary value for each collection of rows. We'll work through the aggregation functions Polars offers, write a couple of our own, and use grouping to answer questions that no individual row of a table can answer. We'll then pick up two more tools for rearranging and combining tables: pivot tables and joins.
```

**Why:** Re-authored to drop the "`GroupBy` objects as tools" framing and name the two additional topics. Nothing in the baseline paragraph is factually pandas-only except that phrase.
**Verdict:** optional
**Minimal alternative:** Keep the baseline paragraph and change only "`GroupBy` objects" -> "`.group_by`" and "`.groupby` methods" -> "`group_by` methods".

<a id="c5"></a>
### C5 · cell 1 [markdown] · prose · **REVIEW**

baseline L28 → branch L30

```diff
- # First, let's load `babynames` dataset.
+ # First, let's load the `babynames` dataset.
```

**Why:** Missing-article grammar fix. Unrelated to the conversion.
**Verdict:** optional
**Minimal alternative:** Revert; the sentence was readable as it stood.

<a id="c6"></a>
### C6 · cell 1: We won't cover it explicitly in this class, but you are welc · dropdown

baseline L35 → branch L37 · mirror of the next code cell (hard rule 3)

```diff
- # import pandas as pd
- # import numpy as np
+ # import polars as pl
+ # import plotly.express as px
```

**Why:** `pandas`/`numpy` -> `polars`/`plotly.express`. `px` is hoisted into this cell because the chapter now draws three figures; the baseline imported it twice, mid-chapter. `numpy` is dropped -- its only use was `np.nan` in the small `df`, which becomes `None`.
**Output:** same -- verified: the dropdown's fenced block is byte-identical to code cell `p2-load-babynames` (hard rule 3 satisfied).

<a id="c7"></a>
### C7 · cell 1: We won't cover it explicitly in this class, but you are welc · dropdown

baseline L52 → branch L54 · mirror of the next code cell (hard rule 3)

```diff
- #     babynames = pd.read_csv(fh, header=None, names=field_names)
+ #     babynames = pl.read_csv(fh, has_header=False, new_columns=field_names)
```

**Why:** `header=None, names=field_names` -> `has_header=False, new_columns=field_names`.
**Output:** same -- verified byte-identical to `p2-load-babynames`.

<a id="c8"></a>
### C8 · cell 1: We won't cover it explicitly in this class, but you are welc · mixed · **REVIEW**

baseline L58 → branch L60 · spans code and prose

```diff
- # %% tags=["remove-input"]
+ 
+ # %% [markdown]
+ #
+ 
+ # %% tags=["remove-input"] id="p2-load-babynames"
```

**Why:** Cell ids were added ahead of the loader cell so the id-keyed gates and the allowlist can address it. The hunk also inserts an **empty markdown cell** (`46704fe4`, branch cell index 1) between the dropdown and the loader -- a jupytext artifact of the rewrite, not content. It renders as nothing, but it is noise in the notebook and nothing in the record accounts for it.
**Verdict:** questionable
**Minimal alternative:** Delete the empty markdown cell; keep the `id=` additions, which the gates require.

<a id="c9"></a>
### C9 · cell 3 [code] · code

baseline L61 → branch L67

```diff
- import pandas as pd
- import numpy as np
+ import polars as pl
+ import plotly.express as px
```

**Why:** Same import swap as C6, in the cell the dropdown mirrors.
**Output:** differs: Polars repr for `babynames.head()` -- see C123. Same five rows and values.

<a id="c10"></a>
### C10 · cell 3 [code] · code

baseline L78 → branch L84

```diff
-     babynames = pd.read_csv(fh, header=None, names=field_names)
+     babynames = pl.read_csv(fh, has_header=False, new_columns=field_names)
```

**Why:** Same `read_csv` keyword rename as C7.
**Output:** differs: repr only; the frame is identical, 407,428 rows (verified live).

<a id="c11"></a>
### C11 · cell 4 [markdown] · prose · **REVIEW**

baseline L82 → branch L88

```diff
- # %% [markdown]
- # ## Aggregating Data with `.groupby`
+ # %% [markdown] id="p2-groupby-intro"
+ # ## Aggregating Data with `group_by`
```

**Why:** `.groupby` -> `group_by` in a section heading, which is also the section anchor.
**Verdict:** necessary

<a id="c12"></a>
### C12 · cell 4: Aggregating Data with `group_by` · prose · **REVIEW**

baseline L85 → branch L91

```diff
- # Up until this point, we have been working with individual rows of `DataFrame`s. As data scientists, we often wish to investigate trends across a larger *subset* of our data. For example, we may want to compute some summary statistic (the mean, median, sum, etc.) for a group of rows in our `DataFrame`. To do this, we'll use `pandas` `GroupBy` objects. Our goal is to group together rows that fall under the same category and perform an operation that aggregates across all rows in the category.
+ # Up until this point, we have been working with individual rows of `DataFrame`s. As data scientists, we often wish to investigate trends across a larger *subset* of our data. We may want to compute some summary statistic (the mean, the median, the sum) for a whole collection of rows at once. The rows of `babynames` record one name, in one year, for one sex; a question like "how many babies were born in California in 1990?" is not answered by any single row.
```

**Why:** The baseline's first two sentences are kept verbatim; the pandas-specific clause ("we'll use `pandas` `GroupBy` objects") is replaced by a concrete question about `babynames` that no single row answers. The replacement motivates grouping rather than naming the object that performs it.
**Verdict:** optional
**Minimal alternative:** Keep the baseline paragraph and swap the one clause: "we'll use `pandas` `GroupBy` objects" -> "we'll use `.group_by`".

<a id="c13"></a>
### C13 · cell 4: Aggregating Data with `group_by` · prose · **REVIEW**

baseline L87 → branch L93

```diff
- # Let's say we wanted to aggregate all rows in `babynames` for a given year.
+ # The tool for this is `.group_by` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.group_by.html). We tell it which column holds the value that decides who belongs with whom. Let's gather all rows in `babynames` that share a year.
```

**Why:** Carries the `.group_by` documentation link. The baseline's link was on pandas' `groupby` and sat in the next cell (C15); it could not survive G13, so the pointer moved here and the sentence gained a statement of what the argument means.
**Verdict:** necessary

<a id="c14"></a>
### C14 · cell 5 [code] · code

baseline L89 → branch L95

```diff
- # %%
- babynames.groupby("Year")
+ # %% id="p2-groupby-object"
+ babynames.group_by("Year")
```

**Why:** `.groupby` -> `.group_by`.
**Output:** differs: `<polars.dataframe.group_by.GroupBy ...>` instead of the pandas `DataFrameGroupBy` repr -- see C124. Both are opaque objects, which is the point the prose makes.

<a id="c15"></a>
### C15 · cell 6 [markdown] · prose · **REVIEW**

baseline L92 → branch L98

```diff
- # %% [markdown]
- # What does this strange output mean? Calling `.groupby` [(documentation)](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html) has generated a `GroupBy` object. You can imagine this as a set of "mini", grouped sub-`DataFrame`s, where each group/sub-`DataFrame` contains all of the rows from `babynames` that correspond to a particular year.
+ # %% [markdown] id="p2-groupby-explain"
+ # That output is not a table. Calling `.group_by` produces a `GroupBy` object, which you can picture as a set of "mini", grouped sub-`DataFrame`s, where each sub-`DataFrame` holds all of the rows from `babynames` that correspond to one particular year.
```

**Why:** The pandas documentation link is removed and "strange output" is reworded to "That output is not a table". The sub-`DataFrame` mental picture is kept verbatim because Polars' `GroupBy` is the same idea.
**Verdict:** necessary

<a id="c16"></a>
### C16 · cell 6 [markdown] · prose · **REVIEW**

baseline L95 → branch L101

```diff
- # The diagram below shows a simplified view of `babynames` to help illustrate this idea.
+ # The diagram below shows a simplified view of `babynames` to help illustrate the idea.
```

**Why:** "this idea" -> "the idea".
**Verdict:** optional
**Minimal alternative:** Revert; no conversion pressure on this word.

<a id="c17"></a>
### C17 · cell 6 [markdown] · prose · **REVIEW**

baseline L98 → branch L104

```diff
- # :alt: Example of how a dataframe is conceptually transformed by group by.
+ # :alt: A DataFrame whose rows are regrouped by the value of one column, producing one sub-table per distinct value.
```

**Why:** Alt text rewritten. The baseline alt restated the caption ("Example of how a dataframe is conceptually transformed by group by") rather than describing the drawing; the replacement describes what is drawn. The PNG itself is unchanged.
**Verdict:** optional
**Minimal alternative:** Keep the baseline alt text -- the image did not change, so this is an a11y improvement the conversion did not require. Worth taking anyway, but it is a separate change.

<a id="c18"></a>
### C18 · cell 6 [markdown] · prose · **REVIEW**

baseline L102 → branch L108

```diff
- # We can't work with a `GroupBy` object directly – that is why you saw that strange output earlier rather than a standard view of a `DataFrame`. To actually manipulate values within these groups/sub-`DataFrame`s, we'll need to call an *aggregation method*. This is a method that tells `pandas` how to aggregate the values within the `GroupBy` object. Once the aggregation is applied, `pandas` will return a normal (now grouped) `DataFrame`.
- #
- # The first aggregation method we'll consider is `.agg`. The `.agg` method takes in a function as its argument; this function is then applied to each column of a group/sub-`DataFrame`. We end up with a new `DataFrame` with one aggregated row per subframe. Let's see this in action by finding the `sum` of all counts for each year in `babynames` – this is equivalent to finding the number of babies born in each year.
+ # A `GroupBy` object holds the groups, but it has not computed anything yet. To get numbers back out, we call `.agg` and hand it one or more *aggregation expressions*. Each expression is applied to every group in turn, and each one collapses a column of the group down to a single value. Let's find the `sum` of all counts for each year, which is the number of babies born in California in that year.
```

**Why:** The baseline says `.agg` "takes in a function as its argument; this function is then applied to each column". That is false of Polars: `.agg` takes expressions, and each expression names the column it applies to. The paragraph also promised a "normal (now grouped) `DataFrame`", which in Polars is just a `DataFrame` with the keys as ordinary columns.
**Verdict:** necessary

<a id="c19"></a>
### C19 · cell 7 [code] · code

baseline L106 → branch L110

```diff
- # %%
- babynames[["Year", "Count"]].groupby("Year").agg("sum").head(5)
+ # %% tags=["remove-input", "remove-output"] id="p2-agg-unsorted"
+ babynames.group_by("Year").agg(pl.col("Count").sum()).head(5)
```

**Why:** `babynames[["Year", "Count"]].groupby("Year").agg("sum")` -> `babynames.group_by("Year").agg(pl.col("Count").sum())`. The column pre-selection disappears because the expression names its own column, and the string agg name becomes an expression. The cell also gained `remove-input, remove-output` because its output is republished inside the tab-set below.
**Output:** differs: group order -- see C125. The sums are also whole-dataset totals (310,020 etc.) rather than the baseline's simplified-diagram numbers.

<a id="c20"></a>
### C20 · cell 8 [markdown] · tab-twins

baseline L110 → branch L114 · spans code and prose

```diff
- # We can relate this back to the diagram we used above. Remember that the diagram uses a simplified version of `babynames`, which is why we see smaller values for the summed counts.
+ # <!-- tab-twins:begin babynames.group_by("Year").agg(pl.col("Count").sum()).head(5) -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # babynames.group_by("Year").agg(pl.col("Count").sum()).head(5)
+ # ```
+ #
+ # ```text
+ # shape: (5, 2)
+ # ┌──────┬────────┐
+ # │ Year ┆ Count  │
+ # │ ---  ┆ ---    │
+ # │ i64  ┆ i64    │
+ # ╞══════╪════════╡
+ # │ 1971 ┆ 310020 │
+ # │ 2004 ┆ 480892 │
+ # │ 1992 ┆ 541054 │
+ # │ 1998 ┆ 464300 │
+ # │ 1995 ┆ 494635 │
+ # └──────┴────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_pd.groupby("Year")["Count"].sum().head(5)
+ # ```
+ #
+ # ```text
+ # Year
+ # 1910     9163
+ # 1911     9983
+ # 1912    17946
+ # 1913    22094
+ # 1914    26926
+ # Name: Count, dtype: int64
+ # ```
+ # ::::
+ … 67 more lines
```

**Why:** The prose that stood here ("relate this back to the diagram... smaller values for the summed counts") is replaced by the chapter's first comparison tab-set.
**Output:** differs: the pandas pane prints a `Series` indexed by Year for 1910-1914; the Polars pane a two-column frame for five arbitrary years. Declared in `OUTPUT_CHURNS`, so `tab_twins --verify` checks the code panes only.

<a id="c21"></a>
### C21 · cell 12 [markdown] · prose · **REVIEW**

baseline L113 → branch L223

```diff
- # :alt: Example of how a dataframe is conceptually transformed by group by and an aggregation.
+ # :alt: Grouped sub-tables each collapsed by a sum into a single row, which are then stacked into one output table.
```

**Why:** As C17: alt text rewritten to describe the drawing rather than the caption. The PNG is unchanged.
**Verdict:** optional
**Minimal alternative:** Keep the baseline alt text.

<a id="c22"></a>
### C22 · cell 12: Aggregation Functions · prose · **REVIEW**

baseline L117 → branch L227

```diff
- # Calling `.agg` has condensed each subframe (i.e. group/sub-`DataFrame`) back into a single row. This gives us our final output: a `DataFrame` that is now indexed by `"Year"`, with a single row for each unique year in the original `babynames` DataFrame.
+ # ### Aggregation Functions
```

**Why:** The baseline sentence describes the output as "a `DataFrame` that is now indexed by `"Year"`". Polars has no index, so the claim could not be adapted, and the section heading was moved up into its place.
**Verdict:** necessary

<a id="c23"></a>
### C23 · cell 12: Aggregation Functions · prose · **REVIEW**

baseline L119 → branch L229

```diff
- # There are many different aggregation functions we can use, all of which are useful in different applications.
+ # An aggregation function takes a column belonging to one group and returns a single value for it. Polars writes these as expressions [(documentation)](https://docs.pola.rs/api/python/stable/reference/expressions/aggregation.html), and the common ones read exactly as they sound:
+ #
+ # * `pl.col("c").sum()`, `.mean()`, `.median()`
+ # * `pl.col("c").min()`, `.max()`
+ # * `pl.col("c").first()`, `.last()`
+ # * `pl.col("c").n_unique()`
+ # * `pl.len()`, the number of rows in the group
+ #
+ # Here is the smallest number of babies given each name in any single year.
```

**Why:** "There are many different aggregation functions" is replaced by the actual list of Polars aggregation expressions plus the Polars documentation link. The baseline's list (further down) was of pandas string names and NumPy functions, neither of which is the Polars form -- `np.mean` on a Polars Series raises.
**Verdict:** necessary

<a id="c24"></a>
### C24 · cell 13 [code] · code

baseline L121 → branch L239

```diff
- # %%
- babynames[["Year", "Count"]].groupby("Year").agg("min").head(5)
- 
- # %%
- babynames[["Year", "Count"]].groupby("Year").agg("max").head(5)
- 
- # %%
- # Same result, but now we explicitly tell pandas to only consider the "Count" column when summing
- babynames.groupby("Year")[["Count"]].agg("sum").head(5)
+ # %% tags=["remove-input", "remove-output"] id="p2-agg-min"
+ # What is the minimum count for each name in any year?
+ babynames.group_by("Name").agg(pl.col("Count").min()).sort("Name").head()
```

**Why:** Three baseline cells (`agg("min")` by Year, `agg("max")` by Year, and `agg("sum")` with explicit column selection) collapse into one, because in Polars all three are the same shape with a different expression. The grouping key moved from `Year` to `Name` so each group has more than one number in it, and `.sort("Name")` was added because group order is not guaranteed.
**Output:** differs: per-name minima (Aadan 5, Aadarsh 6, ...) where the baseline printed per-year minima. The baseline's separate max-by-Year and sum-with-selection cells have no successor.

<a id="c25"></a>
### C25 · cell 14 [markdown] · tab-twins

baseline L132 → branch L244

```diff
- # There are many different aggregations that can be applied to the grouped data. The primary requirement is that an aggregation function must:
+ # <!-- tab-twins:begin babynames.group_by("Name").agg(pl.col("Count").min()).sort("Name").head() -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # What is the minimum count for each name in any year?
+ # babynames.group_by("Name").agg(pl.col("Count").min()).sort("Name").head()
+ # ```
```

**Why:** The baseline prose stated the pandas requirement that an aggregation "take in a `Series`... return a single value". That is a statement about functions, and Polars aggregations are expressions, so the tab-set replaces it.
**Output:** differs: the Polars pane is a two-column frame with a `shape:` header and a dtype row; the pandas pane a `Series`. Same five names and values.

<a id="c26"></a>
### C26 · cell 14: What is the minimum count for each name in any year? · tab-twins

baseline L134 → branch L253

```diff
- # * Take in a `Series` of data (a single column of the grouped subframe).
- # * Return a single value that aggregates this `Series`.
+ # ```text
+ # shape: (5, 2)
+ # ┌─────────┬───────┐
+ # │ Name    ┆ Count │
+ # │ ---     ┆ ---   │
+ # │ str     ┆ i64   │
+ # ╞═════════╪═══════╡
+ # │ Aadan   ┆ 5     │
+ # │ Aadarsh ┆ 6     │
+ # │ Aaden   ┆ 10    │
+ # │ Aadhav  ┆ 6     │
+ # │ Aadhini ┆ 6     │
+ # └─────────┴───────┘
+ # ```
+ # ::::
```

**Why:** Polars output pane for the min-by-name cell.
**Output:** differs: frame repr vs Series repr. Values identical.

<a id="c27"></a>
### C27 · cell 14: What is the minimum count for each name in any year? · tab-twins

baseline L137 → branch L269

```diff
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_pd.groupby("Name")["Count"].min().sort_index().head()
+ # ```
```

**Why:** pandas code pane: `groupby("Name")["Count"].min().sort_index()` -- the `sort_index()` mirrors the Polars `.sort("Name")` that group-order instability forced.
**Output:** same operation both sides.

<a id="c28"></a>
### C28 · cell 14: What is the minimum count for each name in any year? · tab-twins

baseline L138 → branch L275

```diff
- # ### Aggregation Functions
- #
- # Because of this fairly broad requirement, `pandas` offers many ways of computing an aggregation.
- #
- # **In-built** Python operations – such as `sum`, `max`, and `min` – are automatically recognized by `pandas`.
+ # ```text
+ # Name
+ # Aadan       5
+ # Aadarsh     6
+ # Aaden      10
+ # Aadhav      6
+ # Aadhini     6
+ # Name: Count, dtype: int64
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** pandas output pane.
**Output:** differs: a `Series` named `Count` indexed by `Name`, against a two-column frame. Same five values.

<a id="c29"></a>
### C29 · cell 15 [markdown] · mixed · **REVIEW**

baseline L144 → branch L288 · spans code and prose

```diff
- # %%
- # What is the minimum count for each name in any year?
- babynames.groupby("Name")[["Count"]].agg("min").head()
+ # %% [markdown] id="p2-agg-multiple"
+ # One `.agg` call can carry as many expressions as we like, and `.alias` [(documentation)](https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.alias.html) gives each result a name. Without it, three aggregations of `Count` would all want to be called `Count`.
```

**Why:** New prose with no baseline counterpart: `.agg` taking several expressions, and the naming collision that creates (three aggregations of `Count` all wanting to be called `Count`), which pandas resolved silently with MultiIndex columns.
**Verdict:** necessary

<a id="c30"></a>
### C30 · cell 16 [code] · code

baseline L148 → branch L291

```diff
- # %%
- # What is the largest single-year count of each name?
- babynames.groupby("Name")[["Count"]].agg("max").head()
+ # %% tags=["remove-input", "remove-output"] id="p2-agg-multiple-code"
+ babynames.group_by("Name").agg(
+     pl.col("Count").min().alias("Min Count"),
+     pl.col("Count").max().alias("Max Count"),
+     pl.col("Count").mean().alias("Mean Count"),
+     pl.len().alias("Years Recorded"),
+ ).sort("Name").head()
```

**Why:** The max-by-Name cell becomes a four-expression `.agg` with `.alias` on each. This is what replaced pandas' dict-agg-with-lists, which produced MultiIndex columns; `pl.len()` supplies the group size pandas got from `.size()`.
**Output:** differs: one five-column table where the baseline printed a one-column max table, plus a new `Years Recorded` column.

<a id="c31"></a>
### C31 · cell 17 [markdown] · tab-twins

baseline L153 → branch L300

```diff
- # As mentioned previously, functions from the `NumPy` library, such as `np.mean`, `np.max`, `np.min`, and `np.sum`, are also fair game in `pandas`.
+ # <!-- tab-twins:begin pl.col("Count").mean().alias("Mean Count"), -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # babynames.group_by("Name").agg(
+ #     pl.col("Count").min().alias("Min Count"),
+ #     pl.col("Count").max().alias("Max Count"),
+ #     pl.col("Count").mean().alias("Mean Count"),
+ #     pl.len().alias("Years Recorded"),
+ # ).sort("Name").head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 5)
+ # ┌─────────┬───────────┬───────────┬────────────┬────────────────┐
+ # │ Name    ┆ Min Count ┆ Max Count ┆ Mean Count ┆ Years Recorded │
+ # │ ---     ┆ ---       ┆ ---       ┆ ---        ┆ ---            │
+ # │ str     ┆ i64       ┆ i64       ┆ f64        ┆ u32            │
+ # ╞═════════╪═══════════╪═══════════╪════════════╪════════════════╡
+ # │ Aadan   ┆ 5         ┆ 7         ┆ 6.0        ┆ 3              │
+ # │ Aadarsh ┆ 6         ┆ 6         ┆ 6.0        ┆ 1              │
+ # │ Aaden   ┆ 10        ┆ 158       ┆ 46.214286  ┆ 14             │
+ # │ Aadhav  ┆ 6         ┆ 8         ┆ 6.75       ┆ 4              │
+ # │ Aadhini ┆ 6         ┆ 6         ┆ 6.0        ┆ 1              │
+ # └─────────┴───────────┴───────────┴────────────┴────────────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_pd.groupby("Name")["Count"].agg(
+ #     **{"Min Count": "min", "Max Count": "max", "Mean Count": "mean",
+ #        "Years Recorded": "size"}
+ # ).sort_index().head()
+ # ```
+ #
+ # ```text
+ #          Min Count  Max Count  Mean Count  Years Recorded
+ … 10 more lines
```

**Why:** The baseline sentence here claimed NumPy functions such as `np.mean` are "fair game" -- false in Polars, where `np.mean(series)` raises `TypeError` on the `axis=` keyword. It is deleted and the tab-set takes its place.
**Output:** differs: `Years Recorded` is `u32` in Polars against pandas' `int64`; all other values identical.

<a id="c32"></a>
### C32 · cell 18 [markdown] · mixed · **REVIEW**

baseline L155 → branch L351 · spans code and prose

```diff
- # %%
- # What is the average count for each name across all years?
- babynames.groupby("Name")[["Count"]].agg("mean").head()
+ # %% [markdown] id="p2-first-last"
+ # The name "Aaden" is a good illustration of what these four numbers buy us: it appears in 14 different years, with counts ranging from 10 to 158.
+ #
+ # `.first()` and `.last()` are a little different from the rest, because they select a value rather than compute one. They are what we want when every row of a group carries the same value in some column, and we want that value carried through to the output. To see this, let's add a column to `babynames` holding the first letter of each name.
+ #
+ # ```{image} images/first.png
+ # :alt: Grouped sub-tables reduced to one row each by taking the first entry of a column.
+ # :width: 500
+ # ```
```

**Why:** The pandas paragraph describing `"first"`/`"last"` as "unique to `pandas`" could not survive. The replacement reads the four numbers of the previous table (Aaden, 14 years, 10 to 158) and moves the `images/first.png` figure up from the section below to sit beside the explanation it illustrates.
**Verdict:** optional
**Minimal alternative:** Rewrite the "unique to `pandas`" clause only, and leave `first.png` where the baseline had it.

<a id="c33"></a>
### C33 · cell 19 [code] · mixed · **REVIEW**

baseline L159 → branch L361 · spans code and prose

```diff
- # %% [markdown]
- # `pandas` also offers a number of in-built functions. Functions that are native to `pandas` can be referenced using their string name within a call to `.agg`. Some examples include:
- #
- # * `.agg("sum")`
- # * `.agg("max")`
- # * `.agg("min")`
- # * `.agg("mean")`
- # * `.agg("first")`
- # * `.agg("last")`
- #
- # The latter two entries in this list – `"first"` and `"last"` – are unique to `pandas`. They return the first or last entry in a subframe column. Why might this be useful? Consider a case where *multiple* columns in a group share identical information. To represent this information in the grouped output, we can simply grab the first or last entry, which we know will be identical to all other entries.
- #
- # Let's illustrate this with an example. Say we add a new column to `babynames` that contains the first letter of each name.
+ # %% tags=["remove-input", "remove-output"] id="p2-first-letter"
+ # Imagine we had an additional column, "First Letter". We'll explain string methods like this one in a later chapter
+ babynames_new = babynames.with_columns(
+     pl.col("Name").str.slice(0, 1).alias("First Letter")
+ ).select(["Name", "First Letter", "Year"])
```

**Why:** The baseline's list of pandas string agg names (`.agg("sum")`, `.agg("max")`, ...) is pandas-only and is deleted. The First Letter cell replaces it: `babynames["Name"].str[0]` -> `pl.col("Name").str.slice(0, 1)` (Polars' second argument is a length, not a stop), and the baseline's two cells -- assignment then column subset -- merge into one `with_columns(...).select(...)` because there is no in-place assignment. The comment's "next week" became "a later chapter", which is right for a book.
**Verdict:** necessary

<a id="c34"></a>
### C34 · cell 17 [code] · code

baseline L173 → branch L367

```diff
- # %%
- # Imagine we had an additional column, "First Letter". We'll explain this code next week
- babynames["First Letter"] = babynames["Name"].str[0]
- 
- # We construct a simplified DataFrame containing just a subset of columns
- babynames_new = babynames[["Name", "First Letter", "Year"]]
```

**Why:** Deletion of the baseline's First Letter cell, superseded by C33's single `with_columns(...).select(...)`.
**Output:** same -- the surviving cell produces the same five rows (Mary/M/1910 ...).

<a id="c35"></a>
### C35 · cell 20 [markdown] · tab-twins

baseline L182 → branch L370

```diff
- # If we form groups for each name in the dataset, `"First Letter"` will be the same for all members of the group. This means that if we simply select the first entry for `"First Letter"` in the group, we'll represent all data in that group.
+ # <!-- tab-twins:begin pl.col("Name").str.slice(0, 1).alias("First Letter") -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Imagine we had an additional column, "First Letter". We'll explain string methods like this one in a later chapter
+ # babynames_new = babynames.with_columns(
+ #     pl.col("Name").str.slice(0, 1).alias("First Letter")
+ # ).select(["Name", "First Letter", "Year"])
```

**Why:** Polars code pane for the First Letter cell.
**Output:** same result as the pandas pane.

<a id="c36"></a>
### C36 · cell 20: Imagine we had an additional column, "First Letter". We'll e · tab-twins

baseline L184 → branch L380

```diff
- # We can use a dictionary to apply different aggregation functions to each column during grouping.
+ # babynames_new.head()
+ # ```
```

**Why:** `babynames_new.head()` added to the pane so it has an output to show; the baseline cell printed nothing here.
**Output:** same

<a id="c37"></a>
### C37 · cell 20: Imagine we had an additional column, "First Letter". We'll e · tab-twins

baseline L186 → branch L383

```diff
- # ```{image} images/first.png
- # :alt: Example of how a dataframe is conceptually transformed by group by and the function first().
- # :width: 500
+ # ```text
+ # shape: (5, 3)
+ # ┌──────────┬──────────────┬──────┐
+ # │ Name     ┆ First Letter ┆ Year │
+ # │ ---      ┆ ---          ┆ ---  │
+ # │ str      ┆ str          ┆ i64  │
+ # ╞══════════╪══════════════╪══════╡
+ # │ Mary     ┆ M            ┆ 1910 │
+ # │ Helen    ┆ H            ┆ 1910 │
+ # │ Dorothy  ┆ D            ┆ 1910 │
+ # │ Margaret ┆ M            ┆ 1910 │
+ # │ Frances  ┆ F            ┆ 1910 │
+ # └──────────┴──────────────┴──────┘
```

**Why:** Polars output pane. The baseline text at this position was the prose about `"First Letter"` being constant within a name group, which moved to C39.
**Output:** differs: Polars prints no row index; otherwise identical rows.

<a id="c38"></a>
### C38 · cell 20: Imagine we had an additional column, "First Letter". We'll e · tab-twins

baseline L190 → branch L397

```diff
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # Imagine we had an additional column, "First Letter".
+ # babynames_new_pd = babynames_pd.assign(
+ #     **{"First Letter": babynames_pd["Name"].str[0]}
+ # )[["Name", "First Letter", "Year"]]
+ #
+ # babynames_new_pd.head()
+ # ```
+ #
+ # ```text
+ #        Name First Letter  Year
+ # 0      Mary            M  1910
+ # 1     Helen            H  1910
+ # 2   Dorothy            D  1910
+ # 3  Margaret            M  1910
+ # 4   Frances            F  1910
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** pandas pane. It uses `.assign(**{"First Letter": ...})` rather than `babynames_pd["First Letter"] = ...`, because a twin pane has to be a single expression.
**Output:** differs: the pandas pane carries a `0..4` index column. Same five rows.

<a id="c39"></a>
### C39 · cell 21 [markdown] · mixed · **REVIEW**

baseline L191 → branch L422 · spans code and prose

```diff
- # %%
- babynames_new.groupby("Name").agg({"First Letter":"first", "Year":"max"}).head()
+ # %% [markdown] id="p2-first-letter-explain"
+ # If we form one group per name, `"First Letter"` is identical for every row of the group. Taking the first entry therefore represents the whole group faithfully, while a different column can be aggregated a different way in the same call.
+ 
+ # %% tags=["remove-input", "remove-output"] id="p2-first-letter-agg"
+ babynames_new.group_by("Name").agg(
+     pl.col("First Letter").first(),
+     pl.col("Year").max(),
+ ).sort("Name").head()
```

**Why:** `agg({"First Letter":"first", "Year":"max"})` -> two expressions in one `.agg`. `.sort("Name")` is added because Polars does not guarantee group order and the committed table is read row by row in the prose.
**Verdict:** necessary

<a id="c40"></a>
### C40 · cell 23 [markdown] · tab-twins

baseline L195 → branch L432 · spans code and prose

```diff
+ # <!-- tab-twins:begin pl.col("First Letter").first(), -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # babynames_new.group_by("Name").agg(
+ #     pl.col("First Letter").first(),
+ #     pl.col("Year").max(),
+ # ).sort("Name").head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 3)
+ # ┌─────────┬──────────────┬──────┐
+ # │ Name    ┆ First Letter ┆ Year │
+ # │ ---     ┆ ---          ┆ ---  │
+ # │ str     ┆ str          ┆ i64  │
+ # ╞═════════╪══════════════╪══════╡
+ # │ Aadan   ┆ A            ┆ 2014 │
+ # │ Aadarsh ┆ A            ┆ 2019 │
+ # │ Aaden   ┆ A            ┆ 2020 │
+ # │ Aadhav  ┆ A            ┆ 2019 │
+ # │ Aadhini ┆ A            ┆ 2022 │
+ # └─────────┴──────────────┴──────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_new_pd.groupby("Name").agg(
+ #     **{"First Letter": ("First Letter", "first"), "Year": ("Year", "max")}
+ # ).sort_index().head()
+ # ```
+ #
+ # ```text
+ #         First Letter  Year
+ # Name
+ # Aadan              A  2014
+ # Aadarsh            A  2019
+ … 215 more lines
```

**Why:** Comparison pane for the two-expression `.agg`. The pandas pane needs named-agg (`**{"First Letter": ("First Letter", "first"), ...}`) to keep the column names that Polars gets for free.
**Output:** same values on both panes; pandas indexes by `Name`, Polars keeps it as a column.

<a id="c41"></a>
### C41 · cell 36: Plotting Birth Counts · prose · **REVIEW**

baseline L197 → branch L689

```diff
- # Let's use `.agg` to find the total number of babies born in each year. Recall that using `.agg` with `.groupby()` follows the format: `df.groupby(column_name).agg(aggregation_function)`. The line of code below gives us the total number of babies born in each year.
+ # We already have the total number of babies born in each year in `babies_by_year`, sorted by year. Here's an illustration of how we got there:
+ #
+ # ```{image} images/aggregation.png
+ # :alt: A table split into groups, each group reduced by an aggregation to a single value, and the values collected into one summary table.
+ # :width: 600
+ # ```
+ #
+ # Plotting that table tells an interesting story.
```

**Why:** The rewrite computes `babies_by_year` far earlier (C126), so this section no longer introduces the aggregation -- it points back at it. The `aggregation.png` figure moved up here from below.
**Verdict:** optional
**Minimal alternative:** Recompute the total here as the baseline did, and leave the figure in its original position.

<a id="c42"></a>
### C42 · cell 36: Plotting Birth Counts · dropdown

baseline L202 → branch L701 · mirror of the next code cell (hard rule 3)

```diff
- # babynames.groupby("Year")[["Count"]].agg(sum).head(5)
- # # Alternative 1
- # # babynames.groupby("Year")[["Count"]].sum()
- # # Alternative 2
- # # babynames.groupby("Year").sum(numeric_only=True)
+ # #| fig-alt: A line plot of total California births per year from 1910 to 2022. The line climbs steeply through the century to a peak above 550,000 births around 1990, then declines to roughly 360,000 by 2022.
+ # fig = px.line(babies_by_year, x="Year", y="Count")
+ # fig.update_layout(font_size=18, autosize=False, width=700, height=400)
+ # fig
```

**Why:** The dropdown used to mirror a `groupby(...).agg(sum)` cell with two commented alternatives. The code cell in this position is now the total-births figure, so the mirror moved with it, `fig-alt` line included.
**Output:** same -- verified: the dropdown's fenced block is byte-identical to `p2-plot-births`.

<a id="c43"></a>
### C43 · cell 37 [code] · code

baseline L210 → branch L708

```diff
- # %% tags=["remove-input"]
- babynames.groupby("Year")[["Count"]].agg("sum").head(5)
- # Alternative 1
- # babynames.groupby("Year")[["Count"]].sum()
- # Alternative 2
- # babynames.groupby("Year").sum(numeric_only=True)
+ # %% tags=["remove-input"] id="p2-plot-births"
+ #| fig-alt: A line plot of total California births per year from 1910 to 2022. The line climbs steeply through the century to a peak above 550,000 births around 1990, then declines to roughly 360,000 by 2022.
+ fig = px.line(babies_by_year, x="Year", y="Count")
+ fig.update_layout(font_size=18, autosize=False, width=700, height=400)
+ fig
```

**Why:** The `groupby("Year")[["Count"]].agg("sum")` cell and its two commented alternatives (`.sum()`, `.sum(numeric_only=True)`) are replaced by the plotly figure the baseline drew further down. `numeric_only=` has no Polars counterpart worth teaching, and the figure needs `babies_by_year`, which now exists earlier.
**Output:** differs: a plotly line figure replaces a five-row table at this position. The figure is committed as `application/vnd.plotly.v1+json` and the cell is `remove-input` only, so it renders.

<a id="c44"></a>
### C44 · cell 38 [markdown] · prose · **REVIEW**

baseline L217 → branch L714

```diff
- # %% [markdown]
- # Here's an illustration of the process:
+ # %% [markdown] id="p2-plot-warning"
+ # **A word of warning**: we made an enormous assumption when we decided to use this dataset to estimate birth rate. According to [this article from the Legislative Analyst's Office](https://lao.ca.gov/LAOEconTax/Article/Detail/691), the true number of babies born in California in 2020 was 421,275. Our table shows 362,882 for that year — what happened?
```

**Why:** The birth-rate warning moved up from the baseline's position below the Summary section so that it sits under the figure it is about. Its number was re-verified: `babies_by_year` gives **362,882** for 2020 against the LAO's 421,275 (checked live, polars 1.43.1).
**Verdict:** optional
**Minimal alternative:** Leave the warning where the baseline had it; only the figure's position forced the question.

<a id="c45"></a>
### C45 · cell 38: Summary of `group_by()` · prose · **REVIEW**

baseline L220 → branch L717

```diff
- # ```{image} images/aggregation.png
- # :alt: Conceptual illustration of how a dataframe is transformed by groupby and aggregation.
+ # ### Summary of `group_by()`
+ #
+ # A grouping operation involves some combination of **splitting a `DataFrame` into grouped sub-frames**, **applying a function**, and **combining the results**.
+ #
+ # For the code `babynames.group_by("Year").agg(pl.col("Count").sum())`, Polars:
+ #
+ # - **Splits** `babynames` into sub-`DataFrame`s whose rows all belong to the same year.
+ # - **Applies** the expression `pl.col("Count").sum()` to each sub-`DataFrame`.
+ # - **Combines** the results into a single `DataFrame` with one row per year: the year, and its total.
+ #
+ # ```{image} images/groupby_demo.png
+ # :alt: A table split into sub-tables by key, a function applied to each sub-table, and the single-row results combined into one output table.
```

**Why:** Split/apply/combine restated for the expression model. The baseline's third bullet -- "**Combines** the results of `sum` into a single `DataFrame`, indexed by `year`" -- could not survive, and "applies the `sum` function to each column" is wrong for an `.agg` that names one column.
**Verdict:** necessary

<a id="c46"></a>
### C46 · cell 38: Ratio to Peak: A Metric of Our Own · tab-twins

baseline L225 → branch L732 · spans code and prose

```diff
- # Plotting the `DataFrame` we obtain tells an interesting story.
+ # ## Ratio to Peak: A Metric of Our Own
+ #
+ # The aggregations above are all built in. Nothing stops us from inventing our own, because an aggregation is just an expression that ends in a single value per group.
+ #
+ # Say we want to find the name with sex "F" that has fallen furthest out of favor in California. We need a definition of "fallen out of favor" before we can compute anything, so let's define one: the **ratio to peak** (RTP) of a name is the number of babies given that name in the most recent year it appears, divided by the largest number given that name in *any* year. A name at its all-time peak has an RTP of 1; a name that has all but vanished has an RTP near 0.
+ #
+ # Let's work it out for one name first. We start by narrowing `babynames` to sex "F" and sorting by year, so that rows run from oldest to most recent.
+ 
+ # %% tags=["remove-input", "remove-output"] id="p2-f-babynames"
+ f_babynames = babynames.filter(pl.col("Sex") == "F").sort("Year")
+ f_babynames.head()
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin f_babynames = babynames.filter(pl.col("Sex") == "F").sort("Year") -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # f_babynames = babynames.filter(pl.col("Sex") == "F").sort("Year")
+ # f_babynames.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 5)
+ # ┌───────┬─────┬──────┬──────────┬───────┐
+ # │ State ┆ Sex ┆ Year ┆ Name     ┆ Count │
+ # │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   │
+ # │ str   ┆ str ┆ i64  ┆ str      ┆ i64   │
+ # ╞═══════╪═════╪══════╪══════════╪═══════╡
+ # │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   │
+ # │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   │
+ # │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   │
+ # │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   │
+ # │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   │
+ # └───────┴─────┴──────┴──────────┴───────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ … 278 more lines
```

**Why:** The Ratio to Peak section rewritten. The code change is `f_babynames[...]` / `sort_values` -> `.filter(...)` / `.sort("Year")`. **The prose change fixes a pre-existing defect**: the baseline defined RTP as "the ratio of babies born with a given name in 2022 to the maximum", while its code computed `series.iloc[-1] / max(series)` -- the *last year the name appears*. Verified live: 10,080 of the 13,782 names in `f_babynames` last appear in a year other than 2022 (Debra's is 2016), so the baseline sentence was false for 73% of the table. The new definition says "the most recent year it appears", which is what the code does. Not recorded in CONTRADICTIONS.md.
**Output:** differs: `f_babynames.head()` is now printed, which the baseline never showed. The RTP values downstream are unchanged.

<a id="c47"></a>
### C47 · cell 53 [markdown] · dropdown

baseline L230 → branch L1054 · mirror of the next code cell (hard rule 3)

```diff
- # import plotly.express as px
- # puzzle2 = babynames.groupby("Year")[["Count"]].agg("sum")
- # px.line(puzzle2, y = "Count")
+ # #| fig-alt: A line plot of the number of babies named Debra born in California each year. The line rises to a peak of nearly 4,000 in the mid-1950s, falls steadily after 1960, and is indistinguishable from zero on this scale by the 1990s.
+ # fig = px.line(f_babynames.filter(pl.col("Name") == "Debra"), x="Year", y="Count")
+ # fig.update_layout(font_size=18, autosize=False, width=1000, height=400)
+ # fig
```

**Why:** Mirror of the Debra figure cell, which replaced a `groupby("Year").agg("sum")` plot in this position.
**Output:** same -- verified byte-identical to `p2-plot-debra`.

<a id="c48"></a>
### C48 · cell 54 [code] · mixed · **REVIEW**

baseline L236 → branch L1061 · spans code and prose

```diff
- # %% tags=["remove-input"]
- import plotly.express as px
- puzzle2 = babynames.groupby("Year")[["Count"]].agg("sum")
- px.line(puzzle2, y = "Count")
+ # %% tags=["remove-input"] id="p2-plot-debra"
+ #| fig-alt: A line plot of the number of babies named Debra born in California each year. The line rises to a peak of nearly 4,000 in the mid-1950s, falls steadily after 1960, and is indistinguishable from zero on this scale by the 1990s.
+ fig = px.line(f_babynames.filter(pl.col("Name") == "Debra"), x="Year", y="Count")
+ fig.update_layout(font_size=18, autosize=False, width=1000, height=400)
+ fig
+ 
+ # %% [markdown] id="p2-top10-intro"
+ # The names are an ordinary column of `rtp_table`, so we can read the ten biggest fallers straight out of it.
+ 
+ # %% tags=["remove-input", "remove-output"] id="p2-top10"
+ top10 = rtp_table.sort("Count RTP").head(10)["Name"].to_list()
+ top10
```

**Why:** `import plotly.express as px` is dropped because `px` is now imported once at the top of the chapter (the baseline imported it twice, mid-chapter). `f_babynames[f_babynames["Name"] == "Debra"]` -> `.filter(...)`. The `top10` cell is new in this position because `rtp_table` keeps `Name` as an ordinary column instead of an index, so the list is read off a column rather than off `.index`.
**Verdict:** necessary

<a id="c49"></a>
### C49 · cell 57 [markdown] · tab-twins

baseline L242 → branch L1075

```diff
- # **A word of warning**: we made an enormous assumption when we decided to use this dataset to estimate birth rate. According to [this article from the Legislative Analyst's Office](https://lao.ca.gov/LAOEconTax/Article/Detail/691), the true number of babies born in California in 2020 was 421,275. However, our plot shows 362,882 babies —— what happened?
- #
- # ### Summary of the `.groupby()` Function
- #
- # A `groupby` operation involves some combination of **splitting a `DataFrame` into grouped subframes**, **applying a function**, and **combining the results**.
- #
- # For some arbitrary `DataFrame` `df` below, the code `df.groupby("year").agg(sum)` does the following:
- #
- # - **Splits** the `DataFrame` into sub-`DataFrame`s with rows belonging to the same year.
- # - **Applies** the `sum` function to each column of each sub-`DataFrame`.
- # - **Combines** the results of `sum` into a single `DataFrame`, indexed by `year`.
- #
- # ```{image} images/groupby_demo.png
- # :alt: Demonstration of what happens when groupby and aggregation is applied to a dataframe.
- # :width: 600
+ # <!-- tab-twins:begin top10 = rtp_table.sort("Count RTP").head(10)["Name"].to_list() -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # top10 = rtp_table.sort("Count RTP").head(10)["Name"].to_list()
+ # top10
```

**Why:** The baseline's Summary-of-groupby block stood here; the section was moved up (C45) and the tab-set for the top-10 list takes its place.
**Output:** same ten names on both panes.

<a id="c50"></a>
### C50 · cell 57 [markdown] · tab-twins

baseline L259 → branch L1084

```diff
- # ### Revisiting the `.agg()` Function
+ # ```text
+ # ['Debra',
+ #  'Debbie',
+ #  'Carol',
+ #  'Tammy',
+ #  'Susan',
+ #  'Cheryl',
+ #  'Shannon',
+ #  'Tina',
+ #  'Michele',
+ #  'Terri']
+ # ```
+ # ::::
```

**Why:** Polars output pane: a plain Python `list`.
**Output:** differs from the baseline's `Index` object; the ten names and their order are identical.

<a id="c51"></a>
### C51 · cell 57 [markdown] · tab-twins

baseline L261 → branch L1098 · spans code and prose

```diff
- # `.agg()` can take in any function that aggregates several values into one summary value. Some commonly-used aggregation functions can even be called directly, without explicit use of `.agg()`. For example, we can call `.mean()` on `.groupby()`:
- #
- #     babynames.groupby("Year").mean().head()
- #
- # We can now put this all into practice. Say we want to find the baby name with sex "F" that has fallen in popularity the most in California. To calculate this, we can first create a metric: "Ratio to Peak" (RTP). The RTP is the ratio of babies born with a given name in 2022 to the *maximum* number of babies born with the name in *any* year.
- #
- # Let's start with calculating this for one baby, "Jennifer".
- 
- # %%
- # We filter by babies with sex "F" and sort by "Year"
- f_babynames = babynames[babynames["Sex"] == "F"]
- f_babynames = f_babynames.sort_values(["Year"])
- 
- # Determine how many Jennifers were born in CA per year
- jenn_counts_series = f_babynames[f_babynames["Name"] == "Jennifer"]["Count"]
- 
- # Determine the max number of Jennifers born in a year and the number born in 2022
- # to calculate RTP
- max_jenn = max(f_babynames[f_babynames["Name"] == "Jennifer"]["Count"])
- curr_jenn = f_babynames[f_babynames["Name"] == "Jennifer"]["Count"].iloc[-1]
- rtp = curr_jenn / max_jenn
- rtp
- 
- 
- # %% [markdown]
- # By creating a function to calculate RTP and applying it to our `DataFrame` by using `.groupby()`, we can easily compute the RTP for all names at once!
- 
- # %%
- def ratio_to_peak(series):
-     return series.iloc[-1] / max(series)
- 
- #Using .groupby() to apply the function
- rtp_table = f_babynames.groupby("Name")[["Year", "Count"]].agg(ratio_to_peak)
- rtp_table.head()
- 
- # %% [markdown]
- # In the rows shown above, we can see that every row shown has a `Year` value of `1.0`.
- #
- # This is the "**`pandas`**-ification" of logic you saw in Data 8. Much of the logic you've learned in Data 8 will serve you well in Data 100.
- #
- … 7 more lines
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # top10_pd = rtp_pd.sort_values("Count RTP").head(10).index.tolist()
+ # top10_pd
```

**Why:** pandas code pane. `rtp_pd.sort_values("Count RTP").head(10).index.tolist()` reads the names off the index; the Polars half reads them off a column, because `Name` is ordinary data.
**Output:** same ten names.

<a id="c52"></a>
### C52 · cell 57 [markdown] · tab-twins

baseline L310 → branch L1105

```diff
- # We can avoid this issue (and prevent unintentional loss of data) by explicitly selecting column(s) we want to apply our aggregation function to **BEFORE** calling `.agg()`,
- #
- # ### Renaming Columns After Grouping
- #
- # By default, `.groupby` will not rename any aggregated columns. As we can see in the table above, the aggregated column is still named `Count` even though it now represents the RTP. For better readability, we can rename `Count` to `Count RTP`
+ # ```text
+ # ['Debra',
+ #  'Debbie',
+ #  'Carol',
+ #  'Tammy',
+ #  'Susan',
+ #  'Cheryl',
+ #  'Shannon',
+ #  'Tina',
+ #  'Michele',
+ #  'Terri']
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** pandas output pane. Note that this pane and C50 are **byte-identical** -- both print the same Python list. `tab_twins.py` skips identical pairs elsewhere (5 in `polars_1`); this one survives because the *code* differs (`.index.tolist()` vs `["Name"].to_list()`), which is the point being made.
**Output:** same -- identical to the Polars pane.

<a id="c53"></a>
### C53 · cell 58 [markdown] · mixed · **REVIEW**

baseline L316 → branch L1121 · spans code and prose

```diff
- # %%
- rtp_table = rtp_table.rename(columns = {"Count": "Count RTP"})
- rtp_table
- 
- # %% [markdown]
- # ### Some Data Science Payoff
- #
- # By sorting `rtp_table`, we can see the names whose popularity has decreased the most.
- 
- # %%
- rtp_table = rtp_table.rename(columns = {"Count": "Count RTP"})
- rtp_table.sort_values("Count RTP").head()
- 
- # %% [markdown]
- # To visualize the above `DataFrame`, let's look at the line plot below:
+ # %% [markdown] id="p2-top10-plot-intro"
+ # Plotting all ten together shows how much they have in common.
```

**Why:** The baseline had **two** `rename(columns={"Count": "Count RTP"})` cells, the second a redundant repeat of the first. The Polars solution aliases inside `.agg`, so there is nothing to rename and both cells go. The "Renaming Columns After Grouping" section survives as prose in `p2-rtp-explain`, re-aimed at when `.rename` is still the right tool (columns that arrived with the file).
**Verdict:** necessary

<a id="c54"></a>
### C54 · cell 58 [markdown] · dropdown

baseline L335 → branch L1127 · mirror of the next code cell (hard rule 3)

```diff
- # import plotly.express as px
- # px.line(f_babynames[f_babynames["Name"] == "Debra"], x = "Year", y = "Count")
+ # #| fig-alt: Ten line plots on shared axes, one per name. Every line rises to a peak somewhere between the late 1940s and 1970 and then falls away to near zero, with Debra and Susan reaching the highest peaks at just under 4,000 babies a year.
+ # fig = px.line(
+ #     f_babynames.filter(pl.col("Name").is_in(top10)),
+ #     x="Year",
+ #     y="Count",
+ #     color="Name",
+ # )
+ # fig.update_layout(font_size=18, autosize=False, width=1000, height=400)
+ # fig
```

**Why:** Mirror of the ten-name figure cell.
**Output:** same -- verified byte-identical to `p2-plot-top10`.

<a id="c55"></a>
### C55 · cell 59 [code] · code

baseline L340 → branch L1139

```diff
- # %% tags=["remove-input"]
- import plotly.express as px
- px.line(f_babynames[f_babynames["Name"] == "Debra"], x = "Year", y = "Count")
+ # %% tags=["remove-input"] id="p2-plot-top10"
+ #| fig-alt: Ten line plots on shared axes, one per name. Every line rises to a peak somewhere between the late 1940s and 1970 and then falls away to near zero, with Debra and Susan reaching the highest peaks at just under 4,000 babies a year.
+ fig = px.line(
+     f_babynames.filter(pl.col("Name").is_in(top10)),
+     x="Year",
+     y="Count",
+     color="Name",
+ )
+ fig.update_layout(font_size=18, autosize=False, width=1000, height=400)
+ fig
```

**Why:** The single-name Debra plot is replaced by the ten-name plot that the baseline drew in a later cell, and `.isin(top10)` becomes `pl.col("Name").is_in(top10)`. `top10` is a `list`, not an `Index`, which also avoids the `is_in`-with-a-Series ambiguity warning Polars 1.43 emits.
**Output:** differs: ten coloured series instead of one. The `import plotly.express as px` line is gone -- hoisted to the top cell.

<a id="c56"></a>
### C56 · cell 60 [markdown] · mixed · **REVIEW**

baseline L344 → branch L1150 · spans code and prose

```diff
- # %% [markdown]
- # We can get the list of the top 10 names and then plot popularity with the following code:
- 
- # %%
- top10 = rtp_table.sort_values("Count RTP").head(10).index
- px.line(
-     f_babynames[f_babynames["Name"].isin(top10)],
-     x = "Year",
-     y = "Count",
-     color = "Name"
- )
- 
- # %% [markdown]
- # As a quick exercise, consider what code would compute the total number of babies with each name.
+ # %% [markdown] id="p2-filter-intro"
+ # ## Filtering by Group
+ #
+ # Aggregation answers questions of the form "one number per group". A different kind of question asks for the *rows themselves*, chosen by a property of the group they belong to: all the elections held in a close year, all the names that appeared in at least ten different years.
+ #
+ # We'll switch to the `elections` dataset for this.
```

**Why:** The baseline's closing exercise ("consider what code would compute the total number of babies with each name") was a repeat of the `groupby.agg("sum")` already shown, and is dropped. The new section opener introduces filtering by group, which in Polars is `.over()` -- a different construct from `groupby().filter(lambda)`, not a rename of it.
**Verdict:** necessary

<a id="c57"></a>
### C57 · cell 60: Filtering by Group · dropdown

baseline L362 → branch L1160 · spans code and prose; mirror of the next code cell (hard rule 3)

```diff
- # babynames.groupby("Name")[["Count"]].agg("sum").head()
- # # alternative solution:
- # # babynames.groupby("Name")[["Count"]].sum()
- # ```
- # ````
- 
- # %% tags=["remove-input"]
- babynames.groupby("Name")[["Count"]].agg("sum").head()
- # alternative solution:
- # babynames.groupby("Name")[["Count"]].sum()
- 
- # %% [markdown]
- # ## `.groupby()`, Continued
- #
- #
- # We'll work with the `elections` `DataFrame` again.
- #
- # ````{dropdown} Click to see the code
- # :open: false
- # ```python
- # import pandas as pd
- # import numpy as np
- #
- # elections = pd.read_csv("data/elections.csv")
+ # elections = pl.read_csv("data/elections.csv")
```

**Why:** `pd.read_csv` -> `pl.read_csv`, and the two-line `import pandas`/`import numpy` preamble is dropped from the dropdown because the chapter imports once at the top.
**Output:** same -- verified: the dropdown's fenced block is byte-identical to `p2-load-elections`.

<a id="c58"></a>
### C58 · cell 61 [code] · code

baseline L390 → branch L1165

```diff
- # %% tags=["remove-input"]
- import pandas as pd
- import numpy as np
- 
- elections = pd.read_csv("data/elections.csv")
+ # %% tags=["remove-input", "remove-output"] id="p2-load-elections"
+ elections = pl.read_csv("data/elections.csv")
```

**Why:** Same change in the cell the dropdown mirrors. The cell also gained `remove-output`; per CONVERSIONS, `p2-load-elections` had been rendering both its table and its tab pane, showing the reader the same table twice.
**Output:** differs: Polars repr -- see C142. The 187 rows are identical.

<a id="c59"></a>
### C59 · cell 62 [markdown] · tab-twins

baseline L398 → branch L1170

```diff
- # ### Raw `GroupBy` Objects
+ # <!-- tab-twins:begin elections = pl.read_csv("data/elections.csv") elections.head(5) -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # elections = pl.read_csv("data/elections.csv")
+ # elections.head(5)
+ # ```
```

**Why:** Comparison pane for the elections load.
**Output:** same 187-row frame both sides.

<a id="c60"></a>
### C60 · cell 62 [markdown] · tab-twins

baseline L400 → branch L1179

```diff
- # The result of `groupby` applied to a `DataFrame` is a `DataFrameGroupBy` object, **not** a `DataFrame`.
+ # ```text
+ # shape: (5, 6)
+ # ┌──────┬───────────────────┬───────────────────────┬──────────────┬────────┬───────────┐
+ # │ Year ┆ Candidate         ┆ Party                 ┆ Popular vote ┆ Result ┆ %         │
+ # │ ---  ┆ ---               ┆ ---                   ┆ ---          ┆ ---    ┆ ---       │
+ # │ i64  ┆ str               ┆ str                   ┆ i64          ┆ str    ┆ f64       │
+ # ╞══════╪═══════════════════╪═══════════════════════╪══════════════╪════════╪═══════════╡
+ # │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republican ┆ 151271       ┆ loss   ┆ 57.210122 │
+ # │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican ┆ 113142       ┆ win    ┆ 42.789878 │
+ # │ 1828 ┆ Andrew Jackson    ┆ Democratic            ┆ 642806       ┆ win    ┆ 56.203927 │
+ # │ 1828 ┆ John Quincy Adams ┆ National Republican   ┆ 500897       ┆ loss   ┆ 43.796073 │
+ # │ 1832 ┆ Andrew Jackson    ┆ Democratic            ┆ 702735       ┆ win    ┆ 54.574789 │
+ # └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # elections_pd = pd.read_csv("data/elections.csv")
+ # elections_pd.head(5)
+ # ```
+ #
+ # ```text
+ #    Year          Candidate  ... Result          %
+ # 0  1824     Andrew Jackson  ...   loss  57.210122
+ # 1  1824  John Quincy Adams  ...    win  42.789878
+ # 2  1828     Andrew Jackson  ...    win  56.203927
+ # 3  1828  John Quincy Adams  ...   loss  43.796073
+ # 4  1832     Andrew Jackson  ...    win  54.574789
+ #
+ # [5 rows x 6 columns]
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** Output panes.
**Output:** differs: the pandas pane elides four of the six columns behind `...` and prints `[5 rows x 6 columns]`; the Polars pane shows all six with their dtypes.

<a id="c61"></a>
### C61 · cell 63 [markdown] · mixed · **REVIEW**

baseline L402 → branch L1216 · spans code and prose

```diff
- # %%
- grouped_by_year = elections.groupby("Year")
- type(grouped_by_year)
- 
- # %% [markdown]
- # There are several ways to look into `DataFrameGroupBy` objects:
- 
- # %%
- grouped_by_party = elections.groupby("Party")
- grouped_by_party.groups
- 
- # %%
- grouped_by_party.get_group("Socialist")
- 
- # %% [markdown]
- # ### Other `GroupBy` Methods
+ # %% [markdown] id="p2-over-explain"
+ # The tool for this job is `.over` [(documentation)](https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.over.html), which computes an aggregate **within each group** and hands the group's answer back to every row of that group:
```

**Why:** The `DataFrameGroupBy` tour -- `type()`, `.groups`, `get_group` -- is replaced here by the `.over` explanation. `.groups` returns a dict of row *labels*, which Polars has none of. The tour is not lost: it reappears later as `p2-groupby-type` / `p2-groupby-dict` / `p2-groupby-socialist` in a "Raw `GroupBy` Objects" section, rewritten around `dict(group_by)` and tuple keys.
**Verdict:** necessary

<a id="c62"></a>
### C62 · cell 63 [markdown] · prose · **REVIEW**

baseline L419 → branch L1219

```diff
- # There are many aggregation methods we can use with `.agg`. Some useful options are:
+ # - The aggregate collapses each group to a single value, such as `pl.len()` or `pl.col("c").max()`.
+ # - `.over("key")` computes that value per group, then broadcasts it back across the group's rows.
+ # - Comparing it produces `True` or `False` for every row at once, and `.filter` keeps the rows whose group answered `True`.
```

**Why:** Replaces the baseline's "There are many aggregation methods we can use with `.agg`" lead-in with three bullets describing how `.over` broadcasts a group aggregate back across the group's rows -- the mechanism, which has no pandas counterpart in the baseline text.
**Verdict:** necessary

<a id="c63"></a>
### C63 · cell 63 [markdown] · mixed · **REVIEW**

baseline L421 → branch L1223 · spans code and prose

```diff
- # * `.mean()` [documentation](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.mean.html#pandas.core.groupby.DataFrameGroupBy.mean): creates a new `DataFrame` with the mean value of each group
- # * `.sum()` [documentation](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.sum.html#pandas.core.groupby.DataFrameGroupBy.sum): creates a new `DataFrame` with the sum of each group
- # * `.max()` [documentation](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.max.html#pandas.core.groupby.DataFrameGroupBy.max) and `.min()` [documentation](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.min.html#pandas.core.groupby.DataFrameGroupBy.min): creates a new `DataFrame` with the maximum/minimum value of each group
- # * `.first()` [documentation](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.first.html#pandas.core.groupby.DataFrameGroupBy.first) and `.last() ` [documentation](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.last.html#pandas.core.groupby.DataFrameGroupBy.last): creates a new `DataFrame` with the first/last row in each group
- # * `.head(n)` [documentation](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.head.html) and `.tail(n)` [documentation](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.tail.html): creates a new `DataFrame` with the first/last `n` rows in each group
- # * `.size()` [documentation](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.size.html#pandas.core.groupby.DataFrameGroupBy.size): creates a new **`Series`** with the number of entries in each group
- # * `.count()` [documentation](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.count.html#pandas.core.groupby.DataFrameGroupBy.count): creates a new **`DataFrame`** with the number of entries, excluding missing values.
- #
- # Let's illustrate some examples by creating a `DataFrame` called `df`.
- 
- # %%
- df = pd.DataFrame({'letter':['A','A','B','C','C','C'],
-                    'num':[1,2,3,4,np.nan,4],
-                    'state':[np.nan, 'tx', 'fl', 'hi', np.nan, 'ak']})
- df
- 
- # %% [markdown]
- # Note the slight difference between `.size()` and `.count()`: while `.size()` returns a `Series` and counts the number of entries including the missing values, `.count()` returns a `DataFrame` and counts the number of entries in each column *excluding missing values*.
- 
- # %%
- df.groupby("letter").size()
- 
- # %%
- df.groupby("letter").count()
- 
- # %% [markdown]
- # You might recall that the `value_counts()` function in the previous note does something similar. It turns out `value_counts()` and `groupby.size()` are the same, except `value_counts()` sorts the resulting `Series` in descending order automatically.
- 
- # %%
- df["letter"].value_counts()
- 
- # %% [markdown]
- # These (and other) aggregation functions are so common that `pandas` allows for writing shorthand. Instead of explicitly stating the use of `.agg`, we can call the function directly on the `GroupBy` object.
- #
- # For example, the following are equivalent:
- #
- # - `elections.groupby("Candidate").agg(mean)`
- # - `elections.groupby("Candidate").mean()`
- #
- # There are many other methods that `pandas` supports. You can check them out on the `pandas` [documentation](https://pandas.pydata.org/docs/reference/groupby.html).
- … 16 more lines
+ # Because the rows themselves are returned, and not one summary row per group, a filtered result has the same columns and the same row order as the table it came from.
```

**Why:** The largest single deletion in the chapter: the bulleted list of seven `DataFrameGroupBy` methods with their pandas documentation links, the `df` construction with `np.nan`, the `.size()` vs `.count()` comparison, the `value_counts()` equivalence, and the "`.agg(mean)` is the same as `.mean()`" shorthand paragraph, all collapsed into one sentence. Every documentation link was pandas'; the shorthand equivalence is not a Polars fact. The `df` example and the `.size()`/`.count()`/`value_counts` material are not lost -- they moved to their own section (C131-C134) -- but the method list with links is gone outright.
**Verdict:** questionable
**Minimal alternative:** Keep a Polars-side equivalent of the method list, pointing at the Polars aggregation reference. A reader of the old chapter had one page listing every group aggregation with a link each; the replacement has the list at C23 but without the per-method links.

<a id="c64"></a>
### C64 · cell 63 [markdown] · prose · **REVIEW**

baseline L479 → branch L1226

```diff
- # :alt: Groupby demonstration that shows the original indices are preserved.
+ # :alt: A filter applied to groups, where entire sub-tables are kept or discarded and the surviving rows are returned unchanged.
```

**Why:** As C17: alt text rewritten to describe the drawing. The PNG is unchanged.
**Verdict:** optional
**Minimal alternative:** Keep the baseline alt text.

<a id="c65"></a>
### C65 · cell 63 [markdown] · prose · **REVIEW**

baseline L483 → branch L1230

```diff
- # `sf` refers to subframe or sub-`DataFrame` which are the "mini", grouped sub-`DataFrame`s.
- #
- # To illustrate how this happens, let's go back to the `elections` dataset. Say we want to identify "tight" election years – that is, we want to find all rows that correspond to election years where all candidates in that year won a similar portion of the total vote. Specifically, let's find all rows corresponding to a year where no candidate won more than 45% of the total vote.
- #
- # In other words, we want to:
- #
- # - Find the years where the maximum `%` in that year is less than 45%
- # - Return all `DataFrame` rows that correspond to these years
- #
- # For each year, we need to find the maximum `%` among *all* rows for that year. If this maximum `%` is lower than 45%, we will tell `pandas` to keep all rows corresponding to that year.
+ # Here it is on the small `DataFrame` from earlier: keep every row whose letter appears at least twice.
```

**Why:** `sf` is the name of the lambda's sub-frame argument, and `.over()` takes no lambda, so the explanation has nothing to explain. The tight-election setup that followed it moved down to C71, where the elections example now begins.
**Verdict:** necessary

<a id="c66"></a>
### C66 · cell 64 [code] · code

baseline L494 → branch L1232

```diff
- # %%
- elections.groupby("Year").filter(lambda sf: sf["%"].max() < 45).head(9)
+ # %% tags=["remove-input", "remove-output"] id="p2-over-small"
+ df.filter(pl.len().over("letter") >= 2)
```

**Why:** The reshape hard rule 7 exists for: `elections.groupby("Year").filter(lambda sf: sf["%"].max() < 45)` -> `df.filter(pl.len().over("letter") >= 2)`. A window expression, no lambda. The small `df` is used first so the mechanism is visible before the elections example.
**Output:** differs: this position now shows the five-row small-frame example; the elections result moved to C72.

<a id="c67"></a>
### C67 · cell 65 [markdown] · tab-twins

baseline L498 → branch L1236

```diff
- # What's going on here? In this example, we've defined our filtering function, `func`, to be `lambda sf: sf["%"].max() < 45`. This filtering function will find the maximum `"%"` value among all entries in the grouped sub-`DataFrame`, which we call `sf`. If the maximum value is less than 45, then the filter function will return `True` and all rows in that grouped sub-`DataFrame` will appear in the final output `DataFrame`.
+ # <!-- tab-twins:begin df.filter(pl.len().over("letter") >= 2) -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # df.filter(pl.len().over("letter") >= 2)
+ # ```
```

**Why:** Polars code pane.
**Output:** same rows as the pandas pane.

<a id="c68"></a>
### C68 · cell 65 [markdown] · tab-twins

baseline L500 → branch L1244

```diff
- # Examine the `DataFrame` above. Notice how, in this preview of the first 9 rows, all entries from the years 1860 and 1912 appear. This means that in 1860 and 1912, no candidate in that year won more than 45% of the total vote.
+ # ```text
+ # shape: (5, 3)
+ # ┌────────┬──────┬───────┐
+ # │ letter ┆ num  ┆ state │
+ # │ ---    ┆ ---  ┆ ---   │
+ # │ str    ┆ i64  ┆ str   │
+ # ╞════════╪══════╪═══════╡
+ # │ A      ┆ 1    ┆ null  │
+ # │ A      ┆ 2    ┆ tx    │
+ # │ C      ┆ 4    ┆ hi    │
+ # │ C      ┆ null ┆ null  │
+ # │ C      ┆ 4    ┆ ak    │
+ # └────────┴──────┴───────┘
+ # ```
+ # ::::
```

**Why:** Polars output pane.
**Output:** differs: `num` stays `i64` and missing values print `null`, where pandas widened the column to `float64` to hold `NaN`. Same five rows.

<a id="c69"></a>
### C69 · cell 65 [markdown] · tab-twins

baseline L502 → branch L1260

```diff
- # You may ask: how is the `groupby.filter` procedure different to the boolean filtering we've seen previously? Boolean filtering considers *individual* rows when applying a boolean condition. For example, the code `elections[elections["%"] < 45]` will check the `"%"` value of every single row in `elections`; if it is less than 45, then that row will be kept in the output. `groupby.filter`, in contrast, applies a boolean condition *across* all rows in a group. If not all rows in that group satisfy the condition specified by the filter, the entire group will be discarded in the output.
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # df_pd.groupby("letter").filter(lambda g: len(g) >= 2)
+ # ```
```

**Why:** pandas code pane: `groupby("letter").filter(lambda g: len(g) >= 2)` -- the baseline idiom, correctly paired here.
**Output:** same five rows.

<a id="c70"></a>
### C70 · cell 65 [markdown] · tab-twins

baseline L504 → branch L1266

```diff
- # ### Aggregation with `lambda` Functions
+ # ```text
+ #   letter  num state
+ # 0      A  1.0  None
+ # 1      A  2.0    tx
+ # 3      C  4.0    hi
+ # 4      C  NaN  None
+ # 5      C  4.0    ak
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
+ 
+ # %% [markdown] id="p2-over-elections"
+ # `B` occurs once, so its row is gone; the two `A` rows and all three `C` rows survive, in their original order.
```

**Why:** pandas output pane, plus the sentence reading the result.
**Output:** differs: pandas prints `1.0`/`NaN`/`None` where Polars prints `1`/`null`; the surviving rows and their order are identical.

<a id="c71"></a>
### C71 · cell 66 [markdown] · prose · **REVIEW**

baseline L506 → branch L1281

```diff
- # What if we wish to aggregate our `DataFrame` using a non-standard function – for example, a function of our own design? We can do so by combining `.agg` with `lambda` expressions.
- #
- # Let's first consider a puzzle to jog our memory. We will attempt to find the `Candidate` from each `Party` with the highest `%` of votes.
- #
- # A naive approach may be to group by the `Party` column and aggregate by the maximum.
+ # Now for a real question. We want to identify "tight" election years — years in which no candidate won more than 45% of the popular vote — and see every candidate who ran in them. For each year we need the maximum `%` across all of that year's rows, and then we keep the rows whose year passed the test.
```

**Why:** The baseline's lead-in to `lambda` aggregation is replaced by the tight-election setup moved down from C65. The "no candidate won more than 45%" framing is kept and restated for `.over`.
**Verdict:** necessary

<a id="c72"></a>
### C72 · cell 67 [code] · code

baseline L512 → branch L1283

```diff
- # %%
- elections.groupby("Party").agg("max").head(10)
+ # %% tags=["remove-input", "remove-output"] id="p2-over-elections-code"
+ elections.filter(pl.col("%").max().over("Year") < 45).head(9)
```

**Why:** The puzzle cell that stood here moved down; this position now carries the `.over` filter on `elections`.
**Output:** differs: the tight-election rows (see C144) rather than the puzzle's max-per-column table.

<a id="c73"></a>
### C73 · cell 68 [markdown] · tab-twins

baseline L516 → branch L1287

```diff
- # This approach is clearly wrong – the `DataFrame` claims that Woodrow Wilson won the presidency in 2024.
+ # <!-- tab-twins:begin elections.filter(pl.col("%").max().over("Year") < 45).head(9) -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # elections.filter(pl.col("%").max().over("Year") < 45).head(9)
+ # ```
```

**Why:** Polars code pane.
**Output:** same nine rows as the pandas pane.

<a id="c74"></a>
### C74 · cell 68 [markdown] · tab-twins

baseline L518 → branch L1295 · spans code and prose

```diff
- # Why is this happening? Here, the `max` aggregation function is taken over every column *independently*. Among Democrats, `max` is computing:
+ # ```text
+ # shape: (9, 6)
+ # ┌──────┬──────────────────────┬──────────────────────┬──────────────┬────────┬───────────┐
+ # │ Year ┆ Candidate            ┆ Party                ┆ Popular vote ┆ Result ┆ %         │
+ # │ ---  ┆ ---                  ┆ ---                  ┆ ---          ┆ ---    ┆ ---       │
+ # │ i64  ┆ str                  ┆ str                  ┆ i64          ┆ str    ┆ f64       │
+ # ╞══════╪══════════════════════╪══════════════════════╪══════════════╪════════╪═══════════╡
+ # │ 1860 ┆ Abraham Lincoln      ┆ Republican           ┆ 1855993      ┆ win    ┆ 39.699408 │
+ # │ 1860 ┆ John Bell            ┆ Constitutional Union ┆ 590901       ┆ loss   ┆ 12.639283 │
+ # │ 1860 ┆ John C. Breckinridge ┆ Southern Democratic  ┆ 848019       ┆ loss   ┆ 18.138998 │
+ # │ 1860 ┆ Stephen A. Douglas   ┆ Northern Democratic  ┆ 1380202      ┆ loss   ┆ 29.522311 │
+ # │ 1912 ┆ Eugene V. Debs       ┆ Socialist            ┆ 901551       ┆ loss   ┆ 6.004354  │
+ # │ 1912 ┆ Eugene W. Chafin     ┆ Prohibition          ┆ 208156       ┆ loss   ┆ 1.386325  │
+ # │ 1912 ┆ Theodore Roosevelt   ┆ Progressive          ┆ 4122721      ┆ loss   ┆ 27.457433 │
+ # │ 1912 ┆ William Taft         ┆ Republican           ┆ 3486242      ┆ loss   ┆ 23.218466 │
+ # │ 1912 ┆ Woodrow Wilson       ┆ Democratic           ┆ 6296284      ┆ win    ┆ 41.933422 │
+ # └──────┴──────────────────────┴──────────────────────┴──────────────┴────────┴───────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # elections_pd[
+ #     elections_pd.groupby("Year")["%"].transform("max") < 45
+ # ].head(9)
+ # ```
+ #
+ # ```text
+ #     Year             Candidate  ... Result          %
+ # 23  1860       Abraham Lincoln  ...    win  39.699408
+ # 24  1860             John Bell  ...   loss  12.639283
+ # 25  1860  John C. Breckinridge  ...   loss  18.138998
+ # 26  1860    Stephen A. Douglas  ...   loss  29.522311
+ # 66  1912        Eugene V. Debs  ...   loss   6.004354
+ # 67  1912      Eugene W. Chafin  ...   loss   1.386325
+ # 68  1912    Theodore Roosevelt  ...   loss  27.457433
+ # 69  1912          William Taft  ...   loss  23.218466
+ # 70  1912        Woodrow Wilson  ...    win  41.933422
+ #
+ … 80 more lines
```

**Why:** **The pandas pane is not the pandas the baseline taught.** It uses `elections_pd.groupby("Year")["%"].transform("max") < 45`, which is the closest pandas analogue of `.over()`; the baseline chapter taught `groupby("Year").filter(lambda sf: sf["%"].max() < 45)`. Both are valid pandas returning the same nine rows, but a reader migrating from the old chapter will not recognise the pane as the code they knew.
**Output:** same nine rows (1860 and 1912) on both panes; pandas keeps its 23/24/25... row labels.

<a id="c75"></a>
### C75 · cell 72 [markdown] · prose · **REVIEW**

baseline L521 → branch L1417

```diff
- # - The `Candidate` with the alphabetically "largest" name ("Woodrow Wilson")
- # - The `Result` with the alphabetically "largest" outcome ("win")
+ # - The `Candidate` whose name is alphabetically last ("Woodrow Wilson")
+ # - The largest vote share any Democrat has ever won (61.3%)
```

**Why:** The third bullet was re-aimed from `Result` to `%`. Nothing forced it: the branch's own committed table still carries a `Result` column, and the alphabetical max over {"loss", "win"} is still `"win"`, so the original bullet remains true as written. The swap sharpens the point the paragraph then makes — "three columns, three different elections" — because `"win"` does not name an election while 61.3% does, and the sentence above it was re-pointed at the same number. A teaching improvement, not a conversion requirement.
**Verdict:** optional
**Minimal alternative:** Keep the original third bullet (the `Result` with the alphabetically "largest" outcome) and leave the sentence above citing the presidency rather than the vote share.

<a id="c76"></a>
### C76 · cell 72 [markdown] · prose · **REVIEW**

baseline L524 → branch L1420

```diff
- # Instead, let's try a different approach. We will:
+ # Three columns, three different elections, and a row that describes none of them. Naming the columns you want aggregated is a good habit, but the deeper problem is that we asked the wrong question: we do not want the maximum of each column, we want *the row* in which one column reaches its maximum.
```

**Why:** The baseline enumerated what `max` computed for each column. The replacement names the diagnosis instead: the question was wrong, not the column selection -- we want the row in which one column reaches its maximum, not the maximum of each column. Same lesson, different route to it.
**Verdict:** optional
**Minimal alternative:** Keep "Instead, let's try a different approach:" and the baseline bullets.

<a id="c77"></a>
### C77 · cell 72 [markdown] · prose · **REVIEW**

baseline L526 → branch L1422

```diff
- # 1. Sort the `DataFrame` so that rows are in descending order of `%`
- # 2. Group by `Party` and select the first row of each sub-`DataFrame`
+ # So let's take a different approach:
```

**Why:** The numbered list moved to C78; this cell keeps only the transition sentence.
**Verdict:** optional
**Minimal alternative:** Revert -- the reflow is cosmetic.

<a id="c78"></a>
### C78 · cell 72 [markdown] · prose · **REVIEW**

baseline L529 → branch L1424

```diff
- # While it may seem unintuitive, sorting `elections` by descending order of `%` is extremely helpful. If we then group by `Party`, the first row of each `GroupBy` object will contain information about the `Candidate` with the highest voter `%`.
+ # 1. Sort the `DataFrame` so that rows are in descending order of `%`.
+ # 2. Group by `Party` and take the first row of each group.
+ #
+ # Sorting first may seem indirect, but it puts the answer within reach: if the whole table runs from largest `%` to smallest, then within any group the first row is that group's best result.
```

**Why:** The baseline's numbered list and its justification paragraph were merged into one block and the justification reworded ("may seem unintuitive" -> "may seem indirect").
**Verdict:** optional
**Minimal alternative:** Keep both baseline paragraphs; nothing in them is pandas-specific.

<a id="c79"></a>
### C79 · cell 73 [code] · code

baseline L531 → branch L1429

```diff
- # %%
- elections_sorted_by_percent = elections.sort_values("%", ascending=False)
+ # %% tags=["remove-input", "remove-output"] id="p2-puzzle-sorted"
+ elections_sorted_by_percent = elections.sort("%", descending=True)
```

**Why:** `sort_values("%", ascending=False)` -> `sort("%", descending=True)` -- the inverted-sense rename (hard rule 8).
**Output:** differs: repr only. `%` has no nulls (verified), so the Polars nulls-first behaviour does not bite the `.head(5)` here.

<a id="c80"></a>
### C80 · cell 74 [markdown] · tab-twins

baseline L535 → branch L1433 · spans code and prose

```diff
- # %%
- elections_sorted_by_percent.groupby("Party").agg(lambda x : x.iloc[0]).head(10)
+ # %% [markdown]
+ # <!-- tab-twins:begin elections_sorted_by_percent = elections.sort("%", descending=True) -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # elections_sorted_by_percent = elections.sort("%", descending=True)
+ # elections_sorted_by_percent.head(5)
+ # ```
+ #
+ # ```text
+ # shape: (5, 6)
+ # ┌──────┬────────────────────┬────────────┬──────────────┬────────┬───────────┐
+ # │ Year ┆ Candidate          ┆ Party      ┆ Popular vote ┆ Result ┆ %         │
+ # │ ---  ┆ ---                ┆ ---        ┆ ---          ┆ ---    ┆ ---       │
+ # │ i64  ┆ str                ┆ str        ┆ i64          ┆ str    ┆ f64       │
+ # ╞══════╪════════════════════╪════════════╪══════════════╪════════╪═══════════╡
+ # │ 1964 ┆ Lyndon Johnson     ┆ Democratic ┆ 43127041     ┆ win    ┆ 61.344703 │
+ # │ 1936 ┆ Franklin Roosevelt ┆ Democratic ┆ 27752648     ┆ win    ┆ 60.978107 │
+ # │ 1972 ┆ Richard Nixon      ┆ Republican ┆ 47168710     ┆ win    ┆ 60.907806 │
+ # │ 1920 ┆ Warren Harding     ┆ Republican ┆ 16144093     ┆ win    ┆ 60.574501 │
+ # │ 1984 ┆ Ronald Reagan      ┆ Republican ┆ 54455472     ┆ win    ┆ 59.023326 │
+ # └──────┴────────────────────┴────────────┴──────────────┴────────┴───────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # elections_sorted_pd = elections_pd.sort_values("%", ascending=False)
+ # elections_sorted_pd.head(5)
+ # ```
+ #
+ # ```text
+ #      Year           Candidate       Party  Popular vote Result          %
+ # 114  1964      Lyndon Johnson  Democratic      43127041    win  61.344703
+ # 91   1936  Franklin Roosevelt  Democratic      27752648    win  60.978107
+ # 120  1972       Richard Nixon  Republican      47168710    win  60.907806
+ # 79   1920      Warren Harding  Republican      16144093    win  60.574501
+ # 133  1984       Ronald Reagan  Republican      54455472    win  59.023326
+ … 4 more lines
```

**Why:** Comparison pane for the sort. The Polars pane adds `.head(5)` so the sort has something to show; the baseline cell assigned without printing.
**Output:** differs: pandas keeps the original row labels (114, 91, 120, 79, 133), Polars has none. Same five rows.

<a id="c81"></a>
### C81 · cell 75 [code] · code

baseline L538 → branch L1478

```diff
- # Equivalent to the below code
- # elections_sorted_by_percent.groupby("Party").agg('first').head(10)
+ # %% tags=["remove-input", "remove-output"] id="p2-puzzle-attempt2"
+ best_per_party = elections_sorted_by_percent.group_by("Party", maintain_order=True).head(1)
+ best_per_party.head(10)
```

**Why:** `groupby("Party").agg(lambda x : x.iloc[0])` -> `group_by("Party", maintain_order=True).head(1)`. Polars preserves row order *within* a group, so `head(1)` after a global sort is the whole trick; the lambda has no form inside a Polars `.agg`, which is element-wise.
**Output:** differs: row order -- see C147. The parties come out in order of their best result, not alphabetically.

<a id="c82"></a>
### C82 · cell 76 [markdown] · tab-twins

baseline L542 → branch L1483

```diff
+ # <!-- tab-twins:begin best_per_party = elections_sorted_by_percent.group_by("Party", maintain_order=True).head(1) -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # best_per_party = elections_sorted_by_percent.group_by("Party", maintain_order=True).head(1)
+ # best_per_party.head(10)
+ # ```
+ #
+ # ```text
+ # shape: (10, 6)
+ # ┌───────────────────────┬──────┬────────────────────────┬──────────────┬────────┬───────────┐
+ # │ Party                 ┆ Year ┆ Candidate              ┆ Popular vote ┆ Result ┆ %         │
+ # │ ---                   ┆ ---  ┆ ---                    ┆ ---          ┆ ---    ┆ ---       │
+ # │ str                   ┆ i64  ┆ str                    ┆ i64          ┆ str    ┆ f64       │
+ # ╞═══════════════════════╪══════╪════════════════════════╪══════════════╪════════╪═══════════╡
+ # │ Democratic            ┆ 1964 ┆ Lyndon Johnson         ┆ 43127041     ┆ win    ┆ 61.344703 │
+ # │ Republican            ┆ 1972 ┆ Richard Nixon          ┆ 47168710     ┆ win    ┆ 60.907806 │
+ # │ Democratic-Republican ┆ 1824 ┆ Andrew Jackson         ┆ 151271       ┆ loss   ┆ 57.210122 │
+ # │ National Union        ┆ 1864 ┆ Abraham Lincoln        ┆ 2211317      ┆ win    ┆ 54.951512 │
+ # │ Whig                  ┆ 1840 ┆ William Henry Harrison ┆ 1275583      ┆ win    ┆ 53.051213 │
+ # │ Liberal Republican    ┆ 1872 ┆ Horace Greeley         ┆ 2834761      ┆ loss   ┆ 44.071406 │
+ # │ National Republican   ┆ 1828 ┆ John Quincy Adams      ┆ 500897       ┆ loss   ┆ 43.796073 │
+ # │ Northern Democratic   ┆ 1860 ┆ Stephen A. Douglas     ┆ 1380202      ┆ loss   ┆ 29.522311 │
+ # │ Progressive           ┆ 1912 ┆ Theodore Roosevelt     ┆ 4122721      ┆ loss   ┆ 27.457433 │
+ # │ American              ┆ 1856 ┆ Millard Fillmore       ┆ 873053       ┆ loss   ┆ 21.554001 │
+ # └───────────────────────┴──────┴────────────────────────┴──────────────┴────────┴───────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # best_per_party_pd = elections_sorted_pd.groupby("Party", sort=False).head(1)
+ # best_per_party_pd.head(10)
+ # ```
+ #
+ # ```text
+ #      Year               Candidate  ... Result          %
+ # 114  1964          Lyndon Johnson  ...    win  61.344703
+ … 17 more lines
```

**Why:** **The pandas pane is not the pandas the baseline taught**, and its output is not what the baseline published. It uses `groupby("Party", sort=False).head(1)` so that the pane's row order matches Polars'; the baseline used `agg(lambda x: x.iloc[0])`, which sorts group keys and published an alphabetically ordered table (American, American Independent, Anti-Masonic, ...).
**Output:** differs from the baseline's committed output in row order, though not in content: the same 37 party rows, ranked rather than alphabetical.

<a id="c83"></a>
### C83 · cell 77 [markdown] · prose · **REVIEW**

baseline L545 → branch L1543

```diff
- # :alt: In this demo, a dataframe first is sorted, then grouped, and the first item of each group is chosen (ultimately yielding the largest values per group).
+ # :alt: A table sorted in descending order, then grouped, with the first row of each group selected to give the largest value per group.
```

**Why:** As C17: alt text rewritten. The PNG is unchanged.
**Verdict:** optional
**Minimal alternative:** Keep the baseline alt text.

<a id="c84"></a>
### C84 · cell 77 [markdown] · prose · **REVIEW**

baseline L549 → branch L1547

```diff
- # Notice how our code correctly determines that Lyndon Johnson from the Democratic Party has the highest voter `%`.
+ # One row per party, 37 in all, and each one is a real election. Lyndon Johnson's 1964 landslide is the best Democratic result on record, and Richard Nixon's 1972 win the best Republican one. Two properties of `.group_by` are doing the work: rows keep their relative order inside a group, so "first row" means "highest `%`", and `maintain_order=True` orders the parties by where their best result appeared, which turns the output into a ranking.
```

**Why:** The baseline noted only that Lyndon Johnson came out on top. The replacement names the two Polars guarantees the result depends on -- within-group row order is preserved, and `maintain_order=True` orders the groups -- because neither is a default and a reader who omits the keyword gets a different table. "37 in all" verified live: `elections` has 187 rows and 37 distinct parties.
**Verdict:** necessary

<a id="c85"></a>
### C85 · cell 77: Alternative Solutions · prose · **REVIEW**

baseline L551 → branch L1549

```diff
- # More generally, `lambda` functions are used to design custom aggregation functions that aren't pre-defined by Python. The input parameter `x` to the `lambda` function is a `GroupBy` object. Therefore, it should make sense why `lambda x : x.iloc[0]` selects the first row in each groupby object.
+ # #### Alternative Solutions
```

**Why:** The baseline sentence explained `lambda x : x.iloc[0]`, which no longer exists in the code. The section heading takes its place.
**Verdict:** necessary

<a id="c86"></a>
### C86 · cell 77: Alternative Solutions · prose · **REVIEW**

baseline L553 → branch L1551

```diff
+ # With a rich toolkit there is usually more than one way to reach an answer, and the options differ in readability, memory use, and speed. Developing a sense for which is better takes practice, and it is worth trying to imagine a second approach whenever your first one feels convoluted.
```

**Why:** Re-authored version of the baseline's tradeoff sentence, which moved here from C87's slot.
**Verdict:** optional
**Minimal alternative:** Keep the baseline sentence ("there's a few different ways to approach this problem...") verbatim.

<a id="c87"></a>
### C87 · cell 77: Alternative Solutions · prose · **REVIEW**

baseline L554 → branch L1553

```diff
- # In fact, there's a few different ways to approach this problem. Each approach has different tradeoffs in terms of readability, performance, memory consumption, complexity, etc. We've given a few examples below.
+ # ::: {note}
+ # Understanding these alternatives is not required. They are here to show how differently the same question can be asked.
+ # :::
```

**Why:** The baseline's bold **Note** became a `{note}` directive; the wording is otherwise the baseline's minus "in `pandas`".
**Verdict:** optional
**Minimal alternative:** Keep the bold-**Note** form if course staff would rather not mix admonition styles across the chapter.

<a id="c88"></a>
### C88 · cell 77: Alternative Solutions · prose · **REVIEW**

baseline L556 → branch L1557

```diff
- # **Note**: Understanding these alternative solutions is not required. They are given to demonstrate the vast number of problem-solving approaches in `pandas`.
+ # A row's position is the only handle we have on it, so the first alternative writes those positions into a column with `.with_row_index` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.with_row_index.html), then uses `.arg_max` [(documentation)](https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.arg_max.html) to find where each party's best election sits.
```

**Why:** `elections.loc[elections.groupby('Party')['%'].idxmax()]` has no Polars analog in either half: `idxmax` returns index *labels* and `.loc` looks them up, and there is no index. The positions have to be materialized first, which is what `with_row_index` is for, so the alternative needs an explanation the baseline did not.
**Verdict:** necessary

<a id="c89"></a>
### C89 · cell 78 [code] · code

baseline L558 → branch L1559

```diff
- # %%
- # Using the idxmax function
- best_per_party = elections.loc[elections.groupby('Party')['%'].idxmax()]
- best_per_party.head(5)
- 
- # %%
- # Using the .drop_duplicates function
- best_per_party2 = elections.sort_values('%').drop_duplicates(['Party'], keep='last')
- best_per_party2.head(5)
+ # %% tags=["remove-input", "remove-output"] id="p2-puzzle-alt1a"
+ best_positions = (
+     elections.with_row_index("position")
+     .group_by("Party")
+     .agg(pl.col("position").get(pl.col("%").arg_max()))
+     .sort("Party")
+ )
+ best_positions.head()
```

**Why:** Two baseline cells replaced by one. `elections.loc[elections.groupby('Party')['%'].idxmax()]` -> `with_row_index("position")` + `pl.col("position").get(pl.col("%").arg_max())`, because `idxmax` returns index labels and there is no index. `.sort("Party")` added for a stable published order. The `drop_duplicates` alternative moved to its own cell (C150).
**Output:** differs: an intermediate `(Party, position)` table is printed that the baseline never showed -- the baseline did the lookup inline.

<a id="c90"></a>
### C90 · cell 79 [markdown] · tab-twins

baseline L569 → branch L1569 · spans code and prose

```diff
+ # <!-- tab-twins:begin best_positions = ( -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # best_positions = (
+ #     elections.with_row_index("position")
+ #     .group_by("Party")
+ #     .agg(pl.col("position").get(pl.col("%").arg_max()))
+ #     .sort("Party")
+ # )
+ # best_positions.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 2)
+ # ┌──────────────────────┬──────────┐
+ # │ Party                ┆ position │
+ # │ ---                  ┆ ---      │
+ # │ str                  ┆ u32      │
+ # ╞══════════════════════╪══════════╡
+ # │ American             ┆ 22       │
+ # │ American Independent ┆ 115      │
+ # │ Anti-Masonic         ┆ 6        │
+ # │ Anti-Monopoly        ┆ 38       │
+ # │ Citizens             ┆ 127      │
+ # └──────────────────────┴──────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # best_positions_pd = (
+ #     elections_pd.groupby("Party")["%"].idxmax().sort_index()
+ # )
+ # best_positions_pd.head()
+ # ```
+ #
+ # ```text
+ … 269 more lines
```

**Why:** Comparison pane for the positions table.
**Output:** differs: pandas' `idxmax()` returns a `Series` of index labels named `%`; Polars returns a two-column frame with `u32` positions. The positions themselves match (American 22, Anti-Masonic 6, Anti-Monopoly 38), because the CSV row order is the same on both sides.

<a id="c91"></a>
### C91 · cell 95: `group_by` with Multiple Columns · prose · **REVIEW**

baseline L571 → branch L1880

```diff
- # We know now that `.groupby` gives us the ability to group and aggregate data across our `DataFrame`. The examples above formed groups using just one column in the `DataFrame`. It's possible to group by multiple columns at once by passing in a list of column names to `.groupby`.
+ # ### `group_by` with Multiple Columns
```

**Why:** The baseline paragraph restated what `.groupby` does before introducing multi-column grouping; the section heading replaces it.
**Verdict:** necessary

<a id="c92"></a>
### C92 · cell 95: `group_by` with Multiple Columns · prose · **REVIEW**

baseline L573 → branch L1882

```diff
- # Let's consider the `babynames` dataset again. In this problem, we will find the total number of baby names associated with each sex for each year. To do this, we'll group by *both* the `"Year"` and `"Sex"` columns.
+ # Every grouping so far has used a single column. Passing a list groups by a combination of columns instead: one group for each distinct pairing of values.
+ #
+ # Let's find the total number of babies of each sex born in each year, which means grouping by *both* `"Year"` and `"Sex"`.
```

**Why:** "passing in a list of column names" is kept; the surrounding sentences are reworded around "one group for each distinct pairing of values" and the worked question is restated.
**Verdict:** optional
**Minimal alternative:** Swap `.groupby` -> `group_by` in the two baseline sentences and leave them otherwise alone.

<a id="c93"></a>
### C93 · cell 96 [code] · code

baseline L575 → branch L1886

```diff
- # %%
- babynames.head()
- 
- # %%
- # Find the total number of baby names associated with each sex for each
- # year in the data
- babynames.groupby(["Year", "Sex"])[["Count"]].agg("sum").head(6)
+ # %% tags=["remove-input", "remove-output"] id="p2-groupby-multi"
+ babynames.group_by(["Year", "Sex"]).agg(pl.col("Count").sum()).sort(["Year", "Sex"]).head(6)
```

**Why:** The redundant `babynames.head()` cell is dropped, and `groupby(["Year","Sex"])[["Count"]].agg("sum")` -> `group_by([...]).agg(pl.col("Count").sum())` with an explicit `.sort(["Year","Sex"])`, because the prose below reads the table as a time series and Polars does not order groups.
**Output:** same numbers (1910 F 5,950 / M 3,213 ...); the `babynames.head()` output at this position is gone.

<a id="c94"></a>
### C94 · cell 97 [markdown] · tab-twins

baseline L584 → branch L1890

```diff
- # Notice that both `"Year"` and `"Sex"` serve as the index of the `DataFrame` (they are both rendered in bold). We've created a *multi-index* `DataFrame` where two different index values, the year and sex, are used to uniquely identify each row.
+ # <!-- tab-twins:begin babynames.group_by(["Year", "Sex"]).agg(pl.col("Count").sum()).sort(["Year", "Sex"]).head(6) -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # babynames.group_by(["Year", "Sex"]).agg(pl.col("Count").sum()).sort(["Year", "Sex"]).head(6)
+ # ```
```

**Why:** The baseline's paragraph about both keys being "rendered in bold" as a multi-index is replaced by the tab-set. Polars has no index, so there is nothing to render in bold.
**Output:** same values both panes.

<a id="c95"></a>
### C95 · cell 97 [markdown] · tab-twins

baseline L586 → branch L1898

```diff
- # This isn't the most intuitive way of representing this data – and, because multi-indexed DataFrames have multiple dimensions in their index, they can often be difficult to use.
+ # ```text
+ # shape: (6, 3)
+ # ┌──────┬─────┬───────┐
+ # │ Year ┆ Sex ┆ Count │
+ # │ ---  ┆ --- ┆ ---   │
+ # │ i64  ┆ str ┆ i64   │
+ # ╞══════╪═════╪═══════╡
+ # │ 1910 ┆ F   ┆ 5950  │
+ # │ 1910 ┆ M   ┆ 3213  │
+ # │ 1911 ┆ F   ┆ 6602  │
+ # │ 1911 ┆ M   ┆ 3381  │
+ # │ 1912 ┆ F   ┆ 9804  │
+ # │ 1912 ┆ M   ┆ 8142  │
+ # └──────┴─────┴───────┘
+ # ```
+ # ::::
```

**Why:** Polars output pane.
**Output:** differs: a flat three-column frame against pandas' MultiIndex `Series`, which blanks the repeated `Year` label.

<a id="c96"></a>
### C96 · cell 97 [markdown] · tab-twins

baseline L588 → branch L1915

```diff
- # Another strategy to aggregate across two columns is to create a pivot table. You saw these back in [Data 8](https://inferentialthinking.com/chapters/08/3/Cross-Classifying_by_More_than_One_Variable.html#pivot-tables-rearranging-the-output-of-group). One set of values is used to create the index of the pivot table; another set is used to define the column names. The values contained in each cell of the table correspond to the aggregated data for each index-column pair.
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_pd.groupby(["Year", "Sex"])["Count"].sum().head(6)
+ # ```
```

**Why:** pandas code pane. The baseline's Data 8 pivot-table paragraph moved to C97.
**Output:** same values.

<a id="c97"></a>
### C97 · cell 97 [markdown] · tab-twins

baseline L590 → branch L1921

```diff
- # Here's an illustration of the process:
+ # ```text
+ # Year  Sex
+ # 1910  F      5950
+ #       M      3213
+ # 1911  F      6602
+ #       M      3381
+ # 1912  F      9804
+ #       M      8142
+ # Name: Count, dtype: int64
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
+ 
+ # %% [markdown] id="p2-pivot-explain"
+ # In 1910 the data records 5,950 girls and 3,213 boys. The answer is correct, but the shape is awkward: every year is spread across two rows, and comparing the sexes means reading down the table in pairs.
+ #
+ # A **pivot table** puts the second grouping column across the top instead. You saw these back in [Data 8](https://inferentialthinking.com/chapters/08/3/Cross-Classifying_by_More_than_One_Variable.html#pivot-tables-rearranging-the-output-of-group). One set of values labels the rows, another labels the columns, and each cell holds the aggregate for that row-column pair.
+ #
+ # Here's an illustration of the process:
```

**Why:** pandas output pane, plus the new prose that reads the result (5,950 girls and 3,213 boys in 1910) and motivates the pivot. The Data 8 link is kept.
**Output:** differs: pandas' MultiIndex `Series` repr against the Polars frame. Same six values.

<a id="c98"></a>
### C98 · cell 98 [markdown] · prose · **REVIEW**

baseline L593 → branch L1943

```diff
- # :alt: Another illustration of how group by works.
- # :width:600
+ # :alt: Rows grouped by two keys and aggregated, then reshaped so that one key labels the rows and the other labels the columns of a grid.
+ # :width: 600
```

**Why:** Alt text rewritten as at C17 -- but this hunk also fixes a real defect: the baseline wrote `:width:600` with no space after the colon, which MyST does not parse as a width option. The image was rendering at its natural size.
**Verdict:** necessary

<a id="c99"></a>
### C99 · cell 98: `pivot` · prose · **REVIEW**

baseline L597 → branch L1947

```diff
- # The best way to understand pivot tables is to see one in action. Let's return to our original goal of summing the total number of names associated with each combination of year and sex. We'll call the `pandas` `.pivot_table` [documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.pivot_table.html) method to create a new table.
+ # ### `pivot`
+ #
+ # `.pivot` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.pivot.html) builds that grid.
```

**Why:** `pivot_table` -> `pivot`, and the pandas documentation link swapped for the Polars one. The baseline's framing ("call the `pandas` `.pivot_table` method") names the library.
**Verdict:** necessary

<a id="c100"></a>
### C100 · cell 99 [code] · code

baseline L599 → branch L1951

```diff
- # %%
- # The `pivot_table` method is used to generate a Pandas pivot table
- import numpy as np
- babynames.pivot_table(
-     index = "Year",
-     columns = "Sex",
-     values = "Count",
-     aggfunc = "sum",
+ # %% tags=["remove-input", "remove-output"] id="p2-pivot"
+ babynames.pivot(
+     index="Year",             # one row per year
+     on="Sex",                 # the values of Sex become column names
+     values="Count",           # what fills the cells
+     aggregate_function="sum", # how to combine the rows that land in one cell
```

**Why:** `pivot_table(index=, columns=, values=, aggfunc=)` -> `pivot(index=, on=, values=, aggregate_function=)`. The cell-local `import numpy as np` is dropped -- the baseline imported it for an `np.sum` the code never used, since it passed the string `"sum"`. The inline comments are new scaffolding for the walkthrough at C105.
**Output:** same numbers; `Year` is an ordinary column rather than the index, and there is no `Sex` column-index label above the header.

<a id="c101"></a>
### C101 · cell 100 [markdown] · tab-twins

baseline L610 → branch L1960

```diff
- # Looks a lot better! Now, our `DataFrame` is structured with clear index-column combinations. Each entry in the pivot table represents the summed count of names for a given combination of `"Year"` and `"Sex"`.
+ # <!-- tab-twins:begin aggregate_function="sum", # how to combine the rows that land in one cell -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # babynames.pivot(
+ #     index="Year",             # one row per year
+ #     on="Sex",                 # the values of Sex become column names
+ #     values="Count",           # what fills the cells
+ #     aggregate_function="sum", # how to combine the rows that land in one cell
+ # ).head(5)
+ # ```
```

**Why:** Polars code pane for the pivot.
**Output:** same values both panes.

<a id="c102"></a>
### C102 · cell 100 [markdown] · tab-twins

baseline L612 → branch L1973

```diff
- # Let's take a closer look at the code implemented above.
+ # ```text
+ # shape: (5, 3)
+ # ┌──────┬───────┬───────┐
+ # │ Year ┆ F     ┆ M     │
+ # │ ---  ┆ ---   ┆ ---   │
+ # │ i64  ┆ i64   ┆ i64   │
+ # ╞══════╪═══════╪═══════╡
+ # │ 1910 ┆ 5950  ┆ 3213  │
+ # │ 1911 ┆ 6602  ┆ 3381  │
+ # │ 1912 ┆ 9804  ┆ 8142  │
+ # │ 1913 ┆ 11860 ┆ 10234 │
+ # │ 1914 ┆ 13815 ┆ 13111 │
+ # └──────┴───────┴───────┘
+ # ```
+ # ::::
```

**Why:** Polars output pane.
**Output:** differs: no column-index name row; `Year` is a data column. Values identical to pandas.

<a id="c103"></a>
### C103 · cell 100 [markdown] · tab-twins

baseline L614 → branch L1989

```diff
- # * `index = "Year"` specifies the column name in the original `DataFrame` that should be used as the index of the pivot table
- # * `columns = "Sex"` specifies the column name in the original `DataFrame` that should be used to generate the columns of the pivot table
- # * `values = "Count"` indicates what values from the original `DataFrame` should be used to populate the entry for each index-column combination
- # * `aggfunc = np.sum` tells `pandas` what function to use when aggregating the data specified by `values`. Here, we are summing the name counts for each pair of `"Year"` and `"Sex"`
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_pd.pivot_table(
+ #     index="Year",     # one row per year
+ #     columns="Sex",    # the values of Sex become column names
+ #     values="Count",   # what fills the cells
+ #     aggfunc="sum",    # how to combine the rows that land in one cell
+ # ).head(5)
+ # ```
```

**Why:** pandas code pane, carrying the same four inline comments so the two panes read as the same call.
**Output:** same values.

<a id="c104"></a>
### C104 · cell 100 [markdown] · tab-twins

baseline L619 → branch L2000

```diff
- # We can even include multiple values in the index or columns of our pivot tables.
+ # ```text
+ # Sex       F      M
+ # Year
+ # 1910   5950   3213
+ # 1911   6602   3381
+ # 1912   9804   8142
+ # 1913  11860  10234
+ # 1914  13815  13111
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** pandas output pane. The baseline sentence here ("We can even include multiple values") moved into C105's section.
**Output:** differs: pandas prints `Sex` above the column header and `Year` as the index name; Polars prints neither.

<a id="c105"></a>
### C105 · cell 101 [markdown] · mixed · **REVIEW**

baseline L621 → branch L2013 · spans code and prose

```diff
- # %%
- babynames_pivot = babynames.pivot_table(
-     index="Year",     # the rows (turned into index)
-     columns="Sex",    # the column values
-     values=["Count", "Name"],
-     aggfunc="max",      # group operation
- )
- babynames_pivot.head(6)
+ # %% [markdown] id="p2-pivot-explain2"
+ # The same numbers as before, 5,950 and 3,213 for 1910, now sitting side by side, one row per year. The four arguments are worth naming individually:
+ #
+ # * `index="Year"` is the column whose values label the rows.
+ # * `on="Sex"` is the column whose values become the new column names.
+ # * `values="Count"` is the column that fills the cells.
+ # * `aggregate_function="sum"` says what to do when several rows land in the same cell. Every `(Year, Sex)` pair here covers hundreds of names, and we want them summed.
+ #
+ # ### `pivot` with Multiple Values
+ #
+ # `values` can name more than one column. Every pairing of a value column with a value of `on` becomes an output column, named for both: the value column first, then the value it belongs to.
+ 
+ # %% tags=["remove-input", "remove-output"] id="p2-pivot-multi"
+ babynames.pivot(
+     index="Year",
+     on="Sex",
+     values=["Count", "Name"],
+     aggregate_function="max",
+ ).head(6)
```

**Why:** The argument walkthrough moved up from below the cell to above it, and the multiple-values section was written fresh. The walkthrough also fixes a pre-existing mismatch: the baseline bullet said "`aggfunc = np.sum` tells `pandas` what function to use" while the code beside it passed the string `"sum"`. The new bullets describe what the code actually does.
**Verdict:** optional
**Minimal alternative:** Keep the walkthrough below the cell as the baseline had it, and fix only the `np.sum` bullet.

<a id="c106"></a>
### C106 · cell 103 [markdown] · tab-twins

baseline L631 → branch L2034

```diff
- # Note that each row provides the number of girls and number of boys having that year's most common name, and also lists the alphabetically largest girl name and boy name. The counts for number of girls/boys in the resulting `DataFrame` do not correspond to the names listed. For example, in 1910, the most popular girl name is given to 295 girls, but that name was likely not Yvonne.
+ # <!-- tab-twins:begin values=["Count", "Name"], -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # babynames.pivot(
+ #     index="Year",
+ #     on="Sex",
+ #     values=["Count", "Name"],
+ #     aggregate_function="max",
+ # ).head(6)
+ # ```
```

**Why:** Comparison pane for the multiple-values pivot.
**Output:** same values both panes.

<a id="c107"></a>
### C107 · cell 103 [markdown] · tab-twins

baseline L633 → branch L2047

```diff
- # ## Joining Tables
+ # ```text
+ # shape: (6, 5)
+ # ┌──────┬─────────┬─────────┬────────┬─────────┐
+ # │ Year ┆ Count_F ┆ Count_M ┆ Name_F ┆ Name_M  │
+ # │ ---  ┆ ---     ┆ ---     ┆ ---    ┆ ---     │
+ # │ i64  ┆ i64     ┆ i64     ┆ str    ┆ str     │
+ # ╞══════╪═════════╪═════════╪════════╪═════════╡
+ # │ 1910 ┆ 295     ┆ 237     ┆ Yvonne ┆ William │
+ # │ 1911 ┆ 390     ┆ 214     ┆ Zelma  ┆ Willis  │
+ # │ 1912 ┆ 534     ┆ 501     ┆ Yvonne ┆ Woodrow │
+ # │ 1913 ┆ 584     ┆ 614     ┆ Zelma  ┆ Yoshio  │
+ # │ 1914 ┆ 773     ┆ 769     ┆ Zelma  ┆ Yoshio  │
+ # │ 1915 ┆ 998     ┆ 1033    ┆ Zita   ┆ Yukio   │
+ # └──────┴─────────┴─────────┴────────┴─────────┘
+ # ```
+ # ::::
```

**Why:** Polars output pane.
**Output:** differs: flat `Count_F, Count_M, Name_F, Name_M` names where pandas gives a two-level column index. Same six rows of values.

<a id="c108"></a>
### C108 · cell 103 [markdown] · tab-twins

baseline L635 → branch L2064

```diff
- # When working on data science projects, we're unlikely to have absolutely all the data we want contained in a single `DataFrame` – a real-world data scientist needs to grapple with data coming from multiple sources. If we have access to multiple datasets with related information, we can join two or more tables into a single `DataFrame`.
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_pd.pivot_table(
+ #     index="Year",
+ #     columns="Sex",
+ #     values=["Count", "Name"],
+ #     aggfunc="max",
+ # ).head(6)
+ # ```
```

**Why:** pandas code pane.
**Output:** same call, `columns=`/`aggfunc=` spelling.

<a id="c109"></a>
### C109 · cell 103 [markdown] · tab-twins

baseline L637 → branch L2075

```diff
- # To put this into practice, we'll revisit the `elections` dataset.
+ # ```text
+ #      Count          Name
+ # Sex      F     M       F        M
+ # Year
+ # 1910   295   237  Yvonne  William
+ # 1911   390   214   Zelma   Willis
+ # 1912   534   501  Yvonne  Woodrow
+ # 1913   584   614   Zelma   Yoshio
+ # 1914   773   769   Zelma   Yoshio
+ # 1915   998  1033    Zita    Yukio
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** pandas output pane.
**Output:** differs: the two-level header (`Count`/`Name` over `F`/`M`) that Polars flattens. Same values.

<a id="c110"></a>
### C110 · cell 104 [markdown] · mixed · **REVIEW**

baseline L639 → branch L2090 · spans code and prose

```diff
- # %%
+ # %% [markdown] id="p2-pivot-multi-explain"
+ # Four columns come out: `Count_F`, `Count_M`, `Name_F`, and `Name_M`. Each row gives the largest single-name count for each sex that year, and the alphabetically last name of each sex.
+ #
+ # Read that carefully, because the count and the name in a row have nothing to do with each other — they were aggregated separately, exactly as in the puzzle above. In 1910 the most popular girl's name was given to 295 girls, and that name was certainly not Yvonne.
+ #
+ # ## Joining Tables
+ #
+ # When working on data science projects, we're unlikely to have all the data we want sitting in a single `DataFrame`. A real-world data scientist has to grapple with data arriving from several sources, and combining two tables into one is how that work usually starts.
+ #
+ # Say we want to know how popular the first names of presidential candidates were among California babies in 2022. Neither table can answer that alone: `elections` knows the candidates, and `babynames` knows the babies. We'll start by pulling each candidate's first name into a column of its own, so the two tables have something in common to match on.
+ 
+ # %% tags=["remove-input", "remove-output"] id="p2-first-name"
+ # Split each candidate's full name on the blank space, then keep the first piece
+ elections = elections.with_columns(
+     pl.col("Candidate").str.split(" ").list.get(0).alias("First Name")
+ )
```

**Why:** The baseline's warning that the count and the name in a pivot row are unrelated is kept and sharpened with the concrete 1910 reading (295 girls, not Yvonne). The code change is forced: `str.split().str[0]` -> `str.split(" ").list.get(0)`, because Polars' `split` has no whitespace default and returns a `List` column rather than expanding into columns.
**Verdict:** necessary

<a id="c111"></a>
### C111 · cell 106 [markdown] · tab-twins

baseline L643 → branch L2109

```diff
- # Say we want to understand the popularity of the names of each presidential candidate in 2022. To do this, we'll need the combined data of `babynames` *and* `elections`.
+ # <!-- tab-twins:begin pl.col("Candidate").str.split(" ").list.get(0).alias("First Name") -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Split each candidate's full name on the blank space, then keep the first piece
+ # elections = elections.with_columns(
+ #     pl.col("Candidate").str.split(" ").list.get(0).alias("First Name")
+ # )
+ # elections.head(5)
+ # ```
```

**Why:** Comparison pane for the First Name extraction.
**Output:** same first names both panes.

<a id="c112"></a>
### C112 · cell 106: Split each candidate's full name on the blank space, then ke · tab-twins

baseline L645 → branch L2121

```diff
- # We'll start by creating a new column containing the first name of each presidential candidate. This will help us join each name in `elections` to the corresponding name data in `babynames`.
+ # ```text
+ # shape: (5, 7)
+ # ┌──────┬───────────────────┬──────────────────────┬──────────────┬────────┬───────────┬────────────┐
+ # │ Year ┆ Candidate         ┆ Party                ┆ Popular vote ┆ Result ┆ %         ┆ First Name │
+ # │ ---  ┆ ---               ┆ ---                  ┆ ---          ┆ ---    ┆ ---       ┆ ---        │
+ # │ i64  ┆ str               ┆ str                  ┆ i64          ┆ str    ┆ f64       ┆ str        │
+ # ╞══════╪═══════════════════╪══════════════════════╪══════════════╪════════╪═══════════╪════════════╡
+ # │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republica ┆ 151271       ┆ loss   ┆ 57.210122 ┆ Andrew     │
+ # │      ┆                   ┆ n                    ┆              ┆        ┆           ┆            │
+ # │ 1824 ┆ John Quincy Adams ┆ Democratic-Republica ┆ 113142       ┆ win    ┆ 42.789878 ┆ John       │
+ # │      ┆                   ┆ n                    ┆              ┆        ┆           ┆            │
+ # │ 1828 ┆ Andrew Jackson    ┆ Democratic           ┆ 642806       ┆ win    ┆ 56.203927 ┆ Andrew     │
+ # │ 1828 ┆ John Quincy Adams ┆ National Republican  ┆ 500897       ┆ loss   ┆ 43.796073 ┆ John       │
+ # │ 1832 ┆ Andrew Jackson    ┆ Democratic           ┆ 702735       ┆ win    ┆ 54.574789 ┆ Andrew     │
+ # └──────┴───────────────────┴──────────────────────┴──────────────┴────────┴───────────┴────────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # Split each candidate's full name on the blank space, then keep the first piece
+ # elections_pd["First Name"] = elections_pd["Candidate"].str.split(" ").str[0]
+ # elections_pd.head(5)
+ # ```
+ #
+ # ```text
+ #    Year          Candidate                  Party  ...  Result          %  First Name
+ # 0  1824     Andrew Jackson  Democratic-Republican  ...    loss  57.210122      Andrew
+ # 1  1824  John Quincy Adams  Democratic-Republican  ...     win  42.789878        John
+ # 2  1828     Andrew Jackson             Democratic  ...     win  56.203927      Andrew
+ # 3  1828  John Quincy Adams    National Republican  ...    loss  43.796073        John
+ # 4  1832     Andrew Jackson             Democratic  ...     win  54.574789      Andrew
+ #
+ # [5 rows x 7 columns]
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** Output panes for the same.
**Output:** differs: the Polars repr wraps `Democratic-Republican` across two lines inside its cell, making the table harder to scan than the baseline's; pandas elides three columns behind `...`. Same values.

<a id="c113"></a>
### C113 · cell 107 [code] · code

baseline L647 → branch L2161

```diff
- # %%
- # This `str` operation splits each candidate's full name at each
- # blank space, then takes just the candidate's first name
- elections["First Name"] = elections["Candidate"].str.split().str[0]
- elections.head(5)
- 
- # %%
+ # %% tags=["remove-input", "remove-output"] id="p2-babynames-2022"
```

**Why:** Deletion of the baseline's First Name cell, superseded by C110.
**Output:** same -- the surviving cell produces the same column.

<a id="c114"></a>
### C114 · cell 107 [code] · code

baseline L655 → branch L2163

```diff
- babynames_2022 = babynames[babynames["Year"]==2022]
+ babynames_2022 = babynames.filter(pl.col("Year") == 2022)
```

**Why:** `babynames[babynames["Year"]==2022]` -> `.filter(pl.col("Year") == 2022)`.
**Output:** same rows; the pandas 235835.. row labels are gone.

<a id="c115"></a>
### C115 · cell 108 [markdown] · tab-twins

baseline L659 → branch L2167

```diff
- # Now, we're ready to join the two tables. `pd.merge` ([documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html)) is the `pandas` method used to join `DataFrame`s together.
+ # <!-- tab-twins:begin babynames_2022 = babynames.filter(pl.col("Year") == 2022) -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Here, we'll only consider `babynames` data from 2022
+ # babynames_2022 = babynames.filter(pl.col("Year") == 2022)
+ # babynames_2022.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 5)
+ # ┌───────┬─────┬──────┬────────┬───────┐
+ # │ State ┆ Sex ┆ Year ┆ Name   ┆ Count │
+ # │ ---   ┆ --- ┆ ---  ┆ ---    ┆ ---   │
+ # │ str   ┆ str ┆ i64  ┆ str    ┆ i64   │
+ # ╞═══════╪═════╪══════╪════════╪═══════╡
+ # │ CA    ┆ F   ┆ 2022 ┆ Olivia ┆ 2178  │
+ # │ CA    ┆ F   ┆ 2022 ┆ Emma   ┆ 2080  │
+ # │ CA    ┆ F   ┆ 2022 ┆ Camila ┆ 2046  │
+ # │ CA    ┆ F   ┆ 2022 ┆ Mia    ┆ 1882  │
+ # │ CA    ┆ F   ┆ 2022 ┆ Sophia ┆ 1762  │
+ # └───────┴─────┴──────┴────────┴───────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # Here, we'll only consider `babynames` data from 2022
+ # babynames_2022_pd = babynames_pd[babynames_pd["Year"] == 2022]
+ # babynames_2022_pd.head()
+ # ```
+ #
+ # ```text
+ #        State Sex  Year    Name  Count
+ # 235835    CA   F  2022  Olivia   2178
+ # 235836    CA   F  2022    Emma   2080
+ # 235837    CA   F  2022  Camila   2046
+ # 235838    CA   F  2022     Mia   1882
+ … 5 more lines
```

**Why:** Comparison pane for the 2022 subset.
**Output:** differs: pandas keeps the original row labels. Same five rows.

<a id="c116"></a>
### C116 · cell 109 [markdown] · mixed · **REVIEW**

baseline L661 → branch L2213 · spans code and prose

```diff
- # %%
- merged = pd.merge(left = elections, right = babynames_2022, \
-                   left_on = "First Name", right_on = "Name")
+ # %% [markdown] id="p2-join-intro"
+ # Now we're ready to combine them. As in Data 8, this operation is called a **join**: the left table calls the method, and the right table is its first argument [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.join.html).
+ 
+ # %% tags=["remove-input", "remove-output"] id="p2-join"
+ merged = elections.join(
+     babynames_2022,
+     left_on="First Name",
+     right_on="Name",
+     maintain_order="left",
+ )
```

**Why:** `pd.merge(left=, right=, ...)` -> `elections.join(babynames_2022, ...)`: Polars has no free `merge` function, so the left table calls the method and the prose has to say which table is which. `maintain_order="left"` is added because a Polars join gives no ordering guarantee, and both the committed table and the prose that reads it depend on the rows arriving in `elections` order.
**Verdict:** necessary

<a id="c117"></a>
### C117 · cell 75 [code] · code

baseline L665 → branch L2224

```diff
- # Notice that pandas automatically specifies `Year_x` and `Year_y`
- # when both merged DataFrames have the same column name to avoid confusion
- 
- # Second option
- # merged = elections.merge(right = babynames_2022, \
-     # left_on = "First Name", right_on = "Name")
```

**Why:** Deletion of the baseline's two comments: the note that "pandas automatically specifies `Year_x` and `Year_y`" is false of Polars (the suffix is `_right`, and only the right side is suffixed), and the commented-out `elections.merge(right=...)` "second option" is the only form Polars has, so it is not an alternative.
**Output:** same -- the surviving join produces the table at C159.

<a id="c118"></a>
### C118 · cell 111 [markdown] · tab-twins

baseline L673 → branch L2226

```diff
- # Let's take a closer look at the parameters:
+ # <!-- tab-twins:begin merged = elections.join( -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # merged = elections.join(
+ #     babynames_2022,
+ #     left_on="First Name",
+ #     right_on="Name",
+ #     maintain_order="left",
+ # )
+ # merged.head()
+ # ```
```

**Why:** Comparison pane for the join.
**Output:** differs: 11 columns in Polars against 12 in pandas -- see C159.

<a id="c119"></a>
### C119 · cell 111 [markdown] · tab-twins

baseline L675 → branch L2240

```diff
- # * `left` and `right` parameters are used to specify the `DataFrame`s to be joined.
- # * `left_on` and `right_on` parameters are assigned to the string names of the columns to be used when performing the join. These two `on` parameters tell `pandas` what values should act as pairing keys to determine which rows to merge across the `DataFrame`s. We'll talk more about this idea of a pairing key next lecture.
+ # ```text
+ # shape: (5, 11)
+ # ┌──────┬──────────────────┬──────────────────┬──────────────┬───┬───────┬─────┬────────────┬───────┐
+ # │ Year ┆ Candidate        ┆ Party            ┆ Popular vote ┆ … ┆ State ┆ Sex ┆ Year_right ┆ Count │
+ # │ ---  ┆ ---              ┆ ---              ┆ ---          ┆   ┆ ---   ┆ --- ┆ ---        ┆ ---   │
+ # │ i64  ┆ str              ┆ str              ┆ i64          ┆   ┆ str   ┆ str ┆ i64        ┆ i64   │
+ # ╞══════╪══════════════════╪══════════════════╪══════════════╪═══╪═══════╪═════╪════════════╪═══════╡
+ # │ 1824 ┆ Andrew Jackson   ┆ Democratic-Repub ┆ 151271       ┆ … ┆ CA    ┆ M   ┆ 2022       ┆ 741   │
+ # │      ┆                  ┆ lican            ┆              ┆   ┆       ┆     ┆            ┆       │
+ # │ 1824 ┆ John Quincy      ┆ Democratic-Repub ┆ 113142       ┆ … ┆ CA    ┆ M   ┆ 2022       ┆ 490   │
+ # │      ┆ Adams            ┆ lican            ┆              ┆   ┆       ┆     ┆            ┆       │
+ # │ 1828 ┆ Andrew Jackson   ┆ Democratic       ┆ 642806       ┆ … ┆ CA    ┆ M   ┆ 2022       ┆ 741   │
+ # │ 1828 ┆ John Quincy      ┆ National         ┆ 500897       ┆ … ┆ CA    ┆ M   ┆ 2022       ┆ 490   │
+ # │      ┆ Adams            ┆ Republican       ┆              ┆   ┆       ┆     ┆            ┆       │
+ # │ 1832 ┆ Andrew Jackson   ┆ Democratic       ┆ 702735       ┆ … ┆ CA    ┆ M   ┆ 2022       ┆ 741   │
+ # └──────┴──────────────────┴──────────────────┴──────────────┴───┴───────┴─────┴────────────┴───────┘
+ # ```
+ # ::::
```

**Why:** Polars output pane.
**Output:** differs: the key is coalesced, so there is no `Name` column, and the babies' year arrives as `Year_right`. The repr also hides the middle columns behind a single `...` column, which is why C120 adds a column-list cell.

<a id="c120"></a>
### C120 · cell 111 [markdown] · tab-twins

baseline L678 → branch L2259 · spans code and prose

```diff
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # merged_pd = elections_pd.merge(
+ #     babynames_2022_pd,
+ #     left_on="First Name",
+ #     right_on="Name",
+ # )
+ # merged_pd.head()
+ # ```
+ #
+ # ```text
+ #    Year_x          Candidate                  Party  ...  Year_y    Name  Count
+ # 0    1824     Andrew Jackson  Democratic-Republican  ...    2022  Andrew    741
+ # 1    1824  John Quincy Adams  Democratic-Republican  ...    2022    John    490
+ # 2    1828     Andrew Jackson             Democratic  ...    2022  Andrew    741
+ # 3    1828  John Quincy Adams    National Republican  ...    2022    John    490
+ # 4    1832     Andrew Jackson             Democratic  ...    2022  Andrew    741
+ #
+ # [5 rows x 12 columns]
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
+ 
+ # %% tags=["remove-input", "remove-output"] id="p2-join-cols"
+ # The full column list, since the table above is too wide to show it
+ merged.columns
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin merged.columns -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # The full column list, since the table above is too wide to show it
+ # merged.columns
+ # ```
+ #
+ # ```text
+ … 111 more lines
```

**Why:** pandas output pane, plus the two new cells that print `merged.columns`. Per CONVERSIONS, the column cell was added because the join repr elided `First Name` -- the coalesced key that the bullet list is about -- leaving a schema claim the reader could not check.
**Output:** differs: `Year_x`/`Year_y` in the pandas pane against `Year_right` in Polars, and 12 columns against 11. Same five rows of values.

<a id="c121"></a>
### C121 · cell 117: Parting Note · prose · **REVIEW**

baseline L681 → branch L2413

```diff
- # Congratulations! We finally tackled `pandas`. Don't worry if you are still not feeling very comfortable with it—you will have plenty of chances to practice over the next few weeks.
+ # Congratulations! We have now covered the core of Polars. Don't worry if you are still not feeling very comfortable with it — you will have plenty of chances to practice over the next few weeks, and the [user guide](https://docs.pola.rs/user-guide/expressions/aggregation/) shows these same operations written a few more ways.
```

**Why:** "we finally tackled `pandas`" -> "we have now covered the core of Polars", plus a pointer to the Polars user guide's aggregation page in place of nothing.
**Verdict:** necessary

<a id="c122"></a>
### C122 · cell 117: Parting Note · prose · **REVIEW**

baseline L683 → branch L2415

```diff
- # Next, we will get our hands dirty with some real-world datasets and use our `pandas` knowledge to conduct some exploratory data analysis.
+ # Next, we will get our hands dirty with some real-world datasets and use what we know to conduct some exploratory data analysis.
```

**Why:** "use our `pandas` knowledge" -> "use what we know". The library name was the only pandas-specific token.
**Verdict:** necessary

<a id="c123"></a>
### C123 · `import polars as pl` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 5)
+ [text] ┌───────┬─────┬──────┬──────────┬───────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name     ┆ Count │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   │
+ [text] │ str   ┆ str ┆ i64  ┆ str      ┆ i64   │
+ [text] ╞═══════╪═════╪══════╪══════════╪═══════╡
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   │
+ [text] └───────┴─────┴──────┴──────────┴───────┘
```

**Why:** Re-executed `pl.read_csv` on the same zipped CA extract, so the cell now prints the Polars table repr -- a `shape: (5, 5)` line, dtypes under the column names, no row-number column -- over the same five 1910 rows and counts the baseline showed.
**Reader sees:** equivalent

<a id="c124"></a>
### C124 · `babynames.group_by("Year")` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] <polars.dataframe.group_by.GroupBy at 0x107b30090>
```

**Why:** `babynames.group_by("Year")` returns a `polars.dataframe.group_by.GroupBy` and prints the bare `<... at 0x...>` repr, the same opaque-object result pandas gave with `DataFrameGroupBy`. The hex address is whatever that run allocated.
**Reader sees:** equivalent

<a id="c125"></a>
### C125 · `babynames.group_by("Year").agg(pl.col("Count").sum()).head(5)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 2)
+ [text] ┌──────┬────────┐
+ [text] │ Year ┆ Count  │
+ [text] │ ---  ┆ ---    │
+ [text] │ i64  ┆ i64    │
+ [text] ╞══════╪════════╡
+ [text] │ 1971 ┆ 310020 │
+ [text] │ 2004 ┆ 480892 │
+ [text] │ 1992 ┆ 541054 │
+ [text] │ 1998 ┆ 464300 │
+ [text] │ 1995 ┆ 494635 │
+ [text] └──────┴────────┘
```

**Why:** `p2-agg-unsorted`: a deliberately unordered `group_by("Year")` re-executed under Polars, which defaults to `maintain_order=False`, so the five year labels committed here (1971, 2004, 1992, 1998, 1995) are whichever groups finished first. **This output does not reproduce** -- four fresh runs on the pinned 1.43.1 gave four different year sets, none of them this one. It is declared in `OUTPUT_CHURNS` (`conversion/tab_twins_data.py`) so `--verify` checks only the code panes, and since CI never executes, this exact table is what ships. The old chapter had no cell like it: pandas sorted group keys and returned 1910-1914 every time.
**Reader sees:** new: the chapter's one non-reproducible committed table. The old chapter never showed unordered group output, and the sorted 1910-1914 lesson it did teach is now C126. Staff should know the printed years carry no meaning and will differ from any local run.

<a id="c126"></a>
### C126 · `babies_by_year = babynames.group_by("Year").agg(pl.col("Count").sum())` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 2)
+ [text] ┌──────┬───────┐
+ [text] │ Year ┆ Count │
+ [text] │ ---  ┆ ---   │
+ [text] │ i64  ┆ i64   │
+ [text] ╞══════╪═══════╡
+ [text] │ 1910 ┆ 9163  │
+ [text] │ 1911 ┆ 9983  │
+ [text] │ 1912 ┆ 17946 │
+ [text] │ 1913 ┆ 22094 │
+ [text] │ 1914 ┆ 26926 │
+ [text] └──────┴───────┘
```

**Why:** `p2-agg-sorted` re-executes the baseline's per-year sum with an explicit `.sort("Year")`, which Polars needs and pandas got free from the sorted group index. Same 1910-1914 totals: 9163, 9983, 17946, 22094, 26926.
**Reader sees:** equivalent

<a id="c127"></a>
### C127 · `babynames.group_by("Name").agg(pl.col("Count").min()).sort("Name").hea` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 2)
+ [text] ┌─────────┬───────┐
+ [text] │ Name    ┆ Count │
+ [text] │ ---     ┆ ---   │
+ [text] │ str     ┆ i64   │
+ [text] ╞═════════╪═══════╡
+ [text] │ Aadan   ┆ 5     │
+ [text] │ Aadarsh ┆ 6     │
+ [text] │ Aaden   ┆ 10    │
+ [text] │ Aadhav  ┆ 6     │
+ [text] │ Aadhini ┆ 6     │
+ [text] └─────────┴───────┘
```

**Why:** Per-name minimum, re-executed; `.sort("Name")` supplies the alphabetical order pandas got from its group index, and `Name` is an ordinary column rather than the index. Aadan 5, Aadarsh 6, Aaden 10, Aadhav 6, Aadhini 6 -- the baseline's numbers.
**Reader sees:** equivalent

<a id="c128"></a>
### C128 · `babynames.group_by("Name").agg(` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 5)
+ [text] ┌─────────┬───────────┬───────────┬────────────┬────────────────┐
+ [text] │ Name    ┆ Min Count ┆ Max Count ┆ Mean Count ┆ Years Recorded │
+ [text] │ ---     ┆ ---       ┆ ---       ┆ ---        ┆ ---            │
+ [text] │ str     ┆ i64       ┆ i64       ┆ f64        ┆ u32            │
+ [text] ╞═════════╪═══════════╪═══════════╪════════════╪════════════════╡
+ [text] │ Aadan   ┆ 5         ┆ 7         ┆ 6.0        ┆ 3              │
+ [text] │ Aadarsh ┆ 6         ┆ 6         ┆ 6.0        ┆ 1              │
+ [text] │ Aaden   ┆ 10        ┆ 158       ┆ 46.214286  ┆ 14             │
+ [text] │ Aadhav  ┆ 6         ┆ 8         ┆ 6.75       ┆ 4              │
+ [text] │ Aadhini ┆ 6         ┆ 6         ┆ 6.0        ┆ 1              │
+ [text] └─────────┴───────────┴───────────┴────────────┴────────────────┘
```

**Why:** One `.agg` now returns min, max, mean and a `pl.len()` count side by side under flat explicit names, where the baseline printed three separate single-column tables each headed `Count`. The shared values match (Aadan 5/7/6.0, Aaden 10/158/46.214286); `Years Recorded` is a `u32` count the old chapter did not compute.
**Reader sees:** changed: three one-column tables become one five-column table, the column is named `Min Count`/`Max Count`/`Mean Count` rather than `Count` three times, and a `Years Recorded` column is added

<a id="c129"></a>
### C129 · `babynames_new = babynames.with_columns(` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 3)
+ [text] ┌──────────┬──────────────┬──────┐
+ [text] │ Name     ┆ First Letter ┆ Year │
+ [text] │ ---      ┆ ---          ┆ ---  │
+ [text] │ str      ┆ str          ┆ i64  │
+ [text] ╞══════════╪══════════════╪══════╡
+ [text] │ Mary     ┆ M            ┆ 1910 │
+ [text] │ Helen    ┆ H            ┆ 1910 │
+ [text] │ Dorothy  ┆ D            ┆ 1910 │
+ [text] │ Margaret ┆ M            ┆ 1910 │
+ [text] │ Frances  ┆ F            ┆ 1910 │
+ [text] └──────────┴──────────────┴──────┘
```

**Why:** `.str.slice(0, 1)` inside `with_columns` plus a `select`, re-executed: same Mary/M, Helen/H, Dorothy/D, Margaret/M, Frances/F rows, printed as a Polars table with dtypes and no row index.
**Reader sees:** equivalent

<a id="c130"></a>
### C130 · `babynames_new.group_by("Name").agg(` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 3)
+ [text] ┌─────────┬──────────────┬──────┐
+ [text] │ Name    ┆ First Letter ┆ Year │
+ [text] │ ---     ┆ ---          ┆ ---  │
+ [text] │ str     ┆ str          ┆ i64  │
+ [text] ╞═════════╪══════════════╪══════╡
+ [text] │ Aadan   ┆ A            ┆ 2014 │
+ [text] │ Aadarsh ┆ A            ┆ 2019 │
+ [text] │ Aaden   ┆ A            ┆ 2020 │
+ [text] │ Aadhav  ┆ A            ┆ 2019 │
+ [text] │ Aadhini ┆ A            ┆ 2022 │
+ [text] └─────────┴──────────────┴──────┘
```

**Why:** The dict-agg (`{"First Letter": "first", "Year": "max"}`) is now two expressions in one `.agg`, with `.sort("Name")` for the alphabetical order. Same five rows and the same `Year` maxima (2014, 2019, 2020, 2019, 2022).
**Reader sees:** equivalent

<a id="c131"></a>
### C131 · `df = pl.DataFrame({"letter": ["A", "A", "B", "C", "C", "C"],` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (6, 3)
+ [text] ┌────────┬──────┬───────┐
+ [text] │ letter ┆ num  ┆ state │
+ [text] │ ---    ┆ ---  ┆ ---   │
+ [text] │ str    ┆ i64  ┆ str   │
+ [text] ╞════════╪══════╪═══════╡
+ [text] │ A      ┆ 1    ┆ null  │
+ [text] │ A      ┆ 2    ┆ tx    │
+ [text] │ B      ┆ 3    ┆ fl    │
+ [text] │ C      ┆ 4    ┆ hi    │
+ [text] │ C      ┆ null ┆ null  │
+ [text] │ C      ┆ 4    ┆ ak    │
+ [text] └────────┴──────┴───────┘
```

**Why:** The demo frame is built with Python `None` instead of `np.nan`, so Polars keeps `num` as `i64` with a `null` and `state` as `str` with `null`s. pandas had upcast `num` to `float64` and printed `1.0, 2.0, ... NaN`. Verified: the schema reads `num: Int64`.
**Reader sees:** changed: `num` prints as integers with a `null` rather than floats with `NaN`, which is the null-is-not-NaN distinction rather than a data change

<a id="c132"></a>
### C132 · `df.group_by("letter", maintain_order=True).len()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3, 2)
+ [text] ┌────────┬─────┐
+ [text] │ letter ┆ len │
+ [text] │ ---    ┆ --- │
+ [text] │ str    ┆ u32 │
+ [text] ╞════════╪═════╡
+ [text] │ A      ┆ 2   │
+ [text] │ B      ┆ 1   │
+ [text] │ C      ┆ 3   │
+ [text] └────────┴─────┘
```

**Why:** `.len()` replaces `.size()`, so the count comes back as a two-column DataFrame (`letter`, `len`, `u32`) instead of a named `Series` with an index and a `dtype: int64` footer. `maintain_order=True` keeps A/B/C. Counts 2/1/3 unchanged.
**Reader sees:** changed: a Series becomes a DataFrame and the count column is called `len`; the .size()-counts-nulls point still lands against C133

<a id="c133"></a>
### C133 · `df.group_by("letter", maintain_order=True).agg(pl.all().count())` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3, 3)
+ [text] ┌────────┬─────┬───────┐
+ [text] │ letter ┆ num ┆ state │
+ [text] │ ---    ┆ --- ┆ ---   │
+ [text] │ str    ┆ u32 ┆ u32   │
+ [text] ╞════════╪═════╪═══════╡
+ [text] │ A      ┆ 2   ┆ 1     │
+ [text] │ B      ┆ 1   ┆ 1     │
+ [text] │ C      ┆ 2   ┆ 2     │
+ [text] └────────┴─────┴───────┘
```

**Why:** `.agg(pl.all().count())` re-executed: Polars `count()` skips nulls exactly as pandas' `.count()` did, so A 2/1, B 1/1, C 2/2 -- the contrast with C132 that the surrounding prose turns on. `letter` is a column, not an index.
**Reader sees:** equivalent

<a id="c134"></a>
### C134 · `df["letter"].value_counts(sort=True)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3, 2)
+ [text] ┌────────┬───────┐
+ [text] │ letter ┆ count │
+ [text] │ ---    ┆ ---   │
+ [text] │ str    ┆ u32   │
+ [text] ╞════════╪═══════╡
+ [text] │ C      ┆ 3     │
+ [text] │ A      ┆ 2     │
+ [text] │ B      ┆ 1     │
+ [text] └────────┴───────┘
```

**Why:** `value_counts` returns a DataFrame in Polars, so the output is a `letter`/`count` table with `u32` counts rather than a `Series` named `count` with a `dtype` footer; `sort=True` is what supplies the descending order pandas applied automatically. Ranking C 3, A 2, B 1 is the baseline's.
**Reader sees:** changed: a Series becomes a two-column DataFrame and the descending sort is now explicit in the code

<a id="c135"></a>
### C135 · `fig = px.line(babies_by_year, x="Year", y="Count")` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [plotly] figure md5:53d22e934d
+ [plotly] trace 0 scatter
```

**Why:** An authored rewrite, so there is no baseline hunk — but the counterpart figure in `pandas_3` plots the same series, and every `x`/`y` value decodes byte-identical to it. What is new is `fig.update_layout(font_size=18, autosize=False, width=700, height=400)` and a `fig-alt` line.
**Reader sees:** changed: the same births-per-year curve, now drawn at a fixed 700x400 with 18px type instead of plotly's default sizing, and carrying alt text it did not have. Deliberate — it is the house style the rest of the rewritten chapter uses.

<a id="c136"></a>
### C136 · `f_babynames = babynames.filter(pl.col("Sex") == "F").sort("Year")` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 5)
+ [text] ┌───────┬─────┬──────┬──────────┬───────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name     ┆ Count │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   │
+ [text] │ str   ┆ str ┆ i64  ┆ str      ┆ i64   │
+ [text] ╞═══════╪═════╪══════╪══════════╪═══════╡
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   │
+ [text] └───────┴─────┴──────┴──────────┴───────┘
```

**Why:** The filter-and-sort that builds `f_babynames` now displays its head. The baseline computed the same frame inside the RTP cell and never printed it; because the file already starts with 1910 F rows, the five rows shown repeat C123's.
**Reader sees:** new: the old chapter never displayed `f_babynames`

<a id="c137"></a>
### C137 · `jenn_counts = f_babynames.filter(pl.col("Name") == "Jennifer")["Count"` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] 0.018796372629843364
```

**Why:** `jenn_counts.last() / jenn_counts.max()` re-executed on the same `Sex == "F"`, `Year`-sorted frame. Identical float to the baseline's `curr_jenn / max_jenn`.
**Reader sees:** equivalent

<a id="c138"></a>
### C138 · `rtp_table = f_babynames.group_by("Name").agg(` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 2)
+ [text] ┌─────────┬───────────┐
+ [text] │ Name    ┆ Count RTP │
+ [text] │ ---     ┆ ---       │
+ [text] │ str     ┆ f64       │
+ [text] ╞═════════╪═══════════╡
+ [text] │ Aadhini ┆ 1.0       │
+ [text] │ Aadhira ┆ 0.5       │
+ [text] │ Aadhya  ┆ 0.66      │
+ [text] │ Aadya   ┆ 0.586207  │
+ [text] │ Aahana  ┆ 0.269231  │
+ [text] └─────────┴───────────┘
```

**Why:** The RTP is computed as one expression inside `.agg`, so the result has a single `Count RTP` column, named at creation. The baseline aggregated `[["Year", "Count"]]` and so carried a `Year` column of 1.0s, which it then used to teach nuisance columns and renamed `Count` afterwards. Same names and ratios (Aadhini 1.0, Aadhira 0.5, Aadhya 0.66, Aadya 0.586207, Aahana 0.269231); `.sort("Name")` supplies the index order pandas had.
**Reader sees:** changed: the `Year` column of 1.0s is gone, and with it the nuisance-column lesson the baseline hung on it; the RTP numbers are unchanged

<a id="c139"></a>
### C139 · `def ratio_to_peak(series):` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 2)
+ [text] ┌────────┬───────────┐
+ [text] │ Name   ┆ Count RTP │
+ [text] │ ---    ┆ ---       │
+ [text] │ str    ┆ f64       │
+ [text] ╞════════╪═══════════╡
+ [text] │ Debra  ┆ 0.00126   │
+ [text] │ Debbie ┆ 0.002815  │
+ [text] │ Carol  ┆ 0.00318   │
+ [text] │ Tammy  ┆ 0.003249  │
+ [text] │ Susan  ┆ 0.003305  │
+ [text] └────────┴───────────┘
```

**Why:** The same `ratio_to_peak` function the baseline defined, now handed to `map_batches(..., returns_scalar=True)` because Polars will not take a bare Python callable in `.agg`. Sorted ascending it prints the baseline's Debra/Debbie/Carol/Tammy/Susan table with the same ratios.
**Reader sees:** new: `map_batches` is Polars-only plumbing the old chapter had no counterpart for, but the table it produces is the baseline's

<a id="c140"></a>
### C140 · `rtp_table.sort("Count RTP").head()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 2)
+ [text] ┌────────┬───────────┐
+ [text] │ Name   ┆ Count RTP │
+ [text] │ ---    ┆ ---       │
+ [text] │ str    ┆ f64       │
+ [text] ╞════════╪═══════════╡
+ [text] │ Debra  ┆ 0.00126   │
+ [text] │ Debbie ┆ 0.002815  │
+ [text] │ Carol  ┆ 0.00318   │
+ [text] │ Tammy  ┆ 0.003249  │
+ [text] │ Susan  ┆ 0.003305  │
+ [text] └────────┴───────────┘
```

**Why:** `rtp_table.sort("Count RTP").head()` re-executed -- the baseline's "names whose popularity fell most" table, with the same five names and ratios to six places, minus the `Year` column of 1.0s.
**Reader sees:** equivalent

<a id="c141"></a>
### C141 · `fig = px.line(f_babynames.filter(pl.col("Name") == "Debra"), x="Year",` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [plotly] figure md5:dbc84a9817
+ [plotly] trace 0 scatter
```

**Why:** The same styling block at 1000x400 over an identical series: `filter(pl.col("Name") == "Debra")` returns exactly the rows the pandas mask did, and the decoded values match the `pandas_3` figure byte for byte.
**Reader sees:** changed: the Debra curve itself is untouched; only the figure's size and font, plus new alt text.

<a id="c142"></a>
### C142 · `top10 = rtp_table.sort("Count RTP").head(10)["Name"].to_list()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] ['Debra',
+ [text]  'Debbie',
+ [text]  'Carol',
+ [text]  'Tammy',
+ [text]  'Susan',
+ [text]  'Cheryl',
+ [text]  'Shannon',
+ [text]  'Tina',
+ [text]  'Michele',
+ [text]  'Terri']
```

**Why:** `top10` is now a plain Python list of names and is printed. The baseline assigned `.index` from the sorted table and passed it straight into the plot without showing it. Same ten names in the same order.
**Reader sees:** new: the old chapter never printed this list

<a id="c143"></a>
### C143 · `fig = px.line(` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [plotly] figure md5:bdc93b97a2
+ [plotly] trace 0 scatter name='Carol'
+ [plotly] trace 1 scatter name='Susan'
+ [plotly] trace 2 scatter name='Tina'
+ [plotly] trace 3 scatter name='Cheryl'
+ [plotly] trace 4 scatter name='Michele'
+ [plotly] trace 5 scatter name='Debbie'
+ [plotly] trace 6 scatter name='Shannon'
+ [plotly] trace 7 scatter name='Terri'
+ [plotly] trace 8 scatter name='Debra'
+ [plotly] trace 9 scatter name='Tammy'
```

**Why:** Same styling, plus a trace reorder. `f_babynames` is sorted by `Year` on both sides, but pandas `sort_values` is an unstable quicksort and Polars `sort` is stable, so within 1936 — the first year in which both names appear — Debbie and Michele change places, and plotly express assigns trace order and colour by first appearance. Checked against `STATE.CA.TXT`: pandas puts Debbie at row 14484 and Michele at 14560, Polars the reverse.
**Reader sees:** changed: all ten series are byte-identical to the `pandas_3` figure, but Debbie and Michele swap colours (orange <-> cyan) and legend positions; plus the fixed 1000x400 sizing and 18px font. The alt text names only Debra and Susan, so it still holds.

<a id="c144"></a>
### C144 · `elections = pl.read_csv("data/elections.csv")` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 6)
+ [text] ┌──────┬───────────────────┬───────────────────────┬──────────────┬────────┬───────────┐
+ [text] │ Year ┆ Candidate         ┆ Party                 ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---  ┆ ---               ┆ ---                   ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ i64  ┆ str               ┆ str                   ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞══════╪═══════════════════╪═══════════════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republican ┆ 151271       ┆ loss   ┆ 57.210122 │
+ [text] │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican ┆ 113142       ┆ win    ┆ 42.789878 │
+ [text] │ 1828 ┆ Andrew Jackson    ┆ Democratic            ┆ 642806       ┆ win    ┆ 56.203927 │
+ [text] │ 1828 ┆ John Quincy Adams ┆ National Republican   ┆ 500897       ┆ loss   ┆ 43.796073 │
+ [text] │ 1832 ┆ Andrew Jackson    ┆ Democratic            ┆ 702735       ┆ win    ┆ 54.574789 │
+ [text] └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────────┘
```

**Why:** `pl.read_csv("data/elections.csv")` re-executed on the same 2024-vintage file. Same five 1824-1832 rows and percentages; Polars prints dtypes in the header and drops the row index, and the `%` column stays `f64`.
**Reader sees:** equivalent

<a id="c145"></a>
### C145 · `df.filter(pl.len().over("letter") >= 2)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 3)
+ [text] ┌────────┬──────┬───────┐
+ [text] │ letter ┆ num  ┆ state │
+ [text] │ ---    ┆ ---  ┆ ---   │
+ [text] │ str    ┆ i64  ┆ str   │
+ [text] ╞════════╪══════╪═══════╡
+ [text] │ A      ┆ 1    ┆ null  │
+ [text] │ A      ┆ 2    ┆ tx    │
+ [text] │ C      ┆ 4    ┆ hi    │
+ [text] │ C      ┆ null ┆ null  │
+ [text] │ C      ┆ 4    ┆ ak    │
+ [text] └────────┴──────┴───────┘
```

**Why:** A small-frame demo of `pl.len().over("letter") >= 2` on the six-row `df`, keeping the A and C rows. The baseline taught group filtering only on `elections` with a lambda; this cell exists to show the window expression on something a reader can count by eye.
**Reader sees:** new: the old chapter had no small-frame filtering demo

<a id="c146"></a>
### C146 · `elections.filter(pl.col("%").max().over("Year") < 45).head(9)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (9, 6)
+ [text] ┌──────┬──────────────────────┬──────────────────────┬──────────────┬────────┬───────────┐
+ [text] │ Year ┆ Candidate            ┆ Party                ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---  ┆ ---                  ┆ ---                  ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ i64  ┆ str                  ┆ str                  ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞══════╪══════════════════════╪══════════════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 1860 ┆ Abraham Lincoln      ┆ Republican           ┆ 1855993      ┆ win    ┆ 39.699408 │
+ [text] │ 1860 ┆ John Bell            ┆ Constitutional Union ┆ 590901       ┆ loss   ┆ 12.639283 │
+ [text] │ 1860 ┆ John C. Breckinridge ┆ Southern Democratic  ┆ 848019       ┆ loss   ┆ 18.138998 │
+ [text] │ 1860 ┆ Stephen A. Douglas   ┆ Northern Democratic  ┆ 1380202      ┆ loss   ┆ 29.522311 │
+ [text] │ 1912 ┆ Eugene V. Debs       ┆ Socialist            ┆ 901551       ┆ loss   ┆ 6.004354  │
+ [text] │ 1912 ┆ Eugene W. Chafin     ┆ Prohibition          ┆ 208156       ┆ loss   ┆ 1.386325  │
+ [text] │ 1912 ┆ Theodore Roosevelt   ┆ Progressive          ┆ 4122721      ┆ loss   ┆ 27.457433 │
+ [text] │ 1912 ┆ William Taft         ┆ Republican           ┆ 3486242      ┆ loss   ┆ 23.218466 │
+ [text] │ 1912 ┆ Woodrow Wilson       ┆ Democratic           ┆ 6296284      ┆ win    ┆ 41.933422 │
+ [text] └──────┴──────────────────────┴──────────────────────┴──────────────┴────────┴───────────┘
```

**Why:** `groupby("Year").filter(lambda sf: sf["%"].max() < 45)` becomes `filter(pl.col("%").max().over("Year") < 45)`, re-executed. Identical nine rows -- the 1860 and 1912 fields, same candidates, same percentages -- with the 23/24/25/26/66-70 row labels gone.
**Reader sees:** equivalent

<a id="c147"></a>
### C147 · `elections.group_by("Party").max().sort("Party").head(10)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (10, 6)
+ [text] ┌───────────────────────┬──────┬────────────────────┬──────────────┬────────┬───────────┐
+ [text] │ Party                 ┆ Year ┆ Candidate          ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---                   ┆ ---  ┆ ---                ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ str                   ┆ i64  ┆ str                ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞═══════════════════════╪══════╪════════════════════╪══════════════╪════════╪═══════════╡
+ [text] │ American              ┆ 1976 ┆ Thomas J. Anderson ┆ 873053       ┆ loss   ┆ 21.554001 │
+ [text] │ American Independent  ┆ 1976 ┆ Lester Maddox      ┆ 9901118      ┆ loss   ┆ 13.571218 │
+ [text] │ Anti-Masonic          ┆ 1832 ┆ William Wirt       ┆ 100715       ┆ loss   ┆ 7.821583  │
+ [text] │ Anti-Monopoly         ┆ 1884 ┆ Benjamin Butler    ┆ 134294       ┆ loss   ┆ 1.335838  │
+ [text] │ Citizens              ┆ 1980 ┆ Barry Commoner     ┆ 233052       ┆ loss   ┆ 0.270182  │
+ [text] │ Communist             ┆ 1932 ┆ William Z. Foster  ┆ 103307       ┆ loss   ┆ 0.261069  │
+ [text] │ Constitution          ┆ 2016 ┆ Michael Peroutka   ┆ 203091       ┆ loss   ┆ 0.152398  │
+ [text] │ Constitutional Union  ┆ 1860 ┆ John Bell          ┆ 590901       ┆ loss   ┆ 12.639283 │
+ [text] │ Democratic            ┆ 2024 ┆ Woodrow Wilson     ┆ 81268924     ┆ win    ┆ 61.344703 │
+ [text] │ Democratic-Republican ┆ 1824 ┆ John Quincy Adams  ┆ 151271       ┆ win    ┆ 57.210122 │
+ [text] └───────────────────────┴──────┴────────────────────┴──────────────┴────────┴───────────┘
```

**Why:** The deliberately wrong "max of every column independently" table, re-executed. Same ten parties alphabetically (via the added `.sort("Party")`, since Polars does not order groups) and the same absurdity the section is built on: Democratic shows Woodrow Wilson winning in 2024. One difference is in the baseline's favour to lose -- its committed output carried a `First Name` column that the chapter does not create until seventeen cells later, an artifact of out-of-order execution; the Polars table has the six columns that exist at this point.
**Reader sees:** equivalent

<a id="c148"></a>
### C148 · `elections_sorted_by_percent = elections.sort("%", descending=True)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 6)
+ [text] ┌──────┬────────────────────┬────────────┬──────────────┬────────┬───────────┐
+ [text] │ Year ┆ Candidate          ┆ Party      ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---  ┆ ---                ┆ ---        ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ i64  ┆ str                ┆ str        ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞══════╪════════════════════╪════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 1964 ┆ Lyndon Johnson     ┆ Democratic ┆ 43127041     ┆ win    ┆ 61.344703 │
+ [text] │ 1936 ┆ Franklin Roosevelt ┆ Democratic ┆ 27752648     ┆ win    ┆ 60.978107 │
+ [text] │ 1972 ┆ Richard Nixon      ┆ Republican ┆ 47168710     ┆ win    ┆ 60.907806 │
+ [text] │ 1920 ┆ Warren Harding     ┆ Republican ┆ 16144093     ┆ win    ┆ 60.574501 │
+ [text] │ 1984 ┆ Ronald Reagan      ┆ Republican ┆ 54455472     ┆ win    ┆ 59.023326 │
+ [text] └──────┴────────────────────┴────────────┴──────────────┴────────┴───────────┘
```

**Why:** `sort_values("%", ascending=False)` becomes `sort("%", descending=True)`, re-executed: same top five (Johnson, Roosevelt, Nixon, Harding, Reagan) in the same order, without the 114/91/120/79/133 row labels. `%` has no nulls, so nulls-first does not bite here.
**Reader sees:** equivalent

<a id="c149"></a>
### C149 · `best_per_party = elections_sorted_by_percent.group_by("Party", maintai` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (10, 6)
+ [text] ┌───────────────────────┬──────┬────────────────────────┬──────────────┬────────┬───────────┐
+ [text] │ Party                 ┆ Year ┆ Candidate              ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---                   ┆ ---  ┆ ---                    ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ str                   ┆ i64  ┆ str                    ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞═══════════════════════╪══════╪════════════════════════╪══════════════╪════════╪═══════════╡
+ [text] │ Democratic            ┆ 1964 ┆ Lyndon Johnson         ┆ 43127041     ┆ win    ┆ 61.344703 │
+ [text] │ Republican            ┆ 1972 ┆ Richard Nixon          ┆ 47168710     ┆ win    ┆ 60.907806 │
+ [text] │ Democratic-Republican ┆ 1824 ┆ Andrew Jackson         ┆ 151271       ┆ loss   ┆ 57.210122 │
+ [text] │ National Union        ┆ 1864 ┆ Abraham Lincoln        ┆ 2211317      ┆ win    ┆ 54.951512 │
+ [text] │ Whig                  ┆ 1840 ┆ William Henry Harrison ┆ 1275583      ┆ win    ┆ 53.051213 │
+ [text] │ Liberal Republican    ┆ 1872 ┆ Horace Greeley         ┆ 2834761      ┆ loss   ┆ 44.071406 │
+ [text] │ National Republican   ┆ 1828 ┆ John Quincy Adams      ┆ 500897       ┆ loss   ┆ 43.796073 │
+ [text] │ Northern Democratic   ┆ 1860 ┆ Stephen A. Douglas     ┆ 1380202      ┆ loss   ┆ 29.522311 │
+ [text] │ Progressive           ┆ 1912 ┆ Theodore Roosevelt     ┆ 4122721      ┆ loss   ┆ 27.457433 │
+ [text] │ American              ┆ 1856 ┆ Millard Fillmore       ┆ 873053       ┆ loss   ┆ 21.554001 │
+ [text] └───────────────────────┴──────┴────────────────────────┴──────────────┴────────┴───────────┘
```

**Why:** `group_by("Party", maintain_order=True).head(1)` on the %-sorted frame, re-executed. `maintain_order=True` makes the groups come out in order of first appearance -- that is, by descending best `%` -- so the ten parties listed are the ten most successful, where pandas' `agg(lambda x: x.iloc[0])` listed the alphabetically first ten. The row the prose points at, Lyndon Johnson 1964 at 61.34%, is still there, now first instead of ninth.
**Reader sees:** changed: the ten parties shown are a different ten (best-% order, not alphabetical), and `Party` is a column rather than the index; the sort-then-take-first lesson is intact

<a id="c150"></a>
### C150 · `best_positions = (` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 2)
+ [text] ┌──────────────────────┬──────────┐
+ [text] │ Party                ┆ position │
+ [text] │ ---                  ┆ ---      │
+ [text] │ str                  ┆ u32      │
+ [text] ╞══════════════════════╪══════════╡
+ [text] │ American             ┆ 22       │
+ [text] │ American Independent ┆ 115      │
+ [text] │ Anti-Masonic         ┆ 6        │
+ [text] │ Anti-Monopoly        ┆ 38       │
+ [text] │ Citizens             ┆ 127      │
+ [text] └──────────────────────┴──────────┘
```

**Why:** An intermediate step the baseline did not have: `with_row_index` plus `arg_max` inside `.agg`, giving each party's winning row position, because Polars has no `idxmax`-into-`.loc`. The positions printed -- 22, 115, 6, 38, 127 -- are exactly the index labels the baseline's `elections.loc[...]` selection displayed.
**Reader sees:** new: the baseline did this in one `.loc[groupby().idxmax()]` line and never showed the positions

<a id="c151"></a>
### C151 · `elections[best_positions["position"]].sort("Party").head()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 6)
+ [text] ┌──────┬──────────────────┬──────────────────────┬──────────────┬────────┬───────────┐
+ [text] │ Year ┆ Candidate        ┆ Party                ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---  ┆ ---              ┆ ---                  ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ i64  ┆ str              ┆ str                  ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞══════╪══════════════════╪══════════════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 1856 ┆ Millard Fillmore ┆ American             ┆ 873053       ┆ loss   ┆ 21.554001 │
+ [text] │ 1968 ┆ George Wallace   ┆ American Independent ┆ 9901118      ┆ loss   ┆ 13.571218 │
+ [text] │ 1832 ┆ William Wirt     ┆ Anti-Masonic         ┆ 100715       ┆ loss   ┆ 7.821583  │
+ [text] │ 1884 ┆ Benjamin Butler  ┆ Anti-Monopoly        ┆ 134294       ┆ loss   ┆ 1.335838  │
+ [text] │ 1980 ┆ Barry Commoner   ┆ Citizens             ┆ 233052       ┆ loss   ┆ 0.270182  │
+ [text] └──────┴──────────────────┴──────────────────────┴──────────────┴────────┴───────────┘
```

**Why:** The positional take that finishes the `arg_max` route, re-executed, with `.sort("Party")` because a positional gather has no order of its own. Same five rows as the baseline's `idxmax` result -- Fillmore, Wallace, Wirt, Butler, Commoner -- with the row labels gone.
**Reader sees:** equivalent

<a id="c152"></a>
### C152 · `best_per_party2 = elections.sort("%").unique(subset=["Party"], keep="l` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 6)
+ [text] ┌──────┬──────────────────┬──────────────────────┬──────────────┬────────┬───────────┐
+ [text] │ Year ┆ Candidate        ┆ Party                ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---  ┆ ---              ┆ ---                  ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ i64  ┆ str              ┆ str                  ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞══════╪══════════════════╪══════════════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 1856 ┆ Millard Fillmore ┆ American             ┆ 873053       ┆ loss   ┆ 21.554001 │
+ [text] │ 1968 ┆ George Wallace   ┆ American Independent ┆ 9901118      ┆ loss   ┆ 13.571218 │
+ [text] │ 1832 ┆ William Wirt     ┆ Anti-Masonic         ┆ 100715       ┆ loss   ┆ 7.821583  │
+ [text] │ 1884 ┆ Benjamin Butler  ┆ Anti-Monopoly        ┆ 134294       ┆ loss   ┆ 1.335838  │
+ [text] │ 1980 ┆ Barry Commoner   ┆ Citizens             ┆ 233052       ┆ loss   ┆ 0.270182  │
+ [text] └──────┴──────────────────┴──────────────────────┴──────────────┴────────┴───────────┘
```

**Why:** `drop_duplicates(subset, keep="last")` becomes `unique(subset=["Party"], keep="last", maintain_order=True)`, re-executed, then `.sort("Party")` for a stable head. The baseline's `head(5)` inherited the ascending-% order and so showed Natural Law, Constitution, States' Rights, Taxpayers and New Alliance -- the five weakest parties, which was an artifact rather than the point.
**Reader sees:** changed: the five rows shown are American through Citizens instead of the baseline's five lowest-% parties; the one-row-per-party result is the same

<a id="c153"></a>
### C153 · `grouped_by_party = elections.group_by("Party")` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] polars.dataframe.group_by.GroupBy
```

**Why:** `type(...)` on a Polars `GroupBy`, re-executed: `polars.dataframe.group_by.GroupBy` where pandas printed `pandas.core.groupby.generic.DataFrameGroupBy`. Same lesson -- grouping yields an object, not a frame.
**Reader sees:** equivalent

<a id="c154"></a>
### C154 · `groups = dict(grouped_by_party)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] [('American',),
+ [text]  ('American Independent',),
+ [text]  ('Anti-Masonic',),
+ [text]  ('Anti-Monopoly',),
+ [text]  ('Citizens',),
+ [text]  ('Communist',)]
```

**Why:** Polars has no `.groups`, so the cell iterates the `GroupBy` into a dict and prints six sorted keys. Each key is a one-element tuple because `group_by` keys are always tuples. The baseline printed a dict mapping every party to its list of row labels -- which Polars cannot produce, having no row labels.
**Reader sees:** changed: six group keys instead of the full party-to-row-label dictionary; the per-group row positions are gone with the index

<a id="c155"></a>
### C155 · `groups[("Socialist",)]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (10, 6)
+ [text] ┌──────┬─────────────────┬───────────┬──────────────┬────────┬──────────┐
+ [text] │ Year ┆ Candidate       ┆ Party     ┆ Popular vote ┆ Result ┆ %        │
+ [text] │ ---  ┆ ---             ┆ ---       ┆ ---          ┆ ---    ┆ ---      │
+ [text] │ i64  ┆ str             ┆ str       ┆ i64          ┆ str    ┆ f64      │
+ [text] ╞══════╪═════════════════╪═══════════╪══════════════╪════════╪══════════╡
+ [text] │ 1904 ┆ Eugene V. Debs  ┆ Socialist ┆ 402810       ┆ loss   ┆ 2.985897 │
+ [text] │ 1908 ┆ Eugene V. Debs  ┆ Socialist ┆ 420852       ┆ loss   ┆ 2.850866 │
+ [text] │ 1912 ┆ Eugene V. Debs  ┆ Socialist ┆ 901551       ┆ loss   ┆ 6.004354 │
+ [text] │ 1916 ┆ Allan L. Benson ┆ Socialist ┆ 590524       ┆ loss   ┆ 3.194193 │
+ [text] │ 1920 ┆ Eugene V. Debs  ┆ Socialist ┆ 913693       ┆ loss   ┆ 3.428282 │
+ [text] │ 1928 ┆ Norman Thomas   ┆ Socialist ┆ 267478       ┆ loss   ┆ 0.728623 │
+ [text] │ 1932 ┆ Norman Thomas   ┆ Socialist ┆ 884885       ┆ loss   ┆ 2.236211 │
+ [text] │ 1936 ┆ Norman Thomas   ┆ Socialist ┆ 187910       ┆ loss   ┆ 0.412876 │
+ [text] │ 1940 ┆ Norman Thomas   ┆ Socialist ┆ 116599       ┆ loss   ┆ 0.234237 │
+ [text] │ 1948 ┆ Norman Thomas   ┆ Socialist ┆ 139569       ┆ loss   ┆ 0.286312 │
+ [text] └──────┴─────────────────┴───────────┴──────────────┴────────┴──────────┘
```

**Why:** `get_group("Socialist")` becomes `groups[("Socialist",)]`, re-executed. The same ten Socialist rows, 1904 through 1948, same candidates and percentages, minus the 58/62/66/... row labels.
**Reader sees:** equivalent

<a id="c156"></a>
### C156 · `babynames.group_by(["Year", "Sex"]).agg(pl.col("Count").sum()).sort(["` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (6, 3)
+ [text] ┌──────┬─────┬───────┐
+ [text] │ Year ┆ Sex ┆ Count │
+ [text] │ ---  ┆ --- ┆ ---   │
+ [text] │ i64  ┆ str ┆ i64   │
+ [text] ╞══════╪═════╪═══════╡
+ [text] │ 1910 ┆ F   ┆ 5950  │
+ [text] │ 1910 ┆ M   ┆ 3213  │
+ [text] │ 1911 ┆ F   ┆ 6602  │
+ [text] │ 1911 ┆ M   ┆ 3381  │
+ [text] │ 1912 ┆ F   ┆ 9804  │
+ [text] │ 1912 ┆ M   ┆ 8142  │
+ [text] └──────┴─────┴───────┘
```

**Why:** `group_by(["Year", "Sex"])` re-executed with `.sort(["Year", "Sex"])`. Polars has no MultiIndex, so `Year` and `Sex` come back as ordinary columns and `Year` is printed on every row rather than once per block. The six sums (5950, 3213, 6602, 3381, 9804, 8142) are the baseline's.
**Reader sees:** changed: the multi-index header becomes two repeated key columns -- which is also the setup the following `pivot` section now argues against

<a id="c157"></a>
### C157 · `babynames.pivot(` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 3)
+ [text] ┌──────┬───────┬───────┐
+ [text] │ Year ┆ F     ┆ M     │
+ [text] │ ---  ┆ ---   ┆ ---   │
+ [text] │ i64  ┆ i64   ┆ i64   │
+ [text] ╞══════╪═══════╪═══════╡
+ [text] │ 1910 ┆ 5950  ┆ 3213  │
+ [text] │ 1911 ┆ 6602  ┆ 3381  │
+ [text] │ 1912 ┆ 9804  ┆ 8142  │
+ [text] │ 1913 ┆ 11860 ┆ 10234 │
+ [text] │ 1914 ┆ 13815 ┆ 13111 │
+ [text] └──────┴───────┴───────┘
```

**Why:** `pivot_table(index, columns, values, aggfunc)` becomes `pivot(index, on, values, aggregate_function)`, re-executed. Same 1910-1914 rows and the same F/M totals; the Polars header has no `Sex` level name above the `F` and `M` columns.
**Reader sees:** equivalent

<a id="c158"></a>
### C158 · `babynames.pivot(` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (6, 5)
+ [text] ┌──────┬─────────┬─────────┬────────┬─────────┐
+ [text] │ Year ┆ Count_F ┆ Count_M ┆ Name_F ┆ Name_M  │
+ [text] │ ---  ┆ ---     ┆ ---     ┆ ---    ┆ ---     │
+ [text] │ i64  ┆ i64     ┆ i64     ┆ str    ┆ str     │
+ [text] ╞══════╪═════════╪═════════╪════════╪═════════╡
+ [text] │ 1910 ┆ 295     ┆ 237     ┆ Yvonne ┆ William │
+ [text] │ 1911 ┆ 390     ┆ 214     ┆ Zelma  ┆ Willis  │
+ [text] │ 1912 ┆ 534     ┆ 501     ┆ Yvonne ┆ Woodrow │
+ [text] │ 1913 ┆ 584     ┆ 614     ┆ Zelma  ┆ Yoshio  │
+ [text] │ 1914 ┆ 773     ┆ 769     ┆ Zelma  ┆ Yoshio  │
+ [text] │ 1915 ┆ 998     ┆ 1033    ┆ Zita   ┆ Yukio   │
+ [text] └──────┴─────────┴─────────┴────────┴─────────┘
```

**Why:** The two-value pivot, re-executed. pandas built a two-level column header (`Count`/`Name` over `F`/`M`); Polars emits flat `Count_F`, `Count_M`, `Name_F`, `Name_M` and the `Sex` column name does not appear at all. Same six years and the same values, including the mismatched-name point the prose makes about 1910.
**Reader sees:** changed: hierarchical columns become flat `{value}_{Sex}` names; the numbers are identical

<a id="c159"></a>
### C159 · `elections = elections.with_columns(` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 7)
+ [text] ┌──────┬───────────────────┬──────────────────────┬──────────────┬────────┬───────────┬────────────┐
+ [text] │ Year ┆ Candidate         ┆ Party                ┆ Popular vote ┆ Result ┆ %         ┆ First Name │
+ [text] │ ---  ┆ ---               ┆ ---                  ┆ ---          ┆ ---    ┆ ---       ┆ ---        │
+ [text] │ i64  ┆ str               ┆ str                  ┆ i64          ┆ str    ┆ f64       ┆ str        │
+ [text] ╞══════╪═══════════════════╪══════════════════════╪══════════════╪════════╪═══════════╪════════════╡
+ [text] │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republica ┆ 151271       ┆ loss   ┆ 57.210122 ┆ Andrew     │
+ [text] │      ┆                   ┆ n                    ┆              ┆        ┆           ┆            │
+ [text] │ 1824 ┆ John Quincy Adams ┆ Democratic-Republica ┆ 113142       ┆ win    ┆ 42.789878 ┆ John       │
+ [text] │      ┆                   ┆ n                    ┆              ┆        ┆           ┆            │
+ [text] │ 1828 ┆ Andrew Jackson    ┆ Democratic           ┆ 642806       ┆ win    ┆ 56.203927 ┆ Andrew     │
+ [text] │ 1828 ┆ John Quincy Adams ┆ National Republican  ┆ 500897       ┆ loss   ┆ 43.796073 ┆ John       │
+ [text] │ 1832 ┆ Andrew Jackson    ┆ Democratic           ┆ 702735       ┆ win    ┆ 54.574789 ┆ Andrew     │
+ [text] └──────┴───────────────────┴──────────────────────┴──────────────┴────────┴───────────┴────────────┘
```

**Why:** `.str.split(" ").list.get(0)` in `with_columns` replaces `.str.split().str[0]`, re-executed. Same five rows and the same `First Name` values; the Polars repr is narrower than the terminal, so `Democratic-Republican` wraps onto a continuation line.
**Reader sees:** equivalent

<a id="c160"></a>
### C160 · `babynames_2022 = babynames.filter(pl.col("Year") == 2022)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 5)
+ [text] ┌───────┬─────┬──────┬────────┬───────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name   ┆ Count │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---    ┆ ---   │
+ [text] │ str   ┆ str ┆ i64  ┆ str    ┆ i64   │
+ [text] ╞═══════╪═════╪══════╪════════╪═══════╡
+ [text] │ CA    ┆ F   ┆ 2022 ┆ Olivia ┆ 2178  │
+ [text] │ CA    ┆ F   ┆ 2022 ┆ Emma   ┆ 2080  │
+ [text] │ CA    ┆ F   ┆ 2022 ┆ Camila ┆ 2046  │
+ [text] │ CA    ┆ F   ┆ 2022 ┆ Mia    ┆ 1882  │
+ [text] │ CA    ┆ F   ┆ 2022 ┆ Sophia ┆ 1762  │
+ [text] └───────┴─────┴──────┴────────┴───────┘
```

**Why:** `babynames[babynames["Year"]==2022]` becomes `filter(pl.col("Year") == 2022)`, re-executed. Same Olivia/Emma/Camila/Mia/Sophia rows and counts; the 235835-onward row labels are gone, which is the visible cost of having no index.
**Reader sees:** equivalent

<a id="c161"></a>
### C161 · `merged = elections.join(` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 11)
+ [text] ┌──────┬──────────────────┬──────────────────┬──────────────┬───┬───────┬─────┬────────────┬───────┐
+ [text] │ Year ┆ Candidate        ┆ Party            ┆ Popular vote ┆ … ┆ State ┆ Sex ┆ Year_right ┆ Count │
+ [text] │ ---  ┆ ---              ┆ ---              ┆ ---          ┆   ┆ ---   ┆ --- ┆ ---        ┆ ---   │
+ [text] │ i64  ┆ str              ┆ str              ┆ i64          ┆   ┆ str   ┆ str ┆ i64        ┆ i64   │
+ [text] ╞══════╪══════════════════╪══════════════════╪══════════════╪═══╪═══════╪═════╪════════════╪═══════╡
+ [text] │ 1824 ┆ Andrew Jackson   ┆ Democratic-Repub ┆ 151271       ┆ … ┆ CA    ┆ M   ┆ 2022       ┆ 741   │
+ [text] │      ┆                  ┆ lican            ┆              ┆   ┆       ┆     ┆            ┆       │
+ [text] │ 1824 ┆ John Quincy      ┆ Democratic-Repub ┆ 113142       ┆ … ┆ CA    ┆ M   ┆ 2022       ┆ 490   │
+ [text] │      ┆ Adams            ┆ lican            ┆              ┆   ┆       ┆     ┆            ┆       │
+ [text] │ 1828 ┆ Andrew Jackson   ┆ Democratic       ┆ 642806       ┆ … ┆ CA    ┆ M   ┆ 2022       ┆ 741   │
+ [text] │ 1828 ┆ John Quincy      ┆ National         ┆ 500897       ┆ … ┆ CA    ┆ M   ┆ 2022       ┆ 490   │
+ [text] │      ┆ Adams            ┆ Republican       ┆              ┆   ┆       ┆     ┆            ┆       │
+ [text] │ 1832 ┆ Andrew Jackson   ┆ Democratic       ┆ 702735       ┆ … ┆ CA    ┆ M   ┆ 2022       ┆ 741   │
+ [text] └──────┴──────────────────┴──────────────────┴──────────────┴───┴───────┴─────┴────────────┴───────┘
```

**Why:** `pd.merge` becomes `elections.join(..., maintain_order="left")`, re-executed. Same five rows and the same Andrew 741 / John 490 counts, but Polars keeps the left column name and suffixes only the right, so the baseline's `Year_x`/`Year_y` are now `Year`/`Year_right`. Eleven columns exceed the repr width, so Polars elides the middle with a `...` column where pandas wrapped them onto a second block.
**Reader sees:** changed: the merge suffixes the prose used to name are now `Year` and `Year_right`, and the wide table is elided rather than wrapped -- which is why C159 exists

<a id="c162"></a>
### C162 · `merged.columns` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] ['Year',
+ [text]  'Candidate',
+ [text]  'Party',
+ [text]  'Popular vote',
+ [text]  'Result',
+ [text]  '%',
+ [text]  'First Name',
+ [text]  'State',
+ [text]  'Sex',
+ [text]  'Year_right',
+ [text]  'Count']
```

**Why:** Added so the column list the elided repr hides is still readable: eleven names, ending `Year_right`, `Count`. pandas' wrapped display showed every column without needing this.
**Reader sees:** new: a cell that exists to recover what the Polars repr elides

<a id="c163"></a>
### C163 · `elections.join(babynames_2022, left_on="First Name", right_on="Name", ` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 7)
+ [text] ┌──────┬──────────────────┬────────────────────┬──────────────┬────────┬───────────┬────────────┐
+ [text] │ Year ┆ Candidate        ┆ Party              ┆ Popular vote ┆ Result ┆ %         ┆ First Name │
+ [text] │ ---  ┆ ---              ┆ ---                ┆ ---          ┆ ---    ┆ ---       ┆ ---        │
+ [text] │ i64  ┆ str              ┆ str                ┆ i64          ┆ str    ┆ f64       ┆ str        │
+ [text] ╞══════╪══════════════════╪════════════════════╪══════════════╪════════╪═══════════╪════════════╡
+ [text] │ 1852 ┆ Winfield Scott   ┆ Whig               ┆ 1386942      ┆ loss   ┆ 44.056548 ┆ Winfield   │
+ [text] │ 1856 ┆ Millard Fillmore ┆ American           ┆ 873053       ┆ loss   ┆ 21.554001 ┆ Millard    │
+ [text] │ 1868 ┆ Horatio Seymour  ┆ Democratic         ┆ 2708744      ┆ loss   ┆ 47.334695 ┆ Horatio    │
+ [text] │ 1872 ┆ Horace Greeley   ┆ Liberal Republican ┆ 2834761      ┆ loss   ┆ 44.071406 ┆ Horace     │
+ [text] │ 1876 ┆ Rutherford Hayes ┆ Republican         ┆ 4034142      ┆ win    ┆ 48.471624 ┆ Rutherford │
+ [text] └──────┴──────────────────┴────────────────────┴──────────────┴────────┴───────────┴────────────┘
```

**Why:** An `how="anti"` join, re-executed: the candidates whose first name no 2022 CA baby carried -- Winfield, Millard, Horatio, Horace, Rutherford. The result keeps only the left frame's seven columns, which is what makes `anti` a filter rather than a join.
**Reader sees:** new: the old chapter taught only the default inner merge; `semi`/`anti` are added material

