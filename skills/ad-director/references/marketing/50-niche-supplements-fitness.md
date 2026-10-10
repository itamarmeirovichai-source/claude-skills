# 50 — Niche deep-dive: supplements, fitness gear and wellness devices

Research brief, 2026-10-09. No generation money was spent. Nobody was contacted.

**What this adds.** It builds on 41 (action realism), 42 (teardown method), 43 (models, prices, templates), 44 (comedy craft), 45 (what sells, general policy), 46 (sound and QC) and the sibling niche docs 47 (beauty) and 48 (fashion). It does not repeat them. It adds:
- 23 measured TikToks from seven brands that supplement and device founders benchmark against (AG1, Ritual, Oura, WHOOP, Ghost, Cymbiotika, Hyperice), plus case-study evidence for Therabody, Liquid I.V., Create, Bloom and Oura's TV work;
- conversion data for the niche;
- a realism-pitfall table for powders, gummies, shakers, wearables, gym iron and massage devices, mapped to doc 43;
- the policy and legal rules that are stricter here than anywhere else VXO sells (FTC health-claims standard, Meta 18+ targeting, TikTok weight/muscle rules, FDA wellness-device line, the New York minors law);
- the buyer: who signs, what they fear, what proof they need, 20 brand types;
- 8 ready concepts with shot lists, physics checks, audio maps and costs.

**Tags.**
- `[m]` measured by us from the downloaded file: ffmpeg scene cuts at threshold 0.30, a 0.5 s RMS envelope, the beat-regularity score from 42 (> 0.5 = steady music bed, < 0.15 = voice or ambient with no steady beat), and 2 fps frame tiles we read by eye.
- `[c]` the brand's or platform's own claim.
- `[v]` vendor or agency figure: directional only.
- `[inf]` our inference.
- `[unverified]` no primary evidence found.

**Method and limits.**
- **TikTok:** single-video downloads worked. Profile listings were rate-limited: of 23 brand handles tried repeatedly over ~60 minutes, only 8 returned their latest 120 posts (AG1, Ritual, Oura, WHOOP, Ghost, Cymbiotika, Hyperice, and LMNT, whose account has not posted since mid-2023). Bloom (`@bloom`), Liquid I.V., Create, Therabody, Eight Sleep, Seed, Olly, Arrae and Hatch returned empty responses every time. Those brands are covered from case studies and ad-library write-ups, not measured.
- **YouTube:** blocked from this server (doc 42, 47), not retried.
- **Motion MCP:** no workspace (doc 45 §0). Skipped.
- **Files:** 23 TikToks in `scratchpad/niche/supplements/vids/`, analysis in `.../an/`. Nothing is committed or republished.
- **"Paid-scaled"** = millions of views at a like-rate ≤ 0.1 %. That only happens with spend behind the post (Spark Ads). Brands keep spending only on winners, so it is our best public proxy for "sold" [inf, method from 47]. **"Organic hit"** = like-rate ≥ 2 % and a large multiple of the account median.
- **Account medians** (views, latest 120 posts) [m]: AG1 864 · Ritual 44.6K · Oura 31.5K · WHOOP 25.2K · Ghost 9.4K · Cymbiotika 4.5K · Hyperice 1.8K.

---

## 0. The ten things to know before pitching a supplement, fitness or device brand

1. **The most-scaled ad we found is 8 seconds of hands and boxes.** Cymbiotika's "ultimate duo" (18.5M views, 0.09 % likes, ≈ 4,000× the account median, so heavily paid) is three stop-motion-style shots of two product boxes and their sachets stacked outdoors, with one POV caption: "pov you found the best skin + stress support duo" [m]. No face, no claim beyond "support", no VO. The product fills the frame from 0.0 s to the end. Runner-up: Ritual's 5.4 s one-take of a hand dropping a vitamin bottle into a **toy-sized shopping cart** that tips under the weight, captioned "'Ritual is on Sale' / Me:" (1.9M, 0.10 % likes, 43× median, paid) [m]. Both are miniature-scale object gags with a one-line meme caption.
2. **Product or product name on screen at 0.0 s in 12 of the 19 ads we read frame by frame** [m]. The exceptions are story openers (Ghost aisle, Oura's coffee POV, creator talking heads, Ritual's lab, AG1's beach wide), and in the device memes the *device data* is the hook instead.
3. **Two winning grammars, and they split by product type.**
   - **Ingestibles (powders, gummies, drinks):** hands-only ritual and ASMR. Scoop, pour, shake, freezer prep, pack-the-bag. AG1's paid library is almost entirely this: 7–17 s, 1.3–1.6 s average shot length, text on frame 1 [m].
   - **Devices and wearables:** *data as the punchline*. Oura's "my Oura Ring thought I was dying and it wasn't wrong" (a dropped coffee + a 148 bpm screenshot, 6.5 s, 11× median) and "woke up and my ring was pulsing red i thought it was wraps for me" (2.8M, 89× median, 2.4 % likes) [m]. The product *reports* something funny about the owner.
4. **Scale gags work for small hardware.** Oura "Insects for scale" (13 s, 7 shots): a mantis, a monarch butterfly and a ladybird next to the ring; supers "Ultra thin · Built to blend in · Comfortable 24/7" [m]. This is studio CG/macro work that Kling i2v + Cinema Studio can reproduce today, and it proves a product truth (size) without a health claim.
5. **Ghost proves comedy + one body-CG insert sells energy drinks to men.** "The math is mathing" (14.7 s, 9.9 % likes, 28× median): a man in a store aisle bends with a bad back, the picture cuts to a glowing X-ray spine (4.5–9 s), then he straightens and grabs the can [m]. The CG insert is the joke and is AI-native.
6. **Supplements are the longest-surviving ads on Meta.** Brandsearch: supplement survivors run **52 days on average, almost double other niches**; **62 % are video, and 67 % of those are founder-led UGC**; authority hooks are 52 % of supplement hooks; question hooks are the weakest across niches (8 % of 30+ day survivors) [v]. A second vendor study (500 ads, 50 brands) found a 256-day average run and that **single images ran longest** (268 d) [v]. The two disagree on duration but agree: the long runners are *plain, specific and claim-led*, not cinematic.
7. **AI in this niche carries a scam association you must design against.** In December 2025, 35 state attorneys general asked Meta to ban AI-generated content in weight-loss drug ads, citing "fake before-and-after images and nonexistent spokespeople", including an AI model "losing 208 pounds in three weeks" ([MD AG](https://oag.maryland.gov/News/pages/Attorney-General-Brown-Pushes-Meta-to-Act-on-Misleading-AI-Weight-Loss-Ads-.aspx)). The NYT documented AI "doctor" avatars selling supplements ([summary](https://www.emarketer.com/content/ai-doctor-fakes-wellness-influencers-fuel-health-scam-ads-on-social-media)). **VXO rule: in this niche, AI never plays a person who vouches, a doctor, a lab coat, a body transformation or a result.** AI plays the product, objects, metaphors, scale and comedy.
8. **Proof is the product.** Independent tests found that many creatine gummies contained little or no creatine (NOW, March 2024: 5 of 12 failed; SuppCo 2025: 4 of 6 failed) ([NutraIngredients](https://www.nutraingredients.com/Article/2024/03/01/NOW-raises-red-flags-after-creatine-gummy-testing), [Athletech](https://athletechnews.com/creatine-gummies-amazon-suppco-report/)). Amazon now requires third-party (TIC) cGMP verification for all supplement listings, and NSF/ANSI 173 testing for sports-nutrition and weight-management SKUs ([SupplySide](https://www.supplysidesj.com/business-resources/amazon-supplement-testing-rules)). Buyers in this niche sell on *trust receipts*: COA, NSF/Informed Sport seal, grams per serving. **Every VXO film here carries one real proof slot** (§5.3).
9. **The legal bar is the highest of any VXO niche.** FTC: health claims need "competent and reliable scientific evidence", with RCTs on the finished product or equivalent the expected standard; the DSHEA asterisk "won't cure an otherwise deceptive ad"; a "results not typical" line does not fix an atypical testimonial ([FTC Health Products Compliance Guidance](https://www.ftc.gov/business-guidance/resources/health-products-compliance-guidance)). Meta: dietary, health and weight products target **18+ only** and must state "the time taken to achieve noticeable results" ([Meta Health & Wellness](https://transparency.meta.com/policies/ad-standards/restricted-goods-services/health-wellness)). TikTok: weight-loss and muscle-gain claims 18+, no "works without diet or exercise", no "ideal body" ([TikTok](https://ads.tiktok.com/help/article/tiktok-ads-policy-weight-management)). New York bans selling weight-loss and muscle-building supplements to minors (in force April 2024).
10. **Post-click is where this niche bleeds.** Health & Fitness had the highest vertical CPA in one 2025 Meta benchmark set ($52.98 vs a $23.10 average) [v, [Trendtrack](https://www.trendtrack.io/blog-post/meta-ad-spend-by-industry)], and Meta has restricted lower-funnel events (Purchase, Add to Cart) for many accounts it classifies as Health & Wellness since January 2025 [v, [Polar](https://www.polaranalytics.com/post/2025-metas-tracking-restrictions-for-health-wellness-are-here----heres-how-to-fix-it)]. Founders here buy creative on **CPA and subscription take-rate**, not on views. A VXO film must ship as a hook pack that feeds testing (doc 45 rule 8), not as one hero.

---

## 1. Teardowns: 14 ads (12 measured, 2 from case studies)

Selection: each measured brand's top posts by views and multiple of the account median, all inside the two-year window (one Hyperice reference from June 2023 is kept as the "athlete day + data" archetype). Full 23-file measurement list in §1.2.

| # | Ad (link) | Len / shots / ASL [m] | Second 1 (hook) | Turn / punchline | Sound [m] | Text / CTA | Why it sold [inf] | Stats [c] |
|---|---|---|---|---|---|---|---|---|
| 1 | **Cymbiotika "The ultimate duo"** [TikTok](https://www.tiktok.com/@cymbiotika/video/7551544174969982263) | 8.2 s / 3 / 2.7 s. Cuts 3.70, 5.70 | A hand drops a magnesium box onto a stone ledge in sun; a second box lands on top at 1.5 s | 3.7 s: hand fans three sachets of each; 5.7 s: final stack, boxes + sachets, hold | Quiet bed, no VO; beat 0.11 | One persistent super "pov you found the best skin + stress support duo" | **Two products, one bundle, zero claims beyond "support".** Lo-fi phone light reads as real. Product 100 % of frames | **18.5M** views, 0.09 % likes: heavily paid |
| 1b | **Ritual "Adds to Cart"** [TikTok](https://www.tiktok.com/@ritual/video/7633892153931877645) | 5.4 s / 1 (one take) | A clear bottle of yellow softgels swings into frame in a hand over a toy shopping cart on marble, hedge behind | 1 s: the bottle drops into the cart; the cart tips back onto its rear wheels and settles, too small for it | Ambient, no VO; beat 0.15 | "'Ritual is on Sale' / Me:"; caption carries "up to 35% off" and Mother's Day | **Offer hook (doc 45 D5: sale 11.35 %) told as a scale gag.** The product's softgels are visible through the bottle the whole time | **1.9M**, 0.10 %, 43× median: paid |
| 1c | **Ritual "Netflix documentary"** [TikTok](https://www.tiktok.com/@ritual/video/7665086354652433678) | 5.9 s / 3 / 2.0 s | Real lab; a staffer clips a lav mic on a scientist | She sits, settles, looks to camera like a doc interview; no line is spoken | Room tone; beat 0.15 | "Our science team preparing for our Netflix documentary on how Essential Prenatal is the only leading prenatal backed by its own human clinical trial…" | **Proof as a joke.** Real scientists + a real trial (published, cited in the caption) + a self-aware caption. This is the real-proof slot in its native form | 224K, 0.23 %: paid |
| 2 | **AG1 celebrity "Wakey, wakey, shakey, shakey"** [TikTok](https://www.tiktok.com/@drinkag1/video/7620079537321200909) | 50.2 s / 20 / 2.5 s | Ambassador in a sunlit kitchen, AG1 pouches lined up on the counter, already shaking the shaker | 8 s and 19 s: wardrobe-change jump cuts; 24.5–31 s: seated BTS interview; 40–44 s: shaker dance across the room | Speech and laughter, no steady bed; beat 0.05 | Caption is the line; no on-screen CTA | **Celebrity + a repeated physical ritual (the shake).** The shake is the brand gesture. The ambassador appears to be Hugh Jackman [unverified] | **28.6M**, 0.02 % likes: heavily paid |
| 3 | **AG1 Pro launch** [TikTok](https://www.tiktok.com/@drinkag1/video/7652719490727202061) | 15.9 s / 10 / 1.6 s | Gym floor, dumbbells; "INTRODUCING / AG1 / PRO" in acid green fills the frame at 0.5 s | 3 s: gym-bag zip macro, flash-frame; hands pack box, shaker, stick packs; 12.8 s: end card "MAKE A PRO MOVE" over flat-lay | Steady music bed, flat −16 dB; **beat 0.61** | Newness hook, CTA as brand line | **Newness hook (Motion's #1 hook type, doc 45 D5) + hands-only pack-the-bag.** Every shot shows the pack | 193K, 0.02 %: paid |
| 4 | **AG1 "Freezer prep"** [TikTok](https://www.tiktok.com/@drinkag1/video/7678324792348478734) | 17.1 s / 13 / 1.3 s | Top-down: two glasses of green AG1 with berry ice cubes, stick pack beside | Ice-tray recipe: berries in, coconut water poured, mint on; powder pours into bottle; frother; tongs drop cubes; pour | Ambient + soft bed; beat 0.18 | "Kinda chic to start your mornings like this" | **Recipe = reason to buy again.** The pour of green over a berry cube is the money shot. No claim at all | 304K, 0.02 %: paid |
| 5 | **AG1 × Harmless Harvest** [TikTok](https://www.tiktok.com/@drinkag1/video/7660883406674300173) | 7.9 s / 5 / 1.6 s | Beach wide, two women under a green umbrella raise cups | Pour coconut water, pour AG1 bottle, cheers | Beach ambience; beat 0.30 | None | **Co-brand pairing, 8 s, loopable** | 271K, 0.03 %: paid |
| 6 | **Oura "pulsing red"** [TikTok](https://www.tiktok.com/@ouraring/video/7629824861325610270) | 6.5 s / 1 (one take) | Dark bedroom, phone camera; the ring's red sensor glow pulsing on a sleeping hand | None: the joke is the caption | Room tone; beat 0.12 | "woke up and my oura ring was pulsing red i thought it was wraps for me" | **Fear → relief, in a caption.** Answers a real customer question (why does it flash red?) as a meme | **2.8M**, 2.4 % likes, 89× median: organic hit |
| 7 | **Oura "exposed me"** [TikTok](https://www.tiktok.com/@ouraring/video/7635024132668804383) | 6.5 s / 1 | POV: hand holds a coffee cup at a front door, the other unlocks it | 2.5 s: the cup falls and splashes on stone; 3 s: an app card "148 bpm" pops on screen | Real sound: keys, splat | "my Oura Ring thought I was dying and it wasn't wrong." | **The product reports the owner's panic: data as punchline.** VXO-ready structure | 348K, 1.9 %, 11× median |
| 8 | **Oura "Insects for scale"** [TikTok](https://www.tiktok.com/@ouraring/video/7645344193845546254) | 13.0 s / 7 / 1.9 s | Silver ring floating on grey; gold and rose rings pass through frame | 3 s: praying mantis close-up; 4.5 s mantis on a leaf beside the ring; 6–7 s monarch lands *on* the ring; 9.6 s: ladybird beside the ring = end card | Soft bed, no VO; beat 0.10 | "Ultra thin · Built to blend in · Comfortable 24/7 · The world's smallest smart ring" | **Scale proof without a claim fight.** Pure macro/CG; reproducible with Kling i2v | 223K, 1.6 %, 7× median |
| 9 | **Oura Ring 5 launch** [TikTok](https://www.tiktok.com/@ouraring/video/7644911410387979533) | 30.0 s / 19 / 1.6 s | Ring rotating on grey, logo engraved inside | One spec per shot: "40 % smaller" (hand), "Research-grade accuracy" (sensors), "Tougher to scratch" (cracked ice), exploded view, "Fully waterproof" (water crown), "1 charge lasts a week" (desert night), "No alerts / No distractions" (forest), butterfly "Barely there" | Bed + whooshes; beat 0.07 | Spec supers; "Oura Ring 5" end card | **One claim per shot, each with a visual metaphor.** The spec ladder format | 1.3M, 2.9 %, 5,683 comments |
| 10 | **Oura creator explainer (paid)** [TikTok](https://www.tiktok.com/@ouraring/video/7675809956490185997) | 46.7 s / 20 / 2.2 s | Creator to camera on a city street, "Let's be real…" | B-roll walks, night bed, then app screens (readiness 75, sleep, cycle day) at 29–32 s | Speech, no bed; beat 0.03 | Spoken CTA | **The paid workhorse is UGC + app UI.** It is the format VXO cannot replace, only feed (§5.3) | 254K, 0.11 %: paid |
| 11 | **WHOOP "Meridian" band** [TikTok](https://www.tiktok.com/@whoop/video/7678699335680429326) | 33.4 s / 8 / 4.2 s | Grey table, a fan of white boxes; red-nailed hands pick one | Hands unbox mesh bands, clip them on, wrist try-ons in four colours; end card "MERIDIAN" | ASMR handling, light bed; beat 0.19 | Product name only | **Hands-only unboxing (Motion's top format, 9.83 %, doc 45 D3).** Accessories sell as jewellery | 509K, 1.8 %, 20× median |
| 12 | **Ghost "The math is mathing"** [TikTok](https://www.tiktok.com/@ghostlifestyle/video/7568560415425285431) | 14.7 s / 1 take + CG insert (scene detector reads 0 cuts through dissolves) | Supermarket aisle, man in a cap bending to the bottom shelf | 4.5–9 s: dissolve to a blue X-ray body; the spine glows red, then a gnarly CG vertebra close-up; back to the aisle; he straightens, picks the can, walks off | Voice/ambient; beat 0.10 | Caption only | **A body-CG gag as the turn.** The product is the fix to a comic, non-medical "pain" (bending to the bottom shelf) | 266K, **9.9 % likes**, 28× median |
| 13 | **Therabody "The Workout Called Life"** (TV/CTV/social, 2023–2025) [WARC](https://www.warc.com/content/article/warc-awards-effectiveness/therabody-for-the-workout-called-life/en-gb/158915), [Forsman](https://www.forsman.com/news/new-work-therabody/) | :30 spots (not measured) | Everyday strain as a workout: a mom's chores, a professional's day | Characters lift into the air in a "surreal, dreamlike" release as the device hits | — | — | **Broadened the buyer beyond athletes.** Surreal visuals = AI-native | [c] 2023 **ROAS 11.34**, sales decline reversed, #1 massage gun; budget > $20M |
| 14 | **Oura × *Mission: Impossible* tie-in** (2025, TV) [iSpot](https://www.ispot.tv/hub/from-action-packed-stunts-to-everyday-calm-lessons-from-ouras-mission-impossible-tie-in-campaign/) | :15 (not measured) | Stunt footage | Ring as the calm in the chaos | — | — | **Cautionary:** "highest level of Curiosity", but viewers "missed the visuals of the Oura ring" and some thought it was a movie ad; Attention Index 92 | iSpot test data |

### 1.1 Cross-ad patterns (what to copy)

1. **Hands are the cast.** 8 of the 19 ads read frame by frame are hands-only or hands-dominant, including the two most-scaled supplement ads [m]. **Miniature props make them funny** (Ritual's toy cart, Oura's insects). Hands carry the ritual (scoop, shake, clip, stack) and dodge every AI-face, testimonial and body-image problem at once.
2. **ASL 1.3–2.7 s for ingestibles; one take for memes.** The paid AG1 cuts sit at 1.3–1.6 s ASL. The device memes are single takes under 7 s [m].
3. **The text line is the hook, and it is specific.** "pov you found the best skin + stress support duo"; "INTRODUCING AG1 PRO"; "my Oura Ring thought I was dying". None is a question [m]. Matches Brandsearch's finding that question hooks survive least [v].
4. **No music needed.** Only 2 of 23 have a steady beat (AG1 Pro 0.61, Ghost "Locked in" 0.54) [m]. Ambient, ASMR handling and voice dominate.
5. **Spec ladders for launches.** Oura Ring 5: one claim per shot, each with a physical metaphor (cracked ice = scratch, water crown = waterproof) [m]. VXO's "impossible shot that proves a truth" (45 Q2) in its purest form.
6. **Data overlay = device comedy.** Oura 148 bpm, WHOOP 177 bpm (Ronaldo), Hyperice's WHOOP recovery 73 % screenshots [m]. The device's number is the punchline. **Always a real app screenshot comped in post**, never generated (§3).
7. **Celebrity and athlete belong to the brand, not to VXO.** AG1's 28.6M hero and WHOOP's athlete posts depend on licensed people. VXO's equivalent is the client's *real* founder or athlete as a 2–5 s insert (doc 45 F5).

### 1.2 Full measured set [m]

| File | Brand | Dur | Shots | Views | Like % | Read |
|---|---|---|---|---|---|---|
| 7551544174969982263 | Cymbiotika | 8.2 | 3 | 18.5M | 0.09 | paid |
| 7672356278273854733 | Cymbiotika | 11.2 | 1 | 394K | 0.77 | — |
| 7633892153931877645 | Ritual (toy cart) | 5.4 | 1 | 1.9M | 0.10 | paid |
| 7665086354652433678 | Ritual (lab mic-up) | 5.9 | 3 | 224K | 0.23 | paid |
| 7620079537321200909 | AG1 | 50.2 | 20 | 28.6M | 0.02 | paid |
| 7683519695697333517 | AG1 (street quiz, gummies) | 55.8 | 18 | 1.0M | 0.06 | paid |
| 7678324792348478734 | AG1 | 17.1 | 13 | 304K | 0.02 | paid |
| 7660883406674300173 | AG1 | 7.9 | 5 | 271K | 0.03 | paid |
| 7652719490727202061 | AG1 | 15.9 | 10 | 193K | 0.02 | paid |
| 7629824861325610270 | Oura | 6.5 | 1 | 2.8M | 2.39 | organic |
| 7644911410387979533 | Oura | 30.0 | 19 | 1.3M | 2.88 | organic + boost |
| 7556237269913423135 | Oura (Ceramic CG) | 16.0 | 3 | 750K | 1.47 | — |
| 7635024132668804383 | Oura | 6.5 | 1 | 348K | 1.88 | organic |
| 7675809956490185997 | Oura (creator) | 46.7 | 20 | 254K | 0.11 | paid |
| 7645344193845546254 | Oura (insects) | 13.0 | 7 | 223K | 1.59 | — |
| 7678699335680429326 | WHOOP | 33.4 | 8 | 509K | 1.77 | — |
| 7679074032418966798 | WHOOP | 9.2 | 2 | 359K | 3.84 | organic |
| 7642765461851049230 | WHOOP (green-screen + data) | 56.1 | 1 | 224K | 3.61 | organic |
| 7636260274990746893 | WHOOP (hands ASMR) | 10.1 | 9 | 157K | 1.34 | — |
| 7594598282379136311 | Ghost "Locked in for the week" (not read by eye) | 6.6 | 1 | 154K | 9.43 | organic |
| 7618276416173493534 | Ghost × 7UP (rotating can CG, ends on Nutrition Facts) | 18.6 | 2 | 341K | 8.10 | organic |
| 7568560415425285431 | Ghost | 14.7 | 1+CG | 266K | 9.90 | organic |
| 7240210794082749742 | Hyperice (athlete day + app data, 2023) | 46.2 | 33 | 106K | 3.48 | organic |

---

## 2. What actually converts in this niche (data)

| # | Finding | Source | Status |
|---|---|---|---|
| S1 | Supplement survivors (30+ days, "Winning") average **52 days**, ~2× other niches; **62 % video**; **67 % of video survivors are founder-led UGC**; authority claims = **52 %** of hooks; video length **30–60 s**; static copy 120+ words; CTA 65 % Shop Now / 25 % Learn More, Learn More runs longer | [Brandsearch](https://brandsearch.co/blog/winning-meta-ad-patterns-2026), 523 ads across 5 niches | [v] |
| S2 | 500 Meta ads from 50 supplement brands: average run **256 d**; **single image longest (268 d)**; demonstration = 42 % of ads; lifestyle-only underperformed; social-proof words ("bestselling") ran 3.8 % worse than functional-benefit words ("collagen", "probiotic"); quiz funnels 6.6 % | [Evolut via DAN](https://digitalagencynetwork.com/the-supplement-ad-report-2025-what-actually-works-in-meta-advertising-now/) | [v], method thin |
| S3 | Question hooks open only 8 % of 30+ day survivors; pain-point, authority and visual pattern-interrupt = 71 % | Brandsearch via [Segwise](https://segwise.ai/blog/why-boring-ads-beat-polished-ads) | [v] |
| S4 | Create (creatine) runs ~130 active Meta ads, ~63 new per week; mix: demo 20 %, montage 11 %, testimonial 9 %; hooks: "Creatine: LIE vs TRUTH", "Creatine vs Caffeine", bundle "$180 → $114", "Now at Target"; a 20 s us-vs-them shows chalky powder vs clean dissolve | [Motion library](https://motionapp.com/library/create-wellness) | Ad-library read |
| S5 | Create has sold 250M+ gummies since 2022; $5M Series A led by Unilever Ventures; in Target nationwide | [NutraIngredients](https://www.nutraingredients.com/Article/2025/10/29/create-wellness-ceo-on-its-creatine-gummy-journey-into-the-mass-market) | Press |
| S6 | Liquid I.V.: TikTok geo-lift found true impact **2.5× platform-reported**; incremental CPA < half of reported | [WorkMagic](https://workmagic.io/case-study/liquidiv) | [v] |
| S7 | Liquid I.V.: Web+Shop ads **71 % higher iROAS** than Web alone; **62 % of TikTok's incremental impact landed on Amazon** | [TikTok case](https://ads.tiktok.com/business/en-US/inspiration/liquid-iv-tiktok-case-study) | [c] |
| S8 | Bloom: TikTok Shop sales **82 % affiliate video**, 5 % live, 13 % product card; founder story "built more trust than third-party certifications" | [FastMoss](https://www.fastmoss.com/blog/how-bloom-quietly-dominated-tiktok-shop-in-the-past-6-months/) | [v], page has template gaps |
| S9 | Therabody "Workout Called Life": ROAS **11.34** (2023), awareness doubled in key segments | [WARC](https://www.warc.com/content/article/warc-awards-effectiveness/therabody-for-the-workout-called-life/en-gb/158915) | [c] awards entry |
| S10 | WHOOP interactive video: **9.1 % CTR**, +31 % consideration | [Infillion](https://infillion.com/case-studies/whoop/) | [v] |
| S11 | Oura: revenue ≈ **$1B in 2025**, +100 % YoY [v]; 5.5M rings sold, over half in the last year [c] | [Sacra](https://sacra.com/research/oura), [Business Wire via Sherbrooke Record](https://business.sherbrookerecord.com/sherbrookerecord/article/bizwire-2025-9-22-ura-surpasses-55-million-rings-sold-and-doubles-revenue-for-the-second-year-in-a-row-empowering-millions-to-live-better-longer) | — |
| S12 | LMNT scaled through podcast sponsorships and a free-sample (pay-shipping) funnel | [adlibrary](https://adlibrary.com/brands/lmnt) | [v] [unverified] |
| S13 | AG1 paid partner scripts: Supplement Replacement, Simple Routine, Personal Transformation, 90-Day Commitment; welcome-kit funnel "60 % of paid volume" | [Influee](https://influee.co/es/content-hub/ag1-meta-ads-teardown) | [v] [unverified] |
| S14 | Health & Fitness had the highest vertical Meta CPA ($52.98) in one 2025 set | [Trendtrack](https://www.trendtrack.io/blog-post/meta-ad-spend-by-industry) | [v] |
| S15 | Supplements run under 10 % of DTC TikTok spend at ~1.10× ROAS | [EightX](https://eightx.co/blog/marketing-channel-mix-benchmarks-meta-vs-google-vs-tiktok) | [v] [unverified] |
| S16 | Our measured set: product or name at 0.0 s in 12/19 read by eye; hands-only or hands-dominant 8/19; steady music bed in 2/23; paid AG1 ASL 1.3–1.6 s | §1.2 | [m] |

### 2.1 What this means, by sub-niche `[inf]`

| Sub-niche | Lead format | Hero length | Proof that converts | Where VXO's AI wins | Where it must not go |
|---|---|---|---|---|---|
| **Powders, greens, electrolytes** | Hands ritual (scoop/pour/shake/recipe), 7–17 s | 8–15 s + 6 s loop | Grams per serving, NSF/Informed Sport seal, "mixes clean" demo filmed for real | Impossible pours, scale, metaphor, recipe loops | Body change, "bloat gone", energy claims as visuals of people |
| **Gummies and capsules** | Stack/unbox + one-line POV caption | 8–12 s | COA per batch, grams of active, third-party test | Product macro, stop-motion stacking, scale gags | "Same as powder" claims (§0.8), invented lab footage |
| **Energy and pre-workout** | Comedy + one CG insert (Ghost), flavour drops | 10–18 s | Caffeine mg on can, Nutrition/Supplement Facts | Body X-ray gag, flavour collab can renders | Heart-pounding, "insane pump", minors |
| **Wearables (ring, band, sleep)** | Data-as-punchline memes; spec ladder for launches | 6–15 s; 30 s for launch | Real app screenshot, battery days, waterproof rating | Scale and toughness metaphors, object comedy | Generated UI numbers, diagnosis words, blood pressure / glucose claims |
| **Recovery devices (massage gun, boots)** | Everyday-strain story + release (Therabody); athlete day + data (Hyperice) | 15–30 s | Percussion depth (mm), battery, quiet dB | Surreal release, knot metaphors | "Treats", "heals", injury recovery claims |
| **Home gym gear** | Space-saving reveal, neighbour/noise comedy, one-product-replaces-15 | 12–20 s | Weight range, footprint, dial seconds | Clean stacks, mechanism macros, rigid-body physics | Shredded-body transformation, "ideal body" |

**The ship pack for this niche** [inf, doc 45 rule 8 adapted]: hero 12–15 s + 6 s loop + one *proof cut* (the hero's opening 3 s + the client's real proof insert + offer card) × 3 text hooks (newness / specific POV / authority-number). Add one 4:5 static from the hero still: statics are the longest-running supplement format (S2).

---

## 3. AI realism pitfalls for this niche, and the fixes

Each fix follows doc 43's rules (one reference per thing that must not change; describe start and end states; script every object's fate; text only from the reference or in post).

| Pitfall | What goes wrong in AI video | Fix (prompt / reference / pipeline) |
|---|---|---|
| **Powder in water** (greens, electrolytes, creatine) | Powder turns the whole glass uniformly green instantly; no clumps, no surface raft; the level doesn't rise | Write the stages: "powder lands as a raft on the surface, a few clumps sink, a green plume curls down, the colour spreads from the bottom up over ~2 s; the level rises 3 mm". Use Kling i2v 5 s with a `last_image_url` of the fully mixed glass so the end state is locked (43 §3). Never show a "clean dissolve" as proof unless the real product does it: a claim demo must be filmed for real (FTC mock-up doctrine, §4) |
| **Powder pours and scoops** | Scoop volume changes mid-pour; powder flows like liquid; no dust | "One level scoop, 9 g; powder falls in a dry stream with a faint dust puff, settles in a cone". Script the scoop's fate: "the scoop is set on the lid, never vanishes" |
| **Shaker cups** | The whisk ball disappears; liquid sloshes through the lid; foam missing | Name the ball in every shot ("a steel whisk ball visible through the translucent wall"). "Foam head 1 cm after shaking, bubbles pop over 2 s". Sound: ball rattle at 6–8 Hz in the audio block (46) |
| **Gummies** | Gummies turn glossy plastic; sugar coat missing; they bend like rubber or fuse together | Ref a real macro of the product. "Matte sugar-sanded surface, translucent core, slight 5 % squash when pinched, returns to shape, never fuses". Keep counts small and scripted ("exactly three gummies") |
| **Capsules and tablets** | Seams vanish; capsules melt; effervescent tablets shrink without bubbles | "Rigid two-piece capsule, seam visible". Effervescent: "bubbles stream from the tablet, it shrinks and lifts, fizz sound" |
| **Sachets and stick packs** | Tear edge regrows; printed text garbles | Product = first reference; label text only from the ref; tear filmed as "the strip tears along the notch and drops out of frame" (fate). Supers and Supplement Facts in post |
| **Supplement Facts / Nutrition Facts panel** | Every video model garbles small regulated text | **Never generate it.** Comp the client's real panel as a flat graphic in post (Ghost does exactly this as its end card [m]) |
| **Cans and bottles in hand** | Can dents morph; condensation crawls upward; label rotates on its own | Kling i2v from a still with the label locked; "condensation beads run down only"; doc 47/11 beverage rules |
| **Wearable screens and app UI** | Numbers change every frame; fake charts; misspelt metrics; heart-rate values implausible | **UI is always a real client screenshot comped in post** (Oura's 148 bpm card is exactly this [m]). Generate the device screen dark or as a blank green card for tracking |
| **Ring and band sensors** | The inner sensor bumps vanish, move or multiply; LEDs glow the wrong colour | Two refs: outer face and inner sensor side. Write "three raised sensor domes inside, green and red LEDs only when worn". Count check in QC (48 §7.1) |
| **Skin under a wearable** | Ring sinks into the finger; band floats above the wrist; no strap indentation | "The band presses a faint indentation into the skin; the strap follows the wrist curve". Use a real hand plate where possible |
| **Sweat** | Oily full-body gloss; beads that crawl upward; sweat on dry fabric | "Fine beads on the temple and upper lip only; one bead runs down; grey T-shirt shows a darker patch at the sternum". Sweat is optional in this niche: prefer hands and objects |
| **Muscles and bodies** | Hyper-veined, plastic, impossible physiques; arms change size between shots | Policy-sensitive too (§4: no "ideal body"). Use clothed, average, real-proportioned performers, mid-shots, or hands. No transformations, ever |
| **Gym iron** | Plates pass through each other; numbers garble; the bar bends; dumbbells change size; dials spin freely | Rigid-body language from 43 §5: "steel plates are rigid, never bend or overlap; the dial clicks in 2.5 lb detents and stops". Keep weight numbers out of frame or comp them. Close rigged angles, not wides |
| **Massage gun** | The head floats off the skin; no percussion ripple; it buzzes like a toothbrush | "Percussion head travels 16 mm at 40 hits per second; the skin ripples outward in a small ring at each hit; the device body vibrates slightly". Sound: low thud at the real rate, mixed in post |
| **Ice and condensation** | Ice cubes melt instantly or never; cubes clip through glass | "Clear ice cubes with trapped berries; they bob, clink and stay solid". Ice is a strong ASMR hook (AG1 freezer prep [m]) |
| **Scale gags with animals/insects** | Wrong anatomy (six legs become eight), bugs walking on air | One insect per shot; macro lens language; "six legs, each foot touches the surface". Use stock macro footage licensed by the client as reference |
| **Hands** | Extra fingers; a scoop held by no one | 43 §5 hand rules; "exactly five fingers"; contact points named |

---

## 4. Ad policy and legal constraints

US first. The client's counsel has the final word; flag every film for their review.

### 4.1 The claim ladder (what a film may say or show)

| Claim type | Example | Status | VXO rule |
|---|---|---|---|
| **Disease claim** | "treats anxiety", "lowers blood sugar", "cures insomnia", "reduces inflammation" (in a disease context) | Turns a supplement into an unapproved drug (FDA); Meta bans "cure, heal, eliminate" for diseases like diabetes and cancer | **Never.** Not in VO, super, visual metaphor or caption |
| **Structure/function claim** | "supports restful sleep", "supports muscle strength", "supports hydration" | Allowed on labels with the DSHEA disclaimer, but **the FTC treats it like any health claim in advertising**: it needs competent and reliable scientific evidence for the finished product, and the disclaimer "won't cure an otherwise deceptive ad" ([FTC](https://www.ftc.gov/business-guidance/resources/health-products-compliance-guidance)) | Only the client's own wording, supplied in writing with its substantiation. Add `*These statements have not been evaluated by the Food and Drug Administration…` as a legible end super when any S/F claim appears |
| **Implied claim by image** | A tired face turning radiant; a belly shrinking; a bar graph rising | The FTC judges "the ad as a whole, including images and product names" | Metaphors are fine for *experience* (calm, refresh) but never as a *result* on a body |
| **Fact claim** | "5 g creatine monohydrate per serving", "1,000 mg sodium", "NSF Certified for Sport" | Must be true per batch | Show it as a super from the label; the client confirms the COA. Given the gummy test scandal (§0.8), this is a selling point |
| **Comparative claim** | "vs chalky powder", "beats Brand X" | Invites NAD challenges ([NutraIngredients, SSG 2025](https://www.nutraingredients.com/Article/2025/11/24/ssg-2025-asa-waldstein-on-fda-ftc-and-nad-enforcement-trends)) | Compare to a *generic* category or to the old habit, never a named rival |
| **Testimonial / endorsement** | "I sleep 2 hours more" | Must reflect typical results; "results not typical" does not cure it; material connections disclosed; fake/AI testimonials banned (FTC rule, up to $51,744 per violation; doc 45 §5.3) | **No AI person ever gives a testimonial.** Real reviews only, verbatim, from the client |
| **Weight / muscle claim** | "lose 10 lbs", "gain 5 lbs of muscle" | Meta 18+ and "time taken to achieve noticeable results"; TikTok 18+, no "without diet or exercise", no "easy or guaranteed" | Avoid in VXO films. If the client insists: 18+, timeframe stated, diet+exercise line, counsel sign-off |

**Recent enforcement to quote to buyers:** NAD cases in 2025–26: Ryze dropped mushroom-coffee and matcha health claims; Olly's libido claim evidence didn't cover "sensation"; Reus Research, Niagen and Iron Rock (NAD+) were told to modify or discontinue claims; Brainiac had to modify cognitive-enhancement claims ([NutraIngredients](https://www.nutraingredients.com/Article/2025/11/25/what-stakeholders-can-learn-from-nads-national-2025-dietary-supplement-case-decisions), [BBB Programs](https://bbbprograms.org/media/newsroom/decisions/niagen)). In April 2023 the FTC sent Notices of Penalty Offenses to 670 supplement, OTC and functional-food advertisers, enabling civil penalties of ~$50K per violation ([Haynes Boone](https://www.haynesboone.com/news/alerts/ftc-warns-nearly-700-advertisers-about-proper-substantiation-and-endorsement-practices)).

### 4.2 Platform rules

| Topic | Meta | TikTok | VXO rule |
|---|---|---|---|
| Age targeting | Dietary, health, weight-loss and weight-gain products and services: **18+**. Protein/general food exempt ([Meta](https://transparency.meta.com/policies/ad-standards/restricted-goods-services/health-wellness)) | Weight-loss or muscle-gain claims: **18+** ([TikTok](https://ads.tiktok.com/help/article/tiktok-ads-policy-weight-management)) | Brief every client: the paid cut runs 18+. No youth-coded casting, school settings, cartoons aimed at kids |
| Before/after | Weight-loss side-by-side transformations prohibited (Pilates-class exception); no pinching fat close-ups; no "results solely from wearable products" ([Meta personal health & appearance](https://transparency.meta.com/policies/ad-standards/objectionable-content/personal-health-and-appearance)). A 22 Jul 2026 policy change log entry exists; one vendor says before/after is now claim-reviewed rather than auto-rejected ([Adligator](https://adligator.com/blog/meta-health-wellness-ad-policy-update-2026)) [unverified] | Not in the fetched text; treat as prohibited for weight [inf] | **No before/after of bodies, ever** (and AI-made ones are exactly what the 35 AGs flagged) |
| Body image | No negative self-perception, no "perfect body" | No body-shaming, no "ideal body type", no "appearance makes you more desirable, successful, happy" | Comedy never punches at a body. Punch at habits, objects, routines |
| Disease / miracle | No "cure, heal, eliminate" for incurable diseases; no clickbait in health/weight context | Exaggerated claims prohibited | §4.1 ladder |
| Measurement | Lower-funnel events (Purchase, Add to Cart) restricted for many Health & Wellness-classified accounts since Jan 2025 [v] | — | Expect clients to optimize on upper-funnel events: hook rate and hold matter more here than in other niches |
| AI labels | AI-info label; photoreal AI people always labelled (45 §5.3) | AIGC label mandatory for realistic AI in ads (45 §5.3) | Label every film. No photoreal AI people in paid cuts in this niche at all (§0.7) |

### 4.3 Devices and gear

- **FDA General Wellness policy (final, 6 Jan 2026):** FDA uses enforcement discretion for low-risk products intended only for general wellness, and the revision now covers wearables reporting physiologic values such as heart rate variability and even a wrist-worn blood-pressure example ([King & Spalding](https://www.kslaw.com/insights/articles/fda-updates-general-wellness-and-clinical-decision-support-guidance-documents), [Womble](https://www.womblebonddickinson.com/us/insights/blogs/fdas-2026-general-wellness-policy-and-what-it-means-manufacturers-wearable-devices)). The line is still **intended use**: words like "diagnose", "detect hypertension", "medical-grade", "monitor your condition" pull a device into FDA device rules. WHOOP's July 2025 warning letter cited "medical grade" and blood-pressure language ([AFS](https://www.afslaw.com/perspectives/alerts/not-fdas-whoop-ing-boy-how-warning-letter-became-wellness-playbook)). **VXO rule: device films show lifestyle data (sleep, readiness, steps, HRV trend) as wellness insight; never diagnosis words, never a medical setting.**
- **Massage and recovery devices:** say "recovery", "relieves everyday muscle tension" only if the client's labeling says so. "Treats injuries", "reduces inflammation", "heals" are medical claims. Some percussion devices are FDA-registered Class I/II; use exactly the client's cleared wording [inf].
- **Home gym gear:** safety realism matters (CPSC recalls on adjustable dumbbells and treadmills exist [unverified for specific 2025–26 cases]). Never show unsafe use as a joke (a dropped dumbbell near a child, a running treadmill with a pet on it).

### 4.4 State law

- **New York GBL §391-oo** (in force April 2024): no sales of OTC weight-loss or muscle-building supplements to under-18s; age verification required; protein products generally excluded; trade groups sued ([Insurance Journal](https://www.insurancejournal.com/news/east/2024/05/06/772393.htm), [Mondaq](https://mondaq.com/unitedstates/healthcare/1485534/what-is-new-yorks-new-policy-on-supplement-sales-to-minors)). Creatine marketed for muscle falls in scope [inf]. California AB 82 failed in 2024 ([NutraIngredients](https://www.nutraingredients.com/Article/2024/08/16/California-bill-to-restrict-access-to-weight-loss-products-fails)).
- **New York synthetic-performer disclosure** (9 Jun 2026) applies to any AI human in an ad (45 §5.3).

### 4.5 Pre-flight checklist for this niche (add to 45 §5.4 and 46)

- [ ] Every claim word is from the client's approved claims list, with substantiation on file. No disease word anywhere (VO, super, caption, metaphor).
- [ ] S/F claim → DSHEA disclaimer super, legible, on screen ≥ 2 s.
- [ ] No AI person vouches, demonstrates a result, wears a lab coat or plays a doctor, nurse, trainer or customer.
- [ ] No before/after, no body transformation, no bodies as the joke, no "ideal body".
- [ ] Supplement Facts, Nutrition Facts, app UI and numbers are real client assets comped in post.
- [ ] Demo of a product property (mixes clean, waterproof, quiet) is filmed for real or supered "Dramatization"; a dramatized property cannot be the proof.
- [ ] Device: no diagnose/detect/medical-grade wording; no clinic setting.
- [ ] Paid cut set to 18+; casting and setting read adult.
- [ ] AI label on (Meta/TikTok); C2PA kept.

---

## 5. The buyer

### 5.1 Who signs a $1,200–3,500 film

| Company stage | Who signs | Who else must say yes | What they compare us with |
|---|---|---|---|
| **Founder-led, < $5M revenue** (one hero SKU, Shopify + Amazon + TikTok Shop) | Founder (often a trainer, athlete, dietitian or the founder's own health story, cf. Bloom S8) | A regulatory consultant or the contract manufacturer's claims reviewer | $50–500 AI UGC clips (doc 45 D44), affiliate creators paid in product |
| **$5–30M** | Head of Growth / Performance Marketing lead | Creative strategist; **compliance/regulatory reviewer** (in-house or fractional counsel); founder for brand | In-house editor + creator network; agencies at $3–10k a month |
| **$30M+** (AG1, Oura, WHOOP tier) | Brand creative director or social lead | Legal, medical/science team, brand | Agencies (Forsman for Therabody), celebrity budgets; VXO only fits as a *volume* or *launch-teaser* supplier here |

Purchase timing [inf]: January ("new year, new routine") and pre-summer are the spend peaks; product launches and new flavours are the reason to buy a film (AG1 Pro, Oura Ring 5, Ghost flavour collabs [m]).

### 5.2 What they fear (in order of pain) `[inf]`, with evidence

1. **Claim trouble.** An FTC notice, an NAD challenge or an ad-account ban for health claims is existential for a small supplement brand (§4). A creative partner who writes claims on their own is a liability.
2. **Looking like a scam.** AI + supplements is the exact combination the 35 AGs and the NYT pointed at (§0.7). A founder who sells on trust fears that an obviously AI film makes them look like the drop-shippers.
3. **Pretty and useless.** Cinematic b-roll scales at 6.85 % vs 11.6 % for text-led work (doc 45 D3). Their best ads are founder UGC (S1). They fear paying for a mood film that doesn't move CPA.
4. **Account restrictions on measurement.** If Meta restricts their Purchase event, they can't prove ROAS for any creative (§4.2), so they distrust any vendor promising ROAS.
5. **Wrong product.** A gummy that looks like someone else's, a can with a misprinted panel, a ring with the wrong sensor layout on screen.
6. **Fatigue.** They need new hooks every few weeks (Create ships ~63 new ads a week, S4).

### 5.3 What proof they need from VXO

- **A compliance-first process, visible on the pitch:** "We never write claims. You send your approved claims list; we storyboard only with those. Your reviewer signs the board before we generate." This is the single strongest differentiator in this niche [inf].
- **The real-proof slot:** every film reserves 2–4 s for the client's real asset: their COA or NSF seal on the actual batch, a real customer review card (verbatim), their founder's 3 s phone clip, or a real app screenshot. AI carries attention; the real slot carries belief (47 §0.9, generalized). Ritual's paid 6 s mic-up of its real science team (§1, 1c) shows the slot can itself be the joke.
- **Fidelity proof:** their own product in 5 free frames, label and panel exact, gummy colour exact, sensor layout exact.
- **A hook pack, not a hero:** 3 hooks × (hero 12–15 s, 6 s loop, proof cut) + 1 static, so a $1,200 Short feeds two weeks of testing.
- **A spec test number when we have one:** doc 45 §4 test plan. Until then, no ROAS promises (they won't believe them, §5.2.4).

### 5.4 Twenty example brand types (types, not targets; no outreach)

1. Creatine gummy brand selling on TikTok Shop and Target (Create-type)
2. Women's creatine / strength-supplement brand (Bloom/Arrae-type)
3. Greens powder with a celebrity or podcast funnel (AG1-type)
4. Gummy greens / superfood gummies (Grüns-type)
5. Electrolyte stick packs, sugar-free, athlete-founded (LMNT-type)
6. Hydration multiplier sold heavily on Amazon (Liquid I.V.-type)
7. Liposomal liquid-sachet supplements (Cymbiotika-type)
8. Magnesium / sleep stack powder or drink
9. Clean pre-workout with flavour collabs (Ghost-type)
10. Protein powder or clear whey for women
11. Probiotic / gut-health capsule with subscription (Seed-type)
12. Mushroom coffee / adaptogen drink (category under NAD scrutiny: claims care)
13. Smart ring / sleep wearable startup (Oura-type, smaller)
14. Fitness band accessory maker (straps, charms, Meridian-type bands)
15. Massage gun / mini percussion device (Therabody-type, smaller)
16. Compression recovery boots (Hyperice Normatec-type)
17. Adjustable dumbbells or compact home-gym hardware
18. Smart jump rope or connected resistance bands
19. Sunrise alarm / sleep-sound device (Hatch-type)
20. Cold-plunge tub or sauna-blanket brand

---

## 6. Eight ready film concepts (invented brands, VXO spec)

Conventions:
- 9:16 master; 4:5 reframe; 6 s loop; proof cut (§2.1).
- Every camera position is one a real crew could rig (41 §4). Physics read per doc 41 §2 and 44 §4.
- Costs are list prices from doc 43 §6 [EST]: Seedance 2.5 r2v $2.06 / $4.62 per 10 s at 480p / 720p; Cinema Studio 4.0 720p $4.62 per 10 s; Kling 3.0 Pro i2v sound off **$0.48 per 5 s insert**; Wan 3.0 480p previs $0.05/s; stills ≈ $0.30 each. Takes: ×3 for multi-shot, ×2 for inserts.
- Brand names are invented; clear them before use. Claims shown are placeholders the client replaces with its approved list. **Real insert** = the client's real asset (§5.3).
- Otto (deadpan director, huge moustache, mouth never visible) and Vee (producer, one silver stopwatch) appear only where noted, and only because these are VXO spec films.

### C1 · KILNWORK Creatine Gummies — "The Receipt" (15 s)

- **Idea:** a gummy is weighed like gold. A jeweller's scale, tweezers, a loupe. The deadpan assay of one gummy ends with a printed receipt rolling out of a lab printer: the batch COA. The product's proof *is* the punchline.
- **Hook (0–1 s):** macro, a pair of brass tweezers sets one sugar-coated gummy on a gold-assay scale pan; the pan dips with a *tink*. Super: "We weigh every batch."
- **Punchline (product-caused):** the receipt prints, tears off and lands next to the jar; a hand stamps it "5 g ✓". Final: the hand takes a gummy from the jar instead of the tweezers.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Macro on a tabletop slider, 100 mm: tweezers place the gummy on the scale pan; pan dips 2 mm | Kling i2v from a Flare still, end frame = pan settled |
| 2 | 1.5–3.5 | Top-down locked-off: jeweller's bench, loupe, ledger, the jar | Cinema Studio, `camera_movement` none, product ref first |
| 3 | 3.5–5.5 | Over-the-shoulder medium, tripod: Otto (back to camera, moustache in profile) lifts the loupe | Otto ref sheet; mouth never visible |
| 4 | 5.5–7 | POV through the loupe (a real loupe-adapter macro): the gummy's sugar crystals | Kling i2v; "matte sugar-sanded surface, translucent core" |
| 5 | 7–9.5 | Medium, locked-off: a small lab label printer chatters; a paper receipt feeds out | Receipt text blank in generation; COA comped in post |
| 6 | 9.5–11.5 | Insert, slider: a rubber stamp comes down on the receipt | **Real insert option:** the client's actual COA scan |
| 7 | 11.5–13.5 | Top-down: a hand skips the tweezers, takes a gummy straight from the jar | Hands only |
| 8 | 13.5–15 | End card: real pack photo; "5 g creatine monohydrate per serving. Third-party tested." + DSHEA super if any S/F claim | Real photo |

- **Physics check:** jeweller's scales dip and settle (damped, 2–3 oscillations); gummies don't bounce; the receipt curls off the printer and falls by gravity; the stamp compresses then lifts. Every rig (slider, tripod, loupe adapter) is standard tabletop kit.
- **Claim check:** "5 g per serving" and "third-party tested" only if the client's COA shows it per batch. No "works as well as powder".
- **Audio map:** 0.4 s brass *tink*; 1.5–3.5 s quiet room tone, clock tick; 5.5 s loupe click; 7–9.5 s printer chatter (dot-matrix, 1.8 s); 10.4 s stamp thud (sub hit); 12 s jar lid twist; 13.5 s silence → logo sting. No music. Optional VO in the end card: `[dry] Weighed. Not guessed.`
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Wan 3.0 480p previs, 15 s ×2 | $1.50 |
  | Cinema Studio 4.0 shots 2, 3, 5, 7 (10 s total): 480p proof $2.08 + 720p ×3 $13.86 | $15.94 |
  | Kling i2v inserts (1, 4, 6), 5 s ×2 each | $2.86 |
  | Stills, 8 | $2.40 |
  | **Total** | **≈ $23** |

### C2 · TIDELINE Electrolytes — "Salt Lick" (12 s)

- **Idea:** a deadpan nature-doc parody. A deer at a salt lick in a misty forest. Pull back: the "salt lick" is a giant TIDELINE stick pack lying in the clearing, and a line of joggers waits politely behind the deer.
- **Hook (0–1 s):** telephoto, a deer's tongue meets a white crystalline block; dew, birdsong. Super: "Even they know."
- **Punchline (product-caused):** the scale reveal: the block is the product. The last jogger in line checks a running watch, sighs, and the deer keeps licking.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–2 | 400 mm telephoto on a tripod, hide position: deer licks the block | Seedance r2v; "real deer anatomy, four legs, natural ear flicks" |
| 2 | 2–4 | Macro on a slider: salt crystals on the block glint, dew drops | Kling i2v |
| 3 | 4–7 | Drone pull-back (real FPV rule: open clearing, no traffic): the block is a 2 m stick pack; four joggers in a queue | Cinema Studio `aerial-pullback`; label from ref |
| 4 | 7–9 | Medium from behind the queue, gimbal: the last jogger checks a plain watch | Watch face blank; no faces close |
| 5 | 9–10.5 | Medium on the deer, telephoto: it keeps licking, ears flick | |
| 6 | 10.5–12 | End card: real stick pack in a bottle of water, fizz; "1,000 mg sodium. Zero sugar." | Real insert: client's product filmed mixing |

- **Physics check:** deer scale and gait real; joggers stand still (no running physics needed); the giant pack is rigid foil with crinkle highlights; drone path is a straight pull-back over an open clearing.
- **Claim check:** sodium figure from the label; no "prevents cramps".
- **Audio map:** forest dawn bed with a wood thrush; 0.3 s lick; 4 s soft whoosh on the reveal; 8 s jogger sigh (non-lip, back to camera); 11 s foil tear + fizz; narrator VO in nature-doc register optional: `[hushed] The rarest of minerals… in the most common of queues.`
- **Models and cost:** Seedance r2v 10 s (shots 1, 4, 5): 480p $2.06 + 720p ×3 $13.86 = $15.92; Cinema Studio shot 3, 4 s ×3 at 720p = $5.54; Kling insert 2 ×2 = $0.95; stills $1.80. **≈ $24.**

### C3 · STILLWATER Magnesium Night Drink — "2:13 a.m." (15 s)

- **Idea:** a fridge seen from inside. Every night the door opens at 2:13 a.m. and the same hand reaches for leftovers. Tonight, at 9 p.m., the hand takes the STILLWATER can instead. 2:13 comes; the fridge light stays off; the leftovers wait. Last shot: a sticky note on the cheesecake: "u ok?".
- **Hook (0–1 s):** the inside-fridge camera; the door swings open, light floods, a time super "2:13 AM".
- **Punchline (product-caused):** the fridge stays dark at 2:13 because the owner is asleep. The object (cheesecake with a note) misses them.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–2 | Locked-off camera inside the fridge (a real "fridge cam" rig, lipstick camera on the back wall): door opens, hand grabs cheesecake | Seedance r2v; kitchen ref |
| 2 | 2–3.5 | Same rig, montage of two more nights: "2:13 AM" ×2 with jump cuts | Same frame, hard cuts |
| 3 | 3.5–6 | Kitchen counter, 9:00 PM super, tripod medium: hand cracks a STILLWATER can, pours into a glass | Kling i2v; condensation runs down only |
| 4 | 6–8 | Hallway, locked-off: bedroom door closes, light under the door clicks off | |
| 5 | 8–11 | Inside-fridge cam again: "2:13 AM" super; darkness; the fridge hum; nothing happens | Hold: the pause is the joke (44 §8.4) |
| 6 | 11–13 | Inside fridge, next morning light: a sticky note on the cheesecake: "u ok?" | Note text in post |
| 7 | 13–15 | End card: can on a nightstand; "Magnesium + L-theanine. Supports relaxation.*" + DSHEA super | Real product photo |

- **Physics check:** fridge light comes on only with the door open; the inside rig is a real technique; pour from a can foams slightly; light under a door goes off with a click.
- **Claim check:** "supports relaxation" only from the client's approved list, with disclaimer. Never "cures insomnia", never "sleep 2 hours more".
- **Audio map:** fridge seal pop + hum at 0.1 s; 2–3.5 s three pops on the cuts; 3.6 s can crack + pour fizz; 7.6 s light-switch click; 8–11 s fridge hum alone, one ice-maker clunk at 10.2 s; 12 s morning birds; logo sting.
- **Models and cost:** Seedance r2v 12 s (shots 1, 2, 4, 5, 6): 480p $2.47 + 720p ×3 $16.63 = $19.10; Kling insert shot 3 ×2 = $0.95; stills $2.10. **≈ $22.**

### C4 · ORBIT Sleep Ring — "Snitch" (10 s)

- **Idea:** the Oura "exposed me" structure, faceless. A husband's hand types "slept great 😴" in a family chat at breakfast. A notification slides in from the ring's app on the same phone: "Bedtime 2:47 AM · Sleep score 41". The wife's hand slides a cold brew across the table without a word.
- **Hook (0–1 s):** POV over the phone, the thumb typing "slept great"; the ring on the finger in frame.
- **Punchline (product-caused):** the ring's data contradicts him; the wife's deadpan coffee push is the response.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–2.5 | POV top-down over the phone at a breakfast table (chest rig): typing; ring visible | Phone screen = green card, chat UI comped in post |
| 2 | 2.5–4.5 | Same POV: a notification slides in | **Real insert:** client's app screenshot |
| 3 | 4.5–6.5 | Macro on the ring, slider, sensors catching light | Kling i2v; inner-sensor ref |
| 4 | 6.5–8.5 | Wide-ish, table level, locked-off: a second hand slides a cold brew into frame; it stops against his hand | Glass slides with real friction, ice clinks |
| 5 | 8.5–10 | End card: ring on its charger; "Know your night." | Real photo |

- **Physics check:** chest-rig POV is standard; the glass slides and stops (no ice teleport); ring sensors fixed in number.
- **Claim check:** sleep score is wellness data; no "detects sleep apnea".
- **Audio map:** keyboard taps 0–2 s; iOS-style notification ding at 2.6 s (an original sound, not Apple's); 4.5 s silence; 6.8 s glass slide on wood + ice clink at 7.3 s; logo sting.
- **Models and cost:** Seedance r2v 6 s (shots 1, 2, 4): 480p $1.24 + 720p ×3 $8.32 = $9.56; Kling insert ×2 $0.95; stills $1.50. **≈ $12.** Cheapest concept; ideal for a Short.

### C5 · KNOTWORK Mini Massage Gun — "Knot Removal Service" (15 s)

- **Idea:** a sailor's rope knot sits on a sculpted plaster shoulder like a display piece in a hardware store. A clerk's hand applies the massage gun; with each pulse the knot loosens, and after three hits the rope lies straight. The clerk rings the counter bell. The next customer slides a tangled bag of headphone cables onto the counter.
- **Hook (0–1 s):** macro, a tight monkey's-fist knot on a white plaster trapezius; a hand lifts the gun into frame, it starts with a buzz.
- **Punchline (product-caused):** the knot literally unties; the escalation (cables) is the button.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–2 | Macro, tabletop slider: the knot on the plaster shoulder; gun enters | Product first ref |
| 2 | 2–5 | Medium, locked-off: three pulses; the knot loosens step by step | Seedance r2v; "each hit makes the rope fibres jump; the knot loosens one turn per hit, never re-ties" (object fate) |
| 3 | 5–7 | Overhead, locked-off: rope lies straight on the plaster | |
| 4 | 7–8.5 | Insert: a hand taps a brass counter bell | Kling i2v |
| 5 | 8.5–11 | Medium: Otto behind the counter (moustache, mouth hidden), deadpan; a hand slides a ball of tangled cables in front of him | Otto ref sheet |
| 6 | 11–13 | Close on Otto's eyes: one slow blink | 44 §8.4 deadpan |
| 7 | 13–15 | End card: the gun on white; "16 mm percussion. 45 dB quiet. 6 hr battery." Super: "Dramatization." | Real photo; specs from client |

- **Physics check:** percussion head moves along its axis only; rope physics (fibres, friction) believable as a dramatized metaphor, so the "Dramatization" super is mandatory; bell rings with a real tap.
- **Claim check:** no "removes muscle knots" claim in text. The metaphor + specs carry it; specs must be real.
- **Audio map:** 0.8 s motor spin-up; 2–5 s three low thuds at the real percussion rate, each with a rope creak; 7.6 s bell *ding* (clean, 1.5 s decay); 9.5 s cable rattle; 11–13 s silence; logo sting.
- **Models and cost:** Seedance r2v 10 s (shots 1–3, 5–6): 480p $2.06 + 720p ×3 $13.86 = $15.92; Kling inserts (4) ×2 $0.95; stills $2.10. **≈ $19.**

### C6 · DIALSET Adjustable Dumbbells — "Downstairs" (20 s)

- **Idea:** the downstairs neighbour's ceiling: every night the pendant lamp swings and the plaster dusts down as dumbbells clatter above. Tonight the upstairs tenant replaces a rack of 15 pairs with one DIALSET pair. Downstairs, the lamp stays still; the cat stays asleep on the sofa.
- **Hook (0–1 s):** sound first: a heavy iron *clang* over black, then a pendant lamp swinging in a dark living room.
- **Punchline (product-caused):** silence downstairs. The downstairs neighbour (Otto, in an armchair, back three-quarters) slowly lowers the broom he was about to bang on the ceiling.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–2 | Locked-off wide, downstairs living room: pendant lamp swinging, dust sifting, Otto with a broom raised | Seedance r2v; "lamp is a rigid pendant on a cord, swings 10° and damps" |
| 2 | 2–4 | Upstairs, tripod wide: a full rack of 15 dumbbell pairs, one pair thrown down on a mat | No people faces; hands and shoes |
| 3 | 4–6.5 | Upstairs, slider: the rack is wheeled out the door; a single DIALSET pair sits on a small mat | Rigid iron; no plates in motion |
| 4 | 6.5–9 | Macro, tabletop slider: the dial clicks from 25 to 52.5 lb, plates engage | Kling i2v with `last_image_url`; numbers comped in post |
| 5 | 9–12 | Upstairs medium: a controlled set, the dumbbells placed back in the cradle, no drop | Gimbal at waist height |
| 6 | 12–15.5 | Downstairs wide, same frame as shot 1: lamp still; cat asleep; Otto lowers the broom | The hold is the joke |
| 7 | 15.5–18 | Close: the cat's ear twitches once | |
| 8 | 18–20 | End card: "15 pairs. One footprint. 5–52.5 lb." | Real product photo |

- **Physics check:** iron is rigid; plates select by the dial only; the set is controlled (no dropping, which is also the safety rule); the pendant lamp damps with real pendulum period (~1.5 s for a 0.5 m cord).
- **Claim check:** weight range and "replaces 15 pairs" must match the spec; no physique shown.
- **Audio map:** 0.0 s iron clang (sub + metal ring), plaster patter 0.5–2 s; 2.5 s second clang upstairs; 4 s rack wheels; 6.8–8.5 s dial clicks (11 detents); 9–12 s soft cradle thunk; 12–15.5 s room tone + clock; 16 s cat purr; logo sting.
- **Models and cost:** Seedance r2v 15 s (1–3, 5–7): 480p $3.09 + 720p ×3 $20.80 = $23.89; Kling insert ×2 $0.95; stills $2.40. **≈ $27.**

### C7 · FIELDDAY Greens — "The Pill Organizer Retires" (15 s)

- **Idea:** a 7-day pill organizer on a kitchen counter, lid by lid, opens on its own each morning: Monday empty, Tuesday empty, Wednesday empty. A scoop of greens goes into a glass beside it. By Sunday the organizer holds earrings, then paper clips, then a single dog treat.
- **Hook (0–1 s):** macro, the "MON" lid snaps open with a plastic click: empty.
- **Punchline (product-caused):** the organizer has a new career; the product replaced its job. Final shot: the dog's nose pushes the "SUN" lid open.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Macro, locked-off: MON lid snaps open, empty | Kling i2v; lid hinge rigid |
| 2 | 1.5–4 | Top-down, slider: one level scoop of green powder into water; raft, plume, spread over 2 s | Kling i2v with end frame = mixed glass (§3) |
| 3 | 4–7 | Same macro as 1, three hard cuts: TUE empty, WED earrings, THU paper clips | Seedance r2v, "exactly these objects, nothing else" |
| 4 | 7–9.5 | Medium, tripod: a hand shakes the glass, drinks (only hand and glass in frame), the level drops | 41 §2 drinking rule |
| 5 | 9.5–12.5 | Floor level, locked-off: a dog's nose pushes the SUN lid; a treat inside | Dog anatomy ref; one dog |
| 6 | 12.5–15 | End card: pouch; "[N] whole-food ingredients in one scoop." | Real photo + client's claim |

- **Physics check:** powder stages written; the level drops; lids hinge, never bend; dog's nose contact named.
- **Claim check:** "replaces your multivitamin" is a claim needing substantiation; the film only implies a routine change. Avoid "you'll never need supplements".
- **Audio map:** 0.2 s plastic lid click (×4 on each cut, pitched slightly differently); 2 s powder whisper + water swirl; 7.5 s shaker ice rattle; 8.5 s one gulp (off-lip, glass covers the mouth); 10 s dog sniff; 11 s treat crunch; logo sting.
- **Models and cost:** Seedance r2v 8 s (shots 3, 4, 5 partly): 480p $1.65 + 720p ×3 $11.09 = $12.74; Kling inserts (1, 2, plus dog shot if Seedance fails) ×2 = $2.86; stills $1.80. **≈ $17.**

### C8 · DAYBREAK Sunrise Alarm — "Retired Phone" (12 s)

- **Idea:** a phone alarm blares at 6:00; the phone vibrates itself off the nightstand into a glass of water (hook). Rewind-scratch. Same room, same morning, with DAYBREAK: the lamp glows from deep red to warm white from 5:30, birdsong rises, a hand reaches out calmly. The phone lies in the drawer under a label reading "RETIRED".
- **Hook (0–1 s):** extreme close-up, the phone's screen-down vibration walks it to the edge; it drops into the glass with a *plunk*.
- **Punchline (product-caused):** the phone has been retired to a drawer by the lamp.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–2 | Macro, nightstand level, locked-off: phone buzzes, walks, falls into the water glass | Seedance r2v; "phone is rigid, walks 2 cm per buzz, tips and drops; water splashes once" |
| 2 | 2–3 | Same frame: a VHS-style rewind (post effect) | Post only |
| 3 | 3–6.5 | Wide bedroom, locked-off, time-lapse feel: the lamp ramps red → amber → warm white; the room fills with light | Cinema Studio, `light` key changes; no face, a sleeper under the duvet |
| 4 | 6.5–8.5 | Close: a hand reaches out and taps the lamp top | Kling i2v |
| 5 | 8.5–10.5 | Top-down: drawer slides open; phone inside under a label "RETIRED" | Label text in post |
| 6 | 10.5–12 | End card: lamp on white; "Wake with light, not noise." | Real photo |

- **Physics check:** a phone on vibrate does walk on a hard surface; the water splash is one event, the glass doesn't tip; light ramps from the lamp source with matching falloff on the wall.
- **Claim check:** "supports a natural wake-up" style only; no circadian-disorder claims.
- **Audio map:** 0.0 s harsh alarm tone (original), vibration rattle; 1.7 s plunk + muffled buzz; 2–3 s tape rewind; 3–6.5 s birdsong fades up, a soft chime at 6 s; 7 s lamp tap; 9 s drawer slide; logo sting.
- **Models and cost:** Seedance r2v 5 s (shot 1): 480p $1.03 + 720p ×3 $6.93 = $7.96; Cinema Studio 4 s (shot 3) ×3 at 720p = $5.54; Kling inserts (4, 5) ×2 = $1.90; stills $1.80. **≈ $17.**

### 6.1 Concept scorecard

| Concept | Sub-niche | Format it copies [m] | Proof slot | Policy risk | AI-native? | Cost |
|---|---|---|---|---|---|---|
| **C1 The Receipt** | Gummies | Hands ritual + spec super (AG1, Ghost panel end card) | COA (real) | Low | Yes (macro + deadpan) | ≈ $23 |
| C2 Salt Lick | Electrolytes | Scale gag (Oura insects) | Real mixing shot | Low | Yes (giant pack, deer) | ≈ $24 |
| C3 2:13 a.m. | Sleep drink | One-take meme logic (Oura) | Claim + disclaimer | Medium (sleep claim words) | Partly | ≈ $22 |
| **C4 Snitch** | Wearable | Data-as-punchline (Oura "exposed me") | Real app screenshot | Low | Partly (UI is real) | ≈ $12 |
| C5 Knot Removal | Massage gun | Metaphor release (Therabody) | Real specs | Medium (must super "Dramatization") | Yes | ≈ $19 |
| C6 Downstairs | Home gym | Neighbour comedy + space reveal | Real weight range | Low | Yes | ≈ $27 |
| C7 Pill Organizer | Greens | Hands ritual + object comedy | Ingredient count | Medium (replacement implication) | Partly | ≈ $17 |
| C8 Retired Phone | Wellness device | Problem → product reversal | Real product | Low | Partly | ≈ $17 |

**The best concept: C1 "The Receipt" (KILNWORK creatine gummies).**
- It turns the category's biggest buyer fear (gummies that fail lab tests, §0.8) into the punchline, so the film *is* the proof.
- It needs no face that vouches, no body, no health claim beyond a label fact.
- The product is on screen from frame 1; hook = sound + picture (*tink* + gummy on a gold scale).
- It has a real-proof slot built in (the client's COA), which answers fear #1 and #2 in §5.2.
- It fits the hottest TikTok Shop sub-category (creatine gummies, S4–S5) and costs ≈ $23 to make.

For a VXO niche reel, make **C1 + C4 + C6**: ingestible proof, device data comedy, gear scale. Together they cover the three sub-niches.

---

## 7. QA gate additions for this niche

Run after doc 44 §10, doc 45 §5.4 and doc 46:

1. Claim audit: every word on screen and in VO is on the client's approved list (§4.1). Disclaimer present if any S/F claim.
2. No AI person vouches, demonstrates a result, or appears in medical clothing or a clinic.
3. No body, before/after or physique as the subject or the joke.
4. Supplement/Nutrition Facts, app UI and numbers: real assets, comped, legible, unchanged across shots.
5. Counts: gummies, capsules, sensors, plates, dial detents match the reference in every frame (2 fps strip).
6. Powder/liquid stages follow the written physics (raft → plume → spread; level drops when drunk).
7. Any property shown as proof (dissolves, quiet, waterproof) is filmed for real or supered "Dramatization", and a dramatized property is not presented as proof.
8. Paid cut is set to 18+ and reads adult.

## Sources

URLs are inline. Measured files and metadata: `scratchpad/niche/supplements/vids/*.info.json`; analysis (cuts, RMS, beat score, 2 fps tiles) in `scratchpad/niche/supplements/an/`, produced with `scratchpad/niche/tools/an.sh` (same method as 47). Media is not committed.
