# D1 red team: prop-firm economics (2026-10-11)

Target claim: at Sharpe 1.17 net, with vol capped at 12%, the best structures are FTMO Swing (4 x ~$7.0k per
account-year), HyroTrader (2 x ~$8.9k) and CFT (3 x ~$6.3k). ROS is >1000%, and it is >=20% even at S=0.
The binding limit is allocation caps, and the fleet makes ~$90-100k a year.

Starting verdict: REFUTED. **Final verdict: WEAKENED.** The structural point survives: ROS is not an edge
test, and caps bind. The ranking, the per-account dollars and the fleet number do not survive as stated.
Scripts are in the session scratchpad (`rt/`): `pm_fix.py` is a patched copy, `noises.py`, `run_rt.py`
and `t_sel.py`. The model files were not edited. All runs use n=2000 and are **exploratory, not
pre-registered**. The unpatched model at n=2000 matches results.json within about 4% (FTMO 7,295 vs
7,020; Hyro 9,035 vs 8,879).

## 1. Code bugs

**1a. Real bug: the daily-loss anchor ignores payouts (it makes the model more pessimistic).**
In `funded_sim`, `acc.end_day()` sets `day0 = bal` *before* the payout block runs, and the payout then
does `acc.bal -= w`. The next day's daily-loss floor is therefore `pre-payout balance - dll`. A withdrawal
larger than the daily limit (5% = $5k at FTMO/Hyro/CFT, 2% at Blue Guardian funded) breaches the account
on the first sub-step of the next day. Smaller withdrawals silently shrink the daily-loss room. Firms
measure the limit from the start-of-day balance or equity, which is already net of the withdrawal.
Fix tested: `acc.day0 -= w` after the payout. Funded sim, S=1.17, sigma 12%:

life in days / trader pay per account / breach share, orig -> fixed:
- FTMO (10-day cycle): 242 -> 431 / 14.4k -> 25.5k / 0.96 -> 0.74
- HyroTrader (5-day cycle): 347 -> 406 / 21.2k -> 24.8k / 0.86 -> 0.78
- CFT (15-day cycle): 184 -> 452 / 10.7k -> 26.2k / 0.99 -> 0.71

The bug punishes long payout cycles. It is the *only* reason HyroTrader ranks above FTMO and CFT.
Full economics, capped at 12%, n=2000, net per slot-year orig -> fixed: CFT 6,270 -> 9,858;
Hyro 9,035 -> 9,687; FTMO 7,295 -> 9,634; The5ers 6,442 -> 9,702; Breakout 6,274 -> 9,337;
Blue Guardian 3,392 -> 7,608.

Fleet (auto = yes or conditional) goes from 99k to **145k**. After the fix the top five static-10%-DD
firms are tied within MC noise (9.3-9.9k). There is no meaningful "best structure". The ranking in the
claim is a bug artifact. All dollar tables in results.txt and every min-Sharpe answer should be re-run.

**1b. Other mechanics checked; no inflating bug found.** The renewal-reward formulas
(`t_eval = t_fail(1-p)/p + t_pass`, matching fees, rate = E[reward]/E[length]) and the once-per-cycle
refund are correct. Full withdrawal above start (`payout_base=0`) matches firm rules; FTMO's
close-positions-to-claim cost is not modelled but small. Eval idle-after-target and min_days count phase
days, not days with a trade (harmless: a bot can open a token trade). Truncation at 756 days counts live
evals as failures and abandons live funded accounts (26% of FTMO survive in the fixed model), so it is
**conservative**. `lock_on_payout` (E8 only) is read correctly. Optimizer selection bias (best of 81
sigma cells on one seed), re-evaluated on seed 101: FTMO 7,295 -> 6,926 (-5%), Hyro 9,035 -> 8,634
(-4%), CFT 6,270 -> 6,228. A small upward bias; quoted figures sit at the top of their noise band.

## 2. Modeling assumptions

**2a. Sharpe 1.17 is not portable (the largest risk).** The 1.17 is a multi-asset trend book. FTMO CFDs
cover FX, indices, metals and energy, but no bond or STIR futures, and those carried much of trend's
historical edge. CFD financing markups (about 2-3%/yr on notional) come on top of the usual costs.
HyroTrader and CFT are crypto perps only: a few highly correlated coins plus funding payments. A
crypto-only trend Sharpe is a different, *unmeasured* number, so quoting 1.17 for Hyro/CFT has no
support.

Net per slot-year FTMO / Hyro / CFT, fleet (yes/cond): S=0.6 orig 4.1k / 5.0k / 3.7k, $57k;
S=0.6 fixed 5.3k / 5.4k / 5.6k, $80k; S=0.3 fixed 3.4k / 3.4k / 3.7k, $52k.

Because the fee option pays at any Sharpe (point 3), the structures stay positive. The *dollar* claim,
however, depends entirely on an unverified per-venue Sharpe.

**2b. The 12% cap sets the answer.** The optimizer picks sigma at the cap in every top firm
(0.12/0.12), so net per slot scales almost linearly with an arbitrary cap.

Fixed FTMO / Hyro / CFT, fixed fleet, orig fleet: cap 8% 5.2k / 5.3k / 5.4k, $86k, $71k;
cap 15% 12.2k / 12.2k / 12.6k, $179k, $110k.

In the unpatched model the leader also changes with the cap. At 15%: Hyro 9,967 > FTMO 8,004 > CFT
7,193. At 8%: Hyro 5,303 > FTMO 5,097 > Breakout 5,002 > CFT 4,917.
"About $7,000 per account" is a statement about the cap, not about the firm.

**2c. Tails and return dynamics have small effects (all with the fix).** df=3 tails: FTMO / Hyro / CFT
each about -5% (9.2k / 9.2k / 9.4k), fleet $134k. Vol clustering (log-vol AR(1), sd 0.35, half-life 1
month): about -6%. Persistent Sharpe regimes (+-1.0 or +-1.5 around 1.17, 6-month mean length): pass
rate 0.79 -> 0.69-0.74 but net unchanged or slightly up (9.7k-10.6k). Iid noise is *not* the weak point.

**2d. Rules not modelled.** Each item lists its likely direction of effect.
- FTMO: the EUR 439 promo applies only when no other $100K account is active. Accounts 2-4 cost list
  price, EUR 540 (~$630). Small, because fees are ~$330 per slot-year. Swing price parity is unverified.
- FTMO: positions must be closed to claim a payout.
- FTMO: no scaling plan and no 90% split. Both omissions understate FTMO.
- HyroTrader: "copy-trading and account mirroring prohibited". Running one bot on 2 Hyro accounts *and*
  on other firms is explicitly not covered. Treat it as a confiscation risk.
- HyroTrader: per-payout 5% cap (third-party source) is not binding on a 5-day cycle. Margin <=25% and
  notional <=2x are fine at 12% vol on crypto (~0.2-0.3x notional). The 40% best-day rule in eval is
  rarely hit at a 0.76% daily sd.
- CFT: fee unverified ($520/$598/$660). Whether the 5-day first payout applies to 2-Phase is
  unconfirmed. The $10k/day cap is not binding.
- Blue Guardian: the Shield (first trigger halves the split) is modelled as a hard breach at 2%, which
  is conservative. Its number is heavily hit by bug 1a (3.4k -> 7.6k).

**2e. Firm failure and payout denial.** I added a 15%/yr hazard that kills a funded account with no
payout, which approximates firm collapse or a withdrawal denial (the 2024 wave: MFF, True Forex Funds and
others). Result with the fix: FTMO 8.8k, Hyro 8.9k, CFT 9.0k, fleet $134k (-7%). This is modest per
slot, but the hazard is *common* across a fleet that copies one strategy. Detection of identical trades
by a shared risk vendor could hit several firms at once, and the model has no such term.

**2f. Year one is not steady state.** Sequential sim (`slot_years`, unpatched), years 1 / 2 / 3: FTMO 3.1k / 7.0k / 7.3k;
Hyro 3.4k / 8.7k / 9.6k; CFT 2.4k / 6.6k / 6.6k.

P(year 1 < 0) is 0.42-0.45 per slot, because an evaluation at 12% vol takes about 1 year (256 expected
days including re-buys). A "$90-100k a year" fleet is roughly **$40-45k in year 1**. With every
account copying one strategy, P(year 1 < 0) is close to 0.4 for the whole fleet, not just one slot.

## 3. Verdict by sub-claim

| sub-claim | verdict | reason |
|---|---|---|
| Best = FTMO / Hyro / CFT, Hyro on top | **REFUTED as a ranking** | Hyro's lead is a daily-loss bug. Fixed: CFT ~ Hyro ~ FTMO ~ The5ers ~ Breakout within noise. Unpatched: order flips with the cap. Call it "a tie among static-10%-DD 2-step firms"; choose on rule risk (copying, confiscation, fee). |
| ~$7.0k / $8.9k / $6.3k per account-year | **WEAKENED** | Bug fix: ~9.6-9.9k. Cap 8%: ~5.3k; cap 15%: ~12.4k. S=0.6: ~5.4k. These are cap- and Sharpe-assumption outputs, quoted pre-tax and in steady state. |
| ROS >1000%, >=20% even at S=0, so the bar is not an edge test | **SURVIVES** | The static-DD free option is real mechanics: about split x DD per funded life at zero edge. The bug fix only strengthens it. The real risk at low edge is payout denial, not the arithmetic. |
| Binding constraint is the per-person allocation cap | **SURVIVES (qualified)** | Cap x the Sharpe that can be carried to each venue. Copy and mirroring clauses (Hyro, CFT, FundedNext, FTUK) may cut usable slots. |
| Fleet ~$90-100k/yr at S=1.17 | **WEAKENED** | With the bug fixed the model says ~$145k. At an honest venue Sharpe of 0.6, $57-80k. Year 1 is ~45% of steady state. Common-mode firm risk is not modelled. |

## Required before publishing
(1) Fix the payout/day0 bug and re-run D1-01..05. (2) State the per-venue Sharpe (FX/CFD subset,
crypto-only) instead of reusing 1.17. (3) Report caps of 8, 12 and 15%. (4) Report year-1 cash separately
from steady state. (5) Rank firms on rule and counterparty risk, since the economics are tied.
