# H0019 — gamma-conditioned last-half-hour momentum: FAIL

**Verdict:** FAIL. On the out-of-sample SPY data, the GEX<0 trades made +7.69 bp net per trade, but the t-statistic was only +1.47, well short of the 3.48 the rule needs. Stage 2 was not run.

Everything below comes from `agents/daily/gamma-H0019/gamma.py`. The full output is in `agents/daily/gamma-H0019/run.txt`.

## What was tested (as registered in `agents/ledger.csv`, row H0019)

- **When to trade:** only on days when the previous trading day's SqueezeMetrics GEX was below 0.
- **Direction:** the sign of the return from the prior session's 15:59 close to today's 15:29 close.
- **Trade:** enter at the 15:30 open in that direction and exit at the 15:59 close. One trade a day, with no stop and no target.
- **Cost:** 2 bp round trip.
- **Unit:** net return in bp per trade.
- **Control:** the same rule on days when the previous GEX was 0 or higher. It is reported but does not decide anything.
- **Decision rule:** pass only if both of these hold:
  - D2 net mean > 0 with one-sided t ≥ z(0.05/N);
  - D1 gross mean > 0.
- **Threshold:** the ledger N is **197**, so alpha is 0.05/197 = 2.54e-4 and the bar is **z = 3.4767**.

### Choices fixed before any result was computed (also in the script docstring)

- **Session:** a weekday with at least one bar between 09:30 and 15:59 New York time. This is the same definition `gapfade-H0012` uses.
- **Prior session:** the previous session in the price file. If that session has no 15:59 bar, the day is skipped; the script does not reach further back.
- **Previous day's GEX:** the latest DIX.csv row dated strictly before the trade date.
- **Signal bars:** today's 15:29 bar must exist. A zero return means no trade.
- **Entry:** the open of the first bar from 15:30 to 15:59.
- **Exit:** the close of the last bar at or before 15:59.
- **Fills in practice:** every GEX<0 trade filled exactly at 15:30 and 15:59. A few control trades used a neighbouring bar: 49 in D1 and 3 in D2.
- **t-statistic:** mean divided by sd/√n.
- **Bootstrap p5:** the 5th percentile of the mean over 10,000 iid resamples, seed 0.
- **Trades per year:** trades divided by the calendar span of the window.

## Data

| | Source | Check |
|---|---|---|
| GEX | `Fluxus-Trade-Lab/fluxus-dashboard@c1eb9273…/SqueezeMetrics/DIX.csv` (date, price, dix, gex). 3,879 rows, 2011-05-02..2026-10-02. 8.9% of rows have GEX < 0 | sha256 `51bef9ea…9ce62` matches |
| D1 in-sample | FutureSharks SPXUSD 1m. Window 2011-05..2018-12: 1,972 sessions. 166 have no 15:29 bar and 65 have no 15:59 bar | sha256 pins from `gapfade-H0012` all match |
| D2 out-of-sample | Ascensao `spy_intra_data.csv` (LFS) via `daily/2026-10-04/data_fetch.py`. 1,645 sessions, 2019-01-02..2025-07-18 | sha256 matches the pin |

- **Loaders:** copied verbatim into `gamma-H0019/loaders.py`, because `gapfade.py` asserts N = 196 when it is imported.
- **Storage:** the data stay in scratch and were not committed.

### Future-truncation test

For **every** day in each window (1,972 days in D1, 1,644 in D2), the script recomputed the signal twice and compared it with the full-data result:

- once with that day's bars cut off after 15:29;
- once with the GEX table cut to rows dated before that day.

The signal here means eligibility, side and the GEX value used. It was checked under both regimes (GEX<0 and GEX≥0) and both thresholds (0 and the stage-2 20th percentile).

All results were identical. So neither the signal nor eligibility uses anything after 15:29 of the trade day.

## Results (bp per trade; net = after 2 bp)

| Dataset | Days | Trades | Trades/yr | Gross | Net | One-sided t (net) | Bootstrap p5 (net) | Win rate |
|---|---|---|---|---|---|---|---|---|
| D1 SPXUSD 2011–18 | **GEX<0** | 123 | 16.0 | +3.70 | +1.70 | +0.32 | −7.09 | 54.5% |
| D1 SPXUSD 2011–18 | GEX≥0 (control) | 1,621 | 211.5 | +1.33 | −0.67 | −1.26 | −1.54 | 45.2% |
| **D2 SPY 2019–25** | **GEX<0** | 202 | 30.9 | +9.69 | **+7.69** | **+1.47** | −1.01 | 54.0% |
| D2 SPY 2019–25 | GEX≥0 (control) | 1,427 | 218.2 | −0.05 | −2.05 | −2.92 | −3.20 | 46.5% |

### Per year (trades / gross bp / net bp)

- **D1 GEX<0:**
  - 2011 27/+7.0/+5.0
  - 2012 13/+7.9/+5.9
  - 2013 2/+2.6/+0.6
  - 2014 5/−6.8/−8.8
  - 2015 22/+2.2/+0.2
  - 2016 19/+6.9/+4.9
  - 2017 1/+3.1/+1.1
  - 2018 34/+0.3/−1.7
- **D1 control:**
  - 2011 135/+5.4/+3.4
  - 2012 204/−0.5/−2.5
  - 2013 218/+4.0/+2.0
  - 2014 216/+2.3/+0.3
  - 2015 216/+2.0/−0.0
  - 2016 219/−1.5/−3.5
  - 2017 212/−1.1/−3.1
  - 2018 201/+1.5/−0.5
- **D2 GEX<0:**
  - 2019 18/+7.4/+5.4
  - 2020 31/+42.0/+40.0
  - 2021 16/−11.2/−13.2
  - 2022 104/+5.0/+3.0
  - 2023 23/+0.3/−1.7
  - 2024 1/−0.4/−2.4
  - 2025 9/+20.1/+18.1
- **D2 control:**
  - 2019 229/+0.3/−1.7
  - 2020 217/+1.7/−0.3
  - 2021 235/+0.5/−1.5
  - 2022 147/+2.7/+0.7
  - 2023 224/+0.3/−1.7
  - 2024 249/−2.6/−4.6
  - 2025 126/−3.3/−5.3

## Decision

- **Condition 1, D2 net mean > 0 with t ≥ 3.4767:** the net mean is +7.69 bp, but t is only +1.47. **Not met.**
- **Condition 2, D1 gross mean > 0:** +3.70 bp. Met.

**Result: FAIL.** Stage 2 (5 bp cost, the trailing-252-day 20th-percentile threshold, and the NQ check without roll weeks) was registered to run only if this stage passed. It was coded in advance in `gamma.py` but not executed.

## Reading it plainly

The direction matches the paper:

- On negative-gamma days, last-half-hour momentum earned money in both datasets.
- On positive-gamma days, it lost after costs in both datasets.

The edge is still far from significant. It also rests on very few trades:

- **D2:** 2020, with 31 trades at +40 bp net, carries most of the mean. 2022 supplies half the trades at only +3 bp net.
- **D1:** after costs the mean is close to zero (+1.7 bp, t 0.32).

At about 16–31 trades a year, this rule cannot clear a Bonferroni bar of 3.48 from this much history. Even taken at face value it would be a regime filter, not a standalone strategy. The family is closed under the pre-registration. Re-testing a variant would need a new ledger row, and with it a higher N.
