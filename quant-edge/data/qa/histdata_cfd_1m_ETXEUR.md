# QA — histdata_cfd_1m_ETXEUR

Data QA Auditor, Department C, 2026-11-06 02:17 UTC. Outcome-free: no strategy, signal or P&L is computed.

- path `DATA_ROOT/derived/histdata_cfd_1m/ETXEUR`; rows 1,272,116; 2010-11-15 .. 2018-12-14 (UTC); sha256 `0932086c00e8edd6…`
- source https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/etxeur/YYYY (+ /YYYY/M for current-year months); licence free
- manifest notes: HistData personal use; fetched 2026-11-06; 10 raw zips pinned in fetch_log; clock=histdata_rule (agree): US anchor: winter peak 08:30 summer peak 08:30 clock; shift 0 min -> ny_dst | Europe/Berlin 08:00 open: winter 02:00 summer 02:00 clock; shift 0 min (ny_dst predicts +0; est_fixed -60) -> ny_dst | US/EU DST-mismatch weeks; 08:30 ET CPI/NFP spike vs rule (NY DST <2019; EU DST from it): 7 agree; 1 disagree (years 2015); 4 undecided | verdict histdata_rule (agree); bid quotes; volume=0; weekend rows kept; 0 bars dropped at DST fall-back/spring-forward; 0 duplicate local stamps dropped; gaps: 29 gaps > 1 weekday-trading-day (longest: 2013-12-23..2013-12-27 3.4d; 2012-12-21..2012-12-27 3.4d; 2014-12-24..2014-12-29 3.0d); months without bars: none; EXCLUDED 22163 bars 2018-12-17 07:00..2019-12-31 23:59 UTC: ETXEUR file jumps from 3;072 to 8;880-9;222 (not Euro Stoxx 50; IBEX-like levels) until the data end 2019-02-01; periods listed but not downloaded: 2020;2021;2022;2023;2024;2025;2026-01;2026-02;2026-03;2026-04;2026-05;2026-06;2026-07;2026-08;2026-09;2026-10

## Verdict: PASS with caveats

- median cash-session coverage 83.7%

## Clock (outcome-free: minute of day with the largest mean |1m return|, Jan–Feb vs Jun–Jul)

- After conversion, US anchor (08:15–09:45 New York): winter peak 08:30, summer peak 08:30 NY, shift 0 min -> OK.
- After conversion, home-market anchor Europe/Berlin 08:00 (±25 min): winter peak 08:00, summer peak 08:00 local, shift 0 min -> OK.
- After conversion, US/EU DST-mismatch weeks (2nd Sun Mar→last Sun Mar, last Sun Oct→1st Sun Nov): 12 CPI/NFP releases; spike at offset 0 (correct) 7, at −60 min (one hour early) 1, undecided 4.
  - offsets (min): 2011-03-17:31 2011-11-04:-31 2012-03-16:85 2012-11-02:0 2013-03-15:88 2014-03-18:-53 2015-03-24:-82 2016-03-16:30 2016-11-04:5 2017-03-15:-83 2018-03-13:13 2018-11-02:-18
- Daily halt by year (modal NY minute, aligned → mismatch weeks; same = within 2 min): 0 same, 0 one hour off, 5 other: 2012 13:54→16:19 2013 13:44→15:58 2014 14:02→16:00 2016 15:10→16:35 2017 14:17→15:08
- Daily halt (modal NY minute of the last bar before an intraday gap of 20–600 min, Mon–Thu), aligned vs mismatch weeks: 2010-2018 aligned 15:59 (7/465); 2010-2018 mismatch 16:14 (3/38)
- Raw-clock diagnosis used for the conversion: see manifest notes above (`histdata_rule` = NY DST dates before 2019, EU DST dates from 2019, measured on SPXUSD/EURUSD/USDJPY; Jan–Feb vs Jun–Jul cannot separate the two rules).

## Bar counts vs the cash session (XETR, exchange_calendars, breaks excluded)

- sessions in span 2,053; with ≥1 bar 2,052; with no bar 1; median coverage of sessions with bars 83.7%; sessions ≥95% covered 19.4%

| year | sessions | no bar | median coverage | ≥95% | missing runs ≥5 min | ≥30 min | median bars per NY weekday (24h) |
|---|---|---|---|---|---|---|---|
| 2010 | 33 | 0 | 81.2% | 12.1% | 132 | 0 | 650 |
| 2011 | 257 | 0 | 91.2% | 38.5% | 258 | 1 | 724 |
| 2012 | 254 | 0 | 84.7% | 9.1% | 391 | 1 | 615 |
| 2013 | 253 | 0 | 76.1% | 2.8% | 1046 | 4 | 541 |
| 2014 | 252 | 1 | 80.4% | 8.8% | 807 | 2 | 595 |
| 2015 | 253 | 0 | 96.3% | 59.7% | 60 | 1 | 754 |
| 2016 | 255 | 0 | 89.8% | 28.6% | 415 | 8 | 662 |
| 2017 | 252 | 0 | 68.5% | 0.0% | 1639 | 4 | 493 |
| 2018 | 244 | 0 | 80.2% | 8.2% | 572 | 0 | 605 |

- lowest-coverage sessions (with bars): 2016-12-28 26.5% (longest hole 60 min); 2014-07-04 28.8% (longest hole 34 min); 2017-10-12 29.0% (longest hole 27 min); 2017-10-17 29.8% (longest hole 41 min); 2011-05-30 30.4% (longest hole 26 min)
- sessions with no bar (first 15 of 1): 2014-06-02
- delivered hours (2018, share of NY weekdays with ≥1 bar in each NY hour, %): 00:0 01:0 02:93 03:100 04:100 05:100 06:100 07:100 08:100 09:100 10:100 11:100 12:100 13:100 14:100 15:100 16:12 17:0 18:0 19:0 20:0 21:0 22:0 23:0
- bars inside the FX/CFD weekend (Fri 17:00–Sun 17:00 NY), kept as delivered: 0

## Gaps (weekday market time, weekend removed)

- gaps > 1 trading day: 29; months without any bar: none
  - 2013-12-23 20:59 → 2013-12-27 07:01 UTC: 3.4 trading days
  - 2012-12-21 20:59 → 2012-12-27 07:00 UTC: 3.4 trading days
  - 2014-12-24 07:01 → 2014-12-29 07:00 UTC: 3.0 trading days
  - 2012-12-28 16:28 → 2013-01-02 07:00 UTC: 2.6 trading days
  - 2011-04-21 19:58 → 2011-04-26 06:00 UTC: 2.4 trading days
  - 2017-04-13 19:59 → 2017-04-18 06:01 UTC: 2.4 trading days
  - 2017-12-22 20:59 → 2017-12-27 07:01 UTC: 2.4 trading days
  - 2014-12-30 20:58 → 2015-01-02 07:00 UTC: 2.4 trading days
  - 2015-04-02 19:59 → 2015-04-07 06:00 UTC: 2.4 trading days
  - 2014-04-17 19:59 → 2014-04-22 06:00 UTC: 2.4 trading days

## Stale prints (inside the cash session)

- flat bars (O=H=L=C): 16.1%; open == previous close: 0.6% (HistData bars are built from a continuous quote stream, so a high share is expected and is not an error by itself)
- runs of ≥15 consecutive unchanged closes: 0 in 0 sessions
- sessions whose last cash-session close equals the previous session's: 24

## Outliers and OHLC sanity

- OHLC: NaN rows 0, non-positive 0, high < max(O,C) 0, low > min(O,C) 0, duplicate ts 0, non-zero volume 0
- 1m moves above max(20 × the year's median |move|, 50 bp): 50; of which spike-reversals (≥80% retraced next bar): 3
- bar-to-bar level breaks > 25%: 0
- widest single bar high–low: 326 bp
  - 2015-06-18 16:23 UTC +195 bp
  - 2011-08-05 12:31 UTC +194 bp
  - 2015-01-15 09:51 UTC -172 bp (reversed next bar)
  - 2015-01-15 09:52 UTC +152 bp
  - 2011-09-01 14:00 UTC +148 bp
  - 2011-11-30 13:00 UTC +141 bp
  - 2011-09-02 12:32 UTC -138 bp
  - 2015-01-15 09:50 UTC -134 bp
  - 2014-10-13 06:04 UTC -119 bp
  - 2011-10-03 14:02 UTC +113 bp

## Cross-source agreement (daily log returns, all pre-hold-out dates; outcome-free)

- vs daily_assets_1970_2026.GLSTOCK (global equity index (loose; EUR vs USD)), HistData sampled at America/New_York 16:00 bar close, 2010-11-15..2018-12-14: n=2004, corr lag−1 -0.045, lag0 0.873, lag+1 -0.066; sd ratio other/HistData 0.75

## Provenance vs inherited pins (FutureSharks/financial-data copy of the same HistData CSVs)

- 9 of 9 yearly CSVs byte-identical to the inherited pins: 2010 =, 2011 =, 2012 =, 2013 =, 2014 =, 2015 =, 2016 =, 2017 =, 2018 =

## Auditor notes

- 2017-02-17..02-27 is a HistData outage common to every CFD symbol; the 2023-02..06 sparse months seen on SPXUSD also appear on the FX files (WORK-LOG 3.1).
- HistData offers no ETXEUR file from 2020 (the year pages serve an empty download token) and the 2019 file stops 2019-02-01; from 2018-12-17 07:00 UTC the file jumps to 8,880-9,222 (not Euro Stoxx 50; IBEX-like), so those 22,163 bars are EXCLUDED. Usable span 2010-11-15 .. 2018-12-14; no hold-out part.

