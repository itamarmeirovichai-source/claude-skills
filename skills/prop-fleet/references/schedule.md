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
| `broker/proxy.py` — the ratio-cancellation bug | **still live in his repo** |
| `bot/integrity.py` — installed on the write path | **not installed** |
| The replay run against real bars | waiting on IB Gateway on port 4002 |
| The trailing constants read out of `broker/ibkr.py` | unread |

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

The clean window produced 131 setups over 41 trading days: **3.2 setups a
day**. Not every setup fills; the replay reports the rate. At a 50–70%
fill rate that is 1.6 to 2.2 trades a day, which puts each stage here:

| Stage | Accounts | Trades needed | Earliest | Latest |
| --- | --- | --- | --- | --- |
| 1 | 1 | — | 3 Oct 2026 | 3 Oct 2026 |
| 2 | 3 | 100 | 21 Nov 2026 | 19 Dec 2026 |
| 3 | 10 | 250 | 27 Feb 2027 | 5 May 2027 |
| 4 | 20 | 900 | 25 Apr 2028 | 12 Dec 2028 |

So twenty accounts is **19 to 27 months** of trading away, not twenty
months of buying. Ten accounts is five to seven months away, not ten.

And every one of those dates assumes the edge is real *and* survives each
gate on the way. The dates are not a forecast. They are the fastest the
evidence could possibly arrive if everything goes right, which is the
least likely of the available outcomes.

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

1. **Now → 3 Oct 2026.** Fix `proxy.py`, install `integrity.py`, read the
   trailing constants, run the replay on real bars. Send the two letters
   in `verification-letters.md` — the Apex one covers the only unbounded
   risk in the whole plan, and it has to be answered before money moves,
   not after.
2. **3 Oct 2026.** One 50K evaluation. $125. Not two.
3. **Then nothing on the calendar.** The next purchase is triggered by
   `gate.py` returning stage 2, and by nothing else — not by a good month,
   not by the date, and not by the feeling that the pace is too slow.
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
