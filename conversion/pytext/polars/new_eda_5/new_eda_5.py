# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] id="lo-opener"
# ---
# title: EDA V
# ---
#
# ::: {note} Learning Outcomes
# * Describe a dataset by its structure, granularity, temporality, and faithfulness
# * Read CSV, TSV, and JSON files into Polars with `pl.read_csv` (`skip_rows=`, `separator=`) and `pl.read_json`
# * Store each variable with a type that fits its meaning, using `schema_overrides=`, `.cast()`, and `.str.to_datetime()`
# * Check what one row of a table represents with `.n_unique()`
# * Find duplicated records, labeling errors, and disguised missing values with `.is_duplicated()`, `.value_counts()`, and `null_values=`
# * Combine two tables with `.join()` using inner, left, right, full, and cross joins, and write the same join in SQL
# * Explain how primary keys, foreign keys, and a star schema organize the tables in a database
# :::
#
# In this chapter, we will step back from the admissions case study and look at four properties every dataset has: its structure, granularity, temporality, and faithfulness. Along the way, we will read files that are not simple CSVs, combine tables with joins, and see why databases split data across many tables.

# %% tags=["remove-cell"] id="setup"
import polars as pl

pl.Config.set_fmt_str_lengths(40)
pl.Config.set_tbl_rows(16)
pl.Config.set_tbl_cols(-1);

# %% [markdown] id="key-properties"
# ## Key Data Properties
#
# Whatever question we bring to a dataset, a few questions about the data itself come first. Their answers decide which analyses make sense, and they often turn up problems to fix before any analysis can start. We will organize them around four properties:
#
# * **Structure**: the "shape" of a data file.
# * **Granularity**: how fine or coarse each datum is.
# * **Temporality**: how the data is situated in time.
# * **Faithfulness**: how well the data captures "reality".
#
# Structure has three parts here: the format a file arrives in, the type of each variable, and data that is spread across several tables. We start with rectangular data, file formats, and variable types, then turn to granularity, temporality, and faithfulness. At the end of the chapter we come back to structure, combine tables with joins, and look at how databases organize their tables.

# %% [markdown] id="rectangular"
# ## Structure: Rectangular Data
#
# We usually prefer data to be **rectangular**: a set of records (rows) that all have the same fields (columns). Rectangular data is easy to manipulate and analyze, so a big part of data cleaning is reshaping data until it is rectangular. A folder of spam emails is not rectangular, for example, but a table with one row per email and one column per word, counting how often each word appears, is.
#
# Rectangular data comes in two kinds.
#
# * **Tables**, called `DataFrame`s in Polars, have named columns, and different columns can hold different types. We manipulate them with data transformations such as filtering, grouping, and joining.
# * **Matrices** hold numeric data of a single type, such as all floats or all integers. We manipulate them with linear algebra. Computation on a matrix is faster, but a matrix is less flexible than a table.
#
# The list of a table's column names and types is its **schema**, and the `.schema` attribute of a `DataFrame` holds it.
#
# **English:** Read the admissions data and list each column's name and type.

# %% id="admissions-schema"
admissions = pl.read_csv("data/pivoted-ucb-data-w-everything.csv")
admissions.schema

# %% [markdown] id="admissions-schema-sql"
# **SQL:**
# ```sql
# DESCRIBE admissions
# ```
#
# `DESCRIBE` lists a table's columns and their types, which SQL spells `VARCHAR`, `BIGINT`, and `DOUBLE`.
#
# The admissions table has 11 named columns in three types: 4 `String`, 5 `Int64`, and 2 `Float64`. It has names and a mix of types, so it is a table, not a matrix. When a method needs the matrix form, `.to_numpy()` converts a table of numbers into one, and the modeling chapters use it often.

# %% [markdown] id="file-formats"
# ## Structure: File Formats
#
# A file format is an agreement about where one record ends and the next begins, and where one field ends and the next begins. When a file follows the usual agreement, reading it takes one line of code. When it breaks the agreement, we have to tell the reader what the file does instead. We will read three common formats: CSV, TSV, and JSON.
#
# ### CSV
#
# In a **CSV** (comma-separated values) file, records are separated by newlines (`\n`) and fields are separated by commas (`,`). Our example is the CDC's count of tuberculosis (TB) cases in each U.S. jurisdiction in 2019, 2020, and 2021. First, we read it the way we have read every CSV so far.

# %% id="tb-naive"
pl.read_csv("data/cdc_tuberculosis.csv")

# %% [markdown] id="tb-naive-read"
# Something is wrong. The real header, `U.S. jurisdiction, 2019, 2020, 2021`, has become the first row of data, and the columns are named with an empty string, `No. of TB cases`, `_duplicated_0`, and `_duplicated_1`. Polars treated the file's first line as the header. That line holds only a title and some empty fields, and Polars renamed the repeated empty names so that every column has a distinct name. The table also has 53 rows, because the real header line was counted as data.
#
# ::: {tip} Look before you load
# Before reading an unfamiliar file, look at its first few lines as plain text, in a text editor or with a few lines of Python. Here are the first four lines of `cdc_tuberculosis.csv`:
#
# ```text
# ,No. of TB cases,,
# U.S. jurisdiction,2019,2020,2021
# Total,"8,900","7,173","7,860"
# Alabama,87,72,92
# ```
#
# The first line is a title, and the header is on the second line. The [`pl.read_csv` documentation](https://docs.pola.rs/api/python/stable/reference/api/polars.read_csv.html) lists the options for files that break the usual agreement.
# :::
#
# The option we need is `skip_rows=1`, which tells `pl.read_csv` to ignore that many lines at the top of the file before looking for the header.
#
# **English:** Read the TB file, skipping its title line.

# %% id="tb-read"
tb = pl.read_csv("data/cdc_tuberculosis.csv", skip_rows=1)
tb

# %% [markdown] id="tb-read-sql"
# **SQL:**
# ```sql
# SELECT *
# FROM read_csv('data/cdc_tuberculosis.csv', skip = 1)
# ```
#
# A SQL table usually lives in a database already. DuckDB, the SQL engine used throughout these notes, can also read a file directly with its `read_csv` function, which takes the same instruction as `skip = 1`.
#
# Now the table has the right shape: 52 rows and 4 columns, a `Total` row followed by one row per jurisdiction. Look at the `Total` line in the raw text above. Its counts are wrapped in quotes, as in `"8,900"`. A field that contains the delimiter has to be quoted, or the comma inside `8,900` would split it into two fields. The quotes kept the table rectangular, but all four columns are `str`. The jurisdiction names are text, and the counts were read as text too, because `8,900` is not written the way Polars expects a number to be. We will fix that in the section on variable types.

# %% [markdown] id="tsv"
# ### TSV
#
# A **TSV** (tab-separated values) file is like a CSV with tabs (`\t`) between fields instead of commas. `pl.read_csv` reads one once we name the delimiter with `separator="\t"`. To check that the result is the same table as before, we use `.equals()`, which returns `True` when two `DataFrame`s have the same column names and the same values in the same order. It does not compare types: a column of the integers 1 and 2 equals a column of the floats 1.0 and 2.0.
#
# **English:** Read the tab-separated copy of the TB data, and check that it matches the CSV.

# %% id="tsv-read"
tb_tsv = pl.read_csv("data/cdc_tuberculosis.tsv", separator="\t", skip_rows=1)
tb_tsv.equals(tb)

# %% [markdown] id="tsv-read-sql"
# **SQL:**
# ```sql
# SELECT *
# FROM read_csv('data/cdc_tuberculosis.tsv', delim = '\t', skip = 1)
# ```
#
# It is the same table. Only the delimiter changed.

# %% [markdown] id="json"
# ### JSON
#
# **JSON** (JavaScript Object Notation) stores data as nested key–value pairs, much like a Python dictionary. Our example comes from the congress.gov API and lists California's members of the U.S. Congress. JSON files are often **self-documenting**: the same file holds metadata (data about the data) next to the records themselves. `pl.read_json` reads a JSON file into a `DataFrame`, so we start there.
#
# **English:** Read the congress file into a table.

# %% id="json-read"
pl.read_json("data/ca-congress-members.json")

# %% [markdown] id="json-read-look"
# The result has 1 row and 3 columns, `members`, `pagination`, and `request`, and each cell holds a nested structure rather than a single value. The file is one document shaped like a tree, not a table. Because JSON is not rectangular, it pays to inspect the file before importing it. Python's built-in `json` module reads a JSON file into dictionaries and lists, and a dictionary's `.keys()` method lists its keys.

# %% id="json-load"
import json

with open("data/ca-congress-members.json") as f:
    congress = json.load(f)

congress.keys()

# %% [markdown] id="json-pagination"
# The three top-level keys are the three columns Polars made. `pagination` holds metadata about the records:

# %% id="json-pagination-cell"
congress["pagination"]

# %% [markdown] id="json-record"
# The file says it holds 54 records, and they live under `members`, a list with one dictionary per member. Here is the first one:

# %% id="json-first-record"
congress["members"][0]

# %% [markdown] id="json-to-table"
# Each record is nested too. `depiction` holds a dictionary, and `terms` holds a dictionary whose `item` is a list of the member's terms in office. Turning a tree into a table means choosing which level of the tree becomes the rows. Here, we want one row per member, so the rows come from the `members` list. `pl.DataFrame` builds a table from a list of dictionaries, one row per dictionary and one column per key.
#
# **English:** Make a table with one row per member of Congress.

# %% id="members-build"
members = pl.DataFrame(congress["members"])
members.shape

# %% [markdown] id="members-build-sql"
# **SQL:**
# ```sql
# SELECT UNNEST(members, max_depth := 2)
# FROM read_json('data/ca-congress-members.json')
# ```
#
# `UNNEST` turns the `members` list into one row per member, and `max_depth := 2` goes one level further and spreads each member's fields into columns. `read_json`, `read_csv`, and this form of `UNNEST` are DuckDB's own. Most databases load a file into a table once, with a separate command, and queries then read the stored table rather than the file. We come back to that idea in the section on databases.
#
# The table has 54 rows, one per member, and 9 columns, one per key. Its first three rows show the two warnings that come with JSON data.

# %% id="members-head"
members.head(3)

# %% [markdown] id="json-warnings"
# The first warning is **nested tables**. `depiction` and `terms` are `Struct` columns, whose values hold named fields shown between braces: two for `depiction` (`attribution` and `imageUrl`) and one for `terms` (`item`). `terms` goes one level deeper still, because its one field holds a list of terms, each with a chamber, an end year, and a start year. A column whose cells hold small tables of their own is not flat, and analyzing a member's terms would mean unpacking it first.
#
# The second warning is **inconsistent fields**. Nothing forces every record in a JSON file to have the same keys. The `null` inside each `terms` value above is one example: a term still in progress has no `endYear` key, as the first record shows. The `district` key is another. Counting the records that have one shows that two of the 54 do not:

# %% id="district-key-count"
sum("district" in member for member in congress["members"])

# %% [markdown] id="district-null-intro"
# Where a record has no `district` key, `pl.DataFrame` fills the column with `null`.
#
# **English:** Find the members with no district.

# %% id="district-null"
members.filter(pl.col("district").is_null()).select("name", "district")

# %% [markdown] id="district-null-read"
# The two members with no district are Adam Schiff and Alex Padilla, California's two senators. A senator represents the whole state, so their records have no district to report.

# %% [markdown] id="variable-types"
# ## Structure: Variable Types
#
# A variable's **feature type** is about what its values mean. Its dtype (`String`, `Int64`, and so on) is about how the values are stored. These are separate choices, and a mismatch in either direction causes bugs.
#
# ### Feature Types
#
# * **Quantitative** variables are measurable numbers: price, temperature, age.
# * **Qualitative** (or categorical) variables sort values into categories, and they come in two kinds.
#   * **Ordinal** variables have categories with a natural order: grade level, age group.
#   * **Nominal** variables have categories with no natural order: phone brand, or ID numbers assigned at random.
#
# A safe default is to store qualitative data as strings, even when the categories are written with digits. Arithmetic on a category is rarely meaningful, and a string type keeps us from doing it by accident.
#
# Try to classify each variable below before reading its answer.
#
# | Variable | Feature type |
# |---|---|
# | CO2 level (ppm) | Quantitative |
# | Income bracket (low, med, high) | Qualitative ordinal |
# | Race/ethnicity | Qualitative nominal |
# | Political party | Qualitative nominal |
# | Year | Quantitative, or qualitative ordinal |
# | GPA | Quantitative, or qualitative ordinal |
# | U.S. postal code | Qualitative ordinal, or qualitative nominal |
#
# The distinction between types is sometimes murky, and context matters. GPA is a number, and averaging GPAs is common, so it can be quantitative. But if the question is how many students fall in each GPA band, ordered categories may serve better. The right type depends on the question you are asking of the data.
#
# ### The Admissions Columns
#
# Here are the admissions columns, classified against the schema above:
#
# | Columns | Feature type | Stored as |
# |---|---|---|
# | `school`, `city`, `county` | Qualitative nominal | `String` |
# | `is_charter` (`"Y"` or `"N"`) | Qualitative nominal | `String` |
# | `applied`, `admitted`, `attended`, `tot_enrolled`, `grade_12` | Quantitative | `Int64` |
# | `pct_free_reduced`, `dist_to_ucb_miles` | Quantitative | `Float64` |
#
# Every column's dtype fits its meaning. The `frl_percentile` column that EDA III and EDA IV built with `qcut` is a subtler case. Its labels, `"0-25"`, `"25-50"`, `"50-75"`, and `"75-100"`, are ordinal values stored as strings. They sort in the right order only because the labels were chosen so that alphabetical order matches numeric order. A label such as `"5-25"` would sort after `"25-50"`.

# %% [markdown] id="zip-codes"
# ### ZIP Codes
#
# What type of variable is a U.S. postal code, such as 94720? It is written with digits, but adding two ZIP codes means nothing, so it is not quantitative. It is not arbitrary either. ZIP codes are assigned by geography: they start at 0 in the Northeast and rise toward the West Coast.
#
# ```{image} images/us_zip_code_prefix_map.png
# :alt: Map of the United States colored by ZIP-code prefix region. Prefixes start at 0 in the Northeast (such as 039-049 in Maine) and rise westward to the 90s on the Pacific coast, so ZIP codes are geographically ordered, and a Northeast code stored as an integer would lose its leading zero.
# :width: 600
# ```
#
# A ZIP code is an identifier with a geographic order. Storing one as an integer loses information, and the Northeast shows how. To try this on a two-line CSV without creating a file, we use `io.StringIO`, which wraps a string so that `pl.read_csv` can read it as if it were a file.
#
# **English:** Read a small file of cities and their ZIP codes.

# %% id="zip-int"
import io

zip_csv = "city,zip\nCambridge,02138\nBerkeley,94720\n"
pl.read_csv(io.StringIO(zip_csv))

# %% [markdown] id="zip-int-sql"
# **SQL:**
# ```sql
# SELECT CAST('02138' AS INTEGER)
# ```
#
# Polars saw only digits in `zip` and inferred `i64`, so Cambridge's ZIP code became 2138. The SQL cast returns 2138 as well. The leading zero is gone, and 2138 is not a valid ZIP code. The `schema_overrides=` argument of `pl.read_csv` sets a column's type by name instead of letting Polars guess it.
#
# **English:** Read the same file, storing `zip` as a string.

# %% id="zip-string"
pl.read_csv(io.StringIO(zip_csv), schema_overrides={"zip": pl.String})

# %% [markdown] id="zip-string-read"
# Now `zip` is `str`, and Cambridge keeps `02138`. In a database, a column's type is declared once, when its table is created, and we will see such a declaration near the end of this chapter.

# %% [markdown] id="numbers-as-text"
# ### Numbers Stored as Text
#
# The TB table has the opposite problem. Its counts are quantitative, but they arrived as strings because of the commas in values such as `8,900`. We can fix all three year columns at once:
#
# * `pl.col` accepts several column names, and the expression that follows runs on each of those columns separately.
# * `.str` gives access to string methods, and `.str.replace_all(",", "")` replaces every comma with nothing.
# * `.cast(pl.Int64)` converts the cleaned strings to 64-bit integers. EDA II's `.cast(int)` produced the same type, and `pl.Int64` names it explicitly.
#
# These expressions keep their columns' names, so `with_columns` replaces the three columns instead of adding new ones.
#
# **English:** Remove the commas from the three year columns and store them as integers.

# %% id="tb-clean"
tb = tb.with_columns(pl.col("2019", "2020", "2021").str.replace_all(",", "").cast(pl.Int64))
tb.head()

# %% [markdown] id="tb-clean-sql"
# **SQL:**
# ```sql
# SELECT "U.S. jurisdiction",
#        CAST(REPLACE("2019", ',', '') AS INTEGER) AS "2019",
#        CAST(REPLACE("2020", ',', '') AS INTEGER) AS "2020",
#        CAST(REPLACE("2021", ',', '') AS INTEGER) AS "2021"
# FROM read_csv('data/cdc_tuberculosis.csv', skip = 1)
# ```
#
# The column names go in double quotes here, because they begin with digits (or, for `U.S. jurisdiction`, because the name contains spaces and periods). Single quotes, as in `','`, mark a string value.
#
# The three year columns are now `i64`, and the 2019 `Total` is the number 8900.

# %% [markdown] id="granularity"
# ## Granularity
#
# **Granularity** is what each record represents: a single purchase, a single person, a group of users. **Fine-grained** data has one row per small unit, such as one row per purchase. **Coarse-grained** data rolls many of those units up into each row, such as one row per customer with their total spending. Some datasets also include summaries, called **rollups**, as records next to the rows they summarize. If the data is coarse, ask how the records were aggregated: by summing, averaging, or something else. Coarse rows cannot be split back into finer ones, so a dataset's granularity limits the questions it can answer.
#
# ::: {note} "The data shows" or "the data show"?
# "Data" is the plural of "datum", so "the data show" is technically correct and "the data shows" is not. In practice, either is fine.
# :::
#
# ### Elections
#
# What does each row of the `elections` dataset represent?
#
# **English:** Read the elections data and preview it.

# %% id="elections-read"
elections = pl.read_csv("data/elections.csv")
elections

# %% [markdown] id="elections-counts-intro"
# The shape header says the table has 187 rows. Each row names a year and a candidate, so a natural guess is that each row is one candidate in one election. We can test the guess by counting distinct values. `.n_unique()` on a `Series`, which EDA III used, counts the distinct values in one column.
#
# **English:** Count the distinct years, the distinct candidates, and the rows.

# %% id="elections-counts"
elections["Year"].n_unique(), elections["Candidate"].n_unique(), elections.height

# %% [markdown] id="elections-counts-sql"
# **SQL:**
# ```sql
# SELECT COUNT(DISTINCT Year), COUNT(DISTINCT Candidate), COUNT(*)
# FROM elections
# ```
#
# `COUNT(DISTINCT ...)` counts distinct values instead of rows.
#
# Neither column identifies a row by itself: there are 51 years and 135 candidates, against 187 rows. Andrew Jackson, for example, appears in 1824, 1828, and 1832. Called on a `DataFrame`, `.n_unique()` counts distinct *rows*, so after a `select` of two columns it counts the distinct combinations of their values.
#
# **English:** Count the distinct combinations of year and candidate.

# %% id="elections-pairs"
elections.select("Year", "Candidate").n_unique()

# %% [markdown] id="elections-pairs-sql"
# **SQL:**
# ```sql
# SELECT COUNT(*)
# FROM (SELECT DISTINCT Year, Candidate FROM elections)
# ```
#
# `SELECT DISTINCT` keeps one copy of each distinct row, and the outer query counts them.
#
# There are 187 distinct combinations of year and candidate, the same as the number of rows. Each row of `elections` represents a unique combination of candidate and year. That reading rests on two assumptions: there is at most one election in a year, and a candidate represents one party in each election.
#
# ### Baby Names
#
# The `babynames` dataset counts how many babies were given each name. Each of its rows represents a unique combination of name, state, sex, and year. Each count is itself a rollup: a row with a count of 5 stands for five individual births, which the dataset does not list one by one.
#
# ### Admissions
#
# The admissions table deserves the same check. EDA I noticed three schools named ABRAHAM LINCOLN HIGH SCHOOL, so a school's name alone may not identify a row.
#
# **English:** Count the distinct school names and the rows.

# %% id="admissions-schools"
admissions["school"].n_unique(), admissions.height

# %% [markdown] id="admissions-schools-sql"
# **SQL:**
# ```sql
# SELECT COUNT(DISTINCT school), COUNT(*)
# FROM admissions
# ```
#
# There are 1201 distinct names for 1268 rows, so some names repeat.
#
# **English:** Count the distinct combinations of school and city.

# %% id="admissions-pairs"
admissions.select("school", "city").n_unique()

# %% [markdown] id="admissions-pairs-sql"
# **SQL:**
# ```sql
# SELECT COUNT(*)
# FROM (SELECT DISTINCT school, city FROM admissions)
# ```
#
# There are 1268 distinct combinations of school and city, one per row. A row of `admissions` is one school, identified by its name and its city together. Each row is also a rollup: its counts add up many individual decisions, by students to apply and attend and by the university to admit. That is why counts below 3 are blank (EDA I), since a count of one or two could reveal what happened to a single student.
#
# ### Rollups as Records
#
# The TB table holds a rollup as a record: its `Total` row sits next to the jurisdictions it sums. We can check that it really is their sum.
#
# **English:** Add up each year's cases over the jurisdictions, leaving out the `Total` row.

# %% id="tb-total-check"
tb.filter(pl.col("U.S. jurisdiction") != "Total").select(pl.col("2019", "2020", "2021").sum())

# %% [markdown] id="tb-total-check-sql"
# **SQL:**
# ```sql
# SELECT SUM("2019"), SUM("2020"), SUM("2021")
# FROM tb
# WHERE "U.S. jurisdiction" <> 'Total'
# ```
#
# `<>` is SQL's "not equal to".
#
# The sums, 8900, 7173, and 7860, match the `Total` row exactly. Summing each whole column would have counted every case twice, once in its jurisdiction's row and again in `Total`.

# %% [markdown] id="temporality"
# ## Temporality
#
# **Temporality** is how the data is situated in time. What type of variable is a datetime, such as `01/01/2025 3:30pm`? People write datetimes as strings, and a first attempt might store them that way. Stored as strings, datetimes are hard to compare ("before" and "after") and hard to compute with ("how long between"), and they take more space than numbers do. Here are three datetimes stored as strings, in a `DataFrame` built from a dictionary of columns as in EDA III.
#
# **English:** Sort three datetimes written as text.

# %% id="times-string-sort"
times = pl.DataFrame({"when": ["02/04/2025 5:00pm", "01/01/2025 3:30pm", "02/04/1950 5:00pm"]})
times.sort("when")

# %% [markdown] id="times-string-sort-sql"
# **SQL:**
# ```sql
# SELECT *
# FROM times
# ORDER BY "when"
# ```
#
# `WHEN` is a SQL keyword, so as a column name it needs double quotes.
#
# Strings sort character by character, so 1950 lands between the two 2025 dates. `02/04/1950` comes after `01/01/2025` because `02` is greater than `01`, and before `02/04/2025` because `19` is less than `20`.
#
# The fix is to **parse** each string into a datetime. `.str.to_datetime()` does this, given a format that describes how the string is written: `%m` is the month, `%d` the day, `%Y` the four-digit year, `%I` the hour on a 12-hour clock, `%M` the minute, and `%p` the am/pm marker.
#
# **English:** Parse each string into a datetime, then sort on the result.

# %% id="times-parse"
times = times.with_columns(parsed=pl.col("when").str.to_datetime("%m/%d/%Y %I:%M%p"))
times.sort("parsed")

# %% [markdown] id="times-parse-sql"
# **SQL:**
# ```sql
# SELECT "when", strptime("when", '%m/%d/%Y %I:%M%p') AS parsed
# FROM times
# ORDER BY parsed
# ```
#
# `strptime` is DuckDB's name for parsing text into a timestamp; other databases spell it differently (PostgreSQL uses `to_timestamp`, with its own format codes). In Polars, the new column's type is `datetime[μs]`, a point in time recorded to the microsecond, and the sort is now chronological. Datetimes also support arithmetic: subtracting one from another gives a `duration`. Inside `select`, `.max()` and `.min()` work like the `Series` methods from EDA I and reduce a column to one value.
#
# **English:** Find how much time separates the earliest and latest datetimes.

# %% id="times-span"
times.select(span=pl.col("parsed").max() - pl.col("parsed").min())

# %% [markdown] id="times-span-sql"
# **SQL:**
# ```sql
# SELECT MAX(strptime("when", '%m/%d/%Y %I:%M%p'))
#        - MIN(strptime("when", '%m/%d/%Y %I:%M%p')) AS span
# FROM times
# ```
#
# The earliest and latest times are 27394 days apart, which is exactly 75 years.
#
# ### Unix Time
#
# A better way to store a datetime is as a number counted from an agreed origin. The computing standard is **Unix time** (also called POSIX time): the number of seconds since midnight on January 1, 1970, in Coordinated Universal Time (UTC). With every time stored as one number, "before", "after", and "how long between" become arithmetic.
#
# The origin is defined in UTC, so before we can count seconds from it we have to know which time zone our times are in. A time without a time zone is ambiguous: 5:00 pm in California and 5:00 pm in London, on the same February day, are eight hours apart. Ours are California times. `.dt` gives access to datetime methods, the way `.str` does for strings. `.dt.replace_time_zone("America/Los_Angeles")` attaches California's time zone to each datetime without changing its clock reading, and `.dt.epoch("s")` then counts the seconds since the Unix origin.
#
# **English:** Treat the times as California times, and convert each one to Unix time.

# %% id="times-epoch"
times.with_columns(
    unix=pl.col("parsed").dt.replace_time_zone("America/Los_Angeles").dt.epoch("s")
)

# %% [markdown] id="times-epoch-sql"
# **SQL:**
# ```sql
# SELECT "when",
#        epoch(timezone('America/Los_Angeles', strptime("when", '%m/%d/%Y %I:%M%p'))) AS unix
# FROM times
# ```
#
# DuckDB returns these values as `DOUBLE` (floating-point numbers), where Polars returns `i64`.
#
# February is winter, so California is on Pacific Standard Time (PST), eight hours behind UTC. At 5:00 pm on February 4, 2025 in California, it is 1:00 am on February 5 in UTC, which is 1738717200 seconds after the origin. The 1950 time is -628124400: negative, because it falls before 1970.

# %% [markdown] id="faithfulness"
# ## Faithfulness
#
# **Faithfulness** asks whether we can trust the data. How well does it reflect reality, and where might what the data says differ from what happened? Some questions to help answer that:
#
# * Are there any biases in the data collection process?
# * Who (or what) might not be represented in this data?
# * Would the data look different if someone else had collected it?
# * Why is the data grouped or sliced the way it is?
# * Were there limitations in the data-gathering process that matter?
#
# Some faithfulness problems are visible in the data itself, and code can help find them.
#
# ### Finding Problems in a Small Table
#
# The table below is a small, made-up dataset of nine rows, small enough to read in full. Before reading on, look for anything that seems wrong.
#
# ````{dropdown} Click to see the code
# :open: false
# ```python
# purchases = pl.DataFrame(
#     {
#         "ID": [0, 1, 2, 3, 4, 4, 5, 6, 7],
#         "Category": ["Shoes", "Socks", "Socks", "Shirts", "Shoes", "Shoes", "Shirts", "Pnts", "Hats"],
#         "State": ["CA", "NM", "XY", "NY", "FL", "FL", "CA", "TX", "CA"],
#         "Location": ["CA", "NM", "XY", "NY", "FL", "FL", "CA", "TX", "CA"],
#         "Device": [1, 1, 1, 1, 1, 1, 1, 1, 1],
#         "Purchased": [1, 0, 0, None, 0, 0, 0, 1, -1],
#     }
# )
# purchases
# ```
# ````

# %% tags=["remove-input"] id="purchases-build"
purchases = pl.DataFrame(
    {
        "ID": [0, 1, 2, 3, 4, 4, 5, 6, 7],
        "Category": ["Shoes", "Socks", "Socks", "Shirts", "Shoes", "Shoes", "Shirts", "Pnts", "Hats"],
        "State": ["CA", "NM", "XY", "NY", "FL", "FL", "CA", "TX", "CA"],
        "Location": ["CA", "NM", "XY", "NY", "FL", "FL", "CA", "TX", "CA"],
        "Device": [1, 1, 1, 1, 1, 1, 1, 1, 1],
        "Purchased": [1, 0, 0, None, 0, 0, 0, 1, -1],
    }
)
purchases

# %% [markdown] id="duplicates"
# #### Duplicated Records
#
# `.is_duplicated()` returns a Boolean `Series` that is `True` for every row with an identical copy elsewhere in the table. Passing it to `.filter` keeps those rows.
#
# **English:** Find the rows that appear more than once.

# %% id="duplicates-find"
purchases.filter(purchases.is_duplicated())

# %% [markdown] id="duplicates-find-sql"
# **SQL:**
# ```sql
# SELECT *, COUNT(*) AS n
# FROM purchases
# GROUP BY ALL
# HAVING COUNT(*) > 1
# ```
#
# `GROUP BY ALL`, a DuckDB shorthand, groups by every selected column that is not an aggregate (most other databases need those columns listed after `GROUP BY`), and `HAVING` keeps the groups that meet a condition, the way `WHERE` keeps rows. The SQL returns each duplicated record once, with its number of copies in `n`.
#
# Polars shows both copies of the row with ID 4. If there is no reason for the duplication, we drop the extra copy. `.unique()` keeps one copy of each distinct row.
#
# **English:** Keep one copy of each distinct row, and count the rows that remain.

# %% id="duplicates-drop"
purchases.unique().height

# %% [markdown] id="duplicates-drop-sql"
# **SQL:**
# ```sql
# SELECT COUNT(*)
# FROM (SELECT DISTINCT * FROM purchases)
# ```
#
# Eight rows remain out of nine.
#
# #### Labeling and Spelling Errors
#
# A frequency table of a qualitative column puts rare values, which include most typos, at the bottom, where they are easy to spot.
#
# **English:** Count the rows in each category.

# %% id="category-counts"
purchases["Category"].value_counts(sort=True)

# %% [markdown] id="category-counts-sql"
# **SQL:**
# ```sql
# SELECT Category, COUNT(*) AS count
# FROM purchases
# GROUP BY Category
# ORDER BY count DESC
# ```
#
# `Pnts` is almost certainly a misspelling of `Pants`. The `State` column has a similar problem: the row with ID 2 says `XY`, which is not a state. Correct errors like these when you can, and ignore them only if you have to.
#
# #### Sentinel and Missing Values
#
# **English:** Count the rows with each value of `Purchased`.

# %% id="purchased-counts"
purchases["Purchased"].value_counts(sort=True)

# %% [markdown] id="purchased-counts-sql"
# **SQL:**
# ```sql
# SELECT Purchased, COUNT(*) AS count
# FROM purchases
# GROUP BY Purchased
# ORDER BY count DESC
# ```
#
# `Purchased` looks like a yes/no column, with 0 for no and 1 for yes, and most rows hold one of those two values. But one row holds `null`, and one holds -1. A -1 in a 0/1 column is probably a **sentinel**: a stand-in value that someone chose to mean "unknown" or "not recorded". Code that averages `Purchased` would treat that -1 as a real number without complaint.

# %% [markdown] id="missing-encodings"
# ### How Missing Values Are Encoded
#
# Missing data does not always look missing. Some common encodings:
#
# | Encoding | Examples |
# |---|---|
# | A blank or a space | `""`, `" "` |
# | A sentinel number | `0`, `-1999`, `12345` |
# | Not a Number | `NaN` |
# | A missing-value marker | `null`, `NA` |
# | A default date | 1970, 2000 |
#
# A default date of January 1, 1970 is often a Unix time of 0 standing in for "unknown". A single column can even hold a real 0 in some rows and a placeholder 0 in others. Before deciding how to handle missing values, work out how they were encoded and why they are missing.
#
# ::: {note} `NaN` is not `null`
# Polars keeps two kinds of "no value" apart. `NaN` ("not a number") is a floating-point value, the result of a computation such as 0/0. `null` means the value is missing. `.is_null()` finds only nulls, and `.is_nan()` finds only `NaN`s.
# :::

# %% id="nan-vs-null"
pl.DataFrame({"value": [1.0, float("nan"), None]}).with_columns(
    is_null=pl.col("value").is_null(),
    is_nan=pl.col("value").is_nan(),
)

# %% [markdown] id="nan-vs-null-read"
# `is_null` is `true` only in the third row, and `is_nan` is `true` only in the second. The `is_nan` of a null is itself `null`: the value is unknown, so there is no way to say whether it is `NaN`.
#
# Encodings matter in real data too. The next file is the admissions table again, with one difference: where our copy leaves a field empty, this copy writes the two letters `NA`.
#
# **English:** Read the copy of the admissions data that writes missing values as `NA`, and list its column types.

# %% id="admissions-na-read"
admissions_na = pl.read_csv("data/pivoted-ucb-data-w-everything-na-strings.csv")
admissions_na.schema

# %% [markdown] id="admissions-na-read-sql"
# **SQL:**
# ```sql
# DESCRIBE SELECT * FROM read_csv('data/pivoted-ucb-data-w-everything-na-strings.csv')
# ```
#
# Six numeric columns arrived as `String`: `admitted`, `attended`, `tot_enrolled`, `grade_12`, `pct_free_reduced`, and `dist_to_ucb_miles`. `NA` is not a number, so a column containing it can only be read as text. Only `applied`, which has no missing values, is still `Int64`. The column types are the first clue that missing values are hiding in the file.
#
# **English:** Count the rows with each value of `is_charter`.

# %% id="admissions-na-charter"
admissions_na["is_charter"].value_counts(sort=True)

# %% [markdown] id="admissions-na-charter-sql"
# **SQL:**
# ```sql
# SELECT is_charter, COUNT(*) AS count
# FROM read_csv('data/pivoted-ucb-data-w-everything-na-strings.csv')
# GROUP BY is_charter
# ORDER BY count DESC
# ```
#
# `is_charter` should hold `Y` or `N`. Here it also has a third "category", `NA`, with 35 schools, so missingness now looks like data. The numeric columns fare worse. Here are the three most common values of `admitted`:

# %% id="admissions-na-admitted"
admissions_na["admitted"].value_counts(sort=True).head(3)

# %% [markdown] id="admissions-na-fix"
# The most common "value" of `admitted` is `NA`, in 445 schools.
#
# The fix is to tell `pl.read_csv` which strings mean "missing". With `null_values="NA"`, every `NA` field is read as `null`.
#
# **English:** Read the file again, treating `NA` as missing, and check that its values and its column types match our copy of the admissions data.

# %% id="admissions-na-fixed"
admissions_na = pl.read_csv("data/pivoted-ucb-data-w-everything-na-strings.csv", null_values="NA")
admissions_na.equals(admissions), admissions_na.schema == admissions.schema

# %% [markdown] id="admissions-na-fixed-sql"
# **SQL:**
# ```sql
# SELECT *
# FROM read_csv('data/pivoted-ucb-data-w-everything-na-strings.csv', nullstr = 'NA')
# ```
#
# DuckDB calls the same option `nullstr`.
#
# Both checks are `True`: the two tables hold the same values, and every column has the same type. `.null_count()`, from EDA III, shows where the nulls are.

# %% id="admissions-na-nulls"
admissions_na.null_count()

# %% [markdown] id="missing-approaches"
# `admitted` has 445 nulls, `attended` 776, and `pct_free_reduced` 94. `tot_enrolled`, `grade_12`, `is_charter`, and `dist_to_ucb_miles` have 35 each, and `school`, `city`, `county`, and `applied` have none.
#
# ### Handling Missing Values
#
# Once we know how and why values are missing, there are three broad approaches.
#
# 1. **Keep them as null.** This is a good default. For a qualitative column, consider making "Missing" its own category.
# 2. **Drop the records with missing values.** This is typically a bad default, because it is safe only when values are missing at random. If a temperature probe went offline for a minute, its readings are likely missing at random, and dropping them is fine. If a police officer never records the outcomes of vehicle stops, those outcomes are not missing at random, and dropping them leaves a dataset that is systematically missing that officer's stops.
# 3. **Impute or interpolate**: infer the missing values.
#    * Mean or median imputation replaces each missing value with the column's mean or median.
#    * Hot deck imputation replaces it with a random non-missing value.
#    * Regression imputation uses a model to predict it.
#    * Multiple imputation fills in several random values and checks how sensitive the results are to them. It is beyond the scope of this course.
#
# EDA III and EDA IV worked through the third approach on the admissions data. The UC leaves counts below 3 blank, so those chapters replaced each missing count with a random whole number from 0 to 2, drawn with a fixed seed. Then they checked their conclusions against filling every missing count with 0 and with 2, the smallest and largest values it could have been. That is imputation followed by a sensitivity check. EDA III also tried ignoring the schools with missing counts, which is the second approach, and found that it pushed admission rates outside the range that the 0 and 2 fills allow.

# %% [markdown] id="joins"
# ## Structure Again: Data in Several Tables
#
# Data often arrives spread across several files or tables. The admissions table we have used since EDA I is an example: the UC's admissions counts were combined with enrollment and school information from the California Department of Education. The operation that combines them is a **join**. A join pairs the rows of two tables by a **key**, a column whose values say what each row is about, and the kind of join decides what happens to rows that have no partner.
#
# ### Two Small Tables
#
# To see each kind of join clearly, we use two tiny tables about cats. `s` holds each cat's name and `t` holds each cat's breed, and both are keyed by `id`.

# %% id="cats-build"
s = pl.DataFrame({"id": [0, 1, 2, 4], "name": ["Apricot", "Boots", "Cally", "Eugene"]})
t = pl.DataFrame({"id": [1, 2, 4, 5], "breed": ["persian", "ragdoll", "bengal", "persian"]})

# %% [markdown] id="cats-tables"
# ```{image} images/join_input_tables_s_t.png
# :alt: Two small tables. Table s has ids 0, 1, 2, 4 with cat names Apricot, Boots, Cally, Eugene. Table t has ids 1, 2, 4, 5 with breeds persian, ragdoll, bengal, persian. Ids 1, 2 and 4 appear in both tables, id 0 only in s, and id 5 only in t.
# :width: 450
# ```
#
# Ids 1, 2, and 4 appear in both tables. Id 0 (Apricot) appears only in `s`, and id 5 only in `t`.
#
# ### Inner Join
#
# An **inner join** combines each row of the first table with its matching row in the second table. A row that has no match is left out.
#
# ```{image} images/inner_join_s_t.png
# :alt: Tables s and t with lines connecting rows whose ids match (1, 2 and 4). An inner join on s.id = t.id returns only those three rows, Boots-persian, Cally-ragdoll and Eugene-bengal. Apricot (id 0) and the id-5 persian are dropped.
# :width: 700
# ```
#
# `.join()` takes the other table, the key column as `on=`, and the kind of join as `how=`.
#
# **English:** For each cat, attach its breed, keeping only the cats that appear in both tables.

# %% id="join-inner"
s.join(t, on="id", how="inner")

# %% [markdown] id="join-inner-sql"
# **SQL:**
# ```sql
# SELECT *
# FROM s INNER JOIN t
#     ON s.id = t.id
# ```
#
# SQL specifies a join as part of the `FROM` clause: the kind of join (`INNER JOIN`), then the columns that decide which rows match (after `ON`). In Polars, `how=` gives the kind of join and `on=` the matching column. `"inner"` is the default, so `s.join(t, on="id")` gives the same result.
#
# The result has 3 rows: Boots, Cally, and Eugene. Apricot and the id-5 persian have no partner, so they are dropped. The Polars result has a single `id` column, because on every row it keeps, the two tables' ids are equal. The figure and the SQL's `SELECT *` keep one `id` column from each table. For the full set of options, see the [`DataFrame.join` documentation](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.join.html) and the [joins page of the Polars user guide](https://docs.pola.rs/user-guide/transformations/joins/).
#
# ### Cross Join
#
# A **cross join** pairs every row of the first table with every row of the second, and it is also called a Cartesian product. Nothing has to match, so a cross join needs no key, and `on=` is left out.
#
# ```{image} images/cross_join_s_t.png
# :alt: Tables s and t, each with four rows, with a line from every row of s to every row of t. A cross join pairs every row with every other row and needs no matching key.
# :width: 700
# ```
#
# **English:** Pair every cat name with every breed.

# %% id="join-cross"
s.join(t, how="cross")

# %% [markdown] id="join-cross-sql"
# **SQL:**
# ```sql
# SELECT *
# FROM s CROSS JOIN t
# ```
#
# The result has 4 × 4 = 16 rows. Both tables have a column named `id`, and a table cannot have two columns with the same name, so Polars keeps the left table's column as `id` and renames the right table's `id_right`. In general, Polars adds the suffix `_right` to any column of the right table whose name is already taken.
#
# ### Inner Join as a Filtered Cross Join
#
# The 16 rows include the 3 in which the two ids match. Keeping only those rows gives back the inner join.
#
# **English:** Keep the rows of the cross join whose two ids match.

# %% id="join-cross-filter"
matched = s.join(t, how="cross").filter(pl.col("id") == pl.col("id_right"))
matched

# %% [markdown] id="join-cross-filter-sql"
# **SQL:**
# ```sql
# SELECT *
# FROM s CROSS JOIN t
# WHERE s.id = t.id
# ```
#
# This query returns the same rows as the inner join:
#
# ```sql
# SELECT *
# FROM s INNER JOIN t
#     ON s.id = t.id
# ```
#
# To check, we remove `id_right` with `.drop()`, which returns the table without the named columns, and compare the result with the inner join.

# %% id="join-cross-filter-check"
matched.drop("id_right").equals(s.join(t, on="id", how="inner"))

# %% [markdown] id="join-left"
# This is a way to think about an inner join, not how a database computes one. Building every pair first would be far too slow on large tables.
#
# ### Left Join
#
# A **left join** (or left outer join) keeps every row of the left table, which is the first one named, and only the matching rows of the right table. Where a row of the left table has no match, the right table's columns are filled with `null`.
#
# **English:** For each cat in `s`, attach its breed if `t` has one.

# %% id="join-left-cell"
s.join(t, on="id", how="left")

# %% [markdown] id="join-left-sql"
# **SQL:**
# ```sql
# SELECT *
# FROM s LEFT JOIN t
#     ON s.id = t.id
# ```
#
# All 4 cats in `s` are kept, and Apricot's `breed` is `null`, because `t` has no row with id 0. This null is a different kind of missing value from the ones in the section on faithfulness. Nothing was lost or suppressed: there was simply no partner to match.
#
# ### Right Join
#
# A **right join** is the mirror image. It keeps every row of the right table, the second one named, and fills in `null` where the left table has no match.
#
# **English:** For each breed in `t`, attach the cat's name if `s` has one.

# %% id="join-right"
s.join(t, on="id", how="right")

# %% [markdown] id="join-right-sql"
# **SQL:**
# ```sql
# SELECT *
# FROM s RIGHT JOIN t
#     ON s.id = t.id
# ```
#
# All 4 rows of `t` are kept, and the `name` for id 5 is `null`. Notice the column order in the Polars result, `name`, `id`, `breed`: the left table's other columns come first, then the right table's key and columns.
#
# ### Full Outer Join
#
# A **full outer join** keeps every row of both tables. It pairs the rows that match and fills in `null` wherever a row has no partner, much like doing a left join and a right join at once.
#
# **English:** Keep every row from both tables, pairing names with breeds where the ids match.

# %% id="join-full"
s.join(t, on="id", how="full")

# %% [markdown] id="join-full-sql"
# **SQL:**
# ```sql
# SELECT *
# FROM s FULL JOIN t
#     ON s.id = t.id
# ```
#
# The result has 5 rows: the three matched cats, Apricot with no breed, and the id-5 persian with no name. This time Polars keeps both `id` and `id_right`, because each of them is `null` on one unmatched row: `id` is null on the persian's row, and `id_right` on Apricot's. Passing `coalesce=True` merges the two into a single `id` column, which takes whichever of the two values is not null.

# %% id="join-full-coalesce"
s.join(t, on="id", how="full", coalesce=True)

# %% [markdown] id="join-order-note"
# Now every row has an `id`. A join does not promise any particular row order, so refer to the rows of a join's result by their key or name, not by their position. If you sort a full join on `id` without coalescing, pass `nulls_last=True` so that the unmatched right-table row does not sort to the top.
#
# ### Equivalent Joins
#
# Which of the queries A, B, and C return the same information as the first query below? Column order does not matter.
#
# ```sql
# -- The query to match
# SELECT * FROM s LEFT JOIN t ON s.id = t.id;
#
# -- A
# SELECT * FROM s LEFT JOIN t ON t.id = s.id;
#
# -- B
# SELECT * FROM t RIGHT JOIN s ON s.id = t.id;
#
# -- C
# SELECT * FROM s FULL JOIN t ON s.id = t.id WHERE s.id IS NOT NULL;
# ```
#
# All three do.
#
# * **A**: the order of the two sides of an equality does not matter.
# * **B**: a right join is a left join with the tables named in the other order. Here `t`'s columns come first.
# * **C**: the full join adds the unmatched id-5 row, whose `s.id` is null, and the `WHERE` clause removes it again.
#
# B and C can be written in Polars too. B names `t` first and keeps every row of `s`:

# %% id="equiv-b"
t.join(s, on="id", how="right")

# %% [markdown] id="equiv-c"
# It has the same 4 rows as the left join, with the columns in the order `breed`, `id`, `name`. C filters the full join down to the rows where `s`'s id, which Polars calls `id`, is not null:

# %% id="equiv-c-cell"
s.join(t, on="id", how="full").filter(pl.col("id").is_not_null())

# %% [markdown] id="equiv-read"
# It has the same 4 rows as the left join, plus the `id_right` column. A has no Polars counterpart, because `on=` names the key only once, so there is no equality to write in the other order.

# %% [markdown] id="databases"
# ## Databases: Why SQL?
#
# Every table in this chapter so far came from a file. In practice, much of the data a data scientist works with lives in a database instead. A **database** is an organized collection of data. A **database management system** (DBMS) is a software system that stores, manages, and gives access to one or more databases. Common large-scale DBMSs in data science include Google BigQuery, Amazon Redshift, Snowflake, Databricks, and Microsoft SQL Server.
#
# Why not keep everything in CSV files? A DBMS has advantages in two areas.
#
# **Data storage**
#
# * Reliable storage that survives system crashes and disk failures.
# * Computation on data that does not fit in memory.
# * Special data structures that improve performance (covered in CS 186).
#
# **Data management**
#
# * Control over how the data is logically organized and who has access to it.
# * Guarantees on the data, such as a person's age never being negative, which prevent data anomalies.
# * Safe concurrent operations, so that many users can read and write the data at the same time, as they do with ATM transactions.
#
# EDA I described a typical EDA workflow: a database with many dynamic tables, updated frequently (after every customer purchase, for example); a few snapshotted tables, pulled from it with SQL as they stood at one moment in time; manipulation of those snapshots with Polars (or R, pandas, or Excel); and visualization with seaborn. This section is about the first step, the database.
#
# Data scientists use SQL in a few main ways:
#
# 1. Write a SQL query to get the initial dataset for an analysis, save it as a CSV (or JSON, or another format), and explore and analyze it with Polars.
# 2. Interact with the DBMS directly: write SQL queries to explore and analyze the data, save the final results to a CSV, and make figures and summaries with Polars or other tools.
# 3. Use an ORM (object-relational mapping), which translates Python code into SQL automatically. ORMs are most common in large software systems and less common in data science.
# 4. Write SQL queries that run automatically on a schedule, a semi-automated version of the second approach.
#
# Here is the first approach on a small scale. DuckDB is a DBMS that runs inside Python and keeps a whole database in a single file. `duckdb.connect` opens that file and returns a connection to it, and `pl.read_database` sends a SQL query over the connection and returns the result as a `DataFrame`. Opening the file with `read_only=True` means that nothing we do can change it. Writing queries of your own is the subject of the SQL chapters, so here we only fetch two whole tables.

# %% id="duckdb-read"
import duckdb

con = duckdb.connect("data/example_duck.db", read_only=True)
dragon = pl.read_database("SELECT * FROM dragon", con)
setting = pl.read_database("SELECT * FROM setting", con)

# %% [markdown] id="tables-schemas-keys"
# ## Tables, Schemas, and Keys
#
# ### SQL Terminology
#
# Here is the `dragon` table:

# %% id="dragon-show"
dragon

# %% [markdown] id="sql-terms"
# SQL has its own names for the parts of a table.
#
# * A table is also called a **relation**, and `dragon` is the relation's name.
# * A row is also called a **record** or a **tuple**.
# * A column is also called an **attribute** or a **field**.
#
# The `dragon` relation has 6 records, one per dragon, and 4 attributes: `name`, `yr`, `cute`, and `setting_id`.
#
# ### Table Schema
#
# Every column of a SQL table has three properties: a name, a type, and zero or more **constraints**, which are rules that every value in the column must obey. The schema of a `DataFrame` has only the first two.
#
# **English:** List each column of `dragon` with its type.

# %% id="dragon-schema"
dragon.schema

# %% [markdown] id="dragon-schema-sql"
# **SQL:**
# ```sql
# DESCRIBE dragon
# ```
#
# The Polars schema records names and types (`String` and `Int32`), and nothing else. In a database, whoever creates a table must declare its schema, which describes the logical structure of the table, and the constraints are part of that declaration. These are the two statements that created the tables in `example_duck.db`, with `setting` first because `dragon` refers to it:
#
# ```sql
# CREATE TABLE setting (
#     id         INTEGER PRIMARY KEY,
#     media      VARCHAR NOT NULL,
#     place      VARCHAR,
#     "type"     VARCHAR,
#     start_year INTEGER,
#     CHECK (start_year >= 1900)
# );
#
# CREATE TABLE dragon (
#     "name"     VARCHAR PRIMARY KEY,
#     yr         INTEGER,
#     cute       INTEGER,
#     setting_id INTEGER,
#     CHECK (yr >= 1900),
#     FOREIGN KEY (setting_id) REFERENCES setting(id)
# );
# ```
#
# Each line gives a column's name and type, then any constraints on it. `VARCHAR` is text, and `INTEGER` is a 32-bit integer, which is why Polars shows `i32`. (`name` and `type` are in double quotes because they are also SQL keywords.) The constraints are:
#
# * `PRIMARY KEY`: the column identifies each row. Every row must have a value, and no two rows may share one.
# * `NOT NULL`: every row must have a value, so a setting cannot be missing its `media`.
# * `CHECK (yr >= 1900)`: a dragon's year cannot be before 1900. `setting` has the same rule for `start_year`.
# * `FOREIGN KEY (setting_id) REFERENCES setting(id)`: each dragon's `setting_id` must be either null or an `id` that exists in `setting`.
#
# The database refuses any change that would break a constraint. That is the "guarantees on the data" advantage of a DBMS, written out in code.
#
# ### Why Multiple Tables?
#
# Suppose we want to know where each dragon comes from. That information lives in the `setting` table.

# %% id="setting-show"
setting

# %% [markdown] id="setting-read"
# `setting` has 5 rows, one per setting, identified by `id`. Each row records the title of the work the setting comes from (`media`), the `place`, the `type` of work, and the year the work first appeared (`start_year`). The setting with id 2, `IRL` ("in real life"), has no place and no start year.
#
# To attach each dragon's setting, we join the two tables, matching `dragon`'s `setting_id` with `setting`'s `id`. The key has a different name in each table, so instead of `on=` we name the left table's key with `left_on=` and the right table's with `right_on=`.
#
# **English:** For each dragon, attach its setting.

# %% id="dragon-setting-join"
dragon.join(setting, left_on="setting_id", right_on="id")

# %% [markdown] id="dragon-setting-join-sql"
# **SQL:**
# ```sql
# SELECT *
# FROM dragon INNER JOIN setting
#     ON dragon.setting_id = setting.id
# ```
#
# The result has 6 rows and 8 columns. Polars keeps `setting_id` and drops `id`, since the two are equal on every row, while the SQL result keeps both and has 9 columns.
#
# This wide table is what we would get by storing everything about dragons in one table, and it shows two problems with doing that.
#
# * **Redundant information.** drogon and rhaegal both come from Game of Thrones, so the table stores `Game of Thrones`, `Essos`, `tv show`, and `2011` twice. Every dragon from the same setting repeats all of that setting's information.
# * **Column bloat.** Half of the columns, `media`, `place`, `type`, and `start_year`, describe settings rather than dragons. As we add more about each setting, the table stops being about dragons at all.
#
# The solution is to split the information into several tables, store each fact once, and join the tables whenever an analysis needs them together.
#
# ### Primary and Foreign Keys
#
# A **primary key** is a column (or set of columns) that identifies each row of a table. The primary key of `dragon` is `name`, so no two dragons may share a name.
#
# **English:** Check that every dragon has a different name.

# %% id="dragon-key-check"
dragon["name"].n_unique(), dragon.height

# %% [markdown] id="keys"
# **SQL:**
# ```sql
# SELECT COUNT(DISTINCT name), COUNT(*)
# FROM dragon
# ```
#
# There are 6 distinct names in 6 rows. A check like this shows only that the rows we have are unique; the `PRIMARY KEY` constraint is what guarantees that no future row will repeat a name. A key can also span several columns. In the section on granularity, `school` and `city` together identified each row of `admissions`.
#
# The primary key of `setting` is `id`. A **foreign key** is a column that holds another table's primary keys. `setting_id` in `dragon` is a foreign key into `setting`: it records which setting each dragon comes from, without repeating any of that setting's information. Foreign keys are usually what we join on. The join above kept all 6 dragons. No dragon has a null `setting_id`, and the foreign-key constraint guarantees that every non-null `setting_id` appears as an `id` in `setting`. A dragon with a null `setting_id` would pass the constraint, and an inner join would drop it.

# %% [markdown] id="star-schema"
# ## Star Schema
#
# ```{image} images/star_schema_boba_fact_dimension.png
# :alt: A Products fact table with columns drink_id, topping_id and store_id. Each column is color-matched to a dimension table: Drinks (name, ice level, sweetness), Toppings (name) and Stores (store name, location). The fact table holds only keys, and the details live in the dimension tables.
# :width: 700
# ```
#
# To minimize redundant storage, databases often store data across fact and dimension tables. This arrangement is called a **star schema**, and the figure shows one for a group of boba shops.
#
# * The **fact table** is the central table, and it holds the information that links its entries to the dimension tables. It has few columns and many records. Here, `Products` holds only keys: `drink_id`, `topping_id`, and `store_id`.
# * Each **dimension table** holds more detailed information about one kind of fact. Dimension tables have more columns and fewer records. `Drinks` has each drink's name, ice level, and sweetness; `Toppings` has each topping's name; and `Stores` has each store's name and location.
#
# The fact table's granularity is every possible drink and topping combination across all stores, which makes for many rows. With the 3 drinks, 3 toppings, and 3 stores in the figure, there are 3 × 3 × 3 = 27 combinations: the cross join of the three dimension tables' keys. To see a drink's name next to the location of a store that sells it, we join `Products` with `Drinks` on `drink_id` and with `Stores` on `store_id`. Each description is stored once, and joins bring together whatever an analysis needs.

# %% [markdown] id="parting-note"
# ## Parting Note
#
# Structure, granularity, temporality, and faithfulness are questions to carry into any dataset. What shape is the data in, and what does one row represent? When was it recorded, and in which time zone? Does it reflect reality, and how are its missing values encoded? The SQL chapters pick up where the database sections left off, with writing queries against a database directly.
