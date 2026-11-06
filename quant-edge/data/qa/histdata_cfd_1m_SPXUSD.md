# QA — histdata_cfd_1m_SPXUSD

Data QA Auditor, Department C, 2026-11-06 02:18 UTC. Outcome-free: no strategy, signal or P&L is computed.

- path `DATA_ROOT/derived/histdata_cfd_1m/SPXUSD`; rows 4,061,024; 2010-11-14 .. 2024-12-31 (UTC); sha256 `6df2c011d57fc4ad…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/spxusd/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HistData personal use; fetched 2026-11-06; 15 raw zips pinned in fetch_log; clock=histdata_rule (single): US anchor: winter peak 08:30 summer peak 08:30 clock; shift 0 min -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 15 agree; 1 disagree (years 2012); 6 undecided | verdict histdata_rule (single); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 425 duplicate local stamps dropped; gaps: 37 gaps > 1 weekday-trading-day (longest: 2017-02-17..2017-02-26 5.0d; 2013-12-24..2013-12-26 1.7d; 2012-12-24..2012-12-26 1.7d); months without bars: none

## Verdict: PASS with caveats

- 22 spike-reversal prints

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 08:30, summer peak 08:30 NY, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 22 CPI/NFP releases; spike at offset 0 (correct) 18, at −60 min (one hour early) 1, undecided 3.
  - offsets (min): 2011-03-17:90 2011-11-04:2 2012-03-16:-43 2012-11-02:0 2013-03-15:86 2013-10-30:69 2014-03-18:-53 2015-03-24:69 2016-03-16:60 2016-11-04:85 2017-03-15:72 2017-11-03:65 2018-03-13:0 2018-11-02:-19 2019-03-12:67 2019-11-01:0 2020-03-11:72 2021-11-05:9 2022-11-04:5 2023-11-03:0 2024-03-12:0 2024-11-01:1
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 14 same, 0 one hour off, 0 other: 2011 17:29→17:28 2012 17:29→17:29 2013 17:14→17:15 2014 17:14→17:15 2015 17:14→17:15 2016 17:00→17:00 2017 16:59→16:59 2018 16:59→16:59 2019 16:14→16:14 2020 16:14→16:14 2021 16:14→16:14 2022 16:14→16:14 2023 16:14→16:14 2024 16:14→16:14
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2010-2018 aligned 16:59 (290/2629); 2010-2018 mismatch 17:15 (23/143); 2019+ aligned 16:14 (1071/1540); 2019+ mismatch 16:14 (80/129)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (XNYS, exchange_calendars, breaks excluded)

- sessions in span 3,555; with ≥1 bar 3,550; with no bar 5; median coverage of sessions with bars 99.5%; sessions ≥95% covered 73.5%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2010 | 33 | 0 | 84.9% | 15.2% | 112 | 1 | 875 |
| 2011 | 252 | 0 | 97.9% | 63.9% | 46 | 0 | 1023 |
| 2012 | 250 | 0 | 92.1% | 32.8% | 90 | 0 | 941 |
| 2013 | 252 | 0 | 91.5% | 32.9% | 104 | 0 | 855 |
| 2014 | 252 | 0 | 95.0% | 50.0% | 87 | 1 | 878 |
| 2015 | 252 | 0 | 99.5% | 90.1% | 9 | 1 | 1042 |
| 2016 | 252 | 0 | 99.2% | 82.9% | 23 | 0 | 1040 |
| 2017 | 251 | 4 | 94.4% | 43.7% | 85 | 4 | 837 |
| 2018 | 251 | 0 | 100.0% | 92.0% | 10 | 0 | 1166 |
| 2019 | 252 | 0 | 99.7% | 93.7% | 5 | 0 | 1187 |
| 2020 | 253 | 1 | 100.0% | 99.6% | 5 | 1 | 1314 |
| 2021 | 252 | 0 | 100.0% | 100.0% | 0 | 0 | 1296 |
| 2022 | 251 | 0 | 100.0% | 100.0% | 2 | 0 | 1330 |
| 2023 | 250 | 0 | 100.0% | 56.0% | 333 | 330 | 973 |
| 2024 | 252 | 0 | 100.0% | 98.8% | 5 | 4 | 1294 |

- lowest-coverage sessions (with bars): 2014-06-02 13.1% (longest hole 332 min); 2023-02-24 30.8% (longest hole 150 min); 2010-12-31 36.9% (longest hole 62 min); 2023-03-09 38.2% (longest hole 180 min); 2023-03-06 38.5% (longest hole 120 min)
- sessions with no bar (first 15 of 5): 2017-02-21, 2017-02-22, 2017-02-23, 2017-02-24, 2020-11-30
- delivered hours (2024, share of NY weekdays with ≥1 bar in each NY hour, %): 00:99 01:99 02:99 03:99 04:99 05:99 06:99 07:99 08:99 09:99 10:99 11:99 12:99 13:96 14:95 15:95 16:95 17:0 18:79 19:79 20:79 21:79 22:79 23:79
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 0

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 37; months without any bar: none
  - 2017-02-17 21:59 → 2017-02-26 23:01 UTC: 5.0 trading days
  - 2013-12-24 18:15 → 2013-12-26 11:01 UTC: 1.7 trading days
  - 2012-12-24 18:15 → 2012-12-26 11:00 UTC: 1.7 trading days
  - 2011-12-30 21:13 → 2012-01-03 11:00 UTC: 1.6 trading days
  - 2011-12-23 21:15 → 2011-12-27 11:00 UTC: 1.6 trading days
  - 2012-12-31 21:58 → 2013-01-02 11:00 UTC: 1.5 trading days
  - 2023-07-03 16:59 → 2023-07-04 23:03 UTC: 1.3 trading days
  - 2019-12-24 18:14 → 2019-12-25 23:02 UTC: 1.2 trading days
  - 2024-12-24 18:13 → 2024-12-25 23:00 UTC: 1.2 trading days
  - 2020-12-24 18:14 → 2020-12-27 23:00 UTC: 1.2 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 4.0%; open == previous close: 5.8% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 0 in 0 sessions
- sessions whose last cash-session close equals the previous session's: 24

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 452; of which spike-reversals (≥80% retraced next bar): 22
- bar-to-bar level breaks > 25%: 0
- widest single bar high–low: 259 bp
  - 2022-10-13 12:30 UTC -240 bp
  - 2020-03-03 15:00 UTC +221 bp
  - 2022-11-10 13:30 UTC +210 bp
  - 2022-09-13 12:30 UTC -208 bp
  - 2022-07-13 12:30 UTC -179 bp
  - 2011-08-05 12:31 UTC +149 bp
  - 2022-12-13 13:30 UTC +147 bp
  - 2022-12-02 13:30 UTC -144 bp
  - 2022-12-09 13:30 UTC -143 bp
  - 2020-03-26 19:50 UTC +138 bp

## Cross-source agreement (daily log returns, all pre-hold-out dates; outcome-free)

- vs spx_oc_1990_2026.close (S&P 500 cash close (^GSPC)), HistData sampled at America/New_York 16:00 bar close, 2010-11-15..2024-12-31: n=3452, corr lag−1 -0.114, lag0 0.998, lag+1 -0.111; sd ratio other/HistData 1.00
  - level ratio HistData/^GSPC median 0.9995 (p1–p99 0.9949–1.0012); |daily return difference| median 2.6 bp, p99 21.4 bp
- vs daily_assets_1970_2026.USLCAP (US large-cap index level), HistData sampled at America/New_York 16:00 bar close, 2010-11-15..2024-12-31: n=3452, corr lag−1 -0.114, lag0 0.998, lag+1 -0.111; sd ratio other/HistData 1.00

## Provenance vs inherited pins (FutureSharks/financial-data copy of the same HistData CSVs)

- 9 of 9 yearly CSVs byte-identical to the inherited pins: 2010 =, 2011 =, 2012 =, 2013 =, 2014 =, 2015 =, 2016 =, 2017 =, 2018 =

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).
- This dataset also supersedes the inherited SPXUSD 2010-18 (FutureSharks copy): the yearly CSVs are byte-identical.

