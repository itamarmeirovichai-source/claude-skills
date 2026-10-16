# H0021 — intraday VWAP trend: FAIL

**Verdict:** FAIL. On the decisive NQ data the rule made +4.40 bp a day after costs (t +1.38), far short of the t ≥ 3.4794 it needs. SPY lost 12.0 bp a day after costs.

Every number below comes from `agents/daily/vwap-H0021/vwap.py`. The full output is in `agents/daily/vwap-H0021/run.txt`, and the unit-test output is in `agents/daily/vwap-H0021/pytest.txt`.

## What was tested (as registered in `agents/ledger.csv`, row H0021)

This is the rule from Zarattini & Aziz (2023), "Volume Weighted Average Price (VWAP): The Holy Grail for Day Trading Systems" (SSRN 4631351). It was run exactly as written, with no tuning and no filters.

- **Session:** a weekday with regular-hours bars, 09:30 to 15:59 New York time.
- **VWAP:** starts at 09:30. It is the running sum of typical price × volume divided by the running sum of volume, where typical price = (high + low + close) / 3. At each bar it uses only the bars up to and including that one.
- **Signal:** at each bar close from 09:30 to 15:58, the wanted position is long if close > VWAP and short if close < VWAP. If they are equal, the position stays as it is (flat if there has been no signal yet).
- **Execution:** a position change fills at the next bar's open.
- **Exit:** flat at the 15:59 bar close.
- **No** stops, targets, filters or sizing. Size is 1 NQ contract, or 1× notional for SPY.
- **Cost per unit traded:** a flip is 2 units; an open or a close is 1.
  - NQ: 0.375 index point per unit.
  - SPY: 0.5 bp of price per unit.
- **Unit:** net daily return in bp of notional = the day's P&L divided by that day's first entry price.
- **Decision rule:** PASS only if both hold:
  1. NQ net daily mean > 0 with one-sided t ≥ z(0.05/N);
  2. SPY net daily mean > 0.
- **Threshold:** the ledger N is **199**, so alpha is 0.05/199 = 2.51e-4 and the bar is **z = 3.4794**.

### Choices fixed before any result was computed (also in the script docstring)

- **Session:** a weekday with at least one bar between 09:30 and 15:59 New York time, the same definition `orb-H0020` uses. VWAP uses those bars only.
- **Next bar:** the next bar that exists in the file. Missing minutes are not filled in.
- **Last bar:** the position goes flat at the close of the session's last bar. That is 15:59 on a normal day, and earlier on half days or when the 15:59 bar is missing. The last bar's own signal is never acted on. This happened on 41 NQ sessions and 3 SPY sessions.
- **No volume yet:** if the running volume is 0, VWAP is undefined and the bar counts as "equal". This never happened in either dataset.
- **P&L:** marked open to open for each bar, and open to close for the last bar. Each fill pays the cost at its own price (a bar's open, or the last close for the final exit).
- **Days with no position** would score 0 bp and stay in the sample. There were none.
- **NQ roll weeks:** days from `roll_excluded` (copied from `gapfade-H0012`) are dropped. That covers Monday to Friday of the week holding the 3rd Friday of Mar/Jun/Sep/Dec, plus the following Monday.
- **t-statistic:** mean divided by sd/√n, one-sided.
- **Bootstrap p5:** the 5th percentile of the mean over 10,000 iid resamples of days, seed 0.
- **Sharpe:** mean divided by sd, times √252.
- **Max drawdown:** the largest peak-to-trough fall in the running sum of net daily bp, with no compounding.
- **NQ post-publication subsample:** dates from 2023-11-01 on.
- **Cost ×2:** both cost rates doubled.

## Data

The data are fetched with `agents/daily/2026-10-04/data_fetch.py` and checked against the same sha256 pins as `orb-H0020`. They are never committed. `vwap-H0021/loaders.py` is the H0020 loader with the volume column kept.

| | NQ 1m (hindsight-finance) | SPY 1m RTH (Ascensao) |
|---|---|---|
| sessions in file | 1349 (2020-09-01..2025-11-21) | 1645 (2019-01-02..2025-07-18) |
| roll-week days dropped | 126 | 0 |
| sessions used | 1223 | 1645 |
| bars used | 469,740 | 640,753 |
| bars with zero volume | 0 | 0 |
| bars with close exactly = VWAP | 5 | 11 |

## Look-ahead checks (both passed)

- **(a) Truncation test.** For 250 random sessions per dataset (seed 0), the day was cut after every bar in turn, and the positions were recomputed from only the remaining bars. Every position was identical. That is 95,730 cut points on NQ and 97,425 on SPY.
- **(b) Full streaming check.** A separate bar-by-bar loop sees only past bars and keeps cash accounts. Across every session, it reproduced every bar's position, the units traded, the first entry price and the daily gross and cost. The largest P&L difference was 0 on NQ and 5.7e-14 price units on SPY.
- **Unit tests.** 8 tests cover VWAP, next-open execution, holding on an equal close, flat at the last close with the last signal ignored, flip = 2 units, the percent cost, no carry-over between sessions, and a no-position day. All 8 pass (`pytest.txt`).

## Results

### NQ (decisive), ex roll weeks

| | value |
|---|---|
| days | 1223 |
| average units traded per day | 32.64 |
| gross mean | +12.374 bp/day (t +4.00) |
| cost | 7.977 bp/day |
| **net mean** | **+4.397 bp/day** |
| **one-sided t, net** | **+1.38** (bar 3.4794) |
| bootstrap p5, net | −0.856 bp/day (gross +7.310) |
| win rate of days, net | 0.517 |
| annualized Sharpe, net | +0.62 |
| max drawdown, net | 2054.7 bp |
| worst day, net | −470.4 bp (2022-07-06) |

In points: the average first entry price was 16,216. The gross was +18.83 pts a day and the cost was 12.24 pts a day; 0.375 pt is 0.244 bp.

| year | n | units/day | gross bp | net bp | t net | win | Sharpe |
|---|---|---|---|---|---|---|---|
| 2020 | 75 | 34.85 | +13.217 | +2.202 | +0.17 | 0.547 | +0.31 |
| 2021 | 234 | 31.62 | +17.446 | +9.198 | +1.67 | 0.517 | +1.73 |
| 2022 | 234 | 31.68 | +20.527 | +11.164 | +1.05 | 0.568 | +1.09 |
| 2023 | 233 | 35.15 | +4.025 | −5.325 | −0.84 | 0.446 | −0.88 |
| 2024 | 235 | 31.95 | +11.830 | +5.538 | +0.96 | 0.519 | +0.99 |
| 2025 | 212 | 32.05 | +7.261 | +1.827 | +0.24 | 0.524 | +0.27 |

**Post-publication subsample (2023-11-01 on):** 483 days, 32.61 units a day.

- Gross +8.122 bp/day (t +1.88); net +1.975 bp/day (t +0.45).
- Bootstrap p5, net: −5.289.
- Win rate 0.507, Sharpe +0.32.
- Max drawdown 1638.0 bp; worst day −378.5 bp (2025-04-07).

**Cost ×2:**

- Full sample: net −3.580 bp/day (t −1.08), bootstrap p5 −9.001, Sharpe −0.49, max drawdown 6134.7 bp.
- 2023-11 onward: net −4.172 bp/day (t −0.92).

### SPY (corroboration)

| | value |
|---|---|
| days | 1645 |
| average units traded per day | 35.19 |
| gross mean | +5.591 bp/day (t +2.66) |
| cost | 17.593 bp/day |
| **net mean** | **−12.001 bp/day** (t −5.30) |
| bootstrap p5, net | −15.818 bp/day (gross +2.045) |
| win rate of days, net | 0.432 |
| annualized Sharpe, net | −2.07 |
| max drawdown, net | 19,787.5 bp |
| worst day, net | −774.5 bp (2025-04-07) |

| year | n | units/day | gross bp | net bp | t net | win | Sharpe |
|---|---|---|---|---|---|---|---|
| 2019 | 252 | 36.74 | −1.294 | −19.660 | −5.06 | 0.377 | −5.06 |
| 2020 | 253 | 35.30 | +11.792 | −5.854 | −0.83 | 0.462 | −0.83 |
| 2021 | 252 | 34.29 | +8.276 | −8.866 | −2.04 | 0.476 | −2.04 |
| 2022 | 251 | 34.03 | +10.608 | −6.398 | −0.83 | 0.482 | −0.83 |
| 2023 | 250 | 36.24 | +2.346 | −15.774 | −3.32 | 0.400 | −3.34 |
| 2024 | 252 | 35.42 | +4.634 | −13.073 | −2.80 | 0.381 | −2.80 |
| 2025 | 135 | 33.59 | +0.284 | −16.509 | −1.58 | 0.452 | −2.16 |

**Cost ×2:** net −29.594 bp/day (t −12.12).

## Pre-registered decision

1. NQ net mean > 0 with one-sided t ≥ 3.4794: net +4.397 bp, t +1.38. **Not met.**
2. SPY net mean > 0: net −12.001 bp. **Not met.**

**Result: FAIL.**

## What it means (not part of the decision)

- **The gross effect looks real, but the costs are too high.** On NQ the gross mean (+12.4 bp/day, t +4.00) clears the bar before costs. But about 33 units traded a day costs about 8 bp, two thirds of the gross. Doubling the cost makes the net negative.
- **It is weaker after publication:** gross +8.1 bp/day from 2023-11 on, and 2023 was negative after costs.
- **SPY is worse:** a smaller gross (+5.6 bp/day) and a higher cost per unit (0.5 bp against NQ's 0.24 bp) make it clearly negative.
- **Do not rescue it.** Testing fewer trades, a VWAP band or a time filter would be new hypotheses, each costing one more count in N. None was pre-registered here.

**One-line verdict:** H0021 FAILS. VWAP trend has a gross NQ edge, but at about 33 units a day the costs eat most of it: net +4.4 bp/day, t 1.38 against a bar of 3.48, and SPY is negative after costs.
