# 32 — Search, Email & Remarketing

## Part 1 — Search

### Evidence limitation

**No keyword volume data was obtained for this project.** No Keyword Planner access, no
third-party volume tool. Everything in this section is **intent-structure reasoning, not verified
demand.** Any specific search-volume figure appearing here later must carry an E-ID.

Registered as verification task **V-3**: pull real volume and competition data before spending
anything on search ads.

### Intent categories

| Intent | Example queries | Buying intent | Our play |
|---|---|---|---|
| **Learning** | "how to market an airbnb", "vacation rental marketing ideas" | Low | Content, no ads |
| **Comparing** | "airbnb video vs photos", "best ai video tool for real estate" | Medium | Content |
| **Buying** | "property video service", "airbnb listing video service", "vacation rental videographer" | **High** | Content now; ads later |
| **Solving a production problem** | "how to add video to vrbo", "can you put a video on airbnb listing" | Medium, and **highly qualified** | **Our best content opportunity** |
| **Seeking a specialist** | "vacation rental video production" | High | Content, directories |

### The asymmetric opportunity

**"Can you add video to an Airbnb listing?"** is a question with a clear factual answer (E-01)
that most of the category answers evasively, because answering it honestly undermines what they
are selling.

That makes it the single best content asset available to us:
- Genuine informational intent — someone is actually asking.
- The correct answer is short, checkable, and useful.
- Answering it honestly demonstrates the thing we claim to be (accurate, not overselling).
- **It naturally qualifies:** anyone who reads "Airbnb won't display it" and *still* wants video
  has self-selected into Q2 ([08](08-segment-selection-matrix.md)).

### Recommended search content — three pages, written once

| Page | Intent | Why it earns its place |
|---|---|---|
| **"Can you add video to an Airbnb listing?"** | Production problem | The asymmetric opportunity above. Answer honestly and completely, including what to do instead |
| **"How to add video to a Vrbo listing"** | Production problem | E-03–E-07 — real, specific, checkable requirements most write-ups get wrong (especially the music rule) |
| **"What a property video costs in 2026"** | Comparing | Publish the real ranges from E-31 including competitors' options. Honest comparison beats a sales page |

**Not recommended:** thin comparison pages, "best X tools" listicles, or AI-generated volume
content. They cost trust in a small market where our ICP talks to each other.

### Search ads — wait

**Recommendation: no search ads until 90 days.** Reasons:
1. No volume data (V-3) — we would be bidding blind.
2. High-intent clicks are expensive and would land on an unvalidated page.
3. A $300 Meta test teaches the same message lesson for less
   ([31](31-experiment-design.md)).

**Revisit when:** conversion rate from qualified lead to order is measured, the landing page has
converted at least 5 real orders, and monthly contribution margin can absorb a $300 test without
touching the cash buffer.

---

## Part 2 — Email lifecycle

### Separation of transactional and marketing

**These are different systems with different rules, and conflating them is both a compliance
problem and a trust problem.**

| | Transactional | Marketing |
|---|---|---|
| Trigger | An order event | Time or behaviour |
| Consent | Implied by the transaction | **Explicit opt-in required** |
| Unsubscribe | Not applicable — they need these | **Required, functional, honoured immediately** |
| Examples | Order confirmation, asset request, progress, delivery, revision, invoice | Newsletter, seasonal reminder, new-service announcement |
| **Rule** | **Never put marketing content in a transactional email.** A delivery message that ends with an upsell converts the best moment in the relationship into an advertisement | |

### Acquisition

| Source | Consent |
|---|---|
| Qualification form | Consent for **this enquiry**. Separate unticked checkbox for anything else |
| Customer | Transactional automatically. Marketing only with a separate opt-in |
| Content download | Explicit, at the point of download, stating what they will receive |
| **Never** | Scraped addresses, purchased lists, "we found your listing" outreach ([16](16-sales-playbook.md) §2, V-2) |

### Segmentation

| Segment | Definition | Cadence |
|---|---|---|
| Enquired, not ordered | Qualified, no purchase | 2 messages maximum, then stop |
| Declined by us | We said no | **No marketing.** One useful resource, if promised |
| Customer, one order | Delivered | Transactional + opt-in seasonal |
| Customer, repeat | ≥2 orders | Opt-in, low frequency |
| Partner | [33](33-partnership-plan.md) | As agreed |
| **Suppressed** | Unsubscribed, bounced, complained, or asked us to stop | **Never contacted again, by any route** |

### Sequences

**Transactional (always sent):** order confirmation → asset request → asset reminder at 48h →
second reminder at day 5 → delivery-date confirmation → delivery → revision window closing at
day 5 → order closed. Copy: [20](20-brand-voice-and-copy.md).

**Post-enquiry, no order (marketing — 2 messages, then stop):**
1. **Day 4** — the useful thing, not a pitch. "Whether or not you use me, here's the shot
   selection guide."
2. **Day 14** — one line: "Still here if the timing changes. I won't email again about this."
   **And then we don't.**

**Post-delivery (mixed, clearly separated):**
1. Day 3 — transactional: "Revision window closes in 4 days."
2. Day 10 — **ask** for feedback and a referral, once ([20](20-brand-voice-and-copy.md)).
3. Seasonal, opt-in only — timed to *their* pre-season, not our calendar (A-14).

### Expectations and suppression

- Every opt-in states what will be sent and how often.
- Unsubscribe works in one click and takes effect immediately.
- **The suppression list is honoured across every channel**, including partner referrals and ads.
- A complaint is treated as a permanent suppression, not a data point.

**Verification:** commercial email requirements (accurate headers, functional unsubscribe,
physical address, honouring opt-outs within the statutory window) must be read from the primary
source for the jurisdictions we send to, before the first marketing send — **V-2**. These vary by
country and the US, UK and EU rules differ.

---

## Part 3 — Remarketing

### Recommendation: do not run remarketing at launch

**Reasoning, not reflex:**

1. **Audience size.** At a $300 test producing perhaps 100–200 site visitors, most platforms will
   not have a usable audience. Many enforce minimum audience sizes.
2. **Economics.** At a $75 target CAC ([15](15-financial-model.md)) with no LTV assumed (D-12),
   the allowable spend on re-reaching a warm visitor is small. The overhead of building it does
   not pay back at this volume.
3. **Privacy and consent.** Tracking pixels require consent handling that varies by jurisdiction,
   and setting it up properly is not free.
4. **Founder time.** It is a configuration project competing with production hours.

### When to revisit

All three must be true:
- ≥1,000 unique site visitors in a rolling 30 days
- Measured qualified-lead-to-order conversion rate
- Monthly contribution margin ≥$1,500

### The design, for when it is justified

| Element | Spec |
|---|---|
| Audience | Visited the pricing or examples page, did not submit the form, last 30 days |
| **Exclusions** | Anyone who submitted the form · existing customers · **the suppression list** · anyone we declined |
| Sequence | Message 1 (days 1–7): the illustrative library. Message 2 (days 8–21): the accuracy checklist. **Then stop** |
| Frequency | Capped. **A person who has seen our ad fifteen times is being annoyed, not persuaded** |
| **Stopping rule** | Exit on form submission, on 21 days, or on any suppression signal — whichever first |
| Budget | ≤15% of total ad spend |
| Consent | Per jurisdiction, verified first |

**The frequency cap and the 21-day stop are the whole ethical content of this section.**
Remarketing without them is just following people around.

---

## Acceptance criteria

- [ ] Search volume data obtained (V-3) before any search ad spend
- [ ] Three content pages published, each factually checkable
- [ ] Transactional and marketing email fully separated, in different templates
- [ ] Commercial email rules read from primary sources before first marketing send (V-2)
- [ ] Unsubscribe tested end to end, by us, before the first send
- [ ] Suppression list honoured across every channel
- [ ] No remarketing until all three revisit conditions are met
- [ ] Post-enquiry sequence stops at 2 messages, verified in the tool, not by intention
