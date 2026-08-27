"""The pandas half of each comparison tab.

Only the pandas snippet lives here. The Polars half is read from the live notebook cell at
generation time, so the two halves cannot drift apart in this file.

Cells are keyed by a unique substring of the **Polars source**, not by cell id: the jupytext
`.py` carries no ids, so jupytext mints fresh ones on every rebuild. Keying on the code is
stable across that churn, and it fails loudly if the code it points at ever changes.

`prelude` loads the same data the chapter loads, under `_pd` names, so each snippet reads the
way a pandas user would actually write it.
"""

_BABYNAMES_PRELUDE = """
import pandas as pd, zipfile
elections_pd = pd.read_csv('data/elections.csv')
with zipfile.ZipFile('data/babynamesbystate.zip') as z:
    with z.open('STATE.CA.TXT') as fh:
        babynames_pd = pd.read_csv(fh, header=None,
            names=['State', 'Sex', 'Year', 'Name', 'Count'])
"""

# Twins whose Polars output legitimately changes on every execution, declared one at a time.
#
# `order_unstable()` refuses these by default, and that default is right: a frozen block that cannot
# match a fresh run reports STALE at random and teaches people to ignore `--verify`. But a handful of
# cells exist *because* the output is unstable, and for those the churn is the lesson rather than a
# defect. `--verify` checks the code panes of these and says so, instead of pretending to check an
# output that was never going to hold still.
OUTPUT_CHURNS = {
    "polars_2": {
        # The chapter's warning admonition says grouped results come back in no particular order.
        # This is that claim made visible: pandas sorts group keys and returns 1910-1914 every time,
        # Polars returns whichever five finished first. It is the clearest contrast in the chapter,
        # and worth more than a freshness check on five year labels that carry no meaning.
        'babynames.group_by("Year").agg(pl.col("Count").sum()).head(5)',
    },
}

# Baseline-paired twins to leave off the page, by chapter and cell id.
#
# Pairing on cell id assumes the conversion changed how a cell is *spelled*, not what it *does*.
# Where that assumption fails, the two panes sit side by side under one heading and assert an
# equivalence that is false -- which no gate can see, because both halves are real, executed output
# of real code.
BASELINE_SKIP = {
    "intro_lec": {
        # The pandas original taught the `Series` *Index*; the Polars rewrite dropped it, because
        # Polars has no such thing. Pairing on cell id then pairs unrelated operations under one
        # heading, in the first chapter a student reads:
        #
        #   fba44498  `pl.Series("ratings", [...])` (names a Series)  vs  `pd.Series([...],
        #             index=[...])` (labels its rows). The prose above says "a name can be passed
        #             as the first argument" -- which, followed literally on the pandas tab, gives
        #             `pd.Series("ratings", [-1, 10, 2])`: the string becomes the *values* and the
        #             list becomes the index. Nothing raises.
        #   cb6cff88  `.cast(pl.Float64)`  vs  `s.index = [...]`. The prose says the call returns a
        #             new Series and changes the data type; the pandas half mutates in place and
        #             changes no dtype -- its own committed output still reads `dtype: int64`.
        #   53a863ee  `s.dtype`  vs  `s.index`. One reads a data type, the other reads row labels.
        #   3117fc63  `.to_list()` (a `list`)  vs  `.values` (an `ndarray`), under a shared comment
        #             asserting they are the same operation. This is the *first* pandas/Polars pair
        #             in the book, so `.values == .to_list()` is the mapping a reader carries out
        #             of it. The honest twin is `.tolist()`.
        #
        #   12449aec  a bare `s.index` printing `Index(['a', 'b', 'c'])` -- labels that came from
        #             `fba44498`'s pandas half, which is no longer on the page. I originally kept
        #             this one on the grounds that it "carries per-tab comments that disclose the
        #             contrast". It does not; `9371d026` does. That claim was wrong and this entry
        #             is the correction.
        #
        # `9371d026` makes the same Index contrast on purpose and keeps its twin: both its panes
        # carry comments naming what each one is reading.
        "fba44498", "cb6cff88", "53a863ee", "3117fc63", "12449aec",
    },
    "eda": {
        # `dt.weekday()` numbers Monday=1..Sunday=7; pandas `dt.dayofweek` numbers Monday=0..Sunday=6.
        # The prose above *both* tabs announces "Monday = 1", so the pandas pane prints an output
        # that contradicts the sentence introducing it. The honest twin is `dt.dayofweek + 1`.
        "b432c276",
        # Polars reads the file raw -- `(738, 1)`, one string column, no commas anywhere -- and the
        # prose below says "each record is still one long string... We need to do more EDA." The
        # pandas half passes `sep=r'\s+'` and arrives already split and typed at `(738, 7)`, so the
        # two-step narrative the section is built on is finished before it starts on that tab.
        "719dc1a4",
        # The pandas pane's own comment reads `# 2. Replace NaN with -99.99` above code that does
        # the reverse (`co2.replace(-99.99, np.nan)`). It is the pandas original's error, inherited
        # verbatim, and the conversion corrected the Polars side to `# 2. Replace -99.99 with null`
        # -- so the tab now shows two comments describing opposite operations under one heading.
        # Publishing a false statement because it is old is still publishing it.
        "ef3fe041",
    },
    "modeling_slr": {
        # The pandas pane republishes a bug the conversion deliberately fixed, and frames it as a
        # library difference. The baseline cell printed `f"\theta_0: ..."` -- `\t` is Python's tab
        # escape, so the label rendered as a TAB followed by `heta_0`. The conversion repaired the
        # f-string; pairing on cell id then puts the *fixed* Polars run beside the *unfixed* pandas
        # transcript, so the only visible difference under a heading saying "pandas" is four lines
        # of mangled text. pandas does not do that. (This was the chapter's only twinnable cell, so
        # `modeling_slr` now carries none -- see CONVERSIONS.md on cell `ce691b4e`.)
        "e83b8086",
    },
    "pca": {
        # `rectangle` has rank 3, so the fourth singular value is ~1e-14 and its singular vector
        # spans the null space -- LAPACK picks it arbitrarily. Verified that the two libraries agree
        # exactly (`np.array_equal(U, U_pandas)` is True); what differs is the run, not the library.
        # Frozen side by side the tab shows 0.967868 against 0.894121 under one heading and invites
        # the reader to conclude Polars and pandas disagree about an SVD. Same reasoning as the
        # order-unstable guard: a value that is not reproducible does not belong in a frozen pane.
        "a4377823", "f5849357",
    },
    "regex": {
        # Polars: `extract_groups` -> each group's FIRST match, non-matching rows kept as null.
        # pandas baseline: `extractall` -> EVERY match, non-matching rows dropped, MultiIndex.
        # On this data the row for "forty" appears in one pane and not the other, and the second
        # SSN on line 2 appears in one and not the other. The conversion deliberately moved this
        # cell from all-matches to first-match, and the chapter teaches all-matches separately at
        # `cb4897da` (`.str.extract_all`) -- so the honest pandas twin here is `str.extract`, which
        # cell `188458d4` already shows. Two tabs, not three.
        "1ba6f098",
    },
}

TWINS = {
    "polars_1": {
        "prelude": _BABYNAMES_PRELUDE,
        "cells": {
            # Column selection: pandas indexes with a list; there is no expression object.
            'elections.select(["Year", "Candidate", "Result"])':
                'elections_pd[["Year", "Candidate", "Result"]]',
            # A computed column: pandas builds it, then renames it.
            'elections.select((pl.col("Popular vote") / 1_000_000)':
                'elections_pd[["Popular vote"]].div(1_000_000).rename(\n'
                '    columns={"Popular vote": "Popular vote (millions)"}\n)',
            # Filtering: a boolean mask indexed back into the frame.
            'elections.filter(pl.col("Popular vote") > 60000000)':
                'elections_pd[elections_pd["Popular vote"] > 60000000]',
            # A single row: pandas hands back a Series, not a tuple.
            "elections.row(0)":
                "elections_pd.iloc[0]",
            # Distinct count, spelt differently.
            'babynames["Name"].n_unique()':
                'babynames_pd["Name"].nunique()',
            # Sorting: `ascending=` is the opposite sense to `descending=`.
            'babynames.sort("Count").head()':
                'babynames_pd.sort_values("Count").head()',
            'babynames.sort("Count", descending=True).head()':
                'babynames_pd.sort_values("Count", ascending=False).head()',
            # describe(): same name, different shape of answer.

            # --- Building and inspecting ---------------------------------------------------
            # The import itself: one line, no output, and the first difference a reader meets.
            "import polars as pl":
                "# `pd` is the conventional alias for pandas, as `np` is for NumPy\n"
                "import pandas as pd",
            # The whole frame: same call, and a repr a pandas reader will not recognise.
            'elections = pl.read_csv("data/elections.csv")':
                'elections_pd = pd.read_csv("data/elections.csv")\n'
                'elections_pd',
            # Choosing columns at read time. Both libraries return them in *file* order, not the
            # order named -- the keyword picks which, never the arrangement.
            'pl.read_csv("data/elections.csv", columns=["Candidate", "Year", "%"])':
                'pd.read_csv("data/elections.csv", usecols=["Candidate", "Year", "%"])',
            # Reading only the first few rows: `n_rows` vs `nrows`.
            'pl.read_csv("data/elections.csv", n_rows=5)':
                'pd.read_csv("data/elections.csv", nrows=5)',
            # From a list of rows: pandas reads a list of lists row-wise already, so there is no
            # `orient=` to set -- and it names the columns with `columns=` rather than `schema=`.
            'df_list_1 = pl.DataFrame(':
                'df_list_1_pd = pd.DataFrame(\n'
                '    [["Kiwi", 5.49],\n'
                '     ["Orange", 3.99]],\n'
                '    columns=["Fruit", "Price"]\n'
                ')\n'
                'df_list_1_pd',
            # From a list of dicts: identical shape of call in both.
            'df_list_2 = pl.DataFrame(':
                'df_list_2_pd = pd.DataFrame(\n'
                '    [{"Fruit": "Kiwi", "Price": 5.49},\n'
                '     {"Fruit": "Orange", "Price": 3.99}]\n'
                ')\n'
                'df_list_2_pd',
            # From a dict of columns.
            'df_dict = pl.DataFrame(':
                'df_dict_pd = pd.DataFrame(\n'
                '    {"Fruit": ["Kiwi", "Orange"],\n'
                '     "Price": [5.49, 3.99]}\n'
                ')\n'
                'df_dict_pd',
            # A named Series. pandas takes the name as a keyword; Polars as the first argument.
            'ser_a = pl.Series("ser_a", ["a1", "a2", "a3"])':
                'ser_a_pd = pd.Series(["a1", "a2", "a3"], name="ser_a")\n'
                'ser_b_pd = pd.Series(["b1", "b2", "b3"], name="ser_b")\n'
                'ser_a_pd',
            # Two Series side by side under names we choose.
            '{"ColumnA": ser_a, "ColumnB": ser_b}':
                'pd.DataFrame(\n'
                '    {"ColumnA": ser_a_pd, "ColumnB": ser_b_pd}\n'
                ')',
            # A Series handed straight to the frame constructor.
            "pl.DataFrame(ser_a)":
                'pd.DataFrame(ser_a_pd)',

            # --- Attributes ---------------------------------------------------------------
            # Column names: an `Index` object in pandas, a plain list in Polars.
            "elections.columns":
                'elections_pd.columns',
            # Types: a Series keyed by column name in pandas, a list in Polars.
            "elections.dtypes":
                'elections_pd.dtypes',
            # Polars has a dedicated Schema pairing names with types; pandas reuses dtypes.
            "elections.schema":
                'elections_pd.dtypes.to_dict()',
            # Shape agrees exactly -- the tool skips this pair rather than show two identical panes.
            "elections.shape":
                'elections_pd.shape',

            # --- head and tail ------------------------------------------------------------
            "elections.head()":
                'elections_pd.head()',
            "elections.tail(5)":
                'elections_pd.tail(5)',
            "elections.head(3)":
                'elections_pd.head(3)',

            # --- [] indexing: the section a pandas reader has most to unlearn --------------
            # One value. Polars takes (row, column) directly; pandas needs .loc.
            'elections[0, "Candidate"]':
                'elections_pd.loc[0, "Candidate"]',
            # Rows and named columns together.
            'elections[[87, 25, 179], ["Year", "Party", "%"]]':
                'elections_pd.loc[[87, 25, 179], ["Year", "Party", "%"]]',
            # A slice *of column names*, inclusive of the endpoint in both libraries.
            'elections[[87, 25, 179], "Popular vote":"%"]':
                'elections_pd.loc[[87, 25, 179], "Popular vote":"%"]',
            # All rows, three columns. pandas drops the row slot entirely for this.
            'elections[:, ["Year", "Candidate", "Result"]]':
                'elections_pd[["Year", "Candidate", "Result"]]',
            # All columns, three rows.
            "elections[[87, 25, 179], :]":
                'elections_pd.loc[[87, 25, 179]]',
            # A single column name gives a Series...
            'elections[[87, 25, 179], "Popular vote"]':
                'elections_pd.loc[[87, 25, 179], "Popular vote"]',
            # ...and the same name in a list gives a one-column frame. True in both.
            'elections[[87, 25, 179], ["Popular vote"]]':
                'elections_pd.loc[[87, 25, 179], ["Popular vote"]]',
            # Row positions with no column slot at all.
            "elections[[180, 181]]":
                'elections_pd.iloc[[180, 181]]',
            # A bare column name.
            'elections["Candidate"]':
                'elections_pd["Candidate"]',
            # Both slots as integers: this is .iloc territory in pandas.
            "elections[0, 1]":
                'elections_pd.iloc[0, 1]',
            "elections[[1, 2, 3], 1]":
                'elections_pd.iloc[[1, 2, 3], 1]',
            "elections[[1, 2, 3], [0, 1, 2]]":
                'elections_pd.iloc[[1, 2, 3], [0, 1, 2]]',
            # An integer column slice, exclusive of the endpoint in both.
            "elections[[1, 2, 3], 0:3]":
                'elections_pd.iloc[[1, 2, 3], 0:3]',
            # A row slice.
            "elections[138:144]":
                'elections_pd.iloc[138:144]',

            # --- The mistake both libraries refuse ----------------------------------------
            # `and` asks one yes-or-no question of a many-valued object. Both reject it; the
            # wording differs because pandas is looking at a Series and Polars at an expression.
            'elections.filter((pl.col("Year") == 2008) and (pl.col("%") >= 60))':
                '# This line of code will raise a ValueError\n'
                'elections_pd[(elections_pd["Year"] == 2008) and (elections_pd["%"] >= 60)]',

            # A filtered column, kept as a Series.
            'yash_counts = babynames.filter(pl.col("Name") == "Yash")["Count"]':
                'yash_counts_pd = babynames_pd[babynames_pd["Name"] == "Yash"]["Count"]\n'
                'yash_counts_pd',
            "yash_counts.mean()":
                'yash_counts_pd.mean()',
            "yash_counts.max()":
                'yash_counts_pd.max()',
            "babynames.shape":
                'babynames_pd.shape',
            # Polars names the two dimensions; pandas multiplies them into `.size`.
            "babynames.height * babynames.width":
                'babynames_pd.size',
            "len(babynames)":
                'len(babynames_pd)',

            # --- Adding, modifying, renaming and dropping columns --------------------------
            # Polars returns a new frame from `with_columns`; pandas assigns into the existing one.
            "babynames = babynames.with_columns(name_lengths=babyname_lengths)\nbabynames.head()":
                '# Create a Series of the length of each name\n'
                'babyname_lengths_pd = babynames_pd["Name"].str.len()\n'
                '\n'
                '# Add a column named "name_lengths" that includes the length of each name\n'
                'babynames_pd["name_lengths"] = babyname_lengths_pd\n'
                'babynames_pd.head()',
            'babynames = babynames.with_columns(name_lengths=pl.col("name_lengths") - 1)':
                '# Modify the "name_lengths" column to be one less than its original value\n'
                'babynames_pd["name_lengths"] = babynames_pd["name_lengths"] - 1\n'
                'babynames_pd.head()',
            'babynames = babynames.rename({"name_lengths": "Length"})':
                '# Rename "name_lengths" to "Length"\n'
                'babynames_pd = babynames_pd.rename(columns={"name_lengths": "Length"})\n'
                'babynames_pd.head()',
            'babynames = babynames.drop("Length")':
                '# Drop our new "Length" column from the DataFrame\n'
                'babynames_pd = babynames_pd.drop(columns="Length")\n'
                'babynames_pd.head()',
            'babynames.drop("Name")':
                '# This produces a new table without the column "Name"...\n'
                'babynames_pd.drop(columns="Name")\n'
                '\n'
                '# ...but the original `babynames_pd` is unchanged!\n'
                '# Notice that the "Name" column is still present\n'
                'babynames_pd.head()',

            # --- Custom sorts --------------------------------------------------------------
            "babynames = babynames.with_columns(name_lengths=babyname_lengths)\nbabynames.head(5)":
                '# Create a Series of the length of each name\n'
                'babyname_lengths_pd = babynames_pd["Name"].str.len()\n'
                '\n'
                '# Add a column named "name_lengths" that includes the length of each name\n'
                'babynames_pd["name_lengths"] = babyname_lengths_pd\n'
                'babynames_pd.head(5)',
            'babynames = babynames.sort(by="name_lengths", descending=True)':
                '# Sort by the temporary column\n'
                'babynames_pd = babynames_pd.sort_values(by="name_lengths", ascending=False)\n'
                'babynames_pd.head(5)',
            'babynames = babynames.drop("name_lengths")':
                '# Drop the "name_lengths" column\n'
                'babynames_pd = babynames_pd.drop(columns="name_lengths")\n'
                'babynames_pd.head(5)',
            # Element-wise Python: pandas `.apply`, Polars `.map_elements` with a declared dtype.
            "def dr_ea_count(string):":
                '# First, define a function to count the number of times\n'
                '# "dr" or "ea" appear in each name\n'
                'def dr_ea_count_pd(string):\n'
                '    return string.count(\'dr\') + string.count(\'ea\')\n'
                '\n'
                '# Then, use apply to run dr_ea_count over each name in the "Name" column\n'
                'babynames_pd["dr_ea_count"] = babynames_pd["Name"].apply(dr_ea_count_pd)\n'
                '\n'
                '# Sort the DataFrame by the new "dr_ea_count" column so we can see our handiwork\n'
                'babynames_pd = babynames_pd.sort_values(by="dr_ea_count", ascending=False)\n'
                'babynames_pd.head()',
            'babynames = babynames.drop("dr_ea_count")':
                '# Drop the "dr_ea_count" column\n'
                'babynames_pd = babynames_pd.drop(columns="dr_ea_count")\n'
                'babynames_pd.head(5)',

            # --- Selection and filtering -------------------------------------------------
            # A Series becomes a one-column frame; pandas carries the index across with it.
            "ser_a.to_frame()":
                'ser_a_pd.to_frame()',
            # A named row: pandas has no `named=` -- the Series index already holds the names.
            "elections.row(0, named=True)":
                'elections_pd.iloc[0].to_dict()',
            # Filter then pick columns: pandas does both inside one `.loc`.
            'elections.filter(pl.col("Year") == 2008).select(["Year", "Candidate"])':
                'elections_pd.loc[elections_pd["Year"] == 2008, ["Year", "Candidate"]]',
            # OR across two conditions.
            'elections.filter((pl.col("Year") == 2008) | (pl.col("%") >= 60))':
                'elections_pd[(elections_pd["Year"] == 2008) | (elections_pd["%"] >= 60)]',
            # AND across two conditions.
            'elections.filter((pl.col("Year") > 2000) & (pl.col("Result") == "win"))':
                'elections_pd[(elections_pd["Year"] > 2000) & (elections_pd["Result"] == "win")]',
            # Four conditions, broken across lines the way the Polars version is.
            '(pl.col("Year") < 2000) &':
                'elections_pd[\n'
                '    (elections_pd["Year"] < 2000)\n'
                '    & (elections_pd["Year"] > 1941)\n'
                '    & (elections_pd["Result"] == "win")\n'
                '    & (elections_pd["%"] >= 55)\n'
                ']',
            # Row positions: pandas already has them, in the index -- `reset_index` materializes it.
            'elections.with_row_index("original_position").sort("%", descending=True).head()':
                'elections_pd.reset_index(names="original_position").sort_values(\n'
                '    "%", ascending=False\n'
                ').head()',
            # Numbering *after* a sort means dropping the old index and taking a fresh one.
            'elections.sort("%", descending=True).with_row_index().head()':
                'elections_pd.sort_values("%", ascending=False).reset_index(drop=True).reset_index().head()',
            # Four names the long way, one OR per name.
            'babynames.filter((pl.col("Name") == "Bella") |':
                'babynames_pd[\n'
                '    (babynames_pd["Name"] == "Bella")\n'
                '    | (babynames_pd["Name"] == "Alex")\n'
                '    | (babynames_pd["Name"] == "Narges")\n'
                '    | (babynames_pd["Name"] == "Lisa")\n'
                ']',
            # The same four names with a membership test.
            'babynames.filter(pl.col("Name").is_in(names))':
                'names_pd = ["Bella", "Alex", "Narges", "Lisa"]\n'
                'babynames_pd[babynames_pd["Name"].isin(names_pd)]',
            # String predicate: `.str` is an accessor in pandas, a namespace in Polars.
            'babynames.filter(pl.col("Name").str.starts_with("N"))':
                'babynames_pd[babynames_pd["Name"].str.startswith("N")]',

            # --- Summarising --------------------------------------------------------------
            # describe() on a text column: pandas reports count/unique/top/freq.
            'babynames["Sex"].describe()':
                'babynames_pd["Sex"].describe()',
            # value_counts sorts by count in pandas by default, and indexes by the value.
            'babynames["Name"].value_counts(sort=True).head()':
                'babynames_pd["Name"].value_counts().head()',
            # First five distinct names in order of appearance.
            'babynames["Name"].unique(maintain_order=True).head(5)':
                'babynames_pd["Name"].unique()[:5]',

            # --- Sorting ------------------------------------------------------------------
            # Sorting a Series alphabetically.
            'babynames["Name"].sort().head(5)':
                'babynames_pd["Name"].sort_values().head(5)',
            # Nulls: pandas puts NaN last by default, Polars puts null first.
            'demo = pl.DataFrame(':
                'demo_pd = pd.DataFrame({"Name": ["Aaliyah", "Bao", "Cyrus"],\n'
                '                        "Count": [3, None, 1]})\n'
                'demo_pd.sort_values("Count", ascending=False)',
            # Asking for them last explicitly, which is already pandas\' default.
            'demo.sort("Count", descending=True, nulls_last=True)':
                'demo_pd.sort_values("Count", ascending=False, na_position="last")',
            # Sorting by a computed value: pandas needs a temporary column to sort on.
            'babynames.sort(pl.col("Name").str.len_chars(), descending=True).head()':
                'babynames_pd.assign(_len=babynames_pd["Name"].str.len()).sort_values(\n'
                '    "_len", ascending=False\n'
                ').drop(columns="_len").head()',
            "babynames.describe()":
                "babynames_pd.describe()",
        },
    },
    "polars_2": {
        "prelude": _BABYNAMES_PRELUDE + """
df_pd = pd.DataFrame({'letter': ['A', 'A', 'B', 'C', 'C', 'C'],
                      'num': [1, 2, 3, 4, None, 4],
                      'state': [None, 'tx', 'fl', 'hi', None, 'ak']})
babynames_2022_pd = babynames_pd[babynames_pd['Year'] == 2022]
f_babynames_pd = babynames_pd[babynames_pd['Sex'] == 'F'].sort_values('Year')
babynames_new_pd = babynames_pd.assign(**{'First Letter': babynames_pd['Name'].str[0]})
elections_pd['First Name'] = elections_pd['Candidate'].str.split().str[0]
""",
        "cells": {
            # Grouped output comes back in no guaranteed order in Polars; pandas sorts the group
            # keys, so it hands back 1910-1914 every time. The chapter's warning is this pair.
            'babynames.group_by("Year").agg(pl.col("Count").sum()).head(5)':
                'babynames_pd.groupby("Year")["Count"].sum().head(5)',
            # A derived column, then a subset. pandas assigns, then indexes with a list.
            'pl.col("Name").str.slice(0, 1).alias("First Letter")':
                '# Imagine we had an additional column, "First Letter".\n'
                'babynames_new_pd = babynames_pd.assign(\n'
                '    **{"First Letter": babynames_pd["Name"].str[0]}\n'
                ')[["Name", "First Letter", "Year"]]\n'
                '\n'
                'babynames_new_pd.head()',
            # A small frame with missing values: `None` becomes `NaN` in pandas, `null` in Polars.
            'df = pl.DataFrame({"letter": ["A", "A", "B", "C", "C", "C"],':
                'df_pd = pd.DataFrame({"letter": ["A", "A", "B", "C", "C", "C"],\n'
                '                      "num": [1, 2, 3, 4, None, 4],\n'
                '                      "state": [None, "tx", "fl", "hi", None, "ak"]})\n'
                'df_pd',
            'f_babynames = babynames.filter(pl.col("Sex") == "F").sort("Year")':
                'f_babynames_pd = babynames_pd[babynames_pd["Sex"] == "F"].sort_values("Year")\n'
                'f_babynames_pd.head()',
            # Ten names out of a sorted table, as a plain Python list.
            'top10 = rtp_table.sort("Count RTP").head(10)["Name"].to_list()':
                'top10_pd = rtp_pd.sort_values("Count RTP").head(10).index.tolist()\n'
                'top10_pd',
            'elections = pl.read_csv("data/elections.csv")\nelections.head(5)':
                'elections_pd = pd.read_csv("data/elections.csv")\n'
                'elections_pd.head(5)',

            # --- Picking the best row per group --------------------------------------------
            'elections_sorted_by_percent = elections.sort("%", descending=True)':
                'elections_sorted_pd = elections_pd.sort_values("%", ascending=False)\n'
                'elections_sorted_pd.head(5)',
            # First row of each group: pandas `.head(1)` on a GroupBy does the same job.
            'best_per_party = elections_sorted_by_percent.group_by("Party", maintain_order=True).head(1)':
                'best_per_party_pd = elections_sorted_pd.groupby("Party", sort=False).head(1)\n'
                'best_per_party_pd.head(10)',
            # The row *positions* of each group's best: pandas has `idxmax`, which returns index
            # labels rather than positions -- the same idea, expressed in the index it already has.
            'best_positions = (':
                'best_positions_pd = (\n'
                '    elections_pd.groupby("Party")["%"].idxmax().sort_index()\n'
                ')\n'
                'best_positions_pd.head()',
            'elections[best_positions["position"]].sort("Party").head()':
                'elections_pd.loc[best_positions_pd].sort_values("Party").head()',

            # --- GroupBy objects ------------------------------------------------------------
            # Polars keys groups by tuple; pandas by the bare value for a single key.
            "groups = dict(grouped_by_party)":
                'groups_pd = dict(list(grouped_by_party_pd))\n'
                'sorted(groups_pd.keys())[:6]',
            'groups[("Socialist",)]':
                'groups_pd["Socialist"]',

            # --- Pivot ----------------------------------------------------------------------
            'aggregate_function="sum", # how to combine the rows that land in one cell':
                'babynames_pd.pivot_table(\n'
                '    index="Year",     # one row per year\n'
                '    columns="Sex",    # the values of Sex become column names\n'
                '    values="Count",   # what fills the cells\n'
                '    aggfunc="sum",    # how to combine the rows that land in one cell\n'
                ').head(5)',
            'values=["Count", "Name"],':
                'babynames_pd.pivot_table(\n'
                '    index="Year",\n'
                '    columns="Sex",\n'
                '    values=["Count", "Name"],\n'
                '    aggfunc="max",\n'
                ').head(6)',

            # --- Joining --------------------------------------------------------------------
            'pl.col("Candidate").str.split(" ").list.get(0).alias("First Name")':
                '# Split each candidate\'s full name on the blank space, then keep the first piece\n'
                'elections_pd["First Name"] = elections_pd["Candidate"].str.split(" ").str[0]\n'
                'elections_pd.head(5)',
            'babynames_2022 = babynames.filter(pl.col("Year") == 2022)':
                '# Here, we\'ll only consider `babynames` data from 2022\n'
                'babynames_2022_pd = babynames_pd[babynames_pd["Year"] == 2022]\n'
                'babynames_2022_pd.head()',
            # pandas calls it `merge`, and keeps *both* key columns rather than coalescing them.
            'merged = elections.join(':
                'merged_pd = elections_pd.merge(\n'
                '    babynames_2022_pd,\n'
                '    left_on="First Name",\n'
                '    right_on="Name",\n'
                ')\n'
                'merged_pd.head()',
            "merged.columns":
                '# The full column list, since the table above is too wide to show it\n'
                'merged_pd.columns.tolist()',

            # group_by/agg: pandas names the aggregate afterwards; Polars names it in the
            # expression. Paired against the *sorted* cell -- the unsorted one a few lines above
            # is deliberately nondeterministic, and a frozen block cannot mirror a cell whose
            # output legitimately changes on every run.
            'babies_by_year = babynames.group_by("Year").agg(pl.col("Count").sum()).sort("Year")':
                '# pandas sorted the group keys for us -- we never asked it to\n'
                'babies_by_year_pd = babynames_pd.groupby("Year")["Count"].sum()\n'
                'babies_by_year_pd.head(5)',
            # Counting rows per group: `size()` vs `len()`, and pandas returns a Series.
            'df.group_by("letter", maintain_order=True).len()':
                'df_pd.groupby("letter", sort=False).size()',
            # A minimum per group, sorted by key.
            'babynames.group_by("Name").agg(pl.col("Count").min()).sort("Name").head()':
                'babynames_pd.groupby("Name")["Count"].min().sort_index().head()',

            # Several aggregates at once: pandas names them with a dict, Polars with .alias.
            'pl.col("Count").mean().alias("Mean Count"),':
                'babynames_pd.groupby("Name")["Count"].agg(\n'
                '    **{"Min Count": "min", "Max Count": "max", "Mean Count": "mean",\n'
                '       "Years Recorded": "size"}\n'
                ').sort_index().head()',
            # Different aggregate per column.
            'pl.col("First Letter").first(),':
                'babynames_new_pd.groupby("Name").agg(\n'
                '    **{"First Letter": ("First Letter", "first"), "Year": ("Year", "max")}\n'
                ').sort_index().head()',
            # count() per column skips nulls, so the columns disagree -- true in both libraries.
            'df.group_by("letter", maintain_order=True).agg(pl.all().count())':
                'df_pd.groupby("letter", sort=False).count()',
            # value_counts on a Series.
            'df["letter"].value_counts(sort=True)':
                'df_pd["letter"].value_counts()',
            # Pulling two scalars out of a filtered column.
            'latest_jenn / max_jenn':
                'jenn_pd = f_babynames_pd[f_babynames_pd["Name"] == "Jennifer"]["Count"]\n'
                'max_jenn_pd = jenn_pd.max()\n'
                'latest_jenn_pd = jenn_pd.iloc[-1]\n'
                'latest_jenn_pd / max_jenn_pd',
            # A ratio computed inside the aggregation.
            'rtp_table = f_babynames.group_by("Name").agg(':
                'rtp_pd = f_babynames_pd.groupby("Name")["Count"].agg(\n'
                '    **{"Count RTP": lambda s: s.iloc[-1] / s.max()}\n'
                ')\n'
                'rtp_pd.sort_index().head()',
            # A named function applied per group.
            'def ratio_to_peak(series):':
                'def ratio_to_peak_pd(series):\n'
                '    """Ratio of the most recent count to the largest count."""\n'
                '    return series.iloc[-1] / series.max()\n'
                '\n'
                'f_babynames_pd.groupby("Name")["Count"].agg(\n'
                '    **{"Count RTP": ratio_to_peak_pd}\n'
                ').sort_values("Count RTP").head()',
            # The same table, smallest ratio first.
            'rtp_table.sort("Count RTP").head()':
                'rtp_pd.sort_values("Count RTP").head()',
            # Rows chosen by a property of their group: transform() is pandas' window form.
            'elections.filter(pl.col("%").max().over("Year") < 45).head(9)':
                'elections_pd[\n'
                '    elections_pd.groupby("Year")["%"].transform("max") < 45\n'
                '].head(9)',
            # max() over every column of a group -- each column maxes independently.
            'elections.group_by("Party").max().sort("Party").head(10)':
                'elections_pd.groupby("Party").max(numeric_only=False).sort_index().head(10)',
            # The winner per party, via the row that holds each group's largest share.
            'best_per_party2 = elections.sort("%").unique(subset=["Party"], keep="last", maintain_order=True)':
                'best_per_party2_pd = elections_pd.sort_values("%").drop_duplicates(\n'
                '    subset="Party", keep="last"\n'
                ')\n'
                'best_per_party2_pd.sort_values("Party").head()',
            # The GroupBy object's type.
            "type(grouped_by_party)":
                'grouped_by_party_pd = elections_pd.groupby("Party")\n'
                'type(grouped_by_party_pd)',
            # Grouping on two keys: pandas returns a MultiIndex, Polars two ordinary columns.
            'babynames.group_by(["Year", "Sex"]).agg(pl.col("Count").sum()).sort(["Year", "Sex"]).head(6)':
                'babynames_pd.groupby(["Year", "Sex"])["Count"].sum().head(6)',
            # An anti-join: pandas has no `how="anti"`, so it is an indicator merge and a filter.
            'how="anti", maintain_order="left"':
                'elections_pd[\n'
                '    ~elections_pd["First Name"].isin(babynames_2022_pd["Name"])\n'
                '].head()',
            # Filtering by a property of the group: a window expression vs groupby().filter().
            'df.filter(pl.len().over("letter") >= 2)':
                'df_pd.groupby("letter").filter(lambda g: len(g) >= 2)',
        },
    },
}
