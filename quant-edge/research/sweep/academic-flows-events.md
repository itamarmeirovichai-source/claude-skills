# Department B sweep — Academic Scout, lanes 1–2 (structural flows with a calendar; scheduled information outside ES/NQ)

- scout: Academic Scout (Department B, Market Intelligence)
- date: 2026-11-03 (citation fetch date for every URL below unless stated)
- lanes: 1 (structural flows with a calendar), 2 (scheduled information outside ES/NQ)
- method: start from pre-sweep `~/quant-edge-inherited/pr26/prompts/research/lit-academic.md` (cited as pre-sweep A-xx) and `lit-practitioner.md` (P-xx), extend via arXiv q-fin, journal pages, NBER, author pages, Semantic Scholar / Google Scholar snippets. SSRN is blocked (403) — "abstract only" is stated where that is all that was seen.
- status: file written incrementally; candidate blocks appended as found. Summary table and blocked-host list at the end.
- honesty note: most candidates below are plausibility "low" for net Sharpe ≥ 1.5 on a single sleeve; they are listed as pre-registration material for breadth, not as edges.

## Candidate blocks

Cost conventions used below (approximate, Nov-2026 price levels; 1 tick + exchange/commission per side, market orders): ES RT ≈ 1.2 bp; ZN RT ≈ 3 bp (tick 1/64 = $15.6 on ≈ $111k); ZB/UB RT ≈ 5–6 bp (tick 1/32 = $31.25 on ≈ $115–120k); 6E RT ≈ 1.2 bp; 6J RT ≈ 1.5–2 bp; 6A RT ≈ 1.8 bp; CL RT ≈ 4 bp; NG RT ≈ 7 bp; GC RT ≈ 0.6–1 bp; SI RT ≈ 2 bp; ZC RT ≈ 12 bp; ZS RT ≈ 5 bp; LE RT ≈ 2.5 bp; HE RT ≈ 6 bp; RTY RT ≈ 1 bp. Economics screen = gross edge per trade ≥ max(2 ticks, 2 × RT) unless hundreds of trades/yr with win rate > 58%. All Databento prices from the common brief (1m RTH ≈ $6–7/root, full session ≈ $20/root, 1h ≈ $1, 1d ≈ $0.05; ceiling $94).

### C-1-01 Month-end Treasury index-extension strike trade, captured across the futures-firm day boundary (extends pre-sweep A-C09)
- mechanism: Bloomberg bond indices add the month's new issues and extend duration at the month-end strike (4pm ET since 2021-01-14, 3pm before); passive funds, insurers and index-benchmarked dealers buy into the strike. NY Fed interdealer cash data: the 10 minutes around 4pm carried 20.4% of last-trading-day volume in 2025 (11.6% in 2021; 2.5% → 3.5% on normal days 2021 → 2025); the 3:45–4:15pm half hour > 25% of month-end volume, half of that in 3:55–4:00; total month-end volume ≈ 46–58% above normal, an effect "essentially nonexistent" before 2015 and growing since, while Treasury ETF assets grew > 10x 2013–2024; month-end liquidity is better, not worse (price impact −28%, depth +15%). Hartley–Schwarz (cash, 1990–2018): ≈ 20–25 bp/month at 10y concentrated in the last days, last-days-only long Sharpe ≈ 1 after costs, 2015–2018 smaller but significant. Allocate Smartly TLT replication (1999–2019): last three trading days +0.13%/day vs +0.01% other days, 58% vs 52% up-days, with the EOM-2 bias migrating one day earlier after ≈ 2014 (pre-emption already visible). Survival: mechanical, growing with passive share; decay channel = pre-positioning.
- evidence: working paper (Hartley & Schwarz 2019, numbers per pre-sweep A-C09; still unpublished per search 2026-11-03, https://www.kristaschwarz.com/EOM.pdf not re-fetched) + central-bank blogs with data (Dyer, Fleming & Shachar, "Treasury Trading at the Close", NY Fed Liberty Street, Sept 2026, https://libertystreeteconomics.newyorkfed.org/2026/09/treasury-trading-at-the-close/, fetched 2026-11-03; Fleming et al., "End-of-Month Liquidity in the Treasury Market", Sept 2024, https://libertystreeteconomics.newyorkfed.org/2024/09/end-of-month-liquidity-in-the-treasury-market/, fetched 2026-11-03) + blog replication, no code (Allocate Smartly, 2019-10-24, https://allocatesmartly.com/predictable-end-of-month-treasury-etf-returns/, fetched 2026-11-03). Post-2015 OOS: 2015–2018 "smaller but significant" (cash); volume facts to 2025; no post-2019 return figure found anywhere.
- instruments: ZN, ZB, UB (TN, ZF secondary). FTMO: no Treasury CFD found (verify symbol list).
- holding period and expected trades per year: variant A (= A-C09): long 14:00 → 16:05 ET on the last trading day, 12/yr. Variant B (new): overnight-session holds entered 18:00 ET on T-3, T-2, T-1 evenings and exited at 16:05 ET the next day (re-entered each evening), so most of each 24h return of the documented "last three days" sits inside one firm trading day: ≈ 36 holds/yr.
- data needed: Databento GLBX.MDP3 ohlcv-1m ZN and UB full session 2010-06 → 2026 (≈ $20 per root, ≈ $40); 1h bars ($1/root) suffice for a first pass of variant B; SIFMA early-close calendar (free). Cost inside plan.
- expected gross edge per trade: cash evidence ≈ 5–10 bp per last-day session at 10y and 2–3x that in UB; ZN RT ≈ 3 bp, UB RT ≈ 5–6 bp → passes the screen in UB/ZB if ≥ 50% of the cash effect reaches futures (unmeasured); marginal in ZN; 2× costs still positive only for UB. 12–36 events/yr → a sleeve, never the account.
- firm structure fit: intraday futures (A) and overnight-session futures (B: 18:00 ET entry, flat 16:05 ET, inside Topstep's 16:08 ET auto-flatten, MFFU 16:10, Lucid/Tradeify 16:45); consistency rules touched (P&L concentrated in 12 days/yr); no news windows involved.
- nearest closed relative: H0023 (S&P turn-of-month) — different asset, window and mechanism; pre-sweep A-C09 (variant A) not yet registered.
- decay haircut: 0.5 (A, published cash result) / 0.7 (B); splits at 2015-01 (month-end volume regime), 2021-01-14 (3pm → 4pm strike), 2022-03 (hiking cycle).
- plausibility of net Sharpe ≥ 1.5: low-medium — the best mechanism in the lane, but 12–36 events/yr, visible pre-emption, and futures transmission never measured; honest role is one of ≥ 5 sleeves.
- original: yes (variant B: day-boundary capture of the multi-day effect)

### C-1-02 Month-end cross-asset rebalancing pressure, bond leg only (Harvey–Mazzoleni–Melone 2025)
- mechanism: Pension and balanced funds rebalance to 60/40 on the last business day (calendar rule) or when drift exceeds a threshold; when stocks have outperformed bonds month/quarter-to-date they sell equity exposure and buy duration. Paper (S&P 500 and 10y note futures, daily, 1997-09-10 → 2023-03-17): a 1-sd signal lowers next-day equity returns by ≈ 17 bp and raises bond returns ≈ 3 bp; calendar predictability concentrates in the last four days of the month ("funds attempt to minimize market impact by avoiding trades on the very last" day), strengthens toward quarter-ends, became significant in the early 2000s; their cross-asset front-running portfolio (long ES/short ZN or the reverse) earns ≈ 9.9% p.a., Sharpe > 1 (≈ 0.9–1.0 net of their cost estimate) and pensions interviewed "know about that". We trade only the ZN/UB leg (the ES leg is a closed family) on the last four business days.
- evidence: working paper (Harvey, Mazzoleni & Melone, "The Unintended Consequences of Rebalancing", NBER WP 33554, March 2025, https://www.nber.org/system/files/working_papers/w33554/revisions/w33554.rev0.pdf, fetched 2026-11-03, abstract p.1, pp. 3, 19–21, Table 7) + blog replication with code (Quantitativo, https://www.quantitativo.com/p/the-unintended-consequences-of-rebalancing, fetched 2026-11-03: combined signal Sharpe 0.94 gross, no costs, no OOS split). Post-2015 OOS: not reported separately (in-sample to 2023-03).
- instruments: ZN (primary), ZB/UB (duration-scaled); ES leg excluded; FTMO: none.
- holding period and expected trades per year: when |signal| > 1 sd, enter at 18:00 ET on each of the last four business days, exit 15:00 ET next day (16:05 on the last day): ≈ 20–30 holds/yr; the paper's effect is close-to-close, so an intraday-only variant captures less.
- data needed: daily ES and ZN for the signal (free: Stooq/Yahoo continuous, or Databento 1d ≈ $0.05/root); ZN/UB 1h or 1m for execution (shared with C-1-01). ≈ $0–20.
- expected gross edge per trade: ≈ 3 bp on ZN per 1-sd day; perhaps 5–8 bp at quarter-ends with > 2-sd signals; ZN RT ≈ 3 bp → FAILS the economics screen for ZN; UB (≈ 2.5x duration → 7–20 bp vs RT ≈ 5–6 bp) at |signal| > 2 sd is the only registrable variant.
- firm structure fit: overnight-session futures (18:00 ET → next-day 15:00/16:05 ET); consistency rules touched (quarter-end clustering); no news windows.
- nearest closed relative: H0023 (turn-of-month S&P, FTMO Swing) — same calendar, different asset and sign logic.
- decay haircut: 0.5 (published 2025; front-running acknowledged by market participants in the paper); splits at 2008-12, 2020-03, 2025-03 (publication).
- plausibility of net Sharpe ≥ 1.5: low — the documented bond-leg pressure is about one ZN tick; only the quarter-end, long-duration subset can clear 2× costs.
- original: yes (bond-only leg in the long-duration contract, firm-day execution window)

### C-1-03 Treasury auction-day inverted V in ZN/ZB/UB: pre-auction concession and post-result recovery (extends pre-sweep A-C10 with 2026 evidence)
- mechanism: Dealers absorbing a known supply shock sell/hedge in the hours before the 13:00 ET bidding deadline and buy back after results; net order flow transmits the pressure. Fleming–Liu–Nguyen (1-minute interdealer cash data, 1991–2024, 1,684 auctions): six-hour-window yield pressure 0.7–1.2 bp (pre-auction run-up 0.36–0.63 bp, post-auction reversal −0.28 to −0.77 bp), price-based pressure 1.3 bp (2y) to > 17 bp (30y) full sample; sub-periods 0.7–1.4 bp (1991–2006), 0.9–1.8 (2007–2014), 0.3–0.9 (2015–2024, significant decline, pooled); larger when dealer constraints are tighter, smaller when investment-fund demand is stronger/more elastic (funds now take ≈ 70% of awards). Smales (ZN 15-minute bars 2000–2017): prices move higher in the interval right after the auction, more with higher bid-to-cover, read as dealers buying back short futures hedges. Somogyi–Wallen–Xu (HBS 2025): before 2010 long yields fell ≈ 1.5 bp after auctions (daily); after 2010 "yields no longer fall after auctions". Survival: mechanical, ≈ 100 coupon auctions/yr; decay already documented.
- evidence: central-bank staff report (Fleming, Liu & Nguyen, "Intraday Price Pressure and Order Flow Around U.S. Treasury Auctions", FRBNY Staff Report 1188, March 2026 rev. Oct 2026, https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1188.pdf, fetched 2026-11-03, abstract and pp. 19–22, Tables 2–3) + peer-reviewed (Smales, Accounting & Finance 61(S1) 2021 1517–1555, abstract via https://research-repository.uwa.edu.au/en/publications/the-effect-of-treasury-auctions-on-10-year-treasury-note-futures/, search snippet 2026-11-03; Wiley page blocked; Sigaux, "Trading ahead of treasury auctions", JBF 158 (2024) 107032, abstract via https://ideas.repec.org/p/ecb/ecbwps/20182208.html, 2026-11-03) + working paper (Somogyi, Wallen & Xu, HBS WP 26-033, Dec 2025, https://www.hbs.edu/ris/Publication%20Files/26-033_9bebc98f-09f9-4485-aae6-972388865b19.pdf, fetched 2026-11-03, abstract) + CFTC/Fed (Mixon & Tuzun 2018, https://www.cftc.gov/sites/default/files/2019-03/201809%20Mixon%20Tuzun%20-%20ada.pdf, fetched 2026-11-03: dealer inventories move the curve; price discovery in the level sits in non-dealer ZN futures flow). Post-2015 OOS: yes, weakest sub-period (0.3–0.9 bp yield over six hours).
- instruments: ZN (3y/7y/10y auctions), ZB/UB (20y/30y), ZF (5y), ZT (2y); FTMO none.
- holding period and expected trades per year: leg 1 short the auctioned tenor's contract 09:00 → 12:59 ET; leg 2 long 13:11 → 15:00 ET (10-minute buffer as in the paper's robustness check); ≈ 100–200 trades/yr; conditioning: VIX tercile and bid-to-cover sign.
- data needed: Databento 1m ZN and UB RTH 2010–2026 (≈ $7 each; full-session files shared with C-1-01 cover it); TreasuryDirect auction calendar/results incl. bid-to-cover and tail (free); VIX daily (free).
- expected gross edge per trade: post-2014 total pressure 0.3–0.9 bp of yield ≈ 2–6 bp price in ZN (duration ≈ 7) and 5–15 bp in UB (duration ≈ 17), about half per leg → FAILS the screen for ZN (edge ≤ RT ≈ 3 bp per leg) and is marginal for UB unless conditioned on tight-dealer/high-VIX days where the paper shows larger pressure. Win rate unknown.
- firm structure fit: intraday futures (both legs inside 09:00–15:00 ET); auction results (13:01 ET) are not on firm Tier-1 news lists (verify MFFU/Lucid lists); minimum-hold rules irrelevant.
- nearest closed relative: none (E2 macro family is ES/NQ only); pre-sweep A-C10.
- decay haircut: 0.5; splits at 2007, 2015 (regulatory implementation per the paper), 2020-03.
- plausibility of net Sharpe ≥ 1.5: low — real and repeated, but the 2015–2024 magnitude is ≈ one ZN tick per leg; one registered row for the conditioned long-duration version only.
- original: no (new evidence; UB/conditioning twist is incremental)

### C-1-04 WMR 4pm London fix legs with month-end / MSCI-date amplification in 6E/6B/6A/6J (extends pre-sweep A-C06)
- mechanism: Unconditional USD demand at benchmark fixes (passive funds, custodians, corporates) is pre-hedged by capital-constrained dealers. Krohn–Mueller–Whelan (G9, 1999–2019, 5-min spot): the equal-weight foreign-currency portfolio depreciates 4.2% p.a. from the European open to the ECB fix and appreciates ≈ 4.6% p.a. from the London fix to the New York close; post-London reversal ≈ 2.5 bp/day at median VIX; gross reversal strategies 12–15.6% p.a. for EUR/GBP/CHF, negative after full indicative spreads, +2.65% / +0.51% / +2.73% p.a. (EUR/GBP/JPY) with Sharpe 0.12–1.03 at half spreads; the authors: returns "in a relatively small window around the fix are usually more than offset by transaction costs", while multi-hour drift legs may survive for traders with good spreads; 2014–2019 sub-period: pre-ECB leg ≈ 5% p.a. and significant, post-London leg weaker than 1999–2014. Ito–Yamada (JIMF 2018): after the Feb-2015 reform the fixing-window volume spike disappeared but "the anomalies on price dynamics reported in the previous literature still exist", and banks' passive execution "generates another predictability". Melvin–Prins: 16:00 GMT activity peaks at month-ends, more at quarter-ends, most at year-ends (passive hedge resets); FSB 2014: fix volume ≥ 10x typical, passive funds use WMR to minimise tracking error. New conditioning: month-end, quarter-end and MSCI SAIR effective dates (last business day of Feb/May/Aug/Nov) as intensity flags with the equity-hedging sign.
- evidence: peer-reviewed (Krohn, Mueller & Whelan, JF 79(1) 2024 541–578; staff WP version https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf, fetched 2026-11-03, pp. 1–3, Table II, Table VII, Table IX text pp. 34–35; Ito & Yamada, JIMF 80 (2018) 75–95, abstract via https://www.nber.org/papers/w23327, 2026-11-03; Melvin & Prins JFM 2015, workshop version https://www.ecb.europa.eu/events/pdf/conferences/131216/Third_FX_Workshop_MELVIN_PRINS_Equity%20hedging%20and%20exchange%20rates%20Nov%202013.pdf, search snippet 2026-11-03) + regulator (FSB, FX Benchmarks Final Report 2014, https://www.fsb.org/uploads/r_140930.pdf, search snippet 2026-11-03). Post-2015 OOS: KMW 2014–2019 sub-period as above; no post-2019 figure.
- instruments: 6E, 6B, 6A, 6J, 6C (CME); FTMO EURUSD/GBPUSD/AUDUSD.
- holding period and expected trades per year: leg A long USD 02:00 → 08:15 ET (pre-ECB fix; KMW's most robust leg); leg B short USD 11:00 → 16:05 ET; daily (≈ 250/yr per pair) or intensity-only (≈ 16 days/yr: month-ends incl. the 4 MSCI dates and quarter-ends) with direction = −sign(local equity index MTD return).
- data needed: Databento 1m full session for two roots (6E, 6A; ≈ $40) or HistData 1m spot (free) for the first pass; DST-correct London/Frankfurt clocks; MSCI review calendar (free); country-index MTD returns via ETF prices (free).
- expected gross edge per trade: ≈ 1.5–2 bp/day per leg (4–5% p.a. / 250) vs 6E RT ≈ 1.2 bp → FAILS the screen for daily legs (edge < 2 × RT); intensity days 10–25 bp (ITG/FCA figures in A-C06) vs 1.2 bp → passes, n ≈ 16/yr.
- firm structure fit: intraday futures (leg A fully inside; leg B exits 16:05 ET for Topstep); FTMO intraday CFD (no swap) or Swing; news windows: leg A crosses 08:30 ET releases only if extended, keep the 08:15 exit.
- nearest closed relative: D2 (daily FX trend/carry) and D4 (intraday technical rules on CFDs) — not fix-anchored; negative row "FX intraday momentum 6E/6B/6J" is a different mechanism.
- decay haircut: 0.5; splits at 2015-02-15 (5-minute window), 2018-01 (MiFID II), 2020-03.
- plausibility of net Sharpe ≥ 1.5: low for the daily legs (sub-cost by the authors' own accounting), low-medium for the intensity subset as a sleeve.
- original: yes only for the MSCI/quarter-end intensity conditioning (base legs are published, A-C06); count as 0.5 original

### C-1-05 Tokyo 9:55 fix in 6J: pre-fix USD bid and post-fix reversal (extends A-C07 / P-C12 with KMW magnitudes)
- mechanism: Japanese importers' USD purchases are filled at the 9:55 JST fix; banks pre-hedge from the New York close. KMW: the foreign-currency portfolio depreciates 5.0% p.a. from 17:00 ET to the fix (USD up → short 6J) and appreciates 5.3% p.a. afterwards (long 6J); Tokyo-reversal returns positive in 70–83% of months; gross annualized reversal 6.2% (CHF) to 14.2% (NZD), JPY 12.0% gross, ≈ 2.7% at half spreads; "returns around the Tokyo fix have been around 5% or below since 2013", 2014–2019 "notably smaller but remains statistically significant"; at half spreads the JPY version roughly doubled $1 over 1999–2019 and is flat since 2013. Ito–Yamada 2017: gotobi-day intensity; Krueger forward test (P-C12) running since Sept 2026.
- evidence: peer-reviewed (KMW JF 2024, SWP pp. 1–3, 33–35, https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf, fetched 2026-11-03; Ito & Yamada JIE 2017 per A-C07) + blog with pre-registered forward test (Krueger, P-C12). Post-2015 OOS: KMW sub-period 2014–2019 smaller/significant; Krueger 2023–26 +4.5–5.6 bp/trade before global correction.
- instruments: 6J, M6J (window 17:00–02:00 ET sits in the overnight session); FTMO USDJPY.
- holding period and expected trades per year: short 6J 18:00 → 20:55 ET (19:55 ET in US summer), flip long 20:55 → 02:00 ET; daily (≈ 245/yr) or gotobi/month-end only (≈ 60/yr).
- data needed: HistData USDJPY 1m (free) or Databento 6J full session (≈ $20); JST/DST alignment; Japanese holiday calendar (free).
- expected gross edge per trade: ≈ 2 bp per leg on average days vs 6J RT ≈ 1.5–2 bp → FAILS the screen unconditionally; gotobi/month-end days plausibly 5–10 bp → marginal pass with ≈ 60 trades/yr; overnight-session spreads 1–2 ticks.
- firm structure fit: overnight-session futures (entry after 18:00 ET, flat by 02:00 ET); FTMO intraday CFD (enter after 00:00 CET to avoid the swap); Japanese data releases 19:30/19:50 ET fall inside the first leg (no firm clause, but FTMO Standard-style ±2 min bans do not apply to Swing).
- nearest closed relative: D4 (intraday rules across 19 CFDs; verify whether USDJPY time-of-day windows were among them); no closed fix family.
- decay haircut: 0.5; splits at 2013 (Abenomics), 2015-02, 2022-09 (MoF interventions).
- plausibility of net Sharpe ≥ 1.5: low — well known, retail-crowded, a few pips; KMW's net JPY line is flat since 2013.
- original: no (new magnitudes only)

### C-1-06 Leveraged commodity ETF rebalancing into the settlement-time NAV in NG, CL, GC, SI
- mechanism: ProShares Trust II commodity LETFs reset leverage daily against a NAV struck at the futures settlement time: BOIL/KOLD (NG) and UCO/SCO (CL) at 14:30 ET, UGL (GC) 13:30 ET, AGQ (SI) 13:25 ET. Required rebalancing notional = Σ AUM_i × L_i × (L_i − 1) × r_day, always in the direction of the day's move (also for inverse funds), executed in the futures before the NAV print. Net assets 2026-11-02: BOIL $424m (25,334 Jan-27 NG contracts), KOLD $59m (−3,517), UCO $453m, SCO $948m (≈ −21,400 CL across Jan/Jun/Dec-27), UGL $642m, AGQ $953m (2,012 Dec-26 SI). Worked sizes: a +4% NG day ⇒ ≈ 2 × 424m × 4% + 6 × 59m × 4% ≈ $48m ≈ 1,100 NG contracts to buy into 14:30; a −3% CL day ⇒ ≈ 6 × 948m × 3% + 2 × 453m × 3% ≈ $200m ≈ 3,300 CL contracts to sell into 14:30. Equity analogue: Shum et al. (RoF 2016) earned 0.60%/trade gross on ≥ 2% days (2008-heavy) and the effect weakened as intermediaries pre-hedge (Barbon et al. 2022); Ivanov–Lenkey (JFM 2018, cited in Barbon et al.) find fund flows offset much of the rebalancing; Yan–Irwin–Sanders (JCM 2022) find predictable commodity-index flows have "modest and temporary" impact consistent with sunshine trading. No study of commodity-LETF settlement flows found (gap). Survival: flows are public, mechanical, and scale with AUM; they are also easy for others to anticipate.
- evidence: own idea built on peer-reviewed analogues (Shum, Hejazi, Haryanto & Rodier RoF 2016 and Barbon, Beckmeyer, Buraschi & Moerke 2022, both per pre-sweep A-C24; Yan, Irwin & Sanders, J. Commodity Markets 26 (2022), https://www.sciencedirect.com/science/article/abs/pii/S2405851321000295, abstract via search 2026-11-03) + issuer pages (https://www.proshares.com/our-etfs/leveraged-and-inverse/boil, /kold, /uco, /sco, /ugl, /agq, all fetched 2026-11-03). Post-2015 OOS: none (untested).
- instruments: NG/MNG, CL/MCL, GC/MGC, SI/SIL; FTMO NATGAS, USOIL, XAUUSD, XAGUSD (intraday).
- holding period and expected trades per year: enter 30 minutes before the NAV time in the direction of the day's move when |r_day| > 2% (NG/CL) or > 1% (GC/SI), exit at the settlement print or 5 minutes after; ≈ 40–80 trigger days/yr in NG, 20–40 in CL, 15–30 each in GC/SI; optional second leg fading the post-settlement reversal for 15 minutes.
- data needed: Databento 1m RTH NG, CL, GC, SI 2012–2026 (≈ $7 each, ≈ $28); current AUM from issuer pages (free); historical AUM/share counts from SEC filings or ETF databases (partly free); Bloomberg subindex roll schedules (free).
- expected gross edge per trade: unknown; equity precedent on large-move days 20–60 bp gross; NG 1-minute vol in the window ≈ 15–25 bp, so a 20 bp drift is detectable in 1m bars; NG RT ≈ 7 bp, CL RT ≈ 4 bp, GC RT ≈ 1 bp → passes the screen only if ≥ 15–20 bp materialises on trigger days (unverified).
- firm structure fit: intraday futures (all windows end by 14:35 ET); FTMO intraday CFD; news windows: none within ±2 minutes (EIA reports are hours earlier).
- nearest closed relative: H0006/H0019 (last-half-hour momentum incl. GEX, ES/NQ) — different instruments, window and a measurable flow size; pre-sweep A-C24 (NQ/ES LETFs).
- decay haircut: 0.7 (original); splits at 2020-04 (negative WTI, USO/UCO restructuring), 2022 (NG LETF AUM surge).
- plausibility of net Sharpe ≥ 1.5: low — flows are material only on big-move days and the commodity sunshine-trading evidence says predictable orders get absorbed; one registered row is justified because the flow size is computable from free data.
- original: yes

### C-1-07 Leveraged Treasury ETF rebalancing into the 4pm cash close in ZB/UB (TMF/TMV/TBT/TYD)
- mechanism: Daily-reset Treasury LETFs (Direxion TMF +3x / TMV −3x on the ICE 20+y index, TYD/TYO ±3x 7–10y, ProShares TBT −2x) rebalance at the 16:00 ET NAV in cash, ETFs and futures; required notional = Σ AUM × L × (L − 1) × r_day (multiplier 6 for +3x, 12 for −3x), always with the day's move. If TMF holds ≈ $5bn and TMV ≈ $0.3bn (issuer page blocked; to verify from SEC filings), a 2% TLT day implies ≈ $670m of 20y+ exposure ≈ 5,500 UB-equivalents in the last 15 minutes, large against typical late-day UB volume. Tuzun (2013) frames LETF rebalancing as the new portfolio insurance and estimates $1.04bn of equity flow per 1% move; no Treasury-specific study found (gap). The flow coincides with the month-end strike (C-1-01) on last trading days → exclude or model the interaction.
- evidence: own idea; Fed working paper (Tuzun, "Are Leveraged and Inverse ETFs the New Portfolio Insurers?", FEDS 2013, listing https://fedinprint.org/search?facets%5B%5D=authors_literal_array%3ATuzun%2C+Tugkan, search snippet 2026-11-03) + equity analogues (Shum et al. 2016; Barbon et al. 2022, per A-C24). Issuer AUM pages blocked (direxion.com 403, etfdb.com 403). Post-2015 OOS: none.
- instruments: ZB, UB (TN, ZN for the 7–10y funds); FTMO none.
- holding period and expected trades per year: 15:40 → 16:00 ET on days with |TLT r_day at 15:40| > 1.5%, ≈ 25–50 days/yr.
- data needed: Databento 1m UB full session (≈ $20; shared with C-1-01); TLT daily/1m (free via Yahoo/Alpaca); TMF/TMV share counts and NAV history from SEC N-PORT/N-CSR (free, labour).
- expected gross edge per trade: unknown; a 2% TLT day moves UB ≈ 2.4%, so a 10–20 bp late push is plausible; UB RT ≈ 5–6 bp → passes the screen only if ≥ 12 bp materialises (untested).
- firm structure fit: intraday futures (exit 16:00 ET, inside Topstep 16:08 / MFFU 16:10 / Lucid 16:45); consistency rules touched; no news windows.
- nearest closed relative: H0006/H0019 (last-half-hour momentum ES/NQ) — different instrument with a computable flow; A-C24.
- decay haircut: 0.7; splits at 2020-03, 2022–2023 (TMF AUM surge in the bond bear market).
- plausibility of net Sharpe ≥ 1.5: very low-low.
- original: yes

### C-1-08 ES post-cash-close reversal 16:00 → 16:08 ET of the closing-auction move
- mechanism: Closing-auction imbalances (MOC/LOC, passive and LETF flows) push the 16:00 cash print away from mid-quotes. Bogousslavsky–Muravyev (US stocks, JFM 2023): closing-price deviations are about half reversed shortly after the close and fully by the next morning; for stocks with after-hours liquidity one-third to one-half of the reversal occurs within the first half-hour after the close; the closing auction was ≈ 7.5% of volume in their sample (higher now). Liberty Street (2021, Boyarchenko–Larsen–Whelan): positive closing imbalances revert less than negative ones. ES trades to 16:15 ET and is no longer anchored by the auction after 16:00, so the index-level deviation can start reverting at 16:00–16:15 rather than only in the European hour. No study of the ES post-close window found (gap).
- evidence: peer-reviewed (Bogousslavsky & Muravyev, "Who trades at the close? Implications for price discovery and liquidity", JFM 2023, https://www.sciencedirect.com/science/article/abs/pii/S1386418123000502; AEA 2021 version https://www.aeaweb.org/conference/2021/preliminary/paper/H9T4hef7 — abstracts and search snippets 2026-11-03; Jegadeesh & Wu, "Closing auctions: Nasdaq versus NYSE", JFE 143 (2022), https://www.sciencedirect.com/science/article/abs/pii/S0304405X21005092, not fetched) + central-bank blog (Boyarchenko, Larsen & Whelan, "The Overnight Drift in U.S. Equity Returns", Liberty Street May 2021, https://libertystreeteconomics.newyorkfed.org/2021/05/the-overnight-drift-in-us-equity-returns, search snippet 2026-11-03). Post-2015 OOS: stock-level evidence to ≈ 2020; ES window untested.
- instruments: ES/MES (NQ/MNQ secondary); FTMO US500 (verify after-16:00 pricing source).
- holding period and expected trades per year: at 16:00:30 ET fade the 15:50 → 16:00 ES move when |move| > 0.15% (≈ 1 sd), exit 16:07 ET; ≈ 80–120 trades/yr; asymmetric variant: longs only after down-moves.
- data needed: ES 1m with 16:00–16:15 bars — the in-hand ES 1m RTH 2008–2026 may stop at 16:00 (verify); the in-hand Databento ES 2021–2026 copy is under LICENCE HOLD (cross-check only) → Databento ES full session 2010–2026 ≈ $20 if needed. No imbalance feed needed (price proxy).
- expected gross edge per trade: if one third of a typical 10–15 bp index-level closing deviation reverts within 8 minutes → 3–5 bp vs ES RT ≈ 1.2 bp → passes the screen (2 × RT = 2.4 bp) with 100+ trades/yr; but index deviations are smaller than stock-level ones (imbalances net out), so 1–2 bp is as likely → must be measured.
- firm structure fit: intraday futures — the window sits inside Topstep's 16:08 ET auto-flatten (exit 16:07), MFFU 16:10, Lucid/Tradeify 16:45; minimum-hold rules (5 s / 10 s) satisfied; no news windows.
- nearest closed relative: H0006/H0019 (last-half-hour momentum 15:30–16:00) — adjacent in time, opposite window and sign; H0012/H0017 (overnight-gap fade at 09:30) different; A-C25 (data-blocked imbalance version).
- decay haircut: 0.7; splits at 2018 (closing-auction share growth), 2020-03, 2022-05 (daily 0DTE).
- plausibility of net Sharpe ≥ 1.5: low.
- original: yes

### C-1-09 Index-rebalance effective days in ES/NQ/RTY and FTMO CFDs: close print and post-print reversal (extends P-C09)
- mechanism: On S&P quarterly rebalance days (third Friday of Mar/Jun/Sep/Dec, = quad witching), Russell reconstitution (late-June Friday) and MSCI SAIR dates, passive funds trade the closing auction; Krueger (P-C09): FTSE 100 CFD falls into the auction print on eve days, holdout +11.5 bp/event (t 3.9, n 27). But index-level net demand is small because adds and deletes net out, and even the single-stock effect has vanished: Greenwood–Sammon (JF 2025) — S&P 500 addition abnormal return 7.4% (1990s) → < 1% (last decade), deletions ≈ 0.1% (2010–2020), partly because MidCap migrations offset demand. Twist: (a) P-C09 rule in ES/NQ/RTY 15:30 → 16:00 ET on the US dates; (b) the post-print reversal 16:00 → 16:07 ET (C-1-08 logic) on these days only; RTY on reconstitution day is the year's largest closing auction.
- evidence: peer-reviewed (Greenwood & Sammon, "The Disappearing Index Effect", JF 80(2) 2025 657–698, NBER WP 30748 https://www.nber.org/system/files/working_papers/w30748/w30748.pdf, search snippet 2026-11-03) + blog with pre-registered holdout (Krueger Algorithms 2026, P-C09). Post-2015 OOS: Krueger 2023–2026 for UK100 only; US futures none.
- instruments: ES/MES, NQ/MNQ, RTY/M2K; FTMO UK100, GER40, JP225 (P-C09).
- holding period and expected trades per year: 15:30 → 16:00 and 16:00 → 16:07 ET on ≈ 10–12 US event days/yr (+ ≈ 12 European/MSCI dates via CFD).
- data needed: ES 1m (in hand), RTY 1m RTH (≈ $7); index review calendars (free); UK100 CFD ticks (Dukascopy datafeed blocked; FTMO MT5 history only once an account exists).
- expected gross edge per trade: UK100 +8–12 bp/event vs ≈ 1.7 bp RT → passes there (n ≈ 12/yr); US futures unknown and expected smaller (Greenwood–Sammon) → fail until measured.
- firm structure fit: intraday futures; FTMO intraday CFD (post-close pricing to verify); no news windows.
- nearest closed relative: H0006 (last-half-hour momentum) — this is a fixed-direction calendar flow, not momentum; H0023 (turn-of-month) different calendar.
- decay haircut: 0.5; splits at 2018, 2023.
- plausibility of net Sharpe ≥ 1.5: low.
- original: no (US-futures analogue and post-print leg are small twists on P-C09)

### C-1-10 Option-expiration pinning in ES — negative update and the "amplification" kill-test (updates A-C26)
- mechanism: Golez–Jackwerth (1992–2009) pinning via delta-hedge time decay. Elms (2026; 2016–2025, 2,294 trading days, ≈ 1.6m near-expiry SPY contracts, five tests): "no evidence of options pinning in S&P 500 expiration dynamics"; instead high near-expiry ATM open interest is associated with ≈ 16% wider daily ranges (p < 0.001), read as dealers net short gamma in short-dated options (amplification). Implication: A-C26's pinning rule should be expected to fail in the 0DTE era; the residue is range expansion on high-ATM-OI expiration days — a volatility statement, not a direction.
- evidence: working paper, not peer-reviewed (Elms, "From Pinning to Amplification: Evidence of a Regime Shift in S&P 500 Options Expiration Dynamics, 2016–2025", SSRN 6564078 — host blocked; summary https://harbourfrontquant.substack.com/p/from-pinning-to-amplification-evidence, fetched 2026-11-03) + peer-reviewed (Golez & Jackwerth JFE 2012, per A-C26). Post-2015 OOS: Elms is entirely post-2015 and negative for pinning.
- instruments: ES/MES; NQ/MNQ.
- holding period and expected trades per year: kill-test only — the A-C26 rule (15:00 → 16:00 distance-to-strike) on 2016–2026; the amplification variant (late-day breakout on top-quartile ATM-OI days) belongs to the closed last-half-hour family and should not be registered without a new mechanism row.
- data needed: ES 1m (in hand); CBOE delayed OI by strike (free, end-of-day; 0DTE OI known only from the prior close → weak proxy); expiration calendar (free). $0.
- expected gross edge per trade: pinning ≈ 0 expected; amplification is direction-neutral and costs 2 × ES RT per attempt → fails the screen as a directional claim.
- firm structure fit: intraday futures; FTMO intraday CFD.
- nearest closed relative: H0006/H0019 (last-half-hour momentum incl. GEX) — the amplification variant is inside this family; cite, do not re-run.
- decay haircut: n/a (expected null); split at 2022-05-11 (daily SPX expirations).
- plausibility of net Sharpe ≥ 1.5: very low.
- original: no

### C-1-11 FX option 10:00 ET New York cut: strike gravitation before, release after, in 6E/6J
- mechanism: OTC FX options expire at the 10:00 ET New York cut (CME aligned its FX options in 2019); dealers hedging large expiring strikes buy below / sell above the strike in the hour before (dampening, the trader's "magnet") and unwind afterwards (range release). Expiry lists with notional sizes are published free every morning. No academic evidence found (search 2026-11-03); practitioner notes disagree on magnitude.
- evidence: forum/practitioner only (CME Group, "FX Options Expiration Time Change", https://www.cmegroup.com/education/lessons/fx-options-expiration-time-change; daily lists e.g. https://investinglive.com/orders/fx-option-expiries-for-6-october-10am-new-york-cut/ — search snippets 2026-11-03). Post-2015 OOS: none.
- instruments: 6E, 6J (largest notionals), 6B; FTMO EURUSD/USDJPY.
- holding period and expected trades per year: (a) mean reversion toward the nearest strike with ≥ $1.5bn notional within 0.3% of spot, 09:00 → 09:58 ET; (b) breakout continuation 10:00 → 10:30 ET; ≈ 100–150 qualifying days/yr.
- data needed: 6E/6J 1m (HistData spot free, or Databento RTH ≈ $7 each); historical expiry lists scraped from archived daily posts (free but laborious, coverage from ≈ 2016) → partially data-blocked.
- expected gross edge per trade: a few pips (3–8 bp) per event vs 6E RT ≈ 1.2 bp → passes on paper; no evidence that the pull exists at index level.
- firm structure fit: intraday futures; FTMO intraday CFD; US 10:00 ET releases (ISM, consumer confidence, JOLTS) coincide → MFFU Rapid/Pro ±2-minute ban and Lucid Daily rule bind on those days; exclude them.
- nearest closed relative: none; A-C26 is the equity analogue; D4 unrelated.
- decay haircut: 0.7; splits at 2019 (CME alignment), 2022.
- plausibility of net Sharpe ≥ 1.5: very low-low.
- original: yes

### C-1-12 Daily 4pm Treasury index-strike window in ZN/ZB (updates A-C13 with 2026 volume facts)
- mechanism: Index-tracking funds execute at the 4pm strike every day; the 10-minute window's share of cash volume rose from 2.5% (2021) to 3.5% (2025) while the 3pm futures-settlement spike is unchanged, so a growing time-stamped flow sits at 15:55–16:00 ET; if net flows are directional (bond-fund/ETF inflows) price pressure precedes and reverts after the strike. Still no return evidence (gap).
- evidence: central-bank blog with data (Dyer, Fleming & Shachar 2026, URL as in C-1-01, fetched 2026-11-03). Post-2015 OOS: volume facts only.
- instruments: ZN, ZB, UB; FTMO none.
- holding period and expected trades per year: 15:45 → 16:00 ET and fade 16:00 → 16:07 ET, conditioned on prior-day TLT/IEF creation/redemption sign; ≈ 250 days/yr.
- data needed: ZN 1m full session (shared with C-1-01); TLT/IEF daily flows (iShares, free). $0 incremental.
- expected gross edge per trade: expected ≤ 1 bp vs ZN RT ≈ 3 bp → FAILS the screen; only a conditioned version with hundreds of trades/yr and win rate > 58% could qualify, and nothing suggests it.
- firm structure fit: intraday futures (inside Topstep 16:08); no news windows.
- nearest closed relative: none; A-C13.
- decay haircut: 0.7; split at 2021-01-14.
- plausibility of net Sharpe ≥ 1.5: very low.
- original: no

### C-2-01 Natural gas EIA storage announcement-day return premium (Prokopczuk–Wese Simen–Wichmann 2021)
- mechanism: An announcement-day risk premium in NG futures: "more than 50% of the annual return is earned" on EIA storage report days (Thursdays 10:30 ET); the gap versus non-announcement days is not explained by the storage surprise or other controls; intraday the return splits about half before and half after the release; the pre-announcement part occurs only when storage exceeds expectations (the authors read this against informed trading); "a simple trading strategy yields substantial returns after transaction and funding costs." Magnitudes, sign conventions and the strategy's Sharpe are in the paper, which could not be read: Energy Journal paywall, Reading repository behind anti-bot protection, Liverpool accepted manuscript embargoed until 2026-11-30 → abstract only. Survival argument: a premium for holding NG through the week's main scheduled shock, 52 events/yr, little practitioner attention.
- evidence: peer-reviewed, abstract only (Prokopczuk, Wese Simen & Wichmann, "The Natural Gas Announcement Day Puzzle", The Energy Journal 42(2) 2021 91–111, DOI 10.5547/01956574.42.2.mpro; abstract via https://ideas.repec.org/a/aen/journl/ej42-2-wichmann.html and https://livrepository.liverpool.ac.uk/3083246/, fetched 2026-11-03; accepted manuscript https://centaur.reading.ac.uk/90003/1/NG_paper_final_round.pdf — host blocked, not routed around). Post-2015 OOS: unknown from the abstract (sample period not shown on the pages seen).
- instruments: NG, MNG; FTMO NATGAS (intraday or Swing).
- holding period and expected trades per year: long NG from 18:00 ET Wednesday (or 09:00 ET Thursday) to the 14:30 ET Thursday settlement; variants pre-release only (09:00 → 10:29) and post-release only (10:32 → 14:30); ≈ 52 trades/yr (holiday weeks shift to Wednesday/Friday).
- data needed: Databento 1m NG RTH 2010–2026 (≈ $7; both legs sit in RTH); EIA storage actuals (free); consensus survey not free (EIA 5-year average or scraped forecasts as a proxy).
- expected gross edge per trade: NG daily sd ≈ 3–4%; for "> 50% of annual return" to be meaningful the announcement-day mean must be of order +30–80 bp ≫ NG RT ≈ 7 bp → passes the economics screen on paper; a 50 bp mean over 500 events would be t ≈ 3 — sign and size must be confirmed from the paper before any row.
- firm structure fit: overnight-session or intraday futures (flat by 14:30 ET); FTMO intraday CFD (≈ 8 bp RT) or Swing (one swap night); news windows: MFFU Rapid/Pro ±2 min incl. resting orders if EIA NG is on its Tier-1 list (verify; if yes exit 10:27, re-enter 10:33), Lucid Daily red-folder breach risk → not for Lucid Daily; Topstep, Bulenox, FTMO Swing allow news.
- nearest closed relative: E2-01..12 (macro events intraday ES/NQ) — different asset and mechanism (premium, not reaction); pre-sweep A-C15 (NG surprise reaction).
- decay haircut: 0.5; splits at 2012 (shale regime), 2020-03, 2022-02 (LNG/Europe shock).
- plausibility of net Sharpe ≥ 1.5: low-medium — the only lane-2 item with a published after-cost strategy; abstract-only status and a 7 bp RT in a 60%-vol market keep it low until the paper is read.
- original: no

### C-2-02 Pre-EIA crude order-flow drift with API conditioning (Rousse–Sévi 2019; Ye–Karali 2016)
- mechanism: Rousse–Sévi (WTI intraday): in the two hours before the Wednesday 10:30 ET EIA release, on days when inventories later beat forecasts (builds), order flow is abnormal and the price falls ≈ 0.25% on average before the news — read as informed trading (the API figure is known to subscribers from Tuesday 16:30 ET); after the release an over-reaction is "partly compensated in the hours following". Ye–Karali (Energy Economics 59, 2016): API surprises versus Reuters expectations move returns inversely; EIA surprises measured against API still matter, most when Reuters and API miss in the same direction. New conditioning: use the public API headline sign (Tuesday evening) as the direction for CL 08:30 → 10:29 ET, only when the API surprise is large.
- evidence: peer-reviewed, abstracts only (Rousse & Sévi, "Informed Trading in the WTI Oil Futures Market", The Energy Journal 40(2) 2019 139–160, https://journals.sagepub.com/doi/10.5547/01956574.40.2.orou; abstract via https://ideas.repec.org/p/ags/feemes/249788.html, fetched 2026-11-03; Ye & Karali, Energy Economics 59 (2016) 349–364, abstract via https://ideas.repec.org/p/ags/aaea15/205595.html, fetched 2026-11-03; both PDFs on ageconsearch.umn.edu returned 403). Post-2015 OOS: none (working paper 2016 → data ≤ 2015).
- instruments: CL/MCL, RB, HO; FTMO USOIL.
- holding period and expected trades per year: 08:30 → 10:29 ET on EIA days, ≈ 50 trades/yr; optional hold to 10:35.
- data needed: Databento 1m CL RTH (≈ $7); API weekly headline history (scraped from news archives; API data itself is paid) → partial data gap; EIA actuals (free).
- expected gross edge per trade: 25 bp on build days (paper) vs CL RT ≈ 4 bp → passes the screen if the pattern survived; the common brief lists post-2014 pre-announcement drift as negative evidence (macro lock-up reforms) — EIA had no lock-up change, but HFT competition grew.
- firm structure fit: intraday futures; exit at 10:27 satisfies MFFU ±2 min; Lucid Daily red-folder (verify EIA classification) → avoid; FTMO intraday fine.
- nearest closed relative: negative-evidence row "pre-announcement drift post-2014" (macro, different release mechanics); A-C14.
- decay haircut: 0.5; splits at 2015, 2020-04.
- plausibility of net Sharpe ≥ 1.5: low.
- original: yes (API-sign conditioning of the pre-release leg)

### C-2-03 EIA crude post-release: fade the first-minutes over-reaction (updates A-C14 with Miao et al. 2018 and Krueger's negative first-reaction number)
- mechanism: Miao–Ramchander–Wang–Yang (JFM 2018): futures fall after positive inventory surprises; no asymmetry in futures; volatility normalises faster after jump announcements. Rousse–Sévi: over-reaction partly reversed within hours. Krueger (lit-practitioner closed-family cross-references): EIA crude first reaction −14.65 bp (t −2.7) for continuation, i.e. fading the first move was positive in his 2015–2026 CFD sample. This flips A-C14's continuation sign into a reversal hypothesis: fade the 10:30 → 10:32 move from 10:33 to 11:30 ET when |move| > 1 sd.
- evidence: peer-reviewed (Miao, Ramchander, Wang & Yang, "The impact of crude oil inventory announcements on prices: Evidence from derivatives markets", JFM 38(1) 2018 38–65, https://ideas.repec.org/a/wly/jfutmk/v38y2018i1p38-65.html, abstract via search 2026-11-03; Geman & Li 2018 per A-C14) + blog with holdouts (Krueger, per lit-practitioner). Post-2015 OOS: Krueger's −14.65 bp (t −2.7) is the only post-2015 number.
- instruments: CL/MCL; FTMO USOIL.
- holding period and expected trades per year: 10:33 → 11:30 ET, ≈ 50/yr.
- data needed: CL 1m RTH (shared with C-2-02); EIA actuals (free). $0 incremental.
- expected gross edge per trade: ≈ 10–15 bp gross vs CL RT ≈ 4 bp (assume 2 ticks slippage at 10:33) → passes at 1× costs, fails at 2× unless larger on big-surprise days.
- firm structure fit: intraday futures; entry at 10:33 is outside ±2 min; Lucid Daily red-folder risk; FTMO intraday fine.
- nearest closed relative: E2-01..12 (ES/NQ macro reaction) — different asset; A-C14.
- decay haircut: 0.5; splits at 2015, 2020-04.
- plausibility of net Sharpe ≥ 1.5: low.
- original: no

### C-2-04 WASDE and quarterly Grain Stocks/Acreage: minute-data update and the limit-lock reopen twist (updates A-C16)
- mechanism: Adjemian–Irwin (AJAE 2018; 2009–2014 intraday): volatility spikes after USDA releases dissipate within minutes. Arkansas FSA104 (1-minute corn/soybeans 2013–2023): quiet 08:30–10:45 CT, sharp spike 5–15 minutes after 11:00 CT, back toward baseline within 30–60 minutes; the day before and after look like ordinary days. Applied Economics Letters 2024 (2013–2023 intraday): volatility rises after the release (volatility, not drift). Anderson et al. 2024 (A-C16) still report a soybean reaction growing past 30 minutes. New twist: trade only reports that lock limit (June 30 Acreage/Grain Stocks, January final, occasional WASDEs): when ZC/ZS close locked at 13:20 CT, the unfilled adjustment continues at the 19:00 CT (20:00 ET) reopen under expanded limits — an overnight-session hold at futures firms.
- evidence: peer-reviewed (Adjemian & Irwin, "USDA Announcement Effects in Real-Time", AJAE 100(4) 2018 1151–1171, DOI 10.1093/ajae/aay018, via search 2026-11-03, not fetched) + extension fact sheet with minute data (Park, "What Happens on WASDE Days", University of Arkansas FSA104, https://www.uaex.uada.edu/publications/pdf/FSA104.pdf, fetched 2026-11-03) + peer-reviewed (Applied Economics Letters 2024, https://www.tandfonline.com/doi/full/10.1080/13504851.2024.2373337, host blocked, search snippet) + conference paper (Anderson, McKenzie & Noyes 2024, per A-C16). Post-2015 OOS: FSA104 and AEL cover 2013–2023 (volatility only).
- instruments: ZC, ZS, ZW (MZC/MZS); FTMO: no grain CFDs found (verify).
- holding period and expected trades per year: (a) A-C16 rule 12:03 → 13:10 ET, ≈ 36/yr; (b) limit-lock continuation: enter at the 20:00 ET reopen in the lock direction, exit next day 13:15 ET, ≈ 3–8 events/yr.
- data needed: Databento 1m ZC/ZS RTH (≈ $7 each) for (a); full session (≈ $20 each) or 1h ($1 each) for (b); USDA calendar and report numbers (free); CBOT limit schedule (free).
- expected gross edge per trade: (a) ZC RT ≈ 12 bp against a post-15-minute drift the minute data say is small → FAILS; ZS RT ≈ 5 bp vs an unquantified soybean drift → unknown; (b) 1–3% continuation historically → passes, but n ≈ 5/yr → a tail add-on, not a sleeve.
- firm structure fit: intraday futures for (a); overnight-session futures for (b) (20:00 ET entry, flat 13:15 ET); MFFU/Lucid news rules only if USDA is on their lists (verify).
- nearest closed relative: none (E2 is ES/NQ); A-C16.
- decay haircut: 0.5 (a) / 0.7 (b); splits at 2012 (in-session release), 2018 (media lock-up access removed), 2020.
- plausibility of net Sharpe ≥ 1.5: very low (a) / low (b).
- original: yes for (b) (limit-lock reopen continuation)

### C-2-05 USDA Crop Progress (Mondays 16:00 ET, April–November) → ZC/ZS reaction at the 20:00 ET reopen
- mechanism: Weekly condition ratings (good/excellent %) are a scheduled information shock released after the 14:20 ET close. Lehecka (JARE 39(1) 2014; corn/soybeans 1986–2012): prices react rapidly and rationally to new condition information, strongest in July–August. The first tradable print is the 20:00 ET Globex reopen, inside the futures-firm trading day. Rule: direction = −sign(change in good/excellent % versus the prior week net of the seasonal norm); enter 20:00 ET, exit 09:30 or 13:15 ET next day. No study of the reopen window found.
- evidence: peer-reviewed, abstract via search (Lehecka, "The Value of USDA Crop Progress and Condition Information: Reactions of Corn and Soybean Futures Markets", JARE 39(1) 2014; record https://ageconsearch.umn.edu/record/168261 — host returned 403; search snippet 2026-11-03). Post-2015 OOS: none found.
- instruments: ZC, ZS (MZC/MZS); FTMO none.
- holding period and expected trades per year: 20:00 ET Monday → 13:15 ET Tuesday, ≈ 30 weeks × 2 roots ≈ 60 trades/yr (growing season).
- data needed: Databento ZC/ZS 1h full session (≈ $1/root, first pass) or 1m (≈ $20/root); NASS Crop Progress history (free, QuickStats).
- expected gross edge per trade: order of 0.3–0.8% reaction to a 2-point rating change in July–August (magnitude inferred from the literature's description, not a measured figure) vs ZC RT ≈ 12 bp, ZS ≈ 5 bp → passes only if the reopen print does not already contain it; honest expectation: the opening gap carries most of it and the post-open drift is the testable residue.
- firm structure fit: overnight-session futures (20:00 ET → before deadlines); thin overnight grain books (assume 2 ticks slippage); no news windows.
- nearest closed relative: H0012/H0017 (overnight-gap fade, S&P) — different asset and sign; none closed in grains.
- decay haircut: 0.7; splits at 2012, 2018.
- plausibility of net Sharpe ≥ 1.5: low.
- original: yes (new instrument and window)

### C-2-06 USDA livestock reports (Cattle on Feed, Hogs and Pigs; 15:00 ET Fridays) → LE/HE next-session continuation
- mechanism: Reports land after the 14:05 ET livestock close; the Monday open absorbs the surprise, often with limit moves. Schroeder–Mintert–Blair (1972–87): ≥ $1/cwt moves on 48% of post-report days versus 6% of release days; a meta-analysis of USDA forecasts finds hog futures react to unanticipated changes only. Rule: direction = sign(surprise vs pre-report analyst average), enter at the Monday 09:30 ET open, exit 13:00 ET; locked-limit opens continue into Tuesday (tail variant).
- evidence: peer-reviewed, old (Schroeder, Mintert & Blair, K-State record https://krex.k-state.edu/items/e2b691b4-294c-4d51-bd68-36f8db08277a; AAEA 1989 https://ideas.repec.org/p/ags/aaea89/270490.html; USDA forecasts meta-analysis arXiv 1801.06575 https://arxiv.org/pdf/1801.06575 — search snippets 2026-11-03). Post-2015 OOS: none; trade-press reaction notes only.
- instruments: LE, HE, GF (CME); FTMO none.
- holding period and expected trades per year: Monday 09:30 → 13:00 ET after ≈ 12 Cattle-on-Feed and 4 Hogs-and-Pigs reports → ≈ 16–20 trades/yr.
- data needed: Databento 1m LE/HE RTH (≈ $7 each); pre-report analyst averages (trade-press archives, partly free); report numbers (free, NASS).
- expected gross edge per trade: unknown; LE RT ≈ 2.5 bp, HE ≈ 6 bp; limit-locked opens prevent fills in the best cases (adverse selection) → likely fail.
- firm structure fit: intraday futures (livestock allowed at most futures firms — verify product lists); report outside hours → no news-window clause.
- nearest closed relative: none.
- decay haircut: 0.7; splits at 2012 (electronic dominance), 2020.
- plausibility of net Sharpe ≥ 1.5: very low.
- original: yes (new instrument; recorded for completeness, not recommended)

### C-2-07 LBMA gold/silver auctions after the 2015 reform: Nilsson-pattern kill-test and auction-round-imbalance momentum (extends A-C18)
- mechanism: Pre-2015 the PM fix leaked (Caminschi–Heaney: volume/volatility spike at the start of the fix; Aspris et al.: leakage ≈ 4–10 bp pre-reform and "far less" under the electronic auction). The ICE/LBMA auction publishes round-by-round price and imbalance (≈ every 45 s) at 10:30 and 15:00 London (gold) and 12:00 London (silver) — a public, time-stamped order imbalance. Nilsson (2015, as summarised by Crain et al.): futures decline ahead of the AM fix and rise after the PM fix, with similar patterns after the 2015 change (graphical). Crain–Hoelscher–Jones (2020; daily GC/SI futures 2008–2018): volatility and price behaviour changed around the reform. Twist: (a) kill-test Nilsson's pattern on 2015–2026 1m GC/SI; (b) trade GC in the direction of the first-round imbalance for the auction's duration (2–6 minutes) plus 10 minutes.
- evidence: peer-reviewed (Caminschi & Heaney JFM 34(11) 2014 1003–1039, per A-C18; Crain, Hoelscher & Jones, "Fixing the Fix for Silver and Gold", ACRN Journal of Finance and Risk Perspectives 9 (2020) 177–197, http://www.acrn-journals.eu/resources/jofrp09m.pdf, fetched 2026-11-03) + working papers (Aspris, Foley, Gratton & O'Neill, "Towards a New Fix", 2015, https://acfr.aut.ac.nz/__data/assets/pdf_file/0011/29792/A-Aspris-Towards-a-New-Fix-Version-005-Submit.pdf; "Transparency in Commodities Markets", EFMA 2017, https://efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2017-Athens/papers/EFMA2017_0580_fullpaper.pdf — search snippets 2026-11-03). Post-2015 OOS: Aspris et al. find improved post-reform market quality; no return study.
- instruments: GC/MGC, SI/SIL; FTMO XAUUSD/XAGUSD.
- holding period and expected trades per year: AM auction ≈ 05:30–05:40 ET, PM auction ≈ 10:00–10:10 ET (one hour later during the 2–3 weeks of US/UK DST mismatch); ≈ 500 auctions/yr.
- data needed: Databento 1m GC full session (≈ $20; the AM auction is outside US RTH); LBMA/ICE round-by-round history (published on the LBMA/ICE sites; historical depth to verify, possibly free).
- expected gross edge per trade: a few bp per auction vs GC RT ≈ 0.6–1 bp → passes only if ≥ 2 bp per event systematically; Aspris et al.'s "far less leakage" argues ≈ 0; the round-imbalance leg is the only mechanism with a public real-time signal.
- firm structure fit: overnight-session futures for the AM auction (05:30 ET is inside the futures-firm day), intraday for the PM; FTMO intraday CFD; the 10:00 ET PM auction coincides with US 10:00 releases → news-window bans on those days.
- nearest closed relative: none; A-C18.
- decay haircut: 0.7 (leg b) / 0.5 (Nilsson pattern); splits at 2015-03-20 (gold), 2014-08-15 (silver).
- plausibility of net Sharpe ≥ 1.5: low.
- original: yes for the round-imbalance leg (b)

### C-2-08 COMEX gold/silver option-expiry days: pinning into the 13:30/13:25 ET settlement
- mechanism: Monthly GC options expire four business days before month-end at the 13:30 ET settlement; dealers' delta hedges decay and ETF/option flows concentrate into the settlement window — the metals analogue of Golez–Jackwerth — and the window coincides with the UGL/AGQ LETF NAV times (C-1-06). No evidence found.
- evidence: own idea; Golez & Jackwerth JFE 2012 as the equity analogue (A-C26); Elms 2026 negative for ES pinning (C-1-10).
- instruments: GC/MGC, SI/SIL; FTMO XAUUSD/XAGUSD.
- holding period and expected trades per year: 12:30 → 13:30 ET on ≈ 12 GC and 12 SI expiry days/yr.
- data needed: GC/SI 1m RTH (shared with C-1-06); CME option expiry calendar (free); OI by strike (CME daily bulletin, free, delayed). $0 incremental.
- expected gross edge per trade: unknown, likely ≤ 5 bp vs GC RT ≈ 1 bp; fails on n (24/yr) regardless.
- firm structure fit: intraday futures; FTMO intraday CFD.
- nearest closed relative: none; A-C26 analogue.
- decay haircut: 0.7; split at 2022.
- plausibility of net Sharpe ≥ 1.5: very low.
- original: yes (recorded; not recommended for a row)

### C-2-09 FOMC three-day window in long Treasuries, captured as overnight-session holds (Hillenbrand 2025; Pan–Peng 2026)
- mechanism: Hillenbrand (RFS 2025): the entire 1980–2017 fall of the 10y yield (10.1% → 2.4%) occurred inside the three-day window (day before, day of, day after) around FOMC meetings; moves outside the window wash out; attributed mainly to a lower expected short-rate path. Pan–Peng (2026; 250 scheduled announcements since 1994; ZN futures 2004–2025): a pre-FOMC Treasury drift on the day before the announcement — 10y zero-coupon yield −0.79 bp (t −2.39) versus −0.04 bp on other days, term premium −0.71 bp (t −2.34), 2y insignificant; high-frequency Treasury futures show the drift "concentrated outside regular U.S. trading hours", rising from around the Tokyo open on day −2 and peaking around the London close on day −1; stronger when labour-market uncertainty is elevated; the MOVE index falls pre-FOMC. SR1188 adds that yields decline after FOMC announcements, significantly for the four shortest maturities. Twist: long ZN/UB from 18:00 ET on day −2 to 11:30 ET on day −1 (the measured drift window), and separately the post-announcement overnight session 18:00 ET day 0 → 15:00 ET day +1; both inside a futures-firm trading day.
- evidence: peer-reviewed (Hillenbrand, "The Fed and the Secular Decline in Interest Rates", RFS 38(4) 2025 981–1013, https://www.hbs.edu/faculty/Pages/item.aspx?num=67591; summary https://quantpedia.com/secular-decline-in-yields-around-fomc-meetings/, fetched 2026-11-03) + working paper (Pan & Peng, "The Pre-FOMC Drift in Long-Term Treasury Bonds", June 2026, https://en.saif.sjtu.edu.cn/junpan/FOMC_new.pdf, fetched 2026-11-03, pp. 2–3 and Section 2) + central-bank WP (BIS WP 1252: FOMC windows ≈ 70% of the 10y decline across countries, https://www.bis.org/publications/working-paper-1252-monetary-policy-and-secular-decline-long-term-interest-rates-global-perspective.pdf, search snippet 2026-11-03). Negative context: Kurov, Wolfe & Gilbert, "The disappearing pre-FOMC announcement drift", FRL 40 (2021) — the equity drift vanished after 2015 (https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html, snippet). Post-2015 OOS: Pan–Peng's sample runs to 2025 (sub-period numbers not extracted); Hillenbrand to 2017.
- instruments: ZN, ZB, UB (TN); FTMO none.
- holding period and expected trades per year: 8 meetings × 2 windows = 16 holds/yr, ≈ 17.5 h each.
- data needed: ZN/UB 1h full session (≈ $1/root suffices; 1m shared with C-1-01); FOMC calendar (free); MOVE/VIX daily (free).
- expected gross edge per trade: −0.79 bp of 10y yield ≈ +5.5 bp price in ZN (duration ≈ 7) and ≈ +13 bp in UB (duration ≈ 17) per pre-FOMC window vs RT ≈ 3 bp (ZN) / 5–6 bp (UB) → passes the screen in UB (≥ 2 × RT), marginal in ZN; 16 trades/yr → sleeve only; the in-sample t ≈ 2.4 is below the program bar.
- firm structure fit: overnight-session futures (18:00 ET entry, exits 11:30 ET / 15:00 ET); the 14:00 ET statement is never held through → no news-window conflict; consistency rules touched.
- nearest closed relative: E2-05 (pre-FOMC drift intraday ES/NQ, closed) and A-C40 (pre-announcement premium; its ZN window 09:30 → 13:55 on day 0 is not where Pan–Peng find the drift — the day −1 window is new); A-C11 (post-FOMC drift in ZN).
- decay haircut: 0.5 (published 2025/2026, high profile); splits at 2008-12 (ZLB), 2015, 2022-03.
- plausibility of net Sharpe ≥ 1.5: low-medium as a sleeve (strong documentation, right instrument, firm-compatible window) but 16 events/yr and a modest in-sample t.
- original: yes (window construction across the firm day boundary; the day −1 Treasury drift is new to the program)

### C-2-10 Post-FOMC drift in ZN via overnight-session holds (extends A-C11)
- mechanism: Brooks–Katz–Lustig: retail bond-fund outflows after salient surprises make yields drift for ≈ 50 days (≈ 0.25 bp/day on the 10y); A-C11 judged intraday capture hopeless because the drift is mostly overnight. At futures firms the 18:00 → 15:00 ET hold is inside one trading day and captures ≈ 21 of 24 hours. Rule: for 20 sessions after |Kuttner surprise| > 2 bp, hold ZN in the drift direction 18:00 → 15:00 ET.
- evidence: working paper (Brooks, Katz & Lustig, NBER WP 25127, https://www.nber.org/papers/w25127, per A-C11) + SR1188's post-FOMC yield decline for short maturities (fetched 2026-11-03). Post-2015 OOS: the NBER robustness runs to 2015; nothing after.
- instruments: ZN, ZF, ZT (short end per SR1188); FTMO none.
- holding period and expected trades per year: ≈ 20 holds per qualifying meeting × 3–5 meetings/yr = 60–100 holds/yr.
- data needed: ZN/ZF 1h full session (≈ $1/root); ZQ 1m around 14:00 ET for the Kuttner surprise (≈ $7 RTH) or free FedWatch snapshots.
- expected gross edge per trade: ≈ 2 bp/day on ZN vs RT ≈ 3 bp → FAILS the screen unless the first five days carry most of the drift (unknown).
- firm structure fit: overnight-session futures; consistency and inactivity clauses benign.
- nearest closed relative: E2-01..04 (post-statement continuation/reversal ES/NQ); A-C11.
- decay haircut: 0.5; splits at 2008, 2015, 2022.
- plausibility of net Sharpe ≥ 1.5: very low-low.
- original: yes (window), but expected to fail the economics screen

### C-2-11 FOMC press-conference window in ZN: statement-reaction continuation 14:30 → 15:30 ET (Gómez-Cram–Grotteria 2022)
- mechanism: Price moves around the 14:00 ET statement predict the moves during the 14:30 press conference: correlation up to 58% for medium-term Eurodollar futures and 44% for the S&P 500; when the Chair discusses the changes versus the previous statement, volatility and volume spike and prices move in the same direction as around the statement release (verbal re-statement of released news moves prices again). Rule: at 14:29 ET take the sign of the 13:59 → 14:05 ZN move; hold 14:30 → 15:30 ET (or exit when the Q&A starts).
- evidence: peer-reviewed, open access (Gómez-Cram & Grotteria, "Real-time price discovery via verbal communication: Method and application to Fedspeak", JFE 143(3) 2022 993–1025, https://lbsresearch.london.edu/id/eprint/2203/, abstract via search snippet 2026-11-03; SSRN blocked). Post-2015 OOS: press conferences at every meeting only since 2019 → sample mostly 2011–2019 (verify); nothing after 2022.
- instruments: ZN, ZF (closest to the Eurodollar/SOFR result), ZB; FTMO none; ES/NQ excluded (E2).
- holding period and expected trades per year: 8/yr, ≈ 1 hour.
- data needed: ZN/ZF 1m RTH (≈ $7 each, shared); FOMC schedule and press-conference start times (Fed site, free).
- expected gross edge per trade: statement reactions in ZN are typically 10–40 bp; a 44–58% correlation implies a same-direction press-conference move of order 5–15 bp vs ZN RT ≈ 3 bp → passes on paper; n = 8/yr is far too small for the gate alone (pool ZF/ZN/ZB and years; still < 100 events per decade).
- firm structure fit: intraday futures (14:30–15:30 ET); MFFU Rapid/Pro ±2 min applies to the 14:00 release (entry 14:29 is outside; verify whether the press conference is listed); Lucid Daily → avoid; FTMO n/a.
- nearest closed relative: E2-01..04 (post-statement continuation/reversal in ES/NQ at N = 5/15/30 min) — same event, different asset and a later window anchored on the press conference; heavy adjacency flagged.
- decay haircut: 0.5; splits at 2019-01 (press conference every meeting), 2022-03.
- plausibility of net Sharpe ≥ 1.5: low (small n; mechanism well identified).
- original: no

### C-2-12 Auction-result surprise at 13:01 ET: tail / bid-to-cover reaction continuation in ZN/UB (Smales 2021; Ray–Droste–Gorodnichenko 2024)
- mechanism: Auction results (13:01–13:03 ET) resolve demand uncertainty. Smales (ZN 15-min bars 2000–2017): higher bid-to-cover → positive returns and lower volatility in the interval right after the auction. Ray–Droste–Gorodnichenko (JPE 2024) use the yield change in a 30-minute window around auction results as a demand shock with persistent effects on yields over subsequent weeks (robust to using futures), i.e. the shock is not fully reversed. Fleming–Liu–Nguyen show post-auction net buying coincides with the reversal of pre-auction pressure. Rule: at 13:06 ET, direction = sign of the 13:00 → 13:05 ZN move (or of the tail), hold to 13:45 ET; distinct from C-1-03's pressure legs.
- evidence: peer-reviewed (Smales, Accounting & Finance 61(S1) 2021, snippet 2026-11-03, UWA repository URL in C-1-03; Ray, Droste & Gorodnichenko, "Unbundling Quantitative Easing: Taking a Cue from Treasury Auctions", JPE 132(9) 2024 3115–3172, https://ideas.repec.org/a/ucp/jpolec/doi10.1086-729581.html, abstract via search 2026-11-03) + staff report (SR1188, fetched). Post-2015 OOS: Smales to 2017; JPE sample to ≈ 2020 (verify).
- instruments: ZN (10y/7y/3y), ZB/UB (30y/20y), ZF (5y); FTMO none.
- holding period and expected trades per year: 13:06 → 13:45 ET, ≈ 100 auctions/yr.
- data needed: ZN/UB 1m RTH (shared); TreasuryDirect results (free; when-issued tails from trade press) — the 13:00 → 13:05 price move is the free proxy.
- expected gross edge per trade: continuation of a 5–10 bp result move by 2–4 bp vs ZN RT ≈ 3 bp → marginal/fails; UB (≈ 3x) passes if the pattern exists. Prior: the 13:01 reaction is arbitraged within seconds; only slow demand-shock persistence could leave 30-minute drift.
- firm structure fit: intraday futures; auction results not on firm Tier-1 lists (verify); minimum-hold fine.
- nearest closed relative: none; A-C10 / C-1-03.
- decay haircut: 0.5; splits at 2010 (demand-elasticity break per HBS 26-033), 2015.
- plausibility of net Sharpe ≥ 1.5: low.
- original: no

### C-2-13 FOMC-day (and BoJ-day) currency risk premium in 6A/6B/6E/6J (Mueller–Tahbaz-Salehi–Vedolin 2017)
- mechanism: Constrained financiers demand compensation for monetary-policy uncertainty, so short-USD/long-foreign strategies earn more on scheduled FOMC days (1994–2013, 160 announcement days, 4pm-to-4pm ET returns): low-rate portfolio +5.19 bp versus −0.51 bp on other days; high-rate portfolio +14.47 versus +1.73 bp; AUD +17.28 versus +1.16 bp (difference t 2.51); simple strategy 10.77 bp per announcement day, improved version (positive-differential currencies, reversed after a tightening) 20.54 bp (t 4.17), Sharpe 0.51 → 0.93; both the pre- and post-announcement windows are larger on announcement days; survives bid-ask adjustment (annualized Sharpe up to 0.8); BoJ announcement days show a "virtually identical" pattern for the yen, other central banks none; the effect is specific to monetary-policy announcements, not other macro releases.
- evidence: peer-reviewed (Mueller, Tahbaz-Salehi & Vedolin, "Exchange Rates and Monetary Policy Uncertainty", JF 72(3) 2017 1213–1252, https://www.kellogg.northwestern.edu/faculty/alirezat/FXAnnouncements.pdf, fetched 2026-11-03, pp. 1215–1217 and Table I). Post-2015 OOS: none (sample ends 2013); A-C40's "expect null" for 6E pre-FOMC is itself untested.
- instruments: 6A, 6B, 6E, 6C (FOMC days), 6J (BoJ days), M6E; FTMO AUDUSD/EURUSD/USDJPY (Swing for the 22h version).
- holding period and expected trades per year: long foreign currency 18:00 ET day −1 → 16:00 ET day 0 (overnight-session hold ≈ 22 h) on FOMC days (8/yr) and BoJ days (8/yr), pooled over four pairs ≈ 64 position-days/yr; variant: positive-differential currencies only, flip after a hawkish surprise.
- data needed: HistData 1m spot (free) for 2010–2026; Databento 6A/6E 1h (≈ $1/root); FOMC/BoJ calendars (free); ZQ 1m at 14:00 ET for the surprise sign (≈ $7 RTH) or FedWatch snapshots.
- expected gross edge per trade: 5–20 bp per announcement day vs 6A RT ≈ 1.8 bp / 6E RT ≈ 1.2 bp → passes the economics screen; n ≈ 64/yr pooled is thin; post-2013 decay unknown.
- firm structure fit: overnight-session futures (18:00 → 16:00 ET, flat before deadlines); FTMO Swing (one swap night) or intraday CFD (09:00 → 16:00 only); news windows: the 14:00 ET statement is inside the hold → banned at MFFU Rapid/Pro (±2 min incl. resting orders) and Lucid Daily; allowed at Topstep, Bulenox, FTMO Swing.
- nearest closed relative: E2-05 (pre-FOMC drift ES/NQ) and A-C40 (pre-announcement premium with 6E listed as "expect null") — adjacency flagged; this is the published FX announcement-day premium with a post-window component; D2 (daily FX carry) unrelated in horizon.
- decay haircut: 0.5; splits at 2008-12 (ZLB), 2015, 2022.
- plausibility of net Sharpe ≥ 1.5: low — published and cost-robust in-sample, but 16 event days/yr and no post-2013 evidence; the BoJ leg in 6J is the fresher part.
- original: yes only for the BoJ-day 6J leg and the firm-day window (count as 0.5)

## Declined in these lanes (cite the inherited id; no new row)

- Commodity index roll windows (GSCI 5th–9th and BCOM 6th–10th business days, the January reweight, USO/UNG rolls) in CL/GC/ZC: closed by pre-sweep A-C17 and the common-brief negative row "Goldman-roll front-running post-2004". New confirming evidence this run: Yan, Irwin & Sanders, J. Commodity Markets 26 (2022) — GSCI annual rebalancing impact "modest and temporary", no front-running profit (sunshine trading), https://www.sciencedirect.com/science/article/abs/pii/S2405851321000295; Irwin, Sanders & Yan, "The order flow cost of index rolling in commodity futures markets", AEPP 45(2) 2023 1025–1050, https://ideas.repec.org/a/wly/apecpp/v45y2023i2p1025-1050.html; Bessembinder, Carrion, Tuttle & Venkataraman, "Liquidity, resiliency and market quality around predictable trades", JFE 121(1) 2016 142–166 — USO roll days show narrower spreads, deeper books and better resiliency, USO pays ≈ 25 bp per roll, no predatory profits (CFTC WP version https://www.cftc.gov/sites/default/files/idc/groups/public/@economicanalysis/documents/file/oce_predatorysunshine0314.pdf; all search snippets 2026-11-03).
- Pre-announcement drift before scheduled US macro releases in ZN/ES: A-C12 and the common-brief negative row (lock-up reforms 2014/2020). Kurov, Wolfe & Gilbert, FRL 40 (2021): the equity pre-FOMC drift disappeared after 2015.
- Pre-FOMC drift in ES/NQ (E2-05 closed) and its FTMO Swing 22h version (P-C14, low): no new mechanism; the Treasury day −1 drift is registered separately as C-2-09.
- LETF-sized or GEX-conditioned last-half-hour momentum in ES/NQ (A-C24 variants): H0006/H0019; the commodity (C-1-06) and Treasury (C-1-07) LETF flows are kept because the instruments, windows and flow sizes differ.
- Macro-reaction trading in FX futures around ECB/BoE/NFP/CPI (6E/6B): Krueger's "29 of 580 event windows significant = chance" (lit-practitioner closed-family cross-references) and the E2 closure; Conrad & Lamla (JMCB 2010, https://www.peio.me/wp-content/uploads/2014/04/Conf1_Conrad.Lamla_EUR.USD_.ECB_.Monetary.Policy.pdf) document statement-content effects, not a tradable drift; Mueller et al. find no announcement-day premium for central banks other than the Fed and BoJ.
- Bare OPEX-week, pre-holiday, day-of-week and crypto weekday effects (A-C29, A-C31): negative evidence in the common brief.
- 0DTE pinning as a directional rule (A-C26): downgraded by Elms (2026); recorded as C-1-10 kill-test only.
- Quarter-end CIP/FX-swap "turn" in 6E/6J calendar spreads and Treasury futures delivery rolls: no outright direction; not registrable at the firms.

## Summary table

| id | name | lane | evidence grade | plausibility | firm structure | data cost | original |
|---|---|---|---|---|---|---|---|
| C-1-01 | Month-end Treasury index-extension strike, firm-day capture | 1 | WP + central-bank data + blog replication | low-medium | intraday / overnight-session futures | $2 (1h) to $40 (ZN+UB 1m full) | yes (variant B) |
| C-1-02 | Month-end cross-asset rebalancing, bond leg only | 1 | WP (NBER 2025) + blog with code | low | overnight-session futures | $0–20 | yes |
| C-1-03 | Auction-day inverted V in ZN/ZB/UB | 1 | central-bank staff report 2026 + peer-reviewed | low | intraday futures | $14 (shared) | no |
| C-1-04 | WMR fix legs + month-end / MSCI-date intensity | 1 | peer-reviewed (JF 2024, JIMF 2018) | low (daily) / low-medium (intensity days) | intraday futures; FTMO intraday or Swing | $0–40 | partial |
| C-1-05 | Tokyo 9:55 fix in 6J | 1 | peer-reviewed + blog forward test | low | overnight-session futures; FTMO intraday | $0–20 | no |
| C-1-06 | Commodity LETF settlement-time rebalancing NG/CL/GC/SI | 1 | own idea + peer-reviewed analogues + issuer data | low | intraday futures; FTMO intraday | $28 | yes |
| C-1-07 | Treasury LETF close rebalancing ZB/UB | 1 | own idea + Fed WP analogue | very low-low | intraday futures | $20 (shared) | yes |
| C-1-08 | ES post-cash-close reversal 16:00–16:07 | 1 | peer-reviewed analogue (stocks) | low | intraday futures; FTMO intraday | $0–20 | yes |
| C-1-09 | Index-rebalance days ES/NQ/RTY and CFDs | 1 | blog holdout + peer-reviewed negative | low | intraday futures; FTMO intraday | $7 | no |
| C-1-10 | ES expiration pinning: negative update / amplification kill-test | 1 | WP (negative) + peer-reviewed (old) | very low | intraday | $0 | no |
| C-1-11 | FX option NY-cut strike gravitation 6E/6J | 1 | practitioner only | very low-low | intraday futures; FTMO intraday | $0–14 | yes |
| C-1-12 | Daily 4pm Treasury strike window ZN | 1 | central-bank blog (volume only) | very low | intraday futures | $0 (shared) | no |
| C-2-01 | NG storage announcement-day premium | 2 | peer-reviewed (abstract only) | low-medium | overnight-session / intraday futures; FTMO | $7 | no |
| C-2-02 | Pre-EIA CL drift with API conditioning | 2 | peer-reviewed (abstracts) | low | intraday futures; FTMO intraday | $7 | yes |
| C-2-03 | EIA CL first-reaction fade | 2 | peer-reviewed + blog holdout | low | intraday futures; FTMO intraday | $0 (shared) | no |
| C-2-04 | WASDE minute-data update + limit-lock reopen | 2 | peer-reviewed + fact sheet with minute data | very low (a) / low (b) | intraday / overnight-session futures | $2–40 | yes (b) |
| C-2-05 | Crop Progress → 20:00 ET reopen ZC/ZS | 2 | peer-reviewed (old, abstract) | low | overnight-session futures | $2–40 | yes |
| C-2-06 | Livestock reports → LE/HE Monday open | 2 | peer-reviewed (old) | very low | intraday futures | $14 | yes |
| C-2-07 | LBMA auctions: Nilsson kill-test + round-imbalance leg | 2 | peer-reviewed + WPs | low | overnight-session / intraday futures; FTMO | $20 | yes (b) |
| C-2-08 | GC/SI option-expiry settlement pinning | 2 | own idea | very low | intraday futures; FTMO intraday | $0 (shared) | yes |
| C-2-09 | FOMC three-day window in long Treasuries, overnight-session holds | 2 | peer-reviewed (RFS 2025) + WP 2026 | low-medium | overnight-session futures | $2–40 | yes |
| C-2-10 | Post-FOMC drift ZN via overnight-session holds | 2 | WP (NBER) | very low-low | overnight-session futures | $2–9 | yes (window) |
| C-2-11 | FOMC press-conference continuation ZN | 2 | peer-reviewed (JFE 2022) | low | intraday futures | $14 | no |
| C-2-12 | Auction-result surprise continuation ZN/UB | 2 | peer-reviewed (A&F 2021, JPE 2024) | low | intraday futures | $0 (shared) | no |
| C-2-13 | FOMC/BoJ-day FX premium 6A/6B/6E/6J | 2 | peer-reviewed (JF 2017) | low | overnight-session futures; FTMO Swing | $0–9 | partial |

Counts: 25 candidates (lane 1: 12; lane 2: 13); original "yes": 14 (C-1-01, C-1-02, C-1-06, C-1-07, C-1-08, C-1-11, C-2-02, C-2-04, C-2-05, C-2-06, C-2-07, C-2-08, C-2-09, C-2-10) plus 2 partial (C-1-04, C-2-13). Plausibility: 0 high, 0 medium, 4 low-medium (C-1-01, C-2-01, C-2-09, and the intensity subset of C-1-04), 13 low, 8 very low. Candidates that already fail the economics screen on the published magnitudes and are kept only as kill-tests or documentation: C-1-02 (ZN leg), C-1-10, C-1-12, C-2-04(a), C-2-06, C-2-08, C-2-10.

Suggested Databento purchase for these two lanes (within the $94 ceiling, no paid call before D-005 is cleared): ZN full session 1m ($20) + UB full session 1m ($20) serve C-1-01/02/03/07/12 and C-2-09/10/11/12; NG RTH 1m ($7) and CL RTH 1m ($7) serve C-2-01/02/03 and C-1-06; GC full session 1m ($20) serves C-2-07/08 and C-1-06; grains and FX at 1h ($1/root) or free HistData for first passes. Total ≈ $76. ES windows use the in-hand ES 1m RTH file where it covers 16:00–16:15 (verify), otherwise $20 more.

Pre-sweep entries extended here (not re-listed without new evidence or twist): A-C06 (C-1-04), A-C07/P-C12 (C-1-05), A-C09 (C-1-01), A-C10 (C-1-03, C-2-12), A-C11 (C-2-10), A-C13 (C-1-12), A-C14 (C-2-02, C-2-03), A-C16 (C-2-04), A-C18 (C-2-07), A-C24 (C-1-06, C-1-07), A-C25 (C-1-08), A-C26 (C-1-10, C-2-08), A-C40/E2-05 (C-2-09, C-2-13 adjacency), P-C09 (C-1-09). Not touched (no new evidence found): A-C08, A-C12, A-C15, A-C17 (closed), A-C19, A-C28, A-C29, A-C31.

## Blocked hosts and sources not fetched (fetch date 2026-11-03; nothing routed around)

Blocked or refused:
- papers.ssrn.com — 403 (pre-existing; Elms 2026, Smales, Gómez-Cram–Grotteria, Prokopczuk et al. SSRN copies not read)
- centaur.reading.ac.uk — anti-bot interstitial ("Anubis") on the record page and the accepted-manuscript PDF of the NG announcement-day paper
- livrepository.liverpool.ac.uk — record page readable; accepted manuscript embargoed until 2026-11-30
- onlinelibrary.wiley.com — 403 (Smales 2021 open-access page; KMW JF page)
- ageconsearch.umn.edu — 403 on record pages and PDF files (Rousse–Sévi FEEM PDF, Ye–Karali AAEA PDF, Lehecka JARE record)
- tandfonline.com — 403 (Applied Economics Letters 2024 WASDE volatility paper)
- direxion.com and etfdb.com — 403 (TMF/TMV AUM not verified)
- api.semanticscholar.org — HTTP 429 rate limits after a burst (three calls succeeded; Lehecka, Bessembinder et al., Ivanov–Lenkey, Gómez-Cram–Grotteria abstracts were taken from search snippets instead)
- Previously reported and unchanged: datafeed.dukascopy.com, lucidtrading.com

Fetched and used (PDF text extracted locally with pdftotext into the scratchpad): KMW Bank of Canada SWP 2021-48; Mueller–Tahbaz-Salehi–Vedolin JF 2017 (Kellogg copy); Pan & Peng 2026 (SAIF copy); Harvey–Mazzoleni–Melone NBER w33554; FRBNY SR 1188 (Oct 2026 revision); Mixon & Tuzun 2018 (CFTC); Somogyi–Wallen–Xu HBS WP 26-033; Crain–Hoelscher–Jones 2020 (ACRN); Park FSA104 (Arkansas); plus the two NY Fed Liberty Street posts, the Allocate Smartly and Quantitativo posts, the Harbourfront summary of Elms, the Quantpedia Hillenbrand page, and six ProShares fund pages.

Seen only as abstracts or search snippets (full text not read): Prokopczuk–Wese Simen–Wichmann 2021; Rousse & Sévi 2019; Ye & Karali 2016; Miao et al. 2018; Adjemian & Irwin 2018; Lehecka 2014; Schroeder–Mintert–Blair; Smales 2021; Sigaux 2024; Ray–Droste–Gorodnichenko 2024; Hillenbrand 2025 (full PDF at Banca d'Italia not fetched); BIS WP 1252; Ito & Yamada 2018; Greenwood & Sammon 2025; Bogousslavsky & Muravyev 2023; Jegadeesh & Wu 2022; Tuzun 2013; Ivanov & Lenkey 2018; Yan–Irwin–Sanders 2022; Irwin–Sanders–Yan 2023; Bessembinder et al. 2016; Aspris et al. 2015/2017; Nilsson 2015 (via Crain et al.); Kurov–Wolfe–Gilbert 2021; Gómez-Cram & Grotteria 2022; Zhao 2026 (arXiv 2608.03703, Korean LETFs — abstract only, not used as evidence); Melvin & Prins 2015; FSB 2014.
