# 28 · Sales mastery: cold email → reply → call → paid deal

Research brief, 2026-10-08, for the studio's first 50-brand outreach (`scratchpad/outreach/BRIEF.md`, `PROSPECTS_50.md`). It covers the cold-email copy, sending from a personal Gmail, replies, the discovery call, pricing, the contract and the ethics. It does **not** repeat Rourke Heath's playbook in `20-youtube-gapfill.md` §1.1 (the jab-jab-hook, the five-image custom sample, the $2,500 floor, "never quote without the script", the legal-memo answer).

**Evidence.** Most cold-email numbers come from vendors (Lavender, Instantly, Woodpecker, Gong). They sell tools, their samples are B2B SaaS-heavy, and they disagree on baselines, so read them as directional. Books are cited from summaries. YouTube transcripts were attempted with `yt-dlp`; every request returned HTTP 429, even with 45–120 s spacing and exponential back-off, so no transcript is cited (see §10). `[inf]` marks our inference, `[law]` marks a legal point (not legal advice; check with a lawyer before relying on it).

---

## 1. What the data says about cold email (2025–2026)

| Lever | Finding | Source | What we do |
|---|---|---|---|
| Baseline | Average reply rate 3.43 %, top quartile 5.5 %+, top decile 10.7 %+ (Jan–Dec 2025 data) | [Instantly 2026](https://instantly.ai/cold-email-benchmark-report-2026) | Aim for 8–15 % on 50 hand-researched emails `[inf]`: small, relevant lists do better (Woodpecker: campaigns under 50 recipients 5.8 % vs 2.1 % at 1,000+, [Woodpecker](https://woodpecker.co/blog/cold-email-benchmarks/)) |
| Quality lift | Emails graded "A" lift replies from 3.4 % to 4.3 % (231,818 emails) | [Lavender benchmark](https://lavender.ai/blog/the-cold-email-benchmark-report) | Score every email (§2) |
| Length | Optimum 25–50 words, under 75 at most; best campaigns under 80; replies fall sharply above 100 | [Lavender 101](https://lavender.ai/blog/cold-email-101), Instantly, [Gong](https://www.gong.io/blog/do-execs-really-reply-to-cold-email-here-s-what-the-data-says) | **60–90 words.** We need room for one ad idea, so 25–50 is too tight. Our drafts average ~100 words, so trim |
| Reading level | 3rd–5th grade gets "67 % more replies"; 70 % of cold emails are written at 10th grade or above | Lavender 101 (an older post) | Short words, one idea per sentence |
| Subject | 1–4 words do best; no questions, numbers or first names; salesy wording cut opens ~18 % | Lavender; Gong 85M emails (via [summary](https://echai.ventures/startingup/cold-outreach/what-should-my-very-first-cold-email-subject-line-actually-say)) | §3 |
| Personalisation | Personalisation beyond {first name}/{company} gets up to 18 % replies vs ~9 % for basic templates; personalised emails lift replies 50–250 % | [Woodpecker](https://woodpecker.co/blog/cold-email-statistics/); Lavender via [Something Inc](https://somethinginc.com/blog/cold-email-sounds-like-ai-lavender-data/) | The line-1 observation must be load-bearing (test in §2) |
| CTA | Interest CTA → 30 % meetings booked, specific-time ask 15 %, open-ended 13 % (Gong, ~304k emails, secondary reports) | [Growleads](https://growleads.io/blog/interest-based-ctas-vs-meeting-requests-study/), [Prospeo](https://prospeo.io/s/cold-email-call-to-action) | Ask about the *frames*, never for a call, in message 1 (§4) |
| Images/links | Short copy with no images and no links performs best | [Lavender LinkedIn](https://www.linkedin.com/posts/itslavenderduh_cold-email-subject-lines-without-considering-activity-7087049311816994817-AazP) | Plain text and at most one link. The frames are the visual |
| Follow-ups | 58 % of replies come from step 1 and 42 % from follow-ups; 4–7 touches is the sweet spot; space them 3–4 days apart; a reply-style step 2 beats a formal one by ~30 % | Instantly 2026 | §5 |
| Day | Replies peak Tue–Wed (Wednesday best); Friday has the most auto-replies | Instantly 2026 | Send Tue–Thu, 8–10 am in the recipient's time zone `[inf]` |
| Executives | C-level executives are 30 % less likely to reply than non-executives | Gong | Founders get the shortest version; one sharp idea |

**How not to sound like AI or a template** (Lavender data via [Something Inc](https://somethinginc.com/blog/cold-email-sounds-like-ai-lavender-data/), plus `[inf]`):
- **Delete test:** remove the personal line. If the email still works, the line was decoration.
- **Swap test:** if the line would make sense sent to another brand, rewrite it.
- **Don't state facts with no point of view.** "I saw you launched bundles" is a fact. "Four fruits and new bundles is a variant set begging to be tested" is a thought.
- **One researched fact, not three.** Stacking scraped facts shows the machine.
- **Banned words** `[inf]`: "I hope this finds you well", "I came across", "elevate", "unlock", "game-changer", "seamless", "In today's fast-paced…", "I'd love to", "Just following up", em-dash chains, three-adjective lists, "quick question".
- **Write like a text to a smart friend.** Use contractions, keep one typo-free plain sentence per idea, and sign with a first name.
- **Keep follow-ups as specific as message 1.** Generic step 2–4 is the most common AI tell.

### 1.1 Sending from a personal Gmail: deliverability
- **Hard limit:** Gmail allows 500 recipients a day, and more than 500 in one message trips it ([Google](https://support.google.com/mail/answer/22839)). That limit is irrelevant for us. **The practical ceiling for a cold-sending personal account is far lower** `[inf]`.
- **Ramp** `[inf, consistent with Google's "increase gradually, avoid bursts", [sender guidelines](https://support.google.com/a/answer/81126)]`:
  - Days 1–5: 8–10 new emails a day.
  - Week 2: 12–15 a day.
  - Never go above ~25 sends a day, follow-ups included.
  - Space sends 5–15 minutes apart, by hand or with Gmail's "schedule send".
  - Never BCC, and never mail-merge 50 at once.
  - At that pace, the 50 first touches take about 1.5 weeks.
- **Warm-up:** an established personal account with normal two-way traffic is already "warm". A brand-new account should send and receive ordinary mail for 1–2 weeks first `[inf]`. Instantly's new-domain guidance is 5–10 emails a day, ramped over 4–6 weeks.
- **Authentication:** @gmail.com mail is signed by Google (SPF and DKIM pass automatically). Google requires SPF or DKIM from all senders, plus TLS and RFC 5322 formatting. DMARC and one-click unsubscribe are required only at 5,000+ messages a day ([Google](https://support.google.com/a/answer/81126)).
  - If you later move to your own domain (Workspace), set up SPF, a 2048-bit DKIM key and DMARC `p=none` first.
  - Don't buy anything for this campaign. The studio name in the signature does the branding job.
- **Spam rate:** keep it below 0.1 % and never reach 0.3 % (Google). With 50 recipients, **a single "report spam" is 2 %**, so relevance is the only protection `[inf]`.
- **Bounces:** stay under 2 % (Instantly). Use only publicly listed addresses (as the brief requires). Never guess an address.
- **Content hygiene:**
  - Plain text with no images, attachments, link shorteners or open-tracking pixels. Apple Mail Privacy Protection makes open rates meaningless anyway.
  - At most one link, as a full visible URL (e.g. your portfolio).
  - **Never put "Re:" or "Fwd:" on a new email.** Google lists that as a spam trigger, and the FTC treats it as a deceptive subject.
  - Send follow-ups as genuine replies in the same thread.

### 1.2 CAN-SPAM, plus the opt-out footer that isn't a CTA
CAN-SPAM covers B2B email (there is no B2B exception). The FTC's eight requirements ([FTC guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business)) are:
1. Truthful headers.
2. A non-deceptive subject.
3. Identification as an advertisement. The form is flexible.
4. A valid physical postal address.
5. A clear opt-out.
6. Opt-out rights survive any subscription or membership.
7. Honour opt-outs within 10 business days and keep the mechanism working for 30 days.
8. You stay liable for anyone sending on your behalf.

Penalties run up to $53,088 per email. `[law]`

**Footer.** Put it below the signature, in the same plain text and the same font size. It must not be hidden: hiding text with HTML or CSS is itself a Gmail spam signal.
```
Itamar · [Studio name] · AI video ads
[Street address or registered PO box], Boca Raton, FL [ZIP]
This is a one-to-one business pitch. Reply "stop" and I won't email again.
```
- **Why it isn't a CTA:** it sits under the signature, states a fact, and asks no question. The body itself never asks "not interested?" (§4).
- "Business pitch" is the advertisement disclosure. `[law][inf]` The FTC lets you choose how to disclose it, but plain wording beats burying it.
- Keep a do-not-contact list. Honour any "no", "remove" or "stop", however it's phrased, the same day.

---

## 2. Cold-email scoring checklist (grade all 50 before sending)

Score each email out of 20. **Send at 16+. Rewrite at 12–15. Rebuild under 12.**

| # | Check | Pts |
|---|---|---|
| 1 | **Subject line:** 1–4 words, lowercase or sentence case, no question, no "Re:", names their product or world rather than us | 2 |
| 2 | **Line 1 is a load-bearing, true observation.** It passes the delete test and the swap test, and quotes or shows something only someone who looked would know | 3 |
| 3 | **Opens with them.** "You/your" outnumbers "I/we" by at least 2:1, and the email doesn't open with "I" | 1 |
| 4 | **One ad idea**, one line, with a visual twist in *their* brand world, and no claims | 3 |
| 5 | **Credibility in one honest clause:** "small AI studio in Boca, no shoot, AI-made". No fake clients, numbers or adjectives | 2 |
| 6 | **The offer is free and specific:** "5 frames for [product]". No price, no call ask | 2 |
| 7 | **One CTA**, in the two-yes alternative-choice form (§4), as the last line | 2 |
| 8 | **Length 60–90 words** (−1 per 10 words over) | 2 |
| 9 | **Readability:** grade 5 or below, sentences ≤18 words, mobile-friendly with no more than 3 short paragraphs | 1 |
| 10 | **Hygiene:** plain text, no attachment or image, ≤1 link, no banned words (§1), the CAN-SPAM footer present, mirrors their tone (casual or formal) | 2 |

### 2.1 Grading three drafts from `PROSPECTS_50.md`
- **#1 FRUGA:** 15/20.
  - Strong quote opener (3/3) and a vivid idea (3/3).
  - Loses points for length (116 words: 0/2), the yes/no CTA (1/2) and no subject line (0/2).
  - Rewrite:
    > **Subject:** pink guava, falling
    >
    > Hi Allen, "We are not a prebiotic soda… We are a real fruit soda." Your cans already say it: one fruit, nothing to explain.
    >
    > Ad idea for Pink Guava: a hot Coconut Grove afternoon, a guava drops, splits in slow motion, and the inside is fizzing pink. Cut to the sweating can. Taste first, no claims.
    >
    > I run a small AI video studio in Boca (no shoot, all AI-made). I'll make 5 free frames. Want them for Pink Guava, or for the new Sun Affair bundle?

    That's 75 words.
- **#2 Seventh Avenue (IG DM):** 16/20.
  - "They're asking words to do what scent can't" has a point of view (3/3).
  - Two products are offered loosely. Turn that into a clean two-yes CTA: "Want the 5 stills for Kumquat & Clove, or for the Frasier + Bonfire set?"
- **#3 The Magic Scent:** 15/20.
  - "So I'll be direct" opens with *us*, and "perfect fit" is a sales cliché (−1).
  - "Your current Meta ads are mostly static" reads as criticism with no point of view. Reframe it as an opportunity: "Your hotel-scent ads say it in words; film can show the room changing."
  - CTA: "Want the 5 stills built around Penthouse, or Oud Wood?"

**Batch fix for all 50** `[inf]`: cut to ≤90 words (usually the format list and a second descriptive clause go); add a 1–4-word subject; make every CTA two products, scents or flavours; move price, portfolio and ratios to the reply stage.

---

## 3. Subject-line patterns that work

Rules: 1–4 words, look like an internal note, name *their* thing, and never mislead (CAN-SPAM requires the subject to match the content).

| Pattern | Template | Example |
|---|---|---|
| Their product + verb | `[product], [verb]ing` | "pink guava, falling" |
| The idea's title | `[2-word concept]` | "room checks in" (Magic Scent) |
| Their own words | `"[3-word quote]"` | "fall isn't one smell" |
| Product + format | `[product] film idea` | "Kumquat & Clove film" |
| Moment | `[product] for [season/launch]` | "Sun Affair launch" |
| Frames promise (follow-ups) | `5 frames: [product]` | "5 frames: Penthouse" |

(30MPC/Jason Bay families, [summary](https://echai.ventures/startingup/cold-outreach/what-should-my-very-first-cold-email-subject-line-actually-say); we skip "competitor share" with founders `[inf]`.) **Avoid:** questions, numbers, "quick question", the first name, emojis, ALL CAPS, false familiarity ("our chat"), "Re:".

---

## 4. The CTA: two "yes" options (alternative choice)

The house rule (per the owner): **every CTA offers two yes options, and the body never invites a "not interested?" reply.**

**Evidence for:**
- **Single-option aversion** ([Mochon 2013, *JCR*](https://ideas.repec.org/a/oup/jconrs/doi10.1086-671343.html)): with one DVD player shown, ~9–10 % would buy. With two shown, 32 % and 34 % chose one of them. A lone option makes people want to keep searching, and a second option ends the search ([coverage](https://www.sciencedaily.com/releases/2013/07/130726131251.htm)).
- **Gong's CTA data:** low-commitment interest asks beat meeting asks. "Which product should the free frames be for?" is still an interest ask; it just pre-chooses the next step `[inf]`.

**Evidence against, and the limits:**
- No controlled cold-email test isolates either/or CTAs ([search summary](https://www.breakcold.com/explain/alternative-close)). Expect directional results only.
- Sales trainers warn that the alternative close is overused and can read as a hard close.
- Hard-to-compare options increase "decide later" (choice deferral, Dhar 1997, cited by Mochon), so **keep both options equally easy**: both free, same size, differing only in taste.
- Autonomy cues ("but you are free to refuse") roughly double compliance in Carpenter's 2013 meta-analysis of 42 studies. A pre-registered re-analysis found the effect is smaller, and absent in low-risk-of-bias studies ([Meta-Psychology](https://open.lnu.se/index.php/metapsychology/article/view/2640)).
  - **Reconciliation:** we don't invite a "no". We keep autonomy with "no strings" and "your pick" in the body, and the footer carries the opt-out.
- **Ethics line:** an alternative choice is honest when (a) both options are real and good for them, and (b) the frame doesn't hide the fact that "neither" is fine. In message 1 that holds, because both options are free. At the close, use it only *after* they've said the problem is real and the price range is OK. Never use it to steamroll a "not now" (§9).

**Templates:**

| Stage | Two-yes CTA |
|---|---|
| Message 1 | "Want the 5 frames for **[hero product]**, or for **[launch/bundle]**?" |
| Message 1 (one product) | "Should I make the 5 frames **in your [studio-white] look**, or **in a [Miami-afternoon] world**?" |
| Follow-up, day 3 | "Should I start with the **[new idea]** frame, or stick with **[original idea]**?" |
| Close-the-loop, day 14 | "Should I send the frames **this week**, or check back **in January** after Q4?" |
| After a positive reply | "Easier to see the frames **by email Thursday**, or **on a 15-minute call** where I walk you through them?" |
| Package close | "Does the **Starter at $1,200** fit this quarter better, or the **Launch pack at $2,500** with the 6 variants?" |
| Retainer upsell | "Shall we do **one more Launch pack for spring**, or set up the **monthly variant plan**?" |
| Deposit | "I'll send the invoice for the 50 % deposit. Easier to pay **today by card**, or **by bank transfer this week**?" (only after they've said yes to the scope) |
| Scheduling | "**Tuesday 10 am** or **Wednesday 2 pm** for the kickoff?" |

---

## 5. Follow-up sequence template (4 touches, 14 days)

Send all follow-ups in the same thread, keep them reply-style and short, and give each one a new angle (Instantly: 4–7 touches, 3–4 days apart). The brief's day-3 and day-7 notes are steps 2 and 3. Step 4 is optional and only for fit 8+ prospects `[inf]`.

| Day | Step | Words | Angle | Template |
|---|---|---|---|---|
| 0 (Tue–Thu) | 1 | 60–90 | Observation → idea → free frames | §2 rewrite |
| 3 | 2 | ≤50 | **A new idea** (a second storyline, or a variant series) | "One more for [product]: [one-line twist]. It cuts into 6 s / 15 s versions easily, one per [flavour/scent]. Should I start with this one, or the [first idea]?" |
| 7 | 3 | ≤40 | **Show, don't tell:** one finished frame as a link (not an attachment). Make it from their public product photo, clearly marked "concept, AI-made" | "Made one frame so you can judge the look: [link]. AI-made concept, not for use. Want the other 4 for [A], or for [B]?" |
| 14 | 4 | ≤35 | **Close the loop** with timing and a no-oriented feel, without asking "not interested?" | "Q4 is a lot. Should I send the frames now, or check back in January?" |

Rules: stop the moment they reply, even with a "no" or "maybe"; no "just bumping this", guilt or fake deadlines; a frame made before they say yes is for them only. Never post it or use their trademark publicly without written permission `[law][inf]`.

---

## 6. Reply handling and objection playbook

**Principles:**
- Answer within 2 business hours, and match their length.
- Label the concern first, then answer in one or two lines, then give a two-yes next step.
- Voss: a label ("It sounds like…") defuses, a calibrated question ("How/What…") hands them the thinking, and an accusation audit says the negatives first (Voss, *Never Split the Difference*, 2016).

**"How much?"** Quote a range, recommend one option, keep the frames free.
> Fair question. Most brands your size land in one of three: a **Starter** (1 hero film + 3 cuts) at $1,200, a **Launch pack** (hero + 6 variants) at $2,500, or a **monthly plan** of 8–12 new variants at $3,500/mo. For [brand] I'd suggest the Launch pack, since [4 flavours / scent-by-scent ads] give you a real test set. The 5 frames stay free either way. Want them for [A], or for [B]?

**"We do it in-house" / "we have a UGC pipeline."**
> Makes sense. It sounds like you've already got people who know the brand well. I'm not trying to replace that. What I add is the stuff that's hard to shoot: [the guava splitting in slow motion / the room turning into a lobby]. It slots in as extra variants next to your UGC. What's the hardest kind of shot for your team to get right now? Happy to aim the 5 frames there, or at [product].

**"AI looks fake."**
> You're right. Most of it does: waxy skin, melting labels. That's exactly why I offer the frames first: if they look fake on your product, we stop there and you've lost nothing. Product-only scenes with no people are where AI is strongest. One thing to know up front: Meta may add an "AI info" tag to ads made with AI, and I'll always tell you which shots are generated. Want the frames on [A], or [B]?

(Meta labels ads with significant AI edits, and photoreal AI people get a label next to "Sponsored" ([coverage](https://getcoai.com/news/meta-enhances-transparency-with-new-labeling-requirements-for-ai-generated-ads)). Verify the current policy before quoting it.)

**"No budget."**
> Totally fair. It sounds like spend is locked for now. The frames are free and you keep them as concepts. When does the next budget window open, after Q4 or in spring? I'll make the frames now, or hold them until then. Which works?

If they want something small: offer the Starter with fewer cuts at $750 (floor `[inf]`). **Never discount the same scope.** Cut scope instead.

**"Send more info."** Often a polite brush-off, so send *less*, not a deck.
> Sure. Here's a 40-second reel of three spec films, for brands I invented, all AI-made: [link]. Honestly though, frames on *your* product will tell you more than my reel. Should I make them for [A], or [B]?

**"Not now."**
> Understood. It sounds like Q4 is already spoken for. Is it a "January" not now, or more a "after the New York rollout" not now? I'll put a note to check back then.

Then do it. Send one note at the agreed time and nothing in between.

**"Who else have you worked with?"** (No paid clients yet. Never imply otherwise.)
> Honest answer: no paid clients yet. You'd be one of the first. The three films on my reel are spec pieces for brands I made up, to show the craft. That's exactly why the frames are free: you judge the work on your own product before spending anything. For a first project I also only take the balance once you approve the final cut. Want the frames on [A], or [B]?

That last line is Hormozi-style risk reversal: it raises "perceived likelihood" ([value equation](https://www.supersummary.com/100m-offers/section-3-summary/)). Offer it only if you can afford a client walking away after the deposit `[inf]`.

**Ghosting after the frames or a proposal.** Use Voss's no-oriented check ([summary](https://bigthink.com/videos/chris-voss-on-walking-away-from-a-negotiation/)), adapted so it isn't a "not interested?" invitation:
> Have you set the [product] film aside for this quarter?

Send it as a single line. It invites a correction rather than a rejection; the owner's rule applies to *cold* bodies, and this is a warm thread `[inf]`.

---

## 7. Discovery-call script (20–25 min, video or phone)

**Frameworks:** SPIN (Rackham, *SPIN Selling*, 1988, from 35,000 calls) for the question order; Gap Selling (current → future state, impact, root cause; [HubSpot](https://blog.hubspot.com/sales/gap-selling)); the Sandler pain funnel ([Sandler](https://sandler.com/?p=17965)); Gong: 11–14 questions spread through the call, price about 75 % of the way in ([discovery](https://www.gong.io/blog/deal-closing-discovery-call), [price timing](https://www.gong.io/blog/data-reveals-the-best-time-to-talk-price-and-budget)).

**0:00 Up-front contract** (Sandler):
> Thanks for making time. I was thinking: you tell me how ads work for you today, I show the frames and ask some questions, and at the end we decide together whether a next step makes sense, and it's fine if it doesn't. Sound OK?

**Accusation audit** (Voss), said once:
> You're probably thinking: AI studio, no clients yet, how fake will this look? Fair. That's why I lead with the frames.

**2:00 Current state** (situation; 3–4 questions):
1. "Walk me through how a new ad gets made today, from idea to live."
2. "How many new creatives do you launch in a typical month?"
3. "Which ad is your best performer right now, and why do you think it works?"
4. "Roughly what are you spending on Meta/TikTok monthly?" (Ask lightly, then label: "Sounds like paid is a real channel for you.")

**7:00 Problem and impact** (pain funnel; 4–5 questions, spread out):
5. "What's frustrating about creative right now?" → "Tell me more." → "Give me an example."
6. "How long has that been the case?"
7. "What have you tried? Freelancers, UGC, agencies? How did it go?"
8. "When an ad fatigues and there's nothing new to swap in, what happens to results?" (implication)
9. "What does that cost you, in money or in your own time?"

**13:00 Future state** (need-payoff; 2–3 questions):
10. "If creative were solved for Q4, what would that look like?"
11. "How would you know in 60 days that it worked?" (Their metric, not ours. **Never promise ROAS.**)
12. "Who else weighs in on a decision like this?"

**16:00 Show the frames.** Ask "What jumps out?", then stop talking. Label what you hear: "It sounds like the [guava] one feels most like you."

**18:00 Price** (≈75 % of the call; see §8):
> Based on what you said ([4 flavours, Q4 bundles, nothing to swap in when ads fatigue]), here's how people usually do this…

Present three options top-down, recommend one, then go quiet.

**21:00 Next step** (two-yes):
> Want me to send the one-page proposal for the Launch pack, or for the Starter so you can test it first?

If they hesitate, ask a calibrated question: "What would need to be true for this to make sense?"

**Close-out:** recap their words, the agreed next step and the date. Send the proposal the same day.

**Voss toolkit:** mirror their last 1–3 words; label ("It sounds like…"); calibrated questions ("How am I supposed to do that?"); aim for "That's right"; silence after the price.

---

## 8. Pricing, proposal and contract

**Presentation:**
- **Anchor high, top-down.** Show the retainer first, then the Launch pack, then the Starter. The first number sets the reference (Tversky & Kahneman 1974 anchoring).
- **Three options:** a middle option made attractive by its neighbours pulls choices toward it. Ariely's informal *Economist* test went from 32 % to 84 % choosing the target bundle ([summary](https://en.wikipedia.org/wiki/Decoy_effect)); it is a single, non-peer-reviewed test.
- **Every tier must be a real offer.** Never present a sham decoy `[inf]`.
- **Price against value, using their numbers, not ours** `[inf]`:
  > You said you spend ~$8k a month on Meta and swap creative every 3–4 weeks. The Launch pack is $2,500 for 7 assets: about $350 an asset, no shoot, ready in a week.

  Never promise a return.
- **Name a single recommendation**, and ask once.
- **No discount for the same scope.** Trade price against scope or speed. A rush (<5 days) is +25 % `[inf]`.

**One-page proposal template:**
```
[Brand] × [Studio] — [Concept name] proposal            [date] · valid 14 days

WHAT YOU TOLD ME
- [Current state in their words]  - [Problem + what it costs]  - [Goal for Q4]

THE IDEA
[One-line storyline with twist] → frames approved on [date]

OPTIONS
1. Monthly variant plan — 8–12 new variants/month (6/15/20 s; 9:16, 4:5, 1:1), 1 new concept/month — $3,500/mo, 3-month minimum
2. Launch pack (recommended) — 1 hero film (20 s) + 6 variants, all 3 ratios — $2,500
3. Starter — 1 hero film + 3 cuts — $1,200

TIMELINE   Kickoff → storyboard frames (day 2) → first cut (day 5) → final (day 7–8)
INCLUDED   2 revision rounds per film; music licensed for paid social; captions file
NOT INCLUDED  Live shoots, real actors/likeness, medical/health claims, ad buying
PAYMENT    50 % to start, 50 % on approval, before final files. Card or ACH.
RIGHTS     Perpetual, worldwide licence for [Brand]'s paid + organic ads (see terms)
AI NOTE    All footage is AI-generated from your product photos; I'll flag every generated element.
NEXT STEP  Reply "Launch" or "Starter" and I'll send the deposit invoice + short agreement.
```

**Simple agreement terms** (common practice per [contract guides](https://www.artfolio.com/article/essential-clauses-for-short-term-videography-contracts-with-agencies); `[law]`, have a Florida attorney review the template once):

1. **Scope:** list the deliverables (films, lengths, ratios), the agreed concept and the delivery dates.
2. **Payment:** 50 % non-refundable deposit to start and 50 % on approval, before the final unwatermarked files. Invoices due in 7 days; 1.5 %/month late fee.
3. **Revisions:** 2 rounds per film, on consolidated feedback within 5 business days.
   - A *revision* tweaks the agreed concept (timing, colour, text, music).
   - A *new direction* is a new scope.
   - Extra rounds cost $150 each `[inf]`.
4. **Cancellation:** the deposit covers work to date. If they cancel after the first cut, 75 % is due.
5. **Usage rights:** on full payment, the client gets an exclusive, perpetual, worldwide licence to use the deliverables for its brand on all channels.
   - The studio assigns whatever copyright it holds.
   - **Disclosure** `[law]`: purely AI-generated material may not be copyrightable in the US. The Copyright Office's Part 2 report (Jan 2025) says prompts alone aren't authorship; human selection, arrangement and edits can be protected ([summary](https://copyrightalliance.org/ai-report-part-2-copyrightability/)). So exclusivity is a promise not to reuse, not a guarantee that others can't copy.
6. **Studio rights:** the studio may show the work in its portfolio *after the ads go live*, unless the client opts out in writing. Raw generations and project files are not included.
7. **Client warranties:** the client owns or licenses the product images, logos and trademarks it supplies, and approves all claims in the copy. The studio writes no health or medical claims.
8. **AI, liability, law:** commercially licensed AI tools only; no real person's likeness without written consent; the client handles platform AI labels; liability capped at fees paid; Florida law.

**Turning the free frames into a paid deal** `[inf]`:
- Scope the frames tightly: 5 stills, 1 concept, 1 round of light tweaks, delivered in 3–5 days as watermarked "AI concept" stills.
- Deliver them on a 15-minute call, not as attachments, and run §7 compressed.
- If they love a frame, that frame *is* the first storyboard. Close with: "Launch pack or Starter?"
- If they don't, ask "What's off?" and offer one re-direction. Never a second free round.
- Track every prospect in one sheet: stage, date, next step and objection heard.

---

## 9. Ethics: persuasion without manipulation

**The test** `[inf]`: would the tactic still work if the prospect could see exactly what you're doing and why? Labels, good questions, a clear recommendation, three real options and a free sample all pass. Fake scarcity, invented clients and hidden AI fail.

| Allowed (true, transparent) | Never |
|---|---|
| Real capacity: "I take on two projects in November." Say it only if true | Fake deadlines, "price goes up Friday", countdowns |
| Spec work clearly labelled "spec for an invented brand" | Implying the AURUM/VESPER/SOL films were client work |
| "No clients yet. You'd be one of the first" | Invented logos, testimonials, stats or "brands we've worked with". The FTC's 2024 rule bans fake or AI-generated testimonials, with civil penalties ([FTC](https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials)) `[law]` |
| "Everything is AI-made" in message 1 and in the proposal | Calling AI footage "shot" or "filmed"; hiding Meta's AI labels |
| Alternative-choice CTA where both options are real and good | Using it to override a stated "no" or "not now" |
| Anchoring with a real, higher tier | Sham decoys; a "list price" nobody pays |
| Risk reversal you can honour | Promising ROAS, sales or "viral" |
| Honest subject lines, a working opt-out | "Re:" on a first email, hidden unsubscribe text, purchased lists, guessed emails |

Persuasion helps someone decide well, faster, on true information; manipulation changes the decision with false information or pressure `[inf]`.

---

## 10. Sources and gaps
- **Data:** [Instantly 2026 benchmark](https://instantly.ai/cold-email-benchmark-report-2026) · [Lavender benchmark](https://lavender.ai/blog/the-cold-email-benchmark-report) · [Lavender Cold Email 101](https://lavender.ai/blog/cold-email-101) · [Woodpecker](https://woodpecker.co/blog/cold-email-statistics/) · [Gong exec email data](https://www.gong.io/blog/do-execs-really-reply-to-cold-email-here-s-what-the-data-says) · [Gong discovery](https://www.gong.io/blog/deal-closing-discovery-call) · [Gong price timing](https://www.gong.io/blog/data-reveals-the-best-time-to-talk-price-and-budget) · Gong CTA study via [Growleads](https://growleads.io/blog/interest-based-ctas-vs-meeting-requests-study/) (original not found).
- **Practitioners:** Josh Braun via [11x](https://www.11x.ai/guides/josh-braun-cold-outreach-method) (examples not confirmed verbatim) · Becc Holland via [Buteau](https://www.antoinebuteau.com/lessons-from-becc-holland/) (one premise reused across the sequence) · Will Allred, "translation problem" ([GTMnow](https://gtmnow.com/podcast-how-to-write-sales-emails-that-stand-out/)) · 30MPC via [notes](https://notes.nicolasdeville.com/sales/email-sequences) · Hormozi, *$100M Offers* · Voss, *Never Split the Difference* · Rackham, *SPIN Selling* · Keenan, *Gap Selling* · Sandler.
- **Research:** [Mochon 2013](https://ideas.repec.org/a/oup/jconrs/doi10.1086-671343.html) · [BYAF re-analysis](https://open.lnu.se/index.php/metapsychology/article/view/2640) · [Decoy effect](https://en.wikipedia.org/wiki/Decoy_effect).
- **Law and policy:** [FTC CAN-SPAM](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) · [Google sender guidelines](https://support.google.com/a/answer/81126) · [Gmail limits](https://support.google.com/mail/answer/22839) · [FTC fake-reviews rule](https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials) · [USCO Part 2](https://copyrightalliance.org/ai-report-part-2-copyrightability/).
- **Gaps:**
  - YouTube transcripts (Braun teardown `9s-8XtRQEg8`, 30MPC "Sales Email Elimination" `5pjUStm0pvo`, and others) were blocked by HTTP 429 and an IP block on the transcript API. Retry them later with `fetch_yt.py`.
  - No primary Gong CTA report was found, and no controlled test of either/or CTAs exists.
  - All cold-email benchmarks are vendor data, mostly from SaaS.
  - Track our own reply rate by CTA variant from the first 50 sends.
