# W4 · G2: short-term mean reversion across FTMO index CFDs

**Verdict: FAIL. None of the 7 pre-registered variants passes the gate, and none comes close.**

- **Best result:** the headline is G2-06 (3 down closes, long only, 200-day filter), chosen by its in-sample Sharpe. Out of sample (2013–2026) it has net Sharpe **0.24, t 0.90** against a bar of 3.5914. Its bootstrap p5 is below zero and its **alpha t is −0.63**.
- **Beta beat every variant.** Buy-and-hold of the same basket had a Sharpe of **0.72**, and every variant's alpha t against it is negative.
- **Costs are not the only problem.** Even at **zero cost**, the best out-of-sample t is 2.73 (G2-06, close fill, Sharpe 0.72).
- **The edge has decayed.** Before 2013 the classic rule earned about +0.5% a trade on US500 and +0.6% on FRA40. Since 2013 it still earns on the US indices, but it is gone on UK100, FRA40, EU50 and HK50.
- **FTMO's long swap takes about half of what is left.** It is 6.5–8.3% a year on these index CFDs.
- **The prop account cannot hold it either.** Scaled to 15–20% volatility, the book breaks FTMO's 5% daily-loss limit **16–43 times** in 2013–2026. The worst scaled day is −14% to −28%, all in clustered crashes such as March 2020.
- **Checks:** the independent verifier agrees on every row to within 0.01 in t. The red team found no bug, and nothing it tried rescued the result.

Written 2026-10-12 by the G2 head (wave 4).

- **Pre-registration:** `agents/prereg/G2_rules.md` and `agents/prereg/G2.csv`, committed and pushed in **6107458 (2026-10-12 03:26:30Z)**, before any backtest code existed.
- **Budget:** 7 variants counted (the limit is 15). The ledger's N rises by 7.
- Nothing was bought, signed up for or contacted.

Code and output are in `agents/daily/w4-meanrev/`:

| file | what it is |
|---|---|
| `meanrev.py` | engine: data, signals, fills, costs, book, statistics, look-ahead test |
| `report.py` → `run.txt`, `results.csv` | every variant, both fills, costs 0 / spread-only / 1× / 2×, gate, per-year table, scaled breaches |
| `prop.py` → `prop.txt` | $ per $100K FTMO slot, using the F2-09 stress model (`agents/daily/w3-volrisk/stress_model.py`) |
| `diag.py` → `diag.txt` | gross return per trade, by market, in and out of sample (information only) |
| `test_meanrev.py` | unit tests: RSI by hand, exit rule, P&L, swap, truncation; 4 pass |
| `verifier/` | independent re-implementation from the rules alone, and its output |
| `redteam/` | red-team report, script and output |

## 1. What was tested

- **Universe:** all 10 index CFDs in the brief are on FTMO's own symbol list. Source: `https://ftmo.com/wp-json/ftmo/symbols`, the data behind ftmo.com/en/symbols, fetched 12 Oct.
  - The instruments are US500, US100, US30, GER40, UK100, JP225, FRA40, AUS200, EU50 and HK50, all `.cash` spot CFDs.
  - FTMO charges **no commission** on any of them.
  - Swing leverage is 1:15, except HK50 at 1:9.
- **Data:** daily Yahoo index levels: ^GSPC, ^NDX, ^DJI, ^GDAXI, ^FTSE, ^N225, ^FCHI, ^AXJO, ^STOXX50E and ^HSI.
  - Every series runs from 1989 to 9–12 Oct 2026, except EU50, which starts in 2007.
  - The data cache is not committed; it is over 1 MB.
- **Rules:**
  - Entry: RSI(2) < 10 (Connors), or 3 down closes.
  - Exit: the first close above the 5-day moving average, or after 5 days.
  - The long/short versions also go short when RSI(2) > 90, or after 3 up closes.
  - The trend-filter versions go long only above the 200-day average, and short only below it.
- **Sizing:** every position gets the same risk: notional = (10%/√252)/σ60/10, set at entry. All 10 markets are pooled into one book.
- **Fills:** two versions.
  - Close fill: signal and fill both at day t's close.
  - Next-open fill: filled at the open of t+1. Where Yahoo's open is stale, the fill is at that day's close instead.
  - **The worse of the two decides.**
- **Costs:**
  - Swap: FTMO's own figures, converted to %/yr at today's index levels and charged per calendar night, in every year. Long: −8.3% (US), −6.5% (EU), −4.9% (JP225), −7.7% (AUS200), −6.7% (HK50). Short: about 0, between −1.6% and +0.4%.
  - Spread: FTMO does not publish spreads ⚠, so an assumed 1–4 bp per side is used.
  - Every run is repeated at 2× cost.
- **Split:** in sample is 1990 to 2012; **out of sample is 2013-01-01 to 2026-10-12.**
- **Benchmark:** buy-and-hold of the same basket at the same equal-risk weights.
  - Matched benchmark: the basket scaled to the strategy's average exposure.
  - Alpha t: the intercept t of the strategy regressed on the basket, with Newey-West errors (10 lags).

## 2. Gate (out of sample 2013–2026, worse fill, net at 1× cost)

| id | rule | fill | Sharpe | **t** | p5 bp/day | **alpha t** | beta | t at 2× | max drawdown (raw book) | worst day (raw) | trades/yr | avg exposure | gate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G2-01 | RSI2 long | close | −0.02 | **−0.07** | −0.69 | **−2.05** | 0.30 | −1.29 | −20.3% | −4.0% | 123 | 0.16 | FAIL |
| G2-02 | 3-down long | open | +0.12 | **+0.46** | −0.36 | **−1.52** | 0.24 | −0.96 | −11.8% | −2.9% | 125 | 0.15 | FAIL |
| G2-03 | RSI2 long/short | close | −0.40 | **−1.52** | −1.37 | **−2.10** | 0.15 | −2.97 | −27.6% | −4.0% | 284 | −0.08 | FAIL |
| G2-04 | 3-down/3-up long/short | open | −0.31 | **−1.22** | −1.03 | **−1.59** | 0.08 | −2.85 | −16.5% | −2.9% | 286 | −0.08 | FAIL |
| G2-05 | RSI2 long, 200-day filter | close | +0.07 | **+0.23** | −0.40 | **−1.19** | 0.17 | −1.03 | −12.5% | −1.9% | 78 | 0.10 | FAIL |
| **G2-06** | **3-down long, 200-day filter (headline)** | open | **+0.24** | **+0.90** | −0.15 | **−0.63** | 0.14 | −0.65 | −6.9% | −1.5% | 83 | 0.10 | **FAIL** |
| G2-07 | RSI2 long/short, 200-day filter | close | −0.00 | **−0.00** | −0.48 | **−1.04** | 0.13 | −1.30 | −11.9% | −1.9% | 108 | 0.06 | FAIL |

- **The bar** is t ≥ 3.5914, p5 > 0, alpha t ≥ 3.5914, and both look-ahead tests passing. Over 13.8 years, t of 3.59 needs a net Sharpe of about **0.97**.
- **Benchmark:** buy-and-hold of the equal-risk basket had a Sharpe of **0.72**. The matched benchmark (basket × average exposure) earns about the same per year as the long-only variants (e.g. 0.5%/yr for G2-06, against the variant's 0.5–0.6%), with far less work. Long-short exposure is negative, so its matched benchmark is negative too.
- **Look-ahead tests:** truncation and perturbation both pass **20/20** for every variant and both fills (`run.txt`; the verifier agrees).
- **Headline choice:** G2-06, the highest in-sample net Sharpe on the worse fill.

  | | G2-06 | G2-02 |
  |---|---|---|
  | in-sample Sharpe | 0.544 | 0.535 |
  | in-sample t | 2.65 | 2.61 |

  Even in sample, the pooled book never reached t 3.

### Cost sensitivity (out of sample, worse-fill variant shown at its own fill)

| id | Sharpe at 0 cost | t at 0 cost | Sharpe, spread only (no swap) | t, spread only (no swap) | Sharpe at 1× | Sharpe at 2× |
|---|---|---|---|---|---|---|
| G2-01 | 0.31 | 1.10 | 0.22 | 0.78 | −0.02 | −0.34 |
| G2-02 | 0.49 | 1.85 | 0.39 | 1.45 | 0.12 | −0.25 |
| G2-03 | −0.02 | −0.07 | −0.20 | −0.75 | −0.40 | −0.79 |
| G2-04 | 0.10 | 0.38 | −0.10 | −0.38 | −0.31 | −0.73 |
| G2-05 | 0.41 | 1.42 | 0.32 | 1.11 | 0.07 | −0.27 |
| G2-06 | 0.64 (close fill: 0.72) | 2.42 (close fill: 2.73) | 0.53 | 2.00 | 0.24 | −0.17 |
| G2-07 | 0.35 | 1.22 | 0.24 | 0.84 | −0.00 | −0.35 |

**No variant passes even at zero cost.** For G2-06 (next-open fill), the red team summed the out-of-sample totals as a share of the book:

| item | share of book |
|---|---|
| gross | +17.4% |
| swap | −7.9% |
| spread | −3.1% |
| net | +6.4% |

## 3. Per year (out of sample, worse fill, net at 1×): return % of the raw book (Sharpe)

| year | G2-01 | G2-02 | G2-03 | G2-04 | G2-05 | **G2-06** | G2-07 |
|---|---|---|---|---|---|---|---|
| 2013 | +3.80 (1.60) | +4.13 (1.85) | +0.59 (0.17) | −1.95 (−0.63) | +3.08 (1.49) | +3.20 (1.62) | +3.14 (1.52) |
| 2014 | −0.07 (−0.02) | −0.45 (−0.16) | −1.92 (−0.50) | −2.21 (−0.67) | +0.17 (0.07) | +0.13 (0.07) | −0.41 (−0.16) |
| 2015 | +1.17 (0.27) | +2.15 (0.56) | −0.73 (−0.16) | +1.95 (0.45) | +0.48 (0.22) | +1.27 (0.69) | −0.10 (−0.04) |
| 2016 | −0.92 (−0.32) | −1.25 (−0.43) | −1.07 (−0.28) | +0.97 (0.25) | −0.88 (−0.56) | +0.32 (0.19) | −0.36 (−0.16) |
| 2017 | +4.66 (2.19) | +2.43 (1.27) | +0.09 (0.03) | −1.39 (−0.58) | +4.38 (2.09) | +2.42 (1.29) | +4.52 (2.15) |
| 2018 | −9.63 (−2.08) | −5.34 (−1.40) | −7.67 (−1.49) | −4.64 (−1.06) | −5.99 (−1.86) | −2.63 (−1.27) | −4.82 (−1.42) |
| 2019 | −0.88 (−0.28) | +2.77 (1.35) | −3.61 (−0.98) | +1.25 (0.42) | −1.99 (−0.71) | +1.19 (0.69) | −2.40 (−0.82) |
| 2020 | −7.36 (−1.15) | −4.44 (−0.81) | −9.68 (−1.43) | −4.78 (−0.81) | −2.89 (−0.90) | −2.61 (−0.91) | −3.90 (−1.10) |
| 2021 | +2.91 (1.05) | +0.95 (0.40) | +1.87 (0.62) | +0.69 (0.23) | +3.30 (1.27) | +1.35 (0.61) | +2.77 (1.06) |
| 2022 | −0.90 (−0.26) | +0.28 (0.09) | +2.41 (0.60) | +3.29 (0.88) | −0.94 (−0.73) | −0.25 (−0.23) | +0.98 (0.48) |
| 2023 | +0.23 (0.10) | +1.01 (0.43) | −2.99 (−1.02) | −2.85 (−0.98) | +0.39 (0.21) | +0.88 (0.47) | −0.41 (−0.20) |
| 2024 | +2.79 (1.12) | +2.89 (1.45) | −0.77 (−0.25) | −1.50 (−0.57) | +2.19 (1.15) | +1.86 (1.06) | +1.21 (0.63) |
| 2025 | +0.48 (0.12) | −0.70 (−0.24) | −0.76 (−0.18) | −4.06 (−1.17) | −0.90 (−0.37) | −0.83 (−0.37) | −1.23 (−0.50) |
| 2026* | +2.81 (1.34) | +0.69 (0.37) | +1.74 (0.69) | −0.51 (−0.20) | +1.81 (1.02) | +0.12 (0.09) | +0.96 (0.50) |

\* 2026 runs to 12 Oct. The raw book runs at only 2–4% volatility, because it is in the market about a fifth of the time; §4 scales it. Years when markets kept falling (2018 and 2020) do the damage, which is the known failure of buy-the-dip.

## 4. The FTMO slot

**Scaled book.** The scale factor is fixed on the in-sample close-fill volatility, then applied out of sample.

| id | 15% target: realised volatility | 15%: days < −5% | 15%: worst day | 15%: max drawdown | 20% target: realised volatility | 20%: days < −5% | 20%: worst day | 20%: max drawdown |
|---|---|---|---|---|---|---|---|---|
| G2-01 | 18.2% | 24 | −21.4% | −72% | 24.3% | 37 | −28.5% | −83% |
| G2-02 | 17.3% | 20 | −17.3% | −55% | 23.1% | 30 | −23.1% | −67% |
| G2-03 | 17.8% | 19 | −18.4% | −80% | 23.8% | 29 | −24.5% | −90% |
| G2-04 | 17.4% | 16 | −14.5% | −65% | 23.2% | 25 | −19.4% | −78% |
| G2-05 | 19.6% | 29 | −16.6% | −71% | 26.1% | 43 | −22.2% | −82% |
| **G2-06** | 17.7% | **19** | −13.9% | −52% | 23.7% | **35** | −18.6% | −63% |
| G2-07 | 18.8% | 21 | −14.9% | −66% | 25.1% | 36 | −19.9% | −77% |

- **Why the tails are so heavy:** the book is flat most days, then holds up to 10 correlated longs at once just as volatility jumps.
- **How a scaled book ends:** a single −14% day ends an FTMO account (5% daily limit, 10% static maximum loss). These books would be breached in the first crash.
- **The F2 model understates this.** It assumes symmetric t3 shocks at constant exposure. This book's left tail is concentrated, so the true $/slot is *lower* than the model's.

**Yearly $ per $100K FTMO Swing slot (F2-09 stress settings, pre-tax, n = 3000)**, at each variant's decisive out-of-sample Sharpe. Source: `prop.txt`.

| id | S (OOS net Sharpe) | 15% cap | 20% cap |
|---|---|---|---|
| G2-01 | −0.02 | $1.6k | $2.7k |
| G2-02 | +0.12 | $2.3k | $3.7k |
| G2-03 | −0.40 | $0.3k | $0.7k |
| G2-04 | −0.31 | $0.5k | $1.1k |
| G2-05 | +0.07 | $2.1k | $3.3k |
| **G2-06** | **+0.24** | **$3.0k** | **$4.8k** |
| G2-07 | −0.00 | $1.7k | $2.9k |
| G2-06, close fill (better fill) | +0.33 | $3.7k | $5.6k |

Most of these dollars come from the lottery part of the prop structure (S = 0 pays $1.7k–$2.9k), not from the edge. They also ignore this book's crash-day tail (above), so they are an upper bound.

At S = 0 the model gives $1.7k at a 15% cap and $2.9k at 20%, the same as the wave-3 table. The target is $20k, and no variant comes near it.

## 5. Verification

- **Verifier.** A separate agent wrote `verifier/verify.py` from `G2_rules.md` alone, without reading the engine.
  - All 14 variant-and-fill rows agree: t within 0.01, Sharpe within 0.004, alpha t within 0.035, p5 within 0.006 bp, in-sample Sharpe within 0.008.
  - Its headline is also G2-06, and its gate is FAIL for all 7.
  - It listed 13 ambiguities with its choice for each. None changes the verdict.
  - Trades per year differ by a constant 3%: it divides by calendar years, I divide by days/252.
- **Red team.** It tried to refute the *negative* verdict (`redteam/redteam.md`):
  1. **Code review of signals, fills, swap, costs, benchmark, Newey-West and bootstrap:** no bug. The swap matches FTMO's points.
  2. **Swap:** it is harsh in the zero-rate years, but it is not what kills the result. With no swap the best t is 2.32; at zero cost it is 2.73.
  3. **US-only book (US500/US100/US30), chosen with hindsight, information only:** the best out-of-sample t is 2.79 at zero cost, and 1.89 for G2-06 at 1×.
     - In sample, the same US-only rules at zero cost did clear the bar (t 3.70–4.09). The edge decayed after 2012; pooling did not hide it.
     - Re-sizing every day instead of fixing the notional at entry changes nothing (t 2.73 → 2.77).
  4. **Look-ahead:** none found. The close fill is slightly flattering, which is why the worse fill decides.

## 6. Gate verdict

**FAIL for all 7 variants:**

- t is below 3.5914 for every variant;
- bootstrap p5 is below 0 for every variant;
- alpha t is negative for every variant;
- the look-ahead tests pass.

Daily buy-the-dip on index CFDs is beta with a weak, decaying overlay. On FTMO it pays a long swap of 6.5–8.3% a year. Its crash-day tail is also incompatible with the 5% daily-loss rule at the 15–20% volatility the target needs.

## 7. Notes for the director

- **The only part still alive is the US large-cap indices.** Their per-trade gross since 2013 is +0.25% to +0.6%, with t about 1.4–3.8 per market. That is information found after the test, and it is not counted.
  - Even a US-only book at zero cost reaches only t 2.79.
  - Re-testing it would need fresh data, such as out-of-sample years after 2026. Re-fitting it on 2013–2026 would be a fresh fit, not a test.
- **FTMO's index swap is a long-only tax of about 8%/yr.** For a book that is long about 10–16% of the time, that is about 0.5–0.8% a year at raw scale, and it grows with leverage. Any long-biased index strategy on FTMO Swing faces it.
- **Budget used:** 7 of 15 variants. The ledger's N rises by 7.
