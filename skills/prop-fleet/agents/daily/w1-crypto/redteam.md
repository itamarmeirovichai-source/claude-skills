# D3 Crypto: red-team report (wave 2026-10-11)

**Verdict: the head's conclusion stands.** No variant passes the gate, and none comes close after correcting for the bugs found. I found no look-ahead. I found two real bugs, both in the funding/perp plumbing. Both make D3-07, D3-08 and D3-10 look slightly *worse* than they are. Fixing both lifts D3-10 from 6.06 to 6.93 bp/day (decisive t 1.96 to 2.22), against a bar of 3.55. The best TSMOM results (D3-02, D3-11) are unaffected. They are unstable from year to year, depend on about 20 days, and D3-02 is largely crypto beta. At a size that makes 20% a year, they breach typical prop drawdown rules.

All numbers below come from scripts in `/tmp/claude-0/-home-user-claude-skills/8eca21fd-129a-52ba-a3be-cd685444e0e4/scratchpad/redteam/` (run with `python3 -I <script> <that dir>`). Those scripts import the unmodified `d3lib.py` / `run.py` and patch copies in memory only. d3lib.py and run.py were not edited. "t" means the decisive t = min(iid, Newey-West lag 10) unless stated.

---

## A. Implementation findings (severity-ranked)

### 1. MEDIUM (bug, hides edge): stale perp klines and stale funding after a perp is delisted are treated as real data
data.binance.vision keeps publishing UM files after a contract is delisted. It writes **zero-volume daily klines at a frozen price** and **funding prints fixed at exactly 0.0001**. `load()` accepts them as valid (`stale.py`):

| coin | dead perp days (volume = 0) | last traded | stale funding prints after |
|---|---|---|---|
| FTM | 2025-01-07..2026-09-30 (price frozen at 0.7702) | 2025-01-06 | 491 × 0.0001 |
| MATIC | 2024-09-05..09-11; funding file runs on to 2026-09-30 | 2024-09-04 | 2268 × 0.0001 |
| FTT | 2022-11-15..2026-09-30 | 2022-11-14 | 2843 × 0.0001 |
| WAVES | 2024-06-12..2026-09-30 | 2024-06-11 | 1118 × 0.0001 |
| EOS | perp file ends 2025-05-21, but the funding file runs to 2026-09-30 | | 1491 × 0.0001 |
| TON | 2026-06-24..2026-09-30 | 2026-06-23 | 0 |
| ICP | 2022-06-11..2022-08-31 (trading paused) | | real prints |

Effect: `pclose.notna()` stays True and `pret = 0`. So in D3-08 the spot leg looks "hedged" by a dead perp. On FTM, 2025-01-07: spot -11.7%, perp 0%, -234 bp on that coin (`diag6.py`). Before the fix, FTM and MATIC alone produce **all** of D3-08's negative OOS gross (-0.24 bp/day; basis P&L FTM -0.241, MATIC -0.053; `diag5.py`). D3-07 can also hold dead FTT, MATIC or FTM perps at a 0 return.

Proposed patch (in `load()`, after reading the perp file):
```python
p = pd.read_parquet(...).loc[START:END]; p = p[~p.index.duplicated()].reindex(days)
dead = (p.volume == 0)
dead[p[p.volume > 0].index.max() + pd.Timedelta(days=1):] = True   # after the last traded day
pc[c] = p.close.mask(dead); pr[c] = pc[c].pct_change(fill_method=None)
# and mask funding prints on dead days: fs = fs.mask(dead); fcount = fcount.mask(dead)
# (a position still held on a dead-perp day keeps the F_DEFAULT charge)
```
Measured effect (`fix_stale.py`, OOS mean bp/day, decisive t):

| | before | after |
|---|---|---|
| D3-08 | -0.20 (t -0.84) | -0.11 (t -0.52) |
| D3-07 | 2.19 (t 0.70) | 2.26 (t 0.72) |
| D3-10 | 6.06 (t 1.96) | 6.14 (t 1.99) |

Every other variant changes by 0.01 or less. The remaining D3-08 loss comes from the one unhedged day on each delisting (FTM, MATIC). A live system would avoid it by reading Binance's delisting announcements (about 1 week ahead). That cannot be backtested ex-ante with this data.

### 2. MEDIUM-LOW (spec deviation, hides edge): funding signals use the mean *per print*, not per 8h
The prereg says D3-08 needs "mean funding > 0.0001 **per 8h**", and D3-07 ranks by mean funding. The code (`g_carry`, `g_cashcarry`) uses `sum/number_of_prints`. Since 2023 Binance moves coins with extreme funding to 4h (and sometimes 1h) intervals. That is 3,254 coin-days with 6 prints OOS (AXS, POL, TON, WIF, XTZ; `diag4.py`). For those coins the per-print rate is half the 8h rate. D3-07 therefore treats the most crowded longs as "low funding" and may go long them. Patch: `fmean = fund.rolling(7).sum() / 21` (D3-07) and `m = fund.rolling(3).sum() / 9` (D3-08), i.e. the 8h-equivalent rate.
Effect (`diag5.py`, `combo_fix.py`):

| | before | after |
|---|---|---|
| D3-07 OOS | 2.19 (t 0.70) | 3.73 (t 1.20) |
| D3-08 OOS | -0.20 | -0.19 |
| D3-10 OOS | 6.06 (t 1.96) | 6.84 (t 2.19) |

**Bugs 1+2 together:** D3-07 4.06 (t 1.29), D3-08 -0.10 (t -0.49), **D3-10 6.93 (t 2.22, p5 +1.93, cost x2 5.59)**. Still about 1.6× short of the 3.55 bar.

### 3. MEDIUM (survivorship / hindsight in the candidate list; diagnostic only, not a scored variant)
The 55 candidates were fixed in 2026. They include coins that became famous after 2022 (PEPE, WIF, SUI, TON, INJ, APT, ARB, OP). They omit about 40 coins that were top-25 by USDT volume during OOS. I downloaded 72 extra USDT symbols (spot 1h and funding, 2021-07..2026-09, `dlx.py`, data in `scratchpad/xdata/`). With the same rules, the omitted coins take **22.6% of OOS universe slots**: WLD 790 days, FET 701, ENA 638, RUNE 546, TAO 545, BONK 393, RNDR 337, FLOKI 306, TRUMP 275, PENGU 273, and others (`diag3.py`). Results with the expanded list:

| | registered | expanded list |
|---|---|---|
| D3-01 | 4.70 (t 1.33) | 4.08 (t 1.24) |
| D3-02 | 5.61 (t 2.03) | 5.25 (t 2.00) |
| D3-11 | 7.32 (t 2.10) | 6.98 (t 2.03) |
| D3-05 | 0.61 (t 0.15) | 4.21 (t 1.00) |

The hindsight coins contribute 0.92 of D3-02's 5.93 bp/day gross-minus-funding (`diag2.py`). The verdict does not change. IS is worse: in 2019 only about 15 candidates were eligible (BCHABC, ONT, QTUM, ZIL, BAT and others are missing), so the IS universe is small and survivor-tilted.

### 4. MEDIUM (IS realism): IS "perp" backtests mostly predate the perps
The share of TSMOM/XSMOM gross weight on coin-days with **no listed UM perp** is **100% in 2019**, 15–24% in 2020, about 1–2% in 2021–22, and 0.1% OOS. 2019 IS is therefore a spot backtest with assumed funding (shorts would even *receive* the 0.0003/day default), and shorts were not implementable. IS columns and the IS-fixed 20%-vol scale factor carry this caveat. OOS is clean.

### 5. LOW (reporting): the head quotes the iid t, but the gate uses min(iid, NW)
Decisive t: D3-02 **2.03** (iid 2.26), D3-11 **2.10** (iid 2.15), D3-10 **1.96** (NW 2.20).

### 6. LOW: smaller issues, all measured as negligible
- **00:00 UTC funding print.** Trades execute after the 23:00-bar close, so the 00:00 print belongs to the *old* position. The code charges the new one (this follows the prereg wording). Moving it changes D3-08 by -0.01 and D3-02 by +0.01 bp/day.
- **Spot vs perp returns.** TSMOM perp positions are marked on spot returns. Using perp returns: D3-02 5.61→5.58, D3-01 4.70→4.64.
- **LUNA 2.0** (124 OOS universe days). LUNA2USDT was not downloaded, so LUNA 2.0 is held with no perp and zero funding (`fdaily` fillna(0) after the old LUNA perp's first print). The old-LUNA/LUNA-2.0 split works: there is an 18-day hourly gap > GAP_H, returns are NaN across it, and age resets. 0.05% of weight.
- **FTT second segment** (2023-09 on) has a dead perp with stale funding; see #1. **MATIC→POL:** POL is ineligible for 180 days (to about 2025-03), so the momentum history breaks. Negligible.
- **D3-10 / D3-08 netting and drift.** D3-10's carry leg is costed separately from the TSMOM+XSMOM leg, so the same coin is not netted. This is slightly conservative relative to the prereg's "netting allowed". In D3-08, each leg's drift uses its own leg's gross in the denominator. Both negligible.
- **Truncation test blind spot.** It checks decision matrices only. The loader and `evaluate()` (the shift(1) holding map) are outside it. I reviewed both by hand (see B).

## B. Checked and found correct
- **Loader.** No duplicate or off-grid timestamps in any spot file. The 2025+ microsecond timestamps are converted correctly. The only missing months are FTT 2022-12..2023-08, which is a real halt (`dq.py`).
- **Timing.** Decisions use data through the 23:00 bar close of t and are held on t+1. The universe is ranked from data before the 1st of the month, and `holding_universe` handles month ends. Adding 1 or 2 more days of lag decays the results smoothly (D3-02 gross 6.48→6.11→6.24, D3-01 5.91→4.60→3.88), and 1 or 2 hours for D3-04 gives 6.74→5.93→5.80. That is no look-ahead signature (`lag.py`).
- **Hourly mapping.** D3-09 IS gross 17.84 bp/day equals the IS hour means of the chosen hours (long 13,21; short 23,2: 4.79+6.09+3.68+3.37 = 17.9), so decision hour h is held over the bar opening at h+1 correctly.
- **Funding sign.** A long pays positive funding (D3-02 fund +0.55 bp/day paid; D3-07 -2.41 received).
- **Turnover, drift and cost.** Turnover is held weight minus the drifted prior weight, charged per side.
- **Statistics.** The NW Bartlett weights are correct. The bootstrap p5 moves by ±0.05 bp across seeds.
- **Truncation test.** The head's rerun finished: all 11 variants PASS on 54 cuts. D3-09 is skipped for IS cuts by design, so D3-09's IS numbers are in-sample.

## C. Attack on the best results (OOS 2023-01-01..2026-09-30, n = 1369)

### Year by year, net bp/day (`diag1.py`)

| | 2023 | 2024 | 2025 | 2026 (to Sep) | all, cost x1 | all, cost x2 |
|---|---|---|---|---|---|---|
| D3-02 | 8.17 (t 1.55) | 9.77 (1.72) | **-0.98** (-0.23) | 5.43 (1.37) | 5.61, t 2.03 | 5.29, t 1.92 |
| D3-11 | 5.83 (0.86) | 12.87 (1.91) | 1.71 (0.27) | 9.40 (1.27) | 7.32, t 2.10 | 6.61, t 1.90 |
| D3-10 | 8.18 (1.24) | 5.97 (1.10) | 5.10 (0.81) | 4.63 (0.74) | 6.06, t 1.96 | 4.72, t 1.53 |

No single year is significant. D3-02 lost money in 2025.

### Concentration
- **By coin: not concentrated.** For D3-02 the largest contributor is TRX at 0.73 of 5.93 bp; removing the top 3 coins leaves 4.30, and BTC+ETH give only 0.61. D3-11 and D3-01 look similar (`diag2.py`).
- **By day: heavy dependence on a few days.**
  - Removing the 10 best days: D3-02 2.66 (t 1.15), D3-11 2.98, D3-10 2.48.
  - Removing the 20 best days: D3-02 0.47, D3-11 -0.13, D3-10 0.00.
  - The top 1% of days (13) produce 65% (D3-02), 73% (D3-11) and 72% (D3-10) of total net.
- **D3-10 components** (standalone, OOS): TSMOM part 3.66 (t 2.10), XSMOM 0.93, carry 1.44. The carry part is almost entirely 2026 (+7.9) and negative in 2023–24 (`d10.py`).

### Beta
D3-02's mean gross exposure is only **0.21** (always net long, max 0.79). Regressions use NW t (`diag1.py`):

| | alpha (bp/day) | alpha t | beta | R² |
|---|---|---|---|---|
| D3-02 on BTC | 2.49 | 1.10 | 0.21 | 0.31 |
| D3-02 on the equal-weight universe | 3.58 | 2.03 | 0.185 | 0.50 |
| D3-11 on BTC | 8.43 | 2.40 | about 0 | 0.02 |
| D3-10 on BTC | 7.46 | 2.72 | about 0 | 0.04 |

- **BTC buy-and-hold over the same window:** 14.78 bp/day, Sharpe **1.16**, maxDD -53%. Scaled to D3-02's volatility it makes **5.58 bp/day** with maxDD -23%, against D3-02's 5.61 and -18%.
- **So D3-02 has BTC's Sharpe and is mostly a timed long-crypto position.** D3-11 and D3-10 are genuinely beta-neutral, but their alpha t is 2.4–2.7, not 3.5.
- D3-02 makes +45.7 bp on BTC-up days and -35.4 on BTC-down days.

### Prop-firm rules (`prop.py`)
Each series is scaled to 20%/yr arithmetic: 0.98× D3-02, 0.75× D3-11, 0.90× D3-10. P(breach) is measured over rolling 1-year windows inside OOS, starting every 7 days. These are overlapping windows from one path, so treat them as rough.

| | OOS maxDD | worst day | days < -4% | P(breach) 5% daily / 10% max, static | same, trailing | P(breach) 3% / 6% |
|---|---|---|---|---|---|---|
| D3-02 | -17.7% | -5.64% | 6 | 41% | 90% | 100% |
| D3-11 | -12.7% | -6.63% | 2 | 37% | 83% | 100% |
| D3-10 | -14.1% | -6.89% | 3 | 56% | 96% | 100% |

- **D3-02 intraday.** Firms measure daily loss on floating equity. Marked hourly, D3-02's worst intraday floating loss is -6.2%, and 20 days go below -3%.
- **Consistency rules** (for example HyroTrader's "max 40% of the target from one day"). The best day reaches 33–77% of a year's profit (D3-11 in 2025: 77%). D3-02 never reached a +10% target in 2025.
- **Conclusion.** At a size that makes 20% a year, every candidate breaches a 6–10% max-drawdown account with high probability. The 3–5% daily limits are hit within a year in most windows. Sizing down to survive a 6% static limit roughly halves the return to about 8–10% a year, still before evaluation fees.

## D. Bottom line for the head
1. Keep "no variant passes". Report the decisive t (2.03 / 2.10 / 1.96), not the iid t.
2. Apply the stale-perp patch (#1) and the per-8h funding patch (#2) before quoting D3-07, D3-08 and D3-10. The corrected D3-10 is 6.93 bp/day, t 2.22, which still fails.
3. Disclose the hindsight in the candidate list. The expanded-list check leaves TSMOM essentially unchanged (D3-02 5.25, t 2.00).
4. Describe D3-02 as "BTC-like Sharpe at 0.2 average net long". It is not a demonstrated alpha.
