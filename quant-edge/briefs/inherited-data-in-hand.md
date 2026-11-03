# Inherited data in hand (Scribe, 2026-11-03)

Paths: PF=`~/quant-edge-inherited/pr4/skills/prop-fleet`, D=`PF/agents/daily`, DH=`D/2026-10-06-0247/data_hunter`. Pins live in fetch scripts (`D/2026-10-04/data_fetch.py`, `D/2026-10-05/data_hunter/data_fetch_more.py`, `DH/data_fetch_d3.py`) and loaders (`D/orb-H0020/loaders.py`). Raw files were kept in the previous session's scratch and are gone; refetch by commit and verify the hash. Each line: dataset; source; period, resolution; sha256; licence; gaps; clock.

## Intraday, free
- SPXUSD 1m 24h; HistData via GitHub FutureSharks/financial-data master `SPXUSD/DAT_ASCII_SPXUSD_M1_{2010..2018}.csv`; 2010-11-15..2018-12-31, 2.1M bars, 2,090 RTH sessions, no volume; per-year pins (2010 `1166316b…`, 2018 `7f20d258…`) in `D/orb-H0020/loaders.py`; HistData personal use; only 32–34% of 2012–13 weekdays have ≥370 bars, 71 sessions lack 15:59; NY local WITH DST (`R/gapfade-H0012.md` Data).
- SPY 1m RTH (Polygon copy); Ascensao/Intraday-momentum-strategy@5a9e9569 `spy_intra_data.csv` (Git LFS); 2019-01-02..2025-07-18, 1,645 sessions; `d4671c48…`; licence unclear (Polygon redistributed); dividend back-adjusted (ratio to raw 0.9936→1.0000), 12 half-days carry post-13:00 bars; NY (`D/2026-10-05/data_hunter/second_sources.txt`).
- NQ 1m front month; hindsight-finance/Silver-Bullet-AM-Session@9f00a853 `nq_1m.parquet`; 2020-08-31..2025-11-21, 1,349 sessions, unadjusted; `46f2a9a6…`; unclear; contract switches at the 00:00 ET bar, 126 roll-week sessions, 35 CME holiday sessions; DateTime_ET (`R/orb-H0020.md`, `D/w2-events/redteam/findings.md`).
- QQQ 1m; soyMarioPineda/Research-QQQ@cc71b31d `QQQ_1min.csv`; 2017-01-26..2026-03-06; `a48cbb92…`; vendor unknown; ≈unadjusted (−0.014..−0.024 USD vs Alpaca), 202 short sessions, 42 zero-volume bars; NY offset (`DH/qqq_profile.txt`).
- SPY 1m 04:00–20:00; trilespharm2/bactest-openclaw@6b6b00db `data/spy_1min.parquet`; 2024-03-28..2026-08-07; `3bc080a1…`; Polygon copy; matches IBKR to the cent on 98.2% of bars; epoch-ms UTC (`DH/spy_qqq_more.txt`).
- SPY/QQQ 1m IBKR; `*_IBKR_1min_1year_20251110.csv` (pins in data_fetch_more.py); 2024-10-31..2025-11-07, 256 sessions, unadjusted; NY offset; the raw reference for adjustment checks.
- ES 1m TopstepX; commit 60abd3fb `ES/ES_1min_20260120_20260415.csv`; 2026-01-20..04-15; cross-check only (57 of 58 days match FirstRate; `D/2026-10-05/data_hunter/es_crosscheck.txt`).

## Intraday, LICENCE HOLD (board Decision 8: cross-checks only until Itamar rules)
- ES 1m RTH + 5m 24h FirstRate; jimmuell/mes-orb-strategy@48993b9 `api/data/ES_full_1min_rth.parquet` (28,349,422 bytes); 2008-01-02..2026-04-10, 4,711 sessions; `093596df…` (`PF/agents/board.md` Data); third-party copy of paid data; 44 CME-only sessions, rolls 1–3 days before Databento; NY-naive. A 349.8 MB 1m 24h LFS file was never downloaded.
- Databento ES.c.0/NQ.c.0 1m; Eric1K/Trading-Overnight-Drift@e7d69651 `es_1m_{2019..2026}.parquet`, `nq_1m_…` (per-year pins in `DH/data_fetch_d3.py`; warrenn copy identical on 1,757,339 rows); 2019-01-01..2026-09-25 (ES) / 09-11 (NQ), 23h; Databento no-redistribution; no RTH bars on 30 expiry Fridays, illiquid last ~6 sessions, 53 missing weekdays; UTC (`DH/eric_profile.txt`, `DH/xcheck.txt`).
- Databento NQ.c.0 5m; prashanthaitha24/nq-strategy-b-bot@bc199e73 `data/nq_databento_5min.csv`; to 2026-05-07; pin in data_fetch.py; same hold; used by F1 (`PF/agents/prereg/F1.csv` F1-00).

## Daily and other, free
- SqueezeMetrics DIX/GEX; Fluxus-Trade-Lab/fluxus-dashboard@c1eb927 `SqueezeMetrics/DIX.csv`; 2011-05-02..2026-10-02, 3,879 rows; `51bef9ea…9ce62`; public; published ≈17:52 ET (41 of 42 updates after the close), 8.9% GEX<0 (`R/gamma-H0019.md`, `DH/dix_pubtime.txt`).
- Oanda v20 M1 mid, 23 markets (6 FX, 8 indices, 5 commodities, 4 bond CFDs unused); FutureSharks@7ba1d404; 2005-01..2020-05-13; 4,611 file hashes in `D/w1-breadth/manifest.csv`; free; thin sessions AU200 18%, JP225 10%, UK100 no pre-08:00 bars until mid-2015, corn 26%; UTC (`D/w1-breadth/data_check.txt`).
- HistData DAX (GRXEUR), ESTX50 (ETXEUR) M1; same repo; 2010-11..2018-12; in manifest; NY WITH DST.
- Binance public data; data.binance.vision spot 1h 2018-07..2026-09, USDT-M perp 1d + funding, 57 fixed candidates; no pins (`D/w1-crypto/download.py`); public; zero-volume rows after delisting, funding intervals 4h/1h since 2023; UTC (`R/w1-crypto.md`).
- FRED H.10 FX, OECD 3m rates, DGS10/DGS30, Yahoo indices and GLD/SLV/USO; 1971/1990..2026-10-02 daily; sha256[:12] per file in `D/w1-fxtrend/run.txt` line 3; free; FRED/Yahoo blocked 29 Sep, open 11 Oct; noon NY fixes vs 16:00 closes (`PF/agents/prereg/D2_rules.md` §1).
- Yahoo daily: 10 index CFDs 1989/90..2026-10-12 (G2; stale opens ^AXJO 2012–19, ^FTSE 1999–2006); PIT S&P 500 (fja05680) + Yahoo 1999–2026, 432 of 1,214 tickers without history (E1, `R/w2-stocks.md` §2); Nasdaq earnings calendar 2008+, 231,682 rows (E1-05).
- SEC Form 4 2006Q1–2026Q1, 81 zips, 440,544 purchase rows; 55% of tickers lack Yahoo history (`R/insider-H0018.md` stage 1).
- Event calendar: federalreserve.gov FOMC + ALFRED release dates, bls.gov 403; `D/w2-events/events.csv` (ISM January defect noted in `redteam/findings.md`).
- Committed in `PF/data/`: `futures.csv` 55 futures daily 1984-01-03..2016-10-31 (rkohli3/TSMOM, excess returns, VF dropped); `asset_classes.csv` 9 classes 1970..2026-09-25, observed only from 1991-10-29, modelled history is fake (+122% year); `spx_open_close.csv` ^GSPC 1990–2026, opens stale 77%/64% in the 1990s/2000s (`PF/data/README.md`).

## Cross-checks and reachability
- ES–SPY 1m return corr 0.9841 over 639,306 minutes; daily open→close 0.9929; gap outliers all roll dates except 2020-03-16 (`es_crosscheck.txt`). FirstRate vs Databento: median diff 0 on 1,748 of 1,848 days (`DH/xcheck.txt`).
- Reachable then: GitHub raw/LFS, PyPI only; everything else proxy-blocked (`DH/host_probe.txt`). Now: Binance, HistData, FRED, CBOE, Yahoo/CFTC with browser UA; blocked Dukascopy, SSRN, lucidtrading.com (`quant-edge/data/licences.md`, `quant-edge/board.md`).
- Nothing is pinned yet in this program: `quant-edge/data/MANIFEST.md` is empty; DATA_ROOT is `~/quant-edge-data/`.
