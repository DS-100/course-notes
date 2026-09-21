# intro_lec — change report

`887a578b0a4b:content/intro_lec/introduction.ipynb` → `content/intro_lec/introduction.ipynb`

**Tier B · 41 changes:** output 11 · prose 12 · mixed 3 · tab-twins 5 · code 2 · mechanical 5 · metadata 3

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

A re-aim, not a rename. The chapter's `Series` section was built on the pandas index, which Polars does not have, so five demo cells were re-pointed at a `Series`' name, dtype and position, and the third "fundamental data structure" was dropped. Three things to look at: C13–C16, where the gate-frozen `images/df_elections.png` still draws an index and the prose has to name pandas' vocabulary to reconcile it — the one place in the book that explains a picture it cannot redraw; C19, the single pandas/Polars twin whose two panes run different operations (`s.name, s.dtype` against `s.index`), kept on purpose after five sibling twins were deleted for exactly that (§B1); and C8, where a correct but three-line NumPy-reduction caveat lands in the chapter's opening bullet list. All eleven changed outputs are the Polars `Series` repr; none carries a number the prose quotes.

## Needs review

- [C6](#c6) · cell 1: Tabular Data and `polars`
- [C8](#c8) · cell 1: Tabular Data and `polars`
- [C11](#c11) · cell 3 [markdown]
- [C12](#c12) · cell 3 [markdown]
- [C13](#c13) · cell 3 [markdown]
- [C14](#c14) · cell 3 [markdown]
- [C15](#c15) · cell 3 [markdown]
- [C16](#c16) · cell 3 [markdown]
- [C20](#c20) · cell 11 [code]
- [C21](#c21) · cell 13 [code]
- [C22](#c22) · cell 14 [code]
- [C23](#c23) · cell 15: Selection in `Series`
- [C24](#c24) · cell 15: Selection in `Series`
- [C27](#c27) · cell 18: A Single Position
- [C29](#c29) · cell 26 [markdown]

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C31](#c31) · `s = pl.Series(["welcome", "to", "data 100"])`
- [C32](#c32) · `s.to_list()`
- [C33](#c33) · `s.name, s.dtype`
- [C34](#c34) · `s = pl.Series("ratings", [-1, 10, 2])`
- [C35](#c35) · `s.name`
- [C36](#c36) · `s = s.cast(pl.Float64)`
- [C37](#c37) · `s.dtype`
- [C38](#c38) · `s = pl.Series([4, -2, 0, 6])`
- [C39](#c39) · `s[[0, 2]]`
- [C40](#c40) · `s > 0`
- [C41](#c41) · `s.filter(s > 0)`

## Changes

<a id="c1"></a>
### C1 · cell 1 [markdown] · mechanical
baseline L23 → branch L23

```diff
- # - Build familiarity with `pandas` and `pandas` syntax.
+ # - Build familiarity with `polars` and `polars` syntax.
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c2"></a>
### C2 · cell 1 [markdown] · mechanical
baseline L56 → branch L56

```diff
- # - `pandas` and `NumPy`
+ # - `polars` and `NumPy`
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c3"></a>
### C3 · cell 1: Understand the World · mechanical

baseline L170 → branch L170

```diff
- # With that, we'll begin by introducing one of the most important tools in exploratory data analysis: `pandas`.
+ # With that, we'll begin by introducing one of the most important tools in exploratory data analysis: `polars`.
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c4"></a>
### C4 · cell 1: Understand the World · mechanical

baseline L174 → branch L174

```diff
- # In this sequence of lectures, we will dive right into things by having you explore and manipulate real-world data. We'll first introduce `pandas`, a popular Python library for interacting with **tabular data**.
+ # In this sequence of lectures, we will dive right into things by having you explore and manipulate real-world data. We'll first introduce `polars`, a popular Python library for interacting with **tabular data**.
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c5"></a>
### C5 · cell 1: Tabular Data and `polars` · mechanical

baseline L176 → branch L176

```diff
- # ## Tabular Data and `pandas`
+ # ## Tabular Data and `polars`
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c6"></a>
### C6 · cell 1: Tabular Data and `polars` · prose · **REVIEW**

baseline L194 → branch L194

```diff
- # In Data 100, we will be working with the programming library `pandas`, which is generally accepted in the data science community as the industry- and academia-standard tool for manipulating tabular data (as well as the inspiration for Petey, our panda bear mascot).
+ # In Data 100, we will be working with the programming library `polars`, which is designed for manipulating tabular data quickly, even when the dataset is large. You will also come across `pandas`, the long-established standard for tabular data in Python and the inspiration for Petey, our panda bear mascot.
```

**Why:** The baseline claim was that `pandas` is the industry- and academia-standard tool — true, and not true of Polars. The sentence was split: Polars gets a claim it can carry (fast on large tabular data), `pandas` keeps the standard-bearer claim and Petey, who is a real course artifact. Naming `pandas` is allowed here because this passage's subject genuinely is the ecosystem. Not in CONTRADICTIONS.md.
**Verdict:** necessary — pandas-specific content that could not survive a rename; a straight swap would have asserted something false about Polars.

<a id="c7"></a>
### C7 · cell 1: Tabular Data and `polars` · mechanical

baseline L196 → branch L196

```diff
- # Using `pandas`, we can
+ # Using `polars`, we can
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c8"></a>
### C8 · cell 1: Tabular Data and `polars` · prose · **REVIEW**

baseline L201 → branch L201

```diff
- # - Apply `NumPy` functions to our data (our friends from Data 8).
+ # - Apply most `NumPy` functions to our data (our friends from Data 8) — though not the
+ #   reductions. `np.mean(s)` raises where `s.mean()` works, because NumPy hands a reduction an
+ #   `axis` argument that Polars does not take. `np.log`, `np.median` and `np.sort` are fine.
```

**Why:** The baseline bullet promised that `NumPy` functions apply to our data. Verified in the d100 env (polars 1.43.1): `np.mean`, `np.sum`, `np.min`, `np.max`, `np.std`, `np.var` and `np.all` all raise `TypeError` on a `pl.Series`, while `np.log`, `np.median` and `np.sort` return fine. The bullet as written would have been false, so it was qualified — but the fix arrives as three lines of dispatch detail in the chapter's opening bullet list, before the reader has met a `Series`.
**Verdict:** questionable — the correction is required; the dose is a judgment call for staff.
**Minimal alternative:** `- Apply most `NumPy` functions to our data (our friends from Data 8) — reductions such as `np.mean` are the exception; use `s.mean()`.` One line, same warning, with the dispatch explanation moved to where reductions first matter.

<a id="c9"></a>
### C9 · cell 1: Tabular Data and `polars` · mechanical

baseline L204 → branch L206

```diff
- # To begin our work in `pandas`, we must first import the library into our Python environment. This will allow us to use `pandas` data structures and methods in our code.
+ # To begin our work in `polars`, we must first import the library into our Python environment. This will allow us to use `polars` data structures and methods in our code.
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c10"></a>
### C10 · cell 2 [code] · code

baseline L207 → branch L209

```diff
- # `pd` is the conventional alias for Pandas, as `np` is for NumPy
- import pandas as pd
+ # `pl` is the conventional alias for Polars, as `np` is for NumPy
+ import polars as pl
```

**Why:** Import swap; `pl` is the course-wide alias, and the comment naming the convention moves with it.
**Output:** same — the cell prints nothing.

<a id="c11"></a>
### C11 · cell 3 [markdown] · prose · **REVIEW**

baseline L211 → branch L213

```diff
- # There are three fundamental data structures in `pandas`:
+ # There are two fundamental data structures in `polars`:
```

**Why:** `Index` is a pandas object; Polars has no row labels, so the count drops from three to two. CONVERSIONS.md records the deliberate decision not to backfill `Expr` as a third, since the chapter never shows one.
**Verdict:** necessary — the third structure does not exist in the library the chapter now teaches.

<a id="c12"></a>
### C12 · cell 3 [markdown] · prose · **REVIEW**

baseline L213 → branch L215

```diff
- # 1. **`Series`**: 1D labeled array data; best thought of as columnar data.
+ # 1. **`Series`**: 1D array data carrying a name and a single data type; best thought of as columnar data.
```

**Why:** "1D labeled array data" describes an index. A Polars `Series` carries a name and a single dtype instead, which is exactly what the cells below now print.
**Verdict:** necessary.

<a id="c13"></a>
### C13 · cell 3 [markdown] · prose · **REVIEW**

baseline L215 → branch L217

```diff
- # 3. **`Index`**: A sequence of row/column labels.
```

**Why:** The `Index` bullet is deleted outright. Verified in the built notebook that the list is renumbered 1–2, so no dangling `3.` ships.
**Verdict:** necessary.

<a id="c14"></a>
### C14 · cell 3 [markdown] · prose · **REVIEW**

baseline L217 → branch L218

```diff
- # `DataFrame`s, `Series`, and Indices can be represented visually in the following diagram, which considers the first few rows of the `elections` dataset.
+ # `DataFrame`s and `Series` can be represented visually in the following diagram, which considers the first few rows of the `elections` dataset. It is drawn with `pandas`, so a few of its labels carry that library's vocabulary.
```

**Why:** `images/df_elections.png` is a pandas render and `content/*/images/**` is gate-protected (hard rule 9), so the figure cannot be redrawn on this branch. The added clause names it as a pandas drawing before the reader reaches it, instead of leaving the caption quietly contradicting the picture — attempt 1 of this chapter was blocked for precisely that. CONVERSIONS.md logs redrawing the image as an open item; when that lands, this clause should go.
**Verdict:** necessary — the alternative is prose describing a figure that shows something else.

<a id="c15"></a>
### C15 · cell 3 [markdown] · prose · **REVIEW**

baseline L220 → branch L221

```diff
- # :alt: Illustration of how a series can be extracted from a dataframe. The index remains the same.
+ # :alt: The first five rows of the elections DataFrame, with its Result column drawn again to the right as a separate Series. A boxed column of the numbers 0 through 4 runs down the left-hand side of each, labeled 'Index of the elections DataFrame' and 'Index of the Result Series'. The Series is headed 'A Series named Result' and ends with the footer 'Name: Result, dtype: object'.
```

**Why:** The baseline alt text asserted "The index remains the same", which is not true of anything on this page under Polars, and described the figure's purpose rather than its contents. Replaced with a literal description, including the index callouts and the `dtype: object` footer that a sighted reader can see.
**Verdict:** necessary — a fix to a claim that was false, in the only version of the figure a screen-reader user gets.

<a id="c16"></a>
### C16 · cell 3 [markdown] · prose · **REVIEW**

baseline L224 → branch L225

```diff
- # Notice how the **DataFrame** is a two-dimensional object — it contains both rows and columns. The **Series** above is a singular column of this `DataFrame`, namely the `Result` column. Both contain an **Index**, or a shared list of row labels (the integers from 0 to 4, inclusive).
+ # Notice how the **DataFrame** is a two-dimensional object — it contains both rows and columns. The **Series** above is a singular column of this `DataFrame`, namely the `Result` column.
+ #
+ # The boxed column of numbers down the left-hand side is what `pandas` calls the **index**. `polars` stores no such column; instead, you reach a row by its **position**, counting from 0, which is how we will select values out of a `Series` shortly. The footer `dtype: object` is likewise the `pandas` name for text data, which `polars` calls `String`.
```

**Why:** Baseline: "Both contain an **Index**, or a shared list of row labels" — false under Polars. The replacement reconciles the two labels the frozen figure shows (the boxed 0–4 column, and `dtype: object`) against what Polars does: position addressing, and `String`. Verified that a `pl.Series` prints neither row numbering nor `object`.
**Verdict:** necessary — a false claim, attached to a figure that cannot be changed. Staff note: this is the book's one paragraph of conversion meta-commentary, which the house style otherwise bars; it exists only because the picture is frozen.

<a id="c17"></a>
### C17 · cell 3: `Series` · prose · **REVIEW**
baseline L232 → branch L235

```diff
- # - A sequence of **values** of the same type.
- # - A sequence of data labels called the **index**.
+ # - A sequence of **values**, all of the same **data type**.
+ # - A **name**, which becomes the column heading when the `Series` is placed in a `DataFrame`.
```

**Why:** The second bullet defined a `Series` as carrying "a sequence of data labels called the **index**", which has no Polars counterpart, and it is the bullet the rest of the section was built on. It is replaced by the property that does that job in Polars — the `Series`' name, which becomes the column heading once it is placed in a `DataFrame` — so the "it contains both" pairing still holds. The first bullet's rewording carries no new claim.
**Verdict:** necessary

<a id="c18"></a>
### C18 · cell 3: `Series` · tab-twins

baseline L235 → branch L238 · spans code and prose

```diff
- # In the cell below, we create a `Series` named `s`.
+ # In the cell below, we create a `Series` and assign it to the variable `s`.
+ 
+ # %% tags=["remove-input", "remove-output"]
+ s = pl.Series(["welcome", "to", "data 100"])
+ s
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin bace57e2 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # s = pl.Series(["welcome", "to", "data 100"])
+ # s
+ # ```
+ #
+ # ```text
+ # shape: (3,)
+ # Series: '' [str]
+ # [
+ # 	"welcome"
+ # 	"to"
+ # 	"data 100"
+ # ]
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # s = pd.Series(["welcome", "to", "data 100"])
+ # s
+ # ```
+ #
+ # ```text
+ # 0     welcome
+ # 1          to
+ # 2    data 100
+ # dtype: object
+ # ```
+ … 3 more lines
```

**Why:** Twin `bace57e2`. Both panes construct the same three-string `Series` — one operation, spelled twice. The Polars pane matches the executed cell verbatim.
**Output:** differs — `shape: (3,)` / `Series: '' [str]` header where pandas printed a 0–2 index column and `dtype: object`. Same three values.

<a id="c19"></a>
### C19 · cell 6 [code] · tab-twins

baseline L238 → branch L283 · spans code and prose

```diff
- s = pd.Series(["welcome", "to", "data 100"])
+ # Accessing data values within the Series
+ s.to_list()
+ 
+ # %% tags=["remove-input", "remove-output"]
+ # Accessing the name and data type of the Series
+ s.name, s.dtype
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 9371d026 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Accessing the name and data type of the Series
+ # s.name, s.dtype
+ # ```
+ #
+ # ```text
+ # ('', String)
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # Accessing the Index of the Series
+ # s.index
+ # ```
+ #
+ # ```text
+ # RangeIndex(start=0, stop=3, step=1)
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
+ 
+ # %% [markdown]
+ # By default, a `Series` built from a list of values is unnamed, and its data type is inferred from the values it holds. Optionally, a name can be passed as the first argument to the constructor.
+ 
+ # %%
+ … 1 more lines
```

**Why:** Twin `9371d026`, and the one to look at hardest. The Polars pane reads `s.name, s.dtype`; the pandas pane reads `s.index`. CONTRADICTIONS §B1 lists that exact pairing (`intro_lec · 53a863ee`) as a false equivalence, and five sibling twins were deleted for it; `conversion/tab_twins_data.py` keeps this one on the ground that both panes carry comments naming what each is reading, so the contrast is disclosed rather than asserted. The twin is a conversion artifact, not pre-existing content, so the judgment call belongs to this branch.
**Output:** differs — `('', String)` against `RangeIndex(start=0, stop=3, step=1)`. The two panes answer different questions, which is both the point and the risk.

<a id="c20"></a>
### C20 · cell 11 [code] · mixed · **REVIEW**

baseline L242 → branch L327 · spans code and prose

```diff
- # Accessing data values within the Series
- s.values
+ s.name
+ 
+ # %% [markdown]
+ # The data type can also be changed after initialization. `.cast()` returns a new `Series`, so we assign the result back to `s`.
```

**Why:** The line diff misaligns here because whole demo cells were replaced, not edited. `s.values` and the index demos after it have no Polars counterpart, so the section was re-aimed at the two things a Polars `Series` carries — its name and its dtype — and the new sentence introduces `.cast()` returning a new object, the first place in the course that habit appears.
**Verdict:** necessary — `.values` and the index demos are pandas-specific. The added `.cast()` sentence is the one optional part; CONVERSIONS.md records the prose reviewer asking for it.

<a id="c21"></a>
### C21 · cell 13 [code] · mixed · **REVIEW**

baseline L246 → branch L333 · spans code and prose

```diff
- # Accessing the Index of the Series
- s.index
- 
- # %% [markdown]
- # By default, the `index` of a `Series` is a sequential list of integers beginning from 0. Optionally, a manually specified list of desired indices can be passed to the `index` argument.
- 
- # %%
- s = pd.Series([-1, 10, 2], index = ["a", "b", "c"])
+ s = s.cast(pl.Float64)
```

**Why:** `pd.Series([-1,10,2], index=["a","b","c"])` and the paragraph about supplying your own index have no analogue. The cell was re-aimed at `s.cast(pl.Float64)`, keeping the section's "you can change this after construction" shape while changing what is changed.
**Verdict:** necessary.

<a id="c22"></a>
### C22 · cell 14 [code] · mixed · **REVIEW**

baseline L257 → branch L337 · spans code and prose

```diff
- s.index
- 
- # %% [markdown]
- # Indices can also be changed after initialization.
- 
- # %%
- s.index = ["first", "second", "third"]
- s
- 
- # %%
- s.index
+ s.dtype
```

**Why:** `s.index = [...]` mutates in place; Polars `Series` are immutable, so both the assignment and the paragraph above it go. Replaced by `s.dtype`, which reads back what the previous cell changed.
**Verdict:** necessary.

<a id="c23"></a>
### C23 · cell 15: Selection in `Series` · prose · **REVIEW**

baseline L272 → branch L342

```diff
- # Much like when working with `NumPy` arrays, we can select a single value or a set of values from a `Series`. To do so, there are three primary methods:
+ # Much like when working with `NumPy` arrays, we can select a single value or a set of values from a `Series`. Elements are addressed by their **position** in the sequence, counting from 0. There are three primary methods:
```

**Why:** Selection by label does not exist, so the sentence that introduced three label-based methods gains the fact that replaces it: elements are addressed by position, counting from 0.
**Verdict:** necessary.

<a id="c24"></a>
### C24 · cell 15: Selection in `Series` · prose · **REVIEW**

baseline L274 → branch L344

```diff
- # 1. A single label.
- # 2. A list of labels.
+ # 1. A single position.
+ # 2. A list of positions.
```

**Why:** Two of the three listed selection methods were labels.
**Verdict:** necessary.

<a id="c25"></a>
### C25 · cell 16 [code] · code

baseline L280 → branch L350

```diff
- # %%
- s = pd.Series([4, -2, 0, 6], index = ["a", "b", "c", "d"])
+ # %% tags=["remove-input", "remove-output"]
+ s = pl.Series([4, -2, 0, 6])
```

**Why:** `pd.Series([...], index=["a","b","c","d"])` → `pl.Series([...])`, and the cell gains `remove-input`/`remove-output` so the tab-set below carries the display.
**Output:** differs — the printed `Series` has no label column. Values unchanged.

<a id="c26"></a>
### C26 · cell 17 [markdown] · tab-twins

baseline L285 → branch L355 · spans code and prose

```diff
- # ##### A Single Label
- 
- # %%
- # We return the value stored at the index label "a"
- s["a"]
+ # <!-- tab-twins:begin 168aebad -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # s = pl.Series([4, -2, 0, 6])
+ # s
+ # ```
+ #
+ # ```text
+ # shape: (4,)
+ # Series: '' [i64]
+ # [
+ # 	4
+ # 	-2
+ # 	0
+ # 	6
+ # ]
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # s = pd.Series([4, -2, 0, 6], index = ["a", "b", "c", "d"])
+ # s
+ # ```
+ #
+ # ```text
+ # a    4
+ # b   -2
+ # c    0
+ # d    6
+ # dtype: int64
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** Twin `168aebad`. Both panes build the same four integers; the pandas pane keeps its `index=` argument because the label-selection panes below depend on it. Staff note: this is the same naming-vs-labelling shape that got twin `fba44498` deleted under §B1, and it survives here only because the panes underneath need those labels to demonstrate anything.
**Output:** differs — Polars prints `shape: (4,)` and no labels; pandas prints `a`–`d`. Same four values.

<a id="c27"></a>
### C27 · cell 18: A Single Position · prose · **REVIEW**

baseline L292 → branch L395

```diff
- # ##### A List of Labels
+ # ##### A Single Position
```

**Why:** Section headings follow the selection rewrite: `A Single Label` / `A List of Labels` become `A Single Position` / `A List of Positions`. The diff reads as a straight rename only because the two headings shifted past one another.
**Verdict:** necessary.

<a id="c28"></a>
### C28 · cell 19 [code] · tab-twins

baseline L294 → branch L397 · spans code and prose

```diff
- # %%
- # We return a Series of the values stored at the index labels "a" and "c"
- s[["a", "c"]]
+ # %% tags=["remove-input", "remove-output"]
+ # We return the value stored at position 0
+ s[0]
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 120afc0f -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # We return the value stored at position 0
+ # s[0]
+ # ```
+ #
+ # ```text
+ # 4
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # We return the value stored at the index label "a"
+ # s["a"]
+ # ```
+ #
+ # ```text
+ # 4
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
+ 
+ # %% [markdown]
+ # ##### A List of Positions
+ 
+ # %% tags=["remove-input", "remove-output"]
+ # We return a Series of the values stored at positions 0 and 2
+ s[[0, 2]]
+ 
+ … 35 more lines
```

**Why:** Twins `120afc0f` and `641029d4` (the second is inside the truncated tail). `s[0]` against `s["a"]`, and `s[[0, 2]]` against `s[["a", "c"]]` — position against label, which is the honest pairing for this section. Verified that a list of integers gathers positions on the pin.
**Output:** differs — `4` on both panes for the scalar form; the list form gives an unlabelled two-element `Series` against a labelled one. Same values.

<a id="c29"></a>
### C29 · cell 26 [markdown] · prose · **REVIEW**

baseline L310 → branch L485

```diff
- # We then use this boolean condition to index into our original `Series`. `pandas` will select only the entries in the original `Series` that satisfy the condition.
+ # We then pass this boolean condition to the `.filter()` method of our original `Series`. `polars` will keep only the entries that satisfy the condition.
```

**Why:** Load-bearing: `s[s > 0]` raises `TypeError: selecting rows by passing a boolean mask to __getitem__ is not supported`, so `.filter()` is the only available form, not a style preference. The sentence moves from "index into" to "pass to the `.filter()` method" to match.
**Verdict:** necessary.

<a id="c30"></a>
### C30 · cell 27 [code] · tab-twins

baseline L312 → branch L487 · spans code and prose

```diff
- # %%
- s[s > 0]
+ # %% tags=["remove-input", "remove-output"]
+ s.filter(s > 0)
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin a53e4de1 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # s.filter(s > 0)
+ # ```
+ #
+ # ```text
+ # shape: (2,)
+ # Series: '' [i64]
+ # [
+ # 	4
+ # 	6
+ # ]
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # s[s > 0]
+ # ```
+ #
+ # ```text
+ # a    4
+ # d    6
+ # dtype: int64
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** Twin `a53e4de1`. One operation on both panes; the spelling is the whole difference.
**Output:** differs — two unlabelled values against `a 4 / d 6`. Same values.

<a id="c31"></a>
### C31 · `s = pl.Series(["welcome", "to", "data 100"])` · output

committed output

```diff
- [text] 0     welcome
- [text] 1          to
- [text] 2    data 100
- [text] dtype: object
+ [text] shape: (3,)
+ [text] Series: '' [str]
+ [text] [
+ [text] 	"welcome"
+ [text] 	"to"
+ [text] 	"data 100"
+ [text] ]
```

**Why:** Re-executed under Polars; the `Series` repr replaces the pandas one.
**Reader sees:** equivalent — the same three strings.

<a id="c32"></a>
### C32 · `s.to_list()` · output

committed output

```diff
- [text] array(['welcome', 'to', 'data 100'], dtype=object)
+ [text] ['welcome', 'to', 'data 100']
```

**Why:** The cell changed operation, not just spelling: `s.values` (an `ndarray`) became `s.to_list()` (a `list`). §B1 records the `.values ≡ .to_list()` twin (`3117fc63`) being deleted as a false equivalence; the honest pandas analogue is `.tolist()`.
**Reader sees:** changed: the output is a Python list where the baseline showed `array([...], dtype=object)`. Same values, different object.

<a id="c33"></a>
### C33 · `s.name, s.dtype` · output

committed output

```diff
- [text] RangeIndex(start=0, stop=3, step=1)
+ [text] ('', String)
```

**Why:** The cell was re-aimed from `s.index` to `s.name, s.dtype` (see C20–C22).
**Reader sees:** changed: the reader is now shown what the `Series` is called and what type it holds, instead of its row labels.

<a id="c34"></a>
### C34 · `s = pl.Series("ratings", [-1, 10, 2])` · output

committed output

```diff
- [text] a    -1
- [text] b    10
- [text] c     2
- [text] dtype: int64
+ [text] shape: (3,)
+ [text] Series: 'ratings' [i64]
+ [text] [
+ [text] 	-1
+ [text] 	10
+ [text] 	2
+ [text] ]
```

**Why:** `pd.Series([-1,10,2], index=["a","b","c"])` → `pl.Series("ratings", [-1,10,2])`: the optional first positional argument is the name, which is the real counterpart of pandas' optional `index=`.
**Reader sees:** changed: the output demonstrates naming a `Series` rather than labelling its rows.

<a id="c35"></a>
### C35 · `s.name` · output

committed output

```diff
- [text] Index(['a', 'b', 'c'], dtype='object')
+ [text] 'ratings'
```

**Why:** Follows C34 — the cell reads back the property just set.
**Reader sees:** changed: `'ratings'` where the baseline printed the label `Index`.

<a id="c36"></a>
### C36 · `s = s.cast(pl.Float64)` · output

committed output

```diff
- [text] first     -1
- [text] second    10
- [text] third      2
- [text] dtype: int64
+ [text] shape: (3,)
+ [text] Series: 'ratings' [f64]
+ [text] [
+ [text] 	-1.0
+ [text] 	10.0
+ [text] 	2.0
+ [text] ]
```

**Why:** `s.cast(pl.Float64)` replaces `s.index = [...]`, and the result is reassigned because Polars returns a new `Series`.
**Reader sees:** changed: the values print as floats under an `[f64]` header. The baseline output relabelled the rows and left `dtype: int64`, which did not demonstrate what its own prose claimed.

<a id="c37"></a>
### C37 · `s.dtype` · output

committed output

```diff
- [text] Index(['first', 'second', 'third'], dtype='object')
+ [text] Float64
```

**Why:** Reads back the dtype set in C36.
**Reader sees:** changed: `Float64` where the baseline printed the new labels.

<a id="c38"></a>
### C38 · `s = pl.Series([4, -2, 0, 6])` · output

committed output

```diff
- [text] a    4
- [text] b   -2
- [text] c    0
- [text] d    6
- [text] dtype: int64
+ [text] shape: (4,)
+ [text] Series: '' [i64]
+ [text] [
+ [text] 	4
+ [text] 	-2
+ [text] 	0
+ [text] 	6
+ [text] ]
```

**Why:** Constructor without `index=`.
**Reader sees:** equivalent — the same four integers, addressed by position.

<a id="c39"></a>
### C39 · `s[[0, 2]]` · output

committed output

```diff
- [text] a    4
- [text] c    0
- [text] dtype: int64
+ [text] shape: (2,)
+ [text] Series: '' [i64]
+ [text] [
+ [text] 	4
+ [text] 	0
+ [text] ]
```

**Why:** `s[["a","c"]]` → `s[[0, 2]]`; verified on the pin that a list of integers gathers positions.
**Reader sees:** equivalent — the same two values, 4 and 0.

<a id="c40"></a>
### C40 · `s > 0` · output

committed output

```diff
- [text] a     True
- [text] b    False
- [text] c    False
- [text] d     True
- [text] dtype: bool
+ [text] shape: (4,)
+ [text] Series: '' [bool]
+ [text] [
+ [text] 	true
+ [text] 	false
+ [text] 	false
+ [text] 	true
+ [text] ]
```

**Why:** Comparison on the unlabelled `Series`.
**Reader sees:** equivalent — the same four booleans; Polars prints them lowercase.

<a id="c41"></a>
### C41 · `s.filter(s > 0)` · output

committed output

```diff
- [text] a    4
- [text] d    6
- [text] dtype: int64
+ [text] shape: (2,)
+ [text] Series: '' [i64]
+ [text] [
+ [text] 	4
+ [text] 	6
+ [text] ]
```

**Why:** `s[s > 0]` raises under Polars (see C29), so the cell is `s.filter(s > 0)`.
**Reader sees:** equivalent — the same two values.

