# 44 — Independent Review

Six adversarial passes over the whole system. **The standard: a weakness is not resolved because
it is documented.** Each finding below is marked **RESOLVED** (a change was made), **MITIGATED**
(reduced, residual risk stated), or **OPEN** (acknowledged, unfixed, and it stays that way until
something changes).

---

## 1. The skeptical buyer

*A property manager with 14 units who has been pitched by four vendors this year.*

> "You have no customers, no results, and you admit video might do nothing. Why would I go first?"

**Finding — OPEN.** There is no good answer. We have no social proof
([13](13-consumer-psychology-and-sales-method.md) §6), and our substitutes — a published
checklist, a visible decline list, a refusal to claim outcomes — are *credibility* signals, not
*proof*. Some buyers will require proof and we will lose them. That is correct at this stage and
the only fix is time.

> "Your pilot is $837. The other vendor quoted me $99 a video."

**Finding — MITIGATED.** OBJ-8 answers it honestly and we decline to compete on price. **Residual
risk:** if V-1's competitor sweep shows specialists at sub-$100 with comparable output, our
Starter tier is undercut and the [11](11-competitor-analysis.md) gap analysis needs re-running.
We genuinely do not know their pricing yet.

> "You keep telling me what you won't do. Is there anything you're actually good at?"

**Finding — RESOLVED.** Real, and a live risk in the voice guide. [12](12-positioning.md) leads
with the concrete deliverable (P4) and puts the accuracy discipline second **precisely** to avoid
sounding like a list of refusals. Copy review ([20](20-brand-voice-and-copy.md) §7) should add a
check: does this read as capable, or only as careful?

> "What happens when you're ill?"

**Finding — MITIGATED.** [37](37-capacity-and-contractors.md) covers it, and the honest answer is
that a solo operator is a single point of failure. We say so rather than pretending otherwise.

---

## 2. The traveler watching the property video

*Booking a place for six people next August.*

> "This is pretty. Where does everyone actually sleep?"

**Finding — RESOLVED.** VC-4 and SC-7 exist for exactly this, with a mandatory bunk-room shot.
Capacity is the named refund trigger (E-12).

> "The video makes it look enormous. Photos always do."

**Finding — RESOLVED, and turned into an asset.** Honest video often makes a space look *smaller*
than wide-angle photography ([10](10-traveler-decisions-and-property-messaging.md)). We treat
that as a yield strategy: fewer disappointed arrivals, fewer refunds, better reviews. It is one of
the more persuasive things we can say to an operator.

> "Why does the light look different in every shot?"

**Finding — MITIGATED.** Q6 (lighting continuity) is scored at ×2 in
[27](27-quality-rubric.md). **Residual risk:** source photos taken at different times are the
norm, not the exception, and continuity may be the most common quality complaint.

> "Something about the doorway is wrong and I can't say what."

**Finding — MITIGATED, and this is the real threat.** HR-1 hard-rejects geometry warping and Q2
is weighted ×3. **Residual risk is high**: interiors are the worst case for generative motion
(A-03), the artifact is subtle enough to pass a tired reviewer, and a viewer's reaction is
distrust rather than a complaint we would ever hear about.

---

## 3. The production lead

> "2.53 hours per order is invented."

**Finding — OPEN, and correctly so.** A-10 is an estimate and it is the dominant variable in the
whole model. V-1 exists solely to replace it before anything is sold
([43](43-launch-plan.md) day 5).

> "Twelve minutes for Gate 1 on a seven-file order is optimistic."

**Finding — OPEN. This is a real design weakness.** Gate 1 requires opening each clip beside its
source photograph. On a 10-clip video that is roughly 70 seconds per clip including judgment. It
is achievable but tight, and **the failure mode is silent** — a rushed gate looks identical to a
careful one until something escapes.

**Partial control:** [26](26-property-accuracy-rules.md) acceptance criteria flag a median under
8 minutes as evidence the gate is *not* being done properly. That catches habitual rushing but not
a single bad night. **Remains open.**

> "Batching gates across a portfolio is where a systematic error ships."

**Finding — RESOLVED.** [24](24-production-workflow.md) batches by step but keeps **both gates
per property**, and [19](19-property-manager-sales.md) forbids batch approval.

> "The template fallback is the real product and you've buried it."

**Finding — OPEN, and worth sitting with.** If V-1 shows poor generative yield on interiors, the
honest product is programmatic pan-and-scale on real photographs: completely safe, entirely
accurate, much cheaper, and much less impressive in a demo. **It might be the better business.**
The plan treats it as a fallback ([24](24-production-workflow.md)); V-1 may promote it.

---

## 4. The finance lead

> "90.8% contribution margin is a vanity number. It excludes the only real cost."

**Finding — RESOLVED.** [15](15-financial-model.md) §3 says so explicitly, and
[41](41-measurement-definitions.md) forbids quoting contribution margin without effective hourly
earnings alongside it.

> "The compound bad case loses money and you present it as a footnote."

**Finding — RESOLVED, and strengthened.** The runnable model shows −$19.12 per order in the
compound case, and §8 now states that each component shift is individually survivable — which is
precisely why the combination is dangerous and why no single dashboard number catches it.

> "Portfolio pricing at $199 is a trap."

**Finding — RESOLVED.** [15](15-financial-model.md) §6 and
[19](19-property-manager-sales.md) PS-6 forbid quoting volume pricing before per-unit delivery
cost is measured. This is one of the strongest controls in the system.

> "A $400 pre-revenue ceiling doesn't cover a lawyer."

**Finding — OPEN.** [38](38-rights-and-security.md) requires legal review before the first paid
order, and legal review costs more than $400. **The ceiling and the requirement conflict.** The
honest resolution: legal and accounting are a separate, necessary startup cost outside the tools
ceiling, and the founder must budget for them. **This is now flagged in
[46](46-open-decisions.md) as an unresolved cost the plan does not fund.**

> "A 15% referral fee on a first order, against a $75 target CAC?"

**Finding — RESOLVED.** 15% of $279 is $41.85 — comfortably under the $75 target CAC, and referral
leads should convert better than cold. Sound.

---

## 5. The customer support lead

> "The whole plan assumes assets arrive. Most won't, on time."

**Finding — MITIGATED.** [16](16-sales-playbook.md) §1 names onboarding as the stage that kills
orders, the clock starts on complete assets, and [35](35-customer-operations.md) defines the
parked-order path. **Residual risk:** a parked order is paid money against undelivered work, and
holding it feels bad for both parties. The 90-day proactive refund is the control.

> "A day-21 usage question on every order is a lot of follow-up nobody asked for."

**Finding — MITIGATED.** It is one message and it measures the silent failure mode (N3). Worth
the intrusion, but it should never become a sequence.

> "C-11 shows the founder forgot to re-confirm a date when assets slipped. What stops that
> recurring?"

**Finding — RESOLVED.** It is now a process rule, not an intention:
[35](35-customer-operations.md) §2 requires written date confirmation within 4 business hours of
complete assets, and E2E-1 tests it.

> "Refunds require founder approval, and the founder may be gone for ten hours."

**Finding — OPEN, accepted.** A refund delayed ten hours is worse than a refund delayed ten
minutes and much better than an agent approving refunds (D-15). The auto-acknowledgement states
real response hours.

---

## 6. The platform and rights reviewer

> "Nine of your platform claims come from secondary sources you couldn't read."

**Finding — MITIGATED, and it is the most serious methodological weakness in this work.** The
egress proxy blocked airbnb.com, help.vrbo.com and others. **Controls:** everything is graded B,
the ⏳ list in [21](21-claim-register.md) blocks publication, AD-3 cannot run, and V-0 is the
first blocking task. **Residual risk:** if E-01 is wrong, the entire strategy is wrong. Nothing
short of reading the page fixes this.

> "You're building a business on top of another company's enforcement policy, which can change."

**Finding — OPEN and structural.** If Airbnb enabled gallery video tomorrow, D-01's reversal
condition fires and our positioning needs rewriting — though our production system would still be
the asset. **Control:** quarterly re-check, and it is written into D-01 and D-06.

> "You upload customers' property photographs to third-party AI vendors."

**Finding — MITIGATED.** [38](38-rights-and-security.md) requires reading vendor terms on
retention and training, and requires disclosure. **Residual risk:** vendor terms change, and a
vendor training on uploaded customer content would be a confidentiality problem we might not
discover promptly. Quarterly review is the only control and it is imperfect.

> "The photography rights problem is bigger than you've made it."

**Finding — MITIGATED, and it is genuinely serious.** A-08: many hosts hold listing-use-only
licences and cannot authorise derivative video. **Controls:** intake confirmation, uncertainty as
a stop condition, suggested licence wording, and the photographer partnership route that fixes it
at source. **Residual risk:** customers will tick the box without understanding it. The free-text
uncertainty field is the only real catch, and it depends on their honesty.

---

## Contradictions found and resolved

| # | Contradiction | Resolution |
|---|---|---|
| **C-1** | $400 pre-revenue ceiling ([15](15-financial-model.md)) vs. mandatory legal review ([38](38-rights-and-security.md)) | **Unresolved cost.** Legal/accounting sits outside the tools ceiling. Raised to [46](46-open-decisions.md) |
| C-2 | "Under-promise turnaround" ([13](13-consumer-psychology-and-sales-method.md)) vs. "3–5 business days" advertised | Consistent: 5 days is the promise, 3 is the internal target. Made explicit in [37](37-capacity-and-contractors.md) |
| C-3 | Accuracy as differentiator ([12](12-positioning.md)) vs. A-02 saying buyers may not care | Deliberate: P4 leads with the deliverable, accuracy second. AD-1 vs AD-3 tests it |
| C-4 | "No free work" (D-11) vs. free photo assessment (OBJ-6) and free guides | A 10-minute assessment is qualification, not production. Distinction now explicit in [14](14-offer-specification.md) §5 |
| **C-5** | Illustrative portfolio requires rights-clear property imagery — **where does it come from?** | **Raised to [46](46-open-decisions.md).** V-1 assumes this is solvable and does not say how |
| C-6 | Capacity of 5 orders/week vs. day-30 target of only 5 orders total | Not a contradiction — demand, not capacity, is the constraint at launch |

---

## The answers to the six required questions

### The weakest assumption
**A-01 — that anyone pays for this at all.** Not A-03 or A-10, which are operational and
measurable in a week. A-01 is the one with no evidence, no proxy, and no way to resolve it except
by asking strangers for money. Every other document assumes it.

### The most likely reason customers will not buy
**No felt urgency.** Not price, not quality, not AI skepticism. Their dominant channel (Airbnb)
cannot display video (E-01), there is no evidence video causes bookings (E-20), and we refuse to
invent any (D-05). "Doing nothing" is the market-share leader
([11](11-competitor-analysis.md) §I) and it is a *reasonable* choice for many operators. The
counter is not a better argument — it is a better trigger: pre-season, a new unit, an owner pitch.

### The most likely reason delivery will lose money
**Time per order exceeding 2.5 hours** (A-10), through some combination of generation retries,
revision cycles, and customer hand-holding. At 4 hours the effective rate is $63; at 5 it is $51.
**It would not feel like failure** — it would feel like being busy, which is why it is dangerous
and why the tripwire is a number, not a feeling.

### The largest unsupported promise
**"Three to five business days."** It is the most prominent commitment we make, it appears in
every ad and every proposal, and it rests entirely on an unmeasured time estimate plus a
37% capacity reserve. **We have never delivered a single order.** Everything else we say is either
a process fact or a refusal.

### The most consequential automation failure
**An agent writing a property fact that is not on the fact sheet** — a caption reading "sleeps 12"
on a property that sleeps 10, or "steps from the beach" instead of a measured figure. It is
CF-4, it flows straight into a delivered video, and it produces exactly the misrepresentation
E-11 and E-12 penalise. Controls: facts only from the signed sheet
([39](39-data-and-agent-architecture.md)), Gate 1 checks every number, HR-5 hard-rejects it.
**Three independent controls, because one is not enough for the failure that could end the
business.**

### The three highest-value experiments

| Rank | Experiment | Resolves | Cost | Why |
|---|---|---|---|---|
| **1** | **V-1: 10 practice packages with time logs** ([42](42-validation-plan.md)) | A-03, A-09, **A-10** | ~$150, 20h | Replaces the three numbers everything depends on, before a customer is risked. **Cheapest high-value experiment available** |
| **2** | **V-4: 5 paid orders at full price from strangers** | **A-01** | 30 days | The only thing that settles the weakest assumption. Nothing else substitutes |
| **3** | **AD-1 vs AD-3** ([31](31-experiment-design.md)) | A-02, positioning order | $300 | Tests whether accuracy is a message or just a discipline, and whether P4's ordering is right |

---

## What this review did not fix

Stated plainly, so no future session mistakes documentation for resolution:

1. **We still do not know if anyone will buy** (A-01).
2. **We still cannot make the thing** — zero videos produced (A-03).
3. **Nine platform claims remain unverified** against primary sources.
4. **We have no proof, no portfolio, and no results**, and our substitutes may not be enough.
5. **The legal and accounting cost is unfunded** by the current plan (C-1).
6. **Where the illustrative portfolio's imagery comes from is unanswered** (C-5).
7. **The Gate 1 time budget may be too tight**, and the failure is silent.
