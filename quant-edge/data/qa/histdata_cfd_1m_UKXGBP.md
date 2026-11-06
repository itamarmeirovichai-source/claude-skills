# QA — histdata_cfd_1m_UKXGBP

Data QA Auditor, Department C, 2026-11-06 02:19 UTC. Outcome-free: no strategy, signal or P&L is computed.

- path `DATA_ROOT/derived/histdata_cfd_1m/UKXGBP`; rows 3,577,587; 2010-11-15 .. 2024-12-31 (UTC); sha256 `cb2961186e3271dc…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/ukxgbp/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HistData personal use; fetched 2026-11-06; 15 raw zips pinned in fetch_log; clock=histdata_rule (conflict): US anchor: winter peak 09:31 summer peak 08:30 clock; shift -61 min -> est_fixed | Europe/London 08:00 open: winter 03:00 summer 03:00 clock; shift 0 min (ny_dst predicts +0; est_fixed -60) -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 13 agree; 4 disagree (years 2020 2021 2023 2024); 6 undecided | verdict histdata_rule (conflict); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 415 duplicate local stamps dropped; gaps: 71 gaps > 1 weekday-trading-day (longest: 2017-02-17..2017-02-27 5.4d; 2011-12-23..2011-12-28 2.8d; 2014-12-24..2014-12-29 2.8d); months without bars: none

## Verdict: PASS

- no blocking issue found

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 09:31, summer peak 08:30 NY, shift -61 min -> NOT OK.
- After conversion, home-market anchor Europe/London 08:00 (±25 min): winter peak 08:00, summer peak 08:00 local, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 23 CPI/NFP releases; spike at offset 0 (correct) 16, at −60 min (one hour early) 0, undecided 7.
  - offsets (min): 2011-03-17:70 2011-11-04:0 2012-03-16:84 2012-11-02:1 2013-03-15:84 2013-10-30:35 2014-03-18:-53 2015-03-24:-27 2016-03-16:60 2016-11-04:5 2017-03-15:72 2017-11-03:-42 2018-03-13:12 2018-11-02:66 2019-03-12:-66 2019-11-01:0 2020-03-11:60 2021-11-05:60 2022-11-04:5 2023-03-14:88 2023-11-03:0 2024-03-12:27 2024-11-01:5
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 1 same, 0 one hour off, 5 other: 2019 16:14→16:59 2020 15:59→15:59 2021 16:14→16:59 2022 16:14→16:59 2023 16:14→16:59 2024 16:14→17:00
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2010-2018 aligned 16:14 (5/31); 2010-2018 mismatch 02:01 (1/1); 2019+ aligned 16:14 (858/1582); 2019+ mismatch 16:59 (58/125)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (XLON, exchange_calendars, breaks excluded)

- sessions in span 3,568; with ≥1 bar 3,560; with no bar 8; median coverage of sessions with bars 100.0%; sessions ≥95% covered 95.7%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2010 | 33 | 0 | 99.8% | 97.0% | 7 | 0 | 771 |
| 2011 | 251 | 0 | 100.0% | 99.2% | 9 | 1 | 779 |
| 2012 | 252 | 0 | 100.0% | 98.8% | 14 | 0 | 776 |
| 2013 | 253 | 0 | 99.8% | 98.0% | 17 | 1 | 773 |
| 2014 | 253 | 1 | 99.8% | 97.2% | 16 | 3 | 774 |
| 2015 | 253 | 0 | 100.0% | 100.0% | 4 | 0 | 835 |
| 2016 | 253 | 0 | 100.0% | 99.6% | 4 | 0 | 839 |
| 2017 | 252 | 5 | 99.8% | 100.0% | 9 | 5 | 832 |
| 2018 | 253 | 0 | 100.0% | 100.0% | 3 | 0 | 838 |
| 2019 | 253 | 0 | 100.0% | 99.6% | 2 | 0 | 1266 |
| 2020 | 254 | 1 | 100.0% | 100.0% | 3 | 1 | 1301 |
| 2021 | 253 | 1 | 100.0% | 100.0% | 5 | 1 | 1306 |
| 2022 | 250 | 0 | 100.0% | 100.0% | 1 | 0 | 1330 |
| 2023 | 251 | 0 | 97.3% | 52.2% | 348 | 309 | 970 |
| 2024 | 254 | 0 | 100.0% | 94.5% | 61 | 5 | 1301 |

- lowest-coverage sessions (with bars): 2023-07-28 32.9% (longest hole 149 min); 2023-09-21 38.6% (longest hole 313 min); 2023-07-05 51.2% (longest hole 69 min); 2023-03-06 52.9% (longest hole 60 min); 2023-03-09 57.5% (longest hole 67 min)
- sessions with no bar (first 15 of 8): 2014-06-02, 2017-02-20, 2017-02-21, 2017-02-22, 2017-02-23, 2017-02-24, 2020-11-30, 2021-12-24
- delivered hours (2024, share of NY weekdays with ≥1 bar in each NY hour, %): 00:99 01:99 02:99 03:99 04:99 05:99 06:99 07:99 08:99 09:99 10:99 11:99 12:98 13:99 14:98 15:98 16:94 17:3 18:72 19:79 20:79 21:79 22:79 23:79
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 2

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 71; months without any bar: none
  - 2017-02-17 20:59 → 2017-02-27 07:01 UTC: 5.4 trading days
  - 2011-12-23 12:29 → 2011-12-28 08:00 UTC: 2.8 trading days
  - 2014-12-24 12:30 → 2014-12-29 08:00 UTC: 2.8 trading days
  - 2013-12-24 12:31 → 2013-12-27 08:00 UTC: 2.8 trading days
  - 2016-12-23 12:29 → 2016-12-28 07:00 UTC: 2.8 trading days
  - 2017-12-22 12:30 → 2017-12-27 07:01 UTC: 2.8 trading days
  - 2015-12-24 12:30 → 2015-12-29 07:00 UTC: 2.8 trading days
  - 2020-12-24 12:49 → 2020-12-29 01:00 UTC: 2.5 trading days
  - 2012-06-01 19:59 → 2012-06-06 07:00 UTC: 2.5 trading days
  - 2014-04-17 19:59 → 2014-04-22 07:00 UTC: 2.5 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 0.4%; open == previous close: 19.4% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 0 in 0 sessions
- sessions whose last cash-session close equals the previous session's: 7

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 243; of which spike-reversals (≥80% retraced next bar): 6
- bar-to-bar level breaks > 25%: 0
- widest single bar high–low: 168 bp
  - 2020-03-23 01:00 UTC -156 bp
  - 2020-03-09 08:01 UTC +150 bp
  - 2020-03-16 08:36 UTC -142 bp
  - 2020-03-09 08:00 UTC -138 bp (reversed next bar)
  - 2020-03-13 08:05 UTC -132 bp
  - 2020-03-09 01:00 UTC +127 bp
  - 2011-08-05 12:30 UTC +121 bp
  - 2016-06-24 06:18 UTC -118 bp
  - 2011-10-07 12:31 UTC +114 bp
  - 2016-07-14 11:00 UTC -112 bp

## Cross-source agreement (daily log returns, all pre-hold-out dates; outcome-free)

- vs daily_assets_1970_2026.GLSTOCK (global equity index (loose; GBP vs USD)), HistData sampled at America/New_York 16:00 bar close, 2010-11-15..2024-12-31: n=3415, corr lag−1 -0.098, lag0 0.842, lag+1 -0.134; sd ratio other/HistData 1.04

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).
- From 2019 the daily halt sits at 16:14 NY in aligned weeks and ~16:59 in mismatch weeks: the CFD's halt follows the London clock (capped by the 17:00 NY close), not a clock error; the release votes put the clock right (16 vs 0). The Jan-Feb vs Jun-Jul US-anchor peaks compete (09:31 vs 08:30); the London 08:00 open anchor is stable.

