# D4 (Intraday breadth) — pre-registered specification

Written 2026-10-11 by the D4 head, **before any strategy return was computed**. Committed and
pushed together with `D4.csv` before `breadth.py` exists. The only data looked at before this
file: the repository file listing, the first lines of two CSV files (format), and the bar counts
and first/last timestamps that `fetch.py` prints per market. No returns of any kind.

Five counted variants (D4-01..D4-05). Budget 15. The wave bar is fixed: one-sided
z(0.05/260) = **3.5504**.

## 1. Data

- Oanda v20 1-minute MID candles from github.com/FutureSharks/financial-data @ 7ba1d404,
  2005-01..2020-05 (`fetch.py`). Expected clock UTC.
- HistData 1-minute bars from the same repo: GRXEUR (DAX), ETXEUR (EuroStoxx 50),
  2010-11..2018-12. Expected clock fixed EST (UTC-5, no DST) → +5 h to UTC.
- `data_check.py` verifies the clock of every market (outcome-free: mean |1m return| by UTC
  minute in Jan-Feb vs Jun-Aug around each market's known open) and reports gaps (bars per
  session, missing sessions). If a market's clock is not as expected, it is corrected to the
  clock the check shows and the correction is written in the report; if it cannot be
  determined, the market is dropped. This is decided before any strategy return is computed.
- Bond CFDs (DE10YB, UK10YB, USB02Y, USB10Y) are fetched but **not in the basket**: we know of
  no forex/CFD prop firm that offers them. NQ (hindsight) is not used: 2020-2025 overlaps no
  other market here, and it was seen in H0020-H0022.

## 2. Markets, sessions (local exchange time, DST via zoneinfo) and cost per side

| market | O (open) | C (close) | tz | cost/side bp |
|---|---|---|---|---|
| EUR_USD | 08:00 | 16:00 | Europe/London | 0.5 |
| GBP_USD | 08:00 | 16:00 | Europe/London | 0.7 |
| USD_CAD | 08:00 | 16:00 | Europe/London | 0.8 |
| AUD_USD | 08:00 | 16:00 | Europe/London | 0.7 |
| EUR_JPY | 08:00 | 16:00 | Europe/London | 0.8 |
| AUD_JPY | 08:00 | 16:00 | Europe/London | 0.9 |
| SPX500_USD | 09:30 | 16:00 | America/New_York | 1.0 |
| NAS100_USD | 09:30 | 16:00 | America/New_York | 1.0 |
| US2000_USD | 09:30 | 16:00 | America/New_York | 1.5 |
| UK100_GBP | 08:00 | 16:30 | Europe/London | 1.0 |
| FR40_EUR | 09:00 | 17:30 | Europe/Paris | 1.0 |
| NL25_EUR | 09:00 | 17:30 | Europe/Amsterdam | 1.5 |
| JP225_USD | 09:00 | 15:00 | Asia/Tokyo | 1.5 |
| AU200_AUD | 10:00 | 16:00 | Australia/Sydney | 1.2 |
| GRXEUR (DAX) | 09:00 | 17:30 | Europe/Berlin | 0.8 |
| ETXEUR (ESTX50) | 09:00 | 17:30 | Europe/Berlin | 1.5 |
| XAU_USD | 08:20 | 13:30 | America/New_York | 1.0 |
| WTICO_USD | 09:00 | 14:30 | America/New_York | 2.5 |
| NATGAS_USD | 09:00 | 14:30 | America/New_York | 8.0 |
| CORN_USD | 08:30 | 13:15 | America/Chicago | 10.0 |
| SOYBN_USD | 08:30 | 13:15 | America/Chicago | 6.0 |
| WHEAT_USD | 08:30 | 13:15 | America/Chicago | 10.0 |
| SUGAR_USD | 03:30 | 13:00 | America/New_York | 10.0 |

FX uses the London open for every pair (one rule set). Indices use the local cash open/close.
Commodities use the main exchange day session.

**Cost per side** = half a typical raw/ECN or prop-CFD spread + commission (FX: about
$3.5 per $100k per side = 0.35 bp) + 0.1-0.3 bp slippage. These are estimates fixed now, not
measured (the data are mid prices). A flip costs 2 sides, an open or close 1 side. No swap:
every position is flat at C, and no session crosses the 17:00 New York rollover. **Cost ×2**
doubles every number; it is run and reported for every variant.

## 3. Eligibility (outcome-free, uses volatility only)

A market is in the basket only if (a) it has ≥ 250 valid sessions in its in-sample period and
(b) its round-trip cost (2 × cost/side) ≤ 0.10 × σ_IS, where σ_IS is the standard deviation, in
bp, of its session log return log(M(C)/M(O)) over its in-sample sessions. This drops markets
whose cost is too large a share of a day's move. It is computed from prices only, before any
strategy return.

## 4. Splits

- **Time:** in-sample (IS) = sessions with local date 2005-01-01..2012-12-31; out-of-sample
  (OOS) = 2013-01-01..2020-05-13, the end of the Oanda files (HistData markets: IS 2010-11..2012-12, OOS 2013-01..2018-12).
- **Markets:** held-out set H = GRXEUR, ETXEUR (different source) + 4 eligible Oanda markets
  drawn by `numpy.random.default_rng(20261011).choice(sorted(eligible_oanda), 4,
  replace=False)`. No strategy number is computed for H in the IS period (the code refuses).
  Design set D = the other eligible markets.
- IS chooses nothing (rules are fixed here). It is used only for condition G4.

## 5. Common definitions

- Bars are indexed by their open time t (UTC); a bar covers [t, t+1 min).
- **Mark M(T)** = close of the last bar with open time in [T−10 min, T−1 min]; missing if none.
- **Fill F(T)** = open of the first bar with open time in [T, T+10 min]; missing if none.
- A session (market m, local date d) is **valid** if d is a weekday and M(O+30), M(C) and
  F(O+30) all exist. Invalid sessions trade nothing and score 0.
- **Previous close** Cprev = M(C) of the most recent earlier valid session of m within 5
  calendar days; else the gap-based signals (D4-01, D4-02) skip that session.
- **Sizing (equal volatility):** σ̂(m,d) = standard deviation of log(M(C)/M(O)) over the
  previous 60 valid sessions of m (needs ≥ 40, else no trade). Session P&L in return units r
  (side × (exit−entry)/entry − costs, summed over the day's fills) is scaled to
  u = r × (0.01 / σ̂). Every market therefore targets 1% session-return volatility.
- **Basket daily return** for a local date d = (1/K) Σ_m u(m,d), K = number of basket markets
  in that split (fixed; markets without a trade that day contribute 0). Dates = weekdays with
  at least one valid session in the split.

## 6. The five counted variants

- **D4-01 Gao last half hour** (Gao, Han, Li & Zhou 2018, JFE): s = sign(log M(O+30) − log
  Cprev). If s ≠ 0, enter side s at F(C−30), exit at M(C).
- **D4-02 Open move → rest of session** (same signal, longer hold): s as in D4-01. Enter side
  s at F(O+30), exit at M(C).
- **D4-03 TWAP trend, 30-minute decisions** (H0022 cadence; TWAP because Oanda/HistData volume
  is tick count or zero): TWAP(T) = mean of typical price (h+l+c)/3 over bars with open time in
  [O, T). Decision times T_k = O+30, O+60, … while T_k ≤ C−30. At T_k desired = +1 if
  M(T_k) > TWAP(T_k), −1 if <, unchanged if equal (flat before the first non-equal). A missing
  M(T_k) skips that decision. Changes fill at F(T_k) (missing fill → no change). Flat at M(C).
- **D4-04 Opening-range breakout, 30 minutes:** OR high/low = max high / min low of bars with
  open time in [O, O+30). For each bar with open time t in [O+30, C−30): if its close > OR high
  → go long; if close < OR low → go short; fill at the open of the next bar (must exist within
  10 min, else no trade). Only the first breakout of the session trades. Stop = the opposite OR
  side: exit at the stop when a later bar's low ≤ stop (long) / high ≥ stop (short); if that
  bar opens beyond the stop, exit at its open. Otherwise exit at M(C). No target.
- **D4-05 Fixed blend:** basket daily return = mean of D4-01..D4-04 basket daily returns.

## 7. Gate (each variant on its own; the wave bar 3.5504)

PASS only if all hold:

- **G1** OOS basket (D ∪ H) net daily mean > 0 with one-sided t ≥ 3.5504, using the lower of
  the iid t and the Newey-West t (5 lags).
- **G2** OOS bootstrap p5 of the net daily mean > 0, using the lower of 10,000 iid resamples
  (seed 0) and 10,000 moving-block resamples (block 20 days, seed 0).
- **G3** OOS held-out markets H alone: net daily mean > 0.
- **G4** IS design markets D: gross daily mean > 0.
- **G5** Look-ahead: (a) truncation test — for 300 random (market, session) pairs (seed 0) and
  every decision/bar time T, the position held at T computed from bars with open time < T only
  equals the full-data position; σ̂ uses earlier sessions only. (b) A unit-test suite on
  synthetic bars covering fills, flips, stops and costs passes.

Reported, not decisive: cost ×2 for every variant (the worse of base and ×2 is printed next to
the main result), annualized Sharpe (√252), max drawdown at 10% annual vol, per-year table,
per-market net Sharpe, mean pairwise correlation of per-market daily P&L and effective number
of markets, D-only OOS, turnover.

## 8. What is not allowed after this commit

No change of markets, sessions, costs, windows, sizing or splits. No new variant without a new
counted row. A bug fix is allowed only if written in the report with before/after numbers.
