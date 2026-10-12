# Waves 1 and 2: synthesis (12 Oct 2026)

**Target (Itamar, 11 Oct):** $20,000 a year net to Itamar for every $100,000 of funded account,
fully automatic, on many accounts.

## What the target needs (D1 model, FTMO Swing 2-Step 100K, re-run 12 Oct with n=1500 paths)

Net dollars per $100K slot per year, before tax. The model picks the volatility that gives the
most money, up to the cap shown.

| Sharpe | vol cap 12% | vol cap 20% | no cap (picks 30–40% vol) |
|---|---|---|---|
| 0 | $1.8k | $5.0k | $11.1k |
| 1.0 | $8.1k | $13.9k | $25.0k |
| 1.17 | $9.4k | $16.1k | $28.1k |
| 1.5 | $12.1k | **$20.6k** | $34.3k |
| 2.0 | $16.5k | $28.0k | $43.1k |
| 2.5 | **$20.9k** | $35.9k | $53.7k |

**How to read it:**

- At a sober volatility (12%), the target needs Sharpe of about 2.5.
- At 20% volatility it needs about 1.5.
- With no cap the model says even zero edge pays.

That last row is the prop-firm "lottery": you buy many evaluations, pass a few by luck, and
collect payouts before the account blows. Do not trust it, for three reasons:

1. **The firm may refuse it.** Firms have discretionary clauses on gambling, "all-or-nothing"
   trading and risk management (D5).
2. **Most attempts fail.** Pass rates are 21–34%, so most of the money spent is lost fees.
3. **Our model may be wrong here.** It has not been validated at high volatility: it ignores
   gaps, weekend jumps, and the 5% daily-loss rule interacting with fat tails.

## What we have

Every strategy tested fails the gate (N = 254, bar t of about 3.55):

| Dept | Area | Best result | Gate |
|---|---|---|---|
| H0001–H0022 | S&P/NQ intraday (bot, TJR, ORB, VWAP, gap, IBS, gamma …) | NQ 30-min VWAP net t 1.68 | fail |
| D2 | FX/CFD trend + carry, 2013–2026 | OOS Sharpe ≤ 0.16 | fail |
| D3 | crypto | vol-managed TSMOM t 2.15, mostly beta | fail |
| D4 | intraday rules across 19 markets | net negative | fail |
| E1 | stock CFDs at FTMO | all negative; 1:1 leverage + two-sided swap kill it | fail |
| E2 | macro-event intraday ES/NQ | best t 1.09 | fail |

## Firms (D5 + D1)

- **Safe list:** FTMO, MyFundedFutures, Lucid, Topstep, TradeDay.
- **Allowed overnight:** only the forex/CFD/crypto firms (FTMO, Blue Guardian, CFT).
- **Futures firms** force you flat every day.
- **FTMO cap:** $400k per strategy, so about 4 × $100k.

## Honest bottom line

On free data, no tested strategy has the Sharpe of 1.5–2.5 the target needs. The remaining
routes are:

- **(a)** a combination of near-misses that are only weakly correlated (wave 3, free);
- **(b)** a test of whether higher-volatility sizing is contractually and statistically safe at
  the safe-list firms (wave 3, free);
- **(c)** paid multi-asset intraday data, which needs Itamar's decision.

## Update 12 Oct (waves 2 and 3)

- **E1 failed.** Stock CFDs on FTMO lose: leverage is 1:1 and FTMO charges swap on both sides.
- **E2 failed.** Macro-event intraday trading peaks at t 1.09.
- **F1 failed.** The ensemble of near-misses reaches only Sharpe 0.41 at FTMO costs.
- **F2 (stressed): the Sharpe needed for $20k per $100K at FTMO** is about 2.4 at 12% volatility, about 1.9 at 15% and about 1.5 at 20%. The Sharpe-0 lottery does not survive. Volatility of 15–20% is defensible under the contracts; 30% or more is not.
- **The gap between what we have and what we need is still large.** The best real out-of-sample Sharpe we have measured since 2013 is about 0.4–0.8. The target needs at least 1.5.

## Update 12 Oct, director's own checks after wave 3

- **Skew does not rescue the prop structure.** Script: `agents/daily/w3-volrisk/skew_check.py`. It is a simplified FTMO 2-step model with 4,000 paths. At the same mean and volatility:
  - negative skew (steady gains, one −6% day a year) pays **less** than symmetric returns: at S=0 and 12% volatility, $641 against $1,043 a year;
  - positive skew pays about the same.

  Sharpe and volatility decide everything. The jump breaches the 5% daily limit.
- **H0023, turn of the month on the S&P 500: FAIL.** Out-of-sample t is 1.56 and Sharpe 0.38. Buy-and-hold scaled to the same exposure did better (Sharpe 0.76): the effect has been gone since 2010.
