# 58 — Niche deep-dive: eyewear, bags, wallets, luggage and leather goods

Researched 2026-10-09. No generation money was spent. Nobody was contacted. Nothing was sent.

**What this adds.** Doc `11-niche-fashion-luxury.md` §3–§4 covers the *look* of leather and eyewear (grain macros, hinge snaps, the lens-tint grade, two style headers). Doc 51 covers EDC wallets as a gadget (Ridge G09/G13/G17, Ekster G12, the FOLIO NINE "Wobbly Table" concept C6). Doc 52 covers luggage as travel gear (Béis O4/O5, wheel and shell physics, the STOWAWAY "Sizer" concept C7). This doc does not repeat them. It adds:
- **41 ads downloaded and measured**: 20 brand TikToks and **21 Meta ads that were live or recent on Meta** (pulled from Motion's public brand and trending pages), plus YouTube metadata for 25 more;
- the market map: category sizes (Grand View, Grips, Statista), 30 brands with Shopify price bands and SKU velocity, Meta ad volume for 19 brands, Benly creative-lifespan data, a seasonality calendar;
- what converts here, with the evidence;
- the AI realism traps specific to lenses, frames, straps, hardware, leather grain, wheels and cards, with prompt fixes tied to doc 43;
- the legal rules that bite here: the FTC Leather Guides (16 CFR 24), FDA lens impact rule (21 CFR 801.410), blue-light and UV claims, Made in USA, lifetime warranties, Apple/airline/TSA marks, trade dress and the MetaBirkins case, AI likenesses of real people;
- the buyer, re-buy triggers, a lead-scoring add-on and a sample DM;
- 10 concepts (3 marked best, 1 single best) and 13 insights.

It builds on 41 (action realism), 42 (teardown method), 43 (models, prices, templates), 44 (comedy craft), 45 (what sells, policy), 46 (sound and QC), 48 (fashion and jewelry), 51, 52, 56 and the LESSONS file.

**Labels.**
- **[m]** = I measured it from the downloaded file: scene cuts with ffmpeg `select='gt(scene,0.3)'`, 2 fps frame tiles that I looked at, a 0.5 s RMS envelope, integrated LUFS and sample peak (`ebur128`), and a faster-whisper transcript.
- **[c]** = the brand's own claim. **[v]** = a vendor or agency figure (directional). **[inf]** = my inference. **[unverified]** = no primary evidence found.

**Method and limits.**
- **TikTok.** I harvested the newest ~10–13 video IDs of 60 brand handles from their public embed pages (`tiktok.com/embed/@brand`; 44 returned IDs; the `@paravel` handle turned out to be a fan account and was dropped), pulled metadata for 434 posts, ranked them by views and by multiple of the brand's own median, and downloaded the 20 strongest to `scratchpad/niche2/eyewear-bags/vids/` (no media committed). The embed page shows recent posts *plus pinned winners*, so old hits appear next to this week's posts. TikTok tag and profile listing via yt-dlp failed ("No working app info"), so creator posts outside brand accounts are under-sampled.
- **Meta.** The Meta Ad Library still returns HTTP 403 to automated fetches (docs 51, 54, 56). **Motion's public pages** carry the real ad files: each brand page (`motionapp.com/library/<brand>`) lists active-ad counts, new creatives per week, format tags and the 20 most recent ads with their video files; the weekly **trending** pages (`motionapp.com/trending/accessories/`, `/travel/`) show the most-saved ads with **days active**. I downloaded 21 of those Meta videos. Brand pages say "refreshed 4 months ago", so read them as a ~June 2026 snapshot; trending pages are this week's.
- **Paid vs organic.** As in docs 47–56: millions of views with a like rate under ~1 % is the paid-distribution signature (Spark Ads); ≥3 % is an organic hit. A flag, not a fact. On Meta, the number of **variants** Motion lists per ad (1–7) is a proxy for how much the brand invested in that concept.
- **YouTube.** Search metadata worked (views below). Every download failed ("Sign in to confirm you're not a bot", "Failed to extract any player response"). YouTube rows are metadata-only; brand videos with millions of views are almost always TrueView-paid [inf].
- **Web search.** The shared web-search budget for this run was exhausted after the first query, so market and legal facts come from direct fetches of primary or well-known pages (Grand View Research, Grips Intelligence, Benly, Statista, Cornell LII, FTC, AAO). Anything I could not fetch is marked [unverified].
- **Two-year window.** Oct 2024 – Oct 2026. 37 of the 41 measured ads fall inside it. I kept 4 older ones (2022–2023) because the brands pin them as their all-time winners, each marked "older".
- **Revenue figures** for private DTC brands are mostly third-party estimates that disagree by 10×. Each one is marked [unverified].

---

## 0. The ten things to know before pitching an eyewear, bag, wallet or luggage brand

1. **This niche runs on stills; video is the minority and the opportunity.** Across the 20 most recent Meta ads of 19 brands, **135 of 380 (36 %) are video** [v]. The Ridge runs **901 active ads, ~82 new per week, and 0 of its 20 newest are video**; Roka 1/20, Shady Rays 1/20, Cuyana 1/20, Bellroy 2/20, Quince 2/20 ([Motion](https://www.motionapp.com/library/the-ridge)) [v]. But in handbags and leather goods, **video ads live longer: 32 days vs 27 for images**, and Branded/Studio creative has the highest 30-day survival (46 %) after UGC ([Benly, handbags & leather goods Q1 2026](https://benly.ai/benchmarks/q1-2026/fashion-apparel/handbags-leather-goods)) [v]. A VXO film plus a stills pack cut from it fits both halves of how they buy.
2. **Stop-motion is the native format of this niche — and it is the most AI-friendly look there is.** Solgaard's "Carry-on Closet" stop-motion loop (5.3 s, a shelf rising out of a suitcase while folded clothes fly in) has **5.2M views** on TikTok, its MoMA version **2.5M** (both paid signature), and in 2026 Solgaard **re-shot the same loop in a new room** and runs it on Meta with 5 variants [m]. Ridge's "Stop Motion" film has **1.6M** YouTube views; Bellroy and Warby Parker have current Meta ads tagged Stop Motion [v]. Objects moving by themselves, hands-only, a locked-off camera: the safest thing a video model can render, and slight frame jitter reads as style, not error [inf].
3. **The mechanism is the ad.** The longest-lived creative in every sub-niche shows a *thing the product does*: the closet that rises (Solgaard), the cards that fan (Ekster, Ridge), the latches, the compression strap, the pocket map of a tote (Béis "what's in my bag", 7 variants), the 40-ft drop (Brevite). "Demo" is the #1 Motion tag at Away (27 %), Béis (27 %), Ekster (27 %), Monos (24 %), Dagne Dover (34 %) and Solgaard (26 %) [v]. VXO's rule (LESSONS): the *proof* stays real footage; AI builds the world and the gag around it.
4. **Wallets and handcrafted leather are growing fast; DTC luggage is shrinking.** Grips (tracked online GMV, Aug 2026): **slim and minimalist wallets $153M, +20–50 % in 2025, forecast +50 %+, conversion 3.0–3.5 %**; **handcrafted leather goods $371M, +20–50 %**; but **premium travel gear $448M, −10–20 %**, travel bags −10–20 %, sunglasses −10–20 % ([Grips](https://gripsintelligence.com/insights/industries/apparel-accessories/slim-and-minimalist-wallets)) [v]. Lead with wallets and leather; pitch luggage brands on *efficiency* (one film → many sale versions), not on growth.
5. **Collab drops are the share engine and they come with a deadline.** BÉIS × Rare Beauty: **15.5 % like rate, 1,226 shares in its first day** (launch 10/12) [m]; dime × *Mean Girls*: **1.7M** views, dropped on "Mean Girls Day" (Oct 3) [m]; Ridge × Batman Joker (10/7), Diff × Harry Potter (8/31), Topo × Toyota (9/9), Monos × Pre-Merger (10/5) appear in `products.json` [m]. Every collab needs a reveal film inside a licensor approval window — speed is VXO's advantage.
6. **Founders sell wallets; CG sells the mechanism inside the founder's video.** Ekster's founder ad (6 variants, 53 s) cuts his talking head with **CG exploded renders** of the cardholder; Ridge's founder Daniel Kane carries a 57.6 s "Ridge 2.0" film with stacked prototype shots; Dagne Dover's co-founder fronts 5 of its 20 newest ads [m][v]. The structure that sells here is *founder voice + an animated mechanism insert*, which is exactly the part AI makes cheaply [inf].
7. **The proven hook is a question or a complaint, not beauty.** Cuyana's "What's the most embarrassing thing in your bag?" (251K, 3.8 % organic) and Ridge's creator "I'm definitely gonna be returning this wallet… because I paid full price" (live on Meta now) both open on a pain or a reversal [m]. Benly: in handbags, accessories and travel, "Visual Intrigue" hooks dominate but **"Pain Point and Question-style openings frequently achieve longer lifespans"** [v].
8. **Eyewear's AI trap is the reflection, and the legal trap is health.** Lenses mirror whatever is behind the camera, both lenses must match, and prescription lenses bend the face behind them (§4). Legally, the American Academy of Ophthalmology "does not recommend any special blue light-blocking eyewear" ([AAO](https://www.aao.org/eye-health/tips-prevention/should-you-be-worried-about-blue-light)), yet Felix Gray's current Meta headline is a customer quote: *"REM and deep sleep have improved after 1 day of wearing these!"* [v]. VXO never puts a sleep, eye-strain or eye-damage claim on screen (§5).
9. **Leather words are regulated words.** The FTC Leather Guides cover "suitcases, traveling bags… billfolds, wallets… ladies' handbags… belts" and require disclosure of imitation leather, backing material and bonded leather ("Bonded Leather Containing 60 % Leather Fibers…") **in advertising, close to the claim** ([16 CFR 24.0, 24.2](https://www.law.cornell.edu/cfr/text/16/24.2)). An AI macro of "full-grain" texture on a PU bag is a false demonstration.
10. **The category ships broken audio and AI likeness risks.** 11 of the 39 measured ads with sound peak at or above −0.5 dBFS (six above 0 dBFS), and 9 sit at or below −24 LUFS (Portland Leather's Meta ad at **−40.6 LUFS**, Béis's at −36.6, Ridge × Batman at −38.7) [m]. Pit Viper's "ski resort cashier" skit (154K) shows a **look-alike of a real tech CEO** in what reads as an AI-generated diner (garbled chalkboard text) [m][inf] — the kind of shortcut VXO refuses (doc 45, LESSONS).

---

## 1. Market map

### 1.1 Size and growth

| Segment | Size | Growth | Source | Note |
|---|---|---|---|---|
| US eyewear (all: spectacles, contacts, sunglasses) | **$41.12B (2024)** → $62.78B (2030) | 7.3–7.4 % CAGR | [Grand View Research](https://www.grandviewresearch.com/industry-analysis/us-eyewear-market-report) [v] | Spectacles 74 % of revenue; brick-and-mortar 76.4 % (2023) |
| Global sunglasses | **$43.0B (2025)** → $111.6B (2033) | 10.1 % CAGR; **US 9.5 %** | [Grand View](https://www.grandviewresearch.com/industry-analysis/sunglasses-market) [v] | North America 31.6 % share; US sunglasses "a functional necessity rather than a seasonal purchase" |
| Global leather goods | $282.1B (2025) → $538.2B (2033) | 8.7 % CAGR | [Grand View](https://www.grandviewresearch.com/industry-analysis/leather-goods-market) [v] | North America 23.6 % (2024), the US 83.1 % of it; footwear 37.3 %; growth from "affordable-premium handbags, backpacks, laptop bags, and travel accessories sold online" |
| Global accessories (incl. bags, wallets, watches, jewelry) | $758.1B (2026) | 5.65 % CAGR 2026–31 | [Statista](https://www.statista.com/outlook/cmo/accessories/bags-accessories/united-states) [v] | **Online share 16.5 %** |
| **Online GMV tracked by Grips (Aug 2026 pages)** | | | [Grips](https://gripsintelligence.com/insights/industries/luggage-bags) [v] | Conversion = site-wide, not paid only |
| ↳ Luggage & Bags (300+ retailers) | $11B | **−0–5 %** (2026 fcst +0–5 %) | same | Conv. 2.0–2.5 %, AOV $0–100 |
| ↳ Premium travel gear (Tumi, Away, Béis, Monos, Calpak…) | $448M | **−10–20 %** | same | Conv. **1.0–1.5 %**, AOV **$200–300**, desktop 77 % |
| ↳ Travel bags & accessories (Vera Bradley, Baggu, State…) | $749M | −10–20 % (fcst +5–10 %) | same | Conv. 1.5–2.0 % |
| ↳ Leather handbags & accessories (Coach, Portland Leather, Hammitt, Senreve, Saddleback…) | $1.67B | −0–5 % (fcst **+20–50 %**) | same | Mobile 56 % |
| ↳ Fashion handbags & accessories | $3.24B | +5–10 % (fcst +50 %+) | same | Conv. 1.0–1.5 %, AOV $200–300, desktop 77 % |
| ↳ Leather goods & accessories (200+ retailers) | $721M | +0–5 % | same | |
| ↳ **Handcrafted leather goods** | $371M | **+20–50 %** (fcst +50 %+) | same | Conv. 2.5–3.0 %, **mobile 63 %** |
| ↳ **Slim & minimalist wallets** | $153M | **+20–50 %** (fcst +50 %+) | same | **Conv. 3.0–3.5 %** (highest in the niche), AOV $100–200 |
| ↳ Eyewear (350+ retailers: Warby, Ray-Ban, EyeBuyDirect, GlassesUSA…) | $2.82B | −0–5 % (fcst +20–50 %) | same | Conv. 2.0–2.5 %, AOV $100–200, desktop 62 % |
| ↳ Sunglasses (30+ DTC) | $131M | **−10–20 %** (fcst +10–20 %) | same | |

**Read [inf]:** the money is in eyewear (Rx) and handbags; the *growth* is in slim wallets and handcrafted leather; DTC luggage and DTC sunglasses had a bad 2025 and are forecast to recover. Luggage brands are under margin pressure (a $448M segment shrinking 10–20 %), so they buy efficiency; wallet and leather brands are growing, so they buy volume.

### 1.2 Creative benchmarks for this niche (Meta)

| Vertical (Benly Q1 2026) | Ads / brands | Median lifespan | Video share; video vs image lifespan | Best asset type (lifespan · 30-d survival · effectiveness) | Source |
|---|---|---|---|---|---|
| **Handbags & leather goods** | 19K / 15 | **24 d** | **40 %**; video **32 d** vs image 27 d | UGC 28 d · 48 % · **78**; **Branded/Studio 28 d · 46 % · 68**; Product Shot 18 d · 32 % · 31 (worst) | [Benly](https://benly.ai/benchmarks/q1-2026/fashion-apparel/handbags-leather-goods) [v] |
| **Jewelry & accessories** (incl. eyewear brands) | 76K / 48 | 24 d | 39 %; 35 d both | Lifestyle 27 d · 46 %; Product Shot 23 d (lowest) | [Benly](https://benly.ai/benchmarks/q1-2026/fashion-apparel/jewelry-accessories) [v] |
| **Travel & hospitality** (incl. luggage) | 46K / 63 | 26 d | 37 %; video 39 d vs image 34 d | **Motion Design/Animation 35 d · 55 % · 50** (longest-lived); Branded/Studio 30 d · 49 % | [Benly](https://benly.ai/benchmarks/q1-2026/travel-hospitality) [v] |
| Fashion & apparel (all) | 345K / 419 | 20 d | 31 % | — | [Benly](https://benly.ai/benchmarks/q1-2026/fashion-apparel) [v] |

**Read [inf]:** in this niche a plain product shot is the *shortest-lived* asset; a crafted studio film or an animation (stop-motion, CG mechanism) lives longest. That is the VXO lane. Lifespans of 24–26 days mean a new film roughly monthly — the Season plan's natural cadence.

### 1.3 The 30 brands (founder-led and $1–20M marked)

Prices from `products.json` on 2026-10-09 (median of each product's lowest variant; "new 60 d" = products created in the last 60 days) [m]. Meta = active ads / new per week from Motion [v]. TikTok = median views of the brand's recent embed-page posts [m]. Revenue bands are third-party or my estimates [unverified].

| # | Brand | Sub-niche | Founder-led? | Size band [unverified] | Price median / range · new 60 d | Ads seen | Fit |
|---|---|---|---|---|---|---|---|
| 1 | **Ombraz** | Armless sunglasses | Yes | **$1–10M** | $45 / $6–195 · 0 | TikTok 2.6K median; creator reviews (YT 96K, 70K) | ★ VXO band; strong mechanism (cord, no arms) |
| 2 | **Sunski** | Sunglasses (recycled) | Yes | **$5–20M** | $30 / $5–199 · 0 | TikTok 1.1K | ★ |
| 3 | **Knockaround** | Sunglasses ($20–60) | Family/founder | $10–30M | $45 / $0–200 · 0 | TikTok 283 median | Price-led; statics |
| 4 | **Diff Eyewear** | Sun + Rx, licensed collabs | Yes | $10–40M | $128 / $0–189 · **10** (Harry Potter 8/31) | TikTok 241 median | ★ Collab cadence |
| 5 | **dime optics** | Trend sunglasses | Yes | **$1–10M** | $60 / $8–60 · 0 | TikTok **1.7M** (*Mean Girls*), 278K (50 % off) | ★ IP drops; tiny brand, big hits |
| 6 | **Felix Gray** | Blue-light / Rx | Yes | $10–30M | $159 / $0–369 · 0 | Meta 52 / 12 per wk, 16/20 video | Claims risk (§5) |
| 7 | **Roka** | Performance sun + Rx | Yes | $20–50M | $165 / $0–335 · 9 | Meta 13, **80 % offer banners** | Stills-only now |
| 8 | **Caddis** | Readers + sun (40+) | Yes | **$5–20M** | $230 / $85–570 · **72** | — | ★ Presbyopia gag (C9) |
| 9 | **Pit Viper** | Party sunglasses | Founders | $50M+ | $75 / $4–645 · 25 | TikTok 11.8K median; brand comedy | Brand is its own studio |
| 10 | **goodr** | $25–35 sunglasses | Yes | $50–100M | $40 / $5–100 · 20 | Meta **435 / ~47 per wk**, 16/20 video; studio skits | Volume buyer |
| 11 | **Shady Rays** | Sunglasses + lost/broken protection | Yes | $30–60M | $89 / $0–250 · 4 | Meta **320 / ~29**, **19/20 image** | ★ Needs video |
| 12 | **Blenders** | Sunglasses | Safilo-owned (corporate) | — | $79 / $5–318 · 4 | — | Agency path |
| 13 | **Warby Parker** | Rx + sun (public co.) | Founder-run, public | $800M+ | n/a | Meta 134 / ~22; YouTube "Wow" **35.3M** | Reference |
| 14 | **The Ridge** | Metal wallets, MagSafe, rings | Founder-led | $100M+ | (403) | Meta **901 / ~82 per wk, 0/20 video** | Reference + test line |
| 15 | **Ekster** | Smart wallets, travel vacuum bags | Founder-led (Amsterdam) | $20–60M | $69 / $10–249 · 5 | Meta **512 / ~76**, 11/20 video, founder ads | ★ Founder + CG hybrid |
| 16 | **Flowfold** | Recycled-sail wallets (Maine, US-made) | Yes | **$1–5M** | $60 / $6–170 · **48** | — | ★ VXO band; Made in USA claim check |
| 17 | **Pioneer Carry** | Wallets/packs | Yes | **$1–5M** | $86 / $45–429 · 1 | — | Small |
| 18 | **Portland Leather Goods** | Leather bags, slings, wallets | Founder-led | $30–80M | $60 / $0–360 · 14 | Meta **243 / ~16**, BOGO; TikTok 666K | ★ Volume + quiet audio |
| 19 | **Saddleback Leather** | Heritage leather ("they'll fight over it when you're dead") | Yes (Dave Munson) | $10–20M | (404) | — | ★ Heritage story |
| 20 | **Parker Clay** | Ethiopian-made leather | Yes | **$5–15M** | $148 / $6–698 · 0 | TikTok 1.0K | ★ Mission story |
| 21 | **Lotuff Leather** | Handmade US leather | Yes | **$1–10M** | $665 / $25–4,900 · 0 | — | ★ Premiere tier |
| 22 | **Hammitt** | LA leather bags | Owner-led | $30–60M | $385 / $0–895 · 0 | — | |
| 23 | **Cuyana** | "Fewer, better" leather totes | Yes (Gallardo, Shah) | $50–100M | $198 / $5–798 · 2 | Meta 30, **19/20 image**; street interviews | ★ Needs video |
| 24 | **Dagne Dover** | Neoprene bags | Yes (co-founder on camera) | $30–60M | $115 / $1–725 · **43** (Super Soft 9/1) | Meta 45, 12/20 video | ★ |
| 25 | **Brevite** | Camera/school backpacks | Yes ("Brevite bros") | **$5–20M** | $70 / $18–300 · 0 | TikTok **35.4K median** (highest), 11.8M winner | ★ Back-to-school |
| 26 | **Solgaard** | Carry-on Closet luggage | Yes (Adrian Solgaard) | **$5–20M** | $196 / $0–764 · 0 | Meta 30, stop-motion loops | ★ Stop-motion brand |
| 27 | **Monos** | Luggage, aluminium, soft goods | Yes | $50–100M | $135 / $6–… · 6 (collab 10/5) | Meta **298 / ~18**; CG aluminium film | ★ |
| 28 | **BÉIS** | Luggage + bags (Shay Mitchell) | Founder-led (celebrity) | $100M+ | $108 / $0–974 · **40** (Rare Beauty) | Meta 43 / ~11, demo + "yapper" | Collab reference |
| 29 | **Away / July / Calpak / Paravel / State / Nomatic / Topo** | Luggage & packs | Mixed | $10M–$300M+ | Away $348 med, **55 new**; Paravel $400 med; State $98 · **40**; Nomatic $100 · 6; Topo $79 · **144** (Toyota); Calpak $66 · 2 | Away 48 ads; July **276 / ~15** (CaseSafe tracking) | Away, July = references; State, Nomatic, Topo = ★ band |
| 30 | **Stoney Clover Lane / Baggu / Bellroy / Peak Design** | Pouches, nylon bags, carry | Founder-led | $30–150M | Stoney Clover $78 · **141 new** (Disney Halloween); Baggu (404) | Baggu 38 Meta + 3.3M TikTok; Bellroy **204 / 18 of 20 image**; Peak Design 36 (press quotes) | Drop machines |

**The VXO target band** is the ★ rows under ~$30M with a physical behaviour to dramatise (a cord, a fan, a latch, a pocket map, a patina, a flex): Ombraz, Sunski, dime, Diff, Caddis, Flowfold, Portland Leather, Saddleback, Parker Clay, Lotuff, Dagne Dover, Brevite, Solgaard, Nomatic, State, Topo, Shady Rays (needs video), Cuyana (needs video). The $100M+ rows (Ridge, Warby, Béis, Away, goodr) are references and occasional "test line item" buyers (doc 51 §5.1 logic).

### 1.4 Price bands (what the buyer is selling)

| Band | Typical products | Ad implication [inf] |
|---|---|---|
| $20–60 | Sunglasses (goodr, Knockaround, Sunski, dime), pouches, nylon totes, card holders | TikTok/Spark and Shop; 5–15 s loops; drops and colours; offer banners (Roka 80 %) |
| $60–200 | Slim wallets (Ridge, Ekster $69 median), leather slings (PLG $60 median), Rx glasses ($95 Warby), Ombraz, Diff, backpacks (Brevite $70) | Meta video + creators; the 15 s VXO film with proof slot fits here; wallets convert best (3.0–3.5 %) |
| $200–500 | Carry-ons (Away $348 median, Paravel $400), leather totes (Cuyana $198), Caddis readers sets, Hammitt ($385) | Long consideration (premium travel conv. 1.0–1.5 %, desktop 77 %); demo + review + financing; Premiere-tier films |
| $500–5,000 | Aluminium luggage (Monos, Rimowa), Lotuff ($665 median), Mansur Gavriel ($595) | CG/craft films, YouTube/CTV; heritage and patina stories |

### 1.5 Seasonality calendar

| Month | Moment | Who it hits | When the film must be live → pitch |
|---|---|---|---|
| Jan | Vision-insurance and FSA/HSA year resets [inf]; "travel planning" season; Valentine's prep (wallets, bags) | Rx eyewear, luggage | Live Jan 2 → pitch late Nov |
| Feb | Valentine's (card cases, leather gifts); Presidents' Day sales; spring-break travel | Wallets, leather, luggage | Live Jan 25 → pitch Dec |
| Mar–Apr | **Sunglasses season opens**; spring break; new colourways | Sunglasses, luggage | Pitch Jan–Feb |
| **May** | **Mother's Day** (totes, handbags, sunglasses); **Memorial Day sales** (Shady Rays presale, Roka 25 % off, Solgaard summer sale on Motion); **graduation** (luggage, wallets) | All | Live Apr 20 → **pitch mid-March** |
| **Jun** | **Father's Day — the wallet peak** (Ekster "Father's Day sale", BOGO; Ridge "Fits his lifestyle"; Motion snapshots); weddings (Away "wedding travel" ads); summer travel | Wallets, luggage, sunglasses | Live May 25 → **pitch mid-April** |
| Jul | Prime Day; 4th of July; **back-to-school starts** (Brevite reposted its 11.8M "will it fit" on Jul 13) | Backpacks, sunglasses | Pitch late May |
| Aug | Back-to-school, college; end-of-summer sales | Backpacks, totes | Pitch June |
| Sep | Labor Day; fall launches and collabs (Diff × Harry Potter 8/31, Topo × Toyota 9/9, Dagne Dover Super Soft 9/1) | All | Pitch July |
| **Oct** | **Halloween/IP drops** (Ridge × Batman Joker 10/7, Stoney Clover Disney Halloween, dime × *Mean Girls* on Oct 3); Prime Big Deal Days; collab launches (BÉIS × Rare Beauty 10/12) | Wallets, pouches, sunglasses | Pitch Aug |
| **Nov** | **BFCM** — wallets and luggage peak gifting (Ridge's "Missed Black Friday?" re-used in summer) | Everything | Live Nov 1 → **pitch by early October (now)** |
| Dec | Gifting, last-ship dates; **FSA "use it or lose it"** (Rx glasses, prescription sunglasses) [inf]; holiday travel | Rx eyewear, wallets, luggage | Pitch Oct |

**Today (2026-10-09)** is the last useful week to pitch BFCM work, and the right moment to pitch **December FSA films to Rx eyewear brands** and **Valentine's films to wallet and leather brands**.

### 1.6 Where they advertise

- **Meta** (all of them): statics dominate (64 % of the 380 recent ads), offers lead the headlines ("BUY ONE GET ONE FREE" ×3 at Portland Leather; "BUY TWO, GET TWO FREE", "Up to 53 % off" at Ekster; "Free Upgrade to CaseSafe™" at July; "SUMMER SALE 25 % OFF SITEWIDE" ×7 at Roka; "FOUNDER SALE", "MISSED BLACK FRIDAY?" at Ridge) [v].
- **TikTok:** brand accounts are weak (medians 115–35K; 29 of 42 brands under 3K) except where the account is a personality (Brevite 35.4K, Pit Viper 11.8K, Baggu 11.1K, Béis 10.8K) [m]. Reach comes from Spark-boosted posts (Coach 6.8M at 0.35 %, Solgaard 5.2M at 0.28 %, Baggu 3.3M at 0.05 %, goodr 4.3M at 0.41 %) and collabs.
- **YouTube / CTV:** Warby Parker "Wow" **35.3M** (31 s) and "It All Started With Eyeglasses" 20.8M; Ray-Ban Meta 30.7M; Longchamp Le Pliage Xtra Fall 2026 **13.7M (10 s)**; Gentle Monster × Tilda Swinton 4.1M (61 s); Béis review/walk-through videos 1.8M and 1.7M; Ridge Stop Motion 1.6M; Ekster "Ditch the bulk" 594K (22 s) [YouTube metadata].
- **Creators and reviewers as the trust layer:** Trevor Wallace "*wears pit vipers once*" 2.6M (creator skit); Ridge × MKBHD 560K; long Monos reviews (383K, 120K); Ombraz reviews (96K, 70K); Quince handbag review "Too good to be true?" 123K [YouTube metadata]. Doc 51 N12: Ridge's founder called influencer marketing "the principal revenue driver".
- **Retail and IRL:** goodr's Cabana store (4.3M TikTok tour), Monos Chicago store (two current Meta ads), Coach SoHo "Tabby look-alike competition" (6.8M) — stores are content.
- **Licensed IP:** *Mean Girls* (dime), Batman/Joker (Ridge), Harry Potter (Diff), Disney and MLB (Baggu, Stoney Clover), Rare Beauty (BÉIS), MoMA Design Store (Solgaard), Toyota (Topo).

---
## 2. Teardowns: 41 measured ads (20 TikTok, 21 Meta) plus 25 metadata-only

Cut rate = shots ÷ duration (detected cuts + 1). Hook = what is on screen and in the audio in second 1. LUFS / peak are as published (platform re-encode). "1st s" = RMS of the first second vs the clip median.

### 2.1 Full teardowns: the 20 that matter [m]

| # | Ad | Date · views · likes · shares (or Meta signal) | Length · shots · shots/s · LUFS / peak | Shot list (timecodes) | Second 1 (hook) | Turn / punchline | Product interaction | Sound | Text / CTA | Why it sold |
|---|---|---|---|---|---|---|---|---|---|---|
| A01 | **Brevite "will it fit" (reply to a comment)** ([link](https://www.tiktok.com/@brevite/video/7119960505149787438)) | 2022-07-13 (older, pinned) · **11.8M** · **11.0 %** · 7.8K | 64.0 s · 2 · 0.03 · −17.4 / 0.0 | 0–6.6 selfie-cam, comment sticker: a customer's list (4 notebooks, 1 binder, 2 pencil cases, bottle, lunchbox, laptop); she counts it on her fingers: "Easy." · 6.6–64 **one locked-off tripod wide** in front of a wall of backpacks in every colour: laptop into its sleeve, notebooks, pink binder, pencil case in the quick-zip, lunchbox on top, bottle in the side pocket, zip shut | The customer's challenge as a sticker + a confident "Easy." | Everything fits; the bag still zips | Continuous packing, never cut | VO only, room tone; first-onset 0.09 s | Reply sticker | **The buyer wrote the brief.** One unbroken take is the proof. **In 2026-07-13 the brand re-posted the identical file (A01b, 64.1 s, same cut at 6.6 s): 250K views — 47× less.** Winners decay; the *skeleton* needs a new world |
| A02 | **Coach "Tabby Bag look-alike competition"** ([link](https://www.tiktok.com/@coach/video/7453122324405964063)) | 2024-12-27 · **6.8M** · 0.35 % (paid) · 603 | 6.6 s · 3 · 0.46 · −17.0 / −5.9 | 0–2.1 a flyer on a street pole: "Tabby Bag look-alike competition — Now @ Coach SoHo", QR code; super "Get ready to meet the contestants" · 2.1–5.1 handheld pan along store shelves of Tabby bags in ~15 colours · 5.1–6.6 quilted Tabbys | A lost-pet/pageant poster parody | The "contestants" are all the same bag | None (display) | Trend music, steady (1st s −18.9 vs −18.5 median) | "Vote for the Tabby of your choice in the comments" | **A colour range sold as a pageant**, a comment prompt, a 6 s loop. Costs nothing but an idea |
| A03 | **Solgaard "emotional baggage" Carry-on Closet** ([link](https://www.tiktok.com/@solgaard/video/7285425554864524587)) | 2023-10-02 (older) · **5.2M** · 0.28 % (paid) · 2.7K | 5.3 s · 1 · 0.19 · −11.1 / **+0.1** | One **locked-off stop-motion** take: a sage hard-shell opens by itself; a black shelving "closet" rises to full height; folded clothes fly in shelf by shelf (motion-blurred mid-flight); the closet collapses back, the case closes (loop point) | The case already opening in frame 0 | The closet folds back into a normal suitcase | The mechanism performs itself | Loud music bed (−11 LUFS, clipping) | Caption pun only | **Mechanism as a toy.** Loop, no face, no words. Re-made: MoMA version (**2.5M**, 10 s, sweatshirt, caps, sneakers, umbrella fly in; [link](https://www.tiktok.com/@solgaard/video/7294744552680721695)) and a **2026 Meta re-shoot in a new room** (A15) |
| A04 | **Baggu "Polka Dots"** ([link](https://www.tiktok.com/@baggu/video/7681669545643298061)) | 2026-09-04 · **3.3M** · 0.05 % (paid) · 37 | 18.6 s · 8 · 0.43 · −16.9 / −5.5 | 0–1.6 a toddler stuffs a blue dotted bag at a play table (animated dots pop over the frame) · 1.6–3.8 laughing adult, red dotted bag hung on a chair · 3.8–5.9 hands, clay toys · 5.9–7.6 farmer's market: dotted totes, lettuce poking out · 7.6–9.2 walking away in a crowd · 9.2–13.2 fruit stand, a peach handed over the bag · 13.2–16.3 toy baskets · 16.3–18.6 toddler hands a toy to an adult | Child in motion + graphic dots | None: a print as a life montage | Bags carried, stuffed, filled | Music only | Animated dot overlay in brand colours per shot | **The print is the hero; one graphic layer ties eight phone shots.** Paid reach for a pattern drop |
| A05 | **BÉIS × Rare Beauty "elevator"** ([link](https://www.tiktok.com/@beis/video/7694328184136797454)) | 2026-10-08 · **232K in 1 day** · **15.5 %** · **1,226** | 9.9 s · 1 · 0.10 · −21.8 / −2.2 | One **locked-off** take into a steel elevator: doors open → woman 1 with a pink luggage set; doors close; open → woman 2, same set; close; open → only the luggage; close; open → both women | Elevator doors parting (motion at frame 0) | People swap, then vanish; the pink set stays | Hands rest on the handles | Bright music; door chime | "Launching 10/12" | **An in-camera magic trick for a collab colourway.** The products appear in `products.json` on 9/28; the film went up 4 days before launch |
| A06 | **dime × *Mean Girls*** ([link](https://www.tiktok.com/@dimeoptics/video/7420912969078394155)) | 2024-10-01 · **1.7M** · 1.2 % · 472 | 14.1 s · 2 · 0.14 · −21.9 / −6.7 | 0–3 POV hands on stadium bleachers, a pink *Mean Girls* box, VHS "PLAY ▶" overlay · 3–6 box opened, pink pouch · 6–8 pouch opened · 8–12 pink cat-eye frames unfolded, temples flexed, cut-out ransom letters "REGINA" · 12–13.6 "REALLY PRETTY" · 13.6–14.1 card "MEAN GIRLS × dime." | A pink box in hands + movie line "On Wednesdays we wear pink" | The frames are "Regina" | Unbox, unfold, twirl | Film quote then music | Drops Oct 3 | **Licensed IP + a fan holiday (Oct 3) + hands-only POV.** A tiny brand's biggest post |
| A07 | **Cuyana "Bag Therapy"** ([link](https://www.tiktok.com/@cuyana/video/7532536555752246559)) | 2025-07-29 · 251K · **3.8 %** · 172 | 45.7 s · 31 · 0.68 · **−28.3** / −6.4 | 0–2 host on a NYC street, super "BAG THERAPY" · 2–24 she stops a woman: "What's the most embarrassing thing in your bag?" — an R2-D2 AirPods case · 24–33 store: hands move every item into a System Tote's compartments (laptop sleeve, bottle pocket, card slots) · 33–38 the tote handed over: "This is life-changing" · 38–46 walk-out, "organized, stunning" | **A question** that promises an embarrassment | The mess becomes a pocket map | Every pocket filled on camera | Lav dialogue, captions; under-mastered | Word-by-word captions | **Question hook + a reveal of the inside.** The bag's interior is the product; strangers make it credible |
| A08 | **Pit Viper "ski resort cashier"** ([link](https://www.tiktok.com/@pitvipersunglasses/video/7617260012330568974)) | 2026-03-14 · 154K · 4.3 % · **936** | 12.6 s · 2 · 0.16 · −18.3 / −2.1 | 0–4.6 creator in ski helmet + goggles, super "Me at the ski resort: How much is a burger and fries?" · 4.6–12.6 a **look-alike of a real tech CEO** as "Ski resort cashier" in a lodge diner, real audio "at least $600 billion" | A relatable price complaint | The absurd answer | **No product shown** | Real voice clip | Tags Vail Resorts | **Brand as comedian; ski-price pain.** The cashier scene reads as AI (chalkboard text "Boons Burger", "Tomato Basl") [inf]: a public figure's likeness used without consent — VXO never does this (§5) |
| A09 | **Warby Parker × Arch Manning "one condition"** ([link](https://www.tiktok.com/@warbyparker/video/7678455495463570719)) | 2026-08-26 · 18K · **8.3 %** · 111 | 13.0 s · 8 · 0.62 · −14.3 / −0.9 | 0–2.5 QB in tortoise frames on a stadium field, ball in hands: "When I partnered with Warby Parker, I had one condition." · 2.5–3.8 low 3/4 close: "Let me be an eye doctor." · 3.8–9.9 alternating wide/close Q&A: "Degree in optometry? No. Available most days? No. Know what I'm doing? No." · 9.9–12.3 whip blur to the real optometrist on set · 12.3–13 "Hard maybe." | A celebrity's deadpan demand | "Hard maybe" | Glasses worn throughout | Clean dialogue, −14 LUFS | Captions | **Deadpan rule-of-three** with the product as a costume; full film on YouTube "Is It the Glasses?" **2.0M** |
| A10 | **Cuyana "POV: $798 bag, $50 Uber"** ([link](https://www.tiktok.com/@cuyana/video/7641261923933162783)) | 2026-05-18 · 50K · 2.0 % · 64 | 8.8 s · 1 · 0.11 · −24.0 / −8.9 | One locked-off take on a subway bench: a woman in sunglasses scrolls, the brown work bag beside her | The price-justification joke as text | The super is the joke | The bag sits there | Trend audio | "POV: you spent $798 on your work bag but the $50 uber home is where you draw the line" | **Cost-per-wear humour defuses the price objection** in 9 s |
| A11 | **Brevite 40-ft watermelon drop test** ([link](https://www.tiktok.com/@brevite/video/7637261092531473678)) | 2026-05-09 · 15K · 2.2 % | 33.8 s · 23 · 0.68 · −18.2 / −3.0 | 0–2.3 low angle on a smokestack top, word-by-word captions "OUR… BAG… SURVIVE… 40-FOOT… WATERMELON" · 2.3–6.6 the two bags; buying 30-lb melons in a bodega · 6.6–12 faces drawn on melons ("Harry", "Ethan") · 12–19 12-inch drop, 3-ft stair drop · 19–24 thrown from a 40-ft window · 24–30 cheap bag: "blew straight through the seams" · 30–33.8 tease of a bigger test | A bag at the top of a chimney | The rival bag explodes; Brevite's melon is fine | Torture test | Fast VO, kinetic captions | — | **The Stanley ordeal format** with a named rival "cheap bag" (generic). Great test, weak distribution on the brand account |
| A12 | **goodr "Cabana" store tour** ([link](https://www.tiktok.com/@goodr/video/7228330408415464750)) | 2023-05-01 (older) · **4.3M** · 0.41 % (paid) · 454 | 40.7 s · 16 · 0.39 · −13.5 / −0.8 | Wide of a store with giant sunglasses on the roof → every frame on a wall with $25 price cards → neon tunnel → disco room → patio | "If you haven't been to the goodr Cabana in Abbot Kinney…" | Each room tops the last | Racks only | VO + music | "$25 Active Sunglasses For Anyone" | **A retail world as entertainment** — and a world AI can build for brands with no store |
| A13 | **Monos Aluminium "Ladies and gentlemen"** (Meta, Cinematic B-Roll, **7 variants**; [Motion](https://www.motionapp.com/library/monos)) | Active (Jun 2026 snapshot) | 15.4 s · 5 · 0.32 · −17.9 / −3.9 | 0–5.5 turntable plinth in a brushed-steel void: silver → black → champagne case swap in place · 5.5–7.8 macro of the "M:" badge in the champagne shell · 7.8–10 a stack of cases at an angle · 10–11.6 macro along the ribs · 11.6–15.4 trio on the floor, "SHOP ALUMINUM" | A product already turning on a plinth + **pilot PA VO** | — (mood) | Product alone | Cabin-PA voice ("Ladies and gentlemen… please secure…"), music | "Shop aluminum" | **A CG-grade studio film with a sonic hook (the PA).** This is the VXO one-take/product-hero lane, already bought by a luggage brand |
| A14 | **Away "See it differently" (Tokyo)** (Meta, Cinematic B-Roll, **5 variants**; [Motion](https://www.motionapp.com/library/away)) | Active (Jun 2026) | 15.0 s · 15 · 1.00 · −14.8 / −0.2 | 0–1 hand on a case in a dark doorway · 1–3.8 a globe, neon motion blur · 3.8–6 red light, hand on a handle · 6–9.6 a woman spins with a red case at a ramen shop, couple dances in a crossing · 9.6–12 puddle reflections, a man at a pastry counter, a train door · 12–13.7 a woman laughing on a truck bed full of cases under cherry blossom · 13.7–15 hero group shot in a blossom field, "away" | Hands in close-up, music hit | VO: "We're all navigating something… Sometimes all you need is a different view. See it differently. Get away." | Cases rolled, carried, sat on | VO + music | Logo card | **Brand film at 1 cut/s.** Lifestyle editorial — Benly's weakest category in travel (eff. 31) — but Away pairs it with demos |
| A15 | **Solgaard Closet stop-motion, 2026 re-shoot** (Meta, Time Lapse, **5 variants**; [Motion](https://www.motionapp.com/library/solgaard)) | Active (Jun 2026) | 5.7 s · 1 · 0.18 · −14.2 / −3.7 | Same choreography as A03 in a warm hotel-style lounge: case opens, closet rises, clothes fly in (motion-smeared), collapses, closes | Same | Same | Same | Music | — | **The 2023 winner's skeleton, re-dressed.** Proof that brands pay to remake a loop in a new world — the VXO Season plan in one example |
| A16 | **goodr "Shades on, log off" (desk)** (Meta, Transformation, 3 variants; [Motion](https://www.motionapp.com/library/goodr)) | Active | 15.0 s · 1 · 0.07 · −17.6 / **+1.1** | One locked-off take on a hot-pink studio set: a stressed man at a laptop (super "20 % OFF EVERYTHING") puts on sunglasses → "SHADES ON / LOG OFF" → sweeps the desk, dances, catches a frisbee | A visibly stressed face at a laptop | Sunglasses flip his mood | The put-on is the turn | Music; clipped | Offer super first, logo last | **Offer first, gag second, one take.** goodr ships ~47 new creatives a week with this studio template (sister ad: a cyclist knocks his laptop shut) |
| A17 | **Ekster founder "every iPhone user's dream"** (Meta, Founder/Transformation, **6 variants**; [Motion](https://www.motionapp.com/library/ekster)) | Active | 53.4 s · 31 · 0.58 · −23.9 / −2.9 | 0–4 hands clip the red cardholder to an iPhone · 4–6.5 founder to camera, name super · 6.5–10.5 2016 team photo; "wallets hadn't changed in centuries" over old wallets · 10.5–18.5 Kickstarter page ("$331,946… 3,009 backers") · 18.5–28 **CG renders on black**: the MagSafe holder in orange, exploded layers, "dual-sided MagSafe tech" · 28–40 hands demo Find My on the phone, card fan · 40–49 "100 % recycled aluminium… lifetime warranty" · 49–53.4 end card "Get yours at ekster.com" | The product on the phone in hands | 10 years of iteration → "the first…" | Clip, fan, find | VO, music low; quiet master | Supers per claim | **Founder voice + CG mechanism inserts + a proof montage.** Every claim (Apple Find My, recycled aluminium, warranty) is the brand's own, with its documents |
| A18 | **Ridge creator "I'm definitely gonna be returning this wallet"** (Meta trending, Sept–Oct 2026; [Motion trending](https://www.motionapp.com/trending/accessories/)) | Top-saved this week | 33.3 s · 9 · 0.27 · −24.5 / −6.6 | 0–1.8 creator holds the boxed wallet: "I'm definitely gonna be returning this wallet." · 1.8–21 "…not because of the magnet… not the design… not the colour… not the cash strap… holds 12–15 cards" — each "not" over a demo (magnet on the iPhone, card push-out, cash under the strap) · 21–28 "…because I paid full price. They have a massive sale" · 28–33 "Do not pay more than you have to" | **A complaint that is a fake-out** | The reason is the sale | Constant handling, real demos | Selfie audio | Link below | **The reversal hook** carries 6 features in 20 s. Every feature is shown on a real product |
| A19 | **Meller sunglasses triptych** (Meta trending, **active 41 days**; [Motion trending](https://www.motionapp.com/trending/accessories/)) | 41 d (the longest-running in the accessories feed) | 10.9 s · 6 · 0.55 · −14.4 / −1.6 | Three stacked selfie panels (three faces, same frame family) · 3.0 a boat, a woman tucks hair · 4.0 hands rotate the frame against blue sky / a man's face swaps three lens colours · 6.7 a woman in a suede jacket against a stone wall · 8.0–10.9 a man in a desert with a scarf | Three faces in one frame | Colour-swaps on the same face | Worn, flipped against the sky | Music | — | **"Will it suit me?" answered by many faces at once** (doc 11's objection). Real people, phone footage, edited like a lookbook. 41 days is ~1.7× the category median |
| A20 | **Polène "Numéro Neuf" in nature** (Meta trending; [Motion trending](https://www.motionapp.com/trending/accessories/)) | Top-saved | 9.1 s · ~12 (flash cuts) · ~1.3 · −27.0 / −6.0 | A taupe bag on a black rock by a lake · in tall grass with a dark chain · standing on still water with its reflection · macro of the folds · on a tiny wooden raft with a cloth sail · back on the rock | The bag in an impossible-calm landscape | The bag "sails" | None; the bag is a sculpture | Ambient, quiet | Logo once | **Object-in-a-world, surreal but plausible** (Loewe/Jacquemus school). Whether CG, AI or practical is [unverified]; it is exactly the shot type Seedance/Kling do well from a product still |

### 2.2 The other 21 measured ads (one line each) [m]

| # | Ad | Data | Note |
|---|---|---|---|
| B01 | Coach "who is behind these classics?" — designer Stuart Vevers reveal ([link](https://www.tiktok.com/@coach/video/7459803317921697054)) | 2025-01-14 · **2.6M** · **9.8 %** · 5.3K shares · 5.0 s · cut 3.8 | Trend format; the creative director is the punchline |
| B02 | Solgaard × MoMA Design Store ([link](https://www.tiktok.com/@solgaard/video/7294744552680721695)) | 2023-10-27 (older) · 2.5M · 0.27 % paid · 10 s · 0 cuts · peak **+1.3** | Stop-motion, gift-guide hook |
| B03 | Portland Leather "current carry: Oversized Sloan in Coldbrew" ([link](https://www.tiktok.com/@portlandleather/video/7618278942344056077)) | 2026-03-18 · 666K · 1.0 % · **743 comments** · 97.8 s · 5 shots | Staff "yapper"; comments are colour questions — a colour film would answer them |
| B04 | Baggu "In the studio for our new collection" ([link](https://www.tiktok.com/@baggu/video/7691312449697418510)) | 2026-09-30 · 513K · 0.55 % · 18.8 s · 17 shots (~1.1 s) | Prop still-lifes (tennis balls, grapes, trophies, a lamp) with crew hands: a **prop-comedy world** |
| B05 | dime "scientists are saying…" 50 % off ([link](https://www.tiktok.com/@dimeoptics/video/7439429790169451819)) | 2024-11-20 · 278K · 0.65 % · 7.6 s · **−28.3 LUFS** | Offer meme; quiet |
| B06 | Felix Gray *WALL-E* meme ([link](https://www.tiktok.com/@felixgray/video/7602538933246840085)) | 2026-02-03 · 32K · **11.5 %** · **3,069 shares (9.6 % share rate)** | **No product**, a film clip with "me / gf" labels: highest share rate in the set, and an IP risk |
| B07 | Ridge × Batman Joker unboxing ([link](https://www.tiktok.com/@ridge/video/7693962976054889741)) | 2026-10-08 · 28K · 0.35 % · 23.4 s · **−38.7 LUFS** | Hands unbox the collab tin; almost silent |
| B08 | Brevite "will it fit" re-post ([link](https://www.tiktok.com/@brevite/video/7662073977241668878)) | 2026-07-13 · 250K · 3.7 % · 64.1 s | Identical to A01 (same cut at 6.6 s) |
| B09 | goodr cyclist "Shades on, log off" (Meta Skit, 3 variants) | 15.0 s · one take | Same template as A16 |
| B10 | Béis "How to pack smarter" (Meta Demo, **7 variants**) | 9.5 s · 2 shots · **−36.6 LUFS** | Hands load packing cubes into a maple duffle, top-down + 3/4 |
| B11 | Warby Parker "A frame for the maximalists" (Meta Demo, 4 variants) | **3.4 s, silent** | A hand presses an apartment buzzer while holding the frames: a 3 s still-life loop |
| B12 | Warby Parker "catch the Ketty frame while you can" (Meta Unboxing, 4 variants) | **5.2 s, silent** | Red nails flip through a filing drawer and pull out red frames |
| B13 | Bellroy Venture Ready Sling (Meta Stop Motion/Demo, **6 variants**) | 40.0 s · 9 shots · −13.9 LUFS | Top-down: each EDC item goes into its pocket, then the sling worn four ways |
| B14 | Portland Leather Koala Sling (Meta Yapper, 6 variants) | 13.3 s · 9 shots · **−40.6 LUFS** | "Ladies on the go": four carry styles in 13 s; nearly inaudible |
| B15 | July Juliette Weekender (Meta Yapper, **7 variants**) | 37.4 s · 5 shots · peak **+0.3** | Creator monologue |
| B16 | Ridge 2.0 founder film (Meta trending) | 57.6 s · 31 shots | "You never have to buy a new wallet again… 12 years ago… 99-day trial… we'll replace the whole thing" |
| B17 | LOEWE bag on sun loungers (Meta trending) | 11.6 s · 3 shots | A model lies across stacked green loungers, the black bag dangling; editorial |
| B18 | Dagne Dover co-founder drop walk-through (Meta trending) | **118 s** · 42 shots | "We're going to the desert… roadside pit stops and buzzing neon signs": a drop explained by its maker |
| B19 | Béis "now what's in my East to West Tote" (Meta trending) | **6.6 s, one take** | Top-down into the open tote, **hand-drawn arrows label each item** (headphones, laptop, sunglasses, perfume, book) |
| B20 | Monos packing ASMR, aluminium trunk (Meta, 6 variants) | 22.9 s · 7 shots · peak **+1.2** | Hands only; latches, divider, clothes, shoes; no voice |
| B21 | Felix Gray ER-nurse testimonial (Meta, 3 variants) | 39.8 s · 17 shots | "I was coming home… with the absolute biggest headache… until I found these blue light glasses" — health-claim risk (§5) |

### 2.3 Metadata only (YouTube views ≈ paid TrueView [inf])

| Post | Views · length | Note |
|---|---|---|
| Warby Parker "Wow" ([YT](https://youtu.be/TuJao1sbrMQ)) | **35.3M** · 31 s | Brand spot |
| Ray-Ban Meta smart-glasses collection ([YT](https://youtu.be/E1LW_MteTho)) | 30.7M · 30 s | Corporate tech eyewear |
| Warby Parker "It All Started With Eyeglasses" ([YT](https://youtu.be/l0ocuQbWZCw)) | 20.8M · 31 s | Origin film |
| Longchamp "Le Pliage Xtra — Fall 2026" ([YT](https://youtu.be/9cHI8UUp-N4)) | **13.7M · 10 s** | A 10 s bag spot at luxury scale |
| Gentle Monster "2025 BOLD" with Tilda Swinton ([YT](https://youtu.be/YDqjZAZOuSo)) / FKA twigs "Bouquet" ([YT](https://youtu.be/wM7_iTWnCl0)) | 4.1M · 61 s / 2.7M · 81 s | Art-world eyewear films |
| Trevor Wallace "*wears pit vipers once*" ([YT](https://youtu.be/fVrVzeQ3CD0)) | 2.6M · 243 s | Creator character skit |
| Warby Parker "Is It the Glasses? (with Arch Manning)" ([YT](https://youtu.be/goKF7vmCiCQ)) | 2.0M · 31 s | Full version of A09 |
| BÉIS Travel Backpack review / Carry-On walkthrough ([YT](https://youtu.be/UGqJsl5BuoM), [YT](https://youtu.be/PknnVx06oN0)) | 1.8M · 51 s / 1.7M · 43 s | Paid "review"-format demos |
| Ridge "Wallet Stop Motion" ([YT](https://youtu.be/kS-I6mAioRg)) | **1.6M** · 44 s | Stop-motion again |
| Ridge "This Ain't Your Dad's Wallet" ([YT](https://youtu.be/wRndRX2MSiY)) | 898K · 28 s | Generational contrast |
| Oakley Meta Vanguard ([YT](https://youtu.be/Ttm9dKpEc9g)) | 705K · 31 s | |
| RIMOWA "Inside an Aluminium Suitcase" ([YT](https://youtu.be/oFzVY9qn_3c)) | 632K · 21 s | Craft/factory film |
| Ekster "Ditch The Bulk, Slim Your Pockets" ([YT](https://youtu.be/C6vqTV5NIYY)) | 594K · 22 s | |
| Ridge × MKBHD Biflex ([YT](https://youtu.be/wfEUkEq-mDI)) | 560K · 64 s | Creator collab |
| Herschel "Classics Aren't Born. They're Made." ([YT](https://youtu.be/7jARlvqTtIA)) | 502K · 30 s | |
| BÉIS × Shay Mitchell "The Weekender" ([YT](https://youtu.be/M2FYdGJtY4A)) | 468K · 68 s | Founder-celebrity |
| Jacquemus × Nike "Moon Shoe" ([YT](https://youtu.be/3qcCEDOhh50)) | 412K · 61 s | |
| Coach × Jennifer Lopez "#TabbyBag" ([YT](https://youtu.be/pT8JJYMTnI4)) | 353K · 16 s | |
| American Tourister "Gorilla vs Luggage" (1980) ([YT](https://youtu.be/5b1aRop-UbU)) | 197K · 30 s | **The original luggage torture ad** — still the template |
| goodr "technician" :30 ([YT](https://youtu.be/dsPtB0phHeo)) | 190K · 31 s | |
| Monos "Luggage & Travel Accessories" ([YT](https://youtu.be/YihfsnQfSBg)) | 185K · 34 s | |
| Pit Viper "The Original Informational Commercial" ([YT](https://youtu.be/UgJO3lcWVBs)) | 162K · 108 s | Parody infomercial |
| The Independent "Jacquemus send giant bags racing down streets of Paris" ([YT](https://youtu.be/mnDNAv9HBSM)) | 74K · 24 s | News coverage of the 2023 CGI "bag buses" FOOH stunt — the reference for giant-product CGI |
| Quince handbags "Too good to be true?" review ([YT](https://youtu.be/1TdPlKN8HzQ)) | 123K · 33 min | The "dupe/value" objection |
| Ombraz armless sunglasses reviews ([YT](https://youtu.be/SwJojTVGxI8), [YT](https://youtu.be/F-pymUoDx9w)) | 96K / 70K | "Will I lose them?" objection |

### 2.4 What the measured set says [m]

- **Two winning lengths.** The Meta set (21 ads) has a median of **15.0 s**, but it is bimodal: **9 ads ≤ 12 s** (loops, stop-motion, silent 3–5 s still-lifes, the 41-day Meller) and **7 ads ≥ 33 s** (founders, yappers, creator reviews). Nothing between 23 and 33 s. TikTok paid-signature posts: 5.3, 6.6, 10, 18.6, 18.8, 40.7 s. **A VXO film here should ship as a 5–6 s loop + a 15 s master + a slot to sit inside the client's 35–60 s founder/creator video.**
- **Motion in frame 0, by itself.** About half (19 of 41) open on the product already moving or being handled (case opening, doors parting, hands in a box, plinth turning). The weakest openers are a static store pan (A02 needed the poster) and a dark doorway (A14, carried by spend).
- **Hands, not faces.** 13 of 41 are hands-only or product-only (A03, A06, A13, A15, A20, B02, B07, B10–B13, B19, B20). Faces appear where a *person is the proof* (founder, creator, celebrity) or the *fit question* ("will it suit me?" — eyewear, A19).
- **Loops and one-takes win more often than montages.** One-take or locked-off: A01, A03, A05, A10, A15, A16, B02, B09, B11, B12, B19 (11 of 41), including 2 of the 5 biggest TikToks (A01, A03). Cut rate correlates with nothing.
- **The share leaders are jokes, not products:** Felix Gray's film-clip meme 9.6 % shares, the Coach designer 0.2 % shares but 254K likes, BÉIS × Rare Beauty 0.5 % in one day. Drops and gags get *sent*; demos get *bought*.
- **Audio is a sellable gap.** 11 of the 39 ads with sound peak at or above −0.5 dBFS (six above 0); 9 sit at or below −24 LUFS (PLG −40.6, Ridge × Batman −38.7, Béis −36.6) [m]. Doc 46's master (−14 LUFS, ≤ −1 dBTP) is a concrete, checkable improvement.
- **The niche reuses winners.** Brevite re-posted the same 64 s file after 4 years; Solgaard re-shot its 2023 loop in 2026; Ridge still runs "Missed Black Friday?" in June. **The creative skeleton outlives the file** — which is what a Season plan sells.

---

## 3. What converts in this niche (with data)

| # | Finding | Number | Source | Status |
|---|---|---|---|---|
| D1 | Conversion and basket by sub-niche | Slim wallets **3.0–3.5 %**, AOV $100–200; handcrafted leather 2.5–3.0 %; eyewear 2.0–2.5 %, AOV $100–200; luggage & bags 2.0–2.5 %, AOV $0–100; premium travel gear **1.0–1.5 %**, AOV $200–300; fashion handbags 1.0–1.5 %, AOV $200–300 (Aug 2026) | [Grips](https://gripsintelligence.com/insights/industries/luggage-bags) | [v] site-wide |
| D2 | Growth by sub-niche (2025) | Wallets +20–50 %, handcrafted leather +20–50 %, fashion handbags +5–10 %, eyewear −0–5 %, luggage & bags −0–5 %, premium travel −10–20 %, sunglasses −10–20 % | same | [v] |
| D3 | Device split | Premium travel and fashion handbags **77 % desktop** (big-ticket, considered); handcrafted leather **63 % mobile**; wallets 53 % mobile | same | [v] |
| D4 | Creative lifespan | Handbags & leather 24 d; accessories 24 d; travel 26 d; fashion overall 20 d | [Benly](https://benly.ai/benchmarks/q1-2026/fashion-apparel/handbags-leather-goods) | [v] Q1 2026 |
| D5 | Video vs image | Handbags: video 40 % of ads, **video lives 32 d vs image 27 d**; travel: video 39 d vs 34 d | same | [v] |
| D6 | Best asset type | Handbags: UGC (eff. 78, 48 % 30-d survival) and **Branded/Studio (68, 46 %)**; Product Shot worst (31). Travel: **Motion Design/Animation 35 d, 55 % survival** | same | [v] |
| D7 | Hooks | "Visual Intrigue" dominates; **Pain Point and Question openings live longer** (handbags, accessories, travel) | same | [v] |
| D8 | Ad volume (Meta) | Ridge **901 / ~82 per wk**; Ekster 512 / ~76; goodr 435 / ~47; Shady Rays 320 / ~29; Monos 298 / ~18; July 276 / ~15; PLG 243 / ~16; Bellroy 204 / ~7; Warby 134 / ~22 | Motion pages | [v] ~Jun 2026 |
| D9 | Media mix (20 newest per brand, 19 brands) | **135 video / 245 image (36 % video)**. Video-heavy: goodr 16/20, Felix Gray 16/20, July 13/20, Dagne Dover 12/20. Image-only or nearly: **Ridge 0/20**, Roka, Shady Rays, Cuyana 1/20 | same | [v] |
| D10 | Top format tags | Demo leads at Away, Béis, Ekster (27 %), Dagne Dover (34 %), Solgaard (26 %), Monos (24 %); Headline leads at Cuyana and Warby (49 %); **Roka 80 % Offer-First Banner**; Warby "UGC Selfie" 19 %; Béis "Yapper" 13 %; Peak Design "Press" 13 % (Wirecutter, Forbes, CNN quotes) | same | [v] |
| D11 | Investment signal | Most-variant Meta concepts: Béis packing demo (7), July weekender yapper (7), Monos CG aluminium (7), Monos store testimonial (7), Ekster founder (6–7), Bellroy stop-motion (6), Monos packing ASMR (6) | same | [v] |
| D12 | Longest-running in this week's accessories feed | Meller triptych **41 days** (median 24) | [Motion trending](https://www.motionapp.com/trending/accessories/) | [v] |
| D13 | Category hits (TikTok) | Brevite "will it fit" **11.8M / 11 %**; Coach Tabby pageant 6.8M (paid); Solgaard stop-motion 5.2M (paid); goodr store 4.3M; Baggu dots 3.3M (paid); Coach designer 2.6M / 9.8 %; dime × *Mean Girls* 1.7M | §2 | [m] |
| D14 | AI in this niche | No brand has published AI-ad results. Observed: CG mechanism renders inside founder ads (Ekster); CG-grade studio product film (Monos); surreal object-in-landscape (Polène, method unverified); an AI-looking look-alike skit (Pit Viper) | §2 | [m][inf] |
| D15 | AI ads in general | Gains only when they don't look AI; faces cancel the gain; weaker memory; disclosure trims credibility | doc 45 D30–D37 | Read |
| D16 | Founder-led wallet growth | Ridge's founder: influencers were the principal revenue driver | doc 51 N12 | Interview |

### 3.1 Answers by question [inf from the table and §2]

- **Formats that convert.** (1) **The mechanism loop** — stop-motion or one-take, 5–10 s, product performs its trick (A03, A15, B02, B13); (2) **the pocket map** — what's in my bag / will it fit, top-down or locked-off, one take (A01, A07, B10, B19); (3) **founder + mechanism inserts**, 35–60 s (A17, B16, B18); (4) **the reversal or question creator hook** (A18, A07); (5) **drops and collabs**, 6–15 s (A05, A06, A04); (6) **"will it suit me" faces** for eyewear (A19, A09). VXO builds (1), (2)-as-world, (5) and the inserts in (3); (4) and (6) need real people.
- **Proof types, strongest first.** A continuous real demo (packing, fan, flex, drop) → a torture test with a generic rival → press quotes and awards (Peak Design's Wirecutter line) → review counts → a founder's iteration story (Kickstarter numbers, prototype stack) → celebrity use.
- **Claims that work and are safe:** capacity in litres and real dimensions; "fits [X] in the sizer of [airline], [dimensions]"; card count ("holds 12–15 cards"); materials with substantiation ("full-grain", "100 % recycled aluminium"); warranty terms ("lifetime warranty", "99-day trial") that match the written warranty; UV protection rating with the test standard; polarisation (demonstrable). **Avoid:** "indestructible", "unbreakable", "fits every airline", "blocks harmful blue light", "better sleep", "reduces eye strain", "genuine leather" for split/bonded material, any "TSA-approved" wording, rival brand shapes.
- **Offers.** The niche is promotion-heavy (BOGO, B2G2, 20–53 % off, "free upgrade"), so every film needs an **offer slot** in its last 2 s that the client can re-skin, plus a no-offer brand version.
- **Length.** 5–6 s loop; 15 s master; a 3–5 s mechanism insert for founder videos; nothing at 20–30 s unless it is a story (C10 below).
- **Placements.** Meta Reels + Feed 4:5 (most spend), TikTok Spark (sub-$100), YouTube for $200+ luggage and eyewear (desktop-heavy buyers), PDP video (mechanism loops), Amazon listing video (wallets, sunglasses).
- **UGC vs cinematic.** Both, at the same brand (Away: creator demo + Tokyo film; Monos: CG film + packing ASMR + store testimonial). In handbags, UGC and Branded/Studio are the two longest-lived asset types (D6). VXO's place: the studio/animation half, plus hook modules for the UGC half.
- **AI ads and disclosure.** Unpublished in this niche. Hands-only, product-performs-itself and object-in-a-world shots are AI-safe; faces wearing glasses and bodies carrying bags are not (§4). Label per doc 45 §5.3; any AI human needs the NY synthetic-performer disclosure — another reason to keep faces real or absent.

---

## 4. AI realism pitfalls specific to this niche, and the fixes

Built on doc 43 §1 (model choice), §3 (references), §5 (failure table), doc 11 §3–§4 and doc 52 §3 (luggage). The rule of thumb: **the product is Kling 3.0 Pro i2v from the client's photo; mechanisms are stop-motion-style Seedance from real first/last frames or real footage; people and worlds are Seedance 2.5 r2v; the proof is real.**

### 4.1 Eyewear

| Pitfall | What goes wrong | Fix (prompt / reference / process) |
|---|---|---|
| **Lens reflections show the wrong world** | Mirror and dark lenses reflect a sky that isn't there, a ring light, or a crew; each lens reflects something different; reflections don't move when the head turns | Write what is *behind the camera*: "the lenses reflect only the opposite side of the street: a white wall and one tree; both lenses show the same reflection, offset slightly". Build a clean 'reverse plate' still and give it as a reference with "reflection source only". For hero shots, comp the reflection in post on a dark-lens plate |
| **Two lenses that don't match** | Different tint, shape or gradient per side | "Both lenses identical in shape, tint and gradient, symmetrical" (doc 11). Product refs: front, 3/4, folded. Reject any frame where the tint delta is visible |
| **Prescription refraction ignored** | Rx lenses show the face behind them undistorted, or distort it the wrong way | Real optics: **minus lenses (myopia) shrink the eyes and step the cheek outline inward behind the lens; plus lenses (readers) magnify the eyes**. Write the power: "−3.00 lenses: the eyes appear ~8 % smaller, the face edge steps inward at the rim" [inf from thin-lens magnification]. Simpler: clear-lens frames on a bust or in hand, not on a face |
| **Temples through the head, frames floating** | Arms pass through hair or ears; frames hover above the nose; the bridge sinks into skin | Profiles ≤ 15° head turns (doc 11); "temples run over the top of the ears and disappear under the hair; nose pads rest on the nose, 2 mm gap at the bridge". Prefer frames on a plaster bust, a table, or in hand |
| **Hinges and flex** | Metal hinges bend like rubber; spring hinges snap wrongly; TR90 frames shatter | Name the material: "acetate frame, rigid; only the spring hinge flexes ~10° and returns". **Any flex test is a real insert** (C3) |
| **Tint and polarisation** | Polarised "effect" drawn as a filter that changes colour randomly; glare removal shown on the wrong surfaces | Polarisation is physical: it removes glare from water, wet roads and glass at shallow angles, **strongest near Brewster's angle (~53° from vertical for water)**, and the glare *returns when the head tilts 90°*. **Shoot the before/after through the client's real lens in front of a phone** — a true, 2-minute proof (C4) |
| **UV/blue-light visuals** | Glowing "rays" blocked by a lens; "eye damage" overlays | Never draw health effects. A UV-400 claim appears as text with the standard, not as a picture (§5) |
| **Faces wearing glasses** | Waxy skin, eyes that don't line up behind lenses, identity drift — the most "AI" thing in the niche | Real talent with consent, or licensed creators; AI only for bust, hand, reflection, world. If a face is essential: one Kling i2v from a **real** photo, ≤ 5 s, ≤ 15° motion |

### 4.2 Bags, totes and leather goods

| Pitfall | What goes wrong | Fix |
|---|---|---|
| **Straps** | Shoulder strap clips through the body or coat, swaps shoulders between cuts, changes length; crossbody strap disappears behind the back | "Strap on the LEFT shoulder in every shot, outside the coat, diagonal to the right hip"; a FIXED GEOGRAPHY line per doc 43 §7.1; wide body shots ≤ 3 s; doc 11 "no strap close-ups generated" |
| **Volume and weight** | An empty bag hangs like a full one, or a full tote stays rigid and weightless; contents bigger than the bag | Write the load: "tote holds a 1.4 kg 14-inch laptop and a 0.7 kg bottle: the strap pulls the shoulder down ~2 cm, the base bulges". **Conservation of volume**: a 40 × 30 × 15 cm tote holds 18 L — list items that fit. Script each item's fate (doc 43 rule 12) |
| **Hardware** | Zipper pulls multiply; D-rings appear; clasp shape changes; logo plate warps | Count everything: "two brass zipper pulls, one magnetic snap, two D-rings at the top corners"; hardware macros only via **Kling i2v from a real macro photo**; logo plates comped in post (doc 43 §5) |
| **Leather grain and stitching** | Pebble grain "swims"; stitches change spacing; edge paint vanishes | Grain macro = Kling i2v from a real macro, one move, ≤ 5 s; write "stitch spacing 7 per inch, constant; dark edge paint along every edge"; never animate the grain itself |
| **Structure vs slouch** | A structured tote folds like cloth; a slouchy hobo stands rigid | Name the build: "structured: holds its rectangle when empty"; "slouchy: collapses to half height when set down, folds at the gusset" |
| **Interior contents** | Items pass through each other or pop in and out; the lining changes colour | The "pocket map" (A07, B19) = locked-off top-down; contents are **states between cuts** or stop-motion beats, never one continuous hand-placing of 10 items (doc 41 rule: few simultaneous actions) |
| **Patina and ageing** | Patina appears overnight; all leathers shown ageing | Only **vegetable-tanned** leather darkens noticeably with light and handling (months); chrome-tanned barely changes [inf]. Show patina as states across a time cut with "Dramatization." and only if the client's leather is veg-tan |
| **Material lies by picture** | A PU bag rendered with full-grain pores; "leather" texture on a vegan bag | The picture is the claim (FTC Leather Guides, §5): render only the client's real surface from its macro photo |

### 4.3 Wallets and small leather goods

| Pitfall | What goes wrong | Fix |
|---|---|---|
| **Card count and ejection** | Cards multiply or pass through the shell; the pop-up fan opens with the wrong number or angle | The mechanism is the proof: **real insert** (2-minute phone shot, A18 grammar). AI only before/after states. Write "exactly 6 cards, never more" |
| **Metal finish** | Anodised colour shifts (Ridge-type aluminium) under warm light; titanium looks like plastic | Swatch + PDP photo as refs; ΔE < 5 gate (doc 56 §10); "brushed anodised aluminium, fine linear grain, matte" |
| **Phones and MagSafe** | A generic phone grows an Apple logo; the magnet snaps from 10 cm away; the wallet floats | Generic slab phone, no logo, camera bump only if the client's PDP shows one; magnets "snap at ~1 cm with a small jump" [inf]; screen dark or comped |
| **Cash** | Garbled banknotes look fake (and AI money reads as counterfeit) | Show cash folded and out of focus, or a plain paper prop; never a legible generated bill [inf] |
| **Find My / tracking UI** | Garbled maps, wrong pins | Screen dark in generation; comp a **generic** map UI in post labelled "screen simulated"; no Apple UI or logo unless the client is in Apple's programme and approves (§5) |

### 4.4 Luggage (adds to doc 52 §3)

| Pitfall | What goes wrong | Fix |
|---|---|---|
| **Wheels** | Spinner wheels slide instead of roll, turn backwards, or stay still while the case moves | Doc 52: "four spinner wheels rotate and swivel; the case rolls, never slides". Wheel close-ups = real insert; AI wheels only in wides ≥ 5 m away or at night |
| **Telescoping handle** | Segments appear/disappear; the handle extends to arm height then grows | "Two-stage aluminium handle: extends 2 clicks, stops at hip height (~100 cm)"; a first/last-frame pair from real photos (Kling `last_image_url`) |
| **Shell flex and dents** | Polycarbonate dents like foil; aluminium flexes back like plastic | Polycarbonate "flexes ~1 cm and springs back" (doc 52); **aluminium dents and keeps the dent** (that's its charm — Rimowa, Monos) [inf]: never show aluminium springing back |
| **Lock dials and latches** | Dial digits garbled; latches clip through the frame | Dials not in close-up; latches only from real photos; "TSA" wording never generated on the lock |
| **Packing physics** | A carry-on swallows a week of clothes plus boots | Capacity in litres in the prompt (e.g., 39 L carry-on) and an item list that fits; compression shown only from real-product first/last frames (doc 52 C7) |
| **Airports, airlines, carousels** | Real airline liveries, gate signs, TSA uniforms | Invented airline, unreadable signage, no TSA insignia (doc 52 §4.3) |
| **Stop-motion mechanisms (Solgaard style)** | Smooth AI motion kills the stop-motion charm; or the mechanism rises in a way the real product can't | Prompt for the look: "stop-motion animation at 12 frames per second, each object jumps between positions with slight motion blur, camera locked, constant light"; choreography only within the real mechanism (shelf heights from the PDP) |

### 4.5 Model per shot type (consistent with doc 43 §1)

| Shot type | Model / template | Settings | Why |
|---|---|---|---|
| Product macro (hinge, lens, clasp, grain, card fan state, wheel) | **Kling 3.0 Pro i2v** from the client's photo | 5 s, `sound:"off"`, `cfg_scale` 0.5, `last_image_url` = packshot | Keeps logos, hardware and colour from the image (doc 43 §1) |
| Product hero on a plinth / turntable / bust (Monos A13 grammar) | **Cinema Studio 4.0** (template 7.3) | `drone-orbit` or `dolly-in`, `pacing:"single-shot"`, 720p | Enum camera; one move; studio light |
| Stop-motion mechanism loop (Solgaard grammar) | **Seedance 2.5 i2v** from the real "closed" photo, `end_image_url` = real "open" photo; or Kling first/last frame | 5–6 s, locked camera, "12 fps stop-motion" | Two real states anchor the path; jitter is the style |
| Object-in-a-world (Polène, Jacquemus grammar) | **Kling 3.0 Pro i2v** from a composited still (real product photo comped into a generated landscape) | 5 s, one slow move | The product pixels stay real |
| Multi-shot comedy with people, streets, airports, offices | **Seedance 2.5 r2v** (templates 7.5, 7.1 shape) | 9:16, 10–15 s, 4–8 shots, `generate_audio:true` | Multi-angle fidelity, native SFX as a sync guide |
| Inside-the-bag / inside-the-case POV (C2) | **Seedance 2.5 r2v** single shot, or i2v from a real interior photo | ≤ 8 s, locked lipstick-cam framing | One fixed real rig; few objects |
| Faces wearing glasses | **Real footage**; fallback Kling i2v from a real photo ≤ 5 s | — | Faces are where AI fails and where backlash lives |
| The proof (fit, flex, fan, drop, polarisation, packing) | **Real footage only** | Client phone, creator | FTC demonstration rule |
| Blocking previs | **Wan 3.0** 480p | $0.75 per 15 s, seed | Cheapest |
| End card | Real product photo + typography | — | Doc 51 QA |

---

## 5. Policy and legal

The client's counsel has the final word; this is the checklist VXO runs before any frame is generated.

### 5.1 US law and self-regulation

- **Leather words (FTC Guides for Select Leather and Imitation Leather Products, 16 CFR Part 24).** Covers "trunks, suitcases, traveling bags… brief cases… billfolds, wallets, key cases, coin purses, card cases… ladies' handbags, shoulder bags, purses… belts" ([§24.0](https://www.law.cornell.edu/cfr/text/16/24.0)). Key rules ([§24.2](https://www.law.cornell.edu/cfr/text/16/24.2)): disclose non-leather that looks like leather ("Imitation leather", "Vinyl"); disclose leather embossed to imitate another animal; disclose hidden backing ("Top Grain Cowhide Backed With Vinyl"); don't imply a product is wholly leather when parts aren't; **ground/bonded/reconstituted leather "should not be represented as leather"** — state percentages ("Bonded Leather Containing 60 % Leather Fibers and 40 % Non-leather Substances"); disclosures belong **in advertising too, conspicuous and close to the claim**. **VXO rules:** the material word on screen comes from the client's spec sheet; a vegan/PU product is never shown with animal-hide pores or called "leather" without the qualifier; "Italian leather" / "handmade" need proof.
- **Made in USA (16 CFR 323).** "All or virtually all" US content; qualified claims like "Made in USA of U.S. and imported parts" only with significant US content ([FTC](https://www.ftc.gov/business-guidance/resources/complying-made-usa-standard)). Flowfold, Lotuff, Saddleback-type heritage brands use origin as a selling point: ask for substantiation; a flag in the frame is a claim.
- **Warranties (Magnuson-Moss).** "Lifetime warranty", "you never have to buy a new wallet again", "built for life", "we'll replace the whole thing" (Ridge, Ekster) must match the written warranty's terms and exclusions [inf]. "Indestructible" / "unbreakable" are claims, not puffery, when a picture shows a test.
- **Demonstrations.** FTC (Colgate-Palmolive "sandpaper") and NAD *Dyson v. Dreame* (doc 51 §4): the picture is the claim; "Dramatization." cannot cure an AI scene that shows the product doing more than it does. Drop tests, flex tests, card capacity, "fits in the sizer", polarisation, waterproofing, packing capacity are all demonstrations → real footage.
- **Eyewear as medical devices.**
  - **Impact resistance (21 CFR 801.410):** "eyeglasses and sunglasses must be fitted with impact-resistant lenses"; the drop-ball test is a **5/8-inch steel ball (~0.56 oz) dropped from 50 inches** onto the lens centre; the lens must not fracture ([Cornell LII](https://www.law.cornell.edu/cfr/text/21/801.410)). A "drop test" visual must not imply a stronger standard than the client's lens actually meets.
  - **UV claims** ("UV400", "100 % UVA/UVB") need test data against the sunglass standard (ANSI Z80.3 in the US) [unverified: standard version per product]. Show the claim as text with its basis; never draw rays.
  - **Blue light:** the AAO says "there is no scientific evidence that blue light from digital devices causes damage to your eye" and "does not recommend any special blue light-blocking eyewear for computer use"; screen use before bed can affect sleep — a *screen-habit* message, not a *glasses* benefit ([AAO, 2021](https://www.aao.org/eye-health/tips-prevention/should-you-be-worried-about-blue-light)). Health claims need competent and reliable scientific evidence (FTC health-products guidance, doc 45). **VXO never films "less eye strain", "better sleep", "protects your eyes from screens" or a testimonial that says it** (Felix Gray's current Meta headline does).
  - **Prescriptions (FTC Eyeglass Rule, 16 CFR 456; amended 2024)** govern prescribers handing patients their Rx [unverified: details of the 2024 amendment]. For VXO: never imply a product replaces an eye exam, and never stage an "eye doctor" scene as real advice (Warby's A09 is played as an obvious joke by a celebrity).
- **Trademarks and trade dress.**
  - **Bags:** iconic shapes (the Birkin, the Tabby, the Le Pliage, monogram canvases) are trade dress. In *Hermès v. Rothschild* a jury found "MetaBirkins" digital images infringed Hermès's marks (Feb 2023) [unverified via primary source in this run; widely reported]. **A generated "inspired by" bag is not a safe parody.** "Dupe" ads (Quince-type) attract IP complaints; Meta bans "products that copy the trademark (name or logo)" and distinctive features of a genuine product ([Meta ad standards: third-party IP](https://transparency.meta.com/policies/ad-standards/)).
  - **Eyewear:** Wayfarer, Aviator teardrop, Clubmaster browline shapes (doc 11). The "other glasses" in a gag are generic, unbranded.
  - **Apple:** iPhone, MagSafe, AirTag, Find My are Apple marks. "MagSafe-compatible" and Find My language follow Apple's licensing programmes (MFi / "Works with Apple Find My") [inf]; no Apple logo or UI in generated frames; generic phones only unless the client provides approved assets.
  - **Airlines and TSA:** no real liveries or airline names (doc 52 §4.3). Locks are "TSA-recognized" through Travel Sentry/Safe Skies licensing; "TSA-approved" implies a government endorsement [unverified wording; check the client's licence].
  - **Licensed collabs** (*Mean Girls*, Batman, Harry Potter, Disney, MLB, Rare Beauty, MoMA): the licensor approves every frame, often in rounds of 5–10 business days [inf]. Build the approval calendar into the job.
- **Real people's likenesses.** Pit Viper's A08 uses a look-alike of a real executive. Right-of-publicity laws (NY, CA; Tennessee's ELVIS Act on voice) and Meta's impersonation rules make **AI look-alikes of real people off-limits** for VXO (LESSONS: no face-swaps; doc 45).
- **Reviews and testimonials (16 CFR 465, 2024).** No AI "customer" saying "life-changing"; review counts and press quotes ("Best Carry-On Backpack 2026") only from real, current sources with permission where the publication requires it.
- **Prop 65 (California).** PVC, vinyl and some coated leathers can carry Prop 65 warnings [inf]; "lead-free" / "PVC-free" need test reports.
- **Green claims.** "Recycled aluminium", "recycled sailcloth", "sustainable leather", "carbon neutral" follow the FTC Green Guides: specific, substantiated, qualified.
- **Currency.** Avoid legible generated banknotes [inf: Treasury reproduction rules and Meta counterfeit-goods sensitivity]; a folded, defocused prop note is enough.

### 5.2 Platform rules

| Topic | Meta | TikTok | VXO action |
|---|---|---|---|
| **Counterfeit / IP** | "Promotion or sale of counterfeit goods, such as products that copy the trademark (name or logo)" banned | Counterfeit and IP infringement prohibited | No look-alike luxury bags, no "dupe" framing, no blurred-logo trick |
| **Health claims (blue light, sleep, eye strain)** | Health & Wellness: unrealistic outcomes prohibited | Exaggerated health claims prohibited | No health outcome on screen or in VO |
| **Contact lenses / Rx** | Medical-device rules vary by market [unverified] | Contact lenses restricted in many regions [unverified] | VXO doesn't take contact-lens films without the platform check |
| **Weapons context** | — | — | Multitools/knives inside EDC wallets (some cards include blades): culinary/utility only, no "tactical" framing (doc 56 §5.2) |
| **Impersonation / public figures** | Prohibited without consent | Prohibited | No look-alikes (A08 is the counter-example) |
| **AI labels** | "AI info" | AIGC label | Doc 45 §5.3; a label does not fix a false demonstration |
| **Third-party marks in frame** | IP reports | IP reports | No Apple, airline, rival logos or shapes; generic phones and "other bags" |

### 5.3 Age gates

None for the products. Two flags: hip flasks and wine totes sold by leather brands are alcohol-adjacent (21+ targeting in the US); school backpacks (Brevite) target teens — TikTok restricts ad delivery and some formats for under-18 audiences, so build adult-facing (parent) versions [inf].

---
## 6. The buyer

### 6.1 Who signs a $1,200–3,500 film [inf with evidence]

- **$1–20M founder-led** (Ombraz, Sunski, dime, Caddis, Flowfold, Lotuff, Parker Clay, Saddleback, Brevite, Solgaard, Pioneer Carry): **the founder** signs, often with one growth marketer. The founder is the story (Brevite's "brevite bros" origin post, 1.5M; Solgaard's founder-named brand; Saddleback's Dave Munson). They shoot on phones and in-house (Brevite's drop test, Cuyana's street interviews).
- **$20–100M** (Dagne Dover, Ekster, Portland Leather, Shady Rays, Diff, Felix Gray, Monos, Nomatic, State, Topo): a **Head of Growth / Paid Social** owns the budget; a **creative lead** or the co-founder who fronts the ads approves (Dagne Dover's Jessy Dover appears in 5 of its 20 newest Meta ads; Ekster's Olivier in 6). They ship 5–76 new Meta creatives a week (D8).
- **$100M+** (Ridge, goodr, Béis, Away, Warby, Pit Viper): in-house studios, creator programmes and licensed collabs; VXO sells a **test line item, a collab reveal or a CG mechanism insert** they can't make fast in-house.

### 6.2 What they fear (ranked)

1. **The product looking wrong.** Hardware counts, strap side, lens tint, anodised colour and leather grain *are* the product; a buyer spots a wrong zipper pull in one second. Colour drift is the #1 objection in every product niche (doc 56 D14, Cuisinart).
2. **"Fake leather" by picture, and the lawyers.** The Leather Guides make the material a claim; a wallet founder who sells "full-grain" cannot have an AI macro that might read as PU, and an eyewear founder cannot be associated with health claims.
3. **AI faces in an eyewear ad.** Glasses are bought on faces ("will it suit me?"); waxy AI faces wearing frames are the most obvious AI tell in the niche and the biggest backlash risk (doc 45 D31).
4. **Looking like a dupe.** Bag and sunglass founders fight copies; an AI film that drifts toward a Birkin, Tabby or Wayfarer silhouette is a disaster for them and a trade-dress risk.
5. **Volume and speed.** Ridge ships ~82 creatives a week, Ekster ~76, goodr ~47; one film is irrelevant unless it yields many assets and statics.
6. **Missing the drop.** Collabs and Father's Day/BFCM dates are fixed; licensor approvals eat weeks.

### 6.3 What proof makes them pay $1,200–3,500

- **5 free frames of *their* product**, built from their PDP photos: hardware counted, colour checked against their swatch (side by side with the PDP and a ΔE readout), and **one frame showing their mechanism as a stop-motion or pocket-map still** (the closet, the fan, the pocket map, the latch). For eyewear: frames on a bust or in hand, the lens reflection designed, no AI face.
- **A claims sheet**: every on-screen word mapped to their documents (leather type per the Leather Guides, warranty text, UV test, capacity in litres, airline sizer dimensions); a line saying "no health claims, no rival shapes, no real people's likenesses".
- **The asset math.** One 15 s master → a 5–6 s mechanism loop, a 3–5 s insert for their founder/creator videos, 3 hook swaps, 4:5 + 9:16 + 16:9, an offer-slot end card re-skinnable for BOGO/BFCM/Father's Day, and 8–10 stills (the niche is 64 % static).
- **Proof that VXO knows their winners:** "your 2023 closet loop did 5.2M; here it is re-dressed for the holidays" (Solgaard); "your 'will it fit' did 11.8M in 2022 and 250K as a re-post; here is the same skeleton in a new world" (Brevite).
- **A portfolio piece in the niche** (§8 C1–C3, made as VXO spec films; C10 with Otto and Vee).

### 6.4 Re-buy triggers (why they rebook monthly)

1. **Creative lifespan of 24–26 days** (D4): a new hero film roughly monthly is the category norm — Season plan.
2. **Drops and collabs**: Stoney Clover 141 new products in 60 days, Topo 144 (Toyota collab), Caddis 72, Away 55, Flowfold 48, Dagne Dover 43, Béis 40, State 40, Pit Viper 25, goodr 20 [m]. Each needs a 6–15 s reveal.
3. **The gifting calendar**: Valentine's, Mother's Day, graduation, **Father's Day (the wallet peak)**, back-to-school, Halloween IP drops, BFCM, December FSA (Rx eyewear) — one hero world, re-skinned per moment.
4. **Winner refresh**: brands re-post and re-shoot old winners (Brevite, Solgaard) — a "skeleton re-dress" every quarter is a natural retainer.
5. **Founder video cadence**: founder-fronted brands publish a new walk-through for each drop (Dagne Dover 118 s, Ridge 57.6 s, Ekster 53 s); each needs new mechanism inserts and a hook head.

### 6.5 Best outreach angle

**Lead with their mechanism and their best-ever post, not with AI.** "Your [closet / card fan / pocket map / armless cord] is the best visual in your category; your [post] proved it. We'll turn it into a [5 s loop + 15 s film] in your exact colour for [the next drop / Father's Day / BFCM], and the proof stays your real footage." Avoid: health words (eyewear), "dupe", competitor names, AI cost-savings talk in the first message.

### 6.6 Sample first DM (never sent; for a founder-led tote/leather brand)

> Hi [first name] — your "what's in my bag" posts are the best thing on your feed (the pocket map in the [colour] tote is genuinely satisfying). I run VXO, a small studio that makes 15–30 s product films for founder-led brands.
>
> One idea for you: "Black Hole" — a camera hidden *inside* a messy tote at 11:48 p.m. while someone digs for keys, then the same camera inside your tote, where the key is found in one move. Your real interior stays the proof; we build the corridor and the chaos around it.
>
> Want 5 free frames with your actual tote (colour matched to your PDP), timed for the holiday gift guide? No call needed.
>
> — [name], VXO

(Every fact in the opening must be checked on their public page before use; if they have no "what's in my bag" post, open with a real, specific post.)

---

## 7. Lead signals: the niche scoring add-on for `.claude/skills/vxo-leads/SKILL.md`

Apply on top of the base 100-point score. The add-on moves a lead by **−25 to +30**; HOT stays ≥ 70 after the add-on. Public pages only.

| Signal | Points | How to check |
|---|---|---|
| **Gifting-window fit**: 5–7 weeks before Father's Day (wallets, sunglasses, leather), Mother's Day (totes, sunglasses), back-to-school (backpacks), BFCM (all), Valentine's (card cases), December FSA (Rx eyewear) | +8 | Today's date vs §1.5 |
| **A collab or IP drop announced or in `products.json`** (new SKUs with a partner name) in the last 60 days or dated ahead | +7 | `https://<store>/products.json?limit=250` titles + `created_at` (BÉIS × Rare Beauty 9/28, Diff × Harry Potter 8/31, Monos × Pre-Merger 10/5 are examples) |
| **SKU velocity**: ≥ 10 new products in 60 days (ignore engraving/personalisation add-ons, "PLP Spot" placeholders, bundles) | +6 | `products.json` (`created_at`) |
| **Meta library ≥ 80 % static** (Ridge, Roka, Shady Rays, Cuyana, Bellroy type) **or** videos that open on a static product/logo | +6 | Motion brand page `motionapp.com/library/<brand>` (count "Active · video" vs "image" in the 20 newest) |
| **A proven mechanism** (closet, fan, cord, latch, compression, flex hinge, pocket map) that their ads show only in stills or talking-head demos | +5 | Their PDP + ads |
| **A past winner they re-post or re-shoot** (pinned TikTok ≥ 1M, re-uploaded or re-made) | +4 | Embed-page IDs → yt-dlp metadata; duplicate durations |
| **Founder or co-founder fronts the ads** (needs inserts and hook heads every drop) | +3 | Motion tags "Founder" |
| **Audio faults in their paid video** (peak > −1 dBFS or < −24 LUFS) | +2 | `ebur128` on one public ad — a friendly, concrete note for the DM |
| **Growing sub-niche**: slim wallets, handcrafted/heritage leather | +3 | §1.1 (Grips +20–50 %) |
| **Health claims in current ads** (blue light, sleep, eye strain, "protects your eyes") | **−10** | Motion headlines, PDP — they may ask VXO to dramatise a claim we can't make |
| **"Dupe"/look-alike positioning of a luxury bag or iconic frame** | **−15** | Ads and PDP copy ("inspired by", "dupe") |
| **Material ambiguity** ("vegan leather" without a qualifier, "genuine leather" on bonded goods) | −5 | PDP materials section |
| **Uses AI look-alikes of real people or unlicensed film clips** in ads | −5 | TikTok/Meta (A08, B06 patterns) — values mismatch and legal exposure |
| **Corporate-owned** (EssilorLuxottica/Ray-Ban/Oakley, Safilo/Blenders, Samsonite group, Tapestry/Coach, Trove, VF) | −5 | Ownership; the path runs through agencies |
| **Amazon-only private label, dropshipped "RFID" wallets or no-name sunglasses** | −15 | Brand site, reviews |
| **Licensed-IP only with no in-house product story** | −3 | Their catalogue; approvals will gate every frame |

**VERY hot in this niche looks like [inf]:** a founder-led wallet, leather or tote brand ($2–30M) or an independent sunglass/readers brand, with a mechanism or pocket map that sells in demos, a Meta library that is ≥ 80 % stills, a collab or ≥ 10 new SKUs in the last 60 days, a gifting date 5–7 weeks out, and no health or dupe claims. Example: base 72 + gifting window 8 + collab 7 + static library 6 + mechanism 5 = **98**.

---

## 8. Ten ready film concepts (invented brands)

Conventions:
- Invented brands; clear names on USPTO before use; every "other bag", "other wallet", "other glasses" and "cheap case" is **generic and unbranded**, never a real silhouette (no Birkin, Tabby, Wayfarer, Rimowa ribs).
- **Otto and Vee appear only in C10** (VXO's own spec). Any other concept becomes a VXO spec film by casting Otto as the deadpan lead (mouth never visible) and Vee with her one stopwatch.
- Every camera position is a real rig: tripod (incl. low-mode/floor and balcony), slider, overhead C-stand arm, **lipstick camera inside a bag** (a real, cheap rig), handheld, jib, macro on a tripod. **The camera never passes through glass, walls, doors, bags or cases**; "inside the bag" means the camera was placed there before the shot.
- **Proof slot:** each concept names the real footage the client supplies; AI never performs the claim.
- No dialogue on visible lips. Each film ends with a 2-line VO tagline in a locked voice over a frame with no visible lips, plus the logo card and an **offer slot** the client re-skins.
- Faces: backs, profiles, silhouettes or wides; no close AI faces; eyewear on busts, in hands or on real talent.
- **Costs** use doc 43 §6 list prices (as in doc 56 §8): Seedance 2.5 r2v 15 s = $3.09 proof (480p) + 3 × $6.93 (720p) = **$23.88**; 10 s = $2.06 + 3 × $4.62 = **$15.92**; 8 s = $1.65 + 3 × $3.70 = **$12.74**; 20 s two-scene = **$31.84**; Seedance 2.5 i2v 6 s = $1.24 + 2 × $2.77 = **$6.78**; Kling 3.0 Pro i2v 5 s sound-off ×2 takes = **$0.95**; Cinema Studio 4.0 8 s = $1.66 + $3.70 = **$5.36**; Wan 3.0 480p previs 15 s = **$0.75**; stills ≈ $0.30 each; ElevenLabs VO ≈ $0.10. Totals exclude the client's proof footage.

---

### C1 · KEPT (organised leather tote) — "Black Hole" (15 s) ★ BEST 1 · ★ SINGLE BEST

- **Idea:** 11:48 p.m., an apartment corridor with a motion-sensor light. A woman digs for her keys in a big unstructured tote. We cut *inside* her bag: a lipstick camera taped to the bottom corner looks up at the opening — receipts, a banana, three lip balms, a knot of earbuds, a hand groping past the lens. Across the hall a neighbour arrives with a KEPT tote; inside it, every item sits in its pocket and the key hangs on a leash clip; her hand finds it in one move. Back in the corridor the first woman is still digging when the motion-sensor light times out.
- **Hook (0–1 s):** sound first — a muffled key jingle from somewhere inside the bag, then a hand plunges into the frame from above, already moving.
- **Punchline (product-caused):** in total darkness, a phone torch clicks on *inside* the messy bag: the key is lying right next to the lens. Only a bag with a place for everything avoids that scene.
- **Built on:** A07 Cuyana "Bag Therapy" (the inside of the bag is the product, 3.8 % organic), B19 Béis "what's in my tote" (pocket map, current Meta trending), A01 Brevite (one locked take of packing), D7 (pain-point openings live longer), doc 44 "the held last shot is the joke".

| # | t (s) | Shot (rig) | Action / notes |
|---|---|---|---|
| 1 | 0.0–1.5 | **Lipstick camera taped inside the bag's base corner**, 2.8 mm, looking up at the opening | Corridor light blows out the opening; a hand plunges in; receipts flutter; a lip balm rolls |
| 2 | 1.5–3.5 | **Tripod, locked-off, end of the corridor**, 35 mm, hip height | Woman (back 3/4) at her door, bag on a raised knee, digging; ceiling light on |
| 3 | 3.5–5.0 | Same lipstick camera | Banana, earbuds, three lip balms; her fingers pass a key ring that slides under a pouch (we see it, she doesn't) |
| 4 | 5.0–7.0 | Same corridor tripod (identical framing) | The neighbour arrives at the opposite door with a KEPT tote; her hand goes in without looking |
| 5 | 7.0–8.5 | **Lipstick camera inside the KEPT tote** — **proof slot: real footage of the real interior** | Pockets, laptop sleeve, the key on its leash clip; one hand, one move |
| 6 | 8.5–10.0 | Corridor tripod | The neighbour's door clicks shut; the first woman still digs; **the motion-sensor light switches off** |
| 7 | 10.0–12.5 | Lipstick camera in the messy bag, dark | A phone torch clicks on inside the bag: the key is next to the lens. Her hand freezes, then takes it. Hold |
| 8 | 12.5–15.0 | Packshot (real photo), top-down into the open KEPT tote with hand-drawn arrows labelling each pocket (B19 grammar) | "KEPT. Everything has a pocket." + offer slot |

- **Physics check:**
  - Tote 40 × 30 × 15 cm = **18 L**; the chaos contents (wallet, banana, 3 balms, earbuds, receipts, pouch, keys) fit with room; nothing floats or passes through anything.
  - **Granular convection:** when a bag is shaken, small dense items (60 g keys) sink through gaps and large light items rise — the keys end up at the bottom, next to the camera. True and the reason for the punchline.
  - Lipstick camera (~2 cm body, ~120° field of view) in the base sees the opening as a bright rectangle; corridor ~100 lux vs the bag interior ~5 stops darker → the opening clips to white and the interior is lit only by bounce — write it.
  - Motion-sensor lights time out on a timer (typically 15 s–several minutes, adjustable) [inf]; the time cut between shots 4 and 6 covers it.
  - Phone torch ≈ 50 lm: inside a dark bag it lights everything within 20 cm, warm-white, hard shadows.
  - Hands: one hand, fingers named per contact (doc 43 §5); no item placed and removed in the same shot.
- **Audio map (timecoded):**
  - 0.0: muffled key jingle (through fabric), receipt rustle; 0.6 hand rummage.
  - 1.5: corridor room tone, a TV murmur through a wall; 2.4 lip-balm clack.
  - 3.5: inside-bag rummage, banana thud 4.1.
  - 5.0: neighbour's footsteps on carpet stop; 7.0 inside KEPT: zip-pocket rasp 7.3, leash-clip snap 7.8, keys out 8.0.
  - 8.8: lock turn, door click 9.4; **9.6 motion-sensor relay click, light hum stops — 0.4 s of silence**.
  - 10.0: phone-torch tick; 10.6 one single key jingle as she lifts it.
  - 12.5 VO (warm, unhurried, mouth off-screen): `Everything has a pocket.` [pause] `Even the keys.` + sonic logo.
- **Model / template:** shots 1, 3, 7 = one **Seedance 2.5 r2v 8 s** clip ("EXACTLY THREE SHOTS AND TWO HARD CUTS, the camera is a fixed lipstick camera inside the bag base, it never moves"; refs: a real photo of a messy tote interior, the woman's hand ref); shots 2, 4, 6 = one **Seedance 2.5 r2v 8 s** clip (corridor plate, two women from behind, identical locked framing); shot 5 real; shot 8 real photo; Wan 3.0 previs first.
- **Cost:** 2 × $12.74 + previs $0.75 + 8 stills $2.40 + VO $0.10 = **≈ $29**.
- **Claim check:** only pockets and clips the real tote has; no time claim ("find keys in 1 second"); the messy bag is generic.
- **Why it's the single best:** sound-first hook with motion in frame 0; the punchline is caused by the product's real property (a place for everything) and grounded in real physics (keys sink); the inside-the-bag camera is a real, rarely used rig that makes viewers lean in; **no faces, no straps, no walking bodies** — the safest generation in the niche; it copies two measured winners' grammar (pocket map, question/pain hook); it re-skins for every tote, backpack, diaper bag, camera bag and weekender, and for Mother's Day and BFCM, so it is a Season-plan template.

### C2 · ROLLWELL (quiet-wheel carry-on) — "1 A.M." (15 s) ★ BEST 2

- **Idea:** 1 a.m. on a narrow cobbled street in an old European town. A tourist drags a cheap spinner: the hard wheels rattle like a jackhammer off the stone walls. Windows light up one by one. A second traveller glides through with a ROLLWELL — a soft hush. The windows stay dark.
- **Hook (0–1 s):** sound first — the rattle is already deafening at frame 0; a low wheel-height camera, a case ripping past.
- **Punchline (product-caused):** a slipper drops from a third-floor window and lands beside the noisy case — thud — while the ROLLWELL traveller turns the corner and a window light clicks off behind him.
- **Built on:** American Tourister's 1980 "Gorilla" (the luggage ordeal, 197K on YouTube), A13 Monos (sonic hook), Benly (pain-point hooks live longer), doc 52's wheel physics.

| # | t (s) | Shot (rig) | Action / notes |
|---|---|---|---|
| 1 | 0.0–1.5 | **Low-mode tripod at wheel height on the cobbles**, 24 mm, locked | A generic hard case rattles past left → right, wheels bouncing on setts |
| 2 | 1.5–3.5 | **Tripod on a third-floor balcony across the street** (~10 m up), wide | The sleeping street; the noisy traveller (back, small in frame); two windows light up |
| 3 | 3.5–5.0 | Street tripod, medium on a facade | A shutter swings open (window frame dark; a silhouette only) |
| 4 | 5.0–7.0 | Same low wheel-height tripod — **proof slot: real footage of the real ROLLWELL on cobbles** | The case glides past; wheels roll smoothly |
| 5 | 7.0–9.5 | Balcony wide | ROLLWELL traveller passes the noisy one; no new lights |
| 6 | 9.5–11.5 | Street tripod, medium on the noisy case | A slipper lands beside the case (falls from frame top), bounces once; he stops |
| 7 | 11.5–13.0 | Balcony wide | ROLLWELL turns the corner; one window goes dark |
| 8 | 13.0–15.0 | Packshot (real photo) | "ROLLWELL. Arrive quietly." + offer slot |

- **Physics check:**
  - Setts ~10 cm apart: at walking pace 1.3 m/s each wheel strikes ~13 joints per second → a 13 Hz rattle grain (write the rhythm into the SFX).
  - Sound falls ~6 dB per doubling of distance: 1 m → 10 m is about −20 dB, so the rattle must still read clearly from the balcony (night complaints start in the 50–60 dB range [inf]).
  - Slipper from ~7 m: t = √(2h/g) = √(14/9.81) ≈ **1.2 s** of fall, ~12 m/s impact, one soft bounce; it enters from the top of frame — the thrower is never seen.
  - Wheels roll and swivel, never slide (doc 52); the cheap case may wobble on two wheels at the setts — realistic.
  - Quiet wheels = larger, softer PU tyres with bearings [inf]; the "quiet" claim comes only from the client's measured test (dB at 1 m on cobbles).
  - Windows light 2–4 s after the noise passes (people wake, find the switch).
- **Audio map:**
  - 0.0: hard-plastic rattle at ~13 Hz grain, panning L → R, dominant; a dog barks far off 1.0.
  - 1.5: rattle reverberating off stone, −10 dB; 2.6 a window latch; 3.0 a second light switch; 4.0 shutter creak.
  - 5.0: **ROLLWELL: a soft rolling hush and a faint bearing whirr; the night ambience (crickets, a distant moped) returns at −45 dBFS**.
  - 7.0: the rattle again, distant; 9.5 a falling whistle (subtle) → 10.7 slipper thud → **rattle stops 10.8 — silence**.
  - 12.3: light-switch click.
  - 13.0 VO (mouth off-screen): `Arrive at one a.m.` [pause] `Leave the street asleep.` + sonic logo.
- **Model / template:** one **Seedance 2.5 r2v 15 s** multi-shot (template 7.1 shape: FIXED GEOGRAPHY of the street, "EXACTLY EIGHT SHOTS AND SEVEN HARD CUTS", shot 4 and 8 generated as placeholders and replaced in the edit), refs: a clean street plate (no signage, no look-alike cases), the generic case sheet, the ROLLWELL photo for shots 5 and 7 (wides only). Re-place every wheel hit and the slipper on measured frames (doc 46).
- **Cost:** Seedance $23.88 + Kling packshot push $0.95 + previs $0.75 + 8 stills $2.40 + VO $0.10 = **≈ $28**.
- **Claim check:** "quiet" only with a test; no "silent"; no airline, no city name on signs.
- **Why it's in the top 3:** the purest sound-first hook in the set, a universal travel pain, a physics punchline, faces never needed, and every luggage brand with good wheels (Away, Monos, July, Nomatic, State) has the proof footage already.

### C3 · SPRINGFORM (flexible-frame glasses) — "Sat On" (12 s) ★ BEST 3

- **Idea:** the most universal glasses disaster. A man drops onto the sofa where his glasses were lying. Dread. He lifts them out: they spring back into shape. He puts them on, then — deadpan — puts them back on the cushion and sits on them again, on purpose. His partner places her (generic) glasses beside them and sits.
- **Hook (0–1 s):** overhead on a sofa cushion, a pair of glasses lying there, and a backside entering frame from the top — the viewer knows what happens next.
- **Punchline (product-caused):** his deliberate sit: nothing. Her sit: a crisp *snap*. She turns slowly to him (profile).
- **Built on:** A09 Warby (deadpan rule-of-three), A18 Ridge reversal, doc 11 eyewear hinge grammar, doc 44 "the pause is the joke".

| # | t (s) | Shot (rig) | Action / notes |
|---|---|---|---|
| 1 | 0.0–1.2 | **Overhead C-stand arm** above a grey sofa cushion | Glasses on the cushion; a body sits into frame; the cushion compresses |
| 2 | 1.2–2.8 | **Tripod, living-room wide**, profile | He freezes mid-sit, eyes closed (profile only) |
| 3 | 2.8–5.0 | **Proof slot: real footage**, macro on a tripod | A hand lifts the frames: they flex and return; the brand's real flex test |
| 4 | 5.0–6.5 | Tripod, medium profile | He puts them on; deadpan |
| 5 | 6.5–8.0 | Overhead arm (same framing as 1) | He places them on the cushion and sits again, slowly, on purpose |
| 6 | 8.0–9.5 | Overhead arm | Her hand places a generic black pair beside the spot; she sits — snap |
| 7 | 9.5–12.0 | Tripod wide, both in profile, held | Stillness; she turns her head to him. Packshot inset: "SPRINGFORM. Built to bounce back." + offer slot |

- **Physics check:**
  - An 80 kg sitter on a 12 cm foam cushion: the foam spreads the load; glasses near the surface see a fraction of body weight (tens of newtons locally) [inf]; a flexible titanium-alloy or TR90 frame bends and recovers — **only to the degree the brand's own test shows** (state it: e.g., "temples flex 90° and return").
  - A cheap injection-moulded frame fails at the bridge or a hinge: one break, two pieces, no shatter.
  - Lenses stay in the rim in the proof shot (if the real ones pop out, the concept dies — check before pitching).
  - The cushion recovers in ~1 s after the sitter stands; no glasses visible through the fabric.
- **Audio map:** 0.0 cushion whump; 0.9 leather-sofa creak; 1.0–1.4 silence (dread); 3.0 a tiny frame "spring" tick (real); 4.2 clock tick in the room; 6.8 deliberate sit — whump, **no crack**; 8.6 her sit — whump + crisp plastic **snap at 8.9**; 9.0–10.5 silence + clock; 10.5 VO (off-screen): `Sat on them?` [pause] `They'll live.` + sonic logo.
- **Model / template:** shots 2, 4, 7 = **Seedance 2.5 r2v 10 s** ("EXACTLY THREE SHOTS AND TWO HARD CUTS", profiles only, same sofa plate); shots 1, 5, 6 = **Kling 3.0 Pro i2v** ×3 from overhead stills (real photo of the client's frames comped onto the cushion still); shot 3 real.
- **Cost:** Seedance $15.92 + Kling 3 × $0.95 = $2.85 + stills $2.40 + VO $0.10 + previs $0.50 = **≈ $22**.
- **Claim check:** "flexible" and "bounces back" must match the test; no "unbreakable", no "indestructible"; the partner's pair is generic (no recognisable frame).
- **Why it's in the top 3:** a pain every glasses-wearer knows, a product-caused reversal in one gesture, no AI face, proof in one real macro, and a 4 s loop (shots 5–6) for TikTok.

### C4 · CLEARCAST (polarised sunglasses) — "Glare" (15 s)

- **Idea:** 7 a.m., two friends on a lake dock. The water is a sheet of white glare. One wears CLEARCAST; he can see straight into the water — rocks, weeds, and the lure his friend lost last summer. The friend borrows the glasses and, curious, tilts his head like a dog: the glare comes back.
- **Hook (0–1 s):** a blinding sun-flare sheet across the water, a lure on a line already swinging into frame.
- **Punchline (product-caused, real physics):** the 90° head tilt that brings the glare back — he slowly straightens his head, and it's gone again. Deadpan.
- **Shots:** 1 (0–1.5) **low tripod on the dock**, glare sheet. 2 (1.5–3.5) tripod medium, two men from behind/profile, rods. 3 (3.5–5.5) **proof slot: real POV through a plain lens** held in front of a phone — glare. 4 (5.5–8) **proof slot: real POV through the client's CLEARCAST lens** — glare gone, lakebed visible, a lure on a rock. 5 (8–10) tripod medium: the friend borrows the glasses, tilts his head 90° (profile). 6 (10–11.5) **real POV through the lens rotated 90°** — glare returns. 7 (11.5–13) tripod medium: he straightens his head; nods. 8 (13–15) packshot + offer slot.
- **Physics:** reflected glare off water is strongly horizontally polarised, most completely near **Brewster's angle ≈ 53° from the vertical** (looking down at ~37° below the horizon); a vertical-axis polariser blocks it; rotating it 90° passes it. Low morning sun (~15° elevation) gives long glare on the water. Lures don't move underwater without current.
- **Audio:** 0.0 reel clicks + lapping water; 1.5 a loon far off; 4.0 a soft "whoa" exhale (no lips); 8.5 dock creak; 10.0 one water slap; 13 VO: `Less glare.` [pause] `More lake.` + logo.
- **Model:** Seedance 2.5 r2v 10 s (shots 1, 2, 5, 7) $15.92; three real POV proofs; Kling packshot $0.95; stills $2.40; **≈ $20**.
- **Claim check:** polarisation is demonstrable — show it *only through the real lens*; no "eye protection" health claims; UV rating as text with its basis.

### C5 · FINDERS (trackable slim wallet) — "Lost & Found" (15 s)

- **Idea:** a wallet slips from a back pocket onto a train seat. A cleaner hands it to a station lost-and-found clerk, who opens the logbook to write "Wallet, black…" — and looks up. The owner is already at the window, phone in hand.
- **Hook (0–1 s):** the wallet already sliding out of the back pocket onto the seat, low angle.
- **Punchline (product-caused):** the clerk sighs, tears out the half-written log page, and hands the wallet over without a word.
- **Shots:** 1 (0–1.5) **tripod low on the train floor** facing the seat: the wallet slides off. 2 (1.5–3) tripod at the door: doors close, the owner on the platform (back). 3 (3–5) tripod: a cleaner picks the wallet up. 4 (5–7.5) tripod behind the lost-and-found window: the clerk writes (hands + logbook). 5 (7.5–9.5) reverse over the clerk's shoulder: the owner already waiting, phone held low, screen comped with a **generic** map "screen simulated". 6 (9.5–11) wall clock: 18 minutes have passed since shot 2 (time cut). 7 (11–13) **proof slot: real** insert of the wallet's tracker slot/card and the phone alert. 8 (13–15) packshot + offer slot.
- **Physics:** crowd-sourced trackers update when the wallet is near participating devices, not continuously — the 18-minute clock jump keeps it honest; doors close in ~3 s; the wallet (~60 g) slides only on an inclined seat.
- **Audio:** 0.0 fabric slide + soft drop; 1.5 door chime and hiss; 3.5 station PA murmur (unintelligible); 6.0 pen scratch; 8.0 a phone ping (generic tone); 9.5 clock tick; 11.0 page tear; 13 VO: `Lost?` [pause] `Briefly.` + logo.
- **Model:** Seedance 2.5 r2v 15 s $23.88; Kling insert $0.95; stills; **≈ $28**.
- **Claim check:** "Works with Apple Find My" only if certified and approved by Apple's programme; otherwise "trackable via [brand] app"; no Apple UI or logo; no railway brand.

### C6 · GRAINHOUSE (full-grain leather folio) — "Flakes" (15 s)

- **Idea:** a quiet boardroom. Every time a man opens his old (generic) "leather" portfolio, flakes of its peeling coating drift onto the glass table like snow. He brushes; more fall. Across from him a woman opens a GRAINHOUSE full-grain folio, ten years worn and darker for it.
- **Hook (0–1 s):** macro of a flake detaching from a cracked surface and falling.
- **Punchline (product-caused):** an assistant silently places a tiny dustpan beside him and leaves.
- **Shots:** 1 macro tripod: the flake. 2 tripod wide, boardroom (profiles). 3 overhead arm on the glass table: flakes accumulate. 4 slider on the GRAINHOUSE folio: worn, patinated, intact (**proof slot: real macro of the client's real 10-year-old folio**). 5 tripod medium: he brushes; a flake lands on his tie. 6 tripod wide: the assistant enters with the dustpan (back), exits. 7 held wide: nobody moves. 8 packshot + offer slot.
- **Physics:** bonded/coated materials have a polyurethane top layer that can delaminate with age and heat into 1–5 mm flakes [inf]; flakes are rigid and fall almost straight (no snow-like floating); full-grain hide has no separate coated layer to peel. Patina only if the client's leather is vegetable-tanned.
- **Audio:** 0.0 a tiny crackle; 1.5 HVAC hum, a pen click; 3.0 flakes tick on glass; 6.0 dustpan set down on glass, footsteps leave; 7–12 silence; 12.5 VO: `Full grain.` [pause] `Nothing to peel.` + logo.
- **Model:** Seedance 2.5 r2v 15 s $23.88; Kling macro $0.95; stills; **≈ $28**.
- **Claim check:** Leather Guides: GRAINHOUSE's "full-grain" must be documented; the rival is "an old portfolio", not "bonded leather from [brand]"; "Nothing to peel" is a true composition statement only if the folio has no applied top coat.

### C7 · LATCHLINE (aluminium-frame checked case) — "Carousel" (15 s)

- **Idea:** baggage claim. A zippered soft case comes down the chute and bursts; its owner's boxer shorts start a slow lap of the carousel. He pretends they're not his. A LATCHLINE case arrives shut tight; its owner lifts it and leaves.
- **Hook (0–1 s):** a zipper splitting open as the case hits the belt, clothes spilling.
- **Punchline (product-caused):** the boxers come round a third time with an airline "FRAGILE" sticker now stuck to them (invented airline, unreadable logo).
- **Shots:** 1 tripod at the chute mouth: the case drops and bursts. 2 tripod wide, carousel (backs). 3 medium: the owner, arms folded (profile). 4 tripod at the chute: LATCHLINE arrives, latches closed (**proof slot: real footage of the real latches on a real belt or a mock carousel**). 5 tripod: its owner lifts it by the handle, wheels down, leaves. 6 overhead jib: the boxers on lap two; a clock super "+90 s". 7 tripod medium: lap three, the sticker. 8 packshot + offer slot.
- **Physics:** carousel belts run slowly (roughly 0.4–0.5 m/s [unverified]); a 40 m loop takes ~90 s per lap → laps shown with time cuts; a case falls ~1 m from the chute onto the plates, tilts and settles; aluminium frames close on two latches; a burst zipper splits from the stress point near the corner.
- **Audio:** 0.0 chute rumble, case thud, zipper rip 0.4; 1.5 carousel motor drone and plate clacks; 4.0 LATCHLINE thud — solid, no rattle; 5.5 latch-handle click; 6.0 airport PA murmur; 11.0 a cough; 13 VO: `Latches don't burst.` [pause] `Neither will you.` + logo.
- **Model:** Seedance 2.5 r2v 15 s $23.88; Kling packshot $0.95; stills; **≈ $28**.
- **Claim check:** no "never opens", no airline names or TSA wording; the zippered case is generic.

### C8 · PALETTE (nylon crescent bag, colour drop) — "Mixing Desk" (10 s; Season-plan template)

- **Idea:** a hardware-store paint counter. A can locks into the shaker; the shaker roars; the lid comes off; the paint is exactly the new colour; the bag sits on the counter in that colour; the clerk dabs a swatch card next to it — a perfect match. Re-skinned for every drop with a new colour name.
- **Hook (0–1 s):** the shaker already clamping the can, a hard mechanical clunk.
- **Punchline (product-caused):** the colour chip's name is the drop's name ("Pickle", "Cold Brew") and the clerk writes "SOLD OUT" on the chip (only if true; else "Drops Tuesday").
- **Shots:** 1 tripod: shaker clamp. 2 macro tripod: shaker blur. 3 overhead arm: lid off, the colour. 4 **Kling i2v from the real bag photo** on the counter. 5 macro: swatch card beside the bag (ΔE-checked). 6 tripod: chip written on. 7 packshot with date.
- **Physics:** a shaker runs a gallon for ~3–5 min (time cut); fresh paint has a glossy skin and a slow, ribbon-like pour; the bag never touches wet paint.
- **Audio:** 0.0 clamp clunk; 0.6 shaker roar; 3.0 lid pop; 3.4 a slow drip; 6.0 marker squeak; 8.5 VO: `New colour.` [pause] `Tuesday.` + date.
- **Model:** Seedance 2.5 r2v 10 s $15.92 + Kling ×2 $1.90 + stills **≈ $20**; each re-skin ≈ $5 (new Kling product shot + new card).
- **Claim check:** colour exact (ΔE < 5); "sold out" only if true.

### C9 · ARMSLENGTH (reading glasses, 40+) — "Menu" (12 s)

- **Idea:** a dim restaurant. At a long table of friends in their fifties, every menu is held at full arm's length — in sync. One woman unfolds ARMSLENGTH readers and pulls her menu in to a normal distance. The others slowly do the same with their arms — and the waiter, without a word, opens his apron pocket: a row of ARMSLENGTH readers.
- **Hook (0–1 s):** six arms extend six menus at once, a single synchronized paper swish.
- **Punchline (product-caused):** the waiter's apron of readers; he hands them down the table like bread rolls.
- **Shots:** 1 tripod wide from the table end (backs/profiles), arms out. 2 macro: menu text blurred → sharp as the readers go on (rack focus; real lens demo shot through the client's readers = **proof slot**). 3 tripod medium: she pulls the menu in. 4 tripod wide: the others copy, staggered. 5 tripod medium on the waiter (chest down): apron pocket opens. 6 tripod wide: readers passed hand to hand. 7 packshot + offer slot.
- **Physics:** with age the eye's near point recedes (from ~10 cm in youth to ~50–100 cm by the late 50s [inf]); readers of **+1.50 to +2.50 dioptres** bring comfortable reading back to ~40 cm; arms reach ~60–70 cm — the comedy is true.
- **Audio:** 0.0 one synced paper swish; 1.0 restaurant murmur, cutlery; 3.0 a case snap; 4.0 menu rustle; 7.0 apron pocket velcro rip; 9.5 VO: `Read the menu.` [pause] `Not the room.` + logo.
- **Model:** Seedance 2.5 r2v 10 s $15.92 (backs/profiles; doc 43: Seedance glitches past 3 characters → 3 diners in frame per shot, the rest implied off-frame) + real rack-focus proof + stills **≈ $20**.
- **Claim check:** readers are non-prescription magnifiers; no "replaces an eye exam"; no health claims; dioptre on screen = real product power.

### C10 · VXO spec · PLAINSIGHT (anti-reflective-coated glasses) — "Reflections" (20 s) — Otto & Vee

- **Idea:** Otto is directing a glasses product shot: frames on a plaster bust, a 100 mm macro on a tripod. Every take, the lenses show the whole crew: the boom, the lights, Vee and her stopwatch, Otto's moustache. They try a black flag, a black curtain, Otto in a black hood. Finally Vee swaps in the PLAINSIGHT pair: the lenses show only the bust's painted eyes. Otto nods once.
- **Hook (0–1 s):** an extreme close-up of a lens — and in it, a tiny reflected moustache leaning in.
- **Punchline (product-caused):** Vee leans into the PLAINSIGHT lens to check, sees nothing of herself, and clicks her one stopwatch: "that's the take".
- **Shots:** 1 macro tripod on the lens: the crew reflected (moustache). 2 tripod wide of the set from behind the crew: the bust, the camera wrapped in a black flag with a hole for the lens (a real product-photography technique). 3 macro: still reflected (flag now visible). 4 tripod medium: Otto in a black hood beside the camera (moustache peeking out). 5 macro: the hood reflected — a silhouette with a moustache. 6 tripod medium: Vee swaps the frames (hands). 7 macro: **PLAINSIGHT lens — only the bust's eyes** (**proof slot: a real side-by-side of coated vs uncoated lenses under one light**). 8 tripod medium: Vee leans in, clicks her stopwatch (one); Otto nods. 9 packshot + offer slot.
- **Physics:** uncoated lens glass (n ≈ 1.52) reflects R = ((n − 1)/(n + 1))² ≈ **4.3 % per surface** (~8.5 % for the two surfaces); a multi-layer AR coating brings it to ~0.5 % per surface → the reflection is ~8× (3 stops) dimmer and drops into black at the bust's exposure. Plaster bust and frames never move; the camera never moves through anything.
- **Audio:** 0.0 shutter click; 1.0 studio room tone, a fan; 3.5 flag rustle; 6.0 hood fabric; 9.0 Otto's single sigh (moustache, no lips); 12.0 frames set down on the bust (tiny tick); 15.0 **Vee's stopwatch click (her one stopwatch)**; 16.5 VO in Otto's locked voice (no lips visible): `No crew.` [pause] `Just eyes.` + Vee: `PLAINSIGHT.` + VXO sonic logo.
- **Model:** Seedance 2.5 r2v 20 s two scenes $31.84 (Otto/Vee refs, mouth never visible, one stopwatch lock) + Kling macro inserts ×2 $1.90 + stills $2.40 + VO $0.20 = **≈ $37**.
- **Claim check:** "reduces reflections" is demonstrable; percentages only from the coating's spec sheet; no eye-health claims.

### 8.1 Ranking

1. **C1 "Black Hole" (KEPT) — single best.** Sound-first hook, a punchline caused by the product and by real physics (keys sink), a real-but-unusual rig (the camera inside the bag) that is also the safest generation in the niche (fixed camera, hands, objects, no faces, no straps), and it copies the grammar of two measured winners (pocket map, question/pain hook). It re-skins for every bag type and gifting date.
2. **C2 "1 A.M." (ROLLWELL)** — the purest sonic hook, universal travel pain, faces never needed; luggage brands already own the wheel proof footage.
3. **C3 "Sat On" (SPRINGFORM)** — universal eyewear pain, a one-gesture reversal, the proof is one real macro, no AI face.

For a VXO spec reel in this niche, make **C1 + C3 + C10**: one bag film, one eyewear film, one Otto & Vee film that doubles as a VXO craft demo (we control reflections).

---

## 9. Thirteen insights nobody asked for (that would make VXO better)

1. **Stop-motion is the look to master for this niche.** Solgaard's stop-motion closet (5.2M + 2.5M, re-shot in 2026), Ridge's Stop Motion film (1.6M), Bellroy's and Warby's current stop-motion ads: objects moving by themselves on a locked camera. Prompting AI for "12 fps stop-motion" turns small temporal jitter from a flaw into a style [inf]. Build a stop-motion prompt block and a 5 s mechanism-loop template for every film in the niche.
2. **Winners decay; skeletons don't.** Brevite's identical re-post got 250K vs 11.8M (47× less); Solgaard paid to re-shoot the same choreography in a new room. Offer every client a "skeleton re-dress": their best-ever post, same structure, new world, new season — the clearest Season-plan argument in any niche so far.
3. **The inside of the bag is an unused camera position.** Bag brands sell interiors (Cuyana, Béis, Bellroy, Dagne Dover) but always film from above. A lipstick camera inside the bag (C1) is a real, cheap rig that nobody in the set uses.
4. **Founder + CG mechanism is the converting structure for wallets.** Ekster's 6-variant founder ad cuts to CG exploded renders; Ridge's founder film runs 57.6 s. A 3–5 s AI/CG mechanism insert inside the client's own founder video is how VXO's film plugs into their best-performing format — part of the film deliverable, not a separate product.
5. **Wallets are the hottest sub-niche and convert best.** +20–50 % growth and 3.0–3.5 % conversion (Grips), Father's Day and BFCM peaks, the highest ad volumes (Ridge ~82/week, Ekster ~76/week). Prioritise wallet and small-leather-goods leads; deprioritise DTC luggage (premium travel −10–20 %).
6. **This niche is 64 % stills — ship 8–10 stills with every film.** Ridge's 20 newest ads are all images; Roka 80 % offer banners. The stills pack from the film is half of what they will actually run.
7. **Eyewear's AI problem is the reflection, and it can be the joke.** Lenses mirror whatever is behind the camera — a crew, a ring light, the camera itself. Design the reflection in every eyewear prompt (§4.1), and use it as comedy (C10). Also: **retire doc 11's "dolly through the lens into the reflected coast" idea** — it breaks the LESSONS rule that the camera never passes through glass; do it as a match cut on the reflection instead.
8. **Eyewear needs faces; VXO shouldn't generate them.** "Will it suit me?" is answered by many real faces (Meller's 41-day triptych). VXO's eyewear films should be bust/hand/world films plus a slot for the client's real try-on faces, not AI models wearing frames.
9. **The niche ships quiet and clipped ads.** 9 measured ads at or below −24 LUFS (Portland Leather −40.6, Ridge × Batman −38.7, Béis −36.6) and 6 above 0 dBFS. "Your Koala Sling ad is 26 LU quieter than the platform target" is a specific, friendly, verifiable opener.
10. **Pain and question hooks outlive beauty hooks.** Benly says it for handbags, accessories and travel; the measured set agrees (Cuyana's question, Ridge's "I'm returning this", the dime meme). VXO's world-first openers should put the problem in frame 0 (C1 chaos, C2 noise, C3 the sit).
11. **Collab drops are a speed contest.** BÉIS × Rare Beauty got 15.5 % likes in one day; licensors approve in rounds. Pitch "frames in 48 hours, film in 7 days" to brands with a collab in `products.json` but no film yet.
12. **The look-alike shortcut is spreading in this niche.** Pit Viper's AI-looking CEO look-alike and Felix Gray's film-clip meme are top performers on share rate — and legal exposure. VXO's safe-by-design pitch (no real likenesses, no licensed clips, invented brands in specs, claims sheet) is a differentiator, not a limitation.
13. **December is eyewear's hidden season.** FSA "use it or lose it" and vision-benefit timing make Nov–Dec a buying window for Rx eyewear [inf] — and almost nobody's Meta library shows FSA creative. Pitch Rx brands now with an "FSA ends Dec 31" offer slot.

---

## 10. QA gate additions for this niche

Run after doc 44 §10, doc 45 §5.4, doc 46 §7, doc 51 §7 and doc 56 §10:

1. **Hardware count:** zipper pulls, D-rings, rivets, latches, card slots, hinge screws counted against PDP photos in every product frame.
2. **Strap and carry continuity:** the same shoulder, outside the coat, same length, in every shot.
3. **Lens checks:** both lenses identical; reflections designed and consistent with the scene behind the camera; no crew or camera in a lens unless it is the joke; Rx refraction plausible or lenses clear on busts.
4. **Material truth:** leather/PU surface from the client's macro; the material word on screen matches the spec sheet (Leather Guides); patina only on veg-tan and labelled "Dramatization." when time-lapsed.
5. **Proof slot is real:** fit, flex, card fan, drop, polarisation, compression, packing capacity and wheel smoothness are the client's footage.
6. **No health claims** in words, VO, supers or visuals for any eyewear (blue light, sleep, eye strain, eye protection beyond the tested UV rating).
7. **No look-alikes:** no iconic bag or frame silhouettes, no real people's likenesses, no film clips, no Apple/airline/TSA marks.
8. **Colour:** product colour within ΔE < 5 of the swatch; anodised metals and enamel edges checked under the film's grade.
9. **Physics:** wheels roll, aluminium dents (doesn't spring back), polycarbonate flexes 1 cm and returns, bags hang with weight, contents fit the volume, cards never exceed the count.
10. **Audio master:** −14 LUFS integrated, ≤ −1.0 dBTP measured on the encoded file (LESSONS).
11. **Deliverables:** 5–6 s mechanism loop, 15 s master, 3–5 s founder-video insert, offer-slot end card (BOGO/BFCM/Father's Day versions), 4:5 + 9:16 + 16:9, 8–10 stills, claims sheet, ΔE report.

---

## Sources

All URLs are inline above. Measured files (not committed): `scratchpad/niche2/eyewear-bags/vids/E01–E20.mp4` (TikTok, with `.info.json`) and `M01–M21.mp4` (Meta ads from Motion's public pages); analysis in `scratchpad/niche2/eyewear-bags/an/` (`*_tile.jpg` 2 fps tiles, `*_stats.txt` scene cuts at 0.30 + LUFS + peak, `*_asr.txt` faster-whisper base.en); TikTok harvest in `emb/` (434 posts, 44 handles); Motion pages in `motion/`; Shopify snapshots in `shop/shop.txt`. Map from this doc's IDs to files: A01=E01, A02=E02, A03=E03, A04=E04, A05=E08, A06=E06, A07=E12, A08=E11, A09=E13, A10=E17, A11=E10, A12=E05, A13=M01, A14=M06, A15=M07, A16=M03, A17=M04, A18=M15, A19=M13, A20=M16; B01=E20, B02=E19, B03=E07, B04=E18, B05=E16, B06=E14, B07=E15, B08=E09, B09=M02, B10=M05, B11=M08, B12=M09, B13=M10, B14=M11, B15=M12, B16=M14, B17=M17, B18=M18, B19=M19, B20=M20, B21=M21.

- **Market:** [Grand View US eyewear](https://www.grandviewresearch.com/industry-analysis/us-eyewear-market-report), [Grand View sunglasses](https://www.grandviewresearch.com/industry-analysis/sunglasses-market), [Grand View leather goods](https://www.grandviewresearch.com/industry-analysis/leather-goods-market), [Statista accessories](https://www.statista.com/outlook/cmo/accessories/bags-accessories/united-states), Grips: [luggage & bags](https://gripsintelligence.com/insights/industries/luggage-bags), [premium travel gear](https://gripsintelligence.com/insights/industries/luggage-bags/premium-travel-gear), [travel bags](https://gripsintelligence.com/insights/industries/luggage-bags/travel-bags-and-accessories), [leather handbags](https://gripsintelligence.com/insights/industries/luggage-bags/leather-handbags-and-accessories), [apparel & accessories](https://gripsintelligence.com/insights/industries/apparel-accessories), [slim wallets](https://gripsintelligence.com/insights/industries/apparel-accessories/slim-and-minimalist-wallets), [handcrafted leather](https://gripsintelligence.com/insights/industries/apparel-accessories/handcrafted-leather-goods), [fashion handbags](https://gripsintelligence.com/insights/industries/apparel-accessories/fashion-handbags-and-accessories), [eyewear](https://gripsintelligence.com/insights/industries/apparel-accessories/eyewear), [sunglasses](https://gripsintelligence.com/insights/industries/apparel-accessories/sunglasses).
- **Creative benchmarks:** Benly [handbags & leather goods](https://benly.ai/benchmarks/q1-2026/fashion-apparel/handbags-leather-goods), [jewelry & accessories](https://benly.ai/benchmarks/q1-2026/fashion-apparel/jewelry-accessories), [travel & hospitality](https://benly.ai/benchmarks/q1-2026/travel-hospitality), [fashion & apparel](https://benly.ai/benchmarks/q1-2026/fashion-apparel).
- **Ad libraries:** Motion brand pages for [The Ridge](https://www.motionapp.com/library/the-ridge), [Ekster](https://www.motionapp.com/library/ekster), [goodr](https://www.motionapp.com/library/goodr), [Shady Rays](https://www.motionapp.com/library/shady-rays), [Monos](https://www.motionapp.com/library/monos), [July](https://www.motionapp.com/library/july), [Portland Leather Goods](https://www.motionapp.com/library/portland-leather-goods), [Bellroy](https://www.motionapp.com/library/bellroy), [Warby Parker](https://www.motionapp.com/library/warby-parker), [Felix Gray](https://www.motionapp.com/library/felix-gray), [Away](https://www.motionapp.com/library/away), [BÉIS](https://www.motionapp.com/library/beis), [Dagne Dover](https://www.motionapp.com/library/dagne-dover), [Cuyana](https://www.motionapp.com/library/cuyana), [Solgaard](https://www.motionapp.com/library/solgaard), [Peak Design](https://www.motionapp.com/library/peak-design), [Roka](https://www.motionapp.com/library/roka), [Baggu](https://www.motionapp.com/library/baggu), [Quince](https://www.motionapp.com/library/quince); trending [accessories](https://www.motionapp.com/trending/accessories/) and [travel](https://www.motionapp.com/trending/travel/).
- **Law and policy:** [16 CFR 24.0](https://www.law.cornell.edu/cfr/text/16/24.0) and [24.2](https://www.law.cornell.edu/cfr/text/16/24.2) (Leather Guides), [21 CFR 801.410](https://www.law.cornell.edu/cfr/text/21/801.410) (impact-resistant lenses), [FTC Made in USA](https://www.ftc.gov/business-guidance/resources/complying-made-usa-standard), [AAO on blue light](https://www.aao.org/eye-health/tips-prevention/should-you-be-worried-about-blue-light), [Meta ad standards (third-party IP, health & wellness)](https://transparency.meta.com/policies/ad-standards/). Hermès v. Rothschild, the 2024 Eyeglass Rule amendment, ANSI Z80.3, TikTok contact-lens rules and TSA lock wording are marked [unverified] above — the web-search budget for this run was exhausted before they could be fetched from primary sources.
- Builds on docs 11, 41, 42, 43, 44, 45, 46, 48, 51, 52, 56 in this folder and `research/ai-video-reels/lab/LESSONS.md`.
