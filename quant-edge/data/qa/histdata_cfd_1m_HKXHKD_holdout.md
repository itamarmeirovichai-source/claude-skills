# QA — histdata_cfd_1m_HKXHKD_holdout

Data QA Auditor, Department C, 2026-11-06 02:18 UTC. Outcome-free: no strategy, signal or P&L is computed. **HOLD-OUT dataset**: structural checks only (no price levels, no return values, no cross-source correlation).

- path `DATA_ROOT/holdout/histdata_cfd_1m/HKXHKD`; rows 373,168; 2025-01-02 .. 2026-10-30 (UTC); sha256 `dc048b8adfb2c6d1…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/hkxhkd/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HOLD-OUT (ts >= 2025-01-01; gateway window 'holdout' only; QA outcome-free); HistData personal use; fetched 2026-11-06; 11 raw zips pinned in fetch_log; clock=histdata_rule (single): US anchor: winter peak 09:30 summer peak 09:30 clock; shift 0 min -> ny_dst | Asia/Hong_Kong 09:15 open: winter 20:15 summer 21:15 clock; shift 60 min (ny_dst predicts +60; est_fixed +0) -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 1 agree; 0 disagree; 1 undecided | verdict histdata_rule (agree); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 0 duplicate local stamps dropped; gaps: 20 gaps > 1 weekday-trading-day (longest: 2025-01-28..2025-02-03 3.9d; 2026-02-16..2026-02-20 3.9d; 2026-04-02..2026-04-08 3.3d); months without bars: none; clock diag on hold-out part itself

## Verdict: PASS

- no blocking issue found

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 09:30, summer peak 09:30 NY, shift 0 min -> OK.
- After conversion, home-market anchor Asia/Hong_Kong 09:15 (±25 min): winter peak 09:15, summer peak 09:15 local, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 2 CPI/NFP releases; spike at offset 0 (correct) 2, at −60 min (one hour early) 0, undecided 0.
  - offsets (min): 2025-03-12:0 2026-03-11:3
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 1 same, 0 one hour off, 1 other: 2025 23:59→04:29 2026 04:29→04:29
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2019+ aligned 04:29 (225/963); 2019+ mismatch 04:29 (31/92)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (XHKG, exchange_calendars, breaks excluded)

- sessions in span 450; with ≥1 bar 448; with no bar 2; median coverage of sessions with bars 100.0%; sessions ≥95% covered 99.3%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2025 | 246 | 1 | 100.0% | 99.6% | 3 | 1 | 840 |
| 2026 | 204 | 1 | 100.0% | 99.0% | 7 | 2 | 840 |

- lowest-coverage sessions (with bars): 2026-05-29 83.9% (longest hole 42 min); 2025-07-28 92.4% (longest hole 25 min); 2026-06-09 94.2% (longest hole 19 min); 2026-02-24 96.1% (longest hole 5 min); 2026-07-20 97.9% (longest hole 7 min)
- sessions with no bar (first 15 of 2): 2025-09-29, 2026-09-25
- delivered hours (2026, share of NY weekdays with ≥1 bar in each NY hour, %): 00:20 01:97 02:97 03:97 04:97 05:97 06:97 07:97 08:97 09:97 10:97 11:97 12:77 13:0 14:0 15:0 16:0 17:0 18:0 19:0 20:16 21:78 22:78 23:62
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 0

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 20; months without any bar: none
  - 2025-01-28 03:59 → 2025-02-03 01:15 UTC: 3.9 trading days
  - 2026-02-16 03:59 → 2026-02-20 01:15 UTC: 3.9 trading days
  - 2026-04-02 16:58 → 2026-04-08 01:15 UTC: 3.3 trading days
  - 2025-12-24 03:59 → 2025-12-29 01:15 UTC: 2.9 trading days
  - 2025-04-17 16:58 → 2025-04-22 01:15 UTC: 2.3 trading days
  - 2025-12-31 03:58 → 2026-01-02 01:15 UTC: 1.9 trading days
  - 2026-06-30 16:57 → 2026-07-02 01:15 UTC: 1.3 trading days
  - 2026-09-30 16:57 → 2026-10-02 01:15 UTC: 1.3 trading days
  - 2026-04-30 16:57 → 2026-05-04 01:15 UTC: 1.3 trading days
  - 2025-04-03 16:58 → 2025-04-07 01:15 UTC: 1.3 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 0.0%; open == previous close: 0.0% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 0 in 0 sessions

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 56; of which spike-reversals (≥80% retraced next bar): 1
- bar-to-bar level breaks > 25%: 0

## Cross-source

- not computed on hold-out data (outcome-free rule for the hold-out).

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).
- GLSTOCK is a loose, US-timed check: an Asian close precedes the US close, so lag +1 carries as much as lag 0. The 2010-2018 winter profile has bad prints near the open (robust anchor still shifts 12 min); the US anchor and the mismatch-week releases place the clock correctly.

