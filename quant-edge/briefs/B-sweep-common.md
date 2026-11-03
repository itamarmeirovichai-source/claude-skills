# Brief: Department B sweep (Market Intelligence) — common instructions for every scout and analyst

Goal of the run: a ranked list of ≥ 100 candidate mechanisms in `quant-edge/research/candidates.md`, ≥ 30% of them original
(not found in the literature sweep), each with a one-paragraph brief in the format below. Search wide; the gate is merciless later.
Expect most candidates to rate "low"; say so. The two pre-sweeps already exist and must be EXTENDED, not repeated:
`~/quant-edge-inherited/pr26/prompts/research/lit-academic.md` (36 candidates) and `lit-practitioner.md` (30 candidates, 19 cost facts).
Read them first (grep by lane keywords if long) and do not re-list their entries except to add new evidence or a new twist; cite them as "pre-sweep A-xx / P-xx".

## Candidate format (one block per candidate; ids C-<lane>-<nn>, lane 1–13 per the lanes list below)

### C-<lane>-<nn> <short name>
- mechanism: who is forced to trade predictably, when, and why the effect should survive publication and our costs
- evidence: peer-reviewed | working paper | blog with code | forum | own idea — citation (authors, year, URL, fetch date); the post-2015 out-of-sample number if any
- evidence window: the markets × dates the cited evidence displays (e.g. "ES 2010-2024"); a registered OOS overlapping it makes the row "derivative", decided on untouched markets or dates
- instruments: exact roots / CFD symbols
- holding period and expected trades per year
- data needed: dataset, resolution, years; cost inside the Databento plan ($0 if free; the plan ceiling is $94 total; 1m RTH ≈ $6–7 per root, 1h ≈ $1, 1d ≈ $0.05)
- expected gross edge per trade (ticks or bp) and cost sensitivity at the common-brief floors (ticks per round trip); pass/fail of the economics screen
- firm structure fit: intraday futures (flat by deadline) | overnight-session futures (after 18:00 ET, flat before the deadline) | FTMO Swing across the close | FTMO intraday CFD; clauses touched (news windows, inactivity, minimum hold, consistency)
- nearest closed relative: inherited id(s) from the common brief, or "none"
- decay haircut: 0.5 published, 0.7 original, never above 0.8; the institutional change date(s) that split the sample
- plausibility of net Sharpe ≥ 1.5: low | medium | high — one sentence of reasoning
- original: yes | no

## Lanes (from the master prompt; cover every lane assigned to you)
1 structural flows with a calendar (leveraged-ETF rebalancing in the last 30 min in ES/NQ/RTY; closing-auction imbalances; month/quarter-end index-extension flows in ZN/ZB at the 4pm strike; Treasury auction cycle in ZN/ZB/ZF; WMR 4pm London fix and month-end in 6E/6B/6A/6J; Tokyo 9:55 fix on gotobi days; index-rebalance eves; 0DTE-era option pinning; commodity index roll windows in CL/GC/ZC)
2 scheduled information outside ES/NQ (EIA Wed 10:30 ET in CL/NG/RB/HO; USDA WASDE 12:00 ET in ZC/ZS/ZW; London gold/silver auctions in GC/SI; COMEX settlement windows; FOMC/Treasury in ZN/ZB only)
3 the overnight session at futures firms (02:00–03:00 ET European-open drift in ES; 18:00→09:30 holds in MES/MNQ; session-open effects)
4 intraday momentum and reversal in untested markets (first-half-hour→last-half-hour in GC, CL, ZN, 6E, DAX, FTSE, Nikkei, HSI; momentum into settlement; overnight→intraday reversal; Nagel-type liquidity provision after large minute moves; late-session breakouts; dealer-gamma regime switching across the session)
5 cross-market lead-lag at minute horizons with a mechanism (ES↔NQ↔RTY↔YM, bonds→equities, CL→6C, VIX→ES, US close→Asia open; stat-arb triplets; ETF↔futures basis)
6 breadth and portfolio construction (many weak uncorrelated intraday sleeves across 20+ futures; intraday TSMOM across the universe flat by day end; vol-managed overlays; fast mean-reversion execution overlay as a layer)
7 regime-conditional (VIX/realized-vol terciles, 5-day range vs 250-day, FOMC and roll weeks; breakouts in high vol, fades in low vol; inactivity rules stated)
8 FTMO Swing across the close (multi-day trend with a hard drawdown overlay; curve carry; multi-day dip buys in commodities and non-US indices; OPEX-week and pre-holiday biases; seasonal/overnight premia in non-US indices and commodities; funding carry per 8h on CFD terms)
9 order-flow proxies from bars (tick-rule imbalance, dollar-volume bars, BVC, volume clocks; 1s pilot only after a 1m proxy shows gross t > 3)
10 ML done right (pre-registered features and labels, purged k-fold with embargo in sample, meta-labelling on an existing sleeve)
11 the previous org's own open directions (S&P 30-min ORB prereg_orb30; futures-curve carry and value; bond sleeve; trend with hard-DD overlay; US-only index mean reversion post-2026)
12 the market's adversary (who must trade at predictable times or directions: passive funds, leveraged funds, option dealers, VWAP/TWAP algos, index rebalancers, commodity index rollers, central-bank fixings, margin liquidations, prop traders flattening before their own deadlines; which firm rules let a bot be on the other side; register the ten best)
13 text and alternative data, free only (FOMC statement diffs, EIA/USDA text, CFTC extremes, Google Trends, GDELT with the measured lag)

## Rules
- Code-backed and page-backed claims only; every citation with URL and fetch date. SSRN is blocked (403): use arXiv, journal pages, NBER, author pages, Google Scholar snippets, Semantic Scholar; say "abstract only" when that is all you saw.
- Grep `quant-edge/registry.csv` for near relatives (ids and hypothesis text) before calling anything new.
- Write your output file at the start and append candidate blocks as you find them; finish with a summary table (id | name | lane | evidence grade | plausibility | original).
- Honest about retail latency (home PC in Israel through Rithmic/Tradovate/MT5; 1-minute bars; no co-location).
- No purchases, sign-ups, firm contact. Report blocked hosts in the summary. English only.
