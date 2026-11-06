# quant-edge WORK-LOG

Program: autonomous quant research org for Itamar. Master prompt: `prompts/quant-edge-master-prompt.md`
on branch `claude/sweet-dijkstra-kshdva` (PR #26). Program root: `quant-edge/`. Data root: `~/quant-edge-data/`
(= `/root/quant-edge-data`). Inherited record (read-only worktrees, outside the repo):
`~/quant-edge-inherited/pr4/skills/prop-fleet/` (branch `claude/friendly-galileo-eakzlm`, commit e0f5e59) and
`~/quant-edge-inherited/pr26/prompts/` (branch `claude/sweet-dijkstra-kshdva`, commit b5cd0de).
Recreate them with `quant-edge/tools/fetch_inherited.sh` if missing (they do not survive a new container).

## Decisions taken (never reopened)

- D-001 (2026-11-03) RESEARCH_BRANCH is `claude/keen-cori-fvtxcl`, the branch the platform assigned to this
  session, not `quant-edge`: the platform rule forbids pushing to any other branch. One draft PR against `main`.
  Recorded as a parameter change in `PARAMETERS.md`. Nothing is pushed to `claude/friendly-galileo-eakzlm` or
  `claude/sweet-dijkstra-kshdva`.
- D-002 (2026-11-03) N_total = 280 + 150 = 430. Bar: one-sided z(0.05/430) = 3.6807; a variant without a fixed
  sign occupies two counts and is tested at z(0.025/430) = 3.8538; bootstrap ≥ 430,000 day-level draws.
  The bar never comes down. Tool: `tools/registry_n.py`, tests in `tests/test_registry_n.py`.
- D-003 (2026-11-03) Inherited material is read from git worktrees under `~/quant-edge-inherited/`, never copied
  into this branch (no duplication of PR #4 / PR #26 content; licence-held data stays out of the branch).
- D-004 (2026-11-03) Hold-out: 2025-01-01 to the Databento plan's purchase date; stored under
  `DATA_ROOT/holdout/`; unlock date 2026-12-05 (DEADLINE minus 14 days) by creating `quant-edge/HOLDOUT_UNLOCK`.
- D-005 (2026-11-03) No paid Databento call until Itamar confirms in writing (a) remaining credit, expiry and
  signup date and (b) the portal monthly limit; the key is read only from the DATABENTO_API_KEY environment
  variable, which is absent today. Everything free proceeds.
- D-006 (2026-11-03) Registry schema: the 11 inherited ledger columns are kept verbatim inside a 31-column
  `registry.csv` (see `tools/seed_registry.py`); inherited rows are never edited. Program rows get
  `source=program` and a `registered_commit` once committed.
- D-007 (2026-11-03) Blocked hosts are reported, never routed around: Dukascopy datafeed (connection reset),
  SSRN (403), lucidtrading.com (403). Yahoo and CFTC answer only with a browser User-Agent (allowed, not a bypass).
- D-008 (2026-11-03, pre-mortem mode 4) The hold-out pass criterion is restated in the one-sided tolerance form
  (PARAMETERS.md, "Hold-out pass criterion"); the written form passes a no-decay true edge 48% of the time. Reported to Itamar
  in the next daily report as a change to the master prompt's standard.
- D-009 (2026-11-03, mode 3) "Derivative" extends to published evidence; candidate briefs carry an evidence-window field.
- D-010 (2026-11-03, modes 1, 10) No P&L is computed before step 2.2 is green: `load()` is the only door, licence-held datasets
  are crosscheck-only (`LicenceHoldError`), `tests/test_no_direct_reads.py` fails on any direct read, and the Referee rejects a
  result file whose reads are not in `registry_reads.log`.
- D-011 (2026-11-03, mode 8) The Day-0 power line was criterion 4 alone; the joint figure (0.32 / 0.63 / 0.72 at true Sharpe 1.5
  over 5 / 8 / 10 years, costs one third of gross) is printed in PARAMETERS.md and in every result file; the correction goes to Itamar
  in the next report. The 2× cost criterion means only edges with gross ≥ about 3× round-trip cost can be certified.
- D-012 (2026-11-03, modes 2, 9) Critical path written in PARAMETERS.md (6 Nov Databento trigger, 28 Nov Gate 5 for S1, 5 Dec
  hold-out, 19 Dec memo); P1 only after Gates 4+5 and the hold-out read; memo template written before any result
  (`reports/memo-template.md`) with its "not tested: data not bought" and "weaker stated standard" tables.
- D-013 (2026-11-03, mode 2) Two calibration replications: CAL-D on the free daily pipeline (inherited 54-futures TSMOM, expected
  Sharpe ≈ 1.17 on 1984–2016, H0007 as the reference) registered Day 1; CAL-I (noise-area model on ES 1m, expected 0.9–1.25 on
  2016–2024) registered when Databento bars exist. If Databento is unconfirmed on 6 Nov, CAL-I runs on the licence-held FirstRate
  ES copy through window="crosscheck", labelled "pipeline calibration on licence-held data, never a gated result", after Itamar's ruling.
- D-014 (2026-11-03, mode 6) The firm letters go to Itamar as ONE decision request this week ("send now"), not "before any purchase".
- D-015 (2026-11-04) Concurrency lowered to 3 agents in total (Workflow 2 + 1 Agent-tool agent) after the account's 5-hour usage
  limit killed all six concurrent agents on 2026-11-03 at ≈ 15:05 UTC (pre-mortem mode 5 realised). Raise again only after a full run
  finishes inside the window.
- D-017 (2026-11-06) After the second usage-limit stop (2026-11-04 ≈ 19:30 UTC, sweep run + data run killed), runs are SEQUENTIAL: one agent at a time, each writing its output every few minutes; the 7 per-scout analysts are replaced by one merge-and-prioritize agent that reads the six scout files (149 blocks) and does the analyst checks inline.
- D-016 (2026-11-04) Economist re-run accepted as final (report complete when the agent died): $20k/slot-year at FTMO Swing needs net
  Sharpe 2.44 / 1.95 / 1.45 at 12 / 15 / 20% vol pre-tax; after tax 3.16 / 2.53 / 1.89 (25%) or > 4.0 / 3.47 / 2.61 (47%); planning
  number at 20% vol after tax = 2.6 until the accountant answers. Required-Sharpe table on the board refreshed from it.

## Steps

### Phase 0 — orientation (Day 0, 2026-11-03)
- [x] 0.1 Repo state: no `quant-edge` branch on the remote → Day 0. Fetched the two inherited branches.
- [x] 0.2 Environment: Python 3.13.18, 4 CPU, 15 GB RAM, 30 GB free disk; installed numba, scipy, pytest,
      databento, pyarrow, statsmodels, zstandard, detect-secrets. DATABENTO_API_KEY absent. Network per D-007.
- [x] 0.3 Day-0 message sent in Hebrew (chat, 2026-11-03 ~14:25 UTC); copy in `reports/2026-11-03.md`.
- [x] 0.4 PROGRAM_ROOT created; `registry.csv` seeded with 105 inherited rows, count sum 280 (test passes).
- [x] 0.5 Bar fixed (D-002) and written on the board.
- [x] 0.6 `.gitignore` and pre-commit hook (`tools/pre-commit.sh` → `.git/hooks/pre-commit`; detect-secrets
      baseline `quant-edge/.secrets.baseline`).
- [x] 0.7 Draft PR "quant-edge program" opened: https://github.com/itamarmeirovichai-source/claude-skills/pull/27 (commit 4a56ac1).
- [x] 0.8 Red Team pre-mortem returned 15:00 UTC → `daily/2026-11-03/redteam-premortem.md` (12 modes). Answers:
      mode 1 → D-010 (gateway committed with 10 tests + direct-read scanner); mode 2 → D-013 + critical path; mode 3 → D-009;
      mode 4 → D-008; mode 5 → accepted risk with `tools/inflight_check.sh` and the 30-minute write rule in every brief;
      mode 6 → D-014; mode 7 → memo template §5 + Economist re-run pending; mode 8 → D-011 (`tools/joint_power.py`);
      mode 9 → D-012; mode 10 → D-010 (`LicenceHoldError`) + licence ruling in this week's decision request; mode 11 → Gate 2
      before Gate 3 (already in process) + "session-edge and roll-week share" table added to the standard result tables;
      mode 12 → Rules Keeper Day-1 fetch brief + a preliminary path-wise breach count at Gate 3 for information.
      Accepted risks signed as the Red Team listed them (agent deaths with the write rule; target unreachable → honest N1;
      bar fixed at 430; no Alpaca key; blocked hosts; Phase 6 on IBKR paper at most P1; credit expiry; Monte Carlo noise).
- [x] 0.9 Economist F2-12 re-run → `economics/required-sharpe-2026-11.md` + `economics/f2_rerun/` (agent died at the usage limit after finishing; D-016).
- [x] 0.10 Scribe briefs returned 14:56 UTC → `briefs/inherited-{closed-families,method-lessons,data-in-hand,firms,economics,code-reusable,open-directions}.md` (≈ 600 words each). Not found by the Scribe: F2-12..15 figures in a readable report (Economist re-run is the authority), TradeDay flat-by time and FTMO funded-stage agreement (Rules Keeper matrix brief), sha256 pins for the old Binance/Yahoo/SEC pulls (none recorded).
- [ ] 0.11 Gate 0: everything above exists in the repository (commit hash recorded here).

### Phase 1 — the sweep (Days 1–4, 2026-11-04 → 2026-11-07)
- [~] 1.1 Department B sweep: run `wf_2a3bbcb1-b48` died at the usage limit 2026-11-03 15:07 UTC with 2 of 7 scouts complete (academic-flows-events 25 candidates, academic-session-momentum 20); resumed 2026-11-04 18:45 UTC with the script patched (killed scouts continue their files). Originally launched 14:34 UTC as Workflow run `wf_2a3bbcb1-b48` (script `~/.claude/projects/-home-user-claude-skills/c1c15771-3f18-56a1-8828-ab24630be4a0/workflows/scripts/quant-edge-sweep-b-wf_2a3bbcb1-b48.js`; resume with scriptPath + resumeFromRunId) → `research/sweep/*.md`, `research/candidates.md`, `research/prescreen-2026-11-03.md` (≥ 100 mechanisms, ≥ 30% original). Brief: `briefs/B-sweep-common.md`.
- [ ] 1.2 Department E pre-screen (closed-family overlap, look-ahead by construction, economics screen).
- [x] 1.3 Firm letters → `letters/{ftmo,topstep,myfundedfutures,tradeday,lucid,bulenox,accountant}.md` + `letters/README.md` (Hebrew) + `economics/firm-pages-fetched-2026-11-03.md` (94 lines of sources). Lucid unverified (blocked). Decision request sent to Itamar 2026-11-04 (`reports/2026-11-04.md`).
- [ ] 1.4 CAL calibration replication registered (noise-area model on ES, expected Sharpe 0.9–1.25, 2016–2024).
- [ ] 1.5 First batch (≤ 20 variants + CAL) registered; Gate 1 per row (commit before code).

### Phase 2 — data (Days 1–6, in parallel)
- [~] 2.1 Department C data run: first launch died 2026-11-03; relaunched 2026-11-04 19:12 UTC (compute slot; brief `briefs/C-data-run.md`).
- [x] 2.2a `load(id, window)` gateway (`src/qe/gateway.py`, `registry.py`) with 10 tests (incl. licence-hold crosscheck-only) + `tests/test_no_direct_reads.py`; `tools/register.py` (Gate-1 validation: fields, split ≥ 5 OOS years unless post-change, sign/count, family cap 5, 2× cost stated, results empty, stamp commit) with 4 tests: unregistered/inherited id refused, IS/OOS slicing, every read logged, hold-out lock (file + id list), planted 2025 row never leaks. Gate statistics `src/qe/stats.py` (iid/NW/clustered t, stationary + day-cluster bootstraps at 430k draws, Mertens/Opdyke SE, Lo factor, DSR, CSCV) with 7 synthetic tests. Steward `src/qe/steward.py` (credit file gate, ceilings, 10-min alignment, estimate row before request, per-request accounting, batch-vs-stream rule) with 6 tests. 32 tests pass.
- [x] 2.2b shared engine `src/qe/engine/` (Department D, 2026-11-04): fills (stop-first ambiguity, bar-granularity stops, gap-through at open, limit on trade-through), flat-by at deadline − 2 min (half day = min(firm, early close)), 1×/2× costs on one path, truncation + perturbation harnesses, nulls, report; synthetic 16-year calibration mean R 0.012 ± 0.007 (driftless walk, 2R/1R); 52 tests. Still open: real-data loaders (Department C), FTMO swaps and crypto funding in costs, sub-minute hold share.
- [~] 2.3 Calendar and Clock Keeper: the engine agent left a 263-line `src/qe/sessions.py` stub (interface + TODO list for Department C); kept.
- [ ] 2.4 Databento Day-1 purchase (1d all roots + definition + statistics, ≈ $2) — BLOCKED on Day-0 items (a), (b), (c).
- [ ] 2.5 Databento plan file inside the ceiling, each purchase with requesting row ids.
- [ ] 2.6 Gate 2.

### Phase 3 — testing (Days 5–20, batches)
- [ ] 3.1 Batch 1 run exactly as registered; one OOS read each through `load(id, "oos")`.
- [ ] 3.2 Referee Gate 3 verdicts; near-miss list with power at S = 1.5 / 2.0 / 2.4.
- [ ] 3.3 Batch 2+ (≤ 25) after verdicts and a lessons note.

### Phase 4 — verification (rolling)
- [ ] 4.1 Re-implementer, Leak Hunter, Red Team, Null-Model Builder, Multiple-Testing Auditor per Gate-3 pass.

### Phase 5 — economics and compliance (rolling, after E's PASS)
- [ ] 5.1 Criterion 11, stressed $/slot-year per firm, compliance matrix, scaling plan.

### Phase 6 — paper trading (≥ 3 weeks or ≥ 60 trades)
- [ ] 6.1 Real order path in simulation; tolerance written before the first fill.

### Phase 7 — decision memo (by 2026-12-19)
- [ ] 7.1 One of S1 / S2 / P1 / N1 in Hebrew with an English appendix.

### Standing (every day)
- [ ] G.1 Week 1: IBKR connectivity diagnosis document (Department G) → `engineering/ibkr-connectivity-diagnosis.md`.
- [ ] Rules Keeper monthly re-fetch; first fetch Day 1 → `economics/firms-matrix-2026-11.md`.

## Checkpoint

- phase: 1 (sweep) + 2 (data) groundwork; Day 0 closed except Gate 0 bookkeeping
- running N: 280 (inherited) + 0 (program) = 280; budget left 150; N_total 430; bar z = 3.6807 (two-count 3.8538)
- spend total: $0.00 (Databento ceiling not yet set: credit unconfirmed)
- open decision requests (date sent): Day-0 items (1)–(4) (2026-11-03); send the firm letters this week + licence ruling on third-party copies (2026-11-04)
- next action (2026-11-06): sequential (D-017): merge+prioritize agent → candidates.md; then Dept E prescreen; then register CAL-D + batch 1; data run resumes after. Previously: when the sweep returns, read prescreen and register CAL-D + batch 1 (Gate 1); then Rules Keeper matrix and Department G IBKR diagnosis.

## Agents in flight

| name | brief file | output file | start (UTC) | status |
|---|---|---|---|---|
| Red Team pre-mortem | briefs/E-redteam-premortem.md | daily/2026-11-03/redteam-premortem.md | 2026-11-03 14:31 | done 14:50 |
| Economist F2-12 re-run | briefs/F-economist-f2-12.md | economics/required-sharpe-2026-11.md | 2026-11-03 14:31 | dead 15:05 (usage limit); output complete, accepted |
| Scribe inherited briefs | briefs/A-scribe-inherited.md | briefs/inherited-*.md | 2026-11-03 14:31 | done 14:56 |
| Rules Keeper firm letters | briefs/F-rules-keeper-letters.md | letters/*.md, economics/firm-pages-fetched-2026-11-03.md | 2026-11-03 14:43 | dead 15:03 (usage limit); 8 files complete, accepted |
| Dept C data run | briefs/C-data-run.md | src/qe/ingest/*, src/qe/calendars.py, data/manifest.csv, data/qa/*.md | 2026-11-04 19:12 | relaunched (first launch dead 2026-11-03) |
| Dept D shared engine | briefs/D-engine.md | src/qe/engine/*, src/qe/sessions.py (stub), tests | 2026-11-03 14:57 | relaunched 2026-11-04 18:45; done 19:10: engine (bars, rules, fills, pnl, harness, report, run), CONVENTIONS.md, 52 tests pass + 1 opt-in 16-year run (QE_SLOW=1, 213 s, mean R 0.012 ± 0.007) |
| Dept B sweep workflow wf_2a3bbcb1-b48 (7 scouts + analysts + prioritizer + critic + prescreen) | briefs/B-sweep-common.md | research/sweep/*.md, research/candidates.md, research/prescreen-2026-11-03.md | 2026-11-03 14:34 | dead 15:07 (usage limit), 2/7 scouts done; resumed 2026-11-04 18:45 (same run id, patched script) |

## Session log (append-only)

- 2026-11-03 (UTC, from `date -u`; earlier entries were estimates) 14:18 session start (Day 0). 14:22 Day-0 message sent. 14:25 skeleton written. 14:28 commit 4a56ac1 pushed; PR #27 opened. 14:31 Red Team, Economist, Scribe launched. 14:34 sweep workflow wf_2a3bbcb1-b48 launched. 14:43 Rules Keeper letters launched. 14:46 core modules (gateway, stats, steward) committed, 26 tests. 14:50 pre-mortem returned; 14:58 answered (D-008..D-014), joint power measured, hold-out criterion restated, register.py; 32 tests. 14:55 Day-1 briefs written (C data run, G IBKR, F matrix, D engine, E referee). 15:03–15:07 all six agents killed by the 5-hour usage limit.
- 2026-11-04 18:40 UTC resumed on Itamar's "continue"; Resume rule applied (no partial contained an OOS read; registry_reads.log empty); report `reports/2026-11-04.md`; sweep resumed, engine relaunched.
