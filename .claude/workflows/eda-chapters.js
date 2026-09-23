export const meta = {
  name: 'eda-chapters',
  description: 'Author and validate the Fa26 EDA I-V course-notes chapters from lecture decks (outline pass, then build pass)',
  whenToUse: 'args.phase = "outline" first; after a human marks conversion/eda_outlines.md approved and the orchestrator has copied data/images, args.phase = "build". args.lectures = deck-extract root from conversion/lecture_extract.py.',
  phases: [
    { title: 'Images', detail: 'one agent per deck identifies every non-chrome image' },
    { title: 'Outline', detail: 'one outline per chapter, then an overlap critic writes eda_outlines.md' },
    { title: 'Author', detail: 'lecture-chapter-author per chapter (parallel)' },
    { title: 'Gate', detail: 'nb_execute + authored_validate, strictly serial across chapters' },
    { title: 'Review', detail: 'claim-verifier, a11y, prose, lecture-fidelity per chapter' },
    { title: 'Refute', detail: 'one refuter per blocking finding' },
    { title: 'Site', detail: 'site build + render review, once per batch' },
  ],
}

// ---------------------------------------------------------------- configuration

const LECT = args && args.lectures
if (!LECT) throw new Error('args.lectures is required: the root written by conversion/lecture_extract.py --out')
const PHASE = (args && args.phase) || 'outline'
const ONLY = (args && args.chapters) || null           // e.g. ["new_eda_2"] to re-run one chapter
const MAX_ATTEMPTS = 3

const CHAPTERS = [
  { ch: 'new_eda_1', title: 'EDA I', decks: ['L02'], slides: 'L02 S5-S61',
    notebook: 'none -- fix pass on main\'s draft content/new_eda_1/new_eda_1.ipynb (grammar, residue, the defects listed in fa26-course-conventions.md and CONVERSIONS.md)' },
  { ch: 'new_eda_2', title: 'EDA II', decks: ['L03'], slides: 'L03 S9-S49 (S12-S26 repeat L02 S45-S60: keep only what EDA I did not already cover)',
    notebook: 'none -- lec/lec03 in fa26-dev is a stale babynames notebook; rebuild from deck code' },
  { ch: 'new_eda_3', title: 'EDA III', decks: ['L04'], slides: 'L04 S11-S46 (S4-S10 recap EDA II)',
    notebook: '/Users/jedwin321/Documents/fa26-dev/lec/lec04/lec04.ipynb' },
  { ch: 'new_eda_4', title: 'EDA IV', decks: ['L05'], slides: 'L05 S4-S19 only: finish the UCB case study',
    notebook: '/Users/jedwin321/Documents/fa26-dev/lec/lec05/lec05.ipynb' },
  { ch: 'new_eda_5', title: 'EDA V', decks: ['L05', 'L06'], slides: 'L05 S20-S60 (key data properties, joins, file formats, faithfulness) + L06 S39-S51 (DBMS, Why SQL, schema, keys, star schema). L06 S4-S38 repeats L05 and adds only the Polars join line on S20.',
    notebook: '/Users/jedwin321/Documents/fa26-dev/lec/lec06/lec06.ipynb (SQL demo data only; its SELECT/WHERE material belongs to the later SQL chapter, not here)' },
].filter(c => !ONLY || ONLY.includes(c.ch))

const DECKS = ['L02', 'L03', 'L04', 'L05', 'L06']
const SCOPE_TABLE = CHAPTERS.map(c => `- ${c.ch} (${c.title}): ${c.slides}`).join('\n')

// ---------------------------------------------------------------- schemas

const IMAGES_SCHEMA = {
  type: 'object',
  properties: {
    deck: { type: 'string' },
    images: { type: 'array', items: { type: 'object', properties: {
      file: { type: 'string', description: 'media filename, e.g. image27.png' },
      slides: { type: 'array', items: { type: 'integer' } },
      md5: { type: 'string' },
      kind: { type: 'string', enum: ['diagram', 'screenshot', 'map', 'plot', 'table', 'photo', 'chrome', 'other'] },
      depicts: { type: 'string', description: 'what the image actually shows, having opened it' },
      decision: { type: 'string', enum: ['keep', 'regenerate', 'skip'], description: 'keep = copy into the chapter; regenerate = a plot/table the chapter reproduces from code; skip = not useful' },
      target_chapter: { type: 'string' },
      target_name: { type: 'string', description: 'descriptive kebab/underscore filename for images/, only when keep' },
      alt: { type: 'string', description: 'draft alt text, one or two sentences, only when keep' },
    }, required: ['file', 'slides', 'kind', 'depicts', 'decision'] } },
  },
  required: ['deck', 'images'],
}

const OUTLINE_SCHEMA = {
  type: 'object',
  properties: {
    chapter: { type: 'string' },
    markdown: { type: 'string', description: 'the full outline section in the tier_d_outlines.md format' },
    data_needed: { type: 'array', items: { type: 'string' }, description: 'every data file the chapter reads, with its fa26-dev or main source path' },
    images_used: { type: 'array', items: { type: 'string' } },
  },
  required: ['chapter', 'markdown', 'data_needed', 'images_used'],
}

const AUTHOR_SCHEMA = {
  type: 'object',
  properties: {
    summary: { type: 'string' },
    wrote_ipynb: { type: 'boolean', description: 'to-ipynb succeeded and a scratch execution ran clean' },
    open_questions: { type: 'array', items: { type: 'string' } },
    numbers_in_prose: { type: 'array', items: { type: 'string' } },
  },
  required: ['summary', 'wrote_ipynb', 'open_questions'],
}

const GATE_SCHEMA = {
  type: 'object',
  properties: {
    executed: { type: 'boolean' },
    ok: { type: 'boolean' },
    debt: { type: 'integer' },
    fingerprint: { type: 'string' },
    failing: { type: 'array', items: { type: 'string' }, description: 'one line per failing gate detail, verbatim' },
  },
  required: ['executed', 'ok', 'debt', 'fingerprint', 'failing'],
}

const FINDINGS_SCHEMA = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['BLOCK', 'PASS'] },
    findings: { type: 'array', items: { type: 'object', properties: {
      where: { type: 'string' },
      severity: { type: 'string', enum: ['BLOCKING', 'ADVISORY'] },
      claim: { type: 'string' },
      evidence: { type: 'string' },
      fix: { type: 'string' },
    }, required: ['where', 'severity', 'claim', 'evidence', 'fix'] } },
  },
  required: ['verdict', 'findings'],
}

const REFUTE_SCHEMA = {
  type: 'object',
  properties: {
    refuted: { type: 'boolean' },
    reasoning: { type: 'string', description: 'what you re-derived, with the command and its output' },
  },
  required: ['refuted', 'reasoning'],
}

// ---------------------------------------------------------------- helpers

const PY = 'export PATH="/Users/jedwin321/miniforge3/envs/d100/bin:$PATH"'

// Both lecture agents are registered types (.claude/agents/). The prompt still names the contract
// and binds <lectures>, which the contract leaves as a placeholder.
function contract(name, body) {
  return `Your contract is .claude/agents/${name}.md.\n<lectures> = ${LECT}\n\n${body}`
}

// Execution is strictly serial (AGENTS.md wave 2): one kernel at a time. Every gate run goes
// through this chain, so chapters pipelined in parallel still execute one after another.
let execChain = Promise.resolve()
function serial(fn) {
  const p = execChain.then(fn)
  execChain = p.catch(() => null)
  return p
}

function gate(c, attempt) {
  return serial(() => agent(
    `${PY}\nConfirm python -c "import polars; print(polars.__version__)" prints 1.43.1.\n` +
    `Then, from /Users/jedwin321/Documents/data100/course-notes, run exactly:\n` +
    `  python conversion/nb_pytext.py to-ipynb --input conversion/pytext/polars/${c.ch}/${c.ch}.py --output content/${c.ch}/${c.ch}.ipynb\n` +
    `  python conversion/nb_execute.py --chapter ${c.ch}\n` +
    `  python conversion/authored_validate.py --chapter ${c.ch} --json\n` +
    `Do not edit any file. Report executed = whether nb_execute exited 0, and ok/debt/fingerprint from the JSON ` +
    `(ok=false, debt=999 if execution failed). failing = every non-PASS gate detail verbatim, plus nb_execute's ` +
    `error lines if it failed.`,
    { label: `gate:${c.ch}#${attempt}`, phase: 'Gate', schema: GATE_SCHEMA, effort: 'low' }))
}

function reviewers(c) {
  const common = `Chapter: content/${c.ch}/${c.ch}.ipynb (source conversion/pytext/polars/${c.ch}/${c.ch}.py). ` +
    `This is a NEWLY AUTHORED chapter: there is no pandas baseline, so skip every baseline-diff step in your contract ` +
    `and judge the artifact on its own. Lecture: ${c.slides}; deck extract under ${LECT}.`
  return [
    { key: 'claims', opts: { agentType: 'notes-claim-verifier' },
      prompt: `${common}\nAlso run every \`\`\`sql block in DuckDB against the chapter CSV (register it under the table name the SQL uses, adding any derived columns the chapter computed) and compare with the Polars output it pairs with.` },
    { key: 'a11y', opts: { agentType: 'notes-a11y-reviewer' },
      prompt: `${common}\nEvery figure is new: check each #| fig-alt and {image} :alt: against the figure it labels.` },
    { key: 'prose', opts: { agentType: 'notes-prose-reviewer' },
      prompt: `${common}\nJudge voice against the neighbouring chapters (intro_lec, regex, visualization_1). Prose findings are advisory unless a sentence is false or unreadable.` },
    { key: 'fidelity', opts: { agentType: 'notes-lecture-fidelity-reviewer' },
      prompt: contract('notes-lecture-fidelity-reviewer', `${common}\nEarlier EDA chapters to check assumed knowledge against: ${CHAPTERS.filter(x => x.ch < c.ch).map(x => x.ch).join(', ') || 'none'}.`) },
  ]
}

async function reviewAndRefute(c, attempt) {
  const reviews = await parallel(reviewers(c).map(r => () =>
    agent(r.prompt, { ...r.opts, label: `${r.key}:${c.ch}#${attempt}`, phase: 'Review', schema: FINDINGS_SCHEMA })
      .then(v => v && { ...v, reviewer: r.key })))
  const blocking = reviews.filter(Boolean).flatMap(r =>
    r.findings.filter(f => f.severity === 'BLOCKING').map(f => ({ ...f, reviewer: r.reviewer })))
  const advisory = reviews.filter(Boolean).flatMap(r =>
    r.findings.filter(f => f.severity !== 'BLOCKING').map(f => ({ ...f, reviewer: r.reviewer })))
  const judged = await parallel(blocking.map((f, i) => () =>
    agent(`${PY}\nAn independent reviewer made this BLOCKING finding about content/${c.ch}/${c.ch}.ipynb. ` +
      `Your job is to REFUTE it by re-deriving it yourself -- run the code, open the output, read the slide ` +
      `(${LECT}). Reviewers on this project have reported environmental drift as bugs and miscounted by one; ` +
      `only a finding you cannot refute survives. If you are uncertain, it is NOT refuted.\n\n` +
      `Reviewer: ${f.reviewer}\nWhere: ${f.where}\nClaim: ${f.claim}\nEvidence given: ${f.evidence}`,
      { label: `refute:${c.ch}#${attempt}.${i}`, phase: 'Refute', schema: REFUTE_SCHEMA })
      .then(v => ({ ...f, refutation: v }))))
  const survivors = judged.filter(Boolean).filter(f => !f.refutation || !f.refutation.refuted)
  log(`${c.ch} attempt ${attempt}: ${blocking.length} blocking, ${survivors.length} survived refutation, ${advisory.length} advisory`)
  return { survivors, advisory, refuted: judged.filter(Boolean).filter(f => f.refutation && f.refutation.refuted) }
}

// ---------------------------------------------------------------- pass 1: outline

if (PHASE === 'outline') {
  phase('Images')
  // Barrier: EDA V draws on two decks and several images recur across decks, so every outline
  // needs the whole de-duplicated manifest, not just its own deck's rows.
  const manifests = (await parallel(DECKS.map(d => () => agent(
    `Identify every image in the Fa26 deck extract ${LECT}/${d}/ (slides.md lists which media each slide shows; ` +
    `media/ holds the files). Open EVERY image with the Read tool -- do not guess from filenames or slide text. ` +
    `Template chrome was already removed by hash. For each image: what it depicts, and a decision:\n` +
    `- keep: a diagram, screenshot, or map that code cannot produce (boxplot anatomy, split-apply-combine, join diagrams, ` +
    `star schema, EDA workflow, data-source website screenshots, maps);\n` +
    `- regenerate: a plot or table the chapter will reproduce from code (never paste a plot);\n` +
    `- skip: announcements, Askademia screenshots, decorative photos, LLM-chat screenshots, duplicates.\n` +
    `Compute md5 with \`md5 -q\` so duplicates across decks can be merged. For keep, propose target_chapter using this scope:\n${SCOPE_TABLE}\n` +
    `and a descriptive target_name (e.g. split_apply_combine_count.png) plus draft alt text that states what the figure shows.`,
    { label: `images:${d}`, phase: 'Images', schema: IMAGES_SCHEMA, effort: 'medium' })))).filter(Boolean)

  const seen = new Set()
  const manifest = manifests.flatMap(m => m.images.map(i => ({ deck: m.deck, ...i })))
    .filter(i => { const k = i.md5 || `${i.deck}/${i.file}`; if (seen.has(k)) return false; seen.add(k); return true })
  log(`manifest: ${manifest.length} unique images, ${manifest.filter(i => i.decision === 'keep').length} kept`)

  phase('Outline')
  const outlines = (await parallel(CHAPTERS.map(c => () => agent(
    `Write the outline for ${c.ch} ("${c.title}") of the Data 100 course notes, in the format of conversion/tier_d_outlines.md ` +
    `(a disposition table mapping each slide range to Kept/Rewritten/Deleted, a numbered "Proposed shape" with the concept each ` +
    `section carries, the Learning Outcomes bullets, and the open questions). Load data100-textbook-voice and read ` +
    `.claude/skills/pandas-to-polars/fa26-course-conventions.md.\n\n` +
    `Scope of this chapter: ${c.slides}. Lecture notebook: ${c.notebook}. Deck extract: ${c.decks.map(d => `${LECT}/${d}/slides.md`).join(', ')}.\n` +
    `The five chapters and their scopes (do NOT take another chapter's material):\n${SCOPE_TABLE}\n\n` +
    `Constraints: readers never saw polars_1/polars_2, so list the Polars verbs this chapter introduces for the first time. ` +
    `Each operation keeps the lecture's English -> Polars -> SQL framing. Plots are regenerated from code. ` +
    `Name every data file the chapter needs and where it comes from (main:content/new_eda_1/data/, or fa26-dev lec0N/data). ` +
    `The UCB dataset is lec04's pivoted-ucb-data-w-everything.csv (identical to main's copy); lec06's copy encodes nulls as the string "NA" ` +
    `and is only useful as a faithfulness/missing-encoding demo. Pick images from this manifest (keep rows only):\n` +
    JSON.stringify(manifest.filter(i => i.decision === 'keep')),
    { label: `outline:${c.ch}`, phase: 'Outline', schema: OUTLINE_SCHEMA })))).filter(Boolean)

  // Barrier: overlap between neighbouring chapters is only visible with all five outlines at once.
  const critic = await agent(
    `You are the completeness and overlap critic for five chapter outlines. Read them all, then:\n` +
    `1. Find any concept assigned to two chapters, or any slide in the scope table assigned to none; fix by editing the outlines.\n` +
    `2. Check every Polars verb is introduced in the first chapter that uses it.\n` +
    `3. Write conversion/eda_outlines.md: a header saying "Status: draft -- awaiting approval" (each chapter section also carries ` +
    `its own "Status: draft" line a human flips to "Status: approved"), the scope table, then the five outlines.\n` +
    `4. Write ${LECT}/images_manifest.yml from the manifest below (keep and regenerate rows, with target paths).\n` +
    `Return a short summary of what you changed and the open questions for course staff.\n\n` +
    `Scope table:\n${SCOPE_TABLE}\n\nOutlines:\n${JSON.stringify(outlines)}\n\nManifest:\n${JSON.stringify(manifest)}`,
    { label: 'outline-critic', phase: 'Outline' })
  return { manifest, outlines: outlines.map(o => ({ chapter: o.chapter, data_needed: o.data_needed, images_used: o.images_used })), critic }
}

// ---------------------------------------------------------------- pass 2: build

async function buildChapter(c) {
  let fixList = null, lastDebt = Infinity, lastFp = null
  const history = []
  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
    const authored = await agent(contract('lecture-chapter-author',
      `Your chapter: ${c.ch} ("${c.title}"). Scope: ${c.slides}. Lecture notebook: ${c.notebook}. ` +
      `Decks: ${c.decks.join(', ')}. Earlier EDA chapters (what the reader already knows): ` +
      `${['new_eda_1', 'new_eda_2', 'new_eda_3', 'new_eda_4'].filter(x => x < c.ch).join(', ') || 'none'}.\n` +
      (fixList ? `\nThis is attempt ${attempt}. Fix exactly these problems, and nothing else:\n${fixList}` : '')),
      { agentType: 'lecture-chapter-author', label: `author:${c.ch}#${attempt}`, phase: 'Author', schema: AUTHOR_SCHEMA })
    if (!authored) { history.push({ attempt, stage: 'author', result: 'agent died' }); break }

    const g = await gate(c, attempt)
    history.push({ attempt, gate: g })
    if (!g || !g.ok) {
      if (g && g.fingerprint === lastFp) { log(`${c.ch}: identical failure fingerprint twice -- bailing`); return { ch: c.ch, status: 'BAILED_SAME_FAILURE', history, authored } }
      if (g && g.debt >= lastDebt) { log(`${c.ch}: debt did not fall (${lastDebt} -> ${g.debt}) -- bailing`); return { ch: c.ch, status: 'BAILED_NO_PROGRESS', history, authored } }
      lastDebt = g ? g.debt : lastDebt; lastFp = g ? g.fingerprint : lastFp
      fixList = g ? `Gate failures (authored_validate / nb_execute):\n- ${g.failing.join('\n- ')}` : 'The gate agent died; re-run to-ipynb and a scratch execution and report any error.'
      continue
    }
    // A chapter that fails the gate never reaches reviewers (AGENTS.md wave 3).
    const r = await reviewAndRefute(c, attempt)
    history.push({ attempt, review: { survivors: r.survivors.length, advisory: r.advisory.length, refuted: r.refuted.length } })
    if (!r.survivors.length) return { ch: c.ch, status: 'READY_FOR_HUMAN', attempts: attempt, advisory: r.advisory, refuted: r.refuted, open_questions: authored.open_questions, history }
    fixList = r.survivors.map(f => `- [${f.reviewer}] ${f.where}: ${f.claim} -> ${f.fix}`).join('\n')
    lastDebt = Infinity; lastFp = null   // the gate passed; the next gate starts a fresh ladder
  }
  return { ch: c.ch, status: 'NEEDS_HUMAN_REVIEW', history, lastFixList: fixList }
}

if (PHASE === 'build') {
  const results = await pipeline(CHAPTERS, c => buildChapter(c))
  const ready = results.filter(Boolean).filter(r => r.status === 'READY_FOR_HUMAN')

  phase('Site')
  let site = null
  if (ready.length) {
    site = await serial(() => agent(
      `${PY}\nexport PATH="/Users/jedwin321/.nvm/versions/node/v18.20.8/bin:$PATH"\n` +
      `From /Users/jedwin321/Documents/data100/course-notes:\n` +
      `1. Make myst.yml's toc list content/new_eda_N/new_eda_N.ipynb for every N in 1..5 whose notebook EXISTS, ` +
      `directly after content/intro_lec/introduction.ipynb and in N order, and for no N whose notebook is missing. ` +
      `MyST refuses the whole build if a toc entry points at a missing file. Edit only those toc lines.\n` +
      `2. Run \`python conversion/site_gate.py\` and report its G14/G15 verdicts and every problem line verbatim. ` +
      `Edit nothing else.`,
      { label: 'site-gate', phase: 'Site' }))
    const render = await parallel(ready.map(r => () => agent(
      `Chapter ${r.ch}: the site has just been built into _build/html. This is a newly authored chapter (no baseline page). ` +
      `Check its page against its source per your contract.`,
      { agentType: 'notes-render-reviewer', label: `render:${r.ch}`, phase: 'Site', schema: FINDINGS_SCHEMA })
      .then(v => v && { ch: r.ch, ...v })))
    site = { gate: site, render: render.filter(Boolean) }
  }
  return { results, site }
}

throw new Error(`unknown args.phase ${PHASE}; use "outline" or "build"`)
