# eda — change report

`887a578b0a4b:content/eda/eda.ipynb` → `content/eda/eda.ipynb`

**Tier C · 132 changes:** output 38 · prose 29 · mixed 1 · tab-twins 22 · code 30 · mechanical 9 · metadata 3

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

A rename pass over most of the chapter, with three cells genuinely rebuilt: the `%Y%W%w` week parse (no chrono equivalent; verified bit-identical to pandas on all 5380 rows), the whitespace-delimited CO₂ read (no regex separator in Polars, so one `read_csv` became a read/split/name/cast pipeline that reproduces 738×7 exactly), and the naive ILINet read, which raises `ComputeError` without `truncate_ragged_lines=True`. Three things deserve staff attention. First, cell `a3fde967` no longer raises — `pl.read_json` succeeds where `pd.read_json` raised `ValueError` — so the chapter's only deliberate error demo now survives solely inside the pandas pane of its comparison block; that contradicts AGENTS.md hard rule 6 and rests entirely on the `eda: resolved_errors` allowlist entry and the staff decision recorded in CONVERSIONS.md. Second, the `ili`/`vax` join coalesces its keys, so the joined frame ships 20 columns instead of 22 and the scatterplot's `hue` moved from `HHS Region` to `REGION` (verified identical values), and cell `719dc1a4` now shows a 738×1 frame of raw strings where the baseline showed the finished 738×7 table. Third, six prose edits fix pre-existing errors rather than pandas-isms (CONTRADICTIONS §A8 #1, #3, #4), and staff must decide whether those ship inside this diff or against `main`. Mechanically the chapter is clean: all 10 dropdown mirrors match their code cells byte-for-byte, and all 20 tab-twin blocks carry both panes with every Polars pane equal to its cell's committed output (all verified in the d100 env, polars 1.43.1).

## Needs review

- [C6](#c6) · cell 10 [markdown]
- [C12](#c12) · cell 32: JSON with polars
- [C17](#c17) · cell 35 [markdown]
- [C20](#c20) · cell 38 [markdown]
- [C22](#c22) · cell 38: Temporality with the `polars` `dt` namespace
- [C26](#c26) · cell 41 [markdown]
- [C33](#c33) · cell 52 [markdown]
- [C34](#c34) · cell 52: Missing Values
- [C39](#c39) · cell 59 [markdown]
- [C42](#c42) · cell 63: Preprocessing and column manipulation
- [C46](#c46) · cell 71 [markdown]
- [C48](#c48) · cell 71 [markdown]
- [C51](#c51) · cell 81 [markdown]
- [C53](#c53) · cell 83 [markdown]
- [C57](#c57) · cell 89: Dealing with Missing Values
- [C59](#c59) · cell 91: Reading this file into `polars`?
- [C61](#c61) · cell 93 [markdown]
- [C62](#c62) · cell 93: Exploring Variable Feature Types
- [C66](#c66) · cell 103: Understanding Missing Value 1: `Days`
- [C68](#c68) · cell 106 [markdown]
- [C70](#c70) · cell 110: Understanding Missing Value 2: `Avg`
- [C71](#c71) · cell 110: Histograms of average CO2 measurements
- [C75](#c75) · cell 115: Drop, `null`, or Impute Missing `Avg` Data?
- [C76](#c76) · cell 115: Drop, `null`, or Impute Missing `Avg` Data?
- [C77](#c77) · cell 115: Drop, `null`, or Impute Missing `Avg` Data?
- [C79](#c79) · cell 117 [markdown]
- [C87](#c87) · cell 124 [markdown]
- [C88](#c88) · cell 124: results of plotting data in 1958
- [C89](#c89) · cell 124: you may see more next week; focus on output for now
- [C93](#c93) · cell 128: Presenting the Data: A Discussion on Data Granularity

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C95](#c95) · `pl.read_csv("data/elections.csv").head(5)`
- [C96](#c96) · `pl.read_csv("data/elections.txt", separator='\t').head(3)`
- [C97](#c97) · `pl.read_json('data/elections.json').head(3)`
- [C98](#c98) · `pl.read_json(congress_file)`
- [C99](#c99) · `congress_df = pl.DataFrame(congress_json['members'])`
- [C100](#c100) · `calls = pl.read_csv("data/Berkeley_PD_-_Calls_for_Service.csv")`
- [C101](#c101) · `calls = calls.with_columns(`
- [C102](#c102) · `calls["EVENTDT"].dt.month().head()`
- [C103](#c103) · `calls["EVENTDT"].dt.weekday().head()`
- [C104](#c104) · `calls.sort("EVENTDT").head()`
- [C105](#c105) · `ili = pl.read_csv("data/flu/ILINet.csv", truncate_ragged_lines=True)`
- [C106](#c106) · `ili = pl.read_csv("data/flu/ILINet.csv", skip_rows=1) # drop the title`
- [C107](#c107) · `jan_1 = pl.date(pl.col('YEAR'), 1, 1)`
- [C108](#c108) · `ili['week_start'].dt.year().head()`
- [C109](#c109) · `ili['week_start'].dtype`
- [C110](#c110) · `f, ax = plt.subplots(1, 1, figsize=(12, 7))`
- [C111](#c111) · `f, ax = plt.subplots(1, 1, figsize=(12, 7))`
- [C112](#c112) · `vax = pl.read_csv('data/flu/monthly_child_flu_vaccination.csv')`
- [C113](#c113) · `display(ili.tail(2))`
- [C114](#c114) · `ili_vax = ili.join(`
- [C115](#c115) · `f, ax = plt.subplots(1, 1, figsize=(10, 7))`
- [C116](#c116) · `co2 = pl.read_csv(co2_file, has_header = False, skip_rows = 72)`
- [C117](#c117) · `co2 = (`
- [C118](#c118) · `sns.lineplot(x='DecDate', y='Avg', data=co2);`
- [C119](#c119) · `co2.head()`
- [C120](#c120) · `co2.tail()`
- [C121](#c121) · `co2["Mo"].value_counts().sort("Mo")`
- [C122](#c122) · `sns.displot(co2, x='Days');`
- [C123](#c123) · `sns.scatterplot(x="Yr", y="Days", data=co2);`
- [C124](#c124) · `sns.displot(co2, x='Avg');`
- [C125](#c125) · `co2.filter(pl.col("Avg") < 0)`
- [C126](#c126) · `sns.lineplot(x='DecDate', y='Avg', data=co2)`
- [C127](#c127) · `co2_drop = co2.filter(pl.col('Avg') > 0)`
- [C128](#c128) · `co2_null = co2.with_columns(pl.col(pl.Float64).replace(-99.99, None))`
- [C129](#c129) · `co2_impute = co2.with_columns(Avg = pl.col('Int'))`
- [C130](#c130) · `def line_and_points(data, ax, title):`
- [C131](#c131) · `sns.lineplot(x='DecDate', y='Avg', data=co2_impute)`
- [C132](#c132) · `co2_year = co2_impute.group_by('Yr').mean().sort('Yr')`

## Changes

<a id="c1"></a>
### C1 · cell 1 [markdown] · mechanical

baseline L26 → branch L26

```diff
- # In the past few lectures, we've learned that `pandas` is a toolkit to restructure, modify, and explore a dataset. What we haven't yet touched on is *how* to make these data transformation decisions. When we receive a new set of data from the "real world," how do we know what processing we should do to convert this data into a usable form?
+ # In the past few lectures, we've learned that `polars` is a toolkit to restructure, modify, and explore a dataset. What we haven't yet touched on is *how* to make these data transformation decisions. When we receive a new set of data from the "real world," how do we know what processing we should do to convert this data into a usable form?
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c2"></a>
### C2 · cell 2 [code] · code

baseline L41 → branch L41

```diff
- import pandas as pd
+ import polars as pl
```

**Why:** The chapter's only import site: `import pandas as pd` → `import polars as pl`, which every `pl.` call downstream depends on.
**Output:** same — the cell prints nothing and is tagged `remove-cell`, so it never reaches the page.

<a id="c3"></a>
### C3 · cell 2 [code] · code

baseline L51 → branch L51

```diff
- pd.set_option('display.max_rows', 30)
- pd.set_option('display.max_columns', None)
- pd.set_option('display.precision', 2)
- # This option stops scientific notation for pandas
- pd.set_option('display.float_format', '{:.2f}'.format)
+ pl.Config.set_tbl_rows(30)
+ pl.Config.set_tbl_cols(-1)
+ # Two decimal places, which also keeps wide-ranging columns out of scientific notation
+ pl.Config.set_float_precision(2)
```

**Why:** pandas' display options have no one-to-one Polars analogue. `display.max_rows`/`max_columns` → `pl.Config.set_tbl_rows(30)`/`set_tbl_cols(-1)`; `display.precision` and the `float_format` lambda collapse into `set_float_precision(2)`, which fixes the decimals and thereby also suppresses scientific notation. The comment was re-aimed because two pandas options became one Polars call.
**Output:** same (no output), but it governs every table the chapter prints: 30 rows, all columns, two decimals.

<a id="c4"></a>
### C4 · cell 3: CSV · mechanical

baseline L73 → branch L72

```diff
- # In the past two `pandas` lectures, we briefly touched on the idea of file format: the way data is encoded in a file for storage. Specifically, our `elections` and `babynames` datasets were stored and loaded as CSVs:
+ # In the past two `polars` lectures, we briefly touched on the idea of file format: the way data is encoded in a file for storage. Specifically, our `elections` and `babynames` datasets were stored and loaded as CSVs:
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c5"></a>
### C5 · cell 4 [code] · tab-twins

baseline L75 → branch L74 · spans code and prose

```diff
- # %%
- pd.read_csv("data/elections.csv").head(5)
+ # %% tags=["remove-input", "remove-output"]
+ pl.read_csv("data/elections.csv").head(5)
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 09b0a2b7 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # pl.read_csv("data/elections.csv").head(5)
+ # ```
+ #
+ # ```text
+ # shape: (5, 6)
+ # ┌──────┬───────────────────┬───────────────────────┬──────────────┬────────┬───────┐
+ # │ Year ┆ Candidate         ┆ Party                 ┆ Popular vote ┆ Result ┆ %     │
+ # │ ---  ┆ ---               ┆ ---                   ┆ ---          ┆ ---    ┆ ---   │
+ # │ i64  ┆ str               ┆ str                   ┆ i64          ┆ str    ┆ f64   │
+ # ╞══════╪═══════════════════╪═══════════════════════╪══════════════╪════════╪═══════╡
+ # │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republican ┆ 151271       ┆ loss   ┆ 57.21 │
+ # │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican ┆ 113142       ┆ win    ┆ 42.79 │
+ # │ 1828 ┆ Andrew Jackson    ┆ Democratic            ┆ 642806       ┆ win    ┆ 56.20 │
+ # │ 1828 ┆ John Quincy Adams ┆ National Republican   ┆ 500897       ┆ loss   ┆ 43.80 │
+ # │ 1832 ┆ Andrew Jackson    ┆ Democratic            ┆ 702735       ┆ win    ┆ 54.57 │
+ # └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # pd.read_csv("data/elections.csv").head(5)
+ # ```
+ #
+ # ```text
+ #    Year          Candidate                  Party  Popular vote Result     %
+ # 0  1824     Andrew Jackson  Democratic-Republican        151271   loss 57.21
+ # 1  1824  John Quincy Adams  Democratic-Republican        113142    win 42.79
+ # 2  1828     Andrew Jackson             Democratic        642806    win 56.20
+ # 3  1828  John Quincy Adams    National Republican        500897   loss 43.80
+ … 5 more lines
```

**Why:** `pd.read_csv` → `pl.read_csv`, no argument changes. The cell gained `remove-input`/`remove-output` and a tab-twins block, so the reader now meets this read as a two-library comparison; the pandas pane is the baseline cell's own source and output.
**Output:** differs: same five rows and six columns, but Polars prints a `shape:` header, a dtype row and a box table, and carries no index column. Both panes verified equal to their library's committed output; the panes describe the same operation.

<a id="c6"></a>
### C6 · cell 10 [markdown] · prose · **REVIEW**

baseline L109 → branch L151

```diff
- # TSVs can be loaded into `pandas` using `pd.read_csv`. We'll need to specify the **delimiter** with parameter` sep='\t'` [(documentation)](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html).
+ # TSVs can be loaded into `polars` using `pl.read_csv`. We'll need to specify the **delimiter** with the parameter `separator='\t'` [(documentation)](https://docs.pola.rs/api/python/stable/reference/api/polars.read_csv.html).
```

**Why:** `sep=` → `separator=`, and the `pandas.read_csv` documentation link → the `polars.read_csv` one. The article also moved out of the code span, which in the baseline read "with parameter` sep='\t'`".
**Verdict:** necessary

<a id="c7"></a>
### C7 · cell 11 [code] · code

baseline L111 → branch L153

```diff
- # %%
- pd.read_csv("data/elections.txt", sep='\t').head(3)
+ # %% tags=["remove-input", "remove-output"]
+ pl.read_csv("data/elections.txt", separator='\t').head(3)
```

**Why:** Keyword rename only; the cell also gained the twin tags.
**Output:** differs: Polars box rendering, three rows, no index column. Same values.

<a id="c8"></a>
### C8 · cell 12 [markdown] · tab-twins

baseline L115 → branch L157

```diff
- # An issue with CSVs and TSVs comes up whenever there are commas or tabs within the records. How does `pandas` differentiate between a comma delimiter vs. a comma within the field itself, for example `8,900`? To remedy this, check out the `quotechar` [parameter](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html).
+ # <!-- tab-twins:begin 5960d328 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # pl.read_csv("data/elections.txt", separator='\t').head(3)
+ # ```
+ #
+ # ```text
+ # shape: (3, 6)
+ # ┌──────┬───────────────────┬───────────────────────┬──────────────┬────────┬───────┐
+ # │ Year ┆ Candidate         ┆ Party                 ┆ Popular vote ┆ Result ┆ %     │
+ # │ ---  ┆ ---               ┆ ---                   ┆ ---          ┆ ---    ┆ ---   │
+ # │ i64  ┆ str               ┆ str                   ┆ i64          ┆ str    ┆ f64   │
+ # ╞══════╪═══════════════════╪═══════════════════════╪══════════════╪════════╪═══════╡
+ # │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republican ┆ 151271       ┆ loss   ┆ 57.21 │
+ # │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican ┆ 113142       ┆ win    ┆ 42.79 │
+ # │ 1828 ┆ Andrew Jackson    ┆ Democratic            ┆ 642806       ┆ win    ┆ 56.20 │
+ # └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # pd.read_csv("data/elections.txt", sep='\t').head(3)
+ # ```
+ #
+ # ```text
+ #    Year          Candidate                  Party  Popular vote Result     %
+ # 0  1824     Andrew Jackson  Democratic-Republican        151271   loss 57.21
+ # 1  1824  John Quincy Adams  Democratic-Republican        113142    win 42.79
+ # 2  1828     Andrew Jackson             Democratic        642806    win 56.20
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
+ 
+ # %% [markdown]
+ # An issue with CSVs and TSVs comes up whenever there are commas or tabs within the records. How does `polars` differentiate between a comma delimiter vs. a comma within the field itself, for example `8,900`? To remedy this, check out the `quote_char` [parameter](https://docs.pola.rs/api/python/stable/reference/api/polars.read_csv.html).
```

**Why:** The twin block was inserted ahead of the existing paragraph, which itself changed `quotechar` → `quote_char` and repointed its documentation link.
**Output:** differs: rendering only — same three rows, same values. Panes describe the same operation (a tab-separated read); `sep='\t'` is the honest pandas counterpart of `separator='\t'`.

<a id="c9"></a>
### C9 · cell 15 [markdown] · mechanical

baseline L130 → branch L211

```diff
- # JSON files can be loaded into `pandas` using `pd.read_json`.
+ # JSON files can be loaded into `polars` using `pl.read_json`.
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c10"></a>
### C10 · cell 16 [code] · tab-twins

baseline L132 → branch L213 · spans code and prose

```diff
- # %%
- pd.read_json('data/elections.json').head(3)
+ # %% tags=["remove-input", "remove-output"]
+ pl.read_json('data/elections.json').head(3)
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin ee261cc8 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # pl.read_json('data/elections.json').head(3)
+ # ```
+ #
+ # ```text
+ # shape: (3, 6)
+ # ┌──────┬───────────────────┬───────────────────────┬──────────────┬────────┬───────┐
+ # │ Year ┆ Candidate         ┆ Party                 ┆ Popular vote ┆ Result ┆ %     │
+ # │ ---  ┆ ---               ┆ ---                   ┆ ---          ┆ ---    ┆ ---   │
+ # │ i64  ┆ str               ┆ str                   ┆ i64          ┆ str    ┆ f64   │
+ # ╞══════╪═══════════════════╪═══════════════════════╪══════════════╪════════╪═══════╡
+ # │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republican ┆ 151271       ┆ loss   ┆ 57.21 │
+ # │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican ┆ 113142       ┆ win    ┆ 42.79 │
+ # │ 1828 ┆ Andrew Jackson    ┆ Democratic            ┆ 642806       ┆ win    ┆ 56.20 │
+ # └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # pd.read_json('data/elections.json').head(3)
+ # ```
+ #
+ # ```text
+ #    Year          Candidate                  Party  Popular vote Result     %
+ # 0  1824     Andrew Jackson  Democratic-Republican        151271   loss 57.21
+ # 1  1824  John Quincy Adams  Democratic-Republican        113142    win 42.79
+ # 2  1828     Andrew Jackson             Democratic        642806    win 56.20
+ # ```
+ # ::::
+ # :::::
+ … 1 more lines
```

**Why:** `pd.read_json` → `pl.read_json` on `elections.json`, which is a well-shaped record array, so both libraries rectangularize it the same way.
**Output:** differs: rendering only. Panes describe the same operation — and this twin is worth reading beside C14–C16, where the same pair of calls diverges completely on a differently shaped file.

<a id="c11"></a>
### C11 · cell 32: JSON with polars · mechanical

baseline L236 → branch L356

```diff
- # ###### JSON with pandas
+ # ###### JSON with polars
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c12"></a>
### C12 · cell 32: JSON with polars · prose · **REVIEW**

baseline L238 → branch L358

```diff
- # `pandas` has a built in function called `pd.read_json` for reading in JSON files. In order to read in this JSON file, you might want to try something like the code in the cell below. However, if we tried to run this code, it would error.
+ # `polars` reads a JSON file with `pl.read_json` ([documentation](https://docs.pola.rs/api/python/stable/reference/api/polars.read_json.html)). Let's point it at the congress file and see what comes back.
```

**Why:** The baseline sentence predicted a failure ("if we tried to run this code, it would error"). That is a claim about pandas: verified live on polars 1.43.1, `pl.read_json(congress_file)` succeeds and returns a (1, 3) frame. The paragraph now introduces the call and its documentation instead of forecasting an exception.
**Verdict:** questionable
**Minimal alternative:** Keep a raising cell by switching to `pl.read_ndjson`, which does fail on this file. That was tried during the conversion and rejected by both reviewers (CONVERSIONS.md, `eda` → "The deliberate error was retired"): it demonstrates a format mismatch rather than the structural point, and calls `read_ndjson` a reasonable first guess eight cells after `read_json` has already been shown working. Retiring the demo is licensed only by the `eda: resolved_errors` entry in `conversion/conversion_allowlist.yml`; AGENTS.md hard rule 6 otherwise forbids it, so staff should re-confirm the decision rather than inherit it.

<a id="c13"></a>
### C13 · cell 33 [code] · code

baseline L240 → branch L360

```diff
- # %%
- # This line intentionally produces an error
- pd.read_json(congress_file)
+ # %% tags=["remove-input", "remove-output"]
+ pl.read_json(congress_file)
```

**Why:** The call is a straight `pd.` → `pl.` rename; what changed is that it no longer fails, so the `# This line intentionally produces an error` comment was dropped and the cell was hidden behind a tab-set.
**Output:** differs: `ValueError: Mixing dicts with non-Series may lead to ambiguous ordering.` → a (1, 3) frame with `members` as `list[struct[9]]` beside `pagination` and `request`. Verified live.

<a id="c14"></a>
### C14 · cell 34 [markdown] · tab-twins

baseline L245 → branch L364

```diff
- # - The code above tries to import the entire JSON file located at `congress_file` (`congress_json`), including `congress_json['pagination']` and `congress_json['request']`.
+ # <!-- tab-twins:begin a3fde967 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # pl.read_json(congress_file)
+ # ```
```

**Why:** Opens the tab-twins block for cell `a3fde967`, replacing the first of the two bullets that explained the pandas failure.
**Output:** differs — see C16. The two panes show different outcomes, which here is the honest pairing rather than a defect.

<a id="c15"></a>
### C15 · cell 34 [markdown] · tab-twins

baseline L247 → branch L372

```diff
- # - We only want to make a DataFrame out of `congress_json['members']`.
+ # ```text
+ # shape: (1, 3)
+ # ┌─────────────────────────────────┬────────────┬─────────────────────────────┐
+ # │ members                         ┆ pagination ┆ request                     │
+ # │ ---                             ┆ ---        ┆ ---                         │
+ # │ list[struct[9]]                 ┆ struct[1]  ┆ struct[2]                   │
+ # ╞═════════════════════════════════╪════════════╪═════════════════════════════╡
+ # │ [{"T000491",{"Image courtesy o… ┆ {54}       ┆ {"application/json","json"} │
+ # └─────────────────────────────────┴────────────┴─────────────────────────────┘
+ # ```
+ # ::::
```

**Why:** Carries the Polars pane's output: the rectangularized (1, 3) frame that the new prose at C17 reads.
**Output:** differs: the entire API response became one row, with all 54 members packed into a single `list[struct]` cell. Verified live.

<a id="c16"></a>
### C16 · cell 34 [markdown] · tab-twins

baseline L249 → branch L384

```diff
- # Instead, let's try converting the `members` element of `congress_json` to a DataFrame by using `pd.DataFrame`:
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # This line intentionally produces an error
+ # pd.read_json(congress_file)
+ # ```
+ #
+ # ```text
+ # ValueError: Mixing dicts with non-Series may lead to ambiguous ordering.
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** Closes the block with the pandas pane, which keeps the baseline source (intentional-error comment included) and its `ValueError`.
**Output:** differs by design, and this is now the only place the chapter's error demo reaches a reader. The pairing itself is truthful — `pd.read_json` really does raise on this file and `pl.read_json` really does not — so it is not a CONTRADICTIONS §B1 case, but a reader who never opens the pandas tab never sees a file read fail anywhere in the chapter. That cost is recorded in CONVERSIONS.md.

<a id="c17"></a>
### C17 · cell 35 [markdown] · mixed · **REVIEW**

baseline L251 → branch L398 · spans code and prose

```diff
- # %%
+ # %% [markdown]
+ # One row, three columns. `pl.read_json` rectangularized the whole object, so `pagination` and `request` became columns sitting beside `members`, and all 54 members were packed into a single cell as a list of structs.
+ #
+ # That is not the granularity we want. A row should be one member of Congress, not one API response. The three top-level keys are an artifact of how the service wrapped its reply, and only `members` holds the records we came for.
+ #
+ # (`polars` also offers `pl.read_ndjson` ([documentation](https://docs.pola.rs/api/python/stable/reference/api/polars.read_ndjson.html)) for **newline-delimited** JSON, where every line of the file is one complete record. This file is not in that format, but it is a common way for a service to return records and worth knowing about.)
+ #
+ # Let's build the DataFrame from the `members` element directly, using `pl.DataFrame`:
+ 
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Replaces the two bullets that explained the pandas error with prose that reads the new (1, 3) output: the whole object was rectangularized, so the granularity is wrong (one row per API response, not one per member). A parenthetical introduces `pl.read_ndjson` for newline-delimited JSON, and the last line hands off to `pl.DataFrame(congress_json['members'])` as the baseline did.
**Verdict:** questionable
**Minimal alternative:** Keep the baseline's two bullets, re-pointed at the (1, 3) frame, and drop the `read_ndjson` parenthetical — that paragraph is new teaching content, not something the conversion forced. The granularity paragraph is required, since the bullets it replaces described an error that no longer happens.

<a id="c18"></a>
### C18 · cell 36 [code] · code

baseline L253 → branch L409

```diff
- congress_df = pd.DataFrame(congress_json['members'])
+ congress_df = pl.DataFrame(congress_json['members'])
```

**Why:** `pd.DataFrame` → `pl.DataFrame` over the same list of dicts.
**Output:** differs: the nested dicts become typed `struct` columns (`depiction` is `struct[2]`, `terms` `struct[1]`) where pandas held Python dicts in object columns. Same 5×9 head, same values.

<a id="c19"></a>
### C19 · cell 37 [markdown] · tab-twins

baseline L257 → branch L413

```diff
+ # <!-- tab-twins:begin 870f3938 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Convert dictionary to DataFrame
+ # congress_df = pl.DataFrame(congress_json['members'])
+ # congress_df.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 9)
+ # ┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
+ # │ bioguide ┆ depictio ┆ district ┆ name     ┆ partyNam ┆ state    ┆ terms    ┆ updateDa ┆ url      │
+ # │ Id       ┆ n        ┆ ---      ┆ ---      ┆ e        ┆ ---      ┆ ---      ┆ te       ┆ ---      │
+ # │ ---      ┆ ---      ┆ i64      ┆ str      ┆ ---      ┆ str      ┆ struct[1 ┆ ---      ┆ str      │
+ # │ str      ┆ struct[2 ┆          ┆          ┆ str      ┆          ┆ ]        ┆ str      ┆          │
+ # │          ┆ ]        ┆          ┆          ┆          ┆          ┆          ┆          ┆          │
+ # ╞══════════╪══════════╪══════════╪══════════╪══════════╪══════════╪══════════╪══════════╪══════════╡
+ # │ T000491  ┆ {"Image  ┆ 45       ┆ Tran,    ┆ Democrat ┆ Californ ┆ {[{"Hous ┆ 2025-01- ┆ https:// │
+ # │          ┆ courtesy ┆          ┆ Derek    ┆ ic       ┆ ia       ┆ e of Rep ┆ 21T18:00 ┆ api.cong │
+ # │          ┆ of the   ┆          ┆          ┆          ┆          ┆ resentat ┆ :52Z     ┆ ress.gov │
+ # │          ┆ Member…  ┆          ┆          ┆          ┆          ┆ ives",…  ┆          ┆ /v3/me…  │
+ # │ M001241  ┆ {"Image  ┆ 47       ┆ Min,     ┆ Democrat ┆ Californ ┆ {[{"Hous ┆ 2025-01- ┆ https:// │
+ # │          ┆ courtesy ┆          ┆ Dave     ┆ ic       ┆ ia       ┆ e of Rep ┆ 21T18:00 ┆ api.cong │
+ # │          ┆ of the   ┆          ┆          ┆          ┆          ┆ resentat ┆ :52Z     ┆ ress.gov │
+ # │          ┆ Member…  ┆          ┆          ┆          ┆          ┆ ives",…  ┆          ┆ /v3/me…  │
+ # │ K000400  ┆ {"Image  ┆ 37       ┆ Kamlager ┆ Democrat ┆ Californ ┆ {[{"Hous ┆ 2025-01- ┆ https:// │
+ # │          ┆ courtesy ┆          ┆ -Dove,   ┆ ic       ┆ ia       ┆ e of Rep ┆ 21T18:00 ┆ api.cong │
+ # │          ┆ of the   ┆          ┆ Sydney   ┆          ┆          ┆ resentat ┆ :52Z     ┆ ress.gov │
+ # │          ┆ Member…  ┆          ┆          ┆          ┆          ┆ ives",…  ┆          ┆ /v3/me…  │
+ # │ G000598  ┆ {"Image  ┆ 42       ┆ Garcia,  ┆ Democrat ┆ Californ ┆ {[{"Hous ┆ 2025-01- ┆ https:// │
+ # │          ┆ courtesy ┆          ┆ Robert   ┆ ic       ┆ ia       ┆ e of Rep ┆ 21T18:00 ┆ api.cong │
+ # │          ┆ of the   ┆          ┆          ┆          ┆          ┆ resentat ┆ :52Z     ┆ ress.gov │
+ # │          ┆ Member…  ┆          ┆          ┆          ┆          ┆ ives",…  ┆          ┆ /v3/me…  │
+ # │ K000397  ┆ {"Image  ┆ 40       ┆ Kim,     ┆ Republic ┆ Californ ┆ {[{"Hous ┆ 2025-01- ┆ https:// │
+ # │          ┆ courtesy ┆          ┆ Young    ┆ an       ┆ ia       ┆ e of Rep ┆ 21T18:00 ┆ api.cong │
+ # │          ┆ of the   ┆          ┆          ┆          ┆          ┆ resentat ┆ :52Z     ┆ ress.gov │
+ # │          ┆ Member…  ┆          ┆          ┆          ┆          ┆ ives",…  ┆          ┆ /v3/me…  │
+ # └──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
+ … 45 more lines
```

**Why:** Tab-twins block for cell `870f3938`.
**Output:** differs: Polars wraps a wide frame into fixed-width boxes where pandas wrapped it into stacked column groups, and dicts print as structs. Same rows, same values; panes describe the same operation.

<a id="c20"></a>
### C20 · cell 38 [markdown] · prose · **REVIEW**

baseline L258 → branch L499

```diff
+ #
+ # Notice the `depiction` and `terms` columns. Both fields were dictionaries inside each record, so `polars` stores them as **struct** columns: a column whose values carry named fields of their own, reached through the `.struct` namespace.
```

**Why:** New paragraph naming the `struct` columns the reader can now see in the dtype row, and pointing at the `.struct` namespace.
**Verdict:** necessary

<a id="c21"></a>
### C21 · cell 38: Variable Types · mechanical

baseline L271 → branch L514

```diff
- # Variables are columns. A variable is a measurement of a particular concept. Variables have two common properties: data type/storage type and variable type/feature type. The data type of a variable indicates how each variable value is stored in memory (integer, floating point, boolean, etc.) and affects which `pandas` functions are used. The variable type is a conceptualized measurement of information (and therefore indicates what values a variable can take on). Variable type is identified through expert knowledge, exploring the data itself, or consulting the data codebook. The variable type affects how one visualizes and inteprets the data. In this class, "variable types" are conceptual.
+ # Variables are columns. A variable is a measurement of a particular concept. Variables have two common properties: data type/storage type and variable type/feature type. The data type of a variable indicates how each variable value is stored in memory (integer, floating point, boolean, etc.) and affects which `polars` functions are used. The variable type is a conceptualized measurement of information (and therefore indicates what values a variable can take on). Variable type is identified through expert knowledge, exploring the data itself, or consulting the data codebook. The variable type affects how one visualizes and inteprets the data. In this class, "variable types" are conceptual.
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c22"></a>
### C22 · cell 38: Temporality with the `polars` `dt` namespace · prose · **REVIEW**

baseline L307 → branch L550

```diff
- # #### Temporality with `pandas`' `dt` accessors
- # Let's briefly look at how we can use `pandas`' `dt` accessors to work with dates/times in a dataset using the dataset you'll see in Lab 3: the Berkeley PD Calls for Service dataset.
+ # #### Temporality with the `polars` `dt` namespace
+ # Polars groups methods that apply to only one kind of column into **namespaces**: datetime methods live under `.dt`, string methods under `.str`. Let's briefly look at how we can use the `dt` namespace to work with dates/times in a dataset using the dataset you'll see in Lab 3: the Berkeley PD Calls for Service dataset.
```

**Why:** "Accessor" is pandas vocabulary; Polars calls these namespaces, so the heading and its lead sentence changed and a definition was added. The heading rename also discharges a cross-chapter obligation — `regex` links to this anchor, and it is repointed at `#temporality-with-the-polars-dt-namespace` (verified present in `content/regex/regex.ipynb`).
**Verdict:** necessary

<a id="c23"></a>
### C23 · cell 38: Temporality with the `polars` `dt` namespace · mechanical

baseline L313 → branch L556

```diff
- # calls = pd.read_csv("data/Berkeley_PD_-_Calls_for_Service.csv")
+ # calls = pl.read_csv("data/Berkeley_PD_-_Calls_for_Service.csv")
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c24"></a>
### C24 · cell 39 [code] · code

baseline L318 → branch L561

```diff
- # %% tags=["remove-input"]
- calls = pd.read_csv("data/Berkeley_PD_-_Calls_for_Service.csv")
+ # %% tags=["remove-input", "remove-output"]
+ calls = pl.read_csv("data/Berkeley_PD_-_Calls_for_Service.csv")
```

**Why:** `read_csv` rename; the cell also gained `remove-output`, so its table now reaches the reader only through the tab-set.
**Output:** differs: `BLKADDR`'s blanks read as `null` rather than `NaN`, and the frame prints as an 11-column box. Same five rows.

<a id="c25"></a>
### C25 · cell 39 [code] · tab-twins

baseline L321 → branch L564 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 2d223315 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # calls = pl.read_csv("data/Berkeley_PD_-_Calls_for_Service.csv")
+ # calls.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 11)
+ # ┌─────────┬─────────┬────────┬────────┬────────┬───────┬────────┬────────┬────────┬────────┬───────┐
+ # │ CASENO  ┆ OFFENSE ┆ EVENTD ┆ EVENTT ┆ CVLEGE ┆ CVDOW ┆ InDbDa ┆ Block_ ┆ BLKADD ┆ City   ┆ State │
+ # │ ---     ┆ ---     ┆ T      ┆ M      ┆ ND     ┆ ---   ┆ te     ┆ Locati ┆ R      ┆ ---    ┆ ---   │
+ # │ i64     ┆ str     ┆ ---    ┆ ---    ┆ ---    ┆ i64   ┆ ---    ┆ on     ┆ ---    ┆ str    ┆ str   │
+ # │         ┆         ┆ str    ┆ str    ┆ str    ┆       ┆ str    ┆ ---    ┆ str    ┆        ┆       │
+ # │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ str    ┆        ┆        ┆       │
+ # ╞═════════╪═════════╪════════╪════════╪════════╪═══════╪════════╪════════╪════════╪════════╪═══════╡
+ # │ 2101429 ┆ THEFT   ┆ 04/01/ ┆ 10:58  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ Berkel ┆ null   ┆ Berkel ┆ CA    │
+ # │ 6       ┆ MISD.   ┆ 2021   ┆        ┆ Y      ┆       ┆ 2021   ┆ ey, CA ┆        ┆ ey     ┆       │
+ # │         ┆ (UNDER  ┆ 12:00: ┆        ┆        ┆       ┆ 12:00: ┆ (37.86 ┆        ┆        ┆       │
+ # │         ┆ $950)   ┆ 00 AM  ┆        ┆        ┆       ┆ 00 AM  ┆ 9058,  ┆        ┆        ┆       │
+ # │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ -122.… ┆        ┆        ┆       │
+ # │ 2101439 ┆ THEFT   ┆ 04/01/ ┆ 10:38  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ Berkel ┆ null   ┆ Berkel ┆ CA    │
+ # │ 1       ┆ MISD.   ┆ 2021   ┆        ┆ Y      ┆       ┆ 2021   ┆ ey, CA ┆        ┆ ey     ┆       │
+ # │         ┆ (UNDER  ┆ 12:00: ┆        ┆        ┆       ┆ 12:00: ┆ (37.86 ┆        ┆        ┆       │
+ # │         ┆ $950)   ┆ 00 AM  ┆        ┆        ┆       ┆ 00 AM  ┆ 9058,  ┆        ┆        ┆       │
+ # │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ -122.… ┆        ┆        ┆       │
+ # │ 2109049 ┆ THEFT   ┆ 04/19/ ┆ 12:15  ┆ LARCEN ┆ 1     ┆ 06/15/ ┆ 2100   ┆ 2100   ┆ Berkel ┆ CA    │
+ # │ 4       ┆ MISD.   ┆ 2021   ┆        ┆ Y      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ # │         ┆ (UNDER  ┆ 12:00: ┆        ┆        ┆       ┆ 12:00: ┆ HASTE  ┆ HASTE  ┆        ┆       │
+ # │         ┆ $950)   ┆ 00 AM  ┆        ┆        ┆       ┆ 00 AM  ┆ ST     ┆ ST     ┆        ┆       │
+ # │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
+ # │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey, …  ┆        ┆        ┆       │
+ # │ 2109020 ┆ THEFT   ┆ 02/13/ ┆ 17:00  ┆ LARCEN ┆ 6     ┆ 06/15/ ┆ 2600   ┆ 2600   ┆ Berkel ┆ CA    │
+ # │ 4       ┆ FELONY  ┆ 2021   ┆        ┆ Y      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ # │         ┆ (OVER   ┆ 12:00: ┆        ┆        ┆       ┆ 12:00: ┆ WARRIN ┆ WARRIN ┆        ┆       │
+ # │         ┆ $950)   ┆ 00 AM  ┆        ┆        ┆       ┆ 00 AM  ┆ G ST   ┆ G ST   ┆        ┆       │
+ … 51 more lines
```

**Why:** Tab-twins block for cell `2d223315`.
**Output:** differs: rendering, and `NaN` → `null` in `BLKADDR`. Panes describe the same operation.

<a id="c26"></a>
### C26 · cell 41 [markdown] · prose · **REVIEW**

baseline L327 → branch L661

```diff
- # If we check the data type of these columns, we will see they are stored as strings. We can convert them to `datetime` objects using pandas `to_datetime` function.
+ # If we check the data type of these columns, we will see they are stored as strings. We can convert them to `Datetime` values with the `.str.to_datetime()` method, giving it a format string that describes how the date was written.
```

**Why:** `pd.to_datetime(series)` has no free-function analogue; it becomes the `.str.to_datetime()` method on the string column. Polars will not infer this file's `%m/%d/%Y %I:%M:%S %p` layout, so the format string is now explicit and the sentence says so.
**Verdict:** necessary

<a id="c27"></a>
### C27 · cell 42 [code] · code

baseline L329 → branch L663

```diff
- # %%
- calls["EVENTDT"] = pd.to_datetime(calls["EVENTDT"])
+ # %% tags=["remove-input", "remove-output"]
+ calls = calls.with_columns(
+     pl.col("EVENTDT").str.to_datetime("%m/%d/%Y %I:%M:%S %p")
+ )
```

**Why:** Column assignment → `with_columns`, and the parse moved onto the string column with an explicit format.
**Output:** differs: the dtype label reads `datetime[μs]` rather than `datetime64[ns]`. The parsed instants are the same.

<a id="c28"></a>
### C28 · cell 43 [markdown] · tab-twins

baseline L334 → branch L670

```diff
- # Now, we can use the `dt` accessor on this column.
+ # <!-- tab-twins:begin 7bdeda96 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # calls = calls.with_columns(
+ #     pl.col("EVENTDT").str.to_datetime("%m/%d/%Y %I:%M:%S %p")
+ # )
+ # calls.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 11)
+ # ┌─────────┬─────────┬────────┬────────┬────────┬───────┬────────┬────────┬────────┬────────┬───────┐
+ # │ CASENO  ┆ OFFENSE ┆ EVENTD ┆ EVENTT ┆ CVLEGE ┆ CVDOW ┆ InDbDa ┆ Block_ ┆ BLKADD ┆ City   ┆ State │
+ # │ ---     ┆ ---     ┆ T      ┆ M      ┆ ND     ┆ ---   ┆ te     ┆ Locati ┆ R      ┆ ---    ┆ ---   │
+ # │ i64     ┆ str     ┆ ---    ┆ ---    ┆ ---    ┆ i64   ┆ ---    ┆ on     ┆ ---    ┆ str    ┆ str   │
+ # │         ┆         ┆ dateti ┆ str    ┆ str    ┆       ┆ str    ┆ ---    ┆ str    ┆        ┆       │
+ # │         ┆         ┆ me[μs] ┆        ┆        ┆       ┆        ┆ str    ┆        ┆        ┆       │
+ # ╞═════════╪═════════╪════════╪════════╪════════╪═══════╪════════╪════════╪════════╪════════╪═══════╡
+ # │ 2101429 ┆ THEFT   ┆ 2021-0 ┆ 10:58  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ Berkel ┆ null   ┆ Berkel ┆ CA    │
+ # │ 6       ┆ MISD.   ┆ 4-01   ┆        ┆ Y      ┆       ┆ 2021   ┆ ey, CA ┆        ┆ ey     ┆       │
+ # │         ┆ (UNDER  ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ (37.86 ┆        ┆        ┆       │
+ # │         ┆ $950)   ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ 9058,  ┆        ┆        ┆       │
+ # │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ -122.… ┆        ┆        ┆       │
+ # │ 2101439 ┆ THEFT   ┆ 2021-0 ┆ 10:38  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ Berkel ┆ null   ┆ Berkel ┆ CA    │
+ # │ 1       ┆ MISD.   ┆ 4-01   ┆        ┆ Y      ┆       ┆ 2021   ┆ ey, CA ┆        ┆ ey     ┆       │
+ # │         ┆ (UNDER  ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ (37.86 ┆        ┆        ┆       │
+ # │         ┆ $950)   ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ 9058,  ┆        ┆        ┆       │
+ # │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ -122.… ┆        ┆        ┆       │
+ # │ 2109049 ┆ THEFT   ┆ 2021-0 ┆ 12:15  ┆ LARCEN ┆ 1     ┆ 06/15/ ┆ 2100   ┆ 2100   ┆ Berkel ┆ CA    │
+ # │ 4       ┆ MISD.   ┆ 4-19   ┆        ┆ Y      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ # │         ┆ (UNDER  ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ HASTE  ┆ HASTE  ┆        ┆       │
+ # │         ┆ $950)   ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ ST     ┆ ST     ┆        ┆       │
+ # │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
+ # │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey, …  ┆        ┆        ┆       │
+ # │ 2109020 ┆ THEFT   ┆ 2021-0 ┆ 17:00  ┆ LARCEN ┆ 6     ┆ 06/15/ ┆ 2600   ┆ 2600   ┆ Berkel ┆ CA    │
+ # │ 4       ┆ FELONY  ┆ 2-13   ┆        ┆ Y      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ # │         ┆ (OVER   ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ WARRIN ┆ WARRIN ┆        ┆       │
+ # │         ┆ $950)   ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ G ST   ┆ G ST   ┆        ┆       │
+ … 54 more lines
```

**Why:** Tab-twins block for cell `7bdeda96`.
**Output:** differs: rendering, `null` for `NaN`, and the microsecond-resolution dtype label. Panes describe the same operation.

<a id="c29"></a>
### C29 · cell 45 [code] · code

baseline L338 → branch L767

```diff
- # %%
- calls["EVENTDT"].dt.month.head()
+ # %% tags=["remove-input", "remove-output"]
+ calls["EVENTDT"].dt.month().head()
```

**Why:** `.dt.month` is a property in pandas and a method in Polars.
**Output:** differs: `Series.head()` defaults to **10** in Polars and 5 in pandas, so ten values print instead of five, and the dtype is `i8` rather than `int32`. The first five values are identical.

<a id="c30"></a>
### C30 · cell 46 [markdown] · tab-twins

baseline L342 → branch L771

```diff
- # Which day of the week the date is on:
+ # <!-- tab-twins:begin b505d05e -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # calls["EVENTDT"].dt.month().head()
+ # ```
+ #
+ # ```text
+ # shape: (10,)
+ # Series: 'EVENTDT' [i8]
+ # [
+ # 	4
+ # 	4
+ # 	4
+ # 	2
+ # 	2
+ # 	12
+ # 	5
+ # 	3
+ # 	3
+ # 	3
+ # ]
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # calls["EVENTDT"].dt.month.head()
+ # ```
+ #
+ # ```text
+ # 0    4
+ # 1    4
+ # 2    4
+ # 3    2
+ # 4    2
+ # Name: EVENTDT, dtype: int32
+ # ```
+ … 6 more lines
```

**Why:** Tab-twins block for cell `b505d05e`.
**Output:** differs: ten rows against five, from the `head()` default. Same operation, identical first five values.

<a id="c31"></a>
### C31 · cell 48 [code] · code

baseline L345 → branch L819

```diff
- calls["EVENTDT"].dt.dayofweek.head()
+ calls["EVENTDT"].dt.weekday().head()
```

**Why:** `.dt.dayofweek` → `.dt.weekday()`, the nearest Polars equivalent, which numbers Monday 1–7 instead of 0–6.
**Output:** differs, and materially: `3,3,0,5,0` → `4,4,1,6,1`, plus ten rows instead of five. **This cell has no tab-twin** — CONTRADICTIONS §B1 removed it because the prose above both panes announces "Monday = 1" while the pandas pane printed 0-based values, so a pandas reader saw output contradicting the sentence introducing it. That contradiction was introduced by the conversion and is already fixed by dropping the twin. Verified live: the new values match the dataset's own `CVDOW` column on every row except Sundays, where `CVDOW` is 0 and `weekday()` is 7.

<a id="c32"></a>
### C32 · cell 50 [code] · tab-twins

baseline L350 → branch L824 · spans code and prose

```diff
- # %%
- calls.sort_values("EVENTDT").head()
+ # %% tags=["remove-input", "remove-output"]
+ calls.sort("EVENTDT").head()
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin a113c785 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # calls.sort("EVENTDT").head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 11)
+ # ┌─────────┬─────────┬────────┬────────┬────────┬───────┬────────┬────────┬────────┬────────┬───────┐
+ # │ CASENO  ┆ OFFENSE ┆ EVENTD ┆ EVENTT ┆ CVLEGE ┆ CVDOW ┆ InDbDa ┆ Block_ ┆ BLKADD ┆ City   ┆ State │
+ # │ ---     ┆ ---     ┆ T      ┆ M      ┆ ND     ┆ ---   ┆ te     ┆ Locati ┆ R      ┆ ---    ┆ ---   │
+ # │ i64     ┆ str     ┆ ---    ┆ ---    ┆ ---    ┆ i64   ┆ ---    ┆ on     ┆ ---    ┆ str    ┆ str   │
+ # │         ┆         ┆ dateti ┆ str    ┆ str    ┆       ┆ str    ┆ ---    ┆ str    ┆        ┆       │
+ # │         ┆         ┆ me[μs] ┆        ┆        ┆       ┆        ┆ str    ┆        ┆        ┆       │
+ # ╞═════════╪═════════╪════════╪════════╪════════╪═══════╪════════╪════════╪════════╪════════╪═══════╡
+ # │ 2009221 ┆ THEFT   ┆ 2020-1 ┆ 18:30  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ 800    ┆ 800    ┆ Berkel ┆ CA    │
+ # │ 4       ┆ FROM    ┆ 2-17   ┆        ┆ Y -    ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ # │         ┆ AUTO    ┆ 00:00: ┆        ┆ FROM   ┆       ┆ 12:00: ┆ SHATTU ┆ SHATTU ┆        ┆       │
+ # │         ┆         ┆ 00     ┆        ┆ VEHICL ┆       ┆ 00 AM  ┆ CK AVE ┆ CK AVE ┆        ┆       │
+ # │         ┆         ┆        ┆        ┆ E      ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
+ # │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ e…     ┆        ┆        ┆       │
+ # │ 2005737 ┆ GUN/WEA ┆ 2020-1 ┆ 22:18  ┆ WEAPON ┆ 4     ┆ 06/15/ ┆ 6200   ┆ 6200   ┆ Berkel ┆ CA    │
+ # │ 3       ┆ PON     ┆ 2-17   ┆        ┆ S OFFE ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ # │         ┆         ┆ 00:00: ┆        ┆ NSE    ┆       ┆ 12:00: ┆ SAN    ┆ SAN    ┆        ┆       │
+ # │         ┆         ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ PABLO  ┆ PABLO  ┆        ┆       │
+ # │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ AVE    ┆ AVE    ┆        ┆       │
+ # │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berke… ┆        ┆        ┆       │
+ # │ 2005720 ┆ ASSAULT ┆ 2020-1 ┆ 16:50  ┆ ASSAUL ┆ 4     ┆ 06/15/ ┆ 2100   ┆ 2100   ┆ Berkel ┆ CA    │
+ # │ 7       ┆ /BATTER ┆ 2-17   ┆        ┆ T      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ # │         ┆ Y MISD. ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ SHATTU ┆ SHATTU ┆        ┆       │
+ # │         ┆         ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ CK AVE ┆ CK AVE ┆        ┆       │
+ # │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
+ # │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ …      ┆        ┆        ┆       │
+ # │ 2005732 ┆ THEFT   ┆ 2020-1 ┆ 15:44  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ 1800   ┆ 1800   ┆ Berkel ┆ CA    │
+ … 53 more lines
```

**Why:** `sort_values` → `sort`; no keyword was needed, since the baseline sorted ascending and that is Polars' default.
**Output:** differs beyond rendering. Verified: ten records share the minimum timestamp 2020-12-17, and the two libraries break that tie differently, so the panes show **different rows** — pandas leads with CASENO 20057398, Polars with 20092214 and includes 20057373, which pandas' head does not. Same operation, legitimate either way. `EVENTDT` has no nulls (verified), so hard rule 8's nulls-first hazard does not bite here.

<a id="c33"></a>
### C33 · cell 52 [markdown] · prose · **REVIEW**

baseline L356 → branch L921

```diff
- # We can also do many things with the `dt` accessor like switching time zones and converting time back to UNIX/POSIX time. Check out the documentation on `.dt` [accessor](https://pandas.pydata.org/docs/user_guide/basics.html#basics-dt-accessors) and [time series/date functionality](https://pandas.pydata.org/docs/user_guide/timeseries.html#).
+ # We can also do many things with the `dt` namespace like switching time zones and converting time back to UNIX/POSIX time. Check out the documentation on the [`dt` namespace](https://docs.pola.rs/api/python/stable/reference/expressions/temporal.html) and on [parsing and transforming time series](https://docs.pola.rs/user-guide/transformations/time-series/parsing/).
```

**Why:** Vocabulary ("accessor" → "namespace") and two `pandas.pydata.org` links replaced with the Polars temporal-expressions reference and the time-series parsing guide.
**Verdict:** necessary

<a id="c34"></a>
### C34 · cell 52: Missing Values · prose · **REVIEW**

baseline L379 → branch L944

```diff
- # Another common issue encountered with real-world datasets is that of missing data. One strategy to resolve this is to simply drop any records with missing values from the dataset. This does, however, introduce the risk of inducing biases – it is possible that the missing or corrupt records may be systemically related to some feature of interest in the data. This is why it's generally good practice to keep missing data, or at least to only drop if it you can be sure the missing data won't introduce some bias. Another solution is to keep the data as `NaN` values.
+ # Another common issue encountered with real-world datasets is that of missing data. One strategy to resolve this is to simply drop any records with missing values from the dataset. This does, however, introduce the risk of inducing biases – it is possible that the missing or corrupt records may be systemically related to some feature of interest in the data. This is why it's generally good practice to keep missing data, or at least to only drop if it you can be sure the missing data won't introduce some bias. Another solution is to keep the data as `null` values, which is how `polars` marks a value that is absent. A `null` is not the same as a `NaN`: `NaN` is a floating-point value meaning "not a number", which a calculation can produce, while `null` means no value was ever recorded.
```

**Why:** `NaN` → `null`, plus two added sentences distinguishing the two. Polars separates a missing value from a floating-point `NaN`, and this paragraph is the chapter's definition of missing data, so the distinction is load-bearing rather than terminological.
**Verdict:** necessary

<a id="c35"></a>
### C35 · cell 52: CSVs and Field Names · mechanical

baseline L406 → branch L971

```diff
- # 4. `pandas`, using `pd.read_csv()`
+ # 4. `polars`, using `pl.read_csv()`
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c36"></a>
### C36 · cell 56 [markdown] · mechanical

baseline L464 → branch L1029

```diff
- # Finally, let's try option 4 and use the tried-and-true Data 100 approach: `pandas`.
+ # Finally, let's try option 4 and use the tried-and-true Data 100 approach: `polars`.
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c37"></a>
### C37 · cell 57 [code] · code

baseline L466 → branch L1031

```diff
- # %%
- ili = pd.read_csv("data/flu/ILINet.csv")
+ # %% tags=["remove-input", "remove-output"]
+ ili = pl.read_csv("data/flu/ILINet.csv", truncate_ragged_lines=True)
```

**Why:** The naive read is the teaching moment ("why is there only one column?"), and Polars refuses it outright — verified: without the flag `pl.read_csv` raises `ComputeError: found more fields than defined in 'Schema'`. `truncate_ragged_lines=True` restores the pandas behaviour of producing a frame instead of an error, which also keeps G9 from seeing a *new* error.
**Output:** differs: the same (5381, 1) shape as pandas, but the reader sees less — pandas spread every field across 14 unnamed index levels, while Polars keeps only the first field of each line and discards the rest. The lesson (a garbage single-column frame under a title-line header) still lands.

<a id="c38"></a>
### C38 · cell 58 [markdown] · tab-twins

baseline L471 → branch L1036

```diff
- # You may notice some strange things about this table: why is there only one column, and what is happening with column labels?
+ # <!-- tab-twins:begin 35082131 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # ili = pl.read_csv("data/flu/ILINet.csv", truncate_ragged_lines=True)
+ # ili
+ # ```
+ #
+ # ```text
+ # shape: (5_381, 1)
+ # ┌─────────────────────────────────┐
+ # │ PERCENTAGE OF VISITS FOR INFLU… │
+ # │ ---                             │
+ # │ str                             │
+ # ╞═════════════════════════════════╡
+ # │ REGION TYPE                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ …                               │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ # │ HHS Regions                     │
+ … 42 more lines
```

**Why:** Tab-twins block for cell `35082131`.
**Output:** differs: the Polars pane's rows read `HHS Regions` over and over, because only the first field survives `truncate_ragged_lines`, where the pandas pane shows the full records as index levels. Same *operation* — a naive read with the wrong header — but the pandas pane displays data the Polars pane has thrown away, so this is more than a rendering difference and is worth a staff look.

<a id="c39"></a>
### C39 · cell 59 [markdown] · prose · **REVIEW**

baseline L475 → branch L1121

```diff
- # A reasonable first step is to identify the row with the right header. The `pd.read_csv()` function ([documentation](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)) has the convenient `header` parameter that we can set to use the elements in row 1 as the appropriate columns:
+ # A reasonable first step is to identify the row with the right header. The `pl.read_csv()` function ([documentation](https://docs.pola.rs/api/python/stable/reference/api/polars.read_csv.html)) has the convenient `skip_rows` parameter, which throws away lines before the header is read. Setting it to 1 discards the title and promotes row 1 to the column names:
```

**Why:** `header=1` and `skip_rows=1` are not the same parameter: pandas selects which row is the header, Polars discards lines before reading one. The sentence was rewritten to describe discarding rather than selecting, and the doc link repointed.
**Verdict:** necessary

<a id="c40"></a>
### C40 · cell 60 [code] · code

baseline L477 → branch L1123

```diff
- # %%
- ili = pd.read_csv("data/flu/ILINet.csv", header=1) # row index
+ # %% tags=["remove-input", "remove-output"]
+ ili = pl.read_csv("data/flu/ILINet.csv", skip_rows=1) # drop the title line
```

**Why:** `header=1` → `skip_rows=1`; the trailing comment changed from `# row index` to `# drop the title line` to match.
**Output:** differs: the same 15 typed columns, in Polars box rendering, with `AGE 25-64` arriving as `str` holding `null` rather than float `NaN`.

<a id="c41"></a>
### C41 · cell 60 [code] · tab-twins

baseline L480 → branch L1126 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin ffb961d3 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # ili = pl.read_csv("data/flu/ILINet.csv", skip_rows=1) # drop the title line
+ # ili.head(5)
+ # ```
+ #
+ # ```text
+ # shape: (5, 15)
+ # ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬────────┬───────┬───────┬───────┐
+ # │ REG ┆ REG ┆ YEA ┆ WEE ┆ %   ┆ %UN ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE 65 ┆ ILITO ┆ NUM.  ┆ TOTAL │
+ # │ ION ┆ ION ┆ R   ┆ K   ┆ WEI ┆ WEI ┆ 0-4 ┆ 25- ┆ 25- ┆ 5-2 ┆ 50- ┆ ---    ┆ TAL   ┆ OF    ┆ PATIE │
+ # │ TYP ┆ --- ┆ --- ┆ --- ┆ GHT ┆ GHT ┆ --- ┆ 49  ┆ 64  ┆ 4   ┆ 64  ┆ i64    ┆ ---   ┆ PROVI ┆ NTS   │
+ # │ E   ┆ str ┆ i64 ┆ i64 ┆ ED  ┆ ED  ┆ i64 ┆ --- ┆ --- ┆ --- ┆ --- ┆        ┆ i64   ┆ DERS  ┆ ---   │
+ # │ --- ┆     ┆     ┆     ┆ ILI ┆ ILI ┆     ┆ i64 ┆ str ┆ i64 ┆ i64 ┆        ┆       ┆ ---   ┆ i64   │
+ # │ str ┆     ┆     ┆     ┆ --- ┆ --- ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆ i64   ┆       │
+ # │     ┆     ┆     ┆     ┆ f64 ┆ f64 ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ # ╞═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪════════╪═══════╪═══════╪═══════╡
+ # │ HHS ┆ Reg ┆ 201 ┆ 40  ┆ 0.7 ┆ 0.6 ┆ 103 ┆ 50  ┆ nul ┆ 133 ┆ 23  ┆ 13     ┆ 322   ┆ 134   ┆ 47051 │
+ # │ Reg ┆ ion ┆ 5   ┆     ┆ 4   ┆ 8   ┆     ┆     ┆ l   ┆     ┆     ┆        ┆       ┆       ┆       │
+ # │ ion ┆ 1   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ # │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ # │ HHS ┆ Reg ┆ 201 ┆ 40  ┆ 1.0 ┆ 1.2 ┆ 547 ┆ 294 ┆ nul ┆ 528 ┆ 123 ┆ 95     ┆ 1587  ┆ 199   ┆ 12957 │
+ # │ Reg ┆ ion ┆ 5   ┆     ┆ 3   ┆ 2   ┆     ┆     ┆ l   ┆     ┆     ┆        ┆       ┆       ┆ 7     │
+ # │ ion ┆ 2   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ # │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ # │ HHS ┆ Reg ┆ 201 ┆ 40  ┆ 1.2 ┆ 1.2 ┆ 401 ┆ 419 ┆ nul ┆ 625 ┆ 144 ┆ 81     ┆ 1670  ┆ 280   ┆ 13433 │
+ # │ Reg ┆ ion ┆ 5   ┆     ┆ 2   ┆ 4   ┆     ┆     ┆ l   ┆     ┆     ┆        ┆       ┆       ┆ 8     │
+ # │ ion ┆ 3   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ # │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ # │ HHS ┆ Reg ┆ 201 ┆ 40  ┆ 1.0 ┆ 1.1 ┆ 486 ┆ 231 ┆ nul ┆ 613 ┆ 99  ┆ 75     ┆ 1504  ┆ 299   ┆ 12990 │
+ # │ Reg ┆ ion ┆ 5   ┆     ┆ 1   ┆ 6   ┆     ┆     ┆ l   ┆     ┆     ┆        ┆       ┆       ┆ 0     │
+ # │ ion ┆ 4   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ # │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ # │ HHS ┆ Reg ┆ 201 ┆ 40  ┆ 1.0 ┆ 1.1 ┆ 384 ┆ 238 ┆ nul ┆ 444 ┆ 159 ┆ 103    ┆ 1328  ┆ 284   ┆ 11280 │
+ # │ Reg ┆ ion ┆ 5   ┆     ┆ 4   ┆ 8   ┆     ┆     ┆ l   ┆     ┆     ┆        ┆       ┆       ┆ 7     │
+ … 38 more lines
```

**Why:** Tab-twins block for cell `ffb961d3`.
**Output:** differs: rendering, and `NaN` → `null` in `AGE 25-64`. Panes describe the same operation.

<a id="c42"></a>
### C42 · cell 63: Preprocessing and column manipulation · prose · **REVIEW**

baseline L494 → branch L1218

```diff
- # However, `YEAR` and `WEEK` are in two separate columns, so we need to combine them into a single datetime column for the x-axis. Here, the `pd.to_datetime()` function mentioned earlier could help us. The details of how we construct the format here aren't as important as the end result. This is a great use case for a google search or asking an LLM.
+ # However, `YEAR` and `WEEK` are in two separate columns, so we need to combine them into a single date column for the x-axis. Week 1 of a year is the week that begins on its first Monday, and each week is labelled by the Sunday that closes it. `pl.date` builds a date out of year, month and day, and adding a `pl.duration` moves it by whole days. The details of how we construct the date here aren't as important as the end result. This is a great use case for a google search or asking an LLM.
```

**Why:** chrono rejects `%Y%W%w` — `2021520` crosses a year boundary — so the sentence about constructing a format string had nothing left to point at. It was replaced by a plain statement of the rule the arithmetic implements (week 1 begins on the year's first Monday; each week is labelled by its closing Sunday) plus one line introducing `pl.date` and `pl.duration`. The "not as important as the end result" framing is kept.
**Verdict:** necessary

<a id="c43"></a>
### C43 · cell 64 [code] · code

baseline L496 → branch L1220

```diff
- # %%
- ili['week_start'] = pd.to_datetime(
-     (ili['YEAR'] * 100 + ili['WEEK']).astype(str) + '0',
-     format='%Y%W%w'
+ # %% tags=["remove-input", "remove-output"]
+ # Week 1 begins on the first Monday of the year
+ jan_1 = pl.date(pl.col('YEAR'), 1, 1)
+ week_1_monday = jan_1 + pl.duration(days=(8 - jan_1.dt.weekday()) % 7)
+ 
+ # Each week is labelled by the Sunday six days after its Monday
+ ili = ili.with_columns(
+     (week_1_monday + pl.duration(days=7 * (pl.col('WEEK') - 1) + 6)).alias('week_start')
```

**Why:** The chapter's one date rebuild. `pd.to_datetime(..., format='%Y%W%w')` has no Polars equivalent, so it becomes first-Monday-of-the-year plus `7*(WEEK-1)+6` days. **Verified live against pandas: identical on all 5380 rows.** This column is the join key for everything downstream, so an off-by-one here would corrupt the rest of the chapter.
**Output:** differs: the result is `Date`, not `datetime64[ns]`. The values are bit-identical.

<a id="c44"></a>
### C44 · cell 65 [markdown] · tab-twins

baseline L504 → branch L1232

```diff
- # We can access datetime components using the .dt accessor, for example .dt.year and .dt.month.
+ # <!-- tab-twins:begin d4403db1 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # Week 1 begins on the first Monday of the year
+ # jan_1 = pl.date(pl.col('YEAR'), 1, 1)
+ # week_1_monday = jan_1 + pl.duration(days=(8 - jan_1.dt.weekday()) % 7)
+ #
+ # # Each week is labelled by the Sunday six days after its Monday
+ # ili = ili.with_columns(
+ #     (week_1_monday + pl.duration(days=7 * (pl.col('WEEK') - 1) + 6)).alias('week_start')
+ # )
+ # ili.sample(3)
+ # ```
+ #
+ # ```text
+ # shape: (3, 16)
+ # ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬────────┐
+ # │ REG ┆ REG ┆ YEA ┆ WEE ┆ %   ┆ %UN ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ ILI ┆ NUM ┆ TOT ┆ week_s │
+ # │ ION ┆ ION ┆ R   ┆ K   ┆ WEI ┆ WEI ┆ 0-4 ┆ 25- ┆ 25- ┆ 5-2 ┆ 50- ┆ 65  ┆ TOT ┆ .   ┆ AL  ┆ tart   │
+ # │ TYP ┆ --- ┆ --- ┆ --- ┆ GHT ┆ GHT ┆ --- ┆ 49  ┆ 64  ┆ 4   ┆ 64  ┆ --- ┆ AL  ┆ OF  ┆ PAT ┆ ---    │
+ # │ E   ┆ str ┆ i64 ┆ i64 ┆ ED  ┆ ED  ┆ i64 ┆ --- ┆ --- ┆ --- ┆ --- ┆ i64 ┆ --- ┆ PRO ┆ IEN ┆ date   │
+ # │ --- ┆     ┆     ┆     ┆ ILI ┆ ILI ┆     ┆ i64 ┆ str ┆ i64 ┆ i64 ┆     ┆ i64 ┆ VID ┆ TS  ┆        │
+ # │ str ┆     ┆     ┆     ┆ --- ┆ --- ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ ERS ┆ --- ┆        │
+ # │     ┆     ┆     ┆     ┆ f64 ┆ f64 ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ --- ┆ i64 ┆        │
+ # │     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ i64 ┆     ┆        │
+ # ╞═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪════════╡
+ # │ HHS ┆ Reg ┆ 201 ┆ 3   ┆ 2.7 ┆ 3.0 ┆ 392 ┆ 360 ┆ nul ┆ 628 ┆ 222 ┆ 157 ┆ 175 ┆ 141 ┆ 574 ┆ 2018-0 │
+ # │ Reg ┆ ion ┆ 8   ┆     ┆ 7   ┆ 6   ┆     ┆     ┆ l   ┆     ┆     ┆     ┆ 9   ┆     ┆ 49  ┆ 1-21   │
+ # │ ion ┆ 8   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ # │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ # │ HHS ┆ Reg ┆ 202 ┆ 49  ┆ 7.3 ┆ 7.2 ┆ 179 ┆ 140 ┆ nul ┆ 287 ┆ 563 ┆ 558 ┆ 719 ┆ 233 ┆ 994 ┆ 2022-1 │
+ # │ Reg ┆ ion ┆ 2   ┆     ┆ 1   ┆ 4   ┆ 6   ┆ 9   ┆ l   ┆ 3   ┆     ┆     ┆ 9   ┆     ┆ 62  ┆ 2-11   │
+ # │ ion ┆ 8   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ # │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ # │ HHS ┆ Reg ┆ 202 ┆ 1   ┆ 5.7 ┆ 5.1 ┆ 554 ┆ 110 ┆ nul ┆ 964 ┆ 487 ┆ 593 ┆ 371 ┆ 954 ┆ 720 ┆ 2026-0 │
+ # │ Reg ┆ ion ┆ 6   ┆     ┆ 2   ┆ 5   ┆ 7   ┆ 95  ┆ l   ┆ 8   ┆ 5   ┆ 7   ┆ 02  ┆     ┆ 870 ┆ 1-11   │
+ # │ ion ┆ 4   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ # │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ … 33 more lines
```

**Why:** Tab-twins block for cell `d4403db1`.
**Output:** differs: the cell ends in `ili.sample(3)` with no seed, so the two panes show **three different randomly drawn rows** — 2019/2024/2016 on the pandas side, 2018/2022/2026 on the Polars side. That is not a library difference, and a reader may take it for one; seeding the sample would make the panes comparable. Flagged for staff. The Polars pane matches this cell's committed output exactly (verified), and all three drawn `week_start` values are Sundays as the new prose says.

<a id="c45"></a>
### C45 · cell 66 [markdown] · tab-twins

baseline L506 → branch L1306 · spans code and prose

```diff
- # %%
- ili['week_start'].dt.year.head()
+ # %% [markdown]
+ # We can access date components through the `.dt` namespace, for example `.dt.year()` and `.dt.month()`.
+ 
+ # %% tags=["remove-input", "remove-output"]
+ ili['week_start'].dt.year().head()
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin e4371cbb -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # ili['week_start'].dt.year().head()
+ # ```
+ #
+ # ```text
+ # shape: (10,)
+ # Series: 'week_start' [i32]
+ # [
+ # 	2015
+ # 	2015
+ # 	2015
+ # 	2015
+ # 	2015
+ # 	2015
+ # 	2015
+ # 	2015
+ # 	2015
+ # 	2015
+ # ]
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # ili['week_start'].dt.year.head()
+ # ```
+ #
+ # ```text
+ … 10 more lines
```

**Why:** `.dt.year` property → `.dt.year()` method; the sentence above it moved from "accessor" to "namespace", and the cell plus its twin were inserted together.
**Output:** differs: ten rows against five, from the `head()` default, dtype `i32`. Same values.

<a id="c46"></a>
### C46 · cell 71 [markdown] · prose · **REVIEW**

baseline L516 → branch L1364

```diff
- # `ns` above stands for nanoseconds.
+ # `Date` is the `polars` type for a calendar date with no time of day attached.
```

**Why:** "`ns` above stands for nanoseconds" glossed a pandas dtype string that no longer prints. Replaced with a sentence defining Polars' `Date`.
**Verdict:** necessary

<a id="c47"></a>
### C47 · cell 71 [markdown] · prose · **REVIEW**
baseline L518 → branch L1366

```diff
- # - `<M8` refers to the Numpy type `datetime64`
+ # - Its sibling is `Datetime`, which carries a time as well, to microsecond resolution by default
```

**Why:** The bullet glossed `<M8`, the NumPy dtype string `pandas` printed for the cell above it. Under Polars that cell prints `Date`, so there is no `<M8` left on the page to explain; the bullet now names the sibling type a reader will meet next, `Datetime` (microsecond resolution by default, verified on the 1.43.1 pin).
**Verdict:** necessary — the bullet defined a pandas/NumPy dtype spelling that the chapter no longer shows.

<a id="c48"></a>
### C48 · cell 71 [markdown] · prose · **REVIEW**

baseline L520 → branch L1368

```diff
- # Under the hood, datetimes in Pandas are integers representing the number of **nanoseconds** since 1/1/1970 UTC.
+ # Under the hood, a `Date` is an integer counting the number of **days** since 1/1/1970 UTC, and a `Datetime` counts **microseconds** from that same instant.
```

**Why:** The baseline sentence is a claim about pandas storage. Verified: a Polars `Date` counts days since 1970-01-01 and a `Datetime` counts microseconds by default, so both halves of the sentence had to move.
**Verdict:** necessary

<a id="c49"></a>
### C49 · cell 77 [code] · code

baseline L546 → branch L1394

```diff
- # %%
- vax = pd.read_csv('data/flu/monthly_child_flu_vaccination.csv')
- vax['month_dt'] = pd.to_datetime(vax['month_dt'])
- vax['rate'] = vax['Numerator'] / vax['Population']
+ # %% tags=["remove-input", "remove-output"]
+ vax = pl.read_csv('data/flu/monthly_child_flu_vaccination.csv')
+ vax = vax.with_columns(
+     pl.col('month_dt').str.to_date(),
+     rate=pl.col('Numerator') / pl.col('Population'),
+ )
```

**Why:** `pd.to_datetime` → `.str.to_date()` (the column is date-only), and the two separate column assignments collapse into one `with_columns` with a keyword alias for `rate`.
**Output:** differs: `month_dt` is `Date` rather than `datetime64[ns]`. Values unchanged.

<a id="c50"></a>
### C50 · cell 78 [markdown] · tab-twins

baseline L553 → branch L1403

```diff
- # ### Joining Data (Merging different `DataFrame`)
- # First, let's examine the two `DataFrame` we are merging.
+ # <!-- tab-twins:begin 5f24d68b -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # vax = pl.read_csv('data/flu/monthly_child_flu_vaccination.csv')
+ # vax = vax.with_columns(
+ #     pl.col('month_dt').str.to_date(),
+ #     rate=pl.col('Numerator') / pl.col('Population'),
+ # )
+ # vax.head(14)
+ # ```
+ #
+ # ```text
+ # shape: (14, 5)
+ # ┌────────────┬────────────┬───────────┬────────────┬──────┐
+ # │ HHS Region ┆ month_dt   ┆ Numerator ┆ Population ┆ rate │
+ # │ ---        ┆ ---        ┆ ---       ┆ ---        ┆ ---  │
+ # │ str        ┆ date       ┆ f64       ┆ f64        ┆ f64  │
+ # ╞════════════╪════════════╪═══════════╪════════════╪══════╡
+ # │ Region 1   ┆ 2022-07-01 ┆ 17110.00  ┆ 1328581.00 ┆ 0.01 │
+ # │ Region 1   ┆ 2022-08-01 ┆ 42110.00  ┆ 1328581.00 ┆ 0.03 │
+ # │ Region 1   ┆ 2022-09-01 ┆ 129698.00 ┆ 1328581.00 ┆ 0.10 │
+ # │ Region 1   ┆ 2022-10-01 ┆ 297855.00 ┆ 1328581.00 ┆ 0.22 │
+ # │ Region 1   ┆ 2022-11-01 ┆ 430376.00 ┆ 1328581.00 ┆ 0.32 │
+ # │ Region 1   ┆ 2022-12-01 ┆ 508781.00 ┆ 1328581.00 ┆ 0.38 │
+ # │ Region 1   ┆ 2023-01-01 ┆ 545783.00 ┆ 1328581.00 ┆ 0.41 │
+ # │ Region 1   ┆ 2023-02-01 ┆ 563456.00 ┆ 1328581.00 ┆ 0.42 │
+ # │ Region 1   ┆ 2023-03-01 ┆ 575885.00 ┆ 1328581.00 ┆ 0.43 │
+ # │ Region 1   ┆ 2023-04-01 ┆ 581451.00 ┆ 1328581.00 ┆ 0.44 │
+ # │ Region 1   ┆ 2023-05-01 ┆ 586289.00 ┆ 1328581.00 ┆ 0.44 │
+ # │ Region 1   ┆ 2023-06-01 ┆ 590354.00 ┆ 1328581.00 ┆ 0.44 │
+ # │ Region 1   ┆ 2023-07-01 ┆ 10473.00  ┆ 1319459.00 ┆ 0.01 │
+ # │ Region 1   ┆ 2023-08-01 ┆ 32037.00  ┆ 1319459.00 ┆ 0.02 │
+ # └────────────┴────────────┴───────────┴────────────┴──────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ … 31 more lines
```

**Why:** Tab-twins block for cell `5f24d68b`.
**Output:** differs: rendering and the `Date` dtype. Panes describe the same operation.

<a id="c51"></a>
### C51 · cell 81 [markdown] · prose · **REVIEW**

baseline L561 → branch L1480

```diff
- # This is a natural point to pause and consider how weekly timestamps should be aggregated in order to match the monthly granularity of the vaccination data. In this example, we choose to associate each week with the month in which its start date falls. This isn't the only way we could do this, and it also isn't perfect: there may be weeks that are split across two months where the numbers won't match up exactly.
+ # This is a natural point to pause and consider how weekly timestamps should be aggregated in order to match the monthly granularity of the vaccination data. In this example, we choose to associate each week with the month in which its closing Sunday falls. This isn't the only way we could do this, and it also isn't perfect: there may be weeks that are split across two months where the numbers won't match up exactly.
```

**Why:** "the month in which its start date falls" → "in which its closing Sunday falls". `week_start` holds the Sunday that ends the week in both libraries — pandas' `%w` code was `0`, i.e. Sunday — so the baseline wording was loose about a column whose name suggests otherwise; the rewrite states what the value is.
**Verdict:** optional
**Minimal alternative:** Revert to "start date". Note that doing so keeps a pre-existing looseness that CONTRADICTIONS §A8 does not list; if it is kept, it belongs there.

<a id="c52"></a>
### C52 · cell 82 [code] · code

baseline L564 → branch L1483

```diff
- ili["month"] = ili["week_start"].dt.to_period("M").dt.to_timestamp()
+ ili = ili.with_columns(pl.col("week_start").dt.truncate("1mo").alias("month"))
```

**Why:** `dt.to_period('M').dt.to_timestamp()` → `dt.truncate('1mo')`. Polars has no `Period` type, and truncation to the month start reaches the same end state in one call.
**Output:** same values (both give the first of the month); the dtype is `Date` rather than `datetime64[ns]`.

<a id="c53"></a>
### C53 · cell 83 [markdown] · prose · **REVIEW**

baseline L567 → branch L1486

```diff
- # Time to `merge`! Here we use the `DataFrame` method `df1.merge(right=df2, ...)` on `DataFrame df1` ([documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html)). Contrast this with the function `pd.merge(left=df1,right=df2, ...)`([documentation](https://pandas.pydata.org/docs/reference/api/pandas.merge.html#pandas.merge)). Feel free to use either.
+ # Time to join! Here we use the `DataFrame` method `df1.join(df2, ...)` on `DataFrame df1` ([documentation](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.join.html)). `left_on` and `right_on` name the key columns on each side, since the two tables spell them differently, and the default `how='inner'` keeps only the rows that match on both sides. The key columns are folded together, so the joined table carries `month` and `REGION` and does not repeat them under the `vax` names. The user guide walks through the other join strategies ([documentation](https://docs.pola.rs/user-guide/transformations/joins/)).
```

**Why:** `merge` → `join`, both pandas doc links replaced with Polars ones, and two sentences added: what `left_on`/`right_on` do, and that Polars **coalesces** the join keys. The second is what licenses the column drop at C114 — without it the reader has no explanation for `HHS Region` and `month_dt` disappearing.
**Verdict:** necessary

<a id="c54"></a>
### C54 · cell 84 [code] · code

baseline L569 → branch L1488

```diff
- # %%
- ili_vax = ili.merge(
-     vax,
-     left_on=['month', 'REGION'],
+ # %% tags=["remove-input", "remove-output"]
+ ili_vax = ili.join(
+     vax,
+     left_on=['month', 'REGION'],
```

**Why:** `ili.merge(vax, ...)` → `ili.join(vax, ...)`; same `left_on`/`right_on`, same default inner join.
**Output:** differs: 1820 rows on both sides (verified), but 20 columns against pandas' 22 — Polars folds the right-hand keys into the left-hand names, so `HHS Region` and `month_dt` do not survive.

<a id="c55"></a>
### C55 · cell 85 [markdown] · tab-twins

baseline L578 → branch L1497

```diff
- # We often merge datasets to get a much bigger picture of what’s really happening in the data—and one of the best ways to showcase that bigger picture is through a bigger visualization!
+ # <!-- tab-twins:begin 73402b3c -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # ili_vax = ili.join(
+ #     vax,
+ #     left_on=['month', 'REGION'],
+ #     right_on=['month_dt', 'HHS Region']
+ # )
+ # ili_vax.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 20)
+ # ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
+ # │ REG ┆ REG ┆ YEA ┆ WEE ┆ %   ┆ %UN ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ ILI ┆ NUM ┆ TOT ┆ wee ┆ mon ┆ Num ┆ Pop ┆ rat │
+ # │ ION ┆ ION ┆ R   ┆ K   ┆ WEI ┆ WEI ┆ 0-4 ┆ 25- ┆ 25- ┆ 5-2 ┆ 50- ┆ 65  ┆ TOT ┆ .   ┆ AL  ┆ k_s ┆ th  ┆ era ┆ ula ┆ e   │
+ # │ TYP ┆ --- ┆ --- ┆ --- ┆ GHT ┆ GHT ┆ --- ┆ 49  ┆ 64  ┆ 4   ┆ 64  ┆ --- ┆ AL  ┆ OF  ┆ PAT ┆ tar ┆ --- ┆ tor ┆ tio ┆ --- │
+ # │ E   ┆ str ┆ i64 ┆ i64 ┆ ED  ┆ ED  ┆ i64 ┆ --- ┆ --- ┆ --- ┆ --- ┆ i64 ┆ --- ┆ PRO ┆ IEN ┆ t   ┆ dat ┆ --- ┆ n   ┆ f64 │
+ # │ --- ┆     ┆     ┆     ┆ ILI ┆ ILI ┆     ┆ i64 ┆ str ┆ i64 ┆ i64 ┆     ┆ i64 ┆ VID ┆ TS  ┆ --- ┆ e   ┆ f64 ┆ --- ┆     │
+ # │ str ┆     ┆     ┆     ┆ --- ┆ --- ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ ERS ┆ --- ┆ dat ┆     ┆     ┆ f64 ┆     │
+ # │     ┆     ┆     ┆     ┆ f64 ┆ f64 ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ --- ┆ i64 ┆ e   ┆     ┆     ┆     ┆     │
+ # │     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ i64 ┆     ┆     ┆     ┆     ┆     ┆     │
+ # ╞═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╡
+ # │ HHS ┆ Reg ┆ 202 ┆ 26  ┆ 0.9 ┆ 1.0 ┆ 440 ┆ 356 ┆ nul ┆ 346 ┆ 166 ┆ 211 ┆ 151 ┆ 232 ┆ 148 ┆ 202 ┆ 202 ┆ 171 ┆ 132 ┆ 0.0 │
+ # │ Reg ┆ ion ┆ 2   ┆     ┆ 3   ┆ 2   ┆     ┆     ┆ l   ┆     ┆     ┆     ┆ 9   ┆     ┆ 833 ┆ 2-0 ┆ 2-0 ┆ 10. ┆ 858 ┆ 1   │
+ # │ ion ┆ 1   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 7-0 ┆ 7-0 ┆ 00  ┆ 1.0 ┆     │
+ # │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 3   ┆ 1   ┆     ┆ 0   ┆     │
+ # │ HHS ┆ Reg ┆ 202 ┆ 26  ┆ 2.8 ┆ 2.5 ┆ 175 ┆ 630 ┆ nul ┆ 112 ┆ 278 ┆ 297 ┆ 408 ┆ 161 ┆ 163 ┆ 202 ┆ 202 ┆ 699 ┆ 198 ┆ 0.0 │
+ # │ Reg ┆ ion ┆ 2   ┆     ┆ 0   ┆ 0   ┆ 6   ┆     ┆ l   ┆ 4   ┆     ┆     ┆ 5   ┆     ┆ 656 ┆ 2-0 ┆ 2-0 ┆ .00 ┆ 200 ┆ 0   │
+ # │ ion ┆ 2   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 7-0 ┆ 7-0 ┆     ┆ 9.0 ┆     │
+ # │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 3   ┆ 1   ┆     ┆ 0   ┆     │
+ # │ HHS ┆ Reg ┆ 202 ┆ 26  ┆ 1.3 ┆ 1.6 ┆ 134 ┆ 883 ┆ nul ┆ 929 ┆ 397 ┆ 360 ┆ 391 ┆ 371 ┆ 240 ┆ 202 ┆ 202 ┆ 284 ┆ 430 ┆ 0.0 │
+ # │ Reg ┆ ion ┆ 2   ┆     ┆ 9   ┆ 3   ┆ 7   ┆     ┆ l   ┆     ┆     ┆     ┆ 6   ┆     ┆ 707 ┆ 2-0 ┆ 2-0 ┆ .00 ┆ 155 ┆ 0   │
+ # │ ion ┆ 3   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 7-0 ┆ 7-0 ┆     ┆ 6.0 ┆     │
+ # │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 3   ┆ 1   ┆     ┆ 0   ┆     │
+ # │ HHS ┆ Reg ┆ 202 ┆ 26  ┆ 2.2 ┆ 2.4 ┆ 432 ┆ 355 ┆ nul ┆ 343 ┆ 146 ┆ 137 ┆ 141 ┆ 928 ┆ 572 ┆ 202 ┆ 202 ┆ 226 ┆ 132 ┆ 0.0 │
+ # │ Reg ┆ ion ┆ 2   ┆     ┆ 9   ┆ 7   ┆ 0   ┆ 5   ┆ l   ┆ 0   ┆ 9   ┆ 0   ┆ 44  ┆     ┆ 466 ┆ 2-0 ┆ 2-0 ┆ 8.0 ┆ 032 ┆ 0   │
+ # │ ion ┆ 4   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 7-0 ┆ 7-0 ┆ 0   ┆ 79. ┆     │
+ … 55 more lines
```

**Why:** Tab-twins block for cell `73402b3c`.
**Output:** differs: the pandas pane is 22 columns wide and the Polars pane 20. Same operation and the same 1820 rows (verified), and C53 now names the coalescing — but the panes are visibly different shapes, so staff should check that the sentence lands before the reader reaches the tab-set.

<a id="c56"></a>
### C56 · cell 87 [code] · code

baseline L582 → branch L1595

```diff
- sns.scatterplot(ili_vax, x='ILITOTAL', y='rate', alpha=0.3, hue='HHS Region', ax=ax);
+ sns.scatterplot(ili_vax, x='ILITOTAL', y='rate', alpha=0.3, hue='REGION', ax=ax);
```

**Why:** `hue='HHS Region'` no longer exists after the coalescing join, so the hue moved to the surviving key `REGION`. Verified: in the pandas join the two columns are equal on every row, so the colouring is unchanged.
**Output:** differs: the legend title reads `REGION` instead of `HHS Region`. Same ten series, same points.

<a id="c57"></a>
### C57 · cell 89: Dealing with Missing Values · prose · **REVIEW**

baseline L595 → branch L1608

```diff
- # * Keep `NaN` missing values
+ # * Keep `null` missing values
```

**Why:** `NaN` → `null` in the options list, matching the vocabulary settled at C34 and the figure panel title at C89.
**Verdict:** necessary

<a id="c58"></a>
### C58 · cell 91: Reading this file into `polars`? · mechanical

baseline L623 → branch L1636

```diff
- # ### Reading this file into `Pandas`?
+ # ### Reading this file into `polars`?
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c59"></a>
### C59 · cell 91: Reading this file into `polars`? · prose · **REVIEW**

baseline L646 → branch L1659

```diff
- # We can use `read_csv` to read the data into a `pandas` `DataFrame`, and we provide several arguments to specify that the separators are white space, there is no header (**we will set our own column names**), and to skip the first 72 rows of the file.
+ # We can use `pl.read_csv` to read the data into a `polars` `DataFrame`. We provide arguments to specify that there is no header (**we will set our own column names**) and to skip the first 72 rows of the file. There is not a single comma in the data, so every record arrives whole, in one column:
```

**Why:** The baseline listed three `read_csv` arguments, one of them "the separators are white space". Polars `read_csv` has no regex separator, so that argument is gone; the sentence now lists the two that remain and states the consequence the output below shows — every record arrives whole, in one column.
**Verdict:** necessary

<a id="c60"></a>
### C60 · cell 92 [code] · code

baseline L649 → branch L1662

```diff
- co2 = pd.read_csv(
-     co2_file, header = None, skiprows = 72,
-     sep = r'\s+'       #delimiter for continuous whitespace (stay tuned for regex next lecture))
- )
+ co2 = pl.read_csv(co2_file, has_header = False, skip_rows = 72)
```

**Why:** `header=None, skiprows=72, sep=r'\s+'` → `has_header=False, skip_rows=72`. No Polars `separator` matches runs of whitespace, so this read now stops one step short of the pandas one.
**Output:** differs: a 738×1 frame of strings where pandas produced 738×7 typed columns. The split moves to the next cell.

<a id="c61"></a>
### C61 · cell 93 [markdown] · prose · **REVIEW**

baseline L658 → branch L1668

```diff
- # ...But our columns aren't named.
+ # ...But each record is still one long string, and our single column isn't named.
```

**Why:** "...But our columns aren't named" was true of a 7-column frame; the Polars read yields one string column, so the sentence now names both facts. This is CONTRADICTIONS §B1's `719dc1a4` entry — the claim "each record is still one long string … we need to do more EDA" is false on a pandas pane, where parsing has already finished. **Introduced by the conversion and fixed by removing that twin**, which is why this cell ships its Polars output alone.
**Verdict:** necessary

<a id="c62"></a>
### C62 · cell 93: Exploring Variable Feature Types · prose · **REVIEW**

baseline L665 → branch L1675

```diff
- # Using this information, we'll rerun `pd.read_csv`, but this time with some **custom column names.**
+ # Using this information, we'll rerun `pl.read_csv`, but this time we'll pull out every run of non-whitespace characters with `.str.extract_all(r'\S+')`, which amounts to splitting each record on its runs of white space. That leaves a list of seven values per row, which `.list.to_struct` labels with some **custom column names** and `.unnest` spreads across seven columns. Every value arrives as text, so we finish by casting each column to the type it should have.
```

**Why:** The pandas sentence promised a re-run of `read_csv` with custom names. That is no longer what happens, so it now walks the four steps that replace it: `.str.extract_all(r'\S+')`, `.list.to_struct(fields=...)`, `.unnest`, and the cast.
**Verdict:** necessary

<a id="c63"></a>
### C63 · cell 94 [code] · code

baseline L667 → branch L1677

```diff
- # %%
- co2 = pd.read_csv(
-     co2_file, header = None, skiprows = 72,
-     sep = r'\s+', #regex for continuous whitespace (next lecture)
-     names = ['Yr', 'Mo', 'DecDate', 'Avg', 'Int', 'Trend', 'Days']
+ # %% tags=["remove-input", "remove-output"]
+ co2 = (
+     pl.read_csv(co2_file, has_header = False, skip_rows = 72, new_columns = ['row'])
+     .select(
+         pl.col('row')
+         .str.extract_all(r'\S+') #regex for runs of non-whitespace (next lecture)
+         .list.to_struct(fields = ['Yr', 'Mo', 'DecDate', 'Avg', 'Int', 'Trend', 'Days'])
+     )
+     .unnest('row')
+     .cast({'Yr': pl.Int64, 'Mo': pl.Int64, 'DecDate': pl.Float64, 'Avg': pl.Float64,
+            'Int': pl.Float64, 'Trend': pl.Float64, 'Days': pl.Int64})
```

**Why:** The chapter's one genuine reshape. `sep=r'\s+'` has no argument-level equivalent and the file is ragged, so the read/split/name/cast is spelled out instead. **Verified live: 738×7, values identical to the pandas frame, `-99.99` preserved.**
**Output:** same data as the baseline's one-line read; what is new is the Polars rendering and the visible intermediate string stage.

<a id="c64"></a>
### C64 · cell 94 [code] · tab-twins

baseline L674 → branch L1690 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 761e3219 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # co2 = (
+ #     pl.read_csv(co2_file, has_header = False, skip_rows = 72, new_columns = ['row'])
+ #     .select(
+ #         pl.col('row')
+ #         .str.extract_all(r'\S+') #regex for runs of non-whitespace (next lecture)
+ #         .list.to_struct(fields = ['Yr', 'Mo', 'DecDate', 'Avg', 'Int', 'Trend', 'Days'])
+ #     )
+ #     .unnest('row')
+ #     .cast({'Yr': pl.Int64, 'Mo': pl.Int64, 'DecDate': pl.Float64, 'Avg': pl.Float64,
+ #            'Int': pl.Float64, 'Trend': pl.Float64, 'Days': pl.Int64})
+ # )
+ # co2.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 7)
+ # ┌──────┬─────┬─────────┬────────┬────────┬────────┬──────┐
+ # │ Yr   ┆ Mo  ┆ DecDate ┆ Avg    ┆ Int    ┆ Trend  ┆ Days │
+ # │ ---  ┆ --- ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---  │
+ # │ i64  ┆ i64 ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ i64  │
+ # ╞══════╪═════╪═════════╪════════╪════════╪════════╪══════╡
+ # │ 1958 ┆ 3   ┆ 1958.21 ┆ 315.71 ┆ 315.71 ┆ 314.62 ┆ -1   │
+ # │ 1958 ┆ 4   ┆ 1958.29 ┆ 317.45 ┆ 317.45 ┆ 315.29 ┆ -1   │
+ # │ 1958 ┆ 5   ┆ 1958.38 ┆ 317.50 ┆ 317.50 ┆ 314.71 ┆ -1   │
+ # │ 1958 ┆ 6   ┆ 1958.46 ┆ -99.99 ┆ 317.10 ┆ 314.85 ┆ -1   │
+ # │ 1958 ┆ 7   ┆ 1958.54 ┆ 315.86 ┆ 315.86 ┆ 314.98 ┆ -1   │
+ # └──────┴─────┴─────────┴────────┴────────┴────────┴──────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ … 19 more lines
```

**Why:** Tab-twins block for cell `761e3219`.
**Output:** differs: rendering only — both panes end at the same 738×7 frame (verified). The panes reach it by different routes, a single `read_csv` against a four-step pipeline, so this pairing is a real library difference rather than a spelling one, and the tab heading should be read that way.

<a id="c65"></a>
### C65 · cell 97 [code] · code

baseline L680 → branch L1755

```diff
- #| fig-alt: A lineplot of the monthly averages from the 1960s to the 1980s. The data mostly has a repeating wave pattern and is larger as time goes on. However, there are a number of large dips to -100.
+ #| fig-alt: A lineplot of the monthly averages from 1958 to 2019. The data mostly has a repeating wave pattern and is larger as time goes on. However, there are a number of large dips to -100.
```

**Why:** fig-alt corrected. The cell is `sns.lineplot(x='DecDate', y='Avg', data=co2)` with no filter and `DecDate` runs 1958.2 → 2019.6, so "from the 1960s to the 1980s" handed a screen-reader user a 20-year window on a 62-year chart. CONTRADICTIONS §A8 #3, **pre-existing** — the same text is in the baseline.
**Output:** same figure; only the alt text changed.

<a id="c66"></a>
### C66 · cell 103: Understanding Missing Value 1: `Days` · prose · **REVIEW**

baseline L724 → branch L1799

```diff
- # Are we missing any records? The number of months should have 62 or 61 instances (March 1957-August 2019).
+ # Are we missing any records? The number of months should have 62 or 61 instances (March 1958-August 2019). `value_counts` returns a two-column table of each value beside how often it appears, which we sort by month:
```

**Why:** Two changes in one line. "March 1957" → "March 1958": the file starts 1958-03, and 1957 would give 63 instances for March–August (CONTRADICTIONS §A8 #1, **pre-existing**). And a clause was added describing `value_counts`' Polars shape, because the output below is now a two-column table rather than a Series.
**Verdict:** questionable
**Minimal alternative:** The `value_counts` clause is required by the changed output. The 1957 → 1958 correction is not a conversion change and could ship against `main` instead — that is the choice CONTRADICTIONS.md asks staff to make.

<a id="c67"></a>
### C67 · cell 104 [code] · tab-twins

baseline L726 → branch L1801 · spans code and prose

```diff
- # %%
- co2["Mo"].value_counts().sort_index()
+ # %% tags=["remove-input", "remove-output"]
+ co2["Mo"].value_counts().sort("Mo")
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin fb3fcc66 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # co2["Mo"].value_counts().sort("Mo")
+ # ```
+ #
+ # ```text
+ # shape: (12, 2)
+ # ┌─────┬───────┐
+ # │ Mo  ┆ count │
+ # │ --- ┆ ---   │
+ # │ i64 ┆ u32   │
+ # ╞═════╪═══════╡
+ # │ 1   ┆ 61    │
+ # │ 2   ┆ 61    │
+ # │ 3   ┆ 62    │
+ # │ 4   ┆ 62    │
+ # │ 5   ┆ 62    │
+ # │ 6   ┆ 62    │
+ # │ 7   ┆ 62    │
+ # │ 8   ┆ 62    │
+ # │ 9   ┆ 61    │
+ # │ 10  ┆ 61    │
+ # │ 11  ┆ 61    │
+ # │ 12  ┆ 61    │
+ # └─────┴───────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # co2["Mo"].value_counts().sort_index()
+ # ```
+ … 20 more lines
```

**Why:** `value_counts().sort_index()` → `value_counts().sort('Mo')`. Polars returns a DataFrame with the value and `count` as ordinary columns, so there is no index to sort and the sort has to name the column.
**Output:** differs: a 12×2 table against a named Series. The twelve counts are unchanged and the 61/62 split holds (verified). Panes describe the same operation.

<a id="c68"></a>
### C68 · cell 106 [markdown] · prose · **REVIEW**

baseline L738 → branch L1871

```diff
- # sns.displot(co2['Days']);
+ # sns.displot(co2, x='Days');
```

**Why:** Dropdown mirror of code cell `6232f59d`: `sns.displot(co2['Days'])` → `sns.displot(co2, x='Days')`. **Verified: the one-argument form runs on a Polars Series but draws an empty x-axis label**, where pandas took the label from the Series name — so this is a real handoff fix, not churn. Mirror checked byte-for-byte against the code cell: it matches, so hard rule 3 is satisfied.
**Verdict:** necessary

<a id="c69"></a>
### C69 · cell 107 [code] · code

baseline L745 → branch L1878

```diff
- sns.displot(co2['Days']);
+ sns.displot(co2, x='Days');
```

**Why:** The code cell that C68 mirrors; both halves changed together.
**Output:** differs: the x-axis is labelled `Days` again. Left as `displot(co2['Days'])` it would have been blank (verified).

<a id="c70"></a>
### C70 · cell 110: Understanding Missing Value 2: `Avg` · prose · **REVIEW**

baseline L786 → branch L1919

```diff
- # #| fig-alt: Histogram of average CO2 measurements. Most of the data is near 400, though there is a bin with data with AVG less than 0.
+ # #| fig-alt: Histogram of average CO2 measurements. Almost all of the data falls between about 310 and 415 ppm, with the tallest bars in the low 320s. A single isolated bin sits below zero, holding the seven -99.99 missing-value records.
```

**Why:** fig-alt corrected. Binning the column the figure actually plots puts the mass over 310–415 ppm with the tallest bars in the low 320s, not "most of the data is near 400", plus one isolated bin below zero for the seven `-99.99` sentinels (verified: exactly 7 rows). CONTRADICTIONS §A8 #4, **pre-existing**. This is the dropdown mirror; the code-cell half is C72, and the two match.
**Verdict:** questionable
**Minimal alternative:** Revert both halves and fix on `main` — the alt text is not a pandas artifact, so nothing about the conversion required this edit.

<a id="c71"></a>
### C71 · cell 110: Histograms of average CO2 measurements · prose · **REVIEW**

baseline L788 → branch L1921

```diff
- # sns.displot(co2['Avg']);
+ # sns.displot(co2, x='Avg');
```

**Why:** Dropdown mirror of code cell `20adcbbe`: the same seaborn handoff as C68, for `Avg`. Mirror verified identical to the code cell.
**Verdict:** necessary

<a id="c72"></a>
### C72 · cell 111 [code] · code

baseline L793 → branch L1926

```diff
- #| fig-alt: Histogram of average CO2 measurements. Most of the data is near 400, though there is a bin with data with AVG less than 0.
+ #| fig-alt: Histogram of average CO2 measurements. Almost all of the data falls between about 310 and 415 ppm, with the tallest bars in the low 320s. A single isolated bin sits below zero, holding the seven -99.99 missing-value records.
```

**Why:** The code cell's copy of the alt text that C70 mirrors; both halves were changed together, as hard rule 3 requires.
**Output:** same figure; alt text only.

<a id="c73"></a>
### C73 · cell 111 [code] · code

baseline L795 → branch L1928

```diff
- sns.displot(co2['Avg']);
+ sns.displot(co2, x='Avg');
```

**Why:** `sns.displot(co2['Avg'])` → `sns.displot(co2, x='Avg')`, to keep the x-axis label under the Polars handoff.
**Output:** differs: axis label restored. Same histogram.

<a id="c74"></a>
### C74 · cell 113 [code] · tab-twins

baseline L802 → branch L1935 · spans code and prose

```diff
- # %%
- co2[co2["Avg"] < 0]
+ # %% tags=["remove-input", "remove-output"]
+ co2.filter(pl.col("Avg") < 0)
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 0d87b254 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # co2.filter(pl.col("Avg") < 0)
+ # ```
+ #
+ # ```text
+ # shape: (7, 7)
+ # ┌──────┬─────┬─────────┬────────┬────────┬────────┬──────┐
+ # │ Yr   ┆ Mo  ┆ DecDate ┆ Avg    ┆ Int    ┆ Trend  ┆ Days │
+ # │ ---  ┆ --- ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---  │
+ # │ i64  ┆ i64 ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ i64  │
+ # ╞══════╪═════╪═════════╪════════╪════════╪════════╪══════╡
+ # │ 1958 ┆ 6   ┆ 1958.46 ┆ -99.99 ┆ 317.10 ┆ 314.85 ┆ -1   │
+ # │ 1958 ┆ 10  ┆ 1958.79 ┆ -99.99 ┆ 312.66 ┆ 315.61 ┆ -1   │
+ # │ 1964 ┆ 2   ┆ 1964.12 ┆ -99.99 ┆ 320.07 ┆ 319.61 ┆ -1   │
+ # │ 1964 ┆ 3   ┆ 1964.21 ┆ -99.99 ┆ 320.73 ┆ 319.55 ┆ -1   │
+ # │ 1964 ┆ 4   ┆ 1964.29 ┆ -99.99 ┆ 321.77 ┆ 319.48 ┆ -1   │
+ # │ 1975 ┆ 12  ┆ 1975.96 ┆ -99.99 ┆ 330.59 ┆ 331.60 ┆ 0    │
+ # │ 1984 ┆ 4   ┆ 1984.29 ┆ -99.99 ┆ 346.84 ┆ 344.27 ┆ 2    │
+ # └──────┴─────┴─────────┴────────┴────────┴────────┴──────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # co2[co2["Avg"] < 0]
+ # ```
+ #
+ # ```text
+ #        Yr  Mo  DecDate    Avg    Int  Trend  Days
+ # 3    1958   6  1958.46 -99.99 317.10 314.85    -1
+ # 7    1958  10  1958.79 -99.99 312.66 315.61    -1
+ … 9 more lines
```

**Why:** Tab-twins block for cell `0d87b254`; boolean-mask indexing → `filter`.
**Output:** differs: rendering, and pandas' row labels (3, 7, 71, 72, 73, 213, 313) are gone — Polars has no index. Same seven records (verified). Panes describe the same operation.

<a id="c75"></a>
### C75 · cell 115: Drop, `null`, or Impute Missing `Avg` Data? · prose · **REVIEW**

baseline L808 → branch L1988

```diff
- # ### Drop, `NaN`, or Impute Missing `Avg` Data?
+ # ### Drop, `null`, or Impute Missing `Avg` Data?
```

**Why:** Section heading: `NaN` → `null`, following the vocabulary decision at C34. Checked that nothing in `content/` or `myst.yml` links to this heading's anchor, so the rename breaks no cross-reference.
**Verdict:** necessary

<a id="c76"></a>
### C76 · cell 115: Drop, `null`, or Impute Missing `Avg` Data? · prose · **REVIEW**

baseline L813 → branch L1993

```diff
- # 2. Set to NaN
+ # 2. Set to `null`
```

**Why:** The option-list item naming the heading's second branch; changed with the heading.
**Verdict:** necessary

<a id="c77"></a>
### C77 · cell 115: Drop, `null`, or Impute Missing `Avg` Data? · prose · **REVIEW**

baseline L821 → branch L2001

```diff
- # #| fig-alt: A lineplot of the monthly averages from the 1960s to the 1980s. The data mostly has a repeating wave pattern and is larger as time goes on. However, there are a number of large dips to -100.
+ # #| fig-alt: A lineplot of the monthly averages from 1958 to 2019. The data mostly has a repeating wave pattern and is larger as time goes on. However, there are a number of large dips to -100.
```

**Why:** Dropdown mirror of the fig-alt fixed at C65 and C78 — CONTRADICTIONS §A8 #3, **pre-existing**. Mirror verified identical to code cell `11056cc5`.
**Verdict:** questionable
**Minimal alternative:** Same as C65: revert and fix on `main`, since the alt text is not a pandas artifact.

<a id="c78"></a>
### C78 · cell 116 [code] · code

baseline L828 → branch L2008

```diff
- #| fig-alt: A lineplot of the monthly averages from the 1960s to the 1980s. The data mostly has a repeating wave pattern and is larger as time goes on. However, there are a number of large dips to -100.
+ #| fig-alt: A lineplot of the monthly averages from 1958 to 2019. The data mostly has a repeating wave pattern and is larger as time goes on. However, there are a number of large dips to -100.
```

**Why:** The code-cell half of the mirror at C77.
**Output:** same figure; alt text only.

<a id="c79"></a>
### C79 · cell 117 [markdown] · prose · **REVIEW**

baseline L837 → branch L2017

```diff
- # 2. Replace -99.99 with NaN
+ # 2. Replace -99.99 with `null`
```

**Why:** `NaN` → `null` in the three-option list above the demos. Worth noting that the baseline markdown here was already correct — it is the *code* comment at C83 that was reversed.
**Verdict:** necessary

<a id="c80"></a>
### C80 · cell 118 [code] · metadata

baseline L844 → branch L2024

```diff
- # %%
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c81"></a>
### C81 · cell 118 [code] · code

baseline L846 → branch L2026

```diff
- co2_drop = co2[co2['Avg'] > 0]
+ co2_drop = co2.filter(pl.col('Avg') > 0)
```

**Why:** Boolean-mask indexing → `filter`.
**Output:** differs: no row labels, so the dropped row is no longer visible as a gap in the index. Same 731 surviving rows.

<a id="c82"></a>
### C82 · cell 119 [markdown] · tab-twins

baseline L849 → branch L2029

```diff
+ # %% [markdown]
+ # <!-- tab-twins:begin 613b57a2 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # 1. Drop missing values
+ # co2_drop = co2.filter(pl.col('Avg') > 0)
+ # co2_drop.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 7)
+ # ┌──────┬─────┬─────────┬────────┬────────┬────────┬──────┐
+ # │ Yr   ┆ Mo  ┆ DecDate ┆ Avg    ┆ Int    ┆ Trend  ┆ Days │
+ # │ ---  ┆ --- ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---  │
+ # │ i64  ┆ i64 ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ i64  │
+ # ╞══════╪═════╪═════════╪════════╪════════╪════════╪══════╡
+ # │ 1958 ┆ 3   ┆ 1958.21 ┆ 315.71 ┆ 315.71 ┆ 314.62 ┆ -1   │
+ # │ 1958 ┆ 4   ┆ 1958.29 ┆ 317.45 ┆ 317.45 ┆ 315.29 ┆ -1   │
+ # │ 1958 ┆ 5   ┆ 1958.38 ┆ 317.50 ┆ 317.50 ┆ 314.71 ┆ -1   │
+ # │ 1958 ┆ 7   ┆ 1958.54 ┆ 315.86 ┆ 315.86 ┆ 314.98 ┆ -1   │
+ # │ 1958 ┆ 8   ┆ 1958.62 ┆ 314.93 ┆ 314.93 ┆ 315.94 ┆ -1   │
+ # └──────┴─────┴─────────┴────────┴────────┴────────┴──────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # 1. Drop missing values
+ # co2_drop = co2[co2['Avg'] > 0]
+ # co2_drop.head()
+ # ```
+ #
+ # ```text
+ #      Yr  Mo  DecDate    Avg    Int  Trend  Days
+ # 0  1958   3  1958.21 315.71 315.71 314.62    -1
+ # 1  1958   4  1958.29 317.45 317.45 315.29    -1
+ # 2  1958   5  1958.38 317.50 317.50 314.71    -1
+ … 7 more lines
```

**Why:** Tab-twins block for cell `613b57a2`.
**Output:** differs: rendering and the missing index. Panes describe the same operation.

<a id="c83"></a>
### C83 · cell 120 [code] · code

baseline L850 → branch L2077

```diff
- # 2. Replace NaN with -99.99
- co2_NA = co2.replace(-99.99, np.nan)
- co2_NA.head()
+ # 2. Replace -99.99 with null
+ co2_null = co2.with_columns(pl.col(pl.Float64).replace(-99.99, None))
+ co2_null.head()
```

**Why:** Three things at once. `co2.replace(-99.99, np.nan)` → `with_columns(pl.col(pl.Float64).replace(-99.99, None))`, because the Polars form needs a column selector and the target is `null`, not `NaN`; the variable `co2_NA` → `co2_null`; and the comment `# 2. Replace NaN with -99.99` was corrected, since it described the reverse of what the line does. That comment is CONTRADICTIONS §A8 #2, **pre-existing**, and correcting only the Polars side is exactly why §B1 removed this cell's twin — the two panes would have carried opposite comments under one heading. Verified: 7 nulls land in `Avg` and in no other column.
**Output:** differs: the missing entry prints as `null` where the baseline printed `NaN` — which is the section's point.

<a id="c84"></a>
### C84 · cell 122 [code] · metadata

baseline L869 → branch L2096

```diff
- # %%
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c85"></a>
### C85 · cell 122 [code] · code

baseline L871 → branch L2098

```diff
- co2_impute = co2.copy()
- co2_impute['Avg'] = co2['Int']
+ co2_impute = co2.with_columns(Avg = pl.col('Int'))
```

**Why:** `co2.copy()` plus a column assignment → a single `with_columns(Avg = pl.col('Int'))`. Polars frames are immutable, so the copy disappears rather than being translated.
**Output:** same values; Polars rendering.

<a id="c86"></a>
### C86 · cell 123 [markdown] · tab-twins

baseline L875 → branch L2101

```diff
+ # %% [markdown]
+ # <!-- tab-twins:begin 6667c947 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # 3. Use interpolated column which estimates missing Avg values
+ # co2_impute = co2.with_columns(Avg = pl.col('Int'))
+ # co2_impute.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 7)
+ # ┌──────┬─────┬─────────┬────────┬────────┬────────┬──────┐
+ # │ Yr   ┆ Mo  ┆ DecDate ┆ Avg    ┆ Int    ┆ Trend  ┆ Days │
+ # │ ---  ┆ --- ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---  │
+ # │ i64  ┆ i64 ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ i64  │
+ # ╞══════╪═════╪═════════╪════════╪════════╪════════╪══════╡
+ # │ 1958 ┆ 3   ┆ 1958.21 ┆ 315.71 ┆ 315.71 ┆ 314.62 ┆ -1   │
+ # │ 1958 ┆ 4   ┆ 1958.29 ┆ 317.45 ┆ 317.45 ┆ 315.29 ┆ -1   │
+ # │ 1958 ┆ 5   ┆ 1958.38 ┆ 317.50 ┆ 317.50 ┆ 314.71 ┆ -1   │
+ # │ 1958 ┆ 6   ┆ 1958.46 ┆ 317.10 ┆ 317.10 ┆ 314.85 ┆ -1   │
+ # │ 1958 ┆ 7   ┆ 1958.54 ┆ 315.86 ┆ 315.86 ┆ 314.98 ┆ -1   │
+ # └──────┴─────┴─────────┴────────┴────────┴────────┴──────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # # 3. Use interpolated column which estimates missing Avg values
+ # co2_impute = co2.copy()
+ # co2_impute['Avg'] = co2['Int']
+ # co2_impute.head()
+ # ```
+ #
+ # ```text
+ #      Yr  Mo  DecDate    Avg    Int  Trend  Days
+ # 0  1958   3  1958.21 315.71 315.71 314.62    -1
+ # 1  1958   4  1958.29 317.45 317.45 315.29    -1
+ … 7 more lines
```

**Why:** Tab-twins block for cell `6667c947`.
**Output:** differs: rendering only. Panes describe the same operation.

<a id="c87"></a>
### C87 · cell 124 [markdown] · prose · **REVIEW**

baseline L884 → branch L2157

```diff
- # #| fig-alt: "Three plots are shown with overall title 'Monthly Averages for 1958.' The first plot is 'Drop Missing' where the datapoints for x=6 and x=10 are not shown, but the datapoints are connected with lines. The second plot is 'Missing Set to NaN' where the lines are segmented from 3 to 5, 7 to 9, and 11 to 12. The third plot is 'Missing Interpolated' where we see the missing datapoints at x=6 and x=10 are now imputed following the shape of the other data."
+ # #| fig-alt: "Three plots are shown with overall title 'Monthly Averages for 1958.' The first plot is 'Drop Missing' where the datapoints for x=6 and x=10 are not shown, but the datapoints are connected with lines. The second plot is 'Missing Set to Null' where the lines are segmented from 3 to 5, 7 to 9, and 11 to 12. The third plot is 'Missing Interpolated' where we see the missing datapoints at x=6 and x=10 are now imputed following the shape of the other data."
```

**Why:** Dropdown mirror of the three-panel fig-alt: panel 2's title became "2. Missing Set to Null", so the alt text follows it. Mirror verified identical to code cell `7f3ea034`.
**Verdict:** necessary

<a id="c88"></a>
### C88 · cell 124: results of plotting data in 1958 · prose · **REVIEW**

baseline L896 → branch L2169

```diff
- #     return data[data["Yr"] == 1958]
+ #     return data.filter(pl.col("Yr") == 1958)
```

**Why:** Dropdown mirror: `data[data['Yr'] == 1958]` → `data.filter(pl.col('Yr') == 1958)`. (The helper still ignores its `year` parameter and hardcodes 1958 — inherited from the pandas original and deliberately left alone, per CONVERSIONS.md.)
**Verdict:** necessary

<a id="c89"></a>
### C89 · cell 124: you may see more next week; focus on output for now · prose · **REVIEW**

baseline L904 → branch L2177

```diff
- # line_and_points(data_year(co2_NA, year), axes[1], title="2. Missing Set to NaN")
+ # line_and_points(data_year(co2_null, year), axes[1], title="2. Missing Set to Null")
```

**Why:** Dropdown mirror: `co2_NA` → `co2_null` and the panel title "2. Missing Set to NaN" → "2. Missing Set to Null", both following the rename at C83.
**Verdict:** necessary

<a id="c90"></a>
### C90 · cell 125 [code] · code

baseline L913 → branch L2186

```diff
- #| fig-alt: "Three plots are shown with overall title 'Monthly Averages for 1958.' The first plot is 'Drop Missing' where the datapoints for x=6 and x=10 are not shown, but the datapoints are connected with lines. The second plot is 'Missing Set to NaN' where the lines are segmented from 3 to 5, 7 to 9, and 11 to 12. The third plot is 'Missing Interpolated' where we see the missing datapoints at x=6 and x=10 are now imputed following the shape of the other data."
+ #| fig-alt: "Three plots are shown with overall title 'Monthly Averages for 1958.' The first plot is 'Drop Missing' where the datapoints for x=6 and x=10 are not shown, but the datapoints are connected with lines. The second plot is 'Missing Set to Null' where the lines are segmented from 3 to 5, 7 to 9, and 11 to 12. The third plot is 'Missing Interpolated' where we see the missing datapoints at x=6 and x=10 are now imputed following the shape of the other data."
```

**Why:** The code cell's copy of the alt text mirrored at C87.
**Output:** same three panels; only the middle panel's description changed.

<a id="c91"></a>
### C91 · cell 125 [code] · code

baseline L925 → branch L2198

```diff
-     return data[data["Yr"] == 1958]
+     return data.filter(pl.col("Yr") == 1958)
```

**Why:** Boolean-mask indexing → `filter` inside the `data_year` helper.
**Output:** same twelve rows for 1958 in each of the three frames.

<a id="c92"></a>
### C92 · cell 125 [code] · code

baseline L933 → branch L2206

```diff
- line_and_points(data_year(co2_NA, year), axes[1], title="2. Missing Set to NaN")
+ line_and_points(data_year(co2_null, year), axes[1], title="2. Missing Set to Null")
```

**Why:** `co2_NA` → `co2_null` and the panel title, matching C83 and C89.
**Output:** differs: the middle panel is titled "2. Missing Set to Null". The plotted data is unchanged — a Polars `null` reaches matplotlib as a gap exactly as `NaN` did, so panel 2 is still segmented at months 6 and 10.

<a id="c93"></a>
### C93 · cell 128: Presenting the Data: A Discussion on Data Granularity · prose · **REVIEW**

baseline L988 → branch L2261

```diff
- # co2_year = co2_impute.groupby('Yr').mean()
+ # co2_year = co2_impute.group_by('Yr').mean().sort('Yr')
```

**Why:** Dropdown mirror: `groupby('Yr').mean()` → `group_by('Yr').mean().sort('Yr')`. Polars gives no group-order guarantee, so the explicit sort is required rather than cosmetic pandas-matching. Mirror verified identical to code cell `c57fa60e`.
**Verdict:** necessary

<a id="c94"></a>
### C94 · cell 129 [code] · code

baseline L996 → branch L2269

```diff
- co2_year = co2_impute.groupby('Yr').mean()
+ co2_year = co2_impute.group_by('Yr').mean().sort('Yr')
```

**Why:** The code cell that C93 mirrors.
**Output:** differs: `Yr` comes back as an ordinary column rather than the index. Same 62 rows, same means; the explicit sort makes the printed order deterministic.

<a id="c95"></a>
### C95 · `pl.read_csv("data/elections.csv").head(5)` · output

committed output

```diff
- [text]    Year          Candidate                  Party  Popular vote Result     %
- [text] 0  1824     Andrew Jackson  Democratic-Republican        151271   loss 57.21
- [text] 1  1824  John Quincy Adams  Democratic-Republican        113142    win 42.79
- [text] 2  1828     Andrew Jackson             Democratic        642806    win 56.20
- [text] 3  1828  John Quincy Adams    National Republican        500897   loss 43.80
- [text] 4  1832     Andrew Jackson             Democratic        702735    win 54.57
+ [text] shape: (5, 6)
+ [text] ┌──────┬───────────────────┬───────────────────────┬──────────────┬────────┬───────┐
+ [text] │ Year ┆ Candidate         ┆ Party                 ┆ Popular vote ┆ Result ┆ %     │
+ [text] │ ---  ┆ ---               ┆ ---                   ┆ ---          ┆ ---    ┆ ---   │
+ [text] │ i64  ┆ str               ┆ str                   ┆ i64          ┆ str    ┆ f64   │
+ [text] ╞══════╪═══════════════════╪═══════════════════════╪══════════════╪════════╪═══════╡
+ [text] │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republican ┆ 151271       ┆ loss   ┆ 57.21 │
+ [text] │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican ┆ 113142       ┆ win    ┆ 42.79 │
+ [text] │ 1828 ┆ Andrew Jackson    ┆ Democratic            ┆ 642806       ┆ win    ┆ 56.20 │
+ [text] │ 1828 ┆ John Quincy Adams ┆ National Republican   ┆ 500897       ┆ loss   ┆ 43.80 │
+ [text] │ 1832 ┆ Andrew Jackson    ┆ Democratic            ┆ 702735       ┆ win    ┆ 54.57 │
+ [text] └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────┘
```

**Why:** Regenerated from the Polars read.
**Reader sees:** equivalent — same five rows, same six columns, same values. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C5, whose Polars pane is byte-identical to it (verified).

<a id="c96"></a>
### C96 · `pl.read_csv("data/elections.txt", separator='\t').head(3)` · output

committed output

```diff
- [text]    Year          Candidate                  Party  Popular vote Result     %
- [text] 0  1824     Andrew Jackson  Democratic-Republican        151271   loss 57.21
- [text] 1  1824  John Quincy Adams  Democratic-Republican        113142    win 42.79
- [text] 2  1828     Andrew Jackson             Democratic        642806    win 56.20
+ [text] shape: (3, 6)
+ [text] ┌──────┬───────────────────┬───────────────────────┬──────────────┬────────┬───────┐
+ [text] │ Year ┆ Candidate         ┆ Party                 ┆ Popular vote ┆ Result ┆ %     │
+ [text] │ ---  ┆ ---               ┆ ---                   ┆ ---          ┆ ---    ┆ ---   │
+ [text] │ i64  ┆ str               ┆ str                   ┆ i64          ┆ str    ┆ f64   │
+ [text] ╞══════╪═══════════════════╪═══════════════════════╪══════════════╪════════╪═══════╡
+ [text] │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republican ┆ 151271       ┆ loss   ┆ 57.21 │
+ [text] │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican ┆ 113142       ┆ win    ┆ 42.79 │
+ [text] │ 1828 ┆ Andrew Jackson    ┆ Democratic            ┆ 642806       ┆ win    ┆ 56.20 │
+ [text] └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────┘
```

**Why:** Regenerated from the Polars read.
**Reader sees:** equivalent — same three rows and values. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C8, whose Polars pane is byte-identical to it (verified).

<a id="c97"></a>
### C97 · `pl.read_json('data/elections.json').head(3)` · output

committed output

```diff
- [text]    Year          Candidate                  Party  Popular vote Result     %
- [text] 0  1824     Andrew Jackson  Democratic-Republican        151271   loss 57.21
- [text] 1  1824  John Quincy Adams  Democratic-Republican        113142    win 42.79
- [text] 2  1828     Andrew Jackson             Democratic        642806    win 56.20
+ [text] shape: (3, 6)
+ [text] ┌──────┬───────────────────┬───────────────────────┬──────────────┬────────┬───────┐
+ [text] │ Year ┆ Candidate         ┆ Party                 ┆ Popular vote ┆ Result ┆ %     │
+ [text] │ ---  ┆ ---               ┆ ---                   ┆ ---          ┆ ---    ┆ ---   │
+ [text] │ i64  ┆ str               ┆ str                   ┆ i64          ┆ str    ┆ f64   │
+ [text] ╞══════╪═══════════════════╪═══════════════════════╪══════════════╪════════╪═══════╡
+ [text] │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republican ┆ 151271       ┆ loss   ┆ 57.21 │
+ [text] │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican ┆ 113142       ┆ win    ┆ 42.79 │
+ [text] │ 1828 ┆ Andrew Jackson    ┆ Democratic            ┆ 642806       ┆ win    ┆ 56.20 │
+ [text] └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────┘
```

**Why:** Regenerated from the Polars read.
**Reader sees:** equivalent — same three rows and values. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C10, whose Polars pane is byte-identical to it (verified).

<a id="c98"></a>
### C98 · `pl.read_json(congress_file)` · output

committed output

```diff
- [error] ValueError: Mixing dicts with non-Series may lead to ambiguous ordering.
+ [text] shape: (1, 3)
+ [text] ┌─────────────────────────────────┬────────────┬─────────────────────────────┐
+ [text] │ members                         ┆ pagination ┆ request                     │
+ [text] │ ---                             ┆ ---        ┆ ---                         │
+ [text] │ list[struct[9]]                 ┆ struct[1]  ┆ struct[2]                   │
+ [text] ╞═════════════════════════════════╪════════════╪═════════════════════════════╡
+ [text] │ [{"T000491",{"Image courtesy o… ┆ {54}       ┆ {"application/json","json"} │
+ [text] └─────────────────────────────────┴────────────┴─────────────────────────────┘
```

**Why:** `pl.read_json` succeeds on the congress file where `pd.read_json` raised.
**Reader sees:** changed: the chapter's only committed error output is gone, replaced by a (1, 3) frame whose single row holds all 54 members. The cell is hidden, so what the reader actually meets is the tab-set at C14–C16, where the pandas pane still carries the `ValueError`. This is the chapter's largest single change and the one AGENTS.md hard rule 6 names; it ships only on the strength of the `eda: resolved_errors` allowlist entry and the staff decision in CONVERSIONS.md.

<a id="c99"></a>
### C99 · `congress_df = pl.DataFrame(congress_json['members'])` · output

committed output

```diff
- [text]   bioguideId                                          depiction  district  \
- [text] 0    T000491  {'attribution': 'Image courtesy of the Member'...     45.00
- [text] 1    M001241  {'attribution': 'Image courtesy of the Member'...     47.00
- [text] 2    K000400  {'attribution': 'Image courtesy of the Member'...     37.00
- [text] 3    G000598  {'attribution': 'Image courtesy of the Member'...     42.00
- [text] 4    K000397  {'attribution': 'Image courtesy of the Member'...     40.00
- [text]
- [text]                     name   partyName       state  \
- [text] 0            Tran, Derek  Democratic  California
- [text] 1              Min, Dave  Democratic  California
- [text] 2  Kamlager-Dove, Sydney  Democratic  California
- [text] 3         Garcia, Robert  Democratic  California
- [text] 4             Kim, Young  Republican  California
- [text]
- [text]                                                terms            updateDate  \
- [text] 0  {'item': [{'chamber': 'House of Representative...  2025-01-21T18:00:52Z
- [text] 1  {'item': [{'chamber': 'House of Representative...  2025-01-21T18:00:52Z
- [text] 2  {'item': [{'chamber': 'House of Representative...  2025-01-21T18:00:52Z
- [text] 3  {'item': [{'chamber': 'House of Representative...  2025-01-21T18:00:52Z
- [text] 4  {'item': [{'chamber': 'House of Representative...  2025-01-21T18:00:52Z
- [text]
- [text]                                                  url
- [text] 0  https://api.congress.gov/v3/member/T000491?for...
- [text] 1  https://api.congress.gov/v3/member/M001241?for...
- [text] 2  https://api.congress.gov/v3/member/K000400?for...
- [text] 3  https://api.congress.gov/v3/member/G000598?for...
- [text] 4  https://api.congress.gov/v3/member/K000397?for...
+ [text] shape: (5, 9)
+ [text] ┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
+ [text] │ bioguide ┆ depictio ┆ district ┆ name     ┆ partyNam ┆ state    ┆ terms    ┆ updateDa ┆ url      │
+ [text] │ Id       ┆ n        ┆ ---      ┆ ---      ┆ e        ┆ ---      ┆ ---      ┆ te       ┆ ---      │
+ [text] │ ---      ┆ ---      ┆ i64      ┆ str      ┆ ---      ┆ str      ┆ struct[1 ┆ ---      ┆ str      │
+ [text] │ str      ┆ struct[2 ┆          ┆          ┆ str      ┆          ┆ ]        ┆ str      ┆          │
+ [text] │          ┆ ]        ┆          ┆          ┆          ┆          ┆          ┆          ┆          │
+ [text] ╞══════════╪══════════╪══════════╪══════════╪══════════╪══════════╪══════════╪══════════╪══════════╡
+ [text] │ T000491  ┆ {"Image  ┆ 45       ┆ Tran,    ┆ Democrat ┆ Californ ┆ {[{"Hous ┆ 2025-01- ┆ https:// │
+ [text] │          ┆ courtesy ┆          ┆ Derek    ┆ ic       ┆ ia       ┆ e of Rep ┆ 21T18:00 ┆ api.cong │
+ [text] │          ┆ of the   ┆          ┆          ┆          ┆          ┆ resentat ┆ :52Z     ┆ ress.gov │
+ [text] │          ┆ Member…  ┆          ┆          ┆          ┆          ┆ ives",…  ┆          ┆ /v3/me…  │
+ [text] │ M001241  ┆ {"Image  ┆ 47       ┆ Min,     ┆ Democrat ┆ Californ ┆ {[{"Hous ┆ 2025-01- ┆ https:// │
+ [text] │          ┆ courtesy ┆          ┆ Dave     ┆ ic       ┆ ia       ┆ e of Rep ┆ 21T18:00 ┆ api.cong │
+ [text] │          ┆ of the   ┆          ┆          ┆          ┆          ┆ resentat ┆ :52Z     ┆ ress.gov │
+ [text] │          ┆ Member…  ┆          ┆          ┆          ┆          ┆ ives",…  ┆          ┆ /v3/me…  │
+ [text] │ K000400  ┆ {"Image  ┆ 37       ┆ Kamlager ┆ Democrat ┆ Californ ┆ {[{"Hous ┆ 2025-01- ┆ https:// │
+ [text] │          ┆ courtesy ┆          ┆ -Dove,   ┆ ic       ┆ ia       ┆ e of Rep ┆ 21T18:00 ┆ api.cong │
+ [text] │          ┆ of the   ┆          ┆ Sydney   ┆          ┆          ┆ resentat ┆ :52Z     ┆ ress.gov │
+ [text] │          ┆ Member…  ┆          ┆          ┆          ┆          ┆ ives",…  ┆          ┆ /v3/me…  │
+ [text] │ G000598  ┆ {"Image  ┆ 42       ┆ Garcia,  ┆ Democrat ┆ Californ ┆ {[{"Hous ┆ 2025-01- ┆ https:// │
+ [text] │          ┆ courtesy ┆          ┆ Robert   ┆ ic       ┆ ia       ┆ e of Rep ┆ 21T18:00 ┆ api.cong │
+ [text] │          ┆ of the   ┆          ┆          ┆          ┆          ┆ resentat ┆ :52Z     ┆ ress.gov │
+ [text] │          ┆ Member…  ┆          ┆          ┆          ┆          ┆ ives",…  ┆          ┆ /v3/me…  │
+ [text] │ K000397  ┆ {"Image  ┆ 40       ┆ Kim,     ┆ Republic ┆ Californ ┆ {[{"Hous ┆ 2025-01- ┆ https:// │
+ [text] │          ┆ courtesy ┆          ┆ Young    ┆ an       ┆ ia       ┆ e of Rep ┆ 21T18:00 ┆ api.cong │
+ [text] │          ┆ of the   ┆          ┆          ┆          ┆          ┆ resentat ┆ :52Z     ┆ ress.gov │
+ [text] │          ┆ Member…  ┆          ┆          ┆          ┆          ┆ ives",…  ┆          ┆ /v3/me…  │
+ [text] └──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
```

**Why:** Regenerated from `pl.DataFrame(congress_json['members'])`.
**Reader sees:** equivalent — same five members and nine fields; nested dicts print as structs rather than truncated Python dicts. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C19, whose Polars pane is byte-identical to it (verified).

<a id="c100"></a>
### C100 · `calls = pl.read_csv("data/Berkeley_PD_-_Calls_for_Service.csv")` · output

committed output

```diff
- [text]      CASENO                   OFFENSE                 EVENTDT EVENTTM  \
- [text] 0  21014296  THEFT MISD. (UNDER $950)  04/01/2021 12:00:00 AM   10:58
- [text] 1  21014391  THEFT MISD. (UNDER $950)  04/01/2021 12:00:00 AM   10:38
- [text] 2  21090494  THEFT MISD. (UNDER $950)  04/19/2021 12:00:00 AM   12:15
- [text] 3  21090204  THEFT FELONY (OVER $950)  02/13/2021 12:00:00 AM   17:00
- [text] 4  21090179             BURGLARY AUTO  02/08/2021 12:00:00 AM    6:20
- [text]
- [text]              CVLEGEND  CVDOW                InDbDate  \
- [text] 0             LARCENY      4  06/15/2021 12:00:00 AM
- [text] 1             LARCENY      4  06/15/2021 12:00:00 AM
- [text] 2             LARCENY      1  06/15/2021 12:00:00 AM
- [text] 3             LARCENY      6  06/15/2021 12:00:00 AM
- [text] 4  BURGLARY - VEHICLE      1  06/15/2021 12:00:00 AM
- [text]
- [text]                                       Block_Location                BLKADDR  \
- [text] 0           Berkeley, CA\r\n(37.869058, -122.270455)                    NaN
- [text] 1           Berkeley, CA\r\n(37.869058, -122.270455)                    NaN
- [text] 2  2100 BLOCK HASTE ST\r\nBerkeley, CA\r\n(37.864...    2100 BLOCK HASTE ST
- [text] 3  2600 BLOCK WARRING ST\r\nBerkeley, CA\r\n(37.8...  2600 BLOCK WARRING ST
- [text] 4  2700 BLOCK GARBER ST\r\nBerkeley, CA\r\n(37.86...   2700 BLOCK GARBER ST
- [text]
- [text]        City State
- [text] 0  Berkeley    CA
- [text] 1  Berkeley    CA
- [text] 2  Berkeley    CA
- [text] 3  Berkeley    CA
- [text] 4  Berkeley    CA
+ [text] shape: (5, 11)
+ [text] ┌─────────┬─────────┬────────┬────────┬────────┬───────┬────────┬────────┬────────┬────────┬───────┐
+ [text] │ CASENO  ┆ OFFENSE ┆ EVENTD ┆ EVENTT ┆ CVLEGE ┆ CVDOW ┆ InDbDa ┆ Block_ ┆ BLKADD ┆ City   ┆ State │
+ [text] │ ---     ┆ ---     ┆ T      ┆ M      ┆ ND     ┆ ---   ┆ te     ┆ Locati ┆ R      ┆ ---    ┆ ---   │
+ [text] │ i64     ┆ str     ┆ ---    ┆ ---    ┆ ---    ┆ i64   ┆ ---    ┆ on     ┆ ---    ┆ str    ┆ str   │
+ [text] │         ┆         ┆ str    ┆ str    ┆ str    ┆       ┆ str    ┆ ---    ┆ str    ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ str    ┆        ┆        ┆       │
+ [text] ╞═════════╪═════════╪════════╪════════╪════════╪═══════╪════════╪════════╪════════╪════════╪═══════╡
+ [text] │ 2101429 ┆ THEFT   ┆ 04/01/ ┆ 10:58  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ Berkel ┆ null   ┆ Berkel ┆ CA    │
+ [text] │ 6       ┆ MISD.   ┆ 2021   ┆        ┆ Y      ┆       ┆ 2021   ┆ ey, CA ┆        ┆ ey     ┆       │
+ [text] │         ┆ (UNDER  ┆ 12:00: ┆        ┆        ┆       ┆ 12:00: ┆ (37.86 ┆        ┆        ┆       │
+ [text] │         ┆ $950)   ┆ 00 AM  ┆        ┆        ┆       ┆ 00 AM  ┆ 9058,  ┆        ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ -122.… ┆        ┆        ┆       │
+ [text] │ 2101439 ┆ THEFT   ┆ 04/01/ ┆ 10:38  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ Berkel ┆ null   ┆ Berkel ┆ CA    │
+ [text] │ 1       ┆ MISD.   ┆ 2021   ┆        ┆ Y      ┆       ┆ 2021   ┆ ey, CA ┆        ┆ ey     ┆       │
+ [text] │         ┆ (UNDER  ┆ 12:00: ┆        ┆        ┆       ┆ 12:00: ┆ (37.86 ┆        ┆        ┆       │
+ [text] │         ┆ $950)   ┆ 00 AM  ┆        ┆        ┆       ┆ 00 AM  ┆ 9058,  ┆        ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ -122.… ┆        ┆        ┆       │
+ [text] │ 2109049 ┆ THEFT   ┆ 04/19/ ┆ 12:15  ┆ LARCEN ┆ 1     ┆ 06/15/ ┆ 2100   ┆ 2100   ┆ Berkel ┆ CA    │
+ [text] │ 4       ┆ MISD.   ┆ 2021   ┆        ┆ Y      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ [text] │         ┆ (UNDER  ┆ 12:00: ┆        ┆        ┆       ┆ 12:00: ┆ HASTE  ┆ HASTE  ┆        ┆       │
+ [text] │         ┆ $950)   ┆ 00 AM  ┆        ┆        ┆       ┆ 00 AM  ┆ ST     ┆ ST     ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey, …  ┆        ┆        ┆       │
+ [text] │ 2109020 ┆ THEFT   ┆ 02/13/ ┆ 17:00  ┆ LARCEN ┆ 6     ┆ 06/15/ ┆ 2600   ┆ 2600   ┆ Berkel ┆ CA    │
+ [text] │ 4       ┆ FELONY  ┆ 2021   ┆        ┆ Y      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ [text] │         ┆ (OVER   ┆ 12:00: ┆        ┆        ┆       ┆ 12:00: ┆ WARRIN ┆ WARRIN ┆        ┆       │
+ [text] │         ┆ $950)   ┆ 00 AM  ┆        ┆        ┆       ┆ 00 AM  ┆ G ST   ┆ G ST   ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey…    ┆        ┆        ┆       │
+ [text] │ 2109017 ┆ BURGLAR ┆ 02/08/ ┆ 6:20   ┆ BURGLA ┆ 1     ┆ 06/15/ ┆ 2700   ┆ 2700   ┆ Berkel ┆ CA    │
+ [text] │ 9       ┆ Y AUTO  ┆ 2021   ┆        ┆ RY -   ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ [text] │         ┆         ┆ 12:00: ┆        ┆ VEHICL ┆       ┆ 12:00: ┆ GARBER ┆ GARBER ┆        ┆       │
+ [text] │         ┆         ┆ 00 AM  ┆        ┆ E      ┆       ┆ 00 AM  ┆ ST     ┆ ST     ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey,…   ┆        ┆        ┆       │
+ [text] └─────────┴─────────┴────────┴────────┴────────┴───────┴────────┴────────┴────────┴────────┴───────┘
```

**Why:** Regenerated from the Polars read.
**Reader sees:** equivalent — same 5×11 head; `BLKADDR`'s blanks print as `null` rather than `NaN`. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C25, whose Polars pane is byte-identical to it (verified).

<a id="c101"></a>
### C101 · `calls = calls.with_columns(` · output

committed output

```diff
- [text]      CASENO                   OFFENSE    EVENTDT EVENTTM            CVLEGEND  \
- [text] 0  21014296  THEFT MISD. (UNDER $950) 2021-04-01   10:58             LARCENY
- [text] 1  21014391  THEFT MISD. (UNDER $950) 2021-04-01   10:38             LARCENY
- [text] 2  21090494  THEFT MISD. (UNDER $950) 2021-04-19   12:15             LARCENY
- [text] 3  21090204  THEFT FELONY (OVER $950) 2021-02-13   17:00             LARCENY
- [text] 4  21090179             BURGLARY AUTO 2021-02-08    6:20  BURGLARY - VEHICLE
- [text]
- [text]    CVDOW                InDbDate  \
- [text] 0      4  06/15/2021 12:00:00 AM
- [text] 1      4  06/15/2021 12:00:00 AM
- [text] 2      1  06/15/2021 12:00:00 AM
- [text] 3      6  06/15/2021 12:00:00 AM
- [text] 4      1  06/15/2021 12:00:00 AM
- [text]
- [text]                                       Block_Location                BLKADDR  \
- [text] 0           Berkeley, CA\r\n(37.869058, -122.270455)                    NaN
- [text] 1           Berkeley, CA\r\n(37.869058, -122.270455)                    NaN
- [text] 2  2100 BLOCK HASTE ST\r\nBerkeley, CA\r\n(37.864...    2100 BLOCK HASTE ST
- [text] 3  2600 BLOCK WARRING ST\r\nBerkeley, CA\r\n(37.8...  2600 BLOCK WARRING ST
- [text] 4  2700 BLOCK GARBER ST\r\nBerkeley, CA\r\n(37.86...   2700 BLOCK GARBER ST
- [text]
- [text]        City State
- [text] 0  Berkeley    CA
- [text] 1  Berkeley    CA
- [text] 2  Berkeley    CA
- [text] 3  Berkeley    CA
- [text] 4  Berkeley    CA
+ [text] shape: (5, 11)
+ [text] ┌─────────┬─────────┬────────┬────────┬────────┬───────┬────────┬────────┬────────┬────────┬───────┐
+ [text] │ CASENO  ┆ OFFENSE ┆ EVENTD ┆ EVENTT ┆ CVLEGE ┆ CVDOW ┆ InDbDa ┆ Block_ ┆ BLKADD ┆ City   ┆ State │
+ [text] │ ---     ┆ ---     ┆ T      ┆ M      ┆ ND     ┆ ---   ┆ te     ┆ Locati ┆ R      ┆ ---    ┆ ---   │
+ [text] │ i64     ┆ str     ┆ ---    ┆ ---    ┆ ---    ┆ i64   ┆ ---    ┆ on     ┆ ---    ┆ str    ┆ str   │
+ [text] │         ┆         ┆ dateti ┆ str    ┆ str    ┆       ┆ str    ┆ ---    ┆ str    ┆        ┆       │
+ [text] │         ┆         ┆ me[μs] ┆        ┆        ┆       ┆        ┆ str    ┆        ┆        ┆       │
+ [text] ╞═════════╪═════════╪════════╪════════╪════════╪═══════╪════════╪════════╪════════╪════════╪═══════╡
+ [text] │ 2101429 ┆ THEFT   ┆ 2021-0 ┆ 10:58  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ Berkel ┆ null   ┆ Berkel ┆ CA    │
+ [text] │ 6       ┆ MISD.   ┆ 4-01   ┆        ┆ Y      ┆       ┆ 2021   ┆ ey, CA ┆        ┆ ey     ┆       │
+ [text] │         ┆ (UNDER  ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ (37.86 ┆        ┆        ┆       │
+ [text] │         ┆ $950)   ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ 9058,  ┆        ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ -122.… ┆        ┆        ┆       │
+ [text] │ 2101439 ┆ THEFT   ┆ 2021-0 ┆ 10:38  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ Berkel ┆ null   ┆ Berkel ┆ CA    │
+ [text] │ 1       ┆ MISD.   ┆ 4-01   ┆        ┆ Y      ┆       ┆ 2021   ┆ ey, CA ┆        ┆ ey     ┆       │
+ [text] │         ┆ (UNDER  ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ (37.86 ┆        ┆        ┆       │
+ [text] │         ┆ $950)   ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ 9058,  ┆        ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ -122.… ┆        ┆        ┆       │
+ [text] │ 2109049 ┆ THEFT   ┆ 2021-0 ┆ 12:15  ┆ LARCEN ┆ 1     ┆ 06/15/ ┆ 2100   ┆ 2100   ┆ Berkel ┆ CA    │
+ [text] │ 4       ┆ MISD.   ┆ 4-19   ┆        ┆ Y      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ [text] │         ┆ (UNDER  ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ HASTE  ┆ HASTE  ┆        ┆       │
+ [text] │         ┆ $950)   ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ ST     ┆ ST     ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey, …  ┆        ┆        ┆       │
+ [text] │ 2109020 ┆ THEFT   ┆ 2021-0 ┆ 17:00  ┆ LARCEN ┆ 6     ┆ 06/15/ ┆ 2600   ┆ 2600   ┆ Berkel ┆ CA    │
+ [text] │ 4       ┆ FELONY  ┆ 2-13   ┆        ┆ Y      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ [text] │         ┆ (OVER   ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ WARRIN ┆ WARRIN ┆        ┆       │
+ [text] │         ┆ $950)   ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ G ST   ┆ G ST   ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey…    ┆        ┆        ┆       │
+ [text] │ 2109017 ┆ BURGLAR ┆ 2021-0 ┆ 6:20   ┆ BURGLA ┆ 1     ┆ 06/15/ ┆ 2700   ┆ 2700   ┆ Berkel ┆ CA    │
+ [text] │ 9       ┆ Y AUTO  ┆ 2-08   ┆        ┆ RY -   ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ [text] │         ┆         ┆ 00:00: ┆        ┆ VEHICL ┆       ┆ 12:00: ┆ GARBER ┆ GARBER ┆        ┆       │
+ [text] │         ┆         ┆ 00     ┆        ┆ E      ┆       ┆ 00 AM  ┆ ST     ┆ ST     ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey,…   ┆        ┆        ┆       │
+ [text] └─────────┴─────────┴────────┴────────┴────────┴───────┴────────┴────────┴────────┴────────┴───────┘
```

**Why:** Regenerated after the `EVENTDT` parse moved to `.str.to_datetime`.
**Reader sees:** equivalent — same parsed dates, dtype label `datetime[μs]`. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C28, whose Polars pane is byte-identical to it (verified).

<a id="c102"></a>
### C102 · `calls["EVENTDT"].dt.month().head()` · output

committed output

```diff
- [text] 0    4
- [text] 1    4
- [text] 2    4
- [text] 3    2
- [text] 4    2
- [text] Name: EVENTDT, dtype: int32
+ [text] shape: (10,)
+ [text] Series: 'EVENTDT' [i8]
+ [text] [
+ [text] 	4
+ [text] 	4
+ [text] 	4
+ [text] 	2
+ [text] 	2
+ [text] 	12
+ [text] 	5
+ [text] 	3
+ [text] 	3
+ [text] 	3
+ [text] ]
```

**Why:** Regenerated from `.dt.month()`.
**Reader sees:** changed: ten values print instead of five, because `Series.head()` defaults to 10 in Polars. The first five are identical. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C30, whose Polars pane is byte-identical to it (verified).

<a id="c103"></a>
### C103 · `calls["EVENTDT"].dt.weekday().head()` · output

committed output

```diff
- [text] 0    3
- [text] 1    3
- [text] 2    0
- [text] 3    5
- [text] 4    0
- [text] Name: EVENTDT, dtype: int32
+ [text] shape: (10,)
+ [text] Series: 'EVENTDT' [i8]
+ [text] [
+ [text] 	4
+ [text] 	4
+ [text] 	1
+ [text] 	6
+ [text] 	1
+ [text] 	6
+ [text] 	1
+ [text] 	7
+ [text] 	3
+ [text] 	3
+ [text] ]
```

**Why:** Regenerated from `.dt.weekday()`.
**Reader sees:** changed: values shift from 0–6 to 1–7 (`3,3,0,5,0` → `4,4,1,6,1`) and ten rows print instead of five. **This cell is not hidden and has no twin** — §B1 removed it — so the Polars numbering ships alone, under prose that now states the Monday = 1 convention. Verified against the dataset's own `CVDOW` column: equal on every row except Sundays.

<a id="c104"></a>
### C104 · `calls.sort("EVENTDT").head()` · output

committed output

```diff
- [text]         CASENO                   OFFENSE    EVENTDT EVENTTM  \
- [text] 2513  20057398       BURGLARY COMMERCIAL 2020-12-17   16:05
- [text] 624   20057207     ASSAULT/BATTERY MISD. 2020-12-17   16:50
- [text] 154   20092214           THEFT FROM AUTO 2020-12-17   18:30
- [text] 659   20057324  THEFT MISD. (UNDER $950) 2020-12-17   15:44
- [text] 993   20057573      BURGLARY RESIDENTIAL 2020-12-17   22:15
- [text]
- [text]                     CVLEGEND  CVDOW                InDbDate  \
- [text] 2513   BURGLARY - COMMERCIAL      4  06/15/2021 12:00:00 AM
- [text] 624                  ASSAULT      4  06/15/2021 12:00:00 AM
- [text] 154   LARCENY - FROM VEHICLE      4  06/15/2021 12:00:00 AM
- [text] 659                  LARCENY      4  06/15/2021 12:00:00 AM
- [text] 993   BURGLARY - RESIDENTIAL      4  06/15/2021 12:00:00 AM
- [text]
- [text]                                          Block_Location  \
- [text] 2513  600 BLOCK GILMAN ST\r\nBerkeley, CA\r\n(37.878...
- [text] 624   2100 BLOCK SHATTUCK AVE\r\nBerkeley, CA\r\n(37...
- [text] 154   800 BLOCK SHATTUCK AVE\r\nBerkeley, CA\r\n(37....
- [text] 659   1800 BLOCK 4TH ST\r\nBerkeley, CA\r\n(37.86988...
- [text] 993   1700 BLOCK STUART ST\r\nBerkeley, CA\r\n(37.85...
- [text]
- [text]                       BLKADDR      City State
- [text] 2513      600 BLOCK GILMAN ST  Berkeley    CA
- [text] 624   2100 BLOCK SHATTUCK AVE  Berkeley    CA
- [text] 154    800 BLOCK SHATTUCK AVE  Berkeley    CA
- [text] 659         1800 BLOCK 4TH ST  Berkeley    CA
- [text] 993      1700 BLOCK STUART ST  Berkeley    CA
+ [text] shape: (5, 11)
+ [text] ┌─────────┬─────────┬────────┬────────┬────────┬───────┬────────┬────────┬────────┬────────┬───────┐
+ [text] │ CASENO  ┆ OFFENSE ┆ EVENTD ┆ EVENTT ┆ CVLEGE ┆ CVDOW ┆ InDbDa ┆ Block_ ┆ BLKADD ┆ City   ┆ State │
+ [text] │ ---     ┆ ---     ┆ T      ┆ M      ┆ ND     ┆ ---   ┆ te     ┆ Locati ┆ R      ┆ ---    ┆ ---   │
+ [text] │ i64     ┆ str     ┆ ---    ┆ ---    ┆ ---    ┆ i64   ┆ ---    ┆ on     ┆ ---    ┆ str    ┆ str   │
+ [text] │         ┆         ┆ dateti ┆ str    ┆ str    ┆       ┆ str    ┆ ---    ┆ str    ┆        ┆       │
+ [text] │         ┆         ┆ me[μs] ┆        ┆        ┆       ┆        ┆ str    ┆        ┆        ┆       │
+ [text] ╞═════════╪═════════╪════════╪════════╪════════╪═══════╪════════╪════════╪════════╪════════╪═══════╡
+ [text] │ 2009221 ┆ THEFT   ┆ 2020-1 ┆ 18:30  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ 800    ┆ 800    ┆ Berkel ┆ CA    │
+ [text] │ 4       ┆ FROM    ┆ 2-17   ┆        ┆ Y -    ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ [text] │         ┆ AUTO    ┆ 00:00: ┆        ┆ FROM   ┆       ┆ 12:00: ┆ SHATTU ┆ SHATTU ┆        ┆       │
+ [text] │         ┆         ┆ 00     ┆        ┆ VEHICL ┆       ┆ 00 AM  ┆ CK AVE ┆ CK AVE ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆ E      ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ e…     ┆        ┆        ┆       │
+ [text] │ 2005737 ┆ GUN/WEA ┆ 2020-1 ┆ 22:18  ┆ WEAPON ┆ 4     ┆ 06/15/ ┆ 6200   ┆ 6200   ┆ Berkel ┆ CA    │
+ [text] │ 3       ┆ PON     ┆ 2-17   ┆        ┆ S OFFE ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ [text] │         ┆         ┆ 00:00: ┆        ┆ NSE    ┆       ┆ 12:00: ┆ SAN    ┆ SAN    ┆        ┆       │
+ [text] │         ┆         ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ PABLO  ┆ PABLO  ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ AVE    ┆ AVE    ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berke… ┆        ┆        ┆       │
+ [text] │ 2005720 ┆ ASSAULT ┆ 2020-1 ┆ 16:50  ┆ ASSAUL ┆ 4     ┆ 06/15/ ┆ 2100   ┆ 2100   ┆ Berkel ┆ CA    │
+ [text] │ 7       ┆ /BATTER ┆ 2-17   ┆        ┆ T      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ [text] │         ┆ Y MISD. ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ SHATTU ┆ SHATTU ┆        ┆       │
+ [text] │         ┆         ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ CK AVE ┆ CK AVE ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ …      ┆        ┆        ┆       │
+ [text] │ 2005732 ┆ THEFT   ┆ 2020-1 ┆ 15:44  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ 1800   ┆ 1800   ┆ Berkel ┆ CA    │
+ [text] │ 4       ┆ MISD.   ┆ 2-17   ┆        ┆ Y      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ [text] │         ┆ (UNDER  ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ 4TH ST ┆ 4TH ST ┆        ┆       │
+ [text] │         ┆ $950)   ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ Berkel ┆        ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey,    ┆        ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ CA…    ┆        ┆        ┆       │
+ [text] │ 2005757 ┆ BURGLAR ┆ 2020-1 ┆ 22:15  ┆ BURGLA ┆ 4     ┆ 06/15/ ┆ 1700   ┆ 1700   ┆ Berkel ┆ CA    │
+ [text] │ 3       ┆ Y RESID ┆ 2-17   ┆        ┆ RY -   ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
+ [text] │         ┆ ENTIAL  ┆ 00:00: ┆        ┆ RESIDE ┆       ┆ 12:00: ┆ STUART ┆ STUART ┆        ┆       │
+ [text] │         ┆         ┆ 00     ┆        ┆ NTIAL  ┆       ┆ 00 AM  ┆ ST     ┆ ST     ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
+ [text] │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey,…   ┆        ┆        ┆       │
+ [text] └─────────┴─────────┴────────┴────────┴────────┴───────┴────────┴────────┴────────┴────────┴───────┘
```

**Why:** Regenerated from `calls.sort('EVENTDT').head()`.
**Reader sees:** changed: different records. Ten rows tie on the minimum timestamp (verified) and the two libraries break the tie differently, so Polars' head contains CASENO 20057373 where pandas' contains 20057398. Row labels are gone as well. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C32, whose Polars pane is byte-identical to it (verified).

<a id="c105"></a>
### C105 · `ili = pl.read_csv("data/flu/ILINet.csv", truncate_ragged_lines=True)` · output

committed output

```diff
- [text]                                                                                                                                                 PERCENTAGE OF VISITS FOR INFLUENZA-LIKE-ILLNESS REPORTED BY SENTINEL PROVIDERS
- [text] REGION TYPE REGION    YEAR WEEK % WEIGHTED ILI %UNWEIGHTED ILI AGE 0-4 AGE 25-49 AGE 25-64 AGE 5-24 AGE 50-64 AGE 65 ILITOTAL NUM. OF PROVIDERS                                     TOTAL PATIENTS
- [text] HHS Regions Region 1  2015 40   0.743302       0.684364        103     50        NaN       133      23        13     322      134                                                            47051
- [text]             Region 2  2015 40   1.03278        1.22475         547     294       NaN       528      123       95     1587     199                                                           129577
- [text]             Region 3  2015 40   1.2178         1.24313         401     419       NaN       625      144       81     1670     280                                                           134338
- [text]             Region 4  2015 40   1.01464        1.15781         486     231       NaN       613      99        75     1504     299                                                           129900
- [text] ...                                                                                                                                                                                            ...
- [text]             Region 6  2026 3    6.71907        6.40685         1189    1313      NaN       2393     451       375    5721     205                                                            89295
- [text]             Region 7  2026 3    5.70345        5.79518         518     722       NaN       1174     228       338    2980     164                                                            51422
- [text]             Region 8  2026 3    3.03915        3.08624         684     670       NaN       1000     246       289    2889     228                                                            93609
- [text]             Region 9  2026 3    4.85718        4.62364         2045    5863      NaN       4914     2552      3004   18378    402                                                           397479
- [text]             Region 10 2026 3    5.06699        4.91184         1462    1946      NaN       3526     700       793    8427     332                                                           171565
- [text]
- [text] [5381 rows x 1 columns]
+ [text] shape: (5_381, 1)
+ [text] ┌─────────────────────────────────┐
+ [text] │ PERCENTAGE OF VISITS FOR INFLU… │
+ [text] │ ---                             │
+ [text] │ str                             │
+ [text] ╞═════════════════════════════════╡
+ [text] │ REGION TYPE                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ …                               │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] │ HHS Regions                     │
+ [text] └─────────────────────────────────┘
```

**Why:** Regenerated from the naive read with `truncate_ragged_lines=True`.
**Reader sees:** changed: the same (5381, 1) shape, but only the first field of each line survives — the flag discards the rest — where pandas kept every field as an index level. The teaching point ("only one column, and what is happening with the labels?") still lands; the reader simply sees less of the mess. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C38, whose Polars pane is byte-identical to it (verified).

<a id="c106"></a>
### C106 · `ili = pl.read_csv("data/flu/ILINet.csv", skip_rows=1) # drop the title` · output

committed output

```diff
- [text]    REGION TYPE    REGION  YEAR  WEEK  % WEIGHTED ILI  %UNWEIGHTED ILI  \
- [text] 0  HHS Regions  Region 1  2015    40            0.74             0.68
- [text] 1  HHS Regions  Region 2  2015    40            1.03             1.22
- [text] 2  HHS Regions  Region 3  2015    40            1.22             1.24
- [text] 3  HHS Regions  Region 4  2015    40            1.01             1.16
- [text] 4  HHS Regions  Region 5  2015    40            1.04             1.18
- [text]
- [text]    AGE 0-4  AGE 25-49  AGE 25-64  AGE 5-24  AGE 50-64  AGE 65  ILITOTAL  \
- [text] 0      103         50        NaN       133         23      13       322
- [text] 1      547        294        NaN       528        123      95      1587
- [text] 2      401        419        NaN       625        144      81      1670
- [text] 3      486        231        NaN       613         99      75      1504
- [text] 4      384        238        NaN       444        159     103      1328
- [text]
- [text]    NUM. OF PROVIDERS  TOTAL PATIENTS
- [text] 0                134           47051
- [text] 1                199          129577
- [text] 2                280          134338
- [text] 3                299          129900
- [text] 4                284          112807
+ [text] shape: (5, 15)
+ [text] ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬────────┬───────┬───────┬───────┐
+ [text] │ REG ┆ REG ┆ YEA ┆ WEE ┆ %   ┆ %UN ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE 65 ┆ ILITO ┆ NUM.  ┆ TOTAL │
+ [text] │ ION ┆ ION ┆ R   ┆ K   ┆ WEI ┆ WEI ┆ 0-4 ┆ 25- ┆ 25- ┆ 5-2 ┆ 50- ┆ ---    ┆ TAL   ┆ OF    ┆ PATIE │
+ [text] │ TYP ┆ --- ┆ --- ┆ --- ┆ GHT ┆ GHT ┆ --- ┆ 49  ┆ 64  ┆ 4   ┆ 64  ┆ i64    ┆ ---   ┆ PROVI ┆ NTS   │
+ [text] │ E   ┆ str ┆ i64 ┆ i64 ┆ ED  ┆ ED  ┆ i64 ┆ --- ┆ --- ┆ --- ┆ --- ┆        ┆ i64   ┆ DERS  ┆ ---   │
+ [text] │ --- ┆     ┆     ┆     ┆ ILI ┆ ILI ┆     ┆ i64 ┆ str ┆ i64 ┆ i64 ┆        ┆       ┆ ---   ┆ i64   │
+ [text] │ str ┆     ┆     ┆     ┆ --- ┆ --- ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆ i64   ┆       │
+ [text] │     ┆     ┆     ┆     ┆ f64 ┆ f64 ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ [text] ╞═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪════════╪═══════╪═══════╪═══════╡
+ [text] │ HHS ┆ Reg ┆ 201 ┆ 40  ┆ 0.7 ┆ 0.6 ┆ 103 ┆ 50  ┆ nul ┆ 133 ┆ 23  ┆ 13     ┆ 322   ┆ 134   ┆ 47051 │
+ [text] │ Reg ┆ ion ┆ 5   ┆     ┆ 4   ┆ 8   ┆     ┆     ┆ l   ┆     ┆     ┆        ┆       ┆       ┆       │
+ [text] │ ion ┆ 1   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ [text] │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ [text] │ HHS ┆ Reg ┆ 201 ┆ 40  ┆ 1.0 ┆ 1.2 ┆ 547 ┆ 294 ┆ nul ┆ 528 ┆ 123 ┆ 95     ┆ 1587  ┆ 199   ┆ 12957 │
+ [text] │ Reg ┆ ion ┆ 5   ┆     ┆ 3   ┆ 2   ┆     ┆     ┆ l   ┆     ┆     ┆        ┆       ┆       ┆ 7     │
+ [text] │ ion ┆ 2   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ [text] │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ [text] │ HHS ┆ Reg ┆ 201 ┆ 40  ┆ 1.2 ┆ 1.2 ┆ 401 ┆ 419 ┆ nul ┆ 625 ┆ 144 ┆ 81     ┆ 1670  ┆ 280   ┆ 13433 │
+ [text] │ Reg ┆ ion ┆ 5   ┆     ┆ 2   ┆ 4   ┆     ┆     ┆ l   ┆     ┆     ┆        ┆       ┆       ┆ 8     │
+ [text] │ ion ┆ 3   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ [text] │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ [text] │ HHS ┆ Reg ┆ 201 ┆ 40  ┆ 1.0 ┆ 1.1 ┆ 486 ┆ 231 ┆ nul ┆ 613 ┆ 99  ┆ 75     ┆ 1504  ┆ 299   ┆ 12990 │
+ [text] │ Reg ┆ ion ┆ 5   ┆     ┆ 1   ┆ 6   ┆     ┆     ┆ l   ┆     ┆     ┆        ┆       ┆       ┆ 0     │
+ [text] │ ion ┆ 4   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ [text] │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ [text] │ HHS ┆ Reg ┆ 201 ┆ 40  ┆ 1.0 ┆ 1.1 ┆ 384 ┆ 238 ┆ nul ┆ 444 ┆ 159 ┆ 103    ┆ 1328  ┆ 284   ┆ 11280 │
+ [text] │ Reg ┆ ion ┆ 5   ┆     ┆ 4   ┆ 8   ┆     ┆     ┆ l   ┆     ┆     ┆        ┆       ┆       ┆ 7     │
+ [text] │ ion ┆ 5   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ [text] │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
+ [text] └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴────────┴───────┴───────┴───────┘
```

**Why:** Regenerated from `skip_rows=1`.
**Reader sees:** equivalent — same 15 columns and values; `AGE 25-64` reads as `str` with `null` rather than float `NaN`. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C41, whose Polars pane is byte-identical to it (verified).

<a id="c107"></a>
### C107 · `jan_1 = pl.date(pl.col('YEAR'), 1, 1)` · output

committed output

```diff
- [text]       REGION TYPE     REGION  YEAR  WEEK  % WEIGHTED ILI  %UNWEIGHTED ILI  \
- [text] 1856  HHS Regions   Region 7  2019    17            0.99             1.08
- [text] 4421  HHS Regions   Region 2  2024    13            3.51             4.61
- [text] 169   HHS Regions  Region 10  2016     4            1.41             1.50
- [text]
- [text]       AGE 0-4  AGE 25-49  AGE 25-64  AGE 5-24  AGE 50-64  AGE 65  ILITOTAL  \
- [text] 1856      136         43        NaN       106         25      33       343
- [text] 4421     1573       2948        NaN      3310        731     517      9079
- [text] 169        55         37        NaN        92         23       4       211
- [text]
- [text]       NUM. OF PROVIDERS  TOTAL PATIENTS week_start
- [text] 1856                109           31807 2019-05-05
- [text] 4421                245          196943 2024-03-31
- [text] 169                  76           14029 2016-01-31
+ [text] shape: (3, 16)
+ [text] ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬────────┐
+ [text] │ REG ┆ REG ┆ YEA ┆ WEE ┆ %   ┆ %UN ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ ILI ┆ NUM ┆ TOT ┆ week_s │
+ [text] │ ION ┆ ION ┆ R   ┆ K   ┆ WEI ┆ WEI ┆ 0-4 ┆ 25- ┆ 25- ┆ 5-2 ┆ 50- ┆ 65  ┆ TOT ┆ .   ┆ AL  ┆ tart   │
+ [text] │ TYP ┆ --- ┆ --- ┆ --- ┆ GHT ┆ GHT ┆ --- ┆ 49  ┆ 64  ┆ 4   ┆ 64  ┆ --- ┆ AL  ┆ OF  ┆ PAT ┆ ---    │
+ [text] │ E   ┆ str ┆ i64 ┆ i64 ┆ ED  ┆ ED  ┆ i64 ┆ --- ┆ --- ┆ --- ┆ --- ┆ i64 ┆ --- ┆ PRO ┆ IEN ┆ date   │
+ [text] │ --- ┆     ┆     ┆     ┆ ILI ┆ ILI ┆     ┆ i64 ┆ str ┆ i64 ┆ i64 ┆     ┆ i64 ┆ VID ┆ TS  ┆        │
+ [text] │ str ┆     ┆     ┆     ┆ --- ┆ --- ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ ERS ┆ --- ┆        │
+ [text] │     ┆     ┆     ┆     ┆ f64 ┆ f64 ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ --- ┆ i64 ┆        │
+ [text] │     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ i64 ┆     ┆        │
+ [text] ╞═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪════════╡
+ [text] │ HHS ┆ Reg ┆ 201 ┆ 3   ┆ 2.7 ┆ 3.0 ┆ 392 ┆ 360 ┆ nul ┆ 628 ┆ 222 ┆ 157 ┆ 175 ┆ 141 ┆ 574 ┆ 2018-0 │
+ [text] │ Reg ┆ ion ┆ 8   ┆     ┆ 7   ┆ 6   ┆     ┆     ┆ l   ┆     ┆     ┆     ┆ 9   ┆     ┆ 49  ┆ 1-21   │
+ [text] │ ion ┆ 8   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ [text] │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ [text] │ HHS ┆ Reg ┆ 202 ┆ 49  ┆ 7.3 ┆ 7.2 ┆ 179 ┆ 140 ┆ nul ┆ 287 ┆ 563 ┆ 558 ┆ 719 ┆ 233 ┆ 994 ┆ 2022-1 │
+ [text] │ Reg ┆ ion ┆ 2   ┆     ┆ 1   ┆ 4   ┆ 6   ┆ 9   ┆ l   ┆ 3   ┆     ┆     ┆ 9   ┆     ┆ 62  ┆ 2-11   │
+ [text] │ ion ┆ 8   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ [text] │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ [text] │ HHS ┆ Reg ┆ 202 ┆ 1   ┆ 5.7 ┆ 5.1 ┆ 554 ┆ 110 ┆ nul ┆ 964 ┆ 487 ┆ 593 ┆ 371 ┆ 954 ┆ 720 ┆ 2026-0 │
+ [text] │ Reg ┆ ion ┆ 6   ┆     ┆ 2   ┆ 5   ┆ 7   ┆ 95  ┆ l   ┆ 8   ┆ 5   ┆ 7   ┆ 02  ┆     ┆ 870 ┆ 1-11   │
+ [text] │ ion ┆ 4   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ [text] │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ [text] └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴────────┘
```

**Why:** Regenerated after the `week_start` rebuild.
**Reader sees:** changed only by the draw: `ili.sample(3)` is unseeded, so these are three different rows. The column itself is right — verified bit-identical to the pandas `%Y%W%w` parse on all 5380 rows, and all three drawn dates are Sundays. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C44, whose Polars pane is byte-identical to it (verified).

<a id="c108"></a>
### C108 · `ili['week_start'].dt.year().head()` · output

committed output

```diff
- [text] 0    2015
- [text] 1    2015
- [text] 2    2015
- [text] 3    2015
- [text] 4    2015
- [text] Name: week_start, dtype: int32
+ [text] shape: (10,)
+ [text] Series: 'week_start' [i32]
+ [text] [
+ [text] 	2015
+ [text] 	2015
+ [text] 	2015
+ [text] 	2015
+ [text] 	2015
+ [text] 	2015
+ [text] 	2015
+ [text] 	2015
+ [text] 	2015
+ [text] 	2015
+ [text] ]
```

**Why:** Regenerated from `.dt.year()`.
**Reader sees:** changed: ten rows instead of five, from the Polars `head()` default. Same year throughout. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C45, whose Polars pane is byte-identical to it (verified).

<a id="c109"></a>
### C109 · `ili['week_start'].dtype` · output

committed output

```diff
- [text] dtype('<M8[ns]')
+ [text] Date
```

**Why:** `ili['week_start'].dtype` now reports the Polars type.
**Reader sees:** changed: `dtype('<M8[ns]')` → `Date`. This cell is **not** hidden and has no twin, so the Polars answer ships alone — which is why the paragraphs at C46 and C48 had to be rewritten; left as they were, they would describe a NumPy `<M8` dtype and nanosecond storage that no longer appear anywhere on the page.

<a id="c110"></a>
### C110 · `f, ax = plt.subplots(1, 1, figsize=(12, 7))` · output

committed output

```diff
- [text] <Figure size 1200x700 with 1 Axes>
- [image/png] 244208 bytes md5:3f8703464d
+ [text] <Figure size 1200x700 with 1 Axes>
+ [image/png] 243788 bytes md5:5192edb955
```

**Why:** Re-executed. The plotting call is unchanged — `hue='REGION'` on both sides — and only the frame feeding it is now Polars.
**Reader sees:** equivalent — same lineplot of `AGE 0-4` by region; 244208 → 243788 bytes is re-render noise. Not compared pixel by pixel (unverified).

<a id="c111"></a>
### C111 · `f, ax = plt.subplots(1, 1, figsize=(12, 7))` · output

committed output

```diff
- [text] <Figure size 1200x700 with 1 Axes>
- [image/png] 270148 bytes md5:4cf64261b0
+ [text] <Figure size 1200x700 with 1 Axes>
+ [image/png] 269696 bytes md5:42dd4225ce
```

**Why:** Re-executed; the call is unchanged.
**Reader sees:** equivalent — same `% WEIGHTED ILI` lineplot; 270148 → 269696 bytes is re-render noise. Not compared pixel by pixel (unverified).

<a id="c112"></a>
### C112 · `vax = pl.read_csv('data/flu/monthly_child_flu_vaccination.csv')` · output

committed output

```diff
- [text]    HHS Region   month_dt  Numerator  Population  rate
- [text] 0    Region 1 2022-07-01   17110.00  1328581.00  0.01
- [text] 1    Region 1 2022-08-01   42110.00  1328581.00  0.03
- [text] 2    Region 1 2022-09-01  129698.00  1328581.00  0.10
- [text] 3    Region 1 2022-10-01  297855.00  1328581.00  0.22
- [text] 4    Region 1 2022-11-01  430376.00  1328581.00  0.32
- [text] 5    Region 1 2022-12-01  508781.00  1328581.00  0.38
- [text] 6    Region 1 2023-01-01  545783.00  1328581.00  0.41
- [text] 7    Region 1 2023-02-01  563456.00  1328581.00  0.42
- [text] 8    Region 1 2023-03-01  575885.00  1328581.00  0.43
- [text] 9    Region 1 2023-04-01  581451.00  1328581.00  0.44
- [text] 10   Region 1 2023-05-01  586289.00  1328581.00  0.44
- [text] 11   Region 1 2023-06-01  590354.00  1328581.00  0.44
- [text] 12   Region 1 2023-07-01   10473.00  1319459.00  0.01
- [text] 13   Region 1 2023-08-01   32037.00  1319459.00  0.02
+ [text] shape: (14, 5)
+ [text] ┌────────────┬────────────┬───────────┬────────────┬──────┐
+ [text] │ HHS Region ┆ month_dt   ┆ Numerator ┆ Population ┆ rate │
+ [text] │ ---        ┆ ---        ┆ ---       ┆ ---        ┆ ---  │
+ [text] │ str        ┆ date       ┆ f64       ┆ f64        ┆ f64  │
+ [text] ╞════════════╪════════════╪═══════════╪════════════╪══════╡
+ [text] │ Region 1   ┆ 2022-07-01 ┆ 17110.00  ┆ 1328581.00 ┆ 0.01 │
+ [text] │ Region 1   ┆ 2022-08-01 ┆ 42110.00  ┆ 1328581.00 ┆ 0.03 │
+ [text] │ Region 1   ┆ 2022-09-01 ┆ 129698.00 ┆ 1328581.00 ┆ 0.10 │
+ [text] │ Region 1   ┆ 2022-10-01 ┆ 297855.00 ┆ 1328581.00 ┆ 0.22 │
+ [text] │ Region 1   ┆ 2022-11-01 ┆ 430376.00 ┆ 1328581.00 ┆ 0.32 │
+ [text] │ Region 1   ┆ 2022-12-01 ┆ 508781.00 ┆ 1328581.00 ┆ 0.38 │
+ [text] │ Region 1   ┆ 2023-01-01 ┆ 545783.00 ┆ 1328581.00 ┆ 0.41 │
+ [text] │ Region 1   ┆ 2023-02-01 ┆ 563456.00 ┆ 1328581.00 ┆ 0.42 │
+ [text] │ Region 1   ┆ 2023-03-01 ┆ 575885.00 ┆ 1328581.00 ┆ 0.43 │
+ [text] │ Region 1   ┆ 2023-04-01 ┆ 581451.00 ┆ 1328581.00 ┆ 0.44 │
+ [text] │ Region 1   ┆ 2023-05-01 ┆ 586289.00 ┆ 1328581.00 ┆ 0.44 │
+ [text] │ Region 1   ┆ 2023-06-01 ┆ 590354.00 ┆ 1328581.00 ┆ 0.44 │
+ [text] │ Region 1   ┆ 2023-07-01 ┆ 10473.00  ┆ 1319459.00 ┆ 0.01 │
+ [text] │ Region 1   ┆ 2023-08-01 ┆ 32037.00  ┆ 1319459.00 ┆ 0.02 │
+ [text] └────────────┴────────────┴───────────┴────────────┴──────┘
```

**Why:** Regenerated from the Polars read plus `rate`.
**Reader sees:** equivalent — same 14 rows and values; `month_dt` prints as a `Date`. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C50, whose Polars pane is byte-identical to it (verified).

<a id="c113"></a>
### C113 · `display(ili.tail(2))` · output

committed output

```diff
- [text]       REGION TYPE     REGION  YEAR  WEEK  % WEIGHTED ILI  %UNWEIGHTED ILI  \
- [text] 5378  HHS Regions   Region 9  2026     3            4.86             4.62
- [text] 5379  HHS Regions  Region 10  2026     3            5.07             4.91
- [text]
- [text]       AGE 0-4  AGE 25-49  AGE 25-64  AGE 5-24  AGE 50-64  AGE 65  ILITOTAL  \
- [text] 5378     2045       5863        NaN      4914       2552    3004     18378
- [text] 5379     1462       1946        NaN      3526        700     793      8427
- [text]
- [text]       NUM. OF PROVIDERS  TOTAL PATIENTS week_start
- [text] 5378                402          397479 2026-01-25
- [text] 5379                332          171565 2026-01-25
- [text]     HHS Region   month_dt  Numerator  Population  rate
- [text] 418   Region 9 2025-11-01 1416002.00  8216613.00  0.17
- [text] 419   Region 9 2025-12-01 1686327.00  8216613.00  0.21
+ [text] shape: (2, 16)
+ [text] ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬────────┐
+ [text] │ REG ┆ REG ┆ YEA ┆ WEE ┆ %   ┆ %UN ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ ILI ┆ NUM ┆ TOT ┆ week_s │
+ [text] │ ION ┆ ION ┆ R   ┆ K   ┆ WEI ┆ WEI ┆ 0-4 ┆ 25- ┆ 25- ┆ 5-2 ┆ 50- ┆ 65  ┆ TOT ┆ .   ┆ AL  ┆ tart   │
+ [text] │ TYP ┆ --- ┆ --- ┆ --- ┆ GHT ┆ GHT ┆ --- ┆ 49  ┆ 64  ┆ 4   ┆ 64  ┆ --- ┆ AL  ┆ OF  ┆ PAT ┆ ---    │
+ [text] │ E   ┆ str ┆ i64 ┆ i64 ┆ ED  ┆ ED  ┆ i64 ┆ --- ┆ --- ┆ --- ┆ --- ┆ i64 ┆ --- ┆ PRO ┆ IEN ┆ date   │
+ [text] │ --- ┆     ┆     ┆     ┆ ILI ┆ ILI ┆     ┆ i64 ┆ str ┆ i64 ┆ i64 ┆     ┆ i64 ┆ VID ┆ TS  ┆        │
+ [text] │ str ┆     ┆     ┆     ┆ --- ┆ --- ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ ERS ┆ --- ┆        │
+ [text] │     ┆     ┆     ┆     ┆ f64 ┆ f64 ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ --- ┆ i64 ┆        │
+ [text] │     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ i64 ┆     ┆        │
+ [text] ╞═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪════════╡
+ [text] │ HHS ┆ Reg ┆ 202 ┆ 3   ┆ 4.8 ┆ 4.6 ┆ 204 ┆ 586 ┆ nul ┆ 491 ┆ 255 ┆ 300 ┆ 183 ┆ 402 ┆ 397 ┆ 2026-0 │
+ [text] │ Reg ┆ ion ┆ 6   ┆     ┆ 6   ┆ 2   ┆ 5   ┆ 3   ┆ l   ┆ 4   ┆ 2   ┆ 4   ┆ 78  ┆     ┆ 479 ┆ 1-25   │
+ [text] │ ion ┆ 9   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ [text] │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ [text] │ HHS ┆ Reg ┆ 202 ┆ 3   ┆ 5.0 ┆ 4.9 ┆ 146 ┆ 194 ┆ nul ┆ 352 ┆ 700 ┆ 793 ┆ 842 ┆ 332 ┆ 171 ┆ 2026-0 │
+ [text] │ Reg ┆ ion ┆ 6   ┆     ┆ 7   ┆ 1   ┆ 2   ┆ 6   ┆ l   ┆ 6   ┆     ┆     ┆ 7   ┆     ┆ 565 ┆ 1-25   │
+ [text] │ ion ┆ 10  ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ [text] │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
+ [text] └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴────────┘
+ [text] shape: (2, 5)
+ [text] ┌────────────┬────────────┬────────────┬────────────┬──────┐
+ [text] │ HHS Region ┆ month_dt   ┆ Numerator  ┆ Population ┆ rate │
+ [text] │ ---        ┆ ---        ┆ ---        ┆ ---        ┆ ---  │
+ [text] │ str        ┆ date       ┆ f64        ┆ f64        ┆ f64  │
+ [text] ╞════════════╪════════════╪════════════╪════════════╪══════╡
+ [text] │ Region 9   ┆ 2025-11-01 ┆ 1416002.00 ┆ 8216613.00 ┆ 0.17 │
+ [text] │ Region 9   ┆ 2025-12-01 ┆ 1686327.00 ┆ 8216613.00 ┆ 0.21 │
+ [text] └────────────┴────────────┴────────────┴────────────┴──────┘
```

**Why:** Re-executed after both frames became Polars.
**Reader sees:** changed: both frames now print as Polars box tables with a `shape:` header, and `ili`'s 16 columns are boxed rather than wrapped into pandas' stacked column groups. Values unchanged. This cell has no twin, so the Polars rendering ships alone.

<a id="c114"></a>
### C114 · `ili_vax = ili.join(` · output

committed output

```diff
- [text]    REGION TYPE    REGION  YEAR  WEEK  % WEIGHTED ILI  %UNWEIGHTED ILI  \
- [text] 0  HHS Regions  Region 1  2022    26            0.93             1.02
- [text] 1  HHS Regions  Region 2  2022    26            2.80             2.50
- [text] 2  HHS Regions  Region 3  2022    26            1.39             1.63
- [text] 3  HHS Regions  Region 4  2022    26            2.29             2.47
- [text] 4  HHS Regions  Region 5  2022    26            1.15             1.06
- [text]
- [text]    AGE 0-4  AGE 25-49  AGE 25-64  AGE 5-24  AGE 50-64  AGE 65  ILITOTAL  \
- [text] 0      440        356        NaN       346        166     211      1519
- [text] 1     1756        630        NaN      1124        278     297      4085
- [text] 2     1347        883        NaN       929        397     360      3916
- [text] 3     4320       3555        NaN      3430       1469    1370     14144
- [text] 4     1001        678        NaN       817        331     349      3176
- [text]
- [text]    NUM. OF PROVIDERS  TOTAL PATIENTS week_start      month HHS Region  \
- [text] 0                232          148833 2022-07-03 2022-07-01   Region 1
- [text] 1                161          163656 2022-07-03 2022-07-01   Region 2
- [text] 2                371          240707 2022-07-03 2022-07-01   Region 3
- [text] 3                928          572466 2022-07-03 2022-07-01   Region 4
- [text] 4                610          300270 2022-07-03 2022-07-01   Region 5
- [text]
- [text]     month_dt  Numerator  Population  rate
- [text] 0 2022-07-01   17110.00  1328581.00  0.01
- [text] 1 2022-07-01     699.00  1982009.00  0.00
- [text] 2 2022-07-01     284.00  4301556.00  0.00
- [text] 3 2022-07-01    2268.00 13203279.00  0.00
- [text] 4 2022-07-01     662.00 11492529.00  0.00
+ [text] shape: (5, 20)
+ [text] ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
+ [text] │ REG ┆ REG ┆ YEA ┆ WEE ┆ %   ┆ %UN ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ ILI ┆ NUM ┆ TOT ┆ wee ┆ mon ┆ Num ┆ Pop ┆ rat │
+ [text] │ ION ┆ ION ┆ R   ┆ K   ┆ WEI ┆ WEI ┆ 0-4 ┆ 25- ┆ 25- ┆ 5-2 ┆ 50- ┆ 65  ┆ TOT ┆ .   ┆ AL  ┆ k_s ┆ th  ┆ era ┆ ula ┆ e   │
+ [text] │ TYP ┆ --- ┆ --- ┆ --- ┆ GHT ┆ GHT ┆ --- ┆ 49  ┆ 64  ┆ 4   ┆ 64  ┆ --- ┆ AL  ┆ OF  ┆ PAT ┆ tar ┆ --- ┆ tor ┆ tio ┆ --- │
+ [text] │ E   ┆ str ┆ i64 ┆ i64 ┆ ED  ┆ ED  ┆ i64 ┆ --- ┆ --- ┆ --- ┆ --- ┆ i64 ┆ --- ┆ PRO ┆ IEN ┆ t   ┆ dat ┆ --- ┆ n   ┆ f64 │
+ [text] │ --- ┆     ┆     ┆     ┆ ILI ┆ ILI ┆     ┆ i64 ┆ str ┆ i64 ┆ i64 ┆     ┆ i64 ┆ VID ┆ TS  ┆ --- ┆ e   ┆ f64 ┆ --- ┆     │
+ [text] │ str ┆     ┆     ┆     ┆ --- ┆ --- ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ ERS ┆ --- ┆ dat ┆     ┆     ┆ f64 ┆     │
+ [text] │     ┆     ┆     ┆     ┆ f64 ┆ f64 ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ --- ┆ i64 ┆ e   ┆     ┆     ┆     ┆     │
+ [text] │     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ i64 ┆     ┆     ┆     ┆     ┆     ┆     │
+ [text] ╞═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╡
+ [text] │ HHS ┆ Reg ┆ 202 ┆ 26  ┆ 0.9 ┆ 1.0 ┆ 440 ┆ 356 ┆ nul ┆ 346 ┆ 166 ┆ 211 ┆ 151 ┆ 232 ┆ 148 ┆ 202 ┆ 202 ┆ 171 ┆ 132 ┆ 0.0 │
+ [text] │ Reg ┆ ion ┆ 2   ┆     ┆ 3   ┆ 2   ┆     ┆     ┆ l   ┆     ┆     ┆     ┆ 9   ┆     ┆ 833 ┆ 2-0 ┆ 2-0 ┆ 10. ┆ 858 ┆ 1   │
+ [text] │ ion ┆ 1   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 7-0 ┆ 7-0 ┆ 00  ┆ 1.0 ┆     │
+ [text] │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 3   ┆ 1   ┆     ┆ 0   ┆     │
+ [text] │ HHS ┆ Reg ┆ 202 ┆ 26  ┆ 2.8 ┆ 2.5 ┆ 175 ┆ 630 ┆ nul ┆ 112 ┆ 278 ┆ 297 ┆ 408 ┆ 161 ┆ 163 ┆ 202 ┆ 202 ┆ 699 ┆ 198 ┆ 0.0 │
+ [text] │ Reg ┆ ion ┆ 2   ┆     ┆ 0   ┆ 0   ┆ 6   ┆     ┆ l   ┆ 4   ┆     ┆     ┆ 5   ┆     ┆ 656 ┆ 2-0 ┆ 2-0 ┆ .00 ┆ 200 ┆ 0   │
+ [text] │ ion ┆ 2   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 7-0 ┆ 7-0 ┆     ┆ 9.0 ┆     │
+ [text] │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 3   ┆ 1   ┆     ┆ 0   ┆     │
+ [text] │ HHS ┆ Reg ┆ 202 ┆ 26  ┆ 1.3 ┆ 1.6 ┆ 134 ┆ 883 ┆ nul ┆ 929 ┆ 397 ┆ 360 ┆ 391 ┆ 371 ┆ 240 ┆ 202 ┆ 202 ┆ 284 ┆ 430 ┆ 0.0 │
+ [text] │ Reg ┆ ion ┆ 2   ┆     ┆ 9   ┆ 3   ┆ 7   ┆     ┆ l   ┆     ┆     ┆     ┆ 6   ┆     ┆ 707 ┆ 2-0 ┆ 2-0 ┆ .00 ┆ 155 ┆ 0   │
+ [text] │ ion ┆ 3   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 7-0 ┆ 7-0 ┆     ┆ 6.0 ┆     │
+ [text] │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 3   ┆ 1   ┆     ┆ 0   ┆     │
+ [text] │ HHS ┆ Reg ┆ 202 ┆ 26  ┆ 2.2 ┆ 2.4 ┆ 432 ┆ 355 ┆ nul ┆ 343 ┆ 146 ┆ 137 ┆ 141 ┆ 928 ┆ 572 ┆ 202 ┆ 202 ┆ 226 ┆ 132 ┆ 0.0 │
+ [text] │ Reg ┆ ion ┆ 2   ┆     ┆ 9   ┆ 7   ┆ 0   ┆ 5   ┆ l   ┆ 0   ┆ 9   ┆ 0   ┆ 44  ┆     ┆ 466 ┆ 2-0 ┆ 2-0 ┆ 8.0 ┆ 032 ┆ 0   │
+ [text] │ ion ┆ 4   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 7-0 ┆ 7-0 ┆ 0   ┆ 79. ┆     │
+ [text] │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 3   ┆ 1   ┆     ┆ 00  ┆     │
+ [text] │ HHS ┆ Reg ┆ 202 ┆ 26  ┆ 1.1 ┆ 1.0 ┆ 100 ┆ 678 ┆ nul ┆ 817 ┆ 331 ┆ 349 ┆ 317 ┆ 610 ┆ 300 ┆ 202 ┆ 202 ┆ 662 ┆ 114 ┆ 0.0 │
+ [text] │ Reg ┆ ion ┆ 2   ┆     ┆ 5   ┆ 6   ┆ 1   ┆     ┆ l   ┆     ┆     ┆     ┆ 6   ┆     ┆ 270 ┆ 2-0 ┆ 2-0 ┆ .00 ┆ 925 ┆ 0   │
+ [text] │ ion ┆ 5   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 7-0 ┆ 7-0 ┆     ┆ 29. ┆     │
+ [text] │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 3   ┆ 1   ┆     ┆ 00  ┆     │
+ [text] └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
```

**Why:** Regenerated from `ili.join(vax, ...)`.
**Reader sees:** changed: 20 columns where pandas had 22 — Polars coalesces the join keys, so `HHS Region` and `month_dt` are folded into `REGION` and `month`. Row count verified unchanged at 1820. Explained by the sentence added at C53 and visible in the shape mismatch between the two panes at C55. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C55, whose Polars pane is byte-identical to it (verified).

<a id="c115"></a>
### C115 · `f, ax = plt.subplots(1, 1, figsize=(10, 7))` · output

committed output

```diff
- [text] <Figure size 1000x700 with 1 Axes>
- [image/png] 280584 bytes md5:2697bc04dd
+ [text] <Figure size 1000x700 with 1 Axes>
+ [image/png] 278064 bytes md5:d3291c186f
```

**Why:** Re-executed after the hue moved to the surviving key.
**Reader sees:** changed: the legend title reads `REGION` instead of `HHS Region`. The colouring is identical — verified that the two columns are equal on every row of the pandas join — so the figure still matches the prose.

<a id="c116"></a>
### C116 · `co2 = pl.read_csv(co2_file, has_header = False, skip_rows = 72)` · output

committed output

```diff
- [text]       0  1       2      3      4      5  6
- [text] 0  1958  3 1958.21 315.71 315.71 314.62 -1
- [text] 1  1958  4 1958.29 317.45 317.45 315.29 -1
- [text] 2  1958  5 1958.38 317.50 317.50 314.71 -1
- [text] 3  1958  6 1958.46 -99.99 317.10 314.85 -1
- [text] 4  1958  7 1958.54 315.86 315.86 314.98 -1
+ [text] shape: (5, 1)
+ [text] ┌─────────────────────────────────┐
+ [text] │ column_1                        │
+ [text] │ ---                             │
+ [text] │ str                             │
+ [text] ╞═════════════════════════════════╡
+ [text] │ 1958   3    1958.208      315.… │
+ [text] │ 1958   4    1958.292      317.… │
+ [text] │ 1958   5    1958.375      317.… │
+ [text] │ 1958   6    1958.458      -99.… │
+ [text] │ 1958   7    1958.542      315.… │
+ [text] └─────────────────────────────────┘
```

**Why:** Regenerated from the intermediate Polars read.
**Reader sees:** changed, and this is the most conspicuous output move in the chapter: a 738×1 frame of raw strings where the baseline showed the finished 738×7 typed table. Polars has no regex separator, so the parse now takes two cells. The twin was removed (§B1) precisely because the pandas pane had already finished parsing before the section asked its question, and the prose at C59 and C61 was re-aimed to match — so this output and the text around it now agree.

<a id="c117"></a>
### C117 · `co2 = (` · output

committed output

```diff
- [text]      Yr  Mo  DecDate    Avg    Int  Trend  Days
- [text] 0  1958   3  1958.21 315.71 315.71 314.62    -1
- [text] 1  1958   4  1958.29 317.45 317.45 315.29    -1
- [text] 2  1958   5  1958.38 317.50 317.50 314.71    -1
- [text] 3  1958   6  1958.46 -99.99 317.10 314.85    -1
- [text] 4  1958   7  1958.54 315.86 315.86 314.98    -1
+ [text] shape: (5, 7)
+ [text] ┌──────┬─────┬─────────┬────────┬────────┬────────┬──────┐
+ [text] │ Yr   ┆ Mo  ┆ DecDate ┆ Avg    ┆ Int    ┆ Trend  ┆ Days │
+ [text] │ ---  ┆ --- ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---  │
+ [text] │ i64  ┆ i64 ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ i64  │
+ [text] ╞══════╪═════╪═════════╪════════╪════════╪════════╪══════╡
+ [text] │ 1958 ┆ 3   ┆ 1958.21 ┆ 315.71 ┆ 315.71 ┆ 314.62 ┆ -1   │
+ [text] │ 1958 ┆ 4   ┆ 1958.29 ┆ 317.45 ┆ 317.45 ┆ 315.29 ┆ -1   │
+ [text] │ 1958 ┆ 5   ┆ 1958.38 ┆ 317.50 ┆ 317.50 ┆ 314.71 ┆ -1   │
+ [text] │ 1958 ┆ 6   ┆ 1958.46 ┆ -99.99 ┆ 317.10 ┆ 314.85 ┆ -1   │
+ [text] │ 1958 ┆ 7   ┆ 1958.54 ┆ 315.86 ┆ 315.86 ┆ 314.98 ┆ -1   │
+ [text] └──────┴─────┴─────────┴────────┴────────┴────────┴──────┘
```

**Why:** Regenerated from the split/name/cast pipeline.
**Reader sees:** equivalent — the pipeline reproduces the baseline frame exactly: 738×7, identical values, `-99.99` preserved (verified). The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C64, whose Polars pane is byte-identical to it (verified).

<a id="c118"></a>
### C118 · `sns.lineplot(x='DecDate', y='Avg', data=co2);` · output

committed output

```diff
- [text] <Figure size 1200x900 with 1 Axes>
- [image/png] 61500 bytes md5:93bc8c7511
+ [text] <Figure size 1200x900 with 1 Axes>
+ [image/png] 61040 bytes md5:7ac56d889c
```

**Why:** Re-executed; `sns.lineplot(x=..., y=..., data=co2)` takes the Polars frame directly.
**Reader sees:** equivalent — same lineplot including the dips to −100; 61500 → 61040 bytes is re-render noise. Not compared pixel by pixel (unverified).

<a id="c119"></a>
### C119 · `co2.head()` · output

committed output

```diff
- [text]      Yr  Mo  DecDate    Avg    Int  Trend  Days
- [text] 0  1958   3  1958.21 315.71 315.71 314.62    -1
- [text] 1  1958   4  1958.29 317.45 317.45 315.29    -1
- [text] 2  1958   5  1958.38 317.50 317.50 314.71    -1
- [text] 3  1958   6  1958.46 -99.99 317.10 314.85    -1
- [text] 4  1958   7  1958.54 315.86 315.86 314.98    -1
+ [text] shape: (5, 7)
+ [text] ┌──────┬─────┬─────────┬────────┬────────┬────────┬──────┐
+ [text] │ Yr   ┆ Mo  ┆ DecDate ┆ Avg    ┆ Int    ┆ Trend  ┆ Days │
+ [text] │ ---  ┆ --- ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---  │
+ [text] │ i64  ┆ i64 ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ i64  │
+ [text] ╞══════╪═════╪═════════╪════════╪════════╪════════╪══════╡
+ [text] │ 1958 ┆ 3   ┆ 1958.21 ┆ 315.71 ┆ 315.71 ┆ 314.62 ┆ -1   │
+ [text] │ 1958 ┆ 4   ┆ 1958.29 ┆ 317.45 ┆ 317.45 ┆ 315.29 ┆ -1   │
+ [text] │ 1958 ┆ 5   ┆ 1958.38 ┆ 317.50 ┆ 317.50 ┆ 314.71 ┆ -1   │
+ [text] │ 1958 ┆ 6   ┆ 1958.46 ┆ -99.99 ┆ 317.10 ┆ 314.85 ┆ -1   │
+ [text] │ 1958 ┆ 7   ┆ 1958.54 ┆ 315.86 ┆ 315.86 ┆ 314.98 ┆ -1   │
+ [text] └──────┴─────┴─────────┴────────┴────────┴────────┴──────┘
```

**Why:** Re-executed `co2.head()`.
**Reader sees:** changed: Polars box rendering with a `shape:` header and a dtype row, and no index column. Same five rows, same values. No twin on this cell, so the pandas rendering is gone from the page here.

<a id="c120"></a>
### C120 · `co2.tail()` · output

committed output

```diff
- [text]        Yr  Mo  DecDate    Avg    Int  Trend  Days
- [text] 733  2019   4  2019.29 413.32 413.32 410.49    26
- [text] 734  2019   5  2019.38 414.66 414.66 411.20    28
- [text] 735  2019   6  2019.46 413.92 413.92 411.58    27
- [text] 736  2019   7  2019.54 411.77 411.77 411.43    23
- [text] 737  2019   8  2019.62 409.95 409.95 411.84    29
+ [text] shape: (5, 7)
+ [text] ┌──────┬─────┬─────────┬────────┬────────┬────────┬──────┐
+ [text] │ Yr   ┆ Mo  ┆ DecDate ┆ Avg    ┆ Int    ┆ Trend  ┆ Days │
+ [text] │ ---  ┆ --- ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---  │
+ [text] │ i64  ┆ i64 ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ i64  │
+ [text] ╞══════╪═════╪═════════╪════════╪════════╪════════╪══════╡
+ [text] │ 2019 ┆ 4   ┆ 2019.29 ┆ 413.32 ┆ 413.32 ┆ 410.49 ┆ 26   │
+ [text] │ 2019 ┆ 5   ┆ 2019.38 ┆ 414.66 ┆ 414.66 ┆ 411.20 ┆ 28   │
+ [text] │ 2019 ┆ 6   ┆ 2019.46 ┆ 413.92 ┆ 413.92 ┆ 411.58 ┆ 27   │
+ [text] │ 2019 ┆ 7   ┆ 2019.54 ┆ 411.77 ┆ 411.77 ┆ 411.43 ┆ 23   │
+ [text] │ 2019 ┆ 8   ┆ 2019.62 ┆ 409.95 ┆ 409.95 ┆ 411.84 ┆ 29   │
+ [text] └──────┴─────┴─────────┴────────┴────────┴────────┴──────┘
```

**Why:** Re-executed `co2.tail()`.
**Reader sees:** changed: same five rows and values, but pandas' row labels 733–737 are gone, so the reader loses the cue that this is the end of a 738-row frame — `shape: (5, 7)` counts the tail, not the position. The chapter prints `co2.shape` two cells later, which still supplies the 738.

<a id="c121"></a>
### C121 · `co2["Mo"].value_counts().sort("Mo")` · output

committed output

```diff
- [text] Mo
- [text] 1     61
- [text] 2     61
- [text] 3     62
- [text] 4     62
- [text] 5     62
- [text] 6     62
- [text] 7     62
- [text] 8     62
- [text] 9     61
- [text] 10    61
- [text] 11    61
- [text] 12    61
- [text] Name: count, dtype: int64
+ [text] shape: (12, 2)
+ [text] ┌─────┬───────┐
+ [text] │ Mo  ┆ count │
+ [text] │ --- ┆ ---   │
+ [text] │ i64 ┆ u32   │
+ [text] ╞═════╪═══════╡
+ [text] │ 1   ┆ 61    │
+ [text] │ 2   ┆ 61    │
+ [text] │ 3   ┆ 62    │
+ [text] │ 4   ┆ 62    │
+ [text] │ 5   ┆ 62    │
+ [text] │ 6   ┆ 62    │
+ [text] │ 7   ┆ 62    │
+ [text] │ 8   ┆ 62    │
+ [text] │ 9   ┆ 61    │
+ [text] │ 10  ┆ 61    │
+ [text] │ 11  ┆ 61    │
+ [text] │ 12  ┆ 61    │
+ [text] └─────┴───────┘
```

**Why:** Regenerated from `value_counts().sort('Mo')`.
**Reader sees:** changed: a 12×2 table with `Mo` and `count` as columns, instead of a named Series indexed by `Mo`. The counts are unchanged and the Jan/Feb/Sep–Dec 61-vs-62 split holds (verified); C66 now describes the two-column shape. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C67, whose Polars pane is byte-identical to it (verified).

<a id="c122"></a>
### C122 · `sns.displot(co2, x='Days');` · output

committed output

```diff
- [text] <Figure size 500x500 with 1 Axes>
- [image/png] 22508 bytes md5:f28aea1b13
+ [text] <Figure size 500x500 with 1 Axes>
+ [image/png] 22220 bytes md5:9ca43c7d58
```

**Why:** Re-executed after the seaborn handoff changed.
**Reader sees:** equivalent — same `Days` histogram, and the x-axis carries its label again; the one-argument form would have left it blank (verified).

<a id="c123"></a>
### C123 · `sns.scatterplot(x="Yr", y="Days", data=co2);` · output

committed output

```diff
- [text] <Figure size 1200x900 with 1 Axes>
- [image/png] 67028 bytes md5:27c74b8662
+ [text] <Figure size 1200x900 with 1 Axes>
+ [image/png] 66632 bytes md5:ce468146ab
```

**Why:** Re-executed; `sns.scatterplot(..., data=co2)` takes the Polars frame directly.
**Reader sees:** equivalent — same scatter of `Days` against `Yr`. Byte difference is re-render noise (unverified pixel-wise).

<a id="c124"></a>
### C124 · `sns.displot(co2, x='Avg');` · output

committed output

```diff
- [text] <Figure size 500x500 with 1 Axes>
- [image/png] 18308 bytes md5:ee40f82e93
+ [text] <Figure size 500x500 with 1 Axes>
+ [image/png] 17668 bytes md5:0d2a6147fb
```

**Why:** Re-executed after the seaborn handoff changed.
**Reader sees:** equivalent — same `Avg` histogram, isolated sub-zero bin included, and the alt text now describes it correctly (C70/C72).

<a id="c125"></a>
### C125 · `co2.filter(pl.col("Avg") < 0)` · output

committed output

```diff
- [text]        Yr  Mo  DecDate    Avg    Int  Trend  Days
- [text] 3    1958   6  1958.46 -99.99 317.10 314.85    -1
- [text] 7    1958  10  1958.79 -99.99 312.66 315.61    -1
- [text] 71   1964   2  1964.12 -99.99 320.07 319.61    -1
- [text] 72   1964   3  1964.21 -99.99 320.73 319.55    -1
- [text] 73   1964   4  1964.29 -99.99 321.77 319.48    -1
- [text] 213  1975  12  1975.96 -99.99 330.59 331.60     0
- [text] 313  1984   4  1984.29 -99.99 346.84 344.27     2
+ [text] shape: (7, 7)
+ [text] ┌──────┬─────┬─────────┬────────┬────────┬────────┬──────┐
+ [text] │ Yr   ┆ Mo  ┆ DecDate ┆ Avg    ┆ Int    ┆ Trend  ┆ Days │
+ [text] │ ---  ┆ --- ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---  │
+ [text] │ i64  ┆ i64 ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ i64  │
+ [text] ╞══════╪═════╪═════════╪════════╪════════╪════════╪══════╡
+ [text] │ 1958 ┆ 6   ┆ 1958.46 ┆ -99.99 ┆ 317.10 ┆ 314.85 ┆ -1   │
+ [text] │ 1958 ┆ 10  ┆ 1958.79 ┆ -99.99 ┆ 312.66 ┆ 315.61 ┆ -1   │
+ [text] │ 1964 ┆ 2   ┆ 1964.12 ┆ -99.99 ┆ 320.07 ┆ 319.61 ┆ -1   │
+ [text] │ 1964 ┆ 3   ┆ 1964.21 ┆ -99.99 ┆ 320.73 ┆ 319.55 ┆ -1   │
+ [text] │ 1964 ┆ 4   ┆ 1964.29 ┆ -99.99 ┆ 321.77 ┆ 319.48 ┆ -1   │
+ [text] │ 1975 ┆ 12  ┆ 1975.96 ┆ -99.99 ┆ 330.59 ┆ 331.60 ┆ 0    │
+ [text] │ 1984 ┆ 4   ┆ 1984.29 ┆ -99.99 ┆ 346.84 ┆ 344.27 ┆ 2    │
+ [text] └──────┴─────┴─────────┴────────┴────────┴────────┴──────┘
```

**Why:** Regenerated from `co2.filter(pl.col('Avg') < 0)`.
**Reader sees:** equivalent — the same seven `-99.99` records (verified). pandas' row labels are gone. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C74, whose Polars pane is byte-identical to it (verified).

<a id="c126"></a>
### C126 · `sns.lineplot(x='DecDate', y='Avg', data=co2)` · output

committed output

```diff
- [text] <Figure size 1200x900 with 1 Axes>
- [image/png] 68436 bytes md5:54eba35b40
+ [text] <Figure size 1200x900 with 1 Axes>
+ [image/png] 67916 bytes md5:ca5f556247
```

**Why:** Re-executed; call unchanged apart from the frame's library.
**Reader sees:** equivalent — same lineplot. Byte difference is re-render noise (unverified pixel-wise).

<a id="c127"></a>
### C127 · `co2_drop = co2.filter(pl.col('Avg') > 0)` · output

committed output

```diff
- [text]      Yr  Mo  DecDate    Avg    Int  Trend  Days
- [text] 0  1958   3  1958.21 315.71 315.71 314.62    -1
- [text] 1  1958   4  1958.29 317.45 317.45 315.29    -1
- [text] 2  1958   5  1958.38 317.50 317.50 314.71    -1
- [text] 4  1958   7  1958.54 315.86 315.86 314.98    -1
- [text] 5  1958   8  1958.62 314.93 314.93 315.94    -1
+ [text] shape: (5, 7)
+ [text] ┌──────┬─────┬─────────┬────────┬────────┬────────┬──────┐
+ [text] │ Yr   ┆ Mo  ┆ DecDate ┆ Avg    ┆ Int    ┆ Trend  ┆ Days │
+ [text] │ ---  ┆ --- ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---  │
+ [text] │ i64  ┆ i64 ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ i64  │
+ [text] ╞══════╪═════╪═════════╪════════╪════════╪════════╪══════╡
+ [text] │ 1958 ┆ 3   ┆ 1958.21 ┆ 315.71 ┆ 315.71 ┆ 314.62 ┆ -1   │
+ [text] │ 1958 ┆ 4   ┆ 1958.29 ┆ 317.45 ┆ 317.45 ┆ 315.29 ┆ -1   │
+ [text] │ 1958 ┆ 5   ┆ 1958.38 ┆ 317.50 ┆ 317.50 ┆ 314.71 ┆ -1   │
+ [text] │ 1958 ┆ 7   ┆ 1958.54 ┆ 315.86 ┆ 315.86 ┆ 314.98 ┆ -1   │
+ [text] │ 1958 ┆ 8   ┆ 1958.62 ┆ 314.93 ┆ 314.93 ┆ 315.94 ┆ -1   │
+ [text] └──────┴─────┴─────────┴────────┴────────┴────────┴──────┘
```

**Why:** Regenerated from `co2.filter(pl.col('Avg') > 0)`.
**Reader sees:** equivalent — same 731 surviving rows; the dropped row no longer shows as a gap in an index. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C82, whose Polars pane is byte-identical to it (verified).

<a id="c128"></a>
### C128 · `co2_null = co2.with_columns(pl.col(pl.Float64).replace(-99.99, None))` · output

committed output

```diff
- [text]      Yr  Mo  DecDate    Avg    Int  Trend  Days
- [text] 0  1958   3  1958.21 315.71 315.71 314.62    -1
- [text] 1  1958   4  1958.29 317.45 317.45 315.29    -1
- [text] 2  1958   5  1958.38 317.50 317.50 314.71    -1
- [text] 3  1958   6  1958.46    NaN 317.10 314.85    -1
- [text] 4  1958   7  1958.54 315.86 315.86 314.98    -1
+ [text] shape: (5, 7)
+ [text] ┌──────┬─────┬─────────┬────────┬────────┬────────┬──────┐
+ [text] │ Yr   ┆ Mo  ┆ DecDate ┆ Avg    ┆ Int    ┆ Trend  ┆ Days │
+ [text] │ ---  ┆ --- ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---  │
+ [text] │ i64  ┆ i64 ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ i64  │
+ [text] ╞══════╪═════╪═════════╪════════╪════════╪════════╪══════╡
+ [text] │ 1958 ┆ 3   ┆ 1958.21 ┆ 315.71 ┆ 315.71 ┆ 314.62 ┆ -1   │
+ [text] │ 1958 ┆ 4   ┆ 1958.29 ┆ 317.45 ┆ 317.45 ┆ 315.29 ┆ -1   │
+ [text] │ 1958 ┆ 5   ┆ 1958.38 ┆ 317.50 ┆ 317.50 ┆ 314.71 ┆ -1   │
+ [text] │ 1958 ┆ 6   ┆ 1958.46 ┆ null   ┆ 317.10 ┆ 314.85 ┆ -1   │
+ [text] │ 1958 ┆ 7   ┆ 1958.54 ┆ 315.86 ┆ 315.86 ┆ 314.98 ┆ -1   │
+ [text] └──────┴─────┴─────────┴────────┴────────┴────────┴──────┘
```

**Why:** Regenerated from `replace(-99.99, None)`.
**Reader sees:** changed: the missing entry prints as `null` where the baseline printed `NaN`. That is the section's lesson, and the heading, the option list and the figure panel title all moved with it. This cell is **not** hidden and has no twin — §B1 removed it because the two panes carried contradictory comments — so the Polars output ships alone.

<a id="c129"></a>
### C129 · `co2_impute = co2.with_columns(Avg = pl.col('Int'))` · output

committed output

```diff
- [text]      Yr  Mo  DecDate    Avg    Int  Trend  Days
- [text] 0  1958   3  1958.21 315.71 315.71 314.62    -1
- [text] 1  1958   4  1958.29 317.45 317.45 315.29    -1
- [text] 2  1958   5  1958.38 317.50 317.50 314.71    -1
- [text] 3  1958   6  1958.46 317.10 317.10 314.85    -1
- [text] 4  1958   7  1958.54 315.86 315.86 314.98    -1
+ [text] shape: (5, 7)
+ [text] ┌──────┬─────┬─────────┬────────┬────────┬────────┬──────┐
+ [text] │ Yr   ┆ Mo  ┆ DecDate ┆ Avg    ┆ Int    ┆ Trend  ┆ Days │
+ [text] │ ---  ┆ --- ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---  │
+ [text] │ i64  ┆ i64 ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ i64  │
+ [text] ╞══════╪═════╪═════════╪════════╪════════╪════════╪══════╡
+ [text] │ 1958 ┆ 3   ┆ 1958.21 ┆ 315.71 ┆ 315.71 ┆ 314.62 ┆ -1   │
+ [text] │ 1958 ┆ 4   ┆ 1958.29 ┆ 317.45 ┆ 317.45 ┆ 315.29 ┆ -1   │
+ [text] │ 1958 ┆ 5   ┆ 1958.38 ┆ 317.50 ┆ 317.50 ┆ 314.71 ┆ -1   │
+ [text] │ 1958 ┆ 6   ┆ 1958.46 ┆ 317.10 ┆ 317.10 ┆ 314.85 ┆ -1   │
+ [text] │ 1958 ┆ 7   ┆ 1958.54 ┆ 315.86 ┆ 315.86 ┆ 314.98 ┆ -1   │
+ [text] └──────┴─────┴─────────┴────────┴────────┴────────┴──────┘
```

**Why:** Regenerated from `with_columns(Avg = pl.col('Int'))`.
**Reader sees:** equivalent — `Avg` filled from `Int`, same five rows. The cell is tagged `remove-input`/`remove-output`, so this output never reaches the page; the reader meets it through the tab-set at C86, whose Polars pane is byte-identical to it (verified).

<a id="c130"></a>
### C130 · `def line_and_points(data, ax, title):` · output

committed output

```diff
- [text] <Figure size 1200x400 with 3 Axes>
- [image/png] 57488 bytes md5:e8ec65814f
+ [text] <Figure size 1200x400 with 3 Axes>
+ [image/png] 55284 bytes md5:c7754c0fa4
```

**Why:** Re-executed after the middle panel's title changed.
**Reader sees:** changed: panel 2 now reads "2. Missing Set to Null". The three plotted series are unchanged — a Polars `null` reaches matplotlib as a gap exactly as `NaN` did, so panel 2 is still segmented at months 6 and 10, and the alt text at C87/C90 still describes what is drawn. The 57488 → 55284 byte drop is the shorter title.

<a id="c131"></a>
### C131 · `sns.lineplot(x='DecDate', y='Avg', data=co2_impute)` · output

committed output

```diff
- [text] <Figure size 1200x900 with 1 Axes>
- [image/png] 90824 bytes md5:8ca4a4d0d9
+ [text] <Figure size 1200x900 with 1 Axes>
+ [image/png] 90276 bytes md5:21aa81cb2b
```

**Why:** Re-executed; call unchanged apart from the frame's library.
**Reader sees:** equivalent — same imputed lineplot. Byte difference is re-render noise (unverified pixel-wise).

<a id="c132"></a>
### C132 · `co2_year = co2_impute.group_by('Yr').mean().sort('Yr')` · output

committed output

```diff
- [text] <Figure size 1200x900 with 1 Axes>
- [image/png] 54760 bytes md5:611ffa42cf
+ [text] <Figure size 1200x900 with 1 Axes>
+ [image/png] 54228 bytes md5:9f081029bb
```

**Why:** Re-executed after `group_by('Yr').mean().sort('Yr')`.
**Reader sees:** equivalent — same yearly mean line. seaborn sorts by `x` when drawing, so the figure would have looked the same without the added `.sort`; what the sort protects is the printed frame's order, which Polars does not otherwise guarantee.

