# W1 D4 — Intraday breadth: FAIL

**Verdict: FAIL, all 5 pre-registered variants.**
- Run across 19 markets, every rule loses money after costs out of sample (2013 to May 2020), with t between −4.3 and −16.
- Even at **zero cost**, none clears the bar of t ≥ 3.5504. The best, TWAP trend, reaches gross t +3.53.
- Breadth did not lift a Sharpe-1 edge to Sharpe 3, for two reasons:
  - the gross intraday edges mostly vanished after 2012;
  - the markets' daily P&Ls are correlated enough that 19 markets act like about 8.

Every number below comes from `agents/daily/w1-breadth/breadth.py`, whose output is in `run.txt`. An independent verifier re-implemented the rules from the written spec alone (`verifier/verify.py`, `verifier/verify_run.txt`) and got the same means and t-statistics for all five variants.

## What was tested

The rules were pre-registered in `agents/prereg/D4.csv` and `agents/prereg/D4-spec.md` (commit e614c5a). That commit was pushed before any backtest code existed. Five variants were counted against a budget of 15.

- **The basket.** It is free 1-minute data:
  - Oanda mid candles, 2005 to May 2020, from FutureSharks/financial-data;
  - HistData DAX and EuroStoxx 50, 2010 to 2018.
- **Eligibility filter.** It was fixed in advance and uses volatility only: a market stays in if its round-trip cost is at most 10% of its in-sample session volatility. 19 of 23 markets passed:
  - 6 FX pairs;
  - 10 equity indices: SPX, NAS100, Russell 2000, FTSE, CAC, AEX, Nikkei, ASX 200, DAX, EuroStoxx;
  - gold, WTI and natgas.
  - Corn, soybeans, wheat and sugar were dropped, either for too few in-sample sessions or for cost.
- **Sessions.** Each market trades in its own local session, for example the London open for FX and the cash open for indices. Every position is flat at the close, so there is no swap.
- **Sizing.** Every market is sized to 1% session volatility, using the past 60 sessions. The basket return is the average across markets.
- **Costs.** Per side, they are 0.5 to 0.9 bp for FX, 0.8 to 1.5 bp for indices, 1 bp for gold, 2.5 bp for WTI and 8 bp for natgas. Every result was also run at 2× cost.
- **Splits.**
  - In-sample: 2005 to 2012.
  - Out-of-sample: 2013-01 to 2020-05, 1,908 days.
  - Held-out markets: 6 of them, never computed in-sample. They are DAX and EuroStoxx, plus GBP_USD, AU200, natgas and JP225, drawn with a fixed seed.

| id | rule |
|---|---|
| D4-01 | Gao et al. last half hour: the sign of the move from the previous close to open+30 min. Trade it from close−30 to the close. |
| D4-02 | Same signal, held from open+30 to the close. |
| D4-03 | TWAP trend: every 30 minutes, go long if price is above the session TWAP and short if below. Flat at the close. |
| D4-04 | 30-minute opening-range breakout: first break only, stop at the other side of the range, exit at the close. |
| D4-05 | Fixed equal blend of D4-01 to D4-04. |

## Results (out of sample, all 19 markets)

**Units:** the basket's mean daily return in %, when every market targets 1% session volatility.

| | gross mean | gross t | **net mean** | **net t** (min of iid and NW) | net bootstrap p5 | net Sharpe | max DD at 10% vol | net at 2× cost (t) |
|---|---|---|---|---|---|---|---|---|
| D4-01 | +0.002 | +0.80 | **−0.037** | **−16.05** | −0.041 | −5.83 | 460% | −0.075 (−32.4) |
| D4-02 | +0.001 | +0.13 | **−0.037** | **−4.83** | −0.052 | −1.75 | 141% | −0.076 (−9.7) |
| D4-03 | +0.027 | +3.53 | **−0.111** | **−13.83** | −0.126 | −5.03 | 387% | −0.250 (−29.5) |
| D4-04 | +0.013 | +2.30 | **−0.025** | **−4.56** | −0.034 | −1.56 | 119% | −0.063 (−10.9) |
| D4-05 | +0.011 | +2.86 | **−0.053** | **−13.57** | −0.060 | −4.93 | 378% | −0.116 (−29.1) |

### Gate (bar 3.5504)

| Condition | Result |
|---|---|
| G1: t ≥ 3.5504 | **fails for all 5** |
| G2: bootstrap p5 > 0 | **fails for all 5** |
| G3: held-out markets net > 0 | **fails for all 5** (−0.018 to −0.107) |
| G4: in-sample design gross > 0 | passes for all 5 |
| G5a: truncation test | passes: 488,992 cut points with 0 mismatches, and σ̂ always uses past sessions only |
| G5b: 7 unit tests | pass (`pytest.txt`) |

**→ FAIL.**

### Correlation between markets (OOS daily net P&L per market)

- The mean pairwise ρ is +0.06 to +0.08. The maximum is +0.83, from the European indices with each other and from the US indices with each other.
- The effective number of independent markets is K/(1 + (K−1)ρ̄), which comes to **7.9 to 9.0 of 19**.

### In-sample vs out-of-sample (gross, design markets)

| | IS gross t | OOS gross t |
|---|---|---|
| D4-01 | +6.81 (Sharpe +2.37) | +0.80 |
| D4-03 | +4.05 | +3.53 |
| D4-05 | +4.77 | +2.86 |

- Gao's last-half-hour effect was strong before 2013 across this basket and almost gone afterwards. That matches H0006's failure on the S&P.
- Per market out of sample, no market has a positive net Sharpe on D4-01 or D4-03. D4-02 and D4-04 have a few small positives, all ≤ +0.33.
  - The FX pairs and natgas are the worst.
  - The US indices on D4-02 are about flat (+0.03 to +0.13).

## Data checks (`data_check.txt`, `clock_xcorr*.txt`)

- **Oanda clock is UTC.** For example, US 08:30 news shows up at 13:30 UTC in winter and 12:30 in summer, and the FTSE open at 08:00 in winter and 07:00 in summer.
- **The HistData DAX and EuroStoxx files are not on fixed EST, as HistData documents.** They follow **New York local time with DST**.
  - Against Oanda, the best-fitting shift is 0 in US-winter months and −60 minutes in every US-summer month. The same holds for HistData SPXUSD and JPXJPY.
  - This was found and fixed before any strategy return was computed. After the fix, the shift is 0 in all 96 months.
  - **Note for the organisation:** earlier tests on SPXUSD that assumed fixed EST would be off by one hour in summer. The H0019 to H0022 loaders already use a New York clock, so they are consistent with this finding.
- **Gaps:**
  - FX, US/EU indices, gold and WTI have under 0.3% thin sessions.
  - AU200 has 18% thin sessions and JP225 10%. JP225 has no Tokyo-hours bars before 2010.
  - Oanda UK100 has no bars in the 10 minutes before 08:00 London until about mid-2015. Read literally, the spec then gives no σ̂ and no trade, so UK100 trades only about two thirds of its OOS days. Both the head and the verifier read it this way. As a sensitivity run, the verifier filled the open from F(O) instead. Every variant stayed negative (net −0.028 to −0.130).

## Red-team view

- **Could a bug make it falsely negative?** No sign flip would rescue it. The gross is near zero for D4-01 and D4-02, and only modestly positive for D4-03 to D4-05. Costs explain the net losses: TWAP trades about 7.4 sides a session, and the others about 2.
- **Are the costs too high?** Every variant fails even at zero cost: the best gross t is +3.53 against a bar of 3.5504. Cheaper execution cannot rescue it.
- **Could breadth still work?** The arithmetic was right, but its premise was not. Sharpe 1 per market × √(effective N ≈ 8) would give about Sharpe 2.8. Out of sample, though, the per-market gross Sharpe is near zero, not 1.
- **Did we look at the data before deciding?** The in-sample period chose nothing. The held-out markets were never computed in-sample. Out of sample, the held-out markets lose just as much as the design markets.

## What it means for the wave

- Simple open-to-close intraday time-series rules on free 1-minute data do not form a gate-passing basket after 2012, in FX, index or commodity CFDs. This is the fifth intraday family closed, after H0006, H0020, H0021 and H0022.
- The one gross signal that survives out of sample is TWAP/VWAP trend: gross Sharpe +1.28 across 19 markets, about the same as on NQ. Its turnover makes it negative after any realistic cost.
  - A lower-turnover version would be a **new** counted variant. D4 has 10 left in the budget, but the expected net is small. Even zero cost does not reach the bar.
- **Recommendation:** stop D4 intraday work. Move the budget to multi-day horizons (D2 trend and carry), where the edge comes from holding periods that costs cannot eat.

## Files

All files are in `agents/daily/w1-breadth/`:
- `fetch.py` and `manifest.csv`: data and sha256 hashes.
- `common.py`, `strategies.py` and `breadth.py`: the run.
- `test_strategies.py` and `pytest.txt`: unit tests.
- `data_check.py`, `clock_xcorr.py` and their outputs: data checks.
- `verifier/`: the independent re-implementation.

The pre-registration with filled results is in `agents/prereg/D4.csv`.
