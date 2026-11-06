# QA — histdata_cfd_1m_HKXHKD

Data QA Auditor, Department C, 2026-11-06 02:18 UTC. Outcome-free: no strategy, signal or P&L is computed.

- path `DATA_ROOT/derived/histdata_cfd_1m/HKXHKD`; rows 2,429,602; 2010-11-15 .. 2024-12-31 (UTC); sha256 `ca9df94acffed077…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/hkxhkd/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HistData personal use; fetched 2026-11-06; 15 raw zips pinned in fetch_log; clock=histdata_rule (single): US anchor: winter peak 09:31 summer peak 09:30 clock; shift -1 min -> ny_dst | Asia/Hong_Kong 09:15 open: winter 20:03 summer 21:15 clock; shift 72 min (ny_dst predicts +60; est_fixed +0) -> unclear | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 11 agree; 3 disagree (years 2014 2020 2021); 4 undecided | verdict histdata_rule (single); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 0 duplicate local stamps dropped; gaps: 144 gaps > 1 weekday-trading-day (longest: 2017-02-17..2017-02-27 5.4d; 2019-02-01..2019-02-11 5.3d; 2022-01-31..2022-02-04 3.9d); months without bars: none

## Verdict: PASS

- no blocking issue found

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 09:31, summer peak 09:30 NY, shift -1 min -> OK.
- After conversion, home-market anchor Asia/Hong_Kong 09:15 (±25 min): winter peak 09:03, summer peak 09:15 local, shift 12 min -> NOT OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 17 CPI/NFP releases; spike at offset 0 (correct) 10, at −60 min (one hour early) 1, undecided 6.
  - offsets (min): 2013-10-30:69 2014-03-18:-48 2015-03-24:8 2016-03-16:21 2016-11-04:70 2017-03-15:79 2017-11-03:0 2018-03-13:0 2018-11-02:-16 2019-03-12:67 2019-11-01:0 2020-03-11:5 2021-11-05:60 2022-11-04:63 2023-11-03:0 2024-03-12:5 2024-11-01:62
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 7 same, 0 one hour off, 7 other: 2011 23:59→23:59 2012 23:59→23:59 2013 23:59→00:00 2014 04:14→04:14 2015 11:44→11:44 2016 11:44→11:44 2017 11:44→11:44 2018 12:59→12:59 2019 23:59→04:29 2020 04:29→23:59 2021 23:59→04:29 2022 04:29→23:59 2023 23:59→04:29 2024 23:59→04:29
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2010-2018 aligned 23:59 (616/3620); 2010-2018 mismatch 23:59 (65/229); 2019+ aligned 23:59 (691/3426); 2019+ mismatch 04:29 (82/263)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (XHKG, exchange_calendars, breaks excluded)

- sessions in span 3,479; with ≥1 bar 3,467; with no bar 12; median coverage of sessions with bars 100.0%; sessions ≥95% covered 88.3%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2010 | 34 | 1 | 57.3% | 0.0% | 81 | 32 | 110 |
| 2011 | 246 | 0 | 89.5% | 8.9% | 446 | 210 | 292 |
| 2012 | 247 | 0 | 100.0% | 78.1% | 67 | 48 | 360 |
| 2013 | 244 | 0 | 100.0% | 90.2% | 38 | 9 | 620 |
| 2014 | 247 | 0 | 100.0% | 93.1% | 21 | 8 | 675 |
| 2015 | 247 | 0 | 100.0% | 96.4% | 13 | 4 | 739 |
| 2016 | 245 | 0 | 100.0% | 96.7% | 6 | 0 | 763 |
| 2017 | 246 | 5 | 100.0% | 95.0% | 22 | 5 | 754 |
| 2018 | 246 | 0 | 100.0% | 98.8% | 7 | 0 | 840 |
| 2019 | 246 | 2 | 100.0% | 98.8% | 9 | 4 | 840 |
| 2020 | 248 | 0 | 100.0% | 97.2% | 8 | 5 | 840 |
| 2021 | 247 | 0 | 100.0% | 98.8% | 4 | 2 | 840 |
| 2022 | 246 | 1 | 100.0% | 98.8% | 4 | 4 | 840 |
| 2023 | 245 | 3 | 100.0% | 99.2% | 5 | 5 | 675 |
| 2024 | 245 | 0 | 100.0% | 99.2% | 6 | 1 | 840 |

- lowest-coverage sessions (with bars): 2015-02-16 4.5% (longest hole 165 min); 2010-12-28 19.7% (longest hole 241 min); 2010-12-03 21.0% (longest hole 237 min); 2010-11-17 23.7% (longest hole 229 min); 2011-01-06 27.0% (longest hole 219 min)
- sessions with no bar (first 15 of 12): 2010-12-31, 2017-02-20, 2017-02-21, 2017-02-22, 2017-02-23, 2017-02-24, 2019-02-04, 2019-02-08, 2022-01-03, 2023-05-29, 2023-09-01, 2023-09-08
- delivered hours (2024, share of NY weekdays with ≥1 bar in each NY hour, %): 00:33 01:96 02:96 03:96 04:96 05:95 06:95 07:95 08:95 09:95 10:95 11:95 12:62 13:0 14:0 15:0 16:0 17:0 18:0 19:0 20:28 21:78 22:78 23:50
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 0

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 144; months without any bar: none
  - 2017-02-17 15:44 → 2017-02-27 01:15 UTC: 5.4 trading days
  - 2019-02-01 16:59 → 2019-02-11 01:15 UTC: 5.3 trading days
  - 2022-01-31 03:59 → 2022-02-04 01:15 UTC: 3.9 trading days
  - 2012-01-20 08:14 → 2012-01-26 01:20 UTC: 3.7 trading days
  - 2013-02-08 08:14 → 2013-02-14 01:15 UTC: 3.7 trading days
  - 2016-02-05 15:44 → 2016-02-11 01:15 UTC: 3.4 trading days
  - 2015-04-02 15:44 → 2015-04-08 01:15 UTC: 3.4 trading days
  - 2023-01-20 16:58 → 2023-01-26 01:15 UTC: 3.3 trading days
  - 2021-04-01 16:59 → 2021-04-07 01:15 UTC: 3.3 trading days
  - 2020-01-24 03:59 → 2020-01-29 02:04 UTC: 2.9 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 0.2%; open == previous close: 0.7% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 0 in 0 sessions
- sessions whose last cash-session close equals the previous session's: 4

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 275; of which spike-reversals (≥80% retraced next bar): 8
- bar-to-bar level breaks > 25%: 0
- widest single bar high–low: 482 bp
  - 2011-03-09 00:45 UTC -752 bp
  - 2011-01-14 01:44 UTC +268 bp
  - 2024-10-14 13:43 UTC +187 bp
  - 2010-12-16 01:45 UTC +178 bp
  - 2011-01-04 01:40 UTC -157 bp
  - 2011-02-11 01:45 UTC +149 bp
  - 2011-01-03 08:15 UTC -146 bp
  - 2011-02-11 01:40 UTC +136 bp
  - 2024-10-08 02:36 UTC +128 bp
  - 2010-12-15 06:35 UTC -128 bp

## Cross-source agreement (daily log returns, all pre-hold-out dates; outcome-free)

- vs daily_assets_1970_2026.GLSTOCK (global equity index (loose; Asia close precedes US)), HistData sampled at Asia/Hong_Kong 16:00 bar close, 2010-11-15..2024-12-30: n=3347, corr lag−1 -0.004, lag0 0.304, lag+1 0.321; sd ratio other/HistData 0.82

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).
- GLSTOCK is a loose, US-timed check: an Asian close precedes the US close, so lag +1 carries as much as lag 0. The 2010-2018 winter profile has bad prints near the open (robust anchor still shifts 12 min); the US anchor and the mismatch-week releases place the clock correctly.

