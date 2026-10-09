# 57 — Niche deep-dive: non-alcoholic spirits, mocktails, energy and functional drinks

Research brief, 2026-10-09. No generation money was spent. Nobody was contacted. Nothing was sent.

**What this adds.** Doc 11 §1 and §4 cover the visual grammar of beverages and NA spirits: the shots, the light, the liquid workarounds, the ban list and a recipe film for an invented NA aperitivo. Doc 49 covers functional sodas, coffee and electrolytes: Poppi/Celsius/Olipop claims cases, the "facts with units, never effects" rule, TikTok's 18+ energy-drink rule and eight food concepts. This doc does not repeat them. It adds:
- a market map for the **adult non-alcoholic** world (NA spirits, NA beer and wine, RTD mocktails, social/adaptogen tonics, hemp-THC drinks on the eve of a federal ban, and energy drinks), 30 DTC brands with live price bands and launch velocity, a seasonality calendar and where they advertise;
- teardowns of **27 posts I downloaded and measured** (from metadata on 412 TikToks across 39 brand accounts), 18 written up in full, plus Meta-library reads for 5 brands;
- conversion data for the niche (NIQ 2025, Gallup 2025, Benly Q2 2026 F&B, Motion's Meta libraries, Brightfield, Circana via Celsius filings);
- AI-realism pitfalls that are specific to cocktails, ice, foam, corks, cans and bars, with prompt and model fixes consistent with doc 43;
- the policy and legal picture that is **unique to alcohol-adjacent products**: Meta's "no consumption" rule for NA, TikTok's 25+ talent rule, Google's 2026 alcohol rewrite, TTB "non-alcoholic" wording, state minor-sale laws, the hemp-THC ban (now 11 Dec 2026), kratom and adaptogen claim exposure;
- the buyer, re-buy triggers, an outreach angle and a sample DM (never sent);
- a niche scoring add-on for `vxo-leads`;
- 10 ready film concepts (3 marked best) and 10 non-obvious insights.

**Tags.**
- `[m]` I measured it from the file: ffmpeg scene cuts at threshold 0.30, 2 fps frame tiles that I looked at, a 0.5 s RMS envelope, librosa onset rate and beat regularity (autocorrelation peak; > 0.5 = steady music bed, < 0.15 = voice or no steady beat), EBU R128 integrated loudness and sample peak, and a faster-whisper (base.en) transcript. Or: I pulled it from a public `products.json` / embed page on 2026-10-09.
- `[c]` the brand's or platform's own claim. `[v]` a vendor or agency figure (directional). `[inf]` my inference. `[unverified]` I found no primary evidence, or it is from memory.

**Method and limits.**
- **TikTok.** Brand creator-embed pages (`tiktok.com/embed/@handle`) gave 422 post IDs on 39 accounts; yt-dlp returned metadata for 412. I downloaded 28 posts to `scratchpad/niche2/drinks/` for analysis only (one was a photo carousel that arrives as audio only, so 27 are measured video). **No media is committed or republished.** Handles for Seedlip, Lyre's, Ritual, Free Spirits, Monday, Kin's second account, Gorgie, Zoa and Feel Free could not be resolved, so those brands are covered from their stores and press only.
- **Paid signature.** As in docs 49 and 55: a post with ≥ ~250K views and a like rate under ~1 % is almost certainly paid (Spark Ads / boosted). Brands only keep paying for winners, so this is the best public proxy for "sold" `[inf]`.
- **Meta Ad Library** returns HTTP 403 to our fetcher again. I used Motion's public library pages (Ghia, De Soi, Moment, Olipop; Poppi, Celsius, Bloom and Liquid Death also exist) for active-ad counts, cadence, format mix and quoted hooks. They were "refreshed 4 months ago". **Run-length winners on Meta could not be confirmed** (§10).
- **Web search budget ran out** part-way through this session (a shared per-session cap). Everything after that point came from direct fetches of known primary pages, our own measurements and Shopify feeds. Claims I could not re-check are marked `[unverified]`.
- **Shopify.** `products.json` was public on 35 of 60 stores tried; used for price bands and launch velocity (§1.4, §7).

---

## 0. The 10 findings that matter most

1. **The category is small, fast and made of drinkers.** Off-premise NA beer, wine and spirits passed **$1.01B in 2025, +19.2 %** (+$162M), but that is only **0.9 % of alcohol dollars**. Inside it, NA spirits grew **+62.2 %** (0.2 % share of spirits), NA spirits RTDs **+92 %**, NA wine **+21.9 %** and NA beer **+16.3 %** while total bev-alc fell −3.4 % to $110B. And **95 % of NA buyers also buy alcohol** ([NIQ 2025 Year in Review](https://develop.nielseniq.com/global/en/wp-content/uploads/sites/4/2026/01/NIQ-US-BevAl-2025-Year-in-Review_5780f6.pdf)). **Film the occasion and the swap, not a sober identity.** "I quit drinking" speaks to the 5 %.
2. **Moderation is now the majority view.** Only **54 % of US adults drink** (record low; 62 % in 2023) and **53 % say even moderate drinking is bad for health**; among 18–34s it is **50 %** and about two-thirds ([Gallup 2025](https://news.gallup.com/poll/693362/drinking-rate-new-low-alcohol-concerns-surge.aspx)). The demand is real; the creative problem is that most brands still sell it as abstinence.
3. **The biggest paid reach came from the plainest films.** Poppi's **6 s single-shot fridge restock** reached **14.5M views** at 0.54 % likes (paid signature); its 10 s cooler-restock companion 3.9M [m]. Liquid Death ran a **silent, 15 s, CG-only can film** for its Cinnamon Roll Iced Tea to **1.4M at 0.03 %** [m]. Hiyo's 15 s Dry-January unbox-and-pour hit **1.1M at 0.06 %** [m]. **Paid in drinks = one idea, ≤ 15 s, product in frame 0.** The cinematic comedy (Liquid Death "wings" 4.4M, "Blood Zero" 504K) is the brand layer on top.
4. **Organic reach comes from recipes and hacks, not brand films.** Like-rate leaders: Spiritless "load a Jarritos with NA tequila" (1.5M, **8.5 %**), Alani's frozen-fruit mocktail and energy-drink gummy bears (2.3M each, **7.7 %**), Moment's "weird drink" creator (2.0M, **9.7 %**), Ghia joining a snack-plate trend (1.2M, **7.2 %**), Curious "POV: you quit drinking but still love margaritas" (394K, 5.2 %) [m]. **A recipe is the native ad unit of this category**, and it is the one thing AI renders worst (pours). Plan real inserts (§4).
5. **Meta treats NA like alcohol the moment a frame shows drinking or an alcohol brand.** Meta allows non-alcoholic beverages "as long as they do not depict alcohol or consumption"; any "depiction of alcohol brands/logos" makes it an alcohol ad (21+ in the US) ([Meta alcohol policy](https://transparency.meta.com/policies/ad-standards/restricted-goods-services/alcohol/)). **AI's default bar fills the back-bar with real liquor labels**, which turns an NA ad into an alcohol ad and a trademark problem in one frame. The clean-plate rule (doc 43 rule 5) is a compliance rule here.
6. **A federal cliff is 63 days away.** Hemp-derived THC above **0.4 mg per container** becomes illegal on **11 Dec 2026** (moved from 12 Nov by the 2 Sep 2026 stopgap; [Marijuana Moment](https://www.marijuanamoment.net/trump-signs-bill-to-delay-hemp-thc-product-ban-giving-lawmakers-more-time-to-craft-regulations-instead-of-prohibition/), [Harris Sliwoski](https://harris-sliwoski.com/es/cannalawblog/the-intoxicating-hemp-products-ban-was-delayed-a-month-now-what/)). THC drinks were **~$1.1B in 2025** (from $630M) and **1.6M cases, +133 %** ([Brightfield](https://blog.brightfieldgroup.com/brightfield-statement-on-hemp-derived-thc-ban), [Shanken](https://www.shankennewsdaily.com/2026/07/21/40269/hemp-thc-drinks-reached-1-6-million-cases-on-triple-digit-growth-in-2025/)). Cann has already launched **"0MG (ZERO THC)"** (20 Aug and 24 Sep 2026) and a Sober October bundle [m]. **THC brands pivoting to zero-THC lines need new films now** — but VXO never makes the THC film (Meta and Google ban it).
7. **The heaviest spenders are static-heavy: that is the opening.** Moment runs **239 active Meta ads, ~24 new a week, 85 % images**; Ghia 14 active, 55 % images; De Soi 39 active but 80 % video ([Motion: Moment](https://motionapp.com/library/moment), [Ghia](https://motionapp.com/library/ghia), [De Soi](https://motionapp.com/library/de-soi)) [v]. Benly Q2 2026 F&B: images live a **23 d** median vs video **27 d**, and the "AI-Generated" attribute has a **33 d median and 55 % 30-day survival**, among the best of the attributes shown ([Benly F&B Q2](https://benly.ai/benchmarks/q2-2026/food-beverage)) [v].
8. **Comedy that parodies the category leader is the energy-drink playbook, and it ships with a disclaimer.** Liquid Death Energy's "gets you chicken wings" spot (30 s, 9 shots) has a woman drink on a roof, "fly", land flat on a lawn, then appear in a full-body cast with wings — under a permanent super **"DO NOT ATTEMPT. FOR REAL. STAGED PERFORMANCE."** [m]. That disclaimer is what lets an energy brand show a fall. **VXO needs a disclaimer library** (§5.5).
9. **The hook words are claims.** Hooks quoted in live Meta ads: "Hangover-free summer cocktail" (De Soi), "Sleep score TANKING?", "WINE FACE IS REAL", "why people on GLP-1s go with Moment" (Moment), "THE PERFECT BUZZ WITH NO HANGOVER" and "10–15 MINUTE ONSET" (Cann) [v/m]. Feel Free's maker paid **$8.75M** in 2024 over calm/"no more habit-forming than caffeine" marketing ([BevNET](https://bevnet.com/pr/2024/09/18/botanic-tonics-reaches-settlement-agreement-in-class-action-lawsuit-reaffirms-commitment-to-industryleading-standards)). **On a VXO film the super is "0.0 %", an ingredient, or a number in mg — never an effect, a mood, a body or a morning.**
10. **The calendar is the lead list.** NA has two "Super Bowls" (Dry January, Sober October), plus Thanksgiving-to-NYE hosting, summer "mocktail season", festival season, Prime Day and Halloween limited flavours. Moment shipped a new themed collection every 1–2 weeks this summer (Sober Summer sale 5 Aug, back-to-school 14 Aug, Soberfest 21 Aug, Labor Day 25 Aug, Sobertober 15–16 Sep) [m]. **Today (9 Oct) a brand needs its Dry-January film approved by early December. The hottest window of the year starts now (§7).**

---

## 1. Market map

### 1.1 Size and growth (US unless stated)

| Segment | Number | Source | Status |
|---|---|---|---|
| NA beer + wine + spirits, off-premise | **$1.01B in 2025, +19.2 % (+$162.3M)**; 0.9 % of alcohol dollars; 95 % of NA buyers also buy alcohol | [NIQ 2025 YIR](https://develop.nielseniq.com/global/en/wp-content/uploads/sites/4/2026/01/NIQ-US-BevAl-2025-Year-in-Review_5780f6.pdf), L52W to 3 Jan 2026 | Primary (NIQ) |
| NA spirits | **+62.2 %** $, 0.2 % share of spirits; total spirits −1.8 % | same | Primary |
| NA spirits RTD (canned mocktails) | **+92.0 %** $ (the fastest RTD segment after hard juice) | same | Primary |
| NA wine / NA beer | **+21.9 %** / **+16.3 %** (NA beer = 1.5 % of beer $); NA beer +22 % in Circana MULO+C | NIQ; [Constellation/HOPWTR release](https://www.cbrands.com/blogs/press-releases/constellation-brands-announces-agreement-to-acquire-non-alcoholic-brand-hopwtr) | Primary |
| Earlier trend | NA $823M in 2024 (+27.2 %); $925M L52W to 2 Aug 2025 (+22 %); NA spirits value +67 % YTD Aug 2025 | [drinksint](https://drinksint.com/news/fullstory.php/aid/11598/.html), [Beer Business Daily via BeerNet](https://beernet.com/wsd/wsd-article/niq-on-the-billion-dollar-non-alc-growth-engine/), [Shanken](https://www.shankennewsdaily.com/2025/08/15/38096/non-alcohol-spirits-gaining-traction-in-the-u-s/) | Secondary on NIQ |
| Forecast | IWSR: US no-alc +25.4 % through 2026 (measure unclear); global no-alc +7 % volume CAGR to 2028, > US$4bn incremental | [Fox/IWSR](https://www.fox13news.com/news/beyond-dry-january-rise-non-alcoholic-drinks-adult-beverage-market), [drinks-intel](https://drinks-intel.com/cross-category/no-alcohol-segment-expected-to-post-us4bn-growth-by-2028-category-intel/) | [v] |
| Who drinks | 54 % of adults drink (62 % 2023); 50 % of 18–34s; 53 % say moderate drinking is bad for health | [Gallup](https://news.gallup.com/poll/693362/drinking-rate-new-low-alcohol-concerns-surge.aspx) | Primary survey |
| Why they cut | 31 % of US consumers changed alcohol purchases to manage spending; 81 % think declining a drink without explanation is fine; 86 % comfortable choosing low/no at a party (Heineken research) | [BeverageDaily Jan 2026](https://www.beveragedaily.com/Article/2026/01/29/alcohol-free-drink-trends-sober-curious-consumers-brand-building/) | [v] |
| Hemp-THC drinks | **$630M (2024) → ~$1.1B (2025)**, projected $2.6B by 2030 pre-ban; 1.6M cases (+133 %), 305K points of distribution (+129 %); **6–10 mg overtook 10+ mg**; 47.8 % of THC-drink users drink less alcohol | [Brightfield](https://blog.brightfieldgroup.com/brightfield-statement-on-hemp-derived-thc-ban), [Shanken](https://www.shankennewsdaily.com/2026/07/21/40269/hemp-thc-drinks-reached-1-6-million-cases-on-triple-digit-growth-in-2025/), [Whitney Economics](https://www.whitneyeconomics.com/press-detail/whitney-economics-issues-u.s.-cannabis-and-hemp-beverage-report-thc-beverage-sales-top-%241.1b) | [v] |
| Energy drinks | Celsius Holdings (Celsius, Alani Nu, Rockstar) **20.8 % $ share** of US RTD energy, Q3 2025; **Alani Nu retail +114 %**, 7.2 % share; Celsius brand 11.2 %; c-store energy > $16B in 2025 (+10 %) | [Celsius Q3 2025](https://ir.celsiusholdingsinc.com/news/news-details/2025/Celsius-Holdings-Reports-Third-Quarter-2025-Financial-Results/default.aspx); c-store figure via [baristalife](https://baristalife.co/blogs/blog/energy-drink-statistics-2026) | [c] / [unverified] |
| Deals 2026 | Constellation buys the rest of **HOPWTR** (27 Mar); The Wine Group buys **Phony Negroni** (29 Apr); **The Zero Proof** acquires The New Bar (24 Jun); **Neutonic** raises $6M at $60M (28 Apr) | [Constellation](https://www.cbrands.com/blogs/press-releases/constellation-brands-announces-agreement-to-acquire-non-alcoholic-brand-hopwtr), [Wine Group](https://www.thewinegroup.com/the-wine-group-acquires-phony-negroni-non-alcoholic-brand/), [PR Newswire](https://www.prnewswire.com/news-releases/the-zero-proof-acquires-the-new-bar-creating-one-of-the-most-comprehensive-brand-and-distribution-platforms-in-adult-non-alcoholic-beverages-302809453.html), [BevNET](https://bevnet.com/pr/2026/04/28/neutonic-raises-6m-at-a-60m-valuation-to-accelerate-global-expansion-across-retail-and-new-markets) | [c] |
| Funding totals | NA-spirits startups: 90 companies, 20 funded, $92.9M raised (Lyre's $53M, Aplós $10.5M); Moment $5M (May 2025) | [Tracxn](https://tracxn.com/d/trending-business-models/startups-in-non-alcoholic-spirits/___fXkqrUrvwLfHBw9J-jq0_VlquUj2qqijta7sIbYJiY), [Techleap](https://finder.techleap.nl/news/feed/moment-secures-5m-from-btomorrow-ventures) | [v] |

**Read-across [inf].** The pool of founder-led $1–20M brands is large because the category is young, retail velocity is fragile and the strategics (Constellation, The Wine Group, Diageo) buy proven brands. A founder who wants to be bought needs **brand equity that reads on screen**. That is VXO's pitch.

### 1.2 Sub-niches and how each one sells

| Sub-niche | Typical price (DTC) | Core buyer truth | What the winning ads show [m/v] |
|---|---|---|---|
| NA spirits (gin/tequila/whiskey/aperitivo alternatives) | $30–60 per 700–750 ml bottle; $90+ premium | "Does it taste like a real drink?" Ritual, glassware, the serve | Recipe builds, POV "you quit but still love margaritas", us-vs-mocktail statics |
| RTD mocktails and spritz cans | $25–60 per 4–12 pack | Convenience; a can that looks grown-up at a party | Pour into a nice glass; snack-plate and hosting trends; discovery sets |
| Social/adaptogen tonics ("buzz without booze") | $25–60 per 4–12 pack | A reason to drink something at 5 p.m.; the "why" of alcohol | Dry-January unbox-and-pour; festival POV; founder story; GLP-1 hooks (risky) |
| NA beer / hop water | $15–44 per pack | Taste parity; game day | Athletes, tailgates, "can sound" ASMR, retail |
| NA wine / NA sparkling | $25–30 a bottle | Celebrations, dinner | Cork pop, toast, POV at events (Three Spirit at Wimbledon) |
| Hemp-THC drinks (pre-ban) and their 0 mg lines | $11–27 per can or 4-pack | "A buzz without the hangover" (a claim) | Talking-head dosing explainers; bundles; now Sober-October 0 mg |
| Energy (zero sugar, "clean", paraxanthine) | $34–36 per 12 | Taste, flavour drops, sugar facts, identity | Office/prank comedy, mocktail recipes, parodies of Red Bull, CG flavour launches |

### 1.3 Thirty DTC brands to know (founder-led, roughly $1–20M where findable)

Revenue for almost all of these is private. Price and launch data are `[m]` from `products.json` on 2026-10-09 unless marked. Founders are named only where a primary page in this session confirmed it. **Benchmarks above VXO's band** are marked (B).

| # | Brand | Type | Price band (median item) [m] | Launches last 60 d [m] | Notes |
|---|---|---|---|---|---|
| 1 | **Ghia** | NA aperitivo + spritz cans | $60 (bundles to $253) | 0 (newest SKU 30 Mar 2026) | Founder Mélanie Masarin (her own founder video [m]); 14 active Meta ads, 55 % image [v]; TikTok median 428 views; GLP-1 and Mother's Day hooks |
| 2 | **De Soi** | Adaptogen NA aperitifs | $60 | **4** (5 Oct: Vino Violette, Wine Night Duo, sampler, ritual bundle) | 39 active Meta ads, 80 % video, ~8 new/week [v]; "hangover-free" hooks |
| 3 | **Moment** | Adaptogen sparkling ("mood") | $46 | **16** (themed collections every 1–2 weeks) | Shark Tank brand; **239 active Meta ads, 85 % image, ~24 new/week** [v]; $5M raise 2025 |
| 4 | **Kin Euphorics** | Nootropic/adaptogen tonics | $39 | 2 (Three Acts, 5 Oct) | TikTok median 3,082 |
| 5 | **Hiyo** | Organic "social tonic" cans | $25 | 1 | Dry-January paid post 1.1M [m]; festival activations |
| 6 | **Three Spirit** | Plant-based NA (UK-born, US retail) | $28 | 0 | Wimbledon POV 50K [m] |
| 7 | **Curious Elixirs** | NA cocktails, bottled | $49 | 0 | Like rates 5–10 % on POV and memes [m] |
| 8 | **Mingle Mocktails** | Canned and bottled mocktails | $45 | 1 (Espresso Martini, 26 Aug) | TikTok median 246; factory BTS at 300 views [m] |
| 9 | **Lyre's** | NA spirits range (B by funding, $53M raised) | $54 | **6** (three Halloween serves 7 Oct, gift sets) | Canned mocktails as trial format [c] |
| 10 | **Ritual Zero Proof** | NA spirits | $30 | 0 | Ownership [unverified] |
| 11 | **Free Spirits** | NA spirits | $34 | 0 | — |
| 12 | **Spiritless** | NA tequila/bourbon (Jalisco 55, Kentucky 74) | store 404 | — | Jarritos hack 1.5M, 8.5 % [m] |
| 13 | **Optimist Botanicals** | NA botanical spirits | $35 | 1 (SMOKESHOW, 10 Sep) | — |
| 14 | **Abstinence** | Premium NA spirits (SA) | $91 | 0 | — |
| 15 | **For Bitter For Worse** | NA aperitifs | store unreachable | — | [unverified] |
| 16 | **Wilderton** | NA botanical spirits | store unreachable | — | [unverified] |
| 17 | **Little Saints** | Plant-magic NA cocktails | store 404 | — | TikTok median 128 |
| 18 | **Tomorrow Cellars** | NA wine | $28 | 2 (Sparkling Blanc de Rhône, Rhône Blanc, 25 Aug) | Raising $2M per [Dry Atlas](https://www.dryatlas.com/articles/15-emerging-non-alc-founders-to-watch-in-2026/) |
| 19 | **Surely** | NA wine | $25 | 0 (store dormant since 2024) | — |
| 20 | **Hoplark** | Hop water / hop tea | $44 | **5** (Cider One, tailgate bundles) | — |
| 21 | **Athletic Brewing** (B) | NA beer | $15 | 4 | Uses NFL QBs; too big for VXO, the creative benchmark |
| 22 | **Brez** | Mushroom/THC "social" drinks | $60 | 0 since Jul 2026 | Founder calls top customer (107 s one-take, 5.6 %) [m]; THC exposure |
| 23 | **Cann** | Hemp-THC social tonics | $11–27 | **17** (0MG zero-THC, Sober October, Halloween, Tailgate bundles) | Paid explainer 2.7M [m]; the clearest ban-pivot signal |
| 24 | **Wynk** | Hemp-THC seltzer | $25 | 0 | Ban exposure |
| 25 | **UPDATE** | Paraxanthine energy | $36 | 1 (Passion Orange Guava, 11 Sep, Circle K) | CG/AI-look flavour film 30K [m]; Kardashian collab 4.1M |
| 26 | **Bloom** | Energy + "sparkling energy" | $34 | **6** (Canada launch, bundles) | (B) by size [inf] |
| 27 | **Proper Wild** | Plant-based energy shots | $40 | 1 | — |
| 28 | **Kill Cliff** | Clean energy (Navy SEAL foundation) | $36 | 0 | — |
| 29 | **Cure Hydration** | Electrolytes | $24 | 1 | Founder Lauren Picasso; "20,000 stores"; TikTok Shop [m] |
| 30 | **Feel Free (Botanic Tonics)** | Kava/kratom tonic | $75 | 0 | **Do not pitch**: $8.75M settlement, kratom litigation (§5) |

Watch-list from the [Dry Atlas 2026 founders list](https://www.dryatlas.com/articles/15-emerging-non-alc-founders-to-watch-in-2026/): Disco Fizz (NYC energy, launching summer 2026), Tomonotomo (NA agave), Driftology (functional nightcaps, 40K IG, pre-launch), FABRIC (Denver hop water, THC line planned), Plaid Circus (NA sipping spirits + spritz RTDs into Erewhon/Sprouts/Whole Foods in 2026), Norïe, OSIA, Glasrose Zero Proof. Pre-launch and first-retail brands are the cheapest VXO wins (§7).

### 1.4 Price bands (what a buyer can afford) [m]

| Product | Entry | Core | Premium |
|---|---|---|---|
| NA spirit, 700–750 ml | $28–34 (Ritual, Free Spirits, Three Spirit) | $45–60 (Ghia, Lyre's, De Soi, Curious) | $90+ (Abstinence) |
| RTD mocktail / tonic 4-pack | $20–25 | $35–45 (12-pack $44 Moment) | $60 (Brez) |
| Bundles / discovery sets | $40 | $60–110 | $150–250 (Ghia, Cann Sober October $215–243) |
| Energy 12-pack | — | $34–36 | — |
| Hop water / NA beer pack | $15 | $44 | — |

**What it means [inf].** AOVs of $45–110 and subscription offers (Moment "one easy subscription") mean a $1,200 Short needs ~15–30 new orders to pay back on first purchase, and far fewer once subscription LTV is counted. Lead with the Season plan for any brand on subscription.

### 1.5 Seasonality calendar (US)

| When | Event | Who pushes | Creative lead time |
|---|---|---|---|
| **1–31 Jan** | **Dry January** (the biggest NA month; "dry January but make it floaty" = Hiyo's 1.1M paid post) | All NA spirits, tonics, NA beer | Films approved by **early Dec**; outreach Oct–Nov |
| Jan | New-year fitness | Energy, electrolytes | Dec |
| Early Feb | Super Bowl / game day | NA beer, hop water, energy | Dec–Jan |
| Feb | Valentine's ("spice up your date night" hooks: Ghia, Moment) | NA spirits, NA sparkling | Jan |
| Mar–Apr | Festival season (Coachella, EDC); 4/20 (THC, now ending) | Tonics, energy | Feb |
| May | **Mother's Day** gifting (Ghia ran several variants) | NA spirits | Apr |
| Jun–Aug | "Mocktail summer", Sober Summer sales, July 4, Prime Day (July) | Everyone; RTD peak (NIQ: RTDs peak in summer) | Apr–May |
| Late Aug–Sep | Back-to-school (**energy: adult framing only**), Labor Day, Soberfest | Energy, tonics | Jul |
| **1–31 Oct** | **Sober October**, Halloween limited flavours (Lyre's 3 Halloween serves 7 Oct; Liquid Death "Blood Zero"), **Prime Big Deal Days** (Poppi 30 % off, 6 Oct) | All | Aug–Sep |
| Nov | Thanksgiving hosting; THC ban cliff (11 Dec) | NA spirits, THC brands' 0 mg lines | Oct |
| Dec | Holiday gifting, NYE ("zero-proof toast") | NA sparkling, spirits gift sets | Oct–Nov |

### 1.6 Where they advertise (observed)

- **Meta** carries the volume: Moment 239 active ads, De Soi 39, Olipop 44, Ghia 14 [v]. Hooks are text-led statics (offer banners, Reddit-style posts, "us vs them"), testimonials and recipe demos.
- **TikTok and TikTok Shop**: founder stories with a TikTok-Shop-only discount (Ghia 40 % off, Cure "now on TikTok Shop") [m]; Spark-boosted creator recipes; Prime-Day giveaways (Poppi) [m].
- **Amazon** (Liquid Death's Cinnamon Roll Iced Tea "now on Amazon", run as a silent paid TikTok) [m].
- **Retail media**: Target, Circle K, Costco, Sprouts launches drive "find us at" posts (UPDATE at Circle K, Health-Ade Costco) [m]. Some retail media networks treat NA as alcohol (doc 11).
- **Events and OOH**: festivals (Hiyo costumes), Wimbledon (Three Spirit), US Open-style sponsorships, TV (Liquid Death Super Bowl, doc 49).
- **Google Search**: alcohol policy applies to anything that resembles alcohol in Shopping ads (§5.3).

---

## 2. Teardowns: 18 written up, 27 measured

`[m]` = downloaded and measured. **Cut rate** = (cuts + 1) ÷ duration. **Paid?** uses the like-rate signature. LUFS = integrated loudness of the posted file (platforms normalise playback, but a quiet master loses the first second on sound-on feeds, doc 46).

### 2.1 The measured set at a glance [m]

| # | Post | Date · views · like rate | Length · cuts · shots/s | LUFS / peak | Paid? |
|---|---|---|---|---|---|
| D1 | Poppi "organized around the things that matter" (Sour Apple) ([link](https://www.tiktok.com/@drinkpoppi/video/7671002004713491725)) | 2026-08-14 · **14.5M** · 0.54 % · 2,298 shares | 6.2 s · 1 · 0.32 | −12.6 / **+1.1 (clips)** | Yes |
| D2 | Poppi "fridge looking extra crisp" ([link](https://www.tiktok.com/@drinkpoppi/video/7671000699072679181)) | 2026-08-12 · 3.9M · 0.28 % | 10.1 s · 5 · 0.59 | −15.8 / −2.9 | Yes |
| D3 | Liquid Death Energy "gets you chicken wings" ([link](https://www.tiktok.com/@liquiddeath/video/7662786640150088990)) | 2026-07-15 · **4.4M** · 0.05 % | 30.0 s · 9 · 0.33 | −14.0 / **+1.6** | Yes |
| D4 | Liquid Death × Garage Beer "We want your pee" (Jason Kelce) ([link](https://www.tiktok.com/@liquiddeath/video/7675355923765873934)) | 2026-08-18 · **4.6M** · 0.65 % · **12.6K shares** | 89.1 s · 26 · 0.30 | −17.1 / −5.3 | Mixed |
| D5 | Liquid Death "Blood Zero" vampire ([link](https://www.tiktok.com/@liquiddeath/video/7690988314677005598)) | 2026-09-29 · 504K · 0.18 % | 42.9 s · 4 detected (whip-pans hide more) | −16.4 / −0.3 | Yes |
| D6 | Liquid Death "NEW Cinnamon Roll Iced Tea" ([link](https://www.tiktok.com/@liquiddeath/video/7662046156125474079)) | 2026-07-13 · 1.4M · **0.03 %** | 15.0 s · 0 (CG moves) | **no audio track** | Yes |
| D7 | UPDATE "Passion Orange Guava" flavour film ([link](https://www.tiktok.com/@drinkupdate/video/7683563226784599310)) | 2026-09-09 · 30K · 0.89 % | 8.6 s · 6 · 0.81 | −14.3 / −2.4 | Weak |
| D8 | Celsius "powered by pranks pt. 3" ([link](https://www.tiktok.com/@celsiusofficial/video/7686911458776567070)) | 2026-09-18 · 3.6M · 0.49 % | 50.3 s · 38 · 0.78 | −28.8 / −6.4 | Yes |
| D9 | Celsius "consider this a team building exercise" ([link](https://www.tiktok.com/@celsiusofficial/video/7687988327018024222)) | 2026-09-21 · 168K · 2.2 % | 7.9 s · 3 · 0.50 | **−10.3 / +3.7** | Organic |
| D10 | Cann "what happens when you drink Cann" ([link](https://www.tiktok.com/@drinkcann/video/7397501920048336159)) | 2024-07-30 · **2.7M** · 0.24 % | 35.1 s · 3 · 0.11 | −29.8 / −13.0 | Yes |
| D11 | Alani Nu "new summer sip" mocktail ([link](https://www.tiktok.com/@alaninutrition/video/7498456473782029598)) | 2025-04-28 · 2.3M · **7.7 %** | 10.6 s · 3 · 0.38 | −33.0 / −12.5 | Organic |
| D12 | Alani Nu "viral frozen gummy bears" ([link](https://www.tiktok.com/@alaninutrition/video/7617965806000868639)) | 2026-03-16 · 2.3M · 7.7 % · 32.8K shares | 15.9 s · 14 · 0.94 | −23.2 / −12.2 | Organic (metrics identical to D11 in the embed feed: [unverified]) |
| D13 | Moment "Gypsy Rose prison energy drink" (creator weird-drink series) ([link](https://www.tiktok.com/@drinkmoment/video/7371589992260324650)) | 2024-05-21 · 2.0M · **9.7 %** | 89.6 s · 12 · 0.15 | −28.0 / −7.5 | Organic |
| D14 | Spiritless "mocktail summer" Jarritos hack ([link](https://www.tiktok.com/@drinkspiritless/video/7229086314996747566)) | 2023-05-03 · 1.5M · **8.5 %** · 10.6K shares | 16.9 s · 9 · 0.59 | −8.6 / **+2.6** | Organic |
| D15 | Ghia × Courtney Cook snack-plate trend ([link](https://www.tiktok.com/@drinkghia/video/7585010199191178526)) | 2025-12-18 · 1.2M · **7.2 %** | 15.7 s · 12 · 0.83 | −27.9 / −19.0 | Organic |
| D16 | Hiyo "dry january, but make it floaty" ([link](https://www.tiktok.com/@drinkhiyo/video/7592383818921692471)) | 2026-01-06 · **1.1M** · **0.06 %** | 15.0 s · 7 · 0.53 | **−34.4** / −17.9 | Yes |
| D17 | Curious Elixirs "POV: you quit drinking but still love margaritas" ([link](https://www.tiktok.com/@curiouselixirs/video/7271417574531829035)) | 2023-08-26 · 394K · 5.2 % | 13.4 s · 3 · 0.30 | −9.7 / +0.3 | Organic |
| D18 | Curious Elixirs "I'm selective about my chaos" meme ([link](https://www.tiktok.com/@curiouselixirs/video/7595700926946561311)) | 2026-01-30 · 179K · **10.5 %** · 7.7K shares | 22.6 s · 0 | −20.4 / −5.7 | Organic |
| D19 | Ghia founder story + TikTok Shop 40 % off ([link](https://www.tiktok.com/@drinkghia/video/7525226530763574559)) | 2025-07-09 · 223K · 0.98 % | 34.8 s · 26 · 0.78 | −27.8 / −12.6 | Likely paid |
| D20 | Three Spirit at Wimbledon ([link](https://www.tiktok.com/@threespirit/video/7656785852785282326)) | 2026-06-29 · 50K · 1.8 % | 15.1 s · 9 · 0.66 | −25.8 / −8.5 | Organic |
| D21 | Athletic Brewing "What sound does a can make?" (Drake Maye, Dak Prescott) ([link](https://www.tiktok.com/@athleticbrewing/video/7684304924556987662)) | 2026-09-11 · 44.5K · 5.8 % | 18.7 s · 9 · 0.53 | −29.5 / −10.1 | Organic |
| D22 | Brez founder calls a top customer ([link](https://www.tiktok.com/@drinkbrez/video/7527097224178715934)) | 2025-07-15 · 39.6K · 5.6 % | 107.5 s · 0 | −17.0 / +0.6 | Organic |
| D23 | Cure Hydration founder story ([link](https://www.tiktok.com/@curehydration/video/7575182684989820190)) | 2025-11-21 · 112K · 0.54 % | 69.8 s · 17 · 0.26 | −25.8 / −6.6 | Yes |
| D24 | Olipop "a sign for our new flavor" (pomegranate tease) ([link](https://www.tiktok.com/@drinkolipop/video/7691363004079688974)) | 2026-09-30 · 39K · 5.7 % | 7.6 s · 0 | −15.2 / −4.7 | Organic |
| D25 | Hiyo festival "VIP upgrade" costumes ([link](https://www.tiktok.com/@drinkhiyo/video/7626137347293203725)) | 2026-04-07 · 118K · 9.4 % | 7.2 s · 4 | −16.9 / −5.8 | Organic |
| C1 | Mingle Espresso Martini factory BTS (control) ([link](https://www.tiktok.com/@minglemocktails/video/7692863208658423053)) | 2026-10-04 · **300** · 3.0 % | 9.5 s · 9 | −15.1 / −3.3 | — |
| C2 | Ghia "Le Fizz" 5 s product clip (control) ([link](https://www.tiktok.com/@drinkghia/video/7688399565564808462)) | 2026-09-22 · **428** · 2.3 % | 5.1 s · 0 | −24.3 / −9.8 | — |

### 2.2 Full teardowns (shot lists from the 2 fps tiles)

**D1 · Poppi "organized around the things that matter" — 6.2 s, 14.5M, paid.**
- **Shots:** 0–2.5 s locked-off, a home fridge interior at shelf height, door open: Sour Apple cans on every shelf, real green apples, a green bag of Sour Apple candy, the crisper drawer packed with cans. Soft cut (camera nudge) at 2.5 s. 2.5–6.2 s the same frame, closer; a hand enters at the bottom at 5 s and slides one can into the drawer.
- **Hook in second 1:** a colour-coordinated, over-full fridge. Pure visual intrigue, no face, no text.
- **Turn / punchline:** none. The "story" is abundance and order (fridgescaping, a TikTok aesthetic).
- **Product interaction:** placement, not consumption — which is also why it is Meta-safe for any drink.
- **Sound:** a music bed (beat regularity 0.49), loud (−12.6 LUFS) and clipping.
- **Text/CTA:** caption only. **Why it sold:** product in frame 0, colour as the brand, ASMR of order, 6 s loops twice before a viewer decides. **VXO lesson:** a 6 s "fridge-fill" looper per flavour launch is the cheapest high-reach unit in the category, and an AI film can make the *set* but the 60-can wall must come from real pack photos (§4).

**D2 · Poppi "fridge looking extra crisp" — 10.1 s, 3.9M, paid.** A commercial glass-door cooler. 0–0.8 s wide on stacked cans → 0.8–4.7 s a hand restocks the top shelf one can at a time → 4.7–8.7 s three tighter angles of hands filling gaps → 8.7–10.1 s macro of the can rows, label sharp. Music bed. **Lesson:** the same idea in a second location doubles the reach; iterate the *set*, keep the action.

**D3 · Liquid Death Energy "gets you chicken wings" — 30 s, 9 shots, 4.4M, paid.**

| t | Shot (rig) | What happens |
|---|---|---|
| 0–1.2 | Medium, handheld on a roof | A woman cracks a pink can, deadpan |
| 1.2–3.5 | Wide, locked off from the lawn | A white colonial house; she stands on the roof ridge. Super: "DO NOT ATTEMPT. FOR REAL. STAGED PERFORMANCE." |
| 3.5–4.7 | Medium close | She drinks (energy, not alcohol) |
| 4.7–10.3 | Low angle from below, wide lens | She flaps her arms like wings, leans, bends her knees |
| 10.3–14.6 | Same low angle | She leaps up and out of frame; empty sky holds for ~3 s (the gag is the absence) |
| 14.6–17.1 | Top-down drone over the lawn | She lies spread-eagle on the grass, then raises a hand |
| 17.1–23.2 | Medium, kitchen table | A person in a full-body cast with a plate of chicken wings and the can; super "LIQUID DEATH GETS YOU CHICKEN WINGS", then "BUY LIQUID DEATH ENERGY / GET FREE CHICKEN WINGS" |
| 23.2–26.9 | Wide, a row of cast-covered people raise cans | Callback |
| 26.9–30 | Red end card, can | "THE EASY-DRINKING ENERGY DRINK." |

- **Hook:** a can cracked on a roof ridge — wrong place, already in motion.
- **Turn/punchline:** a literal reversal of the leader's slogan ("gives you wings" → you fall, you get chicken wings). **Product-caused** via the promo.
- **Sound:** VO "won't actually make you fly… but who needs to fly when you have wings? Delicious chicken wings" (transcript [m]); music under.
- **Why it sold:** parody of the category king (instant recognition), physical comedy with real weight (the fall is never shown, only before/after), a concrete offer (upload a receipt for wing money). **The fall is solved with coverage and a cut, exactly as doc 41 requires.**

**D4 · Liquid Death × Garage Beer "We want your pee" — 89 s, 26 cuts, 4.6M, 12.6K shares.** A sung musical: Jason Kelce in a bathroom holding a jar of "pee"; a growing crowd marches across a meadow (farmer in overalls, a costumed can mascot, firefighters, a businessman, a mime, an eagle) carrying jars; a post office; a hero jar labelled "DATA CENTER COOLANT — EVERY DROP COUNTS". Transcript: "AI data centers waste millions of gallons of water… We want your pee to cool these data centers" [m]. It is a limited-edition merch drop with an alcohol brand. **Lessons:** (1) **AI is a joke target in drinks culture** — brand-safe creative about AI is satire, not celebration (§9). (2) A co-branded limited drop gives the comedy a purchase reason. (3) The ensemble wide shots read as a real production; whether any frame is generated is [unverified].

**D5 · Liquid Death "Blood Zero" — 43 s, 504K, paid.** A gym; a woman in lilac activewear with blood running from her mouth delivers a deadpan "testimonial": "nothing beats chugging 8 pints of sugary, cholesterol-laden Midwestern dad blood… [but] Blood Zero is just the guilt-free boost I need". Supers carry the facts ("ZERO SUGAR", "UN-EXTREME CAFFEINE", "CRUELTY-FREE RASPBERRY CREAM"). Whip-pans between can close-ups; end card on cream with "EASY-DRINKING ENERGY FOR PEOPLE-DRINKING VAMPIRES." **Lesson:** a parody testimonial that is obviously fictional carries the claims as supers (the FTC fake-review rule does not bite on a vampire, doc 49 §4). Seasonal (Halloween) limited flavour = urgency.

**D6 · Liquid Death "Cinnamon Roll Iced Tea" — 15 s, silent, 1.4M, paid (0.03 %).** Pure CG: the can rises into frame on a cinnamon-brown seamless with "NEW CINNAMON ROLL ICED TEA" → the can tilts and rotates ("BOOST OF CAFFEINE & B VITAMINS") → a cut-glass tumbler of iced tea with sage and cinnamon sticks ("NO ARTIFICIAL SWEETENERS") → packshot with tumbler and a cinnamon roll, "LESS SUGAR.* GREATER TEA." The file has **no audio stream** [m]. **Lessons:** (1) a big brand runs a **silent, text-led product film** at scale — sound-off placements and retail media need a "no-audio" master by design, not as an afterthought. (2) The claims are all facts or comparative with an asterisk. (3) A one-colour world matching the flavour is the entire art direction.

**D7 · UPDATE "Passion Orange Guava" — 8.6 s, 30K (weak).** Chrome can macro with a drop of condensation → orange segment macro → guava slice with suspended droplets → passion fruit with beads → orange segment dripping juice → can pouring clear liquid → wet can macro → three floating packshots on grey. Every frame looks CG or AI-generated (perfect droplets, floating can, impossible pour from an upright can) [inf; AI status unverified]. **Lesson: the "premium fruit-macro flavour film" is the category default and it underperforms** — 30K against the brand's 30K median. It looks expensive and says nothing. This is exactly what founders imagine an "AI product film" is; VXO must show them the alternative.

**D8 · Celsius "powered by pranks pt. 3" — 50 s, 38 cuts, 3.6M, paid.** Handheld office footage at Celsius HQ: an employee "declutters" colleagues' desks (removing monitors, chairs), real reactions, a final reveal. Captions only. Quiet (−28.8 LUFS). **Lesson:** the brand's own staff as a recurring series ("pt. 3") is cheap reach for energy; the product is incidental. VXO does not compete here — but the series logic (a numbered franchise) is the Season-plan argument.

**D9 · Celsius "team building exercise" — 7.9 s, 168K, 2.2 %.** A woman fills a tote bag from the office's branded Celsius fridge, armful after armful, walks off. Mastered hot (−10.3 LUFS, peak +3.7 dBFS: clips). **Lesson:** "the fridge" again (D1, D2): abundance is the joke. And even the category leader posts clipped audio.

**D10 · Cann "what happens when you drink Cann" — 35 s, 2.7M, paid.** Selfie talking head with a can; supers "WHAT HAPPENS WHEN YOU DRINK CANN", "1 CANN = 1 🍷 or 1 🍺", "10–15 MINUTE ONSET", "I'M A 1 CANN GIRL", "THE PERFECT BUZZ WITH NO HANGOVER"; a cutaway pours a can into a jar with ice. Transcript: "with three to four cans you're definitely gonna be giggling a lot more" [m]. **Lesson:** the winning THC format was a **dosing explainer that makes effect claims** — precisely what Meta and Google now prohibit for THC and what the ban will end. A 0 mg successor needs an entirely new creative language (§3.1, insight 2).

**D11 · Alani Nu mocktail — 10.6 s, 2.3M, 7.7 %.** Locked-off kitchen counter: an empty glass → a hand sets the pink can beside it → frozen strawberries and peaches tipped in → the can pours; a **foam cloud rises over the frozen fruit** (real nucleation) → the colour turns deep pink → a straw stirs. Very quiet (−33 LUFS). **Lesson:** one real physical event (the foam bloom) is the whole hook. That event is easy to film and hard for AI (doc 11): **real insert**.

**D12 · Alani Nu "frozen gummy bears" — 15.9 s, 14 cuts, 2.3M, 32.8K shares.** Gummy bears soaked in an energy drink, frozen, served on a plate. **Policy flag:** a candy recipe for a caffeinated product **appeals to minors** (TikTok youth-safety and the 18+ energy rule). Organic is not ads review, but a VXO client film must not copy it (§5).

**D13 · Moment "prison energy drink" — 90 s, 2.0M, 9.7 %.** A creator's "weird drink" series recreates Gypsy Rose's prison recipe (Kool-Aid, Fanta, Jolly Ranchers, coffee) and rates it 8.5. The brand's product is barely present. **Lesson:** the brand account's biggest hit is an **owned recipe-review franchise** riding a news name — reach without product. Useful as organic, useless as an ad.

**D14 · Spiritless "mocktail summer" — 16.9 s, 9 cuts, 1.5M, 8.5 %.**

| t | Shot | Action |
|---|---|---|
| 0–0.9 | Medium, counter, locked | A hand lifts a pink Jarritos bottle with a lime wedge — hook in motion |
| 0.9–4.1 | Same | Chamoy squeezed into the bottle neck |
| 4.1–6.7 | Same | The bottle tipped; Tajín shaken onto the wet neck |
| 6.7–8.7 | Same | A lime squeezed into a glass |
| 8.7–11.2 | Close | Jalisco 55 bottle opened, poured into a shot glass |
| 11.2–14 | Close | A funnel in the Jarritos neck; the shot poured in |
| 14–16.9 | Close | Lime wedge on the rim; hold on the loaded bottle beside the NA tequila |

Loud (−8.6 LUFS), clipping. **Why it sold:** it copies a famous alcoholic hack ("loaded Jarritos") with an NA spirit — **the familiar ritual minus the alcohol**. Product-caused payoff: you can do the thing. **Policy:** organic only; on Meta, "recipes for alcoholic beverages" count as alcohol promotion and a **real soda brand** is in frame (trademark). A paid VXO version uses a generic soda bottle.

**D15 · Ghia × Courtney Cook snack plate — 15.7 s, 1.2M, 7.2 %.** Top-down plate build (purple sweet potato, butter, cream cheese on endive, salmon roe, mac and cheese, scallion) → at 12 s a hand holds the Ghia can to camera → the can pours into a glass of ice, pink foam → the finished plate with the drink. **Lesson:** joining a trend (the "snack plate" of a reality-TV star) and arriving with the product as the last 3 s is how an NA spirit gets organic reach. The drink is the punctuation, not the subject.

**D16 · Hiyo Dry January — 15 s, 7 cuts, 1.1M, paid.** A hand stacks three cases; super "hiyo is 15 % off" → "just in time for dry january" → a thumb lifts the case flap → cans on a table "crafted with adaptogens, nootropics and botanicals" → a can poured into a fluted glass of ice, disco ball behind → "cheers to feeling good and making good choices". Voice VO, **very quiet master (−34.4 LUFS)**. **Lesson:** the paid unit is an offer + a season + one pour, 15 s. "Help you feel your best" is a soft structure/function line; keep it off VXO supers.

**D17 · Curious "POV: you quit drinking but still love margaritas" — 13.4 s, 394K.** Rim a crystal tumbler in salt, add ice, pour Curious No. 2, garnish lime; a hero of the finished drink. Moody wallpaper bar, warm practicals. **Lesson:** a POV line that names the loss ("still love margaritas") converts the curious; the build is pure ritual.

**D18 · Curious "selective about my chaos" — 22.6 s, 179K, 10.5 %.** A relatable caption over **borrowed 1970s TV dance footage**, no product. **Lesson:** the like-rate champion is a meme with no product and an **IP risk** (third-party footage). VXO can make *original* "found-footage-style" meme plates with AI (a fictional 70s dance show), owned outright (insight 8).

**D19 · Ghia founder story — 34.8 s, 26 cuts, 223K, likely paid.** Founder Mélanie on camera: "Here's how I made a viral non-alcoholic spritz… tired of feeling slow and bloated after drinking… 55 versions… you can try them now with our limited time TikTok Shop sale." Cut-ins: a Coke nutrition panel circled, factory floor, hairnet, childhood photos, Mediterranean coast, can towers, pours. **Lesson:** the founder story is the conversion asset; its B-roll is generic. **VXO sells the B-roll layer** (the Mediterranean summer, the first box, the factory) as cinematic inserts into the founder's own talking head — the founder stays real, the world gets bigger.

**D20 · Three Spirit at Wimbledon — 15 s.** POV: a bottle opener pops the cap ("*pop*" super) → Centre Court serve → the crowd → a deadpan friend holding the bottle → the pour into a plastic flute → raised to the court. "non-alc, low sugar, full of active plants". **Lesson:** event POV + one pop sound + a famous place. Real footage only; AI can't fake a real event (and must not).

**D21 · Athletic Brewing "What sound does a can make?" — 18.7 s.** Two NFL quarterbacks imitate a can opening; cut to six real can cracks at tailgates; the last can overflows foam. **Lesson:** the can-open sound is the category's sonic logo; an athlete imitating it is the joke. (NA beer with athletes is fine on Meta only if nobody is shown drinking.)

**D22 · Brez founder calls a top customer — 107.5 s, one take.** The founder phones a repeat buyer on speaker: "I'm a walking billboard… we switched to Brez and cut out drinking for eight months" [m]. **Lesson:** a real customer's voice is the strongest proof in the category and **cannot be AI** (FTC 16 CFR 465). Make the film around it, never instead of it.

**D23 · Cure founder story — 70 s, paid.** "Now in 20,000 stores… on TikTok Shop" [m]. Same pattern as D19.

**Controls.** Mingle's factory BTS (300 views) and Ghia's 5 s "Le Fizz" clip (428) show what a **brand account without a hook** earns: two orders of magnitude below the account's own hits [m].

### 2.3 Cross-ad patterns (what to copy) [m]

- **Second 1 always holds the product in an odd context, already moving:** a can on a roof ridge (D3), a fridge full of one colour (D1), a hand stacking cases (D16), a soda bottle being "loaded" (D14), salt on a rim (D17). The weak posts open on a static product (C2) or a machine (C1).
- **Cut rate follows format:** restock/ASMR 0.3–0.6 shots/s; recipe builds 0.3–0.6; comedy spots 0.3; prank series 0.8; flavour CG 0.8. As in docs 49 and 55, **speed is not the lever**.
- **Length:** paid winners 6–15 s (D1, D2, D6, D16) or 30 s for a narrative parody (D3); organic winners 10–17 s recipes or 60–90 s stories.
- **Nobody sips on the paid NA-spirit posts.** The pour, the glass, the raised glass — never a mouth on the rim (D15, D16, D17, D20). Energy and soda do show drinking (D3, D5), which is allowed because they are not alcohol-adjacent.
- **Loudness is a mess:** 12 of 26 posts with audio are below −24 LUFS (Hiyo −34.4, Alani −33.0) and 6 clip above 0 dBFS (Celsius +3.7, Spiritless +2.6, Liquid Death +1.6, Poppi +1.1) [m]. VXO's −14 LUFS / −1 dBTP master is a visible upgrade (doc 46).
- **The CG/AI flavour film is common and weak** (D7), except when a giant brand pushes a silent one with spend (D6). **A strange idea beats a perfect droplet.**

---

## 3. What converts in this niche (data)

| # | Finding | Number | Source | Status |
|---|---|---|---|---|
| N1 | F&B on Meta: video vs image | Video 51 % of creatives, **27 d** median life (31 d avg); image 49 %, **23 d** (27 d avg); overall 26 d median, 45 % survive 30 d | [Benly F&B Q2 2026](https://benly.ai/benchmarks/q2-2026/food-beverage) | [v] 94K ads, 118 brands |
| N2 | F&B attributes by longevity | **AI-Generated 33 d median, 55 % 30-day survival**; Screen Recording 33 d / 56 %; Infographic 36 d; UGC 26 d / 47 %; **Lifestyle Photography 20 d / 31 %** | same | [v] (ad counts per attribute not shown) |
| N3 | F&B asset top-performance rates | UGC/Organic **61.3 %**, Lifestyle/Editorial 56.6 %, Graphic Design 55.6 %, Product Shot 55.1 %, Branded/Studio 50 %, Motion Design 46.2 % | same | [v] |
| N4 | F&B hooks | Bold Claim 23.9 % of video (27 d), Relatable Situation 12.1 % (27 d, 48 %), Pain Point 9.5 % (24 d) | same | [v] |
| N5 | F&B promo mix | Discount **50.9 %** of promotional intent; free offer 13.8 %; fixed amount off 11.1 %; urgency 7.8 %; bundle 5.6 %; subscribe-and-save 1.4 % | same | [v] |
| N6 | Top-lasting recipe in F&B | UGC × UGC creator × talking head: 16.5× lift, 25 d typical | same | [v] |
| N7 | Moment (adaptogen) Meta | 239 active; ~24 new/week; 20 newest = **85 % image**; top formats Demo 12 %, Press 11 %, Headline 10 % | [Motion](https://motionapp.com/library/moment) | [v] page "4 months" old |
| N8 | De Soi Meta | 39 active; ~8 new/week; **80 % video**; formats incl. ASMR, POV, Skit, Cinematic B-roll | [Motion](https://motionapp.com/library/de-soi) | [v] |
| N9 | Ghia Meta | 14 active; ~3 new/week; 45 % video; formats Offer-First Banner, How-To, Demo, Cinematic B-roll, Social Comments | [Motion](https://motionapp.com/library/ghia) | [v] |
| N10 | Olipop Meta | 44 active; ~11 new/week; 65 % video; top formats **Pattern Interrupt 17 %**, Us vs Them 12 %, Statistic 8 % | [Motion](https://motionapp.com/library/olipop) | [v] |
| N11 | Category stats | NA +19.2 %; NA spirits +62.2 %; NA RTD +92 % | NIQ (§1.1) | Primary |
| N12 | Trial format | Lyre's CEO: "For trial… RTDs are a great entry point"; smaller sizes as lower price entry | [BeverageDaily](https://www.beveragedaily.com/Article/2026/01/29/alcohol-free-drink-trends-sober-curious-consumers-brand-building/) | [c] |
| N13 | TikTok F&B users | 70 % like product-centred content; 64 % love product sounds | doc 49 N8 | Primary |
| N14 | Paid winners measured here | 6–15 s, product in frame 0, one action (restock, pour, CG can) | §2 [m] | Measured |
| N15 | Organic winners measured here | Recipes/hacks 7–10 % like rate; memes 10.5 %; brand films < 1 % | §2 [m] | Measured |

### 3.1 What this means, by sub-niche [inf]

| Sub-niche | Lead format (paid) | Organic engine | Length | Proof type | Offer |
|---|---|---|---|---|---|
| **NA spirits / aperitivo** | The serve as ritual: one strange first frame + a build + the finished glass beside the bottle; or a deadpan "expert fooled" skit | Recipe/hack copies of famous cocktails; trend participation | 10–15 s paid, 20–30 s brand | Taste credibility (awards, bartender endorsements — real only), recipe proof | Discovery set (Ghia 30 % off), Dry-January bundle |
| **RTD mocktails / spritz cans** | Pour-into-nice-glass at a party; hosting/snack-plate frame | Seasonal flavour drops (espresso martini, Halloween) | 6–15 s | The can → glass transformation | Variety pack, first-order discount |
| **Social / adaptogen tonics** | Occasion swap ("the 5 p.m. swap"), Dry January/Sober October unbox-and-pour | Festival POV, founder story | 15 s | Ingredient facts (mg L-theanine) as supers, never moods | Subscription, % off |
| **Hemp-THC → 0 mg lines** | **Not on Meta/Google.** For 0 mg successors: flavour-first, occasion films; no "buzz" language | Founder story about the pivot | 15 s | 0 mg on the label | Bundle (Sober October) |
| **NA beer / hop water** | Game day, the can-crack sound, athletes (real) | Tailgates | 15–20 s | Taste parity | Variety pack |
| **NA wine / sparkling** | Celebration: cork, toast, NYE, Mother's Day | Event POV | 10–15 s | — | Gift set |
| **Energy (DTC)** | Parody of the leader; deadpan physical comedy; flavour-drop "limited" | Mocktail recipes; office/pranks | 15–30 s | mg caffeine, 0 g sugar as supers | Promo (receipt-upload), limited flavour |

**UGC vs cinematic.** UGC/organic wins on Meta in F&B (N3) and recipes win on TikTok (N15). But the **AI-generated attribute lives 33 d** (N2) and lifestyle photography dies at 20 d. The VXO deliverable for this niche is: **a cinematic idea shot in a native frame** (POV, recipe-card layout, deadpan skit), **plus** a 6 s looper, **plus** graphic-design statics from the film's frames (Moment-style static libraries are 85 % of spend).

**AI ads performance and disclosure.** Only D7 in our set looks AI/CG-made, and it was weak; D6 is CG and ran paid with heavy spend. No measured post disclosed AI. Platform labels apply to realistic AI (doc 45 §5.3). Drinks culture mocks AI (D4), so a client's AI film should **not** be about AI; VXO's own spec films can be.

---

## 4. AI realism pitfalls for this niche, and the fixes

Builds on doc 11 (liquid physics, ice, carbonation, ban list), doc 49 §3 (pours, cans, labels, steam) and doc 43 (§1 model table, §5 failure table). **NEW** = not covered before.

| Pitfall | What goes wrong | Fix (prompt / reference / model) |
|---|---|---|
| **NEW: The back-bar problem** | Any "bar" prompt fills shelves with recognisable liquor bottles and labels → the NA ad now depicts alcohol (Meta 21+ alcohol rules) and real trademarks | Clean plate first (doc 43 rule 5): generate the bar **empty**, or with **unlabelled apothecary bottles, books, plants**. Prompt lock: "back-bar shelves hold only plants, books and unlabelled amber apothecary bottles; no wine, beer or liquor bottles anywhere; no readable labels". QC every frame for alcohol cues (§5.5) |
| **NEW: The "intoxicated" read** | Models add swaying, flushed faces, sloppy laughter to "party" prompts; for a functional "buzz" drink that is an effect claim, and on any platform it is "portrayal of intoxication" | Prompt sober behaviour as action: "steady posture, clear eyes, normal speech pace, nobody stumbles or slurs". No "tipsy", "buzzed", "giggly" anywhere. Adults visibly 25+ (TikTok alcohol rule, §5.3) |
| **NEW: Sipping on screen** | Meta: NA allowed "as long as they do not depict… consumption"; AI lips don't seal on rims anyway (LESSONS 2026-10-08) | Never generate a sip for NA spirits/mocktails/beer. Show: the pour, the raised glass, a glass lowered with **the level visibly lower** (state change between cuts), a ring on the napkin. Energy/soda may show a drink, but via a real insert or a profile shot with the can covering the mouth |
| **NEW: Cocktail shaker** | Tins merge into one object; the seal leaks; frost appears instantly or never; ice sound without ice | Two-piece Boston shaker named in the prompt ("a large steel tin and a smaller steel tin pressed together at an angle"). Physics: frost forms on the tin after ~5 s of shaking; shake 10–15 s; one hand on each tin. Shoot shaking as a medium with the tins partly out of frame; the frost close-up as a separate Kling insert from a real photo of a frosted tin |
| **NEW: Clear ice spheres and presses** | AI ice is glass-perfect or melts in the wrong direction | A real ice-press melt takes ~30–60 s; generate only the before/after states with Kling start/end frames (block → sphere) or use a real insert. Prompt "clear ice with a faint cloudy core and two trapped bubbles; one flat facet where it touches the glass" |
| **NEW: Salt and spice rims** | Rim crystals float, drift into the drink, or regrow | Rim built off-camera; show the finished rim. Lock: "coarse salt crust 4–6 mm wide on the outer rim only, crystals stay put". Doc 49 count rule for crumbs applies |
| **NEW: Citrus twist / expressed peel** | Oil mist becomes smoke; the peel bends like rubber | ≤2 s, backlit, "a fine mist of citrus oil droplets catches the light for under half a second" (doc 11). The peel is "rigid, curls once" |
| **NEW: Smoked cocktails** | Dry-ice fog instead of wood smoke; smoke ignores the cloche | Real wood smoke is thin, blue-grey, curls and rises; under a cloche it fills from the top down and pours out sideways when lifted. Prompt exactly that; keep it ≤3 s; never orbit around smoke (doc 49 steam rule) |
| **NEW: NA beer foam** | Head rises from nothing; lacing missing; a glass refills | Head forms only during the pour (2–3 cm on a lager), then settles slowly over 1–3 min; lacing rings stay on the glass after each "sip" state. Use start/end frames; never a continuous level change |
| **NEW: Cork pops (NA sparkling)** | Cork floats, flies in a curve, the bottle refills; foam erupts like a volcano | A cork leaves at roughly 40–50 km/h [unverified], travels straight, is gone in < 0.1 s at 24 fps — show the cork *already gone* and a wisp of vapour at the neck. Foam rises 2–5 cm and stops (it's chilled). Script the cork's fate (doc 43 rule 12) |
| **NEW: Coupes and stemware** | Stems bend, glasses fuse in toasts | Locked camera; a toast cut **before contact**, then a sound; max 4 hands (doc 11). Name the glass type in every prompt (LESSONS: one vessel) |
| **NEW: Can rows and fridge walls** | 60 identical cans: labels drift, flavours swap, extra tabs | AI generates the *set*; **can walls come from a real product photo** composited, or Kling i2v from a photo of the real filled fridge ("labels exactly as the reference; no can changes"). Count lock: "exactly 6 cans per row, 4 rows" |
| **NEW: Vending-machine coils / cooler doors** | Coils spin the wrong way; glass doors show no reflection or show the crew | One coil turn = the can advances one slot; doors reflect a named source ("soft overhead fluorescent reflection, no camera or crew visible"). Camera outside the glass, never through it (LESSONS) |
| **NEW: Energy-drink stunts** | Implies the product enables the stunt (claim) and looks fake | Doc 41 coverage + Liquid Death's device: show before/after, never the impact; permanent super "Staged performance. Do not attempt." Never imply performance, endurance or flight |
| **Labels with ABV / "0.0 %"** | Text drifts; worse, a model writes "40 % ABV" or "proof" on a bottle | Label only from the real pack photo (Kling i2v). "0.0 %" and every mg is a **post super** matching the label. Add to every prompt: "no numbers, no ABV, no proof statements anywhere" |
| Pours, fills, drinks | Liquid from nothing; levels don't drop (doc 11, 41, 49) | Real insert (client phone, 4K60) or hidden transfer ≤2 s; Kling start/end for states |
| Carbonation, condensation, ice clink | Uniform beads; perfect cubes | doc 11 prompts ("uneven beads, two running trails, a dry patch"; "fractured clear ice with trapped air") |
| Garnish drift | Rosemary, mint, berries appear that aren't in the recipe → an ingredient claim | Recipe locked as text: "garnish: one orange wheel and one rosemary sprig only" (doc 49 allergen rule) |
| Faces at parties | > 3 people in focus glitch (doc 43) | Parties as bokeh behind a glass (doc 11 NOCTE grammar); ≤ 3 faces sharp; real talent refs |

**Model routing for this niche** (doc 43 §1 applied; prices doc 43 §6 [EST]):

| Shot type | Model | Settings | Cost per take |
|---|---|---|---|
| Bottle / can / label hero, frosted tin, fridge wall | Kling 3.0 Pro i2v from the real photo | 5 s, `sound:"off"`, `cfg_scale` 0.5, `last_image_url` = same still | $0.48 |
| State changes (block → sphere, full → lowered glass, sealed → popped) | Kling 3.0 Pro i2v start + end frames | 5 s; prompt the path only | $0.48 |
| Sensory one-take (condensation, backlit serve, slow push to the glass) | Cinema Studio 4.0 | `pacing:"single-shot"`, `camera_movement:"dolly-in"`, 720p, 8 s | $3.70 |
| People, skits, bars, parties, multi-shot comedy | Seedance 2.5 r2v | 9:16, 10–15 s, product = first ref, "EXACTLY N SHOTS", clean bar plate | $4.62 / 10 s at 720p |
| Comedic held reveal | Seedance 2.5 r2v, template 7.5 | 8–10 s, last shot ≈ half | ~$3.70–4.62 |
| Previs | Wan 3.0 480p | seed fixed | $0.50 / 10 s |
| Pours, foam blooms, shaking, sips, ice-press melt | **Real insert** | client phone 4K60; VXO grades | $0 |

**Prompt lock block for every NA / functional film** (append to doc 43 §7 POSITIVE LOCKS):
`All adults visibly 25+. Nobody sips on camera; glasses are raised or set down. Steady, sober behaviour; nobody sways, stumbles or slurs. No alcohol bottles, beer taps, wine glasses of wine, or liquor brands anywhere; back-bar holds only plants, books and unlabelled bottles. No numbers, ABV, "proof" or claims in the image; the only readable text is the label in @image1. No driving, no vehicles being operated, no water or heights stunts implied by the product.`

---

## 5. Policy and legal (US first; the client's counsel has the final word)

### 5.1 Platform rules that are specific to alcohol-adjacent products

| Platform | Rule | What it means for a VXO film | Source |
|---|---|---|---|
| **Meta** | NA beverages allowed "as long as they do not depict alcohol or consumption". "Depiction of alcohol brands/logos", "consumption of alcohol beverages" and "recipes for alcoholic beverages" = alcohol promotion; alcohol ads US **21+** | No sipping in NA-spirit/beer films; no alcohol brand in frame; an NA line from an alcohol brand is an alcohol ad; recipe films use only NA ingredients | [Meta alcohol](https://transparency.meta.com/policies/ad-standards/restricted-goods-services/alcohol/) |
| **Meta** | THC banned; CBD needs LegitScript + permission, 18+, no health claims (doc 49) | No THC films; a 0 mg line from a THC brand still needs a clean, THC-free landing page [inf] | doc 49 §4.2 |
| **Meta** | Weight-loss/health products 18+; personal-health policy (doc 49) | GLP-1 hooks ("why people on GLP-1s…") are health targeting; no body or weight imagery | doc 49 |
| **TikTok** | Alcohol ads must not target or appeal to under-age people, **must not feature anyone under 25**, must state alcohol content and a responsible-drinking line; no excessive drinking or intoxication; US alcohol opened to 25+ audiences (2024); market page for 0 % products shows 18+, age-gated landing pages and disclaimers (Argentina example) | Cast 25+ in every NA film; target 21+ (safest); no intoxication; US treatment of 0 % products [unverified] → treat NA as alcohol-adjacent | [TikTok alcohol policy](https://ads.tiktok.com/help/article/tiktok-ads-policy-alcohol), [Marketing Brew](https://marketingbrew.com/stories/2024/08/12/tiktok-allow-alcohol-advertisers-where-are-they) |
| **TikTok** | Energy drinks **18+** in North America (doc 49) | Energy targeting 18+, no school settings or kid-coded candy recipes (D12) | doc 49 |
| **Google** | Alcohol policy rewritten effective **30 Sep 2026**: allow-list structure; mixers allowed to legal-age audiences; **"0 % alcohol advertising application"** required in Egypt, India, Indonesia (violations = suspension); **THC drinks marketed as alcohol-free fall under Dangerous Products**; pregnant people and minors never shown consuming; ABV ≥ 0.5 % shown on landing page; Merchant Center restricts "drinks that resemble alcoholic beverages" | US NA OK with age targeting; Shopping feeds for NA spirits may be restricted; never show pregnancy + drink (Liquid Death's "Kegs for Pregs" would fail on Google) | [Relevant Audience summary of the update](https://www.relevantaudience.com/google-ads-en/google-alcohol-advertising-policy-update-september-2026/), [PPC Land](https://ppc.land/googles-alcohol-advertising-policy-relies-on-two-unchangeable-rules/) |
| **Industry codes** | Beer Institute and DISCUS: advertise only where ≥ **73.8 %** of the audience is 21+ | Clients that are members (or owned by members) will apply it to NA lines | [Mobile Marketing](https://mobilemarketingmagazine.com/tiktok-revises-policy-to-allow-select-alcohol-advertisements/) |
| **All** | AI labels (Meta "AI info", TikTok AIGC) for realistic AI (doc 45 §5.3) | Expect a label on realistic people; disclose | doc 45 |

### 5.2 Labelling words that show up on screen

- **TTB, malt beverages (NA beer):** "non-alcoholic" only with "contains less than 0.5 % (or .5 %) alcohol by volume" **immediately adjacent**; "**alcohol free**" only for **0.0 %**; a "0.0 %" statement requires "alcohol free"; products < 0.5 % can't be called "beer/lager/ale" (they are "malt beverages", "near beer") ([TTB](https://www.ttb.gov/regulated-commodities/beverage-alcohol/beer/labeling/malt-beverage-alcohol-content), [27 CFR 7.65](https://www.law.cornell.edu/cfr/text/27/7.65)). **A VXO super never says "alcohol-free" unless the label does, and "non-alcoholic" travels with "<0.5 % ABV".**
- **NA spirits and wines < 0.5 %** are generally FDA-labelled foods; the same honesty applies: "0.0 %" only if lab-verified [inf]. Never super "proof", "spirit" or "whiskey" in a way the label doesn't (TTB standards of identity may apply to the brand's naming) [unverified].
- **State minor-sale laws:** about **12 states** restrict NA sales to minors to some degree (e.g. Georgia and Idaho by production method; Florida and Kansas by any measurable alcohol; Michigan 18+ for NA beer) ([SAN](https://san.com/cc/should-the-us-implement-age-restrictions-for-nonalcoholic-drinks/), [NPR via KUNC](https://www.kunc.org/npr-news/2024-07-09/id-please-should-kids-be-able-to-buy-nonalcoholic-beer-wine-and-mocktails)). Treat the audience as 21+ by default.

### 5.3 Claims (FTC/FDA/courts) — the lines this niche crosses most

| Claim seen in the wild | Status | VXO rule |
|---|---|---|
| "Hangover-free", "no hangover" (De Soi, Cann, Ghia "but you hate the hangover") | Implied health/effect claim; Google bans health benefits in alcohol-related ads | Super "0.0 %". The hangover never appears as a promise |
| "The perfect buzz", "10–15 minute onset", "mood-boosting", "calm", "helps you unwind" (Cann, Moment, Kin) | Effect/structure-function claims needing substantiation; Feel Free paid **$8.75M** over calm/habit-forming marketing | No effects, moods or onset times on screen. Ingredients with amounts only, sourced from the label |
| "Sleep score", "brain fog", "wine face" (Moment) | Health and appearance claims (Meta personal-health policy) | Not in VXO films |
| GLP-1 targeting | Health-adjacent; FTC scrutiny of GLP-1 marketing generally [unverified] | No GLP-1 words or body imagery; the client may target, VXO doesn't depict |
| "No artificial…", "natural" | Bloom Nu sued over citric acid (doc 49) | Ingredient list, not adjectives |
| Comparative ("It's not a mocktail", "us vs them", Red Bull parody) | Lanham Act §43(a); parody is fine when obviously non-literal | Generic rivals only; never a real competitor's can in an AI frame |
| Energy claims ("power your day") | Puffery if vague; performance claims need substantiation; caffeine mg must match | Super mg as a fact; "Staged performance" on stunts; no minors |
| Energy + minors | Bills in MA (H1908), DE (HB 394 amendment), ME to bar sales to under-18s [unverified status]; England bans > 150 mg/L to under-16s from Apr 2027 (doc 11) | Adults only; no school, gaming-kid or candy cues |
| THC drinks | Federal ban on > 0.4 mg THC per container from **11 Dec 2026**; Meta bans; Google Dangerous Products | VXO does not make THC films. 0 mg successor lines only, after counsel checks the landing page |
| Kratom/kava (Feel Free) | Settlement + state bans (Utah suit 2026) | Do not pitch |
| Fake testimonials (16 CFR 465) | No AI customer verdicts (doc 49) | Brez-style real customer audio only; parody characters make no factual claims |
| Pregnancy | Google: pregnant people never shown consuming alcoholic beverages; Liquid Death's pregnant-shotgun gag worked only because it was water | No pregnancy imagery with NA "spirits" or beer |

### 5.4 IP

- **Borrowed footage** (Curious's 70s TV meme, D18) is a brand-account risk; VXO originals are owned [inf].
- **Real brands in recipes** (Jarritos in D14): fine for a creator's organic post, a trademark problem in a paid AI frame. Use generic bottles.
- **Celebrity likeness** (Kardashians for UPDATE, Kelce for Liquid Death): licensed talent only; no look-alikes (LESSONS).
- **Parody of a leader's slogan** ("gives you wings"): words in a VO are safer than imitating trade dress; never copy the leader's can design.

### 5.5 Pre-flight checklist for this niche (add to doc 45 §5.4, doc 46 §7 and doc 49 §7)

1. **No sip** on screen (NA spirits, mocktails, NA beer/wine); levels change only between cuts.
2. **No alcohol cues:** no liquor/wine/beer bottles, taps or brands in any frame; check backgrounds at 2 fps.
3. **Cast 25+**, visibly; no school, campus or kid-coded props; no pregnancy.
4. **Sober behaviour** in every person (no swaying, slurring, stumbling).
5. **No driving or machinery** in any frame that contains the drink.
6. **Supers are facts from the label:** "0.0 %" (or "<0.5 % ABV" next to "non-alcoholic"), mg of caffeine/ingredients, grams of sugar. No effects, moods, onset, sleep, skin, weight or "hangover".
7. **Disclaimer library** on screen where relevant: "Staged performance. Do not attempt." · "Dramatization." · "Serving suggestion." · "Contains caffeine. Not for children." · "0.0 % ABV."
8. **Targeting note** in the job file: 21+ for NA alcohol-adjacent; 18+ for energy; no THC.
9. **Two masters:** sound-on (−14 LUFS / ≤ −1 dBTP) and a silent text-led master (D6 logic).
10. **Real proof slot** for any taste verdict, customer voice, award or test.

---

## 6. The buyer

### 6.1 Who signs a $1,200–3,500 film

| Brand stage | Who signs | How they buy |
|---|---|---|
| Pre-launch / first retail (< $2M) | **Founder** (often the face: Ghia, Cure, Brez) | Card payment after frames; a Short for the launch or Dry January |
| $2–20M, DTC + regional retail | Founder + **Head of Growth / Brand** (sometimes a fractional CMO) | Creative-testing budget; wants volume (Moment 24/week) → Season |
| Owned by a strategic (HOPWTR→Constellation, Phony Negroni→Wine Group) or > $20M | Brand team + agency + legal | Out of lane except via agencies [inf] |

### 6.2 What they fear (ranked) [inf, grounded in §2–5]

1. **"It will look like a juice ad, or like booze."** NA spirits live between the two: too sweet and they're a mocktail, too boozy and Meta treats them as alcohol. The film has to look adult without looking alcoholic.
2. **Platform rejection.** Their ads get flagged for "alcohol" constantly [unverified but consistent with Meta's wording]. A film that shows a sip or a back-bar bottle can kill an account's NA campaign.
3. **Claims liability.** Feel Free $8.75M, Poppi $8.9M, Olipop and Bloom suits; their own hooks ("hangover-free", "mood") are already on the edge.
4. **AI backlash.** Drinks culture mocks AI (D4); Coca-Cola's AI holidays (doc 11).
5. **Volume.** The heaviest spenders run 8–24 new creatives a week; one film is not a strategy.
6. **Seasonal timing.** Missing Dry January is missing a quarter of the year's NA demand [unverified share].

### 6.3 What proof makes them pay $1,200–3,500

- **5 free frames from their real bottle/can photo**, one of them a **Meta-safe** frame (no sip, no alcohol cues, "0.0 %" super) — answers fears 1 and 2 at once.
- **A pre-flight sheet** (§5.5) attached to the frames: "here is why Meta won't flag this". No competitor offers it.
- **A claims-checked super list** drawn from their label.
- **The pair**: a 15 s paid film + a 6 s looper (D1 logic), plus 6–10 statics for their static-heavy library.
- **Turnaround** against the calendar: "approved frames by 1 Nov, film by 1 Dec, live for 1 Jan."
- **A real-insert plan**: "you film one pour on your phone; we build the world around it."

### 6.4 Re-buy triggers (what makes them rebook monthly)

- **The calendar** (§1.5): Dry January → Valentine's → festival → Mother's Day → summer → Sober October → Halloween flavour → holidays/NYE. Eight natural film slots a year.
- **Flavour and SKU drops:** Lyre's 6 in 60 days, Moment 16, Cann 17, De Soi 4 [m]. Each drop = a 6 s looper + a 15 s film using the locked franchise skeleton.
- **Creative fatigue:** 26 d median life in F&B (N1); statics die at 23 d.
- **Retail launches** (Target, Circle K, Sprouts, Costco): "now at…" films.
- **The THC pivot** (Cann, Brez, Wynk): one repositioning film, then monthly flavour films for the 0 mg line.

### 6.5 Best outreach angle and a sample first DM (never sent)

**Angle:** *"A Dry-January film that Meta won't flag."* Compliment a specific post, name one concrete film idea built on their product truth, and offer frames with the pre-flight built in.

**Sample DM (to an NA-aperitivo founder; NOT SENT — awaiting owner approval):**
> Hi [Name] — your Jarritos-style spritz hack is the best NA recipe post I've seen this year. Film idea for January: a stuffy members' club blind tasting where the expert's monocle drops into your glass at the reveal. I make AI product films (no shoot), checked so Meta doesn't read them as alcohol ads. Want 5 free frames for [Aperitivo] or for [Spritz can]?

(54 words; no link; yes/yes question; follows `vxo-leads` §3.)

### 6.6 Twenty example brand types (no outreach)

1. NA aperitivo/bitter (Ghia-type) 2. NA agave/tequila alternative 3. NA whiskey/bourbon alternative 4. NA gin + tonic RTD 5. Canned spritz 6. Bottled NA cocktails (Curious-type) 7. Espresso-martini-style mocktail cans 8. Adaptogen "social tonic" cans 9. Nootropic "euphoric" tonics 10. Functional nightcaps (sleep wording risk) 11. NA sparkling wine 12. NA still wine 13. Hop water / hop tea 14. Craft NA beer (regional) 15. Former THC brands' 0 mg lines 16. Paraxanthine/"clean" energy 17. Plant-based energy shots 18. Zero-sugar energy with flavour drops 19. Mocktail mixers and syrups 20. Premium glassware/ice kits sold with NA (cross-sell partners)

---

## 7. Lead signals: a niche scoring add-on for `.claude/skills/vxo-leads/SKILL.md`

Apply on top of the base 100-point score. The add-on moves a lead by **−30 to +30**; HOT stays ≥ 70 after the add-on. Public pages only.

| Signal | Points | How to check |
|---|---|---|
| **Calendar window:** 6–10 weeks before Dry January (now → late Nov), Sober October (late Jul–Aug), Mother's Day (Mar), summer (Apr–May), holidays/NYE (Sep–Oct) | **+8** | Today vs §1.5; the brand ran last year's event (archived TikToks, Motion pages) |
| **Static-heavy, high-volume Meta library:** ≥ 20 active ads and ≤ 40 % video (Moment 239 / 15 % video) | **+8** | Motion library page; Meta Ad Library when it loads |
| **SKU velocity:** ≥ 4 new products in 60 days, or a seasonal/limited flavour in the last 30 days | +5 | `https://<store>/products.json?limit=250` `created_at` (Lyre's, Moment, Cann, De Soi, Hoplark, Bloom all qualify today [m]) |
| **THC brand launching a 0 mg / adaptogen line** before 11 Dec 2026 | +6 | Store feed ("0MG", "zero THC"), press |
| **New retail door** (Target, Whole Foods, Sprouts, Erewhon, Circle K, Costco) in the last 90 days | +4 | "Now at…" posts, BevNET PR |
| **Funding or acquisition interest** (seed/Series A, "raising", strategic investor sought) | +3 | BevNET, Dry Atlas, Tracxn |
| **Paid posts that are quiet or clipped** (≤ −24 LUFS or peak > 0 dBFS) — a concrete DM hook | +2 | `ebur128` on one public post |
| **Founder is the face and runs TikTok Shop** (founder-story + Shop-only discount) | +2 | Their TikTok |
| **Current hooks make effect/health claims** ("hangover-free", "mood", "sleep", GLP-1) | **−5** (fixable, but the client may push for it) | Motion page hooks, captions |
| **Core product is hemp-THC with no 0 mg line** | **−20** | Store feed |
| **Kratom, kava-kratom, or other litigated actives** | **−30 (do not pitch)** | Ingredients, ClassAction.org |
| **Energy brand whose content targets teens** (school, gaming-kid, candy recipes) | −10 | Their TikTok |
| Owned by a strategic / big agency of record | −5 | Press |

**VERY hot in this niche looks like** [inf]: a founder-led NA spirit or social-tonic brand, $2–20M, with a Dry-January window open (Oct–Nov), a static-heavy Meta library, ≥ 4 SKUs in 60 days, no THC and no "hangover" headline. Example: base 72 + calendar 8 + static library 8 + SKUs 5 = 93.

---

## 8. Ten ready film concepts (invented brands, VXO spec)

Conventions:
- Invented brands; clear names on USPTO before use; no real-brand look-alikes.
- Otto and Vee appear **only in C10** (VXO's own spec). Any concept can become a VXO spec by casting Otto as the deadpan lead (mouth never visible = no lip-sync risk).
- **Every camera position is a real rig** (tripod, slider, dolly, jib, Steadicam, handheld, top-down arm, hard mount). The camera never passes through glass, walls or vehicles.
- **Meta-safe by default** (§5.5): no sips for NA spirits/beer/wine, no alcohol cues, adults 25+, sober behaviour, facts-only supers. Energy concepts may show a drink only via a real insert.
- Every film ends with the **2-line VO tagline** in a locked voice over a frame with no visible lips, plus the logo card (LESSONS 2026-10-09).
- **Costs** (doc 43 §6 list): Seedance 2.5 r2v 15 s = $3.09 at 480p (proof) + $6.93 × 3 at 720p = **$23.88**; 20 s = $4.12 + $9.24 × 3 = **$31.84**; Kling 3.0 Pro i2v 5 s sound-off $0.48 per take (×2 = $0.95); Cinema Studio 4.0 720p 8 s $3.70; stills ≈ $0.30; ElevenLabs VO ≈ $0.10. Totals exclude the client's real inserts.

---

### C1 · HOLLOWAY 0.0 (NA whiskey alternative) — "Blind" (20 s) ★ BEST 3

- **Idea:** a members' club blind tasting. A tweed-jacketed Master Taster (60s, monocle) noses three tumblers marked A, B, C behind a velvet screen and writes long notes. He taps B: "the finest". The steward lifts the cloth: B is HOLLOWAY 0.0. The monocle drops out of his eye into glass B. Plop.
- **Hook (0–1 s):** ECU of a monocle being screwed into an eye socket, a creak of leather, a crystal tumbler sliding into frame. Strange image, already moving.
- **Punchline (product-caused):** the monocle drop — the shock told by an object, not a face. It only happens because the product fooled the expert.
- **Meta cut:** nobody sips (he noses only); A and C are unlabeled crystal decanters never identified; the reveal shows only HOLLOWAY. The TikTok organic cut can add a VO line "Islay. Eighteen years." before the reveal.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | ECU, locked tripod, 100 mm macro | Monocle in; leather creak |
| 2 | 1.5–4 | Wide, locked, dolly-in 0.5 m | Library, green lamps, three tumblers on a silver tray, velvet screen; back shelves = books only |
| 3 | 4–7 | Medium, slider left→right 30 cm | He noses A, B, C; writes with a fountain pen |
| 4 | 7–9 | Insert, top-down arm | Note card: "B — extraordinary" (post comp text) |
| 5 | 9–11 | Medium close, tripod | He taps glass B twice with the pen; a single nod |
| 6 | 11–13 | Over-shoulder, steward's side | Steward lifts the cloth: the HOLLOWAY bottle (Kling i2v from the real photo) |
| 7 | 13–15 | ECU, locked macro | The monocle falls into glass B: splash ring, it sinks, settles on the ice |
| 8 | 15–17 | Wide, locked | He stares; the steward refills B from HOLLOWAY (bottle tilt only, no level change shown) |
| 9 | 17–20 | End card | Bottle on leather, "HOLLOWAY 0.0 — 0.0 % ABV" + VO |

- **Physics check:** a glass monocle (~10 g) falls ~30 cm in 0.25 s; it hits the liquid with a small crown splash 1–2 cm high and sinks (glass is ~2.5× denser than water), coming to rest on the ice; ripples ring the glass 3–4 times and die within ~1 s. Liquid in B is still before the fall; the level never changes in shot. The library is lit by practicals (2700 K) + a window key; reflections in the crystal show the lamp, not the crew.
- **Audio map:** 0.0 s leather creak + monocle squeak; 1.5 s clock tick, fire crackle; 4–7 s three soft inhales (sniffs) and nib scratch; 9.2 s two pen taps on crystal (bright "tink tink"); 11.2 s velvet rustle; **13.4 s "plop"** (dominant, dry) + ice settle tick at 13.7 s; 15–17 s silence with clock; 17 s VO.
- **VO (locked voice, over shot 9):** `Nobody could tell. [pause] HOLLOWAY. Zero point zero.`
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v 20 s (shots 1–5, 8), clean library plate, 480p proof + 720p × 3 | $31.84 |
  | Kling i2v: bottle reveal (6) + monocle drop start/end (7) × 2 each | $1.90 |
  | Stills (talent sheet, set, tumblers, end card), 10 | $3.00 |
  | **Total** | **≈ $37** |
- **Template:** doc 43 §7.5 (comedic reveal, held beat) extended; Seedance multi-shot "EXACTLY SEVEN SHOTS AND SIX HARD CUTS" for shots 1–5 + 8, then Kling inserts edited in.
- **Claim check:** "nobody could tell" is puffery about a fictional character; do not super "tastes like whiskey" unless the client has blind-test data. "0.0 % ABV" must match the lab sheet.

### C2 · GRIDLOCK (zero-sugar energy, 150 mg caffeine) — "The Spiral" (15 s) ★ BEST 3 · ★ SINGLE BEST

- **Idea:** heist grammar in a dark office at 11:58 p.m. A tired analyst's GRIDLOCK can is stuck on the vending machine coil, hanging over the drop. Three colleagues assemble like a crew: a sticky-note "laser grid" on the glass, a ruler, a desk-lamp "spotlight", a stopwatch-style countdown on a phone. They never rock the machine. At the climax the night guard walks past, presses B4 once; the coil turns; **two** cans drop. He takes one, leaves one, and walks off without a word.
- **Hook (0–1 s):** ECU of a can teetering on a vending coil, lit cold blue; one metallic "tick" as the coil stops. Strange, moving, sound-first.
- **Punchline (product-caused):** the crew's elaborate plan vs the guard's single press; the product is the McGuffin everyone wants, and the guard's quiet theft is the joke (stakes reversal, doc 44 §8.3).

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | ECU, locked macro outside the glass | Can hangs on the coil (Kling i2v from real can photo; "label exactly as reference") |
| 2 | 1.5–3 | Medium, tripod | The analyst presses his forehead to the glass, deadpan |
| 3 | 3–5 | Wide, high corner (security-cam height), locked | Two colleagues arrive with tape, ruler, lamp; office dark, monitors asleep |
| 4 | 5–7 | Insert, handheld | Sticky notes placed on the glass in a grid; a lamp aimed |
| 5 | 7–9 | Low angle, slider | The ruler slid through the flap toward the coil; it's 3 cm short |
| 6 | 9–10.5 | Medium, tripod | The guard enters frame-left, flashlight down, walks past the crew |
| 7 | 10.5–12 | ECU, locked macro | His finger presses B4 once; the coil turns one slot; two cans fall (Kling start/end) |
| 8 | 12–13.5 | Wide, locked (same as 3) | He bends, takes one can, leaves one, exits; the crew frozen |
| 9 | 13.5–15 | End card | Can on a desk, "GRIDLOCK — 150 mg caffeine · 0 g sugar" + "Staged. Don't rock vending machines." |

- **Physics check:** a 355 ml can weighs ~370 g; it hangs because its base rests on the last coil loop. One coil revolution advances each item exactly one slot; the stuck can and the next can both drop ~70 cm into the bin in ~0.38 s and land with a hollow double thunk. A vending machine weighs 300–450 kg; tipping kills people [unverified count] — **nobody touches the cabinet** (and the super says so). The camera is always outside the glass; reflections show the cold front-panel light, not the crew.
- **Audio map:** 0.0 s coil-motor whine stopping + "tick"; 0.3–3 s fridge-compressor hum, an HVAC drone; 3–7 s tape tear, sticky-note pats ×4, lamp click at 6.1 s; 7–9 s ruler scrape; 9.3 s guard's footsteps and key ring; **10.8 s button beep**, 11.0 s coil whir; **11.4 s double thunk**; 12.6 s can pickup; 13.5 s silence → VO.
- **VO:** `It was never stuck. [pause] GRIDLOCK. Zero sugar.` (over shot 9, no lips)
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v 15 s (2–6, 8), "EXACTLY SIX SHOTS AND FIVE HARD CUTS", ≤ 4 people, 480p + 720p × 3 | $23.88 |
  | Kling i2v: shot 1 hang, shot 7 coil turn (start = stuck, end = bin) × 2 each | $1.90 |
  | Stills, 8 | $2.40 |
  | **Total** | **≈ $28** |
- **Targeting/claims:** 18+; mg and sugar from the label; no "keeps you up", no productivity claims; the office is adult (no students).

### C3 · FIELDHOUSE (NA lager, < 0.5 % ABV) — "Shell Game" (15 s) ★ BEST 3

- **Idea:** a neighbourhood bar. A regular sets down three identical pints; a hustler shuffles them like a shell game; a small crowd gathers. The mark points: "That one's the non-alcoholic." The hustler lifts a coaster under each glass: all three coasters read FIELDHOUSE.
- **Hook (0–1 s):** three pints slam onto a wet bar in a row, foam heads wobbling, top-down.
- **Punchline (product-caused):** the game is unwinnable because the product looks identical to beer — the brand's truth made visual.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Top-down arm over the bar | Three pints land; heads wobble |
| 2 | 1.5–3 | Medium, tripod, bartender side | The hustler cracks his knuckles; the mark across, arms folded |
| 3 | 3–6 | Top-down, locked | Pints slide in figure-eights on the wet bar (they glide on the film of water) |
| 4 | 6–7.5 | Wide, Steadicam half-arc 30° | Crowd of 5 leans in (soft background faces) |
| 5 | 7.5–9 | Medium close | The mark points at the middle glass |
| 6 | 9–11 | ECU, locked macro | Each glass lifted in turn: coaster = FIELDHOUSE ×3 (post-comped logo from real coaster photo) |
| 7 | 11–13 | Medium | The mark stares; the hustler slides one pint to him (no sip) |
| 8 | 13–15 | End card | Can + pint, "FIELDHOUSE — non-alcoholic, contains less than 0.5 % alcohol by volume" + VO |

- **Physics check:** a full 16 oz pint weighs ~0.75 kg; on a wet bar it slides 10–20 cm per push and stops; liquid sloshes up the far side (1–2 cm) and settles in ~1 s; the foam head (2 cm) survives gentle slides and leaves lacing; no liquid lost. Back-bar = plants and unlabelled bottles only (no taps with real brands).
- **Audio map:** 0.0 s three glass thumps on wood; 0.2 s pub murmur bed; 3–6 s rhythmic glass-on-wood slides (3 per second), crowd "ooh" at 5.8 s; 7.6 s the mark's finger tap on wood; 9.2/9.8/10.4 s three coaster peels; 11 s single crowd laugh; 13 s VO.
- **VO:** `Pick any one. [pause] FIELDHOUSE. Every one's ours.`
- **Models and cost:** Seedance 15 s (1–5, 7) $23.88 + Kling (6) × 2 $0.95 + stills 8 $2.40 = **≈ $27**.
- **Claim check:** TTB wording on the end card exactly as the label (§5.2); "looks like beer" is shown, not claimed; nobody drinks; cast 25+.

### C4 · MOONWELL (adaptogen sparkling, wine-ritual swap) — "Cellar" (20 s)

- **Idea:** a snobbish collector gives a candle-lit cellar tour: rack after rack of dusty "vintages" (unlabelled, never shown as wine — only bottle silhouettes and chalk numbers). At the last, most precious rack, cans of MOONWELL lie in the bottle slots. He pulls one with reverence; the can is narrower than the slot, so the whole row of cans rolls out after it, clattering across the stone floor.
- **Hook:** a wrought-iron gate creaks open into darkness, candle flame flickering, in second 1.
- **Punchline (product-caused):** a can (66 mm) in a rack built for bottles (~76 mm) — the swap breaks the ritual, literally.
- **Shots (8):** gate open (locked, low) → candle-lit tracking along racks (Steadicam) → his hand dusting a chalk label "'19" (insert) → the precious rack reveal (dolly-in) → he draws one can (Kling, real can) → cans roll out ×12 (Seedance wide, locked) → cans roll to his feet; he holds one up, unbothered (medium) → end card "MOONWELL — 0.0 % · L-theanine [x] mg" (label value).
- **Physics:** 12 cans × 370 g roll on a slight slope at ~0.5 m/s, spreading, bumping, one stops against his shoe; they don't bounce higher than 2 cm; dents none. Candle flames lean toward the open gate.
- **Audio:** 0.0 gate creak; drip echo; footsteps on stone; 12.3 s first can slides, 12.6–14.5 s cascade of 12 rolls (staggered by hand); 15 s a single can stops at his shoe "tock"; VO `A new ritual. [pause] MOONWELL.`
- **Cost:** Seedance 20 s $31.84 + Kling ×2 $0.95 + stills $3.00 = **≈ $36**. **Claims:** no mood words; the ingredient mg only if on the label.

### C5 · BRIGHTCORK (NA sparkling wine) — "Ten Seconds Early" (15 s)

- **Idea:** New Year's Eve living-room party, the TV countdown at 0:15. The host struggles with the NA sparkling bottle; at 0:11 the cork fires, ricochets off the ceiling fan blade and knocks the wall clock's minute hand onto 12. Everyone looks at the clock, sees midnight, and celebrates — the TV in the background still says 0:09.
- **Hook:** "15" on a TV countdown and a thumb pushing a cork, in second 1.
- **Punchline:** the cork (product) causes the early midnight; final beat: the host quietly pours the only glass he's holding, alone in the cheering, deadpan.
- **Shots (8):** TV countdown (locked) → thumb on cork ECU (Kling) → wide room, guests 25+, soft (tripod) → cork already gone, vapour wisp at the neck (Kling state) → ceiling fan blade "tick" insert (locked, low angle) → wall clock: minute hand drops to 12 (Kling start/end) → wide: confetti, hugs, TV still at 0:09 in the corner → end card + VO.
- **Physics:** the cork is never seen in flight (< 0.1 s); only impacts are shown, each a separate cut; a light clock hand (~5 g) can be knocked down by a ~7 g cork; foam rises 3 cm and stops; confetti falls at ~1 m/s, fluttering.
- **Audio:** TV countdown VO "fifteen…"; 4.1 s POP + fan "tick" 4.3 s + clock "clack" 4.5 s (a rapid triple); 5 s silence; 5.6 s cheers; under it the TV still counting "nine…eight"; VO `Midnight. Whenever you like. [pause] BRIGHTCORK.`
- **Cost:** Seedance 15 s $23.88 + Kling ×3 inserts $1.43 + stills $2.40 = **≈ $28**. **Claims:** "0.0 %" super from label; no sips; adults.

### C6 · NULLSET (zero-sugar energy) — "Implosion" (12 s)

- **Idea:** a miniature demolition. On a kitchen counter, a 10-storey tower of sugar cubes stands beside a NULLSET can; a tiny-scale demolition crew grammar: hard-hat camera angles, a detonator plunger (a toy), a countdown. The tower collapses into a heap; the can stands alone. Super: "A typical 12 oz energy drink: ~39 g sugar*. NULLSET: 0 g." (*the client's substantiated generic comparison).
- **Hook:** a hand slams a plunger down in ECU; a siren whoop.
- **Punchline (product-caused):** the can's 0 g is the reason the tower exists and falls.
- **Shots (7):** plunger ECU (locked) → wide "site" with tape and a mini cone (tripod at counter height) → three cube-level inserts with tiny "charges" (macro) → the collapse (Seedance or real insert; locked wide) → dust of powdered sugar settling (Kling) → can alone, condensation bead slides (Cinema Studio single-shot) → end card.
- **Physics:** 39 g ≈ 10 cubes of ~4 g; the tower is 10 cubes high (≈ 16 cm); it collapses downward and outward ≤ 20 cm, sugar dust rises ≤ 5 cm and settles in 1–2 s; cubes chip, never bounce like rubber.
- **Audio:** 0.0 siren whoop + plunger clack; 1.5 s radio chatter "clear!"; 4.0 s three muffled "pops"; 4.3–6 s crumbling cascade; 6–8 s dust settling hiss; 8 s can tick of condensation; VO `All gone. [pause] NULLSET. Zero sugar.`
- **Cost:** Seedance 10 s ($2.06 + $4.62 × 2) $11.30 + Kling $0.95 + Cinema Studio 1 take $3.70 + stills $1.80 = **≈ $18**. **Claim check:** the comparison number needs a source in the job file; generic, unbranded rival (doc 49 Poppi sugar-bag logic).

### C7 · HALCYON (social tonic) — "No Excuse" (15 s) — Dry January

- **Idea:** a house party. A guest is offered drinks three times and dodges with excuses shown as on-screen text bubbles over averted-face close-ups: "antibiotics", "early flight", "marathon (not running it)". The host, deadpan, hands her a HALCYON can. She has no excuse left. Final shot: she's the one now offering cans to others.
- **Hook:** a tray of drinks thrust at the lens, frame 0.
- **Punchline (product-caused):** the product removes the need to explain (Heineken: 81 % think declining without explanation is fine).
- **Shots (8):** tray thrust (handheld POV) → her face 3/4, text bubble 1 (tripod) → tray again, bubble 2 → bubble 3, faster (rule of three) → the host's hand with the can, ECU (Kling) → she takes it; the can tab cracked in profile (real insert) → wide: she walks through the party offering cans → end card "HALCYON — 0.0 % · [ingredients]".
- **Physics:** a tray of 6 glasses tilts ≤ 5°, liquids level; can crack = one vapour puff (doc 49). Party faces in bokeh, ≤ 3 sharp.
- **Audio:** party bed (music replaced in post), 0.0 glass clink; three "pop" text-bubble sounds at 1.6/4.0/6.0 s; 8.4 s can crack (hook-loud); VO `No excuse needed. [pause] HALCYON.`
- **Cost:** Seedance 15 s $23.88 + Kling $0.95 + stills $2.40 = **≈ $27**. **Claims:** no "calm", no "buzz"; the ingredient list only.

### C8 · BRASSHOUSE (NA spirit) — "Sphere" (12 s) — the VXO sensory one-take

- **Idea:** one continuous macro: a rough block of clear ice sits on a copper ice press; the press sinks and the block becomes a perfect sphere; the sphere is lifted into a rocks glass; BRASSHOUSE is poured over it; the camera settles on the glass beside the bottle.
- **Hook:** water hissing off hot-looking copper, the block already slumping, frame 0.
- **Punchline:** a sensory film has no joke; its payoff is the ritual's perfection. Use as the 6–12 s looper and as Dry-January paid unit.
- **Structure:** the press melt is a **real insert** (30–60 s real time, sped ×5) or Kling start/end (block → sphere); then a Cinema Studio single-shot dolly-in for the pour and hold (doc 43 §7.3); the pour hidden as a stream with no level change.
- **Physics:** copper conducts heat ~700× better than ice; the press melts ~1 mm/s at the contact; melt water runs down the channels; the sphere has a faint cloudy core, two bubbles; it sits low in the glass and the liquid rises around it.
- **Audio:** 0.0 hiss + drip; 4.5 s ice-on-glass clunk; 6 s pour; 9 s the ice ticks; VO `Take your time. [pause] BRASSHOUSE.`
- **Cost:** Kling ×2 start/end $0.95 + Cinema Studio 8 s × 2 $7.39 + stills $1.20 = **≈ $10** (+ client real insert).

### C9 · PARADE (energy) — "Halftime" (15 s)

- **Idea:** a stadium tunnel at halftime. The team mascot (an adult performer in a giant foam head and foam mitts) tries to open a can: the mitts can't grip the tab; the foam teeth can't either. A referee jogs past and cracks it without breaking stride. The mascot slides a long bendy straw through the costume's mouth hole and gives a giant foam thumbs-up.
- **Hook:** a giant foam hand slapping uselessly at a can, frame 0.
- **Punchline:** the straw through the mascot's mouth — no lips to sync, the costume is the gag.
- **Shots (8):** foam mitt ECU (locked) → wide tunnel (tripod) → foam teeth attempt (medium) → ref jogs in (Steadicam follow) → crack insert (real or Kling) → straw through mouth hole (medium close) → thumbs-up (wide) → end card "PARADE — 160 mg caffeine" + "Not for children."
- **Physics:** foam mitts are blunt (~5 cm fingers) — they can't fit under a 2 cm tab; the ref's flick is one motion; the can doesn't spray. The mascot performer is an adult; no children in the stadium tunnel.
- **Audio:** 0.0 foam slap ×3; crowd roar muffled through concrete; 6.2 s whistle; 7.0 s can crack; 9 s slurp through a long straw (comic, short); VO `Easy open. [pause] PARADE.`
- **Cost:** Seedance 15 s $23.88 + Kling $0.95 + stills $2.40 = **≈ $27**. **Targeting:** 18+; avoid kid-coded mascot design.

### C10 · VXO spec · Otto & Vee — "Cold Tea" (25 s) ★ (Otto & Vee)

- **Idea:** a 1950s noir bar scene on a soundstage. Otto directs. The actor must down a "whiskey" (prop cold tea) in one take; he grimaces every time. Vee clicks her one silver stopwatch: "Take 41." The prop master swaps in a HOLLOWAY 0.0-style invented spec bottle (VXO's own invented brand, "SPECTRE 0.0"). Take 42: the actor doesn't grimace. Otto lowers his megaphone. Then Otto pours himself one, raises the glass under the moustache; cut; the glass is set down a third lower. Vee stops the watch.
- **Hook:** the clapperboard snaps "TAKE 41" in ECU, frame 0, sound-first.
- **Punchline (product-caused):** the take finally works because the drink is good; Otto's silent pour is the second laugh.
- **Shots (9):** clapper ECU → wide soundstage (dolly) → actor grimace (medium) → Vee's stopwatch in hand, exactly one (insert) → prop master swaps the bottle (Kling, spec bottle) → take 42, actor calm (medium) → Otto lowers megaphone (medium, mouth hidden by moustache) → Otto's glass set down lower (state change between cuts) → end card + VO.
- **Physics/continuity:** one stopwatch only; Otto's mouth never visible, eyes never wide (LESSONS); the glass is the same vessel in every shot; the level drops only between cuts; the soundstage lights are tungsten fresnels on stands (real rig); no camera passes through the bar set's walls.
- **Audio:** 0.0 clapper snap; "Rolling… action" off-screen; 3 s grimace "ugh" (actor off-mic); 5 s stopwatch click; 9 s glass swap clink; 12 s silence of take 42; 15 s megaphone set down; 19 s pour; 22 s stopwatch click; VO (Otto's locked voice) `Finally. [pause] Cut.` — Vee: `SPECTRE zero point zero. Made by VXO.`
- **Cost:** Seedance 25 s (480p $5.15 + 720p $11.55 × 3) $39.80 + Kling ×2 $0.95 + stills $3.00 = **≈ $44**. Organic/portfolio only (it depicts a sip-implied beat; not for a client's Meta account).

### 8.1 Ranking

| Rank | Concept | Why |
|---|---|---|
| ★ 1 (single best) | **C2 The Spiral** | Heist grammar the owner already loves (Red Light), a product-as-McGuffin twist, real physics, ≤ 4 people, no sip, no alcohol cues, a clear energy-brand fit (the largest ad spenders), and a franchise skeleton (the crew returns for every flavour drop) |
| ★ 2 | **C1 Blind** | The NA-spirit founder's core fear answered on screen ("does it taste real?"), told by an object (the monocle) so no face acting or lip-sync is needed; Meta-safe cut built in |
| ★ 3 | **C3 Shell Game** | The cheapest, most native bar film for NA beer; Meta-safe; the truth (it looks like beer) is visual |
| 4 | C10 Cold Tea | VXO's own spec in the category; Otto rules fit perfectly |
| 5 | C5 Ten Seconds Early | NYE/holiday window; cork physics as comedy |
| 6 | C6 Implosion | Cheapest comedy; needs a substantiated comparison |
| 7 | C8 Sphere | The looper and sensory unit; cheapest |
| 8 | C7 No Excuse | Strong Dry-January insight; text-bubble device keeps lips off |
| 9 | C4 Cellar | Great physical gag; long and candle-light is fragile |
| 10 | C9 Halftime | Fun, but mascot design must avoid kid appeal |

---

## 9. Ten surprising insights nobody asked for (that would make VXO better)

1. **The NA buyer is a drinker.** 95 % of NA buyers also buy alcohol (NIQ). Films about "quitting" address the 5 %. Sell **occasions and swaps** ("the 5 p.m. glass", "the toast", "the game") — and the bigger market.
2. **An AI film can turn an NA ad into an alcohol ad.** The default "bar" contains liquor labels; one bottle in the back-bar triggers Meta's alcohol rules (and trademarks). A **compliance-aware clean plate** is a sellable VXO feature in this niche: "We check every frame for alcohol cues." No other AI studio says this.
3. **There is a 63-day market inside a ban.** The THC cliff (11 Dec 2026) forces Cann-type brands to sell 0 mg lines with new language; their winning format (dosing explainers) is now illegal or unadvertisable. They need **a new creative language in weeks** — VXO's speed sells here, but only for THC-free products.
4. **Silence is a format.** Liquid Death ran a 15 s film with **no audio track** to 1.4M paid views [m]. Deliver every drinks film as two masters: sound-on (−14 LUFS) and a silent, text-complete version for retail media, Amazon and sound-off feeds.
5. **The paid unit is six seconds of order.** The year's biggest drinks post we measured is a 6 s locked fridge shot (14.5M). Build a "fridge-fill" template: a client's real can photo × an AI-built fridge set × one hand → one looper per flavour drop, for pennies.
6. **The heaviest spenders buy statics.** Moment: 239 active ads, 85 % images, 24 new a week. VXO's 6–10 stills per film are not a bonus here — they are the larger part of the client's ad library. Price the stills pack explicitly.
7. **The category's sonic logo is the opening sound.** Athletic built a post on QBs imitating a can crack; Three Spirit's caption is literally "*pop*"; Alani's hook is the foam bloom [m]. Design and own each client's **open sound** (crack, pop, ice clunk) as a 0.5 s audio logo mastered at the hook.
8. **Memes without product earn the best like rates — and an IP risk.** Curious's best post (10.5 %) is borrowed TV footage [m]. VXO can generate **original "found footage" meme plates** (a fictional 1970s dance show, a fake infomercial) that brands own outright: an organic offer that costs ~$5 a plate.
9. **Disclaimers are a creative tool.** "DO NOT ATTEMPT. FOR REAL. STAGED PERFORMANCE." let Liquid Death show a roof jump. A pre-written disclaimer library (§5.5) lets VXO pitch bolder action for energy brands without crossing claims lines.
10. **Drinks culture is AI-sceptical.** Liquid Death's biggest summer post mocks AI data centres [m]. A client film should never be "about AI"; the AI is invisible. VXO's own marketing in this niche should lead with taste, speed and the Meta-safe pre-flight, not with "AI".

---

## 10. Gaps and next steps (zero spend)

- **Meta run-lengths are unconfirmed** (Ad Library 403; Motion pages 4 months old). Next: a Motion workspace query (`get_inspo_creatives`) for Ghia, De Soi, Moment, Olipop, Poppi, Celsius, Bloom, Liquid Death, `LAST_90_DAYS`, active, sorted by days running.
- **Several brand TikTok handles were not resolved** (Seedlip, Lyre's, Ritual, Free Spirits, Monday, Gorgie, Zoa, Feel Free). Next run: find handles from each brand's site footer, then repeat the embed → metadata → rank pipeline.
- **TikTok's US treatment of 0 % products** could not be read (the market page is JS-rendered). Confirm via the TikTok Ads Policy Center before any paid NA campaign.
- **Revenue for most brands is [unverified].** Fill per dossier when a brand becomes a lead.
- **Dry January participation and share of annual NA sales** are [unverified]; a NIQ/Circana weekly trend for January would size the window.
- **Web search budget** ran out mid-session; follow-ups worth a search: NAD decisions on NA/adaptogen claims (2025–2026), the Beverage Regulatory Parity Act's status, and any 2026 AI-made beverage campaigns with performance data.

---

## Sources

**Market and industry:**
- NIQ US BevAl 2025 Year in Review: https://develop.nielseniq.com/global/en/wp-content/uploads/sites/4/2026/01/NIQ-US-BevAl-2025-Year-in-Review_5780f6.pdf
- Shanken (NA spirits 2025): https://www.shankennewsdaily.com/2025/08/15/38096/non-alcohol-spirits-gaining-traction-in-the-u-s/ · BeerNet on NIQ: https://beernet.com/wsd/wsd-article/niq-on-the-billion-dollar-non-alc-growth-engine/ · drinksint: https://drinksint.com/news/fullstory.php/aid/11598/.html
- IWSR via Fox: https://www.fox13news.com/news/beyond-dry-january-rise-non-alcoholic-drinks-adult-beverage-market · drinks-intel: https://drinks-intel.com/cross-category/no-alcohol-segment-expected-to-post-us4bn-growth-by-2028-category-intel/
- Gallup 2025: https://news.gallup.com/poll/693362/drinking-rate-new-low-alcohol-concerns-surge.aspx
- BeverageDaily, 5 lessons (Jan 2026): https://www.beveragedaily.com/Article/2026/01/29/alcohol-free-drink-trends-sober-curious-consumers-brand-building/
- Brightfield hemp statement: https://blog.brightfieldgroup.com/brightfield-statement-on-hemp-derived-thc-ban · Shanken THC cases: https://www.shankennewsdaily.com/2026/07/21/40269/hemp-thc-drinks-reached-1-6-million-cases-on-triple-digit-growth-in-2025/ · Whitney Economics: https://www.whitneyeconomics.com/press-detail/whitney-economics-issues-u.s.-cannabis-and-hemp-beverage-report-thc-beverage-sales-top-%241.1b
- Hemp ban delay: https://www.marijuanamoment.net/trump-signs-bill-to-delay-hemp-thc-product-ban-giving-lawmakers-more-time-to-craft-regulations-instead-of-prohibition/ · https://harris-sliwoski.com/es/cannalawblog/the-intoxicating-hemp-products-ban-was-delayed-a-month-now-what/ · https://www.pbs.org/newshour/politics/what-to-know-about-the-looming-federal-ban-on-thc-infused-drinks-and-snacks
- Celsius Q3 2025: https://ir.celsiusholdingsinc.com/news/news-details/2025/Celsius-Holdings-Reports-Third-Quarter-2025-Financial-Results/default.aspx
- Deals: https://www.cbrands.com/blogs/press-releases/constellation-brands-announces-agreement-to-acquire-non-alcoholic-brand-hopwtr · https://www.thewinegroup.com/the-wine-group-acquires-phony-negroni-non-alcoholic-brand/ · https://www.prnewswire.com/news-releases/the-zero-proof-acquires-the-new-bar-creating-one-of-the-most-comprehensive-brand-and-distribution-platforms-in-adult-non-alcoholic-beverages-302809453.html · https://bevnet.com/pr/2026/04/28/neutonic-raises-6m-at-a-60m-valuation-to-accelerate-global-expansion-across-retail-and-new-markets · https://www.parkstreet.com/roundup-of-mergers-and-acquisitions-in-2026-so-far/
- Funding: https://tracxn.com/d/trending-business-models/startups-in-non-alcoholic-spirits/___fXkqrUrvwLfHBw9J-jq0_VlquUj2qqijta7sIbYJiY · https://finder.techleap.nl/news/feed/moment-secures-5m-from-btomorrow-ventures · https://www.fooddive.com/news/functional-non-alcoholic-spirits-brand-aplos-raises-55m/651771/
- Founders to watch: https://www.dryatlas.com/articles/15-emerging-non-alc-founders-to-watch-in-2026/

**Creative benchmarks:**
- Benly Q2 2026 F&B: https://benly.ai/benchmarks/q2-2026/food-beverage
- Motion libraries: https://motionapp.com/library/ghia · https://motionapp.com/library/de-soi · https://motionapp.com/library/moment · https://motionapp.com/library/olipop (also /poppi, /celsius, /bloom-nutrition, /liquid-death)
- TikTok posts: every link in §2.1 (measured 2026-10-09; files in `scratchpad/niche2/drinks/`, not committed)
- Shopify feeds: `https://<store>/products.json?limit=250` for the 35 stores in §1.3 (2026-10-09)

**Policy and law:**
- Meta alcohol policy: https://transparency.meta.com/policies/ad-standards/restricted-goods-services/alcohol/
- TikTok alcohol policy: https://ads.tiktok.com/help/article/tiktok-ads-policy-alcohol · market-specific page: https://ads.tiktok.com/help/article/alcohol-market-specific-requirements · Marketing Brew: https://marketingbrew.com/stories/2024/08/12/tiktok-allow-alcohol-advertisers-where-are-they · Mobile Marketing: https://mobilemarketingmagazine.com/tiktok-revises-policy-to-allow-select-alcohol-advertisements/
- Google alcohol policy update: https://www.relevantaudience.com/google-ads-en/google-alcohol-advertising-policy-update-september-2026/ · https://ppc.land/googles-alcohol-advertising-policy-relies-on-two-unchangeable-rules/ · https://support.google.com/adspolicy/answer/6012382 · https://support.google.com/merchants/answer/6150139
- TTB malt beverage alcohol content: https://www.ttb.gov/regulated-commodities/beverage-alcohol/beer/labeling/malt-beverage-alcohol-content · 27 CFR 7.65: https://www.law.cornell.edu/cfr/text/27/7.65
- NA sales to minors: https://san.com/cc/should-the-us-implement-age-restrictions-for-nonalcoholic-drinks/ · https://www.kunc.org/npr-news/2024-07-09/id-please-should-kids-be-able-to-buy-nonalcoholic-beer-wine-and-mocktails
- Feel Free / Botanic Tonics: https://bevnet.com/pr/2024/09/18/botanic-tonics-reaches-settlement-agreement-in-class-action-lawsuit-reaffirms-commitment-to-industryleading-standards · https://utahnewsdispatch.com/2026/04/07/maker-of-feel-free-tonics-sues-utah-kratom-regulations/ · https://fortune.com/2025/12/28/kratom-drink-feel-free-fda-supplements-labeling-lawsuit/
- Energy-drink minor bills: https://malegislature.gov/Bills/194/H1908.Html · https://www.wdel.com/news/delaware-bill-targets-sales-of-energy-drinks-to-minors/article_f560b899-bbd0-584f-b626-2a16a42e11f9.html
- Earlier docs relied on: 11 (beverages, NA spirits), 41, 43, 44, 45 §5, 46, 49 §4 (Poppi, Olipop, Bloom, Celsius, energy 18+, CBD/THC on Meta).
