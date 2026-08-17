---
name: data100-textbook-voice
description: The house style of the Data 100 course notes — chapter skeleton, the Learning Outcomes block, the dropdown/remove-input code pattern, admonition vocabulary, and the rules for re-authoring or newly authoring prose so it is indistinguishable from the chapters around it. Load when writing or reviewing any student-facing text in this repo.
---

# Data 100 course notes — house style

These notes are a published textbook, not an assignment. A student reads them start to finish and
never runs a cell: `.github/workflows/deploy.yml` builds with `jupyter-book build --html` and no
`--execute`, so what ships is the prose plus whatever outputs are committed. Everything below is
measured from the live chapters, not invented.

## Chapter skeleton

**28 of 30 chapters open exactly this way**, and a converted or newly authored chapter keeps it:

```
---
title: Pandas III
---

::: {note} Learning Outcomes
* Perform advanced aggregation using `.groupby()`
* Use the `pd.pivot_table` method to construct a pivot table
* Perform simple merges between DataFrames using `pd.merge()`
:::

We will introduce the concept of aggregating data — we will familiarize ourselves with
`GroupBy` objects and use them as tools to consolidate and summarize a `DataFrame`.
```

Three things about that block:

- **The frontmatter must be the first construct in cell 0**, with no blank line above it. One line
  out of place and MyST silently falls back to the filename for the page title and still exits 0.
- **Learning outcomes are `*` bullets, imperative, one skill each**, naming the specific API. When a
  chapter is re-aimed at Polars, each bullet has to name something the chapter now actually teaches —
  a bullet promising `pd.pivot_table` above a section teaching `.pivot` is the defect a reader hits
  first and trusts least.
- **The opener says what the chapter will do, in the first person plural.** "We will introduce…",
  "In this lecture, we will explore…". Not "This chapter covers…".

## The dropdown / remove-input pattern

The repo's most distinctive convention, and the one most easily broken. **110 dropdowns, 82 of which
repeat the next code cell verbatim.** The title is `Click to see the code` (108 of 110; two older
chapters say `Click to show the code` — match the neighbours, don't standardise them).

````
```{dropdown} Click to see the code
```python
census_2010s = pl.read_csv("data/nst-est2019-01.csv")
census_2010s
```
```
````

…immediately followed by a code cell carrying `remove-input`, holding *the same source*, so the page
shows the output with the code tucked away.

**The two are one edit.** Change the code cell and the dropdown block has to change identically, in
the same pass. Convert only the cell and the page shows pandas source above Polars output — no gate
downstream of the text can see it, which is why `dropdown-mirror` checks it directly.

Two related tags: `remove-input` hides the source and keeps the output; `remove-cell` removes both,
and is what setup cells use. Never add either to hide a cell that misbehaves — that is this repo's
equivalent of silencing a failing test, and the `tags` gate blocks it.

## Admonitions

Use what the book already uses, in roughly the proportion it already uses it:

| Directive | Count | Used for |
|---|---|---|
| `::: {note}` | 52 | Learning Outcomes, and asides worth pausing on |
| `::: {tip}` | 42 | practical advice, shortcuts, "in practice you would…" |
| `::: {warning}` | 4 | genuine hazards — rare on purpose |
| `::: {caution}` / `{hint}` | 3 / 3 | rarer still |

Both `::: {note}` and `:::{note}` appear; match the surrounding file. Do not introduce directives the
book does not use, and do not promote an aside to a `{warning}` because the conversion made you
nervous about it.

## Voice

- **Second person and first person plural.** "We will…", "you can…", "notice that…".
- **Method and object names in backticks**: `` `.groupby()` ``, `` `DataFrame` ``, `` `pl.col` ``.
- **Concept before syntax.** A section states what the operation does to the data, then shows the
  call. Reversing that is the fastest way to make a converted chapter read like reference docs.
- **Code is introduced by a sentence that says what it demonstrates**, and followed by prose that
  reads the result. That second half is where conversions break: the sentence after a cell routinely
  quotes a row count, a column name, or a number from the output.
- Sentence lengths vary. Paragraphs are 2–5 sentences. Em dashes appear, but sparsely.

## Re-authoring prose

The chapter must read as though it was always about Polars.

- **No conversion meta-commentary.** "Unlike pandas…", "because Polars is immutable…", "we now
  use…". A student reading these notes has never seen the pandas version and is not owed a migration
  diary. The exception is a passage whose subject genuinely is the ecosystem — `intro_lec` names
  pandas as a tool that exists, and that stays.
- **State what Polars does, not what it stops doing.** "Polars addresses rows by position" is a
  sentence about Polars. "Polars has no index" is a sentence about pandas.
- **When a distinction collapses, restructure the section — don't refill the scaffold.** A chapter
  that spent four paragraphs distinguishing `.loc` from `.iloc` cannot have those paragraphs
  find-and-replaced. Ask what the section was *for*, then write the section that does that job for
  Polars. Usually it is shorter, and shorter is the correct answer.
- **Rebalance example counts to match idiomatic weight.** If pandas needed three examples to cover
  something Polars expresses one way, ship one example. Padding back to three to preserve the
  chapter's shape is how a converted chapter starts to feel padded.
- **A newly authored mnemonic must hold for the API generally**, not just for the example under it.
  This is the easiest way to introduce a confident falsehood into a textbook.
- **Repoint documentation links, never delete them.** `pandas.pydata.org` → `docs.pola.rs`. Reading
  documentation is a course outcome; a vanished link fails the `doc-links` gate in the same way an
  unconverted one does.
- **Check every number in the prose against the output above it.** After the notebook executes, the
  numbers in the cell are authoritative and the ones in the paragraph are a claim.

## Writing that reads as machine-written

Load the `humanizer` skill for the full list. The tells that show up most in converted course prose:

- A rule-of-three list where the original had two items.
- "delve", "leverage", "robust", "comprehensive", "seamless", "crucial".
- Em-dash pileups, and "It's not just X — it's Y".
- Uniform sentence length across a paragraph.
- Hedging the original did not have ("generally", "typically", "in most cases") bolted onto a claim
  that used to be flat.
- A summary sentence at the end of a section that restates the section.

Before finishing, grep the diff for `—` and re-read every paragraph you rewrote against the two
paragraphs on either side of it. If it stands out, it is wrong, even if it is good.
