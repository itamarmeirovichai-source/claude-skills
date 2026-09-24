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

**That table assumes trades are independent, and it is the wrong unit besides.**
It is the arithmetic of σ≈1.45R per trade at three trades a day, and it
reproduces to the row. Two things are wrong with using it to decide when to wait.

The independence assumption turns out to cost little here. The cluster-robust
standard error measured on the replay is 0.145R against 0.138R assuming 111
independent trades — **5% wider, a variance inflation of 1.11**. Trades opened
the same afternoon do share a regime, but empirically in this data they barely
do. Say that plainly rather than gesturing at clustering as though it were large.

The unit is the real problem. The right-hand column counts elapsed trading days
and assumes every one of them carries three trades; the clean window produced
trades on only 28 of its 41 trading days. Counting what the error actually
shrinks in — days with a trade in them — and converting at the ~14 such days a
calendar month supplies, the honest horizons are **227 days-with-a-trade at
+0.10R (15.8 months), 103 at +0.15R (7.2), 59 at +0.20R (4.1), 39 at +0.25R
(2.7), 28 at +0.30R (2.0) and 12 at +0.50R (0.8).** `scripts/detect.py` computes
both directions and holds them under test; use it rather than the table above
when the answer decides money. The trade counts in the stage ladder below are
floors — necessary to reach a stage, never sufficient, since the clustered lower
bound is what `gate.py` actually rules on.

| Stage | Accounts | Until | Gate to the next stage |
| --- | --- | --- | --- |
| 0 | 0 | — | Execution verified clean on a simulated run |
| 1 | 1 | 100 trades | CI lower bound above zero |
| 2 | 3 | 250 trades | CI lower bound above +0.10R |
| 3 | 10 | 500 trades | CI lower bound above +0.20R |
| 4 | 20 | 900 trades | and at least one profitable quarter |

The ladder runs **both ways**. If the lower bound falls back under a gate, exposure comes down. Do not argue with it, and do not re-tune the strategy to make it pass — that is fitting to noise, and it is the single most expensive mistake available here.

Skipping stages upward is allowed when the evidence justifies it. A genuine +0.50R clears the lower bound in about 12 days with a trade in them — under a month of calendar trading — so there is no reason to sit at one account waiting out a schedule.

The point of the gate is the asymmetry of being wrong. Discovering there is no edge costs **$165** with the ladder — a $40 evaluation, $85 on activation, and one $40 re-buy if the account is destroyed during the 100 trades. Discovering it by running twenty accounts for eight years costs **$48,564** at an expectancy of exactly zero and **$114,725** at −0.10R, which is inside the current interval. Both figures come out of `apex_model.py` at the correct two-speed sizing; the ratio between them is checked in `claims.py`.

`references/schedule.md` works this out against the calendar, because the brief asks for the first account within two weeks and another every month after. The first of those is compatible with the gate and the second is not: stage 1 needs only a clean simulated run, so one evaluation on 3 October 2026 is fine, but twenty accounts is 19 to 27 months of *trading* away rather than twenty months of *buying* — and only if the edge turns out to be real.

Run `scripts/gate.py` against the trade record weekly rather than deciding by hand. A losing run makes you want to shrink and a winning run makes you want to grow, and neither feeling is evidence; the same formula every week is not moved by either. It reads the record, computes the expectancy and a bootstrap interval, and names the stage — and it refuses to answer at all on a sample too small to carry one, rather than returning a number that looks authoritative. It warns first if the record contains rows that cannot be true, because an expectancy computed over corrupted rows is worse than no number.

**The lower bound of the interval decides, never the mean.** A mean of +0.40R over 20 trades is noise; +0.25R over 400 is a business.

Price the goal before arguing about it. A 20%-a-year target is a threshold on expectancy: **+0.250R** at 4% of drawdown and a 25% tax rate, +0.340R if the income is classified as business income, and +0.182R even at 8% of drawdown — which triples the rate at which accounts are destroyed. No sizing dial closes a gap of that size, and adding accounts changes the dollars without changing the percentage at all. Either the strategy clears the threshold or the target is wrong; those are the only two options, and which one holds is measurable rather than arguable.

## Twenty 50K accounts or ten 150K accounts

Twenty 50K, but not for the reason that presents itself first — and the
reasoning matters more than the answer, because the answer has a condition
attached.

The 50K payout ladder pays $13,000 against $2,500 of drawdown; the 150K pays
$18,000 against $5,000. That is 5.20 versus 3.60 per dollar you are allowed
to lose, a 44% advantage to the small account, and it holds without assuming
anything about expectancy. It is tempting to stop there. It is also wrong to
stop there: the large ladder is bigger in absolute terms, and once there is a
real edge the absolute size is what compounds. The ratio and the total point
in opposite directions.

Holding the account count equal separates the plan from the quantity, and it
reverses the verdict. At ten accounts each, the 150K wins above roughly
+0.10R and the margin grows with expectancy; the 50K wins at zero and below.
The crossover sits between +0.08R and +0.10R. So what actually decided the
original comparison was twenty against ten, not 50K against 150K.

What survives is a conditional answer, which is the more useful one:

- **With no edge, or a negative one, the small account is better and clearly
  so.** At equal sizing and equal count, an expectancy of exactly zero costs
  $25,942 on the 50K against $99,315 on the 150K. That is not a return; it is
  the price of finding out you were wrong, and the small account charges a
  quarter of it.
- **With an edge established above about +0.10R, the large account is better
  per slot.**

The crossover sits inside the range the gate exists to resolve, so this is
not a separate decision — it is the same measurement. Today, with a negative
lower bound, the direction is the small account: cheaper to be wrong in, and
it is also the one that buys twenty slots instead of ten. If the expectancy
is ever measured above +0.10R with confidence, the question reopens.

One detail decides more than it looks like it should. Risk is a percentage of
drawdown and contracts are indivisible. At 4%, the 50K wants $100 against
$42.50 per contract — 2.35, rounding to 2, so it risks 15% *less* than
written. The 150K wants $200, gets 4.71, and rounds to 5 — 6% *more*. The
rounding alone pushes the two plans in opposite directions, and it is not a
rounding error in the reporting: it is the risk actually taken.

`scripts/plan_choice.py` reproduces all of this, and `scripts/test_plan_choice.py`
keeps the conclusion conditional — one test fails if anyone flattens it back
into "the small account always wins".

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

That subset is tens of setups, not hundreds, where a median is noisy — so
the ruling is an exact paired sign test rather than a comparison of
medians. Each setup is measured twice, once under each hypothesis, and the
pairing is what extracts the signal. Calibrated at the real noise level, a
planted bar offset comes back significant (p ≤ 0.002) in four seeds out of
five; the fifth misses, which is the test's honest error rate and is
documented rather than hidden. A planted duration leaves too few divergent
setups to run at all.

All of that covers one era. The bot ran on SPY and QQQ until 15 May and on
futures scale from 18 May, and the diagnosis rests entirely on the first
period, because that is the only one with independent bars to compare
against. The 131 setups after the switch had never been checked, and they
are the ones that decide whether any usable evidence exists at all — a
question worth more than refining the first era further.

`scripts/futures_era_check.py` answers it with hourly bars. IBKR refuses
historical continuous futures, but the feed's own config allows two years of
hourly data, which reaches back past May. An hour is coarse against
five-minute setups and adds roughly a tenth of a percent, which is nothing
against a four-percent signal and a fifteen-day lag.

The catch is that those bars come from the same provider whose live path was
suspect, so a clean result could just be a shifted series compared against
itself. The script therefore runs the ETF era first as a control: if hourly
yfinance reproduces the trough that IBKR bars produced, the source is a valid
witness and the futures test means something; if it does not, the script says
the test is void rather than reporting a result. The verdict is asymmetric on
purpose. "Lagged" keys on the trough alone, because the trough is what stays
stable across noise and volatility, while the error at zero offset measures
how far the market happened to move over the lag window — the same fault
reads 4.5% in a volatile stretch and 1.5% in a quiet one. An earlier version
demanded both and threw away a genuine lag in one seed of five. "Clean"
demands both a flat curve and a small error at zero, since proving a recorded
price was the prevailing price takes more than failing to find a lag.
Everything else is left explicitly undecided.

## Replaying the valid setups

Knowing which setups are trustworthy is not the answer, only the
precondition. Seven closed trades average −0.384R with an interval of
[−1.455, +0.687], which is consistent with an excellent strategy and with a
ruinous one at the same time. Closing that interval to half an R takes 22
trades and calling a +0.3R edge significant takes 117, so at the observed
rate the record alone decides nothing for five to ten months.

The 131 clean setups are the wider evidence, and `scripts/replay.py` turns
them into outcomes against real five-minute bars. Every execution rule in it
is a place where a backtest can quietly pay itself: the entry is a resting
limit that fills at the level, the stop is a market order that eats a gap
open rather than the stop price, a bar holding both the stop and the target
is counted as the stop, and risk is the planned distance from level to stop
rather than the distance from the actual fill, so a favourable fill shows up
as return instead of vanishing into a smaller denominator. A setup whose
level is never touched is counted as no fill, not as a zero.

The replay only trades the session. The bot sends orders in regular hours
and its own `eod_force_close` runs at 15:58, so a replay that leaves a limit
resting until the last five-minute bar of the calendar day fills it in the
evening session, where the setup means nothing, and then exits at a price
nobody would have got. Both errors lean the same way. Setups timestamped
outside the window are reported as untradeable rather than silently dropped,
so the count stays visible.

The window's far edge is finer than it looks. Bars are stamped at their
start, so a cutoff of 15:58 still admits the 15:55 bar — which closes at
16:00, two minutes after the bot is already flat. That bar was paying the
replay twice: the end-of-day exit was taken at a price the account could
not have received, and a limit could fill inside it, opening a position
that never existed. Five-minute bars have no 15:58 price to offer, so the
last usable bar is the one starting 15:50 and closing 15:55 — the last
price observed before the flatten. It shortens every position and deletes
late fills, which is the direction to be wrong in.

Trailing is where a replay can be most generous to itself. The funded
account runs with the stop trailing, so a number measured without it
describes a different instrument. What decides whether the number with it
means anything is that the bot wakes every 300 seconds and reads one live
price — it never sees the bar. A move that touches the trigger between two
scans and retraces did not happen as far as it is concerned, and a replay
that checks the bar's high would trail on every one of those, converting
full losses into free breakevens. So trailing is evaluated at bar closes,
which are exactly the scan interval, and the R denominator stays the
planned risk — once the stop sits at the entry the live distance is zero,
which is the same `zero_risk` the bot itself hits, and the reason it
trails once rather than repeatedly.

The trigger and the destination are the bot's parameters, not the
replay's, and they are not verified here. They are declared as named
constants, run through a sensitivity grid, and kept out of the dollar
model: the headline and the projection still come from the run without
trailing, with the difference printed beside it. A constant that has not
been read out of `broker/ibkr.py` does not get to decide how many accounts
are opened, and if the grid disagrees about the sign of the lower bound,
that constant *is* the decision and nothing should be sized before it is
known.

Three things it reports rather than hides. A bar containing both levels is
unresolvable at five-minute resolution, so the run is repeated with the
opposite convention and both answers are printed; if they disagree in sign,
the backtest has not decided and says so. A gap that clears both the level
and the stop at once enters and exits at nearly the same price, which is a
real outcome but also the quiet way a backtest deletes a loss, so those are
counted and the result is re-shown with each one charged a full −1R. And the
confidence interval is clustered by trading day, because four trades riding
the same afternoon are not four observations; the narrower interval that
assumes independence is printed beside it, labelled as too narrow.

One check has to survive the fetch itself, and the first run failed it. IBKR no longer holds the June
2026 contract — it expired and was removed — so the whole window comes back
from September, while until the mid-June roll the bot was analysing June. The
two are not one price: carry separates them by a few points. A few points
sounds like nothing until it is divided by the stop. Two points against a
stop of 8.5 is a quarter of an R of systematic shift in one direction, and
the expectancy being measured is itself around 0.2R. So the gap against the
series the bot saw is reported per month rather than as one median over the
window, because a single median dilutes the pre-roll period with the
post-roll one, where both sources are the same contract and agree exactly —
and it is restated in R, since that is the unit the decision is made in.

The first real run came back at 60 points on ES and 279 on NQ for the second
half of May, against a typical stop of 20 — 3R and 14R of systematic shift in
one direction, with June and July at zero. That is the carry spread between
the June and September contracts, and it ruled out 82 of the 131 setups by
itself. Two things follow. IBKR does still serve an expired contract, but
only when the request says so, so the contract now carries `includeExpired`.
And the front month is picked by matching the bot's own series day by day
rather than by volume: volume answers which contract was genuinely in front,
while the question here is which contract the recorded levels were computed
from, and those differ whenever the feed rolls on its own schedule. The roll
is one event, so the choice must switch once, from near to far, and never
back; a choice that flip-flops has matched noise rather than a roll, and the
script says so and falls back to volume instead of stitching something it
cannot justify.

`includeExpired` turned out to be necessary but not sufficient: IBKR resolves
the June contract with it and then answers `HMDS query returned no data`. The
contract the levels were computed from is simply not retrievable. So the gap
is corrected rather than fetched. The bot's own hourly series *is* the June
contract for those days, so the difference is measured per day and subtracted,
leaving September's intraday path on June's scale. The offset applied is the
previous day's, never the current one, since today's would be read off closes
that had not happened at the moment of the fill; carry moves slowly enough
that yesterday's is a good estimate and carries no look-ahead at all. Days
that already match get an offset of zero, so June and July are untouched.
What the two contracts do not share is their intraday path, and that residual
is measured rather than assumed: the script reports what is left after the
correction, and a level adjustment leaves a tenth of a point where the
contracts differ by two thousandths of a percent.

Days with no reference series at all — a holiday, or a gap in the feed — used
to fall out of the stitch entirely and silently. The roll is monotone, so the
previous day's choice is the right answer for them, and the count of days
filled that way is printed.

The correction worked and is measured: ES went from 60 points to 0.50, NQ
from 279 to 2.50, and the gap against the series the bot saw fell from 0.030%
to 0.003%. What is left — 0.38 points on ES, 3.12 on NQ, about a tenth of an
R — is the difference between two contracts' intraday paths, which no level
adjustment can remove. That is the floor on how much the corrected month can
be trusted, and it is reported rather than assumed away. Since the results
file carries no mark saying whether a correction was applied, the check states
the magnitude and its consequence without claiming its cause.

It does not explain the gap scratches. The prediction was explicit — with the
contract fixed they should largely disappear — and it failed: thirteen of
seventy-three became fourteen of a hundred and eleven. Whatever they are, they
are not an artifact of the wrong contract. They are setups whose stop was
already breached at the moment they were recorded, which is what the first
reading said before the contract finding displaced it.

The replay is also split by month, because May is the corrected month and June
and July arrived as they were. If the conclusion flips between them, the
correction is carrying the result rather than the strategy.

What the measured expectancy is worth in money goes through
`scripts/apex_model.py` rather than through multiplication. Expectancy times
trades per day times 250 times the risk fraction produces figures like 900% a
year, and they are fiction: the account is destroyed long before, the payout
ladder is capped, and the trailing floor cuts in. The model already contains
all three, so the measured `avg_R` is fed into it as an input.

The engine is calibrated the way the lag scan was, against data whose answer
is known in advance. A driftless random walk with a 2R target and a 1R stop
must return zero, and a planted drift must come back as a long edge and a
short loss on the same series. Building that calibration surfaced two traps
in the synthetic data rather than in the engine, and both inflated the
result: bars whose highs and lows are noise pasted onto the extremes let
every wick fill recover to the close for free, worth 0.26R of imaginary
edge, and a setup stamped at a bar's open while its level was derived from
that bar's close lets the level see five minutes into the future. The
generator now builds each five-minute bar from five one-minute steps of a
continuous path and takes the level from the open. With both removed the
engine returns −0.02R to −0.09R across seeds, which is correct: slightly
below zero, because the end-of-day close truncates positions that had not
yet reached either level.

The first run against real bars caught three more, none of which the
synthetic calibration could have found. The clustered confidence interval
averaged within each day and took its width around the mean of the daily
means while printing the mean of the trades as the point estimate; with
uneven trades per day those are different quantities, and the run printed
+0.172R with an interval of [−0.061, +0.830] — an estimate sitting outside
the middle of its own interval. It is now a cluster-robust standard error
around the trade mean, which reduces exactly to sd/√n when each day holds one
trade. Sessions were calendar days, so limits rested into the evening and
unresolved positions closed at 23:55 rather than at the flatten time. And
`.values` on a timezone-aware series converts to UTC and drops the marker, so
the fill and exit times were written to the results file as bare UTC and
would read as local — four hours, silently; the same trap had already been
fixed on the input side, and a test now asserts it on the output too.

That calibration also caught a real look-ahead in the engine. On the bar
where the entry fills mid-bar, the bar's high may have been made before the
fill, so crediting a target hit there is crediting a peak the position was
never in. It now counts only when the bar's close is itself beyond the
target, which proves the level was reached afterwards. At a 1R target, where
the target sits close enough that many hits fall inside the fill bar, that
one rule moved the reported expectancy by 0.1R — against a decision
threshold of about 0.3R.

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
- `scripts/hypotheses.py` — a pre-registered research queue of 100 hypotheses across execution, trade management, setup quality, market regime, fleet structure, prop-firm mechanics and methodology. Each carries a mechanism, what data it needs, a prior and a cost, and is ranked by value of information (prior × effect ÷ cost) rather than by how promising it sounds. Pre-registration is the whole point: the same hypothesis is evidence when written down first and noise when found by searching for what improves the table.
- `scripts/dashboard.py` — runs every testable hypothesis and writes one self-contained local HTML page; no network, no server, and the trade data never leaves the machine. It shows each effect beside both the single-test noise floor and the multiple-testing threshold, because with 28 active testers on 111 trades a finding needs 0.34R to survive while the entire measured edge is 0.101R. Statistics that are a maximum over groups — by hour, weekday, symbol, grade — are marked descriptive and can never be called a finding.
- `scripts/test_dashboard.py` — 19 tests. The one that matters runs the whole dashboard over data built with no structure at all, across four seeds, and requires zero survivors. The first version failed it: four passed the correction, led by day-of-week at 0.882R, because a max-minus-min across k groups is itself a selection and grows with k at zero effect. A positive control plants a real effect so that silencing everything cannot pass.
- `scripts/diagnose_edge.py` — where the money actually goes, split by exit reason, with every candidate change printed beside the noise floor. Splitting one result by exit reason is not a search over alternatives and does not suffer selection bias; what you then do with it does. A candidate is adopted only if it has a mechanism you can state without looking at the table, beats the clustered standard error rather than merely being positive, and is validated forward. A candidate that passes only the second is the most expensive mistake available here, because it looks exactly like a finding.
- `scripts/test_diagnose_edge.py` — 7 tests, all on the refusal rather than the arithmetic: noise-sized improvements are named as noise, a missing noise floor never reads as a finding, and clustering widens the error rather than narrowing it.
- `scripts/paper_check.py` — whether the execution path is clean, which is the gate's actual stage 0→1 condition and had nothing implementing it. It leans on one invariant a single row can settle: a correct conversion scales entry, stop and target by the *same* ratio, so the bug that pins the entry to the market price while converting the other two correctly makes the three ratios diverge. A range check cannot see it, because every price involved is a real one. It deliberately prints no expectancy: paper fills on touch with no queue, no partial fills and no real slippage, so a number measured there is biased upward.
- `scripts/test_paper_check.py` — 30 tests, each building a row that looks entirely normal to the eye and fails only on the ratio, plus the rule that a row which cannot be compared counts as unchecked rather than as a pass. Seven of them exist because the first version of this checker mixed scales itself: with `exec_entry` empty it fell back to the signal level, compared a futures level against an ETF exit price, and flagged every profitable long and every losing short as a contradiction. It reported three real trades as corrupt that were merely unverifiable. Eight more cover the era cut at `FIX_LANDED`: a row written before the analysis-ordering fix carries `analysis_id = 0` for ever and cannot become clean, so counting it pinned the verdict at "not clean" permanently — five flawless trades would still have printed *do not buy*. The cut is dated, not typed: an orphan or a split ratio after it still blocks, and the empty range now says "unknown" instead of claiming every trade is linked.
- `scripts/pipeline.py` — one command that repairs, measures and reports: backup, the conversion-bug patch, the validator install, the bar fetch, the replay, and the gate's verdict. It touches exactly two things — `broker/proxy.py` and a copy of `integrity.py` — and never `strategy/`, risk parameters, `logger.py` or `ibkr.py`. The patch is derived from the AST rather than from text, and it refuses to write when the function has no live contract price in scope, because a fix that invents a variable turns a silent bug into a crash at order time.
- `scripts/test_pipeline.py` — 16 tests. Half hold the rule that a failed fetch never reaches the replay, since a replay on yesterday's bars looks exactly like a replay on today's. Half hold the opposite rule for the repair: a blocked file stays byte-for-byte identical, a quoted or demonstrated bug is not a bug, and `strategy/` is never touched.
- `scripts/sizing_grid.py` — what raising risk actually buys, across expectancy and risk size, with the death rate beside every cell. Doubling risk from 4% to 8% does not buy return; it lowers the expectancy that a 24.6% year demands from +0.300R to +0.211R, and raises accounts burned from 54 to 178. Getting the tax classification right is worth 7.2 percentage points — almost exactly what 4%→6% buys — and burns no accounts at all. Note which direction that runs: nothing is owned, nothing is sold, the account is simulated and the payment is contractual consideration for a result, so every fact argues against the 25% treatment. The model's 25% base case is the optimistic branch. Until an accountant says otherwise in writing, plan on 17.4% a year and treat 24.6% as the upside.
- `scripts/test_sizing_grid.py` — 5 tests holding the three claims that are easiest to lose: the percentage is invariant to account count, no risk size turns a negative edge positive, and an unreachable target is reported as unreachable rather than extrapolated.
- `references/schedule.md` — the two-week and monthly instructions in the brief, reconciled against the gate with dates. One is compatible and one is not, and the difference between them is $165 against $48,564 to learn the same fact.
- `scripts/plan_choice.py` — twenty 50K accounts against ten 150K, decomposed into the ladder-per-drawdown ratio, the contract-rounding asymmetry, and an equal-count control that reverses the headline. Answers conditionally, because the crossover sits inside the range the gate is still resolving.
- `scripts/test_plan_choice.py` — 9 tests, one of which exists solely to fail if the conditional answer is ever flattened into an unconditional one.
- `scripts/test_gate.py` — 25 tests on the decision logic, since the numbers are the decision. Six of them run real SQL against a real table, because the integrity check that catches a trade closed at its own entry price had been naming a column that does not exist: SQLite raised, the handler returned None, and `if n:` read that exactly like a clean result. A check that cannot run has to look different from a check that passed.
- `scripts/test_apex_model.py` — 21 tests on the model's mechanics: loss bounded by fees, withdrawals arriving only in whole ladders, the evaluation clock expiring an unreachable target, tax never touching a loss, and the withdrawal split. Deterministic, by driving the model to always-win and always-lose.
- `scripts/ladder.py` — trades needed per effect size, and the cost of each rung if the edge turns out not to exist.
- `scripts/horizon.py` — when compounding on extracted profit starts to matter, which inside eight years it does not. Not to be confused with `detect.py`: this one is about money already earned, that one about whether the edge exists.
- `scripts/detect.py` — how long before the question can be answered at all, in both directions: days until a given edge clears zero, and the smallest edge a given wait can resolve. Clustered by trading day, because a busy day is not an extra day, with a t-quantile rather than 1.96 since the cluster count is small. Two conclusions come out of it and neither is comfortable. An edge the size of the one measured (+0.101R) needs about 222 days with a trade in them — some 15 months of calendar trading, and that is the median case — to separate from zero, so if that is the truth this plan never gets its answer. And therefore the wait is not for *how big* the edge is but for *whether it is big enough* — an edge that has not shown itself in roughly three months of trading is already too small to justify the fleet, whatever it later turns out to be. That asymmetry is the only thing that bounds the waiting.
- `scripts/test_detect.py` — 10 tests, and they exist because this number drifted twice in opposite directions. It was first given as "39 days, about 1.8 months" — the count right, the conversion wrong — then "corrected" to 77 on a standard error recalled as 0.207R when the printed interval implies 0.145R, which doubled every row. The settled answer is the original 39, at 2.7 months rather than 1.8. So the tests pin three separate things: that the anchor reproduces the interval `replay.py` actually printed, which is the check that was missing and would have caught both drifts; that the anchor is 39; and that months come from days-with-a-trade rather than from 21. The rest hold that the error shrinks with the root of *days* and not of trades, that bigger edges resolve sooner, that the conservative case is never faster, and that the two directions round-trip.
- `scripts/claims.py` — recomputes every arithmetic claim in the write-up from scratch. Run it after editing any number; it caught a real error where two figures were quoted from different configurations.
- `scripts/proxy_fix.py` — correct futures-to-ETF level conversion with the invariant asserted on every call. Run it directly for a numeric before/after.
- `scripts/test_proxy_fix.py` — 21 tests; the first reproduces the collapse bug and proves the invariant catches it.
- `scripts/lag_scan.py` — the coarse pass: how far behind the market a recorded price sits, in whole days, against a real time offset instead of a free search. Locks its cohort and judges by the rise on both sides of the minimum. Hands off to `lag_refine.py`.
- `scripts/lag_refine.py` — the decisive one: refines the lag to the hour and rules on whether it is locked to a duration (a cache) or to a bar count (an index bug), by scanning both units over the same span.
- `scripts/test_lag_refine.py` — 15 tests. Both directions on planted data, a replica of the real 60-session/304-setup situation in each direction, proof that a shrinking cohort really can manufacture a minimum and that locking it removes one, and proof that a time-only reading would have misread a planted bar offset.
- `scripts/futures_era_check.py` — whether the lag survived into the futures era, using hourly bars from the feed itself, with the ETF era re-run first as a control on whether that source can serve as a witness at all.
- `scripts/test_futures_era_check.py` — 24 tests: planted lag found and clean data left clean across five seeds each, the call holding across four volatility regimes, the cohort lock, and the case that broke the first classifier, where a real lag in a quiet market shows only a modest error at zero offset.
- `scripts/futures_bars.py` — five-minute ES/NQ bars for the clean window from IBKR via dated contracts, since `ContFuture` refuses an end date. The roll is read from daily volume rather than guessed, and the stitched series is checked against the one the bot itself saw.
- `scripts/test_futures_bars.py` — 33 tests on the roll selection, the reference matching and the frame conversion, because a wrong roll slips a silent price jump into the middle of the window where nothing would reveal it. The one clean switch, the flip-flop, the backwards roll and the carry gap each have their own case.
- `scripts/replay.py` — the backtest: the clean setups executed against real bars with limit entries, gap-aware stops, end-of-day flat at the last price observable before the bot flattens, stop trailing sampled at the bot's 300-second scan rather than at the bar's extreme, costs in R, a target grid, and the measured expectancy fed into the fleet model instead of multiplied out.
- `scripts/test_replay.py` — 72 tests. Each execution rule against a bar built to break it, and the calibration: four seeds of a driftless random walk that must not yield an edge, the target-hit rate against its geometric odds, a planted drift recovered as a long edge and a short loss, and setups shifted half an hour to prove the result is tied to their timestamps.
- `scripts/drift_diagnostic.py` — locates the cause of recorded prices that don't match the market. Takes an optional directory argument.
- `scripts/test_drift_diagnostic.py` — 18 tests on which fault the gap implies, using the figures actually measured on planted data, so the thresholds can be tuned without silently breaking the distinction.
- `scripts/streak_check.py` — losing-run tail under each clustering setting, to confirm a stress test is actually stressing something.

`references/apex-rules.md` holds the rule values the model is built on, and the list of what to confirm with the firm directly before paying for anything. Rules change; the file names its date. It also carries the gap nothing else in this skill crosses: the bot trades through IBKR, an Apex account is provisioned on Rithmic or Tradovate, and **no order path between them exists.** Closing it means either a second order path or a bridge mirroring fills, and either way a translation from ETF scale to MES — the same conversion that produced the collapse bug, run unwatched across twenty accounts. It does not block one evaluation, where the exposure is $125 and the purchase is itself the cheapest way to learn what the firm's platform accepts. It blocks the third account. And it bounds what the paper run proves: the edge is measured in R against ES bars and carries across platforms unchanged, but `exec_entry`, fill quality and the conversion are being verified on an order path the funded accounts will never use.

`references/verification-letters.md` is that list already written as two letters to send — one to the firm, one to an accountant. Both questions are answered by other people rather than by analysis, and left as headings they stay open for months. The firm's letter leads with automated order routing because it is the one risk in the plan not bounded by fees: if the order path is not permitted, accounts close and earned payouts can be voided. The accountant's letter carries the facts that decide whether this is business income or a capital gain, which over eight years is worth more than most of the trading decisions.

## Voice

Numbers with their sign and their unit. The uncomfortable number in the same register as the good one. When a quantity is unknown, say unknown — not "probably fine," not a fabricated estimate. State plainly which conclusions are solid, which are order-of-magnitude, and which are still open.
