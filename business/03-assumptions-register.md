# 03 — Assumptions Register

**Authoritative source for every `[ASSUMPTION]` in this system.** Documents cite `A-NN`.

Each assumption names **what breaks if it is wrong**. An assumption with no dependent decision
is trivia and should be deleted rather than tracked.

## Risk key

- **Fatal** — if false, the business as designed does not work; a different business is needed.
- **Structural** — if false, the offer, price, or segment must change.
- **Tunable** — if false, a number or a process changes; the business survives.

---

## Fatal assumptions

### A-01 — Vacation rental operators will pay a third party for marketing video at all
**[ASSUMPTION: No evidence was found that STR hosts or property managers purchase standalone
marketing video as a discrete line item. Evidence exists that they buy *photography* (E-31 is a
real-estate market), and that they have marketing budgets (E-30), but budget existence is not
purchase intent for this specific good.]**

- **Depends on it:** the entire business.
- **Why we believe it anyway:** E-28 shows 62% of operators with a direct site get <25% of
  bookings direct — an active dissatisfaction. E-29 ranks marketing reach as PMs' top 2026
  priority. Photography is a proven adjacent purchase.
- **Why it might be false:** hosts may regard video as optional decoration given that Airbnb —
  their dominant channel — cannot display it (E-01). The purchase may only exist inside an
  agency retainer, not standalone.
- **How we test it:** [42](42-validation-plan.md) V-3. Five paid orders at full price from
  strangers, not friends. **No discounts, no free work.** Money is the only evidence.
- **Kill condition:** fewer than 3 paid orders after 40 qualified conversations.

### A-02 — There is a buyer for whom "video, but provably accurate" is worth paying for
**[ASSUMPTION: Our differentiation rests on accuracy discipline (E-11, E-26 rules). We assume at
least one segment perceives platform-accuracy risk as real and will pay a premium over a
generic AI tool to have it managed. No one has told us this.]**

- **Depends on it:** the whole positioning in [12](12-positioning.md); our price premium over
  DIY tools (E-32, $10–100/mo).
- **Why it might be false:** hosts may have never heard of a listing being penalised for altered
  media and may find the concern abstract and mildly insulting.
- **How we test it:** interview question set B in [09](09-interview-guide.md) asks about *past*
  platform enforcement experience, not hypothetical concern. If <20% of interviewees can recall
  any listing-media enforcement, the fear is not live and the positioning must move to
  time-saving and craft instead.
- **Kill condition:** accuracy framing loses to time-saving framing in ad test AD-T1
  ([31](31-experiment-design.md)) by >2x cost per qualified lead.

### A-03 — AI-assisted output from existing photos is good enough to be sold, not merely tolerated
**[ASSUMPTION: We have produced zero videos. We do not know our own failure rate, artifact rate,
or how many generations it takes to get an acceptable clip from a real host's phone photos.]**

- **Depends on it:** every cost figure in [15](15-financial-model.md); turnaround promises in
  [14](14-offer-specification.md); the hard-reject thresholds in [27](27-quality-rubric.md).
- **Why it might be false:** image-to-video motion on interior photos commonly produces geometry
  warping on straight architectural lines, doorways that dissolve, and furniture that morphs.
  Interiors are the *worst case* for generative video because humans are extremely sensitive to
  architectural geometry.
- **How we test it:** [42](42-validation-plan.md) V-1 — 10 self-funded production runs on
  public-domain / properly licensed property imagery before any customer contact. Measure
  attempts per acceptable clip, minutes per deliverable, cost per deliverable.
- **Kill condition:** if median acceptable-clip yield is worse than 1 in 4 attempts, or median
  hands-on time per order exceeds 3 hours, the price floor in [15](15-financial-model.md) must
  rise above what the segment will plausibly pay, and the product must change (to template-based
  motion rather than generative).

---

## Structural assumptions

### A-04 — The initial buyer is reachable without cold outreach
**[ASSUMPTION: We assume organic content plus small paid tests can produce qualified inbound at
a cost below our target CAC. We have no channel data.]**
- **Depends on it:** [28](28-channel-strategy.md) primary/secondary channel choice; the 30-day
  plan in [43](43-launch-plan.md).
- **Test:** first 30-day organic + $300 paid test. **Kill condition:** zero qualified leads from
  30 days of organic and $300 of ads → the channel hypothesis is wrong, not the offer; move to
  partnership-led acquisition ([33](33-partnership-plan.md)) before changing the offer.

### A-05 — Repeat demand exists for *some* segment, but not for individual single-property hosts
**[ASSUMPTION: A single-property host who owns one cabin plausibly needs new video roughly once
a year, or on refurbishment/seasonal change. A property manager onboarding new units needs video
continuously. We have not verified either frequency.]**
- **Depends on it:** the decision to **not** launch a subscription ([36](36-retention-plan.md));
  the decision to exclude LTV from the financial model ([15](15-financial-model.md)).
- **Test:** count unprompted repeat orders in the first 90 days. Do not build a subscription
  until ≥3 customers have repurchased without being asked.

### A-06 — Property managers have a real approval path we can navigate solo
**[ASSUMPTION: We assume a PM decision involves an operations/marketing lead as champion, an
owner or principal as economic buyer, and possibly individual property-owner consent for
portfolio marketing. We have not mapped a real one.]**
- **Depends on it:** the pilot design in [19](19-property-manager-sales.md).
- **Test:** the first three PM conversations should *map the approval path* before quoting.

### A-07 — Real-estate-sale videography pricing (E-31) is a valid anchor for STR
**[ASSUMPTION: E-31 prices come from the property *sales* market, where a single video supports
a six-figure commission. STR marketing has a much weaker per-asset economic justification, so
willingness to pay may be materially lower.]**
- **Depends on it:** the price ladder in [15](15-financial-model.md).
- **Test:** price test PR-T1 in [42](42-validation-plan.md). This is the assumption most likely
  to force a price cut.

### A-08 — Our customer owns, or can obtain, usable source photography
**[ASSUMPTION: We assume the typical target customer has ≥15 usable photos per property at
≥1500px, and holds the rights to them.]**
- **Depends on it:** the entire "no site visit" model; input requirements in
  [14](14-offer-specification.md).
- **Known risk:** photos commissioned from a photographer are frequently **licensed, not owned**,
  often limited to listing use. A host may not have the right to authorise derivative video.
  This is a live legal exposure ([38](38-rights-and-security.md)).
- **Test:** the intake form asks for rights confirmation; track what share of leads fail it.

---

## Tunable assumptions

| ID | Assumption | Depends on it | Test |
|---|---|---|---|
| **A-09** | Median generation cost lands $8–20/order including failures, based on E-22 per-second pricing × ~50s of usable footage × ~2.5x attempt ratio. | [15](15-financial-model.md) cost line | Measure real invoices over 10 orders |
| **A-10** | Founder hands-on time is ~2.0h/order at steady state after ~10 orders of learning. | Effective hourly rate; capacity ceiling in [37](37-capacity-and-contractors.md) | Time-track every order from order #1 |
| **A-11** | Revision rate ≈ 35% of orders use their included round; ≈8% request a second. | Margin; the revision policy | Count over 20 orders |
| **A-12** | Refund rate ≤5% of orders in year one. | Cash buffer sizing | Count |
| **A-13** | 25% of qualified conversations convert to a paid order at the Standard price. | Break-even CAC maths | **This is a placeholder, not a forecast.** Replace after 20 conversations |
| **A-14** | A host's peak buying window is 6–10 weeks before their high season, plus at new-listing launch and post-refurbishment. | Seasonality planning in [28](28-channel-strategy.md), [43](43-launch-plan.md) | Ask in every interview: "when did you last commission any marketing asset, and what prompted it?" |
| **A-15** | English-language, US-first market. Founder is solo and may be unavailable 8–10 hours at a stretch. | Turnaround promises; the "no same-day SLA" rule in [37](37-capacity-and-contractors.md) | Given as an operating constraint, not tested |
| **A-16** | Buyers will accept a 3–5 business day turnaround as normal, and pay a premium for 48–72h. | Rush pricing in [15](15-financial-model.md) | Offer both; measure take-up |

---

## Assumptions we refuse to make

Recorded so no future session quietly adopts them:

- ❌ That a delivered video causes bookings. (E-20 — no causal evidence.)
- ❌ That market size (E-26) implies demand for our service.
- ❌ That competitor visibility (E-32) implies competitor profitability.
- ❌ That a subscription is the right model because agencies like recurring revenue.
- ❌ That LTV is a multiple of first order value. We model **first order only** until repeat
  purchase is observed.
- ❌ That a free sample converts. Free work is a cost with an unproven return
  ([14](14-offer-specification.md) §7).
