# Board — shared state of the quant-edge program

*Every agent reads this, `WORK-LOG.md` and `registry.csv` before doing anything. The Director rewrites it after every run.*

## Where we stand (Day 0, 2026-11-03)

- **Edge: nothing tested yet in this program; nothing has ever passed a gate (inherited N = 280 variants, 105 rows, 0 passes).**
- **Running N = 280. N_total = 430. Bar z = 3.6807 one-sided (3.8538 for an unfixed sign). Bootstrap ≥ 430,000 draws. Fixed; never lowered.**
- **Spend: $0.00. Databento ceiling not yet set (credit unconfirmed). DATABENTO_API_KEY absent from the environment. No paid call is possible or allowed.**
- Environment: Python 3.13, 4 CPU, 15 GB RAM, 30 GB disk. numba/scipy/pytest/databento/pyarrow/statsmodels installed.
- Reachable: databento.com, data.alpaca.markets (needs a free key Itamar creates), data.binance.vision, histdata.com, Yahoo and CFTC (browser UA), FRED, CBOE, SqueezeMetrics, FTMO, Topstep, MyFundedFutures, TradeDay, arXiv, Quantpedia, GitHub.
- **Blocked (reported, not routed around):** datafeed.dukascopy.com (connection reset), papers.ssrn.com (403), lucidtrading.com (403).

## Lanes (hypothesis_lanes 1–13): all "not yet swept"

| lane | state | notes |
|---|---|---|
| 1 structural flows with a calendar | not swept | |
| 2 scheduled information outside ES/NQ | not swept | firm news windows are part of the brief |
| 3 overnight session at futures firms | not swept | day-boundary verification needed per firm |
| 4 intraday momentum/reversal, new markets | not swept | distinct from closed H0006/H0019/H0020/H0021/H0022/D4 |
| 5 cross-market lead-lag | not swept | mechanism required |
| 6 breadth and portfolio construction | not swept | |
| 7 regime-conditional | not swept | inactivity rules |
| 8 FTMO Swing across the close | not swept | swaps charged honestly; not G2/D2 |
| 9 order-flow proxies from bars | not swept | 1s pilot only after gross t > 3 |
| 10 ML done right | not swept | |
| 11 org's own open directions | not swept | prereg_orb30 exists, never run |
| 12 the market's adversary | not swept | register the ten best |
| 13 text / alt data, free only | not swept | expect low |

## Closed families (never re-run without a new row, new data or a new mechanism; cite the id)

bot-smc-tjr (H0001–H0004, H0010, H0016); noise-area intraday momentum (H0005/H0011); last-half-hour momentum incl. GEX (H0006/H0019);
IBS reversal (H0013/H0014); overnight-gap fade (H0012/H0017); 5-min ORB (H0020); 1m/30m VWAP trend (H0021/H0022); macro events intraday ES/NQ (E2-01..12);
intraday CFD breadth (D4); daily FX/CFD trend+carry (D2); crypto (D3); stock-CFD anomalies (E1); near-miss ensemble (F1); turn-of-month (H0023);
buy-the-dip index CFD (G2); VRP/VIX (G1, no product); insider purchases (H0018); multi-day futures trend as a goal (H0007; sleeve at FTMO Swing only with a new row).

## Decisions today

See WORK-LOG.md D-001 … D-007.

## Open questions (Itamar only)

1. Databento: remaining credit, expiry date, signup date (portal → Billing). 2. Portal monthly limit set to min(105, 85% of credit) with the 50% email. 3. DATABENTO_API_KEY in the environment's secrets. 4. Key rotation if ever pasted in chat.
Later: IBKR history job approval (Day 1), IB Gateway paper mode before Phase 6, sending the firm letters, optional free Alpaca account.

## Next run

Day 0 remainder: Red Team pre-mortem; Economist F2-12 re-run; Scribe briefs. Day 1: Department B sweep (Workflow), Department C free-data run, firm letters, Rules Keeper fetch, Department G IBKR diagnosis document.
