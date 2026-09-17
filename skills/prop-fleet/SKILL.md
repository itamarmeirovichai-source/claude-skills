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

The percentage is the target; the contract count is an integer. On an 8.5-point stop one MES is $42.50, so the reachable steps are $42.50, $85, $127.50 — there is no exactly-4% position on a 50K. Pick the nearest count **for that trade's stop width**: a tighter stop takes more contracts. Averaged over many trades the realised risk converges on the target, which is what the model assumes; on any single trade it ranges roughly 3.4% to 5.1%.

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

Run `scripts/gate.py` against the trade record weekly rather than deciding by hand. A losing run makes you want to shrink and a winning run makes you want to grow, and neither feeling is evidence; the same formula every week is not moved by either. It reads the record, computes the expectancy and a bootstrap interval, and names the stage — and it refuses to answer at all on a sample too small to carry one, rather than returning a number that looks authoritative. It warns first if the record contains rows that cannot be true, because an expectancy computed over corrupted rows is worse than no number.

**The lower bound of the interval decides, never the mean.** A mean of +0.40R over 20 trades is noise; +0.25R over 400 is a business.

## Losing runs, and why they don't change the size

Losses in a regime-dependent methodology arrive in runs, and a run is worse
against a trailing floor than the same losses scattered. Tested at constant
expectancy on a fixed horizon, clustering leaves the mean result flat through
realistic levels and costs about 8% at the tenth percentile. The recommended size
holds.

What clustering does change is the number of accounts destroyed — 52 to 186 over
eight years going from independent trades to strongly clustered ones, and roughly
double that again at 6% of drawdown instead of 4%. Sizing down is bought with
operational calm, not with expected dollars.

Be careful reading a model that says heavy clustering *increases* the mean. That
is the asymmetric payoff — loss capped at the fee, gain capped at the ladder —
combined with a simulation that replaces a dead account instantly and for free.
A firm watching an account die every day will not behave like the simulation.

## Copy trading is not diversification

Twenty accounts on the same orders is one bet twenty times over, not twenty bets. One bad sequence takes the whole fleet in a week, and then every slot is paying for a new evaluation at once with no income while they all re-qualify.

Three things reduce this, and only these three:

- **One new account per month.** Staggered start dates are the only real decorrelation available.
- **Different phases, different sizes.** An account below the safety net and an account above it are not the same risk.
- **A global circuit breaker.** After N consecutive losses, every account stops until the next session. With no diversification, the breaker *is* the risk control.

## Operating cadence

Twenty accounts are unmanageable as twenty decisions. They are manageable as one
decision repeated, on a fixed rhythm.

**Every trading day.** Check that every account took the same trades — they copy
the same orders, so any divergence is an execution fault, not luck: an order that
never arrived or filled somewhere else. Check the execution gap column. Confirm
no account is below its safety net while being traded at funded size.

**Every week.** Run the gate against the trade record and act on what it says,
including downward. Note which accounts are within one cap of a payout and which
are in the dangerous stretch below the safety net. Check the consistency figure
on any account approaching a withdrawal.

**Every month.** Open the next account, if the gate permits it — one, never
several. Reconcile payouts received against payouts requested. Set aside tax on
everything received. Re-read the firm's rules page for changes.

**Every quarter.** Re-run the fleet model with the actual expectancy rather than
the assumed one, and with any rule values that have changed. Compare the accounts
burned against what the model expected; a burn rate well above it means the size
is wrong or the strategy has drifted, and the first is far more likely.

**Never do on a schedule:** change position size after a losing run, add an
account because the last one paid out, or adjust the strategy because a quarter
disappointed. Those are the three decisions that feel most justified in the
moment and are worth the most money to skip.

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

## Level conversion

Where a strategy computes levels on one instrument and orders are placed on another — a futures contract analysed, an ETF traded — the conversion has one invariant:

```
proxy_level / proxy_market_price  ==  level / source_market_price
```

Every level keeps its position relative to its own market price. The ratio must come from a **live reference pair**, the two instruments' current quotes. Deriving it from the entry price instead collapses the arithmetic — `entry / (entry / etf_price)` is `etf_price` — so every order goes out at market and all the waiting the strategy does is thrown away in the execution layer. The distances still look right, because stop and target convert correctly, which is why this survives review.

`scripts/proxy_fix.py` implements the conversion with the invariant asserted on every call rather than only in tests. A sanity range on the output price cannot catch this: the collapsed value is a real market price and passes any range check.

## Diagnosing a price that doesn't match the market

When recorded prices drift from what the market actually did, find the moment in real bar data when the price was closest to the recorded one, and compare it to when the record was written. The gap separates the causes:

| Gap | Cause |
| --- | --- |
| ~0 | no drift |
| constant | a cache whose TTL never expires or whose refresh fails silently |
| grows with time, matching moments converge on one date | a frozen anchor — a reference value set once and never updated |
| noisy, no structure | not a stale price; the numbers are being computed, not read |

A constant gap and a growing gap are different faults, and the difference is in
the *spread* of the gap rather than its correlation with time: a cache returns
the same staleness every time, while a frozen anchor falls further behind.
Getting that backwards makes the tool give a vaguer answer than it has.

The nearest-moment search has a real limit worth knowing: with a dense bar series
the average gap between adjacent bars can be a thousandth of a percent, so almost
any price in range finds a near-perfect match by chance. A low match error there
rules out "computed" only weakly. `scripts/lag_scan.py` settles it properly by
comparing each record against the price at an actual time offset and finding
which offset minimises the error — a sharp minimum is the lag, a flat curve means
the price was never read from history at all.

Two things about that scan are easy to get wrong, and both were got wrong first.

A median taken over a shrinking population measures who dropped out, not what
matched. Setups near the start of the bar series cannot be evaluated at large
offsets, so they fall away as the scan deepens — and if those are the noisy ones,
the curve falls for reasons that have nothing to do with the price. Every scan
here locks its cohort up front: only setups measurable at every offset in the
range are counted, and the reported `n` is constant across the whole curve.

A minimum is not a finding unless the error rises again on the far side of it. A
curve that only climbs has a lowest point too, sitting uselessly on the window
edge. The verdict keys on the rise on *both* sides of the minimum, measured at a
fixed physical distance rather than a fixed number of grid points — on a
one-day grid the adjacent point is still inside the trough, which is how a real
15-day lag came back as "a weak hint". The absolute threshold that produced that
reading is gone: an entry is a computed FVG level, not a quote, so a residual of
a few tenths of a percent is what a correct match looks like.

`scripts/lag_refine.py` then asks the question that decides which bug to hunt:
is the lag a fixed duration or a fixed number of bars? The two are different
faults with different fixes, and they separate on weekends — a bar offset skips
the gap, a duration falls into it. Scanning both units over the same physical
span and comparing is the whole test; a duration wins for a cache or a file that
stopped refreshing, a bar count wins for an index returning `bar[-N]`. Checking
one unit alone is not enough: on a planted bar offset the time scan still
reports a plausible ~15-day lag, and only the comparison exposes it.

Whether that comparison can answer at all depends on the residual, and the
tool says so rather than guessing. Because an entry is a computed level and
not a quote, a residual survives even at the correct offset, and it is what
decides the question. On planted data the margin between the two units is
1.71 at 0.3% residual, 1.24 at 0.6%, and 1.13 at 0.9% — it collapses toward
1.0 *even when a bar offset is genuinely the truth*. So a narrow margin is
never evidence against either unit; it means the data cannot separate them,
and declaring a winner there invents an answer. The existence of the lag is
a separate and far more robust question: the two-sided trough is 2.5–2.7
whenever a lag is planted and exactly 1.00 when none is, at every noise
level tested. Existence keys on the trough, unit keys on the margin, and
above a 0.55% residual even the trough goes blind (a real lag scored 1.99
there), so a negative verdict at that level is reported as weak.

There is also a structural limit worth knowing: a 15-calendar-day lag maps
to the same 11 trading days almost every time, so the weekend-crossing
setups that would separate a duration from a bar count are a small minority.
`decide_by_divergence` isolates exactly those setups and says how many
there are; when too few exist it reports the unit as undecided rather than
ruling on setups that carry no information.

`scripts/drift_diagnostic.py` runs this plus two cheap alternatives (swapped
symbol, constant factor). It is verified against synthetic data for each verdict
it can return: a planted frozen anchor (it names the planted date), a cache with
a planted five-day TTL (it names the five days), prices that never occurred in
the market, and clean data, where it draws no conclusion.

## Scripts

Start with `scripts/doctor.py`. It runs the relevant checks in order and names
the one blocking thing, so the other scripts do not have to be remembered.


- `scripts/doctor.py` — one command for the whole state: environment, whether the conversion bug is still in the execution layer, record integrity, the stage the gate permits, whether the price data for the drift diagnostic is present, and what is waiting on other people. Reads only. Takes an optional home directory.
- `scripts/test_doctor.py` — 22 tests on the bug detection, which is the highest-stakes logic here: a false alarm is annoying, a missed detection ships a broken bot that looks fixed.
- `scripts/integrity.py` — validators for the trade write path. No dependencies.
- `scripts/test_integrity.py` — 20 tests, each a real corrupted row. `python3 -m pytest`.
- `scripts/apex_model.py` — the fleet simulation: trailing floor with lock, evaluation clock, qualifying days, consistency rule, payout ladder, account closure, fees, commissions, slippage, correlated copy trading, staggered onboarding, tax, and the post-year-N withdrawal split. `simulate()` then `report()`.
- `scripts/gate.py` — reads the trade record and names the stage the evidence permits, including downward. Takes a `trades.db`, a CSV of `pnl_r`, and `--stage N` to compare against where you are now.
- `scripts/test_gate.py` — 19 tests on the decision logic, since the numbers are the decision.
- `scripts/test_apex_model.py` — 21 tests on the model's mechanics: loss bounded by fees, withdrawals arriving only in whole ladders, the evaluation clock expiring an unreachable target, tax never touching a loss, and the withdrawal split. Deterministic, by driving the model to always-win and always-lose.
- `scripts/ladder.py` — trades needed per effect size, and the cost of each rung if the edge turns out not to exist.
- `scripts/horizon.py` — when compounding on extracted profit starts to matter, which inside eight years it does not.
- `scripts/claims.py` — recomputes every arithmetic claim in the write-up from scratch. Run it after editing any number; it caught a real error where two figures were quoted from different configurations.
- `scripts/proxy_fix.py` — correct futures-to-ETF level conversion with the invariant asserted on every call. Run it directly for a numeric before/after.
- `scripts/test_proxy_fix.py` — 21 tests; the first reproduces the collapse bug and proves the invariant catches it.
- `scripts/lag_scan.py` — the coarse pass: how far behind the market a recorded price sits, in whole days, against a real time offset instead of a free search. Locks its cohort and judges by the rise on both sides of the minimum. Hands off to `lag_refine.py`.
- `scripts/lag_refine.py` — the decisive one: refines the lag to the hour and rules on whether it is locked to a duration (a cache) or to a bar count (an index bug), by scanning both units over the same span.
- `scripts/test_lag_refine.py` — 15 tests. Both directions on planted data, a replica of the real 60-session/304-setup situation in each direction, proof that a shrinking cohort really can manufacture a minimum and that locking it removes one, and proof that a time-only reading would have misread a planted bar offset.
- `scripts/drift_diagnostic.py` — locates the cause of recorded prices that don't match the market. Takes an optional directory argument.
- `scripts/test_drift_diagnostic.py` — 18 tests on which fault the gap implies, using the figures actually measured on planted data, so the thresholds can be tuned without silently breaking the distinction.
- `scripts/streak_check.py` — losing-run tail under each clustering setting, to confirm a stress test is actually stressing something.

`references/apex-rules.md` holds the rule values the model is built on, and the list of what to confirm with the firm directly before paying for anything. Rules change; the file names its date.

`references/verification-letters.md` is that list already written as two letters to send — one to the firm, one to an accountant. Both questions are answered by other people rather than by analysis, and left as headings they stay open for months. The firm's letter leads with automated order routing because it is the one risk in the plan not bounded by fees: if the order path is not permitted, accounts close and earned payouts can be voided. The accountant's letter carries the facts that decide whether this is business income or a capital gain, which over eight years is worth more than most of the trading decisions.

## Voice

Numbers with their sign and their unit. The uncomfortable number in the same register as the good one. When a quantity is unknown, say unknown — not "probably fine," not a fabricated estimate. State plainly which conclusions are solid, which are order-of-magnitude, and which are still open.
