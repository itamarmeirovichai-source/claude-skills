# Inherited economics: what the target needs (Scribe, 2026-11-03)

Paths: PF=`~/quant-edge-inherited/pr4/skills/prop-fleet`, R=`PF/references`, V=`PF/agents/daily/w3-volrisk`, X=`PF/agents/daily/2026-10-05`. Target (11 Oct): $20,000 a year net per $100,000 funded, fleet-averaged with failed accounts (`PF/agents/wave-2026-10-11.md`).

## Required net Sharpe for $20k per slot-year, pre-tax (`V/tables.md` "Sharpe needed")
- FTMO Swing 2-Step 100K: F2-01 baseline 2.42 @12% vol, 1.88 @15%, 1.42 @20%, 0.96 @30%, 0.69 uncapped; F2-09 (all stresses) 2.42 / 1.92 / 1.46 / 0.94 / 0.69.
- Blue Guardian F2-09: 3.10 / 2.76 / 2.46 / 1.98 / 1.75 (4% DLL plus Guardian Shield). CFT F2-09: 2.52 / 2.06 / 1.70 / 1.47 / 1.42 ($10k/day cap binds above 20%).
- FTMO F2-09 net $/slot-yr at 12/15/20% vol: S=1.0 $7.5k/9.9k/13.6k; S=1.5 $11.7k/15.2k/20.6k; S=2.0 $16.1k/20.9k/28.2k. 15–20% vol is defensible under the contracts, 30%+ is not (`R/w3-volrisk.md`).

## F2-09 versus F2-12 (why 1.5 at 20% is a floor, not a fact)
- F2-12..15 were registered after the model red team to REPLACE F2-09 as the decision row (`PF/agents/prereg/F2.csv`), but `V/make_report.py` prints only F2-01 and F2-09; F2-12 numbers exist only in `V/results.json` (unread, 134 KB) (`R/w3-volrisk.md`).
- What F2-12 corrects (`V/redteam-model.md`): a day summed from 24 t3 shocks is near-Gaussian (DLL breach at 20% vol 18% → 6%); the GARCH cap leaves σ ≈ 0.89σ, effective Sharpe ≈ 1.12 S; the forced 10%/day closed-balance lag costs FTMO/CFT 35–50% of funded pay at 20% vol; a bot guard at −1.6% raises Blue Guardian pay 64%.
- At 15–20% vol F2-12 should need somewhat less Sharpe than F2-09 at FTMO and CFT; the Economist re-run (`briefs/F-economist-f2-12.md` → `economics/required-sharpe-2026-11.md`) is the authority.

## The zero-edge lottery
- D1's uncapped optimiser runs to 25–40% vol; at S=0 an FTMO slot pays $1.8k (12% cap), $5.0k (20%), $11.1k (no cap) a year (`R/w1-synthesis.md` table); 14 of 16 programmes clear 20% ROS on fees at S=0, so return on fees is not an edge test (`R/w1-prop.md` D1-05).
- Stressed: F2-09 S=0 FTMO $1.2k @12%, $2.9k @20%, $9.1k uncapped; calendar chain F2-10 year-1 mean −$0.2k, p10 −$1.5k, P(loss) 84%; uncapped year-1 p10 −$8.7k (`V/tables.md` F2-10). Negative skew pays less ($641 vs $1,043); CPPI sizing pays less (S=1.5 $11.7k vs $17.8k) (`R/w1-synthesis.md` 12 and 16 Oct).

## Futures-firm frame: R per trade × trades per day, always both
- Apex-era model (3 trades/day, 1:2, 4% of drawdown, 25% tax, 20 × 50K): 20% a year needs +0.250R per trade; +0.182R at 8% of drawdown (`R/numbers.md` "What the goal costs"). Measured bot edge +0.101R, clustered 95% [−0.197, +0.398].
- Planning fleet P1 Bulenox 5 + Topstep 5 ($500k nominal, R net of costs): +0.28R at 3/day or +0.78R at 1/day; if both firms' exits bite after 3 payouts, +0.52R at 3/day and never at 1/day (`X/prop_head/structure_run.txt`).
- Sharpe at 2:1 over 250 days: +0.10R → 1.09 (1/day) or 1.89 (3/day); +0.25R → 2.67 / 4.63; +0.50R → 5.27 / 9.13 (`X/redteam/sharpe_needed.txt`).
- Screening rule: plausible gross ≥ 0.15R at stops ≥ 15 ES pt (0.6 pt RT = 0.04R), or several trades a day with positive net (`PF/agents/board.md` Decision 5).

## Tax note
- Classification moves the required edge by about a third: at 20 × 50K and 4% of drawdown, +0.249R at 25% (capital gain), +0.339R at 47% (business income), +0.379R at 53% (with National Insurance), +0.441R at 60% (`R/numbers.md` "The classification decides the target"); over 8 years at +0.30R the gap is $507,154 (`PF/scripts/claims.py`).
- Every fact points to business income (nothing owned or sold, simulated account, payment for a result, daily automation): reserve at the higher rate from each payout. VAT: export of services may be zero-rated under s.30(a)(5); a mistake costs 18% of gross (`R/numbers.md` Tax; `R/verification-letters.md` §2 is the accountant letter).
