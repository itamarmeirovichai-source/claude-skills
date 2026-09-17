# 46 — Open Decisions

Unresolved questions, each with an owner, a decision rule, and a deadline. **An open decision
with no deadline becomes a permanent assumption.**

## Blocking — must be resolved before the first paid order

| # | Decision | Owner | Decision rule | Deadline |
|---|---|---|---|---|
| **OD-1** | **Do the nine blocked primary sources confirm E-01 through E-34?** | Founder | Read them. If E-01 is contradicted, **stop and re-run [12](12-positioning.md) and [08](08-segment-selection-matrix.md)** | Day 1 |
| **OD-2** | **How is legal and accounting funded?** The $400 pre-revenue ceiling ([15](15-financial-model.md) §9) does not cover a lawyer, but [38](38-rights-and-security.md) requires one before the first paid order. **These two documents contradict each other** (C-1) | Founder | Either (a) budget legal/accounting separately as a necessary startup cost outside the tools ceiling, or (b) use a reviewed template agreement and accept the residual risk in writing. **Not (c) skip it** | Day 1 |
| **OD-3** | **Where does the illustrative portfolio's imagery come from?** (C-5) V-1 and [34](34-website-specification.md) both assume rights-clear property imagery exists and neither says how it is obtained | Founder | Options: (a) licence a stock property set with derivative rights, (b) photograph a property with written owner permission, (c) a partner photographer's portfolio with written permission. **Cost and rights must be confirmed before V-1 starts** | Day 1 |
| **OD-4** | Which entity, and what is the sales tax / VAT position on digital services, including cross-border? | Accountant | Professional advice. Jurisdiction-dependent | Day 5 |
| **OD-5** | Is the liability cap in the customer agreement enforceable as drafted? | Lawyer | Professional advice | Day 5 |

### Research done on OD-2 and OD-3 (2026-09-17)

Neither is resolved — both need a decision from the founder — but the option space is now mapped.

**OD-3 — portfolio imagery.** Two workable routes:

| Route | Cost | Rights position | Catch |
|---|---|---|---|
| **Free stock (Pexels / Unsplash)** | $0 | Both licences permit commercial use **and modification/adaptation**, which covers derivative video | ⚠️ **The licences explicitly do not clear identifiable people, private property, trademarks, logos, or some buildings** — and interiors are exactly where property releases bite. The platform pushes that responsibility onto the user |
| **Photograph a property with written owner permission** | A favour or a small fee | Cleanest — you hold everything, and the permission can be written to cover derivative video | Needs a property and an afternoon |
| Paid stock with an extended/property-released licence | $$ | Strongest | Costs money at the point we have least |

**Recommendation:** route 2 for the hero examples (you control the rights completely, and it
doubles as the first real production run for V-1), with free stock only for generic B-roll where
no property is identifiable. **Do not build the public portfolio on free stock interiors without
reading each image's release position** — we would be making exactly the rights mistake we warn
customers about in [38](38-rights-and-security.md).
Sources: [Pexels licence](https://www.pexels.com/license/), [Pexels commercial-use FAQ](https://help.pexels.com/hc/en-us/articles/360042295214-Can-I-use-the-photos-and-videos-for-a-commercial-project), [free-stock licensing analysis](https://www.licenseorg.com/blog/free-stock-photos-licensing-traps).

**OD-2 — funding legal review.** The middle path exists and is defensible:

| Option | Cost | Risk |
|---|---|---|
| Full custom agreement drafted by a lawyer | $$$ | Lowest, and not fundable at pre-revenue |
| **Reputable template + a paid lawyer review of the two clauses that matter** (liability cap, IP/rights assignment) | $ | **Recommended.** Targets spend at the clauses that actually bite |
| Template alone, unreviewed | $0 | Accepted only if written down as an accepted risk, with a date to revisit |

Standard practice supports our draft: capping aggregate liability at fees paid under the
agreement is the conventional small-business position, which is what
[38](38-rights-and-security.md) already specifies. A contract does not need a lawyer to be
valid — but this one carries an IP assignment to the customer and a rights warranty from them,
which is exactly where a cheap review earns its money.
Sources: [service agreement guide](https://beancount.io/blog/2026/04/25/service-agreement-template-complete-guide-small-business), [freelance agreement protections](https://selenethelawyer.com/blog/freelance-service-agreement-template).

**Neither of these is a decision I can make for you.** OD-2 is a spending choice and OD-3 depends
on whether you have a property to photograph.

## Blocking — must be resolved before scaling

| # | Decision | Owner | Decision rule | Deadline |
|---|---|---|---|---|
| **OD-6** | **Is generative motion viable on interiors, or is template motion the real product?** (A-03, and the production lead's finding in [44](44-independent-review.md)) | Founder | V-1 measurement. Accepted-clip yield below 1-in-4 → template motion becomes primary and the price is re-derived | Day 5 |
| **OD-7** | **What is the real time per order?** (A-10 — the dominant variable) | Founder | V-1 time logs. Over 3h with effective hourly under $60 → **raise price or shrink scope before selling** | Day 5 |
| **OD-8** | **Is $279 the right price?** (A-07 — real-estate-sale anchors may not transfer to STR) | Founder | PR-T1 ([31](31-experiment-design.md)). **Adopt $199 only if it converts more than 2×** — smaller differences are not detectable at n=20 | Day 60 |
| **OD-9** | **Is accuracy a message or only a discipline?** (A-02) | Founder | AD-1 vs AD-3, plus interview C1–C3. Under 3 of 12 recalling platform enforcement → demote accuracy to a trust-builder | Day 30 |
| **OD-10** | Does template reuse actually reduce per-unit time on a portfolio job? | Founder | PS-6 ([19](19-property-manager-sales.md)). **No volume discount quoted until measured** | First PM pilot |
| **OD-11** | Is the 12-minute Gate 1 budget sufficient? ([44](44-independent-review.md), production lead) | Founder | Measure actual Gate 1 time over 10 orders. If the median is under 8 minutes, the gate is not being done properly and the budget or the checklist must change | Day 30 |

## Strategic — resolved by evidence over time

| # | Decision | Owner | Decision rule | Deadline |
|---|---|---|---|---|
| **OD-12** | **Does repeat demand exist?** (A-05) | Founder | ≥3 unprompted repeats in 90 days → design a recurring offer around observed behaviour. Otherwise stay one-time (D-10) | Day 90 |
| OD-13 | Is the PM owner-acquisition angle stronger than the guest-booking angle? ([07](07-customer-research.md) §S3) | Founder | AD-4 performance + interview D4 | Day 30 |
| OD-14 | Is "AI" a liability word with this segment? | Founder | Interview B4. Over 6 of 12 negative → remove from headline copy | Day 20 |
| OD-15 | Referral or white label for partnerships? | Founder | Referral at launch. Revisit at 90 days, after accuracy escalation has been exercised once ([33](33-partnership-plan.md)) | Day 90 |
| OD-16 | Is the arrival video (VC-10) a product rather than an add-on? | Founder | Add-on take-up rate ([36](36-retention-plan.md)) | Day 90 |
| OD-17 | Do we ever open the S1 single-host segment? | Founder | Only if unsolicited S1 inbound converts profitably. **Currently declined on structural grounds** (E-01) | Day 90 |
| OD-18 | Should the illustrative portfolio include rejected clips? | Founder | Proposed yes ([34](34-website-specification.md)) — showing rejects is differentiated. Test on the examples page | Day 30 |

## Deliberately not decided

Recorded so a future session does not mistake these for oversights:

| Not decided | Why |
|---|---|
| Lifetime value | Requires 180 days and n≥20 (D-12). Any earlier number would be used to justify an unaffordable CAC |
| Subscription pricing | Gate 3 not met. Designing it now means designing around our cash flow, not their need |
| Volume discount tiers | [15](15-financial-model.md) §6 — measurement first |
| Whether to expand beyond the US | English-speaking market first (A-15). Cross-border tax alone is a separate project |
| Brand identity beyond a clean site | The most enjoyable way to avoid finding out whether anyone will buy |
| Hiring plan beyond the first contractor | Gate 4 not met |

## Review cadence

Reviewed at every go/no-go gate ([43](43-launch-plan.md)). **A decision past its deadline with no
resolution is escalated to the founder report as a blocker**, not silently carried forward.
