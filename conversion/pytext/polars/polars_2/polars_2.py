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

# %% id="p2-agg-unsorted"
babynames.group_by("Year").agg(pl.col("Count").sum()).head(5)

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

# %% id="p2-agg-sorted"
babies_by_year = babynames.group_by("Year").agg(pl.col("Count").sum()).sort("Year")
babies_by_year.head(5)

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

# %% id="p2-agg-min"
# What is the minimum count for each name in any year?
babynames.group_by("Name").agg(pl.col("Count").min()).sort("Name").head()

# %% [markdown] id="p2-agg-multiple"
# One `.agg` call can carry as many expressions as we like, and `.alias` [(documentation)](https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.alias.html) gives each result a name. Without it, three aggregations of `Count` would all want to be called `Count`.

# %% id="p2-agg-multiple-code"
babynames.group_by("Name").agg(
    pl.col("Count").min().alias("Min Count"),
    pl.col("Count").max().alias("Max Count"),
    pl.col("Count").mean().alias("Mean Count"),
    pl.len().alias("Years Recorded"),
).sort("Name").head()

# %% [markdown] id="p2-first-last"
# The name "Aaden" is a good illustration of what these four numbers buy us: it appears in 14 different years, with counts ranging from 10 to 158.
#
# `.first()` and `.last()` are a little different from the rest, because they select a value rather than compute one. They are what we want when every row of a group carries the same value in some column, and we want that value carried through to the output. To see this, let's add a column to `babynames` holding the first letter of each name.
#
# ```{image} images/first.png
# :alt: Grouped sub-tables reduced to one row each by taking the first entry of a column.
# :width: 500
# ```

# %% id="p2-first-letter"
# Imagine we had an additional column, "First Letter". We'll explain string methods like this one in a later chapter
babynames_new = babynames.with_columns(
    pl.col("Name").str.slice(0, 1).alias("First Letter")
).select(["Name", "First Letter", "Year"])

babynames_new.head()

# %% [markdown] id="p2-first-letter-explain"
# If we form one group per name, `"First Letter"` is identical for every row of the group. Taking the first entry therefore represents the whole group faithfully, while a different column can be aggregated a different way in the same call.

# %% id="p2-first-letter-agg"
babynames_new.group_by("Name").agg(
    pl.col("First Letter").first(),
    pl.col("Year").max(),
).sort("Name").head()

# %% [markdown] id="p2-count-intro"
# ### Counting Rows in Each Group
#
# Often the question is simply how many rows fall into each group. `.len()` answers it directly, with no column to name. Let's work with a small `DataFrame` where we can see every row at once.

# %% id="p2-count-df"
df = pl.DataFrame({"letter": ["A", "A", "B", "C", "C", "C"],
                   "num": [1, 2, 3, 4, None, 4],
                   "state": [None, "tx", "fl", "hi", None, "ak"]})
df

# %% [markdown] id="p2-count-nulls"
# Three of these entries are missing. Polars prints a missing value as `null`, and prints it in place rather than dropping the row.

# %% id="p2-count-len"
df.group_by("letter", maintain_order=True).len()

# %% [markdown] id="p2-count-len-explain"
# We get one row per group: the `letter` we grouped by, alongside a `len` column giving the number of rows in that group. Missing values are counted like any other row, so `C` has three. Because we asked for `maintain_order=True`, the letters arrive in the order they first appear in `df`.
#
# A related question is how much data each column actually holds. `pl.all()` stands for every column we did not group by, and `.count()` counts the values that are not missing.

# %% id="p2-count-all"
df.group_by("letter", maintain_order=True).agg(pl.all().count())

# %% [markdown] id="p2-count-vs-value-counts"
# These counts differ from `.len()`, and from each other. Group `C` occupies three rows but carries only two recorded numbers and two recorded states, and group `A` occupies two rows but carries only one recorded state.
#
# You may recall `.value_counts()` [(documentation)](https://docs.pola.rs/api/python/stable/reference/series/api/polars.Series.value_counts.html) from the previous chapter. It reports the same tallies as `.group_by().len()`.

# %% id="p2-value-counts"
df["letter"].value_counts(sort=True)

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

# %% id="p2-f-babynames"
f_babynames = babynames.filter(pl.col("Sex") == "F").sort("Year")
f_babynames.head()

# %% [markdown] id="p2-jennifer-intro"
# Now we can pull out the counts for "Jennifer" and compare the most recent one to the largest.

# %% id="p2-jennifer"
# The number of Jennifers born in CA in each year, oldest first
jenn_counts = f_babynames.filter(pl.col("Name") == "Jennifer")["Count"]

max_jenn = jenn_counts.max()      # the most Jennifers born in any one year
latest_jenn = jenn_counts.last()  # the most recent year's count

latest_jenn / max_jenn

# %% [markdown] id="p2-jennifer-explain"
# At its peak, 6,065 Jennifers were born in a single year; in 2022 there were 114, giving an RTP of about 0.019. Note how much work the sort is doing here: `.last()` means "the final row", and it is only the most recent year because we sorted `f_babynames` by `Year` first.
#
# The whole calculation is one expression, so we can hand it to `.agg` and get an answer for every name at once. Rows keep their relative order inside a group, so `pl.col("Count").last()` picks out the most recent year for each name.

# %% id="p2-rtp-table"
rtp_table = f_babynames.group_by("Name").agg(
    (pl.col("Count").last() / pl.col("Count").max()).alias("Count RTP")
)
rtp_table.sort("Name").head()

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

# %% id="p2-map-batches"
def ratio_to_peak(series):
    """Ratio of the most recent count to the largest count."""
    return series.last() / series.max()

f_babynames.group_by("Name").agg(
    pl.col("Count")
      .map_batches(ratio_to_peak, return_dtype=pl.Float64, returns_scalar=True)
      .alias("Count RTP")
).sort("Count RTP").head()

# %% [markdown] id="p2-map-caveat"
# Same names, same numbers. The difference is in what runs: the expression version computes all 13,782 ratios in one pass through the data, while this version calls a Python function 13,782 times. Its per-value counterpart, `.map_elements` [(documentation)](https://docs.pola.rs/api/python/stable/reference/expressions/api/polars.Expr.map_elements.html), calls Python once per *value* and is slower still — when it can see an expression that would do the same job, Polars raises a `PolarsInefficientMapWarning` telling you which one. Write the expression when you can, and keep these two for the functions that are not yours to rewrite.
#
# ### Some Data Science Payoff
#
# Sorting `rtp_table` finally answers our question: which names have fallen the furthest?

# %% id="p2-rtp-sorted"
rtp_table.sort("Count RTP").head()

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

# %% id="p2-top10"
top10 = rtp_table.sort("Count RTP").head(10)["Name"].to_list()
top10

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

# %% id="p2-over-small"
df.filter(pl.len().over("letter") >= 2)

# %% [markdown] id="p2-over-elections"
# `B` occurs once, so its row is gone; the two `A` rows and all three `C` rows survive, in their original order.
#
# Now for a real question. We want to identify "tight" election years — years in which no candidate won more than 45% of the popular vote — and see every candidate who ran in them. For each year we need the maximum `%` across all of that year's rows, and then we keep the rows whose year passed the test.

# %% id="p2-over-elections-code"
elections.filter(pl.col("%").max().over("Year") < 45).head(9)

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

# %% id="p2-puzzle-attempt1"
# Sorting by Party gives us the same ten parties on every run
elections.group_by("Party").max().sort("Party").head(10)

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

# %% id="p2-puzzle-sorted"
elections_sorted_by_percent = elections.sort("%", descending=True)
elections_sorted_by_percent.head(5)

# %% id="p2-puzzle-attempt2"
best_per_party = elections_sorted_by_percent.group_by("Party", maintain_order=True).head(1)
best_per_party.head(10)

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

# %% id="p2-puzzle-alt1a"
best_positions = (
    elections.with_row_index("position")
    .group_by("Party")
    .agg(pl.col("position").get(pl.col("%").arg_max()))
    .sort("Party")
)
best_positions.head()

# %% [markdown] id="p2-puzzle-alt1b"
# `arg_max` gives the position *within the group* of the largest `%`, and `.get` reads the entry sitting at that position in `position`. Those numbers are positions in the original table, so we can select the rows directly.

# %% id="p2-puzzle-alt1c"
elections[best_positions["position"]].sort("Party").head()

# %% [markdown] id="p2-puzzle-alt2-intro"
# The second alternative does not group at all. `.unique` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.unique.html) keeps one row per party, and `keep="last"` decides which one — so sorting by `%` in ascending order first leaves each party's best election as the one that survives.

# %% id="p2-puzzle-alt2"
best_per_party2 = elections.sort("%").unique(subset=["Party"], keep="last", maintain_order=True)
best_per_party2.sort("Party").head()

# %% [markdown] id="p2-groupby-objects"
# *Challenge:* see if you can find a third approach that gives the same answer.
#
# ### `GroupBy` Objects
#
# We have called `.agg`, `.len`, `.max`, and `.head` on the result of `.group_by`, so it is worth a closer look at what that result actually is.

# %% id="p2-groupby-type"
grouped_by_party = elections.group_by("Party")
type(grouped_by_party)

# %% [markdown] id="p2-groupby-dict-intro"
# It is a `GroupBy` [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/group_by.html), not a `DataFrame` and not a list of them. It records the table and the keys, and computes nothing until we ask it for something.
#
# What it will do is iterate: stepping through a `GroupBy` yields each group's key alongside the rows belonging to it. That makes it easy to turn into a dictionary.

# %% id="p2-groupby-dict"
groups = dict(grouped_by_party)
sorted(groups.keys())[:6]

# %% [markdown] id="p2-groupby-lookup"
# The keys are the groups and the values are the rows belonging to each. Every key arrives as a tuple, because we are allowed to group by several columns at once. Looking one up gives us back an ordinary `DataFrame`.

# %% id="p2-groupby-socialist"
groups[("Socialist",)]

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

# %% id="p2-groupby-multi"
babynames.group_by(["Year", "Sex"]).agg(pl.col("Count").sum()).sort(["Year", "Sex"]).head(6)

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

# %% id="p2-pivot"
babynames.pivot(
    index="Year",             # one row per year
    on="Sex",                 # the values of Sex become column names
    values="Count",           # what fills the cells
    aggregate_function="sum", # how to combine the rows that land in one cell
).head(5)

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

# %% id="p2-pivot-multi"
babynames.pivot(
    index="Year",
    on="Sex",
    values=["Count", "Name"],
    aggregate_function="max",
).head(6)

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

# %% id="p2-first-name"
# Split each candidate's full name on the blank space, then keep the first piece
elections = elections.with_columns(
    pl.col("Candidate").str.split(" ").list.get(0).alias("First Name")
)
elections.head(5)

# %% id="p2-babynames-2022"
# Here, we'll only consider `babynames` data from 2022
babynames_2022 = babynames.filter(pl.col("Year") == 2022)
babynames_2022.head()

# %% [markdown] id="p2-join-intro"
# Now we're ready to combine them. As in Data 8, this operation is called a **join**: the left table calls the method, and the right table is its first argument [(documentation)](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.join.html).

# %% id="p2-join"
merged = elections.join(
    babynames_2022,
    left_on="First Name",
    right_on="Name",
    maintain_order="left",
)
merged.head()

# %% id="p2-join-cols"
# The full column list, since the table above is too wide to show it
merged.columns

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

# %% id="p2-join-anti"
elections.join(babynames_2022, left_on="First Name", right_on="Name", how="anti", maintain_order="left").head()

# %% [markdown] id="p2-parting"
# Forty rows, headed by Winfield Scott and Millard Fillmore. Since `semi` and `anti` joins answer a question about the left table rather than combining two of them, they return the left table's columns only — there is nothing from `babynames_2022` in this output.
#
# ## Parting Note
#
# Congratulations! We have now covered the core of Polars. Don't worry if you are still not feeling very comfortable with it — you will have plenty of chances to practice over the next few weeks, and the [user guide](https://docs.pola.rs/user-guide/expressions/aggregation/) shows these same operations written a few more ways.
#
# Next, we will get our hands dirty with some real-world datasets and use what we know to conduct some exploratory data analysis.
