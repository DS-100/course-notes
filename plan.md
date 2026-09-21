Agentic orchestration for phase 2, with validation that can actually fail
Context
Twenty-nine chapters are converted and the site serves zero pandas. What remains is phase 2: 87 baseline-paired comparison twins across 11 translated chapters, an audit of 36 .to_numpy() sites against the corrected dispatch rule, and a re-read of the chapters converted before that correction landed.

This plan defines how agents run that work, and adds the validation the current pipeline structurally cannot do. The design is not speculative — it is built from what this project's own defects reveal.

The evidence the design rests on
Layer	Caught	Cannot catch, by construction
13 gates	stale reprs, unconverted dropdowns, dropped alt text, tag changes	anything semantic; anything about the rendered page
executor	a lost error demo (refused to write the notebook)	anything that executes cleanly
reviewers (7 blocks)	mirrored plot, lost axis label, pandas traceback shipped as an image, ungrouped figure, a taught default the page contradicted	claims never checked against a live interpreter; the built artifact
Three defects reached course staff because no layer owns them. They are the specification for what to add:

Polars II's title stopped rendering. apply_to_pytext rewrote # %% [markdown] into # %% tags=[...] [markdown], so the frontmatter cell became a code cell and published its own YAML as comments. G11 frontmatter passed throughout — the title block was present, correct and first; it had merely stopped being markdown. No gate reads a rendered title, and no reviewer opens the built page.
A comment claimed columns= returns columns "in the order we name them." The cell's own committed output disproved it. Verified: pl.read_csv(columns=…) and pd.read_csv(usecols=…) both return file order; .select() is what honours the order named. This is exactly the "is it actually true for Polars" class, and nothing checks it.
Tab density. 69 of 80 code cells became tab widgets. No agent holds a view of the chapter as a whole.
A fourth signal: several reviewer findings were confidently wrong — a BLAS attribution corrected to environmental drift, a "pixel-identical" claim that was ~1.4% of pixels, "two win rates moved" that was three, and two of my own (a u8/str mix-up, a nested-backtick bug I introduced while fixing another). Every one was caught only because something re-derived it.

Two new agents
notes-claim-verifier — is this actually true for Polars? Extracts every factual assertion about library behaviour from prose, comments and admonitions — "returns a Series", "sorts nulls first", "in the order we name them", "has no equivalent" — and executes each one against the pinned Polars 1.43.1 / pandas 2.3.0. Reports each claim as supported, contradicted, or unverifiable, quoting the code it ran. Tools: Read, Grep, Glob, Bash, Skill; loads pandas-to-polars. Blocking on a contradicted claim.

This is the agent that would have caught defect 2, and it generalises: the chapters are full of sentences asserting API behaviour, and until now the only check was whether a human happened to notice.

notes-render-reviewer — what does the reader actually see? Reads _build/html/<slug>.json, never the source. Confirms the frontmatter title resolves, no raw title: text leaks into the body, every tab-set carries its sync keys, every figure has non-empty alt text, and the page carries no unrendered directive text. Tools: Read, Grep, Glob, Bash. Blocking.

This is the agent that would have caught defect 1, and it closes the gap between "the source is correct" and "the page is correct" — the gap every one of harness notes 1, 2, 3, 6, 7 and 9 lived in.

The waves
0 · Prepare (serial, cheap). nb_baseline --all, nb_triage, and the negative control nb_validate --all --self-test. The negative control runs first, every time. A battery that passes on pandas is broken, and everything after it would be meaningless.

1 · Convert (parallel, cap 6). notes-converter per chapter for prose/code work; tab_twins --from-baseline for twins, which needs no agent at all.

2 · Execute (STRICTLY SERIAL). One kernel at a time — Polars takes all cores and several chapters read 20–150 MB. Order by data size ascending so failures surface in the first minute. This is the one wave that must not be parallelised.

3 · Gates (parallel). nb_validate per chapter. A chapter failing here never reaches a reviewer — reviewer time is the expensive resource and mechanical defects should never consume it.

4 · Review fan-out (parallel across chapters and across reviewers). Per tier:

Tier	Reviewers
A	none — the predicate is an empty diff
B	output + claim-verifier + render
C	+ prose
D	+ prose + a11y + human sign-off
a11y is added wherever figure outputs moved.

5 · Adversarial verification (parallel, one per BLOCK). Every blocking finding goes to an independent agent instructed to refute it, with the finding surviving only if refutation fails. At this project's rate that is ~7 extra agents, and it is aimed squarely at the confidently-wrong-finding problem above. A refuted finding is reported to the orchestrator, not silently dropped.

6 · Fix loop. Surviving findings become a fix list back to notes-converter, then re-enter at wave 2. Floor unchanged: three attempts, debt must fall strictly between them, an identical failure fingerprint twice bails, three consecutive NEEDS_HUMAN_REVIEW halts the batch.

A blocker phase 2 hits immediately
26 of the 87 baseline twins have a locator that lands in a markdown cell first — measured. The {dropdown} blocks repeat their cell's source verbatim, so text.find(locator) finds the prose copy before the live cell. That is the same mechanism that broke the Polars II title.

The hardening added after that incident means these now report instead of corrupting the file, so 30% of phase-2 twins would simply fail to place. Fix before running wave 1: apply_to_pytext should choose the first occurrence whose enclosing cell header is not [markdown], rather than the first occurrence outright. Small change in conversion/tab_twins.py, and it converts a silent 30% loss into a non-event.

Files
.claude/agents/notes-claim-verifier.md, .claude/agents/notes-render-reviewer.md — new contracts, written to match the existing five in shape and tone.
conversion/tab_twins.py — the locator fix above.
AGENTS.md — the wave table and the serial-execution constraint, so the next orchestrator inherits it rather than rediscovering it.
CONVERSIONS.md — per-chapter records, as now.
Verification
Prove each new agent fails before trusting it to pass. Point claim-verifier at the pre-fix columns= comment and confirm it reports a contradiction; point render-reviewer at the pre-fix Polars II notebook and confirm it reports the missing title. An agent that has never failed on a known defect is not evidence of anything — this is the same reasoning as the --self-test negative control.
tab_twins --verify — all 105 existing twins fresh, plus the new ones.
nb_validate --all --self-test, then nb_validate --all.
site_gate.py — 0 pandas reprs reaching the reader, unchanged.
Spot-check that the 26 previously-unplaceable twins now land in code cells, not markdown.
Deliberately out of scope
Tab density and the UI question — course staff have chosen to keep the current tabs. The elections.csv split between Polars I (182 rows, ends 2020) and Polars II (187, ends 2024) stays recorded and unfixed; changing it is a re-review, not an edit.