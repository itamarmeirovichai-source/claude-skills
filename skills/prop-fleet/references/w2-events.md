# E2 — Scheduled macro events, intraday ES/NQ (wave 2)

**Verdict: FAIL. 0 of 12 pre-registered variants pass.** The best out-of-sample t is **+1.09** (E2-04, fading the first 15 minutes after the FOMC statement). The bar is 3.5603. Its bootstrap p5 is −7.8 bp, it makes 7.8 trades a year, and it lost money in sample. Not one variant has a positive OOS mean on both legs with t above 1.1. Gross edges are near zero, so costs are not what kills them. No payout is computed, because nothing passed the gate.

*Written 2026-10-11 by the E2 head.*

- The rules were pre-registered in commit `d489ea8`, before any backtest.
- An independent verifier re-implemented the backtest from the spec alone and matches all 12 rows to the printed digit.
- The red team found only small defects. None moves any t by more than 0.25.

## What was tested

Target: a fully automatic intraday futures rule for the safe-list firms (MyFundedFutures, Topstep, Lucid, TradeDay) that pays at least 20% a year of funded account size. Every position is flat by the close.

The candidates came from the literature, never from these data:

- post-FOMC drift (Lucca–Moench 2015 for the pre-announcement drift);
- FOMC whipsaw and reversal;
- intraday momentum (Gao–Han–Li–Zhou 2018), reported to be stronger on news days.

The 12 variants (full spec in `agents/prereg/E2_rules.md`):

| id | rule |
|---|---|
| E2-01/02/03 | FOMC: trade in the direction of the first 15 / 5 / 30 minutes after the statement, hold to the close |
| E2-04 | FOMC: fade the first 15 minutes |
| E2-05 | Pre-FOMC drift, intraday part only: long at 09:30, flat 3 minutes before the statement |
| E2-06 / 07 | CPI or NFP days: follow / fade the overnight gap at the open (the gap includes the 08:30 release) |
| E2-08 | Event days (FOMC, CPI, NFP, PCE, retail sales, ISM): first-half-hour momentum, 10:03 to the close |
| E2-09 | Same signal, last half hour only |
| E2-10 | Same as E2-08 on non-event days (control) |
| E2-11 | E2-08, only when the opening range is above its 20-day median (volatility filter) |
| E2-12 | Fixed book: E2-01 + E2-05 + E2-06 + E2-08 |

**News rule.** Every variant obeys the MyFundedFutures Tier-1 window. No position or order is open from 2 minutes before to 2 minutes after a release inside regular hours (FOMC statement, FOMC minutes, ISM at 10:00). A held position is closed at the close of the bar that opens 3 minutes before the release. Every entry is at least 3 minutes after its own release.

## Results (1× cost; unit = net bp per event day; OOS pooled over SPY and NQ)

| id | IS n | IS bp | SPY bp | NQ bp | OOS n | OOS bp | **t** | p5 | trades/yr | t at 2× | t, entry +1 bar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E2-01 | 47 | +5.20 | −13.29 | −25.14 | 54 | −18.39 | −1.25 | −42.91 | 7.8 | −1.34 | −1.20 |
| E2-02 | 47 | −6.84 | −5.74 | −12.41 | 54 | −9.52 | −0.63 | −34.19 | 7.8 | −0.71 | −0.69 |
| E2-03 | 45 | +6.31 | −13.83 | −21.32 | 54 | −17.32 | −1.21 | −40.98 | 7.8 | −1.30 | −1.38 |
| E2-04 | 47 | −10.87 | +10.13 | +24.16 | 54 | +16.02 | **+1.09** | −7.84 | 7.8 | +1.01 | +1.04 |
| E2-05 | 47 | −0.35 | +1.78 | +5.09 | 54 | +2.18 | +0.45 | −5.71 | 7.8 | +0.20 | +0.87 |
| E2-06 | 189 | −1.55 | −4.70 | +1.82 | 161 | −3.70 | −0.46 | −17.32 | 23.4 | −0.62 | −0.47 |
| E2-07 | 189 | −5.09 | +1.51 | −2.80 | 161 | +1.25 | +0.16 | −11.67 | 23.4 | +0.00 | +0.17 |
| E2-08 | 470 | +0.41 | −2.50 | −8.92 | 438 | −5.62 | −1.28 | −13.03 | 63.6 | −1.55 | −1.23 |
| E2-09 | 468 | −4.09 | −3.43 | −4.03 | 437 | −4.10 | −2.27 | −7.04 | 63.5 | −2.93 | −2.31 |
| E2-10 | 1571 | −1.12 | −0.46 | +2.57 | 1330 | +1.59 | +0.69 | −2.10 | 193.2 | +0.17 | +0.76 |
| E2-11 | 201 | +6.36 | −4.53 | −12.72 | 269 | −7.28 | −1.14 | −17.83 | 39.1 | −1.31 | −1.06 |
| E2-12 | 473 | +0.27 | −5.63 | −10.77 | 438 | −8.98 | −1.37 | −20.08 | 63.6 | −1.67 | −1.29 |

What the results say:

- **FOMC.** The first 5 to 30 minutes after the statement did not predict the rest of the day out of sample. Continuation lost; fading gained +16 bp per day, but at t +1.09 over 54 days. In sample (2013–2018) the sign was the opposite: continuation won, at t ≈ +1.0. That is noise, not an edge. The press conference at T+30 seems to move prices as much as the statement does.
- **Pre-FOMC drift.** Its intraday part is small: +2.2 bp out of sample, t +0.45, and −0.35 bp in sample. This fits the published finding that the drift faded after 2015 and was mostly overnight.
- **CPI/NFP at the open.** Neither following nor fading the 08:30 gap works. Both directions have |t| ≤ 0.5 in and out of sample.
- **Event-day momentum.** It is no better than on ordinary days. Event days are negative out of sample (−5.6 bp, t −1.28) and the control days slightly positive (t +0.69). The volatility filter makes it worse. The last half hour on event days is negative in both samples (OOS t −2.27, IS t −3.77 per the verifier). That runs against Gao et al., and it is not tradable as a short either: reversing it would be a new, unregistered variant.

**Gross (zero-cost) check.** The best gross OOS t is +1.21, on E2-10, the control. The mirror pairs give exactly opposite gross values (E2-01/04 ±17.20 bp; E2-06/07 ±2.48 bp). Costs cost about 1.2 bp per trade.

## Gate (bar one-sided z(0.05/270) = 3.5603)

| condition | result |
|---|---|
| OOS t ≥ 3.5603 | **fails for all 12** (max +1.09) |
| bootstrap p5 > 0 | fails for all 12 |
| SPY and NQ legs both > 0 | holds only for E2-04, E2-05 and E2-10, with t of +1.09, +0.45 and +0.69 |
| truncation test | passes: 0 violations in 2,857 SPY, 2,314 NQ and 3,321 SPX decisions. The red team notes it is weaker than its label (it re-checks only taken trades and keeps the entry bar's high/low/close), but `decide()` reads nothing after the entry minute except the entry bar's open. |
| look-ahead test (entry +1 bar) | no t collapses or improves meaningfully |
| 2× cost | everything is worse |

**Payout per $100k funded account (Topstep / MyFundedFutures):** not computed, because the gate failed.

For scale: $20k a year at 7.8 FOMC trades would need about $2,600 net per trade after the split. Even E2-08's 64 trades a year would need about $350 per trade. The measured edges are zero or negative.

## Data and split

| role | data | days |
|---|---|---|
| IS (reported, not in the gate) | SPXUSD 1m, FutureSharks/HistData, 2010-11..2018-12 | 2,089 sessions |
| OOS leg A | SPY 1m RTH (Polygon, pinned), as the ES proxy, 2019-01..2025-07 | 1,644 |
| OOS leg B | NQ 1m (pinned), 2020-09..2025-11 | 1,348 |

All files pass the sha256 pins in `agents/daily/w2-events/loaders.py`, which are the same as `vwap30-H0022`, `orb-H0020` and `data_fetch.py`. No data is committed.

**NQ contract switches** all sit at the 00:00 ET bar, never inside regular hours. So there is no roll-week exclusion. Overnight gaps subtract that day's 00:00-bar jump.

**IS FOMC days before 2013-03-20 are dropped.** In this file, `clock_check.py` cannot confirm the 12:30 / 12:35 / 14:15 statement minute. From 2013-03-20 on, the statement bar shows a median of about 7× the day's normal 1m move, at exactly T+0 in SPXUSD, SPY and NQ.

**Costs per side** are 1 tick plus $2.50 commission: ES / SPXUSD 0.30 pt, SPY $0.030 per share (ES / 10), NQ 0.375 pt. 2× doubles them.

**Statistic.** The unit is one event day. On days in both legs, the SPY and NQ net returns are averaged. t = mean / sd · √n. The iid bootstrap uses 10,000 draws with seed 0; E2-12 also gets a 5-day block bootstrap, and the lower p5 is used. Trades per year use the full OOS span of 6.89 years.

## Event calendar (sources)

`agents/daily/w2-events/events.csv`, built by `calendar_build.py`:

- **FOMC:** federalreserve.gov `fomchistorical2010..2020.htm` and `fomccalendars.htm` (meeting headings; unscheduled and cancelled meetings excluded; minutes release dates).
  - **Statement time:** 14:00 from 2013-03-20, per the Fed press release of 2013-03-13: "Committee policy statements for all regularly scheduled meetings will now be released at 2 p.m.".
  - **Earlier press-conference meetings:** the time printed on `fomcpresconf<date>.htm`.
  - **Other earlier meetings:** 14:15.
- **CPI** (rid 10), **NFP** (rid 50), **PCE** (rid 54) and **retail sales** (rid 9): ALFRED release dates (`alfred.stlouisfed.org/release/downloaddates?rid=…`).
  - The February CPI seasonal-revision dates are dropped.
  - For NFP, the first date in each month is kept.
- **ISM manufacturing:** first business day of the month at 10:00, by rule. ISM is not on FRED or ALFRED.
- **Blocked host:** bls.gov schedule pages return "Access Denied" (403) from this session. This is reported, not routed around. ALFRED carries the same BLS dates.

Defects the red team found (`agents/daily/w2-events/redteam/findings.md`):

- January ISM falls on the 2nd or 3rd business day, so 7 OOS days are misplaced.
- 3 unscheduled-action FOMC releases are tagged as minutes.
- 5 April retail-sales revision postings are counted as event days.

Correcting all of them changes only E2-08 to E2-12, by at most 0.24 in t (E2-08 −1.28 → −1.04; E2-10 +0.69 → +0.52). E2-01 to E2-07 are unchanged. The verdict does not change.

## Verification

- **Independent verifier** (`agents/daily/w2-events/verify/`). It re-implemented the backtest from `E2_rules.md` without seeing the head's code.
  - Its first run disagreed on E2-05. The head's code had ignored the ISM 10:00 blackout on the 4 OOS days where FOMC and ISM coincide. The head fixed this in `events_bt.py` (`exit_e205`).
  - After the fix, all 12 rows match to the printed digit.
- **Red team** (`agents/daily/w2-events/redteam/`). It tried to show that the negative result was wrong. It found:
  - the calendar defects above;
  - SPY half-day bars after 13:00 (1 event trade);
  - NQ CME-holiday sessions (control trades only);
  - the weaker-than-labelled truncation test.

  None could hide an edge. It also confirmed:
  - all 54 OOS FOMC dates;
  - about 25 CPI and 25 NFP spot checks;
  - the NQ roll adjustment (on 2023-12-12 it turns a raw +128.7 bp gap into −2.6 bp);
  - the cost arithmetic;
  - hand recomputation of trade rows to 4 decimals.

## Budget and bar

- **12 of 15** variants were counted (E2.csv); 3 were left unused.
- The wave-2 bar, 3.5603, is unchanged.
- No unregistered variant was run. The verifier and the red team re-ran only the 12 registered rules.

## Files

- `agents/prereg/E2.csv` (with results) and `agents/prereg/E2_rules.md`
- `agents/daily/w2-events/`:
  - `calendar_build.py`, `events.csv`
  - `clock_check.py`, `clock_check.txt`
  - `loaders.py`
  - `events_bt.py`, `run.txt`, `summary.csv`
  - `verify/`, `redteam/`

**Run:** `export CLAUDE_SCRATCH=<data dir>; python3 events_bt.py`, which takes about 15 s. The data come from `daily/2026-10-04/data_fetch.py` and FutureSharks/financial-data `SPXUSD/DAT_ASCII_SPXUSD_M1_2010..2018.csv`.

No purchase, sign-up, firm contact or money movement was made.
