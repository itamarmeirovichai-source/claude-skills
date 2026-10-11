# D2 pre-registration — forex/CFD multi-asset trend and carry (wave 1)

Written 2026-10-11, **before any backtest was run**. The only thing looked at before
writing this was data availability: which FRED and Yahoo series exist, and their first
and last dates. No returns, signals or statistics were computed. The commit that adds
this file and `D2.csv` comes before the commit that adds any result.

Bar: one-sided z(0.05/260) = **3.5504** (fixed for the whole wave).

## 1. Data (free, daily)

| block | instruments | source | from |
|---|---|---|---|
| FX vs USD (9) | EURUSD, GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD, USDSEK, USDNOK | FRED H.10 noon NY rates (DEXUSEU, DEXUSUK, DEXJPUS, DEXSZUS, DEXCAUS, DEXUSAL, DEXUSNZ, DEXSDUS, DEXNOUS) | 1971; EUR 1999-01-04 |
| FX crosses (8) | EURGBP, EURJPY, EURCHF, GBPJPY, AUDJPY, EURAUD, AUDNZD, CADJPY | triangulated from the same FRED rates | as legs |
| Index CFDs (10) | US500 ^GSPC, US100 ^NDX, US30 ^DJI, GER40 ^GDAXI, UK100 ^FTSE, JP225 ^N225, FRA40 ^FCHI, AUS200 ^AXJO, EU50 ^STOXX50E, HK50 ^HSI | Yahoo chart API, close | each series' start |
| Commodities (3) | XAUUSD ← GLD, XAGUSD ← SLV, USOIL ← USO (adjusted close) | Yahoo | 2004-11 / 2006-04 / 2006-04 |
| Bond proxies (2, variant D2-07 only) | US10Y, US30Y | constructed from FRED DGS10 / DGS30 | 1990 |
| Short rates | USD, EUR, GBP, JPY, CHF, CAD, AUD, NZD, SEK, NOK | FRED OECD 3-month interbank `IR3TIB01xxM156N`; EUR = Germany (DEM) series; JPY before 2002-04 and CHF before 1999-07 = call-money `IRSTCI01xxM156N`; GBP after 2026-01 = `IRSTCI01GBM156N`; otherwise last value carried forward | monthly |

The monthly rate for month m is treated as known only from the first trading day of
month m+2, a one-month publication lag. HKD is pegged, so HK50 uses the USD rate.

**Calendar:** weekdays on which FRED has an EURUSD or GBPUSD fix. Prices on other
calendars are carried forward, so a day with no trade has zero return.

## 2. Returns of a fully financed position (before broker markup and trading costs)

- FX pair BASE/QUOTE, long: `S_t/S_{t-1} - 1 + (i_base - i_quote) * dcal/365`, where
  `dcal` is the number of calendar days since the last row. This is covered interest
  parity, the interbank part of the swap.
- Index CFD, long: `P_t/P_{t-1} - 1 + (dy - i_local) * dcal/365`. The dividend yield
  `dy` is a fixed constant per index: US500 1.9%, US100 0.9%, US30 2.2%, GER40 0
  (the DAX is a total-return index), UK100 3.6%, JP225 1.8%, FRA40 2.9%, AUS200
  4.0%, EU50 3.2%, HK50 3.3%. The FX translation of P&L is ignored.
- XAU/XAG/USOIL: `ETF total return - i_USD * dcal/365`. The ETF fee stays in, as a
  small extra cost.
- Bond proxy: a par bond at yesterday's yield, held one day.
  `y_{t-1} * dcal/365 - Dmod(y_{t-1}) * (y_t - y_{t-1}) - i_USD * dcal/365`, with the
  par-bond modified duration of 10 or 30 years.

## 3. Costs, per asset class (base = 1x; repeated at 2x on everything)

| class | per side, bp of notional traded (half-spread + commission + slippage) | swap markup, %/yr of gross notional held, charged per calendar day |
|---|---|---|
| FX majors (7) | 0.75 | 1.0 |
| FX crosses (8) | 1.5 | 1.0 |
| USDSEK, USDNOK | 3.0 | 1.0 |
| Index CFDs | 1.5 | 2.5 |
| Gold | 2.0 | 2.5 |
| Silver | 5.0 | 2.5 |
| Oil | 4.0 | 2.5 |
| Bond proxies | 2.0 | 1.0 |

The markup is charged on long and short positions alike, on top of the interbank
carry already in the return.

## 4. Signals and portfolio (all from data through the close of day t)

- **Asset vol:** `sigma_i` = 60-day rolling standard deviation of daily financed
  returns, annualized, at least 40 observations. A new asset enters only after 260
  days of history.
- **TSMOM multi-horizon (D2-01):** `s_i` = mean of sign(cumulative financed return over
  h days) for h in {21, 63, 126, 252}. Raw position = `s_i * 0.10 / sigma_i`.
- **Class balancing (all trend variants):** classes are FX (crosses and majors
  together), indices, commodities, and bonds when included. Inside a class each asset
  gets 1/N_class; classes get equal weight, 1/N_classes_available.
- **EWMAC (D2-09):** forecasts from EWMA crossovers 8/32, 16/64, 32/128 and 64/256
  on price. Each forecast is divided by price vol, scaled to an average absolute
  value of 10 using a fixed scalar (computed in-sample, 1990–2012, pooled across
  assets), capped at ±20 and averaged; `s_i` = forecast/10, capped at ±2.
- **FX carry, cross-sectional (D2-04):** the available currencies (USD plus the
  9 above) are ranked by lagged 3-month rate. Weight = rank minus the mean rank,
  scaled so the sum of |w| = 1, and divided by `sigma` of the currency's USD pair
  relative to the median `sigma`. Implemented as positions in the 9 USD pairs.
- **FX carry, time-series (D2-05):** for each USD pair, sign(i_ccy - i_USD) times
  `0.10/sigma`, equal weight.
- **Sleeve vol target:** each sleeve's raw daily return series is scaled to 10%/yr by
  `k = 0.10 / (126-day realized vol of the raw sleeve returns through t-1)`, with
  k capped at 4. The cost of that scaling is in the turnover.
- **Stacks:** STACK = 0.5·TREND + 0.5·CARRY, each already at 10%, then the combined
  portfolio is scaled again to 10% by the same rule. The stack holds positions; the
  costs come from the summed positions, not the summed sleeve P&L.
- **Execution:** the target position is set from data through the close of day t and
  earns the return of day t+1 (lag 1). Trades are executed in full every day, except
  with a no-trade buffer: an asset is not traded when |target - current| < 10% of
  |target|.
- **Look-ahead companion:** the identical run with lag 2. **The worse of lag 1 and
  lag 2 decides the gate.**
- **Margin check (reported):** the gross notional per class is checked against
  FTMO-type swing leverage (FX 1:30, indices 1:15, metals 1:9, oil 1:5) at the vol
  chosen for the prop simulation. When margin use is over 80% of equity, every
  position is scaled down that day; this is applied in the prop simulation.

## 5. Split

- **In-sample (IS): 1990-01-01 to 2012-12-31.** It is used only to (a) compute the
  EWMAC forecast scalar, (b) pick the headline variant, which is the one with the
  highest IS net Sharpe at 1x cost and lag 1, and (c) pick the volatility for the prop
  simulation.
- **Out-of-sample (OOS): 2013-01-01 to the last common date (about 2026-10-09).**
  Nothing in the rules is chosen on it.

## 6. Gate (per variant, on OOS daily net returns at 10% vol)

Pass only if all of these hold:

1. t ≥ 3.5504, where t = min(iid t, Newey-West t with 10 lags) of the mean daily net
   return;
2. the 5th percentile of the mean, from a stationary bootstrap (mean block 20 days,
   10,000 draws, seed 0), is above 0;
3. the look-ahead test passes: lag-2 companion (the worse result decides), and
   positions through day d stay identical when every input after d is multiplied by
   random noise (20 random d);
4. the truncation test passes: positions through d are identical when the data is
   cut at d (20 random d).

Everything is done at 1x cost, and the 2x result is reported next to it. A variant
with t ≥ 3.5504 at 1x but not at 2x is reported as "passes at 1x only".

## 7. Prop simulation (FTMO-type swing; the static max loss and daily limit the plan gives)

- **Phase 1:** +10% target. **Phase 2:** +5%. Max loss: equity at or below 90% of
  initial. Daily loss: a day's loss ≥ 5% of the start-of-day balance. Minimum 4
  trading days per phase. No time limit, but a phase not passed within 504 trading
  days counts as abandoned, which is a fail.
- **Intraday buffer:** with daily data the simulation cannot see intraday lows, so a
  breach is counted at a close-to-close day loss of **4%** or worse, or equity at
  **91%** or below (1 point of buffer on each). This is conservative.
- **Funded:** the same limits. Every 21 trading days, if equity is above initial,
  the trader is paid 80% of the profit and equity resets to initial. The account is
  run for 504 trading days or until a breach. The fee is $600 per 100k account, and
  it is refunded with the first payout.
- **Paths:** a stationary bootstrap (mean block 20 days, 10,000 paths per volatility)
  of the headline's daily net returns, scaled linearly from 10% to the chosen
  annualized vol. Vol grid: 4% to 30% in 2-point steps.
- **Vol choice:** the vol that maximizes expected net payout per attempt, E =
  P(pass) × E[payouts + refund | funded] − fee, on **IS** returns. That vol is then
  reported on **OOS** returns, at 1x and 2x cost. The OOS-optimal vol is printed as a
  reference only and marked as such.
- **Reported:** P(pass phase 1 and 2), P(blow) during the evaluation, median days to
  pass, funded 2-year survival, expected payouts, and expected net per $ of fee.

## 7a. What is counted (D2.csv `count`)

There are 9 counted variants: D2-01 to D2-09. The per-class breakdowns (FX only,
indices only, commodities only), the per-period tables, the lag-2 companion and the
2x cost repeat are diagnostics of a counted variant. They are not eligible as the
headline and are not counted separately. Nothing else will be run as a strategy. Any
added rule would need a new row with the next id, written before it is run, and the
total stays at 15 or fewer.

## 8. Verifier and red team

- A verifier sub-agent re-implements the headline from this document alone. It must
  match the OOS net Sharpe within 0.05.
- A red-team sub-agent tries to refute the headline: data errors, survivorship (index
  choice), dividend and swap assumptions, regime dependence, and costs.
