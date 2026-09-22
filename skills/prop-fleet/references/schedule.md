# The schedule, against the gate

Two instructions sit in the brief that do not agree with each other, and
nobody has written down which one gives way. This file does that, with dates.

- **"Buy the first account in two weeks."**
- **"Buy another account every month until there are 10 to 20."**

The first is compatible with the gate. The second is not, and not by a
small margin.

All dates below are measured from **19 September 2026**.

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

The clean window produced 131 setups over 28 trading days: **4.7 setups a
day**. The replay filled 111 of them, an 85% rate — but the replay fills a
limit the moment price touches it, with no queue, so live will be lower.
Call it 2.5 to 4.0 trades a day, and each stage lands here, counting from
5 October:

| Stage | Accounts | Trades needed | Earliest | Latest |
| --- | --- | --- | --- | --- |
| 1 | 1 | — | 3 Oct 2026 | 3 Oct 2026 |
| 2 | 3 | 100 | 9 Nov 2026 | 30 Nov 2026 |
| 3 | 10 | 250 | 30 Dec 2026 | 22 Feb 2027 |
| 4 | 20 | 900 | 16 Aug 2027 | 21 Feb 2028 |

Those dates are sooner than the previous version of this table, because
the setup rate was measured rather than assumed. **That is not good news
and it is not progress.** The trade count is a necessary condition, not
the gate: each stage also requires a positive lower bound, and the next
section shows that at the edge size actually measured, no trade count in
this table produces one.

And every one of those dates assumes the edge is real *and* survives each
gate on the way. The dates are not a forecast. They are the fastest the
evidence could possibly arrive if everything goes right, which is the
least likely of the available outcomes.

## How long until any of it can be decided

A number in this plan was wrong and it was wrong in the direction that
flatters it. It had been said that **+0.250R becomes provable in 39
trading days**. The correct figure, computed rather than recalled, is
**77** — and it is now in `scripts/detect.py` with tests, so it cannot
drift again.

The mechanism is that the standard error is clustered by trading day,
because trades opened the same day share a regime and are not independent.
It shrinks with the square root of the number of *days*, not of trades. A
busy day is not an extra day.

| True edge | Days until the lower bound clears zero | Months |
| --- | --- | --- |
| +0.101R (what was measured) | 452 | 21.5 |
| +0.150R | 205 | 9.8 |
| +0.200R | 118 | 5.6 |
| **+0.250R (the 20%/yr target)** | **77** | **3.7** |
| +0.300R | 54 | 2.6 |
| +0.400R | 32 | 1.5 |

Those are median cases: they assume the observed mean lands exactly on the
true edge, which is a coin flip. To be reasonably sure rather than
half-sure, roughly double them.

Two things follow, and neither depends on which row you prefer.

**An edge the size of the one measured is not decidable on any horizon
that matters.** If +0.101R is the truth, the answer arrives in about two
years of trading — by which point the question has answered itself in
other ways.

**So the wait is not for "how big is the edge". It is for "is it big
enough".** An edge that has not shown itself in roughly four months is
already too small to justify the fleet, whatever it eventually turns out
to be. That asymmetry is the only reason the waiting is bounded.

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
