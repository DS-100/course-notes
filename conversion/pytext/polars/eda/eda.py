# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: data100
#     language: python
#     name: python3
# ---

# %% [markdown] id="eaf0f4a9"
# ---
# title: Data Cleaning and EDA
# ---
#
# ::: {note} Learning Outcomes
# * Recognize common file formats
# * Categorize data by its variable type
# * Build awareness of issues with data faithfulness and develop targeted solutions
# :::
#
# In the past few lectures, we've learned that `polars` is a toolkit to restructure, modify, and explore a dataset. What we haven't yet touched on is *how* to make these data transformation decisions. When we receive a new set of data from the "real world," how do we know what processing we should do to convert this data into a usable form?
#
# **Data cleaning**, also called **data wrangling**, is the process of transforming raw data to facilitate subsequent analysis. It is often used to address issues like:
#
# * Unclear structure or formatting
# * Missing or corrupted values
# * Unit conversions
# * ...and so on
#
# **Exploratory Data Analysis (EDA)** is the process of understanding a new dataset. It is an open-ended, informal analysis that involves familiarizing ourselves with the variables present in the data, discovering potential hypotheses, and identifying possible issues with the data. This last point can often motivate further data cleaning to address any problems with the dataset's format; because of this, EDA and data cleaning are often thought of as an "infinite loop," with each process driving the other.
#
# In this lecture, we will consider the key properties of data to consider when performing data cleaning and EDA. In doing so, we'll develop a "checklist" of sorts for you to consider when approaching a new dataset. Throughout this process, we'll build a deeper understanding of this early (but very important!) stage of the data science lifecycle.

# %% tags=["remove-cell"] id="aa145d32"
import numpy as np
import polars as pl

import matplotlib.pyplot as plt
import seaborn as sns
# #%matplotlib inline
plt.rcParams['figure.figsize'] = (12, 9)

sns.set()
sns.set_context('talk')
np.set_printoptions(threshold=20, precision=2, suppress=True)
pl.Config.set_tbl_rows(30)
pl.Config.set_tbl_cols(-1)
# Two decimal places, which also keeps wide-ranging columns out of scientific notation
pl.Config.set_float_precision(2)

# Silence some spurious seaborn warnings
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# %% [markdown] id="76d58b2d"
# ## Structure
# We often prefer rectangular data for data analysis. Rectangular structures are easy to manipulate and analyze. A key element of data cleaning is about transforming data to be more rectangular. 
#
# There are two kinds of rectangular data: tables and matrices. Tables have named columns with different data types and are manipulated using data transformation languages. Matrices contain numeric data of the same type and are manipulated using linear algebra.
#
# ### File Formats
# There are many file types for storing structured data: TSV, JSON, XML, ASCII, SAS, etc. We'll only cover CSV, TSV, and JSON in lecture, but you'll likely encounter other formats as you work with different datasets. Reading documentation is your best bet for understanding how to process the multitude of different file types. 
#
# #### CSV
# CSVs, which stand for **Comma-Separated Values**, are a common tabular data format. 
# In the past two `polars` lectures, we briefly touched on the idea of file format: the way data is encoded in a file for storage. Specifically, our `elections` and `babynames` datasets were stored and loaded as CSVs:

# %% tags=["remove-input", "remove-output"] id="09b0a2b7"
pl.read_csv("data/elections.csv").head(5)

# %% [markdown]
# <!-- tab-twins:begin 09b0a2b7 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# pl.read_csv("data/elections.csv").head(5)
# ```
#
# ```text
# shape: (5, 6)
# ┌──────┬───────────────────┬───────────────────────┬──────────────┬────────┬───────┐
# │ Year ┆ Candidate         ┆ Party                 ┆ Popular vote ┆ Result ┆ %     │
# │ ---  ┆ ---               ┆ ---                   ┆ ---          ┆ ---    ┆ ---   │
# │ i64  ┆ str               ┆ str                   ┆ i64          ┆ str    ┆ f64   │
# ╞══════╪═══════════════════╪═══════════════════════╪══════════════╪════════╪═══════╡
# │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republican ┆ 151271       ┆ loss   ┆ 57.21 │
# │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican ┆ 113142       ┆ win    ┆ 42.79 │
# │ 1828 ┆ Andrew Jackson    ┆ Democratic            ┆ 642806       ┆ win    ┆ 56.20 │
# │ 1828 ┆ John Quincy Adams ┆ National Republican   ┆ 500897       ┆ loss   ┆ 43.80 │
# │ 1832 ┆ Andrew Jackson    ┆ Democratic            ┆ 702735       ┆ win    ┆ 54.57 │
# └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# pd.read_csv("data/elections.csv").head(5)
# ```
#
# ```text
#    Year          Candidate                  Party  Popular vote Result     %
# 0  1824     Andrew Jackson  Democratic-Republican        151271   loss 57.21
# 1  1824  John Quincy Adams  Democratic-Republican        113142    win 42.79
# 2  1828     Andrew Jackson             Democratic        642806    win 56.20
# 3  1828  John Quincy Adams    National Republican        500897   loss 43.80
# 4  1832     Andrew Jackson             Democratic        702735    win 54.57
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="c56545cb"
# To better understand the properties of a CSV, let's take a look at the first few rows of the raw data file to see what it looks like before being loaded into a `DataFrame`. We'll use the `repr()` function to return the raw string with its special characters:

# %% id="c6b69895"
with open("data/elections.csv", "r") as table:
    i = 0
    for row in table:
        print(repr(row))
        i += 1
        if i > 3:
            break

# %% [markdown] id="6d40d36a"
# Each row, or **record**, in the data is delimited by a newline `\n`. Each column, or **field**, in the data is delimited by a comma `,` (hence, comma-separated!). 
#
# #### TSV
#
# Another common file type is **TSV (Tab-Separated Values)**. In a TSV, records are still delimited by a newline `\n`, while fields are delimited by `\t` tab character. 
#
# Let's check out the first few rows of the raw TSV file. Again, we'll use the `repr()` function so that `print` shows the special characters.

# %% id="36a18efc"
with open("data/elections.txt", "r") as table:
    i = 0
    for row in table:
        print(repr(row))
        i += 1
        if i > 3:
            break

# %% [markdown] id="386ee625"
# TSVs can be loaded into `polars` using `pl.read_csv`. We'll need to specify the **delimiter** with the parameter `separator='\t'` [(documentation)](https://docs.pola.rs/api/python/stable/reference/api/polars.read_csv.html).

# %% tags=["remove-input", "remove-output"] id="5960d328"
pl.read_csv("data/elections.txt", separator='\t').head(3)

# %% [markdown]
# <!-- tab-twins:begin 5960d328 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# pl.read_csv("data/elections.txt", separator='\t').head(3)
# ```
#
# ```text
# shape: (3, 6)
# ┌──────┬───────────────────┬───────────────────────┬──────────────┬────────┬───────┐
# │ Year ┆ Candidate         ┆ Party                 ┆ Popular vote ┆ Result ┆ %     │
# │ ---  ┆ ---               ┆ ---                   ┆ ---          ┆ ---    ┆ ---   │
# │ i64  ┆ str               ┆ str                   ┆ i64          ┆ str    ┆ f64   │
# ╞══════╪═══════════════════╪═══════════════════════╪══════════════╪════════╪═══════╡
# │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republican ┆ 151271       ┆ loss   ┆ 57.21 │
# │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican ┆ 113142       ┆ win    ┆ 42.79 │
# │ 1828 ┆ Andrew Jackson    ┆ Democratic            ┆ 642806       ┆ win    ┆ 56.20 │
# └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# pd.read_csv("data/elections.txt", sep='\t').head(3)
# ```
#
# ```text
#    Year          Candidate                  Party  Popular vote Result     %
# 0  1824     Andrew Jackson  Democratic-Republican        151271   loss 57.21
# 1  1824  John Quincy Adams  Democratic-Republican        113142    win 42.79
# 2  1828     Andrew Jackson             Democratic        642806    win 56.20
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="3f30f357"
# An issue with CSVs and TSVs comes up whenever there are commas or tabs within the records. How does `polars` differentiate between a comma delimiter vs. a comma within the field itself, for example `8,900`? To remedy this, check out the `quote_char` [parameter](https://docs.pola.rs/api/python/stable/reference/api/polars.read_csv.html). 
#
# #### JSON
# **JSON (JavaScript Object Notation)** files behave similarly to Python dictionaries. A raw JSON is shown below.

# %% id="6fc79ef1"
with open("data/elections.json", "r") as table:
    i = 0
    for row in table:
        print(row)
        i += 1
        if i > 8:
            break

# %% [markdown] id="6694209e"
# JSON files can be loaded into `polars` using `pl.read_json`.

# %% tags=["remove-input", "remove-output"] id="ee261cc8"
pl.read_json('data/elections.json').head(3)

# %% [markdown]
# <!-- tab-twins:begin ee261cc8 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# pl.read_json('data/elections.json').head(3)
# ```
#
# ```text
# shape: (3, 6)
# ┌──────┬───────────────────┬───────────────────────┬──────────────┬────────┬───────┐
# │ Year ┆ Candidate         ┆ Party                 ┆ Popular vote ┆ Result ┆ %     │
# │ ---  ┆ ---               ┆ ---                   ┆ ---          ┆ ---    ┆ ---   │
# │ i64  ┆ str               ┆ str                   ┆ i64          ┆ str    ┆ f64   │
# ╞══════╪═══════════════════╪═══════════════════════╪══════════════╪════════╪═══════╡
# │ 1824 ┆ Andrew Jackson    ┆ Democratic-Republican ┆ 151271       ┆ loss   ┆ 57.21 │
# │ 1824 ┆ John Quincy Adams ┆ Democratic-Republican ┆ 113142       ┆ win    ┆ 42.79 │
# │ 1828 ┆ Andrew Jackson    ┆ Democratic            ┆ 642806       ┆ win    ┆ 56.20 │
# └──────┴───────────────────┴───────────────────────┴──────────────┴────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# pd.read_json('data/elections.json').head(3)
# ```
#
# ```text
#    Year          Candidate                  Party  Popular vote Result     %
# 0  1824     Andrew Jackson  Democratic-Republican        151271   loss 57.21
# 1  1824  John Quincy Adams  Democratic-Republican        113142    win 42.79
# 2  1828     Andrew Jackson             Democratic        642806    win 56.20
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="02fabe1e"
# ##### EDA with JSON: United States Congress Data
# The congress.gov API (Application Programming Interface) provides data about the activities and members of the United States Congress (i.e., the House of Representatives and the Senate). 
#
# To get a JSON file containing information about the current members of Congress from California, you could use the following **API call**:
#
# - `https://api.congress.gov/v3/member/CA?api_key=[INSERT_KEY]&limit=250&format=json&currentMember=True`
#
# - You can instantly sign up for a congress.gov **API key** [here](https://gpo.congress.gov/sign-up/). Once you have your key, replace `[INSERT_KEY]` above with your key, and enter the API call as a URL in your browser. What happens? 
#
# - Once the JSON from the API call is visible in your browser, you can click `File` --> `Save Page As` to save the JSON file to your coputer.
#
# - Coarsely, API keys are used to track how much a given user engages with the API. There might be limits to the number of API calls (e.g., congress.gov API limits to 5,000 calls per hour), or a cost for API calls (e.g., using the OpenAI API for programmatically using ChatGPT).
#
# After following these steps, we save this JSON file as `data/ca-congress-members.json`. 
#
# ###### File Contents
# Let's examine this file using Python. We can programmatically view the first couple lines of the file using the same functions we used with CSVs:

# %% id="59b4e04c"
congress_file = "data/ca-congress-members.json"

# Inspect the first five lines of the file
with open(congress_file, "r") as f:
    for i, row in enumerate(f):
        print(row)
        if i >= 4: break

# %% [markdown] id="fabee18d"
# ###### EDA: Digging into JSON with Python
#
# JSON data closely matches the internal Python object model.  
#
# - In the following cell, we import the entire JSON datafile into a Python dictionary using the `json` package.

# %% id="1fa7f5d3"
import json

# Import the JSON file into Python as a dictionary
with open(congress_file, "rb") as f:
    congress_json = json.load(f)

type(congress_json)

# %% [markdown] id="bae51894"
# The `congress_json` variable is a dictionary encoding the data in the JSON file.
#
# Below, we access the first element of the `members` element of the `congress_json` dictionary.
#
# - This first element is also a dictionary (and there are more dictionaries inside of it!)

# %% id="a90fe774"
# Grab the list corresponding to the `members` key in the JSON dictionary, 
# and then grab the first element of this list.
# In a moment, we'll see how we knew to use the key `members`, and that
# the resulting object is a list.
congress_json['members'][0]

# %% [markdown] id="86c5cdf0"
# How should we probe a nested dictionary like `congress_json`?
#
# We can start by identifying the top-level **keys** of the dictionary:

# %% id="d04088ce"
# Grab the top-level keys of the JSON dictionary
congress_json.keys()

# %% [markdown] id="dcc0be09"
# Looks like we have three top-level keys: `members`, `pagination`, and `request`.
#
# > You'll often see a top-level `meta` key in JSON files. This does not refer to Meta (formerly Facebook). Instead, it typically refers to metadata (data about the data).  Metadata are often maintained alongside the data.
#
# Let's check the type of the `members` element:

# %% id="5aa9a55b"
type(congress_json['members'])

# %% [markdown] id="65f6827d"
# Looks like a list! What are the first two elements?

# %% id="0ae19078"
congress_json['members'][:2]

# %% [markdown] id="e438f962"
# More dictionaries! You can repeat the process above to traverse the nested dictionary.
#
# You'll notice that each record of `congress_json['members']` looks like it could be a column of a DataFrame.
#
# - The keys look a lot like column names, and the values could be the entries in each row.
#
# But, the two other elements of `congress_json` don't have the same structure as `congress_json['members']`.
#
# - So, they probably don't belong in a DataFrame containing the members of Congress from CA.
#
# - We'll see the implications of this inconsistency in the next section.

# %% id="9b09278b"
print(congress_json['pagination'])
print(congress_json['request'])

# %% [markdown] id="6763f4ba"
# ###### JSON with polars
#
# `polars` reads a JSON file with `pl.read_json` ([documentation](https://docs.pola.rs/api/python/stable/reference/api/polars.read_json.html)). Let's point it at the congress file and see what comes back.

# %% tags=["remove-input", "remove-output"] id="a3fde967"
pl.read_json(congress_file)

# %% [markdown]
# <!-- tab-twins:begin a3fde967 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# pl.read_json(congress_file)
# ```
#
# ```text
# shape: (1, 3)
# ┌─────────────────────────────────┬────────────┬─────────────────────────────┐
# │ members                         ┆ pagination ┆ request                     │
# │ ---                             ┆ ---        ┆ ---                         │
# │ list[struct[9]]                 ┆ struct[1]  ┆ struct[2]                   │
# ╞═════════════════════════════════╪════════════╪═════════════════════════════╡
# │ [{"T000491",{"Image courtesy o… ┆ {54}       ┆ {"application/json","json"} │
# └─────────────────────────────────┴────────────┴─────────────────────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # This line intentionally produces an error
# pd.read_json(congress_file)
# ```
#
# ```text
# ValueError: Mixing dicts with non-Series may lead to ambiguous ordering.
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="d00042a9"
# One row, three columns. `pl.read_json` rectangularized the whole object, so `pagination` and `request` became columns sitting beside `members`, and all 54 members were packed into a single cell as a list of structs.
#
# That is not the granularity we want. A row should be one member of Congress, not one API response. The three top-level keys are an artifact of how the service wrapped its reply, and only `members` holds the records we came for.
#
# (`polars` also offers `pl.read_ndjson` ([documentation](https://docs.pola.rs/api/python/stable/reference/api/polars.read_ndjson.html)) for **newline-delimited** JSON, where every line of the file is one complete record. This file is not in that format, but it is a common way for a service to return records and worth knowing about.)
#
# Let's build the DataFrame from the `members` element directly, using `pl.DataFrame`:

# %% tags=["remove-input", "remove-output"] id="870f3938"
# Convert dictionary to DataFrame
congress_df = pl.DataFrame(congress_json['members'])
congress_df.head()

# %% [markdown]
# <!-- tab-twins:begin 870f3938 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Convert dictionary to DataFrame
# congress_df = pl.DataFrame(congress_json['members'])
# congress_df.head()
# ```
#
# ```text
# shape: (5, 9)
# ┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
# │ bioguide ┆ depictio ┆ district ┆ name     ┆ partyNam ┆ state    ┆ terms    ┆ updateDa ┆ url      │
# │ Id       ┆ n        ┆ ---      ┆ ---      ┆ e        ┆ ---      ┆ ---      ┆ te       ┆ ---      │
# │ ---      ┆ ---      ┆ i64      ┆ str      ┆ ---      ┆ str      ┆ struct[1 ┆ ---      ┆ str      │
# │ str      ┆ struct[2 ┆          ┆          ┆ str      ┆          ┆ ]        ┆ str      ┆          │
# │          ┆ ]        ┆          ┆          ┆          ┆          ┆          ┆          ┆          │
# ╞══════════╪══════════╪══════════╪══════════╪══════════╪══════════╪══════════╪══════════╪══════════╡
# │ T000491  ┆ {"Image  ┆ 45       ┆ Tran,    ┆ Democrat ┆ Californ ┆ {[{"Hous ┆ 2025-01- ┆ https:// │
# │          ┆ courtesy ┆          ┆ Derek    ┆ ic       ┆ ia       ┆ e of Rep ┆ 21T18:00 ┆ api.cong │
# │          ┆ of the   ┆          ┆          ┆          ┆          ┆ resentat ┆ :52Z     ┆ ress.gov │
# │          ┆ Member…  ┆          ┆          ┆          ┆          ┆ ives",…  ┆          ┆ /v3/me…  │
# │ M001241  ┆ {"Image  ┆ 47       ┆ Min,     ┆ Democrat ┆ Californ ┆ {[{"Hous ┆ 2025-01- ┆ https:// │
# │          ┆ courtesy ┆          ┆ Dave     ┆ ic       ┆ ia       ┆ e of Rep ┆ 21T18:00 ┆ api.cong │
# │          ┆ of the   ┆          ┆          ┆          ┆          ┆ resentat ┆ :52Z     ┆ ress.gov │
# │          ┆ Member…  ┆          ┆          ┆          ┆          ┆ ives",…  ┆          ┆ /v3/me…  │
# │ K000400  ┆ {"Image  ┆ 37       ┆ Kamlager ┆ Democrat ┆ Californ ┆ {[{"Hous ┆ 2025-01- ┆ https:// │
# │          ┆ courtesy ┆          ┆ -Dove,   ┆ ic       ┆ ia       ┆ e of Rep ┆ 21T18:00 ┆ api.cong │
# │          ┆ of the   ┆          ┆ Sydney   ┆          ┆          ┆ resentat ┆ :52Z     ┆ ress.gov │
# │          ┆ Member…  ┆          ┆          ┆          ┆          ┆ ives",…  ┆          ┆ /v3/me…  │
# │ G000598  ┆ {"Image  ┆ 42       ┆ Garcia,  ┆ Democrat ┆ Californ ┆ {[{"Hous ┆ 2025-01- ┆ https:// │
# │          ┆ courtesy ┆          ┆ Robert   ┆ ic       ┆ ia       ┆ e of Rep ┆ 21T18:00 ┆ api.cong │
# │          ┆ of the   ┆          ┆          ┆          ┆          ┆ resentat ┆ :52Z     ┆ ress.gov │
# │          ┆ Member…  ┆          ┆          ┆          ┆          ┆ ives",…  ┆          ┆ /v3/me…  │
# │ K000397  ┆ {"Image  ┆ 40       ┆ Kim,     ┆ Republic ┆ Californ ┆ {[{"Hous ┆ 2025-01- ┆ https:// │
# │          ┆ courtesy ┆          ┆ Young    ┆ an       ┆ ia       ┆ e of Rep ┆ 21T18:00 ┆ api.cong │
# │          ┆ of the   ┆          ┆          ┆          ┆          ┆ resentat ┆ :52Z     ┆ ress.gov │
# │          ┆ Member…  ┆          ┆          ┆          ┆          ┆ ives",…  ┆          ┆ /v3/me…  │
# └──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # Convert dictionary to DataFrame
# congress_df = pd.DataFrame(congress_json['members'])
# congress_df.head()
# ```
#
# ```text
#   bioguideId                                          depiction  district  \
# 0    T000491  {'attribution': 'Image courtesy of the Member'...     45.00
# 1    M001241  {'attribution': 'Image courtesy of the Member'...     47.00
# 2    K000400  {'attribution': 'Image courtesy of the Member'...     37.00
# 3    G000598  {'attribution': 'Image courtesy of the Member'...     42.00
# 4    K000397  {'attribution': 'Image courtesy of the Member'...     40.00
#
#                     name   partyName       state  \
# 0            Tran, Derek  Democratic  California
# 1              Min, Dave  Democratic  California
# 2  Kamlager-Dove, Sydney  Democratic  California
# 3         Garcia, Robert  Democratic  California
# 4             Kim, Young  Republican  California
#
#                                                terms            updateDate  \
# 0  {'item': [{'chamber': 'House of Representative...  2025-01-21T18:00:52Z
# 1  {'item': [{'chamber': 'House of Representative...  2025-01-21T18:00:52Z
# 2  {'item': [{'chamber': 'House of Representative...  2025-01-21T18:00:52Z
# 3  {'item': [{'chamber': 'House of Representative...  2025-01-21T18:00:52Z
# 4  {'item': [{'chamber': 'House of Representative...  2025-01-21T18:00:52Z
#
#                                                  url
# 0  https://api.congress.gov/v3/member/T000491?for...
# 1  https://api.congress.gov/v3/member/M001241?for...
# 2  https://api.congress.gov/v3/member/K000400?for...
# 3  https://api.congress.gov/v3/member/G000598?for...
# 4  https://api.congress.gov/v3/member/K000397?for...
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="3160c1c1"
# We've successfully begun to rectangularize our JSON data!
#
# Notice the `depiction` and `terms` columns. Both fields were dictionaries inside each record, so `polars` stores them as **struct** columns: a column whose values carry named fields of their own, reached through the `.struct` namespace.
#
# ### Other Data Formats
#
# So far, we've looked at text data that comes in a quite nice format. Although some data cleaning might be necessary, it has still had all of the components of a rectangular dataset. However, not all data comes like this, and there are also different kinds of data we can use. Some examples include:
#
# * **Image Data**: Used for medical diagnosis
# * **Audio Data**: Used for speech recognition, sentiment analysis
# * **Video Data**: Used for object tracking, facial recognition
# * **Text**: Used for LLMs, document review
#
# Even though this may not look tabular at first, all of these formats can be represented in tabular/matrix form! So by learning how to work with tabular data, you are well equipped to deal with other kinds of data as well.
#
# ### Variable Types
# Variables are columns. A variable is a measurement of a particular concept. Variables have two common properties: data type/storage type and variable type/feature type. The data type of a variable indicates how each variable value is stored in memory (integer, floating point, boolean, etc.) and affects which `polars` functions are used. The variable type is a conceptualized measurement of information (and therefore indicates what values a variable can take on). Variable type is identified through expert knowledge, exploring the data itself, or consulting the data codebook. The variable type affects how one visualizes and inteprets the data. In this class, "variable types" are conceptual.
#
# After loading data into a file, it's a good idea to take the time to understand what pieces of information are encoded in the dataset. In particular, we want to identify what variable types are present in our data. Broadly speaking, we can categorize variables into one of two overarching types. 
#
# **Quantitative variables** describe some numeric quantity or amount. Some examples include weights, GPA, CO<sub>2</sub> concentrations, someone's age, or the number of siblings they have.
#
# **Qualitative variables**, also known as **categorical variables**, describe data that isn't measuring some quantity or amount. The sub-categories of categorical data are:
#
# * **Ordinal qualitative variables**: categories with ordered levels. Specifically, ordinal variables are those where the difference between levels has no consistent, quantifiable meaning. Some examples include levels of education (high school, undergrad, grad, etc.), income bracket (low, medium, high), or Yelp rating. 
# * **Nominal qualitative variables**: categories with no specific order. For example, someone's political affiliation or Cal ID number.
#
# ```{image} images/variable_types.png
# :alt: Classification of variable types
# :width: 500
# ```
#
# Note that many variables don't sit neatly in just one of these categories. Qualitative variables could have numeric levels, and conversely, quantitative variables could be stored as strings. 
#
# ## Granularity and Temporality
#
# After understanding the structure of the dataset, the next task is to determine what exactly the data represents. We'll do so by considering the data's granularity and temporality.
#
# ### Granularity
# The **granularity** of a dataset is what a single row represents. You can also think of it as the level of detail included in the data. To determine the data's granularity, ask: what does each row in the dataset represent? Fine-grained data contains a high level of detail, with a single row representing a small individual unit. For example, each record may represent one person. Coarse-grained data is encoded such that a single row represents a large individual unit – for example, each record may represent a group of people.
#
# ### Temporality
# The **temporality** of a dataset describes the periodicity over which the data was collected as well as when the data was most recently collected or updated. 
#
# Time and date fields of a dataset could represent a few things:
#
# 1. when the "event" happened
# 2. when the data was collected, or when it was entered into the system
# 3. when the data was copied into the database 
#
# To fully understand the temporality of the data, it also may be necessary to standardize time zones or inspect recurring time-based trends in the data (do patterns recur in 24-hour periods? Over the course of a month? Seasonally?). The convention for standardizing time is the Coordinated Universal Time (UTC), an international time standard measured at 0 degrees latitude that stays consistent throughout the year (no daylight savings). We can represent Berkeley's time zone, Pacific Standard Time (PST), as UTC-7 (with daylight savings). 
#
# #### Temporality with the `polars` `dt` namespace
# Polars groups methods that apply to only one kind of column into **namespaces**: datetime methods live under `.dt`, string methods under `.str`. Let's briefly look at how we can use the `dt` namespace to work with dates/times in a dataset using the dataset you'll see in Lab 3: the Berkeley PD Calls for Service dataset.
#
# ````{dropdown} Click to see the code
# :open: false
# ```
# calls = pl.read_csv("data/Berkeley_PD_-_Calls_for_Service.csv")
# calls.head()
# ```
# ````

# %% tags=["remove-input", "remove-output"] id="2d223315"
calls = pl.read_csv("data/Berkeley_PD_-_Calls_for_Service.csv")
calls.head()

# %% [markdown]
# <!-- tab-twins:begin 2d223315 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# calls = pl.read_csv("data/Berkeley_PD_-_Calls_for_Service.csv")
# calls.head()
# ```
#
# ```text
# shape: (5, 11)
# ┌─────────┬─────────┬────────┬────────┬────────┬───────┬────────┬────────┬────────┬────────┬───────┐
# │ CASENO  ┆ OFFENSE ┆ EVENTD ┆ EVENTT ┆ CVLEGE ┆ CVDOW ┆ InDbDa ┆ Block_ ┆ BLKADD ┆ City   ┆ State │
# │ ---     ┆ ---     ┆ T      ┆ M      ┆ ND     ┆ ---   ┆ te     ┆ Locati ┆ R      ┆ ---    ┆ ---   │
# │ i64     ┆ str     ┆ ---    ┆ ---    ┆ ---    ┆ i64   ┆ ---    ┆ on     ┆ ---    ┆ str    ┆ str   │
# │         ┆         ┆ str    ┆ str    ┆ str    ┆       ┆ str    ┆ ---    ┆ str    ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ str    ┆        ┆        ┆       │
# ╞═════════╪═════════╪════════╪════════╪════════╪═══════╪════════╪════════╪════════╪════════╪═══════╡
# │ 2101429 ┆ THEFT   ┆ 04/01/ ┆ 10:58  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ Berkel ┆ null   ┆ Berkel ┆ CA    │
# │ 6       ┆ MISD.   ┆ 2021   ┆        ┆ Y      ┆       ┆ 2021   ┆ ey, CA ┆        ┆ ey     ┆       │
# │         ┆ (UNDER  ┆ 12:00: ┆        ┆        ┆       ┆ 12:00: ┆ (37.86 ┆        ┆        ┆       │
# │         ┆ $950)   ┆ 00 AM  ┆        ┆        ┆       ┆ 00 AM  ┆ 9058,  ┆        ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ -122.… ┆        ┆        ┆       │
# │ 2101439 ┆ THEFT   ┆ 04/01/ ┆ 10:38  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ Berkel ┆ null   ┆ Berkel ┆ CA    │
# │ 1       ┆ MISD.   ┆ 2021   ┆        ┆ Y      ┆       ┆ 2021   ┆ ey, CA ┆        ┆ ey     ┆       │
# │         ┆ (UNDER  ┆ 12:00: ┆        ┆        ┆       ┆ 12:00: ┆ (37.86 ┆        ┆        ┆       │
# │         ┆ $950)   ┆ 00 AM  ┆        ┆        ┆       ┆ 00 AM  ┆ 9058,  ┆        ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ -122.… ┆        ┆        ┆       │
# │ 2109049 ┆ THEFT   ┆ 04/19/ ┆ 12:15  ┆ LARCEN ┆ 1     ┆ 06/15/ ┆ 2100   ┆ 2100   ┆ Berkel ┆ CA    │
# │ 4       ┆ MISD.   ┆ 2021   ┆        ┆ Y      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
# │         ┆ (UNDER  ┆ 12:00: ┆        ┆        ┆       ┆ 12:00: ┆ HASTE  ┆ HASTE  ┆        ┆       │
# │         ┆ $950)   ┆ 00 AM  ┆        ┆        ┆       ┆ 00 AM  ┆ ST     ┆ ST     ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey, …  ┆        ┆        ┆       │
# │ 2109020 ┆ THEFT   ┆ 02/13/ ┆ 17:00  ┆ LARCEN ┆ 6     ┆ 06/15/ ┆ 2600   ┆ 2600   ┆ Berkel ┆ CA    │
# │ 4       ┆ FELONY  ┆ 2021   ┆        ┆ Y      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
# │         ┆ (OVER   ┆ 12:00: ┆        ┆        ┆       ┆ 12:00: ┆ WARRIN ┆ WARRIN ┆        ┆       │
# │         ┆ $950)   ┆ 00 AM  ┆        ┆        ┆       ┆ 00 AM  ┆ G ST   ┆ G ST   ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey…    ┆        ┆        ┆       │
# │ 2109017 ┆ BURGLAR ┆ 02/08/ ┆ 6:20   ┆ BURGLA ┆ 1     ┆ 06/15/ ┆ 2700   ┆ 2700   ┆ Berkel ┆ CA    │
# │ 9       ┆ Y AUTO  ┆ 2021   ┆        ┆ RY -   ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
# │         ┆         ┆ 12:00: ┆        ┆ VEHICL ┆       ┆ 12:00: ┆ GARBER ┆ GARBER ┆        ┆       │
# │         ┆         ┆ 00 AM  ┆        ┆ E      ┆       ┆ 00 AM  ┆ ST     ┆ ST     ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey,…   ┆        ┆        ┆       │
# └─────────┴─────────┴────────┴────────┴────────┴───────┴────────┴────────┴────────┴────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# calls = pd.read_csv("data/Berkeley_PD_-_Calls_for_Service.csv")
# calls.head()
# ```
#
# ```text
#      CASENO                   OFFENSE                 EVENTDT EVENTTM  \
# 0  21014296  THEFT MISD. (UNDER $950)  04/01/2021 12:00:00 AM   10:58
# 1  21014391  THEFT MISD. (UNDER $950)  04/01/2021 12:00:00 AM   10:38
# 2  21090494  THEFT MISD. (UNDER $950)  04/19/2021 12:00:00 AM   12:15
# 3  21090204  THEFT FELONY (OVER $950)  02/13/2021 12:00:00 AM   17:00
# 4  21090179             BURGLARY AUTO  02/08/2021 12:00:00 AM    6:20
#
#              CVLEGEND  CVDOW                InDbDate  \
# 0             LARCENY      4  06/15/2021 12:00:00 AM
# 1             LARCENY      4  06/15/2021 12:00:00 AM
# 2             LARCENY      1  06/15/2021 12:00:00 AM
# 3             LARCENY      6  06/15/2021 12:00:00 AM
# 4  BURGLARY - VEHICLE      1  06/15/2021 12:00:00 AM
#
#                                       Block_Location                BLKADDR  \
# 0           Berkeley, CA\r\n(37.869058, -122.270455)                    NaN
# 1           Berkeley, CA\r\n(37.869058, -122.270455)                    NaN
# 2  2100 BLOCK HASTE ST\r\nBerkeley, CA\r\n(37.864...    2100 BLOCK HASTE ST
# 3  2600 BLOCK WARRING ST\r\nBerkeley, CA\r\n(37.8...  2600 BLOCK WARRING ST
# 4  2700 BLOCK GARBER ST\r\nBerkeley, CA\r\n(37.86...   2700 BLOCK GARBER ST
#
#        City State
# 0  Berkeley    CA
# 1  Berkeley    CA
# 2  Berkeley    CA
# 3  Berkeley    CA
# 4  Berkeley    CA
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="9c3a98a3"
# Looks like there are three columns with dates/times: `EVENTDT`, `EVENTTM`, and `InDbDate`. 
#
# Most likely, `EVENTDT` stands for the date when the event took place, `EVENTTM` stands for the time of day the event took place (in 24-hr format), and `InDbDate` is the date this call is recorded onto the database.
#
# If we check the data type of these columns, we will see they are stored as strings. We can convert them to `Datetime` values with the `.str.to_datetime()` method, giving it a format string that describes how the date was written.

# %% tags=["remove-input", "remove-output"] id="7bdeda96"
calls = calls.with_columns(
    pl.col("EVENTDT").str.to_datetime("%m/%d/%Y %I:%M:%S %p")
)
calls.head()

# %% [markdown]
# <!-- tab-twins:begin 7bdeda96 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# calls = calls.with_columns(
#     pl.col("EVENTDT").str.to_datetime("%m/%d/%Y %I:%M:%S %p")
# )
# calls.head()
# ```
#
# ```text
# shape: (5, 11)
# ┌─────────┬─────────┬────────┬────────┬────────┬───────┬────────┬────────┬────────┬────────┬───────┐
# │ CASENO  ┆ OFFENSE ┆ EVENTD ┆ EVENTT ┆ CVLEGE ┆ CVDOW ┆ InDbDa ┆ Block_ ┆ BLKADD ┆ City   ┆ State │
# │ ---     ┆ ---     ┆ T      ┆ M      ┆ ND     ┆ ---   ┆ te     ┆ Locati ┆ R      ┆ ---    ┆ ---   │
# │ i64     ┆ str     ┆ ---    ┆ ---    ┆ ---    ┆ i64   ┆ ---    ┆ on     ┆ ---    ┆ str    ┆ str   │
# │         ┆         ┆ dateti ┆ str    ┆ str    ┆       ┆ str    ┆ ---    ┆ str    ┆        ┆       │
# │         ┆         ┆ me[μs] ┆        ┆        ┆       ┆        ┆ str    ┆        ┆        ┆       │
# ╞═════════╪═════════╪════════╪════════╪════════╪═══════╪════════╪════════╪════════╪════════╪═══════╡
# │ 2101429 ┆ THEFT   ┆ 2021-0 ┆ 10:58  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ Berkel ┆ null   ┆ Berkel ┆ CA    │
# │ 6       ┆ MISD.   ┆ 4-01   ┆        ┆ Y      ┆       ┆ 2021   ┆ ey, CA ┆        ┆ ey     ┆       │
# │         ┆ (UNDER  ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ (37.86 ┆        ┆        ┆       │
# │         ┆ $950)   ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ 9058,  ┆        ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ -122.… ┆        ┆        ┆       │
# │ 2101439 ┆ THEFT   ┆ 2021-0 ┆ 10:38  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ Berkel ┆ null   ┆ Berkel ┆ CA    │
# │ 1       ┆ MISD.   ┆ 4-01   ┆        ┆ Y      ┆       ┆ 2021   ┆ ey, CA ┆        ┆ ey     ┆       │
# │         ┆ (UNDER  ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ (37.86 ┆        ┆        ┆       │
# │         ┆ $950)   ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ 9058,  ┆        ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ -122.… ┆        ┆        ┆       │
# │ 2109049 ┆ THEFT   ┆ 2021-0 ┆ 12:15  ┆ LARCEN ┆ 1     ┆ 06/15/ ┆ 2100   ┆ 2100   ┆ Berkel ┆ CA    │
# │ 4       ┆ MISD.   ┆ 4-19   ┆        ┆ Y      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
# │         ┆ (UNDER  ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ HASTE  ┆ HASTE  ┆        ┆       │
# │         ┆ $950)   ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ ST     ┆ ST     ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey, …  ┆        ┆        ┆       │
# │ 2109020 ┆ THEFT   ┆ 2021-0 ┆ 17:00  ┆ LARCEN ┆ 6     ┆ 06/15/ ┆ 2600   ┆ 2600   ┆ Berkel ┆ CA    │
# │ 4       ┆ FELONY  ┆ 2-13   ┆        ┆ Y      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
# │         ┆ (OVER   ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ WARRIN ┆ WARRIN ┆        ┆       │
# │         ┆ $950)   ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ G ST   ┆ G ST   ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey…    ┆        ┆        ┆       │
# │ 2109017 ┆ BURGLAR ┆ 2021-0 ┆ 6:20   ┆ BURGLA ┆ 1     ┆ 06/15/ ┆ 2700   ┆ 2700   ┆ Berkel ┆ CA    │
# │ 9       ┆ Y AUTO  ┆ 2-08   ┆        ┆ RY -   ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
# │         ┆         ┆ 00:00: ┆        ┆ VEHICL ┆       ┆ 12:00: ┆ GARBER ┆ GARBER ┆        ┆       │
# │         ┆         ┆ 00     ┆        ┆ E      ┆       ┆ 00 AM  ┆ ST     ┆ ST     ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey,…   ┆        ┆        ┆       │
# └─────────┴─────────┴────────┴────────┴────────┴───────┴────────┴────────┴────────┴────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# calls["EVENTDT"] = pd.to_datetime(calls["EVENTDT"])
# calls.head()
# ```
#
# ```text
#      CASENO                   OFFENSE    EVENTDT EVENTTM            CVLEGEND  \
# 0  21014296  THEFT MISD. (UNDER $950) 2021-04-01   10:58             LARCENY
# 1  21014391  THEFT MISD. (UNDER $950) 2021-04-01   10:38             LARCENY
# 2  21090494  THEFT MISD. (UNDER $950) 2021-04-19   12:15             LARCENY
# 3  21090204  THEFT FELONY (OVER $950) 2021-02-13   17:00             LARCENY
# 4  21090179             BURGLARY AUTO 2021-02-08    6:20  BURGLARY - VEHICLE
#
#    CVDOW                InDbDate  \
# 0      4  06/15/2021 12:00:00 AM
# 1      4  06/15/2021 12:00:00 AM
# 2      1  06/15/2021 12:00:00 AM
# 3      6  06/15/2021 12:00:00 AM
# 4      1  06/15/2021 12:00:00 AM
#
#                                       Block_Location                BLKADDR  \
# 0           Berkeley, CA\r\n(37.869058, -122.270455)                    NaN
# 1           Berkeley, CA\r\n(37.869058, -122.270455)                    NaN
# 2  2100 BLOCK HASTE ST\r\nBerkeley, CA\r\n(37.864...    2100 BLOCK HASTE ST
# 3  2600 BLOCK WARRING ST\r\nBerkeley, CA\r\n(37.8...  2600 BLOCK WARRING ST
# 4  2700 BLOCK GARBER ST\r\nBerkeley, CA\r\n(37.86...   2700 BLOCK GARBER ST
#
#        City State
# 0  Berkeley    CA
# 1  Berkeley    CA
# 2  Berkeley    CA
# 3  Berkeley    CA
# 4  Berkeley    CA
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="4092a9cf"
# Now, we can use the `dt` namespace on this column.
#
# We can get the month:

# %% tags=["remove-input", "remove-output"] id="b505d05e"
calls["EVENTDT"].dt.month().head()

# %% [markdown]
# <!-- tab-twins:begin b505d05e -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# calls["EVENTDT"].dt.month().head()
# ```
#
# ```text
# shape: (10,)
# Series: 'EVENTDT' [i8]
# [
# 	4
# 	4
# 	4
# 	2
# 	2
# 	12
# 	5
# 	3
# 	3
# 	3
# ]
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# calls["EVENTDT"].dt.month.head()
# ```
#
# ```text
# 0    4
# 1    4
# 2    4
# 3    2
# 4    2
# Name: EVENTDT, dtype: int32
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="4e135f62"
# Which day of the week the date is on. `dt.weekday()` numbers the days Monday = 1 through Sunday = 7:

# %% id="b432c276"
calls["EVENTDT"].dt.weekday().head()

# %% [markdown] id="e599bfcc"
# Check the minimum values to see if there are any suspicious-looking, 70s dates:

# %% tags=["remove-input", "remove-output"] id="a113c785"
calls.sort("EVENTDT").head()

# %% [markdown]
# <!-- tab-twins:begin a113c785 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# calls.sort("EVENTDT").head()
# ```
#
# ```text
# shape: (5, 11)
# ┌─────────┬─────────┬────────┬────────┬────────┬───────┬────────┬────────┬────────┬────────┬───────┐
# │ CASENO  ┆ OFFENSE ┆ EVENTD ┆ EVENTT ┆ CVLEGE ┆ CVDOW ┆ InDbDa ┆ Block_ ┆ BLKADD ┆ City   ┆ State │
# │ ---     ┆ ---     ┆ T      ┆ M      ┆ ND     ┆ ---   ┆ te     ┆ Locati ┆ R      ┆ ---    ┆ ---   │
# │ i64     ┆ str     ┆ ---    ┆ ---    ┆ ---    ┆ i64   ┆ ---    ┆ on     ┆ ---    ┆ str    ┆ str   │
# │         ┆         ┆ dateti ┆ str    ┆ str    ┆       ┆ str    ┆ ---    ┆ str    ┆        ┆       │
# │         ┆         ┆ me[μs] ┆        ┆        ┆       ┆        ┆ str    ┆        ┆        ┆       │
# ╞═════════╪═════════╪════════╪════════╪════════╪═══════╪════════╪════════╪════════╪════════╪═══════╡
# │ 2009221 ┆ THEFT   ┆ 2020-1 ┆ 18:30  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ 800    ┆ 800    ┆ Berkel ┆ CA    │
# │ 4       ┆ FROM    ┆ 2-17   ┆        ┆ Y -    ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
# │         ┆ AUTO    ┆ 00:00: ┆        ┆ FROM   ┆       ┆ 12:00: ┆ SHATTU ┆ SHATTU ┆        ┆       │
# │         ┆         ┆ 00     ┆        ┆ VEHICL ┆       ┆ 00 AM  ┆ CK AVE ┆ CK AVE ┆        ┆       │
# │         ┆         ┆        ┆        ┆ E      ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ e…     ┆        ┆        ┆       │
# │ 2005737 ┆ GUN/WEA ┆ 2020-1 ┆ 22:18  ┆ WEAPON ┆ 4     ┆ 06/15/ ┆ 6200   ┆ 6200   ┆ Berkel ┆ CA    │
# │ 3       ┆ PON     ┆ 2-17   ┆        ┆ S OFFE ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
# │         ┆         ┆ 00:00: ┆        ┆ NSE    ┆       ┆ 12:00: ┆ SAN    ┆ SAN    ┆        ┆       │
# │         ┆         ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ PABLO  ┆ PABLO  ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ AVE    ┆ AVE    ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berke… ┆        ┆        ┆       │
# │ 2005720 ┆ ASSAULT ┆ 2020-1 ┆ 16:50  ┆ ASSAUL ┆ 4     ┆ 06/15/ ┆ 2100   ┆ 2100   ┆ Berkel ┆ CA    │
# │ 7       ┆ /BATTER ┆ 2-17   ┆        ┆ T      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
# │         ┆ Y MISD. ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ SHATTU ┆ SHATTU ┆        ┆       │
# │         ┆         ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ CK AVE ┆ CK AVE ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ …      ┆        ┆        ┆       │
# │ 2005732 ┆ THEFT   ┆ 2020-1 ┆ 15:44  ┆ LARCEN ┆ 4     ┆ 06/15/ ┆ 1800   ┆ 1800   ┆ Berkel ┆ CA    │
# │ 4       ┆ MISD.   ┆ 2-17   ┆        ┆ Y      ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
# │         ┆ (UNDER  ┆ 00:00: ┆        ┆        ┆       ┆ 12:00: ┆ 4TH ST ┆ 4TH ST ┆        ┆       │
# │         ┆ $950)   ┆ 00     ┆        ┆        ┆       ┆ 00 AM  ┆ Berkel ┆        ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey,    ┆        ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ CA…    ┆        ┆        ┆       │
# │ 2005757 ┆ BURGLAR ┆ 2020-1 ┆ 22:15  ┆ BURGLA ┆ 4     ┆ 06/15/ ┆ 1700   ┆ 1700   ┆ Berkel ┆ CA    │
# │ 3       ┆ Y RESID ┆ 2-17   ┆        ┆ RY -   ┆       ┆ 2021   ┆ BLOCK  ┆ BLOCK  ┆ ey     ┆       │
# │         ┆ ENTIAL  ┆ 00:00: ┆        ┆ RESIDE ┆       ┆ 12:00: ┆ STUART ┆ STUART ┆        ┆       │
# │         ┆         ┆ 00     ┆        ┆ NTIAL  ┆       ┆ 00 AM  ┆ ST     ┆ ST     ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ Berkel ┆        ┆        ┆       │
# │         ┆         ┆        ┆        ┆        ┆       ┆        ┆ ey,…   ┆        ┆        ┆       │
# └─────────┴─────────┴────────┴────────┴────────┴───────┴────────┴────────┴────────┴────────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# calls.sort_values("EVENTDT").head()
# ```
#
# ```text
#         CASENO                   OFFENSE    EVENTDT EVENTTM  \
# 2513  20057398       BURGLARY COMMERCIAL 2020-12-17   16:05
# 624   20057207     ASSAULT/BATTERY MISD. 2020-12-17   16:50
# 154   20092214           THEFT FROM AUTO 2020-12-17   18:30
# 659   20057324  THEFT MISD. (UNDER $950) 2020-12-17   15:44
# 993   20057573      BURGLARY RESIDENTIAL 2020-12-17   22:15
#
#                     CVLEGEND  CVDOW                InDbDate  \
# 2513   BURGLARY - COMMERCIAL      4  06/15/2021 12:00:00 AM
# 624                  ASSAULT      4  06/15/2021 12:00:00 AM
# 154   LARCENY - FROM VEHICLE      4  06/15/2021 12:00:00 AM
# 659                  LARCENY      4  06/15/2021 12:00:00 AM
# 993   BURGLARY - RESIDENTIAL      4  06/15/2021 12:00:00 AM
#
#                                          Block_Location  \
# 2513  600 BLOCK GILMAN ST\r\nBerkeley, CA\r\n(37.878...
# 624   2100 BLOCK SHATTUCK AVE\r\nBerkeley, CA\r\n(37...
# 154   800 BLOCK SHATTUCK AVE\r\nBerkeley, CA\r\n(37....
# 659   1800 BLOCK 4TH ST\r\nBerkeley, CA\r\n(37.86988...
# 993   1700 BLOCK STUART ST\r\nBerkeley, CA\r\n(37.85...
#
#                       BLKADDR      City State
# 2513      600 BLOCK GILMAN ST  Berkeley    CA
# 624   2100 BLOCK SHATTUCK AVE  Berkeley    CA
# 154    800 BLOCK SHATTUCK AVE  Berkeley    CA
# 659         1800 BLOCK 4TH ST  Berkeley    CA
# 993      1700 BLOCK STUART ST  Berkeley    CA
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="106b48ee"
# Doesn't look like it! We are good!
#
# We can also do many things with the `dt` namespace like switching time zones and converting time back to UNIX/POSIX time. Check out the documentation on the [`dt` namespace](https://docs.pola.rs/api/python/stable/reference/expressions/temporal.html) and on [parsing and transforming time series](https://docs.pola.rs/user-guide/transformations/time-series/parsing/).
#
# ## Faithfulness
#
# At this stage in our data cleaning and EDA workflow, we've achieved quite a lot: we've identified how our data is structured, come to terms with what information it encodes, and gained insight as to how it was generated. Throughout this process, we should always recall the original intent of our work in Data Science – to use data to better understand and model the real world. To achieve this goal, we need to ensure that the data we use is faithful to reality; that is, that our data accurately captures the "real world."
#
# Data used in research or industry is often "messy" – there may be errors or inaccuracies that impact the faithfulness of the dataset. Signs that data may not be faithful include:
#
# * Unrealistic or "incorrect" values, such as negative counts, locations that don't exist, or dates set in the future
# * Violations of obvious dependencies, like an age that does not match a birthday
# * Clear signs that data was entered by hand, which can lead to spelling errors or fields that are incorrectly shifted
# * Signs of data falsification, such as fake email addresses or repeated use of the same names
# * Duplicated records or fields containing the same information
# * Truncated data, e.g. Microsoft Excel would limit the number of rows to 655536 and the number of columns to 255
#
# We often solve some of these more common issues in the following ways: 
#
# * Spelling errors: apply corrections or drop records that aren't in a dictionary
# * Time zone inconsistencies: convert to a common time zone (e.g. UTC) 
# * Duplicated records or fields: identify and eliminate duplicates (using primary keys)
# * Unspecified or inconsistent units: infer the units and check that values are in reasonable ranges in the data
#
# ### Missing Values
# Another common issue encountered with real-world datasets is that of missing data. One strategy to resolve this is to simply drop any records with missing values from the dataset. This does, however, introduce the risk of inducing biases – it is possible that the missing or corrupt records may be systemically related to some feature of interest in the data. This is why it's generally good practice to keep missing data, or at least to only drop if it you can be sure the missing data won't introduce some bias. Another solution is to keep the data as `null` values, which is how `polars` marks a value that is absent. A `null` is not the same as a `NaN`: `NaN` is a floating-point value meaning "not a number", which a calculation can produce, while `null` means no value was ever recorded.
#
# A third method to address missing data is to perform **imputation**: infer the missing values using other data available in the dataset. There is a wide variety of imputation techniques that can be implemented; some of the most common are listed below.
#
# * Average imputation: replace missing values with the average value for that field
# * Hot deck imputation: replace missing values with some random value
# * Regression imputation: develop a model to predict missing values and replace with the predicted value from the model.
# * Multiple imputation: replace missing values with multiple random values
#
# Regardless of the strategy used to deal with missing data, we should think carefully about *why* particular records or fields may be missing – this can help inform whether or not the absence of these values is significant or meaningful.
#
# **Note: In Spring 2026, interpolation is out of scope for Data 100.**
#
# ## EDA Demo 1: Flu in the United States
#
# Now, let's walk through the data-cleaning and EDA workflow to see what can we learn about the presence of flu in the United States!
#
# We will examine the data included in the [original CDC database](https://gis.cdc.gov/grasp/fluview/fluportaldashboard.html), which we downloaded in 2026.
#
#
# ### CSVs and Field Names
# Suppose this dataset was saved as a CSV file located in `data/flu/`.
#
# We can then explore the CSV (which is a text file, and does not contain binary-encoded data) in many ways:
# 1. Using a text editor like VSCode, emacs, vim, etc.
# 2. Opening the CSV directly in DataHub (read-only), Excel, Google Sheets, etc.
# 3. The `Python` file object
# 4. `polars`, using `pl.read_csv()`
#
# To try out options 1 and 2, you can view or download the flu data from the [lecture demo notebook](https://data100.datahub.berkeley.edu/hub/user-redirect/git-pull?repo=https%3A%2F%2Fgithub.com%2FDS-100%2Fsp26-student&branch=main&urlpath=lab%2Ftree%2Fsp26-student%2Flec%2Flec05%2Flec05-part-1-eda-tuberculosis.ipynb) under the `data` folder in the left hand menu. Notice how the CSV file is a type of **rectangular data (i.e., tabular data) stored as comma-separated values**.
#
# Next, let's try out option 3 using the `Python` file object. We'll look at the first four lines:
#
# ````{dropdown} Click to see the code
# :open: false
# ```
# with open("data/flu/ILINet.csv", "r") as f:
#     i = 0
#     for row in f:
#         print(row)
#         i += 1
#         if i > 3:
#             break
# ```
# ````

# %% tags=["remove-input"] id="a64676bd"
with open("data/flu/ILINet.csv", "r") as f:
    i = 0
    for row in f:
        print(row)
        i += 1
        if i > 3:
            break

# %% [markdown] id="074b40c4"
# Whoa, why are there blank lines interspaced between the lines of the CSV?
#
# You may recall that all line breaks in text files are encoded as the special newline character `\n`. Python's `print()` prints each string (including the newline), and an additional newline on top of that.
#
# If you're curious, we can use the `repr()` function to return the raw string with all special characters:
#
# ````{dropdown} Click to see the code
# :open: false
# ```
# with open("data/flu/ILINet.csv", "r") as f:
#     i = 0
#     for row in f:
#         print(repr(row)) # print raw strings
#         i += 1
#         if i > 3:
#             break
# ```
# ````

# %% tags=["remove-input"] id="5cd5eabd"
with open("data/flu/ILINet.csv", "r") as f:
    i = 0
    for row in f:
        print(repr(row)) # print raw strings
        i += 1
        if i > 3:
            break

# %% [markdown] id="40f647f8"
# Finally, let's try option 4 and use the tried-and-true Data 100 approach: `polars`.

# %% tags=["remove-input", "remove-output"] id="35082131"
ili = pl.read_csv("data/flu/ILINet.csv", truncate_ragged_lines=True)
ili

# %% [markdown]
# <!-- tab-twins:begin 35082131 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# ili = pl.read_csv("data/flu/ILINet.csv", truncate_ragged_lines=True)
# ili
# ```
#
# ```text
# shape: (5_381, 1)
# ┌─────────────────────────────────┐
# │ PERCENTAGE OF VISITS FOR INFLU… │
# │ ---                             │
# │ str                             │
# ╞═════════════════════════════════╡
# │ REGION TYPE                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ …                               │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# │ HHS Regions                     │
# └─────────────────────────────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# ili = pd.read_csv("data/flu/ILINet.csv")
# ili
# ```
#
# ```text
#                                                                                                                                                 PERCENTAGE OF VISITS FOR INFLUENZA-LIKE-ILLNESS REPORTED BY SENTINEL PROVIDERS
# REGION TYPE REGION    YEAR WEEK % WEIGHTED ILI %UNWEIGHTED ILI AGE 0-4 AGE 25-49 AGE 25-64 AGE 5-24 AGE 50-64 AGE 65 ILITOTAL NUM. OF PROVIDERS                                     TOTAL PATIENTS
# HHS Regions Region 1  2015 40   0.743302       0.684364        103     50        NaN       133      23        13     322      134                                                            47051
#             Region 2  2015 40   1.03278        1.22475         547     294       NaN       528      123       95     1587     199                                                           129577
#             Region 3  2015 40   1.2178         1.24313         401     419       NaN       625      144       81     1670     280                                                           134338
#             Region 4  2015 40   1.01464        1.15781         486     231       NaN       613      99        75     1504     299                                                           129900
# ...                                                                                                                                                                                            ...
#             Region 6  2026 3    6.71907        6.40685         1189    1313      NaN       2393     451       375    5721     205                                                            89295
#             Region 7  2026 3    5.70345        5.79518         518     722       NaN       1174     228       338    2980     164                                                            51422
#             Region 8  2026 3    3.03915        3.08624         684     670       NaN       1000     246       289    2889     228                                                            93609
#             Region 9  2026 3    4.85718        4.62364         2045    5863      NaN       4914     2552      3004   18378    402                                                           397479
#             Region 10 2026 3    5.06699        4.91184         1462    1946      NaN       3526     700       793    8427     332                                                           171565
#
# [5381 rows x 1 columns]
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="d73890d0"
# You may notice some strange things about this table: why is there only one column, and why is its label a whole sentence?
#
# `pl.read_csv` sizes the table from the first line of the file, and that line is a title with no commas in it. Every record after it carries fifteen fields, so the reader needed `truncate_ragged_lines=True` to get through the file at all, and everything past the first field of each record was thrown away.
#
# Congratulations — you're ready to wrangle your data! Because of how things are stored, we'll need to clean the data a bit to name our columns better.
#
# A reasonable first step is to identify the row with the right header. The `pl.read_csv()` function ([documentation](https://docs.pola.rs/api/python/stable/reference/api/polars.read_csv.html)) has the convenient `skip_rows` parameter, which throws away lines before the header is read. Setting it to 1 discards the title and promotes row 1 to the column names:

# %% tags=["remove-input", "remove-output"] id="ffb961d3"
ili = pl.read_csv("data/flu/ILINet.csv", skip_rows=1) # drop the title line
ili.head(5)

# %% [markdown]
# <!-- tab-twins:begin ffb961d3 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# ili = pl.read_csv("data/flu/ILINet.csv", skip_rows=1) # drop the title line
# ili.head(5)
# ```
#
# ```text
# shape: (5, 15)
# ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬────────┬───────┬───────┬───────┐
# │ REG ┆ REG ┆ YEA ┆ WEE ┆ %   ┆ %UN ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE 65 ┆ ILITO ┆ NUM.  ┆ TOTAL │
# │ ION ┆ ION ┆ R   ┆ K   ┆ WEI ┆ WEI ┆ 0-4 ┆ 25- ┆ 25- ┆ 5-2 ┆ 50- ┆ ---    ┆ TAL   ┆ OF    ┆ PATIE │
# │ TYP ┆ --- ┆ --- ┆ --- ┆ GHT ┆ GHT ┆ --- ┆ 49  ┆ 64  ┆ 4   ┆ 64  ┆ i64    ┆ ---   ┆ PROVI ┆ NTS   │
# │ E   ┆ str ┆ i64 ┆ i64 ┆ ED  ┆ ED  ┆ i64 ┆ --- ┆ --- ┆ --- ┆ --- ┆        ┆ i64   ┆ DERS  ┆ ---   │
# │ --- ┆     ┆     ┆     ┆ ILI ┆ ILI ┆     ┆ i64 ┆ str ┆ i64 ┆ i64 ┆        ┆       ┆ ---   ┆ i64   │
# │ str ┆     ┆     ┆     ┆ --- ┆ --- ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆ i64   ┆       │
# │     ┆     ┆     ┆     ┆ f64 ┆ f64 ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
# ╞═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪════════╪═══════╪═══════╪═══════╡
# │ HHS ┆ Reg ┆ 201 ┆ 40  ┆ 0.7 ┆ 0.6 ┆ 103 ┆ 50  ┆ nul ┆ 133 ┆ 23  ┆ 13     ┆ 322   ┆ 134   ┆ 47051 │
# │ Reg ┆ ion ┆ 5   ┆     ┆ 4   ┆ 8   ┆     ┆     ┆ l   ┆     ┆     ┆        ┆       ┆       ┆       │
# │ ion ┆ 1   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
# │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
# │ HHS ┆ Reg ┆ 201 ┆ 40  ┆ 1.0 ┆ 1.2 ┆ 547 ┆ 294 ┆ nul ┆ 528 ┆ 123 ┆ 95     ┆ 1587  ┆ 199   ┆ 12957 │
# │ Reg ┆ ion ┆ 5   ┆     ┆ 3   ┆ 2   ┆     ┆     ┆ l   ┆     ┆     ┆        ┆       ┆       ┆ 7     │
# │ ion ┆ 2   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
# │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
# │ HHS ┆ Reg ┆ 201 ┆ 40  ┆ 1.2 ┆ 1.2 ┆ 401 ┆ 419 ┆ nul ┆ 625 ┆ 144 ┆ 81     ┆ 1670  ┆ 280   ┆ 13433 │
# │ Reg ┆ ion ┆ 5   ┆     ┆ 2   ┆ 4   ┆     ┆     ┆ l   ┆     ┆     ┆        ┆       ┆       ┆ 8     │
# │ ion ┆ 3   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
# │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
# │ HHS ┆ Reg ┆ 201 ┆ 40  ┆ 1.0 ┆ 1.1 ┆ 486 ┆ 231 ┆ nul ┆ 613 ┆ 99  ┆ 75     ┆ 1504  ┆ 299   ┆ 12990 │
# │ Reg ┆ ion ┆ 5   ┆     ┆ 1   ┆ 6   ┆     ┆     ┆ l   ┆     ┆     ┆        ┆       ┆       ┆ 0     │
# │ ion ┆ 4   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
# │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
# │ HHS ┆ Reg ┆ 201 ┆ 40  ┆ 1.0 ┆ 1.1 ┆ 384 ┆ 238 ┆ nul ┆ 444 ┆ 159 ┆ 103    ┆ 1328  ┆ 284   ┆ 11280 │
# │ Reg ┆ ion ┆ 5   ┆     ┆ 4   ┆ 8   ┆     ┆     ┆ l   ┆     ┆     ┆        ┆       ┆       ┆ 7     │
# │ ion ┆ 5   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
# │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        ┆       ┆       ┆       │
# └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴────────┴───────┴───────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# ili = pd.read_csv("data/flu/ILINet.csv", header=1) # row index
# ili.head(5)
# ```
#
# ```text
#    REGION TYPE    REGION  YEAR  WEEK  % WEIGHTED ILI  %UNWEIGHTED ILI  \
# 0  HHS Regions  Region 1  2015    40            0.74             0.68
# 1  HHS Regions  Region 2  2015    40            1.03             1.22
# 2  HHS Regions  Region 3  2015    40            1.22             1.24
# 3  HHS Regions  Region 4  2015    40            1.01             1.16
# 4  HHS Regions  Region 5  2015    40            1.04             1.18
#
#    AGE 0-4  AGE 25-49  AGE 25-64  AGE 5-24  AGE 50-64  AGE 65  ILITOTAL  \
# 0      103         50        NaN       133         23      13       322
# 1      547        294        NaN       528        123      95      1587
# 2      401        419        NaN       625        144      81      1670
# 3      486        231        NaN       613         99      75      1504
# 4      384        238        NaN       444        159     103      1328
#
#    NUM. OF PROVIDERS  TOTAL PATIENTS
# 0                134           47051
# 1                199          129577
# 2                280          134338
# 3                299          129900
# 4                284          112807
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="2672314f"
# ### Granularity of the records
# After successfully opening the CSV file, we can examine the granularity of each record in our flu dataset. By inspecting the data, we see that each row represents a unique combination of **week**, **year**, and **region**.
#
# Now that we have the data in a DataFrame and understand what each row represents, we can start thinking about **visualizations**: a picture is always worth a thousand words.

# %% [markdown] id="e804c7ac"
# ### Visualization
#
# #### Preprocessing and column manipulation
#
# We know that our data records observations over a period of time and is separated by region, so a line plot is a reasonable choice due to its ability to effectively display trends over time and allow for easy comparison across regions.
#
# However, `YEAR` and `WEEK` are in two separate columns, so we need to combine them into a single date column for the x-axis. Week 1 of a year is the week that begins on its first Monday, and each week is labelled by the Sunday that closes it. `pl.date` builds a date out of year, month and day, and adding a `pl.duration` moves it by whole days. The details of how we construct the date here aren't as important as the end result. This is a great use case for a google search or asking an LLM.

# %% tags=["remove-input", "remove-output"] id="d4403db1"
# Week 1 begins on the first Monday of the year
jan_1 = pl.date(pl.col('YEAR'), 1, 1)
week_1_monday = jan_1 + pl.duration(days=(8 - jan_1.dt.weekday()) % 7)

# Each week is labelled by the Sunday six days after its Monday
ili = ili.with_columns(
    (week_1_monday + pl.duration(days=7 * (pl.col('WEEK') - 1) + 6)).alias('week_start')
)
ili.sample(3)

# %% [markdown]
# <!-- tab-twins:begin d4403db1 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # Week 1 begins on the first Monday of the year
# jan_1 = pl.date(pl.col('YEAR'), 1, 1)
# week_1_monday = jan_1 + pl.duration(days=(8 - jan_1.dt.weekday()) % 7)
#
# # Each week is labelled by the Sunday six days after its Monday
# ili = ili.with_columns(
#     (week_1_monday + pl.duration(days=7 * (pl.col('WEEK') - 1) + 6)).alias('week_start')
# )
# ili.sample(3)
# ```
#
# ```text
# shape: (3, 16)
# ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬────────┐
# │ REG ┆ REG ┆ YEA ┆ WEE ┆ %   ┆ %UN ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ ILI ┆ NUM ┆ TOT ┆ week_s │
# │ ION ┆ ION ┆ R   ┆ K   ┆ WEI ┆ WEI ┆ 0-4 ┆ 25- ┆ 25- ┆ 5-2 ┆ 50- ┆ 65  ┆ TOT ┆ .   ┆ AL  ┆ tart   │
# │ TYP ┆ --- ┆ --- ┆ --- ┆ GHT ┆ GHT ┆ --- ┆ 49  ┆ 64  ┆ 4   ┆ 64  ┆ --- ┆ AL  ┆ OF  ┆ PAT ┆ ---    │
# │ E   ┆ str ┆ i64 ┆ i64 ┆ ED  ┆ ED  ┆ i64 ┆ --- ┆ --- ┆ --- ┆ --- ┆ i64 ┆ --- ┆ PRO ┆ IEN ┆ date   │
# │ --- ┆     ┆     ┆     ┆ ILI ┆ ILI ┆     ┆ i64 ┆ str ┆ i64 ┆ i64 ┆     ┆ i64 ┆ VID ┆ TS  ┆        │
# │ str ┆     ┆     ┆     ┆ --- ┆ --- ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ ERS ┆ --- ┆        │
# │     ┆     ┆     ┆     ┆ f64 ┆ f64 ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ --- ┆ i64 ┆        │
# │     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ i64 ┆     ┆        │
# ╞═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪════════╡
# │ HHS ┆ Reg ┆ 201 ┆ 3   ┆ 2.7 ┆ 3.0 ┆ 392 ┆ 360 ┆ nul ┆ 628 ┆ 222 ┆ 157 ┆ 175 ┆ 141 ┆ 574 ┆ 2018-0 │
# │ Reg ┆ ion ┆ 8   ┆     ┆ 7   ┆ 6   ┆     ┆     ┆ l   ┆     ┆     ┆     ┆ 9   ┆     ┆ 49  ┆ 1-21   │
# │ ion ┆ 8   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
# │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
# │ HHS ┆ Reg ┆ 202 ┆ 49  ┆ 7.3 ┆ 7.2 ┆ 179 ┆ 140 ┆ nul ┆ 287 ┆ 563 ┆ 558 ┆ 719 ┆ 233 ┆ 994 ┆ 2022-1 │
# │ Reg ┆ ion ┆ 2   ┆     ┆ 1   ┆ 4   ┆ 6   ┆ 9   ┆ l   ┆ 3   ┆     ┆     ┆ 9   ┆     ┆ 62  ┆ 2-11   │
# │ ion ┆ 8   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
# │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
# │ HHS ┆ Reg ┆ 202 ┆ 1   ┆ 5.7 ┆ 5.1 ┆ 554 ┆ 110 ┆ nul ┆ 964 ┆ 487 ┆ 593 ┆ 371 ┆ 954 ┆ 720 ┆ 2026-0 │
# │ Reg ┆ ion ┆ 6   ┆     ┆ 2   ┆ 5   ┆ 7   ┆ 95  ┆ l   ┆ 8   ┆ 5   ┆ 7   ┆ 02  ┆     ┆ 870 ┆ 1-11   │
# │ ion ┆ 4   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
# │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆        │
# └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴────────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# ili['week_start'] = pd.to_datetime(
#     (ili['YEAR'] * 100 + ili['WEEK']).astype(str) + '0',
#     format='%Y%W%w'
# )
# ili.sample(3)
# ```
#
# ```text
#       REGION TYPE     REGION  YEAR  WEEK  % WEIGHTED ILI  %UNWEIGHTED ILI  \
# 1856  HHS Regions   Region 7  2019    17            0.99             1.08
# 4421  HHS Regions   Region 2  2024    13            3.51             4.61
# 169   HHS Regions  Region 10  2016     4            1.41             1.50
#
#       AGE 0-4  AGE 25-49  AGE 25-64  AGE 5-24  AGE 50-64  AGE 65  ILITOTAL  \
# 1856      136         43        NaN       106         25      33       343
# 4421     1573       2948        NaN      3310        731     517      9079
# 169        55         37        NaN        92         23       4       211
#
#       NUM. OF PROVIDERS  TOTAL PATIENTS week_start
# 1856                109           31807 2019-05-05
# 4421                245          196943 2024-03-31
# 169                  76           14029 2016-01-31
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="c14c6b2b"
# We can access date components through the `.dt` namespace, for example `.dt.year()` and `.dt.month()`.

# %% tags=["remove-input", "remove-output"] id="e4371cbb"
ili['week_start'].dt.year().head()

# %% [markdown]
# <!-- tab-twins:begin e4371cbb -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# ili['week_start'].dt.year().head()
# ```
#
# ```text
# shape: (10,)
# Series: 'week_start' [i32]
# [
# 	2015
# 	2015
# 	2015
# 	2015
# 	2015
# 	2015
# 	2015
# 	2015
# 	2015
# 	2015
# ]
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# ili['week_start'].dt.year.head()
# ```
#
# ```text
# 0    2015
# 1    2015
# 2    2015
# 3    2015
# 4    2015
# Name: week_start, dtype: int32
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="6e59fe73"
# Here, we can spend some time to look at what is the data type of the new column.

# %% id="ac8c201a"
ili['week_start'].dtype

# %% [markdown] id="2e523f34"
# `Date` is the `polars` type for a calendar date with no time of day attached.
#
# - Its sibling is `Datetime`, which carries a time as well, to microsecond resolution by default
#
# Under the hood, a `Date` is an integer counting the number of **days** since 1/1/1970 UTC, and a `Datetime` counts **microseconds** from that same instant.

# %% [markdown] id="727b5e32"
# #### Plotting
# We will dive deeper into the details of data visualization later, but for now this is a sneak peek at what we will be able to do in the future!

# %% id="7076dee8"
# Visualize number of cases for babies and small children

f, ax = plt.subplots(1, 1, figsize=(12, 7))
sns.lineplot(ili, x='week_start', y='AGE 0-4', hue='REGION', ax=ax);

# %% id="a0939426"
# Visualize overall prevalence of flu
f, ax = plt.subplots(1, 1, figsize=(12, 7))
sns.lineplot(ili, x='week_start', y='% WEIGHTED ILI', hue='REGION', ax=ax);

# %% [markdown] id="9c330b3a"
# Take some time to examine it and consider any interesting observations or questions that arise from the data. We will explore data visualization in much more depth in upcoming lectures.

# %% [markdown] id="ae048ae9"
# ### Load vaccination data
# This DataFrame contains monthly flu vaccination counts for each flu season (starting in July and ending the following June).
#
# Take a close look at the output, and make sure you understand what happens between 2023-06-01 and 2023-07-01!

# %% tags=["remove-input", "remove-output"] id="5f24d68b"
vax = pl.read_csv('data/flu/monthly_child_flu_vaccination.csv')
vax = vax.with_columns(
    pl.col('month_dt').str.to_date(),
    rate=pl.col('Numerator') / pl.col('Population'),
)
vax.head(14)

# %% [markdown]
# <!-- tab-twins:begin 5f24d68b -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# vax = pl.read_csv('data/flu/monthly_child_flu_vaccination.csv')
# vax = vax.with_columns(
#     pl.col('month_dt').str.to_date(),
#     rate=pl.col('Numerator') / pl.col('Population'),
# )
# vax.head(14)
# ```
#
# ```text
# shape: (14, 5)
# ┌────────────┬────────────┬───────────┬────────────┬──────┐
# │ HHS Region ┆ month_dt   ┆ Numerator ┆ Population ┆ rate │
# │ ---        ┆ ---        ┆ ---       ┆ ---        ┆ ---  │
# │ str        ┆ date       ┆ f64       ┆ f64        ┆ f64  │
# ╞════════════╪════════════╪═══════════╪════════════╪══════╡
# │ Region 1   ┆ 2022-07-01 ┆ 17110.00  ┆ 1328581.00 ┆ 0.01 │
# │ Region 1   ┆ 2022-08-01 ┆ 42110.00  ┆ 1328581.00 ┆ 0.03 │
# │ Region 1   ┆ 2022-09-01 ┆ 129698.00 ┆ 1328581.00 ┆ 0.10 │
# │ Region 1   ┆ 2022-10-01 ┆ 297855.00 ┆ 1328581.00 ┆ 0.22 │
# │ Region 1   ┆ 2022-11-01 ┆ 430376.00 ┆ 1328581.00 ┆ 0.32 │
# │ Region 1   ┆ 2022-12-01 ┆ 508781.00 ┆ 1328581.00 ┆ 0.38 │
# │ Region 1   ┆ 2023-01-01 ┆ 545783.00 ┆ 1328581.00 ┆ 0.41 │
# │ Region 1   ┆ 2023-02-01 ┆ 563456.00 ┆ 1328581.00 ┆ 0.42 │
# │ Region 1   ┆ 2023-03-01 ┆ 575885.00 ┆ 1328581.00 ┆ 0.43 │
# │ Region 1   ┆ 2023-04-01 ┆ 581451.00 ┆ 1328581.00 ┆ 0.44 │
# │ Region 1   ┆ 2023-05-01 ┆ 586289.00 ┆ 1328581.00 ┆ 0.44 │
# │ Region 1   ┆ 2023-06-01 ┆ 590354.00 ┆ 1328581.00 ┆ 0.44 │
# │ Region 1   ┆ 2023-07-01 ┆ 10473.00  ┆ 1319459.00 ┆ 0.01 │
# │ Region 1   ┆ 2023-08-01 ┆ 32037.00  ┆ 1319459.00 ┆ 0.02 │
# └────────────┴────────────┴───────────┴────────────┴──────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# vax = pd.read_csv('data/flu/monthly_child_flu_vaccination.csv')
# vax['month_dt'] = pd.to_datetime(vax['month_dt'])
# vax['rate'] = vax['Numerator'] / vax['Population']
# vax.head(14)
# ```
#
# ```text
#    HHS Region   month_dt  Numerator  Population  rate
# 0    Region 1 2022-07-01   17110.00  1328581.00  0.01
# 1    Region 1 2022-08-01   42110.00  1328581.00  0.03
# 2    Region 1 2022-09-01  129698.00  1328581.00  0.10
# 3    Region 1 2022-10-01  297855.00  1328581.00  0.22
# 4    Region 1 2022-11-01  430376.00  1328581.00  0.32
# 5    Region 1 2022-12-01  508781.00  1328581.00  0.38
# 6    Region 1 2023-01-01  545783.00  1328581.00  0.41
# 7    Region 1 2023-02-01  563456.00  1328581.00  0.42
# 8    Region 1 2023-03-01  575885.00  1328581.00  0.43
# 9    Region 1 2023-04-01  581451.00  1328581.00  0.44
# 10   Region 1 2023-05-01  586289.00  1328581.00  0.44
# 11   Region 1 2023-06-01  590354.00  1328581.00  0.44
# 12   Region 1 2023-07-01   10473.00  1319459.00  0.01
# 13   Region 1 2023-08-01   32037.00  1319459.00  0.02
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="2f0f6573"
# ### Joining Data (Combining different `DataFrame`)
# First, let's examine the two `DataFrame` we are joining.

# %% id="dde3d773"
display(ili.tail(2))
display(vax.tail(2))

# %% [markdown] id="0db8ac21"
# This is a natural point to pause and consider how weekly timestamps should be aggregated in order to match the monthly granularity of the vaccination data. In this example, we choose to associate each week with the month in which its closing Sunday falls. This isn't the only way we could do this, and it also isn't perfect: there may be weeks that are split across two months where the numbers won't match up exactly.

# %% id="ac97d064"
ili = ili.with_columns(pl.col("week_start").dt.truncate("1mo").alias("month"))

# %% [markdown] id="2ed26785"
# Time to join! Here we use the `DataFrame` method `df1.join(df2, ...)` on `DataFrame df1` ([documentation](https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.join.html)). `left_on` and `right_on` name the key columns on each side, since the two tables spell them differently, and the default `how='inner'` keeps only the rows that match on both sides. The key columns are folded together, so the joined table carries `month` and `REGION` and does not repeat them under the `vax` names. The user guide walks through the other join strategies ([documentation](https://docs.pola.rs/user-guide/transformations/joins/)).

# %% tags=["remove-input", "remove-output"] id="73402b3c"
ili_vax = ili.join(
    vax,
    left_on=['month', 'REGION'],
    right_on=['month_dt', 'HHS Region']
)
ili_vax.head()

# %% [markdown]
# <!-- tab-twins:begin 73402b3c -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# ili_vax = ili.join(
#     vax,
#     left_on=['month', 'REGION'],
#     right_on=['month_dt', 'HHS Region']
# )
# ili_vax.head()
# ```
#
# ```text
# shape: (5, 20)
# ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
# │ REG ┆ REG ┆ YEA ┆ WEE ┆ %   ┆ %UN ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ AGE ┆ ILI ┆ NUM ┆ TOT ┆ wee ┆ mon ┆ Num ┆ Pop ┆ rat │
# │ ION ┆ ION ┆ R   ┆ K   ┆ WEI ┆ WEI ┆ 0-4 ┆ 25- ┆ 25- ┆ 5-2 ┆ 50- ┆ 65  ┆ TOT ┆ .   ┆ AL  ┆ k_s ┆ th  ┆ era ┆ ula ┆ e   │
# │ TYP ┆ --- ┆ --- ┆ --- ┆ GHT ┆ GHT ┆ --- ┆ 49  ┆ 64  ┆ 4   ┆ 64  ┆ --- ┆ AL  ┆ OF  ┆ PAT ┆ tar ┆ --- ┆ tor ┆ tio ┆ --- │
# │ E   ┆ str ┆ i64 ┆ i64 ┆ ED  ┆ ED  ┆ i64 ┆ --- ┆ --- ┆ --- ┆ --- ┆ i64 ┆ --- ┆ PRO ┆ IEN ┆ t   ┆ dat ┆ --- ┆ n   ┆ f64 │
# │ --- ┆     ┆     ┆     ┆ ILI ┆ ILI ┆     ┆ i64 ┆ str ┆ i64 ┆ i64 ┆     ┆ i64 ┆ VID ┆ TS  ┆ --- ┆ e   ┆ f64 ┆ --- ┆     │
# │ str ┆     ┆     ┆     ┆ --- ┆ --- ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ ERS ┆ --- ┆ dat ┆     ┆     ┆ f64 ┆     │
# │     ┆     ┆     ┆     ┆ f64 ┆ f64 ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ --- ┆ i64 ┆ e   ┆     ┆     ┆     ┆     │
# │     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ i64 ┆     ┆     ┆     ┆     ┆     ┆     │
# ╞═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╡
# │ HHS ┆ Reg ┆ 202 ┆ 26  ┆ 0.9 ┆ 1.0 ┆ 440 ┆ 356 ┆ nul ┆ 346 ┆ 166 ┆ 211 ┆ 151 ┆ 232 ┆ 148 ┆ 202 ┆ 202 ┆ 171 ┆ 132 ┆ 0.0 │
# │ Reg ┆ ion ┆ 2   ┆     ┆ 3   ┆ 2   ┆     ┆     ┆ l   ┆     ┆     ┆     ┆ 9   ┆     ┆ 833 ┆ 2-0 ┆ 2-0 ┆ 10. ┆ 858 ┆ 1   │
# │ ion ┆ 1   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 7-0 ┆ 7-0 ┆ 00  ┆ 1.0 ┆     │
# │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 3   ┆ 1   ┆     ┆ 0   ┆     │
# │ HHS ┆ Reg ┆ 202 ┆ 26  ┆ 2.8 ┆ 2.5 ┆ 175 ┆ 630 ┆ nul ┆ 112 ┆ 278 ┆ 297 ┆ 408 ┆ 161 ┆ 163 ┆ 202 ┆ 202 ┆ 699 ┆ 198 ┆ 0.0 │
# │ Reg ┆ ion ┆ 2   ┆     ┆ 0   ┆ 0   ┆ 6   ┆     ┆ l   ┆ 4   ┆     ┆     ┆ 5   ┆     ┆ 656 ┆ 2-0 ┆ 2-0 ┆ .00 ┆ 200 ┆ 0   │
# │ ion ┆ 2   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 7-0 ┆ 7-0 ┆     ┆ 9.0 ┆     │
# │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 3   ┆ 1   ┆     ┆ 0   ┆     │
# │ HHS ┆ Reg ┆ 202 ┆ 26  ┆ 1.3 ┆ 1.6 ┆ 134 ┆ 883 ┆ nul ┆ 929 ┆ 397 ┆ 360 ┆ 391 ┆ 371 ┆ 240 ┆ 202 ┆ 202 ┆ 284 ┆ 430 ┆ 0.0 │
# │ Reg ┆ ion ┆ 2   ┆     ┆ 9   ┆ 3   ┆ 7   ┆     ┆ l   ┆     ┆     ┆     ┆ 6   ┆     ┆ 707 ┆ 2-0 ┆ 2-0 ┆ .00 ┆ 155 ┆ 0   │
# │ ion ┆ 3   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 7-0 ┆ 7-0 ┆     ┆ 6.0 ┆     │
# │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 3   ┆ 1   ┆     ┆ 0   ┆     │
# │ HHS ┆ Reg ┆ 202 ┆ 26  ┆ 2.2 ┆ 2.4 ┆ 432 ┆ 355 ┆ nul ┆ 343 ┆ 146 ┆ 137 ┆ 141 ┆ 928 ┆ 572 ┆ 202 ┆ 202 ┆ 226 ┆ 132 ┆ 0.0 │
# │ Reg ┆ ion ┆ 2   ┆     ┆ 9   ┆ 7   ┆ 0   ┆ 5   ┆ l   ┆ 0   ┆ 9   ┆ 0   ┆ 44  ┆     ┆ 466 ┆ 2-0 ┆ 2-0 ┆ 8.0 ┆ 032 ┆ 0   │
# │ ion ┆ 4   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 7-0 ┆ 7-0 ┆ 0   ┆ 79. ┆     │
# │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 3   ┆ 1   ┆     ┆ 00  ┆     │
# │ HHS ┆ Reg ┆ 202 ┆ 26  ┆ 1.1 ┆ 1.0 ┆ 100 ┆ 678 ┆ nul ┆ 817 ┆ 331 ┆ 349 ┆ 317 ┆ 610 ┆ 300 ┆ 202 ┆ 202 ┆ 662 ┆ 114 ┆ 0.0 │
# │ Reg ┆ ion ┆ 2   ┆     ┆ 5   ┆ 6   ┆ 1   ┆     ┆ l   ┆     ┆     ┆     ┆ 6   ┆     ┆ 270 ┆ 2-0 ┆ 2-0 ┆ .00 ┆ 925 ┆ 0   │
# │ ion ┆ 5   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 7-0 ┆ 7-0 ┆     ┆ 29. ┆     │
# │ s   ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆     ┆ 3   ┆ 1   ┆     ┆ 00  ┆     │
# └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# ili_vax = ili.merge(
#     vax,
#     left_on=['month', 'REGION'],
#     right_on=['month_dt', 'HHS Region']
# )
# ili_vax.head()
# ```
#
# ```text
#    REGION TYPE    REGION  YEAR  WEEK  % WEIGHTED ILI  %UNWEIGHTED ILI  \
# 0  HHS Regions  Region 1  2022    26            0.93             1.02
# 1  HHS Regions  Region 2  2022    26            2.80             2.50
# 2  HHS Regions  Region 3  2022    26            1.39             1.63
# 3  HHS Regions  Region 4  2022    26            2.29             2.47
# 4  HHS Regions  Region 5  2022    26            1.15             1.06
#
#    AGE 0-4  AGE 25-49  AGE 25-64  AGE 5-24  AGE 50-64  AGE 65  ILITOTAL  \
# 0      440        356        NaN       346        166     211      1519
# 1     1756        630        NaN      1124        278     297      4085
# 2     1347        883        NaN       929        397     360      3916
# 3     4320       3555        NaN      3430       1469    1370     14144
# 4     1001        678        NaN       817        331     349      3176
#
#    NUM. OF PROVIDERS  TOTAL PATIENTS week_start      month HHS Region  \
# 0                232          148833 2022-07-03 2022-07-01   Region 1
# 1                161          163656 2022-07-03 2022-07-01   Region 2
# 2                371          240707 2022-07-03 2022-07-01   Region 3
# 3                928          572466 2022-07-03 2022-07-01   Region 4
# 4                610          300270 2022-07-03 2022-07-01   Region 5
#
#     month_dt  Numerator  Population  rate
# 0 2022-07-01   17110.00  1328581.00  0.01
# 1 2022-07-01     699.00  1982009.00  0.00
# 2 2022-07-01     284.00  4301556.00  0.00
# 3 2022-07-01    2268.00 13203279.00  0.00
# 4 2022-07-01     662.00 11492529.00  0.00
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="9fd43cfe"
# We often join datasets to get a much bigger picture of what’s really happening in the data—and one of the best ways to showcase that bigger picture is through a bigger visualization!

# %% id="e1bde1fb"
f, ax = plt.subplots(1, 1, figsize=(10, 7))
sns.scatterplot(ili_vax, x='ILITOTAL', y='rate', alpha=0.3, hue='REGION', ax=ax);

# %% [markdown] id="7adb9772"
# Hmm, this graph appears to show more information than the line plot we examined earlier, but something seems off. What are some limitations of this graph? We will explore what makes an effective visualization in more detail later.

# %% [markdown] id="c15d88e0"
# ## Summary
# We went over a lot of content this lecture; let's summarize the most important points: 
#
# ### Dealing with Missing Values
# There are a few options we can take to deal with missing data:
#
# * Drop missing records
# * Keep `null` missing values
# * Impute using an interpolated column
#
# ### EDA and Data Wrangling
# There are several ways to approach EDA and Data Wrangling: 
#
# * Examine the **data and metadata**: what is the date, size, organization, and structure of the data? 
# * Examine each **field/attribute/dimension** individually.
# * Examine pairs of related dimensions (e.g. breaking down grades by major).
# * Along the way, we can:
#     * **Visualize** or summarize the data.
#     * **Validate assumptions** about data and its collection process. Pay particular attention to when the data was collected. 
#     * Identify and **address anomalies**.
#     * Apply data transformations and corrections (we'll cover this in the upcoming lecture).
#     * **Record everything you do!** Developing in Jupyter Notebook promotes *reproducibility* of your own work!
#
# ## [BONUS] EDA Demo 2: Mauna Loa CO<sub>2</sub> Data – A Lesson in Data Faithfulness
#
# We no longer cover the following demo in lecture, but we provide the following section in the course notes for interested students.
#
# [Mauna Loa Observatory](https://gml.noaa.gov/ccgg/trends/data.html) has been monitoring CO<sub>2</sub> concentrations since 1958.

# %% id="8f10478d"
co2_file = "data/co2_mm_mlo.txt"

# %% [markdown] id="769f72b4"
# Let's do some **EDA**!!
#
# ### Reading this file into `polars`?
# Let's instead check out this `.txt` file. Some questions to keep in mind: Do we trust this file extension? What structure is it? 
#
# Lines 71-78 (inclusive) are shown below: 
#
#     line number |                            file contents
#     
#     71          |   #            decimal     average   interpolated    trend    #days
#     72          |   #             date                             (season corr)
#     73          |   1958   3    1958.208      315.71      315.71      314.62     -1
#     74          |   1958   4    1958.292      317.45      317.45      315.29     -1
#     75          |   1958   5    1958.375      317.50      317.50      314.71     -1
#     76          |   1958   6    1958.458      -99.99      317.10      314.85     -1
#     77          |   1958   7    1958.542      315.86      315.86      314.98     -1
#     78          |   1958   8    1958.625      314.93      314.93      315.94     -1
#
#
# Notice how: 
#
# - The values are separated by white space, possibly tabs.
# - The data line up down the rows. For example, the month appears in 7th to 8th position of each line.
# - The 71st and 72nd lines in the file contain column headings split over two lines.
#
# We can use `pl.read_csv` to read the data into a `polars` `DataFrame`. We provide arguments to specify that there is no header (**we will set our own column names**) and to skip the first 72 rows of the file. There is not a single comma in the data, so every record arrives whole, in one column:

# %% id="719dc1a4"
co2 = pl.read_csv(co2_file, has_header = False, skip_rows = 72)
co2.head()

# %% [markdown] id="96d6fda6"
# Congratulations! You've wrangled the data!
#
# ...But each record is still one long string, and our single column isn't named.
# **We need to do more EDA.**
#
# ### Exploring Variable Feature Types
#
# The NOAA [webpage](https://gml.noaa.gov/ccgg/trends/) might have some useful tidbits (in this case it doesn't).
#
# Using this information, we'll rerun `pl.read_csv`, but this time we'll pull out every run of non-whitespace characters with `.str.extract_all(r'\S+')`, which amounts to splitting each record on its runs of white space. That leaves a list of seven values per row, which `.list.to_struct` labels with some **custom column names** and `.unnest` spreads across seven columns. Every value arrives as text, so we finish by casting each column to the type it should have.

# %% tags=["remove-input", "remove-output"] id="761e3219"
co2 = (
    pl.read_csv(co2_file, has_header = False, skip_rows = 72, new_columns = ['row'])
    .select(
        pl.col('row')
        .str.extract_all(r'\S+') #regex for runs of non-whitespace (next lecture)
        .list.to_struct(fields = ['Yr', 'Mo', 'DecDate', 'Avg', 'Int', 'Trend', 'Days'])
    )
    .unnest('row')
    .cast({'Yr': pl.Int64, 'Mo': pl.Int64, 'DecDate': pl.Float64, 'Avg': pl.Float64,
           'Int': pl.Float64, 'Trend': pl.Float64, 'Days': pl.Int64})
)
co2.head()

# %% [markdown]
# <!-- tab-twins:begin 761e3219 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# co2 = (
#     pl.read_csv(co2_file, has_header = False, skip_rows = 72, new_columns = ['row'])
#     .select(
#         pl.col('row')
#         .str.extract_all(r'\S+') #regex for runs of non-whitespace (next lecture)
#         .list.to_struct(fields = ['Yr', 'Mo', 'DecDate', 'Avg', 'Int', 'Trend', 'Days'])
#     )
#     .unnest('row')
#     .cast({'Yr': pl.Int64, 'Mo': pl.Int64, 'DecDate': pl.Float64, 'Avg': pl.Float64,
#            'Int': pl.Float64, 'Trend': pl.Float64, 'Days': pl.Int64})
# )
# co2.head()
# ```
#
# ```text
# shape: (5, 7)
# ┌──────┬─────┬─────────┬────────┬────────┬────────┬──────┐
# │ Yr   ┆ Mo  ┆ DecDate ┆ Avg    ┆ Int    ┆ Trend  ┆ Days │
# │ ---  ┆ --- ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---  │
# │ i64  ┆ i64 ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ i64  │
# ╞══════╪═════╪═════════╪════════╪════════╪════════╪══════╡
# │ 1958 ┆ 3   ┆ 1958.21 ┆ 315.71 ┆ 315.71 ┆ 314.62 ┆ -1   │
# │ 1958 ┆ 4   ┆ 1958.29 ┆ 317.45 ┆ 317.45 ┆ 315.29 ┆ -1   │
# │ 1958 ┆ 5   ┆ 1958.38 ┆ 317.50 ┆ 317.50 ┆ 314.71 ┆ -1   │
# │ 1958 ┆ 6   ┆ 1958.46 ┆ -99.99 ┆ 317.10 ┆ 314.85 ┆ -1   │
# │ 1958 ┆ 7   ┆ 1958.54 ┆ 315.86 ┆ 315.86 ┆ 314.98 ┆ -1   │
# └──────┴─────┴─────────┴────────┴────────┴────────┴──────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# co2 = pd.read_csv(
#     co2_file, header = None, skiprows = 72,
#     sep = r'\s+', #regex for continuous whitespace (next lecture)
#     names = ['Yr', 'Mo', 'DecDate', 'Avg', 'Int', 'Trend', 'Days']
# )
# co2.head()
# ```
#
# ```text
#      Yr  Mo  DecDate    Avg    Int  Trend  Days
# 0  1958   3  1958.21 315.71 315.71 314.62    -1
# 1  1958   4  1958.29 317.45 317.45 315.29    -1
# 2  1958   5  1958.38 317.50 317.50 314.71    -1
# 3  1958   6  1958.46 -99.99 317.10 314.85    -1
# 4  1958   7  1958.54 315.86 315.86 314.98    -1
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="c0d2bbc8"
# ### Visualizing CO<sub>2</sub>
# Scientific studies tend to have very clean data, right...? Let's jump right in and make a time series plot of CO<sub>2</sub> monthly averages.

# %% id="f3c66483"
#| fig-alt: A lineplot of the monthly averages from 1958 to 2019. The data mostly has a repeating wave pattern and is larger as time goes on. However, there are a number of large dips to -100.
sns.lineplot(x='DecDate', y='Avg', data=co2);

# %% [markdown] id="e8c74e2d"
# The code above uses the `seaborn` plotting library (abbreviated `sns`). We will cover this in the Visualization lecture, but now you don't need to worry about how it works!
#
# Yikes! Plotting the data uncovered a problem. The sharp vertical lines suggest that we have some **missing values**. What happened here?

# %% id="e4bf9b58"
co2.head()

# %% id="4cb81718"
co2.tail()

# %% [markdown] id="5d3a894d"
# Some data have unusual values like -1 and -99.99.
#
# Let's check the description at the top of the file again.
#
# * -1 signifies a missing value for the number of days `Days` the equipment was in operation that month.
# * -99.99 denotes a missing monthly average `Avg`
#
# How can we fix this? First, let's explore other aspects of our data. Understanding our data will help us decide what to do with the missing values.
#
# ### Sanity Checks: Reasoning about the data
# First, we consider the shape of the data. How many rows should we have?
#
# * If chronological order, we should have one record per month.
# * Data from March 1958 to August 2019.
# * We should have $ 12 \times (2019-1957) - 2 - 4 = 738 $ records.

# %% id="6c8a81fd"
co2.shape

# %% [markdown] id="9be1f329"
# Nice!! The number of rows (i.e. records) match our expectations.
#
# Let's now check the quality of each feature.
#
# ### Understanding Missing Value 1: `Days`
# `Days` is a time field, so let's analyze other time fields to see if there is an explanation for missing values of days of operation.
#
# Let's start with **months**, `Mo`.
#
# Are we missing any records? The number of months should have 62 or 61 instances (March 1958-August 2019). `value_counts` returns a two-column table of each value beside how often it appears, which we sort by month:

# %% tags=["remove-input", "remove-output"] id="fb3fcc66"
co2["Mo"].value_counts().sort("Mo")

# %% [markdown]
# <!-- tab-twins:begin fb3fcc66 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# co2["Mo"].value_counts().sort("Mo")
# ```
#
# ```text
# shape: (12, 2)
# ┌─────┬───────┐
# │ Mo  ┆ count │
# │ --- ┆ ---   │
# │ i64 ┆ u32   │
# ╞═════╪═══════╡
# │ 1   ┆ 61    │
# │ 2   ┆ 61    │
# │ 3   ┆ 62    │
# │ 4   ┆ 62    │
# │ 5   ┆ 62    │
# │ 6   ┆ 62    │
# │ 7   ┆ 62    │
# │ 8   ┆ 62    │
# │ 9   ┆ 61    │
# │ 10  ┆ 61    │
# │ 11  ┆ 61    │
# │ 12  ┆ 61    │
# └─────┴───────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# co2["Mo"].value_counts().sort_index()
# ```
#
# ```text
# Mo
# 1     61
# 2     61
# 3     62
# 4     62
# 5     62
# 6     62
# 7     62
# 8     62
# 9     61
# 10    61
# 11    61
# 12    61
# Name: count, dtype: int64
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="ffa70516"
# As expected Jan, Feb, Sep, Oct, Nov, and Dec have 61 occurrences and the rest 62.
#
# Next let's explore **days** `Days` itself, which is the number of days that the measurement equipment worked.
#
# ````{dropdown} Click to see the code
# :open: false
# ```
# #| fig-alt: Plotted distribution of days feature.
# sns.displot(co2, x='Days');
# plt.title("Distribution of days feature"); # suppresses unneeded plotting output
# ```
# ````

# %% tags=["remove-input"] id="6232f59d"
#| fig-alt: Plotted distribution of days feature.
sns.displot(co2, x='Days');
plt.title("Distribution of days feature"); # suppresses unneeded plotting output

# %% [markdown] id="ecf1c3de"
# In terms of data quality, a handful of months have averages based on measurements taken on fewer than half the days. In addition, there are nearly 200 missing values--**that's about 27% of the data**!
#
# Finally, let's check the last time feature, **year** `Yr`.
#
# Let's check to see if there is any connection between missing-ness and the year of the recording.
#
# ````{dropdown} Click to see the code
# :open: false
# ```
# #| fig-alt: Scatterplot where day is plotted against year. The lowest values are seen in the 1960s and 1970s. By 1990, most years have days plotted at 20 or above.
# sns.scatterplot(x="Yr", y="Days", data=co2);
# plt.title("Day field by Year"); # the ; suppresses output
# ```
# ````

# %% tags=["remove-input"] id="baa142a4"
#| fig-alt: Scatterplot where day is plotted against year. The lowest values are seen in the 1960s and 1970s. By 1990, most years have days plotted at 20 or above.
sns.scatterplot(x="Yr", y="Days", data=co2);
plt.title("Day field by Year"); # the ; suppresses output

# %% [markdown] id="b3c4b2bc"
# **Observations**:
#
# * All of the missing data are in the early years of operation.
# * It appears there may have been problems with equipment in the mid to late 80s.
#
# **Potential Next Steps**:
#
# * Confirm these explanations through documentation about the historical readings.
# * Maybe drop the earliest recordings? However, we would want to delay such action until after we have examined the time trends and assess whether there are any potential problems.
#
# ### Understanding Missing Value 2: `Avg`
# Next, let's return to the -99.99 values in `Avg` to analyze the overall quality of the CO<sub>2</sub> measurements. We'll plot a histogram of the average CO<sub>2</sub> measurements
#
# ````{dropdown} Click to see the code
# :open: false
# ```
# #| fig-alt: Histogram of average CO2 measurements. Almost all of the data falls between about 310 and 415 ppm, with the tallest bars in the low 320s. A single isolated bin sits below zero, holding the seven -99.99 missing-value records.
# # Histograms of average CO2 measurements
# sns.displot(co2, x='Avg');
# ```
# ````

# %% tags=["remove-input"] id="20adcbbe"
#| fig-alt: Histogram of average CO2 measurements. Almost all of the data falls between about 310 and 415 ppm, with the tallest bars in the low 320s. A single isolated bin sits below zero, holding the seven -99.99 missing-value records.
# Histograms of average CO2 measurements
sns.displot(co2, x='Avg');

# %% [markdown] id="f7554c29"
# The non-missing values are in the 300-400 range (a regular range of CO<sub>2</sub> levels).
#
# We also see that there are only a few missing `Avg` values (**<1% of values**). Let's examine all of them:

# %% tags=["remove-input", "remove-output"] id="0d87b254"
co2.filter(pl.col("Avg") < 0)

# %% [markdown]
# <!-- tab-twins:begin 0d87b254 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# co2.filter(pl.col("Avg") < 0)
# ```
#
# ```text
# shape: (7, 7)
# ┌──────┬─────┬─────────┬────────┬────────┬────────┬──────┐
# │ Yr   ┆ Mo  ┆ DecDate ┆ Avg    ┆ Int    ┆ Trend  ┆ Days │
# │ ---  ┆ --- ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---  │
# │ i64  ┆ i64 ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ i64  │
# ╞══════╪═════╪═════════╪════════╪════════╪════════╪══════╡
# │ 1958 ┆ 6   ┆ 1958.46 ┆ -99.99 ┆ 317.10 ┆ 314.85 ┆ -1   │
# │ 1958 ┆ 10  ┆ 1958.79 ┆ -99.99 ┆ 312.66 ┆ 315.61 ┆ -1   │
# │ 1964 ┆ 2   ┆ 1964.12 ┆ -99.99 ┆ 320.07 ┆ 319.61 ┆ -1   │
# │ 1964 ┆ 3   ┆ 1964.21 ┆ -99.99 ┆ 320.73 ┆ 319.55 ┆ -1   │
# │ 1964 ┆ 4   ┆ 1964.29 ┆ -99.99 ┆ 321.77 ┆ 319.48 ┆ -1   │
# │ 1975 ┆ 12  ┆ 1975.96 ┆ -99.99 ┆ 330.59 ┆ 331.60 ┆ 0    │
# │ 1984 ┆ 4   ┆ 1984.29 ┆ -99.99 ┆ 346.84 ┆ 344.27 ┆ 2    │
# └──────┴─────┴─────────┴────────┴────────┴────────┴──────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# co2[co2["Avg"] < 0]
# ```
#
# ```text
#        Yr  Mo  DecDate    Avg    Int  Trend  Days
# 3    1958   6  1958.46 -99.99 317.10 314.85    -1
# 7    1958  10  1958.79 -99.99 312.66 315.61    -1
# 71   1964   2  1964.12 -99.99 320.07 319.61    -1
# 72   1964   3  1964.21 -99.99 320.73 319.55    -1
# 73   1964   4  1964.29 -99.99 321.77 319.48    -1
# 213  1975  12  1975.96 -99.99 330.59 331.60     0
# 313  1984   4  1984.29 -99.99 346.84 344.27     2
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="e1150336"
# There doesn't seem to be a pattern to these values, other than that most records also were missing `Days` data.
#
# ### Drop, `null`, or Impute Missing `Avg` Data?
#
# How should we address the invalid `Avg` data?
#
# 1. Drop records
# 2. Set to `null`
# 3. Impute using some strategy
#
# Remember we want to fix the following plot:
#
# ````{dropdown} Click to see the code
# :open: false
# ```
# #| fig-alt: A lineplot of the monthly averages from 1958 to 2019. The data mostly has a repeating wave pattern and is larger as time goes on. However, there are a number of large dips to -100.
# sns.lineplot(x='DecDate', y='Avg', data=co2)
# plt.title("CO2 Average By Month");
# ```
# ````

# %% tags=["remove-input"] id="11056cc5"
#| fig-alt: A lineplot of the monthly averages from 1958 to 2019. The data mostly has a repeating wave pattern and is larger as time goes on. However, there are a number of large dips to -100.
sns.lineplot(x='DecDate', y='Avg', data=co2)
plt.title("CO2 Average By Month");

# %% [markdown] id="8035bf9d"
# Since we are plotting `Avg` vs `DecDate`, we should just focus on dealing with missing values for `Avg`.
#
# Let's consider a few options:
# 1. Drop those records
# 2. Replace -99.99 with `null`
# 3. Substitute it with a likely value for the average CO<sub>2</sub>?
#
# What do you think are the pros and cons of each possible action?
#
# Let's examine each of these three options.

# %% tags=["remove-input", "remove-output"] id="613b57a2"
# 1. Drop missing values
co2_drop = co2.filter(pl.col('Avg') > 0)
co2_drop.head()

# %% [markdown]
# <!-- tab-twins:begin 613b57a2 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # 1. Drop missing values
# co2_drop = co2.filter(pl.col('Avg') > 0)
# co2_drop.head()
# ```
#
# ```text
# shape: (5, 7)
# ┌──────┬─────┬─────────┬────────┬────────┬────────┬──────┐
# │ Yr   ┆ Mo  ┆ DecDate ┆ Avg    ┆ Int    ┆ Trend  ┆ Days │
# │ ---  ┆ --- ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---  │
# │ i64  ┆ i64 ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ i64  │
# ╞══════╪═════╪═════════╪════════╪════════╪════════╪══════╡
# │ 1958 ┆ 3   ┆ 1958.21 ┆ 315.71 ┆ 315.71 ┆ 314.62 ┆ -1   │
# │ 1958 ┆ 4   ┆ 1958.29 ┆ 317.45 ┆ 317.45 ┆ 315.29 ┆ -1   │
# │ 1958 ┆ 5   ┆ 1958.38 ┆ 317.50 ┆ 317.50 ┆ 314.71 ┆ -1   │
# │ 1958 ┆ 7   ┆ 1958.54 ┆ 315.86 ┆ 315.86 ┆ 314.98 ┆ -1   │
# │ 1958 ┆ 8   ┆ 1958.62 ┆ 314.93 ┆ 314.93 ┆ 315.94 ┆ -1   │
# └──────┴─────┴─────────┴────────┴────────┴────────┴──────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # 1. Drop missing values
# co2_drop = co2[co2['Avg'] > 0]
# co2_drop.head()
# ```
#
# ```text
#      Yr  Mo  DecDate    Avg    Int  Trend  Days
# 0  1958   3  1958.21 315.71 315.71 314.62    -1
# 1  1958   4  1958.29 317.45 317.45 315.29    -1
# 2  1958   5  1958.38 317.50 317.50 314.71    -1
# 4  1958   7  1958.54 315.86 315.86 314.98    -1
# 5  1958   8  1958.62 314.93 314.93 315.94    -1
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% id="ef3fe041"
# 2. Replace -99.99 with null
co2_null = co2.with_columns(pl.col(pl.Float64).replace(-99.99, None))
co2_null.head()

# %% [markdown] id="4be11b22"
# We'll also use a third version of the data.
#
# First, we note that the dataset already comes with a **substitute value** for the -99.99.
#
# From the file description:
#
# >  The `interpolated` column includes average values from the preceding column (`average`)
# and **interpolated values** where data are missing.  Interpolated values are
# computed in two steps...
#
# The `Int` feature has values that exactly match those in `Avg`, except when `Avg` is -99.99, and then a **reasonable** estimate is used instead.
#
# So, the third version of our data will use the `Int` feature instead of `Avg`.

# %% tags=["remove-input", "remove-output"] id="6667c947"
# 3. Use interpolated column which estimates missing Avg values
co2_impute = co2.with_columns(Avg = pl.col('Int'))
co2_impute.head()

# %% [markdown]
# <!-- tab-twins:begin 6667c947 -->
# :::::{tab-set}
# :::: {tab-item} Polars
# :sync: pl
# ```python
# # 3. Use interpolated column which estimates missing Avg values
# co2_impute = co2.with_columns(Avg = pl.col('Int'))
# co2_impute.head()
# ```
#
# ```text
# shape: (5, 7)
# ┌──────┬─────┬─────────┬────────┬────────┬────────┬──────┐
# │ Yr   ┆ Mo  ┆ DecDate ┆ Avg    ┆ Int    ┆ Trend  ┆ Days │
# │ ---  ┆ --- ┆ ---     ┆ ---    ┆ ---    ┆ ---    ┆ ---  │
# │ i64  ┆ i64 ┆ f64     ┆ f64    ┆ f64    ┆ f64    ┆ i64  │
# ╞══════╪═════╪═════════╪════════╪════════╪════════╪══════╡
# │ 1958 ┆ 3   ┆ 1958.21 ┆ 315.71 ┆ 315.71 ┆ 314.62 ┆ -1   │
# │ 1958 ┆ 4   ┆ 1958.29 ┆ 317.45 ┆ 317.45 ┆ 315.29 ┆ -1   │
# │ 1958 ┆ 5   ┆ 1958.38 ┆ 317.50 ┆ 317.50 ┆ 314.71 ┆ -1   │
# │ 1958 ┆ 6   ┆ 1958.46 ┆ 317.10 ┆ 317.10 ┆ 314.85 ┆ -1   │
# │ 1958 ┆ 7   ┆ 1958.54 ┆ 315.86 ┆ 315.86 ┆ 314.98 ┆ -1   │
# └──────┴─────┴─────────┴────────┴────────┴────────┴──────┘
# ```
# ::::
#
# :::: {tab-item} pandas
# :sync: pd
# ```python
# # 3. Use interpolated column which estimates missing Avg values
# co2_impute = co2.copy()
# co2_impute['Avg'] = co2['Int']
# co2_impute.head()
# ```
#
# ```text
#      Yr  Mo  DecDate    Avg    Int  Trend  Days
# 0  1958   3  1958.21 315.71 315.71 314.62    -1
# 1  1958   4  1958.29 317.45 317.45 315.29    -1
# 2  1958   5  1958.38 317.50 317.50 314.71    -1
# 3  1958   6  1958.46 317.10 317.10 314.85    -1
# 4  1958   7  1958.54 315.86 315.86 314.98    -1
# ```
# ::::
# :::::
# <!-- tab-twins:end -->

# %% [markdown] id="83bf5c89"
# What's a **reasonable** estimate?
#
# To answer this question, let's zoom in on a short time period, say the measurements in 1958 (where we know we have two missing values).
#
# ````{dropdown} Click to see the code
# :open: false
# ```
# #| fig-alt: "Three plots are shown with overall title 'Monthly Averages for 1958.' The first plot is 'Drop Missing' where the datapoints for x=6 and x=10 are not shown, but the datapoints are connected with lines. The second plot is 'Missing Set to Null' where the lines are segmented from 3 to 5, 7 to 9, and 11 to 12. The third plot is 'Missing Interpolated' where we see the missing datapoints at x=6 and x=10 are now imputed following the shape of the other data."
# # results of plotting data in 1958
#
# def line_and_points(data, ax, title):
#     # axssumes single year, hence Mo
#     ax.plot('Mo', 'Avg', data=data)
#     ax.scatter('Mo', 'Avg', data=data)
#     ax.set_xlim(2, 13)
#     ax.set_title(title)
#     ax.set_xticks(np.arange(3, 13))
#
# def data_year(data, year):
#     return data.filter(pl.col("Yr") == 1958)
#     
# # uses matplotlib subplots
# # you may see more next week; focus on output for now
# fig, axes = plt.subplots(ncols = 3, figsize=(12, 4), sharey=True)
#
# year = 1958
# line_and_points(data_year(co2_drop, year), axes[0], title="1. Drop Missing")
# line_and_points(data_year(co2_null, year), axes[1], title="2. Missing Set to Null")
# line_and_points(data_year(co2_impute, year), axes[2], title="3. Missing Interpolated")
#
# fig.suptitle(f"Monthly Averages for {year}")
# plt.tight_layout()
# ```
# ````

# %% tags=["remove-input"] id="7f3ea034"
#| fig-alt: "Three plots are shown with overall title 'Monthly Averages for 1958.' The first plot is 'Drop Missing' where the datapoints for x=6 and x=10 are not shown, but the datapoints are connected with lines. The second plot is 'Missing Set to Null' where the lines are segmented from 3 to 5, 7 to 9, and 11 to 12. The third plot is 'Missing Interpolated' where we see the missing datapoints at x=6 and x=10 are now imputed following the shape of the other data."
# results of plotting data in 1958

def line_and_points(data, ax, title):
    # axssumes single year, hence Mo
    ax.plot('Mo', 'Avg', data=data)
    ax.scatter('Mo', 'Avg', data=data)
    ax.set_xlim(2, 13)
    ax.set_title(title)
    ax.set_xticks(np.arange(3, 13))

def data_year(data, year):
    return data.filter(pl.col("Yr") == 1958)
    
# uses matplotlib subplots
# you may see more next week; focus on output for now
fig, axes = plt.subplots(ncols = 3, figsize=(12, 4), sharey=True)

year = 1958
line_and_points(data_year(co2_drop, year), axes[0], title="1. Drop Missing")
line_and_points(data_year(co2_null, year), axes[1], title="2. Missing Set to Null")
line_and_points(data_year(co2_impute, year), axes[2], title="3. Missing Interpolated")

fig.suptitle(f"Monthly Averages for {year}")
plt.tight_layout()

# %% [markdown] id="76ec57ac"
# In the big picture since there are only 7 `Avg` values missing (**<1%** of 738 months), any of these approaches would work.
#
# However there is some appeal to **option C, Imputing**:
#
# * Shows seasonal trends for CO<sub>2</sub>
# * We are plotting all months in our data as a line plot
#
#
# Let's replot our original figure with option 3:
#
# ````{dropdown} Click to see the code
# :open: false
# ```
# #| fig-alt: Plot titled CO2 averages by month, imputed. Now the data follows a repeating wave pattern while also increasing as the years increase.
# sns.lineplot(x='DecDate', y='Avg', data=co2_impute)
# plt.title("CO2 Average By Month, Imputed");
# ```
# ````

# %% tags=["remove-input"] id="0126ec81"
#| fig-alt: Plot titled CO2 averages by month, imputed. Now the data follows a repeating wave pattern while also increasing as the years increase.
sns.lineplot(x='DecDate', y='Avg', data=co2_impute)
plt.title("CO2 Average By Month, Imputed");

# %% [markdown] id="aa094087"
# Looks pretty close to what we see on the NOAA [website](https://gml.noaa.gov/ccgg/trends/)!
#
# ### Presenting the Data: A Discussion on Data Granularity
#
# From the description:
#
# * Monthly measurements are averages of average day measurements.
# * The NOAA GML website has datasets for daily/hourly measurements too.
#
# The data you present depends on your research question.
#
# **How do CO<sub>2</sub> levels vary by season?**
#
# * You might want to keep average monthly data.
#
# **Are CO<sub>2</sub> levels rising over the past 50+ years, consistent with global warming predictions?**
#
# * You might be happier with a **coarser granularity** of average year data!
#
# ````{dropdown} Click to see the code
# :open: false
# ```
# #| fig-alt: CO2 Average by Year. The line steadily increases from about y = 320 to over 400.
# co2_year = co2_impute.group_by('Yr').mean().sort('Yr')
# sns.lineplot(x='Yr', y='Avg', data=co2_year)
# plt.title("CO2 Average By Year");
# ```
# ````

# %% tags=["remove-input"] id="c57fa60e"
#| fig-alt: CO2 Average by Year. The line steadily increases from about y = 320 to over 400.
co2_year = co2_impute.group_by('Yr').mean().sort('Yr')
sns.lineplot(x='Yr', y='Avg', data=co2_year)
plt.title("CO2 Average By Year");

# %% [markdown] id="2c8528cf"
# Indeed, we see a rise by nearly 100 ppm of CO<sub>2</sub> since Mauna Loa began recording in 1958.
