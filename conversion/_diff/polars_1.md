# polars_1 — change report

`887a578b0a4b:content/pandas_2/pandas_2.ipynb` → `content/polars_1/polars_1.ipynb`

**Tier D · 173 changes:** output 79 · prose 26 · mixed 8 · dropdown 4 · tab-twins 27 · code 27 · metadata 1 · whitespace 1

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

> **Authored rewrite.** This chapter was renamed and re-written rather than converted cell by cell, so the diff below is not a cell-for-cell correspondence — whole sections were dropped, merged from another chapter, or written fresh. Read it as an inventory of what the reader gains and loses, not as a list of edits. `conversion/chapter_map.yml` records the lineage.

## Summary

This is not a conversion of `pandas_2` but a chapter authored over two parents: `pandas_1`'s `DataFrame`/`Series` construction, attributes and `[]` extraction (minus everything about the Index) in the front half, and `pandas_2`'s utility functions, column edits and sorting in the back half. A reader of the old chapters loses the Index outright — `.loc`, `.iloc`, label-versus-position, selection with an explicit `[True, False, ...]` mask, the `logical_operator` demo and its length/`iloc` prints, `.size`, `sort_values(key=...)`, and the "just about any `NumPy` function can be applied" section — and gains two-argument `[]`, `select`/`filter`, `.row()`, `with_row_index`, `.height`/`.width`, an `is_in`-first filter section, a null-sort warning with its own worked demo, and 27 pandas/Polars comparison tab-sets. All 80 committed outputs were regenerated under polars 1.43.1; none carried over, and because the two sides are not cell-aligned, the "before" pane of most output entries below belongs to an unrelated cell. Three things worth staff time: the `.describe()` tab-set (C28/C149), where the new sentence "Text columns are described too" is true of the Polars pane only and the pandas pane lacks the `null_count` row the next paragraph reads off; the ascending-sort tab-set (C66/C67/C164), whose two panes show five completely different rows because thousands of rows tie at `Count == 5` — a tie-break artifact presented as a library difference, the same failure class as CONTRADICTIONS.md §B1; and the `drop("Name")` demo (C163), where the comment promises a table without `Name` and the only committed output is the following `head()`, which still has it (pre-existing — baseline cell `06f920ff` has the same shape).

## Needs review

- [C1](#c1) · cell 1 [markdown]
- [C2](#c2) · cell 1 [markdown]
- [C3](#c3) · cell 1 [markdown]
- [C4](#c4) · cell 1 [markdown]
- [C8](#c8) · cell 169: We won't cover it explicitly in this class, but you are welc
- [C11](#c11) · cell 172: More Ways to Build a Filter
- [C12](#c12) · cell 172: More Ways to Build a Filter
- [C17](#c17) · cell 191: `.shape`, `.height`, and `.width`
- [C19](#c19) · cell 193 [markdown]
- [C22](#c22) · cell 199: `.describe()`
- [C23](#c23) · cell 199: `.describe()`
- [C25](#c25) · cell 11 [markdown]
- [C30](#c30) · cell 209 [markdown]
- [C32](#c32) · cell 211 [markdown]
- [C34](#c34) · cell 213 [markdown]
- [C38](#c38) · cell 221 [markdown]
- [C41](#c41) · cell 223 [markdown]
- [C44](#c44) · cell 229: Adding, Removing, and Modifying Columns
- [C47](#c47) · cell 231 [markdown]
- [C51](#c51) · cell 35 [markdown]
- [C56](#c56) · cell 39: Useful Utility Functions
- [C57](#c57) · cell 39: Useful Utility Functions
- [C61](#c61) · cell 250: Sorting
- [C62](#c62) · cell 250: Sorting
- [C64](#c64) · cell 252 [markdown]
- [C69](#c69) · cell 255 [markdown]
- [C74](#c74) · cell 57: `.unique()`
- [C75](#c75) · cell 57: `.unique()`
- [C78](#c78) · cell 261 [markdown]
- [C84](#c84) · cell 66 [code]
- [C85](#c85) · cell 73: Approach 3: Sorting using the `map` Function
- [C86](#c86) · cell 73: Approach 3: Sorting using the `map` Function
- [C91](#c91) · cell 287 [markdown]
- [C94](#c94) · cell 293: Parting Note

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C95](#c95) · `elections = pl.read_csv("data/elections.csv")` · no matching baseline cell — compare against the chapter, not the hunk
- [C96](#c96) · `pl.read_csv("data/elections.csv", columns=["Candidate", "Year", "%"])` · no matching baseline cell — compare against the chapter, not the hunk
- [C97](#c97) · `pl.read_csv("data/elections.csv", n_rows=5)` · no matching baseline cell — compare against the chapter, not the hunk
- [C98](#c98) · `df_list_1 = pl.DataFrame(` · no matching baseline cell — compare against the chapter, not the hunk
- [C99](#c99) · `df_list_2 = pl.DataFrame(` · no matching baseline cell — compare against the chapter, not the hunk
- [C100](#c100) · `df_dict = pl.DataFrame(` · no matching baseline cell — compare against the chapter, not the hunk
- [C101](#c101) · `ser_a = pl.Series("ser_a", ["a1", "a2", "a3"])` · no matching baseline cell — compare against the chapter, not the hunk
- [C102](#c102) · `pl.DataFrame(` · no matching baseline cell — compare against the chapter, not the hunk
- [C103](#c103) · `pl.DataFrame(ser_a)` · no matching baseline cell — compare against the chapter, not the hunk
- [C104](#c104) · `ser_a.to_frame()` · no matching baseline cell — compare against the chapter, not the hunk
- [C105](#c105) · `elections.columns` · no matching baseline cell — compare against the chapter, not the hunk
- [C106](#c106) · `elections.dtypes` · no matching baseline cell — compare against the chapter, not the hunk
- [C107](#c107) · `elections.schema` · no matching baseline cell — compare against the chapter, not the hunk
- [C108](#c108) · `elections.shape` · no matching baseline cell — compare against the chapter, not the hunk
- [C109](#c109) · `elections.head()` · no matching baseline cell — compare against the chapter, not the hunk
- [C110](#c110) · `elections.tail(5)` · no matching baseline cell — compare against the chapter, not the hunk
- [C111](#c111) · `elections[0, "Candidate"]` · no matching baseline cell — compare against the chapter, not the hunk
- [C112](#c112) · `elections[[87, 25, 179], ["Year", "Party", "%"]]` · no matching baseline cell — compare against the chapter, not the hunk
- [C113](#c113) · `elections[[87, 25, 179], "Popular vote":"%"]` · no matching baseline cell — compare against the chapter, not the hunk
- [C114](#c114) · `elections[:, ["Year", "Candidate", "Result"]]` · no matching baseline cell — compare against the chapter, not the hunk
- [C115](#c115) · `elections[[87, 25, 179], :]` · no matching baseline cell — compare against the chapter, not the hunk
- [C116](#c116) · `elections[[87, 25, 179], "Popular vote"]` · no matching baseline cell — compare against the chapter, not the hunk
- [C117](#c117) · `elections[[87, 25, 179], ["Popular vote"]]` · no matching baseline cell — compare against the chapter, not the hunk
- [C118](#c118) · `elections[[180, 181]]` · no matching baseline cell — compare against the chapter, not the hunk
- [C119](#c119) · `elections["Candidate"]` · no matching baseline cell — compare against the chapter, not the hunk
- [C120](#c120) · `elections[0, 1]` · no matching baseline cell — compare against the chapter, not the hunk
- [C121](#c121) · `elections[[1, 2, 3], 1]` · no matching baseline cell — compare against the chapter, not the hunk
- [C122](#c122) · `elections[[1, 2, 3], [0, 1, 2]]` · no matching baseline cell — compare against the chapter, not the hunk
- [C123](#c123) · `elections[[1, 2, 3], 0:3]` · no matching baseline cell — compare against the chapter, not the hunk
- [C124](#c124) · `elections[138:144]` · no matching baseline cell — compare against the chapter, not the hunk
- [C125](#c125) · `elections.row(0)` · no matching baseline cell — compare against the chapter, not the hunk
- [C126](#c126) · `elections.row(0, named=True)` · no matching baseline cell — compare against the chapter, not the hunk
- [C127](#c127) · `elections.select(["Year", "Candidate", "Result"])` · no matching baseline cell — compare against the chapter, not the hunk
- [C128](#c128) · `elections.select((pl.col("Popular vote") / 1_000_000).alias("Popular v` · no matching baseline cell — compare against the chapter, not the hunk
- [C129](#c129) · `elections.filter(pl.col("Popular vote") > 60000000)` · no matching baseline cell — compare against the chapter, not the hunk
- [C130](#c130) · `elections.filter(pl.col("Year") == 2008).select(["Year", "Candidate"])` · no matching baseline cell — compare against the chapter, not the hunk
- [C131](#c131) · `elections.filter((pl.col("Year") == 2008) | (pl.col("%") >= 60))` · no matching baseline cell — compare against the chapter, not the hunk
- [C132](#c132) · `elections.filter((pl.col("Year") > 2000) & (pl.col("Result") == "win")` · no matching baseline cell — compare against the chapter, not the hunk
- [C133](#c133) · `elections.filter((pl.col("Year") == 2008) and (pl.col("%") >= 60))`
- [C134](#c134) · `elections.filter(` · no matching baseline cell — compare against the chapter, not the hunk
- [C135](#c135) · `elections.with_row_index("original_position").sort("%", descending=Tru` · no matching baseline cell — compare against the chapter, not the hunk
- [C136](#c136) · `elections.head(3)` · no matching baseline cell — compare against the chapter, not the hunk
- [C137](#c137) · `elections.sort("%", descending=True).with_row_index().head()` · no matching baseline cell — compare against the chapter, not the hunk
- [C138](#c138) · `import urllib.request` · no matching baseline cell — compare against the chapter, not the hunk
- [C139](#c139) · `(` · no matching baseline cell — compare against the chapter, not the hunk
- [C140](#c140) · `names = ["Bella", "Alex", "Narges", "Lisa"]` · no matching baseline cell — compare against the chapter, not the hunk
- [C141](#c141) · `babynames.filter(pl.col("Name").str.starts_with("N"))` · no matching baseline cell — compare against the chapter, not the hunk
- [C142](#c142) · `yash_counts = babynames.filter(pl.col("Name") == "Yash")["Count"]` · no matching baseline cell — compare against the chapter, not the hunk
- [C143](#c143) · `yash_counts.mean()` · no matching baseline cell — compare against the chapter, not the hunk
- [C144](#c144) · `yash_counts.max()` · no matching baseline cell — compare against the chapter, not the hunk
- [C145](#c145) · `babynames.shape` · no matching baseline cell — compare against the chapter, not the hunk
- [C146](#c146) · `babynames.height * babynames.width` · no matching baseline cell — compare against the chapter, not the hunk
- [C147](#c147) · `len(babynames)` · no matching baseline cell — compare against the chapter, not the hunk
- [C148](#c148) · `babynames.describe()` · no matching baseline cell — compare against the chapter, not the hunk
- [C149](#c149) · `babynames["Sex"].describe()` · no matching baseline cell — compare against the chapter, not the hunk
- [C150](#c150) · `babynames.sample()` · no matching baseline cell — compare against the chapter, not the hunk
- [C151](#c151) · `babynames.sample(5)[:, 2:]` · no matching baseline cell — compare against the chapter, not the hunk
- [C152](#c152) · `result = (` · no matching baseline cell — compare against the chapter, not the hunk
- [C153](#c153) · `babynames["Sex"].value_counts()` · no matching baseline cell — compare against the chapter, not the hunk
- [C154](#c154) · `babynames["Name"].value_counts(sort=True).head()` · no matching baseline cell — compare against the chapter, not the hunk
- [C155](#c155) · `babynames["Name"].unique()` · no matching baseline cell — compare against the chapter, not the hunk
- [C156](#c156) · `babynames["Name"].n_unique()` · no matching baseline cell — compare against the chapter, not the hunk
- [C157](#c157) · `babynames["Name"].unique(maintain_order=True).head(5)` · no matching baseline cell — compare against the chapter, not the hunk
- [C158](#c158) · `babyname_lengths = babynames["Name"].str.len_chars()` · no matching baseline cell — compare against the chapter, not the hunk
- [C159](#c159) · `babynames = babynames.with_columns(name_lengths=pl.col("name_lengths")` · no matching baseline cell — compare against the chapter, not the hunk
- [C160](#c160) · `babynames = babynames.rename({"name_lengths": "Length"})` · no matching baseline cell — compare against the chapter, not the hunk
- [C161](#c161) · `babynames = babynames.drop("Length")` · no matching baseline cell — compare against the chapter, not the hunk
- [C162](#c162) · `babynames.drop("Name")` · no matching baseline cell — compare against the chapter, not the hunk
- [C163](#c163) · `babynames.sort("Count").head()` · no matching baseline cell — compare against the chapter, not the hunk
- [C164](#c164) · `babynames.sort("Count", descending=True).head()` · no matching baseline cell — compare against the chapter, not the hunk
- [C165](#c165) · `babynames["Name"].sort().head(5)` · no matching baseline cell — compare against the chapter, not the hunk
- [C166](#c166) · `demo = pl.DataFrame({"Name": ["Aaliyah", "Bao", "Cyrus"], "Count": [3,` · no matching baseline cell — compare against the chapter, not the hunk
- [C167](#c167) · `demo.sort("Count", descending=True, nulls_last=True)` · no matching baseline cell — compare against the chapter, not the hunk
- [C168](#c168) · `babyname_lengths = babynames["Name"].str.len_chars()` · no matching baseline cell — compare against the chapter, not the hunk
- [C169](#c169) · `babynames = babynames.sort(by="name_lengths", descending=True)` · no matching baseline cell — compare against the chapter, not the hunk
- [C170](#c170) · `babynames = babynames.drop("name_lengths")` · no matching baseline cell — compare against the chapter, not the hunk
- [C171](#c171) · `babynames.sort(pl.col("Name").str.len_chars(), descending=True).head()` · no matching baseline cell — compare against the chapter, not the hunk
- [C172](#c172) · `def dr_ea_count(string):` · no matching baseline cell — compare against the chapter, not the hunk
- [C173](#c173) · `babynames = babynames.drop("dr_ea_count")` · no matching baseline cell — compare against the chapter, not the hunk

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C6](#c6) · cell 1: We won't cover it explicitly in this class, but you are welc
- [C7](#c7) · cell 169: We won't cover it explicitly in this class, but you are welc
- [C26](#c26) · cell 11 [markdown]
- [C80](#c80) · cell 63: Custom Sorts

## Changes

<a id="c1"></a>
### C1 · cell 1 [markdown] · prose · **REVIEW**

baseline L17 → branch L17

```diff
- # title: Pandas II
+ # title: Polars I
```

**Why:** Chapter renamed with the `content/pandas_2` -> `content/polars_1` `git mv`; allowlisted under `polars_1: frontmatter`. The numbered title keeps the convention this slot already used (`Pandas I/II/III`), which the allowlist records as the deliberate exception to the book's descriptive titles.
**Verdict:** necessary

<a id="c2"></a>
### C2 · cell 1 [markdown] · prose · **REVIEW**

baseline L21 → branch L21

```diff
- # :class: dropdown
- # * Continue building familiarity with `pandas` syntax.
- # * Extract data from a `DataFrame` using conditional selection.
- # * Recognize situations where aggregation is useful and identify the correct technique for performing an aggregation.
+ # * Build a `DataFrame` from a file, a list of rows, a dictionary of columns, or a `Series`, and describe it with `columns`, `dtypes`, `schema`, and `shape`.
+ # * Extract rows and columns using `[]`, `select`, and `filter`.
+ # * Combine filtering conditions with the bitwise boolean operators.
+ # * Address rows by position, and record those positions with `with_row_index`.
+ # * Summarize a table with utility methods such as `.describe()`, `.sample()`, `.value_counts()`, and `.unique()`.
+ # * Add, modify, rename, and drop columns, and order a table with `.sort()`.
```

**Why:** Outcomes rewritten for a chapter with two parents: the four construction routes, `[]`/`select`/`filter`, bitwise operators, `with_row_index`, the utility methods and column/sort operations. `:class: dropdown` goes because the note is now an open `::: {note}`. "Recognize situations where aggregation is useful" is dropped here rather than lost -- aggregation is `polars_2`'s subject.
**Verdict:** necessary

<a id="c3"></a>
### C3 · cell 1 [markdown] · prose · **REVIEW**

baseline L27 → branch L29

```diff
- # Last time, we introduced the `pandas` library as a toolkit for processing data. We learned the `DataFrame` and `Series` data structures, familiarized ourselves with the basic syntax for manipulating tabular data, and began writing our first lines of `pandas` code.
+ # Last time, we met the `Series`: a named, one-dimensional sequence of values that all share a single data type. Almost no dataset arrives as one column, so we now turn to the structure that holds a whole table, the `DataFrame`, and to the operations that get data into and out of it.
```

**Why:** "Last time" pointed at `pandas_1`, which no longer exists. It now points at `intro_lec`'s `Series` material, which is where a reader actually met the `Series`.
**Verdict:** necessary

<a id="c4"></a>
### C4 · cell 1 [markdown] · prose · **REVIEW**

baseline L29 → branch L31

```diff
- # In this lecture, we'll start to dive into some advanced `pandas` syntax. You may find it helpful to follow along with a notebook of your own as we walk through these new pieces of code.
+ # We will work with two datasets in this chapter. The first records the results of United States presidential elections; the second records the names given to babies born in California.
```

**Why:** The chapter now runs on two datasets -- `elections`, carried in from `pandas_1`, and `babynames` from `pandas_2` -- so the opening names both instead of promising "advanced `pandas` syntax".
**Verdict:** necessary

<a id="c5"></a>
### C5 · cell 1 [markdown] · tab-twins

baseline L31 → branch L33 · spans code and prose

```diff
- # We'll start by loading the `babynames` dataset.
+ # Some sections below show the same operation both ways. Pick a library here and every comparison
+ # on this page follows it.
+ #
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # Comparisons on this page are showing **Polars**. This is the library the course uses.
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # Comparisons on this page are showing **pandas**, for readers arriving from it. The course itself
+ # uses Polars throughout.
+ # ::::
+ # :::::
+ 
+ # %% tags=["remove-input", "remove-output"]
+ # `pl` is the conventional alias for Polars, as `np` is for NumPy
+ import polars as pl
+ 
+ 
+ # %% [markdown]
+ #
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin import polars as pl -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # `pl` is the conventional alias for Polars, as `np` is for NumPy
+ # import polars as pl
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # `pd` is the conventional alias for pandas, as `np` is for NumPy
+ # import pandas as pd
+ … 2365 more lines
```

**Why:** New tab-set preamble plus the first tab-twin (`import polars as pl` / `import pandas as pd`), generated by `conversion/tab_twins.py`. The displaced line ("We'll start by loading the `babynames` dataset") moves ~2,300 lines down to where `babynames` is actually introduced.
**Output:** same -- the import cell is tagged `remove-input, remove-output` and both panes are import-only

<a id="c6"></a>
### C6 · cell 1: We won't cover it explicitly in this class, but you are welc · dropdown

baseline L38 → branch L2444 · mirror of the next code cell (hard rule 3)

```diff
- # import pandas as pd
- # import numpy as np
```

**Why:** The dropdown mirror of the download cell loses `import pandas as pd` / `import numpy as np`; the chapter imports neither. **Mirror checked:** the code cell it mirrors (C9) takes the identical deletion, so the two still match.
**Output:** same

<a id="c7"></a>
### C7 · cell 169: We won't cover it explicitly in this class, but you are welc · dropdown

baseline L55 → branch L2459 · mirror of the next code cell (hard rule 3)

```diff
- #     babynames = pd.read_csv(fh, header=None, names=field_names)
+ #     babynames = pl.read_csv(fh, has_header=False, new_columns=field_names)
```

**Why:** `pd.read_csv(fh, header=None, names=field_names)` -> `pl.read_csv(fh, has_header=False, new_columns=field_names)` inside the dropdown. **Mirror checked:** code cell `c8bfdae2` (C10) carries the identical line, so the dropdown and the cell are line-for-line identical in the branch.
**Output:** same -- 407,428 rows, same five column names

<a id="c8"></a>
### C8 · cell 169: We won't cover it explicitly in this class, but you are welc · prose · **REVIEW**

baseline L61 → branch L2465

```diff
+ 
+ # %% [markdown]
+ #
+ 
```

**Why:** An empty `# %% [markdown]` cell left behind by the tab-twin generator between a code cell and its twin block. It renders as nothing.
**Verdict:** optional
**Minimal alternative:** Delete the empty cell. Roughly fifteen of them appear through the chapter; they are tooling residue rather than content.

<a id="c9"></a>
### C9 · cell 2 [code] · code

baseline L64 → branch L2472

```diff
- import pandas as pd
- import numpy as np
```

**Why:** Both imports deleted. `pandas` is gone from the chapter, and no NumPy call survives the rewrite of the NumPy section into "Aggregation Methods" -- `np.mean(s)` and friends raise `TypeError: ... unexpected keyword argument 'axis'` on a Polars `Series`.
**Output:** same -- the cell is `remove-input` and renders only `babynames.head()`

<a id="c10"></a>
### C10 · cell 171 [code] · code

baseline L81 → branch L2487

```diff
-     babynames = pd.read_csv(fh, header=None, names=field_names)
+     babynames = pl.read_csv(fh, has_header=False, new_columns=field_names)
```

**Why:** `header=None, names=` -> `has_header=False, new_columns=`. Keyword rename; same file, same field names.
**Output:** same

<a id="c11"></a>
### C11 · cell 172: More Ways to Build a Filter · prose · **REVIEW**

baseline L86 → branch L2492

```diff
- # ## Conditional Selection
+ # ## More Ways to Build a Filter
```

**Why:** The old section taught conditional selection as "pass a boolean array to `.loc` or `[]`", which has no Polars form. `filter` already covers that ground earlier in the chapter, so the section is re-aimed at the shorthands (`is_in`, `.str.starts_with`) and renamed to match.
**Verdict:** necessary

<a id="c12"></a>
### C12 · cell 172: More Ways to Build a Filter · mixed · **REVIEW**

baseline L88 → branch L2494 · spans code and prose

```diff
- # Conditional selection allows us to select a subset of rows in a `DataFrame` that satisfy some specified condition.
+ # A boolean expression can describe any condition we can write down, but a long list of alternatives gets verbose in a hurry. Suppose we want every row whose name is one of four we care about.
+ 
+ # %% tags=["remove-input", "remove-output"]
+ # Note: The parentheses surrounding the code make it possible to
+ # break the code into multiple lines for readability. But this is
+ # still a lot of code just to check for four names...
+ (
+     babynames.filter((pl.col("Name") == "Bella") |
+                      (pl.col("Name") == "Alex") |
+                      (pl.col("Name") == "Narges") |
+                      (pl.col("Name") == "Lisa"))
+ )
+ 
+ 
+ # %% [markdown]
```

**Why:** Boolean-array-into-`[]` is gone with the Index; `[]` takes positions and labels only. The opening is re-pointed at the verbose four-way `|` filter that motivates `is_in` in the next cell.
**Verdict:** necessary

<a id="c13"></a>
### C13 · cell 174 [markdown] · tab-twins

baseline L90 → branch L2510

```diff
- # To understand how to use conditional selection, we must look at another possible input of the `.loc` and `[]` methods – a boolean array, which is simply an array or `Series` where each element is either `True` or `False`. This boolean array must have a length equal to the number of rows in the `DataFrame`. It will return all rows that correspond to a value of `True` in the array. We used a very similar technique when performing conditional extraction from a `Series` in the last lecture.
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin babynames.filter((pl.col("Name") == "Bella") | -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Note: The parentheses surrounding the code make it possible to
+ # # break the code into multiple lines for readability. But this is
+ # # still a lot of code just to check for four names...
+ # (
+ #     babynames.filter((pl.col("Name") == "Bella") |
+ #                      (pl.col("Name") == "Alex") |
+ #                      (pl.col("Name") == "Narges") |
+ #                      (pl.col("Name") == "Lisa"))
+ # )
+ # ```
```

**Why:** The paragraph explaining boolean arrays as an input to `.loc`/`[]` is replaced by the four-name filter's tab-twin.
**Output:** same -- 317 rows on both panes

<a id="c14"></a>
### C14 · cell 175: still a lot of code just to check for four names... · tab-twins

baseline L92 → branch L2528 · spans code and prose

```diff
- # To see this in action, let's select all even-indexed rows in the first 10 rows of our `DataFrame`.
+ # ```text
+ # shape: (317, 5)
+ # ┌───────┬─────┬──────┬───────┬───────┐
+ # │ State ┆ Sex ┆ Year ┆ Name  ┆ Count │
+ # │ ---   ┆ --- ┆ ---  ┆ ---   ┆ ---   │
+ # │ str   ┆ str ┆ i64  ┆ str   ┆ i64   │
+ # ╞═══════╪═════╪══════╪═══════╪═══════╡
+ # │ CA    ┆ F   ┆ 1923 ┆ Bella ┆ 5     │
+ # │ CA    ┆ F   ┆ 1925 ┆ Bella ┆ 8     │
+ # │ CA    ┆ F   ┆ 1932 ┆ Lisa  ┆ 5     │
+ # │ CA    ┆ F   ┆ 1936 ┆ Lisa  ┆ 8     │
+ # │ CA    ┆ F   ┆ 1939 ┆ Lisa  ┆ 5     │
+ # │ …     ┆ …   ┆ …    ┆ …     ┆ …     │
+ # │ CA    ┆ M   ┆ 2018 ┆ Alex  ┆ 495   │
+ # │ CA    ┆ M   ┆ 2019 ┆ Alex  ┆ 438   │
+ # │ CA    ┆ M   ┆ 2020 ┆ Alex  ┆ 379   │
+ # │ CA    ┆ M   ┆ 2021 ┆ Alex  ┆ 333   │
+ # │ CA    ┆ M   ┆ 2022 ┆ Alex  ┆ 344   │
+ # └───────┴─────┴──────┴───────┴───────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_pd[
+ #     (babynames_pd["Name"] == "Bella")
+ #     | (babynames_pd["Name"] == "Alex")
+ #     | (babynames_pd["Name"] == "Narges")
+ #     | (babynames_pd["Name"] == "Lisa")
+ # ]
+ # ```
+ #
+ # ```text
+ #        State Sex  Year   Name  Count
+ # 6289      CA   F  1923  Bella      5
+ # 7512      CA   F  1925  Bella      8
+ # 12368     CA   F  1932   Lisa      5
+ # 14741     CA   F  1936   Lisa      8
+ # 17084     CA   F  1939   Lisa      5
+ … 257 more lines
```

**Why:** Twin for the four-way `|` filter; the pandas pane keeps the bracket-mask spelling. The displaced sentence (selecting even-indexed rows) belonged to the deleted boolean-array demo.
**Output:** same -- 317 rows, same first five and last five rows; the pandas pane additionally shows the original row labels

<a id="c15"></a>
### C15 · cell 189 [code] · code

baseline L95 → branch L2827

```diff
- # Ask yourself: why is :9 is the correct slice to select the first 10 rows?
- babynames_first_10_rows = babynames.loc[:9, :]
+ # Average number of babies named Yash each year
+ # Keep in mind that even if Python gives you 10 decimal places of precision,
+ # you should think carefully about how much precision is meaningful!
+ # In this case, one decimal place or even no decimal places would be appropriate.
+ yash_counts.mean()
```

**Why:** Positional pairing only. The baseline cell (`.loc[:9, :]`) dies with the Index; the branch cell here is `yash_counts.mean()`, which replaces `np.mean(yash_count)` because the NumPy reduction raises on a Polars `Series`.
**Output:** differs: unrelated cells -- a 10-row frame against the scalar `17.142857142857142`

<a id="c16"></a>
### C16 · cell 190 [code] · code

baseline L98 → branch L2833

```diff
- # Notice how we have exactly 10 elements in our boolean array argument
- babynames_first_10_rows[[True, False, True, False, True, False, True, False, True, False]]
+ # %%
+ # Max number of babies named Yash born in any single year
+ yash_counts.max()
```

**Why:** Same positional pairing. The baseline's explicit `[True, False, ...]` mask has no Polars analog; the branch cell is `yash_counts.max()`, formerly `np.max(yash_count)`.
**Output:** differs: unrelated cells -- `29` against a filtered frame

<a id="c17"></a>
### C17 · cell 191: `.shape`, `.height`, and `.width` · prose · **REVIEW**

baseline L102 → branch L2838

```diff
- # We can perform a similar operation using `.loc`:
+ # ### `.shape`, `.height`, and `.width`
+ #
+ # These attributes measure the "amount" of data stored in a `DataFrame`. Calling `.shape` returns a tuple containing the number of rows followed by the number of columns.
+ #
+ # Many functions strictly require the dimensions of their arguments to match. Asking the table for its dimensions is much faster than counting the items by hand.
```

**Why:** `.size` does not exist in Polars, so the section is rebuilt around `.shape` plus `.height`/`.width`. The prose is `pandas_2`'s own "`.shape` and `.size`" text re-aimed at the three attributes that do exist.
**Verdict:** necessary

<a id="c18"></a>
### C18 · cell 192 [code] · code

baseline L105 → branch L2845

```diff
- babynames_first_10_rows.loc[[True, False, True, False, True, False, True, False, True, False], :]
+ # Return the shape of the DataFrame, in the format (num_rows, num_columns)
+ babynames.shape
```

**Why:** Positional pairing. `.loc[[True, ...], :]` dies with the Index; the branch cell is `babynames.shape`.
**Output:** differs: unrelated cells

<a id="c19"></a>
### C19 · cell 193 [markdown] · mixed · **REVIEW**

baseline L108 → branch L2849 · spans code and prose

```diff
- # These techniques worked well in this example, but you can imagine how tedious it might be to list out `True` and `False`for every row in a larger `DataFrame`. To make things easier, we can instead provide a logical condition as an input to `.loc` or `[]` that returns a boolean array with the necessary length.
+ # `.height` and `.width` report those same two numbers one at a time, so multiplying them gives the total number of values the table holds.
+ 
+ # %% tags=["remove-input", "remove-output"]
+ # The total number of entries in the object, equal to num_rows * num_columns
+ babynames.height * babynames.width
+ 
+ 
+ # %% [markdown]
```

**Why:** `.size` becomes the product `.height * .width`, stated as a multiplication rather than as an attribute, because Polars exposes the two dimensions separately and nothing that combines them.
**Verdict:** necessary

<a id="c20"></a>
### C20 · cell 195 [markdown] · tab-twins

baseline L110 → branch L2858

```diff
- # For example, to return all names associated with `F` sex:
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin babynames.height * babynames.width -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # The total number of entries in the object, equal to num_rows * num_columns
+ # babynames.height * babynames.width
+ # ```
+ #
+ # ```text
+ # 2037140
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_pd.size
+ # ```
+ #
+ # ```text
+ # 2037140
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
+ 
+ # %% [markdown]
+ # Calling `len` on a `DataFrame` gives its height, which is the number we want far more often than the other two.
```

**Why:** Twin pairing `babynames.height * babynames.width` with `babynames_pd.size`, plus the new sentence about `len`.
**Output:** same -- `2037140` on both panes

<a id="c21"></a>
### C21 · cell 198 [code] · code

baseline L113 → branch L2891

```diff
- # First, use a logical condition to generate a boolean array
- logical_operator = (babynames["Sex"] == "F")
- 
- # Then, use this boolean array to filter the DataFrame
- babynames[logical_operator].head()
+ # Return the number of rows in the DataFrame
+ len(babynames)
```

**Why:** Positional pairing. The baseline built `logical_operator` and filtered with it; the branch cell is `len(babynames)`.
**Output:** differs: unrelated cells -- `407428` against a five-row frame

<a id="c22"></a>
### C22 · cell 199: `.describe()` · prose · **REVIEW**

baseline L120 → branch L2895

```diff
- # Recall from the previous lecture that `.head()` will return only the first few rows in the `DataFrame`. In reality, `babynames[logical operator]` contains as many rows as there are entries in the original `babynames` `DataFrame` with sex `"F"`.
+ # ### `.describe()`
```

**Why:** Heading only. The `.describe()` section survives and keeps its heading; the baseline sentence displaced here belonged to the `logical_operator` demo.
**Verdict:** necessary

<a id="c23"></a>
### C23 · cell 199: `.describe()` · prose · **REVIEW**

baseline L122 → branch L2897

```diff
- # Here, `logical_operator` evaluates to a `Series` of boolean values with length 407428.
- #
- # ````{dropdown} Click to see the code
- # :open: false
- # ```python
- # print("There are a total of {} values in 'logical_operator'".format(len(logical_operator)))
- # ```
- # ````
+ # If many statistics are required from a `DataFrame` (minimum value, maximum value, mean value, etc.), then `.describe()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.describe.html) can be used to compute all of them at once.
```

**Why:** The `logical_operator` length demo and its dropdown are deleted with boolean-array selection. The `.describe()` paragraph moves in, with the pandas doc link swapped for the pola.rs one (G13 requires it).
**Verdict:** necessary

<a id="c24"></a>
### C24 · cell 200 [code] · code

baseline L131 → branch L2899

```diff
- # %% tags=["remove-input"]
- print("There are a total of {} values in 'logical_operator'".format(len(logical_operator)))
+ # %% tags=["remove-input", "remove-output"]
+ babynames.describe()
+ 
```

**Why:** Positional pairing: the deleted `print(len(logical_operator))` cell against the new `babynames.describe()` cell.
**Output:** differs: unrelated cells -- a stdout line against a 9x6 statistics table

<a id="c25"></a>
### C25 · cell 11 [markdown] · prose · **REVIEW**

baseline L135 → branch L2904

```diff
- # Rows starting at row 0 and ending at row 239536 evaluate to `True` and are thus returned in the `DataFrame`. Rows from 239537 onwards evaluate to `False` and are omitted from the output.
```

**Why:** The sentence names which row *labels* evaluate `True`. Row labels and the demo they describe are both gone.
**Verdict:** necessary

<a id="c26"></a>
### C26 · cell 11 [markdown] · dropdown

baseline L137 → branch L2905 · spans code and prose; mirror of the next code cell (hard rule 3)

```diff
- # ````{dropdown} Click to see the code
- # :open: false
- # ```python
- # print("The 0th item in this 'logical_operator' is: {}".format(logical_operator.iloc[0]))
- # print("The 239536th item in this 'logical_operator' is: {}".format(logical_operator.iloc[239536]))
- # print("The 239537th item in this 'logical_operator' is: {}".format(logical_operator.iloc[239537]))```
- # ````
- 
- # %% tags=["remove-input"]
- print("The 0th item in this 'logical_operator' is: {}".format(logical_operator.iloc[0]))
- print("The 239536th item in this 'logical_operator' is: {}".format(logical_operator.iloc[239536]))
- print("The 239537th item in this 'logical_operator' is: {}".format(logical_operator.iloc[239537]))
```

**Why:** Dropdown mirror deleted together with the `logical_operator.iloc[...]` code cell it mirrored. **Both halves go**, so hard rule 3 holds and no dropdown is left describing an output the reader cannot see.
**Output:** same -- both removed

<a id="c27"></a>
### C27 · cell 202 [markdown] · tab-twins

baseline L151 → branch L2907

```diff
- # Passing a `Series` as an argument to `babynames[]` has the same effect as using a boolean array. In fact, the `[]` selection operator can take a boolean `Series`, array, and list as arguments. These three are used interchangeably throughout the course.
+ # <!-- tab-twins:begin babynames.describe() -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # babynames.describe()
+ # ```
```

**Why:** The paragraph about passing a boolean `Series`/array/list into `[]` is replaced by the opening of the `.describe()` twin.
**Output:** differs: see C28

<a id="c28"></a>
### C28 · cell 202 [markdown] · tab-twins

baseline L153 → branch L2915 · spans code and prose

```diff
- # We can also use `.loc` to achieve similar results.
+ # ```text
+ # shape: (9, 6)
+ # ┌────────────┬────────┬────────┬─────────────┬────────┬────────────┐
+ # │ statistic  ┆ State  ┆ Sex    ┆ Year        ┆ Name   ┆ Count      │
+ # │ ---        ┆ ---    ┆ ---    ┆ ---         ┆ ---    ┆ ---        │
+ # │ str        ┆ str    ┆ str    ┆ f64         ┆ str    ┆ f64        │
+ # ╞════════════╪════════╪════════╪═════════════╪════════╪════════════╡
+ # │ count      ┆ 407428 ┆ 407428 ┆ 407428.0    ┆ 407428 ┆ 407428.0   │
+ # │ null_count ┆ 0      ┆ 0      ┆ 0.0         ┆ 0      ┆ 0.0        │
+ # │ mean       ┆ null   ┆ null   ┆ 1985.733609 ┆ null   ┆ 79.543456  │
+ # │ std        ┆ null   ┆ null   ┆ 27.00766    ┆ null   ┆ 293.698654 │
+ # │ min        ┆ CA     ┆ F      ┆ 1910.0      ┆ Aadan  ┆ 5.0        │
+ # │ 25%        ┆ null   ┆ null   ┆ 1969.0      ┆ null   ┆ 7.0        │
+ # │ 50%        ┆ null   ┆ null   ┆ 1992.0      ┆ null   ┆ 13.0       │
+ # │ 75%        ┆ null   ┆ null   ┆ 2008.0      ┆ null   ┆ 38.0       │
+ # │ max        ┆ CA     ┆ M      ┆ 2022.0      ┆ Zyrus  ┆ 8260.0     │
+ # └────────────┴────────┴────────┴─────────────┴────────┴────────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_pd.describe()
+ # ```
+ #
+ # ```text
+ #                 Year          Count
+ # count  407428.000000  407428.000000
+ # mean     1985.733609      79.543456
+ # std        27.007660     293.698654
+ # min      1910.000000       5.000000
+ # 25%      1969.000000       7.000000
+ # 50%      1992.000000      13.000000
+ # 75%      2008.000000      38.000000
+ # max      2022.000000    8260.000000
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
+ … 61 more lines
```

**Why:** `describe()` twin. **Flag for staff:** the Polars pane is 9x6 and describes `State`, `Sex` and `Name` as well as the numeric columns; the pandas pane is 8x2 and silently drops every non-numeric column. The new sentence under the twin ("Text columns are described too ... and carry `null` wherever a statistic makes no sense") is true of the Polars pane only, and the paragraph after it reads `null_count` off a row the pandas pane does not have. Same class of false pairing as CONTRADICTIONS.md §B1, introduced by this conversion and not currently recorded there.
**Output:** differs: Polars adds a `null_count` row and four string columns; the numbers agree wherever the two panes overlap

<a id="c29"></a>
### C29 · cell 208 [code] · code

baseline L156 → branch L3018

```diff
- babynames.loc[babynames["Sex"] == "F"].head()
+ # Randomly sample a row from the DataFrame
+ babynames.sample()
```

**Why:** Positional pairing: the baseline's `.loc[mask]` cell against the new `babynames.sample()` cell.
**Output:** differs: unrelated cells

<a id="c30"></a>
### C30 · cell 209 [markdown] · prose · **REVIEW**

baseline L159 → branch L3022

```diff
- # Boolean conditions can be combined using various bitwise operators, allowing us to filter results by multiple conditions. In the table below, p and q are boolean arrays or `Series`.
- #
- # Symbol | Usage      | Meaning
- # ------ | ---------- | -------------------------------------
- # ~    | ~p       | Returns negation of p
- # &#124; | p &#124; q | p OR q
- # &    | p & q    | p AND q
- # ^  | p ^ q | p XOR q (exclusive or)
- #
- # When combining multiple conditions with logical operators, we surround each individual condition with a set of parenthesis `()`. This imposes an order of operations on `pandas` evaluating your logic and can avoid code erroring.
- #
- # For example, if we want to return data on all names with sex `"F"` born before the year 2000, we can write:
+ # Naturally, this can be chained with the extraction tools from earlier in the chapter.
```

**Why:** The bitwise-operator table is **not** lost -- it moves up into the new "Boolean Operators" section, unchanged except that "`pandas` evaluating your logic" becomes library-neutral. The relocated paragraph also gained a new, verified claim about operator precedence (see C134). The line left here introduces `.sample()` chaining.
**Verdict:** necessary

<a id="c31"></a>
### C31 · cell 210 [code] · code

baseline L173 → branch L3025

```diff
- babynames[(babynames["Sex"] == "F") & (babynames["Year"] < 2000)].head()
+ # Sample 5 random rows, and keep all columns from position 2 onwards
+ babynames.sample(5)[:, 2:]
```

**Why:** Positional pairing. `.iloc[:, 2:]` -> `[:, 2:]` survives as its own cell in the `.sample()` section; here it happens to sit opposite the baseline's `&` filter.
**Output:** differs: unrelated cells

<a id="c32"></a>
### C32 · cell 211 [markdown] · prose · **REVIEW**

baseline L176 → branch L3029

```diff
- # Note that we're working with `Series`, so using `and` in place of `&`, or `or` in place `|` will error.
+ # Wrapping a chain of methods in parentheses lets us spread it across several lines. Here we narrow the table to the year 2000, sample four of those rows with replacement, and keep the last three columns.
```

**Why:** The "`and` in place of `&` will error" sentence is not lost -- it moves into Boolean Operators directly above the error demo (C134). This slot now introduces the parenthesised multi-line sample chain.
**Verdict:** necessary

<a id="c33"></a>
### C33 · cell 212 [code] · code

baseline L179 → branch L3032

```diff
- # This line of code will raise a ValueError
- babynames[(babynames["Sex"] == "F") and (babynames["Year"] < 2000)].head()
+ result = (
+     babynames.filter(pl.col("Year") == 2000)
+     .sample(4, with_replacement=True)[:, 2:]
+ )
+ result
```

**Why:** Positional pairing. In the branch cell, `replace=True` -> `with_replacement=True` and `.iloc[:, 2:]` -> `[:, 2:]`; the chain is bound to `result` so the parenthesised form has something to display.
**Output:** differs: unrelated cells -- the branch prints a 4x3 frame

<a id="c34"></a>
### C34 · cell 213 [markdown] · prose · **REVIEW**

baseline L183 → branch L3039

```diff
- # If we want to return data on all names with sex `"F"` *or* all born before the year 2000, we can write:
+ # ::: {tip}
+ # Rerun any of the cells above and you'll get different rows each time. Pass `seed=` to `.sample()` when you need the same rows on every run, which is most of the time once other people have to reproduce your results.
+ # :::
+ #
+ # ### `.value_counts()`
+ #
+ # The `Series.value_counts()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/series/api/polars.Series.value_counts.html) method counts the number of occurrences of each unique value in a `Series`. In other words, it *counts* the number of times each unique *value* appears. This is often useful for determining the most or least common entries in a `Series`.
```

**Why:** New `seed=` tip, plus the `.value_counts()` heading and its pola.rs doc link. The tip is an addition, prompted by three unseeded `.sample()` calls sitting above it.
**Verdict:** optional
**Minimal alternative:** Keep the heading and the doc-link swap and drop the tip. It is accurate and `polars_2` relies on the same habit, but nothing in the conversion required it.

<a id="c35"></a>
### C35 · cell 214 [code] · code

baseline L186 → branch L3048

```diff
- babynames[(babynames["Sex"] == "F") | (babynames["Year"] < 2000)].head()
+ babynames["Sex"].value_counts()
+ 
```

**Why:** Positional pairing: the baseline's `|` filter against `babynames["Sex"].value_counts()`.
**Output:** differs: unrelated cells -- a 2x2 frame, because `value_counts` returns a `DataFrame` in Polars rather than a `Series`

<a id="c36"></a>
### C36 · cell 215 [markdown] · tab-twins

baseline L189 → branch L3052 · spans code and prose

```diff
- # Boolean array selection is a useful tool, but can lead to overly verbose code for complex conditions. In the example below, our boolean condition is long enough to extend for several lines of code.
+ # The result is a two-column `DataFrame`: the distinct values, in a column that keeps the name of the original `Series`, and their counts, in a column named `count`. Those rows come back in no particular order, so pass `sort=True` when the ranking is what you are after.
+ #
+ # Below, we count the number of times each name appears in the `"Name"` column, which tells us the name recorded in the most sex-and-year combinations.
+ 
+ # %% tags=["remove-input", "remove-output"]
+ babynames["Name"].value_counts(sort=True).head()
+ 
+ 
+ # %% [markdown]
+ #
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin babynames["Name"].value_counts(sort=True).head() -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # babynames["Name"].value_counts(sort=True).head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 2)
+ # ┌───────────┬───────┐
+ # │ Name      ┆ count │
+ # │ ---       ┆ ---   │
+ # │ str       ┆ u32   │
+ # ╞═══════════╪═══════╡
+ # │ Jean      ┆ 223   │
+ # │ Francis   ┆ 221   │
+ # │ Guadalupe ┆ 218   │
+ # │ Jessie    ┆ 217   │
+ # │ Marion    ┆ 214   │
+ # └───────────┴───────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_pd["Name"].value_counts().head()
+ … 21 more lines
```

**Why:** Twin for `value_counts(sort=True).head()`. `sort=True` is required because Polars does not sort by default where pandas does; the prose above the twin says so rather than hiding the keyword.
**Output:** same values -- Jean 223, Francis 221, Guadalupe 218, Jessie 217, Marion 214 on both panes. Shapes differ: a two-column `DataFrame` against a named `Series`

<a id="c37"></a>
### C37 · cell 220 [code] · code

baseline L192 → branch L3115

```diff
- # Note: The parentheses surrounding the code make it possible to break the code on to multiple lines for readability
- (
-     babynames[(babynames["Name"] == "Bella") |
-               (babynames["Name"] == "Alex") |
-               (babynames["Name"] == "Ani") |
-               (babynames["Name"] == "Lisa")]
- ).head()
+ babynames["Name"].unique()
+ 
```

**Why:** Positional pairing: the baseline's four-way `|` filter against `babynames["Name"].unique()`.
**Output:** differs: unrelated cells -- a 20,437-value `Series`

<a id="c38"></a>
### C38 · cell 221 [markdown] · prose · **REVIEW**

baseline L201 → branch L3119

```diff
- #  Fortunately, `pandas` provides many alternative methods for constructing boolean filters.
- #
- # The `.isin` function is one such example. This method evaluates if the values in a `Series` are contained in a different sequence (list, array, or `Series`) of values. In the cell below, we achieve equivalent results to the `DataFrame` above with far more concise code.
+ # The 407,428 rows of the table hold 20,437 distinct names between them, a count that `.n_unique()` reports directly.
```

**Why:** The `.isin` introduction moves up into "More Ways to Build a Filter"; this slot carries the `n_unique` sentence instead.
**Verdict:** necessary

<a id="c39"></a>
### C39 · cell 222 [code] · code

baseline L205 → branch L3121

```diff
- # %%
- names = ["Bella", "Alex", "Narges", "Lisa"]
- babynames["Name"].isin(names).head()
+ # %% tags=["remove-input", "remove-output"]
+ babynames["Name"].n_unique()
```

**Why:** Positional pairing. `isin` -> `is_in` lives in the relocated filter section; the cell here is `n_unique()`.
**Output:** differs: unrelated cells -- `20437`

<a id="c40"></a>
### C40 · cell 25 [code] · code

baseline L209 → branch L3124

```diff
- # %%
- babynames[babynames["Name"].isin(names)].head()
```

**Why:** The baseline's `babynames[babynames["Name"].isin(names)].head()`. The demo survives as `babynames.filter(pl.col("Name").is_in(names))` (C141), unpaired at this position.
**Output:** differs: the Polars cell drops the `.head()` and shows all 317 rows, truncated by Polars' own `...` divider

<a id="c41"></a>
### C41 · cell 223 [markdown] · prose · **REVIEW**

baseline L213 → branch L3126

```diff
- # The function `str.startswith` can be used to define a filter based on string values in a `Series` object. It checks to see if string values in a `Series` start with a particular character.
+ #
```

**Why:** The `.str.startswith` paragraph survives in substance in the relocated section ("String columns carry a whole family of methods under `.str`"). What is left at this position is an empty markdown cell.
**Verdict:** necessary

<a id="c42"></a>
### C42 · cell 224 [markdown] · tab-twins

baseline L215 → branch L3128 · spans code and prose

```diff
- # %%
- # Identify whether names begin with the letter "N"
- babynames["Name"].str.startswith("N").head()
+ # %% [markdown]
+ # <!-- tab-twins:begin babynames["Name"].n_unique() -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # babynames["Name"].n_unique()
+ # ```
+ #
+ # ```text
+ # 20437
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_pd["Name"].nunique()
+ # ```
+ #
+ # ```text
+ # 20437
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
+ # %% [markdown]
+ # The unique values arrive in no particular order. When the order matters, `maintain_order=True` returns them in the order they first appear in the `Series`, which here means starting from the top of the table.
```

**Why:** Twin pairing `n_unique()` with `nunique()`, plus the new `maintain_order=True` paragraph -- Polars' `unique` does not preserve order of appearance and pandas' does, so the difference is taught rather than papered over.
**Output:** same -- `20437` on both panes

<a id="c43"></a>
### C43 · cell 226 [code] · tab-twins

baseline L219 → branch L3157 · spans code and prose

```diff
- # %%
- # Extracting names that begin with the letter "N"
- babynames[babynames["Name"].str.startswith("N")].head()
+ # %% tags=["remove-input", "remove-output"]
+ babynames["Name"].unique(maintain_order=True).head(5)
+ 
+ 
+ # %% [markdown]
+ #
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin babynames["Name"].unique(maintain_order=True).head(5) -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # babynames["Name"].unique(maintain_order=True).head(5)
+ # ```
+ #
+ # ```text
+ # shape: (5,)
+ # Series: 'Name' [str]
+ # [
+ # 	"Mary"
+ # 	"Helen"
+ # 	"Dorothy"
+ # 	"Margaret"
+ # 	"Frances"
+ # ]
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_pd["Name"].unique()[:5]
+ # ```
+ #
+ # ```text
+ # array(['Mary', 'Helen', 'Dorothy', 'Margaret', 'Frances'], dtype=object)
+ # ```
+ # ::::
+ # :::::
+ … 1 more lines
```

**Why:** `unique(maintain_order=True).head(5)` twinned with `unique()[:5]`. The explicit `5` matters: `pl.Series.head()` defaults to **10**, which would contradict the sentence teaching the default (recorded in CONVERSIONS.md).
**Output:** same values (Mary, Helen, Dorothy, Margaret, Frances); the reprs differ -- a Polars `Series` block against pandas' `array(..., dtype=object)`

<a id="c44"></a>
### C44 · cell 229: Adding, Removing, and Modifying Columns · prose · **REVIEW**

baseline L228 → branch L3204

```diff
- # To add a new column to a `DataFrame`, we use a syntax similar to that used when accessing an existing column. Specify the name of the new column by writing `df["column"]`, then assign this to a `Series` or array containing the values that will populate this column.
+ # To add a new column, hand `.with_columns()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.with_columns.html) a `Series` or an expression under the name we want it to have. Writing that name as a keyword argument, as below, is the most direct way to say it.
```

**Why:** `df["new"] = ...` has no Polars form. Assignment becomes `.with_columns()` with the column named as a keyword argument, and the doc link moves to pola.rs.
**Verdict:** necessary

<a id="c45"></a>
### C45 · cell 230 [code] · code

baseline L230 → branch L3206

```diff
- # %%
- # Create a Series of the length of each name.
- babyname_lengths = babynames["Name"].str.len()
+ # %% tags=["remove-input", "remove-output"]
+ # Create a Series of the length of each name
+ babyname_lengths = babynames["Name"].str.len_chars()
```

**Why:** `.str.len()` -> `.str.len_chars()`. Polars separates byte length from character length; `len_chars` is the one that matches pandas' `str.len`.
**Output:** same -- 4, 5, 7, 8, 7 for the first five names

<a id="c46"></a>
### C46 · cell 230 [code] · code

baseline L235 → branch L3211

```diff
- babynames["name_lengths"] = babyname_lengths
- babynames.head(5)
+ babynames = babynames.with_columns(name_lengths=babyname_lengths)
+ babynames.head()
```

**Why:** `babynames["name_lengths"] = ...` -> `babynames = babynames.with_columns(name_lengths=...)`; frames are immutable, so the result is re-assigned. `head(5)` -> `head()` because five is the `DataFrame` default the chapter teaches.
**Output:** same rows; the new column is `u32` in Polars rather than `int64`

<a id="c47"></a>
### C47 · cell 231 [markdown] · prose · **REVIEW**

baseline L239 → branch L3215

```diff
- # If we need to later modify an existing column, we can do so by referencing this column again with the syntax `df["column"]`, then re-assigning it to a new `Series` or array of the appropriate length.
+ #
```

**Why:** The sentence survives, rewritten for `with_columns` ("we pass the new values to `.with_columns()` under that column's existing name"). What is left here is an empty markdown cell.
**Verdict:** necessary

<a id="c48"></a>
### C48 · cell 232 [markdown] · tab-twins

baseline L241 → branch L3217 · spans code and prose

```diff
- # %%
- # Modify the “name_lengths” column to be one less than its original value
- babynames["name_lengths"] = babynames["name_lengths"] - 1
+ # %% [markdown]
+ # <!-- tab-twins:begin babynames = babynames.with_columns(name_lengths=babyname_lengths) babynames.head() -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Create a Series of the length of each name
+ # babyname_lengths = babynames["Name"].str.len_chars()
+ #
+ # # Add a column named "name_lengths" that includes the length of each name
+ # babynames = babynames.with_columns(name_lengths=babyname_lengths)
+ # babynames.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 6)
+ # ┌───────┬─────┬──────┬──────────┬───────┬──────────────┐
+ # │ State ┆ Sex ┆ Year ┆ Name     ┆ Count ┆ name_lengths │
+ # │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   ┆ ---          │
+ # │ str   ┆ str ┆ i64  ┆ str      ┆ i64   ┆ u32          │
+ # ╞═══════╪═════╪══════╪══════════╪═══════╪══════════════╡
+ # │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   ┆ 4            │
+ # │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   ┆ 5            │
+ # │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   ┆ 7            │
+ # │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   ┆ 8            │
+ # │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   ┆ 7            │
+ # └───────┴─────┴──────┴──────────┴───────┴──────────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # Create a Series of the length of each name
+ # babyname_lengths_pd = babynames_pd["Name"].str.len()
+ #
+ # # Add a column named "name_lengths" that includes the length of each name
+ # babynames_pd["name_lengths"] = babyname_lengths_pd
+ # babynames_pd.head()
+ # ```
+ … 22 more lines
```

**Why:** Twin for the add-a-column cell.
**Output:** same -- same five rows and lengths; the Polars pane carries a dtype row, the pandas pane an index column

<a id="c49"></a>
### C49 · cell 235 [code] · tab-twins

baseline L245 → branch L3280 · spans code and prose

```diff
+ 
+ 
+ # %% [markdown]
+ #
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin babynames = babynames.with_columns(name_lengths=pl.col("name_lengths") - 1) -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Modify the "name_lengths" column to be one less than its original value
+ # babynames = babynames.with_columns(name_lengths=pl.col("name_lengths") - 1)
+ # babynames.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 6)
+ # ┌───────┬─────┬──────┬──────────┬───────┬──────────────┐
+ # │ State ┆ Sex ┆ Year ┆ Name     ┆ Count ┆ name_lengths │
+ # │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   ┆ ---          │
+ # │ str   ┆ str ┆ i64  ┆ str      ┆ i64   ┆ u32          │
+ # ╞═══════╪═════╪══════╪══════════╪═══════╪══════════════╡
+ # │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   ┆ 3            │
+ # │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   ┆ 4            │
+ # │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   ┆ 6            │
+ # │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   ┆ 7            │
+ # │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   ┆ 6            │
+ # └───────┴─────┴──────┴──────────┴───────┴──────────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # Modify the "name_lengths" column to be one less than its original value
+ # babynames_pd["name_lengths"] = babynames_pd["name_lengths"] - 1
+ # babynames_pd.head()
+ # ```
+ #
+ … 11 more lines
```

**Why:** Twin for the modify-a-column cell: `babynames["name_lengths"] - 1` becomes `pl.col("name_lengths") - 1` inside `with_columns`.
**Output:** same -- 3, 4, 6, 7, 6

<a id="c50"></a>
### C50 · cell 239 [code] · code

baseline L249 → branch L3335

```diff
- # %%
- # Rename “name_lengths” to “Length”
- babynames = babynames.rename(columns={"name_lengths":"Length"})
+ # %% tags=["remove-input", "remove-output"]
+ # Rename "name_lengths" to "Length"
+ babynames = babynames.rename({"name_lengths": "Length"})
```

**Why:** `rename(columns={...})` -> `rename({...})`. Polars has no `columns=`/`axis` keyword, since only columns have names to rename.
**Output:** same

<a id="c51"></a>
### C51 · cell 35 [markdown] · mixed · **REVIEW**

baseline L254 → branch L3340 · spans code and prose

```diff
- # %% [markdown]
- # If we want to remove a column or row of a `DataFrame`, we can call the `.drop` [(documentation)](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html) method. Use the `axis` parameter to specify whether a column or row should be dropped. Unless otherwise specified, `pandas` will assume that we are dropping a row by default.
- 
- # %%
- # Drop our new "Length" column from the DataFrame
- babynames = babynames.drop("Length", axis="columns")
- babynames.head(5)
```

**Why:** `.drop(..., axis="columns")` has no Polars form: `drop` takes column names and nothing else, so dropping rows is explicitly re-pointed at `filter`. The pandas doc link goes with it (G13).
**Verdict:** necessary

<a id="c52"></a>
### C52 · cell 240 [markdown] · tab-twins

baseline L263 → branch L3342 · spans code and prose

```diff
- # Notice that we *re-assigned* `babynames` to the result of `babynames.drop(...)`. This is a subtle but important point: `pandas` table operations **do not occur in-place**. Calling `df.drop(...)` will output a *copy* of `df` with the row/column of interest removed without modifying the original `df` table.
+ #
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin babynames = babynames.rename({"name_lengths": "Length"}) -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Rename "name_lengths" to "Length"
+ # babynames = babynames.rename({"name_lengths": "Length"})
+ # babynames.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 6)
+ # ┌───────┬─────┬──────┬──────────┬───────┬────────┐
+ # │ State ┆ Sex ┆ Year ┆ Name     ┆ Count ┆ Length │
+ # │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   ┆ ---    │
+ # │ str   ┆ str ┆ i64  ┆ str      ┆ i64   ┆ u32    │
+ # ╞═══════╪═════╪══════╪══════════╪═══════╪════════╡
+ # │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   ┆ 3      │
+ # │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   ┆ 4      │
+ # │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   ┆ 6      │
+ # │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   ┆ 7      │
+ # │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   ┆ 6      │
+ # └───────┴─────┴──────┴──────────┴───────┴────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # Rename "name_lengths" to "Length"
+ # babynames_pd = babynames_pd.rename(columns={"name_lengths": "Length"})
+ # babynames_pd.head()
+ # ```
+ #
+ # ```text
+ #   State Sex  Year      Name  Count  Length
+ # 0    CA   F  1910      Mary    295       3
+ … 70 more lines
```

**Why:** Twin for the rename cell. The "operations do not occur in-place" paragraph is not lost -- it moves below the drop cell and now lists `with_columns`, `rename`, `drop`, `filter`, `select`, `.sort()` and `with_row_index`, tying back to `elections` being unchanged earlier in the chapter.
**Output:** same

<a id="c53"></a>
### C53 · cell 247 [code] · code

baseline L267 → branch L3455

```diff
- # %%
- # This creates a copy of `babynames` and removes the column "Name"...
- babynames.drop("Name", axis="columns")
+ # %% tags=["remove-input", "remove-output"]
+ # This produces a new table without the column "Name"...
+ babynames.drop("Name")
```

**Why:** `drop("Name", axis="columns")` -> `drop("Name")`, and the comment drops "creates a copy" -- Polars does not copy, it builds a new frame.
**Output:** same

<a id="c54"></a>
### C54 · cell 247 [code] · code

baseline L271 → branch L3459

```diff
- # ...but the original `babynames` is unchanged!
+ # ...but the original `babynames` is unchanged!
```

**Why:** Unchanged comment line, re-emitted because the cell around it moved.
**Output:** same

<a id="c55"></a>
### C55 · cell 247 [code] · code

baseline L273 → branch L3461

```diff
- babynames.head(5)
+ babynames.head()
+ 
```

**Why:** `head(5)` -> `head()`; five is the `DataFrame` default. Note that this cell holds two expressions and only the last renders, so the committed output is the `head()` frame that still contains `Name` -- see C163.
**Output:** same

<a id="c56"></a>
### C56 · cell 39: Useful Utility Functions · prose · **REVIEW**

baseline L276 → branch L3465

```diff
- # ## Useful Utility Functions
```

**Why:** Heading kept; the section behind it is re-scoped (see C57).
**Verdict:** necessary

<a id="c57"></a>
### C57 · cell 39: Useful Utility Functions · mixed · **REVIEW**

baseline L278 → branch L3466 · spans code and prose

```diff
- # `pandas` contains an extensive library of functions that can help shorten the process of setting and getting information from its data structures. In the following section, we will give overviews of each of the main utility functions that will help us in Data 100.
- #
- # Discussing all functionality offered by `pandas` could take an entire semester! We will walk you through the most commonly-used functions and encourage you to explore and experiment on your own.
- #
- # - `NumPy` and built-in function support
- # - `.shape`
- # - `.size`
- # - `.describe() `
- # - `.sample()`
- # - `.value_counts()`
- # - `.unique()`
- # - `.sort_values()`
- #
- # The `pandas` [documentation](https://pandas.pydata.org/docs/reference/index.html) will be a valuable resource in Data 100 and beyond.
- #
- # ### `NumPy`
- #
- # `pandas` is designed to work well with `NumPy`, the framework for array computations you encountered in [Data 8](https://www.data8.org/su23/reference/#array-functions-and-methods). Just about any `NumPy` function can be applied to `pandas` `DataFrame`s and `Series`.
- 
- # %%
- # Pull out the number of babies named Yash each year
- yash_count = babynames[babynames["Name"] == "Yash"]["Count"]
- yash_count.head()
- 
- # %%
- # Average number of babies named Yash each year
- np.mean(yash_count)
- 
- # %%
- # Max number of babies named Yash born in any one year
- np.max(yash_count)
```

**Why:** The utility list loses `.size` (no Polars equivalent) and `.sort_values()` (sorting is promoted to its own `##` section), gains `.shape`/`.height`/`.width`, and the whole "`NumPy` ... just about any `NumPy` function can be applied" subsection becomes "Aggregation Methods" with `yash_counts.mean()` and `.max()`. The claim could not survive: `np.mean`, `np.max`, `np.std` and kin raise `TypeError: ... unexpected keyword argument 'axis'` on a Polars `Series`. The pandas documentation link goes with it (G13). The pandas claim could not survive verbatim -- but the replacement drops the library-interop lesson rather than restating it, and the Data 8 link above it still promises "array functions and methods".
**Verdict:** questionable
**Minimal alternative:** Keep "Aggregation Methods" and add one sentence saying that these are methods on the `Series` itself, and that the NumPy reduction family (`np.mean`, `np.max`, `np.std`) raises on a Polars `Series` -- which is the fact a Data 8 reader will otherwise discover as an error.

<a id="c58"></a>
### C58 · cell 249 [markdown] · tab-twins

baseline L311 → branch L3468

```diff
- # ### `.shape` and `.size`
+ # <!-- tab-twins:begin babynames.drop("Name") -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # This produces a new table without the column "Name"...
+ # babynames.drop("Name")
```

**Why:** The `.shape` and `.size` heading is displaced by the drop twin; the material lives in `.shape`, `.height`, and `.width` further up.
**Output:** same

<a id="c59"></a>
### C59 · cell 249: ...but the original `babynames` is unchanged! · tab-twins

baseline L313 → branch L3476

```diff
- # `.shape` and `.size` are attributes of `Series` and `DataFrame`s that measure the "amount" of data stored in the structure. Calling `.shape` returns a tuple containing the number of rows and columns present in the `DataFrame` or `Series`. `.size` is used to find the total number of elements in a structure, equivalent to the number of rows times the number of columns.
+ # # ...but the original `babynames` is unchanged!
+ # # Notice that the "Name" column is still present
+ # babynames.head()
+ # ```
```

**Why:** Continuation of the same twin -- the second half of the drop cell, `babynames.head()`.
**Output:** same

<a id="c60"></a>
### C60 · cell 249: Notice that the "Name" column is still present · tab-twins

baseline L315 → branch L3481 · spans code and prose

```diff
- # Many functions strictly require the dimensions of the arguments along certain axes to match. Calling these dimension-finding functions is much faster than counting all of the items by hand.
- 
- # %%
- # Return the shape of the DataFrame, in the format (num_rows, num_columns)
- babynames.shape
- 
- # %%
- # Return the size of the DataFrame, equal to num_rows * num_columns
- babynames.size
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
+ # ```python
+ # # This produces a new table without the column "Name"...
+ # babynames_pd.drop(columns="Name")
+ #
+ # # ...but the original `babynames_pd` is unchanged!
+ # # Notice that the "Name" column is still present
+ # babynames_pd.head()
+ # ```
+ #
+ # ```text
+ #   State Sex  Year      Name  Count
+ # 0    CA   F  1910      Mary    295
+ # 1    CA   F  1910     Helen    239
+ # 2    CA   F  1910   Dorothy    220
+ # 3    CA   F  1910  Margaret    163
+ # 4    CA   F  1910   Frances    134
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** The dimension-finding paragraph and the `.shape`/`.size` cells moved into the new attributes section; this slot carries the rest of the drop twin.
**Output:** same -- and same in the unhelpful sense: both panes show the five-row table with `Name` still present, because both cells end in `head()`. Neither pane shows the dropped-column result the comment promises. Pre-existing; baseline cell `06f920ff` has the same two-expression shape and the same single output

<a id="c61"></a>
### C61 · cell 250: Sorting · prose · **REVIEW**

baseline L326 → branch L3521

```diff
- # ### `.describe()`
+ # ## Sorting
```

**Why:** Sorting is promoted from a `###` utility function to its own `##` section, so this heading changes rather than moving; `.describe()` keeps its own heading further up.
**Verdict:** necessary

<a id="c62"></a>
### C62 · cell 250: Sorting · prose · **REVIEW**

baseline L328 → branch L3523

```diff
- # If many statistics are required from a `DataFrame` (minimum value, maximum value, mean value, etc.), then `.describe()` [(documentation)](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html) can be used to compute all of them at once.
+ # Ordering a `DataFrame` can be useful for isolating extreme values. For example, the first 5 rows of a table sorted in descending order (that is, from highest to lowest) hold the 5 largest values. `.sort()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.sort.html) orders a `DataFrame` by a column we name. It sorts from lowest to highest unless we ask otherwise with `descending=True`.
```

**Why:** `sort_values(by=, ascending=)` -> `sort(by=, descending=)`. The keyword's sense is inverted, so the sentence stating the default had to be rewritten rather than renamed, and the doc link moves to pola.rs.
**Verdict:** necessary

<a id="c63"></a>
### C63 · cell 251 [code] · code

baseline L330 → branch L3525

```diff
- # %%
- babynames.describe()
+ # %% tags=["remove-input", "remove-output"]
+ # Sort the "Count" column from lowest to highest
+ babynames.sort("Count").head()
+ 
```

**Why:** Positional pairing: `babynames.describe()` against `babynames.sort("Count").head()`.
**Output:** differs: unrelated cells

<a id="c64"></a>
### C64 · cell 252 [markdown] · mixed · **REVIEW**

baseline L334 → branch L3531 · spans code and prose

```diff
- # A different set of statistics will be reported if `.describe()` is called on categorical data.
- 
- # %%
- babynames["Sex"].describe()
+ #
```

**Why:** "A different set of statistics will be reported if `.describe()` is called on categorical data" would be false here: Polars reports `count`, `null_count`, `min`, `max` for a `String` column -- no `unique`, `top` or `freq`. The branch says instead that a `Series` reports "the statistics that suit its data type". For staff: the teaching point that a categorical summary is mode-shaped is lost from this output, and `value_counts` in the previous section is now the only place a reader gets it.
**Verdict:** questionable
**Minimal alternative:** Keep the new sentence and add that a `String` column reports only `count`, `null_count`, `min` and `max`, so the most common value has to come from `value_counts` -- one clause, and it names the gap instead of leaving the reader to notice it.

<a id="c65"></a>
### C65 · cell 253 [markdown] · tab-twins

baseline L340 → branch L3534

```diff
- # ### `.sample()`
+ # <!-- tab-twins:begin babynames.sort("Count").head() -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Sort the "Count" column from lowest to highest
+ # babynames.sort("Count").head()
+ # ```
```

**Why:** The `.sample()` heading is displaced by the ascending-sort twin; the heading survives above.
**Output:** same

<a id="c66"></a>
### C66 · cell 253: Sort the "Count" column from lowest to highest · tab-twins

baseline L342 → branch L3543

```diff
- # As we will see later in the semester, random processes are at the heart of many data science techniques (for example, train-test splits, bootstrapping, and cross-validation). `.sample()` [(documentation)](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html) lets us quickly select random entries (a row if called from a `DataFrame`, or a value if called from a `Series`).
+ # ```text
+ # shape: (5, 5)
+ # ┌───────┬─────┬──────┬──────────┬───────┐
+ # │ State ┆ Sex ┆ Year ┆ Name     ┆ Count │
+ # │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   │
+ # │ str   ┆ str ┆ i64  ┆ str      ┆ i64   │
+ # ╞═══════╪═════╪══════╪══════════╪═══════╡
+ # │ CA    ┆ F   ┆ 1910 ┆ Adelaide ┆ 5     │
+ # │ CA    ┆ F   ┆ 1910 ┆ Adele    ┆ 5     │
+ # │ CA    ┆ F   ┆ 1910 ┆ Adrienne ┆ 5     │
+ # │ CA    ┆ F   ┆ 1910 ┆ Althea   ┆ 5     │
+ # │ CA    ┆ F   ┆ 1910 ┆ Antonia  ┆ 5     │
+ # └───────┴─────┴──────┴──────────┴───────┘
+ # ```
+ # ::::
```

**Why:** Polars pane of the ascending-sort twin.
**Output:** **differs: the two panes show five entirely different rows.** Thousands of rows tie at `Count == 5`. Polars' sort is stable and returns the first five in table order (1910 F: Adelaide, Adele, Adrienne, Althea, Antonia); pandas' quicksort returns Zylo and four 1981 names. Nothing in the prose points at it, so a reader flipping tabs reads an arbitrary tie order as a library semantic -- the same failure class as CONTRADICTIONS.md §B1, introduced here and not recorded there

<a id="c67"></a>
### C67 · cell 253: Sort the "Count" column from lowest to highest · tab-twins

baseline L344 → branch L3559 · spans code and prose

```diff
- # By default, `.sample()` selects entries *without* replacement. Pass in the argument `replace=True` to sample with replacement.
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_pd.sort_values("Count").head()
+ # ```
+ #
+ # ```text
+ #        State Sex  Year       Name  Count
+ # 407427    CA   M  2022       Zylo      5
+ # 300815    CA   M  1981  Broderick      5
+ # 300816    CA   M  1981     Brooke      5
+ # 300817    CA   M  1981        Bud      5
+ # 300818    CA   M  1981        Cha      5
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
+ # %% tags=["remove-input", "remove-output"]
+ # Sort the "Count" column from highest to lowest
+ babynames.sort("Count", descending=True).head()
```

**Why:** pandas pane of the same twin, plus the opening of the descending-sort cell.
**Output:** differs: see C66

<a id="c68"></a>
### C68 · cell 51 [code] · code

baseline L346 → branch L3580

```diff
- # %%
- # Sample a single row
- babynames.sample()
```

**Why:** The baseline's `babynames.sample()` cell, which survives at C151 under the `.sample()` heading; the pairing here is positional.
**Output:** differs: same call, re-executed, so a different random row

<a id="c69"></a>
### C69 · cell 255 [markdown] · mixed · **REVIEW**

baseline L351 → branch L3582 · spans code and prose

```diff
- # Naturally, this can be chained with other methods and operators (`iloc`, etc.).
- 
- # %%
- # Sample 5 random rows, and select all columns after column 2
- babynames.sample(5).iloc[:, 2:]
- 
- # %%
- # Randomly sample 4 names from the year 2000, with replacement, and select all columns after column 2
- babynames[babynames["Year"] == 2000].sample(4, replace = True).iloc[:, 2:]
+ #
```

**Why:** `.iloc[:, 2:]` -> `[:, 2:]` and `replace=True` -> `with_replacement=True`; both cells survive in the `.sample()` section above, so what is left here is an empty markdown cell.
**Verdict:** necessary

<a id="c70"></a>
### C70 · cell 256 [markdown] · tab-twins

baseline L362 → branch L3585

```diff
- # ### `.value_counts()`
+ # <!-- tab-twins:begin babynames.sort("Count", descending=True).head() -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Sort the "Count" column from highest to lowest
+ # babynames.sort("Count", descending=True).head()
+ # ```
```

**Why:** The `.value_counts()` heading is displaced by the descending-sort twin; the heading survives above.
**Output:** same

<a id="c71"></a>
### C71 · cell 256: Sort the "Count" column from highest to lowest · tab-twins

baseline L364 → branch L3594

```diff
- # The `Series.value_counts()` [(documentation)](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html) method counts the number of occurrence of each unique value in a `Series`. In other words, it *counts* the number of times each unique *value* appears. This is often useful for determining the most or least common entries in a `Series`.
+ # ```text
+ # shape: (5, 5)
+ # ┌───────┬─────┬──────┬─────────┬───────┐
+ # │ State ┆ Sex ┆ Year ┆ Name    ┆ Count │
+ # │ ---   ┆ --- ┆ ---  ┆ ---     ┆ ---   │
+ # │ str   ┆ str ┆ i64  ┆ str     ┆ i64   │
+ # ╞═══════╪═════╪══════╪═════════╪═══════╡
+ # │ CA    ┆ M   ┆ 1957 ┆ Michael ┆ 8260  │
+ # │ CA    ┆ M   ┆ 1956 ┆ Michael ┆ 8258  │
+ # │ CA    ┆ M   ┆ 1990 ┆ Michael ┆ 8246  │
+ # │ CA    ┆ M   ┆ 1969 ┆ Michael ┆ 8245  │
+ # │ CA    ┆ M   ┆ 1970 ┆ Michael ┆ 8196  │
+ # └───────┴─────┴──────┴─────────┴───────┘
+ # ```
+ # ::::
```

**Why:** Polars pane of the descending-sort twin -- the five largest counts in the dataset.
**Output:** same -- the same five Michael rows, 8260 down to 8196, on both panes

<a id="c72"></a>
### C72 · cell 256: Sort the "Count" column from highest to lowest · tab-twins

baseline L366 → branch L3610

```diff
- # In the example below, we can determine the name with the most years in which at least one person has taken that name by counting the number of times each name appears in the `"Name"` column of `babynames`. Note that the return value is also a `Series`.
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_pd.sort_values("Count", ascending=False).head()
+ # ```
+ #
+ # ```text
+ #        State Sex  Year     Name  Count
+ # 268041    CA   M  1957  Michael   8260
+ # 267017    CA   M  1956  Michael   8258
+ # 317387    CA   M  1990  Michael   8246
+ # 281850    CA   M  1969  Michael   8245
+ # 283146    CA   M  1970  Michael   8196
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
+ # %% [markdown]
+ # There are a lot of Michaels in California: all five of the largest counts in the dataset belong to that name, topping out at 8,260 babies in 1957.
+ #
+ # A `Series` sorts the same way. There is no column to name, since a `Series` is a single column, and only its values come back in their new order.
```

**Why:** pandas pane of the same twin, plus the new Michael sentence and the lead-in to sorting a `Series`.
**Output:** same

<a id="c73"></a>
### C73 · cell 258 [code] · code

baseline L368 → branch L3632

```diff
- # %%
- babynames["Name"].value_counts().head()
+ # %% tags=["remove-input", "remove-output"]
+ # Sort the "Name" Series alphabetically
+ babynames["Name"].sort().head(5)
+ 
```

**Why:** Positional pairing: `value_counts().head()` against `babynames["Name"].sort().head(5)`. The explicit `5` is load-bearing -- `pl.Series.head()` defaults to 10 and would contradict the sentence teaching the default.
**Output:** differs: unrelated cells

<a id="c74"></a>
### C74 · cell 57: `.unique()` · prose · **REVIEW**

baseline L372 → branch L3638

```diff
- # ### `.unique()`
```

**Why:** The `.unique()` heading survives above; this is the positional residue of the move.
**Verdict:** necessary

<a id="c75"></a>
### C75 · cell 57: `.unique()` · mixed · **REVIEW**

baseline L374 → branch L3639 · spans code and prose

```diff
- # If we have a `Series` with many repeated values, then `.unique()` [(documentation)](https://pandas.pydata.org/docs/reference/api/pandas.unique.html) can be used to identify only the *unique* values. Here we return an array of all the names in `babynames`.
- 
- # %%
- babynames["Name"].unique()
```

**Why:** `.unique()` returns a `Series` in Polars rather than an ndarray, and the pandas doc link goes (G13). Both the paragraph and the cell survive in the relocated section.
**Verdict:** necessary

<a id="c76"></a>
### C76 · cell 260 [markdown] · tab-twins

baseline L380 → branch L3641

```diff
- # ### `.sort_values()`
+ # <!-- tab-twins:begin babynames["Name"].sort().head(5) -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Sort the "Name" Series alphabetically
+ # babynames["Name"].sort().head(5)
+ # ```
```

**Why:** The `.sort_values()` heading is displaced -- sorting is now a `##` section of its own.
**Output:** same

<a id="c77"></a>
### C77 · cell 260: Sort the "Name" Series alphabetically · tab-twins

baseline L382 → branch L3650 · spans code and prose

```diff
- # Ordering a `DataFrame` can be useful for isolating extreme values. For example, the first 5 entries of a row sorted in descending order (that is, from highest to lowest) are the largest 5 values. `.sort_values` [(documentation)](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html) allows us to order a `DataFrame` or `Series` by a specified column. We can choose to either receive the rows in `ascending` order (default) or `descending` order.
- 
- # %%
- # Sort the "Count" column from highest to lowest
- babynames.sort_values(by="Count", ascending=False).head()
+ # ```text
+ # shape: (5,)
+ # Series: 'Name' [str]
+ # [
+ # 	"Aadan"
+ # 	"Aadan"
+ # 	"Aadan"
+ # 	"Aadarsh"
+ # 	"Aaden"
+ # ]
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # babynames_pd["Name"].sort_values().head(5)
+ # ```
+ #
+ # ```text
+ # 366001      Aadan
+ # 384005      Aadan
+ # 369120      Aadan
+ # 398211    Aadarsh
+ # 370306      Aaden
+ # Name: Name, dtype: object
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** The `sort_values` paragraph and the descending-sort cell moved into the Sorting section; this slot carries the `Series`-sort twin instead.
**Output:** same values -- Aadan x3, Aadarsh, Aaden on both panes; the reprs differ, a Polars `Series` block against a pandas `Series` with row labels and `dtype: object`

<a id="c78"></a>
### C78 · cell 261 [markdown] · prose · **REVIEW**

baseline L389 → branch L3682

```diff
- # Unlike when calling `.value_counts()` on a `DataFrame`, we do not need to explicitly specify the column used for sorting when calling `.value_counts()` on a `Series`. We can still specify the ordering paradigm – that is, whether values are sorted in ascending or descending order.
+ # ::: {warning}
+ # `.sort()` places null values **first**, ahead of every real value, in both sort directions. A `.head()` or a positional slice taken straight after a sort will therefore pick up missing values and push out the rows you were after. Nothing about that is an error, so nothing announces it. Pass `nulls_last=True` whenever a sort feeds a `.head()`, a `.tail()`, or a slice, unless you already know the column holds no nulls — as is the case for both datasets in this chapter.
+ # :::
+ #
+ # `babynames` has no missing values, so the small table below has one instead.
```

**Why:** New warning, and the chapter's single most important behaviour difference. Polars sorts nulls **first** in both directions where pandas puts `NaN` last (AGENTS.md hard rule 8), so a `.head()` after a sort on a nullable column silently gains a missing row and drops a real one. The hedging clause ("unless you already know the column holds no nulls -- as is the case for both datasets in this chapter") is there because six of the chapter's own sort-then-head cells omit `nulls_last=True`; verified live that `elections` has no nulls in `%`. This is the claim behind CONTRADICTIONS.md §B1's `polars_1 - 9ed57619 / 82a35df6` row -- **introduced by the conversion**, since the whole warning is new -- where the sentence below it read "Sorting from highest to lowest put the missing count at the top" while the pandas pane showed the opposite. The fixed sentence, which names the library, is in the branch.
**Verdict:** necessary

<a id="c79"></a>
### C79 · cell 262 [code] · tab-twins

baseline L391 → branch L3688 · spans code and prose

```diff
- # %%
- # Sort the "Name" Series alphabetically
- babynames["Name"].sort_values(ascending=True).head()
+ # %% tags=["remove-input", "remove-output"]
+ demo = pl.DataFrame({"Name": ["Aaliyah", "Bao", "Cyrus"], "Count": [3, None, 1]})
+ demo.sort("Count", descending=True)
+ 
+ 
+ # %% [markdown]
+ #
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin demo = pl.DataFrame( -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # demo = pl.DataFrame({"Name": ["Aaliyah", "Bao", "Cyrus"], "Count": [3, None, 1]})
+ # demo.sort("Count", descending=True)
+ # ```
+ #
+ # ```text
+ # shape: (3, 2)
+ # ┌─────────┬───────┐
+ # │ Name    ┆ Count │
+ # │ ---     ┆ ---   │
+ # │ str     ┆ i64   │
+ # ╞═════════╪═══════╡
+ # │ Bao     ┆ null  │
+ # │ Aaliyah ┆ 3     │
+ # │ Cyrus   ┆ 1     │
+ # └─────────┴───────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # demo_pd = pd.DataFrame({"Name": ["Aaliyah", "Bao", "Cyrus"],
+ #                         "Count": [3, None, 1]})
+ # demo_pd.sort_values("Count", ascending=False)
+ # ```
+ #
+ … 62 more lines
```

**Why:** The `Series`-sort cell moves up; this slot is the three-row `demo` frame, built specifically to contain a null because `babynames` and `elections` are both null-free, plus its twin.
**Output:** differs by design: Polars puts `Bao`'s null first, pandas puts it last. That contrast is the lesson, and the prose now names the library so the pandas reader is not told they are watching something they are not

<a id="c80"></a>
### C80 · cell 63: Custom Sorts · dropdown

baseline L400 → branch L3796 · spans code and prose; mirror of the next code cell (hard rule 3)

```diff
- # We'll start by loading the `babynames` dataset. Note that this dataset is filtered to only contain data from California.
- #
- # ````{dropdown} Click to see the code
- # :open: false
- # ```python
- # # This code pulls census data and loads it into a DataFrame
- # # We won't cover it explicitly in this class, but you are welcome to explore it on your own
- # import warnings
- # warnings.simplefilter(action='ignore', category=FutureWarning)
- #
- # import pandas as pd
- # import numpy as np
- # import urllib.request
- # import os.path
- # import zipfile
- #
- # data_url = "https://www.ssa.gov/oact/babynames/state/namesbystate.zip"
- # local_filename = "data/babynamesbystate.zip"
- # if not os.path.exists(local_filename): # If the data exists don't download again
- #     with urllib.request.urlopen(data_url) as resp, open(local_filename, 'wb') as f:
- #         f.write(resp.read())
- #
- # zf = zipfile.ZipFile(local_filename, 'r')
- #
- # ca_name = 'STATE.CA.TXT'
- # field_names = ['State', 'Sex', 'Year', 'Name', 'Count']
- # with zf.open(ca_name) as fh:
- #     babynames = pd.read_csv(fh, header=None, names=field_names)
- #
- # babynames.tail(10)
- # ```
- # ````
- 
- # %% tags=["remove-input"]
- # This code pulls census data and loads it into a DataFrame
- # We won't cover it explicitly in this class, but you are welcome to explore it on your own
- import warnings
- warnings.simplefilter(action='ignore', category=FutureWarning)
- 
- import pandas as pd
- … 21 more lines
```

**Why:** Dropdown mirror of the babynames download cell: the `warnings` filter and the `pandas`/`numpy` imports go, and `pd.read_csv(fh, header=None, names=)` becomes `pl.read_csv(fh, has_header=False, new_columns=)`. **Mirror checked line by line against code cell `c8bfdae2`: they are identical in the branch**, so hard rule 3 holds.
**Output:** same -- `babynames.head()`, five rows

<a id="c81"></a>
### C81 · cell 270 [code] · metadata

baseline L465 → branch L3800

```diff
- # %%
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c82"></a>
### C82 · cell 270 [code] · code

baseline L467 → branch L3802

```diff
- babyname_lengths = babynames["Name"].str.len()
+ babyname_lengths = babynames["Name"].str.len_chars()
```

**Why:** `.str.len()` -> `.str.len_chars()`, the same edit as C45; this is the Custom Sorts copy of the cell.
**Output:** same

<a id="c83"></a>
### C83 · cell 270 [code] · code

baseline L470 → branch L3805

```diff
- babynames["name_lengths"] = babyname_lengths
+ babynames = babynames.with_columns(name_lengths=babyname_lengths)
```

**Why:** Assignment -> `with_columns`, the same edit as C46.
**Output:** same

<a id="c84"></a>
### C84 · cell 66 [code] · mixed · **REVIEW**

baseline L472 → branch L3807 · spans code and prose

```diff
- 
- # %% [markdown]
- # We can then sort the `DataFrame` by that column using `.sort_values()`:
- 
- # %%
- # Sort by the temporary column
- babynames = babynames.sort_values(by="name_lengths", ascending=False)
- babynames.head(5)
- 
- # %% [markdown]
- # Finally, we can drop the `name_length` column from `babynames` to prevent our table from getting cluttered.
- 
- # %%
- # Drop the 'name_length' column
- babynames = babynames.drop("name_lengths", axis='columns')
- babynames.head(5)
- 
- # %% [markdown]
- # ### Approach 2: Sorting using the `key` Argument
- #
- # Another way to approach this is to use the `key` argument of `.sort_values()`. Here we can specify that we want to sort `"Name"` values by their length.
- 
- # %%
- babynames.sort_values("Name", key=lambda x: x.str.len(), ascending=False).head()
```

**Why:** Approach 2 was `sort_values("Name", key=lambda x: x.str.len())`. Polars' `.sort()` has no `key` argument, so the approach is re-aimed at passing an **expression** as the sort key -- `babynames.sort(pl.col("Name").str.len_chars(), descending=True)` -- and renamed "Sorting on an Expression". Same kind of thing demonstrated: compute the key on the way in, no temporary column to create or drop. Verified that the expression sort and the temporary-column sort return the same first five rows.
**Verdict:** necessary

<a id="c85"></a>
### C85 · cell 73: Approach 3: Sorting using the `map` Function · prose · **REVIEW**

baseline L499 → branch L3810

```diff
- # ### Approach 3: Sorting using the `map` Function
```

**Why:** Heading kept, `map` -> `map_elements`, which is the Polars name for the per-value escape hatch.
**Verdict:** necessary

<a id="c86"></a>
### C86 · cell 73: Approach 3: Sorting using the `map` Function · prose · **REVIEW**

baseline L501 → branch L3811

```diff
- # We can also use the `map` function on a `Series` to solve this. Say we want to sort the `babynames` table by the number of `"dr"`'s and `"ea"`'s in each `"Name"`. We'll define the function `dr_ea_count` to help us out.
```

**Why:** `Series.map(f)` has no Polars equivalent; `map_elements` is the nearest thing and needs `return_dtype`. A new paragraph below the cell adds what the pandas original did not say -- that it runs Python once per row and is much slower than the expression in Approach 2.
**Verdict:** necessary

<a id="c87"></a>
### C87 · cell 272 [markdown] · tab-twins

baseline L503 → branch L3812 · spans code and prose

```diff
- # %%
- # First, define a function to count the number of times "dr" or "ea" appear in each name
+ # %% [markdown]
+ # <!-- tab-twins:begin babynames = babynames.with_columns(name_lengths=babyname_lengths) babynames.head(5) -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Create a Series of the length of each name
+ # babyname_lengths = babynames["Name"].str.len_chars()
+ #
+ # # Add a column named "name_lengths" that includes the length of each name
+ # babynames = babynames.with_columns(name_lengths=babyname_lengths)
+ # babynames.head(5)
+ # ```
+ #
+ # ```text
+ # shape: (5, 6)
+ # ┌───────┬─────┬──────┬──────────┬───────┬──────────────┐
+ # │ State ┆ Sex ┆ Year ┆ Name     ┆ Count ┆ name_lengths │
+ # │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   ┆ ---          │
+ # │ str   ┆ str ┆ i64  ┆ str      ┆ i64   ┆ u32          │
+ # ╞═══════╪═════╪══════╪══════════╪═══════╪══════════════╡
+ # │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   ┆ 4            │
+ # │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   ┆ 5            │
+ # │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   ┆ 7            │
+ # │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   ┆ 8            │
+ # │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   ┆ 7            │
+ # └───────┴─────┴──────┴──────────┴───────┴──────────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # Create a Series of the length of each name
+ # babyname_lengths_pd = babynames_pd["Name"].str.len()
+ #
+ # # Add a column named "name_lengths" that includes the length of each name
+ # babynames_pd["name_lengths"] = babyname_lengths_pd
+ # babynames_pd.head(5)
+ # ```
+ … 198 more lines
```

**Why:** Twin for the Approach 1 temporary-column cells.
**Output:** same

<a id="c88"></a>
### C88 · cell 286 [code] · code

baseline L508 → branch L4053

```diff
- # Then, use `map` to apply `dr_ea_count` to each name in the "Name" column
- babynames["dr_ea_count"] = babynames["Name"].map(dr_ea_count)
+ # Then, use map_elements to apply dr_ea_count to each name in the "Name" column
+ babynames = babynames.with_columns(
+     dr_ea_count=pl.col("Name").map_elements(dr_ea_count, return_dtype=pl.Int64)
+ )
```

**Why:** `babynames["Name"].map(dr_ea_count)` -> `pl.col("Name").map_elements(dr_ea_count, return_dtype=pl.Int64)` inside `with_columns`. `return_dtype` is not optional decoration: without it Polars emits a dtype warning that would be baked into the committed output.
**Output:** same -- the same `dr_ea_count` values

<a id="c89"></a>
### C89 · cell 286 [code] · code

baseline L512 → branch L4059

```diff
- babynames = babynames.sort_values(by="dr_ea_count", ascending=False)
+ babynames = babynames.sort(by="dr_ea_count", descending=True)
```

**Why:** `sort_values(by=, ascending=False)` -> `sort(by=, descending=True)`.
**Output:** same -- the five Deandrea/Leandrea rows at 3

<a id="c90"></a>
### C90 · cell 286 [code] · whitespace

baseline L515 → branch L4062

```diff
+ 
```

**Why:** Blank-line change only.

<a id="c91"></a>
### C91 · cell 287 [markdown] · prose · **REVIEW**

baseline L516 → branch L4064

```diff
- # We can drop the `dr_ea_count` once we're done using it to maintain a neat table.
+ #
```

**Why:** The sentence survives verbatim below the twin ("We can drop `dr_ea_count` once we're done using it to maintain a neat table"); what is left at this position is an empty markdown cell.
**Verdict:** necessary

<a id="c92"></a>
### C92 · cell 288 [markdown] · tab-twins

baseline L518 → branch L4066 · spans code and prose

```diff
- # %%
- # Drop the `dr_ea_count` column
- babynames = babynames.drop("dr_ea_count", axis = 'columns')
+ # %% [markdown]
+ # <!-- tab-twins:begin def dr_ea_count(string): -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # First, define a function to count the number of times
+ # # "dr" or "ea" appear in each name
+ # def dr_ea_count(string):
+ #     return string.count('dr') + string.count('ea')
+ #
+ # # Then, use map_elements to apply dr_ea_count to each name in the "Name" column
+ # babynames = babynames.with_columns(
+ #     dr_ea_count=pl.col("Name").map_elements(dr_ea_count, return_dtype=pl.Int64)
+ # )
+ #
+ # # Sort the DataFrame by the new "dr_ea_count" column so we can see our handiwork
+ # babynames = babynames.sort(by="dr_ea_count", descending=True)
+ # babynames.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 6)
+ # ┌───────┬─────┬──────┬──────────┬───────┬─────────────┐
+ # │ State ┆ Sex ┆ Year ┆ Name     ┆ Count ┆ dr_ea_count │
+ # │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   ┆ ---         │
+ # │ str   ┆ str ┆ i64  ┆ str      ┆ i64   ┆ i64         │
+ # ╞═══════╪═════╪══════╪══════════╪═══════╪═════════════╡
+ # │ CA    ┆ F   ┆ 1986 ┆ Deandrea ┆ 6     ┆ 3           │
+ # │ CA    ┆ F   ┆ 1988 ┆ Deandrea ┆ 5     ┆ 3           │
+ # │ CA    ┆ F   ┆ 1990 ┆ Deandrea ┆ 5     ┆ 3           │
+ # │ CA    ┆ F   ┆ 1994 ┆ Leandrea ┆ 5     ┆ 3           │
+ # │ CA    ┆ M   ┆ 1985 ┆ Deandrea ┆ 6     ┆ 3           │
+ # └───────┴─────┴──────┴──────────┴───────┴─────────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ … 33 more lines
```

**Why:** Twin for the `map_elements` cell.
**Output:** same

<a id="c93"></a>
### C93 · cell 290 [code] · tab-twins

baseline L522 → branch L4140 · spans code and prose

```diff
+ 
+ 
+ # %% [markdown]
+ #
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin babynames = babynames.drop("dr_ea_count") -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Drop the "dr_ea_count" column
+ # babynames = babynames.drop("dr_ea_count")
+ # babynames.head(5)
+ # ```
+ #
+ # ```text
+ # shape: (5, 5)
+ # ┌───────┬─────┬──────┬──────────┬───────┐
+ # │ State ┆ Sex ┆ Year ┆ Name     ┆ Count │
+ # │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   │
+ # │ str   ┆ str ┆ i64  ┆ str      ┆ i64   │
+ # ╞═══════╪═════╪══════╪══════════╪═══════╡
+ # │ CA    ┆ F   ┆ 1986 ┆ Deandrea ┆ 6     │
+ # │ CA    ┆ F   ┆ 1988 ┆ Deandrea ┆ 5     │
+ # │ CA    ┆ F   ┆ 1990 ┆ Deandrea ┆ 5     │
+ # │ CA    ┆ F   ┆ 1994 ┆ Leandrea ┆ 5     │
+ # │ CA    ┆ M   ┆ 1985 ┆ Deandrea ┆ 6     │
+ # └───────┴─────┴──────┴──────────┴───────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # Drop the "dr_ea_count" column
+ # babynames_pd = babynames_pd.drop(columns="dr_ea_count")
+ # babynames_pd.head(5)
+ # ```
+ #
+ … 11 more lines
```

**Why:** Twin for the final drop cell.
**Output:** same

<a id="c94"></a>
### C94 · cell 293: Parting Note · prose · **REVIEW**

baseline L526 → branch L4195

```diff
- # Manipulating `DataFrames` is not a skill that is mastered in just one day. Due to the flexibility of `pandas`, there are many different ways to get from point A to point B. We recommend trying multiple different ways to solve the same problem to gain even more practice and reach that point of mastery sooner.
+ # The Polars library is enormous and contains many useful functions. Here is a link to its [documentation](https://docs.pola.rs/api/python/stable/reference/index.html). We certainly don't expect you to memorize each and every method of the library, and we will give you a reference sheet for exams.
+ #
+ # Manipulating `DataFrame`s is not a skill that is mastered in just one day. The three custom sorts above all answer the same question, and none of them is the "real" one; trying several routes from point A to point B is how the syntax stops feeling arbitrary.
+ #
+ # A goal of this course is to help you build your familiarity with the real-world programming practice of ... Googling! Answers to your questions can be found in documentation, Stack Overflow, and elsewhere. Being able to search for, read, and implement documentation is an important life skill for any data scientist.
```

**Why:** Two-parent merge rather than new writing: the pola.rs documentation link and the exam reference sheet come from `pandas_1`'s Parting Note (verified in the baseline at `887a578b0a4b:content/pandas_1/pandas_1.ipynb`), and "Manipulating `DataFrame`s is not a skill mastered in just one day" from `pandas_2`'s. The Googling paragraph is `pandas_1`'s, minus its sentence about the introductory `pandas` lectures. Genuinely new: the sentence tying the three custom sorts together.
**Verdict:** necessary

<a id="c95"></a>
### C95 · `elections = pl.read_csv("data/elections.csv")` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (182, 6)
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
+ [text] │ …    ┆ …                 ┆ …                     ┆ …            ┆ …      ┆ …         │
+ [text] │ 2016 ┆ Jill Stein        ┆ Green                 ┆ 1457226      ┆ loss   ┆ 1.073699  │
+ [text] │ 2020 ┆ Joseph Biden      ┆ Democratic            ┆ 81268924     ┆ win    ┆ 51.311515 │
+ [text] │ 2020 ┆ Donald Trump      ┆ Republican            ┆ 74216154     ┆ loss   ┆ 46.858542 │
+ [text] │ 2020 ┆ Jo Jorgensen      ┆ Libertarian           ┆ 1865724      ┆ loss   ┆ 1.1779795 │
+ [text] │ 2020 ┆ Howard Hawkins    ┆ Green                 ┆ 405035       ┆ loss   ┆ 0.255731  │
+ [text] └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────────┘
```

**Why:** Re-executed under Polars: the repr leads with `shape: (182, 6)`, carries a dtype row (`i64`/`str`/`f64`) under the column names, abbreviates the middle with `…`, and has no row-index column. It reads `content/polars_1/data/elections.csv`, the 182-row copy that arrived with the `pandas_2` directory.
**Reader sees:** changed: the old `pandas_1` cell printed 187 rows running through the 2024 election; this one stops at 2020. CONVERSIONS.md records the two-copy `elections.csv` split as open for staff.

<a id="c96"></a>
### C96 · `pl.read_csv("data/elections.csv", columns=["Candidate", "Year", "%"])` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (182, 3)
+ [text] ┌──────┬───────────────────┬───────────┐
+ [text] │ Year ┆ Candidate         ┆ %         │
+ [text] │ ---  ┆ ---               ┆ ---       │
+ [text] │ i64  ┆ str               ┆ f64       │
+ [text] ╞══════╪═══════════════════╪═══════════╡
+ [text] │ 1824 ┆ Andrew Jackson    ┆ 57.210122 │
+ [text] │ 1824 ┆ John Quincy Adams ┆ 42.789878 │
+ [text] │ 1828 ┆ Andrew Jackson    ┆ 56.203927 │
+ [text] │ 1828 ┆ John Quincy Adams ┆ 43.796073 │
+ [text] │ 1832 ┆ Andrew Jackson    ┆ 54.574789 │
+ [text] │ …    ┆ …                 ┆ …         │
+ [text] │ 2016 ┆ Jill Stein        ┆ 1.073699  │
+ [text] │ 2020 ┆ Joseph Biden      ┆ 51.311515 │
+ [text] │ 2020 ┆ Donald Trump      ┆ 46.858542 │
+ [text] │ 2020 ┆ Jo Jorgensen      ┆ 1.1779795 │
+ [text] │ 2020 ┆ Howard Hawkins    ┆ 0.255731  │
+ [text] └──────┴───────────────────┴───────────┘
```

**Why:** New cell. `columns=` prunes at read time, and the committed header shows the three columns in **file** order (`Year, Candidate, %`), not the order named in the call — the comment says so.
**Reader sees:** new: the old chapter's `read_csv` option was `index_col=`, which has no Polars form; column pruning replaces it.

<a id="c97"></a>
### C97 · `pl.read_csv("data/elections.csv", n_rows=5)` · output

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

**Why:** New cell. `n_rows=5` stops the read early, so the header reports `shape: (5, 6)` rather than a `.head()` of a full table.
**Reader sees:** new: an option the old chapter never showed.

<a id="c98"></a>
### C98 · `df_list_1 = pl.DataFrame(` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (2, 2)
+ [text] ┌────────┬───────┐
+ [text] │ Fruit  ┆ Price │
+ [text] │ ---    ┆ ---   │
+ [text] │ str    ┆ f64   │
+ [text] ╞════════╪═══════╡
+ [text] │ Kiwi   ┆ 5.49  │
+ [text] │ Orange ┆ 3.99  │
+ [text] └────────┴───────┘
```

**Why:** Re-executed. Two-row fruit table with a `str`/`f64` dtype row and no index column; `orient="row"` is what makes the inner lists rows rather than columns.
**Reader sees:** equivalent: `pandas_1` built the same shape from a 2-D list (`[[1, "one"], [2, "two"]]`). The sample data moved to the fruit prices so that all four construction routes now build one table.

<a id="c99"></a>
### C99 · `df_list_2 = pl.DataFrame(` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (2, 2)
+ [text] ┌────────┬───────┐
+ [text] │ Fruit  ┆ Price │
+ [text] │ ---    ┆ ---   │
+ [text] │ str    ┆ f64   │
+ [text] ╞════════╪═══════╡
+ [text] │ Kiwi   ┆ 5.49  │
+ [text] │ Orange ┆ 3.99  │
+ [text] └────────┴───────┘
```

**Why:** Re-executed. A list of dictionaries carries its own column names, so the printed table is identical to C98's.
**Reader sees:** equivalent: the baseline built the same table the same way; `Strawberry` became `Kiwi`.

<a id="c100"></a>
### C100 · `df_dict = pl.DataFrame(` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (2, 2)
+ [text] ┌────────┬───────┐
+ [text] │ Fruit  ┆ Price │
+ [text] │ ---    ┆ ---   │
+ [text] │ str    ┆ f64   │
+ [text] ╞════════╪═══════╡
+ [text] │ Kiwi   ┆ 5.49  │
+ [text] │ Orange ┆ 3.99  │
+ [text] └────────┴───────┘
```

**Why:** Re-executed. Dictionary-of-columns construction; same two rows, same dtypes.
**Reader sees:** equivalent: the baseline's dictionary example, minus the row index.

<a id="c101"></a>
### C101 · `ser_a = pl.Series("ser_a", ["a1", "a2", "a3"])` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3,)
+ [text] Series: 'ser_a' [str]
+ [text] [
+ [text] 	"a1"
+ [text] 	"a2"
+ [text] 	"a3"
+ [text] ]
```

**Why:** The Polars `Series` repr prints `shape: (3,)` and a header naming the series and its dtype, then the values.
**Reader sees:** changed: the baseline's `s_a`/`s_b` cell committed no output at all, and gave the pair an explicit `r1`/`r2`/`r3` index. The `Series` now prints, and the row labels are gone with the Index.

<a id="c102"></a>
### C102 · `pl.DataFrame(` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3, 2)
+ [text] ┌─────────┬─────────┐
+ [text] │ ColumnA ┆ ColumnB │
+ [text] │ ---     ┆ ---     │
+ [text] │ str     ┆ str     │
+ [text] ╞═════════╪═════════╡
+ [text] │ a1      ┆ b1      │
+ [text] │ a2      ┆ b2      │
+ [text] │ a3      ┆ b3      │
+ [text] └─────────┴─────────┘
```

**Why:** Two equal-length `Series` in a dictionary become two columns under the names given as keys.
**Reader sees:** equivalent: the baseline's `A-column`/`B-column` table, without the `r1`–`r3` labels.

<a id="c103"></a>
### C103 · `pl.DataFrame(ser_a)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3, 1)
+ [text] ┌───────┐
+ [text] │ ser_a │
+ [text] │ ---   │
+ [text] │ str   │
+ [text] ╞═══════╡
+ [text] │ a1    │
+ [text] │ a2    │
+ [text] │ a3    │
+ [text] └───────┘
```

**Why:** A single `Series` handed to the constructor makes a one-column frame, and the column takes the `Series`' own name.
**Reader sees:** changed: pandas named the column `0`, because `s_a` was built without a name. The sentence above now promises that the name carries over, and the output shows it.

<a id="c104"></a>
### C104 · `ser_a.to_frame()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3, 1)
+ [text] ┌───────┐
+ [text] │ ser_a │
+ [text] │ ---   │
+ [text] │ str   │
+ [text] ╞═══════╡
+ [text] │ a1    │
+ [text] │ a2    │
+ [text] │ a3    │
+ [text] └───────┘
```

**Why:** `.to_frame()` on the same `Series` prints the same one-column table as C103.
**Reader sees:** changed: the baseline called `.to_frame()` on `s_b` and got a column named `0`; the two cells now show the same table under the name `ser_a`.

<a id="c105"></a>
### C105 · `elections.columns` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] ['Year', 'Candidate', 'Party', 'Popular vote', 'Result', '%']
```

**Why:** `DataFrame.columns` is a plain Python `list[str]`, so it prints as a list.
**Reader sees:** changed: pandas printed `Index([...], dtype='object')`, and the baseline cell ran after a `set_index`, so it listed `index, Candidate, Year, …`. Same six names here, no Index wrapper.

<a id="c106"></a>
### C106 · `elections.dtypes` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] [Int64, String, String, Int64, String, Float64]
```

**Why:** `dtypes` returns a list of Polars dtype objects in column order.
**Reader sees:** new: the old chapters never printed `.dtypes`; it pairs with the dtype row the tables now carry.

<a id="c107"></a>
### C107 · `elections.schema` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] Schema([('Year', Int64),
+ [text]         ('Candidate', String),
+ [text]         ('Party', String),
+ [text]         ('Popular vote', Int64),
+ [text]         ('Result', String),
+ [text]         ('%', Float64)])
```

**Why:** `schema` prints name/dtype pairs together, wrapped in a `Schema` repr.
**Reader sees:** new: no baseline counterpart. It is the check that a file was read as expected (`Year` as `Int64`, not `String`).

<a id="c108"></a>
### C108 · `elections.shape` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] (182, 6)
```

**Why:** `shape` returns the `(rows, columns)` tuple for the 182-row file.
**Reader sees:** changed: the baseline printed `(187, 6)`. Same attribute, same lesson, different file — see C95.

<a id="c109"></a>
### C109 · `elections.head()` · output

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

**Why:** `.head()` with no argument gives five rows; the header restates the shape.
**Reader sees:** equivalent: identical five rows to the baseline's `elections.head(5)`.

<a id="c110"></a>
### C110 · `elections.tail(5)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 6)
+ [text] ┌──────┬────────────────┬─────────────┬──────────────┬────────┬───────────┐
+ [text] │ Year ┆ Candidate      ┆ Party       ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---  ┆ ---            ┆ ---         ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ i64  ┆ str            ┆ str         ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞══════╪════════════════╪═════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 2016 ┆ Jill Stein     ┆ Green       ┆ 1457226      ┆ loss   ┆ 1.073699  │
+ [text] │ 2020 ┆ Joseph Biden   ┆ Democratic  ┆ 81268924     ┆ win    ┆ 51.311515 │
+ [text] │ 2020 ┆ Donald Trump   ┆ Republican  ┆ 74216154     ┆ loss   ┆ 46.858542 │
+ [text] │ 2020 ┆ Jo Jorgensen   ┆ Libertarian ┆ 1865724      ┆ loss   ┆ 1.1779795 │
+ [text] │ 2020 ┆ Howard Hawkins ┆ Green       ┆ 405035       ┆ loss   ┆ 0.255731  │
+ [text] └──────┴────────────────┴─────────────┴──────────────┴────────┴───────────┘
```

**Why:** `.tail(5)` on the 182-row file ends at the 2020 candidates.
**Reader sees:** changed: the baseline's tail was the 2024 field (Harris, Stein, Kennedy, Oliver). The lesson is unchanged; the data stops four years earlier.

<a id="c111"></a>
### C111 · `elections[0, "Candidate"]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] 'Andrew Jackson'
```

**Why:** Two single arguments to `[]` address one cell, and the value in it comes back as a bare Python string.
**Reader sees:** equivalent: `.loc[0, 'Candidate']` returned the same string.

<a id="c112"></a>
### C112 · `elections[[87, 25, 179], ["Year", "Party", "%"]]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3, 3)
+ [text] ┌──────┬─────────────────────┬───────────┐
+ [text] │ Year ┆ Party               ┆ %         │
+ [text] │ ---  ┆ ---                 ┆ ---       │
+ [text] │ i64  ┆ str                 ┆ f64       │
+ [text] ╞══════╪═════════════════════╪═══════════╡
+ [text] │ 1932 ┆ Republican          ┆ 39.830594 │
+ [text] │ 1860 ┆ Southern Democratic ┆ 18.138998 │
+ [text] │ 2020 ┆ Republican          ┆ 46.858542 │
+ [text] └──────┴─────────────────────┴───────────┘
```

**Why:** Two lists give a 3x3 frame, with the rows in the order they were asked for. Nothing labels them, since positions are not stored.
**Reader sees:** equivalent: `.loc[[87, 25, 179], [...]]` selected the same cells. The row labels 87/25/179 no longer appear beside the rows, which is why the prose now says they arrive in the order requested.

<a id="c113"></a>
### C113 · `elections[[87, 25, 179], "Popular vote":"%"]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3, 3)
+ [text] ┌──────────────┬────────┬───────────┐
+ [text] │ Popular vote ┆ Result ┆ %         │
+ [text] │ ---          ┆ ---    ┆ ---       │
+ [text] │ i64          ┆ str    ┆ f64       │
+ [text] ╞══════════════╪════════╪═══════════╡
+ [text] │ 15761254     ┆ loss   ┆ 39.830594 │
+ [text] │ 848019       ┆ loss   ┆ 18.138998 │
+ [text] │ 74216154     ┆ loss   ┆ 46.858542 │
+ [text] └──────────────┴────────┴───────────┘
```

**Why:** A slice of **column labels** is inclusive of both ends, so `%` is in the result; the rows are given as a list because row labels no longer exist.
**Reader sees:** changed: the baseline made the inclusive point on both axes at once (`.loc[0:3, 'Year':'Popular vote']`). Only the column half survives; the row half is re-taught as an exclusive position slice at C123/C124.

<a id="c114"></a>
### C114 · `elections[:, ["Year", "Candidate", "Result"]]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (182, 3)
+ [text] ┌──────┬───────────────────┬────────┐
+ [text] │ Year ┆ Candidate         ┆ Result │
+ [text] │ ---  ┆ ---               ┆ ---    │
+ [text] │ i64  ┆ str               ┆ str    │
+ [text] ╞══════╪═══════════════════╪════════╡
+ [text] │ 1824 ┆ Andrew Jackson    ┆ loss   │
+ [text] │ 1824 ┆ John Quincy Adams ┆ win    │
+ [text] │ 1828 ┆ Andrew Jackson    ┆ win    │
+ [text] │ 1828 ┆ John Quincy Adams ┆ loss   │
+ [text] │ 1832 ┆ Andrew Jackson    ┆ win    │
+ [text] │ …    ┆ …                 ┆ …      │
+ [text] │ 2016 ┆ Jill Stein        ┆ loss   │
+ [text] │ 2020 ┆ Joseph Biden      ┆ win    │
+ [text] │ 2020 ┆ Donald Trump      ┆ loss   │
+ [text] │ 2020 ┆ Jo Jorgensen      ┆ loss   │
+ [text] │ 2020 ┆ Howard Hawkins    ┆ loss   │
+ [text] └──────┴───────────────────┴────────┘
```

**Why:** `:` in the row argument keeps all 182 rows and narrows to three columns.
**Reader sees:** equivalent: the baseline's `.loc[:, ["Year", "Candidate", "Result"]]`, with 182 rows rather than 187.

<a id="c115"></a>
### C115 · `elections[[87, 25, 179], :]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3, 6)
+ [text] ┌──────┬──────────────────────┬─────────────────────┬──────────────┬────────┬───────────┐
+ [text] │ Year ┆ Candidate            ┆ Party               ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---  ┆ ---                  ┆ ---                 ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ i64  ┆ str                  ┆ str                 ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞══════╪══════════════════════╪═════════════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 1932 ┆ Herbert Hoover       ┆ Republican          ┆ 15761254     ┆ loss   ┆ 39.830594 │
+ [text] │ 1860 ┆ John C. Breckinridge ┆ Southern Democratic ┆ 848019       ┆ loss   ┆ 18.138998 │
+ [text] │ 2020 ┆ Donald Trump         ┆ Republican          ┆ 74216154     ┆ loss   ┆ 46.858542 │
+ [text] └──────┴──────────────────────┴─────────────────────┴──────────────┴────────┴───────────┘
```

**Why:** `:` in the column argument keeps all six columns for the three rows named.
**Reader sees:** equivalent: the baseline's `.loc[[0, 1, 2, 3], :]` taught the same shorthand.

<a id="c116"></a>
### C116 · `elections[[87, 25, 179], "Popular vote"]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3,)
+ [text] Series: 'Popular vote' [i64]
+ [text] [
+ [text] 	15761254
+ [text] 	848019
+ [text] 	74216154
+ [text] ]
```

**Why:** A single column label in the second argument returns a `Series`, printed with its name and dtype in the header.
**Reader sees:** equivalent: identical three values to the baseline's `.loc[[87, 25, 179], "Popular vote"]`.

<a id="c117"></a>
### C117 · `elections[[87, 25, 179], ["Popular vote"]]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3, 1)
+ [text] ┌──────────────┐
+ [text] │ Popular vote │
+ [text] │ ---          │
+ [text] │ i64          │
+ [text] ╞══════════════╡
+ [text] │ 15761254     │
+ [text] │ 848019       │
+ [text] │ 74216154     │
+ [text] └──────────────┘
```

**Why:** Wrapping the same label in a list returns a one-column `DataFrame` instead.
**Reader sees:** equivalent: the baseline drew the same `Series`-vs-frame contrast with `.loc`.

<a id="c118"></a>
### C118 · `elections[[180, 181]]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (2, 6)
+ [text] ┌──────┬────────────────┬─────────────┬──────────────┬────────┬───────────┐
+ [text] │ Year ┆ Candidate      ┆ Party       ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---  ┆ ---            ┆ ---         ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ i64  ┆ str            ┆ str         ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞══════╪════════════════╪═════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 2020 ┆ Jo Jorgensen   ┆ Libertarian ┆ 1865724      ┆ loss   ┆ 1.1779795 │
+ [text] │ 2020 ┆ Howard Hawkins ┆ Green       ┆ 405035       ┆ loss   ┆ 0.255731  │
+ [text] └──────┴────────────────┴─────────────┴──────────────┴────────┴───────────┘
```

**Why:** One argument that is a list of integers is read as row positions, and every column comes back — here the last two rows of the table.
**Reader sees:** changed: the baseline's one-argument `[]` demo was the slice `elections[0:4]`. The list-of-positions form is new, and the rows shown are 2020's rather than 1824's.

<a id="c119"></a>
### C119 · `elections["Candidate"]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (182,)
+ [text] Series: 'Candidate' [str]
+ [text] [
+ [text] 	"Andrew Jackson"
+ [text] 	"John Quincy Adams"
+ [text] 	"Andrew Jackson"
+ [text] 	"John Quincy Adams"
+ [text] 	"Andrew Jackson"
+ [text] 	…
+ [text] 	"Jill Stein"
+ [text] 	"Joseph Biden"
+ [text] 	"Donald Trump"
+ [text] 	"Jo Jorgensen"
+ [text] 	"Howard Hawkins"
+ [text] ]
```

**Why:** A single string argument names a column, which comes back as a `Series`; the repr puts `shape: (182,)`, the name and the dtype in a header and abbreviates the middle.
**Reader sees:** equivalent: the baseline's `elections["Candidate"]`, whose `Length: 187, dtype: object` footer carried the same information for a longer file.

<a id="c120"></a>
### C120 · `elections[0, 1]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] 'Andrew Jackson'
```

**Why:** The second argument also accepts a column **number**, so `[0, 1]` is the same cell as `[0, "Candidate"]`.
**Reader sees:** changed: the baseline `iloc[0, 1]` cell committed no output at all, so this value is newly on the page. The label-versus-position lesson it opened is gone with the Index.

<a id="c121"></a>
### C121 · `elections[[1, 2, 3], 1]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3,)
+ [text] Series: 'Candidate' [str]
+ [text] [
+ [text] 	"John Quincy Adams"
+ [text] 	"Andrew Jackson"
+ [text] 	"John Quincy Adams"
+ [text] ]
```

**Why:** A list of row positions with a single column number returns a `Series`, as the comment says.
**Reader sees:** equivalent: the baseline's `iloc[[1, 2, 3], 1]` returned the same three names.

<a id="c122"></a>
### C122 · `elections[[1, 2, 3], [0, 1, 2]]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3, 3)
+ [text] ┌──────┬───────────────────┬───────────────────────┐
+ [text] │ Year ┆ Candidate         ┆ Party                 │
+ [text] │ ---  ┆ ---               ┆ ---                   │
+ [text] │ i64  ┆ str               ┆ str                   │
+ [text] ╞══════╪═══════════════════╪═══════════════════════╡
+ [text] │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican │
+ [text] │ 1828 ┆ Andrew Jackson    ┆ Democratic            │
+ [text] │ 1828 ┆ John Quincy Adams ┆ National Republican   │
+ [text] └──────┴───────────────────┴───────────────────────┘
```

**Why:** Lists on both sides select by position on both axes.
**Reader sees:** equivalent: the baseline's `iloc[[0, 1, 2, 3], [0, 1, 2, 3]]` made the same point on four rows.

<a id="c123"></a>
### C123 · `elections[[1, 2, 3], 0:3]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3, 3)
+ [text] ┌──────┬───────────────────┬───────────────────────┐
+ [text] │ Year ┆ Candidate         ┆ Party                 │
+ [text] │ ---  ┆ ---               ┆ ---                   │
+ [text] │ i64  ┆ str               ┆ str                   │
+ [text] ╞══════╪═══════════════════╪═══════════════════════╡
+ [text] │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican │
+ [text] │ 1828 ┆ Andrew Jackson    ┆ Democratic            │
+ [text] │ 1828 ┆ John Quincy Adams ┆ National Republican   │
+ [text] └──────┴───────────────────┴───────────────────────┘
```

**Why:** A slice of column **numbers** is exclusive, so column 3 (`Popular vote`) is absent — the contrast with the inclusive label slice at C113.
**Reader sees:** equivalent: the baseline drew the same exclusive/inclusive contrast with `iloc[0:4, 0:4]` against `.loc[0:3, 'Year':'Popular vote']`.

<a id="c124"></a>
### C124 · `elections[138:144]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (6, 6)
+ [text] ┌──────┬───────────────────┬─────────────┬──────────────┬────────┬───────────┐
+ [text] │ Year ┆ Candidate         ┆ Party       ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---  ┆ ---               ┆ ---         ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ i64  ┆ str               ┆ str         ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞══════╪═══════════════════╪═════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 1988 ┆ Ron Paul          ┆ Libertarian ┆ 431750       ┆ loss   ┆ 0.47266   │
+ [text] │ 1992 ┆ Andre Marrou      ┆ Libertarian ┆ 290087       ┆ loss   ┆ 0.278516  │
+ [text] │ 1992 ┆ Bill Clinton      ┆ Democratic  ┆ 44909806     ┆ win    ┆ 43.118485 │
+ [text] │ 1992 ┆ Bo Gritz          ┆ Populist    ┆ 106152       ┆ loss   ┆ 0.101918  │
+ [text] │ 1992 ┆ George H. W. Bush ┆ Republican  ┆ 39104550     ┆ loss   ┆ 37.544784 │
+ [text] │ 1992 ┆ Ross Perot        ┆ Independent ┆ 19743821     ┆ loss   ┆ 18.956298 │
+ [text] └──────┴───────────────────┴─────────────┴──────────────┴────────┴───────────┘
```

**Why:** A lone slice is read as row positions, giving six rows from 1988-1992 and every column.
**Reader sees:** equivalent: the baseline's `elections[0:4]` taught the same one-argument rule on different rows.

<a id="c125"></a>
### C125 · `elections.row(0)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] (1824, 'Andrew Jackson', 'Democratic-Republican', 151271, 'loss', 57.21012204)
```

**Why:** `.row()` returns a plain Python tuple of the row's values in column order; `%` prints at full stored precision (`57.21012204`) rather than the six figures the table shows.
**Reader sees:** changed: pandas' `iloc[0]` returned a `Series`, printed as a labeled column. A tuple has no labels, which is what motivates the next cell.

<a id="c126"></a>
### C126 · `elections.row(0, named=True)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] {'Year': 1824,
+ [text]  'Candidate': 'Andrew Jackson',
+ [text]  'Party': 'Democratic-Republican',
+ [text]  'Popular vote': 151271,
+ [text]  'Result': 'loss',
+ [text]  '%': 57.21012204}
```

**Why:** `named=True` returns a dictionary instead, so the field names come back with the values.
**Reader sees:** new: no baseline counterpart. It restores the labels the tuple drops, which is what pandas' `iloc[0]` gave for free.

<a id="c127"></a>
### C127 · `elections.select(["Year", "Candidate", "Result"])` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (182, 3)
+ [text] ┌──────┬───────────────────┬────────┐
+ [text] │ Year ┆ Candidate         ┆ Result │
+ [text] │ ---  ┆ ---               ┆ ---    │
+ [text] │ i64  ┆ str               ┆ str    │
+ [text] ╞══════╪═══════════════════╪════════╡
+ [text] │ 1824 ┆ Andrew Jackson    ┆ loss   │
+ [text] │ 1824 ┆ John Quincy Adams ┆ win    │
+ [text] │ 1828 ┆ Andrew Jackson    ┆ win    │
+ [text] │ 1828 ┆ John Quincy Adams ┆ loss   │
+ [text] │ 1832 ┆ Andrew Jackson    ┆ win    │
+ [text] │ …    ┆ …                 ┆ …      │
+ [text] │ 2016 ┆ Jill Stein        ┆ loss   │
+ [text] │ 2020 ┆ Joseph Biden      ┆ win    │
+ [text] │ 2020 ┆ Donald Trump      ┆ loss   │
+ [text] │ 2020 ┆ Jo Jorgensen      ┆ loss   │
+ [text] │ 2020 ┆ Howard Hawkins    ┆ loss   │
+ [text] └──────┴───────────────────┴────────┘
```

**Why:** `select` with a list of names returns all 182 rows and the three named columns.
**Reader sees:** equivalent: the baseline's `elections[["Year", "Candidate", "Party", "Popular vote"]]` did the same job through `[]`.

<a id="c128"></a>
### C128 · `elections.select((pl.col("Popular vote") / 1_000_000).alias("Popular v` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (182, 1)
+ [text] ┌─────────────────────────┐
+ [text] │ Popular vote (millions) │
+ [text] │ ---                     │
+ [text] │ f64                     │
+ [text] ╞═════════════════════════╡
+ [text] │ 0.151271                │
+ [text] │ 0.113142                │
+ [text] │ 0.642806                │
+ [text] │ 0.500897                │
+ [text] │ 0.702735                │
+ [text] │ …                       │
+ [text] │ 1.457226                │
+ [text] │ 81.268924               │
+ [text] │ 74.216154               │
+ [text] │ 1.865724                │
+ [text] │ 0.405035                │
+ [text] └─────────────────────────┘
```

**Why:** `select` evaluating an expression: `pl.col("Popular vote") / 1_000_000` applies to every value and `.alias` names the result, so the output is a single computed column.
**Reader sees:** new: the old chapters computed nothing inside a selection. It introduces `pl.col` before `filter` needs it.

<a id="c129"></a>
### C129 · `elections.filter(pl.col("Popular vote") > 60000000)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (8, 6)
+ [text] ┌──────┬─────────────────┬────────────┬──────────────┬────────┬───────────┐
+ [text] │ Year ┆ Candidate       ┆ Party      ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---  ┆ ---             ┆ ---        ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ i64  ┆ str             ┆ str        ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞══════╪═════════════════╪════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 2004 ┆ George W. Bush  ┆ Republican ┆ 62040610     ┆ win    ┆ 50.771824 │
+ [text] │ 2008 ┆ Barack Obama    ┆ Democratic ┆ 69498516     ┆ win    ┆ 53.02351  │
+ [text] │ 2012 ┆ Barack Obama    ┆ Democratic ┆ 65915795     ┆ win    ┆ 51.258484 │
+ [text] │ 2012 ┆ Mitt Romney     ┆ Republican ┆ 60933504     ┆ loss   ┆ 47.384076 │
+ [text] │ 2016 ┆ Donald Trump    ┆ Republican ┆ 62984828     ┆ win    ┆ 46.407862 │
+ [text] │ 2016 ┆ Hillary Clinton ┆ Democratic ┆ 65853514     ┆ loss   ┆ 48.521539 │
+ [text] │ 2020 ┆ Joseph Biden    ┆ Democratic ┆ 81268924     ┆ win    ┆ 51.311515 │
+ [text] │ 2020 ┆ Donald Trump    ┆ Republican ┆ 74216154     ┆ loss   ┆ 46.858542 │
+ [text] └──────┴─────────────────┴────────────┴──────────────┴────────┴───────────┘
```

**Why:** `filter` with one condition; eight rows clear 60 million votes, and the paragraph above reads that count off the output (verified against the shipped file).
**Reader sees:** new: the baseline opened conditional selection with a hand-written boolean array over `babynames`, which has no Polars form. The idea is the same; the dataset and the worked example are not.

<a id="c130"></a>
### C130 · `elections.filter(pl.col("Year") == 2008).select(["Year", "Candidate"])` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (6, 2)
+ [text] ┌──────┬──────────────────┐
+ [text] │ Year ┆ Candidate        │
+ [text] │ ---  ┆ ---              │
+ [text] │ i64  ┆ str              │
+ [text] ╞══════╪══════════════════╡
+ [text] │ 2008 ┆ Barack Obama     │
+ [text] │ 2008 ┆ Bob Barr         │
+ [text] │ 2008 ┆ Chuck Baldwin    │
+ [text] │ 2008 ┆ Cynthia McKinney │
+ [text] │ 2008 ┆ John McCain      │
+ [text] │ 2008 ┆ Ralph Nader      │
+ [text] └──────┴──────────────────┘
```

**Why:** Chaining `filter` then `select`: the six 2008 candidacies, two columns.
**Reader sees:** equivalent: `.loc[cond, cols]` did rows and columns in one call. The row labels 162-167 are gone with the Index.

<a id="c131"></a>
### C131 · `elections.filter((pl.col("Year") == 2008) | (pl.col("%") >= 60))` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (10, 6)
+ [text] ┌──────┬────────────────────┬──────────────┬──────────────┬────────┬───────────┐
+ [text] │ Year ┆ Candidate          ┆ Party        ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---  ┆ ---                ┆ ---          ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ i64  ┆ str                ┆ str          ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞══════╪════════════════════╪══════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 1920 ┆ Warren Harding     ┆ Republican   ┆ 16144093     ┆ win    ┆ 60.574501 │
+ [text] │ 1936 ┆ Franklin Roosevelt ┆ Democratic   ┆ 27752648     ┆ win    ┆ 60.978107 │
+ [text] │ 1964 ┆ Lyndon Johnson     ┆ Democratic   ┆ 43127041     ┆ win    ┆ 61.344703 │
+ [text] │ 1972 ┆ Richard Nixon      ┆ Republican   ┆ 47168710     ┆ win    ┆ 60.907806 │
+ [text] │ 2008 ┆ Barack Obama       ┆ Democratic   ┆ 69498516     ┆ win    ┆ 53.02351  │
+ [text] │ 2008 ┆ Bob Barr           ┆ Libertarian  ┆ 523715       ┆ loss   ┆ 0.399565  │
+ [text] │ 2008 ┆ Chuck Baldwin      ┆ Constitution ┆ 199750       ┆ loss   ┆ 0.152398  │
+ [text] │ 2008 ┆ Cynthia McKinney   ┆ Green        ┆ 161797       ┆ loss   ┆ 0.123442  │
+ [text] │ 2008 ┆ John McCain        ┆ Republican   ┆ 59948323     ┆ loss   ┆ 45.737243 │
+ [text] │ 2008 ┆ Ralph Nader        ┆ Independent  ┆ 739034       ┆ loss   ┆ 0.563842  │
+ [text] └──────┴────────────────────┴──────────────┴──────────────┴────────┴───────────┘
```

**Why:** `|` between two parenthesized conditions; ten rows satisfy either, and the paragraph below counts them off the table.
**Reader sees:** equivalent: the baseline's `|` demo ended in `.head()`, so only five rows were visible. The whole result now is, which is what lets the prose name the four landslide years.

<a id="c132"></a>
### C132 · `elections.filter((pl.col("Year") > 2000) & (pl.col("Result") == "win")` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 6)
+ [text] ┌──────┬────────────────┬────────────┬──────────────┬────────┬───────────┐
+ [text] │ Year ┆ Candidate      ┆ Party      ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---  ┆ ---            ┆ ---        ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ i64  ┆ str            ┆ str        ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞══════╪════════════════╪════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 2004 ┆ George W. Bush ┆ Republican ┆ 62040610     ┆ win    ┆ 50.771824 │
+ [text] │ 2008 ┆ Barack Obama   ┆ Democratic ┆ 69498516     ┆ win    ┆ 53.02351  │
+ [text] │ 2012 ┆ Barack Obama   ┆ Democratic ┆ 65915795     ┆ win    ┆ 51.258484 │
+ [text] │ 2016 ┆ Donald Trump   ┆ Republican ┆ 62984828     ┆ win    ┆ 46.407862 │
+ [text] │ 2020 ┆ Joseph Biden   ┆ Democratic ┆ 81268924     ┆ win    ┆ 51.311515 │
+ [text] └──────┴────────────────┴────────────┴──────────────┴────────┴───────────┘
```

**Why:** `&` between two conditions; the five post-2000 winners.
**Reader sees:** equivalent: the baseline's `&` example was `Sex == "F"` and `Year < 2000` on `babynames`, shown as a `.head()`. Same operator, same lesson, full result.

<a id="c133"></a>
### C133 · `elections.filter((pl.col("Year") == 2008) and (pl.col("%") >= 60))` · output

committed output

```diff
- [error] ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
+ [error] TypeError: the truth value of an Expr is ambiguous

You probably got here by using a Python standard library function instead of the native expressions API.
Here are some things you might want to try:
- instead of `pl.col('a') and pl.col('b')`, use `pl.col('a') & pl.col('b')`
- instead of `pl.col('a') in [y, z]`, use `pl.col('a').is_in([y, z])`
- instead of `max(pl.col('a'), pl.col('b'))`, use `pl.max_horizontal(pl.col('a'), pl.col('b'))`
```

**Why:** The chapter's deliberate error demo, restored under the baseline's own cell id (hard rule 6). Polars raises `TypeError: the truth value of an Expr is ambiguous` and appends its own hint block naming `&`, `is_in` and `max_horizontal`.
**Reader sees:** equivalent: same lesson — `and` is not `&` — with a longer message that also names the fix. pandas raised `ValueError` about a `Series`.

<a id="c134"></a>
### C134 · `elections.filter(` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 6)
+ [text] ┌──────┬───────────────────┬────────────┬──────────────┬────────┬───────────┐
+ [text] │ Year ┆ Candidate         ┆ Party      ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---  ┆ ---               ┆ ---        ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ i64  ┆ str               ┆ str        ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞══════╪═══════════════════╪════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 1952 ┆ Dwight Eisenhower ┆ Republican ┆ 34075529     ┆ win    ┆ 55.325173 │
+ [text] │ 1956 ┆ Dwight Eisenhower ┆ Republican ┆ 35579180     ┆ win    ┆ 57.650654 │
+ [text] │ 1964 ┆ Lyndon Johnson    ┆ Democratic ┆ 43127041     ┆ win    ┆ 61.344703 │
+ [text] │ 1972 ┆ Richard Nixon     ┆ Republican ┆ 47168710     ┆ win    ┆ 60.907806 │
+ [text] │ 1984 ┆ Ronald Reagan     ┆ Republican ┆ 54455472     ┆ win    ┆ 59.023326 │
+ [text] └──────┴───────────────────┴────────────┴──────────────┴────────┴───────────┘
```

**Why:** Four conditions over several lines; five rows survive.
**Reader sees:** new: the baseline's multi-line example was the four-name `babynames` filter, which is still in the chapter at C139. This one repeats the readability point on `elections`.

<a id="c135"></a>
### C135 · `elections.with_row_index("original_position").sort("%", descending=Tru` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 7)
+ [text] ┌───────────────────┬──────┬────────────────────┬────────────┬──────────────┬────────┬───────────┐
+ [text] │ original_position ┆ Year ┆ Candidate          ┆ Party      ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---               ┆ ---  ┆ ---                ┆ ---        ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ u32               ┆ i64  ┆ str                ┆ str        ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞═══════════════════╪══════╪════════════════════╪════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 114               ┆ 1964 ┆ Lyndon Johnson     ┆ Democratic ┆ 43127041     ┆ win    ┆ 61.344703 │
+ [text] │ 91                ┆ 1936 ┆ Franklin Roosevelt ┆ Democratic ┆ 27752648     ┆ win    ┆ 60.978107 │
+ [text] │ 120               ┆ 1972 ┆ Richard Nixon      ┆ Republican ┆ 47168710     ┆ win    ┆ 60.907806 │
+ [text] │ 79                ┆ 1920 ┆ Warren Harding     ┆ Republican ┆ 16144093     ┆ win    ┆ 60.574501 │
+ [text] │ 133               ┆ 1984 ┆ Ronald Reagan      ┆ Republican ┆ 54455472     ┆ win    ┆ 59.023326 │
+ [text] └───────────────────┴──────┴────────────────────┴────────────┴──────────────┴────────┴───────────┘
```

**Why:** `with_row_index("original_position")` writes each row's current position into a `u32` column *before* the sort, so the top row shows that Johnson's 1964 landslide sat at position 114.
**Reader sees:** new: this is what replaces the deleted Index section. The old chapters had no way to show where a row came from after a reorder — they had labels that travelled with the row instead.

<a id="c136"></a>
### C136 · `elections.head(3)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3, 6)
+ [text] ┌──────┬───────────────────┬───────────────────────┬──────────────┬────────┬───────────┐
+ [text] │ Year ┆ Candidate         ┆ Party                 ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---  ┆ ---               ┆ ---                   ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ i64  ┆ str               ┆ str                   ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞══════╪═══════════════════╪═══════════════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republican ┆ 151271       ┆ loss   ┆ 57.210122 │
+ [text] │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican ┆ 113142       ┆ win    ┆ 42.789878 │
+ [text] │ 1828 ┆ Andrew Jackson    ┆ Democratic            ┆ 642806       ┆ win    ┆ 56.203927 │
+ [text] └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────────┘
```

**Why:** `elections` printed again after C135: still six columns, still in file order, because `with_row_index` returned a new table.
**Reader sees:** new: the baseline made the not-in-place point only for `.drop`. Here it is made where a reader has just seen a table apparently change.

<a id="c137"></a>
### C137 · `elections.sort("%", descending=True).with_row_index().head()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 7)
+ [text] ┌───────┬──────┬────────────────────┬────────────┬──────────────┬────────┬───────────┐
+ [text] │ index ┆ Year ┆ Candidate          ┆ Party      ┆ Popular vote ┆ Result ┆ %         │
+ [text] │ ---   ┆ ---  ┆ ---                ┆ ---        ┆ ---          ┆ ---    ┆ ---       │
+ [text] │ u32   ┆ i64  ┆ str                ┆ str        ┆ i64          ┆ str    ┆ f64       │
+ [text] ╞═══════╪══════╪════════════════════╪════════════╪══════════════╪════════╪═══════════╡
+ [text] │ 0     ┆ 1964 ┆ Lyndon Johnson     ┆ Democratic ┆ 43127041     ┆ win    ┆ 61.344703 │
+ [text] │ 1     ┆ 1936 ┆ Franklin Roosevelt ┆ Democratic ┆ 27752648     ┆ win    ┆ 60.978107 │
+ [text] │ 2     ┆ 1972 ┆ Richard Nixon      ┆ Republican ┆ 47168710     ┆ win    ┆ 60.907806 │
+ [text] │ 3     ┆ 1920 ┆ Warren Harding     ┆ Republican ┆ 16144093     ┆ win    ┆ 60.574501 │
+ [text] │ 4     ┆ 1984 ┆ Ronald Reagan      ┆ Republican ┆ 54455472     ┆ win    ┆ 59.023326 │
+ [text] └───────┴──────┴────────────────────┴────────────┴──────────────┴────────┴───────────┘
```

**Why:** The same two operations in the other order, so the index column counts 0-4 down the *sorted* table.
**Reader sees:** new: the before/after contrast has no baseline counterpart; under pandas the labels would have followed the rows.

<a id="c138"></a>
### C138 · `import urllib.request` · output

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

**Why:** The download cell re-executed: `pl.read_csv(fh, has_header=False, new_columns=field_names)` and a `.head()`, giving 1910's five most common girls' names.
**Reader sees:** equivalent: identical five rows to the baseline's `babynames.head()`.

<a id="c139"></a>
### C139 · `(` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (317, 5)
+ [text] ┌───────┬─────┬──────┬───────┬───────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name  ┆ Count │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---   ┆ ---   │
+ [text] │ str   ┆ str ┆ i64  ┆ str   ┆ i64   │
+ [text] ╞═══════╪═════╪══════╪═══════╪═══════╡
+ [text] │ CA    ┆ F   ┆ 1923 ┆ Bella ┆ 5     │
+ [text] │ CA    ┆ F   ┆ 1925 ┆ Bella ┆ 8     │
+ [text] │ CA    ┆ F   ┆ 1932 ┆ Lisa  ┆ 5     │
+ [text] │ CA    ┆ F   ┆ 1936 ┆ Lisa  ┆ 8     │
+ [text] │ CA    ┆ F   ┆ 1939 ┆ Lisa  ┆ 5     │
+ [text] │ …     ┆ …   ┆ …    ┆ …     ┆ …     │
+ [text] │ CA    ┆ M   ┆ 2018 ┆ Alex  ┆ 495   │
+ [text] │ CA    ┆ M   ┆ 2019 ┆ Alex  ┆ 438   │
+ [text] │ CA    ┆ M   ┆ 2020 ┆ Alex  ┆ 379   │
+ [text] │ CA    ┆ M   ┆ 2021 ┆ Alex  ┆ 333   │
+ [text] │ CA    ┆ M   ┆ 2022 ┆ Alex  ┆ 344   │
+ [text] └───────┴─────┴──────┴───────┴───────┘
```

**Why:** The verbose four-way `|` filter, committed with its whole 317-row result rather than a `.head()` (verified against the shipped zip).
**Reader sees:** changed: the baseline printed only the first five rows, so the reader could not see what `is_in` has to reproduce. The row count is now on the page for the next cell to match.

<a id="c140"></a>
### C140 · `names = ["Bella", "Alex", "Narges", "Lisa"]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (317, 5)
+ [text] ┌───────┬─────┬──────┬───────┬───────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name  ┆ Count │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---   ┆ ---   │
+ [text] │ str   ┆ str ┆ i64  ┆ str   ┆ i64   │
+ [text] ╞═══════╪═════╪══════╪═══════╪═══════╡
+ [text] │ CA    ┆ F   ┆ 1923 ┆ Bella ┆ 5     │
+ [text] │ CA    ┆ F   ┆ 1925 ┆ Bella ┆ 8     │
+ [text] │ CA    ┆ F   ┆ 1932 ┆ Lisa  ┆ 5     │
+ [text] │ CA    ┆ F   ┆ 1936 ┆ Lisa  ┆ 8     │
+ [text] │ CA    ┆ F   ┆ 1939 ┆ Lisa  ┆ 5     │
+ [text] │ …     ┆ …   ┆ …    ┆ …     ┆ …     │
+ [text] │ CA    ┆ M   ┆ 2018 ┆ Alex  ┆ 495   │
+ [text] │ CA    ┆ M   ┆ 2019 ┆ Alex  ┆ 438   │
+ [text] │ CA    ┆ M   ┆ 2020 ┆ Alex  ┆ 379   │
+ [text] │ CA    ┆ M   ┆ 2021 ┆ Alex  ┆ 333   │
+ [text] │ CA    ┆ M   ┆ 2022 ┆ Alex  ┆ 344   │
+ [text] └───────┴─────┴──────┴───────┴───────┘
```

**Why:** `is_in` against a list of four names, returning the same 317 rows in one line.
**Reader sees:** changed: the baseline spent two cells here — the boolean `Series` from `.isin`, then the filtered `.head()`. The boolean-array display went with the deleted mask material; the full result replaces it. The baseline also asked for `Ani` in the verbose version and `Narges` in the `isin` version; both spellings are now `Narges`.

<a id="c141"></a>
### C141 · `babynames.filter(pl.col("Name").str.starts_with("N"))` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (12_229, 5)
+ [text] ┌───────┬─────┬──────┬────────┬───────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name   ┆ Count │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---    ┆ ---   │
+ [text] │ str   ┆ str ┆ i64  ┆ str    ┆ i64   │
+ [text] ╞═══════╪═════╪══════╪════════╪═══════╡
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Norma  ┆ 23    │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Nellie ┆ 20    │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Nina   ┆ 11    │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Nora   ┆ 6     │
+ [text] │ CA    ┆ F   ┆ 1911 ┆ Nellie ┆ 23    │
+ [text] │ …     ┆ …   ┆ …    ┆ …      ┆ …     │
+ [text] │ CA    ┆ M   ┆ 2022 ┆ Nilan  ┆ 5     │
+ [text] │ CA    ┆ M   ┆ 2022 ┆ Niles  ┆ 5     │
+ [text] │ CA    ┆ M   ┆ 2022 ┆ Nolen  ┆ 5     │
+ [text] │ CA    ┆ M   ┆ 2022 ┆ Noriel ┆ 5     │
+ [text] │ CA    ┆ M   ┆ 2022 ┆ Norris ┆ 5     │
+ [text] └───────┴─────┴──────┴────────┴───────┘
```

**Why:** `.str.starts_with("N")` inside `filter`; 12,229 rows, shown whole (verified).
**Reader sees:** changed: the baseline showed the boolean `Series` head and then a filtered `.head()`. One cell and a row count replace them.

<a id="c142"></a>
### C142 · `yash_counts = babynames.filter(pl.col("Name") == "Yash")["Count"]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (28,)
+ [text] Series: 'Count' [i64]
+ [text] [
+ [text] 	8
+ [text] 	9
+ [text] 	11
+ [text] 	12
+ [text] 	10
+ [text] 	…
+ [text] 	10
+ [text] 	9
+ [text] 	15
+ [text] 	13
+ [text] 	13
+ [text] ]
```

**Why:** The `Count` column for every year the name Yash was recorded, as a `Series`; the repr gives `shape: (28,)` and abbreviates the middle.
**Reader sees:** changed: the baseline printed `.head()` (five values). The 28 that the next sentence quotes is now visible in the output.

<a id="c143"></a>
### C143 · `yash_counts.mean()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] 17.142857142857142
```

**Why:** `Series.mean()` replaces `np.mean(...)`, which raises on a Polars `Series` (the NumPy reduction dispatch passes `axis=`).
**Reader sees:** equivalent: 17.142857142857142, identical to the baseline's value (verified).

<a id="c144"></a>
### C144 · `yash_counts.max()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] 29
```

**Why:** `Series.max()` replaces `np.max(...)` for the same reason.
**Reader sees:** equivalent: 29, identical to the baseline (verified).

<a id="c145"></a>
### C145 · `babynames.shape` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] (407428, 5)
```

**Why:** `.shape` on the full `babynames` table.
**Reader sees:** equivalent: `(407428, 5)`, identical to the baseline (verified against the shipped zip).

<a id="c146"></a>
### C146 · `babynames.height * babynames.width` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] 2037140
```

**Why:** Polars has no `.size`, so the total number of values is stated as the product of `.height` and `.width` and prints as a plain integer.
**Reader sees:** equivalent: 2037140, the same number the baseline's `.size` printed.

<a id="c147"></a>
### C147 · `len(babynames)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] 407428
```

**Why:** `len(df)` returns the height.
**Reader sees:** new: a small addition beside `.height`/`.width`; the baseline had no such cell.

<a id="c148"></a>
### C148 · `babynames.describe()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (9, 6)
+ [text] ┌────────────┬────────┬────────┬─────────────┬────────┬────────────┐
+ [text] │ statistic  ┆ State  ┆ Sex    ┆ Year        ┆ Name   ┆ Count      │
+ [text] │ ---        ┆ ---    ┆ ---    ┆ ---         ┆ ---    ┆ ---        │
+ [text] │ str        ┆ str    ┆ str    ┆ f64         ┆ str    ┆ f64        │
+ [text] ╞════════════╪════════╪════════╪═════════════╪════════╪════════════╡
+ [text] │ count      ┆ 407428 ┆ 407428 ┆ 407428.0    ┆ 407428 ┆ 407428.0   │
+ [text] │ null_count ┆ 0      ┆ 0      ┆ 0.0         ┆ 0      ┆ 0.0        │
+ [text] │ mean       ┆ null   ┆ null   ┆ 1985.733609 ┆ null   ┆ 79.543456  │
+ [text] │ std        ┆ null   ┆ null   ┆ 27.00766    ┆ null   ┆ 293.698654 │
+ [text] │ min        ┆ CA     ┆ F      ┆ 1910.0      ┆ Aadan  ┆ 5.0        │
+ [text] │ 25%        ┆ null   ┆ null   ┆ 1969.0      ┆ null   ┆ 7.0        │
+ [text] │ 50%        ┆ null   ┆ null   ┆ 1992.0      ┆ null   ┆ 13.0       │
+ [text] │ 75%        ┆ null   ┆ null   ┆ 2008.0      ┆ null   ┆ 38.0       │
+ [text] │ max        ┆ CA     ┆ M      ┆ 2022.0      ┆ Zyrus  ┆ 8260.0     │
+ [text] └────────────┴────────┴────────┴─────────────┴────────┴────────────┘
```

**Why:** Polars describes **every** column, including the three `String` ones, and adds a `null_count` row; the statistics are rows labeled by a `statistic` column instead of a pandas index. The `Year` and `Count` figures match the baseline exactly.
**Reader sees:** changed: the baseline described only `Year` and `Count`. The reader gains null counts and the alphabetical min/max of the string columns — but the paired pandas tab still shows the two-column table, so the new sentence "Text columns are described too" holds for the Polars pane only, and the pandas pane has no `null_count` row for the next paragraph to read off (Summary, C28/C149).

<a id="c149"></a>
### C149 · `babynames["Sex"].describe()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (4, 2)
+ [text] ┌────────────┬────────┐
+ [text] │ statistic  ┆ value  │
+ [text] │ ---        ┆ ---    │
+ [text] │ str        ┆ str    │
+ [text] ╞════════════╪════════╡
+ [text] │ count      ┆ 407428 │
+ [text] │ null_count ┆ 0      │
+ [text] │ min        ┆ F      │
+ [text] │ max        ┆ M      │
+ [text] └────────────┴────────┘
```

**Why:** A `String` `Series` describes itself with `count`, `null_count`, `min` and `max` — the statistics Polars defines for that dtype.
**Reader sees:** changed: pandas reported `unique`, `top` and `freq`, so the reader loses that `F` is the most common value and occurs 239,537 times. The paragraph's "statistics that suit its data type" no longer delivers a mode; `value_counts` two sections later supplies the same numbers.

<a id="c150"></a>
### C150 · `babynames.sample()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (1, 5)
+ [text] ┌───────┬─────┬──────┬────────┬───────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name   ┆ Count │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---    ┆ ---   │
+ [text] │ str   ┆ str ┆ i64  ┆ str    ┆ i64   │
+ [text] ╞═══════╪═════╪══════╪════════╪═══════╡
+ [text] │ CA    ┆ F   ┆ 2019 ┆ Malena ┆ 13    │
+ [text] └───────┴─────┴──────┴────────┴───────┘
```

**Why:** One random row, committed as executed.
**Reader sees:** changed: the baseline cell shipped no output at all, so a sampled row is newly on the page — and, being a sample, it is a different row after every re-execution.

<a id="c151"></a>
### C151 · `babynames.sample(5)[:, 2:]` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 3)
+ [text] ┌──────┬──────────┬───────┐
+ [text] │ Year ┆ Name     ┆ Count │
+ [text] │ ---  ┆ ---      ┆ ---   │
+ [text] │ i64  ┆ str      ┆ i64   │
+ [text] ╞══════╪══════════╪═══════╡
+ [text] │ 1930 ┆ Sofia    ┆ 12    │
+ [text] │ 2005 ┆ Lael     ┆ 6     │
+ [text] │ 2009 ┆ Shilah   ┆ 12    │
+ [text] │ 1995 ┆ Katerine ┆ 5     │
+ [text] │ 1920 ┆ Refugio  ┆ 6     │
+ [text] └──────┴──────────┴───────┘
```

**Why:** Five random rows, then `[:, 2:]` keeps the columns from position 2 on.
**Reader sees:** equivalent: the baseline's `.sample(5).iloc[:, 2:]` showed five different random rows; `[:, 2:]` replaces `.iloc`.

<a id="c152"></a>
### C152 · `result = (` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (4, 3)
+ [text] ┌──────┬───────────┬───────┐
+ [text] │ Year ┆ Name      ┆ Count │
+ [text] │ ---  ┆ ---       ┆ ---   │
+ [text] │ i64  ┆ str       ┆ i64   │
+ [text] ╞══════╪═══════════╪═══════╡
+ [text] │ 2000 ┆ Jeancarlo ┆ 10    │
+ [text] │ 2000 ┆ Ernest    ┆ 57    │
+ [text] │ 2000 ┆ Socorro   ┆ 9     │
+ [text] │ 2000 ┆ Ankita    ┆ 12    │
+ [text] └──────┴───────────┴───────┘
```

**Why:** `filter` to the year 2000, then `.sample(4, with_replacement=True)` and a column slice; `with_replacement=` is the Polars spelling of pandas' `replace=`.
**Reader sees:** changed: the baseline cell committed no output, so this result is newly on the page, and like C150 it changes on every re-execution.

<a id="c153"></a>
### C153 · `babynames["Sex"].value_counts()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (2, 2)
+ [text] ┌─────┬────────┐
+ [text] │ Sex ┆ count  │
+ [text] │ --- ┆ ---    │
+ [text] │ str ┆ u32    │
+ [text] ╞═════╪════════╡
+ [text] │ F   ┆ 239537 │
+ [text] │ M   ┆ 167891 │
+ [text] └─────┴────────┘
```

**Why:** `value_counts` on a two-valued column, returning a two-column frame: the distinct values keep the `Series` name, the counts land in `count` (`u32`).
**Reader sees:** new: the baseline counted names only. This is where the paragraph below explains the frame-not-Series shape, so it needs a small example first.

<a id="c154"></a>
### C154 · `babynames["Name"].value_counts(sort=True).head()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 2)
+ [text] ┌───────────┬───────┐
+ [text] │ Name      ┆ count │
+ [text] │ ---       ┆ ---   │
+ [text] │ str       ┆ u32   │
+ [text] ╞═══════════╪═══════╡
+ [text] │ Jean      ┆ 223   │
+ [text] │ Francis   ┆ 221   │
+ [text] │ Guadalupe ┆ 218   │
+ [text] │ Jessie    ┆ 217   │
+ [text] │ Marion    ┆ 214   │
+ [text] └───────────┴───────┘
```

**Why:** `sort=True` is required because Polars does not rank by default; `.head()` then gives the five names recorded in the most sex-and-year combinations.
**Reader sees:** equivalent: the same five names and counts as the baseline (Jean 223 through Marion 214, verified), now as a two-column frame rather than a `Series` indexed by name.

<a id="c155"></a>
### C155 · `babynames["Name"].unique()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (20_437,)
+ [text] Series: 'Name' [str]
+ [text] [
+ [text] 	"Silvestre"
+ [text] 	"Angelic"
+ [text] 	"Chelsee"
+ [text] 	"Jyl"
+ [text] 	"Latasha"
+ [text] 	…
+ [text] 	"Ronnesha"
+ [text] 	"Suriya"
+ [text] 	"Demiana"
+ [text] 	"Brena"
+ [text] 	"Dafnee"
+ [text] ]
```

**Why:** The 20,437 distinct names as a `Series`, printed in Polars' internal (hash) order.
**Reader sees:** changed: pandas printed a truncated ndarray beginning `Mary, Helen, Dorothy`, i.e. order of appearance. The values committed here are one arbitrary draw — verified non-reproducible: two consecutive runs gave different first values. The prose does not quote them, and C157 restores the appearance order.

<a id="c156"></a>
### C156 · `babynames["Name"].n_unique()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] 20437
```

**Why:** `n_unique()` states the count directly: 20,437 (verified).
**Reader sees:** new: the baseline left the count implicit in the array repr; the paragraph now quotes it.

<a id="c157"></a>
### C157 · `babynames["Name"].unique(maintain_order=True).head(5)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5,)
+ [text] Series: 'Name' [str]
+ [text] [
+ [text] 	"Mary"
+ [text] 	"Helen"
+ [text] 	"Dorothy"
+ [text] 	"Margaret"
+ [text] 	"Frances"
+ [text] ]
```

**Why:** `maintain_order=True` returns the distinct values in order of first appearance, so `.head(5)` gives the top of the table. `.head(5)` is explicit because `Series.head()` defaults to ten.
**Reader sees:** new: it recovers the ordering pandas gave for free, and names the keyword that costs it.

<a id="c158"></a>
### C158 · `babyname_lengths = babynames["Name"].str.len_chars()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 6)
+ [text] ┌───────┬─────┬──────┬──────────┬───────┬──────────────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name     ┆ Count ┆ name_lengths │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   ┆ ---          │
+ [text] │ str   ┆ str ┆ i64  ┆ str      ┆ i64   ┆ u32          │
+ [text] ╞═══════╪═════╪══════╪══════════╪═══════╪══════════════╡
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   ┆ 4            │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   ┆ 5            │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   ┆ 7            │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   ┆ 8            │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   ┆ 7            │
+ [text] └───────┴─────┴──────┴──────────┴───────┴──────────────┘
```

**Why:** `with_columns(name_lengths=...)` adds the column; `.str.len_chars()` counts characters and the result is `u32`.
**Reader sees:** equivalent: the same five lengths as the baseline (4, 5, 7, 8, 7). The assignment moved from `df["col"] = ...` to `with_columns`.

<a id="c159"></a>
### C159 · `babynames = babynames.with_columns(name_lengths=pl.col("name_lengths")` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 6)
+ [text] ┌───────┬─────┬──────┬──────────┬───────┬──────────────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name     ┆ Count ┆ name_lengths │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   ┆ ---          │
+ [text] │ str   ┆ str ┆ i64  ┆ str      ┆ i64   ┆ u32          │
+ [text] ╞═══════╪═════╪══════╪══════════╪═══════╪══════════════╡
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   ┆ 3            │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   ┆ 4            │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   ┆ 6            │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   ┆ 7            │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   ┆ 6            │
+ [text] └───────┴─────┴──────┴──────────┴───────┴──────────────┘
```

**Why:** The same keyword re-used for an existing name replaces that column; `pl.col("name_lengths")` reads it as it currently stands.
**Reader sees:** equivalent: the same five values as the baseline (3, 4, 6, 7, 6).

<a id="c160"></a>
### C160 · `babynames = babynames.rename({"name_lengths": "Length"})` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 6)
+ [text] ┌───────┬─────┬──────┬──────────┬───────┬────────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name     ┆ Count ┆ Length │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   ┆ ---    │
+ [text] │ str   ┆ str ┆ i64  ┆ str      ┆ i64   ┆ u32    │
+ [text] ╞═══════╪═════╪══════╪══════════╪═══════╪════════╡
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   ┆ 3      │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   ┆ 4      │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   ┆ 6      │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   ┆ 7      │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   ┆ 6      │
+ [text] └───────┴─────┴──────┴──────────┴───────┴────────┘
```

**Why:** `.rename()` takes the same old-to-new dictionary as pandas, without the `columns=` keyword.
**Reader sees:** equivalent: identical table to the baseline's.

<a id="c161"></a>
### C161 · `babynames = babynames.drop("Length")` · output

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

**Why:** `.drop("Length")` needs no `axis=`, since dropping rows is `filter`'s job.
**Reader sees:** equivalent: identical table to the baseline's.

<a id="c162"></a>
### C162 · `babynames.drop("Name")` · output

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

**Why:** The cell's committed output is the trailing `.head()`, which still has `Name`; the discarded `.drop("Name")` result is never displayed, because only the last expression in a cell renders.
**Reader sees:** equivalent: the baseline cell has the same shape and the same committed output. The comment promising a table without `Name` shows nothing in either version — pre-existing, flagged in the Summary.

<a id="c163"></a>
### C163 · `babynames.sort("Count").head()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 5)
+ [text] ┌───────┬─────┬──────┬──────────┬───────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name     ┆ Count │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   │
+ [text] │ str   ┆ str ┆ i64  ┆ str      ┆ i64   │
+ [text] ╞═══════╪═════╪══════╪══════════╪═══════╡
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Adelaide ┆ 5     │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Adele    ┆ 5     │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Adrienne ┆ 5     │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Althea   ┆ 5     │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Antonia  ┆ 5     │
+ [text] └───────┴─────┴──────┴──────────┴───────┘
```

**Why:** Ascending sort on `Count`, then `.head()`. Every count in the file is at least 5, and thousands of rows tie at that floor, so which five surface is a tie-break rather than a fact about the data (verified reproducible on the shipped zip).
**Reader sees:** new: the baseline sorted `Count` only downward. The ascending direction is now the default case the prose introduces, and the tie means the two panes of its tab-set show different rows (Summary, C66/C67).

<a id="c164"></a>
### C164 · `babynames.sort("Count", descending=True).head()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 5)
+ [text] ┌───────┬─────┬──────┬─────────┬───────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name    ┆ Count │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---     ┆ ---   │
+ [text] │ str   ┆ str ┆ i64  ┆ str     ┆ i64   │
+ [text] ╞═══════╪═════╪══════╪═════════╪═══════╡
+ [text] │ CA    ┆ M   ┆ 1957 ┆ Michael ┆ 8260  │
+ [text] │ CA    ┆ M   ┆ 1956 ┆ Michael ┆ 8258  │
+ [text] │ CA    ┆ M   ┆ 1990 ┆ Michael ┆ 8246  │
+ [text] │ CA    ┆ M   ┆ 1969 ┆ Michael ┆ 8245  │
+ [text] │ CA    ┆ M   ┆ 1970 ┆ Michael ┆ 8196  │
+ [text] └───────┴─────┴──────┴─────────┴───────┘
```

**Why:** `descending=True` replaces pandas' `ascending=False`; the five largest counts in the file.
**Reader sees:** equivalent: the same five Michael rows and counts as the baseline (8260, 8258, 8246, 8245, 8196), verified.

<a id="c165"></a>
### C165 · `babynames["Name"].sort().head(5)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5,)
+ [text] Series: 'Name' [str]
+ [text] [
+ [text] 	"Aadan"
+ [text] 	"Aadan"
+ [text] 	"Aadan"
+ [text] 	"Aadarsh"
+ [text] 	"Aaden"
+ [text] ]
```

**Why:** A `Series` sorts with no column to name. `.head(5)` is written out because `Series.head()` defaults to ten, and the sentence above teaches five.
**Reader sees:** equivalent: the baseline's five values (`Aadan` three times, `Aadarsh`, `Aaden`), without the index labels pandas printed beside them.

<a id="c166"></a>
### C166 · `demo = pl.DataFrame({"Name": ["Aaliyah", "Bao", "Cyrus"], "Count": [3,` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3, 2)
+ [text] ┌─────────┬───────┐
+ [text] │ Name    ┆ Count │
+ [text] │ ---     ┆ ---   │
+ [text] │ str     ┆ i64   │
+ [text] ╞═════════╪═══════╡
+ [text] │ Bao     ┆ null  │
+ [text] │ Aaliyah ┆ 3     │
+ [text] │ Cyrus   ┆ 1     │
+ [text] └─────────┴───────┘
```

**Why:** A three-row table built for the demo, sorted descending: the `null` count comes out **first**, ahead of 3 (hard rule 8).
**Reader sees:** new: the old chapters said nothing about where missing values sort. The table exists because neither real dataset in the chapter has a null to show.

<a id="c167"></a>
### C167 · `demo.sort("Count", descending=True, nulls_last=True)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (3, 2)
+ [text] ┌─────────┬───────┐
+ [text] │ Name    ┆ Count │
+ [text] │ ---     ┆ ---   │
+ [text] │ str     ┆ i64   │
+ [text] ╞═════════╪═══════╡
+ [text] │ Aaliyah ┆ 3     │
+ [text] │ Cyrus   ┆ 1     │
+ [text] │ Bao     ┆ null  │
+ [text] └─────────┴───────┘
```

**Why:** `nulls_last=True` sends the null to the bottom, where a following `.head()` will not pick it up.
**Reader sees:** new: the fix for C166. The pandas tab beside it is unchanged, since `sort_values` already put `NaN` last — which is the point the paragraph makes.

<a id="c168"></a>
### C168 · `babyname_lengths = babynames["Name"].str.len_chars()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 6)
+ [text] ┌───────┬─────┬──────┬──────────┬───────┬──────────────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name     ┆ Count ┆ name_lengths │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   ┆ ---          │
+ [text] │ str   ┆ str ┆ i64  ┆ str      ┆ i64   ┆ u32          │
+ [text] ╞═══════╪═════╪══════╪══════════╪═══════╪══════════════╡
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   ┆ 4            │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   ┆ 5            │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   ┆ 7            │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   ┆ 8            │
+ [text] │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   ┆ 7            │
+ [text] └───────┴─────┴──────┴──────────┴───────┴──────────────┘
```

**Why:** Approach 1 re-adds `name_lengths` with `.str.len_chars()`.
**Reader sees:** equivalent: the same five lengths as the baseline's Approach 1.

<a id="c169"></a>
### C169 · `babynames = babynames.sort(by="name_lengths", descending=True)` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 6)
+ [text] ┌───────┬─────┬──────┬─────────────────┬───────┬──────────────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name            ┆ Count ┆ name_lengths │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---             ┆ ---   ┆ ---          │
+ [text] │ str   ┆ str ┆ i64  ┆ str             ┆ i64   ┆ u32          │
+ [text] ╞═══════╪═════╪══════╪═════════════════╪═══════╪══════════════╡
+ [text] │ CA    ┆ F   ┆ 1986 ┆ Mariadelosangel ┆ 5     ┆ 15           │
+ [text] │ CA    ┆ M   ┆ 1987 ┆ Franciscojavier ┆ 5     ┆ 15           │
+ [text] │ CA    ┆ M   ┆ 1988 ┆ Franciscojavier ┆ 10    ┆ 15           │
+ [text] │ CA    ┆ M   ┆ 1989 ┆ Franciscojavier ┆ 6     ┆ 15           │
+ [text] │ CA    ┆ M   ┆ 1991 ┆ Ryanchristopher ┆ 7     ┆ 15           │
+ [text] └───────┴─────┴──────┴─────────────────┴───────┴──────────────┘
```

**Why:** Sorting on the temporary column. The longest names run to 15 characters and many rows tie there, so the five on top are whatever the stable sort left (verified reproducible under polars 1.43.1).
**Reader sees:** changed: the baseline's five were `Franciscojavier` three times, `Ryanchristopher` and `Johnchristopher`; Polars surfaces `Mariadelosangel` first. The claim the section makes — the longest names are 15 characters — is unaffected.

<a id="c170"></a>
### C170 · `babynames = babynames.drop("name_lengths")` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 5)
+ [text] ┌───────┬─────┬──────┬─────────────────┬───────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name            ┆ Count │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---             ┆ ---   │
+ [text] │ str   ┆ str ┆ i64  ┆ str             ┆ i64   │
+ [text] ╞═══════╪═════╪══════╪═════════════════╪═══════╡
+ [text] │ CA    ┆ F   ┆ 1986 ┆ Mariadelosangel ┆ 5     │
+ [text] │ CA    ┆ M   ┆ 1987 ┆ Franciscojavier ┆ 5     │
+ [text] │ CA    ┆ M   ┆ 1988 ┆ Franciscojavier ┆ 10    │
+ [text] │ CA    ┆ M   ┆ 1989 ┆ Franciscojavier ┆ 6     │
+ [text] │ CA    ┆ M   ┆ 1991 ┆ Ryanchristopher ┆ 7     │
+ [text] └───────┴─────┴──────┴─────────────────┴───────┘
```

**Why:** The same tie-broken five rows with the temporary column dropped.
**Reader sees:** changed: the same tie-order difference as C169; the baseline showed the `Franciscojavier`/`Johnchristopher` set.

<a id="c171"></a>
### C171 · `babynames.sort(pl.col("Name").str.len_chars(), descending=True).head()` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 5)
+ [text] ┌───────┬─────┬──────┬─────────────────┬───────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name            ┆ Count │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---             ┆ ---   │
+ [text] │ str   ┆ str ┆ i64  ┆ str             ┆ i64   │
+ [text] ╞═══════╪═════╪══════╪═════════════════╪═══════╡
+ [text] │ CA    ┆ F   ┆ 1986 ┆ Mariadelosangel ┆ 5     │
+ [text] │ CA    ┆ M   ┆ 1987 ┆ Franciscojavier ┆ 5     │
+ [text] │ CA    ┆ M   ┆ 1988 ┆ Franciscojavier ┆ 10    │
+ [text] │ CA    ┆ M   ┆ 1989 ┆ Franciscojavier ┆ 6     │
+ [text] │ CA    ┆ M   ┆ 1991 ┆ Ryanchristopher ┆ 7     │
+ [text] └───────┴─────┴──────┴─────────────────┴───────┘
```

**Why:** Approach 2 hands `.sort()` an expression, computing the key on the way in. `babynames` is still in Approach 1's order at this point, and the sort is stable, so the same five rows come back.
**Reader sees:** changed: pandas' `sort_values(key=...)` has no Polars form, and the baseline's Approach 2 printed a *different* top five from its Approach 1 — a visible reshuffle among the 15-character ties. Here the two approaches print the same rows, so that incidental contrast is gone; the approaches themselves still differ (no temporary column to create or drop).

<a id="c172"></a>
### C172 · `def dr_ea_count(string):` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 6)
+ [text] ┌───────┬─────┬──────┬──────────┬───────┬─────────────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name     ┆ Count ┆ dr_ea_count │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   ┆ ---         │
+ [text] │ str   ┆ str ┆ i64  ┆ str      ┆ i64   ┆ i64         │
+ [text] ╞═══════╪═════╪══════╪══════════╪═══════╪═════════════╡
+ [text] │ CA    ┆ F   ┆ 1986 ┆ Deandrea ┆ 6     ┆ 3           │
+ [text] │ CA    ┆ F   ┆ 1988 ┆ Deandrea ┆ 5     ┆ 3           │
+ [text] │ CA    ┆ F   ┆ 1990 ┆ Deandrea ┆ 5     ┆ 3           │
+ [text] │ CA    ┆ F   ┆ 1994 ┆ Leandrea ┆ 5     ┆ 3           │
+ [text] │ CA    ┆ M   ┆ 1985 ┆ Deandrea ┆ 6     ┆ 3           │
+ [text] └───────┴─────┴──────┴──────────┴───────┴─────────────┘
```

**Why:** Approach 3: `map_elements(dr_ea_count, return_dtype=pl.Int64)` replaces `.map(fn)`; `return_dtype` is required to avoid a warning. All five rows score 3.
**Reader sees:** equivalent: the same five `Deandrea`/`Leandrea` rows as the baseline, in a different tie order.

<a id="c173"></a>
### C173 · `babynames = babynames.drop("dr_ea_count")` · output

committed output · no matching baseline cell — compare against the chapter, not the hunk

```diff
+ [text] shape: (5, 5)
+ [text] ┌───────┬─────┬──────┬──────────┬───────┐
+ [text] │ State ┆ Sex ┆ Year ┆ Name     ┆ Count │
+ [text] │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   │
+ [text] │ str   ┆ str ┆ i64  ┆ str      ┆ i64   │
+ [text] ╞═══════╪═════╪══════╪══════════╪═══════╡
+ [text] │ CA    ┆ F   ┆ 1986 ┆ Deandrea ┆ 6     │
+ [text] │ CA    ┆ F   ┆ 1988 ┆ Deandrea ┆ 5     │
+ [text] │ CA    ┆ F   ┆ 1990 ┆ Deandrea ┆ 5     │
+ [text] │ CA    ┆ F   ┆ 1994 ┆ Leandrea ┆ 5     │
+ [text] │ CA    ┆ M   ┆ 1985 ┆ Deandrea ┆ 6     │
+ [text] └───────┴─────┴──────┴──────────┴───────┘
```

**Why:** The temporary column dropped again, leaving the same five rows.
**Reader sees:** equivalent: the baseline's five rows, reordered by the same tie-break as C172.

