# 31 — Experiment Design

**Authoritative source for experiment rules and stopping conditions.**

## The problem this document exists to solve

At our budget, **almost no acquisition experiment we can afford will be statistically
conclusive.** A $300 test producing 8 leads and 2 orders cannot distinguish a 15% conversion rate
from a 35% one. Pretending otherwise — declaring a winner because two weeks elapsed and one
number was higher — is the most expensive mistake available, because it converts noise into a
strategy and then funds it.

**So the rules below are designed for decision-making under acknowledged ignorance, not for
statistical significance.** They favour large, obvious differences; they treat small differences
as no difference; and they say so explicitly.

---

## Experiment template

Every acquisition experiment specifies all eleven fields before launch. **An experiment without a
pre-registered stopping condition is not an experiment — it is spending.**

| Field | Requirement |
|---|---|
| Hypothesis | A specific, falsifiable statement |
| Variable | **Exactly one** thing differs |
| Comparison | What it is measured against |
| Primary metric | One. Chosen before launch |
| Guardrail metrics | What must not get worse |
| Total budget | Hard number |
| **Maximum acceptable loss** | The number the account spending limit is set to |
| Conversion delay | How long between click and the outcome |
| Decision window | Earliest and latest decision date |
| Stopping conditions | Kill early, and stop normally |
| Scaling conditions | What would justify more money |

---

## The launch experiments

### AD-T1 — Which message acquires cheaper qualified leads?

| Field | |
|---|---|
| **Hypothesis** | The concrete-deliverable message (AD-1) and the accuracy/risk message (AD-3) produce materially different costs per qualified lead. **This is the live test of A-02 and of the [12](12-positioning.md) ordering decision** |
| Variable | Message angle. Same audience, same landing page, same budget pool |
| Comparison | Six concepts in one ad set ([30](30-advertising-packages.md)) |
| **Primary metric** | **Cost per qualified lead** (qualified = meets Q1–Q4, [08](08-segment-selection-matrix.md)) |
| Guardrails | Qualified-lead rate ≥30% of all leads; zero claim violations; zero accuracy complaints |
| Budget | $300 |
| **Max acceptable loss** | **$300 — set as the account spending limit before launch** (D-09, E-34) |
| Conversion delay | Form is same-session. **Order may take 5–14 days.** Do not judge on orders in a 15-day window |
| Decision window | Day 10 earliest, day 15 latest |
| **Stopping conditions** | Kill early: any claim violation, any ad rejected for policy, or cost per lead >$60 after $150 spent. Normal stop: day 15 or $300, whichever first |
| **Scaling conditions** | ≥8 qualified leads **and** cost per qualified lead <$30 **and** ≥1 order. All three, not any one |

### ORG-T1 — Does organic produce qualified leads at all?

| Field | |
|---|---|
| Hypothesis | 30 days of organic short-form produces ≥1 qualified lead |
| Variable | None — this is a baseline, not a comparison |
| Primary metric | Qualified leads attributable to organic |
| Guardrails | Content time ≤4h/week |
| Budget | 16 hours of founder time |
| Max acceptable loss | 16 hours |
| Conversion delay | **Long and unmeasurable.** Someone may follow for 6 weeks before enquiring |
| Decision window | Day 30, reviewed again at day 60 |
| **Stopping conditions** | **Do not stop at day 30 on zero leads** unless paid also produced zero — that combination is the A-04 kill condition. Content is a compounding asset; 30 days is a short look |
| Scaling conditions | ≥2 qualified leads → increase to 6h/week |

### PR-T1 — Is $279 the wrong price?

| Field | |
|---|---|
| Hypothesis | Price is not the primary barrier at $279 |
| Variable | Price shown: $279 vs $199 |
| Comparison | **Sequential, not simultaneous.** First 20 conversations at $279, next 20 at $199 |
| Primary metric | Qualified-conversation-to-order rate |
| Guardrails | Effective hourly ≥$60 ([15](15-financial-model.md)); refund rate unchanged |
| Budget | Foregone margin on 20 conversations |
| Max acceptable loss | ~$1,600 of foregone margin if all 20 convert at the lower price |
| Conversion delay | 5–14 days |
| Decision window | After 40 total conversations |
| **Stopping conditions** | Stop the $199 arm immediately if effective hourly drops below $60 |
| Scaling conditions | If $199 converts **more than double** $279, adopt it. Anything less than double is **not a detectable difference at n=20** and the higher price stays |

**Why sequential and why "more than double":** simultaneous price testing on a live site is
messy and slightly dishonest. And at n=20 per arm, only an enormous difference is distinguishable
from chance. Setting the bar at 2× is an explicit admission that a 30% improvement would be
invisible to us, so we will not act on one.

### MKT-T1 — Conditional marketplace diagnostic

Runs **only if** AD-T1 and ORG-T1 both produce zero orders.

| Field | |
|---|---|
| Hypothesis | Nobody buys this at any price (A-01 fails), vs. our channels are wrong (A-04 fails) |
| Variable | Channel only. **Same price, same scope** |
| Primary metric | Paid orders in 30 days |
| Budget | Listing fees + platform commission |
| **Stopping conditions** | 30 days or 3 orders |
| **Interpretation** | ≥1 order at full price → A-01 survives, A-04 failed, fix channels. **Zero orders across organic, paid, and a high-intent marketplace → A-01 has failed. Stop the business** |

**This is the most important experiment in the document**, because it is the one that can tell us
to quit. A business plan without an experiment that can end it is not a plan.

---

## Decision rules under small samples

| Observation | Correct interpretation |
|---|---|
| Ad A: 4 leads. Ad B: 2 leads | **No difference.** This is noise |
| Ad A: 12 leads. Ad B: 1 lead | Probably a real difference. Act, provisionally |
| 15 days elapsed, no clear winner | **Do not pick one.** Extend, or conclude "no detectable difference" and choose on other grounds |
| One ad got the only order | **Do not scale it.** n=1 |
| Cost per lead fell in week 2 | Could be learning-phase exit, could be noise. **Not evidence the creative improved** |
| A metric is best on the last day | Ignore. Terminal-day readings are the most common self-deception |

**The rule: we act on differences of roughly 3× or more. Anything smaller is not visible at our
sample sizes**, and we say so rather than pretending to a precision we do not have.

### Multiple comparisons

Six ads tested at once means six chances for one to look good by luck. With six variants, it
would be unsurprising for the best one to look meaningfully better than average **even if all six
were identical**. Therefore:

- The winner must beat the *average of the rest* by ≥3×, not beat the worst.
- A winner is **provisional** until it holds for a second period.
- We do not re-test the winner against a new variant and call the survivor validated. That is a
  ladder of luck.

### Delayed conversion

Click → form is immediate. **Form → order is 5–14 days.** So:
- Never judge an ad on orders inside 15 days.
- Cost per qualified lead is the primary metric *because* it resolves fast enough to act on.
- Cost per order is computed retrospectively, at 30 and 60 days, and it is the number that
  actually matters.

### Attribution

- One source field on the form, self-reported, plus UTMs.
- **Never sum conversions reported by multiple platforms.** Each claims credit for the same
  person; summing produces a number larger than reality
  ([41](41-measurement-definitions.md)).
- Our order record is the source of truth. Platform dashboards are directional only.
- Expect a meaningful share of "how did you hear about us" to be wrong or blank. **Report the
  unattributable share rather than allocating it.**

---

## Diagnosing failure: which part is broken?

When an experiment produces nothing, the instinct is to blame the creative. Usually it is not the
creative. Work the funnel in order:

| Symptom | Likely cause | Check | Fix |
|---|---|---|---|
| Low impressions, high CPM | Audience too narrow, or creative rejected | Delivery diagnostics | Broaden; check policy status |
| Impressions, no clicks | **Weak creative** | Hook retention, CTR | New hook, not new offer |
| Clicks, no form starts | **Broken or mismatched landing page** | Page load, mobile render, message match | Fix the page first |
| Form starts, no completions | **Too much friction** | Field-level drop-off | Remove fields |
| Leads, none qualified | **Wrong audience** | Q1–Q4 failure reasons | Change targeting, not creative |
| Qualified leads, no orders | **Weak offer or price** | Lost-reason coding | PR-T1, or revisit the offer |
| Orders, no margin | **Unprofitable production** | Time log | [15](15-financial-model.md) §10 — stop selling, fix delivery |
| Orders, then refunds | **Quality or expectation mismatch** | Refund reasons | [27](27-quality-rubric.md), [35](35-customer-operations.md) |
| Slow response losing leads | **Operational** | Time-to-first-response | Fix the process, not the ad |

**Each row has a different fix and they are not interchangeable.** Replacing creative when the
landing page is broken is the single most common waste in small-budget advertising.

---

## Creative learning log

Maintained for every experiment. **The point is to connect creative to business outcomes, not to
collect metrics.**

| Field | Example |
|---|---|
| Experiment ID | AD-T1 |
| Ad ID | AD-2 |
| Hypothesis | Correcting a false belief outperforms a benefit claim |
| Angle | Education / correction |
| Hook | "Airbnb won't let you post video" |
| Spend | $52 |
| Impressions / clicks / leads / **qualified** leads | 8,400 / 118 / 9 / 6 |
| Cost per qualified lead | $8.67 |
| **Orders (at 30 days)** | 1 |
| **Cost per order** | $52 |
| Guardrails breached | None |
| **Verdict** | Provisional winner. Not scaled — n too small |
| **What we actually learned** | *"Correcting a false belief got attention. We still don't know if it sells — one order is one order."* |

**The last row is the only one that matters.** A log full of numbers and no interpretations is a
spreadsheet, not learning.

## Acceptance criteria

- [ ] Every experiment pre-registers all eleven fields before spending
- [ ] Account spending limit set to max acceptable loss, every time
- [ ] No winner declared on a difference under 3×
- [ ] No ad judged on orders inside 15 days
- [ ] Platform conversions never summed across platforms
- [ ] Learning log entry with a plain-language "what we learned" for every experiment
- [ ] At least one experiment defined that could tell us to stop the business (MKT-T1)
