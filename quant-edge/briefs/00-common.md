# Common brief for every quant-edge agent (read first; English; under 700 words)

**Client goal.** A fully automatic bot, runnable on many funded accounts at once, expected to net Itamar ≥ $20,000 per
$100,000 of funded account per year after profit split, fees, resets and failed accounts, at ≤ 20% annual volatility.
Or an honest, auditable "no edge found" with numbers. Two rules cannot change: (1) fully automatic, no human in the loop;
(2) many funded accounts must be buyable on it. Everything else (style, instrument, holding period, firm) may change.

**What the target means.** FTMO Swing 100K needs net Sharpe ≈ 2.4 at 12% vol, 1.9 at 15%, 1.5 at 20% (inherited F2-09;
F2-12 says 1.5 is a floor). Published strategies lose about half their performance after publication, so a single
strategy needs post-cost OOS Sharpe near 3, or the program needs ≥ 5 independent sleeves. A zero-edge "lottery" of
evaluations is not a business ($1.2k/slot-year stressed, 84% chance of a losing first year).

**Three firm structures a candidate must fit** (verify clauses in `~/quant-edge-inherited/pr26/prompts/research/firms-2026-10-11.md`):
- Intraday futures at Topstep / MyFundedFutures / Lucid / TradeDay / Bulenox: flat by the firm's deadline (Topstep 3:10 PM CT,
  Bulenox 3:59 PM CT, MFFU 4:10 PM ET, Tradeify/Lucid 4:45 PM ET). The trading day starts at the 18:00 ET Globex reopen, so an
  overnight-session hold (after 18:00 ET, closed before the next afternoon deadline) is inside one trading day; cross-close holds are not.
  CME products only. News windows banned at MFFU Rapid/Pro (±2 min incl. resting orders) and Lucid Daily. No holds under 5 s (Lucid) / 10 s (Tradeify).
- FTMO Swing (CFDs): holds across the close at 1:30 leverage; 5% daily loss from the 00:00 CE(S)T balance incl. floating P&L; 10% static max loss;
  swaps charged per calendar day held (index long ≈ −8%/yr US, −6.5% EU, −4.9% JP225; crypto −30%/yr both sides; FX markup ≈ 1%/yr); $400k per strategy.
- FTMO intraday CFD: same account, flat by day end, no swap.
Banned everywhere: cross-firm hedging, martingale/all-in, copy of third-party bots where banned, VPS at Topstep.

**Cost floors per side (market orders, RTH):** ES 0.30 pt + ≈ $2.50; MES 0.25 pt + $0.80; NQ 0.25 pt + ≈ $2.50; SPY 0.5 bp per unit;
CFDs 0.5–1.5 bp FX/indices, 1 bp gold, 2.5 bp WTI, 8 bp natgas; crypto perps 7 bp + funding. 2× cost run always reported.
Economics screen: a candidate whose plausible gross edge per trade is below max(2 ticks, 2 × round-trip cost) is not registered unless it
trades hundreds of times a year with win rate > 58%; Carver's speed limit: annual cost / annual vol (Sharpe units) < one third of pre-cost Sharpe.

**The gate.** N_total = 430, one-sided z = 3.6807; 8+ OOS years where data exists; 2× costs; null models; re-implementation; Red Team.
A real edge of the needed size passes at ~37% with 5 years and ~86% with 10, so "failed" ≠ "absent". Nothing is called an edge, a signal or
"promising" before Gate v2; before that it is "a pre-registered hypothesis under test" or "a near-miss".

**Closed families (cite the id when you decline an idea; never re-run without a new row + new data or a materially new mechanism):**
bot SMC/ICT/TJR (H0001–H0004, H0010, H0016); noise-area intraday momentum "Beat the Market" (H0005/H0011); last-half-hour momentum incl. GEX (H0006/H0019);
intraday IBS reversal (H0013/14); overnight-gap fade (H0012/17); 5-min ORB NQ/SPY (H0020); 1m/30m VWAP trend NQ (H0021/22); FOMC/CPI/NFP/ISM/PCE intraday ES/NQ (E2-01..12);
intraday rules across 19 CFDs (D4); daily FX/CFD trend + carry (D2); crypto TSMOM/XS/funding/cash-and-carry/hour-of-day (D3); FTMO stock-CFD reversal/PEAD/overnight (E1);
near-miss ensemble (F1); S&P turn-of-month (H0023); RSI(2)/3-down buy-the-dip on index CFDs (G2); VRP/VIX (G1); insider purchases (H0018); 54-futures trend as the goal (H0007).
Negative evidence, no new variants without a new mechanism: FX intraday momentum 6E/6B/6J, Goldman-roll front-running post-2004, pre-announcement drift post-2014,
bare OPEX and day-of-week effects, crypto weekday effects, 1-minute lead-lag without a mechanism, order-book deep learning at retail latency.

**Data in hand / reachable (free):** daily futures 1984–2016, daily asset classes 1970–2026, S&P open/close 1990–2026, SPXUSD 1m 2010–2018 (gappy),
ES 1m RTH 2008–2026 and Databento ES/NQ 2021–2026 (both third-party copies under LICENCE HOLD: cross-checks only), SPY/QQQ 1m one year, GEX/DIX daily,
Binance. Reachable: Binance, HistData FX 1m, Alpaca (key pending), Yahoo/Stooq/FRED/CBOE/CFTC daily, SqueezeMetrics. Blocked: Dukascopy datafeed, SSRN (403),
lucidtrading.com (403). Databento GLBX.MDP3 from 2010-06: 1m ≈ $20/root full session, ≈ $6–7/root RTH; 1h ≈ $1/root; 1d ≈ $0.05/root; plan ceiling ≤ $94 total.

**Rules for every agent.** Write your output file early and append as you go (a killed agent loses unwritten work). English everywhere except text to Itamar.
No purchases, sign-ups, trials, firm contact, money movement. Never print or store a key. Report blocked hosts; never route around them. Every number traces to a
URL with fetch date, a file path, or code that ran. Never load a file over 100 KB whole; grep it. To search the web load the tools: ToolSearch "select:WebSearch,WebFetch".
Read `quant-edge/WORK-LOG.md`, `quant-edge/board.md` and grep `quant-edge/registry.csv` before starting.
