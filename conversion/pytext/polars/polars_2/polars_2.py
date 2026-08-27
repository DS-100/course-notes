# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: venv
#     language: python
#     name: python3
# ---

# %% [markdown] id="p2-intro"
# ---
# title: Polars II
# ---
#
# ::: {note} Learning Outcomes
# * Aggregate rows into groups using `.group_by()` and `.agg()`
# * Write aggregations as expressions, including ones of your own design
# * Select rows by a property of the group they belong to using `.over()`
# * Restructure a grouped result with `.pivot()`
# * Combine two `DataFrame`s with `.join()`
# :::
#
# We will introduce the idea of aggregating data: gathering rows that belong together, then computing a single summary value for each collection of rows. We'll work through the aggregation functions Polars offers, write a couple of our own, and use grouping to answer questions that no individual row of a table can answer. We'll then pick up two more tools for rearranging and combining tables: pivot tables and joins.
#
# First, let's load the `babynames` dataset.
#
# ````{dropdown} Click to see the code
# :open: false
# ```python
# # This code pulls census data and loads it into a DataFrame
# # We won't cover it explicitly in this class, but you are welcome to explore it on your own
# import polars as pl
# import plotly.express as px
# import urllib.request
# import os.path
# import zipfile
#
# data_url = "https://www.ssa.gov/oact/babynames/state/namesbystate.zip"
# local_filename = "data/babynamesbystate.zip"
# if not os.path.exists(local_filename): # If the data exists don't download again
#     with urllib.request.urlopen(data_url) as resp, open(local_filename, 'wb') as f:
#         f.write(resp.read())
#
# zf = zipfile.ZipFile(local_filename, 'r')
#
# ca_name = 'STATE.CA.TXT'
# field_names = ['State', 'Sex', 'Year', 'Name', 'Count']
# with zf.open(ca_name) as fh:
#     babynames = pl.read_csv(fh, has_header=False, new_columns=field_names)
#
# babynames.head()
# ```
# ````


# %% [markdown]

# %% tags=["remove-input"] id="p2-load-babynames"
# This code pulls census data and loads it into a DataFrame
# We won't cover it explicitly in this class, but you are welcome to explore it on your own
import polars as pl
import plotly.express as px
import urllib.request
import os.path
import zipfile

data_url = "https://www.ssa.gov/oact/babynames/state/namesbystate.zip"
local_filename = "data/babynamesbystate.zip"
if not os.path.exists(local_filename): # If the data exists don't download again
    with urllib.request.urlopen(data_url) as resp, open(local_filename, 'wb') as f:
        f.write(resp.read())

zf = zipfile.ZipFile(local_filename, 'r')

ca_name = 'STATE.CA.TXT'
field_names = ['State', 'Sex', 'Year', 'Name', 'Count']
with zf.open(ca_name) as fh:
    babynames = pl.read_csv(fh, has_header=False, new_columns=field_names)

babynames.head()

# %% [markdown] id="p2-groupby-intro"
# ## Aggregating Data with `group_by`
#
# Up until this point, we have been working with individual rows of `DataFrame`s. As data scientists, we often wish to investigate trends across a larger *subset* of our data. We may want to compute some summary statistic (the mean, the median, the sum) for a whole collection of rows at once. The rows of `babynames` record one name, in one year, for one sex; a question like "how many babies were born in California in 1990?" is not answered by any single row.
#
# The tool for this is `.group_by` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.group_by.html). We tell it which column holds the value that decides who belongs with whom. Let's gather all rows in `babynames` that share a year.

# %% id="p2-groupby-object"
babynames.group_by("Year")

# %% [markdown] id="p2-groupby-explain"
# That output is not a table. Calling `.group_by` produces a `GroupBy` object, which you can picture as a set of "mini", grouped sub-`DataFrame`s, where each sub-`DataFrame` holds all of the rows from `babynames` that correspond to one particular year.
#
# The diagram below shows a simplified view of `babynames` to help illustrate the idea.
#
# ```{image} images/gb.png
# :alt: A DataFrame whose rows are regrouped by the value of one column, producing one sub-table per distinct value.
# :width: 600
# ```
#
# A `GroupBy` object holds the groups, but it has not computed anything yet. To get numbers back out, we call `.agg` and hand it one or more *aggregation expressions*. Each expression is applied to every group in turn, and each one collapses a column of the group down to a single value. Let's find the `sum` of all counts for each year, which is the number of babies born in California in that year.

# %% tags=["remove-input", "remove-output"] id="p2-agg-unsorted"
babynames.group_by("Year").agg(pl.col("Count").sum()).head(5)


# %% [markdown]
# <!-- tab-twins:begin babynames.group_by("Year").agg(pl.col("Count").sum()).head(5) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# babynames.group_by("Year").agg(pl.col("Count").sum()).head(5)
# ```
#
# ```text
# shape: (5, 2)
# ┌──────┬────────┐
# │ Year ┆ Count  │
# │ ---  ┆ ---    │
# │ i64  ┆ i64    │
# ╞══════╪════════╡
# │ 1971 ┆ 310020 │
# │ 1977 ┆ 315011 │
# │ 1992 ┆ 541054 │
# │ 1980 ┆ 365973 │
# │ 1983 ┆ 394608 │
# └──────┴────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd.groupby("Year")["Count"].sum().head(5)
# ```
#
# ```text
# Year
# 1910     9163
# 1911     9983
# 1912    17946
# 1913    22094
# 1914    26926
# Name: Count, dtype: int64
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-agg-order-warning"
# We get one row per group: a `Year` column holding the key that defined the group, and a `Count` column holding that group's sum. The column keeps the name of the column it was computed from.
#
# Look closely at the years, though. They are not in order, and running the cell again may well hand you a different five.
#
# ::: {warning} Groups come back in no particular order
# Polars builds groups in parallel and returns them in whatever order they finish, so a grouped result carries no ordering guarantee at all. Sort it whenever the order matters: before plotting, before a `.head()`, and before writing a sentence about "the first few years". Passing `maintain_order=True` to `.group_by` is the alternative: it returns groups in the order their keys first appear in the data, at some cost in speed.
# :::
#
# Sorting the result gives us a table we can read from top to bottom.

# %% tags=["remove-input", "remove-output"] id="p2-agg-sorted"
babies_by_year = babynames.group_by("Year").agg(pl.col("Count").sum()).sort("Year")
babies_by_year.head(5)


# %% [markdown]
# <!-- tab-twins:begin babies_by_year = babynames.group_by("Year").agg(pl.col("Count").sum()).sort("Year") -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# babies_by_year = babynames.group_by("Year").agg(pl.col("Count").sum()).sort("Year")
# babies_by_year.head(5)
# ```
#
# ```text
# shape: (5, 2)
# ┌──────┬───────┐
# │ Year ┆ Count │
# │ ---  ┆ ---   │
# │ i64  ┆ i64   │
# ╞══════╪═══════╡
# │ 1910 ┆ 9163  │
# │ 1911 ┆ 9983  │
# │ 1912 ┆ 17946 │
# │ 1913 ┆ 22094 │
# │ 1914 ┆ 26926 │
# └──────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd.groupby("Year")["Count"].sum().head(5)
# ```
#
# ```text
# Year
# 1910     9163
# 1911     9983
# 1912    17946
# 1913    22094
# 1914    26926
# Name: Count, dtype: int64
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-agg-diagram"
# The data begins in 1910, when 9,163 babies were born in California, and the counts climb quickly from there. We can relate this back to the diagram we used above. Remember that the diagram uses a simplified version of `babynames`, which is why its summed counts are so much smaller.
#
# ```{image} images/agg.png
# :alt: Grouped sub-tables each collapsed by a sum into a single row, which are then stacked into one output table.
# :width: 600
# ```
#
# ### Aggregation Functions
#
# An aggregation function takes a column belonging to one group and returns a single value for it. Polars writes these as expressions [(documentation)](https://docs.pola.rs/api/python/stable/reference/expressions/aggregation.html), and the common ones read exactly as they sound:
#
# * `pl.col("c").sum()`, `.mean()`, `.median()`
# * `pl.col("c").min()`, `.max()`
# * `pl.col("c").first()`, `.last()`
# * `pl.col("c").n_unique()`
# * `pl.len()`, the number of rows in the group
#
# Here is the smallest number of babies given each name in any single year.

# %% tags=["remove-input", "remove-output"] id="p2-agg-min"
# What is the minimum count for each name in any year?
babynames.group_by("Name").agg(pl.col("Count").min()).sort("Name").head()


# %% [markdown]
# <!-- tab-twins:begin babynames.group_by("Name").agg(pl.col("Count").min()).sort("Name").head() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # What is the minimum count for each name in any year?
# babynames.group_by("Name").agg(pl.col("Count").min()).sort("Name").head()
# ```
#
# ```text
# shape: (5, 2)
# ┌─────────┬───────┐
# │ Name    ┆ Count │
# │ ---     ┆ ---   │
# │ str     ┆ i64   │
# ╞═════════╪═══════╡
# │ Aadan   ┆ 5     │
# │ Aadarsh ┆ 6     │
# │ Aaden   ┆ 10    │
# │ Aadhav  ┆ 6     │
# │ Aadhini ┆ 6     │
# └─────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd.groupby("Name")["Count"].min().sort_index().head()
# ```
#
# ```text
# Name
# Aadan       5
# Aadarsh     6
# Aaden      10
# Aadhav      6
# Aadhini     6
# Name: Count, dtype: int64
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-agg-multiple"
# One `.agg` call can carry as many expressions as we like, and `.alias` [(documentation)](https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.alias.html) gives each result a name. Without it, three aggregations of `Count` would all want to be called `Count`.

# %% tags=["remove-input", "remove-output"] id="p2-agg-multiple-code"
babynames.group_by("Name").agg(
    pl.col("Count").min().alias("Min Count"),
    pl.col("Count").max().alias("Max Count"),
    pl.col("Count").mean().alias("Mean Count"),
    pl.len().alias("Years Recorded"),
).sort("Name").head()


# %% [markdown]
# <!-- tab-twins:begin pl.col("Count").mean().alias("Mean Count"), -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# babynames.group_by("Name").agg(
#     pl.col("Count").min().alias("Min Count"),
#     pl.col("Count").max().alias("Max Count"),
#     pl.col("Count").mean().alias("Mean Count"),
#     pl.len().alias("Years Recorded"),
# ).sort("Name").head()
# ```
#
# ```text
# shape: (5, 5)
# ┌─────────┬───────────┬───────────┬────────────┬────────────────┐
# │ Name    ┆ Min Count ┆ Max Count ┆ Mean Count ┆ Years Recorded │
# │ ---     ┆ ---       ┆ ---       ┆ ---        ┆ ---            │
# │ str     ┆ i64       ┆ i64       ┆ f64        ┆ u32            │
# ╞═════════╪═══════════╪═══════════╪════════════╪════════════════╡
# │ Aadan   ┆ 5         ┆ 7         ┆ 6.0        ┆ 3              │
# │ Aadarsh ┆ 6         ┆ 6         ┆ 6.0        ┆ 1              │
# │ Aaden   ┆ 10        ┆ 158       ┆ 46.214286  ┆ 14             │
# │ Aadhav  ┆ 6         ┆ 8         ┆ 6.75       ┆ 4              │
# │ Aadhini ┆ 6         ┆ 6         ┆ 6.0        ┆ 1              │
# └─────────┴───────────┴───────────┴────────────┴────────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd.groupby("Name")["Count"].agg(
#     **{"Min Count": "min", "Max Count": "max", "Mean Count": "mean",
#        "Years Recorded": "size"}
# ).sort_index().head()
# ```
#
# ```text
#          Min Count  Max Count  Mean Count  Years Recorded
# Name
# Aadan            5          7    6.000000               3
# Aadarsh          6          6    6.000000               1
# Aaden           10        158   46.214286              14
# Aadhav           6          8    6.750000               4
# Aadhini          6          6    6.000000               1
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-first-last"
# The name "Aaden" is a good illustration of what these four numbers buy us: it appears in 14 different years, with counts ranging from 10 to 158.
#
# `.first()` and `.last()` are a little different from the rest, because they select a value rather than compute one. They are what we want when every row of a group carries the same value in some column, and we want that value carried through to the output. To see this, let's add a column to `babynames` holding the first letter of each name.
#
# ```{image} images/first.png
# :alt: Grouped sub-tables reduced to one row each by taking the first entry of a column.
# :width: 500
# ```

# %% tags=["remove-input", "remove-output"] id="p2-first-letter"
# Imagine we had an additional column, "First Letter". We'll explain string methods like this one in a later chapter
babynames_new = babynames.with_columns(
    pl.col("Name").str.slice(0, 1).alias("First Letter")
).select(["Name", "First Letter", "Year"])

babynames_new.head()


# %% [markdown]
# <!-- tab-twins:begin pl.col("Name").str.slice(0, 1).alias("First Letter") -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Imagine we had an additional column, "First Letter". We'll explain string methods like this one in a later chapter
# babynames_new = babynames.with_columns(
#     pl.col("Name").str.slice(0, 1).alias("First Letter")
# ).select(["Name", "First Letter", "Year"])
#
# babynames_new.head()
# ```
#
# ```text
# shape: (5, 3)
# ┌──────────┬──────────────┬──────┐
# │ Name     ┆ First Letter ┆ Year │
# │ ---      ┆ ---          ┆ ---  │
# │ str      ┆ str          ┆ i64  │
# ╞══════════╪══════════════╪══════╡
# │ Mary     ┆ M            ┆ 1910 │
# │ Helen    ┆ H            ┆ 1910 │
# │ Dorothy  ┆ D            ┆ 1910 │
# │ Margaret ┆ M            ┆ 1910 │
# │ Frances  ┆ F            ┆ 1910 │
# └──────────┴──────────────┴──────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # Imagine we had an additional column, "First Letter".
# babynames_new_pd = babynames_pd.assign(
#     **{"First Letter": babynames_pd["Name"].str[0]}
# )[["Name", "First Letter", "Year"]]
#
# babynames_new_pd.head()
# ```
#
# ```text
#        Name First Letter  Year
# 0      Mary            M  1910
# 1     Helen            H  1910
# 2   Dorothy            D  1910
# 3  Margaret            M  1910
# 4   Frances            F  1910
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-first-letter-explain"
# If we form one group per name, `"First Letter"` is identical for every row of the group. Taking the first entry therefore represents the whole group faithfully, while a different column can be aggregated a different way in the same call.

# %% tags=["remove-input", "remove-output"] id="p2-first-letter-agg"
babynames_new.group_by("Name").agg(
    pl.col("First Letter").first(),
    pl.col("Year").max(),
).sort("Name").head()


# %% [markdown]
# <!-- tab-twins:begin pl.col("First Letter").first(), -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# babynames_new.group_by("Name").agg(
#     pl.col("First Letter").first(),
#     pl.col("Year").max(),
# ).sort("Name").head()
# ```
#
# ```text
# shape: (5, 3)
# ┌─────────┬──────────────┬──────┐
# │ Name    ┆ First Letter ┆ Year │
# │ ---     ┆ ---          ┆ ---  │
# │ str     ┆ str          ┆ i64  │
# ╞═════════╪══════════════╪══════╡
# │ Aadan   ┆ A            ┆ 2014 │
# │ Aadarsh ┆ A            ┆ 2019 │
# │ Aaden   ┆ A            ┆ 2020 │
# │ Aadhav  ┆ A            ┆ 2019 │
# │ Aadhini ┆ A            ┆ 2022 │
# └─────────┴──────────────┴──────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_new_pd.groupby("Name").agg(
#     **{"First Letter": ("First Letter", "first"), "Year": ("Year", "max")}
# ).sort_index().head()
# ```
#
# ```text
#         First Letter  Year
# Name
# Aadan              A  2014
# Aadarsh            A  2019
# Aaden              A  2020
# Aadhav             A  2019
# Aadhini            A  2022
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-count-intro"
# ### Counting Rows in Each Group
#
# Often the question is simply how many rows fall into each group. `.len()` answers it directly, with no column to name. Let's work with a small `DataFrame` where we can see every row at once.

# %% tags=["remove-input", "remove-output"] id="p2-count-df"
df = pl.DataFrame({"letter": ["A", "A", "B", "C", "C", "C"],
                   "num": [1, 2, 3, 4, None, 4],
                   "state": [None, "tx", "fl", "hi", None, "ak"]})
df


# %% [markdown]
# <!-- tab-twins:begin df = pl.DataFrame({"letter": ["A", "A", "B", "C", "C", "C"], -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# df = pl.DataFrame({"letter": ["A", "A", "B", "C", "C", "C"],
#                    "num": [1, 2, 3, 4, None, 4],
#                    "state": [None, "tx", "fl", "hi", None, "ak"]})
# df
# ```
#
# ```text
# shape: (6, 3)
# ┌────────┬──────┬───────┐
# │ letter ┆ num  ┆ state │
# │ ---    ┆ ---  ┆ ---   │
# │ str    ┆ i64  ┆ str   │
# ╞════════╪══════╪═══════╡
# │ A      ┆ 1    ┆ null  │
# │ A      ┆ 2    ┆ tx    │
# │ B      ┆ 3    ┆ fl    │
# │ C      ┆ 4    ┆ hi    │
# │ C      ┆ null ┆ null  │
# │ C      ┆ 4    ┆ ak    │
# └────────┴──────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# df_pd = pd.DataFrame({"letter": ["A", "A", "B", "C", "C", "C"],
#                       "num": [1, 2, 3, 4, None, 4],
#                       "state": [None, "tx", "fl", "hi", None, "ak"]})
# df_pd
# ```
#
# ```text
#   letter  num state
# 0      A  1.0  None
# 1      A  2.0    tx
# 2      B  3.0    fl
# 3      C  4.0    hi
# 4      C  NaN  None
# 5      C  4.0    ak
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-count-nulls"
# Three of these entries are missing. Polars prints a missing value as `null`, and prints it in place rather than dropping the row.

# %% tags=["remove-input", "remove-output"] id="p2-count-len"
df.group_by("letter", maintain_order=True).len()


# %% [markdown]
# <!-- tab-twins:begin df.group_by("letter", maintain_order=True).len() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# df.group_by("letter", maintain_order=True).len()
# ```
#
# ```text
# shape: (3, 2)
# ┌────────┬─────┐
# │ letter ┆ len │
# │ ---    ┆ --- │
# │ str    ┆ u32 │
# ╞════════╪═════╡
# │ A      ┆ 2   │
# │ B      ┆ 1   │
# │ C      ┆ 3   │
# └────────┴─────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# df_pd.groupby("letter", sort=False).size()
# ```
#
# ```text
# letter
# A    2
# B    1
# C    3
# dtype: int64
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-count-len-explain"
# We get one row per group: the `letter` we grouped by, alongside a `len` column giving the number of rows in that group. Missing values are counted like any other row, so `C` has three. Because we asked for `maintain_order=True`, the letters arrive in the order they first appear in `df`.
#
# A related question is how much data each column actually holds. `pl.all()` stands for every column we did not group by, and `.count()` counts the values that are not missing.

# %% tags=["remove-input", "remove-output"] id="p2-count-all"
df.group_by("letter", maintain_order=True).agg(pl.all().count())


# %% [markdown]
# <!-- tab-twins:begin df.group_by("letter", maintain_order=True).agg(pl.all().count()) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# df.group_by("letter", maintain_order=True).agg(pl.all().count())
# ```
#
# ```text
# shape: (3, 3)
# ┌────────┬─────┬───────┐
# │ letter ┆ num ┆ state │
# │ ---    ┆ --- ┆ ---   │
# │ str    ┆ u32 ┆ u32   │
# ╞════════╪═════╪═══════╡
# │ A      ┆ 2   ┆ 1     │
# │ B      ┆ 1   ┆ 1     │
# │ C      ┆ 2   ┆ 2     │
# └────────┴─────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# df_pd.groupby("letter", sort=False).count()
# ```
#
# ```text
#         num  state
# letter
# A         2      1
# B         1      1
# C         2      2
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-count-vs-value-counts"
# These counts differ from `.len()`, and from each other. Group `C` occupies three rows but carries only two recorded numbers and two recorded states, and group `A` occupies two rows but carries only one recorded state.
#
# You may recall `.value_counts()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/series/api/polars.Series.value_counts.html) from the previous chapter. It reports the same tallies as `.group_by().len()`.

# %% tags=["remove-input", "remove-output"] id="p2-value-counts"
df["letter"].value_counts(sort=True)


# %% [markdown]
# <!-- tab-twins:begin df["letter"].value_counts(sort=True) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# df["letter"].value_counts(sort=True)
# ```
#
# ```text
# shape: (3, 2)
# ┌────────┬───────┐
# │ letter ┆ count │
# │ ---    ┆ ---   │
# │ str    ┆ u32   │
# ╞════════╪═══════╡
# │ C      ┆ 3     │
# │ A      ┆ 2     │
# │ B      ┆ 1     │
# └────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# df_pd["letter"].value_counts()
# ```
#
# ```text
# letter
# C    3
# A    2
# B    1
# Name: count, dtype: int64
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-value-counts-explain"
# Two small differences are worth remembering. `.value_counts()` names its second column `count` rather than `len`, and it is a `Series` method, so it works on one column at a time. Like a grouped result, its rows have no guaranteed order unless you ask for one; `sort=True` ranks the letters from most to least common.
#
# ### Plotting Birth Counts
#
# We already have the total number of babies born in each year in `babies_by_year`, sorted by year. Here's an illustration of how we got there:
#
# ```{image} images/aggregation.png
# :alt: A table split into groups, each group reduced by an aggregation to a single value, and the values collected into one summary table.
# :width: 600
# ```
#
# Plotting that table tells an interesting story.
#
# ````{dropdown} Click to see the code
# :open: false
# ```python
# #| fig-alt: A line plot of total California births per year from 1910 to 2022. The line climbs steeply through the century to a peak above 550,000 births around 1990, then declines to roughly 360,000 by 2022.
# fig = px.line(babies_by_year, x="Year", y="Count")
# fig.update_layout(font_size=18, autosize=False, width=700, height=400)
# fig
# ```
# ````

# %% tags=["remove-input"] id="p2-plot-births"
#| fig-alt: A line plot of total California births per year from 1910 to 2022. The line climbs steeply through the century to a peak above 550,000 births around 1990, then declines to roughly 360,000 by 2022.
fig = px.line(babies_by_year, x="Year", y="Count")
fig.update_layout(font_size=18, autosize=False, width=700, height=400)
fig

# %% [markdown] id="p2-plot-warning"
# **A word of warning**: we made an enormous assumption when we decided to use this dataset to estimate birth rate. According to [this article from the Legislative Analyst's Office](https://lao.ca.gov/LAOEconTax/Article/Detail/691), the true number of babies born in California in 2020 was 421,275. Our table shows 362,882 for that year — what happened?
#
# ### Summary of `group_by()`
#
# A grouping operation involves some combination of **splitting a `DataFrame` into grouped sub-frames**, **applying a function**, and **combining the results**.
#
# For the code `babynames.group_by("Year").agg(pl.col("Count").sum())`, Polars:
#
# - **Splits** `babynames` into sub-`DataFrame`s whose rows all belong to the same year.
# - **Applies** the expression `pl.col("Count").sum()` to each sub-`DataFrame`.
# - **Combines** the results into a single `DataFrame` with one row per year: the year, and its total.
#
# ```{image} images/groupby_demo.png
# :alt: A table split into sub-tables by key, a function applied to each sub-table, and the single-row results combined into one output table.
# :width: 600
# ```
#
# ## Ratio to Peak: A Metric of Our Own
#
# The aggregations above are all built in. Nothing stops us from inventing our own, because an aggregation is just an expression that ends in a single value per group.
#
# Say we want to find the name with sex "F" that has fallen furthest out of favor in California. We need a definition of "fallen out of favor" before we can compute anything, so let's define one: the **ratio to peak** (RTP) of a name is the number of babies given that name in the most recent year it appears, divided by the largest number given that name in *any* year. A name at its all-time peak has an RTP of 1; a name that has all but vanished has an RTP near 0.
#
# Let's work it out for one name first. We start by narrowing `babynames` to sex "F" and sorting by year, so that rows run from oldest to most recent.

# %% tags=["remove-input", "remove-output"] id="p2-f-babynames"
f_babynames = babynames.filter(pl.col("Sex") == "F").sort("Year")
f_babynames.head()


# %% [markdown]
# <!-- tab-twins:begin f_babynames = babynames.filter(pl.col("Sex") == "F").sort("Year") -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# f_babynames = babynames.filter(pl.col("Sex") == "F").sort("Year")
# f_babynames.head()
# ```
#
# ```text
# shape: (5, 5)
# ┌───────┬─────┬──────┬──────────┬───────┐
# │ State ┆ Sex ┆ Year ┆ Name     ┆ Count │
# │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   │
# │ str   ┆ str ┆ i64  ┆ str      ┆ i64   │
# ╞═══════╪═════╪══════╪══════════╪═══════╡
# │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   │
# │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   │
# │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   │
# │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   │
# │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   │
# └───────┴─────┴──────┴──────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# f_babynames_pd = babynames_pd[babynames_pd["Sex"] == "F"].sort_values("Year")
# f_babynames_pd.head()
# ```
#
# ```text
#     State Sex  Year     Name  Count
# 0      CA   F  1910     Mary    295
# 148    CA   F  1910    Merle      9
# 149    CA   F  1910  Rosalie      9
# 150    CA   F  1910    Rosie      9
# 151    CA   F  1910   Teresa      9
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-jennifer-intro"
# Now we can pull out the counts for "Jennifer" and compare the most recent one to the largest.

# %% tags=["remove-input", "remove-output"] id="p2-jennifer"
# The number of Jennifers born in CA in each year, oldest first
jenn_counts = f_babynames.filter(pl.col("Name") == "Jennifer")["Count"]

max_jenn = jenn_counts.max()      # the most Jennifers born in any one year
latest_jenn = jenn_counts.last()  # the most recent year's count

latest_jenn / max_jenn


# %% [markdown]
# <!-- tab-twins:begin latest_jenn / max_jenn -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # The number of Jennifers born in CA in each year, oldest first
# jenn_counts = f_babynames.filter(pl.col("Name") == "Jennifer")["Count"]
#
# max_jenn = jenn_counts.max()      # the most Jennifers born in any one year
# latest_jenn = jenn_counts.last()  # the most recent year's count
#
# latest_jenn / max_jenn
# ```
#
# ```text
# 0.018796372629843364
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# jenn_pd = f_babynames_pd[f_babynames_pd["Name"] == "Jennifer"]["Count"]
# max_jenn_pd = jenn_pd.max()
# latest_jenn_pd = jenn_pd.iloc[-1]
# latest_jenn_pd / max_jenn_pd
# ```
#
# ```text
# 0.018796372629843364
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-jennifer-explain"
# At its peak, 6,065 Jennifers were born in a single year; in 2022 there were 114, giving an RTP of about 0.019. Note how much work the sort is doing here: `.last()` means "the final row", and it is only the most recent year because we sorted `f_babynames` by `Year` first.
#
# The whole calculation is one expression, so we can hand it to `.agg` and get an answer for every name at once. Rows keep their relative order inside a group, so `pl.col("Count").last()` picks out the most recent year for each name.

# %% tags=["remove-input", "remove-output"] id="p2-rtp-table"
rtp_table = f_babynames.group_by("Name").agg(
    (pl.col("Count").last() / pl.col("Count").max()).alias("Count RTP")
)
rtp_table.sort("Name").head()


# %% [markdown]
# <!-- tab-twins:begin rtp_table = f_babynames.group_by("Name").agg( -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# rtp_table = f_babynames.group_by("Name").agg(
#     (pl.col("Count").last() / pl.col("Count").max()).alias("Count RTP")
# )
# rtp_table.sort("Name").head()
# ```
#
# ```text
# shape: (5, 2)
# ┌─────────┬───────────┐
# │ Name    ┆ Count RTP │
# │ ---     ┆ ---       │
# │ str     ┆ f64       │
# ╞═════════╪═══════════╡
# │ Aadhini ┆ 1.0       │
# │ Aadhira ┆ 0.5       │
# │ Aadhya  ┆ 0.66      │
# │ Aadya   ┆ 0.586207  │
# │ Aahana  ┆ 0.269231  │
# └─────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# rtp_pd = f_babynames_pd.groupby("Name")["Count"].agg(
#     **{"Count RTP": lambda s: s.iloc[-1] / s.max()}
# )
# rtp_pd.sort_index().head()
# ```
#
# ```text
#          Count RTP
# Name
# Aadhini   1.000000
# Aadhira   0.500000
# Aadhya    0.660000
# Aadya     0.586207
# Aahana    0.269231
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-rtp-explain"
# One row for each of the 13,782 names with sex "F" in the data. This is the Polars version of logic you saw in Data 8, and much of what you learned there will serve you well here.
#
# ### Nuisance Columns
#
# You may hear a column that an aggregation cannot handle called a *nuisance column*, a column of names handed to a sum being the classic case. Nothing of the sort happened above, because `.agg` never has to guess. We wrote `pl.col("Count")` into the expression, so `Count` is the only column that got divided, and every other column of `f_babynames` was simply not part of the question.
#
# The one thing to watch for is asking for an aggregation across *every* column at once. `f_babynames.group_by("Name").agg(pl.all().sum())` reaches the `State` and `Sex` columns, which hold text, and summing text is not something Polars will invent an answer for. It stops with `` InvalidOperationError: `sum` operation not supported for dtype `str` ``, naming both the operation and the type it could not apply it to.
#
# Not every aggregation is so strict. `pl.all().mean()` over the same frame runs without complaint and simply leaves `null` in the text columns, which is the more dangerous of the two behaviours: nothing tells you a column was meaningless until you read the result.
#
# Naming the columns you mean, rather than reaching for `pl.all()`, avoids the question entirely.
#
# ### Renaming Columns After Grouping
#
# We already named the output column: `.alias("Count RTP")` sits inside the `.agg` call, so the column arrives with the right name and there is no clean-up step. Reserve `.rename({"old": "new"})` for columns you did not compute yourself, such as those that came in with the file.
#
# ### Custom Aggregation Functions
#
# Sometimes a metric arrives as a Python function rather than as an expression, out of a colleague's script or a library you don't control. `.map_batches` [(documentation)](https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.map_batches.html) hands each group's column to that function as a `Series` and puts the result back in the output. `returns_scalar=True` tells Polars the function collapses the group to one value.

# %% tags=["remove-input", "remove-output"] id="p2-map-batches"
def ratio_to_peak(series):
    """Ratio of the most recent count to the largest count."""
    return series.last() / series.max()

f_babynames.group_by("Name").agg(
    pl.col("Count")
      .map_batches(ratio_to_peak, return_dtype=pl.Float64, returns_scalar=True)
      .alias("Count RTP")
).sort("Count RTP").head()


# %% [markdown]
# <!-- tab-twins:begin def ratio_to_peak(series): -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# def ratio_to_peak(series):
#     """Ratio of the most recent count to the largest count."""
#     return series.last() / series.max()
#
# f_babynames.group_by("Name").agg(
#     pl.col("Count")
#       .map_batches(ratio_to_peak, return_dtype=pl.Float64, returns_scalar=True)
#       .alias("Count RTP")
# ).sort("Count RTP").head()
# ```
#
# ```text
# shape: (5, 2)
# ┌────────┬───────────┐
# │ Name   ┆ Count RTP │
# │ ---    ┆ ---       │
# │ str    ┆ f64       │
# ╞════════╪═══════════╡
# │ Debra  ┆ 0.00126   │
# │ Debbie ┆ 0.002815  │
# │ Carol  ┆ 0.00318   │
# │ Tammy  ┆ 0.003249  │
# │ Susan  ┆ 0.003305  │
# └────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# def ratio_to_peak_pd(series):
#     """Ratio of the most recent count to the largest count."""
#     return series.iloc[-1] / series.max()
#
# f_babynames_pd.groupby("Name")["Count"].agg(
#     **{"Count RTP": ratio_to_peak_pd}
# ).sort_values("Count RTP").head()
# ```
#
# ```text
#         Count RTP
# Name
# Debra    0.001260
# Debbie   0.002815
# Carol    0.003180
# Tammy    0.003249
# Susan    0.003305
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-map-caveat"
# Same names, same numbers. The difference is in what runs: the expression version computes all 13,782 ratios in one pass through the data, while this version calls a Python function 13,782 times. Its per-value counterpart, `.map_elements` [(documentation)](https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.map_elements.html), calls Python once per *value* and is slower still — when it can see an expression that would do the same job, Polars raises a `PolarsInefficientMapWarning` telling you which one. Write the expression when you can, and keep these two for the functions that are not yours to rewrite.
#
# ### Some Data Science Payoff
#
# Sorting `rtp_table` finally answers our question: which names have fallen the furthest?

# %% tags=["remove-input", "remove-output"] id="p2-rtp-sorted"
rtp_table.sort("Count RTP").head()


# %% [markdown]
# <!-- tab-twins:begin rtp_table.sort("Count RTP").head() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# rtp_table.sort("Count RTP").head()
# ```
#
# ```text
# shape: (5, 2)
# ┌────────┬───────────┐
# │ Name   ┆ Count RTP │
# │ ---    ┆ ---       │
# │ str    ┆ f64       │
# ╞════════╪═══════════╡
# │ Debra  ┆ 0.00126   │
# │ Debbie ┆ 0.002815  │
# │ Carol  ┆ 0.00318   │
# │ Tammy  ┆ 0.003249  │
# │ Susan  ┆ 0.003305  │
# └────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# rtp_pd.sort_values("Count RTP").head()
# ```
#
# ```text
#         Count RTP
# Name
# Debra    0.001260
# Debbie   0.002815
# Carol    0.003180
# Tammy    0.003249
# Susan    0.003305
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-rtp-sorted-explain"
# "Debra" tops the list at an RTP of 0.00126. It peaked in 1955 at 3,969 babies and last appears in the data in 2016, with 5.
#
# ::: {tip} Sorting, and where the nulls go
# `.sort()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.sort.html) orders from smallest to largest; pass `descending=True` for the other direction. It also places nulls at the *front* of the result, so whenever a sort feeds a `.head()` (any "top ten"), pass `nulls_last=True` to keep missing values from crowding out real answers.
# :::
#
# Let's look at the decline of "Debra".
#
# ````{dropdown} Click to see the code
# :open: false
# ```python
# #| fig-alt: A line plot of the number of babies named Debra born in California each year. The line rises to a peak of nearly 4,000 in the mid-1950s, falls steadily after 1960, and is indistinguishable from zero on this scale by the 1990s.
# fig = px.line(f_babynames.filter(pl.col("Name") == "Debra"), x="Year", y="Count")
# fig.update_layout(font_size=18, autosize=False, width=1000, height=400)
# fig
# ```
# ````

# %% tags=["remove-input"] id="p2-plot-debra"
#| fig-alt: A line plot of the number of babies named Debra born in California each year. The line rises to a peak of nearly 4,000 in the mid-1950s, falls steadily after 1960, and is indistinguishable from zero on this scale by the 1990s.
fig = px.line(f_babynames.filter(pl.col("Name") == "Debra"), x="Year", y="Count")
fig.update_layout(font_size=18, autosize=False, width=1000, height=400)
fig

# %% [markdown] id="p2-top10-intro"
# The names are an ordinary column of `rtp_table`, so we can read the ten biggest fallers straight out of it.

# %% tags=["remove-input", "remove-output"] id="p2-top10"
top10 = rtp_table.sort("Count RTP").head(10)["Name"].to_list()
top10


# %% [markdown]
# <!-- tab-twins:begin top10 = rtp_table.sort("Count RTP").head(10)["Name"].to_list() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# top10 = rtp_table.sort("Count RTP").head(10)["Name"].to_list()
# top10
# ```
#
# ```text
# ['Debra',
#  'Debbie',
#  'Carol',
#  'Tammy',
#  'Susan',
#  'Cheryl',
#  'Shannon',
#  'Tina',
#  'Michele',
#  'Terri']
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# top10_pd = rtp_pd.sort_values("Count RTP").head(10).index.tolist()
# top10_pd
# ```
#
# ```text
# ['Debra', 'Debbie', 'Carol', 'Tammy', 'Susan', 'Cheryl', 'Shannon', 'Tina', 'Michele', 'Terri']
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-top10-plot-intro"
# Plotting all ten together shows how much they have in common.
#
# ````{dropdown} Click to see the code
# :open: false
# ```python
# #| fig-alt: Ten line plots on shared axes, one per name. Every line rises to a peak somewhere between the late 1940s and 1970 and then falls away to near zero, with Debra and Susan reaching the highest peaks at just under 4,000 babies a year.
# fig = px.line(
#     f_babynames.filter(pl.col("Name").is_in(top10)),
#     x="Year",
#     y="Count",
#     color="Name",
# )
# fig.update_layout(font_size=18, autosize=False, width=1000, height=400)
# fig
# ```
# ````

# %% tags=["remove-input"] id="p2-plot-top10"
#| fig-alt: Ten line plots on shared axes, one per name. Every line rises to a peak somewhere between the late 1940s and 1970 and then falls away to near zero, with Debra and Susan reaching the highest peaks at just under 4,000 babies a year.
fig = px.line(
    f_babynames.filter(pl.col("Name").is_in(top10)),
    x="Year",
    y="Count",
    color="Name",
)
fig.update_layout(font_size=18, autosize=False, width=1000, height=400)
fig

# %% [markdown] id="p2-filter-intro"
# ## Filtering by Group
#
# Aggregation answers questions of the form "one number per group". A different kind of question asks for the *rows themselves*, chosen by a property of the group they belong to: all the elections held in a close year, all the names that appeared in at least ten different years.
#
# We'll switch to the `elections` dataset for this.
#
# ````{dropdown} Click to see the code
# :open: false
# ```python
# elections = pl.read_csv("data/elections.csv")
# elections.head(5)
# ```
# ````

# %% tags=["remove-input"] id="p2-load-elections"
elections = pl.read_csv("data/elections.csv")
elections.head(5)



# %% [markdown]
# <!-- tab-twins:begin elections = pl.read_csv("data/elections.csv") elections.head(5) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections = pl.read_csv("data/elections.csv")
# elections.head(5)
# ```
#
# ```text
# shape: (5, 6)
# ┌──────┬───────────────────┬───────────────────────┬──────────────┬────────┬───────────┐
# │ Year ┆ Candidate         ┆ Party                 ┆ Popular vote ┆ Result ┆ %         │
# │ ---  ┆ ---               ┆ ---                   ┆ ---          ┆ ---    ┆ ---       │
# │ i64  ┆ str               ┆ str                   ┆ i64          ┆ str    ┆ f64       │
# ╞══════╪═══════════════════╪═══════════════════════╪══════════════╪════════╪═══════════╡
# │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republican ┆ 151271       ┆ loss   ┆ 57.210122 │
# │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican ┆ 113142       ┆ win    ┆ 42.789878 │
# │ 1828 ┆ Andrew Jackson    ┆ Democratic            ┆ 642806       ┆ win    ┆ 56.203927 │
# │ 1828 ┆ John Quincy Adams ┆ National Republican   ┆ 500897       ┆ loss   ┆ 43.796073 │
# │ 1832 ┆ Andrew Jackson    ┆ Democratic            ┆ 702735       ┆ win    ┆ 54.574789 │
# └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd = pd.read_csv("data/elections.csv")
# elections_pd.head(5)
# ```
#
# ```text
#    Year          Candidate  ... Result          %
# 0  1824     Andrew Jackson  ...   loss  57.210122
# 1  1824  John Quincy Adams  ...    win  42.789878
# 2  1828     Andrew Jackson  ...    win  56.203927
# 3  1828  John Quincy Adams  ...   loss  43.796073
# 4  1832     Andrew Jackson  ...    win  54.574789
#
# [5 rows x 6 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown]
# <!-- tab-twins:begin elections = pl.read_csv("data/elections.csv")
# elections.head(5) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections = pl.read_csv("data/elections.csv")
# elections.head(5)
# ```
#
# ```text
# shape: (5, 6)
# ┌──────┬───────────────────┬───────────────────────┬──────────────┬────────┬───────────┐
# │ Year ┆ Candidate         ┆ Party                 ┆ Popular vote ┆ Result ┆ %         │
# │ ---  ┆ ---               ┆ ---                   ┆ ---          ┆ ---    ┆ ---       │
# │ i64  ┆ str               ┆ str                   ┆ i64          ┆ str    ┆ f64       │
# ╞══════╪═══════════════════╪═══════════════════════╪══════════════╪════════╪═══════════╡
# │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republican ┆ 151271       ┆ loss   ┆ 57.210122 │
# │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican ┆ 113142       ┆ win    ┆ 42.789878 │
# │ 1828 ┆ Andrew Jackson    ┆ Democratic            ┆ 642806       ┆ win    ┆ 56.203927 │
# │ 1828 ┆ John Quincy Adams ┆ National Republican   ┆ 500897       ┆ loss   ┆ 43.796073 │
# │ 1832 ┆ Andrew Jackson    ┆ Democratic            ┆ 702735       ┆ win    ┆ 54.574789 │
# └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd = pd.read_csv("data/elections.csv")
# elections_pd.head(5)
# ```
#
# ```text
#    Year          Candidate  ... Result          %
# 0  1824     Andrew Jackson  ...   loss  57.210122
# 1  1824  John Quincy Adams  ...    win  42.789878
# 2  1828     Andrew Jackson  ...    win  56.203927
# 3  1828  John Quincy Adams  ...   loss  43.796073
# 4  1832     Andrew Jackson  ...    win  54.574789
#
# [5 rows x 6 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-over-explain"
# The tool for this job is `.over` [(documentation)](https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.over.html), which computes an aggregate **within each group** and hands the group's answer back to every row of that group:
#
# - The aggregate collapses each group to a single value, such as `pl.len()` or `pl.col("c").max()`.
# - `.over("key")` computes that value per group, then broadcasts it back across the group's rows.
# - Comparing it produces `True` or `False` for every row at once, and `.filter` keeps the rows whose group answered `True`.
#
# Because the rows themselves are returned, and not one summary row per group, a filtered result has the same columns and the same row order as the table it came from.
#
# ```{image} images/filter_demo.png
# :alt: A filter applied to groups, where entire sub-tables are kept or discarded and the surviving rows are returned unchanged.
# :width: 600
# ```
#
# Here it is on the small `DataFrame` from earlier: keep every row whose letter appears at least twice.

# %% tags=["remove-input", "remove-output"] id="p2-over-small"
df.filter(pl.len().over("letter") >= 2)


# %% [markdown]
# <!-- tab-twins:begin df.filter(pl.len().over("letter") >= 2) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# df.filter(pl.len().over("letter") >= 2)
# ```
#
# ```text
# shape: (5, 3)
# ┌────────┬──────┬───────┐
# │ letter ┆ num  ┆ state │
# │ ---    ┆ ---  ┆ ---   │
# │ str    ┆ i64  ┆ str   │
# ╞════════╪══════╪═══════╡
# │ A      ┆ 1    ┆ null  │
# │ A      ┆ 2    ┆ tx    │
# │ C      ┆ 4    ┆ hi    │
# │ C      ┆ null ┆ null  │
# │ C      ┆ 4    ┆ ak    │
# └────────┴──────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# df_pd.groupby("letter").filter(lambda g: len(g) >= 2)
# ```
#
# ```text
#   letter  num state
# 0      A  1.0  None
# 1      A  2.0    tx
# 3      C  4.0    hi
# 4      C  NaN  None
# 5      C  4.0    ak
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-over-elections"
# `B` occurs once, so its row is gone; the two `A` rows and all three `C` rows survive, in their original order.
#
# Now for a real question. We want to identify "tight" election years — years in which no candidate won more than 45% of the popular vote — and see every candidate who ran in them. For each year we need the maximum `%` across all of that year's rows, and then we keep the rows whose year passed the test.

# %% tags=["remove-input", "remove-output"] id="p2-over-elections-code"
elections.filter(pl.col("%").max().over("Year") < 45).head(9)


# %% [markdown]
# <!-- tab-twins:begin elections.filter(pl.col("%").max().over("Year") < 45).head(9) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections.filter(pl.col("%").max().over("Year") < 45).head(9)
# ```
#
# ```text
# shape: (9, 6)
# ┌──────┬──────────────────────┬──────────────────────┬──────────────┬────────┬───────────┐
# │ Year ┆ Candidate            ┆ Party                ┆ Popular vote ┆ Result ┆ %         │
# │ ---  ┆ ---                  ┆ ---                  ┆ ---          ┆ ---    ┆ ---       │
# │ i64  ┆ str                  ┆ str                  ┆ i64          ┆ str    ┆ f64       │
# ╞══════╪══════════════════════╪══════════════════════╪══════════════╪════════╪═══════════╡
# │ 1860 ┆ Abraham Lincoln      ┆ Republican           ┆ 1855993      ┆ win    ┆ 39.699408 │
# │ 1860 ┆ John Bell            ┆ Constitutional Union ┆ 590901       ┆ loss   ┆ 12.639283 │
# │ 1860 ┆ John C. Breckinridge ┆ Southern Democratic  ┆ 848019       ┆ loss   ┆ 18.138998 │
# │ 1860 ┆ Stephen A. Douglas   ┆ Northern Democratic  ┆ 1380202      ┆ loss   ┆ 29.522311 │
# │ 1912 ┆ Eugene V. Debs       ┆ Socialist            ┆ 901551       ┆ loss   ┆ 6.004354  │
# │ 1912 ┆ Eugene W. Chafin     ┆ Prohibition          ┆ 208156       ┆ loss   ┆ 1.386325  │
# │ 1912 ┆ Theodore Roosevelt   ┆ Progressive          ┆ 4122721      ┆ loss   ┆ 27.457433 │
# │ 1912 ┆ William Taft         ┆ Republican           ┆ 3486242      ┆ loss   ┆ 23.218466 │
# │ 1912 ┆ Woodrow Wilson       ┆ Democratic           ┆ 6296284      ┆ win    ┆ 41.933422 │
# └──────┴──────────────────────┴──────────────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd[
#     elections_pd.groupby("Year")["%"].transform("max") < 45
# ].head(9)
# ```
#
# ```text
#     Year             Candidate  ... Result          %
# 23  1860       Abraham Lincoln  ...    win  39.699408
# 24  1860             John Bell  ...   loss  12.639283
# 25  1860  John C. Breckinridge  ...   loss  18.138998
# 26  1860    Stephen A. Douglas  ...   loss  29.522311
# 66  1912        Eugene V. Debs  ...   loss   6.004354
# 67  1912      Eugene W. Chafin  ...   loss   1.386325
# 68  1912    Theodore Roosevelt  ...   loss  27.457433
# 69  1912          William Taft  ...   loss  23.218466
# 70  1912        Woodrow Wilson  ...    win  41.933422
#
# [9 rows x 6 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-over-elections-explain"
# The first nine rows cover two full elections. In 1860 the winner, Abraham Lincoln, took only 39.7% of the popular vote against three opponents; in 1912 five candidates split the vote behind Woodrow Wilson's 41.9%. Neither year contains a single row above 45%, so both survive in their entirety.
#
# This is a different question from the row-by-row filtering we have done before. `elections.filter(pl.col("%") < 45)` inspects each row on its own and would keep Lincoln while discarding the winners of every other year. The `.over` version asks its question of the whole group and then keeps or drops all of the group's rows together.
#
# ### The `group_by` Puzzle
#
# Suppose we want the best election result for each party: for every party, the row describing the election in which it won its largest share of the vote. This turns out to be a good puzzle, and the obvious first attempt is wrong in an instructive way.
#
# Calling `.max()` directly on a `GroupBy` aggregates every column that is not a key.

# %% tags=["remove-input", "remove-output"] id="p2-puzzle-attempt1"
# Sorting by Party gives us the same ten parties on every run
elections.group_by("Party").max().sort("Party").head(10)


# %% [markdown]
# <!-- tab-twins:begin elections.group_by("Party").max().sort("Party").head(10) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Sorting by Party gives us the same ten parties on every run
# elections.group_by("Party").max().sort("Party").head(10)
# ```
#
# ```text
# shape: (10, 6)
# ┌───────────────────────┬──────┬────────────────────┬──────────────┬────────┬───────────┐
# │ Party                 ┆ Year ┆ Candidate          ┆ Popular vote ┆ Result ┆ %         │
# │ ---                   ┆ ---  ┆ ---                ┆ ---          ┆ ---    ┆ ---       │
# │ str                   ┆ i64  ┆ str                ┆ i64          ┆ str    ┆ f64       │
# ╞═══════════════════════╪══════╪════════════════════╪══════════════╪════════╪═══════════╡
# │ American              ┆ 1976 ┆ Thomas J. Anderson ┆ 873053       ┆ loss   ┆ 21.554001 │
# │ American Independent  ┆ 1976 ┆ Lester Maddox      ┆ 9901118      ┆ loss   ┆ 13.571218 │
# │ Anti-Masonic          ┆ 1832 ┆ William Wirt       ┆ 100715       ┆ loss   ┆ 7.821583  │
# │ Anti-Monopoly         ┆ 1884 ┆ Benjamin Butler    ┆ 134294       ┆ loss   ┆ 1.335838  │
# │ Citizens              ┆ 1980 ┆ Barry Commoner     ┆ 233052       ┆ loss   ┆ 0.270182  │
# │ Communist             ┆ 1932 ┆ William Z. Foster  ┆ 103307       ┆ loss   ┆ 0.261069  │
# │ Constitution          ┆ 2016 ┆ Michael Peroutka   ┆ 203091       ┆ loss   ┆ 0.152398  │
# │ Constitutional Union  ┆ 1860 ┆ John Bell          ┆ 590901       ┆ loss   ┆ 12.639283 │
# │ Democratic            ┆ 2024 ┆ Woodrow Wilson     ┆ 81268924     ┆ win    ┆ 61.344703 │
# │ Democratic-Republican ┆ 1824 ┆ John Quincy Adams  ┆ 151271       ┆ win    ┆ 57.210122 │
# └───────────────────────┴──────┴────────────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.groupby("Party").max(numeric_only=False).sort_index().head(10)
# ```
#
# ```text
#                        Year           Candidate  Popular vote Result          %
# Party
# American               1976  Thomas J. Anderson        873053   loss  21.554001
# American Independent   1976       Lester Maddox       9901118   loss  13.571218
# Anti-Masonic           1832        William Wirt        100715   loss   7.821583
# Anti-Monopoly          1884     Benjamin Butler        134294   loss   1.335838
# Citizens               1980      Barry Commoner        233052   loss   0.270182
# Communist              1932   William Z. Foster        103307   loss   0.261069
# Constitution           2016    Michael Peroutka        203091   loss   0.152398
# Constitutional Union   1860           John Bell        590901   loss  12.639283
# Democratic             2024      Woodrow Wilson      81268924    win  61.344703
# Democratic-Republican  1824   John Quincy Adams        151271    win  57.210122
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-puzzle-attempt1-explain"
# Read the Democratic row and something is clearly off: it says Woodrow Wilson ran in 2024 and won 61.3% of the vote.
#
# The trouble is that `max` is taken over each column *independently*. For the Democrats it computes:
#
# - The most recent `Year` a Democratic candidate ran for president (2024)
# - The `Candidate` whose name is alphabetically last ("Woodrow Wilson")
# - The largest vote share any Democrat has ever won (61.3%)
#
# Three columns, three different elections, and a row that describes none of them. Naming the columns you want aggregated is a good habit, but the deeper problem is that we asked the wrong question: we do not want the maximum of each column, we want *the row* in which one column reaches its maximum.
#
# So let's take a different approach:
#
# 1. Sort the `DataFrame` so that rows are in descending order of `%`.
# 2. Group by `Party` and take the first row of each group.
#
# Sorting first may seem indirect, but it puts the answer within reach: if the whole table runs from largest `%` to smallest, then within any group the first row is that group's best result.

# %% tags=["remove-input", "remove-output"] id="p2-puzzle-sorted"
elections_sorted_by_percent = elections.sort("%", descending=True)
elections_sorted_by_percent.head(5)


# %% [markdown]
# <!-- tab-twins:begin elections_sorted_by_percent = elections.sort("%", descending=True) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections_sorted_by_percent = elections.sort("%", descending=True)
# elections_sorted_by_percent.head(5)
# ```
#
# ```text
# shape: (5, 6)
# ┌──────┬────────────────────┬────────────┬──────────────┬────────┬───────────┐
# │ Year ┆ Candidate          ┆ Party      ┆ Popular vote ┆ Result ┆ %         │
# │ ---  ┆ ---                ┆ ---        ┆ ---          ┆ ---    ┆ ---       │
# │ i64  ┆ str                ┆ str        ┆ i64          ┆ str    ┆ f64       │
# ╞══════╪════════════════════╪════════════╪══════════════╪════════╪═══════════╡
# │ 1964 ┆ Lyndon Johnson     ┆ Democratic ┆ 43127041     ┆ win    ┆ 61.344703 │
# │ 1936 ┆ Franklin Roosevelt ┆ Democratic ┆ 27752648     ┆ win    ┆ 60.978107 │
# │ 1972 ┆ Richard Nixon      ┆ Republican ┆ 47168710     ┆ win    ┆ 60.907806 │
# │ 1920 ┆ Warren Harding     ┆ Republican ┆ 16144093     ┆ win    ┆ 60.574501 │
# │ 1984 ┆ Ronald Reagan      ┆ Republican ┆ 54455472     ┆ win    ┆ 59.023326 │
# └──────┴────────────────────┴────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_sorted_pd = elections_pd.sort_values("%", ascending=False)
# elections_sorted_pd.head(5)
# ```
#
# ```text
#      Year           Candidate       Party  Popular vote Result          %
# 114  1964      Lyndon Johnson  Democratic      43127041    win  61.344703
# 91   1936  Franklin Roosevelt  Democratic      27752648    win  60.978107
# 120  1972       Richard Nixon  Republican      47168710    win  60.907806
# 79   1920      Warren Harding  Republican      16144093    win  60.574501
# 133  1984       Ronald Reagan  Republican      54455472    win  59.023326
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% tags=["remove-input", "remove-output"] id="p2-puzzle-attempt2"
best_per_party = elections_sorted_by_percent.group_by("Party", maintain_order=True).head(1)
best_per_party.head(10)


# %% [markdown]
# <!-- tab-twins:begin best_per_party = elections_sorted_by_percent.group_by("Party", maintain_order=True).head(1) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# best_per_party = elections_sorted_by_percent.group_by("Party", maintain_order=True).head(1)
# best_per_party.head(10)
# ```
#
# ```text
# shape: (10, 6)
# ┌───────────────────────┬──────┬────────────────────────┬──────────────┬────────┬───────────┐
# │ Party                 ┆ Year ┆ Candidate              ┆ Popular vote ┆ Result ┆ %         │
# │ ---                   ┆ ---  ┆ ---                    ┆ ---          ┆ ---    ┆ ---       │
# │ str                   ┆ i64  ┆ str                    ┆ i64          ┆ str    ┆ f64       │
# ╞═══════════════════════╪══════╪════════════════════════╪══════════════╪════════╪═══════════╡
# │ Democratic            ┆ 1964 ┆ Lyndon Johnson         ┆ 43127041     ┆ win    ┆ 61.344703 │
# │ Republican            ┆ 1972 ┆ Richard Nixon          ┆ 47168710     ┆ win    ┆ 60.907806 │
# │ Democratic-Republican ┆ 1824 ┆ Andrew Jackson         ┆ 151271       ┆ loss   ┆ 57.210122 │
# │ National Union        ┆ 1864 ┆ Abraham Lincoln        ┆ 2211317      ┆ win    ┆ 54.951512 │
# │ Whig                  ┆ 1840 ┆ William Henry Harrison ┆ 1275583      ┆ win    ┆ 53.051213 │
# │ Liberal Republican    ┆ 1872 ┆ Horace Greeley         ┆ 2834761      ┆ loss   ┆ 44.071406 │
# │ National Republican   ┆ 1828 ┆ John Quincy Adams      ┆ 500897       ┆ loss   ┆ 43.796073 │
# │ Northern Democratic   ┆ 1860 ┆ Stephen A. Douglas     ┆ 1380202      ┆ loss   ┆ 29.522311 │
# │ Progressive           ┆ 1912 ┆ Theodore Roosevelt     ┆ 4122721      ┆ loss   ┆ 27.457433 │
# │ American              ┆ 1856 ┆ Millard Fillmore       ┆ 873053       ┆ loss   ┆ 21.554001 │
# └───────────────────────┴──────┴────────────────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# best_per_party_pd = elections_sorted_pd.groupby("Party", sort=False).head(1)
# best_per_party_pd.head(10)
# ```
#
# ```text
#      Year               Candidate  ... Result          %
# 114  1964          Lyndon Johnson  ...    win  61.344703
# 120  1972           Richard Nixon  ...    win  60.907806
# 0    1824          Andrew Jackson  ...   loss  57.210122
# 27   1864         Abraham Lincoln  ...    win  54.951512
# 11   1840  William Henry Harrison  ...    win  53.051213
# 31   1872          Horace Greeley  ...   loss  44.071406
# 3    1828       John Quincy Adams  ...   loss  43.796073
# 26   1860      Stephen A. Douglas  ...   loss  29.522311
# 68   1912      Theodore Roosevelt  ...   loss  27.457433
# 22   1856        Millard Fillmore  ...   loss  21.554001
#
# [10 rows x 6 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-puzzle-explain"
# Here's an illustration of the process:
#
# ```{image} images/puzzle_demo.png
# :alt: A table sorted in descending order, then grouped, with the first row of each group selected to give the largest value per group.
# :width: 600
# ```
#
# One row per party, 37 in all, and each one is a real election. Lyndon Johnson's 1964 landslide is the best Democratic result on record, and Richard Nixon's 1972 win the best Republican one. Two properties of `.group_by` are doing the work: rows keep their relative order inside a group, so "first row" means "highest `%`", and `maintain_order=True` orders the parties by where their best result appeared, which turns the output into a ranking.
#
# #### Alternative Solutions
#
# With a rich toolkit there is usually more than one way to reach an answer, and the options differ in readability, memory use, and speed. Developing a sense for which is better takes practice, and it is worth trying to imagine a second approach whenever your first one feels convoluted.
#
# ::: {note}
# Understanding these alternatives is not required. They are here to show how differently the same question can be asked.
# :::
#
# A row's position is the only handle we have on it, so the first alternative writes those positions into a column with `.with_row_index` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.with_row_index.html), then uses `.arg_max` [(documentation)](https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.arg_max.html) to find where each party's best election sits.

# %% tags=["remove-input", "remove-output"] id="p2-puzzle-alt1a"
best_positions = (
    elections.with_row_index("position")
    .group_by("Party")
    .agg(pl.col("position").get(pl.col("%").arg_max()))
    .sort("Party")
)
best_positions.head()


# %% [markdown]
# <!-- tab-twins:begin best_positions = ( -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# best_positions = (
#     elections.with_row_index("position")
#     .group_by("Party")
#     .agg(pl.col("position").get(pl.col("%").arg_max()))
#     .sort("Party")
# )
# best_positions.head()
# ```
#
# ```text
# shape: (5, 2)
# ┌──────────────────────┬──────────┐
# │ Party                ┆ position │
# │ ---                  ┆ ---      │
# │ str                  ┆ u32      │
# ╞══════════════════════╪══════════╡
# │ American             ┆ 22       │
# │ American Independent ┆ 115      │
# │ Anti-Masonic         ┆ 6        │
# │ Anti-Monopoly        ┆ 38       │
# │ Citizens             ┆ 127      │
# └──────────────────────┴──────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# best_positions_pd = (
#     elections_pd.groupby("Party")["%"].idxmax().sort_index()
# )
# best_positions_pd.head()
# ```
#
# ```text
# Party
# American                 22
# American Independent    115
# Anti-Masonic              6
# Anti-Monopoly            38
# Citizens                127
# Name: %, dtype: int64
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-puzzle-alt1b"
# `arg_max` gives the position *within the group* of the largest `%`, and `.get` reads the entry sitting at that position in `position`. Those numbers are positions in the original table, so we can select the rows directly.

# %% tags=["remove-input", "remove-output"] id="p2-puzzle-alt1c"
elections[best_positions["position"]].sort("Party").head()


# %% [markdown]
# <!-- tab-twins:begin elections[best_positions["position"]].sort("Party").head() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections[best_positions["position"]].sort("Party").head()
# ```
#
# ```text
# shape: (5, 6)
# ┌──────┬──────────────────┬──────────────────────┬──────────────┬────────┬───────────┐
# │ Year ┆ Candidate        ┆ Party                ┆ Popular vote ┆ Result ┆ %         │
# │ ---  ┆ ---              ┆ ---                  ┆ ---          ┆ ---    ┆ ---       │
# │ i64  ┆ str              ┆ str                  ┆ i64          ┆ str    ┆ f64       │
# ╞══════╪══════════════════╪══════════════════════╪══════════════╪════════╪═══════════╡
# │ 1856 ┆ Millard Fillmore ┆ American             ┆ 873053       ┆ loss   ┆ 21.554001 │
# │ 1968 ┆ George Wallace   ┆ American Independent ┆ 9901118      ┆ loss   ┆ 13.571218 │
# │ 1832 ┆ William Wirt     ┆ Anti-Masonic         ┆ 100715       ┆ loss   ┆ 7.821583  │
# │ 1884 ┆ Benjamin Butler  ┆ Anti-Monopoly        ┆ 134294       ┆ loss   ┆ 1.335838  │
# │ 1980 ┆ Barry Commoner   ┆ Citizens             ┆ 233052       ┆ loss   ┆ 0.270182  │
# └──────┴──────────────────┴──────────────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.loc[best_positions_pd].sort_values("Party").head()
# ```
#
# ```text
#      Year         Candidate  ... Result          %
# 22   1856  Millard Fillmore  ...   loss  21.554001
# 115  1968    George Wallace  ...   loss  13.571218
# 6    1832      William Wirt  ...   loss   7.821583
# 38   1884   Benjamin Butler  ...   loss   1.335838
# 127  1980    Barry Commoner  ...   loss   0.270182
#
# [5 rows x 6 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-puzzle-alt2-intro"
# The second alternative does not group at all. `.unique` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.unique.html) keeps one row per party, and `keep="last"` decides which one — so sorting by `%` in ascending order first leaves each party's best election as the one that survives.

# %% tags=["remove-input", "remove-output"] id="p2-puzzle-alt2"
best_per_party2 = elections.sort("%").unique(subset=["Party"], keep="last", maintain_order=True)
best_per_party2.sort("Party").head()


# %% [markdown]
# <!-- tab-twins:begin best_per_party2 = elections.sort("%").unique(subset=["Party"], keep="last", maintain_order=True) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# best_per_party2 = elections.sort("%").unique(subset=["Party"], keep="last", maintain_order=True)
# best_per_party2.sort("Party").head()
# ```
#
# ```text
# shape: (5, 6)
# ┌──────┬──────────────────┬──────────────────────┬──────────────┬────────┬───────────┐
# │ Year ┆ Candidate        ┆ Party                ┆ Popular vote ┆ Result ┆ %         │
# │ ---  ┆ ---              ┆ ---                  ┆ ---          ┆ ---    ┆ ---       │
# │ i64  ┆ str              ┆ str                  ┆ i64          ┆ str    ┆ f64       │
# ╞══════╪══════════════════╪══════════════════════╪══════════════╪════════╪═══════════╡
# │ 1856 ┆ Millard Fillmore ┆ American             ┆ 873053       ┆ loss   ┆ 21.554001 │
# │ 1968 ┆ George Wallace   ┆ American Independent ┆ 9901118      ┆ loss   ┆ 13.571218 │
# │ 1832 ┆ William Wirt     ┆ Anti-Masonic         ┆ 100715       ┆ loss   ┆ 7.821583  │
# │ 1884 ┆ Benjamin Butler  ┆ Anti-Monopoly        ┆ 134294       ┆ loss   ┆ 1.335838  │
# │ 1980 ┆ Barry Commoner   ┆ Citizens             ┆ 233052       ┆ loss   ┆ 0.270182  │
# └──────┴──────────────────┴──────────────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# best_per_party2_pd = elections_pd.sort_values("%").drop_duplicates(
#     subset="Party", keep="last"
# )
# best_per_party2_pd.sort_values("Party").head()
# ```
#
# ```text
#      Year         Candidate  ... Result          %
# 22   1856  Millard Fillmore  ...   loss  21.554001
# 115  1968    George Wallace  ...   loss  13.571218
# 6    1832      William Wirt  ...   loss   7.821583
# 38   1884   Benjamin Butler  ...   loss   1.335838
# 127  1980    Barry Commoner  ...   loss   0.270182
#
# [5 rows x 6 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-groupby-objects"
# *Challenge:* see if you can find a third approach that gives the same answer.
#
# ### `GroupBy` Objects
#
# We have called `.agg`, `.len`, `.max`, and `.head` on the result of `.group_by`, so it is worth a closer look at what that result actually is.

# %% tags=["remove-input", "remove-output"] id="p2-groupby-type"
grouped_by_party = elections.group_by("Party")
type(grouped_by_party)


# %% [markdown]
# <!-- tab-twins:begin type(grouped_by_party) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# grouped_by_party = elections.group_by("Party")
# type(grouped_by_party)
# ```
#
# ```text
# polars.dataframe.group_by.GroupBy
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# grouped_by_party_pd = elections_pd.groupby("Party")
# type(grouped_by_party_pd)
# ```
#
# ```text
# <class 'pandas.core.groupby.generic.DataFrameGroupBy'>
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-groupby-dict-intro"
# It is a `GroupBy` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/group_by.html), not a `DataFrame` and not a list of them. It records the table and the keys, and computes nothing until we ask it for something.
#
# What it will do is iterate: stepping through a `GroupBy` yields each group's key alongside the rows belonging to it. That makes it easy to turn into a dictionary.

# %% tags=["remove-input", "remove-output"] id="p2-groupby-dict"
groups = dict(grouped_by_party)
sorted(groups.keys())[:6]


# %% [markdown]
# <!-- tab-twins:begin groups = dict(grouped_by_party) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# groups = dict(grouped_by_party)
# sorted(groups.keys())[:6]
# ```
#
# ```text
# [('American',),
#  ('American Independent',),
#  ('Anti-Masonic',),
#  ('Anti-Monopoly',),
#  ('Citizens',),
#  ('Communist',)]
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# groups_pd = dict(list(grouped_by_party_pd))
# sorted(groups_pd.keys())[:6]
# ```
#
# ```text
# ['American', 'American Independent', 'Anti-Masonic', 'Anti-Monopoly', 'Citizens', 'Communist']
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-groupby-lookup"
# The keys are the groups and the values are the rows belonging to each. Every key arrives as a tuple, because we are allowed to group by several columns at once. Looking one up gives us back an ordinary `DataFrame`.

# %% tags=["remove-input", "remove-output"] id="p2-groupby-socialist"
groups[("Socialist",)]


# %% [markdown]
# <!-- tab-twins:begin groups[("Socialist",)] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# groups[("Socialist",)]
# ```
#
# ```text
# shape: (10, 6)
# ┌──────┬─────────────────┬───────────┬──────────────┬────────┬──────────┐
# │ Year ┆ Candidate       ┆ Party     ┆ Popular vote ┆ Result ┆ %        │
# │ ---  ┆ ---             ┆ ---       ┆ ---          ┆ ---    ┆ ---      │
# │ i64  ┆ str             ┆ str       ┆ i64          ┆ str    ┆ f64      │
# ╞══════╪═════════════════╪═══════════╪══════════════╪════════╪══════════╡
# │ 1904 ┆ Eugene V. Debs  ┆ Socialist ┆ 402810       ┆ loss   ┆ 2.985897 │
# │ 1908 ┆ Eugene V. Debs  ┆ Socialist ┆ 420852       ┆ loss   ┆ 2.850866 │
# │ 1912 ┆ Eugene V. Debs  ┆ Socialist ┆ 901551       ┆ loss   ┆ 6.004354 │
# │ 1916 ┆ Allan L. Benson ┆ Socialist ┆ 590524       ┆ loss   ┆ 3.194193 │
# │ 1920 ┆ Eugene V. Debs  ┆ Socialist ┆ 913693       ┆ loss   ┆ 3.428282 │
# │ 1928 ┆ Norman Thomas   ┆ Socialist ┆ 267478       ┆ loss   ┆ 0.728623 │
# │ 1932 ┆ Norman Thomas   ┆ Socialist ┆ 884885       ┆ loss   ┆ 2.236211 │
# │ 1936 ┆ Norman Thomas   ┆ Socialist ┆ 187910       ┆ loss   ┆ 0.412876 │
# │ 1940 ┆ Norman Thomas   ┆ Socialist ┆ 116599       ┆ loss   ┆ 0.234237 │
# │ 1948 ┆ Norman Thomas   ┆ Socialist ┆ 139569       ┆ loss   ┆ 0.286312 │
# └──────┴─────────────────┴───────────┴──────────────┴────────┴──────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# groups_pd["Socialist"]
# ```
#
# ```text
#      Year        Candidate      Party  Popular vote Result         %
# 58   1904   Eugene V. Debs  Socialist        402810   loss  2.985897
# 62   1908   Eugene V. Debs  Socialist        420852   loss  2.850866
# 66   1912   Eugene V. Debs  Socialist        901551   loss  6.004354
# 71   1916  Allan L. Benson  Socialist        590524   loss  3.194193
# 76   1920   Eugene V. Debs  Socialist        913693   loss  3.428282
# 85   1928    Norman Thomas  Socialist        267478   loss  0.728623
# 88   1932    Norman Thomas  Socialist        884885   loss  2.236211
# 92   1936    Norman Thomas  Socialist        187910   loss  0.412876
# 95   1940    Norman Thomas  Socialist        116599   loss  0.234237
# 102  1948    Norman Thomas  Socialist        139569   loss  0.286312
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-pivot-intro"
# The Socialist party contested ten elections, the last of them in 1948.
#
# ## Aggregating Data with Pivot Tables
#
# ### `group_by` with Multiple Columns
#
# Every grouping so far has used a single column. Passing a list groups by a combination of columns instead: one group for each distinct pairing of values.
#
# Let's find the total number of babies of each sex born in each year, which means grouping by *both* `"Year"` and `"Sex"`.

# %% tags=["remove-input", "remove-output"] id="p2-groupby-multi"
babynames.group_by(["Year", "Sex"]).agg(pl.col("Count").sum()).sort(["Year", "Sex"]).head(6)


# %% [markdown]
# <!-- tab-twins:begin babynames.group_by(["Year", "Sex"]).agg(pl.col("Count").sum()).sort(["Year", "Sex"]).head(6) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# babynames.group_by(["Year", "Sex"]).agg(pl.col("Count").sum()).sort(["Year", "Sex"]).head(6)
# ```
#
# ```text
# shape: (6, 3)
# ┌──────┬─────┬───────┐
# │ Year ┆ Sex ┆ Count │
# │ ---  ┆ --- ┆ ---   │
# │ i64  ┆ str ┆ i64   │
# ╞══════╪═════╪═══════╡
# │ 1910 ┆ F   ┆ 5950  │
# │ 1910 ┆ M   ┆ 3213  │
# │ 1911 ┆ F   ┆ 6602  │
# │ 1911 ┆ M   ┆ 3381  │
# │ 1912 ┆ F   ┆ 9804  │
# │ 1912 ┆ M   ┆ 8142  │
# └──────┴─────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd.groupby(["Year", "Sex"])["Count"].sum().head(6)
# ```
#
# ```text
# Year  Sex
# 1910  F      5950
#       M      3213
# 1911  F      6602
#       M      3381
# 1912  F      9804
#       M      8142
# Name: Count, dtype: int64
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-pivot-explain"
# In 1910 the data records 5,950 girls and 3,213 boys. The answer is correct, but the shape is awkward: every year is spread across two rows, and comparing the sexes means reading down the table in pairs.
#
# A **pivot table** puts the second grouping column across the top instead. You saw these back in [Data 8](https://inferentialthinking.com/chapters/08/3/Cross-Classifying_by_More_than_One_Variable.html#pivot-tables-rearranging-the-output-of-group). One set of values labels the rows, another labels the columns, and each cell holds the aggregate for that row-column pair.
#
# Here's an illustration of the process:
#
# ```{image} images/pivot.png
# :alt: Rows grouped by two keys and aggregated, then reshaped so that one key labels the rows and the other labels the columns of a grid.
# :width: 600
# ```
#
# ### `pivot`
#
# `.pivot` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.pivot.html) builds that grid.

# %% tags=["remove-input", "remove-output"] id="p2-pivot"
babynames.pivot(
    index="Year",             # one row per year
    on="Sex",                 # the values of Sex become column names
    values="Count",           # what fills the cells
    aggregate_function="sum", # how to combine the rows that land in one cell
).head(5)


# %% [markdown]
# <!-- tab-twins:begin aggregate_function="sum", # how to combine the rows that land in one cell -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# babynames.pivot(
#     index="Year",             # one row per year
#     on="Sex",                 # the values of Sex become column names
#     values="Count",           # what fills the cells
#     aggregate_function="sum", # how to combine the rows that land in one cell
# ).head(5)
# ```
#
# ```text
# shape: (5, 3)
# ┌──────┬───────┬───────┐
# │ Year ┆ F     ┆ M     │
# │ ---  ┆ ---   ┆ ---   │
# │ i64  ┆ i64   ┆ i64   │
# ╞══════╪═══════╪═══════╡
# │ 1910 ┆ 5950  ┆ 3213  │
# │ 1911 ┆ 6602  ┆ 3381  │
# │ 1912 ┆ 9804  ┆ 8142  │
# │ 1913 ┆ 11860 ┆ 10234 │
# │ 1914 ┆ 13815 ┆ 13111 │
# └──────┴───────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd.pivot_table(
#     index="Year",     # one row per year
#     columns="Sex",    # the values of Sex become column names
#     values="Count",   # what fills the cells
#     aggfunc="sum",    # how to combine the rows that land in one cell
# ).head(5)
# ```
#
# ```text
# Sex       F      M
# Year
# 1910   5950   3213
# 1911   6602   3381
# 1912   9804   8142
# 1913  11860  10234
# 1914  13815  13111
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-pivot-explain2"
# The same numbers as before, 5,950 and 3,213 for 1910, now sitting side by side, one row per year. The four arguments are worth naming individually:
#
# * `index="Year"` is the column whose values label the rows.
# * `on="Sex"` is the column whose values become the new column names.
# * `values="Count"` is the column that fills the cells.
# * `aggregate_function="sum"` says what to do when several rows land in the same cell. Every `(Year, Sex)` pair here covers hundreds of names, and we want them summed.
#
# ### `pivot` with Multiple Values
#
# `values` can name more than one column. Every pairing of a value column with a value of `on` becomes an output column, named for both: the value column first, then the value it belongs to.

# %% tags=["remove-input", "remove-output"] id="p2-pivot-multi"
babynames.pivot(
    index="Year",
    on="Sex",
    values=["Count", "Name"],
    aggregate_function="max",
).head(6)


# %% [markdown]
# <!-- tab-twins:begin values=["Count", "Name"], -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# babynames.pivot(
#     index="Year",
#     on="Sex",
#     values=["Count", "Name"],
#     aggregate_function="max",
# ).head(6)
# ```
#
# ```text
# shape: (6, 5)
# ┌──────┬─────────┬─────────┬────────┬─────────┐
# │ Year ┆ Count_F ┆ Count_M ┆ Name_F ┆ Name_M  │
# │ ---  ┆ ---     ┆ ---     ┆ ---    ┆ ---     │
# │ i64  ┆ i64     ┆ i64     ┆ str    ┆ str     │
# ╞══════╪═════════╪═════════╪════════╪═════════╡
# │ 1910 ┆ 295     ┆ 237     ┆ Yvonne ┆ William │
# │ 1911 ┆ 390     ┆ 214     ┆ Zelma  ┆ Willis  │
# │ 1912 ┆ 534     ┆ 501     ┆ Yvonne ┆ Woodrow │
# │ 1913 ┆ 584     ┆ 614     ┆ Zelma  ┆ Yoshio  │
# │ 1914 ┆ 773     ┆ 769     ┆ Zelma  ┆ Yoshio  │
# │ 1915 ┆ 998     ┆ 1033    ┆ Zita   ┆ Yukio   │
# └──────┴─────────┴─────────┴────────┴─────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd.pivot_table(
#     index="Year",
#     columns="Sex",
#     values=["Count", "Name"],
#     aggfunc="max",
# ).head(6)
# ```
#
# ```text
#      Count          Name
# Sex      F     M       F        M
# Year
# 1910   295   237  Yvonne  William
# 1911   390   214   Zelma   Willis
# 1912   534   501  Yvonne  Woodrow
# 1913   584   614   Zelma   Yoshio
# 1914   773   769   Zelma   Yoshio
# 1915   998  1033    Zita    Yukio
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-pivot-multi-explain"
# Four columns come out: `Count_F`, `Count_M`, `Name_F`, and `Name_M`. Each row gives the largest single-name count for each sex that year, and the alphabetically last name of each sex.
#
# Read that carefully, because the count and the name in a row have nothing to do with each other — they were aggregated separately, exactly as in the puzzle above. In 1910 the most popular girl's name was given to 295 girls, and that name was certainly not Yvonne.
#
# ## Joining Tables
#
# When working on data science projects, we're unlikely to have all the data we want sitting in a single `DataFrame`. A real-world data scientist has to grapple with data arriving from several sources, and combining two tables into one is how that work usually starts.
#
# Say we want to know how popular the first names of presidential candidates were among California babies in 2022. Neither table can answer that alone: `elections` knows the candidates, and `babynames` knows the babies. We'll start by pulling each candidate's first name into a column of its own, so the two tables have something in common to match on.

# %% tags=["remove-input", "remove-output"] id="p2-first-name"
# Split each candidate's full name on the blank space, then keep the first piece
elections = elections.with_columns(
    pl.col("Candidate").str.split(" ").list.get(0).alias("First Name")
)
elections.head(5)


# %% [markdown]
# <!-- tab-twins:begin pl.col("Candidate").str.split(" ").list.get(0).alias("First Name") -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Split each candidate's full name on the blank space, then keep the first piece
# elections = elections.with_columns(
#     pl.col("Candidate").str.split(" ").list.get(0).alias("First Name")
# )
# elections.head(5)
# ```
#
# ```text
# shape: (5, 7)
# ┌──────┬───────────────────┬──────────────────────┬──────────────┬────────┬───────────┬────────────┐
# │ Year ┆ Candidate         ┆ Party                ┆ Popular vote ┆ Result ┆ %         ┆ First Name │
# │ ---  ┆ ---               ┆ ---                  ┆ ---          ┆ ---    ┆ ---       ┆ ---        │
# │ i64  ┆ str               ┆ str                  ┆ i64          ┆ str    ┆ f64       ┆ str        │
# ╞══════╪═══════════════════╪══════════════════════╪══════════════╪════════╪═══════════╪════════════╡
# │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republica ┆ 151271       ┆ loss   ┆ 57.210122 ┆ Andrew     │
# │      ┆                   ┆ n                    ┆              ┆        ┆           ┆            │
# │ 1824 ┆ John Quincy Adams ┆ Democratic-Republica ┆ 113142       ┆ win    ┆ 42.789878 ┆ John       │
# │      ┆                   ┆ n                    ┆              ┆        ┆           ┆            │
# │ 1828 ┆ Andrew Jackson    ┆ Democratic           ┆ 642806       ┆ win    ┆ 56.203927 ┆ Andrew     │
# │ 1828 ┆ John Quincy Adams ┆ National Republican  ┆ 500897       ┆ loss   ┆ 43.796073 ┆ John       │
# │ 1832 ┆ Andrew Jackson    ┆ Democratic           ┆ 702735       ┆ win    ┆ 54.574789 ┆ Andrew     │
# └──────┴───────────────────┴──────────────────────┴──────────────┴────────┴───────────┴────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # Split each candidate's full name on the blank space, then keep the first piece
# elections_pd["First Name"] = elections_pd["Candidate"].str.split(" ").str[0]
# elections_pd.head(5)
# ```
#
# ```text
#    Year          Candidate                  Party  ...  Result          %  First Name
# 0  1824     Andrew Jackson  Democratic-Republican  ...    loss  57.210122      Andrew
# 1  1824  John Quincy Adams  Democratic-Republican  ...     win  42.789878        John
# 2  1828     Andrew Jackson             Democratic  ...     win  56.203927      Andrew
# 3  1828  John Quincy Adams    National Republican  ...    loss  43.796073        John
# 4  1832     Andrew Jackson             Democratic  ...     win  54.574789      Andrew
#
# [5 rows x 7 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% tags=["remove-input", "remove-output"] id="p2-babynames-2022"
# Here, we'll only consider `babynames` data from 2022
babynames_2022 = babynames.filter(pl.col("Year") == 2022)
babynames_2022.head()


# %% [markdown]
# <!-- tab-twins:begin babynames_2022 = babynames.filter(pl.col("Year") == 2022) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Here, we'll only consider `babynames` data from 2022
# babynames_2022 = babynames.filter(pl.col("Year") == 2022)
# babynames_2022.head()
# ```
#
# ```text
# shape: (5, 5)
# ┌───────┬─────┬──────┬────────┬───────┐
# │ State ┆ Sex ┆ Year ┆ Name   ┆ Count │
# │ ---   ┆ --- ┆ ---  ┆ ---    ┆ ---   │
# │ str   ┆ str ┆ i64  ┆ str    ┆ i64   │
# ╞═══════╪═════╪══════╪════════╪═══════╡
# │ CA    ┆ F   ┆ 2022 ┆ Olivia ┆ 2178  │
# │ CA    ┆ F   ┆ 2022 ┆ Emma   ┆ 2080  │
# │ CA    ┆ F   ┆ 2022 ┆ Camila ┆ 2046  │
# │ CA    ┆ F   ┆ 2022 ┆ Mia    ┆ 1882  │
# │ CA    ┆ F   ┆ 2022 ┆ Sophia ┆ 1762  │
# └───────┴─────┴──────┴────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # Here, we'll only consider `babynames` data from 2022
# babynames_2022_pd = babynames_pd[babynames_pd["Year"] == 2022]
# babynames_2022_pd.head()
# ```
#
# ```text
#        State Sex  Year    Name  Count
# 235835    CA   F  2022  Olivia   2178
# 235836    CA   F  2022    Emma   2080
# 235837    CA   F  2022  Camila   2046
# 235838    CA   F  2022     Mia   1882
# 235839    CA   F  2022  Sophia   1762
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-join-intro"
# Now we're ready to combine them. As in Data 8, this operation is called a **join**: the left table calls the method, and the right table is its first argument [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.join.html).

# %% tags=["remove-input", "remove-output"] id="p2-join"
merged = elections.join(
    babynames_2022,
    left_on="First Name",
    right_on="Name",
    maintain_order="left",
)
merged.head()


# %% [markdown]
# <!-- tab-twins:begin merged = elections.join( -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# merged = elections.join(
#     babynames_2022,
#     left_on="First Name",
#     right_on="Name",
#     maintain_order="left",
# )
# merged.head()
# ```
#
# ```text
# shape: (5, 11)
# ┌──────┬──────────────────┬──────────────────┬──────────────┬───┬───────┬─────┬────────────┬───────┐
# │ Year ┆ Candidate        ┆ Party            ┆ Popular vote ┆ … ┆ State ┆ Sex ┆ Year_right ┆ Count │
# │ ---  ┆ ---              ┆ ---              ┆ ---          ┆   ┆ ---   ┆ --- ┆ ---        ┆ ---   │
# │ i64  ┆ str              ┆ str              ┆ i64          ┆   ┆ str   ┆ str ┆ i64        ┆ i64   │
# ╞══════╪══════════════════╪══════════════════╪══════════════╪═══╪═══════╪═════╪════════════╪═══════╡
# │ 1824 ┆ Andrew Jackson   ┆ Democratic-Repub ┆ 151271       ┆ … ┆ CA    ┆ M   ┆ 2022       ┆ 741   │
# │      ┆                  ┆ lican            ┆              ┆   ┆       ┆     ┆            ┆       │
# │ 1824 ┆ John Quincy      ┆ Democratic-Repub ┆ 113142       ┆ … ┆ CA    ┆ M   ┆ 2022       ┆ 490   │
# │      ┆ Adams            ┆ lican            ┆              ┆   ┆       ┆     ┆            ┆       │
# │ 1828 ┆ Andrew Jackson   ┆ Democratic       ┆ 642806       ┆ … ┆ CA    ┆ M   ┆ 2022       ┆ 741   │
# │ 1828 ┆ John Quincy      ┆ National         ┆ 500897       ┆ … ┆ CA    ┆ M   ┆ 2022       ┆ 490   │
# │      ┆ Adams            ┆ Republican       ┆              ┆   ┆       ┆     ┆            ┆       │
# │ 1832 ┆ Andrew Jackson   ┆ Democratic       ┆ 702735       ┆ … ┆ CA    ┆ M   ┆ 2022       ┆ 741   │
# └──────┴──────────────────┴──────────────────┴──────────────┴───┴───────┴─────┴────────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# merged_pd = elections_pd.merge(
#     babynames_2022_pd,
#     left_on="First Name",
#     right_on="Name",
# )
# merged_pd.head()
# ```
#
# ```text
#    Year_x          Candidate                  Party  ...  Year_y    Name  Count
# 0    1824     Andrew Jackson  Democratic-Republican  ...    2022  Andrew    741
# 1    1824  John Quincy Adams  Democratic-Republican  ...    2022    John    490
# 2    1828     Andrew Jackson             Democratic  ...    2022  Andrew    741
# 3    1828  John Quincy Adams    National Republican  ...    2022    John    490
# 4    1832     Andrew Jackson             Democratic  ...    2022  Andrew    741
#
# [5 rows x 12 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% tags=["remove-input", "remove-output"] id="p2-join-cols"
# The full column list, since the table above is too wide to show it
merged.columns


# %% [markdown]
# <!-- tab-twins:begin merged.columns -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # The full column list, since the table above is too wide to show it
# merged.columns
# ```
#
# ```text
# ['Year',
#  'Candidate',
#  'Party',
#  'Popular vote',
#  'Result',
#  '%',
#  'First Name',
#  'State',
#  'Sex',
#  'Year_right',
#  'Count']
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # The full column list, since the table above is too wide to show it
# merged_pd.columns.tolist()
# ```
#
# ```text
# ['Year_x', 'Candidate', 'Party', 'Popular vote', 'Result', '%', 'First Name', 'State', 'Sex', 'Year_y', 'Name', 'Count']
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-join-explain"
# Each row of `merged` pairs a candidate with a 2022 baby-name record whose name matches theirs. We started with 187 rows in `elections` and ended with 156: forty candidates share their first name with no baby born in California that year and drop out, while nine match twice, because their name appears in the 2022 data under both sexes. Four details of the call are worth pulling apart:
#
# * `left_on` and `right_on` name the **key** column on each side. These are the values Polars compares to decide which rows belong together, and we need both forms because the two tables spell the same idea differently: `First Name` here, `Name` there.
# * The key columns are **coalesced** into one. The result carries `First Name` and no `Name` at all — one key column, under the left table's name. This catches people out: a column that was in the right table is simply not in the output. If you need it, keep a copy under another name before joining, or pass `coalesce=False` to hold on to both.
# * Columns that collide but are *not* keys are kept apart by suffixing the right one. Both tables have a `Year`, so the babies' year arrives as `Year_right`.
# * `maintain_order="left"` returns the rows in the order the left table had them. A join gives no ordering guarantee otherwise.
#
# ### Choosing a Join Strategy
#
# The `how=` argument decides what happens to rows that find no partner [(documentation)](https://docs.pola.rs/user-guide/transformations/joins/). Every strategy below is running the same comparison; they differ only in what they keep.
#
# * `how="inner"` (the default) keeps rows that match on both sides, the 156 rows above.
# * `how="left"` keeps every row of the left table, filling the right table's columns with `null` where there was no match. Here that gives 196 rows.
# * `how="full"` keeps everything from both tables. Key columns are *not* coalesced under this strategy unless you also pass `coalesce=True`.
# * `how="semi"` keeps the left rows that have a match, and only the left table's columns. 147 of the 187 rows in `elections` name a candidate whose first name some California baby was given in 2022.
# * `how="anti"` is its mirror image: the left rows with no match at all.
#
# That last one is a useful question in its own right. Which candidates have a first name that no California baby received in 2022?

# %% tags=["remove-input", "remove-output"] id="p2-join-anti"
elections.join(babynames_2022, left_on="First Name", right_on="Name", how="anti", maintain_order="left").head()


# %% [markdown]
# <!-- tab-twins:begin how="anti", maintain_order="left" -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections.join(babynames_2022, left_on="First Name", right_on="Name", how="anti", maintain_order="left").head()
# ```
#
# ```text
# shape: (5, 7)
# ┌──────┬──────────────────┬────────────────────┬──────────────┬────────┬───────────┬────────────┐
# │ Year ┆ Candidate        ┆ Party              ┆ Popular vote ┆ Result ┆ %         ┆ First Name │
# │ ---  ┆ ---              ┆ ---                ┆ ---          ┆ ---    ┆ ---       ┆ ---        │
# │ i64  ┆ str              ┆ str                ┆ i64          ┆ str    ┆ f64       ┆ str        │
# ╞══════╪══════════════════╪════════════════════╪══════════════╪════════╪═══════════╪════════════╡
# │ 1852 ┆ Winfield Scott   ┆ Whig               ┆ 1386942      ┆ loss   ┆ 44.056548 ┆ Winfield   │
# │ 1856 ┆ Millard Fillmore ┆ American           ┆ 873053       ┆ loss   ┆ 21.554001 ┆ Millard    │
# │ 1868 ┆ Horatio Seymour  ┆ Democratic         ┆ 2708744      ┆ loss   ┆ 47.334695 ┆ Horatio    │
# │ 1872 ┆ Horace Greeley   ┆ Liberal Republican ┆ 2834761      ┆ loss   ┆ 44.071406 ┆ Horace     │
# │ 1876 ┆ Rutherford Hayes ┆ Republican         ┆ 4034142      ┆ win    ┆ 48.471624 ┆ Rutherford │
# └──────┴──────────────────┴────────────────────┴──────────────┴────────┴───────────┴────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd[
#     ~elections_pd["First Name"].isin(babynames_2022_pd["Name"])
# ].head()
# ```
#
# ```text
#     Year         Candidate               Party  ...  Result          %  First Name
# 19  1852    Winfield Scott                Whig  ...    loss  44.056548    Winfield
# 22  1856  Millard Fillmore            American  ...    loss  21.554001     Millard
# 29  1868   Horatio Seymour          Democratic  ...    loss  47.334695     Horatio
# 31  1872    Horace Greeley  Liberal Republican  ...    loss  44.071406      Horace
# 33  1876  Rutherford Hayes          Republican  ...     win  48.471624  Rutherford
#
# [5 rows x 7 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="p2-parting"
# Forty rows, headed by Winfield Scott and Millard Fillmore. Since `semi` and `anti` joins answer a question about the left table rather than combining two of them, they return the left table's columns only — there is nothing from `babynames_2022` in this output.
#
# ## Parting Note
#
# Congratulations! We have now covered the core of Polars. Don't worry if you are still not feeling very comfortable with it — you will have plenty of chances to practice over the next few weeks, and the [user guide](https://docs.pola.rs/user-guide/expressions/aggregation/) shows these same operations written a few more ways.
#
# Next, we will get our hands dirty with some real-world datasets and use what we know to conduct some exploratory data analysis.
