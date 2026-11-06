# QA — histdata_cfd_1m_XAUUSD

Data QA Auditor, Department C, 2026-11-06 02:19 UTC. Outcome-free: no strategy, signal or P&L is computed.

- path `DATA_ROOT/derived/histdata_cfd_1m/XAUUSD`; rows 5,250,461; 2010-01-03 .. 2024-12-31 (UTC); sha256 `ca5cb9014a824688…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/xauusd/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HistData personal use; fetched 2026-11-06; 15 raw zips pinned in fetch_log; clock=histdata_rule (single): US anchor: winter peak 08:30 summer peak 08:30 clock; shift 0 min -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 23 agree; 1 disagree (years 2020); 0 undecided | verdict histdata_rule (single); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 1624 duplicate local stamps dropped; gaps: 36 gaps > 1 weekday-trading-day (longest: 2013-12-24..2013-12-26 1.7d; 2012-12-24..2012-12-26 1.7d; 2014-12-24..2014-12-25 1.2d); months without bars: none

## Verdict: PASS

- no blocking issue found

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 08:30, summer peak 08:30 NY, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 25 CPI/NFP releases; spike at offset 0 (correct) 23, at −60 min (one hour early) 0, undecided 2.
  - offsets (min): 2010-03-18:-83 2010-11-05:0 2011-03-17:-11 2011-11-04:-15 2012-03-16:69 2012-11-02:0 2013-03-15:85 2013-10-30:-15 2014-03-18:-53 2015-03-24:0 2016-03-16:0 2016-11-04:2 2017-03-15:79 2017-11-03:0 2018-03-13:1 2018-11-02:0 2019-03-12:0 2019-11-01:0 2020-03-11:64 2021-11-05:6 2022-11-04:5 2023-03-14:78 2023-11-03:0 2024-03-12:2 2024-11-01:0
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 13 same, 0 one hour off, 2 other: 2010 17:15→17:20 2011 17:15→17:15 2012 17:15→17:00 2013 17:14→17:14 2014 17:14→17:14 2015 16:59→16:59 2016 16:59→16:59 2017 16:59→16:59 2018 17:00→17:00 2019 16:59→16:58 2020 16:59→16:59 2021 16:59→16:59 2022 16:59→16:59 2023 16:59→16:59 2024 16:59→16:59
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2010-2018 aligned 16:59 (544/1782); 2010-2018 mismatch 16:59 (34/122); 2019+ aligned 16:59 (1025/1558); 2019+ mismatch 16:59 (70/122)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (CMES23 = 18:00→17:00 ET futures-style day)

- sessions in span 3,869; with ≥1 bar 3,869; with no bar 0; median coverage of sessions with bars 99.9%; sessions ≥95% covered 94.8%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2010 | 258 | 0 | 97.0% | 74.4% | 127 | 6 | 1344 |
| 2011 | 258 | 0 | 98.7% | 97.7% | 33 | 0 | 1369 |
| 2012 | 258 | 0 | 99.8% | 99.6% | 4 | 1 | 1381 |
| 2013 | 258 | 0 | 99.7% | 99.6% | 13 | 3 | 1389 |
| 2014 | 258 | 0 | 99.5% | 99.2% | 10 | 2 | 1373 |
| 2015 | 258 | 0 | 99.5% | 99.2% | 15 | 3 | 1371 |
| 2016 | 258 | 0 | 99.8% | 100.0% | 20 | 1 | 1377 |
| 2017 | 257 | 0 | 99.9% | 100.0% | 10 | 2 | 1378 |
| 2018 | 257 | 0 | 99.9% | 100.0% | 2 | 0 | 1378 |
| 2019 | 258 | 0 | 99.9% | 99.6% | 7 | 3 | 1376 |
| 2020 | 259 | 0 | 100.0% | 99.6% | 5 | 4 | 1380 |
| 2021 | 258 | 0 | 100.0% | 99.2% | 4 | 3 | 1380 |
| 2022 | 258 | 0 | 100.0% | 99.6% | 3 | 2 | 1380 |
| 2023 | 257 | 0 | 99.6% | 55.3% | 655 | 651 | 1020 |
| 2024 | 259 | 0 | 100.0% | 99.2% | 6 | 4 | 1380 |

- lowest-coverage sessions (with bars): 2014-06-02 8.3% (longest hole 1262 min); 2020-11-30 26.1% (longest hole 1020 min); 2021-05-31 31.6% (longest hole 780 min); 2019-05-27 42.1% (longest hole 420 min); 2013-12-26 46.7% (longest hole 729 min)
- delivered hours (2024, share of NY weekdays with ≥1 bar in each NY hour, %): 00:99 01:99 02:99 03:99 04:99 05:99 06:99 07:99 08:99 09:99 10:99 11:99 12:99 13:99 14:98 15:95 16:95 17:0 18:79 19:79 20:79 21:79 22:79 23:79
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 10

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 36; months without any bar: none
  - 2013-12-24 18:45 → 2013-12-26 11:09 UTC: 1.7 trading days
  - 2012-12-24 18:45 → 2012-12-26 11:00 UTC: 1.7 trading days
  - 2014-12-24 18:44 → 2014-12-25 23:01 UTC: 1.2 trading days
  - 2024-12-24 18:43 → 2024-12-25 23:00 UTC: 1.2 trading days
  - 2019-12-24 18:44 → 2019-12-25 23:00 UTC: 1.2 trading days
  - 2020-12-24 18:44 → 2020-12-27 23:00 UTC: 1.2 trading days
  - 2018-12-24 18:44 → 2018-12-25 23:00 UTC: 1.2 trading days
  - 2015-12-24 18:45 → 2015-12-27 23:01 UTC: 1.2 trading days
  - 2013-12-31 20:59 → 2014-01-01 23:04 UTC: 1.1 trading days
  - 2023-04-06 20:58 → 2023-04-09 23:00 UTC: 1.1 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 0.5%; open == previous close: 12.4% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 4 in 4 sessions
- sessions whose last cash-session close equals the previous session's: 7

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 292; of which spike-reversals (≥80% retraced next bar): 10
- bar-to-bar level breaks > 25%: 0
- widest single bar high–low: 409 bp
  - 2021-08-08 22:57 UTC -269 bp
  - 2015-07-20 01:29 UTC -243 bp
  - 2013-09-06 12:30 UTC +201 bp
  - 2013-12-18 19:01 UTC +162 bp
  - 2011-09-07 04:22 UTC -150 bp
  - 2015-11-06 13:30 UTC -141 bp
  - 2013-12-18 19:00 UTC -137 bp (reversed next bar)
  - 2013-09-18 18:00 UTC +136 bp
  - 2016-07-08 12:30 UTC -133 bp
  - 2016-09-02 12:30 UTC +132 bp

## Cross-source agreement (daily log returns, all pre-hold-out dates; outcome-free)

- vs daily_assets_1970_2026.GOLDPM (LBMA gold PM price), HistData sampled at Europe/London 15:00 bar close, 2010-01-04..2024-12-31: n=3709, corr lag−1 -0.005, lag0 0.629, lag+1 0.376; sd ratio other/HistData 1.03

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).
- GOLDPM in daily_assets_1970_2026 correlates 0.63 at lag 0 and 0.38 at lag +1, stable in every year 2010-2024: the second source mixes same-day and next-day dating. XAUUSD's clock checks pass, so the shortfall is attributed to GOLDPM.

