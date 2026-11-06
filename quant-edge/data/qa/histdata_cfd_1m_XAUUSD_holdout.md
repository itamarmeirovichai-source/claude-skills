# QA — histdata_cfd_1m_XAUUSD_holdout

Data QA Auditor, Department C, 2026-11-06 02:19 UTC. Outcome-free: no strategy, signal or P&L is computed. **HOLD-OUT dataset**: structural checks only (no price levels, no return values, no cross-source correlation).

- path `DATA_ROOT/holdout/histdata_cfd_1m/XAUUSD`; rows 648,140; 2025-01-01 .. 2026-10-30 (UTC); sha256 `72767278a2c36e2a…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/xauusd/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HOLD-OUT (ts >= 2025-01-01; gateway window 'holdout' only; QA outcome-free); HistData personal use; fetched 2026-11-06; 11 raw zips pinned in fetch_log; clock=histdata_rule (single): US anchor: winter peak 08:30 summer peak 08:30 clock; shift 0 min -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 1 agree; 1 disagree (years 2026); 0 undecided | verdict histdata_rule (single); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 1624 duplicate local stamps dropped; gaps: 4 gaps > 1 weekday-trading-day (longest: 2025-12-24..2025-12-25 1.2d; 2025-12-31..2026-01-01 1.0d; 2025-04-17..2025-04-20 1.0d); months without bars: none; clock diag on hold-out part itself

## Verdict: PASS

- no blocking issue found

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 08:30, summer peak 08:30 NY, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 2 CPI/NFP releases; spike at offset 0 (correct) 1, at −60 min (one hour early) 0, undecided 1.
  - offsets (min): 2025-03-12:0 2026-03-11:82
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 2 same, 0 one hour off, 0 other: 2025 16:59→16:59 2026 16:59→16:59
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2019+ aligned 16:59 (332/343); 2019+ mismatch 16:59 (32/33)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (CMES23 = 18:00→17:00 ET futures-style day)

- sessions in span 472; with ≥1 bar 472; with no bar 0; median coverage of sessions with bars 100.0%; sessions ≥95% covered 99.2%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2025 | 257 | 0 | 100.0% | 99.2% | 11 | 4 | 1380 |
| 2026 | 215 | 0 | 100.0% | 99.1% | 6 | 4 | 1380 |

- lowest-coverage sessions (with bars): 2026-09-25 8.7% (longest hole 1260 min); 2025-12-05 73.9% (longest hole 360 min); 2026-06-19 82.5% (longest hole 241 min); 2025-06-19 89.1% (longest hole 151 min); 2025-03-31 95.7% (longest hole 60 min)
- delivered hours (2026, share of NY weekdays with ≥1 bar in each NY hour, %): 00:100 01:100 02:100 03:100 04:100 05:100 06:100 07:100 08:100 09:100 10:100 11:100 12:100 13:99 14:99 15:97 16:97 17:0 18:80 19:80 20:80 21:80 22:80 23:80
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 0

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 4; months without any bar: none
  - 2025-12-24 18:43 → 2025-12-25 23:04 UTC: 1.2 trading days
  - 2025-12-31 21:57 → 2026-01-01 23:00 UTC: 1.0 trading days
  - 2025-04-17 20:58 → 2025-04-20 22:00 UTC: 1.0 trading days
  - 2026-04-02 20:58 → 2026-04-05 22:00 UTC: 1.0 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 0.1%; open == previous close: 16.2% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 0 in 0 sessions

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 154; of which spike-reversals (≥80% retraced next bar): 4
- bar-to-bar level breaks > 25%: 0

## Cross-source

- not computed on hold-out data (outcome-free rule for the hold-out).

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).
- GOLDPM in daily_assets_1970_2026 correlates 0.63 at lag 0 and 0.38 at lag +1, stable in every year 2010-2024: the second source mixes same-day and next-day dating. XAUUSD's clock checks pass, so the shortfall is attributed to GOLDPM.

