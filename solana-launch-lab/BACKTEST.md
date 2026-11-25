# Backtest — plan fixed before the data was read

This file has two parts. **Part 1 was written and committed before any outcome was collected.** Part 2 is
added after the run. The commit history of this file is the evidence of that order.

> A backtest is weaker evidence than live paper trading. It can show that a rule loses; it cannot show that a
> rule wins. Nothing here is a forecast or advice.

## Part 1 — plan (written 2026-11-23, before the run)

### Questions

1. **Baseline:** if a trader entered *every* readable Pump.fun launch at the same moment after launch, with
   fixed costs and a fixed exit rule, what is the mean net return per trade?
2. **Filter:** does the fixed ruleset `baseline-v1` do better than that, and how many launches does it accept?

### What is fixed, and when it was fixed

| Item | Value | Fixed in |
|---|---|---|
| Filter rule (`backtest` book) | `DecisionRule` defaults in `launchlab/policy.py` | commit `e3b7e29`, pushed before any backtest code existed |
| Baseline rule (`backtest-all` book) | accept every launch that has a price at the decision time | this commit |
| Exit rule, both books | take-profit 2.0×, stop-loss 0.5×, time stop 1,800 s | commit `e3b7e29` |
| Costs and timing, both books | 0.5 SOL per trade, decision at launch + 90 s, 8 s latency, 15% failure chance per attempt, 1% extra slippage, 1.25% curve fee per side, network fees, account rent | commit `e3b7e29` |
| Exit pricing | the position's own SOL is counted as still in the pool at exit (see below) | this commit |
| Rulesets tried | 2 (filter and baseline) | — |

None of these will be changed after looking at results. If a bug in *reading data* is found, the store is
wiped, the fix is described in Part 2, and the run is repeated on a new window.

### One modelling change made before the run, and why

While testing the reader on a few real launches (statuses only, no returns inspected), one flaw in the exit
model became obvious: the recorded history does not contain our paper position, so pricing the exit against
the recorded reserves treats our own SOL as if it had never entered the pool. On a small bonding curve that
turns "bought, nobody else traded, sold" into a large loss, which is wrong: the seller gets their own SOL
back minus fees. The exit is therefore priced as `Q·x / (B − x)` — the recorded pool, shifted by the tokens
we still hold. The old pricing, `Q·x / (B + x)` capped by recorded real SOL, is kept and reported as a
**conservative bound**. The change favours the strategy, which is why both are reported.

### Population and sample

- **Population:** every successful transaction signed by Pump.fun's mint-authority address
  (`TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM`) in the 24 hours ending about 35 minutes before the run
  starts. Every `create` is signed by that address. A probe on 2026-11-23 05:38 UTC found about 26 per
  minute, roughly 37,000 per day. Transactions on that list that are not creations are skipped and counted.
- **Sample:** systematic — every k-th in time order, k chosen to give **500**. No property of a token is used.
- **Readable launches:** SOL-quoted curves, including "Mayhem" launches. Curves quoted in another token
  (USDC, other coins) are counted and reported but not priced; both books reject them.

### How each launch is read

1. The creation transaction's event gives the mint, curve account, creator, starting reserves, quote
   currency and the Mayhem flag.
2. The curve's transactions in the creation slot give the launch-slot buyers and co-signers.
3. The market state is recorded at 40 fixed offsets from launch: 85 s, 100 s, every 30 s to 400 s, then every
   60 s to 2,080 s. The state at an offset is the state after the curve's last informative transaction **at
   or before** that time; a state is never taken from a later transaction.
4. State source, in order of preference: the trade event in that transaction (exact reserves, used for all
   curve types); for non-Mayhem curves only, the curve's token balance with the starting reserves (checked
   equal to trade events on mainnet); otherwise the moment is recorded as unreadable. Mayhem launches are
   never priced by formula, because their agent moves reserves independently.
5. After a migration, price comes from the pool's balances.

### Metric and reading of the result

- **Primary:** mean net return per accepted launch, counting not-filled, failed and unsellable outcomes,
  with a bootstrap interval adjusted for two rulesets.
- **Also reported:** counts at every stage, rejection reasons, win rate, fees, drawdown; the baseline split
  by Mayhem / non-Mayhem; and two sensitivity runs that change no rule — the conservative exit pricing, and
  the random failure chance set to zero.
- **Verdict:** stays `inconclusive` for the filter whatever the numbers are: the evaluation plan needs 200
  resolved candidates over 14 days and this is one day. The baseline is a description of that day.

### Known limits, stated in advance

| Limit | Direction of the error |
|---|---|
| One 24-hour window | Unknown; a single day can be unusually good or bad |
| Our order does not change what other traders did afterwards | Favourable to the strategy |
| No sandwiching or adverse selection beyond the 1% slippage allowance | Favourable |
| State sampled every 30–60 s; moves between grid points are unseen by the exit rule | Either way |
| Creator history is not available, so the serial-creator check never fires | Favourable for the filter |
| The filter is expected to accept very few launches, so its own result will be noisy | — |
| Public RPC allows about one transaction read per second, which caps the sample at about 500 | Wider intervals |
| A launch or moment that cannot be read is counted, not dropped | Slightly conservative |

## Part 2 — results (added after the run)

Run: 2026-11-23 06:12–07:21 UTC on the public Solana RPC, no rate-limit stalls. Window: launches from
2026-11-22 05:37 to 2026-11-23 05:36 UTC. Store: `data/backtest.sqlite3` (not committed; rebuild with
`python -m launchlab backfill --live`, read with `python -m launchlab backfill-report`).

### What was read

| | Count |
|---|---|
| Launches in the window (mint-authority list) | 36,379 |
| Sampled (every 72nd) | 500 |
| Not a creation transaction | 2 |
| Quoted in a token other than SOL (not priced) | 62 (12%) |
| Priced over the whole window | 436 |
| Mayhem launches among the 498 creations | 272 (55%) |

### A bug found after the run, and how it is reported

Looking at the largest wins showed exits that paid more SOL than the venue held: for example +497% on a
position whose pool held 0.36 SOL. Cause: the exit pricing chosen before the run (`Q·x / (B − x)`, own SOL
kept in the pool) uses virtual reserves, and on Mayhem curves — and pools priced with the InitBoost amount —
virtual SOL can be far above the SOL actually there. Fix: proceeds are capped at the venue's real SOL plus
the SOL the position put in. Nothing was re-read from the chain; the books were re-simulated from the stored
observations. The fix only lowers impossible payouts, so it can only make results worse. Both numbers are
shown. The **corrected** figures are the ones to use.

### Results (0.5 SOL per trade, net of all modelled costs)

| | Filter `baseline-v1` | Enter everything `enter-all-v1` |
|---|---|---|
| Launches accepted | 13 of 498 | 429 of 498 |
| Mean net return per trade, corrected | **−32.5%** | **−6.9%** |
| 95% interval (bootstrap, adjusted for 2 rulesets) | −45.7% … −19.8% | −9.7% … −3.3% |
| Mean, as pre-registered (bug included) | −32.5% | −5.2% (−8.9% … −0.6%) |
| Median | −32.4% | −4.9% |
| Winning trades | 0 of 13 | 13 of 429 (3.0%) |
| Net result | −2.11 SOL | −14.91 SOL |
| Exits | 8 time stop, 4 stop-loss, 1 not filled | 357 time stop, 53 stop-loss, 12 take-profit, 7 other |

Baseline by launch type (corrected): Mayhem −6.6% (−9.3% … −3.7%, n 269); standard −7.5% (−13.4% … +0.7%,
n 160). The cap changed only Mayhem trades, as expected.

Sensitivity (corrected model, no rule changed):

| Variant | Filter | Enter everything |
|---|---|---|
| No random transaction failures | −35.9% | −7.1% |
| Conservative exit pricing (own SOL ignored, minimum 1 SOL exit depth) | −78.2% | −66.0% (408 of 429 unsellable) |

The conservative variant is far too harsh for quiet curves — it calls most of them unsellable because they
hold under 1 SOL — and is shown only as a bound.

### Reading

- **Entering every launch loses about the round-trip cost.** 357 of 429 trades ended at the time stop with
  −10% to 0%: nothing happened and the position paid about 5% in fees, slippage, network fees and account
  rent. A few large wins (4 above +100%) did not make up for 25 losses beyond −50%.
- **The filter selected launches that had already moved, and all 13 lost.** Its liquidity rule (at least
  3 SOL in the curve at 90 seconds) mostly admits launches that had already drawn buyers; on this day those
  fell afterwards. This matches the published finding that entering after early signals loses
  (RESEARCH.md, H3). Thirteen trades from one day is far too few to rely on.
- **Verdict, as planned:** `inconclusive` for both — one day, not the 200 trades over 14 days the plan
  requires. As a description of this day: neither rule made money after costs, and the interval for
  "enter everything" lies entirely below zero.
- **Modelling direction:** the run still favours the strategy in the ways listed in Part 1 (no front-running,
  our orders do not change others' behaviour). One cost is slightly overstated: the 0.0015 SOL token-account
  rent is recoverable when the account is closed (about 0.3% per trade).
