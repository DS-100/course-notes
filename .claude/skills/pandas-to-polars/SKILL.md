---
name: pandas-to-polars
description: Execution-verified pandas to Polars conversion reference for the Data 100 course notes — mapping tables for I/O, group_by, pivot, strings, datetimes, apply/map, display config, and the interop ladder with the NumPy dispatch rule that decides every `.to_numpy()` boundary, plus the output-equivalence policy and the rename-vs-reshape routing rule. Load before converting or reviewing any pandas code in this repo.
---

# Data C100/C200 — Pandas → Polars Reference Sheet

A conversion companion for the course notes. Derived from the Fall 2025 final reference sheet and
extended to cover the full pandas API surface used across the Data 100 corpus. Every Polars mapping
below was verified by executing it against the installed Polars (course pin 1.43.1). Library-agnostic
sections — regex operators, SQL syntax, modeling formulas, scikit-learn — are unchanged and noted at
the end.

**What is different about converting the notes rather than an assignment.** These notebooks are a
published textbook, so three things that did not matter for graded work now do:

- **Committed outputs are the deliverable.** CI runs `jupyter-book build --html` with no `--execute`,
  so MyST renders whatever outputs are committed. Code and output ship together, and a converted cell
  with a stale output publishes Polars source above a pandas table.
- **Prose quotes the outputs.** Paragraphs cite row counts, column names, and specific numbers from
  the cell above them. Whenever an output changes, everything nearby that describes it has to move
  with it. This is the single most common defect in a notes conversion.
- **Code appears twice.** 82 markdown blocks repeat the source of the next code cell inside a
  `{dropdown}`, and the cell itself carries `remove-input` so only its output renders. Convert one
  and not the other and the page shows pandas source above Polars output. See the `myst-jupyterbook`
  skill for the mechanics.

```python
import polars as pl
```

**Watch for `pl` already being taken.** `pl` is a common local name — sklearn `Pipeline`
objects (`pl = Pipeline([...])`) and matplotlib's `pylab` both appear as `pl` in this corpus.
Adding `import polars as pl` silently rebinds it, and the failure surfaces cells later as a
confusing `AttributeError` on the wrong object. Rename the local (`pipe`), never the import,
and check every later reference to it.

---

## Output equivalence policy — "most equivalent", not identical

**Keep Polars-native behavior. Adapt the test and the prose to it — never contort the Polars code to
reproduce pandas output.** This governs every judgment call below.

This has already gone wrong once in this repo: a `group_by` result had its columns manually renamed
so the output matched what the previous library produced. The rename should never have been
written — the test and the prompt should have moved to the Polars name.

- **Row order is not a property to preserve.** `group_by` defaults to `maintain_order=False` and is
  genuinely nondeterministic under Polars' threading. A test that passed under pandas by accident of
  ordering becomes order-independent (sorted lists, sets), or the *solution* gains an explicit
  `.sort(...)` — but only when the question actually cares about order, never to make an assert pass.
- **Default names win.** `.agg(pl.col("score").mean())` produces `score`. pandas dict-agg produced
  MultiIndex tuples like `("score", "mean")`. Take the Polars name and update every downstream
  reference — prompt text, later cells, tests. Do not add `.alias()` or `.rename()` whose only
  purpose is matching a pandas artifact.
- **The prose moves to the output, not the output to the prose.** When a constant genuinely changes
  (tie-break order, null vs NaN, float formatting) or a shape changes (`value_counts` Series →
  DataFrame), rewrite the sentence that describes it and record old→new in `CONVERSIONS.md`. Bending
  the code to preserve a number quoted in a paragraph is the same defect as bending it to preserve a
  test.
- **The bar is pedagogical equivalence.** Does the section still teach what it set out to teach? A
  page that reproduces pandas' exact output under Polars syntax has lost that.

Reviewers treat cosmetic pandas-matching — renames, reshapes, or sorts existing only to reproduce a
pandas artifact — as a blocking defect.

## Rename vs reshape — routing

**Rename** (mechanically safe): `groupby`→`group_by`, `isin`→`is_in`, `astype`→`cast`,
`merge`→`join`, `fillna`→`fill_null`, `nunique`→`n_unique`, `tolist`→`to_list`, `.values`→`to_numpy()`.

**Reshape** (needs a human or an agent — never regex): `groupby().filter()` → `.over()` window,
`.loc`/`.iloc`, `set_index`/`reset_index`, `pivot_table` with hierarchical columns, dict-agg with
lists, anything MultiIndex, `.str.slice` offset/length semantics, index-alignment joins.

**`y = y.loc[X.index]` — the label-alignment shape, and it needs its own treatment.** Standard in
every modeling unit: a pipeline drops rows, and the label vector has to follow. The naive rewrite is
to duplicate the pipeline's filter, which is *incomplete*: `y.loc[X.index]` both **selected** and
**reordered** `y`, so it survived a pipeline containing a sort or a join. A re-filter reproduces the
selection only, and a length check passes while the model trains on permuted labels. Recommended
form:

1. Hoist the threshold to a named constant **in the student-editable cell**, referenced from both
   places, so there is nothing to keep in sync by hand.
2. Re-derive `y` with the same predicate.
3. `if len(X) != len(y): raise ValueError(...)` so the failure names itself.
4. **State in the prompt that the pipeline must return rows in the order it received them**, and
   that `join`/`group_by` inside it need `maintain_order`. Length alone cannot catch reordering.

**`content/eda/ds100_utils.py` is dead.** It defines `fetch_and_cache` and `head`, and no notebook in
the repo imports it — the two chapters that cache downloads define the function inline instead. It is
frozen by the repo-invariants gate. Do not convert it, and do not start importing it to "clean up"
the inline copies; that is a content decision for course staff, not a conversion.

## Read this first: the conceptual shifts

These are the differences that silently break a mechanical find-and-replace. None of them are
renames — they change how the code is *shaped*.

1. **There is no index.** Polars has no row labels. Every `.loc[...]`, `.set_index()`, `df.index`,
   and label-based lookup has no direct analog. Rows are addressed by position only. If you truly
   need a counter column, add one explicitly with `df.with_row_index()`. *Corpus note:* the course
   notebooks never call `set_index` directly — label-based `.loc` appears on the **results of**
   `pivot_table`, `value_counts`, and `groupby`, so converting those calls (which keep keys as
   ordinary columns in Polars) makes the downstream `.loc` a plain `filter`/`select`.

   **`df[rows, cols]` is closer than "no analog" suggests, and it matters when the lab's subject
   *is* selection syntax.** One bracket takes row slices, column-label slices, name lists, integer
   lists, and mixed forms; rewriting eighteen teaching cells into indistinguishable `filter`/`select`
   calls throws the lesson away. Verified against polars 1.43.1:

   | form | result |
   |---|---|
   | `df[0:3, "fruit":"price"]` | rows **exclusive** (3 rows), column labels **inclusive** (`price` is included) — the two halves of one expression disagree, so say so when teaching it |
   | `df[[0, 2]]` | integers read as **rows**, not columns |
   | `df[:, [0, 2]]` | the column form; `:,` is what disambiguates |
   | `df[0, "Name"]` | scalar — replaces `.loc[0, "Name"]` in tests |

   When a question taught label-vs-position, re-aim it at the fact that replaces it: positions belong
   to the table, not to the row, so sorting renumbers them. If the old numbering is the point,
   materialize it with `with_row_index()` **before** sorting.

2. **Column assignment becomes `with_columns`.** `df["new"] = expr` is the single most common
   mutation in the corpus (69 occurrences). It becomes
   `df = df.with_columns(<expr>.alias("new"))`. Same for `df.loc[:, "new"] = ...`.

3. **Expressions run inside contexts.** Polars work happens inside `select()`, `filter()`,
   `with_columns()`, and `group_by().agg()`, using `pl.col("x")` expressions. A boolean mask
   `df[df["x"] > 0]` becomes `df.filter(pl.col("x") > 0)`.

4. **`sort` flips sense, AND puts nulls first.** pandas `ascending=True` ↔ Polars
   `descending=False`; a blind keyword rename inverts the sort. Less obvious and more damaging:
   pandas defaults `na_position="last"`, while Polars sorts nulls to the **front**. Verified —
   `sort_values("co2", ascending=False).head(3)` gives `['China','USA','Mexico']` where
   `sort("co2", descending=True).head(3)` gives `['Palau','China','USA']`, Palau being a null.
   **Any "top N" / `.head()` after a sort on a nullable column silently gains a null row and drops a
   real one**, with no error. Pass `nulls_last=True` whenever the sort feeds a head/tail or a
   positional slice. This is correctness, not pandas-matching.

5. **Everything is immutable.** No `inplace=`. Consequently **`.copy()` (25×) and
   `.reset_index(drop=True)` (most of the 19 `reset_index` calls) simply disappear** — delete
   them, don't translate them. Keep `reset_index()` only when it follows a `groupby`, where
   Polars needs nothing because group keys are already columns.

6. **`null` is not `NaN`.** Polars separates missing values (`null`) from floating-point `NaN`.
   `fillna` → `fill_null`; a column with real `NaN` needs `fill_nan` too.

7. **`value_counts` returns a DataFrame, not a Series.** Columns `[value, count]`, unsorted by
   default — pass `sort=True` to rank. The common corpus idiom
   `s.value_counts().index[0]` (most frequent value) becomes
   `s.value_counts(sort=True)[s.name][0]`, or just `s.mode()[0]`.

8. **`unique` does not preserve order by default.** Add `maintain_order=True` to match pandas'
   order-of-appearance. Same for `group_by(..., maintain_order=True)`.

9. **Join suffixes differ.** pandas `merge` disambiguates overlapping columns as `_x`/`_y`;
   Polars `join` keeps the left name and suffixes only the right as `_right`. Any test or later
   code referencing `col_x`/`col_y` must change.

10. **Keyword renames on `sample`.** `random_state=` → `seed=`, `frac=` → `fraction=`,
    `replace=` → `with_replacement=`. Seeded sampling appears in graded questions — a silent
    keyword mismatch here changes graded output.

---

## I/O and construction

| Pandas | Polars | Notes |
|---|---|---|
| `pd.read_csv(path_or_url)` | `pl.read_csv(path_or_url)` | 46× in corpus. **`sep=` → `separator=`.** **CR-only line endings fail SILENTLY, not loudly** — verified: a `\r`-terminated CSV reads as a **0-row frame with the columns exploded** and no error whatsoever, where pandas parses it correctly. Pass `eol_char='\r'`. Two notebooks in this corpus ship such files (`little_women.csv`, `sat2014.csv`), and in both the failure would have wiped out a whole section while every gate stayed green. Polars is also stricter about trailing-space numerics; `encoding="latin1"` → `encoding="latin-1"` works, or read with `encoding="utf8-lossy"`. `dtype=str` → `infer_schema=False`. |
| `pd.read_csv(path)` on a file with `NA`/`N/A`/`null` tokens | `pl.read_csv(path, null_values="NA")` | pandas has a default NA-token set; Polars has none. A column pandas silently made float-with-NaN raises `ComputeError: could not parse 'NA' as dtype 'i64'`. `null_values=` restores the baseline's *reading* behavior — it is not cosmetic pandas-matching, so don't strip it in review. |
| `pd.read_csv(path, index_col=0)` where the first header field is empty | `pl.read_csv(path).rename({"": "<label>"})` **if anything downstream reads the index**, otherwise `.drop("")` | Common Data 100 shape. pandas gives you a column literally named `""`, unusable unrenamed. Route on use: pandas moved that field *out* of the column set, so when nothing reads it, dropping is the faithful conversion — **not** cosmetic pandas-matching, and a reviewer working from this table alone would otherwise be primed to flag it. |
| `df.insert(0, "bias", 1)` | `df.insert_column(0, pl.Series("bias", np.ones(df.height)))` | The bias-column pattern in every modeling unit. **Two traps:** `insert_column` mutates in place *and* returns self — the one real exception to the immutability rule above — so `out = df.insert_column(...)` leaves `df` changed too. And it will not broadcast a scalar; you must build a full-length Series or it raises `TypeError`. |
| `pd.read_json(path)` | `pl.read_json(path)` | For line-delimited JSON use `pl.read_ndjson`. |
| `%config SqlMagic.autopandas = True` | `%config SqlMagic.autopolars = True` | **jupysql, verified on 0.11.1.** Makes `%%sql` cells and the `result << query` operator return a real `polars.DataFrame`. Any SQL lecture or lab hits this; without it the magic keeps handing back pandas and the notebook silently mixes libraries. |
| `result.DataFrame()` / `result.df()` | `result.PolarsDataFrame()` / `result.pl()` | The jupysql `ResultSet` accessors. Both Polars forms exist on 0.11.1. |
| `pl.read_database(query, engine)` | `pl.read_database(query, engine.connect())` | Polars needs a **Connection**, not an Engine — a SQLAlchemy `Engine` has no `.execute`, so passing one raises. |
| `pd.read_sql(query, conn)` | `pl.read_database(query, conn)` | Accepts the same SQLAlchemy/sqlite3 connection. `%%sql` magic cells are unaffected — only the pandas hand-off changes. **Does not apply to a `duckdb:///` URI — see "duckdb" under Gotchas before converting hw07 or lab09, whose 15 sites are all the duckdb path.** |
| `pd.DataFrame({...})` | `pl.DataFrame({...})` | 35×. Same dict-of-lists shape. List-of-dicts also works. |
| `pd.DataFrame(arr_2d, columns=names)` | `pl.DataFrame(arr_2d, schema=list(names))` | **Orientation differs by input type**, which is the whole trap: a 2D ndarray reads as *rows* (matching pandas), but a list-of-lists reads as *columns* and needs `orient="row"`. Also `schema=` rejects an ndarray of column names — wrap it in `list(...)`, which `sklearn`'s `feature_names_out` and `Bunch.feature_names` both require. |
| `pd.Series(vals)` | `pl.Series(vals)` / `pl.Series("name", vals)` | First positional arg is the *name* when two are given. |
| `pd.concat([a, b])` | `pl.concat([a, b])` | Row-wise by default. |
| `pd.concat([a, b], axis=1)` | **`a.hstack(b)`** | Use `hstack`. The `pl.concat` alternatives both have version problems: `how="horizontal"` emits a `DeprecationWarning` on the 1.43.1 pin *even when heights already match*, and `how="horizontal_extend"` does not exist before ~1.4x and raises `ValueError` there. `hstack` is correct on every version in play, so it is the only safe form for code that may be executed outside the pinned env. |
| `df.to_csv(path, index=False)` | `df.write_csv(path)` | No index, so no `index=` — drop it. |
| `pd.set_option("display....", n)` | `pl.Config.set_tbl_rows(n)` etc. | Display config lives on `pl.Config`. |
| `pd.get_dummies(s, drop_first=True, prefix=col)` | `df.to_dummies([col], drop_first=True)` | Column names come out as `col_value` automatically. |

**Appending a row** (`df.loc[len(df)] = [...]`, used in error-tracking loops):
`df = df.vstack(pl.DataFrame([row_dict]))` — or better, collect rows in a list and build the
frame once at the end.

---

## DataFrame / Series operations

| Pandas | Polars | Notes |
|---|---|---|
| `df.shape` | `df.shape` | Same `(rows, cols)`. Also `df.height`, `df.width`. |
| `df.columns` | `df.columns` | Plain `list[str]` — no `.tolist()` needed. |
| `df.index` | *(no equivalent)* | See shift 1. `df.with_row_index()` if a counter is truly needed. |
| `df[col]` | `df["col"]` / `df.get_column("col")` | In an expression context: `pl.col("col")`. |
| `df[[col1, col2]]` | `df.select(["col1", "col2"])` | Bracket form also works. |
| `df.values` / `s.values` | `df.to_numpy()` / `s.to_numpy()` | 30×. `.values` does not exist. **But route on what the prose promises:** when surrounding text describes `.values` as "a list of lists" or rows/tuples rather than an array, `df.rows()` is the faithful answer — it returns a list of tuples, where `to_numpy()` returns an ndarray and would leave the prose lying. |
| `s.tolist()` | `s.to_list()` | 13×. Note the underscore. |
| `s.astype(dtype)` | `s.cast(pl.Int64)` | 50×. Python types work too: `.cast(int)` → Int64. String args (`"int"`) do **not** — use Polars dtypes. |
| `df.loc[mask, cols]` | `df.filter(mask).select(cols)` | Label `.loc` has no analog (shift 1). |
| `df.iloc[i]` / `df.iloc[a:b]` | `df.row(i)` (tuple) / `df[a:b]` or `df.slice(a, b-a)` | `df.iloc[idx_array]` (train/val splits) → `df[idx_array]` or `df.gather(...)` on Series. |
| `s.iloc[0]` | `s[0]` / `s.first()` | |
| `s.idxmax()` | `s.arg_max()` | Position, not label. |
| `s.isnull()` / `s.isna()` | `pl.col("c").is_null()` | 16×. `pd.isnull(x)` on a scalar → `x is None`. |
| `s.fillna(v)` | `pl.col("c").fill_null(v)` | Add `fill_nan(v)` if real `NaN` present. |
| `df.dropna()` / `df.dropna(subset=[...])` | `df.drop_nulls()` / `df.drop_nulls(subset=[...])` | |
| `df.drop_duplicates()` | `df.unique(maintain_order=True)` | `subset=` supported the same way. |
| `s.nunique()` | `s.n_unique()` | |
| `s.isin(values)` | `pl.col("c").is_in(values)` | |
| `df.drop(columns=[...])` / `df.drop(c, axis=1)` | `df.drop(["c1", "c2"])` | No `axis`. Dropping rows = `filter`. |
| `df.rename(columns={...})` | `df.rename({"old": "new"})` | |
| `df.sort_values(by, ascending=True)` | `df.sort(by, descending=False)` | **Keyword sense inverted** (shift 4). `na_position="last"` → `nulls_last=True`. |
| `s.unique()` | `s.unique(maintain_order=True)` | Shift 8. |
| `s.value_counts()` | `s.value_counts(sort=True)` | Returns DataFrame (shift 7). |
| `pd.merge(l, r, on=, how=)` / `l.merge(r, ...)` | `l.join(r, on=, how=)` | 14×. `how` defaults `"inner"` both sides. **Suffixes differ** (shift 9). |
| `l.join(r)` *(index join)* | join on a key column; or `with_row_index()` on both sides + `join(..., how="left", maintain_order="left")` + `.drop` the index | pandas `.join` aligns on index; pick the real key. 9×, mostly after groupby — where the key is a column anyway. **When you are reproducing *positional* alignment, `maintain_order="left"` is required, not optional** — `join` gives no order guarantee, so any test asserting a specific row passes by luck without it. Prefer this over `concat(how="horizontal_extend")` when the notebook is *teaching* the alignment: it says what is happening, and it does not silently pair rows that were never meant to line up. |
| `df.query("expr")` | `df.filter(...)` | Rewrite the string expression as a `pl.col` expression. |
| `df.melt(id_vars=, value_vars=)` | `df.unpivot(index=, on=)` | **Renamed**, and so were the keywords. `melt` still aliased but deprecated. |
| `df.sample(n, random_state=s)` | `df.sample(n, seed=s)` | Shift 10 keyword renames. |
| `df.describe()` | `df.describe()` | Stats appear as a `statistic` column, not an index. |
| `df.info()` | `df.glimpse()` / `df.schema` | |
| `df.equals(other)` | `df.equals(other)` | Exists, but **null equality semantics differ** — verify tests that use it rather than assuming. |
| `df.T` | `df.transpose()` | Rare on DataFrames (15× corpus `.T` is nearly all NumPy — leave those alone). |
| `X.dot(Y)` / `df.values @ w` | `df.to_numpy() @ w` | Linear-algebra cells (lab05/lab10) should cross to NumPy at the boundary. |
| `s.round(2)` | `s.round(2)` | Same. |
| `s.quantile(q)` | `s.quantile(q)` | Both take 0–1. (Only helpers that used 0–100 percentiles need care.) |
| `df.head(n)` / `df.tail(n)` | same | |

---

## Group by

Let `by` be a column name or list of names. `groupby` → `group_by` (underscore), and group keys
come back as **ordinary columns** — the pandas `as_index=False` / trailing `.reset_index()` dance
disappears.

| Pandas | Polars | Notes |
|---|---|---|
| `df.groupby(by).mean()` | `df.group_by(by).mean()` | Add `maintain_order=True` when output order matters — **group order is not guaranteed**, and narrative text or tests often assume it. Usually the right fix is an explicit `.sort(...)` after `.agg`. |
| `df.sort_values(k).groupby(g).last()` | `df.sort(k).group_by(g).last()` | **Within-group row order *is* preserved**, even though *group* order is not. That is what makes this idiom a faithful translation rather than a flake — verified stable over 200 runs. Don't reach for a `sort_by` inside `.agg`, and don't flag it in review. |
| `df.groupby(by)[col].mean()` | `df.group_by(by).agg(pl.col(col).mean())` | The corpus's most common groupby shape (`.groupby("postal5")["low"].mean()` etc.). |
| `df.groupby(by).size()` | `df.group_by(by).len()` | In an `agg`: `pl.len()`. |
| `df.groupby(by).agg("count")` | `df.group_by(by).agg(pl.all().count())` | |
| `df.groupby(by).agg({"score": "min", "name": "first"})` | `.agg(pl.col("score").min(), pl.col("name").first())` | One expression per dict entry. |
| `df.groupby(by).agg({"score": ["mean", "count"]})` | `.agg(pl.col("score").mean().alias("score_mean"), pl.col("score").count().alias("score_count"))` | **Dict-with-list creates MultiIndex columns in pandas** (then `sort_values(("score","mean"))`). Polars has no MultiIndex — pick flat names once and use them everywhere downstream, tests included. |
| `df.groupby(by).agg(Count=("col", f))` | `.agg(Count=pl.col("col").f())` | Named-agg keyword form carries over directly. |
| `df.groupby(by).filter(lambda sf: sf.shape[0] >= k)` | `df.filter(pl.len().over(by) >= k)` | **Different shape entirely** — window expression, no lambda. |
| `df.groupby(by).filter(lambda sf: sf["c"].max() > v)` | `df.filter(pl.col("c").max().over(by) > v)` | Same pattern, any aggregate. |
| `grouped.head(n)` | `df.group_by(by).head(n)` | |

The `groupby(...).filter(...)` → `.over()` rewrite is the single most common thing a mechanical
translator gets wrong. Both corpus shapes are shown above (`sf.shape[0]` and `sf["col"].agg()`) —
anything else, stop and think rather than pattern-match.

---

## pivot_table

```python
# pandas (corpus shape)
df.pivot_table(index="type", columns="Missing Score", values="score",
               aggfunc="count", fill_value=0)

# polars
df.pivot(on="Missing Score", index="type", values="score",
         aggregate_function="count").fill_null(0)
```

- `columns=` → `on=`; `aggfunc=` → `aggregate_function=`; `fill_value=0` → chain `.fill_null(0)`.
- The pandas index becomes a normal column — downstream `.loc["Democratic", "Popular vote"]`
  becomes `filter(pl.col("Party") == "Democratic").select("Popular vote")`.
- `values=["a", "b"]` (list) makes MultiIndex columns in pandas; Polars emits flat
  **`{value}_{on_value}`** names — `pivot(on="R", values=["Count","Name"])` gives
  `Count_F, Count_M, Name_F, Name_M`. Note the `on` *column* name (`R`) does not appear. As with
  dict-agg: fix the names once, update everything downstream, including any prose that shows them.
- Eager DataFrames only (no LazyFrame).

---

## Datetimes

| Pandas | Polars | Notes |
|---|---|---|
| `pd.to_datetime(s)` | `s.str.to_datetime()` | Method on the string column, not a free function. |
| `pd.to_datetime(s, format="%m/%d/%Y %I:%M:%S %p")` | `s.str.to_datetime(format="%m/%d/%Y %I:%M:%S %p")` | Same strftime codes (chrono). Date-only → `.str.to_date(...)`. |
| `pd.to_datetime(s, errors="coerce")` | `s.str.to_datetime(strict=False)` | Unparseable → `null` instead of raising. |
| `s.dt.year` | `pl.col("c").dt.year()` | Method call, not property. Same for `.month()`, `.day()`, `.hour()`. |
| `s.dt.strftime(fmt)` | `pl.col("c").dt.to_string(fmt)` | |
| `type(x) == pd.Timestamp` *(in tests)* | `isinstance(x, datetime)` / check `df.schema["c"] == pl.Datetime` | Polars scalars come out as stdlib `datetime.datetime`. Rewrite these test asserts — they appear in hw02A. |

---

## apply / map — prefer native expressions

Corpus uses: `.map(dict)`, `.map(lambda)`, `.apply(lambda)` (rare). In order of preference:

1. **Dict mapping** — `s.map({True: "Yes", False: "No"})` →
   `pl.col("c").replace_strict({True: "Yes", False: "No"})`.
   Exact pandas semantics (unmapped → missing): add `default=None`. If unmapped values should
   pass through unchanged instead, use `replace`.
2. **Anything expressible natively** — `s.map(lambda x: "Yes" if x == -1 else "No")` →
   `pl.when(pl.col("c") == -1).then(pl.lit("Yes")).otherwise(pl.lit("No"))`. This covers most
   corpus lambdas (bucketing, thresholds, first-element-of-split).
3. **Last resort** — `pl.col("c").map_elements(f, return_dtype=pl.Utf8)`. Slow, and Polars warns;
   `return_dtype` is required to avoid a warning. If reaching for this, first check whether a
   `.str`/`.list`/`when-then` expression does the job.

---

## String operations

`.str` namespace, as in pandas, with renames and one structural upgrade.

| Pandas | Polars | Notes |
|---|---|---|
| `s.str.len()` | `.str.len_chars()` | |
| `s.str.replace(pat, repl)` | `.str.replace_all(pat, repl, literal=True)` | **`literal=True` is mandatory when the pattern is not meant as a regex.** pandas 2.x `Series.str.replace` defaults to `regex=False`; Polars treats the pattern as a regex. Verified: `.str.replace_all(".", "")` returns **empty strings** — it deletes every character — where pandas removed only literal dots. It raises nothing, so a county/name column silently becomes blanks. Any pattern containing `. ^ $ * + ? ( ) [ ] { } \|` needs `literal=True` or proper escaping. |
| `sum(1 for c in text if c.isupper())` (a Python char-class loop) | `.str.count_matches(r"\p{Lu}")` | **Not `[A-Z]`.** Python's `isupper()`/`isalpha()`/`isdigit()` are Unicode-aware; the ASCII class silently undercounts on accented text — 8 of 7513 subjects differed in projB2, with no test asserting it. Use the Unicode property classes: `\p{Lu}` upper, `\p{Ll}` lower, `\p{L}` letter, `\p{N}` digit. **A character class is a place a conversion changes numbers with nothing to catch it** — when replacing a Python loop with a regex, match the loop's Unicode semantics, not its obvious ASCII shape. |
| `s.str[a:b]` | `.str.slice(a, b - a)` | **Second arg is a length, not a stop.** |
| `s.str.lower()` / `.upper()` | `.str.to_lowercase()` / `.str.to_uppercase()` | |
| `s.str.replace(pat, repl)` | `.str.replace_all(pat, repl)` | pandas replaces all matches; Polars `replace()` does only the **first**. `regex=False` → `literal=True`. |
| `s.str.contains(pat)` | `.str.contains(pat)` | Regex default; `literal=True` for plain substring. |
| `s.str.extract(pat)` *(one group)* | `.str.extract(pat, 1)` | Group index defaults to 1; `0` = whole match. |
| `s.str.extract(pat_with_named_groups, expand=True)` *(multi-group → DataFrame)* | `.str.extract_groups(pat)` then `.struct.unnest()` | Named groups (`(?P<Lat>...)`) become struct fields, unnested to columns — direct replacement for the lab03 lat/lon pattern. Polars regex uses `(?<name>...)`; `(?P<name>...)` also accepted. |
| `s.str.split(d)` | `.str.split(by=d)` | Returns a `List` column. |
| `s.str.split(d, expand=True)[0]` | `.str.split(d).list.get(0)` | The corpus `iid → bid` idiom. Fixed-arity alternative: `.str.split_exact(d, n)` → struct. |
| `s.str.findall(pat)` | `.str.extract_all(pat)` | List column of matches. |
| `s.str.isnumeric()` | `.str.contains(r"^\d+$")` | No direct method — regex it. |

---

## Visualization

**Decision (course-wide): keep seaborn / matplotlib / plotly. No hvPlot, no Altair.**
Notes usage: 227 `np.`, 191 `plt.`, 73 `sns.`, 46 plotly, 30 sklearn touchpoints. Apply the interop
ladder above — direct first, `.to_numpy()` only where NumPy dispatch refuses, `.to_pandas()` only
with a recorded reason.

- **seaborn** — the one library that may need rung 3. Try Polars Series for `x=`/`y=` first; fall
  back to `data=df.to_pandas()` and allowlist it. Pass the **Series**, not a bare array: with `data=`
  present, an ndarray has no name for seaborn to reconcile against the frame's columns, so
  `.to_numpy()` there is actively worse than leaving it.
  - `sns.distplot` (appears 2× in corpus) is **removed in modern seaborn** — replace with
    `sns.histplot(..., kde=True)` or `sns.displot` while converting, independent of Polars.
- **matplotlib — pass the Series directly**: `plt.plot(df["x"], df["y"])`. `plot`, `scatter`, `bar`
  and `hist` all accept Polars Series. This corrects earlier guidance in this file that called
  `.to_numpy()` "the uniform safe pattern": a corpus-wide cleanup in the sister repo deleted ~100
  such conversions with every gate staying green. Add it only when the *result* is used as an
  ndarray.
- **plotly.express** — accepts Polars DataFrames natively (`px.line(df, x=, y=)`). No conversion.
- **scipy / statsmodels** — `scipy.stats.pearsonr`, `cdist`, and anything else coercing via
  `np.asarray` take a Series directly. Only the NumPy reduction family refuses; see the dispatch
  rule under The interop ladder.
- **scikit-learn** — accepts Polars frames for `fit`/`predict` directly;
  `set_output(transform="polars")` keeps transformer output in Polars.

---

## Display configuration — the output is page layout

pandas display options set in a hidden `remove-cell` setup cell control how every table in the
chapter renders. `content/eda/eda.ipynb` is the case to copy from: it sets `display.max_rows`,
`display.precision`, and `display.float_format` before anything else runs.

| Pandas | Polars |
|---|---|
| `pd.set_option("display.max_rows", n)` | `pl.Config.set_tbl_rows(n)` |
| `pd.set_option("display.max_columns", n)` | `pl.Config.set_tbl_cols(n)` |
| `pd.set_option("display.precision", n)` | `pl.Config.set_float_precision(n)` |
| `pd.set_option("display.float_format", fmt)` | `pl.Config.set_float_precision(n)` — no format-string equivalent; pick the precision the prose assumes |
| *(no equivalent)* | `pl.Config.set_tbl_hide_dataframe_shape()` — consider it, but see below |

Two differences change what a reader sees on the page:

- **Polars prints a shape header and a dtype row that pandas did not.** `shape: (5, 3)` above the
  table and `str / i64 / f64` under the column names. That is information pandas hid, and it is worth
  keeping — dtypes are a course topic. Do not hide the shape header just because the old page did not
  have one; that is cosmetic pandas-matching applied to layout.
- **Set configuration once, in the chapter's existing setup cell.** Scattering `pl.Config` calls
  through a chapter puts layout decisions in the middle of a narrative about data. If the setup cell
  carries `remove-cell`, leave that tag exactly where it is.

## The interop ladder

Polars goes to the plotting and modeling libraries **directly** wherever that works. Reach for a
conversion only when it does not, and take the cheapest one that does:

1. **Pass the Polars object.** This is where nearly everything belongs. plotly express,
   scikit-learn (`fit`/`predict`/`train_test_split`), `confusion_matrix`, **matplotlib**
   (`plt.plot`, `scatter`, `bar`, `hist`), `scipy.stats.pearsonr`, `cdist` and statsmodels all take
   Polars frames and Series as-is.
2. **`.to_numpy()`** only when NumPy dispatch actually refuses, or when the *result* is then used as
   an ndarray (a chained `.round()`, `[..., np.newaxis]`). See the dispatch rule below — it decides
   this, and it is a shorter list than it looks.
3. **`.to_pandas()` — last resort, and it needs a written reason.** Every surviving call is
   allowlisted in `conversion/conversion_allowlist.yml` with an entry saying why Polars could not go
   in directly. The gate blocks on unallowlisted ones. This is deliberate friction: `.to_pandas()`
   applied by reflex leaves a chapter that teaches Polars and runs on pandas.

### The dispatch rule that decides every `.to_numpy()` boundary

NumPy routes `min`/`max`/`sum`/`mean`/`std`/`var`/`all` through `_wrapreduction`, which calls the
object's own method with `axis=`/`out=`. Polars signatures reject those kwargs, so **those raise on a
Series**. Everything routed through `asarray`/`asanyarray` instead — `np.median`, `np.corrcoef`,
`np.isclose`, `np.allclose`, `np.percentile`/`np.quantile`, ufuncs like `np.log`, scipy's `cdist`,
sklearn, geopandas — **takes a Series directly**.

Prefer the native reduction over routing through NumPy at all: `s.mean()` or `pl.col("x").mean()`
inside an expression reads better and keeps the work in Polars.

**Verified equivalent, so swap freely:** `mean`, `sum`, `min`, `max`, `median`.

**Verified NOT equivalent — these need a keyword, not a NumPy detour:**

| native | NumPy | fix |
|---|---|---|
| `s.var()` / `s.std()` — `ddof=1` | `np.var` / `np.std` — `ddof=0` | `s.var(ddof=0)` |
| `s.quantile(q)` — `nearest` | `np.percentile` — `linear` | `s.quantile(q, interpolation="linear")` |

Neither raises. They just move the number — and variance ratios are how every $R^2$ is computed, so
a quiet `ddof` flip shifts printed values and anything derived from them.

**Accepting is not the same as equivalent.** `np.percentile(s, q)` runs happily and gives NumPy's
linear interpolation where `s.quantile(q)` defaults to `nearest`; swapping silently reassigns rows to
different quartiles. Those keeps are about semantics, not errors.

**The one genuinely unavoidable conversion:** comparing an sklearn prediction against Polars labels.
`lr.predict(X) == y` and `y == lr.predict(X)` both raise, in both directions, so one side has to
become an ndarray.

**Judge the receiver as executed, not as defined.** A method that looks safe where it is written can
be reached with a different type at run time — the sister repo had 17 `.to_numpy()` removals pass a
definition-level probe and then get reverted by the execution gate.

The known rung-3 case is **seaborn with `data=`**. Seaborn 0.13 nominally accepts Polars through the
interchange protocol, but `hue` ordering, `lmplot`, and dtype introspection are flaky through that
path. Before writing `.to_pandas()`, try the two cheaper forms: pass the columns as Polars Series
(`sns.scatterplot(x=df["a"], y=df["b"])`), or hand seaborn what it actually needs rather than the
whole frame. Note the trap below — with `data=` present, converting `x=`/`y=` to bare arrays is
*worse* than leaving them, because an array has no name to reconcile against `data`'s columns.

---

## Traps found the hard way

Each of these broke a real notebook build during the assignment conversion. They are reproduced
unchanged because they are properties of the libraries, not of the assignments.

- **NumPy reductions fail on a Polars Series.** `np.mean(s)`, `np.all(s)`, `np.sum(s)` raise
  `TypeError: … unexpected keyword argument 'axis'`. Use the native `s.mean()`, `s.all()`, `s.sum()`.
  `np.isclose(s.sum(), v)` is fine — the reduction just has to happen on the Polars side first.
- **In a helper whose argument may be either a Series or an ndarray, write the reduction as a
  method on the expression**: `((actual - predicted) ** 2).mean()`, not `np.mean(...)`. RMSE/MSE
  helpers get called with Series−ndarray, ndarray−Series, and ndarray−ndarray from different
  question cells, and this one form survives all of them — mixed subtraction returns a Polars Series
  either way. Converting the call sites instead means chasing every combination.
- **`np.percentile` / `np.quantile` must NOT be swapped to `.quantile()` either.** Polars defaults to
  `interpolation="nearest"`; NumPy interpolates linearly. On the same data
  `np.percentile(s, [25, 50, 75])` gives `[1.725, 2.9, 4.0]` while `s.quantile(q)` gives
  `[2.0, 2.9, 4.5]` — verified. It raises nothing and the numbers look plausible, so it silently
  moves quartile boundaries and reassigns rows to different quartiles. Either keep `np.percentile`
  (it accepts a Polars Series directly and returns the pandas values) or pass
  `interpolation="linear"` explicitly. Expect this in any EDA or stats lecture that labels quartiles.
- **Except `np.var` / `np.std`, where the native swap silently changes the number.** Polars defaults
  to `ddof=1`, NumPy to `ddof=0`: for `[1,2,3,4,5]`, `s.var()` is 2.5 and `np.var(arr)` is 2.0. Prefer
  `s.var(ddof=0)` over `np.var(s.to_numpy())`: same number, stays in Polars, and the parameter is
  visible instead of implied by which library you routed through. This one does not raise — it just
  shifts every result. Variance ratios are how every $R^2$ in the modeling labs is computed, so a
  quiet `ddof` flip moves printed values and any constant derived from them.
- **`pl.DataFrame` has no `.T`, and no frame-to-frame `@`.** The normal equation `X.T @ X` — not rare
  in a modeling lab — has no Polars form. `transpose()` exists but returns a frame, which still has
  no `__matmul__`. Cross to NumPy first: `X, Y = np.asarray(X), np.asarray(Y)`. The failure is
  asymmetric and so easy to miss: `frame @ ndarray` *works* and returns an ndarray; only
  `frame @ frame` raises.
- **Not every NumPy boundary needs `.to_numpy()`.** A Polars DataFrame implements `__array__`, so
  `np.concatenate([bias, X], axis=1)` takes one directly. The conversion is required for *reductions*
  that pass `axis=`, not for array construction. Over-converting is harmless but obscures which
  crossings are load-bearing.
- **`model.predict(X) - Y` returns a Polars Series**, so `np.mean(resid ** 2)` fails. Write
  `((model.predict(X) - Y) ** 2).mean()`.
- **`df.info()` does not exist** → `df.glimpse()`. And `describe()` includes string columns (pandas
  dropped them), so prose claiming non-numeric columns "are not shown" needs rewriting.
- **`df.fill_null(<scalar>)` silently *skips* columns whose dtype cannot hold the scalar** rather
  than raising: `fill_null(0)` on a frame with a String column leaves that column's nulls in
  place. The result is a quietly under-filled frame with no error to notice. Fill per column
  when the frame is mixed.
- **`fill_null` on a Boolean column with a float mean raises.** Guard with
  `if df[col].is_null().any():` before filling, or cast first.
- **Seeded sampling:** pandas `df.sample(n, replace=True)` rides the NumPy RNG. Polars `.sample()`
  uses its own stream, so seeded values drift. **Two fixes, for two different needs.** When the tests
  pin exact pandas values, `df[np.random.randint(len(df), size=len(df))]` reproduces pandas under the
  same `np.random.seed` — verified bit-identical on hw06. When the tests are tolerance-based and you
  only need run-to-run determinism, add `pl.set_random_seed(<same seed>)` beside the existing
  `np.random.seed(...)` and keep `.sample(..., with_replacement=True)`; this is far cheaper and is
  what lab08 uses. Seeding each `.sample()` call individually is wrong — it makes every iteration of
  a simulation identical.
- **`sns.load_dataset(...)` returns a *pandas* DataFrame**, so it is a pandas site that no `pd.`
  or `import pandas` scan will find. Wrap it: `pl.from_pandas(sns.load_dataset("tips"))`.
- **Sort ties differ** (pandas quicksort vs Polars stable), so equal-key rows can come back in a
  different order. Regenerate affected constants from the executed solution; don't force the order.
- **`is_in` with a Series** warns about ambiguity in 1.43+. Fine for now; pass a list where practical.
- **`np.int64` scalar × `pl.Series` raises**: `TypeError: unsupported type 'numpy.int64'`, out of
  `Series.__array_ufunc__`. A plain Python `int`, an `np.float64`, and a full ndarray all multiply
  fine — only the integer NumPy *scalar* fails, which makes this look like "arithmetic works" until
  it doesn't. The usual source is an int-dtype parameter vector: `np.array([0, 0])` blows up on the
  first gradient-descent step where `np.array([0.0, 0.0])` is fine. Common in modeling labs, and it
  often sits in a helper that ships to students verbatim, so the question becomes unanswerable.
  **Fix it at the parameter-vector literal, not at the arithmetic site.** The arithmetic is usually
  the thing being taught (`theta_1 * X` *is* the model equation), and converting there pushes a
  NumPy boundary into a function whose job is to read like maths. Changing `np.array([0, 0])` to
  `np.array([0.0, 0.0])` is two characters in something that was already conceptually a float vector.
- **`pl.Series == np.ndarray` raises, in both directions.** Distinct from the reduction trap above and
  easy to miss because most *arithmetic* between the two works (`Y * arr`, `1 - Y`). Comparison
  fails: `s == arr` gives `TypeError: cannot convert Python type 'numpy.ndarray' to Int64`, and
  `arr == s` gives `TypeError: No loop matching the specified signature and casting was found for
  ufunc equal`. Add `.to_numpy()` on the Polars side. This is the dominant edit wherever an sklearn
  `.predict()` result meets Polars labels — accuracy computations, `correct` columns, confusion
  matrices — so expect it in every classification unit.
- **sklearn takes Polars frames directly** — `train_test_split`, `.fit`, `.predict` all work, and
  `feature_names_in_` is populated. `train_test_split` also accepts a Polars *Series* and returns
  Polars on both sides, and `confusion_matrix` accepts a Polars Series as `y_true`. Single-row
  prediction needs `[df.row(i)]`, not `df[i]`. Don't add `.to_numpy()` churn where it isn't needed —
  but remember `.predict()` hands back an ndarray, so the comparison trap above applies downstream.
- **Iterative solvers drift in the low digits.** Reordering a reduction to Polars' native `.mean()`
  changes float accumulation order, which moves `scipy.minimize`'s path — lab10's `theta_hat` shifted
  at the 7th decimal. Tests with tolerances are unaffected; the thing that goes stale is *prose
  quoting the optimizer's output*, including display equations. This is a third equivalence category
  beyond tie-breaks and null-vs-NaN: the tell is a value written into markdown rather than asserted.
- **`.to_numpy()` is for matplotlib, not for seaborn's `x=`/`y=`.** When you pass `data=`, converting
  the axis arguments to bare arrays breaks seaborn: an array has no name to reconcile against
  `data`'s columns, and `sns.displot(data=df.to_pandas(), x=<ndarray>)` raises
  `ValueError: Cannot mask with non-boolean array containing NA / NaN values`. Pass the **Polars
  Series** (`np.log10(df['inc'])` keeps the name `inc`) or drop `data=` entirely. Reaching for
  `.to_numpy()` as a uniform safe pattern is actively wrong here.
- **`plt.hist` / `plt.barh` need `.to_numpy()`**; seaborn needs `data=df.to_pandas()`; plotly express
  takes Polars natively. **When the *student* writes the plotting call, the handoff has to be taught,
  not just performed** — a question that asks for a seaborn plot needs `.to_pandas()` stated in its
  hint block, or the student hits an error the prompt gave them no way to anticipate. Converting only
  the provided cells passes every gate and still leaves the question unanswerable. The same notebook
  often converts for seaborn and not for plotly, which reads as arbitrary unless one hint says why.
- **A conversion that introduces an intermediate variable invalidates prompts that point at the old
  line.** `sns.heatmap(df.corr(), …)` becomes `corr_matrix = df.corr()` plus a call that uses
  `corr_matrix` three times, so a prompt reading "modify the data passed to `sns.heatmap`" now aims a
  student at the wrong line. Re-point the prompt at the new variable, and mark conversion-introduced
  scaffolding (`xticklabels=`, `yticklabels=`) the way the notebook marks its other scaffolding —
  otherwise it is silently load-bearing and a student can delete it without knowing.
- **duckdb**: `pd.read_sql(q, "duckdb:///f.db")` → open one connection and use `conn.query(q).pl()`.
  connectorx is not installed, so `pl.read_database_uri` is unavailable. If a `%sql` magic already
  holds the file open, connect in-memory and `ATTACH … (TYPE sqlite)` rather than opening it twice.
  Run `INSTALL sqlite` on that connection, not on the module-level `duckdb` default.
  **One connection per database.** lab09 has two (`imdbmini.db`, `fec_nyc.db`), and attaching both to
  a single connection fails at query time: `USE` is per-connection and an unqualified table name does
  not search other catalogs, so you get `Catalog Error: Table with name Title does not exist! Did you
  mean "imdb.Title"?`. Student SQL uses bare table names, so give each database its own connection
  and `USE` — or qualify every table, which means editing the questions.
- **Dtype drift across the SQL boundary is expected.** `conn.query(q).pl()` types columns differently
  than `pd.read_sql` did. Observed through a sqlite `ATTACH` (lab09, verified live):

  | SQL | Polars dtype | note |
  |---|---|---|
  | `SUM(<bigint>)` | `Decimal(38, 0)` | duckdb widens BIGINT sums to HUGEINT. Prints without a decimal point and `Decimal('1000') == 1000` is True, so it passes some tests silently and fails others |
  | `COUNT(*)` | `Int64` | |
  | `CAST(x AS int)` | `Int32` | not Int64 |
  | sqlite `TEXT` holding numbers | `String` | stays a string even when every value is numeric |

  A `.cast(pl.Int64)` in the test is the sanctioned fix — it makes the intent explicit rather than
  relying on `Decimal`/`int` comparing equal by luck.
- **jupytext collision**: a markdown line matching `^\s*%%\s` (e.g. a literal `    %% sql` inside a
  fenced block) is read back as a cell marker and splits the cell. `%%sql` with no space is safe.

## Sections carried over unchanged

No conversion needed; keep using the original sheet for:

- **Regular expressions** — stdlib `re` and the pattern syntax (Polars `.str` methods take the
  same regex syntax; only `(?P<name>)` vs `(?<name>)` styling differs, and both parse).
- **SQL** — syntax, clauses, and `%%sql` magic cells all unchanged; only the
  `pd.read_sql` → `pl.read_database` hand-off moves.
- **Modeling / probability formulas** — variance, correlation, loss functions, least squares,
  ridge/LASSO, normal equation, R², gradient descent, bias-variance.
- **NumPy** — `np.random.*` (seeded sampling in hw05), `np.linalg`, array math: untouched.
  Matrix cells using `.T` / `@` on arrays stay NumPy; only cross the DataFrame boundary with
  `.to_numpy()`.
- **scikit-learn** — estimators and metrics unchanged (see Visualization section for the
  interop notes).

---

*Coverage basis: the mapping tables were built from an AST inventory of the 26 Data 100 assignment
masters and every mapping was executed against Polars 1.43.1. Cross-checked against this repo's
notes corpus (24 notebooks, `conversion/nb_triage.py`), whose highest frequencies are `.head/.tail`
125, `pd.DataFrame` 44, `.groupby` 37, `pd.read_csv` 31, `.iloc[` 24, `.loc[` 19, `.str.` 16,
`.agg` 16, `.sort_values` 13. The notes corpus contains **zero** `MultiIndex`, `.query()`, and
`.apply()` calls, so those rows are carried for completeness rather than because you will meet them.
Two chapters — `sql_I` and `sql_II` — are pure `%%sql`/jupysql/duckdb and contain no pandas at all.*
