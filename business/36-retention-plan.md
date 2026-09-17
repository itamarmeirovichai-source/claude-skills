# 36 — Retention, Repeat & Referrals

## 1. The question that governs this document

**Does this business actually have repeat demand?**

We do not know (A-05), and it matters enormously: it determines whether we can afford a higher
CAC (D-12), whether a subscription makes sense (D-10), and whether this is a business or a
sequence of one-off transactions.

**The honest prior, by segment:**

| Segment | Structural repeat frequency | Confidence |
|---|---|---|
| S1 single-unit host | **Once a year at best.** One property, one refresh cycle | Reasonable structural inference |
| S2 owner, 2–5 units | Per new unit + occasional refresh. Maybe 1–3 orders per year | Weak |
| **S3 PM, 6–25 units** | **Continuous** — new units onboard throughout the year | Strongest, and still untested |
| Any | Refurbishment, seasonal re-cut, new photography | Event-driven, unpredictable |

**This ranking is why S3 sits at the top of the segment matrix** ([08](08-segment-selection-matrix.md)) and why
[19](19-property-manager-sales.md) exists as a separate motion. It is also why we will not build
a subscription until the behaviour is observed.

---

## 2. Recurring models compared

| Model | Fits? | Reasoning |
|---|---|---|
| **Monthly subscription** | ❌ **Not at launch (D-10)** | Forcing a subscription onto a possibly-annual need produces churn, refund requests, and a reputation for lock-in. It would look like revenue for three months and cost us the market |
| **Credit pack / bundle** (e.g. 5 properties, valid 12 months) | ⏸️ **90-day candidate** | Matches how a PM actually consumes — in batches, unpredictably timed. **No forced cadence.** Best candidate if repeat is observed |
| **Seasonal package** (pre-summer, pre-winter re-cut) | ⏸️ 90-day candidate | Matches a real trigger (A-14). Depends on whether a re-cut is genuinely valuable or just a resale of the same footage |
| **Ordinary repeat orders** | ✅ **Launch default** | No commitment, no churn metric, no disappointment. Correct when frequency is unknown |
| **Retainer** | ❌ | Requires capacity we do not have (A-15, [37](37-capacity-and-contractors.md)) |

**Decision: ordinary repeat orders only.** A recurring product is designed **after** we observe
what customers actually repurchase, not before — and it is designed around their real cadence,
not a cadence convenient for our cash flow.

### The gate for building a recurring offer

**≥3 customers repurchase unprompted within 90 days** (D-10). "Unprompted" matters: a repeat
order produced by a discount offer or a follow-up campaign tells us about our marketing, not
about their need.

---

## 3. What a repeat order actually looks like

Repeat purchase here is **trigger-driven, not calendar-driven.** Following up on a timer annoys
people and produces nothing; following up on a trigger is useful.

| Trigger | Signal we can observe | Follow-up |
|---|---|---|
| **New unit onboarded** | They mention it; a new listing appears | "Saw you've added [property]. Want the same treatment?" |
| Refurbishment complete | They mention it; new photos appear | "Worth a new cut now the kitchen's done?" |
| **Pre-season, 6–10 weeks out** (A-14) | Their calendar, noted at the first order | One message, timed to *their* season |
| New photography | They mention it | "New photos? Happy to re-cut" |
| A video underperformed | They tell us | Second concept at the add-on price |
| **Nothing has changed** | — | **No follow-up.** This is the most important row |

**The last row is the discipline.** Most retention programmes fail by contacting people who have
no reason to buy, which trains them to ignore us for when they do.

### The arrival-video hypothesis

VC-10 ([22](22-creative-concepts.md)) — the post-booking arrival walkthrough (E-02) — is a
candidate repeat purchase worth watching. It is the one deliverable that is:
- per-property but also per-*change* (new lock, new parking arrangement, new access route),
- genuinely useful to a host who answers the same check-in questions weekly,
- near-zero accuracy risk,
- and legitimately usable on Airbnb, which nothing else we make is.

**Test it by offering it as an add-on and counting take-up**, not by building a product around
it first.

---

## 4. Churn and non-repeat reasons

**Terminology note:** with no subscription, "churn" is the wrong word. What we track is
**non-repeat** — a customer who bought once and did not buy again. That is a normal outcome, not
a failure, and treating it as failure produces bad behaviour.

| Category | What it means | Our response |
|---|---|---|
| **N1 — No current need** | Nothing changed at the property | **None.** Correct and healthy |
| **N2 — Structural low frequency** | One property, annual at most (A-05) | None. They were always a one-off |
| **N3 — Didn't publish what we made** | Files never used ([35](35-customer-operations.md) §6) | **Product problem.** Our formats or guidance failed them |
| **N4 — Output disappointed** | Quality below expectation | Quality problem. [27](27-quality-rubric.md) |
| **N5 — Price** | Worth it once, not repeatedly | Pricing signal ([15](15-financial-model.md)) |
| **N6 — Process friction** | Asset gathering too much work | Operations problem. Simplify intake |
| **N7 — Went elsewhere** | Competitor or in-house | Competitive signal ([11](11-competitor-analysis.md)) |
| **N8 — Left the business** | Sold the property, stopped hosting | None |

**N3 is the one to watch.** It is invisible — the customer does not complain, they simply never
return — and it is the most actionable, because it means our deliverable did not fit their
workflow. The day-21 usage question ([35](35-customer-operations.md) §6) exists specifically to
surface it.

---

## 5. Reviews and referrals

### When we ask

**After value is delivered**, never at delivery and never bundled with the delivery message.
Delivery day is when they are checking files, not when they know whether it worked. Day 10.

### How we ask

Per [20](20-brand-voice-and-copy.md). Once. Both requests optional, neither tied to anything.

### What we will not do

| Never | Why |
|---|---|
| **Incentivise a review** (discount, credit, entry into anything) | It changes what people write and what readers believe. A bought review is worth less than no review |
| **Incentivise a referral with a fee to the customer** | The recommendation stops being a recommendation. Partner referral fees are different — they are disclosed and the partner is a business ([33](33-partnership-plan.md)) |
| Suggest wording, or send a draft to approve | That is our review, signed by them |
| Ask more than once | |
| Ask a dissatisfied customer | |
| Publish a review without written permission and the customer's chosen attribution | |
| Publish a partial quote that changes the meaning | |

### The referral ask, and why there is no fee

> "If you know another operator who'd find this useful, I'd rather hear from them than run ads.
> No referral fee, because I don't want you recommending me for a discount."

This is a stronger ask than a paid one, because it makes the recommendation mean something. It
also avoids creating a class of customer who introduces unqualified leads to earn credit.

---

## 6. Measurement

Definitions: [41](41-measurement-definitions.md).

| Metric | Definition | Honest note |
|---|---|---|
| Repeat purchase rate | Customers with ≥2 orders ÷ customers with ≥1 order, **measured at 90 and 180 days** | Meaningless before 90 days |
| Time to second order | Median days | Small n for a long time |
| **Unprompted repeat rate** | Repeats with no preceding outreach from us | **The number that gates D-10** |
| Referral rate | Customers producing ≥1 referred enquiry ÷ delivered customers | |
| Review rate | Reviews received ÷ asked | |
| **Publication rate** | Customers who published ≥1 file ÷ delivered customers | **The most under-rated metric here.** Directly measures N3 |
| Non-repeat reason mix | % by N1–N8 | Distinguishes healthy non-repeat from product failure |

**What we will not compute:** lifetime value, until repeat behaviour is observed over at least
180 days with n ≥ 20 (D-12). An LTV computed from three customers is a number that will be used
to justify an unaffordable CAC.

## 7. Acceptance criteria

At 90 days:
- [ ] Repeat rate measured, not estimated
- [ ] **Unprompted** repeats counted separately
- [ ] Non-repeat reason coded for every non-repeating customer
- [ ] Publication rate measured via the day-21 question
- [ ] Zero incentivised reviews or referrals
- [ ] Zero reviews published without written permission
- [ ] D-10 gate evaluated explicitly: **build a recurring offer, or explicitly decide not to yet**
- [ ] Arrival-video add-on take-up counted
