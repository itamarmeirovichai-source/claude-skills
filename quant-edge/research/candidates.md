# Candidates — Department B merged and prioritized list

- date: 2026-11-06
- author: Prioritizer (Mechanism Analyst and Decay Analyst checks folded in, per D-017); no web access, no market data used; nothing here is an edge, a signal or "promising" — every row is a hypothesis for pre-registration
- inputs: six scout files `research/sweep/{academic-flows-events, academic-session-momentum, practitioner-code, microstructure-ml, session-cfd-swing, idea-generator-adversary}.md` (149 candidate blocks), pre-sweep `~/quant-edge-inherited/pr26/prompts/research/lit-academic.md` (36) and `lit-practitioner.md` (30), `registry.csv` (106 rows) for closed relatives, `briefs/00-common.md`, `briefs/B-sweep-common.md`, `PARAMETERS.md` (Day-0 amendments)
- merge log: `research/sweep/merge-log.md`
- id convention: scout ids collide across files (C-9-01..05, C-10-01, C-8-01 exist twice), so every id carries its source file tag: AF = academic-flows-events, AS = academic-session-momentum, PC = practitioner-code, MS = microstructure-ml, SC = session-cfd-swing, IG = idea-generator-adversary, pre-sweep = lit-academic (A-Cxx) / lit-practitioner (P-Cxx)

## Totals (true counts, no padding)

- scout blocks read: 149; pre-sweep entries checked: 66
- merged away: 15 scout blocks into other scout blocks; 26 pre-sweep entries attached to the scout block that extends them (see merge log)
- declined: 4 scout blocks (negative evidence or no firm structure) and 22 pre-sweep groups (closed family, negative evidence, no firm fit) — Declined appendix; each scout file also has its own declined list (≈ 90 items) that is not re-listed
- pre-sweep accounting (66 = 36 + 30): 26 attached to a scout row, 6 carried as own rows, 1 declined through its scout row (A-C26 via AF C-1-10), 33 declined in 22 groups
- pre-sweep entries carried as their own rows (strong or untouched, re-listed by no scout): 6 (A-C21, A-C08, P-C08, P-C10, P-C13; P-C02 as a layer)
- **surviving entries: 136** = **114 candidate mechanisms** (ranked table A) + **22 construction layers / overlays / measurement rows** (table B; no standalone mean claim, ranked separately so they cannot crowd out edges)
- the brief's target of ≥ 100 candidate mechanisms is met (114) only because the scouts registered many low-rated rows; it is not met with medium-or-better rows
- **original share**: 75 of 136 entries original (55 %), 6 partial (original twist on a published effect), 55 not original; among the 114 mechanisms: 60 original (53 %), 6 partial — the ≥ 30 % target is met
- **plausibility of net Sharpe ≥ 1.5** (mechanisms): high 0; medium 1; low-medium 4; low 80; very low 29. **Medium-or-better: 1; low-medium-or-better: 5** (AS C-4-01, AF C-1-01, AF C-1-04, AF C-2-01, AF C-2-09). No row is plausible as a stand-alone account strategy; the realistic use of the top of the table is a stack of ≥ 5 weakly correlated event sleeves, each of which must still pass Gate v2 alone
- joint-power reminder (PARAMETERS.md Day-0): the 2 × cost criterion certifies only edges whose gross is ≥ ≈ 3 × round-trip cost; the cost-sensitivity score below gives 3 only to rows whose plausible gross AFTER the decay haircut is ≥ 3 × RT, and most rows score 1 (gross ≈ 1–2 × RT or unmeasured)

### Lane coverage (mechanisms / layers)

| lane | mechanisms | layers | note |
|---|---|---|---|
| 1 structural flows with a calendar | 12 | 0 |  |
| 2 scheduled information outside ES/NQ | 13 | 0 |  |
| 3 overnight session at futures firms | 5 | 0 |  |
| 4 intraday momentum/reversal, untested markets | 10 | 0 |  |
| 5 cross-market lead-lag with a mechanism | 11 | 3 |  |
| 6 breadth and portfolio construction | 3 | 4 | THIN |
| 7 regime-conditional | 1 | 5 | THIN |
| 8 FTMO Swing across the close (+ Asia/Europe session rows) | 9 | 0 |  |
| 9 order-flow proxies from bars | 8 | 4 |  |
| 10 ML done right | 2 | 3 | THIN |
| 11 previous org's open directions | 4 | 0 | THIN |
| 12 the market's adversary | 30 | 0 |  |
| 13 text and alternative data (free) | 6 | 3 |  |

Thin lanes: 6, 7, 10, 11. Lane 6 and 7 rows are almost all layers (no edge of their own); lane 10 has two mechanism rows, both expected null (two 2026 falsification studies on MNQ); lane 11 is the inherited prereg_orb30 plus low-rated stack legs; lane 3 has five rows, none above 14 points, and its best-documented member (C-3-01) is flat since 2021. Lane 12 (32 scout blocks) is the deepest but almost entirely own-idea evidence (evidence score 0–1) whose shared prerequisite is the ≈ $14–40 micro/mini footprint study.

### Firm-structure coverage (mechanisms; a row can fit several)

| structure | rows |
|---|---|
| intraday futures (flat by the firm deadline) | 79 |
| overnight-session futures (after 18:00 ET, flat before the deadline) | 30 |
| FTMO intraday CFD | 60 |
| FTMO Swing across the close | 19 |
| no firm structure | 0 |

### Data: free vs Databento (mechanisms)

| class | rows |
|---|---|
| Databento | 53 |
| free first pass | 47 |
| Databento (shared root) | 10 |
| Databento / outside plan | 4 |

"free first pass" = a $0 test exists (HistData FX/CFD 1m, Yahoo/FRED/CFTC/CBOE daily, data in hand) even if the full test later wants Databento minute bars; "Databento (shared root)" = no incremental cost once a root already bought for another row is in hand. Cheapest high-coverage purchase seen across the scout files: ZN + UB full-session 1m (≈ $40) serves nine lane-1/2 Treasury rows (C-1-01/02/03/07/12, C-2-09/10/11/12); ES + MES full session (≈ $40) serves the prop-adversary rows (C-12-01/03/21) and C-1-08/C-12-08/C-12-15; GC full session (≈ $20) serves most gold rows (C-2-07, C-3-03, C-4-02, C-4-06, C-12-04, C-12-20); NG + CL RTH (≈ $14) serves the EIA/energy rows (C-2-01/02/03, C-1-06, C-12-10) — together ≈ $114, over the $94 ceiling, so the batch-1 order must choose (1h bars at ≈ $1/root are enough for the first pass of most lane-1/2/3 rows).

## Scoring

Seven criteria, 0–3 each, total /21: **M** mechanism (3 = a named forced trader with a known time and size; 0 = none); **E** evidence after the decay haircut (3 = peer-reviewed full text with a post-2015 out-of-sample number that survives the haircut; 2 = peer-reviewed or full working paper, in-sample; 1 = abstract/blog/practitioner or marginal after haircut; 0 = own idea or negative); **C** cost sensitivity at the common-brief floors, on the haircut gross (3 = ≥ 3 × RT, 2 = 2–3 ×, 1 = ≈ 1–2 × or unmeasured, 0 = fails); **F** firm compatibility (3 = fits ≥ 2 structures without a clause problem; 2 = one structure cleanly; 1 = only at some firms / a clause binds; 0 = none); **D** data within the $94 plan or free (3 = free or in hand; 2 = ≤ $10 incremental; 1 = ≤ $40; 0 = over the ceiling or not purchasable); **X** closed-family distance (3 = nothing near; 2 = adjacent but a different mechanism or market; 1 = conditioner or transfer of a closed family; 0 = inside a closed family, survives only on new markets/dates); **P** plausibility of net Sharpe ≥ 1.5 as one sleeve (0 very low, 1 low, 2 low-medium/medium, 3 high). Decay haircut: 0.5 for published mechanisms, 0.7 for original, never above 0.8. Ties are broken by P, then E, then C.

The analyst line in each brief is the folded-in Mechanism/Decay Analyst check: closed-family overlap (cited id); look-ahead by construction; economics screen (gross per trade vs max(2 ticks, 2 × RT), trades/yr, Carver speed limit where turnover is high); decay haircut and the institutional change dates that split the sample; firm fit and the clauses touched.

## A. Ranked table — candidate mechanisms

| rank | id | name | lane | score | plausibility | evidence | firm structure | data cost | original | nearest relative |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | AS C-4-01 | Cross-sectional overnight–intraday reversal among ES/NQ/YM/EMD/NKD, open → close | 4 | 16 | medium | peer-reviewed abstract or full WP (B) | IF/FI | $0.25 (1d) → $5 (1h) | no | H0012, H0017, E1-08..10 |
| 2 | AF C-1-01 | Month-end Treasury index-extension strike, firm-day capture | 1 | 16 | low-medium | WP + central-bank data + blog replication | IF/ONF | $2 (1h) to $40 (ZN+UB 1m full) | partial | H0023 |
| 3 | AF C-1-04 | WMR fix legs + month-end / MSCI-date intensity | 1 | 16 | low-medium | peer-reviewed (JF 2024, JIMF 2018) | IF/FI/FS | $0–40 | partial | D2, D4 |
| 4 | AF C-1-09 | Index-rebalance days ES/NQ/RTY and CFDs | 1 | 16 | low | blog holdout + peer-reviewed negative | IF/FI | $7 | no | H0006, H0023 |
| 5 | AF C-2-01 | NG storage announcement-day premium | 2 | 15 | low-medium | peer-reviewed (abstract only) | IF/ONF/FI | $7 | no | E2 |
| 6 | SC C-13-01 | ECB press-conference tone change → EU50/GER40 continuation | 13 | 15 | low | peer-reviewed (JFQA 2025) | FI | $0 | no | E2 |
| 7 | AF C-2-13 | FOMC/BoJ-day FX premium 6A/6B/6E/6J | 2 | 15 | low | peer-reviewed (JF 2017) | ONF/FI/FS | $0–9 | partial | E2-05, A-C40 |
| 8 | IG C-12-15 | Month-end multi-asset rebalancing, equity leg into the last day's close | 12 | 15 | low | WP (NBER 2025) + twist | IF/FI/FS | $0–7 | no | H0023, H0006 |
| 9 | AF C-1-05 | Tokyo 9:55 fix in 6J | 1 | 15 | low | peer-reviewed + blog forward test | ONF/FI | $0–20 | no | D4 |
| 10 | AS C-4-07 | Hedging-overshoot reversal after a large last half hour, 18:00 ET → next close, ... | 4 | 14 | low | peer-reviewed, full text (A) | IF/ONF/FS | $20 extra (NQ/SI/NG RTH) | yes | H0006, H0019, H0012 |
| 11 | IG C-11-01 | prereg_orb30 as written (A/B/C; OOS row only if A's D1 p5 > 0) | 11 | 14 | low | PR + WP + inherited prereg | IF/FI | $0 (+$7 OOS) | no | H0020, H0005, H0011 |
| 12 | SC C-8-05 | Energy term-structure carry on FTMO's own swap sign (USOIL/UKOIL/NATGAS/HEATOIL) | 8 | 14 | low | peer-reviewed family; swap pass-through fetched | FS | ≈ $0.2 | partial | D2-04, H0007 |
| 13 | AS C-3-06 | Treasury-futures day/night sign asymmetry (long day leg, short overnight-session leg; UB ... | 3 | 14 | low | peer-reviewed, full text (A) | IF/ONF/FI | $3 (ZN/ZF/UB 1h) | yes | none |
| 14 | IG C-12-10 | Platts Dated Brent MOC window 11:00–11:30 ET in CL / Brent CFD | 12 | 14 | low | PR (JBF 2018) + OWN (fade leg) | IF/FI | $0–7 | partial | none |
| 15 | IG C-12-04 | CME margin-hike next-open liquidation in GC/SI/CL/NG — TOP10 (7) | 12 | 14 | low | PR (daily) + OWN | IF/ONF/FI | $28 (shared) | yes | H0012, H0017 |
| 16 | IG C-12-06 | Vol-control / risk-parity deleveraging into the close, 1–3 days after a vol jump — TOP10 ... | 12 | 14 | low | PRAC (bank model) + OWN | IF/FI/FS | $0–7 | yes | H0006, H0019 |
| 17 | IG C-12-24 | Buyback-desk dip buying 13:00–15:50 on down days outside blackout, with in-blackout ... | 12 | 14 | low | PRAC + negative daily study + OWN | IF/FI | $0–7 | yes | G2 |
| 18 | AF C-2-09 | FOMC three-day window in long Treasuries, overnight-session holds | 2 | 13 | low-medium | peer-reviewed (RFS 2025) + WP 2026 | ONF | $2–40 | yes | E2-05 |
| 19 | SC C-13-02 | FOMC press-conference vocal tone → US500 drift (new data vs closed E2) | 13 | 13 | low | peer-reviewed (AER 2023) | IF/FI/FS | $0–7 | no | E2-01..04 |
| 20 | AF C-1-02 | Month-end cross-asset rebalancing, bond leg only | 1 | 13 | low | WP (NBER 2025) + blog with code | ONF | $0–20 | yes | H0023 |
| 21 | AF C-1-03 | Auction-day inverted V in ZN/ZB/UB | 1 | 13 | low | central-bank staff report 2026 + peer-reviewed | IF | $14 (shared) | no | E2 |
| 22 | AF C-2-03 | EIA CL first-reaction fade | 2 | 13 | low | peer-reviewed + blog holdout | IF/FI | $0 (shared) | no | E2 |
| 23 | AF C-2-07 | LBMA auctions: Nilsson kill-test + round-imbalance leg | 2 | 13 | low | peer-reviewed + WPs | IF/ONF/FI | $20 | yes | none |
| 24 | AF C-2-12 | Auction-result surprise continuation ZN/UB | 2 | 13 | low | peer-reviewed (A&F 2021, JPE 2024) | IF | $0 (shared) | no | none |
| 25 | IG C-12-08 | VIX ETP leverage rebalancing → ES delta leg 15:45–16:15 — TOP10 (9) | 12 | 13 | low | PR (VX) + OWN (ES leg) | IF | $0–20 | yes | G1, H0006, H0019 |
| 26 | SC C-13-04 | KRT position-change liquidity provision, post-release, across 16 FTMO commodity CFDs | 13 | 13 | low | peer-reviewed (JF 2020), 1994–2012 | FS | ≈ $1 | no | P-C17 |
| 27 | SC C-8-06 | Commodity multi-day dip buy with the real swap sign (crude earns carry) | 8 | 13 | low | blogs, paywalled rules | FS | $0–0.15 | no | G2-01..07 |
| 28 | AS C-3-03 | Gold overnight (Asian/London hours) drift as an 18:00 ET → 08:20 ET GC/MGC hold | 3 | 13 | low | peer-reviewed abstract or full WP (B) | ONF/FI | $1 (GC 1h) → $20 (1m) | yes | D4 |
| 29 | IG C-12-16 | JHEQX quarter-end collar and monthly buffer-ETF resets into the close | 12 | 13 | low | PRAC/press + OWN | IF | $0–7 | yes | H0006, H0019, A-C26 |
| 30 | SC C-8-10 | HSI after-hours move → first-30-minute day-session reversal on HK50 | 8 | 13 | low | thesis/JFM ≈ 2000 (HK); Miwa 2019 (Nikkei) | FI | $0 | yes | H0012, H0017 |
| 31 | AS C-4-06 | VIX/RV-gated 5–30-minute reversal in gold | 4 | 13 | low | WP abstract / snippet (C) | IF/ONF/FI | $0 extra | no | H0013, H0014 |
| 32 | IG C-12-27 | Nikkei SQ morning and HSI all-day-average expiry mechanics in NKD / JP225 / HK50 | 12 | 13 | low | FIRM/exchange + OWN | ONF/FI | $0 (HistData) | yes | none |
| 33 | IG C-11-03 | Real value measures (AMP 2013) as the FTMO Swing stack's missing leg | 11 | 13 | very low | PR | FS | $0 | no | D2 |
| 34 | AF C-2-02 | Pre-EIA CL drift with API conditioning | 2 | 12 | low | peer-reviewed (abstracts) | IF/FI | $7 | yes | none |
| 35 | IG C-12-26 | Index-expiry settlement auctions: ES SOQ 09:30 and DAX 13:00 CET post-auction reversal | 12 | 12 | low | PR (1980s–90s) + PRAC | IF/FI | $0–7 | partial | H0012, H0017 |
| 36 | pre-sweep P-C10 | Late-session breakouts after an early whipsaw (index), pre-sweep P-C10 | 4 | 12 | low | practitioner in-sample (Krueger range setups C/D) | IF/FI | $0 (CFD HistData / ES in hand) | no | H0020, D4-04 |
| 37 | AF C-2-05 | Crop Progress → 20:00 ET reopen ZC/ZS | 2 | 12 | low | peer-reviewed (old, abstract) | ONF | $2–40 | yes | H0012, H0017 |
| 38 | AS C-3-01 | Regime-gated overnight drift 02:00–03:00 ET (authors report ≈ 0 since 2021) | 3 | 12 | low | peer-reviewed, full text (A) | ONF/FI | $20 (ES 1m full session) | yes | H0009 |
| 39 | AS C-3-04 | Nikkei night-session overreaction → Tokyo day-session reversal in NKD/NIY | 3 | 12 | low | peer-reviewed abstract or full WP (B) | ONF/FI | $1 → $20 (NKD) | no | H0012, H0017 |
| 40 | AS C-5-03 | US close → Tokyo open: prior-day S&P return and Nikkei's first 30 minutes | 5 | 12 | low | WP abstract / snippet (C) | ONF/FI | $0 extra | no | H0012, H0017 |
| 41 | AS C-5-05 | Crack-spread residual mean reversion after a one-leg shock (CL/HO/RB) | 5 | 12 | low | WP abstract / snippet (C) | IF | $3 (1h) → $20 | no | none |
| 42 | IG C-12-20 | Round-number stop/take-profit clusters (Osler 2003) on gold and index futures at 1m | 12 | 12 | low | PR (FX 1999–2000) | IF/FI | $0–7 | no | H0001, H0004 |
| 43 | pre-sweep A-C21 | VIX/realized-vol-conditioned intraday mean reversion in ES/NQ (Nagel-style liquidity ... | 4 | 12 | low | peer-reviewed mechanism (Nagel RFS 2012; Kang-Lin-Xiong ... | IF/FI | $0-7 (ES 1m RTH in hand under licence ... | no | H0013, H0014 |
| 44 | SC C-8-11 | European closing-auction reversal at index level (GER40/UK100/FRA40 after 17:35/16:35) | 8 | 12 | low | working paper (stocks), numbers inconsistent (14 % vs 23 %) | FI | $0 | no | H0006, H0019 |
| 45 | IG C-12-05 | Crypto liquidation-cascade exhaustion → MBT / FTMO BTCUSD — TOP10 (8) | 12 | 12 | low | OWN (data limited: no free liquidation feed) | ONF/FI | $0–20 | yes | D3-01..11 |
| 46 | IG C-12-18 | Sunday 18:00 ET reopen overshoot fade, BTC-weekend sign filter | 12 | 12 | low | OWN | ONF/FI | $0 (HistData) → $60 | yes | H0012, H0017 |
| 47 | IG C-12-12 | VIX-settlement Wednesdays: ES 09:31–09:45 fade of the SOQ-hedge unwind | 12 | 12 | very low | PR (auction anomaly) + OWN (ES leg) | IF | $0–20 | yes | E2, H0012, H0017 |
| 48 | pre-sweep A-C08 | Around-the-clock USD time-of-day seasonality (Breedon-Ranaldo local-hours depreciation), ... | 1 | 12 | very low | peer-reviewed (JMCB 2013; KMW JF 2024); practitioner ... | IF/FI | $0 (HistData FX 1m) | no | D4, P-C21 |
| 49 | SC C-13-05 | Google-search FEARS → two-day US500 reversal; Preis-style timing recorded negative | 13 | 11 | low | peer-reviewed (RFS 2015); negative replications of the ... | FS | $0 | no | G2 |
| 50 | AF C-2-11 | FOMC press-conference continuation ZN | 2 | 11 | low | peer-reviewed (JFE 2022) | IF | $14 | no | E2-01..04 |
| 51 | AS C-5-09 | US first half-hour → European last half-hour (cross-country ITSM, LSU) | 5 | 11 | low | peer-reviewed abstract or full WP (B) | FI | $0 (CFD history + ES/SPY 1m in hand) | no | D4-01 |
| 52 | PC C-6-05 | CO-OC overnight→intraday reversal across commodity and rates futures (DKW futures ... | 6 | 11 | low | in-sample pages / code without results (C) | IF/FI | $14 (1h, 14 roots) → $280 (1m, over ... | no | none |
| 53 | SC C-8-01 | Night–day asymmetry in non-US indices on CFD terms (long night with one swap / short day ... | 8 | 11 | low | peer-reviewed (US, international portfolios); figure-level ... | FI/FS | $0 (HistData) | no | E1-08..10 |
| 54 | pre-sweep P-C13 | EU pre-open push (08:00-09:00 Berlin) as the direction filter for DAX/FTSE breakouts, ... | 4 | 11 | low | practitioner in-sample (Krueger, 41,668 episodes, t 6.6) | FI | $0 (HistData GRXEUR/UKXGBP) | no | D4-04 |
| 55 | AF C-1-08 | ES post-cash-close reversal 16:00–16:07 | 1 | 11 | low | peer-reviewed analogue (stocks) | IF/FI | $0–20 | yes | H0006, H0019 |
| 56 | AS C-4-04 | Drift-burst fade after high-volume negative bursts, ES/NQ/CL/GC | 4 | 11 | low | WP abstract / snippet (C) | IF/ONF/FI | $40 (ES+GC) → $80 | yes | A-C20 |
| 57 | AS C-5-10 | Soybean-crush opening reversal (GPM open vs prior close, filtered), ZS/ZM/ZL day trade | 5 | 11 | low | peer-reviewed, full text (A) | IF | $0.15 (1d) → $20 (1m) | no | none |
| 58 | MS C-9-08 | Volume-surprise persistence as the VWAP/TWAP order-splitting footprint → continuation | 9 | 11 | low | own idea; peer-reviewed background | IF | $0–7 incremental | yes | H0021, H0022 |
| 59 | pre-sweep P-C08 | Index-level volume shock -> overnight-session long (transfer of the single-stock effect), ... | 3 | 11 | low | practitioner (stocks; TabNet Sharpe ~1.1); index transfer ... | ONF/FI | $0-7 | no | H0012, H0017 |
| 60 | AS C-5-07 | US close → European cash open fade, GER40/FRA40/EU50/UK100 | 5 | 11 | low | own idea by analogy (D) | FI | $0 (CFD history) | yes | H0012, H0017, D4 |
| 61 | IG C-12-14 | PBoC fix surprise → 6A/M6A 20:16–20:45 ET | 12 | 11 | low | PRAC + OWN | ONF/FI | $0–20 | yes | D4, A-C05 |
| 62 | SC C-8-02 | Halloween / Sell-in-May six-month long in non-US indices, swap-netted | 8 | 11 | very low | peer-reviewed, OOS 1998–2015 panels | FS | $0 | no | H0023 |
| 63 | SC C-8-09 | Closure premium through multi-day holidays (Golden Week, LNY, Easter) in JP225/HK50/GER40 | 8 | 11 | very low | own idea; old pre-holiday literature adjacent | FS | $0 | yes | H0023, A-C29 |
| 64 | AF C-2-04 | WASDE minute-data update + limit-lock reopen | 2 | 11 | very low | peer-reviewed + fact sheet with minute data | IF/ONF | $2–40 | yes | none |
| 65 | AS C-4-02 | ITSM into the COMEX gold settlement, last-10-minute execution, LSU gates | 4 | 10 | low | peer-reviewed abstract or full WP (B) | IF/FI | $0 extra | no | H0006, H0019, D4-01 |
| 66 | AS C-4-05 | Dealer-gamma session regime switch — 2026 evidence update to A-C23 | 4 | 10 | low | peer-reviewed abstract or full WP (B) | IF/FI | $7 (ES RTH); position data outside plan | no | H0019, A-C23 |
| 67 | IG C-12-07 | CTA trigger-level crossing → last-hour continuation, 6 roots — TOP10 (5) | 12 | 10 | low | PRAC + OWN | IF/FI/FS | $35 | yes | H0006, H0019, D4-01 |
| 68 | IG C-12-17 | Large-gap continuation as margin-call liquidation, micro-gated (adjacent to closed ... | 12 | 10 | low | OWN + inherited negative fade | IF/FI | $7 | yes | H0012, H0017 |
| 69 | IG C-12-11 | NG/CL expiry-day final settlement window, hedged via the 2nd month | 12 | 10 | low | OWN (enforcement record as mechanism) | IF/ONF | $28 | yes | none |
| 70 | IG C-12-13 | Deribit 08:00 UTC expiry pin/release → MBT / BTCUSD | 12 | 10 | low | PRAC/press + OWN | ONF | $0–20 | yes | D3-09 |
| 71 | IG C-12-23 | Failed 30-minute ORB fade (the ORB crowd's stops), paired with C-11-01 | 12 | 10 | low | OWN | IF/FI | $0–7 | yes | H0020, prereg_orb30 |
| 72 | AF C-1-06 | Commodity LETF settlement-time rebalancing NG/CL/GC/SI | 1 | 10 | low | own idea + peer-reviewed analogues + issuer data | IF/FI | $28 | yes | H0006, H0019 |
| 73 | IG C-12-03 | Prop daily-loss / trailing-DD stop-out cascade, micro-share trigger — TOP10 (2) | 12 | 10 | low | FIRM + OWN | IF | $14–28 | yes | none |
| 74 | IG C-9-10 | Micro-vs-mini BVC divergence as a 15-minute reversal signal | 9 | 10 | low | OWN | IF | $28 | yes | none |
| 75 | MS C-9-06 | Close-location flow (CLV × volume) vs BVC head-to-head | 9 | 10 | low | own hypothesis; practitioner code without stats | IF | $0 incremental | yes | none |
| 76 | PC C-8-01 | Carver trend + carry with vol-regime multiplier as an FTMO Swing sleeve, swap-filtered ... | 8 | 10 | very low | public code + printed results (A) | FS | $5 (1d + parent symbology) | no | D2-01, D2-09, H0007 |
| 77 | AF C-1-12 | Daily 4pm Treasury strike window ZN | 1 | 10 | very low | central-bank blog (volume only) | IF | $0 (shared) | no | none |
| 78 | AF C-1-11 | FX option NY-cut strike gravitation 6E/6J | 1 | 10 | very low | practitioner only | IF/FI | $0–14 | yes | none |
| 79 | SC C-8-12 | Tokyo's new 15:30 JST closing auction → JP225 reversal at the 16:30 evening reopen ... | 8 | 10 | very low | own idea; institutional change 2024-11-05 | ONF/FI | $0–7 | yes | none |
| 80 | AS C-4-08 | ITSM into settlement in NG/SI/PL/HO (CL excluded by evidence), gated on LETF hedging ... | 4 | 9 | low | peer-reviewed, full text (A) | IF/FI | $26 (NG/SI/PL/HO RTH) | yes | H0006, H0019 |
| 81 | PC C-7-05 | Overnight-session range percentile at 09:29 as the breakout/fade/inactive regime | 7 | 9 | low | own idea, proxy code-backed (D) | IF/FI | $1–20 per root | yes | H0020, D4-04, H0013 |
| 82 | IG C-12-19 | Dealer charm flow midday drift, GEX-gated (folklore kill-test) | 12 | 9 | low | PRAC | IF | $0–7 | no | H0019 |
| 83 | IG C-12-21 | Opening 09:30–09:35 retail thrust fade, top-tercile micro share, with control arm — TOP10 ... | 12 | 9 | low | OWN (+ stock-level retail-imbalance literature) | IF | $14–28 | yes | H0020, H0012, H0017 |
| 84 | IG C-12-22 | Prop news-ban cohort re-entry at 08:33 ET in GC/6E/CL/ZN, traded from exempt firms — ... | 12 | 9 | low | FIRM + OWN | IF/FS | $0 (HistData) → $80 | yes | E2 |
| 85 | IG C-12-01 | Topstep 16:08 / MFFU 16:10 forced flatten, traded from a later-deadline account — TOP10 ... | 12 | 9 | low | FIRM + OWN | IF/FI | $40 (ES+MES full session) | yes | H0006, H0019 |
| 86 | MS C-9-09 | Settlement-window flow proxy → post-settlement reversal (ES/NQ, ZN, 6E, GC, CL, ZC) | 9 | 9 | low | own idea; page-backed procedure facts | IF | $6–20 per root | yes | H0006, H0019 |
| 87 | IG C-11-06 | US-only index mean reversion (G2-06 rules frozen), evaluated only on post-registration ... | 11 | 9 | very low | inherited post-hoc slice | FS | $0 | no | G2-06 |
| 88 | SC C-13-10 | FOMC-minutes / Beige-Book tone divergence → multi-day ZN/UB drift as overnight-session ... | 13 | 9 | very low | Fed research letter (jump), no drift evidence | ONF | ≈ $2 | no | E2 |
| 89 | AS C-5-02 | CL → 6C petro-currency causality at 5–60 min | 5 | 9 | very low | peer-reviewed abstract or full WP (B) | IF/FI | $2 (1h) → $40 | no | none |
| 90 | AF C-2-08 | GC/SI option-expiry settlement pinning | 2 | 9 | very low | own idea | IF/FI | $0 (shared) | yes | A-C26 |
| 91 | SC C-13-09 | MoF weekly securities flows → next-week USDJPY / JP225 drift | 13 | 9 | very low | own idea; data exists, no study found | ONF/FS | $0 | yes | D2 |
| 92 | IG C-11-04 | Bond trend sleeve as a US-day-session hold in ZN/ZB (08:20 → 15:00) with overnight control | 11 | 8 | low | PR (signal, day/night asymmetry) + OWN construction | IF | $2 (1h bars) | yes | H0007, D2-07 |
| 93 | MS C-9-01 | BVC minute imbalance → 5-minute reversal/continuation, calibrated vs aggressor flags ... | 9 | 8 | low | peer-reviewed method + peer-reviewed refutation | IF | $28–80 + 1 week tbbo | no | A-C38 |
| 94 | AS C-5-08 | ZN shock → gold follow-through at 5–30 min | 5 | 8 | low | own idea by analogy (D) | IF/FI | $7 extra (ZN RTH) | yes | none |
| 95 | AF C-2-10 | Post-FOMC drift ZN via overnight-session holds | 2 | 8 | very low | WP (NBER) | ONF | $2–9 | yes | E2-01..04 |
| 96 | AS C-5-06 | NKD ↔ ES minute lead–lag across time zones (trading-place bias) | 5 | 8 | very low | peer-reviewed abstract or full WP (B) | IF/ONF/FI | $2 extra | no | none |
| 97 | IG C-12-09 | Single-stock LETF (NVDL/TSLL) → NQ close on big NVDA/TSLA days | 12 | 8 | very low | PR analogue + issuer AUM | IF/FI | $0–7 | no | H0006, H0019, A-C24 |
| 98 | AF C-1-07 | Treasury LETF close rebalancing ZB/UB | 1 | 8 | very low | own idea + Fed WP analogue | IF | $20 (shared) | yes | H0006, H0019 |
| 99 | IG C-12-29 | Treasury buyback operations 13:40–14:00 ET → ZN/ZB/UB | 12 | 8 | very low | Treasury schedule + OWN | IF | $14 (shared) | yes | none |
| 100 | PC C-6-01 | Intraday TSMOM breadth across ~20 CME futures, 30-min cadence, post-2020 futures only | 6 | 7 | low | in-sample pages / code without results (C) | IF | $20 (1h, 20 roots) → $120–140 (1m, over ... | no | D4-03, H0022, H0005 |
| 101 | MS C-5-15 | Cross-asset BVC flow divergence ES → NQ/RTY/YM | 5 | 7 | low | own idea; peer-reviewed components | IF | ≈ $28 | yes | none |
| 102 | PC C-6-04 | Cross-root signed-volume (BVC) class breadth as a gate on each root's intraday trend ... | 6 | 7 | low | own idea, proxy code-backed (D) | IF | $15 (1h) → $80–110 (1m); +$2.5 trades ... | yes | D4-02, H0005 |
| 103 | PC C-9-01 | First-30-min BVC signed volume → open-to-close sign across non-equity futures | 9 | 7 | low | own idea, proxy code-backed (D) | IF | $40 (6 roots 1m) → $100; +$2.5 trades ... | yes | D4-02 |
| 104 | PC C-9-05 | Hawkes-decayed BVC imbalance momentum as the intraday trend signal | 9 | 7 | low | in-sample pages / code without results (C) | IF | as C-6-01 | yes | H0021, H0022, D4-03 |
| 105 | AS C-5-04 | ZN shock → ES follow-through outside events, stock–bond-correlation regime | 5 | 7 | low | own idea by analogy (D) | IF/FI | $14 (ZN+ES RTH) | yes | E2 |
| 106 | AS C-5-01 | VX-futures → ES lead in high-vol states, signal only | 5 | 7 | very low | peer-reviewed abstract or full WP (B) | IF/FI | VX 1m outside plan | no | G1 |
| 107 | MS C-10-05 | Image-based CNN on intraday bar charts (Jiang–Kelly–Xiu transfer) | 10 | 7 | very low | peer-reviewed (daily equities) | IF | $0 incremental | no | H0001, H0004 |
| 108 | IG C-12-31 | Prop-firm forced roll days: micro front/back spread push | 12 | 7 | very low | FIRM + OWN | IF | $14 | yes | none |
| 109 | MS C-9-07 | Wick-asymmetry absorption proxy → reversal against the wick | 9 | 7 | very low | own idea | IF | $0 incremental | yes | H0013 |
| 110 | IG C-12-28 | 0DTE put-wall first touch (forward-collected CBOE OI; not backtestable) | 12 | 6 | very low | PRAC | IF | $0 | no | H0019, A-C26 |
| 111 | AF C-2-06 | Livestock reports → LE/HE Monday open | 2 | 6 | very low | peer-reviewed (old) | IF | $14 | yes | none |
| 112 | MS C-10-02 | Pre-registered bar-feature gradient boosting with CPCV, PBO, deflated Sharpe (MNQ base ... | 10 | 5 | very low | working papers (arXiv 2026, negative) | IF | $14–40 | no | H0003 |
| 113 | IG C-12-25 | First Notice Day liquidation of non-deliverable longs, GC/SI/CL settlement window ... | 12 | 5 | very low | OWN | IF | $42 | yes | A-C17 |
| 114 | IG C-12-30 | Retail bar-close clock: 15-minute-boundary micro bursts faded (entry-timing overlay) | 12 | 5 | very low | OWN (+ HKS 2010 background) | IF | $14 (shared) | yes | H0021, H0022, H0005 |

Firm codes: IF intraday futures; ONF overnight-session futures; FI FTMO intraday CFD; FS FTMO Swing.

## B. Construction layers, overlays and measurement rows (ranked separately)

These rows claim no mean of their own (variance, breach-rate, fill-quality or sampling claims). They are registered only on top of a sleeve that has its own row; their plausibility score is 0 by definition.

| rank | id | name | lane | score | original | note |
|---|---|---|---|---|---|---|
| L1 | PC C-7-03 | Carver relative-vol attenuation (2 − 1.5 Q) on intraday sleeves, two-sided sign ... | 7 | 13 | no | Carver relative-vol attenuation; +0.05-0.10 Sharpe on daily trend, sign intraday unknown (two-sided test vs Krueger); absorbs pre-sweep A-C30 |
| L2 | pre-sweep P-C02 | Fast mean-reversion execution overlay for intraday trend entries, pre-sweep ... | 6 | 13 | no | fast mean-reversion execution overlay (Concretum: trend net Sharpe 0.87 -> 0.99) on any surviving intraday sleeve |
| L3 | SC C-13-08 | CFTC TFF leveraged-fund positioning extremes as a crash-risk inactivity gate | 13 | 13 | yes | CFTC TFF leveraged-fund extremes as a crash-risk inactivity gate (all structures) |
| L4 | PC C-7-02 | Implied-range sizing overlay (VIX9D/VIX/VIX3M, VVIX, GEX predict width, not ... | 7 | 12 | yes | implied-range sizing (VIX9D/VIX/VIX3M, VVIX, GEX); predicts width not direction; free data in hand |
| L5 | PC C-9-03 | VPIN top decile as fade-inactivity rule and breakout-only regime | 9 | 12 | yes | VPIN top decile as fade-inactivity / breakout-only regime; absorbs MS:C-9-02 (head-to-head vs matched realized-vol gate) |
| L6 | MS C-10-03 | Labelling as a pre-registered design choice (triple-barrier vs trend-scanning ... | 10 | 11 | no | labelling choice (triple-barrier vs trend-scanning vs fixed) as a pre-registered design decision |
| L7 | PC C-6-02 | Decision-clock tranching (three 10-min offsets per sleeve) as a timing-luck ... | 6 | 11 | yes | timing-luck tranching; claims variance reduction only; micro contracts required (none for ZC/NG) |
| L8 | PC C-6-03 | Carver greedy dynamic optimisation with buffering to hold 20–45 micro sleeves ... | 6 | 11 | yes | Carver greedy dynamic optimisation; at $100k the 2021 $25k failure (0.56 vs 1.0) is the warning |
| L9 | PC C-7-01 | Calendar inactivity rules (FOMC day, CPI/NFP morning, roll week) for ... | 7 | 11 | yes | calendar inactivity (FOMC/CPI/NFP/roll week); Krueger levels retracted; FOMC days weaker not negative |
| L10 | PC C-7-04 | HMM vs VIX-threshold regime detectors as inactivity gates ("de-risks, does not ... | 7 | 11 | no | HMM vs VIX-threshold inactivity gates; public walk-forwards show ~0 timing value |
| L11 | IG C-6-06 | Micro-share retail-crowd state variable as a cross-root gate/sizing input | 6 | 10 | yes | micro-contract share of volume as the retail-crowd state variable; prerequisite footprint study for C-12-01/03/21/22 |
| L12 | IG C-7-06 | Clock anchoring and DST-mismatch weeks as construction standard and ... | 7 | 10 | yes | method: clock anchoring and DST-mismatch weeks as a construction standard (better placed in PARAMETERS.md) |
| L13 | MS C-10-04 | ML on the cost side: executability model timing entries of existing sleeves | 10 | 10 | yes | executability model timing entries (cost-side ML); value bounded by the sleeves it serves |
| L14 | MS C-5-12 | ES–SPY / NQ–QQQ 1-minute basis dislocation as a stress gate | 5 | 10 | yes | ES-SPY / NQ-QQQ 1-min basis dislocation as a stress gate |
| L15 | MS C-5-13 | Bar-derived depth proxy (minute Kyle lambda / realized Amihud) as a ... | 5 | 10 | yes | minute Kyle lambda / realized Amihud depth-regime conditioner; must beat a realized-vol tercile |
| L16 | MS C-9-05 | One-second tick rule calibration protocol (go/no-go at 75% agreement) | 9 | 10 | no | one-second tick-rule calibration protocol (go/no-go at 75% agreement); prerequisite measurement for every BVC row |
| L17 | PC C-10-01 | Meta-labelling a Gate-1 sleeve with purged, embargoed k-fold (JFDS code base) | 10 | 10 | no | meta-labelling a surviving sleeve with purged, embargoed k-fold; absorbs MS:C-10-01 (prereg_orb30 / overnight-drift primaries); public intraday ML IC ... |
| L18 | PC C-9-02 | Dollar-bar (volume-clock) decision cadence vs 30-min bars for a surviving sleeve | 9 | 10 | yes | volume-clock / dollar-bar cadence for a surviving sleeve; absorbs MS:C-9-03 and MS:C-9-04 |
| L19 | SC C-13-03 | FOMC statement cosine-similarity as a size/inactivity gate for ZN/UB event ... | 13 | 10 | yes | FOMC statement cosine-similarity as size/inactivity gate for ZN/UB event sleeves (C-2-11, C-2-10) |
| L20 | SC C-13-06 | GDELT conflict-event shocks as gate/tilt for gold and oil holds, with measured ... | 13 | 9 | yes | GDELT conflict-shock gate/tilt for gold and oil holds; measured 15-min feed lag; expect null |
| L21 | MS C-5-14 | Databento bbo-1m minute-sampled top-of-book imbalance as a passive-entry ... | 5 | 8 | yes | bbo-1m top-of-book imbalance as a passive-entry conditioner (0.1-0.3 tick fill improvement) |
| L22 | PC C-9-04 | ES book-skew / 10-level count-imbalance markout measurement before any ... | 9 | 5 | no | ES book-skew / 10-level imbalance markout measurement ($4-7); can close three lane-9 rows early; taker version fails the screen by construction |

## C. Compact briefs — top 40 mechanisms

### 1. AS C-4-01 — Cross-sectional overnight–intraday reversal among ES/NQ/YM/EMD/NKD, open → close
- score 16/21 — M2 E2 C2 F3 D3 X2 P2; plausibility medium; lane 4; original no
- mechanism: Hong–Wang (2000) periodic market closure: liquidity dries up over the close, overnight price moves overshoot, and the intraday session reverses the relative overnight winners and losers; Della Corte–Kosowski–Wang's "CO-OC" strategy (signal = close-to-open return, hold = open-to-close) earns roughly five times a conventional reversal in US stocks and is positive in every futures asset class; the reversal return is ...
- evidence: working paper, full text read (conference copy, "incomplete", Nov 2015): Della Corte, Kosowski, Wang, "Market Closure and Short-Term Reversal", https://www.mcgill.ca/desautels/files/desautels/dkw_2016.pdf (fetched 2026-11-03). Futures: 35 CME contracts, daily open/close from TickData, Jul 1982–Dec 2014; equity-index futures (DJIA, NASDAQ, NIKKEI 225, S&P400, S&P500) CO-OC: ...
- evidence window: 35 CME futures, daily open/close, Jul 1982 - Dec 2014 (DKW); 2015-2026 untouched by the evidence [window derived by the Prioritizer from the evidence field; the block predates the Day-0 field]
- instruments: ES/MES, NQ/MNQ, YM/MYM, EMD (S&P MidCap 400; thin, 0.10 pt tick), NKD/NIY; FTMO: US500, US100, US30, JP225 CFDs (US2000 as a sixth leg).
- holding / trades per year: 09:30 → 16:00 ET (flat before 16:10 ET / 15:10 CT); 1 long + 1 short leg per day ≈ 500 round trips/yr.
- data + cost: daily RTH open/close for the five roots 2010–2026 (Databento ohlcv-1d ≈ $0.05/root, or 1-h ≈ $1/root to define a 09:30–09:31 fill); SPX open/close 1990–2026 in hand; VIX daily free. Cheapest test in this file. [Databento]
- gross vs cost: published 25 bp/day for the long-short (12.5 bp per leg) 1982–2014 gross; leg round trips ES/NQ ≈ 1.3 bp, YM ≈ 1.5 bp, NKD ≈ 2.2 bp, EMD ≈ 3–5 bp → 2 × cost ≈ 3–9 bp per leg → PASS the economics screen on the published number even after a 0.5 haircut; the live question is whether a 09:31 fill reproduces a daily-data "open".
- firm fit: intraday futures (two opposite positions in different products is not hedging under the firm rules as inherited; verify "opposite exposure" wording at Tradeify §6.7 and Lucid); FTMO intraday CFD (no swap). News windows: 10:00 ET releases ...
- haircut: 0.5 (published). Split dates: 2014-12 (sample end), 2019 (equity-index futures 23-h sessions already in place; 2022-05 daily 0DTE), 2020-03.
- analyst line: closed: H0012/H0017 (time-series gap fade, failed) and E1-08..10 (stock-level tug of war) adjacent, this is relative across index futures; look-ahead: daily-data "open" must be re-measured as the 09:31 fill; econ: 25 bp/day L-S 1982-2014 -> 12.5 bp after haircut vs 2.6-10 bp two-leg RT -> >=3x for ES/NQ/YM legs, ~500 RT/yr; haircut 0.5, splits 2014-12, 2022-05; firm: IF 09:30->16:00 + FTMO intraday; evidence window ends 2014 so 2015-2026 is untouched OOS

### 2. AF C-1-01 — Month-end Treasury index-extension strike, firm-day capture
- score 16/21 — M3 E2 C1 F3 D2 X3 P2; plausibility low-medium; lane 1; original partial
- absorbs: pre-sweep A-C09
- mechanism: Bloomberg bond indices add the month's new issues and extend duration at the month-end strike (4pm ET since 2021-01-14, 3pm before); passive funds, insurers and index-benchmarked dealers buy into the strike. NY Fed interdealer cash data: the 10 minutes around 4pm carried 20.4% of last-trading-day volume in 2025 (11.6% in 2021; 2.5% → 3.5% on normal days 2021 → 2025); the 3:45–4:15pm half hour > 25% of month-end ...
- evidence: working paper (Hartley & Schwarz 2019, numbers per pre-sweep A-C09; still unpublished per search 2026-11-03, https://www.kristaschwarz.com/EOM.pdf not re-fetched) + central-bank blogs with data (Dyer, Fleming & Shachar, "Treasury Trading at the Close", NY Fed Liberty Street, Sept 2026, https://libertystreeteconomics.newyorkfed.org/2026/09/treasury-trading-at-the-close/, ...
- evidence window: cash Treasuries 1990–2018 (Hartley–Schwarz, per A-C09; 2015–2018 sub-period 'smaller but significant'); Treasury ETFs to 2019 (Allocate Smartly); cash-market volume facts 2015–2025 (NY Fed 2024/2026). ZN/ZB/UB futures returns at the strike never measured in ...
- instruments: ZN, ZB, UB (TN, ZF secondary). FTMO: no Treasury CFD found (verify symbol list).
- holding / trades per year: variant A (= A-C09): long 14:00 → 16:05 ET on the last trading day, 12/yr. Variant B (new): overnight-session holds entered 18:00 ET on T-3, T-2, T-1 evenings and exited at 16:05 ET the next day (re-entered each evening), so most ...
- data + cost: Databento GLBX.MDP3 ohlcv-1m ZN and UB full session 2010-06 → 2026 (≈ $20 per root, ≈ $40); 1h bars ($1/root) suffice for a first pass of variant B; SIFMA early-close calendar (free). Cost inside plan. [Databento]
- gross vs cost: cash evidence ≈ 5–10 bp per last-day session at 10y and 2–3x that in UB; ZN RT ≈ 3 bp, UB RT ≈ 5–6 bp → passes the screen in UB/ZB if ≥ 50% of the cash effect reaches futures (unmeasured); marginal in ZN; 2× costs still positive only for UB. 12–36 events/yr → a sleeve, never the account.
- firm fit: intraday futures (A) and overnight-session futures (B: 18:00 ET entry, flat 16:05 ET, inside Topstep's 16:08 ET auto-flatten, MFFU 16:10, Lucid/Tradeify 16:45); consistency rules touched (P&L concentrated in 12 days/yr); no news windows ...
- haircut: 0.5 (A, published cash result) / 0.7 (B); splits at 2015-01 (month-end volume regime), 2021-01-14 (3pm → 4pm strike), 2022-03 (hiking cycle).
- analyst line: closed: none (H0023 other asset); look-ahead: none (index-extension sizes published ahead); econ: UB 10-30 bp vs RT 5-6 bp, ZN marginal, 12-36 ev/yr, survives 2x only in UB and only if >=50% of the cash effect reaches futures; haircut 0.5 (A) / 0.7 (B), splits 2015-01, 2021-01-14 (strike 3pm->4pm), 2022-03; firm: IF to 16:05 ET (inside Topstep 16:10 ET) or ONF 18:00 holds

### 3. AF C-1-04 — WMR fix legs + month-end / MSCI-date intensity
- score 16/21 — M3 E2 C1 F3 D3 X2 P2; plausibility low-medium; lane 1; original partial
- absorbs: pre-sweep A-C06
- mechanism: Unconditional USD demand at benchmark fixes (passive funds, custodians, corporates) is pre-hedged by capital-constrained dealers. Krohn–Mueller–Whelan (G9, 1999–2019, 5-min spot): the equal-weight foreign-currency portfolio depreciates 4.2% p.a. from the European open to the ECB fix and appreciates ≈ 4.6% p.a. from the London fix to the New York close; post-London reversal ≈ 2.5 bp/day at median VIX; gross reversal ...
- evidence: peer-reviewed (Krohn, Mueller & Whelan, JF 79(1) 2024 541–578; staff WP version https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf, fetched 2026-11-03, pp. 1–3, Table II, Table VII, Table IX text pp. 34–35; Ito & Yamada, JIMF 80 (2018) 75–95, abstract via https://www.nber.org/papers/w23327, 2026-11-03; Melvin & Prins JFM 2015, workshop version ...
- evidence window: G9 spot vs USD, Jan 1999 → Dec 2019 (Refinitiv Tick History) and Jun 2006 → Dec 2019 (Refinitiv Matching), with CME FX futures series from 2004–06 (KMW SWP 2021-48 and BIS slides, snippet 2026-11-04); Ito–Yamada 2018 and Melvin–Prins 2015 end ≈ 2013; nothing ...
- instruments: 6E, 6B, 6A, 6J, 6C (CME); FTMO EURUSD/GBPUSD/AUDUSD.
- holding / trades per year: leg A long USD 02:00 → 08:15 ET (pre-ECB fix; KMW's most robust leg); leg B short USD 11:00 → 16:05 ET; daily (≈ 250/yr per pair) or intensity-only (≈ 16 days/yr: month-ends incl. the 4 MSCI dates and quarter-ends) with direction ...
- data + cost: Databento 1m full session for two roots (6E, 6A; ≈ $40) or HistData 1m spot (free) for the first pass; DST-correct London/Frankfurt clocks; MSCI review calendar (free); country-index MTD returns via ETF prices (free). [free first pass]
- gross vs cost: ≈ 1.5–2 bp/day per leg (4–5% p.a. / 250) vs 6E RT ≈ 1.2 bp → FAILS the screen for daily legs (edge < 2 × RT); intensity days 10–25 bp (ITG/FCA figures in A-C06) vs 1.2 bp → passes, n ≈ 16/yr.
- firm fit: intraday futures (leg A fully inside; leg B exits 16:05 ET for Topstep); FTMO intraday CFD (no swap) or Swing; news windows: leg A crosses 08:30 ET releases only if extended, keep the 08:15 exit.
- haircut: 0.5; splits at 2015-02-15 (5-minute window), 2018-01 (MiFID II), 2020-03.
- analyst line: closed: D2/D4 adjacent but not fix-anchored; look-ahead: MSCI/month-end dates known ex ante, equity MTD sign at T-1; econ: daily legs 1.5-2 bp vs RT 1.2 FAIL, intensity days 10-25 bp PASS but ~16/yr; haircut 0.5, splits 2015-02-15 (5-min window), 2018-01 MiFID II, 2020-03; firm: IF 6E/6B/6A + FTMO FX intraday/swing; London 16:00 fix = 11:00 ET, inside every deadline

### 4. AF C-1-09 — Index-rebalance days ES/NQ/RTY and CFDs
- score 16/21 — M3 E2 C2 F2 D3 X3 P1; plausibility low; lane 1; original no
- absorbs: pre-sweep P-C09
- mechanism: On S&P quarterly rebalance days (third Friday of Mar/Jun/Sep/Dec, = quad witching), Russell reconstitution (late-June Friday) and MSCI SAIR dates, passive funds trade the closing auction; Krueger (P-C09): FTSE 100 CFD falls into the auction print on eve days, holdout +11.5 bp/event (t 3.9, n 27). But index-level net demand is small because adds and deletes net out, and even the single-stock effect has vanished: ...
- evidence: peer-reviewed (Greenwood & Sammon, "The Disappearing Index Effect", JF 80(2) 2025 657–698, NBER WP 30748 https://www.nber.org/system/files/working_papers/w30748/w30748.pdf, search snippet 2026-11-03) + blog with pre-registered holdout (Krueger Algorithms 2026, P-C09). Post-2015 OOS: Krueger 2023–2026 for UK100 only; US futures none.
- evidence window: S&P 500 additions/deletions ≈ 1980–2020 (Greenwood–Sammon, effect disappearing after ≈ 2010); UK100 CFD rebalance days 2023–2026 (Krueger, P-C09). ES/NQ/RTY futures on effective days not measured.
- instruments: ES/MES, NQ/MNQ, RTY/M2K; FTMO UK100, GER40, JP225 (P-C09).
- holding / trades per year: 15:30 → 16:00 and 16:00 → 16:07 ET on ≈ 10–12 US event days/yr (+ ≈ 12 European/MSCI dates via CFD).
- data + cost: ES 1m (in hand), RTY 1m RTH (≈ $7); index review calendars (free); UK100 CFD ticks (Dukascopy datafeed blocked; FTMO MT5 history only once an account exists). [Databento]
- gross vs cost: UK100 +8–12 bp/event vs ≈ 1.7 bp RT → passes there (n ≈ 12/yr); US futures unknown and expected smaller (Greenwood–Sammon) → fail until measured.
- firm fit: intraday futures; FTMO intraday CFD (post-close pricing to verify); no news windows.
- haircut: 0.5; splits at 2018, 2023.
- analyst line: closed: none (H0006 is momentum, H0023 other calendar); look-ahead: rebalance dates announced weeks ahead; econ: UK100 +8-12 bp/event vs RT 1.7 bp -> 2.4-3.5x after 0.5 haircut, US legs unmeasured, ~12-24/yr; haircut 0.5, splits 2018, 2023; firm: FTMO intraday CFD (verify post-close pricing on UK100), IF for ES/NQ/RTY legs

### 5. AF C-2-01 — NG storage announcement-day premium
- score 15/21 — M2 E1 C2 F3 D2 X3 P2; plausibility low-medium; lane 2; original no
- absorbs: pre-sweep A-C15
- mechanism: An announcement-day risk premium in NG futures: "more than 50% of the annual return is earned" on EIA storage report days (Thursdays 10:30 ET); the gap versus non-announcement days is not explained by the storage surprise or other controls; intraday the return splits about half before and half after the release; the pre-announcement part occurs only when storage exceeds expectations (the authors read this against ...
- evidence: peer-reviewed, abstract only (Prokopczuk, Wese Simen & Wichmann, "The Natural Gas Announcement Day Puzzle", The Energy Journal 42(2) 2021 91–111, DOI 10.5547/01956574.42.2.mpro; abstract via https://ideas.repec.org/a/aen/journl/ej42-2-wichmann.html and https://livrepository.liverpool.ac.uk/3083246/, fetched 2026-11-03; accepted manuscript ...
- evidence window: NG front-month futures on EIA storage days, sample period not shown on the pages seen (Energy Journal 2021; manuscript dated Nov 2019, so ≤ 2018; verify when the accepted manuscript becomes readable).
- instruments: NG, MNG; FTMO NATGAS (intraday or Swing).
- holding / trades per year: long NG from 18:00 ET Wednesday (or 09:00 ET Thursday) to the 14:30 ET Thursday settlement; variants pre-release only (09:00 → 10:29) and post-release only (10:32 → 14:30); ≈ 52 trades/yr (holiday weeks shift to Wednesday/Friday).
- data + cost: Databento 1m NG RTH 2010–2026 (≈ $7; both legs sit in RTH); EIA storage actuals (free); consensus survey not free (EIA 5-year average or scraped forecasts as a proxy). [Databento]
- gross vs cost: NG daily sd ≈ 3–4%; for "> 50% of annual return" to be meaningful the announcement-day mean must be of order +30–80 bp ≫ NG RT ≈ 7 bp → passes the economics screen on paper; a 50 bp mean over 500 events would be t ≈ 3 — sign and size must be confirmed from the paper before any row.
- firm fit: overnight-session or intraday futures (flat by 14:30 ET); FTMO intraday CFD (≈ 8 bp RT) or Swing (one swap night); news windows: MFFU Rapid/Pro ±2 min incl. resting orders if EIA NG is on its Tier-1 list (verify; if yes exit 10:27, ...
- haircut: 0.5; splits at 2012 (shale regime), 2020-03, 2022-02 (LNG/Europe shock).
- analyst line: closed: E2 (ES/NQ) different asset/mechanism; look-ahead: none (fixed weekday); econ: implied 30-80 bp/event vs NG RT 7 bp -> 2-5x after 0.5 haircut if sign confirmed; ~50/yr; haircut 0.5, splits 2012, 2020-03, 2022-02; firm: ONF Wed 18:00 -> Thu 14:30 ET or IF; MFFU/Lucid news window at 10:30 Thu (hold through release banned there; Topstep/Bulenox/FTMO only)

### 6. SC C-13-01 — ECB press-conference tone change → EU50/GER40 continuation
- score 15/21 — M2 E2 C3 F2 D3 X2 P1; plausibility low; lane 13; original no
- mechanism: Schmeling–Wagner measure the tone of the ECB president's press-conference language; a more positive tone raises Euro-area equity prices on the day and the effect grows until the next press conference. They attribute it to a risk-premium channel (tone is unrelated to current or future fundamentals), i.e. the central bank moves the price of risk and slow-moving investors re-price over weeks. The ECB publishes the ...
- evidence: peer-reviewed — Schmeling & Wagner (2025) "Does Central Bank Tone Move Asset Prices?", JFQA 60(1) 36–67, https://econpapers.repec.org/RePEc:cup:jfinqa:v:60:y:2025:i:1:p:36-67_2; open-access PDF https://openaccess.city.ac.uk/id/eprint/32436/10/does-central-bank-tone-move-asset-prices.pdf (not opened; abstract and VoxEU column via search, fetched 2026-11-03): return differential ...
- evidence window: Euro Stoxx 50 / European equities 1999–2017.
- instruments: EU50, GER40 (FTMO); FRA40 as a second check
- holding / trades per year: leg A 15:30 CET (presser end) → 17:30 CET cash close (intraday CFD, no swap); leg B hold to the next meeting (~6 weeks, Swing). 8 scheduled meetings/yr → 8 trades/yr per leg; a decade gives ~80 events.
- data + cost: ECB transcripts 1999–2026 (ecb.europa.eu, free); 1-minute EU50/GER40 from HistData (ETXEUR, GRXEUR; free, 2010–2026); daily closes from Stooq; $0. [free first pass]
- gross vs cost: leg A ≈ 30 bp per event if half the 60 bp day effect is realized after the tone is scorable (scoring needs the full transcript, i.e. the last 30–45 minutes of the presser), vs 1.5–3 bp round trip → passes the economics screen. Leg B ≈ +40 bp incremental over 6 weeks vs swap ≈ −75 bp (GER40 at −6.5 %/yr) → fails; leg B only as a short-tone leg (short pays ...
- firm fit: FTMO intraday CFD (leg A, no news restriction needed on Swing; on Standard the ±2-minute window around the 13:45 decision is avoided by construction since entry is 15:30). Futures firms: no (non-CME).
- haircut: 0.5 (published 2015 working paper, 2025 journal). Splits: 2015 (working paper), 2022 (ECB hiking cycle, presser format changes).
- analyst line: closed: E2 (FOMC/CPI ES/NQ) different bank and market; look-ahead: tone score only from the transcript available at entry (15:30 CET), lexicon frozen before 2015; econ: ~30 bp/event vs 1.5-3 bp RT -> ~5x after haircut; 8/yr; haircut 0.5, splits 2015, 2022; firm: FTMO intraday leg A (check FTMO funded news restriction +-2 min - Swing exempt), Swing leg B

### 7. AF C-2-13 — FOMC/BoJ-day FX premium 6A/6B/6E/6J
- score 15/21 — M2 E2 C2 F3 D3 X2 P1; plausibility low; lane 2; original partial
- mechanism: Constrained financiers demand compensation for monetary-policy uncertainty, so short-USD/long-foreign strategies earn more on scheduled FOMC days (1994–2013, 160 announcement days, 4pm-to-4pm ET returns): low-rate portfolio +5.19 bp versus −0.51 bp on other days; high-rate portfolio +14.47 versus +1.73 bp; AUD +17.28 versus +1.16 bp (difference t 2.51); simple strategy 10.77 bp per announcement day, improved version ...
- evidence: peer-reviewed (Mueller, Tahbaz-Salehi & Vedolin, "Exchange Rates and Monetary Policy Uncertainty", JF 72(3) 2017 1213–1252, https://www.kellogg.northwestern.edu/faculty/alirezat/FXAnnouncements.pdf, fetched 2026-11-03, pp. 1215–1217 and Table I). Post-2015 OOS: none (sample ends 2013); A-C40's "expect null" for 6E pre-FOMC is itself untested.
- evidence window: G10 spot vs USD on FOMC (and BoJ) days, sample ending 2013 (Mueller–Tahbaz-Salehi–Vedolin JF 2017; start year not extracted). 6A/6B/6E/6J futures and 2014–2026 untested.
- instruments: 6A, 6B, 6E, 6C (FOMC days), 6J (BoJ days), M6E; FTMO AUDUSD/EURUSD/USDJPY (Swing for the 22h version).
- holding / trades per year: long foreign currency 18:00 ET day −1 → 16:00 ET day 0 (overnight-session hold ≈ 22 h) on FOMC days (8/yr) and BoJ days (8/yr), pooled over four pairs ≈ 64 position-days/yr; variant: positive-differential currencies only, flip ...
- data + cost: HistData 1m spot (free) for 2010–2026; Databento 6A/6E 1h (≈ $1/root); FOMC/BoJ calendars (free); ZQ 1m at 14:00 ET for the surprise sign (≈ $7 RTH) or FedWatch snapshots. [free first pass]
- gross vs cost: 5–20 bp per announcement day vs 6A RT ≈ 1.8 bp / 6E RT ≈ 1.2 bp → passes the economics screen; n ≈ 64/yr pooled is thin; post-2013 decay unknown.
- firm fit: overnight-session futures (18:00 → 16:00 ET, flat before deadlines); FTMO Swing (one swap night) or intraday CFD (09:00 → 16:00 only); news windows: the 14:00 ET statement is inside the hold → banned at MFFU Rapid/Pro (±2 min incl. resting ...
- haircut: 0.5; splits at 2008-12 (ZLB), 2015, 2022.
- analyst line: closed: E2-05 / A-C40 adjacent; look-ahead: calendars public; econ: 5-20 bp/day vs 6E/6A RT 1.2-1.8 -> 1.7-6x after haircut, ~64 position-days/yr pooled, no post-2013 evidence; haircut 0.5, splits 2008-12, 2015, 2022; firm: ONF 6A/6B/6E/6J (news ban at MFFU/Lucid for FOMC) / FTMO Swing (one swap)

### 8. IG C-12-15 — Month-end multi-asset rebalancing, equity leg into the last day's close
- score 15/21 — M3 E2 C2 F3 D2 X2 P1; plausibility low; lane 12; original no
- mechanism: balanced mandates (60/40, target-date, pensions) rebalance to fixed weights at month- and quarter-ends; Harvey, Mazzoleni & Melone (NBER w33554, 2025, https://www.nber.org/papers/w33554; cited by the sibling block C-1-02 which registers the bond leg) show the rebalancing demand, predictable from the month's equity-vs-bond performance gap, moves prices over the last days of the month and reverts afterwards. The ...
- evidence: working paper (NBER 2025; daily data); own twist for the 30-minute close window and the signed trigger.
- evidence window: US and global 60/40 proxies ≈ 1997–2023 (HMM; window per sibling file, verify); ES last-day 15:30–16:00 untested.
- instruments: ES/MES; NQ secondary; FTMO US500 intraday or Swing (the HMM daily version holds 1–3 days around the turn).
- holding / trades per year: 15:30 → 15:59 ET on the last trading day (12/yr, plus quarter-ends weighted 2×) when |equity − bond MTD return| > 2%; ≈ 8–12 trades/yr — a sleeve only; annual contribution at 1 MES per $5k of drawdown ≈ 10 × 10 bp × $25k notional ...
- data + cost: ES 1m RTH (in hand, licence-held copy cross-check only; Databento ≈ $7); S&P and Treasury daily (free). $0–7. [free first pass]
- gross vs cost: HMM's daily effect is tens of bp per event; a third landing in the final half hour = 5–15 bp vs 1.2 bp RT → passes on paper.
- firm fit: intraday futures (15:30–15:59); FTMO Swing for the multi-day version (swap per night).
- haircut: 0.5 (published); splits at 2008, 2020-03, 2022 (bond bear market changed the rebalancing sign distribution).
- analyst line: closed: H0023 (unconditional TOM long) and H0006 (momentum) adjacent - this is a signed calendar flow; look-ahead: MTD equity-bond gap at 15:30 of the last day (or T-1); econ: 5-15 bp vs 1.2 bp RT -> 1-3x after haircut; 12/yr (quarter-ends 2x) - a sleeve; haircut 0.5, splits 2008, 2020-03, 2022; firm: IF 15:30-15:59 / FTMO Swing; pairs with the bond leg C-1-02

### 9. AF C-1-05 — Tokyo 9:55 fix in 6J
- score 15/21 — M3 E2 C1 F3 D3 X2 P1; plausibility low; lane 1; original no
- absorbs: pre-sweep A-C07, pre-sweep P-C12
- mechanism: Japanese importers' USD purchases are filled at the 9:55 JST fix; banks pre-hedge from the New York close. KMW: the foreign-currency portfolio depreciates 5.0% p.a. from 17:00 ET to the fix (USD up → short 6J) and appreciates 5.3% p.a. afterwards (long 6J); Tokyo-reversal returns positive in 70–83% of months; gross annualized reversal 6.2% (CHF) to 14.2% (NZD), JPY 12.0% gross, ≈ 2.7% at half spreads; "returns ...
- evidence: peer-reviewed (KMW JF 2024, SWP pp. 1–3, 33–35, https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf, fetched 2026-11-03; Ito & Yamada JIE 2017 per A-C07) + blog with pre-registered forward test (Krueger, P-C12). Post-2015 OOS: KMW sub-period 2014–2019 smaller/significant; Krueger 2023–26 +4.5–5.6 bp/trade before global correction.
- evidence window: USD/JPY spot 1999–2019 (KMW; 2014–2019 sub-period smaller but significant); Tokyo fixing order-flow sample ≈ 2008–2015 (Ito–Yamada, per A-C07, verify); Krueger forward test 6J/USDJPY 2023–2026 (P-C12).
- instruments: 6J, M6J (window 17:00–02:00 ET sits in the overnight session); FTMO USDJPY.
- holding / trades per year: short 6J 18:00 → 20:55 ET (19:55 ET in US summer), flip long 20:55 → 02:00 ET; daily (≈ 245/yr) or gotobi/month-end only (≈ 60/yr).
- data + cost: HistData USDJPY 1m (free) or Databento 6J full session (≈ $20); JST/DST alignment; Japanese holiday calendar (free). [free first pass]
- gross vs cost: ≈ 2 bp per leg on average days vs 6J RT ≈ 1.5–2 bp → FAILS the screen unconditionally; gotobi/month-end days plausibly 5–10 bp → marginal pass with ≈ 60 trades/yr; overnight-session spreads 1–2 ticks.
- firm fit: overnight-session futures (entry after 18:00 ET, flat by 02:00 ET); FTMO intraday CFD (enter after 00:00 CET to avoid the swap); Japanese data releases 19:30/19:50 ET fall inside the first leg (no firm clause, but FTMO Standard-style ±2 ...
- haircut: 0.5; splits at 2013 (Abenomics), 2015-02, 2022-09 (MoF interventions).
- analyst line: closed: D4 (check whether USDJPY hour windows were in it); look-ahead: gotobi calendar known; econ: ~2 bp vs RT 1.5-2 FAILS unconditionally, gotobi/month-end 5-10 bp marginal, ~60/yr; haircut 0.5, splits 2013, 2015-02, 2022-09; firm: ONF 6J (19:55-20:55 ET) / FTMO USDJPY intraday; retail-crowded

### 10. AS C-4-07 — Hedging-overshoot reversal after a large last half hour, 18:00 ET → next close, ES/NQ/ZN/GC/SI/NG
- score 14/21 — M2 E2 C3 F3 D1 X2 P1; plausibility low; lane 4; original yes
- mechanism: BDLM attribute market intraday momentum (the rest-of-day return predicting the last half hour) to option market makers and leveraged-ETF providers hedging short-gamma exposure in the direction of the day's move near the close; price pressure, unlike information, must revert, and they show it does: the last-half-hour return negatively predicts the next one to three days in equity-index, bond and commodity futures ...
- evidence: peer-reviewed, full text read (Baltussen, Da, Lammers, Martens, "Hedging demand and market intraday momentum", JFE 142(1):377–403, 2021, DOI 10.1016/j.jfineco.2021.04.029; author PDF https://academicweb.nd.edu/~zda/intramom.pdf, fetched 2026-11-04; the pre-sweep read the same paper for A-C01..C03 but did not use its reversal table). Table 11, pooled regressions of the next 1-, ...
- evidence window: ≈ 60 futures (equity, bond, commodity, currency) 1974–2020, pooled.
- instruments: ES/MES, NQ/MNQ (equity leg); ZN, ZB (bond leg); GC/MGC, SI, NG (commodity leg); FTMO US500/US100/XAUUSD CFDs for the Swing variant.
- holding / trades per year: enter 18:00 ET (Globex reopen) on days where |rLH| exceeds a threshold fixed in advance (1.5 × trailing 60-day σ of rLH) and sign(rLH) = sign(rROD); exit at the next day's cash close (equities 16:00 ET), 15:00 ET (bonds) or ...
- data + cost: ES 1-min RTH (in hand, LICENCE HOLD: cross-check only) and Databento ES/NQ/ZN/GC/SI/NG 1-min RTH for the rLH/rROD signal (≈ $6–7 per root, ≈ $40 for six roots; ES, GC and ZN RTH are already in the plan via ... [Databento]
- gross vs cost: ES last-half-hour σ ≈ 0.35 %; on a day with rLH = 0.6 % the 2-day coefficient implies ≈ 17 bp of reversal and the 1-day coefficient ≈ 9 bp; MES round trip ≈ 1.3 bp, threshold 2.6 bp → PASSES the screen on the published pooled coefficient with room for 2× costs; bonds: 3-day −19.6 bp per 1 % of rLH, but ZN rLH is ≈ 0.1 %, so ≈ 2 bp expected against a 4 bp ...
- firm fit: overnight-session futures (position opened after 18:00 ET and closed before the next afternoon deadline: Topstep 15:10 CT is before the 16:00 ET equity close, so the equity leg exits at 15:00 ET at Topstep and at the close at ...
- haircut: 0.5 (published). Split dates: 2021-01 (closing-imbalance dispersion collapse per BLW 2026), 2020-05 (sample end), 2016-05 (SPX Wednesday weeklies; 0DTE growth 2022-05), 2010-06 (Databento start).
- analyst line: closed: H0006/H0019 (uses the same last half hour but trades the next-day reversal) and H0012/H0017 (different trigger); look-ahead: rLH known at 16:00, entry 18:00; econ: 9-17 bp predicted reversal on trigger days vs MES RT 1.3 -> >=3x after haircut, but R2 <0.3%; ~40-60/yr; haircut 0.5, splits 2016-05, 2020-05, 2021-01; firm: ONF 18:00 -> next-day close before deadline / FTMO Swing

### 11. IG C-11-01 — prereg_orb30 as written (A/B/C; OOS row only if A's D1 p5 > 0)
- score 14/21 — M1 E2 C3 F3 D3 X1 P1; plausibility low; lane 11; original no
- mechanism: the opening-range breakout family (Crabel 1990; Holmberg, Lonnbark & Lundstrom, Finance Research Letters 10(1) 2013, 27–33, crude oil; Zarattini & Aziz 2023, SSRN 4416622 — SSRN blocked, 403, per D-007) assumes early-session order flow from overnight information continues after the first 30 minutes. The org's own pre-registration (file: ...
- evidence: peer-reviewed (Holmberg et al. 2013, crude, ≈ 1983–2011), working paper (Zarattini–Aziz 2023, QQQ 2016–2023, +0.13R gross, no OOS), negative public replication (mql5 blog, snippet only, gross reproduced / net zero); the inherited 5-minute version failed (H0020: gross t 1.63, net −0.005R).
- evidence window: crude oil ≈ 1983–2011; QQQ 2016–2023 (5-minute); the 30-minute S&P version is untested; D1 2010–2018 is declared in-sample.
- instruments: SPXUSD 1m (D1, in hand, free) then ES/MES 1m RTH 2019–2026 (in-hand copies are LICENCE HOLD → Databento ES RTH ≈ $7 for the OOS row).
- holding / trades per year: minutes to 6 hours; ≈ 150–200 trades/yr (one per eligible day with a trigger).
- data + cost: $0 for D1; ≈ $7 for the OOS row if earned. [free first pass]
- gross vs cost: Zarattini–Aziz's +0.13R gross on a 5-minute range; with a 30-minute range the median risk is ≈ 10–20 ES pt so 0.6 pt RT is 3–6% of 1R → passes the economics screen on structure; the family's record says the gross edge is the problem, not the cost.
- firm fit: intraday futures (entries by 12:00, exit 15:59 — inside every deadline; MFFU 10:00 ET news windows touch the trigger window: skip ±2 minutes); FTMO intraday CFD.
- haircut: 0.5 (published family); splits at 2016 (Zarattini sample start), 2022-05 (0DTE).
- analyst line: closed: H0020 (5-min ORB) and H0005/H0011 - prereg_orb30 states its differences (30-min range, one entry) and was registered before any run; look-ahead: D1 2010-2018 declared in-sample, OOS row only if A's D1 p5 > 0; econ: RT 3-6% of 1R passes on structure, gross edge is the risk; 150-200/yr; haircut 0.5, splits 2016, 2022-05; firm: IF/FTMO intraday

### 12. SC C-8-05 — Energy term-structure carry on FTMO's own swap sign (USOIL/UKOIL/NATGAS/HEATOIL)
- score 14/21 — M2 E2 C3 F2 D2 X2 P1; plausibility low; lane 8; original partial
- absorbs: IG C-11-02
- mechanism: the FTMO rolling contracts pass the futures roll yield through the nightly swap (USOIL long +5 %/yr and short −32 %/yr in backwardation; NATGAS short +40 %/yr and long −176 %/yr in contango, table above). Term-structure (carry) strategies — long backwardated, short contango commodities — are among the oldest documented commodity premia; the counterparties are hedgers and index rollers who hold the wrong side of the ...
- evidence: peer-reviewed — Koijen, Moskowitz, Pedersen, Vrugt (2018) "Carry", JFE 127(2) 197–225, https://econpapers.repec.org/RePEc:eee:jfinec:v:127:y:2018:i:2:p:197-225 (abstract only, fetched 2026-11-03): carry predicts returns in the time series and cross-section across asset classes incl. commodities; working-paper Sharpe figures not seen. Peer-reviewed — Fuertes, Miffre, Rallis ...
- evidence window: 20–40 commodity futures 1970s/1980s–2012 (KMPV, FMR); nothing after 2015 seen; nothing on CFD financing terms.
- instruments: USOIL.cash, UKOIL.cash, NATGAS.cash, HEATOIL.c (FTMO); XAU/XAG excluded (always contango, both swaps negative).
- holding / trades per year: position held while the swap sign and a slow trend filter agree; re-evaluated nightly, turnover ≈ 6–15 round trips/yr per instrument; 25–60 trades/yr for the sleeve.
- data + cost: daily front/second futures settlements for CL, BZ, NG, HO 2000–2026 (free: EIA daily spot/futures tables, Stooq/Yahoo continuous — both blocked today, Databento 1d ≈ $0.05/root as the clean source); the FTMO swap JSON ... [Databento]
- gross vs cost: carry collected ≈ 5–40 %/yr while on; price drift against carry historically takes back roughly half (the literature's net TS carry Sharpe ≈ 0.3–0.6 per commodity). Spread 2.5 bp WTI / 8 bp natgas per side on monthly turnover is negligible → passes the economics screen; the risk is the single-market vol (NG 60–80 %/yr) against FTMO's 5 % daily loss, which ...
- firm fit: FTMO Swing only (multi-week holds, weekends). Futures firms: no (overnight holds). Clauses: 5 % daily loss from the 00:00 CE(S)T balance incl. floating P&L — NG gap risk is the binding constraint.
- haircut: 0.5 (published family); 0.7 is NOT claimed for the swap-as-signal twist. Splits: 2004–2008 (financialization), 2020-04 (negative WTI, roll-rule changes), 2026-01-30 (FTMO/OANDA rolling contracts).
- analyst line: closed: D2-04/05 (FX carry only), H0007; commodity curve carry untested; look-ahead: swap sign published per night - use the prior night's sign; econ: carry 5-40%/yr, monthly turnover, spread negligible; 25-60 trades/yr; haircut 0.5, splits 2004-08, 2020-04, 2026-01-30 (FTMO rolling contracts); firm: FTMO Swing

### 13. AS C-3-06 — Treasury-futures day/night sign asymmetry (long day leg, short overnight-session leg; UB row only clears the ...
- score 14/21 — M2 E2 C1 F3 D2 X3 P1; plausibility low; lane 3; original yes
- mechanism: Hendershott, Livdan and Rösch show that the market risk premium is earned overnight in equities but that US Treasury futures do the opposite: day (08:20–15:00 ET) returns are positive and significant, night returns are negative or zero, which they read as the implied risk-free rate switching between a high day level and a low night level (the marginal investor switches between day and night clienteles). For a ...
- evidence: peer-reviewed, full text read (Hendershott, Livdan, Rösch, "Asset pricing: A tale of night and day", JFE 138(3):635–662, 2020, DOI 10.1016/j.jfineco.2020.06.006; author PDF http://faculty.haas.berkeley.edu/hender/CAPMday-night.pdf, fetched 2026-11-04). Table 12, TRTH 5-minute midquotes 1996–2013, winsorised 1/99 %: 5-year front month day +0.010 %/day (t 3.59), night −0.006 % ...
- evidence window: ZF/ZN/ZB/UB, gilt, Bund, JGB 1996–2013 (TRTH midquotes); US equity portfolios 1992–2016.
- instruments: ZN (10-year), ZF (5-year), UB (Ultra); ZB and gilt/Bund only as cross-checks (Bund/gilt are not CME; FTMO bond-CFD availability not verified).
- holding / trades per year: day leg 08:20 → 15:00 ET (≈ 250/yr); night leg 18:00 → 08:20 ET (≈ 250/yr); each leg is one trade a day; combined ≈ 500/yr; a regime-gated version (only when the 60-day rolling day-minus-night spread is positive) trades ...
- data + cost: Databento GLBX.MDP3 ZN, ZF, UB 1-hour bars 2010-06 → 2026 (≈ $1 per root, ≈ $3; 1-day bars $0.15 are not enough because the 18:00 and 08:20 marks are needed); free CFTC/FRED daily for controls. [Databento]
- gross vs cost: ZF/ZN ≈ +1.0 bp per day leg and ≈ −0.1 to −0.6 bp per night leg (published). ZN round trip ≈ 1/64 tick ≈ 1.4 bp + ≈ $5 ≈ 2 bp; ZF tick 1/128 ≈ 0.7 bp, RT ≈ 2 bp; screen threshold max(2 ticks, 2 × RT) = 4 bp per leg → FAILS by 4× for ZF/ZN on the published means. UB: tick 1/32 ≈ 2.6 bp at ≈ 120, RT ≈ 5.7 bp, threshold ≈ 11.4 bp; the Ultra second-front day ...
- firm fit: day leg = intraday futures (enter 08:20 ET, flat 15:00 ET, before every deadline); night leg = overnight-session futures (short after the 18:00 ET reopen, flat 08:20 ET); FTMO: no swap on either intraday leg if the night leg is opened ...
- haircut: 0.5 (published 2020; sample ends 2013). Split dates: 2013-12 (sample end), 2010-01 (Ultra listing), 2015-12 (first hike), 2020-03, 2022-03 (hiking cycle; day/night rate-level switch mechanism should strengthen when ...
- analyst line: closed: none; look-ahead: none; econ: ZF/ZN +1 bp/leg vs threshold 4 bp FAILS 4x, UB clears only on a 4-year midquote sample; 250-500/yr; haircut 0.5, splits 2010-01, 2013-12, 2015-12, 2020-03; firm: IF day leg + ONF night leg

### 14. IG C-12-10 — Platts Dated Brent MOC window 11:00–11:30 ET in CL / Brent CFD
- score 14/21 — M2 E2 C1 F3 D2 X3 P1; plausibility low; lane 12; original partial
- mechanism: physical players with positions priced off Dated Brent trade the Platts market-on-close window to influence the assessment; Frino, Ibikunle, Mollica & Steffen (J. Banking & Finance 2018) show ICE Brent futures trading intensifies in the window and moves in the direction of the published benchmark (snippet 2026-11-04; original not fetched; see also Swinand & O'Mahoney MPRA 56252 ...
- evidence: peer-reviewed (JBF 2018; window ≈ 2010–2014, verify) for the flow; own idea for the two-leg rule; the reversal leg is untested anywhere seen.
- evidence window: ICE Brent ≈ 2010–2014 (Frino et al., verify); CL window untested.
- instruments: CL/MCL (CME; Brent BZ is CME-listed too, low volume); FTMO UKOIL/USOIL intraday CFDs (the Brent CFD is the direct expression).
- holding / trades per year: two legs of ≈ 30 minutes; every trading day → ≈ 250 days × 2 legs (only days whose 11:00–11:10 move exceeds 0.2% for the momentum leg: ≈ 120/yr).
- data + cost: CL 1m RTH (Databento ≈ $7; shared with lanes 1–2); Brent 1m: HistData has BCO/USD 1m free (https://www.histdata.com/download-free-forex-data/?/ascii/1-minute-bar-quotes, fetched 2026-11-04) → $0 for the CFD leg. [free first pass]
- gross vs cost: Brent moves ≈ 20–40 bp in the window on active days; capturing a third = 7–13 bp vs 2.5 bp/side CFD (5 bp RT) → marginal pass; CL 4 bp RT similar.
- firm fit: intraday futures; FTMO intraday CFD; no news windows (EIA is 10:30 ET Wednesday — the window starts 30 minutes later; MFFU ±2 min irrelevant).
- haircut: 0.5 (published) for the momentum leg, 0.7 for the reversal leg; splits at 2015 (Platts Brent basket changes), 2023 (WTI Midland added to Dated Brent).
- analyst line: closed: none; look-ahead: window fixed (11:00-11:30 ET); econ: 7-13 bp vs 4-5 bp RT marginal at 2x; ~120-250/yr; haircut 0.5 (momentum) / 0.7 (fade), splits 2015, 2023; firm: IF CL / FTMO UKOIL intraday

### 15. IG C-12-04 — CME margin-hike next-open liquidation in GC/SI/CL/NG — TOP10 (7)
- score 14/21 — M3 E1 C2 F3 D1 X3 P1; plausibility low; lane 12; original yes
- mechanism: CME Clearing raises performance bonds by advisory, typically after a large move, "effective after the close of business" on the stated date (e.g. https://www.cmegroup.com/notices/clearing/2022/11/Chadv22-433.html, https://www.cmegroup.com/notices/clearing/2024/06/Chadv24-166.html, fetched as snippets 2026-11-04; archive back to 2008). FCMs pass the increase to retail with intraday margin multiples, and ...
- evidence: peer-reviewed (daily-level, direction neutral) + own idea for the intraday rule; CME advisory archive is free text (lane 13 adjacent).
- evidence window: 20 commodity markets to ≈ 2013 (D&S); CME 2000–2011 (AQR); first-hour window untested.
- instruments: GC/MGC, SI/SIL, CL/MCL, NG/MNG, ZC, ZS; ES/NQ hikes are rarer.
- holding / trades per year: 09:30 → 10:30 ET with the prior move, then fade to 12:00; CME issues ≈ 100–300 margin advisories a year across all products, ≈ 30–60 touching these roots → ≈ 30–60 event days/yr (a sleeve, under 40 per root: annual contribution ...
- data + cost: Databento 1m RTH GC, SI, CL, NG (≈ $28; shared with C-1-06); advisory dates parsed from cmegroup.com (free, labour; the 2008–2026 archive exists). [Databento]
- gross vs cost: unknown; a 0.3–0.5% first-hour extension on a hike day in GC is 15–25 bp vs ≈ 1 bp RT → passes the screen if it exists; CL 4 bp RT, NG 7 bp RT need 10–15 bp.
- firm fit: intraday futures (all firms; 09:30–12:00); the 18:00 ET reopen variant is an overnight-session hold (inside one day); MFFU news windows irrelevant except 08:30 releases; FTMO intraday CFD on XAU/XAG/WTI/NATGAS.
- haircut: 0.7; splits at 2011-05 (SI margin cascade), 2020-04, 2022-03 (NI/energy hikes).
- analyst line: closed: none (H0012/H0017 share the open window without a trigger); look-ahead: CME advisories dated the evening before effect - use publication time; econ: 15-25 bp first-hour extension in GC vs ~1 bp RT if it exists, CL/NG need 10-15 bp; 30-60 events/yr; haircut 0.7, splits 2011-05, 2020-04, 2022-03; firm: IF/ONF/FTMO intraday

### 16. IG C-12-06 — Vol-control / risk-parity deleveraging into the close, 1–3 days after a vol jump — TOP10 (3)
- score 14/21 — M3 E1 C2 F3 D2 X2 P1; plausibility low; lane 12; original yes
- mechanism: volatility-targeting funds (Nomura's model: ≈ $28.8bn of forced selling for a week of 1% daily S&P moves, versus ≈ $2.3bn of buying from a sideways week; a two-week run of 1% days ≈ $15bn more; https://www.advisorperspectives.com/articles/2023/08/11/week-of-moves-on-sandp-500-could-trigger-forced-selling, snippet 2026-11-04; "around $17 billion would have to be sold into the close" on one November-2025 day, snippet, ...
- evidence: practitioner (bank model via press); academic background: Moreira & Muir (JF 2017) on the returns of vol-managed portfolios, not on their price impact; no minute-level test found.
- evidence window: none at minute level; the Nomura model numbers are 2023–2026 press snippets.
- instruments: ES/MES (primary), NQ; FTMO US500 (intraday or Swing: the multi-day version holds across the close with swap).
- holding / trades per year: on day t+1..t+3 after a day whose |return| > 1.5% raised 21-day realized vol by > 15% relative: enter 15:00 ET on the vol-change sign (short after a vol jump, long after a vol collapse), exit 15:59 (futures) or hold to the next ...
- data + cost: ES 1m RTH (in hand 2008–2026, licence-held copy cross-check only; or Databento ≈ $7); S&P daily (free) for the vol trigger. $0–7. [free first pass]
- gross vs cost: the sell-side forecast implies ≈ 0.3–0.5% of ES ADV notional per day on the big days; square-root impact of that is 5–15 bp over the hour vs 1.2 bp RT → passes the screen if a third of it is in the last hour and not pre-hedged.
- firm fit: intraday futures (15:00 → 15:59, inside every deadline); FTMO Swing variant holds 2–3 nights (swap ≈ −8%/yr long US index / ≈ +0.4% short per the E1 numbers). Consistency rules: sparse big days concentrate P&L (Topstep consistency policy ...
- haircut: 0.5 (bank models publish the flow daily; it is as public as flow gets); splits at 2018-02 (Volmageddon), 2020-03, 2022.
- analyst line: closed: H0006/H0019 window, conditioned on a known external order (not momentum); A-C30 adjacent; look-ahead: realized-vol trigger from closes to t-1; econ: 5-15 bp hour impact vs 1.2 bp RT -> 1-3x after 0.5 haircut; ~40 big days/yr; splits 2018-02, 2020-03, 2022; firm: IF 15:00-15:59 + FTMO Swing variant

### 17. IG C-12-24 — Buyback-desk dip buying 13:00–15:50 on down days outside blackout, with in-blackout control — TOP10 (6)
- score 14/21 — M3 E1 C2 F3 D2 X2 P1; plausibility low; lane 12; original yes
- mechanism: S&P 500 companies repurchase ≈ $900bn–1tn a year, executed by broker desks under 10b-18's safe harbour (≤ 25% of ADV, no purchases in the last 10 minutes, price ≤ the highest independent bid), typically as VWAP/participation programs that are *price-sensitive* (desks buy more on down days). About 5 weeks before each earnings date most issuers are in blackout (unless on a 10b5-1 plan). So on down days outside ...
- evidence: practitioner (desk behaviour, 10b-18 text) + a negative daily study; own intraday construction.
- evidence window: Bernstein daily study ≈ 2010–2018 (per snippet; verify); intraday untested.
- instruments: ES/MES; FTMO US500 intraday.
- holding / trades per year: on days with 09:30 → 13:00 return < −0.5% and blackout share < 30%: long 13:00 → 15:50; ≈ 40–60 trades/yr, with the in-blackout down days as the pre-registered control arm.
- data + cost: ES 1m RTH (in hand / $7); earnings calendar + S&P membership (in hand, free). [free first pass]
- gross vs cost: if buyback desks add ≈ 2–4% of ADV on those afternoons the square-root impact is ≈ 5–10 bp vs 1.2 bp RT → passes the screen on paper.
- firm fit: intraday futures (13:00 → 15:50 ET); MFFU 14:00 FOMC days excluded; no minimum-hold issue.
- haircut: 0.5 (the blackout calendar is public); splits at 2018 (tax-reform buyback surge), 2023 (1% excise tax).
- analyst line: closed: G2 (daily index dip buy) adjacent, this is intraday conditioned on a named buyer's calendar with an in-blackout control arm; look-ahead: blackout share from the earnings calendar known ex ante; econ: 5-10 bp vs 1.2 bp RT -> 1-2x after 0.5 haircut; 40-60/yr; splits 2018, 2023 (1% excise tax); firm: IF/FTMO intraday

### 18. AF C-2-09 — FOMC three-day window in long Treasuries, overnight-session holds
- score 13/21 — M2 E2 C1 F2 D2 X2 P2; plausibility low-medium; lane 2; original yes
- mechanism: Hillenbrand (RFS 2025): the entire 1980–2017 fall of the 10y yield (10.1% → 2.4%) occurred inside the three-day window (day before, day of, day after) around FOMC meetings; moves outside the window wash out; attributed mainly to a lower expected short-rate path. Pan–Peng (2026; 250 scheduled announcements since 1994; ZN futures 2004–2025): a pre-FOMC Treasury drift on the day before the announcement — 10y ...
- evidence: peer-reviewed (Hillenbrand, "The Fed and the Secular Decline in Interest Rates", RFS 38(4) 2025 981–1013, https://www.hbs.edu/faculty/Pages/item.aspx?num=67591; summary https://quantpedia.com/secular-decline-in-yields-around-fomc-meetings/, fetched 2026-11-03) + working paper (Pan & Peng, "The Pre-FOMC Drift in Long-Term Treasury Bonds", June 2026, ...
- evidence window: US Treasury yields around FOMC 1989–2017 (Hillenbrand RFS 2025), long-term Treasuries/futures to 2025 (Pan–Peng 2026, sub-periods not extracted), cross-country 10y yields to ≈ 2023 (BIS WP 1252, verify). Overnight-session capture in ZB/UB never measured.
- instruments: ZN, ZB, UB (TN); FTMO none.
- holding / trades per year: 8 meetings × 2 windows = 16 holds/yr, ≈ 17.5 h each.
- data + cost: ZN/UB 1h full session (≈ $1/root suffices; 1m shared with C-1-01); FOMC calendar (free); MOVE/VIX daily (free). [Databento]
- gross vs cost: −0.79 bp of 10y yield ≈ +5.5 bp price in ZN (duration ≈ 7) and ≈ +13 bp in UB (duration ≈ 17) per pre-FOMC window vs RT ≈ 3 bp (ZN) / 5–6 bp (UB) → passes the screen in UB (≥ 2 × RT), marginal in ZN; 16 trades/yr → sleeve only; the in-sample t ≈ 2.4 is below the program bar.
- firm fit: overnight-session futures (18:00 ET entry, exits 11:30 ET / 15:00 ET); the 14:00 ET statement is never held through → no news-window conflict; consistency rules touched.
- haircut: 0.5 (published 2025/2026, high profile); splits at 2008-12 (ZLB), 2015, 2022-03.
- analyst line: closed: E2-05 (pre-FOMC ES/NQ) adjacent, different asset and window; look-ahead: FOMC calendar public; econ: UB +13 bp/window vs RT 5-6 -> ~1.2x after 0.5 haircut, ZN marginal, 16/yr, in-sample t 2.4; splits 2008-12, 2015, 2022-03; firm: ONF holds; holding through 14:00 FOMC is banned at MFFU Rapid/Pro and Lucid Daily -> Topstep/Bulenox only

### 19. SC C-13-02 — FOMC press-conference vocal tone → US500 drift (new data vs closed E2)
- score 13/21 — M2 E2 C3 F2 D2 X1 P1; plausibility low; lane 13; original no
- mechanism: Gorodnichenko–Pham–Talavera show that the emotional tone of the Fed chair's voice during the press conference, after controlling for the policy action and the text sentiment, moves stock prices; a positive voice tone raises the S&P 500 with a magnitude comparable to a one-standard-deviation forward-guidance shock. The information is orthogonal to the statement text and to the policy surprise, so the E2 ...
- evidence: peer-reviewed — Gorodnichenko, Pham, Talavera (2023) "The Voice of Monetary Policy", AER 113(2) 548–584, https://econpapers.repec.org/RePEc:aea:aecrev:v:113:y:2023:i:2:p:548-84 (abstract only, fetched 2026-11-03); working paper NBER w28592 / draft https://eml.berkeley.edu/~ygorodni/VoiceMP.pdf (not opened): sample 2011–June 2019, 36 press conferences; moving the tone from −1 ...
- evidence window: S&P 500 around FOMC press conferences 2011–2019.
- instruments: US500, US100 (FTMO); ES/MES only inside the futures-firm day (14:30–15:10 CT window) with the MFFU/Lucid news bans in mind.
- holding / trades per year: enter during the Q&A once the running tone score is stable (~15:00 ET), exit at 16:00 ET (intraday) or next day 09:30 ET (Swing, one swap). 8/yr.
- data + cost: Fed webcast audio archive 2011–2026 (federalreserve.gov, free); open-source speech-emotion model; 1-minute ES or SPXUSD (HistData free 2010–2018 gappy; Databento ES 1m RTH ≈ $6–7 for one root if bought for other lanes); ... [free first pass]
- gross vs cost: if the published 200 bp swing per 2 units of tone holds and the usable realized tone is ±0.5, ≈ ±50 bp per event gross against 1–3 bp round trip → passes the economics screen. Sensitivity is to classifier noise, not cost.
- firm fit: FTMO intraday CFD or Swing (news allowed on Swing; on Standard the ±2-minute ban covers the 14:00 statement, not the 14:30–15:30 presser — to be verified in the rules matrix); futures firms: Topstep/Bulenox allow news; MFFU Rapid/Pro and ...
- haircut: 0.5 (published 2021 WP / 2023 AER). Splits: 2019 (presser after every meeting), 2021 (publication).
- analyst line: closed: E2-01..04 (same event, same index, price continuation) - new data source (vocal affect) is the new element; look-ahead: classifier must be trained on pre-2019 audio only; econ: +-50 bp/event vs 1-3 bp RT; 8/yr; haircut 0.5, splits 2019, 2021; firm: FTMO intraday/Swing, ES at Topstep/Bulenox (MFFU/Lucid news windows irrelevant at 15:00 ET)

### 20. AF C-1-02 — Month-end cross-asset rebalancing, bond leg only
- score 13/21 — M2 E2 C1 F2 D2 X3 P1; plausibility low; lane 1; original yes
- mechanism: Pension and balanced funds rebalance to 60/40 on the last business day (calendar rule) or when drift exceeds a threshold; when stocks have outperformed bonds month/quarter-to-date they sell equity exposure and buy duration. Paper (S&P 500 and 10y note futures, daily, 1997-09-10 → 2023-03-17): a 1-sd signal lowers next-day equity returns by ≈ 17 bp and raises bond returns ≈ 3 bp; calendar predictability concentrates ...
- evidence: working paper (Harvey, Mazzoleni & Melone, "The Unintended Consequences of Rebalancing", NBER WP 33554, March 2025, https://www.nber.org/system/files/working_papers/w33554/revisions/w33554.rev0.pdf, fetched 2026-11-03, abstract p.1, pp. 3, 19–21, Table 7) + blog replication with code (Quantitativo, https://www.quantitativo.com/p/the-unintended-consequences-of-rebalancing, ...
- evidence window: US 60/40 rebalancing proxies, S&P and Treasury futures, ≈ 1997 → 2023-03 (NBER w33554; start year not re-verified; no sub-period split published); Quantitativo replication over the same window, no OOS.
- instruments: ZN (primary), ZB/UB (duration-scaled); ES leg excluded; FTMO: none.
- holding / trades per year: when |signal| > 1 sd, enter at 18:00 ET on each of the last four business days, exit 15:00 ET next day (16:05 on the last day): ≈ 20–30 holds/yr; the paper's effect is close-to-close, so an intraday-only variant captures less.
- data + cost: daily ES and ZN for the signal (free: Stooq/Yahoo continuous, or Databento 1d ≈ $0.05/root); ZN/UB 1h or 1m for execution (shared with C-1-01). ≈ $0–20. [free first pass]
- gross vs cost: ≈ 3 bp on ZN per 1-sd day; perhaps 5–8 bp at quarter-ends with > 2-sd signals; ZN RT ≈ 3 bp → FAILS the economics screen for ZN; UB (≈ 2.5x duration → 7–20 bp vs RT ≈ 5–6 bp) at |signal| > 2 sd is the only registrable variant.
- firm fit: overnight-session futures (18:00 ET → next-day 15:00/16:05 ET); consistency rules touched (quarter-end clustering); no news windows.
- haircut: 0.5 (published 2025; front-running acknowledged by market participants in the paper); splits at 2008-12, 2020-03, 2025-03 (publication).
- analyst line: closed: none (H0023 other asset); look-ahead: signal must use MTD returns to T-1 only; econ: ZN ~3 bp vs RT 3 bp FAILS, UB at 

### 21. AF C-1-03 — Auction-day inverted V in ZN/ZB/UB
- score 13/21 — M3 E2 C1 F2 D1 X3 P1; plausibility low; lane 1; original no
- absorbs: pre-sweep A-C10
- mechanism: Dealers absorbing a known supply shock sell/hedge in the hours before the 13:00 ET bidding deadline and buy back after results; net order flow transmits the pressure. Fleming–Liu–Nguyen (1-minute interdealer cash data, 1991–2024, 1,684 auctions): six-hour-window yield pressure 0.7–1.2 bp (pre-auction run-up 0.36–0.63 bp, post-auction reversal −0.28 to −0.77 bp), price-based pressure 1.3 bp (2y) to > 17 bp (30y) full ...
- evidence: central-bank staff report (Fleming, Liu & Nguyen, "Intraday Price Pressure and Order Flow Around U.S. Treasury Auctions", FRBNY Staff Report 1188, March 2026 rev. Oct 2026, https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1188.pdf, fetched 2026-11-03, abstract and pp. 19–22, Tables 2–3) + peer-reviewed (Smales, Accounting & Finance 61(S1) 2021 1517–1555, ...
- evidence window: cash Treasuries (BrokerTec/GovPX) '33 years of intraday data' to ≈ 2024 (SR1188 abstract, snippet 2026-11-04; post-2015 sub-period weakest); ZN futures to 2017 (Smales 2021); Sigaux JBF 2024 and Somogyi–Wallen–Xu 2025 windows not extracted (abstracts only).
- instruments: ZN (3y/7y/10y auctions), ZB/UB (20y/30y), ZF (5y), ZT (2y); FTMO none.
- holding / trades per year: leg 1 short the auctioned tenor's contract 09:00 → 12:59 ET; leg 2 long 13:11 → 15:00 ET (10-minute buffer as in the paper's robustness check); ≈ 100–200 trades/yr; conditioning: VIX tercile and bid-to-cover sign.
- data + cost: Databento 1m ZN and UB RTH 2010–2026 (≈ $7 each; full-session files shared with C-1-01 cover it); TreasuryDirect auction calendar/results incl. bid-to-cover and tail (free); VIX daily (free). [Databento]
- gross vs cost: post-2014 total pressure 0.3–0.9 bp of yield ≈ 2–6 bp price in ZN (duration ≈ 7) and 5–15 bp in UB (duration ≈ 17), about half per leg → FAILS the screen for ZN (edge ≤ RT ≈ 3 bp per leg) and is marginal for UB unless conditioned on tight-dealer/high-VIX days where the paper shows larger pressure. Win rate unknown.
- firm fit: intraday futures (both legs inside 09:00–15:00 ET); auction results (13:01 ET) are not on firm Tier-1 news lists (verify MFFU/Lucid lists); minimum-hold rules irrelevant.
- haircut: 0.5; splits at 2007, 2015 (regulatory implementation per the paper), 2020-03.
- analyst line: closed: none (E2 is ES/NQ); look-ahead: auction calendar public; econ: ZN 2-6 bp per two legs FAILS, UB 5-15 bp marginal, 100-200/yr; haircut 0.5, splits 2007, 2015, 2020-03; firm: IF, no news clause (auction 13:00 not a listed release)

### 22. AF C-2-03 — EIA CL first-reaction fade
- score 13/21 — M2 E2 C1 F2 D2 X3 P1; plausibility low; lane 2; original no
- absorbs: pre-sweep A-C14
- mechanism: Miao–Ramchander–Wang–Yang (JFM 2018): futures fall after positive inventory surprises; no asymmetry in futures; volatility normalises faster after jump announcements. Rousse–Sévi: over-reaction partly reversed within hours. Krueger (lit-practitioner closed-family cross-references): EIA crude first reaction −14.65 bp (t −2.7) for continuation, i.e. fading the first move was positive in his 2015–2026 CFD sample. This ...
- evidence: peer-reviewed (Miao, Ramchander, Wang & Yang, "The impact of crude oil inventory announcements on prices: Evidence from derivatives markets", JFM 38(1) 2018 38–65, https://ideas.repec.org/a/wly/jfutmk/v38y2018i1p38-65.html, abstract via search 2026-11-03; Geman & Li 2018 per A-C14) + blog with holdouts (Krueger, per lit-practitioner). Post-2015 OOS: Krueger's −14.65 bp (t ...
- evidence window: CL futures and options around EIA releases, ≤ 2016 (Miao et al., JFM 2018; exact window not extracted); Krueger holdout CL/USOIL 2023–2026 (lit-practitioner, −14.65 bp first reaction).
- instruments: CL/MCL; FTMO USOIL.
- holding / trades per year: 10:33 → 11:30 ET, ≈ 50/yr.
- data + cost: CL 1m RTH (shared with C-2-02); EIA actuals (free). $0 incremental. [Databento (shared root)]
- gross vs cost: ≈ 10–15 bp gross vs CL RT ≈ 4 bp (assume 2 ticks slippage at 10:33) → passes at 1× costs, fails at 2× unless larger on big-surprise days.
- firm fit: intraday futures; entry at 10:33 is outside ±2 min; Lucid Daily red-folder risk; FTMO intraday fine.
- haircut: 0.5; splits at 2015, 2020-04.
- analyst line: closed: none (E2 is ES/NQ); look-ahead: entry 10:33 after the surprise is public; econ: 10-15 bp vs CL RT 4 bp -> passes 1x, fails 2x after haircut; ~50/yr; haircut 0.5, splits 2015, 2020-04; firm: IF/FTMO intraday, entry outside the +-2 min window

### 23. AF C-2-07 — LBMA auctions: Nilsson kill-test + round-imbalance leg
- score 13/21 — M2 E2 C1 F3 D1 X3 P1; plausibility low; lane 2; original yes
- absorbs: pre-sweep A-C18
- mechanism: Pre-2015 the PM fix leaked (Caminschi–Heaney: volume/volatility spike at the start of the fix; Aspris et al.: leakage ≈ 4–10 bp pre-reform and "far less" under the electronic auction). The ICE/LBMA auction publishes round-by-round price and imbalance (≈ every 45 s) at 10:30 and 15:00 London (gold) and 12:00 London (silver) — a public, time-stamped order imbalance. Nilsson (2015, as summarised by Crain et al.): ...
- evidence: peer-reviewed (Caminschi & Heaney JFM 34(11) 2014 1003–1039, per A-C18; Crain, Hoelscher & Jones, "Fixing the Fix for Silver and Gold", ACRN Journal of Finance and Risk Perspectives 9 (2020) 177–197, http://www.acrn-journals.eu/resources/jofrp09m.pdf, fetched 2026-11-03) + working papers (Aspris, Foley, Gratton & O'Neill, "Towards a New Fix", 2015, ...
- evidence window: gold/silver spot and futures around the LBMA auctions, pre-reform ≈ 2007–2013 (Caminschi–Heaney, per A-C18) and post-reform 2014–2017 (Crain et al. 2020; Aspris et al. 2015/2017, market quality only). Round-imbalance leg (b) untested.
- instruments: GC/MGC, SI/SIL; FTMO XAUUSD/XAGUSD.
- holding / trades per year: AM auction ≈ 05:30–05:40 ET, PM auction ≈ 10:00–10:10 ET (one hour later during the 2–3 weeks of US/UK DST mismatch); ≈ 500 auctions/yr.
- data + cost: Databento 1m GC full session (≈ $20; the AM auction is outside US RTH); LBMA/ICE round-by-round history (published on the LBMA/ICE sites; historical depth to verify, possibly free). [Databento]
- gross vs cost: a few bp per auction vs GC RT ≈ 0.6–1 bp → passes only if ≥ 2 bp per event systematically; Aspris et al.'s "far less leakage" argues ≈ 0; the round-imbalance leg is the only mechanism with a public real-time signal.
- firm fit: overnight-session futures for the AM auction (05:30 ET is inside the futures-firm day), intraday for the PM; FTMO intraday CFD; the 10:00 ET PM auction coincides with US 10:00 releases → news-window bans on those days.
- haircut: 0.7 (leg b) / 0.5 (Nilsson pattern); splits at 2015-03-20 (gold), 2014-08-15 (silver).
- analyst line: closed: none; look-ahead: round-imbalance published live by LBMA (verify timestamp); econ: few bp vs GC RT 0.6-1 bp; post-reform leakage ~0; ~500/yr; haircut 0.5/0.7, splits 2015-03-20, 2014-08-15; firm: ONF (05:30 ET) / IF (10:00 ET) / FTMO XAUUSD

### 24. AF C-2-12 — Auction-result surprise continuation ZN/UB
- score 13/21 — M2 E2 C1 F2 D2 X3 P1; plausibility low; lane 2; original no
- mechanism: Auction results (13:01–13:03 ET) resolve demand uncertainty. Smales (ZN 15-min bars 2000–2017): higher bid-to-cover → positive returns and lower volatility in the interval right after the auction. Ray–Droste–Gorodnichenko (JPE 2024) use the yield change in a 30-minute window around auction results as a demand shock with persistent effects on yields over subsequent weeks (robust to using futures), i.e. the shock is ...
- evidence: peer-reviewed (Smales, Accounting & Finance 61(S1) 2021, snippet 2026-11-03, UWA repository URL in C-1-03; Ray, Droste & Gorodnichenko, "Unbundling Quantitative Easing: Taking a Cue from Treasury Auctions", JPE 132(9) 2024 3115–3172, https://ideas.repec.org/a/ucp/jpolec/doi10.1086-729581.html, abstract via search 2026-11-03) + staff report (SR1188, fetched). Post-2015 OOS: ...
- evidence window: ZN futures around 13:01 ET results to 2017 (Smales 2021); auction surprises and yields to ≈ 2020 (Ray–Droste–Gorodnichenko JPE 2024, verify); cash Treasuries to ≈ 2024 (SR1188). UB and post-2020 futures untested.
- instruments: ZN (10y/7y/3y), ZB/UB (30y/20y), ZF (5y); FTMO none.
- holding / trades per year: 13:06 → 13:45 ET, ≈ 100 auctions/yr.
- data + cost: ZN/UB 1m RTH (shared); TreasuryDirect results (free; when-issued tails from trade press) — the 13:00 → 13:05 price move is the free proxy. [Databento (shared root)]
- gross vs cost: continuation of a 5–10 bp result move by 2–4 bp vs ZN RT ≈ 3 bp → marginal/fails; UB (≈ 3x) passes if the pattern exists. Prior: the 13:01 reaction is arbitraged within seconds; only slow demand-shock persistence could leave 30-minute drift.
- firm fit: intraday futures; auction results not on firm Tier-1 lists (verify); minimum-hold fine.
- haircut: 0.5; splits at 2010 (demand-elasticity break per HBS 26-033), 2015.
- analyst line: closed: none; look-ahead: result at 13:01, entry 13:06; econ: 2-4 bp continuation vs ZN RT 3 bp FAILS, UB marginal; ~100/yr; haircut 0.5, splits 2010, 2015; firm: IF

### 25. IG C-12-08 — VIX ETP leverage rebalancing → ES delta leg 15:45–16:15 — TOP10 (9)
- score 13/21 — M3 E2 C1 F2 D2 X2 P1; plausibility low; lane 12; original yes
- mechanism: daily-reset VIX ETPs rebalance VIX-futures exposure at the 16:15 ET VIX-futures settlement in the direction of the day's VIX-futures move (Todorov, "When passive funds affect prices", Review of Finance 28(3) 2024, 831–863, https://econpapers.repec.org/RePEc:oup:revfin:v:28:y:2024:i:3:p:831-863; BIS WP 952 https://www.bis.org/publ/work952.pdf; abstracts/snippets 2026-11-04: leverage rebalancing is the largest ...
- evidence: peer-reviewed for the VX pressure; own idea for the ES leg. VIX ETP AUM (free, issuer pages): UVXY/SVXY/SVIX/UVIX of the order of $1–3bn each at 1.5×/−1×/2×; required daily VX notional = Σ AUM × L(L−1) × r_VX.
- evidence window: VX 2004–2019 (Todorov; window per BIS version, verify); ES 15:45–16:15 untested.
- instruments: ES/MES; secondary NQ.
- holding / trades per year: 15:45 → 16:08 (Topstep) / 16:10 (MFFU) / 16:14 (Lucid); trigger |VX front return at 15:45| > 5% → ≈ 40–60 days/yr.
- data + cost: ES 1m full session (16:00–16:15 bars; ≈ $20) or the RTH copy for the 15:45–16:00 part ($0 in hand, licence-held for cross-check); VX daily/1m — CBOE delayed VIX futures history is free daily, not 1m (VX is CFE, not in ... [free first pass]
- gross vs cost: a 10% VX day on $5bn of levered ETP AUM ≈ $1bn VX ≈ 50k ES-vega-equivalents … in delta terms a few thousand ES over 30 minutes → 3–8 bp vs 1.2 bp RT: passes the screen on those days if dealers do not pre-hedge (they partly do, per Barbon et al. on equity LETFs).
- firm fit: intraday futures (exit before each deadline; the 16:00–16:15 part needs Lucid/Tradeify/Bulenox/FTMO); no news windows.
- haircut: 0.5 (published mechanism); splits at 2018-02 (XIV termination), 2022 (SVIX/UVIX launch).
- analyst line: closed: G1 (needs no VIX product), H0006/H0019 window conditioned on a computable external flow; look-ahead: VX return at 15:45 known; econ: 3-8 bp vs 1.2 bp RT -> 1.5-4 bp after haircut, ~1-1.7x; 40-60 days/yr; haircut 0.5, splits 2018-02, 2022; firm: IF to 16:08 (Topstep) / 16:14 (Lucid) / FTMO

### 26. SC C-13-04 — KRT position-change liquidity provision, post-release, across 16 FTMO commodity CFDs
- score 13/21 — M2 E2 C1 F2 D3 X2 P1; plausibility low; lane 13; original no
- mechanism: KRT show hedgers provide short-term liquidity to speculators: commodities most bought by speculators (sold by hedgers) in the week to Tuesday under-perform over the next 20 days and vice versa; a long–short on hedger buying earns 0.431 % (halves, t = 4.16) and 0.667 % (quintiles, t = 4.02) over 20 days, of which 0.433 % (quintiles) accrues AFTER the Friday 15:30 ET public release — so the lagged, public COT report ...
- evidence: peer-reviewed — Kang, Rouwenhorst, Tang (2020) "A Tale of Two Premiums", J. Finance 75(1) 377–417, https://ideas.repec.org/a/bla/jfinan/v75y2020i1p377-417.html; numbers from the NBER conference draft (Oct 2013) https://conference.nber.org/conf_papers/f69870/f69870.pdf (PDF fetched and text-extracted 2026-11-04, pp. 3, 18–19 and Table 5): 26 commodities, weekly COT 1994-01-02 → ...
- evidence window: 26 US commodity futures 1994–2012.
- instruments: FTMO commodity CFDs (fetched list): USOIL, UKOIL, NATGAS, HEATOIL, XAU, XAG, XPT, XPD, XCU, CORN, WHEAT, SOYBEAN, COCOA, COFFEE, SUGAR, COTTON — 16 names, enough for halves/terciles. Swap filter: ...
- holding / trades per year: form on Friday 15:30 ET release, enter Monday 00:05 platform time (after the weekend; or Friday 15:35 ET if Swing), hold to day 16 after the Tuesday; weekly re-formation → 52 formations × ~8 legs ≈ 400 leg-trades/yr.
- data + cost: CFTC legacy + disaggregated COT 1994–2026 (free, cftc.gov, browser UA per the board); daily futures settlements for the 16 underlyings 1994–2026 (Databento 1d ≈ $0.80 total, or free Stooq/Yahoo when reachable); FTMO ... [Databento]
- gross vs cost: ≈ 0.43 % per 16-day long–short formation (quintiles, post-release part) ≈ 27 bp per leg; CFD spreads 1–8 bp per side plus swaps −0.1 to −0.4 % per 16 days on long legs → net ≈ 0–15 bp per leg: passes the economics screen only on the energy-long / metals-short / ags configuration; a 2× cost run turns it negative. Carver speed limit: weekly turnover of ~8 ...
- firm fit: FTMO Swing (16-day holds, weekends). Futures firms: no.
- haircut: 0.5 (published 2013 WP / 2020 JF). Splits: 2006 (disaggregated/CIT reports), 2013 (publication), 2020-04.
- analyst line: closed: none (P-C17 weekly reversal is the price-only cousin); look-ahead: COT released Friday 15:30 ET for Tuesday positions - enter after release only; econ: ~27 bp/leg per 16 days gross vs CFD 1-8 bp + swaps -> net 0-15 bp; weekly formation; haircut 0.5, splits 2006, 2013, 2020-04; firm: FTMO Swing

### 27. SC C-8-06 — Commodity multi-day dip buy with the real swap sign (crude earns carry)
- score 13/21 — M1 E1 C3 F2 D3 X2 P1; plausibility low; lane 8; original no
- absorbs: pre-sweep P-C16, pre-sweep P-C24
- mechanism: sharp two-to-three-day falls in crude and gold are partly liquidity-driven (margin calls, CTA de-risking, index-roller timing) and partly revert over 3–5 sessions. P-C16/P-C24 listed this with no fetched rules. New facts: on FTMO terms a USOIL long currently EARNS swap (+5 %/yr) and a gold long pays −5.2 %/yr, so the crude leg is the only one where the holding cost is not a headwind; and the dip-buy family is closed ...
- evidence: blog with (paywalled) code — Quantified Strategies "Crude oil trading strategy (backtest + setup)", https://quantifiedstrategies.substack.com/p/crude-oil-trading-strategy-backtest (page returned 404 to a direct fetch on 2026-11-03; search snippet: USO 2008–2026, mean reversion after sharp drops, 169 trades, +0.4 % average per trade, no costs, rules paywalled). Blog — Delphic ...
- evidence window: USO 2008–2026 and CL/GC 2008–2026 (blogs, in-sample, no holdout stated).
- instruments: USOIL.cash (primary), XAU/USD (secondary, swap-penalized), UKOIL.cash; XAG/USD excluded (swap −9.7 %/yr).
- holding / trades per year: enter next open after a 2-day return < −2σ(60d), exit after 3 sessions or first close above the 5-day mean; ≈ 8–12 trades/yr per market, 25–35 for three markets.
- data + cost: daily CL/GC/BZ 2000–2026 (Databento 1d ≈ $0.15 for three roots, or free EIA/LBMA series); HistData WTIUSD/BCOUSD/XAUUSD 1m (free, 2009/2010–2026) for the CFD open prints; $0–0.15. [free first pass]
- gross vs cost: +40 to +100 bp per 3-day hold claimed; spread 2.5 bp WTI / 1 bp gold per side plus 3 nights of swap (USOIL +0.04 %, gold −0.04 %) → passes the economics screen by a wide margin; a 2× cost run changes nothing material. The risk is that the claimed edge is in-sample selection.
- firm fit: FTMO Swing (3-session holds, possible weekend). Futures firms: no.
- haircut: 0.5. Splits: 2020-04 (negative WTI), 2022 (energy shock), 2026-01-30 (rolling contracts).
- analyst line: closed: G2-01..07 (index-CFD dip buys) - commodities were not in it (new markets, same rule class); look-ahead: none; econ: +40-100 bp per 3-day hold vs 2.5 bp + swap, 25-35/yr, blog in-sample; haircut 0.5, splits 2020-04, 2022, 2026-01-30; firm: FTMO Swing

### 28. AS C-3-03 — Gold overnight (Asian/London hours) drift as an 18:00 ET → 08:20 ET GC/MGC hold
- score 13/21 — M1 E1 C2 F3 D2 X3 P1; plausibility low; lane 3; original yes
- absorbs: AS C-3-05
- mechanism: Blose, Gondhalekar and Kort find overnight returns significantly positive and day returns significantly negative for COMEX front gold futures, the London fix spot market, gold miners and gold funds, in both up and down markets, "economically important after transaction costs"; they attribute it to gold being priced too high at the opening of the Western markets. A CBS thesis describes a hat-shaped intraday ...
- evidence: peer-reviewed (abstract only): Blose, Gondhalekar, Kort (2018), "Overnight versus day returns in gold and gold related assets", Journal of Economics and Finance 42(3):526–549, https://ideas.repec.org/a/spr/jecfin/v42y2018i3d10.1007_s12197-017-9403-0.html (fetched 2026-11-03; no magnitudes in the abstract). Student thesis (not peer-reviewed, snippet only): "Gold Price Dynamics ...
- evidence window: gold and gold-related assets in Blose-Gondhalekar-Kort 2018 (years not in the abstract) and a 2019 thesis; post-2018 untouched [window derived by the Prioritizer from the evidence field; the block predates the Day-0 field]
- instruments: GC / MGC (CME); FTMO XAUUSD (1 bp per side).
- holding / trades per year: 18:00 ET → 08:20 ET (COMEX floor open) or → 05:30 ET (London AM auction); ≈ 250/yr; variant: exit at the 10:30 London AM auction (05:30 ET for most of the year; schedule on the London clock because the US and UK DST switches ...
- data + cost: GC 1-h bars 2010–2026 (Databento ≈ $1) for the first pass, 1-min full session (≈ $20) for timing; LBMA auction calendar; Shanghai Gold Exchange and Tokyo holidays. [Databento]
- gross vs cost: unmeasured per night. Gold's tick ($0.10 ≈ 0.25 bp at ≈ $4,000) gives a low screen threshold: GC RT ≈ 2 ticks + $5 ≈ 0.6 bp, threshold max(0.5, 1.3) ≈ 1.3 bp (MGC ≈ 1 bp RT, threshold ≈ 2 bp); a +3 bp/night mean would pass — plausible if the 2018 result holds, unknown post-2018. 2 × cost run cheap.
- firm fit: overnight-session futures (entirely inside the day; flat ≥ 6 h before every deadline); FTMO intraday CFD: 18:00 ET ≈ 00:00 CE(S)T, so the hold sits inside one FTMO day with no swap if entered after the server rollover (verify rollover ...
- haircut: 0.5 (published). Split dates: 2015-03-20 (ICE LBMA gold auction replaces the fix), 2018 (publication), 2022–2025 (central-bank buying regime and Shanghai premium).
- analyst line: closed: none (D4 intraday CFD rules, not an overnight hold); look-ahead: none; econ: GC threshold 1.3 bp, a +3 bp/night mean would pass (2.5x after haircut), post-2018 unknown; ~250/yr; haircut 0.5 (0.7 Shanghai sub-window), splits 2015-03-20, 2016-04-19, 2018, 2022-25; firm: ONF 18:00->08:20 ET + FTMO XAUUSD intraday

### 29. IG C-12-16 — JHEQX quarter-end collar and monthly buffer-ETF resets into the close
- score 13/21 — M3 E1 C2 F2 D2 X2 P1; plausibility low; lane 12; original yes
- mechanism: JPMorgan Hedged Equity (JHEQX, ≈ $20bn+) rolls an SPX put-spread collar on the last trading day of each quarter, executed in the afternoon; dealers hedge the new strikes with ES into the close (Bloomberg 2025-03-11 and 2025-06-30 pieces, https://www.bloomberg.com/news/articles/2025-06-30/jpmorgan-fund-s-expiring-s-p-options-position-draws-market-focus; SpotGamma explainer https://spotgamma.com/jpm-collar-explained/; ...
- evidence: press and practitioner commentary; no measured close effect found; own construction.
- evidence window: none; JHEQX collar since ≈ 2013, prominent since 2020.
- instruments: ES/MES; FTMO US500 intraday.
- holding / trades per year: 15:00 → 15:59 ET; 4 quarter-ends + 8 other month-ends = 12 events/yr (a sleeve; annual contribution ≈ $200–400 per account at micro size).
- data + cost: ES 1m RTH (in hand / ≈ $7); strike history from the fund's filings and press (free, labour). [free first pass]
- gross vs cost: a $20bn collar roll moves dealers' net delta by a few $bn → 5–20 bp into the close on the quarter days; passes the screen if the sign is right.
- firm fit: intraday futures; coincides with C-12-15 (month-end rebalancing) and C-1-01 (Treasury strike) on the same afternoons → model the interaction, or register as one "last-day-of-quarter close" row.
- haircut: 0.5 (widely discussed since 2021); splits at 2020, 2023.
- analyst line: closed: H0006/H0019, A-C26 adjacent; look-ahead: JHEQX roll dates public; econ: 5-20 bp into the close if the sign is right; 12/yr; haircut 0.5, splits 2020, 2023; firm: IF

### 30. SC C-8-10 — HSI after-hours move → first-30-minute day-session reversal on HK50
- score 13/21 — M2 E1 C2 F2 D3 X2 P1; plausibility low; lane 8; original yes
- mechanism: HKEX's after-hours futures session (fetched: 5:00 pm → 3:00 am HKT, https://www.hkex.com.hk/Products/Listed-Derivatives/Equity-Index/Hang-Seng-Index-(HSI)/Hang-Seng-Index-Futures?sc_lang=en, 2026-11-03) prices HSI futures off US/European news with thin local participation; when the cash market reopens at 09:30 HKT (CFD 09:20 HKT = 01:20 UTC per the fetched FTMO hours), mainland and local institutional flow re-prices ...
- evidence: working paper / thesis — PolyU thesis (ira.lib.polyu.edu.hk/handle/10397/85644, search snippet 2026-11-03): pre-opening and extended-session HSI futures returns predict cash returns and "futures prices tend to reverse in the subsequent session", attributed to liquidity trading or overreaction; Cheng, Ng, Jiang (JFM) "Information content of extended trading for index futures" ...
- evidence window: HSI futures ≈ 1998–2005 (PolyU, Cheng et al.); Nikkei 2011–2017 (Miwa, per C-3-04). HSI 2012–2026 (AHT since 2013-04) untouched.
- instruments: HK50.cash (FTMO); HKEX HSI/MHI futures are not at any US futures firm.
- holding / trades per year: 01:20 → 02:00 UTC (09:20 → 10:00 HKT), fade the prior AHT move when |move| > 0.7 %; ≈ 60–90 trades/yr; variant: unconditional daily.
- data + cost: HistData HKXHKD 1m (free, 2010-11 → 2026) for both the AHT window and the open; HKEX daily AHT summaries (free pages, e.g. https://www.hkex.com.hk/eng/stat/dmstat/dayrpt/hsifa251010.htm, snippet) as the cross-check; $0. [free first pass]
- gross vs cost: if one third of a 1 % AHT move reverts in 40 minutes → ≈ 30 bp gross on event days vs HK50 spread (unknown at FTMO; assume 1.5–3 bp/side) → passes the screen on conditional days; unconditional version ≈ 3–5 bp vs 3–6 bp round trip → fails.
- firm fit: FTMO intraday CFD (no swap; inside the 01:20–04:00 UTC session). Futures firms: no (non-CME).
- haircut: 0.7 (transfer). Splits: 2013-04 (AHT launch), 2016-11 (AHT extended to 01:00), 2019-06 (to 03:00), 2023 (Stock Connect holiday trading).
- analyst line: closed: H0012/H0017 (US gap fade) logic in a market with its own after-hours print; look-ahead: AHT close known at 09:15 HKT; econ: ~30 bp conditional vs HK50 3-6 bp RT (spread unverified); 60-90/yr; haircut 0.7, splits 2013-04, 2016-11, 2019-06; firm: FTMO intraday (01:20-02:00 UTC)

### 31. AS C-4-06 — VIX/RV-gated 5–30-minute reversal in gold
- score 13/21 — M2 E1 C1 F3 D3 X2 P1; plausibility low; lane 4; original no
- mechanism: Nagel (2012): returns to liquidity provision rise sharply when VIX is high because dealer capital is constrained; Della Corte–Kosowski–Wang extend this to futures (the change in VIX over the non-trading hours adds explanatory power for reversal returns in every asset class); the drift-burst paper finds reversion after bursts in commodities. Pre-sweep A-C21 proposed the ES/NQ version; ES's 2.5 bp threshold is hard ...
- evidence: peer-reviewed mechanism (Nagel 2012, RFS; NBER w17653); futures extension in DKW (full text read, C-4-01); drift-burst commodities evidence (C-4-04). No gold-specific intraday reversal study found (searches 2026-11-03). Post-2015 OOS: none.
- evidence window: no gold window; mechanism evidence is US stocks daily (Nagel) and 35 futures daily 1982-2014 (DKW) [window derived by the Prioritizer from the evidence field; the block predates the Day-0 field]
- instruments: GC / MGC; FTMO XAUUSD.
- holding / trades per year: 5–30 min; z-score of the 5-minute return against a 60-minute rolling σ, fade when |z| > 2 only when VIX (or GVZ, free from CBOE) is above its 60-day 80th percentile; ≈ 100–300/yr.
- data + cost: GC 1-min full session 2010–2026 (≈ $20, shared); CBOE VIX and GVZ daily (free). [Databento (shared root)]
- gross vs cost: unknown; threshold ≈ 1.3 bp; a 5-minute 2-σ move in gold is ≈ 8–12 bp, so a 20 % partial reversion would pass — plausible but unmeasured.
- firm fit: intraday and overnight-session futures (fires in all hours); FTMO intraday CFD; the regime filter concentrates trades in days when daily-loss limits are closest (size down); exclude ±5 min around US releases and the London auctions.
- haircut: 0.5 (published mechanism). Split dates: 2015-03, 2020-03, 2024 (gold bull market).
- analyst line: closed: H0013/H0014 (daily IBS) different horizon; look-ahead: VIX/GVZ at T-1 close, z on closed bars; econ: 8-12 bp 2-sigma moves, 20% reversion would pass GC 1.3 bp; ~100+/yr; haircut 0.5, splits 2015-03, 2020-03, 2024; firm: IF/ONF/FTMO; latency risk vs HFT makers

### 32. IG C-12-27 — Nikkei SQ morning and HSI all-day-average expiry mechanics in NKD / JP225 / HK50
- score 13/21 — M2 E0 C2 F2 D3 X3 P1; plausibility low; lane 12; original yes
- mechanism: (a) Osaka/CME Nikkei 225 futures settle on the Special Quotation = the opening prices of all constituents on SQ day (JPX, https://www.jpx.co.jp/english/derivatives/products/domestic/225mini/01.html; CME Nikkei fact card, snippets 2026-11-04) → the same opening-auction unwind as C-12-26, at 09:00 JST = 19:00/20:00 ET (inside the futures-firm trading day as an overnight-session trade). (b) HKEX settles Hang Seng ...
- evidence: exchange rules for the mechanics; the settlement-method literature (Stoll–Whaley lineage, Hong Kong studies not fetched) for the direction; own rules.
- evidence window: none for these rules.
- instruments: NKD/NIY (CME, overnight session), FTMO JP225 and HK50 intraday CFDs.
- holding / trades per year: 25 minutes (NKD) / up to 5.5 hours (HK50); 24 events/yr → a sleeve (annual contribution small).
- data + cost: HistData JPX/JPY and HKX/HKD 1m (free, 2010–2026; CFD-priced); NKD 1m from Databento (≈ $20 full session) only after the free pass shows gross t > 3. [free first pass]
- gross vs cost: SQ-morning pushes of 0.3–0.6% in the Nikkei are the folklore; a third reverting = 10–20 bp vs JP225 CFD 1.5 bp/side → passes; HK50 TWAP-day drift suppression is a sizing fact more than an edge.
- firm fit: overnight-session futures (NKD at firms listing it; 19:00–20:00 ET) and FTMO intraday CFD; no news-window clauses.
- haircut: 0.5 (settlement effects are an old literature); splits at 2014 (JPX merger), 2020.
- analyst line: closed: none; look-ahead: SQ calendar public; econ: 10-20 bp vs JP225 1.5 bp/side; 24/yr; haircut 0.5, splits 2014, 2020; firm: ONF NKD (SQ morning 19:00-ish ET) / FTMO JP225/HK50

### 33. IG C-11-03 — Real value measures (AMP 2013) as the FTMO Swing stack's missing leg
- score 13/21 — M1 E2 C3 F2 D3 X2 P0; plausibility very low; lane 11; original no
- mechanism: slow value signals (FX: deviation from PPP; commodities: negative 5-year price change; bonds: real 10-year yield; equity indices: CAPE or dividend yield) earn a premium with monthly rebalance and low turnover; AMP (JF 68(3) 2013, "Value and Momentum Everywhere", not fetched; from memory, verify) report value Sharpe ≈ 0.3–0.6 per asset class and a 50/50 value–momentum combination near 1.0 before costs. The org's ...
- evidence: peer-reviewed (AMP 2013; sample ≈ 1972–2011); inherited D2 (trend + carry only; value never tested).
- evidence window: 1972–2011 (AMP, verify); 2012–2026 OOS is in the public factor data (AQR data library, free) — read once, as the gate requires.
- instruments: FTMO FX majors and crosses (PPP from OECD, free), index CFDs (CAPE from free sources), commodities (5-year reversal from Yahoo continuous series, free); no bond CFD at FTMO (verify) → bond leg ...
- holding / trades per year: monthly rebalance; ≈ 20–40 trades/yr.
- data + cost: $0 (FRED, OECD, Yahoo, AQR library). [free first pass]
- gross vs cost: n/a (portfolio); Sharpe ≈ 0.3–0.6 standalone in the literature → fails the 1.5 target alone by construction; registered only as a sleeve of the FTMO Swing stack (with C-11-02 and the C-8-01 trend sleeve).
- firm fit: FTMO Swing only; 30-day inactivity rule satisfied by monthly rebalancing; 5%/10% rules need a guard (C-11-05).
- haircut: 0.5; splits at 2008, 2020.
- analyst line: closed: D2 (trend/carry; value untested), G2; econ: monthly turnover, cost negligible; Sharpe 0.3-0.6 alone; haircut 0.5, splits 2008, 2020; firm: FTMO Swing (stack leg only)

### 34. AF C-2-02 — Pre-EIA CL drift with API conditioning
- score 12/21 — M2 E1 C2 F2 D2 X2 P1; plausibility low; lane 2; original yes
- mechanism: Rousse–Sévi (WTI intraday): in the two hours before the Wednesday 10:30 ET EIA release, on days when inventories later beat forecasts (builds), order flow is abnormal and the price falls ≈ 0.25% on average before the news — read as informed trading (the API figure is known to subscribers from Tuesday 16:30 ET); after the release an over-reaction is "partly compensated in the hours following". Ye–Karali (Energy ...
- evidence: peer-reviewed, abstracts only (Rousse & Sévi, "Informed Trading in the WTI Oil Futures Market", The Energy Journal 40(2) 2019 139–160, https://journals.sagepub.com/doi/10.5547/01956574.40.2.orou; abstract via https://ideas.repec.org/p/ags/feemes/249788.html, fetched 2026-11-03; Ye & Karali, Energy Economics 59 (2016) 349–364, abstract via ...
- evidence window: WTI front-month around Wednesday 10:30 ET, ≈ 2007–2014 (Rousse–Sévi executive summary, truncated snippet 2026-11-04); Ye–Karali ≤ 2015 (2016 working paper). Nothing after 2015.
- instruments: CL/MCL, RB, HO; FTMO USOIL.
- holding / trades per year: 08:30 → 10:29 ET on EIA days, ≈ 50 trades/yr; optional hold to 10:35.
- data + cost: Databento 1m CL RTH (≈ $7); API weekly headline history (scraped from news archives; API data itself is paid) → partial data gap; EIA actuals (free). [Databento]
- gross vs cost: 25 bp on build days (paper) vs CL RT ≈ 4 bp → passes the screen if the pattern survived; the common brief lists post-2014 pre-announcement drift as negative evidence (macro lock-up reforms) — EIA had no lock-up change, but HFT competition grew.
- firm fit: intraday futures; exit at 10:27 satisfies MFFU ±2 min; Lucid Daily red-folder (verify EIA classification) → avoid; FTMO intraday fine.
- haircut: 0.5; splits at 2015, 2020-04.
- analyst line: closed: negative-evidence row pre-announcement drift post-2014 (macro lock-ups; EIA had none); look-ahead: API Tue 16:30 known before entry; econ: 25 bp (2007-14) vs CL RT 4 bp, haircut 0.5 -> 3x if alive; ~50/yr; splits 2015, 2020-04; firm: IF 08:30->10:29, exit before the 10:30 release (MFFU +-2 min rule respected)

### 35. IG C-12-26 — Index-expiry settlement auctions: ES SOQ 09:30 and DAX 13:00 CET post-auction reversal
- score 12/21 — M2 E1 C2 F3 D2 X1 P1; plausibility low; lane 12; original partial
- mechanism: cash-settled index futures and AM-settled index options settle on an opening (SPX/ES quarterly: the Special Opening Quotation from each component's opening print on the third Friday) or an intraday auction (Eurex DAX futures/options: the Xetra intraday auction at 13:00 CET on the third Friday). Arbitrageurs unwinding cash-futures baskets and option hedgers must trade *in the auction*, which pushes the settlement ...
- evidence: peer-reviewed (1980s–1990s US); practitioner for recent years; own two-market construction. "Bare OPEX" negative evidence applies to day-level biases, not to a 25-minute auction-unwind window with a mechanism.
- evidence window: US 1984–1989 (Stoll–Whaley); DAX untested in any source seen; modern ES untested at the 5-minute scale.
- instruments: ES/MES; FTMO GER40 (intraday) for the Eurex leg; NKD/JP225 and HK50 are in C-12-27.
- holding / trades per year: 25–30 minutes; 4 US + 12 DAX (monthly index options; quarterly futures) = 16 events/yr → a sleeve; annual contribution at micro size ≈ $100–300 per account.
- data + cost: ES 1m RTH (in hand / $7); GRX/EUR 1m from HistData (free, 2010–2026). [free first pass]
- gross vs cost: auction pushes of 0.2–0.5% in DAX at 13:00 on expiry days are visible on charts; a third reverting = 7–17 bp vs 0.8–1 bp/side CFD → passes; ES 09:30 push smaller.
- firm fit: intraday futures; FTMO intraday CFD; no news windows.
- haircut: 0.5; splits at 1987 (US settlement moved to the open), 2020.
- analyst line: closed: bare OPEX negative row (day level), H0012/H0017 (09:31) window; econ: 7-17 bp DAX vs 0.8-1 bp/side CFD; 16/yr; haircut 0.5, splits 1987, 2020; firm: IF ES / FTMO GER40 intraday

### 36. pre-sweep P-C10 — Late-session breakouts after an early whipsaw (index), pre-sweep P-C10
- score 12/21 — M1 E1 C2 F3 D3 X1 P1; plausibility low; lane 4; original no
- mechanism: when the first range breakout fails both ways (chop), later-range breakouts carry the delayed directional flow
- evidence: lit-practitioner.md P-C10: C-US +0.024 -> +0.335 R, C-EU +0.111 -> +0.533 R conditional on an early whipsaw (Krueger, in-sample), fetched 2026-11-03
- evidence window: index CFDs 2015-2026 (Krueger) - derivative on those markets/dates
- instruments: ES/NQ; US500/US100/GER40
- holding / trades per year: hours; ~60-100/yr per market
- data + cost: 1m bars [free first pass]
- gross vs cost: R-based; cost small vs R
- firm fit: intraday futures and FTMO intraday
- haircut: 0.5
- analyst line: closed: H0020 / D4-04 (ORB families) adjacent - this is a late-day conditional breakout; econ: R-based (Krueger C-US +0.024 -> +0.335 R in-sample), cost small vs R; haircut 0.5; firm: IF/FTMO intraday

### 37. AF C-2-05 — Crop Progress → 20:00 ET reopen ZC/ZS
- score 12/21 — M2 E1 C1 F2 D2 X3 P1; plausibility low; lane 2; original yes
- mechanism: Weekly condition ratings (good/excellent %) are a scheduled information shock released after the 14:20 ET close. Lehecka (JARE 39(1) 2014; corn/soybeans 1986–2012): prices react rapidly and rationally to new condition information, strongest in July–August. The first tradable print is the 20:00 ET Globex reopen, inside the futures-firm trading day. Rule: direction = −sign(change in good/excellent % versus the prior ...
- evidence: peer-reviewed, abstract via search (Lehecka, "The Value of USDA Crop Progress and Condition Information: Reactions of Corn and Soybean Futures Markets", JARE 39(1) 2014; record https://ageconsearch.umn.edu/record/168261 — host returned 403; search snippet 2026-11-03). Post-2015 OOS: none found.
- evidence window: ZC/ZS reactions to Monday Crop Progress, sample ending ≤ 2012 (Lehecka, JARE 2014; start year not extracted). Nothing after 2014; the 20:00 ET reopen window never measured.
- instruments: ZC, ZS (MZC/MZS); FTMO none.
- holding / trades per year: 20:00 ET Monday → 13:15 ET Tuesday, ≈ 30 weeks × 2 roots ≈ 60 trades/yr (growing season).
- data + cost: Databento ZC/ZS 1h full session (≈ $1/root, first pass) or 1m (≈ $20/root); NASS Crop Progress history (free, QuickStats). [Databento]
- gross vs cost: order of 0.3–0.8% reaction to a 2-point rating change in July–August (magnitude inferred from the literature's description, not a measured figure) vs ZC RT ≈ 12 bp, ZS ≈ 5 bp → passes only if the reopen print does not already contain it; honest expectation: the opening gap carries most of it and the post-open drift is the testable residue.
- firm fit: overnight-session futures (20:00 ET → before deadlines); thin overnight grain books (assume 2 ticks slippage); no news windows.
- haircut: 0.7; splits at 2012, 2018.
- analyst line: closed: H0012/H0017 different asset/sign; look-ahead: report public at 16:00 ET, entry 20:00; econ: 0.3-0.8% reaction inferred vs ZC 12 / ZS 5 bp RT, gap may absorb it; ~60/yr seasonal; haircut 0.7, splits 2012, 2018; firm: ONF

### 38. AS C-3-01 — Regime-gated overnight drift 02:00–03:00 ET (authors report ≈ 0 since 2021)
- score 12/21 — M2 E1 C1 F3 D1 X3 P1; plausibility low; lane 3; original yes
- absorbs: AS C-3-02, pre-sweep A-C27, pre-sweep P-C20
- mechanism: liquidity providers absorb the end-of-day order imbalance at the 16:15 ET close and unwind when European liquidity arrives 02:00–03:00 ET, earning a positive return; the authors' pricing equation is E[overnight return] = closing dollar order imbalance × return variance × (risk-bearing capacity)⁻¹. NEW EVIDENCE: the same three authors report (2026-07-01) that the 02:00–03:00 window, which earned ≈ 3.7 %/yr over ...
- evidence: peer-reviewed origin (Boyarchenko, Larsen, Whelan, "The Overnight Drift", RFS 36(9):3502–3547, 2023, DOI 10.1093/rfs/hhad020) plus the authors' post-publication update: "The Disappearing Overnight Drift", Liberty Street Economics no. 20260701, DOI 10.59576/lse.20260701, https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/ and ...
- evidence window: ES 1998-2020 (BLW, RFS 2023) and the authors' 2021-2025 update (~0); a registered 2021+ OOS overlaps the update, so it is derivative there and is decided on NQ/YM or on data after 2026-07 [window derived by the Prioritizer from the evidence field; the block ...
- instruments: ES/MES (NQ/MNQ and YM/MYM as controls); FTMO US500 CFD (24 h, no swap intraday).
- holding / trades per year: 60 min (01:30–03:30 variant 120 min); unconditional 252/yr; gated variant 30–80/yr.
- data + cost: ES 1-min full session (Databento GLBX.MDP3 from 2010-06, ≈ $20 for the root; the 2008–2026 third-party ES 1m copy is under LICENCE HOLD, cross-check only); RSV proxy from the same bars (BVC); optional tbbo 3-month ... [Databento]
- gross vs cost: ≈ +1.5 bp per hour-trade pre-2021, ≈ 0 since. MES round trip at ≈ 6,500 index: 0.5 pt + $1.60 ≈ 1.3 bp; screen threshold max(2 ticks ≈ 0.8 bp, 2 × RT ≈ 2.5 bp) = 2.5 bp → FAIL unconditional. The gated variant passes only if its conditional mean is ≥ 2.5 bp, which nobody has measured.
- firm fit: overnight-session futures (entirely inside the 18:00-ET-anchored trading day, flat 13 h before the earliest deadline); FTMO intraday CFD (02:00 ET = 08:00 CE(S)T, no swap, inside one daily-loss day). No US Tier-1 release in the window; ...
- haircut: 0.5 (published; already observed ≈ 0 post-publication). Split dates: 2021-01 (post-publication, imbalance-dispersion collapse), 2020-03 (COVID vol), 2010-06 (Databento data start).
- analyst line: closed: none (H0009 stack held an untested overnight-drift leg); look-ahead: prior-day imbalance from RTH bars only; econ: ~0 since 2021 unconditional vs MES threshold 2.5 bp FAIL, gated variant unmeasured (30-80/yr); haircut 0.5, splits 2021-01, 2022-05; firm: ONF 02:00-03:00 ET (inside the trading day) / FTMO intraday

### 39. AS C-3-04 — Nikkei night-session overreaction → Tokyo day-session reversal in NKD/NIY
- score 12/21 — M2 E1 C1 F3 D2 X2 P1; plausibility low; lane 3; original no
- mechanism: Osaka's night session (16:30 → 06:00 JST, concurrent with Europe/US, ≈ 40 % of OSE futures volume) prices foreign news; Miwa shows night-session returns are negatively associated with subsequent day-session returns, that the overreaction strengthens with the length and activity of the night session, and that it is larger for Nikkei 225 futures (longer night session) than TOPIX futures. Domestic institutions and ...
- evidence: peer-reviewed (abstract only): Miwa (2019), "Trading hours extension and intraday price behavior", International Review of Economics & Finance 64:572–585, https://ideas.repec.org/a/eee/reveco/v64y2019icp572-585.html (fetched via search 2026-11-03); blind working-paper PDF ...
- evidence window: Nikkei futures around the 2011 night-session extension (Miwa 2019; years not confirmed) [window derived by the Prioritizer from the evidence field; the block predates the Day-0 field]
- instruments: NKD (CME Nikkei/USD, $5 × index, tick 5 pts) or NIY (yen); FTMO JP225 CFD.
- holding / trades per year: fade the night-session sign from 09:00 JST to 15:30 JST (or first 30 min); 245/yr unconditional, ≈ 60–80/yr gated on |night return| > 1 σ.
- data + cost: NKD 1-h (≈ $1) then 1-min full session (≈ $20) 2010–2026; OSE session calendar (night session end 03:00 → 05:30 in Jul-2016 → 06:00 in Sep-2021; cash close 15:00 → 15:30 on 2024-11-05); JST/ET DST map. [Databento]
- gross vs cost: not in the abstract. NKD tick ≈ 1 bp at ≈ 50,000; RT ≈ 2 ticks + $5 ≈ 2.2 bp; threshold ≈ 4.4 bp; a partial reversal of a 1 % night move would need ≥ 5 bp mean follow-through to pass → provisional FAIL until measured; CFD JP225 spread ≈ 1–1.5 bp per side gives a similar threshold.
- firm fit: overnight-session futures (verify NKD/NIY are on each firm's permitted list; flat 14 h before deadlines); FTMO intraday CFD (01:00–07:30 CE(S)T, inside one day, no swap). News: BoJ decision days (around 12:00 JST) excluded.
- haircut: 0.5 (published). Split dates: 2011-07, 2016-07, 2021-09 (night-session extensions), 2024-11-05 (cash close 15:30).
- analyst line: closed: H0012/H0017 logic (S&P, failed) in another market; look-ahead: night-session close known at 09:00 JST; econ: NKD threshold 4.4 bp, magnitude unknown; 60-80/yr gated; haircut 0.5, splits 2011-07, 2016-07, 2021-09, 2024-11-05; firm: ONF NKD 19:00-01:30 ET (Topstep lists NKD; others to verify) / FTMO JP225

### 40. AS C-5-03 — US close → Tokyo open: prior-day S&P return and Nikkei's first 30 minutes
- score 12/21 — M1 E1 C1 F3 D3 X2 P1; plausibility low; lane 5; original no
- mechanism: a 2026 paper reports that when the previous day's S&P 500 return was higher, lower returns follow in the first 30 minutes of Japanese trading — a reversal of the US-led overnight move at the 09:00 JST open, consistent with Miwa's night-session overreaction (C-3-04): the OSE night session over-prices foreign news and domestic order flow at the cash open leans the other way. Analogue for Australia: overnight SPI ...
- evidence: peer-reviewed, 2026 (title and search snippet only; ScienceDirect returned 403 on fetch): "How the prior day's S&P 500 returns influence the intraday returns of Nikkei 225 futures", https://www.sciencedirect.com/science/article/pii/S3050700626000204 (fetch attempted 2026-11-03). Miwa (2019) as in C-3-04. "Overnight futures trading: now even Australia and US have common trading ...
- evidence window: Nikkei 225 futures vs the prior-day S&P 500 (2026 paper; sample years not seen) [window derived by the Prioritizer from the evidence field; the block predates the Day-0 field]
- instruments: NKD / NIY (CME); FTMO JP225; (AUS200 CFD for the Australian analogue, FTMO only).
- holding / trades per year: 09:00–09:30 JST (19:00–19:30 ET winter, 20:00–20:30 ET summer), sign = −sign(S&P RTH return); 245/yr, ≈ 80/yr gated on |S&P return| > 1 σ.
- data + cost: NKD 1-min (≈ $20) or the inherited Oanda JP225_USD M1 copy (licence check); S&P RTH returns free. [Databento (shared root)]
- gross vs cost: unknown; NKD threshold ≈ 4.4 bp (C-3-04) → provisional FAIL until measured; a 30-minute window makes passive fills unlikely.
- firm fit: overnight-session futures (inside the day; verify NKD permitted); FTMO intraday CFD (01:00–01:30 CE(S)T winter).
- haircut: 0.5 (published 2026, sample unknown). Split dates: 2016-07, 2021-09 (night-session extensions), 2024-11-05.
- analyst line: closed: H0012/H0017 logic with a cross-market conditioner; econ: NKD threshold 4.4 bp, magnitude unknown; ~80/yr gated; haircut 0.5, splits 2016-07, 2021-09, 2024-11-05; firm: ONF NKD 19:00-19:30 ET / FTMO JP225

## D. Remaining mechanisms — one line each

- 41. **AS C-5-05** Crack-spread residual mean reversion after a one-leg shock (CL/HO/RB) — 12/21 (M2 E1 C1 F2 D2 X3 P1), low, orig no [absorbs pre-sweep P-C22] — closed: none; look-ahead: residual from rolling betas to T-1; econ: three-leg RT 8-10 bp, threshold ~20 bp of spread, shock days only 30-60/yr; haircut 0.5, splits 2020-04, 2022-03; firm: IF (three simultaneous legs allowed)
- 42. **IG C-12-20** Round-number stop/take-profit clusters (Osler 2003) on gold and index futures at 1m — 12/21 (M2 E1 C1 F3 D2 X2 P1), low, orig no — closed: H0001-H0004 (bot 'liquidity sweeps') - Osler's published stop/take-profit asymmetry is a distinct mechanism; econ: few bp vs GC 0.6-1 bp RT, needs win rate > 58% over hundreds of trades; 500-1,500/yr; haircut 0.5, splits 2010, 2019; firm: IF/FTMO intraday
- 43. **pre-sweep A-C21** VIX/realized-vol-conditioned intraday mean reversion in ES/NQ (Nagel-style liquidity ... — 12/21 (M2 E1 C1 F3 D2 X2 P1), low, orig no — closed: H0013/H0014 (daily IBS) different horizon; D4 intraday CFD rules were unconditional technical rules; look-ahead: VIX at T-1 close, z on closed bars; econ: only high-vol regimes give > 1-tick swings, unmeasured; hundreds/yr in high-VIX states; haircut 0.5 (Nagel 2012), splits 2020-03, 2022-05; firm: IF/FTMO intraday, ...
- 44. **SC C-8-11** European closing-auction reversal at index level (GER40/UK100/FRA40 after 17:35/16:35) — 12/21 (M2 E1 C1 F2 D3 X2 P1), low, orig no — closed: H0006/H0019 (US) adjacent window; look-ahead: auction print at 17:35 CET; econ: 2-5 bp vs GER40 RT 1.4 bp marginal, fails at 2x; 80-120/yr/index; haircut 0.5, splits 2018-01, 2021, 2025-04; firm: FTMO intraday
- 45. **IG C-12-05** Crypto liquidation-cascade exhaustion → MBT / FTMO BTCUSD — TOP10 (8) — 12/21 (M3 E0 C2 F2 D2 X2 P1), low, orig yes — closed: D3-01..11 (crypto momentum/funding/calendar) - forced liquidation is a new mechanism; look-ahead: Binance OI metrics timestamp lag must be measured; econ: 25-100 bp half-reversion vs MBT RT ~2 bp + $2 (FTMO 23 bp RT fails); 150-400/yr; haircut 0.7, splits 2021-05, 2022-11, 2024-01, 2025-10; firm: ONF MBT (verify MBT at ...
- 46. **IG C-12-18** Sunday 18:00 ET reopen overshoot fade, BTC-weekend sign filter — 12/21 (M2 E0 C2 F3 D2 X2 P1), low, orig yes [absorbs IG C-3-07] — closed: H0012/H0017 (09:30 gap fade) different session and crowd; look-ahead: entry after the 18:05/18:15 bar closes; econ: 3-13 bp reversion vs 1.2 bp ES / 1 bp GC RT on top days -> 1-4x after 0.7 haircut; weekday + Sunday ~200-400/yr across roots; splits 2017-12, 2020-03, 2024; firm: ONF (inside the trading day) / FTMO ...
- 47. **IG C-12-12** VIX-settlement Wednesdays: ES 09:31–09:45 fade of the SOQ-hedge unwind — 12/21 (M2 E2 C2 F2 D2 X2 P0), very low, orig yes — closed: E2 (no macro event), H0012/H0017 (09:31 gap fade) adjacent; econ: 7-13 bp vs 1.2 bp RT if alive; ~50/yr; haircut 0.5, institutional change 2018-05 (CBOE settlement reforms after Griffin-Shams) kills most of it; firm: IF
- 48. **pre-sweep A-C08** Around-the-clock USD time-of-day seasonality (Breedon-Ranaldo local-hours depreciation), ... — 12/21 (M2 E2 C1 F3 D3 X1 P0), very low, orig no — closed: D4 (check hour buckets) and P-C21 (EURUSD Breedon-Ranaldo NEGATIVE record); look-ahead: DST-correct local hours (C-7-06); econ: hour-bucket magnitudes not retrieved, 1-2 RT/day; haircut 0.5, splits 2015-02, 2018-01; firm: IF FX futures / FTMO FX
- 49. **SC C-13-05** Google-search FEARS → two-day US500 reversal; Preis-style timing recorded negative — 11/21 (M1 E2 C2 F2 D2 X1 P1), low, orig no — closed: G2 (dip buy US500, same outcome, price conditioning) adjacent; look-ahead: Google Trends daily series re-sampled per download - freeze a vintage; econ: +20-30 bp/2 days vs ~5.5 bp incl. swaps; ~25/yr; haircut 0.5, splits 2011, 2015, 2016; firm: FTMO Swing
- 50. **AF C-2-11** FOMC press-conference continuation ZN — 11/21 (M2 E2 C1 F2 D1 X2 P1), low, orig no — closed: E2-01..04 (same event, ES/NQ) adjacent; look-ahead: statement reaction known at 14:30; econ: 5-15 bp vs ZN RT 3 bp -> ~1-2.5x after haircut; 8/yr; haircut 0.5, splits 2019-01, 2022-03; firm: IF (press conference not inside the +-2 min statement window)
- 51. **AS C-5-09** US first half-hour → European last half-hour (cross-country ITSM, LSU) — 11/21 (M1 E2 C1 F2 D3 X1 P1), low, orig no — closed: D4-01 (own-market last half hour on CFDs) adjacent, foreign signal new; econ: ~2 bp/market-day vs CFD threshold 2-6 bp FAIL-marginal, ~1,000/yr; haircut 0.5, splits 2017-12, 2018-01, 2021-01; firm: FTMO intraday only
- 52. **PC C-6-05** CO-OC overnight→intraday reversal across commodity and rates futures (DKW futures ... — 11/21 (M2 E2 C0 F2 D2 X2 P1), low, orig no — closed: none (C-4-01 is the equity sibling); look-ahead: none; econ: 1-2 bp/day vs CL 3.8 / ZN 2.9 / ZC 11 bp RT FAILS (paper: futures 'much weaker'), VIX-change gate unmeasured; haircut 0.5, splits 2015-01, 2020-03; firm: IF
- 53. **SC C-8-01** Night–day asymmetry in non-US indices on CFD terms (long night with one swap / short day ... — 11/21 (M1 E2 C0 F2 D3 X2 P1), low, orig no [absorbs SC C-8-08] — closed: E1-08..10 (stock-CFD tug of war / overnight-only, single stocks) adjacent, index level new; look-ahead: none; econ: +2.4 bp/night vs swap -2.6 (EU) / -2.0 (JP) bp + 1.2-3 bp spread -> NET negative on EU, marginal JP; day-leg decomposition (C-8-08) fails unconditionally; haircut 0.5 (0.7 decomposition), splits 2016-07, ...
- 54. **pre-sweep P-C13** EU pre-open push (08:00-09:00 Berlin) as the direction filter for DAX/FTSE breakouts, ... — 11/21 (M1 E1 C2 F2 D3 X1 P1), low, orig no — closed: D4-04 (30-min ORB across CFDs incl. GER40) is the base; the pre-open-push direction filter is the new element (Krueger +0.199 R t 6.6 in-sample, 41,668 episodes); haircut 0.5; firm: FTMO GER40/UK100 intraday only (Eurex not at US futures firms)
- 55. **AF C-1-08** ES post-cash-close reversal 16:00–16:07 — 11/21 (M2 E1 C1 F2 D2 X2 P1), low, orig yes [absorbs pre-sweep A-C25] — closed: H0006/H0019 adjacent in time, opposite window/sign; look-ahead: 16:00:30 entry needs the 16:00 print, no auction feed needed; econ: 1-5 bp vs ES RT 1.2 bp (threshold 2.4) unknown, 80-120/yr; haircut 0.7, splits 2018, 2020-03, 2022-05; firm: IF until 16:07 ET (Topstep 16:10 ET margin 3 min; MFFU 16:10) + FTMO intraday
- 56. **AS C-4-04** Drift-burst fade after high-volume negative bursts, ES/NQ/CL/GC — 11/21 (M2 E1 C1 F3 D0 X3 P1), low, orig yes [absorbs pre-sweep A-C20] — closed: none (A-C20 un-gated sibling); look-ahead: burst detection on closed bars only, entry next bar; econ: 10-20 bp partial reversion vs ES 2.5 / GC 1.3 / CL 7.6 bp thresholds if a 1-min-late taker gets it; 150-200/yr; haircut 0.7, splits 2010-05-06, 2014-10-15; firm: IF/ONF/FTMO; data $40-80 for full-session 1m
- 57. **AS C-5-10** Soybean-crush opening reversal (GPM open vs prior close, filtered), ZS/ZM/ZL day trade — 11/21 (M1 E1 C1 F2 D2 X3 P1), low, orig no — closed: none; econ: floor-era 3.2 c/bu gross vs ~$72 RT per unit -> marginal at 2x; 34-68/yr; haircut 0.5 (electronic since 2006 removed the floor advantage); firm: IF three legs
- 58. **MS C-9-08** Volume-surprise persistence as the VWAP/TWAP order-splitting footprint → continuation — 11/21 (M2 E1 C1 F2 D2 X2 P1), low, orig yes — closed: H0021/H0022 (VWAP trend) adjacent but opposite construction; look-ahead: volume surprise vs time-of-day profile from prior days only; econ: 2-5 bp vs ES RT 1.2 bp (threshold 2.4) -> ~1-2x after haircut; 100-300/root/yr; haircut 0.7, splits 2019-05, 2020-09, 2022; firm: IF
- 59. **pre-sweep P-C08** Index-level volume shock -> overnight-session long (transfer of the single-stock effect), ... — 11/21 (M1 E1 C1 F3 D2 X2 P1), low, orig no — closed: H0012/H0017 (gap fade after the open) different; C-3-01 shows the unconditional overnight drift ~0 since 2017-2021; look-ahead: volume shock from RTH bars, entry 18:00; econ: index transfer untested, needs >= 2.5 bp/night vs MES threshold; haircut 0.5, splits 2017, 2021-01; firm: ONF 18:00->09:30 / FTMO (swap kills it)
- 60. **AS C-5-07** US close → European cash open fade, GER40/FRA40/EU50/UK100 — 11/21 (M2 E0 C1 F2 D3 X2 P1), low, orig yes — closed: H0012/H0017 logic transferred, D4 held-out markets; econ: CFD threshold 3-6 bp, magnitude unknown; ~80/yr; haircut 0.7, splits 2018-12, 2021-01; firm: FTMO intraday CFD only
- 61. **IG C-12-14** PBoC fix surprise → 6A/M6A 20:16–20:45 ET — 11/21 (M2 E0 C1 F3 D2 X2 P1), low, orig yes — closed: D4 (generic CFD rules), A-C05 (FX ITSM negative); look-ahead: expected fix model from CNH at 09:14 Beijing only; econ: 3-5 bp vs 6A RT 1.8 marginal; 80-120/yr; haircut 0.7, splits 2015-08-11, 2017-05, 2022; firm: ONF 6A/M6A / FTMO AUDUSD
- 62. **SC C-8-02** Halloween / Sell-in-May six-month long in non-US indices, swap-netted — 11/21 (M0 E2 C2 F2 D3 X2 P0), very low, orig no — closed: H0023 (S&P turn-of-month) calendar family, non-US Halloween untested; look-ahead: none; econ: +0.5-2% net per six-month hold after swaps, 6 trades/yr -> untestable at the gate; haircut 0.5, splits 2002, 2012; firm: FTMO Swing; 5% daily / 10% static at half exposure
- 63. **SC C-8-09** Closure premium through multi-day holidays (Golden Week, LNY, Easter) in JP225/HK50/GER40 — 11/21 (M1 E1 C2 F2 D3 X2 P0), very low, orig yes [absorbs SC C-8-03] — closed: H0023 / A-C29 calendar families, hold-through-closure untested; look-ahead: holiday calendar public; econ: +15-30 bp gross, net +5-20 bp per event, ~20 events/yr; haircut 0.7, splits 2020, 2022-09-23, 2024-11-05; firm: FTMO Swing (holds through closures allowed)
- 64. **AF C-2-04** WASDE minute-data update + limit-lock reopen — 11/21 (M2 E1 C1 F2 D2 X3 P0), very low, orig yes [absorbs pre-sweep A-C16] — closed: none; look-ahead: limit-lock state known at the close; econ: (a) ZC 12 bp RT FAILS, (b) 1-3% continuation passes but n 3-8/yr; haircut 0.5/0.7, splits 2012, 2018, 2020; firm: (b) ONF 20:00 reopen -> 13:15 CT
- 65. **AS C-4-02** ITSM into the COMEX gold settlement, last-10-minute execution, LSU gates — 10/21 (M1 E2 C1 F2 D2 X1 P1), low, orig no [absorbs AS C-4-03, pre-sweep A-C03] — closed: H0006/H0019 + D4-01 family (last-half-hour momentum) on a new asset; look-ahead: none; econ: ~2 bp vs GC threshold 1.3 bp marginal; ~120-250/yr; haircut 0.5, splits 2015-03, 2018, 2022-05; firm: IF/FTMO intraday
- 66. **AS C-4-05** Dealer-gamma session regime switch — 2026 evidence update to A-C23 — 10/21 (M2 E2 C0 F2 D2 X1 P1), low, orig no [absorbs pre-sweep A-C23] — closed: H0019 (GEX last half hour, failed) and A-C23; look-ahead: GEX/DIX published after the close -> use T-1 values only; econ: flow-unit effects, no return number, 2.5 bp threshold; haircut 0.5, splits 2016, 2022-05-11, 2024; firm: IF/FTMO
- 67. **IG C-12-07** CTA trigger-level crossing → last-hour continuation, 6 roots — TOP10 (5) — 10/21 (M2 E1 C1 F2 D1 X2 P1), low, orig yes — closed: H0006/H0019, D4-01 (unconditional) adjacent; look-ahead: trigger levels must be recomputed from prices to t-1 (bank levels are not archived); econ: 2-3 bp vs 1.2 bp RT -> fails 2x after haircut; 100-180/yr; haircut 0.5, splits 2008, 2020-03, 2022; firm: IF
- 68. **IG C-12-17** Large-gap continuation as margin-call liquidation, micro-gated (adjacent to closed ... — 10/21 (M2 E0 C3 F2 D2 X0 P1), low, orig yes — closed: H0012/H0017 (overnight-gap fade, closed, OOS net t -3.35) - this is the opposite sign of the same gap signal with a margin trigger: post-hoc sign-flip risk, the Pre-registration Officer must rule; econ: 30-50 bp continuation vs 1.2 bp RT; 10-30/yr; haircut 0.7, splits 2019-05, 2020-03; firm: IF/FTMO intraday
- 69. **IG C-12-11** NG/CL expiry-day final settlement window, hedged via the 2nd month — 10/21 (M2 E0 C2 F1 D1 X3 P1), low, orig yes — closed: none; look-ahead: expiry calendar public; econ: 15-50 bp NG / 10-30 bp CL vs 7/4 bp RT; 24 events/yr; haircut 0.7, splits 2008, 2020-04, 2022; firm: IF only via the 2nd month - prop firms force accounts out of the expiring contract (see C-12-31), so the front-month leg is not tradable
- 70. **IG C-12-13** Deribit 08:00 UTC expiry pin/release → MBT / BTCUSD — 10/21 (M2 E0 C2 F2 D2 X1 P1), low, orig yes — closed: D3-09 (BTC hour-of-day, closed) - expiry conditioning must be accepted as new; econ: 12-25 bp vs MBT ~2 bp RT passes, FTMO 23 bp fails; ~250/yr; Deribit's own null; haircut 0.7, splits 2021, 2024-01, 2025; firm: ONF MBT
- 71. **IG C-12-23** Failed 30-minute ORB fade (the ORB crowd's stops), paired with C-11-01 — 10/21 (M1 E0 C2 F3 D2 X1 P1), low, orig yes — closed: H0020 (5-min ORB) and prereg_orb30 (same range, opposite trade); look-ahead: range fixed at 10:00; econ: R-based, cost < 0.1R; 60-100/yr/root; haircut 0.7, splits 2019, 2022-05; firm: IF/FTMO intraday; must share prereg_orb30's sample split
- 72. **AF C-1-06** Commodity LETF settlement-time rebalancing NG/CL/GC/SI — 10/21 (M2 E0 C1 F3 D1 X2 P1), low, orig yes [absorbs pre-sweep A-C24] — closed: H0006/H0019 adjacent (ES/NQ only); look-ahead: day move measured at T-30 min only; econ: unknown, needs >=15-20 bp on
- 73. **IG C-12-03** Prop daily-loss / trailing-DD stop-out cascade, micro-share trigger — TOP10 (2) — 10/21 (M3 E0 C1 F2 D1 X2 P1), low, orig yes — closed: none (C-4-04 drift-burst fade is the price-only sibling); look-ahead: micro share from closed bars; econ: 1-2 pt half-reversion vs 0.6 pt RT -> ~1x of the 2x threshold after 0.7 haircut; 100-250/yr/root; splits 2019-05, 2022-05, 2024; firm: all intraday futures; shares the micro-footprint prerequisite
- 74. **IG C-9-10** Micro-vs-mini BVC divergence as a 15-minute reversal signal — 10/21 (M2 E0 C1 F2 D1 X3 P1), low, orig yes — closed: none; look-ahead: BVC per contract from closed bars; econ: 2-4 tick reversion vs 2.4 tick RT -> needs win rate > 58%; 300-800/yr/root; haircut 0.7, splits 2019-05, 2022; firm: IF
- 75. **MS C-9-06** Close-location flow (CLV × volume) vs BVC head-to-head — 10/21 (M1 E0 C0 F2 D3 X3 P1), low, orig yes — closed: none; econ as C-9-01 (5.6 ticks needed), extreme cost sensitivity; haircut 0.7; firm: IF; mainly a proxy-comparison arm
- 76. **PC C-8-01** Carver trend + carry with vol-regime multiplier as an FTMO Swing sleeve, swap-filtered ... — 10/21 (M1 E2 C2 F2 D3 X0 P0), very low, orig no [absorbs SC C-8-07, IG C-11-05] — closed: D2-01/D2-09 (CFD trend+carry, OOS 0.16) and H0007; no new mechanism, new elements are the vol multiplier, swap netting and an FTMO-shaped DD guard (lane-11 open direction) -> registrable only as an overlay test on D2; look-ahead: daily closes, settlement-time alignment across time zones (Quantitativo retraction); econ: ...
- 77. **AF C-1-12** Daily 4pm Treasury strike window ZN — 10/21 (M2 E1 C0 F2 D2 X3 P0), very low, orig no [absorbs pre-sweep A-C13] — closed: none; look-ahead: ETF flow sign at T-1; econ: <=1 bp vs ZN RT 3 bp FAILS; haircut 0.7, split 2021-01-14; firm: IF
- 78. **AF C-1-11** FX option NY-cut strike gravitation 6E/6J — 10/21 (M2 E0 C1 F3 D1 X3 P0), very low, orig yes — closed: none; look-ahead: strike notional lists must be archived as of 09:00 ET (no free history found); econ: 3-8 bp vs 6E RT 1.2 on paper, no study; haircut 0.7, splits 2019, 2022; firm: IF 6E/6J + FTMO intraday
- 79. **SC C-8-12** Tokyo's new 15:30 JST closing auction → JP225 reversal at the 16:30 evening reopen ... — 10/21 (M2 E0 C1 F3 D2 X2 P0), very low, orig yes — closed: none; econ: 2-5 bp vs 1-2 bp RT marginal; forward-only (auction since 2024-11-05), n ~100 only by late 2026 -> cannot pass the 8-year gate before ~2032; haircut 0.7; firm: FTMO intraday / NKD ONF
- 80. **AS C-4-08** ITSM into settlement in NG/SI/PL/HO (CL excluded by evidence), gated on LETF hedging ... — 9/21 (M2 E2 C0 F2 D1 X1 P1), low, orig yes — closed: H0006/H0019 family on new asset classes; econ: NG 5-6 bp vs threshold 16 bp FAILS 3x unconditional, gate lift unmeasured; ~300/yr; haircut 0.5, splits 2011-10, 2020-04; firm: IF
- 81. **PC C-7-05** Overnight-session range percentile at 09:29 as the breakout/fade/inactive regime — 9/21 (M1 E1 C1 F2 D2 X1 P1), low, orig yes [absorbs pre-sweep P-C11] — closed: H0020/D4-04 (ORB) and H0013/14 (fade) as the bases; regime variable new; look-ahead: overnight range known at 09:29; econ: gate must double a 2-10 bp family mean; Krueger holdout flat; haircut 0.7, splits 2010-06, 2020-03, 2022-05; firm: IF/FTMO intraday
- 82. **IG C-12-19** Dealer charm flow midday drift, GEX-gated (folklore kill-test) — 9/21 (M1 E0 C2 F2 D2 X1 P1), low, orig no — closed: H0019 (GEX last half hour) adjacent window; look-ahead: GEX at T-1 only; econ: 3-5 bp over 4.5 h vs 1.2 bp RT if real; 80-120/yr; folklore, indistinguishable from 'long quiet up-days'; haircut 0.5, splits 2022-05, 2024; firm: IF
- 83. **IG C-12-21** Opening 09:30–09:35 retail thrust fade, top-tercile micro share, with control arm — TOP10 ... — 9/21 (M2 E0 C2 F2 D1 X1 P1), low, orig yes — closed: H0020 (5-min ORB, opposite trade) and H0012/H0017 (09:31 fade) adjacent; look-ahead: micro share of 09:30-09:35 known at 09:35; econ: ~10 bp reversion vs 1.2 bp RT; 80-120/yr/root; haircut 0.7, splits 2019-05, 2022-05, 2024; firm: all intraday futures; micro-footprint prerequisite
- 84. **IG C-12-22** Prop news-ban cohort re-entry at 08:33 ET in GC/6E/CL/ZN, traded from exempt firms — ... — 9/21 (M2 E0 C2 F1 D2 X1 P1), low, orig yes — closed: E2 (release-direction trades) adjacent; this times the prop cohort re-entry; look-ahead: release calendar public; econ: 3-10 bp vs GC 1 bp / 6E 1.2 bp RT; 200-300/yr; haircut 0.7, splits 2023, 2025; firm: only at news-exempt firms (FTMO Swing, Topstep, Bulenox) - by construction it trades inside the window MFFU/Lucid ban
- 85. **IG C-12-01** Topstep 16:08 / MFFU 16:10 forced flatten, traded from a later-deadline account — TOP10 ... — 9/21 (M3 E0 C1 F1 D1 X2 P1), low, orig yes [absorbs IG C-12-02] — closed: H0006/H0019 (15:30-16:00 momentum) adjacent - this trades the 16:00-16:15 forced-flatten reversal; look-ahead: firm deadlines fixed in advance; econ: 0.75-1.5 pt half-reversion vs ES 2x RT 1.2 pt borderline, top-tercile micro-share days only, ~80-150/yr; haircut 0.7, splits 2023-03, 2024, 2026-02; firm: only from ...
- 86. **MS C-9-09** Settlement-window flow proxy → post-settlement reversal (ES/NQ, ZN, 6E, GC, CL, ZC) — 9/21 (M2 E0 C1 F2 D1 X2 P1), low, orig yes [absorbs IG C-12-32] — closed: H0006/H0019 (cash-close momentum) adjacent, this is post-settlement reversal in futures; look-ahead: settlement bar must be closed before entry; econ: needs 5.6 ES ticks / 9 bp CL, top decile only, 50-80/root/yr; haircut 0.7, splits 2015-03, 2020-09 (ES window 15:15->15:00 CT), 2026-01-12 (gold procedure); firm: IF (ES ...
- 87. **IG C-11-06** US-only index mean reversion (G2-06 rules frozen), evaluated only on post-registration ... — 9/21 (M1 E1 C2 F2 D3 X0 P0), very low, orig no — closed: G2-06 (inside the closed family; sanctioned post-hoc US slice); evaluation only on data after 2026-11 -> cannot reach Gate v2 before the deadline; haircut 0.5; firm: FTMO Swing
- 88. **SC C-13-10** FOMC-minutes / Beige-Book tone divergence → multi-day ZN/UB drift as overnight-session ... — 9/21 (M1 E1 C1 F2 D2 X2 P0), very low, orig no — closed: E2 (statement, ES/NQ) and C-2-10 adjacent; look-ahead: minutes text at 14:00 ET, entry 18:00; econ: 4-8 ticks if 10-20% continues vs ~1.3 tick RT, honest prior zero; 16/yr; haircut 0.5, splits 2004-12, 2019; firm: ONF (MFFU/Lucid ban the 14:00 minutes window only)
- 89. **AS C-5-02** CL → 6C petro-currency causality at 5–60 min — 9/21 (M2 E1 C0 F3 D2 X1 P0), very low, orig no — closed: negative rows FX intraday momentum / 1-min lead-lag (this one has a mechanism); econ: <1 bp lagged vs 6C threshold 3 bp FAIL; haircut 0.5, splits 2009, 2014-11, 2020-04; firm: IF + FTMO
- 90. **AF C-2-08** GC/SI option-expiry settlement pinning — 9/21 (M1 E0 C1 F2 D2 X3 P0), very low, orig yes — closed: none (A-C26 analogue); econ: <=5 bp, n 24/yr FAILS on count; haircut 0.7, split 2022; firm: IF
- 91. **SC C-13-09** MoF weekly securities flows → next-week USDJPY / JP225 drift — 9/21 (M1 E0 C1 F2 D3 X2 P0), very low, orig yes — closed: D2 (not flow-based); look-ahead: Thursday 08:50 JST release; econ: short-USDJPY swap -5.8 bp/5 days; 15-25/yr; haircut 0.7; firm: FTMO Swing / ONF 6J
- 92. **IG C-11-04** Bond trend sleeve as a US-day-session hold in ZN/ZB (08:20 → 15:00) with overnight control — 8/21 (M1 E1 C0 F2 D2 X1 P1), low, orig yes — closed: H0007 (multi-day trend as the goal), D2-07; econ: 0.7-1.1 bp/day vs ZN RT 3 bp FAILS 3x; ~250/yr; haircut 0.5, splits 2008, 2022; firm: IF 08:20-15:00
- 93. **MS C-9-01** BVC minute imbalance → 5-minute reversal/continuation, calibrated vs aggressor flags ... — 8/21 (M1 E1 C0 F2 D1 X2 P1), low, orig no [absorbs pre-sweep A-C38] — closed: none (A-C38 feature); look-ahead: next-bar entry; econ: needs ~5.6 ES ticks per 5-min trade at 2 sigma FAILS on priors; 300-600/root/yr; haircut 0.5, splits 2019-05, 2020-09, 2022; firm: IF
- 94. **AS C-5-08** ZN shock → gold follow-through at 5–30 min — 8/21 (M1 E0 C1 F2 D2 X1 P1), low, orig yes — closed: negative row 1-min lead-lag (mechanism named); econ: GC threshold 1.3 bp, lagged share unmeasured; haircut 0.7, splits 2022-03, 2024; firm: IF/FTMO
- 95. **AF C-2-10** Post-FOMC drift ZN via overnight-session holds — 8/21 (M1 E1 C0 F2 D2 X2 P0), very low, orig yes [absorbs pre-sweep A-C11] — closed: E2-01..04 adjacent; econ: ~2 bp/day vs ZN RT 3 bp FAILS; 60-100/yr; haircut 0.5, splits 2008, 2015, 2022; firm: ONF
- 96. **AS C-5-06** NKD ↔ ES minute lead–lag across time zones (trading-place bias) — 8/21 (M1 E1 C0 F3 D2 X1 P0), very low, orig no — closed: negative row 1-min lead-lag (documented mechanism, documented sub-cost ratio 0.58); econ FAIL; haircut 0.5
- 97. **IG C-12-09** Single-stock LETF (NVDL/TSLL) → NQ close on big NVDA/TSLA days — 8/21 (M2 E1 C0 F2 D2 X1 P0), very low, orig no — closed: H0006/H0019 window overlap, A-C24; econ: ~1 bp in NQ FAILS (dilution); 4-year sample cannot meet the 8-year rule; haircut 0.5; firm: IF
- 98. **AF C-1-07** Treasury LETF close rebalancing ZB/UB — 8/21 (M2 E0 C1 F2 D1 X2 P0), very low, orig yes — closed: H0006/H0019 adjacent; look-ahead: TLT move at 15:40; econ: needs >=12 bp vs UB RT 5-6 bp, untested, 25-50/yr; haircut 0.7, splits 2020-03, 2022-23; firm: IF (16:00 exit inside Topstep 16:10 ET)
- 99. **IG C-12-29** Treasury buyback operations 13:40–14:00 ET → ZN/ZB/UB — 8/21 (M2 E0 C0 F2 D1 X3 P0), very low, orig yes — closed: none; econ: 2-5 bp vs ZN RT 3 bp FAILS, UB marginal; programme since 2024-05 (2.5 years) fails the 8-year rule until ~2032; haircut 0.7, split 2026-09; firm: IF
- 100. **PC C-6-01** Intraday TSMOM breadth across ~20 CME futures, 30-min cadence, post-2020 futures only — 7/21 (M1 E1 C1 F2 D1 X0 P1), low, orig no — closed: D4-03 (30-min TWAP trend on 19 CFDs, net t <= -4.6), H0022, H0005/H0011 - same rule family; survives only as new markets (rates/grains/metals futures) and untouched dates 2020-06..2026; look-ahead: none; econ: 2-6 bp on ES/NQ vs 1.2-22 bp thresholds, grains/energies fail; 5,000+ changes/yr; Carver speed limit binding; ...
- 101. **MS C-5-15** Cross-asset BVC flow divergence ES → NQ/RTY/YM — 7/21 (M1 E0 C1 F2 D1 X1 P1), low, orig yes — closed: negative row 1-min lead-lag (names a flow mechanism); econ: needs 2.3 bp in RTY, unknown; haircut 0.7, splits 2019-05, 2020-09, 2022; firm: IF
- 102. **PC C-6-04** Cross-root signed-volume (BVC) class breadth as a gate on each root's intraday trend ... — 7/21 (M1 E0 C1 F2 D1 X1 P1), low, orig yes — closed: D4-02 / H0005 family as the base, BVC breadth gate new; look-ahead: gate from pre-entry bars only (Krueger volume-gate artefact); econ: needs 2-6 bp, grains fail; haircut 0.7; firm: IF
- 103. **PC C-9-01** First-30-min BVC signed volume → open-to-close sign across non-equity futures — 7/21 (M1 E0 C1 F2 D1 X1 P1), low, orig yes — closed: D4-02 (first-30-min move -> rest of day) adjacent, BVC input new; look-ahead: BVC uses the bar's own close -> entry next bar; econ: needs 1.2-22 bp per 5-h hold, R2 >= 1-2% required; ~1,100/yr; haircut 0.7, splits 2019-05, 2020-03; firm: IF
- 104. **PC C-9-05** Hawkes-decayed BVC imbalance momentum as the intraday trend signal — 7/21 (M1 E0 C1 F2 D1 X1 P1), low, orig yes — closed: H0021/H0022, D4-03 (price trend) - flow input new; econ as C-6-01, energies/grains fail; haircut 0.7; firm: IF
- 105. **AS C-5-04** ZN shock → ES follow-through outside events, stock–bond-correlation regime — 7/21 (M1 E0 C0 F3 D1 X1 P1), low, orig yes — closed: E2 (events excluded) + negative row 1-min lead-lag; econ: lagged share below 2.5 bp likely FAIL; haircut 0.7, splits 2020-03, 2022-01; firm: IF/FTMO
- 106. **AS C-5-01** VX-futures → ES lead in high-vol states, signal only — 7/21 (M2 E2 C0 F2 D0 X1 P0), very low, orig no — closed: G1 (no VX product); econ: authors report no profit net of costs FAIL; firm: signal only; data: VX 1m outside the plan
- 107. **MS C-10-05** Image-based CNN on intraday bar charts (Jiang–Kelly–Xiu transfer) — 7/21 (M0 E1 C0 F2 D3 X1 P0), very low, orig no — closed: H0001-H0004 (pattern recognition) adjacent, negative row DL at retail latency; econ: 5.6 ticks per 30-min trade needed; haircut 0.5; firm: IF
- 108. **IG C-12-31** Prop-firm forced roll days: micro front/back spread push — 7/21 (M2 E0 C0 F1 D1 X3 P0), very low, orig yes — closed: none; econ: 1-3 tick spread push vs 2-tick RT FAILS; spreads not supported at most firms; haircut 0.7
- 109. **MS C-9-07** Wick-asymmetry absorption proxy → reversal against the wick — 7/21 (M1 E0 C0 F1 D3 X2 P0), very low, orig yes — closed: H0013/14 (daily IBS) different scale; econ: typical wick < 2 RT, only news minutes are large and firms ban them; haircut 0.7; firm: IF (news clauses bind)
- 110. **IG C-12-28** 0DTE put-wall first touch (forward-collected CBOE OI; not backtestable) — 6/21 (M1 E0 C2 F2 D0 X1 P0), very low, orig no — closed: H0019, A-C26 adjacent; data: CBOE OI history paid -> forward-collected only, untestable before ~2028; econ: 5-15 bp folklore
- 111. **AF C-2-06** Livestock reports → LE/HE Monday open — 6/21 (M1 E0 C0 F1 D1 X3 P0), very low, orig yes — closed: none; look-ahead: none; econ: limit-locked opens kill fills, likely FAIL; 16-20/yr; haircut 0.7; firm: IF (LE/HE availability at firms to verify)
- 112. **MS C-10-02** Pre-registered bar-feature gradient boosting with CPCV, PBO, deflated Sharpe (MNQ base ... — 5/21 (M0 E1 C0 F2 D1 X1 P0), very low, orig no — closed: negative row order-book DL / H0003 (100 hypotheses, 0 survive); econ: MNQ base rate 0.07-1.5 pt vs 2-pt floor FAILS before ML; derivative on NQ 2021-2025; haircut 0.5; firm: IF
- 113. **IG C-12-25** First Notice Day liquidation of non-deliverable longs, GC/SI/CL settlement window ... — 5/21 (M2 E0 C1 F1 D0 X1 P0), very low, orig yes — closed: A-C17 / Goldman-roll negative evidence (different population); econ: 5-10 bp GC marginal, CL fails; ~46/yr; haircut 0.5; firm: front month near FND restricted at prop firms; data $42
- 114. **IG C-12-30** Retail bar-close clock: 15-minute-boundary micro bursts faded (entry-timing overlay) — 5/21 (M1 E0 C0 F2 D1 X1 P0), very low, orig yes — closed: H0021/H0022, H0005/H0011 adjacent; econ: half-tick reversion vs 2.4-tick RT FAILS unless passive; haircut 0.7; firm: IF

## E. Declined appendix

### Scout blocks declined at merge

| id | name | reason |
|---|---|---|
| AF C-1-10 | ES expiration pinning: negative update / amplification kill-test | negative evidence: Elms (2026) finds no pinning in ES/SPX 2016-2025; the amplification variant is inside H0006/H0019 (last-half-hour momentum incl. GEX); A-C26 downgraded. Keep only as a documentation note. |
| SC C-8-04 | Gold autumn seasonality (Baur) - negative update | negative evidence: the 2024 replication (Potrykus-Augustynowicz) reverses the sign; seasonal-window family (P-C29, A-C19) without a mechanism; scout itself says do not register. |
| MS C-5-11 | ES <-> NQ one-minute lead-lag, 2016-2026 code-backed null | negative-evidence row "1-minute lead-lag without a mechanism" (common brief); gross 0.03-0.4 bp vs 1.2 bp RT (0.2-0.6x of cost, two independent code bases); A-C22/P-C22 confirmed dead. |
| SC C-13-07 | Extreme cold-forecast NG risk premium (NG1-NG2 spread) | no firm structure: the only post-cost Sharpe > 1 in lane 13 (1990-2019) is a multi-day calendar-spread hold that no futures prop firm allows across the close and FTMO cannot express; the outright intraday adaptation is untested and has no mechanism of its own. Re-open only if a firm offers spreads across the close. |

### Pre-sweep entries not carried (closed family, negative evidence, no firm fit)

| pre-sweep id | name | reason |
|---|---|---|
| P-C01 | Hybrid overnight carry of intraday index trend | base model = closed H0005/H0011 (noise-area / Beat the Market); the overnight-exit variant is a holding change on a closed base; futures firms cannot hold across the close. |
| P-C03 | BTC intraday trend inside the Monday-Asia-open window | D3 (crypto TSMOM / intraday trend D3-04 / hour-of-day D3-09) closed; a window restriction of a closed trend ensemble is not a new mechanism. |
| P-C04 | Relative-volume-gated ORB on futures | H0020 (5-min ORB) closed; a gate on a closed base; Krueger NET +0.002 R (NQ), negative elsewhere. |
| P-C05 | Short-term basis reversal in commodity calendar spreads | no firm structure (weekly spread holds; personal account only), not a closed family; the strongest code-backed number in the pre-sweep (Sharpe 1.45 net) but untradeable under the client rules. |
| P-C06 | Kalman-filter trend percentile on NQ 1-min | H0021/H0022 (intraday trend NQ) closed; indicator change only. |
| P-C07 / P-C27 / P-C26 / P-C25 | Turnaround Tuesday, Connors VIX-stretch, Clenow counter-trend, Carver fast MR on index futures | G2-01..07 (buy-the-dip on index CFDs) closed; commodity legs carried in SC:C-8-06; US-only slice carried as IG:C-11-06. |
| P-C14 / A-C40 / A-C12 | Pre-FOMC / pre-announcement drift | E2-05 closed; negative-evidence row pre-announcement drift post-2014 (Kurov-Wolfe-Gilbert 2021). |
| P-C15 | Intraday Alpha Atlas 30-min fades across 29 markets | D4 (intraday rules across 19 CFDs) closed; best 1.5 bp/trade sub-cost. |
| P-C18 / A-C29 / A-C31 | OPEX week, pre-holiday, day-of-week, crypto weekday | negative-evidence rows (common brief). |
| P-C21 | EUR/USD European-session depreciation (Breedon-Ranaldo) | practitioner NEGATIVE record; the broader around-the-clock version is kept as PS:A-C08 at very low plausibility. |
| P-C23 | NQ 5-min indicator-slope trend (forum, unverified) | H0021/H0022 adjacent, no verified rules or curve. |
| P-C28 | Crabel NR7 / Larry Williams Oops | ORB (H0020, D4-04) and gap (H0012/H0017) families closed; "likely decayed" per pre-sweep. |
| P-C29 / A-C19 | Seasonality windows (Seasonax, election drift, energy seasonal tilts) | multiple testing without a mechanism; non-US Halloween kept as SC:C-8-02 because it has peer-reviewed OOS panels. |
| P-C30 | Davey walk-forward process | a process reference, not a mechanism. |
| P-C17 | Weekly reversal in futures conditioned on volume and OI | no firm structure for weekly futures holds; profits vanish at 0.16% one-way cost (1983-2000); the KRT position-change version is kept as SC:C-13-04. |
| A-C02 | Treasury-futures intraday momentum into the 15:00 settlement | fails the economics screen (AS declined item 7: ~1-2 bp vs 6 bp threshold). |
| A-C01 / A-C04 | Non-US index intraday momentum (first half hour -> last half hour) and overnight-return -> last-half-hour continuation (Liu-Tse) | D4-01 (last half hour on 19 CFDs incl. GER40/JP225) and H0006/H0019 closed; AS declined item 1. |
| A-C05 | FX-futures intraday momentum 6E/6B/6J | negative-evidence row (common brief). |
| A-C17 | Goldman-roll front-running | negative-evidence row post-2004 (AF declined list adds Yan-Irwin-Sanders 2022, Bessembinder et al. 2016). |
| A-C22 | 1-5 minute cross-market lead-lag | negative-evidence row; MS:C-5-11 numbers. |
| A-C28 | FOMC-cycle even-week ES bias | E2 family adjacent; no new evidence found by any scout; calendar-only. |
| A-C34 / A-C35 / A-C36 | Deep momentum networks intraday, order-book deep learning, sparse LASSO 1-min cross-section | negative-evidence row (order-book DL at retail latency); A-C34/A-C36 low with no new evidence; lane 10 is carried by MS:C-10-02/C-10-05 and the layer rows. |

Pre-sweep entries attached to a scout row (not declined; listed in the merge log): A-C03, A-C06, A-C07, A-C09, A-C10, A-C11, A-C13, A-C14, A-C15, A-C16, A-C18, A-C20, A-C23, A-C24, A-C25, A-C26 (via C-1-10 decline), A-C27, A-C30, A-C38 (MS:C-9-01), P-C02 (layer), P-C09, P-C11, P-C12, P-C16, P-C19, P-C20, P-C22, P-C24.

### Closed families confirmed as the reason for scout-level declines (for the Pre-registration Officer)

H0001–H0004/H0010/H0016 (bot SMC/TJR, incl. the hypotheses.py Z01–Z03 re-runs and the ICT kill-zone inverse); H0005/H0011 (noise-area momentum); H0006/H0019 (last half hour incl. QuantRocket VIX gate, QuantConnect ITSM −0.63, LETF/GEX sizing in ES/NQ); H0012/H0017 (overnight-gap fade and ES/NQ overnight→intraday reversal); H0013/H0014 (IBS; honest-backtest session MR OOS negative); H0020 (Kintoun regime-filtered ORB, quantalgo ORB); H0021/H0022 (VWAP trend, volume-bar re-runs); E2-01..12 (FX macro-reaction 6E/6B, pre-FOMC Swing version); D2 (FX swap carry — FTMO table shows both sides negative on most majors); D3 (crypto funding carry per 8h, weekend effect, freqtrade); D4-01 (first-half-hour→last-half-hour on DAX/FTSE/Nikkei/HSI/ASX CFDs); E1 (single-stock EOD reversal, statistical arbitrage); G2 (index RSI(2)/3-down, Krueger holdout "small in risk units"); F1 (meta-labelling the near-miss stack); H0007 (Quantitativo network momentum, lookahead retraction 2.10 → 0.97). Negative-evidence rows: Goldman roll post-2004, pre-announcement drift post-2014, BoJ ETF afternoon rebound (programme ended 2024-03-19), dividend-adjustment calendar (zero-sum by construction), triple-swap Wednesday (negative before price risk).

