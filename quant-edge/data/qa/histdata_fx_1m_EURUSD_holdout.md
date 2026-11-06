# QA — histdata_fx_1m_EURUSD_holdout

Data QA Auditor, Department C, 2026-11-06 02:19 UTC. Outcome-free: no strategy, signal or P&L is computed. **HOLD-OUT dataset**: structural checks only (no price levels, no return values, no cross-source correlation).

- path `DATA_ROOT/holdout/histdata_fx_1m/EURUSD`; rows 679,893; 2025-01-01 .. 2026-10-30 (UTC); sha256 `77b57992a899c83b…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/eurusd/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HOLD-OUT (ts >= 2025-01-01; gateway window 'holdout' only; QA outcome-free); HistData personal use; fetched 2026-11-06; 11 raw zips pinned in fetch_log; clock=histdata_rule (single): US anchor: winter peak 08:30 summer peak 08:30 clock; shift 0 min -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 1 agree; 0 disagree; 1 undecided | verdict histdata_rule (single); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 66 duplicate local stamps dropped; gaps: 1 gaps > 1 weekday-trading-day (longest: 2025-12-31..2026-01-01 1.0d); months without bars: none; clock diag on hold-out part itself

## Verdict: PASS

- no blocking issue found

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 08:30, summer peak 08:30 NY, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 2 CPI/NFP releases; spike at offset 0 (correct) 2, at −60 min (one hour early) 0, undecided 0.
  - offsets (min): 2025-03-12:0 2026-03-11:90
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2019+ aligned 18:28 (1/4)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (CMES23 = 18:00→17:00 ET futures-style day)

- sessions in span 472; with ≥1 bar 472; with no bar 0; median coverage of sessions with bars 99.9%; sessions ≥95% covered 99.4%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2025 | 257 | 0 | 99.9% | 100.0% | 3 | 1 | 1436 |
| 2026 | 215 | 0 | 99.9% | 98.6% | 8 | 8 | 1434 |

- lowest-coverage sessions (with bars): 2026-09-25 8.6% (longest hole 1260 min); 2026-05-22 73.1% (longest hole 180 min); 2026-05-12 86.7% (longest hole 120 min); 2025-03-31 95.6% (longest hole 60 min); 2026-03-30 95.7% (longest hole 60 min)
- delivered hours (2026, share of NY weekdays with ≥1 bar in each NY hour, %): 00:100 01:100 02:100 03:99 04:100 05:100 06:100 07:100 08:99 09:99 10:100 11:100 12:99 13:99 14:99 15:99 16:99 17:80 18:80 19:80 20:80 21:80 22:80 23:80
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 0

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 1; months without any bar: none
  - 2025-12-31 21:57 → 2026-01-01 22:04 UTC: 1.0 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 0.5%; open == previous close: 26.3% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 0 in 0 sessions

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 4; of which spike-reversals (≥80% retraced next bar): 0
- bar-to-bar level breaks > 25%: 0

## Cross-source

- not computed on hold-out data (outcome-free rule for the hold-out).

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).

