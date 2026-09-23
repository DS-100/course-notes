# EDA I–V outlines: `new_eda_1` … `new_eda_5`

**Status: approved (2026-09-22)** -- all five chapters. Every open question not listed below takes the outline's recommended default.

### Decisions already made (2026-09-22)

These override the matching open questions below. Every other open question stays open until the outlines are approved.

- **Checks the lecture never ran: keep them.** EDA III §10 keeps the mean-of-rates column (EDA III OQ5). EDA III §14 includes the "ignore lands outside the possible range" beat (EDA III OQ4). EDA IV §4 keeps the 0/2 bounds on attendance (EDA IV OQ3). EDA IV §6 keeps the county check and the histogram with cutoffs (EDA IV OQ5).
- **School names: name them as the data shows.** Names may appear in output tables and be read off in the prose. EDA I §13 says "a later homework asks you to diagnose it", not "Homework 2" (EDA I OQ5). EDA IV §9 ends on "do any schools stand out?" and does not build a table of five picks (EDA IV OQ7).
- **EDA V: the core sections only.** Keep every section, including `pl.read_database` on `example_duck.db` (EDA V OQ7). Drop the three optional items (EDA V OQ8): the chained star-schema join and its `name_right` sentence (§11), the `validate="m:1"` tip (§10d), and the `State`/`Location`/`Device` check (§7b).

These are the outlines for the five Fa26 EDA chapters, built from lectures L02–L06. One outline agent wrote each chapter, and an overlap critic then reconciled the five. No chapter has been built yet. To approve a chapter, change its `**Status: draft**` line to `**Status: approved**`. The build pass (`eda-chapters` with `args.phase = "build"`) starts once the chapters are approved and the orchestrator has copied the data and images listed below.

Every number in these outlines was executed in the `d100` env: polars 1.43.1, seaborn 0.13.2, duckdb 1.3.0 and statsmodels 0.14.4. The build pass must re-check each number against executed output. None of them is prose to paste.

## Scope

| Chapter | Title | Lecture scope |
|---|---|---|
| `new_eda_1` | EDA I | L02 S5–S61 |
| `new_eda_2` | EDA II | L03 S9–S49. S12–S26 repeat L02 S45–S60, so the chapter keeps only what EDA I did not already cover. |
| `new_eda_3` | EDA III | L04 S11–S46. S4–S10 recap EDA II. |
| `new_eda_4` | EDA IV | L05 S4–S19 only: finishing the UCB case study |
| `new_eda_5` | EDA V | L05 S20–S60 (key data properties, joins, file formats, faithfulness) and L06 S39–S51 (DBMS, why SQL, schema, keys, star schema). L06 S4–S38 repeat L05 and add only the Polars join line on S20. |

**Coverage.** Every slide in every deck has a disposition row: L02 1–61, L03 1–49, L04 1–46, L05 1–61 and L06 1–52. Deck chrome is marked Deleted. No in-scope slide is taught in two chapters, because each repeated range has exactly one owner:

| Repeated material | Owner | Where |
|---|---|---|
| L03 S12–S26 = L02 S45–S60 | EDA I | §18–§22. This is the extension past `main`'s draft, which stops at S45. |
| L04 S4–S10 = L03 S42–S48 | EDA II | §7–§9 |
| L06 S4 = the L04 S45 and L05 S9/S11 plots | EDA IV | §1, §4, §6 |
| L06 S5–S38 = L05 S20–S60 | EDA V | L06 S20's Polars join line goes in §8b. |
| `lec04.ipynb` c31–c43 = `lec05.ipynb` c16–c28 | EDA IV | §5–§9. EDA III stops at L04 S45. |

## What the critic changed

Edits inside the outlines are marked *critic*.

**Overlaps resolved**

1. **Frame name.** All five chapters now use `admissions`. EDA IV §3 had used `lec04`'s `uce`.
2. **`nulls_last=True`** is introduced once, in EDA I §12. EDA II §5 and EDA III §4 had each claimed to introduce it, and now they only recall it.
3. **`value_counts(sort=True)`, `DataFrame.head(n)` and SQL `GROUP BY`/`LIMIT`** are introduced in EDA I §21. EDA II had listed them conditionally, and EDA III had listed `.head(n)` and `LIMIT` as its own.
4. **`df.height`** was used from EDA III onward but never introduced. It now joins EDA I §8's row-count beat, which is where the conventions file puts it (L02 S25).
5. **`pl.DataFrame({...})` and Series `n_unique()`** belong to EDA III (§3 and §2). EDA V had claimed both. It now introduces only the list-of-records constructor and `DataFrame.n_unique()` on a two-column `select`.
6. **Sorting on several keys** first appears in EDA III §4 (see item 12), not EDA IV §5.
7. **`.null_count()`, `pl.when` and the seeded imputation** belong to EDA III. EDA IV's "only if EDA III doesn't" entries are removed.
8. **`plt.subplots`/`ax=`** first appear in EDA I §18's folded cell. EDA I now gives them one sentence, so EDA III (whose only new part is `sharey=True`) and EDA IV no longer list them as new.
9. **The "a null means 0, 1 or 2" check.** EDA III §12 does it for `admitted`. EDA IV §3 now checks only `attended` instead of repeating both.
10. **Weighted vs unweighted `avg_app_rate`.** EDA II §7 defines it in one sentence. The side-by-side comparison stays in EDA III §10 (L04 S35).
11. **String equality in `filter`** first appears in EDA IV §6, where the county check keeps one distance quartile, not in §9.

**Verbs used before they were introduced**

12. **EDA III §4, top two schools per county.** The draft said a final sort on `county` then `admitted` makes the output deterministic. It doesn't. In 11 counties the second- and third-ranked schools tie on `admitted` (San Diego at 29, Riverside at 19, Kern, Napa and Sonoma at 7, Yuba at 3, and five counties where both are null), so the school `head(2)` keeps depends on how the sort orders ties. The sort now uses `"school"` as a tie-breaker, and the SQL gets `ORDER BY admitted DESC, school`. The 101 rows were checked equal in DuckDB.
13. **EDA II §7's folded cell** uses `qcut`, `group_by().agg()`, `.cast(pl.String)` and `sns.lineplot` a chapter before EDA III teaches them. Fidelity check 5 blocks that, because it counts every live cell, folded or not. The fix is one sentence before the dropdown that says what each verb does. EDA III still teaches them in full. This closes EDA II OQ2 and EDA III OQ9, pending approval.
14. **EDA I's folded cells** use `.quantile(q)`, `ax.annotate` and `stat="density"`. Each now gets a sentence or a clause before its dropdown.
15. **EDA V §8d** uses `.drop()`, which was missing from its verb table. It has been added.

**Shared state and numbers**

16. **EDA IV §1 did not reproduce EDA III's figure.** Its admission rates (0.130 and 0.151) come from drawing the random 0–2 values over all 1,229 rows. EDA III draws over the 1,173 bucketed rows and gets 0.123, 0.129, 0.152 and 0.149 (re-checked in `d100`). EDA IV §1 now copies EDA III §13's cell verbatim with seed 7342. It also uses `<= 1` rather than the lecture's `< 1`, which keeps the same 1,229 rows. EDA III owns the seed, and EDA IV §3 reuses it.
17. **City counts depend on the frame.** EDA I §21 counts the 1,268-row frame and EDA II §9 the 1,229-row frame, so they disagree on Los Angeles (112 vs 100) and Sacramento (28 vs 27). Both are correct, and EDA II now says why in a clause.
18. **Setup cells.** EDA II–IV now copy EDA I's `pl.Config.set_fmt_str_lengths(40)`, since school names run to 35 characters. EDA III's setup had said "matching EDA I", which is corrected: EDA III imports `numpy` and EDA I does not.

**Images manifest**

19. The md5s in `images_manifest.yml` were recomputed from the media files. The image agents had the L03 image53–image60 md5s shifted by one file and the L06 image43/image44 md5s swapped. As a result, the workflow's dedupe dropped L03 image60 (the scatter in EDA II §4a) as a duplicate of a website screenshot. It is restored. Six keep rows are marked `copy: false` because the outlines replace them with live output: five EDA V join-result tables (one mislabels a row) and L03's re-cropped FRPM screenshot.

**Chapter open questions this closes:** EDA II OQ1, 2, 6 and 10; EDA III OQ1, 2, 8, 9, 10 and 12; EDA IV OQ1 and 2. Each is marked **Resolved (critic)** where it appears. OQ2 and OQ9 wait on approval of item 13.

## Where each Polars verb is introduced

Each verb has one owner. A later chapter recalls it in a clause and does not introduce it again. The lecture-fidelity reviewer's check 5 should read "introduced" from this table.

| Chapter | Introduces |
|---|---|
| EDA I | `pl.read_csv`; the `DataFrame` preview; `.sort(descending=)` and `nulls_last=True`; `len(df)`, `.shape`, `.height`; `df["col"]` → `Series`, with `.min()` (and `.max`/`.mean`/`.std` named); `.with_columns(name=expr)`, `pl.col`; `.filter`, comparison masks, `.is_not_null()` (in prose); `.select`, `.describe()`; `value_counts(sort=True)`, `.head(n)`; `sns.boxplot`, `sns.histplot`. In folded cells only: `.quantile`, `plt.subplots`/`ax=`, `ax.annotate`. SQL: `SELECT`, `ORDER BY … ASC/DESC`, `NULLS LAST`, `COUNT(*)`, `MIN`, `WHERE`, `GROUP BY`, `LIMIT`. |
| EDA II | `.cast(int)`; `pl.col(a) * pl.col(b)`; `sns.regplot(lowess=, line_kws=, scatter_kws=)`, `sns.scatterplot(size=, sizes=)`, `plt.xlabel`/`plt.ylabel`. Previewed in one sentence beside a folded cell: `qcut`, `group_by().agg()`, `.cast(pl.String)`, `sns.lineplot`. SQL: `CAST(TRUNC(…) AS INTEGER)`. |
| EDA III | `group_by` with `.len()`, `pl.len()`, `.agg(name=expr)`, `.head(n)` and two keys; Series `n_unique()`; `pl.DataFrame({...})`; expression `.sum()`/`.mean()`; `.sort` on several keys; `.rank()`, `pl.col(c).count()`; `qcut` and `.cast(pl.String)` in full; `is_not_null()` in a live cell, `is_null()`, `null_count()`, `fill_null`; `pl.when().then().otherwise()`; `pl.Series`, `np.random.default_rng(7342)`; `sns.pointplot`; `sharey=True`. SQL: `SUM` with `GROUP BY`, multi-column `GROUP BY`, `IS NOT NULL`, `COALESCE`, `NTILE`, and `QUALIFY ROW_NUMBER() OVER (…)`, labelled as beyond scope. |
| EDA IV | `.filter` with several predicates; string equality; an expression transformed inside `agg`; `sns.pointplot(hue=, hue_order=)`, `px.scatter_3d`, `sns.relplot(col=, col_wrap=, col_order=)`, `plt.axvline`. |
| EDA V | `.schema`; `pl.read_csv(skip_rows=, separator=, schema_overrides=, null_values=)`; `.equals()`; `pl.read_json`, `pl.DataFrame(records)`, `Struct` columns; `pl.col("a", "b")`; `.str.replace_all`, `.cast(pl.Int64)`; `DataFrame.n_unique()`; `.str.to_datetime`, `.dt.replace_time_zone`, `.dt.epoch`; `.is_duplicated()`, `.unique()`, `.is_nan()`; `.join(on=, how=, coalesce=)`, `left_on=`/`right_on=`, `validate=`; `.drop()`; `pl.read_database`. |

## Data the orchestrator copies

Every source md5 below was re-checked. Each UCB copy is lec04's file (`4c9d424f…`). Lec06's copy writes nulls as the string `"NA"`, so EDA V §7c uses it only under a new name.

| Chapter | File in `content/<ch>/data/` | Source | State |
|---|---|---|---|
| `new_eda_1` | `elections.csv`, `pivoted-ucb-data.csv`, `pivoted-ucb-data-w-enrollment.csv`, `pivoted-ucb-data-w-everything.csv` | `main` | present, tracked |
| `new_eda_1` | `world_bank.csv` | `main:content/visualization_1/data/world_bank.csv` (`05c7ef74…`) | **copy** (EDA I OQ2) |
| `new_eda_2`, `_3`, `_4` | `pivoted-ucb-data-w-everything.csv` | fa26-dev `lec/lec04/data/` (`4c9d424f…`) | present, untracked |
| `new_eda_5` | `pivoted-ucb-data-w-everything.csv` | fa26-dev `lec/lec04/data/` (`4c9d424f…`) | **copy** |
| `new_eda_5` | `pivoted-ucb-data-w-everything-na-strings.csv` | fa26-dev `lec/lec06/data/pivoted-ucb-data-w-everything.csv` (`399eec92…`), renamed | **copy** (EDA V OQ10) |
| `new_eda_5` | `elections.csv` | `main:content/new_eda_1/data/elections.csv` (`47b93a15…`) | **copy** |
| `new_eda_5` | `cdc_tuberculosis.csv` | `main:content/eda/data/cdc_tuberculosis.csv` (`3372b94a…`) | **copy** |
| `new_eda_5` | `cdc_tuberculosis.tsv` | fa26-dev `lec/lec06/cdc_tuberculosis.tsv`, at the lec06 root (`34a77f49…`, CRLF) | **copy** |
| `new_eda_5` | `ca-congress-members.json` | fa26-dev `lec/lec06/data/` (`e5057979…`) | **copy** |
| `new_eda_5` | `example_duck.db` | fa26-dev `lec/lec06/data/` (`a05d2d42…`), not `sql_I`'s copy (`45863bb3…`) | **copy** |

## Images the orchestrator copies

The full rows, with alt text and the list of regenerated figures, are in `/private/tmp/claude-1697942503/-Users-jedwin321-Documents-data100-course-notes/5aa6906d-785c-40f3-b441-73256c1554ea/scratchpad/lectures/images_manifest.yml`. The orchestrator copies only rows marked `copy: true`:

* `new_eda_1/images/`: `uc_admissions_source_school_website.png`, `cde_data_statistics_website.png`, `cde_annual_enrollment_snippet.png`, `cde_downloadable_files_by_topic.png`, `cde_frpm_snippet.png`, `cde_public_schools_districts_snippet.png`, `california_population_density_map.png`
* `new_eda_2/images/`: `split_apply_combine_count.png`, `split_apply_combine_mean.png`
* `new_eda_3`, `new_eda_4`: none. Every figure is regenerated from code.
* `new_eda_5/images/`: `us_zip_code_prefix_map.png`, `join_input_tables_s_t.png`, `inner_join_s_t.png`, `cross_join_s_t.png`, `star_schema_boba_fact_dimension.png`

`main`'s six existing images in `content/new_eda_1/images/` stop being referenced (EDA I OQ3).

## Open questions that span chapters

Each chapter's own questions follow its outline. The ones below need a single answer for the whole set.

1. **Code in folded cells** (item 13). The critic's default is one sentence before any dropdown whose code uses a verb that hasn't been taught yet. The alternative is to move plot B to EDA III, which leaves EDA II §7 without the plot L03 S42 compares against.
2. **Naming schools.** EDA I §13 names the school whose enrollment was mismatched and ties it to Homework 2. EDA II §4e and EDA IV §9 read school names off plots. Published notes need one policy (EDA I OQ5, EDA IV OQ7).
3. **One citation for the LLM claims.** EDA I's LLM note (S19) and EDA II's S28 quote both seem to rest on Kosmyna et al. (2025), *Your Brain on ChatGPT*. It needs confirming once (EDA I OQ8, EDA II OQ8).
4. **SQL engine.** Every SQL block was checked in DuckDB, where `/` between integers returns a float. SQLite, which `sql_I` also uses, truncates `applied / grade_12` to 0 for nearly every school. Should EDA I say so once, or should that wait for the SQL chapters (EDA I OQ9, EDA IV's SQL note)?
5. **Later chapters repeat this material.** In `myst.yml`, `polars_1`, `polars_2`, `eda` and `sql_I` come after `new_eda_5`. Between them they cover file formats, variable types, granularity, joins and the `Dragon` database again (EDA V OQ1). These outlines don't edit any of them.
6. **Reference sheet.** These chapters teach `pl.len()`, `group_by().len()`, `qcut`, `rank`, `.dt`, `pl.Config` and plotly, and none of them is in `reference/build_polars_section.py`. The sheet also still tells students that seaborn needs `.to_pandas()` (EDA III OQ11, conventions file).
7. **Gate false positives** (EDA I OQ4, for the gate's owner rather than staff). `authored_validate.py` A11 matches `mmin` inside "programming" and `a a ` inside "data a…". It should match those patterns as whole words, or every chapter's prose has to work around them.

---

## `new_eda_1` — EDA I

**Status: approved**

Scope: **L02 S5–S61**. There is no Fa26 lecture notebook. `fa26-dev/lec/lec02/lec02.ipynb` is the Sp26 Series/DataFrame tutorial on `elections`, and the Fa26 deck never uses it. This is a **fix pass on `main`'s draft** `content/new_eda_1/new_eda_1.ipynb` (98 cells). Keep the author's sections and sentences wherever they are correct. Repair the grammar, the transcript residue, and the defects listed below, and **extend the chapter from S46 to S60**, where the draft stops (its last content cell `f4a573c5` ends at S45, modality). EDA II's outline deletes L03 S12–S26 on the assumption that EDA I covers S45–S60, so the extension is required, not optional.

Every number below was executed under polars 1.43.1 (`d100`), seaborn 0.13.2 and duckdb 1.3.0 against the files in `content/new_eda_1/data/`. The numbers are for the author to check against the outputs, not prose to paste.

| Slides | What they carry | Disposition |
|---|---|---|
| S1–S4 | Slido, title, announcements, Askademia | **Deleted.** Outside scope, and course logistics. |
| S5 | "Review: … today's lecture starts from slide 15" | **Deleted.** Lecture logistics. S6–S13 are L01's review, and the chapter teaches them in full. |
| S6 | Tabular data: rows are observations, columns are features (`elections` table, `image34`) | **Kept** (draft `80e0a7f4`, `e5bc884c`, `6a8147ae`). The table is the live `elections` cell. Fix the typos. |
| S7 | Polars and SQL | **Kept** (`7808153f`). This is an ecosystem passage, so naming pandas is allowed. Tighten the muddled pandas/`datascience` comparison. |
| S8 | Not a coding class; a shared language for people and LLMs | **Kept** (`f7d9b41d`). **Delete `images/polars.png`**: it is decorative, and the manifest skips the slide's copy (`image10`). |
| S9 | EDA workflow: database, then snapshot, then SQL, then Polars, then seaborn | **Kept** as the draft's bullet list (`aabbc70d`). The slide's elections lineplot (`image12`) is **not regenerated**. It decorates the workflow, and drawing it would need `filter`/`is_in` before they are taught. |
| S10–S11 | One road to Berkeley (apply, admit, attend); the analyst task | **Kept** (`743b050a`, `93b4b7f6`). Add S10's "~1,700 public schools offer 12th grade" here, since §5 relies on it. |
| S12–S13 | Clarifying the task; possible clarifying questions | **Kept** (`4967134c`). Add S12's point, which the draft lacks: analysis is not a problem set, and the manager is not hiding a correct answer. |
| S14 | "Lecture 1 ended here" | **Deleted.** |
| S15 | UC admissions-by-source-school data; "be scrappy"; personal-project idea | **Kept** (`256941e4`, `6f10249d`). `uc_admissions_source_school_website.png` replaces `uc_site.png` (same page, higher resolution). Fold the project idea into the "Be Scrappy" note as one sentence. |
| S16–S18 | Preview the dataset; English → Polars → SQL for loading | **Kept, rebuilt** (`c0d1eec3`–`4dc34390`). The triple is restructured (see §6). **Slide bug:** `pivoted-ucb-admissions.csv` does not exist. The file is `data/pivoted-ucb-data.csv`. |
| S17, S34, S40, S47, S54 | Slido polls | **Rewritten** as questions in the prose, each answered by the next slide's content. |
| S19 | Code in Data 100: read and check code, basic LLM fluency | **Kept** (the draft's "A Note On Using LLMs", inside `4dc34390`), trimmed. See open question 8. |
| S20–S21, S27, S37 | The four question types (trust, extremes, distributions, correlation), repeated four times | **Kept once** (`edbf4b85`). §22 recalls it. The three repeats are deleted. |
| S22 | Provenance: we pivoted, missing values are `null`, rows with no visible data were dropped | **Kept** (`e560dbed`). |
| S23 | Why is data missing? Ascending sort on `applied`; counts below 3 are hidden; privacy (Sweeney 2000) | **Kept and moved.** The draft put this sort under "Extremes" (`cca7d21e`). In the lecture it answers "is the data complete?", so it moves into Context and Inspection (§8). The Sweeney footnote stays in `69300c80`, corrected. |
| S24 | Reminder of the dataset | **Deleted.** It repeats S16. |
| S25 | Row count (`len`, `.shape[0]`), `min` of `applied`; why ~1,700 schools become 1,268 rows | **Kept** (`5b0ef3f0`–`8b3a03eb`). |
| S26 | Data ≠ truth; don't give up | **Kept** (`b1e0bce8`). |
| S28 | Sort descending on `applied`; counts are not rates; the denominator assumption | **Kept** (`6067d515`, `4a3f152e`, `9666d888`). |
| S29–S30 | CDE Data & Statistics; Census Day enrollment 2024–25; joining is tricky | **Kept** (`9666d888`). `cde_data_statistics_website.png` replaces `ca_doe.png` (same page). `cde_annual_enrollment_snippet.png` moves here from S50, because this is where the 12th-grade count enters. Finish the truncated sentence "Thus, we will". |
| S31 | `with_columns(app_rate=…)` | **Kept** (`d7e71304`–`86c87945`). **Slide bug:** `pd.read_csv` in the Polars column. |
| S32 | Sort by `app_rate`; rates above 100% | **Kept.** `nulls_last=True` replaces the draft's hidden `is_not_null` filter (`9023a920`, tagged `hide-input`). |
| S33 | Filter `app_rate <= 1`, then sort | **Kept** (`ca548dbc`–`9cf4c747`). The SQL is fixed, and the prose now accounts for the 35 null rows the filter also drops. |
| S34–S35 | Are we done? Defining success | **Kept** (`9309d8fd`). |
| S36 | Fundamental operations so far | **Kept** as an English-only list at the end of §15. |
| S38 | `df.select('app_rate').describe()`; "no concise SQL equivalent" | **Kept, now live.** The draft quotes these statistics (`f031e186`) but never computes them, and the only `describe` it runs is on `applied` (`ea90e5db`). |
| S39–S41 | Boxplot anatomy; poll on the minimum whisker length; the no-whisker boxplot; Tukey's 1.5 | **Kept, regenerated** on `app_rate`, not the slide's world-bank GDP column. **The draft's whisker definition is wrong** (`ec12a741`). |
| S42–S43 | `sns.boxplot` / `sns.histplot` of `app_rate` | **Kept** (`4ccffc51`, `3a023427`), with `#| fig-alt` and a trailing `;`. |
| S44 | Skew; "P for positive" | **Kept, regenerated** from `world_bank.csv`. This replaces the pasted `right_skew.png`/`left_skew.png`. |
| S45 | Mode; unimodal and bimodal | **Kept, regenerated** from `world_bank.csv`. |
| S46–S48 | Why so much variation? Money, distance, resources, priorities; do we have that data? | **New in this pass** (§19). |
| S49–S51 | CDE downloadable files: enrollment, FRPM, public schools; joining in more data | **New** (§19), with four CDE screenshots. |
| S52–S56 | `dist_to_ucb` boxplot; boxplots vs histograms; `bins=50` | **New** (§20). **Slide bug:** the column is `dist_to_ucb_miles`. The slides alternate between `df` and `df_new`. |
| S57–S58 | Three peaks, the population map, rows per city | **New** (§21). **Slide bugs:** `value_counts()` without `sort=True` returns an unordered table, and the SQL `SELECT COUNT(*) … GROUP BY city` omits `city` and `ORDER BY`. |
| S59–S60 | Back to application rates: how do they relate to FRL share? Correlation "next time" | **New** (§22), as the closing question only. The analysis is EDA II's §1–§2. |
| S61 | Closing title | **Deleted.** |
| Draft "Some Code Specifics" (`93041313`–`4e08ecbe`) | Imports, `Series`, `.describe`, `.to_numpy`, `np.min`, `.select` | **Dissolved.** Each item moves to the point where the chapter first uses it (§1, §8, §16), or is deleted. It explained code after the reader had already run it, which reverses concept-before-syntax. |
| Draft `c705b740` | Empty markdown cell | **Deleted.** |

### Defects in `main`'s draft that this pass must fix

- **Gates that fail today:** `hide-input` tag (`9023a920`, A6). Unclosed ```` ```python ```` fence (`4ab96c3e`, A4). No `#| fig-alt`, and `<Axes: …>` reprs leak (`4ccffc51`, `3a023427`; A5, A8). `ORDER BY … DSC` (`958c0207`, `6c90a099`, `1060d089`) and a `SELECT` alias in `WHERE` (`1060d089`) (A10, A11). `-` bullets in Learning Outcomes (A1). Setup cell is `remove-input` and should be `remove-cell`.
- **The triple prints the Polars code a second time** in ten markdown cells (`c0f80bf4`, `48816499`, `a7b7a065`, `27957fe9`, `29640825`, `a2de4c4d`, `abe550dd`, `f82a6c03`, `4ab96c3e`, `af7e7d86`), plus "Here it is again for your convenience" in `4dc34390`. Delete all of them. The live cell is the Polars version.
- **False or unsupported claims:**
  - The boxplot whiskers "end at Q1 − 1.5·IQR / Q3 + 1.5·IQR" (`ec12a741`). They end at the most extreme data point inside those fences.
  - "Don't try to use numpy functions on this object, it will break!" (`1f891405`). Only NumPy's reductions raise: `np.min(s)` gives `TypeError: Series.min() got an unexpected keyword argument 'axis'`. Ufuncs such as `np.sqrt(s)` return a Series.
  - "It is generally more reliable to use `pl.col('column_name')`" in `.select` (`4e08ecbe`). The course writes `select("a", "b")`.
  - `pl.with_columns` (`30bca48c`). It is a DataFrame method.
  - A mask is "a list of rows that satisfy some condition" (`9cf4c747`). A mask is one true/false value per row.
  - "SQL would require us to create a new table in order to add a column" (`9cf4c747`). The real reason is that `WHERE` runs before `SELECT`, so it can't see the alias.
  - The app-rate histogram "peak around 0.05" (`f4a573c5`). The tallest bin is 0.060–0.085, with 223 schools.
  - "1,200 schools in my dataset" (`f031e186`). It is 1,229.
  - "200 students … applied" from Abraham Lincoln SF (`4dc34390`, `edbf4b85`). It is 201.
  - Sweeney's paper "highlighted this problem for the first time" (`69300c80`). That overclaims.
- **Residue and typos:**
  - First-person singular: "I would use 2026" (`c0d1eec3`), "my dataset" (`f031e186`).
  - Transcript filler: "uh" (`6a8147ae`, `6f10249d`).
  - Garbles: "data providence just means" (`e560dbed`); "And the code in DF applied.mmin SQL query looks like" (`8b3a03eb`).
  - Unclosed markup: `**tabular data.` (`80e0a7f4`); `'applied, descending=False)` (`92368879`).
  - Stray punctuation: `.hs.shape` (`2a79309a`).
  - Misspellings and doubled words: "The the", "featue", "freshmmen", "ethncity", "Latana", "usign", "Provenence", "nubmer", "resepctively", "donwloadable", "applcation", "a a special specialized", "who who", "columnn", "additonal", "Acess", "polar code".
- **A gate false positive the author must steer around:** `authored_validate.py`'s literal `KNOWN_TYPOS` flags the substring `mmin`, which matches **"programming"**. S7's "declarative programming language" (kept in `7808153f`) would fail A11. It also flags `a a `, which matches "data a…" and "via a …". Reword those phrases (e.g. "SQL is a declarative language"), or have the gate owner add word boundaries (open question 4).

**Proposed shape**

0. **Frontmatter, Learning Outcomes, opener.** Use `title: EDA I` and the `*` bullets below. The opener starts "In this chapter, we will…". It says we take a vague request from a manager, find data that could answer it, ask whether the data can be trusted, and use our first table operations and plots to look for unusual schools. The setup cell is `remove-cell` and holds:
   - `import polars as pl`, `import seaborn as sns`, `import matplotlib.pyplot as plt`;
   - `sns.set_palette("colorblind")`;
   - `pl.Config.set_fmt_str_lengths(40)`, because the longest school name is 35 characters and the HTML repr otherwise cuts strings at 30 characters with `…` (checked: `ALTUS CHARTER SCHOOL OF SAN DI…`). EDA II–IV copy this line into their own setup cells (*critic*).

   Drop `numpy`, since nothing here needs it.

1. **Exploratory Data Analysis and tabular data** (S6). *Concept: a row is one observation and a column is one feature of it.* Keep the live `elections` cell (187 rows, 1824–2024). It is the first Polars call, so it gets one sentence each on `pl` (the conventional name for Polars) and `pl.read_csv` (it reads a CSV file into a `DataFrame`, the Polars object for a table). The second row is John Quincy Adams, 1824 (checked). §6 has more on CSV.
   **1a. Languages and libraries** (S7). Polars is the table library and SQL the database language. Cut the double comparison. The slide says Polars is the successor to pandas with similar syntax, and similar in spirit to Data 8's `datascience`.
2. **Developing data science skills** (S8). *Concept: the goal is a shared language for describing table manipulations, not memorized syntax.* Keep, and remove the logo.
3. **A typical EDA workflow** (S9). *Concept: a snapshot of a dynamic database, then manipulate, then visualize, then repeat.* Keep the list.
4. **Our data and task** (S10–S13). *Concept: a vague request becomes clarifying questions before any code runs.* Keep the three-stage path, the task, and the question list. Add S12's mindset shift.
5. **Finding our data** (S15, website half of S22, S23's privacy note). *Concept: know where your data comes from, and why values are blank.*
   - Show `uc_admissions_source_school_website.png`. The page has three rows per school (App, Adm, Enr).
   - Keep the three explanations for blanks and the UC rule: counts below 3 are blank, and schools with fewer than 5 applicants show nothing.
   - Correct the footnote: **Latanya** Sweeney's 2000 study showed that ZIP code, birth date and sex identify most Americans uniquely. It is "seminal research", as the slide says, not the "first time" (open question 6).
   - Keep the "Be Scrappy" note.
6. **Opening our data** (S16–S19). *Concept: load, preview, and ask what the preview tells you.* **The triple, as used everywhere in this chapter:**
   - a markdown line **English:** "Load the dataset and show a preview."
   - the live cell `admissions = pl.read_csv("data/pivoted-ucb-data.csv")` then `admissions`
   - a markdown cell **SQL:** ```` ```sql ```` `SELECT * FROM admissions`, plus one sentence that in SQL the table already lives in a database under the name `admissions`.

   The English comes *before* the cell, and the Polars code is never repeated in markdown. Read the header the preview prints: shape `(1_268, 6)` and a dtype under every column name (`str`, `i64`). The CSV-structure note (`bf5ac7f5`, `:open: false`, which mystmd 1.6.6 supports) swaps `csv_view.png` for a ```` ```text ```` block of the file's **first six lines, verbatim**. The screenshot showed the *enrollment* file's eight columns under a paragraph about the six-column file. The block shows the trailing `,` of A B MILLER and the `,,` of ABLE CHARTER, the empty fields that load as `null`. Keep the observations: 1,268 schools; three ABRAHAM LINCOLN HIGH SCHOOLs (LA, SF, San Jose); **201** applicants from SF. Keep the LLM note (S19), trimmed (open question 8).
7. **Four kinds of questions** (S20–S21). *Concept: trust, extremes, distributions, correlation.* Keep `edbf4b85`, correcting 200 to 201.
8. **Context and inspection** (S22–S26). *Concept: data ≠ truth, so check what is missing and why.*
   - **Provenance** (S22). The table was pivoted from three rows per school to one, with no values changed. Missing is shown as `null`, and `null` is not zero. Rows with nothing visible were dropped: ABRAHAM LINCOLN in Riverside is on the website but not in the file (checked).
   - **Is it complete? Sort ascending** (S23, moved here). English: "Sort the dataset in ascending order by the `applied` column." Polars: `admissions.sort("applied", descending=False)`. SQL: `SELECT * FROM admissions ORDER BY applied ASC`.
     - **First `.sort`**, which returns a new, reordered `DataFrame` and leaves `admissions` unchanged. Keep the draft's reassignment remark with its quote fixed.
     - The display shows the first and last five rows. The top rows have `applied = 5` with `null` admitted/attended (38 of the 39 five-applicant schools have null `admitted`). **Don't name the top schools:** 39 tie at 5 and their order is not fixed. The bottom row is DOUGHERTY VALLEY, 542. Keep the draft's sentence, saying "at the bottom of the table".
   - **Count the rows** (S25). English: "Count the number of rows in the dataset." Polars: `len(admissions)` (1268), then `admissions.shape` → `(1268, 6)`, `.shape[0]` / `.shape[1]`, and `admissions.height`, the row count by name. (*Critic:* `.height` is added because EDA III–V use it and the conventions file lists it beside `.shape` for L02 S25.) SQL: `SELECT COUNT(*) FROM admissions`. Give the S25 answer to "~1,700 schools, 1,268 rows": schools with no applicants are not in the UC data, and rows with 1–4 applicants were dropped.
   - **Smallest count** (S25). First `admissions["applied"]`, as a live cell showing the Series (moved from `d3270d0d`). **Brackets pull one column out as a `Series`**, a single named, typed column. Then English "Find the minimum of the `applied` column." Polars: `admissions["applied"].min()` → 5. SQL: `SELECT MIN(applied) FROM admissions`. One sentence names `.max()`, `.mean()`, `.std()` and SQL's `MAX`, `AVG`, `STDDEV`. One corrected sentence on NumPy: its reductions such as `np.min` raise on a `Series`, so use the method, or `.to_numpy()` if an array is really needed. Delete the `.to_numpy()`/`np.min` cells (`06baea1a`, `1a8bd226`). They are not in the lecture, and nothing in EDA I–V needs them (open question 11).
   - Data Science Wisdom (S26).
9. **Extremes: counts are not rates** (S28). *Concept: a rate needs a denominator, and choosing one is an assumption.* English → `admissions.sort("applied", descending=True)` → `SELECT * FROM admissions ORDER BY applied DESC`. The top five are DOUGHERTY VALLEY 542, DUBLIN 435, ARCADIA 371, LOWELL 363, AMERICAN 348. `applied` has no nulls, so no `nulls_last` is needed. Application rate ≈ applied ÷ 12th graders, and treating 12th graders as the possible applicants is the ⚠️ assumption.
10. **Joining in new data** (S29–S30). *Concept: be scrappy, find the denominator elsewhere, and join it on.* Show `cde_data_statistics_website.png`, then `cde_annual_enrollment_snippet.png` (the source of the 12th-grade count). The source is the 2024–25 Census Day enrollment. A join matches rows from two tables on shared information. Here that is the school, and it is tricky because names are written differently (hw02 Q4 has students redo this join). Then `admissions = pl.read_csv("data/pivoted-ucb-data-w-enrollment.csv")`, which has the same 1,268 schools plus `tot_enrolled` and `grade_12`. **35 schools have no enrollment data** (`null` in both). The same 35 rows are null in every CDE column of the `-w-everything` file, but don't assert *why* (open question 10).
11. **Creating new columns** (S31). *Concept: a new column computed row by row from existing columns.* English: "Create a new column with the application rate for each school." Polars: `admissions = admissions.with_columns(app_rate=pl.col("applied") / pl.col("grade_12"))`. SQL: `SELECT *, applied / grade_12 AS app_rate FROM admissions`. This is the **first `.with_columns`** (keyword form: the argument's name becomes the column's name) and the **first `pl.col`**, which names a column inside a method so Polars can compute with it. A null `grade_12` gives a null `app_rate`, for 35 rows.
12. **Highest application rates** (S32). *Concept: missing values have to go somewhere when you sort.* English: "Sort by `app_rate` in descending order." Polars: `admissions.sort("app_rate", descending=True, nulls_last=True)`. SQL: `SELECT *, applied / grade_12 AS app_rate FROM admissions ORDER BY app_rate DESC NULLS LAST`.
    - **First `nulls_last=True`.** Polars puts nulls first, so without it the top 35 rows would be schools with no rate (checked: ALLIANCE MIT 6-12 COMPLEX leads). With it, those schools sit at the bottom of the display, and the prose can point there.
    - `NULLS LAST` is written out for portability. It is DuckDB's default, but PostgreSQL puts nulls first under `DESC`. The DuckDB top five match Polars (checked).
    - Delete `9023a920` and the mask-note sentence about it.
    - Output: GIRLS ACADEMIC LEADERSHIP ACAD 2.5 (40 applied, 16 12th graders), MCFARLAND 1.6, ALAMEDA SCIENCE & TECHNICAL INST 1.448, SCIENCE ACADEMY STEM MAGNET 1.152.
13. **Inspecting anomalies** (S32's annotation). *Concept: when a value is impossible, suspect your own pipeline first.* Keep `f031d12e`'s explanations (data entry, 11th graders or gap-year applicants, a wrong join). Replace "It turns out … this was the result of a mistake!" with the one verified case: GIRLS ACADEMIC LEADERSHIP ACAD was matched to a different school's enrollment, which Homework 2 asks students to diagnose (fa26-dev hw02 Q4e; open question 5).
14. **Filtering rows** (S33). *Concept: keep the rows where a condition is true.* English: "Keep the rows where `app_rate` is at most 1, then sort by `app_rate`." Polars: `admissions = admissions.filter(pl.col("app_rate") <= 1)` then `admissions.sort("app_rate", descending=True)`. SQL: `SELECT *, applied / grade_12 AS app_rate FROM admissions WHERE applied / grade_12 <= 1 ORDER BY app_rate DESC`.
    - **First `.filter`.** Rewrite `9cf4c747`'s note. `pl.col("app_rate") <= 1` is a **Boolean mask**, one true/false per row, and `.filter` keeps the true rows. A null compared with 1 is null, not true, so the filter also drops the 35 null rows. **The result is 1,229 rows, which is 1,268 − 4 − 35**; the draft says "remove those four". One sentence on `pl.col("app_rate").is_not_null()` as the explicit way to drop nulls (EDA II lists it as assumed).
    - SQL: `WHERE` is evaluated before `SELECT`, so it can't use the name `app_rate`, while `ORDER BY` can.
    - Top five: MIDDLE COLLEGE 0.833 (60 12th graders), MONTA VISTA 0.762, GRETCHEN WHITNEY 0.730, CALIFORNIA ACAD MATH & SCIENCE 0.706, LYNBROOK 0.701.
15. **Defining success** (S34–S36). *Concept: turning "defy typical patterns" into a metric is the analyst's job.* Keep `9309d8fd`: one small school (MIDDLE COLLEGE, 60) and one specialized academy (CALIFORNIA ACAD MATH & SCIENCE). Close with S36's English-only list: preview; select rows or columns; create columns; filter; sort; join.
16. **Distributions: summary statistics** (S37–S38). *Concept: numbers summarize a distribution, but pictures are faster to read.* English: "Compute summary statistics about `app_rate`." Polars: `admissions.select("app_rate").describe()`. SQL: none, and say so ("no concise equivalent", as S38 does).
    - **First `.select`**. It keeps the named columns and returns a `DataFrame`, while `admissions["app_rate"]` returns a `Series`. Several names can be passed: `select("school", "attended")`. **First `.describe`**.
    - From the output: count 1229, mean 0.160831, std 0.133873, min 0.009901, 25% 0.068921, median 0.112676, 75% 0.204082, max 0.833333. These match S38's table.
    - Rewrite `f031e186` from these values.
17. **Boxplots** (S39–S42). *Concept: a boxplot draws the quartiles, the IQR, and the points outside 1.5·IQR.*
    - Live: English "Make a boxplot of the values in `app_rate`." Seaborn: `sns.boxplot(admissions, x="app_rate");`, the **first seaborn call**, which takes the Polars frame and a column name. There is no SQL, and one sentence says SQL doesn't draw plots.
    - Then an anatomy figure: a `Click to see the code` dropdown plus a `remove-input` cell that redraws the same boxplot with labels on Q1, the median, Q3, both whisker ends, and the outliers. Compute the labels with `quantile(q, interpolation="linear")`, which is what matplotlib's whiskers use.
    - Checked: box 0.069–0.204, median 0.113, upper whisker 0.407, lower whisker 0.0099 (the minimum, with no low outliers), and **90 outliers** above.
    - Corrected whisker rule: each whisker ends at the most extreme data point within 1.5·IQR of the box.
    - Answer the S40 poll (S41): a whisker can have zero length when every point beyond a quartile is an outlier.
    - Keep "Arbitrary Heuristics" and add the Tukey anecdote (open question 7).
18. **Histograms, skew and modality** (S43–S45). *Concept: the direction of the tail is the skew, and the number of peaks is the modality.*
    - Live: `sns.histplot(admissions, x="app_rate");`. The tallest bin is 0.060–0.085 (223 schools), with a long right tail to 0.833. The mean (0.161) is above the median (0.113).
    - Skew: one dropdown plus `remove-input` figure with two panels, `plt.subplots(1, 2)` and `stat="density"`, from `data/world_bank.csv`. The left panel is `Gross national income per capita, Atlas method: $: 2016`, which is right-skewed (mean 12,963 > median 5,280). The right panel is `Access to an improved water source: % of population: 2015`, which is left-skewed (mean 88.8 < median 96.0). Quote those numbers rather than stating the mean/median rule bare. Keep S44's "P on its side" mnemonic: the bowl is the peak and the stem is the right tail, which holds for any right-skewed histogram. The draft's "right skew is more common" is fine as given, because the reason it gives is quantities bounded below by zero.
    - Modality: the mode, unimodal, bimodal, multimodal. `app_rate` is unimodal. A second two-panel dropdown figure shows `Prevalence of diabetes: % of population ages 20 to 79: 2015` (unimodal) and `Antiretroviral therapy coverage: % of people living with HIV: 2015` (keep the slide's "bimodal?"; the author reads the figure). Keep the draft's point that boxplots can't show modality and that bin choices can create or hide peaks, which §20 demonstrates.
19. **Why so much variation? Bringing in more data** (S46–S51). *Concept: a question about causes becomes a search for new columns.*
    - S47 poll as a question, then S48's answer: money, distance, academic resources, family priorities. Do we have that data?
    - Refer back to the CDE page from §10, then show `cde_downloadable_files_by_topic.png`.
    - The three sources, each with its screenshot: Annual Enrollment (already used; S50: "this is where we got the 12th-grade count"); `cde_frpm_snippet.png`, the free/reduced-price meal share, a proxy for socioeconomic status; `cde_public_schools_districts_snippet.png`, which gives latitude/longitude (hence distance to Berkeley) and charter status.
    - Live triple: English "Load the admissions data joined with the California public schools data." Polars: `admissions = pl.read_csv("data/pivoted-ucb-data-w-everything.csv")`, which has 1,268 rows and 11 columns. It holds all schools again, since this file is unfiltered, and the prose says so. SQL: `SELECT * FROM admissions`.
    - The three new columns: `is_charter` (`Y` 231, `N` 1002, null 35); `pct_free_reduced`, a fraction from 0.034 to 0.985 with 94 nulls; `dist_to_ucb_miles` (35 nulls, computed from latitude/longitude; open question 10).
    - A `{tip}` for S51's personal project, reproducing the joins from the raw files.
20. **Distance to UC Berkeley** (S52–S56). *Concept: boxplots and histograms are not interchangeable.*
    - Live: `sns.boxplot(admissions, x="dist_to_ucb_miles");`. Seaborn silently drops the 35 nulls, so it plots 1,233 schools, and the prose says so. There are no outliers: the range is 0.7–524 miles, the box 67–362, and the median 317.
    - S54 poll: "from this boxplot, what does the histogram look like?"
    - `sns.histplot(admissions, x="dist_to_ucb_miles");`, with seaborn's default of 12 bins here. It shows a heap near Berkeley, a larger heap around 300–390 miles, and a small bump near 440–480.
    - Then with `bins=50`. There are three peaks: within about 20 miles of Berkeley (the 11–22-mile bin holds 61 schools, and every bin out to about 95 miles holds at least 30), 346–356 miles (136 schools, the tallest bin), and 451–461 miles (35).
    - Every plot cell gets `#| fig-alt` with these shapes and ends with `;`.
21. **Connecting plots to the real world** (S57–S58). *Concept: a plot's shape has a cause, so go and find it.*
    - "Three peaks: trimodal." Show `california_population_density_map.png`. There are three hubs: the Bay Area, LA/Orange County, and San Diego.
    - English: "For each city, count the number of rows." Polars: `admissions["city"].value_counts(sort=True).head(5)`. SQL: `SELECT city, COUNT(*) AS count FROM admissions GROUP BY city ORDER BY count DESC LIMIT 5`.
    - **First `.value_counts`** (a two-column table, `city` and `count`, and `sort=True` puts the largest first) and **first `.head(n)`**. The SQL is also the book's first `GROUP BY` and `LIMIT`, so each gets a clause.
    - Output: Los Angeles 112 (as on S58), San Diego 41, San Jose 31, Oakland 28, Sacramento 28. Oakland and Sacramento tie, and DuckDB lists them in the opposite order from Polars, so the prose must not rank them. `head(5)` is safe because the next city has 19.
    - Tie the output to the peaks with checked distances: Oakland schools are 3–11 miles away, San Jose 39–50, Sacramento 58–75, all in the first peak. Los Angeles is 326–358 miles and San Diego 442–471.
    - Don't name split-apply-combine. EDA II §9 introduces it and uses this cell as its callback.
22. **Back to application rates, and what comes next** (S59–S60). *Concept: the fourth question type, correlation.* Rewrite `b6e28431`, which currently promises "next section… bring in … data" that this chapter has now done. Recall the four question types. Pose S59's starting point, how application rate relates to `pct_free_reduced`, and leave it for the next chapter. There is no code and no plot. EDA II §1 rebuilds `app_rate` on the `-w-everything` file.

**Polars verbs this chapter introduces for the first time.** Each gets one or two sentences before its first call, and the chapter never refers the reader to `polars_1`/`polars_2`.

| Verb | Section | Note |
|---|---|---|
| `pl` alias, `pl.read_csv` | §1 | `DataFrame` defined here. |
| DataFrame preview (shape, dtypes, head/tail rows) | §6 | Read the header aloud once. |
| `.sort(col, descending=…)` | §8 | Returns a new frame. Ties have no fixed order. |
| `len(df)`, `df.shape`, `.shape[0]`/`[1]`, `df.height` | §8 | `.height` added by the critic; EDA III–V assume it. |
| `df["col"]` → `Series`; `.min()` (and `.max`/`.mean`/`.std` by name) | §8 | Brackets only for pulling out one column. |
| `.with_columns(name=expr)`, `pl.col`, `/` between columns | §11 | Keyword form, per the conventions file. |
| `.sort(…, nulls_last=True)` | §12 | AGENTS rule 8. **EDA II can now list it as assumed** (its verb table says "moves to EDA I if its fix pass introduces it"). |
| `.filter(expr)`, comparison masks, `.is_not_null()` (prose) | §14 | |
| `.select("col", …)`, `.describe()` | §16 | |
| `sns.boxplot(df, x=…)`, `sns.histplot(df, x=…, bins=…)` | §17, §18, §20 | Polars frame passed directly. |
| `Series.value_counts(sort=True)`, `.head(n)` | §21 | Settles EDA II's open question 10. `DataFrame.head(n)` is introduced here, so EDA III does not re-introduce it. |
| SQL `GROUP BY`, `LIMIT` | §21 | The first SQL grouping and row limit, one clause each. EDA II §9 and EDA III assume both. |
| `.quantile(q)` | §17, folded cell | See the dropdown note below. |
| `plt.subplots(1, 2)`, `ax=` | §18, folded cell | See the dropdown note below. EDA II–IV assume both. |

**Only inside `Click to see the code` dropdowns (layout, not lesson):** `plt.subplots`/`ax=`, `stat="density"`, `ax.annotate`, `quantile(…, interpolation="linear")`. This is the same pattern EDA II uses for its 2×2 figure. *Critic:* a reader who opens a dropdown reads this code, and `notes-lecture-fidelity-reviewer` check 5 treats every live cell, folded or not, as a use. So the prose before the §17 anatomy dropdown gives `.quantile(q)` one sentence (the value below which a fraction `q` of the column falls), and the prose before the first §18 two-panel dropdown gives `plt.subplots(1, 2)` and `ax=` one sentence (one figure with two panels; `ax=` tells seaborn which panel to draw on). `ax.annotate` and `stat="density"` get a clause each in those sentences. EDA II §4c, EDA III §14 and EDA IV §1 then reuse `plt.subplots`/`ax=` without re-introducing them.
**Not used:** `numpy`, `.to_numpy()` (open question 11), `group_by`, `pl.len()`.

**SQL for the claim verifier.** Every block is self-contained against the CSV most recently loaded as `admissions`: `pivoted-ucb-data.csv` for §6–§9, `pivoted-ucb-data-w-enrollment.csv` for §10–§18, and `pivoted-ucb-data-w-everything.csv` for §19–§21. The `app_rate` queries recompute the expression, so no derived column needs registering. No `SELECT` alias appears in a `WHERE`, `ORDER BY` uses `DESC`, and the §12 sort spells out `NULLS LAST`. Checked in DuckDB: `COUNT(*)` 1268, `MIN(applied)` 5, the §12 top five identical to Polars, the §14 result 1229 rows with the same top three, and the §21 top five identical except the Oakland/Sacramento tie order (advisory only).

**Data.** Four files are already in `content/new_eda_1/data/` on `main`, and one is new:
- `elections.csv`: main (md5 `47b93a15…`, identical to `fa26-dev/lec/lec02/data/elections.csv`).
- `pivoted-ucb-data.csv`: main (md5 `0d77eecc…`). It equals the first 6 columns of `-w-everything` (checked with `DataFrame.equals`).
- `pivoted-ucb-data-w-enrollment.csv`: main (md5 `2ebf84d5…`). It equals the first 8 columns of `-w-everything` (checked).
- `pivoted-ucb-data-w-everything.csv`: main (md5 `4c9d424f…`, identical to `fa26-dev/lec/lec04/data/`). Not lec06's `"NA"` copy.
- **NEW:** `world_bank.csv`, copied from `main:content/visualization_1/data/world_bank.csv` (md5 `05c7ef74…`, identical to `fa26-dev/lec/lec08/data/world_bank.csv`). Only the §18 skew/modality dropdowns read it. Its first column is named `""`, which is harmless because the frame is never displayed (open question 2).

The three staged UCB files keep the lecture's order: the admissions data, then plus enrollment (S31), then plus the rest of the CDE data (S51). Each "join" is a file load, because the joins themselves are homework.

**Images.** All from the manifest's keep rows, with the manifest's alt text:
- `uc_admissions_source_school_website.png` (L02 `image49`, S15/S22) in §5;
- `cde_data_statistics_website.png` (`image56`, S29/S49) in §10;
- `cde_annual_enrollment_snippet.png` (`image40`, S50) in §10;
- `cde_downloadable_files_by_topic.png` (`image47`, S50) in §19;
- `cde_frpm_snippet.png` (`image42`, S50) in §19;
- `cde_public_schools_districts_snippet.png` (`image37`, S50) in §19;
- `california_population_density_map.png` (`image52`, S57–S58) in §21.

Regenerated from code, never pasted: `image18`/`23`/`25`/`26`/`29`/`33`/`36`/`44`/`55` (tables, now live outputs), `image20` (the `describe` table), `image27`/`30` (boxplots), `image45` (the `app_rate` histogram), `image32`/`39`/`41`/`43` (the world-bank histograms), and `image48`/`50`/`53`/`54` (the distance plots). **`main`'s six existing images all go unreferenced:** `uc_site.png`, `ca_doe.png` (both superseded by manifest copies of the same pages), `csv_view.png` (replaced by a text block), `polars.png` (decorative), and `right_skew.png`/`left_skew.png` (plots, now regenerated). See open question 3.

---

### Learning Outcomes (proposed)

```
::: {note} Learning Outcomes
* Turn a vague request into clarifying questions and a concrete analysis plan
* Judge how far to trust a dataset by asking where it came from and what it leaves out
* Load and inspect a table with `pl.read_csv`, `len()`, `.shape`, and `df["col"]`
* Sort, filter, and add columns with `.sort()`, `.filter()`, and `.with_columns()`
* Summarize one variable with `.describe()`, `.value_counts()`, `sns.boxplot`, and `sns.histplot`
* Describe a distribution's skew and modality, and explain why a boxplot can hide modality
* Write each table operation three ways: in plain English, in Polars, and in SQL
:::
```

### Open questions for course staff

1. **Frame name.** The slides use `df`/`df_new`, and the draft uses `hs`/`hs_enroll`. This outline renames to **`admissions`**, so the Polars name and the SQL table name match. That agrees with EDA II's open question 6. The name is reassigned at each file load and at the filter, and the prose says so each time. Approve, or keep the draft's names. *Critic:* applied in all five outlines; EDA IV's draft used the lecture's `uce` and now uses `admissions`.
2. **`world_bank.csv` for the skew and modality examples.** The alternatives are to keep `main`'s pasted `right_skew.png`/`left_skew.png`, which breaks "plots are regenerated", or to cut to the chapter's own data. That would mean `app_rate` as the right-skew example and `dist_to_ucb_miles` as the multimodal one, with left skew and bimodality in words only. The recommendation is the copy: it matches the slides exactly and costs one 166-row file.
3. **Six `main` images become unreferenced** (listed above). The author may not touch `images/**`. Should the orchestrator delete them, or leave them in place?
4. **`authored_validate.py` A11 false positives.** `KNOWN_TYPOS` is matched as a raw substring, so `mmin` fires on "programming" and `a a ` fires on "data a…"/"via a …". Recommend word-bounding those two patterns (`\bmmin\b`, `\ba a\b`). Otherwise the author has to reword S7's "declarative programming language".
5. **The Homework 2 callback** (§13). Fa26 hw02 Q4e asks students to diagnose GIRLS ACADEMIC LEADERSHIP ACAD's mismatched join, and its solution says it matched a different "Leadership Academy". Should a textbook name a homework number that changes each term? The alternative is "a later homework asks you to diagnose it".
6. **The Sweeney footnote.** The slide cites "Sweeney (2000)" and "in the news recently, too!" with no links. Staff should supply the paper link (*Simple Demographics Often Identify People Uniquely*, Carnegie Mellon, 2000) and the news item, or drop "in the news". The draft's governor-of-Massachusetts anecdote is Sweeney's 1997 re-identification of Governor Weld. It predates the 2000 paper, so the footnote must not present it as that paper's finding.
7. **Tukey's 1.5.** S39 quotes an unnamed person recounting Tukey's "1 was too small, 2 too big" answer, with no source. The textbook should either cite it or paraphrase it as anecdote ("Tukey reportedly said…").
8. **The LLM note** (S19). The draft adds energy, water and politics caveats and "studies show that people who rely too much on LLMs lose their competency", none of which is on the slide. These presumably come from the lecture audio. Confirm staff want them, and give a citation for the studies. EDA II's open question 8 proposes Kosmyna et al. (2025) for L03 S28's similar claim, and one citation should serve both chapters.
9. **SQL integer division.** `applied / grade_12` is floating-point in DuckDB (checked), but SQLite truncates it to 0 for nearly every school, and the book's `sql_I` uses both engines. Add a one-line `{tip}` in §11, or leave it for the SQL chapter?
10. **Provenance of the derived columns.** The files don't say how `dist_to_ucb_miles` was computed (straight-line from latitude/longitude, presumably), or why 35 schools are null in every CDE column (most likely no match in the enrollment join). The chapter will state neither cause unless staff confirm it.
11. **`.to_numpy()`.** The draft demonstrated it with `np.min`. This outline cuts both to one sentence, because the lecture never uses them. Keep a live `.to_numpy()` cell if a later chapter will assume it. *Critic:* none of EDA II–V runs it. EDA V §2 points back to the §8 sentence once, which is enough.
12. **The population map's source.** `california_population_density_map.png` (2020 Census, by tract) carries no credit on the slide. A published page needs a source line.

---

## `new_eda_2` — EDA II

**Status: approved**

Scope: **L03 S9–S49**. There is no lecture notebook (`fa26-dev/lec/lec03` is a stale babynames notebook), so every cell is rebuilt from the deck's code. L03 S12–S26 re-teach L02 S45–S60, which is EDA I's material, and this outline deletes them. After those deletions, the chapter carries the fourth question type from EDA I, **correlation**. It starts from how application rate relates to the free/reduced-price meal share, and runs through weighting points, a derived count, tidy data, and split-apply-combine. It stops before any `group_by` code, which L04 S11 onward gives to EDA III.

Every number below was executed under polars 1.43.1 (`d100`), seaborn 0.13.2, statsmodels 0.14.4 and duckdb 1.3.0 against `content/new_eda_2/data/pivoted-ucb-data-w-everything.csv`. They are for the author to check against the outputs. They are not prose to paste.

| Slides | What they carry | Disposition |
|---|---|---|
| S1–S8 | Slido, title, announcements, Askademia screenshots | **Deleted.** Course logistics. |
| S9–S10 | Recap: the four question types, the task, the first answer (sort by `app_rate`), "define success" | **Rewritten** into a two-paragraph opener for §1. EDA I teaches all of it, so this is a pointer back, not a re-teach. |
| S11 | Recap table: seven English / Polars / SQL rows | **Deleted as a table.** Every row is an EDA I operation. §1's rebuild cell uses three of them (`read_csv`, `with_columns`, `filter`). Two slide bugs are not copied: the file name `pivoted-ucb-admissions.csv` does not exist, and the SQL puts a `SELECT` alias inside `WHERE`. |
| S12 | Modality (unimodal/bimodal) | **Deleted.** EDA I, L02 S45. |
| S13–S15 | "Why is there so much variation in application rates?" | **Deleted.** EDA I, L02 S46–S48. §1 restates the question in one sentence. |
| S16–S18 | CDE data sources, joining in the expanded school data | **Deleted.** EDA I, L02 S49–S51. `image28` (the FRPM blurb) is a re-crop of L02 `image42`, which EDA I keeps as `cde_frpm_snippet.png`. See open question 7. |
| S19–S23 | `dist_to_ucb` boxplot, histogram, 50 bins, three peaks | **Deleted.** EDA I, L02 S52–S57. |
| S24 | `value_counts` on `city`, now with `.sort(...).head(10)` | **Deleted here.** Its one addition over L02 S58, sorting and taking the top rows, comes back in §9 as the split-apply-combine callback. EDA I §21 now uses the sorted form, `value_counts(sort=True).head(5)` (*critic*). |
| S25–S26 | "Starting point: how do application rates correlate with FRL percentage?"; correlation "next time" | **Kept.** This is the chapter's motivating question (§1). |
| S27 | Reminder: the augmented dataset (`image18`, a pandas render with `NaN`) | **Kept, regenerated.** The §1 rebuild cell displays the Polars frame. Don't paste the image. |
| S28 | `sns.regplot(..., lowess=True)`; "You are the driver, not the LLM" | **Kept.** §2. |
| S29–S30 | LOWESS intuition; should every point count equally? | **Kept.** §3, plus a note on what LOWESS actually computes. |
| S31, S33, S38, S41 | Slido polls | **Rewritten** as questions in the prose (S31 at the end of §3, S33 in §4, S38 in §5, S41 in §7). |
| S32 | Four scatter plots A–D (unsized, `grade_12`, `tot_enrolled`, `applied`) | **Kept, regenerated** as one 2×2 figure in §4. **Moved after S35–S36**, so the reader has seen `size=` before seeing four variations of it (open question 5). |
| S34 | "Take a stand": B vs D | **Kept.** §4. |
| S35–S36 | `sns.scatterplot(..., size='grade_12')`, then `sizes=(1, 100)` | **Kept.** §4, placed first in the section. S36's "I had to ask an LLM" becomes impersonal (the residue gate rejects first-person singular). |
| S37 | "Are you picking the same five schools?" | **Kept.** End of §4. |
| S39 | `(pl.col('pct_frl') * pl.col('grade_12')).cast(int).alias('num_frl_12th')` | **Rewritten** in §5: the column is `pct_free_reduced` (`pct_frl` does not exist), it uses the keyword form rather than `.alias`, and the SQL truncates (see §5). |
| S40 | "Are we done?" | **Kept.** §6. |
| S42 | Summarizing patterns: A (every school) vs B (four binned points); the bin-definition note; "nearly transparent points + bold curve" | **Kept.** §7. |
| S43–S44 | Tidy data; the four-row table; "How do we generate this data?" | **Kept.** §7. The question stays open. L04 S24–S31 answer it in EDA III. |
| S45 | Anatomy of a seaborn call | **Kept.** §8. The slide's `pct_frl` becomes `pct_free_reduced`. |
| S46 | Fundamental operations so far; "For each unique value of COLUMN(S), do SOMETHING." | **Kept.** §9. |
| S47–S48 | Split-apply-combine: count per city, mean `tot_enrolled` per city | **Kept.** §9, with both diagrams. The S48 aside "Josh grew up here!" is **deleted** (personal reference). |
| S49 | Closing title | **Deleted.** |

**Proposed shape**

0. **Frontmatter, Learning Outcomes, opener.** `title: EDA II`. The opener starts "In this chapter, we will…" and names the question: are other characteristics of a school related to its application rate? The setup cell is `remove-cell` and holds `polars`, `seaborn`, `matplotlib.pyplot as plt`, `sns.set_palette("colorblind")` and EDA I's `pl.Config.set_fmt_str_lengths(40)`, so school names are not cut off. There is no `numpy`, because nothing here needs it.

1. **Where we left off** (S9–S10, S25–S27). *Concept: we move from one variable's extremes and spread to the relationship between two variables.* A short recap covers the task, the first answer, why it isn't finished, the augmented data EDA I joined in, and the question "why do application rates vary so much?" Then comes one live cell with the English → Polars → SQL triple: read `pivoted-ucb-data-w-everything.csv`, add `app_rate` with the keyword form, and keep `app_rate <= 1`. The frame is called `admissions` (open question 6). Checked: 1268 rows raw, 35 null `app_rate`, 4 above 1, none exactly 1, so the result has **1229 rows**. Give one sentence to `pct_free_reduced`: the share of a school's students eligible for free or reduced-price meals, used as a proxy for socioeconomic status. EDA I covers where it comes from. **56** of the 1229 schools have no value.
   SQL (reads the raw CSV as `admissions`; after this, "`admissions`" in SQL means this query's result):
   `SELECT *, applied / grade_12 AS app_rate FROM admissions WHERE applied / grade_12 <= 1`

2. **Application rate against free/reduced-price meals** (S28). *Concept: a smoothing curve shows the trend inside a noisy scatter.* The framing is English → Seaborn code, with no SQL, because the deck gives none and SQL doesn't plot. The call is `sns.regplot(admissions, x='pct_free_reduced', y='app_rate', lowess=True, line_kws={"color": "red"})`. **Checked: given a Polars frame, `regplot` leaves both axis labels empty** (seaborn 0.13.2 turns the columns into arrays before labelling). Follow it with `plt.xlabel(...)` and `plt.ylabel(...)`, plus a one-clause comment saying why. `regplot` silently drops the 56 null rows, so 1173 points are drawn, and the prose should say so. The author reads the curve from the output. On the slide it falls until about 0.6 and then flattens. Add a short `{tip}` for "You are the driver, not the LLM": you decide what to plot and why, and an LLM can help with the syntax. The tip carries the slide's cognitive-offloading quote with a citation (open question 8). Keep it well short of EDA I's LLM note, and don't repeat that note's energy/water/politics list.

3. **What the curve averages, and whether every school should count equally** (S29–S31). *Concept: by default every point in a plot carries equal weight, and that default is a choice.* Keep the slide's intuition (average the points in each "bin" and connect the dots) and call it a simplification. Add a `{note}` on what actually runs. Checked: seaborn calls statsmodels' `lowess` with its defaults, which fits a line to the nearest two-thirds of the data around each x, weights closer points more, and does 3 robustifying passes. Schools range from **14 to 1392** 12th graders, so bigger schools arguably deserve more influence. The slide says weighting LOWESS needs "more specialized tools than Seaborn". Keep that wording. `regplot` has no weights argument, and statsmodels' `lowess` doesn't have one either, so don't name it as the tool. End on S31's question: what should the weight be? The candidates are the 12th-grade class, total enrollment, and the number who applied.

4. **Sizing points by a third variable** (S35, S36, S32–S34, S37). *Concept: visual weight is an analytic decision, so choose it to match the message.*
   a. S35: `sns.scatterplot(admissions, x='pct_free_reduced', y='app_rate', size='grade_12')`, with English → Seaborn. This gives labels and a size legend, both checked.
   b. S36: `sizes=(1, 100)` widens the range. Point to the seaborn `scatterplot` documentation, because a formatting argument like this is something you look up.
   c. S32: the four candidates side by side in one 2×2 figure (A unsized, B `grade_12`, C `tot_enrolled`, D `applied`). Use a **`Click to see the code` dropdown + `remove-input`** cell, since `plt.subplots`/`ax=` is layout code nobody needs to read. Each panel is the S36 call with a different `size=`. What each one says: A misleads, because the schools at high `app_rate` are small (checked: median `grade_12` is 164.5 for `app_rate > 0.5` against 337 overall; e.g. MIDDLE COLLEGE HIGH SCHOOL has 60, MAKING WAVES ACADEMY 77, RENAISSANCE ARTS ACADEMY 27). B and C are nearly identical, and they differ because of dropout and how many grades a school offers. D partly repeats the y-axis, because `applied` is `app_rate`'s numerator.
   d. S33–S34: take a stand. B shows where the possible applicants are, and D shows where the actual applicants come from. There is no single right answer. The storyteller decides.
   e. S37: are you picking the same five schools? With sizing, the eye moves to large, low-FRL schools. The author reads the names from the output, e.g. MONTA VISTA, LYNBROOK, DOUGHERTY VALLEY. This leads to "to reach the most students, focus on larger schools?"

5. **Counting the students behind a rate** (S38–S39). *Concept: a derived count is only as good as the assumption behind it.* English: "Add a column with the number of 12th graders who qualify for free or reduced-price meals." Polars: `admissions.with_columns(num_frl_12th=(pl.col('pct_free_reduced') * pl.col('grade_12')).cast(int))`, then `.select(...)` to show the four relevant columns. This is **the first `.cast()`**. It changes a column's type, `int` gives `i64`, and **a float cast to an integer drops the fractional part** (A B MILLER: 0.685365 × 485 = 332.4 → 332). SQL: `SELECT *, CAST(TRUNC(pct_free_reduced * grade_12) AS INTEGER) AS num_frl_12th FROM admissions`. **The `TRUNC` is required.** Checked: DuckDB's `CAST(... AS INTEGER)` *rounds*, and without `TRUNC` the SQL disagrees with Polars on 581 of 1229 rows. S38 asks whether the calculation could be wrong. Answer it in prose with three reasons: it assumes 12th graders qualify at the school-wide rate; it truncates rather than rounds; and the 56 null shares give 56 null counts.
   Then comes the proposed "new answer" (open question 4): sort by `num_frl_12th`, descending, with `nulls_last=True`, which EDA I §12 introduces (*critic:* moved there). A clause recalls why: Polars puts nulls first, so without it those 56 rows fill the top of the table (checked). SQL: `... ORDER BY num_frl_12th DESC NULLS LAST`, checked equal to the Polars top rows. From the output: PARAMOUNT HIGH SCHOOL 758, VISIONS IN EDUCATION 693 (a charter with 1392 12th graders and `app_rate` ≈ 0.02). These are big schools with low application rates.

6. **Are we done?** (S40). *Concept: an answer isn't finished until "typical" is defined.* One short paragraph: "typical" is still undefined, admission and attendance are untouched, and the next step is broad patterns in all three outcomes.

7. **Summarizing patterns, and tidy data** (S41–S44). *Concept: a summary plot needs a summary table, one row per plotted point and one column per feature.*
   - Plot A is every school (refer back to §4). Plot B is four points, application rate by FRL-percentile bin, regenerated in a **dropdown + `remove-input`** cell (`qcut(4, labels=[...])` → filter nulls → `group_by("frl_percentile").agg(...)` → `.cast(pl.String)` → `.sort` → `sns.lineplot`). The prose says the next chapter builds this step by step (open question 2). *Critic:* one sentence before the dropdown also previews each verb the folded code uses: `qcut` splits the schools into four equal-sized groups by `pct_free_reduced`, `group_by(...).agg(...)` totals `applied` and `grade_12` within each group, `.cast(pl.String)` turns the group labels into plain text for seaborn, and `sns.lineplot` joins the four points. That sentence is what makes these verbs introduced where they are first used. EDA III still teaches each one in full. Checked: without `.cast(pl.String)`, seaborn raises on the `Categorical` bin labels in `d100`.
   - A `{note}` taken from S42: the 0–25 bin is the quarter of schools with the lowest `pct_free_reduced`, not the schools below 0.25. Checked: the bin runs up to about **0.341** and holds **294** schools, while only **169** are below 0.25. Bin sizes are 294/293/293/293, totalling 1173.
   - Optional, and a departure (the slide only describes it): S42's "nearly transparent points + bold curve", done as `regplot` with `scatter_kws={"alpha": 0.1}` and the LOWESS line. That uses only §2's call.
   - Tidy data (S43): plot B has 4 points, so it needs 4 rows, and 2 features, so it needs 2 columns. The folded cell displays the four-row table. Checked values: **0.256, 0.117, 0.087, 0.094**, which match S44's 0.26/0.12/0.087/0.094. These are **total applicants ÷ total 12th graders in each bin** (lec04 c11), a `grade_12`-weighted average that ties back to §3. The unweighted mean of `app_rate` would be 0.260/0.134/0.109/0.123 (open question 3). *Critic:* the chapter says in one sentence what `avg_app_rate` is and stops there. Comparing it with the unweighted mean is EDA III §10's job (L04 S35), so those four numbers do not appear in this chapter. Add one sentence generalizing the definition so it holds outside plotting: each row is one observation and each column one variable, and here the observations are plotted points (open question 9).
   - End on S44's "How do we generate this data?" and leave it open.

8. **Anatomy of a seaborn call** (S45). *Concept: every seaborn call has the same four parts, and only the mappings need thought.* A small table: plotting function (`scatterplot`, `lineplot`, `histplot`, …), the `DataFrame`, the column mappings (`x`, `y`, `size`, `hue`), and formatting arguments, which you look up. Use the §4 call, not a new code block.

9. **Operations so far, and grouping** (S46–S48). *Concept: split-apply-combine.* S46's list is English only (preview, select, new columns, filter, order, summary statistics, 1-D plots, 2-D plots, group). It builds to the template "For each unique value of COLUMN(S), do SOMETHING."
   - Count (S47), `images/split_apply_combine_count.png`: "For each unique value of `city`, count the rows." The reader already ran one split-apply-combine in EDA I, and a live callback cell shows it: `admissions["city"].value_counts(sort=True).head(5)`. SQL: `SELECT city, COUNT(*) AS count FROM admissions GROUP BY city ORDER BY count DESC LIMIT 5`. Checked equal: Los Angeles 100, San Diego 41, San Jose 31, Oakland 28, Sacramento 27. These differ from EDA I §21's 112/41/31/28/28 because this is §1's 1,229-row filtered frame, and the prose says so in a clause (*critic*, re-checked in `d100`). Use `head(5)`, not S24's `head(10)`, because at 10 rows San Francisco and Fresno tie at 17 and `value_counts` doesn't fix their order.
   - Mean (S48), `images/split_apply_combine_mean.png`: "For each unique value of `city`, compute the mean `tot_enrolled`." Show the diagram and the English only. The code is `group_by().agg()`, which is EDA III's (L04 S13/S16). Optionally, one sentence from S48's annotation, without the personal reference: a city with one school forms a group of one, and its "mean" is that school's enrollment.
   - Close: the next chapter writes "For each…" statements like these in Polars and uses them to build §7's table. (*Critic:* EDA III writes per-county counts and per-customer sums, not this per-city mean, so don't promise these two statements by name.)

**Polars verbs this chapter introduces for the first time.** Each gets one or two sentences before its first call.

| Verb | Where | Note |
|---|---|---|
| `.cast(int)` | §5 | Truncates when going from float to integer. The SQL pair needs `TRUNC`. |
| `pl.col(a) * pl.col(b)` | §5 | A one-clause extension of EDA I's column division. |
| `qcut`, `group_by().agg()`, `.sum()` in `agg`, `.cast(pl.String)`, `sns.lineplot` | §7, folded cell only | **Previewed, not taught** (*critic*). One sentence before the dropdown says what each does, and EDA III teaches them. `nulls_last=True`, `value_counts(sort=True)` and `.head(n)` moved to EDA I. |

New seaborn/matplotlib calls: `sns.regplot` (`lowess=`, `line_kws=`, `scatter_kws=`), `sns.scatterplot` (`size=`, `sizes=`), `plt.xlabel`/`plt.ylabel`.
**Only inside folded dropdown cells:** the §7 preview verbs above, and `plt.subplots`/`ax=` in §4c, which EDA I §18 introduces.
**Assumed from EDA I:** `pl.read_csv`, `with_columns` (keyword form), `pl.col`, `.filter`, `.sort(descending=)`, `.sort(..., nulls_last=True)`, `.select`, `df["col"]`, `value_counts(sort=True)`, `.head(n)`, `.describe`, `len`/`.shape`/`.height`, `.is_not_null`, `sns.boxplot`, `sns.histplot`, `plt.subplots`/`ax=`, and SQL `GROUP BY`/`COUNT(*)`/`LIMIT`.

**SQL for the claim verifier.** In §1, `admissions` is the CSV. Everywhere after, it is §1's result (1229 rows plus `app_rate`), and §5's queries add `num_frl_12th` themselves. No `SELECT` alias appears in a `WHERE`. `ORDER BY` an alias is used, and DuckDB accepts it.

**Data.** One file: `content/new_eda_2/data/pivoted-ucb-data-w-everything.csv`, copied from `main:content/new_eda_1/data/pivoted-ucb-data-w-everything.csv` (md5 `4c9d424fbb7d930419c18cb11d5517b1`, identical to `fa26-dev/lec/lec04/data/`). It is already in place. Not lec06's copy, which writes nulls as `"NA"`.

**Images.** `split_apply_combine_count.png` (L03 `image50`, S47) and `split_apply_combine_mean.png` (L03 `image52`, S48), with the manifest's alt text. Every plot is regenerated: S28 `image53`, S32 `image54`/`55`/`56`/`58`, S35 `image60`, S36 `image56`, S42/S44 `image57`, S47 `image51` (as the `value_counts` output). S48's `image59` (a pandas `groupby().mean()` output) isn't reproduced, because that code is EDA III's.

---

### Learning Outcomes (proposed)

```
::: {note} Learning Outcomes
* Overlay a LOWESS curve on a scatter plot with `sns.regplot(..., lowess=True)` and explain what the curve summarizes
* Size the points of a scatter plot by a third variable with `sns.scatterplot(..., size=...)`, and justify which variable to use
* Derive a count from a rate and a total with `.with_columns()` and `.cast()`, and name the assumptions that could make it wrong
* Describe the tidy table a plot needs: one row per plotted point, one column per feature
* Phrase a grouping question as "For each unique value of …, do …" and trace it through split, apply, and combine
:::
```

### Open questions for course staff

1. **EDA I has to grow for these deletions to hold.** `main`'s draft of `new_eda_1` stops at L02 S45 (cell `95`, modality). L02 S46–S60 aren't in it: CDE sources, the join to the expanded data, the `dist_to_ucb` plots, three peaks, the population map, `value_counts` by city, and the FRL starting point. This outline deletes L03 S12–S26 on the assumption that EDA I's fix pass adds them, which its manifest rows (the CDE screenshots and population map) imply. If EDA I isn't extended, S12–S26 come back here. **Resolved (critic):** EDA I's outline extends through L02 S60 (its §19–§22), so the deletions hold.
2. **Two folded cells use code EDA III teaches**: the 2×2 comparison (§4c) and plot B with its tidy table (§7). This is the book's own `Click to see the code` pattern, used for layout rather than to hide a misbehaving cell. But `notes-lecture-fidelity-reviewer` check 5 will read `qcut`/`group_by` in a live cell as "used before introduced". Approving this outline should mark those two cells exempt, and the prose must say the code is built in EDA III. The alternative is to show plot B for the first time in EDA III and leave §7 with plot A only. *Critic's resolution, pending approval:* no exemption is needed. With the one-sentence preview in §7, and EDA I's sentence on `plt.subplots`/`ax=`, every verb in both folded cells is named before it is used, which is what check 5 asks for. This also closes EDA III's open question 9.
3. **What does `avg_app_rate` mean?** The slide's numbers are total applicants ÷ total 12th graders per bin (a weighted mean). They are not the mean of `app_rate`. Recommend keeping the name (L03, L04 and lec04 all use it) and saying in one sentence what it is. EDA III must use the same definition (*critic:* it does, in its §10).
4. **The "new answer" at S40 has no code in the deck.** Proposal: sort by `num_frl_12th` (§5), which fits S37's "impact the most students". The alternative is prose only.
5. **Reordering S35–S36 ahead of S32–S34**, so the four-way comparison comes after the reader has met `size=`. Nothing is used before it is computed.
6. **Frame name.** The slides use `df`/`df_new` (and mix them: S19/S28/S35 use `df_new`, S21–S22 use `df`), EDA I's draft uses `hs_enroll`, and L04 uses `admissions`. Recommend `admissions` for EDA I–III, so the Polars name and the SQL table name match. **Resolved (critic):** `admissions` in all five outlines.
7. **Drop `cde_frpm_data_source.png` from `new_eda_2`.** L03 `image28` differs from L02 `image42` only in crop (same heading, same sentence), and EDA I keeps the latter. If a reminder of where `pct_free_reduced` comes from is wanted, a sentence pointing back to EDA I is enough.
8. **The S28 quote needs a citation.** "Over four months, LLM users consistently underperformed at neural, linguistic, and behavioral levels" appears to be from Kosmyna et al. (2025), *Your Brain on ChatGPT* (MIT Media Lab, arXiv:2506.08872). The slide cites nothing. Staff should confirm the source and the link before it goes into a textbook.
9. **Tidy data is defined nowhere else in the book** (checked). The lecture defines it for plotting. Recommend one extra sentence that generalizes it to rows as observations and columns as variables, so it holds outside plots.
10. **The S24 hand-off.** Recommend that EDA I write L02 S58 as `value_counts(sort=True)`, the conventions spelling. If it also shows the top rows with `.head(n)`, then `.head` is introduced in EDA I and drops off this chapter's list. **Resolved (critic):** EDA I §21 does both, and this chapter assumes them.
11. **"Correlate" without a coefficient.** S25–S26 say "correlation" loosely, and the deck never computes one (checked: `pl.corr("pct_free_reduced", "app_rate")` gives −0.43). Recommend leaving the coefficient to the modeling chapters and keeping the word informal here.

---

## `new_eda_3` — EDA III: Grouped Operations and Missing Data

**Status: approved**

A new chapter, authored from **L04 S11–S46** and **`lec04.ipynb` c0–c30**. S4–S10 recap EDA II and are not
taught again. `lec04.ipynb` c31–c43 (distance percentile, the two-key FRL × distance grouping, the 3-D plotly
figure, and the `FacetGrid` final pick) are L05 S10–S19 material and belong to **EDA IV**. They are left out here.

Every number below was executed under polars 1.43.1 (`d100`) and DuckDB 1.3.0 against
`pivoted-ucb-data-w-everything.csv`, after the EDA I recap filter (1,229 schools).

### What the chapter is for

EDA II ends on a four-row table, the pooled application rate for each FRL-percentile bucket, and asks "how do we
generate this data?" EDA III answers that question. The first half teaches `group_by` on small questions whose
answers can be checked by eye. The second half builds the FRL table in three steps, then moves from application
rates to admission rates and runs straight into missing data: **418 of the 1,229 schools have a null `admitted`**.
It closes on the PCS stability check and on the observation that admission rates move the opposite way to
application rates, which EDA IV takes up.

| Slides | Content | Disposition |
|---|---|---|
| S1–S3 | Slido join, title, announcements | **Deleted.** |
| S4–S10 | "Fundamental operations so far", the summarizing-patterns plot, seaborn call anatomy, tidy data, split-apply-combine diagrams | **Deleted. EDA II owns them** (L03 S42–S48, including `split_apply_combine_count.png` and `split_apply_combine_mean.png`). One opening paragraph points back to EDA II's four-row table and the "For each…" form. No recap figure. |
| S11 | "Write an analysis statement in the form 'For each…'" | **Kept** as the frame for §2–§6: each section opens on a question, then states its "For each…" plan. |
| S12, S14, S17, S20, S22, S25, S29, S34, S40 | Slido prompts | **Deleted as slides.** Each prompt becomes the question that opens its section. |
| S13 | Counties with the most schools: `group_by().len()` or `.agg(num_schools=pl.len())` | **Kept**, run on the real data (54 counties; Los Angeles has 321 schools). The slide's schematic County A/B/C table is dropped because the real output is short enough to read directly. |
| S16 | Which customers spend the most: `group_by().sum()` | **Rewritten** on a six-row inline `transactions` frame and taught as `.agg(total_cost=pl.col("cost").sum())`. The slide code fails in two ways (see bugs). |
| S18–S19 | Top two schools per county; "More on `df.head(n)`" | **Kept and reordered.** `.head(3)` on the whole frame comes first (SQL `LIMIT 3`), then `sort` → `group_by` → `head(2)`. Adds `nulls_last=True`. The SQL is replaced because the slide's query is wrong. |
| S21 | Group by two columns | **Kept**, on the same `transactions` frame. |
| S15, S23 | Which customer spent the most each day (repeated grouping) | **Merged.** S15 is an out-of-order copy of S23. **Kept short**: it is §5 and §6 composed, and the Polars chain is one line. The SQL is given in its window-function form and labelled as beyond what students are asked to write, which is what S23 itself says. |
| S24, S26, S30, S32 | Tidy data redux: the three-step plan (percentile → bucket → per-bucket rate), shown four times | **Kept once** as §7. The repeats are deleted. |
| S27 | LLM screenshot: percentile rank as `rank() / pl.count()` | **Rewritten** as prose plus a live cell. The screenshot is not used (LLM chat). Its denominator becomes the teaching point in §8. |
| S28 | `frl_percentile_raw = rank() / count()` and "does it pass the sniff test?" | **Kept**, with the sniff test made concrete. |
| S31 | LLM screenshot: `qcut(4, labels=…)` | **Rewritten** as prose plus a live cell. Screenshot not used. |
| S33, S35, S36, S39, S41 | Per-school table with `frl_percentile` (image41); "don't average `app_rate`"; "sum up and divide" | **Kept**, with the table regenerated from code. image41 is stale: it labels Abraham Lincoln (San Francisco), at raw percentile 0.368, as `0-25`, while the `lec04` code gives `25-50`. |
| S37 | Group-wise application rate, `.agg(…)` plus SQL | **Kept.** `.sum` becomes `.sum()`, and the `is_not_null` filter that the notebook applies (c11) is shown and explained. |
| S38 | `sns.pointplot` recreating EDA II's plot | **Kept**, regenerated. |
| S42 | Four ways to handle a null `admitted`, plus the image54 table of nulls | **Kept.** The table is regenerated from code. |
| S43 | The PCS framework (Bin Yu) | **Kept.** |
| S44 | Four admission-rate plots, one per strategy | **Kept**, regenerated as **one 2×2 figure with a shared y-axis**. Each slide plot autoscales its own axis, which makes a 0.016 swing look as large as a 0.05 one. |
| S45 | Application and admission rates show opposite patterns | **Kept**, regenerated. It ends the chapter as an open question. The explanation (selection effects, UC policy) is EDA IV's (L05 S4–S6). |
| S46 | Closing slide | **Deleted.** |

**Proposed shape**

0. **Frontmatter, Learning Outcomes, opener.** `title: EDA III` as the first construct in cell 0. The opener
   speaks in the first person plural: in EDA II we ended with a four-row table and a plot; in this chapter we
   will learn to build that table, and along the way meet our first real decision about missing data.
1. **Where we left off.** One setup cell (`polars`, `seaborn`, `numpy` for §13's random draw,
   `matplotlib.pyplot as plt`, `sns.set_palette("colorblind")` and EDA I's `pl.Config.set_fmt_str_lengths(40)`;
   EDA I itself has no `numpy`), then one cell that loads the CSV, recomputes `app_rate`,
   and filters to `app_rate <= 1`, giving 1,229 rows. There is no triple here because EDA I taught all three
   operations. *Concept:* a grouped operation has two parts, the column that defines the groups and what we do
   to each group. `group_by` is the Polars spelling of "for each unique value of".
2. **Counting rows per group** (S13). *Which counties have the most schools?*
   English: "For each unique value of `county`, count the rows. Sort in descending order of that count."
   Polars: `admissions.group_by("county").len().sort("len", descending=True)`, then the same thing as
   `.agg(num_schools=pl.len())`, which names the column and sets up §3. SQL:
   `SELECT county, COUNT(*) AS n_schools FROM admissions GROUP BY county ORDER BY n_schools DESC`.
   Reading: 54 rows, one per county, led by Los Angeles (321), San Diego (94) and Orange (77). The other columns
   did not matter. `admissions["county"].n_unique()` also returns 54, but it answers a different question
   ("how many counties?"), and the section says so in one sentence. A second sentence connects this to EDA I's
   `value_counts` (its §21), which gives the same counts.
3. **Aggregating a column within each group** (S16). This section introduces the toy `transactions` frame with
   `pl.DataFrame({...})`: six rows of `customer_id`, `date` and `cost`, taken from S21.
   *Which customers spend the most?* "For each `customer_id`, sum `cost`, then sort descending."
   `transactions.group_by("customer_id").agg(total_cost=pl.col("cost").sum()).sort("total_cost", descending=True)`
   gives A 130 and B 90. *Concept:* `.agg` takes named expressions and returns one row per group; each output
   column is either a group key or something you named. The shortcut `group_by(...).sum()` sums every non-key
   column, so on this frame it raises on the string `date` column. Say what you want in `.agg` instead. SQL:
   `SELECT customer_id, SUM(cost) AS total_cost … GROUP BY customer_id ORDER BY total_cost DESC`.
4. **The first rows of each group** (S19, then S18). Start with `admissions.head(3)`, which
   recalls EDA I's `.head(n)` and SQL `LIMIT`.
   *In each county, which two schools admitted the most students?* "Sort the whole table in descending order of
   `admitted`. Then, for each county, take the first two rows."
   `admissions.sort("admitted", "school", descending=[True, False], nulls_last=True).group_by("county").head(2)`,
   then `.sort("county", "admitted", "school", descending=[False, True, False], nulls_last=True)` for display.
   **Critic (checked in `d100`):** the `"school"` tie-breaker is required. In 11 counties the second- and
   third-ranked schools tie on `admitted`: Kern, Napa and Sonoma at 7, Riverside at 19, San Diego at 29, Yuba at
   3, and Colusa, Lake, Nevada, Shasta and Siskiyou with both null. Without it, *which* school `head(2)` keeps
   depends on how the sort orders ties, and Polars does not promise an order. This is the chapter's first
   sort on several keys: one sentence says rows are ordered by the first key, ties are broken by the next, and
   `descending=` takes one flag per key. The English line can keep the lecture's one-key plan, with a clause on
   why the code adds a key. *Concept:* `.head` on a grouped frame keeps
   **every** column, unlike `.agg`. It takes rows in the order they were in before grouping, which is why the
   sort comes first. A `{tip}` recalling EDA I §12: Polars puts nulls first when it sorts, so without `nulls_last=True` 95 of the
   101 rows would be schools with a null `admitted`. Even with it, 22 null rows remain, because 12 counties
   (Amador, for example) have no school with a reported admit count. That is a forward pointer to §12.
   SQL: `SELECT * FROM admissions QUALIFY ROW_NUMBER() OVER (PARTITION BY county ORDER BY admitted DESC, school) <= 2`
   (the critic added `, school`, and checked the 101 rows equal to the Polars result in DuckDB),
   presented as a window function that we do not ask students to write. DuckDB sorts nulls last on `DESC` by
   default, so this query matches the Polars output only because of `nulls_last=True`.
5. **Grouping on more than one column** (S21). *How much did each customer spend each day?* "For each unique
   combination of `customer_id` and `date`, sum `cost`."
   `transactions.group_by("customer_id", "date").agg(total_cost=pl.col("cost").sum())`, sorted by date and
   customer, gives four rows: A 6/1 10, B 6/1 60, A 6/2 120, B 6/2 30. *Concept:* the groups are unique
   *combinations*. SQL: `GROUP BY customer_id, date`.
6. **Grouping twice** (S15/S23). *Which customer spent the most on each day?* "Sum by customer and date. Sort
   descending by the total. Then, for each date, take the first row." This is one chain built on §5's result,
   and it returns 6/1 B 60 and 6/2 A 120. *Concept:* the second `group_by` throws away the first grouping and
   defines new groups. The SQL uses `QUALIFY ROW_NUMBER() OVER (PARTITION BY date ORDER BY total_cost DESC) = 1`,
   shown in a `{note}` as beyond what we ask students to write.
7. **Back to the FRL table: a three-step plan** (S24–S26). The target is a tidy table with 4 rows (one per point)
   and 2 columns. The plan: (1) compute each school's FRL percentile; (2) put each school into one of four
   buckets; (3) for each bucket, compute the application rate. *Concept:* the English plan doubles as the prompt
   you would give an LLM (S25). You supply the plan, and the LLM supplies syntax you do not need to memorize
   (S26).
8. **Step 1: percentiles with `.rank()`** (S27–S28). Definition: a school's percentile is the fraction of schools
   whose `pct_free_reduced` is at or below its own. `.rank()` numbers the schools 1, 2, …, n (ties get the
   average rank), and we divide by the number of schools. **Which number?** An LLM's answer (described in
   prose) divides by `pl.count()`, an older name for `pl.len()`. That counts all 1,229 rows. A live cell with
   `rank() / pl.len()` shows the maximum reaching only 0.954, which fails the sniff test: the 56 schools with no
   FRL value are counted in the denominator but never ranked. `pl.col("pct_free_reduced").count()` counts only
   non-null values, and the maximum becomes 1.0. *Concept:* `.count()` counts values that are present,
   `pl.len()` counts rows, and a quick look at min/max catches the difference. Do not run `pl.count()` in a
   cell, because it prints a `DeprecationWarning`. No SQL here: the lecture gives none, and §9's SQL covers
   steps 1 and 2 together.
9. **Step 2: buckets with `.qcut()`** (S30–S31).
   `pl.col("frl_percentile_raw").qcut(4, labels=["0-25", "25-50", "50-75", "75-100"]).cast(pl.String)`.
   Counting the buckets reuses §2 and gives 294 / 293 / 293 / 293, plus 56 nulls. *Concept:* `qcut` cuts at
   quantiles, so every bucket holds a quarter of the schools. That answers `lec04`'s note ("how does `qcut`
   create bins?") and makes EDA II's caution concrete: `0-25` is the lowest quarter of schools, not schools with
   `pct_free_reduced < 0.25`. One sentence adds that `qcut` applied to `pct_free_reduced` directly gives the same
   bucket for all 1,173 schools; the percentile column is there for us to read and check. The `.cast` is
   described as storing the labels as plain strings, which already sort in the right order. SQL:
   `NTILE(4) OVER (ORDER BY pct_free_reduced)` over the non-null rows, which matches `qcut` for every school
   (verified).
10. **Step 3: group-wise rates, weighted by school size** (S33–S37). Regenerate the per-school table
    (`school`, `pct_free_reduced`, `frl_percentile_raw`, `frl_percentile`, `applied`, `grade_12`, `app_rate`,
    `.head(5)`). *Should we average `app_rate`?* No: a school with 10 seniors should not count as much as one
    with 1,000. The bucket's rate is total applicants divided by total 12th graders. Polars:
    `.filter(pl.col("frl_percentile").is_not_null()).group_by("frl_percentile").agg(applied=…, grade_12=…,
    avg_app_rate=pl.col("applied").sum() / pl.col("grade_12").sum())`, then `.sort("frl_percentile")`. This is
    the first proper explanation of `is_not_null`: without the filter, the 56 unbucketed schools form a fifth,
    null group. Put `mean_app_rate=pl.col("app_rate").mean()` beside the pooled rate so the reader can see the
    weighting matter. The unweighted mean is higher in every bucket (0.260 vs 0.256, 0.134 vs 0.117, 0.109 vs
    0.087, 0.123 vs 0.094), because small schools with high rates pull it up. SQL:
    `SELECT frl_percentile, SUM(applied) / SUM(grade_12) AS avg_app_rate FROM admissions WHERE frl_percentile IS NOT NULL GROUP BY frl_percentile`.
11. **Recreating the plot** (S38).
    `sns.pointplot(app_by_frl, x="frl_percentile", y="avg_app_rate", order=[…], marker="")`, ending in `;`.
    Reading: 0.256 → 0.117 → 0.087 → 0.094. The `#| fig-alt:` quotes those four values. *Concept:* a tidy table
    goes in with one row per point, and seaborn draws exactly what is there.
12. **Admission rates and the nulls in `admitted`** (S39–S42). *What is the admission rate in each bucket?* The
    naive plan is total admits divided by total applicants. `null_count()` shows 418 null `admitted` values (391
    of them in bucketed schools). Regenerate the image54-style peek at `school`, `applied`, `admitted` and
    `attended`. Why null: UC leaves counts below three blank (EDA I explains this), and the smallest reported
    `admitted` is 3, so a null means 0, 1 or 2. **Key concept:** `.sum()` skips nulls, so the naive computation
    has already made a choice. It is identical, to every digit, to replacing nulls with 0. Not choosing is a
    choice. Then list S42's four options.
13. **Four ways to fill in `admitted`** (S42–S44 code). All four work on one `binned` frame (the §10 filter
    applied once). Each option gets an English line, a live Polars cell, and a SQL line:
    - ignore: `.filter(pl.col("admitted").is_not_null())` / `WHERE admitted IS NOT NULL`
    - replace with 0: `.with_columns(pl.col("admitted").fill_null(0))` / `COALESCE(admitted, 0)`
    - replace with 2: `.fill_null(2)` / `COALESCE(admitted, 2)`
    - replace with a random 0, 1 or 2: `rng = np.random.default_rng(7342)`, then
      `pl.when(pl.col("admitted").is_null()).then(pl.Series(rng.integers(0, 3, size=binned.height))).otherwise(pl.col("admitted"))`.
      Show the SQL `CASE WHEN admitted IS NULL THEN … ELSE admitted END` for its shape only, and say in one
      sentence why its numbers will not match (a different random generator).
    *Concept:* `pl.when().then().otherwise()` is a per-row if/else, and the seed makes the page reproducible.
14. **Stability: the PCS framework** (S43–S44). Define Predictability, Computability and Stability, and credit Bin
    Yu. Figure: a 2×2 grid built with `plt.subplots(2, 2, sharey=True)` and one `sns.pointplot(…, ax=…)` per
    strategy, with the shared axis explained in one sentence. Reading, all verified: in every version the two
    higher-FRL buckets admit at a higher rate than `0-25`. How large that gap is depends on the choice: `75-100`
    ranges from 0.134 (fill 0) to 0.176 (ignore), while `0-25` only moves between 0.122 and 0.127. The reason is
    that nulls pile up in the higher buckets (49 in `0-25`, against 108–118 in each of the others). *Optional
    beat (open question 4):* 0 and 2 bracket the truth, so the true rate lies between the fill-0 and fill-2
    lines. "Ignore" lands **above** fill-2 in all four buckets, which is outside the possible range, because the
    schools it drops are exactly the ones that admitted at most 2. The chapter continues with random imputation
    as its working choice, as L04 S45 and EDA IV do.
15. **Admission rates move the other way** (S45). A side-by-side figure: application rate falls
    (0.256 → 0.094), while admission rate under random imputation rises (0.123, 0.129, 0.152 and 0.149 across
    the four buckets). EDA IV §1 reproduces these exactly by copying this chapter's cell, so the seed (7342) and the
    draw over `binned` belong to this chapter (*critic*, re-checked in `d100`). The chapter closes on the question "what could cause this?" and hands it to EDA IV, without
    explaining it.

**Net effect:** the chapter teaches a single grouping idiom, `sort` → `group_by` → `.agg` / `.len()` / `.head()`,
on small questions whose answers can be checked by eye. It then puts that idiom to work building the one table
EDA II left unexplained. Its missing-data half carries the chapter's two load-bearing ideas: an aggregate that
skips nulls has already chosen how to treat them, and a stability check shows how much that choice matters.

### Learning Outcomes (as they would appear in cell 0)

```
::: {note} Learning Outcomes
* Write a "For each…" analysis plan and carry it out with `.group_by()` and `.agg()`
* Count rows per group with `.group_by().len()`, and group on more than one column
* Take the top rows of each group with `.sort()` followed by `.group_by().head()`
* Compute percentiles with `.rank()` and split them into equal-sized buckets with `.qcut()`
* Compute a group-wise rate that weights each school by its size
* Find and fill missing values with `.is_null()`, `.fill_null()` and `pl.when()`
* Use the PCS framework's stability check to judge a missing-data decision
:::
```

(EDA I's draft uses `-` bullets, and its outline switches to `*`, the house style in 28 of 30 chapters.)

### Polars verbs this chapter introduces for the first time

The reader already knows, from EDA I: `pl.read_csv`, `len(df)` / `.shape` / `.height`, `df["col"]` and Series
`.min()`, `.with_columns(name=expr)`, `pl.col`, `.filter`, `.sort(descending=)`, `.sort(..., nulls_last=True)`,
`.select`, `.describe`, `value_counts(sort=True)`, `.head(n)`, `.is_not_null()` (named in prose in §14),
`plt.subplots`/`ax=` (folded cells), `histplot` / `boxplot`, and SQL `GROUP BY` / `COUNT(*)` / `LIMIT`. From EDA II:
`.cast(int)` and the seaborn `regplot` / `scatterplot` calls. EDA II §7 also previews `qcut`, `group_by().agg()`
and `.cast(pl.String)` in one sentence beside a folded cell, so this chapter can say we glimpsed them there, but
it still teaches each one in full (*critic*). Each verb below gets one or two
sentences where it first appears:

| Verb | First used in | Note |
|---|---|---|
| `.group_by(...)` | §1–§2 | Output row order is not stable, so every displayed group result is sorted afterwards. `maintain_order` is not used. |
| `.group_by(...).len()` → column `len`; `pl.len()` | §2 | Rows per group. |
| `.agg(name=expr)` | §2–§3 | Keyword names only. |
| `Series.n_unique()` | §2 | How many distinct values; contrasted with rows per group. |
| `pl.DataFrame({...})` | §3 | First frame built from a dict. |
| expression aggregates `pl.col(c).sum()`, `.mean()` | §3, §10 | EDA I only used Series `.min()`. |
| `.group_by(...).head(n)` | §4 | Keeps all columns. |
| `.sort("a", "b", descending=[…])` (several keys) | §4, §5 | The `school` tie-breaker in §4 (*critic*). `nulls_last=True` itself is EDA I's. |
| `group_by("a", "b")` (two keys, positional) | §5 | |
| `pl.col(c).rank()` | §8 | |
| `pl.col(c).count()` vs `pl.len()` | §8 | Non-null count vs row count. |
| `pl.col(c).qcut(k, labels=[…])` | §9 | Previewed in one sentence in EDA II §7; taught here. |
| `.cast(pl.String)` | §9 | EDA II uses `.cast(int)` (L03 S39); the dtype is new. |
| `is_not_null()` in a live cell | §10 | EDA I §14 names it in prose. This is its first live use and full explanation. |
| `null_count()`, `is_null()` | §12 | |
| `fill_null(value)` | §13 | |
| `pl.when().then().otherwise()` | §13 | |
| `pl.Series(np_array)`, `np.random.default_rng(seed).integers` | §13 | Replaces `polars_random`. |
| `sns.pointplot(..., order=, marker="")` | §11 | New plot type. |
| `sharey=True` on `plt.subplots` | §14 | `plt.subplots`/`ax=` come from EDA I §18's folded cell. The shared axis is new. |

SQL that appears for the first time: `SUM` with `GROUP BY` (EDA I §21 introduces `GROUP BY` with `COUNT(*)`,
`ORDER BY … DESC` and `LIMIT`), multi-column `GROUP BY`, `IS NOT NULL`, `COALESCE`, `NTILE`, and, labelled as beyond scope, `QUALIFY
ROW_NUMBER() OVER (PARTITION BY …)`.

### The English → Polars → SQL triple

Each operation keeps the lecture's three columns, in this order: an **English** line (the "For each…"
sentence), then the **live Polars cell**, then a **SQL** block. The Polars code is not printed a second time
(fa26-course-conventions). Every SQL block must run in DuckDB against the CSV registered as `admissions` (with
`app_rate` and `frl_percentile` added where the query uses them), and it must reproduce the Polars output
beside it. All of the queries above were checked this way. Where the lecture gives no SQL (S23, S28), the chapter
either gives the verified query marked as beyond scope (§6, §9) or says why it has none (§8, §13's random fill).

### Data

| File the chapter reads | Source |
|---|---|
| `data/pivoted-ucb-data-w-everything.csv` (1,268 × 11) | fa26-dev `lec/lec04/data/pivoted-ucb-data-w-everything.csv`, md5 `4c9d424fbb7d930419c18cb11d5517b1`. Byte-identical to `main:content/new_eda_1/data/pivoted-ucb-data-w-everything.csv`. The untracked copy already in `content/new_eda_3/data/` has the same md5. |
| `transactions` | Inline `pl.DataFrame`, no file. |

**Not used:** lec06's copy that encodes nulls as `"NA"`, which belongs to EDA V's faithfulness section. Also not
used: `pivoted-ucb-data.csv` and `pivoted-ucb-data-w-enrollment.csv`, which are EDA I's build-up.

### Figures and images

**No manifest images.** Every figure is regenerated from code, each with a `#| fig-alt:` that quotes the computed
values and a trailing `;` so no `<Axes>` repr leaks:

1. §11: pointplot of the pooled application rate by FRL bucket.
2. §14: 2×2 shared-y grid of admission rate by bucket, one panel per missing-data strategy.
3. §15: application rate and admission rate side by side.

The slide tables (image41, image54, and the S13/S16/S18/S21 schematic tables) become live outputs. The L04 LLM
screenshots (image38, image42) are skipped. The split-apply-combine diagrams (L04 image7/image13 = L03
image50/image52) belong to EDA II and are not repeated here.

### Slide and notebook bugs not to copy (EDA III–specific)

| Where | What it says | Correct |
|---|---|---|
| L04 S16, S23 | `group_by(...).sum().sort("sum_cost", …)` | `.sum()` keeps the name `cost`. On a frame that also holds a string column such as `date`, `group_by().sum()` raises `InvalidOperationError: sum operation not supported for dtype str`. Use `.agg(total_cost=pl.col("cost").sum())`. |
| L04 S18 (Polars) | `sort("admitted", descending=True).group_by("county").head(2)` | On the real data, 95 of the 101 rows are null. Add `nulls_last=True`. |
| L04 S18 (SQL) | `SELECT * FROM df GROUP BY county ORDER BY admitted DESC LIMIT 2` | DuckDB raises a `BinderException` (`school` must appear in `GROUP BY`), and even the intended query would return 2 rows in total. Use `QUALIFY ROW_NUMBER() OVER (PARTITION BY county ORDER BY admitted DESC) <= 2`. |
| L04 S27 (LLM) | `rank() / pl.count()` | `pl.count()` has been deprecated since 0.20.5 and counts every row, so the maximum percentile is 0.954. Use `pl.col(c).count()`. |
| L04 S33–S41 (image41) | Abraham Lincoln (SF), raw 0.368 → `0-25` | The code gives `25-50`. Regenerate the table; do not transcribe it. |
| L04 S37 | `grade_12 = pl.col('grade_12').sum,` | `.sum()` |
| L04 S44 titles | "admitted=NaN" | Polars values are `null`; write "null". |
| `lec04` c4 | `app_rate < 1` | EDA I uses `<= 1`. No school has a rate of exactly 1, so both keep 1,229 rows. Use `<= 1` for continuity. |
| `lec04` c17/c21/c25/c29 | Group without filtering null `frl_percentile` | A fifth, null group is computed and then silently hidden by `order=`. Filter once into `binned`. |
| `lec04` c28 | `polars_random` plugin | `np.random.default_rng(7342)` plus `pl.Series`. Its numbers differ slightly from the slide's (0.1520 vs 0.1518 at `50-75`). |
| `lec04` c13, c18, … | `Categorical` into `sns.pointplot` | In `d100` (pyarrow 18) this raises (verified: a `RuntimeError` from the interchange path). `.cast(pl.String)` at creation fixes it. |

### Open questions for course staff

1. **Frame name.** The slides say `admissions`, `lec04` says `uce`, S37 says `df`, and EDA I says `hs_enroll`.
   This outline proposes `admissions` so the Polars name and the SQL table name match. The overlap critic
   should settle one name across EDA I–IV. **Resolved (critic):** `admissions` in EDA I–V.
2. **Triple order.** English → live Polars → SQL, with no duplicated Polars block. EDA I's draft currently
   prints code, English, a duplicate Polars block, then SQL. The two chapters should agree. **Resolved (critic):**
   EDA I's outline uses the same order (its §6).
3. **Window-function SQL for per-group top-k** (§4, §6). Options: show the correct `QUALIFY` query, marked as
   beyond scope (proposed), or say "no simple SQL equivalent". The slide query cannot be kept either way.
4. **The "ignore lands outside the possible range" beat** (§14). It follows from the data and a one-line
   argument, and it sharpens S44's "somewhat sensitive" into a claim the reader can check. But it is analysis
   the lecture did not do. Include it, or stop at "the direction holds and the size does not"?
5. **The mean-of-rates column** (§10). It is not on the slides, and it turns S35's argument into visible
   numbers. Keep it?
6. **One shared-y 2×2 figure** instead of the lecture's four separately autoscaled plots (§14).
7. **The toy table.** S16 (with a customer C) and S21 (with dates) use different rows. This outline proposes
   S21's six rows for S16, S21 and S23, so §3's answer is A 130, B 90 rather than S16's C 100, B 90, A 30.
8. **Carry-forward to EDA IV.** EDA IV (L05 S8) reuses random imputation for `attended`. It should reuse this
   chapter's seed and `pl.when` code, or recompute it, so the two chapters' numbers agree. **Resolved (critic):**
   this chapter owns seed 7342 and the draw over `binned`. EDA IV §1 copies the cell verbatim. Its outline had drawn
   over all 1,229 rows, which gives 0.130/0.151 instead of 0.129/0.152. EDA IV §3 uses a fresh
   `default_rng(7342)` for `attended`.
9. **Dependency on EDA II.** EDA II shows the FRL pointplot (L03 S42) before any grouping code exists. If it
   renders that plot from code, the cell should be `remove-input` with a forward pointer, so that EDA III is
   the first place the `qcut` and `group_by` code is read. The critic should check. **Resolved (critic):** EDA II
   keeps plot B in a `Click to see the code` dropdown and adds one sentence naming `qcut`, `group_by().agg()` and
   `.cast(pl.String)`. This chapter is still where that code is built and explained.
10. **The `value_counts` bridge** in §2 assumes EDA I carries L02 S58 (`df["city"].value_counts()`). The EDA I
    draft on `main` does not yet include it. **Resolved (critic):** EDA I's outline adds it (§21,
    `value_counts(sort=True).head(5)`).
11. **Reference sheet** (from fa26-course-conventions): `pl.len()`, `group_by().len()`, `qcut` and `rank` are
    missing from `reference/build_polars_section.py`, and this chapter teaches all four.
12. **Where `is_not_null` is first explained.** Proposal: EDA I's fix pass adds one sentence where it first uses
    `is_not_null` (c59), and EDA III teaches nulls properly (`null_count`, `is_null`, `fill_null`,
    `pl.when`). **Resolved (critic):** EDA I's outline does this in its §14.

---

## `new_eda_4` — EDA IV: Finishing the Case Study

**Status: approved**

Source: L05 S4–S19, and `fa26-dev/lec/lec05/lec05.ipynb` c3–c28. There is no baseline chapter, so the disposition table maps slides. The lecture starts exactly where EDA III stops (L04 S45: "admission rates have a different pattern… we'll investigate next time"). It follows students from admission to attendance, brings in distance as a third variable, and ends with the decisions an analyst has to make to answer the manager. The chapter needs little new Polars. Most of its space goes to reading outputs and stating choices.

All numbers below were produced under polars 1.43.1 / duckdb 1.3.0 / seaborn 0.13.2 in the `d100` env. They are claims for the build pass to re-check against executed output, not text to paste.

| Slides | Disposition |
|---|---|
| S4 Admission rates have a different pattern | **Kept** as a short recap. Both plots regenerated from code as one two-panel figure; the code that rebuilds EDA III's state goes in a dropdown. |
| S5 Slido: what could reverse the pattern? | **Deleted** as a poll. Its question opens §2. |
| S6 Selection effects / UC admissions policy | **Rewritten** as prose: two hypotheses, stated as hypotheses. |
| S7 Slido: attendance rates per `frl_percentile`, handling nulls | **Deleted** as a poll. Its question opens §3. |
| S8 Missing Data: Redux | **Rewritten.** The pandas table screenshot (`image14`, with `NaN` and a row index) is replaced by a live Polars table. The imputation rule is kept and justified from the data. The stability check the slide defers ("Probably! For the sake of lecture time…") is done in §4, in one `group_by`. |
| S9 Yield rates have a different pattern | **Kept**, plot regenerated. The two hypotheses (cost; Berkeley compensating in admissions) are kept as hypotheses. |
| S10 Bringing in an additional variable (3D plot) | **Kept**: distance quartiles, the two-key `group_by`, `px.scatter_3d`, and the list of other encoding channels. |
| S11 Adding a new variable with color | **Kept**, `hue=` pointplot regenerated. |
| S12 Slido: describe the patterns | **Deleted** as a poll, folded into the reading of the S11 plot. |
| S13 Anything unexpected? Central Valley hypothesis | **Kept and extended.** The hypothesis is checked with `group_by("county").len()` (from EDA III). The distance histogram (`image24`) is regenerated from code, not pasted. |
| S14 Slido: rows and columns behind the plot | **Deleted** as a poll. The question is kept in §7. |
| S15 Tidy Data: Redux | **Kept**: 16 points → 16 rows, 3 variables → 3 columns, shown with `.select()` on the live table. |
| S16 Returning to our original question: what we learned | **Kept** as prose, with each claim tied to an output above it. |
| S17 Decisions about the pool | **Kept** as prose. |
| S18 One way to approach the problem | **Rewritten** so the code implements the slide's stated decisions. The lecture code filters `tot_enrolled >= 100`; the slide says "at least 100 12th graders". See Departures. |
| S19 Do any schools stand out? | **Kept.** The faceted scatter is regenerated with `sns.relplot`, followed by a reading of the plot and possibly one rule-based table (open question 7). |
| S1–S3 · S20–S60 | **Out of scope.** Deck chrome (Slido join, title, HW reminder), and EDA V. |

**Proposed shape**

1. **Where we left off** (S4). The setup cell (`remove-cell`) is EDA III's, plus `import plotly.express as px`. Rebuild EDA III's state in one `Click to see the code` dropdown and its `remove-input` twin: `pl.read_csv`, `app_rate`, `filter(pl.col("app_rate") <= 1)` (1,229 schools, as in EDA I–III), `frl_percentile`, and EDA III §13's random-imputation cell copied verbatim: `np.random.default_rng(7342)`, one draw of `binned.height` = 1,173 values over the bucketed schools. Keep the imputed frame under its own name, so `admissions` still has its null `admitted` for §3. Then one two-panel figure (`plt.subplots(1, 2)` + `ax=`). Application rate falls across FRL buckets (0.256 → 0.117 → 0.087 → 0.094) while admission rate rises (0.123 → 0.129 → 0.152 → 0.149, identical to EDA III §15). *Critic (checked in `d100`):* the draft's 0.130/0.151 come from drawing over all 1,229 rows, which is not EDA III's cell. *Concept:* two steps of the same pipeline can move in opposite directions across the same groups, so "high-FRL schools do worse" is not a single claim.

2. **Why might admission rates rise?** (S5–S6). Prose only. *Selection effects:* where few students apply, the ones who still do may be the strongest, so a school's applicant pool is not a random sample of its 12th graders. *Admissions policy:* UC weighs where a student comes from. Open question 8 covers how to word this. *Concept:* a rate depends on who is in its denominator, and that group is itself the result of someone's decision. A candidate for a `::: {note}` aside.

3. **Attendance rates and missing data, again** (S7–S8). Define the attendance (yield) rate as `attended / admitted`. Show `admissions.select("school", "city", "applied", "admitted", "attended").head(5)`. Its first two rows show both null patterns: A B Miller has 3 admitted and a null `attended`, and Able Charter has both null. That is what the slide's screenshot showed. Then two facts from the data justify the slide's rule:
   - A null means 0, 1 or 2. EDA III §12 showed this for `admitted`, so one cell here checks only `attended`: `admissions["attended"].min()` is 3, so counts below 3 are suppressed (*critic:* the `admitted` half is not repeated).
   - `attended` is never known when `admitted` is null: `admissions.filter(pl.col("admitted").is_null(), pl.col("attended").is_not_null())` has 0 rows. This is the chapter's first multi-predicate `filter`.

   So "ignore rows with `admitted` and `attended` both null" is the same as dropping the 418 schools with no admit count. Of the 811 left, 322 have a null `attended`, and each gets a random 0, 1 or 2 via EDA III's `pl.when(...).then(...).otherwise(...)` with a fresh `np.random.default_rng(7342)`, EDA III's seed. Imputing up to 2 never exceeds `admitted`, which is at least 3. English → Polars → SQL. *Concept:* the imputation rule follows from how the data were suppressed; it is not picked for convenience.

4. **Yield rates fall with FRL. Does that survive?** (S9, plus S8's deferred check). `group_by("frl_percentile").agg(attendance_rate=pl.col("attended").sum() / pl.col("admitted").sum())`, sorted, then `sns.pointplot`. Keep the slide's hypotheses: attending is expensive, and Berkeley may admit more students from high-FRL schools because it expects lower yield there. Then the stability check that EDA III's PCS section motivates: one `agg` with `fill_0`, `random`, `fill_2` and `share_null` columns, where `fill_0` is `pl.col("attended").fill_null(0).sum() / pl.col("admitted").sum()` and `fill_2` fills with 2. The readings to write against the output:
   - The share of schools with a suppressed `attended` climbs from 18% (0–25) to 57% (75–100). The choice matters most in the buckets being compared.
   - Filling with 0 and filling with 2 bracket the true rate. The 0–25 lower bound (0.555) sits above the 75–100 upper bound (0.525), so the decline holds whatever the suppressed counts really are, even though its size does not.

   *Concept:* before picking one imputation, bound the missing values with their extremes to see which conclusions are stable.

5. **Bringing in a third variable: distance** (S10). Build `dist_percentile` with `pl.col("dist_to_ucb_miles").qcut(4, labels=[...])`, cast to `pl.String`. Then `group_by("frl_percentile", "dist_percentile").agg(applied=…, grade_12=…, app_rate=…)`, sorted on both keys, which gives 16 rows. In SQL, `NTILE(4) OVER (ORDER BY dist_to_ucb_miles)` matches `qcut` on all 1,229 rows, followed by a two-column `GROUP BY`. Then `px.scatter_3d(..., category_orders=...)` and the slide's question: how readable is this? *Concept:* the data has three dimensions but the page has two. Color, size, shape and line type are further channels.

6. **Adding a variable with color** (S11–S13). `sns.pointplot(two, x="frl_percentile", y="app_rate", hue="dist_percentile", order=…, hue_order=…)`. Read it precisely. The nearest quartile has the highest rate in three of four FRL buckets; in 25–50 FRL, the 50–75 distance quartile edges it out, 0.159 to 0.158. The 25–50 distance line is lowest in three of four FRL buckets, far below the rest at low FRL (0.137 vs 0.223–0.332). Then check S13's hypothesis: `group_by("county").len()` within the 25–50 distance quartile (67.6–316.7 miles) puts Fresno, Kern, Sacramento, Tulare and Stanislaus on top, which is the Central Valley. The 50–75 quartile (317–363 miles) is 294 of its 307 schools in Los Angeles County. Optionally regenerate the distance histogram with the three cutoffs drawn in (`plt.axvline`), and refer back to EDA I's three population peaks in a sentence. *Concept:* here a distance quantile is really a region, and the reading has to say which region.

7. **Tidy data, redux** (S14–S15). How many rows and columns does the S11 plot need? 16 points → 16 rows. 3 encoded variables → 3 columns. Show `.select("frl_percentile", "dist_percentile", "app_rate")` on the §5 table. *Concept:* every channel in the seaborn call (`x`, `y`, `hue`) is a column, and every plotted point is a row.

8. **Returning to our original question** (S16–S17). Prose. First, what we learned: high-FRL schools apply less, are admitted more and attend less; farther schools apply less, with the Los Angeles quartile an exception; Central Valley schools apply least despite being closer than LA or San Diego. Second, what we did not explore: distance vs. admission and attendance, charters, school size, UCLA. Third, the decisions the task forces: small schools, charters, which step to target, geography, imputed rows. *Concept:* an open-ended task ends when you make and state decisions, not when the data runs out.

9. **One way to pick five schools** (S18–S19). The slide's choices in code: `filter(pl.col("grade_12") >= 100, pl.col("is_charter") == "N", pl.col("pct_free_reduced").is_not_null())` leaves 883 schools. Then `qcut(5, labels=[...])` on distance, cast to `pl.String`, gives 177/176/177/176/177 schools per quintile. English → Polars → SQL. Then `sns.relplot(pool, x="pct_free_reduced", y="app_rate", size="grade_12", col="dist_bucket", col_wrap=3, col_order=[...])`. For "Do any schools stand out?", read the panels: the schools that defy the pattern sit well above the downward trend for their FRL level. Possibly one table here (open question 7). *Concept:* the answer is a product of stated choices, and another analyst's choices could yield a different five.

10. **Parting note.** Two or three sentences on what we checked and what we did not (PCS), then a one-line pointer to EDA V stepping back to structure and granularity. No EDA V content.

**Learning Outcomes**

```
::: {note} Learning Outcomes
* Compute group-wise attendance rates from suppressed counts, and test the conclusion by bounding the nulls with `fill_null`
* Keep rows that meet several conditions at once with a multi-predicate `.filter()`
* Group on two variables with `.group_by()` and read the result as one row per plotted point
* Encode a third variable with `hue=` in `sns.pointplot`, and explain what `px.scatter_3d` hides
* Compare groups in small multiples with `sns.relplot(col=...)`
* State the decisions that turn an open-ended question into an answer
:::
```

Opener: "In this chapter, we will finish the UC Berkeley admissions case study. We will follow admitted students to attendance, bring distance in as a third variable, and make the decisions we need to hand our manager five schools."

**Polars introduced here for the first time.** One or two sentences each, where first used:

- `.filter()` with several comma-separated predicates, all of which must hold (§3, again in §9).
- Equality on a string column. It first appears in §6, where the county check keeps one distance quartile (`pl.col("dist_percentile") == "25-50"`), and again as `pl.col("is_charter") == "N"` in §9 (*critic:* §6 comes first).
- An expression transformed *inside* an aggregation, with several named results from one column in one `agg` (`pl.col("attended").fill_null(0).sum()`, §4). This is composition rather than a new verb, but readers have not seen it yet.
- Plotting, also new: `hue=`/`hue_order=` on `sns.pointplot`; `px.scatter_3d` with `category_orders`; `sns.relplot` with `col=`, `col_wrap=`, `col_order=` and a shared `size=`; `plt.axvline` if §6 keeps the cutoffs.

**Assumed from earlier chapters.** Check each against their `.py` and do not re-introduce. From EDA I: `pl.read_csv`, `with_columns`, `pl.col`, single-predicate `filter`, `sort(descending=)`, `sort(..., nulls_last=True)`, `select`, `head`, `.height`, Series `.min()`, and `plt.subplots(1, 2)` + `ax=` (§18's folded cell). From EDA II: `sns.scatterplot(size=)`, `.cast`. From EDA III: `group_by().agg()`, `group_by().len()`, `pl.len()`, `rank()/count()`, `qcut(labels=)`, `is_null`/`is_not_null`, `fill_null`, `pl.when().then().otherwise()`, seeded `np.random.default_rng` + `pl.Series`, `sns.pointplot(order=)`, `sort(...).group_by(...).head(n)`, `.sort()` on several keys, `.null_count()`. EDA III's outline keeps `pl.when` and the seeded imputation (its §13), so neither is re-introduced here (*critic*).

**Used by the lecture, deliberately not introduced:**

- `pl.Enum`: c27 uses it to order the facets. In `d100` (pyarrow 18), Enum and Categorical columns passed to seaborn raise (reproduced), and `col_order=` does the same job.
- `polars_random`: not in `requirements.txt`.
- `polars.selectors`: imported in c0, never used.
- `sns.FacetGrid.map_dataframe`: see Departures 3.

**Departures from the lecture code**

1. `tot_enrolled >= 100` becomes `grade_12 >= 100`, the decision S18 actually states. The lecture's filter keeps 1,226 of 1,229 schools, so it filters almost nothing: its pool is 995 schools against 902 under the slide's rule, before nulls are dropped. The lecture's first panel shows small high-FRL outliers (FRL ≈ 0.93, `app_rate` ≈ 0.5). They are schools with fewer than 100 12th graders, and they disappear under the slide's rule.
2. Null `pct_free_reduced` rows are dropped *before* `qcut(5)`, so each panel holds a fifth of the plotted schools (177/176/177/176/177). Binning first, as the lecture does, gives 184–195. The lecture's `.filter(pl.col('app_rate').is_not_null())` goes: the `<= 1` filter has already dropped null rates, so it does nothing.
3. `FacetGrid.map_dataframe(sns.scatterplot, size=...)` becomes `sns.relplot`. `map_dataframe` normalizes `size` separately in each panel, so the lecture's legend merges two scales (150…900 and 200…1000), and one dot size means different school sizes in different panels. `relplot` uses one scale (200…1000). Both reproduced in `d100`.
4. `polars_random` becomes `np.random.default_rng(7342)` (EDA III's seed) + `pl.Series`. Imputed rates will differ from the slide images in the second or third decimal. For example, the 75–100 attendance rate ranges 0.405–0.437 across six seeds, against the slide's 0.427. Prose quotes executed output only.
5. `qcut` labels are cast with `.cast(pl.String)` before any seaborn call. Order comes from `order=`/`hue_order=`/`col_order=`.
6. The 16-row table is sorted on both keys. The lecture sorts on `frl_percentile` only, so the within-bucket order in its output is arbitrary, because `group_by` order is not stable.
7. `dist_percentile` uses `qcut` directly on miles instead of rank-then-`qcut`. The bins are identical on all 1,229 rows. The lecture itself uses the direct form for the quintiles (open question 6).
8. Names follow the data, not the slide text. S18 says `dist_from_ucb` and `free_reduced_percentage`, and `image58` titles its panels "1st dist_to_ucb quintile". The chapter uses `dist_to_ucb_miles`, `pct_free_reduced`, and the code's labels ("1st distance quintile").
9. Every plotting cell gets a `#| fig-alt:` line and a trailing `;`.

**SQL for the triples**

- `FROM admissions` means the chapter's working frame at that point, as in EDA I. The claim verifier has to register it, or the derived columns (`frl_percentile`, `dist_percentile`) do not exist.
- Random imputation, `COALESCE(attended, FLOOR(RANDOM() * 3))`, uses DuckDB's RNG, not NumPy's, so it can only match in shape. The verifier should compare the deterministic bounds `COALESCE(attended, 0)` and `COALESCE(attended, 2)`. These match Polars exactly: 0.5547/0.4482/0.3758/0.3300 and 0.5774/0.5458/0.5346/0.5251.
- Quartiles: `NTILE(4)` matches `qcut` on 1,229/1,229 rows. Quintiles on the 883-school pool: `NTILE(5)` disagrees on 3 schools, and cut points from `quantile_cont(dist_to_ucb_miles, [0.2, 0.4, 0.6, 0.8])` match 883/883. Proposal: show `NTILE`, with one sentence that it splits by row count while `qcut` splits at quantile values.
- The two-key `GROUP BY` with `SUM(applied) / SUM(grade_12)` reproduces the Polars table exactly. DuckDB's `/` on integer sums returns a float, where most other engines do integer division. It is worth a clause if the SQL chapter uses a different engine.

**Data**

- `content/new_eda_4/data/pivoted-ucb-data-w-everything.csv`, copied from fa26-dev `lec/lec04/data/pivoted-ucb-data-w-everything.csv` (md5 `4c9d424fbb7d930419c18cb11d5517b1`, byte-identical to `main:content/new_eda_1/data/`'s copy). It is already in place. No other file: lec05 has no `data/` folder of its own, and lec06's `"NA"` copy is EDA V's faithfulness demo.

**Images.** None from the manifest.

- `image11`, `image23`, `image48`, `image30`, `image20`, `image24` and `image58` are plots and are regenerated.
- `image14` is a pandas table screenshot; §3 replaces it with live output.
- `image9` is Slido chrome.
- The California population-density map belongs to EDA I (L02 S57–58). §6 refers back to it in a sentence rather than copying it.

**Open questions**

1. **The EDA III/IV boundary inside `lec04.ipynb`.** Cells c31–c43 (distance percentile, 3D plot, `hue` plot, "Final recommendation") duplicate lec05 c16–c28 and have no L04 slide. They belong to this chapter. `new_eda_3` should stop at L04 S45's two plots. Please have the overlap critic enforce this. **Resolved (critic):** EDA III's outline already stops at L04 S45 and leaves c31–c43 to this chapter.
2. **Shared state with EDA III.** §1 must reproduce EDA III's last figure exactly, so it needs EDA III's imputation cell verbatim: the same seed, the same draw length, the same `frl_percentile` construction, and the same `app_rate < 1` filter. `main`'s EDA I draft uses `<= 1`, but no school has a rate of exactly 1, so both give the same 1,229 rows. Which chapter owns the seed? **Resolved (critic):** EDA III owns seed 7342 and the draw over `binned`. This chapter uses `<= 1`, copies EDA III's cell verbatim in §1, and reuses 7342 in §3.
3. **The deferred stability check (§4).** The lecture skips it. Recommend including it: it is cheap, it applies EDA III's PCS idea, and the obvious alternative quietly erases the S9 finding. Dropping the schools with a null `attended` gives 0.584/0.577/0.582/0.562, nearly flat, because it drops exactly the low-yield, mostly high-FRL schools. Should that fourth column go in and be explained as a selection effect (tying back to §2), or stay out?
4. **The S18 filter.** Follow the slide (`grade_12 >= 100`), as proposed, or the lecture code? The choice changes the pool and which schools stand out.
5. **§6 extensions.** The county check and the histogram with cutoffs are not on the slides; they test the hypothesis S13 states. Keep both, one, or neither?
6. **Direct `qcut` for `dist_percentile`.** The lecture uses rank-then-`qcut` for the quartiles and direct `qcut` for the quintiles in the same notebook. Proposal: the direct form for both, plus one sentence that it gives the same bins as EDA III's two-step. Or keep the two-step for fidelity.
7. **Should the chapter name five schools?** The lecture ends at S19 on a question. One option is a table of the highest-`app_rate` school with `pct_free_reduced >= 0.5` in each quintile, built with EDA III's `sort(...).group_by(...).head(1)`. Today that gives Oakland Technical (Oakland, 0.42), Mira Loma (Sacramento, 0.24), Woodrow Wilson (Long Beach, 0.34), Compton Early College (Compton, 0.30) and Del Lago Academy (Escondido, 0.19). The highest application rates overall are low-FRL schools that follow the pattern rather than defy it (Monta Vista 0.76, Gretchen Whitney 0.73), and the prose could make that point. It is a staff call whether published notes name schools.
8. **Wording of the S6 policy point.** The slide says "Top K at high schools in California". UC's Eligibility in the Local Context guarantees top-ranked students a place somewhere in the UC system, not at Berkeley. Proposal: frame it as a hypothesis about local context, without claiming any guarantee. Please confirm.
9. **The 3D plotly figure on a static page.** It is committed as `application/vnd.plotly.v1+json`, so readers can rotate it, which weakens "how readable is this?". Keep plotly (the lecture's code) or render a static matplotlib 3D PNG? The A5 alt-text gate only sees `image/png`, so the `#| fig-alt` on this cell is convention, not enforcement. The render reviewer should confirm it displays.
10. **Terminology.** The slides alternate between "attendance rate", "yield rate" and "attend rates". Proposal: define yield once, and name the column `attendance_rate` to match the slide plot.

---

## `new_eda_5` — EDA V: Key Data Properties, Joins, and Databases

**Status: approved**

Source: L05 S20–S60 and L06 S39–S51. From L06 S4–S38 the chapter takes only S20's Polars join line, because the rest repeats L05. `fa26-dev/lec/lec06/lec06.ipynb` supplies data only: its `data/example_duck.db` holds the `dragon` and `setting` tables that L06 S44–S50 draw. The notebook's jupysql setup, `information_schema` cells and `SELECT`/`WHERE`/`ORDER BY`/`LIMIT` material belong to `sql_I` and are not used here. There is no baseline chapter, so the disposition table maps slides.

The chapter leaves the admissions case study behind and teaches the checklist both decks organise EDA around: **structure, granularity, temporality, faithfulness**. Under structure it covers file formats, variable types and data spread across several tables, which is where joins come in. L06 then asks where those tables come from and answers with databases, schemas, keys and the star schema. This chapter has the most new Polars of the five: file reading beyond a plain CSV, `.str`/`.dt`, and `.join()` are all new. It has **no plots**. Every in-scope slide figure is a diagram, a table or a map, so there are no `#| fig-alt` cells and the a11y review covers `{image}` alt text only.

All numbers below were produced under polars 1.43.1 / duckdb 1.3.0 in `d100`. The build pass should re-check them against executed output. They are not text to paste.

| Slides | Disposition |
|---|---|
| L05 S1–S19 | **Out of scope.** Chrome (S1–S3) and EDA IV (S4–S19). |
| L05 S20, S22, S27, S34, S37, S51, S55 · L06 S39 | Agenda slides (the four properties; S22/S37/S51 add Variable Type, Multiple Files and File Format under Structure). **Rewritten** into §1's overview and the section headings. Not repeated. |
| S21 Rectangular data: tables vs matrices | **Kept**, §2. |
| S23 Variable feature types | **Kept**, §4a. |
| S24 Variable types quiz (7 variables) | **Kept** as a table with the answers, §4b. The speaker-note point that context decides (GPA can go either way) is one sentence. The answer key needs confirming (OQ 4). |
| S25 Slido: what type is a ZIP code? | **Deleted** as a poll. Its question opens §4d. |
| S26 ZIP-prefix map | **Kept**: image plus a Polars demo of the lost leading zero, §4d. |
| S28 "data" singular or plural | **Kept** as a one-sentence `{note}`, §5. |
| S29 Granularity, fine vs coarse, rollups | **Kept**, §5. The fine/coarse row graphic is text-only in the extract, so it becomes prose. |
| S30, S32 Slido: granularity of `elections`, `babynames` | **Deleted** as polls. The questions stay in the prose. |
| S31 Granularity of `elections` (`image28`, a table screenshot) | **Kept, regenerated**: live `elections.head()` plus an `n_unique` check, §5. |
| S33 Granularity of `babynames` (`image31`) | **Kept as prose only** (OQ 3). |
| S35 Slido: what type is a datetime? | **Deleted** as a poll. The question opens §6. |
| S36 How should we store datetimes? Unix time | **Kept** with corrected numbers (Departure 2), §6. |
| S38 Multidimensional data (star schema) | **Moved** to §11 and merged with L06 S51, the same figure. |
| S39 "Cats" photos | **Deleted** (decorative photos). The table figure is used in §8. |
| S40–S41 Inner join | **Kept**, `inner_join_s_t.png`, §8b. |
| S42 JOIN syntax | **Kept**, merged with L06 S20's Polars line, §8b. |
| S43–S44 Cross join | **Kept**, `cross_join_s_t.png`, §8c. The result image (`image60`) is **not used**: it has a mislabelled row (Departure 5). The live 16-row output replaces it. |
| S45 Inner join = cross join + filter | **Kept**, in both Polars and SQL, §8d. `image49` is not used, because the live output shows the same 3 rows. |
| S46–S48 Left, right, full outer join | **Kept**, §8e–g. Results come from live output. The result images are not used (Departure 5, OQ 6). |
| S49 Slido: equivalent joins | **Deleted** as a poll, kept as a question, §8h. |
| S50 Equivalent joins answers | **Kept**, with Polars versions of B and C, §8h. |
| S52 CSV (CDC TB data) | **Kept**, §3a. pandas `header=` becomes `skip_rows=`. |
| S53 TSV | **Kept**, §3b. The "TaB soda" joke image (`image51`) is deleted. |
| S54 JSON (congress.gov members) | **Kept**, §3c. `pd.read_json`/`pd.DataFrame(json_dict)` become `pl.read_json`/`pl.DataFrame`. |
| S56 Faithfulness: key questions | **Kept**, §7a. |
| S57 Slido: issues with this dataset | **Deleted** as a poll. |
| S58 Toy purchases table | **Kept**: built in Polars, and each issue found with code, §7b. |
| S59 Duplicates, spelling errors, missing-value encodings | **Kept**, §7b–c, plus a real-data demo on lec06's `"NA"`-encoded admissions file. |
| S60 Missing data: approaches | **Kept**, short, pointing back to EDA III/IV's worked handling, §7d. |
| S61 Closing title | **Deleted.** |
| L06 S1–S3 | **Deleted.** Slido, title, announcements. |
| L06 S4–S19, S21–S38 | **Deleted as duplicates** of L05 S4–S60 (recap, variable types, granularity, datetimes, joins, formats, faithfulness). Their content is covered by the L05 rows above. |
| L06 S20 | **Kept, one line**: `table1.join(table2, on=key, how='inner')`, written `s.join(t, on="id", how="inner")`, §8b. |
| L06 S40 Databases, DBMS, product list (`image35`, logos) | **Kept** as prose. The logos are not used. §9. |
| L06 S41 Advantages of a DBMS over raw files | **Kept** as two short lists, §9. |
| L06 S42 Review: the EDA workflow (`image37`) | **Kept** as a callback to EDA I's workflow section (L02 S9). No image. §9. |
| L06 S43 How data scientists use SQL | **Kept**, §9. Use 1 is demonstrated with `pl.read_database`. |
| L06 S44 SQL terminology | **Kept**, §10a. The Corgi/T-Rex/Penguin table is deleted and the `dragon` table carries the terms. |
| L06 S45 Table schema, `CREATE TABLE dragon` | **Kept** as a ```sql block taken from the database's own statements, §10b. |
| L06 S46–S48 Why multiple tables? (redundancy, column bloat) | **Rewritten**: a join builds the wide table, and the redundancy is read off its output, §10c. |
| L06 S49–S50 `setting` table, primary and foreign keys | **Kept**, §10d, using the tables as stored in `example_duck.db`, not the slide's version (Departure 6). |
| L06 S51 Star schema | **Kept**, §11. |
| L06 S52 Closing title | **Deleted.** |

**Proposed shape**

0. **Frontmatter, Learning Outcomes, opener.** `title: EDA V`. The setup cell is `remove-cell` and holds `import polars as pl` only. `json`, `io` and `duckdb` are imported in the visible cell that first uses each, because using them is part of what that section teaches. Opener: "In this chapter, we will step back from the admissions case study and look at four properties every dataset has: its structure, granularity, temporality, and faithfulness. Along the way, we will read files that are not simple CSVs, combine tables with joins, and see why databases split data across many tables."

1. **Key data properties** (S20, S22 and the agenda repeats; L06 S39). One paragraph and a four-item list with the slide's one-line definitions. Structure: the shape of a data file. Granularity: how fine or coarse each datum is. Temporality: how the data is situated in time. Faithfulness: how well the data captures reality. Say that structure gets three parts here (file format, variable type, multiple tables). *Concept:* ask these four questions of any dataset, whatever the analysis question is.

2. **Structure: rectangular data** (S21). Records are rows, and fields are columns. Tables have named columns of different types and are manipulated with group by, join and filter. Matrices hold numbers of one type and are manipulated with linear algebra. Keep the slide's point that a big part of cleaning is reshaping data until it is rectangular (spam emails → a table of word counts). One live cell reads `admissions = pl.read_csv("data/pivoted-ucb-data-w-everything.csv")` and shows `admissions.schema`, which introduces **`.schema`**: 11 named columns in three types (4 `String`, 5 `Int64`, 2 `Float64`), so this is a table, not a matrix. English → Polars → SQL: "List each column's name and type" / `DESCRIBE admissions`. One sentence says that `.to_numpy()`, which EDA I §8 mentions in passing, produces the matrix form, which the modeling chapters use. *Concept:* a table is a set of named, typed columns, and that is what makes it flexible.

3. **Structure: file formats** (S52–S54). *Concept:* a file format is an agreement about where records and fields end, and when a file breaks the default you have to tell the reader what it does instead.
   a. **CSV** (S52). First, read it naively: `pl.read_csv("data/cdc_tuberculosis.csv")` gives columns `""`, `No. of TB cases`, `_duplicated_0`, `_duplicated_1`, and the real header ends up in row 0. The file has a title line above its header. Then `tb = pl.read_csv("data/cdc_tuberculosis.csv", skip_rows=1)` gives **52 × 4**. Point at `"8,900"`: a field that contains the delimiter has to be quoted. All four columns are `String`, which §4e fixes. English → Polars → SQL: `SELECT * FROM read_csv('data/cdc_tuberculosis.csv', skip = 1)`. Add a `{tip}` built on S54's "inspect the file before importing": look at the raw lines first, as EDA I's CSV note did.
   b. **TSV** (S53). `pl.read_csv("data/cdc_tuberculosis.tsv", separator="\t", skip_rows=1)`, then `.equals(tb)` gives `True`. It is the same table with a different delimiter, which introduces **`.equals()`**. SQL: `read_csv('data/cdc_tuberculosis.tsv', delim = '\t', skip = 1)`, checked equal to Polars.
   c. **JSON** (S54). `pl.read_json("data/ca-congress-members.json")` gives **1 row × 3 columns** (`members`, `pagination`, `request`). The file is a nested document, not a table. Then inspect it the way S54 advises: `import json`, `json.load`, `congress.keys()`. `pagination` is `{"count": 54}`, metadata stored in the same file as the records ("self-documenting"). Then `members = pl.DataFrame(congress["members"])` gives **54 × 9**, which introduces **`pl.DataFrame` from a list of records**. S54's two warnings, read off the output:
      - *Nested tables:* `depiction` and `terms` are `Struct` columns. `terms` holds a list of terms per member.
      - *Inconsistent fields:* 52 records have a `district` key and 2 have none. Polars fills those with `null`. `members.filter(pl.col("district").is_null()).select("name", "district")` shows Schiff and Padilla, the two senators.
      SQL: `SELECT UNNEST(members, max_depth := 2) FROM read_json('data/ca-congress-members.json')` gives 54 × 9 (DuckDB-specific). One sentence says that most databases never read files from SQL at all, because the DBMS stores the tables itself, and §9 picks this up. *Sub-concept:* JSON is a tree, and turning it into a table means choosing which level is a row.

4. **Structure: variable types** (S23–S26). *Concept:* a variable's feature type is about what it means, and its dtype is about how it is stored. They are separate choices, and a mismatch in either direction causes bugs.
   a. The taxonomy (S23): quantitative, and qualitative split into ordinal and nominal, with the slide's examples. "A safe default: store qualitative data as strings."
   b. The S24 quiz as a table: CO2 level, income bracket, race/ethnicity, political party, year, GPA, U.S. postal code, each with its answer. One sentence carries the speaker note: GPA can be quantitative or ordinal depending on the question.
   c. The admissions columns, classified against §2's schema. `school`, `city`, `county` and `is_charter` (`"Y"`/`"N"`) are nominal. The five counts are quantitative, and so are `pct_free_reduced` and `dist_to_ucb_miles`. EDA III/IV's `frl_percentile` labels (`"0-25"` … `"75-100"`) are ordinal values stored as strings. They sort correctly only because the labels were chosen so that alphabetical order matches.
   d. ZIP codes (S25–S26), with `us_zip_code_prefix_map.png`. ZIPs are identifiers with a geographic order, not quantities. `import io`, then `pl.read_csv(io.StringIO("city,zip\nCambridge,02138\nBerkeley,94720\n"))`: Polars infers `i64` and Cambridge becomes **2138**. Adding **`schema_overrides={"zip": pl.String}`** keeps `"02138"`. SQL: `SELECT CAST('02138' AS INTEGER)` gives 2138.
   e. The opposite problem: the TB counts arrived as text. `tb = tb.with_columns(pl.col("2019", "2020", "2021").str.replace_all(",", "").cast(pl.Int64))` gives `Int64`, with Total = 8900. This introduces **`pl.col` with several names**, the **`.str` namespace** and `.cast(pl.Int64)`. EDA II introduced `.cast(int)`. SQL: `CAST(REPLACE("2019", ',', '') AS INTEGER)`. Column names that are numbers need double quotes in SQL, and that is worth a clause.

5. **Granularity** (S27–S33). *Concept:* know what one row is before you count rows, and coarse data can't be split back into finer rows.
   - Definition (S29): what each record represents, fine vs coarse, and rollups as records. If the data are coarse, ask how the records were aggregated. A `{note}` covers S28: "the data shows" and "the data show" are both fine.
   - `elections` (S30–S31): `elections = pl.read_csv("data/elections.csv")`, `.head()`. `elections["Year"].n_unique()` is **51** and `elections["Candidate"].n_unique()` is **135**, but `elections.select("Year", "Candidate").n_unique()` is **187**, which equals `elections.height`. Each row is one candidate in one election year. Keep the slide's assumptions: one election per year, and one party per candidate per election. Series `.n_unique()` comes from EDA III §2. Calling `.n_unique()` on a two-column `select` is new here, and it counts distinct *rows* (*critic*). English → Polars → SQL: `SELECT COUNT(*) FROM (SELECT DISTINCT Year, Candidate FROM elections)` gives 187.
   - `babynames` (S32–S33): prose only. Each row is a unique name, state, sex and year, and each count is itself a rollup of individual births (OQ 3).
   - `admissions`: `admissions["school"].n_unique()` is **1201** against **1268** rows, and `admissions.select("school", "city").n_unique()` is **1268**. A row is one school, identified by name *and* city. This connects to EDA I's repeated "Abraham Lincoln High School" and prepares §10's keys. Each row is also a rollup of individual students' decisions, which is why counts below 3 were suppressed (EDA I, EDA IV).
   - TB's `Total` row, S29's "summaries as records" made concrete: `tb.filter(pl.col("U.S. jurisdiction") != "Total").select(pl.col("2019", "2020", "2021").sum())` gives **8900 / 7173 / 7860**, exactly the Total row. Summing the whole column would count every case twice. SQL: `SELECT SUM("2019"), SUM("2020"), SUM("2021") FROM tb WHERE "U.S. jurisdiction" <> 'Total'`.

6. **Temporality** (S34–S36). *Concept:* store time as a number counted from an agreed origin, so that "before", "after" and "how long between" become arithmetic. A time without a time zone is ambiguous.
   - `times = pl.DataFrame({"when": ["02/04/2025 5:00pm", "01/01/2025 3:30pm", "02/04/1950 5:00pm"]})`, built from a dict of columns as in EDA III §3. `times.sort("when")` puts 1950 *between* the two 2025 dates, and that is S36's "difficult to make comparisons".
   - Parse with **`.str.to_datetime("%m/%d/%Y %I:%M%p")`** to get `datetime[μs]`. The sort becomes chronological, and `pl.col("parsed").max() - pl.col("parsed").min()` gives a `duration` of **27394 days**.
   - Unix time: **`.dt.replace_time_zone("America/Los_Angeles").dt.epoch("s")`** gives **1738717200**, **-628124400** and **1735774200**. The 1950 value is negative because it falls before 1970. The chapter prints these values, not the slide's (Departure 2).
   - SQL: `SELECT epoch(timezone('America/Los_Angeles', strptime('02/04/2025 5:00pm', '%m/%d/%Y %I:%M%p')))` gives 1738717200.0 (checked). DuckDB returns a `DOUBLE` where Polars returns `i64`.

7. **Faithfulness** (S55–S60). *Concept:* ask whether the data reflects reality, look for how it can fail to, and decode missing values before you decide how to handle them.
   a. S56's key questions as a short list: collection bias, who is missing, whether someone else would have collected it differently, why it is sliced the way it is, and what limited the collection.
   b. The S58 toy table. `purchases` (9 rows: ID, Category, State, Location, Device, Purchased) is built with `pl.DataFrame` in a `Click to see the code` dropdown with its `remove-input` twin, since the construction is not the lesson. Then one short live cell per S59 category:
      - *Duplicated records:* `purchases.filter(purchases.is_duplicated())` shows the two identical ID-4 rows, and `purchases.unique().height` is 8. This introduces **`.is_duplicated()`** and **`.unique()`**. SQL: `SELECT *, COUNT(*) AS n FROM purchases GROUP BY ALL HAVING COUNT(*) > 1`.
      - *Duplicated or uninformative fields:* `State` equals `Location` in all 9 rows, and `Device` has one distinct value. This is optional, one `select`.
      - *Labelling and spelling errors:* `purchases["Category"].value_counts(sort=True)` shows `"Pnts"`, and `"XY"` is not a state.
      - *Sentinels and missing values:* `purchases["Purchased"].value_counts(sort=True)` gives 0 ×5, 1 ×2, `null` ×1 and **-1** ×1. A 0/1 column holding -1 is S59's "0, -1999, 12345" row. Both value counts contain **ties**, so the prose must not depend on tie order. If it has to, sort on count and then on value.
   c. **How missing values are encoded** (S59). The slide's list becomes a table: `" "`, 0/-1999/12345, `NaN`, `null`, and default dates such as 1970 and 2000. A `{note}`: Polars keeps `NaN` (a float value, e.g. 0/0) apart from `null` (missing). `pl.Series([1.0, float("nan"), None]).is_null()` gives `[false, false, true]`, and `.is_nan()` finds the other one. Then the real-data demo: `admissions_na = pl.read_csv("data/pivoted-ucb-data-w-everything-na-strings.csv")`.
      - Its `.schema` shows **six** numeric columns arriving as `String` (`admitted`, `attended`, `tot_enrolled`, `grade_12`, `pct_free_reduced`, `dist_to_ucb_miles`). Only `applied`, which has no missing values, stays `Int64`. The column type is the first clue.
      - `admissions_na["is_charter"].value_counts(sort=True)` gives N 1002, Y 231 and **"NA" 35**. Missingness now looks like a third category. For `admitted`, the most common "value" is `"NA"` (445).
      - The fix is **`null_values="NA"`**: `pl.read_csv(..., null_values="NA").equals(admissions)` gives `True`. `.null_count()` then gives admitted 445, attended 776, pct_free_reduced 94, and 35 each for tot_enrolled, grade_12, is_charter and dist_to_ucb_miles. SQL: `SELECT * FROM read_csv('data/pivoted-ucb-data-w-everything-na-strings.csv', nullstr = 'NA')`, which gives the same types (checked with `DESCRIBE`).
   d. **Approaches** (S60), in prose. (A) Keep as null, a good default, and for a qualitative column consider a `"Missing"` category. (B) Drop records, typically a bad default: a probe offline for a minute is probably missing at random, and an officer who never records stop outcomes is not. (C) Impute or interpolate: mean/median, hot deck, regression, and multiple imputation, which is beyond the course. One paragraph points back: EDA III/IV imputed the suppressed counts with a seeded random 0–2 and then bounded the result with 0 and 2. That was option C followed by a sensitivity check. No new code.

8. **Structure again: data in several tables, and joins** (S37, S39–S50; L06 S20). *Concept:* a join pairs rows from two tables by a key, and `how=` decides what happens to rows that have no partner. Open by saying that the admissions table readers have used since EDA I was already built by joining several sources, and this section shows how.
   a. Build `s` (ids 0, 1, 2, 4: Apricot, Boots, Cally, Eugene) and `t` (ids 1, 2, 4, 5: persian, ragdoll, bengal, persian) live with `pl.DataFrame({...})`. Show `join_input_tables_s_t.png`.
   b. **Inner** (S40–S42, L06 S20), `inner_join_s_t.png`. `s.join(t, on="id", how="inner")` gives **3 rows** (Boots, Cally, Eugene) and **one** `id` column, because the two ids are equal on every row it keeps. The figure and SQL's `SELECT *` keep both, and DuckDB names the second one `id_1`. Map S42's anatomy onto the call: the kind of join is `how=`, and the matching columns are `on=`. `"inner"` is the default. English → Polars → SQL. Link the `DataFrame.join` docs and the user-guide joins page on `docs.pola.rs`.
   c. **Cross** (S43–S44), `cross_join_s_t.png`. `s.join(t, how="cross")` gives **16 = 4 × 4** rows. It takes no `on=`. Both ids are kept, and the second is named **`id_right`**: Polars adds the suffix `_right` to any right-hand column name that already exists. SQL: `SELECT * FROM s CROSS JOIN t`.
   d. **Inner join as a filtered cross join** (S45). `s.join(t, how="cross").filter(pl.col("id") == pl.col("id_right"))` gives the same 3 rows (checked: after `.drop("id_right")`, `.equals` the inner join). Both SQL forms go in the triple. One sentence: this is a way to think about an inner join, not how an engine computes one.
   e. **Left** (S46). `how="left"` gives 4 rows, and Apricot's `breed` is `null`. That null means "no match", a different kind of missing from §7's, and worth a sentence. SQL `LEFT JOIN`.
   f. **Right** (S47). `how="right"` gives 4 rows, and id 5's `name` is `null`. The output's column order is `name, id, breed`, and the prose reads it from the output. SQL `RIGHT JOIN`.
   g. **Full outer** (S48). `how="full"` gives 5 rows with **both** `id` and `id_right`, because each of them is null on one unmatched row. `coalesce=True` merges them into one complete `id` (5 × 3). SQL `FULL JOIN`.
   h. **Equivalent joins** (S49–S50). The question: which queries return the same information as `s LEFT JOIN t`? Answers A, B and C all do. In Polars, B is `t.join(s, on="id", how="right")` (the same 4 rows, columns `breed, id, name`). C is `s.join(t, on="id", how="full").filter(pl.col("id").is_not_null())` (the same 4 rows plus `id_right`). A has no Polars counterpart, because `on=` names the key only once.
   Join row order is not guaranteed. It was identical across 300 runs of these tables, but the prose should name rows by id or name, not position. If a full join is ever sorted on `id`, use `nulls_last=True`.

9. **Databases: why SQL?** (L06 S39–S43). *Concept:* the database is the durable, shared, constrained source of the data, and a Polars frame is a snapshot of one query's result.
   - A database is an organised collection of data. A DBMS stores it, manages it and gives access to it. Name the S40 examples (BigQuery, Redshift, Snowflake, Databricks, SQL Server).
   - S41's advantages as two short lists. Storage: survives crashes, computes on data larger than memory, uses special structures. Management: controls access, enforces guarantees such as a non-negative age, and makes concurrent reads and writes safe (the ATM example).
   - S42: point back to EDA I's EDA workflow (dynamic tables → a snapshot → Polars → seaborn). This section explains its first box.
   - S43: the four ways data scientists use SQL, as a list.
   - Live, and demonstrating use 1: `import duckdb`, `con = duckdb.connect("data/example_duck.db", read_only=True)`, `dragon = pl.read_database("SELECT * FROM dragon", con)` and the same for `setting`. This introduces **`pl.read_database`**. One sentence says that `read_only=True` means reading can never change the file, and that the SQL chapters cover writing queries.

10. **Tables, schemas and keys** (L06 S44–S50). *Concept:* a primary key identifies a row. A foreign key holds another table's primary keys, and it is what you join on. Splitting data into keyed tables stores each fact once.
    a. Terminology (S44): relation/table, row/record/tuple, column/attribute/field, shown on `dragon` (6 × 4).
    b. Schema (S44–S45). Each column has a name, a type, and zero or more constraints. `dragon.schema` shows names and types (`String`, `Int32`) and no constraints, which is S44's own contrast with Polars. Then a ```sql block holding the two statements the database was built with, `setting` first. Both are taken from `duckdb_tables()`: `CREATE TABLE setting(id INTEGER PRIMARY KEY, media VARCHAR NOT NULL, place VARCHAR, "type" VARCHAR, start_year INTEGER, CHECK((start_year >= 1900)));` and `CREATE TABLE dragon("name" VARCHAR PRIMARY KEY, yr INTEGER, cute INTEGER, setting_id INTEGER, CHECK((yr >= 1900)), FOREIGN KEY (setting_id) REFERENCES setting(id));`. Say what each constraint does.
    c. Why multiple tables (S46–S48). The English: "For each dragon, attach its setting." `dragon.join(setting, left_on="setting_id", right_on="id")` gives **6 × 8**. This introduces **`left_on=`/`right_on=`** for keys with different names. Polars keeps only `setting_id`, while the SQL result has 9 columns. Read S48's two problems off the output: drogon and rhaegal both repeat `Game of Thrones / Essos / tv show / 2011` (redundancy), and half the columns describe settings rather than dragons (column bloat). SQL: `SELECT * FROM dragon INNER JOIN setting ON dragon.setting_id = setting.id`.
    d. Keys (S49–S50). `dragon`'s primary key is `name`: `dragon["name"].n_unique()` is 6, which equals `dragon.height`. `setting`'s primary key is `id`. `setting_id` is a foreign key. The join above kept all 6 dragons, which is what the foreign-key constraint guarantees. A `{tip}`: `validate="m:1"` makes `.join()` check that the right-hand key is unique (that it really is a primary key) and raise if it is not (optional, OQ 8).

11. **Star schema** (L05 S38, L06 S51), with `star_schema_boba_fact_dimension.png`. A fact table has few columns and many rows, and holds only keys. Dimension tables have more columns and fewer rows, and hold the descriptions. The fact table's granularity is one row per drink + topping + store. With 3 of each there are up to **3 × 3 × 3 = 27** combinations, the cross join of the three dimension keys (checked), and this is where §8c pays off. Optional (OQ 8): the figure's four tables built in a dropdown, then `products.join(drinks, on="drink_id").join(toppings, on="topping_id").join(stores, on="store_id")` gives 3 × 9. Toppings' `name` arrives as **`name_right`** (the §8c suffix rule), and that is worth a sentence. *Concept:* a star schema stores each fact once and each description once, and joins put back together whatever an analysis needs.

12. **Parting note.** Two or three sentences: the four properties as questions to carry into any dataset, and a pointer to the SQL chapters for querying a database directly. No new content.

**Learning Outcomes**

```
::: {note} Learning Outcomes
* Describe a dataset by its structure, granularity, temporality, and faithfulness
* Read CSV, TSV, and JSON files into Polars with `pl.read_csv` (`skip_rows=`, `separator=`) and `pl.read_json`
* Store each variable with a type that fits its meaning, using `schema_overrides=`, `.cast()`, and `.str.to_datetime()`
* Check what one row of a table represents with `.n_unique()`
* Find duplicated records, labeling errors, and disguised missing values with `.is_duplicated()`, `.value_counts()`, and `null_values=`
* Combine two tables with `.join()` using inner, left, right, full, and cross joins, and write the same join in SQL
* Explain how primary keys, foreign keys, and a star schema organize the tables in a database
:::
```

**Polars introduced here for the first time.** Each gets one or two sentences where it is first used.

| Verb | Where | Note |
|---|---|---|
| `.schema` | §2, §7c, §10b | EDA I reads dtypes off the preview header but never calls `.schema` (*critic*). |
| `pl.read_csv(skip_rows=, separator=)` | §3a–b | pandas `header=`/`delimiter=` on the slides. |
| `.equals()` | §3b, §7c, §8d | |
| `pl.read_json` | §3c | Shown to reveal that the file is nested. |
| `pl.DataFrame(records)` (a list of dicts) | §3c | EDA III §3 builds a frame from a dict of columns. Only the list-of-records form is new (*critic*). |
| `Struct` columns (read only; `.unnest()` optional) | §3c | |
| `schema_overrides=` | §4d | |
| `pl.col("a", "b", "c")` | §4e, §5 | Several columns in one expression. |
| `.str.replace_all()`, `.cast(pl.Int64)` | §4e | EDA II introduced `.cast(int)`. |
| `df.select(...).n_unique()` (distinct rows) | §5 | Series `n_unique()` is EDA III §2's (*critic*). |
| `.str.to_datetime(fmt)`, `.dt.replace_time_zone()`, `.dt.epoch("s")`, datetime subtraction | §6 | The first `.dt` use. |
| `.is_duplicated()`, `.unique()` | §7b | |
| `null_values=` | §7c | |
| `.is_nan()` | §7c | In a `{note}` only. |
| `.join(on=, how=)` with `inner`/`cross`/`left`/`right`/`full`, the `_right` suffix, `coalesce=True` | §8 | The conventions table sources this to L06 S20. |
| `.drop(col)` | §8d | Used once, to compare the filtered cross join with the inner join. The draft's table missed it (*critic*). |
| `pl.read_database(query, con)` + `duckdb.connect(..., read_only=True)` | §9 | |
| `left_on=`/`right_on=`; `validate=` (tip) | §10c–d | |

**Assumed from earlier chapters** (check each against their `.py`, and do not re-introduce): from EDA I, `pl.read_csv`, `with_columns`, `pl.col`, `.filter`, `.select`, `.sort`, `.head`, `df["col"]`, `value_counts(sort=True)`, `len`/`.height`/`.shape`, `.is_not_null`, and `.to_numpy()` (named in prose only); from EDA II, `.cast`; from EDA III, `group_by().agg()`, `.sum()`, `is_null`, `.null_count()`, `pl.DataFrame({...})`, `pl.Series`, Series `n_unique()`, and the `qcut` labels (a callback only); from EDA IV, string equality in `filter`.

**Deliberately not introduced:** `explode` (in 1.43.1 it emits a `DeprecationWarning` about `empty_as_null`, reproduced), `pl.json_normalize`, jupysql `%%sql`, `information_schema`/`duckdb_tables()` as live cells (both `sql_I`'s), `how="semi"`/`"anti"`, `join_asof`, and `pl.Enum`/`Categorical` for ordinal data (not in the decks, and seaborn raises on them in `d100`).

**Departures from the lecture**

1. **Order.** File formats come before variable types, because §4e and §5 reuse the TB table that §3 reads. Joins come after faithfulness, so that §8 → §9 → §10 → §11 runs joins → databases → keys → star schema without a break, the order L06 uses. The deck itself leaves Structure and returns to it (S22 → S37), so returning after faithfulness is the same move.
2. **Unix time.** S36's `1738674000` and `-628167600` are 5:00 **am** PST (13:00 UTC), not 5:00 pm, and February is PST, not PDT. For 5:00 pm PST, the values are 1738717200 and -628124400 (checked in Polars and DuckDB).
3. **pandas on S52–S54** (`pd.read_csv(header=...)`, `delimiter='\t'`, `pd.read_json`, `pd.DataFrame(json_dict)`) becomes `skip_rows=1`, `separator="\t"`, `pl.read_json` and `pl.DataFrame(congress["members"])`.
4. **Key columns.** SQL's `SELECT *` keeps `s.id` and `t.id`. Polars' inner/left/right joins keep one `id`, and its full join keeps `id` and `id_right`. The prose describes the Polars output (AGENTS rule 2), with no renaming to `s.id`/`t.id`.
5. **Join images.** `image60` (cross-join result) shows Eugene paired with t.id 5 twice and never with 1. `image49`/`55`/`53`/`59` duplicate live output and label columns `s.id`/`t.id`, which Polars does not produce. None of them are used.
6. **The database, not the slide.** `example_duck.db` has 6 dragons (adding puff and smaug, whose `cute` is null) and a 5-row `setting` with `media`/`place`/`type`/`start_year` (IRL has a null `place`). The slide shows 4 dragons, a 4-row setting with `place`/`source`/`mediatype`, `source` typed `INT` for a text column, and "year ≥ 2000" (S46–S50), where the database checks `yr >= 1900` (as S45 does). The chapter follows the database.
7. **S58's `NA`** becomes `null` when the toy table is built in Polars. The string-encoding lesson moves to the real `"NA"` file in §7c.
8. **L06 S20's** `on=key` becomes `on="id"`.
9. **Decorative images** dropped: S39's cat photos and S53's TaB soda.

**SQL for the triples (claim verifier)**

- Register: `admissions` (the lec04 CSV), `elections`, `tb` *after* §4e's cleaning (so the `SUM`s run on integers), `purchases`, `s`, `t`, `dragon`, `setting`. File-reading SQL (`read_csv`, `read_json`) uses paths relative to `content/new_eda_5/`.
- DuckDB names the duplicate key in `SELECT *` joins `id_1`, where Polars uses `id_right`. Compare rows, not column names.
- Run §10b's two `CREATE TABLE` statements in a **fresh in-memory connection**, `setting` first (the foreign key needs it). Registered frames named `dragon`/`setting` would collide.
- `UNNEST(..., max_depth := 2)`, `GROUP BY ALL`, `read_csv`/`read_json` and `epoch`/`timezone` are DuckDB-specific. The prose says so once, in §3c.
- Checked equal: TSV read (52 × 4, `.equals` true), JSON unnest (54 × 9), NA-file types with `nullstr`, the elections distinct count (187), the TB sums, all five joins and the cross-join-with-`WHERE`, and the epoch (1738717200.0).

**Data** (all copied into `content/new_eda_5/data/` by the orchestrator; the chapter never writes to them)

- `pivoted-ucb-data-w-everything.csv` ← fa26-dev `lec/lec04/data/` (md5 `4c9d424fbb7d930419c18cb11d5517b1`, byte-identical to `main:content/new_eda_1/data/`). Used in §2, §4c, §5, and as `.equals` target in §7c.
- `pivoted-ucb-data-w-everything-na-strings.csv` ← fa26-dev `lec/lec06/data/pivoted-ucb-data-w-everything.csv` (md5 `399eec926cee224b3320aab033b775c7`). It is **renamed** because its name collides with the file above. It is used in §7c only.
- `elections.csv` ← `main:content/new_eda_1/data/elections.csv` (md5 `47b93a15ce3ef7c3a9642170329ca58d`, identical to fa26-dev `lec/lec02/data/`).
- `cdc_tuberculosis.csv` ← `main:content/eda/data/cdc_tuberculosis.csv` (md5 `3372b94a41c6ac29efa8649d4acfb4c3`). fa26-dev has no CSV copy.
- `cdc_tuberculosis.tsv` ← fa26-dev `lec/lec06/cdc_tuberculosis.tsv`. It sits at lec06's root, not in `data/` (md5 `34a77f492346e2a43e953952532591e7`, CRLF line endings). It parses to the same frame as `main:content/eda/data/cdc_tuberculosis.tsv`, which differs only in line endings.
- `ca-congress-members.json` ← fa26-dev `lec/lec06/data/` (md5 `e50579799e3a7ce96d9d53caeb1b30cb`, identical to `main:content/eda/data/`).
- `example_duck.db` ← fa26-dev `lec/lec06/data/example_duck.db` (md5 `a05d2d42adaccbeb26acf2f972b8e8f1`). **Not** `sql_I`'s copy (`45863bb3…`), which differs. It is opened `read_only=True`, and no `.wal` appears.
- Not needed: lec06's `NST-EST*`/`nst-est2019-01.csv`, `basic_examples.db`, `duckdb_example.db`, `scene.csv` (SQL chapter), and `babynamesbystate.zip` (OQ 3).

**Images** (from the manifest; alt text as drafted there)

- `images/us_zip_code_prefix_map.png` (L05 `image40`, S26), §4d.
- `images/join_input_tables_s_t.png` (L05 `image46`), §8a.
- `images/inner_join_s_t.png` (L05 `image45`, S40–S42), §8b.
- `images/cross_join_s_t.png` (L05 `image50`, S44), §8c.
- `images/star_schema_boba_fact_dimension.png` (L05 `image47` = L06 S51), §11.
- **Not used**, although the manifest keeps them for this chapter: `cross_join_result_s_t.png` (slide error), `inner_join_result_s_t.png`, `left_join_result_s_t.png`, `right_join_result_s_t.png`, `full_outer_join_result_s_t.png`. All of these are replaced by live output (Departure 5, OQ 6). The `image28`/`image31` table screenshots are regenerated or become prose.

**Open questions**

1. **Overlap with later chapters in the TOC.** `myst.yml` places `polars_1`, `polars_2`, `eda`, and later `sql_I`, *after* `new_eda_5`. `eda` teaches the same material from the same files: CSV/TSV/JSON with the same TB and congress data, variable types, granularity, temporality with `.dt`, faithfulness and missing values, and a join. `polars_2` has "Joining Tables", and `sql_I` has "Databases", "Tables and Schema" and primary/foreign keys on the same `Dragon` database. A reader will meet all of it twice. Should those sections be trimmed, or should EDA V stay lighter? This outline edits no other chapter.
2. **The reorder** (Departure 1). Confirm, or keep the deck's order (variable types → granularity → temporality → joins → formats → faithfulness → databases).
3. **`babynames`.** Prose only, as proposed, or load it? It is a 23 MB zip of 51 header-less state files (fa26-dev `lec/lec03/data/babynamesbystate.zip`, identical to `main:content/polars_1/data/`), and loading it takes `zipfile` code and a concat, all for one granularity sentence. `polars_1` loads it properly later.
4. **The S24 answer key.** The extract's text is scrambled. Proposal: CO2 quantitative; income bracket qualitative ordinal; race/ethnicity qualitative nominal; political party qualitative nominal; year quantitative or qualitative ordinal; GPA quantitative or qualitative ordinal; postal code qualitative (ordinal or nominal). Please confirm against the rendered slide.
5. **Unix-time correction** (Departure 2). The chapter prints the correct values and says PST. Should the deck be fixed too?
6. **Join result images.** Proposal: none of the five, since live output shows each result and the images' `s.id`/`t.id` columns contradict Polars' single `id`. The alternative is to keep `left_join_result_s_t.png` alone for its grey "no match" cells.
7. **`pl.read_database` a chapter before `sql_I`.** It is S43's use 1, and it takes three visible lines. The alternative is building `dragon`/`setting` inline with `pl.DataFrame`, which removes the `duckdb` dependency from this chapter.
8. **Optional material:** the star-schema chained join and its `name_right` (§11), the `validate="m:1"` tip (§10d), and the `State`/`Location`/`Device` check (§7b). Keep all, some, or none? The chapter is long.
9. **JSON route.** `json.load` + `pl.DataFrame(congress["members"])` mirrors the slide. The Polars-only route (`pl.read_json(...).select(pl.col("members").explode()).unnest("members")`) warns in 1.43.1. Recommend the first.
10. **File name** `pivoted-ucb-data-w-everything-na-strings.csv` for lec06's copy. OK?
11. **Frame names.** `admissions` is the name the critic applied across EDA I–V (it matches the SQL table name). `admissions_na`, `tb`, `members`, `purchases`, `times`, `s`, `t`, `dragon` and `setting` are new.
12. **DBMS product names** (S40). Keep the slide's five as plain text, or generalise ("cloud data warehouses")?
