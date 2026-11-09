# QA — histdata_cfd_1m_GRXEUR

Data QA Auditor, Department C, 2026-11-06 02:18 UTC. Outcome-free: no strategy, signal or P&L is computed.

- path `DATA_ROOT/derived/histdata_cfd_1m/GRXEUR`; rows 2,552,224; 2010-11-15 .. 2024-12-31 (UTC); sha256 `33dc8b301d04725a…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/grxeur/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HistData personal use; fetched 2026-11-06; 15 raw zips pinned in fetch_log; clock=histdata_rule (agree): US anchor: winter peak 08:30 summer peak 08:30 clock; shift 0 min -> ny_dst | Europe/Berlin 09:00 open: winter 03:00 summer 03:00 clock; shift 0 min (ny_dst predicts +0; est_fixed -60) -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 16 agree; 1 disagree (years 2015); 5 undecided | verdict histdata_rule (agree); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 176 duplicate local stamps dropped; gaps: 49 gaps > 1 weekday-trading-day (longest: 2020-06-12..2023-12-03 905.1d; 2017-02-17..2017-02-27 5.4d; 2018-12-21..2018-12-27 3.4d); months without bars: 2020-07;2020-08;2020-09;2020-10;2020-11;2020-12;2021-01;2021-02;2021-03;2021-04;2021-05;2021-06;2021-07;2021-08;2021-09;2021-10;2021-11;2021-12;2022-01;2022-02;2022-03;2022-04;2022-05;2022-06;2022-07;2022-08;2022-09;2022-10;2022-11;2022-12;2023-01;2023-02;2023-03;2023-04;2023-05;2023-06;2023-07;2023-08;2023-09;2023-10;2023-11; EXCLUDED 637707 bars 2020-06-15 06:00..2023-12-01 20:59 UTC: GRXEUR file carries Euro Stoxx 50 levels (2;908-4;490) instead of DAX (12;000 -> 16;429 either side)

## Verdict: PASS with caveats

- 41 months without bars
- 1 bar-to-bar level breaks > 25% (review: crash/roll or mislabelled segment)

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 08:30, summer peak 08:30 NY, shift 0 min -> OK.
- After conversion, home-market anchor Europe/Berlin 09:00 (±25 min): winter peak 09:00, summer peak 09:00 local, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 19 CPI/NFP releases; spike at offset 0 (correct) 13, at −60 min (one hour early) 2, undecided 4.
  - offsets (min): 2011-03-17:-12 2011-11-04:-29 2012-03-16:1 2012-11-02:0 2013-03-15:90 2013-10-30:69 2014-03-18:-53 2015-03-24:-82 2016-03-16:-46 2016-11-04:79 2017-03-15:72 2017-11-03:0 2018-03-13:13 2018-11-02:-29 2019-03-12:-67 2019-11-01:0 2020-03-11:69 2024-03-12:0 2024-11-01:10
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 0 same, 0 one hour off, 3 other: 2019 16:14→16:59 2020 15:59→16:14 2024 16:14→17:00
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2010-2018 aligned 16:14 (5/29); 2010-2018 mismatch 15:58 (1/3); 2019+ aligned 16:14 (361/489); 2019+ mismatch 17:00 (19/43)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (XETR, exchange_calendars, breaks excluded)

- sessions in span 3,586; with ≥1 bar 2,690; with no bar 896; median coverage of sessions with bars 100.0%; sessions ≥95% covered 99.4%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2010 | 33 | 0 | 100.0% | 100.0% | 1 | 0 | 836 |
| 2011 | 257 | 0 | 100.0% | 99.2% | 9 | 2 | 840 |
| 2012 | 254 | 0 | 100.0% | 99.6% | 18 | 0 | 840 |
| 2013 | 253 | 0 | 100.0% | 98.0% | 15 | 3 | 839 |
| 2014 | 252 | 1 | 100.0% | 100.0% | 7 | 1 | 840 |
| 2015 | 253 | 0 | 100.0% | 99.6% | 7 | 1 | 840 |
| 2016 | 255 | 0 | 100.0% | 99.6% | 5 | 1 | 840 |
| 2017 | 252 | 5 | 100.0% | 100.0% | 6 | 5 | 839 |
| 2018 | 251 | 0 | 100.0% | 99.6% | 3 | 0 | 840 |
| 2019 | 251 | 0 | 100.0% | 99.2% | 3 | 1 | 1270 |
| 2020 | 254 | 141 | 100.0% | 99.1% | 143 | 142 | 1313 |
| 2021 | 255 | 255 | 0.0% | 0.0% | 255 | 255 | 0 |
| 2022 | 257 | 257 | 0.0% | 0.0% | 257 | 257 | 0 |
| 2023 | 255 | 237 | 100.0% | 100.0% | 237 | 237 | 1277 |
| 2024 | 254 | 0 | 100.0% | 99.2% | 3 | 2 | 1286 |

- lowest-coverage sessions (with bars): 2020-04-14 66.5% (longest hole 148 min); 2011-10-11 73.5% (longest hole 135 min); 2019-05-27 76.5% (longest hole 120 min); 2012-02-17 76.9% (longest hole 20 min); 2016-02-22 79.2% (longest hole 106 min)
- sessions with no bar (first 15 of 896): 2014-06-02, 2017-02-20, 2017-02-21, 2017-02-22, 2017-02-23, 2017-02-24, 2020-06-15, 2020-06-16, 2020-06-17, 2020-06-18, 2020-06-19, 2020-06-22, 2020-06-23, 2020-06-24, 2020-06-25
- delivered hours (2024, share of NY weekdays with ≥1 bar in each NY hour, %): 00:99 01:99 02:99 03:99 04:99 05:99 06:99 07:99 08:99 09:99 10:99 11:99 12:99 13:99 14:98 15:98 16:89 17:5 18:73 19:79 20:79 21:79 22:79 23:79
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 0

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 49; months without any bar: 2020-07, 2020-08, 2020-09, 2020-10, 2020-11, 2020-12, 2021-01, 2021-02, 2021-03, 2021-04, 2021-05, 2021-06, 2021-07, 2021-08, 2021-09, 2021-10, 2021-11, 2021-12, 2022-01, 2022-02, 2022-03, 2022-04, 2022-05, 2022-06, 2022-07, 2022-08, 2022-09, 2022-10, 2022-11, 2022-12, 2023-01, 2023-02, 2023-03, 2023-04, 2023-05, 2023-06, 2023-07, 2023-08, 2023-09, 2023-10, 2023-11
  - 2020-06-12 20:14 → 2023-12-03 23:03 UTC: 905.1 trading days
  - 2017-02-17 20:59 → 2017-02-27 07:01 UTC: 5.4 trading days
  - 2018-12-21 21:14 → 2018-12-27 07:55 UTC: 3.4 trading days
  - 2013-12-23 20:59 → 2013-12-27 07:01 UTC: 3.4 trading days
  - 2012-12-21 21:00 → 2012-12-27 07:00 UTC: 3.4 trading days
  - 2014-12-24 07:01 → 2014-12-29 07:00 UTC: 3.0 trading days
  - 2012-12-28 12:59 → 2013-01-02 07:00 UTC: 2.8 trading days
  - 2014-12-30 20:58 → 2015-01-02 07:00 UTC: 2.4 trading days
  - 2013-12-30 20:58 → 2014-01-02 07:00 UTC: 2.4 trading days
  - 2015-12-30 20:58 → 2016-01-04 07:00 UTC: 2.4 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 0.1%; open == previous close: 12.9% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 0 in 0 sessions
- sessions whose last cash-session close equals the previous session's: 5

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 446; of which spike-reversals (≥80% retraced next bar): 17
- bar-to-bar level breaks > 25%: 1: 2020-06-12 20:14 → 2023-12-03 23:03 UTC (+31%)
- widest single bar high–low: 324 bp
  - 2020-03-16 00:17 UTC -353 bp
  - 2020-03-23 00:15 UTC -304 bp
  - 2020-03-23 00:18 UTC +239 bp
  - 2011-08-05 12:31 UTC +205 bp
  - 2011-09-01 14:01 UTC +189 bp
  - 2015-01-15 09:50 UTC -157 bp
  - 2011-11-30 13:00 UTC +143 bp
  - 2020-03-16 08:29 UTC -132 bp
  - 2011-08-25 14:02 UTC -130 bp
  - 2020-04-12 22:16 UTC -124 bp

## Cross-source agreement (daily log returns, all pre-hold-out dates; outcome-free)

- vs daily_assets_1970_2026.GLSTOCK (global equity index (loose; EUR vs USD)), HistData sampled at America/New_York 16:00 bar close, 2010-11-15..2024-12-31: n=2629, corr lag−1 -0.071, lag0 0.897, lag+1 -0.077; sd ratio other/HistData 0.88

## Provenance vs inherited pins (FutureSharks/financial-data copy of the same HistData CSVs)

- 9 of 9 yearly CSVs byte-identical to the inherited pins: 2010 =, 2011 =, 2012 =, 2013 =, 2014 =, 2015 =, 2016 =, 2017 =, 2018 =

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).
- Bars 2020-06-15 06:00 .. 2023-12-01 20:59 UTC (637,707) are EXCLUDED: the HistData GRXEUR files carry Euro Stoxx 50 levels (2,908-4,490) there, while DAX sits at 12,011 before and 16,429 after. Hence the months without bars and the one level break across the hole. The excluded span is NOT landed as an ETXEUR substitute (provenance is a guess).

