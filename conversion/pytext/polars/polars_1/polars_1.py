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

# %% [markdown] id="25b4d24f"
# ---
# title: Polars I
# ---
#
# ::: {note} Learning Outcomes
# * Build a `DataFrame` from a file, a list of rows, a dictionary of columns, or a `Series`, and describe it with `columns`, `dtypes`, `schema`, and `shape`.
# * Extract rows and columns using `[]`, `select`, and `filter`.
# * Combine filtering conditions with the bitwise boolean operators.
# * Address rows by position, and record those positions with `with_row_index`.
# * Summarize a table with utility methods such as `.describe()`, `.sample()`, `.value_counts()`, and `.unique()`.
# * Add, modify, rename, and drop columns, and order a table with `.sort()`.
# :::
#
# Last time, we met the `Series`: a named, one-dimensional sequence of values that all share a single data type. Almost no dataset arrives as one column, so we now turn to the structure that holds a whole table, the `DataFrame`, and to the operations that get data into and out of it.
#
# We will work with two datasets in this chapter. The first records the results of United States presidential elections; the second records the names given to babies born in California.
#
# Some sections below show the same operation both ways. Pick a library here and every comparison
# on this page follows it.
#
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# Comparisons on this page are showing **Polars**. This is the library the course uses.
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# Comparisons on this page are showing **pandas**, for readers arriving from it. The course itself
# uses Polars throughout.
# ::::
# :::::

# %% tags=["remove-input", "remove-output"] id="1c442585"
# `pl` is the conventional alias for Polars, as `np` is for NumPy
import polars as pl


# %% [markdown] id="9db5657e"
# <!-- tab-twins:begin import polars as pl -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # `pl` is the conventional alias for Polars, as `np` is for NumPy
# import polars as pl
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # `pd` is the conventional alias for pandas, as `np` is for NumPy
# import pandas as pd
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="58b0c4f2"
# ## `DataFrame`s and `Series`
#
# A `DataFrame` is a two-dimensional table of data with named columns, where each row is identified by its position in the table. Every column of a `DataFrame` is a `Series`, and a `DataFrame` is a collection of `Series` that all have the same length.
#
# A `DataFrame` can be created from scratch or loaded from a file. We'll cover four of the many ways of doing so:
#
# 1. From a CSV file.
# 2. From a list of rows.
# 3. From a dictionary of columns.
# 4. From a `Series`.
#
# ### From a CSV File
#
# Polars reads a number of file formats. We will use `read_csv` throughout the course to load a comma-separated file into a `DataFrame`.

# %% tags=["remove-input", "remove-output"] id="b30b8999"
elections = pl.read_csv("data/elections.csv")
elections


# %% [markdown] id="d331d68b"
# <!-- tab-twins:begin elections = pl.read_csv("data/elections.csv") -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections = pl.read_csv("data/elections.csv")
# elections
# ```
#
# ```text
# shape: (182, 6)
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
# │ …    ┆ …                 ┆ …                     ┆ …            ┆ …      ┆ …         │
# │ 2016 ┆ Jill Stein        ┆ Green                 ┆ 1457226      ┆ loss   ┆ 1.073699  │
# │ 2020 ┆ Joseph Biden      ┆ Democratic            ┆ 81268924     ┆ win    ┆ 51.311515 │
# │ 2020 ┆ Donald Trump      ┆ Republican            ┆ 74216154     ┆ loss   ┆ 46.858542 │
# │ 2020 ┆ Jo Jorgensen      ┆ Libertarian           ┆ 1865724      ┆ loss   ┆ 1.1779795 │
# │ 2020 ┆ Howard Hawkins    ┆ Green                 ┆ 405035       ┆ loss   ┆ 0.255731  │
# └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd = pd.read_csv("data/elections.csv")
# elections_pd
# ```
#
# ```text
#      Year          Candidate  ... Result          %
# 0    1824     Andrew Jackson  ...   loss  57.210122
# 1    1824  John Quincy Adams  ...    win  42.789878
# 2    1828     Andrew Jackson  ...    win  56.203927
# 3    1828  John Quincy Adams  ...   loss  43.796073
# 4    1832     Andrew Jackson  ...    win  54.574789
# ..    ...                ...  ...    ...        ...
# 177  2016         Jill Stein  ...   loss   1.073699
# 178  2020       Joseph Biden  ...    win  51.311515
# 179  2020       Donald Trump  ...   loss  46.858542
# 180  2020       Jo Jorgensen  ...   loss   1.177979
# 181  2020     Howard Hawkins  ...   loss   0.255731
#
# [182 rows x 6 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="97423f5f"
# The code above stores our `DataFrame` object in the `elections` variable. Upon inspection, our `elections` `DataFrame` has 182 rows and 6 columns (`Year`, `Candidate`, `Party`, `Popular vote`, `Result`, `%`). Each row represents a single record — in our example, a presidential candidate from some particular year. Each column represents a single attribute or feature of the record.
#
# Notice the three lines Polars prints above the data itself. The first gives the shape of the table, the second names the columns, and the third gives the data type of each column: `str` for the text columns, `i64` for whole numbers, `f64` for decimals. Every table you print tells you how big it is and what it holds.
#
# `read_csv` also takes optional arguments that shape the table as it is read.

# %% tags=["remove-input", "remove-output"] id="3093ab49"
# `columns` chooses which columns to read; they arrive in file order, not the order named here
pl.read_csv("data/elections.csv", columns=["Candidate", "Year", "%"])


# %% [markdown] id="2107958a"
# <!-- tab-twins:begin pl.read_csv("data/elections.csv", columns=["Candidate", "Year", "%"]) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # `columns` chooses which columns to read; they arrive in file order, not the order named here
# pl.read_csv("data/elections.csv", columns=["Candidate", "Year", "%"])
# ```
#
# ```text
# shape: (182, 3)
# ┌──────┬───────────────────┬───────────┐
# │ Year ┆ Candidate         ┆ %         │
# │ ---  ┆ ---               ┆ ---       │
# │ i64  ┆ str               ┆ f64       │
# ╞══════╪═══════════════════╪═══════════╡
# │ 1824 ┆ Andrew Jackson    ┆ 57.210122 │
# │ 1824 ┆ John Quincy Adams ┆ 42.789878 │
# │ 1828 ┆ Andrew Jackson    ┆ 56.203927 │
# │ 1828 ┆ John Quincy Adams ┆ 43.796073 │
# │ 1832 ┆ Andrew Jackson    ┆ 54.574789 │
# │ …    ┆ …                 ┆ …         │
# │ 2016 ┆ Jill Stein        ┆ 1.073699  │
# │ 2020 ┆ Joseph Biden      ┆ 51.311515 │
# │ 2020 ┆ Donald Trump      ┆ 46.858542 │
# │ 2020 ┆ Jo Jorgensen      ┆ 1.1779795 │
# │ 2020 ┆ Howard Hawkins    ┆ 0.255731  │
# └──────┴───────────────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# pd.read_csv("data/elections.csv", usecols=["Candidate", "Year", "%"])
# ```
#
# ```text
#      Year          Candidate          %
# 0    1824     Andrew Jackson  57.210122
# 1    1824  John Quincy Adams  42.789878
# 2    1828     Andrew Jackson  56.203927
# 3    1828  John Quincy Adams  43.796073
# 4    1832     Andrew Jackson  54.574789
# ..    ...                ...        ...
# 177  2016         Jill Stein   1.073699
# 178  2020       Joseph Biden  51.311515
# 179  2020       Donald Trump  46.858542
# 180  2020       Jo Jorgensen   1.177979
# 181  2020     Howard Hawkins   0.255731
#
# [182 rows x 3 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% tags=["remove-input", "remove-output"] id="bb730f16"
# `n_rows` stops reading after the first few rows, which is handy for a very large file
pl.read_csv("data/elections.csv", n_rows=5)


# %% [markdown] id="4795d09b"
# <!-- tab-twins:begin pl.read_csv("data/elections.csv", n_rows=5) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # `n_rows` stops reading after the first few rows, which is handy for a very large file
# pl.read_csv("data/elections.csv", n_rows=5)
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
# pd.read_csv("data/elections.csv", nrows=5)
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

# %% [markdown] id="49d18268"
# ### From a List of Rows
#
# We'll now explore creating a `DataFrame` with data of our own. The two cells below build the same two-row table of fruit prices, one row at a time.
#
# The first passes a list of lists. `schema` names the columns, and `orient="row"` tells Polars to read each inner list as a row rather than as a column.

# %% tags=["remove-input", "remove-output"] id="340731ba"
df_list_1 = pl.DataFrame(
    [["Kiwi", 5.49],
     ["Orange", 3.99]],
    schema=["Fruit", "Price"], orient="row"
)
df_list_1


# %% [markdown] id="67979e35"
# <!-- tab-twins:begin df_list_1 = pl.DataFrame( -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# df_list_1 = pl.DataFrame(
#     [["Kiwi", 5.49],
#      ["Orange", 3.99]],
#     schema=["Fruit", "Price"], orient="row"
# )
# df_list_1
# ```
#
# ```text
# shape: (2, 2)
# ┌────────┬───────┐
# │ Fruit  ┆ Price │
# │ ---    ┆ ---   │
# │ str    ┆ f64   │
# ╞════════╪═══════╡
# │ Kiwi   ┆ 5.49  │
# │ Orange ┆ 3.99  │
# └────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# df_list_1_pd = pd.DataFrame(
#     [["Kiwi", 5.49],
#      ["Orange", 3.99]],
#     columns=["Fruit", "Price"]
# )
# df_list_1_pd
# ```
#
# ```text
#     Fruit  Price
# 0    Kiwi   5.49
# 1  Orange   3.99
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="21078267"
# The second passes a list of dictionaries. Each dictionary is a row, and its keys supply the column names, so there is no schema to write out.

# %% tags=["remove-input", "remove-output"] id="9fad839e"
df_list_2 = pl.DataFrame(
    [{"Fruit": "Kiwi", "Price": 5.49},
     {"Fruit": "Orange", "Price": 3.99}]
)
df_list_2


# %% [markdown] id="45d489c4"
# <!-- tab-twins:begin df_list_2 = pl.DataFrame( -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# df_list_2 = pl.DataFrame(
#     [{"Fruit": "Kiwi", "Price": 5.49},
#      {"Fruit": "Orange", "Price": 3.99}]
# )
# df_list_2
# ```
#
# ```text
# shape: (2, 2)
# ┌────────┬───────┐
# │ Fruit  ┆ Price │
# │ ---    ┆ ---   │
# │ str    ┆ f64   │
# ╞════════╪═══════╡
# │ Kiwi   ┆ 5.49  │
# │ Orange ┆ 3.99  │
# └────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# df_list_2_pd = pd.DataFrame(
#     [{"Fruit": "Kiwi", "Price": 5.49},
#      {"Fruit": "Orange", "Price": 3.99}]
# )
# df_list_2_pd
# ```
#
# ```text
#     Fruit  Price
# 0    Kiwi   5.49
# 1  Orange   3.99
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="8e1c361d"
# ### From a Dictionary of Columns
#
# A dictionary describes the table by column instead of by row: each key is a column name, and each value holds that column's data.

# %% tags=["remove-input", "remove-output"] id="3408cdde"
df_dict = pl.DataFrame(
    {"Fruit": ["Kiwi", "Orange"],
     "Price": [5.49, 3.99]}
)
df_dict


# %% [markdown] id="ed033769"
# <!-- tab-twins:begin df_dict = pl.DataFrame( -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# df_dict = pl.DataFrame(
#     {"Fruit": ["Kiwi", "Orange"],
#      "Price": [5.49, 3.99]}
# )
# df_dict
# ```
#
# ```text
# shape: (2, 2)
# ┌────────┬───────┐
# │ Fruit  ┆ Price │
# │ ---    ┆ ---   │
# │ str    ┆ f64   │
# ╞════════╪═══════╡
# │ Kiwi   ┆ 5.49  │
# │ Orange ┆ 3.99  │
# └────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# df_dict_pd = pd.DataFrame(
#     {"Fruit": ["Kiwi", "Orange"],
#      "Price": [5.49, 3.99]}
# )
# df_dict_pd
# ```
#
# ```text
#     Fruit  Price
# 0    Kiwi   5.49
# 1  Orange   3.99
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="981a5a50"
# ### From a `Series`
#
# Since a `DataFrame` is a collection of equal-length `Series`, we can build one out of `Series` we already have. Consider `ser_a` and `ser_b`.

# %% tags=["remove-input", "remove-output"] id="304e0525"
ser_a = pl.Series("ser_a", ["a1", "a2", "a3"])
ser_b = pl.Series("ser_b", ["b1", "b2", "b3"])
ser_a


# %% [markdown] id="94141424"
# <!-- tab-twins:begin ser_a = pl.Series("ser_a", ["a1", "a2", "a3"]) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# ser_a = pl.Series("ser_a", ["a1", "a2", "a3"])
# ser_b = pl.Series("ser_b", ["b1", "b2", "b3"])
# ser_a
# ```
#
# ```text
# shape: (3,)
# Series: 'ser_a' [str]
# [
# 	"a1"
# 	"a2"
# 	"a3"
# ]
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# ser_a_pd = pd.Series(["a1", "a2", "a3"], name="ser_a")
# ser_b_pd = pd.Series(["b1", "b2", "b3"], name="ser_b")
# ser_a_pd
# ```
#
# ```text
# 0    a1
# 1    a2
# 2    a3
# Name: ser_a, dtype: object
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="dbb5b8bc"
# Passing them in a dictionary puts them side by side, under whatever column names we choose.

# %% tags=["remove-input", "remove-output"] id="d1d42c64"
pl.DataFrame(
    {"ColumnA": ser_a, "ColumnB": ser_b}
)


# %% [markdown] id="eb647b8f"
# <!-- tab-twins:begin {"ColumnA": ser_a, "ColumnB": ser_b} -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# pl.DataFrame(
#     {"ColumnA": ser_a, "ColumnB": ser_b}
# )
# ```
#
# ```text
# shape: (3, 2)
# ┌─────────┬─────────┐
# │ ColumnA ┆ ColumnB │
# │ ---     ┆ ---     │
# │ str     ┆ str     │
# ╞═════════╪═════════╡
# │ a1      ┆ b1      │
# │ a2      ┆ b2      │
# │ a3      ┆ b3      │
# └─────────┴─────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# pd.DataFrame(
#     {"ColumnA": ser_a_pd, "ColumnB": ser_b_pd}
# )
# ```
#
# ```text
#   ColumnA ColumnB
# 0      a1      b1
# 1      a2      b2
# 2      a3      b3
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="e3020963"
# A single `Series` makes a one-column `DataFrame`, either by handing it to the constructor or by calling `.to_frame()` on it. Either way, the name of the `Series` becomes the name of the column.

# %% tags=["remove-input", "remove-output"] id="18855ea8"
pl.DataFrame(ser_a)


# %% [markdown] id="599b3601"
# <!-- tab-twins:begin pl.DataFrame(ser_a) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# pl.DataFrame(ser_a)
# ```
#
# ```text
# shape: (3, 1)
# ┌───────┐
# │ ser_a │
# │ ---   │
# │ str   │
# ╞═══════╡
# │ a1    │
# │ a2    │
# │ a3    │
# └───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# pd.DataFrame(ser_a_pd)
# ```
#
# ```text
#   ser_a
# 0    a1
# 1    a2
# 2    a3
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% tags=["remove-input", "remove-output"] id="4b73724f"
ser_a.to_frame()


# %% [markdown] id="caf20aa4"
# <!-- tab-twins:begin ser_a.to_frame() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# ser_a.to_frame()
# ```
#
# ```text
# shape: (3, 1)
# ┌───────┐
# │ ser_a │
# │ ---   │
# │ str   │
# ╞═══════╡
# │ a1    │
# │ a2    │
# │ a3    │
# └───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# ser_a_pd.to_frame()
# ```
#
# ```text
#   ser_a
# 0    a1
# 1    a2
# 2    a3
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="89209a13"
# ## `DataFrame` Attributes: `columns`, `dtypes`, and `shape`
#
# Column names in a `DataFrame` are almost always unique. Looking back to the `elections` dataset, it wouldn't make sense to have two columns named `"Candidate"`. Sometimes you'll want to extract the names, the types, or the size of a table rather than the data itself, most often when meeting a dataset for the first time.
#
# For the column names, use `DataFrame.columns`:

# %% tags=["remove-input", "remove-output"] id="7f746d89"
elections.columns


# %% [markdown] id="dc5641a8"
# <!-- tab-twins:begin elections.columns -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections.columns
# ```
#
# ```text
# ['Year', 'Candidate', 'Party', 'Popular vote', 'Result', '%']
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.columns
# ```
#
# ```text
# Index(['Year', 'Candidate', 'Party', 'Popular vote', 'Result', '%'], dtype='object')
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="d78d08c3"
# For the data type of each column, use `DataFrame.dtypes`. The types come back in the same order as the names above.

# %% tags=["remove-input", "remove-output"] id="a2f55f5a"
elections.dtypes


# %% [markdown] id="2067bab2"
# <!-- tab-twins:begin elections.dtypes -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections.dtypes
# ```
#
# ```text
# [Int64, String, String, Int64, String, Float64]
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.dtypes
# ```
#
# ```text
# Year              int64
# Candidate        object
# Party            object
# Popular vote      int64
# Result           object
# %               float64
# dtype: object
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="3dd70041"
# `DataFrame.schema` reports both at once, pairing each column with its type. This is the quickest way to check that a file was read the way you expected: that a column of years arrived as `Int64` rather than as `String`, for instance.

# %% tags=["remove-input", "remove-output"] id="d77b992c"
elections.schema


# %% [markdown] id="72454ae1"
# <!-- tab-twins:begin elections.schema -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections.schema
# ```
#
# ```text
# Schema([('Year', Int64),
#         ('Candidate', String),
#         ('Party', String),
#         ('Popular vote', Int64),
#         ('Result', String),
#         ('%', Float64)])
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.dtypes.to_dict()
# ```
#
# ```text
# {'Year': dtype('int64'),
#  'Candidate': dtype('O'),
#  'Party': dtype('O'),
#  'Popular vote': dtype('int64'),
#  'Result': dtype('O'),
#  '%': dtype('float64')}
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="357cdcd1"
# And for the size of the `DataFrame`, `DataFrame.shape` gives the number of rows followed by the number of columns:

# %% id="de7741d5"
elections.shape

# %% [markdown] id="c97a340e"
# ## Extracting Data from a `DataFrame`
#
# Now that we've learned more about `DataFrame`s, let's dive deeper into their capabilities.
#
# The API (Application Programming Interface) for the `DataFrame` class is enormous. In this section, we'll discuss several methods of the `DataFrame` API that allow us to extract subsets of data.
#
# The simplest way to manipulate a `DataFrame` is to extract a subset of rows and columns, known as **slicing**.
#
# Common ways we may want to extract data are grabbing:
#
# - The first or last `n` rows in the `DataFrame`.
# - Data at a certain position.
# - Data satisfying some condition.
#
# We will do so with three primary tools of the `DataFrame` class:
#
# 1. `.head` and `.tail`
# 2. `[]`
# 3. `filter` and `select`
#
# ### Extracting Data with `.head` and `.tail`
#
# The simplest scenario in which we want to extract data is when we simply want to select the first or last few rows of the `DataFrame`.
#
# To extract the first `n` rows of a `DataFrame` `df`, we use the syntax `df.head(n)`. Called with no argument at all, `.head` gives us five.

# %% tags=["remove-input", "remove-output"] id="5e522140"
# Extract the first 5 rows of the DataFrame
elections.head()


# %% [markdown] id="46a72c89"
# <!-- tab-twins:begin elections.head() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Extract the first 5 rows of the DataFrame
# elections.head()
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
# elections_pd.head()
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

# %% [markdown] id="573b87b4"
# Similarly, calling `df.tail(n)` allows us to extract the last `n` rows of the `DataFrame`.

# %% tags=["remove-input", "remove-output"] id="3f9bd208"
# Extract the last 5 rows of the DataFrame
elections.tail(5)


# %% [markdown] id="17b531c5"
# <!-- tab-twins:begin elections.tail(5) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Extract the last 5 rows of the DataFrame
# elections.tail(5)
# ```
#
# ```text
# shape: (5, 6)
# ┌──────┬────────────────┬─────────────┬──────────────┬────────┬───────────┐
# │ Year ┆ Candidate      ┆ Party       ┆ Popular vote ┆ Result ┆ %         │
# │ ---  ┆ ---            ┆ ---         ┆ ---          ┆ ---    ┆ ---       │
# │ i64  ┆ str            ┆ str         ┆ i64          ┆ str    ┆ f64       │
# ╞══════╪════════════════╪═════════════╪══════════════╪════════╪═══════════╡
# │ 2016 ┆ Jill Stein     ┆ Green       ┆ 1457226      ┆ loss   ┆ 1.073699  │
# │ 2020 ┆ Joseph Biden   ┆ Democratic  ┆ 81268924     ┆ win    ┆ 51.311515 │
# │ 2020 ┆ Donald Trump   ┆ Republican  ┆ 74216154     ┆ loss   ┆ 46.858542 │
# │ 2020 ┆ Jo Jorgensen   ┆ Libertarian ┆ 1865724      ┆ loss   ┆ 1.1779795 │
# │ 2020 ┆ Howard Hawkins ┆ Green       ┆ 405035       ┆ loss   ┆ 0.255731  │
# └──────┴────────────────┴─────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.tail(5)
# ```
#
# ```text
#      Year       Candidate        Party  Popular vote Result          %
# 177  2016      Jill Stein        Green       1457226   loss   1.073699
# 178  2020    Joseph Biden   Democratic      81268924    win  51.311515
# 179  2020    Donald Trump   Republican      74216154   loss  46.858542
# 180  2020    Jo Jorgensen  Libertarian       1865724   loss   1.177979
# 181  2020  Howard Hawkins        Green        405035   loss   0.255731
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="0d9e8c1f"
# ### Extraction with `[]`
#
# The `[]` selection operator takes up to two arguments: the first names the rows we want, and the second names the columns. It selects rows by **position**, counting from 0 in the order the rows currently sit in the table, and columns by **label**.
#
# Each argument to `[]` can be:
#
# 1. A single value.
# 2. A list.
# 3. A slice. A slice of row positions is **exclusive** of its right-hand side, exactly like ordinary Python indexing, while a slice of column labels is **inclusive** of both of its ends.
#
# For example, to select a single value, we can ask for the row at position `0` and the column labeled `Candidate`.

# %% tags=["remove-input", "remove-output"] id="ae0fa1ba"
elections[0, "Candidate"]


# %% [markdown] id="95ae9af9"
# <!-- tab-twins:begin elections[0, "Candidate"] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections[0, "Candidate"]
# ```
#
# ```text
# 'Andrew Jackson'
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.loc[0, "Candidate"]
# ```
#
# ```text
# 'Andrew Jackson'
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="86dc040c"
# Two single values pick out one cell, and what comes back is the value sitting in it: here, the string `'Andrew Jackson'`.
#
# Two lists pick out a rectangle of the table. The rows arrive in the order we asked for them rather than in table order.

# %% tags=["remove-input", "remove-output"] id="47d72677"
elections[[87, 25, 179], ["Year", "Party", "%"]]


# %% [markdown] id="8b99844c"
# <!-- tab-twins:begin elections[[87, 25, 179], ["Year", "Party", "%"]] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections[[87, 25, 179], ["Year", "Party", "%"]]
# ```
#
# ```text
# shape: (3, 3)
# ┌──────┬─────────────────────┬───────────┐
# │ Year ┆ Party               ┆ %         │
# │ ---  ┆ ---                 ┆ ---       │
# │ i64  ┆ str                 ┆ f64       │
# ╞══════╪═════════════════════╪═══════════╡
# │ 1932 ┆ Republican          ┆ 39.830594 │
# │ 1860 ┆ Southern Democratic ┆ 18.138998 │
# │ 2020 ┆ Republican          ┆ 46.858542 │
# └──────┴─────────────────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.loc[[87, 25, 179], ["Year", "Party", "%"]]
# ```
#
# ```text
#      Year                Party          %
# 87   1932           Republican  39.830594
# 25   1860  Southern Democratic  18.138998
# 179  2020           Republican  46.858542
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="10f474bc"
# A slice of column labels runs from one column to another and includes both ends. `"%"` is the last column of `elections`, and it appears in the result below.

# %% tags=["remove-input", "remove-output"] id="334bf7ef"
elections[[87, 25, 179], "Popular vote":"%"]


# %% [markdown] id="2adfccb2"
# <!-- tab-twins:begin elections[[87, 25, 179], "Popular vote":"%"] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections[[87, 25, 179], "Popular vote":"%"]
# ```
#
# ```text
# shape: (3, 3)
# ┌──────────────┬────────┬───────────┐
# │ Popular vote ┆ Result ┆ %         │
# │ ---          ┆ ---    ┆ ---       │
# │ i64          ┆ str    ┆ f64       │
# ╞══════════════╪════════╪═══════════╡
# │ 15761254     ┆ loss   ┆ 39.830594 │
# │ 848019       ┆ loss   ┆ 18.138998 │
# │ 74216154     ┆ loss   ┆ 46.858542 │
# └──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.loc[[87, 25, 179], "Popular vote":"%"]
# ```
#
# ```text
#      Popular vote Result          %
# 87       15761254   loss  39.830594
# 25         848019   loss  18.138998
# 179      74216154   loss  46.858542
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="735d0b76"
# Suppose instead that we want *all* rows and only a few columns. The shorthand `:` is useful for this.

# %% tags=["remove-input", "remove-output"] id="496493f7"
elections[:, ["Year", "Candidate", "Result"]]


# %% [markdown] id="25d0aa20"
# <!-- tab-twins:begin elections[:, ["Year", "Candidate", "Result"]] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections[:, ["Year", "Candidate", "Result"]]
# ```
#
# ```text
# shape: (182, 3)
# ┌──────┬───────────────────┬────────┐
# │ Year ┆ Candidate         ┆ Result │
# │ ---  ┆ ---               ┆ ---    │
# │ i64  ┆ str               ┆ str    │
# ╞══════╪═══════════════════╪════════╡
# │ 1824 ┆ Andrew Jackson    ┆ loss   │
# │ 1824 ┆ John Quincy Adams ┆ win    │
# │ 1828 ┆ Andrew Jackson    ┆ win    │
# │ 1828 ┆ John Quincy Adams ┆ loss   │
# │ 1832 ┆ Andrew Jackson    ┆ win    │
# │ …    ┆ …                 ┆ …      │
# │ 2016 ┆ Jill Stein        ┆ loss   │
# │ 2020 ┆ Joseph Biden      ┆ win    │
# │ 2020 ┆ Donald Trump      ┆ loss   │
# │ 2020 ┆ Jo Jorgensen      ┆ loss   │
# │ 2020 ┆ Howard Hawkins    ┆ loss   │
# └──────┴───────────────────┴────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd[["Year", "Candidate", "Result"]]
# ```
#
# ```text
#      Year          Candidate Result
# 0    1824     Andrew Jackson   loss
# 1    1824  John Quincy Adams    win
# 2    1828     Andrew Jackson    win
# 3    1828  John Quincy Adams   loss
# 4    1832     Andrew Jackson    win
# ..    ...                ...    ...
# 177  2016         Jill Stein   loss
# 178  2020       Joseph Biden    win
# 179  2020       Donald Trump   loss
# 180  2020       Jo Jorgensen   loss
# 181  2020     Howard Hawkins   loss
#
# [182 rows x 3 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="36043c7d"
# We can use the same shorthand to ask for all columns.

# %% tags=["remove-input", "remove-output"] id="4c335442"
elections[[87, 25, 179], :]


# %% [markdown] id="ed13481b"
# <!-- tab-twins:begin elections[[87, 25, 179], :] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections[[87, 25, 179], :]
# ```
#
# ```text
# shape: (3, 6)
# ┌──────┬──────────────────────┬─────────────────────┬──────────────┬────────┬───────────┐
# │ Year ┆ Candidate            ┆ Party               ┆ Popular vote ┆ Result ┆ %         │
# │ ---  ┆ ---                  ┆ ---                 ┆ ---          ┆ ---    ┆ ---       │
# │ i64  ┆ str                  ┆ str                 ┆ i64          ┆ str    ┆ f64       │
# ╞══════╪══════════════════════╪═════════════════════╪══════════════╪════════╪═══════════╡
# │ 1932 ┆ Herbert Hoover       ┆ Republican          ┆ 15761254     ┆ loss   ┆ 39.830594 │
# │ 1860 ┆ John C. Breckinridge ┆ Southern Democratic ┆ 848019       ┆ loss   ┆ 18.138998 │
# │ 2020 ┆ Donald Trump         ┆ Republican          ┆ 74216154     ┆ loss   ┆ 46.858542 │
# └──────┴──────────────────────┴─────────────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.loc[[87, 25, 179]]
# ```
#
# ```text
#      Year             Candidate  ... Result          %
# 87   1932        Herbert Hoover  ...   loss  39.830594
# 25   1860  John C. Breckinridge  ...   loss  18.138998
# 179  2020          Donald Trump  ...   loss  46.858542
#
# [3 rows x 6 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="2f22dba6"
# A single column label returns that column as a `Series`.

# %% tags=["remove-input", "remove-output"] id="4126ef9d"
elections[[87, 25, 179], "Popular vote"]


# %% [markdown] id="8bad130a"
# <!-- tab-twins:begin elections[[87, 25, 179], "Popular vote"] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections[[87, 25, 179], "Popular vote"]
# ```
#
# ```text
# shape: (3,)
# Series: 'Popular vote' [i64]
# [
# 	15761254
# 	848019
# 	74216154
# ]
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.loc[[87, 25, 179], "Popular vote"]
# ```
#
# ```text
# 87     15761254
# 25       848019
# 179    74216154
# Name: Popular vote, dtype: int64
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="47259a34"
# Wrapping that same label in a list asks for a table of one column, and a table of one column is what comes back.

# %% tags=["remove-input", "remove-output"] id="b010aade"
elections[[87, 25, 179], ["Popular vote"]]


# %% [markdown] id="a9883a51"
# <!-- tab-twins:begin elections[[87, 25, 179], ["Popular vote"]] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections[[87, 25, 179], ["Popular vote"]]
# ```
#
# ```text
# shape: (3, 1)
# ┌──────────────┐
# │ Popular vote │
# │ ---          │
# │ i64          │
# ╞══════════════╡
# │ 15761254     │
# │ 848019       │
# │ 74216154     │
# └──────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.loc[[87, 25, 179], ["Popular vote"]]
# ```
#
# ```text
#      Popular vote
# 87       15761254
# 25         848019
# 179      74216154
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="5b3744da"
# When `[]` is given only one argument, and that argument is a list of integers or a slice, Polars reads it as rows and hands back every column.

# %% tags=["remove-input", "remove-output"] id="7c9c0870"
elections[[180, 181]]


# %% [markdown] id="fdd177b8"
# <!-- tab-twins:begin elections[[180, 181]] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections[[180, 181]]
# ```
#
# ```text
# shape: (2, 6)
# ┌──────┬────────────────┬─────────────┬──────────────┬────────┬───────────┐
# │ Year ┆ Candidate      ┆ Party       ┆ Popular vote ┆ Result ┆ %         │
# │ ---  ┆ ---            ┆ ---         ┆ ---          ┆ ---    ┆ ---       │
# │ i64  ┆ str            ┆ str         ┆ i64          ┆ str    ┆ f64       │
# ╞══════╪════════════════╪═════════════╪══════════════╪════════╪═══════════╡
# │ 2020 ┆ Jo Jorgensen   ┆ Libertarian ┆ 1865724      ┆ loss   ┆ 1.1779795 │
# │ 2020 ┆ Howard Hawkins ┆ Green       ┆ 405035       ┆ loss   ┆ 0.255731  │
# └──────┴────────────────┴─────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.iloc[[180, 181]]
# ```
#
# ```text
#      Year       Candidate        Party  Popular vote Result         %
# 180  2020    Jo Jorgensen  Libertarian       1865724   loss  1.177979
# 181  2020  Howard Hawkins        Green        405035   loss  0.255731
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="07b9c28a"
# A single argument that is a *string*, on the other hand, names a column, and that column comes back as a `Series`. This is the shorthand we use whenever we want one column and nothing else, and it shows up throughout the rest of the chapter.

# %% tags=["remove-input", "remove-output"] id="d5a72acb"
elections["Candidate"]


# %% [markdown] id="a0f3a1ba"
# <!-- tab-twins:begin elections["Candidate"] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections["Candidate"]
# ```
#
# ```text
# shape: (182,)
# Series: 'Candidate' [str]
# [
# 	"Andrew Jackson"
# 	"John Quincy Adams"
# 	"Andrew Jackson"
# 	"John Quincy Adams"
# 	"Andrew Jackson"
# 	…
# 	"Jill Stein"
# 	"Joseph Biden"
# 	"Donald Trump"
# 	"Jo Jorgensen"
# 	"Howard Hawkins"
# ]
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd["Candidate"]
# ```
#
# ```text
# 0         Andrew Jackson
# 1      John Quincy Adams
# 2         Andrew Jackson
# 3      John Quincy Adams
# 4         Andrew Jackson
#              ...
# 177           Jill Stein
# 178         Joseph Biden
# 179         Donald Trump
# 180         Jo Jorgensen
# 181       Howard Hawkins
# Name: Candidate, Length: 182, dtype: object
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="dfecff0b"
# #### Selecting Columns by Position
#
# The second argument to `[]` accepts **column numbers** as well as column labels. The numbers count from the left edge of the table, starting at 0, so `elections[:, 1]` and `elections[:, "Candidate"]` name the same column.
#
# Slicing by column number, like slicing by row position, is **exclusive** of the right-hand side of the slice. The inclusive behavior we saw above belongs to label slices only.

# %% tags=["remove-input", "remove-output"] id="1f2bceeb"
# Extracting the value at the first row (row 0) and the second column
# Remember that Python indexing begins at position 0!
elections[0, 1]


# %% [markdown] id="7177a19f"
# <!-- tab-twins:begin elections[0, 1] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Extracting the value at the first row (row 0) and the second column
# # Remember that Python indexing begins at position 0!
# elections[0, 1]
# ```
#
# ```text
# 'Andrew Jackson'
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.iloc[0, 1]
# ```
#
# ```text
# 'Andrew Jackson'
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% tags=["remove-input", "remove-output"] id="3ea5558b"
# Extracting the second, third, and fourth rows of the second column
# (returns a Series, since we asked for a single column)
elections[[1, 2, 3], 1]


# %% [markdown] id="bff4e353"
# <!-- tab-twins:begin elections[[1, 2, 3], 1] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Extracting the second, third, and fourth rows of the second column
# # (returns a Series, since we asked for a single column)
# elections[[1, 2, 3], 1]
# ```
#
# ```text
# shape: (3,)
# Series: 'Candidate' [str]
# [
# 	"John Quincy Adams"
# 	"Andrew Jackson"
# 	"John Quincy Adams"
# ]
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.iloc[[1, 2, 3], 1]
# ```
#
# ```text
# 1    John Quincy Adams
# 2       Andrew Jackson
# 3    John Quincy Adams
# Name: Candidate, dtype: object
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% tags=["remove-input", "remove-output"] id="7a46e3b5"
# Select the rows at positions 1, 2, and 3
# Select the columns at positions 0, 1, and 2
elections[[1, 2, 3], [0, 1, 2]]


# %% [markdown] id="ff57f9b0"
# <!-- tab-twins:begin elections[[1, 2, 3], [0, 1, 2]] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Select the rows at positions 1, 2, and 3
# # Select the columns at positions 0, 1, and 2
# elections[[1, 2, 3], [0, 1, 2]]
# ```
#
# ```text
# shape: (3, 3)
# ┌──────┬───────────────────┬───────────────────────┐
# │ Year ┆ Candidate         ┆ Party                 │
# │ ---  ┆ ---               ┆ ---                   │
# │ i64  ┆ str               ┆ str                   │
# ╞══════╪═══════════════════╪═══════════════════════╡
# │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican │
# │ 1828 ┆ Andrew Jackson    ┆ Democratic            │
# │ 1828 ┆ John Quincy Adams ┆ National Republican   │
# └──────┴───────────────────┴───────────────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.iloc[[1, 2, 3], [0, 1, 2]]
# ```
#
# ```text
#    Year          Candidate                  Party
# 1  1824  John Quincy Adams  Democratic-Republican
# 2  1828     Andrew Jackson             Democratic
# 3  1828  John Quincy Adams    National Republican
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% tags=["remove-input", "remove-output"] id="69f3c204"
# A list of row positions and a slice of column numbers
# The column at position 3 is left out, since number slices are exclusive
elections[[1, 2, 3], 0:3]


# %% [markdown] id="4bce6905"
# <!-- tab-twins:begin elections[[1, 2, 3], 0:3] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # A list of row positions and a slice of column numbers
# # The column at position 3 is left out, since number slices are exclusive
# elections[[1, 2, 3], 0:3]
# ```
#
# ```text
# shape: (3, 3)
# ┌──────┬───────────────────┬───────────────────────┐
# │ Year ┆ Candidate         ┆ Party                 │
# │ ---  ┆ ---               ┆ ---                   │
# │ i64  ┆ str               ┆ str                   │
# ╞══════╪═══════════════════╪═══════════════════════╡
# │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican │
# │ 1828 ┆ Andrew Jackson    ┆ Democratic            │
# │ 1828 ┆ John Quincy Adams ┆ National Republican   │
# └──────┴───────────────────┴───────────────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.iloc[[1, 2, 3], 0:3]
# ```
#
# ```text
#    Year          Candidate                  Party
# 1  1824  John Quincy Adams  Democratic-Republican
# 2  1828     Andrew Jackson             Democratic
# 3  1828  John Quincy Adams    National Republican
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% tags=["remove-input", "remove-output"] id="396e7319"
# One argument, so Polars reads it as rows and returns all columns
elections[138:144]


# %% [markdown] id="c7703675"
# <!-- tab-twins:begin elections[138:144] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # One argument, so Polars reads it as rows and returns all columns
# elections[138:144]
# ```
#
# ```text
# shape: (6, 6)
# ┌──────┬───────────────────┬─────────────┬──────────────┬────────┬───────────┐
# │ Year ┆ Candidate         ┆ Party       ┆ Popular vote ┆ Result ┆ %         │
# │ ---  ┆ ---               ┆ ---         ┆ ---          ┆ ---    ┆ ---       │
# │ i64  ┆ str               ┆ str         ┆ i64          ┆ str    ┆ f64       │
# ╞══════╪═══════════════════╪═════════════╪══════════════╪════════╪═══════════╡
# │ 1988 ┆ Ron Paul          ┆ Libertarian ┆ 431750       ┆ loss   ┆ 0.47266   │
# │ 1992 ┆ Andre Marrou      ┆ Libertarian ┆ 290087       ┆ loss   ┆ 0.278516  │
# │ 1992 ┆ Bill Clinton      ┆ Democratic  ┆ 44909806     ┆ win    ┆ 43.118485 │
# │ 1992 ┆ Bo Gritz          ┆ Populist    ┆ 106152       ┆ loss   ┆ 0.101918  │
# │ 1992 ┆ George H. W. Bush ┆ Republican  ┆ 39104550     ┆ loss   ┆ 37.544784 │
# │ 1992 ┆ Ross Perot        ┆ Independent ┆ 19743821     ┆ loss   ┆ 18.956298 │
# └──────┴───────────────────┴─────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.iloc[138:144]
# ```
#
# ```text
#      Year          Candidate        Party  Popular vote Result          %
# 138  1988           Ron Paul  Libertarian        431750   loss   0.472660
# 139  1992       Andre Marrou  Libertarian        290087   loss   0.278516
# 140  1992       Bill Clinton   Democratic      44909806    win  43.118485
# 141  1992           Bo Gritz     Populist        106152   loss   0.101918
# 142  1992  George H. W. Bush   Republican      39104550   loss  37.544784
# 143  1992         Ross Perot  Independent      19743821   loss  18.956298
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="306e1d17"
# A whole row on its own comes back from `.row()`, as a tuple of values in column order.

# %% tags=["remove-input", "remove-output"] id="b095a571"
elections.row(0)


# %% [markdown] id="9a3954e3"
# <!-- tab-twins:begin elections.row(0) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections.row(0)
# ```
#
# ```text
# (1824, 'Andrew Jackson', 'Democratic-Republican', 151271, 'loss', 57.21012204)
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.iloc[0]
# ```
#
# ```text
# Year                             1824
# Candidate              Andrew Jackson
# Party           Democratic-Republican
# Popular vote                   151271
# Result                           loss
# %                           57.210122
# Name: 0, dtype: object
# ```
# ::::
# :::::
# <!-- tab-twins:end -->
# %% [markdown] id="b0f9d831"
# Passing `named=True` gives a dictionary instead, which is much easier to read when a table is wide.

# %% tags=["remove-input", "remove-output"] id="a37363f8"
elections.row(0, named=True)


# %% [markdown] id="efdbe2d8"
# <!-- tab-twins:begin elections.row(0, named=True) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections.row(0, named=True)
# ```
#
# ```text
# {'Year': 1824,
#  'Candidate': 'Andrew Jackson',
#  'Party': 'Democratic-Republican',
#  'Popular vote': 151271,
#  'Result': 'loss',
#  '%': 57.21012204}
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.iloc[0].to_dict()
# ```
#
# ```text
# {'Year': 1824,
#  'Candidate': 'Andrew Jackson',
#  'Party': 'Democratic-Republican',
#  'Popular vote': 151271,
#  'Result': 'loss',
#  '%': 57.21012204}
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="71f7fa2a"
# A row's position is the only handle we have on it, and that position belongs to the table rather than to the row. Any operation that reorders the table therefore hands out new positions, which is a point we return to at the end of the section.
#
# ### Extraction with `filter` and `select`
#
# `[]` asks for positions and labels, which makes it concise for the quick looks at a table we take constantly. Anything *computed*, though (a condition, an arithmetic result) goes through a second pair of methods.
#
# `filter` chooses rows and `select` chooses columns. Both take **expressions**, which are built with `pl.col` and can compare and combine columns before anything is returned. This is the pairing you'll reach for most often, because a condition like "more than 60 million popular votes" describes the rows you want without needing to know where they sit.
#
# Two rules cover most of the confusion: `filter` narrows the rows and leaves every column in place, and `select` decides which columns come back.

# %% tags=["remove-input", "remove-output"] id="13b248a7"
# select takes a list of column names and returns a DataFrame
elections.select(["Year", "Candidate", "Result"])


# %% [markdown] id="252a988a"
# <!-- tab-twins:begin elections.select(["Year", "Candidate", "Result"]) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # select takes a list of column names and returns a DataFrame
# elections.select(["Year", "Candidate", "Result"])
# ```
#
# ```text
# shape: (182, 3)
# ┌──────┬───────────────────┬────────┐
# │ Year ┆ Candidate         ┆ Result │
# │ ---  ┆ ---               ┆ ---    │
# │ i64  ┆ str               ┆ str    │
# ╞══════╪═══════════════════╪════════╡
# │ 1824 ┆ Andrew Jackson    ┆ loss   │
# │ 1824 ┆ John Quincy Adams ┆ win    │
# │ 1828 ┆ Andrew Jackson    ┆ win    │
# │ 1828 ┆ John Quincy Adams ┆ loss   │
# │ 1832 ┆ Andrew Jackson    ┆ win    │
# │ …    ┆ …                 ┆ …      │
# │ 2016 ┆ Jill Stein        ┆ loss   │
# │ 2020 ┆ Joseph Biden      ┆ win    │
# │ 2020 ┆ Donald Trump      ┆ loss   │
# │ 2020 ┆ Jo Jorgensen      ┆ loss   │
# │ 2020 ┆ Howard Hawkins    ┆ loss   │
# └──────┴───────────────────┴────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd[["Year", "Candidate", "Result"]]
# ```
#
# ```text
#      Year          Candidate Result
# 0    1824     Andrew Jackson   loss
# 1    1824  John Quincy Adams    win
# 2    1828     Andrew Jackson    win
# 3    1828  John Quincy Adams   loss
# 4    1832     Andrew Jackson    win
# ..    ...                ...    ...
# 177  2016         Jill Stein   loss
# 178  2020       Joseph Biden    win
# 179  2020       Donald Trump   loss
# 180  2020       Jo Jorgensen   loss
# 181  2020     Howard Hawkins   loss
#
# [182 rows x 3 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->
# %% [markdown] id="3cb17307"
# `select` also accepts a computed expression. `pl.col("Popular vote")` refers to that column, arithmetic on it applies to every value, and `.alias` names the result.

# %% tags=["remove-input", "remove-output"] id="4f29d006"
elections.select((pl.col("Popular vote") / 1_000_000).alias("Popular vote (millions)"))


# %% [markdown] id="825bbdcd"
# <!-- tab-twins:begin elections.select((pl.col("Popular vote") / 1_000_000) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections.select((pl.col("Popular vote") / 1_000_000).alias("Popular vote (millions)"))
# ```
#
# ```text
# shape: (182, 1)
# ┌─────────────────────────┐
# │ Popular vote (millions) │
# │ ---                     │
# │ f64                     │
# ╞═════════════════════════╡
# │ 0.151271                │
# │ 0.113142                │
# │ 0.642806                │
# │ 0.500897                │
# │ 0.702735                │
# │ …                       │
# │ 1.457226                │
# │ 81.268924               │
# │ 74.216154               │
# │ 1.865724                │
# │ 0.405035                │
# └─────────────────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd[["Popular vote"]].div(1_000_000).rename(
#     columns={"Popular vote": "Popular vote (millions)"}
# )
# ```
#
# ```text
#      Popular vote (millions)
# 0                   0.151271
# 1                   0.113142
# 2                   0.642806
# 3                   0.500897
# 4                   0.702735
# ..                       ...
# 177                 1.457226
# 178                81.268924
# 179                74.216154
# 180                 1.865724
# 181                 0.405035
#
# [182 rows x 1 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->
# %% [markdown] id="1b6cc8e7"
# `filter` takes a condition and returns the rows that satisfy it. Eight candidacies in the dataset drew more than 60 million popular votes, the earliest of them in 2004.

# %% tags=["remove-input", "remove-output"] id="d60a1e4a"
elections.filter(pl.col("Popular vote") > 60000000)


# %% [markdown] id="ebafccc8"
# <!-- tab-twins:begin elections.filter(pl.col("Popular vote") > 60000000) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections.filter(pl.col("Popular vote") > 60000000)
# ```
#
# ```text
# shape: (8, 6)
# ┌──────┬─────────────────┬────────────┬──────────────┬────────┬───────────┐
# │ Year ┆ Candidate       ┆ Party      ┆ Popular vote ┆ Result ┆ %         │
# │ ---  ┆ ---             ┆ ---        ┆ ---          ┆ ---    ┆ ---       │
# │ i64  ┆ str             ┆ str        ┆ i64          ┆ str    ┆ f64       │
# ╞══════╪═════════════════╪════════════╪══════════════╪════════╪═══════════╡
# │ 2004 ┆ George W. Bush  ┆ Republican ┆ 62040610     ┆ win    ┆ 50.771824 │
# │ 2008 ┆ Barack Obama    ┆ Democratic ┆ 69498516     ┆ win    ┆ 53.02351  │
# │ 2012 ┆ Barack Obama    ┆ Democratic ┆ 65915795     ┆ win    ┆ 51.258484 │
# │ 2012 ┆ Mitt Romney     ┆ Republican ┆ 60933504     ┆ loss   ┆ 47.384076 │
# │ 2016 ┆ Donald Trump    ┆ Republican ┆ 62984828     ┆ win    ┆ 46.407862 │
# │ 2016 ┆ Hillary Clinton ┆ Democratic ┆ 65853514     ┆ loss   ┆ 48.521539 │
# │ 2020 ┆ Joseph Biden    ┆ Democratic ┆ 81268924     ┆ win    ┆ 51.311515 │
# │ 2020 ┆ Donald Trump    ┆ Republican ┆ 74216154     ┆ loss   ┆ 46.858542 │
# └──────┴─────────────────┴────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd[elections_pd["Popular vote"] > 60000000]
# ```
#
# ```text
#      Year        Candidate       Party  Popular vote Result          %
# 157  2004   George W. Bush  Republican      62040610    win  50.771824
# 162  2008     Barack Obama  Democratic      69498516    win  53.023510
# 168  2012     Barack Obama  Democratic      65915795    win  51.258484
# 171  2012      Mitt Romney  Republican      60933504   loss  47.384076
# 173  2016     Donald Trump  Republican      62984828    win  46.407862
# 176  2016  Hillary Clinton  Democratic      65853514   loss  48.521539
# 178  2020     Joseph Biden  Democratic      81268924    win  51.311515
# 179  2020     Donald Trump  Republican      74216154   loss  46.858542
# ```
# ::::
# :::::
# <!-- tab-twins:end -->
# %% [markdown] id="e3bde64d"
# Each of these methods returns a `DataFrame`, so the two can be chained: filter the rows first, then pick the columns to keep.

# %% tags=["remove-input", "remove-output"] id="122c5a2f"
elections.filter(pl.col("Year") == 2008).select(["Year", "Candidate"])


# %% [markdown] id="aa6ebbef"
# <!-- tab-twins:begin elections.filter(pl.col("Year") == 2008).select(["Year", "Candidate"]) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections.filter(pl.col("Year") == 2008).select(["Year", "Candidate"])
# ```
#
# ```text
# shape: (6, 2)
# ┌──────┬──────────────────┐
# │ Year ┆ Candidate        │
# │ ---  ┆ ---              │
# │ i64  ┆ str              │
# ╞══════╪══════════════════╡
# │ 2008 ┆ Barack Obama     │
# │ 2008 ┆ Bob Barr         │
# │ 2008 ┆ Chuck Baldwin    │
# │ 2008 ┆ Cynthia McKinney │
# │ 2008 ┆ John McCain      │
# │ 2008 ┆ Ralph Nader      │
# └──────┴──────────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.loc[elections_pd["Year"] == 2008, ["Year", "Candidate"]]
# ```
#
# ```text
#      Year         Candidate
# 162  2008      Barack Obama
# 163  2008          Bob Barr
# 164  2008     Chuck Baldwin
# 165  2008  Cynthia McKinney
# 166  2008       John McCain
# 167  2008       Ralph Nader
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="018e08ef"
# ### Boolean Operators
#
# To filter on more than one condition at a time, we combine boolean masks using **bitwise operators**. In the table below, p and q are boolean expressions.
#
# Symbol | Usage      | Meaning
# ------ | ---------- | -------------------------------------
# ~    | ~p       | Returns negation of p
# &#124; | p &#124; q | p OR q
# &    | p & q    | p AND q
# ^  | p ^ q | p XOR q (exclusive or)
#
# **Always** wrap each individual condition in a set of parentheses `()` when combining them. Python binds `&` and `|` more tightly than the comparison operators, so `pl.col("Year") == 2008 | pl.col("%") >= 60` is read as `pl.col("Year") == (2008 | pl.col("%")) >= 60` and raises a `TypeError` instead of filtering anything.
#
# For example, to return every candidacy from 2008 *or* with at least 60% of the popular vote, we can write:

# %% tags=["remove-input", "remove-output"] id="e499765b"
# Grab rows from 2008 OR candidates winning over 60% of the vote (or both)
elections.filter((pl.col("Year") == 2008) | (pl.col("%") >= 60))


# %% [markdown] id="9b73bf67"
# <!-- tab-twins:begin elections.filter((pl.col("Year") == 2008) | (pl.col("%") >= 60)) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Grab rows from 2008 OR candidates winning over 60% of the vote (or both)
# elections.filter((pl.col("Year") == 2008) | (pl.col("%") >= 60))
# ```
#
# ```text
# shape: (10, 6)
# ┌──────┬────────────────────┬──────────────┬──────────────┬────────┬───────────┐
# │ Year ┆ Candidate          ┆ Party        ┆ Popular vote ┆ Result ┆ %         │
# │ ---  ┆ ---                ┆ ---          ┆ ---          ┆ ---    ┆ ---       │
# │ i64  ┆ str                ┆ str          ┆ i64          ┆ str    ┆ f64       │
# ╞══════╪════════════════════╪══════════════╪══════════════╪════════╪═══════════╡
# │ 1920 ┆ Warren Harding     ┆ Republican   ┆ 16144093     ┆ win    ┆ 60.574501 │
# │ 1936 ┆ Franklin Roosevelt ┆ Democratic   ┆ 27752648     ┆ win    ┆ 60.978107 │
# │ 1964 ┆ Lyndon Johnson     ┆ Democratic   ┆ 43127041     ┆ win    ┆ 61.344703 │
# │ 1972 ┆ Richard Nixon      ┆ Republican   ┆ 47168710     ┆ win    ┆ 60.907806 │
# │ 2008 ┆ Barack Obama       ┆ Democratic   ┆ 69498516     ┆ win    ┆ 53.02351  │
# │ 2008 ┆ Bob Barr           ┆ Libertarian  ┆ 523715       ┆ loss   ┆ 0.399565  │
# │ 2008 ┆ Chuck Baldwin      ┆ Constitution ┆ 199750       ┆ loss   ┆ 0.152398  │
# │ 2008 ┆ Cynthia McKinney   ┆ Green        ┆ 161797       ┆ loss   ┆ 0.123442  │
# │ 2008 ┆ John McCain        ┆ Republican   ┆ 59948323     ┆ loss   ┆ 45.737243 │
# │ 2008 ┆ Ralph Nader        ┆ Independent  ┆ 739034       ┆ loss   ┆ 0.563842  │
# └──────┴────────────────────┴──────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd[(elections_pd["Year"] == 2008) | (elections_pd["%"] >= 60)]
# ```
#
# ```text
#      Year           Candidate         Party  Popular vote Result          %
# 79   1920      Warren Harding    Republican      16144093    win  60.574501
# 91   1936  Franklin Roosevelt    Democratic      27752648    win  60.978107
# 114  1964      Lyndon Johnson    Democratic      43127041    win  61.344703
# 120  1972       Richard Nixon    Republican      47168710    win  60.907806
# 162  2008        Barack Obama    Democratic      69498516    win  53.023510
# 163  2008            Bob Barr   Libertarian        523715   loss   0.399565
# 164  2008       Chuck Baldwin  Constitution        199750   loss   0.152398
# 165  2008    Cynthia McKinney         Green        161797   loss   0.123442
# 166  2008         John McCain    Republican      59948323   loss  45.737243
# 167  2008         Ralph Nader   Independent        739034   loss   0.563842
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="74e6fd9b"
# Ten rows satisfy that condition: the six candidates who stood in 2008, plus the four landslide winners of 1920, 1936, 1964, and 1972.
#
# If we want the rows where *both* conditions hold, we use `&`.

# %% tags=["remove-input", "remove-output"] id="0c3db1b1"
# Grab post-2000 winners: rows where the year is after 2000 AND the result is a win
elections.filter((pl.col("Year") > 2000) & (pl.col("Result") == "win"))


# %% [markdown] id="73581125"
# <!-- tab-twins:begin elections.filter((pl.col("Year") > 2000) & (pl.col("Result") == "win")) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Grab post-2000 winners: rows where the year is after 2000 AND the result is a win
# elections.filter((pl.col("Year") > 2000) & (pl.col("Result") == "win"))
# ```
#
# ```text
# shape: (5, 6)
# ┌──────┬────────────────┬────────────┬──────────────┬────────┬───────────┐
# │ Year ┆ Candidate      ┆ Party      ┆ Popular vote ┆ Result ┆ %         │
# │ ---  ┆ ---            ┆ ---        ┆ ---          ┆ ---    ┆ ---       │
# │ i64  ┆ str            ┆ str        ┆ i64          ┆ str    ┆ f64       │
# ╞══════╪════════════════╪════════════╪══════════════╪════════╪═══════════╡
# │ 2004 ┆ George W. Bush ┆ Republican ┆ 62040610     ┆ win    ┆ 50.771824 │
# │ 2008 ┆ Barack Obama   ┆ Democratic ┆ 69498516     ┆ win    ┆ 53.02351  │
# │ 2012 ┆ Barack Obama   ┆ Democratic ┆ 65915795     ┆ win    ┆ 51.258484 │
# │ 2016 ┆ Donald Trump   ┆ Republican ┆ 62984828     ┆ win    ┆ 46.407862 │
# │ 2020 ┆ Joseph Biden   ┆ Democratic ┆ 81268924     ┆ win    ┆ 51.311515 │
# └──────┴────────────────┴────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd[(elections_pd["Year"] > 2000) & (elections_pd["Result"] == "win")]
# ```
#
# ```text
#      Year       Candidate       Party  Popular vote Result          %
# 157  2004  George W. Bush  Republican      62040610    win  50.771824
# 162  2008    Barack Obama  Democratic      69498516    win  53.023510
# 168  2012    Barack Obama  Democratic      65915795    win  51.258484
# 173  2016    Donald Trump  Republican      62984828    win  46.407862
# 178  2020    Joseph Biden  Democratic      81268924    win  51.311515
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="7ff49750"
# Note that we need the bitwise operators here, not Python's `and` and `or`. Those two ask a single
# yes-or-no question about the whole object, and an expression stands for a column of many values,
# so there is no one answer to give:

# %% tags=["remove-input", "remove-output"] id="ccf796ec"
# This line of code will raise a TypeError
elections.filter((pl.col("Year") == 2008) and (pl.col("%") >= 60))


# %% [markdown] id="6a7d0a41"
# <!-- tab-twins:begin elections.filter((pl.col("Year") == 2008) and (pl.col("%") >= 60)) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # This line of code will raise a TypeError
# elections.filter((pl.col("Year") == 2008) and (pl.col("%") >= 60))
# ```
#
# ```text
# TypeError: the truth value of an Expr is ambiguous
#
# You probably got here by using a Python standard library function instead of the native expressions API.
# Here are some things you might want to try:
# - instead of `pl.col('a') and pl.col('b')`, use `pl.col('a') & pl.col('b')`
# - instead of `pl.col('a') in [y, z]`, use `pl.col('a').is_in([y, z])`
# - instead of `max(pl.col('a'), pl.col('b'))`, use `pl.max_horizontal(pl.col('a'), pl.col('b'))`
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # This line of code will raise a ValueError
# elections_pd[(elections_pd["Year"] == 2008) and (elections_pd["%"] >= 60)]
# ```
#
# ```text
# ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="417030ce"
# Conditions can be strung together as far as we need. Wrapping the whole call in parentheses lets us break a long one across several lines, which is worth doing well before it becomes hard to read.

# %% tags=["remove-input", "remove-output"] id="469d1df5"
# To make code more readable, use multiple lines
elections.filter(
    (pl.col("Year") < 2000) &
    (pl.col("Year") > 1941) &
    (pl.col("Result") == "win") &
    (pl.col("%") >= 55)
)


# %% [markdown] id="daa99ead"
# <!-- tab-twins:begin (pl.col("Year") < 2000) & -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # To make code more readable, use multiple lines
# elections.filter(
#     (pl.col("Year") < 2000) &
#     (pl.col("Year") > 1941) &
#     (pl.col("Result") == "win") &
#     (pl.col("%") >= 55)
# )
# ```
#
# ```text
# shape: (5, 6)
# ┌──────┬───────────────────┬────────────┬──────────────┬────────┬───────────┐
# │ Year ┆ Candidate         ┆ Party      ┆ Popular vote ┆ Result ┆ %         │
# │ ---  ┆ ---               ┆ ---        ┆ ---          ┆ ---    ┆ ---       │
# │ i64  ┆ str               ┆ str        ┆ i64          ┆ str    ┆ f64       │
# ╞══════╪═══════════════════╪════════════╪══════════════╪════════╪═══════════╡
# │ 1952 ┆ Dwight Eisenhower ┆ Republican ┆ 34075529     ┆ win    ┆ 55.325173 │
# │ 1956 ┆ Dwight Eisenhower ┆ Republican ┆ 35579180     ┆ win    ┆ 57.650654 │
# │ 1964 ┆ Lyndon Johnson    ┆ Democratic ┆ 43127041     ┆ win    ┆ 61.344703 │
# │ 1972 ┆ Richard Nixon     ┆ Republican ┆ 47168710     ┆ win    ┆ 60.907806 │
# │ 1984 ┆ Ronald Reagan     ┆ Republican ┆ 54455472     ┆ win    ┆ 59.023326 │
# └──────┴───────────────────┴────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd[
#     (elections_pd["Year"] < 2000)
#     & (elections_pd["Year"] > 1941)
#     & (elections_pd["Result"] == "win")
#     & (elections_pd["%"] >= 55)
# ]
# ```
#
# ```text
#      Year          Candidate       Party  Popular vote Result          %
# 106  1952  Dwight Eisenhower  Republican      34075529    win  55.325173
# 109  1956  Dwight Eisenhower  Republican      35579180    win  57.650654
# 114  1964     Lyndon Johnson  Democratic      43127041    win  61.344703
# 120  1972      Richard Nixon  Republican      47168710    win  60.907806
# 133  1984      Ronald Reagan  Republican      54455472    win  59.023326
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="6aa29c21"
# ### Working with Row Positions
#
# A row is identified by its position in the table, counting from 0. Those positions are not stored anywhere; `with_row_index` writes them into a column of their own when we want to keep them.
#
# This matters as soon as we reorder a table. Below, we record each row's position and *then* sort by vote share, so the new first column says where each row started out. Lyndon Johnson's 1964 landslide is the largest share in the dataset, and it came from position 114.

# %% tags=["remove-input", "remove-output"] id="eea135a2"
# with_row_index adds a column holding each row's current position
elections.with_row_index("original_position").sort("%", descending=True).head()


# %% [markdown] id="3ebc58dd"
# <!-- tab-twins:begin elections.with_row_index("original_position").sort("%", descending=True).head() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # with_row_index adds a column holding each row's current position
# elections.with_row_index("original_position").sort("%", descending=True).head()
# ```
#
# ```text
# shape: (5, 7)
# ┌───────────────────┬──────┬────────────────────┬────────────┬──────────────┬────────┬───────────┐
# │ original_position ┆ Year ┆ Candidate          ┆ Party      ┆ Popular vote ┆ Result ┆ %         │
# │ ---               ┆ ---  ┆ ---                ┆ ---        ┆ ---          ┆ ---    ┆ ---       │
# │ u32               ┆ i64  ┆ str                ┆ str        ┆ i64          ┆ str    ┆ f64       │
# ╞═══════════════════╪══════╪════════════════════╪════════════╪══════════════╪════════╪═══════════╡
# │ 114               ┆ 1964 ┆ Lyndon Johnson     ┆ Democratic ┆ 43127041     ┆ win    ┆ 61.344703 │
# │ 91                ┆ 1936 ┆ Franklin Roosevelt ┆ Democratic ┆ 27752648     ┆ win    ┆ 60.978107 │
# │ 120               ┆ 1972 ┆ Richard Nixon      ┆ Republican ┆ 47168710     ┆ win    ┆ 60.907806 │
# │ 79                ┆ 1920 ┆ Warren Harding     ┆ Republican ┆ 16144093     ┆ win    ┆ 60.574501 │
# │ 133               ┆ 1984 ┆ Ronald Reagan      ┆ Republican ┆ 54455472     ┆ win    ┆ 59.023326 │
# └───────────────────┴──────┴────────────────────┴────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.reset_index(names="original_position").sort_values(
#     "%", ascending=False
# ).head()
# ```
#
# ```text
#      original_position  Year  ... Result          %
# 114                114  1964  ...    win  61.344703
# 91                  91  1936  ...    win  60.978107
# 120                120  1972  ...    win  60.907806
# 79                  79  1920  ...    win  60.574501
# 133                133  1984  ...    win  59.023326
#
# [5 rows x 7 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="2d2b5b2b"
# `with_row_index` returns a new table rather than changing the one we called it on, so `elections` itself still has its original six columns and its original order.

# %% tags=["remove-input", "remove-output"] id="2a58cf86"
elections.head(3)


# %% [markdown] id="11f86309"
# <!-- tab-twins:begin elections.head(3) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections.head(3)
# ```
#
# ```text
# shape: (3, 6)
# ┌──────┬───────────────────┬───────────────────────┬──────────────┬────────┬───────────┐
# │ Year ┆ Candidate         ┆ Party                 ┆ Popular vote ┆ Result ┆ %         │
# │ ---  ┆ ---               ┆ ---                   ┆ ---          ┆ ---    ┆ ---       │
# │ i64  ┆ str               ┆ str                   ┆ i64          ┆ str    ┆ f64       │
# ╞══════╪═══════════════════╪═══════════════════════╪══════════════╪════════╪═══════════╡
# │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republican ┆ 151271       ┆ loss   ┆ 57.210122 │
# │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican ┆ 113142       ┆ win    ┆ 42.789878 │
# │ 1828 ┆ Andrew Jackson    ┆ Democratic            ┆ 642806       ┆ win    ┆ 56.203927 │
# └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.head(3)
# ```
#
# ```text
#    Year          Candidate  ... Result          %
# 0  1824     Andrew Jackson  ...   loss  57.210122
# 1  1824  John Quincy Adams  ...    win  42.789878
# 2  1828     Andrew Jackson  ...    win  56.203927
#
# [3 rows x 6 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="effc775a"
# Adding the index column *after* the sort numbers the rows in their new order instead, counting 0, 1, 2 down the sorted table. Which of the two you want depends on whether you care where a row came from or where it now sits.

# %% tags=["remove-input", "remove-output"] id="41b15586"
elections.sort("%", descending=True).with_row_index().head()


# %% [markdown] id="9c1b434e"
# <!-- tab-twins:begin elections.sort("%", descending=True).with_row_index().head() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# elections.sort("%", descending=True).with_row_index().head()
# ```
#
# ```text
# shape: (5, 7)
# ┌───────┬──────┬────────────────────┬────────────┬──────────────┬────────┬───────────┐
# │ index ┆ Year ┆ Candidate          ┆ Party      ┆ Popular vote ┆ Result ┆ %         │
# │ ---   ┆ ---  ┆ ---                ┆ ---        ┆ ---          ┆ ---    ┆ ---       │
# │ u32   ┆ i64  ┆ str                ┆ str        ┆ i64          ┆ str    ┆ f64       │
# ╞═══════╪══════╪════════════════════╪════════════╪══════════════╪════════╪═══════════╡
# │ 0     ┆ 1964 ┆ Lyndon Johnson     ┆ Democratic ┆ 43127041     ┆ win    ┆ 61.344703 │
# │ 1     ┆ 1936 ┆ Franklin Roosevelt ┆ Democratic ┆ 27752648     ┆ win    ┆ 60.978107 │
# │ 2     ┆ 1972 ┆ Richard Nixon      ┆ Republican ┆ 47168710     ┆ win    ┆ 60.907806 │
# │ 3     ┆ 1920 ┆ Warren Harding     ┆ Republican ┆ 16144093     ┆ win    ┆ 60.574501 │
# │ 4     ┆ 1984 ┆ Ronald Reagan      ┆ Republican ┆ 54455472     ┆ win    ┆ 59.023326 │
# └───────┴──────┴────────────────────┴────────────┴──────────────┴────────┴───────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# elections_pd.sort_values("%", ascending=False).reset_index(drop=True).reset_index().head()
# ```
#
# ```text
#    index  Year           Candidate       Party  Popular vote Result          %
# 0      0  1964      Lyndon Johnson  Democratic      43127041    win  61.344703
# 1      1  1936  Franklin Roosevelt  Democratic      27752648    win  60.978107
# 2      2  1972       Richard Nixon  Republican      47168710    win  60.907806
# 3      3  1920      Warren Harding  Republican      16144093    win  60.574501
# 4      4  1984       Ronald Reagan  Republican      54455472    win  59.023326
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="63b2e10c"
# ## The `babynames` Dataset
#
# The rest of this chapter works with a second dataset: the names given to babies born in California, as recorded by the Social Security Administration. Each row holds one name, in one year, for one sex, along with the number of babies who were given it.
#
# The cell below downloads the data and loads it into a `DataFrame`. The code is outside the scope of Data 100, but you're encouraged to dig into it if you are interested.
#
# ````{dropdown} Click to see the code
# :open: false
# ```python
# # This code pulls census data and loads it into a DataFrame
# # We won't cover it explicitly in this class, but you are welcome to explore it on your own
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


# %% [markdown] id="abc4e450"
#

# %% tags=["remove-input"] id="c8bfdae2"
# This code pulls census data and loads it into a DataFrame
# We won't cover it explicitly in this class, but you are welcome to explore it on your own
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

# %% [markdown] id="71233ceb"
# ## More Ways to Build a Filter
#
# A boolean expression can describe any condition we can write down, but a long list of alternatives gets verbose in a hurry. Suppose we want every row whose name is one of four we care about.

# %% tags=["remove-input", "remove-output"] id="5c4d156a"
# Note: The parentheses surrounding the code make it possible to
# break the code into multiple lines for readability. But this is
# still a lot of code just to check for four names...
(
    babynames.filter((pl.col("Name") == "Bella") |
                     (pl.col("Name") == "Alex") |
                     (pl.col("Name") == "Narges") |
                     (pl.col("Name") == "Lisa"))
)


# %% [markdown] id="7c067316"
# <!-- tab-twins:begin babynames.filter((pl.col("Name") == "Bella") | -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Note: The parentheses surrounding the code make it possible to
# # break the code into multiple lines for readability. But this is
# # still a lot of code just to check for four names...
# (
#     babynames.filter((pl.col("Name") == "Bella") |
#                      (pl.col("Name") == "Alex") |
#                      (pl.col("Name") == "Narges") |
#                      (pl.col("Name") == "Lisa"))
# )
# ```
#
# ```text
# shape: (317, 5)
# ┌───────┬─────┬──────┬───────┬───────┐
# │ State ┆ Sex ┆ Year ┆ Name  ┆ Count │
# │ ---   ┆ --- ┆ ---  ┆ ---   ┆ ---   │
# │ str   ┆ str ┆ i64  ┆ str   ┆ i64   │
# ╞═══════╪═════╪══════╪═══════╪═══════╡
# │ CA    ┆ F   ┆ 1923 ┆ Bella ┆ 5     │
# │ CA    ┆ F   ┆ 1925 ┆ Bella ┆ 8     │
# │ CA    ┆ F   ┆ 1932 ┆ Lisa  ┆ 5     │
# │ CA    ┆ F   ┆ 1936 ┆ Lisa  ┆ 8     │
# │ CA    ┆ F   ┆ 1939 ┆ Lisa  ┆ 5     │
# │ …     ┆ …   ┆ …    ┆ …     ┆ …     │
# │ CA    ┆ M   ┆ 2018 ┆ Alex  ┆ 495   │
# │ CA    ┆ M   ┆ 2019 ┆ Alex  ┆ 438   │
# │ CA    ┆ M   ┆ 2020 ┆ Alex  ┆ 379   │
# │ CA    ┆ M   ┆ 2021 ┆ Alex  ┆ 333   │
# │ CA    ┆ M   ┆ 2022 ┆ Alex  ┆ 344   │
# └───────┴─────┴──────┴───────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd[
#     (babynames_pd["Name"] == "Bella")
#     | (babynames_pd["Name"] == "Alex")
#     | (babynames_pd["Name"] == "Narges")
#     | (babynames_pd["Name"] == "Lisa")
# ]
# ```
#
# ```text
#        State Sex  Year   Name  Count
# 6289      CA   F  1923  Bella      5
# 7512      CA   F  1925  Bella      8
# 12368     CA   F  1932   Lisa      5
# 14741     CA   F  1936   Lisa      8
# 17084     CA   F  1939   Lisa      5
# ...      ...  ..   ...    ...    ...
# 393248    CA   M  2018   Alex    495
# 396111    CA   M  2019   Alex    438
# 398983    CA   M  2020   Alex    379
# 401788    CA   M  2021   Alex    333
# 404663    CA   M  2022   Alex    344
#
# [317 rows x 5 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="7529b7bd"
# Fortunately, Polars offers more concise ways of saying the same thing.
#
# The `.is_in()` method checks each value of a column against a sequence of values (a list, an array, or another `Series`). It returns the same 317 rows as the four-way condition above, in one line.

# %% tags=["remove-input", "remove-output"] id="316de856"
names = ["Bella", "Alex", "Narges", "Lisa"]
babynames.filter(pl.col("Name").is_in(names))


# %% [markdown] id="4f8a4c1d"
# <!-- tab-twins:begin babynames.filter(pl.col("Name").is_in(names)) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# names = ["Bella", "Alex", "Narges", "Lisa"]
# babynames.filter(pl.col("Name").is_in(names))
# ```
#
# ```text
# shape: (317, 5)
# ┌───────┬─────┬──────┬───────┬───────┐
# │ State ┆ Sex ┆ Year ┆ Name  ┆ Count │
# │ ---   ┆ --- ┆ ---  ┆ ---   ┆ ---   │
# │ str   ┆ str ┆ i64  ┆ str   ┆ i64   │
# ╞═══════╪═════╪══════╪═══════╪═══════╡
# │ CA    ┆ F   ┆ 1923 ┆ Bella ┆ 5     │
# │ CA    ┆ F   ┆ 1925 ┆ Bella ┆ 8     │
# │ CA    ┆ F   ┆ 1932 ┆ Lisa  ┆ 5     │
# │ CA    ┆ F   ┆ 1936 ┆ Lisa  ┆ 8     │
# │ CA    ┆ F   ┆ 1939 ┆ Lisa  ┆ 5     │
# │ …     ┆ …   ┆ …    ┆ …     ┆ …     │
# │ CA    ┆ M   ┆ 2018 ┆ Alex  ┆ 495   │
# │ CA    ┆ M   ┆ 2019 ┆ Alex  ┆ 438   │
# │ CA    ┆ M   ┆ 2020 ┆ Alex  ┆ 379   │
# │ CA    ┆ M   ┆ 2021 ┆ Alex  ┆ 333   │
# │ CA    ┆ M   ┆ 2022 ┆ Alex  ┆ 344   │
# └───────┴─────┴──────┴───────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# names_pd = ["Bella", "Alex", "Narges", "Lisa"]
# babynames_pd[babynames_pd["Name"].isin(names_pd)]
# ```
#
# ```text
#        State Sex  Year   Name  Count
# 6289      CA   F  1923  Bella      5
# 7512      CA   F  1925  Bella      8
# 12368     CA   F  1932   Lisa      5
# 14741     CA   F  1936   Lisa      8
# 17084     CA   F  1939   Lisa      5
# ...      ...  ..   ...    ...    ...
# 393248    CA   M  2018   Alex    495
# 396111    CA   M  2019   Alex    438
# 398983    CA   M  2020   Alex    379
# 401788    CA   M  2021   Alex    333
# 404663    CA   M  2022   Alex    344
#
# [317 rows x 5 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="f9d318d8"
# String columns carry a whole family of methods under `.str`. `.str.starts_with()` checks the beginning of each string, so the filter below keeps every row whose name begins with the letter `N`.

# %% tags=["remove-input", "remove-output"] id="203de3da"
# Extracting names that begin with the letter "N"
babynames.filter(pl.col("Name").str.starts_with("N"))


# %% [markdown] id="5abad0f9"
# <!-- tab-twins:begin babynames.filter(pl.col("Name").str.starts_with("N")) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Extracting names that begin with the letter "N"
# babynames.filter(pl.col("Name").str.starts_with("N"))
# ```
#
# ```text
# shape: (12_229, 5)
# ┌───────┬─────┬──────┬────────┬───────┐
# │ State ┆ Sex ┆ Year ┆ Name   ┆ Count │
# │ ---   ┆ --- ┆ ---  ┆ ---    ┆ ---   │
# │ str   ┆ str ┆ i64  ┆ str    ┆ i64   │
# ╞═══════╪═════╪══════╪════════╪═══════╡
# │ CA    ┆ F   ┆ 1910 ┆ Norma  ┆ 23    │
# │ CA    ┆ F   ┆ 1910 ┆ Nellie ┆ 20    │
# │ CA    ┆ F   ┆ 1910 ┆ Nina   ┆ 11    │
# │ CA    ┆ F   ┆ 1910 ┆ Nora   ┆ 6     │
# │ CA    ┆ F   ┆ 1911 ┆ Nellie ┆ 23    │
# │ …     ┆ …   ┆ …    ┆ …      ┆ …     │
# │ CA    ┆ M   ┆ 2022 ┆ Nilan  ┆ 5     │
# │ CA    ┆ M   ┆ 2022 ┆ Niles  ┆ 5     │
# │ CA    ┆ M   ┆ 2022 ┆ Nolen  ┆ 5     │
# │ CA    ┆ M   ┆ 2022 ┆ Noriel ┆ 5     │
# │ CA    ┆ M   ┆ 2022 ┆ Norris ┆ 5     │
# └───────┴─────┴──────┴────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd[babynames_pd["Name"].str.startswith("N")]
# ```
#
# ```text
#        State Sex  Year    Name  Count
# 76        CA   F  1910   Norma     23
# 83        CA   F  1910  Nellie     20
# 127       CA   F  1910    Nina     11
# 198       CA   F  1910    Nora      6
# 310       CA   F  1911  Nellie     23
# ...      ...  ..   ...     ...    ...
# 407319    CA   M  2022   Nilan      5
# 407320    CA   M  2022   Niles      5
# 407321    CA   M  2022   Nolen      5
# 407322    CA   M  2022  Noriel      5
# 407323    CA   M  2022  Norris      5
#
# [12229 rows x 5 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="c3dbab66"
# ## Useful Utility Functions
#
# Polars contains an extensive library of functions that can help shorten the process of setting and getting information from its data structures. In the following section, we will give overviews of each of the main utility functions that will help us in Data 100.
#
# Discussing all of the functionality offered by Polars could take an entire semester! We will walk you through the most commonly used functions and encourage you to explore and experiment on your own.
#
# - Aggregation methods
# - `.shape`, `.height`, and `.width`
# - `.describe()`
# - `.sample()`
# - `.value_counts()`
# - `.unique()`
#
# The Polars [documentation](https://docs.pola.rs/api/python/stable/reference/index.html) will be a valuable resource in Data 100 and beyond.
#
# ### Aggregation Methods
#
# The array functions you encountered in [Data 8](https://www.data8.org/su23/reference/#array-functions-and-methods) live here as methods you call on a `Series` itself. Below, we pull out the number of babies named Yash in each year the name was recorded.

# %% tags=["remove-input", "remove-output"] id="7b5d42be"
# Pull out the number of babies named Yash each year
yash_counts = babynames.filter(pl.col("Name") == "Yash")["Count"]
yash_counts


# %% [markdown] id="9c418693"
# <!-- tab-twins:begin yash_counts = babynames.filter(pl.col("Name") == "Yash")["Count"] -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Pull out the number of babies named Yash each year
# yash_counts = babynames.filter(pl.col("Name") == "Yash")["Count"]
# yash_counts
# ```
#
# ```text
# shape: (28,)
# Series: 'Count' [i64]
# [
# 	8
# 	9
# 	11
# 	12
# 	10
# 	…
# 	10
# 	9
# 	15
# 	13
# 	13
# ]
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# yash_counts_pd = babynames_pd[babynames_pd["Name"] == "Yash"]["Count"]
# yash_counts_pd
# ```
#
# ```text
# 331824     8
# 334114     9
# 336390    11
# 338773    12
# 341387    10
# 343571    14
# 345767    24
# 348230    29
# 350889    24
# 353445    29
# 356221    25
# 358978    27
# 361831    29
# 364905    24
# 367867    23
# 370945    18
# 374055    14
# 376756    18
# 379660    18
# 383338     9
# 385903    12
# 388529    17
# 391485    16
# 394906    10
# 397874     9
# 400171    15
# 403092    13
# 406006    13
# Name: Count, dtype: int64
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="67230dc8"
# The name appears in 28 rows of the table, and `.mean()` averages the counts across them.

# %% id="062887e7"
# Average number of babies named Yash each year
# Keep in mind that even if Python gives you 10 decimal places of precision,
# you should think carefully about how much precision is meaningful!
# In this case, one decimal place or even no decimal places would be appropriate.
yash_counts.mean()

# %% id="7587fbc6"
# Max number of babies named Yash born in any single year
yash_counts.max()

# %% [markdown] id="ad709a3c"
# ### `.shape`, `.height`, and `.width`
#
# These attributes measure the "amount" of data stored in a `DataFrame`. Calling `.shape` returns a tuple containing the number of rows followed by the number of columns.
#
# Many functions strictly require the dimensions of their arguments to match. Asking the table for its dimensions is much faster than counting the items by hand.

# %% id="4f88d5c3"
# Return the shape of the DataFrame, in the format (num_rows, num_columns)
babynames.shape

# %% [markdown] id="5dc4627d"
# `.height` and `.width` report those same two numbers one at a time, so multiplying them gives the total number of values the table holds.

# %% tags=["remove-input", "remove-output"] id="b733b3ae"
# The total number of entries in the object, equal to num_rows * num_columns
babynames.height * babynames.width


# %% [markdown] id="07eb4fb8"
# <!-- tab-twins:begin babynames.height * babynames.width -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # The total number of entries in the object, equal to num_rows * num_columns
# babynames.height * babynames.width
# ```
#
# ```text
# 2037140
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd.size
# ```
#
# ```text
# 2037140
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="18aadad6"
# Calling `len` on a `DataFrame` gives its height, which is the number we want far more often than the other two.

# %% id="373e3071"
# Return the number of rows in the DataFrame
len(babynames)

# %% [markdown] id="06159aa3"
# ### `.describe()`
#
# If many statistics are required from a `DataFrame` (minimum value, maximum value, mean value, etc.), then `.describe()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.describe.html) can be used to compute all of them at once.

# %% tags=["remove-input", "remove-output"] id="aab9ee2a"
babynames.describe()


# %% [markdown] id="7e4b4d80"
# <!-- tab-twins:begin babynames.describe() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# babynames.describe()
# ```
#
# ```text
# shape: (9, 6)
# ┌────────────┬────────┬────────┬─────────────┬────────┬────────────┐
# │ statistic  ┆ State  ┆ Sex    ┆ Year        ┆ Name   ┆ Count      │
# │ ---        ┆ ---    ┆ ---    ┆ ---         ┆ ---    ┆ ---        │
# │ str        ┆ str    ┆ str    ┆ f64         ┆ str    ┆ f64        │
# ╞════════════╪════════╪════════╪═════════════╪════════╪════════════╡
# │ count      ┆ 407428 ┆ 407428 ┆ 407428.0    ┆ 407428 ┆ 407428.0   │
# │ null_count ┆ 0      ┆ 0      ┆ 0.0         ┆ 0      ┆ 0.0        │
# │ mean       ┆ null   ┆ null   ┆ 1985.733609 ┆ null   ┆ 79.543456  │
# │ std        ┆ null   ┆ null   ┆ 27.00766    ┆ null   ┆ 293.698654 │
# │ min        ┆ CA     ┆ F      ┆ 1910.0      ┆ Aadan  ┆ 5.0        │
# │ 25%        ┆ null   ┆ null   ┆ 1969.0      ┆ null   ┆ 7.0        │
# │ 50%        ┆ null   ┆ null   ┆ 1992.0      ┆ null   ┆ 13.0       │
# │ 75%        ┆ null   ┆ null   ┆ 2008.0      ┆ null   ┆ 38.0       │
# │ max        ┆ CA     ┆ M      ┆ 2022.0      ┆ Zyrus  ┆ 8260.0     │
# └────────────┴────────┴────────┴─────────────┴────────┴────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd.describe()
# ```
#
# ```text
#                 Year          Count
# count  407428.000000  407428.000000
# mean     1985.733609      79.543456
# std        27.007660     293.698654
# min      1910.000000       5.000000
# 25%      1969.000000       7.000000
# 50%      1992.000000      13.000000
# 75%      2008.000000      38.000000
# max      2022.000000    8260.000000
# ```
# ::::
# :::::
# <!-- tab-twins:end -->
# %% [markdown] id="9b6cfaaa"
# The statistics come back as rows, labeled by the `statistic` column on the left, with one column of results per column of the original table. Text columns are described too: they report a count, a null count, and their alphabetical minimum and maximum, and carry `null` wherever a statistic makes no sense for them.
#
# A few things stand out. No value anywhere in the table is missing, since `null_count` is 0 across the board. The years run from 1910 to 2022. And the smallest `Count` in the dataset is 5, so names rarer than that never made it into the file.
#
# A `Series` can describe itself in the same way, reporting the statistics that suit its data type.

# %% tags=["remove-input", "remove-output"] id="0e889dc6"
babynames["Sex"].describe()


# %% [markdown] id="999f2d33"
# <!-- tab-twins:begin babynames["Sex"].describe() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# babynames["Sex"].describe()
# ```
#
# ```text
# shape: (4, 2)
# ┌────────────┬────────┐
# │ statistic  ┆ value  │
# │ ---        ┆ ---    │
# │ str        ┆ str    │
# ╞════════════╪════════╡
# │ count      ┆ 407428 │
# │ null_count ┆ 0      │
# │ min        ┆ F      │
# │ max        ┆ M      │
# └────────────┴────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd["Sex"].describe()
# ```
#
# ```text
# count     407428
# unique         2
# top            F
# freq      239537
# Name: Sex, dtype: object
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="1107addb"
# ### `.sample()`
#
# As we will see later in the semester, random processes are at the heart of many data science techniques (for example, train-test splits, bootstrapping, and cross-validation). `.sample()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.sample.html) lets us quickly select random rows of a `DataFrame`.
#
# By default, `.sample()` selects rows *without* replacement. Pass in the argument `with_replacement=True` to sample with replacement.

# %% id="30e8fcf4"
# Randomly sample a row from the DataFrame
babynames.sample()

# %% [markdown] id="314acaaf"
# Naturally, this can be chained with the extraction tools from earlier in the chapter.

# %% id="ddc580a7"
# Sample 5 random rows, and keep all columns from position 2 onwards
babynames.sample(5)[:, 2:]

# %% [markdown] id="a3eabf64"
# Wrapping a chain of methods in parentheses lets us spread it across several lines. Here we narrow the table to the year 2000, sample four of those rows with replacement, and keep the last three columns.

# %% id="52177a8f"
result = (
    babynames.filter(pl.col("Year") == 2000)
    .sample(4, with_replacement=True)[:, 2:]
)
result

# %% [markdown] id="49aa8d76"
# ::: {tip}
# Rerun any of the cells above and you'll get different rows each time. Pass `seed=` to `.sample()` when you need the same rows on every run, which is most of the time once other people have to reproduce your results.
# :::
#
# ### `.value_counts()`
#
# The `Series.value_counts()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/series/api/polars.Series.value_counts.html) method counts the number of occurrences of each unique value in a `Series`. In other words, it *counts* the number of times each unique *value* appears. This is often useful for determining the most or least common entries in a `Series`.

# %% id="a5df03e2"
babynames["Sex"].value_counts()


# %% [markdown] id="4fb55ec5"
# The result is a two-column `DataFrame`: the distinct values, in a column that keeps the name of the original `Series`, and their counts, in a column named `count`. Those rows come back in no particular order, so pass `sort=True` when the ranking is what you are after.
#
# Below, we count the number of times each name appears in the `"Name"` column, which tells us the name recorded in the most sex-and-year combinations.

# %% tags=["remove-input", "remove-output"] id="e62c94e4"
babynames["Name"].value_counts(sort=True).head()


# %% [markdown] id="37462ab0"
# <!-- tab-twins:begin babynames["Name"].value_counts(sort=True).head() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# babynames["Name"].value_counts(sort=True).head()
# ```
#
# ```text
# shape: (5, 2)
# ┌───────────┬───────┐
# │ Name      ┆ count │
# │ ---       ┆ ---   │
# │ str       ┆ u32   │
# ╞═══════════╪═══════╡
# │ Jean      ┆ 223   │
# │ Francis   ┆ 221   │
# │ Guadalupe ┆ 218   │
# │ Jessie    ┆ 217   │
# │ Marion    ┆ 214   │
# └───────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd["Name"].value_counts().head()
# ```
#
# ```text
# Name
# Jean         223
# Francis      221
# Guadalupe    218
# Jessie       217
# Marion       214
# Name: count, dtype: int64
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="229f0677"
# `Jean` leads with 223 rows: 223 separate combinations of a sex and a year in which at least five California babies were given that name.
#
# ### `.unique()`
#
# If we have a `Series` with many repeated values, then `.unique()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/series/api/polars.Series.unique.html) can be used to identify only the *unique* values. Here we return every name in `babynames`.

# %% id="54331d26"
babynames["Name"].unique()


# %% [markdown] id="fd89d871"
# The 407,428 rows of the table hold 20,437 distinct names between them, a count that `.n_unique()` reports directly.

# %% tags=["remove-input", "remove-output"] id="5b2afa22"
babynames["Name"].n_unique()


# %% [markdown] id="c4c11597"
# <!-- tab-twins:begin babynames["Name"].n_unique() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# babynames["Name"].n_unique()
# ```
#
# ```text
# 20437
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd["Name"].nunique()
# ```
#
# ```text
# 20437
# ```
# ::::
# :::::
# <!-- tab-twins:end -->
# %% [markdown] id="534e88ce"
# The unique values arrive in no particular order. When the order matters, `maintain_order=True` returns them in the order they first appear in the `Series`, which here means starting from the top of the table.

# %% tags=["remove-input", "remove-output"] id="d393da06"
babynames["Name"].unique(maintain_order=True).head(5)


# %% [markdown] id="75ee87f0"
# <!-- tab-twins:begin babynames["Name"].unique(maintain_order=True).head(5) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# babynames["Name"].unique(maintain_order=True).head(5)
# ```
#
# ```text
# shape: (5,)
# Series: 'Name' [str]
# [
# 	"Mary"
# 	"Helen"
# 	"Dorothy"
# 	"Margaret"
# 	"Frances"
# ]
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd["Name"].unique()[:5]
# ```
#
# ```text
# array(['Mary', 'Helen', 'Dorothy', 'Margaret', 'Frances'], dtype=object)
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="4280df73"
# ## Adding, Removing, and Modifying Columns
#
# In many data science tasks, we may need to change the columns contained in our `DataFrame` in some way. Fortunately, the syntax to do so is fairly straightforward.
#
# To add a new column, hand `.with_columns()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.with_columns.html) a `Series` or an expression under the name we want it to have. Writing that name as a keyword argument, as below, is the most direct way to say it.

# %% tags=["remove-input", "remove-output"] id="034644cb"
# Create a Series of the length of each name
babyname_lengths = babynames["Name"].str.len_chars()

# Add a column named "name_lengths" that includes the length of each name
babynames = babynames.with_columns(name_lengths=babyname_lengths)
babynames.head()

# %% [markdown] id="3bd987a7"
# <!-- tab-twins:begin babynames = babynames.with_columns(name_lengths=babyname_lengths) babynames.head() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Create a Series of the length of each name
# babyname_lengths = babynames["Name"].str.len_chars()
#
# # Add a column named "name_lengths" that includes the length of each name
# babynames = babynames.with_columns(name_lengths=babyname_lengths)
# babynames.head()
# ```
#
# ```text
# shape: (5, 6)
# ┌───────┬─────┬──────┬──────────┬───────┬──────────────┐
# │ State ┆ Sex ┆ Year ┆ Name     ┆ Count ┆ name_lengths │
# │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   ┆ ---          │
# │ str   ┆ str ┆ i64  ┆ str      ┆ i64   ┆ u32          │
# ╞═══════╪═════╪══════╪══════════╪═══════╪══════════════╡
# │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   ┆ 4            │
# │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   ┆ 5            │
# │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   ┆ 7            │
# │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   ┆ 8            │
# │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   ┆ 7            │
# └───────┴─────┴──────┴──────────┴───────┴──────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # Create a Series of the length of each name
# babyname_lengths_pd = babynames_pd["Name"].str.len()
#
# # Add a column named "name_lengths" that includes the length of each name
# babynames_pd["name_lengths"] = babyname_lengths_pd
# babynames_pd.head()
# ```
#
# ```text
#   State Sex  Year      Name  Count  name_lengths
# 0    CA   F  1910      Mary    295             4
# 1    CA   F  1910     Helen    239             5
# 2    CA   F  1910   Dorothy    220             7
# 3    CA   F  1910  Margaret    163             8
# 4    CA   F  1910   Frances    134             7
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="5221b1d0"
#

# %% [markdown] id="7cd9b0b5"
# If we need to later modify an existing column, we pass the new values to `.with_columns()` under that column's existing name. Inside the expression, `pl.col("name_lengths")` refers to the column as it stands right now.

# %% tags=["remove-input", "remove-output"] id="0bab8732"
# Modify the "name_lengths" column to be one less than its original value
babynames = babynames.with_columns(name_lengths=pl.col("name_lengths") - 1)
babynames.head()


# %% [markdown] id="be6fdd2d"
# <!-- tab-twins:begin babynames = babynames.with_columns(name_lengths=pl.col("name_lengths") - 1) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Modify the "name_lengths" column to be one less than its original value
# babynames = babynames.with_columns(name_lengths=pl.col("name_lengths") - 1)
# babynames.head()
# ```
#
# ```text
# shape: (5, 6)
# ┌───────┬─────┬──────┬──────────┬───────┬──────────────┐
# │ State ┆ Sex ┆ Year ┆ Name     ┆ Count ┆ name_lengths │
# │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   ┆ ---          │
# │ str   ┆ str ┆ i64  ┆ str      ┆ i64   ┆ u32          │
# ╞═══════╪═════╪══════╪══════════╪═══════╪══════════════╡
# │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   ┆ 3            │
# │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   ┆ 4            │
# │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   ┆ 6            │
# │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   ┆ 7            │
# │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   ┆ 6            │
# └───────┴─────┴──────┴──────────┴───────┴──────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # Modify the "name_lengths" column to be one less than its original value
# babynames_pd["name_lengths"] = babynames_pd["name_lengths"] - 1
# babynames_pd.head()
# ```
#
# ```text
#   State Sex  Year      Name  Count  name_lengths
# 0    CA   F  1910      Mary    295             3
# 1    CA   F  1910     Helen    239             4
# 2    CA   F  1910   Dorothy    220             6
# 3    CA   F  1910  Margaret    163             7
# 4    CA   F  1910   Frances    134             6
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="a8db4117"
# We can rename a column using the `.rename()` method. It takes in a dictionary that maps old column names to their new ones.

# %% tags=["remove-input", "remove-output"] id="5226c1c0"
# Rename "name_lengths" to "Length"
babynames = babynames.rename({"name_lengths": "Length"})
babynames.head()


# %% [markdown] id="b2d58a6b"
# <!-- tab-twins:begin babynames = babynames.rename({"name_lengths": "Length"}) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Rename "name_lengths" to "Length"
# babynames = babynames.rename({"name_lengths": "Length"})
# babynames.head()
# ```
#
# ```text
# shape: (5, 6)
# ┌───────┬─────┬──────┬──────────┬───────┬────────┐
# │ State ┆ Sex ┆ Year ┆ Name     ┆ Count ┆ Length │
# │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   ┆ ---    │
# │ str   ┆ str ┆ i64  ┆ str      ┆ i64   ┆ u32    │
# ╞═══════╪═════╪══════╪══════════╪═══════╪════════╡
# │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   ┆ 3      │
# │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   ┆ 4      │
# │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   ┆ 6      │
# │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   ┆ 7      │
# │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   ┆ 6      │
# └───────┴─────┴──────┴──────────┴───────┴────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # Rename "name_lengths" to "Length"
# babynames_pd = babynames_pd.rename(columns={"name_lengths": "Length"})
# babynames_pd.head()
# ```
#
# ```text
#   State Sex  Year      Name  Count  Length
# 0    CA   F  1910      Mary    295       3
# 1    CA   F  1910     Helen    239       4
# 2    CA   F  1910   Dorothy    220       6
# 3    CA   F  1910  Margaret    163       7
# 4    CA   F  1910   Frances    134       6
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="a4dbe726"
# If we want to remove a column of a `DataFrame`, we can call the `.drop()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.drop.html) method with the name of the column to remove. Dropping rows, by contrast, is a job for `filter`.

# %% tags=["remove-input", "remove-output"] id="00318c2d"
# Drop our new "Length" column from the DataFrame
babynames = babynames.drop("Length")
babynames.head()


# %% [markdown] id="6a6e637b"
# <!-- tab-twins:begin babynames = babynames.drop("Length") -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Drop our new "Length" column from the DataFrame
# babynames = babynames.drop("Length")
# babynames.head()
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
# # Drop our new "Length" column from the DataFrame
# babynames_pd = babynames_pd.drop(columns="Length")
# babynames_pd.head()
# ```
#
# ```text
#   State Sex  Year      Name  Count
# 0    CA   F  1910      Mary    295
# 1    CA   F  1910     Helen    239
# 2    CA   F  1910   Dorothy    220
# 3    CA   F  1910  Margaret    163
# 4    CA   F  1910   Frances    134
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="875e6f28"
# Notice that each of the cells above *re-assigned* `babynames` to the result of the call. This is a subtle but important point: table operations **do not occur in place**. `.with_columns()`, `.rename()`, and `.drop()` each build a new table and hand it back, leaving the table they were called on exactly as it was. The same is true of `filter`, `select`, `.sort()`, and `with_row_index`, which is why `elections` was unchanged earlier in the chapter.
#
# In other words, if we simply call:

# %% tags=["remove-input", "remove-output"] id="d749a213"
# This produces a new table without the column "Name"...
babynames.drop("Name")

# ...but the original `babynames` is unchanged!
# Notice that the "Name" column is still present
babynames.head()


# %% [markdown] id="39c1f83d"
# <!-- tab-twins:begin babynames.drop("Name") -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # This produces a new table without the column "Name"...
# babynames.drop("Name")
#
# # ...but the original `babynames` is unchanged!
# # Notice that the "Name" column is still present
# babynames.head()
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
# # This produces a new table without the column "Name"...
# babynames_pd.drop(columns="Name")
#
# # ...but the original `babynames_pd` is unchanged!
# # Notice that the "Name" column is still present
# babynames_pd.head()
# ```
#
# ```text
#   State Sex  Year      Name  Count
# 0    CA   F  1910      Mary    295
# 1    CA   F  1910     Helen    239
# 2    CA   F  1910   Dorothy    220
# 3    CA   F  1910  Margaret    163
# 4    CA   F  1910   Frances    134
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="e8011ccd"
# ## Sorting
#
# Ordering a `DataFrame` can be useful for isolating extreme values. For example, the first 5 rows of a table sorted in descending order (that is, from highest to lowest) hold the 5 largest values. `.sort()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.sort.html) orders a `DataFrame` by a column we name. It sorts from lowest to highest unless we ask otherwise with `descending=True`.

# %% tags=["remove-input", "remove-output"] id="7291ec4a"
# Sort the "Count" column from lowest to highest
babynames.sort("Count").head()


# %% [markdown] id="0c00ef04"
# <!-- tab-twins:begin babynames.sort("Count").head() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Sort the "Count" column from lowest to highest
# babynames.sort("Count").head()
# ```
#
# ```text
# shape: (5, 5)
# ┌───────┬─────┬──────┬──────────┬───────┐
# │ State ┆ Sex ┆ Year ┆ Name     ┆ Count │
# │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   │
# │ str   ┆ str ┆ i64  ┆ str      ┆ i64   │
# ╞═══════╪═════╪══════╪══════════╪═══════╡
# │ CA    ┆ F   ┆ 1910 ┆ Adelaide ┆ 5     │
# │ CA    ┆ F   ┆ 1910 ┆ Adele    ┆ 5     │
# │ CA    ┆ F   ┆ 1910 ┆ Adrienne ┆ 5     │
# │ CA    ┆ F   ┆ 1910 ┆ Althea   ┆ 5     │
# │ CA    ┆ F   ┆ 1910 ┆ Antonia  ┆ 5     │
# └───────┴─────┴──────┴──────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd.sort_values("Count").head()
# ```
#
# ```text
#        State Sex  Year       Name  Count
# 407427    CA   M  2022       Zylo      5
# 300815    CA   M  1981  Broderick      5
# 300816    CA   M  1981     Brooke      5
# 300817    CA   M  1981        Bud      5
# 300818    CA   M  1981        Cha      5
# ```
# ::::
# :::::
# <!-- tab-twins:end -->
# %% tags=["remove-input", "remove-output"] id="20d2d0ca"
# Sort the "Count" column from highest to lowest
babynames.sort("Count", descending=True).head()


# %% [markdown] id="31182353"
# <!-- tab-twins:begin babynames.sort("Count", descending=True).head() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Sort the "Count" column from highest to lowest
# babynames.sort("Count", descending=True).head()
# ```
#
# ```text
# shape: (5, 5)
# ┌───────┬─────┬──────┬─────────┬───────┐
# │ State ┆ Sex ┆ Year ┆ Name    ┆ Count │
# │ ---   ┆ --- ┆ ---  ┆ ---     ┆ ---   │
# │ str   ┆ str ┆ i64  ┆ str     ┆ i64   │
# ╞═══════╪═════╪══════╪═════════╪═══════╡
# │ CA    ┆ M   ┆ 1957 ┆ Michael ┆ 8260  │
# │ CA    ┆ M   ┆ 1956 ┆ Michael ┆ 8258  │
# │ CA    ┆ M   ┆ 1990 ┆ Michael ┆ 8246  │
# │ CA    ┆ M   ┆ 1969 ┆ Michael ┆ 8245  │
# │ CA    ┆ M   ┆ 1970 ┆ Michael ┆ 8196  │
# └───────┴─────┴──────┴─────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd.sort_values("Count", ascending=False).head()
# ```
#
# ```text
#        State Sex  Year     Name  Count
# 268041    CA   M  1957  Michael   8260
# 267017    CA   M  1956  Michael   8258
# 317387    CA   M  1990  Michael   8246
# 281850    CA   M  1969  Michael   8245
# 283146    CA   M  1970  Michael   8196
# ```
# ::::
# :::::
# <!-- tab-twins:end -->
# %% [markdown] id="b88888a1"
# There are a lot of Michaels in California: all five of the largest counts in the dataset belong to that name, topping out at 8,260 babies in 1957.
#
# A `Series` sorts the same way. There is no column to name, since a `Series` is a single column, and only its values come back in their new order.

# %% tags=["remove-input", "remove-output"] id="a382a073"
# Sort the "Name" Series alphabetically
babynames["Name"].sort().head(5)


# %% [markdown] id="af753b10"
# <!-- tab-twins:begin babynames["Name"].sort().head(5) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Sort the "Name" Series alphabetically
# babynames["Name"].sort().head(5)
# ```
#
# ```text
# shape: (5,)
# Series: 'Name' [str]
# [
# 	"Aadan"
# 	"Aadan"
# 	"Aadan"
# 	"Aadarsh"
# 	"Aaden"
# ]
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd["Name"].sort_values().head(5)
# ```
#
# ```text
# 366001      Aadan
# 384005      Aadan
# 369120      Aadan
# 398211    Aadarsh
# 370306      Aaden
# Name: Name, dtype: object
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="81dc72e0"
# ::: {warning}
# `.sort()` places null values **first**, ahead of every real value, in both sort directions. A `.head()` or a positional slice taken straight after a sort will therefore pick up missing values and push out the rows you were after. Nothing about that is an error, so nothing announces it. Pass `nulls_last=True` whenever a sort feeds a `.head()`, a `.tail()`, or a slice, unless you already know the column holds no nulls — as is the case for both datasets in this chapter.
# :::
#
# `babynames` has no missing values, so the small table below has one instead.

# %% tags=["remove-input", "remove-output"] id="9ed57619"
demo = pl.DataFrame({"Name": ["Aaliyah", "Bao", "Cyrus"], "Count": [3, None, 1]})
demo.sort("Count", descending=True)


# %% [markdown] id="f8ad6158"
# <!-- tab-twins:begin demo = pl.DataFrame( -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# demo = pl.DataFrame({"Name": ["Aaliyah", "Bao", "Cyrus"], "Count": [3, None, 1]})
# demo.sort("Count", descending=True)
# ```
#
# ```text
# shape: (3, 2)
# ┌─────────┬───────┐
# │ Name    ┆ Count │
# │ ---     ┆ ---   │
# │ str     ┆ i64   │
# ╞═════════╪═══════╡
# │ Bao     ┆ null  │
# │ Aaliyah ┆ 3     │
# │ Cyrus   ┆ 1     │
# └─────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# demo_pd = pd.DataFrame({"Name": ["Aaliyah", "Bao", "Cyrus"],
#                         "Count": [3, None, 1]})
# demo_pd.sort_values("Count", ascending=False)
# ```
#
# ```text
#       Name  Count
# 0  Aaliyah    3.0
# 2    Cyrus    1.0
# 1      Bao    NaN
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="9384cac3"
# Sorting from highest to lowest put the missing count at the top. `nulls_last=True` sends it to the bottom, where it stays out of the way of a `.head()`.

# %% tags=["remove-input", "remove-output"] id="82a35df6"
demo.sort("Count", descending=True, nulls_last=True)


# %% [markdown] id="05ce993a"
# <!-- tab-twins:begin demo.sort("Count", descending=True, nulls_last=True) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# demo.sort("Count", descending=True, nulls_last=True)
# ```
#
# ```text
# shape: (3, 2)
# ┌─────────┬───────┐
# │ Name    ┆ Count │
# │ ---     ┆ ---   │
# │ str     ┆ i64   │
# ╞═════════╪═══════╡
# │ Aaliyah ┆ 3     │
# │ Cyrus   ┆ 1     │
# │ Bao     ┆ null  │
# └─────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# demo_pd.sort_values("Count", ascending=False, na_position="last")
# ```
#
# ```text
#       Name  Count
# 0  Aaliyah    3.0
# 2    Cyrus    1.0
# 1      Bao    NaN
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="f969ebb1"
# ## Custom Sorts
#
# Now, let's try to solve a sorting problem using different approaches. Assume we want to find the longest baby names and sort our data accordingly.
#
# ### Approach 1: Create a Temporary Column
#
# One method to do this is to first start by creating a column that contains the lengths of the names.

# %% tags=["remove-input", "remove-output"] id="b03313db"
# Create a Series of the length of each name
babyname_lengths = babynames["Name"].str.len_chars()

# Add a column named "name_lengths" that includes the length of each name
babynames = babynames.with_columns(name_lengths=babyname_lengths)
babynames.head(5)


# %% [markdown] id="b5abf721"
# <!-- tab-twins:begin babynames = babynames.with_columns(name_lengths=babyname_lengths) babynames.head(5) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Create a Series of the length of each name
# babyname_lengths = babynames["Name"].str.len_chars()
#
# # Add a column named "name_lengths" that includes the length of each name
# babynames = babynames.with_columns(name_lengths=babyname_lengths)
# babynames.head(5)
# ```
#
# ```text
# shape: (5, 6)
# ┌───────┬─────┬──────┬──────────┬───────┬──────────────┐
# │ State ┆ Sex ┆ Year ┆ Name     ┆ Count ┆ name_lengths │
# │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   ┆ ---          │
# │ str   ┆ str ┆ i64  ┆ str      ┆ i64   ┆ u32          │
# ╞═══════╪═════╪══════╪══════════╪═══════╪══════════════╡
# │ CA    ┆ F   ┆ 1910 ┆ Mary     ┆ 295   ┆ 4            │
# │ CA    ┆ F   ┆ 1910 ┆ Helen    ┆ 239   ┆ 5            │
# │ CA    ┆ F   ┆ 1910 ┆ Dorothy  ┆ 220   ┆ 7            │
# │ CA    ┆ F   ┆ 1910 ┆ Margaret ┆ 163   ┆ 8            │
# │ CA    ┆ F   ┆ 1910 ┆ Frances  ┆ 134   ┆ 7            │
# └───────┴─────┴──────┴──────────┴───────┴──────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # Create a Series of the length of each name
# babyname_lengths_pd = babynames_pd["Name"].str.len()
#
# # Add a column named "name_lengths" that includes the length of each name
# babynames_pd["name_lengths"] = babyname_lengths_pd
# babynames_pd.head(5)
# ```
#
# ```text
#   State Sex  Year      Name  Count  name_lengths
# 0    CA   F  1910      Mary    295             4
# 1    CA   F  1910     Helen    239             5
# 2    CA   F  1910   Dorothy    220             7
# 3    CA   F  1910  Margaret    163             8
# 4    CA   F  1910   Frances    134             7
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="dcaf47bf"
# We can then sort the `DataFrame` by that column using `.sort()`:

# %% tags=["remove-input", "remove-output"] id="13b0ee0c"
# Sort by the temporary column
babynames = babynames.sort(by="name_lengths", descending=True)
babynames.head(5)


# %% [markdown] id="20fb2d16"
# <!-- tab-twins:begin babynames = babynames.sort(by="name_lengths", descending=True) -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Sort by the temporary column
# babynames = babynames.sort(by="name_lengths", descending=True)
# babynames.head(5)
# ```
#
# ```text
# shape: (5, 6)
# ┌───────┬─────┬──────┬─────────────────┬───────┬──────────────┐
# │ State ┆ Sex ┆ Year ┆ Name            ┆ Count ┆ name_lengths │
# │ ---   ┆ --- ┆ ---  ┆ ---             ┆ ---   ┆ ---          │
# │ str   ┆ str ┆ i64  ┆ str             ┆ i64   ┆ u32          │
# ╞═══════╪═════╪══════╪═════════════════╪═══════╪══════════════╡
# │ CA    ┆ F   ┆ 1986 ┆ Mariadelosangel ┆ 5     ┆ 15           │
# │ CA    ┆ M   ┆ 1987 ┆ Franciscojavier ┆ 5     ┆ 15           │
# │ CA    ┆ M   ┆ 1988 ┆ Franciscojavier ┆ 10    ┆ 15           │
# │ CA    ┆ M   ┆ 1989 ┆ Franciscojavier ┆ 6     ┆ 15           │
# │ CA    ┆ M   ┆ 1991 ┆ Ryanchristopher ┆ 7     ┆ 15           │
# └───────┴─────┴──────┴─────────────────┴───────┴──────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # Sort by the temporary column
# babynames_pd = babynames_pd.sort_values(by="name_lengths", ascending=False)
# babynames_pd.head(5)
# ```
#
# ```text
#        State Sex  Year             Name  Count  name_lengths
# 334166    CA   M  1996  Franciscojavier      8            15
# 337301    CA   M  1997  Franciscojavier      5            15
# 339472    CA   M  1998  Franciscojavier      6            15
# 321792    CA   M  1991  Ryanchristopher      7            15
# 327358    CA   M  1993  Johnchristopher      5            15
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="40df830b"
# The longest names in the dataset run to 15 characters. Finally, we can drop the `name_lengths` column from `babynames` to prevent our table from getting cluttered.

# %% tags=["remove-input", "remove-output"] id="1af7c9a5"
# Drop the "name_lengths" column
babynames = babynames.drop("name_lengths")
babynames.head(5)


# %% [markdown] id="49af424f"
# <!-- tab-twins:begin babynames = babynames.drop("name_lengths") -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Drop the "name_lengths" column
# babynames = babynames.drop("name_lengths")
# babynames.head(5)
# ```
#
# ```text
# shape: (5, 5)
# ┌───────┬─────┬──────┬─────────────────┬───────┐
# │ State ┆ Sex ┆ Year ┆ Name            ┆ Count │
# │ ---   ┆ --- ┆ ---  ┆ ---             ┆ ---   │
# │ str   ┆ str ┆ i64  ┆ str             ┆ i64   │
# ╞═══════╪═════╪══════╪═════════════════╪═══════╡
# │ CA    ┆ F   ┆ 1986 ┆ Mariadelosangel ┆ 5     │
# │ CA    ┆ M   ┆ 1987 ┆ Franciscojavier ┆ 5     │
# │ CA    ┆ M   ┆ 1988 ┆ Franciscojavier ┆ 10    │
# │ CA    ┆ M   ┆ 1989 ┆ Franciscojavier ┆ 6     │
# │ CA    ┆ M   ┆ 1991 ┆ Ryanchristopher ┆ 7     │
# └───────┴─────┴──────┴─────────────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # Drop the "name_lengths" column
# babynames_pd = babynames_pd.drop(columns="name_lengths")
# babynames_pd.head(5)
# ```
#
# ```text
#        State Sex  Year             Name  Count
# 334166    CA   M  1996  Franciscojavier      8
# 337301    CA   M  1997  Franciscojavier      5
# 339472    CA   M  1998  Franciscojavier      6
# 321792    CA   M  1991  Ryanchristopher      7
# 327358    CA   M  1993  Johnchristopher      5
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="edad1790"
# ### Approach 2: Sorting on an Expression
#
# Another way to approach this is to hand `.sort()` an expression instead of a column name. The sort key is then computed on the way in, so there is no temporary column to create and no temporary column to drop.

# %% tags=["remove-input", "remove-output"] id="3b1138f3"
babynames.sort(pl.col("Name").str.len_chars(), descending=True).head()


# %% [markdown] id="0604482f"
# <!-- tab-twins:begin babynames.sort(pl.col("Name").str.len_chars(), descending=True).head() -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# babynames.sort(pl.col("Name").str.len_chars(), descending=True).head()
# ```
#
# ```text
# shape: (5, 5)
# ┌───────┬─────┬──────┬─────────────────┬───────┐
# │ State ┆ Sex ┆ Year ┆ Name            ┆ Count │
# │ ---   ┆ --- ┆ ---  ┆ ---             ┆ ---   │
# │ str   ┆ str ┆ i64  ┆ str             ┆ i64   │
# ╞═══════╪═════╪══════╪═════════════════╪═══════╡
# │ CA    ┆ F   ┆ 1986 ┆ Mariadelosangel ┆ 5     │
# │ CA    ┆ M   ┆ 1987 ┆ Franciscojavier ┆ 5     │
# │ CA    ┆ M   ┆ 1988 ┆ Franciscojavier ┆ 10    │
# │ CA    ┆ M   ┆ 1989 ┆ Franciscojavier ┆ 6     │
# │ CA    ┆ M   ┆ 1991 ┆ Ryanchristopher ┆ 7     │
# └───────┴─────┴──────┴─────────────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# babynames_pd.assign(_len=babynames_pd["Name"].str.len()).sort_values(
#     "_len", ascending=False
# ).drop(columns="_len").head()
# ```
#
# ```text
#        State Sex  Year             Name  Count
# 334166    CA   M  1996  Franciscojavier      8
# 327472    CA   M  1993  Ryanchristopher      5
# 337301    CA   M  1997  Franciscojavier      5
# 337477    CA   M  1997  Ryanchristopher      5
# 312543    CA   M  1987  Franciscojavier      5
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="022f7146"
# ### Approach 3: Sorting with `map_elements`
#
# We can also use `map_elements` [(documentation)](https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.map_elements.html) if we want to sort by an arbitrarily defined Python function. Say we want to sort the `babynames` table by the number of `"dr"`s and `"ea"`s in each `"Name"`. We'll define the function `dr_ea_count` to help us out.
#
# `map_elements` hands each value of the column to that function, one value at a time, and collects the results. `return_dtype` tells Polars what type those results will have.

# %% tags=["remove-input", "remove-output"] id="7c7f19d6"
# First, define a function to count the number of times
# "dr" or "ea" appear in each name
def dr_ea_count(string):
    return string.count('dr') + string.count('ea')

# Then, use map_elements to apply dr_ea_count to each name in the "Name" column
babynames = babynames.with_columns(
    dr_ea_count=pl.col("Name").map_elements(dr_ea_count, return_dtype=pl.Int64)
)

# Sort the DataFrame by the new "dr_ea_count" column so we can see our handiwork
babynames = babynames.sort(by="dr_ea_count", descending=True)
babynames.head()


# %% [markdown] id="7e59d5ac"
# <!-- tab-twins:begin def dr_ea_count(string): -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # First, define a function to count the number of times
# # "dr" or "ea" appear in each name
# def dr_ea_count(string):
#     return string.count('dr') + string.count('ea')
#
# # Then, use map_elements to apply dr_ea_count to each name in the "Name" column
# babynames = babynames.with_columns(
#     dr_ea_count=pl.col("Name").map_elements(dr_ea_count, return_dtype=pl.Int64)
# )
#
# # Sort the DataFrame by the new "dr_ea_count" column so we can see our handiwork
# babynames = babynames.sort(by="dr_ea_count", descending=True)
# babynames.head()
# ```
#
# ```text
# shape: (5, 6)
# ┌───────┬─────┬──────┬──────────┬───────┬─────────────┐
# │ State ┆ Sex ┆ Year ┆ Name     ┆ Count ┆ dr_ea_count │
# │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   ┆ ---         │
# │ str   ┆ str ┆ i64  ┆ str      ┆ i64   ┆ i64         │
# ╞═══════╪═════╪══════╪══════════╪═══════╪═════════════╡
# │ CA    ┆ F   ┆ 1986 ┆ Deandrea ┆ 6     ┆ 3           │
# │ CA    ┆ F   ┆ 1988 ┆ Deandrea ┆ 5     ┆ 3           │
# │ CA    ┆ F   ┆ 1990 ┆ Deandrea ┆ 5     ┆ 3           │
# │ CA    ┆ F   ┆ 1994 ┆ Leandrea ┆ 5     ┆ 3           │
# │ CA    ┆ M   ┆ 1985 ┆ Deandrea ┆ 6     ┆ 3           │
# └───────┴─────┴──────┴──────────┴───────┴─────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # First, define a function to count the number of times
# # "dr" or "ea" appear in each name
# def dr_ea_count_pd(string):
#     return string.count('dr') + string.count('ea')
#
# # Then, use apply to run dr_ea_count over each name in the "Name" column
# babynames_pd["dr_ea_count"] = babynames_pd["Name"].apply(dr_ea_count_pd)
#
# # Sort the DataFrame by the new "dr_ea_count" column so we can see our handiwork
# babynames_pd = babynames_pd.sort_values(by="dr_ea_count", ascending=False)
# babynames_pd.head()
# ```
#
# ```text
#        State Sex  Year      Name  Count  dr_ea_count
# 115957    CA   F  1990  Deandrea      5            3
# 101976    CA   F  1986  Deandrea      6            3
# 131029    CA   F  1994  Leandrea      5            3
# 108731    CA   F  1988  Deandrea      5            3
# 308131    CA   M  1985  Deandrea      6            3
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="14eabcd4"
# Because it runs Python code once per row, `map_elements` is much slower than the expression in Approach 2, which Polars evaluates on the whole column at once. Save it for the cases where nothing in the expression API will do the job.
#
# We can drop `dr_ea_count` once we're done using it to maintain a neat table.

# %% tags=["remove-input", "remove-output"] id="246743e0"
# Drop the "dr_ea_count" column
babynames = babynames.drop("dr_ea_count")
babynames.head(5)


# %% [markdown] id="3b353c48"
# <!-- tab-twins:begin babynames = babynames.drop("dr_ea_count") -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Drop the "dr_ea_count" column
# babynames = babynames.drop("dr_ea_count")
# babynames.head(5)
# ```
#
# ```text
# shape: (5, 5)
# ┌───────┬─────┬──────┬──────────┬───────┐
# │ State ┆ Sex ┆ Year ┆ Name     ┆ Count │
# │ ---   ┆ --- ┆ ---  ┆ ---      ┆ ---   │
# │ str   ┆ str ┆ i64  ┆ str      ┆ i64   │
# ╞═══════╪═════╪══════╪══════════╪═══════╡
# │ CA    ┆ F   ┆ 1986 ┆ Deandrea ┆ 6     │
# │ CA    ┆ F   ┆ 1988 ┆ Deandrea ┆ 5     │
# │ CA    ┆ F   ┆ 1990 ┆ Deandrea ┆ 5     │
# │ CA    ┆ F   ┆ 1994 ┆ Leandrea ┆ 5     │
# │ CA    ┆ M   ┆ 1985 ┆ Deandrea ┆ 6     │
# └───────┴─────┴──────┴──────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # Drop the "dr_ea_count" column
# babynames_pd = babynames_pd.drop(columns="dr_ea_count")
# babynames_pd.head(5)
# ```
#
# ```text
#        State Sex  Year      Name  Count
# 115957    CA   F  1990  Deandrea      5
# 101976    CA   F  1986  Deandrea      6
# 131029    CA   F  1994  Leandrea      5
# 108731    CA   F  1988  Deandrea      5
# 308131    CA   M  1985  Deandrea      6
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="3096db81"
# ## Parting Note
#
# The Polars library is enormous and contains many useful functions. Here is a link to its [documentation](https://docs.pola.rs/api/python/stable/reference/index.html). We certainly don't expect you to memorize each and every method of the library, and we will give you a reference sheet for exams.
#
# Manipulating `DataFrame`s is not a skill that is mastered in just one day. The three custom sorts above all answer the same question, and none of them is the "real" one; trying several routes from point A to point B is how the syntax stops feeling arbitrary.
#
# A goal of this course is to help you build your familiarity with the real-world programming practice of ... Googling! Answers to your questions can be found in documentation, Stack Overflow, and elsewhere. Being able to search for, read, and implement documentation is an important life skill for any data scientist.
#
# Next, we will start digging deeper into the mechanics behind grouping data.
