# 42 — Real Customer Validation

## The premise

**Desk research does not establish willingness to pay.** Everything in this system — the segment
choice, the price, the positioning, the whole business — rests on **A-01: that vacation rental
operators will pay a third party for marketing video at all.** No evidence for that was found
(see [03](03-assumptions-register.md)).

**Only a purchase settles it.** Not a survey, not enthusiasm in an interview, not a waitlist, not
a "definitely, send me details." Money, from a stranger, at full price.

**No one is contacted during this project.** What follows is the instrument.

---

## V-0 — Verify the blocked primary sources (blocking, days 1–2)

**Nine claims in this system are grade B because the egress proxy blocked their primary sources**
([02](02-evidence-ledger.md)). Several of them are things we intend to say in public
([21](21-claim-register.md) ⏳ list). They must be read directly before launch.

| # | Read | Confirms | Blocks |
|---|---|---|---|
| V-0.1 | Airbnb Content Policy + Ground Rules for Hosts | **E-01, E-10, E-11** | [26](26-property-accuracy-rules.md), AD-3, all accuracy copy |
| V-0.2 | Vrbo Video Guidelines | E-03–E-07 | The Vrbo cut spec, D-06 |
| V-0.3 | Meta account spending limit docs | E-34 | **Any ad spend** |
| V-0.4 | Epidemic Sound licence, full text | E-18 | First paid delivery with music |
| V-0.5 | Airbnb Trademark Guidelines §2 | E-13 | Our website and ad copy |
| V-0.6 | Selected AI vendor ToS — commercial use, output rights, **training on uploads** | E-21–E-23 | First paid delivery |
| V-0.7 | Stripe pricing page | E-25 | Financial model accuracy |
| V-0.8 | Google Business Profile video specs | E-08 | The GBP deliverable |
| V-0.9 | Booking.com partner content policy | E-09 | Whether we mention it at all |

**If V-0.1 contradicts E-01** — if Airbnb does accept host video — **stop and re-run
[12](12-positioning.md) and [08](08-segment-selection-matrix.md).** The entire strategy pivots on
that one fact.

Plus the non-web blockers from [38](38-rights-and-security.md): lawyer review of the customer
agreement, accountant on entity and sales tax.

---

## V-1 — Prove we can make the thing (blocking, days 1–5)

**Before any customer is exposed to us**, and before any cost estimate is used to quote a price.

| Element | Spec |
|---|---|
| **What** | Produce 10 complete video packages on rights-clear or properly licensed property imagery |
| Properties | 5 different archetypes ([10](10-traveler-decisions-and-property-messaging.md)), including at least **3 with difficult interiors** — long sightlines, strong straight lines, complex layouts |
| Cost | Self-funded. Inside the $400 pre-revenue ceiling ([15](15-financial-model.md) §9) |
| **What we measure** | Attempts per accepted clip · generation cost per order · **minutes per step** · hard-reject rate by criterion · which concepts and prompts survive |

### What this replaces

| Assumption | Becomes |
|---|---|
| A-03 (output is good enough) | An observed accepted-clip yield |
| A-09 (generation cost $8–20) | A measured invoice |
| **A-10 (2.53h per order)** | **A measured time log — the dominant variable** |

### Kill conditions

| If | Then |
|---|---|
| Median accepted-clip yield worse than **1 in 4** | Generative motion is not viable for interiors. **Switch to template-based motion** and re-price |
| Median hands-on time over **3 hours** | Re-run [`tools/financial_model.py`](tools/financial_model.py). If effective hourly is under $60, **the price must rise or the scope must shrink before selling anything** |
| Generation cost over **$40/order** | Revisit tool choice ([25](25-tool-comparison.md)) and the price floor |

**Also produces:** the illustrative portfolio ([34](34-website-specification.md)) and 6+ pieces of
organic content ([29](29-content-calendar.md)). Nothing here is wasted even if the numbers are
bad.

### V-1 also tests the competitors (day 3)

Visit each named competitor site directly ([11](11-competitor-analysis.md) V-1): record public
pricing, turnaround, revision policy, and claim language. **Do not price against them until this
is done** — the current competitor pricing cells are honestly empty.

---

## V-2 — Channel rules (blocking before any outreach or marketing email)

Read the primary sources for: commercial email requirements in every jurisdiction we send to
(accurate headers, functional unsubscribe, physical address, opt-out windows — **US, UK and EU
rules differ**), and the messaging/promotion rules of every platform and community we participate
in ([33](33-partnership-plan.md)).

---

## V-3 — Interviews (days 6–20, 12 interviews)

Instrument: [09](09-interview-guide.md). Coding sheet and decision rules are in that document.

### Recruitment — without cold outreach

| Route | How |
|---|---|
| **Communities** | Participate genuinely for two weeks first, then ask openly: *"I'm researching how operators handle marketing content — would anyone spare 20 minutes? Not selling anything."* **Following the group's rules** |
| Warm network | Anyone in the founder's existing network who operates rentals |
| **Partner introductions** | Photographers ([33](33-partnership-plan.md)) introducing clients |
| Inbound | Anyone who enquires and does not buy — ask for 15 minutes |
| **Never** | Scraped lists, cold DMs, "I found your listing" emails |

### What interviews can and cannot establish

| Can establish | **Cannot establish** |
|---|---|
| What they have actually bought, and when (B1) | **Whether they will buy ours** |
| What triggered a past purchase (A-14) | What they will pay |
| Whether they have ever made a second video (A-05) | Whether our price is right |
| Whether platform enforcement is a live concern (A-02) | Whether our positioning works |
| Whether prior AI experience was negative | |
| Who approves (A-06) | |
| The language they use ([20](20-brand-voice-and-copy.md)) | |

**The right-hand column is why V-4 exists.** An interview programme that ends in optimism and no
orders has produced nothing.

---

## V-4 — The paid pilot (days 13–30) — **the only real evidence**

| Element | Spec |
|---|---|
| **Target** | **5 paid orders from strangers** — not friends, not family, not anyone who feels obliged |
| **Price** | **Full price. $279 Standard, $149 Starter.** No launch discount, no "first customer" deal, no free work |
| Scope | Exactly [14](14-offer-specification.md). No custom favours |
| Source | Wherever they come from. Organic, ads, partners, inbound |
| Window | 30 days from opening for orders |

### Why full price, with no exceptions

A discounted first sale answers a question we did not ask. "Will someone pay $149 for something
worth $279?" is not the question. **"Will someone pay $279?"** is. A discount destroys the only
experiment that matters, and it establishes a precedent with the customers we most want to keep.

### Acceptance criteria

| # | Criterion | Why |
|---|---|---|
| VA-1 | **≥5 paid orders at full price from strangers** | A-01 |
| VA-2 | **Median hands-on time <3 hours** | A-10 — the dominant cost variable |
| VA-3 | **Zero accuracy incidents** | [26](26-property-accuracy-rules.md) — non-negotiable |
| VA-4 | Zero gate escapes | [27](27-quality-rubric.md) |
| VA-5 | ≥4 of 5 delivered on or before the promised date | The one thing we can honestly promise |
| VA-6 | Refund rate ≤20% at this n | Small sample; 1 refund in 5 is tolerable, 2 is a signal |
| VA-7 | **≥1 customer says unprompted they will order again** | A-05, first weak signal |
| VA-8 | **≥3 of 5 report publishing at least one file** at day 21 | The silent failure mode (N3, [36](36-retention-plan.md)) |

### Evidence collected per order

Source and attribution · qualified-to-order path · price objection, verbatim · **full time log by
step** · attempt ratio and generation cost · both gate records · revisions by category · refund
and reason · day-21 publication answer · unprompted repeat intent.

---

## Decision rules at day 30

| Observation | Decision |
|---|---|
| **≥5 orders, VA-2/3/4 met** | **Proceed** to the 90-day plan ([43](43-launch-plan.md)) |
| 3–4 orders, delivery healthy | **Extend 30 days.** Do not scale acquisition. Do not change the offer yet |
| **1–2 orders after 40 qualified conversations** | **Offer or price problem.** Run PR-T1. Re-read lost-reason coding before changing anything |
| **0 orders, but leads arrived and qualified** | **A-01 is in danger, A-04 is fine.** Run MKT-T1 ([31](31-experiment-design.md)) as the final diagnostic |
| **0 orders, 0 qualified leads** | **A-04 failed first.** Fix channels — partnership-led — **before** touching the offer. Do not conclude nobody buys |
| Orders, but VA-2 missed (>3h each) | **Stop selling. Fix delivery** ([15](15-financial-model.md) §10). More sales would increase losses |
| **Any accuracy incident** | **Stop. Full review.** This is the one failure that ends the business's credibility |

## What must change if the evidence says so

| Evidence | Change |
|---|---|
| Orders only from one segment | Narrow the ICP to it ([08](08-segment-selection-matrix.md)) |
| Price named as the top lost reason in >50% of losses | Run PR-T1. **Note the 2× threshold** — a small difference is not detectable at n=20 |
| <3 of 12 interviewees recall platform enforcement | **A-02 fails.** Demote accuracy to a trust-builder; lead with time saved ([12](12-positioning.md)) |
| >6 of 12 report bad AI-tool experiences | Remove "AI" from headline copy |
| Delivery time is the main complaint | Extend the promise before adding capacity |
| Customers do not publish (VA-8 missed) | **The deliverable does not fit their workflow.** Change the formats, not the marketing |
| **Zero orders across organic, paid and a high-intent marketplace** | **A-01 has failed. Stop the business.** Write up what was learned |

**That last row is the point of the whole document.** A validation plan with no path to "stop" is
not a validation plan.
