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
- D-018 (2026-11-06) Batch 1 = 4 rows on free data (not 20): the pre-screen found only these free-data rows worth a count; twins on identical data are one decision unit and are not counted twice. The FX rows proceed on the outcome-free clock diagnostic plus a cross-source QA; CAL-I (intraday known-result calibration) remains owed and is an accepted risk until Databento or the licence ruling arrives.
- D-019 (2026-11-06) HistData clock defect found by the batch-1b ingest: HistData files follow US DST dates through 2018 and EU DST dates from 2019, so the 2026-11-04 datasets histdata_fx_1m_* are 1 hour early in the 2019–2024 US/EU mismatch weeks (2–3 weeks a year). Affected batch-1 events: Q-0001 October month-ends 2019–2024 (≤ 6 of ≈ 117), Q-0003 March FOMC statements 2019–2024 (≤ 6 of ≈ 88). Decision: no re-read (it would be a second OOS read for verdicts that cannot flip); the FAIL verdicts stand with the defect disclosed in both result files. Crude bound: even if every affected event moved by 4 per-event standard deviations in the favourable direction, t would move by ≤ 6·4/√88 ≈ 2.6, leaving Q-0003 below 3.68 (0.95 + 2.6 = 3.5) and Q-0001 far below. All later rows use the corrected `histdata_rule` datasets; the old ids stay pinned for reproducibility only.
- D-020 (2026-11-06) Low-power rows are registered when they are the best remaining free-data candidates: N_total is fixed at 430, so a count spent costs no strictness; 145 counts remain against far fewer candidates. A row with power ≈ 0 is not registered (Q-0010).
- D-021 (2026-11-06) After Q-0007 (gross ≈ 0 on SPX/NSX/JPX/UKX/FRX/GRX/ETX CFDs), C-4-01 on CME futures stays registrable (different venue and instrument set, 1-hour data) but its plausibility drops from medium to low; it is still the first Databento purchase because it costs ≈ $5 and would settle the family.
- D-025 (2026-11-08 ~20:20 UTC) Reopened for the Databento rows at Itamar's insistence ("not today we finish" → do it today). Network secret removed; DATABENTO_API_KEY set as an environment variable of 'AI Trading' (env vars load only at session start, so the Databento batch runs in a NEW child session in the same environment); credit file written ($99.37; ceiling $79.37; portal monthly limit $84 per Itamar). Tonight's purchase scope ≤ $20: C-4-01, C-2-01, C-1-01, C-2-05 data.
- D-026 (2026-11-08 ~20:25 UTC, child session) Databento rows registered before any purchase (commit 4588d6c): Q-0012 C-4-01 CME CO-OC reversal (1h), Q-0013 C-1-01 variant B on UB+ZN (both legs, so criterion 2 can be met; default OOS kept because no source measured futures returns or the overnight-session hold), Q-0014 C-2-05 Crop Progress (event file from the NASS report archive at esmis.nal.usda.gov; QuickStats API needs a key, bulk files 403), Q-0015 C-2-01 on NG 1h because NG 1m costs $17.29 as one batch (> the $8 limit) and per-day RTH windows would take ~850 streamed requests; Q-0015 OOS 2019-2024 by D-009 (paper sample probably <= 2018). N = 295.
- D-029 (2026-11-09) Q-0017..Q-0021 run: data ES/GC/MES 1m landed and sha256-pinned before any read; IS phase with truncation/perturbation harness (0 changes on 30 events each) and planted look-ahead (caught every time) before one OOS read per dataset. ALL FIVE FAIL: Q-0017 t -8.84 (gross -1.1 bp), Q-0018 t -2.05, Q-0019 t -7.31 (gross +0.2 bp on 3515 trades), Q-0020 t -1.78 (IS +4.3 bp reversed), Q-0021 t 1.14 (net +7.9 bp, 70% years positive, ES leg; real but far from the bar). Sweep2 (literature only): 14 blocks, none reaches power 0.05; summed power x prior ~0.006. Spend $60.60 cumulative. N = 301. Itamar told (2026-11-09) that x400 in 3 years needs ~637%/yr and in 10 years ~82%/yr - no honest method; that funded-firm and broker accounts need age 18; that an unbounded search would manufacture a false positive.
- D-028 (2026-11-09) Reopened at Itamar's request ("start with the six, and search hard for new ways"). Remaining Databento queue: C-12-04 margin-hike NOT registered (CME advisory archive blocked: 403 direct, 503 via fetch; no dates -> no test, precedent Q-0010); hold-out item for Q-0005/6 dropped (both failed; no count). Five rows registered before any purchase or code: Q-0017 C-1-08 ES post-close fade, Q-0018 C-12-01 prop-flatten reversal, Q-0019 C-4-04 drift-burst fade ES+GC, Q-0020 C-12-21 micro-share open-thrust fade, Q-0021 C-4-07 hedging-overshoot reversal ES+GC. Purchase plan from free quotes (research/dbn1m/quotes_1m.json): ES 1m $20.94 + GC 1m $20.77 + MES 1m $9.64 = $51.35 within the $69.12 room. A literature sweep agent (sweep2) started in parallel; literature only, no data reads.
- D-027 (2026-11-08 ~21:05 UTC) Path 1 (own capital, structure change) tested at Itamar's request: Q-0016 risk parity + 10-month trend filter, registered d0f7d39 before code, one OOS read: OOS 2010-2024 excess Sharpe 0.52 (t 2.02) vs 60/40 at equal vol 0.87; FAIL at the bar and worse than 60/40 at the own-capital standard. N = 296.
- D-024 (2026-11-08 ~20:15 UTC) PROGRAM CLOSED (final) at Itamar's instruction to finish today. Triage of all 130 remaining items done (A 1, B 0, C 10, D 119); Q-0011 tested, FAIL (t −0.52). Databento credit confirmed ($99.37) but the credential could not be connected tonight (network-secret form requires a password; env var entered in the Desktop environment); the key appeared in a screenshot in chat → Itamar told to rotate it. Verdict N1; memo `reports/decision-memo-2026-11-08.md` (final). N = 291. $0 spent. Hold-out never read.
- D-023 (2026-11-08 ~20:00 UTC) PROGRAM REOPENED at Itamar's instruction ("continue testing the 107 that remain"), superseding D-022's closure; DEADLINE_DATE back to 2026-12-19. Plan: Department E triages ALL remaining candidates (not only the top 40) by data class (free-now / free-ingest / Databento / not testable) and power; free rows with criterion-4 power at a realistic Sharpe ≥ about 0.05 are registered and run in sequential batches; Databento rows queue until the Day-0 items arrive; rows with power ≈ 0 or closed-family overlap are listed, not counted. The N1 memo stays on file as the verdict IF the program ends without a pass.
- D-022 (2026-11-08) PROGRAM CLOSED at Itamar's instruction ("today we need to finish everything", end condition (c)). Verdict N1; memo `reports/decision-memo-2026-11-08.md`. Databento never confirmed; $0 spent; hold-out never read; N final 290. Pending scheduled check-in for 2026-11-13 cancelled.
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
- [x] 1.1 Department B sweep → `research/candidates.md` (2026-11-06): 114 mechanisms + 22 layers, 55% original; 1 medium (C-4-01), 4 low-medium; thin lanes 6, 7, 10, 11. Forum scout incomplete (killed). History: run `wf_2a3bbcb1-b48` died at the usage limit 2026-11-03 15:07 UTC with 2 of 7 scouts complete (academic-flows-events 25 candidates, academic-session-momentum 20); resumed 2026-11-04 18:45 UTC with the script patched (killed scouts continue their files). Originally launched 14:34 UTC as Workflow run `wf_2a3bbcb1-b48` (script `~/.claude/projects/-home-user-claude-skills/c1c15771-3f18-56a1-8828-ab24630be4a0/workflows/scripts/quant-edge-sweep-b-wf_2a3bbcb1-b48.js`; resume with scriptPath + resumeFromRunId) → `research/sweep/*.md`, `research/candidates.md`, `research/prescreen-2026-11-03.md` (≥ 100 mechanisms, ≥ 30% original). Brief: `briefs/B-sweep-common.md`.
- [x] 1.2 Department E pre-screen done 2026-11-06 → `research/prescreen-2026-11-06.md`: of the top 40, 3 batch-1 mechanisms, 21 later (15 blocked-paid ≈ $82 for the top priorities; 6 need a free ingest), 16 rejected. Strongest objection: event sleeves cannot reach t 3.68 and daily legs are under 3× round-trip cost; only C-4-01 ($5 of Databento 1d/1h) clears both. Expected batch-1 passes ≈ 0.03.
- [x] 1.5 Batch 1 registered 2026-11-06 (D-018): Q-0001 month-end London-fix legs signed by foreign-vs-US equity MTD (EURUSD/GBPUSD/AUDUSD, FTMO intraday CFD), Q-0003 long AUDUSD on FOMC statement days (FTMO intraday CFD), Q-0005 energy two-day-fall dip buy (CL/CO/HO, FTMO Swing), Q-0006 gold two-day-fall dip buy (FTMO Swing). Q-0002/Q-0004 (futures-venue twins on the same data) withdrawn before registration; futures cost attached as no-count sensitivity. N = 285.
- (prescreen launch record:) Department E pre-screen launched 2026-11-06 00:20 UTC → `research/prescreen-2026-11-06.md` + `research/prereg/Q-*.json` (dry-run validated).
- [x] 1.3 Firm letters → `letters/{ftmo,topstep,myfundedfutures,tradeday,lucid,bulenox,accountant}.md` + `letters/README.md` (Hebrew) + `economics/firm-pages-fetched-2026-11-03.md` (94 lines of sources). Lucid unverified (blocked). Decision request sent to Itamar 2026-11-04 (`reports/2026-11-04.md`).
- [x] 1.4a CAL-D registered (a9ddfcd, count 1, N = 281) and run 2026-11-06 00:06 UTC: OOS 1990–2016 gross Sharpe 1.432 (t 6.78), inside [0.85, 1.45] → daily pipeline PASSES (a); (b) not verifiable (no inherited year table); 1.40 vs inherited 1.17 on 1985–2016, convention differences named in `research/results/CAL-D.md`. Disclosed: one crashed run logged an OOS read before any P&L (00:05:59), fixed run re-read at 00:06:13.
- [ ] 1.4b CAL-I (noise-area model on ES 1m, expected 0.9–1.25 on 2016–2024): needs Databento ES 1m or Itamar's licence ruling for the FirstRate copy as crosscheck.
- [ ] 1.5 First batch (≤ 20 variants + CAL) registered; Gate 1 per row (commit before code).

### Phase 2 — data (Days 1–6, in parallel)
- [~] 2.1 Department C data run: first launch died 2026-11-03; relaunched 2026-11-04 19:12 UTC (compute slot; brief `briefs/C-data-run.md`).
- [x] 2.2a `load(id, window)` gateway (`src/qe/gateway.py`, `registry.py`) with 10 tests (incl. licence-hold crosscheck-only) + `tests/test_no_direct_reads.py`; `tools/register.py` (Gate-1 validation: fields, split ≥ 5 OOS years unless post-change, sign/count, family cap 5, 2× cost stated, results empty, stamp commit) with 4 tests: unregistered/inherited id refused, IS/OOS slicing, every read logged, hold-out lock (file + id list), planted 2025 row never leaks. Gate statistics `src/qe/stats.py` (iid/NW/clustered t, stationary + day-cluster bootstraps at 430k draws, Mertens/Opdyke SE, Lo factor, DSR, CSCV) with 7 synthetic tests. Steward `src/qe/steward.py` (credit file gate, ceilings, 10-min alignment, estimate row before request, per-request accounting, batch-vs-stream rule) with 6 tests. 32 tests pass.
- [x] 2.2b shared engine `src/qe/engine/` (Department D, 2026-11-04): fills (stop-first ambiguity, bar-granularity stops, gap-through at open, limit on trade-through), flat-by at deadline − 2 min (half day = min(firm, early close)), 1×/2× costs on one path, truncation + perturbation harnesses, nulls, report; synthetic 16-year calibration mean R 0.012 ± 0.007 (driftless walk, 2R/1R); 52 tests. Still open: real-data loaders (Department C), FTMO swaps and crypto funding in costs, sub-minute hold share.
- [~] 2.3 Calendar and Clock Keeper: the engine agent left a 263-line `src/qe/sessions.py` stub (interface + TODO list for Department C); kept.
- [ ] 2.4 Databento Day-1 purchase (1d all roots + definition + statistics, ≈ $2) — BLOCKED on Day-0 items (a), (b), (c).
- [ ] 2.5 Databento plan file inside the ceiling, each purchase with requesting row ids.
- [x] 2.5b Batch-1b free ingest (2026-11-06): HistData 1m SPX, NSX, JPX, XAU, UKX, BCO, FRX, GRX (EU50 levels 2020-06..2023-12 excluded), HKX, ETX (to 2018-12-14), WTI (to 2023-12); IS/OOS under derived/, 2025+ under holdout/; corrected clock rule; QA PASS or PASS-with-caveats (SPX vs ^GSPC corr 0.998). 61 tests.
- [ ] 2.6 Gate 2.

### Phase 3 — testing (Days 5–20, batches)
- [x] 3.1 Batch 1 run 2026-11-06 (one OOS pass per row; reads reconciled by the Director: Q-0001 4 lines = 4 datasets in one run, Q-0003 2, Q-0005 1, Q-0006 1; no hold-out read). ALL FOUR FAIL, none a near-miss (no t within 1.0 of 3.68): Q-0001 −7.39 bp/event t −2.04; Q-0003 +9.74 bp/event t 0.95; Q-0005 −0.17 bp/day t −1.37; Q-0006 −0.44 bp/day t −2.48. Families fx-month-end-equity-hedge, fx-fomc-day-premium, commodity-dip-swing hold 1, 1, 2 counted variants; not closed (rule: closed after 3 with gross t < 1.5). Disclosed in the result files: gateway ';'-list and parquet-directory fixes before any read; Q-0001/Q-0003 skip rules failed truncation by construction, ex-ante versions no better; no FX series in daily_assets (cross-source vs CME futures in sample, corr 0.91–0.95); HistData lacks 2023-02..06 month-ends.
- [x] 1.5b Batch 1b registered 2026-11-06 (D-020): Q-0007 cross-index overnight-vs-intraday reversal on 7 index CFDs (09:32→15:55 ET, OOS 2015–24), Q-0008 HSI after-hours fade on HK50 (OOS 2016-11..2024), Q-0009 prereg_orb30 as written (A/B/C, count 3; OOS SPXUSD 2019–24 only if A's IS p5 > 0; overlap with closed D4-04 disclosed). Q-0010 ECB tone NOT registered (≈ 20 OOS events, power ≈ 0). N = 290.
- [x] 3.1b Batch 1b run 2026-11-06, ALL FAIL: Q-0007 cross-index CO-OC reversal on index CFDs −4.52 bp/day net, gross +0.01 bp/day, t −4.81 (registered bar-coverage filter reads after entry → fails truncation by construction; ex-ante version t −4.30, printed); Q-0008 HSI after-hours fade +3.64 bp/trade, t 1.09, gross t 2.14, 2×-cost t 0.05 (not a near-miss; HKEX schedule change 2016-07-22 seen in outcome-free bar profiles); Q-0009 prereg_orb30 failed its stage-1 IS test (A: net −0.120 R, p5 −0.167 R), no OOS read, family orb-30min CLOSED. Reads reconciled (one OOS pass per row; none for Q-0009; no hold-out). Implication: the CFD version of the only 'medium' candidate (C-4-01) has zero gross edge on largely the same indices; the CME version's prior is lowered accordingly (D-021).
- [x] 3.1c Databento batch run 2026-11-08 (child session, D-025/D-026): $9.25 spent (5 batch jobs, estimate = billed; the job API shows no cost; Itamar to confirm on the portal). ALL FOUR FAIL, none a near-miss; one OOS read per dataset; hold-out never read.
  - Q-0012 CME CO-OC reversal ES/NQ/YM/EMD/NKD 1h (OOS 2015-24, 2,433 days): net -4.72 bp/day, t_min -5.74, gross +1.01 bp/day (t 1.24), 2x-cost t -12.61 → FAIL. Family xs-closure-reversal now 2 counts, both gross t < 1.5.
  - Q-0013 month-end Treasury, UB+ZN overnight-session holds T-2..T (OOS 2015-24, 348 sessions): net +7.92 bp/session, t_min 1.31, gross +17.5 bp (t 2.91), 2x-cost t -0.30 → FAIL (event vs non-event Welch t 3.10 before costs: the month-end drift is visible, not certifiable).
  - Q-0014 Crop Progress → ZC/ZS 20:00 reopen to 13:00 (OOS 2015-24, 167 weeks): net -10.73 bp/week, t_min -1.58, gross +3.2 bp (t 0.43), 2x-cost t -3.64 → FAIL.
  - Q-0015 NG storage day, Wed 18:00 → Thu 15:00 ET (OOS 2019-24, 241 events): net -9.84 bp/event, t_min -2.53, gross -8.0 bp (t -2.07), 2x-cost t -2.99 → FAIL.
- [ ] 3.2 Referee formal verdict files: not needed for clear FAILs far from the bar (Director reconciliation above); required for any PASS or near-miss.
- [ ] 3.2 Referee Gate 3 verdicts; near-miss list with power at S = 1.5 / 2.0 / 2.4.
- [ ] 3.3 Batch 2+ (≤ 25) after verdicts and a lessons note.

### Phase 4 — verification (rolling)
- [ ] 4.1 Re-implementer, Leak Hunter, Red Team, Null-Model Builder, Multiple-Testing Auditor per Gate-3 pass.

### Phase 5 — economics and compliance (rolling, after E's PASS)
- [ ] 5.1 Criterion 11, stressed $/slot-year per firm, compliance matrix, scaling plan.

### Phase 6 — paper trading (≥ 3 weeks or ≥ 60 trades)
- [ ] 6.1 Real order path in simulation; tolerance written before the first fill.

### Phase 7 — decision memo (by 2026-12-19)
- [x] 7.1 N1 decision memo 2026-11-08 → `reports/decision-memo-2026-11-08.md` (Hebrew + English appendix).

### Standing (every day)
- [x] G.1 IBKR connectivity diagnosis (2026-11-06): `engineering/ibkr-connectivity-diagnosis.md` (Hebrew guide + English appendix), `engineering/ibkr_watchdog.py` (read-only logger, selftest 26/26), `engineering/bot-patch-plan.md`. No IBKR reset window falls 12:00–20:00 Israel; leading hypotheses: a second login on the same username, the bot's own 09:20 ET start (clientId clash / second instance), Gateway auto-restart set in the wrong time zone; the 32-minute lag most likely comes from yfinance, not IBKR. IBKR pages 403 from here: reset/re-login facts are search snippets. Next: Itamar runs the watchdog for five sessions.
- [ ] Rules Keeper monthly re-fetch; first fetch Day 1 → `economics/firms-matrix-2026-11.md`.

## Checkpoint

- phase: CLOSED (final) 2026-11-08 ~20:50 UTC, verdict N1 (D-024..D-026); Databento batch done in a child session
- running N: 301 (Q-0012..Q-0021, all FAIL); bar z = 3.6807
- spend total: $9.25 Databento (5 batch jobs 2026-11-08, ledger rows; credit $99.37; plan ceiling $79.37; $70.12 room left)
- to resume later: new cloud session with DATABENTO_API_KEY=<new key> as an environment variable of THAT environment, then "continue from where you stopped" → start from `research/triage-2026-11-08.md` class C queue (C-4-01 $5, C-2-01 $7, C-1-01 $2, C-12-04 $28, C-2-05 $2)
- next action: none

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
- 2026-11-08 20:22-21:05 UTC child session (D-025): key verified (free metadata call), Q-0012..15 registered and stamped (4588d6c), 5 Databento batch jobs ($9.25 est), 10 roots ingested (IS/OOS to derived/, 2025+ to holdout/), NASS event file built from 527 report texts, QA, harnesses, one OOS read per dataset, 4 FAIL verdicts.
