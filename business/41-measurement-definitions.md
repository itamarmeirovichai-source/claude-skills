# 41 — Measurement Definitions

**Authoritative source for every metric.** A metric used anywhere in this system is defined here,
with its numerator, denominator, window, source, and limitations.

## Why the limitations column exists

Most small-business dashboards report numbers whose weaknesses nobody has written down, which
means the numbers get treated as facts. **Every definition below names what it cannot tell us.**
A metric without stated limitations is more dangerous than no metric.

---

## Funnel metrics

| Metric | Numerator | Denominator | Window | Source | **Limitations** |
|---|---|---|---|---|---|
| **Inquiry rate** | Qualification form submissions | Unique site sessions | Rolling 30d | Site analytics + form | Sessions are undercounted by blockers; a repeat visitor may count twice |
| **Qualified opportunity rate** | Leads meeting Q1–Q7 | All leads | Rolling 30d | Human assessment | **Judgment-based.** Two people could code differently. Criteria must be applied literally, not generously |
| **Proposal rate** | Proposals sent | Qualified leads | Rolling 30d | Order record | Some qualified leads never reach proposal (they go quiet) |
| **Payment conversion** | Paid orders | Proposals sent | Rolling 30d | Stripe | **5–14 day lag.** A 30-day window mixes cohorts. Report by cohort where n allows |
| **Qualified-to-order** | Paid orders | Qualified leads | Rolling 30d, **cohorted** | Order record | The number that matters for CAC. **A-13's 25% is a placeholder, not a forecast** |

## Acquisition

| Metric | Definition | Window | Source | **Limitations** |
|---|---|---|---|---|
| **Cost per qualified lead** | Ad spend ÷ qualified leads attributed | Per experiment | Ad platform spend + our lead record | Attribution is imperfect; some leads are unattributable |
| **CAC** | Total acquisition spend ÷ new customers | Rolling 90d | Our records | **Excludes founder time.** Organic CAC is "free" only in cash |
| **Cost per order** | Ad spend ÷ orders from that source | 30d **and** 60d | Order record | Small n. Rarely conclusive ([31](31-experiment-design.md)) |

### Attribution rules

1. **Our order record is the source of truth.** Platform dashboards are directional.
2. **Never sum conversions reported by multiple platforms.** Each claims the same person; the sum
   exceeds reality.
3. Source is captured two ways: UTM into a hidden field, plus a self-reported "how did you hear
   about us."
4. **When they disagree, report both and say so.** Do not pick the flattering one.
5. **Report the unattributable share explicitly.** Do not distribute it proportionally — that
   invents data.
6. Organic short-form is **structurally under-attributed**: someone may follow for six weeks and
   then search our name. Expect organic's true contribution to exceed its measured one, and do
   not "correct" for it with a guess.

## Delivery and quality

| Metric | Definition | Window | **Limitations** |
|---|---|---|---|
| **Delivery time** | Business days from **complete assets** to delivery | Per order | Not from payment — that would measure the customer's speed, not ours |
| On-time rate | Delivered on or before the promised date ÷ delivered | Rolling 20 | |
| **Revision rate** | Orders using ≥1 revision round ÷ delivered | Rolling 20 | Some customers never respond; counted as no revision, which flatters it |
| Second-revision rate | Orders requesting a 2nd round ÷ delivered | Rolling 20 | |
| **Refund rate** | Refunded orders ÷ delivered | Rolling 20 | Lagging. A bad month shows up later |
| **Gate escape rate** | Defects reaching a customer ÷ delivered | Rolling 20 | **Under-counts** — some customers never report a defect they noticed |
| Hard reject rate | Videos hard-rejected at either gate ÷ videos produced | Rolling 20 | Internal, pre-delivery. **A rising number is good news about the gate and bad news about the pipeline** |
| **Attempt ratio** | Generation attempts ÷ accepted clips | Per order | Feeds A-09 |

## Economics

| Metric | Definition | Source | **Limitations** |
|---|---|---|---|
| Revenue per order | Total charged − refunds | Stripe | |
| **Contribution margin** | Revenue − variable cash costs | [15](15-financial-model.md) | **Excludes founder time.** Never quote it alone |
| **Effective hourly earnings** | Contribution margin ÷ founder hours | Time log | **The single most important metric in the business.** Worthless if the time log is not kept |
| Founder time per order | Minutes, by step | Time log | Self-reported. Under-reports interruption and context-switching |
| Fixed cost coverage | Contribution margin ÷ fixed costs | | |
| Cash buffer | Cash on hand ÷ monthly fixed costs | | |

## Retention

| Metric | Definition | Window | **Limitations** |
|---|---|---|---|
| Repeat purchase rate | Customers with ≥2 orders ÷ customers with ≥1 | **90d and 180d** | **Meaningless before 90 days** |
| **Unprompted repeat rate** | Repeats with no preceding outreach ÷ delivered customers | 90d | **The number that gates D-10.** A prompted repeat measures our marketing, not their need |
| **Publication rate** | Customers who published ≥1 file ÷ delivered customers | Day 21 | Self-reported. **The most under-rated metric here** — directly measures the N3 silent failure ([36](36-retention-plan.md)) |
| Referral rate | Customers producing ≥1 referred enquiry ÷ delivered | 90d | |
| Non-repeat reason mix | % by N1–N8 | 90d | Requires actually asking |

**Not computed:** lifetime value, until ≥20 customers and ≥180 days (D-12).

## Operational

| Metric | Definition | Target |
|---|---|---|
| Time to first response | Business hours from form to reply | **<4h median** |
| Queue depth | Orders in `awaiting_assets` + `in_production` | <8 ([37](37-capacity-and-contractors.md)) |
| Parked orders | Orders waiting >7 days on assets | Watched |
| Founder hours/week | Production + sales + marketing + admin | ≤40 |

---

## The funnel, connected end to end

Every stage must reconcile to the one before it. **If it does not reconcile, the gap is reported
as a gap, not smoothed.**

```
Content impression / ad impression
  └─ Click                      [platform + UTM]
      └─ Site session           [analytics]
          └─ Form submission    [form]      ← INQUIRY
              └─ Qualified      [human, Q1-Q7]
                  └─ Proposal   [order record]
                      └─ Payment [Stripe]   ← THE ONLY UNAMBIGUOUS EVENT
                          └─ Assets received
                              └─ Delivered  [order record]
                                  ├─ Revision
                                  ├─ Refund  [coded to cause]
                                  ├─ Published?   [day-21 question]
                                  └─ Repeat order
```

**Payment is the only unambiguous event in the chain.** Everything above it involves attribution
judgment; everything below it involves self-reporting. That is why
[42](42-validation-plan.md) treats paid orders as the only real evidence of demand.

### Deduplication in reporting

- One person, one lead, even across multiple form submissions.
- One order, one revenue record — from the `Payment` entity only, never from a webhook echo.
- A refunded order counts in *delivered* and in *refunded*, not removed from delivered.
- A repeat customer counts once in customers, twice in orders.

---

## Lost-reason coding

**Every** non-order is coded. Without this, the "why don't people buy" question gets answered by
whichever loss the founder remembers most vividly — usually price, usually wrongly.

| Code | Meaning |
|---|---|
| L1 | No publishing channel (declined by us — E-01) |
| L2 | Insufficient or wrong assets (declined by us) |
| L3 | Rights unclear (declined by us) |
| L4 | Price |
| L5 | Will do it themselves |
| L6 | Wanted a booking guarantee (declined by us) |
| L7 | Timing — no current trigger |
| L8 | Needed approval that did not come |
| L9 | Went to a competitor |
| L10 | Went quiet, no reason given |
| L11 | Asked for something we will not do (accuracy) |
| L12 | Deadline we would not accept |

**L1, L2, L3, L6, L11 and L12 are our declines, not losses.** Reporting them as lost deals makes
a disciplined qualification process look like a sales problem, and invites exactly the wrong fix.
They are reported as a separate line: **"declined by us."**

---

## Refund-reason coding

R1 accuracy defect · R2 spec miss · R3 technical defect · R4 late delivery · R5 changed mind
pre-production · R6 assets never supplied · R7 dispute/chargeback · R8 other.

**R1 is a business-critical incident** ([26](26-property-accuracy-rules.md)), not a line item.

---

## Reporting cadence

| Cadence | Contents |
|---|---|
| **Weekly** | Leads, qualified, orders, delivered, queue depth, time-to-first-response, **effective hourly (trailing 10)** |
| **Monthly** | Full funnel, CAC, margin, refund and revision rates, lost-reason mix, experiment log |
| **At each gate** | [43](43-launch-plan.md) go/no-go criteria, tripwires, assumption status |

### Tripwires — checked weekly

| Tripwire | Threshold | Action |
|---|---|---|
| Effective hourly (trailing 10) | **<$60/h** | **Stop selling. Fix delivery** ([15](15-financial-model.md) §10) |
| Refund rate | >15% | Pause the product |
| Revision rate | >70% | Review scope clarity |
| **Gate escapes** | **≥2 in 20 orders** | **Pause intake.** Fix the gate |
| Queue depth | ≥8 | Pause intake |
| Cost per qualified lead | >$30 | Pause the ad experiment |
| Cash buffer | <1 month fixed costs | Stop all discretionary spend |

## Acceptance criteria

- [ ] Every metric here has a real source before it is reported
- [ ] **No metric reported without its limitation when it informs a decision**
- [ ] Platform conversions never summed across platforms
- [ ] Unattributable share reported explicitly, never allocated
- [ ] Lost reason coded for 100% of non-orders
- [ ] "Declined by us" reported separately from "lost"
- [ ] Refund reason coded for 100% of refunds
- [ ] **Time log completed for 100% of orders** — without it, the most important metric does not
      exist
- [ ] Tripwires checked weekly, and acted on when breached
