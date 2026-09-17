# 39 — Data & Agent Architecture

**Authoritative source for the data model and agent permissions.**

## Design principle

> **Language models draft. Deterministic systems decide. Humans authorise anything that leaves
> the building.**

Every architectural choice below follows from that, and from D-15: no agent sends an external
message, publishes content, spends money, or issues a refund without human approval.

---

## 1. Entities

| Entity | Authoritative source | Lifecycle states |
|---|---|---|
| **Contact** | Qualification form, then human correction | `new → qualified → customer → suppressed` |
| **Organisation** | Form + human | `prospect → customer → former` |
| **Property** | **Property Fact Sheet, signed by the customer** | `draft → confirmed → archived` |
| **Lead** | Form submission | `new → qualifying → qualified → declined → converted` |
| **Opportunity** | Human, after qualification | `open → proposed → won → lost` |
| **Offer** | [14](14-offer-specification.md) — **static config, never model-generated** | `active → retired` |
| **Order** | Payment event | `created → awaiting_assets → in_production → in_review → delivered → revision → closed → refunded` |
| **Asset** | Customer upload | `received → assessed → selected → rejected → archived → deleted` |
| **PropertyFact** | **Signed fact sheet only** | `stated → confirmed → superseded` |
| **Approval** | Customer written confirmation | `pending → granted → withdrawn` |
| **ProductionJob** | System, on order transition | `queued → generating → editing → gate1 → gate2 → exported → failed` |
| **Deliverable** | Export step | `draft → approved → delivered → superseded` |
| **Revision** | Customer request + human categorisation | `requested → categorised → in_progress → complete → billed` |
| **Payment** | Stripe | `pending → succeeded → refunded → disputed` |
| **Message** | Inbound/outbound log | `draft → approved → sent → failed` |
| **Suppression** | Unsubscribe, complaint, bounce, explicit request | `active` — **terminal, never removed** |
| **Experiment** | [31](31-experiment-design.md) | `designed → running → decided → archived` |
| **Cost** | Vendor invoices, time log | `recorded` |
| **AuditEvent** | System | `recorded` — immutable |

### The two that matter most

**PropertyFact** is the only permitted source of property truth. Not the listing text, not the
photographs, not the model's inference, not the founder's memory. If a fact is not on a signed
fact sheet, it does not appear on screen ([26](26-property-accuracy-rules.md)).

**Suppression is terminal.** Once a contact is suppressed, no process may un-suppress them. A
system that can re-add someone who asked to be left alone will eventually do it.

---

## 2. Relationships

```
Organisation 1─* Contact
Organisation 1─* Property
Property     1─1 PropertyFactSheet (signed)  ← the only source of property facts
Property     1─* Asset
Lead         *─1 Contact
Opportunity  *─1 Organisation, references Offer (static)
Order        *─1 Opportunity, 1─* ProductionJob, 1─* Payment
ProductionJob 1─* Deliverable, 1─* Cost, 1─1 Gate1Record, 1─1 Gate2Record
Deliverable  *─* Asset (provenance: which photo produced which clip)
Order        1─* Revision
Contact      1─0..1 Suppression   ← checked before EVERY outbound message
Everything   1─* AuditEvent
```

**Deliverable ↔ Asset provenance is a hard requirement, not a nice-to-have.** It is what lets us
answer "what was this clip derived from" if a platform or a customer ever asks
([26](26-property-accuracy-rules.md) §5).

---

## 3. Deduplication

**Merging two different people is worse than holding two records for one person.** The asymmetry
is severe: a wrong merge exposes one customer's property assets to another, which is a
confidentiality breach. A duplicate is an annoyance.

| Signal | Action |
|---|---|
| Identical email (normalised: lowercase, trimmed) | **Auto-merge.** Safe |
| Same name + same organisation domain | **Flag for human review.** Never auto-merge |
| Same name, different email | **Never merge.** Different people share names |
| Same phone | Flag only |
| Same property name | **Never merge** — many properties share names |

**Rules:** only email is safe to auto-merge on. Everything else is a suggestion for a human.
Merges are reversible and logged. **Gmail dot/plus-address normalisation is not applied** — a
customer using `name+work@` may genuinely want them separate.

---

## 4. Preventing duplicates in the things that cost money

| Duplicate risk | Prevention |
|---|---|
| **Duplicate charge** | Stripe idempotency key on every charge. One `payment_intent` per order |
| **Duplicate message** | Idempotency key = `(contact_id, template_id, order_id)`. **Suppression checked at send time, not at queue time** |
| **Duplicate production job** | `ProductionJob` unique on `(order_id, deliverable_type)`. State transition to `generating` is atomic |
| **Duplicate sale counted** | Revenue counted from the `Payment` record only, never from a webhook echo or a platform dashboard |
| **Duplicate webhook** | Every inbound webhook stores its event ID; replays are ignored |
| **Duplicate refund** | Refund requires founder approval **and** a check that no refund exists for that payment |

### Idempotency and explicit state

**Every external side effect carries an idempotency key.** Charges, emails, generation API calls,
delivery link creation.

**Every state transition is explicit and logged** with `from`, `to`, `actor`, `timestamp`,
`reason`. Illegal transitions are rejected — an order cannot go from `awaiting_assets` to
`delivered`, no matter what any code or agent asks for.

### Failures

| Failure | Handling |
|---|---|
| Timeout | Exponential backoff, max 3 attempts, then escalate to a human queue |
| Partial failure (3 of 7 files exported) | Job stays `exporting`. **Never `delivered`.** Resume exports only the missing files |
| Vendor error | Retry once, then switch vendor ([25](25-tool-comparison.md)), then template fallback |
| **Payment succeeded, order not created** | Reconciliation job compares Stripe payments to orders daily and escalates any mismatch |
| Unrecoverable | Escalate with full context. **Never silently drop** |

---

## 5. Agent roles

Agents exist **only where they create clear value.** Three, not a swarm. Each has explicit
permissions, and **none can act externally**.

### AG-1 — Intake Assistant
| | |
|---|---|
| **Inputs** | Qualification form submission; the thread so far |
| **Outputs** | A **draft** reply; a qualification assessment against Q1–Q7 |
| Tools | Read contact/lead/order records; read [14](14-offer-specification.md), [15](15-financial-model.md), [21](21-claim-register.md) |
| Knowledge | Offer spec, price list, claim register, objection library. **Retrieved live, never memorised** |
| **Allowed** | Draft a reply. Flag qualification status. Suggest a package from the static offer list |
| **Forbidden** | **Send anything.** Invent a price, discount, deadline, guarantee, or property fact. Make any claim not in [21](21-claim-register.md) |
| Approval | **Human reads and sends. Every time** |
| Cost limit | $0.50 per conversation |
| Escalation | Complaint · refund request · request for a human · legal or accuracy question · anything unusual |
| Evaluation | [40](40-testing-plan.md) |
| Audit | Full input/output logged, **redacted** |

### AG-2 — Production Assistant
| | |
|---|---|
| **Inputs** | Asset list, signed fact sheet, chosen concept |
| **Outputs** | A **draft** storyboard: shot order, source-photo mapping, caption text, prompt selection |
| Tools | Read assets and fact sheet; read [22](22-creative-concepts.md), [23](23-scripts-and-storyboards.md), [26](26-property-accuracy-rules.md) |
| **Allowed** | Draft storyboards. Propose shot order. Draft captions **using only fact-sheet values**. Select prompts from the approved library |
| **Forbidden** | **Perform Gate 1** ([26](26-property-accuracy-rules.md)). Write a caption containing a fact not on the fact sheet. Write freehand generation prompts. Approve anything |
| Approval | Human reviews the storyboard before generation |
| Cost limit | $0.50 per order |
| Escalation | Fact sheet incomplete · photo contradicts fact sheet · any accuracy ambiguity |

### AG-3 — Reporting Assistant
| | |
|---|---|
| **Inputs** | Order, cost, time, experiment records |
| **Outputs** | Metric summaries per [41](41-measurement-definitions.md) |
| Tools | Read-only on operational data |
| **Allowed** | Compute defined metrics. Flag tripwire breaches |
| **Forbidden** | Write anything. **Invent a metric definition.** Estimate a missing value. Attribute an outcome causally |
| Approval | None needed — read-only, internal |
| Cost limit | $0.20 per report |
| Escalation | Data gap that would change a number — **report the gap, never fill it** |

### What is deliberately NOT an agent

| Not an agent | Why |
|---|---|
| **Gate 1 accuracy review** | The control that protects the customer from the harm this product can cause. A model evaluating its own pipeline's output for invented content is exactly the wrong reviewer ([26](26-property-accuracy-rules.md)) |
| Gate 2 final sign-off | Requires viewing on a device, at speed |
| Pricing | Static config. **Nothing is computed** |
| Refund decisions | D-15 |
| Scope categorisation | Has direct revenue consequences |
| Sending any external message | D-15 |
| Ad spend changes | D-09 |

---

## 6. Deterministic vs. model-driven

| Deterministic — never a model | Model-assisted — always human-approved |
|---|---|
| Prices and package contents | Drafting a reply |
| Turnaround dates | Drafting a storyboard |
| Revision counting and categorisation rules | Suggesting shot order |
| Capacity and queue state | Drafting captions from fact-sheet values |
| Suppression checks | Summarising a long thread |
| Payment and refund amounts | Proposing experiment interpretations |
| Metric computation | |
| Property facts | |
| Claim permissions | |

**The rule: if a wrong answer would create a binding promise, a charge, or a property claim, it
is deterministic.**

---

## 7. Retrieval

Agents consult **current, approved** sources — they never rely on what was in their context last
week or what they were trained on.

| Need | Source | Refresh |
|---|---|---|
| Offer and price | [14](14-offer-specification.md), [15](15-financial-model.md) as structured config | On every request |
| **Claim permissions** | [21](21-claim-register.md) as a structured allow/deny list | On every request |
| Property facts | The signed fact sheet **for this order only** | On every request |
| Capacity | Live queue state | On every request |
| Policy | [26](26-property-accuracy-rules.md), [35](35-customer-operations.md) | On every request |

**Hard rules:**
- **An agent may never see another customer's property facts or assets.** Retrieval is scoped to
  the order.
- **If retrieval fails, the agent says so and escalates.** It never answers from memory. An
  agent that guesses a price when the price service is down is worse than an agent that says "I
  can't reach the price list."

---

## 8. Audit and redaction

Every agent action logs: timestamp, agent, inputs (redacted), outputs, tools called, cost,
whether a human approved, and what was sent.

**Redacted from every log:** email addresses, property addresses, payment details, API keys,
asset URLs ([38](38-rights-and-security.md)).

**Immutable and retained** for the relationship + 2 years, alongside the Gate 1 and Gate 2
records.

## 9. Acceptance criteria

- [ ] Zero external messages sent without human approval
- [ ] Zero prices, discounts, deadlines or guarantees generated by a model
- [ ] Zero property facts originating anywhere but a signed fact sheet
- [ ] Zero duplicate charges, messages, or production jobs
- [ ] Suppression checked at send time on 100% of outbound messages
- [ ] Every external side effect carries an idempotency key
- [ ] Every state transition logged with actor and reason
- [ ] No agent has read access to another order's assets
- [ ] Retrieval failure escalates rather than falling back to memory
- [ ] Logs contain no unredacted customer data — **verified by inspection, not assumption**
