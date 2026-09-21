# logistic_regression_2 — change report

`887a578b0a4b:content/logistic_regression_2/logistic_reg_2.ipynb` → `content/logistic_regression_2/logistic_reg_2.ipynb`

**Tier B · 32 changes:** output 4 · prose 21 · dropdown 4 · tab-twins 1 · code 2

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

The lightest code surface of the four — two `np.mean` reductions and one float literal — and the heaviest prose list: 21 of 32 changes are prose, and almost all of them are §A2 fixes or MyST option repairs to pre-existing content. Three things to look at: C6/C7, which replace the chapter's "global minimum and a local minimum" reading of the MSE surface with the plateau the plotted function actually has (§A2 #1–2); C22, the PR-AUC floor (§A2 #3), wrong in the one section that exists to handle class imbalance; and C23–C27, four LaTeX corrections in the bonus derivation, which nothing in the build can check and which deserve a second reader. C18 is the only Polars-driven prose change, and it sits in a snippet that never executes.

## Needs review

- [C6](#c6) · cell 6 [markdown]
- [C7](#c7) · cell 6 [markdown]
- [C8](#c8) · cell 6 [markdown]
- [C11](#c11) · cell 8: Linear Separability and Regularization
- [C12](#c12) · cell 8: Linear Separability and Regularization
- [C13](#c13) · cell 8: Linear Separability and Regularization
- [C14](#c14) · cell 8: Linear Separability and Regularization
- [C15](#c15) · cell 8: Linear Separability and Regularization
- [C16](#c16) · cell 8: Regularized Logistic Regression
- [C17](#c17) · cell 8: Regularized Logistic Regression
- [C18](#c18) · cell 8: Performance Metrics
- [C19](#c19) · cell 8: Adjusting the Classification Threshold
- [C20](#c20) · cell 8: Precision-Recall Curves
- [C21](#c21) · cell 8: Precision-Recall Curves
- [C22](#c22) · cell 8: Precision-Recall Curves
- [C23](#c23) · cell 12: [BONUS] Gradient Descent for Logistic Regression
- [C24](#c24) · cell 12: [BONUS] Gradient Descent for Logistic Regression
- [C25](#c25) · cell 12: [BONUS] Gradient Descent for Logistic Regression
- [C26](#c26) · cell 12: [BONUS] Gradient Descent for Logistic Regression
- [C27](#c27) · cell 12: [BONUS] Gradient Descent for Logistic Regression
- [C28](#c28) · cell 12: [BONUS] AUC of the Random Predictor

## Outputs that changed

What the reader sees. CI never executes, so these ship exactly as committed.

- [C29](#c29) · `import warnings`
- [C30](#c30) · `def sigmoid(z):`
- [C31](#c31) · `def cross_entropy(y, p_hat):`
- [C32](#c32) · `thetas = np.linspace(0, 1)`

## Dropdown mirrors

Hard rule 3: each of these repeats a code cell verbatim and must move with it.

- [C1](#c1) · cell 1: Why Not MSE?
- [C2](#c2) · cell 1: Why Not MSE?
- [C4](#c4) · cell 4 [markdown]
- [C9](#c9) · cell 6: Motivating Cross-Entropy Loss

## Changes

<a id="c1"></a>
### C1 · cell 1: Why Not MSE? · dropdown

baseline L42 → branch L42 · spans code and prose; mirror of the next code cell (hard rule 3)

```diff
+ # import polars as pl
+ # import numpy as np
+ # import matplotlib.pyplot as plt
+ # np.seterr(divide='ignore')
+ #
+ # toy_df = pl.DataFrame({
+ #         "x": [-4.0, -2.0, -0.5, 1.0, 3.0, 5.0],
+ #         "y": [0, 0, 1, 0, 1, 1]})
+ # toy_df.head()
+ # ```
+ # ````
+ 
+ # %% tags=["remove-input", "remove-output"]
+ import warnings
+ warnings.filterwarnings("ignore")
+ 
+ import polars as pl
+ import numpy as np
+ import matplotlib.pyplot as plt
+ np.seterr(divide='ignore')
+ toy_df = pl.DataFrame({
+         "x": [-4.0, -2.0, -0.5, 1.0, 3.0, 5.0],
+         "y": [0, 0, 1, 0, 1, 1]})
+ toy_df.head()
+ 
+ # %% [markdown]
+ # <!-- tab-twins:begin 060a298c -->
+ # :::::{tab-set}
+ # :::: {tab-item} Polars
+ # :sync: pl
+ # ```python
+ # import warnings
+ # warnings.filterwarnings("ignore")
+ #
+ # import polars as pl
+ # import numpy as np
+ # import matplotlib.pyplot as plt
+ # np.seterr(divide='ignore')
+ # toy_df = pl.DataFrame({
+ #         "x": [-4.0, -2.0, -0.5, 1.0, 3.0, 5.0],
+ … 26 more lines
```

**Why:** Dropdown mirror of the setup cell, converted with its code cell (hard rule 3). The `x` literal became floats — required, not cosmetic: verified on the pin that `pl.DataFrame({"x": [-4, -2, -0.5, 1, 3, 5]})` raises `TypeError: unexpected value while building Series of type Int64; found value of type Float64: -0.5`, where pandas silently inferred `float64`. The literal now states what pandas inferred and what the baseline's own committed output already showed.
**Output:** differs — repr only (see C29); the same six rows.

<a id="c2"></a>
### C2 · cell 1: Why Not MSE? · dropdown

baseline L46 → branch L112 · mirror of the next code cell (hard rule 3)

```diff
- #
```

**Why:** A blank line inside the mirror. Staff note: the mirror still carries one blank line the code cell does not — verified that the same mismatch is present in the baseline, so it is inherited, not introduced, and CONVERSIONS.md already logs it. Everything else in the two matches verbatim.
**Output:** same — a mirror carries no output.

<a id="c3"></a>
### C3 · cell 3 [markdown] · tab-twins

baseline L52 → branch L117 · spans code and prose

```diff
- # ````
- 
- # %% tags=["remove-input"]
- import warnings
- warnings.filterwarnings("ignore")
- 
- import pandas as pd
- import numpy as np
- import matplotlib.pyplot as plt
- np.seterr(divide='ignore')
- toy_df = pd.DataFrame({
-         "x": [-4, -2, -0.5, 1, 3, 5],
-         "y": [0, 0, 1, 0, 1, 1]})
- toy_df.head()
- 
+ #
+ # ```text
+ #      x  y
+ # 0 -4.0  0
+ # 1 -2.0  0
+ # 2 -0.5  1
+ # 3  1.0  0
+ # 4  3.0  1
+ # ```
+ # ::::
+ # :::::
+ # <!-- tab-twins:end -->
```

**Why:** Twin `060a298c`'s pandas pane — the same construction spelled for pandas.
**Output:** differs — repr only; the same six rows, with `x` floating-point on both sides.

<a id="c4"></a>
### C4 · cell 4 [markdown] · dropdown

baseline L83 → branch L145 · mirror of the next code cell (hard rule 3)

```diff
- #     return np.mean((toy_df['y'] - p_hat)**2)
+ #     return ((toy_df['y'] - p_hat)**2).mean()
```

**Why:** Mirror of the MSE-on-toy-data helper, moved with its code cell and verified identical to it. `np.mean` raises on a Polars `Series`, so the reduction moves onto the expression.
**Output:** same.

<a id="c5"></a>
### C5 · cell 5 [code] · code

baseline L100 → branch L162

```diff
-     return np.mean((toy_df['y'] - p_hat)**2)
+     return ((toy_df['y'] - p_hat)**2).mean()
```

**Why:** Code-cell half of C4.
**Output:** same — CONVERSIONS.md records both 100-point loss surfaces recomputed under each library and found bit-identical, `inf` positions included, with the argmin unmoved at θ = 0.7576.

<a id="c6"></a>
### C6 · cell 6 [markdown] · prose · **REVIEW**

baseline L112 → branch L174

```diff
- # 1. The MSE loss surface is *non-convex*. There is both a global minimum and a (barely perceptible) local minimum in the loss surface above. This means that there is the risk of gradient descent converging on the local minimum of the loss surface, missing the true optimum parameter $\theta_1$.
+ # 1. The MSE loss surface is *non-convex*. It has one global minimum, at $\theta_1 \approx 0.54$, and the barely perceptible bump to its left is a local *maximum* at $\theta_1 \approx -2.1$. Past that bump the surface simply flattens out, falling towards $2/3$ as $\theta_1 \to -\infty$ without ever reaching a minimum. So gradient descent started far enough to the left does not converge on a second minimum — it stalls on a plateau where the gradient is nearly zero, and never reaches the true optimum $\theta_1$.
```

**Why:** §A2 #1, **pre-existing**. Scanning the exact function this cell plots over θ ∈ [−60, 20] finds one interior local minimum — the global one at θ ≈ 0.545 — and one interior local **maximum** at θ ≈ −2.09; the "barely perceptible" feature is the maximum. Left of it the surface is monotone toward the asymptote 2/3, so descent started far enough left stalls on a plateau rather than converging on a second minimum. The rewrite keeps the non-convexity point the section needs and fixes what the reader is told to see.
**Verdict:** necessary — a fix to a claim that was false (pre-existing).

<a id="c7"></a>
### C7 · cell 6 [markdown] · prose · **REVIEW**

baseline L115 → branch L177

```diff
- # :alt: MSE on toy classification data showing two possible minima
+ # :alt: MSE on toy classification data, plotted against theta-one. The curve has a single dip near theta-one = 0.5, a small hump to its left, and then a long flat plateau extending to the left at a height of about two thirds.
```

**Why:** §A2 #2, pre-existing — the same false claim in the alt text, where it was a screen-reader user's only description of the figure. Replaced with what is actually drawn.
**Verdict:** necessary — a fix to a claim that was false (pre-existing).

<a id="c8"></a>
### C8 · cell 6 [markdown] · prose · **REVIEW**

baseline L123 → branch L185

```diff
- # :width:400
+ # :width: 400
```

**Why:** The MyST option was written `:width:NNN` with no space after the colon, which MyST does not parse as an option at all. §A2's closing note records nine of these in this chapter; all are pre-existing.
**Verdict:** optional — a rendering repair the conversion did not require.
**Minimal alternative:** Restore `:width:400`, which ships an unparsed option and an unconstrained image. Minimal, but not recommended.

<a id="c9"></a>
### C9 · cell 6: Motivating Cross-Entropy Loss · dropdown

baseline L189 → branch L251 · mirror of the next code cell (hard rule 3)

```diff
- #     return np.mean(cross_entropy(toy_df['y'], p_hat))
+ #     return cross_entropy(toy_df['y'], p_hat).mean()
```

**Why:** Mirror of the mean-cross-entropy helper, moved with its code cell (hard rule 3) and verified identical to it. `np.mean` raises on a Polars `Series`, so the reduction moves onto the expression that produces it.
**Output:** same.

<a id="c10"></a>
### C10 · cell 7 [code] · code

baseline L204 → branch L266

```diff
-     return np.mean(cross_entropy(toy_df['y'], p_hat))
+     return cross_entropy(toy_df['y'], p_hat).mean()
```

**Why:** Code-cell half of C9. Required, not stylistic: `np.mean` on a `pl.Series` raises `TypeError` because NumPy passes an `axis` argument the Polars signature does not take.
**Output:** same — the mean cross-entropy curve is unchanged; CONVERSIONS.md records the surface as bit-identical under both libraries.

<a id="c11"></a>
### C11 · cell 8: Linear Separability and Regularization · prose · **REVIEW**

baseline L281 → branch L343

```diff
- # :alt:''
- # :width:800
+ # :alt: Two one-dimensional scatter plots of y against x. On the left, labelled "separable",
+ #   every orange point with y=1 lies left of x=0 and every blue point with y=0 lies right of
+ #   it, and a black bar at x=0 divides them. On the right, labelled "not separable", the
+ #   orange and blue points overlap along x, so no single dividing point exists.
+ # :width: 800
```

**Why:** Baseline `:alt:''` — an empty alt on the figure that defines linear separability — plus the `:width:800` spacing repair. Filled in from the figure.
**Verdict:** optional — accessibility plus a rendering repair; neither was required by the conversion.
**Minimal alternative:** Keep `:alt:''` and change only the `:width:` spacing.

<a id="c12"></a>
### C12 · cell 8: Linear Separability and Regularization · prose · **REVIEW**

baseline L312 → branch L377

```diff
- # :alt: Mean cross entropy plot. The direction of the gradient is down and to the right.'
+ # :alt: Mean cross entropy plot. The direction of the gradient is down and to the right.
```

**Why:** A stray apostrophe at the end of the alt text, which a screen reader reads aloud.
**Verdict:** optional.
**Minimal alternative:** Leave the apostrophe in place.

<a id="c13"></a>
### C13 · cell 8: Linear Separability and Regularization · prose · **REVIEW**

baseline L318 → branch L383

```diff
- # The diverging weights cause the model to be **overconfident**. Say we add a new point $(x, y) = (-0.5, 1)$. Following the behavior above, our model will incorrectly predict $p=0$, and thus, $\hat y = 0$.
+ # The diverging weights cause the model to be **overconfident**. Say we add a new point $(x, y) = (-1, 1)$, sitting directly above the existing $y=0$ point at $x=-1$. Following the behavior above, our model will incorrectly predict $p=0$, and thus, $\hat y = 0$.
```

**Why:** §A2 #7, pre-existing — the prose introduced the point as (−0.5, 1) and the figure it introduces labels it (−1, 1). CONTRADICTIONS.md confirms by opening the image; not re-opened in this pass (unverified here). The prose moved to the figure because the figure cannot be edited (hard rule 9).
**Verdict:** necessary — a fix to a claim the page itself contradicted (pre-existing). The added clause "sitting directly above the existing y=0 point at x=−1" is the optional half of the edit.

<a id="c14"></a>
### C14 · cell 8: Linear Separability and Regularization · prose · **REVIEW**

baseline L322 → branch L387

```diff
- # :width:450
+ # :width: 450
```

**Why:** The MyST option was written `:width:NNN` with no space after the colon, which MyST does not parse as an option at all. §A2's closing note records nine of these in this chapter; all are pre-existing.
**Verdict:** optional — a rendering repair the conversion did not require.
**Minimal alternative:** Restore `:width:450`.

<a id="c15"></a>
### C15 · cell 8: Linear Separability and Regularization · prose · **REVIEW**

baseline L327 → branch L392

```diff
- # $$-(y\text{ log}(p) + (1-y)\text{ log}(1-p))=1 * \text{log}(0)$$
+ # $$-(y\text{ log}(p) + (1-y)\text{ log}(1-p))=-1 * \text{log}(0)$$
```

**Why:** §A2 #4, pre-existing — the sentence above calls the loss infinite, and the display then evaluated it as `1 · log(0)`, which is −inf. The sign was missing.
**Verdict:** necessary — a fix to a claim that was false (pre-existing).

<a id="c16"></a>
### C16 · cell 8: Regularized Logistic Regression · prose · **REVIEW**

baseline L343 → branch L408

```diff
- # :width:450
+ # :width: 450
```

**Why:** The MyST option was written `:width:NNN` with no space after the colon, which MyST does not parse as an option at all. §A2's closing note records nine of these in this chapter; all are pre-existing.
**Verdict:** optional — a rendering repair the conversion did not require.
**Minimal alternative:** Restore `:width:450`.

<a id="c17"></a>
### C17 · cell 8: Regularized Logistic Regression · prose · **REVIEW**

baseline L348 → branch L413

```diff
- # :width:450
+ # :width: 450
```

**Why:** The MyST option was written `:width:NNN` with no space after the colon, which MyST does not parse as an option at all. §A2's closing note records nine of these in this chapter; all are pre-existing.
**Verdict:** optional — a rendering repair the conversion did not require.
**Minimal alternative:** Restore `:width:450`.

<a id="c18"></a>
### C18 · cell 8: Performance Metrics · prose · **REVIEW**

baseline L380 → branch L445

```diff
- #         return np.mean(model.predict(X) == Y)
+ #         return np.mean(model.predict(X) == Y.to_numpy())
```

**Why:** The only Polars-driven prose change in the chapter, in an indented snippet that never executes — so no gate can see it. Verified on the pin: `pl.Series == np.ndarray` raises in both directions (`TypeError: cannot convert Python type 'numpy.ndarray' to Int64`), and `model.predict` returns an ndarray, so the baseline line is unrunnable for a student who copies it into a Polars notebook.
**Verdict:** necessary — pandas-specific content that could not survive. Staff note: the same snippet still declares `def accuracy(X, Y)` and then calls `model.score(X, y)` with a lowercase `y`; that is inherited from the baseline and untouched.

<a id="c19"></a>
### C19 · cell 8: Adjusting the Classification Threshold · prose · **REVIEW**

baseline L534 → branch L599

```diff
- # :width:700
+ # :width: 700
```

**Why:** The MyST option was written `:width:NNN` with no space after the colon, which MyST does not parse as an option at all. §A2's closing note records nine of these in this chapter; all are pre-existing.
**Verdict:** optional — a rendering repair the conversion did not require.
**Minimal alternative:** Restore `:width:700`.

<a id="c20"></a>
### C20 · cell 8: Precision-Recall Curves · prose · **REVIEW**

baseline L567 → branch L632

```diff
- # :width:600
+ # :width: 600
```

**Why:** The MyST option was written `:width:NNN` with no space after the colon, which MyST does not parse as an option at all. §A2's closing note records nine of these in this chapter; all are pre-existing.
**Verdict:** optional — a rendering repair the conversion did not require.
**Minimal alternative:** Restore `:width:600`.

<a id="c21"></a>
### C21 · cell 8: Precision-Recall Curves · prose · **REVIEW**

baseline L574 → branch L639

```diff
- # :width:600
+ # :width: 600
```

**Why:** The MyST option was written `:width:NNN` with no space after the colon, which MyST does not parse as an option at all. §A2's closing note records nine of these in this chapter; all are pre-existing.
**Verdict:** optional — a rendering repair the conversion did not require.
**Minimal alternative:** Restore `:width:600`.

<a id="c22"></a>
### C22 · cell 8: Precision-Recall Curves · prose · **REVIEW**

baseline L577 → branch L642

```diff
- # We want our PR curve to be as close to the “top right” of this graph as possible. We can use the **area under curve (or AUC)** to determine "closeness", with the perfect classifier exhibiting an AUC = 1 (and the worst with an AUC = 0.5).
+ # We want our PR curve to be as close to the “top right” of this graph as possible. We can use the **area under curve (or AUC)** to determine "closeness", with the perfect classifier exhibiting an AUC = 1. Note that the *worst* case here is not 0.5, as it is for the ROC curve below: a random classifier's PR-AUC equals the proportion of the data that is actually positive. On the 5%-spam example above that baseline is 0.05, not 0.5 — which is precisely why this curve is the one to reach for when the classes are imbalanced.
```

**Why:** §A2 #3, pre-existing, and the worst-placed of the set: 0.5 is the **ROC** baseline. A random classifier's PR-AUC equals the positive-class rate — measured 0.50 / 0.20 / 0.05 at prevalences 0.5 / 0.2 / 0.05, while random ROC-AUC stayed 0.500 throughout. The section exists to handle imbalance, and the chapter's own worked example is 5% spam, where the floor is 0.05.
**Verdict:** necessary — a fix to a claim that was false (pre-existing).

<a id="c23"></a>
### C23 · cell 12: [BONUS] Gradient Descent for Logistic Regression · prose · **REVIEW**

baseline L764 → branch L829

```diff
- # &= y_i \phi(x_i)^T + \log(\sigma(-\phi(x_i)^T \theta))
+ # &= y_i \phi(x_i)^T \theta + \log(\sigma(-\phi(x_i)^T \theta))
```

**Why:** §A2 #5, pre-existing — θ had been dropped from the first term, making it a vector where the expression needs a scalar. Checked numerically in CONTRADICTIONS.md: with θ the identity reproduces the cross-entropy terms exactly; as printed it does not.
**Verdict:** necessary — a fix to a claim that was false (pre-existing).

<a id="c24"></a>
### C24 · cell 12: [BONUS] Gradient Descent for Logistic Regression · prose · **REVIEW**

baseline L769 → branch L834

```diff
- # $$\text{argmin}_{\theta} - \frac{1}{n} \sum_{i=1}^n (y_i \phi(x_i)^T + \log(\sigma(-\phi(x_i)^T \theta)))$$
+ # $$\text{argmin}_{\theta} - \frac{1}{n} \sum_{i=1}^n (y_i \phi(x_i)^T \theta + \log(\sigma(-\phi(x_i)^T \theta)))$$
```

**Why:** The same identity as C23, restated at the argmin. §A2 #5, pre-existing — the fix has to be applied at every site or the line-to-line algebra stops following.
**Verdict:** necessary — a fix to a claim that was false (pre-existing).

<a id="c25"></a>
### C25 · cell 12: [BONUS] Gradient Descent for Logistic Regression · prose · **REVIEW**

baseline L771 → branch L836

```diff
- # We want to minimize $$L(\theta) = - \frac{1}{n} \sum_{i=1}^n (y_i \phi(x_i)^T + \log(\sigma(-\phi(x_i)^T \theta)))$$
+ # We want to minimize $$L(\theta) = - \frac{1}{n} \sum_{i=1}^n (y_i \phi(x_i)^T \theta + \log(\sigma(-\phi(x_i)^T \theta)))$$
```

**Why:** The same identity as C23, restated as the objective to minimise. §A2 #5, pre-existing.
**Verdict:** necessary — a fix to a claim that was false (pre-existing).

<a id="c26"></a>
### C26 · cell 12: [BONUS] Gradient Descent for Logistic Regression · prose · **REVIEW**

baseline L775 → branch L840

```diff
- # \triangledown_{\theta} L(\theta) &= - \frac{1}{n} \sum_{i=1}^n \triangledown_{\theta} y_i \phi(x_i)^T + \triangledown_{\theta} \log(\sigma(-\phi(x_i)^T \theta)) \\
+ # \triangledown_{\theta} L(\theta) &= - \frac{1}{n} \sum_{i=1}^n \triangledown_{\theta} y_i \phi(x_i)^T \theta + \triangledown_{\theta} \log(\sigma(-\phi(x_i)^T \theta)) \\
```

**Why:** The same identity as C23, carried into the first line of the gradient derivation. §A2 #5, pre-existing.
**Verdict:** necessary — a fix to a claim that was false (pre-existing).

<a id="c27"></a>
### C27 · cell 12: [BONUS] Gradient Descent for Logistic Regression · prose · **REVIEW**

baseline L779 → branch L844

```diff
- # &= - \frac{1}{n} \sum_{i=1}^n (y_i - \sigma(\phi(x_i)^T \theta)\phi(x_i))
+ # &= - \frac{1}{n} \sum_{i=1}^n (y_i - \sigma(\phi(x_i)^T \theta))\phi(x_i)
```

**Why:** §A2 #6, pre-existing — the bracket closed in the wrong place. Against a central-difference gradient the correct form `(y_i − σ(·))φ(x_i)` matches and the printed parenthesisation does not.
**Verdict:** necessary — a fix to a claim that was false (pre-existing).

<a id="c28"></a>
### C28 · cell 12: [BONUS] AUC of the Random Predictor · prose · **REVIEW**

baseline L802 → branch L867

```diff
- # :alt: ''
- # :width:700
+ # :alt: The same ROC diagram as above, repeated for the bonus derivation: a diagonal line from
+ #   (0,0) to (1,1) labelled "Random Predictor. AUC = 0.5", an arrow pointing to the triangle
+ #   beneath it, and the orange right-angled path of the perfect predictor with AUC = 1.0.
+ # :width: 700
```

**Why:** Baseline `:alt: ''` on the ROC figure repeated in the bonus section, plus the `:width:700` spacing repair.
**Verdict:** optional — accessibility plus a rendering repair; neither was required by the conversion.
**Minimal alternative:** Keep `:alt: ''` and change only the `:width:` spacing.

<a id="c29"></a>
### C29 · `import warnings` · output

committed output

```diff
- [text]      x  y
- [text] 0 -4.0  0
- [text] 1 -2.0  0
- [text] 2 -0.5  1
- [text] 3  1.0  0
- [text] 4  3.0  1
+ [text] shape: (5, 2)
+ [text] ┌──────┬─────┐
+ [text] │ x    ┆ y   │
+ [text] │ ---  ┆ --- │
+ [text] │ f64  ┆ i64 │
+ [text] ╞══════╪═════╡
+ [text] │ -4.0 ┆ 0   │
+ [text] │ -2.0 ┆ 0   │
+ [text] │ -0.5 ┆ 1   │
+ [text] │ 1.0  ┆ 0   │
+ [text] │ 3.0  ┆ 1   │
+ [text] └──────┴─────┘
```

**Why:** Re-executed; Polars table repr, and `x` is now explicitly `f64` where pandas inferred it.
**Reader sees:** equivalent — the same five rows.

<a id="c30"></a>
### C30 · `def sigmoid(z):` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 25252 bytes md5:ba8188e342
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 24764 bytes md5:909d9f5f04
```

**Why:** Re-rendered figure for the MSE-on-toy-data surface. The only code change in the cell is `np.mean(...)` → `(...).mean()`, and CONVERSIONS.md records the two surfaces as bit-identical.
**Reader sees:** equivalent — the same curve; 25252 → 24764 bytes is re-render noise. Not re-rendered in this pass; CONVERSIONS.md records a reviewer comparing both PNG pairs visually and numerically.

<a id="c31"></a>
### C31 · `def cross_entropy(y, p_hat):` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 24332 bytes md5:8300cf19d8
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 24392 bytes md5:85c0a273e4
```

**Why:** Same, for the mean cross-entropy curve; the cell's only change is the same reduction move.
**Reader sees:** equivalent — the same curve.

<a id="c32"></a>
### C32 · `thetas = np.linspace(0, 1)` · output

committed output

```diff
- [text] <Figure size 640x480 with 1 Axes>
- [image/png] 31792 bytes md5:c08bf26ec0
+ [text] <Figure size 640x480 with 1 Axes>
+ [image/png] 30716 bytes md5:4769f4f804
```

**Why:** The strongest evidence that C30 and C31 are re-render noise: this cell's source is **byte-identical** to the baseline — verified, it contains no library call at all, just `np.linspace` and `plt.plot` — and its PNG still changed (31792 → 30716 bytes).
**Reader sees:** equivalent — the same likelihood curve.

