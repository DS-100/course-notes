# Fa26 course conventions — the Polars students actually see

Companion to `SKILL.md`. That file maps pandas to Polars. This one records **which** Polars spelling
the Fa26 course uses in lectures, discussions and homework released through 2026-09-22, so newly
authored chapters (`new_eda_1` … `new_eda_5`) match the code students are reading every week.

Unless noted, every path is under `/Users/jedwin321/Documents/fa26-dev/`, and every claim was
executed against polars 1.43.1 in the `d100` env.

Students did **not** read `polars_1`/`polars_2`. A new chapter introduces each Polars verb where it
first uses it, in one or two sentences, and does not send the reader elsewhere for the basics.

## Use these spellings

| Task | Write | Source |
|---|---|---|
| Read a CSV | `pl.read_csv("data/…csv")` | L02 S18, `lec04.ipynb` c3 |
| Rows / shape | `df.shape`, `df.height`, `len(df)` | L02 S25, disc02 c19 |
| Pull out one column as a Series | `df["col"]` — brackets only for this | `polars-tutorial` c22 |
| Choose columns | `df.select("a", "b")` | L03 S11 |
| Keep rows | `df.filter(pl.col("x") <= 1)` | L02 S33 |
| New column | `df.with_columns(app_rate=pl.col("applied") / pl.col("grade_12"))` — keyword form | L02 S31, `lec04` c4 |
| Sort | `df.sort("x", descending=True)` | L02 S28 |
| Summary stats | `df.select("x").describe()` | L02 S38 |
| Frequency table | `df["city"].value_counts(sort=True)` → columns `city`, `count` | L03 S24, hw01 c50 |
| **Rows per group** | `df.group_by("county").len()` → columns `county`, `len`; or `.agg(num_schools=pl.len())` | L04 S13, disc02 c14/c47, hw02 c21 |
| **Number of distinct values** | `df["county"].n_unique()` | disc02 c9/c29, hw01 alt |
| Aggregate per group | `.group_by("k").agg(total=pl.col("cost").sum())` — keyword names | L04 S16, hw02 c15 |
| Top rows per group | `df.sort("admitted", descending=True).group_by("county").head(2)` | L04 S18 |
| Group on two keys | `group_by("a", "b")` — positional | L04 S21, `lec04` c33 |
| Rank-based percentile | `pl.col("x").rank() / pl.col("x").count()` | L04 S28, `lec04` c7 |
| Quantile bins | `pl.col("p").qcut(4, labels=["0-25", "25-50", "50-75", "75-100"])` | `lec04` c9 |
| Nulls | `is_null` / `is_not_null` / `fill_null(0)` / `drop_nulls(subset=…)` / `null_count()` | `lec04` c11/c20, hw02 c58 |
| Conditional value | `pl.when(cond).then(a).otherwise(b)` | hw01 c59, `lec04` c28 |
| Join | `a.join(b, on="key", how="inner")` | L06 S20, hw02 c27 |
| Seaborn | pass the Polars frame: `sns.histplot(df, x="app_rate")` | L02 S42–43, L03 S28/35, `lec04` c13 |
| Plotly | pass the Polars frame: `px.scatter_3d(df, …)` | `lec04` c35 |

**The count-unique convention, precisely.** The staff hunch that lectures count distinct groups
with `len(df.group_by(...))` does not survive a search. It appears in no lecture, discussion,
homework or slide. What they do use:

- `df.group_by(k).len()` for **rows per group**.
- `s.n_unique()` for **how many distinct values**. hw01 c34/c68 also accepts `len(s.unique())`.

The two agree (54 counties both ways on the UCB data), but they answer different questions, so
use the one whose question the prose is asking. `pl.count()` never appears. `pl.col(c).count()`
counts **non-null** values, which is how L04 S28 builds the percentile denominator. Never use it
to mean "distinct" (disc02 groupwork c8 does exactly that under a "Unique names" heading).

## Where the book deliberately differs from the lectures

- **Sorting a nullable column before `head`/`tail`.** Polars puts nulls first. `grade_12`,
  `is_charter`, `pct_free_reduced` and `dist_to_ucb_miles` each have 35–94 nulls in
  `pivoted-ucb-data-w-everything.csv`. Pass `nulls_last=True` when the output shows the top rows
  (AGENTS rule 8). The lectures never do this.
- **Categorical columns into seaborn.** `qcut` returns `Categorical`. In the `d100` env
  (pyarrow 18) seaborn's interchange path raises
  `ArrowTypeError: Converting unsigned dictionary indices to pandas not yet supported` for both
  `Categorical` and `Enum`. The course env's newer pyarrow does not. Add `.cast(pl.String)` to the
  bin labels before plotting; the labels above sort correctly as strings. Do not reach for
  `.to_pandas()`.
- **Randomness.** `lec04`/`lec05` use the `polars_random` plugin, which is not in `requirements.txt`.
  Use `np.random.default_rng(<seed>)` and `pl.Series(...)`/`pl.lit` instead, and always seed.
- **`group_by` output order is not stable.** Follow it with `.sort(...)` whenever the rendered
  table or the prose depends on the order (`polars-tutorial` c35). Don't use `maintain_order=True`
  in chapters.
- **Figures.** End every plotting cell so that no `<Axes: …>` repr leaks: a trailing `;`, or
  `plt.show()`. Give each one a `#| fig-alt:` line.

## The English | Polars | SQL triple

The decks put each operation in three columns: **English** / **Polars** / **SQL**. `main`'s draft
`new_eda_1` repeats it as three consecutive markdown cells after the live cell. Chapters keep the
idea, but:

- the live code cell is the Polars version, so the triple must not print that code a second time;
- the SQL is real SQL that runs in DuckDB against the same CSV — `DESC`, not `DSC`, and no
  `SELECT` alias inside `WHERE`.

## Slide and assignment bugs not to copy

| Where | What it says | Correct |
|---|---|---|
| L02 S31 | `df = pd.read_csv(...)` in the Polars column | `pl.read_csv` |
| L04 S16 | `group_by("customer_id").sum().sort("sum_cost", …)` | `.sum()` keeps the name `cost`, so sort on `"cost"` or name it in `agg` |
| L04 S37 | `grade_12 = pl.col('grade_12').sum,` | `.sum()` |
| L04 S18 | SQL `GROUP BY county ORDER BY admitted DESC LIMIT 2` as "top 2 per county" | That is 2 rows total. Per-group top-k needs a window: `QUALIFY ROW_NUMBER() OVER (PARTITION BY county ORDER BY admitted DESC) <= 2` |
| disc02 groupwork c8 | `pl.col('Name').count()` under "Unique names" | `pl.col('Name').n_unique()` |
| `lec04` c38 | trailing `.` (syntax error) | — |
| `lec05` | reads `data/…` with no `data/` folder beside it | — |

## Not yet on the course reference sheet (open question for staff)

`reference/build_polars_section.py` has no `pl.len()`, `group_by().len()`, `qcut`, `rank`,
`unpivot`, `.dt`, `pl.Config`, or plotly entry, though lectures and homework through hw03 use all
of them. It also tells students seaborn needs `data=df.to_pandas()`. The slides and `lec04`/`lec05`
pass Polars directly, and `polars-tutorial` c42 says the same.

`SKILL.md` contradicts itself on matplotlib: its Visualization section passes Series to
`plt.hist`/`plt.bar`, while the Traps section (line ~542) says they need `.to_numpy()`. Under 1.43.1,
`plt.hist(df["app_rate"])` and `plt.bar(series, series)` both work. This is recorded here and
left for whoever owns `SKILL.md`.
