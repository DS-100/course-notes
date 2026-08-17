# Standing rules — Data 100 course notes, pandas → Polars

Always in effect. Detail lives in `.claude/skills/`; this file is versions, hard constraints, and
commands only.

## Pinned versions

`polars==1.43.1` · Python 3.11 · conda env + Jupyter kernel `d100` · `jupyter-book` v2 (node) ·
baseline commit pinned in `conversion/baseline.lock`

```bash
export PATH="/Users/jedwin321/miniforge3/envs/d100/bin:$PATH"
```

**Export this before running anything, including a one-off `python3 -c` used to check a mapping.**
Several conda envs on this machine carry different Polars versions (`d100` 1.43.1, `cp101` 1.42.1,
`data6` 1.38.1, base 1.38.0), and the system `python3` is 3.9 with no polars at all. Verifying
against the wrong version is silent: the code runs, the answer looks right, and it does not describe
the environment the notebook will be executed in. Start any verification by printing
`polars.__version__` and confirming it reads 1.43.1.

The site build needs node on the PATH too:
`export PATH="/Users/jedwin321/.nvm/versions/node/v18.20.8/bin:$PATH"`.

## Hard rules

1. **Committed outputs are the deliverable.** CI runs `jupyter-book build --html` with no
   `--execute` and no pip install, so MyST publishes whatever outputs are committed. A converted cell
   whose output was not regenerated ships Polars code above a pandas table, and nothing in CI will
   ever catch it.
2. **Keep Polars-native output — move the prose to it, never the reverse.** No `.alias()`,
   `.rename()`, or `.sort()` whose only purpose is reproducing a pandas artifact. The bar is
   pedagogical equivalence, not identical output.
3. **The dropdown and the code cell are one edit.** 82 markdown blocks repeat the next code cell
   verbatim inside `` ```{dropdown} Click to see the code ``. Convert both or neither.
4. **`.to_pandas()` is a last resort and needs a written reason.** Polars goes to plotly and sklearn
   directly, and to matplotlib through `.to_numpy()`. Every surviving call is allowlisted in
   `conversion/conversion_allowlist.yml`.
5. **Never silence a cell.** `remove-input` and `remove-cell` are layout. Using either to hide a cell
   that misbehaves is a hard failure, and so is deleting an output to make a gate pass.
6. **A cell that raises on purpose must keep raising.** Two exist: `eda` cell `a3fde967` and
   `pandas_2` cell `ccf796ec`, both `ValueError`. A demo that goes quiet leaves the paragraph above
   it describing something the reader will never see.
7. **Reshapes go to an agent, renames may go to regex.** `.loc`/`.iloc`, `groupby().filter()`,
   `pivot_table`, `set_index`, and dict-agg-with-lists are all reshapes.
8. **`sort` sense is inverted** — pandas `ascending=True` ↔ Polars `descending=False` — **and Polars
   sorts nulls first.** Any `.head()` after a sort on a nullable column silently gains a null row.
9. **Never edit `content/*/data/**`, `content/*/images/**`, `.github/**`, `assets/**`, or
   `content/eda/ds100_utils.py`.** `myst.yml` and `requirements.txt` change only with an allowlist
   entry. The repo-invariants gate enforces all of this.
10. **Never edit `conversion/.baseline/**`** — it is the diff baseline, regenerated from git.
    Edit `conversion/pytext/polars/**`.

## Convert a chapter

```bash
export PATH="/Users/jedwin321/miniforge3/envs/d100/bin:$PATH"

python conversion/nb_baseline.py --chapter <ch>          # materialize the pinned baseline
# dispatch notes-converter (tier B/C) or chapter-author (tier D) on conversion/pytext/polars/<ch>/

python conversion/nb_pytext.py to-ipynb \
    --input  conversion/pytext/polars/<ch>/<file>.py \
    --output content/<ch>/<file>.ipynb \
    --outputs-from conversion/.baseline/<sha>/content/<ch>/<file>.ipynb

python conversion/nb_execute.py --chapter <ch>           # full re-execution; serial only
python conversion/nb_validate.py --chapter <ch>          # gate battery G1-G13
# dispatch reviewers per tier, then once per batch:
python conversion/site_gate.py                           # G14 + G15
```

**Execution is serial.** One kernel per notebook, Polars uses all cores, and several chapters read
20–150 MB. Run them ordered by data size ascending so failures surface in the first minute.
Converters and reviewers may run in parallel; execution may not.

## Before every batch

```bash
python conversion/nb_validate.py --all --self-test
```

The negative control. It runs the battery against the pandas baseline and asserts the removal gates
fail while the structural gates stay quiet. Ten seconds, and it catches the entire class of bug where
a scanner silently matches nothing — which has already happened twice in this harness: the self-test
probe missed `class=\"dataframe\"` escaped inside notebook JSON, and the site gate missed the same
string escaped inside MyST's page JSON.

## Where things live

| Path | What |
|---|---|
| `AGENTS.md` | this file — versions, rules, commands |
| `CONVERSIONS.md` | per-chapter record and open questions for course staff |
| `.claude/skills/` | the conversion conventions |
| `.claude/agents/` | the writer and reviewer contracts |
| `conversion/` | the toolchain, the gates, the allowlist, and `state.json` |
| `README.md` | the site build, for course staff who are not converting anything |
