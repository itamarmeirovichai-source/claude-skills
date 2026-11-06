# QA — histdata_cfd_1m_GRXEUR_holdout

Data QA Auditor, Department C, 2026-11-06 02:18 UTC. Outcome-free: no strategy, signal or P&L is computed. **HOLD-OUT dataset**: structural checks only (no price levels, no return values, no cross-source correlation).

- path `DATA_ROOT/holdout/histdata_cfd_1m/GRXEUR`; rows 618,735; 2025-01-01 .. 2026-10-30 (UTC); sha256 `edb0d63112412cd6…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/grxeur/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HOLD-OUT (ts >= 2025-01-01; gateway window 'holdout' only; QA outcome-free); HistData personal use; fetched 2026-11-06; 11 raw zips pinned in fetch_log; clock=histdata_rule (agree): US anchor: winter peak 08:30 summer peak 08:30 clock; shift 0 min -> ny_dst | Europe/Berlin 09:00 open: winter 03:00 summer 03:00 clock; shift 0 min (ny_dst predicts +0; est_fixed -60) -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 1 agree; 0 disagree; 1 undecided | verdict histdata_rule (agree); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 176 duplicate local stamps dropped; gaps: 4 gaps > 1 weekday-trading-day (longest: 2025-12-24..2025-12-25 1.2d; 2025-12-31..2026-01-01 1.1d; 2025-04-17..2025-04-20 1.1d); months without bars: none; clock diag on hold-out part itself

## Verdict: PASS

- no blocking issue found

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 08:30, summer peak 08:30 NY, shift 0 min -> OK.
- After conversion, home-market anchor Europe/Berlin 09:00 (±25 min): winter peak 09:00, summer peak 09:00 local, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 2 CPI/NFP releases; spike at offset 0 (correct) 2, at −60 min (one hour early) 0, undecided 0.
  - offsets (min): 2025-03-12:0 2026-03-11:90
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 0 same, 0 one hour off, 2 other: 2025 16:14→17:00 2026 16:14→17:00
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2019+ aligned 16:14 (331/347); 2019+ mismatch 17:00 (22/32)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (XETR, exchange_calendars, breaks excluded)

- sessions in span 466; with ≥1 bar 465; with no bar 1; median coverage of sessions with bars 100.0%; sessions ≥95% covered 99.6%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2025 | 253 | 0 | 100.0% | 99.6% | 8 | 1 | 1305 |
| 2026 | 213 | 1 | 100.0% | 99.5% | 6 | 1 | 1324 |

- lowest-coverage sessions (with bars): 2025-01-20 72.0% (longest hole 143 min); 2026-04-10 94.7% (longest hole 25 min); 2026-07-20 95.5% (longest hole 23 min); 2026-06-17 95.9% (longest hole 21 min); 2026-06-09 96.1% (longest hole 19 min)
- sessions with no bar (first 15 of 1): 2026-09-25
- delivered hours (2026, share of NY weekdays with ≥1 bar in each NY hour, %): 00:100 01:100 02:100 03:100 04:100 05:100 06:100 07:100 08:100 09:100 10:100 11:100 12:100 13:100 14:100 15:100 16:85 17:5 18:73 19:80 20:80 21:80 22:80 23:80
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 5

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 4; months without any bar: none
  - 2025-12-24 18:13 → 2025-12-25 23:04 UTC: 1.2 trading days
  - 2025-12-31 20:57 → 2026-01-01 23:02 UTC: 1.1 trading days
  - 2025-04-17 20:13 → 2025-04-20 22:04 UTC: 1.1 trading days
  - 2026-04-02 20:13 → 2026-04-05 22:02 UTC: 1.1 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 0.0%; open == previous close: 0.1% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 0 in 0 sessions

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 79; of which spike-reversals (≥80% retraced next bar): 6
- bar-to-bar level breaks > 25%: 0

## Cross-source

- not computed on hold-out data (outcome-free rule for the hold-out).

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).
- Bars 2020-06-15 06:00 .. 2023-12-01 20:59 UTC (637,707) are EXCLUDED: the HistData GRXEUR files carry Euro Stoxx 50 levels (2,908-4,490) there, while DAX sits at 12,011 before and 16,429 after. Hence the months without bars and the one level break across the hole. The excluded span is NOT landed as an ETXEUR substitute (provenance is a guess).

