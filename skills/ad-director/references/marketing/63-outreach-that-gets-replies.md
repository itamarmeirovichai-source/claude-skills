# 63 · Outreach that gets replies: the first message, the follow-ups and the objections

Researched 2026-10-09. No money was spent, nobody was contacted, nothing was sent. This doc is the **single source for the first touch, the follow-ups and the first objection replies**. For the rest of the sale it builds on doc 28 (sales mastery: subject lines, deliverability, the discovery call) and doc 34 (objection mastery). Where 28 §5, 34 §4.2 or `research/ai-video-reels/launch/outreach.md` disagree with this doc about the first touch or the follow-ups, **this doc wins** (see §9).

**Labels.** **[v]** = a vendor figure (the vendors sell outreach tools; their samples are mostly B2B SaaS, so read them as directional). **[c]** = a platform's or company's own statement. **[m]** = I checked it myself this run (curl, DNS, Shopify JSON). **[inf]** = my inference. **[law]** = a legal point, not legal advice.

---

## 0. The honest answer: is this the best we can reach?

No. The four drafts in `leads/2026-10-09.md` are well researched, but **the things stopping VXO from getting a paid client aren't in the wording**. In order of damage:

1. **Nothing has ever been sent.** About 85 brands have drafted messages (`HOT_NEW_30`, `HEAT_50`, `PROSPECTS_50` and today's 4). Every pipeline line reads "found", and `launch/tracker.csv` holds only EXAMPLE rows [m]. With no sends there are no replies and no data, so every rule we use is a vendor average.
2. **The sender can't be checked.** A founder who gets a cold DM opens the sender's profile and Googles the name. Today she would find nothing. `vxo.studio` doesn't resolve (DNS NXDOMAIN on 2026-10-09 [m]), the site in `site/` isn't deployed, a web search for "vxo.studio" returns other companies (an Indonesian "VXO" creative agency, Vexo) [m], and every email draft still carries `[Owner name]` and `{BUSINESS_ADDRESS}` placeholders. Without a postal address, **the emails can't legally be sent** (CAN-SPAM [law]). The rule "the portfolio goes in the first reply" has no portfolio to link to.
3. **Instagram allows one text-only message.** Someone who doesn't follow the recipient gets **one message, text only**, until the recipient accepts. No photo, no follow-up DM. It lands in the Requests folder, which has to be opened on purpose ([TechCrunch, Aug 2023](https://techcrunch.com/2023/08/03/instagrams-new-feature-protects-users-from-unwanted-images-and-videos-in-dms); [Neowin](https://www.neowin.net/news/instagram-is-changing-how-unknown-users-can-or-cant-text-you/)) [c]. On a brand account a social or CX person reads it, not the founder. So a DM can't carry a follow-up sequence or a frame, and our "follow-up" plan has to run by email.
4. **One lead is pitched on products that may be hidden.** All three Fishwife products in the draft (the 12 Days Advent Calendar, the Ultimate Gift Pack and the Mermaid Ornament) carry the Shopify tags `redirect-to-404` and `exclude`, and have empty descriptions. The gift pack shows `available: false`, and a web search finds no announcement of the advent calendar [m]. If it is unreleased, then praising it tells the founder **we read her store's back end**: creepy at best, and wrong at worst.
5. **The site contradicts the pitch.** The built site says "Every film is one 30-second take… No cuts" (`site/src/layouts/Base.astro`, 4 film pages) [m]. Every idea in today's DMs is built on hard cuts, and LESSONS requires 6–10 hard cuts for action. A founder who replies and clicks through sees a studio that doesn't make the film we pitched.
6. **The copy reads as a template.** All four DMs share one skeleton ("Hi X, [superlative]. Film idea: … I make AI product films (no shoot). Want 5 free frames for A, or B?"). Each opens on an unprovable superlative ("best holiday piece I've seen this year", "genius gift", "holiday hero", "great line"), which is the commonest AI tell (doc 28 §1). Two of the four founders (Rose Shattuck, Aisha Chottani) are both Women in eComm honorees [m, dossiers], and could plausibly compare notes.
7. **The word "AI" arrives before the reason to care.** In 2026 surveys, 73 % of consumers say they'd be less likely to trust an ad they suspected was AI-made, and 63 % less likely to buy (Harris Poll for the 4As/Infillion, June 2026, via [AAAA](https://www.aaaa.org/blog/consumers-are-sick-and-tired-of-hearing-about-ai-all-the-time/)). 45 % of Australians would trust a brand less ([YouGov, May 2026](https://yougov.com/articles/54818-45-of-australians-say-ai-generated-ads-would-make-them-trust-a-brand-less)). The founder knows those numbers. We must say "AI" (honesty, LESSONS), but **after the idea, and next to what stays real**.
8. **Stale numbers are one paste away from the message.** The ad counts in the dossiers come from Motion snapshots that are about 4 months old, and the Meta Ad Library returned 403 [m]. A line like "17 of your 20 newest ads are stills" could be false today, and a founder knows her own ad account to the ad.
9. **The playbooks contradict each other.** `launch/outreach.md` puts a $750 sprint price in the first email and signs off "Not relevant? Reply 'no'". `vxo-leads` §3 bans both. Doc 28 §5 has a 4-touch, 14-day sequence, and doc 34 §4.2 has a 21-day cadence with video. An agent picking "the" playbook can pick the wrong one.
10. **Throughput is too low for the maths.** At a realistic 5–10 % reply rate (§1), about half of replies positive, and an unknown frames→sale rate (assume 20–30 % [inf]), **one sale needs roughly 60–150 first touches**. Four leads a day, never sent, gives zero.

What I fixed (zero spend): this doc, with red-teamed and rewritten messages for all four leads (§4), a 3-touch follow-up per lead (§5), objection replies (§6) and a pre-send checklist (§7), plus a rewrite of `vxo-leads` §3 and a new §3b. What only the owner can fix is in §8.

---

## 1. What the data says (2025–2026)

| Question | Finding | Source | What we do |
|---|---|---|---|
| Baseline reply rate (email) | Average 3.43 %, top quartile 5.5 %+, top decile 10.7 %+ (2025 campaigns). Hunter: 4.5 % average | [Instantly 2026](https://instantly.ai/cold-email-benchmark-report-2026) [v]; [Hunter](https://hunter.io/outreach-calculator) [v] | Plan for 5–10 % on hand-researched founders; anything under 3 % after 30 sends means the channel or offer is wrong, not the adjectives |
| Small lists | Campaigns of 21–50 recipients average 6.2 %, 500+ average 2.4 % (Hunter). Under 50: 5.8 % vs 2.1 % at 1,000+ (Woodpecker) | via [Instantly/Lemlist summaries](https://lemlist.com/blog/cold-email-benchmarks/) [v]; [Woodpecker](https://woodpecker.co/blog/cold-email-benchmarks/) [v] | Our 1:1 model is on the right side of this |
| Replies ≠ yeses | In one dataset 14 % of replies were positive, 30 % negative, 45 % auto-replies | [Prospeo summary](https://prospeo.io/s/cold-email-benchmarks) [v] | Count **positive** replies (frames requested). That's the KPI |
| Personalisation depth | Two custom attributes: 5.6 % vs 3.6 % replies (31M emails). Real personalisation vs a merge-tag template: +50–250 % | [Hunter, State of Cold Email](https://hunter.io/the-state-of-cold-email) [v]; Lavender via [Something Inc](https://somethinginc.com/blog/cold-email-sounds-like-ai-lavender-data/) [v] | One observation **with a point of view** about something the customer can see. Not three scraped facts |
| Length | Hunter (34M emails, 2022–24): reply rate barely moves with length, 3.4–4.5 % from 0 to 200+ words; 20–39 words was best at 4.5 % | [Hunter word count](https://hunter.io/blog/cold-email-word-count) [v] | Length isn't the lever. Clarity is. A DM is still read on a phone in a Requests list, so 35–50 words |
| Images in email | Emails with images: 2.62 % vs a 3 % baseline (−12.7 %). File attachments: 4 % (+33 %, small sample). Lemlist claims personalised images lift replies (vendor of image tools) | [Reply.io research](https://reply.io/images-gifs-in-cold-emails), [Reply.io attachments](https://reply.io/emojis-attachments-impact-cold-email/) [v]; [Lemlist](https://www.lemlist.com/blog/images-in-cold-emails) [v] | **No image in touch 1.** The single frame goes in follow-up 2, as one JPG in the same thread, once the owner approves the ~$0.10 spend (§5) |
| Instagram DM to a non-follower | One message, text only, until accepted; it lands in Requests. Templated text and bursts to new people push messages into "Hidden Requests" and risk restrictions | [TechCrunch](https://techcrunch.com/2023/08/03/instagrams-new-feature-protects-users-from-unwanted-images-and-videos-in-dms) [c]; [Instagram help](https://help.instagram.com/ipad-app/1264898753662278) [c]; [Inrō](https://www.inro.social/blog/instagram-dm-deliverability) [v] | The DM must stand alone. Max ~10 new DMs a day by hand, each one different. Warm first: the owner follows and leaves one genuine comment 1–3 days before (practitioner reports of large lifts are anecdotal [v]) |
| Cold DM reply rate | 3–12 % "typical" for cold DMs (vendor calculator); 50 %+ claims are all for warm, engaged contacts | [DM Champ](https://dmchamp.com/tools/cold-dm-outreach-roi/) [v] | Treat DM and email as about equal. Use **both** for the top leads: DM on day 0, email on day 1 |
| Founder inbox load | An 8-figure DTC founder gets "30–100 cold pitches a day"; "we help ecommerce brands grow" is the sentence they've heard 200 times | [Modern Inbound](https://moderninbound.com/blog/cold-email-for-ecommerce-agencies) [v] | Never describe VXO first. Lead with their product and our idea |
| Follow-ups | 4–7 step sequences, 3–4 days apart, perform best; a reply-style step 2 beats a formal one | Instantly 2026 via [Lemlist](https://lemlist.com/blog/cold-email-benchmarks/) [v] | 1 first touch + 3 follow-ups over ~16 days (§5), each with a **new** reason to reply |
| Day | Wednesday best, then Tuesday and Thursday; Monday is overloaded and Friday is weekend mode | Instantly 2026 via Lemlist [v] | Send Tue–Thu, 8–10 am in the founder's time zone. Today (Fri 9 Oct) is a bad send day; Mon 12 Oct is Columbus/Indigenous Peoples' Day. **First sends: Tue 13 Oct** |
| AI attitudes | 73 % less likely to trust a suspected-AI ad, 63 % less likely to buy (US-led global, 2026); 49 % of UK consumers feel negatively about brands with uncanny AI ads | [AAAA](https://www.aaaa.org/blog/consumers-are-sick-and-tired-of-hearing-about-ai-all-the-time/) [v]; [Advanced Television/DoubleVerify](https://www.advanced-television.com/2026/08/06/study-ai-slop-poses-growing-risk-to-brand-trust/) [v] | Say "AI" once, after the idea, paired with what stays real (the product shot, the proof slot, no AI people) |
| CAN-SPAM | Covers B2B email. Needs a truthful header and subject, ad identification, a valid postal address and a working opt-out honoured within 10 business days. Up to **$53,088 per email**; the FTC kept the 2025 level for 2026 | [FTC guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) [law]; [FTC 2025 amounts](https://search.ftc.gov/news-events/news/press-releases/2025/02/ftc-publishes-inflation-adjusted-civil-penalty-amounts-2025) [law] | No email goes out until the owner fills in a real postal address (a PO box or a registered-agent address is fine). The footer is in §4 |

**Gaps.** I found no controlled study of a frame or mockup in a creative studio's first touch, and no founder-authored list of "what I reply to" that I could cite. Our own first 30 sends are the only data that will settle these (§7.3).

---

## 2. The channel plan (inside the fixed funnel)

The funnel doesn't change: a very hot lead, then a dossier, then an owner-approved message offering free frames. Only **where** the message lands changes.

| Rank | Channel | Who reads it | Use when |
|---|---|---|---|
| 1 | **The founder's own public business channel**: a personal IG account she uses for the brand, or LinkedIn, sent **by the owner by hand** from his own account | The founder | Always try first. The agent only identifies the public profile URL; the owner logs in and sends |
| 2 | **Brand IG DM** | Social or community manager, who forwards it if it's good | One self-contained message. Write it so it can be forwarded as-is ("for Rose:") |
| 3 | **Public brand inbox** (hi@, hello@, woof@) | CX or ops, who forwards it if it's addressed by name and is clearly not a support ticket | Carries the follow-ups (email allows a thread; IG doesn't). Put the founder's name in the first words |
| — | Guessed personal emails, contact forms, comments with a pitch | — | Never (public business contacts only; no guessing) |

**Sequence for a HOT lead:** day 0, a DM on the best IG channel. Day 1, the email (same idea, worded differently, and it mentions the DM in one clause so it doesn't feel like a blast). Then follow-ups by email only (§5).
**Warm-up (free, by hand, owner only):** 1–3 days before day 0, the owner follows the founder or brand account and leaves one real, specific comment on a recent post. Never a pitch in a comment.

---

## 3. Rules for the first message (they replace the old `vxo-leads` §3)

1. **Name the sender in the first line.** "Itamar from VXO". An anonymous DM reads as a bot.
2. **One observation the customer could see**, with a point of view. Never from back-end data: no `products.json` dates, no hidden or unreleased SKUs, no Motion or Ad Library counts, no "I noticed you're hiring".
3. **The idea in one or two sentences, visual, with a turn caused by the product.** This is the hook of the whole message. Earn the reply with the idea, not with praise.
4. **"AI" once, after the idea, next to what stays real**: "built with AI; your real product shots stay real" or "hands only, no AI people".
5. **The offer, in plain words**: "5 free stills of it, on your real [product]". "Frames" is our jargon; "stills of the film" is theirs. Add: no call, no cost.
6. **A two-yes CTA**, both options equally easy and both free (doc 28 §4).
7. **No superlatives** ("best", "genius", "obsessed", "hero"), no "I came across", no "hope this finds you well", no em-dash chains, no exclamation marks.
8. **Length**: a DM is 35–55 words and must stand alone (one message only). An email body is 50–90 words, with a 1–4-word subject that names their thing.
9. **No link, no image, no price** in touch 1. The price comes after they say yes to the frames or ask. Links come when there is a live site.
10. **Email footer (CAN-SPAM)**: real name, VXO, a real postal address and an opt-out line, in plain text under the signature (template in §4.0).
11. **Every message is different.** If two drafts share three sentences, rewrite one.
12. **Timing**: Tue–Thu, 8–10 am in their time zone. At most ~10 new DMs and ~15 new emails a day, spaced 5–15 minutes apart.

---

## 4. Red team and rewrite: today's four leads

How each founder reads the current draft, line by line, then the replacement. The original drafts stay in `leads/2026-10-09.md` (owned by the leads agent). **Use the versions below.** Status for all of them: **NOT SENT, awaiting the owner's "send #N"**.

### 4.0 The email footer for every email
```
Itamar · VXO · AI product films
{REAL POSTAL ADDRESS: street or PO box, Boca Raton, FL ZIP}  ← owner must fill; no email is legal without it
This is a one-to-one business pitch. Reply "stop" and I won't email again.
```

### 4.1 The Foggy Dog: Rose Shattuck (send first)

**How Rose reads the old DM:**
- "The best holiday piece I've seen this year": she knows it isn't, and it's what every vendor says. It costs trust in the first line.
- The card-shoot idea is genuinely funny and dog-mom-true. That's the asset, and it's buried in the middle.
- "I make AI product films": her first fear is a fake-looking dog (dossier §3). Nothing in the DM answers it.
- Utah, her own dog and the brand's co-signer, is in the email but **not the DM**. Utah is the single most persuasive personal hook we have.
- Product name: the SKU is "Gingerbread Man Embroidered **Bow Tie Collar**" (created 9/23, live [m]). The plain "Dog Bow Tie" has existed since June, so name it exactly.
- Unsigned. Who is this?

**New DM (to Rose's own public business account if the owner finds one, otherwise @thefoggydog; 55 words):**
> Hi Rose, Itamar from VXO here. Film idea for the Gingerbread Man bow tie collar: a family Christmas-card shoot where the photographer keeps zooming in until every human is cropped out and only the dog is left. That's the card on the fridge. Want 5 free stills of it, starring Utah or a model pup?

*Why the CTA works:* both options are free and equally easy, and "Utah" shows we know whose brand this is. The AI line moves to the email and the first reply, so the one-shot DM spends its words on the joke.

**New email (woof@thefoggydog.com, day 1):**
> **Subject:** Utah's holiday card
>
> Hi Rose (or whoever reads woof@, could you pass this to Rose?),
>
> I sent you an idea on Instagram yesterday. Here it is properly. A 15 s film for the Gingerbread Man bow tie collar: a family Christmas-card shoot, and the photographer keeps zooming in until every human is cropped out and only the dog in the bow tie is left. Cut to the card on the fridge.
>
> I build the world with AI. The dog comes from a real photo, and your embroidery stays your real product shot, never redrawn.
>
> Want 5 free stills of it, with Utah as the star, or on the Tartan Plaid walk set instead?
>
> {footer §4.0}

(79 words in the body.)

### 4.2 Moment: Aisha Chottani

**How Aisha reads the old DM:**
- Quoting "all of the ritual, none of the regret" back to her: it's her own homepage line [m], so praising it proves we saw her homepage, nothing more.
- The idea is strong and calendar-true (Dry January is her Super Bowl; doc 57).
- **Risk she will spot:** "Saturday 7 am, already heading out" plus "none of the regret" implies a no-hangover benefit. Doc 57 and LESSONS ban "hangover-free" language, and "the picture is the claim". As a comparison to alcohol it's literally true (0 % alcohol), but keep the supers and VO on the ritual, never the morning after. The Saturday shot shows a fresh, ordinary morning, not a "recovered" one.
- She runs ~24 new creatives a week (June snapshot), so she has a creative machine. Her real objection will be "we have a team". The message should name the gap we fill (motion around the real pour), **without quoting stale ad counts**.
- "Sparkling Collection, or Pink Moment": both are live [m]. Good.

**New DM (@drinkmoment, or Aisha's own public account; 55 words):**
> Hi Aisha, Itamar from VXO. A Dry January film idea: one locked camera on a kitchen counter. Friday 5 pm, ice, the can cracks, a record goes on. Hard cut to Saturday 7 am, same counter, the coupe drying on the rack. Want 5 free stills of it, for Pink Moment or the sparkling line?

**New email (hi@drinkmoment.com, day 1):**
> **Subject:** Same counter, Saturday
>
> Hi Aisha (team, could you pass this to Aisha?),
>
> A Dry January idea I sent on Instagram: one locked camera on a kitchen counter. Friday 5 pm: ice, the can cracks, a record goes on. Hard cut to Saturday 7 am on the same counter: the coupe drying, keys gone. Same ritual, different weekend.
>
> I build it with AI, but your real pour stays in as the proof shot, and every frame is checked so Meta doesn't read it as an alcohol ad.
>
> Want 5 free stills of it, for Pink Moment or for the sparkling line?
>
> {footer §4.0}

(84 words in the body.)

### 4.3 Fishwife: Becca Millstein (HOLD until the product check passes)

**How Becca reads the old DM:**
- "The 12 Days of Fishwife Advent Calendar is a genius gift": if the calendar isn't public yet (it's tagged `redirect-to-404` with an empty description, and no announcement can be found [m]), she wonders **how we know about it**. That ends the conversation.
- Both CTA options (the advent calendar and the Ultimate Gift Pack) carry the same hidden tags, and the gift pack is `available: false` [m].
- The "Day 4: all twelve tins empty" joke is exactly her humour (deadpan, self-aware). Keep the joke and move it to a product she has announced.
- @fishwife is a big account, so a social manager reads the DM. Becca is reachable through press (the Mercury interview on 10/6). The email should cite **that**, which is public and recent.
- Context she lives in: Fishwife went into Aldi in August 2026 at a discount ([IntraFish](https://www.intrafish.com/markets/fishwife-continues-retail-growth-with-discounted-offerings-at-aldi/2-1-2032646)). A brand world under price pressure needs premium-feeling DTC gifting creative. That's our angle [inf].

**Gate:** the owner opens eatfishwife.com and @fishwife by hand. Is the advent calendar visible in the navigation, on IG or in press?
- **Yes**: send version A.
- **No**: send version B, on a public product.

**Version A DM (only if the calendar is public; 54 words):**
> Hi Becca, Itamar from VXO. Film idea for the advent calendar: locked overhead shot, door 1, door 2, door 3, each tin plated a little nicer. Hard cut to "Day 4": all twelve doors open, an empty tin tower, one fork. Want 5 free stills of it, on the calendar or a gift tin?

**Version B DM (public products only; 54 words):**
> Hi Becca, Itamar from VXO. Gifting film idea: a dinner party, one Fishwife tin set out "for the table". Hard cut: twelve guests, one empty tin, bread wiping it clean. The host quietly opens a drawer stacked with thirty more. Want 5 free stills of it, on the smoked salmon or the gift tins?

**Email (hello@eatfishwife.com, day 1; version B shown):**
> **Subject:** One tin for the table
>
> Hi Becca (team, could you pass this to Becca?),
>
> Your Mercury interview on world-building stuck with me. Here's a 15 s gifting film in that world: a dinner party, one tin set out "for the table". Hard cut: twelve guests, one empty tin, bread wiping it clean. The host opens a drawer stacked with thirty more.
>
> I build the room and the joke with AI. Your tins and the real food shots stay real, and Danny's art is never redrawn.
>
> Want 5 free stills of it, on the smoked salmon or on the gift tins?
>
> {footer §4.0}

(83 words in the body.) "Danny" refers to illustrator Danny Miller (dossier §3). Use the name only if the owner confirms it's public on their site or in press; otherwise write "your illustrations".

### 4.4 AUrate New York: Sophie Kahn and Bouchra Ezzahraoui (send last)

**How they read the old DM:**
- "A holiday hero": filler.
- "Net Worth" is the strongest visual of the four (the tennis necklace as a tennis net), but a $4,919 piece being hit by a ball may make a jeweller wince. Say "the ball rolls along the stones" (gentle), not "clips".
- VC-backed (Series B), with a marketing team likely between us and the founders, so the DM will be read by social. Write it to be forwarded.
- Their fear is a wrong stone count or AI models (dossier §3). Answering it in one clause ("hands only, stone count from your photos") is the trust line.
- Names: the 9ct Three-Prong and the 9ct Lightweight are both live (created 9/30) [m]. Pick the Three-Prong as hero and the bracelet as the alternative.

**New DM (@auratenewyork; 54 words):**
> Hi Sophie and Bouchra, Itamar from VXO. Film idea for the lab-grown tennis line: a Manhattan rooftop court where the net is your 9ct tennis necklace. A serve lands on it, it rings like a bell, the ball rolls along the stones. Hands only, no AI models. Want 5 free stills, necklace or bracelet?

**New email (hello@auratenewyork.com, day 1):**
> **Subject:** A tennis necklace, literally
>
> Hi Sophie and Bouchra (or whoever runs paid social, could you pass this on?),
>
> A 15 s idea for the new lab-grown tennis line: a rooftop court in Manhattan at dusk, and the net is your 9ct three-prong necklace. A serve lands on it, it rings like a bell, and the ball rolls along the stones and drops over. "Let."
>
> I build the court with AI. The piece itself comes from your product photos, with the real stone count and "lab-grown" on screen. Hands only, no AI models.
>
> Want 5 free stills of it, on the necklace or the bracelet?
>
> {footer §4.0}

(88 words in the body.)

---

## 5. The follow-up sequence: 3 touches, email only, each one owner-approved

Instagram allows no follow-up DM until the request is accepted (§1), so every follow-up goes in the **same email thread** as a reply (never a new "Re:" subject). Each one is its own approval: the owner says "send #N-FU1", and so on. **Stop at the first reply of any kind** ("no", "later", an out-of-office with a return date: honour the date). Every follow-up keeps the §4.0 footer.

| Touch | Day | Words | The new reason to reply | Spend |
|---|---|---|---|---|
| FU1 | +4 (Tue–Thu) | ≤ 45 | **A second idea**, so it isn't "bumping" | 0 |
| FU2 | +9 | ≤ 40 | **Show one still**: a single JPG made from their public product photo, marked "AI concept, for you only" | ~$0.05–0.30 per lead, **owner approves first**; without approval send FU2-text |
| FU3 | +16 | ≤ 35 | **Their calendar**: a real date that matters to them, plus a two-yes timing question | 0 |

After FU3: silence. Log "no reply" and set one check-in at their next real launch (doc 34 §2.4). Never "just checking in", guilt, fake deadlines or "should I close your file?".

### 5.1 The Foggy Dog
- **FU1:** "One more for the holiday line, Rose: the dog walks the family, the Tartan Plaid walk set leading, the humans being pulled behind. Should the stills follow this one, or the card-photo idea?"
- **FU2 (with one still):** "Made one still so you can judge the look: the card on the fridge, your real bow tie collar. AI concept, just for you. Want the other 4, with Utah or a model pup?"
- **FU2-text (no spend):** "If it helps, the 5 stills come from your own product photos. The embroidery isn't redrawn, and nothing gets posted. Should I start with the bow tie collar, or the walk set?"
- **FU3:** "Holiday ads need to be live by mid-November to catch the card season. Should I send the stills this week, or check back for the Valentine's collection?"

### 5.2 Moment
- **FU1:** "A second Dry January idea, Aisha: a fridge-door camera. Every time the door opens in January, there's one fewer can and one more coupe on the rack. Stills for this one, or the counter idea?"
- **FU2 (with one still):** "One still from the counter idea, built on your real Pink Moment can: Friday 5 pm. AI concept, just for you, and no alcohol cues in frame. Want the other 4 for Pink Moment, or the sparkling line?"
- **FU2-text:** "The 5 stills use your real can photos. I check every frame for alcohol cues before you see it. Should I start with Pink Moment, or the sparkling line?"
- **FU3:** "A Dry January film has to be approved by early December to run on Jan 1. Should I send the stills this month, or check back for Valentine's?"

### 5.3 Fishwife (only after the §4.3 gate)
- **FU1:** "Second idea, Becca: a picnic blanket, everyone's tin open, and one person guarding theirs like a dragon. Stills for this one, or the dinner-party idea?"
- **FU2 (with one still):** "One still so you can judge the look: the empty tin, the bread, the drawer of thirty. Built on your real tin. AI concept, just for you. Want the other 4?" (For a two-yes, end with: "…on the smoked salmon, or the gift tins?")
- **FU2-text:** "The stills use your real tin photos. Your art is never redrawn. Should I start with the gift tins, or the smoked salmon?"
- **FU3:** "Gifting ads need to be live by about Nov 15 to catch December delivery. Should I send the stills this week, or check back for Valentine's?"

### 5.4 AUrate
- **FU1:** "Second idea for the tennis line: a ball boy kneels at the net, and what he hands the umpire is the bracelet, not a ball. Stills for this one, or the necklace net?"
- **FU2 (with one still):** "One still of the court at dusk, built on your 9ct necklace photo, with the stone count checked. AI concept, just for you. Want the other 4, necklace or bracelet?"
- **FU2-text:** "The stills use your product photos, with the real stone count and 'lab-grown' on screen. No AI models. Should I start with the necklace, or the bracelet?"
- **FU3:** "Holiday jewellery ads need to be live before Black Friday (Nov 27). Should I send the stills this week, or check back for Valentine's?"

---

## 6. Objection replies (first-reply stage)

Shape: acknowledge in one line, answer in one or two, then give a two-yes next step (doc 28 §6). Match their length. Reply within 2 business hours. **Never claim clients, results or numbers we don't have.**

**"How much?" / "What does it cost?"**
> Fair question. Three ways people buy: a **Short** (one 15 s film, $1,200), a **Premiere** (the hero film plus a 6 s cut, hook variants and stills, $2,500), or a **Season** (a new film every month, $3,500/mo). For [brand] I'd start with the Premiere, because [holiday + the walk set / Dry January] gives you a real test set. The 5 stills stay free either way. Should I make them for [A], or [B]?

**"Too expensive."**
> Understood. We can cut scope, not quality. The Short is $1,200: one film, no variants. What were you hoping to spend on this? (If they name a number below $1,200: offer a smaller scope, never a discount on the same scope. Doc 34 §2.1.)

**"We do AI in-house" / "our team already uses AI"** (LESSONS: the real competitor is their own AI team.)
> Makes sense. Most brands your size have someone prompting now. What we add is what in-house AI usually skips: one concept with a punchline your product causes, physics checked shot by shot, sound mastered to platform loudness, and every claim checked against your label. Easiest test: let us make the 5 stills, put them next to your team's, and if theirs are better you've lost nothing. Should I aim them at [A], or at [B]?

**"AI looks fake" / "our customers hate AI"**
> You're right, and the numbers back you: most people say they trust ads they suspect are AI less. That's why we build the world and the joke with AI, but your product shots and any proof stay real, and there are no AI people. And it's why you see stills first: if your [can / collar / necklace] doesn't look exactly like itself, we stop there. Is it the product looking fake you're worried about, or customers knowing it's AI?
(Then doc 34 §3.8 R2/R3. If we use AI, we disclose it. Never promise "no one will notice".)

**"Send examples" / "Do you have a portfolio?"**
> Sure: [one link to a 30–40 s reel]. To be straight with you, those are spec films for brands we invented, because we don't show anyone's product without permission. Stills on your own [product] will tell you far more than my reel. Should I make them for [A], or [B]?
**Blocked until a public reel URL exists** (§8). Until then: "I'll send the reel as a private link today." The owner sends a private unlisted link by hand. Never attach a 50 MB video.

**"Who else have you worked with?"**
> Honest answer: no paid clients yet. You'd be one of the first. That's why the stills are free, and for a first project the balance is due only when you approve the final cut. (Only if the owner has agreed to that term; doc 28 §6.)

**"How did you get my email?" / "Is this spam?"**
> From the contact address on your site. This is a one-off note from me, not a list. If you'd rather not hear from me, say so and that's it.

**"Not now" / "After Q4"**
> Understood. Is it a "January" not now, or an "after the [launch]" not now? I'll check back then, once.
(Log the date. Send one note then. Nothing in between.)

---

## 7. Pre-send checklist, KPIs and what to measure

### 7.1 Before the owner says "send"
1. The **Meta Ad Library** is checked by hand (US, active, brand name). 0 active ads → drop the lead to WARM.
2. **The product is public**: it's in the site navigation or on IG or in press, and isn't only in `products.json`. No tags like `redirect-to-404`, `hidden` or `draft`, and it's available.
3. **No back-end or stale data** in the message: ad counts, dates scraped from JSON, job posts, revenue.
4. **The sender exists**: the owner's IG has a real name, photo and bio ("Itamar · VXO · AI product films") plus at least 3 posts. The email has a real name and postal address. If the domain is live, it's in the signature.
5. The message passes §3 (names the sender, one visible observation, the idea, AI once next to what stays real, "5 free stills", two-yes CTA, no superlatives, length).
6. Day and time: Tue–Thu, 8–10 am in the founder's time zone.
7. Logged in `launch/tracker.csv` (or `leads/PIPELINE.md`) on the same day: channel, variant code, date, and the next follow-up date.

### 7.2 Daily limits
At most ~10 new DMs and ~15 new emails a day, by hand, spaced out, never identical. Follow-ups count toward the email total.

### 7.3 What to measure (so the first 30 sends teach us something)
| Metric | Target after 30 first touches | If below |
|---|---|---|
| Positive reply rate (said yes to stills, or asked a real question) | ≥ 5 % (≥ 2 of 30) | Change the **channel and sender** first (founder's own account, warm-up), then the idea, last the wording |
| Reply by channel (founder account / brand DM / brand inbox) | Know which wins | Move volume to the winner |
| Stills → paid | ≥ 1 in 5 [inf] | The stills or the price are the problem; review doc 34 §2.7 |
| Unsubscribes or spam complaints | 0 | Stop and review the list quality |

Variant codes: `DM-v63`, `EM-v63`, `FU1`, `FU2-img`, `FU2-txt`, `FU3`.

---

## 8. What only the owner can do (blocking first)

1. **Make the sender real.** Register `vxo.studio` (or the chosen domain), deploy `site/` (Cloudflare Pages project `studio-site`), and set up the owner's IG with his name, a photo, a bio and 3+ posts (spec films labelled AI). Without this the reply rate is capped, because every founder checks the sender. *(Blocking.)*
2. **Provide a postal address** for the email footer (a PO box or virtual mailbox is fine). *(Blocking for email.)*
3. **Fix the site's "one take, no cuts" promise**, or ask the site agent to: it contradicts the multi-shot films we pitch and LESSONS. *(Before any link goes out.)*
4. **Approve the channel rule**: the owner sends DMs by hand from his own account, and to founders' own public business accounts where they exist.
5. **Approve the FU2 still** (~$0.05–0.30 per lead, frames-only mode). Otherwise FU2-text goes out.
6. **Decide on the risk-reversal term** ("balance due on approval of the final cut") before it is ever offered.
7. **Send.** Start Tue 13 Oct with The Foggy Dog and Moment. Fishwife after the §4.3 gate, AUrate last. Then clear the backlog: the ~30 already-drafted `HOT_NEW_30` leads, after the §7.1 checks and a rewrite to §3. At ~10 a day, that's 30 first touches in a week, which is the first real data VXO will ever have.
8. **Choose one playbook.** Mark `launch/outreach.md` (the $750 sprint, price in email 1, "reply no" footer) as superseded for DTC first touches, so no agent uses it.

---

## 9. What this supersedes
- `vxo-leads` §3 (the old 4-step, ≤60-word template): replaced by §3 here and the new skill §3/§3b.
- Doc 28 §5 (4 touches) and doc 34 §4.2 (21-day cadence) **for the first touch and follow-ups only**. The call, pricing, contract and later-stage objection playbooks in 28 and 34 still stand.
- `launch/outreach.md` DTC templates: superseded for DTC (old offer and pricing). The agency templates there are outside this doc's scope.

## Sources
- Instagram: [TechCrunch, Aug 2023](https://techcrunch.com/2023/08/03/instagrams-new-feature-protects-users-from-unwanted-images-and-videos-in-dms) · [Neowin](https://www.neowin.net/news/instagram-is-changing-how-unknown-users-can-or-cant-text-you/) · [Instagram Help, professional inbox](https://help.instagram.com/ipad-app/1264898753662278) · [Meta Instagram Messaging docs](https://developers.facebook.com/docs/instagram-messaging/overview) · [Inrō deliverability](https://www.inro.social/blog/instagram-dm-deliverability) · [DM Champ](https://dmchamp.com/tools/cold-dm-outreach-roi/)
- Email data: [Instantly 2026](https://instantly.ai/cold-email-benchmark-report-2026) · [Lemlist 2026 benchmarks](https://lemlist.com/blog/cold-email-benchmarks/) · [Hunter State of Cold Email](https://hunter.io/the-state-of-cold-email) · [Hunter word count](https://hunter.io/blog/cold-email-word-count) · [Lavender benchmark](https://www.lavender.ai/blog/the-cold-email-benchmark-report) · [Something Inc on Lavender data](https://somethinginc.com/blog/cold-email-sounds-like-ai-lavender-data/) · [Reply.io images](https://reply.io/images-gifs-in-cold-emails) · [Reply.io attachments](https://reply.io/emojis-attachments-impact-cold-email/) · [Lemlist images](https://www.lemlist.com/blog/images-in-cold-emails) · [Woodpecker](https://woodpecker.co/blog/cold-email-benchmarks/) · [Prospeo](https://prospeo.io/s/cold-email-benchmarks) · [Modern Inbound](https://moderninbound.com/blog/cold-email-for-ecommerce-agencies)
- AI attitudes: [AAAA / Harris Poll](https://www.aaaa.org/blog/consumers-are-sick-and-tired-of-hearing-about-ai-all-the-time/) · [YouGov Australia](https://yougov.com/articles/54818-45-of-australians-say-ai-generated-ads-would-make-them-trust-a-brand-less) · [Advanced Television / DoubleVerify](https://www.advanced-television.com/2026/08/06/study-ai-slop-poses-growing-risk-to-brand-trust/)
- Law: [FTC CAN-SPAM guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) · [FTC 2025 penalty amounts](https://search.ftc.gov/news-events/news/press-releases/2025/02/ftc-publishes-inflation-adjusted-civil-penalty-amounts-2025)
- Lead facts checked this run [m]: `drinkmoment.com` homepage ("all of the ritual / none of the regret"), `products.json` and `/products/<handle>.js` for Moment, The Foggy Dog, AUrate and Fishwife (tags, availability, creation dates); DNS for `vxo.studio` via dns.google (NXDOMAIN); `site/src` text. Fishwife at Aldi: [IntraFish](https://www.intrafish.com/markets/fishwife-continues-retail-growth-with-discounted-offerings-at-aldi/2-1-2032646).
