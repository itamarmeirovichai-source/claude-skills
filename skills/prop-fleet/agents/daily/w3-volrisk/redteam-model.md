# F2 red team: stress model (wave 3)

Date: 2026-10-12. Scope: `stress_model.py`, `scenarios.py`, `run_f2.py`, `make_report.py`, `agents/prereg/F2.csv`, and the clause files.
No repo file was edited. All experiments are in `/tmp/claude-0/f2-redteam/` (e1–e12). They use n ≤ 300 and few sigmas, so their $ figures have Monte Carlo noise of several hundred $/slot-yr. Most use common random numbers (CRN): the switch being compared does not consume the RNG, so the *differences* are much tighter than the levels.

"$/yr" below means pre-tax net $ per slot-year (renewal reward), at S = 1 unless stated.

## Summary

| # | Severity | Finding | Direction on $/slot-yr | Rough size |
|---|---|---|---|---|
| 1 | **bias (large)** | The closed-balance lag `real_rate = 0.10` is forced on every firm-exact scenario. It is a bot-design choice, not a firm rule. | Pessimistic for high vol (FTMO, CFT, BG in F2-07/09/10/11) | FTMO funded pay at 20%: −35%; CFT −51%; BG roughly halved |
| 2 | **bias (large)** | CFT $3,333/day cap × lagged balance: profit carried from earlier days is confiscated | Pessimistic for CFT at caps ≥ 20% | Best $/yr 8.5k vs 16.0k with daily realisation (17.9k with no cap) |
| 3 | **bias (large)** | The bot has no open-P&L guard ahead of the Guardian Shield | Pessimistic for BG funded | Best $/yr 5.3k → 8.7k (+64%) with a −1.6% guard |
| 4 | **bug / confound** | The daily return is the sum of `sub` t-shocks, so raising `sub` to 24 makes daily returns nearly Gaussian | F2-06 understates stress; F2-09 partly undoes t3 | 1-yr DLL breach at 20% vol: 18% (sub 4) → 6% (sub 24) → 3% (sub 96) |
| 5 | **bug (small)** | The GARCH cap at hmax = 16 breaks E[h] = 1 (realised variance −20% under t3) | Mixed at S = 1; understates the S = 0 lottery | S = 1 within ±5%; S = 0: −10 to −20% |
| 6 | **bug (tiny)** | Day after a payout with `dll_ref = "balance"`: the DLL reference is the old lagged closed balance minus the payout | Mixed (CFT slightly pessimistic) | < 3% of pay |
| 7 | **note** | The kill switch is perfect (no slippage or cost). At sub = 4 (F2-03/04) it is crippled by discretisation. | F2-03/04 understate the kill switch; F2-09 may overstate it | see §7 |
| 8 | **note** | The rule (b) threshold of $250 is not "2 s.e." at the caps that matter | Max safe vol biased upward | s.e. of a cap gain is ≈ $300–1,000 |
| 9 | **note** | Smaller items: gap hits flat books, CFT 7-day calendar, CFT DLL base, horizon truncation, BG min-profit days, σe ≠ σf | Mostly pessimistic for CFT, mixed elsewhere | small each |
| 10 | **note** | `make_report.py` does not apply rule (a), the F2-11 verdict, or the "breach share alongside" clause | Process | — |

What checks out:
- The 16 tests pass.
- `stress=None` reproduces D1 bit for bit for eval, funded and the economics grid.
- The gap/weekend construction keeps annual variance: 0.998 of σ².
- Drift is right: 0.049 per day measured vs 0.05 expected, including under GARCH.
- t3 scaling gives unit variance: 0.996.
- GARCH `z` is computed from the whole market move, gap included. `h` is applied to the next day.
- Kill switch and shield are excluded on steps where the account already died. Halted accounts get zero increments for the rest of the day.
- The gap lands before the first check and does not bypass it.
- `closed` is set to equity on kill, shield and payout.
- The firm parameters match the clauses:
  - FTMO: 5% DLL from the 00:00 balance, checked on equity; refund with the 1st reward.
  - BG: funded DLL 4% from the higher of balance and equity, in eval and funded. Shield −2% of initial on open P&L, funded only. Cut split 0.5 × 0.97 for the account's life, applied to all later payouts. Breach on the 2nd trigger. Refund after the 4th payout.
  - CFT: $660, no refund, DLL referenced to balance, $10k per user / 3.

---

## 1. `real_rate = 0.10` drives the firm-exact results (bias, large, pessimistic for high vol)

The code:
- `scenarios.scen_stress` sets `real_rate = 0.10` for every exact scenario whose DLL reference is not "equity", i.e. all three firms.
- F2-09 inherits the same lag from DLLEQ.
- With a 10%/day realisation, open P&L has a memory of about 10 days, with stationary s.d. ≈ 2.3 × daily s.d. That hurts in three ways:
  - balance-referenced DLLs (FTMO, CFT) start the day with carried floating losses already counted;
  - the Shield (BG) fires on accumulated open P&L;
  - the CFT cap confiscates carried gains (§2).

The firms impose none of this. It is how the bot chooses to hold positions. A bot can flatten or re-strike before 00:00 CE(S)T, 00:05 UTC or 5 pm EST. That realisation costs spread, which is NOT modelled, so the truth lies between the two settings.

Experiment e5: F2-07 rules, funded only, n = 300, CRN.

| firm (ref) | real_rate | breach before 1st payout at 8/12/20% | pay $ at 8/12/20% | life (days) at 8/12/20% |
|---|---|---|---|---|
| FTMO (balance) | 0.10 | .01/.05/.20 | 20.1k/21.7k/10.3k | 620/379/83 |
| FTMO (balance) | 1.00 | .01/.04/.13 | 20.1k/23.2k/16.0k | 621/414/146 |
| CFT (balance) | 0.10 | .02/.06/.25 | 19.7k/20.5k/8.0k | 624/389/80 |
| CFT (balance) | 1.00 | .02/.05/.16 | 19.8k/23.5k/16.4k | 626/430/162 |
| BG (max + Shield) | 0.10 | .05/.12/.32 | 7.8k/4.8k/3.5k | 206/65/25 |
| BG (max + Shield) | 1.00 | .02/.08/.29 | 17.1k/10.6k/3.4k | 490/180/30 |

Effect on $/slot-yr:
- Small at 8%.
- About −7% of funded pay at 12%, and −35 to −50% at 20%.
- So F2-07/F2-09 push the optimum toward lower vol, and the low-cap numbers look relatively better.

The prereg covers BG with F2-08 (real_rate = 1.0) but FTMO and CFT have no counterpart.

Recommendation: also report F2-07/F2-09 at real_rate = 1.0 for FTMO and CFT, with a daily spread cost, or treat realisation as a bot decision.

## 2. CFT profit cap measured from the lagged closed balance (bias, large, pessimistic for CFT)

How the code applies the cap:
- `Account.end_day` cuts `bal` to `day0 + cap`.
- For CFT, `day0` is the closed balance, which lags by 10%/day.
- So equity that is up 5.4k on the closed balance is cut to +3.3k, even on a day when the market did not move. Profit earned on earlier days is deducted.

The literal clause supports measuring from the balance: "difference calculated based on the simulated balance at 12:10 AM UTC" (clauses-cft.md l.43–45). But a bot that realises gains before 00:10 UTC loses nothing under the same rule.

Experiment e9 / e9b: F2-07 CFT, n = 300, S = 1.

| setting | $/yr on the diagonal at 12/20/30/40% | best $/yr (σe, σf) |
|---|---|---|
| cap 3,333, real_rate 0.10 (as modelled) | 7.5k / 7.1k / 0.8k / −6.5k | 8.5k (20, 12) |
| cap 3,333, real_rate 1.0 | 8.2k / 13.3k / 14.8k / 8.9k | 16.0k (40, 20) |
| no cap, real_rate 0.10 | 8.2k / 12.1k / 15.0k / 17.1k | 17.9k (40, 30) |
| no cap, real_rate 1.0 | 8.2k / 14.3k / 20.2k / 21.0k | 23.6k (40, 30) |

Smaller second-order issues:
- The real rule is enforced intraday ("once the equity reached $10,000 … trades closed"). The model applies it at day end, so a day that touches the cap and falls back keeps the loss. This is pessimistic, but small.
- The "per trade" aggregation is not modelled. This is optimistic.

## 3. No bot-side guard before the Guardian Shield (bias, large, pessimistic for BG)

The model's bot never manages open P&L, so the firm's Shield always fires first. That cuts the split to 48.5% and breaches on the second trigger.

A bot can instead flatten itself at, for example, −1.6% open P&L. That does not count as a Shield trigger. The economic action is the same, without the penalty.

Experiment e8: F2-07 BG, sub = 4, n = 300. A subclass flattens at 0.8 × level.

| | Shield triggers per account at 5/8/12/15/20% | funded pay $ | best $/yr |
|---|---|---|---|
| model | .66/1.98/1.99/1.96/1.90 | 12.0k/6.9k/4.4k/3.9k/3.8k | 5.3k |
| bot guard at −1.6% | .12/.86/1.42/1.57/1.55 | 13.1k/14.8k/8.6k/7.7k/6.4k | 8.7k |

At sub = 24 (F2-09) the guard would catch more, since fewer steps jump past it.

A caveat on scope: whether BG would treat a funded-only guard as a "strategy switch" is a clause question, not a model question.

## 4. Sub-step aggregation thins daily tails (bug / confound)

`Market.day` draws `sub` independent unit-variance t(df) shocks per day. The daily return is their sum, so its excess kurtosis is about 6/((df−4)·sub) for df > 4.

Raising `sub` from 4 to 24 therefore does two things at once:
- adds monitoring, as intended;
- makes daily returns nearly Gaussian, which was not intended.

Experiment e12: daily-move tails, 10⁶ days.

| market | excess kurtosis | P(< −4 s.d.) | P(< −5 s.d.) |
|---|---|---|---|
| normal | 0 | 3.2e-5 | 2.9e-7 |
| D1 / F2-01 (t5, sub 4) | 1.3 | 6.8e-4 | 2.0e-4 |
| F2-02 (t3, sub 4) | 80 | 2.1e-3 | 9.9e-4 |
| F2-06 (t5, sub 24) | 0.2 | 1.3e-4 | 1.7e-5 |
| t3, sub 24, no gaps | 10 | 1.1e-3 | 4.4e-4 |
| F2-09 market (t3, gaps, sub 24, no GARCH) | 18 | 1.6e-3 | 7.7e-4 |

Experiment e11: FTMO funded with max loss removed, so only DLL breaches count, no kill. P(DLL breach within 1 year) at 20% vol:

| sub | P(DLL breach) |
|---|---|
| 4 | 0.18 |
| 24 | 0.06 |
| 96 | 0.03 |

More checks gave fewer breaches, because the tails shrank.

Effect on the scenarios:
- F2-06's "24 checks a day" makes the DLL safer, not stricter. Its 5-s.d. daily tail is 12× thinner than D1's. F2-06 therefore understates its own stress.
- In F2-09, t3 and the gap keep the tails fatter than D1, but thinner than F2-02 alone.

Fix: draw one daily t-shock and spread it over the sub-steps with a Brownian bridge or a Gaussian partition. Then the daily law does not depend on `sub`.

## 5. GARCH variance deficit from the h cap (bug, small $)

The docstring and prereg say E[h] = 1. The cap `min(…, hmax = 16)` removes the rare high-h episodes, so E[h] < 1. The deficit is severe with t3 shocks, whose infinite fourth moment drives h to the cap.

Experiment e1/e1b: 2,520 days × 400 paths.

| case | realised daily var / nominal | E[h] |
|---|---|---|
| t5 GARCH | 0.965–0.978 | 0.97 |
| t3 GARCH | 0.77–0.78 | 0.78 |
| ALL (F2-09 market) | 0.80–0.82 | 0.81–0.83 |
| first year only, t3 | 0.79 | 0.80 |
| t3 with hmax = 1e9 | 1.03 | 1.03 |

So F2-09's "σ" is really about 0.89σ. Because the drift is unchanged, the effective Sharpe is about 1.12 S. Multiplying the GARCH intercept by 1.25 restores E[h] ≈ 1.00 (e6).

Dollar effect (e6b/e6c, F2-09, n = 300, CRN):

| case | as modelled | fixed |
|---|---|---|
| FTMO S = 1, best | 12,954 | 13,271 |
| CFT S = 1, best | 10,536 | 10,000 |
| FTMO S = 0, (40, 40) | 8,200 | 9,710 |

So at S = 1 the effect is within ±5%, with mixed sign. At S = 0 the variance deficit understates the "lottery" by 10–20%.

Separate observation: FTMO under F2-09 at S = 0 is clearly positive (about +$8k/yr at 40/40, n = 300). The F2-11 lottery check is likely to hinge on the calendar median rather than on renewal reward.

## 6. DLL reference on the day after a payout (bug, tiny)

The code (`funded_sim` l.278–282) does three things on a payout:
- sets `closed = bal`, since positions are closed for the payout;
- subtracts the payout `w` from `bal` and `closed`;
- applies `day0 -= w`.

But `day0` was set in `end_day` from the *old*, lagged closed balance. For "balance" (FTMO, CFT) the next day's reference is therefore `old_closed − w` instead of the new closed balance (e3):

| | value |
|---|---|
| bal 106,000, closed 100,600, payout 6,000 | |
| next-day DLL floor in the model | 89,600 |
| floor under the firm rule | 95,000 |

For "max" the value is right when equity is above closed.

Patched run (e10, F2-07, n = 300):
- FTMO is unchanged.
- CFT pay rises about 1–3%, because the lower `day0` also made the CFT cap confiscate more.

Fix: recompute `day0` from the post-payout `bal`/`closed` according to `dll_ref`.

## 7. Kill switch: perfect execution, but discretisation decides how good it is (note)

How it works in the model:
- The kill switch flattens at the checked price, with no slippage, spread or latency.
- It protects only the DLL. A real bot would also guard the max-loss floor and the Shield (§3).

How effective it is depends almost entirely on `sub`. Experiment e11, P(DLL breach within 1 year) at 20% / 30% vol:

| sub | no kill | kill 0.8 |
|---|---|---|
| 4 | .18 / .80 | .12 / .67 |
| 24 | .06 / .77 | .007 / .23 |
| 96 | .03 / .79 | .00 / .01 |

So:
- F2-03 and F2-04 run at sub = 4. A single sub-step has s.d. of half a day, so it often jumps from above 80% to past 100% of the DLL. These are discretisation artefacts, not gaps. F2-04 understates the kill switch's value, and F2-03 overstates gap damage. Both share the artefact, so their difference is less affected.
- F2-09 runs at sub = 24, where the kill switch is effective, so the gaps are what matter.
- Optimism: execution is perfect, and the switch stays flat only until midnight.
- Pessimism: the account goes back on at the next open and takes the overnight gap (§9a).

## 8. MC noise, selection bias and rule (b) (note)

Experiment e7: FTMO F2-01, S = 1, σ ∈ {8 … 40}%, 6 seeds at n = 300, scaled to n = 3,000.
- Cell s.e. on the diagonal is $50–70 for σ ≤ 12%, but $200, 360, 140, 380 and 760 at 15, 20, 25, 30 and 40%.
- Each σ row uses independent draws, since `rng.standard_t(size=(k, n))` gives no CRN across σ. So the s.e. of a cap-to-cap gain is about √2 × that, roughly $300–1,000 for steps from 15% upward.
- The prereg's "$250 ≈ 2 MC s.e." holds only below 15%. Rule (b) is therefore permissive and biases the "max safe vol" upward. This matters most under F2-09, where the gains are small.
- `capped` maximises over nested sets, so gains are ≥ 0 by construction. Any noise can only count as a gain.
- Winner's curse from the 196-cell argmax: about $250 at n = 300 for caps 30/40, so about $80 at n = 3,000. Negligible next to §1–4.
- Under F2-01 the optimum sits at the cap corner for every cap. Per-seed gains are 12→15: $2.0–3.3k, 15→20: $2.2–6.1k, 20→30: $4.2–6.2k.

## 9. Smaller items (notes)

a. **Gap hits books that were flat overnight.**
- After a kill, shield or payout flatten, `halted` is reset at `end_day`. The next day's opening jump is then applied to the account.
- A bot that re-enters after the open would miss that gap.
- Slightly pessimistic for F2-03 and F2-09.

b. **CFT calendar.**
- The clause file assumes a crypto book on 365 days. CFT's DLL resets every calendar day, including weekends.
- The model uses 252 days with weekend gaps, so each DLL window carries √(365/252) = 1.2× the daily s.d.
- Pessimistic for CFT at high vol. The prereg acknowledges it ("conservative for CFT").

c. **CFT DLL base.** T&C §8 i says "5% of your balance at 12:05 AM UTC". The model uses 5% of the initial balance. The difference is about ±0.25% of equity: negligible.

d. **Renewal-reward horizon.**
- Funded lives are cut at 756 days. Survivors forfeit their future payouts and must buy a new evaluation.
- Low-vol accounts survive (FTMO 8%: life 620/756), so low vol is penalised a few % relative to high vol.

e. **BG payout eligibility.** The 3 days of ≥0.5% profit, possibly required again in each cycle, are not modelled. This is optimistic. The "read-only until approved" period is not modelled either.

f. **σe ≠ σf.**
- The optimiser may pick different vols for eval and funded, e.g. CFT (20, 12) in e9.
- BG's T&C flags "one strategy to pass … a different strategy in a funded account".
- The report's fixed-vol diagonal helps. Rule (a) should look at it.

g. **Kill vs Shield on the same step.** The kill switch is evaluated first, so a step that crosses both is counted as a kill, not a Shield hit. This is optimistic, but rare.

h. **Common random numbers across scenarios.**
- Gaps (an extra jump draw) and df = 3 change the RNG stream. So F2-02, F2-03 and F2-09 vs F2-01 deltas carry full MC noise.
- F2-04, F2-05, F2-06 (sub aside), F2-07 and F2-08 share F2-01's stream.

## 10. `make_report.py` vs the prereg decision rules (note)

- **Rule (a)** (no clause breach, clause reader does not rate c high-risk) is not encoded.
  - The clause files would cap BG below 15%: the Shield is rated BREACH at 15/20/30%.
  - They would cap FTMO at ≤ 20%: 30% is "BREACH likely".
  - For CFT, 30% is "not recommended".
  - The rule (b) table alone will suggest higher caps than the prereg allows.
- **Rule (b)** is computed correctly: F2-09, S = 1.0, gains from 12→15, 15→20 and 20→30. But see §8 on the threshold. The prereg asks for the breach-before-first-payout share "alongside". It exists in `results.json` (`caps[*].breach_pre1`) but is not printed in that table. Only the fixed-vol table shows it.
- **F2-11 lottery verdict** (positive renewal-reward net at S = 0, uncapped, AND positive years-2–3 median) is not computed. Both ingredients are printed. The run does use the F2-09 (σe, σf) at cap 0.40, as the prereg requires.
- The "need" interpolation and the per-stress delta tables are coherent with the prereg. F2-08 appears only for BG, correctly.

## Net assessment

The code is mostly faithful to its spec, and `stress=None` exactly reproduces D1.

The large effects are modelling choices, and all of them push the firm-exact results against high vol:
- the forced 10%/day closed-balance lag (§1), which costs FTMO and CFT 35–50% of funded pay at 20% vol;
- its interaction with the CFT cap (§2), worth about 2× on CFT's best $/yr;
- the missing pre-Shield guard (§3), worth about 1.6× on BG.

Against that, F2-06's 24 checks make daily returns more Gaussian (§4). Rule (b)'s $250 bar is permissive at high caps (§8).

The genuine bugs (§5 GARCH cap, §6 post-payout DLL reference) move $ by less than 5% at S = 1.

Recommended additions before conclusions are drawn:
1. Run F2-07 and F2-09 at real_rate = 1.0 with a spread cost, for FTMO and CFT.
2. Run BG with a bot-side guard.
3. Fix the sub-step tail confound (§4) and the GARCH intercept (§5).
4. Raise the rule (b) threshold to about 2√2 × the cell s.e. at the relevant σ, or about $800.
