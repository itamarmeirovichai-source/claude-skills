# QA — histdata_cfd_1m_UKXGBP_holdout

Data QA Auditor, Department C, 2026-11-06 02:18 UTC. Outcome-free: no strategy, signal or P&L is computed. **HOLD-OUT dataset**: structural checks only (no price levels, no return values, no cross-source correlation).

- path `DATA_ROOT/holdout/histdata_cfd_1m/UKXGBP`; rows 619,744; 2025-01-02 .. 2026-10-30 (UTC); sha256 `e745e8acda3ded0a…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/ukxgbp/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HOLD-OUT (ts >= 2025-01-01; gateway window 'holdout' only; QA outcome-free); HistData personal use; fetched 2026-11-06; 11 raw zips pinned in fetch_log; clock=histdata_rule (conflict): US anchor: winter peak 09:30 summer peak 09:31 clock; shift 1 min -> ny_dst | Europe/London 08:00 open: winter 03:00 summer 03:00 clock; shift 0 min (ny_dst predicts +0; est_fixed -60) -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 1 agree; 0 disagree; 1 undecided | verdict histdata_rule (agree); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 415 duplicate local stamps dropped; gaps: 4 gaps > 1 weekday-trading-day (longest: 2025-12-24..2025-12-25 1.4d; 2025-12-31..2026-01-01 1.2d; 2025-04-17..2025-04-20 1.1d); months without bars: none; clock diag on hold-out part itself

## Verdict: PASS

- no blocking issue found

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 09:30, summer peak 09:31 NY, shift 1 min -> OK.
- After conversion, home-market anchor Europe/London 08:00 (±25 min): winter peak 08:00, summer peak 08:00 local, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 2 CPI/NFP releases; spike at offset 0 (correct) 2, at −60 min (one hour early) 0, undecided 0.
  - offsets (min): 2025-03-12:0 2026-03-11:90
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 0 same, 0 one hour off, 2 other: 2025 16:14→17:00 2026 16:14→16:59
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2019+ aligned 16:14 (329/345); 2019+ mismatch 16:59 (19/32)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (XLON, exchange_calendars, breaks excluded)

- sessions in span 464; with ≥1 bar 462; with no bar 2; median coverage of sessions with bars 100.0%; sessions ≥95% covered 99.6%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2025 | 253 | 1 | 100.0% | 100.0% | 3 | 1 | 1323 |
| 2026 | 211 | 1 | 100.0% | 99.0% | 4 | 2 | 1327 |

- lowest-coverage sessions (with bars): 2026-04-10 92.9% (longest hole 34 min); 2026-06-17 94.9% (longest hole 26 min); 2026-06-09 96.3% (longest hole 19 min); 2025-12-31 97.0% (longest hole 4 min); 2025-12-05 97.5% (longest hole 13 min)
- sessions with no bar (first 15 of 2): 2025-01-02, 2026-09-25
- delivered hours (2026, share of NY weekdays with ≥1 bar in each NY hour, %): 00:100 01:100 02:100 03:100 04:100 05:100 06:100 07:100 08:100 09:100 10:100 11:100 12:100 13:100 14:100 15:100 16:88 17:1 18:73 19:80 20:80 21:80 22:80 23:80
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 0

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 4; months without any bar: none
  - 2025-12-24 12:28 → 2025-12-25 23:03 UTC: 1.4 trading days
  - 2025-12-31 18:13 → 2026-01-01 23:02 UTC: 1.2 trading days
  - 2025-04-17 20:13 → 2025-04-20 22:02 UTC: 1.1 trading days
  - 2026-04-02 20:13 → 2026-04-05 22:02 UTC: 1.1 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 0.0%; open == previous close: 0.3% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 0 in 0 sessions

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 32; of which spike-reversals (≥80% retraced next bar): 3
- bar-to-bar level breaks > 25%: 0

## Cross-source

- not computed on hold-out data (outcome-free rule for the hold-out).

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).
- From 2019 the daily halt sits at 16:14 NY in aligned weeks and ~16:59 in mismatch weeks: the CFD's halt follows the London clock (capped by the 17:00 NY close), not a clock error; the release votes put the clock right (16 vs 0). The Jan-Feb vs Jun-Jul US-anchor peaks compete (09:31 vs 08:30); the London 08:00 open anchor is stable.

