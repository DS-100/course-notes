# _decision_tree — change report

`887a578b0a4b:content/_decision_tree/decision_tree.ipynb` → `content/_decision_tree/decision_tree.ipynb`

**Tier B · 17 changes:** output 10 · prose 1 · dropdown 1 · code 5

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

Archived chapter, out of the toc. The Polars work is small — an import, a `read_csv`, and one chained boolean mask that became `filter`. What matters here is not conversion: `random_state=42` was added to both `DecisionTreeClassifier` constructions (C3, C7) and a false threshold in the prose was corrected (C4). Ten outputs move, most of them because `iris_data.sample(5)` and `.sample(4)` are unseeded on both sides and redraw on every execution. Read C3 and C4 together: without a seed the entropy tree's root split is genuinely unstable — an unseeded refit in the pinned env chose `petal_width <= 0.8` where the committed figure shows `petal_length <= 2.45` — so the seed is what keeps C4's sentence true against the figure above it. C17 is the one figure whose content really moved.

## Needs review

- [C4](#c4) · cell 23 [markdown]

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C8](#c8) · `iris_data = pl.read_csv("data/iris.csv")`
- [C9](#c9) · `logistic_regression_model.predict([[1.4, 0.2]])`
- [C10](#c10) · `from matplotlib.colors import ListedColormap`
- [C11](#c11) · `four_random_rows = iris_data.sample(4)`
- [C12](#c12) · `decision_tree_model.predict(four_random_rows[["petal_length", "petal_w`
- [C13](#c13) · `import graphviz`
- [C14](#c14) · `from matplotlib.colors import ListedColormap`
- [C15](#c15) · `iris_data.filter(`
- [C16](#c16) · `sns.scatterplot(data = iris_data, x = "sepal_length", y="sepal_width",`
- [C17](#c17) · `sepal_decision_tree_model = tree.DecisionTreeClassifier(criterion="ent`

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C6](#c6) · cell 33 [markdown]

## Changes

<a id="c1"></a>
### C1 · cell 4 [code] · code

baseline L32 → branch L32

```diff
- import pandas as pd
+ import polars as pl
```

**Why:** Import rename.
**Output:** same.

<a id="c2"></a>
### C2 · cell 7 [code] · code

baseline L59 → branch L59

```diff
- iris_data = pd.read_csv("data/iris.csv")
+ iris_data = pl.read_csv("data/iris.csv")
```

**Why:** `pd.read_csv` → `pl.read_csv`; the file has no NA tokens and no index column, so nothing else was needed.
**Output:** differs: the displayed head is a fresh unseeded `.sample(5)` in Polars' repr — see C8.

<a id="c3"></a>
### C3 · cell 17 [code] · code

baseline L159 → branch L159

```diff
- decision_tree_model = tree.DecisionTreeClassifier(criterion='entropy')
+ decision_tree_model = tree.DecisionTreeClassifier(criterion='entropy', random_state=42)
```

**Why:** Not a Polars change. `DecisionTreeClassifier` breaks ties between equally good splits with its RNG, so the fitted tree — and the threshold C4's sentence quotes — is not reproducible across executions: an unseeded refit in the pinned env chose `petal_width <= 0.8` as the root where the committed graphviz shows `petal_length <= 2.45` (verified). The seed pins the figure to the prose.
**Output:** same in fact: the committed tree has the same 15 nodes and the same seven split thresholds as the baseline's (verified against both SVGs). The seed removes the chance that the next execution differs.

<a id="c4"></a>
### C4 · cell 23 [markdown] · prose · **REVIEW**

baseline L195 → branch L195

```diff
- # This visualization allows us to see exactly how the decision tree classifies each point. For example, if the `petal_length` of an iris flower is less than or equal to 1.75, we would classify it as `setosa`.
+ # This visualization allows us to see exactly how the decision tree classifies each point. For example, if the `petal_length` of an iris flower is less than or equal to 2.45, we would classify it as `setosa`.
```

**Why:** The baseline's threshold was simply wrong: the root split is `petal_length <= 2.45`, and 1.75 is the `petal_width` split two levels down. This is true of the baseline's own committed graphviz as well as the branch's. Not recorded in CONTRADICTIONS.md — that sweep covered the 18 live chapters, not this archived one.
**Verdict:** necessary — a fix to a false claim, and pre-existing. Worth logging alongside the §A entries if staff are tracking pre-existing content errors rather than just conversion-introduced ones.

<a id="c5"></a>
### C5 · cell 29 [code] · code

baseline L262 → branch L262

```diff
- iris_data[(iris_data["petal_length"]> 2.45)&(iris_data["petal_width"]> 1.75)&(iris_data["petal_length"]<=4.85)]
+ iris_data.filter(
+     (pl.col("petal_length") > 2.45)
+     & (pl.col("petal_width") > 1.75)
+     & (pl.col("petal_length") <= 4.85)
+ )
```

**Why:** Chained boolean masks on a frame become one `filter` over `pl.col` expressions; the parentheses and `&` carry over unchanged.
**Output:** same three rows (C15).

<a id="c6"></a>
### C6 · cell 33 [markdown] · dropdown

baseline L287 → branch L291 · mirror of the next code cell (hard rule 3)

```diff
- # sepal_decision_tree_model = tree.DecisionTreeClassifier(criterion="entropy")
+ # sepal_decision_tree_model = tree.DecisionTreeClassifier(criterion="entropy", random_state=42)
```

**Why:** Mirrors C7 — the same seed argument.
**Output:** same — no output; the mirrored copy matches C7.

<a id="c7"></a>
### C7 · cell 34 [code] · code

baseline L305 → branch L309

```diff
- sepal_decision_tree_model = tree.DecisionTreeClassifier(criterion="entropy")
+ sepal_decision_tree_model = tree.DecisionTreeClassifier(criterion="entropy", random_state=42)
```

**Why:** Same reasoning as C3, but note it is inert on this line: the very next statement rebinds `sepal_decision_tree_model = decision_tree_model.fit(...)`, so the freshly constructed classifier is thrown away and the model actually plotted is `decision_tree_model`, which carries its seed from C3. That rebinding is pre-existing and unchanged by this branch, but it is worth a look on its own.
**Output:** differs: the sepal decision surface moved — see C17.

<a id="c8"></a>
### C8 · `iris_data = pl.read_csv("data/iris.csv")` · output

committed output

```diff
- [text]      sepal_length  sepal_width  petal_length  petal_width     species
- [text] 88            5.6          3.0           4.1          1.3  versicolor
- [text] 41            4.5          2.3           1.3          0.3      setosa
- [text] 119           6.0          2.2           5.0          1.5   virginica
- [text] 25            5.0          3.0           1.6          0.2      setosa
- [text] 18            5.7          3.8           1.7          0.3      setosa
+ [text] shape: (5, 5)
+ [text] ┌──────────────┬─────────────┬──────────────┬─────────────┬────────────┐
+ [text] │ sepal_length ┆ sepal_width ┆ petal_length ┆ petal_width ┆ species    │
+ [text] │ ---          ┆ ---         ┆ ---          ┆ ---         ┆ ---        │
+ [text] │ f64          ┆ f64         ┆ f64          ┆ f64         ┆ str        │
+ [text] ╞══════════════╪═════════════╪══════════════╪═════════════╪════════════╡
+ [text] │ 5.4          ┆ 3.9         ┆ 1.7          ┆ 0.4         ┆ setosa     │
+ [text] │ 5.9          ┆ 3.0         ┆ 4.2          ┆ 1.5         ┆ versicolor │
+ [text] │ 4.6          ┆ 3.1         ┆ 1.5          ┆ 0.2         ┆ setosa     │
+ [text] │ 6.3          ┆ 3.3         ┆ 6.0          ┆ 2.5         ┆ virginica  │
+ [text] │ 7.6          ┆ 3.0         ┆ 6.6          ┆ 2.1         ┆ virginica  │
+ [text] └──────────────┴─────────────┴──────────────┴─────────────┴────────────┘
```

**Why:** `iris_data.sample(5)` is unseeded on both sides, so the five rows are a new draw; plus Polars' repr.
**Reader sees:** changed: five different flowers, and no row labels. Equivalent as an illustration, but this output will churn on every execution unless a `seed=` is added.

<a id="c9"></a>
### C9 · `logistic_regression_model.predict([[1.4, 0.2]])` · output

committed output

```diff
- [text] array(['setosa'], dtype=object)
+ [text] array(['setosa'], dtype='<U10')
```

**Why:** The labels now come from a Polars string column, so sklearn returns a NumPy unicode array instead of the object array pandas produced.
**Reader sees:** changed: only the printed dtype (`dtype=object` → `dtype='<U10'`). The prediction is the same.

<a id="c10"></a>
### C10 · `from matplotlib.colors import ListedColormap` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 59848 bytes md5:6d826f05f4
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 59796 bytes md5:5dce9d2d5b
```

**Why:** Re-rendered decision-region plot.
**Reader sees:** equivalent — pixel-diffed against the baseline, 0.4% of pixels differ and it is all marker antialiasing; the regions and the points coincide.

<a id="c11"></a>
### C11 · `four_random_rows = iris_data.sample(4)` · output

committed output

```diff
- [text]      sepal_length  sepal_width  petal_length  petal_width     species
- [text] 15            5.7          4.4           1.5          0.4      setosa
- [text] 0             5.1          3.5           1.4          0.2      setosa
- [text] 112           6.8          3.0           5.5          2.1   virginica
- [text] 86            6.7          3.1           4.7          1.5  versicolor
+ [text] shape: (4, 5)
+ [text] ┌──────────────┬─────────────┬──────────────┬─────────────┬────────────┐
+ [text] │ sepal_length ┆ sepal_width ┆ petal_length ┆ petal_width ┆ species    │
+ [text] │ ---          ┆ ---         ┆ ---          ┆ ---         ┆ ---        │
+ [text] │ f64          ┆ f64         ┆ f64          ┆ f64         ┆ str        │
+ [text] ╞══════════════╪═════════════╪══════════════╪═════════════╪════════════╡
+ [text] │ 4.9          ┆ 3.1         ┆ 1.5          ┆ 0.1         ┆ setosa     │
+ [text] │ 5.7          ┆ 4.4         ┆ 1.5          ┆ 0.4         ┆ setosa     │
+ [text] │ 5.7          ┆ 2.6         ┆ 3.5          ┆ 1.0         ┆ versicolor │
+ [text] │ 5.2          ┆ 2.7         ┆ 3.9          ┆ 1.4         ┆ versicolor │
+ [text] └──────────────┴─────────────┴──────────────┴─────────────┴────────────┘
```

**Why:** `iris_data.sample(4)`, unseeded on both sides — a new draw, in Polars' repr.
**Reader sees:** changed: four different flowers, and the original row labels (15, 0, 112, 86) are gone. Same churn caveat as C8.

<a id="c12"></a>
### C12 · `decision_tree_model.predict(four_random_rows[["petal_length", "petal_w` · output

committed output

```diff
- [text] array(['setosa', 'setosa', 'virginica', 'versicolor'], dtype=object)
+ [text] array(['setosa', 'setosa', 'versicolor', 'versicolor'], dtype='<U10')
```

**Why:** The predictions follow C11's new rows, and the dtype change from C9.
**Reader sees:** changed: `['setosa','setosa','virginica','versicolor']` → `['setosa','setosa','versicolor','versicolor']` — because the sampled flowers are different, not because the model is.

<a id="c13"></a>
### C13 · `import graphviz` · output

committed output

```diff
- [text] <graphviz.sources.Source at 0x31e2b7b10>
- [image/svg+xml] 20770 bytes md5:a66a2868c5
+ [text] <graphviz.sources.Source at 0x111bf1150>
+ [image/svg+xml] 19309 bytes md5:d7dce40cf9
```

**Why:** Re-rendered graphviz of the petal tree.
**Reader sees:** equivalent — verified identical in content: 15 nodes and the same seven thresholds in both SVGs, including the `petal_length <= 2.45` root that C4 now quotes. The byte difference is layout and serialization, and the object address in the text repr is per-process.

<a id="c14"></a>
### C14 · `from matplotlib.colors import ListedColormap` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 58996 bytes md5:cde8701707
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 59008 bytes md5:3b7de25add
```

**Why:** Re-rendered decision-region plot.
**Reader sees:** equivalent — 0.4% of pixels differ, antialiasing only.

<a id="c15"></a>
### C15 · `iris_data.filter(` · output

committed output

```diff
- [text]      sepal_length  sepal_width  petal_length  petal_width     species
- [text] 70            5.9          3.2           4.8          1.8  versicolor
- [text] 126           6.2          2.8           4.8          1.8   virginica
- [text] 138           6.0          3.0           4.8          1.8   virginica
+ [text] shape: (3, 5)
+ [text] ┌──────────────┬─────────────┬──────────────┬─────────────┬────────────┐
+ [text] │ sepal_length ┆ sepal_width ┆ petal_length ┆ petal_width ┆ species    │
+ [text] │ ---          ┆ ---         ┆ ---          ┆ ---         ┆ ---        │
+ [text] │ f64          ┆ f64         ┆ f64          ┆ f64         ┆ str        │
+ [text] ╞══════════════╪═════════════╪══════════════╪═════════════╪════════════╡
+ [text] │ 5.9          ┆ 3.2         ┆ 4.8          ┆ 1.8         ┆ versicolor │
+ [text] │ 6.2          ┆ 2.8         ┆ 4.8          ┆ 1.8         ┆ virginica  │
+ [text] │ 6.0          ┆ 3.0         ┆ 4.8          ┆ 1.8         ┆ virginica  │
+ [text] └──────────────┴─────────────┴──────────────┴─────────────┴────────────┘
```

**Why:** The `filter` result in Polars' repr.
**Reader sees:** changed: the same three rows and values, but the original row labels (70, 126, 138) are gone — those labels were how the reader could tell which flowers these were.

<a id="c16"></a>
### C16 · `sns.scatterplot(data = iris_data, x = "sepal_length", y="sepal_width",` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 64388 bytes md5:5ade2c9b1c
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 64412 bytes md5:fb9b4e3c68
```

**Why:** Re-rendered seaborn scatter, fed the Polars frame directly (no `.to_pandas()` added).
**Reader sees:** equivalent — 0.6% of pixels differ, antialiasing only.

<a id="c17"></a>
### C17 · `sepal_decision_tree_model = tree.DecisionTreeClassifier(criterion="ent` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 55064 bytes md5:ac7dea818f
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 54900 bytes md5:bc88d3935f
```

**Why:** This figure is the sepal-feature tree, and its content genuinely moved: with the entropy tie-break now seeded (C3/C7), the fitted tree differs from the one the baseline happened to draw.
**Reader sees:** changed: 3.4% of pixels differ and whole regions in the lower-left quadrant are reclassified — a different, equally overfit boundary. The lesson the figure teaches survives; the figure itself is not the baseline's.

