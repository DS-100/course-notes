---
name: myst-jupyterbook
description: MyST / Jupyter Book v2 mechanics for the Data 100 course-notes site — how the site is built and deployed, the TOC in myst.yml, cell tags, image alt text and the a11y gate, the fence-nesting hazard, and why committed outputs are the deliverable. Load before editing any content file or the TOC in this repo.
---

# MyST / Jupyter Book v2 — this site's mechanics

## The one fact that shapes everything

**CI never executes a notebook.** `.github/workflows/deploy.yml` runs:

```yaml
- run: npm install -g jupyter-book
- run: jupyter-book build --html      # no --execute, no pip install
```

There is no Python setup step in the deploy workflow at all. MyST renders the **committed outputs**
of each `.ipynb` and never runs a line of code. So:

- An output committed in the notebook is published exactly as it stands.
- A converted cell whose output was not regenerated publishes Polars source above a pandas table.
- Nothing in CI will ever catch that, because nothing in CI runs the code.

Regenerating outputs is `conversion/nb_execute.py`, and it must run from the chapter's own directory
because every data path is notebook-relative (`pl.read_csv("data/elections.csv")`).

## Build and preview

```bash
jupyter book start                 # local preview server, rebuilds on change
jupyter-book build --html          # what CI runs; output lands in _build/html
jupyter book clean                 # when a change stubbornly does not appear
```

`_build/` is gitignored. Note the layout, because it is not what "build --html" suggests: **page
content is emitted as `_build/html/<slug>.json`**, and the `.html` files are a React shell that
hydrates from it. Grepping the built site for rendered output means reading the JSON, where HTML is
escaped — `class=\"dataframe\"`, not `class="dataframe"`. A scan for the unescaped form finds zero
hits on a site carrying 294 of them.

## myst.yml

Two files are edited in normal work: `myst.yml` and `content/`. The TOC is flat — 26 `file:` entries
in lecture order, no `children:` or parts:

```yaml
project:
  toc:
    - file: content/index.md
    - file: content/pandas_1/pandas_1.ipynb
    ...
```

- A new chapter is invisible until its path is added here.
- A chapter directory prefixed with `_` is archived: it exists in `content/` and is absent from the
  TOC, so it never renders. Four such directories exist.
- Renaming a chapter directory means editing the matching `file:` entry in the same commit. Use
  `git mv` so history follows the file — several chapters carry 20–146 MB of data beside them and
  copying would duplicate it.
- There is no `execute:`, `jupyter:`, or `kernel:` key, and adding one changes deploy behaviour.
  Don't, without saying so.

## Cell tags

Only two are in use anywhere in the repo:

| Tag | Effect |
|---|---|
| `remove-input` | hides the source, keeps the output — the other half of the `{dropdown}` pattern |
| `remove-cell` | removes the cell entirely; used for setup cells that configure display |

Neither may be added to hide a cell that misbehaves. That is the local equivalent of silencing a
failing test, and the `tags` gate blocks it against the baseline.

## Directives in use

`{image}` 274 · `{dropdown}` 110 · `{note}` 52 · `{tip}` 42 · `{warning}` 4 · `{caution}` 3 ·
`{hint}` 3 · `{figure}` 1. Admonitions are written with colon fences (`::: {note}` … `:::`); images
and dropdowns with backtick fences.

### The fence-nesting hazard

The dropdown pattern nests a 3-backtick `python` block inside a 4-backtick `{dropdown}` block:

````
```{dropdown} Click to see the code
```python
...
```
```
````

Get the backtick counts wrong while editing and **MyST renders the rest of the cell as a code block
and exits 0**. The page is visibly broken, the build is green, and no test fails. Six markdown cells
in the repo already have unbalanced-looking fence counts for legitimate reasons, which is why the
`myst-fences` gate compares each cell's fence profile against its own baseline rather than asserting
that fences balance.

## Alt text and accessibility

`.github/workflows/a11y.yml` runs `berkeley-cdss/myst-a11y@v1` on **every pull request** — it is the
only automated gate the repo has today, and it enforces alt text.

- `{image}` directives take an `:alt:` option. Every one needs non-empty text.
- Code cells that produce figures carry a quarto-era `#| fig-alt:` comment — 103 of them. They are
  still meaningful to the a11y tooling and must survive conversion. `#| code-fold` appears 5 times.
- Counts are preserved, text may change. A regenerated figure legitimately needs new alt text; a
  *missing* `#| fig-alt` is a regression.
- `axe-scan.js` at the repo root is the legacy local scanner. There is no `package.json`, so its
  dependencies are not declared — treat it as vestigial and use the CI action.

## Cross-references

Effectively unused: one `(sec-bias-variance-tradeoff)=` label in the whole repo and zero internal
references to it. The README documents the `(label)=` / `[text](label)` syntax, but there is no
existing web of links to break. Don't introduce one during a conversion.

## What must not be touched

`content/*/data/**` (469 MB), `content/*/images/**` (494 files), `.github/**`, `assets/**`, and
`content/eda/ds100_utils.py` (dead — zero imports). The repo-invariants gate freezes all of them.
The cheapest way to make a failing build pass is to stop building the thing that fails, and that is
what this prevents.
