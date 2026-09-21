# pca — change report

`887a578b0a4b:content/pca/pca.ipynb` → `content/pca/pca.ipynb`

**Tier C · 104 changes:** output 28 · prose 10 · dropdown 24 · tab-twins 11 · code 28 · metadata 3

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

Tier C, and the heaviest reshape in the book: the House-of-Representatives section was
built on the pandas index at nearly every step (`pivot_table` → `pivot` with an aggregate *expression*,
the index-alignment join, `.T.reset_index().rename().melt()` → `unpivot`), and the Fashion-MNIST
section moved from a column of Python lists to a native `array[f64, (28, 28)]`. Three things to look
at. (1) `.sort("member")` and `sort_columns=True` on the pivot are load-bearing, not cosmetic
pandas-matching: row order fixes the sign of every principal component, and without the member sort
the live biplot becomes the mirror image of `images/slide17_2.png` and of `images/pca_plot.png`'s alt
text — see CONVERSIONS.md "The sign flip". Verified here: no committed figure in this chapter has a
flipped axis, every one matches the baseline to ≤3.4e-14 relative. (2) `print(vote_pivot.shape)` now
ships `(441, 42)` because `member` is a column rather than an index, and C29 is a new paragraph added
to read that number; it is the one place the converted prose talks about pandas. (3) Four of the ten
prose edits (C6, C7, C8, C9, C76) are corrections to *pre-existing* false claims logged in
CONTRADICTIONS.md §A7, not conversion work — staff should decide whether they ship inside a Polars
diff.

One thing the generated output list cannot show: the report's **output** pass covers text outputs
only, so the 15 plotly figures are absent from it. Checked separately — thirteen are pixel-identical
or drift in the last float digits, but the two Fashion-MNIST grids (`9178ee4c`, `3ec83d53`) redraw
**all 20 garments**, because the sampling expression changed. Same ten classes, same order, correct
labels; different clothes.

## Needs review

- [C6](#c6) · cell 16: Dimensionality
- [C7](#c7) · cell 16: Dimensionality
- [C8](#c8) · cell 17: [Optional for Spring 26] Singular Value Decomposition (SVD)
- [C9](#c9) · cell 17: SVD: $U$
- [C15](#c15) · cell 39: Code Demo
- [C21](#c21) · cell 47: Biplots
- [C29](#c29) · cell 53 [markdown]
- [C30](#c30) · cell 53: PCA with SVD
- [C43](#c43) · cell 61 [markdown]
- [C76](#c76) · cell 92: [BONUS] Proof of Component Score

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C77](#c77) · `mpg = pl.from_pandas(sns.load_dataset("mpg")).drop_nulls()`
- [C78](#c78) · `px.histogram(mpg, x="displacement")`
- [C79](#c79) · `px.scatter(mpg, x="displacement", y="horsepower")`
- [C80](#c80) · `fig = px.scatter_3d(mpg, x="displacement", y="horsepower", z="weight",`
- [C81](#c81) · `fig = px.scatter_3d(mpg, x="displacement",`
- [C82](#c82) · `fig = px.scatter_3d(mpg, x="displacement",`
- [C83](#c83) · `import polars as pl`
- [C84](#c84) · `pl.DataFrame(U).head(5)`
- [C85](#c85) · `S`
- [C86](#c86) · `Sm = np.diag(S)`
- [C87](#c87) · `pl.DataFrame(Vt)`
- [C88](#c88) · `pl.DataFrame(U @ Sm @ Vt).head(5)`
- [C89](#c89) · `centered_df = rectangle.select(pl.all() - pl.all().mean())`
- [C90](#c90) · `two_PCs = Vt.T[:, :2]`
- [C91](#c91) · `import polars as pl`
- [C92](#c92) · `was_yes = (pl.element().first() == "Yes").cast(pl.Int64)`
- [C93](#c93) · `fig = px.line(y=s**2 / sum(s**2), title='Variance Explained', width=70`
- [C94](#c94) · `Z = (u * s)[:, :3]`
- [C95](#c95) · `legislators_data = yaml.safe_load(open("data/legislators-2019.yaml"))`
- [C96](#c96) · `fig_eig = px.bar(x=vote_pivot_centered.columns, y=vt[0, :])`
- [C97](#c97) · `party_line_votes = (`
- [C98](#c98) · `loadings = pl.DataFrame(`
- [C99](#c99) · `class_names = [`
- [C100](#c100) · `def show_images(images, ncols=5, max_images=30):`
- [C101](#c101) · `print(class_dict)`
- [C102](#c102) · `images.head()`
- [C103](#c103) · `fig = px.line(y=pca.explained_variance_ratio_ * 100, markers=True)`
- [C104](#c104) · `images = images.hstack(pl.DataFrame(pca.transform(X)[:, :3], schema=["`

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C1](#c1) · cell 1: Visualization (Revisited)
- [C3](#c3) · cell 3 [markdown]
- [C10](#c10) · cell 18 [markdown]
- [C22](#c22) · cell 47: Example: House of Representatives Voting
- [C23](#c23) · cell 49 [markdown]
- [C33](#c33) · cell 59 [markdown]
- [C34](#c34) · cell 59 [markdown]
- [C35](#c35) · cell 59 [markdown]
- [C36](#c36) · cell 59 [markdown]
- [C37](#c37) · cell 59 [markdown]
- [C44](#c44) · cell 63 [markdown]
- [C45](#c45) · cell 63 [markdown]
- [C48](#c48) · cell 65: Biplot
- [C49](#c49) · cell 65: Biplot
- [C50](#c50) · cell 65: Biplot
- [C51](#c51) · cell 65: Biplot
- [C52](#c52) · cell 65: Biplot
- [C53](#c53) · cell 65: Biplot
- [C57](#c57) · cell 69: Invert and normalize the images so they look better
- [C58](#c58) · cell 69: Invert and normalize the images so they look better
- [C59](#c59) · cell 69: Invert and normalize the images so they look better
- [C65](#c65) · cell 72 [markdown]
- [C66](#c66) · cell 72 [markdown]
- [C67](#c67) · cell 72: keep two rows drawn at random from each class

## Changes

<a id="c1"></a>
### C1 · cell 1: Visualization (Revisited) · dropdown

baseline L38 → branch L38 · mirror of the next code cell (hard rule 3)

```diff
- # import pandas as pd
+ # import polars as pl
```

**Why:** Setup-cell mirror: `import pandas as pd` → `import polars as pl`. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** same — the mirrored cell is `remove-input` setup and emits no output.

<a id="c2"></a>
### C2 · cell 2 [code] · code

baseline L47 → branch L47

```diff
- import pandas as pd
+ import polars as pl
```

**Why:** The chapter's one library import. `pd` had no other use in the chapter once the `sns.load_dataset` wrap below was in place.
**Output:** same — import cell, no committed output.

<a id="c3"></a>
### C3 · cell 3 [markdown] · dropdown

baseline L56 → branch L56 · mirror of the next code cell (hard rule 3)

```diff
- # mpg = sns.load_dataset("mpg").dropna()
+ # mpg = pl.from_pandas(sns.load_dataset("mpg")).drop_nulls()
```

**Why:** `sns.load_dataset` returns a *pandas* DataFrame, so this line was a pandas site that no `pd.`/`import pandas` scan can find; wrapped in `pl.from_pandas(...)`, and `dropna()` → `drop_nulls()`. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — Polars render; see C77.

<a id="c4"></a>
### C4 · cell 4 [code] · code

baseline L61 → branch L61

```diff
- # %% tags=["remove-input"]
- mpg = sns.load_dataset("mpg").dropna()
+ # %% tags=["remove-input", "remove-output"]
+ mpg = pl.from_pandas(sns.load_dataset("mpg")).drop_nulls()
```

**Why:** Same edit as C3 on the code cell. The tag list also gained `remove-output` because the cell's committed output now renders inside the tab-set added at C5 rather than directly beneath the cell.
**Output:** differs — Polars render, same rows. Row count is unchanged at 392: `pl.from_pandas` defaults to `nan_to_null=True`, so the six NaN `horsepower` values arrive as nulls and `drop_nulls()` removes exactly the rows `dropna()` removed. Verified live (polars 1.43.1): `(392, 9)` both ways.

<a id="c5"></a>
### C5 · cell 4 [code] · tab-twins

baseline L64 → branch L64 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 63aeae39 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # mpg = pl.from_pandas(sns.load_dataset("mpg")).drop_nulls()
+ # mpg.head()
+ # ```
+ #
+ # ```text
+ # shape: (5, 9)
+ # ┌──────┬───────────┬─────────────┬────────────┬───┬─────────────┬────────────┬────────┬────────────┐
+ # │ mpg  ┆ cylinders ┆ displacemen ┆ horsepower ┆ … ┆ acceleratio ┆ model_year ┆ origin ┆ name       │
+ # │ ---  ┆ ---       ┆ t           ┆ ---        ┆   ┆ n           ┆ ---        ┆ ---    ┆ ---        │
+ # │ f64  ┆ i64       ┆ ---         ┆ f64        ┆   ┆ ---         ┆ i64        ┆ str    ┆ str        │
+ # │      ┆           ┆ f64         ┆            ┆   ┆ f64         ┆            ┆        ┆            │
+ # ╞══════╪═══════════╪═════════════╪════════════╪═══╪═════════════╪════════════╪════════╪════════════╡
+ # │ 18.0 ┆ 8         ┆ 307.0       ┆ 130.0      ┆ … ┆ 12.0        ┆ 70         ┆ usa    ┆ chevrolet  │
+ # │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ chevelle   │
+ # │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ malibu     │
+ # │ 15.0 ┆ 8         ┆ 350.0       ┆ 165.0      ┆ … ┆ 11.5        ┆ 70         ┆ usa    ┆ buick      │
+ # │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ skylark    │
+ # │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ 320        │
+ # │ 18.0 ┆ 8         ┆ 318.0       ┆ 150.0      ┆ … ┆ 11.0        ┆ 70         ┆ usa    ┆ plymouth   │
+ # │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ satellite  │
+ # │ 16.0 ┆ 8         ┆ 304.0       ┆ 150.0      ┆ … ┆ 12.0        ┆ 70         ┆ usa    ┆ amc rebel  │
+ # │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ sst        │
+ # │ 17.0 ┆ 8         ┆ 302.0       ┆ 140.0      ┆ … ┆ 10.5        ┆ 70         ┆ usa    ┆ ford       │
+ # │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ torino     │
+ # └──────┴───────────┴─────────────┴────────────┴───┴─────────────┴────────────┴────────┴────────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # mpg = sns.load_dataset("mpg").dropna()
+ # mpg.head()
+ … 20 more lines
```

**Why:** New pandas/Polars comparison tab-set. The pandas pane carries the baseline's source and its committed output verbatim; the Polars pane carries the converted pair.
**Output:** differs — same five cars, same values. Polars prints a `shape:` header and a dtype row and wraps the `name` column; pandas prints an index and splits the frame into two blocks.

<a id="c6"></a>
### C6 · cell 16: Dimensionality · prose · **REVIEW**

baseline L132 → branch L192

```diff
- # What about Dataset 3 below?
+ # What about Dataset 4 below?
```

**Why:** The figure is `images/dataset4.png`, whose own caption reads "Dataset 4" and which has four columns, so the baseline sentence named the wrong dataset. CONTRADICTIONS.md §A7 item 5 — **pre-existing**, present verbatim in `887a578b0a4b`; nothing in the conversion produced or required it.
**Verdict:** optional
**Minimal alternative:** revert to "Dataset 3" and ship the correction against `main` with the rest of §A. C6 and C7 are one fix and should move together.

<a id="c7"></a>
### C7 · cell 16: Dimensionality · prose · **REVIEW**

baseline L134 → branch L194

```diff
- # ![Dataset 3 has three columns: height (in), weight (kg), weight (lbs), and age](images/dataset4.png)
+ # ![Dataset 4 has four columns: height (in), weight (kg), weight (lbs), and age.](images/dataset4.png)
```

**Why:** Alt text for the same figure: it said "three columns" and then listed four, and called it Dataset 3. Corrected to four columns and Dataset 4. CONTRADICTIONS.md §A7 item 5, pre-existing.
**Verdict:** optional
**Minimal alternative:** as C6 — revert both or ship both; a screen-reader user is the one who most needs this one, so if only one survives, keep this.

<a id="c8"></a>
### C8 · cell 17: [Optional for Spring 26] Singular Value Decomposition (SVD) · prose · **REVIEW**

baseline L414 → branch L474

```diff
- # - **Orthonormal inverse**: If an $m \times n$ matrix $Q$ has orthonormal columns, $QQ^T= Iₘ$ and $Q^TQ=Iₙ$.
+ # - **Orthonormal inverse**: If an $m \times n$ matrix $Q$ has orthonormal columns, then
+ #   $Q^TQ=Iₙ$ always. $QQ^T= Iₘ$ holds only when $Q$ is square — with $m > n$ the columns of $Q$
+ #   span an $n$-dimensional subspace of $\mathbb{R}^m$, and $QQ^T$ is the projection onto it
+ #   rather than the identity.
```

**Why:** The baseline asserted both $QQ^T = I_m$ and $Q^TQ = I_n$ for any $Q$ with orthonormal columns. Only the second holds in general; $QQ^T$ is the projection onto the column space unless $Q$ is square. CONTRADICTIONS.md §A7 item 1 — pre-existing, and unrelated to Polars.
**Verdict:** questionable
**Minimal alternative:** keep the baseline bullet and append one clause — "…and $QQ^T = I_m$ when $Q$ is square". The four-line replacement is now the longest bullet in that list and pushes the section's register toward a proof.

<a id="c9"></a>
### C9 · cell 17: SVD: $U$ · prose · **REVIEW**

baseline L439 → branch L502

```diff
- # - $UU^T = I_n$ and $U^TU = I_d$.
+ # - $U^TU = I_d$. ($UU^T = I_n$ only for the *full* SVD, where $U$ is $n \times n$; the
+ #   `full_matrices=False` form used below gives an $n \times d$ matrix, for which $UU^T$ is a
+ #   projection of rank $d$.)
```

**Why:** The same error restated for the chapter's own $U$, which is $100 \times 4$ under `full_matrices=False` — the form the cell directly below uses. Measured in CONTRADICTIONS.md §A7 item 2: `U.T@U == I_4` is True, `U@U.T == I_100` is False. Pre-existing.
**Verdict:** questionable
**Minimal alternative:** drop the parenthetical and leave the bullet as `$U^TU = I_d$.` The false half is gone either way and the bullet list keeps its shape.

<a id="c10"></a>
### C10 · cell 18 [markdown] · dropdown

baseline L506 → branch L571 · spans code and prose; mirror of the next code cell (hard rule 3)

```diff
+ # import polars as pl
+ # import seaborn as sns
+ # import matplotlib.pyplot as plt
+ # import numpy as np
+ #
+ # np.random.seed(23)  # kallisti
+ #
+ # plt.rcParams["figure.figsize"] = (4, 4)
+ # plt.rcParams["figure.dpi"] = 150
+ # sns.set()
+ #
+ # rectangle = pl.read_csv("data/rectangle_data.csv")
+ # rectangle.head(5)
+ # ```
+ # ````
+ 
+ # %% tags=["remove-input", "remove-output"]
+ import polars as pl
+ import seaborn as sns
+ import matplotlib.pyplot as plt
+ import numpy as np
+ 
+ np.random.seed(23)  # kallisti
+ 
+ plt.rcParams["figure.figsize"] = (4, 4)
+ plt.rcParams["figure.dpi"] = 150
+ sns.set()
+ 
+ rectangle = pl.read_csv("data/rectangle_data.csv")
+ rectangle.head(5)
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 6844db4c -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # import polars as pl
+ # import seaborn as sns
+ # import matplotlib.pyplot as plt
+ … 31 more lines
```

**Why:** Setup mirror for the `rectangle_data` section — the import and `pd.read_csv` → `pl.read_csv`. The hunk is large because the retag to `remove-output` and the new tab-set land in the same region of the percent-format file. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — Polars render of the same five rectangles; see C78.

<a id="c11"></a>
### C11 · cell 20 [markdown] · tab-twins

baseline L520 → branch L656 · spans code and prose

```diff
- # ````
- 
- # %% tags=["remove-input"]
- import pandas as pd
- import seaborn as sns
- import matplotlib.pyplot as plt
- import numpy as np
- 
- np.random.seed(23)  # kallisti
- 
- plt.rcParams["figure.figsize"] = (4, 4)
- plt.rcParams["figure.dpi"] = 150
- sns.set()
- 
- rectangle = pd.read_csv("data/rectangle_data.csv")
- rectangle.head(5)
+ #
+ # ```text
+ #    width  height  area  perimeter
+ # 0      8       6    48         28
+ # 1      2       4     8         12
+ # 2      1       3     3          8
+ # 3      9       3    27         24
+ # 4      9       8    72         34
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** Closing half of that tab-set: the pandas pane holds the baseline's source and its committed table.
**Output:** differs — rendering only. Both panes show the same five rows of `width/height/area/perimeter`.

<a id="c12"></a>
### C12 · cell 26 [code] · code

baseline L553 → branch L685

```diff
- pd.DataFrame(U).head(5)
+ pl.DataFrame(U).head(5)
```

**Why:** `pd.DataFrame(U)` → `pl.DataFrame(U)`. `np.linalg.svd` returns ndarrays either way; only the display wrapper changed.
**Output:** differs — see C79. Headers become `column_0…column_3`, and the fourth column's numbers move (null-space direction, explained there).

<a id="c13"></a>
### C13 · cell 35 [code] · code

baseline L583 → branch L715

```diff
- pd.DataFrame(Vt)
+ pl.DataFrame(Vt)
```

**Why:** Same display-wrapper change for $V^T$.
**Output:** differs — see C82. Values and signs unchanged; Polars prints 6 significant figures where pandas printed scientific notation.

<a id="c14"></a>
### C14 · cell 37 [code] · tab-twins

baseline L588 → branch L720 · spans code and prose

```diff
- # %%
- pd.DataFrame(U @ Sm @ Vt).head(5)
+ # %% tags=["remove-input", "remove-output"]
+ pl.DataFrame(U @ Sm @ Vt).head(5)
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 39859318 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # pl.DataFrame(U @ Sm @ Vt).head(5)
+ # ```
+ #
+ # ```text
+ # shape: (5, 4)
+ # ┌──────────┬──────────┬──────────┬──────────┐
+ # │ column_0 ┆ column_1 ┆ column_2 ┆ column_3 │
+ # │ ---      ┆ ---      ┆ ---      ┆ ---      │
+ # │ f64      ┆ f64      ┆ f64      ┆ f64      │
+ # ╞══════════╪══════════╪══════════╪══════════╡
+ # │ 8.0      ┆ 6.0      ┆ 48.0     ┆ 28.0     │
+ # │ 2.0      ┆ 4.0      ┆ 8.0      ┆ 12.0     │
+ # │ 1.0      ┆ 3.0      ┆ 3.0      ┆ 8.0      │
+ # │ 9.0      ┆ 3.0      ┆ 27.0     ┆ 24.0     │
+ # │ 9.0      ┆ 8.0      ┆ 72.0     ┆ 34.0     │
+ # └──────────┴──────────┴──────────┴──────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # pd.DataFrame(U @ Sm @ Vt).head(5)
+ # ```
+ #
+ # ```text
+ #      0    1     2     3
+ # 0  8.0  6.0  48.0  28.0
+ # 1  2.0  4.0   8.0  12.0
+ # 2  1.0  3.0   3.0   8.0
+ # 3  9.0  3.0  27.0  24.0
+ … 5 more lines
```

**Why:** Display wrapper on the reconstruction, plus `remove-input`/`remove-output` so the output renders inside the new tab-set.
**Output:** differs — see C83. Reconstructed values are identical; only the column labels (`column_0…` vs `0…`) and the frame render differ.

<a id="c15"></a>
### C15 · cell 39: Code Demo · prose · **REVIEW**

baseline L697 → branch L872

```diff
- # 1. Center $X$ by subtracting the mean from each column. Notice how we specify `axis=0` so that the mean is computed per column.
+ # 1. Center $X$ by subtracting the mean from each column. `pl.all().mean()` produces one mean per column.
```

**Why:** The sentence explained pandas' `axis=0`, which the converted cell no longer contains: `rectangle.select(pl.all() - pl.all().mean())` is per-column by construction, so there is no axis argument left to point at. Re-aimed at the expression that replaced it.
**Verdict:** necessary

<a id="c16"></a>
### C16 · cell 40 [code] · code

baseline L699 → branch L874

```diff
- # %%
- centered_df = rectangle - np.mean(rectangle, axis=0)
+ # %% tags=["remove-input", "remove-output"]
+ centered_df = rectangle.select(pl.all() - pl.all().mean())
```

**Why:** `rectangle - np.mean(rectangle, axis=0)` → `rectangle.select(pl.all() - pl.all().mean())`. `np.mean(frame, axis=0)` is in the NumPy reduction family that rejects Polars' signature, and "subtract the mean of each attribute column" is step 1 of the procedure this section teaches, so the expression stays in Polars rather than crossing to NumPy. Verified live: the centred matrix is elementwise equal to the pandas one.
**Output:** differs — see C84. Same values, Polars render.

<a id="c17"></a>
### C17 · cell 40 [code] · tab-twins

baseline L702 → branch L877 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 30d7edc2 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # centered_df = rectangle.select(pl.all() - pl.all().mean())
+ # centered_df.head(5)
+ # ```
+ #
+ # ```text
+ # shape: (5, 4)
+ # ┌───────┬────────┬────────┬───────────┐
+ # │ width ┆ height ┆ area   ┆ perimeter │
+ # │ ---   ┆ ---    ┆ ---    ┆ ---       │
+ # │ f64   ┆ f64    ┆ f64    ┆ f64       │
+ # ╞═══════╪════════╪════════╪═══════════╡
+ # │ 2.97  ┆ 1.35   ┆ 24.78  ┆ 8.64      │
+ # │ -3.03 ┆ -0.65  ┆ -15.22 ┆ -7.36     │
+ # │ -4.03 ┆ -1.65  ┆ -20.22 ┆ -11.36    │
+ # │ 3.97  ┆ -1.65  ┆ 3.78   ┆ 4.64      │
+ # │ 3.97  ┆ 3.35   ┆ 48.78  ┆ 14.64     │
+ # └───────┴────────┴────────┴───────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # centered_df = rectangle - np.mean(rectangle, axis=0)
+ # centered_df.head(5)
+ # ```
+ #
+ # ```text
+ #    width  height   area  perimeter
+ # 0   2.97    1.35  24.78       8.64
+ # 1  -3.03   -0.65 -15.22      -7.36
+ # 2  -4.03   -1.65 -20.22     -11.36
+ # 3   3.97   -1.65   3.78       4.64
+ … 5 more lines
```

**Why:** Comparison tab-set for the centring step.
**Output:** differs — rendering only; both panes carry the same centred values at the printed precision.

<a id="c18"></a>
### C18 · cell 43 [code] · code

baseline L708 → branch L928

```diff
- Sm = pd.DataFrame(np.diag(np.round(S, 1)))
+ Sm = pl.DataFrame(np.diag(np.round(S, 1)))
```

**Why:** `pd.DataFrame(np.diag(np.round(S, 1)))` → `pl.DataFrame(...)`; display wrapper only.
**Output:** same — this cell (`23f6418b`) carries no committed output, so nothing about it reaches the page.

<a id="c19"></a>
### C19 · cell 45 [code] · metadata

baseline L713 → branch L933

```diff
- # %%
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c20"></a>
### C20 · cell 45 [code] · tab-twins

baseline L715 → branch L935 · spans code and prose

```diff
- pd.DataFrame(two_PCs).head()
+ pl.DataFrame(two_PCs).head()
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 2914fede -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # two_PCs = Vt.T[:, :2]
+ # pl.DataFrame(two_PCs).head()
+ # ```
+ #
+ # ```text
+ # shape: (4, 2)
+ # ┌───────────┬───────────┐
+ # │ column_0  ┆ column_1  │
+ # │ ---       ┆ ---       │
+ # │ f64       ┆ f64       │
+ # ╞═══════════╪═══════════╡
+ # │ -0.098631 ┆ 0.66846   │
+ # │ -0.072956 ┆ -0.374186 │
+ # │ -0.931226 ┆ -0.258375 │
+ # │ -0.343173 ┆ 0.588548  │
+ # └───────────┴───────────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # two_PCs = Vt.T[:, :2]
+ # pd.DataFrame(two_PCs).head()
+ # ```
+ #
+ # ```text
+ #           0         1
+ # 0 -0.098631  0.668460
+ # 1 -0.072956 -0.374186
+ # 2 -0.931226 -0.258375
+ # 3 -0.343173  0.588548
+ … 4 more lines
```

**Why:** `pd.DataFrame(two_PCs).head()` → `pl.DataFrame(...)`, plus the comparison tab-set that now carries the output.
**Output:** differs — see C85. The two principal-component columns are unchanged, including their signs.

<a id="c21"></a>
### C21 · cell 47: Biplots · prose · **REVIEW**

baseline L760 → branch L1023

```diff
- # Biplots superimpose the **directions** onto the plot of PC1 vs. PC2, where vector $j$ corresponds to the direction for feature $j$ (e.g., $v_{1j}, v_{2j}$). There are several ways to scale biplot vectors — in this course, we plot the direction itself. For other scalings, which can lead to more interpretable directions/loadings, see [SAS biplots](https://blogs.sas.com/content/iml/2019/11/06/what-are-biplots.html).
+ # Biplots superimpose the **directions** onto the plot of PC1 vs. PC2, where vector $j$ corresponds to the direction for feature $j$ (e.g., $v_{1j}, v_{2j}$). There are several ways to scale biplot vectors; the cell below scales each axis by the square root of its singular value, plotting $(\sqrt{s_1}\,v_{1j}, \sqrt{s_2}\,v_{2j})$. Because the two axes are scaled by different amounts, an arrow's *length* becomes readable against the spread of the points, at the cost of turning it slightly away from the raw direction. For other scalings, which can lead to more interpretable directions/loadings, see [SAS biplots](https://blogs.sas.com/content/iml/2019/11/06/what-are-biplots.html).
```

**Why:** The baseline stated a course policy — "in this course, we plot the direction itself" — that the cell below contradicts: it plots `sqrt(s[0])*vt[0]` against `sqrt(s[1])*vt[1]`, and because the two axes are scaled by different constants the arrows are rotated by up to 19°. CONTRADICTIONS.md §A7 item 4 — pre-existing. The rewrite describes the scaling the code performs and what it buys.
**Verdict:** questionable
**Minimal alternative:** the smaller fix is to delete the false clause and keep the rest: "There are several ways to scale biplot vectors; the cell below scales each axis by the square root of its singular value." The added sentence about readable arrow length at the cost of direction is new editorial content, and staff may prefer to write that themselves — or to change the code so the prose becomes true again.

<a id="c22"></a>
### C22 · cell 47: Example: House of Representatives Voting · dropdown

baseline L782 → branch L1045 · spans code and prose; mirror of the next code cell (hard rule 3)

```diff
+ # import polars as pl
+ # import seaborn as sns
+ # import matplotlib.pyplot as plt
+ # import numpy as np
+ # import yaml
+ # from datetime import datetime
+ # import plotly.express as px
+ # import plotly.graph_objects as go
+ #
+ #
+ # votes = pl.read_csv("data/votes.csv")
+ # votes = votes.cast({"roll call": pl.String})
+ # votes.head()
+ # ```
+ # ````
+ 
+ # %% tags=["remove-input", "remove-output"]
+ import polars as pl
+ import seaborn as sns
+ import matplotlib.pyplot as plt
+ import numpy as np
+ import yaml
+ from datetime import datetime
+ import plotly.express as px
+ import plotly.graph_objects as go
+ 
+ 
+ votes = pl.read_csv("data/votes.csv")
+ votes = votes.cast({"roll call": pl.String})
+ votes.head()
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 66688b1c -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # import polars as pl
+ # import seaborn as sns
+ # import matplotlib.pyplot as plt
+ … 31 more lines
```

**Why:** Setup mirror for the voting section: import, `pd.read_csv` → `pl.read_csv`, and `astype({"roll call": str})` → `cast({"roll call": pl.String})`. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — Polars render of `votes.head()`; see C86.

<a id="c23"></a>
### C23 · cell 49 [markdown] · dropdown

baseline L796 → branch L1130 · mirror of the next code cell (hard rule 3)

```diff
+ #
+ # ```text
+ #   chamber  session roll call   member        vote
+ # 0   House        1       555  A000374  Not Voting
+ # 1   House        1       555  A000370         Yes
+ # 2   House        1       555  A000055          No
+ # 3   House        1       555  A000371         Yes
+ # 4   House        1       555  A000372          No
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
+ 
+ # %% [markdown]
+ # Suppose we pivot this table to group each legislator and their voting pattern across every (roll call) vote in this month. We mark 1 if the legislator voted Yes ("yea"), and 0 otherwise ("No", "nay", no vote, speaker, etc.). Each legislator becomes one row, labelled by the `member` column, and each roll call becomes a column of 0s and 1s.
+ #
+ # ````{dropdown} Click to see the code
+ # ```python
+ # # 1 when the member's recorded vote on that roll call is a Yes
+ # was_yes = (pl.element().first() == "Yes").cast(pl.Int64)
+ #
+ # vote_pivot = votes.pivot(
+ #     on="roll call",
+ #     index="member",
+ #     values="vote",
+ #     aggregate_function=was_yes,
+ #     sort_columns=True,
+ # ).fill_null(0).sort("member")  # row order fixes the sign of each principal component
+ # print(vote_pivot.shape)
+ # vote_pivot.head()
+ # ```
```

**Why:** Mirror of the pivot cell. It repeats the Polars `pivot` call, including the inline comment that records why `.sort("member")` is there. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — see C87 (shape line and `member` column).

<a id="c24"></a>
### C24 · cell 51 [code] · code

baseline L798 → branch L1163

```diff
- # %% tags=["remove-input"]
- import pandas as pd
- import seaborn as sns
- import matplotlib.pyplot as plt
- import numpy as np
- import yaml
- from datetime import datetime
- import plotly.express as px
- import plotly.graph_objects as go
+ # %% tags=["remove-input", "remove-output"]
+ # 1 when the member's recorded vote on that roll call is a Yes
+ was_yes = (pl.element().first() == "Yes").cast(pl.Int64)
```

**Why:** The pandas helper `def was_yes(s): return 1 if s.iloc[0] == "Yes" else 0` becomes a Polars expression, `(pl.element().first() == "Yes").cast(pl.Int64)`, which `pivot(aggregate_function=...)` accepts directly — no lambda, no per-group Series. The hunk looks large because the import block that used to head this cell moved into the setup cell above.
**Output:** differs — see C87. The 0/1 matrix is identical to the baseline's.

<a id="c25"></a>
### C25 · cell 51 [code] · code

baseline L808 → branch L1167

```diff
- 
- votes = pd.read_csv("data/votes.csv")
- votes = votes.astype({"roll call": str})
- votes.head()
- 
+ vote_pivot = votes.pivot(
+     on="roll call",
+     index="member",
+     values="vote",
+     aggregate_function=was_yes,
+     sort_columns=True,
+ ).fill_null(0).sort("member")  # row order fixes the sign of each principal component
+ print(vote_pivot.shape)
+ vote_pivot.head()
```

**Why:** `pivot_table(index=, columns=, values=, aggfunc=, fill_value=0)` → `pivot(index=, on=, values=, aggregate_function=)` + `.fill_null(0)`. Two keywords are chart content rather than pandas-matching: `sort_columns=True` keeps roll calls 515–555 in ordinal order (they are the x-axis of two bar charts; Polars would otherwise emit CSV order, 555 first), and `.sort("member")` fixes the row permutation that LAPACK's sign choice depends on — without it PC1 flips and the live biplot mirrors the chapter's static figures. See CONVERSIONS.md "The sign flip".
**Output:** differs — see C87: `(441, 42)` instead of `(441, 41)`, `member` as the first column. Same 441 legislators, same 41 roll calls, same values. With the member sort the singular values are bit-identical to the pandas path.

<a id="c26"></a>
### C26 · cell 52 [markdown] · tab-twins

baseline L815 → branch L1178

```diff
- # Suppose we pivot this table to group each legislator and their voting pattern across every (roll call) vote in this month. We mark 1 if the legislator voted Yes ("yea"), and 0 otherwise ("No", "nay", no vote, speaker, etc.).
+ # <!-- tab-twins:begin 5880e99c -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # # 1 when the member's recorded vote on that roll call is a Yes
+ # was_yes = (pl.element().first() == "Yes").cast(pl.Int64)
```

**Why:** Opening of the comparison tab-set for the pivot; the prose sentence that used to sit here moved down (see C29).
**Output:** differs — see C87.

<a id="c27"></a>
### C27 · cell 52: 1 when the member's recorded vote on that roll call is a Yes · tab-twins

baseline L817 → branch L1186

```diff
- # ````{dropdown} Click to see the code
+ # vote_pivot = votes.pivot(
+ #     on="roll call",
+ #     index="member",
+ #     values="vote",
+ #     aggregate_function=was_yes,
+ #     sort_columns=True,
+ # ).fill_null(0).sort("member")  # row order fixes the sign of each principal component
+ # print(vote_pivot.shape)
+ # vote_pivot.head()
+ # ```
+ #
+ # ```text
+ # (441, 42)
+ # shape: (5, 42)
+ # ┌─────────┬─────┬─────┬─────┬───┬─────┬─────┬─────┬─────┐
+ # │ member  ┆ 515 ┆ 516 ┆ 517 ┆ … ┆ 552 ┆ 553 ┆ 554 ┆ 555 │
+ # │ ---     ┆ --- ┆ --- ┆ --- ┆   ┆ --- ┆ --- ┆ --- ┆ --- │
+ # │ str     ┆ i64 ┆ i64 ┆ i64 ┆   ┆ i64 ┆ i64 ┆ i64 ┆ i64 │
+ # ╞═════════╪═════╪═════╪═════╪═══╪═════╪═════╪═════╪═════╡
+ # │ A000055 ┆ 1   ┆ 0   ┆ 0   ┆ … ┆ 0   ┆ 0   ┆ 1   ┆ 0   │
+ # │ A000367 ┆ 0   ┆ 0   ┆ 0   ┆ … ┆ 1   ┆ 1   ┆ 0   ┆ 1   │
+ # │ A000369 ┆ 1   ┆ 1   ┆ 0   ┆ … ┆ 0   ┆ 0   ┆ 1   ┆ 0   │
+ # │ A000370 ┆ 1   ┆ 1   ┆ 1   ┆ … ┆ 1   ┆ 1   ┆ 1   ┆ 1   │
+ # │ A000371 ┆ 1   ┆ 1   ┆ 1   ┆ … ┆ 1   ┆ 1   ┆ 1   ┆ 1   │
+ # └─────────┴─────┴─────┴─────┴───┴─────┴─────┴─────┴─────┘
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
```

**Why:** Polars pane of the pivot tab-set, carrying the converted call and its executed output.
**Output:** differs — the Polars pane's shape line reads `(441, 42)`; the pandas pane's reads `(441, 41)`. C29 is the paragraph that reconciles them.

<a id="c28"></a>
### C28 · cell 52: 1 when the member's recorded vote on that roll call is a Yes · tab-twins

baseline L829 → branch L1227 · spans code and prose

```diff
- # ````
- 
- # %% tags=["remove-input"]
- def was_yes(s):
-     return 1 if s.iloc[0] == "Yes" else 0
- 
- 
- vote_pivot = votes.pivot_table(
-     index="member", columns="roll call", values="vote", aggfunc=was_yes, fill_value=0
- )
- print(vote_pivot.shape)
- vote_pivot.head()
+ #
+ # ```text
+ # (441, 41)
+ # roll call  515  516  517  518  519  520  521  522  523  524  ...  546  547  \
+ # member                                                       ...
+ # A000055      1    0    0    0    1    1    0    1    1    1  ...    0    0
+ # A000367      0    0    0    0    0    0    0    0    0    0  ...    0    1
+ # A000369      1    1    0    0    1    1    0    1    1    1  ...    0    0
+ # A000370      1    1    1    1    1    0    1    0    0    0  ...    1    1
+ # A000371      1    1    1    1    1    0    1    0    0    0  ...    1    1
+ #
+ # roll call  548  549  550  551  552  553  554  555
+ # member
+ # A000055      1    0    0    1    0    0    1    0
+ # A000367      1    1    1    0    1    1    0    1
+ # A000369      1    0    0    1    0    0    1    0
+ # A000370      1    1    1    0    1    1    1    1
+ # A000371      1    1    1    0    1    1    1    1
+ #
+ # [5 rows x 41 columns]
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** pandas pane of the same tab-set: the baseline's `was_yes` function, its `pivot_table` call, and its committed output verbatim.
**Output:** differs — the pandas pane reproduces the baseline's index-labelled, column-wrapped table.

<a id="c29"></a>
### C29 · cell 53 [markdown] · prose · **REVIEW**

baseline L843 → branch L1253

```diff
+ # The two shapes differ by one, and the difference is bookkeeping rather than data. Polars leaves
+ # `member` as an ordinary column, so the frame is 41 roll calls *plus* the labels; pandas moves
+ # `member` into the index, where it stops being counted. Both tables hold the same 441 legislators
+ # and the same 41 votes.
+ #
```

**Why:** New paragraph, added because the conversion moved a number the reader can see: `print(vote_pivot.shape)` went from `(441, 41)` to `(441, 42)`. It explains that `member` is an ordinary column in Polars and an index in pandas, so the frame counts one more column while holding the same data.
**Verdict:** questionable
**Minimal alternative:** the house style asks for sentences about what Polars does rather than what pandas did (`data100-textbook-voice`, "Re-authoring prose"), and this is the one paragraph in the chapter that breaks it. A one-sentence version — "`member` is an ordinary column here, so the frame reports 42: the 41 roll calls plus the labels." — reads the number without the migration note. It sits directly under a tab-set that shows both libraries, which is the argument for keeping it as written.

<a id="c30"></a>
### C30 · cell 53: PCA with SVD · prose · **REVIEW**

baseline L846 → branch L1261

```diff
- # While we could consider loading information about the legislator, such as their party, and see how this relates to their voting pattern, it turns out that we can do a lot with PCA to cluster legislators by how they vote. Let's calculate the principal components using the SVD method.
+ # While we could consider loading information about the legislator, such as their party, and see how this relates to their voting pattern, it turns out that we can do a lot with PCA to cluster legislators by how they vote. Let's calculate the principal components using the SVD method. `pl.exclude("member")` selects every roll call column, so we subtract each column's own mean and leave the member labels out of the matrix we decompose.
```

**Why:** Added clause naming `pl.exclude("member")`, because the next cell has to keep the member labels out of the matrix it decomposes — centring them along with the 41 vote columns would corrupt the SVD and every figure downstream with all gates green. CONVERSIONS.md records that `pl.exclude` appears in this chapter and nowhere else in the book, so a reader had the pattern but no term to search for.
**Verdict:** optional
**Minimal alternative:** move it to an inline comment on the code line and leave the paragraph as the baseline had it; the sentence is now three clauses long and the last one restates the section heading.

<a id="c31"></a>
### C31 · cell 54 [code] · code

baseline L849 → branch L1264

```diff
- vote_pivot_centered = vote_pivot - np.mean(vote_pivot, axis=0)
+ vote_pivot_centered = vote_pivot.select(pl.exclude("member") - pl.exclude("member").mean())
```

**Why:** `vote_pivot - np.mean(vote_pivot, axis=0)` → `vote_pivot.select(pl.exclude("member") - pl.exclude("member").mean())`. The pandas version could subtract a column mean from every column because `member` was the index; here it is data, so it has to be excluded explicitly.
**Output:** same — this cell (`a30cd5d8`) carries no committed output. The centred matrix it produces is elementwise equal to the baseline's.

<a id="c32"></a>
### C32 · cell 58 [code] · code

baseline L866 → branch L1281

```diff
- vote_2d = pd.DataFrame(index=vote_pivot_centered.index)
- vote_2d[["z1", "z2", "z3"]] = (u * s)[:, :3]
+ Z = (u * s)[:, :3]
+ vote_2d = pl.DataFrame(
+     {"member": vote_pivot["member"], "z1": Z[:, 0], "z2": Z[:, 1], "z3": Z[:, 2]}
+ )
```

**Why:** `pd.DataFrame(index=vote_pivot_centered.index)` followed by a three-column assignment has no Polars form — there is no index to seed a frame from. Rebuilt as an explicit frame with `member` taken from `vote_pivot` and `z1/z2/z3` sliced out of `u * s`. Row order is positional on both sides, which is why the pivot's `.sort("member")` matters here too.
**Output:** same — no committed output on this cell. The scatter it feeds (`52aa5028`) is unchanged apart from ≤1.7e-14 relative drift.

<a id="c33"></a>
### C33 · cell 59 [markdown] · dropdown

baseline L887 → branch L1304 · mirror of the next code cell (hard rule 3)

```diff
- # legs = pd.DataFrame(
- #     columns=[
+ # legs = pl.DataFrame(
+ #     schema=[
```

**Why:** Mirror of the legislator-loading cell: `pd.DataFrame(columns=…, data=…)` → `pl.DataFrame(schema=…, data=…)`. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — the mirrored cell draws the 3-D PCA scatter (`8f3d5894`), unchanged apart from ≤3.4e-14 relative drift.

<a id="c34"></a>
### C34 · cell 59 [markdown] · dropdown

baseline L911 → branch L1328 · mirror of the next code cell (hard rule 3)

```diff
+ #     orient="row",
```

**Why:** `orient="row"` added: a list-of-lists reads as *columns* in Polars, where pandas read it as rows, so without it the frame would be transposed. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — as C33; the figure is unchanged.

<a id="c35"></a>
### C35 · cell 59 [markdown] · dropdown

baseline L912 → branch L1330 · mirror of the next code cell (hard rule 3)

```diff
- # legs["age"] = 2024 - legs["birthday"].dt.year
- # legs.set_index("leg_id")
- # legs.sort_index()
+ # legs = legs.with_columns((2024 - pl.col("birthday").dt.year()).alias("age"))
```

**Why:** `legs["age"] = …` → `with_columns((2024 - pl.col("birthday").dt.year()).alias("age"))` (`.dt.year` is a method, not a property, in Polars). The two lines below it — `legs.set_index("leg_id")` and `legs.sort_index()` — were **no-ops in the baseline**: both returned new frames that were discarded, so they were deleted rather than translated. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — as C33; nothing downstream read the discarded frames.

<a id="c36"></a>
### C36 · cell 59 [markdown] · dropdown

baseline L916 → branch L1332 · mirror of the next code cell (hard rule 3)

```diff
- # vote_2d = vote_2d.join(legs.set_index("leg_id")).dropna()
+ # vote_2d = vote_2d.join(
+ #     legs, left_on="member", right_on="leg_id", how="inner", maintain_order="left"
+ # )
```

**Why:** `vote_2d.join(legs.set_index("leg_id")).dropna()` was an index-alignment join. Rewritten as an explicit key join; `maintain_order="left"` is load-bearing, because three `np.random.normal` jitter columns are attached positionally immediately afterwards. CONVERSIONS.md records 439 rows either way, so the `.dropna()` was doing an inner join's work and nothing else. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — as C33; same 439 legislators plotted.

<a id="c37"></a>
### C37 · cell 59 [markdown] · dropdown

baseline L919 → branch L1337 · mirror of the next code cell (hard rule 3)

```diff
- # vote_2d["z1_jittered"] = vote_2d["z1"] + np.random.normal(0, 0.1, len(vote_2d))
- # vote_2d["z2_jittered"] = vote_2d["z2"] + np.random.normal(0, 0.1, len(vote_2d))
- # vote_2d["z3_jittered"] = vote_2d["z3"] + np.random.normal(0, 0.1, len(vote_2d))
+ # vote_2d = vote_2d.with_columns(
+ #     z1_jittered=pl.col("z1") + pl.Series(np.random.normal(0, 0.1, len(vote_2d))),
+ #     z2_jittered=pl.col("z2") + pl.Series(np.random.normal(0, 0.1, len(vote_2d))),
+ #     z3_jittered=pl.col("z3") + pl.Series(np.random.normal(0, 0.1, len(vote_2d))),
+ # )
```

**Why:** Three `df["col"] = …` assignments → one `with_columns` with keyword aliases. Same three `np.random.normal` draws in the same order under the same `np.random.seed(42)`. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — as C33; the jitter is identical.

<a id="c38"></a>
### C38 · cell 60 [code] · code

baseline L939 → branch L1359

```diff
- legs = pd.DataFrame(
-     columns=[
+ legs = pl.DataFrame(
+     schema=[
```

**Why:** Code half of C33 — `pd.DataFrame(columns=…)` → `pl.DataFrame(schema=…)`.
**Output:** differs — figure only; ≤3.4e-14 relative drift, no sign change.

<a id="c39"></a>
### C39 · cell 60 [code] · code

baseline L963 → branch L1383

```diff
+     orient="row",
```

**Why:** Code half of C34 — `orient="row"` for the list-of-lists.
**Output:** differs — as C38.

<a id="c40"></a>
### C40 · cell 60 [code] · code

baseline L964 → branch L1385

```diff
- legs["age"] = 2024 - legs["birthday"].dt.year
- legs.set_index("leg_id")
- legs.sort_index()
+ legs = legs.with_columns((2024 - pl.col("birthday").dt.year()).alias("age"))
```

**Why:** Code half of C35 — `with_columns` for `age`, and the two discarded `set_index`/`sort_index` no-ops deleted.
**Output:** differs — as C38.

<a id="c41"></a>
### C41 · cell 60 [code] · code

baseline L968 → branch L1387

```diff
- vote_2d = vote_2d.join(legs.set_index("leg_id")).dropna()
+ vote_2d = vote_2d.join(
+     legs, left_on="member", right_on="leg_id", how="inner", maintain_order="left"
+ )
```

**Why:** Code half of C36 — the index-alignment join made explicit, with `maintain_order="left"`.
**Output:** differs — as C38.

<a id="c42"></a>
### C42 · cell 60 [code] · code

baseline L971 → branch L1392

```diff
- vote_2d["z1_jittered"] = vote_2d["z1"] + np.random.normal(0, 0.1, len(vote_2d))
- vote_2d["z2_jittered"] = vote_2d["z2"] + np.random.normal(0, 0.1, len(vote_2d))
- vote_2d["z3_jittered"] = vote_2d["z3"] + np.random.normal(0, 0.1, len(vote_2d))
+ vote_2d = vote_2d.with_columns(
+     z1_jittered=pl.col("z1") + pl.Series(np.random.normal(0, 0.1, len(vote_2d))),
+     z2_jittered=pl.col("z2") + pl.Series(np.random.normal(0, 0.1, len(vote_2d))),
+     z3_jittered=pl.col("z3") + pl.Series(np.random.normal(0, 0.1, len(vote_2d))),
+ )
```

**Why:** Code half of C37 — three assignments folded into one `with_columns`.
**Output:** differs — as C38.

<a id="c43"></a>
### C43 · cell 61 [markdown] · prose · **REVIEW**

baseline L991 → branch L1414

```diff
- # vote_2d["num votes"] = votes[votes["vote"].isin(["Yes", "No"])].groupby("member").size()
- # vote_2d.dropna(inplace=True)
+ # num_votes = votes.filter(pl.col("vote").is_in(["Yes", "No"])).group_by("member").agg(pl.len().alias("num votes"))
+ # vote_2d = vote_2d.join(num_votes, on="member", how="inner")
```

**Why:** `groupby("member").size()` assigned onto an index-aligned column, plus `dropna(inplace=True)`, becomes a `group_by(...).agg(pl.len().alias("num votes"))` and an inner join — there is no index to align on and nothing is mutated in place. This hunk sits inside an HTML-commented block (`<!-- ### Analysis: Regular Voters … -->`), so no reader sees it; it was converted so that no pandas survives under `content/`.
**Verdict:** necessary

<a id="c44"></a>
### C44 · cell 63 [markdown] · dropdown

baseline L1012 → branch L1435 · mirror of the next code cell (hard rule 3)

```diff
- #     vote_pivot_centered.join(legs.set_index("leg_id")["party"])
- #     .groupby("party")
+ #     vote_pivot_centered.with_columns(member=vote_pivot["member"])
+ #     .join(legs.select("leg_id", "party"), left_on="member", right_on="leg_id")
+ #     .drop("member")
+ #     .group_by("party")
```

**Why:** Mirror of the party-means cell. The pandas version joined a Series onto the centred frame by index; here `member` is re-attached, joined on explicitly, then dropped before the group-by. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** same — the figure this mirrors (`d1903691`) is **byte-identical** to the baseline apart from plotly serialising two template values as `0.0` instead of `0`. Verified.

<a id="c45"></a>
### C45 · cell 63 [markdown] · dropdown

baseline L1015 → branch L1440 · mirror of the next code cell (hard rule 3)

```diff
- #     .T.reset_index()
- #     .rename(columns={"index": "call"})
- #     .melt("call")
+ #     .sort("party")
+ #     .unpivot(index="party", variable_name="call", value_name="value")
```

**Why:** `.T.reset_index().rename(columns={"index": "call"}).melt("call")` existed only to get roll calls into rows so `melt` could work; `unpivot(index="party", …)` does it in one step. `.sort("party")` added because Polars guarantees no group order and this drives facet-row order on a published figure. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** same — as C44, the figure is unchanged.

<a id="c46"></a>
### C46 · cell 64 [code] · code

baseline L1029 → branch L1453

```diff
-     vote_pivot_centered.join(legs.set_index("leg_id")["party"])
-     .groupby("party")
+     vote_pivot_centered.with_columns(member=vote_pivot["member"])
+     .join(legs.select("leg_id", "party"), left_on="member", right_on="leg_id")
+     .drop("member")
+     .group_by("party")
```

**Why:** Code half of C44.
**Output:** same — figure unchanged (see C44).

<a id="c47"></a>
### C47 · cell 64 [code] · code

baseline L1032 → branch L1458

```diff
-     .T.reset_index()
-     .rename(columns={"index": "call"})
-     .melt("call")
+     .sort("party")
+     .unpivot(index="party", variable_name="call", value_name="value")
```

**Why:** Code half of C45 — the transpose disappears into `unpivot`, and `.sort("party")` pins facet order.
**Output:** same — figure unchanged; 123 rows (3 parties × 41 calls), as in pandas.

<a id="c48"></a>
### C48 · cell 65: Biplot · dropdown

baseline L1047 → branch L1472 · mirror of the next code cell (hard rule 3)

```diff
- # loadings = pd.DataFrame(
- #     {"pc1": np.sqrt(s[0]) * vt[0, :], "pc2": np.sqrt(s[1]) * vt[1, :]},
- #     index=vote_pivot_centered.columns,
+ # loadings = pl.DataFrame(
+ #     {
+ #         "call": vote_pivot_centered.columns,
+ #         "pc1": np.sqrt(s[0]) * vt[0, :],
+ #         "pc2": np.sqrt(s[1]) * vt[1, :],
+ #     }
```

**Why:** Mirror of the biplot cell: `pd.DataFrame(index=vote_pivot_centered.columns)` → an explicit `call` column, since the loadings frame is iterated by row two hunks later. Mirror re-checked against the code cell it repeats: identical (hard rule 3). Note that this dropdown **contains its code cell's source twice** — a pre-existing defect (see C51–C53, which are the same three changes again). Both copies were converted identically.
**Output:** differs — the biplot (`ce889eb1`) drifts by ≤3.4e-14 relative; no arrow or point changed sign, checked trace by trace.

<a id="c49"></a>
### C49 · cell 65: Biplot · dropdown

baseline L1052 → branch L1480 · mirror of the next code cell (hard rule 3)

```diff
- # vote_2d["num votes"] = votes[votes["vote"].isin(["Yes", "No"])].groupby("member").size()
- # vote_2d.dropna(inplace=True)
+ # num_votes = (
+ #     votes.filter(pl.col("vote").is_in(["Yes", "No"]))
+ #     .group_by("member")
+ #     .agg(pl.len().alias("num votes"))
+ # )
+ # vote_2d = vote_2d.join(num_votes, on="member", how="inner", maintain_order="left")
```

**Why:** Same `groupby().size()` → `group_by().agg(pl.len().alias("num votes"))` rewrite as C43, here in the live path. The `.alias` is kept because that string is a plotly legend/hover label on a published figure — Polars' default `len` would print on the page. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — as C48; 435 members sized, same as pandas.

<a id="c50"></a>
### C50 · cell 65: Biplot · dropdown

baseline L1070 → branch L1502 · mirror of the next code cell (hard rule 3)

```diff
- # for (call, pc1, pc2) in loadings.head(20).itertuples():
+ # for (call, pc1, pc2) in loadings.head(20).iter_rows():
```

**Why:** `loadings.itertuples()` → `loadings.iter_rows()`. Both yield `(call, pc1, pc2)`, because `call` is now the first column rather than the index. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — as C48; the same 20 arrows are drawn.

<a id="c51"></a>
### C51 · cell 65: Biplot · dropdown

baseline L1075 → branch L1507 · mirror of the next code cell (hard rule 3)

```diff
- # loadings = pd.DataFrame(
- #     {"pc1": np.sqrt(s[0]) * vt[0, :], "pc2": np.sqrt(s[1]) * vt[1, :]},
- #     index=vote_pivot_centered.columns,
+ # loadings = pl.DataFrame(
+ #     {
+ #         "call": vote_pivot_centered.columns,
+ #         "pc1": np.sqrt(s[0]) * vt[0, :],
+ #         "pc2": np.sqrt(s[1]) * vt[1, :],
+ #     }
```

**Why:** Second copy of C48, inside the same dropdown. The duplication is pre-existing (CONVERSIONS.md open items); the mirror gate never registered the pair because of it. Both copies match the code cell.
**Output:** differs — as C48.

<a id="c52"></a>
### C52 · cell 65: Biplot · dropdown

baseline L1080 → branch L1515 · mirror of the next code cell (hard rule 3)

```diff
- # vote_2d["num votes"] = votes[votes["vote"].isin(["Yes", "No"])].groupby("member").size()
- # vote_2d.dropna(inplace=True)
+ # num_votes = (
+ #     votes.filter(pl.col("vote").is_in(["Yes", "No"]))
+ #     .group_by("member")
+ #     .agg(pl.len().alias("num votes"))
+ # )
+ # vote_2d = vote_2d.join(num_votes, on="member", how="inner", maintain_order="left")
```

**Why:** Second copy of C49.
**Output:** differs — as C48.

<a id="c53"></a>
### C53 · cell 65: Biplot · dropdown

baseline L1098 → branch L1537 · mirror of the next code cell (hard rule 3)

```diff
- # for (call, pc1, pc2) in loadings.head(20).itertuples():
+ # for (call, pc1, pc2) in loadings.head(20).iter_rows():
```

**Why:** Second copy of C50.
**Output:** differs — as C48.

<a id="c54"></a>
### C54 · cell 66 [code] · code

baseline L1107 → branch L1546

```diff
- loadings = pd.DataFrame(
-     {"pc1": np.sqrt(s[0]) * vt[0, :], "pc2": np.sqrt(s[1]) * vt[1, :]},
-     index=vote_pivot_centered.columns,
+ loadings = pl.DataFrame(
+     {
+         "call": vote_pivot_centered.columns,
+         "pc1": np.sqrt(s[0]) * vt[0, :],
+         "pc2": np.sqrt(s[1]) * vt[1, :],
+     }
```

**Why:** Code half of C48: `pd.DataFrame(index=vote_pivot_centered.columns)` → an explicit `call` column, because the loadings frame is iterated by row two hunks later and there is no index to iterate.
**Output:** differs — the biplot (`ce889eb1`) drifts by ≤3.4e-14 relative; no arrow or point changed sign, checked trace by trace.

<a id="c55"></a>
### C55 · cell 66 [code] · code

baseline L1112 → branch L1554

```diff
- vote_2d["num votes"] = votes[votes["vote"].isin(["Yes", "No"])].groupby("member").size()
- vote_2d.dropna(inplace=True)
+ num_votes = (
+     votes.filter(pl.col("vote").is_in(["Yes", "No"]))
+     .group_by("member")
+     .agg(pl.len().alias("num votes"))
+ )
+ vote_2d = vote_2d.join(num_votes, on="member", how="inner", maintain_order="left")
```

**Why:** Code half of C49: `groupby("member").size()` assigned onto an index-aligned column plus `dropna(inplace=True)` becomes `group_by(...).agg(pl.len().alias("num votes"))` and an inner join with `maintain_order="left"`. The `.alias` is kept because that string is a plotly legend/hover label on a published figure.
**Output:** differs — as C54; 435 members sized, same as pandas.

<a id="c56"></a>
### C56 · cell 66 [code] · code

baseline L1130 → branch L1576

```diff
- for (call, pc1, pc2) in loadings.head(20).itertuples():
+ for (call, pc1, pc2) in loadings.head(20).iter_rows():
```

**Why:** Code half of C50: `loadings.itertuples()` → `loadings.iter_rows()`. Both yield `(call, pc1, pc2)`, because `call` is a column now rather than the index.
**Output:** differs — as C54; the same 20 arrows are drawn.

<a id="c57"></a>
### C57 · cell 69: Invert and normalize the images so they look better · dropdown

baseline L1480 → branch L1926 · mirror of the next code cell (hard rule 3)

```diff
- # img_mat = -1 * train_images[sample_idx].astype(np.int16)
+ # img_mat = -1 * np.asarray(train_images[sample_idx], dtype=np.int16)
```

**Why:** `train_images[sample_idx].astype(np.int16)` → `np.asarray(train_images[sample_idx], dtype=np.int16)`. Both sides are NumPy; the explicit `asarray` is what makes the dtype conversion independent of what `load_data` hands back. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — see C88 (the cell's only text output is the cache log) and C89.

<a id="c58"></a>
### C58 · cell 69: Invert and normalize the images so they look better · dropdown

baseline L1483 → branch L1929 · mirror of the next code cell (hard rule 3)

```diff
- # images = pd.DataFrame(
+ # images = pl.DataFrame(
```

**Why:** `pd.DataFrame` → `pl.DataFrame` for the Fashion-MNIST frame. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — see C89.

<a id="c59"></a>
### C59 · cell 69: Invert and normalize the images so they look better · dropdown

baseline L1485 → branch L1931 · mirror of the next code cell (hard rule 3)

```diff
- #         "images": img_mat.tolist(),
+ #         "images": img_mat,
```

**Why:** `img_mat.tolist()` → `img_mat`. Polars takes the 3-D ndarray directly and types the column as `array[f64, (28, 28)]`, where pandas needed it flattened into a column of nested Python lists. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — see C89: the column's printed dtype and elision change; the pixel values do not.

<a id="c60"></a>
### C60 · cell 70 [code] · metadata

baseline L1493 → branch L1939

```diff
- # %% tags=["remove-input"]
+ # %% tags=["remove-input", "remove-output"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c61"></a>
### C61 · cell 70 [code] · code

baseline L1517 → branch L1963

```diff
- img_mat = -1 * train_images[sample_idx].astype(np.int16)
+ img_mat = -1 * np.asarray(train_images[sample_idx], dtype=np.int16)
```

**Why:** Code half of C57.
**Output:** differs — see C88; the printed image shapes are unchanged at (60000, 28, 28) / (10000, 28, 28).

<a id="c62"></a>
### C62 · cell 70 [code] · code

baseline L1520 → branch L1966

```diff
- images = pd.DataFrame(
+ images = pl.DataFrame(
```

**Why:** Code half of C58.
**Output:** differs — see C89.

<a id="c63"></a>
### C63 · cell 70 [code] · code

baseline L1522 → branch L1968

```diff
-         "images": img_mat.tolist(),
+         "images": img_mat,
```

**Why:** Code half of C59 — the 3-D array goes in whole, giving a native fixed-shape array column instead of a list-of-lists object column.
**Output:** differs — see C89.

<a id="c64"></a>
### C64 · cell 71 [markdown] · tab-twins

baseline L1528 → branch L1974

```diff
+ # %% [markdown]
+ # <!-- tab-twins:begin cef56efa -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # class_names = [
+ #     "T-shirt/top",
+ #     "Trouser",
+ #     "Pullover",
+ #     "Dress",
+ #     "Coat",
+ #     "Sandal",
+ #     "Shirt",
+ #     "Sneaker",
+ #     "Bag",
+ #     "Ankle boot",
+ # ]
+ # class_dict = {i: class_name for i, class_name in enumerate(class_names)}
+ #
+ # (train_images, train_labels), (test_images, test_labels) = load_data()
+ # print("Training images", train_images.shape)
+ # print("Test images", test_images.shape)
+ #
+ # rng = np.random.default_rng(42)
+ # n = 5000
+ # sample_idx = rng.choice(np.arange(len(train_images)), size=n, replace=False)
+ #
+ # # Invert and normalize the images so they look better
+ # img_mat = -1 * np.asarray(train_images[sample_idx], dtype=np.int16)
+ # img_mat = (img_mat - img_mat.min()) / (img_mat.max() - img_mat.min())
+ #
+ # images = pl.DataFrame(
+ #     {
+ #         "images": img_mat,
+ #         "labels": train_labels[sample_idx],
+ #         "class": [class_dict[x] for x in train_labels[sample_idx]],
+ #     }
+ # )
+ # ```
+ … 60 more lines
```

**Why:** Comparison tab-set for the Fashion-MNIST load, carrying both constructions side by side.
**Output:** differs — the two panes' `text` outputs are the same cache log and shapes; the frames differ only in how the `images` column is typed and printed.

<a id="c65"></a>
### C65 · cell 72 [markdown] · dropdown

baseline L1536 → branch L2082 · mirror of the next code cell (hard rule 3)

```diff
- #     img_mat = np.array(images.head(max_images)["images"].to_list())
+ #     img_mat = images.head(max_images)["images"].to_numpy()
```

**Why:** `np.array(images.head(max_images)["images"].to_list())` → `images.head(max_images)["images"].to_numpy()`. The array column already has a shape, so the round-trip through a Python list is gone. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — the figure it draws is a different sample; see C70.

<a id="c66"></a>
### C66 · cell 72 [markdown] · dropdown

baseline L1547 → branch L2093 · mirror of the next code cell (hard rule 3)

```diff
- #         lambda a: a.update(text=images.iloc[int(a.text.split("=")[-1])]["class"])
+ #         lambda a: a.update(text=images["class"][int(a.text.split("=")[-1])])
```

**Why:** `images.iloc[i]["class"]` → `images["class"][i]`. Positional row access with no index in play. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — as C65. Facet labels stay correct by construction: the lambda looks the class up by the same positional index the facet was built from.

<a id="c67"></a>
### C67 · cell 72: keep two rows drawn at random from each class · dropdown

baseline L1552 → branch L2098 · mirror of the next code cell (hard rule 3)

```diff
- # fig = show_images(images.groupby("class", as_index=False).sample(2), ncols=6)
+ # # keep two rows drawn at random from each class
+ # two_per_class = images.filter(pl.int_range(pl.len()).shuffle(seed=23).over("class") < 2).sort("class")
+ # fig = show_images(two_per_class, ncols=6)
```

**Why:** `groupby("class", as_index=False).sample(2)` → a shuffled-rank window filter, `filter(pl.int_range(pl.len()).shuffle(seed=23).over("class") < 2).sort("class")`. Three parts are all load-bearing: `.over("class")` is the group, `.sort("class")` restores the grouped grid the sentence above the figure promises (the window filter returns original frame order, scattering each class's pair), and `seed=23` re-seeds a figure the conversion had otherwise un-seeded — `np.random.seed` does not govern Polars' RNG. A comment was added because the baseline's line was self-documenting and this one is not. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — see C70. Do not replace this with `group_by("class").head(2)`: it reads better and makes the chapter's two grids identical.

<a id="c68"></a>
### C68 · cell 73 [code] · code

baseline L1560 → branch L2108

```diff
-     img_mat = np.array(images.head(max_images)["images"].to_list())
+     img_mat = images.head(max_images)["images"].to_numpy()
```

**Why:** Code half of C65.
**Output:** differs — see C70.

<a id="c69"></a>
### C69 · cell 73 [code] · code

baseline L1571 → branch L2119

```diff
-         lambda a: a.update(text=images.iloc[int(a.text.split("=")[-1])]["class"])
+         lambda a: a.update(text=images["class"][int(a.text.split("=")[-1])])
```

**Why:** Code half of C66.
**Output:** differs — see C70.

<a id="c70"></a>
### C70 · cell 73 [code] · code

baseline L1576 → branch L2124

```diff
- fig = show_images(images.groupby("class", as_index=False).sample(2), ncols=6)
+ # keep two rows drawn at random from each class
+ two_per_class = images.filter(pl.int_range(pl.len()).shuffle(seed=23).over("class") < 2).sort("class")
+ fig = show_images(two_per_class, ncols=6)
```

**Why:** Code half of C67 — the per-class sample rewritten as a window filter.
**Output:** differs — **this is the one figure in the chapter that genuinely redraws.** All 20 garments in the grid are different images from the baseline's (checked pixel-wise: 0 of 20 identical). The ten classes appear in the same order, two per class, with correct labels, so the reader learns the same thing from different clothes. The generated output list does not show this, because the report's output pass covers text outputs only.

<a id="c71"></a>
### C71 · cell 75 [code] · metadata

baseline L1582 → branch L2132

```diff
- # %%
+ # %% tags=["remove-input"]
```

**Why:** Notebook or cell metadata (jupytext header, tags). Not reader-visible.

<a id="c72"></a>
### C72 · cell 75 [code] · tab-twins

baseline L1585 → branch L2135 · spans code and prose

```diff
- show_images(images.groupby('class',as_index=False).sample(2), ncols=6)
+ # keep two rows drawn at random from each class
+ two_per_class = images.filter(pl.int_range(pl.len()).shuffle(seed=23).over("class") < 2).sort("class")
+ show_images(two_per_class, ncols=6)
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 3ec83d53 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # print(class_dict)
+ #
+ # # keep two rows drawn at random from each class
+ # two_per_class = images.filter(pl.int_range(pl.len()).shuffle(seed=23).over("class") < 2).sort("class")
+ # show_images(two_per_class, ncols=6)
+ # ```
+ #
+ # ```text
+ # {0: 'T-shirt/top', 1: 'Trouser', 2: 'Pullover', 3: 'Dress', 4: 'Coat', 5: 'Sandal', 6: 'Shirt', 7: 'Sneaker', 8: 'Bag', 9: 'Ankle boot'}
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # print(class_dict)
+ #
+ # show_images(images.groupby('class',as_index=False).sample(2), ncols=6)
+ # ```
+ #
+ # ```text
+ # {0: 'T-shirt/top', 1: 'Trouser', 2: 'Pullover', 3: 'Dress', 4: 'Coat', 5: 'Sandal', 6: 'Shirt', 7: 'Sneaker', 8: 'Bag', 9: 'Ankle boot'}
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** Comparison tab-set for the student-visible copy of the same sampling change.
**Output:** differs — the `print(class_dict)` text is identical in both panes; the figure below redraws as in C70.

<a id="c73"></a>
### C73 · cell 80 [code] · code

baseline L1597 → branch L2182

```diff
- # %%
- X = np.array(images["images"].to_list())
+ # %% tags=["remove-input", "remove-output"]
+ X = images["images"].to_numpy()
```

**Why:** `np.array(images["images"].to_list())` → `images["images"].to_numpy()`, and the cell gained `remove-input`/`remove-output` so its output renders in the tab-set at C74.
**Output:** same — `X.shape` is `(5000, 28, 28)` on both sides.

<a id="c74"></a>
### C74 · cell 80 [code] · tab-twins

baseline L1600 → branch L2185 · spans code and prose

```diff
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin d0992d63 -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # X = images["images"].to_numpy()
+ # X.shape
+ # ```
+ #
+ # ```text
+ # (5000, 28, 28)
+ # ```
+ # ::::
+ #
+ # :::: {tab-item} pandas
+ # :sync: pd
+ # ```python
+ # X = np.array(images["images"].to_list())
+ # X.shape
+ # ```
+ #
+ # ```text
+ # (5000, 28, 28)
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** Comparison tab-set for the array extraction.
**Output:** same — both panes print `(5000, 28, 28)`.

<a id="c75"></a>
### C75 · cell 91 [code] · code

baseline L1641 → branch L2255

```diff
- images[['z1', 'z2', 'z3']] = pca.transform(X)[:, :3]
+ images = images.hstack(pl.DataFrame(pca.transform(X)[:, :3], schema=["z1", "z2", "z3"]))
```

**Why:** `images[['z1','z2','z3']] = pca.transform(X)[:, :3]` has no Polars form (multi-column assignment onto an existing frame). Rewritten as `hstack` of a named three-column frame, which is positional — the same alignment the pandas assignment had.
**Output:** differs — the 3-D scatter it feeds (`8fa60bde`) drifts by ≤3.7e-14 relative, no axis flipped. Note the neighbouring scree plot (`869a4839`) moves by ~6e-5 relative: `PCA(n_components=50)` on a 5000×784 matrix uses sklearn's randomized solver and this cell sets no `random_state`, so it is unseeded in the baseline too. Pre-existing, not a conversion effect.

<a id="c76"></a>
### C76 · cell 92: [BONUS] Proof of Component Score · prose · **REVIEW**

baseline L1721 → branch L2335

```diff
- # \frac{1}{n} \tilde{X}^T \tilde{X} &= \frac{1}{n} V S V^T =V \left( \frac{1}{n} S \right) V^T \\
- # \frac{1}{n} \tilde{X}^T \tilde{X} V &= V \left( \frac{1}{n} S \right) V^T V = V \left( \frac{1}{n} S \right) & \text{(right multiply by }V \rightarrow V^T V = I \text{)} \\
- # V^T \frac{1}{n} \tilde{X}^T \tilde{X} V &= V^T V \left( \frac{1}{n} S \right) = \frac{1}{n} S & \text{(left multiply by }V^T \rightarrow V^T V = I \text{)} \\
+ # \frac{1}{n} \tilde{X}^T \tilde{X} &= \frac{1}{n} V S^2 V^T =V \left( \frac{1}{n} S^2 \right) V^T \\
+ # \frac{1}{n} \tilde{X}^T \tilde{X} V &= V \left( \frac{1}{n} S^2 \right) V^T V = V \left( \frac{1}{n} S^2 \right) & \text{(right multiply by }V \rightarrow V^T V = I \text{)} \\
+ # V^T \frac{1}{n} \tilde{X}^T \tilde{X} V &= V^T V \left( \frac{1}{n} S^2 \right) = \frac{1}{n} S^2 & \text{(left multiply by }V^T \rightarrow V^T V = I \text{)} \\
```

**Why:** The proof drops the square: on the centred SVD, $\frac1n\tilde X^T\tilde X = V(\frac1n S^2)V^T$, not $V(\frac1n S)V^T$. The line directly above derives $VS^2V^T$ correctly and the line below reads $\frac1n S_j^2$, so the three bad lines were an anomaly rather than a belief. CONTRADICTIONS.md §A7 item 3 — pre-existing, and nothing to do with Polars.
**Verdict:** optional
**Minimal alternative:** revert and ship with the rest of §A. It is three characters and unambiguously correct, so the only question is which branch owns it.

<a id="c77"></a>
### C77 · `mpg = pl.from_pandas(sns.load_dataset("mpg")).drop_nulls()` · output

committed output

```diff
- [text]     mpg  cylinders  displacement  horsepower  weight  acceleration  \
- [text] 0  18.0          8         307.0       130.0    3504          12.0
- [text] 1  15.0          8         350.0       165.0    3693          11.5
- [text] 2  18.0          8         318.0       150.0    3436          11.0
- [text] 3  16.0          8         304.0       150.0    3433          12.0
- [text] 4  17.0          8         302.0       140.0    3449          10.5
- [text]
- [text]    model_year origin                       name
- [text] 0          70    usa  chevrolet chevelle malibu
- [text] 1          70    usa          buick skylark 320
- [text] 2          70    usa         plymouth satellite
- [text] 3          70    usa              amc rebel sst
- [text] 4          70    usa                ford torino
+ [text] shape: (5, 9)
+ [text] ┌──────┬───────────┬─────────────┬────────────┬───┬─────────────┬────────────┬────────┬────────────┐
+ [text] │ mpg  ┆ cylinders ┆ displacemen ┆ horsepower ┆ … ┆ acceleratio ┆ model_year ┆ origin ┆ name       │
+ [text] │ ---  ┆ ---       ┆ t           ┆ ---        ┆   ┆ n           ┆ ---        ┆ ---    ┆ ---        │
+ [text] │ f64  ┆ i64       ┆ ---         ┆ f64        ┆   ┆ ---         ┆ i64        ┆ str    ┆ str        │
+ [text] │      ┆           ┆ f64         ┆            ┆   ┆ f64         ┆            ┆        ┆            │
+ [text] ╞══════╪═══════════╪═════════════╪════════════╪═══╪═════════════╪════════════╪════════╪════════════╡
+ [text] │ 18.0 ┆ 8         ┆ 307.0       ┆ 130.0      ┆ … ┆ 12.0        ┆ 70         ┆ usa    ┆ chevrolet  │
+ [text] │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ chevelle   │
+ [text] │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ malibu     │
+ [text] │ 15.0 ┆ 8         ┆ 350.0       ┆ 165.0      ┆ … ┆ 11.5        ┆ 70         ┆ usa    ┆ buick      │
+ [text] │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ skylark    │
+ [text] │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ 320        │
+ [text] │ 18.0 ┆ 8         ┆ 318.0       ┆ 150.0      ┆ … ┆ 11.0        ┆ 70         ┆ usa    ┆ plymouth   │
+ [text] │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ satellite  │
+ [text] │ 16.0 ┆ 8         ┆ 304.0       ┆ 150.0      ┆ … ┆ 12.0        ┆ 70         ┆ usa    ┆ amc rebel  │
+ [text] │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ sst        │
+ [text] │ 17.0 ┆ 8         ┆ 302.0       ┆ 140.0      ┆ … ┆ 10.5        ┆ 70         ┆ usa    ┆ ford       │
+ [text] │      ┆           ┆             ┆            ┆   ┆             ┆            ┆        ┆ torino     │
+ [text] └──────┴───────────┴─────────────┴────────────┴───┴─────────────┴────────────┴────────┴────────────┘
```

**Why:** The cell now returns a Polars DataFrame, so `.head()` renders Polars' box table: a `shape:` line, a dtype row, no index column, and long strings wrapped inside the cell.
**Reader sees:** equivalent — same five cars, same nine columns, same values, and the frame is still 392 rows after `drop_nulls()`. No prose in the chapter quotes the index or the row count.

<a id="c78"></a>
### C78 · `px.histogram(mpg, x="displacement")` · output

committed output

```diff
- [plotly] figure md5:ab8afc0d59
- [plotly] trace 0 histogram
+ [plotly] figure md5:35d30e84ee
+ [plotly] trace 0 histogram
```

**Why:** `mpg` is now `pl.from_pandas(sns.load_dataset("mpg")).drop_nulls()` handed straight to `px.histogram`. Decoded out of the payload, the 392 `x` values are byte-identical to the baseline's; the figure md5 moves because plotly 6.1.2 writes axis domains as `[0.0, 1.0]` where the plotly that produced the committed baseline wrote `[0, 1]`.
**Reader sees:** equivalent — same bars, same counts, same axes. Nothing in the payload differs but that number formatting.

<a id="c79"></a>
### C79 · `px.scatter(mpg, x="displacement", y="horsepower")` · output

committed output

```diff
- [plotly] figure md5:3db8377a21
- [plotly] trace 0 scatter
+ [plotly] figure md5:e18d0a4cea
+ [plotly] trace 0 scatter
```

**Why:** Same hand-off, same 392 rows: both coordinate arrays decode byte-identical to the baseline. Only the layout re-serialized (`domain: [0, 1]` -> `[0.0, 1.0]`).
**Reader sees:** equivalent — an identical scatter.

<a id="c80"></a>
### C80 · `fig = px.scatter_3d(mpg, x="displacement", y="horsepower", z="weight",` · output

committed output

```diff
- [plotly] figure md5:420df07eac
- [plotly] trace 0 scatter3d
+ [plotly] figure md5:a71fb2d35c
+ [plotly] trace 0 scatter3d
```

**Why:** The 3D scatter is drawn from the same three columns of the same 392 rows, and all three coordinate arrays are byte-identical. The hash moves on the `scene.domain` int-to-float re-serialization alone.
**Reader sees:** equivalent.

<a id="c81"></a>
### C81 · `fig = px.scatter_3d(mpg, x="displacement",` · output

committed output

```diff
- [plotly] figure md5:f465d7f7ff
- [plotly] trace 0 scatter3d
+ [plotly] figure md5:a4f3064e96
+ [plotly] trace 0 scatter3d
```

**Why:** As C80, plus the `model_year` colour axis, whose colorscale stops re-serialize from `[0, "#0d0887"]` to `[0.0, "#0d0887"]`. No coordinate and no colour value changed.
**Reader sees:** equivalent.

<a id="c82"></a>
### C82 · `fig = px.scatter_3d(mpg, x="displacement",` · output

committed output

```diff
- [plotly] figure md5:5141f07c79
- [plotly] trace 0 scatter3d name='usa'
- [plotly] trace 1 scatter3d name='japan'
- [plotly] trace 2 scatter3d name='europe'
+ [plotly] figure md5:5049f00008
+ [plotly] trace 0 scatter3d name='usa'
+ [plotly] trace 1 scatter3d name='japan'
+ [plotly] trace 2 scatter3d name='europe'
```

**Why:** Three traces, `usa`/`japan`/`europe`, in the same order with the same memberships and byte-identical coordinates. Layout float formatting only.
**Reader sees:** equivalent.

<a id="c83"></a>
### C83 · `import polars as pl` · output

committed output

```diff
- [text]    width  height  area  perimeter
- [text] 0      8       6    48         28
- [text] 1      2       4     8         12
- [text] 2      1       3     3          8
- [text] 3      9       3    27         24
- [text] 4      9       8    72         34
+ [text] shape: (5, 4)
+ [text] ┌───────┬────────┬──────┬───────────┐
+ [text] │ width ┆ height ┆ area ┆ perimeter │
+ [text] │ ---   ┆ ---    ┆ ---  ┆ ---       │
+ [text] │ i64   ┆ i64    ┆ i64  ┆ i64       │
+ [text] ╞═══════╪════════╪══════╪═══════════╡
+ [text] │ 8     ┆ 6      ┆ 48   ┆ 28        │
+ [text] │ 2     ┆ 4      ┆ 8    ┆ 12        │
+ [text] │ 1     ┆ 3      ┆ 3    ┆ 8         │
+ [text] │ 9     ┆ 3      ┆ 27   ┆ 24        │
+ [text] │ 9     ┆ 8      ┆ 72   ┆ 34        │
+ [text] └───────┴────────┴──────┴───────────┘
```

**Why:** Same render change for `rectangle.head(5)`; the file and the values are untouched.
**Reader sees:** equivalent — the same five rectangles, now with dtypes shown and no index.

<a id="c84"></a>
### C84 · `pl.DataFrame(U).head(5)` · output

committed output

```diff
- [text]           0         1         2         3
- [text] 0 -0.155151  0.064830 -0.029935  0.967868
- [text] 1 -0.038370 -0.089155  0.062019 -0.151231
- [text] 2 -0.020357 -0.081138  0.058997  0.003355
- [text] 3 -0.101519 -0.076203 -0.148160  0.006977
- [text] 4 -0.218973  0.206423  0.007274 -0.042254
+ [text] shape: (5, 4)
+ [text] ┌───────────┬───────────┬───────────┬───────────┐
+ [text] │ column_0  ┆ column_1  ┆ column_2  ┆ column_3  │
+ [text] │ ---       ┆ ---       ┆ ---       ┆ ---       │
+ [text] │ f64       ┆ f64       ┆ f64       ┆ f64       │
+ [text] ╞═══════════╪═══════════╪═══════════╪═══════════╡
+ [text] │ -0.155151 ┆ 0.06483   ┆ -0.029935 ┆ 0.894121  │
+ [text] │ -0.03837  ┆ -0.089155 ┆ 0.062019  ┆ -0.353004 │
+ [text] │ -0.020357 ┆ -0.081138 ┆ 0.058997  ┆ 0.013634  │
+ [text] │ -0.101519 ┆ -0.076203 ┆ -0.14816  ┆ 0.048877  │
+ [text] │ -0.218973 ┆ 0.206423  ┆ 0.007274  ┆ -0.035264 │
+ [text] └───────────┴───────────┴───────────┴───────────┘
```

**Why:** Two separate things moved. The wrapper change gives Polars headers (`column_0…column_3`) instead of `0…3`. Separately, the fourth column's numbers changed: `rectangle_data` is rank 3, so the fourth singular value is ~1e-14 and LAPACK is free to return any unit vector in that null direction. Verified live in the d100 env (polars 1.43.1, numpy 1.26.4) that a pandas frame and a Polars frame produce **identical** new values — the change is this machine's LAPACK against the baseline's, not the conversion.
**Reader sees:** changed: the fourth column's five numbers (0.967868 → 0.894121 and so on). The first three columns — the three components the section is about — are identical to every printed digit, and no prose quotes the fourth.

<a id="c85"></a>
### C85 · `S` · output

committed output

```diff
- [text] array([3.62932568e+02, 6.29904732e+01, 2.56544651e+01, 1.75309971e-14])
+ [text] array([3.62932568e+02, 6.29904732e+01, 2.56544651e+01, 9.92685575e-15])
```

**Why:** The fourth singular value, mathematically zero for a rank-3 matrix, re-executed to a different float: 1.75e-14 → 9.93e-15. Same LAPACK difference as C79; not a Polars effect.
**Reader sees:** changed: the fourth entry's exponent. The prose beside it reads "so small ($10^{-15}$) that it's practically $0$" — which the baseline's `e-14` did not match and this value does, so the sentence is more accurate than before. The first three values are unchanged.

<a id="c86"></a>
### C86 · `Sm = np.diag(S)` · output

committed output

```diff
- [text] array([[3.62932568e+02, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
- [text]        [0.00000000e+00, 6.29904732e+01, 0.00000000e+00, 0.00000000e+00],
- [text]        [0.00000000e+00, 0.00000000e+00, 2.56544651e+01, 0.00000000e+00],
- [text]        [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.75309971e-14]])
+ [text] array([[3.62932568e+02, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
+ [text]        [0.00000000e+00, 6.29904732e+01, 0.00000000e+00, 0.00000000e+00],
+ [text]        [0.00000000e+00, 0.00000000e+00, 2.56544651e+01, 0.00000000e+00],
+ [text]        [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 9.92685575e-15]])
```

**Why:** `np.diag(S)` propagates C80's value into the matrix's bottom-right entry.
**Reader sees:** changed: one entry, 1.75e-14 → 9.93e-15, both practically zero. The three real singular values are unchanged.

<a id="c87"></a>
### C87 · `pl.DataFrame(Vt)` · output

committed output

```diff
- [text]           0         1             2         3
- [text] 0 -0.146436 -0.129942 -8.100201e-01 -0.552756
- [text] 1 -0.192736 -0.189128  5.863482e-01 -0.763727
- [text] 2 -0.704957  0.709155  7.951614e-03  0.008396
- [text] 3 -0.666667 -0.666667 -8.701245e-17  0.333333
+ [text] shape: (4, 4)
+ [text] ┌───────────┬───────────┬─────────────┬───────────┐
+ [text] │ column_0  ┆ column_1  ┆ column_2    ┆ column_3  │
+ [text] │ ---       ┆ ---       ┆ ---         ┆ ---       │
+ [text] │ f64       ┆ f64       ┆ f64         ┆ f64       │
+ [text] ╞═══════════╪═══════════╪═════════════╪═══════════╡
+ [text] │ -0.146436 ┆ -0.129942 ┆ -0.81002    ┆ -0.552756 │
+ [text] │ -0.192736 ┆ -0.189128 ┆ 0.586348    ┆ -0.763727 │
+ [text] │ -0.704957 ┆ 0.709155  ┆ 0.007952    ┆ 0.008396  │
+ [text] │ -0.666667 ┆ -0.666667 ┆ -5.2721e-17 ┆ 0.333333  │
+ [text] └───────────┴───────────┴─────────────┴───────────┘
```

**Why:** Display-wrapper change plus Polars' default formatting, which prints six significant figures where pandas chose scientific notation for the column. The `-8.70e-17` entry also re-executed to `-5.27e-17` — the same null-direction noise as C79/C80.
**Reader sees:** equivalent — every row of $V^T$ keeps its sign and its value to the digits that matter, so no principal component flipped and every figure downstream still points the way the chapter's static images do.

<a id="c88"></a>
### C88 · `pl.DataFrame(U @ Sm @ Vt).head(5)` · output

committed output

```diff
- [text]      0    1     2     3
- [text] 0  8.0  6.0  48.0  28.0
- [text] 1  2.0  4.0   8.0  12.0
- [text] 2  1.0  3.0   3.0   8.0
- [text] 3  9.0  3.0  27.0  24.0
- [text] 4  9.0  8.0  72.0  34.0
+ [text] shape: (5, 4)
+ [text] ┌──────────┬──────────┬──────────┬──────────┐
+ [text] │ column_0 ┆ column_1 ┆ column_2 ┆ column_3 │
+ [text] │ ---      ┆ ---      ┆ ---      ┆ ---      │
+ [text] │ f64      ┆ f64      ┆ f64      ┆ f64      │
+ [text] ╞══════════╪══════════╪══════════╪══════════╡
+ [text] │ 8.0      ┆ 6.0      ┆ 48.0     ┆ 28.0     │
+ [text] │ 2.0      ┆ 4.0      ┆ 8.0      ┆ 12.0     │
+ [text] │ 1.0      ┆ 3.0      ┆ 3.0      ┆ 8.0      │
+ [text] │ 9.0      ┆ 3.0      ┆ 27.0     ┆ 24.0     │
+ [text] │ 9.0      ┆ 8.0      ┆ 72.0     ┆ 34.0     │
+ [text] └──────────┴──────────┴──────────┴──────────┘
```

**Why:** Display-wrapper change only; the reconstruction $USV^T$ is computed in NumPy either way.
**Reader sees:** equivalent — the original rectangle data recovered exactly, as before.

<a id="c89"></a>
### C89 · `centered_df = rectangle.select(pl.all() - pl.all().mean())` · output

committed output

```diff
- [text]    width  height   area  perimeter
- [text] 0   2.97    1.35  24.78       8.64
- [text] 1  -3.03   -0.65 -15.22      -7.36
- [text] 2  -4.03   -1.65 -20.22     -11.36
- [text] 3   3.97   -1.65   3.78       4.64
- [text] 4   3.97    3.35  48.78      14.64
+ [text] shape: (5, 4)
+ [text] ┌───────┬────────┬────────┬───────────┐
+ [text] │ width ┆ height ┆ area   ┆ perimeter │
+ [text] │ ---   ┆ ---    ┆ ---    ┆ ---       │
+ [text] │ f64   ┆ f64    ┆ f64    ┆ f64       │
+ [text] ╞═══════╪════════╪════════╪═══════════╡
+ [text] │ 2.97  ┆ 1.35   ┆ 24.78  ┆ 8.64      │
+ [text] │ -3.03 ┆ -0.65  ┆ -15.22 ┆ -7.36     │
+ [text] │ -4.03 ┆ -1.65  ┆ -20.22 ┆ -11.36    │
+ [text] │ 3.97  ┆ -1.65  ┆ 3.78   ┆ 4.64      │
+ [text] │ 3.97  ┆ 3.35   ┆ 48.78  ┆ 14.64     │
+ [text] └───────┴────────┴────────┴───────────┘
```

**Why:** Render change only: the centring now happens in a Polars expression, so the result prints as a Polars frame.
**Reader sees:** equivalent — the centred values are elementwise identical to the baseline's (verified live).

<a id="c90"></a>
### C90 · `two_PCs = Vt.T[:, :2]` · output

committed output

```diff
- [text]           0         1
- [text] 0 -0.098631  0.668460
- [text] 1 -0.072956 -0.374186
- [text] 2 -0.931226 -0.258375
- [text] 3 -0.343173  0.588548
+ [text] shape: (4, 2)
+ [text] ┌───────────┬───────────┐
+ [text] │ column_0  ┆ column_1  │
+ [text] │ ---       ┆ ---       │
+ [text] │ f64       ┆ f64       │
+ [text] ╞═══════════╪═══════════╡
+ [text] │ -0.098631 ┆ 0.66846   │
+ [text] │ -0.072956 ┆ -0.374186 │
+ [text] │ -0.931226 ┆ -0.258375 │
+ [text] │ -0.343173 ┆ 0.588548  │
+ [text] └───────────┴───────────┘
```

**Why:** Render change only; `two_PCs` is a NumPy slice of $V^T$ on both sides.
**Reader sees:** equivalent — the two principal components, signs included, are unchanged.

<a id="c91"></a>
### C91 · `import polars as pl` · output

committed output

```diff
- [text]   chamber  session roll call   member        vote
- [text] 0   House        1       555  A000374  Not Voting
- [text] 1   House        1       555  A000370         Yes
- [text] 2   House        1       555  A000055          No
- [text] 3   House        1       555  A000371         Yes
- [text] 4   House        1       555  A000372          No
+ [text] shape: (5, 5)
+ [text] ┌─────────┬─────────┬───────────┬─────────┬────────────┐
+ [text] │ chamber ┆ session ┆ roll call ┆ member  ┆ vote       │
+ [text] │ ---     ┆ ---     ┆ ---       ┆ ---     ┆ ---        │
+ [text] │ str     ┆ i64     ┆ str       ┆ str     ┆ str        │
+ [text] ╞═════════╪═════════╪═══════════╪═════════╪════════════╡
+ [text] │ House   ┆ 1       ┆ 555       ┆ A000374 ┆ Not Voting │
+ [text] │ House   ┆ 1       ┆ 555       ┆ A000370 ┆ Yes        │
+ [text] │ House   ┆ 1       ┆ 555       ┆ A000055 ┆ No         │
+ [text] │ House   ┆ 1       ┆ 555       ┆ A000371 ┆ Yes        │
+ [text] │ House   ┆ 1       ┆ 555       ┆ A000372 ┆ No         │
+ [text] └─────────┴─────────┴───────────┴─────────┴────────────┘
```

**Why:** `pl.read_csv` plus `cast({"roll call": pl.String})` in place of `astype`; the render is Polars' table with a dtype row.
**Reader sees:** equivalent — the same first five roll-call records. The `roll call` column is still a string, which matters because it becomes column names in the pivot.

<a id="c92"></a>
### C92 · `was_yes = (pl.element().first() == "Yes").cast(pl.Int64)` · output

committed output

```diff
- [stdout] (441, 41)
- [text] roll call  515  516  517  518  519  520  521  522  523  524  ...  546  547  \
- [text] member                                                       ...
- [text] A000055      1    0    0    0    1    1    0    1    1    1  ...    0    0
- [text] A000367      0    0    0    0    0    0    0    0    0    0  ...    0    1
- [text] A000369      1    1    0    0    1    1    0    1    1    1  ...    0    0
- [text] A000370      1    1    1    1    1    0    1    0    0    0  ...    1    1
- [text] A000371      1    1    1    1    1    0    1    0    0    0  ...    1    1
- [text]
- [text] roll call  548  549  550  551  552  553  554  555
- [text] member
- [text] A000055      1    0    0    1    0    0    1    0
- [text] A000367      1    1    1    0    1    1    0    1
- [text] A000369      1    0    0    1    0    0    1    0
- [text] A000370      1    1    1    0    1    1    1    1
- [text] A000371      1    1    1    0    1    1    1    1
- [text]
- [text] [5 rows x 41 columns]
+ [stdout] (441, 42)
+ [text] shape: (5, 42)
+ [text] ┌─────────┬─────┬─────┬─────┬───┬─────┬─────┬─────┬─────┐
+ [text] │ member  ┆ 515 ┆ 516 ┆ 517 ┆ … ┆ 552 ┆ 553 ┆ 554 ┆ 555 │
+ [text] │ ---     ┆ --- ┆ --- ┆ --- ┆   ┆ --- ┆ --- ┆ --- ┆ --- │
+ [text] │ str     ┆ i64 ┆ i64 ┆ i64 ┆   ┆ i64 ┆ i64 ┆ i64 ┆ i64 │
+ [text] ╞═════════╪═════╪═════╪═════╪═══╪═════╪═════╪═════╪═════╡
+ [text] │ A000055 ┆ 1   ┆ 0   ┆ 0   ┆ … ┆ 0   ┆ 0   ┆ 1   ┆ 0   │
+ [text] │ A000367 ┆ 0   ┆ 0   ┆ 0   ┆ … ┆ 1   ┆ 1   ┆ 0   ┆ 1   │
+ [text] │ A000369 ┆ 1   ┆ 1   ┆ 0   ┆ … ┆ 0   ┆ 0   ┆ 1   ┆ 0   │
+ [text] │ A000370 ┆ 1   ┆ 1   ┆ 1   ┆ … ┆ 1   ┆ 1   ┆ 1   ┆ 1   │
+ [text] │ A000371 ┆ 1   ┆ 1   ┆ 1   ┆ … ┆ 1   ┆ 1   ┆ 1   ┆ 1   │
+ [text] └─────────┴─────┴─────┴─────┴───┴─────┴─────┴─────┴─────┘
```

**Why:** `member` is an ordinary column in Polars and was an index in pandas, so the printed shape gains one. The values come from the aggregate expression that replaced the `was_yes` function, and `sort_columns=True` / `.sort("member")` reproduce the baseline's column and row order.
**Reader sees:** changed: the stdout line reads `(441, 42)` rather than `(441, 41)`, and `member` appears as the first column rather than as the index label. Same 441 legislators, same 41 roll calls, same 0/1 values. C29 is the paragraph added to read the new number; a reader who skips it could take the 42 as an extra vote.

<a id="c93"></a>
### C93 · `fig = px.line(y=s**2 / sum(s**2), title='Variance Explained', width=70` · output

committed output

```diff
- [plotly] figure md5:4406e2a3e6
- [plotly] trace 0 scatter
- [plotly] title='Variance Explained'
+ [plotly] figure md5:4bbdcf8567
+ [plotly] trace 0 scatter
+ [plotly] title='Variance Explained'
```

**Why:** Re-executed: `np.linalg.svd` now runs on a matrix Polars centred rather than pandas, and the 41 proportions move by at most 1.1e-16 — one ULP on the largest of them.
**Reader sees:** equivalent — the same scree curve, first point 0.803 either way, and the movement is orders of magnitude below a pixel.

<a id="c94"></a>
### C94 · `Z = (u * s)[:, :3]` · output

committed output

```diff
- [plotly] figure md5:d02497acf9
- [plotly] trace 0 scatter3d
- [plotly] title='Vote Data'
+ [plotly] figure md5:c74d925da7
+ [plotly] trace 0 scatter3d
+ [plotly] title='Vote Data'
```

**Why:** Same 441 legislators and the same SVD, re-executed off the Polars pivot; coordinates differ by at most 5.5e-14 against axes spanning roughly +/-3.2. Checked all three components for a sign flip and found none — the `.sort("member")` on the pivot holds the baseline's orientation.
**Reader sees:** equivalent.

<a id="c95"></a>
### C95 · `legislators_data = yaml.safe_load(open("data/legislators-2019.yaml"))` · output

committed output

```diff
- [plotly] figure md5:0f48da9152
- [plotly] trace 0 scatter3d name='Republican, M'
- [plotly] trace 1 scatter3d name='Republican, F'
- [plotly] trace 2 scatter3d name='Independent, M'
- [plotly] trace 3 scatter3d name='Democrat, M'
- [plotly] trace 4 scatter3d name='Democrat, F'
- [plotly] title='Vote Data'
+ [plotly] figure md5:7644acbdb0
+ [plotly] trace 0 scatter3d name='Republican, M'
+ [plotly] trace 1 scatter3d name='Republican, F'
+ [plotly] trace 2 scatter3d name='Independent, M'
+ [plotly] trace 3 scatter3d name='Democrat, M'
+ [plotly] trace 4 scatter3d name='Democrat, F'
+ [plotly] title='Vote Data'
```

**Why:** The party/gender split is unchanged — five traces in the same order carrying 184/15/1/148/91 points — and the `np.random.normal` jitter still lands on the same legislators, because the join carries `maintain_order="left"`. Coordinates move by at most 5.5e-14 from the re-run SVD.
**Reader sees:** equivalent, including the left/right party orientation that `images/pca_plot.png`'s alt text describes; PC1 did not flip.

<a id="c96"></a>
### C96 · `fig_eig = px.bar(x=vote_pivot_centered.columns, y=vt[0, :])` · output

committed output

```diff
- [plotly] figure md5:2083efd31f
- [plotly] trace 0 bar x: n=41
+ [plotly] figure md5:2d63ff2b38
+ [plotly] trace 0 bar x: n=41
```

**Why:** The 41 roll calls arrive in the same order (`sort_columns=True` on the pivot) and the PC1 loadings differ by at most 2.2e-16, with no sign change.
**Reader sees:** equivalent — the same bars above and below zero, so the paragraph reading PC1 against party still holds.

<a id="c97"></a>
### C97 · `party_line_votes = (` · output

committed output

```diff
- [plotly] figure md5:24aa3ca41f
- [plotly] trace 0 bar name='Democrat' x: n=41
- [plotly] trace 1 bar name='Independent' x: n=41
- [plotly] trace 2 bar name='Republican' x: n=41
+ [plotly] figure md5:4654ff511a
+ [plotly] trace 0 bar name='Democrat' x: n=41
+ [plotly] trace 1 bar name='Independent' x: n=41
+ [plotly] trace 2 bar name='Republican' x: n=41
```

**Why:** Nothing in the data moved: `unpivot` plus `.sort("party")` reproduce the baseline's three facet rows and all 41 bars in each of them byte-for-byte. The md5 changes on the layout's `[0, 1]` -> `[0.0, 1.0]` domains alone.
**Reader sees:** equivalent.

<a id="c98"></a>
### C98 · `loadings = pl.DataFrame(` · output

committed output

```diff
- [plotly] figure md5:7a67cc88ea
- [plotly] trace 0 scatter name='Republican, M'
- [plotly] trace 1 scatter name='Republican, F'
- [plotly] trace 2 scatter name='Independent, M'
- [plotly] trace 3 scatter name='Democrat, M'
- [plotly] trace 4 scatter name='Democrat, F'
- [plotly] trace 5 scatter name='515' x: n=2 min=-0.215368 max=0 y: n=2 min=0 max=1.14739
- [plotly] trace 6 scatter name='516' x: n=2 min=-0.846835 max=0 y: n=2 min=0 max=0.930164
- [plotly] trace 7 scatter name='517' x: n=2 min=-1.37564 max=0 y: n=2 min=0 max=0.180715
- [plotly] trace 8 scatter name='518' x: n=2 min=-1.37161 max=0 y: n=2 min=0 max=0.197301
- [plotly] trace 9 scatter name='519' x: n=2 min=-0.0390205 max=0 y: n=2 min=0 max=0.827081
- [plotly] trace 10 scatter name='520' x: n=2 min=0 max=1.28627 y: n=2 min=0 max=0.548131
- [plotly] trace 11 scatter name='521' x: n=2 min=-1.24995 max=0 y: n=2 min=0 max=0.207553
- [plotly] trace 12 scatter name='522' x: n=2 min=0 max=1.14936 y: n=2 min=0 max=0.498054
- [plotly] trace 13 scatter name='523' x: n=2 min=0 max=1.26862 y: n=2 min=0 max=0.548341
- [plotly] trace 14 scatter name='524' x: n=2 min=0 max=1.33084 y: n=2 min=0 max=0.593161
- [plotly] trace 15 scatter name='525' x: n=2 min=-1.30705 max=0 y: n=2 min=0 max=0.227945
- [plotly] trace 16 scatter name='526' x: n=2 min=0 max=1.29953 y: n=2 min=0 max=0.60106
- [plotly] trace 17 scatter name='527' x: n=2 min=0 max=1.28286 y: n=2 min=0 max=0.609823
- [plotly] trace 18 scatter name='528' x: n=2 min=0 max=1.29394 y: n=2 min=0 max=0.598366
- [plotly] trace 19 scatter name='529' x: n=2 min=0 max=1.31088 y: n=2 min=0 max=0.620105
- [plotly] trace 20 scatter name='530' x: n=2 min=-1.32875 max=0 y: n=2 min=0 max=0.242291
- [plotly] trace 21 scatter name='531' x: n=2 min=0 max=1.28109 y: n=2 min=0 max=0.637608
- [plotly] trace 22 scatter name='532' x: n=2 min=0 max=0.0144394 y: n=2 min=0 max=0.914313
- [plotly] trace 23 scatter name='533' x: n=2 min=-1.36126 max=0 y: n=2 min=0 max=0.315752
- [plotly] trace 24 scatter name='534' x: n=2 min=-1.37086 max=0 y: n=2 min=0 max=0.307624
- [plotly] title='Biplot'
+ [plotly] figure md5:48e45bd5a6
+ [plotly] trace 0 scatter name='Republican, M'
+ [plotly] trace 1 scatter name='Republican, F'
+ [plotly] trace 2 scatter name='Independent, M'
+ [plotly] trace 3 scatter name='Democrat, M'
+ [plotly] trace 4 scatter name='Democrat, F'
+ [plotly] trace 5 scatter name='515' x: n=2 min=-0.215368 max=0 y: n=2 min=0 max=1.14739
+ [plotly] trace 6 scatter name='516' x: n=2 min=-0.846835 max=0 y: n=2 min=0 max=0.930164
+ [plotly] trace 7 scatter name='517' x: n=2 min=-1.37564 max=0 y: n=2 min=0 max=0.180715
+ [plotly] trace 8 scatter name='518' x: n=2 min=-1.37161 max=0 y: n=2 min=0 max=0.197301
+ [plotly] trace 9 scatter name='519' x: n=2 min=-0.0390205 max=0 y: n=2 min=0 max=0.827081
+ [plotly] trace 10 scatter name='520' x: n=2 min=0 max=1.28627 y: n=2 min=0 max=0.548131
+ [plotly] trace 11 scatter name='521' x: n=2 min=-1.24995 max=0 y: n=2 min=0 max=0.207553
+ [plotly] trace 12 scatter name='522' x: n=2 min=0 max=1.14936 y: n=2 min=0 max=0.498054
+ [plotly] trace 13 scatter name='523' x: n=2 min=0 max=1.26862 y: n=2 min=0 max=0.548341
+ [plotly] trace 14 scatter name='524' x: n=2 min=0 max=1.33084 y: n=2 min=0 max=0.593161
+ [plotly] trace 15 scatter name='525' x: n=2 min=-1.30705 max=0 y: n=2 min=0 max=0.227945
+ [plotly] trace 16 scatter name='526' x: n=2 min=0 max=1.29953 y: n=2 min=0 max=0.60106
+ [plotly] trace 17 scatter name='527' x: n=2 min=0 max=1.28286 y: n=2 min=0 max=0.609823
+ [plotly] trace 18 scatter name='528' x: n=2 min=0 max=1.29394 y: n=2 min=0 max=0.598366
+ [plotly] trace 19 scatter name='529' x: n=2 min=0 max=1.31088 y: n=2 min=0 max=0.620105
+ [plotly] trace 20 scatter name='530' x: n=2 min=-1.32875 max=0 y: n=2 min=0 max=0.242291
+ [plotly] trace 21 scatter name='531' x: n=2 min=0 max=1.28109 y: n=2 min=0 max=0.637608
+ [plotly] trace 22 scatter name='532' x: n=2 min=0 max=0.0144394 y: n=2 min=0 max=0.914313
+ [plotly] trace 23 scatter name='533' x: n=2 min=-1.36126 max=0 y: n=2 min=0 max=0.315752
+ [plotly] trace 24 scatter name='534' x: n=2 min=-1.37086 max=0 y: n=2 min=0 max=0.307624
+ [plotly] title='Biplot'
```

**Why:** 25 traces in the same order with the same names — five party/gender groups plus roll calls 515-534 — and no coordinate more than 5.5e-14 from the baseline. None of the 20 loading arrows is negated.
**Reader sees:** equivalent — the arrows still point the way the prose walks through them ("the purple arrow labeled '520'... we would infer that $v_1$ is positive").

<a id="c99"></a>
### C99 · `class_names = [` · output

committed output

```diff
- [stdout] Using cached version that was downloaded (UTC): Tue Dec 16 13:23:25 2025
- [stdout] Using cached version that was downloaded (UTC): Tue Dec 16 13:23:25 2025
- [stdout] Using cached version that was downloaded (UTC): Tue Dec 16 13:23:25 2025
- [stdout] Using cached version that was downloaded (UTC): Tue Dec 16 13:23:25 2025
- [stdout] Training images (60000, 28, 28)
- [stdout] Test images (10000, 28, 28)
+ [stdout] Using cached version that was downloaded (UTC): Sun Aug 16 22:33:59 2026
+ [stdout] Using cached version that was downloaded (UTC): Sun Aug 16 22:33:59 2026
+ [stdout] Using cached version that was downloaded (UTC): Sun Aug 16 22:33:59 2026
+ [stdout] Using cached version that was downloaded (UTC): Sun Aug 16 22:33:59 2026
+ [stdout] Training images (60000, 28, 28)
+ [stdout] Test images (10000, 28, 28)
```

**Why:** The notebook was re-executed, so the cached-download log line carries the new execution date. Nothing in the code or the data changed.
**Reader sees:** equivalent — the four cache lines print a 2026 date instead of a 2025 one; the image shapes below them, (60000, 28, 28) and (10000, 28, 28), are identical.

<a id="c100"></a>
### C100 · `def show_images(images, ncols=5, max_images=30):` · output

committed output

```diff
- [plotly] figure md5:e70b1103ad
- [plotly] trace 0 heatmap name='0'
- [plotly] trace 1 heatmap name='1'
- [plotly] trace 2 heatmap name='2'
- [plotly] trace 3 heatmap name='3'
- [plotly] trace 4 heatmap name='4'
- [plotly] trace 5 heatmap name='5'
- [plotly] trace 6 heatmap name='6'
- [plotly] trace 7 heatmap name='7'
- [plotly] trace 8 heatmap name='8'
- [plotly] trace 9 heatmap name='9'
- [plotly] trace 10 heatmap name='10'
- [plotly] trace 11 heatmap name='11'
- [plotly] trace 12 heatmap name='12'
- [plotly] trace 13 heatmap name='13'
- [plotly] trace 14 heatmap name='14'
- [plotly] trace 15 heatmap name='15'
- [plotly] trace 16 heatmap name='16'
- [plotly] trace 17 heatmap name='17'
- [plotly] trace 18 heatmap name='18'
- [plotly] trace 19 heatmap name='19'
+ [plotly] figure md5:75f4d90d24
+ [plotly] trace 0 heatmap name='0'
+ [plotly] trace 1 heatmap name='1'
+ [plotly] trace 2 heatmap name='2'
+ [plotly] trace 3 heatmap name='3'
+ [plotly] trace 4 heatmap name='4'
+ [plotly] trace 5 heatmap name='5'
+ [plotly] trace 6 heatmap name='6'
+ [plotly] trace 7 heatmap name='7'
+ [plotly] trace 8 heatmap name='8'
+ [plotly] trace 9 heatmap name='9'
+ [plotly] trace 10 heatmap name='10'
+ [plotly] trace 11 heatmap name='11'
+ [plotly] trace 12 heatmap name='12'
+ [plotly] trace 13 heatmap name='13'
+ [plotly] trace 14 heatmap name='14'
+ [plotly] trace 15 heatmap name='15'
+ [plotly] trace 16 heatmap name='16'
+ [plotly] trace 17 heatmap name='17'
+ [plotly] trace 18 heatmap name='18'
+ [plotly] trace 19 heatmap name='19'
```

**Why:** The baseline drew two garments per class with an unseeded `groupby("class").sample(2)` riding NumPy's global RNG; the Polars version uses `pl.int_range(pl.len()).shuffle(seed=23).over("class") < 2`. Different stream, and now a seeded one — hashing the 20 heatmap grids on each side gives zero overlap.
**Reader sees:** changed: all 20 panels show different garments. The grid is still two examples of each of the same ten classes in the same facet order, and the facet titles are generated from the data rather than hard-coded, so nothing is mislabelled — but every picture on the page is new.

<a id="c101"></a>
### C101 · `print(class_dict)` · output

committed output

```diff
- [stdout] {0: 'T-shirt/top', 1: 'Trouser', 2: 'Pullover', 3: 'Dress', 4: 'Coat', 5: 'Sandal', 6: 'Shirt', 7: 'Sneaker', 8: 'Bag', 9: 'Ankle boot'}
- [plotly] figure md5:f4ef686674
- [plotly] trace 0 heatmap name='0'
- [plotly] trace 1 heatmap name='1'
- [plotly] trace 2 heatmap name='2'
- [plotly] trace 3 heatmap name='3'
- [plotly] trace 4 heatmap name='4'
- [plotly] trace 5 heatmap name='5'
- [plotly] trace 6 heatmap name='6'
- [plotly] trace 7 heatmap name='7'
- [plotly] trace 8 heatmap name='8'
- [plotly] trace 9 heatmap name='9'
- [plotly] trace 10 heatmap name='10'
- [plotly] trace 11 heatmap name='11'
- [plotly] trace 12 heatmap name='12'
- [plotly] trace 13 heatmap name='13'
- [plotly] trace 14 heatmap name='14'
- [plotly] trace 15 heatmap name='15'
- [plotly] trace 16 heatmap name='16'
- [plotly] trace 17 heatmap name='17'
- [plotly] trace 18 heatmap name='18'
- [plotly] trace 19 heatmap name='19'
+ [stdout] {0: 'T-shirt/top', 1: 'Trouser', 2: 'Pullover', 3: 'Dress', 4: 'Coat', 5: 'Sandal', 6: 'Shirt', 7: 'Sneaker', 8: 'Bag', 9: 'Ankle boot'}
+ [plotly] figure md5:75f4d90d24
+ [plotly] trace 0 heatmap name='0'
+ [plotly] trace 1 heatmap name='1'
+ [plotly] trace 2 heatmap name='2'
+ [plotly] trace 3 heatmap name='3'
+ [plotly] trace 4 heatmap name='4'
+ [plotly] trace 5 heatmap name='5'
+ [plotly] trace 6 heatmap name='6'
+ [plotly] trace 7 heatmap name='7'
+ [plotly] trace 8 heatmap name='8'
+ [plotly] trace 9 heatmap name='9'
+ [plotly] trace 10 heatmap name='10'
+ [plotly] trace 11 heatmap name='11'
+ [plotly] trace 12 heatmap name='12'
+ [plotly] trace 13 heatmap name='13'
+ [plotly] trace 14 heatmap name='14'
+ [plotly] trace 15 heatmap name='15'
+ [plotly] trace 16 heatmap name='16'
+ [plotly] trace 17 heatmap name='17'
+ [plotly] trace 18 heatmap name='18'
+ [plotly] trace 19 heatmap name='19'
```

**Why:** The same seeded expression as C100, so the same 20 garments come back. In the baseline the two grids drew independently and showed different clothes; seeded, this one is now an exact repeat of C100 (verified by hashing both).
**Reader sees:** changed: 20 new garments, and — separately — the page now shows the same grid twice where it used to show two different draws. The cell exists to print `class_dict` beside an example grid, so nothing breaks, but staff may prefer a second seed here.

<a id="c102"></a>
### C102 · `images.head()` · output

committed output

```diff
- [text]                                               images  labels        class
- [text] 0  [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,...       3        Dress
- [text] 1  [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,...       4         Coat
- [text] 2  [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,...       0  T-shirt/top
- [text] 3  [[1.0, 1.0, 1.0, 1.0, 1.0, 0.996078431372549, ...       2     Pullover
- [text] 4  [[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,...       1      Trouser
+ [text] shape: (5, 3)
+ [text] ┌─────────────────────────────────┬────────┬─────────────┐
+ [text] │ images                          ┆ labels ┆ class       │
+ [text] │ ---                             ┆ ---    ┆ ---         │
+ [text] │ array[f64, (28, 28)]            ┆ u8     ┆ str         │
+ [text] ╞═════════════════════════════════╪════════╪═════════════╡
+ [text] │ [[1.0, 1.0, … 1.0], [1.0, 1.0,… ┆ 3      ┆ Dress       │
+ [text] │ [[1.0, 1.0, … 1.0], [1.0, 1.0,… ┆ 4      ┆ Coat        │
+ [text] │ [[1.0, 1.0, … 1.0], [1.0, 1.0,… ┆ 0      ┆ T-shirt/top │
+ [text] │ [[1.0, 1.0, … 1.0], [1.0, 1.0,… ┆ 2      ┆ Pullover    │
+ [text] │ [[1.0, 1.0, … 1.0], [1.0, 1.0,… ┆ 1      ┆ Trouser     │
+ [text] └─────────────────────────────────┴────────┴─────────────┘
```

**Why:** `img_mat.tolist()` → `img_mat` types the column as a native `array[f64, (28, 28)]` rather than a column of nested Python lists, and `labels` keeps its `u8` dtype instead of being widened. Polars elides the nested array in the cell.
**Reader sees:** equivalent — the same five images with the same labels and classes, in the same order. The reader sees a dtype they did not see before (`array[f64, (28, 28)]`), which is arguably clearer about what the column holds; no prose describes the old list-of-lists shape.

<a id="c103"></a>
### C103 · `fig = px.line(y=pca.explained_variance_ratio_ * 100, markers=True)` · output

committed output

```diff
- [plotly] figure md5:c4c87adaef
- [plotly] trace 0 scatter
+ [plotly] figure md5:504421f477
+ [plotly] trace 0 scatter
```

**Why:** `PCA(n_components=50)` on 5000x784 falls through to sklearn's randomized SVD, which takes no `random_state`, so the low-variance tail redraws on every execution. Components 1-40 agree to ~1e-13; the largest move is component 46, 0.17423% -> 0.17598%.
**Reader sees:** equivalent — the y-axis runs to 29% and the whole disagreement is 0.0018 percentage points in the flat tail, well under a pixel. Not a conversion effect: two runs of the baseline code would differ the same way.

<a id="c104"></a>
### C104 · `images = images.hstack(pl.DataFrame(pca.transform(X)[:, :3], schema=["` · output

committed output

```diff
- [plotly] figure md5:ac5667ea6c
- [plotly] trace 0 scatter3d name='Dress'
- [plotly] trace 1 scatter3d name='Coat'
- [plotly] trace 2 scatter3d name='T-shirt/top'
- [plotly] trace 3 scatter3d name='Pullover'
- [plotly] trace 4 scatter3d name='Trouser'
- [plotly] trace 5 scatter3d name='Bag'
- [plotly] trace 6 scatter3d name='Shirt'
- [plotly] trace 7 scatter3d name='Sandal'
- [plotly] trace 8 scatter3d name='Ankle boot'
- [plotly] trace 9 scatter3d name='Sneaker'
+ [plotly] figure md5:c49071f188
+ [plotly] trace 0 scatter3d name='Dress'
+ [plotly] trace 1 scatter3d name='Coat'
+ [plotly] trace 2 scatter3d name='T-shirt/top'
+ [plotly] trace 3 scatter3d name='Pullover'
+ [plotly] trace 4 scatter3d name='Trouser'
+ [plotly] trace 5 scatter3d name='Bag'
+ [plotly] trace 6 scatter3d name='Shirt'
+ [plotly] trace 7 scatter3d name='Sandal'
+ [plotly] trace 8 scatter3d name='Ankle boot'
+ [plotly] trace 9 scatter3d name='Sneaker'
```

**Why:** `images` now gains z1-z3 through `hstack` rather than multi-column assignment. The ten class traces keep their names, order and sizes (Dress 509, Coat 520, T-shirt/top 491, ...) and `pca.transform` output moves by at most 1.9e-13.
**Reader sees:** equivalent.

