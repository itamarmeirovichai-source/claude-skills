# H0018: opportunistic insider purchases — result

**Verdict: FAIL. Stopped at Stage 2.** Out of sample (2017 onward), the strategy trailed SPY by
0.50% a month (t = −1.66). To pass it needed to beat SPY with t ≥ 3.48. No robustness tests
(Stage 3) or paper-trading spec (Stage 4) were run, as the pre-registration requires.

Run date: 2026-10-06. Ledger row: `agents/ledger.csv` H0018 (bar: N = 196, one-sided
alpha 0.05/196, t ≥ 3.48).
Scripts: `agents/daily/insider-H0018/`. Printed outputs: `agents/daily/insider-H0018/output/`.

## What was tested (as pre-registered)

- **Data:** SEC Form 4 open-market purchases (code P) by officers and directors.
- **Routine vs opportunistic:** A purchase is *routine* if the same insider also traded in the
  same calendar month in each of the 3 prior years. Every other purchase is *opportunistic*.
  This follows Cohen, Malloy and Pomorski (2012).
- **Portfolio:** At each month-end, buy an equal-weight basket of every stock with at least one
  opportunistic purchase filed that month. Hold it for one month.
- **Costs and filters:** 20 bp round-trip cost. Stocks priced under $5 are excluded.
- **Benchmark:** SPY, total return.
- **Periods:** In-sample is signal months 2009–2016. Out-of-sample is 2017 to the latest month.
- **Decision rule:** Uses the out-of-sample mean monthly excess return over SPY.

## Implementation details (set in the script docstrings before any return was computed)

- **Filings:** Only original Form 4s are used (amendments are skipped), non-derivative table only.
  A purchase is code P, "acquired", and filed by an owner whose role includes Officer or Director.
- **What counts as "traded" for the routine test:** Any open-market buy (P) or sell (S) by the same
  reporting-owner CIK, in any company, dated by transaction date.
- **Which purchases are scored:** Only purchases dated 2009 or later, so that all 3 look-back
  years fall inside the data, which starts in 2006.
- **Signal month:** The month of the filing date.
- **Formation date:** The last SPY trading day of the signal month. Each stock is bought at that
  day's close and sold at the close on the last trading day of the next month. If a stock's price
  series stops mid-month, its last available price is used.
- **$5 filter:** Uses the actual traded price that day. Yahoo's split adjustment is undone using
  Yahoo's split history.
- **Wrong-ticker guard:** A stock is dropped if its price at formation is more than 2× away from
  the median Form 4 purchase price. This catches tickers that Yahoo has since given to a
  different company.
- **Turnover and costs:** Turnover is half the sum of absolute weight changes against the
  drifted prior basket. The monthly cost is turnover × the round-trip cost.
- **Sharpe:** Annualised mean ÷ standard deviation of the monthly net return, with no risk-free rate
  deducted.
- **Months are labelled by the holding month.** In-sample is therefore holding months 2009-02 to
  2017-01. Out-of-sample is 2017-02 to 2026-04.

## Stage 1 — data

| Item | Value | Source |
|---|---|---|
| SEC quarterly zips used | 2006Q1–2026Q1 (81 files) | `output/sec_download_log.txt` |
| SEC 2026Q2+ | HTTP 404, not yet published, so the out-of-sample period ends with holding month 2026-04 | same |
| Officer/director purchase rows (2009+) | 440,544, of which 10.9% are routine | `build_signals.py` stdout |
| Distinct tickers with an opportunistic signal | 11,495 | `output/surv.txt` |
| Price source | Yahoo via yfinance. Stooq was blocked (connection reset through the proxy). | — |
| Tickers requested (signals + SPY) | 11,524 | `output/price_fetch_summary.txt` |
| Tickers with no Yahoo price history | **6,385** (55%) | same; list in `output/tickers_no_price_history.csv` |

**Rate limiting.** Yahoo rate-limited the first download pass (HTTP 429). Every ticker named in a
rate-limit error was requested again slowly (`fetch_prices_retry.py`), which recovered 850 of
them. A spot check of large live names (AAPL, CSCO, COST, CI, CSX, JPM, XOM and others) found
none missing.

### Survivorship and delisting bias (required by the ledger)

Yahoo drops delisted tickers, so most of the missing history belongs to companies that were
delisted, acquired or renamed. Source: `survivorship.py` → `output/surv.txt`.

| Period | Stock-month signals | Share with no price history | Share of purchase dollars with no price history |
|---|---|---|---|
| In-sample 2009–2016 | 51,204 | 54.7% | 40.6% |
| Out-of-sample 2017–2026 | 47,111 | 28.9% | 8.7% |

At the signal level, the backtest dropped stock-months for these reasons:

- 45,713 because the ticker had no price on the formation date.
- 1,589 because of the wrong-ticker guard.
- 11,458 because the price was under $5.

**What this means:**

- **The tested baskets are biased toward survivors.** This is worst in-sample, where more than
  half of the signals are missing.
- **The direction of the bias isn't known.** Delisting for failure tends to cut returns, while
  being acquired tends to raise them.
- **It is very unlikely to change the verdict.** Out-of-sample is the cleaner sample: only 8.7% of
  purchase dollars are missing there. For a pass, the missing names would have to move the
  result from t = −1.66 to t ≥ +3.48. That last point is a judgement, not something I measured.

## Stage 2 — pre-registered test

Source: `backtest.py` → `output/backtest_opp.txt`. Monthly series: `output/monthly_opp_20bp.csv`.

### Pre-registered result (20 bp round-trip)

| | In-sample (2009-02 to 2017-01) | **Out-of-sample (2017-02 to 2026-04)** |
|---|---|---|
| Months | 96 | 111 |
| Mean monthly return (net) | 1.50% | 0.78% |
| SPY mean monthly return | 1.31% | 1.28% |
| Mean monthly excess vs SPY | +0.19% | **−0.50%** |
| t-stat of excess | 0.92 | **−1.66** |
| Sharpe (annualised, net return) | 1.17 | 0.48 |
| Max drawdown (net) | −18.4% | −33.9% |
| Average stocks per month | 160.9 | 217.1 |
| Average monthly turnover | 0.78 | 0.82 |

**Decision:** The out-of-sample mean excess must be above 0 with t ≥ 3.48. It is −0.50% with
t = −1.66, so the hypothesis **fails**.

### Sensitivity only (not a choice): 50 bp round-trip

| | In-sample | Out-of-sample |
|---|---|---|
| Mean monthly excess vs SPY | −0.04% | −0.74% |
| t-stat of excess | −0.21 | −2.48 |
| Sharpe | 0.98 | 0.33 |
| Max drawdown | −19.4% | −34.5% |

## In plain English

Buying every stock where an officer or director made an "unusual" (non-calendar-habit) purchase
didn't beat simply holding SPY. In-sample (2009–2016) it was about level with SPY: +0.19% a month,
which is statistically nothing. From 2017 on it lagged SPY by about half a percent a month and
had a deeper drawdown. Higher trading costs only make it worse.

The anomaly published in 2012 doesn't show up in this equal-weight, month-end version after its
publication. That holds even before allowing for the many signals that couldn't be priced.

## Not done (per the stop rule)

- Stage 3 robustness: value-weighting, a market-cap or $10 filter, next-day-open entry, and the
  routine-only placebo.
- Stage 4 paper-trading spec.

Running any of these now would be an unregistered extra test and would need its own ledger row.

## Reproduce

All commands are run from a scratch directory. Raw data isn't committed: the SEC extract is about
49 MB and the prices about 213 MB.

```
python -I fetch_sec.py sec sec_ps.parquet              # SEC zips -> Form 4 P/S rows
python -I build_signals.py sec_ps.parquet signals.csv   # routine/opportunistic classification
python -I fetch_prices.py signals.csv prices.parquet    # Yahoo daily prices + SPY
python -I extract_ratelimited.py fetch_prices.out prices.parquet.missing.csv ratelimited.csv  # 1,974 of 7,235 missing were 429'd
python -I fetch_prices_retry.py prices.parquet ratelimited.csv   # retry them slowly
python -I backtest.py signals.csv prices.parquet        # Stage 2 table + decision
python -I survivorship.py signals.csv prices.parquet    # survivorship table
```

Yahoo data changes over time, so a rerun can differ slightly in which tickers are covered.
