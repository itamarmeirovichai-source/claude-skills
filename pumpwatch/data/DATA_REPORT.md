# PumpWatch data report

> Data department, 4 October 2026. Anything not checked is marked **UNVERIFIED**.
> Regenerate the market data with `python scripts/fetch_real_data.py --cik-overrides data/cik_overrides.csv` (run it from `pumpwatch/`).

## 1. What is in `data/`

| file | what | rows |
|---|---|---|
| `cases.csv` | labelled cases: `ticker,label,start,end,note,source_url,confidence` (the format `backtest.load_cases` reads) | 32 pump, 46 legit |
| `cases_evidence.csv` | audit trail per case: issuer name, CIK, a verbatim quote from the source (30 words or fewer), the Yahoo sanity check, and for legit cases the % move and market cap | 78 |
| `cik_overrides.csv` | `ticker,cik,company,yahoo_symbol` for the fetcher: the CIK at the time (most pump tickers are delisted and missing from SEC's current ticker map) and the current Yahoo symbol when it changed (EDAP→FOCL, CEI→CEIN) | 74 |
| `real/bars.csv` | daily OHLCV `ticker,day,open,high,low,close,volume` (Yahoo, split-adjusted) | 6,871 |
| `real/filings.csv` | EDGAR filings `ticker,day,form,title` (day = EDGAR filingDate) | 3,873 |
| `real/coverage.csv` | per ticker: CIK, names on Yahoo and EDGAR, window, bar and filing counts, status, warnings | 74 |
| `work/` | team working files and the rejected-candidate lists with reasons (`*_rejected.md`) | |

Window per ticker: from 120 days before the first case start to 30 days after the last case end. Filings go back 400 more days so the dormant-shell check in `signals/corporate.py` can see the history.

## 2. Network access (tested 4 Oct 2026 from this environment)

| host | result |
|---|---|
| www.sec.gov, data.sec.gov, efts.sec.gov (full-text search) | **reachable** (requests send the User-Agent `PumpWatch research contact@example.com`; the fetcher keeps SEC calls under 5 per second) |
| query1.finance.yahoo.com (chart API) | **reachable** with a short browser User-Agent. A full Chrome User-Agent string gets HTTP 429. |
| www.justice.gov | the home page loads, but press-release pages return an Akamai bot-challenge page. **DOJ sources were not used**, and we did not try to get around the challenge. |
| www.finra.org, www.otcmarkets.com | reachable (not used as sources) |
| stooq.com | **not reachable** (the tunnel closed mid-exchange) |
| api.nasdaq.com | **not reachable** (timeout) |
| courtlistener.com | **blocked** (403) |

## 3. How cases were collected and checked

**Pump cases (team A).** Taken from SEC primary documents only:
- litigation complaints and releases: Constantin et al. ("Atlas Trading"), Sabo, Beck, Global Wholehealth Partners, Ballout, Fassari, Nielsen, Nicosia et al., Casey et al., Gomes et al. and Tobin et al.;
- six SEC trading-suspension orders.

How the dates were set:
- `start` is the first public promotion day stated in the source.
- `end` is the collapse day when the source states one (high confidence, the 3 GWHP rows). Otherwise it is the end of the dump or promotion period, or the suspension date, as the source states it (medium).
- No date was taken from price data.

No source document supplies more than 7 rows. About 60 candidates were rejected (`work/pump_cases_rejected.md`). On review, the Head of Data also dropped 3 more rows:
- **BIVI ×2:** the stock never collapsed, so this was scalping, not a pump and dump.
- **GRCU:** a 2016 case with no CIK, and Yahoo now shows a different company name, so the ticker may have been reused.

**Legit controls (team B):**
- **How they were found:** a Yahoo screen of about 6,000 still-listed Nasdaq/NYSE tickers for days with a close-to-close gain of +30% or more since 2019. Each jump was then matched to the company's 8-K or 6-K press release filed that day or the day before.
- **Market cap:** under $300M before the news. The share count comes from the cover page or from `dei:EntityCommonStockSharesOutstanding`; borderline cases were read off the 10-Q cover page.
- **News timing:** whether the release came pre-market, intraday or after the close is taken from the EDGAR acceptance time. `start` is the first trading day the news was public.
- **End date:** `end` is the highest close within the next 10 trading days (from Yahoo).
- **Taint screen:** candidates were screened with EDGAR full-text search for manipulation and pump-and-dump allegations. FLNT was dropped: a former vice chairman of Fluent's predecessor was a defendant in the SEC's 2018 Honig pump-and-dump case.

**Independent review by the Head of Data, on every row:**
- Every `source_url` was re-fetched: it returns HTTP 200, and the ticker or the company name appears in the text (for PDFs, via `pdftotext`).
- For every pump row, the date strings appear in the source, with two exceptions:
  - AREC's start: the source says "the day before" March 18, so the date is derived.
  - SSTU: the complaint is a scanned image with no text layer, so the dates are marked UNVERIFIED.
- For every legit row:
  - The % move and the end date were recomputed from fresh Yahoo data. All 46 match, and all moves are +30% or more.
  - The source filing's EDGAR filing date is 0–1 trading days before `start` (SEER is 4 calendar days, across the 3 July market holiday).
- The market caps were **not** recomputed independently. They are team B's figures, and team B checked the borderline ones against 10-Q cover pages.

## 4. Coverage and gaps

- **Pump rows with no bars: 12 of 32.** The tickers are ARGW, BEAG, DEVV, ENKS, GWHP (3 rows), ODYY, RGLS, TRCH, VIDA and WODI. Yahoo returns 404 or 400 for delisted or renamed symbols, so 20 of 32 pump rows have bars. All 46 legit rows have bars.
- **Pump tickers with no CIK: 4 (ARGW, ARYC, CASG, SSTU).** These have no EDGAR filings. ARGW has neither bars nor a CIK, so it is the most thinly covered pump case.
- **Zero filings despite a CIK:** ARCS, ENKS, PLWY, PUPS, UCSO, VIDA and ZNNC. These are OTC issuers that were not filing with the SEC during the case windows, so the empty result is real.
- **Zero-volume days in Yahoo data:** TMGI (106 of 106 bars), SSTU, UCSO, EPTI, PLWY, ZNNC, CASG, PUPS and NBTX. For sub-penny OTC stocks, some zero-volume days are real. For TMGI, and probably others, they are an artifact: Yahoo back-adjusts volume for later reverse splits and rounds it to an integer. **On these tickers the S1 and S2 market signals see little or nothing.** No source of unadjusted data is reachable from here.
- **No 2024–2026 "ramp-and-dump" cases.** The 17 SEC suspensions in 2024–2026 (QMMM, SDM, MAGH, EFTY, PLTS, CHSN, BYU and others) give the suspension date but no promotion start. DOJ indictments (Ostin/OST, CLEU, TDIC, the DOJ Atlas case) could not be read (see §2). They are listed in `work/pump_cases_rejected.md` as leads.
- **Pump rows before 2019: 6 (PUPS, ZNNC, VIDA, CASG, TMGI, EPTI).** By start year: 2017: 4, 2018: 2, 2019: 5, 2020: 12, 2021: 9. Legit rows: 2019: 6, 2020: 2, 2021: 3, 2022: 5, 2023: 6, 2024: 8, 2025: 8, 2026: 8. The two sets are not matched in time.
- **Repeat tickers:** CEI (2 rows), GWHP (3) and SSTU (2) have separate campaigns. A split by ticker keeps them together.

## 5. Limitations (read before trusting any backtest)

1. **`end` is usually not the collapse day.** 27 of 32 pump rows are medium confidence: the end of the dump or promotion window, or the trading-suspension date. For a suspension the real crash happens after trading resumes, so a "catch before end" is a little generous there.
2. **Several Atlas, Sabo and ABVC cases last only 1–2 days.** A daily-bar engine can barely lead them, and only promotion before the window could be detected.
3. **Social evidence exists only as quoted in SEC documents** (tweets, Discord posts, newsletters). It is in the notes and evidence column, not as `Post` records. No social-media data was collected. Under the CEO's scope decision, X, Telegram and Reddit data are out.
4. **Yahoo serves the current holder of a symbol.** The fetcher flags name mismatches and first trade dates after a case, and drops bars that miss every case window. Remaining risk: CEI was fetched as CEIN (same CIK, now Viking Global Technologies); TMGI's Yahoo name is "Transglobal Management Group" (same CIK as the issuer named in the complaint).
5. **Survivorship bias in the legit set.** Only companies still listed and on Yahoo could be verified. Acquired or delisted small caps are missing.
6. **The taint check is incomplete.** EDGAR full-text search does not index SEC litigation releases, so a legit control could still have an enforcement history we missed (UNVERIFIED that none do).
7. **News mixed with other events:** URGN's trial data came together with a private placement, CELC's licence with a financing, and VATE's FDA approval went to a subsidiary. LFCR, SSTI and SANG started at the end of September 2026, so their 10-day `end` window was not complete yet.
8. **EDGAR filing titles come only from item codes and document descriptions.** A name change or reverse split filed under item 5.03 does not read as "name change". Synthetic `NAME-CHANGE` rows are dated the day after the `to` date of EDGAR's `formerNames` record, which is approximate.
9. **First engine run on this data, for information only** (default config, threshold 35, no social data, no calibration, unchanged local `engine.py`):
   - 5 of 32 pumps caught before `end`.
   - 21 of 46 legit movers flagged.
   - 75 false alerts.
   - 12 pump rows had no bars, so they could not be caught.

   This is not an evaluation; the CEO owns calibration.

## 6. Requests to CEO

1. **Volume units.** Yahoo's split-adjusted volume makes serially reverse-split tickers look silent. S1 and S2 could skip tickers where more than 20% of bars have zero volume (from `coverage.csv`), or use dollar volume. Alternatively, approve a paid source of unadjusted data.
2. **A field for case kind.** Consider adding `end_kind` (collapse / dump_end / suspension) to `Case`, so suspension-ended cases can be scored differently. It would be an extra CSV column; `load_cases` already ignores unknown columns.
3. **Small-cap universe.** The false-alert denominator has no unlabelled small-cap universe yet. If wanted, the data department can fetch a random sample of same-era OTC and Nasdaq micro-caps as background.
4. **DOJ access.** Reaching justice.gov needs a browser-based or manual download to add the 2024–2026 ramp-and-dump cases (OST, CLEU and others).

## 7. All cases

Data status comes from `real/coverage.csv`. `no_bars` means no Yahoo bars, so the case can only be tested on filings. `no_cik` means no EDGAR filer was found.

| # | ticker | label | start | end | conf | bars | filings | data status | source |
|---|---|---|---|---|---|---|---|---|---|
| 1 | CEI | pump | 2021-08-04 | 2021-08-05 | medium | 150 | 90 | ok | [comp-pr2022-221.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp-pr2022-221.pdf) |
| 2 | CEI | pump | 2021-09-01 | 2021-10-05 | medium | 150 | 90 | ok | [comp-pr2022-221.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp-pr2022-221.pdf) |
| 3 | ALZN | pump | 2021-06-29 | 2021-06-30 | medium | 33 | 61 | ok | [comp-pr2022-221.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp-pr2022-221.pdf) |
| 4 | VISL | pump | 2021-03-02 | 2021-03-03 | medium | 104 | 87 | ok | [comp-pr2022-221.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp-pr2022-221.pdf) |
| 5 | TRCH | pump | 2021-02-10 | 2021-02-23 | medium | 0 | 92 | no_bars | [comp-pr2022-221.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp-pr2022-221.pdf) |
| 6 | ABVC | pump | 2021-08-11 | 2021-08-11 | medium | 106 | 50 | ok | [comp-pr2022-221.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp-pr2022-221.pdf) |
| 7 | AREC | pump | 2021-03-17 | 2021-03-18 | medium | 103 | 85 | ok | [comp-pr2022-221.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp-pr2022-221.pdf) |
| 8 | RGLS | pump | 2020-06-12 | 2020-06-12 | medium | 0 | 88 | no_bars | [comp25736.pdf](https://www.sec.gov/files/litigation/complaints/2023/comp25736.pdf) |
| 9 | PUPS | pump | 2017-04-23 | 2017-05-18 | medium | 119 | 0 | ok (zero-vol days) | [comp25325.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp25325.pdf) |
| 10 | ZNNC | pump | 2017-09-24 | 2017-09-27 | medium | 107 | 0 | ok (zero-vol days) | [comp25325.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp25325.pdf) |
| 11 | VIDA | pump | 2017-10-30 | 2017-12-11 | medium | 0 | 0 | no_bars | [comp25325.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp25325.pdf) |
| 12 | CASG | pump | 2018-04-25 | 2018-05-01 | medium | 108 | 0 | no_cik (zero-vol days) | [comp25325.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp25325.pdf) |
| 13 | TMGI | pump | 2018-12-15 | 2018-12-20 | medium | 106 | 32 | ok (zero-vol days) | [comp25325.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp25325.pdf) |
| 14 | PLWY | pump | 2019-03-11 | 2019-03-14 | medium | 104 | 0 | ok (zero-vol days) | [comp25325.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp25325.pdf) |
| 15 | UCSO | pump | 2019-04-29 | 2019-05-02 | medium | 105 | 0 | ok (zero-vol days) | [comp25325.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp25325.pdf) |
| 16 | ENKS | pump | 2021-03-09 | 2021-06-22 | medium | 0 | 0 | no_bars | [comp26122.pdf](https://www.sec.gov/files/litigation/complaints/2024/comp26122.pdf) |
| 17 | ARCS | pump | 2020-12-09 | 2020-12-18 | medium | 110 | 0 | ok | [comp25185.pdf](https://www.sec.gov/files/litigation/complaints/2021/comp25185.pdf) |
| 18 | ARYC | pump | 2020-03-02 | 2020-04-13 | medium | 132 | 0 | no_cik | [comp24832.pdf](https://www.sec.gov/files/litigation/complaints/2020/comp24832.pdf) |
| 19 | GWHP | pump | 2020-06-23 | 2020-06-25 | high | 0 | 29 | no_bars | [comp25332.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp25332.pdf) |
| 20 | GWHP | pump | 2020-08-28 | 2020-09-24 | high | 0 | 29 | no_bars | [comp25332.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp25332.pdf) |
| 21 | GWHP | pump | 2020-11-03 | 2020-11-17 | high | 0 | 29 | no_bars | [comp25332.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp25332.pdf) |
| 22 | ODYY | pump | 2020-03-26 | 2020-07-06 | medium | 0 | 26 | no_bars | [comp25529.pdf](https://www.sec.gov/files/litigation/complaints/2022/comp25529.pdf) |
| 23 | EBET | pump | 2021-04-15 | 2021-04-16 | medium | 22 | 28 | ok | [comp26071.pdf](https://www.sec.gov/files/litigation/complaints/2024/comp26071.pdf) |
| 24 | SSTU | pump | 2020-03-23 | 2020-04-03 | medium | 212 | 0 | no_cik (zero-vol days) | [lr-24839](https://www.sec.gov/enforcement-litigation/litigation-releases/lr-24839) |
| 25 | SSTU | pump | 2019-10-28 | 2020-02-03 | low | 212 | 0 | no_cik (zero-vol days) | [lr-24839](https://www.sec.gov/enforcement-litigation/litigation-releases/lr-24839) |
| 26 | AEMD | pump | 2020-01-22 | 2020-02-07 | medium | 114 | 90 | ok | [34-88142-o.pdf](https://www.sec.gov/files/litigation/suspensions/2020/34-88142-o.pdf) |
| 27 | BEAG | pump | 2019-05-22 | 2019-07-02 | medium | 0 | 21 | no_bars | [34-86271-o.pdf](https://www.sec.gov/files/litigation/suspensions/2019/34-86271-o.pdf) |
| 28 | DEVV | pump | 2020-03-20 | 2020-05-11 | medium | 0 | 16 | no_bars | [34-88846-o.pdf](https://www.sec.gov/files/litigation/suspensions/2020/34-88846-o.pdf) |
| 29 | WODI | pump | 2020-05-04 | 2020-05-21 | medium | 0 | 16 | no_bars | [34-88916-o.pdf](https://www.sec.gov/files/litigation/suspensions/2020/34-88916-o.pdf) |
| 30 | LITH | pump | 2020-03-12 | 2020-04-08 | medium | 122 | 25 | ok | [34-88607-o.pdf](https://www.sec.gov/files/litigation/suspensions/2020/34-88607-o.pdf) |
| 31 | ARGW | pump | 2019-01-17 | 2019-02-04 | low | 0 | 0 | no_bars | [34-85049-o.pdf](https://www.sec.gov/files/litigation/suspensions/2019/34-85049-o.pdf) |
| 32 | EPTI | pump | 2017-06-12 | 2017-06-27 | medium | 115 | 13 | ok (zero-vol days) | [comp24583.pdf](https://www.sec.gov/files/litigation/complaints/2019/comp24583.pdf) |
| 33 | AXSM | legit | 2019-01-07 | 2019-01-08 | high | 104 | 59 | ok | [a19-1343_1ex99d1.htm](https://www.sec.gov/Archives/edgar/data/1579428/000110465919000962/a19-1343_1ex99d1.htm) |
| 34 | EGAN | legit | 2019-02-08 | 2019-02-11 | high | 104 | 70 | ok | [ex-99d1.htm](https://www.sec.gov/Archives/edgar/data/1066194/000155837019000458/ex-99d1.htm) |
| 35 | EDAP | legit | 2019-04-02 | 2019-04-11 | high | 109 | 11 | ok | [exh_991.htm](https://www.sec.gov/Archives/edgar/data/1041934/000117184319002142/exh_991.htm) |
| 36 | SMSI | legit | 2019-07-26 | 2019-08-08 | high | 113 | 83 | ok | [smsi-ex991_6.htm](https://www.sec.gov/Archives/edgar/data/948708/000156459019026114/smsi-ex991_6.htm) |
| 37 | ARDX | legit | 2019-09-03 | 2019-09-12 | high | 112 | 61 | ok | [d795858d8k.htm](https://www.sec.gov/Archives/edgar/data/1437402/000119312519235868/d795858d8k.htm) |
| 38 | FLGT | legit | 2019-11-05 | 2019-11-08 | high | 108 | 41 | ok | [flgt-ex991_6.htm](https://www.sec.gov/Archives/edgar/data/1674930/000156459019039801/flgt-ex991_6.htm) |
| 39 | RVP | legit | 2020-05-04 | 2020-05-11 | medium | 109 | 199 | ok | [tm2018538d1_8k.htm](https://www.sec.gov/Archives/edgar/data/946563/000110465920056151/tm2018538d1_8k.htm) |
| 40 | SPRO | legit | 2020-09-08 | 2020-09-08 | high | 106 | 55 | ok | [d54756dex992.htm](https://www.sec.gov/Archives/edgar/data/1701108/000119312520240546/d54756dex992.htm) |
| 41 | CELC | legit | 2021-04-09 | 2021-04-12 | high | 105 | 49 | ok | [celc_ex991.htm](https://www.sec.gov/Archives/edgar/data/1603454/000165495421003990/celc_ex991.htm) |
| 42 | BBW | legit | 2021-05-26 | 2021-06-08 | high | 114 | 63 | ok | [a52433065ex99_1.htm](https://www.sec.gov/Archives/edgar/data/1113809/000115752321000715/a52433065ex99_1.htm) |
| 43 | SOTK | legit | 2021-10-13 | 2021-10-13 | high | 107 | 62 | ok | [ex99-1.htm](https://www.sec.gov/Archives/edgar/data/806172/000117152021000411/ex99-1.htm) |
| 44 | HDSN | legit | 2022-03-09 | 2022-03-22 | high | 113 | 73 | ok | [tm228676d1_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/925528/000110465922031528/tm228676d1_ex99-1.htm) |
| 45 | BKSY | legit | 2022-05-25 | 2022-05-31 | medium | 109 | 119 | ok | [eocl-pressrelease_blacksky.htm](https://www.sec.gov/Archives/edgar/data/1753539/000175353922000039/eocl-pressrelease_blacksky.htm) |
| 46 | TSHA | legit | 2022-10-25 | 2022-10-25 | high | 106 | 60 | ok | [d411848dex991.htm](https://www.sec.gov/Archives/edgar/data/1806310/000119312522267999/d411848dex991.htm) |
| 47 | TACT | legit | 2022-11-11 | 2022-11-25 | high | 115 | 84 | ok | [ex99_1.htm](https://www.sec.gov/Archives/edgar/data/1017303/000121465922013498/ex99_1.htm) |
| 48 | ORIC | legit | 2022-12-22 | 2023-01-03 | high | 112 | 58 | ok | [d399008dex991.htm](https://www.sec.gov/Archives/edgar/data/1796280/000119312522310169/d399008dex991.htm) |
| 49 | SOPH | legit | 2023-03-14 | 2023-03-16 | medium | 104 | 39 | ok | [dp190609_ex9901.htm](https://www.sec.gov/Archives/edgar/data/1840706/000095010323004062/dp190609_ex9901.htm) |
| 50 | SCYX | legit | 2023-03-30 | 2023-04-03 | high | 106 | 52 | ok | [scyx-20230330.htm](https://www.sec.gov/Archives/edgar/data/1178253/000095017023010748/scyx-20230330.htm) |
| 51 | NBTX | legit | 2023-05-05 | 2023-05-05 | high | 103 | 68 | ok (zero-vol days) | [exh_991.htm](https://www.sec.gov/Archives/edgar/data/1760854/000117184323002918/exh_991.htm) |
| 52 | URGN | legit | 2023-07-27 | 2023-07-28 | high | 104 | 68 | ok | [d538950d8k.htm](https://www.sec.gov/Archives/edgar/data/1668243/000119312523195560/d538950d8k.htm) |
| 53 | ULBI | legit | 2023-07-27 | 2023-08-08 | high | 112 | 56 | ok | [ex_548759.htm](https://www.sec.gov/Archives/edgar/data/875657/000143774923020793/ex_548759.htm) |
| 54 | DCTH | legit | 2023-08-15 | 2023-08-23 | high | 111 | 101 | ok | [d324309dex991.htm](https://www.sec.gov/Archives/edgar/data/872912/000119312523212940/d324309dex991.htm) |
| 55 | AXTI | legit | 2024-02-23 | 2024-02-27 | high | 106 | 32 | ok | [axti-20240222xex99d1.htm](https://www.sec.gov/Archives/edgar/data/1051627/000155837024001530/axti-20240222xex99d1.htm) |
| 56 | APEI | legit | 2024-03-06 | 2024-03-06 | high | 103 | 85 | ok | [tm247734d1_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/1201792/000110465924030996/tm247734d1_ex99-1.htm) |
| 57 | INOD | legit | 2024-05-08 | 2024-05-21 | high | 113 | 54 | ok | [tm2412945d1_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/903651/000110465924058055/tm2412945d1_ex99-1.htm) |
| 58 | ACIU | legit | 2024-05-13 | 2024-05-14 | high | 105 | 49 | ok | [dp211110_ex9901.htm](https://www.sec.gov/Archives/edgar/data/1651625/000095010324006573/dp211110_ex9901.htm) |
| 59 | TTEC | legit | 2024-09-30 | 2024-10-11 | high | 112 | 51 | ok | [tm2425158d1_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/1013880/000110465924103930/tm2425158d1_ex99-1.htm) |
| 60 | MNPR | legit | 2024-10-24 | 2024-10-24 | high | 106 | 64 | ok | [ex_735003.htm](https://www.sec.gov/Archives/edgar/data/1645469/000143774924031957/ex_735003.htm) |
| 61 | CRNC | legit | 2024-11-21 | 2024-12-02 | high | 112 | 95 | ok | [crnc-ex99_1.htm](https://www.sec.gov/Archives/edgar/data/1768267/000095017024129486/crnc-ex99_1.htm) |
| 62 | CADL | legit | 2024-12-11 | 2024-12-19 | high | 109 | 71 | ok | [d901922dex991.htm](https://www.sec.gov/Archives/edgar/data/1841387/000119312524274870/d901922dex991.htm) |
| 63 | VATE | legit | 2025-01-21 | 2025-01-31 | high | 109 | 60 | ok | [a202410258-kxexhibit991.htm](https://www.sec.gov/Archives/edgar/data/1006837/000100683725000002/a202410258-kxexhibit991.htm) |
| 64 | MASS | legit | 2025-03-04 | 2025-03-17 | high | 112 | 68 | ok | [tm258071d1_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/1555279/000110465925020021/tm258071d1_ex99-1.htm) |
| 65 | REKR | legit | 2025-06-03 | 2025-06-04 | high | 105 | 97 | ok | [ex_826235.htm](https://www.sec.gov/Archives/edgar/data/1697851/000143774925019217/ex_826235.htm) |
| 66 | IMXI | legit | 2025-08-11 | 2025-08-11 | high | 103 | 52 | ok | [ef20053638_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/1683695/000114036125029957/ef20053638_ex99-1.htm) |
| 67 | TLS | legit | 2025-08-11 | 2025-08-22 | high | 110 | 71 | ok | [q22025earningspressrelease.htm](https://www.sec.gov/Archives/edgar/data/320121/000032012125000037/q22025earningspressrelease.htm) |
| 68 | ENTA | legit | 2025-09-29 | 2025-09-29 | high | 105 | 48 | ok | [d16388dex991.htm](https://www.sec.gov/Archives/edgar/data/1177648/000119312525221527/d16388dex991.htm) |
| 69 | OMER | legit | 2025-10-15 | 2025-10-15 | high | 106 | 36 | ok | [ex_870020.htm](https://www.sec.gov/Archives/edgar/data/1285819/000143774925030968/ex_870020.htm) |
| 70 | VELO | legit | 2025-12-22 | 2026-01-06 | high | 114 | 109 | ok | [ex99-1.htm](https://www.sec.gov/Archives/edgar/data/1825079/000149315225028653/ex99-1.htm) |
| 71 | NDLS | legit | 2026-03-26 | 2026-03-26 | high | 102 | 61 | ok | [a2025q4ex991earningsrelease.htm](https://www.sec.gov/Archives/edgar/data/1275158/000127515826000019/a2025q4ex991earningsrelease.htm) |
| 72 | BLZE | legit | 2026-05-05 | 2026-05-05 | high | 105 | 49 | ok | [ex991blze20260331earningsp.htm](https://www.sec.gov/Archives/edgar/data/1462056/000162828026029795/ex991blze20260331earningsp.htm) |
| 73 | BWEN | legit | 2026-05-12 | 2026-05-15 | high | 106 | 48 | ok | [exh_991.htm](https://www.sec.gov/Archives/edgar/data/1120370/000117184326003268/exh_991.htm) |
| 74 | SEER | legit | 2026-07-06 | 2026-07-07 | high | 105 | 95 | ok | [ck0001726445-ex99_1.htm](https://www.sec.gov/Archives/edgar/data/1726445/000119312526294994/ck0001726445-ex99_1.htm) |
| 75 | CHPT | legit | 2026-09-03 | 2026-09-17 | high | 104 | 62 | ok | [chpt8-kerfy2027q2exx991.htm](https://www.sec.gov/Archives/edgar/data/1777393/000177739326000061/chpt8-kerfy2027q2exx991.htm) |
| 76 | LFCR | legit | 2026-09-28 | 2026-09-29 | high | 87 | 54 | ok | [ef20082009_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/1005286/000114036126037767/ef20082009_ex99-1.htm) |
| 77 | SSTI | legit | 2026-09-29 | 2026-10-01 | high | 87 | 63 | ok | [d107296dex991.htm](https://www.sec.gov/Archives/edgar/data/1351636/000119312526406024/d107296dex991.htm) |
| 78 | SANG | legit | 2026-09-29 | 2026-09-29 | high | 87 | 19 | ok | [tm2626529d1_ex99-1.htm](https://www.sec.gov/Archives/edgar/data/1753368/000110465926111514/tm2626529d1_ex99-1.htm) |
