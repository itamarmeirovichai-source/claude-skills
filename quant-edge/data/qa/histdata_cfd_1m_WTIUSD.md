# QA — histdata_cfd_1m_WTIUSD

Data QA Auditor, Department C, 2026-11-06 02:19 UTC. Outcome-free: no strategy, signal or P&L is computed.

- path `DATA_ROOT/derived/histdata_cfd_1m/WTIUSD`; rows 4,203,945; 2010-11-15 .. 2023-12-01 (UTC); sha256 `8586c8b96c183853…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/wtiusd/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HistData personal use; fetched 2026-11-06; 14 raw zips pinned in fetch_log; clock=histdata_rule (single): US anchor: winter peak 09:00 summer peak 09:00 clock; shift 0 min -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 10 agree; 4 disagree (years 2017 2020 2021 2022); 7 undecided | verdict histdata_rule (single); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 312 duplicate local stamps dropped; gaps: 37 gaps > 1 weekday-trading-day (longest: 2017-02-17..2017-02-26 5.0d; 2013-12-24..2013-12-26 1.7d; 2012-12-24..2012-12-26 1.7d); months without bars: none; periods listed but not downloaded: 2024;2025;2026-01;2026-02;2026-03;2026-04;2026-05

## Verdict: PASS with caveats

- 2 bar-to-bar level breaks > 25% (review: crash/roll or mislabelled segment)
- 106 spike-reversal prints

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 09:00, summer peak 09:00 NY, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 21 CPI/NFP releases; spike at offset 0 (correct) 14, at −60 min (one hour early) 1, undecided 6.
  - offsets (min): 2011-03-17:30 2011-11-04:2 2012-03-16:1 2012-11-02:0 2013-03-15:88 2013-10-30:-78 2014-03-18:31 2015-03-24:45 2016-03-16:60 2016-11-04:-21 2017-03-15:65 2017-11-03:-72 2018-03-13:78 2018-11-02:35 2019-03-12:-34 2019-11-01:62 2020-03-11:-9 2021-11-05:30 2022-11-04:61 2023-03-14:5 2023-11-03:51
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 13 same, 0 one hour off, 0 other: 2011 17:59→17:59 2012 17:14→17:14 2013 17:14→17:14 2014 17:14→17:14 2015 17:15→17:15 2016 16:59→16:59 2017 16:59→16:59 2018 17:00→16:59 2019 16:59→16:59 2020 16:59→16:59 2021 16:59→16:59 2022 16:59→16:59 2023 16:59→16:59
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2010-2018 aligned 17:14 (412/1721); 2010-2018 mismatch 17:14 (35/115); 2019+ aligned 16:59 (832/1333); 2019+ mismatch 16:59 (60/103)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (CMES23 = 18:00→17:00 ET futures-style day)

- sessions in span 3,367; with ≥1 bar 3,362; with no bar 5; median coverage of sessions with bars 91.9%; sessions ≥95% covered 36.0%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2010 | 34 | 0 | 87.1% | 0.0% | 58 | 36 | 1221 |
| 2011 | 258 | 0 | 88.7% | 0.0% | 364 | 263 | 1239 |
| 2012 | 258 | 0 | 94.5% | 42.6% | 307 | 18 | 1298 |
| 2013 | 258 | 0 | 90.4% | 8.1% | 630 | 4 | 1237 |
| 2014 | 258 | 0 | 86.1% | 11.2% | 1330 | 1 | 1169 |
| 2015 | 258 | 0 | 92.0% | 25.6% | 683 | 4 | 1245 |
| 2016 | 258 | 0 | 90.3% | 18.2% | 984 | 1 | 1201 |
| 2017 | 257 | 5 | 78.6% | 0.0% | 3482 | 16 | 1048 |
| 2018 | 257 | 0 | 89.6% | 16.3% | 825 | 5 | 1207 |
| 2019 | 258 | 0 | 92.7% | 31.8% | 484 | 46 | 1247 |
| 2020 | 259 | 0 | 97.5% | 73.7% | 85 | 6 | 1325 |
| 2021 | 258 | 0 | 98.4% | 94.2% | 36 | 3 | 1349 |
| 2022 | 258 | 0 | 100.0% | 99.6% | 14 | 2 | 1379 |
| 2023 | 238 | 0 | 96.1% | 52.1% | 663 | 640 | 1016 |

- lowest-coverage sessions (with bars): 2014-06-02 6.6% (longest hole 1264 min); 2020-11-30 25.4% (longest hole 1020 min); 2021-05-31 29.8% (longest hole 780 min); 2013-12-26 40.4% (longest hole 721 min); 2012-12-26 43.2% (longest hole 720 min)
- sessions with no bar (first 15 of 5): 2017-02-20, 2017-02-21, 2017-02-22, 2017-02-23, 2017-02-24
- delivered hours (2023, share of NY weekdays with ≥1 bar in each NY hour, %): 00:100 01:100 02:99 03:100 04:98 05:96 06:74 07:79 08:76 09:74 10:79 11:75 12:75 13:74 14:74 15:75 16:72 17:0 18:60 19:64 20:80 21:80 22:80 23:80
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 4

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 37; months without any bar: none
  - 2017-02-17 21:59 → 2017-02-26 23:00 UTC: 5.0 trading days
  - 2013-12-24 18:45 → 2013-12-26 11:01 UTC: 1.7 trading days
  - 2012-12-24 18:45 → 2012-12-26 11:00 UTC: 1.7 trading days
  - 2011-12-23 18:59 → 2011-12-27 01:07 UTC: 1.3 trading days
  - 2015-12-24 18:44 → 2015-12-27 23:00 UTC: 1.2 trading days
  - 2019-12-24 18:44 → 2019-12-25 23:00 UTC: 1.2 trading days
  - 2020-12-24 18:44 → 2020-12-27 23:00 UTC: 1.2 trading days
  - 2018-12-24 18:44 → 2018-12-25 23:00 UTC: 1.2 trading days
  - 2014-12-24 18:44 → 2014-12-25 23:00 UTC: 1.2 trading days
  - 2019-04-18 18:29 → 2019-04-21 22:00 UTC: 1.1 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 6.6%; open == previous close: 6.1% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 10 in 10 sessions
- sessions whose last cash-session close equals the previous session's: 4

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 2149; of which spike-reversals (≥80% retraced next bar): 106
- bar-to-bar level breaks > 25%: 2: 2020-03-06 21:59 → 2020-03-08 22:02 UTC (-32%); 2020-04-17 20:39 → 2020-04-19 22:00 UTC (+30%)
- widest single bar high–low: 2688 bp
  - 2020-04-21 17:49 UTC -2153 bp
  - 2020-04-21 17:48 UTC -2052 bp
  - 2020-04-21 17:53 UTC +1925 bp
  - 2020-04-21 09:33 UTC -1672 bp
  - 2020-04-21 18:23 UTC +1516 bp
  - 2020-04-21 17:51 UTC +1150 bp
  - 2020-04-21 17:45 UTC -1076 bp
  - 2020-04-21 18:24 UTC -897 bp
  - 2020-04-02 14:37 UTC +878 bp
  - 2020-04-21 18:27 UTC -833 bp

## Cross-source agreement (daily log returns, all pre-hold-out dates; outcome-free)

- vs daily_assets_1970_2026.CMDTY (broad commodity index (loose)), HistData sampled at America/New_York 16:00 bar close, 2010-11-15..2023-12-01: n=3191, corr lag−1 -0.025, lag0 0.784, lag+1 0.004; sd ratio other/HistData 0.41

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).
- HistData offers no WTIUSD file for 2024 and 2025 or for 2026-01..05 (empty tokens); IS ends 2023-12-01 and the hold-out part is 2026-06-28 .. 2026-10-30 only. The two level breaks are real: the 2020-03-09 OPEC+ gap and the 2020-04-19 CFD roll after the negative-price May contract.

