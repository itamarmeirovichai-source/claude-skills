# 53 — Niche deep-dive: men's grooming, shaving, men's fragrance and oral care

Research brief, 2026-10-09. No generation money was spent. Nobody was contacted. Nothing was sent.

**What this adds.** No earlier doc covers this niche (doc 47 lists "men's grooming skincare" as one line; doc 11 has no men's section). This doc builds on 41 (action realism), 42 (teardown method), 43 (models, prices, templates), 44 (comedy craft), 45 (what sells, policy, AI disclosure), 46 (sound and QC) and the niche docs 47–49. It does not repeat them. It adds:
- a market map: size, growth, 30 DTC brands with price bands and launch velocity, a seasonality calendar and where the money goes;
- teardowns of **22 ads I downloaded and measured** (from 429 TikToks whose metadata I pulled across 39 brand accounts), plus 8 metadata-only campaigns;
- conversion data for the niche (Benly Q1 2026 sub-industry figures, NIQ, Charm.io, Circana);
- AI realism pitfalls specific to stubble, blades, foam, toothbrushes, teeth, sprays and glass, with prompt fixes and model routing per doc 43;
- policy and legal (OTC drug lines for toothpaste, antiperspirant and hair loss; whitening NAD/NARB cases; fragrance dupes; sexual-innuendo rules for body grooming);
- the buyer, re-buy triggers, an outreach angle and a sample DM (never sent);
- a niche scoring add-on for `vxo-leads`;
- 10 ready film concepts (3 marked best) and 10 non-obvious insights.

**Tags.**
- `[m]` measured by me from the file: ffmpeg scene cuts at threshold 0.30, 2 fps frame tiles that I looked at, a 0.5 s RMS envelope, librosa onset rate and beat-regularity score (autocorrelation peak of the onset envelope; > 0.5 = steady music bed, < 0.15 = voice or no steady beat), EBU R128 integrated loudness and sample peak, and a faster-whisper (base.en) transcript.
- `[c]` the brand's or platform's own claim. `[v]` vendor or agency figure (directional). `[inf]` my inference. `[unverified]` no primary evidence found.

**Method and limits.**
- **TikTok:** profile listing through yt-dlp fails (JSON error), so I pulled each account's public creator-embed page (`tiktok.com/embed/@handle`), which lists ~10–14 recent and pinned posts, then fetched metadata for all 429 posts and downloaded 23 (one failed) to `scratchpad/niche2/grooming/` for analysis only. **No media is committed or republished.**
- **Account medians** below are over those 9–14 recent posts per account, a small window. **Paid signature:** ≥ ~700K views at a like rate under ~1 % (doc 49 method). Brands keep paying only for winners, so this is the best public proxy for "sold" `[inf]`.
- **YouTube:** search works, downloads are blocked ("confirm you're not a bot", every client tried). Super Bowl and AI spots are metadata-only.
- **Meta Ad Library:** the public page returns HTTP 403 to our fetcher, and Motion's MCP has no workspace. I used third-party mirrors (Atria, Motion's public library) for formats, start dates and variant counts. **No run-length winners could be confirmed on Meta** — that is the biggest gap in this doc (see §10).
- **Shopify:** `products.json` is public on most stores; I used it for price bands and launch velocity (§1.3, §7).

---

## 0. The 10 findings that matter most

1. **This is a paid-distribution niche, above all in oral care.** Organic medians on brand TikTok accounts are tiny — Quip 252 views, Snow 135, Hismile 342, Burst 172 — while their paid posts sit at 0.7–20M [m]. The biggest post in the measured set is a Spotlight Oral Care water-flosser stitch at **20.4M views and a 0.77 % like rate** [m]. Men's grooming accounts do better organically (Dr. Squatch median 28.2K, Beardbrand 25.4K, Manscaped 17.3K) [m]. **Sell VXO films as paid-ready variant packs, not as "viral" content.**
2. **The winners in this niche explain a mechanism.** The two biggest razor posts are long explainers: Henson's machinist founder on blade exposure (123 s, **33M views**, 2023) and Supply's "How many blades do you actually need?" (59 s, 381K, **3.31 % likes**, 2026) with a CG cross-section of a hair being cut under the skin [m]. Oral care's biggest is a dentist explaining water-flosser debris (37.7 s, 20.4M) [m]. **CG cross-sections, blade geometry and "what happens under the skin" are exactly what AI does cheaply and well** — a sellable "mechanism insert" (§9, insight 4).
3. **Men's grooming creatives live long; fragrance creatives die fast.** Benly Q1 2026: Men's Grooming averages **47 days** of ad life (62 % video), against 18 days median / 23 days average for Fragrance [v]. That sets the offer: **grooming = one Premiere per launch plus quarterly refresh; fragrance = the Season plan** (§5.4).
4. **In fragrance, a product-only film is the weakest asset.** Benly fragrance effectiveness index: UGC/Organic **83**, Lifestyle 67, Branded/Studio 54, Graphic 47, **Product Shot 43** [v]. The AI cliché (bottle in petals, slow orbit) is the bottom of the table. What works instead: **"scent as a place"** — Fulton & Roark's 10 s montage "Need a perfume that smells like this?", 14 cuts at 0.35–0.4 s, **5.21 % likes** [m] — or a person (Every Man Jack's skier testimonial, Dossier's layering lecture).
5. **The category's comedy engine is a personified body part.** Manscaped "The Boys" (2024, tiny hairy men), Manscaped "Hair Ballad" (Super Bowl 2026, singing hair puppets by Can Can Club, MJZ, Quality Meats), DSC "Danglers" (AI, 2026), Lume's animated cartoon sweat drops [m]. Big brands pay puppet-shop budgets for this. **AI makes creature comedy affordable for a $3M brand** — VXO's sharpest wedge in this niche `[inf]`.
6. **The in-house AI competitor is already here.** Dollar Shave Club made "250 Years. No BS. Still Free" in-house with **Higgsfield and Claude for $400**, concept to launch in ~3 weeks, and calls it "the most successful campaign in its history" [c] ([Marketing Dive](https://marketingdive.com/news/how-dollar-shave-club-uses-generative-ai-to-unlock-advertising-creativity/825016); [Modern Retail](https://www.modernretail.co/marketing/how-dollar-shave-club-decides-when-to-use-ai-generated-creative/)). Its CBIO admits "some were executed better than others". **VXO cannot sell access to the tools; it must sell taste, physics, QC, claims safety and speed for brands without an in-house AI team** (§5).
7. **"Real" has become a claim.** Oars + Alps captions every person "Real", "A real dude", "This cat? real too" ("We closed down a city street for real") [m]. Quip's practical-effects spot (actor in a mouth headpiece, miniatures) was accused of being AI and the brand posted BTS with "No AI, just us" ([Modern Retail](https://www.modernretail.co/marketing/quips-latest-ad-wasnt-ai-generated-people-were-convinced-it-was/)). Gartner: 68 % of US consumers often wonder whether content is real; half prefer brands that avoid gen-AI in consumer-facing content [v]. **Rule: AI for the obviously impossible (creatures, miniatures, cross-sections, absurd scale); real footage for any result on skin, beard or teeth.**
8. **Hands-only is the dominant paid format in oral care and fragrance.** 4 of the 9 paid-signature posts are hands-only product films with one text line (Snif 11.1M; Quip ×3 at 0.7–1.3M) [m]. Hands are the cheapest AI-safe human element (doc 45 D43: hands-only ads lived ≥ 98 d in 6 of 8 cases).
9. **Claims are the landmine, and they differ by sub-niche.** Toothpaste with fluoride and antiperspirants are **OTC drugs**; hair regrowth is a **drug** claim; whitening is cosmetic but heavily litigated (NARB told Boka to drop "whitens teeth" for lack of product-specific tests, 2025; NAD told GuruNanda and Lumineux to drop "enamel safe", 2025; the UK ASA banned Hismile's "instant" V34 ads, 2024). **An AI shot of teeth getting whiter or a beard getting thicker is a mock-up demonstration and is never allowed** (§4).
10. **Calendar beats everything else as a lead signal.** Father's Day (men's prestige fragrance > $230M in the Father's Day window per Circana [c]), No-Shave November → **Dec 1 "shave-off"**, BFCM and holiday gift sets, Valentine's, summer body care. A brand 5–7 weeks before one of these with a new SKU and weak video is the hottest lead in this niche (§7).

---

## 1. Market map

### 1.1 Size and growth (US)

| Segment | Number | Source | Status |
|---|---|---|---|
| Men's grooming (NIQ scope) | **$7.1B**, +6.9 % YoY; **online +27.6 %**, now nearly half of dollars | [NIQ, Nov 2025](https://nielseniq.com/global/en/insights/report/2025/mens-grooming-market-surges-key-trends-you-need-to-know/) | Primary (measured scanner + e-com) |
| …inside it | Bar soap **+33 %**, deodorant **+11.4 %**, **whole-body deodorant +150 %**, shaving **+14.5 %**, body wash $1B | same | Primary |
| …shoppers | 59 % worry about aging; 40 % say premium is worth it; **households with teens spend +26 %** | same | Primary |
| Men's grooming (broad scope incl. skincare, fragrance, tools) | $18.3B (2024) → $28.5B (2033) | [IMARC](https://imarcgroup.com/male-grooming-products-market-united-states) | [v] |
| Wet shave, North America (Edgewell) | **−7.2 % organic**, FY2025 | [eightx teardown](https://eightx.co/blog/edgewell-teardown) | [v] (third-party read of filings) |
| Men's fragrance | ~1/3 of US fragrance, **+15 %** YTD (Circana via trade press; year unclear); prestige fragrance +6 % / mass +17 % in 9M 2025 | [Beauty Independent](https://orbit.beautyindependent.com/article/what-next-fragrance-2026) | [c] Circana, partly [unverified] |
| Men's fragrance on TikTok Shop | Monthly men's fragrance sales above women's for ~2 years; peak **$18M in one month**; men-targeted fragrance creators **×12** (Apr 2024→Apr 2025) | Charm.io via [SCMP/Bloomberg](https://scmp.com/magazines/style/beauty/trends/article/3355775/tiktoks-fragrance-boom-why-gen-z-men-are-spending-us400-creed-cologne) | [v] |
| US fragrance retail | $8.91B, +3.5 % (2025 forecast) | [eMarketer](https://www.emarketer.com/content/tiktok-social-change-gen-z-give-mens-fragrances-their-moment) | [v] |
| US oral care | $8.9B (MarketsandMarkets) to $11.6B (Mordor), 5.7–7.5 % CAGR | [M&M](https://www.marketsandmarkets.com/Market-Reports/geography/oral-care-market/US), [Mordor](https://www.mordorintelligence.com/industry-reports/united-states-oral-care-market) | [v] (scope differs) |
| Oral care on TikTok Shop | Hismile in the top-10 beauty storefronts Q2 2026; Hismile mouthwash #4 US best-seller wk 22/2026 (29.6K units, $610K in a week); DR.DENT strips **$3.1M in Jan 2026**, 91 % via shoppable video, 3,800 affiliates, 15 % commission; GuruNanda **$23M** in 12 months | [Beauty Independent](https://www.beautyindependent.com/tiktok-shop-nears-1b-beauty-sales-second-straight-quarter/), [Nexscope](https://www.nexscope.ai/cases/40), [FastMoss](https://www.fastmoss.com/blog/how-dr-dent-dominated-the-tiktok-shop-market-in-january-2026/), [Beauty Independent](https://www.beautyindependent.com/indie-beauty-brands-surpassed-500-million-on-tiktok-shop-in-the-past-year/) | [v] |
| Men's grooming on TikTok Shop | **Based Bodyworks $50.6M** in the 12 months to June 2026 (#2 indie beauty brand); Viking Revolution $1.5M in 2025 from ~9,000 affiliates | [Beauty Independent](https://www.beautyindependent.com/indie-beauty-brands-surpassed-500-million-on-tiktok-shop-in-the-past-year/), [Beauty Independent](https://www.beautyindependent.com/?p=182167) | [v] |

**Read [inf]:** the money is moving to (1) **body** (whole-body deodorant, bar soap, body trimmers) rather than face shaving; (2) **fragrance for young men**, bought on TikTok Shop and as gifts; (3) **oral care as beauty** (whitening, flavoured toothpaste, nano-hydroxyapatite, water flossers), sold through creators on TikTok Shop. Face wet-shave is flat to down overall, but premium single-blade and safety razors (Henson, Supply, Leaf) grow by taking share with "one blade" arguments.

### 1.2 Scale anchors (above VXO's band; benchmarks, not targets)
- **Dr. Squatch:** > $400M 2024 sales, bought by Unilever in 2025 (terms undisclosed; reports up to $2B) ([Marketing Dive](https://www.marketingdive.com/news/unilever-acquires-dr-squatch-valuing-brands-viral-marketing-to-gen-z-men/751304/)). Sydney Sweeney "Bathwater Bliss" soap: 5,000 bars at $8 sold out in minutes, June 2025 ([Campaign](https://campaignlive.com/article/final-numbers-sydney-sweeneys-bathwater-campaign-dr-squatch/1937718)).
- **Manscaped:** "> 15M customers, 39 countries, $300M revenue" (founder op-ed, Feb 2026 [c]); "$100M in media" (CEO interview, date unclear [c]); first Super Bowl spot 2026 ([SDBJ](https://sdbj.com/retail/manscaped-grooms-growth-with-super-bowl-ad/)).
- **Hismile:** > $300M sales in 2023 [v]; > 5M TikTok followers; Stain iD mouthwash "debris" video drove $1.8M TikTok Shop sales in 30 days [v] ([Baijing/BrandArk](https://www.baijing.cn/article/55299)).
- **Dossier:** ~$100M annualised 2025 [v]; TikTok Shop $4.4M in 2024; Walmart ~4,000 doors, Target national (Sept 2025) ([Sacra](https://sacra.com/c/dossier/)).
- **Harry's, Dollar Shave Club (PE-owned since 2023), Native/Bevel (P&G), Oars + Alps (S.C. Johnson), Cremo (Edgewell), Boka and Viking Revolution (Essor):** corporate-owned; useful as creative benchmarks only. (Edgewell's 2019 deal to buy Harry's for $1.37B was abandoned after the FTC sued to block it in 2020.)

### 1.3 Thirty DTC brands to know (founder-led, roughly $1–60M where findable)

Columns: TikTok median = median views of the ~10–14 recent posts I pulled [m]; SKUs / median price / new in 60 days = from the store's public `products.json` on 2026-10-09 [m]. Revenue figures are estimates and mostly `[unverified]`. These are **examples for the market map, not outreach targets**; any lead goes through the `vxo-leads` dossier first.

| # | Brand | Sub-niche | Size signal | Founder-led? | Price band (median SKU) | New SKUs 60 d | TikTok median | Where they advertise (observed) |
|---|---|---|---|---|---|---|---|---|
| 1 | Henson Shaving | Safety razor (aerospace machining) | > $25M (2023) [c] | Yes (Jantzi family) | $89 median; razor ~$90, blades $0.10 | 2 | 4.3K (pinned explainer 33M) | TikTok long explainers, YouTube, Meta |
| 2 | Supply | Single-edge razor | [unverified] | Yes | $28; razor up to $129 | 3 | 39.8K | TikTok/Meta comparative explainers (4:5) |
| 3 | Leaf Shave | Pivoting safety razor, dermaplaner | [unverified] | Yes | $23 | 1 | 18K | TikTok unboxings, reply-to-comment |
| 4 | Beardbrand | Beard care | ~$10M GMV (ECDB est.) [v] | Yes (Eric Bandholz) | $36 | 1 | 25.4K | TikTok creator-style, YouTube |
| 5 | Live Bearded | Beard care | [unverified] | Yes | $30 | 1 | — | Meta, YouTube |
| 6 | Scotch Porter | Beard/hair, Black men | [unverified] | Yes | $19 | **6** (Oct 8) | 556 | Just joined TikTok Shop (June 2026) |
| 7 | Bossman | Beard/hair | [unverified] | Yes | — | — | 115 | Meta, Amazon |
| 8 | Viking Revolution | Value grooming, Amazon-first | "on track for $59M" [c] | Founder-run, Essor-owned | $15 | 3 | — | Amazon, TikTok Shop affiliates, Walmart Connect |
| 9 | Based Bodyworks | Hair/body, "looksmaxxing" | $50.6M TikTok Shop (12 mo) [v] | Yes (Lance Baker) | $28 | 2 | — | TikTok Shop founder + affiliate + live |
| 10 | Fulton & Roark | Solid & spray men's fragrance | [unverified] | Yes | $35 | 1 | 18K | TikTok scent montages, Meta |
| 11 | Snif | Fragrance (unisex, Ulta) | [unverified] | Yes | $24 | **15** | 1.9K (paid 11.1M) | TikTok Spark hands-only, Ulta |
| 12 | Oakcha | Fragrance dupes/originals | [unverified] | Yes | $35 | **47** | — | Meta "inspired by", TikTok |
| 13 | Alt Fragrances | Fragrance dupes | [unverified] | Yes | $39 | 4 | — | Meta, TikTok |
| 14 | Boy Smells | Candles + fragrance (gender-neutral) | [unverified] | Yes | $44 | 2 | — | Meta, retail |
| 15 | Jaxon Lane | Men's skincare (K-beauty) | [unverified] | Yes | $46 | 6 | — | Meta, Amazon |
| 16 | Geologie | Men's skincare subscription | [unverified] | Yes | $49 | 0 | 238 | Meta quiz funnels |
| 17 | Brickell | Natural men's skincare | [unverified] | Yes | $35 | 1 | 156 | Meta, Amazon |
| 18 | Lume | Whole-body deodorant | [unverified] | Yes (OB-GYN founder) [unverified] | — | — | 8.2K | TikTok animated reviews, TV |
| 19 | Duke Cannon | "Big" men's soap & care | [unverified] | Yes (veteran-led) [unverified] | — | — | 1.4K | TikTok stunts, retail |
| 20 | Every Man Jack | Body care, deodorant, scent | [unverified] | [unverified] | — | — | 1.6K (paid 820K) | Athlete docs, Meta |
| 21 | Meridian | Body trimmer | [unverified] | Yes | $20 | 0 | — | Meta, podcasts |
| 22 | Cocofloss | Floss, toothpaste | > 5M spools sold [c] | Yes (Dr. Chrystle Cu, dentist) | $22 | **5** | — | Meta, TikTok |
| 23 | Bite | Toothpaste tablets | ~$4M (2021) [v] | Yes (Lindsay McCormick) | $29 | 0 | 473 | Founder story, Meta |
| 24 | Risewell | Nano-hydroxyapatite toothpaste | [unverified] | Yes | $12 | 0 | 226 | Meta, creators |
| 25 | Lumineux (Oral Essentials) | Whitening, nHA | [unverified] | Dentist-founded [unverified] | $36 | 2 | 1.0K | TikTok dentist content |
| 26 | Davids | Natural toothpaste, metal tube | [unverified] | Yes | $11 | 1 | — | Meta, Amazon |
| 27 | Smile Actives | Whitening | [unverified] | Yes | $30 | **10** | 65 | Meta, gift sets |
| 28 | Snow | LED whitening | "$100M" milestone [unverified] | Yes (Josh Elizetxe) | $39 | 0 | 135 (paid 690K) | TikTok UGC reply videos |
| 29 | Spotlight Oral Care | Whitening, water flosser (dentist sisters, IE/US) | [unverified] | Yes | — | — | 739 (paid 20.4M) | TikTok dentist stitches |
| 30 | GuruNanda | Oil pulling, whitening, flossers | $23M TikTok Shop (12 mo) [v] | Yes | $10 | 6 | — | TikTok Shop affiliates |

**Too big but worth watching:** Manscaped, Dr. Squatch, Hismile, Dossier, Quip, Harry's, DSC, Hims/Keeps (telehealth hair loss), Native.

### 1.4 Price bands (from `products.json`, 2026-10-09 [m])

| Sub-niche | Entry | Hero | Premium | Notes |
|---|---|---|---|---|
| Razors (single-blade/safety) | $10 blade packs | $28–90 handle | $129–300 (Henson, Supply sets) | Hardware AOV supports long explainers |
| Trimmers (body/beard) | $20 accessories | ~$70–110 trimmer [unverified for Manscaped, store 403] | Kits $130+ | Gift-set driven (Q4, Father's Day) |
| Beard & hair care | $10 | $19–36 oils/balms | $135–180 kits | Bundles, variety packs |
| Bar soap / body | $8–10 bar | $16 median (Dr. Squatch) | Bundles "49 % off + 3 gifts" | Collab drops every few weeks |
| Men's fragrance (DTC/dupe) | $24–29 | $35–44 | $99–195 | "Inspired by" vs originals; gift sets in Sept–Oct |
| Toothpaste / floss | $10–12 | $18–22 | $29 tablets subscription | Subscription = re-buy |
| Whitening | $30 | $39–49 kits | $99–225 LED kits/sets | BOGO and "buy 3 get 5" on Meta |
| Electric brush / flosser | $25 | $50–80 | $110–140 | Quip ultra lite ~$110 top SKU |

### 1.5 Seasonality calendar (US)

| Month | Moment | Who it matters for | Pitch lead time |
|---|---|---|---|
| Jan | New Year routines; "dry January" body reset | Skincare, whitening, oral care subscriptions | Pitch in Nov |
| Feb | **Super Bowl** (Manscaped, Dr. Squatch, DSC), **Valentine's** | Fragrance, grooming gift sets, whitening ("kiss-ready") | Pitch early Jan |
| Mar–Apr | Spring; wedding & prom season starts | Whitening, fragrance, beard shaping | Pitch Feb |
| **May–Jun** | **Father's Day** (men's prestige fragrance > $230M in the window [c] [Happi/Circana](https://www.happi.com/breaking-news/fragrance-sales-expected-to-exceed-230-million-for-fathers-day-2025/)); graduation | Fragrance, trimmers, razors, kits | **Pitch late Mar–Apr** |
| Jul–Aug | Summer heat, beach, gym; TikTok Shop "Deals for You Days" (July) | Deodorant, whole-body, body trimmers, SPF for men, bar soap | Pitch May |
| Aug–Sep | Back to school / college; new scent drops; gift-set builds | Gen Z fragrance, starter kits | Pitch Jul |
| Oct | Amazon Prime Big Deal Days (men's fragrance in the top 10 [c]) ; Halloween/collab drops (Dr. Squatch × One Piece, Stranger Things) | Fragrance, soap collabs | Pitch Aug |
| **Nov** | **Movember / No-Shave November** (beard-care peak, shaving trough); **BFCM** | Beard brands peak; razor brands go quiet then hit **Dec 1** | **Pitch late Sep–Oct** |
| Dec | **Dec 1 "shave-off"**; holiday gifting (gift sets, stocking stuffers) | Razors, trimmers, fragrance | Pitch Oct |

### 1.6 Where they advertise (observed)
- **Meta:** everyone. Libraries skew to **image + offer** (Manscaped: feature-benefit pointout images and "Bundle & Save"; Hismile: offer-first banners "Buy 2 get 1 free", "We really f*cked up this time…" pricing-mistake hooks; Dossier: Us-vs-Them price-gap images) ([Motion: Manscaped](https://motionapp.com/library/manscaped), [Hismile](https://motionapp.com/library/hismile), [Dossier](https://motionapp.com/library/dossier)). **Hismile's live Meta videos are mostly 50–78 s** ([Atria](https://tryatria.com/ads/meta/hismile-ads)). Dr. Squatch launches waves of ~9–19 ads on one day with 10 s, 19–46 s and 70 s cuts ([Atria](https://tryatria.com/ads/meta/dr-squatch-ads)).
- **TikTok Spark / TikTok Shop:** oral care and fragrance live here (affiliates, shoppable video = 91 % of DR.DENT sales [v]).
- **CTV, YouTube and podcasts:** Manscaped (Tatari as media agency on the Super Bowl), DSC (YouTube, Spotify, podcasts), Henson (YouTube) [c].
- **Amazon and retail media:** Viking Revolution, Boka (Walmart Connect, sponsored search, DSP) [c].

---

## 2. Teardowns: 22 measured ads plus 8 metadata-only

Selection: from 429 posts on 39 accounts, I kept posts with (a) the paid signature, (b) a high multiple of the account median, or (c) a format that VXO could make, and I added two older classics (Henson, Leaf) because they remain pinned and still define the razor category. Cut rate = (cuts + 1) ÷ duration. "Hook" = what is on screen and in the audio in second 1.

### 2.1 Measured (TikTok)

| # | Ad · date · stats [m] | Length · cuts · cut rate | Second 1 | Shot list (timecodes) | Turn / punchline | Product interaction | Sound [m] | Text / CTA | Why it sold [inf] |
|---|---|---|---|---|---|---|---|---|---|
| G1 | **Manscaped "Send face pics instead" — life montage** ([link](https://www.tiktok.com/@manscaped/video/7537843044532423950)) · 2025-08-13 · **7.5M**, 1.98 % likes, **29.8K shares** | 62.8 s · 25 · 0.41/s | A man in a bathroom pulling his red shorts out, looking down (the implied dick-pic) | 0–2.3 shorts; 2.3–7.9 wide doorway "Tom, what are you doing in there?"; 7.9 phone on rug; 9.4–13 he picks it up; 13–18 phone screen: a face selfie; 18–25 "So I take a pic of my face… She responds back: Cute face"; 27–37 date, fireworks, trimmer in hand (~33 s); 37.4 proposal in a field; 39 wedding; 43 birth; 44.7 camcorder dad; 47.8 mowing the lawn; 49.7 birthday cake; 55.0 engraved urn; 57–59 old man on a porch; 59.5 grandson; end card "SEND FACE PICS INSTEAD" | A whole lifetime follows from choosing the face pic | Trimmer as one beat (~33 s); the product enables the "clean" choice | Quiet open (−38 dB first second), then a score; **−14.0 LUFS, peak +3.0 dBFS (clipping)** | End card only | **Taboo flipped to wholesome**; a feature-film life montage; high share rate (0.4 %) = social currency. The product is barely shown, so it works as brand, not DR |
| G2 | **Manscaped "customer service rep"** ([link](https://www.tiktok.com/@manscaped/video/7558255342803635469)) · 2025-10-06 · **1.2M, 0.11 %** (paid) | 60 s · 4 · 0.08/s | A deadpan **moustached** rep at a desk under a giant "MANSCAPED" wall, super "MANSCAPED HQ" | 0–23 locked medium; "THOUSANDS" super at ~5 s; 23.3 close-up, headset, "*This actually happens" super; 30.7 wide office, he holds up a printed "pic" with a black bar; 56 end card | "Maybe the next pic will be of their clean, smiling face" → launches Chairman Pro face shaver | Shaver named, not demoed | VO-led, **−23.3 LUFS** (quiet) | "SEND FACE PICS INSTEAD" | **Deadpan spokes-character with a moustache** (an Otto-like register); confession + taboo + "true" disclaimer |
| G3 | **Snif "what's in your cart" (Ulta)** ([link](https://www.tiktok.com/@snif/video/7491483346879515934)) · 2025-04-10 · **11.1M, 0.08 %** (heavy paid) | 17.5 s · 5 · 0.34/s | A hand lifts the "hot cakes" bottle off a phone showing its own product page | 0–2.5 lift; 2.5–3.4 bottle to camera; 3.4–7 Ulta app splash, scrolling; 7–14 more scrolling, adding to cart; 14.4 bottle again; 15.7 three minis on concrete | None; it's a retail-availability ad | Hands-only throughout | Music, −14.5 LUFS; one line "Oh god, look at it. It's perfect." | Super "what's in your cart" for 17 s | **Retail news + hands-only + native "haul" frame.** Shows the paid lane for fragrance: availability, not mood |
| G4 | **Quip "what makes the Ultra Lite different?"** ([link](https://www.tiktok.com/@quip/video/7662019514158140685)) · 2026-07-13 · **1.3M, 0.02 %** (paid) | 19.9 s · 4 · 0.25/s | Toothbrush on a white cloud pedestal, olive wall, question super | 0–2.7 brush on stand, three angles; 2.7–6 red-nailed fingers on the brush head "easy-to-clean"; 6–9 button: "3 intensities: gentle, daily + deep"; 9–16 head swap; 16–18 "a clean mouth with 15x more plaque removal"; 18.5–20 back to the stand | None | Hands-only feature walk | Steady music bed (beat regularity 0.62), no VO, −24 LUFS | One super per feature | **Hands + one super per feature + a number** ("15x") |
| G5 | **Quip "morning rush"** ([link](https://www.tiktok.com/@quip/video/7675028008608042270)) · 2026-08-17 · 1.1M, 0.09 % (paid) | 10.7 s · 7 · 0.75/s | A bathroom-sink flat-lay with a lit candle | 7 slow push-ins on sink objects (candle, floss, mints "Rapid", "Ritual", brush), one every ~1.3 s | None | Products as set dressing | Music, −14.7 LUFS | "this and nobody rushing me" | **Mood + routine** frame; the cheapest possible paid asset |
| G6 | **Quip "oral care but make it whimsical"** ([link](https://www.tiktok.com/@quip/video/7675414661092691213)) · 2026-08-18 · 706K (paid) | 8.3 s · 2 · 0.36/s | Two rhinestoned tubes and a brush on a shelf | 0–2.7 trio; 2.7–4.4 brush in hand; 4.4–8.3 tube close-ups | None | Hands | Music bed (0.60) | One super | **Decorated product = novelty**; 8 s |
| G7 | **Dr. Squatch × IShowSpeed "SPEEDRUN"** ([link](https://www.tiktok.com/@drsquatch/video/7680226955588930830)) · 2026-08-31 · **3.4M**, 1.13 % | 26.0 s · 11 · 0.46/s | Black frame → Speed sitting on a pile of cash in a vault | 0–5.4 vault "Welcome to the Speedrun Million Dollar Mission"; 5.4 soap bar to the lens "presented by the natural soap legends at Dr. Squatch"; 7.6 calendar flip "You got 9 weeks"; 9.2 CRT wall "25 missions"; 10.8 cash in hand "cold hard cash"; 13.4 fisheye "What other soap company…"; 16.2 shirt rip "grab some Squatch"; 18.9 crouch "complete a mission"; 21.4 airhorn; 22–26 football sprint | Contest mechanics as the story | Bar to lens at 5.4 s | Captions every word; −14.7 LUFS | Captions + contest | **Creator collab + contest** = participation. Not reproducible without the creator, but the vault/CRT set is AI-native |
| G8 | **Every Man Jack "Mountain Air" × Tanner Hall** ([link](https://www.tiktok.com/@everymanjack/video/7608312028473740557)) · 2026-02-18 · **820K, 0.33 %** (paid) | 17.9 s · 13 · 0.78/s | ECU of a weathered, bearded face: "There's a scent called Mountain Air" | 0–1.8 ECU; 1.8–3.7 wide walking on snow; 3.7–9 backlit pines "the sap is really potent"; 9–11 silhouette, sun flare; 11–13 seated interview; 13–15 skis on a ridge; 15–16.8 product line-up on a snowcat; 16.8 ECU "made me feel like home" | Scent = memory of a place | Product shown once at 15 s | Interview VO, no music, −19.6 LUFS | Word captions | **Athlete testimonial that translates scent into a place.** No product use shown |
| G9 | **Dossier "the art of fragrance layering"** ([link](https://www.tiktok.com/@dossierperfumes/video/7598622208776326431)) · 2026-01-23 · **1.6M, 0.33 %** | 41.4 s · 23 · 0.58/s | A symmetrical library, a woman in a white shirt at a desk: "Welcome to the art of fragrance layering" | 3.6 bottle row; 4.6–8 spray on neck; 8.6 desk; **11 stopwatch close-up "let it dry"**; 13.8 a pulse-point body diagram traced in red pencil; 15.3 wrists; 18 sample tray "True layering"; 21–27 pairings; 27–37 bottle pairs "Woody Sage + Aromatic Star Anise"; 37–41 desk | "Creates a third scent" | Spray, dab, pairs | VO, −16.8 LUFS | Section supers ("Fragrance Layering", "Mix & Match") | **Lecture format, Wes-Anderson symmetry, education that sells two bottles at once** |
| G10 | **Snow LED whitening, reply-to-comment** ([link](https://www.tiktok.com/@snow/video/7397928561211952426)) · 2024-07-31 · 690K, **13.3K comments** | 44.6 s · 4 · 0.11/s | Creator face + comment sticker "Before and after or it's fake!" | 0–4 unboxing the mouthpiece; 4–18 mouthpiece in, 10 min; 18–30 smile check; 30–44 "two weeks ago" photo inset | "Tell me you don't see a difference" | Product in mouth | Phone audio, **−36.4 LUFS** (very quiet) | Reply sticker | **Comment-bait proof.** Real teeth, real creator; exactly what AI must never fake |
| G11 | **Oars + Alps "We closed down a city street for real"** ([link](https://www.tiktok.com/@oarsandalps/video/7540659706797378829)) · 2025-08-20 · 114K, 0.03 % (paid) | 15.4 s · 14 · 0.98/s | A man in a yellow jumpsuit holds the SPF can to the lens | 1.0 "ROAD CLOSED" barricade; 1.7–3.8 crowd, "This guy?"; 3.8–5.5 "A real dude", dodgeball; 5.5–7.8 suit guy "This dude? Real"; 7.8–10 "Even this man? Yeah, he's real"; 10–11.7 "This cat? real too"; 11.7–13 can sprayed on an arm; 13.7 sign "MAN NEEDS MORE SUN"; 14.5 product trio | **Realness itself is the joke** | Can to lens at 0.0, spray at 12 s | VO + music, −14.7 LUFS | Supers on every person | **Anti-AI positioning in a summer SPF ad.** Fast (1 s ASL) |
| G12 | **Lume "we turned a real review into a song"** ([link](https://www.tiktok.com/@lumedeodorant/video/7636425622474083614)) · 2026-05-05 · 69.7K, **2,364 shares (3.4 % share rate)** | 27.7 s · ~12 real (animation inflates detection) | Cartoon woman jogging, sung line "I get boob sweat" | 0–5 jogging; 5.5–10 sweat drops become characters chasing her; 10–12 she sinks into a cloud "tried using deodorant"; 12–14 hand with the product "gave Lume a try"; 15–23 she applies, sparkles, beach; 24–27.7 end card "ODOR FREE YOURSELF · 72Hr" | The review sung as a jingle | Animated applications | Sung, beat 0.39, −22.4 LUFS | Lyrics as captions; end card | **A real review re-performed in a stylised medium** = testimonial without a fake person. AI-native |
| G13 | **Hismile Tru-Fit brush (creator, #ad)** ([link](https://www.tiktok.com/@hismile/video/7693696430594182408)) · 2026-10-06 · 88.6K (259× median) | 31.5 s · 15 · 0.51/s | Two hands hold a three-headed brush: "There's one for the front and back" | 0–4.6 product + packaging; 4.6–9 talking head; 9–13 brushing in a second creator's mouth; 13–23 three heads "even a three-year-old…"; 23–28 more brushing; 28–31.5 pack | "You might feel like an idiot for not inventing it" | Demo in mouth | VO-led, −12.5 LUFS | "FRONT & BACK?!" | **Clever-mechanism demo by a creator** |
| G14 | **Henson "AL13" machinist explainer** (classic) ([link](https://www.tiktok.com/@hensonshaving/video/7206158826792406277)) · 2023-03-03 · **33M**, 1.33 %, 25.6K shares | 123 s · 7 | Macro of the razor head with the blade edge | 0–9.5 product macro; 9.5–45 founder at the CNC shop; 45–47 cutaway diagrams; 47–82 parts, Mars rover, ISS; 82–89 blade-exposure diagram; 89–123 price "$10" for blades, end card | "The design nobody else wanted to make because it's tricky" | Hands, parts | Voice, −14.9 LUFS | Captions | **Engineering credibility + a counter-intuitive price.** Long works when every line is a new fact |
| G15 | **Leaf Shave dermaplaner unboxing** (classic) ([link](https://www.tiktok.com/@leafshave/video/7263065292241177902)) · 2023-08-03 · 8.2M | 56.4 s · 24 · 0.44/s | "This is going to help you stop using cheap plastic razors" | Unbox → blade in guard → clip → stand → refills → "$9" → "sold out four times" | Scarcity | Hands | VO, −16.5 LUFS | — | **Zero-waste + refills price + scarcity**; bought by women (dermaplaning) from a men's razor brand |
| G16 | **Beardbrand "From this to Wolverine's beard"** ([link](https://www.tiktok.com/@beardbrand/video/7693694791174999326)) · 2026-10-06 · 165.8K (7× median) | 20.3 s · 10 · 0.54/s | Founder-type face + a celebrity photo inset, super "FROM THIS TO WOLVERINE'S BEARD" | 1–6 trimmer close-ups along the jaw; 6–17 sideburn and neck lines; 17–20 "Rate this look 1–10", "Now I am Wolverine for a few days" | Comedic self-awareness | Trimmer in use | Quiet (−25.6 LUFS), no music | Big supers | **Transformation + celebrity reference** (right-of-publicity risk, §4) |
| G17 | **Duke Cannon "Soap Hammerschlagen"** ([link](https://www.tiktok.com/@dukecannon/video/7691813477740023053)) · 2026-10-01 · 36.5K (26× median) | 8.5 s · 12 · **1.5/s** | A huge soap puck on a log, hammer raised; super "Soap Hammerschlagen" | 0.8 box; 2.3–5 hands drive nails into the soap; 5–7 nails standing in it; 7–8.5 guys crouching, tailgate | The soap is a game | Nails into product | Room tone, −26.2 LUFS | One super | **Durability proof disguised as a tailgate game**; fastest cut rate in the set |
| G18 | **Harry's × Scrub Daddy kit** ([link](https://www.tiktok.com/@harrys/video/7691334322359520543)) · 2026-09-30 · 19.8K (21×) | 6.0 s · 0 | Kit on a tiled shelf, bubbles drifting, box reads "Put a smile on your face." | One locked shot, bubbles | — | None | Music, −17.2 LUFS | Pack copy | **Collab news in a 6 s loop**; bubbles are the only motion (AI-trivial) |
| G19 | **Fulton & Roark "Hwy 190"** ([link](https://www.tiktok.com/@fultonandroark/video/7485803046010621214)) · 2025-03-25 · 280K, **5.21 %** | 10.0 s · 14 · **1.5/s** | A pickup kicking dust on a desert road; serif super "Need a perfume that smells like this?" | 0.4 map; 0.8 cracked rock; 1.2 sun; 1.6 silhouette; 2.0 desert; 2.4 4×4 tyre; 2.7 smoke wisp; 3.0 hands on wheel; 3.4 empty road; 3.8–5.1 road → the bottle fades in, standing on the asphalt; 5.1–10 bottle + "HWY 190" + three note icons "Freesia · Desert Wind · Myrrh" | The place becomes the bottle | None (composite) | Music, beat 0.66, **peak +2.9 dBFS (clipping)** | Notes as icons | **Scent translated into a place, 14 images in 5 s.** Every shot is stock-like and AI-trivial |
| G20 | **Cremo antiperspirant launch** ([link](https://www.tiktok.com/@cremocompany/video/7475803404485315883)) · 2025-02-26 · 19.5K (16×) | 7.4 s · 8 · 1.2/s | Sticks fanned on white, super "Cremo Antiperspirant & Deodorants are finally here!!!" | 1.0 one stick; 2.2 "Available in 3 scents"; 4.0 rotate; 4.9 cream dome macro; 5.6–7.4 toss, "Available now @ select retailers" | Newness | Hands | Music, −17.6 LUFS | Newness + retail | **Newness hook (Motion D5: 11.37 %) in 7 s** |
| G21 | **Supply "How many blades do you actually need?"** ([link](https://www.tiktok.com/@supply/video/7598402292341148941)) · 2026-01-23 · 381K, **3.31 %**, 477 shares | 59.1 s · 33 · 0.58/s · **4:5** | A 2×2 grid of 1/2/3/5-blade razors, super "How many blades gives the BEST SHAVE POSSIBLE?" | 3.7 drugstore 3-blade pack; 4.9–7.5 man shaving; **7.5–11.6 3D cross-section of a hair pulled and cut below the skin**; 11.6 "4–5 blades"; 14 a cartridge clogged with grass clippings; 16.6–21 redness; **21.4 "1 blade": 3D cut clean at the surface**; 22.6–29 barber single-edge; 29–35 "difficult to use"; 35–38 founders walk in; 38–48 magnetic pivoting head macro; 48–54 three users shaving; 54–59 end card "100 Day Trial | Free Shipping | Lifetime Warranty" | "One blade, zero learning curve" | Many product macros | VO + light bed, −21.7 LUFS | Section labels (red) + captions | **Category myth-busting with CG cross-sections**, Us-vs-them without naming a rival |
| G22 | **Spotlight Oral Care water-flosser stitch** ([link](https://www.tiktok.com/@spotlightoralcare/video/7469767086617709846)) · 2025-02-10 · **20.4M, 0.77 %** (paid) | 37.7 s · 1 | A creator spits water-flosser debris into a glass, super "The moment I realized my waterflosser removed hard plaque", "Stitch incoming…" | 0–5.8 stitched creator clip; 5.8–37.7 dentist co-founder in a clinic explains interdental cleaning | Expert validates a gross reveal | Product only in the stitch | Voice, **−32.7 LUFS** (very quiet) | Stitch + caption | **Gross-out proof + expert** — the biggest view count in the set. Not AI-reproducible (and must not be) |

Supporting (measured, not in the table): Supply "Seki City blades" — 5 s **silent** hands-only blade-loading loop, 354K at 0.37 % (paid) [m]. TheraBreath "the science behind TheraBreath toothpaste" (60 s, 7.6M) — metadata only, the download failed.

### 2.2 Metadata only (YouTube blocked; press descriptions)

| Ad | Date · length | What it is | Evidence |
|---|---|---|---|
| Manscaped **"Hair Ballad"** (Super Bowl) | 2026-02-08 · 30 s / 60 s / 109 s cuts | A man trims his chest; the clumps on the floor sing a power ballad about losing their body and are flushed. Puppets by Can Can Club; VFX Trafik; MJZ; Quality Meats. Adweek top-10 of the game | [Reel Chicago](https://reelchicago.com/article/manscaped-makes-super-bowl-debut-with-singing-hairballs/), [Ads of the World](https://www.adsoftheworld.com/campaigns/hair-ballad), YouTube 280K (id jI9V70EAXiI) |
| Manscaped **"The Boys"** | 2024-04 · 45 s | Two tiny shaggy versions of a man follow him; after the Lawn Mower 5.0 they admire their bald heads. AR lens on TikTok/Snap/IG | [Contagious](https://www.contagious.com/news-and-views/campaign-of-the-week-grooming-brand-personifies-plums-to-prompt-men-to-preen-their-pubes) |
| Dollar Shave Club **"We Put Our Money Where It Matters"** — first AI ad | 2025-12 · 60 s | Boardroom of a fictional "Razor Corp"; AI animates a razor-shaped skyscraper and a gorilla "animal testing" shave; few-week build (Too Short For Modeling) | [Retail Dive](https://www.retaildive.com/news/dollar-shave-clubs-first-ai-generated-ad-makes-tech-the-punchline/808105/), YouTube 13.3K (WqwauvN9C2Q) |
| DSC **"Clean Girls"** (AI) vs filmed spokesperson spot | 2026-04 · 30 s each | Anthropomorphised pastel bath products thrown out; a glitter razor lands in a bin next to "AI videos with Sora". Brand expects the AI spot to win on TikTok | [Marketing Dive](https://www.marketingdive.com/news/dollar-shave-club-swipes-at-competition-in-first-womens-grooming-push/816515/), YouTube (3dZw-kbP7h8) |
| DSC **"250 Years. No BS. Still Free"** (AI, in-house) | 2026-07-01 | Founding-father paintings fight "big razor monopolies"; $2.50 starter kit; Higgsfield + Claude; **$400**; "most successful campaign in our history" [c] | [Modern Retail](https://www.modernretail.co/marketing/how-dollar-shave-club-decides-when-to-use-ai-generated-creative/) |
| DSC **"Danglers"** (Ball Spray, AI) | 2026-07 · 15 s hero | Truck nuts as a stand-in in outsized scenarios; exaggerated look "is part of the joke" | [ContentGrip](https://www.contentgrip.com/dollar-shave-club-ai-ads/) |
| Dr. Squatch × Sydney Sweeney **"Body Wash Genie"** / **"Bathwater Bliss"** | 2024-10 to 2025-06 · 30–33 s | Celebrity genie spot (~36M views across platforms [c]); the follow-up soap sold 5,000 bars in minutes; resale up to $1,000 | [Campaign](https://campaignlive.com/article/final-numbers-sydney-sweeneys-bathwater-campaign-dr-squatch/1937718), [NBC](https://www.nbcchicago.com/entertainment/entertainment-news/sydney-sweeney-bathwater-soap-sold-out-dr-squatch-website/3761751/) |
| Quip **practical "mouth-head" spa** | 2026-03 · 15 s | Actor in a mouth headpiece on a shell daybed with a giant brush; blue-screen composite; accused of being AI | [Modern Retail](https://www.modernretail.co/marketing/quips-latest-ad-wasnt-ai-generated-people-were-convinced-it-was/) |

### 2.3 What the measured set says [m]

- **Product (or the product held in hand) is in frame 0 in 12 of 23** (Snif, Quip ×3, Oars + Alps, Hismile, Henson, Duke Cannon, Harry's, Cremo, Supply ×2). **A text super is on screen by 1 s in ~16 of 23.** That matches docs 45 (D43: product by 2 s in 83 % of long runners) and 47.
- **Paid-signature lengths:** 8.3, 10.7, 17.5, 17.9, 19.9, 37.7, 41.4, 44.6, 60 s → **median 19.9 s**, bimodal: ≤ 20 s hands-only/mood ads and 37–60 s talking/explainer ads. The same split as doc 45 D29.
- **Two families of format sell here:**
  1. **"Show me the mechanism"** — explainer, cross-section, comparison, expert, stunt proof (Henson, Supply, Spotlight, Dossier, Duke Cannon). Long, voice-led, often low cut rate.
  2. **"Make the taboo funny"** — body hair, sweat, dick pics, bad breath (Manscaped ×2, Lume, Hair Ballad, The Boys, Danglers). Character- or creature-led.
  VXO can build family 2 fully and supply family 1's **inserts** (CG cross-sections, macro mechanics, stunt-proof tableaux).
- **Cut rate is not the lever.** It ranges from 0.03/s (Spotlight, 20.4M) to 1.5/s (Duke Cannon, F&R). The fastest posts are the shortest product/scent montages; the biggest reach goes to one-take voices.
- **Audio QC is a real differentiator.** Loudness ranges **−12.5 to −36.4 LUFS**; three posts ship above 0 dBFS (Manscaped +3.0, F&R +2.9, Duke Cannon 0.0) and three are far too quiet (Snow −36.4, Spotlight −32.7, Manscaped rep −23.3). Doc 46's −14 LUFS / ≤ −1 dBTP master is better than most of this category's paid output.
- **Women are in the frame of men's products** — red-nailed hands (Quip), a woman's review (Lume "boob sweat"), a woman presenting (Dossier, Snif), women dermaplaning with a men's razor brand (Leaf). The gift buyer and the co-user are often women `[inf]`; cast hands and supporting characters accordingly.

---

## 3. What converts in this niche (data)

| # | Finding | Number | Source | Status |
|---|---|---|---|---|
| N1 | Beauty & Personal Care on Meta, effectiveness by asset type | UGC 55, **Branded/Studio 54**, Product Shot 52, Lifestyle 46, Graphic 44; median life 21 d; video 56 % | [Benly B&PC Q1 2026](https://benly.ai/benchmarks/q1-2026/beauty-personal-care) | [v] (longevity-based index) |
| N2 | **Men's Grooming sub-industry** | 2.8K creatives, 12 brands, **avg life 47 d**, **video 62 %**, top hook Bold Statement, top asset UGC | same (sub-industry table) | [v], small n (12 brands) |
| N3 | **Fragrance** | UGC **83**, Lifestyle 67, Branded 54, Graphic 47, **Product Shot 43**; median life **18 d**, 25 % survive 30 d; hooks Bold Statement 42.8 %, Visual Intrigue 30.9 %; promo intent **Discount 59.5 %**, New launch 17.9 %; landing on homepage 48 % | [Benly fragrance](https://benly.ai/benchmarks/q1-2026/beauty-personal-care/fragrance) | [v] |
| N4 | B&PC video hooks | Bold Statement 31.7 % (28 d), Visual Intrigue 27.8 % (29 d), Pain Point 15.4 % (29 d), Pattern Interrupt 13.8 % (**31 d**) | Benly B&PC | [v] |
| N5 | Health & Beauty on Meta | Hook rate **28.11 %** (vs 25.44 % all), best CTR, bottom-third ROAS | [Billo H1 2026](https://billo.app/blog/h1-2026-video-ad-benchmarks/) | [v] |
| N6 | Oral care is a TikTok Shop video business | DR.DENT: 91 % of $7.6M GMV via shoppable video, 3.8K affiliates, 15 % commission; Hismile mouthwash debris video → $1.8M in 30 days | FastMoss, BrandArk | [v] |
| N7 | Hismile's Meta formats | Demo 21 %, Before & After 13 %, Testimonial 9 %; heavy offer framing ("buy 3 get 5 free"); live videos 50–78 s | [Motion](https://motionapp.com/library/hismile), [Atria](https://tryatria.com/ads/meta/hismile-ads) | [v] |
| N8 | Dossier's Meta formats | Yapper 15 %, Offer-first 14 %, Us-vs-Them 9 % (price gap vs Bleu de Chanel, BR540) | [Motion](https://motionapp.com/library/dossier) | [v] |
| N9 | Manscaped's Meta formats | Demo most common; Feature-benefit pointout most common image; most variants on bundle/ASMR unboxing | [Motion](https://motionapp.com/library/manscaped) | [v] |
| N10 | Cross-industry (doc 45) | Unboxing 9.83 %, BTS 8.64 %, founder 8.57 %, demo 8.11 %, **cinematic b-roll 6.85 %**; hooks newness 11.37 %, sale 11.35 %, price anchor 10.89 % | doc 45 D3–D5 | Read |
| N11 | AI ads | AI images lift CTR only if they don't look AI; faces cancel the gain (OII, doc 45 D31); 41 % of men "not OK" with AI models (Attest, doc 47); Gartner: 68 % often wonder if content is real, 50 % prefer brands without gen-AI | doc 45, doc 47, [Modern Retail](https://www.modernretail.co/marketing/quips-latest-ad-wasnt-ai-generated-people-were-convinced-it-was/) | Mixed |
| N12 | AI ads in this niche, in practice | DSC: 4+ AI spots in 7 months; one at $400 claimed best-ever; AI used where "the exaggerated look is part of the joke", real footage "where sincerity matters" | Marketing Dive, ContentGrip | [c] |
| N13 | TikTok F&B-style sensory finding, applied | Product sounds (fizz, pour) loved by 64 % in F&B (doc 49 N8); here the equivalents are the **trimmer buzz, blade scrape, spray hiss, brush hum** | doc 49 [inf] | [inf] |

### 3.1 What this means, by sub-niche [inf]

| Sub-niche | Lead format | Proof that sells | Length | VXO's role |
|---|---|---|---|---|
| **Razors** | Comparative explainer (blade count, exposure, cost per blade) | CG cross-section, machining, cost math, lifetime warranty | 15 s hook head + 45–60 s explainer | Make the **hook head** and the **CG mechanism inserts**; client keeps the founder voice |
| **Trimmers / body grooming** | Taboo comedy, creatures, durability/safety proof | "Won't nick" test, waterproof, runtime | 15–30 s | **Creature comedy** and **proof tableaux** (balloon, peach) |
| **Beard / hair care** | Transformation (real), routine, texture | Real before/after by the client; texture macro | 15–20 s | Texture macros, sound gags; **never** an AI beard result |
| **Bar soap / deodorant / body** | Stunts, collabs, limited drops, animated reviews | Durability, 72 h claim (tested), ingredient list | 6–30 s | Drop films per SKU (Season plan), animated reviews (Lume grammar), state-change films |
| **Men's fragrance** | Scent-as-place montage, lecture/education, haul/availability, Us-vs-Them (dupes) | Notes, longevity test (real), retail availability | 6–20 s | **Place montages** and **lectures** — both AI-native; one per scent; monthly |
| **Oral care** | Hands-only feature walk, dentist explainer, gross-out proof (real), whimsical/novelty packs | Expert, real debris, real shade change, numbers with footnotes | 8–20 s hands; 40–60 s explainer | **Hands-only feature films, novelty pack films, mechanism CG**; the proof stays real |

**Placements:** TikTok In-Feed/Spark (native supers, hands-only, comment-reply frames) → TikTok Shop video (must show the product in hand and the price) → Meta Reels (supers burned in; 4:5 cut for feed — Supply runs 4:5) → YouTube/CTV for Super Bowl-style comedy (the big brands). **AI disclosure:** follow doc 45 §5.3 (Meta "AI info", TikTok AIGC toggle, the New York synthetic-performer law). In this niche, disclose and lean in: "Made with AI. The [proof] is real." turns the Oars + Alps / Quip anxiety into a feature `[inf]`.

---

## 4. AI realism pitfalls in this niche, and the fixes

Routing follows doc 43 §1. New niche items are marked **NEW**. Every motion shot starts from an approved still (doc 17). "Proof slot" = 1.5–3 s of the client's real footage.

| Pitfall | What goes wrong | Fix (prompt / reference / model) |
|---|---|---|
| **NEW: Shaving stroke on skin** | The blade path leaves no clean lane, foam regrows behind it, stubble reappears, the jaw reshapes, blood/nicks appear | **Never generate the result.** Cut on the stroke: start still (foam) → end still (clean lane) with Kling 3.0 Pro first/last frame, ≤ 1.5 s, "the lane stays clean; foam only moves forward with the blade; nothing regrows". Better: **proof slot** with the client's real stroke. For comedy, shave **objects** (a balloon, a peach, a foam-covered sculpture), not faces |
| **NEW: Stubble and beard texture** | Texture flickers between frames, density changes on head turns, beard edge drifts; "plastic" male skin | Real-photo face ref, side key light, "visible pores, uneven stubble 2–3 mm, a few grey hairs at the chin, no smoothing"; ≤ 20° head turns; ≤ 5 s per shot; **no AI before/after of a beard**. Grain in post (doc 43 §5) |
| **NEW: Trimmer and razor geometry** | Blade count changes, comb guard morphs, cartridge pivots wrong, LED digits garble | Kling 3.0 Pro i2v from the client's pack photo for every product shot ("rigid metal and plastic, never deforms; exactly [N] blades; guard length [x] mm"); write the mechanism as start/end positions ("the head pivots 15° and returns"); digits only as post supers |
| **NEW: Toothbrush in a mouth** | Extra or merged teeth, gums melt, lips don't seal on the handle, foam appears from nothing, the brush passes through teeth | **Keep mouths out of frame**: profile from behind, mirror out of focus, or the brush shown *before* and *after*. If unavoidable, Seedance 2.5 at 720p, close-mouthed foam only, ≤ 2 s; never a smile result. Quip itself avoids AI "where accuracy matters, like brushing demos" [c] |
| **NEW: Teeth colour** | Any AI shift in shade is a whitening claim (mock-up) | Teeth stay neutral and untouched in every AI frame; shade change only in the client's real, unretouched proof slot with "results vary" (and only if substantiated) |
| **NEW: Toothpaste ribbon** | Stripes swirl or merge, paste extrudes from a capped tube, ribbon floats | Kling first/last frame; "the cap is off before the squeeze; the ribbon exits only from the nozzle; stripes stay parallel; it settles and holds its ridges"; ≤ 2 s |
| **NEW: Floss and water-flosser jets** | Floss passes through teeth; jet is a smoky cone | Floss only on objects/metaphors; jet: "a thin, coherent stream, pulsing ~20 times per second, breaking into droplets after 3 cm" [inf: typical 1,200–1,400 pulses/min] |
| **Spray / mist (cologne, deodorant, SPF)** | Mist reads as smoke or a CG cone; liquid level in the bottle never drops | "Fine atomised cone ~20 cm long, backlit, droplets visible at the edge, settles within 1 s; no smoke" (doc 47 mist row). Level change only between cuts |
| **Glass fragrance bottles** | Refraction wrong, label floats, cap merges with glass, liquid sloshes like water when the bottle is still | Packshot still first; Kling i2v with `last_image_url` = same still; "rigid glass; liquid surface flat when still; one vertical specular moves 2 cm"; label text only from ref |
| **Lather, foam, bubbles** | Uniform bubbles, foam that never collapses | "Irregular bubble sizes, some pop, foam sags slowly" (doc 47); Harry's 6 s bubble loop is the easy version |
| **Soap and solids** | A bar melts or regrows across cuts | Write each state per cut ("week 1: crisp edges; week 6: rounded edges, 30 % smaller") and change it **between** cuts, never during (doc 49 rule) |
| **NEW: Hair falling / clippings** | Clippings appear from nowhere, fall upward, vanish, or don't pile | Object fate (doc 43 rule 12): "clippings fall straight down in < 0.5 s and stay on the sink"; count them for close-ups |
| **NEW: Tattoos, rings, chest hair** | Tattoos and rings change between shots (see the tattooed Beardbrand creator) | Put tattoos and rings in the character sheet or remove them; "no tattoos" is easier to hold than a specific tattoo |
| **NEW: Shower and bath scenes** | Implied nudity triggers Meta's adult-nudity policy; steam fogs into mush | Product on the shelf + hands; shoulders-up in a towel at most; "steam drifts upward and pools at the ceiling"; mirror shows only tile (doc 47 reflections row) |
| **Mirror shots (shaving mirror)** | Mirror shows the wrong room or the camera | Shoot from beside the mirror, never into it; or "the mirror is fogged except a wiped stripe that shows only tile" |
| **Creatures (hairballs, sweat drops, tiny men)** | Scale flicker, creature merges with the human, multiplies | Write scale ("creature 6 cm tall next to a 20 cm trimmer"); one creature per shot unless it's a chorus tableau; tilt-shift macro; stylised materials (felt, fur puppet) read as intentional, not as failed realism (Hair Ballad, Quip practical) |
| **Labels, claims, numbers** | Text softened or misspelled; "15x" rendered wrong | Text only from the ref; every number is a post super with the client's footnote (doc 47) |
| **Faces as proof** | "AI person says it worked" = fake testimonial | No AI person gives a verdict (16 CFR 465). Real reviews can be **re-performed in a stylised medium** (Lume's cartoon) with the reviewer's consent and the claim substantiated |

**Model routing for this niche** (doc 43 §1, §6 list prices [EST]):

| Shot type | Model | Settings | Cost per take |
|---|---|---|---|
| Product insert (razor head, trimmer, bottle, tube, brush) | Kling 3.0 Pro i2v | 5 s, `sound:"off"`, `cfg_scale` 0.5, `last_image_url` = same still | $0.48 |
| State change (foam → clean lane on an object, full → used soap, cap on → off) | Kling 3.0 Pro i2v first/last frame | 5 s, path only | $0.48 |
| Hero packshot one-take (spray, condensation, dolly-in) | Cinema Studio 4.0 | `pacing:"single-shot"`, `camera_movement:"dolly-in"`, 720p, 8 s | $3.70 |
| Comedy multi-shot with people/creatures | Seedance 2.5 r2v | 9:16, 10–15 s, "exactly N shots", product = first ref | $3.09 (480p proof) / $6.93 (720p, 15 s) |
| CG mechanism (hair cross-section, blade exposure, enamel layers) | **Still from an image model → Kling i2v** with "clean 3D medical illustration, matte materials, no text" | 5 s per insert | $0.30 + $0.48 |
| Scent-as-place montage (12–14 stills × 0.4 s) | **Stills only** (no video needed), Ken Burns/parallax in edit; 2–3 Kling i2v for the moving ones | 14 stills | ~$4–6 |
| Dialogue to camera (spokes-character) | Seedance 2.5 r2v dialogue block, or Wan 3.0 r2v + `audio_urls` for a fixed VO (doc 43 §7.4) | ≤ 12 s per line | $1.00 per 10 s (Wan 720p) |
| Blocking previs | Wan 3.0 r2v 480p | fixed seed | $0.50 / 10 s |
| Any result on skin, beard, teeth, sweat, odour | **Real proof slot** from the client | 1.5–3 s | $0 generation |

**Style header delta (add to doc 11's headers for this niche):** "Product-film still, 100 mm macro, hard side key or window light, real bathroom surfaces (tile, chrome, porcelain, wet glass), label text '[EXACT]' is the only readable text, rigid metal and glass never deform, exactly [N] blades, foam with irregular bubbles, real male skin with pores and uneven stubble, no smoothing, no beauty retouch, no teeth shade change, exactly five fingers per hand, no tattoos or rings unless in the reference."

---

## 5. Policy and legal (US first; the client's counsel has the final word)

### 5.1 Where cosmetic ends and drug begins
| Product | Status | Safe on screen | Never on screen | Source |
|---|---|---|---|---|
| Fluoride toothpaste, anticavity rinse | **OTC drug** (monograph) | "Fluoride toothpaste", "aids in the prevention of cavities" (label wording) | "Repairs enamel", "reverses cavities", "heals gums" | [otclabels/FDA labels](https://otclabels.com/lib/otc/otc-meds/advanced-whitening-anticavity-fluoride-1/) |
| Nano-hydroxyapatite toothpaste (fluoride-free) | Cosmetic unless drug claims | "With nano-hydroxyapatite"; sensory/cleaning claims | "Remineralizes" / "rebuilds enamel" without product-specific tests (Boka, NARB 2025) | NARB panel, Essor/Boka, July 2025 ([BBB National Programs decisions](https://bbbprograms.org/media/newsroom/decisions); read via search summary, primary page not opened) [unverified primary] |
| Whitening strips, serums, LED kits | Cosmetic; claims heavily challenged | "Removes surface stains" **with product-specific substantiation**; shade numbers only from the client's study, footnoted | "Instant", "permanent", "enamel safe" (NAD: GuruNanda Mar 2025, Lumineux Jan 2025), "dentist recommended" without a survey | [NAD GuruNanda](https://bbbprograms.org/media/newsroom/decisions/gurunanda-enamel-safe), [NAD Lumineux](https://bbbprograms.org/media-center/dd/oral-essentials-lumineux-mouthwash), [ASA Hismile V34, Apr 2024](https://www.asa.org.uk/rulings/hismile-pty-ltd-g23-1212696-hismile-pty-ltd.html) |
| Antiperspirant | **OTC drug** (aluminium salt) | "Antiperspirant", "reduces underarm wetness" (label) | Wetness claims on an **aluminium-free deodorant** (NAD vs Native) | [HBW on Native](https://hbw.pharmaintelligence.informa.com/RS149550/NAD-Decision-Against-Native-Deodorant-AntiWetness-Claims-Holds-Up-On-Appeal) |
| Deodorant (incl. whole-body) | Cosmetic | "Controls odour", "72-hour" **only if tested** (Lume shows "72Hr") | "Kills bacteria for 72 hours" without a test; medical claims about infections | — |
| Hair regrowth (minoxidil, finasteride) | **Drug** (OTC monograph / Rx) | Only the approved label claims; fair balance for Rx | Any regrowth claim on a non-drug ("thicker hair in 30 days") — FDA has issued warning letters | [PMC study](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11105151/) |
| Beard oil, balm, soap | Cosmetic | Sensory ("softens the feel", "tames the look") | "Grows your beard", "fills patches" | [inf, FDA cosmetic vs drug] |
| Fragrance | Cosmetic | Notes, longevity **if tested**, "inspired by" only with legal sign-off | "Pheromones attract women", guaranteed compliments as fact | [inf] |

### 5.2 FTC, NAD and courts
- **Mock-up doctrine:** an AI shot of a smoother shave, a whiter smile, a thicker beard or "odour gone" is a demonstration. Allowed only as obvious metaphor or with "Dramatization", and only if the claim itself is proven elsewhere (doc 47 §4.3).
- **Fake reviews rule (16 CFR 465, Oct 2024):** no AI customers giving verdicts; no invented review cards. A **real** review re-voiced or animated (Lume) is fine with consent and if typical.
- **Endorsements (16 CFR 255):** creator content needs #ad (Hismile's creator post carries #ad [m]).
- **Comparative ads:** "1 blade beats 5" must be substantiated and must not name or show a rival's trademarked product in an AI frame. Supply shows generic drugstore cartridges [m]; keep it generic.
- **Fragrance dupes:** lawful in themselves, but trademark/false-advertising risk rises when the ad names the famous perfume, implies affiliation or makes unproven "smells identical" claims (Sol de Janeiro v. MCo Beauty, 2024; EU: L'Oréal v Bellure). **VXO never puts a real luxury bottle, logo or name in an AI frame**; "inspired by" copy comes from the client's legal-approved text only ([Glossy](https://www.glossy.co/beauty/dupe-fragrance-has-hit-the-mainstream-now-what/), [Dreyfus](https://www.dreyfus.fr/en/2025/09/04/the-protection-of-olfactory-creations-how-to-combat-perfume-dupes/)).
- **Right of publicity:** no celebrity faces, names or look-alikes (the "Wolverine's beard" format uses a real actor's photo — fine for a creator's organic post maybe, not for a VXO paid film).
- **Subscriptions:** razor-blade, toothpaste and telehealth subscriptions fall under ROSCA/negative-option rules; the FTC sued Hims & Hers in July 2026 over billing and health-data sharing ([McDermott](https://www.mcdermottlaw.com/insights/ftc-two-states-take-aim-at-hims-hers-subscription-and-health-data-practices/)). Any "subscribe & save" end card needs the client's exact terms.

### 5.3 Platform rules
- **Meta, Adult Nudity & Sexual Activity (ads):** no nudity, "sexually suggestive poses or activities", nudity covered only by an overlay, "gestures that suggest genitalia or sex acts", or sexual audio; even "artistic implied nudity" is shown as non-compliant; the UK version asks for 18+ targeting on body-part-focused imagery ([Meta](https://transparency.meta.com/policies/ad-standards/objectionable-content/adult-nudity-and-sexual-activity)). **Body-grooming humour must work through metaphor** (plums, hedges, hairballs, creatures), never a gesture, a crotch focus or a shower body.
- **Meta, personal health:** no negative self-perception addressed to the viewer ("Ashamed of your yellow teeth?") — doc 47 §4.4; Hismile's crude hooks ("maggot mouth") are a risk a small brand can't carry `[inf]`.
- **Meta, telehealth / prescription drugs:** LegitScript certification needed `[unverified exact current terms]`.
- **TikTok Adult content policy** (updated Aug 2026): sexually suggestive content restricted; ads also fall under the inventory filter that excludes "any nudity or sexually suggestive acts" ([TikTok](https://ads.tiktok.com/help/article/tiktok-ads-policy-adult-content)). **TikTok Healthcare policy:** no medical claims, no "exaggerated performance", no results comparable to procedures ("veneers in a bottle" is out) (doc 47 §4.4).
- **Teens:** men's grooming households with teens spend +26 % (NIQ) and "looksmaxxing" drives Based Bodyworks' reach. Do not target or address minors with appearance-anxiety messages; keep teen-coded characters out; TikTok youth-safety rules apply (doc 49 §4.2).
- **AI disclosure:** doc 45 §5.3. For an AI person in an ad shown in New York, the synthetic-performer disclosure applies (in force 9 Jun 2026). VXO default end-card line: "Made with AI. The [proof] is real." `[inf]`

### 5.4 Pre-flight checklist for this niche (add to doc 45 §5.4 and doc 46 §7)
1. Every claim on screen is on the client's approved list, with its footnote; drug-type verbs (repair, regrow, heal, prevent, remineralize, stop sweat on non-AP) are absent.
2. No AI frame shows a result on skin, beard, hair, teeth, sweat or odour. Results appear only in the real proof slot, unretouched, with "results vary" if needed.
3. Teeth in AI frames are untouched and neutral; mouths mostly out of frame.
4. Blade count, guard length, LED digits and label text match the reference in every frame (frame strip at 2 fps).
5. No real competitor product, bottle, logo or celebrity in any AI frame.
6. No nudity, implied nudity, crotch focus or genital gesture; body-hair humour via metaphor only.
7. Disclosure line present when an AI person appears; #ad on any creator cut.
8. Audio master −14 LUFS, ≤ −1 dBTP (half the measured category ships outside this).

---

## 6. The buyer

### 6.1 Who signs a $1,200–3,500 film
| Brand stage | Who decides | How they buy | Evidence |
|---|---|---|---|
| < $5M, founder-led (beard, soap, floss, fragrance, toothpaste) | **The founder**, often the face and the product expert (machinist, barber, dentist, chemist) | Card after seeing frames; launch-driven; a Short to test | Bite, Cocofloss, Beardbrand, Henson are founder-voiced [m] |
| $5–60M, Amazon/TikTok-Shop-heavy or entering Walmart/Target/Ulta | **Head of Growth/Performance** + founder approval; sometimes a creative strategist running affiliates | Needs volume: variants, hook heads, a monthly cadence (Season) | Viking Revolution (Walmart Connect plan), Dossier (Boots/Target), Snif (Ulta) [c] |
| $60M+ / corporate (DSC, Dr. Squatch, Manscaped, Hismile) | CMO + agency + **in-house AI team** | Out of lane, or only via their agencies | DSC in-house Higgsfield team [c] |

### 6.2 What they fear (ranked) [inf, with evidence]
1. **"It'll look AI and the comments will say so."** Quip got "This is AI" on a practical ad; Oars + Alps now advertises "real". Men are slightly less hostile than women (41 % vs 52 % not OK with AI models), but the trust tax is the same.
2. **"It won't show the product working."** This category sells mechanisms and results — and AI can't legally fake results. They need to see how VXO handles proof (§4: proof slot + mechanism CG).
3. **Claims trouble.** NARB/NAD in oral care, OTC lines on toothpaste/antiperspirant, FTC on subscriptions.
4. **Wrong hardware.** A razor with the wrong blade count or a trimmer with a morphing guard is a product defect on screen; their customers are gear nerds (Henson/Supply comments).
5. **Off-voice humour.** Men's brands live on a precise joke register (DSC irreverent, Duke Cannon "big", Manscaped cheeky). Generic AI comedy reads as cringe.
6. **Ad rejection** for innuendo (body grooming) or health claims.

### 6.3 What proof makes them pay $1,200–3,500
- **Five frames from their own product photo** with the right blade count/guard/label and a niche-correct physical detail (foam with irregular bubbles, stubble with real texture, a correct spray cone). Niche-specific 5 frames: (1) mechanism macro, (2) packshot on a real bathroom surface, (3) the hook frame of the concept, (4) a creature/metaphor frame or a place frame (fragrance), (5) the end card with their real offer.
- **A measured comparison**: their category's paid winner (§2) next to our hook frame and cut plan.
- **The proof-slot plan**: "You film 3 seconds of a real stroke/swatch/rinse on a phone; we build the world around it." It answers fears 1–3 at once.
- **Claims pre-flight** (§5.4) up front, in their category's words (fluoride = OTC, "enamel safe" NAD case). This alone signals we're not a generic AI shop.
- **Variant math** tied to the creative-life data: grooming 47 d → one hero per launch + 3 hook heads + 6 s loop; fragrance 18 d → a monthly drop pack.
- **Speed against the calendar**: "Father's Day film in 10 days."

### 6.4 Re-buy triggers (what makes them book again)
1. **SKU velocity:** Dr. Squatch shipped 17 new products in 60 days, Snif 15, Oakcha 47, Smile Actives 10, Scotch Porter 6 on one day [m]. Each scent/flavour/collab = a film (Season plan).
2. **Creative fatigue:** fragrance median 18 d; beauty 21 d; grooming ~47 d average (N2–N3).
3. **Calendar:** Father's Day, Dec 1/Movember, BFCM, Valentine's, summer (§1.5).
4. **Retail launches:** Ulta, Target, Walmart, Boots: each needs a "now at…" film (Snif 11.1M paid on an Ulta haul [m]).
5. **Collabs and limited editions:** Harry's × Scrub Daddy, Dr. Squatch × One Piece / Stranger Things / Speed [m].
6. **TikTok Shop campaigns:** affiliate seeding needs a brand "hero" asset for creators to riff on.

### 6.5 Best outreach angle
**"Your mechanism, made visible — and your proof stays real."** For hardware (razors, trimmers, brushes): offer the CG cross-section/mechanism insert plus a comedy hook head for their existing explainer. For consumables (soap, deodorant, fragrance, toothpaste): offer a **drop film per SKU** timed to the next calendar moment. Lead with a specific, measured observation about one of their ads (doc `vxo-leads` §3 rule).

**Sample first DM (NOT SENT — template; a real one needs a dossier and the owner's approval):**
> Hi [Name] — your "[exact hook line]" ad is the clearest blade-exposure explanation I've seen; the founder-at-the-machine shot does all the work. One idea: open it with a 3-second cross-section of a hair being cut under the skin, then your stroke. I make AI product films (no shoot), and the proof stays your real footage. Want 5 free frames for [razor], or for the [new SKU]?

(57 words; one compliment, one visual idea, one line on what we do, a yes/yes question; no links — `vxo-leads` §3.)

### 6.6 Twenty example brand types (no outreach)
1. Single-blade / safety razor maker (engineering story)
2. Pivoting safety razor with refills
3. Body trimmer for men (ceramic blade, waterproof)
4. Head shaver for bald men
5. Beard oil/balm line (scent-led)
6. Beard & hair care for Black men (texture, shaping)
7. Natural bar soap for men (scent drops, collabs)
8. Whole-body deodorant (unisex or men's)
9. Aluminium-free deodorant (no wetness claims)
10. Men's solid cologne / travel fragrance
11. "Inspired-by" fragrance house (dupes + originals)
12. Niche men's eau de parfum (place-based scents)
13. Men's skincare starter kit (moisturiser + SPF)
14. Men's concealer / tinted moisturiser
15. Nano-hydroxyapatite toothpaste
16. Flavoured / novelty toothpaste (whimsical packs)
17. Expanding floss and floss picks
18. Water flosser / sonic toothbrush (hardware)
19. Whitening strips / LED kit (claims-heavy; proof slot mandatory)
20. Breath spray / tongue scraper / oral probiotic mints

---

## 7. Lead signals: a niche scoring add-on for `.claude/skills/vxo-leads/SKILL.md`

Apply on top of the base 100-point score (base table in the skill). The add-on can move a lead by **−25 to +30**; HOT stays ≥ 70 after the add-on. Check every item with public pages only.

| Signal | Points | How to check |
|---|---|---|
| **Calendar window**: 5–7 weeks before Father's Day (late Apr–mid May), Dec 1/BFCM (mid Oct–early Nov), Valentine's (early–mid Jan), summer body (May) | +8 | Today's date vs §1.5; the brand sells a gift set or a seasonal SKU |
| **SKU velocity**: ≥ 3 new products in the last 60 days in `products.json` (ignore "[Test]" and gift cards) | +6 | `https://<store>/products.json?limit=250`, `created_at` |
| **Retail launch announced** (Ulta, Target, Walmart, Boots, Sephora) in the last 90 days or upcoming | +6 | Press, LinkedIn, store locator; "now at…" ads |
| **TikTok Shop just opened / affiliate push** ("now on TikTok Shop" post; creators with #[brand]partner) | +5 | Brand TikTok embed page; Scotch Porter posted this on 2026-06-16 [m] |
| **Hardware with a mechanism story** (razor, trimmer, brush, flosser) and **no mechanism visual** in their ads (talking head only) | +5 | Their pinned/top TikToks, Meta library mirrors |
| **Paid but weak video**: posts with the paid signature (≥ 500K, like rate < 1 %) that are static/slideshow/feature walks, or Meta library ≥ 70 % images | +4 | yt-dlp metadata on embed IDs; Motion/Atria pages |
| **Audio or format faults** in their paid video (peaks above 0 dBFS, < −24 LUFS, no supers by 1 s) | +2 | `ebur128` on one public post — a concrete compliment/critique for the DM |
| Claims-heavy sub-niche (whitening, hair regrowth, AP) **with** visible compliance care (footnotes, "results vary") | +2 | They'll value the §5.4 checklist |
| Claims-heavy sub-niche **with** risky claims now running ("instant", "enamel safe", "regrow", "dentist recommended" unsupported) | **−10** | They may want VXO to amplify a claim we can't make |
| Telehealth / Rx (hair loss, ED) | **−15** | Regulated, LegitScript, fair balance — out of lane |
| Brand already has an **in-house AI team** or names Higgsfield/AI studios in job posts or press | −8 | Press (DSC), job boards |
| Core message depends on sexual innuendo beyond metaphor (crotch focus, genital gestures) | −5 | Their ads; Meta/TikTok rejection risk |
| Corporate-owned (P&G, Unilever, Edgewell, S.C. Johnson, Essor) | −5 | Ownership; buying path runs through agencies |

**VERY hot in this niche looks like** [inf]: a founder-led razor/trimmer/oral-hardware or fragrance brand, $2–30M, with a new SKU or retail door in the last 60 days, a calendar moment 5–7 weeks out, paid posts that are hands-only feature walks or talking heads without a mechanism visual, and no in-house AI team. Score example: base 72 + calendar 8 + SKU 6 + mechanism gap 5 = 91.

---

## 8. Ten ready film concepts (invented brands, VXO spec)

Conventions:
- Invented brands and packs; clear names on USPTO before use. No real-brand look-alikes. **Otto and Vee are absent** (client-style specs). Any of these can become a VXO spec film by casting Otto as the deadpan lead (mouth never visible = no lip-sync risk); concept 4 is the most Otto-ready.
- Every camera position is a real rig (tripod, slider, dolly, overhead arm, Steadicam, hard mount, phone handheld). The camera never passes through glass, walls or bodies (LESSONS 2026-10-08).
- No AI person shows a result on skin, beard or teeth. Each concept names its **proof slot** (client's real footage) where a claim is made. Claims on supers are placeholders the client replaces with its approved list.
- Every film ends with the 2-line VO tagline in a locked voice over a frame with no visible lips, plus the logo card (LESSONS 2026-10-09).
- **Costs** use doc 43 §6 list prices: Seedance 2.5 r2v 15 s = $3.09 at 480p (proof) and $6.93 per 720p take (×3 = $20.79); Kling 3.0 Pro i2v 5 s sound-off = $0.48 per take (×2); Cinema Studio 4.0 720p 8 s = $3.70; stills ≈ $0.30; ElevenLabs VO ≈ $0.10. Totals exclude the client's proof slot.

---

### C1 · OXBOW (single-blade safety razor) — "Blade Count" (20 s) ★ BEST 3
- **Idea:** a sterile R&D lab of a fictional razor giant keeps adding blades: 5, 8, 14… The engineer feeds blade #31 into a cartridge the width of a paperback. Cut to a bathroom: one OXBOW, one blade, one stroke. The product is the anti-climax, and the anti-climax is the joke.
- **Hook (0–1 s):** ECU: a gloved hand clicks blade #31 into a monstrous cartridge, "CLACK", super "Blade #31."
- **Punchline (product-caused):** the lab's 31-blade cartridge is wheeled past on a trolley; our man shaves with one blade; super "One. Done right." The joke works only because the product has one blade.
- **Built on:** Supply's "How many blades" (3.31 % likes) [m], Henson's blade-exposure explainer (33M) [m], DSC's corporate-boardroom satire.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.2 | Macro on a slider, lab bench | Blade #31 clicks into the giant cartridge; slider creeps 1 cm |
| 2 | 1.2–3.0 | Overhead arm, locked | A wall chart: "Blades per cartridge 1971→2026", the line rising off the chart (unreadable except the numbers, post supers) |
| 3 | 3.0–5.0 | Medium, tripod, lab | Two engineers in white coats nod gravely at the cartridge on a pedestal (AI people, deadpan) |
| 4 | 5.0–7.0 | Low wide, dolly track | The cartridge is wheeled on a trolley through the lab doors; its width scrapes both door frames |
| 5 | 7.0–9.5 | **CG cross-section** (still → Kling) | Hair at the skin line: many blades tug the hair, the last one cuts below the surface (dramatised; super "Dramatization") |
| 6 | 9.5–12.0 | **CG cross-section** | One blade at the correct angle cuts the hair cleanly at the surface |
| 7 | 12.0–15.0 | **Proof slot**: client's real stroke | One stroke through foam on a real cheek, phone 4K 60 fps |
| 8 | 15.0–17.0 | Macro, Kling | OXBOW head pivots 15° and returns; label crisp |
| 9 | 17.0–20.0 | Packshot on a porcelain sink edge, Cinema Studio dolly-in | The single blade glints; super "One. Done right." + offer |

- **Physics check:** a double-edge blade is ~0.1 mm thick and ~43 mm long [inf]; the 31-blade cartridge is ~110 mm wide and stays **rigid**; the trolley's casters roll at walking pace (~1.3 m/s), and the cartridge scrapes the 80 cm doorway because it's on a 90 cm fixture (write the fixture width). Cross-sections are labelled illustrations, not demonstrations. Foam is only in the real slot.
- **Audio map:** 0.0 cleanroom HVAC hum; 0.6 heavy "CLACK" (metal, layered); 1.5 marker squeak on chart; 3.2 two lab-coat rustles; 5.0 trolley casters + 6.4 door-frame scrape ×2; 7.0 soft "tug" foley ×3 (dramatised); 9.5 a single clean "tsk"; 12.0 real stroke sound from the slot (keep it); 15.0 pivot click; 16.5 bed in (dry brass, 92 bpm); 18.0 VO: "Thirty-one blades. Or one that's right. OXBOW." 19.5 logo tick.
- **Models / template:** Seedance 2.5 r2v 10 s for 3–4 (doc 43 §7.5 comedic reveal, adapted, "exactly two shots"); Kling 3.0 Pro i2v for 1, 2, 5, 6, 8; Cinema Studio 4.0 for 9 (§7.3).
- **Est. cost:** stills 9 × $0.30 = $2.70; Seedance 10 s 480p $2.06 + 720p ×3 $13.86; Kling 5 × 2 × $0.48 = $4.80; Cinema Studio $3.70; VO $0.10 → **≈ $27**.
- **Claim check:** comparative claim generic only (no rival trademark); "Dramatization" on the cross-sections; the "irritation" benefit only if the client substantiates it.

### C2 · LONGSHOT (cordless beard & body trimmer) — "Midnight, December 1" (15 s)
- **Idea:** No-Shave November ends at midnight. A barbershop full of bearded men waits with corded trimmers like a New Year countdown. At 00:00 everyone hits "on"; the breaker trips; total darkness. One LONGSHOT keeps buzzing, its blue LED the only light.
- **Hook (0–1 s):** a wall clock at 23:59:57, nine men holding trimmers like party poppers; super "Nov 30, 11:59 p.m."
- **Punchline (product-caused):** the darkness, one buzz, one LED; the barber's flashlight finds our man, already half-trimmed, calm. Super "Cordless. 120-min runtime." (client claim). It's funny only because the product is cordless.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.5 | Medium wide, tripod, shop | Clock 23:59:57; nine bearded men in chairs, trimmers raised |
| 2 | 1.5–3.0 | Insert, locked | One overloaded power strip: nine trimmer plugs plus a hair dryer and a kettle, daisy-chained |
| 3 | 3.0–4.5 | Close, slider | Clock hand hits 12 |
| 4 | 4.5–6.0 | Wide, same as 1 | Nine "clicks", a roar of buzz for 0.4 s — then the breaker pops; darkness |
| 5 | 6.0–8.5 | Wide, same frame, black | One buzz continues; a single blue LED at frame right |
| 6 | 8.5–11.0 | Medium, barber's flashlight beam (handheld) | The beam finds our man trimming calmly, half his beard done |
| 7 | 11.0–13.0 | Macro, Kling | LONGSHOT body, LED, no cord; clippings fall straight down |
| 8 | 13.0–15.0 | Packshot on the shop counter under the flashlight | Super + "Shop the cordless" |

- **Physics check:** the breaker trips on inrush (9 trimmers ≈ tiny load — so write a **hair dryer + kettle** on the same strip to make the trip plausible); the dark frame keeps faint exit-sign spill; clippings fall in < 0.5 s; the trimmer guard never morphs (Kling from pack photo); no result shown on the face (half-beard is mid-action, not a claim).
- **Audio map:** 0.0 shop chatter murmur; 1.0 clock tick ×3; 3.8 crowd "10, 9…" whispered under; 4.5 nine clicks + buzz roar; 4.9 breaker "THUNK", total silence 0.5 s; 5.5 one trimmer buzz alone (close-miked); 8.5 flashlight click; 11.0 clipping patter; 13.0 bed (soul organ, 80 bpm); 13.5 VO: "Everyone else plugged in. LONGSHOT." 14.6 logo.
- **Models / template:** Seedance 2.5 r2v 15 s for 1, 3–6 (≤ 3 people in focus; others soft); Kling for 2, 7, 8.
- **Est. cost:** stills 8 $2.40 + Seedance 480p $3.09 + 720p ×3 $20.79 + Kling 3 × 2 $2.88 + VO → **≈ $29**.

### C3 · KEEL (body trimmer, skin-safe guard) — "Balloon Test" (12 s) ★ BEST 3 · ★ SINGLE BEST
- **Idea:** the classic barber-school test, played straight as a tense lab procedure: a balloon coated in shaving foam, a trimmer descending. Everyone flinches. Three passes. The balloon survives. To prove it was a real balloon, the tester taps it with a sewing pin: **POP**.
- **Hook (0–1 s):** ECU of a foam-covered, fully inflated balloon trembling slightly as a buzzing trimmer enters frame; a latex creak; super "Test 1 of 1."
- **Punchline (product-caused):** the pin pop after three clean passes. The pop proves the stakes were real, and the survival is caused by the product's guard. Loops perfectly (pop → black → balloon).
- **Built on:** the category's proof/stunt family (Duke Cannon nails, 26× median [m]; Henson/Supply mechanism) and the doc 47 "sound is the result" device.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.5 | Macro, locked, 100 mm, balloon on a ring stand | Foamed balloon; trimmer enters frame-left, buzzing |
| 2 | 1.5–3.0 | Medium, tripod, lab table | A deadpan tester in safety goggles (hands + torso; face optional) holds the trimmer; a second tech covers her ears |
| 3 | 3.0–5.0 | Macro, slider tracking the pass | Pass 1: foam lifts in a clean 32 mm lane; latex dimples 1–2 mm under the guard and springs back |
| 4 | 5.0–6.5 | Macro, opposite angle | Pass 2 across the top |
| 5 | 6.5–8.0 | **Proof slot**: the client's real balloon test (phone, 60 fps) | Pass 3 — real |
| 6 | 8.0–9.5 | Medium, same as 2 | The tester lowers the trimmer, picks up a sewing pin |
| 7 | 9.5–10.3 | Macro, same as 1 | Pin touches the balloon: POP, foam flecks spray outward |
| 8 | 10.3–12.0 | Packshot, Cinema Studio dolly-in on the foam-flecked table | KEEL standing; super "Skin-safe guard. [client claim]" |

- **Physics check:** a 12-inch latex balloon at ~30 cm diameter has ~0.05–0.1 mm walls [inf]; the guard presses ≤ 2 mm with a visible dimple that recovers in < 0.2 s; the foam lane is the guard width (write it: 32 mm); the pop is instantaneous (< 1 frame at 24 fps), the skin shreds into 2–4 pieces and the foam flecks fly ≤ 40 cm and land; the balloon is tethered to the ring stand (no floating away). Kling first/last frames for each pass (foamed → laned).
- **Audio map:** 0.0 trimmer buzz close-miked + latex creak at 0.4; 1.6 a tech's sharp inhale; 3.0 pass 1 — buzz pitch drops slightly under load, foam "shhh"; 5.0 pass 2; 6.5 real pass audio from the slot; 8.0 silence (room tone only) 1.0 s; 9.6 tiny "tink" of pin; **9.7 POP** (−1 dBTP peak, clean transient); 9.8 foam pattering; 10.3 bed (tight snare, 100 bpm); 10.8 VO: "If it's gentle on this… KEEL." 11.8 logo.
- **Models / template:** Kling 3.0 Pro i2v first/last for 1, 3, 4, 7 (single-move inserts); Seedance 2.5 r2v 5 s for 2 + 6 as a 2-shot clip (doc 43 §7.5, "exactly two shots"); Cinema Studio for 8.
- **Est. cost:** stills 8 $2.40 + Kling 4 × 2 $3.84 + Seedance 5 s 480p $1.03 + 720p ×3 $6.93 + Cinema Studio $3.70 + VO → **≈ $18**.
- **Why it's the best:** hook in motion at frame 0 with physical tension, a punchline that is a pure sound event the product causes, no faces needed, no innuendo, a real proof slot for the claim, a loopable 6 s cutdown (shots 1, 3, 7), and it re-skins to any trimmer/razor/shaver brand. Policy-clean on Meta and TikTok.

### C4 · CEDARLINE (men's eau de parfum) — "Floor 12" (20 s)
- **Idea:** a man steps into an office elevator wearing CEDARLINE. As floors tick, three strangers drift a half-step closer, eyes closed. He exits at 12. The doors close. Nobody gets out. The strangers press 12 again.
- **Hook (0–1 s):** security-camera angle, high corner: elevator doors opening, timestamp burn-in "08:57:12"; super "Floor 1."
- **Punchline (product-caused):** after he leaves, the three ride back to 12 just to stand in the scent. The joke exists only because the scent lingers (claim placeholder "8-hour wear", only if tested).
- **Built on:** "scent translation" (fragrance UGC 83 / product shot 43, N3) and the deadpan tableau (doc 44 §5.6). Otto-ready: Otto as the scent-wearer (back to camera, moustache in profile).

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–2.0 | High corner, locked (ceiling mount) | Doors open, he steps in; three strangers already inside |
| 2 | 2.0–3.5 | Insert, locked | Floor display 3 → 5 (digits as post super) |
| 3 | 3.5–6.0 | Medium two-shot, tripod at shoulder height in the back corner | Stranger A's eyes close; a half-step closer |
| 4 | 6.0–8.0 | Same as 1 | All three have drifted 15 cm closer; he stays still |
| 5 | 8.0–10.0 | Close, his hands | He adjusts his cuff; a faint spray mist memory (no spray now) |
| 6 | 10.0–12.0 | Same as 1 | "Ding", floor 12; he exits; the doors close on the three |
| 7 | 12.0–15.0 | Insert: button panel, locked | A finger presses "12" again; then two more fingers press it too |
| 8 | 15.0–20.0 | Packshot on a lobby stone ledge, Cinema Studio slow dolly-in, morning light | CEDARLINE bottle; super "[notes]. [tested wear claim]." |

- **Physics check:** elevator cab 2.0 × 1.5 m, so the "drift" is ≤ 15 cm per beat and nobody touches him; screen direction fixed (doors frame-left in every wide); the ceiling camera stays in the corner (no passing through walls); the floor counter is a post super; no spray in the cab (mist only in the packshot if used).
- **Audio map:** 0.0 elevator ding + door rumble; 1.5 muzak (original, 70 bpm) low; 3.5 a long nasal inhale (stranger A); 6.0 fabric shuffle ×3; 8.0 cufflink click; 10.0 "ding", door rumble; 12.5 button click ×3 (rising rhythm); 15.0 muzak swells into the brand bed; 17.5 VO: "It stays after you leave. CEDARLINE." 19.5 logo.
- **Models / template:** Seedance 2.5 r2v 15 s for 1, 3, 4, 6, 7 ("exactly five shots", 4 people max, faces deadpan, no dialogue); Kling for 2, 5; Cinema Studio for 8.
- **Est. cost:** stills 8 $2.40 + Seedance 480p $3.09 + 720p ×3 $20.79 + Kling 2 × 2 $1.92 + Cinema Studio $3.70 → **≈ $32**.
- **Claim check:** "lingers" is puffery unless a duration is stated; any hour number needs the client's test. Strangers sniff, nobody is harassed or touched.

### C5 · NORTHFORK (men's cologne) — "Smells Like" (10 s place montage)
- **Idea:** Fulton & Roark grammar, built from AI stills: "Need a cologne that smells like the first cold morning at a lake cabin?" — 12 images at 0.4 s (frost on a canoe, woodsmoke, a wool cuff, coffee steam, cedar shavings, a dog's breath in cold air, a cast-iron pan, a pine needle on a dock…) collapsing into the bottle standing on the dock with three note icons.
- **Hook (0–1 s):** frost crystals cracking on a canoe gunwale as a thumb presses it; serif super.
- **Punchline (product-caused):** the last montage image is the dock; the bottle is now standing in that exact spot, condensation on the glass — the place became the bottle.

| # | t (s) | Shot | Action |
|---|---|---|---|
| 1–12 | 0.0–4.8 | 12 stills, 0.4 s each, parallax in edit (2–3 animated via Kling) | Frost, smoke, wool, steam, cedar shavings, dog breath, pan, needle, lake mist, boot on dock, hand on axe handle, dawn ripple |
| 13 | 4.8–6.0 | Kling i2v | Bottle fades in on the dock planks (one move, rigid glass) |
| 14 | 6.0–10.0 | Locked | Bottle + "NORTHFORK · Cedar · Woodsmoke · Cold Air" icons; VO |

- **Physics check:** steam and breath as thin wisps that rise and vanish within 10 cm (doc 49 steam row); frost cracks propagate from the thumb outward; bottle condensation beads uneven with 1–2 trails; dawn light from frame-left in every still (one sun direction).
- **Audio map:** 0.0 frost crackle; 0.4–4.8 one sound per image (fire crackle, wool rub, coffee pour, axe tap, loon call at 3.2, dock creak) cut on the beat of a 150 bpm acoustic pluck; 4.8 bed resolves; 6.5 VO: "Bottled at dawn. NORTHFORK." 9.5 logo tick. Master −14 LUFS, ≤ −1 dBTP (F&R's original clips at +2.9 dBFS [m]).
- **Models:** image model for 14 stills; Kling 3.0 Pro i2v ×3 (2 animated stills + bottle).
- **Est. cost:** 14 stills $4.20 + Kling 3 × 2 $2.88 + VO → **≈ $7.50**. The cheapest film here; sell it as a **monthly per-scent pack** (fragrance creative life 18 d median, N3).

### C6 · TIDEMARK (sonic toothbrush with a 2-min, 30-s quadrant timer) — "Four Quarters" (15 s)
- **Idea:** a man brushes; the brush's 30-second quadrant pulse becomes a pro-basketball shot-clock buzzer, and his roommate on the sofa outside the bathroom calls the game like a commentator. Four quarters, final buzzer, crowd roar from the TV.
- **Hook (0–1 s):** shot-clock-style digits "0:30" over a bathroom doorway (post super), the brush hum starting; super "Q1."
- **Punchline (product-caused):** at 2:00 the brush stops by itself; the roommate stands and applauds; the man spits off-screen and nods like an MVP. The timer feature is the joke engine.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–2.0 | Wide through the open bathroom door from the hallway, tripod | Man at the sink seen from behind; mirror soft-focus |
| 2 | 2.0–3.5 | Macro, Kling | TIDEMARK pulses (handle LED blinks once) |
| 3 | 3.5–5.5 | Medium, sofa, tripod | Roommate with a bowl of cereal: "Quarter two, he's switching sides" (mouth visible → Seedance dialogue or VO with mouth hidden behind the bowl) |
| 4 | 5.5–7.5 | Wide, same as 1 | Man shifts the brush to the other side (seen from behind) |
| 5 | 7.5–9.5 | Insert, locked | Two-minute timer graphic Q3 → Q4 (post) and the LED pulses |
| 6 | 9.5–11.5 | Medium, sofa | Roommate stands, cereal spills 3 flakes |
| 7 | 11.5–13.0 | Wide, same as 1 | The brush stops on its own; he turns, nods (mouth closed) |
| 8 | 13.0–15.0 | Packshot on the sink, Kling | Brush on its charger; super "2-min timer. 30-sec pulses." |

- **Physics check:** sonic brushes run ~31,000 strokes/min [inf, typical]; on screen that's a blur at the head, not a wobble of the hand; the man is **always seen from behind or mouth closed** (no teeth on screen); spill: 3 flakes fall, they don't multiply; timer graphics are post.
- **Audio map:** 0.0 brush hum (high, steady) + hallway room tone; 2.0 pulse "bzt-bzt" (the product's real sound, recorded from the client's unit); 3.5 roommate line (or VO); 5.5 pulse; 7.5 pulse + TV crowd swell low; 9.5 crowd rising; 11.5 brush stops → arena horn from the TV + crowd roar; 13.0 VO: "Two minutes. Every time. TIDEMARK." 14.6 logo.
- **Models / template:** Seedance 2.5 r2v 15 s multi-shot (1, 3, 4, 6, 7; ≤ 2 people; doc 43 §7.4 B if the roommate speaks on-camera) + Kling for 2, 5, 8.
- **Est. cost:** stills 8 $2.40 + Seedance 480p $3.09 + 720p ×3 $20.79 + Kling 3 × 2 $2.88 + VO → **≈ $29**.
- **Claim check:** the timer is a feature (safe); any plaque claim needs the client's study and footnote (Quip's "15x" [m] is the model).

### C7 · GUMLINE (expanding floss) — "Gone Fishing" (15 s)
- **Idea:** an old fisherman on a jetty fights a big fish on a tiny spool. Line hums, rod bends. He lands it. Then, deadpan, he snips 40 cm off the same spool and flosses (back to camera, sunset).
- **Hook (0–1 s):** a reel screaming as line peels off a tiny turquoise spool clamped to a rod; spray flies off the line.
- **Punchline (product-caused):** the reveal that the "line" is the floss — "Shred-resistant. [client claim]" — and that he uses it for its real job.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.5 | Macro, hard-mounted to the rod butt | Spool spinning, line peeling, water spray |
| 2 | 1.5–3.5 | Wide, tripod on the jetty | Old man leaning back, rod bent in a deep arc |
| 3 | 3.5–5.0 | Low on the water, boat-mounted | The fish breaks the surface (a 2 kg sea bass, not a monster) |
| 4 | 5.0–7.0 | Medium | He lands it in a net; checks the line: intact, still fluffy where it expanded |
| 5 | 7.0–9.0 | Insert, Kling | The spool label turns to camera: GUMLINE |
| 6 | 9.0–11.0 | Medium from behind, sunset | He snips 40 cm with teeth-free scissors, lifts it to his mouth (back to camera) |
| 7 | 11.0–13.0 | Wide silhouette | He flosses, seagull lands beside him |
| 8 | 13.0–15.0 | Packshot on the jetty plank | Spool + box; super |

- **Physics check:** a 2 kg fish on a light rod gives a rod arc of ~60–90° [inf]; the line stays taut in a straight path from tip to water (no slack loops while loaded); spray comes off the spool on spin; the fish is released or netted, never harmed on screen; **floss strength claim only with the client's test** — otherwise drop the claim and keep the gag as metaphor ("Dramatization").
- **Audio map:** 0.0 reel drag scream; 1.5 gulls, waves; 3.5 fish splash; 5.0 net swish; 7.0 quiet; 9.0 scissor snip; 11.0 seagull landing flap; 13.0 bed (slide guitar, 76 bpm); 13.5 VO: "Strong enough. Gentle enough. GUMLINE." 14.6 logo.
- **Models:** Seedance 2.5 r2v 15 s (1–4, 6–7; one person + a fish); Kling for 5, 8.
- **Est. cost:** ≈ **$29** (same structure as C6).

### C8 · GRANITE BAR (cold-process men's soap) — "Last Bar Standing" (15 s) ★ BEST 3
- **Idea:** one shower shelf, six weeks, a locked-off camera. Week by week, three generic soaps slump into puddles and are replaced; GRANITE BAR just gets slightly rounder. Week 6: a new generic bar arrives and is placed next to it; it looks at GRANITE (a tiny 2° tilt).
- **Hook (0–1 s):** a generic soap bar collapsing off the edge of the shelf into the drain with a wet "plop"; super "Week 1."
- **Punchline (product-caused):** week 6, GRANITE is still there; a hand places the fourth newcomer; super "Still here. [client: lasts X washes, tested]."
- **Built on:** doc 49 C2 "Gone by Friday" (states between cuts are AI-safe), Duke Cannon durability proof (26×) [m], NIQ bar soap +33 % [c].

| # | t (s) | Shot (rig) | Action (state per cut, never during) |
|---|---|---|---|
| 1 | 0.0–1.5 | Locked-off, wall-mounted, shower shelf | Week 1: generic bar slides off the wet edge into the drain |
| 2 | 1.5–3.5 | Same frame | Week 2: a new generic bar, already slumped; GRANITE crisp |
| 3 | 3.5–5.5 | Same frame | Week 3: generic #2 a puddle in its dish |
| 4 | 5.5–7.5 | Macro, Kling | GRANITE's edge: barely rounded, label stamp legible |
| 5 | 7.5–9.5 | Same frame | Week 4–5 (time-lapse light shift): generic #3 cracked and shrinking |
| 6 | 9.5–11.5 | Same frame | Week 6: a hand places generic #4 beside GRANITE |
| 7 | 11.5–15.0 | Packshot on the same shelf, Cinema Studio slow push | GRANITE + box, steam wisps; super + offer |

- **Physics check:** a cold-process bar at ~110 g loses mass gradually; write each week's size: GRANITE 100 → 92 → 85 → 78 % (rounded corners only); generic bars slump (softening from the base where water pools, write "a puddle forms only where the dish holds water"); steam rises and pools at the ceiling; no person in the shower (only a hand at the shelf edge — no nudity issues).
- **Audio map:** 0.0 shower running; 0.8 "plop" + drain gurgle; each week cut: shower stop/start + a different bird/morning sound (time passing); 4.0 soggy squelch; 9.5 dish clink as #4 is placed; 11.5 bed (warm upright bass, 84 bpm); 12.5 VO: "Six weeks. Still standing. GRANITE." 14.6 logo.
- **Models / template:** Kling 3.0 Pro i2v first/last for each weekly state (1–6, single locked frame = very stable); Cinema Studio for 7.
- **Est. cost:** stills 8 $2.40 + Kling 6 × 2 $5.76 + Cinema Studio $3.70 + VO → **≈ $12**.
- **Why best-3:** no people, no faces, no innuendo, no in-shot transformations (states change between cuts), a cheap and very AI-safe build, a product-caused punchline, and it re-skins for every scent drop (Season plan). The longevity claim needs the client's numbers.

### C9 · DRIFTWOOD (whole-body deodorant) — "The Sommelier" (20 s)
- **Idea:** an outdoor summer wedding at 34 °C. A deadpan sommelier walks the reception "tasting the air" around guests with a wine glass, writing notes. Most guests: "notes of… panic." Our man: he swirls, inhales, closes his eyes: "Cedar. Sea salt. Hint of linen."
- **Hook (0–1 s):** a sommelier swirls an **empty** wine glass under a sweating groomsman's armpit; super "Reception, 3:40 p.m., 34°C."
- **Punchline (product-caused):** the sommelier's notebook for our man reads "would wear again"; he discreetly swipes DRIFTWOOD from his jacket pocket on the dance floor.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–2.0 | Medium, Steadicam following | Empty glass swirled near a groomsman's arm (clothed) |
| 2 | 2.0–4.0 | Insert, locked | Notebook: "Notes of: panic" (post text) |
| 3 | 4.0–6.0 | Wide, tripod at the edge of the tent | Heat shimmer, guests fanning themselves |
| 4 | 6.0–8.5 | Medium two-shot | Sommelier reaches our man; swirls; long inhale; eyes close |
| 5 | 8.5–10.5 | Close on sommelier (mouth visible → Seedance dialogue) | {Cedar. Sea salt. A hint of linen.} |
| 6 | 10.5–12.5 | Insert | Notebook: "Would wear again" |
| 7 | 12.5–15.0 | Medium, dance floor | Our man swipes the stick under his collar line (clothed, quick, discreet) |
| 8 | 15.0–20.0 | Packshot on a linen table with a champagne flute, Cinema Studio | DRIFTWOOD; super "[72-h odour claim if tested]" |

- **Physics check:** 34 °C: heat shimmer above the lawn, damp collars, flutes sweating; the glass is always empty (no liquid level issue); application is over clothing edge or a quick wrist/neck swipe — no torso, no nudity; ≤ 3 people sharp per frame (doc 43).
- **Audio map:** 0.0 string quartet (diegetic) + crowd; 0.6 glass swirl "whoosh"; 2.0 pen scratch; 4.0 cicadas rise; 6.0 long inhale; 8.5 line; 10.5 pen scratch; 12.5 DJ drop (the quartet becomes a dance track); 15.5 VO: "Notes of you. Just better. DRIFTWOOD." 19.5 logo.
- **Models:** Seedance 2.5 r2v 15 s (1, 3, 4, 5, 7 with a dialogue block); Kling for 2, 6, 8 (notebook as a post overlay on a blank page).
- **Est. cost:** ≈ **$32**.
- **Claim check:** "odour protection" only with the client's test; no "stops sweat" unless it's an antiperspirant (OTC).

### C10 · HOLLOW OAK (beard oil) — "Velcro" (15 s)
- **Idea:** a winter hug. Every time his partner pulls away from his dry beard, her fleece makes a loud **Velcro rip** — at the station, at the door, at the couch. He applies HOLLOW OAK. Next hug: silence, then a soft "fwip".
- **Hook (0–1 s):** a station-platform hug; she pulls back; "RRRRIP" on a fleece collar; she freezes.
- **Punchline (product-caused):** the last hug is silent; she pulls back slowly, waiting for the rip that never comes, suspicious; he raises one eyebrow.
- **Built on:** doc 47 C7 "Sandpaper Handshake" (foley carries the result, no visual claim) and the Velcro sound as a pattern interrupt.

| # | t (s) | Shot (rig) | Action |
|---|---|---|---|
| 1 | 0.0–2.0 | Medium, tripod on the platform | Hug, pull-back, RRRIP |
| 2 | 2.0–3.5 | Close on her collar fleece | A few fleece fibres stand up (no beard close-up result) |
| 3 | 3.5–5.0 | Doorway, medium | Second hug, second RRRIP |
| 4 | 5.0–7.5 | Bathroom counter, macro, Kling | 3 drops of oil into his palm; amber, viscous ("each drop hangs 0.5 s") |
| 5 | 7.5–9.0 | Medium, mirror out of frame | He works it in (hands only, beard soft focus) |
| 6 | 9.0–12.0 | Couch, medium two-shot | Hug; she pulls away slowly — silence; a tiny "fwip" |
| 7 | 12.0–15.0 | Packshot on a wool blanket, Cinema Studio | Bottle + super "[softens the feel of your beard]" |

- **Physics check:** oil viscosity: drops hang 0.5 s then fall; 3 drops only (write the count); fleece fibres lift 2–3 mm on the rip; no before/after beard close-ups (AI stubble rule, §4); two people max.
- **Audio map:** 0.0 platform ambience + train hiss; 1.2 RRRIP (exaggerated Velcro); 2.0 a stunned beat; 3.5 door creak + RRRIP; 5.0 bathroom fan; 5.6 three drip ticks; 7.5 soft rub; 9.0 TV murmur; 10.5 near-silence + tiny "fwip"; 12.0 bed (lo-fi piano, 70 bpm); 12.5 VO: "Softer beard. Quieter hugs. HOLLOW OAK." 14.6 logo.
- **Models:** Seedance 2.5 r2v 15 s (1, 3, 6 + 2, 5 as cutaways); Kling for 4, 7.
- **Est. cost:** ≈ **$29**.

### 8.1 Ranking

| Concept | Sub-niche | Proof route | Policy risk | AI difficulty (1–5) | Est. spend |
|---|---|---|---|---|---|
| C1 Blade Count ★ | Razor | Real stroke slot + labelled CG | Low (generic comparison) | 3 | $27 |
| C2 Midnight, December 1 | Trimmer | Runtime claim (client) | Low | 3 | $29 |
| **C3 Balloon Test ★★ (best)** | Body trimmer | Real balloon pass slot | Very low | 2 | **$18** |
| C4 Floor 12 | Fragrance | Puffery / tested wear | Low | 3 | $32 |
| C5 Smells Like | Fragrance | Notes only | Very low | 1 | $7.50 |
| C6 Four Quarters | Oral (brush) | Timer feature | Low | 3 | $29 |
| C7 Gone Fishing | Oral (floss) | Client strength test or "Dramatization" | Medium | 4 (fish, line tension) | $29 |
| C8 Last Bar Standing ★ | Soap | Client longevity numbers | Low | 1 | $12 |
| C9 The Sommelier | Deodorant | Client odour test | Medium (body, claims) | 4 | $32 |
| C10 Velcro | Beard oil | Foley only (comedy) | Low | 3 | $29 |

**The single best concept: C3 "Balloon Test" (KEEL body trimmer).** Frame 0 is already tense motion; the punchline is a sound event caused by the product's guard; it needs no face, no nudity and no innuendo in a sub-niche famous for innuendo; the claim lives in the client's real 1.5 s slot; it cuts to a 6 s loop; and it re-skins for any shaver or trimmer client. Second: **C1 "Blade Count"** (the category's measured winning argument, made funny). Third: **C8 "Last Bar Standing"** (the cheapest, safest, Season-friendly template). For a VXO niche spec reel: **C3 + C1 + C5** (one trimmer, one razor, one fragrance), total ≈ $52.

---

## 9. Ten surprising insights nobody asked for (that would make VXO better)

1. **The real competitor is a brand's own $400 AI team, not another studio.** DSC's in-house team (Higgsfield + Claude) shipped its claimed best-ever campaign for $400 [c]. VXO's moat is the stuff they admit they got wrong ("some were executed better than others"): physics reads, QC (§2.3 shows half the category ships clipped or too-quiet audio), claims pre-flight and a deadpan comedy craft. **Put "physics-checked, QC-measured, claims-checked" on the site and in every DM.**
2. **Sell "hook heads", not whole films, to oral care.** Hismile's live Meta videos run 50–78 s; Spotlight's 20.4M post is a 37 s talking head; Supply's best is 59 s [m][v]. Those bodies are creator/expert footage the brand already owns. VXO's highest-value unit is a **3–5 s AI hook head + a 2–4 s mechanism insert** grafted onto their existing bodies — cheap to make (≈ $3–6), easy to test, endless re-buy. Price it as a pack inside the Season plan.
3. **"Made with AI. The proof is real." is a positioning line.** "Real" became an ad claim (Oars + Alps), and a practical ad got accused of AI (Quip). A studio that publicly separates **AI for the impossible** from **real for the proof** sidesteps the backlash instead of hiding from it.
4. **Mechanism CG is the cheapest high-value asset in the whole niche.** A hair cut under the skin, blade exposure in microns, a floss expanding between teeth, enamel layers: the top razor posts are built on such visuals (Supply's 3.31 % likes, Henson's 33M) and they cost brands animators. As still → Kling inserts they cost VXO under $1 each. Make a 6-insert "mechanism library" per spec niche.
5. **Body-hair creature comedy is a Super Bowl format at Short prices.** Manscaped pays MJZ/Can Can Club for hair puppets; DSC uses AI truck nuts. A $3M trimmer brand can't — but VXO can deliver a stylised, obviously-not-real creature (felt/fur puppet look) that sidesteps both the uncanny valley and the AI-slop accusation. Build one creature spec (not Otto/Vee) to show it.
6. **Women are the hidden audience of men's grooming creative.** Red-nailed hands sell Quip; a woman's sweat review sells Lume; women dermaplane with Leaf; gift buyers are often partners. Cast the hands and the second character as the buyer, and write gift-season hooks to her `[inf]`.
7. **Creative life sets the price more than production cost does.** Men's grooming creatives average 47 days, fragrance 18 days median (Benly). Quote grooming clients per launch (Premiere) and fragrance clients per month (Season) — and say why with the numbers.
8. **Shopify's `products.json` is a free lead-heat meter.** Launch velocity is visible for most stores (Dr. Squatch 17 SKUs in 60 days, Oakcha 47, Scotch Porter 6 in one day). Add it to every `vxo-leads` run (§7); it also tells you which product to put in the "5 free frames".
9. **Dec 1 is the niche's under-used Super Bowl.** No-Shave November trains men to wait; Dec 1 is the shave-off. Razor and trimmer brands go quiet in November (beard brands peak). A razor film that drops at 00:00 Dec 1 (C2) owns the date. Pitch it in October; the same logic applies to Father's Day in April.
10. **Otto's register already sells in this category — use it carefully.** Manscaped's paid "customer service rep" is a moustached deadpan at a desk (1.2M paid) and Dossier's layering lecture uses a stopwatch close-up (1.6M) [m]. Grooming buyers will read an Otto spec as "category-native" — but too close to Manscaped reads derivative. Make Otto's grooming spec a **procedure film** (C3's lab test, or a deadpan "blade count" briefing), not a talking rep.

---

## 10. Gaps and next steps (zero spend)
- **Meta run-length winners not confirmed.** The Ad Library returned 403 to our fetcher. Next run: open the library in a real browser session (built-in browser skill), search the 30 brands in §1.3, and log every ad active ≥ 60 days (Benly's 47-day grooming average is the bar).
- **YouTube spots** (Hair Ballad, DSC AI ads, Dr. Squatch × Sweeney) not measured; retry yt-dlp later or use the browser.
- **Revenue for most of the 30 brands is [unverified].** Fill per dossier only when a brand becomes a lead.
- **TheraBreath 7.6M explainer** failed to download (likely a photo/carousel post); not needed for the conclusions.

## Sources

**Measured (scratchpad only, not committed):** `scratchpad/niche2/grooming/` — `meta/meta_all.txt` (429 posts, 39 accounts, 2026-10-09), `an/*_stats.txt`, `*_tile.jpg`, `*_asr.txt`; store data in `shop/`. TikTok URLs are linked in §2.1.

**Market and data:** [NIQ men's grooming 2025](https://nielseniq.com/global/en/insights/report/2025/mens-grooming-market-surges-key-trends-you-need-to-know/) · [IMARC](https://imarcgroup.com/male-grooming-products-market-united-states) · [Benly Q1 2026 index](https://benly.ai/benchmarks/q1-2026) · [Benly B&PC](https://benly.ai/benchmarks/q1-2026/beauty-personal-care) · [Benly fragrance](https://benly.ai/benchmarks/q1-2026/beauty-personal-care/fragrance) · [Billo H1 2026](https://billo.app/blog/h1-2026-video-ad-benchmarks/) · [Circana/Happi Father's Day](https://www.happi.com/breaking-news/fragrance-sales-expected-to-exceed-230-million-for-fathers-day-2025/) · [Beauty Independent fragrance 2026](https://orbit.beautyindependent.com/article/what-next-fragrance-2026) · [SCMP/Bloomberg men's fragrance on TikTok](https://scmp.com/magazines/style/beauty/trends/article/3355775/tiktoks-fragrance-boom-why-gen-z-men-are-spending-us400-creed-cologne) · [eMarketer men's fragrance](https://www.emarketer.com/content/tiktok-social-change-gen-z-give-mens-fragrances-their-moment) · [MarketsandMarkets oral care](https://www.marketsandmarkets.com/Market-Reports/geography/oral-care-market/US) · [Mordor oral care](https://www.mordorintelligence.com/industry-reports/united-states-oral-care-market) · [Beauty Independent TikTok Shop Q2](https://www.beautyindependent.com/tiktok-shop-nears-1b-beauty-sales-second-straight-quarter/) · [Beauty Independent indie top 25](https://www.beautyindependent.com/indie-beauty-brands-surpassed-500-million-on-tiktok-shop-in-the-past-year/) · [Beauty Independent Viking Revolution](https://www.beautyindependent.com/?p=182167) · [FastMoss DR.DENT](https://www.fastmoss.com/blog/how-dr-dent-dominated-the-tiktok-shop-market-in-january-2026/) · [Nexscope wk 22](https://www.nexscope.ai/cases/40) · [Baijing/BrandArk Hismile](https://www.baijing.cn/article/55299) · [Sacra Dossier](https://sacra.com/c/dossier/) · [eightx Edgewell](https://eightx.co/blog/edgewell-teardown) · [ECDB Beardbrand](https://ecdb.com/resources/sample-data/retailer/beardbrand) · [Read the Peak, Henson](https://www.readthepeak.com/p/10-24-daniel-jantzi-on-scaling-henson-shaving) · [Freethink, Bite](https://www.freethink.com/series/ramen-profitable/toothpaste-tablets).

**Brands and campaigns:** [Marketing Dive, Dr. Squatch/Unilever](https://www.marketingdive.com/news/unilever-acquires-dr-squatch-valuing-brands-viral-marketing-to-gen-z-men/751304/) · [Campaign, Sweeney numbers](https://campaignlive.com/article/final-numbers-sydney-sweeneys-bathwater-campaign-dr-squatch/1937718) · [SDBJ, Manscaped](https://sdbj.com/retail/manscaped-grooms-growth-with-super-bowl-ad/) · [Reel Chicago, Hair Ballad](https://reelchicago.com/article/manscaped-makes-super-bowl-debut-with-singing-hairballs/) · [Ads of the World, Hair Ballad](https://www.adsoftheworld.com/campaigns/hair-ballad) · [Contagious, The Boys](https://www.contagious.com/news-and-views/campaign-of-the-week-grooming-brand-personifies-plums-to-prompt-men-to-preen-their-pubes) · [Retail Dive, DSC first AI ad](https://www.retaildive.com/news/dollar-shave-clubs-first-ai-generated-ad-makes-tech-the-punchline/808105/) · [Marketing Dive, DSC women's line](https://www.marketingdive.com/news/dollar-shave-club-swipes-at-competition-in-first-womens-grooming-push/816515/) · [Marketing Dive, DSC AI in-house](https://marketingdive.com/news/how-dollar-shave-club-uses-generative-ai-to-unlock-advertising-creativity/825016) · [Modern Retail, DSC when to use AI](https://www.modernretail.co/marketing/how-dollar-shave-club-decides-when-to-use-ai-generated-creative/) · [ContentGrip, DSC](https://www.contentgrip.com/dollar-shave-club-ai-ads/) · [Modern Retail, Quip not AI](https://www.modernretail.co/marketing/quips-latest-ad-wasnt-ai-generated-people-were-convinced-it-was/) · [Motion library: Manscaped](https://motionapp.com/library/manscaped), [Hismile](https://motionapp.com/library/hismile), [Dossier](https://motionapp.com/library/dossier) · [Atria: Hismile](https://tryatria.com/ads/meta/hismile-ads), [Dr. Squatch](https://tryatria.com/ads/meta/dr-squatch-ads), [men's grooming](https://tryatria.com/ads/meta/mens-grooming-ads).

**Policy and legal:** [Meta adult nudity & sexual activity (ads)](https://transparency.meta.com/policies/ad-standards/objectionable-content/adult-nudity-and-sexual-activity) · [TikTok adult content](https://ads.tiktok.com/help/article/tiktok-ads-policy-adult-content) · [NAD GuruNanda](https://bbbprograms.org/media/newsroom/decisions/gurunanda-enamel-safe) · [NAD Lumineux](https://bbbprograms.org/media-center/dd/oral-essentials-lumineux-mouthwash) · [NAD DR.DENT](https://bbbprograms.org/media/newsroom/decisions/drdent) · [CosmeticsDesign oral care NAD 2025 (Boka/NARB)](https://www.cosmeticsdesign.com/Article/2025/11/25/what-oral-care-stakeholders-can-learn-from-nads-2025-case-decisions) · [ASA Hismile ruling](https://www.asa.org.uk/rulings/hismile-pty-ltd-g23-1212696-hismile-pty-ltd.html) · [HBW, Native NAD](https://hbw.pharmaintelligence.informa.com/RS149550/NAD-Decision-Against-Native-Deodorant-AntiWetness-Claims-Holds-Up-On-Appeal) · [PMC, minoxidil advertising](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11105151/) · [Glossy, fragrance dupes](https://www.glossy.co/beauty/dupe-fragrance-has-hit-the-mainstream-now-what/) · [Dreyfus, perfume dupes](https://www.dreyfus.fr/en/2025/09/04/the-protection-of-olfactory-creations-how-to-combat-perfume-dupes/) · [McDermott, FTC v. Hims & Hers](https://www.mcdermottlaw.com/insights/ftc-two-states-take-aim-at-hims-hers-subscription-and-health-data-practices/) · doc 45 §5 (AI labels, NY law), doc 47 §4 (cosmetic vs drug, Meta/TikTok health rules).

**AI craft:** doc 43 (all model behaviour and prices), doc 41/44 (physics, comedy), doc 46 (QC), doc 47 §3 (mist, foam, glass, skin rows), doc 49 §3 (steam, state-between-cuts rule).
