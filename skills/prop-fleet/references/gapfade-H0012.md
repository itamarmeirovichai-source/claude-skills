# H0012 / H0017 — S&P overnight-gap fade: result

**Verdict: FAIL. The gap fade loses money in the primary out-of-sample test, so the family is closed. Per the pre-registration, no other k, stop or target is to be tried.**

All three conditions of the fixed decision rule fail, for both H0012 and H0017. Since the worse of the two governs, the result is a FAIL either way.

- **Run:** 2026-10-06, by one research agent.
- **Code:** `agents/daily/gapfade-H0012/gapfade.py`.
- **Full output:** `agents/daily/gapfade-H0012/run.txt`. Every number below is copied from that file.
- **Rules:** `agents/daily/2026-10-04/prereg_gapfade_draft.txt` and ledger rows H0012 and H0017. They were applied as written and nothing was tuned.

## Multiple-testing bar

- `ledger_gate.ledger_n` gives **N = 196**. That is the ledger's count column summed, and it includes H0018.
- The test is one-sided at alpha = 0.05/196 = 2.55e-4, so **z = 3.4753**.
- A positive result would have needed one-sided t ≥ 3.48 on D2 net R, and both lower bounds above zero:
  - the normal bound, mean − z·se;
  - the day-clustered bootstrap bound from `daily/2026-10-05/eng_head/ledger_gate.py`, with 196,000 draws.

## Data (all fetched; nothing was blocked)

| | Source | Check | Sessions used |
|---|---|---|---|
| D1 in-sample | FutureSharks/financial-data `SPXUSD/DAT_ASCII_SPXUSD_M1_2010..2018.csv`, master branch, read on NY clock as `tjr_backtest.load_minutes` does | sha256 recorded in `gapfade.py` | 2,090 (2010-11-15..2018-12-31; 71 have no 15:59 bar) |
| D2 primary OOS | Ascensao/Intraday-momentum-strategy@5a9e9569 `spy_intra_data.csv` (Git LFS), via `daily/2026-10-04/data_fetch.py` | sha256 matches the pin | 1,645 (2019-01-02..2025-07-18; 3 have no 15:59 bar) |
| D3 second OOS | hindsight-finance/Silver-Bullet-AM-Session@9f00a853 `nq_1m.parquet`, via the same script | sha256 matches the pin | 1,349 weekdays with RTH bars, 126 of them roll-excluded (2020-09-01..2025-11-21) |

- **D1 clock check:** in both January and July 2015, average 1-minute volatility jumps at the 09:30 bar. That means the HistData timestamps follow New York time including daylight saving, so no shift was applied.
- **Storage:** the data files sit in scratch only and were not committed.
- **Dependency:** `pyarrow` was pip-installed to read the parquet file.

## Results (R per trade; net = after the 2 bp round-trip cost)

| Dataset | Hyp. | Trades | Trades/yr | Mean R gross | Mean R net | Bootstrap p5 of mean (net) | One-sided t (net) | Win rate (net R > 0) |
|---|---|---|---|---|---|---|---|---|
| D1 SPXUSD 2010–18 | H0012 | 572 | 70.4 | −0.0240 | −0.0614 | −0.1154 | −1.83 | 45.6% |
| D1 SPXUSD 2010–18 | H0017 | 581 | 71.5 | −0.0250 | −0.0626 | −0.1167 | −1.89 | 45.4% |
| **D2 SPY 2019–25** | H0012 | 455 | 69.6 | −0.0950 | **−0.1223** | −0.1821 | −3.35 | 41.3% |
| **D2 SPY 2019–25** | H0017 | 456 | 69.7 | −0.0969 | **−0.1243** | −0.1846 | −3.40 | 41.2% |
| D3 NQ 2020–25 | H0012 | 333 | 63.8 | +0.0307 | +0.0087 | −0.0654 | +0.19 | 49.8% |
| D3 NQ 2020–25 | H0017 | 334 | 64.0 | +0.0305 | +0.0085 | −0.0657 | +0.19 | 49.7% |

- **Bootstrap p5:** 10,000 draws, as the pre-registration asks. There is one trade per day at most, so a day-level bootstrap is the same as a trade-level one.
- **Gross t:**
  - D1: −0.72 for H0012, −0.76 for H0017.
  - D2: −2.60, −2.66.
  - D3: +0.67, +0.67.

### Rule-3 lower bounds at alpha 0.05/196 (net)

| Dataset | Hyp. | Normal bound | Day bootstrap bound (196,000 draws) |
|---|---|---|---|
| D1 | H0012 / H0017 | −0.1778 / −0.1774 | −0.1763 / −0.1759 |
| D2 | H0012 / H0017 | −0.2493 / −0.2512 | −0.2494 / −0.2491 |
| D3 | H0012 / H0017 | −0.1498 / −0.1495 | −0.1493 / −0.1489 |

### Net R by year (number of trades in brackets; H0012)

- **D1:**
  - 2011 +0.027 (66), 2012 −0.005 (70), 2013 −0.072 (65), 2014 +0.005 (78)
  - 2015 −0.223 (73), 2016 −0.037 (72), 2017 −0.132 (70), 2018 −0.051 (78)
- **D2:**
  - 2019 −0.168 (67), 2020 −0.105 (65), 2021 −0.219 (68), 2022 −0.174 (77)
  - 2023 −0.098 (77), 2024 −0.073 (65), 2025 +0.083 (36)
- **D3:**
  - 2020 −0.025 (9), 2021 +0.054 (68), 2022 −0.127 (71)
  - 2023 +0.041 (67), 2024 −0.060 (56), 2025 +0.146 (62)

H0017's figures by year differ only slightly; `run.txt` lists them.

**Exits:**

| | Close | Target | Stop |
|---|---|---|---|
| D2, H0012 | 217 | 107 | 131 |
| D1, H0012 | 259 | 159 | 154 |
| D3, H0012 | 130 | 111 | 92 |

**Correlation with the H0005 momentum sign:** not computed. No H0005 daily series exists in the repository; its ledger row has no result fields.

## Decision rule (fixed in advance) applied

| Condition | H0012 | H0017 |
|---|---|---|
| D2 net lower bound at 0.05/N > 0 (lower of the normal and bootstrap bounds) | −0.2494 → **no** | −0.2512 → **no** |
| D3 net mean has the same sign as D2's | D3 +0.0087 vs D2 −0.1223 → **no** | +0.0085 vs −0.1243 → **no** |
| D1 gross mean > 0 | −0.0240 → **no** | −0.0250 → **no** |
| **Outcome** | **FAIL** | **FAIL** |

The worse of the two governs, and both fail, so **the overnight-gap-fade family is closed**.

In D2 the strategy is not merely flat; it loses money. Net t is −3.35, which comes close to significance in the wrong direction. On SPY after 2019, fading 1-sigma gaps from the 09:31 open lost about 0.12R per trade.

## Implementation choices the pre-registration did not spell out

These were fixed in the script header before any result was computed. None of them was revisited after the results.

1. **Sessions:** a session is a weekday with at least one bar in 09:30–15:59 NY.
   - H0012 uses H0017's prior-session rule: the most recent earlier session. If that session has no 15:59 bar, the day gets no P0 and no gap, and the code does not reach further back.
   - The pre-registration is silent on this point for H0012.
2. **Gap volatility s:** the sample standard deviation (ddof = 1) of the last 20 defined gaps on dates strictly before today. A day with fewer than 20 earlier gaps is not traded.
3. **D3 roll weeks:** these are Monday–Friday of the week holding the third Friday of Mar/Jun/Sep/Dec, plus the following Monday.
   - They are never traded, and their gaps are left out of s.
   - Their bars still provide the prior-session close for the next day.
4. **Gap already filled:** "target already beyond entry" includes entry equal to P0; such a day is skipped.
5. **Target fills:** a target fills at P0, even when the bar opens through it, so there is no price improvement. Stop fills follow the pre-registration: the worse of the stop and the bar open, and the stop counts first when both are touched in the same bar.
6. **Look-ahead in H0012:** H0012 requires today's 15:59 bar, as registered, which is look-ahead. H0017 does not, and it exits at the last bar at or before 15:59.
   - **Future-truncation test:** on 60 random days per dataset, deleting the bars after 09:31 left H0017's trade/no-trade decision, side and entry unchanged.

H0012 and H0017 differ by only 1 to 9 trades per dataset, so the 15:59 look-ahead does not matter for this strategy.

## Caveats (none changes the verdict)

- **D2 is dividend back-adjusted**, as the pre-registration accepts. That takes ex-dividend drops out of the gaps.
- **Fills:** the 09:31 open is a mid-bar print; there is no queue or slippage model beyond the 2 bp cost. Note that D2 is negative even gross (−0.095R).
- **D3 roll:** hindsight's own roll date was not measured. A roll that falls outside the excluded week could leave one cross-contract gap per quarter. D3 enters the decision rule only through its sign, and D2 alone already fails.
