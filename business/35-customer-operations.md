# 35 — Customer Operations

Onboarding, exceptions, complaints, refunds, and distribution support.

## 1. The Property Fact Sheet

**The single source of truth for every property fact** ([26](26-property-accuracy-rules.md),
[39](39-data-and-agent-architecture.md)). Eight questions, about five minutes. Nothing appears on
screen in a video that is not on this sheet.

| # | Question | Why it is here |
|---|---|---|
| 1 | Property name and location (town, not full address) | Captions, end cards |
| 2 | **Exact sleeping arrangement**: bedrooms, bed types, sofa beds, bunk rooms, total capacity | The named refund trigger (E-12). **Bunk rooms and sofa beds must be declared** |
| 3 | Bathrooms: how many, en-suite or shared | Frequently asked, frequently overstated |
| 4 | **Amenities that are actually present** — tick list plus free text | Nothing gets shown that is not ticked (E-11) |
| 5 | **Measured** distances/times to the 3 nearest things guests care about | "Near the beach" is not a fact. "8 minutes on foot" is |
| 6 | Who is this property best for? Who is it *not* for? | The messaging framework ([10](10-traveler-decisions-and-property-messaging.md)) |
| 7 | **Access and accessibility**: stairs, steps, thresholds, parking, lift | Highest-harm category. Asked explicitly, never inferred |
| 8 | **Anything that must not be shown or implied** | The field competitors do not have. Customer names their own boundaries |

Plus two confirmations, not questions:
- **Rights:** "I hold or control the rights to these photographs and may authorise derivative
  video." *(free text if uncertain — uncertainty is a stop condition)*
- **Authority (PM orders):** "I am authorised to market this property in this way."

---

## 2. Onboarding

| Step | Timing | Who |
|---|---|---|
| Payment clears | Day 0 | Customer |
| Upload link + fact sheet sent automatically | Day 0, immediately | System |
| Assets and fact sheet received | Day 0–3 | Customer |
| **Delivery date confirmed in writing** | Within 4 business hours of complete assets | Founder |
| Production starts | On confirmation | Founder |

**The clock starts on complete assets, not on payment.** Stated before payment, on the
confirmation page, and in the onboarding email. This is the single most important expectation in
the business ([13](13-consumer-psychology-and-sales-method.md) §9) and the one most likely to be
forgotten under pressure (see C-11 in [18](18-conversation-examples.md)).

---

## 3. Exception handling

### Missing or insufficient assets

| Stage | Action |
|---|---|
| Day 2 | One reminder. Friendly, specific about what is missing |
| Day 5 | Second reminder, stating the order will park |
| Day 7 | **Order parks.** "Your order is paid and waiting. No deadline pressure from me — send the photos when you're ready and I'll pick it up." |
| Day 30 | One final note. Offer a full refund if they would rather not proceed |
| Day 90 | **Offer a full refund proactively.** Holding money indefinitely for undelivered work is not acceptable |

**We never nag.** Three contacts total over 90 days, then we hand the money back.

### Unclear brief

Ask one specific question, not "can you clarify?" If the fact sheet is thin, ask about the one
field that blocks production. **Never fill the gap ourselves and never let a model fill it**
([39](39-data-and-agent-architecture.md)).

### Missing approvals (PM orders)

Production does not start on a property without its signed fact sheet and owner authority. Other
properties in the batch continue; the blocked one waits.

### Generation failures

Per [24](24-production-workflow.md): budget cap at 3× estimated cost → escalate → consider the
template-motion fallback. **The customer is told which method was used** if the fallback is used.

### Scope changes

The decision tree in [14](14-offer-specification.md) §4. **Always name the category and always
offer the in-scope alternative** before quoting (C-12).

### Late delivery

| Rule | |
|---|---|
| **Tell them before the date, not after** | The difference between a professional and a disappointment |
| Give a new date, once, and meet it | A second slip is a different conversation |
| **Proactive partial refund for a material delay** | Not because it is demanded — because they paid for a date they did not get (C-11) |
| Log the cause | A late delivery is a process failure to fix, not just an apology to make |

---

## 4. Complaints

**The diagnostic question comes first, always:**

> "Tell me what's wrong — and specifically, is it not to your taste, or is something in there not
> accurate to the property? Those go different ways."

| Type | Route | Cost to customer |
|---|---|---|
| **Accuracy error** | [26](26-property-accuracy-rules.md) escalation. Free fix, prioritised, logged as a **gate escape**, gate reviewed | $0 |
| **Spec miss** (a file missing or wrong format) | Category 1. Free fix within 1 business day | $0 |
| **Technical defect** (warping, flicker, artifacts) | Category 1 + [27](27-quality-rubric.md) gate review | $0 |
| **Taste disagreement** | Included revision round | $0 (within the round) |
| **Wants something different** | Category 3/4/5/6 — named, priced, with an in-scope alternative offered | Quoted |
| **Late delivery** | §3 above | Proactive partial refund |

### Complaint principles

1. Answer the actual complaint before explaining anything.
2. **Own it in one sentence.** No paragraph of apology — it reads as anxiety, not accountability.
3. Fix it before discussing whose fault it was.
4. **Never argue about an accuracy defect.** Fix, refund if unfixable, log.
5. Log the cause, not just the resolution. A complaint you only apologise for will recur.

---

## 5. Refunds

| Situation | Position |
|---|---|
| **Accuracy defect we cannot fix** | **Full refund. No argument, no delay.** |
| Spec miss we cannot fix | Full refund |
| Material late delivery | Partial refund, offered by us, unprompted |
| Technical defect we cannot fix in 2 attempts | Full refund |
| Taste disagreement after the revision round is used | **No refund.** The scope was met. Offered kindly, with the option of a paid new direction |
| Customer changed their mind before production | **Full refund, no questions** |
| Customer changed their mind after delivery | No refund. Work was done to spec |
| Assets never supplied, 90 days | **Full refund, offered by us** |
| Chargeback filed | Respond with the written scope, the delivery record, and the review records. Do not retaliate |

### Rules

- **Only the founder approves a refund.** Never an agent (D-15).
- **Every refund is coded to a cause** ([41](41-measurement-definitions.md)) — accuracy, quality,
  delay, scope, mind-changed, other.
- Refunds are paid within 2 business days of approval.
- **Refund rate over 15% is a tripwire**, not a cost of doing business
  ([15](15-financial-model.md) §11) — the product or the sales promise is wrong, and selling
  more will make it worse.

---

## 6. Distribution support — a delivered video is not a used video

**The uncomfortable truth:** a customer who receives seven files and posts none of them got
nothing, whatever we delivered. This is the most likely quiet failure in the business, and it
would show up as low repeat purchase rather than as a complaint.

### What we do

| We do | We do not |
|---|---|
| Name each file by destination | Post to their accounts |
| Provide the **Where To Post This** one-pager | Manage their channels |
| Say which file to post first, and why | Schedule anything |
| Provide caption and copy suggestions they can edit | Write their entire content calendar |
| State each platform's limits plainly | Guarantee any platform accepts anything |
| **Ask at day 21 whether they published** | Chase them about it |

**Production and distribution are separate services.** We sell production. Distribution support
is included as guidance because it is cheap for us and materially changes whether the product is
used.

### The "Where To Post This" one-pager

> **Your files, and where each one goes**
>
> **`01-reels-hook-a.mp4` / `02-reels-hook-b.mp4`** — Instagram Reels, TikTok. Vertical, captions
> burned in. Two different openings: post one, and if it does nothing, post the other the
> following week rather than reposting the same thing.
>
> **`03-feed-square.mp4`** — Instagram feed, Facebook. Square.
>
> **`04-web-hero.mp4`** — your booking site, near the top. Wide.
>
> **`05-web-loop-silent.mp4`** — a header loop. No sound on purpose: autoplay is muted
> everywhere, and a loop with audio just gets blocked.
>
> **`06-vrbo-cut.mp4`** — your Vrbo listing. **No music and no text overlay, deliberately** —
> Vrbo rejects added music and any on-screen contact details. Upload it through your Vrbo
> property page.
>
> **`07-google-profile.mp4`** — Google Business Profile, if the property has one. Under 30
> seconds and under 75MB, which is what they want.
>
> **`captions.srt`** — if you'd rather use platform captions than the burned-in ones.
>
> **Not for Airbnb.** Airbnb doesn't accept host-uploaded video on listing galleries. You *can*
> send a video to a guest in the message thread after a booking is confirmed — that's what an
> arrival video is for, if you ever want one.
>
> **If you post one thing:** `01-reels-hook-a.mp4`.

### Confirming usage

At day 21 we ask once: *"Did you end up posting any of them? Genuinely useful for me to know, and
no wrong answer."*

**What we do with the answer:**
- "Yes, and X happened" → recorded as an **observation**, with attribution caveats. **Never
  converted into a claim** (D-05, [21](21-claim-register.md)).
- "No" → the more valuable answer. Find out why — wrong format, no time, unsure what to say. That
  is product feedback about the deliverable, not about their discipline.

**We never attribute a booking change to the video.** If a customer says "we got three bookings
after posting it," the correct response is genuine pleasure and no causal claim, in our records
or in our marketing.

---

## 7. What the customer sees vs. what the founder sees

| Stage | Customer sees | Founder sees |
|---|---|---|
| Order | Confirmation, upload link, fact sheet | Order record, capacity check |
| Waiting | One reminder at 48h | Parked-order queue, days elapsed |
| Production | Confirmed date, one substantive update | Time log, attempt log, generation spend |
| Review | Nothing | Gate 1 and Gate 2 records |
| Delivery | Files, guide, delivery message | Time log closed, metadata archived |
| Revision | Acknowledgement, category if relevant | Revision counter, minutes spent |
| After | One feedback/referral ask, one usage question | Repeat trigger, lost/won coding |

**Deliberately invisible to the customer:** the attempt log, the generation cost, and the review
scores. They are our operating data, not reassurance theatre. **Deliberately visible:** the
accuracy checklist itself, published, so the discipline is verifiable even though the individual
scores are not.

## 8. Acceptance criteria

After 10 orders:
- [ ] 100% have a signed fact sheet and rights confirmation before production
- [ ] 100% had a delivery date confirmed in writing from complete assets
- [ ] Median first response under 4 business hours
- [ ] Zero orders delivered late without advance notice
- [ ] Every complaint diagnosed before being resolved
- [ ] Every refund coded to a cause
- [ ] Day-21 usage question asked on 100% of delivered orders
- [ ] Zero booking claims recorded, internally or externally
