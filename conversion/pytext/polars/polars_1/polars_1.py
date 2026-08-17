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

# %% [markdown]
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

# %%
# `pl` is the conventional alias for Polars, as `np` is for NumPy
import polars as pl

# %% [markdown]
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

# %%
elections = pl.read_csv("data/elections.csv")
elections

# %% [markdown]
# The code above stores our `DataFrame` object in the `elections` variable. Upon inspection, our `elections` `DataFrame` has 182 rows and 6 columns (`Year`, `Candidate`, `Party`, `Popular vote`, `Result`, `%`). Each row represents a single record — in our example, a presidential candidate from some particular year. Each column represents a single attribute or feature of the record.
#
# Notice the three lines Polars prints above the data itself. The first gives the shape of the table, the second names the columns, and the third gives the data type of each column: `str` for the text columns, `i64` for whole numbers, `f64` for decimals. Every table you print tells you how big it is and what it holds.
#
# `read_csv` also takes optional arguments that shape the table as it is read.

# %%
# `columns` keeps just the columns we name, in the order we name them
pl.read_csv("data/elections.csv", columns=["Candidate", "Year", "%"])

# %%
# `n_rows` stops reading after the first few rows, which is handy for a very large file
pl.read_csv("data/elections.csv", n_rows=5)

# %% [markdown]
# ### From a List of Rows
#
# We'll now explore creating a `DataFrame` with data of our own. The two cells below build the same two-row table of fruit prices, one row at a time.
#
# The first passes a list of lists. `schema` names the columns, and `orient="row"` tells Polars to read each inner list as a row rather than as a column.

# %%
df_list_1 = pl.DataFrame(
    [["Kiwi", 5.49],
     ["Orange", 3.99]],
    schema=["Fruit", "Price"], orient="row"
)
df_list_1

# %% [markdown]
# The second passes a list of dictionaries. Each dictionary is a row, and its keys supply the column names, so there is no schema to write out.

# %%
df_list_2 = pl.DataFrame(
    [{"Fruit": "Kiwi", "Price": 5.49},
     {"Fruit": "Orange", "Price": 3.99}]
)
df_list_2

# %% [markdown]
# ### From a Dictionary of Columns
#
# A dictionary describes the table by column instead of by row: each key is a column name, and each value holds that column's data.

# %%
df_dict = pl.DataFrame(
    {"Fruit": ["Kiwi", "Orange"],
     "Price": [5.49, 3.99]}
)
df_dict

# %% [markdown]
# ### From a `Series`
#
# Since a `DataFrame` is a collection of equal-length `Series`, we can build one out of `Series` we already have. Consider `ser_a` and `ser_b`.

# %%
ser_a = pl.Series("ser_a", ["a1", "a2", "a3"])
ser_b = pl.Series("ser_b", ["b1", "b2", "b3"])
ser_a

# %% [markdown]
# Passing them in a dictionary puts them side by side, under whatever column names we choose.

# %%
pl.DataFrame(
    {"ColumnA": ser_a, "ColumnB": ser_b}
)

# %% [markdown]
# A single `Series` makes a one-column `DataFrame`, either by handing it to the constructor or by calling `.to_frame()` on it. Either way, the name of the `Series` becomes the name of the column.

# %%
pl.DataFrame(ser_a)

# %%
ser_a.to_frame()

# %% [markdown]
# ## `DataFrame` Attributes: `columns`, `dtypes`, and `shape`
#
# Column names in a `DataFrame` are almost always unique. Looking back to the `elections` dataset, it wouldn't make sense to have two columns named `"Candidate"`. Sometimes you'll want to extract the names, the types, or the size of a table rather than the data itself, most often when meeting a dataset for the first time.
#
# For the column names, use `DataFrame.columns`:

# %%
elections.columns

# %% [markdown]
# For the data type of each column, use `DataFrame.dtypes`. The types come back in the same order as the names above.

# %%
elections.dtypes

# %% [markdown]
# `DataFrame.schema` reports both at once, pairing each column with its type. This is the quickest way to check that a file was read the way you expected: that a column of years arrived as `Int64` rather than as `String`, for instance.

# %%
elections.schema

# %% [markdown]
# And for the size of the `DataFrame`, `DataFrame.shape` gives the number of rows followed by the number of columns:

# %%
elections.shape

# %% [markdown]
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

# %%
# Extract the first 5 rows of the DataFrame
elections.head()

# %% [markdown]
# Similarly, calling `df.tail(n)` allows us to extract the last `n` rows of the `DataFrame`.

# %%
# Extract the last 5 rows of the DataFrame
elections.tail(5)

# %% [markdown]
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

# %%
elections[0, "Candidate"]

# %% [markdown]
# Two single values pick out one cell, and what comes back is the value sitting in it: here, the string `'Andrew Jackson'`.
#
# Two lists pick out a rectangle of the table. The rows arrive in the order we asked for them rather than in table order.

# %%
elections[[87, 25, 179], ["Year", "Party", "%"]]

# %% [markdown]
# A slice of column labels runs from one column to another and includes both ends. `"%"` is the last column of `elections`, and it appears in the result below.

# %%
elections[[87, 25, 179], "Popular vote":"%"]

# %% [markdown]
# Suppose instead that we want *all* rows and only a few columns. The shorthand `:` is useful for this.

# %%
elections[:, ["Year", "Candidate", "Result"]]

# %% [markdown]
# We can use the same shorthand to ask for all columns.

# %%
elections[[87, 25, 179], :]

# %% [markdown]
# A single column label returns that column as a `Series`.

# %%
elections[[87, 25, 179], "Popular vote"]

# %% [markdown]
# Wrapping that same label in a list asks for a table of one column, and a table of one column is what comes back.

# %%
elections[[87, 25, 179], ["Popular vote"]]

# %% [markdown]
# When `[]` is given only one argument, and that argument is a list of integers or a slice, Polars reads it as rows and hands back every column.

# %%
elections[[180, 181]]

# %% [markdown]
# A single argument that is a *string*, on the other hand, names a column, and that column comes back as a `Series`. This is the shorthand we use whenever we want one column and nothing else, and it shows up throughout the rest of the chapter.

# %%
elections["Candidate"]

# %% [markdown]
# #### Selecting Columns by Position
#
# The second argument to `[]` accepts **column numbers** as well as column labels. The numbers count from the left edge of the table, starting at 0, so `elections[:, 1]` and `elections[:, "Candidate"]` name the same column.
#
# Slicing by column number, like slicing by row position, is **exclusive** of the right-hand side of the slice. The inclusive behavior we saw above belongs to label slices only.

# %%
# Extracting the value at the first row (row 0) and the second column
# Remember that Python indexing begins at position 0!
elections[0, 1]

# %%
# Extracting the second, third, and fourth rows of the second column
# (returns a Series, since we asked for a single column)
elections[[1, 2, 3], 1]

# %%
# Select the rows at positions 1, 2, and 3
# Select the columns at positions 0, 1, and 2
elections[[1, 2, 3], [0, 1, 2]]

# %%
# A list of row positions and a slice of column numbers
# The column at position 3 is left out, since number slices are exclusive
elections[[1, 2, 3], 0:3]

# %%
# One argument, so Polars reads it as rows and returns all columns
elections[138:144]

# %% [markdown]
# A whole row on its own comes back from `.row()`, as a tuple of values in column order.

# %%
elections.row(0)

# %% [markdown]
# Passing `named=True` gives a dictionary instead, which is much easier to read when a table is wide.

# %%
elections.row(0, named=True)

# %% [markdown]
# A row's position is the only handle we have on it, and that position belongs to the table rather than to the row. Any operation that reorders the table therefore hands out new positions, which is a point we return to at the end of the section.
#
# ### Extraction with `filter` and `select`
#
# `[]` asks for positions and labels, which makes it concise for the quick looks at a table we take constantly. Anything *computed*, though (a condition, an arithmetic result) goes through a second pair of methods.
#
# `filter` chooses rows and `select` chooses columns. Both take **expressions**, which are built with `pl.col` and can compare and combine columns before anything is returned. This is the pairing you'll reach for most often, because a condition like "more than 60 million popular votes" describes the rows you want without needing to know where they sit.
#
# Two rules cover most of the confusion: `filter` narrows the rows and leaves every column in place, and `select` decides which columns come back.

# %%
# select takes a list of column names and returns a DataFrame
elections.select(["Year", "Candidate", "Result"])

# %% [markdown]
# `select` also accepts a computed expression. `pl.col("Popular vote")` refers to that column, arithmetic on it applies to every value, and `.alias` names the result.

# %%
elections.select((pl.col("Popular vote") / 1_000_000).alias("Popular vote (millions)"))

# %% [markdown]
# `filter` takes a condition and returns the rows that satisfy it. Eight candidacies in the dataset drew more than 60 million popular votes, the earliest of them in 2004.

# %%
elections.filter(pl.col("Popular vote") > 60000000)

# %% [markdown]
# Each of these methods returns a `DataFrame`, so the two can be chained: filter the rows first, then pick the columns to keep.

# %%
elections.filter(pl.col("Year") == 2008).select(["Year", "Candidate"])

# %% [markdown]
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

# %%
# Grab rows from 2008 OR candidates winning over 60% of the vote (or both)
elections.filter((pl.col("Year") == 2008) | (pl.col("%") >= 60))

# %% [markdown]
# Ten rows satisfy that condition: the six candidates who stood in 2008, plus the four landslide winners of 1920, 1936, 1964, and 1972.
#
# If we want the rows where *both* conditions hold, we use `&`.

# %%
# Grab post-2000 winners: rows where the year is after 2000 AND the result is a win
elections.filter((pl.col("Year") > 2000) & (pl.col("Result") == "win"))

# %% [markdown]
# Note that we need the bitwise operators here, not Python's `and` and `or`. Those two ask a single
# yes-or-no question about the whole object, and an expression stands for a column of many values,
# so there is no one answer to give:

# %% id="ccf796ec"
# This line of code will raise a TypeError
elections.filter((pl.col("Year") == 2008) and (pl.col("%") >= 60))

# %% [markdown]
# Conditions can be strung together as far as we need. Wrapping the whole call in parentheses lets us break a long one across several lines, which is worth doing well before it becomes hard to read.

# %%
# To make code more readable, use multiple lines
elections.filter(
    (pl.col("Year") < 2000) &
    (pl.col("Year") > 1941) &
    (pl.col("Result") == "win") &
    (pl.col("%") >= 55)
)

# %% [markdown]
# ### Working with Row Positions
#
# A row is identified by its position in the table, counting from 0. Those positions are not stored anywhere; `with_row_index` writes them into a column of their own when we want to keep them.
#
# This matters as soon as we reorder a table. Below, we record each row's position and *then* sort by vote share, so the new first column says where each row started out. Lyndon Johnson's 1964 landslide is the largest share in the dataset, and it came from position 114.

# %%
# with_row_index adds a column holding each row's current position
elections.with_row_index("original_position").sort("%", descending=True).head()

# %% [markdown]
# `with_row_index` returns a new table rather than changing the one we called it on, so `elections` itself still has its original six columns and its original order.

# %%
elections.head(3)

# %% [markdown]
# Adding the index column *after* the sort numbers the rows in their new order instead, counting 0, 1, 2 down the sorted table. Which of the two you want depends on whether you care where a row came from or where it now sits.

# %%
elections.sort("%", descending=True).with_row_index().head()

# %% [markdown]
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

# %% tags=["remove-input"]
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

# %% [markdown]
# ## More Ways to Build a Filter
#
# A boolean expression can describe any condition we can write down, but a long list of alternatives gets verbose in a hurry. Suppose we want every row whose name is one of four we care about.

# %%
# Note: The parentheses surrounding the code make it possible to
# break the code into multiple lines for readability. But this is
# still a lot of code just to check for four names...
(
    babynames.filter((pl.col("Name") == "Bella") |
                     (pl.col("Name") == "Alex") |
                     (pl.col("Name") == "Narges") |
                     (pl.col("Name") == "Lisa"))
)

# %% [markdown]
# Fortunately, Polars offers more concise ways of saying the same thing.
#
# The `.is_in()` method checks each value of a column against a sequence of values (a list, an array, or another `Series`). It returns the same 317 rows as the four-way condition above, in one line.

# %%
names = ["Bella", "Alex", "Narges", "Lisa"]
babynames.filter(pl.col("Name").is_in(names))

# %% [markdown]
# String columns carry a whole family of methods under `.str`. `.str.starts_with()` checks the beginning of each string, so the filter below keeps every row whose name begins with the letter `N`.

# %%
# Extracting names that begin with the letter "N"
babynames.filter(pl.col("Name").str.starts_with("N"))

# %% [markdown]
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

# %%
# Pull out the number of babies named Yash each year
yash_counts = babynames.filter(pl.col("Name") == "Yash")["Count"]
yash_counts

# %% [markdown]
# The name appears in 28 rows of the table, and `.mean()` averages the counts across them.

# %%
# Average number of babies named Yash each year
# Keep in mind that even if Python gives you 10 decimal places of precision,
# you should think carefully about how much precision is meaningful!
# In this case, one decimal place or even no decimal places would be appropriate.
yash_counts.mean()

# %%
# Max number of babies named Yash born in any single year
yash_counts.max()

# %% [markdown]
# ### `.shape`, `.height`, and `.width`
#
# These attributes measure the "amount" of data stored in a `DataFrame`. Calling `.shape` returns a tuple containing the number of rows followed by the number of columns.
#
# Many functions strictly require the dimensions of their arguments to match. Asking the table for its dimensions is much faster than counting the items by hand.

# %%
# Return the shape of the DataFrame, in the format (num_rows, num_columns)
babynames.shape

# %% [markdown]
# `.height` and `.width` report those same two numbers one at a time, so multiplying them gives the total number of values the table holds.

# %%
# The total number of entries in the object, equal to num_rows * num_columns
babynames.height * babynames.width

# %% [markdown]
# Calling `len` on a `DataFrame` gives its height, which is the number we want far more often than the other two.

# %%
# Return the number of rows in the DataFrame
len(babynames)

# %% [markdown]
# ### `.describe()`
#
# If many statistics are required from a `DataFrame` (minimum value, maximum value, mean value, etc.), then `.describe()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.describe.html) can be used to compute all of them at once.

# %%
babynames.describe()

# %% [markdown]
# The statistics come back as rows, labeled by the `statistic` column on the left, with one column of results per column of the original table. Text columns are described too: they report a count, a null count, and their alphabetical minimum and maximum, and carry `null` wherever a statistic makes no sense for them.
#
# A few things stand out. No value anywhere in the table is missing, since `null_count` is 0 across the board. The years run from 1910 to 2022. And the smallest `Count` in the dataset is 5, so names rarer than that never made it into the file.
#
# A `Series` can describe itself in the same way, reporting the statistics that suit its data type.

# %%
babynames["Sex"].describe()

# %% [markdown]
# ### `.sample()`
#
# As we will see later in the semester, random processes are at the heart of many data science techniques (for example, train-test splits, bootstrapping, and cross-validation). `.sample()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.sample.html) lets us quickly select random rows of a `DataFrame`.
#
# By default, `.sample()` selects rows *without* replacement. Pass in the argument `with_replacement=True` to sample with replacement.

# %%
# Randomly sample a row from the DataFrame
babynames.sample()

# %% [markdown]
# Naturally, this can be chained with the extraction tools from earlier in the chapter.

# %%
# Sample 5 random rows, and keep all columns from position 2 onwards
babynames.sample(5)[:, 2:]

# %% [markdown]
# Wrapping a chain of methods in parentheses lets us spread it across several lines. Here we narrow the table to the year 2000, sample four of those rows with replacement, and keep the last three columns.

# %%
result = (
    babynames.filter(pl.col("Year") == 2000)
    .sample(4, with_replacement=True)[:, 2:]
)
result

# %% [markdown]
# ::: {tip}
# Rerun any of the cells above and you'll get different rows each time. Pass `seed=` to `.sample()` when you need the same rows on every run, which is most of the time once other people have to reproduce your results.
# :::
#
# ### `.value_counts()`
#
# The `Series.value_counts()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/series/api/polars.Series.value_counts.html) method counts the number of occurrences of each unique value in a `Series`. In other words, it *counts* the number of times each unique *value* appears. This is often useful for determining the most or least common entries in a `Series`.

# %%
babynames["Sex"].value_counts()

# %% [markdown]
# The result is a two-column `DataFrame`: the distinct values, in a column that keeps the name of the original `Series`, and their counts, in a column named `count`. Those rows come back in no particular order, so pass `sort=True` when the ranking is what you are after.
#
# Below, we count the number of times each name appears in the `"Name"` column, which tells us the name recorded in the most sex-and-year combinations.

# %%
babynames["Name"].value_counts(sort=True).head()

# %% [markdown]
# `Jean` leads with 223 rows: 223 separate combinations of a sex and a year in which at least five California babies were given that name.
#
# ### `.unique()`
#
# If we have a `Series` with many repeated values, then `.unique()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/series/api/polars.Series.unique.html) can be used to identify only the *unique* values. Here we return every name in `babynames`.

# %%
babynames["Name"].unique()

# %% [markdown]
# The 407,428 rows of the table hold 20,437 distinct names between them, a count that `.n_unique()` reports directly.

# %%
babynames["Name"].n_unique()

# %% [markdown]
# The unique values arrive in no particular order. When the order matters, `maintain_order=True` returns them in the order they first appear in the `Series`, which here means starting from the top of the table.

# %%
babynames["Name"].unique(maintain_order=True).head(5)

# %% [markdown]
# ## Adding, Removing, and Modifying Columns
#
# In many data science tasks, we may need to change the columns contained in our `DataFrame` in some way. Fortunately, the syntax to do so is fairly straightforward.
#
# To add a new column, hand `.with_columns()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.with_columns.html) a `Series` or an expression under the name we want it to have. Writing that name as a keyword argument, as below, is the most direct way to say it.

# %%
# Create a Series of the length of each name
babyname_lengths = babynames["Name"].str.len_chars()

# Add a column named "name_lengths" that includes the length of each name
babynames = babynames.with_columns(name_lengths=babyname_lengths)
babynames.head()

# %% [markdown]
# If we need to later modify an existing column, we pass the new values to `.with_columns()` under that column's existing name. Inside the expression, `pl.col("name_lengths")` refers to the column as it stands right now.

# %%
# Modify the "name_lengths" column to be one less than its original value
babynames = babynames.with_columns(name_lengths=pl.col("name_lengths") - 1)
babynames.head()

# %% [markdown]
# We can rename a column using the `.rename()` method. It takes in a dictionary that maps old column names to their new ones.

# %%
# Rename "name_lengths" to "Length"
babynames = babynames.rename({"name_lengths": "Length"})
babynames.head()

# %% [markdown]
# If we want to remove a column of a `DataFrame`, we can call the `.drop()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.drop.html) method with the name of the column to remove. Dropping rows, by contrast, is a job for `filter`.

# %%
# Drop our new "Length" column from the DataFrame
babynames = babynames.drop("Length")
babynames.head()

# %% [markdown]
# Notice that each of the cells above *re-assigned* `babynames` to the result of the call. This is a subtle but important point: table operations **do not occur in place**. `.with_columns()`, `.rename()`, and `.drop()` each build a new table and hand it back, leaving the table they were called on exactly as it was. The same is true of `filter`, `select`, `.sort()`, and `with_row_index`, which is why `elections` was unchanged earlier in the chapter.
#
# In other words, if we simply call:

# %%
# This produces a new table without the column "Name"...
babynames.drop("Name")

# ...but the original `babynames` is unchanged!
# Notice that the "Name" column is still present
babynames.head()

# %% [markdown]
# ## Sorting
#
# Ordering a `DataFrame` can be useful for isolating extreme values. For example, the first 5 rows of a table sorted in descending order (that is, from highest to lowest) hold the 5 largest values. `.sort()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.sort.html) orders a `DataFrame` by a column we name. It sorts from lowest to highest unless we ask otherwise with `descending=True`.

# %%
# Sort the "Count" column from lowest to highest
babynames.sort("Count").head()

# %%
# Sort the "Count" column from highest to lowest
babynames.sort("Count", descending=True).head()

# %% [markdown]
# There are a lot of Michaels in California: all five of the largest counts in the dataset belong to that name, topping out at 8,260 babies in 1957.
#
# A `Series` sorts the same way. There is no column to name, since a `Series` is a single column, and only its values come back in their new order.

# %%
# Sort the "Name" Series alphabetically
babynames["Name"].sort().head(5)

# %% [markdown]
# ::: {warning}
# `.sort()` places null values **first**, ahead of every real value, in both sort directions. A `.head()` or a positional slice taken straight after a sort will therefore pick up missing values and push out the rows you were after. Nothing about that is an error, so nothing announces it. Pass `nulls_last=True` whenever a sort feeds a `.head()`, a `.tail()`, or a slice, unless you already know the column holds no nulls — as is the case for both datasets in this chapter.
# :::
#
# `babynames` has no missing values, so the small table below has one instead.

# %%
demo = pl.DataFrame({"Name": ["Aaliyah", "Bao", "Cyrus"], "Count": [3, None, 1]})
demo.sort("Count", descending=True)

# %% [markdown]
# Sorting from highest to lowest put the missing count at the top. `nulls_last=True` sends it to the bottom, where it stays out of the way of a `.head()`.

# %%
demo.sort("Count", descending=True, nulls_last=True)

# %% [markdown]
# ## Custom Sorts
#
# Now, let's try to solve a sorting problem using different approaches. Assume we want to find the longest baby names and sort our data accordingly.
#
# ### Approach 1: Create a Temporary Column
#
# One method to do this is to first start by creating a column that contains the lengths of the names.

# %%
# Create a Series of the length of each name
babyname_lengths = babynames["Name"].str.len_chars()

# Add a column named "name_lengths" that includes the length of each name
babynames = babynames.with_columns(name_lengths=babyname_lengths)
babynames.head(5)

# %% [markdown]
# We can then sort the `DataFrame` by that column using `.sort()`:

# %%
# Sort by the temporary column
babynames = babynames.sort(by="name_lengths", descending=True)
babynames.head(5)

# %% [markdown]
# The longest names in the dataset run to 15 characters. Finally, we can drop the `name_lengths` column from `babynames` to prevent our table from getting cluttered.

# %%
# Drop the "name_lengths" column
babynames = babynames.drop("name_lengths")
babynames.head(5)

# %% [markdown]
# ### Approach 2: Sorting on an Expression
#
# Another way to approach this is to hand `.sort()` an expression instead of a column name. The sort key is then computed on the way in, so there is no temporary column to create and no temporary column to drop.

# %%
babynames.sort(pl.col("Name").str.len_chars(), descending=True).head()

# %% [markdown]
# ### Approach 3: Sorting with `map_elements`
#
# We can also use `map_elements` [(documentation)](https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.map_elements.html) if we want to sort by an arbitrarily defined Python function. Say we want to sort the `babynames` table by the number of `"dr"`s and `"ea"`s in each `"Name"`. We'll define the function `dr_ea_count` to help us out.
#
# `map_elements` hands each value of the column to that function, one value at a time, and collects the results. `return_dtype` tells Polars what type those results will have.

# %%
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

# %% [markdown]
# Because it runs Python code once per row, `map_elements` is much slower than the expression in Approach 2, which Polars evaluates on the whole column at once. Save it for the cases where nothing in the expression API will do the job.
#
# We can drop `dr_ea_count` once we're done using it to maintain a neat table.

# %%
# Drop the "dr_ea_count" column
babynames = babynames.drop("dr_ea_count")
babynames.head(5)

# %% [markdown]
# ## Parting Note
#
# The Polars library is enormous and contains many useful functions. Here is a link to its [documentation](https://docs.pola.rs/api/python/stable/reference/index.html). We certainly don't expect you to memorize each and every method of the library, and we will give you a reference sheet for exams.
#
# Manipulating `DataFrame`s is not a skill that is mastered in just one day. The three custom sorts above all answer the same question, and none of them is the "real" one; trying several routes from point A to point B is how the syntax stops feeling arbitrary.
#
# A goal of this course is to help you build your familiarity with the real-world programming practice of ... Googling! Answers to your questions can be found in documentation, Stack Overflow, and elsewhere. Being able to search for, read, and implement documentation is an important life skill for any data scientist.
#
# Next, we will start digging deeper into the mechanics behind grouping data.
