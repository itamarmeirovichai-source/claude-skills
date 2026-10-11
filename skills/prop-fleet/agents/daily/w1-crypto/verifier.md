# D3 (Crypto) — independent verification

Verifier re-implemented D3-01, 02, 03, 05, 06, 07, 08, 09 (+ETH) and 11 from `prereg/D3.csv` only, then compared against the head's numbers. The head's `d3lib.py`/`run.py` were read only after the verifier's numbers existed, to explain differences.
Script: `verify/verify_d3.py` (run `python3 -I verify/verify_d3.py <data_dir>`, ~12 s). Numbers: `verify/verify_results.csv`. Head-vs-verifier diff tool: `verify/diag_compare_head.py`.

## Results (net, bp of capital per day; OOS 2023-01-01..2026-09-30, IS 2019-01-01..2022-12-31)

| Variant | OOS mean V / H | OOS t_iid V / H | OOS NW10 t (V) | Sharpe (V) | cost x2 mean (V) | IS mean V / H | IS t V / H |
|---|---|---|---|---|---|---|---|
| D3-01 TSMOM L/S | 4.68 / 4.70 | 1.32 / 1.33 | 1.35 | 0.68 | 3.98 | 6.39 / 6.41 | 1.74 / 1.75 |
| D3-02 TSMOM long/flat | 5.60 / 5.61 | 2.26 / 2.26 | 2.03 | 1.17 | 5.28 | 6.74 / 6.75 | 2.43 / 2.41 |
| D3-03 BTC+ETH TSMOM | 7.21 / – | 1.37 / – | 1.40 | 0.71 | 6.25 | 12.65 / – | 2.39 / – |
| D3-05 XS-mom 28d | 0.31 / 0.61 | 0.08 / 0.15 | 0.08 | 0.04 | -0.60 | 17.56 / 17.56 | 2.97 / 2.97 |
| D3-06 XS-mom 7d | -1.61 / – | -0.40 / – | -0.42 | -0.21 | -3.20 | 12.68 / – | 2.51 / – |
| D3-07 funding carry | 2.20 / 2.19 | 0.70 / 0.70 | 0.70 | 0.36 | 1.20 | 2.43 / 2.02 | 0.64 (NW 0.58) / 0.49 |
| D3-08 cash-and-carry | -0.17 / -0.20 | -0.70 / -0.84 | -0.49 | -0.36 | -1.30 | 2.93 / 2.93 | 9.36 (NW 4.00) / 4.00 |
| D3-09 hour-of-day BTC | -54.34 / -54.33 | -20.85 / -20.84 | -21.93 | -10.77 | -110.34 | -38.16 / – | -8.76 / – |
| D3-09 ETH (same hours) | -53.70 | -15.71 | -16.32 | -8.11 | -109.70 | -35.29 | -6.63 |
| D3-11 vol-managed TSMOM | 7.32 / 7.32 | 2.15 / 2.15 | 2.10 | 1.11 | 6.61 | 7.26 / 7.27 | 2.10 / 2.10 |

D3-09 hours, picked independently on IS BTC by mean 1h log return per UTC bar-open hour: long 21 and 13, short 23 and 2. These are the head's hours. Cost is 8 position changes a day × 7 bp = 56 bp a day, which is why the result is so negative. The pattern is not exploitable.

## Verdict
- **The check passes for every variant.** Signs and conclusions match. All t-stats are within 0.2 of the head's, and all means are within 30% except D3-05 OOS, where both numbers are about zero (0.31 vs 0.61 bp, t 0.08 vs 0.15).
- **No variant passes the gate in either implementation.** The gate needs OOS min(iid, NW) t ≥ 3.5504. The best OOS t is 2.26 (iid) / 2.03 (NW) for D3-02, then 2.15 / 2.10 for D3-11. D3-05's in-sample momentum (t 2.97) vanishes OOS.

## Material discrepancies and causes
1. **The head reports IS t as min(iid, NW).** In `run.py` the IS column prints `t = min(t_iid, t_nw)`. This explains D3-08 IS 4.00: that is the NW t, and the iid t is 9.36 because cash-and-carry P&L is strongly autocorrelated. It also explains D3-07 IS 0.49, which sits below both iid and NW in my run (see 3). The OOS figures the head quoted are iid t as stated. Not an error, but the label is mixed.
2. **D3-05 OOS (0.31 vs 0.61 bp).** This comes from a one-day boundary in the age filter. The spec says ">=180 days of prior data". I admit a coin whose first daily bar is ≤ m0−180, which gives 180 daily bars through the previous month-end. The head requires `age(prev) >= 180`, i.e. first bar ≤ m0−181. As a result PEPE and APE (2023-11) and WIF (2024-09) enter the universe one month earlier in mine, and the rank-25 boundary moves DOGE (2020-01) and FIL (2024-09). These months are the only universe differences once LUNA/FTT segments are merged. They change D3-05 picks on about 51 days, almost all in those months. Gross OOS is 0.84 (mine) vs 1.14 bp (head). Cost and funding are identical to within 0.01 bp. Both readings of the spec are defensible.
3. **D3-07 IS (2.43 vs 2.02).** The 7-day funding window and history test differ slightly. I use the mean of prints timestamped Monday−7d..Sunday and need the first print ≤ Sunday−6d. The head uses rolling 7-day sum/count and needs ≥7 days with prints. The same age-boundary universe effect also applies. OOS is identical.
4. **D3-08 OOS t (-0.70 vs -0.84).** The head approximates "mean of the last 9 prints" by the mean of the last 3 days of prints, which is a documented deviation in `d3lib.g_cashcarry`. It differs for coins on 4h funding. I use exactly the last 9 prints. Leg-drift details also differ: I drift each leg without renormalising. The conclusion is the same: positive in IS, about zero or negative OOS.
5. **Segments.** Both implementations split any >72h hourly gap. The splits are LUNA → new segment from 2022-05-31, and FTT → new segment from 2023-09-22, after a 311-day gap. I restrict funding prints to each segment's life, and the head does not. This has no visible effect.

## Implementation notes (verifier)
- Daily close is the last 1h close of each UTC day. r is spot close-to-close and is NaN across missing days and segments, in which case P&L is 0.
- The universe is ranked at m0 on 30-day spot qvol over days [m0−30, m0−1].
- Weights for t+1 come from data through t and from the universe for month(t+1).
- Drifted-weight turnover: w(1+r)/(1+gross).
- Funding is the actual prints summed per UTC day. Before a symbol's first print it defaults to 3 bp a day.
- D3-07 uses perp-kline returns. D3-08 uses spot−perp with 9.5 + 7 bp per side.
- D3-09 runs on the BTC spot 1h series as a proxy for the perp, with funding on the day's average weight, which is 0.
- I did not re-run the bootstrap p5 or the truncation test. They are moot because no variant clears the t bar.
