# Model output

From `scripts/apex_model.py`. Assumptions: 3 trades/day, 250 trading days/year,
1:2 reward-to-risk, MES micros, $1.30 commission per contract round turn, 0.25
points of slippage on stopped exits, evaluation sized at 10% of drawdown, funded
account at 4%, one new account opened per month, 25% tax, and full copy-trading
correlation (every account takes the same trades).

Every figure below is a Monte Carlo mean. Re-running reproduces them to within
about 1%; rows near zero expectancy have much larger relative noise because the
absolute number is small (the 0.00R row moves by a few hundred dollars, which is
10% of itself). Read them to two significant figures, not to the dollar. The
model was extended after these tables were produced — adding the regime option
changed which random numbers each draw consumes — and the tables were re-checked
against the current code: 0.3% to 0.8% apart, which is the noise, not a change in
behaviour.

## Net after tax, steady state (years 5–8)

| Expectancy | 10 × 50K | 20 × 50K | 10 × 150K | 20 × 150K |
| --- | --- | --- | --- | --- |
| −0.10R | −$7,880 | −$15,759 | −$18,274 | −$36,547 |
| 0.00R | −$2,448 | −$4,895 | −$10,806 | −$21,612 |
| +0.10R | $28,683 | $57,438 | $33,094 | $66,102 |
| +0.20R | $76,368 | $152,684 | $110,348 | $220,653 |
| +0.30R | $123,227 | $246,498 | $187,152 | $374,055 |
| +0.35R | $146,269 | $292,355 | $223,608 | $447,296 |

Expectancy is the whole business. Everything else is second order.

## Eight years at +0.30R, 20 × 50K

Withdrawal plan: from year 5, 25% of net into a private portfolio compounding at
7%, 25% into business and real estate compounding at 12%, the rest held in reserve.

| Year | Gross | Fees | Net after tax | Reserve | Portfolio | Business | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | $73,002 | $2,076 | $53,194 | $53,194 | — | — | $53,194 |
| 2 | $268,818 | $3,674 | $198,858 | $252,052 | — | — | $252,052 |
| 3 | $333,844 | $3,774 | $247,552 | $499,605 | — | — | $499,605 |
| 4 | $330,880 | $3,726 | $245,366 | $744,970 | — | — | $744,970 |
| 5 | $329,003 | $3,688 | $243,986 | $866,964 | $60,997 | $60,997 | $988,957 |
| 6 | $327,402 | $3,672 | $242,797 | $988,362 | $125,966 | $129,015 | $1,243,343 |
| 7 | $333,690 | $3,754 | $247,452 | $1,112,088 | $196,646 | $206,360 | $1,515,095 |
| 8 | $332,772 | $3,736 | $246,777 | $1,235,477 | $272,106 | $292,818 | **$1,800,401** |

Tenth percentile $1,616,006, ninetieth $1,987,618. Median 284 evaluations bought
and 54 accounts lost to drawdown across the eight years.

## Evaluation sizing matters more than it looks

20 × 50K, +0.30R, funded account fixed at 4% of drawdown:

| Evaluation size | Net per year | Evaluations bought over 8 years |
| --- | --- | --- |
| 4% | $155,845 | 758 |
| 8% | $236,380 | 317 |
| 10% | ~$250,000 | ~290 |
| 12% | $251,766 | 288 |
| 16% | $257,886 | 319 |

Sizing the evaluation like the funded account costs about $95,000 a year and buys
2.6× as many evaluations, because most of them expire before reaching the target
rather than failing on it. Past about 12% the gain flattens and the burn rises.

## Per-slot throughput by size, 50K

| Expectancy | 2% of DD | 4% | 6% | 8% | 12% |
| --- | --- | --- | --- | --- | --- |
| +0.20R | $4,232 | $8,961 | $11,470 | $14,573 | $19,127 |
| +0.30R | $6,376 | $14,705 | $19,911 | $24,648 | $29,878 |
| +0.35R | $7,381 | $17,485 | $23,920 | $29,075 | $34,369 |

Raw throughput keeps rising with size because the downside per account is capped
at the fee while the upside is capped at the ladder. **Do not read this as a
reason to size up.** It is only true when the expectancy is known to be positive,
and at 12% of drawdown between 37% and 62% of accounts die without a single
payout. The 4% figure is the recommendation; these columns exist to show what is
being given up and why it is worth giving up.

## What the goal costs, in R

The brief asks for more than 20% a year. That is not a vague aspiration once
it is priced: it is a single measurable threshold on expectancy, and every
other decision follows from whether the strategy clears it.

Net after tax in steady state, 20 × 50K, as a percentage of nominal account
capital — solved for the expectancy that returns exactly 20%:

| Risk, as % of drawdown | At 25% tax | At 47% tax |
| --- | --- | --- |
| 4% (the recommendation) | **+0.250R** | +0.340R |
| 6% | +0.207R | +0.270R |
| 8% | +0.182R | +0.234R |

Measured on the 131 clean setups against real bars: **+0.101R**, with a
day-clustered interval of [−0.184R, +0.385R].

Two things follow. No sizing dial closes that gap — even 8% of drawdown,
which triples the rate at which accounts are destroyed, still demands
+0.182R against +0.101R measured, and +0.234R if the income is classified as
business income. And the goal is nevertheless still live, because +0.250R
sits inside the measured interval. It is unproven, not refuted.

## Risk before and after the floor locks

The trailing floor follows the peak down until the peak reaches the safety
net, after which it pins at start + $100 permanently. So only the first
$2,600 is genuinely dangerous, and an account before that point and one
after it are not the same bet. The model takes `risk_pct_locked` for the
second state.

20 × 50K, evaluations at 10%, net per year in steady state:

| Before lock | After lock | At +0.101R | At +0.250R | Accounts burned at +0.250R |
| --- | --- | --- | --- | --- |
| 2% | 4% | 4.3% | 17.0% | 57 |
| 4% | 4% | **5.9%** | 20.0% | 72 |
| 4% | 6% | 5.8% | 24.1% | 118 |
| 4% | 8% | 6.3% | **27.0%** | 168 |

Two things follow, and the first corrects an intuition that sounds right.

**Cutting risk before the lock does not help.** It reads as prudent — the
dangerous zone deserves caution — but 2% before the lock returns 4.3% a
year against 5.9% at a flat 4%, at both expectancies tested. Undersizing
through the dangerous stretch means taking longer to clear it, and the
floor is trailing the whole time. The way past a trailing floor is
through it.

**Raising risk after the lock is worth a great deal, but only if the edge
is real.** At +0.250R it takes 20.0% to 27.0%, seven percentage points for
one parameter. At the measured +0.101R the same change is worth 0.4 points
and nearly doubles accounts destroyed, from 305 to 564.

So this is not a change whose value is independent of the expectancy, and
it does not belong on a list of things safe to adopt before the
measurement exists. It belongs on the list of things to adopt the moment
the lower bound clears, and it is worth having measured in advance so that
the decision is ready rather than deliberated.

## The classification decides the target, not just the take-home

The model's tax parameter had only ever been run at 25% and 47%. If the
income is business income, National Insurance and health levy sit on top
of the marginal rate, and that was never modelled at all. Solved for the
expectancy that returns 20% a year, 20 × 50K at 4% of drawdown:

| Effective rate | What it is | Expectancy required |
| --- | --- | --- |
| 25% | capital gain | +0.249R |
| 47% | business income, top marginal | +0.339R |
| 53% | business income plus National Insurance* | +0.379R |
| 60% | adverse case* | +0.441R |

\* The National Insurance rates and their ceiling are not verified here.
That is a question for an accountant, and it is question 2 in the letter.

Measured: **+0.101R**. So the classification does not merely change the
take-home — it moves the target between +0.249R and +0.441R, a range wider
than the entire measured edge. Every fact in the letter argues for the
business-income side: nothing is owned, nothing is sold, the account is
simulated, the payment is contractual consideration for a result, and the
activity is daily and automated.

One item the plan had never priced at all: **VAT**. Business income from a
US company is export of services to a foreign resident, which can qualify
for zero-rated VAT under section 30(a)(5) subject to conditions. Getting
that wrong is 18% of gross receipts, which is larger than any trading
decision in this document.

Until an accountant answers in writing, reserve at the higher rate from
every payout on the day it arrives. Over-reserving is an inconvenience;
under-reserving for two years while the plan compounds is not.

## How long until the lower bound decides

The latest run prints +0.101R with a clustered interval of [−0.197, +0.398]
over 28 day-clusters — a half-width of 0.2975R, which at t(27) is a standard
error of **0.1450R**. It narrows as the square root of the cluster count.

| If the true expectancy is | Days with a trade, to a positive lower bound | Calendar months |
| --- | --- | --- |
| +0.101R | 222 | 15.5 |
| +0.200R | 59 | 4.1 |
| +0.250R | 39 | 2.7 |
| +0.300R | 28 | 2.0 |
| +0.500R | 12 | 0.8 |

Both columns changed from the previous version of this table and neither
conclusion did. The middle column now uses t(k−1) rather than 1.96, which
lengthens it slightly at small cluster counts. The months column now divides
by days-with-a-trade rather than by 21: the window produced 111 fills over 41
elapsed trading days — 2.71 a day — but they landed on only 28 of those days,
so a calendar month supplies about 14 clusters, not 21. Dividing by 21 made
every horizon look a third shorter than it is.

This is the reason the evaluation is worth buying before the question is
settled rather than after. If the strategy really does clear the threshold the
goal requires, live trading proves it in under three months — and if it does
not, the same three months cost $165 to find out.

## Tax

20 × 50K at +0.30R, in the same configuration with only the rate changed:

| | 25% | 47% | Difference |
| --- | --- | --- | --- |
| Net per year | $246,311 | $174,060 | $72,251 |
| Over 8 years | $1,728,928 | $1,221,774 | **$507,154** |

Which way this is likely to fall matters more than the spread. Nothing is owned,
nothing is sold, the account is simulated, and the payment is contractual
consideration for a result produced by a program trading daily — every one of
those facts argues against capital-gains treatment. So 25% is the optimistic
branch of this table, not the neutral one, and the headline 24.6% a year is
really 17.4% until an accountant says otherwise in writing.

An earlier draft reported $642,993 here. That paired a 47% figure from a run
with the evaluation sized at 4% against a 25% figure from a run at 10%, which
overstated the gap by about $136,000. `scripts/claims.py` now recomputes every
arithmetic claim in the write-up and caught it.

## Clustering stress test

The model draws trades independently through time. A real methodology is regime
dependent — it works in trending conditions and bleeds in chop — so losses arrive
in runs, and a run is far worse against a *trailing* floor than the same losses
scattered, because the floor has already ratcheted up behind the peak. This was
worth testing before trusting the sizing.

`scripts/streak_check.py` first confirms the regime chain produces real
clustering. The mean losing run barely moves; the tail is what changes:

| Regime | Mean run | p99.9 | Longest | Runs ≥ 12 |
| --- | --- | --- | --- | --- |
| i.i.d. | 2.31 | 13 | 24 | 0.19% |
| strong | 2.44 | 16 | 32 | 0.63% |
| severe | 2.54 | 19 | 36 | 1.08% |
| regime-flip | 3.36 | 36 | 73 | **6.05%** |

Then the fleet is run on a **fixed 8-year horizon** — not a per-slot rate, which
would flatter a fast death — with expectancy held at +0.30R, so only the shape of
the sequence differs:

| Scenario | 8y net, 4% | p10, 4% | Accounts burned |
| --- | --- | --- | --- |
| i.i.d. | $1,733,772 | $1,583,957 | 52 |
| mild | $1,736,149 | $1,571,388 | 66 |
| strong | $1,729,301 | $1,455,874 | 186 |
| severe | $1,878,442 | $1,416,611 | 692 |
| extreme | $2,278,883 | $1,534,552 | 1,589 |
| regime-flip | $3,026,960 | $1,648,280 | 2,886 |

**The 4% recommendation survives.** The mean is flat through strong clustering,
and the real cost shows up at the tenth percentile: $1.58M down to $1.46M, about
8%. That is the honest price of clustering and it is modest.

Read the bottom rows carefully and do **not** conclude that clustering is good.
The mean rises there because the payoff is asymmetric — loss capped at the fee,
gain capped at the ladder — so dispersion is worth something, and the model will
replace a dead account instantly and for free. Reality will not. At regime-flip,
2,886 accounts over eight years is roughly one death per day across twenty slots:
operationally absurd, and an invitation for the firm to look closely at the
account. The model has no ceiling on how fast evaluations can be bought and
re-qualified, so those rows are an artifact of that missing constraint, not a
finding.

The usable conclusion is the burn column. At 6% of drawdown the burn count is
roughly double at every clustering level for about 30% more money. Clustering
therefore strengthens the case for the **smaller** size — not on dollars, on
operational load and on staying unremarkable to the firm.

## Compounding barely matters inside eight years

The year-8 wealth figure rests on two assumed rates — 7% on a private portfolio,
12% on business and real estate. Worth knowing how much it actually depends on
them:

| Returns | Wealth at year 8 |
| --- | --- |
| zero | $1,728,928 |
| 5% / 8% | $1,779,346 |
| 7% / 12% | $1,804,247 |
| 9% / 15% | $1,825,703 |

**Every return assumption together is worth $75,319 of $1.8M — 4.2%.** The figure
is almost entirely the cash the accounts produce, not what happens to it
afterwards. That is reassuring: the forecast does not rest on a guess about
property markets. The reason is simply that extraction starts in year 5, so the
money has three or four years to work, which is nothing.

Over a longer horizon it inverts completely, assuming the fleet keeps producing:

| Year | Wealth | Cash contributed | From returns |
| --- | --- | --- | --- |
| 8 | $1,807,300 | $1,732,078 | **4.2%** |
| 10 | $2,427,278 | $2,225,632 | 8.3% |
| 15 | $4,350,270 | $3,459,517 | 20.5% |
| 20 | $7,077,350 | $4,693,402 | 33.7% |
| 25 | $11,144,394 | $5,927,287 | **46.8%** |

The practical consequence for the next eight years: effort spent chasing two more
points of portfolio return is worth tens of thousands, while five more accounts
or a fifth of an R of expectancy are worth hundreds of thousands. Optimise the
fleet's output, not the yield on money that has already left it.

The long rows assume an edge surviving a quarter of a century, which nothing in
markets does, and a firm still operating. Treat them as showing when compounding
starts to matter, not as a forecast. `scripts/horizon.py` runs it.

## What the model does not contain

- A fixed 1:2 reward-to-risk on every trade. Tested: lognormal dispersion of the
  win multiple at 0.35 moves the eight-year figures by under 2%.
- Three trades per day. Two would cut everything by a third.
- Any ceiling on how fast a dead account can be replaced. See the caveat above.
- Integer contract counts. P&L is priced at the target risk percentage, while
  commissions and slippage are charged at the nearest whole contract count. This
  matches sizing to each trade's own stop width, which is what a real sizer does;
  it would overstate a bot that always traded a fixed contract count on a fixed
  stop by roughly 15%.
- No rules changes at the firm over eight years. There was one in March 2026.
- Quarter-point slippage on stopped exits. News days are far worse.
- And above all: it assumes the expectancy is known. It is not.
