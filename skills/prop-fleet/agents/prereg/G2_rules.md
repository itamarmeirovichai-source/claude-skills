# G2 pre-registration: short-term mean reversion across FTMO index CFDs (wave 4)

Written 2026-10-12 by the G2 head, **before any backtest**. Before writing this I looked only at:
- FTMO's symbol JSON (`https://ftmo.com/wp-json/ftmo/symbols`, the data behind ftmo.com/en/symbols, fetched 2026-10-12, HTTP 200);
- which Yahoo index histories exist, their first dates, and how often Yahoo's open is stale (open equal to the previous close or to the same day's close).

I computed no returns, signals or statistics. The commit that adds this file and `G2.csv` comes before
any backtest code or result.

**Bar:** one-sided z(0.05/304) = **3.5914** (wave 4, fixed). **Budget:** 7 counted variants (limit 15; the brief caps G2 at 8).

## 0. FTMO facts (symbol JSON, 2026-10-12)

All 10 index CFDs in the brief are listed and active as `*.cash` ("Spot CFD"): US500, US100, US30, GER40, UK100,
JP225, FRA40, AUS200, EU50, HK50. Commission is **0** on all ten. Swing leverage is 1:15 (HK50 1:9).
Swap is in points per lot (`swapType: points`, 2 digits, so 1 point = 0.01 index unit per unit of contract).
At the last Yahoo close (9–12 Oct 2026) that is, per year of calendar nights:

| CFD | Yahoo | swap long | swap short | long %/yr | short %/yr | assumed cost per side |
|---|---|---|---|---|---|---|
| US500 | ^GSPC | −177.10 | +8.94 | −8.28 | +0.42 | 1.0 bp |
| US100 | ^NDX | −701.31 | +35.40 | −8.29 | +0.42 | 1.0 bp |
| US30 | ^DJI | −1167.96 | +58.96 | −8.25 | +0.42 | 1.0 bp |
| GER40 | ^GDAXI | −446.74 | −4.51 | −6.50 | −0.07 | 1.0 bp |
| UK100 | ^FTSE | −237.61 | +10.97 | −8.22 | +0.38 | 1.0 bp |
| JP225 | ^N225 | −923.80 | −307.93 | −4.88 | −1.63 | 1.5 bp |
| FRA40 | ^FCHI | −139.00 | −1.40 | −6.50 | −0.07 | 2.0 bp |
| AUS200 | ^AXJO | −186.19 | −20.17 | −7.74 | −0.84 | 2.5 bp |
| EU50 | ^STOXX50E | −109.98 | −1.11 | −6.50 | −0.07 | 3.0 bp |
| HK50 | ^HSI | −445.79 | +4.90 | −6.70 | +0.07 | 4.0 bp |

- **Swap** is applied as these constant %/yr rates, per calendar night held (a Friday-to-Monday hold pays 3 nights),
  in **every** year. That is conservative for 2013–2021, when policy rates were near zero. A positive short swap is credited.
- **Spread:** FTMO does not publish spreads ⚠. The cost per side above is my assumption: roughly the full typical
  CFD spread at today's level (US500 0.5 pt, US100 1.5, US30 2.5, GER40 1.5, UK100 1.0, JP225 10, FRA40 1.5,
  AUS200 2, EU50 2, HK50 10 points), floored at 1 bp, to cover wider spreads at the close and the open.
  Charged on every change in position, as a fraction of the notional traded.
- **Cost ×2:** spread **and** swap doubled. Reported next to every result.

## 1. Data

- Yahoo chart API daily open and close of the ten indices (price indices, local currency). Timestamps shifted by
  the exchange's gmtoffset and normalised to the local date. Each market runs on its own trading calendar; the book
  is pooled on the union of dates (a market with no bar that day contributes 0).
- P&L is in local currency as a fraction of notional; FX on P&L is ignored (it is second order).
- **Open-price quality:** Yahoo's open is stale (equal to the previous close or the same day's close) in some
  market-years (e.g. ^AXJO 2012–2019, ^FTSE 1999–2006, ^GSPC before 1997). In the next-open version a day's open is
  **valid** only if it differs from both. If the fill day's open is invalid, the fill is at that day's **close**
  instead (one more day of delay).

## 2. Signals (computed at the close of day t from closes up to and including t)

- **RSI(2):** Wilder RSI, period 2 (average gain and loss smoothed with alpha = 1/2, seeded with the first 2 changes).
- **Down day:** C_t < C_{t−1}. **3 down closes:** days t, t−1 and t−2 are all down days. **3 up closes:** mirror.
- **SMA5:** mean of C_{t−4..t}. **SMA200:** mean of C_{t−199..t}.
- **Long entry:** flat at the close of t and the entry rule holds at t.
  - RSI rule: RSI2_t < 10. 3-down rule: 3 down closes ending at t.
- **Long exit:** at the close of the first day d after entry with C_d > SMA5_d, or at the close of the 5th trading day
  after entry, whichever comes first. No re-entry on the exit day; the next possible entry is the next close.
- **Short (long/short versions):** RSI2_t > 90 (or 3 up closes); exit at the first close with C_d < SMA5_d, or after 5 days.
- **Trend filter (200-day):** a long may be **entered** only if C_t > SMA200_t; a short only if C_t < SMA200_t.
  The filter is checked only at entry.
- Warm-up: no signal until 200 closes exist for that market (all variants, so the filter does not change the sample).

## 3. Sizing and pooling

- **Volatility:** sigma_i,t = standard deviation of the last 60 close-to-close returns of market i up to t (needs 60).
- **Equal risk:** an open position in market i carries notional w_i,t = (0.10 / sqrt(252)) / sigma_i,t / 10 of book
  equity, fixed at entry and held unchanged to the exit (no daily rebalance).
  So each open position targets 1% a year of book volatility (a 10%/yr risk budget split over 10 markets).
- **Book:** the sum over markets. Daily book return = Σ_i signed notional_i × market return_i − costs.
- **Scaling for prop numbers:** one scale factor k is fixed on the **in-sample** net book (the close version's
  realised vol before 2013). Out-of-sample returns are multiplied by k·(target/IS vol) for the 15% and 20% vol
  targets. Sharpe and t do not depend on this scale.

## 4. Execution versions (both run; the worse decides)

- **Close (lag 0):** the position decided at the close of t is filled at the close of t (cost charged), and earns
  C_{t+1}/C_t − 1 onward.
- **Next open (lag ½):** the position decided at the close of t is filled at the open of t+1 (or that day's close if
  the open is invalid). It earns O_{t+1}→C_{t+1}, then close-to-close, and is exited at the open after the exit signal.
- Swap is charged for every calendar night a position is held through a close in both versions.
- **The worse of the two** (lower out-of-sample net t) is the reported result of each variant.

## 5. Split

- **In sample:** first available signal date (1990-01-02 at the earliest) to 2012-12-31. Used only to pick the headline.
- **Out of sample:** 2013-01-01 to the last date (9–12 Oct 2026). **Decisive.**
- Markets with no data in a period (EU50 before 2007-03-30) simply contribute nothing then.

## 6. Benchmark (beta never counts as an edge)

- **Basket:** buy-and-hold of the same 10 markets, each at notional (0.10/sqrt(252))/sigma_i,t/10, rebalanced daily
  (the same equal-risk weights the strategy would use if every market were long every day), gross of costs.
- **Matched benchmark:** that basket scaled by the strategy's average net exposure E = mean over days of
  Σ_i signed notional_i / Σ_i full basket notional_i. For long-only variants E > 0. Its Sharpe and t are reported.
- **Alpha t:** OLS of the strategy's daily net return on the basket's daily return (plus a constant), out of sample;
  alpha t = t of the constant with Newey-West standard errors (10 lags). Also reported: beta, and the Sharpe of the
  strategy minus beta × basket.

## 7. Statistics (out of sample, daily net returns of the book)

- **t:** the smaller of the iid t and the Newey-West t (10 lags) of the daily mean.
- **Bootstrap p5:** 5th percentile of the daily mean over 10,000 moving-block bootstrap samples (block 10 days, seed 0).
- Net Sharpe (×sqrt 252), CAGR, max drawdown, worst day, per-year return and Sharpe, trades per year, average holding
  days, average exposure, cost ×2 run.
- **5% daily-loss breaches:** days with a book loss worse than −5% when the book is scaled to 15% and to 20% annual vol
  (scale fixed in sample, §3).
- **$ per $100K FTMO slot per year:** `agents/daily/w3-volrisk/stress_model.py`, FTMO Swing 2-Step 100K,
  F2-09 settings (t3 tails, gaps + kill switch, GARCH clustering, 24 checks a day with a lagging balance,
  FTMO-exact rules), n = 3000, seeds 11/12, at S = the decisive out-of-sample net Sharpe, vol caps 15% and 20%.
  If S ≤ 0 the S = 0 figure is reported as the upper bound.

## 8. Look-ahead and truncation tests

For 20 random cut dates d (seed 1): (a) **truncation** — positions up to d are identical when the data is cut at d;
(b) **perturbation** — positions up to d are identical when every price after d is replaced by noise.
Both versions, every variant. A variant passes if 20/20 on both.

## 9. Gate (per variant, on the worse execution version)

PASS only if **all** hold: out-of-sample net t ≥ 3.5914; bootstrap p5 > 0; alpha t vs the basket ≥ 3.5914;
look-ahead tests 20/20. Cost ×2 is reported, not gated (as in waves 1–3).

**Headline:** the variant with the highest **in-sample** net Sharpe (worse version), chosen before reading its
out-of-sample numbers. Every variant's out-of-sample row is reported regardless.

## 10. Variants (7 counted)

| id | rule | direction | trend filter |
|---|---|---|---|
| G2-01 | RSI(2) < 10 | long only | none |
| G2-02 | 3 down closes | long only | none |
| G2-03 | RSI(2) < 10 / > 90 | long and short | none |
| G2-04 | 3 down / 3 up closes | long and short | none |
| G2-05 | RSI(2) < 10 | long only | 200-day |
| G2-06 | 3 down closes | long only | 200-day |
| G2-07 | RSI(2) < 10 / > 90 | long and short | 200-day |

Not counted, reported only as information: a zero-cost run and a spread-only run (swap set to zero, a bound on how much
today's high swap rates hurt in the zero-rate years).
