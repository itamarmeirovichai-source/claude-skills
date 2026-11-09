# QA — histdata_cfd_1m_JPXJPY

Data QA Auditor, Department C, 2026-11-06 02:18 UTC. Outcome-free: no strategy, signal or P&L is computed.

- path `DATA_ROOT/derived/histdata_cfd_1m/JPXJPY`; rows 3,764,103; 2010-11-14 .. 2024-12-31 (UTC); sha256 `8b8c09dfb61a248d…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/jpxjpy/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HistData personal use; fetched 2026-11-06; 15 raw zips pinned in fetch_log; clock=histdata_rule (agree): US anchor: winter peak 08:30 summer peak 08:30 clock; shift 0 min -> ny_dst | Asia/Tokyo 09:00 open: winter 19:00 summer 20:00 clock; shift 60 min (ny_dst predicts +60; est_fixed +0) -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 15 agree; 0 disagree; 5 undecided | verdict histdata_rule (agree); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 418 duplicate local stamps dropped; gaps: 38 gaps > 1 weekday-trading-day (longest: 2017-02-17..2017-02-26 5.0d; 2012-12-24..2012-12-26 1.7d; 2013-12-24..2013-12-26 1.7d); months without bars: none

## Verdict: PASS with caveats

- 35 spike-reversal prints

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 08:30, summer peak 08:30 NY, shift 0 min -> OK.
- After conversion, home-market anchor Asia/Tokyo 09:00 (±25 min): winter peak 09:00, summer peak 09:00 local, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 20 CPI/NFP releases; spike at offset 0 (correct) 16, at −60 min (one hour early) 0, undecided 4.
  - offsets (min): 2011-03-17:-84 2011-11-04:0 2012-11-02:0 2013-10-30:72 2014-03-18:-53 2015-03-24:0 2016-03-16:30 2016-11-04:85 2017-11-03:0 2018-03-13:12 2018-11-02:60 2019-03-12:-67 2019-11-01:0 2020-03-11:-10 2021-11-05:0 2022-11-04:2 2023-03-14:0 2023-11-03:0 2024-03-12:0 2024-11-01:0
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 11 same, 0 one hour off, 3 other: 2011 17:30→16:51 2012 17:29→07:42 2013 17:14→17:15 2014 17:14→17:14 2015 17:14→17:15 2016 16:59→16:59 2017 16:59→16:59 2018 16:59→17:00 2019 16:14→16:14 2020 16:14→16:14 2021 16:14→16:14 2022 16:14→16:14 2023 16:14→12:59 2024 16:14→16:14
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2010-2018 aligned 16:59 (372/3187); 2010-2018 mismatch 17:15 (22/179); 2019+ aligned 16:14 (903/1633); 2019+ mismatch 16:14 (72/123)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (XTKS, exchange_calendars, breaks excluded)

- sessions in span 3,458; with ≥1 bar 3,423; with no bar 35; median coverage of sessions with bars 93.3%; sessions ≥95% covered 46.2%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2010 | 32 | 1 | 54.0% | 0.0% | 225 | 6 | 556 |
| 2011 | 245 | 2 | 61.7% | 2.1% | 1192 | 6 | 693 |
| 2012 | 248 | 2 | 62.7% | 0.0% | 916 | 3 | 577 |
| 2013 | 245 | 3 | 92.3% | 37.6% | 43 | 4 | 948 |
| 2014 | 244 | 3 | 86.3% | 17.8% | 285 | 4 | 897 |
| 2015 | 244 | 1 | 90.0% | 30.5% | 116 | 2 | 991 |
| 2016 | 245 | 2 | 94.7% | 49.8% | 103 | 3 | 1056 |
| 2017 | 247 | 7 | 77.7% | 5.4% | 608 | 9 | 817 |
| 2018 | 245 | 2 | 96.3% | 57.6% | 57 | 2 | 1080 |
| 2019 | 241 | 2 | 87.0% | 18.8% | 237 | 3 | 978 |
| 2020 | 242 | 2 | 99.0% | 75.4% | 45 | 3 | 1175 |
| 2021 | 245 | 1 | 99.7% | 95.5% | 5 | 3 | 1219 |
| 2022 | 244 | 2 | 99.3% | 85.5% | 29 | 5 | 1263 |
| 2023 | 246 | 3 | 99.7% | 76.1% | 37 | 3 | 953 |
| 2024 | 245 | 2 | 100.0% | 99.6% | 6 | 3 | 1298 |

- lowest-coverage sessions (with bars): 2011-12-27 0.3% (longest hole 173 min); 2010-12-24 2.0% (longest hole 97 min); 2022-02-21 6.7% (longest hole 45 min); 2010-12-27 26.7% (longest hole 22 min); 2011-05-02 27.0% (longest hole 150 min)
- sessions with no bar (first 15 of 35): 2010-11-29, 2011-04-22, 2011-12-26, 2012-12-25, 2012-12-26, 2013-03-29, 2013-12-25, 2013-12-26, 2014-04-18, 2014-06-02, 2014-12-25, 2015-12-25, 2016-03-25, 2016-12-26, 2017-02-20
- delivered hours (2024, share of NY weekdays with ≥1 bar in each NY hour, %): 00:99 01:99 02:98 03:98 04:98 05:99 06:99 07:99 08:99 09:99 10:99 11:99 12:99 13:96 14:95 15:95 16:95 17:0 18:79 19:79 20:79 21:79 22:79 23:79
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 0

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 38; months without any bar: none
  - 2017-02-17 21:59 → 2017-02-26 23:01 UTC: 5.0 trading days
  - 2012-12-24 18:14 → 2012-12-26 11:00 UTC: 1.7 trading days
  - 2013-12-24 18:15 → 2013-12-26 11:01 UTC: 1.7 trading days
  - 2013-12-31 20:58 → 2014-01-02 11:01 UTC: 1.6 trading days
  - 2011-12-30 21:11 → 2012-01-03 11:00 UTC: 1.6 trading days
  - 2012-12-31 21:53 → 2013-01-02 11:00 UTC: 1.5 trading days
  - 2018-12-24 17:59 → 2018-12-25 23:09 UTC: 1.2 trading days
  - 2023-07-03 16:59 → 2023-07-04 22:00 UTC: 1.2 trading days
  - 2019-12-24 18:14 → 2019-12-25 23:11 UTC: 1.2 trading days
  - 2011-12-23 21:15 → 2011-12-27 02:06 UTC: 1.2 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 8.9%; open == previous close: 11.9% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 9 in 9 sessions
- sessions whose last cash-session close equals the previous session's: 23

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 422; of which spike-reversals (≥80% retraced next bar): 35
- bar-to-bar level breaks > 25%: 0
- widest single bar high–low: 1220 bp
  - 2011-03-15 13:32 UTC -1155 bp
  - 2011-03-15 12:39 UTC +1133 bp
  - 2011-03-15 12:34 UTC -1119 bp (reversed next bar)
  - 2011-03-15 12:41 UTC -1115 bp
  - 2011-03-15 12:54 UTC -770 bp
  - 2011-03-15 02:48 UTC -670 bp
  - 2011-03-15 02:31 UTC -475 bp
  - 2011-03-15 02:33 UTC +439 bp
  - 2010-12-06 21:15 UTC -435 bp
  - 2011-03-15 02:37 UTC -433 bp

## Cross-source agreement (daily log returns, all pre-hold-out dates; outcome-free)

- vs daily_assets_1970_2026.GLSTOCK (global equity index (loose; Asia close precedes US)), HistData sampled at Asia/Tokyo 15:00 bar close, 2010-11-15..2024-12-31: n=3536, corr lag−1 0.033, lag0 0.228, lag+1 0.427; sd ratio other/HistData 0.83

## Provenance vs inherited pins (FutureSharks/financial-data copy of the same HistData CSVs)

- 9 of 9 yearly CSVs byte-identical to the inherited pins: 2010 =, 2011 =, 2012 =, 2013 =, 2014 =, 2015 =, 2016 =, 2017 =, 2018 =

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).
- GLSTOCK is a loose, US-timed check: the Tokyo close precedes the US close (lag +1 0.43 > lag 0).

