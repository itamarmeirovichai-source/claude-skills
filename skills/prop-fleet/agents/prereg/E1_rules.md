# E1 pre-registration: stock breadth on FTMO stock CFDs (wave 2)

Written 2026-10-11 by the E1 head, **before any backtest**. Before writing this I looked only
at data availability and FTMO's contract specifications:
- which tickers Yahoo returns;
- how many S&P 500 members per day have trusted price history (`agents/daily/w2-stocks/coverage.txt`);
- FTMO's symbol JSON.

I computed no returns, signals or statistics. The commit that adds this file and `E1.csv`
comes before the commit that adds any backtest code or result.

**Bar:** one-sided z(0.05/270) = **3.5603** (wave 2, fixed). **Budget:** 11 counted variants (limit 15).

## 0. FTMO facts that shape the design

These come from FTMO's own pages, fetched 2026-10-11. Quotes and URLs are in `references/w2-stocks.md` §1.
- **59 stock CFDs: 46 priced in USD and 13 in EUR.**
- **Commission:** 0.004% of value.
- **Leverage:** 1:1 on Swing (1:3.33 on Standard).
- **Swaps:** quoted in points and negative on both sides for every stock.
- **US hours:** 09:35–16:00 New York.
- **Order limits:** 200 orders open at once; 2,000 positions a day.

## 1. Universe

- **Membership.** Point-in-time S&P 500 membership comes from fja05680/sp500, `S&P 500 Historical Components & Changes (Updated).csv`. The row dated d applies from d until the next row.
- **Prices.** Yahoo chart API daily data:
  - O/H/L/C are split-adjusted;
  - AC is adjusted for splits and dividends;
  - V is volume.

  The calendar is SPY's trading days, starting 1999-01-04.
- **Trusted history ("covered").** A member interval counts as covered only if Yahoo's history for that ticker starts no later than 5 trading days after the interval begins, or the interval begins on the first calendar day. This drops ticker symbols that were later reused by another company.
- **Eligible on day t (universe A, the bias-reduced research universe).** All five must hold:
  1. covered member on day t;
  2. C_t ≥ $5;
  3. at least 55 valid daily returns in the last 60 days;
  4. AC valid on day t;
  5. V_t > 0.
- **Universe B (FTMO-tradable).** A ∩ {the 46 FTMO USD stock CFDs, matched to the membership ticker of that day (BRK.B; GOOG only, not GOOGL; renamed tickers such as FB→META count only under the ticker FTMO lists)}. Only names that were S&P 500 members on day t enter. B carries extra selection bias, because FTMO's list was chosen in 2026.
- **Bias that remains.** About 35% of tickers that were ever members have no Yahoo history (delisted, acquired or renamed). Covered share per day ranges from 45% (1999) through 74% (2015) to 98% (2026). Missing names are mostly failures and takeover targets.

## 2. Returns

- **Total:** r_t = AC_t/AC_{t−1} − 1.
- **Dividend factor:** f_t = (AC_t/C_t)/(AC_{t−1}/C_{t−1}).
- **Overnight:** on_t = O_t·f_t/C_{t−1} − 1.
- **Intraday:** id_t = C_t/O_t − 1, so that (1+on)(1+id) = 1+r.
- **Invalid open.** When O_t is missing, ≤ 0 or outside [L_t, H_t], the overnight/intraday split for that stock-day is missing. It then counts as 0 return in O/I strategies, and the count of such cases is reported.
- **Market:**
  - mkt_t is the SPY total return;
  - the hedge instrument is the US500 CFD, modelled as SPY total return minus a 1.3%/yr dividend yield. CFD index swaps embed the dividend, which is handled in the swap below.
- **Beta.** β_i,t is the 60-day OLS beta of r on mkt, using days t−59..t. It is clipped to [0, 3]; when missing it is 1.

## 3. Variants (all signals use data up to the close of day t)

**Weights.** Weights are "rank weights" unless a variant says otherwise. Take the cross-sectional rank of the signal among eligible names, subtract the mean rank, and scale so that Σ|w| = 1: half the book long, half short, dollar-neutral.

| id | name | signal / rule | rebalance | holding |
|---|---|---|---|---|
| E1-01 | REV5-D | −(5-day total return) | daily | close→close |
| E1-02 | REV5-W | as E1-01 | weekly: last trading day of each week; weights held until the next rebalance | close→close |
| E1-03 | RREV5-W | −Σ over the last 5 days of the residual e = r − β·mkt | weekly | close→close |
| E1-04 | REV5-LH | long-only: the half of eligible names with the lowest 5-day return, weights ∝ (median rank − rank), Σw = 1, hedged with a short US500 of Σ w_i·β_i | weekly | close→close |
| E1-05 | PEAD-SUE | Nasdaq earnings calendar (date d, EPS "surprise" %, 2008 on). d0 = first trading day ≥ d. Enter at the close of d0+1. Long if surprise > 0, short if < 0; N/A or 0 are skipped. Hold 20 trading days. Each day, active events are equal-weighted with Σ\|w\| = 1. The net Σw·β is hedged with US500. | daily | close→close |
| E1-06 | PEAD-EAR | as E1-05, but the sign is the earnings-announcement abnormal return Σ(r − β·mkt) over d0 and d0+1 | daily | close→close |
| E1-07 | GAPVOL | proxy with no dates (from 1999). Event on day t when V_t > 3 × median(V over t−60..t−1) and \|r_t − β·mkt_t\| > 3%. Enter at the close of t in the sign of the abnormal return. Hold 20 days. Same weighting and hedge as E1-05. | daily | close→close |
| E1-08 | TOW-W | rank(Σ on over 21 days) − rank(Σ id over 21 days), using log sums. High = long. | weekly | close→close |
| E1-09 | OVN-ONLY | rank of the 21-day Σ overnight return. High = long. | daily | enter at the close of t, exit at the open of t+1 |
| E1-10 | INTRA-TOW | −rank of the 21-day Σ overnight return. High past-overnight stocks are short. | daily | enter at the open of t+1, exit at the close of t+1 |
| E1-11 | STACK | E1-03 + E1-06 + E1-08: each sleeve's weights are scaled by 1/(its in-sample 1999/2008–2014 gross vol), positions are summed, then rescaled to Σ\|w\| = 1. Costs are charged on the netted positions. | daily | close→close |

**Execution lag.**
- **Lag 0:** the weights from close t earn day t+1 (or the night or session of t+1).
- **Lag 1:** the same weights earn one day later.

Lag 0 assumes an EA can trade on prices a few minutes before the close, which are close to the closing prices. **The worse of lag 0 and lag 1 decides.** That is the day-2 look-ahead rule.

## 4. Costs (FTMO, per side, on traded notional)

- **Commission:** 0.4 bp (0.004%).
- **Half-spread:** FTMO does not publish spreads. Assumed:
  - universe B: 2 bp;
  - universe A: 3 bp;
  - US500 hedge: 0.5 bp.

  The open and close trades of E1-09 and E1-10 get +2 bp extra slippage, because FTMO's session opens at 09:35, after the official open price.
- **Swap.** Charged on the notional held over each close, per calendar night (Friday→Monday = 3).
  - Rates are taken from FTMO's points today, using MT5 semantics (points × 0.01 × shares per night). As % of notional, the mean over the 46 USD names is **long −8.40%/yr, short −6.64%/yr**, and they apply to both universes.
  - US500: long −8.37%/yr, short +0.42%/yr.
  - These are today's constants, applied to every year. That is conservative for 2015–2021, when policy rates were near zero.
- **2× cost.** Commission, spread and swap are all doubled. Reported next to the main result.

## 5. Sizing

The book is gross 1.0 × equity (Σ|w| = 1). Swing stock leverage is 1:1, so gross may not exceed about 1. The prop simulation uses min(1.0, the gross that targets the in-sample vol) and never more than gross 1.0 on stocks. The US500 hedge uses 1:15 leverage.

## 6. Split and statistics

- **In-sample:** 1999-04-01 (2008-04-01 for E1-05/06) to 2014-12-31.
- **Out-of-sample:** 2015-01-02 to the last data day (about 2026-10-09).
- **Rule choice.** No parameter is chosen in-sample. In-sample decides only:
  - the STACK scalars;
  - the **headline**: the variant with the highest in-sample net Sharpe at 1× cost, on universe A, at the worse lag.
- **Gate** (the out-of-sample daily net return of the gross-1 book):
  - t = min(iid t, Newey-West(10) t) ≥ **3.5603**;
  - a stationary block bootstrap (block 20, 10,000 draws) gives a mean p5 > 0;
  - the truncation and perturbation look-ahead tests (20 random dates) pass 20/20.
- **What must pass.** A variant passes only if it passes on **universe A and on universe B**, at 1× cost and the worse lag.
- **Also reported:**
  - out-of-sample Sharpe, CAGR, max drawdown and worst day;
  - turnover (one-way per year);
  - average and maximum positions against FTMO's 200-orders-at-a-time and 2,000-positions-a-day limits.
- **Prop simulation (only if the gate passes).** FTMO Swing $100k:
  - targets 10% then 5%;
  - 10% static maximum loss;
  - 5% daily loss;
  - at least 4 days per phase;
  - fee $630, refunded at the first payout;
  - 80% split;
  - payout every 21 trading days on a positive balance;
  - stationary-bootstrap paths of out-of-sample net returns.

  Reported: pass rate and the yearly payout per $100k.
