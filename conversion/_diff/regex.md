# regex — change report

`887a578b0a4b:content/regex/regex.ipynb` → `content/regex/regex.ipynb`

**Tier B · 43 changes:** output 8 · prose 8 · dropdown 3 · tab-twins 4 · code 9 · mechanical 7 · metadata 4

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

A near-mechanical library swap plus one genuinely restructured section: the `extract` / `extractall` passage was rebuilt around Polars' struct and list columns, because a MultiIndexed result has no counterpart. Three things to look at: C20, a pre-existing factual error in the quantifier reference table (§A12 #1) that this branch fixes and course staff own; C5/C6/C15/C24, where `replace_all`'s and `contains`' regex-by-default behaviour is now taught explicitly (§A12 #2, also pre-existing); and C43, where the committed output loses the second SSN on row 2 because the cell moved from all-matches to first-match. Verified in the d100 env: the canonicalised county values are unchanged, and both replacement strings in the quantifier table are genuinely non-matching.

## Needs review

- [C4](#c4) · cell 2: Python String Methods
- [C5](#c5) · cell 2: Python String Methods
- [C6](#c6) · cell 2: Python String Methods
- [C7](#c7) · cell 2: Python String Methods
- [C15](#c15) · cell 7: Canonicalization with Polars Series Methods
- [C20](#c20) · cell 16: Convenient RegEx
- [C24](#c24) · cell 20: Canonicalization with `polars`
- [C29](#c29) · cell 27: Extraction with `polars`

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C36](#c36) · `display(county_and_state), display(county_and_pop);`
- [C37](#c37) · `def canonicalize_county_series(county_series):`
- [C38](#c38) · `html_data`
- [C39](#c39) · `pattern = r"<[^>]+>"`
- [C40](#c40) · `ssn_data`
- [C41](#c41) · `ssn_data["SSN"].str.extract_all(pattern)`
- [C42](#c42) · `pattern_cg = r"(?<area>[0-9]{3})-(?<group>[0-9]{2})-(?<serial>[0-9]{4}`
- [C43](#c43) · `ssn_data["SSN"].str.extract_groups(pattern_cg).struct.unnest()`

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C8](#c8) · cell 2: Canonicalization
- [C9](#c9) · cell 2: Canonicalization
- [C10](#c10) · cell 2: Canonicalization

## Changes

<a id="c1"></a>
### C1 · cell 1 [markdown] · prose · **REVIEW**
baseline L21 → branch L21

```diff
- # - Understand Python string manipulation, `pandas` `Series` methods
+ # - Understand Python string manipulation, `polars` `Series` string methods
```

**Why:** A learning outcome that told students to learn `pandas` `Series` methods, above a chapter that now teaches Polars' `.str` namespace, so the library name could not stay. The added word "string" narrows the promise to what the chapter actually covers — Polars keeps its string operations in `.str` rather than on `Series` generally.
**Verdict:** necessary

<a id="c2"></a>
### C2 · cell 2: Python String Methods · mechanical

baseline L41 → branch L41

```diff
- # First, we'll introduce a few methods useful for string manipulation. The following table includes a number of string operations supported by Python and `pandas`. The Python functions operate on a single string, while their equivalent in `pandas` are  **vectorized** — they operate on a `Series` of string data.
+ # First, we'll introduce a few methods useful for string manipulation. The following table includes a number of string operations supported by Python and `polars`. The Python functions operate on a single string, while their equivalent in `polars` are  **vectorized** — they operate on a `Series` of string data.
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c3"></a>
### C3 · cell 2: Python String Methods · mechanical

baseline L43 → branch L43

```diff
- # | Operation | Python | `Pandas` (`Series`) |
+ # | Operation | Python | `Polars` (`Series`) |
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c4"></a>
### C4 · cell 2: Python String Methods · prose · **REVIEW**

baseline L45 → branch L45

```diff
- # | Transformation | - `s.lower()` <br> - `s.upper()` | - `ser.str.lower()` <br> - `ser.str.upper()` |
- # | Replacement + Deletion | `s.replace(_)` | `ser.str.replace(_)` |
+ # | Transformation | - `s.lower()` <br> - `s.upper()` | - `ser.str.to_lowercase()` <br> - `ser.str.to_uppercase()` |
+ # | Replacement + Deletion | `s.replace(_)` | `ser.str.replace_all(_)` |
```

**Why:** Method-name rows in the Python↔library mapping table. `.str.lower` and `.str.replace` do not exist in Polars under those names, and Polars' `.str.replace` replaces only the **first** match where pandas' replaced all — so `replace_all` is the honest partner for `s.replace(_)`.
**Verdict:** necessary.

<a id="c5"></a>
### C5 · cell 2: Python String Methods · prose · **REVIEW**

baseline L48 → branch L48

```diff
- # | Substring | `s[1:4]` | `ser.str[1:4]` |
- # | Membership | `'_' in s` | `ser.str.contains(_)` |
- # | Length | `len(s)` | `ser.str.len()` |
+ # | Substring | `s[1:4]` | `ser.str.slice(1, 3)` |
+ # | Membership | `'_' in s` | `ser.str.contains(_)` (regex by default — pass `literal=True` for a plain substring) |
+ # | Length | `len(s)` | `ser.str.len_chars()` |
```

**Why:** Three rows. `ser.str[1:4]` → `.str.slice(1, 3)`, because the second argument is a length, not a stop — verified, both give `bcd` from `abcdef`. `len()` → `len_chars()`. The `contains` row gains a regex caveat: §A12 #2 records that the pairing `'_' in s` ↔ `ser.str.contains(_)` is right as an operation but silently wrong about semantics, verified — `pl.Series(["cowscom"]).str.contains("cow.com")` is `True`, and `literal=True` makes it `False`. That table row is **pre-existing course content**, and the pandas method is regex-by-default too, so the claim was equally wrong before the conversion.
**Verdict:** necessary — one rename the library forces, and one fix to a claim that was false (§A12 #2, pre-existing).

<a id="c6"></a>
### C6 · cell 2: Python String Methods · prose · **REVIEW**

baseline L52 → branch L52

```diff
- # Note that the `.str` method is also an accessor, similar to the `.dt` accessor we discussed in lecture on [Data Cleaning and EDA](https://ds100.org/course-notes/eda/#temporality-with-pandas-dt-accessors).
+ # Two of these deserve a second look. `ser.str.slice` takes a **start and a length**, not a start
+ # and a stop — `s[1:4]` and `ser.str.slice(1, 3)` both give you three characters beginning at
+ # index 1. And `ser.str.replace_all` treats its pattern as a *regular expression* by default,
+ # which is convenient in this note and a trap everywhere else; pass `literal=True` when you mean
+ # the characters themselves.
```

**Why:** Replaces the `.str`-accessor cross-reference sentence (which moves to C7) with the two behaviours the table cannot express in a cell: `slice` takes a length, and `replace_all` reads its pattern as a regex. Both verified on the pin, and both are on topic in a chapter about regular expressions.
**Verdict:** necessary — the `slice` row of the table is unusable without it.

<a id="c7"></a>
### C7 · cell 2: Python String Methods · prose · **REVIEW**

baseline L54 → branch L58

```diff
- # We'll discuss the differences between Python string functions and `pandas` `Series` methods in the following section on canonicalization.
+ # Note that `.str` is a **namespace**, similar to the `.dt` namespace we discussed in lecture on [Data Cleaning and EDA](https://ds100.org/course-notes/eda/#temporality-with-the-polars-dt-namespace). Polars groups methods that only apply to one kind of column this way, so string methods live under `.str` and datetime methods under `.dt`.
+ #
+ # We'll discuss the differences between Python string functions and `polars` `Series` methods in the following section on canonicalization.
```

**Why:** Keeps the `eda` cross-reference, re-pointed at the converted anchor, and calls `.str` a namespace rather than an accessor, matching Polars' own vocabulary. Verified: `content/eda` now heads that section "Temporality with the `polars` `dt` namespace", so `#temporality-with-the-polars-dt-namespace` resolves. This discharges CONVERSIONS.md open question 8, which flagged the link as breakable by no gate in the harness.
**Verdict:** necessary — an un-repointed absolute URL is a dead link, which the `doc-links` gate treats the same as an unconverted one.

<a id="c8"></a>
### C8 · cell 2: Canonicalization · dropdown

baseline L62 → branch L68 · mirror of the next code cell (hard rule 3)

```diff
- # import pandas as pd
+ # import polars as pl
```

**Why:** Mirror of the setup cell; hard rule 3 means it moves in the same pass. Verified: the dropdown's `python` block matches the following code cell verbatim.
**Output:** same — a mirror carries no output.

<a id="c9"></a>
### C9 · cell 2: Canonicalization · dropdown

baseline L65 → branch L71 · mirror of the next code cell (hard rule 3)

```diff
- #     county_and_state = pd.read_csv(f)
+ #     county_and_state = pl.read_csv(f)
```

**Why:** Same mirror, the first `read_csv`. Verified identical to the code cell it mirrors.
**Output:** same — a mirror carries no output.

<a id="c10"></a>
### C10 · cell 2: Canonicalization · dropdown

baseline L68 → branch L74 · mirror of the next code cell (hard rule 3)

```diff
- #     county_and_pop = pd.read_csv(f)
+ #     county_and_pop = pl.read_csv(f)
```

**Why:** Same mirror, the second `read_csv`. Verified identical to the code cell it mirrors.
**Output:** same — a mirror carries no output.

<a id="c11"></a>
### C11 · cell 3 [code] · code

baseline L73 → branch L79

```diff
- import pandas as pd
+ import polars as pl
```

**Why:** Import swap.
**Output:** same — the cell prints nothing of its own.

<a id="c12"></a>
### C12 · cell 3 [code] · code

baseline L76 → branch L82

```diff
-     county_and_state = pd.read_csv(f)
+     county_and_state = pl.read_csv(f)
```

**Why:** `pl.read_csv` accepts the open file handle directly, so the `with open(...)` block stays — worth keeping in a chapter whose subject is text handling.
**Output:** differs — repr only (see C36); the same four rows and two columns.

<a id="c13"></a>
### C13 · cell 3 [code] · code

baseline L79 → branch L85

```diff
-     county_and_pop = pd.read_csv(f)
+     county_and_pop = pl.read_csv(f)
```

**Why:** Second file, same swap.
**Output:** differs — repr only; the same four rows and two columns.

<a id="c14"></a>
### C14 · cell 7: Canonicalization with Polars Series Methods · mechanical

baseline L108 → branch L114

```diff
- # #### Canonicalization with Pandas Series Methods
+ # #### Canonicalization with Polars Series Methods
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c15"></a>
### C15 · cell 7: Canonicalization with Polars Series Methods · prose · **REVIEW**

baseline L110 → branch L116

```diff
- # Alternatively, we can use `pandas` `Series` methods to create this standardized column. To do so, we must call the `.str` attribute of our `Series` object prior to calling any methods, like `.lower` and `.replace`. Notice how these method names match their equivalent built-in Python string functions.
+ # Alternatively, we can use `polars` `Series` methods to create this standardized column. To do so, we reach through the `.str` namespace of our `Series` object before calling any method, like `.to_lowercase` and `.replace_all`. The names are more explicit than their built-in Python counterparts: `replace_all` says that every match is replaced, not just the first.
+ #
+ # One argument is doing quiet work below. `replace_all` reads its pattern as a regular expression, so `.str.replace_all('.', '')` would match *every* character and return empty strings. Passing `literal=True` asks for the characters themselves, which is what canonicalization wants here.
```

**Why:** The baseline paragraph's point was that the library's method names match Python's built-ins. Under Polars they do not (`to_lowercase`, `replace_all`), so the paragraph makes the opposite and more useful point, and the added sentence explains the `literal=True` that now appears five times in the cell below. Verified: `.str.replace_all('.', '')` without it returns empty strings for every row.
**Verdict:** necessary — the original claim is false under Polars, and the new argument is load-bearing in the code the paragraph introduces.

<a id="c16"></a>
### C16 · cell 8 [code] · metadata

baseline L114 → branch L122

```diff
- # %%
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c17"></a>
### C17 · cell 8 [code] · code

baseline L118 → branch L126

```diff
-             .str.lower()
-             .str.replace(' ', '')
-             .str.replace('&', 'and')
-             .str.replace('.', '')
-             .str.replace('county', '')
-             .str.replace('parish', '')
+             .str.to_lowercase()
+             .str.replace_all(' ', '', literal=True)
+             .str.replace_all('&', 'and', literal=True)
+             .str.replace_all('.', '', literal=True)
+             .str.replace_all('county', '', literal=True)
+             .str.replace_all('parish', '', literal=True)
```

**Why:** `.str.lower` → `.str.to_lowercase`, and five `.str.replace` → `.str.replace_all(..., literal=True)`. Both halves matter: Polars' `replace` does the first match only, and an unescaped `'.'` read as a regex deletes every character.
**Output:** same — the canonicalised values are identical to the baseline (`dewitt`, `lacquiparle`, `lewisandclark`, `stjohnthebaptist`).

<a id="c18"></a>
### C18 · cell 8 [code] · code

baseline L126 → branch L134

```diff
- county_and_pop['clean_county_pandas'] = canonicalize_county_series(county_and_pop['County'])
- county_and_state['clean_county_pandas'] = canonicalize_county_series(county_and_state['County'])
+ county_and_pop = county_and_pop.with_columns(
+     canonicalize_county_series(county_and_pop['County']).alias('clean_county_polars')
+ )
+ county_and_state = county_and_state.with_columns(
+     canonicalize_county_series(county_and_state['County']).alias('clean_county_polars')
+ )
```

**Why:** `df['new'] = ...` has no Polars form; `with_columns` plus an explicit `.alias` replaces it, and the column is named `clean_county_polars` rather than leaving a pandas label on a Polars column.
**Output:** differs — the added column's name. No prose names it (grepped); the only surviving `clean_county_pandas` strings in the chapter are inside the pandas pane of the tab twin, where they belong.

<a id="c19"></a>
### C19 · cell 8 [code] · tab-twins

baseline L129 → branch L141 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 533afe7f -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # def canonicalize_county_series(county_series):
+ #     return (
+ #         county_series
+ #             .str.to_lowercase()
+ #             .str.replace_all(' ', '', literal=True)
+ #             .str.replace_all('&', 'and', literal=True)
+ #             .str.replace_all('.', '', literal=True)
+ #             .str.replace_all('county', '', literal=True)
+ #             .str.replace_all('parish', '', literal=True)
+ #     )
+ #
+ # county_and_pop = county_and_pop.with_columns(
+ #     canonicalize_county_series(county_and_pop['County']).alias('clean_county_polars')
+ # )
+ # county_and_state = county_and_state.with_columns(
+ #     canonicalize_county_series(county_and_state['County']).alias('clean_county_polars')
+ # )
+ # display(county_and_pop), display(county_and_state);
+ # ```
+ #
+ # ```text
+ # shape: (4, 3)
+ # ┌──────────────────────┬────────────┬─────────────────────┐
+ # │ County               ┆ Population ┆ clean_county_polars │
+ # │ ---                  ┆ ---        ┆ ---                 │
+ # │ str                  ┆ i64        ┆ str                 │
+ # ╞══════════════════════╪════════════╪═════════════════════╡
+ # │ DeWitt               ┆ 16798      ┆ dewitt              │
+ # │ Lac Qui Parle        ┆ 8067       ┆ lacquiparle         │
+ # │ Lewis & Clark        ┆ 55716      ┆ lewisandclark       │
+ # │ St. John the Baptist ┆ 43044      ┆ stjohnthebaptist    │
+ # └──────────────────────┴────────────┴─────────────────────┘
+ # shape: (4, 3)
+ … 47 more lines
```

**Why:** Twin `533afe7f`. Both panes canonicalise the same two frames. §B2 #4 records that this pane once showed only the first of the two frames a `display(); display()` cell renders, which broke the section's argument that two differently-spelled county columns canonicalise to the same value; the committed pane now carries both.
**Output:** differs — repr and the column name; the canonicalised values match on both tabs, which is what the section argues.

<a id="c20"></a>
### C20 · cell 16: Convenient RegEx · prose · **REVIEW**

baseline L284 → branch L383

```diff
- # | `lazy version of zero or more`: `*?` | `5.*?5` | `5005`<br />`55` | `5005005` |
+ # | `lazy version of zero or more`: `*?` | `5.*?5` | `5005`<br />`55` | `500`<br />`005` |
```

**Why:** §A12 #1, **pre-existing course content** — present verbatim in the baseline, so the fix belongs to course staff and arguably to `main`. Verified: `re.fullmatch(r"5.*?5", "5005005")` matches, because backtracking lets a lazy quantifier expand to satisfy an anchor-free full match — lazy and greedy differ in *which* match, not whether there is one. Replaced with `500` and `005`, both verified non-matching under `fullmatch` and `search`.
**Verdict:** necessary — a fix to a claim that was false; the only wrong row in three otherwise correct tables.

<a id="c21"></a>
### C21 · cell 18: Regex in Python and Polars (RegEx Groups) · mechanical

baseline L334 → branch L433

```diff
- # ## Regex in Python and Pandas (RegEx Groups)
+ # ## Regex in Python and Polars (RegEx Groups)
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c22"></a>
### C22 · cell 18: Canonicalization with RegEx · mechanical

baseline L340 → branch L439

```diff
- # Earlier in this note, we examined the process of canonicalization using `python` string manipulation and `pandas` `Series` methods. However, we mentioned this approach had a major flaw: our code was unnecessarily verbose. Equipped with our knowledge of regular expressions, let's fix this.
+ # Earlier in this note, we examined the process of canonicalization using `python` string manipulation and `polars` `Series` methods. However, we mentioned this approach had a major flaw: our code was unnecessarily verbose. Equipped with our knowledge of regular expressions, let's fix this.
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c23"></a>
### C23 · cell 20: Canonicalization with `polars` · mechanical

baseline L365 → branch L464

```diff
- # #### Canonicalization with `pandas`
+ # #### Canonicalization with `polars`
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c24"></a>
### C24 · cell 20: Canonicalization with `polars` · prose · **REVIEW**

baseline L367 → branch L466

```diff
- # We can also use regular expressions with `pandas` `Series` methods. This gives us the benefit of operating on an entire column of data as opposed to a single value. The code is simple: <br /> `ser.str.replace(pattern, repl, regex=True`).
+ # We can also use regular expressions with `polars` `Series` methods. This gives us the benefit of operating on an entire column of data as opposed to a single value. The code is simple: <br /> `ser.str.replace_all(pattern, repl)`.
+ #
+ # This is the same method we used for plain text above, without `literal=True`. That is the default we warned about earlier, and here it is exactly what we want.
```

**Why:** `regex=True` does not exist in Polars — regex is the default — so the keyword disappears rather than being translated. The second sentence ties that default back to the `literal=True` warning earlier in the chapter; that half is the optional part of the edit.
**Verdict:** necessary — the API differs, and the sentence quotes the call signature.

<a id="c25"></a>
### C25 · cell 21 [code] · code

baseline L375 → branch L476

```diff
- html_data = pd.DataFrame(data)
+ html_data = pl.DataFrame(data)
```

**Why:** `pd.DataFrame(data)` → `pl.DataFrame(data)`.
**Output:** differs — repr only, and Polars truncates the long HTML strings at the column width (see C38).

<a id="c26"></a>
### C26 · cell 23 [code] · metadata

baseline L380 → branch L481

```diff
- # %%
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c27"></a>
### C27 · cell 23 [code] · tab-twins

baseline L382 → branch L483 · spans code and prose

```diff
- html_data['HTML'].str.replace(pattern, '', regex=True)
+ html_data['HTML'].str.replace_all(pattern, '')
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 16323c05 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # pattern = r"<[^>]+>"
+ # html_data['HTML'].str.replace_all(pattern, '')
+ # ```
+ #
+ # ```text
+ # shape: (3,)
+ # Series: 'HTML' [str]
+ # [
+ # 	"Moo"
+ # 	"Link"
+ # 	"Bold text"
+ # ]
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # pattern = r"<[^>]+>"
+ # html_data['HTML'].str.replace(pattern, '', regex=True)
+ # ```
+ #
+ # ```text
+ # 0          Moo
+ # 1         Link
+ # 2    Bold text
+ # Name: HTML, dtype: object
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** Twin `16323c05`. One operation on both panes: strip tags with the same pattern.
**Output:** differs — repr only; the same three stripped strings.

<a id="c28"></a>
### C28 · cell 27: Extraction with `polars` · mechanical

baseline L399 → branch L538

```diff
- # #### Extraction with `pandas`
+ # #### Extraction with `polars`
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c29"></a>
### C29 · cell 27: Extraction with `polars` · prose · **REVIEW**

baseline L401 → branch L540

```diff
- # `pandas` similarily provides extraction functionality on a `Series` of data: `ser.str.findall(pattern)`
+ # `polars` similarily provides extraction functionality on a `Series` of data: `ser.str.extract_all(pattern)`
```

**Why:** `findall` → `extract_all`; the sentence names the method, so it moves with the code.
**Verdict:** necessary.

<a id="c30"></a>
### C30 · cell 28 [code] · code

baseline L409 → branch L548

```diff
- ssn_data = pd.DataFrame(data)
+ ssn_data = pl.DataFrame(data)
```

**Why:** `pd.DataFrame(data)` → `pl.DataFrame(data)`.
**Output:** differs — repr only (see C40).

<a id="c31"></a>
### C31 · cell 30 [code] · code

baseline L414 → branch L553

```diff
- # %%
- ssn_data["SSN"].str.findall(pattern)
+ # %% tags=["remove-input", "remove-output"]
+ ssn_data["SSN"].str.extract_all(pattern)
```

**Why:** `.str.findall` → `.str.extract_all`, and the cell gains `remove-input`/`remove-output` so the tab-set below carries the display.
**Output:** differs — the result is a `list[str]` column rather than an object column of Python lists. The same four lists, including the empty one for `"forty"`.

<a id="c32"></a>
### C32 · cell 31 [markdown] · tab-twins

baseline L418 → branch L557

```diff
- # This function returns a list for every row containing the pattern matches in a given string.
+ # <!-- tab-twins:begin cb4897da -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # ssn_data["SSN"].str.extract_all(pattern)
+ # ```
```

**Why:** Twin `cb4897da`, the `extract_all` pair. Both panes return one list per row, including the empty list for `"forty"`.
**Output:** differs — repr, and the visible `list[str]` dtype, which the new prose names.

<a id="c33"></a>
### C33 · cell 31 [markdown] · tab-twins

baseline L420 → branch L565 · spans code and prose

```diff
- # As you may expect, there are similar `pandas` equivalents for other `re` functions as well. `Series.str.extract` takes in a pattern and returns a `DataFrame` of each capture group’s first match in the string. In contrast, `Series.str.extractall` returns a multi-indexed `DataFrame` of all matches for each capture group. You can see the difference in the outputs below:
+ # ```text
+ # shape: (4,)
+ # Series: 'SSN' [list[str]]
+ # [
+ # 	["987-65-4321"]
+ # 	[]
+ # 	["123-45-6789", "321-45-6789"]
+ # 	["999-99-9999"]
+ # ]
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # ssn_data["SSN"].str.findall(pattern)
+ # ```
+ #
+ # ```text
+ # 0                 [987-65-4321]
+ # 1                            []
+ # 2    [123-45-6789, 321-45-6789]
+ # 3                 [999-99-9999]
+ # Name: SSN, dtype: object
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
+ 
+ # %% [markdown]
+ # Notice the column type: `list[str]`. Every row holds a *list* of the matches found in that string, so the row for `"forty"` is an empty list rather than a missing value.
+ #
+ # As you may expect, there are similar `polars` equivalents for other `re` functions as well. `Series.str.extract_groups` takes a pattern and returns a **struct** — one field per capture group, holding that group's first match. Naming the groups in the pattern names the fields, and `.struct.unnest()` spreads them into columns. You can see the difference in the outputs below:
+ 
+ # %% tags=["remove-input", "remove-output"]
+ pattern_cg = r"(?<area>[0-9]{3})-(?<group>[0-9]{2})-(?<serial>[0-9]{4})"
+ ssn_data["SSN"].str.extract_groups(pattern_cg)
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 188458d4 -->
+ … 37 more lines
```

**Why:** The restructured passage. The baseline taught `extract` (first match per group, a `DataFrame`) against `extractall` (every match, a MultiIndexed `DataFrame`); Polars has no MultiIndex, so the contrast was re-aimed at the two structures it does return — a struct column, and the columns `.struct.unnest()` spreads it into. Consequence worth naming: this passage no longer shows the second SSN on row 2 anywhere. §B1 records the `1ba6f098` twin being deleted for exactly that, with all-matches taught at the `extract_all` cell above instead.
**Output:** differs — see C42 and C43.

<a id="c34"></a>
### C34 · cell 35 [code] · code

baseline L423 → branch L644

```diff
- pattern_cg = r"([0-9]{3})-([0-9]{2})-([0-9]{4})"
- ssn_data["SSN"].str.extract(pattern_cg)
- 
- # %%
- ssn_data["SSN"].str.extractall(pattern_cg)
+ ssn_data["SSN"].str.extract_groups(pattern_cg).struct.unnest()
```

**Why:** `extract` + `extractall` collapse into one `extract_groups`, with the capture groups named in the pattern so the struct fields carry meaning, and `.struct.unnest()` to spread them into columns.
**Output:** differs — columns `area`/`group`/`serial` instead of `0`/`1`/`2`; the non-matching row is kept as nulls rather than dropped; the second match on row 2 is gone.

<a id="c35"></a>
### C35 · cell 45: Limitations of Regular Expressions · mechanical
baseline L497 → branch L714

```diff
- # - Use `python` and `pandas` RegEx methods.
+ # - Use `python` and `polars` RegEx methods.
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c36"></a>
### C36 · `display(county_and_state), display(county_and_pop);` · output

committed output

```diff
- [text]                        County State
- [text] 0              De Witt County    IL
- [text] 1        Lac qui Parle County    MN
- [text] 2      Lewis and Clark County    MT
- [text] 3  St John the Baptist Parish    LS
- [text]                  County  Population
- [text] 0                DeWitt       16798
- [text] 1         Lac Qui Parle        8067
- [text] 2         Lewis & Clark       55716
- [text] 3  St. John the Baptist       43044
+ [text] shape: (4, 2)
+ [text] ┌────────────────────────────┬───────┐
+ [text] │ County                     ┆ State │
+ [text] │ ---                        ┆ ---   │
+ [text] │ str                        ┆ str   │
+ [text] ╞════════════════════════════╪═══════╡
+ [text] │ De Witt County             ┆ IL    │
+ [text] │ Lac qui Parle County       ┆ MN    │
+ [text] │ Lewis and Clark County     ┆ MT    │
+ [text] │ St John the Baptist Parish ┆ LS    │
+ [text] └────────────────────────────┴───────┘
+ [text] shape: (4, 2)
+ [text] ┌──────────────────────┬────────────┐
+ [text] │ County               ┆ Population │
+ [text] │ ---                  ┆ ---        │
+ [text] │ str                  ┆ i64        │
+ [text] ╞══════════════════════╪════════════╡
+ [text] │ DeWitt               ┆ 16798      │
+ [text] │ Lac Qui Parle        ┆ 8067       │
+ [text] │ Lewis & Clark        ┆ 55716      │
+ [text] │ St. John the Baptist ┆ 43044      │
+ [text] └──────────────────────┴────────────┘
```

**Why:** Re-executed; the Polars table repr replaces the pandas one.
**Reader sees:** equivalent — the same four rows on each of the two frames, and both frames are present (the pane generator once dropped one, §B2 #4).

<a id="c37"></a>
### C37 · `def canonicalize_county_series(county_series):` · output

committed output

```diff
- [text]                  County  Population clean_county_pandas
- [text] 0                DeWitt       16798              dewitt
- [text] 1         Lac Qui Parle        8067         lacquiparle
- [text] 2         Lewis & Clark       55716       lewisandclark
- [text] 3  St. John the Baptist       43044    stjohnthebaptist
- [text]                        County State clean_county_pandas
- [text] 0              De Witt County    IL              dewitt
- [text] 1        Lac qui Parle County    MN         lacquiparle
- [text] 2      Lewis and Clark County    MT       lewisandclark
- [text] 3  St John the Baptist Parish    LS    stjohnthebaptist
+ [text] shape: (4, 3)
+ [text] ┌──────────────────────┬────────────┬─────────────────────┐
+ [text] │ County               ┆ Population ┆ clean_county_polars │
+ [text] │ ---                  ┆ ---        ┆ ---                 │
+ [text] │ str                  ┆ i64        ┆ str                 │
+ [text] ╞══════════════════════╪════════════╪═════════════════════╡
+ [text] │ DeWitt               ┆ 16798      ┆ dewitt              │
+ [text] │ Lac Qui Parle        ┆ 8067       ┆ lacquiparle         │
+ [text] │ Lewis & Clark        ┆ 55716      ┆ lewisandclark       │
+ [text] │ St. John the Baptist ┆ 43044      ┆ stjohnthebaptist    │
+ [text] └──────────────────────┴────────────┴─────────────────────┘
+ [text] shape: (4, 3)
+ [text] ┌────────────────────────────┬───────┬─────────────────────┐
+ [text] │ County                     ┆ State ┆ clean_county_polars │
+ [text] │ ---                        ┆ ---   ┆ ---                 │
+ [text] │ str                        ┆ str   ┆ str                 │
+ [text] ╞════════════════════════════╪═══════╪═════════════════════╡
+ [text] │ De Witt County             ┆ IL    ┆ dewitt              │
+ [text] │ Lac qui Parle County       ┆ MN    ┆ lacquiparle         │
+ [text] │ Lewis and Clark County     ┆ MT    ┆ lewisandclark       │
+ [text] │ St John the Baptist Parish ┆ LS    ┆ stjohnthebaptist    │
+ [text] └────────────────────────────┴───────┴─────────────────────┘
```

**Why:** Re-executed after the `with_columns` rewrite; the added column is named `clean_county_polars`.
**Reader sees:** changed: the third column's heading. The canonicalised values are identical, which is what the section is about.

<a id="c38"></a>
### C38 · `html_data` · output

committed output

```diff
- [text]                                    HTML
- [text] 0  <div><td valign='top'>Moo</td></div>
- [text] 1   <a href='http://ds100.org'>Link</a>
- [text] 2                      <b>Bold text</b>
+ [text] shape: (3, 1)
+ [text] ┌─────────────────────────────────┐
+ [text] │ HTML                            │
+ [text] │ ---                             │
+ [text] │ str                             │
+ [text] ╞═════════════════════════════════╡
+ [text] │ <div><td valign='top'>Moo</td>… │
+ [text] │ <a href='http://ds100.org'>Lin… │
+ [text] │ <b>Bold text</b>                │
+ [text] └─────────────────────────────────┘
```

**Why:** Polars' table repr truncates cell contents at the column width.
**Reader sees:** changed: the HTML strings are cut off with `…`, so the reader can no longer read the full tags in this output — in the one chapter whose subject is matching those tags. The pattern and the stripped result are printed in the cells below, so nothing is unrecoverable, but this is a real loss and a staff decision.

<a id="c39"></a>
### C39 · `pattern = r"<[^>]+>"` · output

committed output

```diff
- [text] 0          Moo
- [text] 1         Link
- [text] 2    Bold text
- [text] Name: HTML, dtype: object
+ [text] shape: (3,)
+ [text] Series: 'HTML' [str]
+ [text] [
+ [text] 	"Moo"
+ [text] 	"Link"
+ [text] 	"Bold text"
+ [text] ]
```

**Why:** Re-executed; `Series` repr.
**Reader sees:** equivalent — the same three stripped strings.

<a id="c40"></a>
### C40 · `ssn_data` · output

committed output

```diff
- [text]                               SSN
- [text] 0                     987-65-4321
- [text] 1                           forty
- [text] 2  123-45-6789 bro or 321-45-6789
- [text] 3                     999-99-9999
+ [text] shape: (4, 1)
+ [text] ┌────────────────────────────────┐
+ [text] │ SSN                            │
+ [text] │ ---                            │
+ [text] │ str                            │
+ [text] ╞════════════════════════════════╡
+ [text] │ 987-65-4321                    │
+ [text] │ forty                          │
+ [text] │ 123-45-6789 bro or 321-45-6789 │
+ [text] │ 999-99-9999                    │
+ [text] └────────────────────────────────┘
```

**Why:** Re-executed; table repr.
**Reader sees:** equivalent — the same four SSN strings, none truncated.

<a id="c41"></a>
### C41 · `ssn_data["SSN"].str.extract_all(pattern)` · output

committed output

```diff
- [text] 0                 [987-65-4321]
- [text] 1                            []
- [text] 2    [123-45-6789, 321-45-6789]
- [text] 3                 [999-99-9999]
- [text] Name: SSN, dtype: object
+ [text] shape: (4,)
+ [text] Series: 'SSN' [list[str]]
+ [text] [
+ [text] 	["987-65-4321"]
+ [text] 	[]
+ [text] 	["123-45-6789", "321-45-6789"]
+ [text] 	["999-99-9999"]
+ [text] ]
```

**Why:** `findall` → `extract_all`.
**Reader sees:** equivalent — the same four lists; the `list[str]` dtype is now visible and the prose names it.

<a id="c42"></a>
### C42 · `pattern_cg = r"(?<area>[0-9]{3})-(?<group>[0-9]{2})-(?<serial>[0-9]{4}` · output

committed output

```diff
- [text]      0    1     2
- [text] 0  987   65  4321
- [text] 1  NaN  NaN   NaN
- [text] 2  123   45  6789
- [text] 3  999   99  9999
+ [text] shape: (4,)
+ [text] Series: 'SSN' [struct[3]]
+ [text] [
+ [text] 	{"987","65","4321"}
+ [text] 	{null,null,null}
+ [text] 	{"123","45","6789"}
+ [text] 	{"999","99","9999"}
+ [text] ]
```

**Why:** `extract` returned a three-column frame; `extract_groups` returns a struct, one field per named group. Verified on the pin.
**Reader sees:** changed: a struct of named fields replaces three integer-labelled columns, and the non-matching row reads `{null,null,null}` rather than `NaN`. The same three captured pieces.

<a id="c43"></a>
### C43 · `ssn_data["SSN"].str.extract_groups(pattern_cg).struct.unnest()` · output

committed output

```diff
- [text]            0   1     2
- [text]   match
- [text] 0 0      987  65  4321
- [text] 2 0      123  45  6789
- [text]   1      321  45  6789
- [text] 3 0      999  99  9999
+ [text] shape: (4, 3)
+ [text] ┌──────┬───────┬────────┐
+ [text] │ area ┆ group ┆ serial │
+ [text] │ ---  ┆ ---   ┆ ---    │
+ [text] │ str  ┆ str   ┆ str    │
+ [text] ╞══════╪═══════╪════════╡
+ [text] │ 987  ┆ 65    ┆ 4321   │
+ [text] │ null ┆ null  ┆ null   │
+ [text] │ 123  ┆ 45    ┆ 6789   │
+ [text] │ 999  ┆ 99    ┆ 9999   │
+ [text] └──────┴───────┴────────┘
```

**Why:** The baseline cell was `extractall`, which returns every match under a MultiIndex; the branch cell is `extract_groups(...).struct.unnest()`, which returns the first match per row. Verified on the pin.
**Reader sees:** changed: the second SSN on row 2 (`321-45-6789`) no longer appears, and the non-matching row is kept as nulls instead of dropped. The all-matches lesson survives at the `extract_all` cell above, but a reader who reads only this pair no longer sees it. This is the one output in the chapter where the reader learns something different.

