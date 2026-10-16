# W1 D3 Crypto: verdict

**FAIL: none of the 11 pre-registered crypto variants passes the gate.** The best out-of-sample t is 2.26, for long/flat time-series momentum (TSMOM), against a bar of 3.5504. That result is mostly crypto beta: a BTC position scaled to the same volatility earned the same over 2023–2026. Nothing from D3 goes to the bot.

Department D3, wave 1, 11 Oct 2026. Branch `claude/w1-crypto`. Pre-registration: `agents/prereg/D3.csv`, pushed in commit 53539f1 before any data was downloaded. Code: `agents/daily/w1-crypto/`.

## What was tested and how

- **Data.** Only data.binance.vision was used: spot 1h klines from 2018-07 to 2026-09, plus USD-M perpetual daily klines and the full funding-rate history. The 57 candidate coins were fixed in advance. They deliberately include coins that later collapsed or were delisted: LUNA, FTT, WAVES, MATIC, FTM, XMR, EOS and others.
- **Blocked hosts.** api.binance.com and fapi.binance.com return HTTP 451 from this environment, and api.bybit.com returns 403. We did not use them and did not try to get around the blocks. data.binance.vision had everything we needed.
- **Universe.** Each month, the 25 candidates with the highest 30-day quote volume, computed from data before that month. A coin needs 180 days of history to enter.
- **Costs.** Perps cost 5 bp taker fee plus 2 bp spread per side. A spot leg costs 9.5 bp per side. Real funding prints are charged, so a long pays positive funding. Before a symbol has funding history we assume 0.01% per 8h. Every variant was also run at 2× cost.
- **Out-of-sample design.**
  - All rules were written before any data was seen.
  - The decisive window is **OOS 2023-01-01 to 2026-09-30** (1,369 days). No rule was chosen on it.
  - **IS 2019–2022** was used for only two things: choosing D3-09's hours, and the fixed scale factor behind the "scaled" columns.
  - The bar is z(0.05/260) = **3.5504**. It applies to t = min(iid, Newey-West lag 10). The bootstrap p5 = min(iid, circular block 20) must also be above 0, with 10k draws and seed 0.
- **Count.** 11 variants counted, out of a budget of 15.

## Results: out of sample 2023-01 to 2026-09, net, cost ×1

Units are net bp of capital per day. Sharpe uses √365. CAGR and maxDD come from the raw series. The "scaled" column is the same series scaled to 20% annual volatility using the IS volatility, so it is ex-ante for OOS.

| id | strategy | mean bp/d | t iid / NW | p5 iid / block | Sharpe | CAGR | maxDD | scaled CAGR / maxDD | cost ×2 mean (t) | IS mean (t min, Sharpe) | gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D3-01 | TSMOM 20/60/120 L/S, universe | +4.70 | +1.33 / +1.36 | −1.16 / −0.75 | +0.69 | +15.1% | −22.2% | +11.7% / −16.8% | +4.00 (+1.13) | +6.41 (+1.75, 0.87) | FAIL |
| D3-02 | TSMOM long/flat | +5.61 | +2.26 / +2.03 | +1.52 / +1.02 | +1.17 | +20.9% | −18.1% | +20.6% / −17.9% | +5.29 (+1.92) | +6.75 (+2.41, 1.22) | FAIL |
| D3-03 | TSMOM BTC+ETH only | +7.21 | +1.37 / +1.40 | −1.34 / −1.08 | +0.71 | +21.4% | −41.0% | +12.5% / −23.1% | +6.25 (+1.19) | +12.65 (+2.29, 1.20) | FAIL |
| D3-04 | 1h EMA24/168 trend, top 10 | +3.03 | +0.66 / +0.64 | −4.55 / −4.14 | +0.34 | +6.0% | −33.1% | +4.5% / −18.4% | −0.11 (−0.02) | +9.46 (+1.81, 0.91) | FAIL |
| D3-05 | XS momentum 28d weekly | +0.61 | +0.15 / +0.17 | −6.00 / −5.52 | +0.08 | −1.8% | −55.9% | +0.2% / −31.0% | −0.29 (−0.08) | +17.56 (+2.97, 1.49) | FAIL |
| D3-06 | XS momentum 7d weekly | −1.64 | −0.41 / −0.43 | −8.15 / −8.15 | −0.21 | −9.5% | −54.5% | −4.3% / −33.2% | −3.23 (−0.85) | +12.67 (+2.51, 1.26) | FAIL |
| D3-07 | funding carry, perps, market-neutral | +2.19 | +0.70 / +0.70 | −3.02 / −3.06 | +0.36 | +5.7% | −38.6% | +4.6% / −28.9% | +1.19 (+0.38) | +2.02 (+0.49, 0.26) | FAIL |
| D3-08 | cash-and-carry (spot + short perp) | −0.20 | −0.84 / −0.59 | −0.62 / −0.81 | −0.43 | −0.7% | −5.4% | −7.3% / −40.9% | −1.34 (−4.94) | +2.93 (+4.00, 4.70) | FAIL |
| D3-09 | BTC hour-of-day (IS-chosen hours) | −54.33 | −20.84 / −21.91 | −58.6 / −58.5 | −10.76 | −86.5% | −99.9% | (1×) | −110.3 (−44.5) | selection period | FAIL |
| D3-10 | vol-managed combo 01+05+07 | +6.06 | +1.96 / +2.20 | +0.97 / +1.85 | +1.01 | +21.8% | −15.5% | +21.7% / −15.4% | +4.72 (+1.53) | +8.21 (+2.86, 1.49) | FAIL |
| D3-11 | vol-managed TSMOM | +7.32 | +2.15 / +2.10 | +1.73 / +1.96 | +1.11 | +26.9% | −16.7% | +21.4% / −13.4% | +6.61 (+1.90) | +7.27 (+2.10, 1.05) | FAIL |

**Net bp/day by year:**

| id | 2023 | 2024 | 2025 | 2026 (to Sep) |
|---|---|---|---|---|
| D3-02 | 8.2 | 9.8 | −1.0 | 5.4 |
| D3-11 | 5.8 | 12.9 | 1.7 | 9.4 |
| D3-10 | 8.2 | 6.0 | 5.1 | 4.6 |

The full per-year table, including IS years, is in `daily/w1-crypto/results.json`.

## What the numbers say, in plain English

1. **Trend works a little in crypto, but not enough.** All the TSMOM versions made money in both periods. The best is long/flat (D3-02), at about Sharpe 1.2. At 1,369 days the bar needs about Sharpe 1.8 (3.55/√1369 × √365), and no version got near it.
2. **D3-02 is mostly beta.**
   - It is on average 0.21 net long.
   - BTC buy-and-hold over the same window has Sharpe 1.16, against D3-02's 1.17.
   - Against an equal-weight universe, its alpha t is 2.03.
   - Removing the 20 best days brings D3-02, D3-10 and D3-11 to about zero.
3. **Cross-sectional momentum died out of sample.**
   - In sample it was the strongest family: D3-05 had t 2.97 and Sharpe 1.49, driven by 2020–2021.
   - Out of sample it is zero, and −24 bp/day in 2026.
   - This is the classic failure after the factor was published (Liu–Tsyvinski–Wu).
4. **Carry is real but small, and crowded.**
   - Cash-and-carry (D3-08) had in-sample Sharpe 4.7, from the 2021 funding boom.
   - Out of sample, funding fell to about 1 bp/day, and costs plus basis noise took all of it.
   - D3-08 also needs spot holdings, which perp-only prop accounts do not offer.
5. **Hour-of-day seasonality is a cost trap.**
   - The best and worst BTC hours in sample were 13h and 21h UTC (long) and 23h and 2h UTC (short).
   - Those 4 hours mean 8 position changes a day, which costs 56 bp/day, against a gross of +1.7 bp/day.
   - The same result on ETH: −53.7 bp/day.
6. **The 1h intraday trend (D3-04)** had a gross of +6.7 bp/day, but 3.1 bp of cost and 0.6 bp of funding left it at t 0.66. At 2× cost it is zero.

## Checks (all passed, or explained)

- **Look-ahead and truncation test.** For each of 54 cut days (50 random, plus 4 month-ends and Sundays), every generator was rerun with all data after the cut deleted. Decision weights were identical on every day up to the cut for all 11 variants. Log: `daily/w1-crypto/truncation-run.txt`.
  - D3-09 was tested only on OOS cuts. Its hours are chosen on the whole IS window by design, and it trades only OOS.
- **Independent verifier** (`daily/w1-crypto/verifier.md`, `verify/`). The verifier rebuilt 9 variants from the pre-registration alone, without reading our code. Every t is within 0.2 of ours, and no variant passes in their version either.
  - D3-05 differs, 0.31 vs 0.61 bp/day. The cause is a one-day boundary in the 180-day history rule.
  - Our IS t column is min(iid, NW). For D3-08 IS, the iid t is 9.36 and the NW t is 4.00.
- **Red team** (`daily/w1-crypto/redteam.md`, `redteam/`). No look-ahead found. It found two real deviations, and both make carry look **worse** than it is:
  - **Stale rows after delisting.** data.binance.vision keeps publishing zero-volume perp klines and funding prints of 0.0001 after a perp is delisted (FTM, MATIC, FTT, WAVES and others). Masking them moves D3-08 from −0.20 to −0.11 bp/day.
  - **Funding ranked per print, not per 8h.** Since 2023, coins with extreme funding have switched to 4h or 1h funding intervals, so the per-print rate understates them. Ranking per 8h moves D3-07 from 2.19 to 3.73 (t 1.20).
  - With both fixes, the combination D3-10 is +6.93 bp/day, t 2.22. It still fails.
  - These fixes are reported only as corrections and are not counted as new variants. The verdict does not change.
- **Survivorship.** The candidate list leaves out about 40 coins that were top-25 by volume during OOS. As a diagnostic, the red team added 72 more symbols. D3-02 moved to 5.25 bp/day (t 2.00), D3-11 to 6.98 (t 2.03) and D3-05 to 4.21. The verdict does not change.
- **The IS period is mostly a spot backtest.** In 2019 none of the TSMOM weight is on coins with a listed perp; in 2020 only part of it is. The OOS period is clean.
- **Prop-rule fit (gate item 4).** At the scale needed for 20% a year (about 0.75–1.0× the tested series):
  - OOS maxDD is −13% to −18%, and the worst day is −5.6% to −6.9%.
  - Over rolling 1-year windows, the chance of breaching a 5% daily / 10% max limit is 37–56% with a static drawdown and 83–96% with a trailing one. A 3%/6% account is breached in 100% of windows.
  - Even a strategy that passed the t bar would fail most crypto prop drawdown rules at this size.

## Crypto prop firms that allow bots on funded accounts

Full table, with an evidence tag on every claim: `daily/w1-crypto/propfirms.md`. All of it was gathered on 2026-10-11 from firm pages where reachable. Rules change often; recheck before any purchase.

| Firm | Bots on funded? | Key limits | Source |
|---|---|---|---|
| Propr (Hyperliquid perps) | Yes, "with no restrictions"; public REST API | Copying between your own accounts allowed. 1-Step static 3–6% DD, 3% daily. Funding passed through. **$300k aggregate** | propr.xyz/rules (firm page) |
| Velotrade (DXtrade API) | Yes, API on every account since 13 May 2026 | No HFT, grid or arbitrage. No bots coordinated across accounts. Static DD. 5 days of ≥0.8% profit per phase | velotrade.com/blog/velotrade-api-access-funded-accounts (firm page) |
| HyroTrader (Bybit/BloFin demo API) | Yes, own strategy only | **One account per program type** (terms §4.5). USDT perps. 3–5% daily. Max 40% of the target from one day. $200k | hyrotrader.com FAQ and T&C (firm page) |
| Crypto Fund Trader (Bybit API, MT5) | Implicitly yes: only HFT, tick-scalping and arbitrage EAs are banned | API key must stay unchanged. 1-Phase trails 6%. $300k per user | cryptofundtrader.com/faq (firm page) |
| FTMO crypto CFDs (MT5) | Yes, EAs allowed | $400k per trader **or per strategy**. Funded Standard must be flat for the weekend (Swing is not) | ftmo.com FAQ (firm page / snippet) |

**Ban bots or are effectively closed to them:**
- Bitfunded: its firm FAQ says "API automation… prohibited".
- SizeProp: API bots are blocked.
- FundedNext: accounts of $50k and up are manual only.
- Goat Funded Trader: no VPS from 6 Oct 2026.
- Alpha Capital: each EA needs pre-approval, with source code.
- Breakout (Kraken): no public API, and third-party sources conflict.

**Blocked during this research:** breakoutprop.com and propfirmmatch.com (HTTP 403). myfundedperps.com did not resolve.

**For a fleet**, the binding limit is per-strategy or per-person capital caps of about $200–400k, more than bot permission. Funding is a real cost at every perp firm.

## What this means for the wave

Crypto adds no edge that clears the bar. The one family that survived out of sample, trend, is at Sharpe about 1.1–1.2. That matches the futures trend result we already have (Sharpe 1.17 on 54 markets), and in crypto it is largely beta. Because both are trend, a crypto sleeve inside a multi-asset trend book (D2) would add correlated return more than new breadth. Its −18% drawdown also does not fit the 6–10% limits of crypto prop accounts at the size needed for 20% a year. Next steps that might be worth one counted variant in a later wave:
- carry with the per-8h funding fix, on a venue where funding is the main return;
- trend with a hard drawdown overlay, tested against the firms' actual rules.
