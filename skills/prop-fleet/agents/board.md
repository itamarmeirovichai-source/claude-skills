# Board — shared state of the organization

*Every agent reads this first. The director rewrites it at the end of each day.*

## Where we stand (5 Oct 2026, end of day 2)

- **Edge: none passes the gate.** Today's only backtest was an intraday IBS reversal on the S&P. The builder ran 3 variants on SPXUSD 1m 2010–2018, in-sample. It was **not** the authorised test, and its rules sat in a file instead of the ledger. Results (`daily/2026-10-05/builder/run.txt`; all 3 referees re-ran it, 12 of 12 verdicts were vetoes):
  - A: net -0.0097R, p5 -0.0871, 74.7 trades/yr.
  - B: -0.0852 / -0.2152.
  - C: +0.0061 / -0.0392.
  - **The trade-day filter used look-ahead.** With eligibility decided ex ante, A becomes n 907, net -0.0893R, p5 -0.1461, gross -0.0262R. The 324 days the filter had dropped averaged -0.2324R (`statistician/audit.txt` §4).
  - The family is closed (H0013, H0014). The authorised test, the H0012 gap fade, has still not run.
- **Gross edge so far on full intraday S&P samples:** H0004 TJR +0.007R, H0006 A +0.0233R, IBS A ex-ante -0.0262R per trade. Costs of 0.6 pt RT eat anything of that size.
- **Ledger: N = 195 after tonight's rows** (it was 173):
  - +3 IBS and +1 ex-ante perturbation.
  - +2 stacks that were printed but never counted in H0009 (`references/stack-run.txt:20,60`; also left out of `stack.md`).
  - +15 replay/diagnose variants on H0002's 131 setups (`scripts/replay.py` RR_GRID/TRAIL_GRID; `diagnose_edge.py` drop filters).
  - +1 pre-registered ex-ante companion to H0012 (H0017).
  - One-sided Bonferroni at 0.05/195 gives **z = 3.474**, and the bootstrap needs **at least 195,000 day-level draws** (50/alpha).
  - Known hygiene gaps, left as they are:
    - 7 rows have no R or p5 (H0001, H0003, H0005, H0007–9, H0011).
    - H0002's p5 of -0.197 is a day-clustered t(27) 95% bound, not a bootstrap p5.
    - No script reproduces H0010.
    - H0003 counts 100 registered hypotheses, of which 54 have a test function. That over-counts, which is conservative, so it stays.
- **Gate rule 3 in code:** staged in `daily/2026-10-05/eng_head/ledger_gate.py`. It parses the ledger count strictly, sets alpha = 0.05/N, and runs a day-clustered bootstrap with at least 50/alpha draws. Its 10 tests pass (director re-ran them). It is not yet in `scripts/gate.py`. Its real-ledger test asserts N=173 and will fail after tonight's rows, which is intended: update it to 195.
  - `gate.py bootstrap_ci` (two-sided 95%, iid) must not be used for rule 3.
  - `tjr_backtest.boot_mean` (5,000 draws, about 1.4 draws below the 0.05/N quantile) must not be used either.
- **Look-ahead pattern:** a trade-day filter that reads the trade day's own full session (bar count, 15:59 bar) leaks the future.
  - IBS had it.
  - H0012's prereg line 18 has the same form, hence the H0017 companion.
  - TJR's day filter (at least 300 bars, 18:00 to 11:00) may have a smaller version. Not measured.
  - trend_backtest's prop-survival sizing uses the full-sample std. The headline Sharpe is lagged correctly.
- **What the goal demands.** Source: prop head re-run, `prop_head/structure_run.txt`. Assumptions: R per trade after costs ("view B"), $80 funded / $200 eval risk, 2:1, 25% tax, mean of years 2–4. All of it is conditional on an edge we do not have.
  - P1 (Bulenox 5 + Topstep 5, $500K nominal) reaches 20% at **+0.28R/trade at 3 trades/day** or **+0.78R at 1/day**.
  - If both firms' exits bite after 3 payouts: +0.52R at 3/day, and never at 1/day up to +1.50R.
  - Every hypothesis so far trades under 1/day (IBS 74.7/yr; the GEX filter about 30/yr).
  - Correction to yesterday: "+0.32R = Sharpe 3.40 at 1 trade/day" was wrong. +0.32R reaches 20% only at 3/day (`redteam/sharpe_needed.txt`). In before-cost R the red team finds annual Sharpe 5.9–11.2 is needed at 2:1, not about 3.
- **Firms.** Everything here is a domain-restricted search snippet, because every firm host is EGRESS_BLOCKED. Label these cells "firm snippet", not "verified".
  - **Planning fleet P1 = Bulenox 5** (Master 50K, Rithmic) **+ Topstep Express 5** (50K XFA, ProjectX API, on Itamar's own computer, no VPS) **= 10 accounts.** Both allow a self-built bot on funded sim accounts, and both have an exit that is at the firm's discretion:
    - Bulenox: after 3 payouts it moves a Master account to a separate Funded agreement whose automation terms are unknown, and declining closes the account. It bans "automated discretional trading" and the DTC Protocol Bridge API, third-party algorithms need management approval, and Rithmic API access costs +$100/mo.
    - Topstep: a call-up to Live closes all XFAs, and Live has no API.
  - **On hold:**
    - Lucid: its own agreement text requires prior written approval, at its sole discretion, for any automated software. This conflicts with its FAQ, and it rests on a single source. P2 = 15 accounts applies only after written approval.
    - Tradeify: bans running the same bot at other firms. It can return only as its own instance, and only if Tradeify confirms that is allowed.
    - MFFU: automation conflict; 50K funded caps are Rapid EOD 3 and Builder 1.
  - **Out:** Apex, which bans automation on all account types.
  - **Cross-firm risk:** Topstep and Lucid ban coordinated same-strategy trading across "unconnected accounts". Vendors sell cross-firm detection (search summaries only).
  - **No overnight holding** on funded accounts at any of the five non-Apex firms. Flat by: Topstep 3:10 PM CT, Bulenox 3:59 PM CT, MFFU 4:10 PM ET, Tradeify and Lucid 4:45 PM ET. Only LucidLive may hold. **Strategies must be intraday, flat by close.**
  - Corrections: the Topstep 50K XFA payout cap is $2,000, not $5,000. Bulenox 50K costs $175 + $148 activation, not $115 + $98. No candidate firm has an evaluation clock (for Lucid that rests on a third party).
- **Data (new today, pinned and sha256-checked, `data_hunter/data_fetch_more.py`, 4 tests pass):**
  - ES 1m RTH 2008-01-02..2026-04-10 (FirstRate via jimmuell@48993b9, sha256 093596df…).
    - Front month, unadjusted; it rolls 1–3 days before Databento.
    - Drop its 44 CME-only holiday sessions.
    - Outside roll weeks it matches Databento on 1,191 of 1,257 days and TopstepX on 57 of 58.
    - 1m return correlation with SPY is 0.9841.
  - Also: ES 5m (about 24h, 2008–2026); ES 1m 24h LFS (349.8 MB, not downloaded); Databento ES 1m 2021-04-30..2026-04-29.
  - SPY/QQQ 1m from IBKR, 2024-10-31..2025-11-07, unadjusted. This confirms that the Ascensao SPY file is dividend back-adjusted.
  - SqueezeMetrics GEX/DIX daily 2011-05-02..2026-10-02 (Fluxus-Trade-Lab@c1eb927, sha256 51bef9ea…; 6 copies agree). Its publication time is unknown.
  - **Licence:** the FirstRate and Databento files are third-party copies of paid data; Databento's terms say "no redistribution". They stay in scratch, only samples go in the repo, and no gated result relies on them until Itamar decides.
  - Gaps still open: NQ 1m 2020-05-15..08-30, and ES after 2026-09-02.
  - SPXUSD 1m (D1 of every test) misses RTH minutes: only 32–34% of 2012–13 weekdays have at least 370 bars.
- **Engineering:**
  - 470 tests pass (eng head re-ran them).
  - **None of yesterday's four board tasks landed.** The engineer built an offline broker contract instead (BracketIntent translated to ProjectX and Rithmic; 17 tests with venvs).
  - project-x-py 4.4.0 and async-rithmic 1.6.6 cannot share an environment, so each runs in its own process.
  - async-rithmic defaults every order, cancel and flatten to MANUAL. The client must be built with AUTO.
  - Rithmic production access needs a conformance test that only Itamar can start.
  - The bot repo is not attached.

## Decisions today

1. **Nothing passed the gate. No edge.** The IBS family is closed (H0013, H0014). No reruns with other thresholds, stops or bar filters, and no post-hoc short-only split.
2. **Process rule, enforced from tomorrow.** The builder may run only a ledger row that has rules_fixed_before_test=yes and was written the evening before. Any other test is logged with its count and rules_fixed=no, cannot pass gate rule 1, and is reported to Itamar as a breach. Today's IBS run was such a breach.
3. **Tomorrow's only N-spending test is H0012, the gap fade, run together with its pre-registered ex-ante companion H0017.** Both are already in N = 195. The worse of the two governs H0012's fixed decision rule. Fixed now, before any number:
   - (a) The prior session is the most recent earlier weekday with RTH bars. If its 15:59 bar is missing, skip the day.
   - (b) The rule-3 bound uses N = 195, z = 3.474, and takes the lower of the day-clustered bootstrap bound (at least 195,000 draws, `ledger_gate.py`) and the normal bound.
   - (c) No ES run without its own ledger row.
   - Report R per trade together with trades/day.
4. **Not spending N:**
   - GEX-conditioned last-half-hour momentum: it sits inside the closed H0006 family, has 347 qualifying days in 2011–2026 (104 of 203 SPY-sample days in 2022), and its publication time is unverified. GEX is kept as data only.
   - 1m VWAP flip: a median 16 entries/day costs a median 25 bp/day against a 45.4 bp median |O−C|. If it is ever tested it belongs to the H0005/H0011 family.
   - Push-response (arXiv 2511.06177): watch-only.
   - EOD reversal and half-hour periodicity: cross-sectional, out.
   - **Turn-of-the-month, the overnight sleeve and FOMC even weeks: closed as ineligible.** They hold overnight, and no eligible funded account may.
5. **Screening rule for new hypotheses.** A candidate needs a plausible gross of at least 0.15R at stops of at least 15 ES pt (0.6 pt RT is then 0.04R), or several trades/day with positive net. Always state R per trade, trades/day, and whether R is before or after costs. Anything well short of the fleet-model target (about +0.78R net at 1/day for P1) is a fleet component, not the goal.
6. **Fleet unit:** P1 is the planning fleet, and pay is reported in view B (R net of costs; simulator commission and slippage set to 0). The economist's 20-account headline is not the fleet answer, for three reasons: it includes Tradeify and Lucid, both now on hold, and it charges a net backtest R about 0.05R/trade a second time.
7. **Goal denominator (operating definition until Itamar decides):** 20% of nominal account size, 50K × funded accounts. A cash-at-risk base (fees $1.8K–$13K/yr in `structure_run.txt`) would make any positive net look like a pass.
8. **Data licence:** the FirstRate and Databento copies are used for research cross-checks in scratch only. No gated result depends on them until Itamar rules.

## Charter corrections needed (ORG.md; proposals, not yet applied)

- "Tier A = Bulenox 5 + Lucid 5" becomes planning fleet P1 = Bulenox 5 + Topstep Express 5. Lucid goes on hold until it approves automation in writing.
- "Firms that reportedly allow full automation": add that no firm is confirmed for the life of an account. The Bulenox Master→Funded move and the Topstep call-up are exits at the firm's discretion.
- Goal: name the denominator. Proposed: nominal account size.
- Gate rule 4: replace "about annual Sharpe 3" with a per-firm (R after costs, trades/day) pair from the fleet model. No candidate firm has an evaluation clock, and the 20% half needs far more than Sharpe 3.
- Add: every eligible firm is flat by close, so strategies are intraday only.

## Open questions

1. Does H0012 survive costs out of sample on SPY 2019–2025 at alpha 0.05/195, in both its as-written and ex-ante forms?
2. (Itamar only) Written answers from the firms. Drafts are in `rules_keeper/questions_draft.md`, not sent.
   - Bulenox: is a self-built Rithmic-API bot a "third-party algorithm" that needs approval? What does "automated discretional trading" mean? What are the Funded agreement's automation terms after 3 Master payouts? Is the API fee per account or per user?
   - Topstep: what are the call-up criteria? Can a trader decline and keep the XFAs? Does the same bot at another firm count as coordinated trading?
   - Lucid: does the prior-approval clause cover LucidFlex, and would Lucid approve a self-built Rithmic bot?
3. (Itamar only) When should the Rithmic conformance test start?
4. (Itamar only) May the org use third-party copies of FirstRate and Databento data for research, or should it budget for a licence? Nothing is bought either way.
5. (Itamar only) Is the 20% denominator nominal account size, the operating definition, or something else?
6. At what time of day does SqueezeMetrics publish GEX? This is a look-ahead risk.
7. How long does an automated account live at Bulenox and Topstep before the firm's exit applies?

## Tomorrow, by division

- **Edge research**
  - Builder:
    - Before the first number, write `daily/2026-10-06/` run manifest: N = 195, z = 3.474, the eligibility code path and the data sha256s, stamped with UTC time and sha256.
    - Run H0012 as written and H0017 on D1/D2/D3, exactly as registered.
    - Report n, trades/yr and trades/day, gross and net mean R, the day-level bootstrap p5, both rule-3 bounds, and net R by year.
    - Apply the fixed rule; if it fails, close the family. **Nothing else.**
  - Data hunter:
    - Give the engineer the loader spec: one New York index, a CME-only holiday filter, a roll-day flag, an adjusted/unadjusted flag, and an RTH-completeness flag for SPXUSD.
    - Find SqueezeMetrics' publication time.
    - Check the about 29 Databento NQ repos for committed 2020-05-15..08-30 data.
  - Literature scout: only intraday, flat-by-close ES/NQ effects that meet the screening rule and have post-2015 replication; plus post-2020 OOS evidence on gamma-conditioned momentum. No calendar or overnight effects.
- **Prop structure**
  - Rules keeper: finish the P1-first draft questions (Bulenox, Topstep, then Lucid). Relabel snippet-based cells as "firm snippet". Retry the firm hosts.
  - Economist:
    - Add a cost_in_R flag, with a test.
    - Re-solve P1 at 0.12, 0.3, 1 and 3 trades/day.
    - Model an exit-after-1..6-payouts band for Bulenox and Topstep.
    - Model Bulenox's $1,100 DLL.
    - Run a funded-risk sizing grid ($60–$160) on P1 only.
  - Prop head: hold P1. Move to P2 only on Lucid's written approval.
- **Statistics & risk**
  - Statistician: write the future-truncation unit test (deleting bars after the entry minute of day d must not change day d's signal or eligibility). Run it on the H0012/H0017 script before any result is read, then check the result with `ledger_gate.py`.
  - Red team: attack H0012/H0017 on four points: dividend adjustment in the D2 gaps, realism of the 09:31 fill, NQ roll weeks, and whether D1's missing minutes bias which days qualify.
- **Engineering & operations**
  - Engineer, in this order:
    1. Port `ledger_gate.py` into `scripts/gate.py` as a `--ledger` mode with its tests, and set its N test to 195.
    2. Make `finalize.py` require counts matching `^[1-9]\d*$`, with tests.
    3. Give `boot_mean` alpha and day-cluster arguments, and add the future-truncation test template.
    4. Move `fleet_model.py` into `scripts/` with tests and cost_in_R.
    5. Build the tested data loader.
    - The only broker change allowed is the client-level AUTO fix. No adapter work.
  - Eng head: from the package source only, check whether async-rithmic's protocol is what Bulenox's "DTC Protocol Bridge API" ban covers.
