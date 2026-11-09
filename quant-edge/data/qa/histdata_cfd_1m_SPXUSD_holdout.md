# QA — histdata_cfd_1m_SPXUSD_holdout

Data QA Auditor, Department C, 2026-11-06 02:18 UTC. Outcome-free: no strategy, signal or P&L is computed. **HOLD-OUT dataset**: structural checks only (no price levels, no return values, no cross-source correlation).

- path `DATA_ROOT/holdout/histdata_cfd_1m/SPXUSD`; rows 623,058; 2025-01-01 .. 2026-10-30 (UTC); sha256 `b5ff5df98e257180…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/spxusd/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HOLD-OUT (ts >= 2025-01-01; gateway window 'holdout' only; QA outcome-free); HistData personal use; fetched 2026-11-06; 11 raw zips pinned in fetch_log; clock=histdata_rule (single): US anchor: winter peak 08:30 summer peak 09:30 clock; shift 60 min -> unclear | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 1 agree; 1 disagree (years 2026); 0 undecided | verdict histdata_rule (default); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 425 duplicate local stamps dropped; gaps: 4 gaps > 1 weekday-trading-day (longest: 2025-12-24..2025-12-25 1.2d; 2025-12-31..2026-01-01 1.1d; 2025-04-17..2025-04-20 1.1d); months without bars: none; clock diag on hold-out part itself

## Verdict: PASS with caveats

- Jan–Feb vs Jun–Jul peaks differ (competing 08:30/09:30 spikes), but the mismatch-week halt and release checks place the clock correctly

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 08:30, summer peak 09:30 NY, shift 60 min -> NOT OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 2 CPI/NFP releases; spike at offset 0 (correct) 2, at −60 min (one hour early) 0, undecided 0.
  - offsets (min): 2025-03-12:0 2026-03-11:90
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 2 same, 0 one hour off, 0 other: 2025 16:14→16:14 2026 16:14→16:14
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2019+ aligned 16:14 (331/348); 2019+ mismatch 16:14 (32/32)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (XNYS, exchange_calendars, breaks excluded)

- sessions in span 459; with ≥1 bar 458; with no bar 1; median coverage of sessions with bars 100.0%; sessions ≥95% covered 100.0%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2025 | 250 | 0 | 100.0% | 100.0% | 1 | 0 | 1326 |
| 2026 | 209 | 1 | 100.0% | 100.0% | 4 | 1 | 1334 |

- lowest-coverage sessions (with bars): 2025-09-26 96.2% (longest hole 15 min); 2026-06-08 96.4% (longest hole 13 min); 2026-03-24 97.7% (longest hole 9 min); 2025-04-07 98.2% (longest hole 4 min); 2026-08-13 98.7% (longest hole 5 min)
- sessions with no bar (first 15 of 1): 2026-09-25
- delivered hours (2026, share of NY weekdays with ≥1 bar in each NY hour, %): 00:100 01:100 02:100 03:100 04:100 05:100 06:100 07:100 08:100 09:100 10:100 11:100 12:100 13:97 14:97 15:97 16:97 17:0 18:80 19:80 20:80 21:80 22:80 23:80
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 0

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 4; months without any bar: none
  - 2025-12-24 18:13 → 2025-12-25 23:00 UTC: 1.2 trading days
  - 2025-12-31 21:12 → 2026-01-01 23:00 UTC: 1.1 trading days
  - 2025-04-17 20:13 → 2025-04-20 22:00 UTC: 1.1 trading days
  - 2026-04-02 20:13 → 2026-04-05 22:00 UTC: 1.1 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 0.0%; open == previous close: 0.1% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 0 in 0 sessions

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 75; of which spike-reversals (≥80% retraced next bar): 5
- bar-to-bar level breaks > 25%: 0

## Cross-source

- not computed on hold-out data (outcome-free rule for the hold-out).

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).
- This dataset also supersedes the inherited SPXUSD 2010-18 (FutureSharks copy): the yearly CSVs are byte-identical.

