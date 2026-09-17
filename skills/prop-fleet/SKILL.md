---
name: prop-fleet
description: Size, gate and run a fleet of funded futures prop accounts (Apex-style, trailing drawdown, capped payout ladder). Use when deciding position size, when to add an account, whether a payout is ready, or whether a result has earned more exposure. Not for choosing or tuning a trading strategy.
---

# Prop Fleet

Running ten or twenty funded accounts is not a trading problem. It is a manufacturing problem with one scarce input — the account slot — and one statistical gate that decides how many slots you are allowed to run. This skill holds the arithmetic for both, and the rules that keep a bad week from taking the whole fleet.

It never touches strategy. Not entry logic, not grading, not thresholds, not sessions. If the numbers say the edge isn't there, the answer is less exposure, never a re-tuned strategy.

## The three facts that drive everything

**1. The account is a consumable, not an asset.** A funded account closes permanently after a fixed number of payouts, and each payout is capped. On an Apex 50K the six caps are 1500 / 1500 / 2000 / 2500 / 2500 / 3000 — **$13,000 for the whole life of the account**, no matter how well it trades. What you own is a slot that produces a stream of accounts. The question is never "how much is this account worth," it is **how many dollars a year does one slot produce**.

**2. The trailing drawdown stops trailing.** The floor follows the peak until the peak reaches `start + drawdown + $100`, then it locks at `start + $100` forever. On a 50K that means the floor pins at $50,100 once the balance touches $52,600. Every account therefore has two completely different risk regimes, and the dangerous one is only the first $2,600.

**3. The evaluation has a clock; the funded account does not.** Typically 30 calendar days, about 21 trading days, no extension. That single fact inverts the sizing: the evaluation's enemy is time, the funded account's enemy is the floor.

## Sizing

Size from trade geometry — stop distance times point value times contracts. **Never** from account balance times a risk percentage; that is how phantom `pnl_r` values get written and how a record stops being evidence.

| Phase | Risk per trade | Why |
| --- | --- | --- |
| Evaluation | **10% of drawdown** | The fee is small and the clock is the real constraint. Sizing this like a funded account makes most evaluations expire unfinished. |
| Funded | **4% of drawdown** | The slot is worth the full payout ladder. Nothing is worth risking it for speed. |

Cut the size the same day the account converts. This is the rule that is easiest to forget and most expensive to forget.

Micro contracts are a precondition, not a preference. A full ES contract on an 8.5-point stop risks $425 — 17% of a 50K drawdown in one trade. Six in a row and the account is gone, and six in a row happens about monthly at a 45% win rate.

## Payouts

- **Never take a partial payout.** Each slot on the ladder is consumed whether you withdraw the cap or half of it. Withdrawing $900 against a $1,500 cap burns $600 that does not come back. Waiting for the full cap is worth roughly 80% more over an account's life.
- **After every withdrawal, stay at or above the safety net.** Build to safety-net-plus-one-cap, withdraw the cap, land back on the safety net with a full cushion. Withdrawing down to a thin cushion is how accounts die after they were already profitable.
- **On the final payout, take everything.** The account closes regardless; a cushion left behind is money deleted.
- **Stop trading once the next cap is reachable and the qualifying days are in.** Trading past that point risks banked money for nothing.
- **Manage the consistency rule forward, not backward.** If one day exceeds the allowed share of total profit, the payout is blocked until profit grows. Show the number on the dashboard; do not discover it at withdrawal time.

## The gate

Exposure rises only when the evidence rises. The gate is a number, not a feeling.

At 1:2 reward-to-risk, the trades needed before a 95% interval around an observed expectancy excludes zero:

| Observed | Trades | Trading days |
| --- | --- | --- |
| +0.50R | 35 | 12 |
| +0.35R | 70 | 23 |
| +0.30R | 95 | 32 |
| +0.25R | 135 | 45 |
| +0.20R | 208 | 69 |
| +0.15R | 364 | 121 |
| +0.10R | 803 | 268 |

| Stage | Accounts | Until | Gate to the next stage |
| --- | --- | --- | --- |
| 0 | 0 | — | Execution verified clean on a simulated run |
| 1 | 1 | 100 trades | CI lower bound above zero |
| 2 | 3 | 250 trades | CI lower bound above +0.10R |
| 3 | 10 | 500 trades | CI lower bound above +0.20R |
| 4 | 20 | 900 trades | and at least one profitable quarter |

The ladder runs **both ways**. If the lower bound falls back under a gate, exposure comes down. Do not argue with it, and do not re-tune the strategy to make it pass — that is fitting to noise, and it is the single most expensive mistake available here.

Skipping stages upward is allowed when the evidence justifies it. A genuine +0.50R is established in 35 trades; there is no reason to sit at one account for six weeks.

The point of the gate is the asymmetry of being wrong. Discovering there is no edge costs about **$170** with the ladder. Discovering it by running twenty accounts for eight years costs about **$114,000**.

## Copy trading is not diversification

Twenty accounts on the same orders is one bet twenty times over, not twenty bets. One bad sequence takes the whole fleet in a week, and then every slot is paying for a new evaluation at once with no income while they all re-qualify.

Three things reduce this, and only these three:

- **One new account per month.** Staggered start dates are the only real decorrelation available.
- **Different phases, different sizes.** An account below the safety net and an account above it are not the same risk.
- **A global circuit breaker.** After N consecutive losses, every account stops until the next session. With no diversification, the breaker *is* the risk control.

## Record integrity

A fleet is only as good as the record that measures it, and a broken record is worse than none because it reads as evidence.

`scripts/integrity.py` refuses to write a trade that cannot be true, and `scripts/test_integrity.py` covers each failure with a real corrupted row. Wire `validate_trade_record` into the write path and let it raise; a bot that halts loudly beats a bot that logs a fiction.

What it catches:

- A P&L whose sign contradicts direction and prices — a short that "profited" while price rose.
- Entry equal to exit with a non-zero P&L.
- `dollar_risk` of zero, which silently turns every R-multiple into garbage.
- A real P&L recorded as `0.0R` — the calculation returns `None` when risk is unknown, never a number that looks computed.
- A trade with no link back to the setup that produced it.

Alongside it, log the execution gap on every trade: the price the strategy asked for against the price actually filled. An execution-layer bug that silently replaces the strategy's entry with the market price is invisible in P&L and obvious in that one column on day one.

## Scripts

- `scripts/integrity.py` — validators for the trade write path. No dependencies.
- `scripts/test_integrity.py` — 20 tests, each a real corrupted row. `python3 -m pytest`.
- `scripts/apex_model.py` — the fleet simulation: trailing floor with lock, evaluation clock, qualifying days, consistency rule, payout ladder, account closure, fees, commissions, slippage, correlated copy trading, staggered onboarding, tax, and the post-year-N withdrawal split. `simulate()` then `report()`.
- `scripts/ladder.py` — trades needed per effect size, and the cost of each rung if the edge turns out not to exist.

`references/apex-rules.md` holds the rule values the model is built on, and the list of what to confirm with the firm directly before paying for anything. Rules change; the file names its date.

## Voice

Numbers with their sign and their unit. The uncomfortable number in the same register as the good one. When a quantity is unknown, say unknown — not "probably fine," not a fabricated estimate. State plainly which conclusions are solid, which are order-of-magnitude, and which are still open.
