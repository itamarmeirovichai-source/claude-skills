# QA — histdata_cfd_1m_FRXEUR_holdout

Data QA Auditor, Department C, 2026-11-06 02:17 UTC. Outcome-free: no strategy, signal or P&L is computed. **HOLD-OUT dataset**: structural checks only (no price levels, no return values, no cross-source correlation).

- path `DATA_ROOT/holdout/histdata_cfd_1m/FRXEUR`; rows 388,073; 2025-01-02 .. 2026-10-30 (UTC); sha256 `1dcdee3085006298…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/frxeur/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HOLD-OUT (ts >= 2025-01-01; gateway window 'holdout' only; QA outcome-free); HistData personal use; fetched 2026-11-06; 11 raw zips pinned in fetch_log; clock=histdata_rule (agree): US anchor: winter peak 08:30 summer peak 08:30 clock; shift 0 min -> ny_dst | Europe/Paris 08:00 open: winter 02:01 summer 02:01 clock; shift 0 min (ny_dst predicts +0; est_fixed -60) -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 1 agree; 0 disagree; 1 undecided | verdict histdata_rule (agree); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 0 duplicate local stamps dropped; gaps: 7 gaps > 1 weekday-trading-day (longest: 2025-12-24..2025-12-29 2.8d; 2025-04-17..2025-04-22 2.4d; 2026-04-02..2026-04-07 2.4d); months without bars: none; clock diag on hold-out part itself

## Verdict: PASS

- no blocking issue found

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 08:30, summer peak 08:30 NY, shift 0 min -> OK.
- After conversion, home-market anchor Europe/Paris 08:00 (±25 min): winter peak 08:01, summer peak 08:01 local, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 2 CPI/NFP releases; spike at offset 0 (correct) 2, at −60 min (one hour early) 0, undecided 0.
  - offsets (min): 2025-03-12:0 2026-03-11:11
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2019+ aligned 14:09 (1/4); 2019+ mismatch 07:05 (1/1)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (XPAR, exchange_calendars, breaks excluded)

- sessions in span 468; with ≥1 bar 467; with no bar 1; median coverage of sessions with bars 100.0%; sessions ≥95% covered 99.4%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2025 | 255 | 0 | 100.0% | 99.6% | 4 | 1 | 839 |
| 2026 | 213 | 1 | 100.0% | 99.1% | 13 | 3 | 839 |

- lowest-coverage sessions (with bars): 2026-05-11 88.2% (longest hole 60 min); 2025-09-29 88.4% (longest hole 59 min); 2026-03-23 91.8% (longest hole 35 min); 2026-06-09 95.9% (longest hole 19 min); 2025-12-24 96.4% (longest hole 6 min)
- sessions with no bar (first 15 of 1): 2026-09-25
- delivered hours (2026, share of NY weekdays with ≥1 bar in each NY hour, %): 00:0 01:0 02:91 03:100 04:100 05:100 06:100 07:100 08:100 09:100 10:100 11:100 12:100 13:100 14:100 15:100 16:9 17:0 18:0 19:0 20:0 21:0 22:0 23:0
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 0

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 7; months without any bar: none
  - 2025-12-24 12:58 → 2025-12-29 07:00 UTC: 2.8 trading days
  - 2025-04-17 19:58 → 2025-04-22 06:00 UTC: 2.4 trading days
  - 2026-04-02 19:58 → 2026-04-07 06:00 UTC: 2.4 trading days
  - 2025-12-31 12:57 → 2026-01-02 07:00 UTC: 1.8 trading days
  - 2026-04-30 19:57 → 2026-05-04 06:00 UTC: 1.4 trading days
  - 2025-04-30 19:58 → 2025-05-02 06:00 UTC: 1.4 trading days
  - 2026-09-24 19:59 → 2026-09-28 06:00 UTC: 1.4 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 0.0%; open == previous close: 0.0% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 0 in 0 sessions

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 48; of which spike-reversals (≥80% retraced next bar): 3
- bar-to-bar level breaks > 25%: 0

## Cross-source

- not computed on hold-out data (outcome-free rule for the hold-out).

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).

