# F1 verifier: independent re-implementation

I rebuilt F1-01, F1-02 and F1-03 using only the written rules: `prereg/F1.csv` (F1-00..03), `prereg/D3.csv` (D3-00/01/11), `ledger.csv` H0022, `references/vwap30-H0022.md`, `references/w1-crypto.md`, plus `w1-crypto/download.py` (file format) and `vwap30-H0022/loaders.py` (roll-week rule). I did not read any other `w3-ensemble/` files, `d3lib.py`, `run.py` or `vwap30.py`.

- Code: `s2_nq.py` (S2 sessions), then `stack.py` (S1, weights, stack, statistics).
- Output: `run.txt`.
- Data: in the scratchpad only, never committed.

## Calibration: both sleeves reproduce the published numbers

| check | published | verifier |
|---|---|---|
| H0022 NQ 1m ex-roll, 0.375 pt | n 1223, 5.90 units/day, gross +6.483, net +5.043, t +1.68, worst −856.0 bp on 2025-04-07, 2025 −9.40 | n 1223, 5.895, gross +6.483, net +5.043, t +1.685, worst −855.96 bp on 2025-04-07, 2025 −9.40 |
| D3-11 (full U_m, Binance perp costs), OOS 2023-01..2026-09 | +7.324 bp/d, t +2.15/+2.10, p5 +1.729, Sharpe 1.11, maxDD −16.7%, worst −8.9% | +7.317, t +2.153/+2.098, p5 +1.712 (iid) / +1.938 (block), Sharpe 1.112, maxDD −16.8%, worst −8.87% |
| Data check: S2 daily net, 1m vs 5m, 2023-01..2025-11 ex roll | — | n 680, corr 0.980; means +0.15 (1m) vs −0.10 (5m) bp/day |

## Results on window W = 2023-01-01..2026-05-07

The window has 1,223 calendar days. All figures are stack daily net, in bp of equity per day.

| variant | cost | mean bp/d | t iid | t NW10 | t min | p5 iid | p5 block20 | p5 | Sharpe √365 | maxDD | worst day | 2023 | 2024 | 2025 | 2026 (to 05-07) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **F1-01** | 1x | **+1.652** | +0.745 | +0.804 | **+0.745** | −1.987 | −1.538 | **−1.987** | +0.41 | −20.0% | −6.74% (2025-04-07) | +0.86 | +7.90 | −4.26 | +2.94 |
| F1-01 | 2x | −1.387 | −0.624 | −0.681 | −0.681 | −5.037 | −4.526 | −5.037 | −0.34 | −27.2% | −6.80% (2025-04-07) | −3.00 | +4.77 | −6.65 | +0.66 |
| F1-02 | 1x | +1.727 | +0.775 | +0.835 | +0.775 | −1.947 | −1.473 | −1.947 | +0.42 | −16.9% | −6.52% (2025-04-07) | +1.41 | +4.96 | −2.10 | +4.30 |
| F1-02 | 2x | −1.442 | −0.645 | −0.702 | −0.702 | −5.146 | −4.633 | −5.146 | −0.35 | −31.8% | −6.59% | −2.51 | +1.80 | −4.92 | +2.28 |
| F1-03 | 1x | +3.657 | +1.653 | +1.776 | +1.653 | +0.021 | +0.435 | +0.021 | +0.90 | −14.5% | −6.70% (2025-04-07) | +3.47 | +9.71 | −2.54 | +4.57 |
| F1-03 | 2x | +2.817 | +1.271 | +1.369 | +1.271 | −0.829 | −0.392 | −0.829 | +0.69 | −16.6% | −6.72% | +2.43 | +8.79 | −3.17 | +3.93 |

**Gate result for F1-01:** FAIL. The t of +0.745 is far below the 3.5745 bar, and the p5 is below 0. I did not run the truncation test. F1-02 also fails.

### Sleeves and weights

**Sleeve means (per unit of each sleeve, on W):**

| | F1-01 1x | F1-01 2x | F1-02 1x | F1-03 1x | F1-03 2x |
|---|---|---|---|---|---|
| r1 (S1) | +2.19 bp/d (Sharpe 0.33) | −2.42 | +2.86 (Sharpe 0.45) | +5.63 (Sharpe 0.86) | +4.92 |
| r2 per session (784 sessions) | +0.16 bp/session | −2.22 | +0.16 | +1.35 | +0.16 |

**Each sleeve alone, F1-01 1x:**

| | n | mean | t min | p5 | Sharpe | maxDD | worst day |
|---|---|---|---|---|---|---|---|
| S1 | 1223 days | +2.19 | +0.58 | −3.70 | 0.33 | −25.3% | −8.55% (2025-06-23) |
| S2 | 784 sessions | +0.16 | +0.05 | — | 0.03 (√365) | −28.0% | −8.59% (2025-04-07) |

**Correlations (daily, W, calendar index; S2 = 0 on non-sessions; F1-01 1x):**

| | r1 | r2 | BTC | NQ |
|---|---|---|---|---|
| r1 | 1 | +0.001 | −0.120 | −0.077 |
| r2 | | 1 | −0.021 | +0.050 |
| BTC | | | 1 | +0.308 |

- r1–r2 on session days only: +0.002.
- F1-02: r1–r2 is −0.008.

**Weights (before the margin cap):**

| | F1-01 range (mean) | F1-02 mean | cap ever hit? |
|---|---|---|---|
| k1 | 0.343..0.533 (0.422) | 0.438 | no (cap 3) |
| k2 | 0.427..0.990 (0.711) | 0.711 | no (cap 5) |

- The monthly k1, k2, sigma1 and sigma2 values are listed in `run.txt` under `k_monthly_F1-01`.
- k2 drops to about 0.43 from 2025-05 to 2025-10 because the April-2025 sessions are inside its 120-session window.

**Margin-cap days: 0 for all variants.** The largest value of k1·Σ|W1| + k2·|pos2|/15 was 0.559 for F1-01/F1-03 and 0.927 for F1-02.

S1 book (F1-01), averaged over W:
- gross notional Σ|W1|: 0.418;
- turnover: 0.102 per day;
- FTMO-restricted universe: 13 to 18 coins per month.

## Ambiguities in the rules and how I resolved them

1. **Candidate count.** D3-00 and F1-00 say "57 candidates", but the list itself has 55 names. Accordingly, 55 × 3 = 165 files exist and none are missing. I used the 55 names.
2. **Daily close.** I used the last 1h bar of the UTC day, which is the 23:00 bar when it exists. Daily quote volume is the sum of the 1h quote volume.
3. **Order of the universe filter.** I took the top 25 of U_m first, then intersected with the FTMO list, as the text reads. N_t counts only the FTMO coins with a valid signal (a non-NaN r20/r60/r120 and sigma60) that also have a bar on the held day.
   - A coin with no bar on day t+1 is closed at its last close, and the close is charged as turnover.
   - Signals use calendar-day lags on a full daily index.
4. **F1-02 universe.** BTC and ETH are used without the U_m filter. They are in U_m every month anyway.
5. **D3-11 multiplier.** I used the std of the last 60 days of the restricted book's own D3-01 gross daily return (ddof 1) × √365, measured through day t and applied to the weights held on t+1. It requires 60 observations.
6. **Turnover and drift.** Turnover is Σ|W_{t+1} − W_t,drifted|, with W_drifted = W_t(1+r_i)/(1+Σ W r).
7. **FTMO swap.** It is charged as 0.30/365 × Σ|W| of the weights held that day, on the S1 book before k (k then scales it). At 2x it is 0.60/365. The commission is 0.00115 per unit traded (0.0023 at 2x).
8. **Which series sets k.** sigma_i uses the variant's own NET series at 1x FTMO cost (F1-02 uses its own S1). The S2 sigma uses the last 120 non-roll sessions, including sessions before 2023 (2022 data). No-position sessions count as 0. Std uses ddof 1.
   - The same k is then used at 2x cost, so positions are identical across cost levels.
   - Sensitivity: recomputing k from the 2x series changes the 2x mean by less than 0.01 bp (F1-01 −1.389 vs −1.387; t NW −0.685 vs −0.681).
   - F1-03 uses F1-01's k and margin scaling, as written.
9. **Margin terms.** |pos2| on a session is 1 if S2 held any position that day, else 0. Roll days and non-sessions are 0. The S1 term uses Σ|W1| of the S1 book held that day. The cap never binds, so this choice does not matter here.
10. **F1-03 funding and cost at 2x.**
    - Funding: the actual prints summed per UTC day of the print timestamp. The 00:00 print counts toward the day that starts at 00:00, so it is charged on the weights held that day. Before a symbol's first funding print, 0.0003 per day is used.
    - Cost x2 doubles only the 7 bp per side and the 0.375 pt; funding stays at the actual prints. D3-00's "double all" could also be read as doubling funding. I did not do that.
11. **5m splice.** Bars are converted from UTC to America/New_York bar-open time. The RTH session on 5m is 09:30 to 15:55 bar-open. A decision is made on the last 5m bar of each 30-minute slot (normally :25/:55), filled at the next bar's open, and the position goes flat at the last bar's close.
    - 1m covers sessions through 2025-11-21 and 5m covers 2025-11-24..2026-05-07: 114 sessions, 10 of them roll days.
    - A half day's last-bar decision is not acted on.
12. **Calendar join.** S2 is booked on its ET session date and S1 on its UTC day; they are joined by calendar date. Roll days and non-sessions give S2 = 0.
13. **S2 unit.** The S2 return is the day's points P&L minus cost × units, divided by the day's first entry price, following H0022. A flip counts as 2 units.
14. **Statistics.**
    - t iid uses std ddof 1. NW uses Bartlett weights with lag 10 and the 1/n variance.
    - Bootstrap: 10k iid means and 10k circular block-20 means. Each uses its own `np.random.default_rng(0)`, the 5th percentile, and the minimum of the two.
    - Sharpe = mean/sd × √365. maxDD is taken on compounded equity.
    - Per-year figures are means; 2026 runs only to 05-07.
15. **NQ buy-and-hold (context).** It is RTH last-bar close to close on consecutive sessions, including roll days, and 0 on non-sessions. BTC is the daily close-to-close of the 23:00 bar.
16. **Not done.**
    - The truncation test (gate item 4). It is not needed for the verdict, because F1-01 already fails on t and p5.
    - The prop_model $-economics (I am not allowed to read that code).
