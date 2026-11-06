# Brief: Department C data run (Head of Data playing Free-Data Hunter, Calendar and Clock Keeper, Ingestion Engineer, Data QA Auditor in sequence)

Output root: code under `quant-edge/src/qe/ingest/` and `quant-edge/src/qe/qa/` (the only places allowed to read raw files; `tests/test_no_direct_reads.py`
enforces it), market data under `~/quant-edge-data/` (never in the repo), one manifest row per dataset in `quant-edge/data/manifest.csv` (and the
human table `quant-edge/data/MANIFEST.md`), a QA report per dataset in `quant-edge/data/qa/<dataset_id>.md`, licence rows in `quant-edge/data/licences.md`.
Every dataset is a parquet file with a UTC `ts` column (bar OPEN time), partitioned by root and year when large. Compute budget: you are the one
compute agent; keep downloads polite (one request at a time, Retry-After honoured) and write the manifest row the moment a file lands.

1. Free-Data Hunter (reachability and licence first, record blocks, never route around them: Dukascopy datafeed is blocked, Alpaca needs keys that do not exist yet).
   Priority order, each only as far as the candidate lanes need it: (a) the inherited daily files in `~/quant-edge-inherited/pr4/skills/prop-fleet/data/`
   (read `data/README.md` there for provenance, clock and licence; futures.csv 1984–2016, asset_classes 1970–2026, spx_open_close 1990–2026) →
   `daily_futures_1984_2016`, `daily_assets_1970_2026`, `spx_oc_1990_2026`; (b) Yahoo (browser User-Agent) and Stooq daily for SPY, QQQ, IWM, DIA, GLD, SLV,
   USO, TLT, IEF, EFA, EWJ, ^GSPC, ^GDAXI, ^FTSE, ^N225, ^HSI, and CBOE VIX history (cdn.cboe.com) → regime filters, CAL-D benchmark, 60/40 reference;
   (c) HistData FX 1m 2010–2024 for EURUSD, GBPUSD, USDJPY, AUDUSD (NY local time WITH DST: convert to UTC per bar; verify with the outcome-free
   winter-vs-summer minute diagnostic) → lane 1 fixes; (d) CFTC COT weekly (fut_fin / fut_disagg history zips), FRED series, SqueezeMetrics GEX/DIX;
   (e) release calendars with exact timestamps 2010–2026: FOMC statements, BLS (CPI, NFP), EIA petroleum (Wed 10:30 ET) and natural gas (Thu 10:30 ET),
   USDA WASDE (12:00 ET), Treasury auction schedule, S&P/Russell/MSCI rebalance dates, LBMA auction times → `~/quant-edge-data/calendars/*.csv` with a
   manifest row each and the source URL + fetch date; (f) Binance only if a registered row needs it (D3 is closed).
2. Calendar and Clock Keeper: with `exchange_calendars` (installed; XNYS and CMES) build `src/qe/sessions.py`: per-root session template (RTH window in
   America/New_York, Globex hours, maintenance break, half days, holidays, listing date; the firm trading day starting at the 18:00 ET reopen; each firm's
   flat-by time), one New York index for everything, DST transitions, a roll-calendar scaffold per root (third-Friday weeks, `.v.0` flip-back rule). Tests:
   2024-07-03 and 2024-11-29 are half days (210 RTH bars), 2024-03-10 DST day, a trading-day boundary case at 17:59 vs 18:01 ET.
3. Ingestion Engineer: loaders `ingest/<source>.py` with `--dry-run`, sha256 on every file, idempotent re-runs, parquet writers; the Databento Day-1 purchase
   script `ingest/databento_day1.py` built on `qe.steward` (1d bars for all 37 roots + `definition` + `statistics`, ≈ $2; batch job; raw `.dbn.zst` kept;
   DRY-RUN ONLY until `quant-edge/data/databento_credit.json` exists; never read the key yourself: the databento client reads DATABENTO_API_KEY).
   Read `~/quant-edge-inherited/pr26/prompts/research/databento-cost-check-2026-11-03.md` first for prices, symbols and schemas.
4. Data QA Auditor: per dataset, bar counts against the session template (never against 1,380 minutes), gaps inside the template only, stale prints
   (open == previous close), outliers, cross-source agreement (e.g. SPX daily vs SPY), the clock diagnostic; write `data/qa/<dataset_id>.md`.
Read first: `quant-edge/briefs/00-common.md`, `WORK-LOG.md`, `board.md`, `briefs/inherited-data-in-hand.md` and `inherited-method-lessons.md` (if present).
Run `python3 -m pytest -q quant-edge/tests` before finishing; add tests for every loader (synthetic inputs). Write files as you go. Do not commit.
