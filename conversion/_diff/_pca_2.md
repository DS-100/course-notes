# _pca_2 — change report

`887a578b0a4b:content/_pca_2/pca_2.ipynb` → `content/_pca_2/pca_2.ipynb`

**Tier C · 81 changes:** output 22 · prose 5 · dropdown 20 · code 33 · mechanical 1

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

Tier C, and effectively the same conversion as `pca` performed on the superseded
two-part version of the chapter: the same `pivot_table` → `pivot`-with-an-expression, the same
index-alignment join, the same `.T…melt()` → `unpivot`, the same Fashion-MNIST array column. **The
chapter is not in `myst.yml`'s TOC** — only `content/pca/pca.ipynb` is — so `jupyter-book` never
builds it and none of these 71 changes reaches a reader. CONVERSIONS.md recommends deleting the
directory outright, and its state is `GATED` rather than `DONE`.

Two things still worth staff attention even so. First, this chapter is where the PC1 sign flip was
*found*: converting the "redundant" copy is what exposed the defect in the live chapter, and the
`.sort("member")` fix at C20 is the same fix that shipped in `pca`. Second, `_pca_2` got the shorter
half of the prose work — C16 adds one sentence about `member` becoming a column, but there is no
counterpart to `pca`'s C29, so the `(441, 41)` → `(441, 42)` shape change ships here with nothing
reading it. If staff keep the chapter rather than delete it, that paragraph and the 19 missing
`:alt:` attributes are what it needs.

## Needs review

- [C1](#c1) · cell 4: SVD in `NumPy`
- [C8](#c8) · cell 23: Code Demo
- [C16](#c16) · cell 31 [markdown]
- [C21](#c21) · cell 33: PCA with SVD
- [C34](#c34) · cell 41 [markdown]

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C60](#c60) · `import polars as pl`
- [C61](#c61) · `pl.DataFrame(U).head(5)`
- [C62](#c62) · `S`
- [C63](#c63) · `Sm = np.diag(S)`
- [C64](#c64) · `pl.DataFrame(Vt)`
- [C65](#c65) · `pl.DataFrame(U @ Sm @ Vt).head(5)`
- [C66](#c66) · `centered_df = rectangle.select(pl.all() - pl.all().mean())`
- [C67](#c67) · `two_PCs = Vt.T[:, :2]`
- [C68](#c68) · `import polars as pl`
- [C69](#c69) · `was_yes = (pl.element().first() == "Yes").cast(pl.Int64)`
- [C70](#c70) · `fig = px.line(y=s**2 / sum(s**2), title='Variance Explained', width=70`
- [C71](#c71) · `Z = (u * s)[:, :3]`
- [C72](#c72) · `legislators_data = yaml.safe_load(open("data/legislators-2019.yaml"))`
- [C73](#c73) · `fig_eig = px.bar(x=vote_pivot_centered.columns, y=vt[0, :])`
- [C74](#c74) · `party_line_votes = (`
- [C75](#c75) · `loadings = pl.DataFrame(`
- [C76](#c76) · `class_names = [`
- [C77](#c77) · `def show_images(images, ncols=5, max_images=30):`
- [C78](#c78) · `print(class_dict)`
- [C79](#c79) · `images.head()`
- [C80](#c80) · `fig = px.line(y=pca.explained_variance_ratio_ * 100, markers=True)`
- [C81](#c81) · `images = images.hstack(pl.DataFrame(pca.transform(X)[:, :3], schema=["`

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C12](#c12) · cell 29: Example: House of Representatives Voting
- [C13](#c13) · cell 29: Example: House of Representatives Voting
- [C17](#c17) · cell 31: 1 when the member's recorded vote on that roll call is a Yes
- [C18](#c18) · cell 31: 1 when the member's recorded vote on that roll call is a Yes
- [C24](#c24) · cell 39 [markdown]
- [C25](#c25) · cell 39 [markdown]
- [C26](#c26) · cell 39 [markdown]
- [C27](#c27) · cell 39 [markdown]
- [C28](#c28) · cell 39 [markdown]
- [C35](#c35) · cell 43 [markdown]
- [C36](#c36) · cell 43 [markdown]
- [C39](#c39) · cell 45: Biplot
- [C40](#c40) · cell 45: Biplot
- [C41](#c41) · cell 45: Biplot
- [C45](#c45) · cell 49: Invert and normalize the images so they look better
- [C46](#c46) · cell 49: Invert and normalize the images so they look better
- [C47](#c47) · cell 49: Invert and normalize the images so they look better
- [C51](#c51) · cell 51 [markdown]
- [C52](#c52) · cell 51 [markdown]
- [C53](#c53) · cell 51: keep two rows drawn at random from each class

## Changes

<a id="c1"></a>
### C1 · cell 4: SVD in `NumPy` · prose · **REVIEW**

baseline L216 → branch L216

```diff
- # import pandas as pd
+ # import polars as pl
```

**Why:** Dropdown mirror of the setup cell's import; it is classified `prose` only because the whole cell is markdown. `pd` had no other use once `pl.read_csv` replaced `pd.read_csv` two lines down. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Verdict:** necessary

<a id="c2"></a>
### C2 · cell 4: SVD in `NumPy` · mechanical

baseline L227 → branch L227

```diff
- # rectangle = pd.read_csv("data/rectangle_data.csv")
+ # rectangle = pl.read_csv("data/rectangle_data.csv")
```

**Why:** Library rename only (pandas → Polars, `pd.` → `pl.`, dataframe → DataFrame, or similar). Wording is otherwise identical.

<a id="c3"></a>
### C3 · cell 5 [code] · code

baseline L233 → branch L233

```diff
- import pandas as pd
+ import polars as pl
```

**Why:** The chapter's library import.
**Output:** same — import cell, no committed output.

<a id="c4"></a>
### C4 · cell 5 [code] · code

baseline L244 → branch L244

```diff
- rectangle = pd.read_csv("data/rectangle_data.csv")
+ rectangle = pl.read_csv("data/rectangle_data.csv")
```

**Why:** `pd.read_csv` → `pl.read_csv`; same file, same parse.
**Output:** differs — Polars render; see C60.

<a id="c5"></a>
### C5 · cell 11 [code] · code

baseline L263 → branch L263

```diff
- pd.DataFrame(U).head(5)
+ pl.DataFrame(U).head(5)
```

**Why:** `pd.DataFrame(U)` → `pl.DataFrame(U)`; display wrapper only.
**Output:** differs — see C61.

<a id="c6"></a>
### C6 · cell 20 [code] · code

baseline L293 → branch L293

```diff
- pd.DataFrame(Vt)
+ pl.DataFrame(Vt)
```

**Why:** Same display-wrapper change for $V^T$.
**Output:** differs — see C64.

<a id="c7"></a>
### C7 · cell 22 [code] · code

baseline L299 → branch L299

```diff
- pd.DataFrame(U @ Sm @ Vt).head(5)
+ pl.DataFrame(U @ Sm @ Vt).head(5)
```

**Why:** Display wrapper on the reconstruction.
**Output:** differs — see C65.

<a id="c8"></a>
### C8 · cell 23: Code Demo · prose · **REVIEW**

baseline L413 → branch L413

```diff
- # 1. Center $X$ by subtracting the mean from each column. Notice how we specify `axis=0` so that the mean is computed per column.
+ # 1. Center $X$ by subtracting the mean from each column. `pl.all().mean()` produces one mean per column.
```

**Why:** The sentence explained pandas' `axis=0`, which the converted cell no longer contains: `rectangle.select(pl.all() - pl.all().mean())` is per-column by construction.
**Verdict:** necessary

<a id="c9"></a>
### C9 · cell 24 [code] · code

baseline L416 → branch L416

```diff
- centered_df = rectangle - np.mean(rectangle, axis=0)
+ centered_df = rectangle.select(pl.all() - pl.all().mean())
```

**Why:** `rectangle - np.mean(rectangle, axis=0)` → `rectangle.select(pl.all() - pl.all().mean())`. `np.mean(frame, axis=0)` is in the NumPy reduction family that rejects a Polars frame's signature, and the section is teaching per-column centring, so the expression stays in Polars.
**Output:** differs — see C66; the values are elementwise identical.

<a id="c10"></a>
### C10 · cell 26 [code] · code

baseline L424 → branch L424

```diff
- Sm = pd.DataFrame(np.diag(np.round(S, 1)))
+ Sm = pl.DataFrame(np.diag(np.round(S, 1)))
```

**Why:** `pd.DataFrame(np.diag(np.round(S, 1)))` → `pl.DataFrame(...)`; display wrapper only.
**Output:** same — the cell (`559cf6e9`) carries no committed output.

<a id="c11"></a>
### C11 · cell 28 [code] · code

baseline L431 → branch L431

```diff
- pd.DataFrame(two_PCs).head()
+ pl.DataFrame(two_PCs).head()
```

**Why:** Display wrapper on `two_PCs`.
**Output:** differs — see C67.

<a id="c12"></a>
### C12 · cell 29: Example: House of Representatives Voting · dropdown

baseline L507 → branch L507 · mirror of the next code cell (hard rule 3)

```diff
- # import pandas as pd
+ # import polars as pl
```

**Why:** Setup mirror for the voting section: the import. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — Polars render of `votes.head()`; see C68.

<a id="c13"></a>
### C13 · cell 29: Example: House of Representatives Voting · dropdown

baseline L517 → branch L517 · mirror of the next code cell (hard rule 3)

```diff
- # votes = pd.read_csv("data/votes.csv")
- # votes = votes.astype({"roll call": str})
+ # votes = pl.read_csv("data/votes.csv")
+ # votes = votes.cast({"roll call": pl.String})
```

**Why:** `pd.read_csv` → `pl.read_csv` and `astype({"roll call": str})` → `cast({"roll call": pl.String})`, in the same mirror. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — see C68. The column has to stay a string: it becomes column names in the pivot.

<a id="c14"></a>
### C14 · cell 30 [code] · code

baseline L525 → branch L525

```diff
- import pandas as pd
+ import polars as pl
```

**Why:** Code half of C12.
**Output:** differs — see C68.

<a id="c15"></a>
### C15 · cell 30 [code] · code

baseline L535 → branch L535

```diff
- votes = pd.read_csv("data/votes.csv")
- votes = votes.astype({"roll call": str})
+ votes = pl.read_csv("data/votes.csv")
+ votes = votes.cast({"roll call": pl.String})
```

**Why:** Code half of C13.
**Output:** differs — see C68.

<a id="c16"></a>
### C16 · cell 31 [markdown] · prose · **REVIEW**

baseline L541 → branch L541

```diff
- # Suppose we pivot this table to group each legislator and their voting pattern across every (roll call) vote in this month. We mark 1 if the legislator voted Yes ("yea"), and 0 otherwise ("No", "nay", no vote, speaker, etc.).
+ # Suppose we pivot this table to group each legislator and their voting pattern across every (roll call) vote in this month. We mark 1 if the legislator voted Yes ("yea"), and 0 otherwise ("No", "nay", no vote, speaker, etc.). Each legislator becomes one row, labelled by the `member` column, and each roll call becomes a column of 0s and 1s.
```

**Why:** Added sentence, because the pivot's committed shape changed from `(441, 41)` to `(441, 42)` when `member` stopped being an index. It describes the frame the next cell prints.
**Verdict:** questionable
**Minimal alternative:** as written it explains the *shape* of the result but never names the number, so a reader comparing it with `pca`'s C29 paragraph gets a weaker account of the same change. Either carry `pca`'s paragraph across, or — given the chapter is out of the TOC and recommended for deletion — revert to the baseline sentence and spend the effort on `pca`.

<a id="c17"></a>
### C17 · cell 31: 1 when the member's recorded vote on that roll call is a Yes · dropdown

baseline L546 → branch L546 · mirror of the next code cell (hard rule 3)

```diff
- # def was_yes(s):
- #     return 1 if s.iloc[0] == "Yes" else 0
+ # # 1 when the member's recorded vote on that roll call is a Yes
+ # was_yes = (pl.element().first() == "Yes").cast(pl.Int64)
```

**Why:** The pandas helper `def was_yes(s): return 1 if s.iloc[0] == "Yes" else 0` becomes an expression, `(pl.element().first() == "Yes").cast(pl.Int64)`, which `pivot(aggregate_function=)` takes directly. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — see C69.

<a id="c18"></a>
### C18 · cell 31: 1 when the member's recorded vote on that roll call is a Yes · dropdown

baseline L549 → branch L549 · mirror of the next code cell (hard rule 3)

```diff
- #
- # vote_pivot = votes.pivot_table(
- #     index="member", columns="roll call", values="vote", aggfunc=was_yes, fill_value=0
- # )
+ # vote_pivot = votes.pivot(
+ #     on="roll call",
+ #     index="member",
+ #     values="vote",
+ #     aggregate_function=was_yes,
+ #     sort_columns=True,
+ # ).fill_null(0).sort("member")  # row order fixes the sign of each principal component
```

**Why:** `pivot_table(index=, columns=, values=, aggfunc=, fill_value=0)` → `pivot(...)` + `.fill_null(0)`, with `sort_columns=True` (roll calls 515–555 are the x-axis of two bar charts) and `.sort("member")` (row order fixes the sign of every principal component). Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — see C69.

<a id="c19"></a>
### C19 · cell 32 [code] · code

baseline L560 → branch L563

```diff
- def was_yes(s):
-     return 1 if s.iloc[0] == "Yes" else 0
+ # 1 when the member's recorded vote on that roll call is a Yes
+ was_yes = (pl.element().first() == "Yes").cast(pl.Int64)
```

**Why:** Code half of C17.
**Output:** differs — see C69.

<a id="c20"></a>
### C20 · cell 32 [code] · code

baseline L563 → branch L566

```diff
- 
- vote_pivot = votes.pivot_table(
-     index="member", columns="roll call", values="vote", aggfunc=was_yes, fill_value=0
- )
+ vote_pivot = votes.pivot(
+     on="roll call",
+     index="member",
+     values="vote",
+     aggregate_function=was_yes,
+     sort_columns=True,
+ ).fill_null(0).sort("member")  # row order fixes the sign of each principal component
```

**Why:** Code half of C18. **This is the chapter where the sign flip was found**: without `.sort("member")`, Polars' `pivot` returns members in order of first appearance, the row permutation flips LAPACK's sign choice, and every principal component — and so the biplot, the PC1 bar chart and every arrow — mirrors. The same fix was then applied to `pca`. See CONVERSIONS.md "The sign flip".
**Output:** differs — see C69: `(441, 42)` instead of `(441, 41)`, `member` as the first column, same values. Verified here that no figure in this chapter has a flipped axis; the largest figure drift is 3.4e-14 relative.

<a id="c21"></a>
### C21 · cell 33: PCA with SVD · prose · **REVIEW**

baseline L574 → branch L580

```diff
- # While we could consider loading information about the legislator, such as their party, and see how this relates to their voting pattern, it turns out that we can do a lot with PCA to cluster legislators by how they vote. Let's calculate the principal components using the SVD method.
+ # While we could consider loading information about the legislator, such as their party, and see how this relates to their voting pattern, it turns out that we can do a lot with PCA to cluster legislators by how they vote. Let's calculate the principal components using the SVD method. `pl.exclude("member")` selects every roll call column, so we subtract each column's own mean and leave the member labels out of the matrix we decompose.
```

**Why:** Added clause naming `pl.exclude("member")`, which keeps the member labels out of the matrix being decomposed — centring them with the 41 vote columns would corrupt the SVD with every gate green.
**Verdict:** optional
**Minimal alternative:** move it to an inline comment on the code line; the paragraph now ends on a third clause that restates the section heading.

<a id="c22"></a>
### C22 · cell 34 [code] · code

baseline L577 → branch L583

```diff
- vote_pivot_centered = vote_pivot - np.mean(vote_pivot, axis=0)
+ vote_pivot_centered = vote_pivot.select(pl.exclude("member") - pl.exclude("member").mean())
```

**Why:** `vote_pivot - np.mean(vote_pivot, axis=0)` → `vote_pivot.select(pl.exclude("member") - pl.exclude("member").mean())`; `member` is data now, not an index, so it has to be excluded explicitly.
**Output:** same — the cell (`0563d901`) carries no committed output.

<a id="c23"></a>
### C23 · cell 38 [code] · code

baseline L594 → branch L600

```diff
- vote_2d = pd.DataFrame(index=vote_pivot_centered.index)
- vote_2d[["z1", "z2", "z3"]] = (u * s)[:, :3]
+ Z = (u * s)[:, :3]
+ vote_2d = pl.DataFrame(
+     {"member": vote_pivot["member"], "z1": Z[:, 0], "z2": Z[:, 1], "z3": Z[:, 2]}
+ )
```

**Why:** `pd.DataFrame(index=…)` seeded from an index has no Polars form. Rebuilt as an explicit frame with `member` from `vote_pivot` and `z1/z2/z3` sliced out of `u * s`.
**Output:** same — no committed output on this cell; the scatter it feeds (`f8039978`) drifts by ≤1.7e-14 relative.

<a id="c24"></a>
### C24 · cell 39 [markdown] · dropdown

baseline L616 → branch L624 · mirror of the next code cell (hard rule 3)

```diff
- # legs = pd.DataFrame(
- #     columns=[
+ # legs = pl.DataFrame(
+ #     schema=[
```

**Why:** Mirror of the legislator-loading cell: `pd.DataFrame(columns=…)` → `pl.DataFrame(schema=…)`. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — the mirrored cell's figure (`c6480b65`) drifts by ≤3.4e-14 relative, no sign change.

<a id="c25"></a>
### C25 · cell 39 [markdown] · dropdown

baseline L640 → branch L648 · mirror of the next code cell (hard rule 3)

```diff
+ #     orient="row",
```

**Why:** `orient="row"` added: a list-of-lists reads as *columns* in Polars, so without it the frame would be transposed. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — as C24.

<a id="c26"></a>
### C26 · cell 39 [markdown] · dropdown

baseline L641 → branch L650 · mirror of the next code cell (hard rule 3)

```diff
- # legs["age"] = 2024 - legs["birthday"].dt.year
- # legs.set_index("leg_id")
- # legs.sort_index()
+ # legs = legs.with_columns((2024 - pl.col("birthday").dt.year()).alias("age"))
```

**Why:** `legs["age"] = …` → `with_columns((2024 - pl.col("birthday").dt.year()).alias("age"))`. `legs.set_index("leg_id")` and `legs.sort_index()` were no-ops in the baseline — both returned discarded frames — so they were deleted rather than translated. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — as C24.

<a id="c27"></a>
### C27 · cell 39 [markdown] · dropdown

baseline L645 → branch L652 · mirror of the next code cell (hard rule 3)

```diff
- # vote_2d = vote_2d.join(legs.set_index("leg_id")).dropna()
+ # vote_2d = vote_2d.join(
+ #     legs, left_on="member", right_on="leg_id", how="inner", maintain_order="left"
+ # )
```

**Why:** The index-alignment join `join(legs.set_index("leg_id")).dropna()` made explicit. `maintain_order="left"` is load-bearing: three jitter columns are attached positionally immediately after. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — as C24; the `.dropna()` was doing an inner join's work, 439 rows either way.

<a id="c28"></a>
### C28 · cell 39 [markdown] · dropdown

baseline L648 → branch L657 · mirror of the next code cell (hard rule 3)

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

**Why:** Three `df["col"] = …` assignments folded into one `with_columns`; same three `np.random.normal` draws in the same order under the same seed. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — as C24; the jitter is identical.

<a id="c29"></a>
### C29 · cell 40 [code] · code

baseline L669 → branch L680

```diff
- legs = pd.DataFrame(
-     columns=[
+ legs = pl.DataFrame(
+     schema=[
```

**Why:** Code half of C24.
**Output:** differs — figure only, ≤3.4e-14 relative.

<a id="c30"></a>
### C30 · cell 40 [code] · code

baseline L693 → branch L704

```diff
+     orient="row",
```

**Why:** Code half of C25.
**Output:** differs — as C29.

<a id="c31"></a>
### C31 · cell 40 [code] · code

baseline L694 → branch L706

```diff
- legs["age"] = 2024 - legs["birthday"].dt.year
- legs.set_index("leg_id")
- legs.sort_index()
+ legs = legs.with_columns((2024 - pl.col("birthday").dt.year()).alias("age"))
```

**Why:** Code half of C26.
**Output:** differs — as C29.

<a id="c32"></a>
### C32 · cell 40 [code] · code

baseline L698 → branch L708

```diff
- vote_2d = vote_2d.join(legs.set_index("leg_id")).dropna()
+ vote_2d = vote_2d.join(
+     legs, left_on="member", right_on="leg_id", how="inner", maintain_order="left"
+ )
```

**Why:** Code half of C27.
**Output:** differs — as C29.

<a id="c33"></a>
### C33 · cell 40 [code] · code

baseline L701 → branch L713

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

**Why:** Code half of C28.
**Output:** differs — as C29.

<a id="c34"></a>
### C34 · cell 41 [markdown] · prose · **REVIEW**

baseline L721 → branch L735

```diff
- # vote_2d["num votes"] = votes[votes["vote"].isin(["Yes", "No"])].groupby("member").size()
- # vote_2d.dropna(inplace=True)
+ # num_votes = votes.filter(pl.col("vote").is_in(["Yes", "No"])).group_by("member").agg(pl.len().alias("num votes"))
+ # vote_2d = vote_2d.join(num_votes, on="member", how="inner")
```

**Why:** `groupby("member").size()` assigned onto an index-aligned column plus `dropna(inplace=True)` becomes `group_by(...).agg(pl.len().alias("num votes"))` and an inner join. The hunk sits inside an HTML-commented block, so no reader would see it even if the chapter were built; it was converted so no pandas survives under `content/`.
**Verdict:** necessary

<a id="c35"></a>
### C35 · cell 43 [markdown] · dropdown

baseline L751 → branch L765 · mirror of the next code cell (hard rule 3)

```diff
- #     vote_pivot_centered.join(legs.set_index("leg_id")["party"])
- #     .groupby("party")
+ #     vote_pivot_centered.with_columns(member=vote_pivot["member"])
+ #     .join(legs.select("leg_id", "party"), left_on="member", right_on="leg_id")
+ #     .drop("member")
+ #     .group_by("party")
```

**Why:** Mirror of the party-means cell: the index join becomes re-attach `member`, join on it, drop it, then group. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** same — the figure this mirrors (`3a95dcc1`) is byte-identical to the baseline apart from plotly serialising two template values as `0.0` instead of `0`.

<a id="c36"></a>
### C36 · cell 43 [markdown] · dropdown

baseline L754 → branch L770 · mirror of the next code cell (hard rule 3)

```diff
- #     .T.reset_index()
- #     .rename(columns={"index": "call"})
- #     .melt("call")
+ #     .sort("party")
+ #     .unpivot(index="party", variable_name="call", value_name="value")
```

**Why:** `.T.reset_index().rename().melt()` existed only to get roll calls into rows; `unpivot(index="party", …)` does it in one step, and `.sort("party")` pins facet-row order, which Polars does not guarantee. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** same — as C35.

<a id="c37"></a>
### C37 · cell 44 [code] · code

baseline L769 → branch L784

```diff
-     vote_pivot_centered.join(legs.set_index("leg_id")["party"])
-     .groupby("party")
+     vote_pivot_centered.with_columns(member=vote_pivot["member"])
+     .join(legs.select("leg_id", "party"), left_on="member", right_on="leg_id")
+     .drop("member")
+     .group_by("party")
```

**Why:** Code half of C35.
**Output:** same — figure unchanged.

<a id="c38"></a>
### C38 · cell 44 [code] · code

baseline L772 → branch L789

```diff
-     .T.reset_index()
-     .rename(columns={"index": "call"})
-     .melt("call")
+     .sort("party")
+     .unpivot(index="party", variable_name="call", value_name="value")
```

**Why:** Code half of C36 — 123 rows (3 parties × 41 calls), as in pandas.
**Output:** same — figure unchanged.

<a id="c39"></a>
### C39 · cell 45: Biplot · dropdown

baseline L788 → branch L804 · mirror of the next code cell (hard rule 3)

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

**Why:** Mirror of the biplot cell: the loadings frame's index becomes an explicit `call` column, because it is iterated by row below. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — the biplot (`d14ea484`) drifts by ≤3.4e-14 relative; no arrow or point changed sign.

<a id="c40"></a>
### C40 · cell 45: Biplot · dropdown

baseline L793 → branch L812 · mirror of the next code cell (hard rule 3)

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

**Why:** Same `groupby().size()` → `group_by().agg(pl.len().alias("num votes"))` rewrite as C34, here in the live path. The `.alias` is kept because the string is a plotly legend label. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — as C39; 435 members sized, same as pandas.

<a id="c41"></a>
### C41 · cell 45: Biplot · dropdown

baseline L811 → branch L834 · mirror of the next code cell (hard rule 3)

```diff
- # for (call, pc1, pc2) in loadings.head(20).itertuples():
+ # for (call, pc1, pc2) in loadings.head(20).iter_rows():
```

**Why:** `itertuples()` → `iter_rows()`; both yield `(call, pc1, pc2)` now that `call` is a column. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — as C39; the same 20 arrows.

<a id="c42"></a>
### C42 · cell 46 [code] · code

baseline L821 → branch L844

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

**Why:** Code half of C39.
**Output:** differs — as C39.

<a id="c43"></a>
### C43 · cell 46 [code] · code

baseline L826 → branch L852

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

**Why:** Code half of C40.
**Output:** differs — as C39.

<a id="c44"></a>
### C44 · cell 46 [code] · code

baseline L844 → branch L874

```diff
- for (call, pc1, pc2) in loadings.head(20).itertuples():
+ for (call, pc1, pc2) in loadings.head(20).iter_rows():
```

**Why:** Code half of C41.
**Output:** differs — as C39.

<a id="c45"></a>
### C45 · cell 49: Invert and normalize the images so they look better · dropdown

baseline L1196 → branch L1226 · mirror of the next code cell (hard rule 3)

```diff
- # img_mat = -1 * train_images[sample_idx].astype(np.int16)
+ # img_mat = -1 * np.asarray(train_images[sample_idx], dtype=np.int16)
```

**Why:** `train_images[sample_idx].astype(np.int16)` → `np.asarray(train_images[sample_idx], dtype=np.int16)`; both sides NumPy, the explicit `asarray` makes the cast independent of what `load_data` returns. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — see C70 (cache log) and C71.

<a id="c46"></a>
### C46 · cell 49: Invert and normalize the images so they look better · dropdown

baseline L1199 → branch L1229 · mirror of the next code cell (hard rule 3)

```diff
- # images = pd.DataFrame(
+ # images = pl.DataFrame(
```

**Why:** `pd.DataFrame` → `pl.DataFrame` for the Fashion-MNIST frame. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — see C71.

<a id="c47"></a>
### C47 · cell 49: Invert and normalize the images so they look better · dropdown

baseline L1201 → branch L1231 · mirror of the next code cell (hard rule 3)

```diff
- #         "images": img_mat.tolist(),
+ #         "images": img_mat,
```

**Why:** `img_mat.tolist()` → `img_mat`: Polars takes the 3-D ndarray directly and types the column `array[f64, (28, 28)]`, where pandas needed nested Python lists. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — see C71.

<a id="c48"></a>
### C48 · cell 50 [code] · code

baseline L1232 → branch L1262

```diff
- img_mat = -1 * train_images[sample_idx].astype(np.int16)
+ img_mat = -1 * np.asarray(train_images[sample_idx], dtype=np.int16)
```

**Why:** Code half of C45.
**Output:** differs — see C70; image shapes unchanged.

<a id="c49"></a>
### C49 · cell 50 [code] · code

baseline L1235 → branch L1265

```diff
- images = pd.DataFrame(
+ images = pl.DataFrame(
```

**Why:** Code half of C46.
**Output:** differs — see C71.

<a id="c50"></a>
### C50 · cell 50 [code] · code

baseline L1237 → branch L1267

```diff
-         "images": img_mat.tolist(),
+         "images": img_mat,
```

**Why:** Code half of C47.
**Output:** differs — see C71.

<a id="c51"></a>
### C51 · cell 51 [markdown] · dropdown

baseline L1252 → branch L1282 · mirror of the next code cell (hard rule 3)

```diff
- #     img_mat = np.array(images.head(max_images)["images"].to_list())
+ #     img_mat = images.head(max_images)["images"].to_numpy()
```

**Why:** `np.array(images.head(max_images)["images"].to_list())` → `images.head(max_images)["images"].to_numpy()`; the array column already has a shape, so the round-trip through a Python list goes. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — the figure redraws; see C56.

<a id="c52"></a>
### C52 · cell 51 [markdown] · dropdown

baseline L1263 → branch L1293 · mirror of the next code cell (hard rule 3)

```diff
- #         lambda a: a.update(text=images.iloc[int(a.text.split("=")[-1])]["class"])
+ #         lambda a: a.update(text=images["class"][int(a.text.split("=")[-1])])
```

**Why:** `images.iloc[i]["class"]` → `images["class"][i]` — positional access with no index in play. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — as C51. Facet labels stay correct: the lambda looks the class up by the same positional index the facet was built from.

<a id="c53"></a>
### C53 · cell 51: keep two rows drawn at random from each class · dropdown

baseline L1268 → branch L1298 · mirror of the next code cell (hard rule 3)

```diff
- # fig = show_images(images.groupby("class", as_index=False).sample(2), ncols=6)
+ # # keep two rows drawn at random from each class
+ # two_per_class = images.filter(pl.int_range(pl.len()).shuffle(seed=23).over("class") < 2).sort("class")
+ # fig = show_images(two_per_class, ncols=6)
```

**Why:** `groupby("class", as_index=False).sample(2)` → `filter(pl.int_range(pl.len()).shuffle(seed=23).over("class") < 2).sort("class")`. `.over` is the group, `.sort("class")` restores the grouped grid (the window filter returns original frame order), and `seed=23` re-seeds a figure that would otherwise be unseeded, because `np.random.seed` does not govern Polars' RNG. Mirror re-checked against the code cell it repeats: identical (hard rule 3).
**Output:** differs — see C56.

<a id="c54"></a>
### C54 · cell 52 [code] · code

baseline L1276 → branch L1308

```diff
-     img_mat = np.array(images.head(max_images)["images"].to_list())
+     img_mat = images.head(max_images)["images"].to_numpy()
```

**Why:** Code half of C51.
**Output:** differs — see C56.

<a id="c55"></a>
### C55 · cell 52 [code] · code

baseline L1287 → branch L1319

```diff
-         lambda a: a.update(text=images.iloc[int(a.text.split("=")[-1])]["class"])
+         lambda a: a.update(text=images["class"][int(a.text.split("=")[-1])])
```

**Why:** Code half of C52.
**Output:** differs — see C56.

<a id="c56"></a>
### C56 · cell 52 [code] · code

baseline L1292 → branch L1324

```diff
- fig = show_images(images.groupby("class", as_index=False).sample(2), ncols=6)
+ # keep two rows drawn at random from each class
+ two_per_class = images.filter(pl.int_range(pl.len()).shuffle(seed=23).over("class") < 2).sort("class")
+ fig = show_images(two_per_class, ncols=6)
```

**Why:** Code half of C53 — the per-class sample as a window filter.
**Output:** differs — the Fashion-MNIST grids are the only figures in this chapter that genuinely redraw: all 20 garments differ from the baseline's (0 of 20 identical, checked pixel-wise), in the same ten classes, same order, correctly labelled. Not in the report's output list, which covers text outputs only.

<a id="c57"></a>
### C57 · cell 54 [code] · code

baseline L1301 → branch L1335

```diff
- show_images(images.groupby('class',as_index=False).sample(2), ncols=6)
+ 
+ # keep two rows drawn at random from each class
+ two_per_class = images.filter(pl.int_range(pl.len()).shuffle(seed=23).over("class") < 2).sort("class")
+ show_images(two_per_class, ncols=6)
```

**Why:** Student-visible copy of the same sampling change. The cell still opens with quarto's `#| code-fold: true`, which MyST does not read — pre-existing, and one of the reasons CONVERSIONS.md recommends deleting this chapter.
**Output:** differs — as C56; the `print(class_dict)` text above the figure is identical.

<a id="c58"></a>
### C58 · cell 58 [code] · code

baseline L1314 → branch L1351

```diff
- X = np.array(images["images"].to_list())
+ X = images["images"].to_numpy()
```

**Why:** `np.array(images["images"].to_list())` → `images["images"].to_numpy()`.
**Output:** same — `X.shape` is `(5000, 28, 28)` on both sides.

<a id="c59"></a>
### C59 · cell 68 [code] · code

baseline L1357 → branch L1394

```diff
- images[['z1', 'z2', 'z3']] = pca.transform(X)[:, :3]
+ images = images.hstack(pl.DataFrame(pca.transform(X)[:, :3], schema=["z1", "z2", "z3"]))
```

**Why:** `images[['z1','z2','z3']] = pca.transform(X)[:, :3]` has no Polars form; rewritten as `hstack` of a named three-column frame, which is positional — the same alignment the pandas assignment had.
**Output:** differs — the 3-D scatter (`d3493bae`) drifts by ≤3.7e-14 relative, no axis flipped. The neighbouring scree plot (`dd2e7cb1`) moves ~6e-5 relative because `PCA(n_components=50)` on 5000×784 uses sklearn's randomized solver with no `random_state` — unseeded in the baseline too, so pre-existing.

<a id="c60"></a>
### C60 · `import polars as pl` · output

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

**Why:** `pl.read_csv` returns a Polars frame, so `.head()` renders Polars' box table: `shape:` line, dtype row, no index column.
**Reader sees:** equivalent — the same five rectangles with the same values.

<a id="c61"></a>
### C61 · `pl.DataFrame(U).head(5)` · output

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

**Why:** Display-wrapper change gives `column_0…column_3` instead of `0…3`. Separately the fourth column's numbers moved: `rectangle_data` is rank 3, the fourth singular value is ~1e-14, and LAPACK may return any unit vector in that null direction. Verified live in the d100 env that pandas and Polars inputs give identical new values — the change is this machine's LAPACK against the baseline's, not the conversion.
**Reader sees:** changed: the fourth column's five numbers. The first three columns, which are what the section is about, are identical to every printed digit.

<a id="c62"></a>
### C62 · `S` · output

committed output

```diff
- [text] array([3.62932568e+02, 6.29904732e+01, 2.56544651e+01, 1.75309971e-14])
+ [text] array([3.62932568e+02, 6.29904732e+01, 2.56544651e+01, 9.92685575e-15])
```

**Why:** The fourth singular value, mathematically zero, re-executed to a different float. Same LAPACK difference as C61.
**Reader sees:** changed: 1.75e-14 → 9.93e-15, both practically zero. The three real singular values are unchanged.

<a id="c63"></a>
### C63 · `Sm = np.diag(S)` · output

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

**Why:** `np.diag(S)` propagates C62 into the bottom-right entry.
**Reader sees:** changed: one entry, both values practically zero.

<a id="c64"></a>
### C64 · `pl.DataFrame(Vt)` · output

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

**Why:** Display wrapper plus Polars' six-significant-figure formatting; the `-8.70e-17` entry also re-executed to `-5.27e-17` (same null-direction noise).
**Reader sees:** equivalent — every row of $V^T$ keeps its sign and value, so no principal component flipped.

<a id="c65"></a>
### C65 · `pl.DataFrame(U @ Sm @ Vt).head(5)` · output

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

**Why:** Display wrapper only; $USV^T$ is computed in NumPy either way.
**Reader sees:** equivalent — the rectangle data recovered exactly, as before.

<a id="c66"></a>
### C66 · `centered_df = rectangle.select(pl.all() - pl.all().mean())` · output

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

**Why:** Render change: the centring is now a Polars expression, so the result prints as a Polars frame.
**Reader sees:** equivalent — the centred values are elementwise identical.

<a id="c67"></a>
### C67 · `two_PCs = Vt.T[:, :2]` · output

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

<a id="c68"></a>
### C68 · `import polars as pl` · output

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

**Why:** `pl.read_csv` plus `cast` in place of `astype`; Polars' table render with a dtype row.
**Reader sees:** equivalent — the same first five roll-call records, `roll call` still a string.

<a id="c69"></a>
### C69 · `was_yes = (pl.element().first() == "Yes").cast(pl.Int64)` · output

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

**Why:** `member` is a column in Polars and was an index in pandas, so the printed shape gains one. The values come from the aggregate expression that replaced `was_yes`; `sort_columns=True` and `.sort("member")` reproduce the baseline's column and row order.
**Reader sees:** changed: the stdout line reads `(441, 42)` rather than `(441, 41)`, and `member` is the first column rather than the index. Same 441 legislators, same 41 roll calls, same 0/1 values. Unlike `pca`, this chapter has no paragraph reading the new number — see C16.

<a id="c70"></a>
### C70 · `fig = px.line(y=s**2 / sum(s**2), title='Variance Explained', width=70` · output

committed output

```diff
- [plotly] figure md5:4406e2a3e6
- [plotly] trace 0 scatter
- [plotly] title='Variance Explained'
+ [plotly] figure md5:4bbdcf8567
+ [plotly] trace 0 scatter
+ [plotly] title='Variance Explained'
```

**Why:** The archived twin of `pca` C93. The SVD is re-executed on the Polars-centred matrix and the 41 proportions move by at most 1.1e-16.
**Reader sees:** equivalent — sub-ULP on the scree line. The chapter is outside `myst.yml`'s TOC, so it is never built either way.

<a id="c71"></a>
### C71 · `Z = (u * s)[:, :3]` · output

committed output

```diff
- [plotly] figure md5:d02497acf9
- [plotly] trace 0 scatter3d
- [plotly] title='Vote Data'
+ [plotly] figure md5:c74d925da7
+ [plotly] trace 0 scatter3d
+ [plotly] title='Vote Data'
```

**Why:** `pca` C94's twin: same 441 legislators, coordinates within 5.5e-14, and no sign flip on any of the three components — the `.sort("member")` fix shipped here too.
**Reader sees:** equivalent.

<a id="c72"></a>
### C72 · `legislators_data = yaml.safe_load(open("data/legislators-2019.yaml"))` · output

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

**Why:** `pca` C95's twin: five party/gender traces in the same order with 184/15/1/148/91 points, coordinates within 5.5e-14, and the jitter still attached to the right legislators.
**Reader sees:** equivalent.

<a id="c73"></a>
### C73 · `fig_eig = px.bar(x=vote_pivot_centered.columns, y=vt[0, :])` · output

committed output

```diff
- [plotly] figure md5:2083efd31f
- [plotly] trace 0 bar x: n=41
+ [plotly] figure md5:2d63ff2b38
+ [plotly] trace 0 bar x: n=41
```

**Why:** `pca` C96's twin. The roll calls come back in the same order and the PC1 loadings differ by at most 2.2e-16, sign unchanged.
**Reader sees:** equivalent.

<a id="c74"></a>
### C74 · `party_line_votes = (` · output

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

**Why:** `pca` C97's twin, and the one figure in this chapter whose trace data is byte-identical to the baseline — `unpivot` plus `.sort("party")` reproduce every bar. The md5 moves purely on plotly writing `[0.0, 1.0]` where the committed baseline had `[0, 1]`.
**Reader sees:** equivalent.

<a id="c75"></a>
### C75 · `loadings = pl.DataFrame(` · output

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

**Why:** `pca` C98's twin: 25 traces, same names and order, coordinates within 5.5e-14, and no loading arrow negated.
**Reader sees:** equivalent.

<a id="c76"></a>
### C76 · `class_names = [` · output

committed output

```diff
- [stdout] Using cached version that was downloaded (UTC): Wed Jan  7 21:18:58 2026
- [stdout] Using cached version that was downloaded (UTC): Wed Jan  7 21:18:58 2026
- [stdout] Using cached version that was downloaded (UTC): Wed Jan  7 21:18:58 2026
- [stdout] Using cached version that was downloaded (UTC): Wed Jan  7 21:18:58 2026
- [stdout] Training images (60000, 28, 28)
- [stdout] Test images (10000, 28, 28)
+ [stdout] Using cached version that was downloaded (UTC): Sun Aug 16 22:33:58 2026
+ [stdout] Using cached version that was downloaded (UTC): Sun Aug 16 22:33:58 2026
+ [stdout] Using cached version that was downloaded (UTC): Sun Aug 16 22:33:58 2026
+ [stdout] Using cached version that was downloaded (UTC): Sun Aug 16 22:33:58 2026
+ [stdout] Training images (60000, 28, 28)
+ [stdout] Test images (10000, 28, 28)
```

**Why:** The notebook was re-executed, so the cached-download log carries the new execution date.
**Reader sees:** equivalent — the four cache lines print the re-execution date (Aug 2026) instead of the baseline's (Jan 2026); the image shapes beneath them, (60000, 28, 28) and (10000, 28, 28), are identical.

<a id="c77"></a>
### C77 · `def show_images(images, ncols=5, max_images=30):` · output

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

**Why:** `pca` C100's twin — the unseeded pandas `groupby("class").sample(2)` became `shuffle(seed=23).over("class")`, a different RNG stream, so all 20 panels are different images with zero overlap against the baseline's.
**Reader sees:** changed: 20 new garments. Same ten classes in the same facet order, and the titles are generated from the data so they stay correct. Not built — the chapter is outside the TOC.

<a id="c78"></a>
### C78 · `print(class_dict)` · output

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

**Why:** `pca` C101's twin. Same seeded draw as C77, so the two grids in this chapter now show identical clothes where the baseline's two drew independently.
**Reader sees:** changed: 20 new garments, and the grid repeats C77 exactly.

<a id="c79"></a>
### C79 · `images.head()` · output

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

**Why:** `img_mat.tolist()` → `img_mat` types the column as a native `array[f64, (28, 28)]` rather than nested Python lists, and `labels` keeps `u8`.
**Reader sees:** equivalent — the same five images, labels and classes in the same order; only the printed dtype and the elision change.

<a id="c80"></a>
### C80 · `fig = px.line(y=pca.explained_variance_ratio_ * 100, markers=True)` · output

committed output

```diff
- [plotly] figure md5:c4c87adaef
- [plotly] trace 0 scatter
+ [plotly] figure md5:504421f477
+ [plotly] trace 0 scatter
```

**Why:** `pca` C103's twin — sklearn's unseeded randomized SVD redraws the tail of the 50-component scree plot. Components 1-40 agree to ~1e-13; the biggest move is component 46, 0.17423% -> 0.17598%.
**Reader sees:** equivalent — 0.0018 percentage points on an axis that runs to 29%.

<a id="c81"></a>
### C81 · `images = images.hstack(pl.DataFrame(pca.transform(X)[:, :3], schema=["` · output

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

**Why:** `pca` C104's twin. Ten class traces with the same names, order and sizes; `pca.transform` output within 1.9e-13.
**Reader sees:** equivalent.

