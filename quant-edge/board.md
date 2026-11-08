# Board — shared state of the quant-edge program

*Every agent reads this, `WORK-LOG.md` and `registry.csv` before doing anything. The Director rewrites it after every run.*

## PROGRAM REOPENED 2026-11-08 (D-023): testing the remaining candidates. The N1 memo stays on file if nothing passes.

## Where we stood before closing

- **Edge: nothing tested yet in this program; nothing has ever passed a gate (inherited N = 280 variants, 105 rows, 0 passes).**
- **Running N = 280. N_total = 430. Bar z = 3.6807 one-sided (3.8538 for an unfixed sign). Bootstrap ≥ 430,000 draws. Fixed; never lowered.**
- **Spend: $0.00. Databento ceiling not yet set (credit unconfirmed). DATABENTO_API_KEY absent from the environment. No paid call is possible or allowed.**
- Environment: Python 3.13, 4 CPU, 15 GB RAM, 30 GB disk. numba/scipy/pytest/databento/pyarrow/statsmodels installed.
- Reachable: databento.com, data.alpaca.markets (needs a free key Itamar creates), data.binance.vision, histdata.com, Yahoo and CFTC (browser UA), FRED, CBOE, SqueezeMetrics, FTMO, Topstep, MyFundedFutures, TradeDay, arXiv, Quantpedia, GitHub.
- **Blocked (reported, not routed around):** datafeed.dukascopy.com (connection reset), papers.ssrn.com (403), lucidtrading.com (403).

## Required net Sharpe for $20k per slot-year (Economist re-run 2026-11-03, `economics/required-sharpe-2026-11.md`)

| vol | pre-tax (re-run) | pre-tax (inherited F2-09) | after 25% tax | after 47% tax |
|---|---|---|---|---|
| 12% | 2.44 | 2.42 | 3.16 | > 4.0 |
| 15% | 1.95 | 1.92 | 2.53 | 3.47 |
| 20% | 1.45 | 1.46 | 1.89 | 2.61 |

Planning number at 20% vol after tax: 2.6 until the accountant answers. Futures-firm frame: first pass in §8 of the report, all firm parameters inherited (2026-10-11).

## Lanes (hypothesis_lanes 1–13)

| lane | state | notes |
|---|---|---|
| 1 structural flows with a calendar | scouted (academic) | 25 candidates in lanes 1–2, mostly low |
| 2 scheduled information outside ES/NQ | scouted (academic) | see research/sweep/academic-flows-events.md |
| 3 overnight session at futures firms | scouted (academic) | 20 candidates in lanes 3–5, 1 medium |
| 4 intraday momentum/reversal, new markets | scouted (academic) | research/sweep/academic-session-momentum.md |
| 5 cross-market lead-lag | scouted (academic) | 9 candidates, all low |
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

Sweep workflow (resumed) and the engine agent, 3 concurrent (D-015). Then: Department C data run; Pre-registration Officer registers CAL-D and batch 1 from the prescreen; Rules Keeper matrix; Department G IBKR diagnosis.
