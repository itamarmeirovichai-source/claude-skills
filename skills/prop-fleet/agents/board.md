# Board — shared state of the organization

*Every agent reads this first. The director rewrites it at the end of each day.*

## Where we stand (4 Oct 2026, end of day 1)

- **Edge:** none that passes the gate. Today's only test, last-half-hour
  momentum (Gao, Han, Li & Zhou 2018; 3 variants on SPXUSD 1m 2010–2018),
  failed every gate criterion. Net mean R was -0.142 / -0.161 / -0.069, every
  bootstrap p5 was below zero, and gross was +0.07R in 2010–14 and -0.02R in
  2015–18 (`daily/2026-10-04/run.txt`, re-run by all 3 referees). Family closed.
  Earlier state unchanged: TJR/ICT has zero gross edge (`references/tjr.md`).
  Trend-following has Sharpe ~1 but is not a prop strategy
  (`references/trend-following.md`). Beat-the-Market momentum shows Sharpe ≈ 0
  since 2025 (`references/second-opinion-audit.md`).
- **Ledger:** N = 173 after tonight's rows (it was 110). +3 today's test,
  +33 tested variants in `references/` that were never logged (statistician
  audit: trend futures 6, trend ETF 16, stack 10, TJR slice 1), +26 for the
  external Beat-the-Market 27-variant grid (gate rule 3 says "by anyone"),
  +1 for the gap fade pre-registered tonight.
- **Gate rule 3, operating definition from today (director's decision):**
  one-sided Bonferroni. The day-level bootstrap lower bound of net mean R at
  alpha = 0.05/N must be above zero on out-of-sample data. At N = 173,
  z = 3.44, so a test with n trades needs a per-trade net Sharpe of at least
  about 3.44/√n. This is not yet in code: `scripts/gate.py` does not read
  the ledger.
- **Gate rule 4 (Sharpe ~3) stays in force** until Itamar changes ORG.md. The
  red team showed it comes from Apex's 21-day clock: with a 252-day horizon,
  the same synthetic test passes Sharpe 2 at 81% (`redteam/sharpe_horizon.txt`).
  The proposal is to restate rule 4 per firm, as R per trade together with
  trades per day. Rule 3 already requires an out-of-sample t-stat of about
  3.4, so restating rule 4 lowers no bar for calling an edge.
- **One unit from now on:** report R per trade together with trades per day.
  At 2:1 reward-to-risk, +0.25R is Sharpe 2.67 at 250 trades/yr and 4.63 at
  750 (red team). The board's old "+0.25R ≈ Sharpe ~3" was loose.
- **Firms (all from search snippets; no firm page could be fetched):**
  - **Tier A, the planning fleet:** Bulenox 5 + Lucid 5 = 10 accounts. Both
    FAQ snippets allow bots and copiers on funded accounts. Not confirmed in
    writing.
  - **Tier B:** Topstep Express 5, via the ProjectX API on Itamar's own
    computer (no VPS). The API stops at Live Funded, so these accounts age out.
  - **On hold:** MyFundedFutures (third parties say semi-automated only, with
    a human watching) and Tradeify (forbids running the same bot at other
    firms).
  - **Out:** Apex. Its own compliance-page snippet bans automation on all
    account types, evaluations included. ORG.md understates this.
- **Economics (`prop_head/tiers.txt`, fleet_model.py; conditional on an edge
  we do not have):** Tier A nets $19,477 / $76,476 / $133,799 a year after
  25% tax at +0.10 / +0.25 / +0.40R. That is 3.9% / 15.3% / 26.8% of $500K
  nominal. Every tier first reaches 20% at about +0.32R per trade, under the
  model's 3 trades/day and 2:1. That equals Sharpe 3.40 at 1 trade/day and
  5.88 at 3/day. Many inputs are ASSUMED (`economist_run.py`).
- **Data available here:**
  - S&P minute 2010–2018 (FutureSharks).
  - New today: SPY 1m RTH 2019-01-02..2025-07-18 (dividend back-adjusted),
    NQ 1m front month 2020-08-31..2025-11-21 (no roll adjustment), NQ 5m
    Databento 2023–2026-05, QQQ 1m 2024-08..2026-08, and ES 1m only for
    2026-01-20..04-15 and 2026-04-01..09-02.
  - All of the new files come from third-party GitHub uploads, pinned to a
    commit and checked by sha256 via `daily/2026-10-04/data_fetch.py`. The
    full files sit in scratch only, so re-fetch them.
  - Gaps: no free ES 2019–2025, and nothing for S&P 2025-07-19..2026-01-19.
  - Vendor and paper hosts are blocked.
- **Engineering:** 470 tests pass. Seven scripts and finalize.py have no
  tests. Routes: Rithmic (async-rithmic) for Tier A, ProjectX (project-x-py,
  needs Python ≥3.12) for Topstep. Tradovate is not a route. No live adapter
  is built before a strategy passes the gate.

## Decisions today

1. Tomorrow's only N-spending test is the **overnight-gap fade**, ledger row
   pre-registered tonight. It runs exactly as written in
   `daily/2026-10-04/prereg_gapfade_draft.txt`, with one variant. D2 (SPY
   2019–2025) is the primary out-of-sample set. The decision rule is fixed,
   and no retuning is allowed. The prior is weak: the paper's significance
   fell sharply after costs.
2. **Closed or not spending N:**
   - Closed: last-half-hour momentum, and any ES signal held under an hour
     with a stop under 10 pt (cost alone is 0.08–0.17R).
   - Covered externally, not tested: the pre-FOMC drift (disappeared after
     2015, Kurov et al. 2021) and the 5-minute ORB (independent replication
     net ≈ 0). Both rest on single-source search summaries.
3. **Queued, not spending N:**
   - Turn-of-the-month: cheap on `data/spx_open_close.csv`, but it holds
     overnight. It waits until each firm's overnight-holding rule is known.
   - FOMC even weeks: no FOMC date list for 1994–2026 is reachable.
4. **Process:** from now on a test is pre-registered as a ledger row the
   evening before it runs. Workers cannot write the ledger, and today's
   builder ran with the rules only in a docstring, which failed gate
   criterion 1.

## Charter corrections

Applied end of day 1 (Itamar delegated every change except the two
unchangeable rules): Apex out on all account types; Tier A = 10 accounts;
rule 3 names one-sided Bonferroni at 0.05/N; rule 4 restated per firm in R
and trades per day. H0012 (gap fade) is pre-registered and already counted in
N; tomorrow's run fills its result into that row, not a new one.

## Open questions

1. Does the gap fade survive costs out-of-sample on SPY 2019–2025 at alpha =
   0.05/173?
2. Do Bulenox and Lucid confirm in writing that a fully unattended,
   self-built bot may run on funded and live accounts, the same one at other
   firms too? Only Itamar can ask.
3. What does each firm require for overnight holding and the flat-by time?
   This decides whether turn-of-the-month and the overnight sleeve are even
   eligible.
4. What are the eval clock and VPS rule at Bulenox and Lucid? Neither was
   found today.
5. How large is the SPY-to-ES gap basis on the 2026 overlap windows?
6. Is there free S&P 1m data for 2025-07-19..2026-01-19?

## Tomorrow, by division

- **Edge research**
  - Builder: implement the gap fade exactly as pre-registered on D1/D2/D3.
    Report:
    - n and trades/yr
    - gross and net mean R
    - day-level bootstrap p5 and the lower bound at 0.05/N
    - net R by year
    Add a look-ahead perturbation test. Change nothing after seeing a number.
  - Data hunter: move `data_fetch.py` into a tested `scripts/` loader on one
    New York time index, with adjustment and roll flags. Measure the SPY-vs-ES
    gap basis on the 2026 windows.
  - Literature scout: look only for intraday, flat-by-close effects with
    post-2010 evidence and code on GitHub raw. No more calendar or overnight
    effects.
- **Prop structure**
  - Rules keeper: add an overnight-holding / flat-by row per firm. Find the
    eval clock and VPS rule for Bulenox and Lucid. Draft, and do not send,
    one written automation question per firm for Itamar.
  - Economist:
    - Re-solve the R needed at 1 trade/day.
    - Size every firm at equal dollar risk.
    - Model Topstep leaving at Live Funded.
    - Add per-account costs (data, platform, own computer).
    - Check whether `keep_off` is used on the frac=1.0 path.
- **Statistics & risk**
  - Statistician: specify the ledger-aware Bonferroni check for `gate.py`
    with the engineer. Re-run the overnight sleeve without stale-open days,
    or from 2014, with p5.
  - Red team: attack the gap-fade result the moment it exists (data
    adjustment, 09:31 fill realism, roll weeks on NQ).
- **Engineering & operations**
  - Engineer:
    - Add gate rule 3 to `scripts/gate.py`, with tests.
    - Harden `finalize.py`: reject a count that is not an integer ≥1, and add
      an OOS flag.
    - Add a day-clustered bootstrap to `tjr_backtest.boot_mean`.
    - Add tests for `hypotheses.py` and `fleet_model.py`.
    - Adapters wait until the bot repository is attached, then go in as a
      PR, never a push.
