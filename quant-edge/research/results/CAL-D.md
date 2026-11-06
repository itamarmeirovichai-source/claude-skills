# CAL-D — daily pipeline calibration (MOP 12-month TSMOM, 54 futures)

Registry row CAL-D (registered commit a9ddfcd, count 1). Script `research/cal_d/cal_d.py`. Data `daily_futures_1984_2016` via `qe.gateway.load` (IS read for 12-month warm-up only; reads logged in `registry_reads.log`).

**This is a pipeline calibration, not a strategy test. It never re-opens H0007 and is not an edge claim.**

| series (OOS 1990-01-01..2016-10-28) | Sharpe | t_min (iid, NW lag 21) | ann. mean | ann. vol |
|---|---|---|---|---|
| gross | 1.432 | 6.78 (7.40, 6.78) | 16.88% | 11.79% |
| net1x | 1.413 | 6.68 (7.30, 6.68) | 16.65% | 11.79% |
| net2x | 1.393 | 6.59 (7.20, 6.59) | 16.43% | 11.79% |

- Sharpe s.e. (Mertens/Opdyke, annual): 0.196; 90% CI 1.11..1.75; skew -0.15, kurtosis 6.0; Lo-adjusted Sharpe 1.308.
- Max drawdown (gross, uncompounded daily sum compounded): -23.2%. Days: 6971.
- 1985-2016 Sharpe of the same run (comparable to the inherited 1.17): 1.404.
- Positive calendar years (OOS): 23 of 27.

## Decision (rule fixed in the row)

OOS gross Sharpe 1.432 inside [0.85, 1.45] → pipeline calibration **PASSES** on criterion (a).
Criterion (b), year-sign agreement with the inherited run, is checked separately against the inherited yearly table (see below).

## Criterion (b) and the gap to the inherited 1.17

- The inherited record has no per-year table for H0007 (`references/trend-following-run.txt` prints only worst/best year and positive-month share), so criterion (b) **cannot be computed from a file**. It is recorded as "not verifiable", not as passed.
- This run gives 1.40 on 1985–2016 against the inherited 1.17. The inherited code (`scripts/trend_backtest.py`, read, not run) differs in three ways the registry row did not copy: rolling 60-day standard deviation instead of EWMA (com 60), a 10% per-asset target instead of 40% (scale only), and a Sharpe of compounded annual return over volatility instead of the arithmetic daily Sharpe. Which of these, if any, explains the 0.23 gap is unmeasured; the Re-implementer checks it before CAL-D is used as evidence for anything beyond "the gateway, the reads log and the daily engine path work".
- Read-log note: the script crashed once (a pandas shape error in the weighting step, 2026-11-06 00:05:59 UTC) after the gateway had logged an OOS read and before any P&L was computed; the fixed run read IS and OOS again at 00:06:13. Both reads are in `registry_reads.log`; the row's count stays 1 and the double read is disclosed here and in WORK-LOG for the Referee.

## Verdict

Pipeline calibration (a) PASSES at the top of its pre-stated range (1.432 vs upper bound 1.45); (b) not verifiable. Testing may proceed on the daily pipeline; the intraday pipeline still needs CAL-I.
