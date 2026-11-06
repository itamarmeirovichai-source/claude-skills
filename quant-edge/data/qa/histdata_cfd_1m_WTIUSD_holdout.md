# QA — histdata_cfd_1m_WTIUSD_holdout

Data QA Auditor, Department C, 2026-11-06 02:19 UTC. Outcome-free: no strategy, signal or P&L is computed. **HOLD-OUT dataset**: structural checks only (no price levels, no return values, no cross-source correlation).

- path `DATA_ROOT/holdout/histdata_cfd_1m/WTIUSD`; rows 122,309; 2026-06-28 .. 2026-10-30 (UTC); sha256 `1d52800cd3267115…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/wtiusd/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HOLD-OUT (ts >= 2025-01-01; gateway window 'holdout' only; QA outcome-free); HistData personal use; fetched 2026-11-06; 5 raw zips pinned in fetch_log; clock=histdata_rule (single): US anchor: winter peak n/a summer peak 09:00 clock; shift None min -> unclear | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 0 agree; 0 disagree; 0 undecided | verdict histdata_rule (default); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 312 duplicate local stamps dropped; gaps: 0 gaps > 1 weekday-trading-day (longest: none); months without bars: none; clock diag on hold-out part itself; periods listed but not downloaded: 2024;2025;2026-01;2026-02;2026-03;2026-04;2026-05

## Verdict: PASS with caveats

- clock not testable on this span (no Jan–Feb or no Jun–Jul bars); conversion follows the measured HistData rule

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak n/a, summer peak 09:00 NY, shift None min -> NOT OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 0 CPI/NFP releases; spike at offset 0 (correct) 0, at −60 min (one hour early) 0, undecided 0.
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 1 same, 0 one hour off, 0 other: 2026 16:59→16:59
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2019+ aligned 16:59 (63/68); 2019+ mismatch 16:59 (4/4)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (CMES23 = 18:00→17:00 ET futures-style day)

- sessions in span 90; with ≥1 bar 90; with no bar 0; median coverage of sessions with bars 99.9%; sessions ≥95% covered 98.9%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2026 | 90 | 0 | 99.9% | 98.9% | 6 | 1 | 1378 |

- lowest-coverage sessions (with bars): 2026-09-25 8.7% (longest hole 1260 min); 2026-07-03 97.8% (longest hole 4 min); 2026-08-17 98.5% (longest hole 20 min); 2026-10-15 98.6% (longest hole 20 min); 2026-07-16 98.6% (longest hole 19 min)
- delivered hours (2026, share of NY weekdays with ≥1 bar in each NY hour, %): 00:100 01:100 02:100 03:100 04:100 05:100 06:100 07:100 08:100 09:100 10:100 11:100 12:100 13:99 14:99 15:98 16:98 17:0 18:81 19:81 20:80 21:80 22:80 23:80
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 0

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 0; months without any bar: none

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 0.6%; open == previous close: 3.7% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 0 in 0 sessions

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 35; of which spike-reversals (≥80% retraced next bar): 0
- bar-to-bar level breaks > 25%: 0

## Cross-source

- not computed on hold-out data (outcome-free rule for the hold-out).

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).
- HistData offers no WTIUSD file for 2024 and 2025 or for 2026-01..05 (empty tokens); IS ends 2023-12-01 and the hold-out part is 2026-06-28 .. 2026-10-30 only. The two level breaks are real: the 2020-03-09 OPEC+ gap and the 2020-04-19 CFD roll after the negative-price May contract.

