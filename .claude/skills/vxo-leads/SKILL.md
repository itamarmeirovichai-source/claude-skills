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

## 3. The first message (DM or email), personal, under 60 words
Structure, matching the proven examples in `HOT_NEW_30.md`:
1. One specific compliment on THEIR ad, line or product (shows real attention).
2. One concrete film idea for ONE product, in one sentence, visual and with a twist.
3. "I make AI product films (no shoot)."
4. A yes/yes question: "Want 5 free frames for {product A}, or for {product B}?"

Don't add links in the first message, and don't use "if you're not interested" exits. The portfolio link goes in the first reply.

## 4. Output every run
Write `research/ai-video-reels/leads/YYYY-MM-DD.md` containing:
- the ranked table (brand, category, score with its breakdown, the evidence URLs, the public contact, the suggested tier);
- the DM and the email draft per lead;
- the status line `NOT SENT — awaiting owner approval`.

Append to `research/ai-video-reels/leads/PIPELINE.md`, one line per lead:

`brand · score · date found · status (found / approved / sent / replied / frames sent / won / lost) · next action`

## 5. When a lead says yes to the frames
Hand over to `vxo-film` in **frames-only mode**: 5 concept frames, a total cost of about $0.30–1.50, a one-line idea per frame and the planned film structure. The owner approves the frames before they're sent.
