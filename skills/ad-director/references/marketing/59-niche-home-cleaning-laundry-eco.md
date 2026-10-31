# 59 — Niche deep-dive: home cleaning, laundry and eco/refill products

Researched 2026-10-09. No generation money was spent. Nobody was contacted. Nothing was sent.

**What this adds.** No earlier doc covers cleaning. Doc 36 mentions Scrub Daddy as a character account, and doc 53 lists the Harry's × Scrub Daddy kit. Docs 51 (gadgets and home) and 56 (kitchen) cover appliances, cookware and drinkware, but not consumables. This doc adds:
- 26 cleaning, laundry and eco posts downloaded and measured, plus paid-ad structure from six Meta libraries (Motion) and metadata for 300+ posts from 32 brand and creator accounts;
- the market map: scale from SEC filings (P&G, Clorox, Grove), Grips online data for "eco-friendly cleaning", 30 brands with Shopify price and launch data, a seasonality calendar, and where they advertise;
- what converts here, with evidence;
- the realism traps specific to liquids, foam, tablets, sheets, stains, glass, mirrors and washing machines, with fixes tied to doc 43;
- the legal rules that bite in this niche: FTC Green Guides (16 CFR 260), EPA/FIFRA germ claims, CPSC recalls (The Laundress, Angry Orange, P&G pods, Clorox), NAD #7521 (P&G v. Blueland creator disclosures), and the "never make detergent look like food" rule;
- the buyer, re-buy triggers, a lead-scoring add-on and a sample DM;
- 10 concepts (3 marked best) and 10 insights.

It builds on 41 (action realism), 42 (teardown method), 43 (models, prices, templates), 44 (comedy craft), 45 (what sells, policy), 46 (sound and QC), 51 and 56 (home and kitchen), and the LESSONS file.

**Labels.**
- **[m]** = I measured it from the downloaded file: scene cuts with ffmpeg `select='gt(scene,0.3)'`, 2 fps frame tiles that I looked at, a 0.5 s RMS envelope with onset detection (librosa), integrated LUFS and sample peak (`ebur128`), and a faster-whisper transcript.
- **[c]** = the brand's own claim. **[v]** = a vendor or third-party figure (directional). **[inf]** = my inference. **[unverified]** = no primary evidence found in this run.

**Method and limits.**
- **TikTok.** I harvested recent and pinned video IDs from the public embed pages (`tiktok.com/embed/@handle`) of 80 candidate handles. 32 accounts returned IDs. Three of them (`earthbreeze_`, `angryorange`, `folex`) matched a brand name but turned out to be unrelated, so I dropped them, leaving 24 brand and 5 creator accounts. I pulled metadata for 336 posts, downloaded 26 to `scratchpad/niche2/cleaning/C01…C26/` (all 26 succeeded) and analysed them. No media is committed.
- **Paid vs organic.** As in docs 47–57: millions of views with a like rate under ~1 % is the paid-distribution signature (Spark Ads); ≥3 % is an organic hit. This is a flag, not a fact.
- **Meta.** The Meta Ad Library returned 403 to automated fetches (as in docs 51, 54 and 56), so run lengths of individual ads could not be read. **Motion's public library pages** are the proxy for Meta activity: Blueland, Grove Collaborative, Branch Basics, Earth Breeze, Purdy & Figg, Smol, Who Gives A Crap and Public Goods exist. They say "refreshed 4 months ago", so read them as a ~June 2026 snapshot. No Motion page exists for Dropps, Scrub Daddy, The Pink Stuff, Force of Nature, Laundry Sauce, Tru Earth, Truman's or Cleancult (all 404).
- **Search budget.** The shared web-search budget for this run was exhausted before I started, so every web source here was fetched directly from a known URL (SEC EDGAR, the CPSC recall API, Cornell LII for the CFR, BBB National Programs, Grips, Benly, Motion, Shopify `products.json`). Some facts I would normally confirm by search (state laws, funding, founders' revenue) are marked **[unverified]**. A follow-up run with search should close them; §11 lists them.
- **YouTube** was not used in this run (no IDs without search). The TikTok set plus the Motion libraries cover the paid and organic picture.
- **Two-year window.** Oct 2024 – Oct 2026. 19 of the 26 measured posts fall inside it. I kept 7 older ones (2022–2024) because they are pinned all-time winners or show a format that still runs, and each is marked "older".

---

## 0. The ten things to know before pitching a cleaning, laundry or eco brand

1. **This is a giant, flat category, and its challengers are shrinking online.** P&G's Fabric & Home Care segment sold **$30.3B in FY2026 (+2 %, unit volume unchanged)**, and P&G spent **$10.2B on advertising** company-wide ([P&G 10-K, Aug 2026](https://www.sec.gov/Archives/edgar/data/80424/000008042426000103/pg-20260630.htm)). Clorox: $6.7B, 84 % US ([10-K](https://www.sec.gov/Archives/edgar/data/21076/000002107626000034/0000021076-26-000034-index.htm)). Against that, Grips tracks **"eco-friendly cleaning" DTC sites (Branch Basics, Blueland, Dropps, Dr. Bronner's, Puracy) at $63M GMV in 2025, down 20–50 %**, with indexed revenue down 19 % from March to August 2026 ([Grips](https://gripsintelligence.com/insights/industries/home-garden/eco-friendly-cleaning)) [v]. Grove Collaborative's Q2 2026 revenue fell **17 % to $36.6M**, active DTC customers fell from 664K to 509K, and it cut advertising **55 %** ([Grove 10-Q](https://www.sec.gov/Archives/edgar/data/1841761/000184176126000064/grov-20260630.htm)). **Eco DTC is moving to retail shelves** (Blueland at Costco, Kroger and Meijer; Branch Basics "Now at Target" is its most-repeated 2026 headline [Motion]). VXO should sell *retail-launch* and *sale* films, not "DTC brand awareness".
2. **The paid volume is enormous and the ads are long.** Active Meta ads and new creatives per week: **Purdy & Figg 4,000 / ~134**; **Earth Breeze 471 / ~58**; Who Gives A Crap 439 / ~53; Smol 382 / ~46; Branch Basics 114 / ~8; Grove 74 / ~10; Public Goods 53 / ~10; Blueland 46 / ~11 [Motion, v]. Earth Breeze's video ads run **57 s to 1 min 57 s**; Smol's 15–63 s; Purdy & Figg 23–39 s; Blueland 15–38 s; Branch Basics 4–32 s [Motion storyline timestamps]. **"Demo" is the #1 tag nearly everywhere** (Smol 30 %, Branch Basics 23 %, Earth Breeze 22 %, Grove 17 %, WGAC 16 %, Blueland 13 %). A 15 s VXO film is rarely the whole ad here; it is the **hook and world** in front of a long demo/yapper body (LESSONS 53–54).
3. **The biggest posts sell a hack, not a product.** Grove's top two posts are a dish-towel bread wrap (**19.2M views**) and a vinegar shower-head soak (**8.6M**); both are paid (0.72 % and 0.22 % likes) and the product is almost incidental [m]. Nellie's best post (845K) is a fitted sheet that "ate" the dryer load, with **no product on screen** [m]. A creator janitor's "3 tips" has **13.3M** [m]. **In cleaning, the problem is the hook and the hack is the product.**
4. **Brand-owned TikTok accounts are almost dead, except one.** Median views of the latest posts: Blueland 1,152, Laundry Sauce 819, Method 554, Grove 403, Dropps 360, Branch Basics 348, Mrs. Meyer's 341, Force of Nature 218, Kind Laundry 160 [m]. **Scrub Daddy's median is 80,500**, with a 5.4M launch at 10.9 % likes and 64.8K shares [m]. The difference is a **product with a face** that acts as a character (doc 36), plus a community that asks for products in the comments.
5. **The legal fault line is "germs", "toxic" and "plastic-free".** "Kills 99.9 % of germs", "disinfects", "sanitizes" and "antibacterial" make a product a pesticide under FIFRA, which needs EPA registration ([40 CFR 152.15](https://www.law.cornell.edu/cfr/text/40/152.15)). A registered pesticide may **not** say "safe", "non-toxic" or "all natural" ([40 CFR 156.10(a)(5)](https://www.law.cornell.edu/cfr/text/40/156.10)). An unregistered eco cleaner may not say it kills germs. And "non-toxic" under the Green Guides means non-toxic to **humans and the environment** ([16 CFR 260.10](https://www.law.cornell.edu/cfr/text/16/260.10)). **An animated germ dying on a countertop is a pesticidal claim**, whoever drew it [inf].
6. **Contamination recalls hit the "clean" brands.** The Laundress recalled **~8 million** products for bacteria (Dec 2022); **Thrasio recalled ~1.5 million Angry Orange enzyme stain removers** for bacteria (Jan 2026); Clorox Puerto Rico recalled **6.3 million** cleaners (Sep 2026); P&G recalled **8.2 million** bags of laundry pods for child-resistant packaging failures (Apr 2024) ([CPSC recall API](https://www.saferproducts.gov/RestWebServices/Recall)). Never write "safe for babies", "safe around kids" or "pure" on screen without the client's evidence, and never show a child near pods or sprays (§5).
7. **P&G watches challengers' creators.** NAD Case #7521 (Nov 25, 2025): **P&G challenged Blueland's TikTok Shop creator posts** over disclosures. NAD accepted TikTok's automatic "creator earns commission" label for pure affiliates, but Blueland had to fix posts by creators it also paid ([BBB National Programs](https://bbbprograms.org/media/newsroom/decisions/blueland)). Any film VXO makes for creator seeding must carry its own disclosure plan.
8. **The eco audience is the most AI-sceptical audience VXO will meet.** Zero Waste Store's post "AI uses a significant amount of water and electricity…" has **8.5M views, 9.1 % likes and 141.8K shares**, the most-shared post in the whole set [m]. The only clearly AI-generated ad I found (Kind Laundry, "$300 for a bottle…", with the generator's sparkle watermark still in the corner) has **1,488 views** and is almost silent at **−44 LUFS** [m]. **For eco clients, AI must be invisible as AI**: no AI faces, objects and worlds only, real proof, and a short honest answer ready for "why AI?" (§6.2).
9. **Gross is the proof, and AI can't fake it.** Dirty mop water poured into a tub ("Repeat.", GoCleanCo, 373K) [m], "a rat in my washing machine" and "re-washing clothes that still smell damp" (Smol paid ads) [Motion], a clogged-drain "DNA test" (Scrub Daddy × Harry's, 18.1 % likes) [m]. The before/after is the claim (FTC demonstration rules, doc 51 §4). **The proof slot is always real footage**. AI builds the comedic world *around* the gross reveal and never shows the dirt leaving.
10. **The category ships broken audio.** 15 of 26 measured posts sit below −24 LUFS (Kind's AI ad at −44, Dropps −33.9, Puracy −30.7/−30.2), and 6 peak at or above −0.5 dBFS (GoCleanCo **+2.6**, Scrub Baby launch +0.7, The Laundress +0.4, Blueland +0.2) [m]. Doc 46's master (−14 LUFS, ≤ −1 dBTP) is a concrete, checkable improvement to offer, as in kitchen (doc 56).

---

## 1. Market map

### 1.1 Size and growth

| Measure | Figure | Source | Note |
|---|---|---|---|
| P&G Fabric & Home Care (global) | **$30.3B FY2026, +2 %; organic +1 %; unit volume unchanged** | [P&G 10-K](https://www.sec.gov/Archives/edgar/data/80424/000008042426000103/pg-20260630.htm) | Tide, Gain, Downy, Dawn, Cascade, Mr. Clean, Swiffer, Febreze. 35 % of P&G sales |
| P&G advertising (all segments) | **$10.2B FY2026** ($9.2B FY2025) | same | The incumbent's war chest |
| Clorox total | **$6.7B FY2026; 84 % US** | [Clorox 10-K](https://www.sec.gov/Archives/edgar/data/21076/000002107626000034/0000021076-26-000034-index.htm) | "US markets… mature… high household penetration" |
| Church & Dwight | Laundry detergents are its **largest consumer business** by net sales (Arm & Hammer, OxiClean); consumers "increasingly seeking lower cost private label" | [C&D 10-K](https://www.sec.gov/Archives/edgar/data/313927/000119312526048139/0001193125-26-048139-index.htm) | Value pressure |
| Eco-friendly cleaning, online (Grips, 50+ tracked sites) | **$63M GMV 2025, down 20–50 %**; 2026 forecast −0–5 %; conv. **2.0–2.5 %**; AOV $0–100; 58 % desktop | [Grips](https://gripsintelligence.com/insights/industries/home-garden/eco-friendly-cleaning) | [v] tracked DTC sites only, not retail |
| Eco-friendly household, online (40+ sites) | **$56M 2025, down 5–10 %**; 2026 forecast +0–5 %; conv. **3.0–3.5 %** | [Grips](https://gripsintelligence.com/insights/industries/home-garden/eco-friendly-household) | [v] |
| Home & Garden, online | conv. 2.5–3.0 %, AOV $100–200 (Aug 2026) | [Grips](https://gripsintelligence.com/insights/industries/home-garden) | [v] |
| Grove Collaborative (public, eco marketplace + own brands) | Q2 2026 revenue **$36.6M (−17 %)**; DTC active customers **509K vs 664K**; net revenue per order **$69.19**; advertising **−55 %** | [Grove 10-Q](https://www.sec.gov/Archives/edgar/data/1841761/000184176126000064/grov-20260630.htm) | "Active Customers declined primarily due to our lower advertising spend" |
| US household cleaning, total retail | ≈ $35–45B; laundry care the largest slice | — | **[unverified]**: no primary source fetched in this run |

**Read [inf]:** the category is huge, mature and value-squeezed. The eco/refill wave of 2019–2022 (tablets, sheets, refill concentrates) is now consolidating. The winners are going to retail (Target, Costco, Walmart, Kroger), the DTC-only players are cutting ad spend, and the survivors run very high-volume, offer-led Meta programmes. **That is good for VXO:** retail launches, new SKUs and constant offers each need a fresh hook, and an AI world is the cheapest way to make a $5 product look like a brand.

### 1.2 The 30 brands (founder-led and $1–20M marked)

Revenue bands are third-party or my estimates **[unverified]** unless sourced. "Shopify" = live `products.json` on 2026-10-09: product count, median price, newest product date, products created in the last 60 days. "TT median" = median views of the latest posts [m].

| # | Brand | Sub-niche | Founder-led? | Size band | Shopify (n · median $ · newest · new in 60 d) | Ads seen | Fit |
|---|---|---|---|---|---|---|---|
| 1 | **Dropps** | Laundry + dish pods, cardboard packs | Yes [unverified] | $10–30M | 32 · $34 · **2026-10-01 · 31 new** (full range relisted: Year Supply, Starter, Travel & Trial) | TT median 360 | ★ relaunch now |
| 2 | **Earth Breeze** | Laundry sheets → dish tablets, pet detergent, stain spray | Yes [unverified] | $20–60M | 37 · $36 · 09-24 · 6 new (Pet Laundry 9/9, Miracle Stain Remover 9/24) | **Meta 471 active, ~58/wk**; 57–117 s demos | ★ category extension |
| 3 | **Tru Earth** | Laundry strips, refills (Vancouver) | Yes [unverified] | $10–50M | 44 · $20 · 08-26 · **11 new** (Year boxes, bundles) | Meta, Amazon | ★ |
| 4 | **Branch Basics** | Concentrate refill system, "human-safe" | Yes (co-founders Allison Evans, Kelly Love, Marilee Nelson on its TikTok) | $10–30M | 104 · $0 (free samples) · 09-25 · 2 new | **Meta 114, "Now at Target"**; TT 348 | ★ retail launch |
| 5 | **Blueland** | Tablets + forever bottles, laundry, dish | Yes (Sarah Paiji Yoo, CEO) [unverified] | $20–60M | 80 · $18 · 09-18 · 5 new (PowerDuo, Coast hand soap) | **Meta 46; retail coupons (Costco, Kroger, Meijer)**; TT 1,152 | ★ launch (PowerDuo) |
| 6 | **Puracy** | Plant-based soaps, stain remover (Austin) | Yes [unverified] | $5–20M | 46 · $18 · 09-25 · 2 new | TT paid hits (788K, 382K) | ★ |
| 7 | **Defunkify** | Sports/odour laundry | Yes [unverified] | $1–10M | 11 · $29 · 09-03 · 1 new | TT 329 | ★ C3 fit |
| 8 | **Dirty Labs** | Bio-enzymatic laundry, dish | Yes [unverified] | $1–10M | 29 · $20 · 05-18 · 0 | — | No new SKU since May |
| 9 | **Kind Laundry** | Scented laundry sheets ("perfume-inspired") | Yes [unverified] | $1–10M | 65 · $22 · 05-31 · 0 | TT 160; **AI ad (1.5K)**; celebrity-footage meme | ★ needs better creative; claims risk |
| 10 | **Laundry Sauce** | Luxury-scent detergent | Yes [unverified] | $10–30M | 27 · $37 · 07-29 · 0 | Motion "trending home goods" #21 | ★ C2 fit |
| 11 | **Sheets Laundry Club** | Laundry sheets | Yes [unverified] | $5–20M | (404) | TT 196 median; 6.5M pinned (2022) | Fading |
| 12 | **Force of Nature** | Electrolysed-water appliance, **EPA-registered** disinfectant | Yes [unverified] | $10–30M | (404) | TT 218 | Germ claims allowed, "non-toxic" not (§5) |
| 13 | **Truly Free** | "Non-toxic" laundry, home | Yes [unverified] | $10–30M | (404) | TT 434 | Fear-led copy = risk |
| 14 | **Molly's Suds** | Laundry powder | Yes [unverified] | $1–10M | 43 · $14 · 2025-08 · 0 | — | Quiet |
| 15 | **Nellie's** | Laundry soda, dryer balls (Canada) | Yes [unverified] | $5–20M | 48 · $18 · 2025-09 · 0 | TT 817; 845K "fitted sheet" | ★ problem-hook brand |
| 16 | **Woolzies** | Wool dryer balls, candles | Yes [unverified] | $1–10M | 250 · $20 · 10-06 · **75 new** (holiday candles) | — | ★ Q4 drops |
| 17 | **ecoegg** | Laundry egg (UK, US) | Yes | $1–10M | 18 · $6 · 09-24 · 2 new | — | |
| 18 | **Etee** | Enzyme laundry, wraps (Toronto) | Yes | $1–10M | 88 · $20 · 10-08 · 2 new | — | |
| 19 | **Jaws** | Refill pods for spray bottles | Yes [unverified] | $1–10M | 86 · $10 · 09-28 · 2 new (Stock-Up bundles) | — | ★ BFCM bundles |
| 20 | **Koala Eco** | Plant-based cleaners (Australia, US) | Yes | $5–20M | 83 · $24 · 10-07 · **8 new** | TT paid 1.6M, 616K | ★ |
| 21 | **Murchison-Hume** | Cleaners (Australia/US) | Yes | $1–10M | (404) | TT 830 | |
| 22 | **Plaine Products** | Refill aluminium bottles (personal + home) | Yes | $1–10M | 81 · $24 · 09-03 · 8 new | — | Refill-model reference |
| 23 | **Homecourt** | Premium home care (Courteney Cox) | Celebrity-founded | $10–30M | 48 · $42 · **10-08** · 2 new (gift box, tray) | — | Gifting Q4 |
| 24 | **Public Goods** | Household + personal care | Yes | $20–60M | 160 · $20 · 08-16 · 2 new | Meta 53 (80 % image) | |
| 25 | **Scrub Daddy** | Sponges, Pink Stuff-type paste, Scrub Baby | Yes (Aaron Krause) | $100M+ [unverified] | (404) | **TT median 80,500**; Walmart exclusive launch | Reference: character brand |
| 26 | **Grove Collaborative** | Eco marketplace + Grove Co. | Public company | $150M/yr run-rate | — | Meta 74; TT paid hacks 19.2M, 8.6M | Reference |
| 27 | **Purdy & Figg** | Refill cleaning (Australia) | Yes | $10–50M [unverified] | — | **Meta 4K active, ~134/wk**; "Starter Kit 65–70 % off" | Volume reference |
| 28 | **Smol** | Tablets/capsules (UK) | Yes | $50M+ [unverified] | — | Meta 382, ~46/wk; myths, street interviews | Format reference |
| 29 | **The Laundress** (Unilever) | Premium laundry | No | — | 64 · $26 · 08-11 | TT 720; 2022 recall | Reference |
| 30 | **Method / Mrs. Meyer's / Seventh Generation / Angry Orange (Thrasio)** | Mass "green" | No (SC Johnson, Unilever, Thrasio) | large | — | TT 341–554 | Reference only |

**The VXO target band** is rows 1–24: founder-led, $1–30M, selling a physical change you can dramatise (a tablet that fizzes, a sheet that dissolves, a smell, a stain, a shine). Rows 25–30 are format references and occasional "test line item" buyers.

### 1.3 Price bands (what the buyer is selling)

| Band | Typical products | Ad implication [inf] |
|---|---|---|
| $5–15 | Single refill tablets, sponges, sample packs (Blueland $1 samples, Branch Basics free samples, Scrub Daddy) | Trial offers ("try for $3", "9 free tablets"); TikTok Shop; 6–15 s loops |
| $18–40 | Starter kits, 60–120-load packs (median prices: Blueland $18, Puracy $18, Tru Earth $20, Kind $22, Earth Breeze $36, Dropps $34, Laundry Sauce $37) | The core Meta DR band; subscription upsell; the 15 s hook + demo body format |
| $60–200 | Year supplies and bundles (Dropps Year Supply, Tru Earth "Box for a Year", Earth Breeze $79.80 offers, Branch Basics Ultimate Kit $190) | BFCM and New Year; "price per load" maths on screen |
| $200+ | Appliances (Force of Nature), gift boxes (Homecourt) | Gifting films; Premiere tier |

AOV runs **$0–100** for eco cleaning (Grips) and $69 per Grove order. **A $1,200 Short is about 20–35 first orders at typical AOV**. Pitch the film on subscription lifetime value, not first-order ROAS [inf].

### 1.4 Seasonality calendar

Evidence is from the brands' own 2026 ad copy (Motion) and posts [m]; the shape is [inf].

| Month | Moment | Evidence | When the film must be live → when to pitch |
|---|---|---|---|
| **Jan** | **"New Year reset / detox your home"** | Branch Basics "Clean Slate, Clean Home… perfect time to detox your home" (New Year ad) [Motion] | Live Dec 26 → **pitch late Nov** |
| **Feb–Apr** | **Spring cleaning (the category peak)**; allergy season | Purdy & Figg "Spring Complete Starter Kit 70 % off", "Spring Cleaning Kit"; Puracy "spring cleaning tip" (788K); Grove "Get ahead of allergy season" [Motion, m]; Grips index **−19 % Mar→Aug** (spring high, summer low) | Live Feb 15 → **pitch early Jan** |
| Apr 22 | **Earth Day** (eco brands' brand moment) | [inf] | Pitch early Mar |
| May–Aug | Moving season, "new home, new habits" | Smol "new home new habits" [Motion] | Pitch Apr |
| **Jul** | **Plastic Free July**; Prime Day | Amazon-heavy brands [inf] | Pitch late May |
| **Aug–Sep** | **Back to school / dorms** | #CloroxPartner back-to-school (4.9K) [m]; Kind "Moved into residence…" [m]; Smol school-uniform stain ad [Motion] | Live Aug 1 → pitch June |
| **Sep–Oct** | **Cold and flu**; fall scents; Halloween | Grove "Get ahead of cold & flu season" [Motion]; Scrub Daddy "PUMPKIN SPICE SZN" (9/13); GoCleanCo "Fall Cleaning Challenge" [m] | Pitch Aug |
| **Nov** | **Holiday hosting + BFCM** (year-supply bundles) | Grove's 19.2M dish-towel "hostess icon" post (Nov 8) [m]; Jaws "Stock-Up Value Bundle" (9/28) and Dropps "Year Supply" (10/1) listed just before Q4 [Shopify] | Live Nov 1 → **pitch now (early Oct)** |
| Dec | Gifting (Homecourt gift box 10/6; Woolzies 75 holiday SKUs); limited editions (WGAC "Splash Edition… not for long") | [Shopify, Motion] | Pitch Oct |

**Today (2026-10-09):** the last useful week for BFCM/hosting work, and the right time to pitch **January "reset"** films. That is the strongest window in this niche, because January plus spring is when people actually restock cleaning products.

### 1.5 Where they advertise

- **Meta (everyone):** very high-volume libraries. **Images still dominate** for most: Blueland 14 of its 20 newest ads are images, Grove 14/20, Branch Basics 14/20, Public Goods 16/20, Purdy & Figg 13/20. Video leads only at Smol (15/20), WGAC (17/20) and Earth Breeze (12/19) [Motion]. Hooks are offer-first ("JUST $79.80", "WE'RE SO SORRY.", "Get our Starter Kit for 65 % off", "GET 9 FREE ROLLS"), retail ("Now at Target", "$5 off at Costco") or fear-led ("No Hormone Disruptors", "WHY WOMEN NEED PLASTIC FREE DISHWASHER TABLETS").
- **TikTok:** creators and Spark Ads carry the reach. Grove's paid hacks reach 1.6–19.2M; Koala Eco 0.6–1.6M; Puracy 0.4–0.8M [m]. TikTok Shop affiliates matter enough that P&G challenged Blueland's (NAD #7521).
- **CleanTok creators as media:** Clean That Up (median 17.9K, a 13.3M pin), GoCleanCo (7.1K), The Home Edit [m]. Sponsored posts underperform: Clean That Up's #CloroxPartner post got **4.9K vs her 17.9K median (0.27×)** [m].
- **Retail media:** Costco, Kroger, Meijer coupons (Blueland); Target (Branch Basics, Grove); Walmart exclusives (Scrub Baby, Clorox via creator links) [Motion, m].
- **Amazon:** price-per-load comparisons; Thrasio-type roll-ups (Angry Orange).

---

## 2. Teardowns: 26 measured posts plus Meta library structure

Cut rate = shots ÷ duration. Hook = what is on screen and in the audio in second 1. LUFS / peak are as published (TikTok re-encode). Like rate = likes ÷ views; share rate = shares ÷ views.

### 2.1 The 18 strongest, full teardown [m]

| # | Post | Date · views · likes · shares | Length · shots · shots/s · LUFS / peak | Shot list (timecodes) | Second 1 (hook) | Turn / punchline | Product interaction | Sound | Text / CTA | Why it sold |
|---|---|---|---|---|---|---|---|---|---|---|
| C01 | **Grove "a fold so simple"** ([link](https://www.tiktok.com/@grovecollaborative/video/7570180680521370911)) | 2025-11-08 · **19.2M** · 0.72 % (paid) · 11.8K | 13.0 s · 3 · 0.23 · −26.8 / −12.3 | 0–0.9 hands lift a loaf wrapped in a striped dish towel over a set holiday table (payoff); 0.9–5.7 overhead: the towel laid flat, folded in thirds; 5.7–13.0 corners tucked, loaf placed, bundle tied, lifted | **The finished gift-wrapped loaf** + super "Your dish towel's secretly a hostess icon. Save for later!" | The towel becomes a bread basket | The towel *is* the product (Grove Co. textiles); hands only | Quiet room sound, 1.1 onsets/s | Save bait; caption "never reach for a basket again" | **Payoff-first hack + save bait + hosting season.** The product is shown being *useful*, not advertised. Biggest post in the niche |
| C02 | **Grove × Aunt Fannie's shower-head soak** ([link](https://www.tiktok.com/@grovecollaborative/video/7602805182732193055)) | 2026-02-04 · **8.6M** · 0.22 % (paid) · 1.0K | 10.9 s · 4 · 0.37 · −26.7 / −13.4 | 0–2.2 man reaches up to a rain shower head; 2.2–5.1 vinegar cleaner poured into a zip bag; 5.1–9.9 bag strapped over the hand shower; 9.9–10.9 the bag hangs in the stall | Hands on a crusted shower head + super "You're not still using harsh chemicals on your shower head… right? Watch this." | The soak setup (the result is promised, not shown) | Pour + bag (real) | Licensed pop (RAYE) | Super only | **A "reminder" hook ("this is your reminder to…") is a guilt trigger.** Note it never shows the result, so no demonstration claim is made |
| C03 | **Grove "stainless steel means stuck eggs" myth** ([link](https://www.tiktok.com/@grovecollaborative/video/7575308052732103967)) | 2025-11-21 · 1.6M · 0.73 % (paid) · 826 | 13.6 s · 13 · 0.95 · −26.1 / −11.5 | 0–2.2 eggs poured into a pan (payoff); 2.2–4.5 burner on, egg cracked; 4.5–8.6 water-bead test, droplets dance; 8.6–11.8 oil shimmer, eggs slide; 11.8–13.6 eggs on a plate | Eggs already in the pan | The water-bead test (science) | Real cooking | Music | Long supers ("You're thinking: stainless steel is a trap…") | **Myth-bust with a visible physical test.** Shows a marketplace selling *knowledge* |
| C04 | **Scrub Daddy "Scrub Baby is here"** ([link](https://www.tiktok.com/@scrubdaddy/video/7688381219578334494)) | 2026-09-22 · **5.4M** · **10.9 %** · **64.8K (1.2 %)** | 41.8 s · 7 · 0.17 · **−13.3 / +0.7** (clips) | 0–3.3 social-team host at the sink, to camera; 3.3–13 the blister pack, close; 13–19 brush pushed into a green bottle, scrubbing; 19–24 brush end on a "Scrub Daddy" plush; 24–30.6 the nipple-cleaner tip, macro; 30.6–41.8 static pack + bottle, VO to the end | Host mid-sentence: "I don't care what you call it…" | "Stop with the 'where's the baby bottle brush' comments… it's here" | Real demo of each feature | Talking, captions | "Available exclusively at Walmart" | **The community asked for it in the comments, and the launch answers them.** A 7-day teaser (C05) primed it |
| C05 | **Scrub Daddy bottle teaser** ([link](https://www.tiktok.com/@scrubdaddy/video/7685776639694818591)) | 2026-09-15 · **3.2M** · 8.2 % · **45.6K (1.4 %)** | 16.8 s · 2 · 0.12 · −17.4 / −1.9 | 0–14.0 overhead locked-off: a sink full of baby bottles in suds, two hands scrub with a pink smiley sponge, bottle after bottle; 14.0–16.8 mint card, a baby-faced sponge logo | A sink *full* of bottles (abundance) | The baby logo card = "something is coming" | Real scrubbing | Music | Caption "Wish we had a product made specifically for that… 👀" | **A teaser with the product hidden earns a higher share rate than the launch.** Loopable overhead |
| C06 | **Zero Waste Store "stop buying"** ([link](https://www.tiktok.com/@zerowastestore/video/7505154729194868010)) | 2025-05-16 · **11.3M** · **15.0 %** · 53.8K | 9.6 s · ~5 (stock clips under fixed letterbox text; the detector saw 0) · −14.3 / −6.0 | Black frame with two lines of white text; under it, landfill aerials, a polluted river, confetti trash, a garbage truck tipping | "Everything you have ever bought still exists on the Earth today." | "The Earth cannot sustain this rate of overconsumption." | None | Trending track | Text only | **Pure values statement, stock footage, 10 s.** The eco audience shares guilt-free *anti-consumption*, so ads must look like the opposite of hype |
| C07 | **Zero Waste Store "10 things I won't be buying in 2026"** ([link](https://www.tiktok.com/@zerowastestore/video/7586850472162577694)) | 2025-12-27 · 739K · 6.9 % · 1.2K | 46.9 s · 23 · 0.49 · −28.4 / −5.2 | 10 swaps at ~4 s each: paper towels → reusable roll; bottle dish soap → bar; plastic wrap → beeswax; **Tide pods → laundry sheets**; loofah, shampoo, dryer sheets → wool balls, floss, brush, toothpaste tablets | "10 things I won't be buying in 2026" | The list itself | Each swap held up | VO, no music bed | — | **The New Year swap listicle.** Every eco refill brand fits a slot: buy a slot, not a film |
| C08 | **Koala Eco "if I am to put you on anything"** ([link](https://www.tiktok.com/@koalaeco/video/7403072446711991582)) | 2024-08-14 (older) · 1.6M · 0.16 % (paid) · 128 | 5.7 s · 4 · 0.70 · −29.5 / −12.1 | 0–1.5 flat lay of four bottles; 1.5–3.1 a hand pumps hand wash; 3.1–4.2 two bottles on a wooden riser, window light; 4.2–5.7 high angle on two sprays, hard shadow | Product line-up | "The best smelling natural, non-toxic cleaning products" | Pump press | Creator voice "10 out of 10" | Super | **A 5.7 s recommendation loop.** "Non-toxic" super = claim risk (§5) |
| C09 | **Koala Eco refill ritual** ([link](https://www.tiktok.com/@koalaeco/video/7465847039147003182)) | 2025-01-30 · 616K · 0.22 % (paid) · 42 | 10.4 s · 3 · 0.29 · −15.9 / −0.1 | 0–2 a refill pours into a green glass bottle, close; 2–4.5 mother and daughter at a table with eucalyptus, the **child sprays**; 4.5–10.4 wide pantry, mother and child, logo | The pour | — | Refill pour (the system) | Music | "Safe, powerful & plant-based. Made with Australian essential oils" | **The refill pour is the ritual shot of the category.** A child using a spray in an ad is a safety and claims risk VXO must not copy (§5) |
| C10 | **Nellie's "fitted sheet ate everything"** ([link](https://www.tiktok.com/@nelliesclean/video/7492132499535990071)) | 2025-04-11 · 845K · 1.7 % · **4.5K (0.54 %)** | 6.3 s · 1 · 0.16 · −30.5 / −13.3 | One locked-off tripod shot in the laundry nook: she yanks a balled fitted sheet from the dryer, drops it, pulls it open; damp items spill out | Motion already happening + super "POV: it's 8pm and nothing has dried because your fitted sheet has eaten everything and created a giant ball" | The reveal of what's inside the ball | **None** | Room sound only | POV super | **A universal, unspoken laundry pain in 6 s.** Problem-only posts get shared ("this is me") |
| C11 | **Puracy oven-door "spring cleaning tip"** ([link](https://www.tiktok.com/@puracy/video/7358164751899233569)) | 2024-04-15 (older) · 788K · 0.56 % (paid) · 53 | 30.4 s · 5 · 0.16 · −30.7 / −15.2 | 0–1.7 dish soap squeezed onto greasy oven glass; 1.7–10.8 the grease close, paper towel; 10.8–26.6 bottle to lens, then wiping; 26.6–30.4 "Before" / "After" | Product already squeezing onto grease + super "The spring cleaning tip for the oven I wish I knew sooner" | The before/after | Real wipe | Creator VO "I hate using oven cleaner" | Before/After supers | **"Off-label" use: the dish soap cleans the oven.** One product, a new job, a seasonal tip |
| C12 | **Puracy stain remover meme** ([link](https://www.tiktok.com/@puracy/video/7362239956279954720)) | 2024-04-26 (older) · 382K · 0.19 % (paid) · 22 | 6.7 s · 3 · 0.45 · −30.2 / −17.3 | 0–1.6 a stained white sheet, super "You just used soap & water for your stain?"; 1.6–4.4 bottle to lens, spray; 4.4–6.7 the clean sheet, "after" | A visible stain | **Jump cut from stain to clean** | Spray (real) | Trending dialogue clip ("You look older… that's not a compliment") | "Try this instead!" | **A 6.7 s proof loop.** Note the jump cut hides the wash, which is exactly what the FTC calls a demonstration (§5). Real footage only |
| C13 | **Sheets Laundry Club ice-cube dryer hack** ([link](https://www.tiktok.com/@sheetslaundryclub/video/7180215418735381802)) | 2022-12-23 (older, pinned) · **6.5M** · 3.5 % · **39.4K (0.61 %)** | 6.3 s · 1 · 0.16 · −18.7 / −4.8 | One locked-off shot: she drops two ice cubes into a dryer of clothes, shuts it | Ice cubes in hand + super "When you discover the laundry hack that you can steam your clothes by throwing a couple ice cubes in the dryer on high for 10 minutes" | The hack itself | **None** | Trending "Taylor's Version" sound | Super only | **A hack with no product earns 33,000× the account median.** The brand is the source of the trick, not its subject |
| C17 | **Scrub Daddy × Harry's "Mr. Mitt" drain-hair DNA show** ([link](https://www.tiktok.com/@scrubdaddy/video/7691405716816563487)) | 2026-09-30 · 168K · **18.1 %** · **3.2K (1.9 %)** | 144.9 s · 53 · 0.37 · −23.9 / −6.0 | A daytime-talk-show parody set: two roommates on a couch; a clump of drain hair in an evidence bag; the mother "defends her son's honour"; a lab tech with the "DNA results"; reveal: "a synthetic third" (the mitt); crowd sign "HAIR CLOG CONSPIRACY"; brawl; logo bumpers | Host: "this biohazard was pulled directly from Pete and Marco's shared apartment drain" | "You are not the clog… the hair came from a synthetic third" | The mitt as the culprit | Dialogue, audience | "Get your own Mr. Mitt" | **Highest like and share rates in the set.** A gross household fight told as a TV format. 145 s is organic, not paid |
| C18 | **Bar Keepers Friend × creator copper sink** ([link](https://www.tiktok.com/@barkeepersfriend/video/7683242744302603533)) | 2026-09-08 · 32K · 1.0 % · 18 | 56.2 s · 2 · 0.04 · −27.1 / −14.1 | One handheld high-angle take: powder swirled onto a dark, tarnished copper sink; paste scrubbed with coloured sponges; rinse; 54.5–56.2 the shining pink-copper basin, close | Powder already drizzling onto a black sink | The colour change from black-brown to pink copper | Real scrub (proof) | Room sound | Caption | **Satisfying transformation as one long take.** A colour change you can't fake is the trust signal |
| C23 | **Clean That Up "3 quick cleaning tips from a janitor"** ([link](https://www.tiktok.com/@cleanthatup/video/7117377265054256426)) | 2022-07-06 (older, pinned) · **13.3M** · **10.5 %** · 27.5K | 17.6 s · 6 · 0.34 · **−12.6 / −0.8** | 0–1.6 he introduces himself at lens; 1.6–4.4 baking soda + peroxide grout paste; 4.4–7.3 pillowcase over a fan blade; 7.3–11.3 iron steam on a carpet dent; 11.3–17.6 fork grooming | "Hey I'm Brandon and I'm a janitor" (authority in 2 s) | The fork trick | Household items | Clean VO, well mastered | — | **Authority + three tips in 17 s.** The highest-performing creator format in the niche |
| C24 | **Clean That Up broom-towel baseboard hack** ([link](https://www.tiktok.com/@cleanthatup/video/7691804360128351519)) | 2026-10-01 · 333K · 2.4 % · 1.2K | 17.4 s · 1 · 0.06 · −30.0 / −14.6 | One take: towel over a broom head, rubber band, wiping baseboards standing up | "If cleaning your baseboards is hurting your back…" | Standing up | Household items | VO | — | **Pain → simpler way.** 19× her median, with zero product |
| C26 | **GoCleanCo "Tide or die" mop water** ([link](https://www.tiktok.com/@gocleanco/video/7055339226589662470)) | 2022-01-20 (older) · 373K · 4.0 % · 905 | 21.9 s · 13 · 0.59 · −11.5 / **+2.6** (clips) | 0–1.5 hot water into a red spin bucket; 1.5–4.8 a teaspoon of powdered detergent; 4.8–8 mop wrung; 8–10 mopping wood; 10–22 **the grey-brown water poured into a white tub**, super "Repeat." ×5, alternating with mopping | Water roaring into the bucket + super "Floor recipe: 1 gallon hot water, 1 teaspoon powdered Tide" | **The dirty water in the white tub** | Real use | Licensed song "Hard Work" | "Repeat." | **The gross reveal is the proof.** Every pour gets darker → lighter. A real-only shot |
| C16 | **Blueland PowerDuo launch, "reporting live from the lab"** ([link](https://www.tiktok.com/@blueland/video/7673921667567013133)) | 2026-08-14 · 1.8K · 2.0 % · 8 | 47.3 s · 38 · 0.80 · −17.8 / **+0.2** | 0–2.6 the Chief Innovation Officer in a lab coat holds the pack; 2.6–11 laundry-room B-roll; 11–19 two-layer tablet, macro; 19–28 stains, enzymes, a sweaty-shirt sniff; 28–36 a white suit splattered with mud; 36–44 the lab, a tablet press "tested over 100 formulas"; 44–47.3 back to him | "It's finally here, our PowerDuo tablets" | "3+ years, over 100 formulas" | Many inserts | VO, captions; peak clips | — | **The right content (an R&D proof) at the wrong length on the wrong channel.** It belongs as a 15 s hook + 30 s body on Meta |

### 2.2 The other 8 measured posts [m]

| # | Post | Views · like rate | Length · shots · LUFS | What it shows | Lesson |
|---|---|---|---|---|---|
| C14 | Kind Laundry "Olivia should've used Kind Laundry Detergent Sheets…" ([link](https://www.tiktok.com/@kindlaundry/video/7690663162898566413)) | 5.3K · 0.75 % | 9.3 s · 2 · −12.5 / 0.0 | Concert footage of a singer's dress disintegrating in stage rain; caption says competitor sheets dissolve "clumpy, messy" in cold water | **Unlicensed celebrity footage + an implied comparative claim.** Low reach, double legal risk |
| C15 | Dropps "I'll just put something on while I clean / the something:" ([link](https://www.tiktok.com/@dropps/video/7693266749176777997)) | 2.2K · 9.5 % | 18.5 s · 1 · −33.9 / −23.5 | Woman from behind, vacuuming, the VMAs on the TV | Relatable, but a TV broadcast on screen is someone else's IP |
| C19 | Method "bfs this is the correct amount of body wash to use" ([link](https://www.tiktok.com/@methodproducts/video/7676530686089530637)) | 11.9K · 1.7 % | 7.0 s · 1 · −15.8 / −5.3 | Absurd over-pour on a sea sponge in a shower | **Over-use as a gag** works for consumables (tag-a-friend) |
| C20 | Blueland "5 unexpected ways plastic may end up on your plate" ([link](https://www.tiktok.com/@blueland/video/7685516084274875679)) | 2.0K · 2.0 % | 13.4 s · 12 · −27.3 / −9.1 | Recycling plant → black spatula → **a detergent pod torn open "containing copolymer of acrylic"** → sponge → cutting board → takeout | Fear education with an implied rival claim. Low reach |
| C21 | **Kind Laundry "$300 perfume vs Kind Laundry" — AI-generated** ([link](https://www.tiktok.com/@kindlaundry/video/7644684553629617422)) | 1.5K · 1.0 % | 12.3 s · 6 · **−44.2 / −29.4** | Smoke curling from a box; a boutique perfume shelf ("$300 for a bottle that runs out in 3 months"); an AI woman sniffs a burgundy sweater by a washer; a red-velvet hotel-bar packshot "inspired by [a named luxury fragrance]". A generator's sparkle watermark is visible bottom-right | **The only clear AI ad in the set: generic AI face, near-silent mix, a named-perfume dupe line, a visible watermark.** Everything VXO's QC exists to prevent |
| C22 | The Laundress "POV: washing my 'dry clean only' items at home" ([link](https://www.tiktok.com/@thelaundress/video/7282005783552724267)) | 49K · 1.6 % | 38.2 s · 16 · −29.5 / +0.4 | Bright laundry room; wool shampoo; mesh bags; machine dial | Calm "ritual" demo for a premium brand (older) |
| C25 | Clean That Up #CloroxPartner back-to-school wipes ([link](https://www.tiktok.com/@cleanthatup/video/7685502831851244831)) | 4.9K · 3.3 % | 24.5 s · 8 · −27.5 / −11.4 | Wipes on lunch boxes and backpacks; "kill 99.9 % of germs"; Walmart link | **Sponsored = 0.27× her median.** And the germ claim is only legal because the wipes are EPA-registered |

### 2.3 Paid structure from the Meta libraries (Motion, ~June 2026) [v]

| Brand | Video length range | Formats that recur | Offer / hook pattern |
|---|---|---|---|
| **Earth Breeze** (471 ads) | **57 s – 1 min 57 s** | Skit + unboxing + demo; behind the scenes + infographic; yapper + demo; before and after; expert explainer | "Tap below now to get a great deal on these American-made dish tablets with up to four free gifts"; "JUST $79.80"; "WE'RE SO SORRY."; fear of "ethoxylated alcohols" and "mega corporations" (Motion summary) |
| **Smol** (382) | 15–63 s | Myth vs. fact ("Myth 1: small pods won't work on big loads"); street interview; warehouse-staff testimonial; comment response; split-screen glass "NEW ME / OLD ME"; "a rat in my washing machine" | "Try for £3", "get 9 tablets FREE", "just cover the postage" |
| **Purdy & Figg** (4,000) | 23–39 s | Montage; unboxing; yapper how-to; couple skit ("cut cleaning time in half"); "six sprays swapped for one" (bottles binned) | 65–70 % off starter kits; free cloth and bottle |
| **Blueland** (46) | 15–38 s | Split-screen dirty toilet / tablet; phone screen-recording ("how to remove toilet ring"); cinematic B-roll; static-to-video | 21-day trial, free shipping; retail coupons |
| **Branch Basics** (114) | 4–32 s | Mom testimonial; a "podcast" clip on toxin fear; two women in a Target aisle; static-to-video | "Now at Target", Starter Kit, "only $4.99" |
| **Who Gives A Crap** (439) | — | Demo 16 %, **Us vs Them 8 %**, unboxing | "GET 9 FREE ROLLS", limited editions |

### 2.4 What the measured set says [m]

- **The problem is the hook; the product is optional.** Leaving aside the Zero Waste Store's values post (C06), the five most-viewed brand posts in the window (C01 19.2M, C02 8.6M, C04 5.4M, C05 3.2M, C03 1.6M) are a hack, a reminder, a community answer, a teaser and a myth-bust. C10 and C13 never show the product. **A VXO cleaning film should open on the *problem* in frame 0** (a fitted-sheet ball, a gross drain, a crusted shower head), not on a bottle.
- **The paid signature lives in "useful" formats.** Every post with ≥300K views and <1 % likes (C01, C02, C03, C08, C09, C11, C12) is a hack, a tip or a ritual. Brands pay to distribute *service*.
- **Shares come from community and values.** Share rates: Scrub Daddy collab 1.9 %, teaser 1.4 %, launch 1.2 %; Sheets hack 0.61 %; Nellie's problem 0.54 %; ZWS values 0.48 %. Product demos sit at 0.01 %.
- **One-takes dominate.** 8 of 26 are a single shot (C10, C13, C15, C18, C19, C24 and, in effect, C01 and C05). The median cut rate is **0.3 shots/s**, lower than kitchen (0.4–0.8). **Cleaning is shown as a continuous physical event**, which suits VXO's one-take signature (doc 41 §1), as long as the transformation itself is real.
- **The proof is a colour change, a pour or a shine:** copper (C18), mop water (C26), the oven glass (C11), the stain (C12). Each one is a demonstration under FTC rules.
- **Faces are rare.** Hands-only or backs: C01, C02, C05, C10 (a body, no close face), C11, C12, C13, C15, C18, C19. Faces appear when a person is the authority (janitor C23, the Chief Innovation Officer C16, the social team C04).
- **AI is close to absent, and where it shows, it fails** (C21).

---

## 3. What converts in this niche (with data)

| # | Finding | Number | Source | Status |
|---|---|---|---|---|
| D1 | Online conversion and basket, eco cleaning | Conv. **2.0–2.5 %**, AOV **$0–100**; eco household conv. **3.0–3.5 %** | [Grips cleaning](https://gripsintelligence.com/insights/industries/home-garden/eco-friendly-cleaning), [household](https://gripsintelligence.com/insights/industries/home-garden/eco-friendly-household) | [v] site-wide |
| D2 | Basket at the category's public marketplace | Grove DTC net revenue per order **$69.19** (Q2 2026) | [Grove 10-Q](https://www.sec.gov/Archives/edgar/data/1841761/000184176126000064/grov-20260630.htm) | Audited filing |
| D3 | Advertising drives customer count | Grove: ad spend −55 % → active customers −23 % ("primarily due to our lower advertising spend") | same | Filing |
| D4 | Ad volume | P&F 4,000 / ~134 per week; Earth Breeze 471 / ~58; WGAC 439 / ~53; Smol 382 / ~46; Branch Basics 114 / ~8; Grove 74 / ~10; Public Goods 53 / ~10; Blueland 46 / ~11 | Motion pages | [v] ~Jun 2026 |
| D5 | Format tags | Demo #1 at Smol 30 %, Branch Basics 23 %, Earth Breeze 22 %, Grove 17 %, WGAC 16 %, Blueland 13 %; Before/After 11 % (Smol); Unboxing 7–16 %; Offer-first banner 8–23 %; **Us vs Them** 8 % (WGAC) | Motion | [v] |
| D6 | Media split, 20 newest ads | Images lead at Blueland 14/20, Grove 14/20, Branch Basics 14/20, Public Goods 16/20, P&F 13/20; video leads at Smol 15/20, WGAC 17/20, Earth Breeze 12/19 | Motion | [v] |
| D7 | Paid video length | Earth Breeze 57–117 s; Smol 15–63 s; P&F 23–39 s; Blueland 15–38 s; Branch Basics 4–32 s | Motion storyline timestamps | [v] approximate |
| D8 | Organic hit formats | Hack/tip (13.3M, 6.5M, 333K), problem POV (845K), community launch (5.4M), teaser (3.2M), values (11.3M) | §2 [m] | Measured |
| D9 | Sponsored creator posts | #CloroxPartner at 0.27× the creator's median | C25 [m] | n = 1 |
| D10 | Home & Living creative lifespan | Median **25 d**; 30-day survival 41.8 %, 60-day 21.3 %; storage & organisation 38 d | [Benly Home & Living](https://benly.ai/benchmarks/q1-2026/home-living) | [v] no cleaning sub-vertical |
| D11 | AI ads generally | Gains only when they don't look AI; faces cancel the gain; disclosure trims credibility | doc 45 D30–D37 | Read |
| D12 | AI ads in this niche | One clear AI ad found: 1.5K views, −44 LUFS, AI face, watermark visible | C21 [m] | n = 1 |
| D13 | Eco audience attitude to AI | ZWS "AI uses a significant amount of water and electricity" 8.5M, 9.1 %, **141.8K shares** | [m] | Organic signal |

### 3.1 Answers by question [inf from the table and §2]

- **Formats that convert.**
  1. **Offer + demo DR** (Earth Breeze, Smol, P&F): 30–120 s, a starter kit, a free gift or a "just pay postage" trial.
  2. **The useful hack** with the product as the tool (Grove, Puracy): 6–17 s, paid.
  3. **Myth vs. fact** (Smol "small pods won't work", Grove stainless eggs).
  4. **Swap listicle** (ZWS "10 things"; P&F "six sprays swapped for one").
  5. **Problem POV** (Nellie's fitted sheet).
  6. **Character/community launch** (Scrub Daddy).

  VXO can own the **hook and world** of 1, 3 and 5, and the whole of 6 for brands with a mascot-able product.
- **Proof types, strongest first:**
  1. a visible transformation on a real surface (copper, mop water, oven glass, a stain);
  2. a "lab" or test ritual with a number (Blueland's "100 formulas", Smol's "big loads" myth test);
  3. a price-per-load sum;
  4. retail availability ("Now at Target", which reads as validation);
  5. review counts and real testimonials;
  6. certifications (EPA Safer Choice, USDA BioPreferred, Leaping Bunny, only if held).
- **Claims that work and are safe:** what it replaces ("one bottle for six sprays", "fits in your mailbox"), what it is ("plant-based surfactants" with a % if true), what it does on a named, tested stain, packaging facts ("100 % plastic-free packaging" only if the film/coating is also plastic-free, §5). **Avoid:** "non-toxic", "chemical-free" (water is a chemical), "kills germs" unless EPA-registered, "safe for kids/pets" without evidence, "biodegradable" without a test and qualifier, "hormone disruptors" about rivals.
- **Offers:** a trial for postage, a starter kit at 50–70 % off, a free forever bottle, "year supply" bundles in Q4, a subscription discount ("20 % off, always", Public Goods). Every VXO film needs an **offer slot** in its last 2 s that the client can re-skin per sale (as in doc 56).
- **Length:**
  - a 6 s loop (problem → result);
  - a 15 s VXO master;
  - a **3–5 s hook head** that grafts onto the client's 45–120 s demo body (LESSONS 53–54).

  In this niche the hook head is the most useful single deliverable [inf from D7].
- **Placements:** Meta Reels/Feed 4:5 (offers), TikTok Spark and TikTok Shop affiliate seeds, retail-media video (Target Roundel, Walmart Connect) for brands launching in stores [inf], Amazon listing video (no CTA super).
- **UGC vs cinematic:** UGC and demos dominate paid. Cinematic wins where the product is a **ritual or an object of design** (Koala Eco glass bottles, Homecourt, Laundry Sauce scent, refill pours) and where the brand wants retail-buyer polish. The VXO pitch is a **cinematic hook that stops the scroll, in front of the client's own UGC demo**.
- **AI and disclosure:** label per doc 45 §5.3. For eco brands, add a plain-English line to the proposal: what the AI built (the world and the gag), what is real (the product, the proof), and that tests run at 480p to keep the compute low [inf]. No AI people at all for eco clients.

---

## 4. AI realism pitfalls specific to cleaning and laundry, and the fixes

Built on doc 43 §1 (model choice), §3 (references) and §5 (failure table). The rule of thumb is the same as in kitchen:
- the **proof** (stain out, shine, dirty water, dissolve test) is **real footage**;
- the **product** is **Kling 3.0 Pro i2v** from the client's photo;
- **people, rooms and gags** are **Seedance 2.5 r2v**;
- **one-move heroes and refill pours** are **Cinema Studio 4.0**.

| Pitfall | What goes wrong | Fix (prompt / reference / process) |
|---|---|---|
| **The cleaning result is the claim** | AI wipes a stain away perfectly, or the grime vanishes with one swipe: a false demonstration | **Never generate the transformation.** Show the dirty state in an AI shot, cut to the client's real "after" insert, or keep the comedic payoff on behaviour (people's reactions), not on the surface |
| **Germ visuals** | Cartoon germs dying, glowing "bacteria" on a counter | Banned for unregistered products (a pesticidal claim, §5). Even for EPA-registered clients, keep germs off screen and use the registered label wording only |
| **Liquids: viscosity** | Detergent pours like water; dish soap splashes; refill concentrate behaves like syrup one shot and water the next | Name the viscosity in words and numbers: "laundry detergent, honey-like, ~500 cP, forms a rope as it pours and folds on itself"; "concentrate, water-thin"; one vessel and one fill level per shot (LESSONS) |
| **Fill levels** | Bottles refill themselves between cuts; a jug is full again after a pour | Script each level: "the bottle is 3/4 full and only ever goes down"; show start/end states with Kling first+last frame |
| **Tablet effervescence** | Tablets regrow, bubble forever, or dissolve in 1 s | Write: "the tablet fizzes, sheds a stream of fine bubbles that rise straight up, and shrinks steadily; it never regrows; it is still visible at the end of the 5 s shot" (real tablets take minutes) [inf]. Never show the solution changing colour unless the real one does |
| **Laundry sheets dissolving** | A sheet vanishes instantly in still water, or melts like ice | A sheet goes translucent, softens and breaks up **with agitation**; in a still glass it stays visible for many seconds. Dissolve speed in cold water is a **claim** (Kind C14 makes it comparative): real insert only |
| **Foam and suds** | Foam that grows from nothing; HE front-loaders brimming with suds (wrong: HE detergents are low-suds) | Suds in the drum stay low, a band at the bottom of the window; hand-wash foam peaks, then slowly collapses; bubbles show thin-film colour and pop, never morph |
| **Spray physics** | A spray mist that hangs in the air like smoke; a trigger that doesn't move; mist from a closed nozzle | "Trigger pulled fully once; a cone of droplets 30–40 cm long hits the surface in under 0.2 s; the droplets bead and run down within 1 s; no mist lingers". Nozzle open/closed state per shot |
| **Front-loader drum physics** | Clothes float weightlessly; the drum spins at wash speed in "rinse"; water fills the whole window | A wash tumble runs ~40–55 rpm: clothes lift to about 2 o'clock and **fall** (centripetal acceleration < g; see C1 physics). The water line sits in the bottom 20–30 % of the window. A spin runs 800–1,400 rpm: the load is plastered flat to the drum wall and blurs. The door glass is curved and fogged slightly. **The camera never enters the drum**: shoot through the door glass from a tripod, or use a real waterproof action cam bolted inside the drum (a known rig) |
| **Dryer behaviour** | Steam pouring out of a dryer; sheets coming out flat every time | Dryer air ~55–65 °C: no visible steam on opening except a faint wisp in a cold room. Fitted sheets *do* ball up (C10). Let the AI play the problem, and the real insert the fix |
| **Mirrors, chrome, glass doors** | The crew, the camera or a ring light appears in the bathroom mirror; reflections don't match the room | Write the camera position and "reflections show only the opposite tiled wall and the window; no camera, no person, no light rig appears in any reflection". Angle mirrors 15–25° off axis. Prefer a matte tile background. Check every frame strip for crew reflections (doc 46 QC) |
| **Streaks and shine** | Glass becomes impossibly invisible (people walk into it); chrome glows like CG | A clean glass still shows a faint reflection and edge highlights. Write "real-world clean glass, faint reflections remain" |
| **Dirty water colour** | Ink-black water, or water that changes colour mid-pour | Real mop water is translucent grey-brown with particles (C26). Only the real insert shows it. AI shows the bucket, never the colour change |
| **Stains** | A red-wine stain that changes shape between cuts; a stain on the wrong garment | One stain, one garment, one position (write "a 6 cm red stain on the left cuff"). Real "before" photo as the reference; Kling i2v for its macro |
| **Labels, ingredient panels, pod and sheet packs** | Garbled tiny text; the logo on a tablet emboss swims | Blank shells in generation, real label comped in post (doc 43 §5). Tablets: emboss only from the real photo via Kling |
| **Pods look like candy** | Glossy colourful pods near food, bowls or children read as edible | **Never put pods or tablets near food, mouths, candy bowls or children** (§5). Pods stay in their closed container or go straight into the drum. This overrides the "product-as-food" format in LESSONS for this niche |
| **Chemistry in mixing** | Bleach poured next to vinegar or ammonia; "DIY" mixes that release chlorine gas | Never show two cleaners mixed, poured together, or open side by side with bleach. Add "no other cleaning products in frame" to PHYSICS |
| **Gloves and hands** | Fused fingers on spray triggers; gloves that change colour | Name the trigger grip finger by finger ("index and middle finger on the trigger, thumb behind the neck"). One glove colour, locked. "Exactly five fingers per hand" (doc 43) |
| **Cloth simulation** | Towels fold themselves; fitted sheets unfold cleanly | Fabric falls with weight; a wet towel is heavy and slaps; a microfibre cloth bunches. Use Kling first+last frame for any fold |
| **Scale of refills** | A 16 oz forever bottle becomes a gallon jug; an envelope of tablets becomes a parcel | Real dimensions + a scale anchor (a hand, a standard US letter envelope 24 × 10.5 cm, a 12 oz can) |
| **Eco props** | Plastic sneaks into an eco brand's set (a plastic spray bottle, a plastic bag, a polyester sponge) | Write a prop rule: "only glass, aluminium, cotton, wood and paper on set; no plastic packaging visible except where the script says". Check every frame |
| **Pets and kids** | A dog licks a freshly mopped floor; a toddler holds a spray | One animal per shot, ≤5 s, from a real photo (LESSONS). **No child ever touches or stands near a cleaning product**; kids only in a separate room or a background wide |
| **AI faces** (eco audience) | The C21 look: a generic glossy model sniffing a sweater | No AI faces for eco clients. Hands, backs, silhouettes, or the client's real people (NY synthetic-performer law, doc 45) |

### 4.1 Model per shot type (consistent with doc 43 §1)

| Shot type | Model / template | Settings | Why |
|---|---|---|---|
| Product macro (bottle, tablet, sheet, pack, forever bottle) | **Kling 3.0 Pro i2v** from the client's photo | 5 s, `sound:"off"`, `cfg_scale` 0.5, `last_image_url` = packshot | Keeps labels, embossing and colour from the image |
| Refill pour / tablet drop hero one-take | **Cinema Studio 4.0** (template 7.3) | `dolly-in` or static, `pacing:"single-shot"`, 720p, 6–8 s | One controlled move; liquid physics written in the prompt |
| Multi-shot comedy with people, rooms, laundromats, elevators | **Seedance 2.5 r2v** (templates 7.5, 7.1 shape) | 9:16, 10–15 s, 4–8 shots, `generate_audio:true` | Multi-angle object fidelity; native SFX as a sync guide |
| Washer-window, dryer and bathroom ambience inserts | **Seedance 2.5 i2v** from a real still of the room | ≤5 s, locked-off | Reflections and physics read better; keep short |
| A product-character world (sponge characters, a mascot) | **Seedance 2.5 r2v**, product as the first ref | 10–15 s | Scrub Daddy-style character comedy |
| Blocking previs | **Wan 3.0** 480p | $0.75 per 15 s, seed | Cheapest |
| **The proof** (stain out, shine, mop water, dissolve test, lab test) | **Real footage only** | Client phone or creator | FTC demonstration rule |
| End card with offer slot | Real product photo + typography | — | Editable per sale |

---

## 5. Policy and legal

### 5.1 US law and self-regulation

- **FTC Green Guides (16 CFR 260), the core eco rulebook.**
  - **Non-toxic** (§260.10): "likely conveys that a product… is non-toxic both for humans and for the environment generally". You need competent and reliable scientific evidence for both, or a clear qualifier. The Guides' own example is a cleaning product called "essentially non-toxic", which is deceptive if it is toxic to the environment ([LII](https://www.law.cornell.edu/cfr/text/16/260.10)).
  - **Free-of** (§260.9): deceptive if the product has a substance posing a similar risk, or if the substance "has not been associated with the product category". Trace amounts are allowed only if unintentional and harmless ([LII](https://www.law.cornell.edu/cfr/text/16/260.9)).
  - **Degradable/biodegradable** (§260.8): an unqualified claim is deceptive unless the item "completely decompose[s] within one year after customary disposal"; landfill-bound items can't make it ([LII](https://www.law.cornell.edu/cfr/text/16/260.8)). Down-the-drain detergents use qualified "readily biodegradable (OECD 301B)" claims [inf].
  - **Recyclable** (§260.12): unqualified only if facilities are available to a "substantial majority", "at least 60 percent", of consumers or communities ([LII](https://www.law.cornell.edu/cfr/text/16/260.12)).
  - **General "eco-friendly"** (§260.4), **refillable** (§260.14), **renewable** (§260.16), **source reduction** (§260.17) all need specific qualification.
  - A revision of the Guides has been pending since the FTC's 2022–2023 review [unverified status in Oct 2026].
- **EPA / FIFRA (germs).**
  - A product that claims to prevent, destroy, repel or mitigate pests, which includes microorganisms under EPA practice [inf], is a pesticide and must be EPA-registered ([40 CFR 152.15](https://www.law.cornell.edu/cfr/text/40/152.15)).
  - **Registered products may not make safety claims** like "safe", "harmless", "nontoxic to humans and pets", or "contains all natural ingredients" ([40 CFR 156.10(a)(5)](https://www.law.cornell.edu/cfr/text/40/156.10)).
  - Treated-article claims protect only the article itself ([152.25](https://www.law.cornell.edu/cfr/text/40/152.25)).
  - **VXO rules:** no "kills germs / antibacterial / sanitizes / disinfects" in words *or* pictures (germ animations, glowing bacteria, a "germ-free" shield) unless the client gives the EPA registration number and the exact label claim. For a registered client (Force of Nature-type), no "non-toxic" or "safe" line.
- **"Plastic-free" and PVA/PVOH.** Pods and most laundry sheets use polyvinyl alcohol film or binders. Whether PVA counts as "plastic" is disputed: Blueland campaigns against it (C20 calls pods out); sheet brands call themselves "plastic-free" [unverified: litigation status against specific sheet brands]. **VXO rule:** "plastic-free *packaging*" only when the packaging truly has none; never "plastic-free product" for a PVA product; never show rival pods "shedding plastic" without the client's study.
- **Comparative and fear claims.** Kind's "competitor detergent sheets: clumpy, messy" (C14) and Earth Breeze's "ethoxylated alcohols… mega corporations" framing [Motion] are comparative or health-implied claims that need substantiation. In doc 56, NAD and the courts punished "toxic rival" cookware claims. Expect the same here: **sell ritual, scent, convenience and weight, never fear of a rival's chemistry.**
- **Demonstrations.** Before/after, stain removal, "streak-free", "lifts red wine", "dissolves in cold water", "one tablet = one load" are all demonstrations (FTC Colgate "sandpaper"; NAD *Dyson v. Dreame*, doc 51 §4). A jump cut that hides the wash (C12) must still show the real product doing the real job.
- **Creator disclosure.** NAD #7521 (P&G v. Blueland, 2025-11-25): TikTok Shop's automatic commission label was adequate for pure affiliates; creators with extra paid deals needed their own disclosure ([BBB](https://bbbprograms.org/media/newsroom/decisions/blueland)). Every VXO "creator kit" ships with disclosure language.
- **Testimonials.** FTC rule 16 CFR 465: no AI "mom" praising the spray; review counts only from real data (doc 45).
- **Contamination and child safety (CPSC, via the [recall API](https://www.saferproducts.gov/RestWebServices/Recall)).**
  - The Laundress, ~8 million units, bacteria (2022-12-01; fabric conditioners again 2023-03-31).
  - Art of Green laundry detergent, ~14,550, bacteria (2022-12).
  - P&G Tide/Gain/Ace/Ariel pods, ~8.2 million bags, child-resistant packaging (2024-04-05).
  - Woolite Delicates, ~16,200, bacteria (2025-03-20).
  - **Thrasio / Angry Orange enzyme stain removers, ~1.5 million, bacteria (2026-01-22).**
  - Clorox Puerto Rico Mistolin/Lestoil, ~6.3 million, bacteria (2026-09-03).

  Preservative-light "clean" formulas are the ones recalled for bacteria [inf]. **VXO rules:**
  - no "pure", "safe for babies" or "safe around kids" supers without evidence;
  - never show pods outside their container except going into a drum;
  - never show a child or pet with a product;
  - never show pods next to food or candy;
  - no ingestion jokes.
- **Ingredient disclosure laws.** California's Cleaning Product Right to Know Act requires ingredient disclosure on the website and label (phased in from 2020–2021) [unverified details]. New York has a disclosure programme [unverified]. These matter only if a film shows an "ingredients" card: it must match the label.
- **State PFAS laws** now reach cleaning products in some states (Maine and Minnesota cover cleaning products in their intentionally-added-PFAS bans from 2025–2026) [unverified]. A "PFAS-free" super needs the client's statement.
- **California SB 343** limits the chasing-arrows symbol and "recyclable" claims to materials CalRecycle finds collected and sorted statewide, with compliance phased in 2025–2026 [unverified exact date]. **No recycling symbol on any VXO-generated packaging.**
- **IP and likeness.** C14 (concert footage of a famous singer) and C15 (a live awards broadcast on a TV) show the category's casual use of others' footage. **VXO never uses real broadcasts, celebrities or lookalikes**, and "inspired by [named luxury perfume]" lines (C21) belong to the client's lawyer, not to VXO's script.

### 5.2 Platform rules

| Topic | Meta | TikTok | VXO action |
|---|---|---|---|
| **Dangerous acts (pods)** | Content that encourages dangerous behaviour is restricted [unverified exact clause] | Dangerous activities and challenges are prohibited (the 2018 pod "challenge") [unverified exact clause] | No pod near a mouth, no "challenge" framing, no product-as-food gag |
| **Before/after and "unrealistic outcomes"** | Ads with unrealistic outcomes are disapproved (doc 45) | Exaggerated or misleading claims prohibited | Real before/after only; "Dramatization." where comic, and still within spec |
| **Gross or shocking content** | Shocking or disgusting imagery is limited in ads [unverified for cleaning] | Same [unverified] | Gross reveals (drain hair, mould, mop water) kept short, off-centre and never the thumbnail. Make a clean thumbnail variant |
| **Health and "toxin" claims** | Health-outcome claims face review | Same | No "detox", "hormone disruptor" or fume visuals |
| **AI labels** | "AI info" | AIGC label | Doc 45 §5.3; the label never fixes a false demo |
| **Third-party marks** | IP policy | IP policy | No Tide orange, no Clorox blue, no Scrub Daddy face shapes. Rival products are generic and unbranded. Couriers wear no USPS/UPS/FedEx trade dress (FTC Impersonation Rule, doc 45) |

### 5.3 Age gates

None for cleaning or laundry. **Exception:** if a stain concept uses red wine, either age-target 21+ on Meta/TikTok or swap to grape juice, tomato sauce or berry smoothie in the paid cut (C4 in §8 does the swap).

---

## 6. The buyer

### 6.1 Who signs a $1,200–3,500 film [inf with evidence]

- **$1–20M founder-led** (Defunkify, Dirty Labs, Kind Laundry, Molly's Suds, Woolzies, Jaws, Puracy, Etee, Koala Eco US): **the founder** signs, often with one growth marketer or a part-time agency. Branch Basics posts its three co-founders' faces, which is founder-voice marketing [m].
- **$20–60M** (Dropps, Earth Breeze, Tru Earth, Blueland, Branch Basics, Laundry Sauce): a **Head of Growth / Performance** owns the Meta budget. The Earth Breeze-type team ships ~58 creatives a week, mostly in-house or creator-made. A **brand or retail-marketing lead** owns retail launch assets. Blueland put its **Chief Innovation Officer** on camera [m], so R&D people are also in the content loop.
- **Retail-led** brands add a **trade-marketing** buyer: the "Now at Target" film, the retail-media video, the shelf-reset asset.

### 6.2 What they fear (ranked)

1. **Greenwashing exposure.** The Green Guides, PVA disputes, NAD, competitor challenges (P&G watches Blueland). An AI studio that writes "non-toxic" on screen is a liability.
2. **AI backlash from their own customers.** Eco buyers share anti-AI posts (D13). A founder will ask: "Won't my customers hate that it's AI?"
3. **Fake-looking results.** Cleaning is a proof category; one obviously generated "after" destroys trust.
4. **Wasted money at a low AOV.** $18–40 products and 2–3 % conversion mean every dollar of creative must pay back through subscriptions.
5. **Volume.** P&F and Earth Breeze ship 50–130 creatives a week. One film is noise unless it yields a hook library.
6. **Missing retail windows.** A store launch date is fixed; the creative must be live that week.

### 6.3 What proof makes them pay $1,200–3,500

- **5 free frames** of *their* product in *their* problem, colour-matched to their pack. One frame must show the **problem hook** (the fitted-sheet ball, the jug-hauling, the drain), not a pretty bottle.
- **A claims sheet:** every on-screen line mapped to their substantiation. Explicit lines: "No germ claims (not EPA-registered)", "No 'non-toxic'", "No rival products shown". This alone separates VXO from the in-house $400 AI team (LESSONS 53–54).
- **The "where AI is used" note** for eco brands: AI built the world and the joke; the product and proof are real; no AI people; tests at 480p.
- **The asset maths:** one 15 s master → a 6 s loop, **five 3–5 s hook heads** to graft onto their best demo bodies, 4:5 + 9:16 + 16:9, an offer-slot end card, 8 stills. Against 50–130 creatives a week, sell **hooks per month**, not films.
- **A calendar fit:** "live by Dec 26 for the January reset" or "live the week you land in Target".
- **A niche portfolio piece** (§8's three best, made as VXO spec films).

### 6.4 Re-buy triggers (why they rebook monthly)

1. **Offers rotate constantly** (P&F "Last chance" / "Save 70 % this long weekend"; Earth Breeze "WE'RE SO SORRY" / "$79.80"): re-skin the end card and hook per offer.
2. **Retail launches roll out store by store and chain by chain** (Blueland: Costco → Kroger → Meijer coupons; Branch Basics: Target): each needs a "now at…" version.
3. **Category extensions** (Earth Breeze: sheets → dish tablets → pet detergent → stain spray; Blueland PowerDuo; Scrub Baby): each new SKU gets a launch film.
4. **Seasonal scents and limited editions** (pumpkin spice, holiday, the WGAC "Splash Edition"): drop films, the Season plan's natural cadence (doc 56 C10 template).
5. **The calendar:** January reset → spring cleaning → Earth Day → back to school → cold and flu → hosting/BFCM. That is about six themed moments a year, before offers.
6. **Fatigue:** Home & Living creatives last a median 25 days (D10). A hook library needs monthly refills.

### 6.5 Best outreach angle

**Lead with their customer's problem and their real proof, not with AI.** "Your [stain/drain/jug] demo is great proof. We'd put a 3-second hook in front of it that stops the scroll (here are 5 frames), claims-checked, so you can test it against your current opener on the same body." For eco brands, mention up front that AI builds the world, not the people or the results.

### 6.6 Sample first DM (never sent; for a founder-led laundry-tablet or sheet brand)

> Hi [first name] — saw you just relisted the full range with Year Supply bundles (10/1). Timely for January "reset" season.
>
> I run VXO, a small studio that makes 15–30 s product films for founder-led brands. I sketched a hook for you called "Water Weight": a courier staggering up a front path under four jugs of liquid detergent, while your whole year arrives as a flat envelope in the mailbox next door. Your real wash footage stays the proof; we only build the hook and the world, with no AI people and no green claims we can't back.
>
> Happy to send 5 free frames using your actual pack, sized as a 3-second opener for your current demo ads. No call needed. Want them?
>
> — [name], VXO

(Every fact in the opening must be checked on their public page before use. Here, the 10/1 relisting is from Dropps' `products.json`; re-check it on the day. If the brand's product doesn't ship flat, use concept C2 or C3 instead.)

---

## 7. Lead signals: the niche scoring add-on for `.claude/skills/vxo-leads/SKILL.md`

Apply on top of the base 100-point score. The add-on can move a lead by **−30 to +30**; HOT stays ≥ 70 after the add-on. Check everything on public pages only.

| Signal | Points | How to check |
|---|---|---|
| **Calendar fit**: 5–8 weeks before the January reset (now → mid-Nov), spring cleaning (pitch early Jan), back-to-school (pitch June), hosting/BFCM (pitch by early Oct) | +8 | Today's date vs §1.4 |
| **Retail launch** in the last 90 days or announced (Target, Costco, Walmart, Kroger, Whole Foods): "Now at…" ads, store locator changes | +7 | Motion page headlines; brand IG; press |
| **SKU velocity / relaunch**: ≥3 new products in 60 days, or a full range relisted (bundles, year supplies, a new category such as dish → pet) | +6 | `https://<store>/products.json?limit=250` → `created_at` (§1.2 snapshot) |
| **High ad volume, low video share**: Meta library ≥70 % image (Blueland, Grove, Branch Basics, Public Goods type) | +5 | Motion library page or Ad Library (manual) |
| **Long demo bodies with weak openers**: paid videos ≥45 s that open on a bottle or a logo, not a problem | +4 | Motion storyline / their TikTok |
| **Brand TikTok median < 1K while hack/creator posts hit 300K+** | +3 | Embed-page IDs → yt-dlp metadata (§method) |
| **Audio faults** in a public video (peak > −1 dBFS or < −24 LUFS) | +2 | `ebur128` on one post: a friendly, concrete note for the DM |
| **Founder on camera / maker story** (co-founders, the lab, the factory) | +2 | TikTok/IG |
| **Running "toxic", "hormone disruptor" or rival-chemistry fear ads now** | **−10** | Their ads (Motion summary) |
| **Germ/disinfect claims on an unregistered product**, or "non-toxic" on a registered one | **−10** | PDP vs EPA registration number on the label |
| **Recall or contamination news in the last 18 months** | −8 | CPSC recall API by brand name |
| **Named in an NAD case or false-ad suit** in the last 12 months | −5 | BBB National Programs decisions; court news |
| **Corporate-owned** (P&G, Clorox, SC Johnson incl. Method/Mrs. Meyer's, Unilever incl. Seventh Generation/The Laundress, Church & Dwight, Reckitt, Thrasio incl. Angry Orange, Henkel) | −5 | Ownership; the path runs through agencies |
| **Amazon-only private label / white-label sheets with no brand site** | −15 | Brand site, reviews |

**VERY hot in this niche looks like [inf]:** a founder-led laundry, refill or cleaning brand, $2–30M, AOV $25–80, that **just landed in a national retailer or relaunched its range**, sells into a calendar moment 5–8 weeks out, runs a big Meta library that is mostly static or long demos with no problem hook, makes no fear or germ claims, and has a founder or R&D lead willing to be the voice. Example: base 72 + calendar 8 + retail 7 + SKU velocity 6 = 93.

**Current snapshot (2026-10-09, public data only, NOT a lead list; each needs a dossier per vxo-leads §2b):** Dropps (31 SKUs relisted 10/1), Tru Earth (11 bundle SKUs 8/26), Earth Breeze (pet detergent 9/9, stain spray 9/24, 471 ads), Branch Basics (Target launch, 70 % image ads), Blueland (PowerDuo launch, retail coupons, 70 % image ads), Koala Eco (8 SKUs in 60 d), Woolzies (75 holiday SKUs). Red flags to check: Earth Breeze's and Branch Basics' fear-led copy (−10 if current).

---

## 8. Ten ready film concepts (invented brands)

Conventions:
- **Brands are invented**; clear the names on USPTO before use; no real-brand look-alikes. Rival products are generic and unbranded (no orange jugs, no blue wipes tubs).
- **Otto and Vee are absent** (client-style specs), except where a "spec version" line says how to recast. They appear only in VXO's own films. C5 and C6 are the most Otto-ready.
- **Every camera position is a real rig:** tripod (incl. low-mode/floor), slider, dolly, overhead C-stand arm, Steadicam, handheld, a hard mount (an elevator-corner or car-door mount), a waterproof action cam bolted inside a drum, a jib. **The camera never passes through glass, walls, doors, drums or appliances.** Any shot through a washer door is from a tripod outside the glass.
- **Proof slot:** each concept names the real footage the client supplies. AI never performs the cleaning claim.
- **No dialogue on visible lips.** Each film ends with a 2-line VO tagline in a locked voice over a frame with no visible lips, plus the logo card and an **offer slot**.
- **No AI faces in close-up** (eco audience, NY synthetic-performer law): hands, backs, profiles, wides.
- **No children near products, no pods near food, no germ visuals, no "toxic" visuals.**
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

### C1 · VELLUM (laundry + cleaning tablets that ship flat) — "Water Weight" (15 s) ★ BEST 1

- **Idea:** a quiet suburban street. A courier staggers up a front path under four jugs of liquid laundry detergent and a crate of spray bottles. He sets them down, wipes his brow, goes back to the van for more. Next door, without breaking stride, he slides one flat envelope into a mailbox: a year of VELLUM tablets.
- **Hook (0–1 s):** motion already happening. The courier's legs and a jug swinging into frame, the jug's handle creaking, a heavy *thunk* on the porch step.
- **Punchline (product-caused):** the neighbour with the jugs opens her door, looks at the pile, then across at the mailbox flag going up next door. **The joke only works because the product removes the water weight.**
- **Built on:** the category's own "we don't ship water" argument [c], Smol "replaced the entire cleaning cupboard", P&F "six sprays swapped for one" [Motion], doc 44 "rule of three" + "the held last shot is the joke".

| # | t (s) | Shot (rig) | Action / notes |
|---|---|---|---|
| 1 | 0.0–2.0 | **Tripod, low (knee height)**, side-on to the path, 35 mm | Courier's legs enter frame-left, two jugs in each hand, arms straight, shoulders down; *thunk* as the first jug lands on the step at 1.6 |
| 2 | 2.0–4.0 | **Steadicam**, following behind at 1.5 m | He walks back to an unbranded grey van, the open side door showing **more jugs** |
| 3 | 4.0–6.5 | **Tripod, wide**, across the street (long lens, 85 mm) | Second trip: a crate of plastic spray bottles on top of two jugs; he tilts back for balance; the porch pile grows (one direction only) |
| 4 | 6.5–8.5 | **Tripod, medium**, next-door mailbox at chest height | Without slowing, he slides **one flat envelope** into the mailbox with two fingers; the flag stays down; a soft *tk* |
| 5 | 8.5–10.5 | **Proof slot (real):** overhead C-stand arm | The client's real footage: a tablet drops into a forever bottle of water and fizzes; one tablet goes into a drum |
| 6 | 10.5–13.5 | Shot-3 tripod (identical framing), held | The jug-house door opens; a woman (back to camera) looks at the pile; next door a hand raises the mailbox flag; she slowly looks from one to the other |
| 7 | 13.5–15.0 | Packshot (real photo) | The envelope + forever bottle; "VELLUM. We don't ship water." + offer slot |

- **Physics check:**
  - A typical large liquid detergent jug holds ~150 fl oz ≈ 4.4 L. At a density of ~1.03 kg/L that is **≈ 4.6 kg each**, so four jugs ≈ 18.5 kg.
  - The courier's posture must show it: arms straight down, shoulders depressed, short steps, slight lean back. The jugs swing **in phase with his steps** with a pendulum period of ~1 s (handle-to-centre ~0.25 m → T = 2π√(0.25/9.81) ≈ 1.0 s).
  - When set down, a jug thuds; it never bounces.
  - The envelope: ~60 tablets × ~4 g ≈ 240 g + paper ≈ **0.25 kg**, held between two fingers, one-handed.
  - The van door stays open in all van shots (continuity); the porch pile only ever grows; the mailbox flag goes up once.
  - **Claim:** "we don't ship water" is true only for a dry product; the brand must back any "% water in liquid detergent" figure if one is shown (none is shown here).
- **Audio map (timecoded):**
  - 0.0: a plastic handle creaks; footsteps on concrete (heavy, uneven), heavy breathing (off-mic).
  - 1.6: **jug *thunk*** on the step (the loudest hit).
  - 2.0–4.0: van door rattle, keys.
  - 4.0–6.5: bottles clink in the crate; a strained exhale at 6.0.
  - 7.6: the envelope *tk* into the mailbox (quiet, crisp).
  - 8.5: a tablet *plink* + fizz (real insert sound).
  - 10.5: a door latch; 11.8: the metal flag *clack*.
  - 12.0–13.5: silence + a bird (one beat).
  - 13.5 VO (dry, unhurried, mouth off-screen): `A year of laundry.` [pause] `Fits in the mail.` + sonic logo.
- **Model / template:** shots 1–4 and 6 = **one Seedance 2.5 r2v multi-shot** (template 7.5 shape, "EXACTLY FIVE SHOTS AND FOUR HARD CUTS"; refs: a courier wardrobe sheet (**no carrier insignia**), the clean street plate, a generic unlabelled jug on grey, the client's envelope on grey). Shot 4's envelope close can be a **Kling 3.0 Pro i2v** insert if the label must read. Shot 5 is real. Wan 3.0 480p previs first.
- **Cost:** Wan $0.75 + Seedance 15 s $23.88 + Kling insert $0.95 + 8 stills $2.40 + VO $0.10 = **≈ $28**.
- **Claim check:** "a year" must match the pack's real load count at the brand's stated frequency; "fits in the mail" must be true for that pack; no recycling symbols; rivals unbranded.
- **Why it's the best:**
  - the hook is motion in frame 0;
  - the punchline is caused by a true, visible product property (weight);
  - there are no faces and no AI performing a claim;
  - the physics is simple and checkable;
  - the 6 s loop (shots 1–4) stands alone as a hook head in front of any demo body;
  - it re-skins for January ("a year of laundry"), BFCM (year-supply bundles) and Earth Day.

  **Spec version:** Otto is the courier (moustache, deadpan, no mouth visible); Vee times his second trip on her one stopwatch from the porch.

### C2 · LOBBY & LINEN (luxury-scent laundry detergent) — "Elevator" (15 s) ★ BEST 2

- **Idea:** an office elevator at 8:59. A man in a freshly washed sweater steps in. One by one, the others inhale slowly. At his floor, the doors open, he steps out — and everyone else steps out with him, though it's not their floor.
- **Hook (0–1 s):** the elevator doors already closing on a crowded car; a hand slips between them, the doors bounce open (real elevator behaviour), *ding*.
- **Punchline (product-caused):** the doors close on an empty elevator, with one person's coffee left on the handrail. **Scent made visible by behaviour**, the only honest way to film a smell.
- **Built on:** Laundry Sauce / Kind's scent-as-luxury positioning [m, Motion], doc 44 rule of three, deadpan held wide. It is the opposite of C21: same promise, no AI face, no perfume dupe line.

| # | t (s) | Shot (rig) | Action / notes |
|---|---|---|---|
| 1 | 0.0–1.5 | **Hard-mounted wide camera in the elevator's upper corner**, 16 mm (a real security-cam position) | Doors closing; a hand in a cream knit sleeve stops them; doors reopen; he steps in, back to camera |
| 2 | 1.5–4.5 | Same corner mount, held | Doors close. Five passengers, all seen from above and behind. The woman nearest him lifts her chin slightly and inhales; a beat later the man next to her does the same; then a third |
| 3 | 4.5–6.5 | **Handheld, chest height**, inside the car facing the panel (a real camera op in the corner, no mirrors in the car) | Close on the sweater's knit shoulder; a passenger's profile leans 5 cm closer, eyes closed |
| 4 | 6.5–8.5 | **Proof slot (real):** tripod, the client's laundry room | Real footage: a cap of detergent poured; a sweater lifted from the drum (scent can't be shown, so the ritual is the proof) |
| 5 | 8.5–12.0 | **Tripod in the corridor**, facing the elevator doors, wide | *Ding*. Doors open on 14. He steps out. Pause. All five step out after him in a loose line, as if it were their floor |
| 6 | 12.0–13.5 | Shot-1 corner mount | The empty car; one coffee cup on the handrail; the doors close |
| 7 | 13.5–15.0 | Packshot (real photo) | Bottle on a hotel-lobby marble; "LOBBY & LINEN." + offer slot |

- **Physics check:**
  - Doors reopen when obstructed (safety edge); they travel ~0.5 m/s and pause ~3–5 s fully open.
  - Six adults in a small car (~1.5 m²) stand ~30–40 cm apart.
  - The inhale is visible as a slow chest rise and a 2–3° chin lift over ~1.5 s, never a cartoon sniff.
  - Floor-indicator text is unreadable or comped in post.
  - **There are no mirrors in the car** (no crew reflections): write "brushed-steel walls, matte, no mirrors".
  - The cup's level never changes; its fate is scripted (it stays on the rail).
- **Audio map:** 0.0 door rumble + the safety-edge *bump* at 0.6, *ding* 0.9; 1.5 hum of the car, cable creak; 2.6 / 3.4 / 4.1 three soft inhales (each a little longer, rule of three); 4.5 knit-fabric brush; 6.5 detergent glug (real); 8.5 *ding* + doors; 9.4–11.5 six sets of footsteps on carpet, staggered; 12.0 the doors close on silence; 13.5 VO: `Clean is a feeling.` [pause] `Yours is contagious.` + sonic logo.
- **Model / template:** shots 1–3, 5, 6 = **Seedance 2.5 r2v** 15 s multi-shot (≤6 people, so keep everyone small in frame and from behind; "only the backs and tops of heads are visible; no faces toward camera"); shot 4 real; shot 7 real photo.
- **Cost:** Wan $0.75 + Seedance 15 s $23.88 + stills $2.40 + VO $0.10 = **≈ $27**.
- **Claim check:** no "lasts 12 weeks" or longevity numbers unless tested; no named-perfume comparison; "contagious" is puffery (a figure of speech).
- **Why it's in the top 3:** the hook is real elevator behaviour in frame 0; the punchline is caused by the product; no faces; it re-skins per scent drop (the passengers' wardrobe and the lobby change with each scent); and it beats the one AI ad in the niche (C21) at its own game.

### C3 · FUNKLESS (enzyme sports laundry) — "The Bench" (15 s) ★ BEST 3

- **Idea:** a locker room. A player unzips his gym bag. Everyone on the long bench slides one seat away in unison. Next week: he unzips again, washed with FUNKLESS, and they slide back, all the way.
- **Hook (0–1 s):** sound-first. A loud zip, then a wooden bench scraping as six people slide away together.
- **Punchline (product-caused):** in the "after", they slide back so far that the last player gets bumped off the end of the bench onto his feet (a harmless step-down). Deadpan.
- **Built on:** Smol "rewashing clothes that still smell damp" [Motion], Defunkify's niche (§1.2), doc 44 reversal + callback.

| # | t (s) | Shot (rig) | Action / notes |
|---|---|---|---|
| 1 | 0.0–2.5 | **Tripod, locked-off wide**, end-on to a 4 m wooden bench, chest height | Zip; six players (backs/profiles, in neutral grey kit) slide one seat away in unison |
| 2 | 2.5–4.0 | **Slider**, close on the open bag | A crumpled grey T-shirt; one light fly-like *buzz* (sound only; no insect shown) |
| 3 | 4.0–6.5 | **Proof slot (real)** | The client's real footage: the shirt into a drum, an enzyme pre-soak, a timer (no "smell" visual) |
| 4 | 6.5–7.5 | Title card | "One week later." |
| 5 | 7.5–12.5 | Shot-1 tripod (identical framing), held | Zip. Pause. All six slide **back**, closer than before; the man at the far end is nudged off and steps down, standing; he looks at the bench |
| 6 | 12.5–15.0 | Packshot | Pouch on a locker shelf; "FUNKLESS." + offer slot |

- **Physics check:**
  - Six adults (~80 kg each) slide on a varnished bench with a friction coefficient around 0.3–0.4. Each body shifts ~45 cm by lifting slightly on their hands and scooting; it takes ~0.6 s and happens **in unison but not perfectly** (stagger 2–4 frames).
  - Nobody "glides".
  - The last player steps down onto his feet (a 45 cm bench), no fall. Write "no one falls; he simply stands".
  - Bag contents stay identical between shots 1 and 2.
  - Smell is never visualised (no green lines, no fumes: §5 "toxic visuals").
- **Audio map:** 0.0 **zip** (the hook), 0.4–1.1 bench-scrape chord (six overlapping scrapes, the loudest moment); 2.5 fabric rustle, a single *bzz* 3.2; 4.0 washer door, water (real); 6.5 silence on the card; 7.5 zip; 8.3 a half-second pause (room tone); 8.8–9.6 the scrape chord in reverse direction; 10.2 one *thud* of feet on tile; 12.5 VO: `Keep the sweat.` [pause] `Lose the funk.` + sonic logo.
- **Model / template:** shots 1, 2, 5 = **Seedance 2.5 r2v** 15 s ("EXACTLY THREE SHOTS AND TWO HARD CUTS; identical framing in shots 1 and 3"; six people = keep them wide, backs and profiles; doc 43 notes Seedance glitches past 3 characters, so test the 480p proof first and fall back to **four** players if counts drift); shot 3 real.
- **Cost:** Wan $0.75 + Seedance 15 s $23.88 + stills $2.40 + VO $0.10 = **≈ $27** (budget one extra 720p take, +$6.93, for the crowd).
- **Claim check:** "removes odour" needs the brand's test; no "antibacterial" (FIFRA) unless registered; no gym or league logos.
- **Why it's in the top 3:** a sound-first hook; rule of three in two beats; a physical punchline everyone understands; no faces needed; and a 2.5 s hook head (zip + scrape) that graft onto any sports-laundry demo.

### C4 · LIFTWELL (enzyme stain remover) — "Second Glass" (15 s)

- **Idea:** a white-tablecloth dinner party. A guest knocks over a glass of red (grape juice in the paid cut); everyone freezes. The host reaches calmly for LIFTWELL, sprays, and then deliberately tips her *own* glass too, "so you don't feel bad".
- **Hook (0–1 s):** the glass is already tipping; liquid arcs onto white linen.
- **Punchline (product-caused):** the host's confidence comes from the product; the guest's mortified profile relaxes.
- **Shots:**
  1. (0–1.5) **Tripod, table height**, 3/4: the tip and the splash.
  2. (1.5–3.5) **Locked-off wide**: everyone freezes (backs/profiles).
  3. (3.5–5.5) **Slider**: the host's hand to the spray on the sideboard, two pumps.
  4. (5.5–8.5) **Proof slot real**: the client's real stain-lift on the same linen type, before/after, no jump cut.
  5. (8.5–11.5) **Tripod medium**: she tips her own glass, deadpan.
  6. (11.5–13.5) Wide: the table exhales, someone laughs (off-screen audio).
  7. (13.5–15) Packshot.
- **Physics check:**
  - A 150 mL pour from a tipped wine glass spreads ~15–20 cm on cotton in ~1 s and wicks for 3–5 s more.
  - The glass rolls an arc on its bowl; stem glasses don't roll straight.
  - Each spill gets its own fixed stain shape and position (the stains are written as two separate objects).
  - Enzymes need minutes of dwell, so the "after" is real footage and never shown happening in AI.
- **Audio:** 0.0 the glass *tink* on a plate; 0.3 the liquid *splash*; 1.5 total silence (the freeze, the joke's setup); 3.9 / 4.4 two trigger *pfft*s; 5.5 real scrub/rinse; 8.9 the second glass *tink* + splash (callback); 11.5 laughter, chairs; 13.5 VO: `Spill freely.` + offer slot.
- **Model:** Seedance 15 s (shots 1–3, 5–6) + real proof. **≈ $28.**
- **Claim check:** "lifts red wine/juice" only on tested fabrics with the brand's dwell time; age-gate if real wine (§5.3).

### C5 · QUIETLOAD (enzyme dishwasher tablets) — "Pre-Rinse" (15 s)

- **Idea:** a man pre-rinses every plate under a running tap, scrubbing it nearly clean before loading the dishwasher. His partner watches the water bill rise on the counter (an envelope, unreadable). She loads the next plate straight from the table, ketchup and all, drops in one QUIETLOAD tablet and closes the door.
- **Hook (0–1 s):** water roaring from a tap onto a plate, sound-first.
- **Punchline:** he hesitates, then hands her the plate he was scrubbing, still dripping. Deadpan.
- **Spec version (VXO's own film):** Otto pre-rinses, deadpan, moustache over the sink; **Vee times each plate on her one stopwatch**; the stopwatch click is the rhythm. Ideal Otto-and-Vee spec because neither needs to speak.
- **Shots:**
  1. (0–1.5) **Overhead C-stand arm** over the sink: tap, plate, sponge.
  2. (1.5–4) **Tripod wide**, kitchen profile: him at the sink, her at the island.
  3. (4–6.5) Slider: plates stacking in the rack, each already clean.
  4. (6.5–9) **Proof slot real**: the client's real dirty-plate → clean result through their machine.
  5. (9–12.5) Tripod medium: she loads a dirty plate, tablet in the dispenser, closes; he hands over his.
  6. (12.5–15) Packshot.
- **Physics check:**
  - A kitchen tap runs ~1.5–2.2 gal/min (5.7–8.3 L/min); 20 s per plate × 12 plates = 4 min ≈ **23–33 L** pre-rinse.
  - Write the water stream as a continuous column, splashing off the plate, with droplets on his forearms.
  - The dishwasher door closes with a soft latch.
  - The tablet goes into the dispenser cup (not loose); the pouch is closed and never near food.
- **Audio:** tap roar 0.0 (loud); stopwatch clicks (spec) every 2 s; plate clatter 4.0–6.5; dishwasher door 11.2; VO 12.5: `Skip the rinse.` [pause] `Keep the evening.` + offer slot.
- **Model:** Seedance 15 s + Kling tablet insert + real proof. **≈ $28.**
- **Claim check:** "no pre-rinse needed" only if the brand's test supports it; no water-saving figure unless sourced.

### C6 · EVERSCRUB (long-life silicone scrubber) — "Retirement" (15 s)

- **Idea:** a retirement party, in the sink caddy. A grey, frayed sponge sits on a tiny cake plate; the other sink items (a brush, a bottle cap, a ring dish) gather round. EVERSCRUB arrives, new. The old sponge is lowered gently into the bin. Pause. EVERSCRUB stays. Months pass (window light changes); it's still there, still bright.
- **Hook (0–1 s):** a tiny party-horn *toot* and a single falling confetti square landing on a wet sponge.
- **Punchline:** the last frame is a calendar page flip in the background (unreadable), and the scrubber is unchanged.
- **Spec version:** Otto gives the eulogy in VO only (mouth hidden), one-line; Vee clicks her stopwatch as "time served".
- **Shots:**
  1. (0–2) **Macro on a slider** at counter height: the caddy party.
  2. (2–4.5) Tripod, top-down: hands place the new scrubber.
  3. (4.5–7) **Proof slot real**: the client's real scrub test (pan, grout) + a rinse and quick dry.
  4. (7–9) Tripod: the old sponge lowered into a pedal bin; the lid closes.
  5. (9–13) **Locked-off tripod**, same caddy framing, a light sweep from morning to evening ×3 (window timelapse feel): the scrubber unchanged.
  6. (13–15) Packshot.
- **Physics check:**
  - The sponge is wet: it sags and drips 2–3 drops when lifted.
  - Silicone stays clean and dries without staining.
  - Light changes come from the window, so the shadows rotate consistently (sun from frame-left, moving right).
  - No faces anywhere. No sponge "characters" with eyes (avoids Scrub Daddy trade dress).
- **Audio:** toot 0.2; confetti tick 0.6; wet squelch 2.5; real scrub 4.5; bin pedal + lid 7.6; three time-of-day ambiences (birds, traffic, crickets) 9–13; VO: `Some things retire.` [pause] `This one doesn't.` + offer slot.
- **Model:** Kling 3.0 Pro i2v ×3 (party macro, bin, lighting states via first+last frame) + Cinema Studio 8 s locked-off. **≈ $10** (cheap tabletop).
- **Claim check:** lifespan ("lasts X months") from the brand's test and replacement guidance; "replaces N sponges" only with data.

### C7 · FOLIO (laundry sheets, dorm) — "Fifth Floor" (15 s)

- **Idea:** move-in day at a dorm. The lift is "out of order" (a handwritten sign). One freshman lugs a jug of detergent, a basket and a jumbo fabric-softener bottle up five flights. His roommate jogs past him on the stairs with a thin FOLIO pack in his back pocket.
- **Hook (0–1 s):** an out-of-order sign flaps on a lift door; a basket corner bangs a stair rail, *clang*.
- **Punchline:** at the top, the roommate is already on the bunk, laundry started; the jug guy drops onto the floor and gives the jug a pat.
- **Shots:**
  1. (0–1.5) Tripod: the sign.
  2. (1.5–4) **Steadicam** up the stairwell behind the jug guy.
  3. (4–6) **Tripod on the landing**, looking down: the roommate overtakes.
  4. (6–8.5) **Proof slot real**: a sheet into a drum with clothes, the machine starts.
  5. (8.5–12.5) Tripod, dorm room wide: the jug guy collapses onto a beanbag; the roommate on the bunk.
  6. (12.5–15) Packshot.
- **Physics check:**
  - A full 150 fl oz jug ≈ 4.6 kg + basket ~3 kg: his pace on the stairs is ~0.5 steps/s, rising on the stronger leg, rail used.
  - The roommate takes stairs two at a time at ~2 steps/s.
  - The jug's fill level never changes.
  - The stairwell must be geometrically consistent (same rail, same landing window) across shots 2–3; use one stairwell plate as a reference.
- **Audio:** sign flap 0.2; *clang* 0.8; heavy footsteps + breathing; light running footsteps 4.2; washer start (real) 6.5; beanbag *whump* 9.5; VO: `Moving in?` [pause] `Pack light.` + offer slot.
- **Model:** Seedance 15 s + real proof. **≈ $28.**
- **Claim check:** "works in cold water / HE machines" per the brand; no university marks or real dorm names; back-to-school timing (live Aug 1).

### C8 · CLEARCOAT (streak-free glass concentrate) — "The Door" (15 s)

- **Idea:** a backyard party. A guest carrying two plates walks towards the patio. The sliding glass door is so clean that she stops 10 cm short, unsure, and reaches out a finger to check. Three more guests stop behind her, each reaching out a finger. The host slides the door open from the other side.
- **Hook (0–1 s):** a finger approaches glass in macro, sound of party chatter muffled through glass.
- **Punchline:** the queue of pointing fingers; nobody walks into anything (no harm), and the joke is the hesitation.
- **Shots:**
  1. (0–1.5) **Macro, slider** perpendicular to the glass (camera on the *inside*, never passing through): the fingertip approaches; a faint reflection of the garden on the glass.
  2. (1.5–5) **Tripod, wide from inside the house**, the door in frame-centre: four guests line up, fingers out.
  3. (5–8) **Proof slot real**: the client's real spray-and-wipe on a door with side light, before/after.
  4. (8–11.5) Tripod, same as 2: the host slides the door open; the guests flinch slightly, then step in.
  5. (11.5–13) Macro: one fingerprint left on the glass; a hand wipes it with one pass.
  6. (13–15) Packshot.
- **Physics check:**
  - Clean glass still shows faint reflections and edge highlights (write it in).
  - The sliding door travels on a track at ~0.5 m/s with a rolling rumble.
  - The fingerprint is an oily smudge, visible at a grazing angle only.
  - **No one collides with the glass** (keeps it harmless and policy-safe).
- **Audio:** muffled party through glass (low-pass) 0–5; fingertip *tap* none (they never touch); door roll 8.4; party audio opens up (high frequencies return) 8.6; one squeak of a cloth 12.0; VO: `So clean it's confusing.` + offer slot.
- **Model:** Seedance 15 s (shots 2, 4) + Kling macros ×2 + real proof. **≈ $29.**
- **Claim check:** "streak-free" under the brand's test conditions; the "so clean it's confusing" line is puffery.

### C9 · FLOCKWELL (wool dryer balls) — "The Knot" (15 s)

- **Idea:** Nellie's measured problem (C10), solved. A dryer door opens and a single balled fitted sheet, with socks and a T-shirt trapped inside, rolls out. The owner pulls it apart like a magician's scarf: sock, sock, tee, another sock. Cut: the next load with FLOCKWELL balls; she opens the door and the sheet is loose.
- **Hook (0–1 s):** the dryer door pops open and the ball tumbles out onto the floor (motion in frame 0).
- **Punchline:** she pulls a **ninth** sock out of the knot and looks at it; it isn't even hers.
- **Shots:**
  1. (0–1.5) **Floor-level tripod** facing the dryer: the ball rolls out.
  2. (1.5–6) **Tripod medium**: she unwinds it; items spill one by one (count them: eight socks + one tee + one "foreign" sock).
  3. (6–8.5) **Proof slot real**: the client's real load with three wool balls, the sheet coming out loose.
  4. (8.5–11.5) Tripod close: the ninth sock held up; deadpan.
  5. (11.5–13) Kling macro: three wool balls on a folded sheet.
  6. (13–15) Packshot.
- **Physics check:**
  - A dryer tumbles at ~50 rpm; a fitted sheet's elastic corners trap smaller items.
  - The ball is ~40 cm across, warm and slightly damp in the centre (the items inside are visibly damper).
  - Wool balls (~60 g each, 7 cm) bounce once on landing.
  - Item counts only go down as items are pulled out, then the one new sock appears from the knot's last fold (scripted fate).
- **Audio:** door pop 0.2; soft fabric *flump* 0.6; sock pulls, each a cloth zip; the dryer's tick as it cools; VO: `Untangle your Sundays.` + offer slot.
- **Model:** Seedance 10 s (shots 1–2, 4) + Kling ×2 + real proof. **≈ $20.**
- **Claim check:** "reduces tangling / drying time" only with the brand's test; no "replaces dryer sheets' chemicals" fear line.

### C10 · PANTRY & PINE (refill concentrates, seasonal scents) — "The Scent Cellar" (12 s; Season-plan drop template)

- **Idea:** a drop film built like doc 56 C10 but in a cool stone cellar: a row of aged oak shelves holds glass forever bottles, one per season, like a wine cellar. A hand slides out the new limited scent (pumpkin, pine, citrus), uncorks the refill pouch, pours it into the forever bottle, and a chalk tag on the shelf is wiped and rewritten with the drop date.
- **Hook (0–1 s):** a refill pour already in motion, a thin glossy stream into glass (sound-first *glug*).
- **Punchline:** the chalk tag for the *next* season reads "Soon" (scarcity, re-skinned each drop); if the drop sells out, it flips to "Gone".
- **Shots:**
  1. (0–2) **Cinema Studio dolly-in** on the pour.
  2. (2–4) Tripod: the cellar shelf, wide, warm practical light.
  3. (4–6) **Kling i2v** from the real limited-edition bottle: a 20° arc.
  4. (6–8) **Proof slot real**: the real scent's ingredients (pine needles, peel) on a board.
  5. (8–10) Tripod macro: the chalk tag wiped and rewritten (hand only; text comped).
  6. (10–12) Packshot + date.
- **Physics check:**
  - A refill concentrate pours water-thin: a laminar stream ~3–4 mm wide with a slight wobble; a small air bubble *glugs* every ~0.5 s from the pouch spout.
  - The bottle fills to the line, never above.
  - The glass shows the cellar's bulb reflection, not a crew.
  - Chalk dust falls.
- **Audio:** *glug* 0.0–2.0; cellar room tone; the bottle set on wood 3.8; chalk scratch 8.2; VO: `Autumn's in.` [pause] `Refill Tuesday.` + date card.
- **Model:** Cinema Studio 8 s $3.70 + Kling ×2 $1.90 + stills $1.80 = **≈ $8**; each re-skin ≈ $3 (a new Kling bottle shot + a new tag).
- **Claim check:** "limited" only if truly limited; scent ingredient imagery must match the real fragrance notes; no "natural" claim beyond the label.

### 8.1 Ranking

1. **C1 "Water Weight" (VELLUM).** Best overall:
   - a motion hook;
   - a punchline caused by a true, visible property (no water to carry);
   - no faces and no AI performing a claim;
   - simple, checkable physics (the pendulum swing, the 18 kg posture);
   - a 6 s loop that works as a hook head for every tablet, sheet or concentrate brand;
   - it fits January, BFCM and Earth Day.

   As a VXO spec film, Otto carries the jugs while Vee times him.
2. **C2 "Elevator" (LOBBY & LINEN).** Makes the invisible benefit (scent) visible through behaviour; re-skins per scent drop; directly answers the niche's one failed AI ad.
3. **C3 "The Bench" (FUNKLESS).** A sound-first hook, rule of three, a physical callback; perfect as a 2.5 s hook head.

For a VXO cleaning spec reel, make **C1 + C2 + C10**: one category film, one premium scent film, one drop template. Recast C5 with Otto and Vee as the studio's own short.

---

## 9. Ten insights nobody asked for

1. **The eco audience shares anti-AI posts, so make AI invisible as AI.** ZWS's "AI uses water and electricity" post earned **141.8K shares** [m], the most-shared item in the set. For eco clients VXO should commit in writing: no AI people, AI only for worlds and gags, real product and proof, low-resolution tests first. It turns the biggest objection into a reason to choose VXO over the brand's own $400 AI tool (LESSONS).
2. **In cleaning, the hack is the ad.** Grove's 19.2M and 8.6M posts and Clean That Up's 13.3M are tips [m]. A VXO concept can open on a genuinely useful micro-tip that the product completes. It earns saves (and saves are what the paid hack formats run on).
3. **Build "problem hooks", not product hooks.** The highest share rates come from shared pain (Nellie's fitted sheet, Scrub Daddy's drain fight). Keep a **20-item problem library** for the niche (fitted-sheet ball, crusted shower head, drain hair, gym-bag smell, the jug haul, mop water, sticky oven door, the sock thief, the toilet ring, the over-poured detergent cap…) and pitch hooks from it.
4. **The money is moving to shelves.** Eco DTC online GMV is down 20–50 % (Grips), Grove's customers fell 23 % with its ad cuts, and the brands' 2026 headlines are retail ("Now at Target", Costco coupons). **Pitch "retail launch films"** (a 15 s "now at…" with a store-shelf beat and an editable retailer card), timed to each chain's rollout.
5. **Sell hooks by the dozen.** Libraries of 46–4,000 ads with 57–117 s demos (Earth Breeze) mean the bottleneck is the first 3 seconds, not the film. A Season plan here should be priced as "**20 hook heads + 1 hero film per month**", tested on the client's best existing body (LESSONS 53–54).
6. **The FIFRA line is a sales tool.** Most eco founders don't know that an animated germ is a pesticide claim, or that a registered disinfectant can't say "non-toxic". A one-page claims sheet per film (§3.1 and §5) shows expertise no in-house AI team has.
7. **Contamination is the category's hidden risk.** Bacteria recalls (The Laundress 8M, Angry Orange 1.5M, Clorox PR 6.3M) [CPSC] hit preservative-light formulas. VXO scripts must never promise purity, and the lead scorer should check the recall API first (−8).
8. **Character products travel; bottles don't.** Scrub Daddy's median is 80,500 views vs 160–1,152 for bottle brands [m]. If a client's product has a shape that can hold a personality (a sponge, a scrubber, a dryer ball, a tablet), propose a **product-character** world (a Seedance world, product as first ref), never with a face that copies Scrub Daddy's.
9. **Teasers out-share launches.** Scrub Daddy's teaser (product hidden) got a 1.43 % share rate vs 1.20 % for the launch [m]. Offer every launch client a **two-film pack**: a 10 s teaser seven days before, plus the launch film, from the same world. It costs VXO little extra and doubles the moments.
10. **Category audio is broken.** 15 of 26 posts sit under −24 LUFS and 6 clip [m]. Combined with kitchen (doc 56), that makes "your ads are 18 LU too quiet" a free, checkable, friendly opener for almost any home-goods founder.

---

## 10. QA gate additions for this niche

Run after doc 44 §10, doc 45 §5.4, doc 46 §7 and doc 56 §10:

1. **No AI-performed cleaning result:** every stain lift, shine, dissolve, before/after or dirty-water reveal is the client's real footage. Comic exaggeration carries "Dramatization." and still stays within spec.
2. **No germ visuals or words** unless EPA-registered, with the exact label claim; no "non-toxic/safe" on a registered product.
3. **Green claims checked** against 16 CFR 260 (non-toxic, free-of, biodegradable, recyclable, plastic-free) with written substantiation; no recycling symbols on generated packs.
4. **No rival products, colours or shapes** (no orange jugs, no blue tubs, no smiley sponges with Scrub Daddy's features); no courier trade dress.
5. **Child and pod safety:** no child or pet with a product; no pods or tablets near food, candy or mouths; pods only in a closed pack or going into a drum; no two cleaners mixed.
6. **Liquids and levels:** viscosity right per product; fill levels only ever go down; foam and suds behave (low suds in HE drums).
7. **Reflections:** no crew, camera or light rig in mirrors, chrome, glass doors or washer windows.
8. **Drum physics:** wash tumble lift-and-fall at ~50 rpm; spin plasters the load; the water line low; the camera never inside a drum unless it is a named action-cam mount.
9. **Eco props:** no stray plastic in an eco brand's set.
10. **No AI faces** for eco clients; NY synthetic-performer disclosure if any AI person appears for others.
11. **Gross-reveal thumbnail:** a clean alternative first frame for platforms that limit shocking imagery.
12. **Audio master:** −14 LUFS integrated, ≤ −1.0 dBTP measured on the encoded file (LESSONS).
13. **Deliverables:** a 6 s loop, a 15 s master, **5 hook heads (3–5 s)** with matching loudness for grafting, an offer-slot end card, 4:5 + 9:16 + 16:9, 8 stills, a claims sheet, and the "where AI is used" note.

---

## 11. Open items for the next run (search budget was exhausted)

- The US cleaning/laundry market size and growth from a primary source (Circana, Euromonitor, ACI).
- Founders, funding and revenue for Dropps, Earth Breeze, Tru Earth, Blueland, Branch Basics, Laundry Sauce, Kind Laundry, Defunkify, Truly Free and Force of Nature.
- Litigation on "plastic-free" laundry sheets/pods (PVA), and the status of Blueland's PVA petition to EPA.
- The exact SB 343 compliance date, California/New York ingredient-disclosure details, and the Maine/Minnesota PFAS cleaning-product provisions.
- Meta Ad Library run lengths for Earth Breeze, Smol, P&F and Branch Basics (manual browser check; automated fetch is 403).
- The exact Meta and TikTok ad-policy clauses on dangerous acts and shocking imagery.
- YouTube TrueView metadata for Dropps, Blueland, Grove and Scrub Daddy brand films.

---

## Sources

All URLs are inline above. Measured files (not committed): `scratchpad/niche2/cleaning/C01…C26/` with `v.info.json` metadata, and `scratchpad/niche2/cleaning/an/` with `*_tile.jpg` (2 fps frame tiles), `*_stats.txt` (scene cuts at 0.30, LUFS, peak) and `*_asr.txt` (faster-whisper base.en). Brand and creator ID harvest and metadata: `scratchpad/cscripts/emb/` (275 posts; 24 brand accounts after dropping 3 unrelated handles) and `scratchpad/cscripts/cre/` (61 posts, 5 creators). Shopify snapshot: `scratchpad/cscripts/shop_out.txt`. Additional sources read:
- **Filings:** [P&G 10-K FY2026](https://www.sec.gov/Archives/edgar/data/80424/000008042426000103/pg-20260630.htm), [Clorox 10-K FY2026](https://www.sec.gov/Archives/edgar/data/21076/000002107626000034/0000021076-26-000034-index.htm), [Church & Dwight 10-K](https://www.sec.gov/Archives/edgar/data/313927/000119312526048139/0001193125-26-048139-index.htm), [Grove Collaborative 10-Q Q2 2026](https://www.sec.gov/Archives/edgar/data/1841761/000184176126000064/grov-20260630.htm).
- **Market:** [Grips eco-friendly cleaning](https://gripsintelligence.com/insights/industries/home-garden/eco-friendly-cleaning), [Grips eco-friendly household](https://gripsintelligence.com/insights/industries/home-garden/eco-friendly-household), [Grips home & garden](https://gripsintelligence.com/insights/industries/home-garden), [Benly Home & Living Q1 2026](https://benly.ai/benchmarks/q1-2026/home-living).
- **Ad libraries:** Motion pages for [Blueland](https://motionapp.com/library/blueland), [Grove Collaborative](https://motionapp.com/library/grove-collaborative), [Branch Basics](https://motionapp.com/library/branch-basics), [Earth Breeze](https://motionapp.com/library/earth-breeze), [Purdy & Figg](https://motionapp.com/library/purdy-and-figg), [Smol](https://motionapp.com/library/smol), [Who Gives A Crap](https://motionapp.com/library/who-gives-a-crap), [Public Goods](https://motionapp.com/library/public-goods), [Home goods trending](https://www.motionapp.com/trending/home-goods/).
- **Law and policy:** [16 CFR 260.8](https://www.law.cornell.edu/cfr/text/16/260.8), [260.9](https://www.law.cornell.edu/cfr/text/16/260.9), [260.10](https://www.law.cornell.edu/cfr/text/16/260.10), [260.12](https://www.law.cornell.edu/cfr/text/16/260.12), [Part 260 index](https://www.law.cornell.edu/cfr/text/16/part-260); [40 CFR 152.15](https://www.law.cornell.edu/cfr/text/40/152.15), [152.25](https://www.law.cornell.edu/cfr/text/40/152.25), [156.10](https://www.law.cornell.edu/cfr/text/40/156.10); [NAD #7521 P&G v. Blueland](https://bbbprograms.org/media/newsroom/decisions/blueland); CPSC recalls via the [SaferProducts API](https://www.saferproducts.gov/RestWebServices/Recall): [The Laundress](https://www.cpsc.gov/Recalls/2023/The-Laundress-Recalls-Laundry-Detergent-and-Household-Cleaning-Products-Due-to-Risk-of-Exposure-to-Bacteria), [The Laundress fabric conditioners](https://www.cpsc.gov/Recalls/2023/The-Laundress-Recalls-Fabric-Conditioners-Due-to-Chemical-Hazard-Including-Previously-Recalled-Units), [Art of Green](https://www.cpsc.gov/Recalls/2023/AlEn-USA-Recalls-Art-of-Green-Laundry-Detergent-Products-Due-to-Risk-of-Exposure-to-Bacteria), [P&G pods](https://www.cpsc.gov/Recalls/2024/Procter-Gamble-Recalls-8-2-Million-Defective-Bags-of-Tide-Gain-Ace-and-Ariel-Laundry-Detergent-Packets-Distributed-in-US-Due-to-Risk-of-Serious-Injury), [Woolite](https://www.cpsc.gov/Recalls/2025/Woolite-Delicates-Detergent-Recalled-by-Reckitt-Due-to-Risk-of-Exposure-to-Bacteria-Sold-Exclusively-on-Amazon-com), [Angry Orange](https://www.cpsc.gov/Recalls/2026/Thrasio-Recalls-Angry-Orange-Enzyme-Stain-Removers-Due-to-Risk-of-Exposure-to-Bacteria), [Clorox Puerto Rico](https://cpsc.gov/Recalls/2026/Clorox-Puerto-Rico-Recalls-6-Million-Scented-Mistolin-and-Lestoil-Multi-Purpose-Cleaners-Due-to-Risk-of-Exposure-to-Bacteria).
- Builds on docs 36, 41, 42, 43, 44, 45, 46, 51, 53 and 56 in this folder and `research/ai-video-reels/lab/LESSONS.md`.
