# Pre-screen 2026-11-06: Department E (Chief Statistician + Red Team, default verdict "refuted")

- Inputs: `research/candidates.md` (ranked table A and top-40 briefs §C, read in parts), `PARAMETERS.md`, `briefs/00-common.md`, `WORK-LOG.md` Decisions D-001..D-017, `research/results/CAL-D.md`, `data/manifest.csv`, `tools/register.py`, `registry.csv` (107 rows; 1 program row, CAL-D, count 1; running N = 281).
- One web fact checked: Krohn–Mueller–Whelan, BoC SWP 2021-48 (https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf, fetched 2026-11-06). The sample is Jan 1999–Dec 2019. On p. 30 the authors say their reversal "is not driven by an end-of-month equity hedging channel as studied by Melvin and Prins (2015)" and that there is no stronger quarter-end effect.
- No market data was read and no P&L was computed. Nothing below is an edge or a signal. Every row is a hypothesis that is either pre-registered and under test, or declined.
- Data rule applied (Databento is UNCONFIRMED past the 72-hour trigger):
  - **free-now**: the data is a `manifest.csv` dataset.
  - **free-reachable**: the data is free (HistData index/commodity CFDs, SPXUSD 1m, transcripts, COT legacy) but has not been ingested yet. It needs Department C first.
  - **blocked-paid**: the row needs Databento. The cost given is the plan estimate in `candidates.md`.
  - **licence-hold**: the ES/NQ 1m copies, which are for cross-checks only.
- Bar in Sharpe units = 3.6807/√T. Criterion-4 power is Φ(S√T − 3.6807) at true Sharpe S = 1.5 / 2.0 / 2.4, computed with scipy.
  - T is the **decision window**. For a "derivative" row (D-009) that is only the part of the data the evidence never displayed.
  - Joint power (criteria 3+4+7, costs one third of gross) comes from the PARAMETERS.md table: 5 y 0.32/0.67/0.78, 8 y 0.63/0.82/0.89, 10 y 0.72/0.85/0.91. When costs are half of gross, criterion 3 alone passes about 5%.

## 1. The squeeze that decides almost every row (strongest Red Team objection overall)

The gate requires t = (per-trade Sharpe) × √(number of trades) ≥ 3.68 inside the decision window. Two families of rows fail this from opposite sides:

- **Event sleeves** (8–60 events/yr): the gross per trade is large relative to cost, but the noise is large too. With 10 years of FOMC days (80 events) a row needs per-event Sharpe ≥ 0.41. That means a mean of 41% of one day's s.d., every time. No published effect, cut by the 0.5 haircut, is near that. For example, MTV AUD gives ≈ 8 bp against ≈ 70 bp s.d., about 0.12.
- **Daily legs** (250–500 trades/yr): there are enough trades, but the haircut gross per trade is 1–2 bp against 1.2–3 bp round trip. These rows fail the economics screen, or the 2×-cost criterion, which needs gross ≥ ≈ 3× round trip.

The window that survives both is narrow: about ≥ 100 trades/yr with haircut gross ≥ 3× round trip and per-trade Sharpe ≥ 0.1. In the top 40, only AS C-4-01 (blocked-paid, $5) sits clearly inside it. The free-data rows in batch 1 are all event sleeves. Their criterion-4 power at a *true* Sharpe of 1.5 is high (0.84–1.00, because the windows are long). Their power at the Sharpe the evidence actually implies after haircut (≈ 0.2–0.8) is about 0.02–0.2. The batch is worth running only as cheap, honest tests of stack legs. It is not a route to an account strategy.

## 2. Top-40 screen

Column guide:
- **gross/RT** is the haircut gross per trade divided by the round trip at the 1× floors. Registering needs ≥ max(2 ticks, 2×). Certifying needs ≈ 3×.
- **T** is the decision-window years.
- **pow** is criterion-4 power at S = 1.5/2.0/2.4.
- **RT-obj**: the Red Team's single strongest objection, and whether it can be answered before registration (A = yes, N = no).
- Verdict codes: **B1** = eligible-batch-1, **L** = eligible-later, **R** = reject.

| # | id | closed-family verdict | look-ahead by construction | economics (haircut gross vs RT; trades/yr; Carver) | Red Team strongest objection (A/N) | firm-rule conflicts | data | T / bar / pow | verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 | AS C-4-01 X-sectional CO-OC reversal ES/NQ/YM/EMD/NKD | adjacent H0012/H0017, E1-08..10; not inside (relative, multi-index) | daily "open" ≠ 09:31 fill; 1d Globex bars give the 18:00 open, so 1h/1m is required | 12.5 bp/leg vs 2.6 bp pair RT = 4.8× ✓; 500/yr; Carver 0.8 Sharpe units of cost vs 1/3 × 3.9 pre-cost ✓ | Hong–Wang closure mechanism weakened by 23 h Globex; index futures nearly collinear, so the spread is dominated by NKD/EMD (wide RT) (N: empirical) | two opposite positions: check "hedging" wording at Tradeify/Lucid; MFFU 10:00 ET releases held through | blocked-paid $5 (1h × 5 roots); FTMO-CFD version free-reachable (HistData SPX/NSX/JPX) | 10 (2015–24) / 1.16 / 0.86 1.00 1.00 | **L**: first paid row once the trigger clears (only row inside the squeeze window) |
| 2 | AF C-1-01 month-end Treasury strike | none (H0023 other asset) | none | UB 5–15 bp vs 5–6 = 1–2.5× (<3×); ZN fails; 12–36/yr | strike moved 15:00→16:00 ET on 2021-01-14, so a post-change OOS has 3.9 y; cash→futures transmission unmeasured (N) | 16:05 exit vs Topstep 16:10 ET; consistency rules | blocked-paid $2 (1h) / $40 (1m) | 3.9 post-change / 1.86 / 0.24 0.61 0.86 | **L** (UB variant B only) |
| 3 | AF C-1-04 WMR fix legs | adjacent D2/D4, not fix-anchored | MSCI/month-end dates ex ante; MTD signal at T−1 | daily legs 0.75–1 bp vs 1.2–3 = FAIL; signed month-end 5–10 bp vs CFD 2–3 (2–4×), futures 1.3–2 (3–6×); 12/yr × 3 pairs | KMW (to 2019) find no month-end intensification in exactly these pairs; unsigned month-end is derivative and leaves 2020–24 = 4.9 y (<5, no institutional change) (A for the signed version only) | FTMO ±2 min news rule at entry/exit; futures leg spans 08:30 ET (MFFU/Lucid) | **free-now** (HistData + daily_assets) | 9.8 (2015-03..2024) / 1.18 / 0.84 1.00 1.00 | **B1** signed Melvin–Prins leg (Q-0001 CFD, Q-0002 futures twin); daily and unsigned legs **R** |
| 4 | AF C-1-09 index-rebalance days | none | rule-generated dates (verify against providers) | US legs unmeasured (Greenwood–Sammon: effect gone); UK100 4–6 bp vs 1.7 = 2.4–3.5×; 12–24/yr | index-level net demand ≈ 0 (adds and deletes net out); UK100 evidence 2023–26 overlaps any OOS (N) | UK100 post-close CFD pricing unverified | ES licence-hold; RTY blocked-paid $7; UK100 free-reachable (HistData UKXGBP) | ≤ 5 / 1.65 / 0.37 0.79 0.95 | **L** (low) |
| 5 | AF C-2-01 NG storage-day premium | none (E2 is ES/NQ) | none | implied 15–40 bp after haircut vs NG 7 bp = 2–6×; 52/yr | abstract only, sign and size unseen; sample probably ≤ 2018, so derivative 2010–18 and decision 2019–24 = 6 y (A: read the manuscript before registering) | MFFU/Lucid news window 10:30 Thu: Topstep/Bulenox/FTMO only | blocked-paid $7 (NG 1m RTH) | 6 / 1.50 / 0.50 0.89 0.99 | **L**: second paid row |
| 6 | SC C-13-01 ECB tone → EU50/GER40 | adjacent E2 (other bank/market) | tone only from text available by 15:30 CET; lexicon frozen pre-2015 | 15 bp vs 1.5–3 = 5–10× ✓; 8/yr | 8 events/yr × 7 y (evidence to 2017) = 56 events, so per-event Sharpe ≥ 0.49 is needed: structurally underpowered (N) | FTMO funded ±2 min not touched (15:30 entry) | free-reachable (HistData ETX/GRX + ECB transcripts) | 7 / 1.39 / 0.61 0.95 1.00 | **L** (stack leg; realistic power < 0.05) |
| 7 | AF C-2-13 FOMC/BoJ-day FX premium | adjacent E2-05/A-C40 | calendars public | pooled 5.4 bp vs CFD 2–3 bp < 3×; AUD leg 8 bp vs CFD 3 (2.7×) / 6A 2.3 (3.5×); 8/yr | premium may be a 1994–2013 ZLB/carry artefact; AUD rate differential turned negative 2019–23 (A: sign fixed, test decides) | holding through 14:00 FOMC banned at MFFU Rapid/Pro, Lucid Daily | **free-now** (HistData AUDUSD + cal_fomc); BoJ calendar missing | 11 (2014–24) / 1.11 / 0.90 1.00 1.00 | **B1** AUD leg (Q-0003 CFD, Q-0004 futures twin); BoJ leg **L** |
| 8 | IG C-12-15 month-end equity rebalancing | adjacent H0023/H0006 | MTD gap at T−1 | 2.5–7.5 bp vs 1.2 = 2–6×; 8–12/yr | HMM evidence window 1997–2023 covers all usable dates; the untouched windows are 1991–97 (pre-target-date regime, 5.8 y) or 2023-04..2024 (1.75 y) (N) | FTMO Swing swap on multi-day | free-now (daily) / ES licence-hold | ≤ 5.8 / 1.53 / ≈0 at realistic | **R**: no clean ≥ 5 y window with the mechanism alive |
| 9 | AF C-1-05 Tokyo 9:55 fix 6J | D4 (check USDJPY windows) | **clock error in the brief**: 09:55 JST = 00:55 UTC = 19:55 EST / 20:55 EDT; the brief has winter and summer reversed | unconditional 1 bp vs 1.5–3 FAIL; gotobi 2.5–5 bp marginal; rollover spreads 17:00–18:05 ET | derivative: KMW 1999–2019 + Krueger 2023–26 leave 2020–22 = 3 y (N) | FTMO rollover spread; 19:30/19:50 ET JP data inside | free-now | 3 / 2.13 / 0.14 0.41 0.68 | **R**: < 5 y untouched window; economics fail |
| 10 | AS C-4-07 hedging-overshoot reversal | adjacent H0006/H0019 (same window, next-day horizon) | rLH known 16:00, entry 18:00 ✓ | 4.5–8.5 bp vs MES 1.3 = 3.5–6.5× ✓; 40–60/yr | pooled R² < 0.3%; evidence 1974–2020 covers every root, so the decision window is 2020-06..2024 = 4.6 y < 5 (N without a Director ruling) | Topstep exit 15:00 ET for the equity leg | blocked-paid ≈ $40 (6 roots RTH) | 4.6 / 1.72 / 0.32 0.73 0.93 | **L** (needs ruling on the window) |
| 11 | IG C-11-01 prereg_orb30 | H0020 adjacent; differences stated before any run | D1 2010–18 is IS by declaration | RT 3–6% of 1R ✓ on structure; 150–200/yr | the most-mined intraday rule; H0020 net −0.005R; Zarattini–Aziz no OOS (N) | MFFU 10:00 releases (skip ±2 min) | SPXUSD 1m free-reachable (inherited pins, not in manifest); OOS ES blocked-paid $7 | 6 (2019–24) / 1.50 / 0.50 0.89 0.99 | **L**: inherited prereg obliges a D1 run after ingest |
| 12 | SC C-8-05 energy carry on FTMO swap | D2-04/05 (FX carry), H0007 adjacent | prior night's swap sign | turnover low, cost negligible ✓; 25–60/yr | FTMO's swap regime only exists from 2026-01-30; curve-carry proxy Sharpe 0.3–0.6 per commodity, so the sleeve is ≈ 0.6–0.9 (N) | NG gap vs 5% daily loss | blocked-paid $0.20 (1d + 2nd month); daily_futures has no curve | 12 (2013–24) / 1.06 / 0.92 1.00 1.00 | **L** |
| 13 | AS C-3-06 Treasury day/night | none | none | ZF/ZN 0.5 bp vs threshold 4 bp FAIL 4×; UB only on a 4-y midquote sample | fails the screen (N) | – | blocked-paid $3 | – | **R** (economics) |
| 14 | IG C-12-10 Platts Brent MOC | none | fixed window | 3.5–6.5 bp vs CFD 5 / CL 4 = 1–1.6× | below 2× RT after haircut (N) | – | BCOUSD free-reachable; CL $7 | – | **R** (economics) |
| 15 | IG C-12-04 CME margin-hike liquidation | none | must use the advisory's publication time, not its effective date | GC 10–17 bp (h 0.7) vs 1 bp ≥ 3× if it exists; 30–60/yr | retail FCM liquidation is small next to GC depth; advisory timestamps need labour (A: rule on publication time) | – | blocked-paid $28 | 14 / 0.98 / ≈1 | **L** |
| 16 | IG C-12-06 vol-control deleveraging | H0006/H0019 window; A-C30 | trigger from closes to t−1 | 2.5–7.5 bp vs 1.2 = 2–6×; ≈ 40/yr | Swing sign (short after a vol jump) contradicts the daily S&P reversal regularity that G2's data show; banks publish the flow daily (N) | consistency rules (sparse big days) | intraday: ES licence-hold, blocked-paid $7 | 10 / 1.16 | **L** intraday; Swing variant **R** |
| 17 | IG C-12-24 buyback-desk dip | G2 adjacent | blackout share needs a point-in-time earnings calendar | 2.5–5 bp vs 1.2 = 2–4×; 40–60/yr | no PIT earnings calendar for 500 names 2010–24 in hand; a mis-dated control arm (N) | MFFU FOMC days excluded | blocked-paid $7 (ES) + calendar labour | 10 / 1.16 | **L** |
| 18 | AF C-2-09 FOMC 3-day long Treasuries | E2-05 adjacent | calendar public | UB 6.5 bp vs 5–6 = 1.2× FAIL; ZN fails; 16/yr; IS t 2.4 | fails 2× RT (N) | holding through 14:00 banned at MFFU/Lucid | blocked-paid $2 | – | **R** (economics; "low-medium" in B does not survive the haircut) |
| 19 | SC C-13-02 FOMC vocal tone | inside E2-01..04 event, new data source | classifier trained on pre-2019 audio only | ±25 bp vs 1–3 ✓; 8/yr | 40 events in 2020–24 need per-event Sharpe 0.58; classifier noise (N) | MFFU/Lucid news | free-reachable (audio) + ES blocked-paid | 5 / 1.65 / ≈0 realistic | **R** (power) |
| 20 | AF C-1-02 month-end bond leg | none | MTD to T−1 | ZN fails; UB 3.5–10 vs 5–6 = 0.6–1.8× | fails 2× RT (N) | – | blocked-paid | – | **R** (economics) |
| 21 | AF C-1-03 auction-day inverted V | none | calendar public | ZN 1–3 bp per leg vs 3 FAIL; UB marginal | fails the screen (N) | – | blocked-paid $14 | – | **R** (economics) |
| 22 | AF C-2-03 EIA CL first-reaction fade | none | entry 10:33 ✓ | 5–7.5 bp vs 4 = 1.3–1.9× (passes 1×, fails 2×) | criterion 3 passes ≈ 5% by construction (N) | Lucid red folder | blocked-paid (shared CL) | – | **R** (economics) |
| 23 | AF C-2-07 LBMA auctions | none | round-imbalance timestamp must be verified | few bp vs GC 0.6–1; post-reform leakage ≈ 0 | imbalance history availability unverified; the Nilsson leg is dead (N) | PM auction vs US 10:00 releases | blocked-paid $20 + unverified data | 9 (2015–24) | **L** (imbalance leg only) |
| 24 | AF C-2-12 auction-result continuation | none | entry 13:06 ✓ | ZN 1–2 bp vs 3 FAIL; UB marginal | fails the screen (N) | – | blocked-paid (shared) | – | **R** (economics) |
| 25 | IG C-12-08 VIX-ETP rebalancing → ES | G1 adjacent | trigger needs VX at 15:45 | 1.5–4 bp vs 1.2 = 1.2–3.3× | VX intraday is CFE, not GLBX: the trigger is not purchasable in plan (N) | 16:00–16:15 only at Lucid/Tradeify/Bulenox | not purchasable | – | **R** (data + economics) |
| 26 | SC C-13-04 KRT COT liquidity | P-C17 cousin | release Fri 15:30 ✓ | net 0–15 bp/leg; 2× run negative per brief | fails criterion 3 by its own numbers (N) | – | COT legacy free-reachable (manifest has TFF only); daily futures to 2016 | – | **R** (economics) |
| 27 | SC C-8-06 commodity dip buy (swap sign) | G2 rule class on new markets: not a re-run | signal close ≠ fill: one-day delay required | 20–50 bp (energy) / 15–25 bp (gold) vs 5–7.5 bp incl. markup = 3–7×; 25–35/yr; Carver 0.15 units ✓ | only evidence is a paywalled in-sample blog on 2008–26; decided on 1990–2007, a different regime (A: window stated, hold-out bridges) | FTMO 5% daily loss path-wise; NG excluded | **free-now** (daily_futures CL/CO/HO/GC); hold-out 2025–26 daily blocked-paid ≈ $0.20 | 18 (1990–2007) / 0.87 / 1.00 1.00 1.00 | **B1** (Q-0005 energy, Q-0006 gold) |
| 28 | AS C-3-03 gold overnight drift | none | none | +3 bp → 1.5 bp vs GC 0.6 = 2.5× (<3×); FTMO RT 2 bp FAIL | no magnitudes in the abstract; 2015-03 auction change (N) | – | GC 1h blocked-paid $1; XAUUSD free-reachable | 9 (2015-04..2024) | **L** (futures only) |
| 29 | IG C-12-16 JHEQX collar | H0006/H0019, A-C26 | dates public | 5–20 bp "if the sign is right" | sign not fixable ex ante (unfixed = 2 counts); 4 informative events/yr (N) | – | ES licence-hold / $7 | – | **R** (no fixed sign; power ≈ 0) |
| 30 | SC C-8-10 HSI after-hours → HK50 reversal | H0012/H0017 logic, other market | AHT close known 09:15 HKT ✓ | 21 bp (h 0.7) vs 3–6 bp = 3.5–7×; 60–90/yr | HK50 CFD spread unknown; vendor CFD-index quality in the AHT window (A: 2× run + spread survey) | – | free-reachable (HistData HKXHKD) | 11 (2013-04..2024) / 1.11 / 0.90 1.00 1.00 | **L**: first batch-2 row after ingest |
| 31 | AS C-4-06 VIX-gated gold reversal | H0013/14 other horizon | VIX at T−1; closed bars | 20% reversion of 8–12 bp would pass 1.3 bp; 100–300/yr | 5-minute reversion competes with HFT makers; unmeasured (N) | exclude ±5 min releases | GC $20 shared; XAUUSD free-reachable | 10 | **L** |
| 32 | IG C-12-27 Nikkei SQ / HSI expiry | none | SQ calendar public | 10–20 bp vs 1.5/side ✓; 24/yr | evidence score 0; 24 events/yr → realistic power ≈ 0 (N) | – | free-reachable | 10 | **L** (stack only) |
| 33 | IG C-11-03 value (AMP) | D2 adjacent | none | cost negligible; Sharpe 0.3–0.6 standalone | cannot reach the bar alone by construction (N) | 30-day inactivity OK | free-reachable | – | **R** (power; stack leg only) |
| 34 | AF C-2-02 pre-EIA drift with API | negative-evidence row (pre-announcement drift post-2014) | API headline history is paid, so conditioning is not reproducible | 12.5 bp vs 4 = 3× if alive | conditioning variable unavailable; unconditional variant is in negative evidence (N) | exit 10:27 ✓ | blocked-paid $7 + paid API data | – | **R** (data gap + negative evidence) |
| 35 | IG C-12-26 expiry settlement auctions | bare-OPEX negative row (day level), H0012/17 | – | DAX 3.5–8.5 vs 1.6–2 ✓; 16/yr | 16 events/yr: power ≈ 0 (N) | – | DAX free-reachable; ES licence-hold | – | **L** (stack only) |
| 36 | pre-sweep P-C10 late breakouts after whipsaw | H0020/D4-04 adjacent | – | R-based, cost small | practitioner in-sample from a large search; derivative on CFDs 2015–26, leaving ≈ 4 y (2010-11..2014) (N) | – | free-reachable | ≈ 4 / 1.84 | **L** (low) |
| 37 | AF C-2-05 Crop Progress → 20:00 reopen | H0012/17 other asset | report 16:00, entry 20:00 ✓ | unknown vs ZC 12 / ZS 5 bp | the reopen gap absorbs the information (N) | thin overnight books | blocked-paid $2 (1h) | 12 | **L** |
| 38 | AS C-3-01 overnight drift 02:00–03:00 | none (H0009 leg) | – | ≈ 0 since 2021 vs 2.5 bp FAIL | authors themselves report decay to ≈ 0 (N) | – | blocked-paid $20 | – | **R** (documented decay; economics) |
| 39 | AS C-3-04 Nikkei night → day reversal | H0012/17 logic | ✓ | threshold 4.4 bp, magnitude unknown | provisional FAIL until measured (N) | NKD permitted list varies by firm | blocked-paid $1 (1h) | 13 | **L** (merge with #40) |
| 40 | AS C-5-03 S&P → Tokyo first 30 min | H0012/17 logic | ✓ | unknown vs 4.4 bp | same mechanism as #39 (N) | – | blocked-paid (NKD shared) | 13 | **L** (merged into #39) |

Tally: **B1 3 mechanisms / 6 counted variants** (#3, #7, #27); **L 21**; **R 16** (#8, 9, 13, 14, 18, 19, 20, 21, 22, 24, 25, 26, 29, 33, 34, 38).

## 3. BATCH 1 (proposed; the Director registers and commits; none is registered here)

All batch-1 rows use free-now data, have a fixed sign, use a single configuration (no IS grid) and have guard 0.7. No Red Team objection to them is unanswerable before registration.

| id | name | family (counts after) | firm structure | data | OOS (decision) | dry-run |
|---|---|---|---|---|---|---|
| Q-0001 | month-end WM/R fix, signed equity-hedge pre-fix leg, EURUSD/GBPUSD/AUDUSD | fx-month-end-equity-hedge (1) | ftmo-intraday-cfd | HistData ×3 + daily_assets | 2015-03-02..2024-12-31 (9.8 y) | ok |
| Q-0002 | same, CME 6E/6B/6A venue twin | fx-month-end-equity-hedge (2) | intraday-futures | same | same | ok |
| Q-0003 | FOMC-day AUD premium, long AUDUSD 00:05 CE(S)T → 15:58 ET | fx-fomc-day-premium (1) | ftmo-intraday-cfd | HistData AUDUSD + cal_fomc | 2014-01-01..2024-12-31 (11 y) | ok |
| Q-0004 | same, CME 6A 18:05 ET → 15:58 ET venue twin | fx-fomc-day-premium (2) | overnight-session-futures | same | same | ok |
| Q-0005 | energy two-day-fall dip buy, CL/CO/HO → USOIL/UKOIL/HEATOIL | commodity-dip-swing (1) | ftmo-swing | daily_futures_1984_2016 | 1990-01-02..2007-12-31 (18 y, derivative rule) | ok |
| Q-0006 | gold two-day-fall dip buy, GC → XAUUSD | commodity-dip-swing (2) | ftmo-swing | daily_futures_1984_2016 | 1990-01-02..2007-12-31 (18 y) | ok |

- Files: `research/prereg/Q-0001.json` … `Q-0006.json`. Each passed `python3 quant-edge/tools/register.py <file> --dry-run`, which printed "ok … would be appended (count 1)" for all six.
- Six counts. Running N would go from 281 to 287, inside the 150 budget; the bar does not change.
- Balance:
  - FTMO intraday CFD: 2 (Q-0001, Q-0003).
  - Futures firms: 2 (Q-0002 intraday, Q-0004 overnight session).
  - FTMO Swing: 2 (Q-0005, Q-0006).
  - That is the most free data allows. There is no free intraday data for CME index, energy or rates futures, so futures-firm rows can only use FX spot as a proxy for CME FX futures.
- **Venue twins** (Q-0002, Q-0004) use the same data and signal as their CFD sibling. The Referee must read each pair as one hypothesis with two cost models. A pass of only one is a cost result, not an edge result.
- **Why only 6, not 20.** Every other free-now top-40 row failed for one of three reasons:
  - the derivative rule leaves a window under 5 years (#8, #9, unsigned #3);
  - the economics fail (daily #3);
  - the data is free but not yet ingested (#6, #11, #30, #32, #35, #36).
- **Batch 1b (free, after a Department C ingest, about 1 day).** These need no Databento. Ingest HistData HKXHKD, ETXEUR, GRXEUR, SPXUSD/NSXUSD/JPXJPY, XAUUSD, BCOUSD and the inherited SPXUSD 2010–18, then register:
  - #30 HSI after-hours reversal;
  - #1 CO-OC on index CFDs (the FTMO version of the only medium row);
  - #11 prereg_orb30 D1;
  - #6 ECB tone.
- **Hold-out data still to land.** HistData FX 2025–2026 (free). Daily CL/BZ/HO/GC 2025–2026 for Q-0005/Q-0006: Databento 1d ≈ $0.20 (blocked-paid), or EIA/LBMA free when reachable.

## 4. Blocked-paid list (Databento unconfirmed; cost = plan estimate in candidates.md)

| priority | row | purchase | est. cost |
|---|---|---|---|
| 1 | AS C-4-01 CO-OC reversal (medium) | ES, NQ, YM, EMD, NKD ohlcv-1h 2010-06..2024 | ≈ $5 |
| 2 | AF C-2-01 NG storage day | NG ohlcv-1m RTH | ≈ $7 |
| 3 | IG C-12-04 margin hikes | GC, SI, CL, NG 1m RTH | ≈ $28 (shares NG/CL with 2, 22, 34) |
| 4 | AF C-1-01 Treasury strike (UB, variant B) | ZN + UB 1h | ≈ $2 (→ $40 for 1m) |
| 5 | AS C-4-07 hedging-overshoot | ES, NQ, ZN, GC, SI, NG 1m RTH | ≈ $40 (shared) |
| 6 | SC C-8-05 energy carry | CL, BZ, NG, HO 1d front + 2nd month + definitions | ≈ $0.20 |
| 7 | IG C-12-06 / C-12-24 / C-1-09 ES legs | ES 1m RTH (licence-hold copy only cross-checks) | ≈ $7 (+ RTY $7) |
| 8 | AS C-3-03, C-4-06, C-2-07 gold rows | GC 1h ($1) → 1m full session | $1 → $20 |
| 9 | AS C-3-04 / C-5-03 Nikkei | NKD 1h → 1m | $1 → $20 |
| 10 | AF C-2-05 Crop Progress | ZC, ZS 1h | ≈ $2 |
| – | hold-out for Q-0005/Q-0006 | CL, BZ, HO, GC 1d 2025–2026 | ≈ $0.20 |

A plan of priorities 1–6 plus the hold-out costs ≈ $82, under the $94 ceiling. Priority 7 brings it to ≈ $89. Gold 1m and NKD 1m do not fit without dropping priority 5.

## 5. Honest base rate

- **Under the null** (all 6 batch-1 variants have zero edge): per-variant false-pass probability ≤ 0.05/430 = 1.2e-4 on criterion 4, before criteria 3/7 and the hold-out. Expected false passes ≈ 0.0007. P(any) < 0.1%. With the 40-row slate (≈ 30 counts if all L rows were run) it is still < 0.5%.
- **Under a realistic prior**, per row:
  - P(true edge exists) ≈ 0.10 for event sleeves with peer-reviewed evidence (Q-0001/2, Q-0003/4) and ≈ 0.05 for the blog-only dip buy (Q-0005/6).
  - If the edge exists, its true Sharpe at our costs is what the haircut evidence implies: ≈ 0.8 (fix leg), ≈ 0.3 (FOMC AUD), ≈ 0.2–0.4 (dip buys). Joint gate power there is ≈ 0.15, 0.02 and 0.05–0.10.
  - If the edge were as large as the program needs (Sharpe 1.5), power would be 0.70 (9.8–11 y, joint) to ≈ 0.95 (18 y).
- **Expected passes in batch 1** ≈ 0.1×0.15 + 0.1×0.02 + 2×(0.05×0.08) ≈ **0.03 independent hypotheses** (twins counted once). P(at least one pass) ≈ 3%. If every edge were at Sharpe 1.5: ≈ 0.1×0.7 + 0.1×0.7 + 2×0.05×0.95 ≈ 0.24.
- **Whole top 40**, if all L rows are eventually tested: expected passes ≈ 0.2–0.4, carried mostly by AS C-4-01 (medium; P(edge) ≈ 0.2, joint power ≈ 0.5 at the published-after-haircut Sharpe). A program outcome of "no edge found" (N1) is the modal result. Batch 1 does not move that; it buys cheap, honest evidence on three stack legs while the Databento trigger is unresolved.
- **The single strongest Red Team objection overall** is §1, the economics-versus-power squeeze. Event sleeves fail per-event Sharpe × √n ≥ 3.68. Daily legs fail gross ≥ 3× round trip. The only top-40 row inside the window (AS C-4-01) is blocked-paid at $5. It should be the first purchase the moment the 72-hour trigger clears.

## 6. Notes for the Director and Referee

- The brief for AF C-1-05 has the Tokyo-fix clock reversed: 09:55 JST = 00:55 UTC = 19:55 EST / 20:55 EDT. Any future 6J row must compute the fix in UTC.
- Q-0001/Q-0002 use GLSTOCK − USLCAP as the foreign-minus-US signal. GLSTOCK contains US equity, so the proxy is diluted but has the right sign. Its column semantics must be confirmed by Data QA before the run (`~/quant-edge-inherited/pr4/skills/prop-fleet/data/README.md` names the columns but not the indices).
- HistData is bid-only and has no spread. Every FX row therefore charges the full per-side floor on the bid-to-bid return. Rollover-hour spreads (17:00–18:05 ET) are avoided by construction: entries are at 00:05 CE(S)T, 18:05 ET or 10:00 London.
- The FTMO funded-account news clause is assumed to allow holding through a release when no order is placed within ±2 minutes. The Rules Keeper matrix must confirm this before Q-0003 runs.
