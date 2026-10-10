# 48 — Niche deep-dive: fashion, sneakers, watches and jewelry

Research brief, 2026-10-09. No generation money was spent. Nobody was contacted.

**What this adds.** Doc `11-niche-fashion-luxury.md` already covers the visual grammar of watches, sneakers, leather and eyewear: shot types, light, the style header, the FTC Jewelry Guides basics and the dial-morph workarounds. This doc does not repeat that. It adds:
- teardowns of 12 real ads plus 2 reference classics, built from 17 TikToks we downloaded and measured;
- conversion data for the niche;
- a realism-pitfall table mapped to doc 43's model rules;
- policy and legal rules beyond the Jewelry Guides;
- a buyer profile;
- 8 ready concepts with shot lists, physics checks, audio maps and costs.

**Tags.**
- `[measured]`: we downloaded the file and measured it with ffmpeg (scene cuts at threshold 0.30, audio RMS in 0.5 s windows, 2 fps frame tiles we looked at).
- `[unverified]`: we found no primary source.
- `[inf]`: our own inference.
- `[vendor]`: the number comes from a company that sells the thing measured.

**Method and limits.**
- **YouTube:** yt-dlp downloads were blocked ("Sign in to confirm you're not a bot"). YouTube search still worked, so YouTube items below are metadata only.
- **TikTok:** downloads worked. We pulled 17 public TikToks to `scratchpad/niche/fashion/`, outside the repo. No media is committed.
- **View counts:** these are the yt-dlp metadata snapshot of 2026-10-09.
- **Like rate:** likes ÷ views.
- **Purchase data:** none of these ads publishes CPA. Where purchase data exists, it comes from TikTok or Northbeam case studies.

---

## 0. The 8 findings that matter most

1. **In this niche the winning ads are proof stunts or people, not beauty shots.** Our two highest-reach brand-adjacent items:
   - a sponsored creator's Pandora "surprise" story: 2.5M views;
   - Kallmekris's Vessi sketch: 807K views. As a Spark Ad it cut cost per purchase by 59% ([TikTok case](https://ads.tiktok.com/business/en/inspiration/vessi-354)).

   Pandora's own polished lab-grown film from the same period got **34K views and a 1.2% like rate** `[measured]`. Polish alone is the weakest position in the niche.
2. **The best AI-native format here is the forced-perspective or FOOH stunt, and it works because one real hand anchors it.**
   - Jacquemus giant bags: 15.4M views, 11% like rate, 7.9 s, **zero cuts**.
   - Foot Locker EU Salomon "split": 281K views, **zero cuts**. A real hand "picks up" a building-sized shoe at 0.5 s.

   Both are single takes with a locked or handheld real-world camera `[measured]`.
3. **AI humans are the niche's landmine.** Four documented backlashes in 12 months:
   - Skechers in Vogue, Dec 2024;
   - Guess in Vogue, Aug 2025 (a 2M+ view TikTok callout);
   - J.Crew × Vans, Aug 2025;
   - Valentino DeVain, late 2025, which drew backlash even with an AI label.

   Rule: **AI builds the world and the stunt. The product and the skin are real or reference-locked. Faces are averted, or are licensed real talent.**
4. **Comedy that turns on the price or the product beats product beauty on engagement.** Foot Locker staff skits ran at a **6.4–8.5% like rate**. The product-caused punchline ("that'll actually be $160") lands in the last 2 s `[measured]`. Foot Locker's straight unboxing with the same staff and set got **1.8%**.
5. **Proof demos are the jewelry conversion engine.** Two examples:
   - Ring Concierge's hammer "stone smashing" test: 174K views, 5% like rate, 32 cuts in 64 s.
   - Gold-filled vs plated "three days in water", side by side: 13.7 s, 9 cuts.

   But the claims in them are legally loaded (§4): moissanite, vermeil, "tarnish-proof".
6. **The meta-data says that in fashion, editorial and product shots still survive, and video is a minority.** Benly Q1 2026, luxury fashion:
   - Product Shot effectiveness 67, Lifestyle/Editorial 64, UGC 40;
   - only **25.5% of creatives are video**;
   - median creative life is **19 days**.

   In sportswear, Lifestyle/Editorial scores 77 and UGC has the highest top-performance rate, 63.6% ([Benly](https://benly.ai/benchmarks/q1-2026/fashion-apparel/sportswear)) `[vendor]`. For VXO this means each film must explode into 6–10 stills and cutdowns, because the creative dies in about 3 weeks.
7. **Motion's 2026 fashion top-10 by hit rate is native and meme-like.** In rank order: Post-it, Quiz, Stylized product shot, Meme, ASMR, Product shot, Social comment, Podcast, Product showcase, Unconventional text placement ([Motion](https://motionapp.com/library/research/creative-benchmarks-2026/visual-formats-by-vertical)). "Stylized product shot" is the slot VXO's AI films fit. Wrap it in a native frame such as a text overlay, a comment reply or a meme setup.
8. **Watches and jewelry fail in AI on text, counts and metal reflections, not on motion.** The fix is doc 43's split: Kling 3.0 Pro i2v for any frame that shows a dial, stone or logo, and Seedance 2.5 r2v only for the stunt and the world.

---

## 1. Teardowns: 12 ads from the last 2 years (plus 2 reference classics)

`[measured]` = downloaded. Cut rate = (cuts + 1) ÷ duration.

### 1.1 Measured (TikTok)

| # | Ad | Date · views · like rate | Length · cuts · shots/s | Second 1 (hook) | Turn / punchline | Sound | CTA | Why it sold |
|---|---|---|---|---|---|---|---|---|
| T1 | **Foot Locker EU × Salomon XT-6 "splits the difference"** ([link](https://www.tiktok.com/@footlockereu/video/7542807258346835233)) | 2025-08-26 · 281K · 1.2% | 18.9 s · **0 cuts** · one take | A **building-sized** black shoe sits in front of the Royal Exchange, London. A real arm enters and "pinches" it at 0.5 s (forced perspective) | The shoe splits in half. One half is a trail diorama (moss, forest, tiny runner), the other a street diorama (graffiti, "Foot Locker" storefront). It is put back down, and the giant shoe returns in the plaza with a pedestrian walking past | Rhythmic loops, RMS swinging −11 to −24 dB every ~2.5 s. The beat paces the reveals | Speech bubble "Split it open, what's inside?" | Product truth (trail + street hybrid) made literal. One take = believable. **The product is the joke** |
| T2 | **Foot Locker "results may vary" (MB.05)** ([link](https://www.tiktok.com/@footlocker/video/7542899661498027319)) | 2025-08-26 · 169K · **6.4%** | 21.4 s · 8 cuts · 0.42 | Customer holding a pink box: "Hey, how much are these?" Captioned dialogue from frame 1 | "$130… but we have a discount for good-looking people." Second customer: "Oh perfect! How much is it?" Staff group-hug the first customer, then: "**That'll actually be $160**" | Dialogue + room tone | Drop date in caption | Price-anchor joke (Motion: price-anchor hooks hit 10.89%, doc 45 D5). Staff in referee "Striper" uniforms = recurring cast |
| T3 | **Foot Locker "not again" (Ja 3 Showstopper)** ([link](https://www.tiktok.com/@footlocker/video/7558849055095328014)) | 2025-10-08 · 225K · **8.5%** | 6.25 s · 3 cuts · 0.64 | A Striper is mid-dance, already leaning as if hit by wind | Caption "go where the wind takes you". He is blown through the stockroom to the exact box | Trending sound | Release date in caption | 6 s loop, a meme template, and the product at the end of the gust |
| T4 | **Foot Locker AJ1 "Voodoo" unbox** ([link](https://www.tiktok.com/@footlocker/video/7566371301154163982)) | 2025-10-28 · 20K · 1.8% | 17.8 s · 7 cuts · 0.45 | Box lid opening (hands only) | None. Turns, lace, heel | Music −25 to −33 dB, quiet | "Dropping tomorrow" | Control case: same brand, no joke → 1/10th the reach |
| T5 | **Pandora LGD, creator @bruontheradio (#PandoraPartner)** ([link](https://www.tiktok.com/@bruontheradio/video/7440646273868549422)) | 2024-11-24 · **2.5M** · 1.6% | 43.5 s · 17 cuts (none in the first 12 s) | Selfie in a car, talking fast: the plan to surprise his partner | Store montage (0.8 s cuts from 12–23 s), bag reveal at home, "Anna-versary" caption. Payoff: her hand with the bracelet | VO-led, RMS steady −20 dB | Brand bag on screen 3× | A story with a reaction; the product appears in the last third. Gifting is the purchase driver (doc 11) |
| T6 | **Pandora brand: "All eyes on Pandora Lab-Grown Diamonds"** ([link](https://www.tiktok.com/@theofficialpandora/video/7488731102723591446)) | 2025-04-02 · 34K · 1.2% | 17.4 s · 1 cut | A slow arc along a wall of wheat-paste posters (BE LOVE) | None. End card "Pandora Lab-Grown Diamonds" on pink | Flat music, −28 to −31 dB, no events | End card | Control: a beauty OOH document with no event in the first second |
| T7 | **Kallmekris × Vessi (Spark Ad creative)** ([link](https://www.tiktok.com/@kallmekris/video/7440165965825936696)) | 2024-11-22 · 807K · **8.6%** | 69.4 s · 28 cuts · 0.42 | A character entrance (hair flip, mid-motion) | A multi-character sketch, all played by one creator. The shoe insert sits at ~10 s on a doormat. A wet weather payoff | Dialogue, RMS jumps −45 → −18 dB at beat changes | Caption link | TikTok's case: **ROAS 2×+, cost per purchase −59%, CPC −38%** vs prior ads ([TikTok](https://ads.tiktok.com/business/en/inspiration/vessi-354)). Creator control + Spark Ads |
| T8 | **@veronicagayleu × Vessi waterproof test** ([link](https://www.tiktok.com/@veronicagayleu/video/7468049779977669893)) | 2025-02-05 · 30K · 0.7% | 31.9 s · 16 cuts | White shoes held up: "Vessi waterproof test" super | POV feet stomping in puddles, rainy seawall, "it's the driest thing on me right now" | Talk + rain | #VessiAmbassador | The standard demo works but plateaus without a character or a twist |
| T9 | **Ring Concierge "Stone smashing with RC"** ([link](https://www.tiktok.com/@ringconcierge/video/7398220303958150431)) | 2024-08-01 · 174K · 5.0% | 63.6 s · **32 cuts** (6 in the first 3 s) | Staff squealing at a phone, then a black card "STONE SMASHING WITH RC *do not try this at home" | Hammer blows on concrete. CZ and moissanite vs diamond, labelled BEFORE/AFTER with tweezers | Shrieks, impact transients (RMS dips to −48 dB between hits) | None (organic) | Destruction proof plus office characters. **Legal note:** a diamond is hard but brittle (it can cleave). A "diamonds survive hammers" implication is a claim `[inf]` |
| T10 | **SimplySunshine gold-filled vs "fashion brand" in water** ([link](https://www.tiktok.com/@simplysunshinejewelry/video/7188534844282965290)) | 2023-01-14 (older control) · 23K | 13.7 s · 9 cuts · 0.73 | Two glasses, "both sat in water for three days" super | The competitor's water is rust-brown, ours is clear | Loud ASMR pours (−8 dB) | "Our brand" label | Side-by-side proof in 2 s. Names a competitor = comparative-ad risk |
| T11 | **Swatch MoonSwatch 1965** ([link](https://www.tiktok.com/@swatch/video/7475864905078328608)) | 2025-02-26 · 57K · 2.5% | 22.6 s · 3 hard cuts (many dissolves) | A hand-drawn "1" then "1965" on white | Dial macros, then the watch on a grey sweep, then "OMEGA × swatch 1965" | Silence for 2.5 s, then music at −11 dB | Store availability | Pure CGI product film. Works for a hype brand with demand already in place; weak engagement otherwise |
| T12 | **Swatch Mission to Earthphase** ([link](https://www.tiktok.com/@swatch/video/7431336896720047392)) | 2024-10-29 · 134K · 3.8% | 49 s · 6 cuts | A real moon through trees (live action), match-cut to a CG moon | Earthrise on a lunar horizon → dial with earth phase → lume glow in the dark | Ambient, then a drop to −8 dB at 9 s | Store date | "World → dial" match cut, and **lume-in-the-dark as the closing punch** |

**Reference classics (older than 2 years, still the template):**
- **Jacquemus "Giant Bambino bags"** ([link](https://www.tiktok.com/@jacquemus/video/7218514305401031941)): 2023-04-05, **15.4M** views, 11% like rate. 7.9 s, 0 cuts. Handheld street POV. Giant bags roll down the Opéra Garnier street like buses; "BAMBINO" is painted in the lane. A CGI, not AI, piece by Ian Padgham. A year later the brand built them physically ([link](https://www.tiktok.com/@thefashionnetwork/video/7353986995690982689)).
- **Valentino DeVain "Digital Creative Project"** (YouTube [hgIe0txXD94](https://www.youtube.com/watch?v=hgIe0txXD94), 28 s, 11K views; metadata only, download blocked). The logo morphs into arms, then a mass of bodies. It drew "cheap", "lazy" and "disturbing" comments even with an AI label ([BBC via AOL](https://www.aol.com/news/fashion-house-valentino-criticised-over-082605233.html), [Yahoo](https://www.yahoo.com/entertainment/articles/valentino-trashed-tacky-lazy-ai-185952693.html)). **The anti-pattern: morphing bodies and logos read as slop in luxury.**

### 1.2 Metadata-only (YouTube; download blocked)

| Ad | Length · views | Note |
|---|---|---|
| Vessi "But Are They REALLY Waterproof?" (MgtU9xfJFcI) | 82 s · **11.8M** | Long-running demo explainer. Matches doc 45 D29: >30 s speech-led explainers survive |
| Vessi "More Than Waterproof" (VozXiV4DPq4) | 21 s · 738K | Short cut of the same claim |
| Brilliant Earth "Jane Goodall Collection" (nHAwx5Ap8u8) | 61 s · 2.2M | A cause + celebrity collection film |
| Zales Holiday 2025 "Wear Your Wishlist" (Yr0C-u8UcDM) | 31 s · 3.9M | Paid TV/YouTube gifting spot |
| On "Roger vs Zendaya" (C36-bDnDDqg) | 71 s · 2.4M | Celebrity comedy sport |
| Seiko Prospex "The Watch perspective" (qx9pT52BaWQ) | 16 s · 331K | POV-of-the-watch device |
| Nike "So Win" Super Bowl 2025 (W2VLEmzPC1U) | 60 s | Brand manifesto, out of DTC scale |
| "Nike's AI-Powered Commercial" spec (RFGfkOLGsEM) | 41 s · 257K | Creator AI spec: Veo 2 + Kling + Suno. Reach comes from creator/AI curiosity, not purchase |

### 1.3 What the measured set says `[measured]`

- **Cut rate splits by format, not by quality.**
  - Stunt/FOOH: 0 cuts (T1, Jacquemus).
  - Skits/stories: 0.4–0.5 shots/s (T2, T5, T7, T9).
  - Proof side-by-side: 0.7 shots/s (T10).
  - Brand beauty films: 0.1–0.2 shots/s (T6, T11, T12).

  This matches doc 41: a sensory or stunt film is one take, a story is coverage.
- **The first second always has an event or a voice.** Every item above a 4% like rate opens with motion already under way (T3 dance, T7 hair flip), a spoken question (T2) or a forced-perspective grab (T1, at 0.5 s). Both brand films that open on a static or slow move sit at 1.2–2.5%.
- **The product appears late in the winners.** The Pandora creator reveal comes at 12 s+, the Vessi shoe at ~10 s, the Foot Locker price punchline at 19 s. This contradicts the "brand in the first 5 s" rule (doc 45 D13) for *organic/Spark* reach `[inf]`. For a *paid* 15 s VXO film, keep the product in the hook. Put the product's *consequence* (the punchline) late.
- **Silence before the drop.** Swatch 1965 uses 2.5 s near-silence (−33 dB) and then −11 dB. Earthphase drops at 9 s. Same device as doc 11: "0.5 s silence before the logo".

---

## 2. What actually converts in this niche (data)

| # | Finding | Number | Source | Status |
|---|---|---|---|---|
| F1 | Fashion & Apparel top formats by hit rate (rank) | Post-it, Quiz, **Stylized product shot**, Meme, ASMR, Product shot, Social comment, Podcast, Product showcase, Unconventional text placement | [Motion 2026 vertical page](https://motionapp.com/library/research/creative-benchmarks-2026/visual-formats-by-vertical) (Sep 2025–Jan 2026; cells with <50 accounts suppressed) | Read; ranks only, no % |
| F2 | Fashion top formats by **spend share** | Podcast, Unconventional text, **Billboard**, Text message, Sign, Celebrity, Slideshow, Post-it, Offer-first banner, **Demo** | same | Read. "Billboard" here is the FOOH/OOH slot `[inf]` |
| F3 | Luxury fashion effectiveness by asset type | **Product Shot 67**, Lifestyle/Editorial 64, UGC 40, Branded/Studio 39, Graphic 27 | [Benly Q1 2026 luxury](https://benly.ai/benchmarks/q1-2026/fashion-apparel/luxury-fashion), 11.7K creatives, 74 brands | `[vendor]`; a composite score, not KPIs |
| F4 | Luxury fashion creative life | median **19 d**; 27% survive 30 d; 9.1% survive 60 d; 0% survive 90 d | same | `[vendor]` |
| F5 | Luxury fashion video share | **25.5%** video vs 41.4% cross-industry | same | `[vendor]` |
| F6 | Luxury hook mix (video) | Visual Intrigue 81.7%; "Demonstration" ~0% share but survives **2.1×** longer | same | `[vendor]`. The gap is an opening |
| F7 | Luxury promo intent, Jan→Mar 2026 | Discount 69% → 42%; New Launch 19% → 46% | same | `[vendor]` |
| F8 | Sportswear effectiveness | **Lifestyle/Editorial 77**, UGC 65, Studio 60, Product Shot 43; UGC top-performance rate **63.6%** | [Benly sportswear](https://benly.ai/benchmarks/q1-2026/fashion-apparel/sportswear), ~11K creatives | `[vendor]` |
| F9 | Sportswear life | median 23 d; 36.4% survive 30 d | same | `[vendor]` |
| F10 | Vessi × creator Spark Ad | ROAS 2×+, CPP −59%, CPC −38% | [TikTok case](https://ads.tiktok.com/business/en/inspiration/vessi-354) | Platform-reported |
| F11 | Vessi video vs baseline (Meta) | CAC −42%, ROAS +61% | [Northbeam](https://www.northbeam.io/post/creative-iteration-and-optimization-at-vessi-through-trustworth-first-party-metrics) (doc 45 D25) | `[vendor]` |
| F12 | CREA Jewelry: Spark Ads (boosted organic) vs standard in-feed | CVR +44%, CPA −26%, conversions +35.8% | [TikTok case](https://ads.tiktok.com/business/en/inspiration/crea-jewelry) | Platform-reported |
| F13 | Meta overall 2025 | CPA $38.19, CPM $14.19, CTR 2.19%, CVR 1.6%, ROAS 1.86, AOV $71.69 | [Triple Whale](https://triplewhale.com/blog/facebook-ads-benchmarks), ~35K brands | Search snippet; full page 403 |
| F14 | Apparel & Accessories CAC up **45% since 2023** | — | [Triple Whale apparel report](https://www.triplewhale.com/reports-guides/fashion-industry-benchmarks-2025) | Snippet only; page 403 `[unverified]` |
| F15 | UGC gallery on PDP: median CVR lift 18%; fashion **24%** | 500+ brands, self-selected | [Idukki](https://idukki.io/blog/ugc-conversion-rate-boost) | `[vendor]`; PDP galleries, not ads |
| F16 | Watch microbrands: drops sell out in minutes (Studio Underd0g "6,000 watches in nine hours") | — | [The Hour Markers](https://www.thehourmarkers.com/articles/studio-underd0g-watches-and-why-they-are-hyped) | One outlet `[unverified]` |
| F17 | Vogue Business Watch Index (Sep 2024–Aug 2025): brands that moved to short-form video improved their standing | qualitative | via [Vogue](https://www.vogue.com/article/how-to-market-watches-in-the-digital-era) (search snippet) | `[unverified]` |

### 2.1 What this means, by sub-niche `[inf]`

| Sub-niche | Format that converts | Claim/proof that converts | Length | Placement |
|---|---|---|---|---|
| **Demi-fine jewelry** (vermeil, gold-filled, $40–250) | Creator gifting/reaction story (T5) + side-by-side proof (T10) + "stylized product shot" ASMR macro | Water/sweat/tarnish proof, price vs "solid gold" | 15 s paid; 30–45 s Spark | TikTok Spark, Reels, Meta Advantage+ catalog plus one video |
| **Fine/lab-grown** ($800–10K) | Founder or staff expert + destruction/loupe proof (T9) + gift story | Certification (IGI/GIA), price per carat vs mined, the 4Cs | 20–40 s | Meta, YouTube, Pinterest. Long consideration, so retargeting matters |
| **Watch microbrands** ($300–1,500) | Drop film (hype) + macro product poem (T11/T12) + creator review | Specs: movement, WR metres, sapphire, lume. "Sold out last time" scarcity (only if true) | 15–30 s; 6 s teaser | Instagram, YouTube Shorts, watch forums, email |
| **Sneakers/footwear DTC** | Creator sketch with the shoe as payoff (T7) + demo (waterproof, weight, comfort) + FOOH stunt (T1) | One measurable property: waterproof, grams, cushioning | 15–30 s paid; up to 70 s Spark | TikTok Spark first, Meta second |
| **Apparel basics** (merino, cashmere, denim) | Try-on/fit, "worn X days" proof, price vs luxury equivalent | Fiber content, a durability test | 15–20 s | Meta, with product shots as statics alongside |

**VXO positioning in one line `[inf]`:** in this niche VXO should sell the **stunt or proof film + the stills pack**, not the "luxury mood film". Mood films are what the brands' own photographers make, and the data says they plateau (T6, T11).

---

## 3. AI realism pitfalls for this niche, and the fixes

Builds on doc 43 §5 (failure → fix) and doc 11 §1 (5)–(6). Model choice per row follows doc 43 §1:
- **Kling 3.0 Pro i2v:** inserts where text, logos or counts must hold.
- **Cinema Studio 4.0:** one-take hero moves.
- **Seedance 2.5 r2v:** multi-shot stories, stunts and worlds.

| Material / subject | How AI fails (seen in the field) | Fix (prompt + reference + pipeline) |
|---|---|---|
| **Dial text, indices, logos** | Letters swim; numerals multiply; the brand name morphs. Real logos leak in (doc 11: the community divewatch leaked a real logo) | (a) Design a **wordless dial** and comp the wordmark in post on a tracked plate. (b) Kling i2v, `last_image_url` = same still, 5 s, `cfg_scale` 0.5. (c) Use the first 3 s only. (d) Write: "dial, hands and indices are a fixed printed surface; only light moves" |
| **Watch hands** | Hands spin at random speeds; the second hand goes backwards; 10:10 drifts | Freeze the hour and minute hands at **10:10** in the still. Let the seconds hand move only in one shot. Mechanical = smooth sweep, 8 beats/s; quartz = 1 tick/s. Write which. If it fails, comp the seconds hand in post (rotate a PNG at 6°/s) |
| **Polished metal (steel case, gold)** | Reflections show a studio, a camera or nothing (flat grey CG). Gold goes orange-plastic | "Reflections show only one large white diffusion card and a black flag; no camera, no crew, no windows." Name the alloy: "warm 14k yellow gold, slightly pink-orange in shadow, pale in highlights" |
| **Faceted stones / pavé** | Stone count drifts. Pavé melts into glitter. "Sparkle" becomes a CG star cloud | Solitaire or bezel set only. Write the count: "exactly one 1.0 ct oval stone, four claw prongs". Sparkle = a post star PNG on 1–3 highlights with an 8-frame fade (doc 11). Never prompt "sparkle" |
| **Chains** | Float; fuse into skin; links merge; the clasp is a blob | "The chain hangs straight and heavy, links separate, rests in the suprasternal notch, moves 3–5 frames behind the body." Keep the clasp out of frame, or use a **real macro photo** of the clasp as the start frame |
| **Earrings** | Mismatched pair; extra earrings; hoops pass through the jaw | One ear only, in profile. "Exactly one hoop per earlobe; the hoop swings on its post as a pendulum, never passes through skin" |
| **Rings on fingers** | 6 fingers; the band clips into the finger; the ring changes fingers | Hands from a real reference photo (Soul Cinema still → Flare comp of the ring). Write: "ring on the left ring finger, band partly hidden under skin compression". Lock with Kling start=end frames |
| **Bracelets / watches on wrists** | The strap fuses with skin; the buckle side flips; the watch jumps wrists | "Watch on the LEFT wrist, crown facing the hand, case 2 cm above the wrist bone, strap casts a soft shadow on skin." One wrist per shot |
| **Sneaker geometry** | Panel count, lace count, eyelet count and sole tread change per shot; the colourway shifts; a swoosh-like mark appears | Reference sheet with side, three-quarter, top and sole views on grey (doc 43 §3). "Exactly 6 eyelets per side, lace ends tipped in black, tread is a hex pattern." Negative: "no logos, no stripes, no swoosh". Grade lock: name the hex colour, and match in post with a LUT from the real product photo |
| **Footfall** | Feet slide; soles hover; there is no compression; puddle splashes are backwards | Doc 43 rule 11, start/end positions: "heel strikes first, sole flattens 3 mm, toe pushes off; foot does not slide." For splashes: "water sheets outward from the heel, then falls back with gravity, droplets bead on the knit and roll off" |
| **Water on fabric/knit** | A waterproof shoe darkens as if soaked (fails the claim); or it looks glassy-CG | "Water beads into round droplets on the upper and rolls off; the knit colour does **not** darken; inside stays dry." **Show the dry-sock reveal with a real photo insert.** It is the proof, and it must not be AI-faked (FTC §4) |
| **Fabric drape (tees, knit, cashmere)** | Garments re-tailor between shots; the knit pattern moirés; fabric behaves like rubber | One garment reference per shot. "Fine-gauge merino jersey, matte, soft drape, creases at the elbow." Avoid tight knit patterns in wide shots; use 85 mm crops |
| **Skin (wrist, neck, collarbone)** | Plastic skin; no pores; a waxy neck. Most viewers flag this first (Guess / J.Crew backlash) | Soul Cinema still with "unretouched skin, fine vellus hair, a freckle, slight redness at knuckles". Never a full AI face as brand talent. Faces averted or cropped (doc 11's cross-niche law) |
| **Mirrors / shop glass** | Reflections disagree with the scene; the camera appears | Avoid mirrors. If unavoidable: "the mirror reflects the room behind camera as a soft blur; no camera visible" |
| **Price tags, size labels, shop signage** | Gibberish text | Clean the plate (doc 43 rule 5). All on-screen text goes in post |
| **Forced perspective / giant product (FOOH)** | Scale breaks: the giant product has no contact shadow, the perspective lines don't converge, the passers-by are wrong size | Plate shot with a real horizon. "Giant shoe 9 m long, resting on the paving, contact shadow and slight ambient occlusion, pedestrians 1.7 m tall walk behind it at correct scale." The real hand in the foreground does the scale handoff (T1). In AI, make the hand a **separate Kling i2v shot** from a real hand photo |
| **Lume (glow in dark)** | Glows in daylight; the colour shifts | "Lume glows green-blue only in the dark shot; in daylight the indices are matte off-white." Do the dark shot as a separate i2v from a dark still |
| **Underwater watch** | Bubbles inside the crystal; the dial distorts; there are no caustics | "Water outside the sapphire only; a few bubbles cling to the bezel edge; caustic light ripples cross the case; the dial stays sharp and dry behind the crystal." Seedance 2.5 720p, 5 s (doc 11 BIG IDEA) |

**Pipeline rule for this niche `[inf]` from doc 43 §1 + T1/Jacquemus:**
- Any shot where **text or count is visible** = Kling i2v from a Flare still made with the product reference.
- Any shot with **people moving or the world reacting** = Seedance 2.5 r2v with the product as `@image1`, and the product kept **small or moving fast** in frame.
- Finish with the **real product photo** as the end card. The doc 45 "AI disclosure" stance applies.

---

## 4. Ad policy and legal constraints

Doc 11 §1 (2) already covers the FTC Jewelry Guides (karat, plated, vermeil, lab-grown) and watch terms ("water-resistant to X m", ISO 6425 "diver's", "chronometer", "Swiss Made"). Additions:

| Area | Rule | What it means for a VXO film |
|---|---|---|
| **Fake testimonials incl. AI** | FTC Rule on Consumer Reviews & Testimonials, 16 CFR 465, effective **2024-10-21**. It bans reviews and testimonials by people who don't exist or lacked real experience, **including AI-generated ones**. Civil penalties ($51,744 per violation in 2024, inflation-adjusted) ([FTC](https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials), [Hunton](https://hunton.com/hunton-retail-law-resource/ftc-issues-final-rule-targeting-fake-consumer-reviews-and-testimonials-including-those-generated-by-artificial-intelligence-ai-and-online-bots)) | **Never generate an AI "customer" saying "I love these, they never tarnish".** Characters may act; they may not testify. Quotes on screen must come from real verified reviews |
| **Demonstrations** | FTC deception policy: a demo must show what the product really does. No mock-ups presented as real tests `[inf from FTC Act §5 case history]` | Waterproof, tarnish, hammer and scratch tests shown as **proof** must be filmed for real, or clearly framed as a dramatization ("Dramatization. Real test results at …"). AI may stage the comedy around a real test insert |
| **Endorsements** | FTC Endorsement Guides, 16 CFR 255 (2023 revision). Clear "#ad / Paid partnership" | Applies when the brand boosts creator posts (T5, T7) |
| **Pricing** | FTC Guides Against Deceptive Pricing, 16 CFR 233. "Compare at" must be a real prevailing price | Price-punchline comedy (T2 style) is fine. "Worth $2,000, ours $200" needs substantiation |
| **Scarcity** | Fake countdowns / fake "sold out" = deception (doc 11; FTC dark-patterns staff report 2022) | "Drop sold out in 9 minutes last time" only if true and documented |
| **Made in USA** | FTC Made in USA Labeling Rule, 16 CFR 323 (2021): "all or virtually all" | Common in boots, denim, jewelry. Check before writing it in a super |
| **Textiles / wool / cashmere** | Textile Fiber Products Identification Act; Wool Products Labeling Act (cashmere has a statutory definition: fine dehaired undercoat, avg ≤19 µm) | "100% merino", "cashmere" and "recycled" claims must match the label |
| **Green claims** | FTC Green Guides, 16 CFR 260. "Sustainable" is not substantiable unqualified; "recycled" needs a % | Sneaker/apparel DTC loves "eco". Qualify it, or leave it out of the film |
| **Lead / cadmium in jewelry** | CPSIA: children's products ≤100 ppm lead. California H&S Code §25214.1–.4 (lead in jewelry) and Prop 65 warnings | Never cast children wearing adult fashion jewelry unless the brand confirms CPSIA compliance |
| **Counterfeit / look-alike** | Meta: no ads for counterfeits, knock-offs or replicas, or ads likely to confuse about source ([Meta](https://transparency.meta.com/en-gb/policies/ad-standards/intellectual-property-infringement/copyright-and-trademarks/)). TikTok: no replicas or imitations; no unauthorized third-party names or logos ([TikTok](https://ads.tiktok.com/help/article/tiktok-ads-policy-intellectual-property-infringement)) | No "dupe of [brand]" framing. No Tank-style, Royal Oak-style or swoosh-like shapes (doc 11 trade-dress list). Screen every AI frame for leaked marks |
| **Comparative ads** | Lanham Act §43(a): false comparative claims are actionable | T10-style "fashion brand vs our brand" is OK only with a truthful, documented test. Don't name or show a real competitor |
| **AI disclosure** | Meta "AI info" label for photoreal people/events; TikTok requires an AIGC label (doc 45 §5.3) | Label it. And design so the label doesn't hurt (finding 3): real product, averted faces, the stunt clearly a stunt |
| **Age gates** | None for fashion/jewelry on Meta/TikTok `[inf]`. Note: TikTok ads to under-18s are restricted for some categories, and Meta ad targeting for teens is limited to age/location | Keep casting visibly 21+ for anything with nightlife or alcohol (party concepts) |
| **Weapons / violence** | Doc 45 §5.1 | The hammer test is fine (a tool). Avoid knives in a "cut-resistant" demo framed as violence |

---

## 5. The buyer

### 5.1 Who signs a $1,200–3,500 film

| Brand size (annual revenue) | Signer | How they buy `[inf]` |
|---|---|---|
| <$3M | **Founder/designer** (often the face of the brand) | Pays by card; decides in 1–2 calls; wants the 5 free frames on *their* SKU |
| $3–20M | **Head of Growth / Performance marketing lead**, with the founder approving creative | Buys "creative volume for testing". Asks about variants, hooks and cutdowns, and how many ads they get |
| $20–75M | **Brand/Creative Director** (brand film) or **Growth lead** (ads), budgeted | Wants an SOW, usage rights, revisions and a timeline. A Season retainer fits here |

### 5.2 What they fear (ranked) `[inf]`, with evidence

1. **"It will look like AI slop and cheapen the brand."** Valentino, Guess, J.Crew and Skechers all took public hits (§0 finding 3). Luxury and fine jewelry buyers are the most sensitive.
2. **"The product will be wrong."** Wrong stone count, wrong colourway, an extra eyelet → returns and complaints. Jewelry buyers are visual and skeptical ([BrandIgnity](https://www.brandignity.com/?p=36193) `[vendor]`).
3. **"It won't beat our UGC."** Their own creator ads may be winning (T5, T7, F10, F12).
4. **"Legal/compliance."** Vermeil/lab-grown disclosures; FTC fake-review rule; marketplace rejection for "replica" look-alikes.
5. **"One film dies in 3 weeks."** The median luxury creative lives 19 days (F4).
6. **"Comments will say 'AI' and derail."** AI disclosure is required anyway.

### 5.3 What proof they need

- **Fidelity side-by-side:** their product photo next to our frame, macro crop, with the count (stones, eyelets, links) annotated.
- **5 free frames on their actual SKU,** including one macro with a visible text element (dial, stamp, tag) that holds.
- **Before-you-pay plan:** a 480p blocking test, then 720p.
- **The format menu matched to data:** one hero film + 3 hook variants + 6 s cutdown + 4:5/1:1/9:16 + 6–10 stills. This answers fear 5.
- **The "real product closes the film" rule** and an AI-label plan. This answers fears 1 and 6.
- **A test plan:** run as Spark/partnership-style placements alongside their UGC, and judge on hook rate and CPA (doc 45 benchmarks: hook rate 25.44% Meta avg).
- **Price anchor:** an equivalent live-action jewelry macro + talent shoot typically runs well above $5K `[unverified]`; VXO Short is $1,200.

### 5.4 Twenty example brand types (no outreach)

1. Demi-fine gold vermeil jewelry DTC ("waterproof/shower-proof")
2. Lab-grown diamond engagement and fine jewelry DTC
3. Gold-filled permanent-style chains and anklets
4. Personalized name/initial/birthstone necklaces
5. Freshwater pearl jewelry DTC
6. Men's stainless chains, rings and cuffs
7. Signet ring and heirloom-style DTC
8. Mechanical watch microbrand (dive)
9. Mechanical watch microbrand (field/dress, sub-$600)
10. Watch straps and accessories (rubber, NATO, leather)
11. Waterproof knit sneakers
12. Recycled/sustainable sneakers
13. Minimalist leather sneakers
14. Skate shoes DTC
15. Barefoot/minimal running shoes
16. Recovery slides and clogs
17. Merino performance basics (travel tees, "wear 7 days")
18. Cashmere DTC at accessible prices
19. Premium denim DTC (fit-led)
20. Socks/underwear with a performance claim (moisture, odor)

---

## 6. Eight ready film concepts (invented brands)

Conventions:
- **Formats:** 9:16 master; 4:5 and 1:1 reframes; 6 s cutdown.
- **Physics:** each concept passes doc 41 §2 and doc 44's "could a crew rig this?" read.
- **Costs** are list prices from doc 43 §6 [EST]:
  - Seedance 2.5 r2v: $2.06 / $4.62 per 10 s at 480p / 720p;
  - Kling 3.0 Pro i2v, sound off: $0.95 per 10 s (**$0.48 per 5 s insert**);
  - Cinema Studio 4.0 720p: $4.62 per 10 s;
  - stills (Flare / Soul Cinema): ~$0.30 each (doc 11);
  - takes per doc 43: ×3 for action, ×1–2 for inserts.
- **Brand names** are invented. Clear them on USPTO before use (doc 11).
- **Claims shown as proof** must be filmed for real, or supered as dramatization (§4). Each concept marks its "real insert".

### C1 · HALDEN 200 (dive watch) — "On Time" (20 s)

- **Idea:** a man in a suit takes a deliberate backward fall into a hotel pool. Underwater, calm, he checks the time. His phone sinks past him, dark. He surfaces, walks dripping into a boardroom, and the wall clock and his dial both read **10:10**. Everyone else is late.
- **Hook (0–1 s):** the splash. The camera is already underwater at the pool wall as his body breaks the surface: a white bubble column, the suit billowing.
- **Punchline (product-caused):** the watch is the only thing that kept working, so he's the only one on time. The 10:10 is a watch-ad in-joke the buyer will recognize.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Underwater housing, locked to the pool wall at 1.2 m depth, looking up: the body breaks the surface in a bubble column | Seedance. Stunt fall = backward, arms crossed (a real stunt move) |
| 2 | 1.5–4 | Underwater medium, a diver-operator 2 m away: he settles, suit jacket billowing, tie floating up | Hair and cloth lag (doc 43 §7.2) |
| 3 | 4–6.5 | Underwater insert, macro housing: wrist turns, dial at 10:09 → the seconds hand sweeping; caustics on the case | **Kling i2v** from a Flare still; wordless dial |
| 4 | 6.5–8.5 | Underwater medium: a black phone tumbles slowly past his face, screen dark | Object fate written: it rests on the pool floor |
| 5 | 8.5–10.5 | Above-water, poolside low angle: he surfaces, exhales, climbs the ladder | Water sheets off the suit; ladder contact |
| 6 | 10.5–13.5 | Corridor Steadicam, behind: he walks, dripping footprints on the stone floor | Real crew move |
| 7 | 13.5–16 | Boardroom wide, locked tripod: he sits, soaked; empty chairs; a wall clock at 10:10 | Clock face is a post comp |
| 8 | 16–18 | Wrist insert on the table, tabletop slider: the dial at 10:10, a droplet runs off the bezel | **Kling i2v**, `last_image_url` = same still |
| 9 | 18–20 | End card: real product photo, "HALDEN 200. Water-resistant to 200 m." | Real photo |

- **Physics check:**
  - Backward pool fall from standing is a standard stunt.
  - Suit fabric is buoyant at first, then sinks.
  - A dead phone sinks (dense).
  - Footprints fade as he walks.
  - No impossible camera: the underwater housing and Steadicam are standard.
  - **Claim:** "200 m" must match the spec. Say "water-resistant to 200 m", not "waterproof". "Diver's" only if ISO 6425.
- **Audio map:**
  - 0.0 s: muffled underwater splash plus bubble roar.
  - 1.5–8.5 s: underwater hum and a heartbeat-slow low drone. Mechanical tick at 8 beats/s (mixed in post) on shot 3.
  - 8.5 s: hard surface break, then pool echo.
  - 10.5–13.5 s: wet shoe squelch on stone.
  - 13.5 s: room tone, one throat clear.
  - 17.5 s: 0.5 s silence. Logo sting.
  - No VO, or one line: `[deadpan] On time.`
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v, 15 s, 6 shots (1, 2, 4, 5, 6, 7), template 7.2 adapted: 480p proof $3.09 + 720p ×3 $20.80 | $23.89 |
  | Kling inserts (shots 3, 8), ×2 each | $1.90 |
  | Stills, 8 | $2.40 |
  | **Total** | **≈ $28** |

### C2 · DRYLINE (waterproof knit sneaker) — "Footprints" (15 s)

- **Idea:** a flooded crosswalk at rush hour. Everyone hops around the giant puddle. One commuter walks straight through. At the office, the coworker leaves wet squelching prints on the carpet. He leaves **none**.
- **Hook (0–1 s):** ground-level 24 mm. A white knit shoe plants into ankle-deep water; a sheet of splash hits the lens.
- **Punchline (product-caused):** the clean, dry carpet behind him vs the trail of wet prints behind the coworker. Final beat: he takes one shoe off and the white sock is bone dry. **This is the real insert.**

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Ground rig on a sandbag at curb level, 24 mm: foot plants, splash sheets toward the lens | Seedance. "heel strikes, water sheets outward, droplets bead and roll off the knit; knit colour never darkens" |
| 2 | 1.5–3.5 | Wide from across the street, tripod: commuters leap and tiptoe around the puddle; he walks through the middle | Crowd at correct scale |
| 3 | 3.5–5 | Tracking dolly beside the foot at ankle height: water beads on the upper | **Kling i2v** from a real product photo + water |
| 4 | 5–7 | Office lobby, locked-off wide: two coworkers enter side by side | |
| 5 | 7–9.5 | Floor-level locked-off behind them, low on the carpet: the coworker's shoes leave dark wet prints; ours leave nothing | The punchline frame. Seedance, held |
| 6 | 9.5–11.5 | Medium: the coworker looks down at the trail, then at our guy. Deadpan | Faces OK if licensed or averted. Keep the coworker 3/4 back |
| 7 | 11.5–13.5 | Insert, desk height: the shoe comes off; a dry white sock | **Real footage/photo insert** = the proof |
| 8 | 13.5–15 | End card: the shoe on a grey sweep, "DRYLINE. Walk through it." | Real photo |

- **Physics check:**
  - Puddle depth ≈ 5 cm, so ankle splash is plausible.
  - Water must bead, not soak.
  - Wet prints fade over 3–4 steps.
  - The dry-sock proof is real.
  - **Claim:** "waterproof" requires a documented test (e.g. a submersion or flex test) `[inf]`.
- **Audio map:**
  - 0.0 s: hard splash transient + city traffic.
  - 1.5 s: crowd chatter, a bike bell.
  - 3.5 s: droplet ticks on knit (ASMR).
  - 5 s: lobby room tone.
  - 7 s: a "squelch, squelch" from the coworker, silence from ours.
  - 11.5 s: sock-fabric whisper.
  - 13 s: 0.5 s silence → logo knock.
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v, 15 s, 6 shots: proof $3.09 + ×3 $20.80 | $23.89 |
  | Kling insert (shot 3), ×2 | $0.95 |
  | Stills, 6 | $1.80 |
  | Real sock insert | brand-supplied phone footage |
  | **Total** | **≈ $27** |

### C3 · OBRA (gold vermeil hoops) — "Everything Else Aged" (15 s)

- **Idea:** a one-room apartment in fast "time-lapse". The bike rusts, the plant dies, the faucet crusts with limescale, the phone screen cracks. Through it all, the hoops on the bedside dish stay bright.
- **Hook (0–1 s):** macro. A single hoop drops into a glass of water: plink, rings in the water.
- **Punchline (product-caused):** she puts the hoops on and walks out. The only thing in the room that didn't age is on her.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Tabletop macro, 100 mm on a tripod: a hoop drops into a water glass, ripples | **Kling i2v** from a Flare still with the product reference |
| 2 | 1.5–4 | Locked-off wide of the room (camera on a wall bracket for "time-lapse" logic): light cycles day/night 3×, the plant wilts | Seedance. "time-lapse, camera never moves" |
| 3 | 4–6 | Same locked-off angle, closer: the bike chain rusts orange, then the tyre goes flat | |
| 4 | 6–8 | Insert at the sink: limescale crust grows on the faucet | Seedance or Kling |
| 5 | 8–10 | Insert at the bedside: a phone screen cracks on its own, dust settles, the hoops beside it in a ceramic dish stay bright gold | **Kling i2v**. Dust lands on the dish, not the hoops = the joke. Stays honest because it is clearly comedic, not a test |
| 6 | 10–12.5 | Medium, back of the head: a hand lifts the hoops and puts them on, one ear in profile | Soul Cinema still → Flare comp → Kling. One hoop per lobe |
| 7 | 12.5–15 | Doorway wide: she walks out. The room is dusty. End card "OBRA. 18k gold vermeil over sterling silver." | Vermeil disclosure in the super |

- **Physics check:**
  - Clearly a time-lapse gag: a locked camera, consistent light cycles.
  - The water ripple decays.
  - The hoop swings on its post.
  - **Claim:** do NOT super "never tarnishes". If the brand has a documented water/sweat test, add "Tested: 30 days of daily wear in water" `[inf]`.
  - Vermeil per 16 CFR 23.5 (sterling base, ≥10k gold, ≥2.5 µm; doc 11).
- **Audio map:**
  - 0.0 s: glass plink + water ring.
  - 1.5–10 s: a ticking clock speeding up, a time-lapse whoosh at each day cycle, a rust creak, a crack at 8.5 s.
  - 10 s: hush. Hoop clicks shut at 11.5 s.
  - 12.5 s: a door. 0.5 s silence → logo.
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v, 8 s, 3 shots: proof $1.65 + ×2 $7.40 | $9.05 |
  | Kling inserts ×4, ×2 each | $3.80 |
  | Stills, 8 | $2.40 |
  | **Total** | **≈ $15** |

### C4 · SOLENNE (lab-grown diamond ring) — "The Appraiser" (25 s)

- **Idea:** a family dinner. The new fiancée's ring is passed to Grandma, who produces a jeweler's loupe from her cardigan. Silence. She inspects. "Lab-grown." Tension. Then: "How much?" The fiancée whispers the price. Grandma slides her own hand under the table and quietly takes off her old ring.
- **Hook (0–1 s):** extreme macro through a loupe: a magnified eye, the ring facets filling frame.
- **Punchline (product-caused):** the price makes Grandma want an upgrade.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Macro through a 10× loupe (macro lens behind a real loupe): the oval stone fills frame | **Kling i2v** from a Flare still. "exactly one oval stone, four prongs" |
| 2 | 1.5–4 | Dining table wide, tripod: family frozen mid-dinner, everyone watching Grandma | Seedance; faces OK (licensed talent refs or averted) |
| 3 | 4–6.5 | Over-the-shoulder on Grandma: loupe to eye, ring held in tweezers | |
| 4 | 6.5–8.5 | Reverse: the fiancée swallows | |
| 5 | 8.5–11 | Grandma close (from behind the loupe; her mouth may be visible): "Lab-grown." | One spoken line. Seedance 2.5 r2v dialogue (doc 43 §1), kept inside the first 10 s of its generation; or keep the mouth off-screen and use VO |
| 6 | 11–14 | Medium two-shot: "…How much?" The fiancée leans in, whispers | Whisper = no lip-sync needed |
| 7 | 14–18 | Under-table insert, low tripod: Grandma's hand twists off her old ring | **Kling i2v** from a real hand photo; ring on the left ring finger |
| 8 | 18–21 | Grandma, deadpan, slides her phone to the fiancée: "Send me the link." | |
| 9 | 21–25 | End card: real product photo. "SOLENNE. Laboratory-grown diamonds, IGI certified." | Lab-grown disclosure **with equal prominence** |

- **Physics check:**
  - The loupe magnification must be consistent (10×).
  - The tweezers grip at the girdle.
  - Ring removal: the knuckle resists, a slight twist.
  - **Legal:** "Laboratory-grown" is clear. No "real diamond vs fake" framing that disparages mined stones falsely.
- **Audio map:**
  - 0.0 s: a near-silent room, a fork scrape.
  - 1.5 s: a clock tick (tension).
  - 8.5 s: line 1.
  - 11 s: whisper (unintelligible, then a cough-laugh).
  - 14 s: ring scrape.
  - 18 s: phone slide on the tablecloth + line 2.
  - 21 s: 0.5 s silence → logo + a single piano note.
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v, 15 s dialogue block, shots 2–6 & 8 (template 7.4 logic): proof $3.09 + ×3 $20.80 | $23.89 |
  | Kling inserts ×2, ×2 each | $1.90 |
  | Stills, 8 | $2.40 |
  | **Total** | **≈ $28** |

  If Seedance lip-sync fails: Wan 3.0 r2v + `audio_urls`, 720p, ~$1 per 10 s.

### C5 · TICKWELL (automatic field watch, lume) — "Countdown" (15 s)

- **Idea:** a New Year's Eve rooftop party. At 23:59:50 the power cuts out: speakers die, phones at 1%. Dark. One wrist glows green. The crowd gathers around a stranger's watch to count down from the seconds hand.
- **Hook (0–1 s):** a bass drop dies mid-beat; the frame goes black on a crowd's "ohhh".
- **Punchline (product-caused):** no battery, no signal. The mechanical watch with lume is the only clock left, and its wearer becomes the party.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Handheld crowd wide: party lights, then hard blackout | Seedance |
| 2 | 1.5–3 | Phone insert: a 1% battery icon dies | Post comp on a black screen (no AI UI text) |
| 3 | 3–5 | Darkness, moonlit medium: confused silhouettes | Low-light; motion minimal |
| 4 | 5–7 | Wrist insert: the lume glows green-blue; the seconds hand sweeps smoothly | **Kling i2v** from a dark Flare still; "lume glows only, smooth sweep, no ticking" |
| 5 | 7–10 | Overhead, from a camera on a jib: the crowd huddles around one wrist | Seedance. Faces lit only by the lume |
| 6 | 10–12 | Close insert: the seconds hand passes 12 | Kling, same still |
| 7 | 12–13.5 | Wide: fireworks over the city; the crowd erupts | Fireworks in the background; nobody holds them (no pyro near people) |
| 8 | 13.5–15 | End card: "TICKWELL. Automatic. No battery." | Real photo |

- **Physics check:**
  - Lume is bright for minutes after charging (plausible after a lit party).
  - An automatic's seconds hand sweeps (6 beats/s for a 21,600 vph movement; 8 for 28,800). Match the spec.
  - Fireworks are distant.
  - **Claim:** "No battery" is true for automatics. "Never stops" is false (power reserve). Avoid it.
- **Audio map:**
  - 0.0 s: house track; cut to dead silence at 1.0 s; crowd groan.
  - 3 s: wind on the rooftop.
  - 5 s: a close mechanical tick-sweep, mixed loud.
  - 7 s: whispered crowd counting "…five, four…" from 10 s.
  - 12 s: firework thump + cheer.
  - 13.5 s: crowd fades, logo.
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v, 10 s, 4 shots (1, 3, 5, 7): proof $2.06 + ×3 $13.86 | $15.92 |
  | Kling inserts ×2, ×2 each | $1.90 |
  | Stills, 6 | $1.80 |
  | **Total** | **≈ $20** |

### C6 · MIDBLOCK (everyday sneaker) — "Pick Up" (FOOH, 12 s, one take)

- **Idea:** T1's grammar. A 9 m sneaker sits across a city plaza. A real hand enters the foreground, pinches it in forced perspective and lifts it to normal size in the hand. A pigeon that was sitting on the giant toe box is left flapping in mid-air.
- **Hook (0–1 s):** the giant shoe is already in frame, with a passer-by walking under the heel tab.
- **Punchline (product-caused):** the displaced pigeon glares, then lands on the real shoe in the hand.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–3 | Handheld 24 mm POV, eye height: the plaza with the giant shoe; pedestrians at scale | Plate: a real or Soul Cinema plaza; Seedance r2v (shoe + plaza refs), **one continuous take** |
| 2 | 3–6 | Same take: a hand enters frame left and "pinches" the shoe; the shoe lifts and the perspective resolves to hand size | The hardest beat. Fallback: cut on the pinch to a **Kling i2v** of a real hand holding the real shoe in front of the same plaza |
| 3 | 6–9 | Same take: the pigeon hovers where the toe box was, then flaps down onto the shoe in hand | Write the bird's fate |
| 4 | 9–12 | Hold; super "MIDBLOCK. Fits any city." Logo | |

- **Physics check:**
  - Forced perspective: the camera position is fixed, the hand is ~40 cm from the lens, the shoe ~30 m away.
  - The shoe's contact shadow disappears when lifted.
  - Pigeon flight is plausible.
  - One take = doc 41's sensory/stunt grammar.
  - Trade dress: no stripes or swoosh shapes. Own signature: an odd-colour heel tab.
- **Audio map:**
  - 0 s: city ambience, a distant bus.
  - 3 s: a giant "creak" of rubber as it's pinched, pitched down.
  - 4.5 s: a cartoonish shrink whoosh (subtle).
  - 6 s: pigeon wing flaps.
  - 8.5 s: a soft landing coo.
  - 9 s: beat drop → logo.
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v, 10 s one take, ×4 takes (hard): proof $2.06 + $18.48 | $20.54 |
  | Kling fallback insert ×2 | $0.95 |
  | Stills, 4 | $1.20 |
  | **Total** | **≈ $23** |

### C7 · PACER (lightweight runner) — "Deli Scale" (15 s)

- **Idea:** a corner deli. A runner slaps her shoe on the deli scale. The deli man, deadpan, weighs it like cold cuts. Then he weighs a sandwich. The sandwich is heavier. He looks at her, then at the shoe, and wraps the shoe in deli paper.
- **Hook (0–1 s):** the shoe hits the stainless scale plate with a slap; the needle swings.
- **Punchline (product-caused):** the shoe weighs less than a sandwich (only if true: e.g. a 198 g shoe vs a ~300 g sandwich). He wraps it in deli paper like a sale.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Counter-height locked-off, 50 mm: the shoe lands on the scale plate, the needle swings | Use an **analog dial scale with a blank dial**; numbers comped in post |
| 2 | 1.5–3.5 | Medium: the deli man, apron, deadpan, looks at the shoe | Licensed talent or a back 3/4 |
| 3 | 3.5–5.5 | Insert: needle settles; post super "198 g" | Kling i2v |
| 4 | 5.5–8 | Same as shot 1: the sandwich replaces the shoe, the needle swings further; super "312 g" | Seedance; object fates written |
| 5 | 8–10 | Two-shot: they exchange looks | Hold = the joke (doc 43 §7.5) |
| 6 | 10–13 | Insert: hands wrap the shoe in white deli paper, tape, a marker scribble | Kling i2v |
| 7 | 13–15 | End card: "PACER. 198 g." | Real photo |

- **Physics check:**
  - The needle overshoots then settles (damped).
  - Paper creases.
  - **Claim:** the weight must be the real weight for a stated size (e.g. US M9) `[inf]`.
- **Audio map:**
  - 0 s: slap + spring twang.
  - Deli ambience: a slicer hum, a fridge buzz.
  - 5.5 s: a heavier thunk.
  - 8 s: 1.5 s near-silence (the beat).
  - 10 s: paper crinkle, tape rip, marker squeak.
  - 13 s: bell over the door, logo.
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v, 10 s, shots 1, 2, 4, 5: proof $2.06 + ×2 $9.24 | $11.30 |
  | Kling inserts ×2, ×2 each | $1.90 |
  | Stills, 6 | $1.80 |
  | **Total** | **≈ $15** |

### C8 · WEFT (merino travel tee) — "Laundry Bag" (15 s)

- **Idea:** a hotel. Day 1, Day 2, Day 3: same tee, different city out the window. On the morning of Day 4 the hotel laundry bag comes back on the doorknob, still empty, with a note.
- **Hook (0–1 s):** a dog in a hotel lobby sniffs the guy's tee, then shrugs and walks away, uninterested.
- **Punchline (product-caused):** the laundry has nothing to wash. The note reads: "Nothing to wash. — Housekeeping." The hotel has given up on him.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–2 | Lobby, low tripod at dog height: the dog sniffs the hem, then leaves | Seedance; dog weight and gait (doc 43 rule 10) |
| 2 | 2–4 | Hotel window wide, locked-off from the bed: a man in a grey tee, Paris rooftops; "DAY 1" super | |
| 3 | 4–6 | Same locked-off composition, same tee: Tokyo skyline; "DAY 2" | Match-cut; the tee unchanged |
| 4 | 6–8 | Same: desert city; "DAY 3" | |
| 5 | 8–10 | Macro: the merino jersey's fine texture, a crease falls out as he moves | **Kling i2v** from a real fabric photo |
| 6 | 10–12.5 | Corridor locked-off: the doorknob, the laundry bag hanging flat | |
| 7 | 12.5–14 | Insert: a handwritten note in the bag (post comp text) | Text in post |
| 8 | 14–15 | End card "WEFT. 100% merino." | Fiber claim accurate per Wool Act |

- **Physics check:**
  - Merino doesn't wrinkle much, so creases drop out (plausible).
  - The window plates must match the time of day.
  - **Claims:** "odor-resistant" needs a test; avoid "never smells". "100% merino" must match the label.
- **Audio map:**
  - 0 s: dog sniff, claws on marble, lobby murmur.
  - Each day: one city ambient sting (Paris accordion is a cliché; use a scooter, a train chime, a desert wind).
  - 8 s: soft fabric rustle.
  - 10 s: corridor HVAC.
  - 12.5 s: paper rustle.
  - 13.5 s: 0.5 s silence → logo.
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v, 10 s, shots 1–4 & 6: proof $2.06 + ×2 $9.24 | $11.30 |
  | Kling inserts ×2 | $1.90 |
  | Stills, 7 | $2.10 |
  | **Total** | **≈ $15** |

### 6.1 Ranking

**The best concept: C6 "Pick Up" (MIDBLOCK).**
- It copies the measured best performers' grammar: a one-take FOOH with a real-hand scale handoff (Jacquemus 15.4M; Foot Locker EU 281K).
- It needs no AI faces, so it dodges the backlash pattern.
- The product is huge in frame from second 1.
- The punchline is caused by the product's existence.
- It is AI-native: it can't be shot cheaply live.

**Second: C2 "Footprints".** It is the strongest conversion logic: a demo with a real proof insert, in the Vessi category (F10/F11).

For a VXO spec reel, make **C6 + C2 + C1**: one stunt, one proof and one watch. Together they cover the three sub-niches.

---

## 7. QA gate additions for this niche

Run these after doc 44 §10 and doc 45 §5.4:

1. Count stones, prongs, links, eyelets and panels in every frame. They must match the reference.
2. The dial reads only what we comped. Hands at 10:10 except in the scripted seconds shot.
3. No real trademark, monogram or trade-dress shape (doc 11 list). Screen at 2 fps.
4. Every proof claim (waterproof, tarnish, weight, hardness) is filmed for real or supered "Dramatization".
5. No AI person gives a testimonial (16 CFR 465).
6. Disclosure supers present: vermeil / plated / lab-grown, with equal prominence where required.
7. The real product photo closes the film.
8. Faces: licensed talent references, or averted. No synthetic "brand model".

## Sources

All URLs are inline in the tables above. Measured files and their metadata: `scratchpad/niche/fashion/meta.txt`. The local analysis script ran ffmpeg scene detection at 0.30, astats RMS per 0.5 s, and 2 fps tiles. Media is not committed.
