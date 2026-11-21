# 65 · Offer, proof, pricing and the site: what stops a founder from buying, and the exact fixes

Written 2026-10-09. Zero spend. Nothing was sent, posted or deployed, and the site was not edited: this is a change list for the owner to approve, ending in §7. It builds on `29` (site strategy), `32` (positioning and offer), `40` (growth levers) and `63` (outreach; its §1 items 2 and 5 and its §8 already flag that the sender can't be checked and the "one take" problem; this doc adds the measurements and the exact copy).

Evidence tags: **[m]** I measured it today (local build of `site/`, headless Chromium screenshots at 390 px and 1440 px, `ffmpeg ebur128` on the films in `site/public/media/films/`, frame sheets of the first 2 s). **[r]** read in this repo. **[w]** a web source. Vendor pages are **self-reported marketing**; the numbers in them are the claims competitors make to the same founders, not audited results.

How the audit was done: the Cloudflare preview `research-ai-video-reels.peakform-qtzvm.pages.dev` returns **401, a password page for the PeakForm app** [m], so it isn't the VXO site and a founder can't open it. No login was attempted. `vxo.studio` doesn't resolve (also `63` §1). So I built `site/` locally (`astro build`, 18 pages), served it, and read it the way a skeptical founder would: home, /pricing, /work, /frames, /about, /ai and /for/example-halden-fig.

---

## 0. The verdict, bluntly

**No, this isn't the best we can reach.** The site is well built (fast, accessible, honest about AI, prices on the page, a strong personalised `/for/<brand>` page). But as a sales tool it argues against us in four ways:

1. **The work on the site fails our own bar.** The owner rejected the mood films ("pretty but no punchline", "there are no hooks"). They make up 7 of the 7 films on the site. The one film the owner loved, **Red Light**, isn't there.
2. **Our measurable promise is false on our own reel.** We pitch mastered sound (−14 LUFS, ≤ −1 dBTP). 6 of the 7 site films miss −14 LUFS by more than 1 LU, 3 peak above −1 dBTP, and VESPER "Keep the Light" peaks at **+1.6 dBFS, which is clipping** [m].
3. **We sell a camera trick, not an outcome.** "One unbroken take, no cuts" appears about 45 times in 21 source files [m]. It contradicts LESSONS (6–10 hard cuts for action), the Red Light film and every concept in today's drafts (`63` §1.5). A DTC founder buys "a new ad that stops the scroll and sells", not "no cuts".
4. **A founder can't check who we are, and a lead can vanish.** No face, no email, no city, no live domain. With the R2 and Resend bindings unset (`site/wrangler.toml`), the form tells the visitor "done" and stores nothing (`stored:false`, `alerted:false`) [r].

None of this needs generation spend to fix. Items 1–3 are copy and remastering work (ffmpeg, free). Item 4 is owner setup.

---

## 1. What the market shows founders (2025–2026)

| Who | Price | Free or pilot offer | Turnaround | Guarantee | Proof shown |
|---|---|---|---|---|---|
| **Pinprick** (AI ad production for DTC) [w] | "$0 per ad" + % of agreed ad spend (media and growth fees on top) | **"Two free ad storyboards" from your public product imagery, "No call, no deck, yours to keep", in 48 h**; plus a free "teardown of 3 of your current ads" | 48 h storyboards; reply in 1 business day | None | "2,000+ ads shipped", "$100M+ generated", "500+ ads in 13 weeks"; anonymised work; no logos or testimonials |
| **Creatify Studio** [w] | Not published ("Book demo") | None | "48h turnaround" | "Every asset reviewed", "unlimited revisions, same day" | G2 4.8/5, named case studies with metrics (e.g. "40%+ hook rate", "47.6% CTR increase"), investors, SOC 2 |
| **Admiral Media** (AI creative) [w] | From €200 per AI video; retainers €4,000–21,500/mo (€4,000 ≈ 20 AI videos + statics) | Says "most credible" agencies offer a 1-month pilot (doesn't offer one itself) | First batch "within two weeks", then weekly | None on results; 30 days' notice | Clutch 4.9 (48 reviews), 150+ brands, case metrics (−32% CPA, −66% cost per subscription) |
| **MAW AI Studios** [w, via search summary] | From $1,500 per commercial, $5,000 per brand film, $3,000/mo retainer | n/a | 48 h priority on the retainer | n/a | Portfolio per service page |
| **Panda Studios** (AI-native) [w] | $1,000–10,000 for a 30–60 s spot + 3–5 variants; up to $25k+ for campaigns | n/a | 5–10 business days | None | Two named clients with cost claims (Kalshi spot in 48 h for ~$2k) |
| **Genre.ai** (PJ Accetturo) [w] | Reportedly ~$100k per 30 s spot today | n/a | Kalshi spot in 2–3 days | n/a | The work itself, viral |
| AI-UGC rate cards (Wireflow 2026 guide) [w] | $75–150 per AI UGC video; $1,500–2,500/mo for ~15 videos | **Pilot: $500–750 for a batch of 5**, then a retainer "based on proven performance" | n/a | n/a | "Use pilot results as case-study material" |

What this means for VXO:
- **Our lead magnet isn't unique.** Pinprick's hero offer is almost word for word ours ("free storyboards… no call… yours to keep… 48 hours"). A founder who has seen both will compare the proof next to it, and that's where we're empty. We need a free offer they can't get elsewhere (see §4.1).
- **Prices: we sit in the right band for directed films** (an AI-native studio spot runs $1k–10k), **but we invite the wrong comparison.** The site's context line compares us to "a single UGC video at $150–200" [r]. Next to the AI-UGC rate cards ($75–150 a video, ~15 a month for $1.5–2.5k), Season ("1 new concept a month" for $3,500) reads as expensive. Compare against a spot from a studio, and count the finished assets.
- **Everyone shows numbers. Nobody we found offers a money-back guarantee**, and a guaranteed ROAS is widely read as a red flag [w: attnagency]. Our honest "we guarantee the work, not ROAS" is right. What's missing is a measurable promise we control (§4.3).

## 2. How studios like this won their first clients (patterns, with the evidence quality)

1. **A public spec piece with a joke, not a mood.** Genre.ai's founder had "thousands of views" and no money, then made "Puppramin", a parody pharma ad, overnight. Kalshi saw it and commissioned the NBA Finals spot (confirmed by Kalshi to Business Insider) [w]. The spec that converts is **a funny, product-caused punchline**, which is our Red Light rule, not our current reel.
2. **Free work on the buyer's own product before any call.** Pinprick (storyboards in 48 h) [w]; our own `/for/<brand>` page already does this better (one frame made unasked, plus a 60 s walkthrough). That page is our strongest asset.
3. **A small paid pilot, then a retainer "based on proven performance"** (Wireflow's rate card; Admiral's "1-month pilot") [w]. Our Short at $1,200, credited toward Premiere/Season within 30 days, is this pilot. It's right. Keep it.
4. **First clients pay (or get a discount) in exchange for proof and referrals**: "worked for free in exchange for a testimonial… and two referrals" (an anecdote) [w]. Our founding-five line asks only for "permission to show the work… and a 15-minute debrief" [r]. **It doesn't ask for the numbers**, so even our first five clients won't give us a case study with a result in it.
5. **A personalised video audit** beats generic outreach (vendor claims; a ~3.4% cold-email reply baseline) [w]. That's our 60 s frame walkthrough, already in `40` §3.1 and `63`.

Evidence quality: 1 is confirmed by the brand. 2–5 are vendor pages or anecdotes. I found no audited study of what made AI studios' first sales.

## 3. The site audit: ranked weaknesses, with the evidence

| # | Weakness | Evidence | Severity |
|---|---|---|---|
| W1 | **The reel breaks LESSONS.** Mood films with no punchline caused by the product; slow openings | Frame sheets at 0, 1 and 2 s: SOL, VESPER "After dusk", Otto "The Director" and VESPER-23 are near-static in second 1 [m]. 5 of 7 are golden hour over a city skyline [m]: one look, repeated. LESSONS 2026-10-08/09: "pretty but no punchline", "no hooks", "no slow aerial reveal". Red Light (the owner: "wow, I loved the ad") isn't on the site [r]. | Critical |
| W2 | **Our own sound fails our own spec** | Integrated loudness / true peak of the files the site serves [m]: AURUM noon −15.0/−2.0 · Top Shelf −16.6/**−0.6** · Otto −20.4/−3.3 · SOL −22.8/−4.8 · Tabletop −13.6/**−0.5** · VESPER "After dusk" −17.1/−1.0 · VESPER-23 −16.3/**+1.6 (clipping)**. Spec: −14 LUFS, ≤ −1.0 dBTP. Red Light final (not on the site): −14.7/−1.5, the only one that passes. | Critical (we use sound as a DM opener: `63`, LESSONS 55–61) |
| W3 | **Positioning is a technique, and it contradicts our films** | "Your product, filmed in one unbroken take." (H1); "Every film is one continuous take." (Work H2); "We film one 30 s take." (step 3); the tile label "· one take" (`lib/media.ts:82`); "One take. No cuts." (`site.json` signature). About 45 mentions in 21 files [m]. LESSONS requires 6–10 hard cuts for action; Red Light has 9 shots. | Critical (`63` §8.3: "before any link goes out") |
| W4 | **The sender can't be checked; leads can vanish** | Domain NXDOMAIN; the preview is a PeakForm 401 [m]. `site.json`: `email ""`, `address ""`, `founderLine ""`, `bookingUrl ""` [r]. About = "I'm Itamar. I direct every film myself." No photo. "Book a call" falls back to `/frames?next=call` [r]. With no `UPLOADS`/`NOTIFY_TO`, `/api/lead/*` returns `ok:true` with `stored:false`: **the visitor sees success and nobody gets the lead** [r]. | Critical (blocking) |
| W5 | **No niche match for today's HOT leads** | Today's leads: pet accessories (Foggy Dog), NA functional drinks (Moment), fine jewellery (AUrate) [r]. The site has drinks (AURUM) and fragrance/candle. Nothing a dog-collar or jewellery founder can picture their product in. | High |
| W6 | **No measurable proof anywhere** | Every competitor shows a number (ads shipped, hook rate, CPA). We show none, though we have real ones: QC measurements, shot counts, the 480p test → final process and the faults we caught. Every film page carries `TODO(founder): add the real breakdown` [r] and a generic "keyframes fix the light…" text. | High |
| W7 | **The founding offer doesn't create proof, and it's hidden** | `pricing.json` founding: "one extra variant, in exchange for permission to show the work… and a 15-minute debrief". It shows only on /pricing under the add-ons (`Pricing compact` hides it on home) [r]. No ask for numbers, so no future case study. | High |
| W8 | **The lead magnet reads like a competitor's** | Pinprick: "two free ad storyboards… No call, no deck, yours to keep… 48 hours" [w] vs ours: "5 free frames… No call, no card… yours to keep… 48 h" [r]. | Medium |
| W9 | **The price framing invites the losing comparison** | The context line compares us to "a single UGC video… $150–200" [r]. Season lists "1 new concept a month" first, and "8–12 variants" only on line 4. | Medium |
| W10 | **The hero sells the mascot before the product** | Desktop and mobile folds: a large moustached Otto in the centre; 4 of the 6 ring cards show Otto or Vee's faces; product cards are smaller [m]. The orbit hero is the owner's fixed concept (`29` S0). Keep it, but change what it features. | Medium |
| W11 | **"Do you have clients?" is answered only deep in the FAQ** | The FAQ id `clients` ("Not yet…") isn't in the home FAQ list [r]. A founder will ask anyway. Answering it first, with what being one of the first five gets them, turns a weakness into the founding offer. | Low |
| W12 | **Never show the Heist film** | `VXO_aurum_heist_14s` lands a person in a moving car (frame sheet [m]), which LESSONS bans. Keep it off the site. | Guardrail |

What works and must stay: prices on the page, 50/50 with "approve before the balance", the honest AI and copyright notes, the free frames with "No call", the `/for/<brand>` page, the BFCM dated offer (real dates; capacity hidden until confirmed), the AI labels on every tile, and the honest About ("No client logos yet… we won't invent any").

## 4. The honest proof we can show with zero clients (ranked by value ÷ cost)

1. **Lead with Red Light, plus its making-of.** Nine storyboard frames → the 480p test → what our QC caught (Vee had two stopwatches; the cruiser stopped beside, not behind) → the final. Showing the faults we caught is the proof that we catch them. That's exactly what LESSONS 53–54 says to sell against the brand's "$400 in-house AI team". Cost: $0 (the media exists; the ledger is `lab/experiments/W01_site_films/ledger.md`).
2. **A QC sheet per film, as published numbers.** Shots and cuts · loudness and true peak, measured on the delivered file · the hits placed on measured frames · lip-sync offset or "voice-over, no lips" · the claims check. After remastering (§6 P0-2), every film can carry a line like "−14.0 LUFS · −1.5 dBTP · 9 shots · 0 frozen frames". Cost: $0 (`skills/ad-director/scripts/qc/`).
3. **Frames in the lead niches.** Five frames each for an invented pet-accessory, NA-drink and jewellery brand, labelled "AI concept · invented brand". Cost: storyboard stills only (~$0.05 a frame at our rates). **Generation spend: owner approval needed.** Later, with written permission only, a "Frames we made for real brands" gallery.
4. **A real performance number from our own ad.** Run "Tabletop City" (VXO's own ad, not an invented brand, so it isn't a fake product ad), or a better studio ad, on VXO's own Meta page, aimed at founders. Then publish the 3-second view rate and hold rate whatever they are, next to the date and spend. It's the only honest performance number available before clients. **Ad spend (not generation): owner decision, and it means posting, which the owner does.**
5. **The founding five, re-written to produce case studies** (§4.2).
6. **A real person.** Photo, full name, one true line of background, a reply email, city or state. Practitioner guides agree a founder checks the About page and the work in one session [w]. This is also `63`'s blocking item 1.

### 4.1 Make the free offer ours, not Pinprick's
Keep "5 free frames, 48 h, no call, no card". Add what only we give, all of it zero-spend at frame stage:
- **One hook line on frame 1** (written, not rendered): what the first second says or shows.
- **The punchline in one sentence**, caused by their product (LESSONS).
- **A 60-second walkthrough** of the frames by the owner (already `40` §3.1 and `63`). Name it on the site.

New copy (home offer block and /frames ticks):
> 5 frames of your product, free, in 48 hours. Plus the hook for second one and the punchline in a sentence, and a 60-second walkthrough from the director. No call, no card. Yours to keep.

### 4.2 The founding five: trade a discount for numbers
Current: "First five brands: one extra variant, in exchange for permission to show the work once it's live and a 15-minute debrief."
Proposed (**owner decision: it changes what we give away, not the list prices**):
> **First five brands.** One extra hook variant and a QC sheet. In return: permission to show the film once it's live, and a screenshot of 30 days of Ads Manager results for the film and your current best ad. We publish numbers only with your written OK, good or bad. **[N] of 5 places left.**

Show it on the home page, directly under the three price cards (the `Pricing compact` view hides it today). Keep `left` true.

### 4.3 A promise we control (no ROAS guarantee)
Today: "On-time promise: if the first take is late through our fault, the balance drops 10 %." That's good; it should be visible on the home page, not only /pricing. Two additions for the **owner to decide** (both cost us only edit time, no generation):
- **"The test take matches the frames, or we redo it."** You approve the 480p test against the frames you approved. If it doesn't match them, we redo it before round 1, and it doesn't count as a revision. (A redo is a paid render: worst case ~$6 at our 480p test rate.)
- **The hook re-cut promise.** If after 7 days and at least $300 of spend, the film's 3-second view rate is below your current best ad's, we cut 3 new opening hooks from the same film, free. (Re-edit only, no new generation; it needs their screenshot.)

## 5. Pricing (prices stay; framing changes)

- **Replace the anchor line.** Current: "A polished product video from a production company typically runs $3–10k. A single UGC video is about $150–200, and you still direct it. Source: DesignRush." Proposed:
  > A 30-second spot from a production company typically runs $3–10k and weeks of work (DesignRush). AI-native studios quote $1k–10k for a spot with a few variants (Panda Studios, 2026). Premiere is $2,500 for the film, 6 variants, a loop and stills, with the price on the page.
  (Drop the UGC comparison: it invites a per-asset comparison with $75 AI-UGC clips, which aren't our product.)
- **Lead each card with the count of finished assets**, then the details. Premiere: "**11 finished assets**: a 30 s film, 6 variants, an 8 s loop, 3 stills" (1 + 6 + 1 + 3 per `pricing.json`). Season: "**16–20 finished assets a month**: a 30 s film, 8–12 variants, a loop, 6 stills" (1 + 8–12 + 1 + 6). Short: "**4 finished assets**: a 30 s film and 3 short versions".
- **Rename lengths to "15–30 s"** wherever it says "30-second" (LESSONS: the winners are often 8–15 s; Short already ships 6 s and 15 s versions).
- **Season** "1 new concept a month" → "A new film every month, and a fresh hook drop every week". Same scope, said as the outcome. Whether Season should add a 2nd concept is an owner decision (§7); I don't recommend changing the price.

## 6. The prioritised site change list (for the owner, then the site agent)

**P0: before any link goes to a lead.**

| # | Change | Where | Exact edit |
|---|---|---|---|
| P0-1 | **Make leads arrive** | Cloudflare Pages settings (owner) | Bind the R2 `UPLOADS` bucket, or at least set `RESEND_API_KEY`, `MAIL_FROM` and `NOTIFY_TO`. Then a test submission must show `stored:true` or `alerted:true`. Until then, put a plain `mailto:` under every form: "Or email me: [address]". |
| P0-2 | **Remaster every film on the site, then measure** | `site/public/media/films/*/full.*` (the site agent; ffmpeg only, $0) | `loudnorm=I=-14:TP=-2` two-pass, re-encode AV1 + H.264, measure the encoded files. The gate: −14 ±1 LUFS and ≤ −1.0 dBTP. Any film that fails comes off the site. |
| P0-3 | **Put Red Light on the site and make it the lead film** | `media.json`, `content/films/red-light.md`, `index.astro` `lead[]`, hero `featured` | The 30 s final (passes −14.7/−1.5 [m]). Label: "Spec film · invented brand · 100% AI · 30 s · 9 shots". Idea line: "AURUM is a sparkling yuzu drink we invented. A getaway car, a police cruiser, a red light, and one can that ends the chase." **Never add the Heist film** (W12). |
| P0-4 | **Kill "one take / no cuts" everywhere** | The ~45 mentions in 21 files (see W3; `grep -rni "one take\|unbroken\|continuous take\|no cuts" site/src`) | Signature "One take. No cuts." → "**Hook first. Punchline last.**" Tile label "· one take" → "· {shots} shots" (or the film's length only). Film pages "The take: one continuous camera move, 30 seconds. No cuts." → a true per-film line (shot count, what the hook is, what the punchline is). |
| P0-5 | **The hero copy: an outcome** | `site.json` headlines, `Hero.astro` sub-line | H1 default: "**A new product ad, with a punchline only your product can land.**" Sub: "15–30 s films made with AI and directed by a person: something moving in the first second, a twist your product causes, and sound mastered for the feed. Films from $1,200." Keep "Free. No call. 48 h." and the AI disclosure line. Variants: `fatigue` "Your best ad is tired. Here's the next one, without a shoot." · `launch` "Your launch, as an ad people watch to the end." · `bfcm` unchanged. |
| P0-6 | **A real person** | `about.astro`, `site.json`, the footer | A photo of the owner (real, not AI), full name, one true background line, a reply email, a state or city, the postal address the CAN-SPAM emails need (`63` §1). Footer: "Questions? [email], I answer myself." |

**P1: the proof sections (this week; $0 except where marked).**

| # | Change | Where | Exact edit |
|---|---|---|---|
| P1-1 | **New section after the hero: "What every film passes before you see it"** | `index.astro`, new, between Hero and Problem | Four items, each a number we measure: "**Hook:** motion or a line in the first frame." · "**Sound:** −14 LUFS, true peak ≤ −1 dBTP, measured on the file you get." · "**Sync:** every hit on the frame of its action, checked at 10 fps." · "**Claims:** only your tested numbers on screen. AI never plays the result: your real footage goes in a proof slot." Link: "See Red Light's QC sheet →". Sub-line: "Most AI ads skip these. That's the difference between an AI clip and an ad you can run." |
| P1-2 | **A making-of for Red Light** | `/work/red-light` page body (replaces the TODO) | 9 storyboard frames → the 480p test → "What we caught and fixed: Vee had two stopwatches in one shot; the cruiser stopped beside the car, not behind it; a drink that's 'drunk' must visibly drop." → the final + its QC numbers. Same for every film that stays on the site; delete the TODO comments. |
| P1-3 | **How it works = the real funnel (5 steps, not "one take")** | `index.astro` `steps[]` | 1 "Send one photo, or your product page." · 2 "5 frames in 48 h, free. Plus the hook and the punchline in a sentence." · 3 "The storyboard, then a 480p test take you approve." · 4 "The final film: 15–30 s, 9:16 + 4:5, short cuts and stills." · 5 "A QC sheet with every film, and a list of every AI element for your disclosure." |
| P1-4 | **The Work section** | `index.astro` Work head; `/work` lede | H2 "Every film is one continuous take." → "**Spec ads for brands we invented. Each one has a turn and a punchline.**" Lede: "We invented these brands so we could show the work without using anyone's product. Your film starts from your real product photo." Order: Red Light first; then the remastered films that have a turn (Top Shelf, Keep the Light, Tabletop City); then the mood films, or drop them. Filters: only niches with at least one film. |
| P1-5 | **Founding five on the home page** | `Pricing.astro` (show it in `compact` too), `pricing.json` | The §4.2 copy, with a true live count. |
| P1-6 | **The on-time promise on home** | Offer block ticks | Add a tick: "First take late through our fault? The balance drops 10 %." |
| P1-7 | **Price framing** | `pricing.json` `context`, card deliverables | The §5 anchor line; the asset count at the top of each card; "15–30 s". |
| P1-8 | **"Do you have clients?" on the home FAQ, first** | `index.astro` Faq `only[]`, `faq.json` | "Not yet, and we won't invent any. You'd be one of our first five, which gets you an extra hook variant and a QC sheet, in return for showing the film and sharing its 30-day numbers with us. Until then, judge us on frames of your own product, free." |
| P1-9 | **The free offer: ours, not a generic one** | Offer block, `/frames` ticks, MiniForm note | The §4.1 copy. |

**P2: within two weeks.**

| # | Change | Notes |
|---|---|---|
| P2-1 | **Frames for the lead niches** (pet accessories, NA drinks, jewellery), invented brands, labelled | Stills only (~$0.05 a frame). **Owner approval (generation spend).** Show them on `/work` under "Frames". |
| P2-2 | **The hero ring features products** | Keep the orbit and Otto (fixed concept); make Red Light the `featured` card, and give the ring at least 4 product-first posters (can, bottle, candle) against at most 2 character-face posters. |
| P2-3 | **One honest performance number** | §4 item 4. Publish only after a real run, with the date, spend and metric definition (3-second views ÷ impressions). **Owner: ad spend, and the owner posts.** |
| P2-4 | **The `/for/<brand>` page shows the hook line and the QC promise** | It's the page the walkthrough links to; it should repeat the P1-1 four checks in one line. |
| P2-5 | **Per-niche pages** `/for/pets`, `/for/drinks`, `/for/jewellery` | Only once P2-1 frames exist. Each one carries its niche's guardrails from docs 48, 52 and 57 (e.g. "AI never plays your dog loving the food; your real clip goes in the proof slot"). |

The new home order (P0 + P1): **Hero (outcome H1, Red Light featured) → What every film passes (QC proof) → The problem → How it works (5 real steps) → Work (Red Light first, with making-of links) → Pricing (asset counts, honest anchor) + founding five → The offer (frames + hook + walkthrough, on-time promise) → A person (photo, name, email) → FAQ ("Do you have clients?" first).**

## 7. Decisions only the owner can take

1. **P0-1:** bind R2/Resend in Cloudflare (or accept the mailto fallback). Until then, any lead from the site can be lost silently.
2. **P0-6, `63` §8.1:** register the domain, deploy, and give a real photo, name, reply email and postal address. Nothing else on this list matters to a founder who can't find us.
3. **P0-4:** approve the new signature line ("Hook first. Punchline last.") in place of "One take. No cuts.", a brand-level change.
4. **P0-5:** approve the hero H1 and sub-line (or reword them; keep it an outcome and keep it true).
5. **§4.2:** approve the founding-five trade (an extra hook variant + a QC sheet for public use + 30-day numbers).
6. **§4.3:** approve either or both promises ("test matches the frames, or we redo it"; the hook re-cut). Each costs at most one 480p render or an edit.
7. **P2-1:** approve stills spend for three niche frame sets (≈ 15 stills).
8. **P2-3:** decide whether to run a small paid test of VXO's own studio ad to earn one honest performance number. The owner posts and pays; the agent never does.
9. **Season:** keep "1 concept a month" (my recommendation: keep the price, reword it as the outcome), or add a 2nd concept.
10. **Mood films:** remaster and keep the ones with a turn (Top Shelf, Keep the Light, Tabletop City), or remove all but Red Light until new spec films exist.

## Sources

- Pinprick: https://pinprick.io/ [w]
- Creatify Studio: https://creatify.ai/studio [w]
- Admiral Media, AI creative agency pricing: https://admiral.media/ai-creative-agency-pricing/ [w]
- Wireflow, "How much to charge clients for AI UGC ads" (2026): https://www.wireflow.ai/blog/how-much-to-charge-clients-for-ai-ugc-ads [w]
- Panda Studios, "AI commercial cost 2026": https://panda-studios.com/ai-commercial-cost-2026 [w]
- MAW AI Studios (search summary only, page not fetched): https://mawmotionstudios.com/ai-video-production/ [w]
- Business Insider on the Kalshi ad and Genre.ai's start: https://www.businessinsider.nl/the-filmmaker-behind-the-ai-generated-kalshi-ad-built-an-ai-studio-it-didnt-kick-off-until-veo-3-launched/ [w]
- CO/AI on Genre.ai pricing: https://getcoai.com/news/i-made-this-in-like-two-days-in-my-underwear-ai-studios-slash-advertising-production-costs/ [w]
- Guaranteed ROAS as a red flag: https://www.attnagency.com/blog/marketing-agency-red-flags [w]
- Segwise, AI UGC vs human UGC (2026): https://segwise.ai/blog/ai-ugc-vs-human-ugc-meta-ads-roas-2026 [w]
- B2B trust signals (practitioner guide, no study): https://www.lowcode.agency/blog/b2b-website-trust-signals [w]
- Repo: `site/src/**`, `site/wrangler.toml`, `site/functions/api/lead/*`, `research/ai-video-reels/leads/2026-10-09.md`, `lab/LESSONS.md`, `lab/experiments/W01_site_films/ledger.md`, docs `29`, `32`, `40`, `63` [r]
