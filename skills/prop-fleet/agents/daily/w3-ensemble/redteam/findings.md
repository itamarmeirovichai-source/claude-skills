# F1 red team: findings (wave 3, equal-risk stack)

Written by the F1 red-team sub-agent on 2026-10-12. Saved here by the head, because the sub-agent could not write .md files. Every number comes from the scripts in this folder: `rt_rebuild.py`, `rt_orig.py`, `rt_analysis.py`, `rt_extra.py` and `rt_splice.py`, with outputs in `*.txt`. These are diagnostics of F1-01's fixed positions. No new variant was run.

**Verdict: the FAIL stands.** No look-ahead, timing or statistics bug flatters the stack, and no cost or weighting error hides an edge.
- The most generous diagnostic is zero cost on both sleeves plus the ex-post best fixed weight. It reaches t 2.20, against a bar of 3.5745.
- The bar needs +7.92 bp/day at the stack's vol, which is Sharpe 1.95. The stack's gross Sharpe is 1.16.

## 1. Look-ahead and timing: no error found

- **Truncation test.** A re-run of the head's `truncation.py` passes: all 50 cuts are identical (`trunc_rerun.txt`).
- **Risk weights k.** An independent recomputation equals the head's k on every day. Neither timing change helps:
  - a look-ahead k (data through the current month end) gives t 0.62;
  - a k one month staler gives t 0.43;
  - the headline is 0.74.
- **Margin scaling.** It uses that day's units > 0, which is conservative. It never binds: maximum margin 0.552, and 0 capped days.
- **UTC crypto day vs the NY session.** The NY session falls inside the same UTC date, so the alignment is correct. The S1–S2 correlation at lags −1, 0 and +1 is −0.018, +0.001 and −0.038.
- **1m/5m splice.**
  - The 5m bars are the 1m bars resampled and labelled by bar open: 95.6% of OHLC values match exactly (`bar_check.txt`).
  - Per-session S2 correlation is 0.98, with a mean difference of −0.25 bp (t −0.34).
  - Using 5m S2 over the whole window gives t 0.71, against 0.74 with the splice.

## 2. FTMO cost model: correct as read, and no plausible cost rescues the stack

- **What FTMO publishes.** The live symbol table confirms all 30 crypto CFDs at swap −30/−30 "percentage", commission 0.065% per side and Swing leverage 1:1.
  - `usdCommission` is consistent with 0.065% per side charged on the round turn.
  - US100.cash has 0 commission. Its swap does not matter, because S2 is flat before the rollover.

| Cost assumption (k fixed) | Stack t |
|---|---|
| headline | 0.74 |
| swap 30%/360 | 0.73 |
| triple Wednesday swap plus weekends (9 nights a week) | 0.54 |
| triple Friday swap, no weekend charge | 0.74 |
| swap 15%/yr | 1.07 |
| swap 0 | 1.40 |
| half-spread 0 / 2.5 / 10 bp | 0.84 / 0.79 / 0.65 |
| BTC/ETH 3 bp, alts 15 bp | 0.59 |
| BTC/ETH 3 bp, alts 25 bp | 0.42 |
| US100 0.25 / 0.375 / 0.5 / 1.0 pt | 1.07 / 0.99 / 0.91 / 0.58 |
| most favourable plausible (swap 0, 6.5 bp per side, US100 0.25 pt) | 1.83 |
| zero cost everywhere | 2.12 |

- **S2's weakness in the window is the signal, not the cost.** At zero cost S2 alone makes +2.54 bp per session (t 0.78).
- **H0022 decayed over time.** At 0.375 pt it made +9.61 bp over 2020-09 to 2022, and +1.40 bp over 2023-01 to 2025-11.

## 3. Sleeve rebuild matches the originals exactly

- **D3-11.** With the full universe at D3 costs, out of sample 2023-01 to 2026-09, it makes +7.32 bp/day, t 2.15 (iid) and 2.10 (NW), p5 +1.73. This is identical to `run.py`.
- **H0022.** On NQ 1m over 2020-09 to 2025-11, it makes +5.043 bp/day, t 1.68. This is exact.
- **The FTMO-coin restriction costs** the following, at D3 costs:

| period | full D3 universe | FTMO-listed coins only |
|---|---|---|
| D3's whole OOS | +7.32 bp/day | +6.95 bp/day |
| window W | +6.57 bp/day (t 1.76) | +5.60 bp/day (t 1.49) |

## 4. Weighting (diagnostic only, not a variant)

- The ex-post best fixed mix is a = 0.64 on the crypto sleeve. It gives t 0.78, against 0.74 for the registered 0.5.
- Pure S1 gives t 0.66 and pure S2 gives 0.36.
- The best weight at venue costs gives t 1.76, and at zero cost 2.20.

## 5. Statistics and annualisation

- **t-statistics.** iid t 0.7438 and NW10 t 0.8019 match an independent Bartlett computation.
- **Bootstrap.** The iid p5 of −1.98 agrees with the analytic −2.00, and the block bootstrap is correct.
- **Annualisation.** Calendar-day √365 annualisation with weekend zeros is internally consistent. Realised leg vols are 0.105 and 0.104, against targets of 0.10.
- **Cosmetic bug.** The standalone "s2" line in `run.txt` annualises a sessions-only series with √365. Its Sharpe of 0.034 should be about 0.027. t and p5 are unaffected.

## Other findings

- **Prop-account risk.** The worst stack day is −6.74%, on 2025-04-07 (S2 −8.59% × k2 0.76).
  - That day breaches FTMO's 5% maximum daily loss.
  - The stack's maxDD of −20% is twice FTMO's 10% maximum loss.
  - The `prop_dollars` output must be read with this tail in mind.
- **Roll weeks.** Including roll weeks makes the stack worse (t 0.46). The 76 roll-week sessions in the window average −10.7 bp.
- **Weekend vs weekday crypto.** The S1 unit book makes +10.4 bp/day net on weekends and −1.1 on weekdays.
  - This split was picked after seeing the data, from many possible cuts.
  - It is not actionable without its own pre-registration and fresh data.
- **Concentration.** Without 2024 the stack is negative: −1.04 bp/day, t −0.39.
