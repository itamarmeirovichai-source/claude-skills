# G2 red team: can the negative verdict be overturned?

Short answer: **no.** I found no bug that changes any number. No modelling choice I could find, made as generous as
possible, gets any variant to the bar (t ≥ 3.5914) out of sample. The closest any version gets is **t = 2.79**,
and that version is US-only, zero cost and close fill, which is a cherry-picked information row.

Script: `rt.py`. Output: `rt_output.txt` (run with `G2_CACHE` set to the scratch Yahoo cache). Nothing here is a
counted variant. It is information only.

## 1. Code review of meanrev.py (no bugs found)

| Item | Finding |
|---|---|
| RSI(2) | Wilder smoothing with alpha 1/2, seeded with the mean of the first 2 changes. Matches the rules and the hand test. OK. |
| 3 down closes | `dn & roll(dn,1) & roll(dn,2)`, with the wrapped first 3 values blanked. OK. |
| State machine | Entry at close t, a counter of days held, exit at the first close > SMA5 or on the 5th day, no re-entry on the exit close, 200-day filter checked only at entry, notional fixed at entry. OK. |
| Close fill | Earns `e[t-1] * r_cc[t]`. Cost is charged on the size of each position change at close t. OK, no look-ahead: the decision uses closes up to t and starts earning from t+1. |
| Next-open fill | The overnight leg earns the old exposure and the intraday leg the new one. If the open is invalid, the fill moves to the close. Exits fill at the open after the signal. OK. |
| Swap | %/yr ÷ 365 × calendar nights to the next bar. The sign is kept: long costs, a positive short swap is credited. The %/yr numbers match the points in FTMO's JSON at Oct-2026 index levels. In close mode the swap is booked on the day the position is held through, not the next bar. That is a one-day timing difference and does not matter. |
| Benchmark / alpha | The basket earns the previous day's weight × the return (no look-ahead). OLS uses Newey-West (Bartlett, 10 lags) on X·e. Correct. |
| t / bootstrap | `min(iid, NW)`. Moving-block bootstrap with blocks of 10 via cumulative sums. Correct. Zero-return days on the union calendar barely change t. |
| Independent check | `verifier/verify_run.txt` agrees on every OOS row within 0.01 t. |

Severity: none. Verdict unchanged.

## 2. Is today's swap what kills it? It costs about 1.2 t, but even zero cost fails

- From `run.txt`, the full 10-market book out of sample at **zero cost** (`OOS0`): the best variant is G2-06 close,
  **t = 2.73** (Sharpe 0.72). With spread but no swap (`OOSns`) its best is t = 2.32. **No variant clears 3.5914 even at zero cost.**
- G2-06 next-open, 2013–2026 total, as a fraction of book: gross +17.4%, swap −7.9%, spread −3.1%, net +6.4%.
  Swap takes about 45% of the gross. It is overstated for 2013–21, when rates were near zero, but OOSns already
  sets swap to 0 in every year and still fails.
- Medium caveat: charging today's swap in the zero-rate years is harsh. It explains why the 1x t (0.90) sits so far
  below the gross t (2.4–2.7). It does not change the verdict.

## 3. Does pooling or the equal-risk sizing dilute a real edge? Somewhat, but not to the bar

US-only book (US500, US100, US30), out of sample 2013–2026. Information only, because the subset was chosen
after seeing per-market results.

| Variant | Close, zero cost | Close, 1x | Open, zero cost | Open, 1x |
|---|---|---|---|---|
| G2-06 (3 down closes + 200d) | **t 2.79** | 1.89 | 2.27 | 1.37 |
| G2-02 (3 down closes) | 2.47 | 1.66 | 1.83 | 1.02 |
| G2-05 / G2-07 (RSI + 200d) | 1.96–2.07 | 1.16–1.27 | 2.05–2.07 | 1.24–1.27 |

- Best over all 7 variants × 2 fills × 3 cost levels: **t = 2.79 < 3.5914**. At 1x cost on the decisive (worse)
  fill, the best is 1.37.
- In sample, US-only at zero cost did clear the bar: t 3.70–4.09 for G2-01, G2-02 and G2-06. So the edge has
  **decayed** after 2012 (per trade: US500 down3 +0.50% → +0.36%, US30 RSI +0.41% → +0.25%). It was not hidden by the pooling.
- Sizing: if the notional is rebalanced daily instead of fixed at entry, G2-06 close at zero cost gets t 2.77
  (fixed at entry: 2.73). Sizing is not the issue.
- Low severity: pooling in markets with no OOS edge (UK100, FRA40, HK50, EU50) costs t. But even the best
  hindsight-picked subset, at zero cost, does not pass.

## 4. Look-ahead

None found. The close fill is *not* look-ahead: the position starts earning on the next close-to-close return. It
does assume you can trade at the exact close on a signal computed from that same close. That flatters the close
version a little, but the gate already uses the worse of the two fills, and next-open is usually the worse one.
Truncation and perturbation tests: 20/20 for every variant in both the main code and the verifier.

## Verdict

**The negative verdict stands.** The rules show a gross edge (zero-cost Sharpe about 0.6–0.75) that is real but
modest. Out of sample it never reaches t 3.59 under any fair or generous variation tried here: zero cost, no swap,
US-only, daily-rebalanced sizing.
