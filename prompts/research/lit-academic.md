# Academic literature sweep - candidate edges for an intraday futures / FTMO-Swing research program

_Date: 2026-11-03. Lane: academic. Companion file: lit-academic.json (same content, structured)._

## Summary

Academic sweep (Nov 2026) of 11 families compatible with intraday futures prop firms and FTMO Swing. 36 candidates catalogued; 8 judged worth pre-registered tests, led by (1) the ES overnight drift 02:00-03:00 ET (RFS 2023; 1.48 bps/day gross, mechanism-based, persisted to 2020; net viability hinges on today's lower relative tick cost and conditioning on prior-day selloffs), (2) month-end Treasury index-extension buying traded intraday into the 4pm strike in ZN/ZB (Hartley-Schwarz Sharpe~1 in cash; NY Fed shows 20% of month-end volume in 10 minutes around 4pm), (3) USD appreciation into the WMR 4pm London fix with month-end equity-hedging amplification in 6E/6B/6A (Krohn-Mueller-Whelan JF 2024; Melvin-Prins), (4) Tokyo 9:55 gotobi fix in 6J, (5) EIA crude/natgas and (6) WASDE post-release continuation, (7) option-expiration pinning in ES extended to the 0DTE era, and (8) dealer-gamma regime switching between intraday mean reversion and momentum. Negative/closed-by-evidence: FX intraday momentum, Goldman-roll front-running, pre-announcement drift (procedure changes), OPEX/day-of-week/crypto weekday effects, 1-min cross-market lead-lag and LOB deep learning (data/latency). Decay literature implies ~50% post-publication haircut (more in US liquid markets) and abrupt death when institutions change; a single strategy therefore needs post-cost OOS Sharpe >=3 or a portfolio of >=5 independent sleeves to deliver net 1.5. Most candidates are honestly LOW plausibility for net Sharpe 1.5 on their own; the realistic path is a portfolio of mechanism-anchored, time-stamped flow trades.

## Top 8 (pre-registered test priority)

- **C27 - Overnight drift: long ES during the 02:00-03:00 ET European-open hour, conditional on prior-day US order imbalance (Boyarchenko-Larsen-Whelan)** - plausibility: medium (best-documented, mechanism-based, top-journal, persisted through 2020; net Sharpe realistically 0.3-0.8 unconditional, higher conditional). 1998-2020: +1.48 bps/day (3.7% annualized) in 02:00-03:00; positive in 20/23 years, significant in 17; only hour significant in all subsamples; strategy long 02:00-03:00 Sharpe 1.1 gross, -0.5 after full bid-ask; 01:30-03:30 Sharpe 1.3 gross / 0.3 net; conditi...
- **C09 - Month-end Treasury index-extension buying measured intraday (last trading day, 14:00-16:05 ET) in ZN/ZB/UB** - plausibility: medium (strong mechanism, few events; good portfolio sleeve). Hartley-Schwarz 1990-2018: coupon Treasuries earn ~20-25 bps/month at 10y concentrated in last few days; last-days-only long strategy Sharpe ~1 across maturities after costs; 2015-2018 smaller but significant; spillover to futures/swaps. NY Fed: month-end 3:45...
- **C06 - USD appreciation into the WMR 4pm London fix and reversal after (Krohn-Mueller-Whelan 'W' pattern)** - plausibility: medium for pre-fix drift (esp. month-end), low for post-fix fade. KMW: USD appreciates on average in hours before fixes and depreciates after (W-shaped 24h), inter-dealer data show unconditional USD demand at fixes; Sharpe not retrieved. Marsh et al. (2012-2016 spot + CME GBP/AUD/NZD futures): small 1-minute reversal after t...
- **C07 - Tokyo 9:55 fix USD/JPY pre-fix drift (gotobi days) - Ito-Yamada** - plausibility: low-medium (few pips, well-known). Ito-Yamada: price spikes at Tokyo fix more frequent than London; order flow biased to USD creates predictable pattern; after 2008 fixing still above median window price; calendar (gotobi) effects significant. No Sharpe reported. Retail 'gotobi' strategy widely...
- **C14 - EIA Weekly Petroleum Status Report (Wed 10:30 ET): post-release continuation in CL/RB/HO** - plausibility: low-medium. Immediate negative price/positive volatility response to inventory surprises; effects last ~25 min (Geman-Li) vs no reversion (Linn); API Tuesday 16:30 report also moves prices. No net Sharpe published....
- **C16 - USDA WASDE / Crop Production (12:00 ET monthly): post-release drift in ZC/ZS/ZW** - plausibility: low-medium (36 events/yr). Anderson et al.: significant correctly-signed 30-min reactions, soybean reaction grows past 30 min (drift). No Sharpe/cost figures. 2012 switch to in-session release makes 1-min data informative....
- **C26 - Option-expiration pinning / anti-cross-pinning in S&P futures (Golez-Jackwerth) extended to the 0DTE era** - plausibility: low-medium. 1992-2009 serial expirations: statistically significant pinning in futures; anti-cross-pinning before SPX expirations; no pinning in cash basket. No strategy Sharpe. 0DTE era untested....
- **C23 - Dealer-gamma regime switch (0DTE-era): mean-reversion on positive-net-gamma days, momentum on negative-net-gamma days at 5-30 min horizons** - plausibility: low-medium. Adams et al.: 1 bp higher hedging need -> 4 bp lower RV; higher net gamma predicts stronger E-mini order-flow reversals and negative HF momentum over next 10 min, fading within an hour; authors suggest intraday hedging of positive-gamma portfolio profitable if...

## Candidates by category

### 1-intraday-momentum

#### C01 - Market intraday momentum in non-US equity index futures/CFDs (Nikkei 225, DAX, FTSE 100, HSI, KOSPI)

- **Mechanism:** Return from open (or prior close) to T-30min predicts last-30-min return; driven by late-day hedging of short-gamma option books and leveraged-ETF rebalancing plus late informed trading (Baltussen et al.). Non-US indices have their own closing-hour hedging flows.
- **References:** Baltussen, Da, Lammers, Martens (2021), *Hedging demand and market intraday momentum*, Journal of Financial Economics 142:377-403, https://academicweb.nd.edu/~zda/intramom.pdf; Limkriangkrai, Chai, Zheng (2023), *Market intraday momentum: APAC evidence*, Pacific-Basin Finance Journal 80:102086, https://researchmgt.monash.edu/ws/files/519509174/494419119_oa.pdf; Ho, Lu, et al. (2021), *Intraday Time Series Momentum: Global Evidence and Links to Market Characteristics (16 developed markets)*, SSRN working paper (cited by Limkriangkrai et al.), https://papers.ssrn.com/author=3577769; Gao, Han, Li, Zhou (2018), *Market intraday momentum*, Journal of Financial Economics 129:394-414, https://profiles.wustl.edu/en/publications/market-intraday-momentum/
- **Instruments:** CME NKD/NIY (Nikkei), FTMO CFDs DE40/UK100/JP225/HK50; KOSPI only via FTMO if offered  
- **Holding period:** Last 30 minutes of each local cash session  
- **Data needed:** 1-min bars of index futures/CFDs in local session time; exchange holiday calendar; DST mapping
- **Reported performance:** Baltussen: 60+ futures 1974-2020, pooled equity-index rROD slope significant in both 1974-99 and 2000-20 subsamples (t>3), 'high and attractive annualized Sharpe' (gross, number per index not extracted). Limkriangkrai 2023 (ETFs to Apr-2021): effect in Japan (Nikko 225 ETF, 2001-2021) and China; weak Korea; none HK/Singapore; Japan persisted during COVID. Ho et al.: significant in 12/16 developed markets.
- **Cost sensitivity:** High: one round trip per day; gross last-30-min edge is a few bps; Baltussen state they ignore costs but S&P futures net Sharpe positive at 1-tick cost. CFD spreads (DE40 ~1-2 pts) likely consume most of the edge.  
- **Firm compatibility:** Futures firms: only NKD/NIY (thin). FTMO: index CFDs intraday OK (Standard: avoid news windows).
- **Overlap with closed families:** SAME FAMILY as closed Gao-Han-Li-Zhou last-half-hour momentum (closed on ES/NQ); new only in instruments. Flag: requires materially new OOS evidence (post-2019) per market before any work.
- **Plausibility of net Sharpe >= 1.5:** low (medium only as one sleeve of a multi-index portfolio)  
- **Why not already tested:** Prior work tested ES/NQ only; APAC/European closes were not examined; Nikkei result (Japan persists) is the strongest non-US evidence.
- **Pre-registerable test:** Per index: signal = sign(r[open->T-30m]) (also sign(r[prev close->T-30m])); position in last 30 min; costs = spread+commission per side. Params from Baltussen (rROD, 30-min). In-sample 2010-2018, OOS 2019-2026, pooled t-stat across indices; promote only if pooled post-cost t>3 and each-index sign agreement.  
- **Evidence quality:** JFE 2021 + PBFJ 2023 replication; verified from PDF text

#### C02 - Government-bond-futures intraday momentum into the 3pm ET cash/futures settlement (ZN/ZB/ZF/UB)

- **Mechanism:** Same hedging/late-informed-trading mechanism in rates; index-tracking funds and dealers rebalance into the 3pm (now 4pm) index strike; MBS/option hedgers trade with the day's move late in the session.
- **References:** Baltussen, Da, Lammers, Martens (2021), *Hedging demand and market intraday momentum*, JFE 142, https://academicweb.nd.edu/~zda/intramom.pdf; Zhang, Wang, Li (2021), *Bond intraday momentum*, Journal of Behavioral and Experimental Finance 31, https://ideas.repec.org (abstract not retrieved); Dyer, Fleming, Shachar (2026), *Treasury Trading at the Close*, Liberty Street Economics (NY Fed), https://libertystreeteconomics.newyorkfed.org/2026/09/treasury-trading-at-the-close/
- **Instruments:** ZN, ZF, ZB, UB (CBOT); micro 10Y/30Y yield futures  
- **Holding period:** Last 30 min before 15:00 ET (test also 16:00 ET window post-Jan-2021 strike change)  
- **Data needed:** 1-min ZN/ZB/ZF 2010-2026; definition of 'close' (15:00 pit-settlement vs 16:00 index strike)
- **Reported performance:** Baltussen pooled bond futures: rROD slope 1.89*** (1974-99) and 1.60*** (2000-20), R2 small; strategy Sharpe table shows bonds positive (gross). Zhang-Wang-Li 2021: abstract not found. NY Fed: 3.4%-3.5% of daily cash volume in the 10 minutes around the strike; month-end 12-20%.
- **Cost sensitivity:** Very high: ZN daily vol ~30-40 bps so last-30-min move ~5-8 bps vs 1 tick (1/64 = 1.6 bps) + commission each side.  
- **Firm compatibility:** Futures firms: yes (ZN/ZB allowed). FTMO: no Treasury futures CFDs (verify).
- **Overlap with closed families:** Same family as closed last-half-hour momentum but different asset class (allowed as 'materially different' only if bond-specific construction, e.g., window tied to index strike).
- **Plausibility of net Sharpe >= 1.5:** low  
- **Why not already tested:** Closed work covered equities only.
- **Pre-registerable test:** Signal sign(r[8:20->14:30]) traded 14:30-15:00 and 15:30-16:00; also condition on |rROD|>1 sigma. IS 2010-2018, OOS 2019-2026; split at Jan-14-2021 strike change.  
- **Evidence quality:** JFE pooled evidence; bond-specific paper unverified

#### C03 - Commodity-futures intraday momentum into settlement windows (CL 14:30 ET, GC 13:30 ET, NG 14:30 ET)

- **Mechanism:** Settlement-window hedging by ETF/ETN (USO, GLD creations), index rollers and option dealers trades with the day's direction; strongest when first-session volume/volatility is high.
- **References:** Jin, Kearney, Li, Yang (2020), *Intraday time-series momentum: Evidence from China*, Journal of Futures Markets 40(4):632-650, https://ideas.repec.org/a/wly/jfutmk/v40y2020i4p632-650.html; Baltussen, Da, Lammers, Martens (2021), *Hedging demand and market intraday momentum*, JFE 142, https://academicweb.nd.edu/~zda/intramom.pdf; Wen et al. (2021), *Intraday momentum in crude oil (EIA-day third-half-hour predicts last half-hour)*, cited in search; venue not verified, not found
- **Instruments:** CL, GC, NG, (SI, HG); micro MCL/MGC  
- **Holding period:** 30 min before settlement window  
- **Data needed:** 1-min bars; settlement-window times by product; EIA calendar
- **Reported performance:** Jin et al.: first-half-hour return predicts last-half-hour in copper, rebar, soybean, soy meal; strongest in high-volume/high-vol metal sessions; strategy beats always-long (no cost figures). Baltussen pooled commodities: rROD 1.57*** in 2000-2020 (weaker pre-2000).
- **Cost sensitivity:** High (CL tick $10 = ~1.5 bps at $65; GC tick $10 = ~0.4 bps).  
- **Firm compatibility:** Futures firms yes; FTMO XAUUSD/USOIL/NATGAS CFDs intraday yes.
- **Overlap with closed families:** Same family (last-half-hour momentum); new asset class and settlement-window construction.
- **Plausibility of net Sharpe >= 1.5:** low-medium (GC best cost ratio)  
- **Why not already tested:** Equity-only prior tests.
- **Pre-registerable test:** Per product: sign(r[pit open->T-30m]) traded into settlement; condition on EIA/WASDE day flags; IS 2012-2018, OOS 2019-2026; require net t>3 pooled.  
- **Evidence quality:** JFM 2020 (China) + JFE pooled

#### C04 - Overnight-return -> last-half-hour continuation in international index futures (Liu-Tse)

- **Mechanism:** Overnight information processed slowly by domestic institutions who trade late; opposite sign to overnight-gap FADE.
- **References:** Liu, Tse (2017), *Overnight returns of stock indexes: Evidence from ETFs and futures (12 international index futures)*, International Review of Economics & Finance (venue per search; verify), not found; Baltussen, Da, Lammers, Martens (2021), *Hedging demand and market intraday momentum (rONFH predictor)*, JFE 142, https://academicweb.nd.edu/~zda/intramom.pdf
- **Instruments:** ES, NQ, NKD, FTMO index CFDs  
- **Holding period:** Last 30 min  
- **Data needed:** 1-min bars incl. overnight session
- **Reported performance:** Liu-Tse: overnight return positively predicts last-half-hour return in S&P ETFs and 12 international index futures; first half-hour not predictive. Baltussen: rONFH significant but dominated by rROD.
- **Cost sensitivity:** High (same as C01)  
- **Firm compatibility:** Both firm types intraday
- **Overlap with closed families:** Adjacent to closed overnight-gap fade (opposite direction, different window) and closed last-half-hour family -> flag.
- **Plausibility of net Sharpe >= 1.5:** low  
- **Why not already tested:** Closed tests used first-half-hour or full-day predictors.
- **Pre-registerable test:** sign(r[prev 16:00 -> 9:30]) traded 15:30-16:00; OOS 2019-2026.  
- **Evidence quality:** abstract-level only

#### C05 - FX-futures intraday momentum (6E/6B/6J) - NEGATIVE EVIDENCE, recommend skip

- **Mechanism:** None robust: FX has no single close/settlement hedging wave (24h market).
- **References:** Elaut, Frommel, Lampaert (2018), *Intraday momentum in FX markets: Disentangling informed trading from liquidity provision*, Journal of Financial Markets 37:35-51, https://ideas.repec.org/a/eee/finmar/v37y2018icp35-51.html; Baltussen et al. (2021), *Hedging demand and market intraday momentum*, JFE 142, https://academicweb.nd.edu/~zda/intramom.pdf
- **Instruments:** 6E, 6B, 6J, 6A  
- **Holding period:** n/a  
- **Data needed:** n/a
- **Reported performance:** Baltussen pooled currency futures: rROD slope 0.37 (n.s.) in 2000-2020, 1.84 (n.s.) in 1974-99; Elaut et al. find the effect only in RUB/USD (illiquid).
- **Cost sensitivity:** n/a  
- **Firm compatibility:** n/a
- **Overlap with closed families:** Closed family; also closed 'intraday rules across 19 FX/CFD markets'.
- **Plausibility of net Sharpe >= 1.5:** very low  
- **Why not already tested:** It was, indirectly; include as a stop-sign.
- **Pre-registerable test:** Do not test.  
- **Evidence quality:** JFE pooled regression (verified)

### 10-machine-learning

#### C34 - Deep Momentum Networks / Momentum Transformer on futures (Lim-Zohren-Roberts; Wood et al.) adapted to intraday bars

- **Mechanism:** Sharpe-optimized LSTM/attention models learn position sizing from momentum/vol features across 88 futures; improvement over TSMOM mostly from volatility scaling and turnover control.
- **References:** Lim, Zohren, Roberts (2019), *Enhancing Time Series Momentum Strategies Using Deep Neural Networks*, Journal of Financial Data Science 1(4); arXiv 1904.04912, https://arxiv.org/abs/1904.04912; Wood, Giegerich, Roberts, Zohren (2022), *Trading with the Momentum Transformer: An Intelligent and Interpretable Architecture*, arXiv 2112.08534, https://arxiv.org/abs/2112.08534; Wood, Roberts, Zohren (2022), *Slow Momentum with Fast Reversion: A Trading Strategy Using Deep Learning and Changepoint Detection*, Journal of Financial Data Science; arXiv 2105.13727, https://arxiv.org/abs/2105.13727
- **Instruments:** Daily: 88 futures (not holdable at futures firms; FTMO Swing CFDs partially). Intraday adaptation: ES/NQ/CL/GC/6E 30-min bars  
- **Holding period:** Daily rebalance (paper); intraday variant forced flat at close  
- **Data needed:** Daily continuous futures (free: Nasdaq Data Link/Stooq) + 1-min bars aggregated
- **Reported performance:** DMN: >2x Sharpe of TSMOM before costs; advantage survives only up to 2-3 bps per-trade costs. Momentum Transformer: outperforms TSMOM/DMN after costs incl. 2020 (figures not retrieved).
- **Cost sensitivity:** Very high: 2-3 bps breakeven is at/below futures RT cost+slippage; CFD spreads worse.  
- **Firm compatibility:** FTMO Swing only for multi-day; intraday variant untested academically.
- **Overlap with closed families:** Closed: TSMOM/EWMAC trend on FX/CFD and multi-day trend on 54 futures. ML variant is a different construction but same signal family -> flag.
- **Plausibility of net Sharpe >= 1.5:** low  
- **Why not already tested:** Compute-heavy; intraday adaptation novel.
- **Pre-registerable test:** Train DMN on 30-min bars of 8 CME contracts 2010-2018 with forced close, walk-forward yearly 2019-2026, cost 1 tick+commission; promote only if net Sharpe>1 OOS and stable across years.  
- **Evidence quality:** JFDS 2019/2022; cost fragility documented

#### C35 - Universal order-book deep learning (DeepLOB / Sirignano-Cont / Lucchese et al. / Kolm et al.) - DATA-BLOCKED within budget

- **Mechanism:** Order-book state (depth imbalance, OFI) predicts mid-price moves seconds to minutes ahead, universally across assets; predictability is ubiquitous but tiny per event.
- **References:** Sirignano, Cont (2019), *Universal features of price formation in financial markets: perspectives from deep learning*, Quantitative Finance 19(9); arXiv 1803.06917, https://arxiv.org/abs/1803.06917; Lucchese, Pakkanen, Veraart (2024), *The short-term predictability of returns in order book markets: a deep learning perspective*, International Journal of Forecasting; arXiv 2211.13777, https://arxiv.org/abs/2211.13777; Kolm, Turiel, Westray (2023), *Deep order flow imbalance: Extracting alpha at multiple horizons from the limit order book*, Mathematical Finance 33(4); arXiv 2102.08811, https://arxiv.org/abs/2102.08811
- **Instruments:** ES/NQ (needs MBP-10 / MBO)  
- **Holding period:** seconds-minutes  
- **Data needed:** Databento GLBX.MDP3 mbp-10 (expensive; exceeds $125 for multi-year) - 1-min bars insufficient
- **Reported performance:** Predictability 'ubiquitous' at HF (Lucchese); Kolm: multi-horizon OFI alpha on Nasdaq stocks; none show net profits after costs for a retail-latency trader.
- **Cost sensitivity:** Extreme.  
- **Firm compatibility:** Latency/cost incompatible with retail prop execution.
- **Overlap with closed families:** Not closed.
- **Plausibility of net Sharpe >= 1.5:** very low for this program  
- **Why not already tested:** Data/latency.
- **Pre-registerable test:** Skip unless a 1-week mbp-10 sample is used only to calibrate BVC proxies (C38).  
- **Evidence quality:** strong HF literature; not actionable

#### C36 - Sparse LASSO cross-sectional 1-minute lead-lag across ~25 CME futures (Chinco-Clark-Joseph-Ye analogue)

- **Mechanism:** Short-lived, sparse, news-related predictors among lagged returns of the whole cross-section improve 1-minute-ahead forecasts OOS (NYSE stocks); futures analogue: lagged returns of all CME contracts predict each contract.
- **References:** Chinco, Clark-Joseph, Ye (2019), *Sparse Signals in the Cross-Section of Returns*, Journal of Finance 74(1):449-492; NBER w23933, https://www.nber.org/papers/w23933
- **Instruments:** ES, NQ, RTY, YM, ZN, ZB, ZF, 6E, 6J, 6B, CL, NG, GC, SI, HG, ZC, ZS, ZW, MBT  
- **Holding period:** 1-5 minutes  
- **Data needed:** Synchronized 1-min bars for ~20 contracts 2018-2026 (ohlcv-1m, cheap)
- **Reported performance:** Stocks: LASSO improves OOS fit and forecast-implied Sharpe (figures not retrieved); predictors are sparse (<30) and unexpected.
- **Cost sensitivity:** Extreme at 1-min.  
- **Firm compatibility:** Both intraday.
- **Overlap with closed families:** Not closed.
- **Plausibility of net Sharpe >= 1.5:** very low (small cross-section, HFT-arbitraged)  
- **Why not already tested:** Cheap diagnostic.
- **Pre-registerable test:** Rolling 30-day LASSO on 1-min lagged returns (lags 1-3) of all contracts -> next-minute return; OOS R2 and net PnL at 1 tick; 2019-2026.  
- **Evidence quality:** JF 2019 (stocks)

### 11-order-flow-proxies

#### C38 - Bulk-volume-classified order imbalance from 1-min bars as conditioner (closing RSV -> overnight drift; intraday imbalance -> reversal/continuation)

- **Mechanism:** Signed order flow moves prices (inventory and information); BVC assigns bar volume to buys/sells via standardized price change, approximating aggressor side without tick data; end-of-day imbalance predicts overnight reversal (BLW) and intraday imbalance predicts short-horizon reversal (Chordia et al. daily; OFI contemporaneous).
- **References:** Easley, Lopez de Prado, O'Hara (2016), *Discerning information from trade data*, Journal of Financial Economics 120(2):269-285 (BVC), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1989555; Easley, Lopez de Prado, O'Hara (2012), *Flow Toxicity and Liquidity in a High-frequency World*, Review of Financial Studies 25(5):1457-1493 (VPIN), not fetched; Chordia, Roll, Subrahmanyam (2002), *Order imbalance, liquidity, and market returns*, Journal of Financial Economics 65:111-130, not fetched; Cont, Kukanov, Stoikov (2014), *The Price Impact of Order Book Events*, Journal of Financial Econometrics 12(1):47-88 (OFI), https://arxiv.org/abs/1011.6402; Boyarchenko, Larsen, Whelan (2023), *The Overnight Drift (RSV conditioner)*, RFS, https://www.newyorkfed.org/research/staff_reports/sr917
- **Instruments:** ES, NQ, ZN, CL, GC  
- **Holding period:** Feature, not a holding period  
- **Data needed:** 1-min OHLCV (free with bars); optional Databento tbbo/trades for ES 1-2 years (~tens of dollars) to validate BVC accuracy
- **Reported performance:** BVC classifies aggressor side with ~85-90% accuracy in futures (ELO 2016); Chordia et al.: lagged daily imbalance predicts returns weakly; BLW: negative close RSV -> stronger 02:00-03:00 return. No standalone intraday Sharpe.
- **Cost sensitivity:** n/a (feature).  
- **Firm compatibility:** n/a
- **Overlap with closed families:** Not closed.
- **Plausibility of net Sharpe >= 1.5:** low standalone; medium as conditioner for C27/C24/C21  
- **Why not already tested:** Prior tests used price-only rules.
- **Pre-registerable test:** Compute BVC imbalance per 1-min bar; validate against tbbo for 3 months; build RSV(15:15-16:15) and test as conditioner in C27; test lagged 5-min imbalance -> next 5-min return (expect reversal) 2019-2026.  
- **Evidence quality:** JFE 2016 method; application untested

### 2-fx-fixes

#### C06 - USD appreciation into the WMR 4pm London fix and reversal after (Krohn-Mueller-Whelan 'W' pattern)

- **Mechanism:** Unconditional USD demand at fixings (benchmark-tracking funds, custodians, corporates) executed by capital-constrained dealers who pre-hedge; prices rise into the fix and partially revert after. Month-end amplified by equity-hedging flows (Melvin-Prins).
- **References:** Krohn, Mueller, Whelan (2024), *Foreign Exchange Fixings and Returns Around the Clock*, Journal of Finance 79(1); Bank of Canada SWP 2021-48, https://www.bankofcanada.ca/2021/10/staff-working-paper-2021-48/; Evans (2018), *Forex Trading and the WMR Fix*, Journal of Banking and Finance 87, https://mpra.ub.uni-muenchen.de/81583/; Marsh, Panagiotou, Payne (2017), *The WMR Fix and its Impact on Currency Markets (spot + CME futures)*, Cass working paper, https://www.norges-bank.no/contentassets/619c8b75e1ed4ba691e8ad6a006855e6/39-panagiotou---the-wmr-fix-and-its-impact-on-currency-markets-.pdf; Evans, O'Neill, Rime, Saakvitne (2018), *Fixing the Fix? Assessing the Effectiveness of the 4pm Fix*, FCA Occasional Paper 46, https://www.fca.org.uk/publication/occasional-papers/occasional-paper-46.pdf; Melvin, Prins (2015), *Equity hedging and exchange rates at the London 4pm fix*, Journal of Financial Markets 22:50-72, https://ideas.repec.org/a/eee/finmar/v22y2015icp50-72.html
- **Instruments:** 6E, 6B, 6J, 6A, 6C, 6S (CME) and FTMO FX CFDs  
- **Holding period:** Pre-fix: ~2-4 hours ending 15:59 London; post-fix reversal: 1-15 minutes after 16:00  
- **Data needed:** 1-min FX futures with London-time alignment (BST/GMT), month-end calendar; MSCI country-index monthly returns for Melvin-Prins hedging leg
- **Reported performance:** KMW: USD appreciates on average in hours before fixes and depreciates after (W-shaped 24h), inter-dealer data show unconditional USD demand at fixes; Sharpe not retrieved. Marsh et al. (2012-2016 spot + CME GBP/AUD/NZD futures): small 1-minute reversal after the fix; futures positions built pre-fix reverse over a longer window; reversals 'not economically large'. FCA OP46 (2012-2017): reversals weakened after Feb-2015 5-minute window; fix less representative at month-end. ITG (2014): 10-25 bps around month-end fix (cited in FCA).
- **Cost sensitivity:** Pre-fix multi-hour drift: one RT/day, 6E tick 0.5 pip (~0.5 bps) -> moderate. Post-fix 1-min reversal: likely consumed by spread.  
- **Firm compatibility:** Futures firms: yes (11:00-12:00 ET window is regular hours). FTMO: yes; Standard account avoid data releases at 10:00 ET.
- **Overlap with closed families:** Not closed (closed FX work was trend/carry and generic intraday rules, not fix-anchored).
- **Plausibility of net Sharpe >= 1.5:** medium for pre-fix drift (esp. month-end), low for post-fix fade  
- **Why not already tested:** Fix-anchored timing requires London-time alignment and month-end conditioning; not in prior generic FX rule sets.
- **Pre-registerable test:** Rule A: short 6E/6B/6A (long USD) from 13:00 to 15:58 London daily, flat at 15:59; Rule B: month-end only, direction = -sign(foreign equity index MTD return) per Melvin-Prins; Rule C: fade the 15:57:30-16:02:30 window move for 10 min. IS 2012-2018, OOS 2019-2026; split pre/post Feb-2015 window change; report bps/day and net Sharpe per pair.  
- **Evidence quality:** JF 2024 + JBF 2018 + FCA; magnitudes partly unretrieved

#### C07 - Tokyo 9:55 fix USD/JPY pre-fix drift (gotobi days) - Ito-Yamada

- **Mechanism:** Japanese importers/real-side customers buy USD for settlement at the fix; order flow biased toward USD before 9:55 JST, strongest on gotobi (5/10/15/20/25/EOM) settlement days; banks set fixing above market, consistent with predictable pre-fix USD/JPY rise.
- **References:** Ito, Yamada (2017), *Puzzles in the Tokyo Fixing in the Forex Market: Order Imbalances and Bank Pricing*, Journal of International Economics 109:214-234; NBER w22820, https://www.nber.org/papers/w22820; Krohn, Mueller, Whelan (2024), *Foreign Exchange Fixings and Returns Around the Clock*, Journal of Finance 79(1), https://www.bankofcanada.ca/2021/10/staff-working-paper-2021-48/
- **Instruments:** 6J (CME, trades 19:00-21:00 ET = 8:00-10:00 JST), FTMO USDJPY  
- **Holding period:** ~8:30-9:55 JST pre-fix; optional 9:55-10:30 fade  
- **Data needed:** 1-min 6J overnight session; Japanese holiday & gotobi calendar
- **Reported performance:** Ito-Yamada: price spikes at Tokyo fix more frequent than London; order flow biased to USD creates predictable pattern; after 2008 fixing still above median window price; calendar (gotobi) effects significant. No Sharpe reported. Retail 'gotobi' strategy widely known -> crowding risk.
- **Cost sensitivity:** Moderate: 6J tick 0.5 pip ($6.25); overnight-session spreads 1-2 ticks; drift a few pips.  
- **Firm compatibility:** Futures firms: allowed (overnight session, flat long before US close). FTMO: yes.
- **Overlap with closed families:** Not closed.
- **Plausibility of net Sharpe >= 1.5:** low-medium (few pips, well-known)  
- **Why not already tested:** Requires JST alignment and gotobi calendar; not in prior generic FX rules.
- **Pre-registerable test:** Short 6J (long USDJPY) 08:30-09:54 JST on gotobi days vs non-gotobi control; fade 09:55-10:25; IS 2010-2018, OOS 2019-2026; report pips/trade net of 1 tick.  
- **Evidence quality:** JIE 2017 abstract verified; magnitudes not retrieved

#### C08 - Around-the-clock USD time-of-day seasonality (Breedon-Ranaldo local-hours depreciation; Frankfurt/ECB fix leg of the W)

- **Mechanism:** Domestic currencies tend to depreciate during their own trading hours (local corporates/exporters sell FX received; dealers' inventory cycles); KMW attribute the full 24h W to fixes (Tokyo 9:55, Frankfurt 13:15/14:15 CET, London 16:00).
- **References:** Breedon, Ranaldo (2013), *Intraday Patterns in FX Returns and Order Flow*, Journal of Money, Credit and Banking 45(5):953-965, https://ideas.repec.org/a/wly/jmoncb/v45y2013i5p953-965.html; Ranaldo (2009), *Segmentation and time-of-day patterns in foreign exchange markets*, Journal of Banking and Finance 33:2199-2206, not fetched; Krohn, Mueller, Whelan (2024), *Foreign Exchange Fixings and Returns Around the Clock*, Journal of Finance 79(1), https://www.bankofcanada.ca/2021/10/staff-working-paper-2021-48/
- **Instruments:** 6E, 6J, 6B, 6A, 6C, 6S; FTMO FX  
- **Holding period:** Hour-bucket positions (1-4 hours)  
- **Data needed:** 1-min FX futures 2010-2026 with DST-correct local hours
- **Reported performance:** Breedon-Ranaldo: significant intraday seasonality in returns and order flow (magnitudes not retrieved). KMW: pattern robust via natural experiments (fix-time changes).
- **Cost sensitivity:** Moderate (1-2 RT/day).  
- **Firm compatibility:** Both, intraday.
- **Overlap with closed families:** Closed 'intraday rules across 19 FX/CFD markets' may have included hour-of-day; flag and check which hour-buckets were tested.
- **Plausibility of net Sharpe >= 1.5:** low-medium  
- **Why not already tested:** Prior rules were technical, not fix/hour-anchored.
- **Pre-registerable test:** Hour-of-day mean return table per pair (local-time buckets), IS 2010-2018 pick buckets with |t|>3, OOS 2019-2026 trade only those; Bonferroni over 24x6 buckets.  
- **Evidence quality:** JMCB 2013 + JF 2024

### 3-treasuries

#### C09 - Month-end Treasury index-extension buying measured intraday (last trading day, 14:00-16:05 ET) in ZN/ZB/UB

- **Mechanism:** Bond indices add new issues and extend duration only at month-end; passive funds, insurers (net buyers on rebalancing dates) and dealers buy into the 4pm (pre-2021: 3pm) index strike; cash volume share in the 10 minutes around the strike reaches 12-20% at month-end; Hartley-Schwarz find positive excess returns in the last few days with spillover to Treasury futures and swaps.
- **References:** Hartley, Schwarz (2019), *Predictable End-of-Month Treasury Returns*, Wharton/Rodney White WP 17-19, https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2019/12/17-19.Schwarz.pdf; Etula, Rinne, Suominen, Vaittinen (2020), *Dash for Cash: Monthly Market Impact of Institutional Liquidity Needs*, Review of Financial Studies 33(1):75-111, https://academic.oup.com/rfs/article/33/1/75/5494694; Dyer, Fleming, Shachar (2026), *Treasury Trading at the Close*, Liberty Street Economics, https://libertystreeteconomics.newyorkfed.org/2026/09/treasury-trading-at-the-close/
- **Instruments:** ZN, ZB, UB, ZF (also TN); FTMO: no  
- **Holding period:** Intraday on last trading day of month: 12:00/14:00 -> 16:05 ET (also T-1, T-2 sessions)  
- **Data needed:** 1-min ZN/ZB 2010-2026; month-end calendar incl. early closes; Bloomberg index extension estimates (optional, from sell-side previews)
- **Reported performance:** Hartley-Schwarz 1990-2018: coupon Treasuries earn ~20-25 bps/month at 10y concentrated in last few days; last-days-only long strategy Sharpe ~1 across maturities after costs; 2015-2018 smaller but significant; spillover to futures/swaps. NY Fed: month-end 3:45-4:15pm = >25% of day's volume (2025). Etula: negative pressure before month-end, recovery after.
- **Cost sensitivity:** Low-moderate: 12 trades/yr, expected move 5-15 bps vs ZN RT ~3 bps.  
- **Firm compatibility:** Futures firms: yes (intraday). FTMO: not available.
- **Overlap with closed families:** Closed turn-of-month S&P (McConnell-Xu) is equities; Treasury leg and intraday strike-window construction are new.
- **Plausibility of net Sharpe >= 1.5:** medium (strong mechanism, few events; good portfolio sleeve)  
- **Why not already tested:** Prior work was daily and equity-focused; the 2021 strike-time move created a clean natural experiment untested intraday.
- **Pre-registerable test:** Long ZN/ZB from 14:00 to 16:05 ET on last trading day (and from 15:30 to 16:02 tight window); control = same window other days; split pre/post Jan-14-2021 (3pm vs 4pm strike); IS 2010-2018, OOS 2019-2026; also daily (non-month-end) 15:45-16:00 drift as C13.  
- **Evidence quality:** WP (Sharpe ~1 after costs, cash) + RFS 2020 + NY Fed volume facts; verified from PDF

#### C10 - Treasury auction-cycle price pressure: intraday post-auction recovery (13:00-15:00 ET) and morning concession

- **Mechanism:** Dealers with limited risk-bearing capacity demand a concession before auctions; prices fall days before and recover shortly after (Lou-Yan-Zhang). Intraday: result release at 13:00 ET resolves uncertainty; post-result recovery and 'tail' surprises move ZN/ZB.
- **References:** Lou, Yan, Zhang (2013), *Anticipated and Repeated Shocks in Liquid Markets*, Review of Financial Studies 26(8):1891-1912, https://researchonline.lse.ac.uk/id/eprint/43120/; Fleming, Liu (2016), *Intraday pricing and liquidity effects of U.S. Treasury auctions*, NY Fed Staff Report (from memory - verify), not fetched
- **Instruments:** ZN (10y auctions), ZB/UB (30y), ZF (5y), ZT (2y)  
- **Holding period:** 13:01-15:00 ET on auction days; optional short 09:00-12:59  
- **Data needed:** 1-min bars; TreasuryDirect auction calendar and results (bid-to-cover, tail vs when-issued; free)
- **Reported performance:** Lou-Yan-Zhang (1980-2008): secondary prices decline in days before auctions and recover after; issuance cost 9-18 bps of auction size (>$0.5bn for notes in 2007). Intraday magnitudes not retrieved.
- **Cost sensitivity:** Moderate: ~8-10 note/bond auctions per month; expected intraday recovery a few bps vs ~3 bps RT.  
- **Firm compatibility:** Futures firms yes; FTMO no.
- **Overlap with closed families:** Not closed.
- **Plausibility of net Sharpe >= 1.5:** low-medium  
- **Why not already tested:** Needs auction calendar alignment; prior work daily.
- **Pre-registerable test:** Long contract matching auction tenor 13:01->15:00 on auction days (also 13:01->13:30); condition on tail sign; control non-auction days; IS 2010-2018, OOS 2019-2026.  
- **Evidence quality:** RFS 2013 (daily); intraday unverified

#### C11 - Post-FOMC drift in Treasury yields used as an intraday directional tilt in ZN/ZB (Brooks-Katz-Lustig)

- **Mechanism:** Retail bond-fund investors sell short/intermediate funds after salient target-rate increases; funds sell gradually, increasing supply arbitrageurs must absorb -> yields drift for ~50 days (10y: +1.7 bp same day vs +14 bp after 50 days per 10 bp surprise), partial reversal later.
- **References:** Brooks, Katz, Lustig (2019), *Post-FOMC Announcement Drift in U.S. Bond Markets*, NBER WP 25127 (rev. Apr 2019), https://www.nber.org/papers/w25127
- **Instruments:** ZN, ZB, ZF (intraday only at futures firms)  
- **Holding period:** Daily intraday sessions during days 1-30 after FOMC, direction = sign of Kuttner surprise  
- **Data needed:** 1-min ZN; fed funds futures (ZQ) 1-min for Kuttner surprise; FOMC calendar
- **Reported performance:** 1982-2008 baseline (157 meetings), robust to extension to 2015; effects mostly from positive surprises; bond fund returns 12.86 bps per bp surprise after 50 days. Drift per day ~0.25 bp of 10y yield -> ~2 bps price/day on ZN.
- **Cost sensitivity:** Very high for intraday-only capture (overnight component lost; ~2 bps/day gross vs ~3 bps RT).  
- **Firm compatibility:** Futures firms: intraday only (weak). FTMO: no bond CFDs (verify).
- **Overlap with closed families:** Adjacent to closed FOMC drift/continuation (ES/NQ); different asset -> flag partial.
- **Plausibility of net Sharpe >= 1.5:** low  
- **Why not already tested:** Closed tests were equity-only.
- **Pre-registerable test:** After FOMC with |Kuttner surprise|>2 bp, trade ZN 09:00-15:00 in drift direction for 20 sessions; compare to unconditional; OOS 2016-2026 (post-paper).  
- **Evidence quality:** NBER WP; verified numbers from PDF

#### C12 - Pre-announcement drift in ZN and ES in the 30 minutes before macro releases (Kurov et al.) - likely extinct

- **Mechanism:** Information leakage via pre-release/lock-up procedures (esp. three electronically pre-released series) plus proprietary-data forecasting; prices moved ~30 min early, ~40-50% of total adjustment (2008-2014).
- **References:** Kurov, Sancetta, Strasser, Halova Wolfe (2019), *Price Drift before U.S. Macroeconomic News: Private Information about Public Announcements?*, Journal of Financial and Quantitative Analysis 54(1):449-479; ECB WP 1901 (2016), https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1901.en.pdf
- **Instruments:** ZN, ES  
- **Holding period:** t-30min -> t (release) then exit at t+5  
- **Data needed:** 1-min ZN/ES; release timestamps; consensus surprises (paid; free scrape of Investing.com/ForexFactory as fallback)
- **Reported performance:** 2008-Mar 2014: 7-9 of 20 market-moving announcements show drift; ~$20m/yr estimated E-mini profits; 'strict release procedures make drift less likely'. Post-2014 lock-up reforms (ISM, Conference Board, 2020 lock-up closures) -> expected zero.
- **Cost sensitivity:** High (small moves, HFT competition).  
- **Firm compatibility:** Futures firms yes; FTMO Standard bans +/-2 min around news.
- **Overlap with closed families:** Closed macro-event family (CPI/NFP gap, event-day momentum); pre-release window is different but same family -> flag; include ONLY as a kill-test.
- **Plausibility of net Sharpe >= 1.5:** very low  
- **Why not already tested:** Pre-release window not tested; mechanism likely removed by procedure changes.
- **Pre-registerable test:** Momentum in t-30->t-1 window predicting t-1->t+5 for ISM, consumer confidence, existing home sales, GDP; 2015-2026 only; expect null.  
- **Evidence quality:** JFQA 2019; verified

#### C13 - Daily 3:45-4:00pm ET index-strike liquidity window drift in ZN/ZB (post-2021 Bloomberg strike move)

- **Mechanism:** Index-tracking funds execute at the 4pm strike every day (3.5% of volume in 10 minutes); if flows are net-directional (inflows into bond funds/ETFs), price pressure appears pre-strike and reverts after.
- **References:** Dyer, Fleming, Shachar (2026), *Treasury Trading at the Close*, Liberty Street Economics, https://libertystreeteconomics.newyorkfed.org/2026/09/treasury-trading-at-the-close/
- **Instruments:** ZN, ZB, UB  
- **Holding period:** 15:45-16:00 ET and 16:00-16:15 fade  
- **Data needed:** 1-min bars 2016-2026; daily bond-ETF flow data (free from issuers) as sign conditioner
- **Reported performance:** Volume facts only; no return evidence found.
- **Cost sensitivity:** Very high (tiny expected move).  
- **Firm compatibility:** Futures firms yes.
- **Overlap with closed families:** Not closed.
- **Plausibility of net Sharpe >= 1.5:** low  
- **Why not already tested:** New institutional feature (2021).
- **Pre-registerable test:** Mean 15:45-16:00 return pre/post 2021-01-14; condition on TLT/IEF prior-day flow sign; OOS 2023-2026.  
- **Evidence quality:** volume facts only (hypothesis)

#### C40 - Pre-announcement 'uncertainty premium' drift before FOMC/NFP/ISM/GDP (Hu-Pan-Wang-Zhu) in ZN, GC, 6E - CLOSED-ADJACENT

- **Mechanism:** Risk premium accrues in the hours before scheduled announcements as uncertainty peaks (VIX rises then collapses); documented for equities (ES) overnight/morning before releases.
- **References:** Hu, Pan, Wang, Zhu (2022), *Premium for heightened uncertainty: Explaining pre-announcement market returns*, Journal of Financial Economics 145(3) (from memory - verify), not fetched; Lucca, Moench (2015), *The Pre-FOMC Announcement Drift*, Journal of Finance 70(1), not fetched
- **Instruments:** ZN, GC, 6E (new instruments); ES closed  
- **Holding period:** t-24h/t-3h -> t-5min  
- **Data needed:** 1-min bars; release calendar
- **Reported performance:** ES: large pre-announcement returns 1994-2018 (Hu et al.); later samples weaker (Lucca-Moench drift faded post-2016 per follow-ups).
- **Cost sensitivity:** Moderate.  
- **Firm compatibility:** Futures firms yes (ZN/GC/6E).
- **Overlap with closed families:** CLOSED for ES/NQ (Lucca-Moench, CPI/NFP gap). Only non-equity instruments would be new.
- **Plausibility of net Sharpe >= 1.5:** very low  
- **Why not already tested:** Equity-only closure.
- **Pre-registerable test:** Pre-FOMC 09:30->13:55 ET returns in ZN/GC/6E 2016-2026; expect null.  
- **Evidence quality:** JFE 2022 (equities)

### 4-commodities

#### C14 - EIA Weekly Petroleum Status Report (Wed 10:30 ET): post-release continuation in CL/RB/HO

- **Mechanism:** Inventory surprise is a persistent fundamental shock; initial jump within 1-2 minutes, then continued adjustment/volatility for ~25 minutes (Geman-Li) or no reversion (Linn et al.); on EIA days the third half-hour return predicts the last half-hour (Wen et al.).
- **References:** Geman, Li (2018), *An analysis of intraday market response to crude oil inventory shocks*, Journal of Energy Markets 11(2), https://www.risk.net/journal-of-energy-markets/5728636/an-analysis-of-intraday-market-response-to-crude-oil-inventory-shocks; Halova (Wolfe), Kurov, Kucher (2014), *Noisy inventory announcements and energy prices*, Journal of Futures Markets 34(10) (from memory - verify), not fetched; Linn et al. (2017), *Crude oil inventory news and futures (Linn, Ederington, Fernando, Guernsey)*, EIA workshop slides, https://www.eia.gov/finance/markets/reports_presentations/2017/linn.pdf
- **Instruments:** CL, MCL, RB, HO; FTMO USOIL/UKOIL  
- **Holding period:** 10:32 -> 11:00/12:00 or -> 14:30 settlement  
- **Data needed:** 1-min CL 2012-2026; EIA release calendar (holiday shifts); EIA actuals (free); consensus (optional)
- **Reported performance:** Immediate negative price/positive volatility response to inventory surprises; effects last ~25 min (Geman-Li) vs no reversion (Linn); API Tuesday 16:30 report also moves prices. No net Sharpe published.
- **Cost sensitivity:** Moderate: CL tick $10 (~1.5 bps); EIA-day moves 1-3% so cost is small vs potential, but entry slippage at 10:30 is large (use 10:32 entry).  
- **Firm compatibility:** Futures firms yes (check news-trading rules); FTMO Standard: +/-2 min ban only.
- **Overlap with closed families:** Not closed (closed macro events were FOMC/CPI/NFP on ES/NQ).
- **Plausibility of net Sharpe >= 1.5:** low-medium  
- **Why not already tested:** Energy-specific event calendar not covered.
- **Pre-registerable test:** Direction = sign(r[10:30->10:32]) if |move|>0.5 sigma(1-min); enter 10:32, exit 11:30 / 14:25; also fade variant; ~500 events 2012-2026; IS 2012-2018, OOS 2019-2026; require net t>3.  
- **Evidence quality:** JEM 2018 + JFM 2014; magnitudes partial

#### C15 - EIA Natural Gas Storage Report (Thu 10:30 ET): post-release continuation/reversal in NG

- **Mechanism:** Weekly storage surprise vs consensus is the dominant NG fundamental news; reaction within one minute; follow-through/reversal depends on positioning (short covering).
- **References:** Gay, Simkins, Turac (2009), *Analyst forecasts and price discovery in futures markets: The case of natural gas storage*, Journal of Futures Markets 29(5) (from memory - verify), not fetched; Halova (Wolfe), Kurov, Kucher (2014), *Noisy inventory announcements and energy prices*, Journal of Futures Markets (from memory - verify), not fetched
- **Instruments:** NG, MNG; FTMO NATGAS  
- **Holding period:** 10:32 -> 11:30 / 14:30  
- **Data needed:** 1-min NG 2012-2026; EIA storage actuals (free); consensus (paid/scraped)
- **Reported performance:** Trade press and JFM papers document immediate, surprise-signed reaction; no post-cost drift study found (gap).
- **Cost sensitivity:** Moderate: NG tick $10 (~0.3%?? no: 0.001 x 10,000 = $10 at $3 = 0.03%); vol high.  
- **Firm compatibility:** Futures firms yes; FTMO yes.
- **Overlap with closed families:** Not closed.
- **Plausibility of net Sharpe >= 1.5:** low-medium  
- **Why not already tested:** Energy event calendar not covered.
- **Pre-registerable test:** Same as C14 with NG; ~700 events; also pre-report 10:00-10:29 vol-sizing rule.  
- **Evidence quality:** abstract/trade-press level

#### C16 - USDA WASDE / Crop Production (12:00 ET monthly): post-release drift in ZC/ZS/ZW

- **Mechanism:** Large public supply/demand revisions; adjustment is not instantaneous (Adjemian-Irwin); significant correctly-signed reactions at 30 minutes with soybeans continuing beyond 30 minutes (Anderson et al. 2024); daily limits and thin liquidity slow incorporation.
- **References:** Anderson, McKenzie, Noyes (2024), *Intraday price reaction of corn and soybean futures to WASDE (event study 2010-2021)*, NCCC-134 conference paper, https://ideas.repec.org/p/ags/nccc24/379003.html; Adjemian, Irwin (2018), *Price adjustment after USDA reports (2009-2014 intraday)*, American Journal of Agricultural Economics (verify), https://aaec.vt.edu/people/faculty/Isengildina_Olga/report/insights.html; Quantitative Brokers (2023), *WASDE: Its Significance and Impact on the Market Microstructure of Futures*, practitioner note, https://www.quantitativebrokers.com/market-updates/wasde-its-significance-and-impact-on-the-market-microstructure-of-futures
- **Instruments:** ZC, ZS, ZW (and MZC/MZS micros); FTMO: verify ag CFD availability  
- **Holding period:** 12:02 -> 13:15 (settle) or 14:20 close  
- **Data needed:** 1-min grains 2012-2026; USDA release calendar (free); report numbers (free) for surprise sign
- **Reported performance:** Anderson et al.: significant correctly-signed 30-min reactions, soybean reaction grows past 30 min (drift). No Sharpe/cost figures. 2012 switch to in-session release makes 1-min data informative.
- **Cost sensitivity:** Low-moderate: ZC tick $12.50 (~0.3%?? -> 0.25c/450c = 0.06%); WASDE-day moves 1-4%.  
- **Firm compatibility:** Futures firms yes (grains allowed at most). FTMO: likely not available.
- **Overlap with closed families:** Not closed.
- **Plausibility of net Sharpe >= 1.5:** low-medium (36 events/yr)  
- **Why not already tested:** Ag calendar never covered.
- **Pre-registerable test:** Direction = sign(r[12:00->12:03]) if |move|>1 sigma; hold to 13:10 and 14:15; IS 2012-2018, OOS 2019-2026; soybeans primary.  
- **Evidence quality:** conference paper 2024 + AJAE 2018

#### C17 - Goldman-roll (GSCI/BCOM 5th-9th business day) front-running - CLOSED BY LATER EVIDENCE

- **Mechanism:** Index funds sell front/buy deferred on a published schedule; arbitrageurs pre-position; profitability falls with arbitrage capital.
- **References:** Mou (2011), *Limits to Arbitrage and Commodity Index Investment: Front-Running the Goldman Roll*, SSRN 1716841, https://papers.ssrn.com/abstract=1716841; Dubois, Marechal (2019), *Does the Goldman roll still move prices? (poster)*, JP Morgan Center for Commodities, UC Denver, https://business.ucdenver.edu/jpmorgancenter/content/poster-loic-marechal
- **Instruments:** CL, NG, GC, ZC, ZS calendar spreads  
- **Holding period:** multi-day spread (not firm-compatible)  
- **Data needed:** n/a
- **Reported performance:** Mou: 2000-2010 large (3.6%/yr forgone, 48% Sharpe uplift). Dubois-Marechal: +115 bps pre-2004, -60 bps 2004-2010, no abnormal profit after costs.
- **Cost sensitivity:** n/a  
- **Firm compatibility:** Spreads/multi-day: incompatible with intraday firms.
- **Overlap with closed families:** Not in list; closing it here.
- **Plausibility of net Sharpe >= 1.5:** very low  
- **Why not already tested:** Known to have decayed.
- **Pre-registerable test:** Skip (optional: intraday-only roll-window spread drift as diagnostic).  
- **Evidence quality:** SSRN + poster

#### C18 - London gold/silver auctions (10:30/15:00 London) and COMEX settlement window (13:25-13:30 ET) price pressure in GC/SI

- **Mechanism:** Old PM fix leaked (volume +50% during fix; trades predicted the fix result). Since Mar-2015 ICE electronic auction publishes imbalance every 45s; benchmark-linked producer/ETF flows still execute at these times -> possible pre-auction drift/post-auction reversal; COMEX settlement attracts ETF/option-hedge flows.
- **References:** Caminschi, Heaney (2014), *Fixing a leaky fixing: Short-term market reactions to the London PM gold price fixing*, Journal of Futures Markets 34(1):70-91, https://www.news.uwa.edu.au/201410067021/research/uwa-research-finds-gold-and-silver-price-setting-open-exploitation; ICE (2015), *ICE Benchmark Administration launches LBMA Gold Price*, press release, https://ir.theice.com/press/news-details/2015/ICE-Benchmark-Administration-Launches-LBMA-Gold-Price-Transitions-Gold-Price-to-Transparent-Electronic-Auction-Process/default.aspx
- **Instruments:** GC, MGC, SI; FTMO XAUUSD/XAGUSD  
- **Holding period:** 10 minutes before/after auctions; 13:00-13:30 ET  
- **Data needed:** 1-min GC/SI 2015-2026 aligned to London time
- **Reported performance:** Pre-2015: leakage documented; post-2015: no study found (gap).
- **Cost sensitivity:** Moderate (GC tick ~0.4 bps).  
- **Firm compatibility:** Both, intraday (GC auctions at 05:30/10:00 ET).
- **Overlap with closed families:** Not closed.
- **Plausibility of net Sharpe >= 1.5:** low  
- **Why not already tested:** Niche timing; no post-2015 literature.
- **Pre-registerable test:** Mean returns in [-10,0] and [0,+10] min around 10:30/15:00 London and 13:25-13:30 ET vs control windows, 2015-2026; Bonferroni; trade only if |t|>3 IS (2015-2020) and OOS (2021-2026) confirms.  
- **Evidence quality:** JFM 2014 (pre-reform)

#### C19 - Energy seasonality tilts (NG injection/withdrawal, RBOB spring spec change, HO winter) as daily direction filter

- **Mechanism:** Predictable seasonal demand/supply and storage cycles create seasonal futures-curve shape; mostly priced into the curve, leaving weak directional seasonality in the front month.
- **References:** Back, Prokopczuk, Rudolf (2013), *Seasonality and the valuation of commodity options*, Journal of Banking and Finance 37:273-290 (from memory - verify), not fetched
- **Instruments:** NG, RB, HO; FTMO NATGAS/USOIL (Swing can hold)  
- **Holding period:** Multi-week (FTMO Swing) or intraday-only tilt (futures firms)  
- **Data needed:** Daily + 1-min bars
- **Reported performance:** Seasonality in volatility is strong; in returns weak/unstable (literature consensus).
- **Cost sensitivity:** Low (few trades) but edge small.  
- **Firm compatibility:** FTMO Swing for multi-week; futures firms only as intraday tilt.
- **Overlap with closed families:** Adjacent to closed TSMOM/trend families.
- **Plausibility of net Sharpe >= 1.5:** very low  
- **Why not already tested:** Low priority; include for completeness.
- **Pre-registerable test:** Calendar-month mean returns with bootstrap, 2000-2026; expect nothing robust.  
- **Evidence quality:** weak

### 5-intraday-reversal

#### C20 - Reversal after extreme 1-minute moves (non-news) in ES/NQ/RTY and in liquid single-name analogues

- **Mechanism:** Temporary price concessions to liquidity providers after order-flow shocks; 31% of an extreme 1-min down move reverses in the next minute in Nasdaq-100 stocks (largest/most liquid names most). Index futures: reversals after large opening moves documented 1987-2002 but killed by bid-ask costs (Grant-Wolf-Yu).
- **References:** Rif, Utz (2021), *Short-term stock price reversals after extreme downward price movements*, Journal of Empirical Finance / QREF (2021) - see PDF, https://opus.bibliothek.uni-augsburg.de/opus4/files/94257/1-s2.0-S1062976921000922-main.pdf; Grant, Wolf, Yu (2005), *Intraday price reversals in the US stock index futures market: A 15-year study*, Journal of Banking and Finance 29:1311-1327, https://researchwith.montclair.edu/en/publications/intraday-price-reversals-in-the-us-stock-index-futures-market-a-1/; Fung, Mok, Lam (2000), *Intraday price reversals for index futures in the US and Hong Kong*, Journal of Banking and Finance 24:1179-1201, https://scholars.hkbu.edu.hk/en/publications/intraday-price-reversals-for-index-futures-in-the-us-and-hong-kon/; Nagel (2012), *Evaporating Liquidity*, Review of Financial Studies 25(7):2005-2039, https://www.nber.org/papers/w17653
- **Instruments:** ES, NQ, RTY, YM (micros for sizing); CL, GC  
- **Holding period:** 1-15 minutes  
- **Data needed:** 1-min bars (ideally 1-s or tbbo for fill realism); news timestamps to exclude scheduled releases
- **Reported performance:** Rif-Utz: 31% next-minute reversal of extreme 1-min declines; profits sensitive to spread. Grant-Wolf-Yu: significance 'sharply reduced' after bid-ask proxy. Fung et al.: small profits after costs (HSI/S&P, 1990s).
- **Cost sensitivity:** Extreme: edge ~1 tick; requires passive fills.  
- **Firm compatibility:** Both intraday (watch daily loss limits in crash regimes).
- **Overlap with closed families:** Adjacent to closed overnight-gap fade (open-specific); mid-session version not closed.
- **Plausibility of net Sharpe >= 1.5:** low  
- **Why not already tested:** Prior work targeted the open only.
- **Pre-registerable test:** Trigger |r_1min| > 4 x rolling sigma outside +/-5 min of scheduled news; fade for 3/5/10 min with limit entry at trigger close; report gross bps vs 1-tick cost; condition on VIX>20 and on time-of-day; OOS 2021-2026.  
- **Evidence quality:** JBF + 2021 single-stock evidence

#### C21 - VIX/realized-vol-conditioned intraday mean reversion in ES/NQ (Nagel-style liquidity-provision premium)

- **Mechanism:** Returns to liquidity provision rise sharply when VIX is high (dealer capital constrained); short-horizon reversal is compensation for providing liquidity (US) though in China it reflects uninformed liquidity oversupply (Kang-Lin-Xiong).
- **References:** Nagel (2012), *Evaporating Liquidity*, RFS 25(7), https://www.nber.org/papers/w17653; Kang, Lin, Xiong (2022), *What drives intraday reversal? Illiquidity or liquidity oversupply?*, Journal of Economic Dynamics and Control 136:104313, https://ideas.repec.org/a/eee/dyncon/v136y2022ics0165188922000185.html
- **Instruments:** ES, NQ, RTY; FTMO US500/US100  
- **Holding period:** 5-60 minutes  
- **Data needed:** 1-min bars; VIX daily (free, CBOE); intraday RV from bars
- **Reported performance:** Nagel: daily-stock reversal returns strongly predictable by VIX (Sharpe high in high-VIX states). No futures-intraday figures.
- **Cost sensitivity:** High; only high-vol regimes offer >1-tick swings.  
- **Firm compatibility:** Both; daily-loss limits bind exactly in the regimes where it works -> size down.
- **Overlap with closed families:** Not closed (IBS daily reversal closed; this is intraday, vol-conditioned).
- **Plausibility of net Sharpe >= 1.5:** low-medium (regime-dependent)  
- **Why not already tested:** Conditioning on VIX regime not done at intraday horizon.
- **Pre-registerable test:** z-score of 5-min return vs 60-min rolling; fade when |z|>2 only if VIX>22 (or RV pct>80); exit at z=0 or 30 min; IS 2010-2018, OOS 2019-2026 split by regime.  
- **Evidence quality:** RFS 2012 mechanism; intraday untested

### 6-lead-lag

#### C22 - Cross-market lead-lag at 1-5 minute horizons (ES<->NQ<->RTY<->YM; ZN->ES; CL->6C; SI vs GC)

- **Mechanism:** Information arrives in the most liquid contract first; less liquid contracts adjust with a lag. Literature: lead-lag among S&P/FTSE/DAX futures lasts fractions of a second (85% directional accuracy sub-second, unexploitable after slippage); CFFEX calendar spreads lead by one tick.
- **References:** Huth, Abergel (2014), *High frequency lead/lag relationships - Empirical facts*, Journal of Empirical Finance 26:41-58, https://hal.archives-ouvertes.fr/hal-00645685; Hayashi, Koike (2018), *Wavelet-based methods for high-frequency lead-lag analysis*, SIAM J. Financial Math (arXiv 1612.01232), https://arxiv.org/pdf/1612.01232; Li, Chen, Liu (2025), *High-frequency lead-lag relationships in the Chinese stock index futures market*, arXiv 2501.03171, https://arxiv.org/abs/2501.03171; Ferraro, Rogoff, Rossi (2015), *Can oil prices forecast exchange rates?*, Journal of International Money and Finance 54 (from memory - verify), not fetched
- **Instruments:** RTY/M2K, YM/MYM, 6C, SI as laggards  
- **Holding period:** 1-5 minutes  
- **Data needed:** Synchronized 1-min bars across ~10 contracts (Databento ohlcv-1m, cheap)
- **Reported performance:** Sub-second effects only for liquid US/EU index futures; no evidence of exploitable 1-min lead-lag post-2010.
- **Cost sensitivity:** Extreme.  
- **Firm compatibility:** Both intraday.
- **Overlap with closed families:** Not closed.
- **Plausibility of net Sharpe >= 1.5:** very low (ES/NQ), low (RTY/YM/6C)  
- **Why not already tested:** Cheap diagnostic; almost certainly null.
- **Pre-registerable test:** Rolling VAR(1-3) on 1-min returns with strict OOS; Granger F-tests; trade laggard only if OOS R2>0.5% and net t>3; 2019-2026.  
- **Evidence quality:** HF literature consensus

#### C23 - Dealer-gamma regime switch (0DTE-era): mean-reversion on positive-net-gamma days, momentum on negative-net-gamma days at 5-30 min horizons

- **Mechanism:** Market makers long gamma trade against moves (dampening vol, causing order-flow reversals; effect fades after ~1 hour); short gamma forces trading with moves (intraday momentum). 0DTE expansion (2022+) raised hedging needs ~0.15pp and lowered RV ~60 bps annualized.
- **References:** Adams et al. (2025), *Do S&P500 Options Increase Market Volatility? Evidence from 0DTEs*, SSRN 5641974 (summarized by Quantpedia Feb-2026), https://quantpedia.com/do-sp500-0dtes-options-increase-market-volatility/; Dim, Eraker, Vilkov (2024), *0DTEs: Trading, Gamma Risk and Volatility Propagation*, SSRN 4692190, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4692190; Baltussen, Da, Lammers, Martens (2021), *Hedging demand and market intraday momentum*, JFE 142, https://academicweb.nd.edu/~zda/intramom.pdf
- **Instruments:** ES, MES, NQ; FTMO US500  
- **Holding period:** 5-60 minutes, all day (not only last 30 min)  
- **Data needed:** 1-min ES; daily SPX/SPY option open interest by strike (CBOE delayed, free) to build Ni-Pearson-Poteshman-White style net gamma; OPEX/0DTE calendar
- **Reported performance:** Adams et al.: 1 bp higher hedging need -> 4 bp lower RV; higher net gamma predicts stronger E-mini order-flow reversals and negative HF momentum over next 10 min, fading within an hour; authors suggest intraday hedging of positive-gamma portfolio profitable if costs low. No backtested rule.
- **Cost sensitivity:** High at 5-10 min; moderate at 30-60 min.  
- **Firm compatibility:** Both intraday.
- **Overlap with closed families:** Closed: gamma/GEX-conditioned LAST-HALF-HOUR momentum. NEW: full-session regime switch between MR and momentum keyed to net gamma; flag heavy adjacency.
- **Plausibility of net Sharpe >= 1.5:** low-medium  
- **Why not already tested:** Prior test used GEX only to condition the closing-momentum trade.
- **Pre-registerable test:** Daily net-gamma sign from prior-close OI (free CBOE data); on positive days run C21-style fade (z>2, 15-min), on negative days run 30-min breakout continuation; OOS 2022-2026 (0DTE era); compare to unconditional.  
- **Evidence quality:** 2024-2026 WPs; summary-level

### 7-eod-flows

#### C24 - Leveraged-ETF rebalancing-demand-sized last-30-min momentum in NQ (TQQQ/SQQQ complex) and ES on large-move days

- **Mechanism:** Daily-rebalanced LETFs must buy (sell) after up (down) days in proportion to AUM x leverage x day return, executed 15:30-16:00; option dealers' gamma hedging adds; intermediaries now pre-hedge strategically, weakening LETF predictability.
- **References:** Shum, Hejazi, Haryanto, Rodier (2016), *Intraday Share Price Volatility and Leveraged ETF Rebalancing*, Review of Finance 20(6):2379-2409, https://www.cxoadvisory.com/volatility-effects/front-running-leveraged-etfs-at-the-end-of-the-day; Cheng, Madhavan (2009), *The Dynamics of Leveraged and Inverse Exchange-Traded Funds*, Journal of Investment Management 7(4), not fetched; Barbon, Beckmeyer, Buraschi, Moerke (2022), *Liquidity Provision to Leveraged ETFs and Equity Options Rebalancing Flows: Evidence from End-of-Day Stock Prices*, SFI Research Paper 22-40 / SSRN 3925725, https://www.sfi.ch/en/publications/n-22-40-liquidity-provision-to-leveraged-etfs-and-equity-options-rebalancing-flows-evidence-from-end-of-day-stock-prices
- **Instruments:** NQ/MNQ (primary), ES/MES, RTY (TNA/TZA)  
- **Holding period:** 15:30/15:45 -> 16:00 ET  
- **Data needed:** 1-min NQ/ES; daily LETF AUM (issuer sites, free) to compute dollar rebalancing demand = sum(AUM_i x L_i x (L_i-1) x r_day)
- **Reported performance:** Shum et al.: buying after >=2% moves at 14:45 and selling at close earned 0.60% gross/trade, concentrated in late 2008; rebalancing explains ~1/3 of late-day vol. Barbon et al.: LETF effects weakened over time; gamma effects persist; flows attract liquidity provision.
- **Cost sensitivity:** Low on trigger days (moves >1%); few trades (15-30/yr).  
- **Firm compatibility:** Both intraday.
- **Overlap with closed families:** Heavy: closed last-half-hour momentum and its gamma version. New element = dollar-demand sizing from LETF AUM and NQ focus; proceed only as a conditional variant.
- **Plausibility of net Sharpe >= 1.5:** low-medium (event-sparse)  
- **Why not already tested:** Demand-sized conditioning with free AUM data not used before.
- **Pre-registerable test:** Days with |r[09:30->15:30]|>1.5%: trade direction of day 15:30-16:00 in NQ, size by estimated LETF demand; compare unconditional vs demand-top-quartile; OOS 2019-2026.  
- **Evidence quality:** RoF 2016 + SFI 2022

#### C25 - Closing-auction imbalance (MOC) -> last-10-minute ES/NQ drift and overnight reversal (Bogousslavsky-Muravyev)

- **Mechanism:** Passive/ETF and institutional rebalancing concentrate in the closing auction; disseminated imbalances (NYSE 15:50, Nasdaq 15:55) move prices into the close; closing-price deviations from midquotes fully revert overnight.
- **References:** Bogousslavsky, Muravyev (2023), *Who Trades at the Close? Implications for Price Discovery and Liquidity*, Journal of Financial Markets (forthcoming); SSRN 3485840, https://aeaweb.org/conference/2021/preliminary/paper/H9T4hef7; Jegadeesh, Wu (2022), *Closing auctions: Nasdaq versus NYSE*, Journal of Financial Economics 143 (from memory - verify), not fetched
- **Instruments:** ES, NQ (15:50-16:00), FTMO US500  
- **Holding period:** 15:50/15:55 -> 16:00; overnight reversal not holdable at futures firms  
- **Data needed:** Aggregate MOC imbalance feed (paid: NYSE/Nasdaq imbalance; Databento XNAS.ITCH imbalance messages - likely exceeds budget) or free vendor summaries
- **Reported performance:** Imbalance information contributes to price discovery; magnitudes not retrieved; closing-price deviations revert overnight.
- **Cost sensitivity:** Moderate.  
- **Firm compatibility:** Both intraday for the pre-close leg.
- **Overlap with closed families:** Adjacent to closed last-half-hour family.
- **Plausibility of net Sharpe >= 1.5:** low-medium but DATA-BLOCKED  
- **Why not already tested:** Imbalance data cost.
- **Pre-registerable test:** If a free aggregate imbalance proxy exists: sign(imbalance at 15:50) -> ES 15:51-15:59; else skip.  
- **Evidence quality:** JFM 2023 abstract

#### C26 - Option-expiration pinning / anti-cross-pinning in S&P futures (Golez-Jackwerth) extended to the 0DTE era

- **Mechanism:** Market makers rebalance delta hedges as options lose time value: futures gravitate toward the ATM strike on days ES options expire (pinning) and move away from the carry-adjusted ATM strike before SPX index-option expirations (anti-cross-pinning); >= $115m notional shift per expiration day.
- **References:** Golez, Jackwerth (2012), *Pinning in the S&P 500 futures*, Journal of Financial Economics 106(3):566-585, https://ideas.repec.org/a/eee/jfinec/v106y2012i3p566-585.html; Adams et al. (2025), *Do S&P500 Options Increase Market Volatility? Evidence from 0DTEs*, SSRN 5641974, https://quantpedia.com/do-sp500-0dtes-options-increase-market-volatility/
- **Instruments:** ES/MES (also NQ vs NDX strikes)  
- **Holding period:** Last 1-2 hours of expiration days (now daily for SPXW 0DTE; Mon/Wed/Fri + EOM for ES options)  
- **Data needed:** 1-min ES; strike grid (SPX 5/25 pts, ES options 5 pts); option expiration calendar (CME/CBOE, free); optional OI by strike (CBOE delayed)
- **Reported performance:** 1992-2009 serial expirations: statistically significant pinning in futures; anti-cross-pinning before SPX expirations; no pinning in cash basket. No strategy Sharpe. 0DTE era untested.
- **Cost sensitivity:** High (distance-to-strike moves are a few points).  
- **Firm compatibility:** Both intraday.
- **Overlap with closed families:** Not closed.
- **Plausibility of net Sharpe >= 1.5:** low-medium  
- **Why not already tested:** Requires strike-grid construction; 0DTE regime new.
- **Pre-registerable test:** At 15:00 on expiration days compute d = nearest-strike - price (for ES-option expiries) and carry-adjusted d for SPX expiries; predict sign of 15:00-16:00 return = sign(d) (pinning) or -sign(d) (anti-cross); trade when |d| in [0.1,0.5] x strike spacing; IS 2012-2019, OOS 2020-2026.  
- **Evidence quality:** JFE 2012

#### C27 - Overnight drift: long ES during the 02:00-03:00 ET European-open hour, conditional on prior-day US order imbalance (Boyarchenko-Larsen-Whelan)

- **Mechanism:** Dealers absorb negative end-of-day order imbalances at the 16:15 US close and unwind them when European liquidity arrives (02:00-03:00 ET), paying a positive return; asymmetric: strong positive reversals after US selloffs, modest after rallies (time-varying dealer risk capacity).
- **References:** Boyarchenko, Larsen, Whelan (2023), *The Overnight Drift*, Review of Financial Studies 36(9); NY Fed Staff Report 917 (Feb 2020, rev. Aug 2022), https://www.newyorkfed.org/research/staff_reports/sr917; Bondarenko, Muravyev (2020), *Market Return Around the Clock: A Puzzle (replication: lion's share of overnight return in that hour)*, SSRN (from search citation), not fetched
- **Instruments:** ES/MES (also NQ, FTMO US500/US100 24h CFD)  
- **Holding period:** 02:00-03:00 ET (or 01:30-03:30); DST: window shifts when US/EU offsets differ  
- **Data needed:** 1-min ES overnight session 1998-2026 (Databento GLBX.MDP3 ohlcv-1m), signed volume 15:15-16:15 for RSV conditioner (tbbo or BVC proxy from bars)
- **Reported performance:** 1998-2020: +1.48 bps/day (3.7% annualized) in 02:00-03:00; positive in 20/23 years, significant in 17; only hour significant in all subsamples; strategy long 02:00-03:00 Sharpe 1.1 gross, -0.5 after full bid-ask; 01:30-03:30 Sharpe 1.3 gross / 0.3 net; conditioning on negative close RSV strengthens.
- **Cost sensitivity:** Decisive: at 1998-2020 index levels the spread exceeded the edge; at 2024-2026 levels (ES ~5000-6500) 1 tick = 0.4-0.5 bps so gross 1.5 bps/day leaves ~0.5-1 bps net; must use passive/limit entries and condition on prior-day selloff.  
- **Firm compatibility:** Futures firms: allowed (overnight session trading, flat long before the daily close). FTMO: yes, 24h index CFD, no swap (intraday).
- **Overlap with closed families:** Not closed (overnight-gap FADE and macro events are different windows).
- **Plausibility of net Sharpe >= 1.5:** medium (best-documented, mechanism-based, top-journal, persisted through 2020; net Sharpe realistically 0.3-0.8 unconditional, higher conditional)  
- **Why not already tested:** Prior work focused on RTH; overnight-session hour-of-day never tested.
- **Pre-registerable test:** Long 1 MES at 02:00 ET, exit 03:00 (limit-order entry at bid, 1-tick cost stress); variants: 01:30-03:30; condition on prior-day RTH return <0 or RSV<0 (BVC from 15:15-16:15 bars); DST handling per paper; IS 1998-2018 (replicate 1.48 bps), OOS 2021-2026 (post-publication); report bps/day, net Sharpe, yearly sign.  
- **Evidence quality:** RFS 2023; numbers verified from staff report

### 8-vol-managed-overlay

#### C30 - Volatility targeting / conditional vol scaling as a risk overlay (not an alpha) using intraday realized vol

- **Mechanism:** Volatility is persistent and forecastable while returns are not; scaling exposure by 1/sigma raises Sharpe for assets with leverage effect (equities, credit) and cuts tails/drawdowns everywhere; intraday RV from 1-min bars is the best next-day vol forecast.
- **References:** Moreira, Muir (2017), *Volatility-Managed Portfolios*, Journal of Finance 72(4):1611-1644, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2659431; Harvey, Hoyle, Korgaonkar, Rattray, Sargaison, Van Hemert (2018), *The Impact of Volatility Targeting*, Journal of Portfolio Management 45(1):14-33, https://scholars.duke.edu/publication/1370354; Cederburg, O'Doherty, Wang, Yan (2020), *On the performance of volatility-managed portfolios*, Journal of Financial Economics 138:95-117 (from memory - verify), not fetched; Bongaerts, Kang, van Dijk (2020), *Conditional Volatility Targeting*, Financial Analysts Journal 76(4) (from memory - verify), not fetched
- **Instruments:** All; applied to every strategy's sizing  
- **Holding period:** Overlay  
- **Data needed:** 1-min bars (RV), VIX
- **Reported performance:** Harvey et al. (1926-2017, 60+ assets): equity Sharpe ~0.40 -> ~0.48-0.51 scaled; negligible for bonds/FX/commodities; tail and drawdown reduction broad. Cederburg et al.: real-time implementable gains largely vanish for factor portfolios.
- **Cost sensitivity:** Low (sizing changes daily).  
- **Firm compatibility:** Essential for daily-loss/trailing-drawdown rules at prop firms.
- **Overlap with closed families:** Not closed; it is an overlay.
- **Plausibility of net Sharpe >= 1.5:** n/a as standalone (low alpha); high value as risk control  
- **Why not already tested:** Overlay, not an edge.
- **Pre-registerable test:** Size each day so that forecast daily vol (RV_1min EWMA) x position <= 1/3 of firm daily loss limit; compare Sharpe/maxDD of each strategy with and without scaling; never increase size above base in low-vol.  
- **Evidence quality:** JF 2017 + JPM 2018; OOS caveats JFE 2020

### 9-calendar

#### C28 - FOMC-cycle even-week long bias for ES (Cieslak-Morse-Vissing-Jorgensen) applied intraday

- **Mechanism:** Equity premium 1994-2016 earned entirely in even weeks (0,2,4,6) of the FOMC cycle; half from mean reversion after declines ('Fed put' / informal Fed communication); fed funds vol peaks in even weeks.
- **References:** Cieslak, Morse, Vissing-Jorgensen (2019), *Stock Returns over the FOMC Cycle*, Journal of Finance 74(5):2201-2248, https://papers.ssrn.com/abstract=2687614
- **Instruments:** ES/MES, NQ; FTMO US500  
- **Holding period:** Intraday RTH sessions in even weeks (overnight component not capturable at futures firms; FTMO Swing can hold)  
- **Data needed:** Daily + 1-min ES; FOMC meeting calendar (free)
- **Reported performance:** Even-minus-odd week excess return highly significant 1994-2016, robust in subperiods and internationally; odd weeks -0.09% to -0.18% avg. Post-2016 OOS: not found. Most index premium accrues overnight (Lou-Polk-Skouras), so intraday capture is small.
- **Cost sensitivity:** Low (1 RT/day).  
- **Firm compatibility:** Futures firms intraday; FTMO Swing can hold overnight (swap).
- **Overlap with closed families:** Partial: closed macro-event family includes Lucca-Moench pre-FOMC drift (week 0). Broader cycle weeks not tested.
- **Plausibility of net Sharpe >= 1.5:** low  
- **Why not already tested:** Cycle-time indexing not implemented.
- **Pre-registerable test:** Long ES 09:30-16:00 only in even weeks vs odd weeks, 2017-2026 OOS; also overnight-inclusive version for FTMO Swing.  
- **Evidence quality:** JF 2019

#### C29 - Option-expiration (OPEX/quad-witching) week and pre-holiday long bias in index futures

- **Mechanism:** OPEX week: higher large-cap returns 1983-2008 attributed to option hedging/liquidity (Stivers-Sun); pre-holiday: positive sentiment and institutional window dressing (Ariel; Lakonishok-Smidt).
- **References:** Stivers, Sun (2013), *Returns and Option Activity over the Option-Expiration Week for S&P 100 Stocks*, Journal of Banking and Finance 37 (verify), https://quantpedia.com/strategies/option-expiration-week-effect; Ariel (1990), *High stock returns before holidays: Existence and evidence on possible causes*, Journal of Finance 45(5) (from memory), not fetched
- **Instruments:** ES, NQ, YM; FTMO indices  
- **Holding period:** Intraday sessions in OPEX week / day before holidays  
- **Data needed:** Daily + 1-min; CBOE expiration and NYSE holiday calendars
- **Reported performance:** OPEX-week effect 1996-2008 significant for S&P 100 stocks; no credible 2015-2023 replication found. Pre-holiday effect weakened post-1990s (literature).
- **Cost sensitivity:** Low.  
- **Firm compatibility:** Both intraday.
- **Overlap with closed families:** Adjacent to closed turn-of-month calendar family.
- **Plausibility of net Sharpe >= 1.5:** very low  
- **Why not already tested:** Low priority.
- **Pre-registerable test:** Mean RTH return in OPEX week vs others, pre-holiday vs others, 2010-2026 with bootstrap; expect null.  
- **Evidence quality:** old; unreplicated

#### C31 - Day-of-week / weekend effects in CME crypto futures (BTC/MBT, ETH/MET)

- **Mechanism:** Retail-dominated weekend trading with lower volume; Monday returns reflected weekend spot moves pre-24/7; early studies found higher Monday returns, later ones none.
- **References:** Caporale, Plastun (2017), *The Day of the Week Effect in the Crypto Currency Market*, CESifo WP 6716, https://cesifo.org/DocDL/cesifo1_wp6716.pdf; Aharon, Qadan (2019), *Bitcoin and the day-of-the-week effect*, Finance Research Letters 31, https://cris.haifa.ac.il/en/publications/bitcoin-and-the-day-of-the-week-effect/; CME Group (2026), *Aligning cryptocurrency derivatives with spot markets: measuring the 24/7 trading opportunity*, CME research, https://www.cmegroup.com/articles/2026/aligning-cryptocurrency-derivatives-with-spot-markets-measuring-the-247-trading-opportunity.html
- **Instruments:** BTC/MBT, ETH/MET (CME)  
- **Holding period:** Intraday by weekday  
- **Data needed:** 1-min MBT 2020-2026
- **Reported performance:** Caporale-Plastun (2013-2017): Monday higher for Bitcoin only; 2021 GARCH (2013-2019) and 2024 study: no DOW return effect, lower weekend vol. CME moving to 24/7 (pending) removes weekend gap.
- **Cost sensitivity:** Moderate (MBT spread).  
- **Firm compatibility:** Futures firms: MBT/MET allowed at many; FTMO crypto CFDs yes.
- **Overlap with closed families:** Adjacent to closed crypto hour-of-day/TSMOM family.
- **Plausibility of net Sharpe >= 1.5:** very low  
- **Why not already tested:** DOW not in closed list explicitly.
- **Pre-registerable test:** Weekday mean intraday returns 2020-2026 with Bonferroni; expect null.  
- **Evidence quality:** mixed/negative

## Decay evidence and implied haircuts

Published anomalies lose roughly half their in-sample performance out of sample; decay is fastest for high in-sample Sharpe (overfitting), for recently published strategies, and in the most arbitraged market (US). Mechanism-based intraday edges die abruptly when the underlying institution changes (fix window 2015, lock-up reforms 2014/2020, gold auction 2015, LETF pre-hedging, Bloomberg strike move 2021) rather than fading gradually.

- **McLean & Pontiff 2016, 'Does Academic Research Destroy Stock Return Predictability?', Journal of Finance 71(1)** - 97 anomalies: returns 26% lower post-sample/pre-publication and 58% lower post-publication; decay larger for high in-sample returns and for cheap-to-arbitrage stocks. (from memory - widely cited numbers) https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2156623
- **Falck, Rej & Thesmar 2022, 'When do systematic strategies decay?', Quantitative Finance 22(11):1955-1969 (WP 'Why and how systematic strategies decay', arXiv 2105.01380)** - 72 published strategies (US 1963-2014, intl 1995-2018): OOS performance about 50% of in-sample; publication year explains ~30% of decay variance (newer decays faster, ~5pp/yr); overfitting proxies (in-sample Sharpe) add ~15%; arbitrage proxies marginal. (verified via search summary) https://arxiv.org/pdf/2105.01380
- **Jacobs & Muller 2020, 'Anomalies across the globe: Once public, no longer existent?', Journal of Financial Economics 135(1)** - 241 anomalies in 39 countries: significant post-publication decline only in the US; no reliable decline elsewhere -> arbitrage (not data mining) drives US decay; expect fastest decay in US liquid futures. (from memory - verify) https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2816490
- **Chen & Zimmermann 2020, 'Publication Bias and the Cross-Section of Stock Returns', Review of Asset Pricing Studies 10(2)** - Bias-adjusted expected returns only ~12% below in-sample for published predictors; the much larger post-publication drop (~50%+) is therefore mostly real decay (mispricing correction), not selection bias. (from memory - verify) https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2802357
- **Harvey, Liu & Zhu 2016 RFS '...and the Cross-Section of Expected Returns'; Harvey & Liu 2021 JFE 'Lucky Factors'** - Multiple testing implies t>3.0 hurdle for new findings; bootstrap-based 'lucky factors' procedure to control false discoveries across many tested variants. (from memory) https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2528780
- **Hou, Xue & Zhang 2020 RFS 'Replicating Anomalies'; Jensen, Kelly & Pedersen 2023 JF 'Is There a Replication Crisis in Finance?'** - HXZ: 65% of 452 anomalies insignificant with value weights/no microcaps. JKP: Bayesian hierarchical model - most factors replicate, work OOS in 93 countries, but posterior alphas are shrunk and post-publication alphas lower (not zero). (verified (JKP abstract)) https://www.nber.org/papers/w28432
- **Suhonen, Lennkh & Perez 2017, 'Quantifying Backtest Overfitting in Alternative Beta Strategies', Journal of Portfolio Management 43(2)** - 215 bank systematic strategies: live Sharpe about 27% of backtest Sharpe (median haircut ~73%). (from memory - verify) not fetched
- **Mechanism-shutdown cases found in this sweep** - Pre-announcement drift (Kurov) tied to pre-release procedures changed 2013-2014; WMR fix reversals shrank after Feb-2015 5-minute window (FCA OP46); London gold fix leakage ended with ICE electronic auction Mar-2015; LETF end-of-day effects weakened as intermediaries pre-hedge (Barbon et al. 2022); Goldman-roll front-running unprofitable after 2004 (Dubois-Marechal); Treasury index strike moved 3pm->4pm Jan-2021 (NY Fed); 0DTE daily since May-2022 changed gamma dynamics. (verified) see candidates

**Implied haircuts:**
- published_in_sample_to_live_us_liquid_futures: multiply gross in-sample Sharpe by 0.4-0.5 (publication decay) then subtract costs; for strategies with in-sample Sharpe > 2 assume additional overfitting haircut (0.3x).
- practitioner_backtest_to_live: 0.25-0.5x (Suhonen et al.; Bailey-Lopez de Prado deflated Sharpe).
- required_backtest_bar: to credibly deliver net Sharpe 1.5 live, a single pre-registered strategy needs post-cost OOS Sharpe >= 3 (t>3 with >= 300 trades), or a portfolio of >= 5 weakly correlated mechanism-based sleeves each with net OOS Sharpe >= 0.6.
- regime_rule: treat any institutional change date as a hard sample split; evidence before the change does not count toward OOS.

## Prompt rules (imperative)

1. Treat every published in-sample Sharpe as an upper bound; apply a 0.5x publication haircut and full costs before deciding whether a candidate can reach net Sharpe 1.5.
2. Pre-register each test: paper's exact rule, parameters, window, instruments, IS/OOS split and success threshold written to a file before the first backtest; one OOS evaluation per registered variant.
3. Prioritise edges with an identifiable forced trader and a verifiable timestamp: fix windows, index strike times, auction results, LETF rebalancing, option expiries, European open.
4. Split every sample at institutional change dates (2015-02 fix window, 2015-03 gold auction, 2021-01-14 Treasury strike, 2022-05 daily 0DTE, 2014 lock-up reforms); only post-change data counts as OOS.
5. Convert all timestamps to exchange/local time with explicit DST handling (ET, London, JST, CET) and verify event times against the official calendars.
6. Model costs as >=1 tick plus commission per side, add slippage for market orders at 02:00 ET, opens and settlements; require the edge to survive 2x costs.
7. Report gross edge in ticks per trade; drop any rule averaging under 2 ticks per trade unless n>=500 and win rate above 58%.
8. Spend Databento first on ohlcv-1m for ES, NQ, ZN, 6E, 6J, CL, GC, ZC 2018-2026 including overnight sessions; buy tbbo only for a 3-month ES sample to validate BVC order-flow proxies.
9. Flag any variant of a CLOSED family and test it only if the construction is materially different (new asset class, new window, new conditioning data) and documented as such.
10. Control multiple testing across all variants with Harvey-Liu t>3 or deflated Sharpe; log every test, including failures, in a running registry.
11. Build the portfolio from several small mechanism-based sleeves (overnight drift, month-end Treasury strike, FX fixes, EIA/WASDE continuation) rather than one dominant strategy.
12. Size positions with intraday realized-vol targeting so forecast daily P&L vol is at most one third of the prop firm's daily loss limit; never scale up in low-vol regimes beyond base size.
13. Check instrument availability per firm before testing: Treasury and grain futures only at futures firms; DAX/FTSE/Nikkei/HSI only via FTMO CFDs; overnight-session trades allowed at futures firms if flat before the daily close.

## Sources swept

- https://academicweb.nd.edu/~zda/intramom.pdf (Baltussen-Da-Lammers-Martens 2021 JFE, full text read)
- https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf (Boyarchenko-Larsen-Whelan, full text read)
- https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2019/12/17-19.Schwarz.pdf (Hartley-Schwarz, full text read)
- https://www.fca.org.uk/publication/occasional-papers/occasional-paper-46.pdf (Evans-O'Neill-Rime-Saakvitne, full text read)
- https://www.norges-bank.no/.../39-panagiotou---the-wmr-fix-and-its-impact-on-currency-markets-.pdf (Marsh-Panagiotou-Payne 2017, full text read)
- https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1901.en.pdf (Kurov et al. 2016 WP, full text read)
- https://www.nber.org/system/files/working_papers/w25127/w25127.pdf (Brooks-Katz-Lustig, full text read)
- https://researchmgt.monash.edu/ws/files/519509174/494419119_oa.pdf (Limkriangkrai-Chai-Zheng 2023 PBFJ, full text read)
- https://libertystreeteconomics.newyorkfed.org/2026/09/treasury-trading-at-the-close/ (read)
- https://ideas.repec.org/a/wly/jfutmk/v40y2020i4p632-650.html (Jin et al. 2020 abstract)
- https://quantpedia.com/do-sp500-0dtes-options-increase-market-volatility/ (Adams et al. 0DTE summary)
- https://www.sfi.ch/en/publications/n-22-40-... (Barbon-Beckmeyer-Buraschi-Moerke abstract)
- https://ideas.repec.org/a/eee/dyncon/v136y2022ics0165188922000185.html (Kang-Lin-Xiong 2022 abstract)
- https://arxiv.org/abs/1904.04912, /2211.13777, /2106.04028, /2112.08534, /2501.03171 (abstracts)
- https://www.nber.org/papers/w22820 (Ito-Yamada abstract); https://researchonline.lse.ac.uk/id/eprint/43120/ (Lou-Yan-Zhang abstract)
- WebSearch result summaries (Nov 2026) for: Krohn-Mueller-Whelan JF 2024; Golez-Jackwerth JFE 2012; Falck-Rej-Thesmar QF 2022; Kurov et al. JFQA 2019; Anderson-McKenzie-Noyes 2024; Cieslak-Morse-Vissing-Jorgensen JF 2019; Caminschi-Heaney JFM 2014; Grant-Wolf-Yu JBF 2005; Rif-Utz 2021; Stivers-Sun; Chinco-Clark-Joseph-Ye JF 2019; Jensen-Kelly-Pedersen JF 2023; Mou 2011; Dubois-Marechal; Nagel RFS 2012; Shum et al. RoF 2016; Bogousslavsky-Muravyev JFM 2023; Harvey et al. JPM 2018; Caporale-Plastun 2017; Geman-Li JEM 2018; Etula et al. RFS 2020
- NOT reachable this session (403/limits): SSRN full texts, risk.net, Elsevier/Wiley paywalls, reading.ac.uk eprints; Zhang-Wang-Li 2021 'Bond intraday momentum' abstract not found; Elaut et al. 2018 abstract not found.

## Caveats
- Web search budget and fetch limits were hit; several magnitudes marked 'not retrieved' or 'from memory - verify'.
- SSRN/Elsevier full texts unreachable; eight PDFs were read in full (listed in sources_swept).
- Plausibility ratings are the author's judgment, not computed.
