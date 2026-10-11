# W2 · E1: stock breadth on FTMO stock CFDs (Swing)

**Verdict: FAIL. None of the 11 pre-registered variants passes the gate, and none comes close.**
- **Headline:** E1-04, a weekly 5-day-reversal long book hedged with a short US500 CFD. It lost 9.8% a year out of sample (2015–2026) after FTMO costs.
  - Out-of-sample t is −3.52 against a bar of +3.5603, and bootstrap p5 is below zero.
  - The verifier (independent code) and the red team both confirm.
- **Every variant is negative after costs** on both universes:
  - universe A is point-in-time S&P 500 members;
  - universe B is FTMO's tradable US names.
- **Even with zero costs, no variant passes.** The best out-of-sample t is 2.66, for E1-09 on universe B: an overnight-only book that trades its whole size twice a day.
- **Why it cannot work on FTMO:**
  - Stocks are capped at **1:1 leverage on Swing**.
  - **FTMO charges swap on both sides**: about 8.4% a year on longs and 6.6% a year on shorts.
  - A market-neutral book therefore pays about 7.5% a year before it earns anything, and can never be levered.
  - **No FTMO pass rate or payout is reported, because the gate failed.**

Written 2026-10-12 by the E1 head (wave 2). Pre-registration: `agents/prereg/E1_rules.md` and
`agents/prereg/E1.csv`, committed and pushed in **b09d049 (2026-10-11 23:01:21Z)**, before any
backtest code existed. Code and output are in `agents/daily/w2-stocks/`:

| file | what it is |
|---|---|
| `fetch.py`, `data.py` | data download and point-in-time panels |
| `coverage.txt` | survivorship coverage by year |
| `stocks.py` | engine: all variants, costs, statistics and look-ahead tests |
| `run.txt`, `results.csv` | full results |
| `lookahead_run.py`, `lookahead_part*.txt` | truncation and perturbation tests |
| `test_stocks.py` | unit tests; 4 pass |
| `ftmo_findings.md`, `ftmo_stocks.csv`, `ftmo_swaps_implied.csv` | FTMO conditions with quotes |
| `verifier/` | independent re-implementation and its output |
| `redteam/` | red-team report and checks |

Nothing was bought, signed up for or contacted.

---

## 1. FTMO stock CFDs: what FTMO's own pages say (fetched 2026-10-11)

The source is FTMO's symbol table at https://ftmo.com/en/symbols/, which reads its data from `https://ftmo.com/wp-json/ftmo/symbols`, plus the FTMO FAQ pages. Full quotes are in `agents/daily/w2-stocks/ftmo_findings.md`. No host was blocked.

| Item | Value |
|---|---|
| Stock CFDs | **59 in total: 46 priced in USD, 13 in EUR.** <br>US: AAPL AMD AMZN ARM ASML AVGO AZN BA BABA BAC BRK.B CSCO CVX DIS FDX GE GM GME GOOG IBM INTC JNJ JPM KO LMT MCD META MSFT MSTR NFLX NKE NVDA PFE PLTR QCOM RACE RTX SBUX SNOW SPCX T TSLA V WMT XOM ZM.<br>EU: ADSGn AIRF ALVG BAYGn BMW DBKGn IBE LVMH MBG SAN SIEGn TTE VOWG_p. |
| Commission | `"commission":0.004,"commissionType":"percent"`, i.e. 0.004% of value, charged on each side ⚠ (inferred from the `usdCommission` field) |
| Spread | Not published. FTMO says only "We do not add hidden markups or additional slippage". |
| Leverage on stocks | **Standard 1:3.33 (30% margin); Swing 1:1** (`"leverageSwing":1`) |
| Swap | In points, **negative on both sides for every stock**. Example: AAPL long −7.72, short −6.10. With MT5 "points" semantics (FTMO: a swap "is stated in points per lot"; 1 lot = 1 share; 2 digits), that is $0.0772 per share per night. Across the 46 US names this is **long −8.40%/yr and short −6.64%/yr of notional** (range 7.8–8.7 and 6.2–6.9). US500 CFD: long −8.37%/yr, short +0.42%/yr. Dividends are "folded into" swaps. |
| US hours | 13:35–20:00 UTC, i.e. **09:35–16:00 New York**. No pre- or post-market; the first 5 minutes after the open are missing. |
| Shorting | Allowed, except during a lock-up (SPCX) |
| EAs | Allowed on every instrument ("algorithmic trading, EAs, etc."), on MT4, MT5 and cTrader |
| Swing account | 10% then 5% targets; 5% daily loss; **10% static** maximum loss; at least 4 days per phase; no time limit; 80% split (90% with scaling); first payout from day 14; no restriction on news or weekend holding; $100k fee €540 (whether Swing costs the same is not stated ⚠) |
| Caps | **$400k per trader or strategy.** Servers allow **200 orders at a time and 2,000 positions a day.** |

**What this means.** Only about 37 of the 46 US names were ever S&P 500 members; BABA, RACE, ZM, MSTR, ARM, SNOW, ASML, AZN and SPCX never were. Out of sample, about 33 tradable names are eligible on an average day. That is breadth of about 30, not hundreds.

## 2. Universe and the survivorship bias that remains

- **Membership:** point-in-time S&P 500 from fja05680/sp500 (1996→2026), with prices from the Yahoo daily chart API.
- **Missing prices:** 432 of the 1,214 tickers that were ever members have **no Yahoo history**: delisted, acquired or renamed.
- **Ticker reuse:** a member interval is used only if Yahoo's history starts within 5 trading days of the interval start. This drops symbols later reused by another company.
- **Coverage of the actual index** (`coverage.txt`):
  - 45% in 1999;
  - 58% in 2007;
  - **74% in 2015**;
  - 87% in 2020;
  - 98% in 2026.
- **Remaining bias:** in sample is badly biased, and out of sample is moderately biased. The missing names are mostly failures and takeover targets. For a reversal book, that bias favours the strategy: its losers that would have kept falling are missing. So the true results are probably *worse* than shown.
- **Universe B is more biased still**, because FTMO chose its 2026 list from today's winners (NVDA, AVGO, PLTR and others).
- **Renamed tickers** (FB→META, for example) count only from the rename on.

## 3. What was tested (11 counted variants; full spec in `E1_rules.md`)

All books are dollar-neutral rank-weighted long/short at gross 1× equity, or beta-hedged with the US500 CFD where noted. Signals use closes up to t. The worse of lag 0 (trade at the close) and lag 1 decides.

| id | idea |
|---|---|
| E1-01 / 02 | 5-day reversal, rebalanced daily / weekly |
| E1-03 | residual (beta-adjusted) 5-day reversal, weekly |
| E1-04 | long-only 5-day losers, weekly, beta-hedged with a short US500 CFD |
| E1-05 | PEAD on EPS surprise sign (Nasdaq earnings calendar, 231,682 rows 2008–2026), held 20 days, beta-hedged |
| E1-06 | PEAD on the sign of the 2-day announcement abnormal return |
| E1-07 | gap-on-volume event proxy (volume > 3× median and \|abnormal return\| > 3%), held 20 days |
| E1-08 | Lou–Polk–Skouras "tug of war": rank of 21-day overnight return minus rank of intraday return, weekly |
| E1-09 | overnight-only book (close→open) on 21-day overnight momentum |
| E1-10 | intraday-only book (open→close), short past-overnight winners |
| E1-11 | stack of E1-03 + E1-06 + E1-08 at equal in-sample volatility |

**Split:** in sample 1999-04 (2008-04 for PEAD) to 2014; **out of sample 2015-01-02 to 2026-10-02**, the last day with data, 11.8 years.

**Costs:**
- 0.4 bp commission plus an assumed half-spread of 2 bp on B, 3 bp on A and 0.5 bp on US500;
- an extra 2 bp for the 09:35 open legs of E1-09/10;
- swap per calendar night, using FTMO's current rates in every year (conservative for 2015–21, when policy rates were near zero);
- everything again at 2×.

## 4. Results (out of sample 2015–2026, gross-1 book, worse lag)

| id | U | Sharpe 0 cost | t 0 cost | Sharpe 1× | **t 1×** | t 2× | p5 bp/day | maximum drawdown 1× | worst day | one-way turnover/yr | positions average / maximum | orders/day average / maximum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1-01 | A | 0.48 | 1.51 | −1.23 | **−4.22** | −10.05 | −4.89 | −69% | −3.7% | 71× | 435/498 | 431/498 |
| E1-01 | B | −0.09 | −0.33 | −1.33 | **−4.73** | −9.15 | −6.29 | −78% | −2.8% | 73× | 33/36 | 29/36 |
| E1-02 | A | 0.20 | 0.70 | −1.23 | **−4.41** | −9.57 | −4.52 | −65% | −3.3% | 34× | 435/498 | 90/498 |
| E1-02 | B | −0.22 | −0.77 | −1.29 | **−4.40** | −8.03 | −6.04 | −76% | −3.0% | 34× | 33/36 | 7/36 |
| E1-03 | A | 0.40 | 1.36 | −1.22 | **−4.31** | −10.04 | −4.14 | −60% | −2.4% | 34× | 435/498 | 90/498 |
| E1-03 | B | −0.28 | −0.96 | −1.39 | **−4.85** | −8.76 | −6.08 | −77% | −3.0% | 34× | 33/36 | 7/36 |
| **E1-04** | A | 0.06 | 0.19 | −1.03 | **−3.52** | −7.21 | −5.63 | −71% | −4.7% | 39× | 218/249 | 67/405 |
| E1-04 | B | 0.48 | 1.66 | −0.54 | **−1.91** | −5.56 | −3.76 | −58% | −3.6% | 41× | 16/18 | 5/31 |
| E1-05 | A | 0.15 | 0.52 | −1.80 | **−6.28** | −13.05 | −4.55 | −66% | −1.9% | 32× | 128/404 | 129/406 |
| E1-05 | B | 0.17 | 0.57 | −0.63 | **−2.16** | −4.88 | −5.06 | −63% | −13.8% | 37× | 10/29 | 6/29 |
| E1-06 | A | −0.43 | −1.55 | −3.00 | **−10.93** | −20.21 | −5.29 | −75% | −1.6% | 33× | 137/421 | 139/423 |
| E1-06 | B | 0.18 | 0.59 | −0.81 | **−2.79** | −6.16 | −5.49 | −68% | −6.7% | 40× | 10/30 | 7/30 |
| E1-07 | A | −0.37 | −1.47 | −1.25 | **−4.90** | −8.31 | −8.09 | −85% | −17.0% | 29× | 49/188 | 46/200 |
| E1-07 | B | 0.33 | 1.14 | −0.33 | **−1.19** | −3.57 | −4.73 | −66% | −6.2% | 39× | 4/16 | 2/16 |
| E1-08 | A | 0.03 | 0.11 | −1.80 | **−6.63** | −13.37 | −4.23 | −63% | −3.0% | 16× | 435/498 | 90/498 |
| E1-08 | B | −0.34 | −1.16 | −1.54 | **−5.28** | −9.39 | −5.56 | −73% | −3.4% | 16× | 33/36 | 7/36 |
| E1-09 | A | 0.47 | 1.61 | −8.62 | **−34.04** | −69.84 | −13.66 | −98% | −3.1% | 252× | 435/498 | 871/996 |
| E1-09 | B | 0.78 | 2.66 | −5.13 | **−18.63** | −40.05 | −11.12 | −95% | −2.6% | 252× | 33/36 | 65/72 |
| E1-10 | A | 0.49 | 1.67 | −5.42 | **−20.69** | −43.24 | −10.69 | −95% | −2.4% | 252× | 435/498 | 871/996 |
| E1-10 | B | 0.56 | 1.91 | −3.03 | **−11.31** | −24.70 | −8.53 | −89% | −2.1% | 252× | 33/36 | 65/72 |
| E1-11 | A | 0.14 | 0.49 | −2.32 | **−8.10** | −16.70 | −4.45 | −67% | −2.7% | 32× | 436/498 | 377/498 |
| E1-11 | B | −0.30 | −1.04 | −1.64 | **−5.61** | −10.16 | −6.07 | −76% | −3.3% | 34× | 33/36 | 17/36 |

The bar is t ≥ 3.5603 **and** p5 > 0, on both universes. Over 11.8 years that needs a net out-of-sample Sharpe of about **1.04**. **No row has a positive net Sharpe.**

**Headline (highest in-sample net Sharpe on A, chosen before looking out of sample): E1-04.**
- In-sample net Sharpe: +0.08.
- Out of sample: −9.8% a year, t −3.52, p5 −5.6 bp a day, maximum drawdown −71%, worst day −4.7%.
- At 2×: t −7.21.
- Turnover is 39× a year one-way. It holds about 218 positions on A and 16 on B, with at most 31 orders a day on B.

**Limits.** No variant breaks FTMO's limits of 200 orders at a time or 2,000 positions a day on universe B; at most 72 orders a day. Universe A's books (up to 996 orders a day) cannot be traded at FTMO anyway, because the names are not offered.

**Look-ahead tests:**
- Truncation and perturbation results for every variant and universe are in `lookahead_part1.txt` and `lookahead_part2.txt`. LOOKAHEAD_SUMMARY
- The first run failed E1-02 truncation at 4/20. The cause was the test harness: `weekly()` treated the final row of a truncated series as a week-end. This was fixed in 1367612 by marking it a week-end only if it is a Friday. Full-sample results were unchanged.
- The perturbation test perturbs returns and the market, not volume or eligibility.

## 5. Why it fails (decomposition)

1. **The edges have decayed.** Before costs, in-sample (1999–2014) Sharpes were real:
   - 5-day reversal: 1.36;
   - overnight persistence (E1-09): 3.86.

   Out of sample, before costs, they are only 0.0–0.8. The red team's own quintile and decile rebuilds agree:
   - reversal: in sample 1.30, out of sample 0.53;
   - Lou–Polk–Skouras overnight: in sample 3.22, out of sample 0.47.

   Both effects earned well until about 2011 and almost nothing after. This matches the published post-discovery decay in large caps.
2. **The swap kills what is left.** A gross-1 neutral book pays (8.40 + 6.64)/2 ≈ **7.5%/yr** in swap, about 3 bp a day. That is larger than every variant's gross out-of-sample return. With the swap removed entirely and spread and commission kept, the best out-of-sample t is 1.40 at lag 0 and 1.04 at the worse lag (red team, `redteam/rt_checks.txt`).
3. **No leverage.** At Swing 1:1, the most a gross-1 book can make is its gross return: about 1.5–5% a year out of sample for the best rows before costs. Itamar's target is 20% a year net on a $100k account. After the 80% split that needs about **25% a year** on the account, which at the book's 7–9% volatility means a net Sharpe of about 3. That is roughly 10× better than anything measured here, before costs.
4. **Breadth is small.** FTMO offers about 33 eligible US stocks on an average day, not hundreds. The B books have the same gross signal as A, with more noise.

## 6. Verification

- **Verifier.** A separate agent wrote `verifier/verify.py` from `E1_rules.md` alone, without reading `stocks.py`.
  - All 22 variant×universe rows came out negative, at both 1× and 2×.
  - The out-of-sample t-values agree to 2 decimals on most rows, e.g. E1-05 A −6.28/−6.28, E1-06 A −10.93/−10.93, E1-04 A −3.52/−3.50.
  - Its coverage rule matched `data.py` on 100% of cells.
  - Its turnover column is reported as two-way (Σ|Δw|×252), so it is twice this table's.
  - It listed 12 ambiguities in the rules, with its choice for each (`verifier/verify_run.txt`). None changes the verdict.
- **Red team.** It tried to refute the *negative* verdict (`redteam/redteam.md`):
  - It found no bug in lag, sign, cost, swap, overnight/intraday split, hedge or event timing.
  - It confirmed the swap reading from FTMO's own text and JSON (EURUSD and US500 give sensible rates under the same reading).
  - It showed that no swap, cost or lag change can rescue any variant, because the best zero-cost t is 2.66.

## 7. Gate verdict and prop economics

**FAIL on every count:**
- t is below 3.5603 for all 11 variants on both universes;
- p5 is below 0 for every one;
- the look-ahead tests pass.

Per the brief, no FTMO pass-rate or payout simulation is reported for a failed strategy. The arithmetic in §5.3 shows the target is out of reach at 1:1 leverage anyway.

## 8. Notes for the director

- **FTMO stock CFDs are the wrong vehicle** for stock-breadth market-neutral strategies. The reasons are structural, not about the signals:
  - 1:1 leverage on Swing;
  - swap charged on both long and short positions;
  - about 33 eligible names.

  The Standard account has 1:3.33 leverage, but it has the same two-sided swap and 3.3× the swap drag per unit of equity.
- **The same anomalies elsewhere** (IBKR or real futures) would face a lower borrow and financing cost. But their decayed gross out-of-sample Sharpe of 0.5 or less still would not clear the wave bar.
- **Budget used:** 11 of 15 variants. The ledger's N rises by 11.
