# _case_study_climate — change report

`887a578b0a4b:content/_case_study_climate/case_study_climate.md` → `content/_case_study_climate/case_study_climate.md`

**Tier A · 2 changes:** prose 2

Categories: **output** = a committed cell output moved, which is what the reader sees. **prose** / **mixed** = wording re-authored beyond a library rename → review. **dropdown** = the mirrored copy of a code cell. **code** = inside a code cell. **mechanical** = rename only. Verdict scale: *necessary* (pandas-specific content that cannot survive as-is), *optional* (style edit the conversion did not require; safe to revert), *questionable* (reviewer should decide).

## Summary

This chapter is tier A, so its predicate is an empty diff — any change at all is by definition the defect, and this diff has two. Neither has anything to do with the conversion: the chapter is an archived, out-of-toc walkthrough of Xarray slides containing no pandas, no Polars, and no code cells. Both changes are typographic — backticks around method names, plus “Xarray's” prepended to one `.groupby()`. Recommendation: revert both. They are harmless as content, and that is exactly the problem — a tier whose only check is “nothing moved” cannot absorb harmless edits.

## Needs review

- [C1](#c1) · Weighing Data Using Xarray
- [C2](#c2) · Weighing Data Using Xarray

## Changes

<a id="c1"></a>
### C1 · Weighing Data Using Xarray · prose · **REVIEW**

baseline L152 → branch L152

```diff
- Xarray methods like .weighted() can be combined with .mean() to create means across coordinates.
+ Xarray methods like `.weighted()` can be combined with `.mean()` to create means across coordinates.
```

**Why:** Backticks added around `.weighted()` and `.mean()` so they render as code. No factual or functional change, and nothing in the sentence is pandas-specific: the only library in this chapter is Xarray, which the conversion does not touch.
**Verdict:** optional — a style edit the conversion did not require, in a chapter whose predicate is an empty diff. It should be reverted.
**Minimal alternative:** restore the baseline line verbatim; if staff want the code formatting, land it as its own change against `main` where it is not masquerading as conversion fallout.

<a id="c2"></a>
### C2 · Weighing Data Using Xarray · prose · **REVIEW**

baseline L159 → branch L159

```diff
- We can use .groupby() in combination with the above methods to calculate the annual temperature cycle.
+ We can use Xarray's `.groupby()` in combination with the above methods to calculate the annual temperature cycle.
```

**Why:** Backticks plus “Xarray's” before `.groupby()` — apparently a converter reflex to disambiguate it from pandas' `groupby`. There was nothing to disambiguate: the chapter never mentions pandas.
**Verdict:** optional — same as C1: not required by the conversion, and a tier A chapter should have come back with an empty diff. It should be reverted.
**Minimal alternative:** restore the baseline line verbatim.

