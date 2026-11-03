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
- [ ] 0.7 Draft PR "quant-edge program" opened with the Hebrew checkpoint line.
- [ ] 0.8 Red Team pre-mortem commissioned → `daily/2026-11-03/redteam-premortem.md`; answers in this log.
- [ ] 0.9 Economist F2-12 re-run commissioned → `economics/required-sharpe-2026-11.md`.
- [ ] 0.10 Scribe briefs of the inherited record → `briefs/inherited-*.md`.
- [ ] 0.11 Gate 0: everything above exists in the repository (commit hash recorded here).

### Phase 1 — the sweep (Days 1–4, 2026-11-04 → 2026-11-07)
- [ ] 1.1 Department B sweep run (Workflow) → `research/candidates.md` (≥ 100 mechanisms, ≥ 30% original).
- [ ] 1.2 Department E pre-screen (closed-family overlap, look-ahead by construction, economics screen).
- [ ] 1.3 Firm letters → `letters/<firm>.md` (FTMO, MyFundedFutures, Lucid, Topstep, TradeDay, Bulenox).
- [ ] 1.4 CAL calibration replication registered (noise-area model on ES, expected Sharpe 0.9–1.25, 2016–2024).
- [ ] 1.5 First batch (≤ 20 variants + CAL) registered; Gate 1 per row (commit before code).

### Phase 2 — data (Days 1–6, in parallel)
- [ ] 2.1 Free-Data Hunter: reachability + licence register → `data/licences.md`.
- [ ] 2.2 `load(id, window)` gateway + `registry_reads.log` + tests (planted leak, hold-out refusal, synthetic calibration).
- [ ] 2.3 Calendar and Clock Keeper: session templates, DST, rolls, firm trading-day boundaries.
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

- phase: 0 (orientation), step 0.7
- running N: 280 (inherited) + 0 (program) = 280; budget left 150; N_total 430; bar z = 3.6807 (two-count 3.8538)
- spend total: $0.00 (Databento ceiling not yet set: credit unconfirmed)
- open decision requests (date sent): Day-0 items (1)–(4) to Itamar, 2026-11-03
- next action: open the draft PR, then commission the pre-mortem, the F2-12 re-run and the Scribe briefs.

## Agents in flight

| name | brief file | output file | start (UTC) | status |
|---|---|---|---|---|

## Session log (append-only)

- 2026-11-03 14:19 UTC session start (Day 0). 14:25 Day-0 message sent. 14:27 skeleton written.
