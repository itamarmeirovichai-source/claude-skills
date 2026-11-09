# QA — histdata_cfd_1m_FRXEUR

Data QA Auditor, Department C, 2026-11-06 02:18 UTC. Outcome-free: no strategy, signal or P&L is computed.

- path `DATA_ROOT/derived/histdata_cfd_1m/FRXEUR`; rows 2,958,952; 2010-11-15 .. 2024-12-31 (UTC); sha256 `e54c8fa571468761…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/frxeur/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HistData personal use; fetched 2026-11-06; 15 raw zips pinned in fetch_log; clock=histdata_rule (agree): US anchor: winter peak 08:30 summer peak 08:30 clock; shift 0 min -> ny_dst | Europe/Paris 08:00 open: winter 02:00 summer 02:00 clock; shift 0 min (ny_dst predicts +0; est_fixed -60) -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 15 agree; 3 disagree (years 2013 2015 2020); 4 undecided | verdict histdata_rule (agree); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 0 duplicate local stamps dropped; gaps: 46 gaps > 1 weekday-trading-day (longest: 2017-02-17..2017-02-27 5.4d; 2013-12-24..2013-12-27 2.8d; 2014-12-24..2014-12-29 2.8d); months without bars: none

## Verdict: PASS

- no blocking issue found

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 08:30, summer peak 08:30 NY, shift 0 min -> OK.
- After conversion, home-market anchor Europe/Paris 08:00 (±25 min): winter peak 08:00, summer peak 08:00 local, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 23 CPI/NFP releases; spike at offset 0 (correct) 14, at −60 min (one hour early) 3, undecided 6.
  - offsets (min): 2011-03-17:31 2011-11-04:44 2012-03-16:85 2012-11-02:0 2013-03-15:84 2013-10-30:72 2014-03-18:-53 2015-03-24:14 2016-03-16:60 2016-11-04:79 2017-03-15:-83 2017-11-03:90 2018-03-13:12 2018-11-02:-19 2019-03-12:-87 2019-11-01:0 2020-03-11:69 2021-11-05:32 2022-11-04:5 2023-03-14:79 2023-11-03:0 2024-03-12:1 2024-11-01:10
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 0 same, 0 one hour off, 2 other: 2019 16:14→16:59 2023 05:59→07:59
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2010-2018 aligned 16:14 (5/48); 2010-2018 mismatch 15:59 (1/2); 2019+ aligned 05:59 (40/462); 2019+ mismatch 16:59 (12/74)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (XPAR, exchange_calendars, breaks excluded)

- sessions in span 3,619; with ≥1 bar 3,612; with no bar 7; median coverage of sessions with bars 100.0%; sessions ≥95% covered 94.3%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2010 | 35 | 0 | 99.6% | 82.9% | 6 | 1 | 824 |
| 2011 | 257 | 0 | 100.0% | 97.7% | 10 | 3 | 837 |
| 2012 | 256 | 0 | 99.8% | 98.0% | 17 | 0 | 822 |
| 2013 | 255 | 0 | 99.2% | 95.3% | 26 | 1 | 814 |
| 2014 | 255 | 1 | 99.4% | 90.2% | 34 | 2 | 816 |
| 2015 | 256 | 0 | 100.0% | 98.4% | 24 | 1 | 838 |
| 2016 | 257 | 0 | 100.0% | 97.7% | 15 | 2 | 838 |
| 2017 | 255 | 5 | 99.4% | 94.4% | 19 | 6 | 820 |
| 2018 | 255 | 1 | 100.0% | 99.6% | 14 | 2 | 834 |
| 2019 | 255 | 0 | 100.0% | 98.8% | 5 | 1 | 840 |
| 2020 | 257 | 0 | 100.0% | 99.6% | 4 | 1 | 839 |
| 2021 | 258 | 0 | 100.0% | 98.8% | 8 | 1 | 839 |
| 2022 | 257 | 0 | 100.0% | 99.2% | 7 | 2 | 840 |
| 2023 | 255 | 0 | 100.0% | 55.3% | 313 | 311 | 833 |
| 2024 | 256 | 0 | 100.0% | 98.0% | 6 | 4 | 840 |

- lowest-coverage sessions (with bars): 2023-03-17 52.9% (longest hole 120 min); 2023-07-13 52.9% (longest hole 240 min); 2023-02-20 58.8% (longest hole 90 min); 2023-02-21 58.8% (longest hole 90 min); 2023-02-23 58.8% (longest hole 60 min)
- sessions with no bar (first 15 of 7): 2014-06-02, 2017-02-20, 2017-02-21, 2017-02-22, 2017-02-23, 2017-02-24, 2018-12-31
- delivered hours (2024, share of NY weekdays with ≥1 bar in each NY hour, %): 00:0 01:0 02:93 03:100 04:100 05:100 06:100 07:100 08:99 09:99 10:99 11:99 12:99 13:98 14:98 15:98 16:7 17:0 18:0 19:0 20:0 21:0 22:0 23:0
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 0

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 46; months without any bar: none
  - 2017-02-17 20:59 → 2017-02-27 07:01 UTC: 5.4 trading days
  - 2013-12-24 11:58 → 2013-12-27 07:01 UTC: 2.8 trading days
  - 2014-12-24 12:00 → 2014-12-29 07:00 UTC: 2.8 trading days
  - 2024-12-24 12:53 → 2024-12-27 07:00 UTC: 2.8 trading days
  - 2012-12-24 12:59 → 2012-12-27 07:01 UTC: 2.8 trading days
  - 2019-12-24 12:59 → 2019-12-27 07:00 UTC: 2.8 trading days
  - 2018-12-24 12:59 → 2018-12-27 00:17 UTC: 2.5 trading days
  - 2023-04-06 18:59 → 2023-04-11 06:00 UTC: 2.5 trading days
  - 2022-04-14 19:58 → 2022-04-19 06:00 UTC: 2.4 trading days
  - 2017-12-22 20:59 → 2017-12-27 07:01 UTC: 2.4 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 1.0%; open == previous close: 19.3% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 1 in 1 sessions
- sessions whose last cash-session close equals the previous session's: 15

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 353; of which spike-reversals (≥80% retraced next bar): 18
- bar-to-bar level breaks > 25%: 0
- widest single bar high–low: 277 bp
  - 2022-03-11 11:26 UTC +182 bp
  - 2020-03-12 12:46 UTC -165 bp
  - 2015-01-15 09:51 UTC -152 bp
  - 2011-09-01 14:00 UTC +143 bp
  - 2022-10-13 12:30 UTC -137 bp
  - 2011-11-30 13:00 UTC +135 bp
  - 2024-10-15 15:45 UTC -132 bp
  - 2020-03-13 15:56 UTC +131 bp
  - 2012-05-30 11:00 UTC +127 bp
  - 2020-03-03 15:00 UTC +124 bp

## Cross-source agreement (daily log returns, all pre-hold-out dates; outcome-free)

- vs daily_assets_1970_2026.GLSTOCK (global equity index (loose; EUR vs USD)), HistData sampled at America/New_York 16:00 bar close, 2010-11-15..2024-12-30: n=3431, corr lag−1 -0.092, lag0 0.869, lag+1 -0.116; sd ratio other/HistData 0.84

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).

