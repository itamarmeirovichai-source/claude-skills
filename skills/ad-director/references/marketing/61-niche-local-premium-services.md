# 61 — Niche deep-dive: local premium businesses (restaurants, hotels, real-estate developers, med-spas, gyms; US + Israel)

Researched 2026-10-09. No generation money was spent. Nobody was contacted. Nothing was sent.

**What this adds.** Docs 47–59 cover physical DTC products. This doc covers a different kind of buyer: a **business tied to a place**, where "the product" is a room, a dish, a treatment, a class or an apartment that may not exist yet. It does **not** change VXO's direction (LESSONS, 2026-10-09). It answers one question: *when a local premium business asks for a VXO film (Short / Premiere / Season), what sells, what is legal, what AI must never do, and which of these buyers are worth answering?* It adds:
- 26 posts downloaded and measured (TikTok) from 17 accounts, metadata for 389 posts from 52 handles, and paid-ad structure from 19 Motion public ad-library pages (Meta);
- the market map from primary filings (Planet Fitness, Xponential, Life Time 10-Ks), the National Restaurant Association, AmSpa, and Globes for Israeli housing;
- the rules that bite here and nowhere else in our docs: the Fair Housing Act ad clause and Meta's housing Special Ad Category, the FTC fee rule for hotel prices (16 CFR 464), the FTC fake-reviews rule, the 18+ rule for cosmetic procedures, alcohol, medical advertising in Israel, and "render vs reality" for off-plan property;
- the buyer by sub-niche, re-buy triggers, a lead-scoring add-on and a sample DM;
- 10 concepts (3 marked best) and 10 insights.

It builds on 41 (action realism), 42 (teardown method), 43 (models, prices, templates), 44 (comedy craft), 45 (what sells, policy), 46 (sound and QC), 47 (beauty: faces and results), 49 (food), and the LESSONS file.

**Labels.**
- **[m]** = I measured it from the downloaded file: scene cuts with ffmpeg `select='gt(scene,0.3)'`, 2 fps frame tiles that I looked at, a 0.5 s RMS envelope with onset detection (librosa), integrated LUFS and sample peak (`ebur128`), and a faster-whisper transcript.
- **[c]** = the company's own claim or filing. **[v]** = a vendor or third-party figure (directional). **[inf]** = my inference. **[unverified]** = no primary evidence found in this run.

**Method and limits.**
- **Web search was unavailable for this run** (the shared search budget was already used up). Every web source here was fetched directly from a known URL: SEC EDGAR, restaurant.org, americanmedspa.org, ftc.gov, fda.gov, transparency.meta.com, Cornell LII, Globes, and Motion. Facts I would normally confirm by search are marked **[unverified]**, and §11 lists them for a follow-up run.
- **TikTok.** I harvested recent and pinned video IDs from public embed pages (`tiktok.com/embed/@handle`) for ~100 candidate handles. 52 returned IDs; I dropped the ones that turned out to be unrelated accounts (e.g. `pendry` is an Indonesian motorbike account, `danhotels` is a Saudi hotel, not Israel's Dan Hotels). I pulled metadata for 389 posts and downloaded 26 to `scratchpad/niche2/local/L01…L26/` (all succeeded). No media is committed.
- **Independent venues are hard to find without search.** Guessable handles skew to chains and famous names (Hilton, Equinox, Nobu, Salt Bae, Serhant). Where I have independents (TMPL, Papi Steak, Levain, PUBLIC, Sweat440, Fattal in Israel) I say so. The patterns transfer; the reach numbers of chains do not.
- **Paid vs organic.** As in docs 47–59: millions of views with a like rate under ~1 % is the paid (Spark Ads) signature; ≥3 % is an organic hit. A flag, not a fact.
- **Meta.** The Meta Ad Library returns 403 to automated fetches (docs 51–59), so I used **Motion's public library pages** as a ~June 2026 snapshot ("refreshed 4 months ago"). Pages exist for Equinox, Solidcore, F45, Planet Fitness, Club Pilates, ClassPass, LaserAway, Ideal Image, Hilton, Marriott Bonvoy, Airbnb, Vrbo, OpenTable, Resy, Sweetgreen, Levain, Compass, Zillow. No page for Barry's, Orangetheory, Life Time, SkinSpirit, Hydrafacial, Graduate, 1 Hotels, PUBLIC, Nobu, Papi, Serhant, The Agency, TMPL (404).
- **Israel** sources are thin in this run (no search): Globes English (two September 2026 articles), Fattal Hotels' TikTok, and law I know by name but could not fetch (marked [unverified]).
- **Two-year window:** Oct 2024 – Oct 2026. 24 of 26 measured posts fall inside it; two (L08 May 2025 is inside; L26 Dec 2025 inside) — all are inside except none; the older all-time winners found in metadata (LaserAway 29.4M, 2022; OTF 2.2M, 2022; The Agency 1.8M, 2023) are cited from metadata only and marked "older".

---

## 0. The ten things to know before a local premium business gets a VXO film

1. **"It looks like AI" is now a complaint hotels must answer.** Graduate Hotels (Hilton) ran a polished campaign in August–September 2026: its biggest post has **19.7M views** (paid signature, 0.05 % likes) [m]. The comments called it AI, so Graduate posted **two behind-the-scenes replies**: "POV: our hotel background is so immaculate that the internet thinks it's an AI prompt" (replying to "this is literally ai you guys we are so doomed"), **1.4M views**, and "When your hotel looks too good to be real, you have to drop the raw BTS footage" (replying to "Can't they just pay an actor $50 and use AI…?"), **784K** [m]. **For a place people will visit, the room, the dish and the view must be real.** AI that replaces the venue is a misrepresentation risk *and* a trust risk (§5, §6.2).
2. **So the best use of AI in this niche is the thing that does not exist yet.** "Coming soon" and "Now open" are the shared ad of the whole niche: Equinox ("COMING SOON", "EQUINOX PLAYA VISTA", founding-member rate locks), Planet Fitness ("COMING SOON TO CRYSTAL RIVER", "$1 Down" pre-opening), Solidcore ("LEAWOOD IS COMING", founder's memberships), Sweetgreen ("NOW OPEN AT UNIVERSITY TOWN CENTER") [Motion]. PUBLIC West Hollywood's pre-opening teaser is Ian Schrager's voice over **renders** and an archival film clip, because the rooms were not finished [m]. Off-plan apartments, unopened hotels, gyms in pre-sale and restaurants under construction **cannot be filmed**; VXO can animate the architect's approved renders and build the world around them, labelled as a visualisation.
3. **Personality beats production.** The biggest posts in the set are a person, not a place: Salt Bae carving at a hillside table (**31.1M**, 4.5 % likes, one handheld take) [m]; Ryan Serhant's office prank (**30.5M**, 9.2 % likes, 87K shares) [m]; Nobu Matsuhisa telling the black-cod story himself (272K, 5.8 % likes, a 170 s post) [m]. A local premium film should carry the **founder's or chef's real voice and real hands**; AI builds the world around them.
4. **Premium operators spend little on media; the openers and franchises spend a lot.** Life Time (185+ "athletic country clubs", ~1.6M members) spent **$38.0M on marketing on $3.0B revenue in 2025 (≈1.3 %)** [c, 10-K]. Planet Fitness and its franchisees spent **"over $360 million combined in 2025"**: 2 % of dues to a national fund ($98.1M) plus a **7 % local-advertising requirement** (6 % from 2026) [c, 10-K]. Xponential's brand funds spent **$40.5M** (2 % of franchisee sales) [c]. **The money in local premium sits with openings, franchise locals and developers, not with established luxury venues**, which run on word of mouth.
5. **The paid libraries are offer-led and image-led.** Compass: **188 new creatives/week, 0 of 20 recent ads are video** ("JUST LISTED", "NEW PRICE"); Marriott Bonvoy: 946 active, 0/20 video; Hilton: 730 active, 6/20 video; Ideal Image 2/20 video; Planet Fitness 377 active, 39 % "offer-first banner" [Motion]. The creative gap is real, but the buyer is used to cheap statics: **sell a film plus a stills pack**, not a film alone.
6. **Hospitality has a reusable 10-second format.** Hilton's "**Is this the treehouse of your dreams IRL? …or is this HILTON?**" series: a question super over a surprising real image, a brand answer at ~3.5 s, a location pin, a logo at ~8 s. Three of its posts reached **9.6M, 3.2M and 970K** (paid) [m]. It is a template a boutique hotel, restaurant or developer can own with its own wording.
7. **Fitness wins with members as performers.** TMPL's "This is our official audition to be your new gym" (a dancer doing *A Chorus Line* through every zone of the club) hit **17.15 % likes** on 312K views [m]; Orangetheory's coach-as-flight-attendant skit and Anytime Fitness' "seeing the same guy no matter what" are 8–10 s one-takes [m]. **Gyms should be shown with real people in the real club; AI only for the impossible beat or the pre-opening shell.**
8. **Med-spas are the most dangerous AI client VXO can take.** The niche's proof is faces, needles and results (LaserAway's CoolSculpting one-take, 1.9M; Ideal Image's unit-count explainer; SkinSpirit's injector "everything I've done to my face at 33") [m]. Meta requires cosmetic-procedure ads to target 18+ ([Meta Ad Standards](https://transparency.meta.com/policies/ad-standards/)), the FTC bans fake or AI testimonials ([FTC, Aug 2024](https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials)), and AI-generated results would be a deceptive demonstration (doc 47). **AI never shows a face that was "treated".** Tell the story through objects, devices, calendars and rituals (concept C6).
9. **Real estate has its own law.** The Fair Housing Act bans any ad that "indicates any preference, limitation, or discrimination" by race, colour, religion, sex, handicap, familial status or national origin ([42 USC 3604(c)](https://www.law.cornell.edu/uscode/text/42/3604)), and US housing ads on Meta must run as a **Special Ad Category** with limited targeting ([Meta Ad Standards](https://transparency.meta.com/policies/ad-standards/)). **AI "residents" are a fair-housing risk**: who you generate is a statement of who you prefer. Off-plan renders must match the approved plans (floor count, view, orientation, finishes), or they become the misleading-ad evidence in a buyer's lawsuit [inf].
10. **Israel is a developer market under pressure.** Globes (Sep 2026): developers are **renting out unsold new homes rather than cutting prices** (e.g. 78 of 113 units in a Bat Yam tower leased for ten years) and the southern district alone had **10,788 unsold new homes at end-June 2026** (11,457 counting 669 cancelled deals) ([Globes 23 Sep](https://en.globes.co.il/en/article-developers-rent-unsold-homes-to-avoid-price-cuts-1001557092); [Globes 27 Sep](https://en.globes.co.il/en/article-buyers-cancelling-deals-yet-building-starts-still-growing-in-south-1001557644)). Units are marketed through **project-marketing firms**, Yad2, Facebook groups and WhatsApp. That firm, not the developer, is often the buyer (§6.1).

---

## 1. Market map

### 1.1 Size and growth

| Sub-niche | Measure | Figure | Source | Note |
|---|---|---|---|---|
| **Restaurants (US)** | 2026 sales | **$1.55T projected; real growth +1.3 %; 15.8M employees (+~100K)** | [National Restaurant Association](https://restaurant.org/research-and-media/research/research-reports/state-of-the-industry/) [c] | Operators plan to "invest in more technology that boosts efficiency and strengthens guest connections" |
| Restaurants (US) | Fine dining / premium share | — | **[unverified]** | Not in the free page |
| **Med-spas (US)** | Industry revenue | **"$17B+", growing "more than $1 billion per year"** | [AmSpa](https://americanmedspa.org/resources/med-spa-statistics) [v] | The free page gives no location count; ~10,000+ locations and ~$1.4–1.6M average revenue per location are commonly quoted from earlier AmSpa reports **[unverified]** |
| **Gyms, mass (US)** | Planet Fitness 2025 | **Revenue $1.3B; system-wide sales $5.3B; ~20.8M members; 2,896 clubs; mature-club AUV ~$2.0M; 4-wall EBITDA ~42.7 %** | [PLNT 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1637207/000163720726000011/plnt-20251231.htm) [c] | "Member joins are typically higher in January" |
| **Gyms, boutique (US)** | Xponential (Club Pilates, Pure Barre, YogaSix, StretchLab…) | **Revenue $314.9M; ~774K members (704K paying, +5 %); 59.2M visits (+12 %); marketing funds spent $40.5M** | [XPOF 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1802156/000180215626000016/xpof-20251231.htm) [c] | Typical studio 1,500–1,800 sq ft; "comprehensive pre-opening support, including membership sales" |
| **Gyms, premium (US)** | Life Time | **Revenue $2.995B (+$374M); ~1.6M members, ~873K memberships; 185+ clubs; marketing $38.0M** | [LTH 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1869198/000186919826000010/lth-20251231.htm) [c] | Must "escrow funds received from pre-opening sales or post a bond" in some states |
| **Hotels** | US hotel revenue / boutique share | — | **[unverified]** | Not fetched in this run |
| **Real estate, Israel** | Unsold new homes, southern district | **10,788 (end-Jun 2026); 669 cancelled deals; building starts exceed sales by ~11,000** | [Globes](https://en.globes.co.il/en/article-buyers-cancelling-deals-yet-building-starts-still-growing-in-south-1001557644) citing CBS | National unsold inventory **[unverified]** |
| Real estate, Israel | Developer behaviour | **Renting unsold units to avoid price cuts; marketing via Yad2, Facebook groups, WhatsApp; project-marketing firms (e.g. Dara Project Marketing)** | [Globes](https://en.globes.co.il/en/article-developers-rent-unsold-homes-to-avoid-price-cuts-1001557092) | "Avoid price cuts partly to protect the project's reputation" |
| Real estate, US | New-construction / condo pre-sales | — | **[unverified]** | Not fetched |

**Read [inf]:** these are big, slow-growing, local markets. The marketing money concentrates at three moments: **an opening** (gyms pre-sell, hotels and restaurants "premiere"), **a sales push on inventory** (developers, hotels in low season), and **a recurring calendar** (January for gyms, holidays for restaurants and hotels, pre-summer for med-spas). VXO's product film fits the first two best.

### 1.2 Fit by sub-niche (the honest verdict)

| Sub-niche | Typical creative budget per asset [inf] | What AI can legitimately do | What AI must not do | VXO fit |
|---|---|---|---|---|
| **Real-estate developers (US luxury condos; Israel)** | High: projects already pay for renders, animations, sales galleries and print **[unverified amounts]** | Animate approved renders; build the lifestyle world, the view, the light through the day; a comedic hook | Change the floor count, view, finishes or orientation; generate "residents" with implied demographics | ★★★ best fit |
| **Hotels — pre-opening, boutique, resort** | Medium–high at opening; low otherwise | Pre-opening world from renders; the impossible hook (a bed rolling out, a sound gag); destination fantasy beats | Replace real rooms after opening; show a view the room doesn't have; show a nightly price without total-price fees | ★★★ at opening, ★★ after |
| **Gyms — independent premium and pre-sale** | Medium; franchisees have mandated local budgets but brand-locked creative | Pre-opening shell, founder-rate countdown, the impossible beat | Fake transformations; fake members; results claims | ★★ (independents, pre-sale) |
| **Restaurants — openings, groups, signature dishes** | Low–medium (most use creators and phones) | A hook world around the real dish; the opening teaser; a sound gag | Generate the food that is sold; fake crowds or reviews | ★★ openings and groups only |
| **Med-spas** | Medium (high ad spend, offer-led) | Device and mechanism inserts, objects, calendars, the clinic world without faces | Faces, skin, needles, results, testimonials | ★ only with strict limits |

### 1.3 The 30 businesses (reference list, public data only; NOT a lead list)

Sizes are **[unverified]** unless sourced. "TT median" = median views of the latest posts I sampled [m]. These are mostly chains and famous names (see Method); the VXO target band is the **founder-led, single- to ten-location operator** that resembles them.

| # | Business | Sub-niche | Founder-led? | Size band | Signals seen | Use for VXO |
|---|---|---|---|---|---|---|
| 1 | **TMPL** (NYC) | Premium gym | Yes [unverified] | 1–5 clubs | TT median 408; 312K "audition" at 17 % likes | ★ format reference: members as performers |
| 2 | **Sweat440** | Boutique HIIT franchise | Yes [unverified] | $10–50M system | TT median 687 | Franchise; local owners |
| 3 | **Solidcore** | Reformer HIIT | PE-owned | $100M+ | Meta 80 active, ~7/wk; "LEAWOOD IS COMING", founder's memberships | Pre-opening pattern |
| 4 | **Barry's** | Boutique HIIT | PE-owned | $100M+ | TT median 2,452; "6-pack summer sale"; All Stars challenge | Calendar pattern |
| 5 | **Equinox** | Luxury gym | Private | $1B+ | Meta 46 active, ~22/wk; "COMING SOON", founding rate locks, "The Equinox Sale" | Opening pattern |
| 6 | **Life Time** | Premium club | Public | $3.0B | Marketing 1.3 % of revenue [c] | Shows premium ≠ big media |
| 7 | **Planet Fitness** franchisees | Mass gym | Franchise | AUV ~$2.0M/club | $1 Down, "COMING SOON TO…"; 7 %→6 % local ad requirement | Budget exists; creative brand-locked |
| 8 | **Orangetheory** | Boutique franchise | Franchise | $1B+ system | TT 2.2M (older); coach skits | Format reference |
| 9 | **Club Pilates** (Xponential) | Reformer franchise | Franchise | — | "TRY A FREE INTRO CLASS" on most ads | Offer reference |
| 10 | **Anytime Fitness** locations | Franchise | Franchise | — | Location-made relatable posts | Format reference |
| 11 | **Papi Steak** (Miami/Vegas) | Steakhouse | Yes (David Einhorn) [unverified] | 1–5 venues | TT median 18,550; 156K "quiet desserts" | ★ sound/spectacle reference |
| 12 | **Nusr-Et (Salt Bae)** | Steakhouse group | Yes | $100M+ [unverified] | TT median 1.3M; 31.1M one-take | Personality reference |
| 13 | **Nobu** | Restaurant + hotel group | Yes (chef) | $500M+ [unverified] | 272K origin story told by the chef | Founder-voice reference |
| 14 | **Levain Bakery** | Bakery (NYC → national) | Yes | $50M+ [unverified] | Meta 60 active, ~5/wk; LTO "4 DAYS ONLY"; 1.76 % share rate on the latte build | ★ LTO cadence = Season plan |
| 15 | **Magnolia Bakery** | Bakery | — | — | Seasonal LTOs (Biscoff, Pumpkin) | Calendar reference |
| 16 | **Katz's Deli** | Legacy restaurant | Family | — | TT median 984 | — |
| 17 | **Peter Luger / Joe's Pizza / J.G. Melon** | NYC legacy | Family | — | Little brand TikTok | Don't need ads |
| 18 | **PUBLIC Hotels** (Ian Schrager) | Lifestyle hotel | Yes (Schrager) | 2–3 hotels | Pre-opening WeHo teasers, 58–61K | ★ pre-opening reference |
| 19 | **Graduate (by Hilton)** | Collegiate boutique hotels | Hilton-owned | — | 19.7M paid oath film; "it's AI" replies | ★ the AI-suspicion case |
| 20 | **1 Hotels** | Eco-luxury hotels | SH Hotels | — | Paid creator interviews 284K | — |
| 21 | **Ace Hotel** | Lifestyle hotels | Private | — | TT median 2,294 | — |
| 22 | **Hilton** | Hotel chain | Public | — | "…or is this Hilton?" 9.6M/3.2M/970K; Meta 730 active | Format reference |
| 23 | **Fattal Hotels** (Israel) | Hotel chain | Family | — | TT median 538; "from ₪99 a night", Kinneret couples | Israel tone reference |
| 24 | **Ocean House** (RI) | Independent resort | Private | 1–2 hotels | Seasonal posts | Independent example |
| 25 | **LaserAway** | Med-spa chain | PE-owned | $100M+ | Meta 59 active, ~15/wk, 15/20 video, "70 % OFF"; 29.4M (2022) and 1.9M CoolSculpting | Offer/demo reference |
| 26 | **Ideal Image** | Med-spa chain | PE-owned | — | 2/20 video; "BARE IT ALL BY SPRING", "BLACK FRIDAY AFTERPARTY" | Calendar reference |
| 27 | **SkinSpirit / Heyday / GlowBar / Hydrafacial** | Med-spa / facials | Mixed | — | Injector-led education; Heyday influencer programme; GlowBar founder story (Greek franchise) | Founder-voice reference |
| 28 | **Serhant / Ryan Serhant** | Brokerage + founder | Yes | — | Founder TT median 71.6K; 30.5M prank | Personality reference |
| 29 | **The Agency / Compass** | Brokerage | — | — | 1.3M listing walk-through; Compass 188 new statics/week | Listing-tour reference |
| 30 | **Sobha Realty** (Dubai) | Developer | Founder-led | $1B+ | FPV-to-handover film (492 views) | Developer-film reference |

### 1.4 Price bands (what the buyer sells, and what a film must return)

| Sub-niche | Ticket | Film economics [inf] |
|---|---|---|
| Restaurant | $40–250 per cover; LTO items $7–20 (Levain latte) | A $1,200 Short needs ~10–30 covers or one private event to pay back. Only groups, openings and destination venues will pay |
| Hotel | $150–1,000+ a night; ₪99+ a night in Israeli chain promotions (Fattal) | One direct booking saves the OTA commission (typically 15–25 % **[unverified]**). A film that sells a *direct-only* perk has a GM-friendly ROI |
| Gym | $15–25/mo (PF) → $200–300+/mo (Equinox, TMPL **[unverified]**); founder rates pre-opening | A member at $200/mo × 12–24 months = $2.4–4.8K LTV; **one member ≈ one Short** |
| Med-spa | $300–1,500 per treatment; repeat every 3–4 months for neuromodulators | High patient LTV; most ads run "70 % off"/"free package" offers (LaserAway) |
| Developer (US) | $500K–$10M+ per unit | One extra sale pays for years of films |
| Developer (Israel) | ₪1.5–5M+ per apartment **[unverified]** | Same; the buyer is the project-marketing firm or the developer's marketing manager |

### 1.5 Seasonality calendar (US + Israel)

| Month | Restaurants | Hotels | Gyms | Med-spas | Developers |
|---|---|---|---|---|---|
| **Jan** | Restaurant Week (NYC late Jan) **[unverified dates]** | US "wave season" for summer bookings; Israel winter breaks | **The peak: "member joins are typically higher in January"** (PF 10-K); Life Time "greater membership growth at the beginning of the year" | New-year resets | Israel: post-holiday launch window |
| **Feb** | Valentine's Day (the biggest single night **[unverified]**) | Valentine's packages | Retention | Valentine's glow | US spring selling season starts |
| **Mar–Apr** | Passover (Israel: hotels and restaurants Pesach packages) | **Pesach** is Israel's top hotel week; spring break US | Pre-summer | **"BARE IT ALL BY SPRING"** (Ideal Image), laser and body contouring push | Spring launches |
| **May–Jun** | Mother's / Father's Day; patios | Summer bookings | Summer packs (F45 "10-class pack", Barry's "6-pack summer sale") | "Summer ready" (LaserAway CoolSculpting "just in time for summer") | — |
| **Jul–Aug** | Summer | **Israel peak (August)**; US peak | Pre-fall challenges (OTF "Hit Your Stride") | Slow | Israel: slow summer |
| **Sep–Oct** | Fall menus (Magnolia Biscoff/Pumpkin LTOs) | **Israel: Rosh Hashana → Sukkot** (Fattal "₪99" promo, Kinneret couples); US fall foliage | Back-to-routine; club anniversaries (Equinox "35 clubs in 1 day") | Fall facials | **Israel: post-holiday sales push** (now) |
| **Nov** | Thanksgiving; holiday party bookings | Black Friday room sales | Black Friday | **"BLACK FRIDAY AFTERPARTY"** (Ideal Image) | Year-end promotions |
| **Dec** | Holiday parties, NYE | NYE, Hanukkah | **Pitch window for January** | Holiday glow, gift cards | — |

**Today (2026-10-09):** the right moment to pitch **gyms for January pre-sales and openings**, **hotels and restaurants for holiday/NYE and Q1 openings**, **med-spas for Black Friday/holiday gift cards**, and **Israeli developers for the post-holiday sales push**.

### 1.6 Where they advertise

- **Meta (all five):** high-volume, offer-led, mostly images. Hilton 730 active ads, ~60/wk, "Cinematic B-Roll 26 %, Montage 22 %, Offer-First Banner 22 %"; Marriott Bonvoy 946, 0/20 video; Compass 222 active, **188 new/wk**, "Split Screen 40 %", 0/20 video; Planet Fitness 377, "Offer-First Banner 39 %"; LaserAway 59, "Demo 49 %", 15/20 video; Equinox 46, "Headline 47 %"; Solidcore 80; ClassPass 462 [Motion]. Housing ads must use the Special Ad Category in the US ([Meta](https://transparency.meta.com/policies/ad-standards/)).
- **TikTok/Instagram (organic + Spark):** personality-led accounts dominate (Salt Bae, Serhant, Nobu); chains pay to boost hospitality reels (Hilton, Graduate); gyms post member skits; injectors post education [m].
- **Creators as media:** hotels pay creators for stays and interviews (1 Hotels × a musician, 284K, paid signature) [m]; restaurants are reviewed by local food creators for free.
- **Google Search, Maps, OpenTable/Resy, booking engines and OTAs** carry most local intent **[inf]**. OpenTable's own Meta ads pitch restaurants on "AI search visibility" [Motion].
- **Israel:** Yad2, Facebook groups, WhatsApp, Instagram, project-marketing firms, outdoor signage at the site (Globes; [inf]).

---

## 2. Teardowns: 26 measured posts plus Meta library structure

Cut rate = shots ÷ duration. Hook = what is on screen and in the audio in second 1. LUFS / peak are as published (TikTok re-encode). Like rate = likes ÷ views; share rate = shares ÷ views.

### 2.1 The 20 strongest, full teardown [m]

| # | Post | Date · views · likes · shares | Length · shots · shots/s · LUFS / peak | Shot list (timecodes) | Second 1 (hook) | Turn / punchline | Product interaction | Sound | Text / CTA | Why it sold |
|---|---|---|---|---|---|---|---|---|---|---|
| L01 | **Salt Bae "Çıtır çıtır"** ([link](https://www.tiktok.com/@nusr_et/video/7672820723857050898)) | 2026-08-11 · **31.1M** · 4.5 % · 57.5K | 25.0 s · 1 · 0.04 · −22.2 / −6.3 | One handheld take at a candle-lit hillside table at night, city lights below: 0–4 he leans over a seared rib roast and starts slicing; 4–8 close on two rosy slices laid out; 8–12 a crisp fat cap peeled off with tongs; 12–18 the bone section carved and held up to lens, he smiles; 18–23 the signature elbow-salt pour, arm raised; 23–25 slicing again | Knife already moving into a crust | The elbow-salt pose (the brand's own meme) | The dish is the whole film | Room sound and crust crackle ("çıtır" = crunchy); 3.2 onsets/s | Hashtags only | **A ritual the audience already knows, performed again, on the real meat.** No cut, no music; the person *is* the brand |
| L08 | **Ryan Serhant "giving my boss random objects"** ([link](https://www.tiktok.com/@ryanserhant/video/7506951442171694378)) | 2025-05-21 · **30.5M** · **9.2 %** · **87K** | 57.9 s · 8 · 0.14 · −30.3 / −5.5 | 0–5.3 staff hands him a tennis ball mid-talk; 5.3–14.6 on stage at a company event, hands behind his back accepting a vial; 14.6–25 in a meeting, a lip balm; 25–35 in the car, a hand sanitiser and a red object; 35–47 a skyscraper corridor, on the phone, accepting more; 47–57.9 in a barber chair, still accepting | Super "Giving my boss random objects to see if he'll accept them" | "The way he just accepts it in the last one" | None (the brand is the CEO) | Ambient + talk, quiet (−30 LUFS) | — | **A founder with a running gag.** Brokerage brand-building runs on the founder's personality; listings are a separate, static channel (Compass) |
| L04 | **Graduate Hotels "college move-in oath"** ([link](https://www.tiktok.com/@graduatehotels/video/7675822813306965262)) | 2026-08-19 · **19.7M** · 0.05 % (paid) · 548 | 30.0 s · 2 · 0.07 · −26.4 / −7.3 | 0–26.6 one locked-off tripod medium: a man with a large moustache, glasses and bow tie at a library desk, left hand on a "Graduate Hotels" book, right hand raised, reading an oath; 22.7 super "WE ARE ALL STUDENTS"; 26.6–30 end card "Order of the Stay" bookcase → "Graduate by Hilton · Drop in anytime" | "We will now take the college move-in oath. Repeat after me." | "I will check in on my family. I will check in to Graduate. I am now a student." | The book prop; the brand is the hotel | Clean VO, word-by-word kinetic captions | Word captions; end card | **Deadpan character + a ritual (an oath) + a seasonal moment (move-in).** The closest thing in the set to Otto's register. The "check in" pun is caused by the product (a hotel) |
| L02 | **Hilton "rolling beds"** ([link](https://www.tiktok.com/@hilton/video/7688018187031448863)) | 2026-09-21 · **9.6M** · 0.29 % (paid) · 1.5K | 10.4 s · 1 · 0.10 · −24.7 / −12.1 | One locked-off wide on a treehouse deck: 0–3.5 a woman sits at the deck edge as a made-up bed **rolls out of the room on rails** toward her; 3.5–8.5 a man climbs in, they settle; 8.5–10.4 logo fades in | Super "Is this the treehouse of your dreams IRL?" over a bed already moving | "…or is this HILTON?" at 3.5 s; pin "La Valise Tulum, an SLH Hotel" | The room's real gimmick (a rolling bed) | Licensed-feel bed track, 4.7 onsets/s | "Hilton · For the stay · Discover new ways to stay" | **Question → brand answer.** One impossible-looking but real feature, held in a single frame |
| L03 | **Hilton "lava tunnel restaurant"** ([link](https://www.tiktok.com/@hilton/video/7691063297075891486)) | 2026-09-29 · **3.2M** · 0.44 % (paid) · 590 | 9.6 s · 6 · 0.62 · −22.1 / −9.0 | 0–1.2 cave mouth, lit stairs descending; 1.2–3.0 a figure with a lantern in a black tunnel; 3.0–3.5 diners at candle-lit tables inside the tube; 3.5–4.7 aerial of villas in green hills + "…or is this HILTON?"; 4.7–6.3 snorkeller in a fish school; 6.3–7.0 sea turtle; 7.0–7.5 poolside lounger; 7.5–9.6 aerial + logo | Super "Is this the hottest new restaurant?" over a cave mouth | The answer at 3.5 s | Location reveal | Music bed | Pin "Royal Palm Galápagos, Curio Collection" | **Same template, faster cut.** Restaurants as hotel bait |
| L25 | **Hilton "curator's camera roll"** ([link](https://www.tiktok.com/@hilton/video/7689108622063815966)) | 2026-09-24 · 970K · 0.59 % (paid) · 55 | 10.0 s · 15 · 1.5 · −21.8 / −8.2 | 0–4.0 seven 0.3–0.7 s cuts of murals with a woman's back in frame; 4.0–5.7 "…or is this HILTON?" over a suite; 5.7–7 staircase mural, a brass desk bell; 7–8.5 woman outside a brick hotel; 8.5–10 logo | "Is this a curator's camera roll?" | The answer at 4 s | Art = amenity | Music | Pin "The Radical Asheville, Tapestry Collection" | The fastest version (1.5 cuts/s). **Back-of-head talent only: no face to be accused of AI** |
| L09 | **The Agency "$4.4M listing in Studio City"** ([link](https://www.tiktok.com/@theagencyre/video/7514035950473841951)) | 2025-06-09 · **1.3M** · 4.0 % · **7.4K (0.57 %)** | 59.4 s · 1 (walk-through with whip transitions) · −12.9 / −4.0 | Gimbal follow of the agent from the front lawn, through the door, living room, backyard and pool, kitchen, pantry, theatre, stairs, primary suite, closet, bath, guest rooms; he gestures but never speaks | Agent striding up the path to the door | — (the house is the payoff) | Every room touched or pointed at | Licensed pop track ("As It Was"), well mastered | Price in caption | **The listing tour is the format of real estate**: one continuous path, a guide's back, a song. High share rate = "send to partner" |
| L10 | **Serhant "coolest NYC apartment"** ([link](https://www.tiktok.com/@serhant/video/7693318477335121165)) | 2026-10-05 · 347K · **8.0 %** · 1.7K | 17.1 s · 12 · 0.70 · −16.6 / −5.4 | 0–4.8 handheld from the street: tilt-up and push in on a small red-brick corner house; 4.8–15.8 ten ~1 s interior beats cut to a vocal track: dining room, library, living room, stairs, fireplace wall, bedroom, fireplace, window seat; 15.8–17.1 roof terrace | Super over the exterior: wondering what the inside of that little house looks like | The 1 s reveal rhythm | — | Trending vocal ("Quench") | Super | **Curiosity hook (street → inside).** The house is an "oddity" (a tiny old house among towers) |
| L11 | **TMPL "official audition to be your new gym"** ([link](https://www.tiktok.com/@tmplclubs/video/7538509606356667678)) | 2025-08-14 · 312K · **17.15 %** · 730 | 23.8 s · 7 · 0.29 · −14.6 / −3.7 | 0–4.6 a dancer on the TMPL floor logo hits a *Chorus Line* pose ("five, six, seven, eight!"); 4.6–7 functional zone, a member on a mat behind; 7–9.5 front desk, staff watching; 9.5–11.6 weights floor; 11.6–14.5 lounge; 14.5–18.9 pool deck under a chandelier; 18.9–23.8 the street entrance with gold "TMPL" balloons | The count-in, mid-move | "Did we get it?" (caption) | **Every zone of the club shown as a set** | Musical-theatre track, 152 bpm | Super "This is our official audition to be your new gym" | **A club tour disguised as a performance.** The highest like rate in the set |
| L12 | **Papi Steak "we don't do quiet desserts"** ([link](https://www.tiktok.com/@papisteak/video/7672521972500253983)) | 2026-08-10 · 156K · 0.93 % · 162 | 7.1 s · 3 · 0.42 · −19.4 / −7.4 | 0–1.6 macro: flaming spirit poured from a brass pitcher over a meringue log on a copper tray (super "Baked Alaska — the right way to end the night"); 1.6–5.5 wide: a white-gloved server in a tux ladles blue flame tableside, red-lit bar behind; 5.5–6.2 a cognac decanter pour; 6.2–7.1 the torched meringue cut open | Fire already falling | The cut reveal | The dessert *is* the show | Music; quiet first second (−34 dB) | Super | **Spectacle service** in 7 s. Note that blue alcohol flame is almost invisible in bright light, so the venue is lit dark-red |
| L22 | **Papi Steak "Birkin cocktail"** ([link](https://www.tiktok.com/@papisteak/video/7674012883562286367)) | 2026-08-14 · 28.8K · 0.51 % · 14 | 7.0 s · 6 · 0.85 · −14.8 / −3.1 | Six ~1 s beats: staff dancing at a table; a server in white gloves lifts an orange designer handbag; drinks served from it; a caviar bump on a guest's hand; guests filming with phones | "First Class Service — vegas at its finest" | The handbag as tray | The service ritual | Music | Super | Excess as product. **Uses a named luxury handbag as a prop: trademark risk VXO must not copy** |
| L14 | **Levain "cookie milk latte"** ([link](https://www.tiktok.com/@levainbakery/video/7663511461708270879)) | 2026-07-17 · 101K · 3.8 % · **1.8K (1.76 %)** | 7.7 s · 2 · 0.26 · −17.0 / −6.5 | 0–1.2 a hand holds the finished drink to lens (payoff first); 1.2–7.7 locked-off build on a wooden counter, labelled supers: cookie milk pour ("steeped in our cookies overnight"), espresso, salted cold foam, cookie crumbles | The finished drink | — | The build | Trending track | Layer labels | **The highest share rate in the set.** Payoff → recipe in 7 s, LTO language. Food data from doc 49 holds here |
| L13 | **PUBLIC West Hollywood "premieres October 30th"** ([link](https://www.tiktok.com/@publichotels/video/7691042601671200030)) | 2026-09-29 · 61K · 1.0 % · 22 | 30.3 s · 9 · 0.30 · **−13.5 / +0.8** | 0–6.3 B/W close-up of Ian Schrager ("I always considered myself in the entertainment business"); 6.3–9.4 pool cabana with pop-art mural; 9.4–11.7 night terrace; 11.7–14 the Hollywood sign; 14–16 Schrager; 16–19 warm minimalist room ("we don't even have a TV in the room"); 19–27 the same room with a classic film projected on a wall ("8 by 12 foot screen… projection system we designed"); 27–30 PUBLIC logo | Founder's face and voice | "Every room functions as a private screening room" | The room feature | VO; clipped peak | Supers per phrase | **The founder sells a feature you can't see yet.** The rooms look like **renders**: this is the pre-opening VXO case |
| L17 | **Sobha Realty "Waves Opulence handover"** ([link](https://www.tiktok.com/@sobharealty/video/7686833066874047764)) | 2026-09-18 · 492 · 3.5 % · 0 | 37.2 s · 24 · 0.65 · −26.2 / −8.9 | 0–3.9 FPV dive from cloud level over the city to the tower; 3.9–6.8 drive-up past "Welcome Home" flags; 6.8–12.7 lobby, logo walls; 12.7–17 handover lounge, signs; 17–33 buyers posing with a giant gold key and flowers; 33–35 the welcome gift box opened; 35–37 logo | Falling from the sky | Families with the key | The finished building | Music, 144 bpm | — | **Proof of delivery** for an off-plan market. Low reach on TikTok; built for WhatsApp and sales decks [inf] |
| L18 | **Fattal "₪99 a night" (Israel)** ([link](https://www.tiktok.com/@fattalhotels/video/7681004461568822548)) | 2026-09-02 · 906 · 0.4 % · 1 | 9.7 s · 1 · 0.10 · −16.7 / −1.2 | One handheld take: BTS of a photo shoot in a suite (couple in robes, photographer, light stand); 3 s the man grabs the camera and announces the sale to lens; 9 s the camera is dropped to the floor | "Behind the scenes?" super over a shoot | "Fattal on time — vacations from ₪99 a night, 07.09, limited stock" | The room as backdrop | Hebrew speech | Hebrew supers, date, "limited stock" | **Offer-first, self-aware Israeli tone.** Weak reach; the offer does the work |
| L19 | **Fattal Kinneret couples (Israel)** ([link](https://www.tiktok.com/@fattalhotels/video/7692494709263977749)) | 2026-10-03 · 938 · 1.9 % · 3 | 6.5 s · 5 · 0.77 · −17.3 / −6.0 | 0–1.1 woman in white walking on a pebble shore; 1.1–2 a wooden tour boat; 2–3 couple at the room window; 3–4.2 palms; 4.2–6.5 couple embrace on the shore | Movement on the shore | — | The lake view | "Chill Vibes" track | Super: "send this to whoever owes you a couples' holiday at the Kinneret" | **Send-to-partner hook** in Hebrew; a 6 s loop |
| L20 | **Orangetheory "coach, you're needed in row 12"** ([link](https://www.tiktok.com/@orangetheory/video/7694373744881569038)) | 2026-10-08 · 4.9K · 0.45 % · 6 | 10.2 s · 1 · 0.10 · −14.2 / −2.1 | One locked-off shot of a coach in an aircraft-cabin seat: she hears the announcement, ties her hair, puts on a headset mic, stands and leaves frame | Super "Flight attendant: omg we have an emergency!" + "Is there anyone here who can convince an exhausted person that now is actually the perfect time to go faster?!" | She answers the call | Coach = the product | Music | Supers | **The coach as a superhero, set somewhere else.** A transposition gag (doc 44 §8.3) in one shot |
| L24 | **Anytime Fitness "same guy no matter what"** ([link](https://www.tiktok.com/@anytimefitness/video/7686160465944268062)) | 2026-09-16 · 18.1K · 1.0 % · 26 | 8.0 s · 2 · 0.25 · −14.3 / −3.9 | 0–4.2 a man walks into a club with his bag: "Going to the gym 6 hours later than your normal time"; 4.2–8 an older member on a bike waves: "Seeing the same guy no matter what" | The walk-in | The regular | The community | "How You Like Me Now" | Two supers | **Community as the product.** Made by a franchise location, reposted by the brand |
| L07 | **LaserAway CoolSculpting "3…2…1"** ([link](https://www.tiktok.com/@laseraway/video/7633654902085930254)) | 2026-04-28 · **1.9M** · 1.0 % (paid) · 1.3K | 12.7 s · 1 · 0.08 · **−33.1 / −14.2** | One handheld take: a reclined patient, eyes closed; the clinician (pink gloves) seats the applicator under the chin and adjusts it | Applicator already on the chin | "Section, beautiful" (suction) | The device on the body | Clinician's countdown, very quiet | Caption: "freezes fat cells with little to no downtime" | **The calm procedure is the reassurance.** A real patient, real device, no result shown in the post |
| L26 | **Ideal Image "Nefertiti neck lift"** ([link](https://www.tiktok.com/@idealimage/video/7579286058634988830)) | 2025-12-02 · 2.6K · 2.4 % · 2 | 23.8 s · 6 · 0.25 · −32.2 / −13.0 | 0–8.7 nurse injector to camera, title super; 8.7–11.9 injection into the neck; 11.9–15 jawline; 15–16.7 chin; 16.7–19.9 DAO; 19.9–23.8 back to the injector: "on average… 50 to 100 units of Botox" | "What's included in a Nefertiti neck lift?" | The total units | Real injections | Talking head, quiet | Captions | **Education with numbers.** Uses the "Botox" trademark and a unit count: both are claims a film must not invent |

### 2.2 The other 6 measured posts [m]

| # | Post | Views · like rate | Length · shots · LUFS | What it shows | Lesson |
|---|---|---|---|---|---|
| L05 | Graduate "POV: our hotel background is so immaculate that the internet thinks it's an AI prompt" ([link](https://www.tiktok.com/@graduatehotels/video/7680705191200525582)) | 1.4M · 0.29 % | 11.9 s · 2 · **−42.8 / −26.0** | Hooded "Order of the Stay" extras in blue robes in the lobby, a boom mic in frame; then a handheld walk past the director's monitor across the checkerboard floor | **The AI accusation answered with BTS.** Nearly silent (−42.8 LUFS) |
| L06 | Graduate "When your hotel looks too good to be real" ([link](https://www.tiktok.com/@graduatehotels/video/7681093569846758669)) | 784K · 0.13 % | 14.5 s · slideshow · −24.4 | BTS stills: crew, slate, the oath actor, students on a sofa, the robe | Replying to "Can't they just pay an actor $50 and use AI…?" |
| L15 | Nobu "Why everyone loves Nobu's Black Cod with Miso" ([link](https://www.tiktok.com/@noburestaurants/video/7670959989556530463)) | 272K · 5.8 % · 0.62 % shares | 169.9 s · 32 · −27.2 | The chef tells the 1987 origin (frozen black cod at "25 to 20 cents a pound", three days of marinade) over kitchen B-roll | **Origin story in the founder's own accented English**; organic, long |
| L16 | Equinox "35 clubs, 1 day" ([link](https://www.tiktok.com/@equinox/video/7689248289119603982)) | 7.4K · 2.2 % | 49.4 s · 45 · 0.91 · −14.9 / **+0.1** | A member visits 35 NYC clubs in one day for the 35th anniversary; one ~1 s beat per club | Anniversary stunt; clipped audio |
| L21 | 1 Hotels × Izzy Escobar rapid-fire ([link](https://www.tiktok.com/@1hotels/video/7692181628042415391)) | 284K · 0.05 % (paid) | 72.4 s · 5 · −14.7 / **+1.7** | A paid musician interview in a suite before Austin City Limits | Event tie-in; clipped peak |
| L23 | SkinSpirit "everything I've done to my face at 33" ([link](https://www.tiktok.com/@skinspirit/video/7690721025889258783)) | 8.2K · 1.5 % | 90.4 s · 1 · −22.7 | An injector talks over her own photo at 23 vs now, listing filler and Botox | The med-spa's real proof is a staff member's own face and history; AI cannot do this |

### 2.3 Paid structure from the Meta libraries (Motion, ~June 2026) [v]

| Business | Active · new/wk | Top formats | Offer / hook pattern | Recent 20: video / image |
|---|---|---|---|---|
| **Hilton** | 730 · ~60 | Cinematic B-Roll 26 %, Montage 22 %, Offer-First Banner 22 % | "The Hilton sale", up to 20–25 % off for Honors; join-free loyalty | 6 / 14 |
| **Marriott Bonvoy** | 946 · ~60 | Headline 38 %, Montage 13 %, Offer-First 13 % | Pet-friendly stays, repeated obsessively | 0 / 20 |
| **Equinox** | 46 · ~22 | Headline 47 %, Montage 22 %, Cinematic B-Roll 18 % | **New club openings (Playa Vista, King West) with founding-member rate locks**; "The Equinox Sale" (waived initiation) | 7 / 13 |
| **Planet Fitness** | 377 · ~57 | Offer-First Banner 39 %, Montage 15 % | **"$1 Down"; "COMING SOON TO [town]"** pre-opening in Florida | 5 / 15 |
| **Solidcore** | 80 · ~7 | Headline 26 %, Offer-First 24 %, Montage 16 % | "TWO WEEKS, UNLIMITED CLASSES", **"LEAWOOD IS COMING"**, founder's memberships | 8 / 12 |
| **F45** | 61 · ~6 | Montage 29 %, Collage 12 % | "TRAIN AROUND YOUR SUMMER — 10-CLASS PACK" | 7 / 13 |
| **Club Pilates** | 28 · ~3 | Offer-First 36 %, Headline 29 %, Statistic 21 % | "TRY A FREE INTRO CLASS" on nearly all | 5 / 5 |
| **ClassPass** | 462 · ~15 | Montage 22 %, Demo 13 % | "get 2 weeks free" | 13 / 7 |
| **LaserAway** | 59 · ~15 | **Demo 49 %**, Offer-First 14 %, Testimonial 10 % | "70 % OFF", "Free Package", CoolSculpting 50 % off | 15 / 5 |
| **Ideal Image** | — | — | "BARE IT ALL BY SPRING", "BLACK FRIDAY AFTERPARTY", "MEDICAL-GRADE FACIALS" | 2 / 18 |
| **Sweetgreen** | 41 · ~15 | Montage 23 %, Demo 20 % | Wraps launch; **"NOW OPEN AT [mall]"** | 17 / 3 |
| **Levain Bakery** | 60 · ~5 | Demo 25 %, Unboxing 17 % | Free shipping, gifting, rotating LTO cookies | 5 / 15 |
| **Compass** | 222 · **~188** | Split Screen 40 %, Offer-First 13 % | "JUST LISTED", "NEW PRICE", "JUST SOLD BY" (agent statics) | **0 / 20** |
| **Zillow** | 123 · ~18 | Screen Recording 16 % | Agent recruitment | 9 / 11 |
| **Resy / OpenTable** | 43 / 137 | Montage 62 % (Resy) | B2B to restaurants ("Put your menu on the map with AI search") + diners (birthdays) | 17/3 · 7/13 |

### 2.4 What the measured set says [m]

- **One take or one-second beats, nothing in between.** 9 of 26 posts are effectively single shots (L01, L02, L04, L07, L09, L18, L20, L23, and L05's first half); the montages run at ~1 cut/s (L10 0.70, L16 0.91, L25 1.5). The median is 0.25 shots/s. **A VXO local film should pick one: a held one-take (VXO's signature) or a beat-cut tour, not a slow cinematic montage.**
- **The paid hospitality signature is a question super.** L02, L03 and L25 all open with "Is this…?" over motion already happening, answer at 3.5–4.0 s, and end on a logo at ~8.5 s.
- **Shares come from "send to partner" content:** listing tours (The Agency 0.57 %), the latte build (1.76 %), Nobu's story (0.62 %), Serhant's tiny house (0.49 %). Hotel paid posts get almost no shares (0.00–0.02 %).
- **The highest like rates are people performing in the real place:** TMPL 17.15 %, Serhant 9.2 %/8.0 %, Nobu 5.8 %, Salt Bae 4.5 %.
- **Faces carry risk both ways.** The Graduate actor was accused of being AI; Hilton's posts show backs of heads (L25), couples at a distance (L02) or no people at all (L03).
- **Audio is broken at both ends:** six posts below −24 LUFS (Graduate BTS −42.8, LaserAway −33.1, Ideal Image −32.2, Serhant −30.3, Nobu −27.2, Graduate oath −26.4) and three clipping above 0 dBFS (1 Hotels +1.7, PUBLIC +0.8, Equinox +0.1).
- **No AI-generated venue ad appeared in the set.** The only AI in the data is an *accusation* (L05, L06). The likeliest AI-assisted footage is PUBLIC's room renders (L13) and possibly Sobha's FPV opener (L17) [inf, unverified].

---

## 3. What converts in this niche (with data)

| Question | Evidence | Answer [inf] |
|---|---|---|
| **Formats** | Hotel paid reels: question super → reveal (L02, L03, L25); listing tours (L09); club "audition" tours (L11); spectacle service (L12, L22); recipe builds (L14); founder stories (L13, L15); offers (Fattal, PF "$1 Down") | Three formats to sell: **(1) the question-reveal 10 s**, **(2) the tour / audition one-take**, **(3) the pre-opening founder teaser** |
| **Proof types** | Real venue footage; founder face/voice; handover photos with families (L17); injector's own face (L23); BTS when accused of AI (L05) | The proof is **the real place, the real founder, the real customer**. VXO keeps a proof slot for all three |
| **Claims** | Room features ("8 by 12 foot screen"), prices ("₪99"), units ("50 to 100 units"), outcomes ("freezes fat cells") | Every on-screen number is the client's, sourced; prices show the total (16 CFR 464) |
| **Offers** | Founding-member rates, "$1 Down", free intro class, 2 weeks free, 70 % off, "from ₪99", "4 DAYS ONLY" | Offer-first banners dominate paid libraries; every film needs an **editable offer card** |
| **Length** | Paid hotel reels 9–10 s; restaurant spectacle 7 s; listing tours ~60 s; founder stories 30–170 s | Deliver **8–10 s**, **15 s** and a **30 s founder cut** |
| **Placements** | Meta Reels/Stories (paid), TikTok Spark, Instagram organic; Israel: WhatsApp and Facebook groups | Make 9:16 first, 4:5 and 1:1 for feed and WhatsApp; a 16:9 cut for the sales-gallery screen (developers) |
| **UGC vs cinematic** | Hilton = cinematic B-roll 26 %; gyms and med-spas = member/staff UGC; developers = renders + drone | **Cinematic for places that are sold as fantasy (hotels, developers); UGC-real for community products (gyms, med-spas)** |
| **AI performance and disclosure** | No measured AI venue ads; Graduate's "AI" accusations at 1.4M and 784K views; Motion survey of 380+ DTC marketers: video-generation tools score **5.2/10** satisfaction ([Motion, Nov 2025](https://motionapp.com/thumbstop-pulse/ai-divide)) | Use AI where nothing can be filmed; disclose; keep the real venue real |

### 3.1 Answers by sub-niche [inf from §2]

- **Restaurants:** sell the **ritual of one signature item** (Salt Bae's carving, Papi's flaming dessert, Nobu's cod, Levain's latte) in 7–10 s, with a payoff-first opener. AI's job: a hook world around the real dish (a sound gag, a deadpan room), never the dish.
- **Hotels:** sell **one unexpected feature** with a question super. AI's job: pre-opening worlds from renders, and the impossible hook; after opening, real footage of real rooms.
- **Developers:** sell **the view, the light and the life** of an unbuilt home, then **proof of delivery** (handovers, construction milestones). AI's job: animate approved renders, show the day's light, build the comedic hook; label "visualisation".
- **Gyms:** sell **community and belonging** with members as performers, and **urgency** pre-opening. AI's job: the pre-opening shell and the countdown.
- **Med-spas:** sell **trust and education** through the injector's real face and the device's real use. AI's job: objects, mechanisms, calendars and clinic worlds without faces.

---

## 4. AI realism pitfalls specific to this niche, and the fixes

| Pitfall | Why it happens | Fix (consistent with doc 43) |
|---|---|---|
| **The venue drifts** (window count, ceiling height, furniture, view change between shots) | Each shot reinvents the room | Every shot from **the client's real photo or approved render via Kling 3.0 Pro i2v** (keeps details from the image, doc 43 §1); "Location, as-is from the reference" (doc 43 §0 rule 3); one statics plate per room |
| **A tower's floor count or façade changes** | Video models redraw architecture | Write "EXACTLY 22 floors, exactly 4 balconies per floor on this face"; check the count frame by frame at 2 fps; keep the building small or cropped in frame |
| **Wrong view or orientation** (sea out of a north-facing window; sun setting on the wrong side) | Models choose the prettiest light | Put the compass bearing and the time of day in the prompt ("windows face 250° WSW; sun low, from frame-right at 18:30"); match to the architect's sun study |
| **Invented skyline** (fake Tel Aviv or Miami towers) | The model hallucinates a city | Use a real photo plate from the client's site or a licensed plate; never let the model invent a real city's skyline |
| **Food lies** (steak doneness changes between cuts, a sauce defies viscosity, steam from a cold dish) | Food physics is weakly learned (doc 49) | The dish is real footage; AI never renders the food being sold. If a prop dish appears in a gag, name its state ("medium-rare, pink centre 55 °C, the same slices in every shot") |
| **Flame looks fake** | Models love orange fire | Flambé alcohol burns **blue and almost invisible in daylight**; write "pale blue flame, visible only in the dark room, 10–20 cm tall, dies in 5–8 s" |
| **Restaurant crowds morph** (cloned diners, extra hands, cutlery fusing) | Many subjects (doc 43: >3 characters glitch) | Shallow depth of field; background diners as soft shapes; ≤3 readable people per shot; "background guests out of focus, no readable faces" |
| **Gym mirrors** reflect the wrong thing, or the crew | Gyms are walls of mirrors | Shoot at 30–45° to the mirror; "no camera or crew in any reflection"; check every mirror frame in QC |
| **Gym equipment physics** (barbells bend, plate numbers garble, cables float, reformer springs disconnected) | Rigid objects as adjectives (doc 43 §5) | "Rigid steel bar, 20 kg, does not bend"; plates unreadable or from a real photo; name each spring's anchor; keep weights moving at real speed (a squat ≈ 2–3 s per rep) |
| **Pool water** (caustics wrong, splash too slow) | Fluid sim | Real footage for the pool; in a gag, write the splash height (a cannonball by an 80 kg adult: 2–3 m spray, falls in ~1.2 s) |
| **Hotel beds and linens** (sheets clip through bodies, pillows multiply) | Cloth sim | Count pillows ("exactly four pillows"); "the duvet drapes, doesn't clip" |
| **Signage and menus** garbled | Video models redraw text (doc 43) | All readable text in post; "all signage unreadable"; the logo from the real photo only |
| **AI people as residents, members or patients** | Generated faces | Backs, hands, wides; licensed or consenting real people; **never** AI faces for med-spa outcomes; for housing, no demographic "preference" signals (§5) |
| **Construction sites** (cranes with impossible booms, scaffolding scale, no PPE) | Weak domain knowledge | Real site photo as the plate; "tower crane, one jib, counter-jib with concrete counterweights; workers in hard hats and hi-vis vests; guardrails at 1.1 m on the slab edge" |
| **"Too good to be real"** (the Graduate effect) | Over-polished light and skin | Real grain, imperfect practicals, a little handheld; keep the founder and BTS footage in the cut; **show the real place at least once** |

### 4.1 Model per shot type (consistent with doc 43 §1)

| Shot type in this niche | First choice | Settings | Why |
|---|---|---|---|
| **Animate an approved render or venue photo** (room, façade, lobby) | Kling 3.0 Pro i2v | 5 s, sound off, `cfg_scale` 0.5, `last_image_url` for a landing frame | Keeps details from the image; one move per shot |
| **Pre-opening hero one-take** (dolly through a render) | Cinema Studio 4.0 | `camera_movement:"dolly-in"`, `pacing:"single-shot"`, 720p | Retains constraints; camera as a parameter |
| **Multi-shot comedic hook in a venue** (hotel corridor, dining room, gym floor) | Seedance 2.5 r2v | 10–15 s, 4–7 shots, location plate as a reference, `generate_audio:true` | Multi-angle coverage with the location held |
| **Light-through-the-day / sun study** | Kling 3.0 i2v first+last frame (morning still → evening still) | 5–10 s | Start and end frames fix the light path |
| **Drone / FPV establishing over a real site** | Real drone footage first; Seedance 2.5 i2v from a real aerial still if needed | Tight; no traffic; "the camera never passes through glass" | Wide aerials over traffic fail (doc 43 rule 4) |
| **Founder talking** | **Real footage** (Wan 3.0 r2v lip-sync only for an animated mascot) | — | The founder's voice is the proof (L13, L15) |
| **Food, drink, dish** | **Real footage**; Kling insert for a prop | — | Food is the claim (doc 49) |
| **Device / mechanism insert** (cryo applicator, reformer spring, smart lock) | Kling 3.0 Pro i2v from a real product photo | 5 s | Label and shape preserved |
| **Previs / blocking** | Wan 3.0 480p | $0.05/s, seed | Cheapest |

---

## 5. Policy and legal

### 5.1 US law and self-regulation

- **FTC Act §5 (deceptive ads) and demonstrations.** A visual that misrepresents the room, view, dish or result is deceptive regardless of a "dramatization" label (doc 47; Dyson v. Dreame, LESSONS).
- **FTC rule on fake reviews and testimonials (announced Aug 14, 2024).** Bans fake reviews and testimonials, explicitly including **"AI-generated fake reviews"**, paying for reviews with a particular sentiment, undisclosed insider reviews (officers, managers, employees), company-controlled "independent" review sites, review suppression by threats, and buying fake followers or views ([FTC](https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials)). **No AI diner, guest, member or patient may "say" anything in a VXO film.** Staff on camera must be disclosed as staff if they praise the place.
- **FTC fee rule, 16 CFR 464 (short-term lodging and live events).** Any advertised price must disclose **"the total price"** clearly and conspicuously and **"more prominently than any other pricing information"** ([16 CFR 464.2](https://www.law.cornell.edu/cfr/text/16/464.2)); effective May 2025 **[unverified date]**. **A hotel film that shows "$199/night" must show the total including resort fees.**
- **Fair Housing Act §804(c).** Unlawful to publish any ad "that indicates any preference, limitation, or discrimination" by protected class ([42 USC 3604(c)](https://www.law.cornell.edu/uscode/text/42/3604)). HUD's long-standing advertising guidance treats the human models shown as part of the message **[unverified current status of the guidance]**. **VXO rule for developer films:** no AI-generated residents in close-up; if people appear, they are backs/hands/wides or licensed real people, and the cast is never one demographic by design; no "perfect for young couples", "exclusive", "Christian community", "no kids" language; include the Equal Housing Opportunity logo where the client requires it.
- **Off-plan sales.** Renders and animations become part of the sales representation. US condo statutes and contracts usually say renderings are illustrative **[unverified by state]**. **VXO rule:** every animated render comes from the client's approved renders, the floor count, view, finishes and orientation are checked against plans, and a "Visualisation — for illustration only; final design may differ" super appears.
- **Medical aesthetics.** Neuromodulators (Botox, Dysport, Xeomin, Jeuveau) and fillers are prescription products and brand names are trademarks; FDA is cracking down on drug ads that omit risk information and on undisclosed influencer promotion (FDA, **Sep 9, 2025**: "thousands of letters" and "approximately 100 cease-and-desist letters") ([FDA](https://www.fda.gov/news-events/press-announcements/fda-launches-crackdown-deceptive-drug-advertising)). State medical boards regulate med-spa advertising and supervision **[unverified per state]**. **VXO rule:** no drug brand names, unit counts, prices per unit or outcome visuals unless the client's medical director supplies and approves them; no "painless", "no downtime", "permanent" supers.
- **Gyms.** State auto-renewal laws apply to memberships; the FTC's federal "click-to-cancel" rule was vacated by the 8th Circuit in July 2025 **[unverified]**. Offers like "$1 Down" need the recurring price and terms nearby (PF does this in its landing pages [inf]). No transformation claims ("lose 10 kg in 30 days") and no before/after bodies (Meta prohibits ads that imply negative self-perception for weight-loss and health products, [Meta](https://transparency.meta.com/policies/ad-standards/)).
- **Alcohol (restaurants, hotel bars).** Ads referencing alcohol must follow local law and age-targeting; **minimum 18** on Meta, 21+ in practice in the US [Meta; inf]. Never show drinking and driving, excess, or anyone who looks under 25 **[industry code, unverified]**.
- **AI disclosure.** Meta "AI info" and TikTok AIGC labels (doc 45 §5.3). New York's synthetic-performer ad disclosure law (signed Dec 2025) **[unverified details]** applies if an AI human appears. **VXO rule for this niche: AI people are avoided; where they appear, disclose.**
- **IP.** No named luxury goods as props (L22's handbag), no licensed film clips (L13 used an archival film, licensed or owned by the client **[unverified]**), no famous chefs, no real hotel brand trade dress, no Hollywood-sign-style trademarks (the Hollywood Sign is a registered trademark **[unverified]**).

### 5.2 Israel [mostly unverified in this run; confirm with Israeli counsel before any Israeli client film]

- **Consumer Protection Law, 1981, §7 (misleading advertising)** covers property ads, including visualisations ("הדמיה") **[unverified enforcement details]**. Developers commonly add "ההדמיה להמחשה בלבד" (the visualisation is for illustration only); VXO should treat that as a minimum, not a shield.
- **Sale (Apartments) Law, 1973** governs the specification ("מפרט") a buyer receives; a film that shows finishes beyond the specification is risky [inf].
- **Physicians' advertising rules** (under the Physicians Ordinance and its advertising regulations) restrict medical advertising, including testimonials and before/after material **[unverified exact rules]**. **Default: no before/after, no testimonials, no outcome visuals for Israeli clinics.**
- **Alcohol advertising** is restricted by the Restriction on Advertising and Marketing of Alcoholic Beverages Law, 2012 (warnings, limits on imagery) **[unverified details]**.
- **Hebrew copy and holidays.** Supers and VO in Hebrew need a native check; dates by both calendars when the client uses them (Fattal: "07.09.26") [m].
- **Wartime sensitivity.** Safe rooms (ממ"ד), sirens and military imagery are not comedy props [inf].

### 5.3 Platform rules

| Topic | Meta | TikTok | VXO action |
|---|---|---|---|
| **Housing ads** | US advertisers must self-identify as a **Special Ad Category**; restricted targeting ([Meta](https://transparency.meta.com/policies/ad-standards/)) | Housing ads restricted in targeting **[unverified]** | Deliver creative that works without demographic targeting: broad, place-led |
| **Cosmetic procedures** | Must target **18+** | Restricted; 18+ **[unverified]** | Age-gate; no results |
| **Weight loss / health** | 18+; no negative self-perception | Same **[unverified]** | No body-shaming hooks for gyms or med-spas |
| **Alcohol** | Local law + age; never under 18 | Restricted by region | Age-gate restaurant cuts with alcohol; make an alcohol-free cut |
| **Personal attributes** | Ads "must not contain content that asserts or implies personal attributes" | Similar | No "Are you overweight?" or "Tired of your wrinkles?" |
| **AI labels** | "AI info" | AIGC label | Doc 45 §5.3 |

### 5.4 Age gates

Med-spa and cosmetic: 18+. Alcohol: 18+ minimum on Meta, 21+ in the US cut. Gyms and weight: 18+ for weight-loss angles. Hotels, restaurants (no alcohol), developers: none.

---

## 6. The buyer

### 6.1 Who signs a $1,200–3,500 film [inf with evidence]

| Sub-niche | Signer | Influencers | Evidence |
|---|---|---|---|
| **Developer (US)** | VP/Director of Marketing or Sales; for boutique developers, the founder | The architect, the sales-gallery broker team, the branding agency | Developers buy renders and branding as projects; the founder appears on camera at handovers (Sobha) |
| **Developer (Israel)** | The developer's marketing manager **or the project-marketing firm** (e.g. Dara Project Marketing in Globes) | Visualisation studio ("משרד הדמיות"), media buyer | Globes: units are marketed through firms, Yad2, Facebook groups and WhatsApp |
| **Hotel (independent / boutique)** | GM or Director of Sales & Marketing; the owner in family hotels | Management company, revenue manager | PUBLIC: the founder is the voice; Graduate: brand team with a production crew |
| **Hotel (pre-opening)** | The pre-opening team / owner's rep | Brand (if flagged), PR agency | "Premieres October 30th" teasers (PUBLIC) |
| **Restaurant group** | Founder/chef-owner or group marketing director | Social agency, PR | Salt Bae, Nobu, Papi Steak (owner-driven) |
| **Gym (independent premium)** | Founder or head of marketing | Head coach, community manager | TMPL, Sweat440 (founder-run brands); pre-sale offers |
| **Gym (franchise)** | Franchisee, inside brand guidelines | Franchisor marketing (approval) | PF 6–7 % local ad requirement; Xponential 2 % fund |
| **Med-spa** | Owner (often a nurse injector, physician or entrepreneur) + the medical director | Marketing agency | Injector-led content (SkinSpirit, Ideal Image) |

### 6.2 What they fear (ranked)

1. **"It will look fake, and guests will say so."** The Graduate replies prove the risk is public and viral [m].
2. **Misrepresentation liability.** Off-plan buyers sue over renders; hotel guests complain about rooms that don't match ads; FTC fee rules on prices.
3. **Medical-board and FTC exposure** (med-spas): testimonials, outcomes, drug names.
4. **Brand-standards violations** (franchisees, flagged hotels).
5. **"My agency / my videographer already does this."** Locals have relationships with photographers who shoot the real place.
6. **Timing.** An opening date is fixed; the pre-sale window is 6–12 weeks.

### 6.3 What proof makes them pay $1,200–3,500

- **5 free frames made from *their* render or photo** (not a generic venue): the façade at golden hour, the room with the morning light, the empty club shell with "founding member" countdown. One frame must be the **hook**, not the pretty shot.
- **A "where AI is used" sheet:** AI only for what can't be filmed yet and for the comedic hook; the real venue, food, founder and customers stay real; renders labelled; no AI people speaking.
- **A claims sheet:** floor count, view, orientation and finishes checked against plans; prices with total fees; no outcome visuals.
- **The asset maths against their alternatives** (renders, a day shoot, a local videographer): one Premiere = a 15 s hero, a 10 s question-reveal, a 6 s loop, a 30 s founder cut built around their own talking-head, 9:16 + 4:5 + 16:9, 8 stills, an editable offer card in English and Hebrew where needed.
- **A calendar fit:** "live 8 weeks before opening", "live for January", "live for the post-holiday sales push".

### 6.4 Re-buy triggers (why they rebook monthly)

1. **Construction milestones** (developers): groundbreaking → topping-out → model unit → handover (Sobha) → each new release of units or price step. About 4–6 film moments per project [inf].
2. **Pre-opening countdown** (hotels, gyms, restaurants): teaser → founding rates → "2 weeks to go" → "Now open" → first-month recap. A natural Season plan for 3 months.
3. **Rotating offers and LTOs:** Levain's "4 DAYS ONLY" lattes and seasonal cookies; Magnolia's fall LTOs; Fattal's "₪99"; LaserAway's monthly specials; Equinox sales. Each needs a re-skinned hook and offer card.
4. **The calendar** (§1.5): January (gyms), Valentine's, Pesach/Easter, summer, Rosh Hashana–Sukkot, Black Friday, NYE.
5. **New outlets and features:** a new rooftop bar, spa, menu, class format, device.
6. **Fatigue:** Hilton and Compass refresh 60–188 creatives a week [Motion]. A local client won't match that, but a monthly hook keeps paid reels from dying.

### 6.5 Best outreach angle

**"You can't film what isn't built yet."** For developers, pre-opening hotels and gyms in pre-sale: "your renders are beautiful stills; we turn them into a 15 s film with a hook, checked against your plans, and keep your founder's voice and the real site as the proof." For open venues, lead with **their own real best moment** (the flaming dessert, the rolling bed) and offer a hook world around it, not a replacement for it.

### 6.6 Sample first DM (never sent; for a boutique developer or pre-opening hotel)

> Hi [first name] — saw the "[project name] coming [season]" post and the new renders of the rooftop. They're the best thing on your page.
>
> I run VXO, a small studio that makes 15–30 s films. I sketched one for you called "Unbuilt": a buyer turns a key in a door standing alone on the bare 22nd-floor slab, and the door opens into your finished living room at sunset. Built only from your approved renders, checked against the plans, labelled as a visualisation, with your real site as the last shot.
>
> Happy to send 5 free frames from your renders. No call needed. Want them?
>
> — [name], VXO

Hebrew version (for an Israeli project-marketing firm; never sent):

> היי [שם], ראיתי את ההדמיות החדשות של [פרויקט] — הגג נראה מעולה.
> אני מ-VXO, סטודיו קטן לסרטונים של 15–30 שניות. יש לי רעיון בשבילכם: קונה מסובב מפתח בדלת שעומדת לבד על רצפת הבטון בקומה 22, והדלת נפתחת לסלון הגמור בשקיעה. הכול רק מההדמיות המאושרות שלכם, בדוק מול התוכניות, עם כיתוב "הדמיה להמחשה בלבד", והאתר האמיתי בשוט האחרון.
> אשמח לשלוח 5 פריימים בחינם מההדמיות. בלי שיחה. מתאים?

(Every fact in the opening must be checked on their public page on the day. Do not mention the competition, unsold units or price cuts in a first message.)

---

## 7. Lead signals: the niche scoring add-on for `.claude/skills/vxo-leads/SKILL.md`

Apply on top of the base 100-point score. The add-on can move a lead by **−30 to +30**; HOT stays ≥ 70 after the add-on. Public pages only. **Note:** the base score's "Shopify launch" check does not apply here; use the opening and project signals below instead.

| Signal | Points | How to check |
|---|---|---|
| **Pre-opening or pre-sale in the next 3–16 weeks**: "coming soon", "premieres [date]", founding-member rates, sales-gallery opening, new project launch | **+10** | Their IG/TikTok/site; Motion headlines ("COMING SOON", "IS COMING"); signage; Israeli project pages |
| **Has renders or an architect's visualisation but no video** of the unbuilt product | +8 | Website, Yad2/project pages, IG grid |
| **Calendar fit** (§1.5): gyms now → January; hotels/restaurants now → NYE and Q1 openings; med-spas now → Black Friday; Israeli developers now → post-holiday push | +5 | Today's date vs §1.5 |
| **Paid activity with 0–25 % video** (Compass/Marriott pattern) | +5 | Motion page or Ad Library (manual) |
| **Founder or chef who is visible and talks** (a voice to build around) | +4 | Their posts; podcasts; press |
| **Milestone just passed or coming** (topping-out, handover, anniversary, new outlet) | +4 | Posts, press |
| **Audio faults** in a public video (peak > −1 dBFS or < −24 LUFS) | +2 | `ebur128` on one post |
| **Independent, 1–10 locations, premium price** (not a chain HQ) | +2 | Locations page |
| **Franchisee inside a brand with locked creative** (PF, OTF, Xponential brands) | −8 | Franchise disclosure; brand guidelines |
| **Med-spa** (any) | −5 (and require medical-director approval before frames) | — |
| **Running outcome, before/after, "painless" or drug-price ads now** | −10 | Their ads |
| **Developer with active buyer lawsuits, cancellations news or a stalled site** | −10 | Press (Globes, The Marker, local news); court records |
| **Venue already accused of misleading photos/renders, or review-gating** | −10 | Reviews, press |
| **Established luxury venue with waitlists and no paid ads** | −8 | No ads in library; "fully booked" posts (they don't need demand) |

**VERY hot in this niche looks like [inf]:** a founder-led boutique developer, hotel or premium gym **6–16 weeks from a launch or opening**, with approved renders and no video, a visible founder, a paid library that is all statics, and a dated offer (founding rates, launch prices). Example: base 66 + pre-opening 10 + renders 8 + calendar 5 + statics 5 = 94.

**Current snapshot (2026-10-09, public data only, NOT a lead list; each needs a dossier per vxo-leads §2b):** PUBLIC West Hollywood (premieres Oct 30; founder voice; renders) — likely has a big agency, a format reference rather than a target; Equinox Playa Vista / King West openings (corporate, agency-led); Planet Fitness Florida pre-openings (franchise, brand-locked). The real targets are the independent equivalents found by searching "coming soon" posts per city (§11).

---

## 8. Ten ready film concepts (invented brands)

Conventions:
- **Brands are invented**; clear names on USPTO (and the Israeli trademark register for Israeli use) before use; no real-brand look-alikes.
- **Otto and Vee are absent** (client-style specs). A "spec version" line says how to recast them for VXO's own reel. C2 and C7 are the most Otto-ready.
- **Every camera position is a real rig:** tripod, slider, dolly on track, Steadicam, gimbal walk, jib, a ceiling-mounted overhead on a C-stand, a corridor dolly, a drone outside the building (never through glass). **The camera never passes through glass, walls or closed doors.** Moving through an *open* doorway on a dolly or Steadicam is allowed.
- **Proof slot:** each concept names the real footage the client supplies (the real room, dish, founder, site). AI never performs the claim.
- **No dialogue on visible lips.** Each film ends with a 2-line VO tagline in a locked voice over a frame with no visible lips, plus the logo card and an **offer slot**.
- **No AI faces in close-up.** Hands, backs, profiles, wides. No AI residents with implied demographics.
- **Costs** use doc 43 §6 list prices:

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v 15 s: 480p proof $3.09 + 3 × $6.93 at 720p | **$23.88** |
  | Seedance 10 s: $2.06 + 3 × $4.62 | **$15.92** |
  | Kling 3.0 Pro i2v 5 s sound-off, 2 takes | **$0.95** |
  | Cinema Studio 4.0 720p 8 s | **$3.70** |
  | Wan 3.0 480p previs, 15 s | $0.75 |
  | Stills | ≈ $0.30 each |
  | ElevenLabs VO | ≈ $0.10 |

  Totals exclude the client's proof footage.

---

### C1 · HALCYON 22 (boutique residential tower, off-plan) — "Unbuilt" (15 s) ★ BEST 1

- **Idea:** a bare concrete slab on the 22nd floor of a tower under construction. A solid wooden front door stands alone in a steel frame bolted to the slab (a real sales-gallery stunt). A buyer in a hard hat turns a brass key and opens it. Through the doorway: the finished living room at sunset, exactly as in the approved render. She steps through. The door swings shut behind her on its closer. Cut back to the wind and the bare slab, the door alone.
- **Hook (0–1 s):** sound-first. Wind roaring at height, a hard-hat strap flapping, a brass key already turning in the lock in macro, with a heavy *clack*.
- **Punchline (product-caused):** the door is the only finished thing on the floor, and it opens onto the home that will be there. **Without the product (an apartment you can buy before it exists), the joke doesn't exist.**
- **Shots (8, EXACTLY 8 SHOTS AND 7 HARD CUTS):**

| # | Time | Rig | Action |
|---|---|---|---|
| 1 | 0.0–1.0 | Tripod, macro on a 100 mm lens | The key turns in the lock; a thumb with a work glove; dust on the brass |
| 2 | 1.0–3.0 | Tripod, wide, low, from the slab edge behind the guardrail | The door in its frame stands alone; rebar stubs, a tower-crane jib in the sky; the buyer (back to camera) in a hard hat and hi-vis vest |
| 3 | 3.0–4.5 | Handheld over her shoulder | The door swings open inward; warm light spills out onto the concrete |
| 4 | 4.5–7.5 | Steadicam follows her **through the open doorway** (no glass) | The finished living room at sunset (Kling i2v from the approved render), the sea view through the windows |
| 5 | 7.5–9.0 | Tripod, medium, inside the room facing the door | The door closes on its closer; the wind sound cuts to silence |
| 6 | 9.0–11.0 | Slider along the window | Her hand on the sofa back; the sun on the floor at the same angle as the render |
| 7 | 11.0–13.0 | Tripod outside on the slab (the reverse of shot 2) | The door alone on the slab, shut; wind; a worker walks past and doesn't look |
| 8 | 13.0–15.0 | Drone, outside the building, slow pull-back from the 22nd floor | **Proof slot: the client's real site drone footage**; logo + "Visualisation for illustration only" + offer card ("Launch prices until [date]") |

- **Physics check:** 22 floors × 3.2 m ≈ **70 m**; wind there is often 1.5–2× ground speed, so **8–12 m/s gusts**: hair and vest flap, dust streams sideways, the hard-hat strap is buckled. Guardrail top rail ~1.1 m (OSHA 42 in ± 3 in). A solid-core door weighs **25–35 kg**: it opens with a push and a 0.5 s acceleration, and the closer returns it in **3–5 s** with a soft latch. The door frame is **bolted to a steel base plate** (visible bolts), or it would fall. Sunset light inside: low, warm (~2,700–3,000 K), from the window side that **matches the plan's orientation**. Floor count, window count and view are checked against the architect's plans.
- **Audio map:** 0.0 <wind roar, strap flutter>; 0.6 <key clack>; 3.2 <door unlatch, hinge creak>; 4.5 the wind drops 20 dB, <room tone, faint distant sea>; 8.6 <door closer hiss, latch click> → silence; 11.0 <wind returns> abruptly; 13.0 VO (no lips): "Some homes you have to see before they exist. / HALCYON 22 — launch prices until [date]." Music: a single low piano note under shots 4–6 only.
- **Model/template:** shots 4 and 6 Kling 3.0 Pro i2v from the approved render (doc 43 §7.3 Kling variant); shots 1–3, 5, 7 Seedance 2.5 r2v 10 s multi-shot with the slab plate and the door as references (doc 43 §2.1, "EXACTLY N SHOTS"); shot 8 real.
- **Estimated cost:** Seedance 10 s $15.92 + Kling 2 inserts $1.90 + stills $1.50 + VO $0.10 = **≈ $19.40**.
- **Spec version:** Otto in the hard hat (moustache, mouth never visible) turns the key; Vee clicks her one stopwatch when the door closes.

### C2 · THE QUIET MILE (boutique hotel, soundproofed rooms) — "Do Not Disturb" (15 s) ★ BEST 2

- **Idea:** a hotel corridor. A full marching band (drums, brass) marches down it at full volume. In room 412, a guest sleeps. The band passes the door with the "Do Not Disturb" sign. Inside: nothing. A housekeeper opens the door a crack to check on the noise; the band blares in; she closes it; silence.
- **Hook (0–1 s):** sound-first. A bass drum hit and a cymbal crash over a frame already moving (the drumline's feet stepping onto the corridor carpet).
- **Punchline (product-caused):** the contrast is the rooms' real acoustic rating; **the joke needs the product (a quiet room) to work.** The client's STC/acoustic spec is the claim and must be real.
- **Shots (7):**

| # | Time | Rig | Action |
|---|---|---|---|
| 1 | 0.0–1.5 | Dolly at floor height in the corridor, tracking backward | Marching boots and a bass drum enter frame in step |
| 2 | 1.5–3.5 | Tripod, wide down the corridor | The band (backs and hats, no faces readable) fills the hallway |
| 3 | 3.5–5.5 | Tripod inside the room, locked off | A guest asleep (back to camera), clock at 07:12, curtains glowing; the only sound is a faint AC hum |
| 4 | 5.5–7.0 | Tripod in the corridor, close on the door handle | The DND sign swings as the tuba passes |
| 5 | 7.0–9.5 | Tripod in the room facing the door | The door opens 10 cm: a wall of brass blares in; the guest doesn't move (sleeping under the duvet); the door closes; silence |
| 6 | 9.5–12.0 | Slider across the bedside table | **Proof slot: the real room, real bed, real window detail** |
| 7 | 12.0–15.0 | Tripod, the room wide, held | The guest turns over; VO; logo + "Book direct: late checkout included" |

- **Physics check:** a marching band in a corridor is **100–110 dB**; inside a good hotel room with the door shut the claim may be ~30–35 dB (use the client's measured number only). Step cadence ~120 bpm (2 steps/s). The door opening 10 cm leaks a jump of 20–30 dB; the door closer shuts it in ~3 s. The DND sign on a handle swings with a period of ~0.6–0.8 s after a bump. The duvet rises ~1 cm per breath every 4–5 s.
- **Audio map:** 0.0 <bass drum + cymbal>; 0.0–3.5 <band, march at 120 bpm>; 3.5 hard cut to <room tone 30 dB, AC hum>; 5.5 <band muffled, low-passed under 300 Hz>; 7.2 <door unlatch> → full band; 8.8 <door latch> → silence; 12.0 VO (no lips): "Whatever's happening out there, / it isn't happening in here. The Quiet Mile."
- **Model/template:** Seedance 2.5 r2v 15 s, 7 shots, corridor and room plates as references (the client's real rooms photographed); shot 6 real footage. Native audio as the sync guide, then the band track replaced with a cleared march (doc 43 §4 always replace music).
- **Estimated cost:** **≈ $25.90** (Seedance 15 s $23.88 + Kling insert $0.95 + stills $1.00 + VO).
- **Spec version:** Otto leads the band with a mace, deadpan; Vee times the door with the stopwatch.

### C3 · CARRAWAY (fine-dining restaurant) — "The Loudest Thing on the Menu" (10 s) ★ BEST 3

- **Idea:** a hushed, candle-lit dining room. A server sets down a crème brûlée. A guest taps the caramel with a spoon. The crack echoes like a pistol shot. Every head in the room turns. The guest, mid-spoon, freezes.
- **Hook (0–1 s):** motion already happening, then sound: the spoon is already descending in macro; at 0.8 s the **crack**.
- **Punchline (product-caused):** the dessert's real glass-thin caramel is the sound; the room's silence makes it a scandal. The joke requires the product.
- **Shots (6):**

| # | Time | Rig | Action |
|---|---|---|---|
| 1 | 0.0–1.2 | Tripod, 100 mm macro, from table height | Spoon descends, taps the caramel: a clean star crack |
| 2 | 1.2–2.5 | Tripod, wide from the corner, locked off | The room: eight soft-focus tables; every head turns toward the sound (backs and profiles, faces soft) |
| 3 | 2.5–4.0 | Slider, medium on the guest from behind | Her hand frozen with the spoon |
| 4 | 4.0–5.5 | Tripod, close on the server | A tiny nod of approval, gloved hands folded |
| 5 | 5.5–7.5 | Tripod macro, real footage | **Proof slot: the real dessert, the real spoon break, the custard** |
| 6 | 7.5–10.0 | Tripod, wide | The room slowly turns back; one other guest raises a hand to order one; VO + logo |

- **Physics check:** a torched sugar crust is **1–2 mm** thick; one firm tap cracks it into 3–6 shards; the crack is ~65–75 dB at the table and reads as an echo in a quiet (~35–40 dB) room. Human head-turn reaction ~**200–300 ms** after the sound, staggered across tables (not in sync). Candles: flames bend ~5° when the server passes; a ramekin ~9 cm across.
- **Audio map:** 0.0 <room tone, soft cutlery, distant murmur 38 dB>; 0.8 <caramel crack, dry, then a 0.6 s reverb tail> (sweetened, still natural); 1.4 murmur stops dead; 4.2 <one chair creak>; 7.5 murmur returns; 7.8 VO (no lips): "Our loudest dish. / Carraway — book the 9:30." Music: none.
- **Model/template:** Seedance 2.5 r2v 10 s (shots 1–4, 6) with the real dining-room photo as the location reference; shot 5 real. Doc 43 §7.5 comedic reveal (the held reaction is the joke).
- **Estimated cost:** **≈ $17.20**.
- **Spec version:** Otto is the guest (back to camera); Vee the server, stopwatch in her apron.

### C4 · SOLANA HEIGHTS (developer, sea-facing apartments) — "Sun Study" (12 s)

- **Idea:** one apartment interior, locked off, from 7:00 to 19:30. A sunbeam moves across the floor. A cat follows the warm patch all day, room to room, and ends on the balcony at sunset.
- **Hook:** motion in frame 0: the cat already stretching in a beam at dawn.
- **Punchline:** the cat's day *is* the orientation claim ("west-facing living room, sunset balcony"). The product (the apartment's orientation) causes the joke.
- **Shots (6):** (1) tripod, wide living room, 07:00, cat in the beam; (2) the same tripod, 10:00, the beam has moved 45°, the cat moved with it; (3) tripod in the kitchen, 13:00, the cat on a stool in the patch; (4) tripod, 16:00, the cat on the rug; (5) tripod at the balcony door (open), 19:00, the cat on the balcony, the sea at sunset; (6) **real drone of the actual building at sunset (proof)** + logo + "Visualisation".
- **Physics check:** the sun's azimuth moves ~**15° per hour**; shadows lengthen toward evening and always point away from the sun; a west-facing room gets direct sun only after ~13:00 (so the morning beam must come from a different window, per the plan). One cat, ≤5 s per shot, generated from a real photo of a real cat (LESSONS). Window count and frame positions identical in every shot.
- **Audio map:** 0.0 <morning birds, a purr>; per cut a <clock tick> and a shift in ambience (traffic midday, sea evening); 9.5 VO: "It knew where the sun would be. / So do we. Solana Heights."
- **Model/template:** Kling 3.0 i2v from the approved render, first+last frame per time of day (doc 43 §4.1); 5 inserts.
- **Estimated cost:** 5 × $0.95 + stills $1.50 = **≈ $6.35**.

### C5 · FORGE & FOUND (premium gym, pre-sale) — "Founding Members" (15 s)

- **Idea:** an empty construction shell. Workers install the club over weeks; on lunch breaks, they quietly use each machine as it arrives. Opening day: the crew are the first in line with founding-member cards.
- **Hook:** a 16 kg kettlebell set down on bare concrete by a gloved hand: a heavy *clonk* at 0.5 s.
- **Punchline:** the people who built it couldn't wait to train in it (the club's quality causes the joke). Offer card: founding rates.
- **Shots (8):** tripod locked-off in the same corner across "weeks" (1) the shell, kettlebell down; (2) a worker curls it between drilling; (3) rack delivered on a pallet jack; (4) two workers spot each other on a bench, hard hats on; (5) mirror wall installed (camera at 40° to it, nothing reflected); (6) lights on; (7) opening day, the crew in hi-vis queue at the desk; (8) **real footage of the finished club** + founder VO + countdown card.
- **Physics check:** a 16 kg kettlebell curl ~2 s up/2 s down, the forearm strains; a loaded 20 kg bar doesn't bend; pallet jacks move at walking pace ~1 m/s; PPE on every worker; no one lifts with a power tool in hand.
- **Audio map:** 0.5 <kettlebell clonk>; drill bursts at 2.0, 5.5; <pallet jack rattle> 4.5; <lights switch on, hum> 10.0; crowd murmur 11.0; VO 12.5: "Even the builders signed up. / Founding rates end [date]."
- **Model/template:** Seedance 2.5 r2v 15 s with the empty-shell plate (a real photo of the site) and the finished render.
- **Estimated cost:** **≈ $25.40**.

### C6 · ROSEWATER CLINIC (med-spa) — "Ninety Days" (10 s)

- **Idea:** no faces at all. A kitchen counter, locked off: a coffee mug, a phone, a wall calendar. Pages fly, seasons change outside the window, the mug changes from iced coffee to hot cocoa; every 90 days the phone lights with "Rosewater: time for your refresh" and a hand books it.
- **Hook:** the calendar page tears off in frame 0 with a crisp *rip*.
- **Punchline:** the clinic's reminder system and rebooking ritual is the product; the joke is that everything changes except the appointment.
- **Shots (5):** (1) tripod macro, the page rips; (2) tripod wide on the counter, a season passes (window light shifts); (3) phone lights with the reminder; a thumb taps "Book"; (4) repeat for a second season (rule of three, shortened); (5) **real clinic reception footage (proof)** + logo + "Book your next visit".
- **Physics check:** iced coffee shows condensation that runs down in ~30–60 s; cocoa steams only when hot (>60 °C); window light angle lower in winter; the phone screen text added in post.
- **Audio map:** 0.0 <page rip>; 2.0 <phone buzz>; 2.4 <tap>; 5.0 <page rip>; 6.4 <buzz/tap>; 7.5 VO: "Seasons change. / Your face shouldn't have to. Rosewater." (claims-check the line with the medical director; alternative: "Your next visit, on time. Rosewater.")
- **Model/template:** Kling 3.0 i2v ×3; no people.
- **Estimated cost:** **≈ $4.35**.

### C7 · THE LARK (boutique hotel, direct-booking perk) — "11:00" (15 s)

- **Idea:** 10:59 on check-out day. Every door on the corridor bursts open; guests sprint with spinner suitcases. Cut to one guest in a robe reading by the pool. Super: "Booked direct. Check-out 14:00."
- **Hook:** a corridor clock ticks to 10:59 and seven doors open at once.
- **Punchline:** the direct-booking perk (late checkout) causes the calm; the OTA-guests' panic is the joke. Measurable for the GM.
- **Shots (7):** (1) tripod, the corridor clock; (2) dolly down the corridor, doors open, suitcases roll; (3) handheld low on spinner wheels hitting the elevator threshold; (4) tripod, the elevator doors closing on a crush of luggage; (5) cut to the pool, tripod, a robe, a book, a coffee; (6) **real pool footage (proof)**; (7) logo + "Book direct: late checkout" + total price with fees if any price shown.
- **Physics check:** spinner wheels on carpet slow and wobble; on hard floor they glide; a full suitcase is 20–23 kg and swings on turns; elevator doors close in ~3–4 s and re-open on obstruction (show it).
- **Audio map:** 0.0 <clock tick>; 0.6 <seven door latches, overlapping>; 1–6 <wheel rumble, hurried footsteps>; 6.0 <elevator chime>; 6.5 hard cut to <pool ambience, a page turn>; 11.5 VO: "Some guests check out at 11. / Ours finish the chapter. The Lark — book direct."
- **Model/template:** Seedance 2.5 r2v 15 s, corridor + pool plates from the real hotel.
- **Estimated cost:** **≈ $25.40**.
- **Spec version:** Otto in the robe; Vee runs past with her stopwatch.

### C8 · BELLWEATHER (restaurant, waitlist + bar seats) — "Fully Booked" (15 s)

- **Idea:** a man tries to get a table: he offers the host a watch, then a car key, then a live lobster in a box. The host, unmoved, points at the bar: "Four seats, every night, walk-in."
- **Hook:** a watch slides across the host stand in frame 0 (*clink*).
- **Punchline:** the product's real policy (walk-in bar seats) makes the bribes pointless.
- **Shots (6):** (1) macro of the watch sliding; (2) over-the-shoulder wide of the host (back of the man's head); (3) the car key; (4) the lobster box opening, the lobster's antennae waving (one animal, real-photo-based, ≤5 s); (5) the host's gloved hand points; (6) **real bar footage, the four seats, the real dish (proof)** + logo.
- **Physics check:** a lobster moves slowly out of water (antennae flick ~1/s, claws banded); a watch on marble slides ~20 cm and stops; no money on screen (bribery joke stays absurd, not cash).
- **Audio map:** 0.0 <watch clink>; 3.5 <keys jingle>; 6.5 <box lid, lobster click>; 9.5 VO: "No bribes. Four bar seats, every night. / Bellweather."
- **Model/template:** Seedance 2.5 r2v 10 s + real footage.
- **Estimated cost:** **≈ $18.30**.

### C9 · STUDIO VANTAGE (reformer Pilates studio, opening) — "Not a Couch" (10 s)

- **Idea:** in a sleek new studio lobby, a delivery driver flops onto a reformer to rest; the unlocked carriage rolls him gently along the rails across the room and parks him at the instructor's feet. She hands him a free-intro-class card.
- **Hook:** the carriage already rolling with a man on it, rails humming.
- **Punchline:** the product's machine does what it's built to do (glide); the free intro class is the offer.
- **Shots (5):** (1) tripod wide, he sits; (2) low slider along the rail, the carriage glides; (3) tripod close on the springs (unhooked); (4) the instructor's sneakers, the card in her hand; (5) **real class footage (proof)** + "Try a free intro class".
- **Physics check:** an 80 kg adult on a free carriage glides **~1–1.5 m** on a slight push and stops at the stopper with a soft bump; springs visibly unhooked; nobody falls.
- **Audio map:** 0.0 <rail hum>; 2.2 <stopper bump>; 4.0 <card tap>; 6.5 VO: "It's not a couch. / Your first class is free. Studio Vantage."
- **Model/template:** Seedance 2.5 r2v 10 s.
- **Estimated cost:** **≈ $17.20**.

### C10 · KEDEM HOMES (Israeli developer, handover season) — "The Key" (12 s)

- **Idea:** a family receives an oversized ceremonial gold key at a handover (the Sobha ritual). It doesn't fit in the car, the elevator or the door. At the apartment, the father simply taps his phone on the smart lock; the door opens.
- **Hook:** the 1.2 m gold key swung into frame, hitting the car's door frame (*clonk*).
- **Punchline:** the product's real smart-home spec makes the giant key absurd. Bilingual supers (Hebrew/English).
- **Shots (6):** (1) handheld, the key hits the car frame; (2) tripod, the key wedged diagonally across an elevator; (3) tripod, the corridor, the key against the door; (4) macro, the phone tap on the lock, the LED turns green; (5) the family walks in (backs); (6) **real handover photos/footage (proof)** + logo + "Handovers now: [project]".
- **Physics check:** a foam-core prop key ~1.2 m, ~2 kg, flexes slightly when it hits; an elevator car interior ~1.1 × 1.4 m, so a 1.2 m key fits only diagonally; smart lock unlock delay ~0.5–1 s with a motor whirr. Only real features of the project's spec.
- **Audio map:** 0.0 <clonk>; 3.0 <elevator chime>; 6.0 <lock beep + motor whirr>; 8.5 VO (Hebrew, locked voice; English sub): "המפתח הכי גדול שקיבלתם. / והכי פחות נחוץ. קדם." ("The biggest key you've ever been given. / And the least necessary.")
- **Model/template:** Seedance 2.5 r2v 10 s + Kling insert for the lock.
- **Estimated cost:** **≈ $18.30**.

### 8.1 Ranking

1. **C1 "Unbuilt" (HALCYON 22).** Best overall:
   - a sound-first hook and a punchline that only the product (an apartment sold before it exists) can cause;
   - it uses AI exactly where filming is impossible (the unbuilt interior) and keeps the real site as proof;
   - the door-on-a-slab is a real, riggable sales stunt, so every shot passes the crew test;
   - it re-skins for every off-plan project in the US and Israel, and for pre-opening hotels (a door on the unfinished rooftop).
2. **C2 "Do Not Disturb" (THE QUIET MILE).** A clean sound gag that makes an invisible feature audible; works for any hotel with a real acoustic spec; Otto-ready.
3. **C3 "The Loudest Thing on the Menu" (CARRAWAY).** 10 s, cheap, the real dessert as proof; re-skins per signature dish (a crackling crust, a fizzing drink, a sizzling plate).

For a VXO local-premium spec reel, make **C1 + C2 + C3**. C7 is the strongest direct-ROI argument for a hotel GM.

---

## 9. Ten insights nobody asked for

1. **"Looks like AI" is now an insult hotels pay to rebut.** Graduate posted two BTS replies (1.4M and 784K views) to prove its film was real [m]. VXO's pitch for real venues must therefore be the opposite of "we replace your shoot": **we build the impossible hook, your place stays real.** Put a "Where AI is used" line in every local proposal.
2. **Sell the gap between render and reality.** Developers, pre-opening hotels and pre-sale gyms already own approved stills and nothing to film. That is VXO's cleanest local use case: **animate approved renders, checked against plans**, with the real site as proof.
3. **Follow the openings, not the luxury.** Life Time spends 1.3 % of revenue on marketing; Planet Fitness' system spends $360M [c]. Established premium venues rarely need ads; **openings and inventory pushes do.** A local lead list should be built from "coming soon" signals by city.
4. **Franchisees have budgets but no creative freedom.** PF franchisees must spend 6–7 % of dues locally [c], yet creative is brand-controlled. Skip them unless the franchisor approves; target independents.
5. **The question-reveal is a free template.** Hilton's "Is this…? …or is this Hilton?" reached 9.6M/3.2M/970K [m]. A boutique version ("Is this a Tuscan villa? …or is this Haifa?") is cheap, real-footage-friendly and loops at 10 s. Offer it as the Short.
6. **The founder's voice is the moat.** PUBLIC (Schrager), Nobu, Salt Bae and Serhant prove that a real face beats production [m]. Every Premiere in this niche should include a **30 s founder cut** built from the client's own phone footage, with VXO's world as the B-roll.
7. **Israeli developers buy through marketing firms.** Globes names project-marketing firms and WhatsApp as the channel. **One firm = many projects.** For Israel, the outreach target is the firm, with Hebrew supers and a WhatsApp-ready 1:1 cut.
8. **Hotels can measure a film by direct bookings.** A film that sells a direct-only perk (late checkout, breakfast) is judged against OTA commission (often 15–25 % [unverified]), a number every GM knows. It turns "brand video" into ROI.
9. **Med-spas are a trap for AI.** Faces, results, drug names and testimonials are all regulated (FTC, FDA, Meta 18+, state boards; Israeli medical-ad rules). Take med-spa work only as object-and-mechanism films with medical-director sign-off; otherwise decline.
10. **The niche ships broken audio too.** Six of 26 posts sit below −24 LUFS and three clip above 0 dBFS, including 1 Hotels (+1.7), PUBLIC (+0.8) and Equinox (+0.1) [m]. Doc 46's master is a concrete, friendly opener for any venue.

---

## 10. QA gate additions for this niche

Run after doc 44 §10, doc 45 §5.4 and doc 46 §7:

1. **The venue is real:** every room, view, dish and amenity shown as existing is the client's real footage or an **approved render labelled "Visualisation"** (Hebrew: "הדמיה להמחשה בלבד").
2. **Plans check** (developers, pre-opening): floor count, window count, balcony count, view direction and sun angle match the plans; finishes match the specification.
3. **No AI people speaking or praising;** no AI residents in close-up; no implied demographic preference (Fair Housing).
4. **Prices show the total** (16 CFR 464 for lodging); offers carry terms (recurring price, dates).
5. **Med-spa:** no faces "after", no needles in AI, no drug names, unit counts or "painless/no downtime" supers unless supplied and approved by the medical director; 18+ targeting.
6. **Alcohol:** age-gated cut and an alcohol-free cut; nobody under 25 in alcohol scenes.
7. **Mirrors and glass:** no crew or rig in any reflection (gyms, bathrooms, lobbies).
8. **Rigid architecture:** walls, windows and furniture don't drift between shots (2 fps strip).
9. **No real trademarks as props** (handbags, cars, watches, film clips) and no real hotel trade dress.
10. **Israel:** Hebrew copy checked by a native speaker; no wartime imagery as comedy.
11. **Audio master:** −14 LUFS integrated, ≤ −1.0 dBTP on the encoded file (LESSONS).
12. **Deliverables:** 15 s hero, 10 s question-reveal, 6 s loop, 30 s founder cut, 9:16 + 4:5 + 1:1 (WhatsApp) + 16:9 (sales-gallery screen), 8 stills, an editable offer card (EN/HE), a claims sheet and the "Where AI is used" note.

---

## 11. Open items for the next run (search was unavailable)

- Independent "coming soon" venues by city (NYC, LA, Miami, Austin, Tel Aviv): restaurants, boutique hotels, premium gyms, with dates.
- US boutique-hotel and fine-dining market sizes; OTA commission ranges from a primary source.
- AmSpa's latest location count and average revenue; state med-spa advertising rules (CA, TX, FL, NY).
- Israeli law texts: the physicians' advertising regulations, Consumer Protection Authority guidance on property visualisations, and the alcohol advertising law details.
- National Israeli unsold new-home inventory (CBS) and developer marketing budgets; the top project-marketing firms.
- HUD's current position on human models in housing ads; Meta's exact housing Special Ad Category targeting limits.
- Meta Ad Library run lengths for Hilton's "…or is this Hilton?" series and for Equinox opening ads (manual browser check; automated fetch is 403).
- Any measured AI-generated venue ads (hotels, restaurants, developers) with performance data.

---

## Sources

All URLs are inline above. Measured files (not committed): `scratchpad/niche2/local/L01…L26/` with `v.info.json` metadata, and `scratchpad/niche2/local/an/` with `*_tile.jpg` (2 fps frame tiles), `*_stats.txt` (scene cuts at 0.30, LUFS, peak), `audio.txt` (RMS/onsets) and `*_asr.txt` (faster-whisper base.en). Handle harvest and metadata: `scratchpad/niche2/local/ids/` (389 posts, 52 handles before dropping unrelated accounts). Motion pages: `scratchpad/niche2/local/motion/`. Additional sources read:
- **Filings:** [Planet Fitness 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1637207/000163720726000011/plnt-20251231.htm), [Xponential Fitness 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1802156/000180215626000016/xpof-20251231.htm), [Life Time 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1869198/000186919826000010/lth-20251231.htm).
- **Market:** [National Restaurant Association State of the Industry](https://restaurant.org/research-and-media/research/research-reports/state-of-the-industry/), [AmSpa med-spa statistics](https://americanmedspa.org/resources/med-spa-statistics), [Globes: developers rent unsold homes (23 Sep 2026)](https://en.globes.co.il/en/article-developers-rent-unsold-homes-to-avoid-price-cuts-1001557092), [Globes: cancellations and building starts in the south (27 Sep 2026)](https://en.globes.co.il/en/article-buyers-cancelling-deals-yet-building-starts-still-growing-in-south-1001557644), [Motion AI-divide pulse (Nov 2025)](https://motionapp.com/thumbstop-pulse/ai-divide), [Motion creative benchmarks 2026](https://motionapp.com/thumbstop-pulse/creative-benchmarks-2026).
- **Ad libraries (Motion):** [Equinox](https://motionapp.com/library/equinox), [Solidcore](https://motionapp.com/library/solidcore), [F45](https://motionapp.com/library/f45-training), [Planet Fitness](https://motionapp.com/library/planet-fitness), [Club Pilates](https://motionapp.com/library/club-pilates), [ClassPass](https://motionapp.com/library/classpass), [LaserAway](https://motionapp.com/library/laseraway), [Ideal Image](https://motionapp.com/library/ideal-image), [Hilton](https://motionapp.com/library/hilton), [Marriott Bonvoy](https://motionapp.com/library/marriott-bonvoy), [Airbnb](https://motionapp.com/library/airbnb), [Vrbo](https://motionapp.com/library/vrbo), [OpenTable](https://motionapp.com/library/opentable), [Resy](https://motionapp.com/library/resy), [Sweetgreen](https://motionapp.com/library/sweetgreen), [Levain Bakery](https://motionapp.com/library/levain-bakery), [Compass](https://motionapp.com/library/compass), [Zillow](https://motionapp.com/library/zillow).
- **Law and policy:** [FTC final rule on fake reviews and testimonials (Aug 2024)](https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials), [16 CFR 464.2 hidden fees](https://www.law.cornell.edu/cfr/text/16/464.2), [42 USC 3604 (Fair Housing Act)](https://www.law.cornell.edu/uscode/text/42/3604), [Meta Advertising Standards](https://transparency.meta.com/policies/ad-standards/), [FDA crackdown on deceptive drug advertising (Sep 2025)](https://www.fda.gov/news-events/press-announcements/fda-launches-crackdown-deceptive-drug-advertising).
- Builds on docs 41, 42, 43, 44, 45, 46, 47 and 49 in this folder and `research/ai-video-reels/lab/LESSONS.md`.
