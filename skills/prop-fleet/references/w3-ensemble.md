# W3 · F1: ensemble of near-misses on one FTMO Swing account

**Verdict: FAIL.** The pre-registered equal-risk stack (F1-01) makes +1.65 bp a day after FTMO costs, out of sample from 2023-01-01 to 2026-05-07.

| | F1-01 at FTMO cost | bar |
|---|---|---|
| net mean | +1.65 bp/day | |
| t | **0.74** | 3.5745 |
| bootstrap p5 | −1.98 bp | > 0 |
| Sharpe | **0.41** | about 1.95 |
| max drawdown | −20% | |
| at 2× cost | −1.39 bp/day (Sharpe −0.34) | |

The stack has two sleeves: crypto vol-managed TSMOM (D3-11) and US100 30-minute VWAP trend (H0022).

- **The sleeves are uncorrelated** (+0.00), so the combination does diversify. Neither sleeve has enough edge in this window for that to matter.
  - FTMO's **−30%/yr swap on crypto CFDs, long and short alike**, eats half of the crypto sleeve's gross.
  - The US100 sleeve has earned about zero since 2023.
- **Even the most generous diagnostic stays far short.** Zero costs everywhere plus the ex-post best weight gives t 2.20.
- **Not a single FTMO account could run this.** The worst day, −6.7%, breaches FTMO's 5% daily-loss rule, and the drawdown is twice the 10% limit.
- **Money per $100K FTMO slot is far below the $20k target.** At Sharpe 0.41 the D1 model gives about $3.9k a year at a 12% vol cap and $8.0k at 20%. Most of that is the fee-lottery value a zero-edge strategy also earns ($1.9k / $5.0k).
- **Nothing goes to the bot.**

Department F1, wave 3, 12 Oct 2026. Branch `claude/w3-ensemble`.

- **Pre-registration:** `agents/prereg/F1.csv`, pushed in **d2a5938 (2026-10-12 00:21:28Z)** before any sleeve series was rebuilt or combined.
- **Code and output:** `agents/daily/w3-ensemble/`.
- Nothing was bought, signed up for or contacted, and no money moved.

## What was pre-registered (F1-00, fixed before combining)

### Window

- The decisive window W runs from 2023-01-01 to 2026-05-07, 1,223 calendar days. It is the overlap of the two sleeves' own out-of-sample periods:
  - D3's crypto OOS starts 2023-01-01;
  - H0022's NQ data were decisive in full, because its rules came from the paper and were never fitted.
- NQ 1m data run to 2025-11-21. The pinned Databento NQ 5m file, never used before, carries the window on to 2026-05-07.
- On their overlap, the 1m and 5m versions of the US100 sleeve correlate at 0.98.

### Sleeve S1: crypto

- **Rules:** D3-11 exactly, run with D3's own code (`w1-crypto/d3lib.py`):
  - signal: sign of the 20-, 60- and 120-day returns;
  - size: 0.5/σ per coin, divided by N;
  - a 20% vol-managed multiplier on top.
- **Universe:** D3's monthly top-25 universe restricted to the 28 coins FTMO lists as crypto CFDs.
- **Why the D3 universe rather than BTC/ETH:** D3-11 was tested on that universe, and FTMO lists 28 of the D3 candidates, so it can be traded. The BTC/ETH-only version is F1-02.

### Sleeve S2: US100

- **Rules:** H0022 exactly, run with its own code (`vwap30-H0022/vwap30.py`).
- **Instrument:** NQ stands in for FTMO US100.cash.
- **Roll weeks:** excluded, as registered.

### Third sleeve: none qualified

The rule was fixed before any combination: a D2, E1 or E2 sleeve joins only if all three of these hold:
- its own OOS net t is at least 1.5;
- its IS and OOS means have the same sign;
- it can run on FTMO Swing.

None qualified:

| dept | best sleeve | OOS t | why it fails the rule |
|---|---|---|---|
| D2 | D2-02 | 0.54 | t too low (FRED, its data source, is also unreachable from here) |
| E1 | — | all negative | t too low |
| E2 | E2-04 | 1.09 | t too low, and its IS mean has the opposite sign |

### Costs

FTMO's symbol table (`ftmo.com/wp-json/ftmo/symbols`, fetched 2026-10-12) gives these terms:

| | crypto CFDs | US100.cash |
|---|---|---|
| commission | 0.065% per side | 0 |
| swap | **−30%/yr, long and short** (type "percentage") | long −701 points; irrelevant, because the sleeve is flat before the 17:00 NY rollover |
| leverage on Swing | 1:1 | 1:15 |

FTMO publishes no spreads, so two were assumed:
- crypto: a 5 bp half-spread, giving 11.5 bp per side in total;
- US100: 1.5 points round trip, i.e. 0.75 pt per unit, twice H0022's futures cost.

At 2× cost, every cost doubles, including the swap.

### Weights, rebalance and gate

- **Equal risk.** On the first of each month, each sleeve gets k = 10% ÷ its vol over its last 120 observations. The caps are k1 ≤ 3 and k2 ≤ 5.
- **Margin.** A margin rule scales both weights down if crypto notional + US100 notional/15 exceeds equity. It never bound.
- **Rebalance inside the sleeves:** crypto daily at 00:00 UTC; US100 every 30 minutes and flat at 15:59 NY.
- **Gate:**
  - t = min(iid, Newey-West lag 10) ≥ 3.5745;
  - bootstrap p5 = min(iid, block 20) > 0;
  - the truncation test passes.
- **Variants:** 3 counted out of the 5 allowed:
  - F1-01, the headline;
  - F1-02, with the crypto sleeve on BTC/ETH only;
  - F1-03, a diagnostic at non-FTMO costs.

## Results (window W, net)

| id | cost | mean bp/day | t iid / NW | p5 iid / block | Sharpe | vol | maxDD | worst day | gate |
|---|---|---|---|---|---|---|---|---|---|
| **F1-01** | **FTMO 1×** | **+1.65** | **+0.74 / +0.80** | **−1.98 / −1.55** | **+0.41** | 14.8% | **−20.0%** | −6.74% | **FAIL** |
| F1-01 | FTMO 2× | −1.39 | −0.63 / −0.68 | −5.05 / −4.53 | −0.34 | 14.9% | −27.2% | −6.80% | FAIL |
| F1-02 (BTC/ETH) | FTMO 1× | +1.73 | +0.77 / +0.83 | −1.95 / −1.47 | +0.42 | 14.9% | −16.9% | −6.52% | FAIL |
| F1-02 | FTMO 2× | −1.44 | −0.65 / −0.70 | −5.15 / −4.63 | −0.35 | 14.9% | −31.8% | −6.59% | FAIL |
| F1-03 (Binance-perp + futures costs) | venue 1× | +3.65 | +1.65 / +1.77 | +0.01 / +0.43 | +0.90 | 14.8% | −14.5% | −6.70% | FAIL |
| F1-03 | venue 2× | +2.81 | +1.27 / +1.37 | −0.83 / −0.41 | +0.69 | 14.8% | −16.6% | −6.72% | FAIL |

**Units and the bar**
- bp/day is per calendar day of account equity. Sharpe uses √365.
- At 1,223 days, t ≥ 3.5745 needs a net Sharpe of about **1.95**.

**F1-01 by year (bp/day):**

| | 2023 | 2024 | 2025 | 2026 (to May 7) |
|---|---|---|---|---|
| FTMO 1× | +0.80 | +7.94 | −4.26 | +2.94 |
| FTMO 2× | −3.06 | +4.80 | −6.65 | +0.66 |

Without 2024 the stack is negative: −1.04 bp/day (red team).

### The sleeves on their own (F1-01, FTMO 1×)

| sleeve | mean | t | Sharpe | maxDD | by year |
|---|---|---|---|---|---|
| S1 crypto (unit book) | +2.16 bp/day | 0.57 | 0.33 | −25% | 2023 −1.2, 2024 +9.3, 2025 −1.6, 2026 +2.1 |
| S2 US100 (per session, 784 sessions) | +0.16 bp | 0.05 | ≈0 | −28% | 2023 +4.1, 2024 +5.8, 2025 −10.6, 2026 +3.5 |

**Where S1's money goes (bp/day):**

| gross | trading cost | FTMO swap | net |
|---|---|---|---|
| +6.77 | 1.17 | **3.44** | +2.16 |

- The mean gross notional is 0.42× of sleeve capital.
- At D3's Binance-perp costs the same positions net +5.60 (F1-03).

**What S2 earned over time:**
- At zero cost, S2 still makes only +2.54 bp per session in the window (t 0.78), so the weakness is the signal, not the cost.
- H0022 made +9.6 bp/day in 2020–22 and +1.4 bp/day from 2023 to 2025-11 (red team).

**Weights:**
- The mean risk weights are k1 = 0.42 and k2 = 0.71.
- The realised vols of the scaled legs are 10.5% and 10.4%, against 10% targets.
- Margin use peaked at 55% of equity. The cap never bound (0 days).

## Correlation matrix (window W, daily)

On NQ session days:

| | S1 crypto | S2 US100 | stack | BTC | NQ (RTH) |
|---|---|---|---|---|---|
| S1 crypto | 1 | **+0.001** | +0.64 | −0.07 | −0.09 |
| S2 US100 | +0.001 | 1 | +0.76 | −0.02 | +0.00 |
| stack | +0.64 | +0.76 | 1 | −0.06 | −0.08 |
| BTC | −0.07 | −0.02 | −0.06 | 1 | +0.30 |
| NQ (RTH) | −0.09 | +0.00 | −0.08 | +0.30 | 1 |

On all calendar days, with S2 = 0 off-session:
- S1–S2: +0.001;
- S1–BTC: −0.12;
- stack–BTC: −0.10.

The red team checked lags −1 and +1 for a lead-lag effect and found none: −0.018 and −0.038.

**Reading:** the diversification is real. Two uncorrelated sleeves at equal risk combine to Sharpe (s1 + s2)/√2. With the scaled legs' in-window Sharpes of 0.38 and 0.20, that gives the observed 0.41. To reach 1.95 with two uncorrelated sleeves, each would need a Sharpe of about 1.4.

## FTMO $ per $100K slot (D1 model)

The source is `daily/w1-prop/prop_model.py` `economics()`, firm "FTMO Swing 2-Step 100K", n = 1,500. That is the same setup as the `w1-synthesis.md` table, which it reproduces: S = 0 gives $1.9k / $5.0k and S = 1.5 gives $12.1k / $20.6k. Output is in `daily/w3-ensemble/prop_dollars.txt`.

| | Sharpe | vol cap 12% | vol cap 20% |
|---|---|---|---|
| **F1-01, FTMO 1×** | 0.41 | **$3.9k/yr** (pass 50%) | **$8.0k/yr** (pass 43%) |
| F1-01, FTMO 2× | −0.34 (model run at 0) | $1.9k* | $5.0k* |
| F1-02, FTMO 1× | 0.42 | $4.0k | $8.2k |
| F1-02, FTMO 2× | −0.35 (model run at 0) | $1.9k* | $5.0k* |
| *zero edge, for reference* | 0 | $1.9k | $5.0k |

\* The model is not built for negative drift, so negative Sharpes were floored at 0. Those cells are upper bounds.

**How to read it**
- The target is $20k per slot. The stack gets 20–40% of it, and about half of that is the zero-edge fee-lottery value that `w1-synthesis.md` warns against.
- **The model is too kind to this stack.** It assumes t-distributed noise at the chosen vol, but the stack's real tail is worse:
  - The worst day is −6.74% at about 15% vol (2025-04-07, the US100 sleeve's −8.6% times k2 = 0.76). Scaled to 12% vol, that day is still about −5.5%. It breaches FTMO's 5% daily-loss limit and ends the account.
  - The −20% max drawdown at about 15% vol is twice FTMO's 10% maximum loss.
- F2 is testing exactly this fat-tail effect on the dollar figures.

## Checks

- **Truncation and look-ahead test: PASS.** It used 50 random cut dates in W (seed 0). After all data past the cut were deleted, the following were identical on every day up to the cut (`truncation-run.txt`):
  - the S1 weights (F1-01 and F1-02);
  - the S2 daily series;
  - the risk weights k.
- **The sleeves reproduce the departments' originals:**
  - H0022 on NQ 1m: +5.043 bp/day, t 1.68, exactly as published;
  - D3-11 (full universe, D3 costs, 2023-01 to 2026-09): +7.32 bp/day, t 2.15 / 2.10, identical to `w1-crypto/run.py`.
  - Restricting D3-11 to FTMO coins costs 0.4 bp/day over D3's whole OOS period, and 1.0 bp/day inside W.
- **Independent verifier** (`verify/`). It rebuilt everything from the written rules without reading the head's code. Every stack row agrees within 0.04 bp/day and 0.03 in t (F1-01: +1.652, t 0.745). It listed 16 ambiguities it had to resolve (`verify/verify.md`), none of them material:
  - D3's candidate list has 55 names, not 57; this is inherited from D3 and changes nothing;
  - whether F1-03's 2× should double funding prints;
  - the 5m session's last bar sits at 15:55.
- **Red team** (`redteam/findings.md`). It found no error that flatters the stack and nothing that hides an edge. How much each assumption moves the stack t (headline 0.74):

| assumption | stack t |
|---|---|
| swap 0 | 1.40 |
| swap triple-charged, 9 nights a week | 0.54 |
| alt spreads 15–25 bp (probably more realistic than 5 bp) | 0.42–0.59 |
| US100 at 0.25 pt | 1.07 |
| most favourable plausible costs | 1.83 |
| zero cost everywhere | 2.12 |
| ex-post best weight (64/36), at FTMO cost | 0.78 |
| ex-post best weight, at zero cost | 2.20 |
| including the roll weeks | 0.46 |

  - **The answer:** no cost or weighting choice reaches 3.57.
  - **One cosmetic bug:** the standalone S2 Sharpe in `run.txt` uses √365 on a sessions-only series; it should be about 0.03 either way.
- **A pattern the red team saw that is NOT actionable.** The crypto sleeve earned most of its money at weekends: +10.4 bp/day net on weekends against −1.1 on weekdays. This was found after looking at the data, among many possible cuts. It would need its own pre-registration and fresh data.

## What this means for the wave

1. **Stacking near-misses does not create an edge when the near-misses decay out of sample and the venue taxes them.**
   - On their own OOS histories D3-11 had Sharpe 1.1 and H0022 had 0.76.
   - Inside the common window at FTMO terms they fall to about 0.4 and 0.
2. **FTMO is a poor venue for crypto trend.** A −30%/yr swap on both sides with 1:1 leverage costs about 3.4 bp/day on a 0.42-notional book. That is half the gross. Off FTMO (F1-03) the stack's Sharpe doubles to 0.9, still far from 1.95.
3. **The US100 30-minute VWAP rule has been flat since 2023.** It earns nothing on fresh 2025–26 data either: 2025 −10.6 bp, 2026 +3.5 bp per session.
4. **Budget and bar.** 3 of 5 variants were used, and the wave-3 bar of 3.5745 is unchanged. No unregistered variant was run. The verifier and red team ran only diagnostics of the registered positions.

## Files

`agents/prereg/F1.csv` (rules plus results). In `agents/daily/w3-ensemble/`:

| file | what it is |
|---|---|
| `ensemble.py` | the stack, reusing `w1-crypto/d3lib.py` and `vwap30-H0022/vwap30.py` unchanged |
| `run.txt`, `results.json`, `daily_F1-0*.csv.gz` | output |
| `truncation.py`, `truncation-run.txt` | look-ahead test |
| `prop_dollars.py`, `prop_dollars.txt`, `prop_dollars.json` | FTMO $/slot via `w1-prop/prop_model.py` |
| `verify/` | independent re-implementation |
| `redteam/` | red-team scripts and findings |

**Run:**

```
export CLAUDE_SCRATCH=<data dir>
python3 ../2026-10-04/data_fetch.py nq_1m nq_5m
python3 ../w1-crypto/download.py <bin dir>
python3 ensemble.py <bin dir>
python3 prop_dollars.py
python3 truncation.py <bin dir>
```

`ensemble.py` takes about 15 s. The data are not committed.
