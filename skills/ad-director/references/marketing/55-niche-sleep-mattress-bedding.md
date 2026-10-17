# 55 — Niche deep-dive: sleep (mattresses, bedding, pillows, non-drug sleep aids)

Research brief, 2026-10-09. No generation money was spent. Nobody was contacted. Nothing was sent.

**What this adds.** No earlier doc covers sleep. Doc 51 (gadgets and home) touches furniture; doc 11 has no bedroom section. This doc builds on 41 (action realism), 42 (teardown method), 43 (models, prices, templates), 44 (comedy craft), 45 (what sells, policy, AI disclosure), 46 (sound and QC) and niche docs 47–53. It does not repeat them. It adds:
- a market map: size, growth, 30 DTC brands with price bands and launch velocity, a seasonality calendar and where the money goes;
- teardowns of **36 posts I downloaded and measured** (from 435 TikToks whose metadata I pulled across 44 brand accounts), 22 of them written up in full, plus Meta-library and YouTube metadata;
- conversion data for the niche (Benly Q1/Q2 2026 Home & Living, Bedding & Bath and Health & Wellness; Motion's Meta library reads; J.D. Power; Amerisleep's 2026 buyer survey; ISPA);
- AI realism pitfalls specific to fabric, foam, beds, sleeping bodies, darkness and night light, with prompt fixes and model routing per doc 43;
- policy and legal (reference-price class actions, "organic" and "non-toxic" claims, Made in USA, mattress flammability, sleep-aid device lines, mouth tape, infant sleep);
- the buyer, re-buy triggers, an outreach angle and a sample DM (never sent);
- a niche scoring add-on for `vxo-leads`;
- 10 ready film concepts (3 marked best) and 10 non-obvious insights.

**Tags.**
- `[m]` I measured it from the file: ffmpeg scene cuts at threshold 0.30, 2 fps frame tiles that I looked at, a 0.5 s RMS envelope, librosa onset rate and beat regularity (autocorrelation peak; > 0.5 means a steady music bed, < 0.15 means voice or no steady beat), EBU R128 integrated loudness and sample peak, and a faster-whisper (base.en) transcript.
- `[c]` the brand's or platform's own claim. `[v]` a vendor or agency figure (directional). `[inf]` my inference. `[unverified]` I found no primary evidence.

**Method and limits.**
- **TikTok.** I read each brand's public creator-embed page (`tiktok.com/embed/@handle`), which lists 10–14 recent and pinned posts. That gave 461 post IDs on 44 accounts; metadata came back for 435. I downloaded 37 posts to `scratchpad/niche2/sleep/` for analysis only. One was excluded: the `@sleepme` handle posts unrelated Russian-language content and is not the Sleepme brand. Five of the downloads are photo carousels that arrive as audio only. **No media is committed or republished.**
- **Paid signature.** A post with ≥ ~250K views and a like rate under ~0.2 % is almost certainly paid (doc 49 method; sleep accounts' organic medians are tiny, so the cut-off is lower than in doc 53). Brands keep paying only for winners, so this is the best public proxy for "sold" `[inf]`.
- **Account medians** use those 4–14 recent posts per account. That is a small window.
- **Meta Ad Library** returns HTTP 403 to our fetcher, and Atria's mirror has no sleep brands. I used Motion's public library pages (7 sleep brands indexed; refreshed "4 months ago") for active-ad counts, creative cadence and format mix. **Run-length winners on Meta could not be confirmed.** That is the biggest gap in this doc (§10).
- **YouTube.** Search works; every download client returned "confirm you're not a bot" or 403. Casper's "Daymares" TV spots are metadata-only, but two of its TikTok cuts were measured.
- **Shopify.** `products.json` is public on 34 of the 51 stores I tried. I used it for price bands and launch velocity (§1.4, §7).

---

## 0. The 10 findings that matter most

1. **The mattress category is shrinking and fighting on price, so the creative is mostly static.** US wholesale mattress value fell to **$9.25B in 2025, −6.5 %, with units −13.2 %** ([ISPA via BedTimes](https://bedtimesmagazine.com/2026/05/the-mattress-industry-trends-report-sharpens-the-industry-picture-for-2025/), [Bedding News](https://beddingnewsnow.com/?p=14447)). Purple's revenue fell 3.9 % to $468.7M, with e-commerce down every year and a going-concern note in its audit ([Purple FY25](https://www.barchart.com/story/news/1061046/purple-innovation-reports-fourth-quarter-and-full-year-2025-results), [Yahoo](https://finance.yahoo.com/markets/stocks/articles/purple-innovation-q4-earnings-call-141036729.html)). In Motion's sample of their 20 newest Meta ads, **Casper ran 5 videos and Purple 6**; the rest were split-screen and offer images [v] ([Motion: Casper](https://motionapp.com/library/casper), [Purple](https://motionapp.com/library/purple)). **A mattress brand that runs 5 sale tentpoles a year on static banners is VXO's clearest opening.**
2. **Bedding and sleep accessories are where the growth, the SKU velocity and the re-buy are.** In 60 days, Boll & Branch added **127** products, Parachute **121**, Brooklinen **88** and Bedsure **38** [m]. Of recent mattress buyers, 63 % then bought toppers, pillows or bedding (avg $74) ([Amerisleep 2026](https://amerisleep.com/blog/state-of-mattress-buying/)). The mattress is bought every 5+ years; the sheets, pillows and sleep aids are bought every season. **Sell the Season plan to bedding and sleep-aid brands; sell a per-tentpole Premiere to mattress brands.**
3. **Sleep's biggest organic hits contain no product at all; the paid winners are plain product films.** The top organic posts were Casper's whispered nature-documentary parody (**5.0M views, 14.9 % likes, 224K shares**) and Hush's "sleep debt" lecture (4.6M, 12 %, 87.8K shares) [m]. Paid posts look nothing like that. Purple filmed its Times Square billboards on a phone (921K, 14.8 s, one take), Silk & Snow ran an 11 s hand-press product film (256K), and Coop's employee explained TENCEL in 35 s (846K) [m]. **Use VXO's comedy for reach and its product films for sales; never mix the two in one asset.**
4. **In Home & Living, plain product shots last longest and "AI-generated" scored best.** Benly Q1 2026, Home & Living: Product Shot effectiveness **66** (32 d median), UGC 62, Branded/Studio 36, Lifestyle 30 [v]. In Bedding & Bath, Branded/Studio is **65** and Product Shot **64**; median ad life is 27 d and 45 % of ads survive 30 days ([Benly Bedding & Bath](https://benly.ai/benchmarks/q1-2026/home-living/bedding-bath)). Benly Q2 2026: the **"AI-Generated" attribute has a 30 d median life and 55 % 30-day survival, the highest effectiveness index of the attributes shown**, and "Calm" is Home & Living's signature attribute (3.6×) ([Benly Q2 Home & Living](https://benly.ai/benchmarks/q2-2026/home-living)) [v]. **Sleep is the one niche where a calm, AI-made product film is the data-backed default, not a compromise.**
5. **The buyer shops at night, and a sale-event ad is a race against a lawsuit.** In one survey, 72 % had made an online purchase after their usual bedtime ([eachnight via Amerisleep](https://amerisleep.com/blog/state-of-mattress-buying/)) [v]. Meanwhile discount creatives are **57.7 %** of Bedding & Bath and **63.8 %** of Home & Living ads [v]. Reference-price class actions hit Brooklyn Bedding (**$8.16M settlement**, prelim. approval June 2026), Saatva, Sleep Number, Eight Sleep, Nest Bedding and Mattress Firm ([ClassAction.org](https://www.classaction.org/news/8.16m-brooklyn-bedding-settlement-wraps-up-class-action-lawsuit-over-allegedly-inflated-reference-prices), [Bloomberg Law](https://news.bloomberglaw.com/litigation/dtc-mattress-company-saatva-accused-of-advertising-fake-sales)). **VXO end cards never show a struck-through "was" price unless the client supplies its 90-day price history (§5).**
6. **The physical joke is native to this category, and the product causes it.** Gravity's weighted blanket collapses a blanket fort (10 s one take, 275K, 1.77 %). Purple's egg-drop heritage, motion isolation (the wine glass test) and mattress-in-a-box expansion are all real-world physics that sell [m] ([Furniture Today on the egg test](https://www.furnituretoday.com/mattress-bedding-news/purples-clever-egg-test-racks-online-views-wins-fans)). **Rule (LESSONS, docs 47–52): the AI film builds the world and the setup; the proof itself (the glass not spilling, the egg not breaking) is the client's real test footage.**
7. **The brand ads have discovered Otto's register.** Casper's first big brand campaign in four years, "Daymares" (Orchard, 2026), shows daytime horrors, then the person in bed, with the end line "Goodnight, day." The TikTok cut I measured stars a **deadpan, moustached presenter** waiting through a silent video call, then cuts to him in bed with a "Shhhhhh" super and **no visible lips** ([Bedding News](https://beddingnewsnow.com/?p=14051), [AdForum](https://act.adforum.com/agency/6700077/creative-work/34733216/birthday-boy/casper)) [m]. **VXO's Otto spec films are on-trend in sleep, and the "shh" ending is the house rule (VO over hidden lips) made into a brand device.**
8. **AI is already in the category, and it is clumsy.** Spring Air (mascot bears), Symphony Sleep ("The Tank", directed by its president) and Kingsdown all shipped gen-AI ads in 2025–2026 ([Bedding News](https://beddingnewsnow.com/blog/2026/07/14/spring-air-will-debut-new-ai-generated-campaign-at-las-vegas-market/), [BedTimes](https://bedtimesmagazine.com/2026/04/symphony-sleep-leverages-ai-for-new-marketing-campaign/), [Furniture Today](https://www.furnituretoday.com/mattress-bedding-news/kingsdown-uses-ai-to-revive-ads-and-train-retail-teams)). Boll & Branch uses AI for imagery and copy ([Modern Retail](https://modernretail.co/operations/where-boll-branch-draws-the-line-on-ai-generated-advertising)). Leesa's "LeesaBot" (an actor playing an AI sleep expert) ran paid at 1.7M [m]. **The buyer has seen AI ads. VXO sells taste, physics and claims safety, not access to the tools.**
9. **Sleep aids are a claims minefield, and one fad is fading.** Mouth-tape search interest is down to **22 from a peak of 100** (Dec 2024; Google Trends via [Fawcett](https://fawcettmattress.com/blogs/news/mouth-taping)). A 2025 PLOS ONE systematic review found 2 of 10 studies with a benefit and 4 warning of asphyxiation risk ([PMC12094774](https://pmc.ncbi.nlm.nih.gov/articles/PMC12094774)). Anti-snoring mouthpieces are Class II devices (21 CFR 872.5570). SomniFix's organic hit claims a "more defined jawline", "mental health" and "10× more productive" [m]. **VXO films sleep aids as rituals and sensations (dark, quiet, weight, cool), never as treatments.**
10. **Calendar beats everything else as a lead signal.** The mattress tentpoles are Presidents' Day, Memorial Day, July 4, Labor Day and BFCM. Bedding adds the January white sale, Mother's Day, back-to-school dorms and gifting (Oprah's Favorite Things in November; Cozy Earth has made the list seven times). Sleep aids add the DST changes and heat waves. **A brand 5–7 weeks before one of these with a new SKU and static-heavy ads is the hottest lead in this niche (§7).**

---

## 1. Market map

### 1.1 Size and growth (US unless stated)

| Segment | Number | Source | Status |
|---|---|---|---|
| Mattresses (wholesale, incl. foundations) | **$9.25B in 2025, −6.5 %; units −13.2 %**; mattress-only units −6.7 %, value −4 %; average prices held | [ISPA trends report](https://sleepproducts.org/2026/07/mattress-industry-trends-report-2026-overview/), [Bedding News](https://beddingnewsnow.com/?p=14447) | Primary (ISPA) |
| Mattresses, 2026 outlook | ISPA's spring forecast: units +3 %, value +5 % vs 2025 | [BedTimes](https://bedtimesmagazine.com/2025/07/latest-forecast-predicts-decline-in-2025-increase-in-2026/) | Forecast |
| Online vs store | Online buyers paid **$984 on average, $258 less** than in-store buyers, and were more satisfied (878 vs 869) | [J.D. Power 2025](https://www.jdpower.com/business/press-releases/2025-us-mattress-satisfaction-study/) | Primary survey (n = 1,751) |
| Buyer behaviour | Average 5-year delay before replacing; 49 % start on Google, **37 % use AI tools**; price drives 73 %; average ceiling $982 (Gen Z $606); 58 % have a regret; 33 % abandoned because of confusion | [Amerisleep 2026](https://amerisleep.com/blog/state-of-mattress-buying/) | [v] brand-run survey, n = 1,006 |
| Bed sheets | **$8.06B in 2025** → $11.55B in 2032 (5.3 % CAGR) | [Fortune BI](https://www.fortunebusinessinsights.com/u-s-bedsheets-market-108607) | [v] |
| Bedding DTC revenue | Brooklinen ~$200M, Boll & Branch ~$180M, Parachute ~$160M (2024); Cozy Earth **$88M on its own site in 2024 (+50–55 %)** | [ReportPrime](https://www.reportprime.com/home-bedding-r17781/company), [Parse](https://www.parse.gl/brands/cozyearth-com) | [v] [unverified] |
| Weighted blankets (global) | ~$516M in 2025, 7.3 % CAGR | via [AOL/Ringly roundup](https://www.aol.com/finance/sleep-become-big-business-yielding-174300942.html) | [v] |
| Sleep-tech devices (N. America) | $9B in 2023, 18 % CAGR | Global Market Insights via [Ringly](https://www.ringly.io/discover/sleep-and-bedding-statistics-2026) | [v] |
| "Sleep economy" (global) | From $66B (narrow) to $616B (broad); the definitions differ by 10× | Emergen, TBRC, Straits via [Ringly](https://www.ringly.io/discover/sleep-and-bedding-statistics-2026) | [v], not comparable |
| Sleep-aid brands | Hostage Tape: **$14M (2023) → ~$40M (2024 projection)**, AOV $25 → ~$60, men 30–50; Manta Sleep "8-figure" with ~25 % revenue lift from a TikTok-led international push; Bearaby "double-digit millions"; Loftie $2.5M (FY2021) | [2X eCommerce](https://2xecommerce.transistor.fm/episodes/40m-revenue-in-year-3-how-meta-ads-strategic-branding-and-influencers-drive-hostage-tapes-success-alex-neist), [Shopify](https://www.shopify.com/blog/manta-sleep-international-expansion), [OMR](https://omr.com/de/daily/bearaby-kathrin-hamm), [KingsCrowd](https://kingscrowd.com/loftie-on-startengine-2022/) | [c]/[v] |
| Sleep tech, premium end | Eight Sleep: **$1.5B valuation** (Mar 2026), FCF-positive in 2025, 34 countries; covers start around $2,000 | [TechCrunch](https://techcrunch.com/2026/03/04/eight-sleep-raises-50m-at-1-5b-valuation) | [c] |
| Couples | ~31 % of US adults sleep apart from a partner at least sometimes (AASM 2024: 29 %); ResMed 2025: US couples split 50/50 | [AASM](https://aasm.org/americans-opting-sleep-divorce-accommodate-bed-partner/), [HealthDay](https://www.healthday.com/health-news/sleep-disorder/are-you-your-partner-in-a-sleep-divorce-youre-not-alone) | Primary survey |

**What the numbers mean [inf]:**
- **Mattresses are a mature, shrinking, promotion-driven market.** Volume moves to wholesale (Purple's Q4 wholesale +39.8 % at Mattress Firm and Costco) and to larger sizes and bundles (adjustable bases, split kings).
- **Bedding is a fashion business.** It has colourways, collabs, robes, pyjamas and towels, and runs 88–127 launches in 60 days.
- **Sleep aids are a creator business on TikTok and Meta.** Masks, mouth and nasal tape, white noise, sunrise lamps, sleep earbuds and weighted blankets sell through "sleepmaxxing" and night-routine content. Sleepmaxxing hashtag counts run from 40M to 500M+ depending on the date ([Healthline](https://www.healthline.com/health-news/sleepmaxxing-tiktok-trend), [Storyboard18](https://www.storyboard18.com/amp/how-it-works/gen-z-explainer-the-rise-of-sleepmaxxing-a-sleep-revolution-or-overhyped-trend-43938.htm)).
- **"Sleep divorce" and couples are a real demand driver.** They sell split kings (Nectar), dual-zone cooling (Eight Sleep), separate duvets and sleep earbuds (Ozlo's "snoring rivals").

### 1.2 Scale anchors (above VXO's band: benchmarks, not targets)
- **Purple:** $468.7M in FY2025; DTC 55.8 % of revenue; 2026 guidance $500–520M. Its largest lender and shareholder, Coliseum, controls any exit ([eightx teardown](https://eightx.co/blog/us-teardown-purple)). The egg test drew 194M views, per its agency, Harmon Brothers.
- **Casper:** owned by Carpenter Co. "Daymares" (Orchard Creative, April 2026) is its first major campaign in 4 years. Historically Casper spent ~33 % of revenue on advertising, booked $81M in refunds, returns and discounts in 2018, and had a 20 % repeat-customer rate ([Retail Dive](https://www.retaildive.com/news/dtc-brands-struggled-with-profitability-prior-to-covid-19-now-what/580689/), [WUWF](https://www.wuwf.org/2020-01-17/the-cost-of-free-casper-pays-a-price-for-generous-mattress-returns)).
- **Tempur Sealy (now Somnigroup, with Mattress Firm), Sleep Number, Serta Simmons, Resident (Nectar, DreamCloud):** corporate- or PE-owned; benchmarks only.
- **Eight Sleep, Hatch, Cozy Earth, Brooklinen, Boll & Branch, Parachute:** above $50M or VC-scale. Good creative references; their buying path runs through in-house teams and agencies.

### 1.3 Thirty DTC brands to know (founder-led, roughly $1–90M where findable)

Columns:
- **TT median** = median views of the account's recent posts [m].
- **SKUs, median price and "new 60 d"** come from the store's `products.json` on 2026-10-09 [m]. "New" counts products created in the last 60 days; content pages and colourways inflate the bedding numbers.
- Revenue is mostly `[unverified]`.

These are **examples for the market map, not outreach targets**. Any lead goes through the `vxo-leads` dossier first.

| # | Brand | Sub-niche | Size signal | Founder-led? | Median SKU price | New 60 d | TT median | Where they advertise (observed) |
|---|---|---|---|---|---|---|---|---|
| 1 | Saatva | Luxury innerspring, white-glove | large [unverified] | Yes (founder-run) [unverified] | — (not Shopify) | — | 16.7K (n = 4) | Meta (11 active, ~4/wk: BTS, demo, athletes, podcast, Memorial Day $625 off) [v]; reference-price suit 2024 |
| 2 | Brooklyn Bedding | Hybrid / RV / OEM | $8.16M settlement shows scale | Founder family [unverified] | $365 | 1 | 2.0K | Meta, affiliates, review sites |
| 3 | Avocado Green | Organic latex mattress + bedding | [unverified] | Yes [unverified] | $157 | **7** (Coyuchi line) | 260 | Meta certification ads (GOTS, GOLS, Greenguard) |
| 4 | PlushBeds | Organic latex, adjustable | "family-owned" [c] | Yes [c] | $236 | 5 | 420 | Creator "toxin-free" stories (fiberglass hook) |
| 5 | WinkBeds | Luxury hybrid | [unverified] | Yes [unverified] | $50 (accessories) | 3 | 322 | Meta, YouTube review creators |
| 6 | Nolah | Hybrid for side sleepers | [unverified] | Yes [unverified] | $211 | 0 | — | Meta, affiliates |
| 7 | Zoma | Athlete-recovery hybrid | [unverified] | [unverified] | — | — | 274 | Athlete creators, "#zomapartner" |
| 8 | GhostBed | Cooling foam | [unverified] | Yes (Marc Werner) [unverified] | — | — | 132 (paid 14.1M, 2021) | UGC couples, quiz funnel |
| 9 | Helix | Quiz-led hybrid | [unverified] | No (portfolio) [unverified] | — | — | 732 | Pro sports (NY Liberty), "best for back pain" |
| 10 | Bear | Athletic / cooling | [unverified] | [unverified] | $175 | 0 | 209 | Athletes (Cubs, Angel City FC), testimonials |
| 11 | Silk & Snow | Hybrid + bedding (Canada) | [unverified] | Yes [unverified] | 403 | — | 896 (paid 256K) | Hand-press product films (paid) |
| 12 | Coop Sleep Goods | Adjustable-fill pillows, sheets | [unverified] | Yes [unverified] | $78 | 1 | **27.8K** | **TikTok LIVE** daily, employee explainers (paid 846K) |
| 13 | Pluto Pillow | Custom pillows (Shark Tank) | "200,000 customers" [c] | Yes | — (TLS timeout) | — | 1.1K (paid 53K) | Quiz, founder-voice 48 s explainer |
| 14 | Eli & Elm | Side-sleeper pillows | [unverified] | Yes [unverified] | — | — | 824 | Meta |
| 15 | Blissy | Silk pillowcases | [unverified] | Yes [unverified] | $95 | 14 | 625 | Meta: 58 active ads, **~47 new creatives/wk**, yapper/demo, 55 % off [v] |
| 16 | Slip | Silk pillowcases, masks | [unverified] | Yes [unverified] | $79 | 2 | — | Retail, Meta |
| 17 | Sijo | Eucalyptus/linen bedding | [unverified] | Yes [unverified] | $60 | 0 | 1.8K | Meta, TikTok |
| 18 | Buffy | Eucalyptus comforters | [unverified] | Yes [unverified] | $139 | 0 | — | Meta |
| 19 | Ettitude | Bamboo lyocell bedding | [unverified] | Yes (Kristy Chong) [unverified] | $35 | 0 | 1 post | Meta |
| 20 | Sunday Citizen | Snug bedding, loungewear | [unverified] | Yes [unverified] | $100 | **22** | 242 | Meta, TikTok |
| 21 | Lunya | Sleepwear | [unverified] | Yes [unverified] | $128 | 0 | 1.5K | Meta |
| 22 | Dagsmejan | Performance sleepwear (CH) | [unverified] | Yes [unverified] | $119 | **19** | — | Meta |
| 23 | Bearaby | Knit weighted blankets | "double-digit millions" [v] | Yes (Kathrin Hamm) | $149 | 2 | 1 post | Netflix/TV product placement, Meta |
| 24 | Hush | Weighted blankets (Canada) | [unverified] | Yes [unverified] | $224 | 0 | 284 (organic 4.6M) | Creator education |
| 25 | Gravity | Weighted blankets | [unverified] | Yes [unverified] | $139 (6 SKUs) | 0 | 1.1K | TikTok skits |
| 26 | Hostage Tape | Mouth tape, nasal strips | ~$40M (2024 proj.) [v] | Yes (Alex Neist) | $50 | **7** (nose-strip bundles) | 938 (organic 4.9M) | **Meta (founder runs ads)**, UFC/Rogan partnerships [v]; TikTok AI-voiced "dream" stories |
| 27 | Manta Sleep | Blackout masks, new white-noise machine | "8-figure" [v] | Yes (Mark Zhang) | $69 | **7** | 270 | TikTok-led international push [c]; Amazon deals |
| 28 | Loftie | Alarm clock, lamp, sound | $2.5M FY21 [c] | Yes (Matt Hassett) | $40 | 1 | 706 (organic 1.5M) | Sound-as-product posts, Meta |
| 29 | Ozlo | Sleepbuds (ex-Bose team) | [unverified] | Yes [unverified] | $29 (accessories); $299 hero | 0 | 167 | Couples/snoring angle, launch films |
| 30 | MyoTape / SomniFix / Nodpod / Yogasleep / Snooz | Small sleep-aid tools | [unverified] | Mostly yes | $16 / $18 / $42 / $50 / $115 | 2 / 0 / 1 / 0 / 0 | 1.0K / 868 / — / 86 / — | Expert podcast clips (MyoTape), meme skits (SomniFix) |

**Too big, but worth watching:** Purple, Casper, Eight Sleep, Hatch, Cozy Earth, Brooklinen, Boll & Branch, Parachute, Sleep Number, Tempur, Nectar/DreamCloud, Bedsure (Amazon/TikTok Shop scale, 38 new SKUs in 60 days).

### 1.4 Price bands (from `products.json`, 2026-10-09 [m], plus site prices)

| Sub-niche | Entry | Hero | Premium | Notes |
|---|---|---|---|---|
| Mattresses (DTC) | $300–600 twin/full foam | **$900–1,800 queen hybrid** | $2,500–5,500 latex/luxury | Online buyers average $984 (J.D. Power); bundles with bases up to $5,499 [m] |
| Adjustable bases / smart beds | $400 | $1,000–2,400 | $4,000+ | DreamCloud's hook: "$4,000 for a smart bed?" [m] |
| Pillows | $35–60 | $78–150 (Coop median $78) | $200–300 (custom, Pluto) | 100–125-night trials common |
| Sheets & duvets | $35–60 (Ettitude median $35) | $100–240 (Boll & Branch median $239) | $400–900 bundles | Collab and colour drops weekly |
| Weighted blankets | $49 | $139–224 | $300–4,000 (Bearaby custom) | Knit vs glass-bead |
| Sleep masks | $20–35 | $69 (Manta median) | $150–999 bundles | Bluetooth audio masks |
| Mouth/nasal tape | $13–18 (30 nights) | $50 bundles (Hostage median) | $200 multipacks | Subscription = re-buy |
| Sound / light devices | $40–50 | $115–170 (Snooz, Hatch Restore) | $280–300 (Loftie lamp, Ozlo) | App subscriptions (Hatch Baby includes 6 months) |
| Temperature (cooling/heating) | $74 (BedJet accessories) | $500–2,426 (BedJet, ChiliPad) | $2,000+ (Eight Sleep) | Long launch films (Eight Sleep 128–144 s) |

### 1.5 Seasonality calendar (US)

| Month | Moment | Who it matters for | Pitch lead time |
|---|---|---|---|
| Jan | New-year sleep resolutions; **January "white sale"** (bedding) | Sleep aids, bedding | Pitch Nov |
| Feb | **Presidents' Day mattress sales** (DreamCloud posted 11 Feb [m]); Valentine's (silk, pyjamas) | Mattresses, silk | Pitch early Jan |
| Mar | **DST spring-forward** (8 Mar 2026); Sleep Awareness Week / World Sleep Day (mid-March) [unverified exact 2027 dates] | Sunrise lamps, masks, sound | Pitch Jan–Feb |
| Apr–May | Wedding registries (Cozy Earth registry ads [v]); **Mother's Day** (robes, PJs, silk, sheets) | Bedding, sleepwear | Pitch Mar |
| **Late May** | **Memorial Day** (the mattress tentpole: Purple, Casper, Saatva, Blissy all ran it [v]) | Mattresses, pillows | **Pitch early–mid Apr** |
| Jun | Father's Day ("All dads want is good sleep", Purple [m]); first heat waves | Mattresses, cooling | Pitch Apr |
| Jul | **July 4 sales**; Prime Day; peak heat | Cooling sheets, pillows, mattresses | Pitch May |
| Aug | **Back to school / college dorms** (twin XL, toppers) | Bedding, toppers, pillows | Pitch Jun |
| **Early Sep** | **Labor Day** ("Biggest Sale of the Year", Sleep Number [m]) | Mattresses | **Pitch mid-Jul** |
| Oct | Prime Big Deal Days (Manta's Amazon push, 6 Oct [m]); fall launches (Eight Sleep Pod 6, 23 Sep [m]) | Sleep tech, aids | Pitch Aug |
| **Nov** | **DST fall-back** (1 Nov 2026); **Oprah's Favorite Things**; **BFCM** | Everyone; heated blankets; gifting | **Pitch mid-Sep–Oct** |
| Dec | Gifting (robes, PJs, masks, sunrise alarms, silk) | Bedding, aids | Pitch Oct |

### 1.6 Where they advertise (observed)
- **Meta: everyone.** Mattress libraries skew to **static split-screens and offer banners**: Casper 45 active ads (Split Screen 8 of 20, Offer-First 4); Purple 86 active (Split Screen 19 %, Headline 11 %, Offer-First 10 %; "63 % reduction in pain" from a SleepScore Labs study [c]) [v].
- **Bedding on Meta is volume plus social proof.** Cozy Earth runs **442 active ads at ~36 new creatives a week** (UGC overlays, text-message testimonials, pregnancy and registry life stages). Brooklinen runs 111 active ads at ~29/week (Headline 31 %, Slideshow 18 %) [v] ([Motion: Cozy Earth](https://motionapp.com/library/cozy-earth), [Brooklinen](https://motionapp.com/library/brooklinen)).
- **Sleep aids on Meta are demos with experts.** Hatch runs 40 active ads, ~16/week, Demo 30 %, with doctors and dentists on circadian light; Blissy ~47/week with petri-dish "science" demos [v] ([Motion: Hatch](https://motionapp.com/library/hatch), [Blissy](https://motionapp.com/library/blissy)).
- **TikTok.** Organic reach is tiny for mattress accounts (Casper median 587, Helix 732) and decent for Purple (70.4K, mostly photo carousels) and Coop (27.8K, from daily **TikTok LIVE** selling) [m].
- **OTT/CTV, DOOH and athletes.** Casper "Daymares" ran on OTT; Purple filmed its Times Square screens for social; Saatva, Bear, Helix and Zoma sign athletes and teams; Eight Sleep signs F1 drivers and cycling teams [m].
- **Affiliates and review sites** are a hidden ad channel: DreamCloud pays a flat $150 per mattress, Purple 2–15 %, Mattress Firm 3.2–4 % ([Authority Hacker](https://www.authorityhacker.com/mattress-affiliate-programs/)) [v]. Creators who review mattresses need assets, and so do brand landing pages.

---

## 2. Teardowns: 22 measured posts written up (36 measured in total)

Selection:
- From 435 posts on 44 accounts, I kept posts with (a) the paid signature, (b) a high multiple of the account median, or (c) a format VXO could make.
- I added the brands' newest campaign cuts (Casper "Daymares", Brooklinen "Best Sheets Ever", Eight Sleep Pod 6) and four pinned classics that still define the category (GhostBed, Hostage Tape, Hush, Loftie).
- "Last 2 years" = Oct 2024–Oct 2026; older classics are marked.

Definitions:
- Cut rate = (cuts + 1) ÷ duration. Scene detection undercounts jump cuts on a fixed set (Cozy Earth), so I corrected those by eye from the tiles.
- "Second 1" = what is on screen and in the audio in the first second.

### 2.1 Measured (TikTok)

| # | Ad · date · stats [m] | Length · cuts · rate | Second 1 | Shot list (timecodes) | Turn / punchline | Product interaction | Sound [m] | Text / CTA | Why it sold [inf] |
|---|---|---|---|---|---|---|---|---|---|
| S1 | **Casper "the elusive sleep-deprived adult"** ([link](https://www.tiktok.com/@casper/video/7462089201039740206)) · 2025-01-22 · **5.0M, 14.9 % likes, 224K shares** | 11.3 s · 0 · one handheld take | A curly-haired guide whispers at camera in a yellow dining room: "And here we have…" | 0–3.4 guide, nature-doc whisper; a woman behind him, others filming on phones; 3.4–5.8 "hasn't had a full night's sleep since 2009"; 5.8–9.0 points at her "dark circles"; 9.0–11.3 "Anyway, moving on", the group turns away | A safari tour treats a tired adult like wildlife | **None.** No product, no logo | Whisper VO; −23.0 LUFS; peak −8.9 | Word captions | **Self-recognition and tag-a-friend.** A 4.5 % share rate is extreme. Pure brand reach, not DR. AI could stage it, but the authenticity of a phone take is the point |
| S2 | **Cozy Earth "How long could you rot in bed?"** ([link](https://www.tiktok.com/@cozyearth/video/7556332460485709069)) · 2025-10-01 · **2.4M, 4.0 %** | 25.8 s · ~10 jump cuts · 0.43/s | Two contestants in Cozy Earth PJs on chairs, three made beds and a red LED timer behind; super "HOW LONG COULD YOU ROT IN BED FOR?" | Fixed wide on a branded set; each contestant answers: "two days", "24 hours", "two weeks", "five… maybe seven", "a month", "a year", "30? 50?", 24.2 "I will turn into a bed" | The answers escalate to absurdity | PJs worn, beds on set | Room tone, −13.5 LUFS | Question super + captions | **A contest (#bedrotchallenge) with creators.** Follow-ups by creators hit 1.3M and 1.2M. Product = the set |
| S3 | **Purple "this city never sleeps"** ([link](https://www.tiktok.com/@purple/video/7662494500186524958)) · 2026-07-14 · **921K, 0.10 %** (paid) | 14.8 s · 0 · one take | A phone looks up at a stack of Times Square screens all playing Purple; super "LOOK MOM!!! 👀" | One slow tilt: screens cycle through "We think you're HOT", the GelFlex Grid, an egg/ball drop on the Grid, "This is your back on foam / on Purple", "Try it to believe it", "Any questions?"; 2.5 s second super "I'm in TIMES SQUARE!" | The brand acts like a kid who made it | The ad *is* the product demos on billboards | Music bed (0.57), −14.7 LUFS | Two supers | **OOH turned into a paid social asset (scale = trust).** A FOOH CGI version is AI-native and cheap [inf] |
| S4 | **Purple "This is why editing is so important"** ([link](https://www.tiktok.com/@purple/video/7643869954743323935)) · 2026-05-25 · **508K, 0.11 %** (paid) | 14.8 s · 1 · effects-led | Showroom pan labelled "RAW" | 0–4 RAW showroom; 4–14.8 the same footage "edited": fire VFX, pixel sheep jumping, a cartoon egg character waddling, "Memorial Day Sale", "BEST PRICE OF THE YEAR!!!!" | Making fun of its own sale ad | Showroom beds | Music, beat 0.66, −16.0 LUFS | Sale supers | **A meme template makes a discount watchable.** Mascots from brand lore (egg = egg test; sheep = counting sheep) |
| S5 | **Coop "All Things Sheets: TENCEL"** ([link](https://www.tiktok.com/@coopsleepgoods/video/7509560100625993006)) · 2025-05-28 · **846K, 0.05 %** (paid) | 35.5 s · 12 · 0.37/s | An employee in a sage sweater, selfie framing: "Welcome to our new series" | 0–3.8 host; 3.8–10 her in bed under a duvet, sheet stack; 10–14 host; 14–18 process diagram "100 % eucalyptus"; 18–23 leaf shadows, forest; 23–26 fabric macros "softer than cotton"; 26–30 hand on sheet "refreshingly cool"; 30–33 curtain, airflow; 33–35.5 arms up in bed | None; a series pilot | Hand on fabric | VO, **−30.8 LUFS (very quiet)** | Word captions, series card | **Employee host plus material education.** The series format gives the brand a creative system |
| S6 | **Silk & Snow "complete sleep upgrade"** ([link](https://www.tiktok.com/@silkandsnow/video/7679180195135311122)) · 2026-08-28 · **256K, 0.03 %** (paid) | 11.1 s · 6 · 0.63/s | A navy hybrid on a walnut frame, the shipping box beside it | 0–1.2 bed + box; 1.2–4.1 ¾ bed; 4.1–5.1 **hand presses the quilting**; 5.1–7.6 side angles, night table; 7.6–9.0 a woman sits and lies back; 9.0–11.1 hand presses the edge, "Shop now!" | None | Two hand presses | Music bed (0.59), −24.4 LUFS | "award winning… made in Canada", "free bundle" | **The cheapest possible paid product film.** The hand press is the proof gesture. Product in frame 0 |
| S7 | **DreamCloud "$4,000 for a smart bed?"** ([link](https://www.tiktok.com/@dreamcloudsleep/video/7577811354950634807)) · 2025-11-28 · 91K, 0.06 % (paid) | 59.0 s · 25 · 0.44/s | A moustached guy in a cap looking at his phone, super "$4,000 FOR A SMART BED?" over a rival's product page | 0–3.6 reaction to "$4,100"; 3.6–8 "Meet the DreamCloud adjustable bundle"; then one feature per cut: head/foot elevation, zero gravity, anti-snore preset, cooling, USB ports, massage, under-bed lighting, app; 36–41 "who's actually paying that?"; 41–51 "up to 66 % less"; end card | Price anchor vs a premium rival | Remote, app, lying down | VO, −19.6 LUFS | Feature supers per cut | **Us-vs-them price anchor plus a feature walk.** Black Friday bundle |
| S8 | **Eight Sleep "Introducing Pod 6"** ([link](https://www.tiktok.com/@eightsleep/video/7688692391032753421)) · 2026-09-23 · 84K, **6.9 % likes, 1,950 shares** | 128 s · 22 | Cinematic dark bedroom, VO "Introducing Pod 6" | Hub under the frame; cover on any mattress; "55 to 110 degrees"; "9× more biometric sensors"; Autopilot cases: late dinner, partner's training day, pregnancy, hot flashes, snoring | Personalised scenarios | Hub, cover, app | VO, **−32.4 LUFS (very quiet)** | Spec supers | **Launch film for a cult product.** A long film works at $2,000+ when every line is a new fact |
| S9 | **Casper "Daymares": the cold meeting** ([link](https://www.tiktok.com/@casper/video/7693912828410989837)) · 2026-10-07 · 311 (organic cut of an OTT campaign) | 15.0 s · 6 · 0.47/s | MCU of a **deadpan moustached presenter** in a tan suit: "I'll just pause here and see if you guys have any questions" | 0–2.8 presenter; 2.8–4.2 his screen: a silent conference room; 4.2–6.3 him, smile fading; 6.3–7.8 the room; 7.8–8.9 wide, him on the big screen; 8.9–10.1 an executive's stare; 10.1–13 **him in bed, eyes closed, super "Shhhhhh"**; 13–15 dark wide, Casper on the mattress, "Goodnight, day." | Daytime horror → the bed rescues him | Bed at the end only | −18.0 LUFS; dialogue then silence | "Goodnight, day." | **The Otto register.** Day chaos, then bed. No lips visible in the ending |
| S10 | **Casper "Today was a lot"** ([link](https://www.tiktok.com/@casper/video/7689508057511922958)) · 2026-09-25 · 499 (organic) | 15.2 s · 17 · **1.2/s** | A woman on a rowing machine, super "Today was… a lot" | 0–6 gym, mirror, whiteboard, standing desk, sigh; 6–8 grocery; 8–9 outdoor walk; 9.4 "But my Casper Snow = instant reset", bedroom wide; 10–11 mattress label macro; 11–12 sits, reads; 12–13 remote, LED mood light; 13–15.2 lights off, "Goodnight, day" | The montage resolves in bed | Mattress, label | Music, −15.1 LUFS | Two supers | **A creator's day-in-the-life.** The cheapest version of "Daymares" |
| S11 | **Brooklinen "Best Sheets Ever": therapy** ([link](https://www.tiktok.com/@brooklinen/video/7679098193228860686)) · 2026-08-28 · 1.1K (organic) | 30.0 s · 12 · 0.43/s | Comedian Robby Hoffman sitting up in bed on a laptop: "I mean, do I even need therapy anymore?" | 0–4 bed, laptop; 4–9 her CU "I feel like I'm… good?"; 9–11 "Maybe I'm too comfortable"; 11–18 therapist on call: "you finally found a place that feels truly safe"; 13–15 hand smooths the sheet; 18–20 "Is it my sheets?"; 20–25 overhead, she rolls in bed, "BEST. SHEETS. EVER."; 25–27 navy card "Best in Bed."; 27–30 "Now that we're not working together anymore, we can be friends" | The sheets replace therapy | Hands on sheets, overhead roll | VO/dialogue, −23.4 LUFS | Super slogan + end card | **Celebrity comedy with the product as the cause.** The joke needs the sheets |
| S12 | **Brooklinen "Fitted sheet challenge"** ([link](https://www.tiktok.com/@brooklinen/video/7693569861913480462)) · 2026-10-06 · 14.9K (9× median) | 30.0 s · 13 · 0.47/s | Two athletes in robes at a table with crumpled blue fitted sheets | 2.9 title "Fitted Sheet Challenge"; 6.5 timer **0:30** on screen; overhead and side angles; 15–17 timer 0:05 → 0:00; 17–21 reveal of messy folds; 21–27 a crew member wins; 27–30 laughter | Nobody can fold a fitted sheet | Folding the product | **Peak +1.1 dBFS (clipping)**, −14.8 LUFS | Title + timer | **Universal pain point as a game** |
| S13 | **Hostage Tape "this is gonna sound really weird"** ([link](https://www.tiktok.com/@hostagetape/video/7212371894035680558)) · 2023-03-19 (classic) · **4.9M, 4.7 %** | 21.6 s · 5 · 0.28/s | ECU: a bearded man in a beanie peels a black mouth tape off his lips | 0–2.8 tape off; 2.8–4.8 asleep on a pillow with the tape on; 4.8–19 to camera on a saturated blue backdrop, animated supers "GAME CHANGER", "#BIOHACKING", "1UP", "HEALTHY"; 19–21.6 points at the tape on his mouth | Confession of a weird habit | Tape in frame 0 | VO, −23.9 LUFS | Kinetic word captions | **A visual oddity in frame 0** (black tape on a mouth) + biohacker identity |
| S14 | **Hush "sleep debt"** ([link](https://www.tiktok.com/@hushblankets/video/7202609518818135302)) · 2023-02-21 (classic) · **4.6M, 12.1 %, 87.8K shares** | 56.8 s · 7 | Green-screen creator, super "PSA: You're probably in Sleep Debt" | Talking head over articles; 40–47 calculator "730" hours; 47–54 body-diagram article; ends "in the next video…" | 2 h × 365 = 730 h | **None** | VO, −26.7 LUFS | PSA super | **Education plus a number plus a serial hook** |
| S15 | **SomniFix "I'm a mouth taper, of course…"** ([link](https://www.tiktok.com/@somnifix/video/7366768814354369838)) · 2024-05-08 · 772K, 1.55 % | 30.0 s · 6 · 0.23/s | A creator holds a strip by her lips: "I'm a mouth taper, of course I'm getting the best night's sleep of my life" | Seven outfits and locations, one claim each: sleep, "jawline more defined", "mental health", "no funny business after 10", morning breath, "10× more productive", telling everyone | Self-aware smugness | Strip in hand each shot | VO, **−34.3 LUFS** | Captions | **A meme format with a repeated line.** Several claims are unsubstantiable (§5) |
| S16 | **Leesa "LeesaBot"** ([link](https://www.tiktok.com/@leesasleep/video/7379638046100081963)) · 2024-06-12 · **1.7M, 0.12 %** (paid) | 37.6 s · 0 · one locked take | An actor in glasses at a window: "Hey there, tired humans. I'm LeesaBot, your always-awake AI sleep expert" | One medium shot; "I've observed countless nights… Creepy? Maybe. Accurate? Definitely… I'm always watching… don't worry, I won't actually watch. Probably." | Creepy-but-kind AI persona | None | Dialogue, −25.9 LUFS | Captions | **AI as the comedy subject, played by a human.** Shows paid appetite for an "AI" character |
| S17 | **Gravity "blanket fort with a weighted blanket"** ([link](https://www.tiktok.com/@gravityblankets/video/7219369411881258283)) · 2023-04-07 · 275K, 1.77 % | 10.3 s · 0 · one take | A woman and a dog under a crochet blanket fort; a man holds a purple weighted blanket above it; super "pov you tried to make a blanket fort with a weighted blanket" | 0–4.5 he lifts and spreads it; 4.5–5 drops it on the roof; **5–7 the fort collapses flat**; 7–10.3 he peels it back, she and the dog lie flat | **The product's weight causes the collapse** | The product is the gag | **−10.0 LUFS, peak +2.0 dBFS (clipping)** | POV super | **A product-caused physical joke in 10 s.** VXO's grammar exactly |
| S18 | **Loftie "Brown noise FTW"** ([link](https://www.tiktok.com/@byloftie/video/7111327560474185003)) · 2022-06-20 (classic) · **1.5M** | 22.0 s · 3 | An off-white card, "White Noise", with white noise playing | Colour-field cards, each with its own noise: white 0–7, red 7–10 (water caustics), grey 10–16, pink 16–?, blue, brown | Which colour is yours? | None (the sounds are the product) | Noise only, −13.9 LUFS | Name of each noise | **Sound as the product; ASMR-adjacent comment bait.** Visuals are AI-trivial |
| S19 | **Pluto "a pillow is secretly a personality test"** ([link](https://www.tiktok.com/@plutopillow/video/7638716366454918413)) · 2026-05-11 · 8.9K (8× median) | 18.7 s · 4 | A white pillow on grey seamless, super "a pillow is secretly a personality test" | 0–6.4 pillows tossed onto the sweep with quote tags ("I sleep on my side but wake up somewhere else"); 6.4–7.9 quilting macro "we make yours"; 7.9–8.8 **gloved hands at a sewing machine**; 8.8–18.7 a man lies down on the pillow, blue night light, "Sleep is personal" | One pillow per person | Pillows, sewing | Music, −29.2 LUFS | Supers + URL | **Customisation shown as craft.** The paid 48 s founder cut (53K, 0.13 %) adds "200,000 customers… 125 nights" [c] |
| S20 | **Hatch Baby, reply to a comment** ([link](https://www.tiktok.com/@hatchbaby/video/7556346079147511053)) · 2025-10-01 · 17.9K (27× median) | 14.9 s · 3 | Comment sticker ("What's the difference?") over the device glowing amber in a nursery | 0–3 device in the nursery; 3–4.5 a finger presses the big button; 4.5–9.3 app screens, sleep consultants; 9.3–14.9 device colour changes with the app | "A $1,000 sleep coach for $99" (caption) | Hands + app | VO, −26.0 LUFS | Sticker | **Hands-only feature demo answering a real question.** No baby on screen |
| S21 | **Nectar "the magic of the split king bundle"** ([link](https://www.tiktok.com/@nectarsleep/video/7623141169647717662)) · 2026-03-30 · 18.3K (6× median) | 10.8 s · 1 | A sunlit bedroom, two split adjustable bases; serif super types on | 0–4.6 split king, title; 4.6–10.8 locked wide: a person makes the bed in fast motion, duvet, pillows, throw | Two beds become one | Bed-making | Song, peak +0.1 dBFS | Title | **"Sleep divorce" without the word.** Time-lapse is AI-friendly |
| S22 | **GhostBed / Leesa: the paid-UGC and meme-sound class** (GhostBed [link](https://www.tiktok.com/@ghostbed/video/7021535968595381510) 2021, **14.1M, 0.50 %** paid; Leesa "unicorn man" [link](https://www.tiktok.com/@leesasleep/video/7274006441772584238) 2023, **10.8M, 0.84 %**) | 33.1 s / 5.0 s | GhostBed: a couple carries a rolled mattress to a bed; Leesa: a girlfriend walks in to see a real mattress on a frame, super "When his bachelor pad bedroom doesn't have a mattress on the floor" | GhostBed: unroll 0.4–7.8, cut-open 7.8–11.9, logo macro, hand press "It's even cool to the touch!", logo; Leesa: one locked shot, trending audio "this place is magnificent" | Leesa: the bar is on the floor | Unboxing / mattress as set | −13.8 / −15.5 LUFS | Green caption boxes / meme super | **UGC unboxing with a quiz CTA; meme audio over a product.** Both are older; they set the floor for "paid UGC" |

**Supporting, measured but not in the table:**
- Casper "WFH almost worked" (9 s, 485K, 2022), a laptop on a Zoom grid with a muffled snore.
- Casper "underslept text" (7 s, 319K, 2023).
- MyoTape podcast clip on the "glymphatic system" (25.7 s, 190K, 0.40 % paid).
- PlushBeds fiberglass creator story (62 s; "less than 1 % of mattresses match their purity certifications").
- DreamCloud "5 reasons you shouldn't buy a DreamCloud" (68 s, 31 cuts, reverse-psychology yapper).
- Eight Sleep Hub redesign (144 s, 35 cuts).
- Purple photo carousels "Are you sleeping yet?" (82K), "better sleep is right under here" (96K) and "Squishies" (118K, 1.8 % likes): audio-only downloads, so no tile.
- Hostage Tape's 2026 AI-voiced "dream/mythology" story carousels (343 s, 50K; 60 s, 2.9K) [inf: synthetic narration over stills].

### 2.2 Metadata only (YouTube blocked; press descriptions)

| Ad | Date · length | What it is | Evidence |
|---|---|---|---|
| Casper **"Daymares"** ("Birthday Boy", "Crowded", "Poor Connections") | Apr 2026 · :30/:15 | An awkward party, a crowded elevator and a bad call, shot like horror; cut to the person peacefully in bed; "Goodnight, day." The word "mattress" is never said. Orchard Creative; OTT + digital | [AdForum](https://act.adforum.com/agency/6700077/creative-work/34733216/birthday-boy/casper), [Bedding News](https://beddingnewsnow.com/?p=14051); YouTube TORNI5rnCbg (2.3K views) |
| Purple **raw-egg test** (classic) | ~2018 · ~2–4 min | Four raw eggs glued under a 330 lb tempered-glass pane dropped from ~3 ft onto Purple vs other beds; Harmon Brothers; "194M views" [c]; Purple's own disclaimer: "not a scientifically designed clinical study" | [Furniture Today](https://www.furnituretoday.com/mattress-bedding-news/purples-clever-egg-test-racks-online-views-wins-fans), [Spectacle](https://spectacle.is/video/how-to-use-a-raw-egg-to-determine-if-your-mattress-is-awful-purple-mattress) |
| Casper **"Casper Sleepers"** | 2022–23 | VaynerMedia: a TikTok became a real job posting for paid sleepers; Cannes-listed; Casper's best TikTok "of all time" [c] | [Cannes Lions](https://www.lovethework.com/work-awards/campaigns/casper-sleepers-1529682) |
| Spring Air **AI Bears** | Jul 2026 | AI-generated mascot-bear video campaign for the Back Supporter Hybrid; launched at Las Vegas Market | [Bedding News](https://beddingnewsnow.com/blog/2026/07/14/spring-air-will-debut-new-ai-generated-campaign-at-las-vegas-market/) |
| Symphony Sleep **"The Tank"** (AI) | Apr 2026 | Adjustable-base durability; written and directed by the president; YouTube, TikTok, IG, LinkedIn; results not reported | [BedTimes](https://bedtimesmagazine.com/2026/04/symphony-sleep-leverages-ai-for-new-marketing-campaign/) |
| Kingsdown **AI-revived archive ads** | Aug 2025 | 1960s print ads re-imagined with gen-AI | [Furniture Today](https://www.furnituretoday.com/mattress-bedding-news/kingsdown-uses-ai-to-revive-ads-and-train-retail-teams) |

### 2.3 What the measured set says [m]

- **The product is in frame 0 in ~15 of 36** (Silk & Snow, Purple ×3, Hostage Tape, SomniFix, Gravity, Pluto, Hatch, Nectar, GhostBed, Leesa unicorn, PlushBeds, Brooklinen ×2). **But the 4 biggest organic posts (Casper 5.0M, Hostage 4.9M, Hush 4.6M, Cozy Earth 2.4M) show no product being used in second 1.** Three show none at all, and Hostage shows only tape coming off a mouth. Sleep's reach is about the *state* (tired, rotting in bed); its paid winners are about the *object*.
- **Paid-signature lengths:** 11.1, 14.8, 14.8, 25.7, 33.1, 35.5, 37.6, 48.3 and 59.0 s → **median 33.1 s**. The distribution is bimodal: ≤ 15 s product/OOH films and 33–59 s explainers or price anchors. This matches doc 45 D29 and doc 53.
- **Cut rate is not the lever.** One-take posts dominate the top (Casper 0 cuts, Leesa 0, Gravity 0, Purple NYC 0). The fastest edits (Casper "Today was a lot" 1.2/s) got the least reach. **Sleep rewards a held frame.** Benly agrees: "Slow Cinematic" pacing has the longest median life in Home & Living (30 d, 53 % 30-day survival) [v].
- **Two families of format sell here:**
  1. **"Name my tired"**: identity, relatable states, education and contests (Casper documentary, Hush debt, Cozy Earth bed rot, Daymares, SomniFix meme). Character- and situation-led, often product-free.
  2. **"Show me it works"**: hand press, egg/glass drop, unboxing expansion, feature walk, price anchor (Silk & Snow, Purple, GhostBed, DreamCloud, Coop, Hatch). Object-led.
  VXO can build family 1 with Otto-style deadpan and family 2 as product films. **The money is in combining them: a family-1 hook head on a family-2 body.**
- **Audio QC is a real differentiator.** Loudness ranges from **−9.7 to −34.3 LUFS**. Four posts peak above 0 dBFS (Gravity +2.0, Brooklinen +1.1, Purple carousel +0.7, Nectar +0.1). **11 of 36 are quieter than −24 LUFS** (Coop −30.8, Eight Sleep −32.4, SomniFix −34.3, Pluto −29.2/−26.0, Hush −26.7, Hatch −26.0, Leesa −25.9, DreamCloud −27.0, Casper WFH −28.5, Silk & Snow −24.4). Sleep brands confuse "calm" with "quiet". A calm mix at −14 LUFS / ≤ −1 dBTP (doc 46) is a concrete edge to pitch.
- **Photo carousels are a real format here.** Purple's 82–118K carousels and Hostage Tape's narrated carousels arrived as audio-only files. **Ship 6–10 stills with every sleep film (LESSONS: furniture/home ads are 70 % images).**

---

## 3. What converts in this niche (data)

| # | Finding | Number | Source | Status |
|---|---|---|---|---|
| N1 | **Home & Living** effectiveness by asset type (Meta) | **Product Shot 66** (32 d median, 51 % survive 30 d), UGC 62, Branded/Studio 36, Lifestyle 30, Graphic 30; median life 25 d; **video 41 %** | [Benly H&L Q1 2026](https://benly.ai/benchmarks/q1-2026/home-living) | [v] longevity-based |
| N2 | **Bedding & Bath** (18 brands, 4.0K creatives) | **Branded/Studio 65**, Product Shot 64, Lifestyle 54, UGC 45, Graphic 36; median 27 d; 45.1 % survive 30 d; **video 45.8 %**; hooks Bold Statement 31.2 %, Visual Intrigue 21.9 %, Pattern Interrupt 18.1 %, Pain Point 16.5 %; **Discount 57.7 %**, Free Offer 15.2 %, New Launch 11.6 % (rising from 7 % to 17 % Jan → Mar) | [Benly Bedding & Bath](https://benly.ai/benchmarks/q1-2026/home-living/bedding-bath) | [v] |
| N3 | **Furniture** (closest proxy for mattresses) | Avg life **56 d**, video **30 %** | Benly H&L sub-industry table | [v] |
| N4 | Home & Living, Q2 creative genome | "Calm" is the signature attribute (3.6×); **Hands Only is the top talent (14.6 %)**; Slow Cinematic 30 d / 53 %; **AI-Generated 30 d median, 55 % 30-day survival, highest effectiveness index**; Stock Footage worst (13 d, 29 %) | [Benly Q2 H&L](https://benly.ai/benchmarks/q2-2026/home-living) | [v] |
| N5 | **Health & Wellness** (proxy for sleep aids) | Lifestyle 62, Motion/Animation 61, Graphic 59, UGC 57, Branded 52; median **21 d**; video 47.9 %; hooks Bold Statement 41.9 %, Pain Point 19.8 %; Discount 54.3 %, **Free Offer 24.1 %**; Medical Devices avg life 46 d | [Benly H&W](https://benly.ai/benchmarks/q1-2026/health-wellness) | [v] |
| N6 | Meta "sensitive category" | Since Jan 2025, health & wellness advertisers can lose Purchase/Add-to-Cart optimisation events; agencies claim a 30–40 % efficiency drop [unverified] | [Click](https://www.click.co.uk/insights/metas-new-advertising-restrictions-impacts-health-and-wellness-brands/), [Polar](https://www.polaranalytics.com/post/2025-metas-tracking-restrictions-for-health-wellness-are-here----heres-how-to-fix-it) | [v] |
| N7 | Mattress unit economics | Historic DTC CAC ~$200–300+ per mattress; Casper spent ~$0.30–0.33 per $1 of revenue on marketing; returns estimated at 12–14 % [unverified] | [Bedding News](https://beddingnewsnow.com/?p=3914), [Retail Dive](https://www.retaildive.com/news/dtc-brands-struggled-with-profitability-prior-to-covid-19-now-what/580689/) | [v] dated |
| N8 | Buyer research | 37 % use AI tools; 49 % start on Google; 33 % abandon from confusion; 18 % regret firmness | [Amerisleep](https://amerisleep.com/blog/state-of-mattress-buying/) | [v] |
| N9 | Night buying | 72 % bought online after their usual bedtime (avg $165/yr); 23 % reported remorse | eachnight via Amerisleep | [v] |
| N10 | Brand Meta formats | Casper: Split Screen, Offer-First, Us vs Them, Yapper; Purple: Split Screen, Testimonial, Us vs Them, Listicle; Saatva: Demo, Celebrity/athlete, Podcast, BTS (19/20 video); Cozy Earth: UGC overlay, text message; Hatch: Headline, Demo, Listicle; Blissy: Yapper, Offer-First, Skit | Motion pages (§1.6) | [v] |
| N11 | Cross-industry (doc 45) | Unboxing 9.83 %, BTS 8.64 %, founder 8.57 %, demo 8.11 %, **cinematic b-roll 6.85 %**; hooks newness 11.37 %, sale 11.35 %, price anchor 10.89 % | doc 45 D3–D5 | Read |
| N12 | AI in this niche | Spring Air, Symphony Sleep, Kingsdown ship AI ads; Boll & Branch uses AI for imagery and copy; no performance disclosed | §2.2 | [c] |

### 3.1 What this means, by sub-niche [inf]

| Sub-niche | Lead format | Proof that sells | Length | VXO's role |
|---|---|---|---|---|
| **Mattresses** | Sale-event product film; us-vs-them price anchor; hand press; unboxing; motion-isolation/egg-style test | **Real test footage** (glass, egg, bowling ball), trial length, warranty, certifications (CertiPUR-US, GOTS), reviews (real) | 6–15 s per tentpole + 30–45 s anchor | **One hero film per tentpole + 3 hook heads + stills**; the client's real test sits in the proof slot |
| **Pillows** | Customisation craft; sleeper-type quiz; slow-rebound macros | Trial nights, fill adjustability, real reviews | 10–20 s; 45 s founder cut | Craft/material macros, personality-test comedy |
| **Sheets, duvets, sleepwear** | Texture macros, colour drops, celebrity/creator comedy, challenges | Material story (TENCEL, percale, GOTS), wash test (real), registry/gift moments | 6–15 s drops; 30 s comedy | **Drop film per colourway/collab (Season plan)**; texture-first one-takes |
| **Weighted blankets** | Physical gags (the weight does something), calm ASMR | Weight options (10 % of body weight), knit vs beads | 8–15 s | **Product-caused physical comedy** (the fort collapse is the template) |
| **Masks, sound, light, earbuds** | Sound/light as the product (Loftie), demo with hands, couple/snoring situations, expert | Specs (lux, dB, battery), app UI, real reviews | 10–20 s | **Sound-first films** (VXO's audio QC is the selling point); dark-to-light reveals |
| **Mouth/nasal tape** | Confession hook, meme formats, podcast experts | Only real testimonials with typicality; no apnea or jawline claims | 15–30 s | Ritual and identity films only; avoid health outcomes (§5) |
| **Sleep tech (cooling/heating)** | Long launch film; partner-split scenarios | Temperature range, sensors, athletes | 15 s hook + 60–140 s launch | Partner-split comedy and hook heads for existing launch films |

**Placements:**
- Meta Reels and Feed. Product films with supers burned in; 4:5 cut for Feed; a 6 s loop for every sale. Bedding's Meta mix is ~46 % video, mattress ~25–30 %.
- TikTok In-Feed and Spark. Meme/one-take hook heads; replies to comments (Hatch).
- TikTok LIVE and Shop. Coop's daily LIVE drives its 27.8K median, and bedding AOV runs $35–65 on TikTok Shop [v] ([Dashboardly](https://www.dashboardly.io/tiktok-shop/bedding-pillows)).
- CTV/OTT for the brand campaign (Casper).
- **Night dayparting (22:00–02:00 local) for sleep aids** [inf from N9].

**AI disclosure:** follow doc 45 §5.3. In this niche, show hands, beds and objects; avoid AI faces in testimonials; the default end line is "Made with AI. The test is real." `[inf]`

---

## 4. AI realism pitfalls in this niche, and the fixes

Routing follows doc 43 §1. New niche items are marked **NEW**. Every motion shot starts from an approved still (doc 17). "Proof slot" = 1.5–3 s of the client's real footage.

| Pitfall | What goes wrong | Fix (prompt / reference / model) |
|---|---|---|
| **NEW: Sleeping bodies** | AI sleepers look dead (no breath) or twitch; eyelids flutter; faces morph when the head turns on the pillow | "Chest and duvet rise ~1 cm every 4 s (15 breaths/min); eyelids closed and still; one small head shift at [t] only; face ≤ 20° turn". Keep sleepers ≤ 5 s per shot; Kling 3.0 Pro i2v from a real-photo still; or show the back of the head / under-duvet silhouette |
| **NEW: Two people in one bed** | Limbs merge under the duvet, a third leg appears, partners swap sides | Distinct pyjama colours in the sheet; "arms above the duvet, exactly 2 arms each"; FIRST FRAME AND BLOCKING with each person's side ("she is always screen-left"); ≤ 2 people per bed; Seedance 2.5 r2v with both character refs |
| **NEW: Fabric physics (sheets, duvets, weighted blankets)** | Cloth floats "underwater", fluffs up forever, passes through bodies, a fitted sheet's elastic corners vanish | Name the fabric and weight: "300-thread-count percale, crisp, holds sharp creases; falls 1 m in ~0.5 s"; "duvet, 1 kg, billows once and settles in 1.2 s"; **"weighted blanket, 7 kg glass-bead fill, drapes instantly, no billow, no flutter, conforms to the shapes beneath"**; "elastic corners hug the mattress"; Kling first/last frame for a single drop; doc 43 PHYSICS block |
| **NEW: Foam and mattress deformation** | A hand sinks too far or too little; the print vanishes instantly or never; springs show through; the mattress bends like cloth | Write the physics: "memory foam: the hand sinks ~4 cm in 0.5 s; on lift, the print recovers slowly over ~5 s"; "latex/hybrid: springs back in < 0.3 s"; "the mattress is a rigid 30 cm block; edges stay square"; Kling 3.0 Pro i2v first/last frame (press still → released still) |
| **NEW: Mattress-in-a-box expansion** | The roll grows to the wrong size; expands in 0.2 s; plastic stays on; the logo border jumps | "Vacuum film is slit with a cutter, a 1 s hiss; the roll unfurls flat in ~2 s; the foam rises from ~5 cm to its full 30 cm over ~60 s (shown as a time-lapse cut, not in one second)"; label only from the ref; any expansion claim (time to full height) comes from the client |
| **NEW: Bed geometry and continuity** | The number of pillows changes per cut; the duvet colour shifts; the bed changes size (queen ↔ king); the headboard morphs | Locked set statics (doc 43 §3: one locked-off video of the set, screenshot elements); "**exactly 4 pillows, 2 euro shams**, [colour] duvet, queen 152 × 203 cm, walnut headboard 120 cm high"; check pillow count in every frame strip |
| **NEW: Darkness and night light** | Night turns into muddy noise; faces go grey; the "dark" scene is lit like noon; lamp colour drifts | "Practical bedside lamp 2,700 K as the only key, falloff to near-black; cool moonlight 4,100 K rim from the window; expose for the face; deep blacks, no crushed noise"; render the dark shot from a graded still; QC rule: the hero frame's mean luma stays above ~15/255 so the product still reads on a phone |
| **NEW: Glow devices (sunrise lamps, LED, screens)** | The glow bleeds and pulses randomly; the colour cycles wrong; app UIs garble | "Lamp ramps smoothly from 0 to warm amber over 3 s, no flicker"; app UI only as a post comp of the client's real screenshots; never AI text on screens |
| **NEW: Liquids on beds (wine glass, egg tests)** | The liquid level jumps; the glass slides; the egg changes shape; physics too good to be true | **These are demonstrations of a claim → the real test is the client's footage (proof slot).** AI may stage the setup and the reaction, never the result. If AI must show the glass in a non-claim shot: "one glass, 150 ml of red wine, the surface stays flat; the glass never moves" |
| **NEW: Mouth tape, masks, earbuds on faces** | Tape warps the lips; strap geometry changes; earbuds sit inside the ear canal wrongly | Product on the face only from a real photo still (Kling i2v, ≤ 3 s); never animate speech through tape; prefer the product in hand or on the nightstand |
| **NEW: Babies and cribs** | Any AI infant; a crib with pillows/bumpers/blankets = unsafe-sleep imagery | **Never generate babies (LESSONS).** Nursery shots show an empty, bare crib (AAP: back to sleep, nothing in the crib); weighted products never near an infant (§5) |
| **NEW: Pets on beds** | Paws multiply, a dog merges into the duvet | One animal per shot, ≤ 5 s, from a real photo (Kling), LESSONS rule |
| Hands on fabric | Fingers fuse into creases | Name contact points ("palm flat, four fingers spread, thumb tucked"); 5 fingers lock; doc 43 §5 |
| Labels and law tags | Text garbled or invented | Text only from the ref; supers in post; no AI-written certification seals |
| Packaging | Box size wrong; logos drift | Measured box from the client (e.g. 107 × 46 × 46 cm queen) in the prompt; Kling i2v for packshots |

**Model routing for this niche** (doc 43 §1, §6 list prices [EST]):

| Shot type | Model | Settings | Cost per take |
|---|---|---|---|
| Product insert (hand press, pillow, mask, lamp, label) | Kling 3.0 Pro i2v | 5 s, `sound:"off"`, `cfg_scale` 0.5, `last_image_url` | $0.48 |
| State change (press → recovery, duvet drop, box → unrolled) | Kling 3.0 Pro i2v first/last frame | 5 s, path only | $0.48 |
| Hero bed one-take (slow dolly-in, morning light sweep) | Cinema Studio 4.0 | `pacing:"single-shot"`, `camera_movement:"dolly-in"`, `light:"window"`, 720p, 8 s | $3.70 |
| Comedy multi-shot with people (Daymares-style, deadpan) | Seedance 2.5 r2v | 9:16, 10–15 s, "exactly N shots", product = first ref | $3.09 (480p proof) / $6.93 (720p, 15 s) |
| Sleeper close-ups (breathing, one turn) | Kling 3.0 Pro i2v from a real-photo still | ≤ 5 s | $0.48 |
| Sound-as-product films (noise colours, rain) | **Stills + parallax in edit**; 1–2 Kling inserts | — | ~$2–4 |
| Dialogue to camera (spokes-character) | Seedance 2.5 dialogue block, or Wan 3.0 r2v + `audio_urls` (doc 43 §7.4) | ≤ 12 s per line | $1.00 per 10 s (Wan 720p) |
| Blocking previs | Wan 3.0 r2v 480p | fixed seed | $0.50 / 10 s |
| Any test result (glass, egg, cooling, sleep score) | **Real proof slot** from the client | 1.5–3 s | $0 |

**Style header delta (add to doc 11's headers for this niche):** "Bedroom product film, real textiles with visible weave, crisp percale creases or soft sateen sheen as specified, foam that compresses and recovers at a real speed, exactly [N] pillows, [bed size] in cm, practical warm lamp 2,700 K and cool window light, deep but clean blacks, label text '[EXACT]' is the only readable text, sleeping bodies breathe slowly, exactly five fingers per hand, no babies, no visible brand other than the client's."

---

## 5. Policy and legal (US first; the client's counsel has the final word)

### 5.1 Claim lines by product

| Product | Status | Safe on screen | Never on screen | Source |
|---|---|---|---|---|
| Mattresses, pillows, sheets | Consumer products (CPSC flammability: 16 CFR 1632/1633 for mattresses) | Comfort, feel, materials, trial, warranty; **"better sleep" as puffery** (NAD treated "better night's sleep" and "fully charged" as puffery) | Comparative superiority ("more supportive than memory foam") without head-to-head tests (NAD, Tempur v. Simmons); pain cure/medical claims; "orthopedic" or "chiropractor recommended" without the real endorsement | [NAD Simmons](https://bbbprograms.org/media/newsroom/decisions/simmons-memory-foam) |
| "Organic", "natural", "non-toxic", "VOC-free" | FTC Green Guides; first FTC "organic" case was a mattress maker | Certified claims with the certifier's real mark (GOTS, GOLS, Greenguard Gold) | Self-made seals, "organic" for mostly synthetic foam, "plant-based" foam with little plant content, "emissions-free" (FTC v. Moonlight Slumber, 2017) | [FTC Moonlight Slumber](https://search.ftc.gov/news-events/news/press-releases/2017/12/ftc-approves-final-consent-order-moonlight-slumber-llc-advertising-case), [Kelley Drye](https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/moonlight-slumber-says-goodnight-to-misleading-and-unsubstantiated-organic-advertising-claims-after-settlement-with-ftc) |
| "Made in USA" | FTC Made in USA Labeling Rule (civil penalties) | Only "all or virtually all" US-made, from the client's written basis | "Proudly made with 100 % USA-made materials" when finished overseas (Resident Home/DreamCloud, **$753K**); "crafted in the US" for imports (Williams-Sonoma PBTeen pads, 2024) | [ISPA on FTC](https://sleepproducts.org/?p=10888), [Claims Journal](https://www.claimsjournal.com/news/national/2024/04/30/323301.htm) |
| Prices and sales | FTC Guides Against Deceptive Pricing; state laws (CA 90-day rule) | Real current price; dated offers that really end | **Fictitious "was" prices**, perpetual sales, "limited offer" that never ends, "free pillows" not actually available (NAD v. Nectar, referred to the FTC 2019) | [NAD Nectar](https://bbbprograms.org/media/newsroom/decisions/nad-refers-nectar-sleep-to-ftc), §0 item 5 |
| Cooling / temperature claims | Substantiation | Measured specs ("55–110 °F", Eight Sleep [c]) | "Sleeps X° cooler" without a test protocol; a thermal-camera AI shot as proof (mock-up) | doc 47 §4.3 mock-up rule |
| Sleep-score / pain stats | Substantiation | The client's study, footnoted ("63 % reduction in pain… SleepScore Labs study" [c, Purple]) | AI-visualised outcomes; unattributed percentages | Motion: Purple |
| White-noise, light, masks, earbuds | General wellness (FDA guidance, revised 6 Jan 2026) | "Helps you wind down", "blocks light", "masks noise" | Treats insomnia, anxiety, ADHD, sleep apnea (disease claims → device authorisation) | [Faegre Drinker](https://faegredrinker.com/en/insights/publications/2026/1/key-updates-in-fdas-2026-general-wellness-and-clinical-decision-support-software-guidance) |
| Anti-snoring mouthpieces, chin straps | **Class II device** (21 CFR 872.5570) when they claim snoring reduction | The cleared indication only | Apnea, "cure snoring" beyond the clearance | [FDA 510(k) K250028](https://www.accessdata.fda.gov/cdrh_docs/pdf25/K250028.pdf) |
| Mouth tape | Unclear status; Amazon reportedly stopped mouth-tape sales in 2023 [unverified] | "Encourages nasal breathing" (if substantiated), ritual, comfort | Apnea, jawline, mental-health, productivity, children's use claims (MyoTape sells a kids' book [m]: **never target children**); 2025 PLOS ONE review warns of asphyxiation risk with nasal obstruction | [PLOS ONE review](https://pmc.ncbi.nlm.nih.gov/articles/PMC12094774), [HealthDay](https://www.healthday.com/health-news/sleep-disorder/mouth-taping-for-better-sleep-little-benefit-lots-of-risk-review-says) |
| Weighted blankets | Consumer product | Adults; "about 10 % of body weight" guidance from the client | Any infant/toddler use; CPSC and AAP warn against weighted infant swaddles, sacks and blankets (retailers pulled Dreamland Baby, Nested Bean); a ban bill is proposed | [CPSC Trumka](https://www.cpsc.gov/About-CPSC/Commissioner/Richard-Trumka/Statement/Beware-Weighted-Infant-Swaddles-and-Blankets-Are-Unsafe-for-Sleep-Retailers-Should-Consider-Stopping-Sales), [CBS](https://www.cbsnews.com/amp/miami/news/safety-concerns-arise-over-weighted-baby-sleeping-products-after-cpsc-warning) |
| Infant sleep products (sound machines, monitors) | Safe Sleep for Babies Act (2022) bans inclined sleepers and crib bumpers | Empty crib, baby on back, room-sharing imagery from the client | Pillows, bumpers, blankets or positioners in the crib; any AI baby | AAP/CPSC [inf] |

### 5.2 FTC, NAD and courts
- **Mock-up doctrine.** An AI shot of a wine glass that doesn't spill, an egg that doesn't break, a cooler body or a better sleep score is a demonstration. Allowed only as obvious metaphor with "Dramatization", and only when the claim is proven elsewhere (doc 47 §4.3). **House rule: the result is the client's real test.** Purple itself captions its egg test as "not a scientifically designed clinical study".
- **Fake reviews rule (16 CFR 465).** No AI customers giving verdicts, no invented review cards, no "200,000 happy sleepers" super unless the client's data supports it. Mattress review sites have a history of undisclosed affiliate conflicts; creator reviews need #ad and real use (16 CFR 255).
- **Comparative ads.** Never show a rival's trademarked mattress, its colour grid or its billboard in an AI frame. DreamCloud's "$4,000 smart bed" anchor shows a rival web page; VXO uses a generic "$4,000 smart bed" only with the client's legal-approved comparison.
- **Reference prices** (§0 item 5). End cards carry the dated offer and the exact sale terms; strike-through prices only with written price history.
- **Subscriptions** (mouth-tape refills, Hatch Sleep membership, Eight Sleep Autopilot) fall under ROSCA/negative-option rules; show the client's exact terms.
- **Right of publicity.** No celebrity look-alikes (Brooklinen pays real celebrities; we never fake one). The "sleep-deprived adult" documentary format must not imitate a specific famous narrator's voice.
- **Music and sounds.** White/brown-noise and rain beds must be licensed or generated with rights; trending TikTok sounds (Leesa's) are not licensed for paid ads outside TikTok's commercial library.

### 5.3 Platform rules
- **Meta, adult nudity and sexual activity.** Bed scenes are fine; "sexually suggestive poses" and implied nudity are not ([Meta](https://transparency.meta.com/policies/ad-standards/objectionable-content/adult-nudity-and-sexual-activity)). Couples stay in pyjamas, duvets at chest height, with no innuendo gestures. SomniFix's "no funny business after 10" is a line Meta reviewers may flag `[inf]`.
- **Meta, personal health.** No negative self-perception addressed to the viewer ("Look at your dark circles"). Casper's documentary works organically because a third person is teased, but **don't run it as a paid ad that targets the viewer** `[inf]`.
- **Meta, "sensitive category" data restrictions** for sleep-aid and wellness sites (N6). Expect weaker optimisation; creative must carry more of the load (an argument for VXO's variant packs).
- **TikTok, Healthcare & Pharmaceuticals** (updated Dec 2025). Medical devices need market approval and 18+ targeting; no medical claims or exaggerated performance ([TikTok](https://ads.tiktok.com/help/article/tiktok-ads-policy-healthcare-pharmaceuticals?lang=en)).
- **Minors.** No teen-coded characters in sleepmaxxing ads; no children with mouth tape; no infants with weighted products.
- **AI disclosure.** Doc 45 §5.3 (Meta AI info, TikTok AIGC toggle, the New York synthetic-performer law in force 9 Jun 2026). Hands-only and empty-bed films are the lowest-risk AI films in this niche.

### 5.4 Pre-flight checklist for this niche (add to doc 45 §5.4 and doc 46 §7)
1. Every claim on screen is on the client's approved list, with its footnote. No disease verbs (treats, cures, prevents insomnia/apnea/anxiety/pain).
2. No AI frame shows a test result (glass, egg, cooling, sleep score, pain). Results appear only in the real proof slot.
3. Price supers carry dates and real terms; no struck-through price without 90-day history; "free" items are actually available.
4. "Organic", "non-toxic", "Made in USA" only with the client's written basis and the real certifier marks.
5. Pillow count, bed size, colour and label match the reference in every frame (frame strip at 2 fps).
6. No babies; no infant near any weighted product; cribs empty.
7. No rival's product, colour or billboard in any AI frame; no celebrity look-alikes or sound-alikes.
8. Couples: pyjamas on, no suggestive framing.
9. Disclosure line present when an AI person appears; #ad on any creator cut.
10. Audio master −14 LUFS, ≤ −1 dBTP. **Calm ≠ quiet:** 11 of 36 measured posts were too quiet and 4 clipped.

---

## 6. The buyer

### 6.1 Who signs a $1,200–3,500 film

| Brand stage | Who decides | How they buy | Evidence |
|---|---|---|---|
| < $10M sleep-aid or pillow/bedding brand (masks, sound, tape, weighted, custom pillows) | **The founder**, who often runs the Meta ads personally (Hostage Tape's founder did at $14M [v]) | Card after seeing frames; launch- or calendar-driven; a Short to test | Hostage Tape, Pluto, Loftie, Manta |
| $10–90M bedding or DTC mattress (Brooklyn Bedding, Avocado, PlushBeds, Sunday Citizen, Silk & Snow) | **Head of Growth/Performance** + **creative director**; founder approves brand work | Needs volume per tentpole: hero + hook heads + 6 s loops + stills; Season plan | Weekly creative cadence of 4–47 new ads (Motion) [v] |
| $100M+ / corporate (Purple, Casper, Tempur, Sleep Number, Cozy Earth, Brooklinen) | CMO + agency (Orchard, Harmon Brothers, VaynerMedia) | Out of lane, or only via their agencies | §1.2 |

### 6.2 What they fear (ranked) [inf, with evidence]
1. **"AI will make my product look fake or cheap."** The category sells touch (soft, cool, supportive), which video can't transmit; buyers worry AI makes it worse. → Show texture fidelity in the free frames (weave, quilting, foam recovery).
2. **A claim problem: lawsuits and NAD.** Reference-price suits are everywhere; "organic" and "Made in USA" have FTC history. → Lead with the §5.4 checklist.
3. **"Sale ads can't be creative."** Mattress marketers live on 5 tentpoles and banners. → Purple's meme sale ad (508K) and Gravity's 10 s gag are the counter-examples.
4. **Speed against the calendar.** Memorial Day and Labor Day are fixed. → "Your Labor Day film in 10 days."
5. **Weak optimisation (sleep aids on Meta).** → More hook variants per film.
6. **Brand tone.** Sleep brands guard "calm"; they fear loud, jokey AI. → Deadpan, slow, quiet-sounding comedy (Daymares) is the bridge.

### 6.3 What proof makes them pay $1,200–3,500
- **Five frames from their own product photo**, niche-correct: (1) a hand-press macro with real foam recovery or a fabric weave macro; (2) the product in a lamp-lit bedroom at night with clean blacks; (3) the concept's hook frame; (4) the physical-gag or test setup frame (with the proof-slot marked); (5) the end card with their real dated offer.
- **A measured comparison:** their current paid ad's loudness and cut data next to our plan ("your Labor Day video runs at −30 LUFS; ours will be −14 and still feel calm").
- **The proof-slot plan:** "You film 3 seconds of your real glass/egg/press test on a phone; we build the world around it."
- **The tentpole pack math:** one hero (15–30 s) + 3 hook heads + a 6 s loop + 6–10 stills per sale event; five events a year = the Season plan.
- **Legal pre-flight** in their words (reference prices, organic, Made in USA).

### 6.4 Re-buy triggers (what makes them book again)
1. **Five mattress tentpoles a year** (Presidents', Memorial, July 4, Labor, BFCM) plus Father's/Mother's Day. Each needs fresh creative; ad life in Bedding & Bath is ~27 d median [v].
2. **SKU velocity in bedding:** Boll & Branch 127, Parachute 121, Brooklinen 88, Sunday Citizen 22, Dagsmejan 19, Blissy 14 new products in 60 days [m]. Each colourway or collab = a drop film.
3. **New product categories:** Manta launching a white-noise machine (teaser posts 29 Sep–7 Oct [m]); Hostage Tape adding nasal strips (7 bundles in 60 days [m]); Pluto Pod travel pillow at MoMA Design Stores [c]. Each launch needs an explainer.
4. **Seasonal state changes:** heat (cooling), cold (heated, weighted), DST (light and sound).
5. **Retail and marketplace entries:** Purple into Costco and Mattress Firm; Amazon Prime Days (Manta); TikTok Shop LIVE (Coop).
6. **Creative fatigue on Meta:** Health & Wellness median 21 d, Home & Living 25 d [v].

### 6.5 Best outreach angle
**"Your next sale event, filmed without a shoot — and your real test stays the proof."**
- For mattress brands: a tentpole pack timed 5–7 weeks ahead.
- For bedding: a drop film per colourway, texture-first.
- For sleep aids: a sound- or light-first film that makes the product's sensation audible or visible, without health claims.
- Lead with one specific, measured observation about one of their ads (`vxo-leads` §3 rule).

**Sample first DM (NOT SENT — a template; a real one needs a dossier and the owner's approval):**
> Hi [Name] — your hand-press ad for the [mattress] is the cleanest product film in the category; that slow quilting press does all the selling. One idea for Labor Day: a sleepless city block, every window lit, and one window going dark as your box unrolls. I make AI product films (no shoot), and your real tests stay real. Want 5 free frames for the [mattress], or for the [pillow]?

(60 words: one compliment, one visual idea, one line on what we do, a yes/yes question, no links — `vxo-leads` §3.)

### 6.6 Twenty example brand types (no outreach)
1. Organic latex mattress (certification story)
2. Hybrid mattress for hot sleepers (cooling cover)
3. Mattress for athletes / recovery
4. Split-king adjustable base bundle
5. Mattress topper (dorms, guest rooms)
6. Custom-built pillow (quiz)
7. Side-sleeper / shredded-fill adjustable pillow
8. Percale or linen sheets (texture, colour drops)
9. Eucalyptus / TENCEL cooling sheets
10. Silk pillowcases (gifting)
11. Duvet / comforter (weights, seasons)
12. Performance sleepwear
13. Knit weighted blanket
14. Glass-bead weighted blanket
15. Blackout sleep mask (incl. audio masks)
16. White-noise / sound machine
17. Sunrise alarm / sleep lamp
18. Sleep earbuds
19. Nasal strips / mouth tape (ritual only)
20. Bed cooling/heating pad

---

## 7. Lead signals: a niche scoring add-on for `.claude/skills/vxo-leads/SKILL.md`

Apply on top of the base 100-point score (base table in the skill). The add-on can move a lead by **−25 to +30**; HOT stays ≥ 70 after the add-on. Check every item with public pages only.

| Signal | Points | How to check |
|---|---|---|
| **Tentpole window:** 5–7 weeks before Presidents' Day (early Jan), Memorial Day (early–mid Apr), July 4 (mid May), Labor Day (mid Jul), BFCM (mid Sep–Oct), Mother's Day (late Mar) for bedding, DST (late Jan / mid Sep) for light/sound | +8 | Today's date vs §1.5; the brand ran last year's event (archived posts, Motion pages) |
| **Static-heavy paid library:** of their newest ~20 Meta ads, ≤ 30 % video (Casper 25 %, Purple 30 % [v]) | +7 | Motion library page; Meta Ad Library when it loads |
| **SKU velocity:** ≥ 5 new products in 60 days (ignore content pages and colour-only duplicates) | +5 | `https://<store>/products.json?limit=250`, `created_at` |
| **New category launch teased** ("coming soon", waitlist, "something new is coming": Manta Sleep, 29 Sep–7 Oct 2026 [m]) | +6 | Brand TikTok embed page, IG posts, email sign-up pages |
| **Retail or marketplace entry** (Costco, Target, Mattress Firm, Amazon Prime event, TikTok Shop opening) in the last 90 days | +4 | Press, store locators, "now at…" posts |
| **Paid posts that are quiet, clipped or one-shot** (≤ −24 LUFS, peaks > 0 dBFS, or a single static take): a concrete DM hook | +3 | `ebur128` on one public post |
| **Physical product truth unused** (foam recovery, weight, cooling, blackout, motion isolation) while ads are banners or talking heads | +3 | Their top posts vs §3.1 |
| **Founder runs the ads himself / herself** (interviews, podcasts) | +2 | Podcast transcripts (e.g. Hostage Tape on 2X eCommerce) |
| **Reference-price or Made-in-USA suit pending** against the brand | −5 | ClassAction.org, TINA.org, FTC press |
| Core message is a **health outcome** (apnea, insomnia, jawline, anxiety, ADHD) | **−10** | Their captions and Meta library |
| **Children or infants** as the target or user of a sleep aid (kids' mouth tape, weighted infant wear) | **−20** | Product pages |
| Corporate or PE-owned with an agency of record (Somnigroup, Resident, Carpenter, Serta Simmons) | −5 | Ownership, trade press |
| Brand already has an in-house AI production team, or names AI tools in job posts | −5 | Job boards, press |

**VERY hot in this niche looks like** [inf]: a founder-led sleep-aid or bedding brand, $3–50M, with a teased launch or ≥ 5 new SKUs in 60 days, a sale event 5–7 weeks out, a Meta library ≤ 30 % video, and no health-outcome claims. Example: base 72 + tentpole 8 + static library 7 + launch tease 6 = 93.

---

## 8. Ten ready film concepts (invented brands, VXO spec)

Conventions:
- Invented brands and packs; clear names on USPTO before use; no real-brand look-alikes.
- Otto and Vee appear **only in C10** (VXO's own spec film). Any other concept can become a VXO spec by casting Otto as the deadpan lead (mouth never visible = no lip-sync risk).
- Every camera position is a real rig (tripod, slider, dolly, overhead arm, jib, Steadicam, handheld, hard mount). The camera never passes through glass, walls, mattresses or bodies (LESSONS 2026-10-08).
- **No AI frame shows a test result or a health outcome.** Each concept names its **proof slot** (the client's real footage). Claims on supers are placeholders the client replaces with its approved list.
- Every film ends with the 2-line VO tagline in a locked voice over a frame with no visible lips, plus the logo card (LESSONS 2026-10-09).
- **Costs** use doc 43 §6 list prices:
  - Seedance 2.5 r2v 15 s: $3.09 at 480p (proof) and $6.93 per 720p take (×3 = $20.79);
  - Kling 3.0 Pro i2v 5 s sound-off: $0.48 per take (×2);
  - Cinema Studio 4.0 720p 8 s: $3.70;
  - stills ≈ $0.30 each; ElevenLabs VO ≈ $0.10.
  Totals exclude the client's proof slot.

---

### C1 · STILLWATER (hybrid mattress, motion isolation) — "Night Shift" (20 s) ★ BEST 3 · ★ SINGLE BEST
- **Idea:** heist grammar for a 3:12 a.m. homecoming. A nurse in scrubs sneaks into her own bedroom like a jewel thief: shoes off, laser-precise steps. Her sleeping husband dozed off with a full glass of red wine **standing on the mattress beside his hand**. She can't reach her side without shaking the bed. She gives up, and **falls backwards onto the bed like a felled tree**. Cut to the client's real test: the wine doesn't move. He doesn't wake.
- **Hook (0–1 s):** ECU of a door handle turning a millimetre at a time, a single "click"; super "3:12 a.m."
- **Punchline (product-caused):** the full-body flop — and nothing happens. The joke exists only because the mattress isolates motion.
- **Built on:** Gravity's product-caused gag [m], Purple's egg-test heritage [c], Casper's "Daymares" deadpan [m], heist grammar (doc 44 §3).

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.2 | Macro on a slider, hallway side of the door | The handle turns millimetre by millimetre; click |
| 2 | 1.2–3.0 | Low tripod at floor height, bedroom doorway | Socked feet step in over a creaking board, toes test it first |
| 3 | 3.0–5.0 | Overhead arm, locked, above the bed | Plan view: husband asleep screen-left, a full wine glass on the duvet near his hand, her side empty; super "Obstacle." |
| 4 | 5.0–7.0 | Medium, Steadicam, at the foot of the bed | She freezes, assesses, tilts her head like a safecracker |
| 5 | 7.0–8.5 | CU, tripod | Her face: a slow exhale; she gives up |
| 6 | 8.5–10.0 | Wide, tripod at bed height, side view | She falls backwards, rigid, onto her side of the bed (stunt-style flop) |
| 7 | 10.0–13.0 | **Proof slot: the client's real test** | Same set-up filmed for real: a person drops onto the bed; the glass ~60 cm away barely ripples |
| 8 | 13.0–15.5 | CU, tripod | Husband asleep, chest rising every 4 s; one contented sigh |
| 9 | 15.5–20.0 | Packshot, Cinema Studio dolly-in on the bed corner, lamp-lit | Super "Fall in. Nobody wakes up." + dated offer; VO over the bed (no lips) |

- **Physics check:**
  - An adult of ~65 kg falling from standing height lands with its centre of mass dropping ~0.9 m (~4 m/s at contact); the mattress (30 cm hybrid, pocketed coils) compresses ~8–10 cm under her and rebounds once.
  - The glass (150 ml in a 450 ml bowl) is ~60 cm from her impact. Real tests on good isolation show a ripple of a few mm and no spill — **shown only in the client's footage** (shot 7).
  - In AI shots the glass is static, the same glass in every cut, with the same level.
  - The flop is a stunt-style fall written with "arms crossed on chest, body rigid, falls straight back, the duvet puffs once".
- **Audio map:** 0.0 fridge hum from the hallway, room tone; 0.6 handle click (close); 1.4 floorboard creak; 3.0 husband's slow breathing, 4 s cycle; 5.0 a heist-style pizzicato low string, 3 notes; 7.5 her exhale; 8.5 whoosh + **heavy duvet "whumpf"** at the contact frame (measured, doc 46); 9.0 total silence 1 s; 10.0 real test audio kept; 13.0 husband's sigh; 15.5 bed: soft bed-bell chime + bed music at 70 bpm; 16.5 VO: "Come home loud. Land quiet. STILLWATER."; 19.5 logo tick.
- **Models / template:** Seedance 2.5 r2v 10 s for shots 2–6 (doc 43 §7.5 comedic reveal adapted, "exactly five shots"; both character refs, plan view as the location ref); Kling 3.0 Pro i2v for 1 and 8; Cinema Studio 4.0 for 9 (§7.3).
- **Est. cost:** stills 9 × $0.30 = $2.70; Seedance 10 s 480p $2.06 + 720p ×3 $13.86; Kling 2 shots × 2 × $0.48 = $1.92; Cinema Studio $3.70; VO $0.10 → **≈ $24**.
- **Claim check:** motion-isolation claim only with the client's test; "Dramatization" super on shots 1–6; no rival product; wine is an adult prop (fine on Meta in a home setting; check the client's alcohol policy, and offer a water-glass cut).

### C2 · FIRSTFOLD (mattress-in-a-box) — "Fifth Floor Walk-Up" (15 s) ★ BEST 3
- **Idea:** two movers sweat a traditional queen mattress up a narrow NYC stairwell and jam it on the third-floor landing. A woman slides past them with the FIRSTFOLD box on a hand truck. Upstairs, the box unrolls in her tiny bedroom. Downstairs, the old mattress is still stuck.
- **Hook (0–1 s):** a low wide of a stairwell: a mattress wedged diagonally across the landing, one mover's face pressed against it, a muffled "pivot."
- **Punchline (product-caused):** her bed is made before the movers move an inch. It works only because the product ships compressed.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.5 | Low wide, tripod on the landing below | Mattress wedged diagonally; mover: muffled "pivot…" |
| 2 | 1.5–3.0 | Medium, handheld, from the stairs | She passes beneath the mattress with a boxed roll on a hand truck, polite nod |
| 3 | 3.0–4.5 | Overhead, top of the stairwell looking down | Spiral stairs, her climbing, movers frozen 2 floors below |
| 4 | 4.5–6.5 | CU on a slider, her bedroom floor | The cutter slits the film; vacuum hiss |
| 5 | 6.5–9.0 | Overhead arm, locked | The roll unfurls flat across the frame in ~2 s |
| 6 | 9.0–11.0 | Time-lapse insert (same overhead) | The foam rises to full height, then her sheets go on (time-lapse; super "Time-lapse") |
| 7 | 11.0–13.0 | Low wide, same tripod as shot 1 | Movers unchanged, a little sadder; one sits on the stair |
| 8 | 13.0–15.0 | Packshot, tripod, lamp-lit | Made bed, box on the floor; super + offer; VO |

- **Physics check:**
  - A queen innerspring is 152 × 203 cm and ~35–45 kg and does not fold; a 90–100 cm stairwell turn jams it diagonally (real).
  - A boxed queen ships around 105 × 45 × 45 cm, ~30–40 kg, so a hand truck is plausible.
  - The film is slit, then a hiss of ~1 s; the roll unfurls in ~2 s; the foam recovers most of its shape over minutes and full height over 24–72 h. **Hence the time-lapse cut, labelled, and the client supplies its real times.**
  - The box stays rigid; the label is from the ref.
- **Audio map:** 0.0 stairwell reverb, muffled "pivot"; 1.0 mattress scrape on plaster; 2.0 hand-truck wheel clacks on each step (measured); 4.5 cutter zip; 5.0 vacuum **hiss** 1 s; 6.5 foam unrolling "whomp"; 9.0 time-lapse whoosh; 11.0 a mover sighs; 12.0 bed music; 13.0 VO: "Some beds take the stairs. Ours takes the box. FIRSTFOLD."; 14.6 logo.
- **Models / template:** Seedance 2.5 r2v 15 s for 1–3, 7 (stairwell set ref, movers ref, mattress ref); Kling 3.0 Pro i2v first/last for 4–6; Cinema Studio for 8.
- **Est. cost:** stills 8 $2.40 + Seedance 480p $3.09 + 720p ×3 $20.79 + Kling 3 × 2 $2.88 + CS $3.70 + VO → **≈ $33**.
- **Claim check:** expansion and "ready to sleep" times from the client only; "Time-lapse" super.

### C3 · DEADWEIGHT (knit weighted blanket) — "The Fort" (10 s)
- **Idea:** VXO's version of Gravity's proven gag, as a staged tableau. A kid-free adult blanket fort built across two armchairs (a grown-up "work-from-fort"). Her partner tops it off with the weighted blanket for "extra cosy". The fort collapses slowly, with dignity. She doesn't move. She's asleep.
- **Hook (0–1 s):** a laptop glowing inside a perfect blanket fort; super "WFF (work from fort)".
- **Punchline (product-caused):** the collapse — and she sleeps through it, calm under 7 kg.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.5 | Wide, tripod | The fort, laptop glow inside |
| 2 | 1.5–3.0 | Medium, tripod | He lifts the knit blanket overhead with effort (it's 7 kg) |
| 3 | 3.0–4.5 | Wide, same as 1 | He lays it on the roof; the sheet roof sags in a slow arc |
| 4 | 4.5–6.5 | Wide, same as 1 | The fort folds flat, armchairs stay put |
| 5 | 6.5–8.0 | CU, tripod at floor level | Her calm face under the knit, eyes closed, slow breath |
| 6 | 8.0–10.0 | Packshot overhead, the knit on the flattened fort | Super + VO |

- **Physics check:** a 7 kg knit drapes immediately with no billow; a bedsheet roof spanning ~1.5 m between chair backs can't carry it, sagging over ~0.8 s and then sliding off the chair backs. The laptop is closed first (written: she closes it at 1.2 s). Breathing 15/min. The knit loops stay the same size (ref).
- **Audio map:** 0.0 keyboard taps; 1.2 laptop closes; 1.6 his strained "hup"; 3.0 fabric stretch creak; 4.5 a soft slump and a pillow puff; 6.5 her single slow exhale; 7.5 room tone + one bed chime; 8.2 VO: "Heavy on purpose. DEADWEIGHT."; 9.6 logo.
- **Models:** Seedance 2.5 r2v 10 s for 1–4 (one continuous wide is also possible as one take); Kling for 5–6.
- **Est. cost:** stills 6 $1.80 + Seedance 10 s 480p $2.06 + 720p ×3 $13.86 + Kling 2 × 2 $1.92 + VO → **≈ $20**.
- **Claim check:** no anxiety/insomnia claims; adults only; "choose ~10 % of body weight" only as the client's guidance.

### C4 · HUSHLINE (white-noise machine) — "Jackhammer" (15 s)
- **Idea:** sound-first. 6:02 a.m., a jackhammer outside a ground-floor bedroom window. She turns one dial. **The film's soundtrack becomes rain.** We keep seeing the jackhammer through the window, now silent to us, the worker's whole body shaking. She sleeps.
- **Hook (0–1 s):** black frame; a jackhammer starts at full volume (sound-first hook, LESSONS 2026-10-09).
- **Punchline (product-caused):** the visual chaos with the product's sound — the audience hears what she hears.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.0 | Black, then the window from the bed (tripod) | Jackhammer audio; picture fades in on the worker outside |
| 2 | 1.0–3.0 | CU, tripod | Her eyes open, flat stare at the ceiling |
| 3 | 3.0–4.5 | Insert, slider on the nightstand | Her hand turns the HUSHLINE dial |
| 4 | 4.5–9.0 | Wide, tripod (same as 1) | Window: the worker jackhammering; soundtrack = rain only; she rolls over |
| 5 | 9.0–11.5 | Exterior medium, tripod across the street | Worker pauses, looks at the window, puzzled (no audio from him) |
| 6 | 11.5–15.0 | Packshot, Cinema Studio, the device glowing on the nightstand | Super "Pick your sound." + VO |

- **Physics check:** a jackhammer is ~100–110 dB at 1 m; through a closed double-glazed window ~10 m away it might be ~55–65 dB `[inf]`. A white-noise machine **masks**, it does not block — so the "silence" is presented as her subjective soundscape, and **the super says "masks noise"**, never "blocks". The device LED is steady; the dial turns 90°.
- **Audio map:** 0.0 jackhammer at full; 2.0 it continues under her stare; 3.6 dial click (measured); 4.0 jackhammer **cuts to rain** on the click frame; 4.5–11.5 rain only; 9.0 one bird chirp; 11.5 bed music under rain; 12.2 VO: "Can't change the street. Change what you hear. HUSHLINE."; 14.6 logo.
- **Models:** Seedance 2.5 r2v 10 s for 1, 2, 4, 5 (worker and sleeper refs; window plate); Kling for 3; Cinema Studio for 6.
- **Est. cost:** stills 6 $1.80 + Seedance 480p $2.06 + 720p ×3 $13.86 + Kling $0.96 + CS $3.70 + VO → **≈ $23**.

### C5 · NOCTURNE (blackout sleep mask) — "High Noon" (12 s)
- **Idea:** a western standoff at noon in a desert town — sun glaring, tumbleweed. The "outlaw" isn't a gunslinger: it's a night-shift nurse who needs to sleep at noon. She draws… the mask. The frame goes completely black for 1.5 s. Then a quiet "zzz" super.
- **Hook (0–1 s):** an ECU of a sun-squinting eye under a hat brim; a spur jingle.
- **Punchline (product-caused):** the screen literally goes black — the product turns noon into night.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.0 | ECU, tripod | Squinting eye, hat brim, harsh sun |
| 2 | 1.0–2.5 | Wide, tripod at street level | Empty western street, sun overhead, tumbleweed |
| 3 | 2.5–4.0 | Medium, dolly in | She stands in scrubs and a duster coat, hand hovering at her hip |
| 4 | 4.0–5.0 | Insert, slider | Her hand draws the mask from the holster |
| 5 | 5.0–6.0 | CU | She slips it on; eye cups seat |
| 6 | 6.0–7.5 | **Full black frame** | Super "12:00 p.m." fades to "zzz" |
| 7 | 7.5–12.0 | Packshot on a hospital locker shelf | Super + VO |

- **Physics check:** noon sun outdoors is ~50,000–100,000 lux; a blackout claim (e.g. "100 % blackout") must come from the client's test, and the black frame is a stylised POV, labelled "Dramatization". No weapon: the holster holds only the mask (doc 45 weapons rule).
- **Audio map:** 0.0 wind + spur jingle; 1.0 harmonica sting; 2.5 boots on dust; 4.0 leather holster slide; 4.6 mask elastic snap; 5.2 all sound **drops to a single heartbeat-slow room tone** on the black frame; 7.5 bed music; 8.2 VO: "Your night starts when your shift ends. NOCTURNE."; 11.6 logo.
- **Models:** Seedance 2.5 r2v 10 s for 1–3; Kling for 4–5; still for 6–7.
- **Est. cost:** ≈ $2.10 stills + $2.06 + $13.86 + $1.92 + VO → **≈ $20**.

### C6 · TWOFOLD (two-weight split duvet, snaps together) — "Tug of War" (15 s)
- **Idea:** a duvet tug-of-war shot like a sports final, with a commentator VO. He's hot; she's cold. Both pull; the duvet stretches. At peak tension, the snaps release, and each tumbles onto their own half: his light, hers warm. Both asleep in 2 seconds.
- **Hook (0–1 s):** an ECU of two fists gripping opposite corners of one duvet, knuckles white; a referee whistle.
- **Punchline (product-caused):** the snaps give way exactly as designed — the "split" ends the war.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.0 | ECU, slider | Fists on corners; whistle |
| 2 | 1.0–3.0 | Overhead arm, locked | Plan view: a couple pulling a duvet in opposite directions |
| 3 | 3.0–5.0 | Medium, tripod, his side | He pulls, sweating |
| 4 | 5.0–7.0 | Medium, tripod, her side | She pulls, shivering, socks on |
| 5 | 7.0–8.0 | Insert, macro on slider | The snap line strains; snaps pop open one by one |
| 6 | 8.0–10.0 | Overhead, same as 2 | Two halves; each falls back onto their own side |
| 7 | 10.0–12.5 | Overhead, same | Both asleep, each wrapped in their own half |
| 8 | 12.5–15.0 | Packshot: halves snapped together on a made bed | Super + VO |

- **Physics check:** a duvet snap releases at ~10–20 N per snap `[inf]`; 8 snaps pop in sequence over ~0.4 s, not all at once. A down-alternative duvet weighs ~1 kg (light) vs ~2 kg (warm); halves fall onto the bed in ~0.4 s. Two people, distinct pyjama colours, arms above the duvet; he is always screen-left.
- **Audio map:** 0.0 whistle; 1.0 crowd murmur (stylised) + commentator VO (mouth off-screen): "And it's a tense one tonight…"; 3.0 his grunt; 5.0 her teeth chatter; 7.0 eight snap pops (each on its measured frame); 8.0 two soft mattress landings; 8.5 crowd "ohhh"; 10.0 silence, two slow breaths; 12.5 VO: "Hot or cold. Not both. TWOFOLD."; 14.6 logo.
- **Models:** Seedance 2.5 r2v 15 s for 2–4, 6–7; Kling for 1, 5; Cinema Studio for 8.
- **Est. cost:** ≈ $2.40 + $3.09 + $20.79 + $1.92 + $3.70 + $0.10 → **≈ $32**.

### C7 · SLOWRISE (sunrise alarm lamp) — "The Rooster's Last Day" (20 s)
- **Idea:** a farm rooster's farewell party (deadpan office-retirement tone: a cake, a card, a hen dabbing her eye). The new hire is a lamp. Final shot: dawn light ramps slowly on a sleeping woman; she wakes calmly; through the window, the rooster sits at a desk with a résumé.
- **Hook (0–1 s):** an ECU of a sheet cake iced "THANKS FOR THE MEMORIES", a candle lit.
- **Punchline (product-caused):** the rooster is "replaced" because the lamp wakes her gently.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.2 | ECU, tripod | Cake, candle |
| 2 | 1.2–3.5 | Medium, tripod in the barn | The rooster on a hay bale, a party hat, deadpan (real-photo ref, ≤ 5 s) |
| 3 | 3.5–5.5 | Insert | A card on hay: "Good luck, Gerald" (post super) |
| 4 | 5.5–8.0 | Wide, tripod, dark bedroom | The lamp starts glowing deep red, the woman asleep |
| 5 | 8.0–12.0 | Same frame, time-lapse | Light ramps red → amber → warm white over "30 minutes" (super) |
| 6 | 12.0–14.5 | CU | Her eyes open slowly, she stretches |
| 7 | 14.5–17.0 | Window POV from the bed (tripod) | Outside, the rooster at a garden table, reading the classifieds |
| 8 | 17.0–20.0 | Packshot | Super + VO |

- **Physics check:** a sunrise lamp ramps over ~20–30 min (client spec) to a few hundred lux at the pillow; shown as a labelled time-lapse. One animal per shot ≤ 5 s from a real photo (LESSONS). No claim about circadian health beyond the client's approved line.
- **Audio map:** 0.0 party blower; 1.5 a single hen cluck; 3.5 paper card flap; 5.5 night room tone; 8.0 soft rising pad tone matching the light ramp; 12.0 her exhale; 14.5 a newspaper page turn outside; 16.0 one indignant crow (muted, through glass); 17.0 VO: "Wake up like it's sunrise. Because it is. SLOWRISE."; 19.6 logo.
- **Models:** Kling i2v for the rooster shots (2, 7) and inserts; Cinema Studio for the lamp ramp one-take (4–6, 8 s); still for 8.
- **Est. cost:** stills 8 $2.40 + Kling 5 shots × 2 × $0.48 = $4.80 + CS 8 s $3.70 + VO → **≈ $11**.

### C8 · LOAMWELL (organic latex mattress) — "The Inspector" (20 s)
- **Idea:** a deadpan "certification inspector" (clipboard, magnifying loupe, lab coat) audits a bedroom like a crime scene: sniffs the air, checks the tag with a loupe, peers at the latex through a cutaway sample. He signs, then quietly lies down and falls asleep on the job.
- **Hook (0–1 s):** an ECU through a jeweller's loupe of a woven cotton cover, a magnified eye at the edge.
- **Punchline (product-caused):** the inspector, whose job is to be sceptical, falls asleep on it.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.2 | Macro through a loupe | Weave texture, eye at the edge |
| 2 | 1.2–3.5 | Medium, tripod | Inspector in a lab coat, clipboard, by the bed |
| 3 | 3.5–6.0 | Insert | **Proof slot: the client's real certificate/tag**, framed and still |
| 4 | 6.0–8.5 | CU, slider | He presses a latex cutaway sample; it springs back < 0.3 s |
| 5 | 8.5–10.5 | Medium | He ticks a box; hesitates; sits on the edge |
| 6 | 10.5–14.0 | Wide, tripod | He lies back "to test it", clipboard on his chest |
| 7 | 14.0–16.5 | Overhead | Asleep, clipboard rising with each breath |
| 8 | 16.5–20.0 | Packshot | Super "Certified [GOTS/GOLS as provided]." + VO |

- **Physics check:** natural latex rebounds in < 0.3 s; the cutaway shows real layer thickness from the client's spec (e.g. 15 cm latex over coils). Certification marks appear **only** in the real proof slot (no AI-drawn seals, per FTC v. Moonlight Slumber).
- **Audio map:** 0.0 a tiny creak of the loupe; 1.2 pen click; 3.5 room tone; 6.0 latex "thup" rebound (measured); 8.5 tick; 10.5 bed creak; 12.0 one slow exhale; 14.0 clipboard rises on breath (no sound); 16.5 bed music; 17.0 VO: "We passed. So did he. LOAMWELL."; 19.6 logo.
- **Models:** Seedance 2.5 r2v 10 s for 2, 5–7; Kling for 1, 4; Cinema Studio for 8.
- **Est. cost:** ≈ $2.40 + $2.06 + $13.86 + $1.92 + $3.70 + $0.10 → **≈ $24**.
- **Claim check:** only the certifications the client holds, with real marks; no "non-toxic" without basis.

### C9 · FIRECLAY (dual-zone heated mattress pad) — "Cold Feet" (12 s)
- **Idea:** sound-first. A woman's shriek in the dark: his ice-cold feet just touched her calves. Next night, his side of the bed is preheated. The twist: she's the one who migrates onto his warm side; he ends up on the edge.
- **Hook (0–1 s):** black frame, a sharp "AAH!" and a light switch flicking on.
- **Punchline (product-caused):** the warm zone reverses who invades whose side.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.0 | Black → lamp on (tripod, bedside) | Shriek, light clicks on |
| 2 | 1.0–2.5 | Insert under the duvet edge, slider at mattress level | His bare feet near her calves (no skin beyond ankles) |
| 3 | 2.5–4.0 | Two-shot, tripod | Her glare, his guilty shrug |
| 4 | 4.0–6.0 | Insert, the remote | "Next night": dial to his side "7" (client's real UI only) |
| 5 | 6.0–9.0 | Overhead arm, locked, time-lapse | Through the night, she drifts across to his side |
| 6 | 9.0–10.5 | Overhead, same | Morning: he's on the edge, she's sprawled on his warm side |
| 7 | 10.5–12.0 | Packshot | Super + VO |

- **Physics check:** cold-foot skin temperature can be ~25 °C vs a pad's warm setting of ~30–40 °C (client spec); the overnight drift is a labelled time-lapse; pillows stay 4 throughout; she's always screen-left at the start.
- **Audio map:** 0.0 shriek + switch click; 1.0 duvet rustle; 2.5 his tiny "sorry"; 4.0 remote beeps ×2; 6.0 time-lapse whoosh + clock ticks; 9.0 morning birds; 9.6 his sigh; 10.5 VO: "Warm feet. Fair borders. FIRECLAY."; 11.6 logo.
- **Models:** Seedance 2.5 r2v 10 s for 1–3, 5–6; Kling for 4; still for 7.
- **Est. cost:** ≈ $2.10 + $2.06 + $13.86 + $0.96 + $0.10 → **≈ $19**.
- **Claim check:** temperature range and safety (auto-off) from the client; no circulation/health claims.

### C10 · VXO spec · SOMNE (luxury hybrid mattress) — "Take 47" (25 s) ★ BEST 3 (Otto & Vee)
- **Idea:** Otto directs a mattress commercial. The talent is supposed to lie down and say one line, but **falls asleep every take**. Vee's single stopwatch clicks each new take. By take 47, the boom operator, the gaffer and the script supervisor are asleep on the mattress too. Otto, deadpan, lies down "to show them how it's done". Vee clicks the stopwatch one last time. Silence.
- **Hook (0–1 s):** a clapperboard slammed in close-up: "TAKE 47"; Vee's stopwatch click.
- **Punchline (product-caused):** the whole crew asleep on the product, then the director too — the mattress defeats the shoot.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.2 | ECU on a slider | Clapper "TAKE 47" snaps shut; stopwatch click |
| 2 | 1.2–3.5 | Wide, tripod on the studio floor | A bed set under film lights; actor lies down; boom pole above |
| 3 | 3.5–5.5 | CU, tripod | Actor's eyes close before the line |
| 4 | 5.5–7.5 | Medium, tripod behind the monitor | Otto's back and moustache in profile; he lowers his megaphone slowly (mouth never visible) |
| 5 | 7.5–10.0 | Montage of 3 inserts (slider) | Take 48 clapper; the boom op now lying on the bed; take 49: the gaffer too |
| 6 | 10.0–13.0 | Wide, same as 2 | Four crew asleep in a row on the bed, the boom resting on the duvet |
| 7 | 13.0–16.0 | Medium, tripod | Vee checks her one stopwatch, looks at Otto |
| 8 | 16.0–19.5 | Wide, same as 2 | Otto walks in, lies down stiffly at the end of the row, hands folded; his moustache rises and falls |
| 9 | 19.5–21.0 | CU | Vee's thumb clicks the stopwatch: stop |
| 10 | 21.0–25.0 | Packshot under film lights, Cinema Studio dolly-in | Super "SOMNE. Hard to stay awake on." + VO |

- **Physics check:** studio lights are real (2K fresnels on stands), the boom pole rests on the duvet (2–3 kg) with a visible dimple; five adults on a king (193 × 203 cm) are a squeeze but real (shoulder width ~45 cm × 5 ≈ 2.25 m, so the last one half hangs off — write it); breathing 15/min for each; Vee holds **exactly one** stopwatch in every frame; Otto's mouth is never visible, eyes never wide.
- **Audio map:** 0.0 clapper crack + stopwatch click; 1.2 studio room tone, light ballast hum; 3.5 the actor's soft snore begins; 5.5 Otto's megaphone lowered (fabric rustle, no voice); 7.5 clapper ×2 (measured), each followed by a thud of a body onto the bed; 10.0 a chorus of four slow breaths, off-sync; 13.0 Vee's tiny sigh; 16.0 Otto's footsteps, bed creak at the contact frame; 19.7 final stopwatch click; 20.0 silence 1 s; 21.0 bed music; 21.6 VO (Otto's locked voice, as VO over a frame with no lips): "Forty-seven takes. Zero complaints."; 23.2 Vee's VO: "SOMNE."; 24.6 logo.
- **Models / template:** Seedance 2.5 r2v 15 s for 2–8 (Otto and Vee character sheets, studio set ref; "exactly seven shots"; ≤ 3 characters in focus per shot, others soft); Kling for 1, 9; Cinema Studio for 10.
- **Est. cost:** stills 10 $3.00 + Seedance 480p $3.09 + 720p ×3 $20.79 + Kling 2 × 2 $1.92 + CS $3.70 + VO $0.20 → **≈ $33**.

### 8.1 Ranking

| Rank | Concept | Why |
|---|---|---|
| ★ 1 | **C1 Night Shift (motion isolation)** | Proven test (wine glass/egg heritage) + heist comedy + the client's real test as the punchline: the fullest LESSONS fit (hook, turn, product-caused punchline, proof slot). Works for every mattress brand on every tentpole |
| ★ 2 | **C2 Fifth Floor Walk-Up** | The category's oldest truth (bed-in-a-box) made visual; real stairwell physics; a cheap time-lapse; no claims beyond expansion times |
| ★ 3 | **C10 Take 47 (Otto & Vee)** | VXO's own spec in the exact register of Casper's 2026 "Daymares"; shows the studio's deadpan style and continuity discipline (one stopwatch, no lips) |
| 4 | C4 Jackhammer | Sound-first; showcases VXO's audio QC; needs careful "masks" wording |
| 5 | C3 The Fort | Proven gag, cheapest action concept |
| 6 | C6 Tug of War | Sells a real split-sleep trend; snap physics is fun |
| 7 | C7 Rooster | Cheapest (~$11) but animal shots are fragile |
| 8 | C9 Cold Feet | Strong hook; niche product |
| 9 | C5 High Noon | Big visual, but the black frame needs a substantiated blackout claim |
| 10 | C8 The Inspector | Good for certification brands; the joke is gentler |

---

## 9. Ten surprising insights nobody asked for (that would make VXO better)

1. **The audience buys sleep products while they should be sleeping.** 72 % have bought online after bedtime [v]. Build a "night-native" film style: dark palette, warm practicals, quiet-*feeling* mix at full loudness, no flash frames. Recommend 22:00–02:00 dayparting for sleep-aid clients. Benly's Home & Living signature is "Calm" (3.6×), and slow cinematic pacing lives longest [v].
2. **"Calm" is not "quiet", and that is a sales line.** 11 of 36 measured sleep posts were below −24 LUFS (one at −34.3) and 4 clipped [m]. A film mastered to −14 LUFS / −1 dBTP that still feels hushed is a demonstrable craft edge. Put the before/after loudness numbers in the pitch.
3. **The ending device for the whole niche is "Shhh".** Casper's "Daymares" closes on a "Shhhhhh" super over a sleeper with hidden lips [m]. That turns VXO's house rule (VO over a lip-free frame) into a category convention. Make "shh" endings a template in `vxo-film`.
4. **Mattress customers don't re-buy; mattress marketers do.** Customers wait ~5 years between mattresses, but brands run 5–7 sale events a year on 27-day creative [v]. Sell the mattress client a **tentpole retainer**, not a "brand film". Sell bedding clients **per-drop films** (88–127 new products in 60 days [m]).
5. **The proof is the punchline in this niche.** Wine glass, egg drop, bowling ball, box expansion: the category's best demos are physical. That flips the AI rule into a feature: VXO stages the world and the setup; the client's 3-second real test lands the joke. **"Made with AI. The test is real."** is honest and persuasive.
6. **Sleep is a "state" niche: reach comes from naming the state, sales come from the object.** The top four organic posts show no product being used in second 1, while paid winners show the object in frame 0 [m]. Build every client delivery as a pair: a state-named hook head (organic, shareable) + an object-first product film (paid).
7. **AI search is now part of the mattress funnel.** 37 % of buyers used AI tools [v]. Films with spoken specs and captions, uploaded with full transcripts and product names, feed the pages and videos that AI assistants summarise `[inf]`. Offer a transcript + caption file with every film.
8. **Photo carousels are a TikTok format we under-sell.** Purple's carousels hit 82–118K; Hostage Tape narrates stories over stills [m]. VXO's 6–10 stills per film can be shipped as a ready-to-post carousel with a VO track, at almost no extra cost.
9. **Fads die fast in sleep; build for the next one.** Mouth-tape interest fell from 100 to 22 in 20 months; Hostage Tape is already adding nasal strips [m]. In outreach, pitch the pivot product (the new SKU), not the fad.
10. **A dead social handle is a lead signal, and a warning for VXO.** The `@sleepme` TikTok handle posts unrelated content, and several brands' TikToks run at a median under 300 views [m]. Brands whose own channels are neglected need ready-made paid assets most. And VXO must lock its own handles on every platform before its spec films travel.

---

## 10. Gaps and next steps (zero spend)

- **Meta run-lengths are unconfirmed.** The public Ad Library returns 403; Atria has no sleep pages; Motion's pages are 4 months old. Next: a Motion workspace (`get_inspo_creatives` for Purple, Casper, Saatva, Cozy Earth, Brooklinen, Hatch, Blissy; `LAST_90_DAYS`, ACTIVE) to find the longest-running sleep videos.
- **YouTube downloads are blocked.** Casper "Daymares" :30 spots and Purple's egg test are metadata-only. Retry later with backoff or another mirror.
- **TikTok Shop sleep-category GMV** (Bedsure, Cozy Earth, mouth tape) was not found publicly. FastMoss/EchoTik category pages are the next source.
- **Revenue for most of the 30 brands is [unverified].** Fill it per dossier only when a brand becomes a lead.
- **No NAD decisions from 2025–2026 on sleep products surfaced.** The BBB National Programs decisions page should be searched by brand before any comparative-claim film.
- **The "AI-Generated" Benly attribute** has no ad count; treat it as directional.

---

## Sources

**Market and industry:**
- ISPA / BedTimes 2025 trends: https://bedtimesmagazine.com/2026/05/the-mattress-industry-trends-report-sharpens-the-industry-picture-for-2025/ · https://sleepproducts.org/2026/07/mattress-industry-trends-report-2026-overview/ · https://beddingnewsnow.com/?p=14447 · https://bedtimesmagazine.com/2025/07/latest-forecast-predicts-decline-in-2025-increase-in-2026/
- Purple FY2025: https://www.barchart.com/story/news/1061046/purple-innovation-reports-fourth-quarter-and-full-year-2025-results · https://finance.yahoo.com/markets/stocks/articles/purple-innovation-q4-earnings-call-141036729.html · https://eightx.co/blog/us-teardown-purple
- J.D. Power 2025 mattress study: https://www.jdpower.com/business/press-releases/2025-us-mattress-satisfaction-study/
- Amerisleep 2026 buyer survey: https://amerisleep.com/blog/state-of-mattress-buying/
- Sheets market: https://www.fortunebusinessinsights.com/u-s-bedsheets-market-108607 · bedding revenue table: https://www.reportprime.com/home-bedding-r17781/company · Cozy Earth: https://www.parse.gl/brands/cozyearth-com
- Sleep economy roundups: https://www.ringly.io/discover/sleep-and-bedding-statistics-2026 · https://www.aol.com/finance/sleep-become-big-business-yielding-174300942.html
- Eight Sleep: https://techcrunch.com/2026/03/04/eight-sleep-raises-50m-at-1-5b-valuation
- Hostage Tape: https://2xecommerce.transistor.fm/episodes/40m-revenue-in-year-3-how-meta-ads-strategic-branding-and-influencers-drive-hostage-tapes-success-alex-neist · Manta: https://www.shopify.com/blog/manta-sleep-international-expansion · Bearaby: https://omr.com/de/daily/bearaby-kathrin-hamm · Loftie: https://kingscrowd.com/loftie-on-startengine-2022/
- Sleep divorce: https://aasm.org/americans-opting-sleep-divorce-accommodate-bed-partner/ · https://www.healthday.com/health-news/sleep-disorder/are-you-your-partner-in-a-sleep-divorce-youre-not-alone
- Sleepmaxxing: https://www.healthline.com/health-news/sleepmaxxing-tiktok-trend · https://www.storyboard18.com/amp/how-it-works/gen-z-explainer-the-rise-of-sleepmaxxing-a-sleep-revolution-or-overhyped-trend-43938.htm
- Casper history: https://www.retaildive.com/news/dtc-brands-struggled-with-profitability-prior-to-covid-19-now-what/580689/ · https://www.wuwf.org/2020-01-17/the-cost-of-free-casper-pays-a-price-for-generous-mattress-returns · https://beddingnewsnow.com/?p=3914
- Affiliates: https://www.authorityhacker.com/mattress-affiliate-programs/

**Creative benchmarks:**
- Benly Q1 2026 Home & Living: https://benly.ai/benchmarks/q1-2026/home-living · Bedding & Bath: https://benly.ai/benchmarks/q1-2026/home-living/bedding-bath · Health & Wellness: https://benly.ai/benchmarks/q1-2026/health-wellness · Q2 2026 Home & Living: https://benly.ai/benchmarks/q2-2026/home-living
- Motion libraries: https://motionapp.com/library/casper · /purple · /saatva · /brooklinen · /cozy-earth · /hatch · /blissy
- Meta H&W restrictions: https://www.click.co.uk/insights/metas-new-advertising-restrictions-impacts-health-and-wellness-brands/ · https://www.polaranalytics.com/post/2025-metas-tracking-restrictions-for-health-wellness-are-here----heres-how-to-fix-it
- TikTok Shop bedding: https://www.dashboardly.io/tiktok-shop/bedding-pillows

**Campaigns and AI ads:**
- Casper Daymares: https://act.adforum.com/agency/6700077/creative-work/34733216/birthday-boy/casper · https://beddingnewsnow.com/?p=14051 · Casper Sleepers: https://www.lovethework.com/work-awards/campaigns/casper-sleepers-1529682
- Purple egg test: https://www.furnituretoday.com/mattress-bedding-news/purples-clever-egg-test-racks-online-views-wins-fans · https://spectacle.is/video/how-to-use-a-raw-egg-to-determine-if-your-mattress-is-awful-purple-mattress
- Spring Air AI: https://beddingnewsnow.com/blog/2026/07/14/spring-air-will-debut-new-ai-generated-campaign-at-las-vegas-market/ · Symphony Sleep: https://bedtimesmagazine.com/2026/04/symphony-sleep-leverages-ai-for-new-marketing-campaign/ · Kingsdown: https://www.furnituretoday.com/mattress-bedding-news/kingsdown-uses-ai-to-revive-ads-and-train-retail-teams · Boll & Branch: https://modernretail.co/operations/where-boll-branch-draws-the-line-on-ai-generated-advertising

**Policy and legal:**
- Reference-price suits: https://www.classaction.org/news/8.16m-brooklyn-bedding-settlement-wraps-up-class-action-lawsuit-over-allegedly-inflated-reference-prices · https://news.bloomberglaw.com/litigation/dtc-mattress-company-saatva-accused-of-advertising-fake-sales · https://openclassactions.substack.com/p/eight-sleep-hit-with-class-action · https://truthinadvertising.org/class-action/nest-beddings-discounts/?pg=7 · https://beddingnewsnow.com/blog/2024/09/15/lessons-froms-mattress-firms-latest-class-action-lawsuit/
- NAD: https://bbbprograms.org/media/newsroom/decisions/nad-refers-nectar-sleep-to-ftc · https://www.manatt.com/insights/newsletters/advertising-law/dont-sleep-on-price-comparison-claims-nad-cautions · https://bbbprograms.org/media/newsroom/decisions/simmons-memory-foam
- FTC organic: https://search.ftc.gov/news-events/news/press-releases/2017/12/ftc-approves-final-consent-order-moonlight-slumber-llc-advertising-case · https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/moonlight-slumber-says-goodnight-to-misleading-and-unsubstantiated-organic-advertising-claims-after-settlement-with-ftc
- FTC Made in USA: https://sleepproducts.org/?p=10888 · https://www.afslaw.com/perspectives/the-fine-print/750k-wake-call-ftc-fines-mattress-manufacturer-over-false-made-usa · https://www.claimsjournal.com/news/national/2024/04/30/323301.htm
- Mouth taping: https://pmc.ncbi.nlm.nih.gov/articles/PMC12094774 · https://www.healthday.com/health-news/sleep-disorder/mouth-taping-for-better-sleep-little-benefit-lots-of-risk-review-says · https://fawcettmattress.com/blogs/news/mouth-taping
- Weighted infant products: https://www.cpsc.gov/About-CPSC/Commissioner/Richard-Trumka/Statement/Beware-Weighted-Infant-Swaddles-and-Blankets-Are-Unsafe-for-Sleep-Retailers-Should-Consider-Stopping-Sales · https://www.cbsnews.com/amp/miami/news/safety-concerns-arise-over-weighted-baby-sleeping-products-after-cpsc-warning
- FDA general wellness 2026: https://faegredrinker.com/en/insights/publications/2026/1/key-updates-in-fdas-2026-general-wellness-and-clinical-decision-support-software-guidance · https://www.kslaw.com/insights/articles/fda-updates-general-wellness-and-clinical-decision-support-guidance-documents · anti-snoring 510(k): https://www.accessdata.fda.gov/cdrh_docs/pdf25/K250028.pdf
- Meta nudity policy: https://transparency.meta.com/policies/ad-standards/objectionable-content/adult-nudity-and-sexual-activity · TikTok healthcare policy: https://ads.tiktok.com/help/article/tiktok-ads-policy-healthcare-pharmaceuticals?lang=en

**Measured posts [m]** (TikTok URLs in §2.1). Analysis files (not committed): `scratchpad/niche2/sleep/an/` (stats, tiles, ASR), `emb/meta_all.txt` (435 posts' metadata), `shop/shop.txt` (Shopify data), `motion/` (Motion pages).
