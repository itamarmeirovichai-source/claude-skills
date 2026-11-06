# QA — histdata_cfd_1m_NSXUSD

Data QA Auditor, Department C, 2026-11-06 02:18 UTC. Outcome-free: no strategy, signal or P&L is computed.

- path `DATA_ROOT/derived/histdata_cfd_1m/NSXUSD`; rows 4,694,242; 2010-11-14 .. 2024-12-31 (UTC); sha256 `0c02f4c45f78e52c…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/nsxusd/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HistData personal use; fetched 2026-11-06; 15 raw zips pinned in fetch_log; clock=histdata_rule (single): US anchor: winter peak 09:30 summer peak 09:30 clock; shift 0 min -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 16 agree; 0 disagree; 7 undecided | verdict histdata_rule (single); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 856 duplicate local stamps dropped; gaps: 38 gaps > 1 weekday-trading-day (longest: 2017-02-17..2017-02-26 5.0d; 2013-12-24..2013-12-26 1.7d; 2012-12-24..2012-12-26 1.7d); months without bars: none

## Verdict: PASS with caveats

- 25 spike-reversal prints

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 09:30, summer peak 09:30 NY, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 22 CPI/NFP releases; spike at offset 0 (correct) 18, at −60 min (one hour early) 0, undecided 4.
  - offsets (min): 2011-03-17:70 2011-11-04:-31 2012-03-16:60 2012-11-02:1 2013-03-15:86 2013-10-30:74 2014-03-18:-53 2015-03-24:65 2016-03-16:60 2016-11-04:63 2017-03-15:60 2017-11-03:0 2018-03-13:0 2018-11-02:60 2019-03-12:67 2019-11-01:0 2020-03-11:72 2021-11-05:2 2022-11-04:0 2023-11-03:0 2024-03-12:2 2024-11-01:2
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 14 same, 0 one hour off, 0 other: 2011 17:30→17:30 2012 17:29→17:29 2013 17:15→17:15 2014 17:15→17:15 2015 17:15→17:15 2016 17:00→17:00 2017 17:00→16:59 2018 17:00→17:00 2019 16:14→16:14 2020 16:14→16:14 2021 16:14→16:14 2022 16:14→16:14 2023 16:14→16:14 2024 16:14→16:14
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2010-2018 aligned 17:00 (416/1523); 2010-2018 mismatch 17:15 (32/100); 2019+ aligned 16:14 (1065/1529); 2019+ mismatch 16:14 (78/130)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (XNYS, exchange_calendars, breaks excluded)

- sessions in span 3,555; with ≥1 bar 3,550; with no bar 5; median coverage of sessions with bars 100.0%; sessions ≥95% covered 96.2%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2010 | 33 | 0 | 98.7% | 75.8% | 3 | 1 | 1237 |
| 2011 | 252 | 0 | 100.0% | 99.2% | 2 | 0 | 1286 |
| 2012 | 250 | 0 | 100.0% | 99.2% | 3 | 0 | 1266 |
| 2013 | 252 | 0 | 100.0% | 99.2% | 6 | 0 | 1208 |
| 2014 | 252 | 0 | 100.0% | 99.6% | 6 | 1 | 1234 |
| 2015 | 252 | 0 | 100.0% | 99.6% | 7 | 1 | 1290 |
| 2016 | 252 | 0 | 100.0% | 98.8% | 3 | 0 | 1325 |
| 2017 | 251 | 4 | 100.0% | 99.6% | 5 | 4 | 1312 |
| 2018 | 251 | 0 | 100.0% | 100.0% | 1 | 0 | 1362 |
| 2019 | 252 | 0 | 100.0% | 100.0% | 0 | 0 | 1334 |
| 2020 | 253 | 1 | 100.0% | 100.0% | 6 | 1 | 1335 |
| 2021 | 252 | 0 | 100.0% | 100.0% | 0 | 0 | 1335 |
| 2022 | 251 | 0 | 100.0% | 100.0% | 1 | 0 | 1335 |
| 2023 | 250 | 0 | 100.0% | 55.6% | 316 | 314 | 975 |
| 2024 | 252 | 0 | 100.0% | 98.4% | 8 | 4 | 1328 |

- lowest-coverage sessions (with bars): 2014-06-02 14.9% (longest hole 332 min); 2023-02-28 30.8% (longest hole 150 min); 2023-03-02 30.8% (longest hole 120 min); 2023-03-06 30.8% (longest hole 150 min); 2023-03-15 30.8% (longest hole 270 min)
- sessions with no bar (first 15 of 5): 2017-02-21, 2017-02-22, 2017-02-23, 2017-02-24, 2020-11-30
- delivered hours (2024, share of NY weekdays with ≥1 bar in each NY hour, %): 00:99 01:99 02:99 03:99 04:99 05:99 06:99 07:99 08:99 09:99 10:99 11:99 12:98 13:95 14:95 15:94 16:94 17:0 18:77 19:79 20:79 21:79 22:79 23:79
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 0

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 38; months without any bar: none
  - 2017-02-17 21:59 → 2017-02-26 23:01 UTC: 5.0 trading days
  - 2013-12-24 18:15 → 2013-12-26 11:01 UTC: 1.7 trading days
  - 2012-12-24 18:15 → 2012-12-26 11:00 UTC: 1.7 trading days
  - 2011-12-30 21:14 → 2012-01-03 11:00 UTC: 1.6 trading days
  - 2011-12-23 21:15 → 2011-12-27 11:00 UTC: 1.6 trading days
  - 2012-12-31 21:58 → 2013-01-02 11:00 UTC: 1.5 trading days
  - 2024-12-24 18:13 → 2024-12-25 23:01 UTC: 1.2 trading days
  - 2019-12-24 18:14 → 2019-12-25 23:01 UTC: 1.2 trading days
  - 2023-07-03 17:13 → 2023-07-04 22:00 UTC: 1.2 trading days
  - 2020-12-24 18:14 → 2020-12-27 23:00 UTC: 1.2 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 0.2%; open == previous close: 9.6% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 0 in 0 sessions
- sessions whose last cash-session close equals the previous session's: 4

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 555; of which spike-reversals (≥80% retraced next bar): 25
- bar-to-bar level breaks > 25%: 0
- widest single bar high–low: 358 bp
  - 2022-10-13 12:30 UTC -350 bp
  - 2022-11-10 13:31 UTC +338 bp
  - 2022-07-13 12:30 UTC -264 bp
  - 2020-03-03 15:00 UTC +219 bp
  - 2022-09-13 12:30 UTC -218 bp
  - 2022-12-02 13:30 UTC -195 bp
  - 2022-12-13 13:30 UTC +180 bp
  - 2020-03-18 19:59 UTC +166 bp
  - 2022-12-09 13:30 UTC -156 bp
  - 2022-11-02 18:36 UTC -155 bp

## Cross-source agreement (daily log returns, all pre-hold-out dates; outcome-free)

- vs daily_assets_1970_2026.USLCAP (US large-cap index level (Nasdaq-100 vs broad US)), HistData sampled at America/New_York 16:00 bar close, 2010-11-15..2024-12-31: n=3467, corr lag−1 -0.102, lag0 0.928, lag+1 -0.118; sd ratio other/HistData 0.83
- vs spx_oc_1990_2026.close (S&P 500 cash close), HistData sampled at America/New_York 16:00 bar close, 2010-11-15..2024-12-31: n=3467, corr lag−1 -0.102, lag0 0.928, lag+1 -0.118; sd ratio other/HistData 0.83
  - level ratio HistData/^GSPC median 2.4086 (p1–p99 1.7561–3.5762); |daily return difference| median 27.5 bp, p99 162.4 bp

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).

