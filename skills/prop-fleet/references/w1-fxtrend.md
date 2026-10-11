# D2 (wave 1): forex/CFD multi-asset trend and carry

**Verdict: FAIL. None of the 9 pre-registered variants passes the gate. The headline (D2-08, trend + trend-filtered FX carry) made −1.6% a year out of sample in 2013–2026. Its out-of-sample t is −0.66 against a bar of 3.5504, and its bootstrap p5 is below zero. Even with no costs at all, no variant earns an out-of-sample Sharpe above 0.58, and the bar needs about 0.96.**

Written 2026-10-11 by the D2 head. Pre-registration: `agents/prereg/D2_rules.md` and
`agents/prereg/D2.csv`, committed and pushed in 77a78e7 (21:54:59Z) before any
backtest code existed. Code is in `agents/daily/w1-fxtrend/`:

| file | what it is |
|---|---|
| `data.py` | loader |
| `fxtrend.py` | engine, gate, tests and prop simulation |
| `diag.py` | diagnostics |
| `is1990.py` | the in-sample window check |
| `test_fxtrend.py` | unit tests (6 pass) |
| `run.txt`, `diag.txt`, `is1990.txt` | raw output |

Every number below comes from those files.

---

## 1. What was tested

**Universe (32 instruments, free daily data)**
- **FX:** 9 majors against USD and 8 crosses, from FRED H.10 noon fixes. The crosses are triangulated from those fixes.
- **Index CFDs (10):** US500, US100, US30, GER40, UK100, JP225, FRA40, AUS200, EU50 and HK50, from Yahoo.
- **Gold, silver and oil:** the GLD, SLV and USO ETFs, from Yahoo.
- **US 10y and 30y bond proxies:** built from FRED yields. They are used in D2-07 only.

**Network:** Yahoo (with a browser user agent) and FRED were reachable today; on 29 September both were blocked. Stooq was still blocked, and I did not try to route around it.

**Returns and costs**
- Returns are financed returns: the price change plus the interbank carry. The rates are OECD 3-month rates from FRED, applied with a one-month lag.
- The cost model has three parts:
  - a spread and commission charge per side, between 0.75 bp (FX majors) and 5 bp (silver);
  - a broker swap markup on gross notional held: 1% a year for FX and bonds, 2.5% for indices and commodities;
  - the whole set repeated at 2×.

**Split:** in-sample is 1990-01-02 to 2012-12-31; out-of-sample is 2013-01-01 to 2026-10-02, the last FRED fix (13.6 years).

**Sizing:** each sleeve is volatility-targeted to 10% from past data only, rebalanced daily with a 10% no-trade buffer.

**Look-ahead companion:** every variant was also run with a one-day-later execution (lag 2), and the worse of the two decides.

## 2. The gate: out of sample, worse of lag 1 and lag 2, 1× cost (2× shown)

| id | variant | IS Sharpe | OOS Sharpe | OOS t | OOS p5 (bp/day) | 2× Sharpe | 2× t | gate |
|---|---|---|---|---|---|---|---|---|
| D2-01 | trend, 1/3/6/12-month | 0.71 | −0.09 | −0.33 | −2.24 | −0.52 | −1.92 | fail |
| D2-02 | trend, 12-month only | 0.54 | **0.16** | 0.54 | −1.31 | −0.27 | −0.99 | fail |
| D2-03 | trend, 1+3 month | 0.58 | −0.50 | −1.85 | −4.07 | −0.96 | −3.56 | fail |
| D2-04 | FX carry, cross-sectional | 0.45 | −0.17 | −0.64 | −2.43 | −0.50 | −1.85 | fail |
| D2-05 | FX carry, time-series | 0.61 | −0.21 | −0.76 | −2.86 | −0.45 | −1.68 | fail |
| D2-06 | stack: trend + carry | 0.86 | −0.17 | −0.62 | −2.46 | −0.67 | −2.49 | fail |
| D2-07 | stack + bonds | 0.81 | −0.03 | −0.10 | −1.84 | −0.54 | −2.07 | fail |
| **D2-08** | **stack, carry only where the trend agrees (headline)** | **0.87** | **−0.17** | **−0.66** | **−2.56** | −0.57 | −2.15 | **fail** |
| D2-09 | trend, EWMA crossovers | 0.54 | 0.00 | 0.01 | −1.91 | −0.31 | −1.14 | fail |

- **The bar:** at 13.6 years, t ≥ 3.5504 needs a net Sharpe of about **0.96**. No variant is within 0.8 of it.
- **The look-ahead and truncation tests passed 20/20 on every variant.** Positions up to a random day d are identical when the data is cut at d. They are also identical when everything after d is replaced by noise.
- **The headline was picked by the pre-registered rule:** the highest in-sample net Sharpe. D2-08 has 0.87 and D2-06 has 0.86.
  - A first run measured in-sample from 1988, when positions first open, instead of from 1990 as pre-registered. On that window D2-06 looked first.
  - That run's EWMAC scalars also used pre-1990 data.
  - Both were fixed before this report, and `run.txt` is the corrected run. The out-of-sample results did not change.

### Headline D2-08 in detail (lag 1, 1× cost, at 10% volatility)

| | in-sample 1990–2012 | out of sample 2013–2026 | out of sample at 2× cost |
|---|---|---|---|
| Sharpe | 0.87 | **−0.10** (lag 2: −0.17) | −0.51 |
| CAGR | +9.2% | **−1.6%** | −5.8% |
| max drawdown | −17.4% | **−39.5%** | −61.9% |
| worst day | −5.0% | −4.4% | −4.4% |
| t (min of iid and Newey-West) | 4.03 | −0.37 | −1.90 |
| bootstrap p5 of daily mean | — | −2.19 bp (lag 2: −2.56) | −3.94 bp |

**Out of sample by year:** +11.0, −1.7, −3.8, −12.6, −4.9, −3.1, −1.4, +6.1, −2.7,
+6.5, −12.8, −4.6, +4.3, +0.6 (%), for 2013–2026 in order.

**By period:**

| period | Sharpe |
|---|---|
| 1990s | 1.01 |
| 2000–07 | 1.02 |
| 2008–12 | 0.38 |
| 2013–17 | −0.20 |
| 2018–21 | 0.02 |
| 2022–26 | −0.10 |

The edge was strong in the 1990s and 2000s, faded after 2008, and is gone after 2012.
This is the same decay `trend-following-etf.md` found on ETFs, but sharper here.

## 3. Why it fails: three findings, each checked

1. **There is little gross edge left.**
   - Out of sample, before any cost, D2-08 earns Sharpe 0.31. After trading costs it earns 0.19, and after the swap markup −0.10.
   - The red team computed the before-cost Sharpe for all nine variants: 0.07 to 0.58, with D2-02 the best.
   - **Even with no costs, the best variant reaches only 0.58 of the 0.96 needed.** Costs are not what decides the verdict.
2. **The swap markup is the killer at CFD firms.**
   - At 10% volatility the headline carries an average gross notional of 2.1× equity. D2-06 carries 3.3×, because carry needs large FX notionals.
   - The broker markup on that notional costs 3.1% a year for D2-08 and 4.3% for D2-06. Trading costs add 1.0–1.3%.
   - Gross return out of sample is only 3.3–4.5% a year. A prop CFD account pays the swap a futures account would not, and that alone takes the edge to zero.
3. **Carry and trend, by class, are all dead out of sample.**

   | sleeve | IS Sharpe | OOS Sharpe |
   |---|---|---|
   | FX trend | 0.48 | −0.12 |
   | index trend | 0.44 | −0.05 |
   | commodity trend | 0.66 | 0.02 |
   | bond trend | 0.25 | 0.02 |
   | FX carry (D2-04) | 0.45 | −0.17 |

   - **Diversification did not help, because there was nothing to diversify.** Trend and carry are uncorrelated out of sample (−0.01), and the stack is uncorrelated with the S&P (0.0).
   - This matches the published decay of G10 carry and of trend after 2009.

**Other checks (`diag.txt`):**
- Removing the 15 January 2015 SNB day changes nothing (−0.10 stays −0.10).
- Margin use at 10% volatility is a median 10% of equity, with a maximum of 37.5% under FTMO-type swing leverage, so leverage limits do not bind.

## 4. FTMO-type simulation (100k swing, 10% static max loss, 5% daily)

**Rules modelled**
- Phase 1 targets +10% and phase 2 targets +5%.
- A breach is counted at a 4% close-to-close day loss or at 91% equity. That is one point of buffer each, for intraday moves daily data cannot see.
- Funded accounts pay 80% of profit every 21 days, then reset. The $600 fee is refunded with the first payout. Funded accounts run for 2 years.
- Paths come from a block bootstrap, 10,000 per volatility level.
- The volatility was chosen on in-sample returns: the one that maximized expected payout per attempt was **10%**.

| at 10% volatility | in-sample returns (what it promised) | **out of sample, 1×** | out of sample, 2× | OOS 1×, lag 2 |
|---|---|---|---|---|
| passes phases 1 and 2 | 66% | **20%** | 10% | 17% |
| blown in evaluation | 29% | **73%** | 86% | 78% |
| median days to pass | 216 | 233 | 209 | 220 |
| funded account survives 2 years | 42% | **9.5%** | 3.9% | 7.3% |
| expected net per $600 attempt | +$9,800 | **+$550** | **−$224** | +$299 |

**The +$550 is not the strategy's edge. It is the fee's free option.**
- The same rules on the same paths, with the mean return set to exactly zero, give **+$894** per attempt. The actual returns give +$550, less than zero edge.
- With the mean at −2 bp a day the result is −$183. At +2 bp a day it is +$3,866, and at +4 bp it is +$9,545.
- **Why:** the most an attempt can lose is the $600 fee, but payouts are taken off the top every 21 days. Any volatile, zero-edge strategy therefore shows positive expected value in this model.
- **How fragile it is:**
  - It disappears at 2× cost.
  - It assumes the firm pays the trader of a strategy with no edge.
  - It assumes the firm doesn't restrict this behaviour.
  - The payout cadence and split are modelled, not verified.
- **This is a question about the prop structure, which D1 owns. It is not evidence for D2.** What D2 can say: this strategy is worse than a coin flip with the same volatility.

## 5. Verification and red team

**Verifier** (sub-agent, re-implemented from `D2_rules.md` alone without reading my code):

| | verifier OOS net Sharpe | mine |
|---|---|---|
| D2-01 | −0.06 | −0.05 |
| D2-04 | −0.14 | −0.15 |
| D2-06 | −0.10 | −0.08 |

- All three match within the pre-registered 0.05.
- It reproduced the costs too:
  - swap markup 3.2–4.3% a year;
  - mean gross leverage of 1.82 for trend and 3.33 for the stack;
  - gross out-of-sample Sharpe 0.38, 0.19 and 0.42.
- Its in-sample Sharpe for D2-06 (0.85) matches the corrected window (0.86). It is lower than my first run's 0.96, which is how the 1988 window error was found.
- Ambiguities it reported, now written down:
  - The calendar ends on the last FRED fix (2026-10-02), not 2026-10-09.
  - The sleeve volatility uses data through t or t−1 (the effect on out-of-sample Sharpe is 0.016 or less).
  - The carry sleeve has no base scale of its own, so the sleeve volatility target sets its size.

**Red team:** see section 7.

## 6. What this means for the wave

- **Daily trend and carry on a forex/CFD prop account do not pass the gate, and they don't come close.** Over 2013–2026 the edge was about Sharpe 0.3–0.4 before costs and below zero after a CFD broker's swap markup. The 1990–2012 numbers (0.87) are history, not a forecast.
- **The swing-account premise is right; the edge isn't.** Overnight and weekend holding opens multi-day strategies, but the multi-day strategy with the best literature behind it no longer earns what a CFD account costs to hold.
- **Do not build the EA on this.** If D1 finds that a firm's structure has positive expected value even at zero edge, that is a separate finding. It is a fee lottery, and it needs its own pre-registration and the firms' terms in writing.
- **Count:** 9 variants used of 15. The wave N stays at the fixed 260.

## 7. Red-team findings

The red team (a sub-agent) reproduced the numbers with its own scripts. Its default stance was "refuted".

**(A) All 9 variants fail: CONFIRMED.**
- On the 1990–2012 window, D2-08 has an in-sample Sharpe of 0.871 and D2-06 has 0.855.
- The headline choice is effectively a coin flip, and it doesn't change the verdict.
- The best out-of-sample t of any variant is 0.54 (D2-02).

**(B) Not a cost artefact: CONFIRMED.**
- Before costs, out-of-sample Sharpe is 0.07–0.58 across the nine variants.
- A 1% FX swap markup may be on the harsh side, but removing it entirely still doesn't reach 0.96.

**(C) The prop expected value is the fee option, not an edge: CONFIRMED and robust.** Rules were changed one at a time; dollars per attempt:

| change | actual returns | zero-mean returns |
|---|---|---|
| no buffer | 925 | 1351 |
| 90% split | 683 | 1068 |
| payout every 10 days | 611 | 967 |
| funded 252 days | 350 | 621 |
| buffer 3% / 92% | −11 | 177 |
| 60-day evaluation limit | −500 | −480 |

- Zero-mean returns beat the actual returns under every change and at every volatility from 6% to 20%.
- Break-even is a mean of about −1.5 bp a day, inside the out-of-sample range of the mean.
- The zero-edge "profit" needs an evaluation with no time limit.

**(D) The look-ahead and truncation tests pass, but they are limited.** They cut or perturb the panel after it is built, so they can't catch errors in the loader. The red team checked those by hand:
- the rate lag (month m is used from m+2, plus one day);
- Yahoo dates;
- quote directions and carry signs;
- cross construction;
- swap charged on gross notional;
- cost timing and the buffer.

All are correct.

**Deviations found (none changes the verdict):**
1. The in-sample window started in 1988 and the EWMAC scalars used pre-1990 data. **Fixed** before this report; the fix moved the headline from D2-06 to D2-08.
2. The sleeve scaler uses realized volatility through day t, while the rules say t−1. The 60-observation minimum was not pre-registered. This is not look-ahead; the verifier measured the effect on out-of-sample Sharpe at 0.016 or less.
3. FX returns run from one noon NY fix to the next, but the portfolio scaler also sees US index closes at 16:00 on day t. That is about 4 hours of look-ahead on FX sizing. It can only flatter the result, and it is tiny.
4. In D2-08, carry is zeroed when the 3-month and 12-month trend signals disagree (the trend signal is 0). The filtered carry is not re-scaled to its volatility target before the 50/50 weighting. Both are readings of an under-specified rule.
5. A docstring in `data.py` (`on_cal`) says prices are not carried past their last real price; the code does carry them. It has no effect, since every series ends on 2026-10-09.
6. The calendar ends on 2026-10-02, the last FRED fix, not about 2026-10-09 as the rules say.

**A side note, not a refutation.** Trend lost 4.1% gross in 2022, a strong year for trend benchmarks. The core universe has no bonds, and 2022 was a bond-shorting year; the equity trades whipsawed. Per-asset P&L directions check out. D2-07, which adds bonds, is the variant with the best out-of-sample Sharpe after D2-02 and D2-09.
