# Department B sweep — Idea Generator: lanes 12 (the market's adversary), 11 (the previous org's open directions) + original mechanisms across any lane

- scout: Idea Generator (Department B, Market Intelligence)
- date: 2026-11-04 (citation fetch date for every URL below: 2026-11-03 unless stated; searches run 2026-11-04)
- lanes: 12 (who must trade at predictable times or directions; when the footprint appears in minute bars; which firm rules let a bot be on the other side; the ten best are marked "LANE-12 TOP TEN" in the summary), 11 (prereg_orb30, futures-curve carry and value, bond sleeve, trend with hard-DD overlay, US-only mean reversion post-2026, hypotheses.py Z01–Z05), and original mechanisms in any lane
- method: first principles first (list the forced traders, derive the clock time and the direction, derive the firm clause that lets a bot be on the other side), then the web only to check whether the idea is already published (then it is not original) and to size the flow. Inherited sources read: `~/quant-edge-inherited/pr4/skills/prop-fleet/agents/daily/2026-10-06-0247/builder/prereg_orb30.txt`, `~/quant-edge-inherited/pr4/skills/prop-fleet/scripts/hypotheses.py` (Z01–Z05), `~/quant-edge-inherited/pr26/prompts/research/firms-2026-10-11.md`, the two pre-sweeps (A-xx, P-xx), the four sibling sweep files already in this directory (C-1-xx … C-10-xx; cited where a lane-12 idea would otherwise duplicate them).
- status: written incrementally; blocks appended as found. Summary table and blocked-host list at the end.
- honesty note: almost every block below is plausibility "low" for net Sharpe ≥ 1.5 on a single sleeve. They are pre-registration material and breadth, not edges. Nothing here has been tested; nothing is "promising".

## Cost conventions used below
Approximate Nov-2026 price levels, 1 tick + commission per side, market orders: ES RT ≈ 1.2 bp (0.6 pt); MES RT ≈ 0.5 pt + $1.60 ≈ 1.3 bp; NQ RT ≈ 0.5 pt + $5 ≈ 0.4 bp + tick-dominated; ZN RT ≈ 3 bp; ZB/UB RT ≈ 5–6 bp; 6E RT ≈ 1.2 bp; 6A RT ≈ 1.8 bp; CL RT ≈ 4 bp; NG RT ≈ 7 bp; GC RT ≈ 0.6–1 bp; SI RT ≈ 2 bp; MBT (0.1 BTC, tick $5 = 0.5 pt) RT ≈ 1.5–2 bp + $2; CFDs per the common brief; Binance perps 7 bp/side + funding. Economics screen = gross edge per trade ≥ max(2 ticks, 2 × RT) unless hundreds of trades/yr with win rate > 58%. Databento prices from the common brief (1m RTH ≈ $6–7/root, full session ≈ $20/root, 1h ≈ $1, 1d ≈ $0.05; ceiling $94; no paid call allowed until the Databento credit is confirmed — D-005).

## The adversary list (first principles, before any search)
Who must trade at a known time or in a known direction, and where the footprint should sit in 1-minute bars:

| forced trader | when (ET) | direction known from | footprint instrument | already covered by | lane-12 block here |
|---|---|---|---|---|---|
| Daily-reset leveraged ETFs (equity) | 15:30–16:00 | day's sign × AUM × L(L−1) | ES/NQ/RTY | A-C24, H0006/H0019 (closed window) | C-12-09 (single-stock LETF twist only) |
| Daily-reset leveraged ETFs (commodity, Treasury) | 13:25–14:30; 15:40–16:00 | same | NG/CL/GC/SI; ZB/UB | C-1-06, C-1-07 | none (covered) |
| VIX ETPs (UVXY/SVXY/SVIX) | 15:45–16:15 | VIX day move × AUM × leverage | VX (no firm) → ES hedge leg | none | C-12-08 |
| Vol-control / risk-parity funds | 15:00–16:00 for 1–3 days after a vol jump | realized-vol change | ES/NQ, ZN | none at minute level | C-12-06 |
| CTA trend models | last hour on days a popular signal level is crossed | sign of the cross | ES/NQ/CL/GC/ZN/6E | none at minute level | C-12-07 |
| Option dealers (0DTE gamma/charm) | all day; 15:30–16:00 | GEX sign, put/call OI | ES | A-C23/C-4-05 (regime), A-C26/C-1-10 (pinning), H0019 | C-12-19 (charm, not original), C-12-28 |
| Defined-outcome / collar funds | last 30 min of month/quarter ends | published strikes | ES | none | C-12-16 |
| VWAP/TWAP parent orders | until the round clock mark | flow sign | ES/NQ/ZN/CL/GC | C-9-08 | none (covered) |
| Index rebalancers / closing auction | 15:50–16:00; 16:00–16:08 | imbalance | ES/NQ/RTY | A-C25, C-1-08, C-1-09 | none (covered) |
| Month-end multi-asset rebalancers | last day 15:30–16:00 | month's equity-minus-bond return | ES (equity leg), ZN (bond leg C-1-02) | C-1-02 (bond leg), H0023 (daily TOM) | C-12-15 |
| Commodity index rollers (GSCI/BCOM) | 5th–9th business day, settlement | roll schedule | CL/GC/ZC spreads | A-C17 (closed, negative post-2004) | declined |
| Non-index longs before First Notice Day | 3 days before FND, settlement window | long liquidation | GC/SI/CL front vs 2nd | A-C17 (negative, different population) | C-12-25 |
| Expiring energy contracts (physical index) | expiry day 14:00–14:30 | settlement painting | NG/CL expiring vs 2nd | C-9-09 (daily settlement, not expiry) | C-12-11 |
| Physical oil traders in the Platts window | 11:00–11:30 | assessment incentives | CL (Brent via CFD) | none | C-12-10 |
| Central-bank fixings (WMR, Tokyo, ECB, PBoC) | 11:00; 20:55/21:55; 09:15/10:15; 20:15/21:15 | fix mechanics | 6E/6B/6J/6A | C-1-04, C-1-05, A-C08 | C-12-14 (PBoC → 6A only) |
| SPX/VIX settlement auctions (SOQ), DAX 13:00 CET, Nikkei SQ, HSI average | 09:30–09:45 ET; 13:00 CET; 09:00 JST; all day HKT | hedge unwind / TWAP settlement | ES, GER40, NKD/JP225, HK50 | negative evidence "bare OPEX" (no mechanism) | C-12-26, C-12-12, C-12-27 |
| Margin-call liquidations (FCM, CME margin hikes) | 09:30–10:30 the day after | against under-margined side | GC/SI/CL/NG/ZC, ES | none; H0012/H0017 adjacent (fade sign failed) | C-12-04, C-12-17 |
| Crypto perp liquidation engines | any; clusters at round levels | liquidation side | BTC perps → CME MBT / FTMO BTCUSD | D3 (closed families; different mechanism) | C-12-05, C-12-13 |
| Retail CFD / FX stop clusters | round numbers | Osler stop/take-profit asymmetry | XAUUSD, GC, ES/NQ | D4 (closed; different rules) | C-12-20 |
| Prop traders at Topstep (16:08 auto-flatten) and MFFU (16:10) | 16:00–16:10 | side of the day's losers | MES/MNQ, ES/NQ | none found | C-12-01 |
| Prop traders at Lucid/Tradeify (16:45), NinjaTrader/AMP intraday-margin end, Bulenox (16:59) | 16:30–17:00 | same | MES/MNQ | none found | C-12-02 |
| Prop traders hitting daily-loss / trailing-drawdown stop-outs | after a ≥ N-point move inside RTH | with the move | MES/MNQ micro share | C-4-04 (drift bursts, price-only) | C-12-03 |
| Prop evaluation crowd at the open and at news bans (±2 min) | 09:30–09:35; 08:28–08:35 | crowd direction from micro share | MES/MNQ; GC/6E/CL/ZN at 08:33 | H0020 (ORB, closed); E2 (ES/NQ macro, closed) | C-12-21, C-12-22 |
| The ORB crowd's stops | after a failed 30-min range break | opposite the failed break | ES/NQ | H0020, prereg_orb30 (C-11-01) | C-12-23 |
| Corporate buyback desks (Rule 10b-18) | 13:00–15:50 on down days outside blackout | buy | ES | none | C-12-24 |
| Sunday and weekday 18:00 reopen crowd | 18:00–18:15 | news overshoot through a thin book | ES/NQ/GC/6E | lane 3 (not this window) | C-12-18, C-3-07 |
| Prop accounts forced to roll the expiring contract | firm roll date, fixed minute | two outright legs | MES/MNQ front vs 2nd | none | C-12-31 |
| TAS users (index rollers, ETFs, hedgers) | before the settlement window | sign of TAS prints | CL/NG/GC | A-C17, C-9-09 | C-12-32 |
| Treasury buyback counterparties (primary dealers) | 13:40–14:00 | hedge then unwind | ZN/ZB/UB | none (program since 2024) | C-12-29 |
| Retail indicator bots at bar closes | :00/:15/:30/:45 | indicator flips | MES/MNQ | C-9-08 (30-min periodicity) | C-12-30, C-9-10, C-6-06 |
| 0DTE dealers at the put wall | first touch after 10:00 | local gamma sign | ES | C-1-10, C-4-05 | C-12-28 (forward-only) |

Which firm rules let a bot be on the other side: an FTMO account (US500/US100 CFD priced off ES/NQ, tradable to ≈ 23:00 CET) and a Bulenox account (flat by 15:59 CT = 16:59 ET) can trade against every futures-firm deadline; a Lucid/Tradeify account (16:45 ET) can trade against Topstep (16:08) and MFFU (16:10) but not against its own crowd; a Topstep account can trade against nobody later than itself. Minimum holds (Lucid 5 s, Tradeify 10 s) are irrelevant at minute horizons; MFFU Rapid/Pro news windows matter only for C-12-22 (and are the mechanism there).

## Candidate blocks

### C-12-01 Prop-firm forced flatten at Topstep (16:08 ET auto-flatten) and MyFundedFutures (16:10 ET): the post-cash-close liquidation of the day's losers, traded from a later-deadline account
- mechanism: tens of thousands of funded/evaluation accounts at Topstep (auto-flatten 15:08 CT, breach at 15:10 CT) and MFFU (flat by 16:10 ET) must close every position in the 8–10 minutes after the 16:00 ET cash close, when ES/NQ liquidity has already thinned (the cash-close auction is over, ES halts at 16:15). Retail position-holders at that minute are disproportionately the day's losers (the disposition effect: winners were taken at targets; losers are "held to the deadline"), so the forced flow is on the losing side of the day: on an up day the forced orders are buy-to-cover, on a down day sell-to-close, i.e. the flatten *extends* the day's move 16:00 → 16:08 and the extension reverts afterwards (no fundamental information; the counterparties are market makers who need to be paid). Footprint: a volume spike in MES/MNQ (not ES/NQ) at 16:05–16:09 ET, visible in 1-minute bars as micro volume / mini volume far above its 16:00 baseline; a second, smaller spike at 16:10. The micro share of CME equity-index volume was 40.5% of contracts in 2025 (CME, https://www.cmegroup.com/news/2025/equity-insights-report.html, search snippet 2026-11-04), MES ADV ≈ 1.3M contracts (≈ 130k ES-equivalents a day), MNQ ≈ 1.8M; if even 2% of a day's micro volume is forced into eight minutes the burst is 2–3k ES-equivalents, comparable to a normal minute's ES volume at 16:05. Survival: the deadlines are written in firm rules and cannot move intraday; the crowd cannot learn its way out because the rule, not a belief, forces the trade.
- evidence: own idea. Firm clauses from `firms-2026-10-11.md` (Topstep "Flat by 3:10 PM CT with auto-flatten at 3:08"; MFFU "Flat by 4:10 PM ET"); no published study of prop-firm flatten footprints found (searches 2026-11-04: only firm marketing, forum posts and a SpotGamma note about close-concentrated ES volume that does not attribute it; e.g. https://www.daytraders.com/overnight-trading-rules-prop-firms, https://spotgamma.com/?p=952). Post-2015 OOS: none; the prop-firm population only became large after 2020 (Topstep bots on Express Funded since 2023; MFFU founded 2023), so the usable sample is ≈ 2021–2026.
- evidence window: none (untested); institutional window 2021-01 → today only.
- instruments: MES/ES (primary), MNQ/NQ; FTMO US500.cash / US100.cash for the counter-side if their CFD prices follow ES after 16:00 ET (verify on the symbol page).
- holding period and expected trades per year: leg A (with the flow): enter 16:00:30 ET in the direction of the 09:30 → 16:00 day sign when |day return| > 0.5%, exit 16:08; leg B (against the flow, the main leg): enter 16:08:30 fading the 16:00 → 16:08 move when that move exceeded 1.5 ES points and micro share in 16:04–16:08 was in its top tercile, exit 16:44 (Lucid/Tradeify) or 16:58 (Bulenox) or hold at FTMO to 17:00 / the 18:00 reopen. ≈ 120–180 qualifying days/yr; two legs → up to ≈ 300 trades/yr.
- data needed: Databento 1m full session (RTH files stop at 16:00) for ES and MES 2019–2026 (≈ $20 each = $40; MNQ/NQ another $40 — over the ceiling together, so ES+MES first); the in-hand Databento ES 2021–2026 copy is LICENCE HOLD (cross-check only). Micro share needs both roots. $40 inside the plan.
- expected gross edge per trade: leg B must earn ≥ 2 × RT: ES RT ≈ 0.6 pt → ≥ 1.2 pt per trade; a 16:00–16:08 overshoot of 1.5–3 pt on qualifying days that half-reverts gives 0.75–1.5 pt gross → borderline; passes the screen only on the top-tercile micro-share days; leg A fails the screen alone (≈ 0.5 pt expected). MES RT ≈ 0.5 pt + $1.60 per contract (≈ 0.8 pt) is worse per unit.
- firm structure fit: intraday futures, but only from an account whose deadline is later than the crowd's: Lucid/Tradeify (16:45 ET; leg B exit 16:44, minimum holds 5 s / 10 s irrelevant), Bulenox (16:59 ET; conditional firm), FTMO intraday CFD (to ≈ 23:00 CET) — a Topstep or MFFU account cannot trade this. No news windows at 16:00. Cross-firm clause: the bot must not hold opposite exposure at two firms (Tradeify §6.7(i)): legs A and B are sequential, never simultaneous.
- nearest closed relative: H0006/H0019 (last-half-hour momentum, 15:30–16:00, closed) — this window starts where that one ends and trades the reversal of a forced flow, not momentum; C-1-08 (post-cash-close reversal of the auction move, 16:00 → 16:08) is the adjacent sibling candidate: C-1-08 fades the 15:50–16:00 auction move at 16:00; this fades the 16:00–16:08 forced-flatten move at 16:08 and conditions on the micro footprint. Register both only if the Pre-registration Officer accepts the different trigger window; otherwise merge as one row with two legs.
- decay haircut: 0.7 (original); splits at 2023-03 (Topstep API bots allowed), 2024 (MFFU scale), 2026-02 (ProjectX third-party service ended).
- plausibility of net Sharpe ≥ 1.5: low — the flow is real and timed to the minute, but it is small against ES depth and the eight-minute overshoot may be a fraction of a point; the micro-share footprint is the first thing to measure (free once the bars exist) before any P&L.
- original: yes
- LANE-12 TOP TEN: yes (rank 1: the only forced trader whose clock is written in a contract Itamar can read, and whose counter-side is a firm structure on the safe list)

### C-12-02 The 16:30–17:00 ET micro-session: Lucid/Tradeify (16:45) and NinjaTrader/AMP intraday-margin end (15:45 CT) flatten, Bulenox (16:59) last, after the 16:15–16:30 ES halt
- mechanism: ES/NQ halt 16:15–16:30 ET and reopen 16:30–17:00 ET (secondary sources, e.g. https://tradeify.co/post/futures-market-hours-and-the-best-times-to-trade, 2026-11-04; verify on cmegroup.com). Into that thin half-hour three forced flows arrive on a clock: NinjaTrader Brokerage's intraday margin ends 15:45 CT = 16:45 ET for ES (https://ninjatrader.com/pricing/margins-position-management/, snippet 2026-11-04: "intraday margin end time 15:45 CT"), after which under-margined retail positions are liquidated; Lucid and Tradeify funded accounts must be flat by 16:45 ET; Bulenox by 15:59 CT = 16:59 ET. The 16:30 reopen print itself repriceses 15 minutes of news with almost no book. Direction as in C-12-01 (losers are flattened: the flow extends the day's sign). Footprint: micro volume spikes at 16:30–16:31, 16:43–16:45 and 16:57–16:59 ET.
- evidence: own idea; broker and firm pages above; no study found.
- evidence window: none.
- instruments: MES/ES, MNQ/NQ; FTMO US500/US100 (the only safe-list counter-side after 16:45).
- holding period and expected trades per year: fade the 16:40 → 16:45 move at 16:45:30, exit 16:58 (Bulenox) or 17:00 / hold to the 18:00 reopen (FTMO; swap is charged at FTMO's midnight server time, so a 16:45 → 18:30 ET hold crosses it: cost 1 swap night); ≈ 100–150 trades/yr.
- data needed: as C-12-01 (full-session 1m ES + MES, $40, shared).
- expected gross edge per trade: unknown; 16:30–17:00 ES minute ranges are ≈ 0.5–1 pt, so a 1-pt overshoot that half-reverts is 0.5 pt < 2 × RT (1.2 pt) → fails the screen unless the top-decile days are 3 pt+; MES is worse. Honest expectation: a footprint study, not a sleeve.
- firm structure fit: Bulenox only (conditional firm, written approval needed) or FTMO intraday CFD / FTMO Swing (hold to the reopen). Topstep, MFFU, Lucid, Tradeify cannot trade this window at all.
- nearest closed relative: none closed; C-12-01 sibling; C-1-08.
- decay haircut: 0.7; splits as C-12-01 plus 2013-03 (CME halt moved from 15:15 CT).
- plausibility of net Sharpe ≥ 1.5: low (very low): the firms that can trade it are the weakest in the fleet.
- original: yes
- LANE-12 TOP TEN: no (fits only Bulenox/FTMO)

### C-12-03 Prop-account daily-loss and trailing-drawdown stop-outs: the micro-share liquidation cascade after a ≥ N-point move inside RTH
- mechanism: every funded account carries a hard daily loss (≈ $1,000–$2,500 on 50K–150K plans) and, at MFFU Rapid and Topstep, a trailing maximum-loss computed on unrealized P&L in real time; the firm's risk engine liquidates at the breach. A one-directional move of 15–25 ES points inside an hour pushes a cohort of retail positions (mostly counter-trend: retail fades) through those limits simultaneously → forced orders in the direction of the move, concentrated in micro contracts → the move's last leg is retail liquidation, which has no information and reverts. Footprint: during the move, the micro share of volume (MES/(MES+10·ES) in contracts, or MES volume relative to its time-of-day profile) rises above its 90th percentile while price makes new extremes; the cascade ends when micro volume collapses below profile while price is still at the extreme (no more accounts left to liquidate). Trade: fade the extreme once the micro-volume burst has decayed for 3 consecutive minutes.
- evidence: own idea. Firm rules: MFFU "Rapid funded uses an intraday trailing drawdown from the equity high-water mark"; Topstep "maximum loss limit … enforced in real time including unrealized P&L" (`firms-2026-10-11.md`). The micro-contract retail base: CME 2025 equity recap (https://www.cmegroup.com/newsletters/quarterly-equity-index-recap/2025-july-equity-index-recap.html, 2026-11-04). Price-only drift-burst fades are lane-4 material (C-4-04, Nagel-type); this adds the retail footprint as the trigger. No study of micro-share dynamics found.
- evidence window: none; micro contracts exist since 2019-05 (MES/MNQ), so 2019–2026 only.
- instruments: MES/ES, MNQ/NQ (MNQ has the largest retail share: MNQ ADV 1.8M = 53% of the micro suite); secondary MGC/GC, MCL/CL.
- holding period and expected trades per year: 10–40 minutes; ≈ 100–250 triggers/yr per root at |move| ≥ 1.5 × the 60-minute realized-vol forecast.
- data needed: Databento 1m RTH ES + MES (≈ $14) or NQ + MNQ (≈ $14); the volume profile needs ≥ 3 years. Free alternatives do not carry micro volume.
- expected gross edge per trade: if the liquidation leg is 2–4 ES points and half reverts, 1–2 pt gross vs 0.6 pt RT → passes the screen; the 2 × cost run (1.2 pt) is the real test; the top-decile burst days decide it.
- firm structure fit: intraday futures at every safe-list firm (window inside RTH, exits well before 16:08); MFFU news windows: triggers within ±2 minutes of a Tier-1 release skipped; no minimum-hold issue.
- nearest closed relative: H0013/H0014 (IBS reversal, daily) no; C-4-04 (drift-burst fade, price/volume only) — this is the same trade family with a different, retail-specific trigger; if C-4-04 is registered first, this becomes its conditional variant (one count).
- decay haircut: 0.7; splits at 2019-05 (micro launch), 2022-05 (daily 0DTE), 2024 (prop population peak).
- plausibility of net Sharpe ≥ 1.5: low-medium for the footprint being measurable, low for the P&L; it is the cleanest test of whether the prop crowd leaves any trace at all, which every other lane-12 block depends on.
- original: yes
- LANE-12 TOP TEN: yes (rank 2)

### C-12-04 CME margin-hike liquidation at the next session's open: the under-margined side is forced out 09:30–10:30 ET (GC/SI/CL/NG/ZC) and at the 18:00 reopen
- mechanism: CME Clearing raises performance bonds by advisory, typically after a large move, "effective after the close of business" on the stated date (e.g. https://www.cmegroup.com/notices/clearing/2022/11/Chadv22-433.html, https://www.cmegroup.com/notices/clearing/2024/06/Chadv24-166.html, fetched as snippets 2026-11-04; archive back to 2008). FCMs pass the increase to retail with intraday margin multiples, and under-margined positions are liquidated at the next session (brokers run liquidation at the open or by a fixed morning deadline). The under-margined side is the side that just lost (the hike follows the move), so the liquidation is *with* the prior move at the open and reverts after. Daskalaki & Skiadopoulos (J. Financial Stability 22, 2016, https://econpapers.repec.org/RePEc:eee:finsta:v:22:y:2016:i:c:p:129-152, abstract 2026-11-04) find margin increases "decrease the rate at which prices change" and impair liquidity in commodities, stronger than in equity/rates futures; AQR's working paper on 2000–2011 CME margins reports realized volatility ≈ 50% higher on the day of a margin increase (https://www.aqr.com/Insights/Research/Working-Paper/Causes-and-Consequences-of-Margin-Levels-in-Futures-Markets, snippet). Nobody measured the first-hour footprint.
- evidence: peer-reviewed (daily-level, direction neutral) + own idea for the intraday rule; CME advisory archive is free text (lane 13 adjacent).
- evidence window: 20 commodity markets to ≈ 2013 (D&S); CME 2000–2011 (AQR); first-hour window untested.
- instruments: GC/MGC, SI/SIL, CL/MCL, NG/MNG, ZC, ZS; ES/NQ hikes are rarer.
- holding period and expected trades per year: 09:30 → 10:30 ET with the prior move, then fade to 12:00; CME issues ≈ 100–300 margin advisories a year across all products, ≈ 30–60 touching these roots → ≈ 30–60 event days/yr (a sleeve, under 40 per root: annual contribution at 1 MGC/MCL per $10k drawdown is at most a few hundred dollars per account; it only matters inside a stack).
- data needed: Databento 1m RTH GC, SI, CL, NG (≈ $28; shared with C-1-06); advisory dates parsed from cmegroup.com (free, labour; the 2008–2026 archive exists).
- expected gross edge per trade: unknown; a 0.3–0.5% first-hour extension on a hike day in GC is 15–25 bp vs ≈ 1 bp RT → passes the screen if it exists; CL 4 bp RT, NG 7 bp RT need 10–15 bp.
- firm structure fit: intraday futures (all firms; 09:30–12:00); the 18:00 ET reopen variant is an overnight-session hold (inside one day); MFFU news windows irrelevant except 08:30 releases; FTMO intraday CFD on XAU/XAG/WTI/NATGAS.
- nearest closed relative: none closed; H0012/H0017 (gap fade) share the open window but had no event trigger.
- decay haircut: 0.7; splits at 2011-05 (SI margin cascade), 2020-04, 2022-03 (NI/energy hikes).
- plausibility of net Sharpe ≥ 1.5: low (event-sparse, direction only half-known per event).
- original: yes
- LANE-12 TOP TEN: yes (rank 7: free text trigger, forced side identifiable)

### C-12-05 Crypto perpetual liquidation cascades → CME MBT / FTMO BTCUSD: fade the exhaustion of the forced leg
- mechanism: offshore perp exchanges auto-liquidate leveraged positions at known maintenance-margin levels; cascades (liquidations begetting liquidations) are the dominant intraday flow in BTC on high-vol days and have no information content once the queue is empty. The forced leg exhausts when open interest stops falling while price stops making new extremes. CME MBT and the FTMO BTCUSD CFD follow Binance within seconds, so a retail bot cannot front-run the cascade, only its end. Free data check 2026-11-04: the Binance bulk archive (https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?delimiter=/&prefix=data/futures/um/daily/) has aggTrades, bookDepth, bookTicker, indexPriceKlines, klines, markPriceKlines, metrics, premiumIndexKlines, trades — **no liquidation folder** (the `liquidationSnapshot` prefix returns an empty listing), so the forced flow must be proxied from `metrics` (5-minute open interest, long/short account ratio, taker buy/sell volume) + aggTrades, which is coarser than a liquidation feed. That proxy limitation is why this ranks below C-12-03.
- evidence: own idea; the mechanism is practitioner folklore ("liquidation heatmaps"), no code-backed public test seen; D3 (closed) tested TSMOM/XS/funding/C&C/hour-of-day on Binance, never a liquidation-exhaustion rule.
- evidence window: none; Binance UM `metrics` exist from ≈ 2021-12 (verify) → 2021–2026.
- instruments: MBT/BTC (CME, overnight-session or intraday at futures firms that list MBT — Topstep does), FTMO BTCUSD (intraday; swap −30%/yr both sides forbids holding).
- holding period and expected trades per year: 15–90 minutes; ≈ 150–400 cascades/yr at the |5-min return| > 3σ and ΔOI < −1% trigger.
- data needed: data.binance.vision UM BTCUSDT 1m klines + 5-min metrics + aggTrades (free, large); CME MBT 1m from Databento (≈ $20 full session; needed for the tradable price, basis and MBT liquidity at 03:00 ET).
- expected gross edge per trade: cascades overshoot by 0.5–2% in BTC; half-reversion = 25–100 bp vs MBT RT ≈ 2 bp + $2 and FTMO 11.5 bp/side → passes the screen on paper at both venues; the real question is MBT depth at the cascade minute (retail size only).
- firm structure fit: overnight-session or intraday futures (MBT at Topstep/MFFU if listed; verify per firm); FTMO intraday CFD; no news windows; crypto firms are "Out" per `firms-2026-10-11.md`.
- nearest closed relative: D3-01..11 (crypto; closed) — different mechanism (forced liquidation, not momentum/funding/calendar); the board allows a new row only with a new mechanism, which this is; the Pre-registration Officer decides.
- decay haircut: 0.7; splits at 2021-05, 2022-11 (FTX), 2024-01 (spot ETFs), 2025-10 (record liquidation day).
- plausibility of net Sharpe ≥ 1.5: low — without the liquidation feed the trigger is blunt, and MBT depth at 03:00 ET is thin.
- original: yes
- LANE-12 TOP TEN: yes (rank 8)

### C-12-06 Vol-control and risk-parity deleveraging: the 1–3 day sell program executed into the close after a realized-vol jump
- mechanism: volatility-targeting funds (Nomura's model: ≈ $28.8bn of forced selling for a week of 1% daily S&P moves, versus ≈ $2.3bn of buying from a sideways week; a two-week run of 1% days ≈ $15bn more; https://www.advisorperspectives.com/articles/2023/08/11/week-of-moves-on-sandp-500-could-trigger-forced-selling, snippet 2026-11-04; "around $17 billion would have to be sold into the close" on one November-2025 day, snippet, unverified) scale exposure to trailing realized vol and execute at or near the close over the following sessions (sunshine-style VWAP/MOC). The trigger (a jump in 1-month realized vol after a big down day) is computable from free daily data the night before, the direction is known (sell after vol up, buy after vol down), and the time of day is the last hour. Risk-parity and target-vol insurance products (≈ $300–500bn by sell-side estimates) add to it. The question is only whether the last-hour footprint survives market makers who know the same arithmetic.
- evidence: practitioner (bank model via press); academic background: Moreira & Muir (JF 2017) on the returns of vol-managed portfolios, not on their price impact; no minute-level test found.
- evidence window: none at minute level; the Nomura model numbers are 2023–2026 press snippets.
- instruments: ES/MES (primary), NQ; FTMO US500 (intraday or Swing: the multi-day version holds across the close with swap).
- holding period and expected trades per year: on day t+1..t+3 after a day whose |return| > 1.5% raised 21-day realized vol by > 15% relative: enter 15:00 ET on the vol-change sign (short after a vol jump, long after a vol collapse), exit 15:59 (futures) or hold to the next open (FTMO Swing); ≈ 40–80 trading days/yr.
- data needed: ES 1m RTH (in hand 2008–2026, licence-held copy cross-check only; or Databento ≈ $7); S&P daily (free) for the vol trigger. $0–7.
- expected gross edge per trade: the sell-side forecast implies ≈ 0.3–0.5% of ES ADV notional per day on the big days; square-root impact of that is 5–15 bp over the hour vs 1.2 bp RT → passes the screen if a third of it is in the last hour and not pre-hedged.
- firm structure fit: intraday futures (15:00 → 15:59, inside every deadline); FTMO Swing variant holds 2–3 nights (swap ≈ −8%/yr long US index / ≈ +0.4% short per the E1 numbers). Consistency rules: sparse big days concentrate P&L (Topstep consistency policy touched).
- nearest closed relative: H0006/H0019 (last-half-hour momentum; closed) — same window, different conditioning (a known external order, not price momentum); A-C30 (vol-targeting as an overlay, not as a counterparty).
- decay haircut: 0.5 (bank models publish the flow daily; it is as public as flow gets); splits at 2018-02 (Volmageddon), 2020-03, 2022.
- plausibility of net Sharpe ≥ 1.5: low — the flow is enormous but the most-anticipated in the market; a measurable last-hour tilt on the 40 biggest days a year would still be worth a sleeve.
- original: yes (no minute-level construction found; the bank commentary is not a test)
- LANE-12 TOP TEN: yes (rank 3)

### C-12-07 CTA trigger levels: last-hour continuation on the day a crowded trend signal flips (ES/NQ/CL/GC/ZN/6E)
- mechanism: trend followers (≈ $300bn+ in CTAs, plus bank replication and ETF trend products) run slow signals that flip at computable price levels (the 50/100/200-day moving averages, 1/3/12-month return signs, EWMAC crossovers); flips are executed at or after the close of the flip day (most CTAs trade daily on the close or the next open). Sell-side desks publish the "trigger levels" every week; the glossary/vendor claim that they become self-fulfilling is widely repeated and never tested in public (search 2026-11-04: https://convextrade.com/glossary/cta-trend-following; https://www.tradingpedia.com/2025/12/22/bank-of-america-sees-limited-cta-forced-selling-risk-despite-stretched-equity-positions; the academic base, Levine & Pedersen "Which Trend Is Your Friend", compares signals and says nothing about intraday pressure). Rule: when the 15:00 ET price is through a signal level that was not crossed at the prior close (so a close beyond it flips the model), trade in the cross direction 15:00 → 15:59 and (futures firms) stop there; FTMO Swing holds to the next open to capture the "next-open" CTAs.
- evidence: practitioner/vendor only; peer-reviewed signal literature without flow tests; own construction.
- evidence window: none.
- instruments: ES, NQ, CL, GC, ZN, 6E (the six most CTA-crowded liquid roots); FTMO twins (US500, US100, USOIL, XAUUSD, EURUSD; no bond CFD).
- holding period and expected trades per year: 15:00 → 15:59 ET; a basket of 3 signal families × 6 roots crosses ≈ 15–30 times per root per year → ≈ 100–180 trades/yr.
- data needed: daily closes (free) for the levels; 1m RTH for the six roots (ES in hand; CL/GC/ZN/6E/NQ ≈ $35 at $7 each). Inside the plan.
- expected gross edge per trade: a $5–15bn aggregate flip executed over a close in ES is ≈ 1–3% of ADV → 5–10 bp square-root impact; a third in the last hour = 2–3 bp vs 1.2 bp RT (ES), 3 bp RT (ZN) → passes in ES/6E/GC, marginal in ZN/CL.
- firm structure fit: intraday futures (15:00 → 15:59 ET; ZN's 15:00 settlement means the ZN leg runs 14:00 → 15:00); FTMO Swing variant for the next-open leg.
- nearest closed relative: H0006/H0019 (last-half-hour momentum ES, closed); D4-01 (Gao last half hour across CFDs, closed) — both unconditional; this trades only on signal-cross days with a named counterparty. H0007 (multi-day trend as goal) is not touched: no position is held across the close at futures firms.
- decay haircut: 0.5 (trigger levels are published weekly by several banks); splits at 2008, 2020-03, 2022.
- plausibility of net Sharpe ≥ 1.5: low; a clean negative result would also retire a popular belief, which has value for the Red Team's priors.
- original: yes (as a tested rule; the belief is not)
- LANE-12 TOP TEN: yes (rank 5)

### C-12-08 VIX ETP leverage rebalancing (UVXY/SVXY/SVIX/UVIX) → the ES delta leg 15:45–16:15 ET on large VIX days
- mechanism: daily-reset VIX ETPs rebalance VIX-futures exposure at the 16:15 ET VIX-futures settlement in the direction of the day's VIX-futures move (Todorov, "When passive funds affect prices", Review of Finance 28(3) 2024, 831–863, https://econpapers.repec.org/RePEc:oup:revfin:v:28:y:2024:i:3:p:831-863; BIS WP 952 https://www.bis.org/publ/work952.pdf; abstracts/snippets 2026-11-04: leverage rebalancing is the largest component and VIX futures were overpriced ≈ 18.5%/yr after ETP introduction). The dealers who sell that VX exposure hedge vega with ES (short ES when they go long VX), so an ES footprint should appear 15:45–16:15 on days with a large VIX-futures move, in the direction of equities' day sign (VIX up → ETPs buy VX → dealers short ES). No safe-list firm offers VX (G1 closed for that reason); the ES leg is the only tradable expression, and it was not tested in G1 or anywhere seen.
- evidence: peer-reviewed for the VX pressure; own idea for the ES leg. VIX ETP AUM (free, issuer pages): UVXY/SVXY/SVIX/UVIX of the order of $1–3bn each at 1.5×/−1×/2×; required daily VX notional = Σ AUM × L(L−1) × r_VX.
- evidence window: VX 2004–2019 (Todorov; window per BIS version, verify); ES 15:45–16:15 untested.
- instruments: ES/MES; secondary NQ.
- holding period and expected trades per year: 15:45 → 16:08 (Topstep) / 16:10 (MFFU) / 16:14 (Lucid); trigger |VX front return at 15:45| > 5% → ≈ 40–60 days/yr.
- data needed: ES 1m full session (16:00–16:15 bars; ≈ $20) or the RTH copy for the 15:45–16:00 part ($0 in hand, licence-held for cross-check); VX daily/1m — CBOE delayed VIX futures history is free daily, not 1m (VX is CFE, not in GLBX; Databento XCBF 1m ≈ price not checked); ETP AUM histories from issuer pages (free).
- expected gross edge per trade: a 10% VX day on $5bn of levered ETP AUM ≈ $1bn VX ≈ 50k ES-vega-equivalents … in delta terms a few thousand ES over 30 minutes → 3–8 bp vs 1.2 bp RT: passes the screen on those days if dealers do not pre-hedge (they partly do, per Barbon et al. on equity LETFs).
- firm structure fit: intraday futures (exit before each deadline; the 16:00–16:15 part needs Lucid/Tradeify/Bulenox/FTMO); no news windows.
- nearest closed relative: G1 (VRP/VIX; closed for lack of product — this needs no VIX product); H0006/H0019 (last-half-hour momentum, closed; this is conditional on an external flow and extends past 16:00).
- decay haircut: 0.5 (published mechanism); splits at 2018-02 (XIV termination), 2022 (SVIX/UVIX launch).
- plausibility of net Sharpe ≥ 1.5: low; event-sparse.
- original: yes (ES leg)
- LANE-12 TOP TEN: yes (rank 9)

### C-12-09 Single-stock leveraged ETFs (NVDL, TSLL, and the 2× NVDA/TSLA/MSTR/COIN complex) → NQ last-15-minute flow on big NVDA/TSLA days (twist on A-C24)
- mechanism: 2× single-stock ETFs did not exist when the LETF literature was written (US launches 2022-07); NVDL alone holds ≈ $4.1–4.5bn (TradingView / Walnut Invest pages, 2026, https://in.tradingview.com/symbols/NASDAQ-NVDL, snippet 2026-11-04), TSLL similar order of magnitude (not verified: search found no figure), plus MSTU/MSTX, CONL, AMDL, etc. They reset daily at the 16:00 NAV via swaps whose dealers hedge in the stock into the close: required flow = AUM × 2 × 1 × r_day, i.e. ≈ $80–90m of NVDA for a 1% NVDA day from NVDL alone, several hundred million on a 5% day across the complex, concentrated in the names that are 10–15% of the Nasdaq-100. The NQ footprint is the index-level shadow of that flow: last-15-minute NQ momentum conditional on |NVDA or TSLA day return| > 3% and the single-stock LETF AUM (free from issuer pages).
- evidence: peer-reviewed analogues for index LETFs (Shum et al. RoF 2016; Barbon et al. 2022; per A-C24) + issuer AUM; own twist. Post-2015 OOS: none; the instruments exist only since 2022-07.
- evidence window: US equity LETFs ≈ 2006–2020 (A-C24); single-stock LETFs untested; usable sample 2022-08 → today only (≈ 4 years; cannot meet the 8-year rule — flagged).
- instruments: NQ/MNQ; FTMO US100 intraday.
- holding period and expected trades per year: 15:45 → 15:59 ET with the day sign of the trigger stock; ≈ 40–70 trigger days/yr.
- data needed: NQ 1m (in-hand NQ 2020-09–2025-11 copy, licence status to check; Databento ≈ $7 RTH); NVDA/TSLA daily (free); LETF AUM history (issuer pages, SEC N-PORT, free, labour).
- expected gross edge per trade: on a 5% NVDA day the complex trades ≈ $0.5bn of NVDA into the close (≈ 1–2% of NVDA ADV) → 5–10 bp in NVDA ≈ 1 bp in NQ: fails the screen at index level unless the day is extreme (10%+) — honest reading: the index shadow is too diluted; register only as a conditional variant of a last-15-minute NQ row, if any.
- firm structure fit: intraday futures; FTMO intraday CFD.
- nearest closed relative: H0006/H0019 (last-half-hour momentum ES/NQ, closed) — heavy overlap in window; A-C24 (index LETF demand sizing).
- decay haircut: 0.5; split at 2022-07 (launch), 2024 (AUM surge).
- plausibility of net Sharpe ≥ 1.5: very low (dilution at index level, 4-year sample).
- original: no (A-C24 with a new flow source; listed because the flow did not exist when A-C24's sources were written)
- LANE-12 TOP TEN: no

### C-12-10 The Platts Dated Brent MOC window (16:00–16:30 London = 11:00–11:30 ET): assessment-driven futures flow in CL / Brent CFD
- mechanism: physical players with positions priced off Dated Brent trade the Platts market-on-close window to influence the assessment; Frino, Ibikunle, Mollica & Steffen (J. Banking & Finance 2018) show ICE Brent futures trading intensifies in the window and moves in the direction of the published benchmark (snippet 2026-11-04; original not fetched; see also Swinand & O'Mahoney MPRA 56252 https://mpra.ub.uni-muenchen.de/56252/1/MPRA_paper_56252.pdf and the 2013 civil complaint reproduced at https://mining.com/wp-content/uploads/2013/11/181998111-Court-Filing.pdf). The window is 16:00–16:30 London with price changes accepted to 16:28 (S&P Global subscriber note, https://www.spglobal.com/commodity-insights/en/pricing-benchmarks/our-methodology/subscriber-notes/021813-platts-to-extend-brent-cfd-timings-for-price-changes-in-moc). The footprint is a half-hour of direction-persistent flow in Brent that CL follows via the spread, then a post-window reversal (the assessment is done; the painter steps away). Rule: momentum 11:00 → 11:28 ET in the direction of the 11:00–11:10 move, then fade 11:30 → 12:00.
- evidence: peer-reviewed (JBF 2018; window ≈ 2010–2014, verify) for the flow; own idea for the two-leg rule; the reversal leg is untested anywhere seen.
- evidence window: ICE Brent ≈ 2010–2014 (Frino et al., verify); CL window untested.
- instruments: CL/MCL (CME; Brent BZ is CME-listed too, low volume); FTMO UKOIL/USOIL intraday CFDs (the Brent CFD is the direct expression).
- holding period and expected trades per year: two legs of ≈ 30 minutes; every trading day → ≈ 250 days × 2 legs (only days whose 11:00–11:10 move exceeds 0.2% for the momentum leg: ≈ 120/yr).
- data needed: CL 1m RTH (Databento ≈ $7; shared with lanes 1–2); Brent 1m: HistData has BCO/USD 1m free (https://www.histdata.com/download-free-forex-data/?/ascii/1-minute-bar-quotes, fetched 2026-11-04) → $0 for the CFD leg.
- expected gross edge per trade: Brent moves ≈ 20–40 bp in the window on active days; capturing a third = 7–13 bp vs 2.5 bp/side CFD (5 bp RT) → marginal pass; CL 4 bp RT similar.
- firm structure fit: intraday futures; FTMO intraday CFD; no news windows (EIA is 10:30 ET Wednesday — the window starts 30 minutes later; MFFU ±2 min irrelevant).
- nearest closed relative: none closed; C-2-02/C-2-03 (EIA) are the morning neighbours; C-9-09 (settlement-window flow, 14:28–14:30 ET) is the afternoon neighbour.
- decay haircut: 0.5 (published) for the momentum leg, 0.7 for the reversal leg; splits at 2015 (Platts Brent basket changes), 2023 (WTI Midland added to Dated Brent).
- plausibility of net Sharpe ≥ 1.5: low.
- original: no (momentum leg published: Frino et al. 2018); the reversal leg is an original twist
- LANE-12 TOP TEN: no

### C-12-11 Energy expiry-day final settlement: NG and CL last-trading-day 14:00–14:30 ET window in the expiring month, hedged through the second month
- mechanism: NYMEX NG expires three business days before the delivery month at 14:30 ET and its final settlement is the index for a large share of physical gas; CL expires three business days before the 25th. On the last trading day the expiring contract is thin and dominated by participants with physical or swap exposure to the settlement (the Amaranth 2006 and the 2007–2008 "banging the close" cases are the record), so the last 30 minutes carry one-directional settlement-targeting flow, which the second month only partly follows and which reverts at the 18:00 reopen. Rule: in the expiring month (if the firm allows trading it on expiry day — many prop platforms roll traders out the day before: verify), momentum 14:00 → 14:28 in the direction of the 13:30–14:00 move; else trade the second month's 14:00 → 14:30 move and fade it at the 18:00 reopen (overnight-session hold, inside one day).
- evidence: own idea; the enforcement record (CFTC Amaranth, Optiver 2008 "bang the close") as mechanism evidence, not as a test; C-9-09 covers the *daily* settlement flow proxy, not expiry days.
- evidence window: none.
- instruments: NG/MNG, CL/MCL (expiring and second month); FTMO NATGAS/USOIL CFDs track the front/second month by the provider's roll rule (verify which).
- holding period and expected trades per year: 30 minutes + an optional overnight-session fade; 12 NG + 12 CL expiries/yr = 24 events (a sleeve; annual contribution at micro size is small: ≈ 24 × 1 MNG/MCL × 10–20 bp ≈ $100–300 per $100k account; it only matters in a stack).
- data needed: NG and CL 1m, *two contract months* (Databento by raw symbol, ≈ $7 each per root-month set for RTH; ≈ $28 for both roots and months); expiry calendar free.
- expected gross edge per trade: expiry-day final half-hour moves of 0.5–1.5% in NG are common; a third captured = 15–50 bp vs 7 bp RT → passes; CL smaller (10–30 bp vs 4 bp RT) → passes.
- firm structure fit: intraday futures for the window; the fade is an overnight-session hold (allowed: after 18:00 ET, closed before the next deadline); check each firm's rule on trading the expiring contract on its last day (Topstep/MFFU may force a roll — verify, Rules Keeper).
- nearest closed relative: none closed; C-9-09 (daily settlement bar flow, different days); C-1-06 (LETF settlement flows: BOIL/KOLD roll before expiry, so the LETF flow is in the second month on these days — interaction to model).
- decay haircut: 0.7; splits at 2008 (CFTC enforcement), 2020-04 (CL negative expiry), 2022.
- plausibility of net Sharpe ≥ 1.5: low (24 events/yr).
- original: yes
- LANE-12 TOP TEN: no (too few events)

### C-12-12 VIX settlement Wednesdays: the SPX pre-open settlement auction and the ES 09:30–09:45 footprint
- mechanism: monthly (and now weekly) VIX futures/options settle on a special opening quotation computed from SPX options traded in a pre-open auction (07:30–08:30 CT); Griffin & Shams (RFS 31(4) 2018, 1377–1417, https://econpapers.repec.org/RePEc:oup:rfinst:v:31:y:2018:i:4:p:1377-1417, abstract 2026-11-04) document volume spikes in exactly the OTM SPX options that enter the VIX formula at settlement, consistent with manipulation; the settling VIX open interest was ≈ 5.7 × the SPX options traded at settlement. Whoever pushes the SPX option book in the auction is left with delta exposure to hedge when ES opens the cash session at 09:30 → an ES footprint in the first 15 minutes of VIX-settlement days: the hedging unwind should *oppose* the direction in which the settlement was pushed, observable as a reversal of the 09:15–09:30 ES move. Rule: on VIX-settlement Wednesdays fade the 09:15 → 09:30 ES move from 09:31 to 09:45.
- evidence: peer-reviewed for the auction anomaly (sample 2008–2015); own idea for the ES leg; "bare OPEX/day-of-week" negative evidence does not apply (a named mechanism and a 15-minute window).
- evidence window: SPX options 2008-01 → 2015-04 (Griffin–Shams); ES window untested.
- instruments: ES/MES; FTMO US500 intraday.
- holding period and expected trades per year: 09:31 → 09:45 ET; 12 monthly + ≈ 40 weekly settlements/yr → ≈ 50 events (a sleeve).
- data needed: ES 1m full session (09:15–09:30 bars are outside RTH files: ≈ $20) or the licence-held copy for cross-check; VIX settlement dates (CBOE, free).
- expected gross edge per trade: 09:15–09:30 ES moves of 0.2–0.4% on those mornings; a third reverting = 7–13 bp vs 1.2 bp RT → passes the screen if the effect exists.
- firm structure fit: intraday futures (all firms); 09:30 is not a news window; MFFU Tier-1 list irrelevant unless a release coincides (skip those days).
- nearest closed relative: E2-01..12 (macro-event intraday ES, closed) — no macro event involved; H0012/H0017 (gap fade, closed) — this is a 15-minute pre-open-move fade on 50 named days, not the overnight gap; "bare OPEX" negative evidence (no mechanism) — this has one.
- decay haircut: 0.5 (the paper changed CBOE's auction design after 2018); splits at 2018-05 (CBOE settlement reforms), 2022 (weekly VIX expansion).
- plausibility of net Sharpe ≥ 1.5: low (very low after the reforms).
- original: yes (ES leg)
- LANE-12 TOP TEN: no

### C-12-13 Deribit options expiry 08:00 UTC (daily, and the monthly/quarterly last-Friday giants): pin into, release after, traded in CME MBT / FTMO BTCUSD
- mechanism: Deribit settles BTC options at 08:00 UTC; monthly/quarterly expiries now reach $10–28bn notional (e.g. https://www.kucoin.com/news/flash/15-6b-in-bitcoin-options-set-to-expire-on-deribit-friday, https://decrypt.co/376752, snippets 2026-11-04). Dealers' delta hedges of expiring near-the-money strikes are unwound at settlement and the pinning force disappears at 08:00 → a pre-expiry drift toward the max-OI strike cluster in the final 2–4 hours (gravitation) and a release afterwards (the 08:00 → 10:00 UTC move away from the pin). Deribit itself notes recent expiries did not show consistent pinning (CoinDesk/Deribit commentary in the same snippets) — that is exactly the kind of null a pre-registered row should record. 08:00 UTC = 03:00/04:00 ET: inside the futures-firm trading day (an overnight-session hold) and inside FTMO's intraday day.
- evidence: forum/press only (no academic study found 2026-11-04); own construction; D3 (closed) never tested an expiry mechanism; max-pain data free from Deribit's public API (OI by strike) only for the present, not historically → the history must be rebuilt from daily snapshots (Deribit public endpoints allow it without an account; verify the terms: no sign-up) or restricted to the expiry *time* effect (no OI needed).
- evidence window: none.
- instruments: MBT/BTC (CME; verify listing per firm), FTMO BTCUSD intraday (swap −30%/yr both sides → never hold past the daily swap time).
- holding period and expected trades per year: pin leg 05:00 → 07:55 UTC; release leg 08:05 → 10:00 UTC; daily expiries → ≈ 250 events/yr for the time-only rule (fade the 06:00–08:00 move after 08:05), monthly/quarterly ≈ 16/yr for the OI-strike version.
- data needed: Binance 1m (free) as the price proxy, CME MBT 1m (Databento ≈ $20 full session) for the tradable instrument; Deribit OI snapshots forward-only (free, no account).
- expected gross edge per trade: BTC 2-hour moves ≈ 50–100 bp; a quarter reverting = 12–25 bp vs MBT RT ≈ 2 bp + $2, FTMO 23 bp RT → passes at CME, fails at FTMO.
- firm structure fit: overnight-session futures (MBT) at firms listing it; FTMO intraday only if the edge is > 2 × 23 bp (unlikely).
- nearest closed relative: D3-09 (BTC hour-of-day seasonality, closed — a bare clock effect; this is conditional on an expiry mechanism) — the Pre-registration Officer must accept the distinction or decline.
- decay haircut: 0.7; splits at 2021 (daily expiries), 2024-01 (US spot ETFs and IBIT options), 2025.
- plausibility of net Sharpe ≥ 1.5: low (Deribit's own null).
- original: yes (no test found; the folklore is not a test)
- LANE-12 TOP TEN: no

### C-12-14 PBoC USD/CNY fixing surprise at 09:15 Beijing (20:15/21:15 ET) → AUD (6A/M6A) and copper reaction in the following 30 minutes
- mechanism: the PBoC's daily mid-point is published at 09:15 Beijing; the market reads the gap between the fix and the model consensus (previous close + overnight dollar move) as a policy signal (Newsquawk fix notes with "vs exp." every day, e.g. https://www.newsquawk.com/headlines/pboc-sets-usdcny-mid-point-at-67873-vs-exp-67382-prev-67878; explainer https://www.forex.com/en-uk/news-and-analysis/explainer-the-pboc-usd-cny-fix-and-how-it-impacts-fx-markets/, snippets 2026-11-04). AUD is the liquid proxy for China risk and the one G10 currency whose futures (6A) trade at the safe-list firms; a stronger-than-expected CNY fix (lower USD/CNY) should lift AUD in the 30 minutes after 20:15 ET as macro desks re-mark the China beta, and the reverse. The fix surprise is computable from free data (fix history from the PBoC/CFETS pages or FRED's daily CNY series as a proxy — the exact consensus is not free; use "fix minus previous onshore close" as the surprise).
- evidence: trader commentary only; no event study of AUD minute returns around the fix found (search 2026-11-04). The 2015-08 episode is the anecdote.
- evidence window: none.
- instruments: 6A/M6A (CME; overnight session = inside the futures-firm day), HG (copper) secondary; FTMO AUDUSD, USDCNH (if listed) intraday.
- holding period and expected trades per year: 20:16 → 20:45 ET (21:16 → 21:45 in US winter); every weekday with |surprise| > 1 sd → ≈ 80–120 trades/yr.
- data needed: 6A 1m full session (Databento ≈ $20; Asian hours are outside RTH) or HistData AUDUSD 1m (free, 2010–2026) for a CFD-priced test ($0); fix history: CFETS/PBoC pages (reachability not checked), FRED DEXCHUS daily noon-NY rate as a weak proxy.
- expected gross edge per trade: AUD 30-minute moves in Asian hours ≈ 10–15 bp; a conditional tilt of 3–5 bp vs 6A RT 1.8 bp / CFD 1.4 bp RT → marginal.
- firm structure fit: overnight-session futures (6A) at every futures firm; FTMO intraday CFD; no news-window clause covers the PBoC fix (verify MFFU's Tier-1 list).
- nearest closed relative: D4 (intraday CFD rules across 19 CFDs, closed — generic rules, no fix); A-C05 (FX intraday momentum negative evidence — this is event-conditioned, not momentum); C-1-05 (Tokyo fix, a different fixing and currency).
- decay haircut: 0.7; splits at 2015-08-11 (fix reform), 2017-05 (counter-cyclical factor), 2022.
- plausibility of net Sharpe ≥ 1.5: low.
- original: yes
- LANE-12 TOP TEN: no

### C-12-15 Month-end multi-asset rebalancing, equity leg: short/long ES into the last trading day's close in proportion to the month's equity-minus-bond return (intraday twist on Harvey–Mazzoleni–Melone 2025)
- mechanism: balanced mandates (60/40, target-date, pensions) rebalance to fixed weights at month- and quarter-ends; Harvey, Mazzoleni & Melone (NBER w33554, 2025, https://www.nber.org/papers/w33554; cited by the sibling block C-1-02 which registers the bond leg) show the rebalancing demand, predictable from the month's equity-vs-bond performance gap, moves prices over the last days of the month and reverts afterwards. The execution is concentrated in the closing auction of the last trading day (MOC orders are how a passive mandate rebalances), so the equity leg's footprint belongs in ES 15:30 → 16:00 on the last trading day, direction = minus sign(equity − bond month-to-date return) — after a strong equity month the mandate sells equities into the close. The daily turn-of-month long bias (H0023, closed) is a different, unconditional calendar object.
- evidence: working paper (NBER 2025; daily data); own twist for the 30-minute close window and the signed trigger.
- evidence window: US and global 60/40 proxies ≈ 1997–2023 (HMM; window per sibling file, verify); ES last-day 15:30–16:00 untested.
- instruments: ES/MES; NQ secondary; FTMO US500 intraday or Swing (the HMM daily version holds 1–3 days around the turn).
- holding period and expected trades per year: 15:30 → 15:59 ET on the last trading day (12/yr, plus quarter-ends weighted 2×) when |equity − bond MTD return| > 2%; ≈ 8–12 trades/yr — a sleeve only; annual contribution at 1 MES per $5k of drawdown ≈ 10 × 10 bp × $25k notional ≈ $250 per account; worthless alone, cheap to add.
- data needed: ES 1m RTH (in hand, licence-held copy cross-check only; Databento ≈ $7); S&P and Treasury daily (free). $0–7.
- expected gross edge per trade: HMM's daily effect is tens of bp per event; a third landing in the final half hour = 5–15 bp vs 1.2 bp RT → passes on paper.
- firm structure fit: intraday futures (15:30–15:59); FTMO Swing for the multi-day version (swap per night).
- nearest closed relative: H0023 (turn-of-month, closed; unconditional long); H0006 (last-half-hour momentum; this is a signed calendar flow, not momentum); C-1-02 (bond leg of the same paper — register as one two-leg row if the Officer prefers).
- decay haircut: 0.5 (published); splits at 2008, 2020-03, 2022 (bond bear market changed the rebalancing sign distribution).
- plausibility of net Sharpe ≥ 1.5: low (12 events/yr).
- original: no (published mechanism; the close-window construction is the only twist)
- LANE-12 TOP TEN: no

### C-12-16 Defined-outcome / collar roll days: JHEQX quarter-end collar and the monthly buffer-ETF resets into the close
- mechanism: JPMorgan Hedged Equity (JHEQX, ≈ $20bn+) rolls an SPX put-spread collar on the last trading day of each quarter, executed in the afternoon; dealers hedge the new strikes with ES into the close (Bloomberg 2025-03-11 and 2025-06-30 pieces, https://www.bloomberg.com/news/articles/2025-06-30/jpmorgan-fund-s-expiring-s-p-options-position-draws-market-focus; SpotGamma explainer https://spotgamma.com/jpm-collar-explained/; snippets 2026-11-04). The monthly-series buffer ETFs (Innovator, First Trust, AllianzIM; tens of billions) reset their option packages at the close of the last business day of each month. Direction is computable from where SPX sits relative to the expiring strikes at 14:00 ET (e.g. above the old put strike → the expiring put's delta is ≈ 0 and the dealers who were long futures against it buy back less … the sign depends on the strike geometry, which is public on the day). Rule: on these days, compute the dealer delta change implied by the published strikes at 14:00 and trade its sign 15:00 → 15:59.
- evidence: press and practitioner commentary; no measured close effect found; own construction.
- evidence window: none; JHEQX collar since ≈ 2013, prominent since 2020.
- instruments: ES/MES; FTMO US500 intraday.
- holding period and expected trades per year: 15:00 → 15:59 ET; 4 quarter-ends + 8 other month-ends = 12 events/yr (a sleeve; annual contribution ≈ $200–400 per account at micro size).
- data needed: ES 1m RTH (in hand / ≈ $7); strike history from the fund's filings and press (free, labour).
- expected gross edge per trade: a $20bn collar roll moves dealers' net delta by a few $bn → 5–20 bp into the close on the quarter days; passes the screen if the sign is right.
- firm structure fit: intraday futures; coincides with C-12-15 (month-end rebalancing) and C-1-01 (Treasury strike) on the same afternoons → model the interaction, or register as one "last-day-of-quarter close" row.
- nearest closed relative: H0006/H0019 (last-half-hour momentum/GEX, closed); A-C26/C-1-10 (pinning).
- decay haircut: 0.5 (widely discussed since 2021); splits at 2020, 2023.
- plausibility of net Sharpe ≥ 1.5: low (12 events/yr; sign uncertainty).
- original: yes (as a rule; the commentary is not a test)
- LANE-12 TOP TEN: no

### C-12-17 Large overnight gaps as margin-call liquidation: continuation 09:30 → 10:30 on gaps > 2σ, gated on the micro-contract footprint (opposite sign and new mechanism relative to the closed gap-fade H0012/H0017)
- mechanism: after an overnight gap larger than the maintenance-margin buffer of a typical retail account (ES 2σ ≈ 1.5–2% ≈ $4–6k per ES, i.e. the whole day-trading margin at most retail FCMs), the gap-side losers receive margin calls due by a morning deadline and are liquidated through the first hour by brokers and by prop-firm risk engines (trailing drawdown on unrealized P&L) → forced flow in the gap direction 09:30–10:30, after which the move reverts. The inherited gap *fade* was tested (H0012/H0017: SPY net −0.122R, t −3.35) and lost — weak evidence that the opposite sign exists net of costs on the days it was tested, but a sign flip after the fact is exactly the post-hoc choice the board forbids; what is new here is (a) the trigger (gaps beyond the margin buffer, not 1 × gap sd), (b) the mechanism and its footprint (micro share and MES/ES volume ratio in 09:30–10:00), (c) the exit at 10:30, not the prior close.
- evidence: own idea; the inherited negative result of the fade is the only data point (`registry.csv` H0012/H0017).
- evidence window: H0012 tested SPXUSD 2010–2018 IS and SPY 2019–2025 OOS for the fade; the continuation with a margin trigger is untested.
- instruments: ES/MES, NQ/MNQ; FTMO US500/US100 intraday.
- holding period and expected trades per year: 09:31 → 10:30 ET, then optional fade 10:30 → 12:00; gaps > 2σ occur ≈ 10–20 days/yr in ES, ≈ 20–30 in NQ → a sleeve (annual contribution small; the fade variant of the day doubles the count).
- data needed: ES 1m RTH (in hand, cross-check status) + MES 1m RTH (≈ $7) for the footprint.
- expected gross edge per trade: continuation of 0.3–0.5% on a 2% gap day = 30–50 bp vs 1.2 bp RT → passes easily if it exists; the danger is the sample (≈ 100 events in 8 years) and the sign-flip optics.
- firm structure fit: intraday futures; MFFU news windows (08:30 releases precede the open; 10:00 ET releases inside the window → skip those days at MFFU).
- nearest closed relative: H0012/H0017 (overnight-gap fade, CLOSED) — this is declared as adjacent; the Pre-registration Officer must rule whether the margin-buffer trigger + micro footprint is "a materially new mechanism" (the common brief's condition); if not, decline.
- decay haircut: 0.7; splits at 2019-05 (micro launch), 2020-03.
- plausibility of net Sharpe ≥ 1.5: low (event-sparse; adjacency risk).
- original: yes (mechanism and trigger), with the adjacency stated
- LANE-12 TOP TEN: no

### C-12-18 Sunday 18:00 ET Globex reopen: the weekend-news repricing overshoot by a thin crowd, faded 18:15 → 20:00 (ES/NQ/GC/6E)
- mechanism: the Sunday reopen is the only session open where 65 hours of news is priced by a book with no US institutional depth: retail CFD and crypto-weekend positioning, Asian early flows and prop-firm "Sunday-evening start" traders set the first 15 minutes. Who is forced: weekend CFD holders whose brokers (and FTMO's weekend rules on Standard accounts) require flat before the close and re-open positions at 18:00; and hedgers of weekend crypto moves (BTC trades all weekend; ES does not). The first-15-minute move over-weights thin flow and should partly revert by the Asian cash opens (Tokyo 19:00/20:00 ET). Rule: fade the 18:00 → 18:15 move when it exceeds 1 × the Friday 15-minute sd and the BTC weekend return disagrees with it in sign (crypto as the weekend information proxy); exit 20:00 ET. The whole position is an overnight-session hold inside the futures-firm trading day.
- evidence: own idea; no study of the Sunday reopen found (lane-3 session-open work covers 02:00–03:00 ET and the 18:00→09:30 hold, not the Sunday first quarter-hour).
- evidence window: none.
- instruments: ES/MES, NQ/MNQ, GC/MGC, 6E/M6E; FTMO US500/XAUUSD (Sunday 23:05 CET opens: verify).
- holding period and expected trades per year: 18:15 → 20:00 ET Sundays; ≈ 50 Sundays × 2–4 roots ≈ 100–200 trades/yr.
- data needed: 1m full session (Sunday evening bars): ES ≈ $20, GC ≈ $20, 6E ≈ $20 — $60, heavy; cheaper first pass: HistData SPXUSD/XAUUSD/EURUSD 1m (free, CFD-priced, 2010–2026, includes Sunday evening) for the gross signal, Databento only after gross t > 3 (lane-9 style gate).
- expected gross edge per trade: 18:00–18:15 moves of 0.2–0.4% on news Sundays; a third reverting = 7–13 bp vs 1.2 bp RT (ES) / 1 bp (GC) → passes if it exists; 6E smaller.
- firm structure fit: overnight-session futures (all firms; inside one trading day); FTMO intraday CFD (Sunday evening = Monday 00:05 CET: the position crosses FTMO's 00:00 CE(S)T daily-loss reset — fine, no swap until the next midnight).
- nearest closed relative: H0012/H0017 (gap fade at 09:30; different session and crowd); D3 (crypto, used only as a signal here, not traded).
- decay haircut: 0.7; splits at 2017-12 (CME BTC futures), 2020-03, 2024.
- plausibility of net Sharpe ≥ 1.5: low.
- original: yes
- LANE-12 TOP TEN: no

### C-12-19 Dealer charm flow: midday-to-afternoon drift in the direction of the dealers' decaying hedge on quiet days (gated on daily GEX sign) — practitioner folklore, registered as a kill-test
- mechanism: as expiry approaches, OTM option deltas decay toward zero (charm); dealers unwind the futures hedges against those deltas through the session, "most aggressive in the final two hours" (SpotGamma, https://spotgamma.com/vanna-and-charm-explained/, https://support.spotgamma.com/hc/en-us/articles/15246596430483-Charm, snippets 2026-11-04). With customers net long puts (the usual state when GEX is positive and the market is above the put wall), dealers are short puts, hedged short futures; charm shrinks the put delta → dealers buy back futures through the day → a drift up on quiet, positive-GEX days that is strongest on Fridays and 0DTE-heavy days, and reverses sign when customers are net long calls. Competing flows (gamma, vanna) dominate when the underlying moves > 0.5% intraday (Convex glossary, same snippets), hence the "quiet day" gate. Rule: if |09:30→11:00 return| < 0.25% and yesterday's SqueezeMetrics GEX > its 60-day median, long ES 11:00 → 15:30; short when GEX is in its bottom quintile.
- evidence: practitioner blogs (no test, no code); own gate construction; SqueezeMetrics GEX daily 2011–2026 is in hand (free).
- evidence window: none (folklore).
- instruments: ES/MES; FTMO US500 intraday.
- holding period and expected trades per year: 4.5 hours; ≈ 80–120 quiet days/yr.
- data needed: ES 1m RTH (in hand / ≈ $7); GEX daily (in hand). $0–7.
- expected gross edge per trade: a persistent 3–5 bp drift over 4.5 hours vs 1.2 bp RT → passes the screen if real; the Red Team will note it is indistinguishable from "long on quiet up-days" unless the GEX-quintile sign flip holds.
- firm structure fit: intraday futures (11:00 → 15:30 ET); MFFU news windows (10:00 ET releases precede the entry).
- nearest closed relative: H0019 (GEX-conditioned last-half-hour momentum, CLOSED) — different window (midday, not the last half hour) and a drift, not momentum; C-4-05 (gamma regime switch, momentum vs reversal) — a different prediction (level drift vs autocorrelation). The Officer may still call it H0019-adjacent; it is listed so the folklore gets one honest kill-test rather than a hundred informal ones.
- decay haircut: 0.5; splits at 2022-05 (daily 0DTE), 2024.
- plausibility of net Sharpe ≥ 1.5: low.
- original: no (practitioner-described mechanism; the gated rule is the only construction)
- LANE-12 TOP TEN: no

### C-12-20 Round-number stop and take-profit clusters (Osler 2003) on gold and index futures at 1-minute resolution: reversal at the round number, acceleration just beyond it
- mechanism: Osler (JF 58(5) 2003, 1791–1819, https://econpapers.repec.org/RePEc:bla:jfinan:v:58:y:2003:i:5:p:1791-1819; NY Fed SR 125 https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr125.pdf, snippets 2026-11-04) shows from a dealing bank's order book that take-profit orders cluster *on* round numbers (→ reversals there) and stop-loss orders cluster *just beyond* them (→ trends accelerate once crossed): the two technical-analysis predictions with a microstructural cause. The modern retail-CFD and prop crowd places stops the same way (the inherited hypotheses.py lists A08 "levels at round numbers suffer from order accumulation" and C11 "proximity to a round number at entry" as untested). Twist: test on gold ($10/$50/$100 levels in XAUUSD and GC) and on ES/NQ (25/100-point levels), which Osler's FX sample does not cover, at 1-minute resolution: (a) first touch of a round level from below/above → fade for 15 minutes; (b) a 1-minute close beyond the level by > 0.05% → continuation for 15 minutes (the stop cascade), then fade.
- evidence: peer-reviewed (FX 1999–2000); own instruments and 1m rules; the mechanism is 23 years old and widely known → decay haircut at the floor.
- evidence window: USD/JPY, GBP/USD, EUR/USD orders 1999-09 → 2000-04 (Osler); gold and index futures untested at 1m in any source seen.
- instruments: GC/MGC, XAUUSD CFD (FTMO), ES/MES, NQ/MNQ; 6E/6B/6J as the published control.
- holding period and expected trades per year: 15–30 minutes; gold touches a $10 level several times a day → ≈ 500–1,500 events/yr (the win-rate > 58% path of the economics screen is the relevant one).
- data needed: HistData XAUUSD 1m 2010–2026 (free), GC 1m RTH (≈ $7), ES in hand; $0–7.
- expected gross edge per trade: Osler-type effects are a few bp; GC RT ≈ 0.6–1 bp, XAU CFD 2 bp RT → passes only with win rate > 58% over hundreds of trades; ES at 1.2 bp RT is marginal.
- firm structure fit: intraday futures; FTMO intraday CFD (XAUUSD); no clauses touched; minimum holds satisfied.
- nearest closed relative: H0001–H0004/H0010/H0016 (bot SMC/ICT "liquidity sweeps", closed) — those rules were pattern-based with discretionary levels; this is the published Osler mechanism at fixed round numbers; D4 (generic CFD rules, closed) did not test levels. Declared adjacent to the closed SMC family; the Officer rules.
- decay haircut: 0.5; splits at 2010 (algorithmic FX), 2019 (micro contracts).
- plausibility of net Sharpe ≥ 1.5: low.
- original: no (Osler 2003); new instruments only
- LANE-12 TOP TEN: no

### C-12-21 Opening retail thrust: fade the 09:30–09:35 ET move when the micro-contract share of volume is in its top tercile (MES/MNQ vs ES/NQ)
- mechanism: the first five minutes of the cash session are where the prop-evaluation and retail-day-trading crowd enters (TJR-style opening plays, 5-minute ORB bots, "9:30 scalpers"); the inherited hypotheses.py lists A05 "entries in the first five minutes are inferior" as a belief never tested. The crowd's footprint is observable: micro contracts' share of equity-index volume is 40.5% of contracts overall (CME 2025), and should spike at 09:30–09:35; when the micro share is unusually high the opening move is retail-driven, uninformed, and absorbed by market makers who then let it revert. Rule: at 09:35:30 fade the 09:30 → 09:35 move if |move| > 0.15% and the micro share (MES/(MES + 10·ES) by contracts, or MES volume relative to its own 09:30–09:35 profile) is in its top tercile; exit 10:00 or at −1R. The control arm (bottom tercile of micro share) should show no reversal — a pre-registered contrast, which is the honest form of the test.
- evidence: own idea; retail-order-imbalance reversal is a published stock-level fact (Barber–Odean line of work; Boehmer–Jones–Zhang–Zhang JF 2021 on retail imbalance predicting returns — from memory, verify, not fetched), never at the futures/micro level.
- evidence window: none for futures; micro share observable 2019-05 → today.
- instruments: MES/ES, MNQ/NQ; secondary M2K/RTY.
- holding period and expected trades per year: 25 minutes; ≈ 80–120 trigger days/yr per root.
- data needed: Databento 1m RTH ES + MES (≈ $14) and/or NQ + MNQ (≈ $14); the ratio needs both roots. Shared with C-12-03.
- expected gross edge per trade: a 0.3% opening thrust that reverts by a third = 10 bp vs 1.2 bp RT → passes; the top-tercile contrast decides whether the footprint carries information.
- firm structure fit: intraday futures at all firms; MFFU news windows: 10:00 ET releases are after the exit; skip days with 09:30–09:35 Tier-1 events (none normally).
- nearest closed relative: H0020 (5-minute ORB on NQ/SPY, closed — a breakout *with* the first 5 minutes; this fades them, conditional on the crowd footprint); H0012/H0017 (gap fade at 09:31, closed — the overnight gap, not the first-5-minute thrust; declared adjacent in window).
- decay haircut: 0.7; splits at 2019-05, 2022-05, 2024.
- plausibility of net Sharpe ≥ 1.5: low; the footprint contrast is cheap and informative for every other micro-share block.
- original: yes
- LANE-12 TOP TEN: yes (rank 4)

### C-12-22 The prop news-ban cohort at 08:30 ET: forced flat at 08:28, forced re-entry at 08:33, in the roots where the macro family is not closed (GC, 6E, ZN, CL)
- mechanism: MFFU Rapid/Pro funded accounts may hold no position or resting order within ±2 minutes of the firm's Tier-1 releases (CPI, NFP, PCE, etc.), Lucid Daily treats red-folder news as a breach, FTMO Standard bans ±2 minutes (`firms-2026-10-11.md`). A sizeable retail cohort therefore flattens by 08:28 and re-enters at 08:33, chasing the release direction. The 08:33–08:35 re-entry is late, crowded and uninformed → fade it 08:35 → 09:00 in the roots where the inherited macro family did not test (E2 closed FOMC/CPI/NFP/ISM/PCE in ES/NQ only; lane 2 covers ZN/ZB for FOMC and auctions). Footprint: micro share (MGC/GC, M6E/6E, MCL/CL) collapsing at 08:28–08:32 and spiking at 08:33–08:35.
- evidence: own idea; firm clauses are the evidence of the forced timing; E2's result (best t 1.09, opposite sign) is the cautionary tale for anything 08:30-shaped.
- evidence window: none; the prop news-ban rules date from ≈ 2023.
- instruments: GC/MGC, 6E/M6E, CL/MCL, ZN (no micro); FTMO XAUUSD/EURUSD intraday on Swing (exempt from the ban) — an FTMO Swing account is precisely the counter-side the rules create.
- holding period and expected trades per year: 08:35 → 09:00 ET on Tier-1 release days (≈ 60–80/yr) × 3–4 roots ≈ 200–300 trades/yr.
- data needed: 1m full session for GC, 6E, CL, ZN (08:30 is outside RTH files → ≈ $20 each = $80, over the budget together; HistData XAUUSD/EURUSD 1m free for the CFD-priced first pass; Databento only after gross t > 3).
- expected gross edge per trade: the 08:33–08:35 chase overshoot in gold is often 0.1–0.3%; a third reverting = 3–10 bp vs 1 bp RT (GC) / 1.2 bp (6E) → passes; ZN 3 bp RT marginal.
- firm structure fit: FTMO Swing (exempt from the ban) or Topstep/Bulenox (allow news trading) — the firms whose rule *creates* the crowd (MFFU Rapid/Pro, Lucid Daily) cannot trade it; Topstep "not at maximum size" clause touched.
- nearest closed relative: E2-01..12 (macro events intraday ES/NQ, CLOSED) — different roots, a crowd-timing trade at 08:33 rather than a release-direction trade; the Officer must accept the distinction (the common brief closes ES/NQ macro families, not GC/6E/CL).
- decay haircut: 0.7; splits at 2023 (news-ban rules), 2025.
- plausibility of net Sharpe ≥ 1.5: low.
- original: yes
- LANE-12 TOP TEN: yes (rank 10: the only block where a firm rule literally manufactures the counterparty)

### C-12-23 Failed 30-minute opening-range breakout: the ORB crowd's stops as the counterparty (fade a break that closes back inside within 10 minutes)
- mechanism: the opening-range breakout is the most-taught retail futures setup (Crabel 1990; Zarattini–Aziz 2023; prereg_orb30 is the org's own version). Its practitioners enter on the break with stops at the range midpoint or opposite edge. When a break fails (price closes back inside the range within k minutes), the crowd's stops become a one-directional order cluster from the midpoint to the opposite edge; the failed-break move therefore tends to travel through the range to the opposite edge. Rule: 09:30–09:59 range; first 1-minute close outside; if within 10 minutes a 1-minute close is back inside → enter against the original break at that close, target the opposite range edge, stop at the break extreme; one trade per day.
- evidence: own idea (practitioner lore "failed breakouts are the best breakouts" exists without code); the prereg_orb30 family's own future results (C-11-01) are the natural paired test — register the pair so that the ORB and its failure are read together.
- evidence window: none.
- instruments: ES/MES, NQ/MNQ; FTMO US500/US100 intraday; GC/CL secondary.
- holding period and expected trades per year: 10 minutes to 3 hours; ≈ 60–100 trades/yr per root (failed breaks are ≈ 40% of break days).
- data needed: ES 1m RTH (in hand / ≈ $7); SPXUSD 1m 2010–2018 (in hand, free) for the in-sample as in prereg_orb30.
- expected gross edge per trade: target = range width (median ≈ 15–25 ES pt) vs stop ≈ 5–8 pt; at 0.6 pt RT the cost is < 0.1R → passes the screen on structure; the win rate is the unknown.
- firm structure fit: intraday futures; FTMO intraday CFD; no clauses touched.
- nearest closed relative: H0020 (5-minute ORB, CLOSED; different range length and the opposite trade); prereg_orb30 (lane 11, C-11-01; the same range, the opposite trade on a subset of days); H0005/H0011 (noise-area momentum, closed).
- decay haircut: 0.7; splits at 2019, 2022-05.
- plausibility of net Sharpe ≥ 1.5: low.
- original: yes (as a tested rule with the crowd mechanism)
- LANE-12 TOP TEN: no

### C-12-24 Corporate buyback desks (Rule 10b-18) as price-sensitive afternoon buyers: ES dip-buying 13:00 → 15:50 on down days outside the earnings blackout
- mechanism: S&P 500 companies repurchase ≈ $900bn–1tn a year, executed by broker desks under 10b-18's safe harbour (≤ 25% of ADV, no purchases in the last 10 minutes, price ≤ the highest independent bid), typically as VWAP/participation programs that are *price-sensitive* (desks buy more on down days). About 5 weeks before each earnings date most issuers are in blackout (unless on a 10b5-1 plan). So on down days outside blackout there is an extra, mechanical, price-insensitive-to-information buyer whose participation ends at 15:50; on down days inside blackout he is absent. Index-level blackout returns show no clear effect (Alpha Architect 2019 on Bernstein data, https://alphaarchitect.com/2019/01/buyback-blackout-periods-do-not-negatively-impact-market-performance/, snippet 2026-11-04) — that is the daily, unconditional test; the intraday conditional contrast (down days, 13:00–15:50, in vs out of blackout) is not published. Blackout share is computable from the in-hand Nasdaq earnings calendar (2008+, 231,682 rows) weighted by S&P membership.
- evidence: practitioner (desk behaviour, 10b-18 text) + a negative daily study; own intraday construction.
- evidence window: Bernstein daily study ≈ 2010–2018 (per snippet; verify); intraday untested.
- instruments: ES/MES; FTMO US500 intraday.
- holding period and expected trades per year: on days with 09:30 → 13:00 return < −0.5% and blackout share < 30%: long 13:00 → 15:50; ≈ 40–60 trades/yr, with the in-blackout down days as the pre-registered control arm.
- data needed: ES 1m RTH (in hand / $7); earnings calendar + S&P membership (in hand, free).
- expected gross edge per trade: if buyback desks add ≈ 2–4% of ADV on those afternoons the square-root impact is ≈ 5–10 bp vs 1.2 bp RT → passes the screen on paper.
- firm structure fit: intraday futures (13:00 → 15:50 ET); MFFU 14:00 FOMC days excluded; no minimum-hold issue.
- nearest closed relative: G2 (buy-the-dip index CFD, daily, closed) — this is intraday, conditional on a named buyer's calendar, with a control arm; H0006 (last-half-hour momentum) — the window ends at 15:50 on purpose.
- decay haircut: 0.5 (the blackout calendar is public); splits at 2018 (tax-reform buyback surge), 2023 (1% excise tax).
- plausibility of net Sharpe ≥ 1.5: low.
- original: yes
- LANE-12 TOP TEN: yes (rank 6: a counterparty with a legal clock)

### C-12-25 First Notice Day liquidation of non-deliverable longs in GC/SI/CL: the front month's settlement-window weakness in the three days before FND
- mechanism: speculators who cannot take delivery (retail, most CTAs, the ETFs that hold futures) must exit the expiring month before First Notice Day; their exit is a roll (sell front, buy next) executed mostly at settlement (TAS orders) over the last 3–5 days, and in retail's case an outright sale on the last permitted day (prop firms force the roll a day or two before FND — verify each firm's rule). Unlike the index roll (A-C17, Goldman roll, closed as decayed after 2004) this is not a published date window shared by a few index funds but a diffuse deadline that binds the long side only (shorts are commercials who can deliver). Footprint: the front-vs-second spread weakens into the 13:30 ET settlement on FND−3 … FND−1, and the outright front shows a settlement-window dip that the second month does not. Rule (outright, since spreads are awkward at prop firms): short the front month 13:00 → 13:30 ET on FND−2 and FND−1 in GC/SI; long the second month as the control; CL at 14:00–14:30.
- evidence: own idea; the Goldman-roll literature (Mou 2010; per A-C17) is the negative relative; no FND-specific minute study found.
- evidence window: index-roll studies ≈ 2000–2010 (Mou; closed); FND retail roll untested.
- instruments: GC/MGC, SI/SIL, CL/MCL (front and second month); FTMO XAUUSD is spot-priced (no roll) → futures only.
- holding period and expected trades per year: 30 minutes; GC has 6 delivery months (Feb/Apr/Jun/Aug/Oct/Dec) × 2 days, SI 5 × 2, CL 12 × 2 → ≈ 46 events/yr (a sleeve).
- data needed: GC, SI, CL 1m RTH for two contract months (≈ $7 per root-month set → ≈ $42); FND calendar free.
- expected gross edge per trade: a 5–10 bp settlement dip in the front on roll days vs GC 0.6–1 bp RT → passes if it exists; CL 4 bp RT marginal.
- firm structure fit: intraday futures; check whether the firm permits trading the expiring month on FND−1 (Topstep/MFFU roll rules — Rules Keeper).
- nearest closed relative: A-C17 / "Goldman-roll front-running post-2004" (negative evidence) — different population (all non-deliverable longs, not index funds) and a settlement-window footprint rather than a 5-day window; declared adjacent.
- decay haircut: 0.5; splits at 2004 (index roll crowding), 2020-04.
- plausibility of net Sharpe ≥ 1.5: low (very low).
- original: yes (with adjacency to a negative-evidence family)
- LANE-12 TOP TEN: no

### C-12-26 Index-expiry settlement auctions: ES quad-witching SOQ (09:30 ET) and DAX futures expiry (13:00 CET Xetra auction) — post-settlement reversal of the auction push
- mechanism: cash-settled index futures and AM-settled index options settle on an opening (SPX/ES quarterly: the Special Opening Quotation from each component's opening print on the third Friday) or an intraday auction (Eurex DAX futures/options: the Xetra intraday auction at 13:00 CET on the third Friday). Arbitrageurs unwinding cash-futures baskets and option hedgers must trade *in the auction*, which pushes the settlement away from fair value; the push reverts afterwards. Stoll & Whaley (1987, 1990 J. Business 63(1) S165–S192, https://econpapers.repec.org/RePEc:ucp:jnlbus:v:63:y:1990:i:1:p:s165-92; 1991 on the move of settlement to the open; snippets 2026-11-04) documented expiration-day volume and reversal effects whose size shrank after settlement moved to the open; the practitioner record for recent years is mixed (Seasonax 2004–2019: low volatility on expiry days; a 2021–present note: expiry Fridays average −0.36%). Rule: ES — fade the 09:30 → 09:35 move on quad-witching Fridays from 09:35 to 10:00 (the SOQ hedging unwind); GER40 CFD — fade the 12:55 → 13:01 CET move from 13:02 to 13:30 CET on Eurex expiry days.
- evidence: peer-reviewed (1980s–1990s US); practitioner for recent years; own two-market construction. "Bare OPEX" negative evidence applies to day-level biases, not to a 25-minute auction-unwind window with a mechanism.
- evidence window: US 1984–1989 (Stoll–Whaley); DAX untested in any source seen; modern ES untested at the 5-minute scale.
- instruments: ES/MES; FTMO GER40 (intraday) for the Eurex leg; NKD/JP225 and HK50 are in C-12-27.
- holding period and expected trades per year: 25–30 minutes; 4 US + 12 DAX (monthly index options; quarterly futures) = 16 events/yr → a sleeve; annual contribution at micro size ≈ $100–300 per account.
- data needed: ES 1m RTH (in hand / $7); GRX/EUR 1m from HistData (free, 2010–2026).
- expected gross edge per trade: auction pushes of 0.2–0.5% in DAX at 13:00 on expiry days are visible on charts; a third reverting = 7–17 bp vs 0.8–1 bp/side CFD → passes; ES 09:30 push smaller.
- firm structure fit: intraday futures; FTMO intraday CFD; no news windows.
- nearest closed relative: "bare OPEX / day-of-week" negative evidence (day-level); A-C26/C-1-10 (pinning, the day before); H0012/H0017 (09:31 gap fade, closed — the ES leg's window overlaps; the trigger is the SOQ day, not the gap).
- decay haircut: 0.5; splits at 1987 (US settlement moved to the open), 2020.
- plausibility of net Sharpe ≥ 1.5: low (16 events/yr).
- original: no (Stoll–Whaley); the DAX 13:00 CET leg is an untested twist
- LANE-12 TOP TEN: no

### C-12-27 Asian index settlement mechanics: Nikkei SQ morning (second Friday, 09:00 JST) and the HSI expiry day's all-session average settlement (second-last business day), traded in NKD/NIY and the JP225 / HK50 CFDs
- mechanism: (a) Osaka/CME Nikkei 225 futures settle on the Special Quotation = the opening prices of all constituents on SQ day (JPX, https://www.jpx.co.jp/english/derivatives/products/domestic/225mini/01.html; CME Nikkei fact card, snippets 2026-11-04) → the same opening-auction unwind as C-12-26, at 09:00 JST = 19:00/20:00 ET (inside the futures-firm trading day as an overnight-session trade). (b) HKEX settles Hang Seng futures at the *average of index quotations taken at five-minute intervals* over the whole last trading day (HKEX rules, https://www.hkex.com.hk/-/media/HKEX-Market/Services/Rules-and-Forms-and-Fees/Rules/HKFE/Rules/SIF_CS.pdf, snippet 2026-11-04) → expiry-day hedgers must trade a TWAP across the session, which (i) suppresses intraday drift on expiry day and (ii) front-loads any directional push into the morning (the earlier the push, the more 5-minute samples it moves). Rules: NKD — fade the 09:00 → 09:05 JST move 09:05 → 09:30 JST on SQ days (monthly incl. mini SQ; 12/yr); HK50 — on expiry day fade the 09:30 → 10:30 HKT move 10:30 → 16:00 HKT against the day's running average (12/yr).
- evidence: exchange rules for the mechanics; the settlement-method literature (Stoll–Whaley lineage, Hong Kong studies not fetched) for the direction; own rules.
- evidence window: none for these rules.
- instruments: NKD/NIY (CME, overnight session), FTMO JP225 and HK50 intraday CFDs.
- holding period and expected trades per year: 25 minutes (NKD) / up to 5.5 hours (HK50); 24 events/yr → a sleeve (annual contribution small).
- data needed: HistData JPX/JPY and HKX/HKD 1m (free, 2010–2026; CFD-priced); NKD 1m from Databento (≈ $20 full session) only after the free pass shows gross t > 3.
- expected gross edge per trade: SQ-morning pushes of 0.3–0.6% in the Nikkei are the folklore; a third reverting = 10–20 bp vs JP225 CFD 1.5 bp/side → passes; HK50 TWAP-day drift suppression is a sizing fact more than an edge.
- firm structure fit: overnight-session futures (NKD at firms listing it; 19:00–20:00 ET) and FTMO intraday CFD; no news-window clauses.
- nearest closed relative: none closed; C-3-04 (Nikkei night→day reversal, lane 3; different days and mechanism); C-1-09 (rebalance days).
- decay haircut: 0.5 (settlement effects are an old literature); splits at 2014 (JPX merger), 2020.
- plausibility of net Sharpe ≥ 1.5: low.
- original: yes (these two rules; the lineage is not)
- LANE-12 TOP TEN: no

### C-12-28 0DTE put-wall first touch: dealers' intraday hedging of the strike with the largest same-day put open interest as support (forward-collected free CBOE delayed OI; cannot be backtested)
- mechanism: distinct from pinning at expiry (C-1-10) and from the gamma-regime sign (C-4-05): on a positive-gamma day the strike holding the most 0DTE put OI is where dealers (short those puts) buy futures as price approaches it (their delta rises as the put goes ATM) — the "put wall" acts as intraday support on the *first* approach, and as an accelerant once broken with conviction (dealers' hedge flips with the sign of the local gamma). The level is computable at 09:35 ET from the free CBOE delayed SPX option chain (OI as of the prior day's close plus the morning's 0DTE listings; verify what the delayed feed shows). There is no free historical 0DTE OI-by-strike archive (CBOE DataShop is paid), so this is forward-collection only: a daily snapshot script from today builds the sample, and the rule can only be tested on data that does not yet exist — which is also its protection against overfitting.
- evidence: practitioner (SpotGamma, Menthor Q daily "put wall" levels, not fetched as evidence); peer-reviewed background on 0DTE and intraday volatility (Beckmeyer–Branger–Gayda 2023; Brogaard et al. 2024 — from memory, not fetched, verify); own rule.
- evidence window: none; forward-only from the collection start date.
- instruments: ES/MES; FTMO US500 intraday.
- holding period and expected trades per year: first touch within 0.1% of the wall after 10:00 ET → long for 30 minutes or to +0.3%; ≈ 100–150 touches/yr.
- data needed: CBOE delayed option chain snapshots (free, forward; a cron job at 09:35 and 12:00 ET); ES 1m (in hand / $7). $0–7.
- expected gross edge per trade: 5–15 bp bounces are the folklore; vs 1.2 bp RT passes if real.
- firm structure fit: intraday futures; FTMO intraday CFD; no clauses touched.
- nearest closed relative: H0019 (GEX last-half-hour, closed); A-C26/C-1-10 (expiry pinning); C-4-05 (gamma regime) — this is a *level* rule, not a regime or an expiry rule.
- decay haircut: 0.5 (levels are sold by several vendors daily); splits at 2022-05 (daily 0DTE), 2023 (0DTE ≈ 50% of SPX volume).
- plausibility of net Sharpe ≥ 1.5: low, and untestable before ≈ 2028 at the 8-year rule → listed for the forward-collection decision only (the collection costs nothing).
- original: no (vendor-described level; the pre-registered first-touch rule is the construction)
- LANE-12 TOP TEN: no

### C-12-29 Treasury buyback operations (since 2024-05): the 13:40–14:00 ET operation window and the 14:00 result print in ZN/ZB/UB
- mechanism: the Treasury's regular buyback program (liquidity-support and cash-management operations, tentative schedules published quarterly: https://home.treasury.gov/system/files/221/Tentative-Buyback-ScheduleQ32026.pdf; third-party tracker https://www.tftc.io/treasury-buybacks, snippets 2026-11-04; 64 operations and ≈ $230bn in 2026 to October; long-end operations "at least doubled" from 2026-09) buys off-the-run securities from primary dealers in a 20-minute window ending 14:00 ET with results right after. Dealers pre-position (buy off-the-runs, hedge short ZN/ZB/UB into the window) and unwind the hedge after the results: a predictable futures footprint — pressure 13:30 → 14:00 in the sector being bought, recovery 14:00 → 14:30 — on ≈ 50–70 scheduled days/yr. New program, new calendar, no literature (the auction-cycle literature, C-1-03, is the mirror image: issuance instead of purchase).
- evidence: Treasury schedule pages (primary); own idea; no study found (search 2026-11-04 found only schedules and trackers).
- evidence window: none; program exists since 2024-05 (≈ 2.5 years → fails the 8-year rule until ≈ 2032; listed as a calendar to collect and as a sleeve candidate later).
- instruments: ZN, ZB, UB (TN, ZF for the shorter buckets); no FTMO twin.
- holding period and expected trades per year: 13:30 → 14:00 (with the hedge) and 14:01 → 14:30 (against it); ≈ 50–70 operation days/yr × 2 legs.
- data needed: ZN/UB 1m RTH (≈ $7 each; shared with C-1-01/C-1-03); the Treasury schedule and results pages (free).
- expected gross edge per trade: a $4–6bn operation vs ≈ $150bn+ of daily ZN notional ADV ≈ 3–4% of ADV → 2–5 bp vs 3 bp RT (ZN), 5–6 bp (UB) → fails or marginal; the long-end (20–30y) operations against UB's thinner book are the only leg with a chance.
- firm structure fit: intraday futures (13:30–14:30 ET, before the 15:00 settlement); MFFU news windows: buyback results are not Tier-1 (verify).
- nearest closed relative: none closed; C-1-03 (auction-day inverted V) and C-1-12 (daily 4pm strike) are the lane-1 neighbours.
- decay haircut: 0.7; split at 2026-09 (size doubling).
- plausibility of net Sharpe ≥ 1.5: low (very low; cost-bound).
- original: yes
- LANE-12 TOP TEN: no

### C-12-30 The retail bar-close clock: synchronized indicator-driven orders at 5/15/30-minute boundaries in MES/MNQ, faded in the following minute
- mechanism: TradingView/NinjaTrader retail bots and alert-followers act on indicator values computed at bar closes (Supertrend, VWAP bands, EMA crosses on 5-/15-minute charts), so retail order arrival is lumpy at :00/:05/:15/:30 minute boundaries while institutional flow is not. The minute *after* a 15-minute boundary should carry an abnormal micro-contract volume burst and a small price move that reverts within 5 minutes, scaled by how many popular indicators flipped at that close (proxy: the 15-minute bar's close crossing its own 20-period EMA or the session VWAP). Rule: at :01/:16/:31/:46 when the prior 15-minute close crossed VWAP or EMA20 and micro share in the boundary minute is in its top tercile, fade the boundary minute's move for 5 minutes. Heston–Korajczyk–Sadka (JF 2010, half-hour periodicity in stock returns; cited in C-9-08) is the published ancestor at the 30-minute grain for stocks.
- evidence: own idea; HKS 2010 as background; no futures/micro test seen.
- evidence window: US stocks 2001–2005 (HKS); futures untested.
- instruments: MES/ES, MNQ/NQ.
- holding period and expected trades per year: 5 minutes; ≈ 2–6 signals/day → 500–1,500 trades/yr (the win-rate > 58% path).
- data needed: ES + MES 1m RTH (≈ $14, shared with C-12-03/21); a 1-second pilot (lane 9 rule: only after 1m gross t > 3) would show the first-10-second burst directly.
- expected gross edge per trade: 1-minute boundary moves of 1–2 ticks; a half-tick reversion vs 0.6 pt (2.4 ticks) RT → fails the screen unless executed passively (limit orders at the boundary, fill uncertainty) — honest expectation: a footprint study, maybe a timing overlay for other sleeves' entries (do not enter at :00; enter at :03), not a sleeve.
- firm structure fit: intraday futures; minimum holds satisfied; sim-fill clauses (tight brackets) touched if executed with 1-tick limits at MFFU/Topstep.
- nearest closed relative: H0021/H0022 (VWAP trend, closed — this is a boundary-reversal, not a trend); H0005/H0011 (noise-area momentum, half-hour entries, closed — opposite sign and a 1-minute horizon).
- decay haircut: 0.7; splits at 2019-05, 2023.
- plausibility of net Sharpe ≥ 1.5: low (very low); value is in the entry-timing overlay.
- original: yes
- LANE-12 TOP TEN: no

### C-12-31 Prop-firm forced roll days: every funded account must leave the expiring equity-index contract on the firm's roll date — the micro front/back spread push and the outright footprint at that minute
- mechanism: futures firms do not let sim accounts carry the expiring contract into its last days; each platform forces a roll on a fixed date (typically the Thursday/Friday before expiry week or the Monday of it, at a stated time — verify per firm, Rules Keeper), closing the expiring month and reopening the next. The crowd's roll is thus concentrated at a known minute, in micro contracts, and is executed as two outright orders (retail platforms rarely use the spread), so it pushes the expiring micro month against the next month for a few minutes (a calendar-spread footprint) and leaves an outright footprint from the asynchronous legs. Rule: trade the calendar spread (short expiring / long next if the crowd is net long, inferred from the day's micro share and sign) in the mini contract 5 minutes before the forced-roll minute, unwind 15 minutes after; or trade the outright reversal after the micro burst.
- evidence: own idea; firm roll rules from the platforms (Topstep/Tradovate: "positions in expiring contracts are liquidated at …" — exact clause to fetch; MFFU similar); no study.
- evidence window: none.
- instruments: ES/MES and NQ/MNQ calendar spreads (two contract months); 8 roll events/yr (4 ES + 4 NQ) → a sleeve at best; annual contribution at 1 spread per account ≈ tens of dollars → honestly a footprint study.
- data needed: MES + ES 1m for two months around each roll (Databento by raw symbol; ≈ $14 for a year of two months per root; cheaper with 1-week slices).
- expected gross edge per trade: spread moves of 1–3 ticks (0.05 pt = $2.50 each in ES) vs 2 ticks RT on the spread → fails the screen unless the push is ≥ 4 ticks; outright leg sub-point.
- firm structure fit: intraday futures; spreads allowed at Topstep/MFFU (verify); the firm doing the forcing is the one whose crowd it is.
- nearest closed relative: none.
- decay haircut: 0.7; split at 2023 (firm scale).
- plausibility of net Sharpe ≥ 1.5: very low.
- original: yes
- LANE-12 TOP TEN: no

### C-12-32 Trade-at-Settlement (TAS) instrument prints as the direct read of settlement-targeting flow: TAS net volume by minute → the 14:28–14:30 ET CL (and GC/NG) settlement push and the post-settlement reversal
- mechanism: CME lists TAS instruments (trades priced at the day's settlement ± a few ticks) for CL, NG, GC, SI and others; index rollers, ETFs (USO/UNG/BOIL at their NAV time) and hedgers who want the settlement price use TAS; the sign of TAS prints (+1 tick = willing to pay above settle = urgent buyer) and their volume are visible *before* the settlement window and are a cleaner flow read than the settlement bar's BVC (C-9-09). Databento GLBX carries TAS as separate symbols (e.g. `CLZ6 TAS`-style raw symbols; exact naming per the dataset's definitions — check the free `definition` schema sample before buying), so the TAS minute bars are a $7-class purchase. Rule: at 14:15 ET, if net TAS volume (buy-side TAS minus sell-side, signed by the tick offset) over 09:00–14:15 is in its top/bottom decile, trade the outright in that direction 14:15 → 14:29 and fade it 14:31 → 15:00.
- evidence: own idea; CME TAS rules (public); the index-roll and LETF settlement literature (A-C17 negative; C-1-06) as background; no TAS-flow study seen.
- evidence window: none.
- instruments: CL/MCL (TAS most used), NG/MNG, GC/MGC; FTMO USOIL/NATGAS/XAUUSD intraday for the counter-side.
- holding period and expected trades per year: 15 + 30 minutes; ≈ 50–80 decile days/yr per root.
- data needed: Databento ohlcv-1m for the TAS symbols + outright (CL ≈ $7 + TAS ≈ $7; NG/GC same) → ≈ $28–42; verify TAS symbology in the free definitions first.
- expected gross edge per trade: settlement pushes of 10–30 bp in CL on roll days vs 4 bp RT → passes; the fade leg likewise.
- firm structure fit: intraday futures (14:15–15:00 ET); EIA Wednesdays excluded at MFFU (10:30 release is hours earlier, no clash); FTMO intraday CFD.
- nearest closed relative: A-C17 (Goldman roll, negative post-2004 — this reads the flow directly rather than assuming the calendar); C-9-09 (settlement-bar BVC proxy; this is the better instrument for the same mechanism — register as its data-upgrade variant, one count).
- decay haircut: 0.7; splits at 2009 (TAS expansion), 2020-04.
- plausibility of net Sharpe ≥ 1.5: low.
- original: yes
- LANE-12 TOP TEN: no

### C-3-07 Weekday 18:00 ET Globex reopen: fade the 18:00 → 18:05 repricing of the 17:00–18:00 maintenance hour (ES/NQ/GC/6E), an overnight-session hold inside one firm day
- mechanism: the one-hour daily halt (17:00–18:00 ET) accumulates after-hours earnings, Asian macro prints and the 16:30 API (Tuesdays) with no CME price; the 18:00 reopen prints that information through a thin book populated by Asian early flows and retail re-entries (and, on Tuesdays, energy desks repricing API). The first-5-minute move overshoots and partly reverts by the Tokyo open (19:00/20:00 ET). Who is forced: nobody strictly — retail CFD and prop accounts that were flattened at 16:08–16:59 and re-enter on the reopen are the thin crowd; the Sunday version (C-12-18) has the bigger news load. Rule: fade the 18:00 → 18:05 move when |move| > 1.5 × the 16:30–17:00 5-minute sd; exit 19:30 ET.
- evidence: own idea; lane-3 sibling blocks cover 02:00–03:00 ET and the 18:00 → 09:30 hold, not the reopen print.
- evidence window: none.
- instruments: ES/MES, NQ/MNQ, GC/MGC, 6E/M6E; FTMO US500/XAUUSD (00:00–01:00 CET reopen, verify hours).
- holding period and expected trades per year: 85 minutes; ≈ 80–150 trigger days/yr per root.
- data needed: full-session 1m (ES ≈ $20; GC ≈ $20); free first pass on HistData SPXUSD/XAUUSD 1m (CFD-priced; includes 18:00 ET).
- expected gross edge per trade: 18:00–18:05 moves of 0.1–0.3%; a third reverting = 3–10 bp vs 1.2 bp RT → passes on the top days.
- firm structure fit: overnight-session futures at all firms (inside one trading day); FTMO intraday CFD; no news windows (Asian releases are not on the Tier-1 lists; verify).
- nearest closed relative: H0012/H0017 (gap fade at 09:30, closed; different session); C-12-18 (Sunday sibling).
- decay haircut: 0.7; splits at 2020-03, 2024.
- plausibility of net Sharpe ≥ 1.5: low.
- original: yes

### C-9-10 Micro-vs-mini signed-flow divergence: BVC on micro bars (retail) against BVC on mini bars (institutional) as a 5–30 minute reversal signal
- mechanism: the same minute's signed flow can be computed separately for the micro and the mini contract (both have their own 1-minute OHLCV); when micro flow is strongly one-sided while mini flow is flat or opposite, the move is retail-driven and should revert; when both agree it is informed and should continue. This is the signed, cross-contract version of the micro-share state variable (C-6-06) and the retail counterpart of C-5-15 (ES-vs-NQ flow divergence). Rule: z-score of (BVC_micro − BVC_mini) over the last 10 minutes; fade when |z| > 2 and mini BVC has the opposite sign; horizon 15 minutes.
- evidence: own idea; BVC validity per the microstructure scout (C-9-01, Andersen–Bondarenko critique applies); retail-order-imbalance reversal is a stock-level fact (Boehmer et al. 2021, from memory, verify).
- evidence window: none; micro contracts since 2019-05.
- instruments: MES/ES, MNQ/NQ, MGC/GC, MCL/CL.
- holding period and expected trades per year: 15 minutes; ≈ 300–800 signals/yr per root.
- data needed: 1m RTH for each pair (≈ $14 per pair; ES+MES and NQ+MNQ first = $28; shared with C-12-03/21/30).
- expected gross edge per trade: a 2–4 tick reversion vs 2.4 ticks RT (ES) → only with win rate > 58% over hundreds of trades; MGC (tick $1) cheaper per unit.
- firm structure fit: intraday futures; minimum holds satisfied; no clauses.
- nearest closed relative: none closed; C-9-01/C-9-06 (BVC/CLV reversal on one contract) — this is the cross-contract contrast; C-5-15 (cross-root flow divergence).
- decay haircut: 0.7; split at 2019-05, 2022.
- plausibility of net Sharpe ≥ 1.5: low.
- original: yes

### C-6-06 The retail-crowd state variable: micro-contract share of volume by minute (MES/ES, MNQ/NQ, M2K/RTY, MGC/GC, MCL/CL, M6E/6E, MBT/BTC) as a cross-root gate and sizing input for every sleeve
- mechanism: CME micro contracts are 1/10 the mini and are traded overwhelmingly by retail and prop accounts (CME frames their 2025 growth as "the retail ecosystem"; 40.5% of equity-index contracts in 2025). The minute-level micro share relative to its time-of-day profile is a free-of-interpretation measure of how retail-driven the current tape is, available in every root with a micro twin. Uses, each pre-registrable as an overlay (not a sleeve): (i) breakout/trend sleeves inactive when the breakout minute's micro share is in the top decile (retail-driven breakouts fail — hypothesis, not fact); (ii) fade sleeves active only then; (iii) a cross-root "retail concentration" index (fraction of roots with micro share above profile) as an inactivity rule for the whole book on days retail dominates (e.g. meme-driven sessions). The same variable is the trigger in C-12-03, C-12-21, C-12-30 and C-9-10; registering it once as a construction avoids four ad-hoc definitions.
- evidence: own idea; CME volume facts (links in C-12-01).
- evidence window: none; 2019-05 → today.
- instruments: the seven pairs above.
- holding period and expected trades per year: n/a (overlay); it changes the trade count of the sleeves it gates.
- data needed: 1m RTH for the pairs (≈ $14 per pair; a $28 start with ES/MES and NQ/MNQ; the full set $98 is over the ceiling → not all at once).
- expected gross edge per trade: n/a; the pre-registered success criterion is a Sharpe gain ≥ 0.2 on the gated sleeve at 2 × costs, or a measurable footprint contrast (top vs bottom tercile) with t > 3.
- firm structure fit: any (overlay).
- nearest closed relative: none; C-9-02/C-9-03 (VPIN as a gate), C-7-04 (regime detectors as gates) are the methodological siblings.
- decay haircut: 0.7; split at 2019-05, 2022-05.
- plausibility of net Sharpe ≥ 1.5: low as a standalone (it is not one); unknown as a gate — the honest word.
- original: yes

### C-7-06 Clock anchoring and the DST-mismatch weeks: anchor every session-based rule to the clock of the flow that causes it, and use the 2–3 mismatch weeks per half-year as the identification test
- mechanism: US DST starts the second Sunday of March and ends the first Sunday of November; the EU/UK switch on the last Sundays of March and October; for ≈ 2–3 weeks a year (≈ 15–20 trading days) London is 4 hours ahead of New York instead of 5. Every London-clock flow (European cash open 08:00 London, WMR fix 16:00 London, Platts window 16:00 London, LBMA auctions 10:30/15:00 London, Eurex expiry 13:00 CET) shifts by one hour in ET during those weeks, while New-York-clock flows (09:30 open, 16:00 close, the 16:08/16:10/16:45 prop deadlines, 14:30 CL settlement) do not. A rule coded in ET for a London mechanism is mis-timed on those days (a known pitfall the inherited D4/lane-3 code may or may not have handled — check), and the mismatch weeks are a natural experiment: a candidate effect that moves with London in those weeks is a London flow, one that stays is a New-York flow, one that vanishes was never a flow. Register as (a) a construction standard for lanes 1–3 and 12 (store each rule's anchor clock) and (b) a pre-registered identification test for any lane-1/3/12 row that passes its first gate (the effect's ET timing must shift by 60 minutes in mismatch weeks, else the mechanism is misattributed).
- evidence: own idea; the calendar facts are public (timeanddate.com; not fetched); Bondarenko–Muravyev's hour-by-hour EU-open decomposition (C-3-02) is where the mis-timing would show.
- evidence window: n/a (method).
- instruments: all session-anchored rows.
- holding period and expected trades per year: n/a.
- data needed: none beyond the rows it audits ($0).
- expected gross edge per trade: n/a; it prevents a known loss (mis-timed entries on ≈ 7% of days for London-anchored rules).
- firm structure fit: any.
- nearest closed relative: none.
- decay haircut: n/a.
- plausibility of net Sharpe ≥ 1.5: n/a (not an edge; listed because the brief asks for constructions that other lanes depend on; the Director may move it to PARAMETERS.md instead of the candidate list).
- original: yes

### C-11-01 The never-run pre-registered S&P 30-minute opening-range breakout (prereg_orb30, 2026-10-06-0247): variants A/B/C exactly as written, then the OOS row only if A's D1 net bootstrap p5 > 0
- mechanism: the opening-range breakout family (Crabel 1990; Holmberg, Lonnbark & Lundstrom, Finance Research Letters 10(1) 2013, 27–33, crude oil; Zarattini & Aziz 2023, SSRN 4416622 — SSRN blocked, 403, per D-007) assumes early-session order flow from overnight information continues after the first 30 minutes. The org's own pre-registration (file: `~/quant-edge-inherited/pr4/skills/prop-fleet/agents/daily/2026-10-06-0247/builder/prereg_orb30.txt`, read 2026-11-04) fixes every rule: eligibility at 10:00 (≥ 25 of 30 bars), ORH/ORL from 09:30–09:59, first 1-minute close beyond the range in 10:00–11:59, entry next bar open ≤ 12:00, stop at the opposite edge, risk ≥ 1.0 pt, exit at the stop or the ≤ 15:59 close, cost 0.6 pt RT; A base, B 2R target, C narrow-range filter (W < median of the previous 20 sessions); D1 = SPXUSD 1m 2010-11 → 2018-12 in-sample; decision rule: the family earns an OOS row (ES 1m RTH 2019–2026) only if A's D1 net bootstrap p5 > 0; B and C cannot rescue it; no other range lengths, windows, targets or filters, ever. Nothing is changed here; the brief asks for the open direction as a concrete candidate, and the concrete candidate is the file. Twist offered separately, not inside this row: the failed-break fade (C-12-23) runs on the same range as its paired adversary.
- evidence: peer-reviewed (Holmberg et al. 2013, crude, ≈ 1983–2011), working paper (Zarattini–Aziz 2023, QQQ 2016–2023, +0.13R gross, no OOS), negative public replication (mql5 blog, snippet only, gross reproduced / net zero); the inherited 5-minute version failed (H0020: gross t 1.63, net −0.005R).
- evidence window: crude oil ≈ 1983–2011; QQQ 2016–2023 (5-minute); the 30-minute S&P version is untested; D1 2010–2018 is declared in-sample.
- instruments: SPXUSD 1m (D1, in hand, free) then ES/MES 1m RTH 2019–2026 (in-hand copies are LICENCE HOLD → Databento ES RTH ≈ $7 for the OOS row).
- holding period and expected trades per year: minutes to 6 hours; ≈ 150–200 trades/yr (one per eligible day with a trigger).
- data needed: $0 for D1; ≈ $7 for the OOS row if earned.
- expected gross edge per trade: Zarattini–Aziz's +0.13R gross on a 5-minute range; with a 30-minute range the median risk is ≈ 10–20 ES pt so 0.6 pt RT is 3–6% of 1R → passes the economics screen on structure; the family's record says the gross edge is the problem, not the cost.
- firm structure fit: intraday futures (entries by 12:00, exit 15:59 — inside every deadline; MFFU 10:00 ET news windows touch the trigger window: skip ±2 minutes); FTMO intraday CFD.
- nearest closed relative: H0020 (5-minute ORB, CLOSED), H0005/H0011 (noise-area momentum, closed) — the prereg itself states the differences (fixed 09:30–09:59 range, one entry, opposite-edge stop, 15:59 exit); the row is allowed because it was pre-registered before those closures and never run (board: "prereg_orb30 exists, never run").
- decay haircut: 0.5 (published family); splits at 2016 (Zarattini sample start), 2022-05 (0DTE).
- plausibility of net Sharpe ≥ 1.5: low — two ORB variants already died in this program; the row exists to close the question cleanly (count 3 per the prereg).
- original: no

### C-11-02 Futures-curve carry (Koijen–Moskowitz–Pedersen–Vrugt 2018) as an FTMO Swing commodity sleeve on CFD twins, curve shape from the two nearest CME contract months, swap charged honestly
- mechanism: the futures-curve slope (backwardation/contango) measures the expected return from holding the front contract if the curve does not move; long high-carry (backwardated) and short low-carry (contango) commodities earned positive returns across the KMPV sample (JFE 127(2) 2018, 197–225, https://econpapers.repec.org/RePEc:eee:jfinec:v:127:y:2018:i:2:p:197-225; NBER w19325; abstract 2026-11-04 — the commodity-specific Sharpe figures were not verified from the paper; a secondary guide quotes cross-correlations 0.1–0.3 between carry strategies). The org flagged it as an open direction needing paid curve data ("hundreds of dollars" then); today Databento 1d bars for two contract months per CME root cost ≈ $0.05–0.10 per root per year-slice (≈ $2–5 total for CL, NG, GC, SI, HG, ZC, ZW, ZS, 2010–2026; ICE softs are not in GLBX — sugar/cocoa/coffee/cotton need another free source or are dropped). At FTMO the position is a CFD whose cost is spread + swap (2.5%/yr both sides for commodities per the D2 convention; the CFD provider's own roll handling embeds part of the carry — the sibling block C-8-01 and the Rules Keeper must check how FTMO's commodity CFDs roll, since a spot-priced XAUUSD has no curve carry at all).
- evidence: peer-reviewed (KMPV 2018; sample ≈ 1980–2012, verify); inherited negative evidence for FX carry at CFD costs (D2-04/05: closed).
- evidence window: KMPV ≈ 1980–2012 (verify); CFD implementation untested anywhere.
- instruments: FTMO USOIL/UKOIL/NATGAS/XAG (XAU is spot — no carry; copper if listed; grains if listed per the D4 symbol list: corn, wheat, soybeans, sugar).
- holding period and expected trades per year: weekly rebalance, positions held weeks to months → ≈ 50–150 trades/yr across the basket.
- data needed: Databento 1d for two months per root (≈ $2–5) or Yahoo individual-contract tickers (free, patchy); FTMO swap table (symbol pages, free).
- expected gross edge per trade: n/a (portfolio); the literature's commodity carry Sharpe is ≈ 0.4–0.8 before costs (unverified); after a 2.5%/yr swap on both legs and 2.5–8 bp spreads it is lower; cannot reach 1.5 alone.
- firm structure fit: FTMO Swing (across the close; 5% daily / 10% static rules; 30-day inactivity satisfied); not implementable at futures firms (flat daily).
- nearest closed relative: D2-04/D2-05/D2-06 (FX carry at CFD costs, CLOSED) — different asset class and signal source; H0007 (futures trend as goal, closed).
- decay haircut: 0.5; splits at 2004–2008 (financialization), 2014 (oil regime), 2020-04.
- plausibility of net Sharpe ≥ 1.5: low (literature Sharpe < 1 before swap).
- original: no

### C-11-03 Value measures on real quantities (PPP for FX, 5-year reversal for commodities, real yield for bonds; Asness–Moskowitz–Pedersen 2013) as an FTMO Swing sleeve — the "everywhere" stack's missing leg
- mechanism: slow value signals (FX: deviation from PPP; commodities: negative 5-year price change; bonds: real 10-year yield; equity indices: CAPE or dividend yield) earn a premium with monthly rebalance and low turnover; AMP (JF 68(3) 2013, "Value and Momentum Everywhere", not fetched; from memory, verify) report value Sharpe ≈ 0.3–0.6 per asset class and a 50/50 value–momentum combination near 1.0 before costs. The org's digest lists "value on the papers' real measures" as an untested open direction. At FTMO Swing the costs are the swap (FX ≈ 1%/yr markup; indices/commodities 2.5%/yr) and spreads once a month — the cheapest possible implementation of anything in this file.
- evidence: peer-reviewed (AMP 2013; sample ≈ 1972–2011); inherited D2 (trend + carry only; value never tested).
- evidence window: 1972–2011 (AMP, verify); 2012–2026 OOS is in the public factor data (AQR data library, free) — read once, as the gate requires.
- instruments: FTMO FX majors and crosses (PPP from OECD, free), index CFDs (CAPE from free sources), commodities (5-year reversal from Yahoo continuous series, free); no bond CFD at FTMO (verify) → bond leg dropped.
- holding period and expected trades per year: monthly rebalance; ≈ 20–40 trades/yr.
- data needed: $0 (FRED, OECD, Yahoo, AQR library).
- expected gross edge per trade: n/a (portfolio); Sharpe ≈ 0.3–0.6 standalone in the literature → fails the 1.5 target alone by construction; registered only as a sleeve of the FTMO Swing stack (with C-11-02 and the C-8-01 trend sleeve).
- firm structure fit: FTMO Swing only; 30-day inactivity rule satisfied by monthly rebalancing; 5%/10% rules need a guard (C-11-05).
- nearest closed relative: D2 (FX trend/carry, closed; value untested), G2 (index mean reversion; a different horizon), H0023.
- decay haircut: 0.5; splits at 2008, 2020.
- plausibility of net Sharpe ≥ 1.5: low (very low alone; it is a diversifier).
- original: no

### C-11-04 The bond sleeve of multi-asset trend, expressed as a US-day-session hold in ZN/ZB (08:20 → 15:00 ET) so that it lives inside one futures-firm day
- mechanism: the org's digest asks for "a bond sleeve in multi-asset trend"; at futures firms nothing can be held across the deadline, so the daily trend signal (12-month sign, or EWMAC 16/64 + 32/128 per D2-09 conventions, computed from free daily data) must be expressed as a position opened after 18:00 ET and closed before the deadline. For Treasuries the evidence says the return premium accrues in US trading hours and the overnight session is flat-to-negative (Hendershott–Livdan–Rösch, per sibling block C-3-06), the opposite of equities, where momentum profits accrue overnight (Lou, Polk & Skouras, JFE 2019, "A tug of war" — from memory, verify). So the bond leg is the one place where a day-session-only expression of a slow signal could capture most of the signal's return while paying one round trip a day. Rule: position = sign of the daily trend signal, entered 08:20 ET (Treasury cash open), exited 15:00 ET (futures settlement), sized to a fixed vol target; the overnight-session variant (18:00 → 08:20) is the pre-registered control that should earn nothing.
- evidence: peer-reviewed for the signal (Moskowitz–Ooi–Pedersen 2012; inherited H0007 54-futures 1984–2016 Sharpe 1.17 incl. bonds) and for the day/night asymmetry (HLR); own construction for the day-session expression.
- evidence window: trend 1984–2016 (H0007); HLR day/night Treasury returns ≈ 1990s–2010s (verify in C-3-06); the day-session trend expression is untested.
- instruments: ZN, ZB (UB, ZF secondary); no FTMO twin (no bond CFD; verify).
- holding period and expected trades per year: 6.7 hours; one round trip per trading day → ≈ 250/yr per root (the "hundreds of trades" branch of the economics screen, but the win rate will be ≈ 52%, so it must clear 2 × RT on the mean instead).
- data needed: Databento 1h ZN and ZB (≈ $1 each; the 08:00 and 15:00 hourly bars suffice) → $2; daily signals from free data (FRED/Yahoo).
- expected gross edge per trade: a trend Sharpe of 0.5–0.8 on bonds at 5% vol ≈ 1–1.6 bp/day; if 70% of it accrues in the day session, 0.7–1.1 bp/day vs 3 bp RT (ZN) → fails the economics screen by a factor of 3; the only rescue is to trade on the signal's *change* days only (≈ 20–40/yr), which makes it a sleeve with a different test. Stated honestly: this is a calibration of how much of a slow premium survives intraday expression, and the expected answer is "not enough".
- firm structure fit: intraday futures at all firms; FOMC 14:00 and 08:30 release windows touched at MFFU (skip or exit around them).
- nearest closed relative: H0007 (multi-day futures trend as the goal, CLOSED; this holds nothing across the close); D2-07 (bond proxies in the FX/CFD stack, closed); C-6-01 (intraday TSMOM breadth with 30-minute signals — different signal horizon).
- decay haircut: 0.5 (published signal); splits at 2008, 2022 (bond bear market).
- plausibility of net Sharpe ≥ 1.5: low (cost arithmetic above).
- original: yes (the day-session expression and its overnight control)

### C-11-05 Trend with a hard drawdown overlay, tested against FTMO Swing's 5% daily / 10% static rules: the overlay as a buffer-aware guard fraction, with its Sharpe cost measured
- mechanism: the base is the inherited multi-asset trend (H0007 rules on the daily data in hand; or the D2-09 EWMAC set on CFD twins with swaps), which cannot be a futures-firm strategy (flat daily) and at FTMO Swing (Sharpe 0.6–0.9 for ETF trend 2016–2026 per the inherited record) breaches the 5%/10% rules at the vol the target needs. The overlay: scale the whole book by g = min(1, B_d/(k_d·σ_1d), B_s/(k_s·σ_10d)) where B_d is the remaining daily buffer from the 00:00 CE(S)T balance incl. floating P&L and B_s the remaining static buffer, with a hard flat when either buffer falls below 1.5 × the relevant vol; k_d, k_s fixed in sample at 3 and 2. The hypothesis is not "the overlay adds return" (it cannot) but "the overlay cuts breach probability to < 2%/yr at 15% vol while costing < 0.1 Sharpe" — a pre-registered pair of numbers, both reported.
- evidence: inherited (H0007; D2; F2-06 "hard daily loss on equity incl. floating P&L" stress model; G2's 16–43 breaches at 15–20% vol); practitioner sibling C-8-01 (Carver's relative-vol multiplier); own guard definition (the registry already carries a `guard_fraction` column — this fills it).
- evidence window: 1984–2016 (H0007 data), 2013–2026 (D2 OOS); the overlay is untested.
- instruments: FTMO Swing CFDs (indices, FX, commodities; no bonds).
- holding period and expected trades per year: multi-day; ≈ 100–300 trades/yr with the overlay's extra rebalances.
- data needed: $0 (daily data in hand; FTMO swap table).
- expected gross edge per trade: n/a; success = breach rate and Sharpe cost as above.
- firm structure fit: FTMO Swing only; the overlay is the firm-fit check itself.
- nearest closed relative: H0007 (closed as the goal; the board allows "a sleeve at FTMO Swing only with a new row" — this is that row), D2 (closed), F1 (near-miss ensemble, closed — breached 5% on its worst day).
- decay haircut: 0.5; splits at 2020-03, 2022.
- plausibility of net Sharpe ≥ 1.5: low (the base is < 1; the overlay cannot create Sharpe).
- original: no

### C-11-06 US-only index mean reversion (US500/US100/US30), the G2 post-hoc slice, frozen now and evaluated only on data after the registration date
- mechanism: G2 (closed) found, after looking, that the RSI(2) buy-the-dip rule was positive on the three US index CFDs (zero-cost t 2.79) and negative elsewhere; the digest says it is "re-testable only on fresh post-2026 data". The concrete candidate is therefore a time capsule: the G2-06 rules verbatim (long when RSI(2) < 10 and close > SMA200; exit at the first close > SMA5 or after 5 days; equal-risk 60-day-vol sizing; worse of close and next-open fill; FTMO swap per night + spread), restricted to US500/US100/US30, with the evaluation window opening at the registration commit date and the test run once when ≥ 8 years (or the gate's power-adjusted minimum) have accrued. Mechanism offered by the org's own file: retail dip-buying in US indices is the most crowded trade in the world, which is also why it should not survive.
- evidence: inherited post-hoc slice (registry G2-01..07; `agents/prereg/G2_rules.md`); the published RSI(2) literature (Connors) is pre-sweep P-C27.
- evidence window: 2013–2026 (G2 OOS, contaminated for this slice); evaluation only on ≥ 2026-11 data.
- instruments: FTMO US500, US100, US30 (Swing).
- holding period and expected trades per year: 1–5 days; ≈ 10–15 trades/yr per index.
- data needed: $0 (daily closes).
- expected gross edge per trade: G2-06's pooled result was t 0.90 net; the US slice's zero-cost t 2.79 is the post-hoc number that must not be used.
- firm structure fit: FTMO Swing; swap per night (≈ −8%/yr long US index), 5% daily rule (G2 had 16–43 breaches at 15–20% vol → size at ≤ 10% vol).
- nearest closed relative: G2 (CLOSED; this is its sanctioned post-hoc slice under the digest's own condition), P-C27, H0023.
- decay haircut: 0.5; no split (future data only).
- plausibility of net Sharpe ≥ 1.5: low; registered so that the slice is never "found" again.
- original: no

## Declined in these lanes (closed family, negative evidence, covered by a sibling block, or no firm fit) — no new row

- hypotheses.py Z01 (retune the SMC/TJR bot's grading, FVG, BOS, kill zones): declined, closed family H0001–H0004/H0010/H0016; the file itself says "forbidden".
- hypotheses.py Z02 (the same bot on gold, oil, FX) and Z03 (other timeframes): declined as the same closed family on new instruments/bars; the common brief requires a materially new mechanism, and "same rules, other market" is not one. The inherited A08/C11 round-number beliefs are absorbed into C-12-20 with the Osler mechanism.
- hypotheses.py Z04 (a second uncorrelated strategy): not a candidate; it is this program's purpose (lane 6 breadth; the Director's stack).
- hypotheses.py Z05 (ML on the 111 setups): declined, 111 samples; lane 10 (C-10-01..05) covers ML done right.
- Digest open direction (6) "lower-turnover TWAP/VWAP breadth variant": declined (D4 closed; C-6-01 is the futures re-expression with new data).
- Digest open direction (9) "crypto funding carry per 8h on a funding-centric venue": declined (D3-07/08 closed; no safe-list firm offers perps with funding; FTMO crypto swap −30%/yr).
- Digest open direction (8) "crypto weekend effect in the F1 sleeve": declined (board: crypto weekday effects are negative evidence; found after looking).
- Digest open direction (3) "2007–2019 1-minute data to tell a Beat-the-Market pause from a vanished edge": a data purchase decision (H0005/H0011 closed), not a candidate; noted for Department C.
- Digest open direction (10) "FTMO adding a VIX/volatility CFD": a Rules Keeper symbol-gate task (G1 closed for lack of product), not a candidate.
- Digest open direction (2) "the 02:00–03:00 ET European-open window": covered by C-3-01/C-3-02 (academic scout); not re-listed.
- Commodity index roll (GSCI/BCOM 5th–9th business day) in CL/GC/ZC, outright or spread: declined, A-C17 and the board's negative evidence (post-2004); C-12-25 (FND) and C-12-32 (TAS flow) are the only roll-adjacent rows, each with a different population or a direct flow read.
- Equity LETF (TQQQ/SQQQ/UPRO) last-30-minute demand: covered by A-C24 and the closed H0006/H0019 window; commodity/Treasury LETFs by C-1-06/C-1-07; only the single-stock twist is listed (C-12-09).
- VWAP/TWAP parent-order footprint: covered by C-9-08 (microstructure scout); not re-listed.
- Closing-auction imbalance / MOC and the post-close reversal: covered by A-C25 and C-1-08.
- Index-rebalance effective days (S&P, Russell, MSCI, FTSE): covered by C-1-09 / P-C09.
- WMR, Tokyo, ECB fixings: covered by C-1-04, C-1-05, A-C08; only the PBoC fix is new (C-12-14).
- Expiry pinning, 0DTE gamma regime: covered by A-C26/C-1-10 and A-C23/C-4-05; the charm (C-12-19) and put-wall (C-12-28) rows are listed as non-original kill-tests.
- Settlement-window flow from the settlement bar: covered by C-9-09; C-12-32 is its data upgrade.
- Autocallable/structured-product barrier hedging in Nikkei/HSCEI/SX5E: declined — barrier data are not free (sell-side only); mechanism noted for the future.
- ES calendar-spread richening into roll week (asset-manager long roll; Hazelkorn–Moskowitz–Vasudevan JF 2023 on the equity basis): declined — the position is multi-day in a spread no safe-list firm structure can hold across the close; FTMO has no futures.
- Treasury wild-card option hour (15:00–17:00 ET in delivery months): declined — expiring contracts near delivery are not tradable at prop firms.
- London-open "Asian-range stop run" in 6E/6B (Judas-swing folklore): declined as D4-adjacent generic intraday FX rules (closed) without a measurable forced trader; the Osler row (C-12-20) carries the stop-cluster mechanism where it is published.
- Pre-holiday early-close (13:00 ET) flatten: 4–5 days/yr; too few to register.
- BoJ ETF purchases at 12:30 JST on weak mornings: dead since 2024-03 (programme ended); declined.
- Mutual-fund T+1 investment of 16:00 NAV flows; 401(k) mid-month paydays; dividend reinvestment dates: declined — flows not observable daily for free, or bare-calendar families (H0023 closed, day-of-week negative evidence).
- ICT/SMC "kill-zone" crowd fade (inverting the closed bot's rules): declined — the inverse of a closed family is the same family.

## Summary table

Grades: PR = peer-reviewed; WP = working paper / central-bank; PRAC = practitioner / vendor / press; FIRM = firm or exchange rule text; OWN = own idea (no evidence beyond the mechanism). Plausibility is for net Sharpe ≥ 1.5 on the single sleeve. "TOP10" marks the ten lane-12 rows the brief asks to register (rank in brackets).

| id | name | lane | evidence grade | plausibility | firm structure | data cost | original |
|---|---|---|---|---|---|---|---|
| C-12-01 | Topstep 16:08 / MFFU 16:10 forced flatten, traded from a later-deadline account — TOP10 (1) | 12 | FIRM + OWN | low | intraday futures at Lucid/Tradeify/Bulenox; FTMO intraday CFD | $40 (ES+MES full session) | yes |
| C-12-02 | 16:30–17:00 micro-session: Lucid/Tradeify 16:45, NinjaTrader margin end, Bulenox 16:59 | 12 | FIRM/broker + OWN | very low | Bulenox or FTMO only | shared $40 | yes |
| C-12-03 | Prop daily-loss / trailing-DD stop-out cascade, micro-share trigger — TOP10 (2) | 12 | FIRM + OWN | low | intraday futures (all) | $14–28 | yes |
| C-12-04 | CME margin-hike next-open liquidation in GC/SI/CL/NG — TOP10 (7) | 12 | PR (daily) + OWN | low | intraday / overnight-session futures; FTMO intraday | $28 (shared) | yes |
| C-12-05 | Crypto liquidation-cascade exhaustion → MBT / FTMO BTCUSD — TOP10 (8) | 12 | OWN (data limited: no free liquidation feed) | low | overnight-session futures (MBT); FTMO intraday | $0–20 | yes |
| C-12-06 | Vol-control / risk-parity deleveraging into the close, 1–3 days after a vol jump — TOP10 (3) | 12 | PRAC (bank model) + OWN | low | intraday futures 15:00–15:59; FTMO Swing variant | $0–7 | yes |
| C-12-07 | CTA trigger-level crossing → last-hour continuation, 6 roots — TOP10 (5) | 12 | PRAC + OWN | low | intraday futures; FTMO Swing next-open leg | $35 | yes |
| C-12-08 | VIX ETP leverage rebalancing → ES delta leg 15:45–16:15 — TOP10 (9) | 12 | PR (VX) + OWN (ES leg) | low | intraday futures (post-16:00 part needs Lucid/Bulenox/FTMO) | $0–20 | yes |
| C-12-09 | Single-stock LETF (NVDL/TSLL) → NQ close on big NVDA/TSLA days | 12 | PR analogue + issuer AUM | very low | intraday futures; FTMO intraday | $0–7 | no |
| C-12-10 | Platts Dated Brent MOC window 11:00–11:30 ET in CL / Brent CFD | 12 | PR (JBF 2018) + OWN (fade leg) | low | intraday futures; FTMO intraday | $0–7 | no (fade leg twist) |
| C-12-11 | NG/CL expiry-day final settlement window, hedged via the 2nd month | 12 | OWN (enforcement record as mechanism) | low | intraday + overnight-session futures | $28 | yes |
| C-12-12 | VIX-settlement Wednesdays: ES 09:31–09:45 fade of the SOQ-hedge unwind | 12 | PR (auction anomaly) + OWN (ES leg) | very low | intraday futures | $0–20 | yes |
| C-12-13 | Deribit 08:00 UTC expiry pin/release → MBT / BTCUSD | 12 | PRAC/press + OWN | low | overnight-session futures (MBT) | $0–20 | yes |
| C-12-14 | PBoC fix surprise → 6A/M6A 20:16–20:45 ET | 12 | PRAC + OWN | low | overnight-session futures; FTMO intraday | $0–20 | yes |
| C-12-15 | Month-end multi-asset rebalancing, equity leg into the last day's close | 12 | WP (NBER 2025) + twist | low (12/yr) | intraday futures; FTMO Swing | $0–7 | no |
| C-12-16 | JHEQX quarter-end collar and monthly buffer-ETF resets into the close | 12 | PRAC/press + OWN | low (12/yr) | intraday futures | $0–7 | yes |
| C-12-17 | Large-gap continuation as margin-call liquidation, micro-gated (adjacent to closed H0012/H0017) | 12 | OWN + inherited negative fade | low | intraday futures; FTMO intraday | $7 | yes |
| C-12-18 | Sunday 18:00 ET reopen overshoot fade, BTC-weekend sign filter | 12 | OWN | low | overnight-session futures; FTMO intraday | $0 (HistData) → $60 | yes |
| C-12-19 | Dealer charm flow midday drift, GEX-gated (folklore kill-test) | 12 | PRAC | low | intraday futures | $0–7 | no |
| C-12-20 | Round-number stop/take-profit clusters (Osler 2003) on gold and index futures at 1m | 12 | PR (FX 1999–2000) | low | intraday futures; FTMO intraday | $0–7 | no |
| C-12-21 | Opening 09:30–09:35 retail thrust fade, top-tercile micro share, with control arm — TOP10 (4) | 12 | OWN (+ stock-level retail-imbalance literature) | low | intraday futures (all) | $14–28 | yes |
| C-12-22 | Prop news-ban cohort re-entry at 08:33 ET in GC/6E/CL/ZN, traded from exempt firms — TOP10 (10) | 12 | FIRM + OWN | low | FTMO Swing / Topstep / Bulenox (exempt firms only) | $0 (HistData) → $80 | yes |
| C-12-23 | Failed 30-minute ORB fade (the ORB crowd's stops), paired with C-11-01 | 12 | OWN | low | intraday futures; FTMO intraday | $0–7 | yes |
| C-12-24 | Buyback-desk dip buying 13:00–15:50 on down days outside blackout, with in-blackout control — TOP10 (6) | 12 | PRAC + negative daily study + OWN | low | intraday futures; FTMO intraday | $0–7 | yes |
| C-12-25 | First Notice Day liquidation of non-deliverable longs, GC/SI/CL settlement window (adjacent to A-C17 negative) | 12 | OWN | very low | intraday futures | $42 | yes |
| C-12-26 | Index-expiry settlement auctions: ES SOQ 09:30 and DAX 13:00 CET post-auction reversal | 12 | PR (1980s–90s) + PRAC | low (16/yr) | intraday futures; FTMO GER40 | $0–7 | no (DAX leg twist) |
| C-12-27 | Nikkei SQ morning and HSI all-day-average expiry mechanics in NKD / JP225 / HK50 | 12 | FIRM/exchange + OWN | low (24/yr) | overnight-session futures; FTMO intraday | $0 (HistData) | yes |
| C-12-28 | 0DTE put-wall first touch (forward-collected CBOE OI; not backtestable) | 12 | PRAC | low; untestable before ≈ 2028 | intraday futures | $0 | no |
| C-12-29 | Treasury buyback operations 13:40–14:00 ET → ZN/ZB/UB | 12 | Treasury schedule + OWN | very low (cost-bound; 2.5-yr history) | intraday futures | $14 (shared) | yes |
| C-12-30 | Retail bar-close clock: 15-minute-boundary micro bursts faded (entry-timing overlay) | 12 | OWN (+ HKS 2010 background) | very low | intraday futures | $14 (shared) | yes |
| C-12-31 | Prop-firm forced roll days: micro front/back spread push | 12 | FIRM + OWN | very low | intraday futures (spreads) | $14 | yes |
| C-12-32 | TAS-instrument prints as the direct settlement-flow read (CL/NG/GC) | 12 | OWN (CME TAS rules) | low | intraday futures; FTMO intraday | $28–42 | yes |
| C-3-07 | Weekday 18:00 ET reopen 5-minute overshoot fade | 3 | OWN | low | overnight-session futures; FTMO intraday | $0 (HistData) → $40 | yes |
| C-9-10 | Micro-vs-mini BVC divergence as a 15-minute reversal signal | 9 | OWN | low | intraday futures | $28 | yes |
| C-6-06 | Micro-share retail-crowd state variable as a cross-root gate/sizing input | 6 | OWN (CME volume facts) | n/a as standalone; unknown as gate | any (overlay) | $28–98 | yes |
| C-7-06 | Clock anchoring and DST-mismatch weeks as construction standard and identification test | 7 | OWN (calendar facts) | n/a (method) | any | $0 | yes |
| C-11-01 | prereg_orb30 as written (A/B/C; OOS row only if A's D1 p5 > 0) | 11 | PR + WP + inherited prereg | low | intraday futures; FTMO intraday | $0 (+$7 OOS) | no |
| C-11-02 | Futures-curve carry (KMPV 2018) on FTMO commodity CFDs, swap charged | 11 | PR | low | FTMO Swing | $2–5 | no |
| C-11-03 | Real value measures (AMP 2013) as the FTMO Swing stack's missing leg | 11 | PR | very low alone | FTMO Swing | $0 | no |
| C-11-04 | Bond trend sleeve as a US-day-session hold in ZN/ZB (08:20 → 15:00) with overnight control | 11 | PR (signal, day/night asymmetry) + OWN construction | low (cost arithmetic) | intraday futures | $2 (1h bars) | yes |
| C-11-05 | Trend + buffer-aware hard-DD guard vs FTMO 5%/10% rules; breach rate and Sharpe cost reported | 11 | inherited + OWN guard | low (overlay cannot create Sharpe) | FTMO Swing | $0 | no |
| C-11-06 | US-only index mean reversion (G2-06 rules frozen), evaluated only on post-registration data | 11 | inherited post-hoc slice | low | FTMO Swing | $0 | no |

Counts: 42 candidates; 30 original (23 of 32 in lane 12; C-3-07, C-9-10, C-6-06, C-7-06, C-11-04); lanes covered: 12 (32 blocks, ten marked TOP10), 11 (6), 3, 6, 7, 9 (one each). Pre-sweep entries extended rather than re-listed: A-C24 (C-12-09), A-C17 (C-12-25/C-12-32 adjacency), A-C25/A-C26/A-C23 (declined list). Sibling blocks cited as cover: C-1-06/07/08/09/10/12, C-2-02/03/08, C-3-01/02/04/06, C-4-04/05, C-5-12/15, C-6-01, C-8-01, C-9-01/08/09, C-10-01.

The ten lane-12 rows recommended for registration, in order: C-12-01, C-12-03, C-12-06, C-12-21, C-12-07, C-12-24, C-12-04, C-12-05, C-12-08, C-12-22. Four of them (01, 03, 21, 22) share one cheap prerequisite — the micro/mini footprint study on ES+MES 1m (≈ $14 RTH, $40 full session) — which should run before any P&L test, because if the prop crowd leaves no measurable trace in micro volume at 16:05 ET, at 09:31 ET and at 08:33 ET, the entire prop-adversary thesis is dead at the cost of one purchase.

## Blocked hosts and sources not fetched (searches 2026-11-04; citation fetch date 2026-11-03 per the brief; nothing routed around)

Blocked or unreachable (pre-existing, unchanged): papers.ssrn.com (403 — Zarattini & Aziz 2023 for C-11-01 cited from the inherited prereg, not re-read); datafeed.dukascopy.com; lucidtrading.com (403 — Lucid's 16:45 deadline and 5-second rule are taken from the inherited firms file, not re-verified).
No new host was blocked in this run. Hosts not attempted (no need or paid): cboe.com DataShop (0DTE OI history, paid), direxion.com / etfdb.com (403 in the sibling run; TSLL AUM therefore unverified), coinglass.com (liquidation history, paid), cmegroup.com contract-spec pages (halt times taken from secondary sources; to verify), ninjatrader.com margin table (snippet only), home.treasury.gov buyback PDFs (titles only).
Checked directly: s3-ap-northeast-1.amazonaws.com/data.binance.vision listing (fetched 2026-11-04: `data/futures/um/daily/` has aggTrades, bookDepth, bookTicker, indexPriceKlines, klines, markPriceKlines, metrics, premiumIndexKlines, trades — no liquidation folder; the `liquidationSnapshot` prefix is empty); histdata.com 1-minute symbol list (fetched 2026-11-04: SPXUSD, UDXUSD, NSXUSD, UKXGBP, JPXJPY, GRXEUR, FRXEUR, HKXHKD, AUXAUD, ETXEUR, XAUUSD/AUD/CHF/EUR/GBP, XAGUSD, BCOUSD, WTIUSD).
Seen only as search snippets or abstracts (full text not read): Todorov RoF 2024 / BIS WP 952; Frino–Ibikunle–Mollica–Steffen JBF 2018; Griffin–Shams RFS 2018; Osler JF 2003 / NY Fed SR 125; Koijen–Moskowitz–Pedersen–Vrugt JFE 2018; Daskalaki–Skiadopoulos JFS 2016; AQR margin working paper; Stoll–Whaley 1990 J. Business; Harvey–Mazzoleni–Melone NBER w33554 (via sibling C-1-02); Heston–Korajczyk–Sadka JF 2010 (via C-9-08); CME 2025 equity-index recap and Equity Insights report; Nomura/McElligott vol-control estimates via Advisor Perspectives, Reuters/StreetInsider and SpotGamma; SpotGamma charm/JPM-collar explainers; Bloomberg JHEQX pieces (2025-03-11, 2025-06-30); HKEX SIF contract specifications; JPX Nikkei 225 mini/micro pages; NinjaTrader margin page; Treasury tentative buyback schedules Q1–Q3 2026; S&P Global Platts MOC subscriber note (2013); Alpha Architect buyback-blackout post (2019). From memory, flagged "verify" in the blocks: Boehmer–Jones–Zhang–Zhang JF 2021; Lou–Polk–Skouras JFE 2019; Asness–Moskowitz–Pedersen JF 2013; Beckmeyer–Branger–Gayda 2023; Brogaard et al. 2024; Hazelkorn–Moskowitz–Vasudevan JF 2023; Moskowitz–Ooi–Pedersen 2012; Levine–Pedersen "Which Trend Is Your Friend".
