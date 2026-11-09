# Ingest batch 1b — progress (Department C, Ingestion Engineer + Data QA Auditor)

Task: HistData 1m 2010-01..latest month for HKXHKD, ETXEUR, GRXEUR, SPXUSD, NSXUSD, JPXJPY, XAUUSD, BCOUSD (+ UKXGBP, FRXEUR, WTIUSD if carried);
HistData FX 2025–2026 months for EURUSD, GBPUSD, USDJPY, AUDUSD (hold-out: DATA_ROOT/holdout/ only, outcome-free QA).
Rule applied to every symbol (D-004, paths.HOLDOUT_START = 2025-01-01): bars from 2025-01-01 UTC go to `holdout/`, never into the derived IS/OOS dataset.

## Log (UTC)
- 01:26 start. Read histdata.py, common.py, qa/clock.py, qa/pins.py, manifest HistData rows, fetch_log. HistData index page for SPXUSD lists 2010..2025 yearly + 2026/1..2026/10 monthly; month form = datemonth YYYYMM.

## Resume notes
- Raw zips are cached under DATA_ROOT/raw/histdata/<SYM>/ (2010–2024) and DATA_ROOT/holdout/raw/histdata/<SYM>/ (2025+); a re-run never re-downloads.
- 01:28 loader extended (`list_periods`, monthly files, `ingest_symbol`, hold-out split); QA module `src/qe/qa/histdata_qa.py`; anchor diagnostic in `qa/clock.py`.
- 01:31 SPXUSD landed (IS 4,061,024 rows 2010-11-14..2024-12-31; hold-out 623,058 rows 2025-01-01..2026-10-30). Background run started for the other 10 CFDs, then FX hold-out (log: DATA_ROOT/logs/histdata_batch1b.log).
- 01:34 SPXUSD QA: corr 0.998 vs ^GSPC daily, level ratio 0.9995; 2010–2018 yearly CSVs byte-identical to the inherited FutureSharks pins (9/9).
- 01:40 **CLOCK FINDING**: HistData follows NY DST dates through 2018 but the EU DST dates from 2019. Evidence: SPXUSD daily halt sits at 16:14 NY in aligned weeks but 15:14 in every US/EU mismatch window 2019-03..2024-11 (16:59/17:14 in both before 2019); 08:30 ET CPI/NFP spikes at −60 min in every decisive mismatch event 2019–2024 on EURUSD and USDJPY, at 0 before. Winter-vs-summer cannot see it. New clock `histdata_rule` (ny_dst < 2019, eu_dst ≥ 2019) in `to_utc`; all batch-1b datasets will be re-converted from the cached zips with it. **The existing histdata_fx_1m_{EURUSD,GBPUSD,USDJPY,AUDUSD} (2026-11-04) are 1 h early in the 2019–2024 mismatch weeks (~3 weeks/yr; e.g. March FOMC days, Oct-31 month-ends); not re-landed (sha256 pins; Director decision).**
- 01:41 ETXEUR: HistData index lists 2020–2026 but the pages carry no download token (files missing); ETXEUR = 2010-11..2019-12 only. JPXJPY clock agrees on both anchors.
- 01:50 mismatch-week vote refined (release at −60/0/+60; the 09:30 open cannot fake a vote). Votes on the existing 2026-11-04 FX files (plain ny_dst): EURUSD 2010–2018 ny 15 / eu 1, 2019–2024 eu 8 / ny 1; USDJPY 2010–2018 ny 14 / eu 2, 2019–2024 eu 7. Tests: tests/test_ingest_histdata.py (7, synthetic). Background downloads continue (done: SPX, HKX, ETX, GRX, NSX, JPX, XAU, BCO); all CFDs will be re-landed from cache with `histdata_rule` after the downloads.
- 02:00 all downloads done, no 429, no 4xx/5xx (fetch_log). All 11 CFDs carried by HistData. ETXEUR: pages for 2020–2026 serve an EMPTY token (file not offered) and the 2019 file stops 2019-02-01 → ETXEUR = 2010-11-15..2019-02-01 only, no hold-out part.
- 02:01 FX hold-out landed under DATA_ROOT/holdout/histdata_fx_1m/<PAIR> (clock histdata_rule; ≈679k rows each, 2025-01-01..2026-10-30); outcome-free QA PASS ×4. HistData artifact: the raw files lack local 19:00–19:59 on the Sunday of the EU spring switch (2025-03-30, 2026-03-30).
- 02:08 all 11 CFDs re-landed from cache with `histdata_rule` (manifest rows replaced; mismatch-week votes agree with the rule on every symbol except noisy commodity/UKX years). QA running for 21 datasets.
=== progress 02:09: GRXEUR 2020-06-15..2023-12-01 (637,707 bars) and ETXEUR 2018-12-17.. (22,163 bars) EXCLUDED as mislabelled (EU50 levels in GRX; IBEX-like levels in ETX); WTIUSD 2024-01..2026-05 not offered by HistData (empty token). QA rerun.
- 02:35 bug fixed in `common.write_parquet_partitioned`: a re-land left stale `year=*` parts behind (GRX/ETX); stale parts now removed; GRX/ETX re-landed; all 47 histdata manifest sha256 re-verified against disk (0 mismatches).
- 02:40 QA reports written for 25 datasets (data/qa/histdata_*.md) with auditor notes. Verdicts: PASS — FRX, HKX, UKX, XAU (IS) and every hold-out except as listed; PASS with caveats — SPX/NSX/JPX (spike-reversal prints), BCO (ICE-like hours, 85% of the 23 h template), ETX (84% coverage; span ends 2018-12-14), GRX (span excluded), WTI (breaks are the real 2020 crash/roll; 106 spike reversals), SPX hold-out (US-anchor peaks compete, mismatch checks OK), WTI hold-out (2026-06..10 only, clock not testable). Cross-source: SPX vs ^GSPC 0.998 (level ratio 0.9995), NSX 0.93, GRX 0.90 / ETX 0.87 / FRX 0.87 / UKX 0.84 vs GLSTOCK, BCO 0.87 / WTI 0.78 vs CMDTY, XAU 0.63 vs GOLDPM (second-source dating), HKX/JPX loose (Asia timing). Inherited pins: SPX, GRX, ETX, JPX 2010–2018 CSVs 9/9 byte-identical.
- 02:42 manifest rendered; `python3 -m pytest -q quant-edge/tests` 61 passed, 1 skipped. Not committed. DONE.

## Open items for the Director
1. Existing `histdata_fx_1m_{EURUSD,GBPUSD,USDJPY,AUDUSD}` (2026-11-04, plain ny_dst) are 1 h early in the 2019–2024 US/EU mismatch weeks. Re-landing with `clock=histdata_rule` changes their sha256 (pinned by Q-0001/Q-0003). Batch-1 rows touching mismatch weeks: March FOMC days 2019–2024 (Q-0003), Oct-31 month-ends 2019/2024 etc. (Q-0001).
2. The gateway's hold-out window reads the row's dataset; hold-out bars now live in separate `*_holdout` datasets, so a hold-out read must name the `_holdout` dataset (gateway untouched).
3. ETXEUR after 2018-12 and WTIUSD 2024-01..2026-05 are not offered by HistData; the GRXEUR 2020-06..2023-12 span holding EU50 levels was excluded, not re-labelled.
