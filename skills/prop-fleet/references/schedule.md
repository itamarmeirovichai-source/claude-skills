# The schedule, against the gate

Two instructions sit in the brief that do not agree with each other, and
nobody has written down which one gives way. This file does that, with dates.

- **"Buy the first account in two weeks."**
- **"Buy another account every month until there are 10 to 20."**

The first is compatible with the gate. The second is not, and not by a
small margin.

All dates below are measured from **22 September 2026**.

## Why the first one works

Stage 1 of the ladder permits one account, and the only thing standing
between stage 0 and stage 1 is *execution verified clean on a simulated
run* — not a trade count and not an expectancy. That is engineering work,
and it is nearly done:

| Blocking before a single dollar is spent | State |
| --- | --- |
| `broker/proxy.py` — the ratio-cancellation bug | **fixed**; `doctor.py` reports the conversion clean |
| `bot/integrity.py` — installed on the write path | **installed and wired**, marking not blocking |
| The replay run against real bars | **run**: +0.101R, clustered CI [−0.197, +0.398] on 28 days |
| The trailing constants read out of `broker/ibkr.py` | **read**: 1.0R → breakeven, 1.5R → +0.5R (lines 1608/1611/1616) |
| `exec_entry` written on a real fill | **the one that is left** — no live fill has passed through the fixed path yet |

The first four are closed. The fifth is what the paper run exists to
answer, and it is the whole of the Oct 3 condition: **at least five
comparable trades with `exec_entry` populated and zero integrity flags**,
as `paper_check.py` counts them. Below that the account is bought to find
out whether the recording works, which is a question the paper run answers
for nothing.

None of these needs a funded account to fix. All of them have to be true
before one is bought, because an account bought on top of a live
conversion bug is not an experiment — every order goes out at market and
the record it produces cannot be used as evidence for anything.

**Target: one 50K evaluation by 3 October 2026. $40 evaluation, $85
activation on a pass — $125 all in.** That is the entire exposure at this
stage, and it is deliberately the price of a rounding error.

## Why the second one does not work

The monthly instruction buys accounts on a calendar. The gate buys them on
evidence. The gap between those two is not a matter of temperament — it is
arithmetic, and it comes out like this.

The clean window opens 18 May 2026 and spans **41 elapsed trading days**,
which produced 131 setups: **3.2 setups a day**. (41 is the measured span;
it implies an end around mid-July, consistent with July contributing 25 of
the 111 filled trades. The span is the number that matters here, not the
closing date.) The replay filled 111,
an 85% rate, but it fills a limit the moment price touches it, with no queue,
so live will be lower. At 50% to 70% that is **1.6 to 2.2 trades a day**, and
each stage lands here, counting from 5 October:

| Stage | Accounts | Trades needed | Earliest | Latest |
| --- | --- | --- | --- | --- |
| 1 | 1 | — | 3 Oct 2026 | 3 Oct 2026 |
| 2 | 3 | 100 | 8 Dec 2026 | 5 Jan 2027 |
| 3 | 10 | 250 | 17 Mar 2027 | 20 May 2027 |
| 4 | 20 | 900 | 11 May 2028 | Jan 2029 |

**Two day-counts live in this analysis and they are not interchangeable.**
The replay reports 28, and that is the number of days on which a filled trade
occurred — the cluster count that widens the confidence interval. The window
spans 41, and that is elapsed trading days. Rates for a *schedule* take the
elapsed count, because a day with no setup still costs a day; rates for an
*interval* take the cluster count, because a day with no trade carries no
information. An earlier version of this table divided 131 setups by the 28,
got 4.7 a day, and pulled stage 4 forward by nine months. `claims.py` is what
caught it, which is the entire reason that file exists.

The trade count is a necessary condition and not the gate. Each stage also
requires a positive lower bound, and the next section shows that at the edge
size actually measured, no trade count in this table produces one.

And every one of those dates assumes the edge is real *and* survives each
gate on the way. The dates are not a forecast. They are the fastest the
evidence could possibly arrive if everything goes right, which is the
least likely of the available outcomes.

## How long until any of it can be decided

This number drifted twice, in opposite directions, and it is worth saying
exactly how because the second drift was the attempt to fix the first.

It was first said that **+0.250R becomes provable in 39 trading days, about
1.8 months**. The count was right; the conversion was not. Then it was
"corrected" to **77 days**, on a standard error of 0.207R — and the reason
that happened is worth more than the number.

**0.207R is not a misremembering. It is what two of these scripts print.**
`diagnose_edge.py` and `dashboard.py` compute the clustered error as the
spread of day means over the root of their count; `replay.py` computes a
cluster-robust error around the trade mean. On the same 111 trades the first
pair returns 0.207R and the second 0.145R — a disagreement of 1.43×, sitting
in plain sight in the output of a single pipeline run. The horizon was
anchored on the wrong one of the two, and every row doubled.

Which one is right was settled by simulation rather than by argument. Against
a known true standard error, on 111 trades over 28 unequal days with a real
day-level effect, the cluster-robust estimator comes back at 0.99× the truth
and the day-mean estimator at 1.07×. The quantity every downstream number
uses is the mean *per trade*, and the robust error is the one that belongs to
it; the day-mean version is the error of a different estimator, equal-weighting
a one-trade day against an eight-trade day.

So the settled figure is **39 days with a trade in them, which is 2.7 calendar
months.** `scripts/detect.py` derives the error from the interval `replay.py`
prints rather than storing a scalar, and a test asserts the anchor reproduces
that interval.

Two cautions, both real. The simulation reproduces a 1.08–1.13× gap between
the estimators; his data shows 1.43×, which size inequality alone does not
explain — a few thin days with extreme means are moving the day-mean figure,
and that is worth looking at directly. And a cluster-robust error on only 28
clusters is known to run narrow, which is why the t(k−1) quantile is used
rather than 1.96. **39 days is the honest estimate, not a floor to plan
against.** Until `diagnose_edge.py` and `dashboard.py` are reconciled with
`replay.py`, treat the horizon as 39 days with a wide margin rather than a
settled constant.

The mechanism is that the standard error is clustered by trading day, because
trades opened the same day share a regime. It shrinks with the square root of
the number of *days*, not of trades: a busy day is not an extra day. Worth
noting how small that correction actually is here — 0.145R against 0.138R for
111 independent trades, 5% wider. The clustering is real and it is not what
makes the wait long. The unit is.

| True edge | Days with a trade, until the lower bound clears zero | Calendar months |
| --- | --- | --- |
| +0.101R (what was measured) | 222 | 15.5 |
| +0.150R | 103 | 7.2 |
| +0.200R | 59 | 4.1 |
| **+0.250R (the 20%/yr target)** | **39** | **2.7** |
| +0.300R | 28 | 2.0 |
| +0.400R | 17 | 1.2 |

The middle column counts *days on which a trade closed*, because that is what
the standard error shrinks in. Turning it into calendar time goes through the
same ratio as the schedule table above: 28 such days per 41 elapsed trading
days, so a month supplies about 14, not 21. Dividing by 21 instead — which both
earlier versions of this table did — shortens every row by a third.

Those are median cases: they assume the observed mean lands exactly on the
true edge, which is a coin flip. To be reasonably sure rather than
half-sure, roughly double them.

Two things follow, and neither depends on which row you prefer.

**An edge the size of the one measured is not decidable on any horizon
that matters.** If +0.101R is the truth, the answer arrives after about
15 months of calendar trading — and that is the median case, so call it
two to three years to be reasonably sure. By then the question has
answered itself in other ways.

**So the wait is not for "how big is the edge". It is for "is it big
enough".** An edge that has not shown itself in roughly three months of
trading is already too small to justify the fleet, whatever it eventually
turns out to be. That asymmetry is the only reason the waiting is bounded.

## The measured edge is one month, not a run rate

The +0.101R is not a small edge repeating across the sample. Broken up:

| Month | Trades | Mean | Contribution |
| --- | --- | --- | --- |
| 2026-05 | 44 | +0.049R | +2.2R (19%) |
| **2026-06** | **42** | **+0.243R** | **+10.2R (91%)** |
| 2026-07 | 25 | −0.046R | −1.2R (−10%) |

Drop June and +0.101R becomes **+0.015R** on 69 trades. July is negative.
One good month out of three is not a track record; it is a sample of one,
and a sample of one neither establishes an edge nor rules it out.
`diagnose_edge.py` now prints this split on every run so it cannot be
read past again.

## The blocker that was invisible until the bot ran

The paper run produced zero trades on its first full session, and the reason
is one config line rather than anything about the strategy.

`config.yaml` carries `account_size: 220`, described as mirroring the real
IBKR account. `risk_manager.py` derives the budget as
`account_size × max_risk_per_trade_pct / 100`, which at 1.0% is **$2.20 per
trade** — and $1.10 on a Grade B, which the code caps at half size. Against an
ES stop of 23.5 points at a multiplier of 50, and against an ETF proxy at any
sane stop distance, that rounds to zero. Every signal that survives every
filter dies in the last division.

Tuesday 22 September, the full funnel from the log: 77 scans, 33 analyses per
instrument, grades reaching **A+ and A** with sweep, BOS and entry all
confirmed, 24 signals passing the AI gate as tradeable — and then **14 blocked
with "Position size too small for $1 risk"**, and zero approved. The strategy
found setups. The account size deleted them.

It also explains the record going quiet after 13 July with nothing apparently
broken: the bot never stopped working, it just stopped being able to open
anything.

**What this means for the gate.** The paper run cannot produce a single
comparable trade — cannot populate `exec_entry`, cannot verify the conversion,
cannot count toward the five the Oct 3 purchase is conditional on — until the
sizing reflects the account actually being traded. The condition is unchanged;
it is simply unreachable in the present configuration.

**The arithmetic, for whoever decides.** At 1.0% per trade the mapping is
direct: `account_size` of **10,000 gives $100**, which is 4% of a 50K account's
$2,500 drawdown and therefore the exact regime this plan is built on; 25,000
gives $250, the evaluation's 10%. (An earlier version of this note said 22,000,
inferred from the log's rounded "$1" rather than from the formula. The code is
`account_size × pct / 100`, and reading it beats inferring from a printout.)

**The number feeds four things, not one**, which is why it is not a one-line
change to make casually. `config_validator.py` says so outright — "the
denominator for BOTH position sizing AND the daily-loss". At 10,000: risk per
trade $2.20 → $100, daily loss limit $2.20 → $100, the 8% strategy-drawdown
kill switch $17.60 → $800, and the equity cap on share count ~3 → ~158. All
four land in sensible places — $800 is 32% of an Apex 50K drawdown, so the kill
switch still fires well before the account dies — and the validator's sane
range is 50 to 100,000, so 10,000 sits inside it.

**A separate constraint the same file revealed.** `max_daily_trades: 1`, set
for T+1 settlement in cash stock mode. The replay measured about four trades a
day; the paper run is capped at one. Five comparable trades is therefore five
trading days, which still clears the Oct 3 condition — but the 100 trades that
gate stage 2 would be 100 trading days on this path, not the 45 to 63 in the
table above. The cap is specific to IBKR stock mode; Apex futures have no T+1,
so it does not move the funded-account schedule.

Two things have to be said alongside it. This is a position-sizing parameter,
and those do not get changed on anybody's initiative but the owner's. And at
$220 the strategy cannot run at all on any measurement — that was always true
and merely invisible, so if the real IBKR account is ever armed, this value
has to go back.

The edge measurement is in R and is scale-free, so none of this biases the
number. It only decides whether a trade exists to measure.

## The gap that stage 2 runs into

Stage 1 can be bought on the evidence above. Stage 2 cannot, and not because of
the statistics.

The bot places orders at IBKR. An Apex account is provisioned on the firm's own
platform — Rithmic or Tradovate — and **no order path from one to the other
exists today.** Building it means either a second order path in the bot or a
bridge that mirrors IBKR fills into the Apex accounts, and whichever it is also
has to translate instrument and size, because the master is on ETF scale and the
funded account trades MES or ES. That translation is the same one that produced
the proxy bug, where the ratio collapsed and every order went out at market.

This does not block buying one evaluation: the exposure there is $125, and an
evaluation is the cheapest way to discover what the firm's platform actually
accepts. It blocks the third account, which is the point where one unverified
conversion becomes three and then twenty.

It also bounds what the paper run proves. The edge measurement is in R against
ES bars, so it carries across platforms unchanged. Execution does not —
`exec_entry`, fill quality and the conversion itself are being verified on an
order path the funded accounts will never use. The Oct 3 condition is about
whether the record can be trusted; it was never a claim about the bridge.

Full statement in `apex-rules.md`, and the question to the firm is item 2 of the
first letter in `verification-letters.md`.

## What the disagreement is actually about

It is not about speed. Both plans reach twenty accounts inside the eight
years. The entire difference shows up in the branch where there is no
edge, and there it is the whole story:

- **Monthly, on the calendar.** Twenty accounts are running long before
  the measurement could have said anything. Twenty 50K accounts at an
  expectancy of exactly zero cost **$48,564** over the horizon; at
  −0.10R, which is inside the current interval, **$114,725**. Ten 150K
  accounts cost **$99,315** and **$140,110** at the same two points.
- **On the gate.** The lower bound never clears stage 1, so the
  measurement stops at one account and the spend is the evaluation fees
  incurred while measuring: **$40** for the evaluation, **$85** on
  activation, and **$40** for one re-buy if the account is destroyed
  during the 100 trades — **$165**, and $125 if it is not.

That is the trade: about **$165 against about $49,000** to learn the same
fact, and against $115,000 if the expectancy is negative rather than
merely absent. The monthly cadence is not faster at making money. It is
faster at spending it, and only in the branch where there is nothing to
make.

The $165 figure assumes exactly one re-buy. Two re-buys make it $205. The
point does not depend on the precision — two orders of magnitude of
separation survives any reasonable count.

## What the schedule is, then

1. **Now → 3 Oct 2026.** The code work is done: `proxy.py` fixed,
   `integrity.py` wired, trailing constants read, replay run. What remains
   is the paper run, which is already scheduled and unattended — the bot
   fires at 9:20 each trading day, IBC brings the Gateway back after its
   nightly restart, and the daily report lands at 16:05. Send the two
   letters in `verification-letters.md` — the Apex one covers the only
   unbounded risk in the whole plan, and it has to be answered before money
   moves, not after.
2. **3 Oct 2026, conditional.** One 50K evaluation, $125, not two — and
   only if `paper_check.py` shows at least five comparable trades with
   `exec_entry` populated and zero integrity flags. If it does not, the
   purchase waits; the condition is about whether the record can be
   trusted, and it is not negotiable by a date.
3. **Then nothing on the calendar.** The next purchase is triggered by
   `gate.py` returning stage 2, and by nothing else — not by a good month,
   not by the date, and not by the feeling that the pace is too slow. Stage 2
   has a second condition that is not statistical: an order path to the firm's
   platform that has been built and watched place real orders correctly. See
   the section above; it is engineering, it has not started, and the time to
   start it is while the measurement is accumulating.
4. **Run `gate.py` weekly.** It moves exposure down as readily as up, and
   the downward direction is the one that will be argued with.

## The one thing that would change this

A measured expectancy whose *lower bound* clears +0.10R would pull every
date in and would also reopen the 50K-versus-150K question, since the
crossover between the two plans sits between +0.08R and +0.10R (see
`scripts/plan_choice.py`). Nothing else changes the schedule: not a good
week, not a run of winners, and not the fact that the calendar said a
month had passed.

Today the lower bound is negative. The schedule above is what that permits.
