# PumpWatch: Detection Literature Review (Detection Science, Team A)

**Status / confidence:** Draft v1, written 2026-10-04. Overall confidence is **medium**. Every number below was read in the full text, the abstract, or a publisher or regulator page that I opened myself. Where I saw only an abstract, a search-engine summary, or a secondary write-up, the entry says so. Anything I could not confirm is marked **UNVERIFIED**. The recommendations at the end are evidence-led where possible. Where no source supports a parameter, the recommendation is labelled **GUESS**.

**Network access used:** WebSearch, WebFetch, and `curl` through the agent proxy. Full PDFs were downloaded and read from arXiv, NBER, USENIX, NSF-PAR, FINRA.org, thomas-renault.com and readkong.com. Metadata and some abstracts came from the Crossref REST API. Regulator pages read: FBI IC3, FINRA.org, SEC.gov. Law-firm and news pages were used only for the Nasdaq and SEC 2025–26 items.
**Blocked or failed:** SSRN (403), ScienceDirect (403), Springer/BioMed Central (login redirect), IEEE Xplore (418), ResearchGate (403), Harvard DASH (bot check), HAL (bot check), OpenAlex (rate-limited), and the OTC Markets policy page (rendered empty).
**Worker subagents:** none spawned. No Agent tool was available in this session, so I did all of the work myself.

---

## 0. Executive summary (read this first)

1. **Equities: the pump-and-dump (P&D) window is short.** In stock studies, prices rise on the day before and the day of the promotion spike, then reverse within about 2–5 trading days (Renault: +4.10% on day −1, +6.88% on day 0, −3.11% over days [+1,+5]; Sabherwal et al.: "two-day pump followed by a two-day dump"). For an investor-protection alert to be useful, it must fire **on day −1 or day 0** of the social spike. The 20-day "quiet accumulation" pattern has almost no direct support in the literature (see S2).
2. **Who is talking matters more than how much.** In Renault's data, price reversals happen only for tweet spikes that involve known promoters or pump-tracker accounts (−5.34% vs +0.87%). Sabherwal et al. find that sentiment predicts next-day returns but the raw post count does not. Mention-count bursts (S4) on their own are weak.
3. **Detectors that use only price and volume produce many false positives.** When La Morgia et al. re-ran the Kamps & Kleinberg price/volume anomaly detector on confirmed pumps, precision was 15.9%–52.1%. Their own detector reached 98.2% precision but used order-book "rush orders" seen 25 seconds *after* the pump starts. This supports keeping the ≥2-independent-families rule.
4. **Crypto "prediction" papers report high AUC, but lead times are seconds to hours**, and operating precision and recall are much lower than the AUC suggests. Xu & Livshits had 9/9 correct flags on their test set but caught only 9 of 60 pumps (recall 15%, my calculation from their Table 3). In Bolz et al., top-5 target hit rate falls from 55.81% at 20 seconds before the pump to 19.05% at 1 minute before.
5. **The 2024–2026 "ramp-and-dump" wave is a different shape from classic OTC P&D.** Targets are exchange-listed, small-float issuers with foreign (often China/HK) operations. Schemes now run **months after the IPO**, often several times on the same issuer. FINRA describes nominee accounts "funneling" shares to foreign omnibus accounts beforehand, account-takeover (ATO) buying, investment-club victims, and coordinated limit orders (FINRA 2026 Oversight Report, pp. 21–22). Our S3 and S6 do not yet model most of this.
6. **Our news filter has a blind spot.** In SEC P&D complaints from 2002–2015, **press releases were the most common promotion channel (73.3%)** (Renault, SEC sample). PumpWatch currently treats "PR", "NEWS" and "6-K" filings as innocent explanations for volume. For foreign-issuer ramp-and-dumps, a 6-K or press release may *be* the pump.

---

## 1. Source-by-source review

Format for each entry: **Citation + URL**, then Market & data, Method, What predicted the pump and how early (lead time), Reported performance (exact numbers and where in the paper), Limitations, and Relevance to PumpWatch. "Access" states what I actually read.

### A. Equities, OTC and spam-era promotion

#### A1. Renault (2017/2018): Market manipulation and suspicious stock recommendations on social media
- **Citation:** Thomas Renault, "Market Manipulation and Suspicious Stock Recommendations on Social Media," SSRN WP 3010850 (2017), DOI 10.2139/ssrn.3010850. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3010850 (SSRN returned 403). Read instead: author PDF dated 14 April 2018, https://www.thomas-renault.com/wp/market-manipulation-suspicious.pdf, and a 20 Nov 2016 draft on readkong.com.
- **Access:** full text (2018 version).
- **Market & data:** Twitter only (not StockTwits). 7,196,307 tweets from 248,748 users mentioning 5,087 OTC small caps (OTCQX/OTCQB/Pink), 5 Oct 2014 – 1 Sep 2015. Also hand-coded 273 SEC "market manipulation" complaints from 2002–2015, of which 150 are P&D.
- **Method:** event study. An event day is when the daily tweet count exceeds the **yearly average + 2 standard deviations**, with **at least 20 tweets** and **market cap ≥ $1,000,000**, and at least **20 trading days between events**. Tweets from 4 p.m. on t−1 to 4 p.m. on t count toward day t. This gives 635 events across 315 firms. Promoters were a manual list of 156 promoter or paid-advertiser accounts. Regressions control for lagged returns, press releases, sentiment and firm characteristics.
- **What predicted the pump / lead time:** abnormal return is **+4.10% on day −1** and **+6.88% on day 0** (significant), followed by a cumulative abnormal return (CAR) of **−3.11% over [+1,+5]** (Section 5). The tweet spike is effectively the pump, so the warning window is day −1 to day 0.
- **Effect sizes:** at least one promoter tweet appeared in **403 of 635 events (63.46%)**. Pump-tracker accounts (@ThePumpTracker, @PUMPSandDUMPS) appeared in **57 events (8.98%)**. "Promoter events" (407) show a reversal of **−5.34%** over 5 days; non-promoter events show **+0.87%** (Table 10). In the SEC sample, **86%** of P&D cases targeted OTC stocks. Promotion channels were press releases **73.3%**, spam/newsletters **34%**, websites **32%**, fax **12.6%** and message boards **10.6%** (Table 2 discussion, p. 6). 84.88% of events had positive sentiment.
- **Limitations:** Twitter in 2014–15, OTC only. The study is descriptive, not a classifier, so there is no precision or recall. Promoter labels are manual.
- **Relevance:** the main source for S4 thresholds (mean + 2 SD, ≥20 posts), for the case that promoter identity carries the signal, and for the conclusion that **press releases are the main promotion vehicle and should not count as innocent news** in S1.

#### A2. Frieder & Zittrain (2006/2008): Spam works
- **Citation:** Laura Frieder & Jonathan Zittrain, "Spam Works: Evidence from Stock Touts and Corresponding Market Activity," *Hastings Communications and Entertainment Law Journal* 30(3):479 (2008). SSRN DOI 10.2139/ssrn.920553. https://repository.uclawsf.edu/hastings_comm_ent_law_journal/vol30/iss3/3
- **Access:** abstract only, via Crossref and the UC Law SF repository page. The PDF was behind a bot check.
- **Market & data:** Pink Sheets stocks touted by spam e-mail. The exact period and sample size are **UNVERIFIED**.
- **Method:** event-style regressions of returns and volume on touting intensity.
- **What predicted / lead time:** "stocks experience a significantly positive return on **days prior to** heavy touting." Price run-up before the touting is a pre-signal of a few days; the exact count is **UNVERIFIED**.
- **Effect sizes (abstract):** the probability that a touted stock is the most actively traded stock in the sample goes from **4% on a no-touting day to 70% on a touting day**. Returns after touting are significantly negative. An investor who buys on a peak touting day and sells two days later loses about **5.5%**; spammers earn about **4.29%** before transaction costs (repository abstract).
- **Limitations:** e-mail spam era (2004–06). Only the abstract was read.
- **Relevance:** supports S1, and supports the claim that a short pre-touting price rise exists. "Buy low, spam high" is the S2/S5 sequence compressed into days, not weeks.

#### A3. Hanke & Hauser (2008): On the effects of stock spam e-mails
- **Citation:** Michael Hanke & Florian Hauser, "On the effects of stock spam e-mails," *Journal of Financial Markets* 11(1):57–83 (2008), DOI 10.1016/j.finmar.2007.10.001. SSRN 965509.
- **Access:** SSRN abstract via Crossref, plus a University of Innsbruck press release (Nov 2007): https://www.uibk.ac.at/archive/public-relations/presse/texte/2007/200711/pa153_2007.html. ScienceDirect returned 403.
- **Market & data:** 1,241 spam e-mails, 235 US-listed stocks, 2005. Each stock was spammed on about 5 days on average (press release).
- **Method:** excess returns, turnover and intraday range around spam days.
- **What predicted / lead time:** spam has a significant effect on excess returns, turnover and intraday range. The positive price effect does not last; per the press release it is limited to one day. **Liquidity is a major factor** in spam success. **Spamming on successive days keeps excess demand up** and gives the spammers a longer window to sell.
- **Effect sizes:** exact coefficients are **UNVERIFIED** (full text not accessible).
- **Relevance:** supports S1 using a liquidity-conditioned baseline and S5 using a multi-day campaign window. Campaigns repeated over several days are the norm (average about 5 days), which supports `coord_window_days = 3` or more.

#### A4. Böhme & Holz (2006): The effect of stock spam on financial markets
- **Citation:** Rainer Böhme & Thorsten Holz, "The Effect of Stock Spam on Financial Markets," WEIS 2006, Cambridge, pp. 1–24. SSRN DOI 10.2139/ssrn.897431. Record: https://madoc.bib.uni-mannheim.de/23040
- **Access:** catalogue record, plus the abstract text as shown in a search-engine snippet. The PDF links failed (404 or timeout).
- **Method & findings (abstract):** multivariate regressions of traded volume on spam, and an event study on returns, find "significant reactions to spam campaigns in the short run."
- **Numbers:** all **UNVERIFIED**.
- **Relevance:** independent confirmation of A2 and A3: volume reacts to promotion within days.

#### A5. Aggarwal & Wu (2006): Stock market manipulations
- **Citation:** Rajesh K. Aggarwal & Guojun Wu, "Stock Market Manipulations," *Journal of Business* 79(4):1915–1953 (2006), DOI 10.1086/503652. Working paper: SSRN 474582 (2003), DOI 10.2139/ssrn.474582.
- **Access:** abstract of the 2003 working paper via Crossref.
- **Market & data:** SEC manipulation actions in the US. Sample size and period **UNVERIFIED**.
- **Findings (abstract):** likely manipulators are insiders, brokers, underwriters, large shareholders and market makers. **More illiquid stocks are more likely to be manipulated**, and manipulation increases volatility. **Prices rise throughout the manipulation period and fall afterwards.** Prices and liquidity are higher when the manipulator sells.
- **Effect sizes:** **UNVERIFIED**.
- **Relevance:** supports S3 (insider and control-person involvement) and using illiquidity as a prior. "Liquidity higher when the manipulator sells" supports S1 firing on volume.

#### A6. Leuz, Meyer, Muhn, Soltes & Hackethal: Who falls prey to the Wolf of Wall Street?
- **Citation:** Christian Leuz, Steffen Meyer, Maximilian Muhn, Eugene Soltes & Andreas Hackethal, "Who Falls Prey to the Wolf of Wall Street? Investor Participation in Market Manipulation," NBER WP 24083 (Nov 2017, revised June 2021). https://www.nber.org/system/files/working_papers/w24083/revisions/w24083.rev1.pdf
- **Access:** full text.
- **Market & data:** trading records for more than 110,000 clients of one German bank, matched to touted stocks from Jan 2002 to Jan 2015. Tout cases come from BaFin (259 alleged illegal campaigns) plus a hand-collected set.
- **Method:** participation, returns and investor-type analysis.
- **Findings (pp. 2–3):** 6,569 investors made more than 20,000 purchases in the first 60 days of **421** schemes. "Nearly 6%" of sample investors bought at least one. Each year a sample investor has a **2%** chance of joining a tout. The average stake is **€6,972**, which is 11.4% of portfolio value. The average return on a tout investment is **−28%**. The mean (median) **120-day holding-period return from the first tout date is −53% (−70%)**. **More than 35%** of tout investors were already penny-stock day traders or frequent short-horizon traders. E-mail touts drew bigger responses than phone or fax. German-headquartered issuers drew the most investors.
- **Discrepancy:** the abstract of the same revision says "470" schemes and "nearly 8% of active investors", while the body says 421 and nearly 6%. I report both. Our RESEARCH.md quotes "about 30%"; the abstract says "average loss of nearly 30%" and the body says −28%.
- **Lead time:** not a detection paper.
- **Relevance (S6):** the best evidence on what client flow into a tout looks like. Victims are **mostly already penny-stock traders**, not first-time small-cap buyers. S6 therefore cannot rely only on "accounts that never bought small caps." The −53% 120-day price path means an alert even weeks into a scheme still prevents losses.

#### A7. Sabherwal, Sarkar & Zhang (2011): Do internet stock message boards influence trading?
- **Citation:** Sanjiv Sabherwal, Salil K. Sarkar & Ying Zhang, "Do Internet Stock Message Boards Influence Trading? Evidence from Heavily Discussed Stocks with No Fundamental News," *Journal of Business Finance & Accounting* 38(9–10):1209–1237 (2011), DOI 10.1111/j.1468-5957.2011.02258.x.
- **Access:** abstract (Crossref). Two numbers are quoted second-hand from Renault (A1).
- **Market & data:** heavily discussed stocks with **no fundamental news** on online message boards (TheLion.com per other sources; **UNVERIFIED**). These are mostly small, financially weak firms.
- **Findings (abstract):** "a **two-day pump followed by a two-day dump**." A credit-weighted sentiment index (not the number of postings) is positively related to same-day return and **negatively predicts returns 1 and 2 days later**. Absolute sentiment is related to a higher share of small trades.
- **Numbers (via Renault, second-hand):** **+13.93%** on the event day, **+4.91%** on the day before, and **−5.4%** over the next five days. Not checked against the original, so **UNVERIFIED in the original**.
- **Relevance:** the "no news + heavy discussion" design is exactly our S1 + S4. It supports weighting **sentiment and hype over raw counts**, and a short 2–5 day memory.

#### A8. Nelson, Price & Rountree (2013): Optimism and credibility of stock spam
- **Citation:** Karen K. Nelson, Richard A. Price & Brian R. Rountree, "Are Individual Investors Influenced by the Optimism and Credibility of Stock Spam Recommendations?" *Journal of Business Finance & Accounting* 40(9–10):1155–1183 (2013), DOI 10.1111/jbfa.12053.
- **Access:** abstract (Crossref).
- **Findings:** returns and volume on spam days are significantly higher when the spam has **optimistic target-price projections** combined with **credible-looking information quoted from an earlier company press release**. Disclaimers reduce the response but do not remove it. Attention effects shape which stocks spammers target and which cases the SEC enforces.
- **Numbers:** **UNVERIFIED**.
- **Relevance:** supports upweighting "target price / PT" phrases in `text.py` (currently 0.4). Also supports a feature for **promo text that quotes the issuer's own PR**, which links S4 and S3.

#### A9. Brüggemann, Kaul, Leuz & Werner (2018): The twilight zone (OTC regulatory regimes)
- **Citation:** Ulf Brüggemann, Aditya Kaul, Christian Leuz & Ingrid M. Werner, "The Twilight Zone: OTC Regulatory Regimes and Market Quality," NBER WP 19358 (2013); *Review of Financial Studies* 31(3):898–942 (2018). https://www.nber.org/papers/w19358
- **Access:** NBER abstract page.
- **Findings:** more than 10,000 US OTC stocks. Firms under stricter regulatory and disclosure regimes have **higher liquidity and lower crash risk**.
- **Numbers:** **UNVERIFIED**.
- **Relevance:** supports a static **prior from tier and disclosure status** (Pink/Expert/non-reporting/delinquent filer) in S3 or as a score multiplier. Not a timing signal.

#### A10. Nam & Skillicorn (2023): Detecting P&D stock manipulation from online forums
- **Citation:** D. Nam & D.B. Skillicorn, "Detecting Pump&Dump Stock Market Manipulation from Online Forums," arXiv:2301.11403 (Jan 2023). https://arxiv.org/abs/2301.11403
- **Access:** full text.
- **Market & data:** Reddit r/pennystocks and r/RobinHoodPennyStocks, 1 Oct 2019 – 28 Jun 2020. 18,555 posts and 312,578 comments, matched to Yahoo Finance prices (Table 1).
- **Method:** a post is labelled P&D if price and volume rise more than **2 SD above a 5-day baseline** after the post and then drop sharply. The models (XGBoost, RF, SVM, MLP, CNN, biLSTM) use only the post text.
- **Performance (Table 7, 5-fold CV):** best model is CNN on posts + comments: accuracy **85.07%**, precision **52.70%**, recall **76.65%**, F1 **62.46%**. MLP on posts alone reaches F1 **67.04% (±12.12)**. Random Forest has high accuracy but recall of only 9–14%. Fewer than 9% of records are positive (Table 6).
- **Lead time:** predicts at post time whether a P&D-shaped price pattern will follow (a horizon of a few days).
- **Limitations:** **labels come from the price pattern, not confirmed fraud**, so a meme rally counts as a "P&D". The large standard deviations mean the results are unstable.
- **Relevance:** the only text-only equities classifier found with full metrics. It shows the precision ceiling of about 50% for text alone, which again supports requiring multiple families.

### B. Crypto pump groups (Telegram/Discord) and detection

#### B1. Kamps & Kleinberg (2018): To the moon
- **Citation:** Josh Kamps & Bennett Kleinberg, "To the moon: defining and detecting cryptocurrency pump-and-dumps," *Crime Science* 7(1), article 18 (2018), DOI 10.1186/s40163-018-0093-5. https://crimesciencejournal.biomedcentral.com/articles/10.1186/s40163-018-0093-5
- **Access:** **abstract-level only, via search-engine summaries.** The open-access PDF redirected to a Springer login. Method details come from descriptions in La Morgia et al. (B4) and Xu & Livshits (B2), both of which I read in full.
- **Method:** anomaly detection that flags a point when **both volume and price exceed thresholds** computed from rolling windows of recent candles, in three configurations: Initial (recall-oriented), Balanced and Strict (precision-oriented). Xu & Livshits note that Kamps et al. found a **12-hour rolling window works better than 24 hours** in crypto.
- **Findings:** suspected P&Ds cluster on particular exchanges and coins. Kamps et al. had no ground truth.
- **Performance (from La Morgia et al. re-implementation on confirmed pumps, TOIT Table 3):** Initial: precision **15.9%**, recall **95.3%**, F1 **27.2%**. Balanced: **38.9% / 93.2% / 54.9%**. Strict: **52.1% / 78.8% / 62.7%**. The ICCCN 2020 version (Table III) gives 15.6/96.7/26.8, 38.4/93.5/54.4 and 50.1/75.0/60.5.
- **Exact window and multiplier values:** **UNVERIFIED**.
- **Relevance:** the closest published analogue of our S1. Used **alone**, it has precision of at most about 50% even on a pump-rich crypto dataset. Equities, with a much lower base rate, would be worse.

#### B2. Xu & Livshits (2019): The anatomy of a cryptocurrency pump-and-dump scheme
- **Citation:** Jiahua Xu & Benjamin Livshits, "The Anatomy of a Cryptocurrency Pump-and-Dump Scheme," *28th USENIX Security Symposium* (2019). https://www.usenix.org/conference/usenixsecurity19/presentation/xu-jiahua (PDF: https://www.usenix.org/system/files/sec19-xu-jiahua_0.pdf). Page range not checked (**UNVERIFIED**; p. 1621 appears in the PDF).
- **Access:** full text.
- **Market & data:** **412** pumps organised in Telegram channels, 17 Jun 2018 – 26 Feb 2019. Hourly OHLCV data. The model focuses on Cryptopia (about 200 pump events with data). In the modelling sample, positives are about 0.3% of coin-hours.
- **Method:** Random Forest and GLM (logit) models on coin features (market cap, listing age, etc.) and on returns, volumes and volatilities in windows ending **1 hour before the pump**. Data are split chronologically into training, validation and test sets.
- **What predicted / lead time:** abnormal returns appear before the coin is announced and are **strongest in the hour before**. On Cryptopia, the pre-pump hourly return sometimes exceeds the in-pump return, a sign of organiser buying. **Market cap and the last-hour return (return1h)** are the two most important features. Short-window features beat long-window ones, and return features beat volume features (Section 5, Fig. 17). **Lead time: about 1 hour.**
- **Performance:** ROC AUC on training data: RF1 **0.948**, RF2 **0.9535**, RF3 **0.9433**; GLMs 0.8794 / 0.7082 / 0.6337 (Fig. 14). On validation: RF **0.9152 / 0.9115 / 0.9109** (Fig. 15). **Test set (Table 3), RF1 at threshold 0.3:** 9 predicted positive, all 9 actual pumps; 51 pumps missed; 18,135 true negatives. That is **precision 100% and recall 9/60 = 15%** (my calculation from Table 3). The trading strategy returned **60%** over about 2.5 months (2.61/4.38).
- **Limitations:** a single exchange (Cryptopia, since closed). The recall at the operating point is very low. The model is tuned for trading profit, not alerting.
- **Relevance:** pre-pump price drift exists but appears **hours, not weeks**, before the pump. A high AUC can coexist with very low recall at a useful precision. Report operating-point precision and recall, not AUC.

#### B3. Hamrick, Rouhi, Mukherjee, Feder, Gandal, Moore & Vasek (2021): The cryptocurrency pump-and-dump ecosystem
- **Citation:** J.T. Hamrick, F. Rouhi, A. Mukherjee, A. Feder, N. Gandal, T. Moore & M. Vasek, "An examination of the cryptocurrency pump-and-dump ecosystem," *Information Processing & Management* 58(4):102506 (2021), DOI 10.1016/j.ipm.2021.102506. Author copy: https://par.nsf.gov/servlets/purl/10251729. Earlier version: "The Economics of Cryptocurrency Pump and Dump Schemes," WEIS 2019 / CEPR DP13404 (https://par.nsf.gov/servlets/purl/10098691).
- **Access:** full text.
- **Data:** **2,469** Telegram pumps and **952** Discord pumps over six months of 2018 (25 Telegram channels, 47 Discord groups), matched to about 2,000 coins on 220 exchanges.
- **Findings:** the median maximum price rise around a pump is **2.4–2.6% for the top-75 coins** versus **14–16% for coins ranked below 1,000**. Overall median (mean) rise is **5.1% (9.8%)** on Telegram and **3.5% (7.4%)** on Discord. The top 10% of pumps rose **16.3%** (Telegram) and **15.6%** (Discord). Transparent pumps had a median return of **7.7%**; obscured pumps had **4.1%**, and only the obscured ones declined over time. Binance and Bittrex hosted **86%** of pumps that named an exchange. Success fell over time.
- **Lead time:** not a detector.
- **Relevance:** **size and obscurity matter**. Pumps of illiquid assets move prices far more, which supports a market-cap/liquidity prior. Highly concentrated channels support a **repeat-offender / known-channel** feature in S5.

#### B4. La Morgia, Mei, Sassi & Stefa (2020 / 2023): Real-time detection
- **Citations:**
  (a) "Pump and Dumps in the Bitcoin Era: Real Time Detection of Cryptocurrency Market Manipulations," *ICCCN 2020*, pp. 1–9, DOI 10.1109/ICCCN49398.2020.9209660, arXiv:2005.06610. https://arxiv.org/abs/2005.06610
  (b) "The Doge of Wall Street: Analysis and Detection of Pump and Dump Cryptocurrency Manipulations," *ACM Transactions on Internet Technology* 23(1):1–28 (2023), DOI 10.1145/3561300, arXiv:2105.00733. https://arxiv.org/abs/2105.00733
- **Access:** full text of both.
- **Data:** (a) more than 100 groups; 343 pumps found on Telegram, 104 modelled. (b) more than 3 years of monitoring, about 900 events (1,108 from 20 groups); **317 Binance pumps** used for the classifier.
- **Method:** Random Forest and AdaBoost on trade-level data split into chunks of *s* seconds within a moving window (best F1 at 25-second chunks and a 7-hour window). The key feature is **"rush orders"**: many market buy orders in the same millisecond.
- **Lead time:** this is **detection after the pump starts, not prediction**: within **25 seconds of the start**. Expected detection time improves from 30 minutes (Kamps) to 25 seconds.
- **Performance:** (b) Table 3, 5-fold CV: RF at 25 seconds has precision **98.2%**, recall **91.2%**, F1 **94.5%**. RF at 5 seconds: **94.6 / 72.9 / 82.4**. AdaBoost at 25 seconds: **95.4 / 90.9 / 93.1**. (a) Table III: RF at 25 seconds (10 folds) **93.1 / 91.4 / 92.0**. Feature importance: StdRushOrders **0.401** in (a), **0.251** in (b).
- **Key quote (b, Section 5):** "detectors based only on the coin price and transaction volume are prone to many false positives."
- **Relevance:** not directly transferable. We do not have exchange order books for OTC, and minutes-scale pumps are a crypto pattern. The equivalent in our data is S6 (many small buy orders from distinct new accounts at the same time). The paper also gives the main evidence against relying on S1 alone.

#### B5. Victor & Hagemann (2019): Quantification and detection
- **Citation:** Friedhelm Victor & Tanja Hagemann, "Cryptocurrency Pump and Dump Schemes: Quantification and Detection," *2019 International Conference on Data Mining Workshops (ICDMW)*, pp. 244–251, DOI 10.1109/ICDMW.2019.00045. https://ieeexplore.ieee.org/abstract/document/8955594
- **Access:** **abstract-level only**, via search-engine summaries of the IEEE abstract (IEEE returned 418) plus descriptions in Clough & Edwards (B9), which I read.
- **Data/findings:** 149 confirmed Telegram-coordinated pumps on Binance. Pumps occur frequently in coins with **market cap below $50 million**, and organisers often coordinate across several channels. An XGBoost classifier trained on these found **612 pump-like events across 172 coins**. According to Clough & Edwards, pumped coins performed about **10% better** than peers over 100 days.
- **Precision/recall/AUC:** **UNVERIFIED** (not seen).
- **Relevance:** supports the small-cap prior and **multi-channel coordination** as the signature behind S5.

#### B6. Nizzoli, Tardelli, Avvenuti, Cresci, Tesconi & Ferrara (2020): Charting online crypto manipulation
- **Citation:** "Charting the Landscape of Online Cryptocurrency Manipulation," *IEEE Access* 8:113230–113245 (2020), DOI 10.1109/ACCESS.2020.3003370, arXiv:2001.10289. https://arxiv.org/abs/2001.10289
- **Access:** full text (arXiv v1).
- **Data:** more than 50M messages from about 7M users on Twitter, Telegram and Discord over 3 months.
- **Method:** snowball crawl of invite links, Botometer-style bot detection, and topic modelling.
- **Findings:** **more than 56%** of Twitter accounts sharing Telegram/Discord invite links were **bots (36.4%) or suspended (19.9%)**. **93% (92.9%)** of invite links posted by Twitter bots point to **Telegram pump-and-dump channels**. 296 P&D channels and 432 Ponzi channels were found, about 20% of the total.
- **Lead time / performance:** no predictive metrics (descriptive study).
- **Relevance (S5):** **invite-link spreading by bot-like accounts** is a strong, cheap coordination feature that can be added beside text near-duplicates.

#### B7. Mirtaheri, Abu-El-Haija, Morstatter, Ver Steeg & Galstyan (2021): Twitter + Telegram pump identification
- **Citation:** "Identifying and Analyzing Cryptocurrency Manipulations in Social Media," *IEEE Transactions on Computational Social Systems* 8(3):607–617 (2021), DOI 10.1109/TCSS.2021.3059286, arXiv:1902.03110. https://arxiv.org/abs/1902.03110
- **Access:** full text (arXiv v2).
- **Data:** 62,850 pump attempts (47,992 pump messages) from 209 Telegram channels covering 543 coins, plus Twitter cashtag streams for about 1,600 cashtags (Table 3).
- **Method:** (i) a TF-IDF + linear SVM pump-message classifier, using Telegram as ground truth; (ii) **Task I:** detect from Twitter and market features alone that a Telegram pump is unfolding; (iii) **Task II:** predict whether the pump will hit its target price within 6 hours. Both use Random Forest on features from the previous *w* hours (w = 15 for Task I).
- **Performance:** message classifier: accuracy **0.879**, precision **0.895**, recall **0.908**, F1 **0.901** (Table 2). **Task I average AUC: Twitter-only 0.73±0.07, economic-only 0.67±0.1, both 0.74±0.08** (Table 5a). **Task II: economic about 0.70 vs Twitter about 0.59**, and adding Twitter features *hurt* (Section 4.3). Bots: **84%** of users who took part in more than 10K pump-related tweets were suspended or had Botometer > 0.55.
- **Lead time:** Task I detects an "unfolding" operation, not a forward forecast.
- **Relevance:** **social features detect that a promotion is happening; market features predict whether it will move the price.** This maps directly to keeping the social family (S4/S5) and market family (S1/S2) separate, and requiring both.

#### B8. Hu, Zhang, Lu, He & Li (2023): Sequence-based target coin prediction
- **Citation:** Sihao Hu, Zhen Zhang, Shengliang Lu, Bingsheng He & Zhao Li, "Sequence-Based Target Coin Prediction for Cryptocurrency Pump-and-Dump," *Proc. ACM Manag. Data (SIGMOD)* 1(1), Article 6 (May 2023), DOI 10.1145/3588686, arXiv:2204.12929. https://arxiv.org/abs/2204.12929
- **Access:** full text (arXiv v2).
- **Data:** **709** Telegram P&D events from 108 channels, 278 coins and 18 exchanges, Jan 2019 – Jan 2022 (Table 2). Binance–BTC subset for modelling.
- **Method:** SNN, which encodes each channel's past pump sequence with positional attention, plus coin and market features. The model ranks all coins on the exchange before the scheduled pump time.
- **Findings:** **the likelihood of a coin being pumped again is 60.1%** (Section 4.1). Pumped coins show intra-channel homogeneity: each channel has a "type". The exchange mix shifted to Binance (62.8% of events).
- **Performance (Table 5, test set):** SNN reaches HR@1 **0.260**, HR@3 **0.383**, HR@5 **0.465**, HR@10 **0.596**, HR@20 **0.727**, HR@30 **0.797**, compared with RF at HR@1 0.189 and HR@10 0.537. Pump-message detector (Table 1): RF AUC **0.994**, precision 0.901, recall 0.939, F1 0.920.
- **Lead time:** before the coin announcement, at a time scheduled in advance. The exact feature cut-off is **UNVERIFIED**.
- **Relevance:** **repeat targeting and per-channel history** are among the best predictors. PumpWatch has no "previously pumped / previously promoted by this group" feature yet. FINRA reports the same repeat-target pattern in equities (C1).

#### B9. Clough & Edwards (2023): Long-term impact of crypto P&D
- **Citation:** Joshua Clough & Matthew Edwards, "Pump, Dump, and then What? The Long-Term Impact of Cryptocurrency Pump-and-Dump Schemes," *2023 APWG eCrime*, pp. 1–17, DOI 10.1109/eCrime61234.2023.10485505, arXiv:2309.06608.
- **Access:** full text.
- **Findings:** 765 coins pumped. The abstract reports an average **30%** relative price drop one year after a pump; the body reports **27%** at 365 days and **more than 25% lower after 90 days**. This contradicts Victor & Hagemann's +10% at 100 days.
- **Relevance:** harm lasts long after the pump. It also makes a **"previously pumped" flag** useful as a long-lived prior.

#### B10. Dhawan & Putniņš (2023): A new wolf in town?
- **Citation:** Anirudh Dhawan & Tālis J. Putniņš, "A New Wolf in Town? Pump-and-Dump Manipulation in Cryptocurrency Markets," *Review of Finance* 27(3):935–975 (2023; online Aug 2022), DOI 10.1093/rof/rfac051. SSRN 3670714.
- **Access:** SSRN abstract via Crossref.
- **Findings:** 355 pumps in 6 months. Pumps cause **average price distortions of 65%**, abnormal volumes in the millions of dollars, and large wealth transfers. Overconfidence and gambling preferences explain why people participate despite negative expected returns.
- **Relevance:** background. The victim psychology here matches the "investment club" pattern in the 2025 equity schemes.

#### B11. Bolz et al. (2025): Real-time ML detection of Telegram P&D (NLP pipeline)
- **Citation:** Manuel Bolz, Kevin Bründler, Liam Kane, Panagiotis Patsias, Liam Tessendorf, Krzysztof M. Gogol, Taehoon Kim & Claudio J. Tessone, "Real-Time Machine Learning Detection of Telegram-Based Pump-and-Dump Schemes," *ACM CCS Workshop on Decentralized Finance and Security* (2025), arXiv:2412.18848 (v2, 29 Sep 2025). https://arxiv.org/abs/2412.18848
- **Access:** full text.
- **Method:** an NLP classifier on Telegram messages that identified 2,079 past pump events, plus a z-score model on order-book and trade features that ranks candidate coins.
- **Performance:** message classifier weighted F1 **0.982**, precision 0.982, recall 0.982. On a Poloniex case study, **the target coin was in the top 5 of 50 random coins in 24/43 events (55.81%)** when run **20 seconds** before the pump; top-10 hit rate 74.42%. Top-5 falls to **41.46%** at 40 seconds (the text says 41.45%) and **19.05% at 1 minute** before.
- **Relevance:** clear quantitative evidence that **predictive skill decays within seconds** for crypto schedule-based pumps. Equity ramp-and-dumps run over days, so our horizon is different. Also an example of an NLP (pre-LLM style) text-classification stage for pump-message detection.

#### B12. Karbalaii (2025): Threshold-based detection with market noise
- **Citation:** Mahya Karbalaii, "Detecting Crypto Pump-and-Dump Schemes: A Thresholding-Based Approach to Handling Market Noise," arXiv:2503.08692 (Feb 2025).
- **Access:** abstract only (PDF downloaded; only the abstract and introduction were read).
- **Findings:** an unsupervised model combining thresholds with EWMA and volatility, aimed at low-liquidity tokens where standard anomaly detectors "often over-flag negligible volume spikes."
- **Numbers:** **UNVERIFIED**.
- **Relevance:** supports adding a **volatility-scaled / EWMA baseline and an absolute dollar-volume floor** to S1, so dormant tickers do not hit 50x on trivial volume.

### C. Regulator and market-operator practice (2022–2026)

#### C1. FINRA 2026 Annual Regulatory Oversight Report: Manipulative Trading (Dec 2025)
- **Citation & URL:** https://www.finra.org/sites/default/files/2025-12/2026-annual-regulatory-oversight-report.pdf (read in full for pp. 19–23), and the web version https://www.finra.org/rules-guidance/guidance/reports/2026-finra-annual-regulatory-oversight-report/manipulative-trading
- **Content (box "Increase in Small-Cap Fraud Involving Exchange-Listed Equities", pp. 21–22):**
  - Schemes now occur "**less frequently at the time of the small-cap issuers' IPOs, and more frequently months after these IPOs. Oftentimes, the same issuer is subject to multiple suspected pump-and-dump schemes.**"
  - Nominee accounts are centrally controlled by one or more bad actors.
  - "In advance of the pump-and-dump scheme, nominee accounts may '**funnel**,' or sell their shares in a coordinated manner to one or more **foreign omnibus accounts**."
  - Some issuers make **privately placed secondary offerings to select foreign investors** without adequate public disclosure.
  - New trend: **account takeover (ATO)**. A bad actor "sells legitimately acquired investments and uses the funds to purchase shares of the subject securities."
  - **Investment-club** scams run by text and social media.
  - Victim purchases happen "through the use of **coordinated limit orders**," and "often coincide with liquidations of shares by accounts presumed to be controlled by foreign bad actors."
  - In October 2025, FINRA opened a targeted exam of offerings by small-cap foreign issuers.
- **Effective practices (p. 22):** monitor accounts referred by the issuer to the underwriter, money movements between issuer and customer accounts, and nominee-controlled pre-IPO raises. Monitor activity across platforms and cross-border.
- **Findings on deficiencies (p. 20):** surveillance thresholds "set too low or too high"; reviews that ignore patterns "across appropriate lengths of time (e.g., several days) or across different customers."
- **Correction to our RESEARCH.md:** I did **not** find the phrase "coordinated social media promotion" in this report. The report talks about social-media and text-message investment-club scams and coordinated limit orders. RESEARCH.md §0.1 should be reworded.
- **Relevance:** the most direct specification for **S6** (ATO pattern, funneling, coordinated limit orders, many customers over several days) and for an **S3 issuer-profile prior** (foreign, small float, months after IPO, repeat target).

#### C2. FINRA Regulatory Notice 22-25: Heightened threat of fraud (17 Nov 2022)
- **URL:** https://www.finra.org/rules-guidance/notices/22-25 (page read).
- **Red flags (quoted):** IPOs typically raised "**less than $25 million**", valued the issuer at "**less than $100 million**", and issued "**fewer than 20 million shares**". Primary operations were often in China. Nominee-account indicators: "similar timing of account opening; similar referral source...; similar customer contact information; similar bank account information; **similar IP addresses**; **similar initial account funding amounts**." Complaints mention "**pig butchering**." Shares are concentrated "in very few hands." Large price rises came on or just after the listing day.
- **2025 notice:** I searched finra.org and found **no 2025 Regulatory Notice specifically on ramp-and-dump**. The 2025 and 2026 Oversight Reports and the investor insights cover it. If the CEO means a specific 2025 notice number, it is **UNVERIFIED / not found**.

#### C3. FINRA investor insight: "This On-Ramp Could Lead You to a Dump" (first published 30 Mar 2023)
- **URL:** https://www.finra.org/investors/insights/ramp-and-dump-schemes (page shows an updated date of 9 Sep 2026).
- **Content:** ramp-and-dump involves "a slower, more deliberate promotion that takes place in peer-to-peer platforms like online forums, chat rooms and social media threads."
- **Relevance:** "slower, more deliberate" promotion suggests a **longer S4 baseline and a multi-day S5 window** for equities than crypto papers use.

#### C4. FBI IC3 PSA250703 (3 Jul 2025)
- **URL:** https://www.ic3.gov/PSA/2025/PSA250703
- **Content:** "at least a **300 percent increase** in victim complaints referencing ramp-and-dump stock fraud from 2024." Stages: social-media ads or messages lead to "investment clubs" on messaging apps, run by people impersonating brokers or analysts, who coordinate buying in a low-priced stock they control. Red flags: unsolicited tips, urgency, "low-priced stocks in new or emerging companies", and requests for account access or screenshots.
- **Relevance:** **S7** (victim reports, including screenshots) matches what the FBI receives. It also confirms that WhatsApp-style closed groups are where the pitch happens, which we cannot see. That is why S6 (broker flow) is more important than S4/S5 for the 2025 wave.

#### C5. SEC v. Constantinescu et al. ("Atlas Trading" influencers), 14 Dec 2022
- **URL:** https://www.sec.gov/newsroom/press-releases/2022-221 (read). A related later case: SEC v. Francis Sabo, Lit. Rel. 25736 (26 May 2023), https://www.sec.gov/litigation/litreleases/lr-25736. Note that the link in our RESEARCH.md points to the Sabo release, not the main Dec 2022 case.
- **Content:** eight influencers on **Twitter and Discord**, about **$100 million** in alleged fraudulent gains, since at least Jan 2020. Mechanics: buy first, then post **price targets** or claims of "buying/holding/adding" to followers, then sell without disclosure.
- **Relevance:** gives S4 lexicon cues ("price target", "adding", "holding"). It also shows that **a small set of repeat influencer accounts across many tickers** is the signature. That supports a cross-ticker promoter-history feature in S5.

#### C6. SEC trading suspensions for social-media manipulation: QMMM Holdings & Smart Digital Group (Sep 2025)
- **Sources:** secondary only. https://www.securitieslawyer101.com/2025/sec-trading-suspensions-of-qmmm-sdm-new-sec-cross-border-task-force/ (read), and a Seeking Alpha headline seen in search results. **I did not open the SEC order**, so the release number is **UNVERIFIED**.
- **Content (secondary):** suspensions ran from 29 Sep 2025 to 10 Oct 2025, citing "potential manipulation through recommendations made to investors by unknown persons via social media." These were reportedly the first SEC trading suspensions since Oct 2024. Both are Cayman holding companies (Singapore and Hong Kong) that IPO'd on Nasdaq Capital Market in 2024 at $4.00. According to the secondary source, QMMM went from about $1 (May–June 2025) to $11 on 8 Sep 2025, and to an intraday high of about $300 on 9 Sep **after announcing a pivot to crypto**. The SEC's Cross-Border Task Force launched on 5 Sep 2025.
- **Relevance:** a live example of **S3 "new business direction / crypto" plus a months-after-IPO small float**. The 8 Sep move (to about $11 from about $1) would have triggered S2 before the 9 Sep spike. This is consistent with S2, but it is a single anecdote.

#### C7. Nasdaq rule changes for small and China-based issuers (2025–2026)
- **Sources:** Harvard Law School Forum summary (9 Nov 2025): https://corpgov.law.harvard.edu/2025/11/09/nasdaq-proposes-stricter-initial-and-continued-listing-standards/ . National Law Review: https://natlawreview.com/article/sec-approves-nasdaqs-25-million-ipo-requirement-china-based-companies . Both read.
- **Content:** filed 3 Sep 2025 (SR-NASDAQ-2025-068 and -069). Proposals: minimum **$15M** market value of unrestricted publicly held shares (MVUPHS) under the net-income standard; **$25M minimum offering proceeds for companies principally operating in China** (Rule 5210(l)); immediate suspension and delisting of non-compliant companies with market value of listed securities **below $5M**. **The SEC approved Rule 5210(l) on 14 May 2026** (NatLawReview). The SEC noted that from **Aug 2022 to Apr 2025 about 70%** of Nasdaq's manipulation referrals to the SEC/FINRA involved Chinese companies, which made up **less than 10%** of listings. Whether the $15M and $5M parts were approved is **UNVERIFIED**.
- **Relevance:** a regulator-backed **issuer prior**: China/HK operations, small float, recent small IPO. New listings under the rule should be less vulnerable, while the **pre-rule cohort (2022–2026 small IPOs) is the at-risk population**.

#### C8. OTC Markets Group: Caveat Emptor and Stock Promotion Policy
- **URL:** https://www.otcmarkets.com/learn/policy-on-stock-promotion (page did not render for me).
- **Content (search-engine summaries only, so all details are UNVERIFIED):** the Caveat Emptor designation (skull and crossbones) can be assigned when OTC Markets learns of promotion that may be misleading or manipulative, including news releases, spam e-mail and newsletters from the issuer or third parties. The policy was established in Dec 2017 per law-firm blogs. Promotion-flag criteria and durations are **UNVERIFIED**.
- **Relevance:** OTC Markets' own **Promotion and Caveat Emptor flags are free, labelled outcome data**. They can serve as backtest ground truth for OTC names and as an S3 input. Licence and terms are **UNVERIFIED**.

### D. LLM/NLP-based detection, 2023–2026
- **What I found:** Bolz et al. 2025 (B11, an NLP Telegram classifier), Nam & Skillicorn 2023 (A10, text-only deep learning on Reddit), and Hu et al. 2023's message classifier (B8). A search for **LLM-based (GPT-class) pump-and-dump detection with reported precision and recall on equities found nothing peer-reviewed.** General LLM papers on influence-campaign and bot detection exist (e.g. arXiv:2311.07816, arXiv:2402.00371), but I saw only their titles in search results and they are **not reviewed here**.
- **Implication:** the reported text classifiers reach **F1 of about 0.90–0.98 at telling pump messages from other messages** (Mirtaheri 0.901, Hu 0.920, Bolz 0.982). Telling whether a message will lead to a P&D price pattern is much weaker (Nam & Skillicorn F1 0.62). An LLM hype scorer in `HypeScorer` is likely to beat our lexicon at message classification, but it **will not solve the "does it move the price" problem**. That still needs the market and client families.

---

## 2. Summary table

| # | Source | Market | Signal family | Lead time vs. pump/peak | Best reported metric (where) | Access |
|---|---|---|---|---|---|---|
| A1 | Renault 2017/18 | OTC, Twitter | Social + promoter identity | Day −1 (+4.10% AR) to day 0 | Promoter events −5.34% vs +0.87% (Tab. 10); 63.46% events with promoter | Full |
| A2 | Frieder & Zittrain 2008 | Pink Sheets, e-mail spam | Social → volume | Days before touting (positive return) | Most-traded probability 4% → 70% on touting days | Abstract |
| A3 | Hanke & Hauser 2008 | US penny, spam | Volume, returns | Same day; effect lasts about 1 day | 1,241 e-mails / 235 stocks; coefficients UNVERIFIED | Abstract + press release |
| A4 | Böhme & Holz 2006 | US, spam | Volume, returns | Short run | UNVERIFIED | Abstract (snippet) |
| A5 | Aggarwal & Wu 2006 | SEC cases | Market, insiders | Prices rise through the manipulation period | UNVERIFIED | Abstract (WP) |
| A6 | Leuz et al. NBER w24083 | Germany, bank clients | Client flow | n/a | −53% mean 120-day return; >35% of victims penny day-traders | Full |
| A7 | Sabherwal et al. 2011 | US message boards | Sentiment, no news | 2-day pump, 2-day dump | +13.93% day 0 (via Renault; UNVERIFIED in original) | Abstract |
| A8 | Nelson et al. 2013 | US spam | Promo content | Spam day | UNVERIFIED | Abstract |
| A9 | Brüggemann et al. 2018 | US OTC | Issuer regime prior | n/a | UNVERIFIED | Abstract |
| A10 | Nam & Skillicorn 2023 | Reddit penny stocks | Text | Post → days | CNN F1 62.46%, precision 52.70% (Tab. 7) | Full |
| B1 | Kamps & Kleinberg 2018 | Crypto | Price + volume anomaly | Within the hour | Strict: precision 52.1%, recall 78.8% (per La Morgia Tab. 3) | Abstract (secondary) |
| B2 | Xu & Livshits 2019 | Crypto, Cryptopia | Pre-pump market | About 1 hour | Validation AUC 0.915; test precision 9/9, recall 9/60 (Tab. 3) | Full |
| B3 | Hamrick et al. 2021 | Crypto, Telegram/Discord | Ecosystem | n/a | Median rise 2.4–2.6% (top-75) vs 14–16% (rank >1000) | Full |
| B4 | La Morgia et al. 2020/23 | Crypto, Binance | Order flow (rush orders) | +25 seconds after start | Precision 98.2%, recall 91.2%, F1 94.5% (TOIT Tab. 3) | Full |
| B5 | Victor & Hagemann 2019 | Crypto, Binance | Market | n/a | 612 pump-like events / 172 coins; metrics UNVERIFIED | Abstract (secondary) |
| B6 | Nizzoli et al. 2020 | Twitter/Telegram/Discord | Bots, invite links | n/a | >56% bots or suspended; 93% of bot links → P&D channels | Full |
| B7 | Mirtaheri et al. 2021 | Twitter + Telegram | Social vs. market | Unfolding (w = 15h history) | AUC 0.74 (both), 0.73 (Twitter) (Tab. 5a) | Full |
| B8 | Hu et al. 2023 | Crypto, Telegram | Channel history | Before scheduled pump | HR@1 0.260, HR@10 0.596 (Tab. 5); 60.1% re-pump | Full |
| B9 | Clough & Edwards 2023 | Crypto | Long-term harm | n/a | −30% (abstract) / −27% (body) at 1 year | Full |
| B10 | Dhawan & Putniņš 2023 | Crypto | Participation | n/a | 65% average price distortion, 355 pumps | Abstract |
| B11 | Bolz et al. 2025 | Crypto, Poloniex | NLP + order book | 20 s → 1 min | Top-5 55.81% at 20 s, 19.05% at 1 min | Full |
| B12 | Karbalaii 2025 | Crypto, Poloniex | EWMA thresholds | n/a | UNVERIFIED | Abstract |
| C1 | FINRA 2026 Oversight Report | US listed small caps | Client flow, issuer | Months after IPO; repeat schemes | Qualitative | Full (pp. 19–23) |
| C2 | FINRA RN 22-25 | US small-cap IPOs | Issuer + nominee accounts | At or after listing | <$25M raised, <$100M value, <20M shares | Page |
| C3 | FINRA ramp-and-dump insight | US | Social | "Slower, more deliberate" | Qualitative | Page |
| C4 | FBI PSA250703 | US | Victims | n/a | ≥300% complaint increase in 2025 vs 2024 | Page |
| C5 | SEC 2022-221 (Atlas) / LR-25736 | US, Twitter/Discord | Influencers | n/a | About $100M alleged gains | Page |
| C6 | SEC suspensions QMMM/SDM 2025 | Nasdaq, foreign | Social + crypto pivot | n/a | Qualitative | Secondary |
| C7 | Nasdaq SR-2025-068/069 | Nasdaq | Issuer prior | n/a | About 70% of referrals involve China-based issuers (<10% of listings) | Secondary (law sites) |
| C8 | OTC Markets promotion policy | OTC | Labels | n/a | UNVERIFIED | Snippet |
| D | LLM/NLP | Mixed | Text | n/a | Message classification F1 0.90–0.98 (B7, B8, B11) | as above |

---

## 3. Recommendations for S1–S7 and thresholds

Each recommendation says **KEEP** or **CHANGE**, gives the evidence, and is marked **GUESS** where no source supports the number.

### S1: Abnormal volume without news (`vol_ratio_trigger = 5`, `vol_ratio_full = 50`, `vol_lookback = 60`, `news_window_days = 1`)
1. **CHANGE the news filter (high priority).** Remove `PR`, `NEWS` and `6-K` from the exculpatory `NEWS_FORMS`, or at least do not let them *cancel* S1 for low-float or foreign issuers. Instead, flag "volume spike + issuer PR / 6-K with no 8-K-grade substance" as a feature. *Evidence:* press releases were the promotion channel in **73.3%** of SEC P&D cases (Renault, A1). Nelson et al. (A8) show spam quoting the issuer's own PR moves prices most. The 2025 targets are foreign private issuers that file 6-Ks (C1, C2, C6).
2. **KEEP the 5x trigger for now (GUESS), but add an absolute dollar-volume floor and a volatility-scaled baseline.** *Evidence:* there is no equities paper that calibrates a volume multiple. Crypto detectors using only price and volume reach precision of just **15.9–52.1%** (La Morgia's re-run of Kamps, B1/B4). Low-liquidity series over-flag trivial spikes (Karbalaii, B12). Liquidity determines spam success (Hanke & Hauser, A3). Floor value: **GUESS** of about $250k/day of dollar volume, to be calibrated in the backtest.
3. **CHANGE: also compute S1 as a z-score** (for example log dollar volume against the 60-day mean and SD) alongside the ratio. *Evidence:* Renault and Nam & Skillicorn both use **mean + 2 SD** event definitions (A1, A10). The cut-off is copied from them, not tuned for volume, so treat it as a **GUESS** for volume.
4. **KEEP S1 as a necessary-but-not-sufficient signal**, never alerting alone. Already enforced by `min_families = 2`. *Evidence:* B4 quote; Mirtaheri: market features predict pump *success* (AUC about 0.70) better than social features (B7).

### S2: Quiet accumulation (`acc_window = 20`, `+30%`, `55% up days`, `1.5x volume`, `max single day 25%`)
1. **CHANGE: add a short-horizon pre-promotion run-up (1–3 sessions)** as a second S2 variant, for example abnormal return over [−2, −1] above X% before an S4/S5 hit (X is a **GUESS**, say 5–10% for small caps). *Evidence:* equity run-ups before promotion appear about **1 day** before the spike (+4.10% on day −1, Renault A1; +4.91% on day −1, Sabherwal via Renault A7; "positive return on days prior to heavy touting", Frieder & Zittrain A2). In crypto the run-up is concentrated in the **last hour** (Xu & Livshits B2).
2. **KEEP the 20-day version but down-weight it** (weight 0.10 → 0.05, **GUESS**). *Evidence:* **no paper I read documents a 20-day, +30% "quiet accumulation" price signature.** Aggarwal & Wu (A5) say prices "rise throughout the manipulation period" but give no window (UNVERIFIED). The QMMM anecdote (C6) is consistent with S2 but is a single case.
3. **CHANGE (new signal or S2 feature): a "previously pumped / repeat target" prior.** *Evidence:* a coin's chance of being pumped again is **60.1%** (Hu et al. B8). FINRA: "the same issuer is subject to multiple suspected pump-and-dump schemes" (C1). Harm lasts (−27 to −30% at 1 year, B9). Implement as a decaying memory of past PumpWatch alerts, SEC suspensions or OTC Caveat Emptor flags on the same ticker.

### S3: Suspicious filings (dilution forms, name change, change of control, custodianship, dormant > 365d)
1. **KEEP the existing items.** *Evidence:* insiders and control persons are typical manipulators (Aggarwal & Wu A5). Insiders were involved in **60.7%** and paid promoters in **49.3%** of SEC P&D complaints (Renault A1, p. 6).
2. **CHANGE: add an issuer-profile prior for the ramp-and-dump population.** Features: IPO raised < $25M, valuation < $100M, fewer than 20M IPO shares (FINRA RN 22-25, C2); principal operations in China/HK (Nasdaq: about **70%** of manipulation referrals, C7); **months after IPO** (FINRA 2026, C1); private placement to foreign investors after the IPO (C1). Pull these from the F-1/424B prospectus already in `DILUTION_FORMS`.
3. **CHANGE: add "business pivot to crypto / AI" press releases or 6-Ks as a red flag even when they are not filings.** The existing `RED_FLAG_TITLE_WORDS` already lists crypto and AI. Make sure they are matched against PR/6-K titles, not only EDGAR form titles. *Evidence:* the QMMM crypto-pivot announcement came just before its spike (C6, secondary).
4. **CHANGE: add OTC tier and disclosure status (Pink, Expert, non-reporting, delinquent) and OTC Markets Promotion / Caveat Emptor flags** as priors. *Evidence:* Brüggemann et al. (A9): weaker regimes have lower liquidity and higher crash risk. The OTC Markets policy (C8, UNVERIFIED details).

### S4: Hype burst (`>= 5 mentions/day`, `>= 5x 30-day mean`, `avg hype >= 0.35`)
1. **CHANGE the burst rule to `mentions > mean + 2·SD of baseline` AND `mentions >= 20` for Twitter/X**, keeping a lower floor (5) only for small closed-source channels such as a single Telegram group. *Evidence:* Renault's event definition (A1): yearly mean + 2 SD, at least 20 tweets, with 10 posts as the floor in the older message-board studies. With a 30-day baseline, `5x mean` can fire on tiny numbers.
2. **CHANGE: lengthen `mention_baseline_days` from 30 to about 90–250** (**GUESS** within the range in the literature; Renault uses the yearly average). This stops a slow ramp from pulling the baseline up. *Evidence:* FINRA describes ramp-and-dump promotion as "slower, more deliberate" (C3).
3. **CHANGE: add a promoter-identity component** (known paid promoters, accounts with promo-site links in their bio, pump-tracker accounts). *Evidence:* promoters were in **63.46%** of events, and only promoter/tracker events reverse (**−5.34% vs +0.87%**, A1). Pump-tracker accounts are themselves a useful external alert source.
4. **KEEP `hype_min_avg = 0.35` (GUESS), but upweight "target price / PT / price target", "adding/holding" and quoted-press-release text.** *Evidence:* Nelson et al. (A8); SEC Atlas complaint mechanics (C5); Sabherwal: sentiment, not post count, predicts reversals (A7).
5. **PLAN: swap the lexicon for an LLM or fine-tuned classifier behind `HypeScorer`**, but evaluate it on *message-level* labels. *Evidence:* message-level F1 of 0.90–0.98 is achievable (B7, B8, B11), but text alone predicting a P&D price outcome reaches only F1 about 0.62 (A10).

### S5: Coordinated promotion (Jaccard ≥ 0.6 on 4-word shingles, ≥ 3 distinct authors in 3 days)
1. **KEEP the near-duplicate test; the thresholds are a GUESS.** *Evidence:* **I found no published Jaccard or shingle threshold for stock-promo text.** Calibrate on labelled campaigns: SEC complaints quote promo text, and OTC Markets promotion flags give positives.
2. **CHANGE: extend `coord_window_days` from 3 to 5–7** (**GUESS**). *Evidence:* spam campaigns average about 5 days per stock, and repeating spam on successive days sustains demand (Hanke & Hauser A3). Ramp-and-dump promotion is "slower" (C3).
3. **CHANGE: add two cheap coordination features:** (a) **invite-link spreading** (t.me, discord.gg, WhatsApp links) by many accounts mentioning the same cashtag; (b) an **account-quality / bot score** (account age, suspended status). *Evidence:* more than 56% of accounts sharing invite links were bots or suspended, and 93% of bot invite links led to P&D channels (Nizzoli B6). 84% of the most active pump participants were bots or suspended (Mirtaheri B7).
4. **CHANGE: add a cross-ticker repeat-promoter graph** (the same authors or clusters promoting many unrelated small caps over months). *Evidence:* pump channels are concentrated (Hamrick B3). Channel history predicts the target (Hu B8). In the Atlas case, a small group of influencers pushed many tickers (C5).

### S6: Broker flow (`>= 20 new buyers`, `5x`)
1. **CHANGE the definition of "suspicious buyer" (high priority).** Count buyers whose holding in the ticker is new, **including experienced penny-stock traders**, not only first-time small-cap buyers. *Evidence:* **more than 35%** of tout investors were already penny-stock day traders or frequent traders (Leuz A6).
2. **CHANGE: add the ATO pattern.** Flag existing accounts that **sell diversified long-held positions and put the proceeds into a single low-float ticker** within a short time. *Evidence:* FINRA 2026 (C1) describes exactly this new trend.
3. **CHANGE: add nominee-cluster features** for brokers that share KYC metadata: accounts opened around the same time with the same IP, bank, funding amount or referral source that trade the same ticker. *Evidence:* FINRA RN 22-25 (C2) lists these indicators verbatim.
4. **CHANGE: add order-style features:** many small **limit** buy orders at similar prices or times from distinct accounts. This is the equities equivalent of crypto "rush orders". *Evidence:* "coordinated limit orders" (FINRA C1); rush orders were the top feature in La Morgia (importance 0.401 / 0.251, B4).
5. **KEEP `flow_min_new_buyers = 20` and 5x as a GUESS.** Leuz's 2%-per-year participation base rate (A6) suggests that even a mid-sized broker sees only a handful of buyers per tout. This needs calibration per broker size, ideally as a ratio to the broker's active small-cap trader count.

### S7: Victim reports (14 days)
1. **KEEP the weight low (0.05) and the 14-day window (GUESS).** Victim reports arrive at or after the dump, so they add little lead time. *Evidence:* FBI PSA (C4) and FINRA "pig butchering" complaints (C2) are all after the fact.
2. **CHANGE its main role: use S7 as a training and backtest label source and a "confirm" signal**, not mainly as a predictor. Reports on one ticker should also raise the repeat-target prior (S2 recommendation 3) for future episodes.

### Scoring, memory and alerting
1. **KEEP `min_families = 2`.** *Evidence:* single-family detectors have low precision (price/volume only: at most 52.1% precision, B1/B4; text only: 52.7%, A10). Social signals detect promotion while market signals predict impact (B7).
2. **KEEP `signal_memory_days = 5`.** *Evidence:* the reversal plays out over days [+1,+5] (A1) and in a 2-day pump plus 2-day dump (A7), so hits more than 5 days apart are rarely the same episode in equities.
3. **CHANGE `cooldown_days` from 10 to about 20 trading days** (**GUESS**, copied from Renault's 20-trading-day spacing between events, A1). Also allow **re-alerts on the same issuer months later**, since repeat schemes are documented (C1, B8).
4. **CHANGE the evaluation protocol:** report precision and recall at the operating threshold and lead time in days relative to the price peak, not AUC. *Evidence:* Xu & Livshits had AUC of about 0.92 yet only 15% test recall at their chosen threshold (B2).

---

## 4. Gaps: what the literature does NOT tell us

1. **No peer-reviewed, out-of-sample equity P&D *early-warning* detector with confirmed-fraud labels** was found. Equity studies are event studies (A1–A9) or use price-pattern labels (A10). Our H3 (≥50% caught ≥2 days before collapse) and H4 (≤5 false positives per true positive) have **no published benchmark** to compare against.
2. **No academic study of the 2024–2026 ramp-and-dump wave** (foreign small-cap Nasdaq/NYSE American IPOs) was found. Evidence for it is regulator text and press only (C1–C7).
3. **No calibrated thresholds** for volume multiples on OTC or small-float listed stocks, for near-duplicate text similarity, or for broker-flow counts. Every such number in `config.py` is still a guess.
4. **Lead time for equities is thin.** The best evidence (A1, A7) puts detectable signs about 1 day before the spike. Whether 2–3 days' warning before the *dump* is realistic is unknown. Leuz's −53% 120-day path (A6) suggests that alerts after the spike still have value.
5. **Closed channels (WhatsApp, private Telegram "VIP" groups)**, where the 2025 investment-club pitch happens (C4), are not studied in any detection paper. Crypto Telegram studies (B2–B8, B11) cover *public* channels and the minutes-scale pump format.
6. **Broker-side evidence comes from one source:** a single German bank, 2002–2015 (A6). Nothing published covers US retail apps, ATO-driven buying, or nominee clusters quantitatively.
7. **Base rates:** the share of small-cap volume spikes that are manipulations is unknown, so expected false-positive rates cannot be derived from the literature.
8. **Hebrew / Israeli channels:** nothing found.
9. **LLM-based detection:** no peer-reviewed equity-specific evaluation found (Section D).

---

## 5. List of UNVERIFIED items

- Frieder & Zittrain: sample size, period and exact pre-touting window (abstract only).
- Hanke & Hauser: coefficient and effect sizes (abstract and press release only).
- Böhme & Holz: all numbers (abstract seen only via search snippet).
- Aggarwal & Wu: sample size, period and effect sizes.
- Sabherwal et al.: +13.93% / +4.91% / −5.4% (seen only as quoted by Renault); the TheLion.com data source.
- Nelson, Price & Rountree: effect sizes.
- Brüggemann et al.: effect sizes.
- Kamps & Kleinberg: exact window, multiplier values and detection counts. The paper's own text was not read; method and metrics come from La Morgia et al. and Xu & Livshits.
- Victor & Hagemann: classifier precision, recall and AUC; the abstract was seen only via secondary summaries.
- Xu & Livshits: proceedings page range.
- Hu et al.: exact feature cut-off before the scheduled pump.
- Karbalaii 2025: all metrics.
- SEC QMMM/SDM suspension: SEC release number and the SEC's own wording (secondary source only).
- Nasdaq: whether the $15M MVUPHS and <$5M MVLS accelerated-delisting parts were approved (only Rule 5210(l) approval on 14 May 2026 was confirmed via NatLawReview).
- OTC Markets Promotion / Caveat Emptor criteria and timing (page did not render; snippets only).
- A FINRA *2025* Regulatory Notice specifically on ramp-and-dump: **not found**. Only RN 22-25 (2022) and the 2025/2026 Oversight Reports exist as far as I could see.
- RESEARCH.md's statement that FINRA's 2026 report asks to monitor "coordinated social-media promotion": **not found verbatim** in the report text.
