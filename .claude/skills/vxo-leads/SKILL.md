---
name: vxo-leads
description: VXO funnel stage 1–3. Find the hottest US DTC product brands for VXO films, score them, and draft a personal first message that offers free concept frames. Nothing is ever sent without the owner's explicit approval. Use when the owner asks for leads, prospects, outreach, DMs, or "find me a hot lead".
---

# VXO leads: hot lead → first message → free frames → sale

**The owner's funnel (2026-10-09):**
1. Find a VERY hot lead.
2. Message them: do they want a few free concept images?
3. Either they buy straight away, or they buy after seeing the frames.
4. The owner then brings the brand, product name and product photo, and the `vxo-film` skill takes over.

**Hard rules (these never change):**
- **Never send anything** (email, DM, form, comment) without the owner's explicit "send" for that exact message.
- Use public business contacts only. Never personal phone numbers or home addresses. No scraping behind logins, and no logging into Instagram.
- Email follows CAN-SPAM: real sender, the business address footer, and an honest opt-out line on any follow-up.
- No fake claims, no fake clients, no invented stats. The only offer is free concept frames.
- Read `research/ai-video-reels/lab/LESSONS.md` first.

## 1. What "very hot" means (score out of 100)
| Signal | Points | How to check (public) |
|---|---|---|
| Running paid ads right now | 30 | Meta Ad Library, US, active, brand name. More active ads with few or weak videos scores higher. |
| Creative need | 20 | The share of video among their ads is low, the videos are static or slideshows, or they reuse the same creative for weeks. |
| Momentum | 15 | A product launched in the last 60 days (check Shopify `/products.json` dates), a new collection, press, or a funding round. |
| Seasonal pressure | 10 | A BFCM or holiday gifting fit, or a launch date on the calendar. |
| Budget proxy | 10 | Price points × number of SKUs × ad volume. Target the $1–20M revenue band. |
| Founder-led and reachable | 10 | The founder is visible and a public business contact exists. |
| Hiring for creative or content | 5 | Job posts for a content creator, UGC or video role. |

HOT = 70 or above. Only HOT leads reach the owner, five at most per day, best first.

## 2. Where to look
- Meta Ad Library: categories beverage, fragrance, candles, skincare, jewelry, coffee, snacks, home, pet.
- Shopify stores with recent launches.
- "New product" posts on brand IG, read through public web pages only.
- ProductHunt, Kickstarter and Indiegogo projects with an upcoming launch.
- Trade press: BevNET, Food Dive, Glossy, Modern Retail and similar.
- Existing lists: `research/ai-video-reels/prospects/HOT_NEW_30.md`, `HEAT_50.md`, `us-*.md`. Never re-pitch a brand that is already listed unless its status is updated.

## 2b. Deep lead research: a dossier BEFORE any message (owner rule, 2026-10-09)
A lead is never messaged from a score alone. For each candidate, write a dossier in `research/ai-video-reels/leads/dossiers/<brand>.md`:
1. **Why they are hot, in one sentence with evidence:** for example "launched X on 9/28, running 14 static ads, zero video, BFCM in 6 weeks".
2. **The business:**
   - what they sell, their hero product and price;
   - estimated size, channels (DTC/Amazon/retail) and where they advertise;
   - their current creative: what works, what's weak, how long their winning ads have run.
3. **The person:**
   - who decides (founder or marketing lead);
   - their public voice from interviews, posts and podcasts;
   - what they care about (taste, speed, ROAS, brand) and what they'd fear in an AI studio.
4. **Fit and red flags:** budget proxy, founder-led, any legal or claims risk, recent bad news, already working with an agency.
5. **The buying path:**
   - Which ONE film would make them buy now?
   - Which proof do they need (frames, a sample in their niche, a price anchor)?
   - What would make them buy AGAIN (a monthly "Season" cadence, seasonal drops, new SKUs, ad fatigue every ~4 weeks)?
6. **The angle for the first message.**

**Filter hard.** Only leads whose dossier shows a clear reason to buy NOW go to the owner. Rank them, and send the owner only the very hottest (best 1–3 per day, never more than 5).

## 3. The first message (DM or email): rules from doc 63
Full research, red-teamed examples and objection replies: `skills/ad-director/references/marketing/63-outreach-that-gets-replies.md`. It supersedes the old template here, doc 28 §5, doc 34 §4.2 and the DTC templates in `launch/outreach.md`.

**Instagram facts that shape everything:** a non-follower gets **one text-only message** until the recipient accepts. It lands in Requests, and a brand account's DMs are read by a social or CX person. So the DM must stand alone, carries no image or link, and **every follow-up goes by email**.

**Channel order:**
1. The founder's own public business account (IG or LinkedIn), sent by the owner by hand.
2. The brand IG DM, written so it can be forwarded.
3. The public brand inbox, with the founder's name in the first words.

Sequence: DM on day 0, email on day 1. Never guess an email address, use a form or pitch in a comment.

**Every first message:**
1. Names the sender in line 1 ("Itamar from VXO").
2. Makes ONE observation a customer could see. **Never** use back-end data: no `products.json` dates, no hidden or unreleased SKUs (tags such as `redirect-to-404`, `hidden`, `draft`, or `available: false`), no Motion or Ad Library counts, no job posts.
3. Gives the film idea in 1–2 visual sentences, with a turn the product causes. The idea earns the reply, not praise.
4. Says "AI" once, after the idea, next to what stays real (the real product shot or proof, no AI people).
5. Makes the offer in their words: "5 free stills of it, on your real [product]". No call, no cost.
6. Ends on a two-yes CTA, both options free and equally easy.
   - Every product the message names (both CTA options included) must pass `python3 skills/ad-director/scripts/research/products_check.py <domain> "<title words>"` with no HIDDEN, FINAL, MARKDOWN, OOS or PAGE!=200 flag, on the day it is drafted **and again on the send morning** (2026-10-10: a queued CTA, Little Beast's Miami Vice onesie, went on sale overnight). A brand-wide standing promo that was already there when the lead was scored (e.g. Cuddle Clones' pajama offer) is noted in the dossier, not a blocker.
7. Uses no superlatives ("best", "genius", "hero"), no "I came across", no exclamation marks, no em-dash chains.
8. Length: a DM is 35–55 words; an email body is 50–90 words, with a 1–4-word subject naming their thing.
9. Has no link, image or price in touch 1.
10. Email only: carries the footer (real name, VXO, a **real postal address**, and `This is a one-to-one business pitch. Reply "stop" and I won't email again.`). **No email is sent while the address is a placeholder.**
11. Is different from every other draft that day (no shared sentences).

**Before the owner's "send":** run the doc 63 §7.1 checklist:
- the Ad Library is checked by hand;
- the product is public;
- no stale or back-end data appears in the message;
- the sender profile is real;
- the send slot is Tue–Thu, 8–10 am in their time zone;
- the send is logged the same day.

Limits: about 10 new DMs and 15 new emails a day, by hand, spaced out.

## 3b. Follow-ups: 3 touches, email only, each one owner-approved
Reply in the same email thread (never a fake "Re:"). Each touch is its own approval ("send #N-FU1"). **Stop at the first reply of any kind**, and honour any "stop" or "no" the same day (CAN-SPAM: within 10 business days at most). Every follow-up keeps the footer.

| Touch | Day | Words | New reason to reply | Spend |
|---|---|---|---|---|
| FU1 | +4 | ≤ 45 | A second film idea for the same product, ending in a two-yes ("this one, or the first?") | 0 |
| FU2 | +9 | ≤ 40 | One still from their public product photo, attached as a single JPG and marked "AI concept, just for you" | ~$0.05–0.30, **only with the owner's approval** (frames-only mode); otherwise send FU2-text (how the stills protect their product) |
| FU3 | +16 | ≤ 35 | A real date on their calendar, plus a two-yes on timing ("this week, or check back for [next season]?") | 0 |

Rules:
- Never send "just checking in", guilt or fake deadlines.
- Never post or share a frame made before they say yes.
- After FU3, log "no reply" and set one check-in at their next real launch.
- When they reply, use the doc 63 §6 objection replies (price, in-house AI, "AI looks fake", "send examples", "who else have you worked with", "not now"), then docs 28 §6–8 and 34 for the call and the close.

## 4. Output every run
Write `research/ai-video-reels/leads/YYYY-MM-DD.md` containing:
- the ranked table (brand, category, score with its breakdown, the evidence URLs, the public contact, the suggested tier);
- the DM and the email draft per lead;
- the status line `NOT SENT — awaiting owner approval`.

Append to `research/ai-video-reels/leads/PIPELINE.md`, one line per lead:

`brand · score · date found · status (found / approved / sent / replied / frames sent / won / lost) · next action`

## 5. When a lead says yes to the frames
Hand over to `vxo-film` in **frames-only mode**: 5 concept frames, a total cost of about $0.30–1.50, a one-line idea per frame and the planned film structure. The owner approves the frames before they're sent.
