# 47 — V-0 Verification Worksheet

**For a human with a browser. It cannot be done by the agent.**

## Why this exists

Nine claims in [02](02-evidence-ledger.md) are grade **B** — sourced from secondary reporting
because their primary sources are unreachable from this environment. Verification was attempted
and failed comprehensively:

| Route tried | Result |
|---|---|
| `WebFetch` → airbnb.com, help.vrbo.com | `EGRESS_BLOCKED` |
| `WebFetch` → airbnb.co.uk (regional) | `EGRESS_BLOCKED` |
| `WebFetch` → stripe.com, support.google.com, facebook.com, epidemicsound.com | `EGRESS_BLOCKED` |
| `WebFetch` → web.archive.org | Blocked |
| `curl` via Bash → any host, incl. `example.com` | `403 CONNECT tunnel failed` |

**Bash has no web egress in this environment, and WebFetch is blocked for every commercial
domain. Only WebSearch works, and it returns summaries, not source text.** A future session
should not spend time retrying these — the block is at the proxy, not the tool.

So: **this is yours to do.** Budget 30–40 minutes. It unblocks everything else.

## How to use this

1. Open each URL in a normal browser.
2. Answer the question in the **"What to find"** column.
3. Write the answer in the **Result** column and date it.
4. If an answer differs from **"We currently believe"**, do the action in **"If different"**.
5. When done, update [02](02-evidence-ledger.md): change the grade from **B** to **A**, and move
   the affected claims out of the ⏳ list in [21](21-claim-register.md).

---

## P0 — Decision-critical. Do these first.

### V-0.1 — Airbnb: can hosts upload video to a listing?
- **URL:** `airbnb.com/help/article/546` (Content Policy) and `airbnb.com/help/article/2895`
  (Ground Rules for Hosts). Also just open your own listing editor and look for a video upload
  control.
- **What to find:** Is there *any* way to put a video file in the listing gallery? Photos only?
- **We currently believe:** No host video on listing galleries; photos only, except Luxe and some
  API-connected professional accounts (**E-01**).
- **If different:** 🚨 **Stop everything.** This is the finding the whole strategy rests on.
  Re-run [12](12-positioning.md) and [08](08-segment-selection-matrix.md) before any other work.
  It would be good news — a much larger market — but the positioning would be wrong.
- **Result:** ________________________  Date: __________

### V-0.2 — Airbnb: AI-altered listing media and enforcement
- **URL:** same two articles.
- **What to find:** The exact wording on AI or digitally edited media. Does Airbnb say it will
  require removal of content that edits flaws, hides damage, or adds amenities not present? What
  is the enforcement ladder — warnings, suspension, cancelled reservations, refunds from payouts?
- **We currently believe:** All of the above (**E-11**). This is the basis of
  [26](26-property-accuracy-rules.md) and ad concept AD-3.
- **If different (softer than we think):** AD-3's copy must be rewritten or dropped. The accuracy
  rules stay regardless — they are also general advertising law (**E-17**).
- **Copy the exact sentence**, because we quote this to customers:
- **Result:** ________________________  Date: __________

### V-0.3 — Vrbo video guidelines
- **URL:** `help.vrbo.com/articles/Vrbo-video-guidelines`
- **What to find:** Min/max duration · accepted formats · **is added music prohibited?** · **are
  on-screen contact details prohibited?** · the cap on area/neighbourhood footage · number of
  videos per listing.
- **We currently believe:** 15s min, 60s preferred, 2min max; mp4/mov; **added music is a common
  rejection reason**; no contact details in frame; ~20% area footage cap (**E-03–E-07**).
- **If different:** the Vrbo cut spec in [14](14-offer-specification.md) changes, and so does
  D-06 — the music-free cut is one of our few real differentiators.
- **Result:** ________________________  Date: __________

### V-0.4 — Meta: is a daily budget a hard cap?
- **URL:** Meta Business Help Centre, search "daily budget" and "account spending limit".
- **What to find:** How much over a daily budget can Meta spend in one day? Is there a weekly
  limit? Where exactly do you set an **account spending limit**?
- **We currently believe:** Daily budgets are **not** caps — up to 1.75× daily in a single day,
  7× daily over a rolling week; only an account spending limit is a true ceiling (**E-34**).
- **If different:** doesn't matter much — **set the account spending limit anyway** before any
  campaign (D-09). This is a money-safety control, not an optimisation.
- **Do now while you're there:** note the exact click path to the setting.
- **Result:** ________________________  Date: __________

---

## P1 — Before the first paid delivery

### V-0.5 — Epidemic Sound licence
- **URL:** epidemicsound.com pricing page, then the **full licence text** (not the summary).
- **What to find:** Does the Pro tier permit client work and paid ads? Can you sublicense to a
  client? **What happens to already-delivered work if you cancel?**
- **We currently believe:** Pro ≈ $16.99/mo annual; perpetual right for productions completed
  during the subscription period; client sublicensing under $50M revenue (**E-18**).
- **If the perpetual term is absent:** ⚠️ **Do not use them.** Every video ever delivered would
  become a liability the day you stop paying. Switch to Artlist and read its terms the same way.
- **Result:** ________________________  Date: __________

### V-0.6 — AI video vendor terms (whichever you pick)
- **URL:** the vendor's Terms of Service — Kling and/or Runway.
- **What to find, in order of importance:**
  1. **Does the vendor train on, or retain, uploaded content?** ← this is a *customer
     confidentiality* question, not just licensing. You upload their property photos.
  2. Does the paid tier permit commercial client work?
  3. Does the vendor claim any rights in the outputs?
  4. Can you delete uploads?
- **We currently believe:** paid tiers permit commercial use; Runway's **free tier is personal-use
  only** (**E-21, E-23**). Retention/training terms are **unknown**.
- **If they train on uploads with no opt-out:** that needs disclosing to customers, or pick a
  different vendor. See [38](38-rights-and-security.md).
- **Result:** ________________________  Date: __________

### V-0.7 — Airbnb trademark guidelines
- **URL:** Airbnb brand/trademark guidelines, **section 2** (permitted uses of the word "Airbnb").
- **What to find:** Exactly how may a third party use the word "Airbnb" descriptively? What is
  forbidden?
- **We currently believe:** no logo, no Bélo, no Superhost badge, no implied endorsement;
  limited descriptive word use only (**E-13**).
- **Affects:** every page of the site and every ad.
- **Result:** ________________________  Date: __________

### V-0.8 — Stripe pricing
- **URL:** stripe.com/pricing
- **What to find:** US online card rate, international surcharge, currency conversion fee,
  dispute fee.
- **We currently believe:** 2.9% + $0.30; +1.5% international; +1% conversion; $15 dispute
  (**E-25**).
- **Then:** put the real figures into `tools/financial_model.py` and re-run it.
- **Result:** ________________________  Date: __________

---

## P2 — Before mentioning it to anyone

### V-0.9 — Booking.com partner video
- **URL:** partner.booking.com help.
- **What to find:** Is partner video upload only for **location verification**, or is there a
  marketing video placement?
- **We currently believe:** verification only — must be recent, unedited, showing street sign →
  exterior → path → interior (**E-09**).
- **If different:** a new distribution channel opens and [06](06-two-marketing-systems.md)'s
  channel map needs updating.
- **Result:** ________________________  Date: __________

---

## Non-web blockers — same urgency, different route

| Item | Who | Why it blocks |
|---|---|---|
| Customer agreement + liability cap review | A lawyer | First paid order ([38](38-rights-and-security.md)) |
| Entity choice, sales tax / VAT on digital services **including cross-border** | An accountant | First paid order |
| **How these two are funded** | You | **OD-2** — the $400 ceiling in [15](15-financial-model.md) does not cover them. See [46](46-open-decisions.md) |

---

## When you've finished

1. Update the grades in [02](02-evidence-ledger.md) — B → A for everything confirmed.
2. Release or delete the ⏳ claims in [21](21-claim-register.md).
3. Re-run `python3 business/tools/financial_model.py` with real Stripe figures.
4. If V-0.1 contradicted E-01 — **stop and re-plan.** Nothing else matters until that is settled.
5. Then V-1: the ten practice videos ([42](42-validation-plan.md)).
