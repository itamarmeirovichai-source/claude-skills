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
| Option dealers (0DTE gamma/charm) | all day; 15:30–16:00 | GEX sign, put/call OI | ES | A-C23/C-4-05 (regime), A-C26/C-1-10 (pinning), H0019 | C-12-19 (charm, not original) |
| Defined-outcome / collar funds | last 30 min of month/quarter ends | published strikes | ES | none | C-12-16 |
| VWAP/TWAP parent orders | until the round clock mark | flow sign | ES/NQ/ZN/CL/GC | C-9-08 | none (covered) |
| Index rebalancers / closing auction | 15:50–16:00; 16:00–16:08 | imbalance | ES/NQ/RTY | A-C25, C-1-08, C-1-09 | none (covered) |
| Month-end multi-asset rebalancers | last day 15:30–16:00 | month's equity-minus-bond return | ES (equity leg), ZN (bond leg C-1-02) | C-1-02 (bond leg), H0023 (daily TOM) | C-12-15 |
| Commodity index rollers (GSCI/BCOM) | 5th–9th business day, settlement | roll schedule | CL/GC/ZC spreads | A-C17 (closed, negative post-2004) | declined |
| Non-index longs before First Notice Day | 3 days before FND, settlement window | long liquidation | GC/SI/CL front vs 2nd | none | C-12-26 |
| Expiring energy contracts (physical index) | expiry day 14:00–14:30 | settlement painting | NG/CL expiring vs 2nd | C-9-09 (daily settlement, not expiry) | C-12-11 |
| Physical oil traders in the Platts window | 11:00–11:30 | assessment incentives | CL (Brent via CFD) | none | C-12-10 |
| Central-bank fixings (WMR, Tokyo, ECB, PBoC) | 11:00; 20:55/21:55; 09:15/10:15; 20:15/21:15 | fix mechanics | 6E/6B/6J/6A | C-1-04, C-1-05, A-C08 | C-12-14 (PBoC → 6A only) |
| SPX/VIX settlement auctions (SOQ) | 09:30–09:45 on 3rd Fridays and VIX Wednesdays | hedge unwind | ES | negative evidence "bare OPEX" (no mechanism) | C-12-12, C-12-30 |
| Margin-call liquidations (FCM, CME margin hikes) | 09:30–10:30 the day after | against under-margined side | GC/SI/CL/NG/ZC, ES | none; H0012/H0017 adjacent (fade sign failed) | C-12-04, C-12-17 |
| Crypto perp liquidation engines | any; clusters at round levels | liquidation side | BTC perps → CME MBT / FTMO BTCUSD | D3 (closed families; different mechanism) | C-12-05, C-12-13 |
| Retail CFD / FX stop clusters | round numbers; London open | Osler stop/take-profit asymmetry | XAUUSD, EURUSD, GBPUSD | D4 (closed; different rules) | C-12-20, C-12-27 |
| Prop traders at Topstep (16:08 auto-flatten) and MFFU (16:10) | 16:00–16:10 | side of the day's losers | MES/MNQ, ES/NQ | none found | C-12-01 |
| Prop traders at Lucid/Tradeify (16:45), NinjaTrader/AMP intraday-margin end, Bulenox (16:59) | 16:30–17:00 | same | MES/MNQ | none found | C-12-02 |
| Prop traders hitting daily-loss / trailing-drawdown stop-outs | after a ≥ N-point move inside RTH | with the move | MES/MNQ micro share | C-4-04 (drift bursts, price-only) | C-12-03 |
| Prop evaluation crowd at the open and at news bans (±2 min) | 09:30–09:35; 08:28–08:35 | crowd direction from micro share | MES/MNQ; GC/6E/ZN at 08:33 | H0020 (ORB, closed); E2 (ES/NQ macro, closed) | C-12-21, C-12-29 |
| The ORB crowd's stops | after a failed 30-min range break | opposite the failed break | ES/NQ | H0020, prereg_orb30 | C-12-50 (original fade) |
| Corporate buyback desks (10b5-18) | 13:00–15:50 on down days outside blackout | buy | ES | none | C-12-61 |
| Sunday 18:00 reopen crowd | 18:00–18:30 Sunday | weekend-news overshoot | ES/NQ/GC/6E | lane 3 (not this window) | C-12-54 |

Which firm rules let a bot be on the other side: an FTMO account (US500/US100 CFD priced off ES/NQ, tradable to ≈ 23:00 CET) and a Bulenox account (flat by 15:59 CT = 16:59 ET) can trade against every futures-firm deadline; a Lucid/Tradeify account (16:45 ET) can trade against Topstep (16:08) and MFFU (16:10) but not against its own crowd; a Topstep account can trade against nobody later than itself. Minimum holds (Lucid 5 s, Tradeify 10 s) are irrelevant at minute horizons; MFFU Rapid/Pro news windows matter only for C-12-29.

## Candidate blocks

