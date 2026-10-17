# 60 — Niche deep-dive: e-bikes, scooters and e-rideables, car accessories and car care, outdoor power gear

Researched 2026-10-09. No generation money was spent. Nobody was contacted. Nothing was sent. No media is committed.

**What this adds.** No earlier doc covers this niche. Doc 44 covers *how to film* car chases and stunts (rigs, physics, police grammar); doc 43 §7.1 has the car-chase template; doc 52 covers coolers, fire pits and travel gear. This doc covers the *products*: the people who sell e-bikes, e-scooters, one-wheels, smart helmets and phone mounts; car-care chemicals, microfiber, floor liners, car scents, dash cams, Tesla accessories, truck storage, rooftop tents; and battery power stations, solar kits and robotic mowers. It adds:
- **51 ads downloaded, 50 measured**: 20 brand TikToks and **31 Meta ads that were live or recent** (Motion's public brand pages and this week's *trending* pages for Automotive, Outdoors and Technology), plus YouTube search metadata for 60 more (21 listed in §2.3);
- the market map: tracked online GMV for 18 sub-categories (Grips, Aug 2026), Benly's Meta lifespan data for Automotive and Sports & Recreation, Meta ad volume for 17 brands, Shopify price bands and SKU velocity for 47 stores, 30 brands, a seasonality calendar;
- what converts here, with the evidence;
- the AI realism traps specific to spokes, chains, tyres, water on paint, foam, fluids, screens, LEDs and battery boxes, with prompt fixes tied to doc 43;
- the rules that bite here: e-bike classes and the 750 W federal line, battery-fire standards, helmet test speeds, dangerous-riding ad policy, emissions "defeat device" law, Magnuson-Moss, Made in USA, runtime and capacity claims, car trade dress;
- the buyer, re-buy triggers, a lead-scoring add-on and a sample DM;
- 10 concepts (3 marked best, 1 single best) and 12 insights.

It builds on 41 (action realism), 42 (teardown method), 43 (models, prices, templates), 44 (action and comedy craft), 45 (what sells, policy), 46 (sound and QC), 51, 52, 58 and the LESSONS file.

**Labels.**
- **[m]** = I measured it from the downloaded file: scene cuts with ffmpeg `select='gt(scene,0.3)'`, 2 fps frame tiles that I looked at, a 0.5 s RMS envelope and onset detection (librosa), integrated LUFS and sample peak (`ebur128`), and a faster-whisper transcript.
- **[c]** = the brand's own claim. **[v]** = a vendor or agency figure (directional). **[inf]** = my inference. **[unverified]** = no primary evidence fetched this run.

**Method and limits.**
- **TikTok.** I harvested the newest ~10–13 video IDs from the public embed pages (`tiktok.com/embed/@handle`) of 120 candidate handles. 38 returned posts; many brand handles are wrong, empty or private (Ride1Up's account exists but its embed list is empty). I pulled metadata for 376 posts (358 parsed), ranked them by views and by multiple of the brand's own median, and downloaded the 20 strongest. **The handle `@drift` is not Drift car scents** (it is a Spanish mechanic-meme account; T08 was dropped from the teardowns). Brand-account organic reach in this niche is tiny: **the median post across 358 brand posts has 1,266 views** [m].
- **Meta.** The Meta Ad Library still blocks automated fetches (docs 51–58). **Motion's public pages** carry the real ad files: each brand page (`motionapp.com/library/<brand>`) lists active-ad counts, new creatives per week, format tags and the 20 newest ads with video files (Motion says "refreshed 4 months ago", so read brand pages as a ~June 2026 snapshot); the weekly **trending** pages show the most-saved ads with **days active**. I downloaded 31 Meta videos. Only 17 of my ~70 target brands have a Motion page (sitemap of 2,893 slugs).
- **Paid vs organic.** As in docs 47–58: millions of views with a like rate under ~1 % is the paid-distribution signature (Spark Ads); ≥3 % reads as an organic hit. A flag, not a fact. On Meta, the number of **variants** Motion lists per ad (1–8) is a proxy for how much the brand invested in a concept.
- **YouTube.** Search metadata worked; every download failed ("Sign in to confirm you're not a bot", "Requested format is not available"). Brand YouTube videos with millions of views are almost always TrueView-paid [inf].
- **Web search.** The shared web-search budget for this run was **already exhausted before my first query**. Market and legal facts come from direct fetches of primary pages (Grips Intelligence, Benly, Motion, Cornell LII, CPSC, FTC, TikTok Ads policy) and from Shopify `products.json`. Legal facts I know but could not fetch this run are marked [unverified] with the canonical URL so the owner can check them.
- **Two-year window.** Oct 2024 – Oct 2026. 41 of the 50 measured ads fall inside it. Older ones (2021–2023) are kept only where the brand still pins them as its all-time winners; each is marked "older".
- **Revenue figures** for private brands are third-party estimates or nothing; marked [unverified].

---

## 0. The ten things to know before pitching an e-bike, car-accessory or power-gear brand

1. **The split-line is this niche's native proof.** A strip of blue painter's tape across a dirty surface, the product used on one side, the tape peeled: Chemical Guys "Nonsense" did it in **one unbroken 30.9 s take — 11.4M views, 2.18 % likes, 16.2K shares** [m]; Chemical Guys' current Meta winner on the *trending* page does the same on a door sill and has been **active 72 days** [m]. The Rag Company's "Gauntlet" towel drinks a graduated jug of water nearly dry next to a generic chamois that leaves it full: **10.0M views, 9.05 % likes** [m]. Adam's Polishes let rinse water sheet off a coated hood until the bare paint underneath *draws the Adam's "A" logo*: **8.8 s, one shot, 9.5 % likes** [m]. Every winner is one measurable before/after inside one frame. VXO's rule (LESSONS) holds: **the proof itself stays real footage**; AI builds the world, the gag and the hook around it.
2. **Brand TikTok is dead here; Meta is where the money is.** Median brand post 1,266 views; Lectric's two 6M+ launch posts run at 0.12–0.50 % likes, Chemical Guys' 2026 water-spot gel at 0.48 %, Super73's mascot assembly at 0.27 % — all paid signatures [m]. On Meta the volume is real: **Drift 366 active ads, ~159 new per week; Jackery 291 / 66; Velotric 288 / 35; Chemical Guys 220 / 20; EcoFlow 146 / 70; Unit 1 79 / 37** [v]. Pitch films as **paid-social assets** (Reels/Stories), not organic content.
3. **Offer-first statics dominate, so a film is the gap.** In the 20 newest Meta ads: **Jackery 1 video of 20, EcoFlow 1/20, Trek 1/20, Rad Power Bikes 4/20, Unit 1 4/20, Velotric 5/20, Drift 6/20** [v]. Motion's top tags: EcoFlow "Offer-First Banner" 44 %, Rad 60 % [v]. Benly: automotive Meta creatives are **only 25.6 % video** (−15.8 pp vs the 41.4 % cross-industry average), sports & recreation 26.7 % ([Benly Automotive Q1 2026](https://benly.ai/benchmarks/q1-2026/automotive); [Sports & Recreation](https://benly.ai/benchmarks/q1-2026/sports-recreation)) [v]. A VXO film with a built-in **offer slot** fits how they already sell.
4. **The money is moving.** Tracked online GMV, Aug 2026 ([Grips](https://gripsintelligence.com/insights/industries)) [v]: **e-bikes and accessories $312M in 2025, −20–50 %, forecast +10–20 % in 2026 (+45 % Mar→Aug)**; e-bicycles and trikes $149M, forecast **+20–50 %**; **automotive care $1.03B, forecast +50 %+ (+124 % Mar→Aug)**; automotive interior accessories $245M, conversion **3.5–4.0 %**, forecast +20–50 %; **battery and power solutions $1.12B, +10–20 % and accelerating**; portable power (generators, stations, solar) $354M, +10–20 %; but **dash cams −10–20 %, truck accessories −10–20 %, overlanding gear −20–50 %**. Lead with e-bikes (recovering), car care, interior accessories and power stations.
5. **These are considered purchases: the ad is seen on a phone, the bike is bought on a desktop.** Grips revenue by device: **e-bikes 72 % desktop**, power solutions 66 % desktop, detailing 59 % desktop, but interior accessories 51 % mobile [v]. AOV: e-bikes $600–1,100, power $700–800, Tesla accessories $400–500, detailing $100–200 [v]. A VXO film must survive the week between "saw it" and "bought it": same skeleton as the retargeting cut, a 16:9 version for YouTube/desktop and stills for the PDP [inf].
6. **The mechanism beats the lifestyle.** Super73's look-book montages (6–7 variants each) and Dometic's cinematic CFX5 film are the expensive outliers; the long-lived and most-varianted creatives show *the thing working*: Velotric's one-hand stair carry for a lightweight claim (6 variants), EcoFlow powering an ice-cream cart (5), TentBox latches → tent in "less than 30 seconds" (7), Navimow's no-wire auto-mapping (trending), Unit 1's foam-crush cross-section (live headline) [m][v]. Motion tags "Demo" first at Chemical Guys (36 %), Goal Zero (44 %), TentBox (27 %), Unit 1 (26 %) and Milwaukee (61 %) [v].
7. **Comedy and mascots work in this niche — the Otto/Vee playbook is native here.** Super73's lightning-bolt mascot "Keith" assembling a bike: **5.2M** views (paid) [m]. Quad Lock's motocross riders racing a UTV in **inflatable shark and bee costumes: 24.9 % like rate**, the highest in the whole sample [m]. Chemical Guys' innuendo skit ("When I do it, I use both hands… I make my mother-in-law watch") runs 5 variants, and its 5-minute couple challenge with a phone stopwatch runs 4 [m]. A deadpan character with a product-caused punchline is not off-brand for this buyer.
8. **The picture is the claim, and this niche's claims are numbers.** "Tested at 28 mph" (Unit 1), "fridge for up to 14 days" vs "up to 24 hours" (**two current Jackery ads for the same HP3600 Plus**), "150 miles on a single charge" (Lectric XPedition), "less than 30 seconds" (TentBox) [m]. An AI shot of a range bar, a speed readout, a runtime clock or a crash test **is** that claim (NAD, Dyson v. Dreame, LESSONS). Only the client's tested number, with its conditions, in a proof slot.
9. **Riding and driving are policed, and the rules are physics-shaped.** TikTok ads bar "potentially inappropriate use of dangerous tools, vehicles, or objects" and easily imitated stunts; professional stunts may run only if the safety context is clear, 18+ and possibly "Do not try this at home" ([TikTok Ads policy](https://ads.tiktok.com/help/article/tiktok-ads-policy-violence-and-dangerous-activities)). A federal "low-speed electric bicycle" is **<750 W and <20 mph on the motor alone with a 170 lb rider** ([15 U.S.C. §2085](https://www.law.cornell.edu/uscode/text/15/2085)). Every e-bike shot: helmet on, legal lane, plausible speed, no phone in hand (§5).
10. **AI spectacle without a mechanism flops here.** Mammotion's AI-generated feed gag (a robotic mower "teleporting" through Starry Night, a castle, a vineyard and a golf course): **52K views, 0.43 % likes** [m], while Segway Navimow's plain creator demo of the same category is on this week's *trending* page [m]. Segway's CG-studio teaser for the Xyber Air did 270K at 4.6 % because it teased a real launch [m]. AI must serve the demo, not replace it.

---

## 1. Market map

### 1.1 Size and growth (tracked online GMV, Grips, August 2026) [v]

Grips tracks a panel of retailers' online sales, not the whole market. Use it for direction and comparison, not for TAM.

| Sub-category | 2025 GMV tracked | 2025 vs 2024 | 2026 forecast | Mar→Aug 2026 index | Conv. rate | AOV | Device (revenue) | Retailers tracked |
|---|---|---|---|---|---|---|---|---|
| [Electric bikes and accessories](https://gripsintelligence.com/insights/industries/electronics/electric-bikes-and-accessories) | **$312M** | −20–50 % | **+10–20 %** | **+45 %** | 0.5–1.0 % | $600–700 | **72 % desktop** | 70+ (Aventon, Rad, sixthreezero, Jenson…) |
| [Electric bicycles and trikes](https://gripsintelligence.com/insights/industries/electronics/electric-bicycles-and-trikes) | $149M | −20–50 % | **+20–50 %** | **+71 %** | 0.5–1.0 % | $1,000–1,100 | — | 40+ |
| [Electric motorbikes and bicycles](https://gripsintelligence.com/insights/industries/automotive/electric-motorbikes-and-bicycles) | $28M | −20–50 % | +20–50 % | −13 % | 0.5–1.0 % | $500–600 | — | 10+ |
| [Electric scooters and personal mobility](https://gripsintelligence.com/insights/industries/electronics/electric-scooters-and-personal-mobility) | $75M | −20–50 % | +10–20 % | +2 % | 1.0–1.5 % | $300–400 | 52 % desktop | 20+ |
| [Electric mobility](https://gripsintelligence.com/insights/industries/electronics/electric-mobility) | $102M | −20–50 % | +10–20 % | — | 0.5–1.0 % | $400–500 | — | 40+ |
| [Electric skateboards](https://gripsintelligence.com/insights/industries/electronics/electric-skateboards-and-accessories) | $47M | −20–50 % | +5–10 % | — | 0.5–1.0 % | $200–300 | — | 30+ |
| [Automotive care](https://gripsintelligence.com/insights/industries/automotive/automotive-care) | **$1.03B** | −0–5 % | **+50 %+** | **+124 %** | 1.5–2.0 % | $200–300 | — | 70+ |
| [Automotive detailing supplies](https://gripsintelligence.com/insights/industries/automotive/automotive-detailing-supplies) | $115M | −10–20 % | −5–10 % | −14 % | **2.0–2.5 %** | $100–200 | 59 % desktop | 60+ (Chemical Guys, Griot's, Don't Drive Dirty, Autogeek…) |
| [Automotive accessories](https://gripsintelligence.com/insights/industries/automotive/automotive-accessories) | **$1.35B** | −10–20 % | **+20–50 %** | +4 % | 2.5–3.0 % | $200–300 | — | 70+ |
| [Automotive interior accessories](https://gripsintelligence.com/insights/industries/automotive-supplies/automotive-interior-accessories) | $245M | −5–10 % | +20–50 % | −6 % | **3.5–4.0 %** | $100–200 | **51 % mobile** | 15+ |
| [Automotive protective accessories](https://gripsintelligence.com/insights/industries/automotive-accessories/automotive-protective-accessories) (mats, liners, PPF, tint) | $286M | −5–10 % | +20–50 % | −17 % | 3.0–3.5 % | $100–200 | — | 20+ |
| [Tesla automotive accessories](https://gripsintelligence.com/insights/industries/automotive-accessories/tesla-automotive-accessories) | $20M | −20–50 % | 0–5 % | +12 % | 0.5–1.0 % | $400–500 | — | 15+ |
| [Truck accessories and equipment](https://gripsintelligence.com/insights/industries/automotive-accessories/truck-accessories-and-equipment) | $122M | flat | **−10–20 %** | +41 % | 0.5–1.0 % | $600–700 | — | 15+ |
| [Off-road vehicle accessories](https://gripsintelligence.com/insights/industries/automotive/off-road-vehicle-accessories) | $461M | −20–50 % | −0–5 % | +13 % | 1.0–1.5 % | $400–500 | — | 200+ |
| [Overlanding and off-road adventure gear](https://gripsintelligence.com/insights/industries/outdoor-equipment/overlanding-and-off-road-adventure-gear) | $207M | −10–20 % | **−20–50 %** | — | 1.0–1.5 % | $300–400 | — | 50+ |
| [Dash cameras and accessories](https://gripsintelligence.com/insights/industries/electronics/dash-cameras-and-accessories) | $26M | −5–10 % | **−10–20 %** | −6 % | 0.5–1.0 % | $200–300 | — | 10+ |
| [Battery and power solutions](https://gripsintelligence.com/insights/industries/electronics/battery-and-power-solutions) | **$1.12B** | **+10–20 %** | **+10–20 %, accelerating** | +6 % | 1.5–2.0 % | $300–400 | — | 40+ |
| [Electrical power solutions](https://gripsintelligence.com/insights/industries/electronics/electrical-power-solutions) (generators, stations, solar) | $354M | +5–10 % | +10–20 %, accelerating | +21 % | 1.0–1.5 % | $700–800 | 66 % desktop | 20+ |
| [Solar power](https://gripsintelligence.com/insights/industries/electronics/solar-power) | $109M | −20–50 % | +5–10 % | — | 0.5–1.0 % | $600–700 | — | 30+ |
| [Lawn and garden equipment](https://gripsintelligence.com/insights/industries/home-garden/lawn-and-garden-equipment) | $98M | −10–20 % | +10–20 % | — | 0.5–1.0 % | $400–500 | — | 20+ |

**Context [unverified, not fetched this run]:**
- US e-bike unit sales passed ~1M a year in 2022 (Circana/NPD and LEVA estimates), then the category hit an inventory glut in 2023–2025: VanMoof's bankruptcy (Jul 2023), Juiced Bikes' closure (2024), Cake's bankruptcy (2024) and Rad Power Bikes' public financial trouble in late 2025. Tariffs on Chinese-made e-bikes and batteries rose in 2025. The Grips "−20–50 % then +10–50 %" shape fits that story.
- Portable power stations rode home-backup demand (hurricane seasons, grid outages) and the shift from gas generators; CPSC's long campaign on generator carbon-monoxide deaths makes "no fumes" a real, not cosmetic, benefit.
- The 2025–2026 detailing boom is DIY ceramic coatings and interior kits (Grips: automotive care +124 % Mar→Aug).

### 1.2 Creative benchmarks for this niche (Meta) [v]

| Metric | Automotive (49 brands, 6.0K creatives) | Sports & Recreation (23 brands, 2.9K creatives) | Source |
|---|---|---|---|
| Median creative lifespan | **29 d** (+24 % vs cross-industry) | **20 d** (−23 %) | [Benly Automotive](https://benly.ai/benchmarks/q1-2026/automotive), [Benly Sports & Rec](https://benly.ai/benchmarks/q1-2026/sports-recreation) |
| 30-day survival | 48.3 % | 27.9 % | same |
| Video share | **25.6 %** | 26.7 % | same |
| Best asset type (effectiveness index) | Lifestyle/Editorial 77; **Product Shot 75 (35 d median, 56 % 30-d survival — longest)** | Branded/Studio 67; Lifestyle 65 | same |
| Worst | Branded/Studio 65 | **UGC/Organic 18 (13 d, 15 % survival)** | same |
| Hook note | "Visual Intrigue" is the default; **Pain Point and Question openings frequently live longer** | same | same |

Read with care: Benly's "automotive" set is dominated by car makers (its one sub-vertical page is car manufacturers). But both sets agree with our measured ads: **product-forward studio and demo work outlive UGC in sports/outdoor**, and cadence is ~3–4 weeks.

### 1.3 The 30 brands (founder-led and $1–20M marked)

Price bands are from each store's `products.json` (first 250 products; min / median / max of the cheapest variant) on 2026-10-09 [m]. "New 60 d" = products created in the last 60 days. Meta volume from Motion brand pages (~June 2026 snapshot) [v]. ★ = founder-led and plausibly $1–20M revenue (the VXO sweet spot) [inf/unverified]. Revenue is not published for any of these; band estimates are [unverified].

| # | Brand | Sub-niche | Price band (min/med/max) | New 60 d | Meta (active · new/wk · video in newest 20) | Note |
|---|---|---|---|---|---|---|
| 1 | Lectric eBikes | Value e-bikes, trikes | $0 / $999 / $1,999 | 2 | — | Founders Levi Conlow & Robby Deziel; far above $20M [unverified]; 6.5M and 6.2M TikTok launch posts (paid) |
| 2 | Aventon | E-bikes | $0 / $21 / $5,999 | 2 | — | YouTube "Aventure 3" **56M** views (TrueView) |
| 3 | Rad Power Bikes | E-bikes, cargo | $5 / $55 / $2,399 | 0 | 10 · 6 · 4/20; Offer-First 60 % | Founder Mike Radenbaugh; distressed 2025 [unverified]; no new SKUs since June |
| 4 | Super73 | E-motos / e-bikes | $8 / $80 / $5,499 | 1 (Red Bull Racing M1D SE, 9/9) | 32 · 6 · 11/20 | Montage-heavy; founder ad "Michael from Super73" |
| 5 | Velotric | E-bikes | $20 / $96 / $2,499 | 2 | **288 · 35** · 5/20 | Feature callouts by use case (hunters, families) |
| 6 | ★ Murf Electric Bikes | Lifestyle e-bikes | $10 / $95 / $2,595 | 2 | — | Small catalogue (49), TikTok median 1.5K |
| 7 | ★ Ride1Up | Value e-bikes | n/a (non-Shopify) | — | — | San Diego; TikTok embed empty |
| 8 | Heybike | Value e-bikes | $0 / $61 / $5,499 | **21** | — | Pannier/accessory push |
| 9 | Himiway | Fat-tire e-bikes | $0 / $79 / $3,999 | 1 | — | |
| 10 | Mokwheel | Off-road e-bikes | $0 / $118 / $3,300 | 148 (site rebuild 8/20) | — | Re-created catalogue = new site |
| 11 | ★ Vanpowers | Lightweight e-bikes | $10 / $40 / $3,999 | 9 | — | Replaceable-battery UrbanCross |
| 12 | Tenways / Engwe / Fiido | E-bikes (CN-founded DTC) | $15–1 / $37–149 / $2,299–4,999 | 4–7 | — | Gift-with-purchase bundles (Engwe) |
| 13 | ★ Apollo Scooters | Performance e-scooters | $0 / $40 / $5,499 | **7 (Phantom 2.0, Stellar "Warrior", 10/7)** | — | Montreal; launch this week |
| 14 | Unagi | Scooter subscription | n/a | — | — | 2021 balloon stunt 2.8–3.2M (older) |
| 15 | Onewheel (Future Motion) | Board e-rideables | $1 / $35 / $2,900 | 5 | — | Founder Kyle Doerksen; race-season merch |
| 16 | ★ Evolve Skateboards (US) | E-boards, BMX e-bike | $0 / $129 / $5,499 | 0 | — | "Project BMX eBike" 801K (10/1/2026) |
| 17 | ★ Unit 1 | Smart helmets, lights | $0 / $35 / $260 | 1 | **79 · 37** · 4/20 | Two founders; "helmet gap" claim ads |
| 18 | Quad Lock | Phone mounts | $8 / $50 / $160 | 6 (iPhone 18 cases 9/10) | 10/20 video | 24.9 %-like costume race (T12) |
| 19 | ★ Drift | Car scents | $0 / **$17** / $99 | **35 (limited drops)** | **366 · 159** · 6/20 | Highest velocity in sample |
| 20 | Chemical Guys (Holley) | Car-care chemicals | $1 / $45 / $625 | 1 | 220 · 20 · **20/20** | Corporate-owned; the format leader |
| 21 | ★ Adam's Polishes | Car care | $0 / $16 / $3,260 | 17 | — | Seasonal scents ("Pumpkin Spice Total Interior") |
| 22 | ★ The Rag Company | Microfiber + chemicals | $3 / $71 / $1,620 | 15 | — | 10.0M Gauntlet demo (older) |
| 23 | ★ Obsessed Garage | Detailing kits, tools | $2 / $205 / $18,421 | 20 | — | Kit-ification (Fabric/Leather/Winter kits 10/2–10/7) |
| 24 | ★ Ethos Car Care | Ceramic sprays | $0 / $40 / $1,499 | 3 | — | Free-gift offers |
| 25 | ★ TuxMat | Laser-fit floor mats | $0 / $110 / $188 | 7 (new fitments) | — | Adds vehicle fitments weekly |
| 26 | Fanttik | Inflators, dash cams, car vacs | $1 / $100 / $1,100 | 9 (Luma K10 Apex 4K, 9/10) | — | TikTok-Shop native |
| 27 | ★ ROVE | Dash cams | $6 / $40 / $750 | 12 | — | Sale statics on TikTok (0.02 % likes) |
| 28 | ★ DECKED | Truck/SUV drawer systems | $10 / $40 / $2,100 | 1 | — | "Made in America" (claim risk §5) |
| 29 | ★ Roofnest | Rooftop tents | $0 / $442 / $5,261 | **17 (Meadowlark 2, 9/23)** | — | Bundles with awnings |
| 30 | Jackery · EcoFlow · Goal Zero (NRG) | Power stations | $0–2 / $300–399 / $6,429–12,999 | 15 · 4 · 1 | 291·66·1/20 · 146·70·1/20 · 24·7·13/20 | Corporate; offer-first statics |
| — | ★ Pecron, OUPES, ★ Lion Energy, BougeRV | Power stations / 12 V | med $119–1,129 | 0–5 | — | Smaller power brands; Lion Energy (Utah) founder-led [unverified] |
| — | ★ Tesery, Jowua, ★ Abstract Ocean | Tesla accessories | med $40–87 | **93** · 8 · 3 | — | Tesery = SKU firehose |
| — | ★ Banks Power | Diesel/gas performance | — | — | 156 · 2 · 7/20 | Family-owned (Gale Banks); one skeleton × 8 vehicle makes |
| — | TentBox (UK) | Rooftop tents | — | — | **366 · 29 · 17/20** | The most video-heavy outdoor brand in sample |

Out of the VXO band but useful as references: WeatherTech (founder David MacNeil; Super Bowl ads every year — "Lucky Dog" 2020 914K, "American Factory" 648K, 2025 "Whatever Comes Your Way" 472K YouTube views [m-metadata]), Chemical Guys, Jackery, EcoFlow, Segway, Thule, Dometic, Milwaukee.

### 1.4 Price bands (what the buyer is selling)

| Band | Products | Buying mode | What the film must do [inf] |
|---|---|---|---|
| **<$30 impulse** | Car scents (Drift $17 median), microfiber, sprays, gel cleaners | Mobile, same-day; offer and novelty | 8–15 s loop; one sensory hook; offer slot; many variants |
| **$30–200 problem-solver** | Floor liners ($110), phone mounts ($50), interior kits, tyre inflators, dash cams ($40–200), seat-gap fillers, helmets lights | Mobile → cart in a day or two; 2–4 % conversion | A pain-point opening and one mechanism shot; 15–20 s |
| **$200–800 upgrade** | Smart helmets ($260), small power stations ($300–400), Tesla accessories ($400–500), truck drawers, e-scooters ($300–400 AOV) | Research a week; reviews; desktop finish | Mechanism + proof + spec card; 20–30 s; a 16:9 cut |
| **$800–6,000 considered** | E-bikes ($999–2,599 typical), large power stations ($1,000–6,400), rooftop tents ($2,000–5,000), e-motos ($2,500–5,500) | Weeks; desktop (72 %); financing; showrooms/test rides | Identity + trust; founder; a "would I use this" scene; financing/offer slot; a long-form explainer the film points to |

### 1.5 Seasonality calendar (US)

| Month | E-bikes / scooters | Car care / accessories | Power gear | Evidence |
|---|---|---|---|---|
| Jan | New-Year deals (Rad "NEW YEAR DEALS") | New-car registrations; winter salt kits | Winter-storm outages | Motion Rad headlines [v] |
| Feb–Mar | Pre-season launches (Lectric XP Trike 2/7/2023, XPedition 2/21/2023) | Spring-wash prep | — | TikTok dates [m] |
| **Mar–Jun** | **Peak season (+45 % to +71 % Mar→Aug index)**; Earth Day; Father's Day | **Detailing season (+124 % Mar→Aug)**; Memorial Day sales | Camping/RV season (EcoFlow "RV Sale", Goal Zero "biggest sale of the season") | Grips [v], Motion [v] |
| **Jun–Nov** | Summer riding; back-to-school commuters (Aug–Sep) | Road-trip season; Amazon Prime Day (Jul) | **Hurricane season (Jun 1–Nov 30)**; Memorial Day/July 4 sales; Jackery "Member Sale Jul 23–28" | Motion/M31 [m] |
| Sep–Oct | New model-year launches (Apollo 10/7, Segway Xyber Air Aug, Super73 × Red Bull 9/9); Halloween (Rad "My broomstick is an ebike") | New phones → new mounts (Quad Lock iPhone 18, 9/10); new model-year vehicle fitments (TuxMat) | Fall storm season; pre-winter backup | products.json [m] |
| **Nov–Dec** | **BFCM + gifting** (Rad "the perfect gift … up to $500 off") | **BFCM gifting** (car scents gift sets 9/16, detailing kits); "Super Brand Day" | BFCM (ROVE "$199.99 → $99.99") | Motion/TikTok [m][v] |

Cadence: automotive Meta ads die at a median **29 d**, sports/recreation at **20 d** (Benly) [v]. That is a monthly refresh need → the Season plan.

### 1.6 Where they advertise

- **Meta (Facebook/Instagram Reels)** — primary for everyone in the sample. Statics dominate power and e-bike brands; video dominates car care (Chemical Guys 20/20), rooftop tents (TentBox 17/20) and Super73 (11/20) [v].
- **YouTube** — the e-bike majors buy TrueView heavily: Aventon "Aventure 3" 56M views, Rad "Find Your Fun" 15.3M, Lectric "XP4" 8.4M, Jackery "Explorer 1500 Ultra" 1.6M, EcoFlow "DELTA Pro Ultra" 337K [m-metadata]. Long product films (61–148 s) live here, not on Meta.
- **TikTok** — Spark Ads boosting brand posts (paid signature everywhere), plus TikTok Shop for the <$200 accessories (Fanttik, car vacs, inflators) [inf].
- **Google Search** — Jackery's Meta ad ends on a **Google search bar typing "Jackery 3600 plus"** (M31) [m]: the brand is buying the branded search the film sends people to. Grips lists Google Ads spend per category (paywalled).
- **Linear TV / CTV** — Lectric ran 30 s TV spots in 2022–2023 (Allard Ave archive), EcoFlow ran 30/60 s spots with a spokesperson, WeatherTech runs the Super Bowl [m-metadata]. The $1–20M brands mostly don't.
- **Creators** — Velotric (Let's Roll, a hunter-firefighter), Jackery ("Steve DOES"), Goal Zero (camp cooks), Navimow and Unit 1 all front ads with creators [v].

---

## 2. Teardowns: 50 measured ads (19 TikTok, 31 Meta) plus 21 YouTube metadata-only

Cut rate = shots ÷ duration (detected cuts + 1). Hook = what is on screen and in the audio in second 1. LUFS / peak are as published (platform re-encode). "1st s" = RMS of the first second vs the clip median.

### 2.1 Full teardowns: the 20 that matter [m]

| # | Ad | Date · views · likes · shares (or Meta signal) | Length · shots · shots/s · LUFS / peak | Shot list (timecodes) | Second 1 (hook) | Turn / punchline | Product interaction | Sound | Text / CTA | Why it sold |
|---|---|---|---|---|---|---|---|---|---|---|
| A01 | **The Rag Company "The Gauntlet is the real hero"** ([link](https://www.tiktok.com/@theragcompany/video/7176702985806974254)) | 2022-12-13 (older, still the account's top post) · **10.0M · 9.05 % · 2,448** | 49.7 s · 2 · 0.04 · −11.7 / **+3.0** (clipped) | 0–28.2 **locked-off tripod**, white cyc, man behind a butcher-block table with two 2 L graduated jugs: a generic pink chamois is dunked, kneaded, lifted, dripping; the jug still reads near-full · 28.2–49.7 same frame, the grey twisted-loop Gauntlet towel dunked, kneaded, lifted: **the jug is almost empty** | Reply sticker ("Shamwow wouldn't have left a drop behind 😏") + the towel already dropping into water | The second jug is empty | Continuous: dunk, knead, lift | Music bed (beat regularity 0.77), no VO | Comment-reply sticker only | **A measurable proof (graduated jug) in one frame, competitor generic.** The audience wrote the brief |
| A02 | **Chemical Guys "Nonsense" tape split** ([link](https://www.tiktok.com/@chemicalguys/video/7062417417988836655)) | 2022-02-08 (older) · **11.4M · 2.18 % · 16.2K** | 30.9 s · **1** · 0.03 · −8.6 / +2.8 | One handheld-locked take on a grimy grey trunk liner: blue painter's tape laid (0–3), bottle to camera (3–5), spray + boar-hair brush agitates foam on the left half (5–19), towel wipes (19–25), **tape peeled (25–27): a razor line, clean vs dirty**, bottle hero (27–31) | Hand already pressing tape down | The peeled tape reveals the line | Spray → brush → wipe → peel | Music bed; foam fizz | None | **Before and after in the same frame — impossible to fake by editing.** 16.2K shares = people sent it |
| A03 | **Chemical Guys Heavy Duty Water Spot Remover Gel** ([link](https://www.tiktok.com/@chemicalguys/video/7646819822176668942)) | 2026-06-02 · **11.4M · 0.48 % (paid)** · 4,966 | 47.7 s · 10 · 0.21 · −10.9 / +1.9 | Hands-only, hard sun: wiping spotted window (0–4.3) · bottle to lens (4.3–6.8) · orange gel drops onto a blue foam pad (6.8–10) · circular rubbing on glass (10–17.7) · Speed Wipe spray (17.7–22) · door paint, same routine (22–40) · yellow towel buff (40–47.7) | A wet hand already wiping, mineral spots in raking sun | Spots vanish under the towel | Every beat is the product touching the surface | ASMR: pad squeak, spray hiss; no VO | Product names on bottle only | **The 2026 version of A02: raking sunlight makes the defect visible.** One new SKU, millions of paid views |
| A04 | **Adam's Polishes "Coating going crazy"** ([link](https://www.tiktok.com/@adamspolishes/video/7201296955715210542)) | 2023-02-18 (older) · 404K · **9.51 %** · 1,831 | **8.8 s · 1** · 0.11 · −11.1 / +3.3 | One handheld shot looking down a silver hood: rinse water sheets toward camera (0–3); as it drains, beads form everywhere except a logo-shaped area; **the Adam's "A" logo appears, drawn by water** (3–8.8); three bottles stand on the cowl | Water already flowing in frame 0 | The logo draws itself | The coating's physics is the action | One shout ("Yes!"), water | None | **The product's real property writes the brand mark.** Loops perfectly at 8.8 s |
| A05 | **Chemical Guys "What are you doing in my car?"** (Meta, trending Automotive) | **Active 72 days** (this week's trending page) | 19.3 s · 3 · 0.16 · **−32.7 / −13.1** (far too quiet) | Selfie-POV door-sill: tape laid, "This is magic" super, InvisiBall-style spray, brush scrub (0–8.9) · wipe (8.9–12.3) · tape gone, clean sill, two hands dance in frame (12.3–19.3) | Off-screen partner: "What are you doing in my car?" | "Nothing. This is invisible." → clean line → happy-hands dance | Spray, brush, wipe | Banter VO, barely audible | "This is magic" | **72 days live with broken loudness: the split-line and the couple banter carry it.** Audio polish is not what makes these sell |
| A06 | **Chemical Guys Interior Deep Clean Kit** (Meta, trending) | **Active 71 days** | 44.7 s · **45** · **1.01** · −18.8 / −3.5 | One box → each tool on its own 1 s shot: towel on dash, door, console; Nonsense + brush on a stain; "Sticky Icky" gel pressed into vents, seams, cup holders, lifted; final clean cabin | "If you're looking for a place to start with interior cleaning, **start here**." | "Whole interior knocked out in one go" | A kit, used in order | VO + light bed | Product names | **A kit sold as a decision removed ("no research, no guessing").** One cut per second, every cut a product touch |
| A07 | **Chemical Guys "However you like to do it"** (Meta) | 5 variants (Skit, Humor, Social-Proof Mashup) | 30.0 s · 16 · 0.53 · −14.2 / −0.7 | Three talking heads, each in their own world (woman by a hybrid under a carport; man in sunglasses and polo by palms; man in a pegboard garage with a red convertible) alternate innuendo lines ("I love to do it… before work, in traffic, at the gym"; "I like to start from the back"; "I use both hands… I want to feel every inch of my baby"; "I make my mother-in-law watch") (0–25) · each now shown washing (25–26.7) · logo card (26.7–28.7) · button: garage man, "Sup?" (28.7–30) | "I love to do it." on a straight face | The reveal that "it" is washing the car | Only in the payoff | Dry delivery, no music under lines | Burned-in captions, logo, "Clean your car" | **Deadpan cross-cut comedy, product as the punchline's reveal; three archetype buyers in 30 s.** Directly the Otto register |
| A08 | **Chemical Guys "5-minute challenge"** (Meta) | 4 variants (Skit, Demo) | 47.3 s · 25 · 0.53 · −16.1 / **+1.7** | Driveway: girlfriend's phone **stopwatch at 00:00** (0–7) · rapid product cards (Fabric, Total Interior, Air Freshener, VRP) as he sprints between doors (7–31) · interior macro inserts (31–41) · stopwatch **4:54** · "Where's my $100?" (41–47) | "You can't clean the entire car in 5 minutes." | He beats the clock and claims the bet | Every product card is a hand-off | Dialogue + clock tension | Product name supers; "Check out the full kit at chemicalguys.com" | **A clock is a story engine.** (Vee's stopwatch is exactly this device) |
| A09 | **Chemical Guys Jeep Rubicon POV detail** (Meta) | **7 variants** | 32.0 s · 27 · **0.84** · **−6.0 / +5.8** (badly clipped) | POV pressure-washer on two muddy Rubicons (0–6) · foam cannon mixing (6–9) · foam (9–12) · wheel cleaner + brush (12–20) · tyre shine (20–24) · Butter Wet Wax pad (24–28) · hero wides (28–32) | Water jet already hitting mud | Mud → gloss | Hands use six products | Music hard on the beat (beat regularity 0.76), cuts on beats | None | **Process on the beat, 7 variants = the brand's money is here.** The mix is 8 dB too hot — a friendly note for a DM |
| A10 | **Drift "juicy white peach"** (Meta) | **7 variants** (Cinematic B-roll) | 10.1 s · **1** · 0.10 · −12.8 / −1.5 | One slow push on the tin of scent resting on glossy, stylised peach slices under god-rays; sparkle motes | Super: "Your car will smell like a juicy white peach" | — (pure sensory) | Static product | Soft bed | One line | **Scent shown as its ingredient. Looks CGI/AI-rendered [inf]; Drift's only cinematic ad among 6 videos and it got 7 variants.** A VXO-shaped asset already being bought |
| A11 | **Drift "Someone explain?"** (Meta) + Spanish "Les mentimos a todos" | 8 variants each (Comment Response, Unboxing, Demo) | 30.2 s · 15 · 0.50 · −20.8 / −1.5 (ES: 29.2 s · 15 · −15.7) | Comment sticker in a Tesla cabin (0–2.8) · unboxing on the steering wheel (2.8–10) · visor-clip install (10–16) · scent names over each tin (16–25) · driving POV (25–30) | "Drift is under $10 right now? Someone explain?" (ES: "Drift has something to confess — we lied to everyone") | "Same exact Drift everyone's been posting about" | Unbox → clip → drive | Female VO, light bed | Captions; "drift.co" | **Price anchor + confession hooks (Motion's top hit-rate hooks) inside a luxury-car POV.** Localised to Spanish with 8 variants |
| A12 | **Velotric Tempo "Your e-bike just got lighter"** (Meta) | 6 variants (Demo, Text Message, Screen Recording) | 30.1 s · 25 · 0.83 · −10.7 / +2.1 | Kinetic type over a white-walled bike (0–3) · kitchen: girlfriend stuffs a donut in his mouth as he grabs the bike (3–8) · **he carries the bike down the stairs one-handed, donut in mouth, trash bag in the other hand** — "LIGHTWEIGHT" (8–12.6) · helmet on, text "Boss Man: Meet me downtown" (12.6–14) · phone map (14–17) · rides, "LONG RANGE" (17–26) · end card "Move at your Tempo" (26–30) | Huge yellow type "YOUR EBIKE JUST GOT LIGHTER" | The one-handed carry with a donut in his mouth | Lift, carry, ride | VO only at 12.6 s; music | Feature supers, end card | **A weight spec turned into a sight gag.** The spec is visible as a behaviour (one hand, full mouth) |
| A13 | **Super73 founder "Michael from Super73"** (Meta) | 6 variants (Founder) | 34.8 s · 27 · 0.78 · **−25.9** / −6.6 | Talking head cut against b-roll of riders, bikes, HQ | "Okay, I get it, I get it. You could ride any bike, but **there's a reason I'm showing up on your newsfeed.**" | "Maybe the algorithm's saying you might need another bike" | Light | Founder VO, quiet | Captions | **The algorithm-aware confession hook.** Founder + b-roll is cheap to refresh |
| A14 | **Super73 grid-swap montage** (Meta) | **7 variants** | 17.4 s · 19 · **1.09** · −12.5 / 0.0 | Wide-angle, fisheye-close portraits of riders; purple studio; split-screen grid swaps; the "73" tank badge; a rider over a ramp; logo | A fisheye face lunging into lens on a beat | — (vibe) | Riding/posing | Music only | Logo | **Identity, not mechanism; the brand's cool is the product.** Only works with a brand this strong |
| A15 | **Jackery "I hate gas generators"** (Meta, trending Technology) | Trending this week | 30.7 s · 14 · 0.46 · −14.1 / +1.8 | Desert: a man yanks a gas generator's pull cord, carries it, hoses fuel — supers "they're hard to move", "messy", "and SUPER LOUD" (0–7.7) · creator in orange tee with the HP3600 Plus in a field: "the lightest, most compact 3600 watt generator there is" (7.7–20) · welder runs off it in the desert, "quietly" (20–23) · kitchen: unit beside a fridge, a hand plugs in (23–28) · **a Google search bar typing "Jackery 3600 plus"** → sale page "Up to 50% off, Jul 23–28" (28–30.7) | "I hate gas generators." over a man fighting a pull cord | "There's none smaller or lighter" | Plug-in shots | Creator VO, music | Kinetic captions with red keywords | **Enemy-first hook (the gas generator) + search CTA.** It claims "fridge **up to 24 hours**"; Jackery's other current ad (M16, Steve DOES) claims "**up to 14 days**" for the same product |
| A16 | **EcoFlow "ice-cream bar" ASMR** (Meta) | 5 variants (ASMR, Montage) | 11.1 s · 25 · **2.25** · −21.9 / −0.1 | Stacked DELTA unit by a food trailer (0–0.8) · hand opens the outlet flap, plugs in (0.8–2) · string lights on · freezer basket, scoop into cup · root-beer bottle opened · pour, foam rises · lid, straw · slurp (2–11.1) | Logo on unit + plug "click" | The slurp | Plug → everything runs | Pure ASMR: click, fizz, pour, slurp | Logo only | **B2B micro-business use case, ASMR at 2.3 cuts/s.** A food-cart owner sees income, not camping |
| A17 | **Segway Navimow creator demo** (Meta, trending Outdoors) | Trending this week | 21.2 s · 10 · 0.47 · −10.7 / +0.4 | Creator sets the mower on the lawn: "Okay, this one actually broke my brain" (0–2.4) · app "no perimeter wire" (2.4–4) · NRTK, dock (4–5) · auto-mapping in app (5–8) · zero-turn pivots in long grass (8–11.7) · stripes (11.7–15) · **he eats at a garden table while it mows: "I haven't touched a mower in 3 weeks"** (15–18) · packshot "Compare where others stop" (18–21) | Mower already being carried in | Man at lunch while the lawn mows itself | Set → tap → watch | VO + captions | Feature labels, end card | **The pay-off is idleness.** Compare Mammotion's AI fantasy (T19): 52K at 0.43 % |
| A18 | **TentBox "Have you seen these everywhere?"** (Meta) | **7 variants** (Demo); sibling listicle M21 also 7 | 32.1 s · 19 · 0.59 · −14.8 / +2.4 | Car-POV in traffic, an estate car ahead with a hard box on its roof (0–4.6) · reveal: tent open, glowing (4.6–7) · "you just park up, release the latches, and **in less than 30 seconds**" (7–14) · ladder, windows, skylight, pockets, light bar = power bank, memory-foam mattress (14–29) · end card "Start your adventure today" (29–32) | "Have you seen these popping up everywhere lately?" over real traffic | Box → bedroom | Latches, ladder, zip, lamp | VO + light music | Captions, logo bug | **Social-proof curiosity hook ("everywhere") + a timed mechanism.** "Less than 30 seconds" is a claim (§5) |
| A19 | **Unit 1 "Your helmet was tested at 14"** ([link](https://www.tiktok.com/@unit1gear/video/7665864904758316289); Meta headlines identical) | 2026-07-23 · 29.5K · 0.11 % (paid) · Meta: 79 active, 37 new/wk | 49.3 s · 21 · 0.43 · −19.4 / −3.5 | Reply sticker on a cracked green helmet (0–4) · dash-cam POV of a cyclist and a car near-miss (4–8) · a helmet tumbles on wet asphalt (8–11) · **CG cross-section: the foam crushes, "IRREVERSIBLE DAMAGE", it doesn't bounce back** (16–24) · the two founders at a table (26–29) · night city riding, light bar on the helmet, turn signals, brake light (29–44) · **drop-test split screen: "UNIT 1 tested at 28 mph" vs "OTHER tested at 14 mph"** (44–46) · end on a shelf | "Most e-bike riders get this wrong, and it's putting them in real danger." | "A helmet you don't have to replace as often" → the founders | CG mechanism + real use | VO + bed | Captions; feature labels | **Category creation by fear + a CG mechanism insert.** Exactly the "inside the machine" cutaway VXO sells (LESSONS) — but every number is a claim (§5) |
| A20 | **Quad Lock "Young Guns 2" (shark vs bee)** ([link](https://www.tiktok.com/@quadlock/video/7678571712333499666)) | 2026-08-27 · 174K · **24.9 %** · 3,570 | 53.2 s · 25 · 0.47 · −13.1 / +0.3 | Two young racers zip into inflatable shark and bee costumes (0–10) · they climb into a side-by-side UTV and race a dirt track with real onboard and trackside angles (10–40) · an older man waves a checkered flag (40–44) · costume heads off, grins (44–53) · "YOUNG GUNS 2" card | Wind-blown costume face + "the bee was fast" | Inflatable costumes doing a real race | Brand on the car livery only | Raw onboard + engine + laughter | Burned-in captions; title card | **Absurd costume × real motorsport = the highest like rate in the sample.** The brand is the sponsor, not the subject |

### 2.2 The other measured ads (one line each) [m]

| # | Ad | Signal | Length · shots · LUFS | What it is | Lesson |
|---|---|---|---|---|---|
| T04 | Lectric XP Trike launch ([link](https://www.tiktok.com/@lectricebikes/video/7197460027781713195)) | 2023-02-07 · 6.5M · 0.50 % (paid) | 14.4 s · 5 · −17.2 | A rider with prosthetic legs on the trike; spec supers "500W REAR HUB MOTOR", "60 MILES ON A SINGLE CHARGE", "FULLY FOLDABLE / FULLY ASSEMBLED" | Accessibility story + spec supers; 14 s |
| T05 | Lectric XPedition teaser | 2023-02-21 · 6.2M · 0.12 % (paid) | **6.0 s** · 4 · −14.5 | Dark-garage macro of frame, tyre "LECTRIC 20x3.0", "150 MILES ON A SINGLE CHARGE", "1300W PEAK MOTOR POWER" | A 6 s spec teaser bought to 6M; range is the hook claim |
| T06 | Super73 "even a Keith can do it" | 2023-01-25 · **5.2M** · 0.27 % (paid) | 57.2 s · 35 · **−34.1** | Super73's lightning-bolt mascot in white gloves unboxes and assembles a bike, rides it off | **A mascot did assembly proof at 5.2M.** Audio 20 dB too quiet and it still ran |
| T07 / T20 | Unagi balloon stunts (older, 2021) | 2.8M / 3.2M · 4.97 % / 3.67 % | 41.3 s / 24.1 s | 1,000 helium balloons lift a scooter; a stratosphere POV; Find My tracking to a Joshua tree; he rides it off | A real stunt that ends in a product test (it still rides). Pre-2024 |
| T09 | see A04 | | | | |
| T10 | Evolve "Project BMX eBike" | **2026-10-01 · 801K · 1.96 %** · 3,819 shares | 24.0 s · 13 · −20.4 / +3.8 | Founder-type walkaround in the warehouse: lifts the bike one-handed, display, rear light, mag wheels, mid-drive motor | A founder walkaround of a nostalgic object (BMX + motor) earned 229× the account median |
| T11 | Segway Xyber Air teaser | 2026-08-10 · 270K · 4.59 % | 5.4 s · 7 · −12.4 | CG-studio macros: an X-shaped light signature, spokes, tank, red X tail-light | A 5 s CG tease of a real launch earns organic engagement |
| T12 | see A20 | | | | |
| T13 | see A19 | | | | |
| T14 | ROVE "SALE EXTENDED! Up to 52% OFF" | 2025-11-01 · 420K · **0.02 %** | 15.1 s · 1 · −11.0 | A static sale card, music | Paid statics on TikTok: reach without a single human reaction |
| T15 | Fanttik K10 Apex 4K dash cam | 2026-10-06 · 37.6K · 0.37 % | 47.9 s · 15 · −14.1 | Side-by-side spec ping-pong ("4K vs 4K", "Sony Starvis II vs generic sensor", "GPS vs no GPS") + 30-day guarantee | Us-vs-them spec comparison for a new SKU |
| T16 | Chemical Guys Total Reset "Galactic" scent fog | 2026-10-07 · 266K · 0.36 % | 38.1 s · 9 · −26.1 | Skit opener ("Did you have too much fun in the rental?" "It's my car, bro") → how-to: AC on recirculate, people/pets out, press button | Skit-to-tutorial; a safety step said aloud |
| T17 | Rad "My broomstick is an ebike" | 2023-10-06 · 44.9K · 1.96 % · 654 shares | 6.1 s · 1 · −23.4 | A rider in a witch costume on a Rad (user content) | Seasonal costume one-liner |
| T18 | DECKED "Get the most out of your 4Runner" | 2026-10-06 · 4.4K | 36.5 s · 23 (cut every 1.0 s) | Drawer system slide-out montage on the beat | Vehicle-specific title; the drawer slide is the money shot |
| T19 | **Mammotion AI "Took a shortcut"** | 2026-09-28 · 52K · **0.43 %** | 17.0 s · 2 · −16.1 | An AI-generated mower "teleports" between fake Instagram posts (Starry Night, a castle, a vineyard, a golf course), back home | **AI fantasy without a mechanism = no reaction** |
| M03 | Chemical Guys holiday UGC | 6 variants | 27.9 s · 5 · −26.0 | A creator washes for the holidays, Mr. Pink, Butter Wet Wax, Two Face, Shine Logic | Product roll-call UGC |
| M05 | Chemical Guys "As a professional mobile detailer, I absolutely hate automatic car washes" | 2 variants (+1 near-twin) | 61.3 s · 16 · −25.1 | Expert enemy hook → kit in his trunk → steps | "I hate X" enemy hook again (cf. A15) |
| M07 | see A11 | | | | |
| M09 | Unit 1 Smart Lights | 3 variants | 34.5 s · 10 · −15.1 | "What if I told you that you could be even more visible?" → lights sync with helmet, turn signals, brake light | Upsell ad to existing owners ("you already made the right move") |
| M10 | Unit 1 "POV: your new Smart Helmet finally arrived" | 4 variants | 27.2 s · 9 · **−25.2** (near silent) | Hands-only unboxing on a white desk: visor clips on, light bar cycles white/red/green, turn-signal swipe | The light *is* the demo; silent is fine on a desk |
| M12 | Velotric GoMad split-screen creator | 6 variants | 42.6 s · 4 · −15.9 | Creator review: "500 pound total payload… 176 pound rear rack… nephews tried the rear seat" | Spec-dense creator review |
| M15 | Rad "We know Rad because we ride Rad" | 2 variants | 15.8 s · 5 · −12.7 | Staff riders; "Everyday e-bikes for everyday e-bike people" | Brand line, little proof |
| M16 | Jackery HP3600 Plus, Steve DOES | 5 variants | 30.4 s · 11 · −15.3 | Creator spec list; "**full-size refrigerator for up to 14 days**"; "UL94-V0 fire-retardant" | Contradicts A15's "up to 24 hours" (§5) |
| M18 | Goal Zero Yeti 1500 "an entire gear list without a single wall outlet" | 6 variants | 27.8 s · 8 · −17.2 | Base-camp charging: cameras, radios, speakers, 140 W USB-C | Spec-by-scenario |
| M19 | Goal Zero camp cook | 6 variants | 44.5 s · 25 · −13.5 | Blended mashed potatoes, miso trout, cold kale salad; fridge-cooler and blender running | **Food beats watts**: a gourmet camp meal makes 1,500 Wh tangible |
| M21 | TentBox "3 reasons" listicle | 7 variants | 44.5 s · 22 · −14.1 | "Finish work Friday, wake up to insane views Saturday"; "built for British weather"; "£35 per month, 0 % finance" | Listicle + finance CTA |
| M22 | Banks PedalMonster "for Silverado" | 2 variants; 1 of 8 make-specific twins | 8.0 s · 1 · **no audio** | Static-to-video: the throttle controller over a Silverado on a red desert card, slow zoom | **One skeleton × 8 vehicle names** (Wrangler, Mustang, F-150…) = personalisation by fitment |
| M23 | Quad Lock motorcycle "This used to be me" | 7 variants (Before and After) | 22.8 s · 8 · −21.9 | A cable-tied generic mount fails → Quad Lock locks on, charges "in any weather" | Pain-point before/after |
| M24 | Quad Lock indoor-trainer setup | **8 variants** | 13.8 s · 5 · −12.4 | Mount installed on a road bike in a home trainer; phone on; rider pedals | Use case nobody thinks of (indoor riding); 14 s |
| M25 | Dometic CFX5 "VIP of coolers" | 4 variants | 30.1 s · 24 · −14.3 | Cinematic mountain campsite, supers "VACUUM INSULATED PANELS", "VMSO 3.5 COMPRESSOR", "OFF-GRID READY", champagne pop, apple in the fridge | Corporate cinematic; spec supers on lifestyle |
| M26 | see A06 | | | | |
| M28 | AdMore light bar founder demo (trending) | Trending | 59.6 s · 24 · −14.4 | Founder walks four customer motorcycles: brake brighter than stock; sequential turn signal "two inputs to the driver's brain" | A founder explaining *why* a light matters |
| M29 | Can Auto Performance V3 intake (trending) | Trending | 24.8 s · 6 · **−30.3** | Phone selfie: "look at the size of this thing compared to the one I have now… lifetime warranty" | Lo-fi size comparison; quiet audio, still trending |
| M01, M02, M04, M06, M08, M11, M13, M14, M17, M20, M27, M30, M31 | see A05–A18 | | | | |

### 2.3 Metadata only (YouTube; views ≈ paid TrueView [inf])

| Brand · title | Views | Length |
|---|---|---|
| Aventon "Aventure 3: The Ultimate All-Terrain E-Bike" | **56.2M** | 122 s |
| Rad Power Bikes "Find Your Fun" | 15.3M | 31 s |
| Aventon "Introducing the Level 4" | 9.8M | 61 s |
| Aventon "The Current — Is That An Aventon!?" | 8.4M | 135 s |
| Lectric "XP4" | 8.4M | 148 s |
| Jackery "See Why Top Influencers are Raving About the New 5000 Plus" | 3.6M | 54 s |
| Aventon "Aventure M" | 3.2M | 62 s |
| Rad "RadRunner Promotional Debut" | 2.7M | 65 s |
| Jackery "Explorer 1500 Ultra" | 1.6M | 47 s |
| Rad "Meet the New RadRunners" | 1.5M | 172 s |
| Lectric "XPress" | 1.3M | 30 s |
| WeatherTech "Lucky Dog" (Super Bowl 2020) | 914K | 31 s |
| WeatherTech "American Factory" (Super Bowl) | 648K | 32 s |
| WeatherTech "Whatever Comes Your Way" (Big Game 2025) | 472K | 61 s |
| Jackery "Solar Generator 5000 Plus — Most Trusted Home Backup" | 465K | 156 s |
| WeatherTech "Tech Team" (Super Bowl) | 397K | 31 s |
| EcoFlow "DELTA Pro Ultra — One Powers All" | 337K | 139 s |
| Super73 "MZFT: Your New Backyard Brawler" | 140K | 28 s |
| Drift "meet drift, your new car freshener" | 118K | 16 s |
| EcoFlow "Power Cut? #ReadyIn30!" | 86K | 40 s |
| WeatherTech "TaDa" (Big Game 2026) | 16K | 31 s |

YouTube is where e-bike brands put 60–150 s product films; the 30 s TV-style spots get the reach. Unagi's polished brand films ("A Scooter With Soul") got 300–4K views — its stunt TikToks got millions [m-metadata].

### 2.4 What the measured set says [m]

| Measure | Value |
|---|---|
| Median length, 50 analysed ads (51 downloaded; T08 dropped as the wrong brand) | **30.1 s** (TikTok median 30.9 s; Meta median 30.1 s) |
| Share ≤15 s | 10 of 50 (20 %) — teasers, ASMR, statics |
| Share ≥45 s | 9 of 50 (18 %) — UGC demos, kits, founder/creator |
| Median shots per second | **0.38** (≈ one cut every 2.6 s); range 0.03 (one-take proofs) to 2.25 (EcoFlow ASMR) |
| One-shot / near one-shot ads (≤1 detected cut) | 7 of 50, plus A01 (2 shots, same frame); **the three biggest organic hits are among them** (A01, A02, A04) |
| Motion in frame 0 | 25 of the 28 frame tiles I inspected (exceptions: statics and a slow push) |
| Hands-only or no face for the first 3 s | 14 of the 28 inspected |
| First audio onset | ≤0.1 s in 38 of 49 with audio (M22 has no audio track) |
| Published loudness | median −15.1 LUFS; **14 of 49 below −20 LUFS and 24 with sample peaks above 0 dBFS** (clipped on encode) — and A05 (−32.7) is still running at 72 days |
| Comedy / skit / costume | 8 of 51 (A05, A07, A08, A12, A20, T06, T16, T17) |
| Claims as numbers on screen or in VO | 19 of 50 (range, watts, mph, days, seconds, payload, % off) |
| AI-looking or CG footage | 4 (A10 [inf], A19 cross-section, T11, T19) |

**Patterns:**
1. **The strongest organic hits are single-frame proofs** (tape line, graduated jug, water drawing a logo). The paid winners are **process at ~1 cut/s** (A06, A09) or **creator demos with a pain-point opening** (A15, A17, A18, A19).
2. **Hooks that recur:** a comment-reply sticker (A01, A11, A19); "I hate X" enemy hooks (A15, M05); a confession or price anchor (A11, A13); "Have you seen these everywhere?" (A18); a clock or a bet (A08).
3. **Faces are cheap here; the buyer trusts a dirty hand more than a face.** Hands-only demos dominate car care; e-bike ads use riders with helmets, mostly at mid-distance — both AI-friendly framings.
4. **Variants cluster on demos and skits** (7–8 variants: A09, A10, A11, A14, A18, M24), not on cinematic lifestyle (Dometic 4, Super73 cinematic 6).

---

## 3. What converts in this niche (with data)

| Question | Evidence | Answer [inf from evidence] |
|---|---|---|
| **Format** | Motion tags: Demo 36 % (Chemical Guys), 44 % (Goal Zero), 26–27 % (Unit 1, TentBox), 61 % (Milwaukee); Offer-First Banner 44–60 % at EcoFlow and Rad [v]; Motion cross-industry hit rates: unboxing 9.83 %, demo 8.11 %, ASMR 8.58 %, founder 8.57 %, cinematic b-roll 6.85 % (doc 45 D3) [v] | **Demo first, then offer.** Cinematic only for brand-strong lifestyle (Super73) |
| **Proof type** | Split-line and measured containers (A01–A05); cross-section CG (A19); comparison spec ping-pong (T15); creator use-case (A15–A17) | One measurable before/after in one frame; a mechanism insert for invisible tech (foam, batteries, sensors) |
| **Claims** | Range, watts, mph, runtime, payload, seconds-to-set-up appear in 19/50 [m] | The number sells and the number is the legal risk (§5). Always the client's tested figure with conditions |
| **Offers** | 30 % off 2-packs (Drift), $400–700 off + 75 % accessories (Rad), up to 52–61 % off (Jackery, EcoFlow), 0 % finance (TentBox), free gifts (Engwe, Ethos), 30-day money-back (Fanttik) [m][v] | A re-skinnable **offer slot** in the last 3 s of every film; finance messaging for >$800 |
| **Length** | Measured median 30 s; organic one-take proofs 9–50 s; paid demos 20–47 s; teasers 5–6 s; YouTube 47–150 s | Deliver **15 s + 30 s + a 6 s teaser** cut; a 16:9 60 s for YouTube on e-bikes and power |
| **Placement** | Meta Reels/Feed dominant; YouTube TrueView for e-bikes/power; TikTok Spark and Shop for <$200 | Vertical 9:16 master, 4:5 and 16:9 crops planned at storyboard |
| **UGC vs cinematic** | Benly Sports & Rec: UGC/Organic effectiveness **18**, 13-day median life (worst) vs Branded/Studio 67; Automotive: Product Shot 75 (longest life, 35 d) [v]; but car-care paid winners are UGC-style demos [m] | **Studio-grade product craft in a UGC-honest frame** (hands, real surfaces, real light) — exactly the VXO "looks shot, not generated" standard |
| **AI ads** | Mammotion's AI fantasy 0.43 % likes vs Navimow demo trending [m]; Drift's CGI-looking peach loop has 7 variants [m]; doc 45: AI images lift CTR only when they don't look AI (OII), AI disclosure can lower credibility (Bui 2025) | AI for the **world, the gag and the mechanism insert**; real footage for the proof; never an AI rider's face in close-up |
| **Disclosure** | Meta "AI info" for photoreal AI; TikTok AIGC label; NY synthetic-performer law from 9 Jun 2026 (doc 45 §5.3) | Label every AI human; keep hands/backs/helmets; C2PA intact |

### 3.1 Answers by sub-niche [inf]

- **E-bikes / scooters:** the buyer fears "will I actually use it?" and "is it safe?". Sell the *use* (the commute, the hill, the grocery run, the kid's school run) and the *mechanism* (weight, battery swap, folding, torque sensor). Big brands' YouTube films are 1–2.5 min; Meta needs 15–30 s cut-downs. Lifestyle montages only work for an already-cool brand.
- **Car care:** the split-line, the bead, the sheet, the foam, the towel that drinks. 1 cut/s process films on the beat. Skits for reach (couples, innuendo, challenges). Kits beat single SKUs (A06 "no research, no guessing").
- **Interior accessories (mats, liners, gap fillers, organisers, scents):** highest conversion (3.5–4.0 %) and mobile-first: short, problem-first, one mechanism. Scents: show the ingredient (A10) or the reaction (comments).
- **Dash cams:** shrinking category; sells on fear (insurance, hit-and-run) and spec comparisons; footage samples are the proof.
- **Power stations:** offer-first statics now; the films that work are **use cases with an enemy** (gas generator, outage, a dead cooler) and **food/heat/light you can see**. Runtime claims are dangerous (§5).
- **Rooftop tents / overland:** timed set-up demos; financing; weather.

---

## 4. AI realism pitfalls specific to this niche, and the fixes

The audience here is **pedantic by hobby**. Cyclists count spokes, detailers know how a bead behaves, overlanders know a ladder angle. A wrong drivetrain side is the e-bike equivalent of six fingers. Every fix below is written to slot into doc 43's labeled-block prompts (§2.1) and its failure table (§5).

### 4.1 E-bikes, e-motos and scooters

| Trap | What goes wrong | Prompt / reference fix | Physics to write |
|---|---|---|---|
| **Spokes and wheels** | Spoke count changes, wheels strobe backwards (wagon-wheel effect), hubs melt; fat tyres lose their tread | Hero wheel = **Kling 3.0 Pro i2v from a real photo** (doc 43 §1 "product macro insert"); in motion: "at speed the spokes blur into a translucent disc; when still, exactly [36] spokes; tyre tread blocks stay fixed" | Contact patch flattens under load: a 4-inch fat tyre at ~20 psi visibly bulges ~1 cm at the bottom |
| **Drivetrain side** | Chain and cassette jump to the left side, or vanish | "The chain, chainring and rear cassette are on the bike's RIGHT side only (drive side). Camera on the drive side for this shot." Reference: one drive-side and one non-drive-side product photo, labeled | Chain sags slightly on the lower run; never a loop |
| **Pedalling vs speed** | The rider glides with frozen legs on a pedal-assist (Class 1/3) bike, or pedals furiously at a walk | Class 1/3: "cranks rotate at a steady 70 rpm, the legs push down alternately, crank arms always 180° apart". Class 2 throttle: "feet rest still on the pedals, right thumb on the throttle" | 70 rpm cadence on a typical gear ratio ≈ 15–18 mph; legs and speed must agree |
| **Speed and lean** | Riders lean like motorbikes at commuter speeds, or turn flat | Write speed and radius: "turns a 12 m radius corner at about 12 mph, body and bike lean together about 14°" | Lean ≈ atan(v²/gr): 12 mph (5.4 m/s), 12 m radius → ~14°; 20 mph on the same corner → ~34° (reads as racing, too fast for a street) |
| **Display readouts** | Garbled numbers; a speed that contradicts the class | Display unreadable ("screen glow only, no readable digits") **or** composite the client's real screen in post. Never a speed above the bike's class | A Class 1/2 readout tops at 20 mph; Class 3 at 28 mph (§5) |
| **Battery and motor placement** | Battery moves from downtube to rack; hub motor becomes mid-drive | Product sheet on grey (front, both sides, ¾), first reference; "battery integrated in the downtube; rear hub motor; never redesigned" | — |
| **Weight** | A 70 lb cargo bike lifted one-handed like a toy | Only the client's weight spec: "the 39 lb bike is lifted one-handed at the top tube; forearm tendons tense; the bike swings slightly" | 39 lb ≈ 17.7 kg (a heavy suitcase); 60+ lb needs two hands and a hip |
| **Helmets and straps** | Unbuckled straps, helmet drifting on the head, helmet appearing and disappearing | "Helmet on and buckled in every riding shot, strap under the chin"; same helmet ref every shot | — |
| **Scooters** | Stem fold latch invented; rider stands sideways; tiny wheels roll over curbs | "Rider stands with the left foot forward on the deck, right foot behind, knees soft; wheels never mount a curb; slows for a crack" | 8–10 inch wheels: a 3 cm lip stops them; deck flex visible on 100 kg rider |
| **One-wheel boards** | Rider faces forward like a skateboard; board floats | "Rider stands sideways, feet on the nose and tail pads; leans the nose to go; at a stop the tail touches down" | — |
| **Traffic** | Bikes in car lanes against traffic, no lane markings, cars drifting into the bike lane | Clean plate with a painted bike lane; "the rider stays in the bike lane, same direction as traffic; cars stay in their lanes"; tight framings (doc 43 rule 4) | — |

### 4.2 Car care and detailing

| Trap | What goes wrong | Fix |
|---|---|---|
| **Water physics** | Beads look like gel; water runs uphill; sheeting on horizontal panels looks like plastic | Beading and sheeting are the proof → **real footage in the proof slot**. For AI hooks around it, write the physics: "on the coated area water forms round beads 3–6 mm wide that roll off when the panel tilts; on bare paint water lies as a flat film"; prefer Kling i2v from a real still of the panel |
| **Foam** | Foam is translucent soap-bubble film, or rises like dough | "Thick white foam clings to the vertical door for 3 minutes, then slides in slow sheets; never bubbles larger than a pea" |
| **Paint reflections** | Mirror-finish paint reflects nothing, or reflects a camera, crew or a different sky | Real shoots flag the reflection: "the paint reflects only the open sky and a line of trees; no camera, no crew, no people visible in any reflection". Keep the camera at an oblique 30–45° to the panel |
| **Microfibre** | Towels become cotton rags; folds disappear | "Plush grey microfibre folded in quarters, one face used per pass, towel pile visible in macro" |
| **Swirls and defects** | Defects appear and disappear between cuts | Defects only under one light source: "a single LED inspection light at 45° reveals fine circular swirls; the same swirls in every shot until the polisher passes" |
| **Split-line** | A clean straight boundary is the model's weakness | Real footage only (it is the claim). AI may build the reveal *around* the real line |
| **Car identity** | The hero car becomes a real model (a seven-slot grille, a 911 roofline, a Tesla "T"), or morphs between shots | Generic car sheet: "unbadged mid-size SUV, invented grille with horizontal bars, no manufacturer logo anywhere"; for fitment-specific products use the client's **licensed photos of the real vehicle**, no AI rendering of the trade dress (§5) |
| **Plates** | Real-looking state plates, readable numbers | "Plates blank or unreadable" |
| **Interiors** | Dashboards rewritten, steering-wheel shape drifts, screens show gibberish | Doc 43: one locked-off "statics" clip of the cabin, frames reused as elements; screens off or composited |
| **Driver behaviour** | Hands off the wheel, phone in hand, no seatbelt | "Seatbelt on, both hands on the wheel, phone in its mount and untouched while moving" |

### 4.3 Interior accessories (mats, liners, gap fillers, organisers, scents)

| Trap | Fix |
|---|---|
| **Liquids in footwells** | Write volume and container: "a 32 oz (0.95 L) cup tips; the drink spreads across the liner and stops at its raised 1-inch lip; nothing reaches the carpet". 0.95 L over ~0.25 m² of footwell is ~4 mm deep — well under a lip |
| **Fitment** | A mat that floats or overlaps the pedals is a lawsuit, not a joke. "The liner sits flat, edges follow the footwell walls, the pedals are fully clear" |
| **Tiny gaps** | Phones pass *through* seat consoles. Write "the gap between seat and console is 3 cm; the phone (8 mm thick) slides in edge-first and stops on the carpet below" and shoot the inside with a **lipstick camera placed in the gap before the take** |
| **Scent** | Smell is invisible; AI "scent trails" look like smoke. Show the ingredient (Drift A10) or a behaviour (a passenger inhales, eyes close) |

### 4.4 Power stations, solar and robotic mowers

| Trap | Fix | Numbers |
|---|---|---|
| **Cables and plugs** | Floating cables, plugs not in sockets, EU plugs in US homes | "A US three-prong plug seated in the left AC outlet; the cable runs along the floor to the fridge; never crosses itself" | — |
| **Displays** | Invented %, W and hours = runtime claims | Screen unreadable or composited from the client's real screen at the tested load | — |
| **Weight** | 30 kg units lifted like a lunchbox | "Lifted with both hands by the handles, knees bent, a short carry" | Typical: ~10 kg per kWh for LFP portable units [inf from spec sheets]; a 3.6 kWh unit is two-hand heavy |
| **Runtime logic** | A small unit runs a house for days | Runtime ≈ usable Wh × ~0.85 inverter efficiency ÷ average load | 2,000 Wh × 0.85 ÷ 150 W average fridge ≈ **11 h**; Jackery's own ads say "24 hours" and "14 days" for one product (§5) |
| **Outage lighting** | One dark window in a lit street | "The whole street is dark: street lights off, every window black except one; moonlight only" |
| **Gas generators** | Shown indoors or in a garage | Gas generators only outdoors, 20+ ft from windows (CPSC CO guidance [unverified]); battery stations indoors are the point |
| **Solar panels** | Panels facing away from the sun, no shadow | "Panel tilted toward the sun at frame-left, its shadow falls to the right" |
| **Robotic mowers** | Random paths, stripes in the wrong direction | "Parallel passes, overlap 5 cm; stripes alternate light/dark by mowing direction" (stripes are grass bent toward/away from the viewer) |

### 4.5 Rooftop tents and racks

- Ladder at ~70° to the ground, feet on firm ground; the tent's weight is on the roof bars, the car's suspension compresses slightly when a person climbs in.
- Hard-shell opening is a gas-strut motion: slow at first, steady, stops at the stop. Never a "pop".
- "Less than 30 seconds" and similar timings are claims: show the real time-lapse or none.

### 4.6 Model per shot type (consistent with doc 43 §1)

| Shot type in this niche | First choice | Settings | Why |
|---|---|---|---|
| Hero wheel, motor, display, chain, logo macro | **Kling 3.0 Pro i2v** from a real photo | 5 s, `sound:"off"`, `cfg_scale` 0.5, `last_image_url` = packshot | Keeps decals and text from the input image; one move per shot |
| Riding: tracking, lean, commute, hill | **Seedance 2.5 r2v** multi-shot, tight rigs (chase-bike, car-mounted gimbal, roadside tripod) | 3–4 s shots, "EXACTLY N SHOTS", CYCLING PHYSICS block (cadence, lean, lane), clean plate | Multi-angle object fidelity; tight frames hide traffic logic failures (doc 43 rule 4) |
| Car-care process inserts around a real proof | Kling 3.0 Pro i2v (foam, spray, towel) | 5 s, sound off | Text on bottles survives |
| Car driving (accessories in use) | Seedance 2.5 r2v with the car sheet + CAR PHYSICS block (doc 43 §7.1) | Generic car only | The car template from doc 43 |
| Interior cabin, footwell, seat gap | Seedance 2.5 i2v from a locked cabin still; lipstick-camera framings | 6–8 s | A fixed camera inside a small space is the safest generation |
| Outage night exteriors, storm | Seedance 2.5 r2v, static wide from a tripod across the street | 8 s | Static camera, lights-off event is a single state change |
| Sensory one-take (scent ingredient, foam, water drawing a logo) | Cinema Studio 4.0 `pacing:"single-shot"` | 8 s, `dolly-in` | Doc 43 §7.3 |
| Mechanism cutaway (foam crush, battery cells, inside a mat's lip) | Kling 3.0 Pro i2v or Cinema Studio from a clean CG-style still | 5 s | No realism expectation; cheapest proof-adjacent asset |
| Deadpan character beat (Otto/Vee, VXO spec only) | Seedance 2.5 r2v; any line as VO with mouth off-screen | 8–10 s | LESSONS: Otto's mouth never visible |
| Previs | Wan 3.0 480p | seed fixed | $0.05/s |

---

## 5. Policy and legal

**Not legal advice.** Facts fetched this run are linked. Facts marked [unverified] are well known but were not re-read this run; check them before the first client campaign.

### 5.1 US law and self-regulation

| Topic | Rule | Source | VXO rule |
|---|---|---|---|
| **What an "e-bike" is (federal)** | A "low-speed electric bicycle" has operable pedals, a motor **under 750 W (1 hp)** and a top speed **under 20 mph on motor power alone with a 170 lb rider**; it is a consumer product under CPSC, not a motor vehicle | [15 U.S.C. §2085](https://www.law.cornell.edu/uscode/text/15/2085) (fetched) | Never show or say more than the bike's rated power and speed |
| **State three-class system** | Class 1 pedal-assist ≤20 mph; Class 2 throttle ≤20 mph; Class 3 pedal-assist ≤28 mph with a speedometer; Class 3 often 16+ and helmet-required; adopted by most states | [PeopleForBikes](https://www.peopleforbikes.org/electric-bikes/policies-and-laws) (page confirms the class system; definitions and count [unverified]) | Each film's job file names the class; riding speed, rider age and helmet match it |
| **"E-motos" sold as e-bikes; tuning** | California AB 1774 (2024) bars selling products that modify an e-bike's speed beyond its class; several cities and counties restrict high-power "e-bikes" | [unverified] (leginfo.legislature.ca.gov) | No "unlock", "off-road mode" or "derestrict" message in a street scene; e-motos shown only off-road, on private land, with gear |
| **Battery fire safety** | CPSC warns of rising micromobility injuries, deaths and lithium-ion fires; warned against "universal" chargers (Sep 5, 2024) and named products (Ridstar e-bikes, 2026) | [CPSC Micromobility Information Center](https://www.cpsc.gov/Safety-Education/Safety-Education-Centers/Micromobility-Information-Center) (fetched) | Never show overnight charging in a bedroom or blocking an exit, a non-OEM charger, a damaged pack, or charging unattended |
| **Battery certification** | NYC Local Law 39 (2023): e-bikes and e-scooters sold in NYC must be certified to UL 2849 / UL 2272; California SB 1271: certified e-bike batteries from Jan 1, 2026 | [unverified] (nyc.gov, leginfo) | Ask the client for the certificate; "UL certified" on screen only if true for that SKU |
| **Helmet speed claims** | US bicycle helmets meet CPSC 16 CFR 1203 (drop tests at roughly 14 mph equivalent impact speed); e-bike-specific standards (Dutch NTA 8776) test faster | [unverified] (ecfr.gov) | "Tested at X mph" only with the lab report naming the standard; never animate a crash test VXO did not receive |
| **Claim substantiation** | FTC Act §5: objective claims need a reasonable basis before they run; "up to" claims imply many users get near the maximum | [unverified] (ftc.gov) | Range, runtime, "lightest", "fastest", "first", "30 seconds", "14 days" only with the client's test and its conditions on screen |
| **Reference pricing** | Former-price comparisons ("$199.99 → $99.99", "up to 52 % off") must use a bona fide former price | 16 CFR 233 [unverified] | The offer slot carries only the client's live, documented offer |
| **Financing** | Advertising "£35 per month" / "$X a month" triggers Truth-in-Lending disclosures (APR, term) in the US | Reg Z [unverified] | Monthly prices only with the provider's required disclosure line |
| **Warranty language** | A warranty cannot require brand-name parts to stay valid (tie-in ban); a warrantor may exclude damage *caused* by other parts | [FTC Businessperson's Guide to Federal Warranty Law](https://www.ftc.gov/business-guidance/resources/businesspersons-guide-federal-warranty-law) (fetched) | "Won't void your warranty" is a legal claim; say it only in the client's approved words |
| **Emissions tampering** | Clean Air Act §203: selling or installing parts that defeat emissions controls is prohibited; in California emissions-related parts need a CARB Executive Order | [unverified] (epa.gov, arb.ca.gov) | **Red flag: delete kits, tuners, "race only" emissions parts.** VXO films only 50-state-legal or non-emissions products (intakes need a CARB EO to be street-legal in CA) |
| **Lighting and tint** | FMVSS 108 governs road lighting; off-road light bars are "off-road use only"; red/blue forward lights and plate covers are restricted by states | [unverified] | Light bars lit only off-road; no red/blue flashing lights on civilian cars |
| **Distracted driving** | Many states ban handheld phone use while driving | [unverified] | Phone mounted and untouched while moving |
| **Made in USA** | FTC Made in USA Labeling Rule (2021): unqualified "Made in USA" means all or virtually all US-made | 16 CFR 323 [unverified] | DECKED-style "Made in America" only as the client already states it, and qualified if needed |
| **Green claims** | "Zero emissions", "eco-friendly", "clean energy" need qualification and substantiation | FTC Green Guides, 16 CFR 260 [unverified] | Say "no fumes at the point of use", never "zero emissions" |
| **Car makers' marks and trade dress** | Nominative fitment use ("fits Tesla Model Y", "for Silverado") is generally fine; logos, implied endorsement and recognisable trade dress (e.g. a seven-slot grille) are risky | [unverified]; doc 58 §5 (trade dress) | Text fitment yes; no AI rendering of a real model's design; real-vehicle shots only from client-licensed footage |
| **Fake reviews / AI testimonials** | Banned, up to $51,744 per violation | doc 45 §5.3 | No AI "rider" or "customer" endorsing |
| **Synthetic performers** | NY GBL §396-b: conspicuous disclosure for AI performers in ads from Jun 9, 2026 | doc 45 §5.3 | AI human → on-screen disclosure |

### 5.2 Platform rules

| Platform | Rule | Source | VXO rule |
|---|---|---|---|
| **TikTok** | No "potentially inappropriate use of dangerous tools, vehicles, or objects"; no stunts that might lead to injury or are easy to imitate; professional stunts and extreme sports may run if the context and safety measures are clear; imitable ones → **18+ and possibly "Do not try this at home"**; films/cartoons and safety education are exceptions | [TikTok Ads policy](https://ads.tiktok.com/help/article/tiktok-ads-policy-violence-and-dangerous-activities) (fetched) | No wheelies, no riding without a helmet, no speeding, no traffic weaving, no jumps in TikTok cuts unless clearly professional, gear on, 18+ |
| **TikTok** | Police/military gear may not be displayed | doc 45 §5.2 | No police cars in this niche's paid cuts |
| **Meta** | No vehicle-specific restriction found; general dangerous-acts and AI-label rules apply | doc 45 §5 [unverified for vehicle specifics] | Same safety standard as TikTok, so one cut serves both |
| **Google/YouTube** | Restricted "dangerous products"; emissions-defeat devices are a known disapproval category in Shopping | [unverified] | Don't take tuner/delete clients |
| **All** | AI labels (Meta "AI info", TikTok AIGC) | doc 45 §5.3 | Label on; C2PA intact |

### 5.3 Age gates

- E-bikes: Class 3 riders are commonly 16+ by state law [unverified]; under-18 riders must wear helmets in California [unverified]. **Never generate children riding** (LESSONS: never generate babies; children are a backlash and policy risk). Kids' e-bikes (e.g. Super73's K1D) → client footage only, parents present, helmets.
- Ads for e-motos, scooters and power tools should not target under-18s; COPPA applies to anything aimed at under-13s.
- Power stations, car care and accessories: no age gate; scent foggers carry "people and pets out of the car" (Chemical Guys says it aloud, T16) — keep the client's safety step in the film.

### 5.4 Pre-flight checklist additions (with doc 45 §5.4)

- [ ] Bike class, motor wattage and max assisted speed written in the job file; every readout and every riding speed within them.
- [ ] Helmets buckled, legal lane, same direction as traffic, no phone in hand, seatbelts on, both hands on the wheel.
- [ ] No overnight/unattended charging, no non-OEM charger, no gas generator indoors.
- [ ] Every number (range, Wh, runtime, mph, seconds, payload, % off, monthly price) traced to the client's document, with its conditions on screen.
- [ ] No real car logo, grille trade dress or plate; fitment named in text only.
- [ ] Emissions/lighting legality of the product confirmed (50-state legal; off-road-only lighting shown off-road).
- [ ] TikTok cut checked for imitable stunts; 18+ targeting and "Do not try this at home" where needed.

---

## 6. The buyer

### 6.1 Who signs a $1,200–3,500 film [inf with evidence]

- **Founder/CEO** in the $1–20M band (Murf, Apollo, Unit 1, Drift, Adam's, The Rag Company, Obsessed Garage, TuxMat, ROVE, Roofnest, Lion Energy): approves anything that touches the brand; often the face of the ads (Super73's founder ad, Unit 1's founders, AdMore's founder demo, Evolve's walkaround) [m].
- **Head of growth / performance marketer**: owns Meta spend; measures hook rate, CPA, ROAS; buys volume; pain = creative fatigue at 20–29 days (Benly).
- **Brand or creative lead** at the bigger ones (Velotric, Super73, Jackery US): cares about the look; pain = the gap between the YouTube hero film and the Meta statics.
- **Agency**: the corporate players (Chemical Guys/Holley, Jackery, EcoFlow) buy through agencies; VXO would be a subcontractor there [inf].

### 6.2 What they fear (ranked)

1. **"Our community will roast AI."** Riders and detailers spot a wrong drivetrain, a fake bead or a melted spoke instantly; comment sections are the brand's reputation. (Evidence: Mammotion's AI piece earned 0.43 % likes and almost no comments; the measured top performers are all real proof.)
2. **Liability**: a film that shows unsafe riding, an e-bike above its class, a battery charging in a hallway, or a runtime the product can't meet. These are the categories CPSC and state legislatures are actively policing (§5).
3. **Product inaccuracy**: decals, frame geometry, battery placement, colourways, port layouts — a buyer who receives a different-looking bike returns it, and a $1,500 return is expensive.
4. **ROAS on a discount-driven calendar**: 44–60 % of their ads are offer-first; a film has to beat a static with "$500 OFF".
5. **Volume**: Drift ships ~159 creatives a week, Jackery 66, EcoFlow 70; a single film looks small next to that.
6. **Car makers' IP** for accessory brands (fitment shots of real vehicles).

### 6.3 What proof makes them pay $1,200–3,500

- **5 free frames of *their* product, accurate** — correct drivetrain side, correct decals, their real colourway, their real port layout — built from their PDP photos (doc 43 §3 product sheet). Accuracy is the first sale.
- **A niche spec film** (one of §8's best three) showing a mechanism-driven punchline and a proof slot.
- **A claims sheet**: for each number on screen, the source document and the on-screen condition line. This answers fear #2 before they say it.
- **A variant plan**: one skeleton → 6–10 versions (per model, per colour, per offer, per vehicle fitment) — answers fear #5. Banks Power already runs one skeleton × 8 vehicle names (M22) [m].
- **The measured winners in their category** (§2): "your category's longest-running Meta ads are split-line demos and creator use-cases; here is that grammar, made cinematic".
- Price anchor: one TV-style 30 s spot (Lectric/EcoFlow) or a creator shoot with bikes shipped and returned costs more and takes longer [inf]; doc 45 §1.8 for AI-studio prices.

### 6.4 Re-buy triggers (why they rebook monthly)

| Trigger | When | Evidence |
|---|---|---|
| **Model-year and colourway launches** | Feb–Mar and Sep–Oct for rideables; Apollo dropped Phantom 2.0 and Stellar "Warrior" editions on 10/7; Super73 × Red Bull Racing on 9/9; Roofnest Meadowlark 2 on 9/23 | products.json [m] |
| **New vehicle fitments** | Every model year; TuxMat added Expedition Max, Cherokee Hybrid, Prelude, 2 Series, Escalade IQL in 30 days; Lasfit 42 new SKUs in 60 days | products.json [m] |
| **Sales calendar** | Memorial Day, Prime Day, Labor Day, BFCM, New Year; Jackery "Member Sale Jul 23–28", Rad "NEW YEAR DEALS" | Motion [v], M31 [m] |
| **Disaster seasons** | Hurricane season Jun 1–Nov 30; winter storms; wildfire PSPS outages | [inf] |
| **Creative fatigue** | Median Meta life 29 d (automotive) / 20 d (sports & recreation) | Benly [v] |
| **Limited drops** | Drift: 35 new SKUs in 60 days ("Limited Drop: Fresh Baked" 10/5); Adam's seasonal "Pumpkin Spice" | products.json [m] |
| **New phones** | Quad Lock iPhone 18 cases (9/10) | products.json [m] |

**The Season-plan argument here:** one locked skeleton per brand (§8), re-shot per launch, per colourway, per fitment and per sale. That is 2–4 new films a month in this niche without a new idea each time.

### 6.5 Best outreach angle

Lead with **their mechanism moving**, not with AI: "Your best-running ads are a static with a discount. Your [mechanism] deserves to move." Name one real thing from their store (a launch, a colourway, a fitment) and one concrete, product-caused gag. Offer 5 free frames, two options (yes/yes, per `vxo-leads` §3). Never mention their competitors' numbers or any measured flaw unless it's friendly and concrete (e.g. clipped audio).

### 6.6 Sample first DM (never sent; for a founder-led performance e-scooter brand that just launched a new edition)

> Hi [first name] — the new [edition name] colourway is sharp; the [one specific detail, e.g. "red stem against the matte deck"] is the best launch photo you've posted this year.
> One film idea: a commuter at a red light next to a stuck delivery van; the light changes, the van doesn't move, and your scooter folds into the elevator before the van has moved a metre.
> I make AI product films (no shoot), always built from your real product photos.
> Want 5 free frames for the [edition name], or for the [second model]?

(56 words. No link. Speeds, range and folding time only from their spec sheet. Status: **NOT SENT — awaiting owner approval.**)

---

## 7. Lead signals: the niche scoring add-on for `.claude/skills/vxo-leads/SKILL.md`

Apply on top of the base 100-point score. The add-on moves a lead by **−30 to +30**; HOT stays ≥ 70 after the add-on. Public pages only.

| Signal | Points | How to check |
|---|---|---|
| **Season window fit**: 5–7 weeks before the sub-niche's peak (rideables: Mar–Apr and BFCM; detailing: Mar–Apr and BFCM gifting; power: late May before hurricane season, Oct–Nov; rooftop tents: Mar) | +8 | Today's date vs §1.5 |
| **A model-year launch, new edition or colourway** in `products.json` in the last 45 days or announced | +7 | `https://<store>/products.json?limit=250` titles + `created_at` (Apollo Phantom 2.0 Warrior 10/7; Roofnest Meadowlark 2 9/23) |
| **Meta library ≥ 75 % static / offer-first** while the product has a visible mechanism (fold, swap, latch, foam, bead, slide-out) | +7 | Motion brand page (count "Active · video" vs "image" in the 20 newest); Meta Ad Library manually |
| **Fitment or SKU velocity**: ≥ 10 new SKUs or fitments in 60 days | +5 | products.json |
| **A creator- or founder-led demo already winning** (multiple variants) that needs a stronger hook head or a mechanism insert | +4 | Motion variants ≥ 5 on a Demo/Founder tag |
| **Audio faults** in their paid video (peak > 0 dBFS or < −24 LUFS) — a friendly, concrete DM note | +2 | `ebur128` on one public ad (24 of 49 measured ads clip; 14 are below −20 LUFS) |
| **Growing sub-niche** (e-bikes/trikes, automotive care, interior/protective accessories, battery and power solutions) | +3 | §1.1 Grips |
| **Shrinking sub-niche** (dash cams, truck accessories, overlanding gear) | −3 | §1.1 Grips (still fine if the brand is growing) |
| **Unsafe riding or driving in their current ads** (no helmet, wheelies on streets, speed bragging, phone in hand) | −8 | Their TikTok/Meta — they'll ask for it again, and it fails §5 |
| **E-moto sold as an "e-bike", "unlock speed" or derestriction messaging** | **−15** | PDP/ads ("off-road mode", "unlocked", >750 W "e-bike") |
| **Emissions-related performance parts without CARB EO, delete kits, tuners** | **−20** | PDP ("for off-road/competition use only", "not legal in CA") |
| **Battery-fire recall or CPSC warning on the brand in the last 24 months** | −10 | cpsc.gov recalls search |
| **Unsubstantiated big numbers in ads** (runtime/range contradictions like 24 h vs 14 d, "lightest/first" with no qualifier) | −5 | Motion headlines; their ads (they may push VXO to dramatise them) |
| **Corporate-owned** (Holley/Chemical Guys, Segway-Ninebot, Thule, Dometic, NRG/Goal Zero, Trek) | −5 | Ownership; the path runs through agencies |
| **Amazon-only private label / no-name dropship** (generic inflators, universal chargers) | −15 | Brand site, reviews |
| **Distressed** (layoffs, liquidation sales, no new SKUs in 4+ months, public financial trouble) | −10 | News; products.json (Rad: newest product 2026-06-15) |

**VERY hot in this niche looks like [inf]:** a founder-led brand in the $1–20M band (a performance scooter or lightweight e-bike brand, a detailing-kit or microfibre brand, a laser-fit liner brand, a smaller power-station brand), with a fresh launch or fitment wave in products.json, a Meta library of discount statics around a product that visibly *does* something, a season peak 5–7 weeks out, and clean, class-compliant, claims-light ads. Example: base 72 + season 8 + launch 7 + static library 7 + growing sub-niche 3 = **97**.

---

## 8. Ten ready film concepts (invented brands)

Conventions:
- Invented brands; clear names on USPTO before use. Every car is a **generic, unbadged design** (no real grille, roofline or logo); plates blank.
- **Otto and Vee appear only in C10** (VXO's own spec). Any other concept becomes a VXO spec film by casting Otto as the deadpan lead (mouth never visible) and Vee with her one stopwatch.
- Every camera position is a real rig: tripod (incl. low-mode and inside a house), C-stand overhead arm, jib, slider, **suction-cup car mount**, **lipstick camera placed in a small space before the take**, chase car or chase bike with gimbal, handheld. **The camera never passes through glass, walls, doors, car bodies or seats.**
- **Proof slot:** each concept names the real footage the client supplies; AI never performs the claim (the bead, the runtime, the fit, the inflation time, the dash-cam image).
- No dialogue on visible lips. Every film ends with a 2-line VO tagline in a locked voice over a frame with no visible lips, plus the logo card and an **offer slot** the client re-skins.
- Riding and driving: helmets buckled, legal lanes, plausible speeds within the class, seatbelts, no phone in hand.
- **Costs** use doc 43 §6 list prices (as in docs 56 and 58): Seedance 2.5 r2v 15 s = $3.09 proof (480p) + 3 × $6.93 (720p) = **$23.88**; 10 s = $2.06 + 3 × $4.62 = **$15.92**; 8 s = $1.65 + 3 × $3.70 = **$12.74**; Seedance 2.5 i2v 6 s = $1.24 + 2 × $2.77 = **$6.78**; Kling 3.0 Pro i2v 5 s sound-off × 2 takes = **$0.95**; Cinema Studio 4.0 8 s = $1.66 + $3.70 = **$5.36**; Wan 3.0 480p previs 15 s = **$0.75**; stills ≈ $0.30 each; ElevenLabs VO ≈ $0.10. Totals exclude the client's proof footage.

---

### C1 · BEADWELL (spray ceramic coating) — "Your Turn" (15 s) ★ BEST 1 · ★ SINGLE BEST

- **Idea:** A couple shares one car and one chore chart. Saturday night she coats the hood with BEADWELL — but first lays painter's-tape letters on it, and peels them after. Sunday morning it rains. He steps onto the porch with a coffee: on the hood, the rain beads and runs off everywhere except where the tape was, where the water lies flat and dark and spells **YOUR TURN**. Behind the rain-streaked window, her silhouette raises a mug.
- **Hook (0–1 s):** sound first — hard rain drumming on sheet metal; a macro of beads already racing down the hood.
- **Punchline (product-caused):** only a hydrophobic coating can make rain write a message: water beads on coated paint and wets out on the uncoated strokes. Without the product there is no joke.
- **Built on:** A04 Adam's (water drawing the logo, 9.5 % likes, one shot), A02/A05 the tape split-line (11.4M; 72 days live), A07 deadpan reveal, doc 44 "the held last shot is the joke".

| # | t (s) | Shot (rig) | Action / notes |
|---|---|---|---|
| 1 | 0.0–1.5 | **Low-mode tripod on the hood's edge**, 100 mm macro, raking grey light | Rain impacts; round beads 3–6 mm skate downhill; one big bead slides out of frame |
| 2 | 1.5–3.5 | **Tripod on the porch, locked-off**, 35 mm, behind the man at shoulder height | Screen door opens; man in a robe (back to camera) steps out with a mug; the car sits in the driveway in steady rain |
| 3 | 3.5–6.0 | **Proof slot: real footage.** Client shoots from a step-ladder with a phone over a taped-then-coated hood under a garden hose | The dark, flat-wet letters YOUR TURN emerge as the beaded field drains |
| 4 | 6.0–7.5 | Porch tripod, reframed over his shoulder (same position, 50 mm) | The mug stops halfway to his mouth; steam keeps rising |
| 5 | 7.5–9.0 | **Overhead C-stand arm in the garage**, last night (warmer light) | Two hands peel the last tape letter "N" off the hood, slow, one rasp |
| 6 | 9.0–11.0 | **Tripod inside the living room**, facing the window from 2 m; the camera stays inside | Rain streaks on the glass; her back-lit silhouette lifts a mug, one slow nod |
| 7 | 11.0–12.5 | Porch tripod, wide again | He sets the mug on the rail, picks up the bucket by the door, walks into the rain toward the car |
| 8 | 12.5–15.0 | Packshot (real photo): BEADWELL bottle on a beaded panel | VO + logo + offer slot |

- **Physics check:**
  - Ceramic (SiO₂-type) coatings give water contact angles of roughly 100–115°; untreated or decontaminated clear coat is well under that, so water films instead of beading [inf; check the client's data sheet]. That contrast is visible as dark, glossy, continuous strokes against a field of bright beads.
  - A hood slopes ~10–15° toward the windshield; beads of 3–6 mm start to roll at slide angles of ~10–20° → they roll *toward the windshield*, not toward the camera at the bumper: put shot 1's camera at the cowl end looking down-slope.
  - Letters ~22 cm tall, 4 cm strokes, 2 words across a ~1.4 m hood → legible from the porch at ~5 m.
  - Light rain ~2–4 mm/h; puddles don't form on a sloped hood; ~10 °C morning → visible mug steam.
  - The camera inside (shot 6) never moves through the window; the reflection of the room stays dim because the room is unlit.
- **Audio map (timecoded):**
  - 0.0: dense rain on sheet metal (dominant), gutter trickle; 0.9 one heavy drip.
  - 1.5: screen-door spring creak; 1.9 porch boards; rain shifts to "outdoor wide" (softer, broader).
  - 3.5: rain continues; a hose-like hiss is avoided (it's rain in the edit).
  - 6.0: rain only — 1.5 s of deadpan silence in the foreground.
  - 7.5: garage room tone; 7.9 slow painter's-tape rasp; 8.6 tape ball crumple.
  - 9.0: rain on glass (muffled, close); 10.3 a ceramic mug *tink* on the sill.
  - 11.0: mug set on the wooden rail 11.2; bucket handle clank 11.8; footsteps into wet gravel 12.0–12.5.
  - 12.5: VO (dry, warm, mouth off-screen): `Water can't stand it.` [pause] `Your partner, on the other hand…` + two-note sonic logo.
- **Model / template:** shots 2, 4, 6, 7 = **one Seedance 2.5 r2v 10 s clip** ("EXACTLY FOUR SHOTS AND THREE HARD CUTS"; refs: porch/driveway plate, the man from behind, the generic car sheet; "the camera inside the house never moves and never passes through the window"); shot 1 = **Kling 3.0 Pro i2v** from a real macro still of beaded paint; shot 5 = **Kling 3.0 Pro i2v** (hands and tape); shot 3 real; shot 8 real still; Wan 3.0 previs first.
- **Cost:** $15.92 + 2 × $0.95 + previs $0.75 + 8 stills $2.40 + VO $0.10 = **≈ $21**.
- **Claim check:** the film claims only "it beads"; no durability ("lasts 12 months"), no "hydrophobic for X washes" unless the client supplies it. The coated/uncoated contrast is the client's real footage.
- **Why it's the single best:** sound-first hook with motion in frame 0; the punchline is caused by the product's real physical property; it copies the niche's two strongest organic grammars (water writing a mark, the tape line); **no faces, no driving, no riding** — the safest generation in the niche; the proof is cheap for the client to shoot (tape, hose, phone); it re-skins for every coating, sealant, glass treatment and wheel coating, and for Valentine's Day ("BE MINE"), Father's Day ("THANKS DAD") and BFCM — a Season-plan franchise.

### C2 · KILOWATT KIN (2 kWh home-backup power station) — "Lights Out" (20 s) ★ BEST 2

- **Idea:** A storm night. Every hum on the street stops at once: the whole block goes dark. One kitchen window stays lit. Inside, a power station on the floor runs the fridge and one lamp. A knock. Then another. The punchline: the neighbours are queued on the porch, each holding out a phone, and our hero has already laid out a six-way strip with six cables, labelled with names on masking tape.
- **Hook (0–1 s):** sound first — the street's chorus of fridge and transformer hum *cuts* to silence with a relay click, while a wide street is already in motion (rain, swaying branches).
- **Punchline (product-caused):** only the house with stored power becomes the street's charging station; the labelled cables say he planned for it.
- **Built on:** A15 Jackery (enemy hook, trending), A16 EcoFlow ASMR plug-in, M19 Goal Zero (food beats watts), doc 44 rule of three (knock, knock, queue).

| # | t (s) | Shot (rig) | Action / notes |
|---|---|---|---|
| 1 | 0.0–2.5 | **Tripod across the street, locked-off**, 24 mm, night, rain | Lit houses; at 0.6 s every window and the street lights go dark; one kitchen window stays lit |
| 2 | 2.5–4.5 | **Tripod low on the kitchen floor**, 35 mm | Power station on the tiles, one cable to the fridge; the fridge's compressor hum resumes; fridge light glows through its door gap |
| 3 | 4.5–6.0 | **Proof slot: real footage** of the station's screen at the client's tested fridge load (watts in/out) | Real numbers only |
| 4 | 6.0–8.0 | Kitchen tripod, wider, from the counter end | A man (back to camera) eats cereal at the counter under one lamp; a knock at 6.8 s; he doesn't turn |
| 5 | 8.0–10.0 | Same frame | A second knock, louder; a third rhythm (three knocks); he puts the spoon down |
| 6 | 10.0–13.0 | **Tripod inside the hallway, facing the front door** | He opens the door: backlit by phone torches, four silhouettes on the porch, each holding out a phone at arm's length |
| 7 | 13.0–15.5 | **Overhead C-stand arm** above the hall table | A six-way strip already laid out; six charging cables, each with a masking-tape name ("DEB", "MARCO", "THE TWINS"…); hands plug in phones one by one |
| 8 | 15.5–17.0 | Back to the street tripod (shot 1 framing) | The dark street; the one lit window; now a small cluster of phone screens glowing in it |
| 9 | 17.0–20.0 | Packshot (real photo) | VO + logo + offer slot (e.g. hurricane-season sale) |

- **Physics check:**
  - Runtime ≈ usable Wh × ~0.85 ÷ average load: 2,000 Wh × 0.85 = 1,700 Wh; a modern fridge averages ~100–150 W (compressor cycling) → **~11–17 h**; six phones (~15 Wh each, 90 Wh) and one 9 W LED lamp for 5 h (45 Wh) are rounding errors. The film never states hours unless the client's test does.
  - A power outage takes out the street lights and every window at once; the transformer hum stops; rain continues. Phone torches light faces from below — keep them as silhouettes.
  - The station sits indoors on tiles with clearance for its fans; it is a battery, no fumes (the reason the "gas generator outdoors only" rule never collides).
  - Six-way strip: one strip on one outlet, no daisy-chaining (safety); total load well below the station's rated output.
- **Audio map:**
  - 0.0: rain, distant thunder roll at 0.2, **a street-wide hum (transformer + fridges) that cuts dead at 0.6 with a relay clack**; 1.0–2.5 rain only.
  - 2.5: fridge compressor kicks back on at 2.8 (low, steady); station fan whisper.
  - 6.0: spoon on bowl 6.3; knock ×3 at 6.8; spoon chew; knock ×3 louder at 8.6; spoon set down 9.6.
  - 10.0: door latch 10.2; rain louder; a polite cough off-screen 11.1.
  - 13.0: six cable clicks 13.4–15.2 in rhythm (on the music's first beats if music enters).
  - 15.5: street wide, rain; murmured chatter through the window.
  - 17.0: VO (mouth off-screen): `When the street goes dark,` [pause] `you'll find out how many friends you have.` + sonic logo.
- **Model / template:** shots 1 and 8 = one **Seedance 2.5 r2v 8 s** clip (same street plate, the outage as one state change; "every window and street light goes dark at 0.6 s except the kitchen window"); shots 2, 4, 5 = **Seedance 2.5 r2v 8 s** (kitchen plate, station product sheet as first ref, the man from behind); shots 6–7 = **Seedance 2.5 r2v 8 s** (silhouettes only; doc 43 hands block for plugging); shot 3 real; shot 9 real still.
- **Cost:** 3 × $12.74 + previs $0.75 + 8 stills $2.40 + VO $0.10 = **≈ $41**.
- **Claim check:** no runtime, capacity or "powers your whole home" claim on screen beyond the client's tested screen (shot 3); no "zero emissions" (§5.1).
- **Why best:** a sound-first, frame-0 state change; a rule-of-three comic build; a product-caused reversal with real social pay-off; disaster-season timing makes it re-launchable each June and October.

### C3 · LIPLINE (laser-fit floor liners) — "Refill" (15 s) ★ BEST 3

- **Idea:** A passenger holds a giant 32 oz slushie. Hard stop at a yellow light — the cup tips over into the footwell. Silence. The driver doesn't look. The passenger stares at the red lake trapped inside the liner's raised lip. At the next red light, the passenger lifts the liner by its edges, pours the slushie back into the cup through the corner, and holds it up: "Refill?"
- **Hook (0–1 s):** a cup already tipping in frame 0 to the hiss of brakes.
- **Punchline (product-caused):** only a liner with a raised, sealed lip holds a litre of drink well enough to pour it back.
- **Built on:** A06 kit "no guessing", M23 Quad Lock before/after, Benly "Pain Point openings live longer", doc 44 deadpan.

| # | t (s) | Shot (rig) | Action / notes |
|---|---|---|---|
| 1 | 0.0–1.2 | **Lipstick camera fixed in the passenger footwell**, looking up | The 32 oz cup tips past the lens, red slush arcs down |
| 2 | 1.2–2.5 | **Suction-cup mount on the windshield inside, facing the two front seats** | Both lurch forward ~10 cm against belts; driver (from the shoulders down) keeps both hands on the wheel |
| 3 | 2.5–4.5 | **Proof slot: real footage** — overhead of the real liner in a footwell with ~1 L of coloured water poured in | The lake stops at the lip; carpet edges dry |
| 4 | 4.5–6.5 | Windshield mount again | Neither moves; the passenger slowly looks down; the driver keeps his eyes on the road |
| 5 | 6.5–9.0 | Footwell lipstick camera | Car stopped at a red light (ambient red glow); two hands lift the liner by its edges, tilt one corner into the cup; the slush pours back |
| 6 | 9.0–11.0 | Windshield mount | The passenger raises the full cup toward the driver; the driver's hand (only) declines with one finger |
| 7 | 11.0–12.5 | **Exterior: tripod on the sidewalk, locked-off**, wide | The car waits at the red light; a tiny drip from nowhere — nothing reaches the road |
| 8 | 12.5–15.0 | Packshot (real photo) of the liner with the lip in profile | VO + offer slot |

- **Physics check:**
  - Braking at ~0.5 g (a firm yellow-light stop from 25 mph) tips a tall top-heavy cup; slush leaves in an arc and lands within ~30 cm.
  - 0.95 L over a ~0.25 m² passenger footwell ≈ **4 mm** deep; a lip of ~2–3 cm holds it with margin [inf; use the client's lip height].
  - Pouring from a flexible liner corner works because the liner bends at the corner; the cup is placed on the floor below the corner; slush flows slowly (viscous).
  - Belts lock; occupants move ~10 cm; nobody is hurt; the driver never looks away from the road.
- **Audio map:** 0.0 tyre chirp/brake hiss, 0.4 cup rattle, 0.7 slush *splat*; 1.2 belt lock clack; 2.5–4.5 silence + indicator tick; 4.5 a long slurp-free silence (deadpan) with one ice crackle at 5.6; 6.5 liner peel sound (rubbery), 7.3–8.6 slow pour glug; 9.0 cup raised, ice rattle; 10.2 one finger tap on the wheel; 11.0 traffic ambience, drip at 11.8; 12.5 VO: `It holds everything.` [pause] `Even grudges.` + sonic logo.
- **Model / template:** shots 1 and 5 = **Seedance 2.5 i2v 6 s** each from a locked footwell still ("fixed lipstick camera, never moves"); shots 2, 4, 6 = **Seedance 2.5 r2v 8 s** (generic cabin statics clip first, doc 43; hands and torsos only; "EXACTLY THREE SHOTS AND TWO HARD CUTS"); shot 7 = Kling 3.0 Pro i2v from a street still; shot 3 real; shot 8 real.
- **Cost:** 2 × $6.78 + $12.74 + $0.95 + previs $0.75 + 8 stills $2.40 + VO $0.10 = **≈ $31**.
- **Claim check:** no "100 % waterproof", "holds X litres" or fitment claim beyond the client's; the pour-back is a gag, the proof is shot 3.
- **Why best:** motion in frame 0; the product's real geometry causes the joke; mobile-first category with the niche's best conversion rate (3.5–4.0 %); re-skins per vehicle fitment (the Season plan writes itself).

### C4 · FOLDLINE (folding commuter e-scooter) — "Same Light" (15 s)

- **Idea:** 8:52 a.m. At a red light: a delivery van and a commuter on a FOLDLINE. Green. The van is boxed in by a double-parked truck. The rider goes (bike lane, steady speed). Cut to the office lobby: she folds the scooter in one move and steps into the elevator. Last shot: through the lobby's glass doors from the sidewalk, the van finally rolls past — at walking pace.
- **Hook:** the light's red lens fills frame 0, already ticking to green, with a horn blare.
- **Punchline:** the fold is what wins (the elevator), not speed.

| # | t | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0–1.5 | Tripod on the sidewalk, 85 mm on the traffic light | Red → green at 1.0 |
| 2 | 1.5–3.5 | **Chase car with a gimbal arm**, tracking in the adjacent lane at bumper height | Rider (helmet buckled) pulls away in the painted bike lane, ~14 mph |
| 3 | 3.5–5.0 | Same tripod as 1, wider | The van doesn't move; the truck ahead unloads |
| 4 | 5.0–7.0 | **Tripod in the lobby**, low | She rolls to the lobby door, steps off |
| 5 | 7.0–9.0 | **Proof slot: real footage** of the fold, one move, hands only | Client's real fold time |
| 6 | 9.0–11.0 | Lobby tripod | She steps into the elevator carrying it; doors close |
| 7 | 11.0–13.0 | **Tripod outside on the sidewalk**, looking through the glass doors into the empty lobby | The van crawls past in the reflection-free foreground |
| 8 | 13.0–15.0 | Packshot | VO + offer slot |

- **Physics:** scooter ~15 kg folded, carried by the stem with one hand; 8.5–10 inch wheels: no curb hops; 14 mph on a straight bike lane; no lean needed; the helmet stays on until the lobby.
- **Audio:** 0.0 horn; 1.0 signal "beep" crossing tone; 1.5 motor whine rising (quiet), tyre hum; 3.5 van idling, truck tail-lift whine; 5.0 lobby echo; 7.0 latch clack (real proof audio); 9.0 elevator ding 9.6, door slide; 11.0 street ambience muffled through glass; 13.0 VO `Beat the traffic.` [pause] `Then fold it.`
- **Model:** shots 1, 3 Kling i2v; shot 2 Seedance r2v 8 s (CYCLING PHYSICS block, clean bike-lane plate); 4, 6, 7 Seedance r2v 8 s (lobby plate, rider from behind/profile, helmet); 5 real.
- **Cost:** 2 × $12.74 + 2 × $0.95 + $0.75 + $2.40 + $0.10 ≈ **$31**.
- **Claim check:** no top speed or range on screen; legal lane and helmet; fold time only from the client's footage.

### C5 · SNUGSEAM (seat-gap filler) — "Archaeology" (15 s)

- **Idea:** Inside the 3 cm gap between a car seat and the console, a lipstick camera watches a year of things fall in, dated by supers: a fry (Jan), a hair tie (Mar), a lone AirPod-like earbud (Jun), a receipt (Aug), a lipstick (Oct)… Finally a phone drops edge-first — and stops on top of a SNUGSEAM. The hand takes it back. A last super: "Jan–Dec: excavated."
- **Hook:** a fry already falling past the lens with a crinkle, frame 0.
- **Punchline:** the phone is the first object that ever came back.

| # | t | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0–1.5 | **Lipstick camera placed in the gap before each take**, looking up at a slot of daylight | A fry tumbles down onto the carpet (super "JAN") |
| 2 | 1.5–3.5 | Same | Hair tie, coin, a sauce packet (MAR, MAY, JUN) — each lands on the pile |
| 3 | 3.5–5.5 | Same | An earbud bounces in (AUG), a receipt flutters (OCT) |
| 4 | 5.5–7.0 | **Suction-cup mount on the passenger window inside**, looking at the seat edge | A hand drops a phone, edge-first, toward the gap |
| 5 | 7.0–9.0 | **Proof slot: real footage** — the same phone landing on the installed filler | Real fit |
| 6 | 9.0–11.0 | Window mount | The hand picks the phone up without looking |
| 7 | 11.0–12.5 | Lipstick camera (gap) | Now only a strip of foam above; the pile of the year's objects sits in the dark below |
| 8 | 12.5–15.0 | Packshot | VO `Some things are lost forever.` [pause] `Not anymore.` + offer slot |

- **Physics:** gap 2–4 cm; phone 7.8 mm × 160 mm slides edge-first; objects land on carpet ~25 cm down; light falls through the slot as a bright line; the camera never moves (placed before each take).
- **Audio:** 0.0 fry crinkle, soft thud 0.9; 1.5–3.5 elastic flick, coin ring 2.6, packet squish 3.2; 3.5 earbud tick 4.0, receipt flutter 4.8; 5.5 phone slide; 7.0 soft foam stop (real); 9.0 cabin ambience; 11.0 muffled road hum; 12.5 VO.
- **Model:** shots 1–3 + 7 = one **Seedance 2.5 i2v 6 s** + one **Seedance 2.5 i2v 6 s** (fixed lipstick-camera still; "objects fall, land and stay; nothing disappears"); 4, 6 Kling i2v; 5 real.
- **Cost:** 2 × $6.78 + 2 × $0.95 + $0.75 + $2.40 + $0.10 ≈ **$19**.
- **Claim check:** fits "most cars" only if the client says so; no vehicle brands visible.

### C6 · PSI PAL (cordless tyre inflator) — "6:40 a.m." (20 s)

- **Idea:** A man in a suit at dawn, a soft tyre (warning light on the dash). His phone: roadside assistance "ETA 2 h 40 min". He takes a small inflator from the glovebox, attaches, the digital gauge climbs (proof), auto-stops; he drives off. Cut: two hours later, a tow truck pulls into the now-empty spot; the driver looks around, at his clipboard, at the empty space; a bird lands.
- **Hook:** the hiss of a tyre already sagging, macro, frame 0.

| # | t | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0–1.5 | Low-mode tripod on asphalt, 50 mm, on the tyre | Sidewall visibly bulged at the contact patch |
| 2 | 1.5–3.5 | **Suction-cup mount inside, on the windshield**, toward the dash | Tyre-pressure warning icon (generic, no brand) glows |
| 3 | 3.5–5.0 | Over-the-shoulder handheld | Phone screen "ETA 2 h 40 min" (composited, generic app) |
| 4 | 5.0–7.0 | **Handheld low, kneeling height** | The hand screws the chuck onto the valve stem |
| 5 | 7.0–10.0 | **Proof slot: real footage** — the client's gauge climbing to the preset and auto-stopping (time-lapse with on-screen clock) | Real time and PSI |
| 6 | 10.0–12.0 | Tripod at the kerb, wide | He drives away, signal on |
| 7 | 12.0–15.0 | **Same kerb tripod, same framing**, light now warmer (2 h later) | A tow truck pulls into the empty spot, stops |
| 8 | 15.0–17.0 | Same frame | The tow driver (back) looks left, right, at the clipboard; a pigeon lands where the car was |
| 9 | 17.0–20.0 | Packshot | VO `Flat at six forty.` [pause] `Gone by six forty-five.` (only if the client's real inflation time supports "five minutes"; otherwise `Gone before help arrives.`) |

- **Physics:** a passenger tyre from ~20 to ~35 psi with a cordless inflator takes a few minutes depending on size [inf; client spec rules]; the bulge flattens visibly as pressure rises; never inflate past the door-placard pressure; tow truck positions identical framing for the time cut.
- **Audio:** 0.0 slow hiss; 1.5 dash chime; 3.5 phone tick; 5.0 chuck thread; 7.0 compressor buzz (real), auto-stop beep; 10.0 indicator, engine pull-away; 12.0 diesel tow-truck air brakes at 12.6; 15.0 clipboard rustle, pigeon wing flaps at 16.1; 17.0 VO.
- **Model:** shots 1, 2, 4 Kling i2v (3 × $0.95); 6–8 one Seedance r2v 8 s (same kerb plate; "identical locked framing, the car is gone in the second half; a tow truck arrives"); 3 composited; 5 real.
- **Cost:** $12.74 + 3 × $0.95 + $0.75 + $2.40 + $0.10 ≈ **$19**.
- **Claim check:** "minutes", PSI and battery cycles only from the client; inflator never shown as a puncture repair.

### C7 · HINDSIGHT (4K dash cam with parking mode) — "The Note" (15 s)

- **Idea:** A parked car; a note under the wiper: "So sorry about the scratch! — nobody saw." The owner frowns. Cut to the dash-cam playback on her phone: the parking-mode clip shows a man dinging the door, looking around, writing the note — and, in a final gesture, *waving at the camera* to say hi. Owner deadpan. (The playback is the client's real camera footage of a staged ding with a consenting actor.)
- **Hook:** a wiper snaps the note against the glass in frame 0.

| # | t | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0–1.5 | Tripod low by the wheel, 85 mm on the wiper | The note flutters, held by the wiper |
| 2 | 1.5–3.5 | Tripod, medium, parking lot | The owner (back/profile) reads the note |
| 3 | 3.5–4.5 | Insert, hands-only | The note: handwritten text (post-composited, legible) |
| 4 | 4.5–9.5 | **Proof slot: real footage** from the client's camera (parking mode, its true resolution and lens), staged with a consenting actor | Ding → look around → write → wave |
| 5 | 9.5–11.0 | Tripod, medium | The owner lowers the phone; one slow blink (eyes only, mouth hidden by the phone) |
| 6 | 11.0–12.5 | **Suction-cup mount inside the windshield** facing out | The small dash cam's status LED blinks once |
| 7 | 12.5–15.0 | Packshot | VO `Nobody saw.` [pause] `Somebody recorded.` + offer slot |

- **Physics:** parking mode triggers on impact (G-sensor) or motion; a 140–160° lens bends straight lines at the edges; night parking-mode footage is grainy — the real clip sets the look, AI never fakes it (the picture is the claim).
- **Audio:** 0.0 wiper snap + paper flutter; 1.5 lot ambience; 3.5 paper; 4.5 the real clip's own audio (car door ding); 9.5 a long exhale; 11.0 tiny LED "blip" (designed); 12.5 VO.
- **Model:** shots 1, 3, 6 Kling i2v; 2, 5 Seedance r2v 8 s (lot plate, owner from behind/profile); 4 real.
- **Cost:** $12.74 + 3 × $0.95 + $0.75 + $2.40 + $0.10 ≈ **$19**.
- **Claim check:** resolution, field of view and night performance only from the real footage; no plates readable; no insurance-savings claim.

### C8 · HEARTH & HIGHWAY (vent-clip car diffuser) — "Valet" (15 s)

- **Idea:** A restaurant valet takes the keys and drives off. The owner waits at the kerb with her coat on. A minute. Two. She looks down the street: her car is parked thirty metres away, engine off, and the valet is sitting inside, seat reclined, eyes closed, breathing in. He sees her, sits up fast, adjusts the mirror.
- **Hook:** the key fob landing in a white-gloved palm with a chunky click, frame 0.

| # | t | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0–1.5 | Handheld insert at hand height | Keys drop into the valet's gloved hand |
| 2 | 1.5–3.5 | Tripod on the kerb, wide | The car pulls away from the kerb (generic car) |
| 3 | 3.5–5.5 | **Suction-cup mount inside, passenger window, facing the vent** | The diffuser clip on the vent; a hand turns the dial |
| 4 | 5.5–7.5 | Kerb tripod | The owner checks her watch (wrist only), looks down the street |
| 5 | 7.5–10.0 | **Tripod with a 200 mm lens down the street** | The parked car, engine off; through the side glass, the valet reclines, eyes closed (profile, mouth below frame line) |
| 6 | 10.0–12.0 | Same | He spots her, snaps upright, fiddles with the mirror |
| 7 | 12.0–15.0 | Packshot with the scent's ingredient (real photo: cedar, ember, vanilla) | VO `It's not the car he's in love with.` [pause] `It's the air.` + offer slot |

- **Physics:** a vent diffuser scents a cabin in minutes with the fan on; scent is invisible — show it by behaviour only; a 200 mm lens compresses 30 m of street.
- **Audio:** 0.0 key click; 1.5 engine pull-away; 3.5 vent airflow, dial click 4.4; 5.5 street ambience; 7.5 distant city; 8.6 a long inhale (designed, off-mic feel); 10.0 seat recline clunk 10.4; 12.0 VO.
- **Model:** 1, 3 Kling i2v; 2, 4, 5, 6 one Seedance r2v 10 s (street plate, valet in profile, owner from behind).
- **Cost:** $15.92 + 2 × $0.95 + $0.75 + $2.40 + $0.10 ≈ **$21**.
- **Claim check:** no "lasts 60 days", no "natural"/"non-toxic" without client substantiation.

### C9 · HAULIE (Class 1 cargo e-bike) — "Lot 7" (20 s)

- **Idea:** Saturday at the grocery store. An SUV circles the full car park — lap one, lap two (supers "LAP 1", "LAP 2"). A HAULIE rider rolls to the bike rack by the door, loads four bags and a watermelon into the cargo box, rides off. Lap three: the SUV finally finds a spot — at the far end, by the cart corral. As the driver gets out, the HAULIE passes him leaving the car park, watermelon riding up front like a passenger.
- **Hook:** tyres squeal on painted concrete as the SUV takes a tight car-park turn in frame 0 (at 8 mph).

| # | t | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0–2.0 | **Tripod on a light pole platform / high tripod (4 m)**, wide car park | The SUV rounds the aisle end; super LAP 1 |
| 2 | 2.0–4.0 | Same, later | LAP 2 |
| 3 | 4.0–6.5 | **Low tripod at the bike rack by the door** | The rider (helmet buckled) docks the bike, kickstand down (centre stand) |
| 4 | 6.5–9.0 | **Proof slot: real footage** of the real cargo box loaded with four bags + a melon, real payload | Real capacity |
| 5 | 9.0–11.0 | High tripod | LAP 3; the SUV parks at the far end |
| 6 | 11.0–13.5 | **Chase bike with a gimbal** following the cargo bike at 10 mph through the car-park lane | The bike exits past the SUV |
| 7 | 13.5–16.0 | Tripod at the far parking spot, low | The driver (back) shuts his door; the HAULIE rolls past behind him, the melon in the box |
| 8 | 16.0–20.0 | Packshot | VO `Park at the door.` [pause] `Every time.` + offer slot |

- **Physics:** cargo payload per the client (often 300–440 lb total); centre-stand loading; groceries ~10 kg a bag; melon ~5 kg; car-park speed ≤10 mph; pedal-assist: cranks turn at ~60 rpm in low gear; helmet on.
- **Audio:** 0.0 tyre squeal on painted concrete; 1.5 engine idle; 4.0 cart rattles, centre-stand clunk 5.6; 6.5 real loading audio; 9.0 SUV reversing beeps; 11.0 freewheel tick, chain hum, motor whisper; 13.5 door thunk 13.8; 16.0 VO.
- **Model:** 1, 2, 5 one Seedance r2v 8 s (high car-park plate, "identical framing, SUV on three laps"); 3, 6, 7 one Seedance r2v 10 s (CYCLING PHYSICS; the rider from behind; the SUV generic); 4 real.
- **Cost:** $12.74 + $15.92 + $0.75 + $2.40 + $0.10 ≈ **$32**.
- **Claim check:** payload only from the client; no kids in the box (never generate children); no speed readout.

### C10 · VXO spec · STILLWATT (portable power station) — "Golden Hour" (20 s) — Otto & Vee

- **Idea:** A desert film set at golden hour. The crew's gas generator dies. Vee holds up her one silver stopwatch: 4 minutes of light left. Grips yank the generator's pull cord — once, twice, three times. Otto, in his director's chair, silently points at a STILLWATT on a cart. A PA plugs the key light into it. The light glows. Action. The shot gets made. The final beat: the camera pans down the cart — the STILLWATT is also running Otto's espresso machine; a tiny cup sits on the armrest by his huge moustache. Vee stops her stopwatch.
- **Hook:** a pull-cord rip and a dying engine cough, already in motion in frame 0.

| # | t | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0–1.5 | Tripod low on sand, 35 mm | A grip yanks the generator cord; it coughs, dies |
| 2 | 1.5–3.0 | Tripod, medium on Vee | Her one stopwatch held up; low sun flares (she is 3/4 from behind) |
| 3 | 3.0–5.0 | Same as 1 | Two more yanks; nothing (rule of three) |
| 4 | 5.0–7.0 | **Tripod behind the director's chair** | Otto (from behind, moustache visible in profile, mouth never visible) lifts one finger toward a cart |
| 5 | 7.0–9.0 | **Proof slot: real footage** of the client's station powering a real 1–1.2 kW LED light (screen shows its real load) | Real watts |
| 6 | 9.0–11.5 | Wide tripod, set | The key light glows; "Action" board clap (slate, no readable text) |
| 7 | 11.5–14.5 | **Slider on the cart**, slow lateral move | Along the cart: STILLWATT, the light cable, then a second cable to a small espresso machine; a cup steams on Otto's armrest |
| 8 | 14.5–16.0 | Tripod on Vee | She clicks the stopwatch stop; one eyebrow |
| 9 | 16.0–20.0 | Logo card | VO (Vee's locked voice): `Silent power.` [pause] `Loud coffee.` + VXO bumper |

- **Physics:** a 1.2 kW LED key light + a ~1,000–1,300 W espresso machine heating briefly exceed many stations' output — the espresso only pulls *after* the shot wraps (write it: the light is switched off before the espresso starts), or the client's station must be rated for both; golden hour on a desert set gives ~20–40 min of usable warm light; the gas generator stays outdoors (it's a set), no fumes near people.
- **Audio:** 0.0 cord rip, engine cough, die 0.9; 1.5 wind; 2.3 stopwatch tick (Vee's motif); 3.0 rip ×2 (3.4, 4.2), silence; 5.0 chair creak; 7.0 real light fan whisper; 9.0 slate clap 9.6; 11.5 espresso pump buzz 12.8, cup set 14.0; 14.5 stopwatch click 14.9; 16.0 VO.
- **Model:** shots 1–4, 6, 8 = two **Seedance 2.5 r2v 8 s** clips (set plate; Otto and Vee sheets; "Otto's mouth is never visible; Vee holds exactly ONE silver stopwatch"); 7 = Cinema Studio 4.0 slider 8 s; 5 real.
- **Cost:** 2 × $12.74 + $5.36 + $0.75 + $2.40 + $0.10 ≈ **$34**.
- **Claim check:** wattage only from the client's real footage; "silent" → say "quiet"; no fuel/emissions comparison numbers.

### 8.1 Ranking

| Rank | Concept | Why |
|---|---|---|
| ★ 1 (single best) | **C1 BEADWELL "Your Turn"** | Proven niche grammar (water drawing a mark, the split-line), product-caused physics punchline, no faces/driving, the client's proof is cheap, a holiday franchise |
| ★ 2 | **C2 KILOWATT KIN "Lights Out"** | Sound-first state change, rule-of-three build, social pay-off, disaster-season relaunches |
| ★ 3 | **C3 LIPLINE "Refill"** | Highest-converting sub-niche, a deadpan gross-out the product causes, per-fitment variants |
| 4 | C10 STILLWATT "Golden Hour" | Best VXO spec (shows Otto and Vee in a product-caused gag) |
| 5 | C5 SNUGSEAM "Archaeology" | Cheapest, safest (one fixed rig) |
| 6–10 | C6, C7, C8, C4, C9 | Good; more moving vehicles and people → more generation risk |

---

## 9. Twelve insights nobody asked for (that would make VXO better)

1. **The phone sells the dream; the desktop closes the sale.** E-bikes earn 72 % of revenue on desktop, power solutions 66 % (Grips). Deliver every e-bike/power film with a **16:9 "desktop retargeting" cut** and 6–10 PDP stills from the same world — that turns one film into the whole purchase path.
2. **The niche's best ads are one frame long.** The tape line, the graduated jug, the water-drawn logo: the biggest organic hits have 1–2 shots. VXO's craft should **build the world around one real proof frame** instead of replacing it — and say so in the pitch ("we never fake your bead").
3. **Contradictions are a door-opener.** Jackery runs "fridge up to 24 hours" and "up to 14 days" for the same unit at the same time. A **claims sheet** with every number, its source and its on-screen condition is a deliverable these brands don't have — and the AI-specific fear (§6.2) is exactly "the picture overclaims".
4. **Loudness is not the bottleneck — but it is a friendly DM opener.** 24 of 49 measured ads clip and 14 are below −20 LUFS; Chemical Guys' −32.7 LUFS ad has run 72 days. Keep VXO's −14 LUFS/−1 dBTP standard, but sell *demos and hooks*, not mixing.
5. **One skeleton × N vehicles is already how they buy.** Banks Power runs the same 8 s PedalMonster film for Wrangler, Mustang, F-150, Silverado, Tahoe, Suburban, Bronco, Charger; TuxMat adds fitments weekly. A **fitment-variant pipeline** (same film, swapped generic vehicle class + fitment super) is the natural Season deliverable in auto accessories — with real-vehicle shots only from the client (trade dress, §5).
6. **Mascots are already proven in this niche.** Super73's bolt mascot did 5.2M; Quad Lock's shark-and-bee race had a 24.9 % like rate. Otto and Vee are not a VXO indulgence here — they are the format. Offer clients **a brand mascot as a Season add-on only if they ask** (LESSONS: direction is fixed).
7. **AI spectacle alone fails in front of gearheads.** Mammotion's AI montage: 0.43 % likes. The same category's plain demo trends. In every brief, write the mechanism shot first and the AI world second.
8. **A clock is this niche's story engine** — and Vee owns one. The 5-minute detailing challenge (a phone stopwatch), TentBox's "less than 30 seconds", Navimow's "3 weeks without mowing". Vee's stopwatch can be the house device for *any* timed claim (with the client's real time).
9. **Safety-compliant riding is a selling point, not a constraint.** Brands are under CPSC, state-law and platform pressure; a VXO film where every rider is helmeted, in-lane and in-class, with no overnight charging, is the one their legal team approves fast. Put "class-compliant riding" in the deliverable list.
10. **Disaster calendars are launch calendars.** Power stations sell on outage news. A pre-approved "storm kit" film (C2 skeleton) with a 24-hour re-skin — new offer, new region super — ready before June 1 and October is a concrete Season-plan promise.
11. **Founders already front these ads** (Super73, Unit 1's two founders, AdMore, Evolve). Doc 53's "hook head + body" idea in this niche is concrete: a 3–5 s AI hook head (the street going dark, the slush tipping) in front of the founder's existing talking-head body — offered only as a cut of the same film, not a new product.
12. **The overlooked mid-tier detailers are the hottest leads.** Automotive care is forecast +50 %+ (Grips) and the chemistry brands (Adam's 17 new SKUs, The Rag Company 15, Obsessed Garage 20 in 60 days) are founder-led, launch constantly and have proof grammar built in — they need *hooks*, which is exactly what VXO makes.

---

## 10. QA gate additions for this niche

Add to doc 44 §10 and doc 46 §7:

- [ ] **Drivetrain on the right side** in every frame; spoke count stable; wheels turn in the direction of travel at a speed that matches the ground (no wagon-wheel strobing at the payoff).
- [ ] **Cadence matches class** (pedalling for Class 1/3 assist; still feet for Class 2 throttle); lean angle plausible for speed and radius.
- [ ] Helmets buckled; bike lane, same direction as traffic; no phone in hand; seatbelts; hands on the wheel.
- [ ] **No readable readout** (speed, %, W, hours, PSI) except the client's real footage.
- [ ] **Water**: beads round and rolling downhill; films flat; foam opaque; reflections show sky/trees only — no crew, no camera.
- [ ] **Generic cars only**: no grille trade dress, no logo, blank plates; cabin statics locked.
- [ ] Cables seated in the right sockets (US three-prong); no daisy-chained strips; batteries never charging unattended in a hallway or bedroom; gas engines outdoors only.
- [ ] Every object's fate scripted (the slush, the tape letters, the fry, the melon) per doc 43 rule 12.
- [ ] Offer slot present, client-supplied, with any required financing/pricing disclosure line.
- [ ] TikTok cut: no imitable stunts; 18+ and "Do not try this at home" if any professional stunt remains.

---

## Sources

**Measured files** (not committed): `scratchpad/niche2/ebikes-auto/vids/` (T01–T20, M01–M31), analysis in `…/an/` (stats, tiles, transcripts, audio).

**TikTok posts** (all via `https://www.tiktok.com/@<handle>/video/<id>`): theragcompany 7176702985806974254; chemicalguys 7062417417988836655, 7646819822176668942, 7693961636507372813; adamspolishes 7201296955715210542; lectricebikes 7197460027781713195, 7202666850432585006; super73 7192719415740222762; unagiscooters 7009815235041266949, 7042193583855684870; evolveskateboards 7691490103243328789; segway 7672550819610266893; quadlock 7678571712333499666; unit1gear 7665864904758316289; rovedashcam 7567884322615692557; fanttik_official 7693336471100591391; radpowerbikes 7286943037543206190; decked 7693610852175334686; mammotion_official 7690426216972635406.

**Motion (public pages, Meta ad files):** [chemical-guys](https://www.motionapp.com/library/chemical-guys), [drift](https://www.motionapp.com/library/drift), [unit-1](https://www.motionapp.com/library/unit-1), [velotric-e-bike](https://www.motionapp.com/library/velotric-e-bike), [super73](https://www.motionapp.com/library/super73), [rad-power-bikes](https://www.motionapp.com/library/rad-power-bikes), [jackery](https://www.motionapp.com/library/jackery), [ecoflow](https://www.motionapp.com/library/ecoflow), [goal-zero](https://www.motionapp.com/library/goal-zero), [tentbox](https://www.motionapp.com/library/tentbox), [banks-power](https://www.motionapp.com/library/banks-power), [quad-lock](https://www.motionapp.com/library/quad-lock), [dometic](https://www.motionapp.com/library/dometic), [anker](https://www.motionapp.com/library/anker), [thule](https://www.motionapp.com/library/thule), [trek-bicycle](https://www.motionapp.com/library/trek-bicycle), [milwaukee-tool](https://www.motionapp.com/library/milwaukee-tool), [garmin](https://www.motionapp.com/library/garmin), [yeti](https://www.motionapp.com/library/yeti), [solo-stove](https://www.motionapp.com/library/solo-stove), [peak-design](https://www.motionapp.com/library/peak-design); trending: [automotive](https://www.motionapp.com/trending/automotive/), [outdoors](https://www.motionapp.com/trending/outdoors/), [technology](https://www.motionapp.com/trending/technology/).

**Market data:** Grips Intelligence industry pages linked in §1.1 (index: https://gripsintelligence.com/insights/industries); Benly Q1 2026 [Automotive](https://benly.ai/benchmarks/q1-2026/automotive) and [Sports & Recreation](https://benly.ai/benchmarks/q1-2026/sports-recreation); Shopify `products.json` for 47 stores (output in `scratchpad/niche2/ebikes-auto/shop/shop.txt`); YouTube search metadata (`…/yt/search.txt`).

**Law and policy (fetched):** [15 U.S.C. §2085](https://www.law.cornell.edu/uscode/text/15/2085); [CPSC Micromobility Information Center](https://www.cpsc.gov/Safety-Education/Safety-Education-Centers/Micromobility-Information-Center); [FTC Businessperson's Guide to Federal Warranty Law](https://www.ftc.gov/business-guidance/resources/businesspersons-guide-federal-warranty-law); [TikTok Ads policy: violence and dangerous activities](https://ads.tiktok.com/help/article/tiktok-ads-policy-violence-and-dangerous-activities); [PeopleForBikes e-bike policy page](https://www.peopleforbikes.org/electric-bikes/policies-and-laws).
**Law (not fetched this run, [unverified]):** California AB 1774 (2024) and SB 1271 (leginfo.legislature.ca.gov); NYC Local Law 39 of 2023 (nyc.gov); 16 CFR 1203 bicycle helmets, 16 CFR 233 deceptive pricing, 16 CFR 260 Green Guides, 16 CFR 323 Made in USA Labeling Rule (ecfr.gov); Clean Air Act §203 tampering (epa.gov) and CARB Executive Orders (arb.ca.gov); FMVSS 108 (nhtsa.gov); Regulation Z trigger terms (consumerfinance.gov).

**Internal:** docs 41, 42, 43 (§1, §2.1, §5, §6, §7), 44 (§10), 45 (§1, §5), 46 (§7), 51, 52, 53, 58; `research/ai-video-reels/lab/LESSONS.md`; `.claude/skills/vxo-leads/SKILL.md`.
