# QA — histdata_cfd_1m_BCOUSD

Data QA Auditor, Department C, 2026-11-06 02:18 UTC. Outcome-free: no strategy, signal or P&L is computed.

- path `DATA_ROOT/derived/histdata_cfd_1m/BCOUSD`; rows 4,253,019; 2010-11-15 .. 2024-12-31 (UTC); sha256 `8818927149637f45…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/bcousd/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HistData personal use; fetched 2026-11-06; 15 raw zips pinned in fetch_log; clock=histdata_rule (single): US anchor: winter peak 09:00 summer peak 09:00 clock; shift 0 min -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 11 agree; 4 disagree (years 2011 2017 2020 2021); 8 undecided | verdict histdata_rule (single); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 434 duplicate local stamps dropped; gaps: 39 gaps > 1 weekday-trading-day (longest: 2013-12-24..2013-12-26 1.7d; 2012-12-24..2012-12-26 1.7d; 2024-12-24..2024-12-26 1.3d); months without bars: none

## Verdict: PASS with caveats

- median cash-session coverage 85.4%
- 50 spike-reversal prints

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 09:00, summer peak 09:00 NY, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 22 CPI/NFP releases; spike at offset 0 (correct) 15, at −60 min (one hour early) 2, undecided 5.
  - offsets (min): 2011-03-17:90 2011-11-04:2 2012-03-16:1 2012-11-02:0 2013-03-15:-42 2013-10-30:-26 2014-03-18:49 2015-03-24:0 2016-03-16:60 2016-11-04:-21 2017-03-15:78 2017-11-03:10 2018-03-13:78 2018-11-02:-30 2019-03-12:-34 2019-11-01:4 2020-03-11:-9 2021-11-05:30 2022-11-04:61 2023-11-03:51 2024-03-12:61 2024-11-01:61
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 13 same, 1 one hour off (2019), 0 other: 2011 17:59→17:59 2012 17:59→17:59 2013 17:59→17:59 2014 17:59→17:59 2015 17:59→17:59 2016 17:59→17:59 2017 17:59→17:59 2018 17:59→17:59 2019 16:59→17:59 2020 16:59→16:59 2021 16:59→16:59 2022 16:59→16:59 2023 16:59→16:59 2024 16:59→16:59
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2010-2018 aligned 17:59 (1014/1815); 2010-2018 mismatch 17:59 (76/126); 2019+ aligned 16:59 (1018/1517); 2019+ mismatch 16:59 (64/117)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (CMES23 = 18:00→17:00 ET futures-style day)

- sessions in span 3,645; with ≥1 bar 3,645; with no bar 0; median coverage of sessions with bars 85.4%; sessions ≥95% covered 0.3%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2010 | 34 | 0 | 82.9% | 0.0% | 150 | 36 | 1142 |
| 2011 | 258 | 0 | 85.3% | 0.0% | 719 | 263 | 1190 |
| 2012 | 258 | 0 | 83.3% | 0.0% | 799 | 266 | 1168 |
| 2013 | 258 | 0 | 79.2% | 0.0% | 989 | 265 | 1114 |
| 2014 | 258 | 0 | 75.3% | 0.0% | 2531 | 267 | 1044 |
| 2015 | 258 | 0 | 81.4% | 0.0% | 1691 | 227 | 1110 |
| 2016 | 258 | 0 | 82.4% | 1.9% | 1355 | 214 | 1123 |
| 2017 | 257 | 0 | 75.8% | 0.0% | 2721 | 223 | 1042 |
| 2018 | 257 | 0 | 85.1% | 2.7% | 862 | 213 | 1167 |
| 2019 | 258 | 0 | 89.6% | 0.0% | 347 | 271 | 1225 |
| 2020 | 259 | 0 | 90.5% | 0.0% | 334 | 264 | 1241 |
| 2021 | 258 | 0 | 90.9% | 0.0% | 291 | 260 | 1250 |
| 2022 | 258 | 0 | 91.3% | 0.0% | 275 | 262 | 1259 |
| 2023 | 257 | 0 | 89.3% | 0.0% | 820 | 799 | 1015 |
| 2024 | 259 | 0 | 89.7% | 0.0% | 329 | 267 | 1232 |

- lowest-coverage sessions (with bars): 2014-06-02 5.4% (longest hole 1264 min); 2020-11-30 17.2% (longest hole 1020 min); 2021-05-31 20.7% (longest hole 780 min); 2019-05-27 36.4% (longest hole 720 min); 2013-12-26 39.5% (longest hole 721 min)
- delivered hours (2024, share of NY weekdays with ≥1 bar in each NY hour, %): 00:99 01:99 02:99 03:99 04:99 05:99 06:99 07:99 08:99 09:99 10:99 11:99 12:98 13:99 14:96 15:95 16:95 17:0 18:0 19:0 20:79 21:79 22:79 23:79
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 4

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 39; months without any bar: none
  - 2013-12-24 18:59 → 2013-12-26 11:01 UTC: 1.7 trading days
  - 2012-12-24 18:59 → 2012-12-26 11:00 UTC: 1.7 trading days
  - 2024-12-24 18:28 → 2024-12-26 01:00 UTC: 1.3 trading days
  - 2018-12-24 18:29 → 2018-12-26 01:00 UTC: 1.3 trading days
  - 2019-12-24 18:46 → 2019-12-26 01:00 UTC: 1.3 trading days
  - 2011-12-23 18:59 → 2011-12-27 01:04 UTC: 1.3 trading days
  - 2016-12-23 18:59 → 2016-12-27 01:02 UTC: 1.3 trading days
  - 2014-12-24 18:59 → 2014-12-26 01:00 UTC: 1.3 trading days
  - 2020-12-24 18:59 → 2020-12-28 01:00 UTC: 1.3 trading days
  - 2018-12-31 19:28 → 2019-01-02 01:00 UTC: 1.2 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 6.4%; open == previous close: 4.1% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 10 in 10 sessions
- sessions whose last cash-session close equals the previous session's: 12

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 1169; of which spike-reversals (≥80% retraced next bar): 50
- bar-to-bar level breaks > 25%: 0
- widest single bar high–low: 1305 bp
  - 2020-04-02 14:36 UTC +1374 bp
  - 2020-04-02 14:38 UTC -1047 bp
  - 2020-04-02 14:35 UTC +502 bp
  - 2020-04-21 09:11 UTC -468 bp
  - 2020-04-02 14:37 UTC -456 bp
  - 2020-04-22 04:34 UTC +456 bp
  - 2020-04-02 14:40 UTC +421 bp
  - 2020-04-21 18:23 UTC +418 bp
  - 2020-04-21 09:59 UTC +395 bp
  - 2020-04-21 17:53 UTC +388 bp

## Cross-source agreement (daily log returns, all pre-hold-out dates; outcome-free)

- vs daily_assets_1970_2026.CMDTY (broad commodity index (loose)), HistData sampled at America/New_York 16:00 bar close, 2010-11-15..2024-12-30: n=3430, corr lag−1 -0.005, lag0 0.868, lag+1 -0.008; sd ratio other/HistData 0.48

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).
- Coverage is measured against the 18:00->17:00 ET template; the Brent CFD keeps ICE-like hours, so ~85% is its own session length, not missing data.

