# 38 — Rights, Contracts & Security

**Authoritative source for rights, contract terms and access control.**

## ⚠️ This is not legal advice

Everything here is **business practice designed to reduce risk**, assembled from secondary
sources. **A lawyer in the operating jurisdiction must review the customer agreement, the rights
language, and the tax position before the first paid order.** Several items below are flagged as
requiring that review, and the flags are not decorative.

## The four categories, kept distinct

Conflating these is how businesses talk themselves into confident nonsense.

| Category | Binding? | Example here | Consequence of breach |
|---|---|---|---|
| **Law** | Yes, enforceable by a state | FTC truth-in-advertising (E-17); CA B&P §10140.8 (E-14); commercial email rules | Legal liability |
| **Platform policy** | Yes, enforceable by the platform | Airbnb content rules (E-11); Vrbo video guidelines (E-03–E-07); Airbnb trademark rules (E-13) | Account or listing action |
| **Contract** | Yes, between parties | Our customer agreement; vendor ToS (E-18, E-21, E-24) | Breach of contract |
| **Business recommendation** | No | Our disclosure policy; our accuracy checklist | None — but they exist to prevent the above |

---

## 1. Rights

### Property image rights — the live exposure (A-08)

**The problem:** a customer sends us photographs. Those photographs were very often taken by a
photographer who licensed them for *listing use*, retaining copyright. The customer may have no
right to authorise a derivative work, and therefore no right to give us one.

**This is the most likely legal problem this business will actually encounter**, and it is
invisible unless asked about.

| Control | |
|---|---|
| **Intake** | Explicit confirmation: *"I hold or control the rights to these photographs and may authorise derivative video."* Plus a free-text field for uncertainty |
| **Uncertainty is a stop condition** | "A photographer took them" without written derivative rights → production does not start. We ask them to obtain it |
| **Suggested wording** | Provided to the customer to send to their photographer ([33](33-partnership-plan.md)) |
| **Partnership route** | Photographers adopt derivative-rights language in their standard licence — **turning our biggest exposure into a partnership benefit** |
| **Never** | Assume. Proceed on a verbal. Rely on "they'd never sue" |

### Footage, area imagery and AI output

| Asset | Position |
|---|---|
| Generated clips derived from customer photos | Assigned to the customer for property marketing. **Vendor ToS must be checked** for any claim over outputs (E-21, E-23 — grade C, unverified) |
| Area/neighbourhood imagery (VC-7) | **Rights cleared for every image.** No scraped or unlicensed imagery, ever |
| Stock imagery | Only under a licence permitting client deliverables |
| Illustrative portfolio properties | Rights-clear or properly licensed imagery only, and **labelled as illustrative** |

### Music

- Licensed via Epidemic Sound Pro (D-07, E-18). The decisive term is the **perpetual right for
  work completed during the subscription period** plus client sublicensing.
- **Never** editor-bundled music. CapCut grants no rights to its built-in music at any tier
  (E-24) — the most common licensing trap in this category.
- **Never** trending platform audio in a client deliverable.
- **Vrbo cut has no added music at all** (E-04).
- **Required before first paid delivery:** read the full licence. The summary is grade B.

### Voice

- AI voiceover only from a vendor whose terms permit commercial client use.
- **Disclosed as synthetic** (D-13).
- **Never** clone a real person's voice, including the customer's, without explicit written
  consent — and not at all at launch.

### Portfolio permissions

**Separate, explicit, opt-in. Never assumed from the order.** A customer may buy without ever
appearing in our portfolio, and buying does not grant us promotional rights to their property.

### AI vendor terms — the recurring check

| Question | Why it matters |
|---|---|
| Does the paid tier permit commercial client work? | E-21: **Runway's free tier is personal-use only.** Free tiers are unusable |
| Does the vendor claim any rights in outputs? | Would conflict with what we assign to the customer |
| **Does the vendor retain or train on uploaded content?** | **A customer-confidentiality question, not just licensing.** We upload their property photographs |
| Can we delete uploaded content? | Retention obligations |
| What changes on cancellation? | Delivered work must not become a liability |

**Reviewed quarterly and before any vendor change.** Customer-facing disclosure: property
photographs are processed by third-party AI vendors.

---

## 2. Advertising and messaging rules

| Area | Requirement |
|---|---|
| **Truthfulness** | Claims must be truthful and not misleading (E-17). Governed by [21](21-claim-register.md) |
| **Substantiation** | No claim without evidence we could produce on demand |
| **AI disclosure** | Policy, ahead of legal requirement. E-14/E-15 address *sales* by *licensees* and probably do not cover our customers — **we disclose anyway** ([26](26-property-accuracy-rules.md) §6) |
| **Airbnb branding** | **No logo, Bélo, Superhost badge, or AirCover mark. No implied endorsement.** Descriptive word use only, within their stated exceptions (E-13). **Verify §2 of their guidelines before publishing** |
| Other platform marks | Same principle |
| **Commercial email** | Accurate headers, functional unsubscribe honoured promptly, physical address, no harvested addresses. **Rules differ by jurisdiction — read the primary sources before the first marketing send (V-2)** |
| Platform messaging | Read each channel's rules before any outreach. **We do no cold outreach at launch** ([16](16-sales-playbook.md) §2) |

---

## 3. The order record — one authoritative document

**One record per order, holding everything, and it is what governs if there is ever a dispute.**

| Field | Source |
|---|---|
| Customer, organisation, contact | Form |
| Property name and location | Fact sheet |
| **Accepted scope** — package, exact file list, formats, lengths | [14](14-offer-specification.md) |
| **Price**, add-ons, total | [15](15-financial-model.md) |
| **Deadline**, and that it counts from complete assets | Confirmation message |
| **Assets** — filenames, hashes, date received | Intake |
| **Property facts** — the signed fact sheet, as signed | Customer |
| **Approvals** — rights confirmation, owner authority, portfolio permission | Customer |
| **Revision policy** and rounds used | [14](14-offer-specification.md) §4 |
| **Rights granted** to the customer | Below |
| Review records — Gate 1 and Gate 2, reviewer, timestamp | [26](26-property-accuracy-rules.md), [27](27-quality-rubric.md) |
| Production metadata — models, settings, attempts, source mapping | [22](22-creative-concepts.md) |
| Payment, refund, dispute history | Stripe + order record |

**If it is not in the order record, it was not agreed.** This is the single control that makes
scope disputes resolvable rather than a memory contest.

### Customer agreement — key terms

*Draft. Requires legal review before use.*

| Term | Position |
|---|---|
| **Rights granted** | Perpetual, worldwide, non-exclusive right to use the deliverables to market the property named in the order, including in paid advertising |
| Rights retained | We retain the right to use *illustrative* work only; client property requires separate portfolio permission |
| Customer warranties | They hold or control rights to supplied assets; they have authority to market the property; the facts they supply are accurate |
| **Our warranties** | Delivery to the written spec by the agreed date; human accuracy review before delivery |
| **Explicit non-warranty** | **No warranty as to bookings, occupancy, revenue, reach, ranking, or acceptance by any platform** (D-05) |
| Liability cap | Limited to the fees paid for the order. **Requires legal review** |
| Revisions | One round, 7 days, categories per [14](14-offer-specification.md) §4 |
| Refunds | [35](35-customer-operations.md) §5 |
| Asset retention | Source assets deleted 90 days after delivery unless asked to keep |
| AI disclosure | Deliverables produced with AI assistance and human review; assets processed by third-party vendors |
| Termination | Either party; work delivered is paid for; undelivered work refunded |

### Tax and entity — jurisdiction required

**Cannot be answered here.** These need the operating jurisdiction and a professional:

- Business entity choice and liability implications
- Sales tax / VAT on digital services **and on cross-border sales to customers in other
  jurisdictions** — the most commonly missed item for a solo digital business
- Income tax treatment and contractor classification
- Whether any professional licensing applies to property marketing in a given state
- Insurance: professional indemnity, and whether it is worth carrying at this revenue

**Flagged for the day-1–5 verification block** ([43](43-launch-plan.md)).

---

## 4. Security and access

### Account ownership

Every account — domain, hosting, payment, email, storage, AI vendors, social — is registered to a
business email the founder controls. **No account under a contractor's personal address. No
shared logins.**

### Role-based access

| Role | Access |
|---|---|
| Founder | Everything |
| **Contractor** | **Per-order folder only, expiring.** Shortlisted assets, storyboard, fact sheet. **No customer list, no payments, no email, no social accounts** |
| Agents / automation | Scoped API access only, no credentials with spending or sending authority ([39](39-data-and-agent-architecture.md)) |
| Partners | No system access at all |

### Secrets

- A password manager. Unique passwords everywhere. MFA on every account that supports it.
- API keys in environment variables, **never in code, never in a document, never in a prompt**.
- Keys scoped to minimum permissions; rotated quarterly and on any contractor offboarding.
- **No secret is ever pasted into a model prompt or a shared folder.**

### Preview and delivery permissions — the one that bites

| Rule | |
|---|---|
| **Delivery links are per-customer and expiring.** Never a public folder | A public link is a public link forever, and it is indexed |
| **No customer asset in a publicly listable bucket** | The single most common way small studios leak client material |
| Previews are unlisted and expiring | |
| **Never** a folder containing multiple customers' assets, shared with one of them | |
| Portfolio hosting is separate from delivery storage | |

### Log redaction

Logs and error reports must never contain customer email addresses, property addresses, payment
details, API keys, or asset URLs. **If an agent or tool logs a customer message, it is redacted
before storage** ([39](39-data-and-agent-architecture.md)).

### Contractor offboarding — same day

1. Revoke every folder and tool access **the same day**.
2. Rotate any shared credential.
3. Obtain written confirmation that customer assets have been deleted.
4. Remove from all channels.
5. **Pay them promptly.** An unpaid former contractor holding customer material is a risk created
   entirely by us.

### Incident response

| Incident | Response |
|---|---|
| Customer asset exposed publicly | Remove immediately. **Notify the customer the same day.** Determine scope. Document |
| Credential compromised | Rotate immediately. Review access logs. Notify if customer data was reachable |
| Contractor misuse of assets | Terminate, demand deletion, notify the customer |
| **Platform contacts a customer about our media** | Full cooperation. Provide provenance records. Refund. **Re-review every video made with the same technique** ([26](26-property-accuracy-rules.md) §7) |
| Vendor breach affecting uploaded assets | Notify affected customers with what we know and what we do not |

---

## 5. Verification queue

Blocking items before the first paid order:

| Priority | Item |
|---|---|
| **P0** | Lawyer review: customer agreement, liability cap, rights language |
| **P0** | Accountant: entity, sales tax/VAT on digital services including cross-border |
| **P0** | Read the Epidemic Sound licence in full (E-18) |
| **P0** | Read the selected AI vendor's ToS: commercial use, output rights, **training on uploads** |
| **P1** | Read Airbnb Trademark Guidelines §2 (E-13) |
| **P1** | Read commercial email rules for every jurisdiction we send to (V-2) |
| **P2** | Insurance quote for professional indemnity |

## 6. Acceptance criteria

- [ ] Rights confirmation on 100% of orders before production
- [ ] Zero orders started on unclear rights
- [ ] Zero customer assets in a publicly listable location — **verified by actually checking**
- [ ] Every delivery link expiring and per-customer
- [ ] MFA on every account that supports it
- [ ] No secret in any document, prompt, or repository
- [ ] Contractor access per-order and expiring; revoked same-day on offboarding
- [ ] Customer agreement reviewed by a lawyer before the first paid order
- [ ] Vendor ToS reviewed quarterly, with the date recorded
