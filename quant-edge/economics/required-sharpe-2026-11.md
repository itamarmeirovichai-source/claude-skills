# Required net Sharpe for $20k / $30k per slot-year — F2-12 re-run (2026-11-03)

Status: **complete** (written early, extended as the run proceeded). Economist, Department F.
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
- Code, logs, raw outputs and every table: `quant-edge/economics/f2_rerun/` (README with provenance and SHA256 sums; no data
  files, nothing over 1 MB). Full tables: `quant-edge/economics/f2_rerun/tables_rerun.md` (T1–T9, cited below).

## 1. Summary

- **Required net Sharpe for $20,000 per $100k FTMO Swing two-step slot-year, pre-tax, re-run 2026-11-03: 2.44 at 12% annual
  volatility, 1.95 at 15%, 1.45 at 20%** (F2-12 corrected model; F2-13, the daily-realisation book, loses to F2-12 in every cell,
  so F2-12 is also the "better-of" verdict). Inherited F2-09: 2.42 / 1.92 / 1.46. The re-run confirms the inherited table within
  0.03 Sharpe, and "1.5 at 20% is a floor" holds: the better book gives 1.45, the other book 1.93.
- **For $30,000 per slot-year: 3.52 / 2.82 / 2.11** (the 12% figure sits between single-seed cells at S = 3.5 and 4.0).
- **Monte Carlo s.e.** from five seed pairs: $6–61 per slot-year per cell (0.1–0.3% of the cell), and 0.002–0.004 on each
  interpolated Sharpe by the delta method. The linear interpolation (≈ 0.02 in S) and model error dominate the MC error.
- F2-12 is 3–4% below the inherited F2-09 at S = 1.0 (the fat-daily-tail correction) and equal within 1.5% at S ≥ 2.0; the four
  F2-12 corrections net to almost nothing for FTMO. F2-13 (close and reopen everything daily at a 0.47 Sharpe cost) is worse by
  $3.7k–7.8k per slot-year in every cell: the 10%/day closed-balance lag costs less than the daily round trip at these volatilities.
- At S = 1.5 (12 / 15 / 20% vol): evaluation pass probability 91 / 88 / 85% per attempt; first payout 234 / 192 / 144 trading days
  after the first purchase (≈ 11 / 9 / 7 months); funded life 601 / 521 / 402 days; 0.11 / 0.19 / 0.36 funded accounts lost and
  0.34 / 0.41 / 0.56 evaluations bought per slot-year; 1 / 3 / 5% of funded accounts breach before their first payout. Calendar
  chain, year 1: mean $3.5k / 6.7k / 11.4k, p10 −$0.5k, P(loss) 40 / 23 / 13%; years 2–3: mean $13.0k / 16.4k / 22.0k, p10 $6.0k /
  8.1k / 11.6k, p90 $19.7k / 24.8k / 32.5k.
- **Tax**: the table is pre-tax, as inherited. If the $20k must be net of tax, the capital-gains reading (25%) needs 3.16 / 2.53 /
  1.89 and the business-income reading (47%) > 4.0 / 3.47 / 2.61: the two readings differ by ≈ 37% in required Sharpe, "about a
  third", and the business-income reading is the likely one.
- **Futures-firm frame, first pass** (every parameter inherited, fetched 2026-10-11): on a $2,000-drawdown 50K plan at 4% of
  drawdown per trade, 20% of nominal needs **+0.31R per trade at 3 trades a day** at 25% tax (+0.41R at 47%), +0.21R at 5 a day,
  +0.44R at 2 a day; 1 trade a day cannot reach it at 4% (a single win is below the $200 qualifying-day minimum) and needs +0.53R at
  8% of drawdown. Those pairs imply an annual Sharpe of 3.7–5.8 at 5–8% volatility of nominal, a return-to-drawdown ratio of 5. In
  the daily Sharpe frame the five bot-allowed futures programs need S ≈ 2.6–4.0 at a 12% vol cap and 1.6–2.4 at 20% for $10k per
  50K slot-year. The legacy 50K plan reproduces the inherited +0.25R / +0.34R / +0.38R (25 / 47 / 53% tax) to ±0.003R.
- CPU used: 57.6 minutes in total (budget ≈ 60). No web access, no purchases, no contact, no market data.

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
`w1-prop/`) because `stress_model.py` imports `prop_model` from `../w1-prop`. Nothing in `~/quant-edge-inherited` was edited;
`f2_rerun/SHA256SUMS` shows the copies equal the worktree files.

- `python3 -m pytest -q test_stress_model.py` in `w3-volrisk/`: **21 passed in 8.39 s** (log `f2_rerun/logs/pytest_w3.log`).
  `test_no_stress_reproduces_d1_eval_and_funded` and `test_new_switches_off_still_match_d1` pass, so the copy reproduces D1 bit for
  bit with every stress switch off.
- `python3 -m pytest -q test_prop_model.py` in `w1-prop/`: **14 passed in 0.25 s** (log `f2_rerun/logs/pytest_w1.log`).
- Environment: Python 3.13.18, numpy 2.5.3, scipy 1.18.1, numba 0.68.1, 4 CPUs.

## 4. Runtime budget

`run_f2.log` and `run_f2_full.log` carry no timings, only "done" lines (the inherited run was finished in a director session after
the F2 session stopped mid-run). One F2-12 job (FTMO, S = 1.0, n = 3000, 24 checks a day, 756-day horizon) was timed in the
scratch copy (`time_job.py`, log `logs/time_job.log`): sigma grid restricted to ≤ 20% (11 of D1's 14 sigmas) eval 20.5 s + funded
20.7 s = **41 s CPU**; full grid 26.2 + 26.4 = **53 s CPU** (an F2-09 job costs about twice that, because without `daily_t` every
sub-step draws Student-t shocks). The inherited F2-01..15 programme is about 268 grid jobs and 144 calendar-chain jobs, roughly 3
CPU-hours on this machine, far above the brief's ≈ 60 CPU-minutes, so the re-run was shrunk as follows (nothing else changed in the
model):

- FTMO Swing 2-Step 100K only (the brief's firm); Blue Guardian and CFT not re-run.
- Sigma grid ≤ 20% (1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20%). The capped optimum at caps 12 / 15 / 20% only reads cells with both
  sigmas ≤ cap, so this changes the random stream (the arrays have 11 rows instead of 14) but not the estimand. The seed-to-seed s.e.
  reported below covers that stream difference.
- S grid {1.0, 1.5, 2.0, 2.4, 3.0} as the brief asks (the inherited grid was 0 … 3.5 in steps of 0.25), with five seed pairs each
  (F2's base pair eval 11 / funded 12 and F2-15's 101/102, 202/203, 303/304, 404/405): 2 scenarios × 5 S × 5 seeds = 50 jobs,
  35.5 CPU-minutes. S = 3.5 and 4.0 at the base seed only (to bracket the $30k crossing at 12% vol; 4 jobs, 2.9 CPU-minutes). One
  F2-09 job at S = 1.0 on the full grid as a replication check against the inherited `tables.md` (1.8 CPU-minutes). Calendar
  chains (inherited `slot_years`, 2000 slots × 3 years) for every (scenario, S, cap) at the base seed's sigma pair (42 small jobs,
  2.5 CPU-minutes).
- n = 3000 paths per sigma kept as registered.

Achieved: 42.8 CPU-minutes for the FTMO re-run (97 jobs), 13.1 for the futures frame, 1.7 for tests and timing: **57.6 CPU-minutes**.

## 5. Re-run F2-12 and F2-13, FTMO Swing 100K two-step, caps 12 / 15 / 20%

Scenario definitions exactly as registered (`scenarios.py`, unchanged): F2-12 = t3 daily moves with a Brownian intraday path
(`daily_t`), gaps (25% of daily variance at the open, a second day's variance on Mondays) with the bot's kill switch at 80% of the
daily loss, GARCH clustering (0.10 / 0.88, cap h ≤ 100), 24 equity checks a day, FTMO-exact rules (5% daily loss from the 00:00
CE(S)T balance checked on equity, 10% static maximum loss, $510 fee refunded with the first payout, 80% split, first payout after 10
days then every 10 days), closed balance realising 10% of open P&L a day, the post-payout reference fix. F2-13 = F2-12 with
`real_rate = 1` (everything realised daily) and `cost_S = 0.47`. Metric: pre-tax net $ per slot-year in the renewal-reward frame
(expected payouts + refund − fees per cycle, divided by the expected cycle length of evaluations until a pass plus the funded life),
at the best (σ_eval, σ_funded) pair with both ≤ cap. The optimiser chose the diagonal (σ_e = σ_f = cap) in every cell.

**T1 (compact). Net $ per slot-year, pre-tax, seed mean ± MC s.e. over five seed pairs (one seed at S = 3.5, 4.0)**

| Scenario | S | cap 12% | cap 15% | cap 20% |
|---|---|---|---|---|
| F2-12 | 1.0 | 7,220 ± 17 | 9,472 ± 30 | 13,349 ± 24 |
| F2-12 | 1.5 | 11,496 ± 6 | 14,887 ± 31 | 20,700 ± 51 |
| F2-12 | 2.0 | 15,973 ± 15 | 20,551 ± 19 | 28,323 ± 58 |
| F2-12 | 2.4 | 19,6xx ± 23 | 25,2xx ± 29 | 34,5xx ± 61 |
| F2-12 | 3.0 | 25,2xx ± 24 | 32,2xx ± 21 | 43,9xx ± 47 |
| F2-12 | 3.5 | 29.8k | 38.1k | 51.7k |
| F2-12 | 4.0 | 34.6k | 44.0k | 59.5k |
| F2-13 | 1.0 | 3,5xx ± 16 | 4,8xx ± 24 | 6,9xx ± 33 |
| F2-13 | 1.5 | 7,4xx ± 11 | 9,7xx ± 23 | 13,6xx ± 25 |
| F2-13 | 2.0 | 11,7xx ± 11 | 15,2xx ± 39 | 21,0xx ± 46 |
| F2-13 | 2.4 | 15,3xx ± 19 | 19,7xx ± 30 | 27,0xx ± 50 |
| F2-13 | 3.0 | 20,8xx ± 15 | 26,6xx ± 32 | 36,2xx ± 50 |

(Exact seed means to the dollar, base-seed values and the F2-13 rows at S = 3.5 / 4.0: `tables_rerun.md` T1; the "xx" cells are
printed there to $0.1k, the first three F2-12 rows above are the exact means.) F2-12 wins every cell (T2), so **better-of =
F2-12**. Inherited F2-09 at S = 1.0 for comparison: 7.5k / 9.9k / 13.6k; at S = 1.5: 11.7k / 15.2k / 20.6k; at S = 2.0: 16.1k /
20.9k / 28.2k.

**Replication check (T6)**: the F2-09 scenario at S = 1.0, base seed, full grid, re-creates the inherited `tables.md` row to the
rounding: 7,546 / 9,927 / 13,551 / 21,161 / 26,560 against 7.5k / 9.9k / 13.6k / 21.2k / 26.6k at caps 12 / 15 / 20 / 30 / 40%.
The pipeline, seeds and numpy stream are the inherited ones.

**Diagnostics at the base seed (T4, F2-12)** — pass probability per attempt, expected evaluation days until the first pass
(geometric re-buys), funded life, trader payouts per funded account, P(any payout), breach before the first payout, trading days
from the first purchase to the first payout, evaluations bought and funded accounts lost per slot-year, fees per slot-year:

| S | cap | pass | eval days | life | pay/acct | P(any) | breach pre-1st | days to 1st payout | evals/slot-yr | funded lost/slot-yr | fees/slot-yr |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.0 | 12% | 85% | 318 | 557 | 25,298 | 98% | 2% | 337 | 0.34 | 0.13 | 174 |
| 1.0 | 15% | 81% | 259 | 473 | 27,848 | 96% | 4% | 278 | 0.43 | 0.22 | 218 |
| 1.0 | 20% | 74% | 187 | 340 | 28,175 | 94% | 6% | 203 | 0.65 | 0.40 | 330 |
| 1.5 | 12% | 91% | 218 | 601 | 37,451 | 99% | 1% | 234 | 0.34 | 0.11 | 172 |
| 1.5 | 15% | 88% | 176 | 521 | 41,405 | 97% | 3% | 192 | 0.41 | 0.19 | 210 |
| 1.5 | 20% | 85% | 130 | 402 | 43,749 | 95% | 5% | 144 | 0.56 | 0.36 | 285 |
| 2.0 | 12% | 94% | 163 | 619 | 49,738 | 99% | 1% | 177 | 0.34 | 0.11 | 174 |
| 2.0 | 15% | 91% | 134 | 552 | 56,091 | 98% | 2% | 148 | 0.40 | 0.17 | 206 |
| 2.0 | 20% | 89% | 99 | 442 | 60,932 | 96% | 4% | 111 | 0.52 | 0.32 | 267 |
| 2.4 | 12% | 96% | 137 | 629 | 59,777 | 99% | 1% | 149 | 0.34 | 0.10 | 175 |
| 2.4 | 15% | 93% | 111 | 574 | 68,688 | 98% | 2% | 124 | 0.40 | 0.16 | 202 |
| 2.4 | 20% | 92% | 83 | 467 | 75,489 | 97% | 3% | 95 | 0.50 | 0.29 | 256 |
| 3.0 | 12% | 96% | 110 | 642 | 75,270 | 99% | 1% | 121 | 0.35 | 0.09 | 177 |
| 3.0 | 15% | 94% | 89 | 590 | 86,867 | 99% | 1% | 101 | 0.39 | 0.15 | 201 |
| 3.0 | 20% | 94% | 67 | 491 | 96,933 | 97% | 3% | 78 | 0.48 | 0.27 | 246 |

Reading: "accounts burned" has two parts. Funded accounts lost to a breach are 0.1–0.4 per slot-year; the rest of the
"evaluations bought" (0.34–0.65 per slot-year) are renewals forced by the model's 756-day cap on a funded life (at 12% vol most
funded accounts reach the cap alive and are counted as re-bought; this is the inherited convention and is conservative). Time to
the first payout in calendar months ≈ trading days × 12 / 252: at S = 1.5 about 11 / 9 / 7 months at 12 / 15 / 20%, at S = 2.4
about 7 / 6 / 4.5 months. F2-13's diagnostics (same table in `tables_rerun.md`) are uniformly worse: at S = 1.0 pass 64 / 61 / 58%
and 596 / 475 / 325 days to the first payout.

## 6. Required net Sharpe table ("re-run 2026-11-03" beside "inherited")

Linear interpolation on the S grid of the seed means; ± is the delta-method MC s.e. from the bracketing cells (absent where a
bracketing cell has one seed). FTMO Swing 2-Step 100K, pre-tax net $ per slot-year to Itamar after split, fees, resets and failed
accounts.

| Target | Book | vol 12% | vol 15% | vol 20% |
|---|---|---|---|---|
| **$20k** | **F2-12 re-run 2026-11-03** | **2.44 ± 0.002** | **1.95 ± 0.002** | **1.45 ± 0.003** |
| $20k | F2-13 re-run 2026-11-03 | 2.92 | 2.43 | 1.93 |
| $20k | better-of (F2-12 / F2-13) re-run 2026-11-03 | 2.44 | 1.95 | 1.45 |
| $20k | F2-09 (ALL combined) inherited | 2.42 | 1.92 | 1.46 |
| $20k | F2-01 (D1 baseline) inherited | 2.42 | 1.88 | 1.42 |
| **$30k** | **F2-12 re-run 2026-11-03** | **3.52** (single-seed bracket) | **2.82 ± 0.002** | **2.11 ± 0.004** |
| $30k | F2-13 re-run 2026-11-03 | 3.99 | 3.29 | 2.59 |
| $30k | better-of re-run 2026-11-03 | 3.52 | 2.82 | 2.11 |
| $20k after 25% tax (= $26.7k pre-tax) | F2-12 re-run | 3.16 | 2.53 | 1.89 |
| $20k after 47% tax (= $37.7k pre-tax) | F2-12 re-run | > 4.0 | 3.47 | 2.61 |
| $30k after 25% tax (= $40.0k pre-tax) | F2-12 re-run | > 4.0 | 3.66 | 2.75 |
| $30k after 47% tax (= $56.6k pre-tax) | F2-12 re-run | > 4.0 | > 4.0 | 3.81 |

Source: `tables_rerun.md` T3 (all rows incl. F2-13 and better-of for every target). The seed-mean curves are concave: slope ≈
$9.0k per unit of Sharpe at 12% vol, $11.4k at 15%, $14.8k at 20% around the $20k crossing.

Verdict for the board: **$20k per slot-year at FTMO Swing needs net Sharpe 2.44 / 1.95 / 1.45 at 12 / 15 / 20% vol; $30k needs
3.52 / 2.82 / 2.11.** The inherited 2.4 / 1.9 / 1.5 stand; the re-run replaces the "inherited" label on them.

## 7. Calendar chain: p10 / p90 per slot-year, year 1 against steady state

Inherited `slot_years` (fees paid on the purchase date, the $510 refund on the date of the first payout, attempts and funded lives
chained in calendar order, 2000 slots × 3 years, seed 21), F2-12, at the base-seed sigma pair of each cap (T5 has every row incl.
F2-13 and S = 1.0, 3.5, 4.0):

| S | cap | year-1 mean | p10 | p50 | p90 | P(year-1 loss) | years 2–3 mean | p10 | p50 | p90 | P(loss) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.5 | 12% | 3.5k | −0.5k | 2.0k | 10.1k | 40% | 13.0k | 6.0k | 12.9k | 19.7k | 0% |
| 1.5 | 15% | 6.7k | −0.5k | 5.4k | 16.1k | 23% | 16.4k | 8.1k | 16.3k | 24.8k | 0% |
| 1.5 | 20% | 11.4k | −0.5k | 10.5k | 24.3k | 13% | 22.0k | 11.6k | 21.6k | 32.5k | 0% |
| 2.0 | 12% | 7.0k | −0.5k | 6.3k | 14.8k | 15% | 18.1k | 11.2k | 18.1k | 24.8k | 0% |
| 2.0 | 15% | 11.2k | 0.6k | 10.7k | 21.4k | 8% | 22.5k | 14.3k | 22.3k | 30.4k | 0% |
| 2.0 | 20% | 18.1k | 4.7k | 17.6k | 31.8k | 4% | 30.0k | 18.8k | 29.8k | 40.8k | 0% |
| 2.4 | 12% | 10.3k | 1.6k | 10.0k | 18.8k | 7% | 22.1k | 15.0k | 22.0k | 28.8k | 0% |
| 2.4 | 15% | 15.4k | 4.6k | 15.0k | 26.1k | 3% | 27.4k | 19.0k | 27.5k | 35.3k | 0% |
| 2.4 | 20% | 24.0k | 10.2k | 24.1k | 37.7k | 2% | 36.6k | 25.4k | 36.6k | 47.3k | 0% |
| 3.0 | 12% | 15.8k | 6.7k | 15.7k | 24.6k | 1% | 27.8k | 20.8k | 27.9k | 34.4k | 0% |
| 3.0 | 15% | 21.9k | 10.9k | 21.7k | 32.7k | 1% | 34.7k | 25.7k | 34.9k | 42.9k | 0% |
| 3.0 | 20% | 32.5k | 17.8k | 32.5k | 47.1k | 0% | 46.2k | 35.2k | 46.0k | 57.0k | 0% |

Reading: year 1 is lean at every Sharpe the program can hope for (at S = 1.5 and 12% vol a slot has a 40% chance of a losing first
year and a p10 of −$0.5k, i.e. the fee), because the two-step evaluation at 12% vol takes most of a year; the steady state of years
2–3 is 5–15% above the renewal-reward rate of §5 (the renewal frame charges every cycle's evaluation time; the chain's later years
start funded). At S = 1.0 (T5) the year-1 loss probability is 66 / 52 / 34% and the steady-state p10 $1.3k / 2.7k / 3.8k. The p90
of a single slot in steady state at the S the target requires is roughly 1.4–1.5× the mean; across a fleet that copies one strategy
the slots are perfectly correlated, so fleet p10 = slots × slot p10 (inherited convention).

## 8. Futures-firm frame, first pass (D1 `prop_model.py`, all firm parameters "inherited (fetched 2026-10-11)")

Script: `f2_rerun/futures_frame.py` (+ `futures_frame_1tpd.py`; logs `logs/futures_frame*.log`, outputs `futures_frame*.json`),
running the unmodified inherited `w1-prop/prop_model.py` + `firms.py`. Every firm parameter below is **inherited (fetched
2026-10-11)**; nothing was re-fetched. Two frames, because the inherited model has two:

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
- **Frame B, daily Sharpe/vol** (`economics`, D1-01 settings: t5 shocks, 4 checks a day, n = 2000, seeds 11/12, no F2 stresses)
  for the five bot-allowed futures programs in `firms.py` (Topstep XFA 50K, Bulenox Master 50K, Lucid Flex 50K, Tradeify Select
  50K, MFFU Rapid EOD 50K) at S ∈ {1, 1.5, 2, 3, 4, 6}, sigma grid ≤ 20%, read at vol caps 12% and 20%; the Sharpe at which net
  $/slot-year reaches 20% of nominal ($10k) is interpolated.
- To tie frame A to the FTMO table, each (R, trades/day) cell also carries the annual Sharpe it implies for i.i.d. trades with the
  model's payoff and costs (per-trade mean ÷ s.d. × √(trades/day × 250)) and the annual vol as % of nominal.

**Frame A results (T7, T7b): R per trade that reaches 20% of nominal in steady state**

| Plan | trades/day | funded size | pre-tax | 25% tax | 47% tax | 53% tax | implied annual Sharpe at the 25% threshold | implied vol, % of nominal |
|---|---|---|---|---|---|---|---|---|
| 50K-2026 ($2,000 DD) | 1 | 4% of DD | never (≤ 1.0R) | never | never | never | – | – |
| 50K-2026 | 2 | 4% | 0.344 | 0.442 | 0.604 | 0.675 | 5.8 | 5% |
| **50K-2026** | **3** | **4%** | **0.244** | **0.306** | **0.413** | **0.460** | **4.7** | **7%** |
| 50K-2026 | 5 | 4% | 0.167 | 0.205 | 0.270 | 0.299 | 3.7 | 8% |
| 50K-2026 | 1 | 8% | 0.433 | 0.526 | 0.682 | 0.748 | 5.0 | 8% |
| 50K-2026 | 2 | 8% | 0.245 | 0.308 | 0.430 | 0.491 | 3.8 | 11% |
| 50K-2026 | 3 | 8% | 0.181 | 0.216 | 0.273 | 0.298 | 3.0 | 13% |
| 150K ($5,000 DD) | 1 | 4% | 0.941 | > 1.0 | > 1.0 | > 1.0 | – | – |
| 150K | 2 | 4% | 0.586 | 0.784 | > 1.0 | > 1.0 | 11.1 | 4% |
| 150K | 3 | 4% | 0.355 | 0.459 | 0.651 | 0.747 | 7.4 | 6% |
| 150K | 5 | 4% | 0.241 | 0.324 | 0.488 | 0.567 | 6.4 | 7% |
| 150K | 1 / 2 / 3 | 8% | 0.700 / 0.352 / 0.274 | 0.840 / 0.433 / 0.355 | > 1.0 / 0.578 / 0.524 | > 1.0 / 0.649 / 0.611 | 8.6 / 5.8 / 5.6 | 6 / 9 / 11% |
| legacy 50K ($2,500 DD) | 3 | 4% | 0.198 | **0.251** | **0.341** | **0.382** | 3.9 | 8% |

- The legacy 50K row reproduces the inherited "+0.250R at 25%, +0.340R at 47%, +0.379R at 53%" (`numbers.md`) to ±0.003R, so the
  frame runs as it did. On the current $2,000-drawdown 50K plans the same sizing needs **+0.31R at 3 trades a day** (25% tax),
  +0.41R at 47%; 5 trades a day lowers it to +0.21R / +0.27R; 2 a day raises it to +0.44R / +0.60R.
- **1 trade a day never pays out at 4% of drawdown**: one winning trade (+$157 on 50K-2026, +$197 on legacy 50K) is below the plan's
  $200 qualifying-day minimum, so no payout day ever qualifies, whatever R is. At 8% of drawdown (one win = +$317) 1 trade a day
  needs +0.53R (25% tax) / +0.68R (47%). The inherited "+0.78R at 1 a day" came from a different fleet configuration ("view B",
  Bulenox 5 + Topstep 5) and was not re-derived here. Qualifying-day minimums exist at the real futures firms too (Topstep $150 on 5
  days, Lucid $150, MFFU buffer), so this interaction must be re-run with the refreshed rules (§10).
- The implied-Sharpe column is the point of the exercise: the pairs that reach 20% of nominal imply an **annual Sharpe of 3.7–5.8
  at 5–8% volatility of nominal** (3.0 at 13% vol with 8% sizing), because the risk capital is the $2,000 drawdown, not the $50k
  nominal, so 20% of nominal is a return-to-drawdown ratio of 5. Against the FTMO table (1.45 at 20% vol, 2.44 at 12%) the futures
  route needs two to three times the Sharpe per unit of volatility, before the cost floor of the common brief (MES 0.25 pt + $0.80
  per side, about twice what this model charges) is applied. Grid behind the 50K-2026 / 3-a-day row, with p10 across fleet paths
  and accounts lost per slot-year: T8 (at +0.30R: 0.3 accounts lost and 1.7 evaluations bought per slot-year, fleet p10 16% of
  nominal at 25% tax; at +0.10R: 2.5 lost, 3.8 bought, 3.3%).

**Frame B results (T9): net $ per 50K slot-year in the daily model, and the Sharpe for 20% of nominal ($10k)**

| Program (inherited parameters, fetched 2026-10-11) | S = 1: cap 12% / 20% | S = 2 | S = 3 | S = 4 | S for $10k at cap 12% / cap 20% |
|---|---|---|---|---|---|
| Topstep XFA 50K | 1,756 / 5,497 | 4,615 / 10,585 | 8,929 / 19,185 | 14,851 / 29,316 | 3.18 / 1.90 |
| Bulenox Master 50K | 1,382 / 5,737 | 6,200 / 12,925 | 12,507 / 22,156 | 18,755 / 32,128 | 2.60 / 1.63 |
| Lucid Flex 50K | 1,870 / 4,532 | 4,127 / 8,185 | 6,886 / 12,962 | 10,137 / 18,181 | 3.96 / 2.38 |
| Tradeify Select 50K | 2,632 / 5,551 | 5,979 / 10,723 | 10,345 / 18,460 | 15,945 / 27,527 | 2.92 / 1.88 |
| MFFU Rapid EOD 50K | 3,084 / 5,928 | 7,051 / 11,243 | 12,417 / 18,637 | 18,633 / 27,055 | 2.55 / 1.79 |

Reading: in the daily frame (no F2 stresses, D1 baseline settings) the futures programs need S ≈ 2.6–4.0 at a 12% vol cap and
1.6–2.4 at 20% for 20% of nominal, against FTMO's 2.44 / 1.45 under the full F2-12 stress; the $2,000 trailing drawdown (4% of
nominal against FTMO's 10% static), 20–60-day funded lives and payout caps are why. All of it is a first pass on inherited
parameters; §10 lists what the Rules Keeper must refresh before any intraday variant is registered.

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
- In the trade-level frame the required edge moves from +0.306R (25%) to +0.413R (47%), **+35%**, and +0.460R (53%) on the
  50K-2026 plan at 3 trades a day (legacy 50K: +0.251R → +0.341R → +0.382R, the inherited +36%). In the Sharpe frame: if the $20k
  must be **after** tax, the pre-tax target is $26.7k (25%) or $37.7k (47%) and the required net Sharpe becomes 3.16 / 2.53 / 1.89
  (25%) or > 4.0 / 3.47 / 2.61 (47%) at 12 / 15 / 20% vol (T3): the capital-gains reading adds ≈ 30% to the pre-tax requirement, the
  business-income reading adds ≈ 80%, and **the two readings differ by ≈ 37%**, which is the "about a third" of the inherited
  record. At 20% vol the honest planning number for an after-tax $20k is therefore 2.6, not 1.5, until an accountant answers.
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
4. **Payout caps, qualifying-day minimums and consistency rules at every firm** (eval best-day 50–55% at Topstep, 50% Lucid, 40%
   Tradeify, 30% MFFU, 40% Bulenox payout consistency; $150 qualifying days at Topstep/Lucid): none of the consistency rules is in
   the daily model; the Apex-era trade-level model has only Apex's $200 qualifying day, 50% rule and ladder, and §8 shows the
   qualifying-day rule alone decides whether 1 trade a day can ever pay.
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
   σ_e ≠ σ_f is allowed by the optimiser (at caps 12–20% it always picked the diagonal, T4); no payout denial, firm failure or
   common-mode event across a fleet; FTMO's $400k per-strategy cap, scaling plan, swaps (≈ −8%/yr on long index exposure) and the
   30-day inactivity rule are outside the model: "net Sharpe S" is the book's daily Sharpe **after** all those costs.
4. **Linear interpolation** between S grid points: the inherited 0.25-step F2-09 curve is smooth and slightly concave, so the error
   from the coarser 0.4–0.6 steps used here is of order 0.02 in S, an order of magnitude above the MC s.e.; the $30k figure at 12%
   vol rests on single-seed cells at S = 3.5 and 4.0.
5. **"Net Sharpe" means** a constant-vol daily book; a strategy that is flat most of the time has the same Sharpe but a different
   breach path (and meets inactivity rules differently). The volatility in the table is the book's realised annual vol, which is
   what the firm sees, not the instrument's.
6. **Futures frame (§8) is a first pass on Apex-era proxies**; every parameter is inherited (fetched 2026-10-11) and §10 lists what
   must be refreshed before any intraday variant is registered. The trade-level model has no slippage on winning exits, no
   per-side cost floor as in the common brief, no ceiling on how fast burned accounts are replaced, and the 1-trade-a-day result is
   decided by Apex's $200 qualifying-day rule; frame B carries none of the F2 stresses.
7. **No web access was used** and nothing was bought or contacted. No market data was read. N is unchanged (280 inherited + 0).
8. **Reproducibility**: the inherited `results.json` of the F2 run is not in the record (git-ignored), so the F2-12/F2-13 numbers
   here cannot be checked against the inherited run; the F2-09 replication job (T6) is the bridge: it re-creates the inherited
   S = 1.0 row from `tables.md` with the same seeds and the full grid. The copied inherited `.py` files duplicate worktree content
   (D-003); `f2_rerun/README.md` says how to drop them and keep only the hashes.

## 12. Files, commands, seeds, run times

Scratch folder (all runs): `/tmp/claude-0/-home-user-claude-skills/c1c15771-3f18-56a1-8828-ab24630be4a0/scratchpad/f2_rerun/`.
Delivered copy: `quant-edge/economics/f2_rerun/` (README with the layout, SHA256SUMS of the inherited copies, scripts, logs, raw
JSON outputs, `tables_rerun.md`).

| step (UTC, 2026-11-03) | command | jobs | CPU-min | wall-min | log |
|---|---|---|---|---|---|
| 14:35 | `pytest -q test_stress_model.py` / `pytest -q test_prop_model.py` | 21 + 14 tests | 0.15 | 0.15 | `logs/pytest_w3.log`, `logs/pytest_w1.log` |
| 14:35 | `python3 time_job.py` (F2-12, FTMO, S = 1.0, sigma ≤ 20% then full grid) | 2 | 1.6 | 1.6 | `logs/time_job.log` |
| 14:40–14:52 | `python3 run_f2_rerun.py --scen F2-12 F2-13 --S 1.0 1.5 2.0 2.4 3.0 --seeds 11 101 202 303 404 --n 3000 --sigmax 0.20 --procs 4` | 50 | 35.5 | 11.7 | `logs/run_rerun.log` |
| 14:52 | `… --S 3.5 4.0 --seeds 11` | 4 | 2.9 | 1.0 | same |
| 14:53 | `… --scen F2-09 --S 1.0 --seeds 11 --sigmax 0.40 --caps 0.12 0.15 0.20 0.30 0.40 --procs 1` | 1 | 1.8 | 1.9 | same |
| 14:55 | `… --seq --scen F2-12 F2-13 --S 1.0 1.5 2.0 2.4 3.0 3.5 4.0` (calendar chains, n = 2000, seed 21) | 42 | 2.5 | 0.7 | same |
| 14:44–14:54 | `python3 futures_frame.py` (frame A grid + frame B) | 158 + 30 | 9.8 | 10.1 | `logs/futures_frame.log` |
| 14:56 | `python3 futures_frame_1tpd.py` (8%-of-drawdown supplement) | 60 | 3.3 | 3.4 | `logs/futures_frame_1tpd.log` |
| 14:59 | `python3 make_rerun_tables.py` → `tables_rerun.md` | – | – | – | – |
| | **total** | | **57.6** | | |

Seeds: grid jobs eval 11 / funded 12 (F2's base pair) and F2-15's 101/102, 202/203, 303/304, 404/405; every job's seeds, sigma grid,
stress dictionary, firm dictionary, wall and CPU seconds are stored under `meta` in `results_rerun.json`; calendar chains seed 21
(eval 21, funded 22, chain 23); futures frame A seed 11, frame B seeds 11/12 (D1 defaults). Inherited code was not modified; the
new scripts call it through its public functions (`eval_sim`, `funded_sim`, `economics`, `capped`, `slot_years`, `simulate`) and
set only the module constant `TRADES_DAY` in frame A.
