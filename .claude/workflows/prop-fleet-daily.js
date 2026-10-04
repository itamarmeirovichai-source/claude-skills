export const meta = {
  name: 'prop-fleet-daily',
  description: 'Daily run of the MeiroX prop-fleet agent organization: workers research, heads decide, the statistics referee vetoes, the director writes the board',
  whenToUse: 'Once per trading day, from the scheduled routine. Args: {date: "YYYY-MM-DD", n: <sum of ledger count column>}.',
  phases: [
    { title: 'Workers', detail: 'eight workers across four divisions' },
    { title: 'Heads', detail: 'four division heads, each seeing every worker' },
    { title: 'Referee', detail: 'statistics head with veto plus red team on every claimed edge' },
    { title: 'Director', detail: 'decides the day, writes the board and the Hebrew report' },
  ],
}

const DATE = (args && args.date) || 'unknown-date'
const ROOT = 'skills/prop-fleet'

const COMMON = `
You are part of the MeiroX prop-fleet agent organization. Today is ${DATE}.
Before anything else read ${ROOT}/agents/ORG.md (the charter, the goal, the two
rules that cannot change, the gate), ${ROOT}/agents/board.md (yesterday's shared
state) and ${ROOT}/agents/ledger.csv (every hypothesis ever tested; N = sum of
the count column). Existing tools: ${ROOT}/scripts/ (trend_backtest.py,
stack_backtest.py, tjr_backtest.py, apex_model.py and their tests) and
${ROOT}/references/ (every result so far). Shared goal: >20%/yr net from many
funded prop accounts, fully automatic. Network: GitHub raw and PyPI and web
search work; most market-data and company sites are blocked (EGRESS_BLOCKED) —
report the host and move on, never route around. Never buy, sign up, move money,
or contact anyone. Never claim an edge; only the referee can. Never invent a
number — every number you report must come from a source you name or a command
you ran. Do not edit board.md, ORG.md or ledger.csv; the director's step writes
them. You may write new files only under ${ROOT}/agents/daily/${DATE}/ .
Return only the structured output.`

const WORKER_SCHEMA = {
  type: 'object',
  properties: {
    summary: { type: 'string', description: 'three sentences, English' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          claim: { type: 'string' },
          evidence: { type: 'string', description: 'numbers, command run, or source' },
          source: { type: 'string', description: 'URL, file path or command' },
          confidence: { type: 'string', enum: ['verified', 'corroborated', 'single-source', 'unverified'] },
        },
        required: ['claim', 'evidence', 'source', 'confidence'],
      },
    },
    hypotheses_tested: {
      type: 'array',
      description: 'every hypothesis you backtested today, for the ledger',
      items: {
        type: 'object',
        properties: {
          hypothesis: { type: 'string' },
          rules: { type: 'string', description: 'the exact rules, written before the test' },
          count: { type: 'integer', description: 'number of variants run' },
          data: { type: 'string' },
          mean_R: { type: ['number', 'null'] },
          p5_R: { type: ['number', 'null'] },
          trades: { type: ['integer', 'null'] },
          trades_per_year: { type: ['number', 'null'] },
          script: { type: 'string', description: 'path of the script you ran' },
        },
        required: ['hypothesis', 'rules', 'count', 'data', 'mean_R', 'p5_R', 'trades', 'trades_per_year', 'script'],
      },
    },
    blockers: { type: 'array', items: { type: 'string' } },
    next: { type: 'array', items: { type: 'string' }, description: 'what you would do tomorrow' },
  },
  required: ['summary', 'findings', 'hypotheses_tested', 'blockers', 'next'],
}

const WORKERS = [
  { key: 'literature', division: 'edge', title: 'Literature scout',
    task: `Find intraday or short-horizon futures/ES/NQ edges with public evidence that the board has NOT already covered (check board.md and ledger.csv). Prefer peer-reviewed papers and independent replications with code; record sample period, costs, Sharpe, drawdown, and whether the edge is reported to persist after publication. Two to four candidates, ranked by how testable they are with data reachable here.` },
  { key: 'data', division: 'edge', title: 'Data hunter',
    task: `Find free intraday (1-min or 5-min) data for ES, NQ, SPY or QQQ covering 2019–2026 that is reachable from here (GitHub raw, PyPI packages that ship data). Download a small sample to ${ROOT}/agents/daily/${DATE}/ to prove reachability, report columns, timezone, period, gaps. Do not commit large files. Also report which known sources are blocked.` },
  { key: 'builder', division: 'edge', title: 'Hypothesis builder',
    task: `Write ONE new pre-registered intraday hypothesis that is not in ledger.csv, fix its rules completely in your output BEFORE running anything, implement it as ${ROOT}/agents/daily/${DATE}/hypothesis.py reusing tjr_backtest.py's data loader and cost model (0.6 pt round trip, stop-first on ambiguous bars), run it on the S&P minute data 2010–2018, and report mean R, bootstrap 5th percentile, trades, trades per year, and gross vs net. One hypothesis, at most three variants, all reported.` },
  { key: 'rules', division: 'prop', title: 'Rules keeper',
    task: `For MyFundedFutures, Bulenox, Tradeify, Lucid, Topstep and Apex: current rules on fully automated trading on FUNDED accounts (not only evaluations), max accounts per person, copy-trading across own accounts, required platform/API, VPS rules, 50K drawdown type and size, evaluation clock, payout caps. Cite the source for each cell; mark firm's own help center as verified, third-party as corroborated. Note firm sites that are blocked.` },
  { key: 'econ', division: 'prop', title: 'Economist',
    task: `Using ${ROOT}/scripts/apex_model.py (read it; add a plan to a COPY under ${ROOT}/agents/daily/${DATE}/ if a firm's numbers differ, never edit the original), estimate net yearly income across a 20-account fleet split over the firms the board lists, at expectancies of +0.10R, +0.25R and +0.40R. State every input and its source. Flag inputs that are unverified.` },
  { key: 'stats', division: 'risk', title: 'Statistician',
    task: `Audit the ledger and every result in references/ for statistical soundness: is N counted correctly, are any results reported without bootstrap lower bounds, is there look-ahead risk in any script used for a headline number. Propose concrete fixes with file:line.` },
  { key: 'redteam', division: 'risk', title: 'Red team',
    task: `Attack the board's current beliefs, especially the claim that some prop firms allow full automation on funded accounts and the claim that the required Sharpe is ~3. Find the strongest evidence against each. Default to "refuted" when evidence is thin.` },
  { key: 'engineer', division: 'eng', title: 'Engineer',
    task: `Run every test suite in ${ROOT}/scripts/ (python3 -m pytest -q) and report pass/fail counts. Then write a concrete automation route for the allowed firms: which API (ProjectX/TopstepX, Tradovate, Rithmic), what the bot (which today speaks only IBKR) would need, and the smallest first step. Do not modify existing scripts unless a test fails; if one fails, fix it minimally and report the diff.` },
]

const HEADS = [
  { key: 'edge', title: 'Head of Edge Research', focus: 'Is there any candidate edge worth tomorrow\'s work, and what is the single best next experiment?' },
  { key: 'prop', title: 'Head of Prop Structure', focus: 'Which firms satisfy both unchangeable rules, with how many accounts, and what does it pay at each expectancy?' },
  { key: 'eng', title: 'Head of Engineering & Operations', focus: 'Is the repository healthy, and what is the shortest path to an automated order route at an allowed firm?' },
]

const HEAD_SCHEMA = {
  type: 'object',
  properties: {
    decision: { type: 'string', description: 'one paragraph, English' },
    keep: { type: 'array', items: { type: 'string' } },
    drop: { type: 'array', items: { type: 'string' } },
    tomorrow: { type: 'array', items: { type: 'string' } },
    concerns_about_other_divisions: { type: 'array', items: { type: 'string' } },
  },
  required: ['decision', 'keep', 'drop', 'tomorrow', 'concerns_about_other_divisions'],
}

const VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    hypothesis: { type: 'string' },
    passes_gate: { type: 'boolean' },
    failed_criteria: { type: 'array', items: { type: 'string' } },
    reasoning: { type: 'string' },
  },
  required: ['hypothesis', 'passes_gate', 'failed_criteria', 'reasoning'],
}

const DIRECTOR_SCHEMA = {
  type: 'object',
  properties: {
    board_md: { type: 'string', description: 'the full new board.md, English, same structure as today' },
    ledger_rows: {
      type: 'array',
      description: 'new ledger rows, one per hypothesis tested today, in the CSV column order of ledger.csv, without id (ids are assigned after)',
      items: { type: 'string' },
    },
    report_he: { type: 'string', description: 'the report to Itamar in Hebrew, under 250 words: what was found, what failed, the one decision, what tomorrow does. No invented numbers.' },
    edge_found: { type: 'boolean' },
  },
  required: ['board_md', 'ledger_rows', 'report_he', 'edge_found'],
}

phase('Workers')
log(`Day ${DATE}: ${WORKERS.length} workers across 4 divisions`)
const workerOut = await parallel(WORKERS.map(w => () =>
  agent(`${COMMON}\n\nYour role: ${w.title} (division: ${w.division}).\n\nToday's task: ${w.task}`,
    { label: `worker:${w.key}`, phase: 'Workers', schema: WORKER_SCHEMA })
    .then(r => r && ({ ...r, key: w.key, title: w.title, division: w.division }))))
const workers = workerOut.filter(Boolean)
const dropped = WORKERS.length - workers.length
if (dropped) log(`${dropped} worker(s) returned nothing`)
const digest = JSON.stringify(workers, null, 1)

phase('Heads')
const heads = (await parallel(HEADS.map(h => () =>
  agent(`${COMMON}\n\nYour role: ${h.title}. Your question: ${h.focus}\n\nEvery worker's output today (all divisions, so you know what the others did):\n${digest}`,
    { label: `head:${h.key}`, phase: 'Heads', schema: HEAD_SCHEMA })
    .then(r => r && ({ ...r, key: h.key, title: h.title }))))).filter(Boolean)

phase('Referee')
const tested = workers.flatMap(w => (w.hypotheses_tested || []).map(t => ({ ...t, by: w.key })))
const nPrior = (args && args.n) || 173   // the routine passes the ledger's current N
const verdicts = await parallel(tested.map(t => () =>
  parallel([0, 1, 2].map(i => () =>
    agent(`${COMMON}\n\nYou are ${i === 0 ? 'the Head of Statistics & Risk (veto holder)' : `skeptic #${i} of the red team`}. Decide whether this result passes ALL FOUR criteria of the gate in ORG.md. Prior N from the ledger is ${nPrior} plus today's variants. Re-run the script yourself if it exists (${t.script}) and check the numbers match. Default to passes_gate=false when anything is missing or uncertain.\n\nResult:\n${JSON.stringify(t, null, 1)}`,
      { label: `referee:${i}:${(t.hypothesis || '').slice(0, 24)}`, phase: 'Referee', schema: VERDICT_SCHEMA })))
    .then(vs => {
      const v = vs.filter(Boolean)
      return { ...t, verdicts: v, passes: v.length === 3 && v.every(x => x.passes_gate) }
    })))
const judged = verdicts.filter(Boolean)
log(`${tested.length} hypotheses tested today; ${judged.filter(j => j.passes).length} passed the gate`)

phase('Director')
const director = await agent(`${COMMON}\n\nYou are the Director. Decide the day. Inputs:\n\nWORKERS:\n${digest}\n\nHEADS:\n${JSON.stringify(heads, null, 1)}\n\nREFEREE (unanimous pass required; the referee's veto is final):\n${JSON.stringify(judged, null, 1)}\n\nWrite the new board.md (state, open questions, what each division does tomorrow), the new ledger rows, and the Hebrew report to Itamar. If nothing passed the gate, say so plainly in the report.`,
  { label: 'director', phase: 'Director', schema: DIRECTOR_SCHEMA })

return { date: DATE, workers, heads, judged, director, dropped }
