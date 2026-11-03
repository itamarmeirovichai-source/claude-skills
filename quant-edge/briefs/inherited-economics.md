# Inherited economics: what the target needs (Scribe, 2026-11-03)

Paths: PF=`~/quant-edge-inherited/pr4/skills/prop-fleet`, R=`PF/references`, V=`PF/agents/daily/w3-volrisk`, P=`PF/agents/daily/w1-prop`. Target since 11 Oct: $20,000/yr net per $100,000 funded, fleet-averaged incl. failed accounts (`PF/agents/wave-2026-10-11.md` "Itamar's decision").

## Required net Sharpe for $20k per slot-year, pre-tax (`V/tables.md` "Sharpe needed")
- FTMO Swing 2-Step 100K: F2-01 baseline 2.42 @12% vol, 1.88 @15%, 1.42 @20%, 0.96 @30%, 0.69 uncapped; F2-09 (all stresses) 2.42 / 1.92 / 1.46 / 0.94 / 0.69.
- Blue Guardian: F2-09 3.10 / 2.76 / 2.46 / 1.98 / 1.75 (4% DLL + Guardian Shield). CFT: 2.52 / 2.06 / 1.70 / 1.47 / 1.42 ($10k/day cap binds above 20%).
- Net $/slot-yr FTMO F2-09 at 12/15/20% vol: S=1.0 $7.5k/9.9k/13.6k; S=1.5 $11.7k/15.2k/20.6k; S=2.0 $16.1k/20.9k/28.2k. Volatility 15–20% is defensible under the contracts, 30%+ is not (`R/w3-volrisk.md`).

## F2-09 vs F2-12 (why the common brief calls 1.5 a floor)
- F2-12..15 were registered after the model red team to REPLACE F2-09 as the decision row (`PF/agents/prereg/F2.csv`), but `V/make_report.py` prints only F2-01/F2-09; F2-12 figures sit in `V/results.json` (134 KB, not loaded here). The run "stopped mid-run" and was finished by the director (`R/w3-volrisk.md` Sources).
- Red-team findings F2-12 corrects (`V/redteam-model.md`): a day summed from 24 t3 shocks is near-Gaussian (DLL breach at 20% vol 18% → 6% with more checks); the GARCH cap makes σ ≈ 0.89σ, effective Sharpe ≈ 1.12 S; the forced 10%/day closed-balance lag is a bot choice and costs FTMO/CFT 35–50% of funded pay at 20% vol; a bot guard at −1.6% raises BG funded pay 64%; the $250 rule-(b) threshold is below Monte Carlo s.e. at caps ≥ 15%.
- Net direction: at 15–20% vol F2-12 should need somewhat less Sharpe than F2-09 at FTMO, more at BG; the Economist re-run (`briefs/F-economist-f2-12.md` → `economics/required-sharpe-2026-11.md`) is the authority, not this brief.

## The lottery (zero edge)
- D1 uncapped optimiser picks 25–40% vol everywhere; S=0 pays $1.8k (12% cap), $5.0k (20%), $11.1k (no cap) per FTMO slot-year (`R/w1-synthesis.md` table); 14 of 16 programmes clear 20% ROS on fees at S=0, so "20% on money spent" is not an edge test (`R/w1-prop.md` §2, D1-05).
- Stressed: F2-09 S=0 FTMO $1.2k @12%, $2.9k @20%, $9.1k uncapped; calendar chain F2-10 year-1 mean −$0.2k, p10 −$1.5k, P(loss) 84%; uncapped year-1 p10 −$8.7k (`V/tables.md` F2-10). Negative skew pays less ($641 vs $1,043); CPPI/barrier sizing pays less (S=1.5 $11.7k vs $17.8k) (`R/w1-synthesis.md` 12 and 16 Oct).
- Fleets at S=1.17, 12% cap: FTMO $9,398 × 4, BG $7,352 × 4, CFT $9,644 × 3 = $95.9k/yr, p10 $20.6k, year-1 $40k; five static-DD structures tie at $9.2–9.6k (`R/w1-prop.md` §2–3). That is 8.7% of $1.1M notional.

## Futures-firm frame: R per trade × trades per day (always report both)
- Apex-era model (3 trades/day, 1:2, 4% of drawdown, 25% tax, 20 × 50K): 20%/yr needs +0.250R/trade; +0.182R at 8% of DD (triples burn) (`R/numbers.md` "What the goal costs"). Measured bot edge +0.101R, clustered 95% [−0.197, +0.398].
- Planning fleet P1 Bulenox 5 + Topstep 5 ($500k nominal, R net of costs): +0.28R at 3/day or +0.78R at 1/day; if the firms' exits bite after 3 payouts, +0.52R at 3/day and never at 1/day up to +1.50R (`PF/agents/daily/2026-10-05/prop_head/structure_run.txt`).
- Sharpe implied at 2:1, 250 days: +0.10R → 1.09 (1/day) / 1.89 (3/day); +0.25R → 2.67 / 4.63; +0.32R → 3.40 / 5.88; +0.50R → 5.27 / 9.13 (`.../redteam/sharpe_needed.txt`). A 21-day evaluation ($3k target, $2k DD) is a volatility lottery: SR 1 at $500/day vol passes 23%, blows 40%; SR 3 41%/23%; SR 5 62%/11% (`R/stack.md` §3).
- Screening rule for intraday candidates: plausible gross ≥ 0.15R at stops ≥ 15 ES pt (0.6 pt RT = 0.04R), or several trades/day with positive net (`PF/agents/board.md` Decision 5). Detection: +0.25R needs 39 days-with-a-trade for a two-sided bound, 114 at the gate's z (`.../statistician/audit_run.txt`).
- Costs in R: MES $1.30 RT + 0.25 pt slip (apex_model); ES 0.6 pt RT = 0.21R on TJR's 3.2-pt stops (`R/tjr.md`); the Nov 2026 all-in ES ≈ $2.0–2.7/side plus a tick (`~/quant-edge-inherited/pr26/prompts/research/lit-practitioner.md` Cost facts).

## Tax note
- Classification moves the required edge by about a third: at 20 × 50K and 4% of DD, +0.249R at 25% (capital gain), +0.339R at 47% (business income), +0.379R at 53% (plus National Insurance, unverified), +0.441R at 60% (`R/numbers.md` "The classification decides the target"). Over 8 years at +0.30R the gap is $507,154 (24.6% vs 17.4%/yr; `scripts/claims.py` recomputes it).
- Every fact argues for business income (nothing owned or sold, simulated account, contractual payment for a result, daily automated activity); plan on the higher rate and reserve it from each payout. VAT: export of services may be zero-rated under s.30(a)(5); a mistake is 18% of gross (`R/numbers.md` Tax; `R/verification-letters.md` §2 is the accountant letter).
