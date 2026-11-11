# 37 — Capacity, Contractors & Continuity

**Authoritative source for capacity limits and business continuity.**

## 1. Capacity

At 2.53 hours per Standard order (A-10), assuming the founder can sustain **20 production hours
per week** alongside sales, marketing and admin:

| | Value |
|---|---|
| Theoretical weekly capacity | 7.9 orders |
| **Committed weekly capacity** | **5 orders** |
| Reserve | ~2.9 orders' worth of hours |

### Why commit to 5 and not 8

Running at theoretical capacity means any single disruption — a hard-reject requiring a rebuild
([27](27-quality-rubric.md)), a vendor outage, an 8–10 hour unavailability (A-15) — pushes a
customer's delivery past its promised date. **Once that happens, the delay propagates to every
order behind it.**

The 37% reserve is not slack. It is what makes a delivery date a commitment rather than an
aspiration — and delivery reliability is one of the few things we can honestly promise (D-05
removes the others).

### Limits

| Limit | Value | Rationale |
|---|---|---|
| **Concurrent orders in production** | **3** | Beyond this, context-switching inflates per-order time, which attacks the dominant cost variable ([15](15-financial-model.md)) |
| Committed orders per week | 5 | Above |
| Portfolio jobs | 5 properties per 10 business days | [19](19-property-manager-sales.md) |
| **Rush orders per week** | **1** | Only against genuine spare capacity. **Never on a first order** |
| Delivery buffer | **Promise 5 days when the real estimate is 3** | Under-promise ([13](13-consumer-psychology-and-sales-method.md) §9) |
| **Backlog threshold** | **8 orders in the queue → pause intake** | Below |
| Content time | ≤4h/week, hard cap | Content never eats production hours |

### Intake pause

At 8 queued orders, the site's form is replaced with:

> **Not taking new orders this week.** The queue is full and I'd rather say that than give you a
> date I'll miss. Leave your email and I'll tell you when it opens — usually within a week.

**This is real scarcity, honestly stated** ([13](13-consumer-psychology-and-sales-method.md) §11).
We may only say "full" when we are full, and we must actually decline work at that number.
Otherwise it becomes fake scarcity, which is forbidden.

### Intake also pauses when

- **Two quality gate escapes occur within 20 orders** ([27](27-quality-rubric.md)) — the gate is
  broken and more volume makes it worse.
- **Trailing-10-order effective hourly falls below $60** ([15](15-financial-model.md) §10) — more
  sales would increase losses.
- Any accuracy incident reaches a platform ([26](26-property-accuracy-rules.md) §7).

**Pausing intake because delivery is unhealthy is not a setback. Selling through it is.**

---

## 2. When hiring becomes justified

**Not when we are busy. When the maths works.**

A contractor at $25/hour taking the 50 minutes of edit-and-export work per order costs ~$21 per
order. Contribution margin falls from $253 to $232; founder time falls from 2.53h to ~1.7h;
effective hourly on the founder's remaining time rises to ~$136.

**That is only worth doing if the freed hours produce more than $21 of value per order** — which
means they must go into selling or into orders we could not otherwise take.

### The gate — all four must be true

| # | Condition | Why |
|---|---|---|
| H1 | **≥15 orders delivered**, with a measured time log | Cannot delegate a process we have not measured ([24](24-production-workflow.md)) |
| H2 | **Demand exceeds committed capacity for 3 consecutive weeks** | Not one busy week |
| H3 | **Cash buffer ≥ $2,000** | We can pay them through a slow month ([15](15-financial-model.md)) |
| H4 | **The task is documented well enough that a stranger could do it** | If it isn't written down, we are hiring to avoid writing it down |

**H4 is the real gate.** Hiring to escape documenting a process reliably produces a contractor who
needs constant supervision, which costs more founder time than the task did.

### What is delegated first, and what is never delegated

| Delegate first | Never delegate |
|---|---|
| Edit assembly to storyboard | **Gate 1 accuracy review** ([26](26-property-accuracy-rules.md)) |
| Exports and file naming | Gate 2 final sign-off |
| Caption timing | Refund decisions (D-15) |
| Asset prep and shortlisting | Scope-change decisions |
| | Any customer-facing promise |

**Gate 1 is never delegated, at any scale.** It is the control that protects the customer from
the specific harm this product can cause, and it is the one thing a contractor has no incentive
to do slowly and carefully.

---

## 3. Contractor system

### Selection criteria

| Criterion | Requirement |
|---|---|
| Skill | Can assemble to a storyboard, cut to time, place and time captions |
| **Judgment** | **Can articulate why a clip should be rejected.** Weighted highest |
| Reliability | Meets a deadline on a paid test |
| Communication | Asks a question rather than guessing. **This is the one that matters most for accuracy** |
| Availability | Overlapping hours at least 3 days/week |
| Terms | Accepts a written agreement covering confidentiality and IP assignment |

### Paid test brief

**Always paid. Never a free trial.** $75 flat, regardless of outcome.

> Attached: 18 photographs of an illustrative property, a completed fact sheet, a storyboard, and
> our export checklist.
>
> Produce: one 9:16 cut, 20–25 seconds, to the storyboard, with captions burned in, exported to
> spec.
>
> **Also return:** a short note listing any shot you think should not be used, and why.
>
> Deadline: 3 business days. $75 on delivery, whether or not we work together again.

**The note is the actual test.** Anyone competent can follow a storyboard. What we need to know is
whether they notice that photo 11 shows a fireplace the fact sheet does not mention — because
that judgment is the thing that keeps a customer's listing safe.

### Quality rubric for contractor work

[27](27-quality-rubric.md), plus:

| Criterion | Pass |
|---|---|
| Storyboard adherence | Every shot present, in order, to time |
| Export spec | 100% correct |
| **Flagging** | Raised at least one genuine concern, or correctly stated there were none |
| Communication | Asked before guessing |
| Deadline | Met, or notified before it |

### Onboarding, handoff, access

| Element | Rule |
|---|---|
| Documents | [24](24-production-workflow.md), [26](26-property-accuracy-rules.md), [27](27-quality-rubric.md), [23](23-scripts-and-storyboards.md) export checklist |
| Handoff | Storyboard + shortlisted assets + fact sheet. **Never the whole customer folder** |
| **Access** | **Least privilege.** Per-order shared folder, expiring. No access to the customer list, payment system, email, or accounts ([38](38-rights-and-security.md)) |
| **Prohibited** | Storing customer assets on personal devices beyond the job; using them in their own portfolio without written permission from us **and** the customer |
| Payment | Per order, not hourly, once quality is established. Paid within 5 days |
| Review | After orders 1, 5 and 10, then quarterly |
| **Offboarding** | **Access revoked the same day.** Assets confirmed deleted in writing. Final payment made promptly — always |

---

## 4. Continuity

The founder may be unavailable for 8–10 hours at a stretch (A-15). Every procedure below assumes
nobody is watching.

| Failure | Prevention | Response |
|---|---|---|
| **Generation vendor outage** | Two vendors configured ([25](25-tool-comparison.md)) | Switch. If both are down, template-motion fallback, or notify the customer with a new date |
| **Vendor terms change** | Quarterly ToS re-check | Stop using it. Re-verify delivered assets made with it |
| Contractor unavailable | Never a single point of failure on a deadline | Founder absorbs; delivery buffer covers it |
| **Failed generations exceed budget** | 3× cost cap ([24](24-production-workflow.md)) | Escalate. Template fallback |
| **Founder unavailable 8–10h** | **Delivery buffer; no same-day promises; account spending limits set** (D-09) | Auto-acknowledgement states real response hours. No SLA is breached |
| Founder ill / unavailable for days | Queue visible; every order has a written brief | Notify every active customer **proactively** with a new date. Offer refunds. **Never go silent** |
| **Lost assets** | 3-2-1 backup: working copy, cloud, offline archive | Restore. If unrecoverable, request re-supply and refund the order |
| Payment provider issue | Manual invoice fallback | |
| Site down | Static site, low failure surface | Form falls back to a direct email address |
| **Founder stops the business** | Below | |

### Backups and retention

| Data | Backup | Retention |
|---|---|---|
| Customer source assets | Cloud + offline | **Deleted 90 days after delivery unless the customer asks us to keep them** |
| Delivered files | Cloud + offline | 12 months, then archived |
| Production metadata, review records | Cloud + offline | Relationship + 2 years ([26](26-property-accuracy-rules.md)) |
| Order and financial records | Cloud + offline | Per tax requirements ([38](38-rights-and-security.md)) |

### Customer handover, if the business stops

1. Notify every customer with an open order. **Refund every undelivered order in full.**
2. Deliver everything deliverable, or refund it.
3. Give every customer 30 days' notice and a download link for their files.
4. Confirm in writing that their source assets have been deleted.
5. Cancel subscriptions **after** the retention obligations are met, not before.

**This is written down now, while it is cheap to think about clearly.** A founder deciding to stop
is not in a good state for improvising an ethical wind-down.

---

## 5. Acceptance criteria

- [ ] Committed capacity never exceeds 5 orders/week
- [ ] Concurrent production never exceeds 3 orders
- [ ] Intake paused when any pause condition is met — **actually paused, not intended**
- [ ] No rush order on a first order
- [ ] Backups verified by an actual restore test, at least once
- [ ] No contractor engaged before all four H-gate conditions are met
- [ ] Contractor access is per-order and expiring
- [ ] Gate 1 never delegated
- [ ] Wind-down procedure reviewed at each go/no-go gate
