# Inherited firm matrix as of 2026-10-11 (Scribe, 2026-11-03)

Sources: F=`~/quant-edge-inherited/pr26/prompts/research/firms-2026-10-11.md`; W=`PF/references/w1-firms.md`, L=`PF/references/verification-letters.md`, C=`PF/agents/daily/w3-volrisk/clauses-ftmo.md`, CF=`PF/agents/daily/w1-firms/clauses-futures.md` (PF=`~/quant-edge-inherited/pr4/skills/prop-fleet`). Readings dated 2026-10-11; re-fetch before use (F).

## Safe list (W §1)
- FTMO (CFD, B): EAs allowed; Swing holds overnight and weekends, exempt from the ±2 min news ban, leverage 1:30; 5% daily loss from the 00:00 CE(S)T balance, checked on equity, 10% static max loss (C §7); $400k per trader OR strategy (C S14); T&C 7.8 one forbidden practice ends all agreements; funded-stage agreement never read (W §9).
- MyFundedFutures (B−): own-settings automation allowed, "unattended" unresolved; 5 sim-funded at 25K/50K, 3 if any 100K+; Rapid/Pro no positions or resting orders ±2 min around Tier-1 releases; flat 4:10 PM ET (F; CF §6).
- Lucid (B−): automated systems and copiers permitted; 5 funded per household; hedging ban covers "different firms or funded platforms"; microscalping flagged above 50% of profit from ≤5 s holds; Lucid Daily treats red-folder news as a breach; flat 4:45 PM ET (F; CF §3).
- Topstep (B): bots on Express Funded via the ProjectX API; "all trading activity must originate from your personal device", VPS/VPN banned; a Live call-up closes every XFA; 5 XFAs; MLL trails the EOD balance, locks at +$2,000; flat 3:10 PM CT; ToU §27 forfeits all accounts on one finding (F; CF §1).
- TradeDay (B−): own automation only inside supported platforms, no platform API, third-party bots banned; 5 funded sim + 5 live; identical trades across users shut all accounts (F).

## Conditional (written answer first; F)
Bulenox (2021 terms: third-party algorithms need approval, commercial tools banned, +$100/mo Rithmic API, Funded agreement after 3 payouts), The5ers (written approval; copy and bulk-trading bans), FXIFY, E8, Funding Pips, Tradeify (§6.6 bans the same bot at other firms; §6.7(i) opposite exposure elsewhere is hedging).

## Out (F; W §2)
Apex (bans all automation), Take Profit Trader, Earn2Trade, Alpha Futures, Top One, Phidias, Elite Trader Funding, FundedNext (manual-only ≥$50k; $25,000 penalties), FTUK, Alpha Capital, FundingTraders, Maven, Blue Guardian (one account per level, Guardian Shield −2% open P&L), every crypto firm (HyroTrader, Breakout, CFT, Velotrade, Bitfunded).

## Clauses that kill a bot fleet (W §3, verbatim there)
One bot = one strategy = one cap; identical trades across own accounts read as copy or group trading; third-party bots banned, so bot and bridge must be Itamar's own code; cross-firm clauses (Tradeify, Lucid): never net-opposite between firms; Topstep own device only; success ends the fleet (live call-ups, mergers); one finding voids everything; discretion over payouts and rules; sim-fill clauses (tight brackets, 5 s and 10 s holds); news windows (MFFU ±2 min incl. limits, FTMO Standard, Lucid Daily).

## Structural facts (F; W §4–5)
Every funded account is simulated and paid from the firm's cash at its discretion; My Forex Funds was dismissed over CFTC misconduct, the model never ruled on; the futures trading day runs from the 18:00 ET reopen to the flat deadline, so overnight-session holds are inside one day and cross-close holds are not; ceiling about 20–25 futures accounts plus one FTMO strategy at $400k.

## Open written questions (Itamar sends; L §1 is the letter)
Every firm before any purchase: a fully automatic, self-built, unattended bot on N funded accounts taking identical trades, allowed? which platform, API and hosting? does the same bot at other firms matter? Then MFFU on "unattended"; Lucid on prior approval and owner; Bulenox on whether a self-built Rithmic bot is "third-party"; Topstep on call-up criteria and coordinated trading; FTMO on the funded-stage agreement and per-strategy cap (`PF/agents/board.md` Open questions). Accountant letter on tax (L §2) at the first Gate-5 pass.
