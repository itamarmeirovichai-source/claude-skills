# E2 pre-registration — scheduled macro events, intraday futures (wave 2)

Written 2026-10-11, **before any backtest was run**. Before writing this, only three things
were looked at: (1) the event calendar (`agents/daily/w2-events/events.csv`, built by
`calendar_build.py` from federalreserve.gov and ALFRED), (2) where the NQ file switches
contract (a scan of bar-to-bar jumps, which shows every switch at the 00:00 ET bar, outside
RTH), and (3) `clock_check.py`, which measures only the *size* of 1m moves around the FOMC
statement minute, never a direction or a trade outcome. No signal, trade or return was
computed. The commit that adds this file and `E2.csv` comes before any result commit.

Bar: one-sided z(0.05/270) = **3.5603** (fixed for wave 2). Budget used: **12** of 15.

## 1. Data and split

| role | data | dates | notes |
|---|---|---|---|
| in-sample (IS, reported, not part of the gate) | SPXUSD 1m, FutureSharks/HistData (sha256 pins in `loaders.py`) | 2010-11..2018-12 | FOMC days before 2013-03-20 are dropped from IS: the clock check cannot confirm the 12:30 / 12:35 / 14:15 statement minute in this file (`clock_check.txt`) |
| OOS leg A | SPY 1m RTH (Polygon, pinned) as the ES proxy | 2019-01-02..2025-07-18 | |
| OOS leg B | NQ 1m (pinned) | 2020-08-31..2025-11-21 | no roll-week exclusion: contract switches sit at the 00:00 ET bar, never inside RTH; overnight gaps subtract the 00:00 bar jump (sec. 3) |

Rules were taken from the literature (Lucca-Moench 2015 pre-FOMC drift; post-announcement
drift/whipsaw on FOMC days; Gao-Han-Li-Zhou 2018 intraday momentum, stronger on news days),
not from any of these data.

## 2. Events (`events.csv`, scheduled rows only)

FOMC statement (time per row; 14:00 ET from 2013-03-20), CPI 08:30, NFP 08:30, PCE 08:30,
retail sales 08:30, ISM manufacturing 10:00, FOMC minutes 14:00. Unscheduled/cancelled
meetings are never event days for signals.

**Tier-1 blackout (MyFundedFutures rule, applied to every variant):** for each event whose
time T falls inside RTH that day (FOMC statement, FOMC minutes, ISM), no position may be open
in [T−2 min, T+2 min]. A position open at T−3 is closed at the **close of the bar opening at
T−3** (= T−2) and is not re-entered unless the variant's own entry comes at or after the open
of the bar at T+3. Every entry below is ≥ T+3 for its own event. 08:30 releases are before
the RTH open and need no action.

## 3. Common mechanics

- Bars are labelled by their open time, NY clock. RTH = bars 09:30..15:59 on weekdays.
- `o[X]` = open of bar X, `c[X]` = close of bar X. A signal bar that is missing uses the last
  bar at or before it; an entry bar that is missing uses the next bar within 3 minutes, else
  no trade. Exit = close of the last bar at or before 15:59 (or the blackout exit). Nothing
  about the trade day after the entry minute is used to decide eligibility (truncation test).
- Previous close `pc` = `c` of the last RTH bar of the previous session in the file.
- Overnight gap `g = ln(o[09:30]/pc)`. On NQ only, subtract `ln(o[00:00]/c[last bar before
  00:00])` for that day (removes the front-month switch; ~0 on other days).
- `sign(0)` = no trade. Size = 1 unit (1 contract; SPY treated as 1/10 ES).
- **Costs per side** (1 tick + $2.50 commission): ES/SPXUSD 0.25 + 2.5/50 = **0.30 index pt**;
  SPY proxy **$0.030/share** (ES/10); NQ 0.25 + 2.5/20 = **0.375 pt**. 2× cost = double.
- Trade return (bp) = `side*(exit−entry)/entry*1e4 − 2*cost/entry*1e4`.

## 4. Variants (12 counted)

| id | event days | signal | entry | exit |
|---|---|---|---|---|
| E2-01 | FOMC | s = sign(c[T+14] − c[T−1]) | o[T+15], side s | close |
| E2-02 | FOMC | s = sign(c[T+4] − c[T−1]) | o[T+5], side s | close |
| E2-03 | FOMC | s = sign(c[T+29] − c[T−1]) | o[T+30], side s | close |
| E2-04 | FOMC | reversal of E2-01 | o[T+15], side −s | close |
| E2-05 | FOMC | pre-FOMC drift (Lucca-Moench), long only | o[09:30], long | c[T−3] |
| E2-06 | CPI or NFP | s = sign(g) | o[09:31], side s | close |
| E2-07 | CPI or NFP | reversal of E2-06 | o[09:31], side −s | close |
| E2-08 | any of FOMC, CPI, NFP, PCE, RETAIL, ISM | s = sign(ln(c[09:59]/pc)) (overnight + first half hour; NQ gap-adjusted as above) | o[10:03], side s | close (blackout applies on FOMC/minutes days) |
| E2-09 | as E2-08 | as E2-08 | o[15:30], side s | c[15:59] |
| E2-10 | days with none of the six events (control) | as E2-08 | o[10:03] | close (blackout for FOMC minutes) |
| E2-11 | as E2-08, and range(09:30..09:59)/o[09:30] > median of the same over the previous 20 sessions | as E2-08 | o[10:03] | close |
| E2-12 | combination book: per day, the sum of E2-01, E2-05, E2-06 and E2-08 trade returns (each 1 unit) | | | |

## 5. Statistics and gate

- Unit = one event day. For each OOS day, the net return is the mean of the available legs
  (SPY and/or NQ). n = OOS event days with a trade; t = mean/sd·√n.
- Bootstrap p5 of the mean: 10,000 iid resamples of days, seed 0; for E2-12 also a
  5-day block bootstrap, the lower p5 is used.
- **Gate (all must hold, at 1× cost):** pooled OOS t ≥ 3.5603; bootstrap p5 > 0; SPY-leg net
  mean > 0; NQ-leg net mean > 0; truncation test passes; look-ahead test passes. The 2× cost
  result is reported next to it; if 2× fails the t bar the verdict says "passes at 1× only".
- **Truncation test:** for every OOS event day, deleting all bars after the entry minute must
  leave eligibility, side, entry time and entry price unchanged.
- **Look-ahead test:** (a) entry delayed by one bar must keep the sign of the OOS mean and at
  least half its t; (b) event dates are publicly scheduled ahead of time (calendars above).
- Reported: OOS t, bootstrap p5, trades/year, IS mean, 2× cost t. Payout per $100k funded
  (Topstep, MyFundedFutures) only if the gate passes.
