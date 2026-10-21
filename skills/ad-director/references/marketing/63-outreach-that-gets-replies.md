# 63 · Outreach that gets replies: the first message, the follow-ups and the objections

Researched 2026-10-09. No money was spent, nobody was contacted, nothing was sent. This doc is the **single source for the first touch, the follow-ups and the first objection replies**. For the rest of the sale it builds on doc 28 (sales mastery: subject lines, deliverability, the discovery call) and doc 34 (objection mastery). Where 28 §5, 34 §4.2 or `research/ai-video-reels/launch/outreach.md` disagree with this doc about the first touch or the follow-ups, **this doc wins** (see §9).

**Labels.** **[v]** = a vendor figure (the vendors sell outreach tools; their samples are mostly B2B SaaS, so read them as directional). **[c]** = a platform's or company's own statement. **[m]** = I checked it myself this run (curl, DNS, Shopify JSON). **[inf]** = my inference. **[law]** = a legal point, not legal advice.

---

## 0. The honest answer: is this the best we can reach?

No. The four drafts in `leads/2026-10-09.md` are well researched, but **the things stopping VXO from getting a paid client aren't in the wording**. In order of damage:

1. **Nothing has ever been sent.** About 85 brands have drafted messages (`HOT_NEW_30`, `HEAT_50`, `PROSPECTS_50` and today's 4). Every pipeline line reads "found", and `launch/tracker.csv` holds only EXAMPLE rows [m]. With no sends there are no replies and no data, so every rule we use is a vendor average.
2. **The sender can't be checked.** A founder who gets a cold DM opens the sender's profile and Googles the name. Today she would find nothing. `vxo.studio` doesn't resolve (DNS NXDOMAIN on 2026-10-09 [m]), the site in `site/` isn't deployed, a web search for "vxo.studio" returns other companies (an Indonesian "VXO" creative agency, Vexo) [m], and every email draft still carries `[Owner name]` and `{BUSINESS_ADDRESS}` placeholders. Without a postal address, **the emails can't legally be sent** (CAN-SPAM [law]). The rule "the portfolio goes in the first reply" has no portfolio to link to.
3. **Instagram allows one text-only message.** Someone who doesn't follow the recipient gets **one message, text only**, until the recipient accepts. No photo, no follow-up DM. It lands in the Requests folder, which has to be opened on purpose ([TechCrunch, Aug 2023](https://techcrunch.com/2023/08/03/instagrams-new-feature-protects-users-from-unwanted-images-and-videos-in-dms); [Neowin](https://www.neowin.net/news/instagram-is-changing-how-unknown-users-can-or-cant-text-you/)) [c]. Re-checked 2026-10-10: no source reverses it (a 2026 SmartHouse piece repeats it); Instagram's own help page did not load logged-out, so it stays a reported rule [c] and we keep the safe plan (one DM, follow-ups by email). **Re-checked 2026-10-20 on Meta's own newsroom page** ([about.fb.com, 27 Jun 2023, message-request bullet updated 25 Nov 2024, page revised 30 Jun 2025](https://about.fb.com/news/2023/06/parental-supervision-and-teen-time-management-on-metas-apps/)) [c]: Meta confirms the **text-only** half ("We limit the message requests people can send to someone who doesn't follow or isn't already connected to them to text-only messages"; no images, videos or voice notes until accepted). The current page names **no count limit**; the "one message" half rests only on 2023 press (TechCrunch, Neowin) and the in-app notice they quote. Instagram's help centre still renders an empty shell logged-out (not worked around). Operating rule unchanged and conservative: **one text-only DM, no link-preview bait, no second DM**; follow-ups by email only. On a brand account a social or CX person reads it, not the founder. So a DM can't carry a follow-up sequence or a frame, and our "follow-up" plan has to run by email.
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
| Baseline reply rate (email) | Average 3.43 %, top quartile 5.5 %+, top decile 10.7 %+ (2025 campaigns). Hunter: 4.5 % average | [Instantly 2026](https://instantly.ai/cold-email-benchmark-report-2026) [v, re-read on Instantly's own page 2026-10-19: 3.43 % / 5.5 %+ / 10.7 %+ confirmed; data 1 Jan–18 Dec 2025; **58 % of replies come from step 1, 42 % from follow-ups**]; [Hunter](https://hunter.io/outreach-calculator) [v] | Plan for 5–10 % on hand-researched founders; anything under 3 % after 30 sends means the channel or offer is wrong, not the adjectives |
| Small lists | Campaigns of 21–50 recipients average 6.2 %, 500+ average 2.4 % (Hunter). Under 50: 5.8 % vs 2.1 % at 1,000+ (Woodpecker) | via [Instantly/Lemlist summaries](https://lemlist.com/blog/cold-email-benchmarks/) [v]; [Woodpecker](https://woodpecker.co/blog/cold-email-benchmarks/) [v] | Our 1:1 model is on the right side of this |
| Replies ≠ yeses | In one dataset 14 % of replies were positive, 30 % negative, 45 % auto-replies | [Prospeo summary](https://prospeo.io/s/cold-email-benchmarks) [v] | Count **positive** replies (frames requested). That's the KPI |
| Personalisation depth | Two custom attributes: 5.6 % vs 3.6 % replies (31M emails). Real personalisation vs a merge-tag template: +50–250 % | [Hunter, State of Cold Email](https://hunter.io/the-state-of-cold-email) [v]; Lavender via [Something Inc](https://somethinginc.com/blog/cold-email-sounds-like-ai-lavender-data/) [v] | One observation **with a point of view** about something the customer can see. Not three scraped facts |
| Length | Hunter (34M emails, 2022–24): reply rate barely moves with length, 3.4–4.5 % from 0 to 200+ words; 20–39 words was best at 4.5 % | [Hunter word count](https://hunter.io/blog/cold-email-word-count) [v] | Length isn't the lever. Clarity is. A DM is still read on a phone in a Requests list, so 35–50 words |
| Images in email | Emails with images: 2.62 % vs a 3 % baseline (−12.7 %). File attachments: 4 % (+33 %, small sample). Lemlist claims personalised images lift replies (vendor of image tools) | [Reply.io research](https://reply.io/images-gifs-in-cold-emails), [Reply.io attachments](https://reply.io/emojis-attachments-impact-cold-email/) [v]; [Lemlist](https://www.lemlist.com/blog/images-in-cold-emails) [v] | **No image in touch 1.** The single frame goes in follow-up 2, as one JPG in the same thread, once the owner approves the ~$0.10 spend (§5) |
| Instagram DM to a non-follower | One message, text only, until accepted; it lands in Requests. Templated text and bursts to new people push messages into "Hidden Requests" and risk restrictions | Text-only: [Meta newsroom, updated 2024-11-25](https://about.fb.com/news/2023/06/parental-supervision-and-teen-time-management-on-metas-apps/) [c, verified 2026-10-20]; one-message count: [TechCrunch](https://techcrunch.com/2023/08/03/instagrams-new-feature-protects-users-from-unwanted-images-and-videos-in-dms) [press, 2023 only]; [Instagram help](https://help.instagram.com/ipad-app/1264898753662278) [c]; [Inrō](https://www.inro.social/blog/instagram-dm-deliverability) [v] | The DM must stand alone. Max ~10 new DMs a day by hand, each one different. Warm first: the owner follows and leaves one genuine comment 1–3 days before (practitioner reports of large lifts are anecdotal [v]) |
| Cold DM reply rate | 3–12 % "typical" for cold DMs (vendor calculator); 50 %+ claims are all for warm, engaged contacts | [DM Champ](https://dmchamp.com/tools/cold-dm-outreach-roi/) [v] | Treat DM and email as about equal. Use **both** for the top leads: DM on day 0, email on day 1 |
| Founder inbox load | An 8-figure DTC founder gets "30–100 cold pitches a day"; "we help ecommerce brands grow" is the sentence they've heard 200 times | [Modern Inbound](https://moderninbound.com/blog/cold-email-for-ecommerce-agencies) [v] | Never describe VXO first. Lead with their product and our idea |
| Follow-ups | 4–7 step sequences, 3–4 days apart, perform best; a reply-style step 2 beats a formal one | Instantly 2026 via [Lemlist](https://lemlist.com/blog/cold-email-benchmarks/) [v] | 1 first touch + 3 follow-ups over ~16 days (§5), each with a **new** reason to reply |
| Day | Wednesday best, then Tuesday and Thursday; Monday is overloaded and Friday is weekend mode. **Re-read 2026-10-19 on the primary pages:** Instantly's own report (data 1 Jan–18 Dec 2025, "billions" of interactions) says "Wednesday is highest" and its 21 Sep 2026 blog says "Tuesday and Wednesday saw peak reply rates", with no per-day numbers [v]. Smartlead's 2026-H1 benchmark (850M+ emails) calls best day "mostly a myth": reply rate 0.82–0.91 % across days, Wednesday slightly ahead (110 contacts per reply vs Saturday 122) [v]. Both are email data; for IG DMs it is [inf] | [Instantly report](https://instantly.ai/cold-email-benchmark-report-2026), [Instantly blog](https://instantly.ai/blog/best-time-to-send-cold-email/), [Smartlead](https://www.smartlead.ai/benchmarks) [v] | Send Tue–Thu, 8–10 am in the founder's time zone. The day effect is small (Smartlead: ≤0.09 pt), so a ready wave that misses its day rolls to the **next** Tue–Thu slot, never a week later to chase "Wednesday" (2026-10-19). Today (Fri 9 Oct) is a bad send day; Mon 12 Oct is Columbus/Indigenous Peoples' Day. **First sends: Tue 13 Oct** |
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
- **It reads as a threat to her own staff (WEAKNESSES #16).** Finn & Gray's public case study says they shot Foggy's photos and monthly stop-motion pieces until a full-time in-house hire took over [c, undated]. Someone on her team owns content. A message that implies "replace your content person with AI" gets forwarded to exactly that person, who has every reason to kill it.

**Positioning (owner decision 14, approved 2026-10-09):** VXO is the **scenario layer her content lead can't shoot**: a staged family card shoot, a crowd, a snowstorm, built around her real collar and a real photo of Utah. We don't replace photos, stop-motion or social. The stills and the shot list go to her content lead to reuse. Never write "instead of", "replace", "no shoot needed" or "cheaper than a team".

**New DM (to Rose's own public business account if the owner finds one, otherwise @thefoggydog; 54 words; rewritten 2026-10-09 for decision 14):**
> Hi Rose, Itamar from VXO. Film idea for the Gingerbread Man bow tie collar: a Christmas-card shoot where the photographer zooms in until every human is cropped out and only Utah is left. Cut to the card on the fridge. Want 5 free stills and a shot list, for you or your content lead?

*Why the CTA works:* both options are free and equally easy, and the second one hands the work to her own team instead of competing with it. "Utah" in the idea shows we know whose brand this is. The AI line moves to the email and the first reply, so the one-shot DM spends its words on the joke.

**New email (woof@thefoggydog.com, day 1):**
> **Subject:** Utah's holiday card
>
> Hi Rose (or whoever reads woof@, could you pass this to Rose?),
>
> Following up my Instagram note: a 15 s film for the Gingerbread Man bow tie collar. A Christmas-card shoot where the photographer zooms in until every human is cropped out and only the dog is left. Cut to the card on the fridge.
>
> A shoot day can't stage that, so I build it with AI around your real collar and a real photo of Utah.
>
> Want 5 free stills plus a shot list your content lead can reuse, on the collar or the Evergreen Candy Canes walk set?
>
> {footer §4.0}

(88 words in the body.) **CTA stock, checked live 2026-10-09 [m]:** Gingerbread Man Embroidered Bow Tie Collar $52, 8/8 variants available; Evergreen Candy Canes Embroidered Collar Walk Set $102, 6/6 available; both published 9/29 and listed in `/collections/holiday-shop`, which the homepage links. The Tartan Plaid walk sets (3/6 sizes) are out of every Foggy draft. Re-check on the send day.

### 4.2 Moment: Aisha Chottani

**How Aisha reads the old DM:**
- **The old drafts carried the alcohol and claims cues she fears most (WEAKNESSES #11, owner decision 10, approved 2026-10-09):** a "coupe" (a cocktail glass), ice plus a record going on at Friday 5 pm (cocktail hour), and a Saturday 7 am "fresh morning" payoff (an implied no-hangover benefit, which is the picture making the claim). All three are gone. The new idea uses her real can or a plain tumbler, no bar ritual, no morning-after, and no calm, mood, sleep or health outcome. If she later insists on "no hangover" or "calm" on screen, we walk away.
- Quoting "all of the ritual, none of the regret" back to her: it's her own homepage line [m], so praising it proves we saw her homepage, nothing more.
- The idea is strong and calendar-true (Dry January is her Super Bowl; doc 57).
- ~~**Risk she will spot:** "Saturday 7 am, already heading out" implies a no-hangover benefit.~~ **Superseded 2026-10-09:** the Friday/Saturday concept is dropped entirely, because no Saturday shot can avoid reading as "recovered". Doc 57 and LESSONS ban "hangover-free" language, and "the picture is the claim". The replacement ("Calendar") sells the ritual itself: the punchline is that she keeps reaching for the can after January ends.
- She runs ~24 new creatives a week (June snapshot), so she has a creative machine. Her real objection will be "we have a team". The message should name the gap we fill (motion around the real pour), **without quoting stale ad counts**.
- ~~"Sparkling Collection, or Pink Moment"~~ **CTA swapped 2026-10-09 [m]:** Pink Moment is in stock but is an October pack ("for the month when the color carries a little more weight") and isn't in the site navigation, so it's wrong for a Dry January film. New options: **the sparkling collection** (`/products/moodboostsparklingcollection`, $59, 18/24/36 packs all available, linked from the homepage "Shop Now") and **strawberry rose (12 Pack)** ($40, available, in the homepage flavour slider). Avoid cherry hibiscus as a CTA: its own page says it "channels the complexity of red wine" (an alcohol cue). Re-check on the send day.

**New DM (@drinkmoment, or Aisha's own public account; 55 words; rewritten 2026-10-09 for decision 10):**
> Hi Aisha, Itamar from VXO. Dry January film: a locked camera on a counter under a paper calendar. Jan 1, a can cracks open. Hard cuts, a page and a flavour a day. Then February: the page flips and the hand still reaches for a can. Want 5 free stills, sparkling collection or strawberry rose?

**New email (hi@drinkmoment.com, day 1):**
> **Subject:** Then February
>
> Hi Aisha (team, could you pass this to Aisha?),
>
> A Dry January idea I sent on Instagram: one locked camera on a kitchen counter under a paper calendar. Jan 1, a can cracks and pours into a plain tumbler. Hard cuts, a page and a flavour a day. Then the page flips to February, and the hand reaches for a can anyway.
>
> I build it with AI, but your real cans stay real, there's no sip on screen, and every frame is checked for alcohol cues.
>
> Want 5 free stills, on the sparkling collection or strawberry rose?
>
> {footer §4.0}

(88 words in the body.) **Copy rules for every Moment message:** no coupe, wine, flute or cocktail glass (her can, or a plain straight-sided tumbler); no ice-and-record, candle or "5 pm" cocktail-hour framing; no morning-after shot; no "hangover", "calm", "mood", "sleep", "focus", "regret" or "good for you", in words or in pictures.

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
- **FU1:** "One more for the holiday line, Rose: the dog walks the family, the Evergreen Candy Canes walk set leading, the humans being pulled behind. Should the stills follow this one, or the card-photo idea?"
- **FU2 (with one still):** "Made one still so you can judge the look: the card on the fridge, your real bow tie collar. AI concept, just for you. Want the other 4 and the shot list, for you or your content lead?"
- **FU2-text (no spend):** "If it helps, the 5 stills come from your own product photos, plus a shot list your team can reuse. The embroidery isn't redrawn, and nothing gets posted. Should I start with the bow tie collar, or the walk set?"
- **FU3:** "Holiday ads need to be live by mid-November to catch the card season. Should I send the stills this week, or check back for the Valentine's collection?"

### 5.2 Moment
- **FU1:** "A second Dry January idea, Aisha: a fridge-door camera. Every time the door opens in January there's one fewer can, until someone tapes their name to the last one. Stills for this one, or the calendar idea?"
- **FU2 (with one still):** "One still from the calendar idea, built on your real strawberry rose can: Jan 1, the tab just cracked. AI concept, for you only, no alcohol cues in frame. Want the other 4, on strawberry rose or the sparkling collection?"
- **FU2-text:** "The 5 stills use your real can photos. I check every frame for alcohol cues before you see it. Should I start with the sparkling collection, or strawberry rose?"
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
> Makes sense. Most brands your size have someone prompting now. What we add is what in-house AI usually skips: one concept with a punchline your product causes, physics checked shot by shot, sound mastered to platform loudness, and every claim checked against your label. We don't replace your team; we build the scenes they can't shoot, around your real product, and hand them the stills and the shot list to reuse. Easiest test: the 5 stills are free, and your team decides if they earn a place. Should I aim them at [A], or at [B]?
(LESSONS 2026-10-09: never pitch an AI film as replacing a brand's own creative staff.)

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

### 7.4 Markdown regimes of the queued brands (measured 2026-10-16) [m]
Read from each brand's public `/products.json` on Fri 16 Oct, five weeks before Black Friday. "Marked" = at least one in-stock variant with a compare-at above its price; "final" = a Final Sale / Final Farewell / Last Chance tag or title; "new" = published since 16 Sep.

| Brand | Products | Marked | Median depth | Final | New (30 d) | New and marked | Regime |
|---|---|---|---|---|---|---|---|
| LAKE Pajamas | 379 | 0 % | — | 33 | 95 | 0 | full-price house |
| Printfresh | 2,248 | 4.6 % | 50 % (old bundles) | 0 | 598 | 36 (bundles only) | full-price house; launches weekly (a "10.13.26 Launch" of 83 products) |
| Dandelion Chocolate | 202 | 0 % | — | 0 | 10 | 0 | full-price house |
| Brackish | 460 | 0 % | — | 0 | 36 | 0 | full-price house; Maroon collection live 15 Oct |
| Kinn | 1,132 | 3.7 % | 12 % | 277 | 46 | 0 | full-price house; Final Sale only on limited/archive pieces |
| The Foggy Dog | 915 | 26.8 % | 11 % | 0 | 224 | 80 | standing promo (shallow "bow-promo" compare-at) |
| Cuddle Clones | 659 | 77.5 % | 25 % | 0 | 302 | 275 | standing promo (compare-at is the list price); depth moved 67 % → 33 % on the pajamas between 12 and 16 Oct |
| Sunday Citizen | 408 | 33.8 % | 20 % | 40 | 18 | 1 | clearance (old lines "Last Chance"; new launches full price) |
| Little Beast | 180 | 18.9 % | 21 % | 17 | 17 | 5 | clearance (Final Sale on collabs and returns) |
| Dana Rebecca Designs | 1,019 | 6.4 % | 20 % | 65 | 42 | 22 | clearance of retired lines ("Final Farewell", 3 new on 15 Oct) next to weekly full-price "New Arrivals" |

What it means for the films [inf]:
- **Full-price houses** spend on new collections, and none has started holiday markdowns. Pitch their newest full-price line. This is also where a Season plan (one film per drop) fits best, since they drop weekly (Printfresh, Dana Rebecca) or monthly (Brackish, LAKE).
- **Standing-promo brands** always show a "sale" price, so a MARKDOWN flag tells us nothing. Track the promo price itself. A change in depth is the signal (Cuddle Clones got shallower, which reads as a list-price reset before the holiday push, not clearance [inf]). Messages name no price.
- **Clearance brands** are retiring old lines. Pitch only what was published in the last ~60 days at full price (Sunday Citizen's Ciel love seat, 24 Sep). Never a Last Chance or Final Farewell piece.
- None of the ten had a sitewide Black Friday sale yet on 16 Oct. Re-measure on Tue 20 Oct and on Mon 2 Nov. The first brand to go sitewide moves its follow-up angle to an evergreen, offer-free film (LESSONS 2026-10-10: the evergreen twin).


### 7.5 Ad-count moves as a heat signal (measured 2026-10-09 → 2026-10-17) [m]
Question: when a queued brand's active Meta ad count falls, is it cutting spend (cooler) or rotating creative before the holiday push (hotter)? All 19 queued Pages were read with `ad_library.py page` (US, active, 2 agreeing loads each; Saranoni 1 load) on 10-09 and again on Sat 17 Oct. "Fresh flow" = how many of the top ~30 cards started in the last 30 days, and how old the newest ad is.

| Brand | Active 10-09 → 10-17 | Change | Top cards started ≤30 d (10-09 → 10-17) | Newest ad (age on 10-17) | Formats in top cards, 10-17 | Read |
|---|---|---|---|---|---|---|
| LAKE Pajamas | 221 → 103 | **−53 %** | 25 → 25 | 10/16 (1 d) | DCO 27, DPA 2, video 1 | **rotation**: old ad IDs retired, new ones still going up daily |
| Vosges Haut-Chocolat | 73 → 36 | **−51 %** | 8 → 19 | 10/16 (1 d) | DCO 28 | **rotation into holiday**: fewer, newer, almost all DCO |
| The Foggy Dog | 218 → 168 | −23 % | 19 → 18 | 10/07 (10 d) | DCO 19, DPA 7, video 4 | steady flow, pruning |
| Kinn | 95 → 79 | −17 % | 6 → 13 | 10/13 (4 d) | DCO 21, video 8 | rotation |
| Cuddle Clones | 174 → 148 | −15 % | 18 → 12 | 10/03 (14 d) | DCO 26 | slowing; watch |
| **Hawkins New York** | 93 → 81 | −13 % | 5 → **0** | **9/11 (36 d)** | DPA 11, carousel 7, DCO 4 | **cooling**: nothing new in 5 weeks |
| Printfresh | 336 → 320 | −5 % | 11 → 16 | 10/08 (9 d) | image 14, video 8, DCO 8 | steady |
| Dandelion, Little Beast, Dana Rebecca, KREWE, Legendary, Equator, Saranoni (1 load) | flat (±2 %) | — | 13 / 8 / 20 / 29 / 6 / 9 / 3 | 10/01, 10/06, 10/09, 10/16, 10/13, 10/13, 10/07 | — | steady; Saranoni stays "stale winners" (21 of 30 running 60+ d) |
| Brackish | 60 → 69 | +15 % | 30 → 23 | 10/15 (2 d) | image 21 | Maroon launch |
| THATCH | 16 → 21 | +31 % | 16 → 21 | 10/16 (1 d) | DCO 18 | ramping |
| Sunday Citizen | 306 → 413 | +35 % | 30 → 19 | 10/02 (15 d) | DCO 14, DPA 10 | ramping, but no new ad in 2 weeks |
| STONE AND STRAND | 19 → 21 | +11 % | 17 → 18 | 10/16 (1 d) | DCO 7, image 7, video 6 | steady |
| Alexis Bittar | 27 → 79 | **+193 %** | 27 → 20 | 10/16 (1 d) | DCO 14, DPA 9 | **ramping hard** (FW26 + handbags) |

What it shows:
- [m] The two biggest drops of the week (LAKE −53 %, Vosges −51 %) belong to brands with the **freshest** flow: newest ad 1 day old, 19–25 of the top 30 started this month. The one brand with no fresh flow at all (Hawkins: zero ads started in 30 days, newest 36 days old) fell only 13 %. **The size of a drop does not tell cooling from rotation; the fresh flow does.**
- [m] The brands that shrank hardest now run almost only DCO cards (LAKE 27 of 30, Vosges 28 of 30). [inf] They are folding many single ads into a few dynamic ones (the "consolidate under Andromeda" advice agencies give for 2026 [v]), which cuts the count without cutting spend. A falling count on a DCO-heavy page reads as consolidation first.
- [inf] A brand rotating creative five weeks before Black Friday is **buying creative right now**: that is the warmest moment to land a film idea, not a reason to wait.

The rule (in `vxo-leads` §1):
- **Hold (cooling):** no ad started in the last 21 days AND at most 2 of the top cards started in the last 30 days, whatever the count does. Re-check weekly; one new ad lifts the hold.
- **Rotation (keep, note as warm):** active count down more than 30 % in a week, but the newest ad is ≤ 7 days old or ≥ 10 of the top cards started in the last 30 days.
- **Watch:** newest ad 14–21 days old (Cuddle Clones, Sunday Citizen, Dandelion on 10-17). Re-read on the send morning.
- Never quote any of these counts in a message (rule 2 above).

---

### 7.6 Story share in the wave-A brands' video ads (measured 2026-10-19) [m, frame-read, not model-read]
**Question.** Ipsos (May 2026, doc 45 D37b) found fully-AI ads chose a story 30 % of the time vs 49 % for ads overall, and story drove effectiveness. How many of our leads' own video ads tell a story, and does that change which pitch each brand gets?

**Method.** One Ad Library Page per call (logged-out top ~30 cards; Printfresh returned no cards twice, and Brackish runs 1 video card in 30, so 8 brands were read). Every distinct video creative was downloaded to the scratchpad (never committed), cut into a 16-frame contact sheet and read by eye. Ratio versions of one creative count once (LAKE "The Ornament" 30 s + 10 s cut = 1). 24 creatives, 4–69 s. Classes:
- **S, scripted story:** characters, a situation and a turn.
- **T, testimonial story:** a real person's personal arc.
- **P, premise hook over a demo:** a gag or problem line, then the product shown.
- **D, pure demo:** process, try-on, unboxing, haul, loop, review card, catalogue or narrated explainer.

| Brand | S | T | P | D | What the long-runners (≥60 d) are |
|---|---|---|---|---|---|
| LAKE | 1 ("Chapter 1: The Ornament", a cinematic road trip) | | | 1 (creator gift unboxing) | none ≥60 d in the sample |
| Kinn | 1 ("Family Legacy": kids "approve" the collection in a boardroom, 158 d) | | | 2 (wrist POV on a crosswalk, 158 d; wrist stack) | 1 S + 1 D |
| Cuddle Clones | | 2 (memorial plush: a mother and a toddler, 86 d; "Wait, is that real?" creator) | 1 (PJ mirror selfie, then cut to the dog) | 2 (bobblehead airbrush process + money-back line, 194 d; unboxing reactions) | 1 D + 1 T |
| Dana Rebecca | | 1 (staff vox pop, "What was your first DRD piece?") | 1 (UGC one-liner: "Thank god my name isn't Jessica") | 1 (review-quote card) | none |
| Sunday Citizen | | | 1 (text-message hook "Sorry, I can't, I'm busy", then a chair review) | 2 (comforter review demo; "Why is everyone obsessed?" 3 steps: **box → unbox → expands**) | none |
| Little Beast | | | | 3 (haul try-on, 173 d; dog-in-bag loops, 102 d and 47 d) | 2 D |
| Dandelion | | | | 2 (Tokyo Gateau process "POV", 151 d; Advent explainer) | 1 D |
| The Foggy Dog | | | 1 ("a dog bed they'll choose over your couch") | 2 (bed set-up; animated jacket catalogue) | none |
| **Total (24)** | **2 (8 %)** | **3 (13 %)** | **4 (17 %)** | **15 (63 %)** | **7 long-runners: 5 D, 1 S, 1 T** |

**What it says.**
- [m] Only **5 of 24 (21 %)** carry a story arc, and **9 of 24 (38 %)** use any narrative device. Our leads run mostly demos, and 5 of their 7 sampled long-runners are pure demos (the oldest is Cuddle Clones' 194-day airbrush-process video).
- [m] Only 2 brands run scripted fiction, and both are long-runners or a series: LAKE's "Chapter 1" film and Kinn's 158-day "Family Legacy". The 3 testimonial stories all rest on real people, which an AI film may never play (FTC rule, LESSONS 2026-10-09: proof slot).
- [inf] Against Ipsos's 49 % for ads overall, these brands under-use story. So story is the gap we fill, but the pitch must ride on the format that already earns their money (Ipsos: the best fully-AI ads reused the brand's long-running format).

**Rule: pitch type per brand.** Applied in `vxo-leads` §3 step 3 and `vxo-film` Step 1.
- **Story house** (runs scripted fiction: LAKE, Kinn): a story pitch is native.
- **Testimonial house** (Cuddle Clones, Dana Rebecca): pitch a scripted gag, never a fake testimonial. Keep a proof slot for their real customer clip.
- **Demo house** (Sunday Citizen, Little Beast, Dandelion, Foggy): **the punchline has to be their own demo.** The product doing its job is the payoff of our story. Sunday Citizen's own long-running demo is "box → unbox → expands", and Q-6's stairwell gag ends on exactly that, so the pitch rides their proven format.

**Check of the ten queued DMs:** all ten already fit their house. Q-1 and Q-10 are stories. Q-7 and Q-9 are scripted scenes with no testimonial. Q-3, Q-4, Q-5 and Q-6 end on the product doing its job. No DM changes.

### 7.6b House read for wave B (measured 2026-10-20) [m, frame-read, not model-read]
Same method as §7.6: one Ad Library Page per call (logged-out top cards), every distinct video downloaded to the scratchpad (never committed), a 12-frame contact sheet read by eye. 8 wave-B Pages (Hawkins is on hold). **KREWE and Vosges returned 0 cards on 2 calls each** (logged-out rate limit; not worked around), so they stay unread. **Equator** served 30 cards with **0 video** (20 IMAGE, 8 DCO stills, 2 carousels). 11 distinct videos read, 7–42 s.

| Brand | Cards read · video cards | Videos read (age) | House |
|---|---|---|---|
| Legendary Foods | 18 · 1 | 1 P/D: a stylised "maple tapped from the tree" pour onto the donut, ending on supers "20g PROTEIN", "<1g SUGAR", the box on a stump (6 d) | **Demo house** (stylised product demo; mostly carousels and DPA) |
| Equator Coffees | 30 · 0 | none (all stills) | **Stills house**: no video in the top 30 |
| Saranoni | 30 · 19 | 1 S, cause story "A blanket can do more than keep you warm" (Cambodia, West Africa, Syrian refugees; **315 d**); 1 T, UGC mom review of the Lush Toddler blanket (**129 d**); 1 T-style UGC montage "The blanket they'll grow up with" (11 d) | **Testimonial house** (UGC parents), with a mission story as its oldest runner |
| STONE AND STRAND | 22 · 7 | 3 D: "Why our tennis necklace never flips" neck close-up; "Set by hand, one stone at a time" hand-held pavé; "Quality isn't reserved for gold" silver wrist stack (all 2–3 d, a fresh launch) | **Demo house** |
| THATCH | 17 · 4 (2nd call) | 3 D/editorial: model in sun wearing the shell pendant (18 d); "FALL '26" earring close-up (18 d); "The earrings that keep selling out" ear close-up (10 d) | **Demo (editorial wear) house** |
| Alexis Bittar | 30 · 10 | 3 founder to camera: "I AM ALEXIS BITTAR" origin story with workshop and street B-roll (**69 d**); "THE TINY" studs explained by Alexis (24 d); "The Molten Bezel Front Back" explained by Alexis (6 d) | **Founder house** (the founder's own voice is the format) |
| KREWE · Vosges | 0 · 0 (2 calls each) | not read | unknown: read before their DMs go |
| KREWE (read 2026-10-21) | 30 · 9 | 4 silent product loops, all ≤4.2 s: aviator folding on sand ("For Those Who Travel Light"), St. Louis colour cycle ("Our signature frame … New Colors"), a "SALE · up to 70 % off" frame flipbook (6 of 11 video cards started 10/19–20: "Black Friday is coming early") | **Demo house** (≤4 s product loops; a sale starts Sun 25 Oct) |
| Vosges (read 2026-10-21) | 30 · 11 | 15 s illustrated "Grand Cacao Lodge" (snow on glass, a lodge at night, a bison in a sweater sipping cocoa, the Advent Calendar opening); two 11 s silent cinemagraphs of the 2026 Advent Calendar (one with a customer-review super) | **World house** (an illustrated season world; Q-18's snowed-in cabin sits next to it) |

**What it says.**
- [m] Wave B splits differently from wave A: of 11 videos, **6 pure or editorial demos, 1 premise demo, 3 founder pieces, 2 UGC testimonials, 1 cause story, and 0 scripted fiction**. No wave-B brand is a story house.
- [m] Two new houses: a **stills house** (Equator: no video in its top 30) and a **founder house** (Alexis Bittar: all 3 videos are him to camera, including a 69-day long-runner).
- [m] Two DMs already end on the brand's own demo, almost word for word: Q-16's "diamonds face out after every cut" is STONE AND STRAND's own "Why our tennis necklace never flips", and Q-13's "turns the box to the label. Silence." lands on Legendary's own end supers (20 g protein, <1 g sugar).

**Rule additions** (`vxo-leads` §3 step 3, `vxo-film` Step 1, LESSONS [self]):
- **Founder house** = a testimonial house whose proof slot is the founder. Never script or imitate the founder. Our film is a ≤6 s cold open that hands over to his own to-camera piece. Offer the stills as B-roll for his videos.
- **Stills house** (≤2 video cards in the top 30): the 5 free stills are the pitch, and the film comes second. Every still ships 1:1 + 4:5 + 9:16 for their catalogue ads.

**Check of the 8 wave-B DMs** (no text changed today):

| DM | House | Verdict |
|---|---|---|
| Q-13 Legendary | demo | fits; ends on their label demo |
| Q-14 Equator | stills | fits; the 5 stills are the offer |
| Q-15 Saranoni | testimonial | fits; a scripted gag, no fake testimonial. In the frames, keep a slot for their UGC parent clip |
| Q-16 STONE AND STRAND | demo | best fit in the queue |
| Q-17 THATCH | editorial demo | fits, but the film must **end on the charm worn in close-up**, their own shot, not on the plane seat |
| Q-19 Alexis Bittar | founder | fits as a product gag. Pitch the film as a 2–4 s insert (plus an optional ≤2 s open) for his own videos (§7.6c, 2026-10-21), never as a replacement for his voice |
| Q-11 KREWE · Q-18 Vosges | unread → read 2026-10-21 | KREWE: demo house, fits (the gag ends on the frames worn; their own loops can close the film); a sale starts Sun 25, so re-check MUSE if the DM slips past it. Vosges: world house, fits (a snowed-in cabin next to their snowed-in lodge) |

### 7.6c Founder and to-camera openers (measured 2026-10-21) [m, frame-read at 2 fps over 0–6 s, not model-read]
Question (backlog, "founder-house cold opens"): how long is the open before a founder speaks, and does any founder ad open on a staged scene? Method: one Ad Library Page per call (logged-out top cards, video filter), every read video downloaded to the scratchpad (never committed), a 0–6 s strip at 2 fps plus a 12-frame overview. 11 videos from 4 Pages: Alexis Bittar (3), Jones Road Beauty (3), Mid-Day Squares (3), Bobbie (2). Tower 28 served only creator UGC; SPANX served 0 cards on 2 calls (rate limit, not worked around).

| Ad (age) | Who talks | First 0–6 s | Product on screen |
|---|---|---|---|
| Alexis Bittar "I AM ALEXIS BITTAR" (**70 d**, 30 s) | founder | face at 0.0 s, already speaking; red super builds by 0.5 s; archive photos as picture-in-picture from ~4 s | bangle cutaway mid-film |
| Alexis Bittar "THE TINY" (25 d, 36 s) | founder | face at 0.0 s, hands miming the size | studs cutaway at ~4.5 s with a yellow title |
| Alexis Bittar "Molten Bezel Front Back" (7 d, 42 s) | founder | face at 0.0 s holding the stud | macro of the stud in his fingers at ~1 s |
| Jones Road "My Skin, But Glowier" (**92 d**, 82 s) | creator | face + Miracle Balm tin in hand at 0.0 s, lid off by 1 s | at 0 s |
| Jones Road "Coverage That Doesn't Cake" (**84 d**, 56 s) | creator | product pot + brush filling the frame at 0.0 s, super "Your skin doesn't suck, you just need to change your makeup", face at ~2.5 s | at 0 s |
| Jones Road "Meet The Bobbi Kit 6.0" (14 d, 50 s) | **founder** (Bobbi Brown) | **~5 s cold open**: swatches "Decades in the making" (0–1.5 s) → 3 model faces → embossed kit "The Bobbi Kit 6.0" → Bobbi on her sofa at ~5 s | in the open |
| Mid-Day Squares "Crunchy Peanut" (**316 d**, 61 s) | founders' family as a cast | a **staged retro-TV skit** ("We just launched", a presenter in a white suit inside a 1970s TV), product held up at ~1.5 s | at ~1.5 s |
| Mid-Day Squares PB&J (**239 d**, 94 s) | presenter in a store | **~1.5 s shelf B-roll** (the PB&J boxes), then face "It is selling like hotcakes" | at 0 s (shelf) |
| Mid-Day Squares "Hunger Crusher" (**316 d**, 43 s) | presenter on a sofa | face + square in hand at 0.0 s, two display boxes in the foreground | at 0 s |
| Bobbie (49 d, 124 s) | a pediatrician (expert) | face at 0.0 s, super "What's the safest infant formula?", a stethoscope twirl as the motion | ~later |
| Bobbie (48 d, 31 s) | creator | face at 0.0 s, super "Hot take: feeding your baby should not be this stressful"; the tin enters at ~4 s | ~4 s |

**What it says.**
- [m] **Face first is the norm for long-runners.** Of the 6 to-camera videos running 60+ days, 4 open on the speaker's face at frame 0 (2 with the product already in hand), 1 opens on the product filling the frame with the face at ~2.5 s, and 1 opens on 1.5 s of shelf B-roll. **None opens on a staged cold open longer than 2 s.**
- [m] **The only ~5 s cold open was a 14-day launch ad** (Jones Road's Bobbi Kit), and its open is product and models, not a scene.
- [m] **Founders do appear in staged comedy.** Mid-Day Squares' 316-day long-runner is a scripted retro-TV skit cast with the founders' family. So a founder house can take a story, as long as the people are the brand's own real people on real footage.
- [m] In the founder pieces, the product cutaway lands at **1–4.5 s** (Bittar), often with a big title super. That cutaway is the slot an AI insert fits without touching the founder's voice.
- [inf] Our old rule ("≤6 s cold open before the founder") put our film where these brands put the face. The better default is a **2–4 s product insert** at the moment the founder names the product, plus an optional **≤2 s wordless open** (one product action). A 5 s open is pitched only around a launch.

**Rule changes** (`vxo-film` Step 1, `vxo-leads` §3 step 3, LESSONS [self]): founder house = insert first, ≤2 s open optional, never script, voice or imitate the founder; world house (Vosges) = a story next to their world, never their characters or art.
**DMs:** no text changed. Q-19's DM never says "cold open"; on a reply, offer the stills and a 2–4 s insert for Alexis's own videos (the email's "film idea" stands).

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
- Foggy in-house content (§4.1): [Finn & Gray case study, The Foggy Dog](https://finnandgray.com/?p=1561) (photos, social and monthly stop-motion until a full-time in-house hire; undated). CTA stock re-checked 2026-10-09 via `products.json`, `/products/<handle>.js`, `/collections/holiday-shop/products.json` (Foggy) and the homepage and collection JSON (Moment) [m].
- Lead facts checked this run [m]: `drinkmoment.com` homepage ("all of the ritual / none of the regret"), `products.json` and `/products/<handle>.js` for Moment, The Foggy Dog, AUrate and Fishwife (tags, availability, creation dates); DNS for `vxo.studio` via dns.google (NXDOMAIN); `site/src` text. Fishwife at Aldi: [IntraFish](https://www.intrafish.com/markets/fishwife-continues-retail-growth-with-discounted-offerings-at-aldi/2-1-2032646).
