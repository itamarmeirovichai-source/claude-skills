# 16 — Sales Playbook

Method: consultative diagnosis with JTBD questions and scope-based negotiation
([13](13-consumer-psychology-and-sales-method.md)). Prices: [15](15-financial-model.md). Scope:
[14](14-offer-specification.md). Claims: [21](21-claim-register.md).

## 1. The customer journey

| Stage | What happens | Owner | Exit criterion | Typical duration |
|---|---|---|---|---|
| **Discovery** | They see organic content, an ad, a partner referral, or a search result | System | Click to site | — |
| **Inquiry** | Qualification form submitted | Customer | Form complete | — |
| **Qualification** | We check Q1–Q7 ([08](08-segment-selection-matrix.md)) | Founder / agent draft | Qualified or declined | <4 business hours |
| **Demonstration** | Illustrative portfolio + the closest-match example | Founder | They have seen representative work | Same message |
| **Scope agreement** | Package, deliverables, dates, what we will not do | Founder | Written scope acknowledged | 1–2 exchanges |
| **Proposal** | One page: scope, price, dates, terms, payment link | Founder | Sent | Same day |
| **Payment** | Stripe. 100% upfront ≤$500 | Customer | Cleared | — |
| **Onboarding** | Asset upload + Property Fact Sheet + rights confirmation | Customer | **Assets complete** — the clock does not start before this | 1–3 days |
| **Production** | [24](24-production-workflow.md) | Founder | Passed both review gates | 3–5 business days |
| **Approval** | Internal accuracy + quality sign-off | Founder | Both gates passed | — |
| **Delivery** | Files, labelled by destination, + Where To Post This guide | Founder | Sent | — |
| **Revision** | One consolidated round within 7 days | Customer | Closed or expired | ≤2 business days |
| **Repeat** | Follow-up at a genuine trigger, not on a timer | Founder | Order or polite no | — |
| **Referral** | Asked once, after value delivered | Founder | Asked | — |

### The stage that actually kills orders

**Onboarding.** The customer has paid and now has homework: gather photos, fill a fact sheet,
confirm rights. This is where orders stall for a week and where our turnaround promise quietly
breaks. Two controls:

1. **The clock starts on complete assets, not on payment.** Stated before payment, every time.
2. **A single reminder at 48h and another at 5 days**, then the order parks with a clear note.
   No nagging. [35](35-customer-operations.md) covers the stalled-order process.

---

## 2. Paths by lead source

| Source | First touch | Key difference | Qualification depth |
|---|---|---|---|
| **Inbound (organic)** | Form → reply within 4 business hours | Warmest. Already saw work. Go straight to fit questions | Standard Q1–Q7 |
| **Paid ad lead** | Form → reply within 4 business hours | Colder, less context. **Must re-verify they have somewhere to publish** — ads attract S1 hosts we decline | Stricter on Q1/Q2 |
| **Organic content response (comment/DM)** | Reply in-thread, then move to form | Never pitch in the comment. Answer the question, offer the link once | Standard |
| **Referral (customer or partner)** | Personal reply, reference the referrer by name | Highest trust. Do **not** skip qualification — a referred bad-fit is still a bad fit | Standard, faster |
| **Returning customer** | Direct message, no form | Skip demonstration. Confirm anything changed about the property | Fact sheet re-confirmation only |
| **Property management company** | [19](19-property-manager-sales.md) | Multi-stakeholder, pilot-first | Extended, incl. approval mapping |
| **Outbound** | **Not used at launch** — see below | | |

### On outbound outreach

**We do not do cold outbound at launch.** Reasons, in order:

1. **Channel rules must be verified before any outreach**, and they vary by channel: platform
   DM policies, CAN-SPAM requirements for commercial email (accurate headers, functional
   unsubscribe, physical address), and the terms of any community or forum. **None of these were
   verified in this project** — registered as verification task V-2 in
   [42](42-validation-plan.md).
2. It consumes founder hours in exactly the block that production needs, and A-15 says those
   hours are scarce and interruptible.
3. Sending cold pitches with no portfolio and no results produces a low response rate and burns
   the addressable list.

If outbound is added later, it is **warm outbound only**: someone who has interacted with our
content, or a partner-introduced contact, with the channel's rules read first and a suppression
list honoured from the first send ([32](32-search-email-remarketing.md)).

---

## 3. Conversation state model

States are explicit so that a human or an assistant can pick up any conversation and know what
is permitted. **No state permits inventing a price, a discount, a deadline, or a property fact**
(D-15, [39](39-data-and-agent-architecture.md)).

### S0 — NEW
- **Entry:** form submitted or first message received.
- **Required info:** none yet.
- **Allowed questions:** any single opening question.
- **Allowed promises:** response time only.
- **Next:** → S1 on acknowledgement.
- **Escalate:** never.
- **Stop:** if the message is spam or abusive.

### S1 — QUALIFYING
- **Entry:** acknowledged.
- **Required info to leave:** unit count; **where they would publish** (Q2); photo count and
  resolution; who decides; timeline.
- **Allowed questions:** Q1–Q7, **one at a time**.
- **Allowed promises:** none beyond response time.
- **Next:** → S2 if qualified; → S6 if not.
- **Escalate:** if they claim an existing order, a complaint, or ask for a human.
- **Stop:** if they decline to answer Q2 twice — without a publishing channel we cannot serve
  them.

### S2 — DIAGNOSING
- **Entry:** qualified.
- **Required info to leave:** what they have tried; what triggered them now; primary guest type;
  the one thing that makes the property different.
- **Allowed questions:** JTBD questions from [09](09-interview-guide.md) §B, adapted.
- **Allowed promises:** none.
- **Next:** → S3.
- **Stop:** if diagnosis reveals a bad fit → S6.

### S3 — RECOMMENDING
- **Entry:** diagnosis complete.
- **Required info:** all of S1 and S2.
- **Allowed:** recommend exactly one package, from [14](14-offer-specification.md), at the price
  in [15](15-financial-model.md). State turnaround. State what we will not do.
- **Forbidden:** any booking, occupancy, revenue or ranking claim (D-05). Any price not in
  [15](15-financial-model.md). Any deadline not checked against the capacity board
  ([37](37-capacity-and-contractors.md)).
- **Next:** → S4 on interest; → S5 on objection; → S6 on no.

### S4 — PROPOSING
- **Entry:** package agreed in principle.
- **Required:** written scope — package, file list, property name, dates, price, revision policy,
  exclusions.
- **Allowed promises:** exactly what the proposal says.
- **Next:** → S7 on payment; → S5 on objection.
- **Escalate:** any request for custom terms, volume pricing, or an unusual deadline → founder.

### S5 — HANDLING OBJECTION
- **Entry:** an objection raised.
- **Required:** diagnose the cause before responding ([17](17-objection-library.md)).
- **Allowed:** one diagnostic question, then a response, then a next step.
- **Forbidden:** discounting to close (§[15](15-financial-model.md) discount rules). Inventing
  evidence. Arguing past a second "no."
- **Next:** → S4, or → S6.
- **Stop:** **second clear no ends the conversation.** Thank them, leave the door open, stop.

### S6 — DECLINED / NOT A FIT
- **Entry:** we decline, or they decline twice.
- **Allowed:** a genuine alternative recommendation (a videographer, a DIY tool, a guide, or
  "come back when X").
- **Forbidden:** further pitching, drip sequences they did not opt into.
- **Next:** terminal. Add to suppression unless they opted in
  ([32](32-search-email-remarketing.md)).

### S7 — ORDERED
- **Entry:** payment cleared.
- **Required:** assets, Property Fact Sheet, rights confirmation.
- **Allowed promises:** the delivery date, **counted from complete assets**.
- **Next:** → production ([24](24-production-workflow.md)).

### Conversation rules that apply in every state

1. **Respond to what they actually said.** If they asked about turnaround, answer turnaround
   first, before any question of our own.
2. **One question per message** where a question is needed. A message with four questions in it
   gets one answer, usually to the easiest.
3. **Never re-ask for information already given.** Read the thread. This is the single most
   common way an automated or distracted reply destroys trust.
4. **Never conceal automation** (D-13). A drafted-by-assistant message says so, or a human sends
   it.
5. **Never impersonate a human employee.** There is one person in this business. Saying "our
   team" when it is one founder is a small lie that makes every other claim suspect.
6. **Stop when it is not a fit**, and say why.

---

## 4. Qualification form (the only front door)

Design principle: short enough to complete on a phone in 90 seconds, but it must capture Q1–Q4,
because that is what makes the first reply useful instead of a round of basic questions.

| Field | Type | Maps to |
|---|---|---|
| Name | text | — |
| Email | email | — |
| How many properties do you manage? | 1 / 2–5 / 6–25 / 25+ | Q1 |
| **Where would you use the video?** (tick all) | Instagram or TikTok / Our booking site / Vrbo listing / Google profile / Email to guests / Not sure yet | **Q2 — the most important field** |
| Link to your site or social | url, optional | Q2 verification |
| Roughly how many photos do you have per property? | Under 15 / 15–30 / 30+ | Q3 |
| Are the photos yours to use? | Yes, I own them / A photographer took them / Not sure | **Q4 — rights** |
| When do you need this by? | No rush / Within 3 weeks / Within a week / Sooner | Q6 |
| Anything else? | textarea | — |

**"Not sure yet" on the publishing question is not a disqualification — it is a conversation.**
Many buyers genuinely have not thought about it, and helping them think about it is the most
useful thing we do in the first reply.

---

## 5. Acceptance criteria for the sales system

After 20 qualified conversations:
- [ ] Median first response under 4 business hours
- [ ] 100% of conversations have a recorded state and outcome
  ([41](41-measurement-definitions.md))
- [ ] Zero instances of a promise outside [14](14-offer-specification.md) /
      [15](15-financial-model.md)
- [ ] Zero booking-performance claims made
- [ ] Zero cases of re-asking for information already supplied
- [ ] Every declined lead received a genuine alternative
- [ ] Lost-reason coded for every non-order
