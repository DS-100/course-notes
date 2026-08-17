# Tier D outlines — `polars_1` / `polars_2` / `polars_3`

**Status: awaiting course-staff approval.** `chapter-author` may not start until these are signed off.
These three chapters are *about* the library, so they get rewritten rather than translated. Everything
below is a proposal.

## Why these are different

The other 26 chapters use pandas to do something else, so conversion is translation. These teach
pandas itself. Roughly **60% of `pandas_1` is about the Index**, which Polars does not have — so the
question is not "what is the Polars spelling" but "what should a student learn instead, in the same
slot, at the same point in the course".

Two commitments already made elsewhere in the book constrain this:

1. **`intro_lec` now says there are *two* fundamental data structures**, `DataFrame` and `Series`, and
   that rows are addressed **by position, counting from 0**. `polars_1` must not reintroduce `Index`.
2. **`intro_lec` deliberately does not mention expressions**, on the grounds that it never shows one.
   That makes `polars_1` the first place expressions can be introduced — and they are the centre of
   the library, so the outline gives them real space rather than treating them as syntax.

---

## `polars_1` — DataFrames, Series, and Selection

Replaces `pandas_1` (67 cells, 34 code). The heaviest rewrite of the three.

| Baseline section | Disposition |
|---|---|
| `DataFrame`s and Indices | **Rewritten.** Two structures, not three. |
| `DataFrame` Attributes: Index, Columns, Shape | **Rewritten** — `.columns`, `.shape`, `.dtypes`, `.schema`. No `.index`. |
| Slicing: `.head`/`.tail` | **Kept**, nearly unchanged. |
| Label-based Extraction: `.loc` | **Deleted as a concept.** Replaced by `.select()` for columns. |
| Integer-based Extraction: `.iloc` | **Replaced** by `[]` with integers/slices, `.row()`, `.item()`. |
| Context-dependent Extraction: `[]` | **Shrunk.** Polars' `[]` is for quick exploration; the idiom is expressions. |
| Parting Note | **Kept**, repointed at `docs.pola.rs`. |

**Proposed shape**

1. **DataFrames and Series** — the two structures. A Series has a *name* and a *dtype*; a DataFrame
   is an ordered, named collection of Series. Rows have positions, not labels.
2. **Attributes** — `.shape`, `.columns`, `.dtypes`, `.schema`. The `.schema` is worth its own beat:
   pandas students learn dtypes late, and Polars puts them on every table it prints.
3. **Looking at data** — `.head()`, `.tail()`, `.sample()`, `.glimpse()`.
4. **Selecting columns: `.select()`** — the replacement for the column half of `.loc`.
5. **Filtering rows: `.filter()`** — the replacement for boolean `.loc`. Introduce `pl.col`.
6. **Expressions** *(new section, no baseline counterpart)* — `pl.col("x") > 5` is a *description* of
   a computation, not a computation. This is the concept that makes the rest of the course legible,
   and the chapter currently spends that space on `.loc` vs `.iloc` vs `[]`.
7. **Positional access when you really need it** — `df[0, "col"]`, `.row()`, `.item()`, and a note
   that reaching for positions is usually a sign an expression would be clearer.
8. **Parting Note.**

**Net effect:** three overlapping indexing methods collapse into two clearly-separated ideas
(`select` for columns, `filter` for rows), and the space that buys goes to expressions.

---

## `polars_2` — Working with Columns and Rows

Replaces `pandas_2` (77 cells, 41 code). The most nearly translatable of the three.

| Baseline section | Disposition |
|---|---|
| Conditional Selection | **Kept**, rebuilt on `.filter()` + expressions. |
| Adding, Removing, Modifying Columns | **Kept**, rebuilt on `with_columns` / `drop` / `rename`. |
| Useful Utility Functions (`NumPy`, `.shape`/`.size`, `.describe`, `.sample`, `.value_counts`, `.unique`, `.sort_values`) | **Kept**, one-for-one, with three behaviour notes below. |
| Custom Sorts: 3 approaches | **Collapsed to one.** See below. |
| Parting Note | **Kept.** |

**Three behaviour notes this chapter must carry, because later chapters depend on them:**

- **Immutability.** `with_columns` returns a *new* frame. `intro_lec` now introduces this idea with
  `.cast()`; this is where it gets stated properly.
- **`value_counts` returns a two-column DataFrame with no guaranteed order** — not a Series indexed
  by value. Every chapter that plots a value count has had to sort it explicitly.
- **Sorting: `descending=` not `ascending=`, and nulls sort first.** This has been the single most
  repeated hazard across the whole conversion.

**The Custom Sorts section is the chapter's best teaching opportunity.** pandas needed three separate
approaches — a temporary column, the `key=` argument, and `.map()` — and the section exists largely
to work around the API. In Polars all three are one idea: `sort_by` takes an *expression*, so you sort
by a computed value without materialising it. Proposal: teach the one form, then show explicitly that
it subsumes all three, and reclaim the space for the sorting hazards above. This is a case where the
Polars version is genuinely shorter and better, and the chapter should say so by being shorter.

---

## `polars_3` — Aggregating and Combining Data

Replaces `pandas_3` (76 cells, 42 code). Highest output surface of the three.

| Baseline section | Disposition |
|---|---|
| Aggregating with `.groupby` | **Kept** → `group_by().agg()`. |
| Aggregation Functions | **Kept**, rebuilt on expressions. |
| Plotting Birth Counts | **Kept.** |
| Revisiting `.agg()` | **Merged** into the main agg section — Polars needs one story, not two. |
| **Nuisance Columns** | **Deleted.** The concept does not exist: pandas silently dropped columns it could not aggregate, and Polars requires you to say what you want. Worth one sentence explaining why the problem is gone. |
| Renaming Columns After Grouping | **Shrunk** — `.alias()` inside `.agg()` names the output where it is computed. |
| Raw `GroupBy` Objects | **Kept but reframed.** Polars has a GroupBy; it is lazier and less inspectable. |
| Other `GroupBy` Methods | **Kept** — `.first()`, `.len()`, `.n_unique()`. |
| Filtering by Group | **Rewritten** around **window expressions** — `.over()`. This is a genuinely different and more powerful idea than `groupby().filter()`. |
| Aggregation with `lambda` | **Rewritten.** Expressions replace most lambdas; keep one honest example of when you still need `map_elements`, with its performance caveat. |
| Pivot Tables | **Kept** → `.pivot()`. |
| Joining Tables | **Kept** → `.join()`, plus `how=` and key-coalescing. |
| Parting Note | **Kept.** |

**Two notes this chapter must carry:**

- **`group_by` does not preserve order** unless you ask (`maintain_order=True`) or sort afterwards.
  Several converted chapters needed an explicit sort for exactly this reason.
- **Key coalescing on joins.** `eda` lost two columns to it and had to explain it inline; this is the
  chapter that should own the explanation.

---

## The concept diagrams — narrower than open question 2 assumed

Nine of the twelve images under the three chapters are unreferenced. Of the twelve that are
referenced, the verdict splits cleanly:

**`pandas_1` — all 3 die with the concept, no redraw needed.**

| Image | Verdict |
|---|---|
| `locgraphic.png` | A pandas render annotated "**Row labels**" / "Column labels". Polars has no row labels. **Delete.** |
| `uniqueindex.png`, `non-uniqueindex.png` | Both illustrate index uniqueness. **Delete.** |

**`pandas_2` — references no images at all.** Nothing to decide.

**`pandas_3` — 9 referenced, and most are semantically fine.** These draw *operations*, not pandas
internals, and the operations survive:

| Image | Verdict |
|---|---|
| `gb.png` | Shows rows regrouped by key into a "GroupBy Object" — **conceptually correct for Polars.** Only the rendered method name `.groupby("Year")` is wrong (`group_by`). Text-only redraw. |
| `agg.png` | Same three-stage story plus `.agg(sum)` → output. **Semantics correct**; two method names wrong. Text-only redraw. |
| `pivot.png` | group → aggregate → reshape to an R×C grid. **No pandas method names in the image at all** — the labels are generic (`group`, `f = sum`). Only the `NaN` cell should read `null`. |
| `aggregation.png`, `error.png`, `filter_demo.png`, `first.png`, `groupby_demo.png`, `puzzle_demo.png` | Need the same check; expected to be the same pattern — correct semantics, pandas spelling. |

**So the ask on staff is small:** delete 3, and correct method-name text in roughly 6. No diagram needs
its *semantics* redrawn, which is what open question 2 feared.

---

## The rename

`git mv` per the recorded global decision, so history follows the file and `pandas_2`'s 146 MB of data
is not duplicated:

```bash
git mv content/pandas_1 content/polars_1
git mv content/polars_1/pandas_1.ipynb content/polars_1/polars_1.ipynb   # and _2, _3
```

`conversion/chapter_map.yml` already declares `polars_1: pandas_1` and siblings, so the gates resolve
the baseline correctly the moment the move happens.

**In-repo blast radius is three lines.** A search for `pandas-1`/`pandas_1` and siblings across
`content/`, `myst.yml` and `README.md` finds **only the three TOC entries** — no chapter
cross-references them. `myst.yml` needs an `_repo: changed_paths` allowlist entry, which the allowlist
template already anticipates.

**The external question is still open (question 3):** the published URLs change from `/pandas-1` to
`/polars-1`, and nothing in this repo can tell us whether a syllabus, assignment or Piazza post links
to them.
