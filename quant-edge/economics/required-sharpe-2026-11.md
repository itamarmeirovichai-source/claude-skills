# Required net Sharpe for $20k / $30k per slot-year — F2-12 re-run (2026-11-03)

Status: **in progress** (written early, extended as the run proceeds). Economist, Department F.
This is an economics-model re-run: it reads no market data and adds nothing to N (N stays 280 inherited + 0 program).

## 0. Scope and provenance

- Brief: `quant-edge/briefs/F-economist-f2-12.md` (after `quant-edge/briefs/00-common.md`).
- Inherited model (read-only worktree, commit e0f5e59 of `claude/friendly-galileo-eakzlm`):
  `~/quant-edge-inherited/pr4/skills/prop-fleet/agents/daily/w3-volrisk/` (`stress_model.py`, `scenarios.py`, `run_f2.py`,
  `make_report.py`, `test_stress_model.py`, logs `run_f2.log`, `run_f2_full.log`, `tables.md`, `redteam-model.md`), which imports
  the D1 model `~/quant-edge-inherited/pr4/skills/prop-fleet/agents/daily/w1-prop/` (`prop_model.py`, `firms.py`).
- Registered specifications: `~/quant-edge-inherited/pr4/skills/prop-fleet/agents/prereg/F2.csv` rows F2-09, F2-12, F2-13, F2-14, F2-15
  (also rows 84–98 of `quant-edge/registry.csv`). Synthesis: `~/quant-edge-inherited/pr4/skills/prop-fleet/references/w3-volrisk.md`.
- Scratch copy used for every run (the worktree was never edited):
  `/tmp/claude-0/-home-user-claude-skills/c1c15771-3f18-56a1-8828-ab24630be4a0/scratchpad/f2_rerun/`.
- Code and logs delivered under `quant-edge/economics/f2_rerun/` (no data files, nothing over 1 MB).

## 1. Summary (filled at the end)

_pending_

## 2. What the inherited record says (labelled "inherited")

- `w3-volrisk.md` verdict (from F2-09, ALL stresses, FTMO Swing 100K two-step, pre-tax net $/slot-year, renewal reward):
  net Sharpe ≈ 2.4 at 12% annual vol, ≈ 1.9 at 15%, ≈ 1.5 at 20% for $20k per slot-year.
- `tables.md` "Sharpe needed for $20k per slot-year (pre-tax)", FTMO: F2-01 (D1 baseline) 2.42 / 1.88 / 1.42 / 0.96 / 0.69 and
  F2-09 (ALL combined) 2.42 / 1.92 / 1.46 / 0.94 / 0.69 at caps 12 / 15 / 20 / 30 / 40%.
- F2-12 (the row that "REPLACES F2-09 as the decision row") and F2-13 were run (`run_f2_full.log` lists all 45 + 45 jobs done), but
  their numbers were **never written into the record**: `make_report.py` tabulates only F2-01 and F2-09, and `results.json` is
  git-ignored in that folder. So there is no inherited F2-12 figure to put beside the re-run; the inherited column below is F2-09
  (and F2-01 for reference).
- Search of both inherited trees for written F2-12/F2-13 results (`grep -rn "F2-1[2-5]"` over pr4 and pr26, 2026-11-03): none.
  The only statements are the registrations themselves (`F2.csv`, `ledger.csv`), the digest note that F2-12 was registered to
  replace F2-09 (`pr26/prompts/research/digest-hypotheses-ledger.md` line 162), and the master prompt (line 54): "F2-12, registered
  to replace F2-09, found that the closed-balance lag costs 35–50% of funded pay at 20% vol, so treat 1.5 as a floor until the
  Day-0 re-run". That 35–50% figure is in fact red-team experiment e5 (`redteam-model.md` §1, n = 300, F2-07 rules), not an F2-12
  output, and it motivated F2-13 (daily realisation at a Sharpe cost of 0.47). So "1.5 is a floor" was a reading of the red team,
  and this re-run is the first time F2-12/F2-13 numbers are written down.
- Inherited F2-09 context the re-run must be read against (`tables.md`, FTMO, S = 1.0): net $/slot-year 7.5k / 9.9k / 13.6k /
  21.2k / 26.6k at caps 12 / 15 / 20 / 30 / 40%; fixed-vol diagnostics at S = 1.0: pass 79 / 73 / 67%, breach before the first
  payout 3 / 4 / 9%, funded life 493 / 399 / 248 days at 12 / 15 / 20% vol; F2-11 lottery: S = 0 at the 12% cap pays $1.2k a
  year with an 84% chance of a losing first year.

## 3. Tests run first

Scratch copy: `cp` of the w3-volrisk and w1-prop folders (scripts, logs, tables, `rules.csv`; the git-ignored `results.json` of
w3-volrisk does not exist in the worktree, and w1-prop's 134 KB `results.json` was not copied). Layout kept (`w3-volrisk/` next to
`w1-prop/`) because `stress_model.py` imports `prop_model` from `../w1-prop`. Nothing in `~/quant-edge-inherited` was edited.

- `python3 -m pytest -q test_stress_model.py` in `w3-volrisk/`: **21 passed in 8.39 s** (log `f2_rerun/logs/pytest_w3.log`).
  `test_no_stress_reproduces_d1_eval_and_funded` and `test_new_switches_off_still_match_d1` pass, so the copy reproduces D1 bit for
  bit with every stress switch off.
- `python3 -m pytest -q test_prop_model.py` in `w1-prop/`: **14 passed in 0.25 s** (log `f2_rerun/logs/pytest_w1.log`).
- Environment: Python 3.13.18, numpy 2.5.3, scipy 1.18.1, numba 0.68.1, 4 CPUs.

## 4. Runtime budget

`run_f2.log` and `run_f2_full.log` carry no timings, only "done" lines (the inherited run was finished in a director session after
the F2 session stopped mid-run). One F2-12 job (FTMO, S = 1.0, n = 3000, 24 checks a day, 756-day horizon) was timed in the
scratch copy (`time_job.py`, log `logs/time_job.log`): sigma grid restricted to ≤ 20% (11 of D1's 14 sigmas) eval 20.5 s + funded
20.7 s = **41 s CPU**; full grid 26.2 + 26.4 = **53 s CPU**. The inherited F2-01..15 programme is about 268 grid jobs and 144
calendar-chain jobs, roughly 3 CPU-hours on this machine, far above the brief's ≈ 60 CPU-minutes, so the re-run was shrunk as
follows (nothing else changed in the model):

- FTMO Swing 2-Step 100K only (the brief's firm); Blue Guardian and CFT not re-run.
- Sigma grid ≤ 20% (1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20%). The capped optimum at caps 12 / 15 / 20% only reads cells with both
  sigmas ≤ cap, so this changes the random stream (the arrays have 11 rows instead of 14) but not the estimand. The seed-to-seed s.e.
  reported below covers that stream difference.
- S grid {1.0, 1.5, 2.0, 2.4, 3.0} as the brief asks (the inherited grid was 0 … 3.5 in steps of 0.25), with five seed pairs each
  (F2's base pair eval 11 / funded 12 and F2-15's 101/102, 202/203, 303/304, 404/405): 2 scenarios × 5 S × 5 seeds = 50 jobs ≈ 34
  CPU-minutes. S = 3.5 and 4.0 at the base seed only (to bracket the $30k crossing at 12% vol; 4 jobs). One F2-09 job at S = 1.0 on
  the full grid as a replication check against the inherited `tables.md` (53 s). Calendar chains (inherited `slot_years`, 2000
  slots × 3 years) for every (scenario, S, cap) at the base seed's sigma pair (42 small jobs).
- n = 3000 paths per sigma kept as registered.

The achieved CPU totals are in §12.

## 5. Re-run F2-12 and F2-13, FTMO Swing 100K two-step, caps 12 / 15 / 20%, S in {1.0, 1.5, 2.0, 2.4, 3.0}

_pending_

## 6. Required net Sharpe table ("re-run 2026-11-03" beside "inherited")

_pending_

## 7. Calendar chain: p10 / p90 per slot-year, time to first payout, accounts burned

_pending_

## 8. Futures-firm frame, first pass (D1 `prop_model.py`, all firm parameters "inherited (fetched 2026-10-11)")

Script: `f2_rerun/futures_frame.py` (log `logs/futures_frame.log`, output `futures_frame.json`), running the unmodified inherited
`w1-prop/prop_model.py` + `firms.py`. Every firm parameter below is **inherited (fetched 2026-10-11)**; nothing was re-fetched.
Two frames, because the inherited model has two:

- **Frame A, trade level** (`simulate`, the Apex-era model that produced the inherited "+0.250R per trade at 3 trades a day"):
  1:2 reward/risk, a trailing drawdown that locks at start + $100, a 30-day evaluation clock, Apex's payout ladder and 50%
  consistency rule, MES contracts at $1.30 round trip plus 0.25 pt slippage on stopped exits, 20 copy-traded slots onboarded one a
  month, evaluation sized at 10% of the drawdown and the funded account at 4% (the inherited recommendation). Plans: **50K-2026**
  ($2,000 drawdown, the size Topstep / MyFundedFutures / Lucid 50K use, so the closest inherited stand-in for those plans),
  **150K** ($5,000) and legacy **50K** ($2,500, to reproduce the inherited +0.250R). Grid: R per trade 0.05 … 1.00 in steps of
  0.05 × trades per day {1, 2, 3, 5}; steady state = years 3–5 of a 5-year run (all 20 slots are on after month 20); n = 400 fleet
  paths (perfectly correlated slots, as inherited); tax applied after the run at 0 / 25 / 47 / 53%. "20% of nominal" = mean
  steady-state net per year ÷ (20 × account size) ≥ 20%, i.e. $10k per 50K slot-year = 5 × the $2,000 drawdown. Apex itself bans
  bots on funded accounts (inherited grade D); its plan is used here only because it is the only trade-level plan the inherited
  model has. The Topstep / MFFU / Lucid differences (lock level, no evaluation clock, payout caps, consistency rules, real-time or
  intraday trailing) are exactly the items in §10.
- **Frame B, daily Sharpe/vol** (`economics`, D1-01 settings: t5 shocks, 4 checks a day, n = 2000, seeds 11/12) for the five
  bot-allowed futures programs in `firms.py` (Topstep XFA 50K, Bulenox Master 50K, Lucid Flex 50K, Tradeify Select 50K, MFFU Rapid
  EOD 50K) at S ∈ {1, 1.5, 2, 3, 4, 6}, sigma grid ≤ 20%, read at vol caps 12% and 20%; the Sharpe at which net $/slot-year reaches
  20% of nominal ($10k) is interpolated.
- To tie frame A to the FTMO table, each (R, trades/day) cell also carries the annual Sharpe it implies for i.i.d. trades with the
  model's payoff and costs (per-trade mean ÷ s.d. × √(trades/day × 250)) and the annual vol as % of nominal.

_Results: pending (filled from `tables_rerun.md` T7–T9 when the run completes)._

## 9. Tax note: business income vs capital gains (±≈ one third on the required edge)

- Every F2 figure, inherited and re-run, is **pre-tax** net $ per slot-year to Itamar: after the 80% split, the $510 fee (refunded
  with the first payout), re-bought evaluations and breached funded accounts (the renewal-reward frame prices resets and failed
  accounts), before Israeli tax. The common brief's "$20,000 … after profit split, fees, resets and failed accounts" and
  `PARAMETERS.md` are silent on tax, so the headline table (§6) is pre-tax, as inherited.
- Two readings exist in the inherited record (`references/numbers.md` "The classification decides the target", the accountant
  letter in `references/verification-letters.md` §2, and `pr26/prompts/research/firms-2026-10-11.md`: "business income vs capital
  gains changes the required edge by about a third"): **25% capital gains** (the optimistic branch) or **47% business income** at
  the top marginal rate (≈ 53% with National Insurance and the health levy, rates unverified; 60% adverse case). Every fact in the
  letter argues for the business-income side: nothing is owned or sold, the account is simulated, the payment is contractual
  consideration for a result produced by a program trading daily. VAT (18% of gross receipts unless the export zero-rating applies)
  was never priced; it is the accountant's question.
- In the inherited trade-level frame the required edge moved from +0.249R (25%) to +0.339R (47%), **+36%**, and +0.379R (53%); the
  re-run of that frame is in §8 (T7). In the Sharpe frame the equivalent statement is: if the $20k must be **after** tax, the
  pre-tax target is $26.7k (25%) or $37.7k (47%), and the required net Sharpe rises as T3 in §6 shows (rows "$20k after 25% tax" and
  "$20k after 47% tax"). Because net $/slot-year is close to linear in S above S ≈ 1 with a small positive intercept, the
  business-income reading raises the required Sharpe by roughly a third to a half at every volatility; the capital-gains reading by
  roughly 15–25%. _Exact figures: §6, T3, filled when the run completes._
- The D1/F2 convention taxes each positive year and gives no relief on losing years (`after = net × (1 − TAX) if net > 0`), which is
  conservative; this note uses the same convention through the pre-tax target.

## 10. What the Rules Keeper must refresh before any intraday variant is registered

Every futures-firm parameter used in §8 is **inherited (fetched 2026-10-11)** from `w1-prop/firms.py` / `rules.csv`
(`~/quant-edge-inherited/pr4/skills/prop-fleet/agents/daily/w1-prop/`) and the pr26 digest
`~/quant-edge-inherited/pr26/prompts/research/firms-2026-10-11.md` (partly re-verified 2026-11-03). None of it was fetched by this
agent (no web access was used in this re-run). Before any intraday variant is registered the Rules Keeper must re-fetch, date and
archive at least these inputs, because the inherited model either omits them or models them with an Apex-era proxy:

1. **Topstep 50K Express Funded**: the maximum loss limit of $2,000 trails the end-of-day balance but is enforced in real time
   including unrealised P&L, locks at **+$2,000** (floor stops at the initial balance) and resets to the initial balance after the
   first payout (`firms.py` has `dd_lock=0.0`, no post-payout reset); payout policy 50% of balance per request, capped at $2,000
   (Standard) or $3,000 (Consistency policy; the April 2026 cap change is supported only by secondary sources); $49/month plus
   $149 activation; 5-day / $150 qualification; flat by 3:10 PM CT (auto-flatten 3:08); own-device-only execution (no VPS); Live
   call-up closes every Express account; pass-through commissions ≈ $3.78 round trip per mini, $1.22 per micro.
2. **MyFundedFutures Rapid (non-EOD)**: intraday trailing drawdown from the equity high-water mark (`firms.py` models only Rapid
   EOD with `trail_eod`; a `trail_intraday` row is needed), Rapid/Pro news ban ±2 minutes including resting orders, flat by 4:10 PM
   ET, 3 accounts on Rapid EOD 50K, payout buffer $2,100, split cut from 90% to 80% on Flex/Pro in Feb 2026 (`firms.py` still has
   0.9 for Rapid EOD: verify per plan), 7-day inactivity rule, 30% / 40% consistency rules (not modelled).
3. **EOD-trailing plans** (Lucid Flex, Tradeify Select, MFFU Rapid EOD, Bulenox Master): the $2,000 (Bulenox $2,500) EOD-trailing
   drawdown and its lock at +$100 (Topstep locks at start); Lucid's live review after 5 payouts and 5-second micro-scalping flag;
   Tradeify's $2,500 payout cap, 10-second hold rule and single-firm clause; Bulenox's 30-day evaluation clock, $1,100 soft daily
   loss, 100% of the first $10k then 90%, $1,500 cap on the first three payouts; flat deadlines (Lucid/Tradeify 4:45 PM ET,
   Bulenox 3:59 PM CT).
4. **Payout caps and consistency rules at every firm** (eval best-day 50–55% at Topstep, 50% Lucid, 40% Tradeify, 30% MFFU, 40%
   Bulenox payout consistency): none is in the daily model; the Apex-era trade-level model has only Apex's 50% rule and ladder.
5. **Costs**: the trade-level model charges $1.30 per MES round trip plus 0.25 pt slippage on stopped exits only; the common brief's
   floor is MES 0.25 pt + $0.80 **per side** (ES 0.30 pt + ≈ $2.50) and the Nov 2026 sweep's pass-through round trips are
   $1.00–1.22 per micro at Lucid/Topstep. Refresh and run the 2× cost case.
6. **Trading-day boundary** (18:00 ET Globex reopen to the firm's flat deadline) and whether an overnight-session hold counts as one
   trading day at each firm, in writing.
7. **Unattended automation wording** at MyFundedFutures (the firm's text is silent on "unattended") and Topstep's own-device rule
   (the bot must run on Itamar's computer, which also decides the IBKR-bridge design, Department G).

## 11. Failures, limits and honest caveats

1. **Scope cut by the CPU budget**: FTMO Swing 100K only; Blue Guardian and CFT were not re-run; sigma grid ≤ 20% (caps 30% and
   "no cap" not re-run except in the F2-09 replication job); S grid of five points plus 3.5 / 4.0 at one seed; the inherited F2-14
   calendar chains at S = 0 (the lottery verdict) were not repeated, the inherited F2-11 verdict stands (S = 0 at the 12% cap:
   $1.2k a year, 84% chance of a losing first year).
2. **What the s.e. covers**: five seed pairs give the Monte Carlo s.e. of each cell (itself uncertain by ≈ 35% with 4 degrees of
   freedom) and, through the delta method, of each interpolated Sharpe. It does not cover model error. The "better-of" rule takes
   the larger of two noisy means, a small upward bias that is irrelevant here because F2-13 never wins a cell (T2).
3. **Model biases F2-12/F2-13 did not remove** (all documented in the inherited `redteam-model.md`): the 10%/day closed-balance lag
   is a bot-design choice, not a firm rule (F2-12 keeps it; F2-13 is the other extreme at a 0.47 Sharpe cost, so the truth sits
   between the two books and F2-12 is the better of the two everywhere); the kill switch executes perfectly at no cost; a book that
   was flattened still takes the next opening gap; funded lives are cut at 756 days (survivors forfeit future payouts, conservative);
   σ_e ≠ σ_f is allowed by the optimiser (at caps 12–20% it always picked the diagonal, see T4); no payout denial, firm failure or
   common-mode event across a fleet; FTMO's $400k per-strategy cap, scaling plan, swaps (≈ −8%/yr on long index exposure) and the
   30-day inactivity rule are outside the model: "net Sharpe S" is the book's daily Sharpe **after** all those costs.
4. **Linear interpolation** between S grid points: the inherited 0.25-step F2-09 curve is smooth and slightly concave, so the error
   from the coarser 0.4–0.5 steps used here is of order 0.02 in S, below the reported s.e. at 12% vol and comparable to it at 20%.
5. **"Net Sharpe" means** a constant-vol daily book; a strategy that is flat most of the time has the same Sharpe but a different
   breach path (and meets inactivity rules differently). The volatility in the table is the book's realised annual vol, which is
   what the firm sees, not the instrument's.
6. **Futures frame (§8) is a first pass on Apex-era proxies**; every parameter is inherited (fetched 2026-10-11) and §10 lists what
   must be refreshed before any intraday variant is registered. The trade-level model has no slippage on winning exits, no
   per-side cost floor as in the common brief, and no ceiling on how fast burned accounts are replaced.
7. **No web access was used** and nothing was bought or contacted. No market data was read. N is unchanged (280 inherited + 0).
8. **Reproducibility**: the inherited `results.json` of the F2 run is not in the record (git-ignored), so the F2-12/F2-13 numbers
   here cannot be checked against the inherited run; the F2-09 replication job (T6) is the bridge: it re-creates the inherited
   S = 1.0 row from `tables.md` with the same seeds and the full grid.

## 12. Files, commands, seeds, run times

_pending_
