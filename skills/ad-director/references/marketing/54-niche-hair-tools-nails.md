# 54 — Niche deep-dive: hair tools, haircare and nail products

Researched 2026-10-09. No generation money was spent. Nobody was contacted. Nothing was sent.

**What this adds.** Doc 11 §4 covers the haircare *look*: the swish, the strand macro, the shine band, the "hangs by a thread" metaphor and a style header. Doc 47 covers skincare and makeup. It touches haircare only in passing (C5 "Steam Room" with mannequin heads, and the "no AI hair growth" rule). Neither doc covers **heated hair tools** or **nails**. Neither has measured hair or nail ads. This doc adds:
- 31 measured hair and nail TikToks (18 teardowns in full);
- Meta creative-volume data for 28 brands in the niche;
- the conversion data that is specific to this category;
- the AI traps that are specific to hair, heated tools, hands and nails;
- the policy cases that already hit this niche (*Dyson v. Dreame* 2026, Shark "fastest blowout" 2026, Shark "frizz-free" 2022, the EU TPO ban);
- the buyer and a lead-scoring add-on;
- 10 concepts.

It builds on 41 (action realism), 42 (teardown method), 43 (models, prices, templates), 44 (comedy craft), 45 (what sells, policy cheat-sheet), 46 (sound and QC) and the LESSONS file. It does not repeat them.

**Labels.**
- **[m]** = I measured it from the downloaded file: scene cuts with ffmpeg at threshold 0.3, 2 fps frame tiles that I looked at, a 0.5 s RMS envelope, integrated LUFS and true peak, and a faster-whisper transcript.
- **[c]** = the brand's or platform's own claim.
- **[v]** = a vendor or agency figure. Treat it as directional.
- **[inf]** = my inference.
- **[unverified]** = no primary evidence found.

**Method and limits.**
- **TikTok.** Downloads worked. Profile listing did not: `yt-dlp` returned a JSON error on every `@brand` page. So account medians are missing, and every URL came from a web search restricted to tiktok.com. I pulled 50+ candidate URLs, read their metadata (views, likes, shares, length, date), and downloaded the 31 strongest and most instructive to `scratchpad/niche2/hair/`. No media is committed.
- **Paid vs organic.** I use the doc 47/49 proxy. Millions of views with a like-rate under about 1 % means paid distribution (Spark Ads). A like-rate of 3 % or more means an organic hit. This is a flag, not a fact.
- **Meta Ad Library** returned HTTP 403 to automated fetches. The **Motion Inspo Library** public pages (motionapp.com/library/<brand>) are the proxy for Meta activity: active ads, new creatives per week and format mix. Those pages say "refreshed 4 months ago", so read the counts as a snapshot from about June 2026.
- **The Motion MCP** returned no workspace, so there is no Motion performance data.
- **The two-year window** runs from Oct 2024 to Oct 2026. 18 of the 31 measured posts fall inside it. I kept 13 older ones (2023 to mid-2024) because they are the formats the newer winners copy, and each one is marked "older".

---

## 0. The ten things to know before pitching a hair-tool, haircare or nail brand

1. **This niche is a creator-demo niche, and brand-made polish loses.** About 25 of the 31 measured posts are a person on camera demonstrating. The two brand-made "cinematic" posts in the set flopped next to creator content on the same product. Shark's SilkiPro launch montage (19 cuts in 8.8 s) got **43K** views [m]. Glamnetic's brand-shot "car runs over our press-ons" test got **7.9K**. A creator's kitchen "apple test" of press-ons got **2.3M** [m]. **VXO must not pitch "replace your UGC".** Pitch "**a cinematic hook and world bolted onto the UGC you already have**" (§8, insight 1).
2. **Paid winners here run long, unlike beauty.** Paid-scaled posts (≥300K views, like-rate under 1 %) run **5.6–67 s, median ≈43 s** (n = 8) [m]. Examples: RevAir 46 s (26.3M), K18 60 s (4.7M), amika 41 s (15.3M), Bondi Boost 41 s and 67 s. A tool needs *process time*. Doc 47's skincare paid winners had a median of 11 s. The only short paid exception is Gisou's 5.6 s POV gag (its 6.2 s twin was an organic hit). **VXO's 15 s film is a hook-and-world module, not the whole ad.**
3. **The strongest second-1 hooks show the category's failure, already happening.**
   - A thermal brush **tangled in hair**: "oh no, why is it stuck" (Wavytalk creator, 6.2M, 3.1 % likes) [m].
   - **A press-on popping off a finger** (Glamnetic PAS ad, 525K) [m].
   - **A vacuum brush-roll wrapped in shed hair** (Bondi Boost, 327K paid) [m].
   - **A weird device already sucking hair in** (RevAir, 1.0M and 26.3M) [m].

   Failure-in-frame-0 is the niche's native hook, and AI can stage it without showing any result.
4. **Proof in this niche is a person, a clock and a real result.** The proof devices that recur in the measured ads:
   - an on-screen clock: RevAir's "12:39", Shark's "that literally took me three minutes";
   - a half-and-half split: RevAir's "this side is dry, the other side is dripping wet"; Shark's "look how straight that made my hair compared to this side";
   - an ordeal: an apple, a can tab, running water, a car tyre;
   - days of wear: "nine days", "over two weeks".

   **AI can never supply this proof** (LESSONS; FTC mock-up doctrine; §5). Every VXO film keeps a **proof slot** filled with the client's real footage.
5. **The picture is the claim, and this niche already has the case law.** In *Dyson v. Dreame* (NAD, 2026-08-07) models with hair *longer than shoulder length* contradicted a "dries shoulder-length hair in two minutes" claim, and "a disclosure cannot contradict or be used to cure an unsupported message." Shark changed "fastest blowout" after a Dyson challenge (2026). It was told to drop "frizz-free / no frizz" in 2022. **On screen, hair length, hair type, drying time and temperature must all sit inside the client's tested spec** (§5).
6. **Hair is the hardest material for the models, and nails are a hands problem.** The safest AI shots in this niche are **the world, the props, the tool as an object, and the joke**. The hair *result* and the nail *result* come from real footage (§4). That maps exactly onto point 4: AI makes the hook and the turn, the client's footage makes the proof.
7. **Hair tools and nails are volume games, and founder-led brands are far behind.** New Meta creatives per week (Motion snapshot):

   | Brand | New creatives per week | Active ads |
   |---|---|---|
   | TYMO | ~688 | 4K |
   | Kitsch | ~173 | 1K |
   | Switch Nails | ~79 | 615 |
   | Prose | ~41 | — |
   | Glamnetic | ~37 | 449 |
   | Static Nails | ~3 | — |
   | Nailboo | ~7 | — |
   | JVN | ~5 | — |
   | K18 | ~5 | — |

   **The founder-led gap is exactly what the $3,500/mo Season tier fills.**
8. **Haircare advertising is discount-led and graphic-led.** Benly's Q1 2026 haircare benchmark (4.7K Meta creatives, 23 brands) [v]:
   - **63 % of creatives carry a discount**, rising from 57 % to 69 % across the quarter;
   - **Graphic Design scores highest on effectiveness (74)**, UGC 67, Branded/Studio 65, **plain product shots lowest (44)**;
   - **before/after hooks are only 0.1 % of videos but live 1.9× longer than average.**

   Deliver every film with **swappable offer end-cards** and a **graphic-design cutdown**.
9. **TikTok Shop is a real channel for this niche.**
   - Haircare on US TikTok Shop: **$401M in 12 months, +118 %** [v, Charm.io via Beauty Independent].
   - Wavytalk was a **top-5 TikTok Shop beauty storefront: $15M in Q1 2026**, with one bundle at $4.7M.
   - Nails rose with makeup **+24.9 %** over BFCM 2025 [v, NIQ].

   A second buyer exists inside these brands: **the TikTok Shop / affiliate manager**, who needs "seed" videos for affiliates to copy.
10. **Words to fear, by sub-niche.**

    | Sub-niche | Words to fear | Why |
    |---|---|---|
    | Haircare | "grows hair", "regrowth", "stops hair loss / shedding", "thicker hair" (as growth), "repairs" (as a medical claim), "treats dandruff" | FDA drug claims; TikTok bans "treat hair loss" |
    | Hair tools | "no heat damage", "frizz-free", "fastest", "dries in X min" (with longer hair on screen), "salon results" (if uncontrolled) | NAD cases |
    | Nails | "non-toxic", "damage-free" (unqualified), "TPO-free" (only if true), "car-accident proof", "waterproof" (for wear claims), "lasts 30 days" (unless tested) | — |

---

## 1. Market map

### 1.1 Size and growth (US unless stated)

| Segment | Number | Source | Status |
|---|---|---|---|
| Prestige haircare, 2025 | **+8 %**, the fastest prestige category (fragrance +5, makeup +4, skincare +3) | Circana via [Beauty Independent](https://www.beautyindependent.com/haircare-prestige-beauty-hottest-category/) | [c] Circana |
| Prestige haircare, H1 2025 | **$2.3B, +6 %**; scalp care **+19 %**; styling up double digits | Circana via [BeautyMatter](https://beautymatter.com/articles/us-beauty-industry-grows-in-h1-2025) | [c] |
| Prestige haircare buyers | 34 % aged 55+; 66 % earn >$100K; salon brands ≈70 % of prestige hair; clean ≈18 %; celebrity hair doubled but is 3 % | Circana via Beauty Independent (above) | [c] |
| Mass hair | Hair is the largest piece of mass beauty; mass hair +4 % in H1 2025 | Circana via BeautyMatter | [c] |
| TikTok Shop haircare | **$401.1M in 12 months to Jun 2026, +118 %**; TikTok Shop beauty overall $980M in Q2 2026 | Charm.io via [Beauty Independent](https://www.beautyindependent.com/tiktok-shop-nears-1b-beauty-sales-second-straight-quarter/) | [v] |
| TikTok Shop hair tools | Wavytalk **$15M in Q1 2026** (No. 5 beauty storefront), Blowout Boost Bundle **$4.7M**; No. 9 in Q2 | Charm.io via [Beauty Independent](https://www.beautyindependent.com/?p=188868) | [v] |
| TikTok Shop BFCM 2025 | Haircare **+32.5 %** (styling led; **tools and colour declined**); makeup + nails **+24.9 %** | NIQ via [Beauty Independent](https://www.beautyindependent.com/?p=180109) | [v] |
| Hair tools (global) | ≈$5.0B in 2025 → $6.97B in 2032 (5 % CAGR); multi-stylers are the fastest segment (≈7.5–7.8 % CAGR); Dyson ≈17 % of dryers | QYResearch / GMI summaries | [v] low quality, estimates disagree |
| SharkNinja "Beauty & Home Environment" | **$826.3M in 2025, +45 %** (fans, purifiers and face masks drove it; hair not broken out) | [SharkNinja 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm) | [c] audited |
| Press-on nails (global) | $0.7B (Grand View 2023) to $1.8B (Marketintelo 2025); 6.5–7.2 % CAGR. Estimates disagree by 10×, so trust the growth rate, not the size | [Cosmetics Business](https://cosmeticsbusiness.com/press-on-nails-are-having-a-sustainable-makeover), [Fortune BI](https://www.fortunebusinessinsights.com/de/press-on-nails-market-117086) | [v] |
| Nail leader | KISS ≈**$456M** in glue-on + press-on (2022, Circana via CEW) | [CEW](https://cew.org/?p=92953) | [c] dated |
| Social interest | "Press-on nails" social video views **+119 %** (Traackr) | Cosmetics Business (above) | [v] |
| Olive & June | Bought by Helen of Troy for $225M + $15M earn-out (Dec 2024); contributed **$26.8M / $33.4M / $37.7M** in HELE's FY26 Q1–Q3 | [HELE Q3 FY26 release](https://s2.q4cdn.com/117307772/files/doc_financials/2026/q3/Helen-of-Troy-Limited-Reports-Third-Quarter-Fiscal-2026-Results-2026.pdf), [DC360](https://www.digitalcommerce360.com/2024/11/25/helen-of-troy-acquires-olive-june/) | [c] |

**Read-out [inf].**
- Haircare is the hottest prestige category, and the growth sits in **treatments, scalp and styling**. Those are claim-heavy, which matters for compliance (§5).
- Hair *tools* are a mature market. Growth sits in multi-stylers and cheap high-speed dryers sold on TikTok Shop and Amazon.
- Nails are moving from salon to **DIY systems** (press-ons, gel strips, home gel kits, dip kits) and into mass retail (Target, Walgreens, Ulta). That is a launch-content machine.

### 1.2 Thirty brands (founder-led and $1–20M where evidence allows; benchmarks marked)

Revenue bands are **estimates**. "Est." means a third-party model (Growjo, ZoomInfo, Grips, Prospeo). Treat those as ±50 %. Nothing here is a target list. Leads go through `vxo-leads` with a dossier.

| # | Brand | Sub-niche | Founder / leader | Size signal | Meta activity (Motion) | Note |
|---|---|---|---|---|---|---|
| 1 | **RevAir** | Reverse-air dryer | Debra Isaacson (founding partner, co-inventor) | Est. ≈$6M ([Growjo](https://growjo.com/company/RevAir)) [unverified] | — | **26.3M-view paid TikTok, Jan 2026** [m]; strange device = curiosity hook |
| 2 | **TYME** | Iron (curl + straighten) | Jacynda Smith (stylist-founder) | Est. <$5M ([ZoomInfo](https://www.zoominfo.com/c/tyme/351827449)) [unverified] | — | Founder-stylist story |
| 3 | **Bondi Boost** | Scalp/haircare + infrared tools (AU, US DTC) | Founders (AU) | [unverified] | **57 active, ~27/wk**; Demo 27 %, Before/After 14 % | Runs growth-adjacent claims (§5 red flag) |
| 4 | **L'ange Hair** | Hot tools + styling | Founder-led [unverified] | Likely >$20M [unverified] | — | Heavy creator #langepartner program |
| 5 | **Hairitage** | Haircare + tools (Walmart) | Mindy McKnight (creator-founder) | [unverified] | — | Creator-founder; mass retail |
| 6 | **Kitsch** | Heatless curlers, accessories, haircare | Cassandra Thurswell | Large (benchmark) | **1K active, ~173/wk** | Licensed Grinch collab; volume benchmark |
| 7 | **Crown Affair** | Prestige haircare + tools (combs, brushes) | Dianna Cohen | $8M (2023) → ≈$20M (2024) → $30M target 2025 ([Modern Retail](https://www.modernretail.co/operations/how-crown-affairs-ceo-took-the-brand-into-sephora-and-beyond-to-capture-more-of-hair-cares-market/)) | — | Series C 2026; "ritual" brand |
| 8 | **Ceremonia** | Latinx heritage haircare | Babba C. Rivera | $2M seed 2021 [c] | — | Founder-led; Sephora |
| 9 | **Bread Beauty Supply** | Curly/textured haircare | Maeve Reilly | [unverified] | — | Founder-led |
| 10 | **Rizos Curls** | Curly haircare | Julissa Prado (bootstrapped) | "multi-million" [c]; est. $10–25M [v] | — | Amazon + Target |
| 11 | **Arey** | Grey-hair care | Leah Ferrari | [unverified] | — | Growth-adjacent claims risk |
| 12 | **Act+Acre** | Scalp care | Helen Reavey | [unverified] | — | Scalp = fastest prestige subsegment |
| 13 | **Fable & Mane** | Ayurvedic haircare | Akash & Nikita Mehta | [unverified] | — | Sephora |
| 14 | **Jupiter** | Scalp / dandruff-adjacent | Founders | [unverified] | — | Dandruff = drug claim (§5) |
| 15 | **Divi** | Scalp serum | Dani Austin | ≈$40M first year [c] ([Dallas Innovates](https://dallasinnovates.com/dallas-based-scalp-hair-health-brand-divi-snags-minority-investment-from-california-vc-firm/)) | **187 active, ~15/wk**; Headline 21 % | Above the band (benchmark) |
| 16 | **Gisou** | Honey haircare, hair perfume | Negin Mirsalehi | Above the band [inf] | **47 active, ~10/wk**; Offer banner 16 % | Best POV gag in the set [m] |
| 17 | **Vegamour** | "Hair wellness" | Founder-led | Above the band [unverified] | 41 active, ~6/wk | Claims risk |
| 18 | **Static Nails** | Reusable pop-on nails | Alexis Irene | $500K in its first 6 months, then +89 % YoY ([Glossy](https://www.glossy.co/beauty/how-static-nails-hopes-to-carve-out-a-niche-in-the-9-billion-nail-market)); est. ≈$0.85M/mo online, Sep 2024 ([Grips](https://gripsintelligence.com/insights/retailers/staticnails.com)) [v]; AOV $50–75 | **~3/wk**; Headline 22 % | 7 % online conversion, 57 % repeat [c] |
| 19 | **Mooncat** | Indie polish (magnetic, holo, glow) | Michelle Lin | Est. ≈$2.6M ([Prospeo](https://prospeo.io/c/mooncat)) [unverified] | — | Collector drops |
| 20 | **Holo Taco** | Indie polish | Cristine Rotenberg (creator-founder) | "millions of bottles" [c] | — | Creator-led |
| 21 | **Le Mini Macaron** | Gel kits, mini polish | Christina Kao (co-founder) | Self-funded; 30+ markets [c] | — | Target, Ulta |
| 22 | **Nailboo** | Dip-powder kits | Raz Romanescu | "mid-to-low eight figures" (2024, [Modern Retail](https://www.modernretail.co/operations/nailboo-is-tripling-its-presence-in-walmart-amid-an-at-home-nail-care-boom/)) [c] | **21 active, ~7/wk**; Demo 26 % | Walmart expansion |
| 23 | **Chillhouse** | Press-ons + polish | Cyndi Ramirez | [unverified] | **112 active, ~16/wk** | Target, CVS |
| 24 | **ManiMe** | Custom-fit gel stickers | Founders | [unverified] | — | Phone-scan fit tech |
| 25 | **Paintbox** | Nail art + polish | Founder-led [unverified] | [unverified] | — | — |
| 26 | **Gelcare** | Home gel | Founder-led [unverified] | [unverified] | — | TPO-free messaging opportunity (§5.4) |
| 27 | **Olive & June** | Polish, gel, press-on systems | Sarah Gibson Tuttle (now Helen of Troy) | ≈$98M over 3 HELE quarters [c] | **163 active, ~27/wk**; Demo 28 % | Benchmark: Mandalorian collab |
| 28 | **Glamnetic** | Press-ons | Ann McFerran | ">$100M a year" (Shopify Masters, Apr 2026) [c] | **449 active, ~37/wk** | Benchmark; founder on camera |
| 29 | **Wavytalk / TYMO / Laifen** | Mass tools (China-based) | Corporate | Large | TYMO **4K active, ~688/wk** | Benchmarks only; not founder-led buyers |
| 30 | **Dyson / Shark** | Premium tools | Corporate | Very large | Dyson 57 active, Offer 28 %; Shark 43 active, Demo 34 % | Benchmarks; NAD fighters |

### 1.3 Price bands

| Band | Hair tools | Haircare | Nails |
|---|---|---|---|
| Mass | $20–60: Wavytalk, TYMO, Revlon-type dryer brushes [inf from TikTok Shop listings] | $8–15 drugstore | $8–15: KISS imPRESS "BEST $8 press-on" [c]; Beetles gel kits |
| Mid / masstige | $100–250: Laifen Swift Special ≈$159 [c]; T3; L'ange; Shark FlexStyle ≈$270–330 [unverified] | $20–45: Gisou oil, Divi serum, Crown Affair [unverified exact] | $15–28 press-ons: Glamnetic "start at like $15" [c, creator]; Olive & June "$10 per set" [c]; Static AOV $50–75 |
| Premium | $400–600: Dyson Airwrap, RevAir [unverified exact] | $40–75: K18 mask, Olaplex | $40–100 systems: O&J Mani System, gel lamp kits; Nailboo "$30 kit" [c] |

**Implication [inf]:** a $1,200 Short pays back in roughly 25 premium tools, about 100 haircare units, or about 80 press-on sets. Below the $40 price point, VXO must sell *variants and volume* (Season), not one hero.

### 1.4 Seasonality calendar

| Month | Hair tools | Haircare | Nails | Evidence |
|---|---|---|---|---|
| Jan | "New year hair" resets; post-holiday gift tutorials | Hair-growth and scalp "journeys" (claims risk) | Winter sets | Shark "got a FlexStyle for the holidays? dos and don'ts" post [c] |
| Feb | — | — | **Valentine's** drops | [inf] |
| Mar–May | **Mother's Day = No. 1 gifting peak for tools**; prom, wedding | Spring launches | **Prom, wedding, Mother's Day** gift sets | Glamnetic and Beetles Mother's Day ads (Motion; [m] Beetles post 2025-05-11) |
| Jun–Aug | **Humidity / frizz season**; travel tools (dual voltage); **Prime Day (July)** | Sun, chlorine, "summer hair" | **Vacation nails**; back to school (Aug) | Glamnetic "SHOP VACATION NAILS" ×9 ads; Laifen/Gisou/Kitsch Prime Day posts [m] |
| Sep–Oct | Back to routine | Fall launches | **Halloween drops** (glow, 3D) | Olive & June glow-in-the-dark polish and press-ons [c]; "Halloween sets" trend |
| Nov–Dec | **BFCM + holiday gifting = the peak for tools** | Gift sets; licensed collabs (Kitsch × Grinch) | Holiday sets, licensed IP (Glamnetic × Harry Potter, O&J × Mandalorian) | Kitsch Grinch Motion ads; NIQ BFCM data |

**Where they advertise:**
- **Meta** (all; volumes above).
- **TikTok** Spark + affiliates + Shop (Wavytalk, TYMO, Laifen, Glamnetic, RevAir all run TikTok Shop).
- **Amazon** (TYMO, Laifen, Wavytalk, Nailboo "$30 kit from Amazon").
- **Retail co-op**: Ulta, Sephora, Target, Walmart, CVS, Sally Beauty.
- **YouTube** for premium tools (Dyson).
- **Live shopping**: Bondi Boost and L'ange run TikTok LIVE sales [c].

---

## 2. Teardowns: 18 in full, from 31 measured

Cut rate = (detected cuts + 1) ÷ duration. Scene detection at 0.3 **misses jump cuts inside talking-head UGC**, so for talking heads I counted cuts by eye from the 2 fps tiles where it mattered. Like-rate = likes ÷ views. Sound: "voice-led" means speech dominates the RMS envelope.

### 2.1 Measured set at a glance [m]

| # | Ad (link) | Date | Views · like-rate | Length · cuts | Signature |
|---|---|---|---|---|---|
| H1 | RevAir salon one-take ([link](https://www.tiktok.com/@myrevair/video/7596389334874443021)) | 2026-01-17 | **26.3M · 0.44 %** | 46.0 s · 0 | Paid |
| H2 | amika × @abigaillinnn thermal brush ([link](https://www.tiktok.com/@abigaillinnn/video/7273892789786643755)) | 2023-09 (older) | **15.3M · 0.26 %** | 41.4 s · 7 | Paid |
| H3 | Dyson Airwrap Co-anda2x × @briannenhowey ([link](https://www.tiktok.com/@briannenhowey/video/7528092738940718367)) | 2025-07-17 | **9.4M · 10.6 %** | 37.8 s · 31 | Organic (#DysonPartner) |
| H4 | Wavytalk Blowout Boost × @mo__styles ([link](https://www.tiktok.com/@mo__styles/video/7608692379591249165)) | 2026-02-19 | **6.2M · 3.1 %** | 100.6 s · 37 | Mixed |
| H5 | K18 mask "secret" ([link](https://www.tiktok.com/@k18hair/video/7393403629849300255)) | 2024-07 (older) | **4.7M · 0.02 %** | 59.8 s · 3 (+ jump cuts) | Heavily paid |
| H6 | Gisou × @alysialoo oil ([link](https://www.tiktok.com/@alysialoo/video/7390075205349068074)) | 2024-07 (older) | 3.6M · 2.3 % | 21.0 s · 15 | Mixed |
| H7 | TYMO Ring "trying the viral brush" ([link](https://www.tiktok.com/@valeria_deldinova/video/7336920067810102560)) | 2024-02 (older) | 3.2M · **11.1 %** | 202 s · 6 | Organic |
| H8 | Press-on "apple strength test" ([link](https://www.tiktok.com/@chelseygobbo/video/7429060659708431662)) | 2024-10-23 | 2.3M · 2.5 % (shares 0.31 %) | 94.9 s · 5 | Organic |
| H9 | Glamnetic × GLAMZILLA "how I apply" ([link](https://www.tiktok.com/@glamzilla/video/7647739109007445256)) | 2026-06-05 | 2.1M · 1.8 % | 112 s · 10 | Mixed |
| H10 | Dyson USA "Airwrap for beginners" ([link](https://www.tiktok.com/@dyson_usa/video/7475815898503220510)) | 2025-02-26 | 2.0M · 3.0 % | 94.9 s · 13 | Organic, brand account |
| H11 | L'ange Le Duo × @anggwells ([link](https://www.tiktok.com/@anggwells/video/7328440181575421230)) | 2024-01 (older) | 1.8M · 1.2 % | 59.1 s · 16 | Mixed |
| H12 | Nimble AI manicure robot × @uptin ([link](https://www.tiktok.com/@uptin/video/7345177050333990177)) | 2024-03 (older) | 1.7M · 1.7 %, **shares 1.0 %** | 63.3 s · 15 | Organic tech |
| H13 | Gisou "we only carry facts" POV ([link](https://www.tiktok.com/@gisou/video/7466921889588399382)) | 2025-02-02 | 1.6M · 3.2 % | **6.2 s · 0** | Organic |
| H14 | Gisou "take the edge off" POV, repeat of H13 ([link](https://www.tiktok.com/@gisou/video/7525532113102277920)) | 2025-07-10 | 1.3M · 0.38 % | **5.6 s · 0** | Paid |
| H15 | Shark FlexFusion × @golloria ([link](https://www.tiktok.com/@golloria/video/7431011606303083818)) | 2024-10-29 | 1.2M · 3.9 % | 54.8 s · 2 | Organic |
| H16 | Static Nails "best press-ons" ([link](https://www.tiktok.com/@sammypur/video/7327827381610122538)) | 2024-01 (older) | 1.1M · 1.8 % | 36.9 s · 6 | Mixed |
| H17 | RevAir "WHAT?! a reverse-air dryer" ([link](https://www.tiktok.com/@myrevair/video/7236414907824999722)) | 2023-05 (older) | 1.0M · 2.0 %, shares 0.54 % | 52.1 s · 23 | Mixed |
| H18 | Bondi Boost "lock drops" ([link](https://www.tiktok.com/@bondiboost/video/7528185552521170207)) | 2025-07-17 | 1.0M · 0.15 % | 67.2 s · 0 | Paid |
| — | Glamnetic founder "movement" ([link](https://www.tiktok.com/@annmcferran/video/7512626566317378862)) | 2025-06-06 | 696K · 0.70 % | 57.7 s · 20 | Paid-ish |
| — | Gisou × Alysia hair perfume "I'm a fraud" ([link](https://www.tiktok.com/@gisou/video/7525210652365933857)) | 2025-07-09 | 613K · 0.51 % | 20.1 s · 4 | Paid |
| — | Glamnetic PAS "do your press-ons disappoint you?" ([link](https://www.tiktok.com/@glamnetic/video/7299259191313616171)) | 2023-11 (older) | 525K · 2.6 % | 23.9 s · 9 | Mixed |
| — | Bondi Boost "vacuum shedding" ([link](https://www.tiktok.com/@bondiboost/video/7486868882792402222)) | 2025-03-28 | 327K · 0.22 % | 41.4 s · 8 | Paid |
| — | Glamnetic "stop wasting $$$ at the salon" ([link](https://www.tiktok.com/@glamnetic/video/7533887976552549645)) | 2025-08-02 | 327K · 1.1 % | 30.9 s · 0 | Mixed |
| — | Nailboo dip-powder fill ([link](https://www.tiktok.com/@nailboo/video/7560832929048415519)) | 2025-10-13 | 325K · 1.5 % | 31.5 s · 10 | Mixed |
| — | Dashing Diva gel strips ([link](https://www.tiktok.com/@salomeandreaa/video/7387450501551443230)) | 2024-07 (older) | 324K · 1.9 % | 39.4 s · 20 | Mixed |
| — | Glamnetic "if our press-ons at Ulta could talk" ([link](https://www.tiktok.com/@glamnetic/video/7574527786950397198)) | 2025-11-19 | 207K · 3.4 % | 8.0 s · 4 | Organic |
| — | Gisou "hair oil from scratch" ([link](https://www.tiktok.com/@gisou/video/7369709172767673633)) | 2024-05 (older) | 123K · 7.8 % | 10.9 s · 20 | Organic |
| — | Kitsch × Grinch hair perfume ([link](https://www.tiktok.com/@kitsch/video/7573775017108983070)) | 2025-11-17 | 101K · 0.86 % | 14.5 s · 10 | — |
| — | **Shark SilkiPro launch montage (control)** ([link](https://www.tiktok.com/@sharkbeauty/video/7608222442540092702)) | 2026-02-18 | **43K** · 3.4 % | 8.8 s · 19 | Brand-made |
| — | **Glamnetic "test with a CAR" (control)** ([link](https://www.tiktok.com/@glamnetic/video/7515547712318770478)) | 2025-06-14 | **7.9K** · 1.8 % | 32.4 s · 4 | Brand-made |
| — | Glamnetic "car accident" review read ([link](https://www.tiktok.com/@glamnetic/video/7249919956194823467)) | 2023-06 (older) | 4.5K · 3.2 % | 25.8 s · 0 | Brand-made |

### 2.2 Full teardowns (shot list with timecodes from the 2 fps tiles)

**H1 · RevAir salon one-take (26.3M, paid, 46 s, 0 cuts).**
- **Second 1:** a stylist in a busy salon is *already* sectioning a client's type-4 hair, with the wand in hand. Motion at frame 0.
- **Shot list:**
  - 0–1.5: sections the hair;
  - 1.5–8: feeds a section into the hose wand;
  - 8.5–10: a clock super "**12:39**" appears;
  - 9.5–45: a red **arrow super points at the hose** throughout;
  - 26–30: super "I DON'T KNOW WHO YOU ARE" (a song lyric);
  - 35: "PRETTY GOOD";
  - 43.5–46: "MAKE SURE Y'ALL TAKE ADVANTAGE OF THESE DEALS NOW".
- **Turn:** none. The device *is* the turn: a hose that eats hair.
- **Product interaction:** continuous, in a real salon, on hard-to-dry hair.
- **Sound:** music bed plus a short speech fragment; −16.1 LUFS, peak −0.6 dBTP (mastered hot).
- **CTA:** the deal super.
- **Why it sold [inf]:** a professional context (a stylist uses it on clients), a hair type that sells the speed claim, a visible clock, and an ugly-but-fascinating machine. **One take reads as untouched proof.**

**H2 · amika Blowout Babe × @abigaillinnn (15.3M, paid, 41.4 s, 7 cuts, ASL 5.2 s).**
- **Second 1:** "**Stop what you're doing.** This tip will change your entire blowout game." She points at camera. A permanent super names the product.
- **Shots:**
  - 0–5.6: talking head, brush up at 3.0;
  - 5.6–8.3: **flash-forward result**: straight hair → full blowout curls by a hair flip at 7.5;
  - 8.3–12.5: "if you're wrapping it up and just pulling down…" (the wrong way);
  - 12.5–17.4: the heat-protect product to camera;
  - 17.4–31.8: technique (clips in, wrap away from the face, tension, spin counter-clockwise);
  - 33–37: the dry-shampoo product;
  - 37.8–41.4: the result.
- **Product interaction:** three amika products in 41 s.
- **Sound:** voice-led, −25.9 LUFS.
- **Why it sold:** an **"you're doing it wrong" correction**, the result shown by 8 s, and a 3-SKU basket.

**H3 · Dyson Co-anda2x × @briannenhowey (9.4M, 10.6 % likes, 37.8 s, 31 cuts, ASL 1.2 s).**
- **Second 1:** the creator flicks her already-styled hair; super "Dyson Partner". At 2.0 s: the **tool in its case**.
- **Shots:** an insert every 1–1.3 s:
  - pre-style cream into the palm (3.0);
  - finger-combing wet hair (5–7);
  - an ECU of wet ends (7.5);
  - the tool attaching (11.5);
  - the rough-dry;
  - brush sections;
  - the smoothing attachment;
  - the serum;
  - "and we're off" (37).
- **Sound:** VO −29.8 LUFS over a light bed.
- **Text:** "#DysonPartner".
- **Why it sold:** a **polished creator tutorial at a brand-film pace**: 1.2 s ASL with every shot a real step. It is the closest thing in the niche to what VXO makes, and it works because each cut is a *process step*, not a mood shot.

**H4 · Wavytalk Blowout Boost × @mo__styles (6.2M, 3.1 %, 100.6 s, 37 cuts).**
- **Second 1:** **the thermal brush is tangled in her hair at frame 0.** "Oh no, no… why is it stuck?"
- **Turn:** the same creator plays **two characters**, told apart by props (a purple brush and straight hair = the beginner; a blue brush and waves = the expert): "There are steps."
- **Shots:** a shot/reverse-shot skit every 1–3 s, then a 10-minute routine.
- **Sound:** voice, −14.6 LUFS.
- **Why it sold:** **fear first, then fix**. The fear (tangling) is the top objection to every rotating or thermal brush, and the skit makes the instructions entertaining.

**H5 · K18 "secret" (4.7M, 0.02 % = almost entirely paid, 59.8 s).**
- **Second 1:** a talking head; super "My haircare secret". The product in hand from 3.0.
- **Script:** "not enough people are talking about this" → "**reverses damage from heat, colour, bleach**" (a K18 claim it substantiates) → method (skip conditioner, 1–3 pumps, wait 4 min) → "I used it 4–6 weeks at first" → thanks K18.
- **Shots:** jump cuts only; scene-detect found 3.
- **Sound:** voice, −26.5 LUFS.
- **Why it sold:** a classic whitelisted testimonial with **the usage rule as content** (4 minutes, no conditioner). It scaled on spend, not on engagement.

**H6 · Gisou × @alysialoo (3.6M, 2.3 %, 21 s, 15 cuts, ASL 1.3 s).**
- **Second 1:** sleek hair, finger-combed. Super "how do I keep my hair so healthy?"
- **Shots:**
  - 1.5: a **hair-tousle "before"** (messy);
  - 2.0: the bottle to camera, label legible;
  - 3.0–4.5: the dropper lifts, a drop falls;
  - 5.0: oil into the palm;
  - 6–8: apply;
  - 8.5–10.5: blow-dry with **hair flips** used as cut points;
  - 11: sleek.
- **Sound:** voice, −28.6 LUFS.
- **Why it sold:** the product is on screen at 2 s, **hair flips work as transitions**, and there is a sensory reason to believe ("smell", "glossy").

**H7 · TYMO Ring "trying the viral brush" (3.2M, 11.1 %, 202 s).**
- **Second 1:** the tool to camera with a **price super "60€"**.
- **Story:** an unboxing (glove, brush), "I've seen it do wonders, but I don't know", the frizz shown honestly, the heat-up wait, a long real-time demo, the result.
- **Why it sold:** a **sceptical first-try** with a price anchor. An organic Amazon-find format. Long is fine when it's honest.

**H8 · Press-on "apple strength test" (2.3M, 2.5 %, shares 0.31 %, 94.9 s).**
- **Second 1:** a mum on camera; super "**Let's test the strength of these press-ons!!**"
- **Story:**
  - 0–36: the backstory (teen daughter, salon fills, cost);
  - 36.4: cut to the teen's hand on a granite counter;
  - 39–45: she **presses her nails into the counter edge and bends them**;
  - 46–59: **she digs her nails into an apple**;
  - 60–65: "not lifting at the cuticle".
- **Sound:** voice, −30.4 LUFS.
- **Why it sold:** a **real ordeal on real hands**, family credibility, and a high share rate (an argument piece: "nails that actually work").
- **The brand version (Glamnetic × BMW) got 7.9K.** The ordeal is too far from use, a stranger is in a supercar, and the proof frame comes after 22 s.

**H9 · Glamnetic × GLAMZILLA "how I apply" (2.1M, 1.8 %, 112 s).**
- **Second 1:** the creator grimaces, holding up the pack: "I launched an entire collab… and didn't even show you how to apply them. **Influencers these days, disgusting.**"
- **Story:** self-roast → step-by-step with honest skips ("I'm lazy, I just buff").
- **Sound:** voice, −15 LUFS.
- **Why it sold:** **a self-roast hook plus a tutorial**. A collab partner selling her own SKU.

**H10 · Dyson USA "Airwrap for beginners" (2.0M, 3.0 %, 94.9 s, brand account).**
- **Second 1:** **the result first**: a back-of-head swish of big curls; super "Dyson Airwrap for Beginners"; turn to camera at 2.5.
- **Story:** "everything you need to know": wet hair, rough-dry roots, three sections, full heat, curl away from the face, cool shot.
- **Sound:** **−12.2 LUFS, peak +3.2 dBFS (clipping)**. Mastered loud.
- **Why it sold:** **education removes the main fear for a $500 tool** ("I'll never learn to use it"). Even Dyson's own account wins with a creator-led tutorial, not a brand film.

**H11 · L'ange Le Duo × @anggwells (1.8M, 1.2 %, 59 s, 16 cuts).**
- **Second 1:** **the result first** (big curls, a hand fluff); super "Curls that last for days".
- **Story:** texturising spray → heat tamer → the Le Duo with "cooling air vents… like a cool shot" → the claim "**stay for three plus days**" → the dry shampoo.
- **Sound:** voice, −36.2 LUFS (very quiet).
- **Why it sold:** **result first, 4 SKUs, a longevity claim**.

**H12 · Nimble AI manicure robot × @uptin (1.7M, shares 1.0 %).**
- **Second 1:** a hand slides into a white box; super "**$700 AI Manicure Machine**".
- **Story:** a tech explainer (machine vision, 10 min, 30 colours).
- **Why it sold:** **novelty + a price + "AI"**. The highest share rate in the set: tech curiosity travels. For VXO: **a nail *device* is a gadget story** (doc 51 grammar), not a beauty story.

**H13 · Gisou "We don't judge, we only carry facts…" (1.6M, 3.2 %, 6.2 s, one take).**
- **Second 1:** **a POV down a staircase, carrying about 9 oil bottles stacked along a forearm.** Motion at frame 0.
- **Turn:** the pun "carry" (the bottles, the facts).
- **Sound:** a trending sound, a laugh at 0.2 and "here!" at 4.2.
- **Why it sold:** **a balance stunt + a pun + a loop**. It has the product at full saturation for 6 s with zero claims.
- **H14 is the same gag 5 months later**, now with shampoo and conditioner bottles ("Just a little something to take the edge off…"): **1.3M, paid**. **A winning gag becomes a series.**

**H15 · Shark FlexFusion × @golloria (1.2M, 3.9 %, 54.8 s).**
- **Second 1:** two pink tools held to camera: "This is the brand new Shark Beauty FlexFusion."
- **Story:** attachments → "going to lunch with the girls" → brush-out → **half-head comparison at 37–41**: "look how straight that made my hair compared to this side" → "**that literally took me three minutes**" → the air-straightener insert.
- **Sound:** voice, −19.8 LUFS.
- **Why it sold:** **split-head proof + a time claim + 42" hair** (a big-hair creator).

**H16 · Static Nails "best press-ons" (1.1M, 1.8 %, 36.9 s).**
- **Second 1:** hands with the nails covering her face; super "**THE BEST PRESS ON NAILS**".
- **Story:**
  - "not sponsored";
  - "usual press-ons last a day… these have been on for **nine days**";
  - "**look as good as a $100 manicure in Miami**";
  - "I could rip open an Amazon package";
  - 10.5: a window-light hand shot;
  - the shade name.
- **Why it sold:** **days-of-wear + a price anchor + "not sponsored"**.

**H17 · RevAir "WHAT?! A REVERSE-AIR DRYER?" (1.0M, shares 0.54 %, 52 s, 23 cuts).**
- **Second 1:** her wet hair is already sucked into the wand at full arm stretch, and she has a cringe face.
- **Shots:**
  - 5.5: a whip/zoom-blur transition to a **flash-forward hair flip** of the dry result;
  - 8.0: a red flash frame;
  - back to the unboxing (10–12: the canister);
  - 24–30: **"this side is dry, the other side is dripping wet"**;
  - 33.5: a hand-over-mouth reaction.
- **Sound:** voice, −24.4 LUFS.
- **Why it sold:** **a weird machine + a flash-forward result + split proof**.

**H18 · Bondi Boost "lock drops" (1.0M, 0.15 % paid, 67 s, one take).**
- **Second 1:** "**If your hairline is looking a little too similar to your boyfriend's…**"
- **Story:** "helping grow all of these baby hairs".
- **Why it is here:** a **cautionary paid winner**. The hook is a **negative self-perception** line (a Meta Health & Wellness risk), and the body makes a **growth claim** (a drug claim, FDA; TikTok bans "treat hair loss"). It scaled anyway, which shows how much enforcement varies. **VXO never writes this.**

### 2.3 Cross-ad patterns (what to copy) [m]

| Pattern | Evidence | How VXO uses it |
|---|---|---|
| **Failure in frame 0** | Tangle (H4), pop-off (Glamnetic PAS), shed-hair vacuum roll, hose sucking hair (H1, H17) | AI stages the failure. It is not a claim, it's the category's fear |
| **Result-first flash-forward** | H2 at 5.6 s, H10 at 0 s, H11 at 0 s, H17 at 5.5 s | Open on the client's *real* result for 0.5–1.5 s, then the AI hook world, then the proof |
| **Split or half-and-half proof** | H15 (half head), H17 (dry/wet halves) | Always real footage. AI frames it (labels, a ruler, a clock) |
| **A clock on screen** | H1 "12:39", H15 "3 minutes", Wavytalk "10 minutes" | A diegetic clock in the AI world (a kitchen timer, a stopwatch) *only* echoing a tested time |
| **The usage rule as content** | K18 (4 min, no conditioner), Dyson (cool shot), amika (counter-clockwise) | The rule becomes the joke (§7 C3, C4) |
| **One creator, two characters** | H4 | AI makes the second character cheaply: a deadpan "expert" double (comedy only, disclosed) |
| **POV balance or carry gag** | H13, H14 | A loopable 5–6 s product-saturation stunt. A Seedance one-take is feasible with rigid bottles (§4) |
| **Price anchor** | "60€", "$100 manicure", "$150 salon", "start at like $15", "$700 AI machine" | One super per film. Salon price vs product price is the nail niche's master argument |
| **Pacing** | Organic hits: talking heads with 0–6 cuts *or* 1.2 s ASL tutorials; brand montages at 0.46 s ASL lost (Shark control) | Speed follows *steps*, not style. Never cut faster than the process |
| **Loudness** | Brand-mastered posts at −12 to −16 LUFS (Dyson, Glamnetic, RevAir, Bondi); creator-native at −25 to −36 | When a VXO hook is stitched onto UGC, **match the UGC's loudness at the seam**, then master the whole to −14 (46). A +15 dB jump at the splice screams "ad" [inf] |

---

## 3. What actually converts in this niche (data)

| # | Finding | Number | Source | Status |
|---|---|---|---|---|
| D1 | Haircare Meta creatives: asset-type effectiveness | **Graphic Design 74** · UGC 67 · Branded/Studio 65 · Lifestyle 58 · **Product Shot 44**; UGC has the top-performance rate (73.8 %) | [Benly Q1 2026 haircare](https://benly.ai/benchmarks/q1-2026/beauty-personal-care/haircare), 4.7K creatives, 23 brands | [v] |
| D2 | Haircare creative lifespan | Median 23 d (+15 % vs cross-industry); 43.6 % survive 30 d; **0 % reach 90 d** | Same | [v] |
| D3 | Haircare video hooks | Bold Statement 32.7 % (36 d) · **Pain Point 27.6 % (41 d, the longest-lived common hook)** · Visual Intrigue 16.3 % · Pattern Interrupt 12.9 % · **Before/After 0.1 % but 1.9× the average lifespan** | Same | [v] |
| D4 | Haircare promo intent | **Discount 63.2 %** (57 → 69 % Jan–Mar) · Free Offer 16.5 % · New Launch 12.6 % · Bundle 5.2 % | Same | [v] |
| D5 | Makeup (incl. nail-adjacent) for contrast | **Product Shot 64 scores highest**, UGC 61; **New Launch 60 %** of creatives; Visual Intrigue hook 41 % | [Benly makeup](https://benly.ai/benchmarks/q1-2026/beauty-personal-care/makeup-cosmetics) | [v] (nails not broken out) |
| D6 | Meta format mix, hair tools | **Shark: Demo 34 %, Before/After 19 %** · **TYMO: Demo 36 %, Before/After 25 %** · ghd: Demo 21 %, B/A 13 % · Dyson: **Offer banner 28 %**, Demo 21 % | Motion public library ([TYMO](https://motionapp.com/library/tymo-beauty), [Shark](https://motionapp.com/library/shark-beauty)) | [v] snapshot |
| D7 | Meta format mix, haircare | K18: **Headline images 64 %**, B/A 21 % · Olaplex: B/A 19 % · Ouai: Demo 30 %, B/A 17 % · Prose: Demo 19 %, Testimonial 12 % · Divi: Headline 21 %, Testimonial 14 % · Gisou: Offer banner 16 %, Demo 16 %, Statistic 12 % | Motion | [v] |
| D8 | Meta format mix, nails | Olive & June: Demo 28 %, Unboxing 12 %, B/A 10 % · KISS: Demo 29 %, Yapper 12 % · Glamnetic: Demo 19 %, Headline 16 % · Nailboo: Demo 26 % · Static: Headline 22 %, UGC overlay 14 % · Doonails: Demo 29 %, Us-vs-Them 12 % | Motion | [v] |
| D9 | Volume (new creatives per week) | TYMO 688 · Kitsch 173 · Switch Nails 79 · Prose 41 · Nutrafol 41 · Glamnetic 37 · Olaplex 36 · Bondi Boost 27 · O&J 27 · ghd 22 · Moroccanoil 21 · Chillhouse 16 · Divi 15 · KISS 15 · Amika 14 · Shark 14 · Dyson 12 · Gisou 10 · Nailboo 7 · Ouai 7 · Vegamour 6 · JVN 5 · K18 5 · **Static 3** | Motion | [v] |
| D10 | Video length in Meta nail ads | Doonails: 19 of 20 video ads run **29–89 s** (most ≈1 min); Glamnetic videos 12 s and 29 s; Olive & June 8–58 s | Motion ([Doonails](https://motionapp.com/library/doonails)) | [v] |
| D11 | Measured paid-scaled length (TikTok) | Median **≈43 s** (5.6–67 s), n = 8 | §2 | [m] small n |
| D12 | Measured organic-hit length | 6–202 s; the two shortest hits are the Gisou POV gags (6 s, 11 s) | §2 | [m] |
| D13 | Conversion and repeat (nails) | Static: ≈7 % online conversion, **57 % of purchases repeat** [c] | [Glossy](https://www.glossy.co/beauty/how-static-nails-hopes-to-carve-out-a-niche-in-the-9-billion-nail-market) | [c] dated |
| D14 | TikTok Shop | Haircare +118 % YoY; Wavytalk $15M/quarter; tools declined over BFCM 2025 | §1.1 | [v] |
| D15 | Category funnel (all H&B) | Best CTR (2.36 %) but ROAS 1.82 vs 2.17 cross-industry | Billo via doc 47 §2 | [v] |
| D16 | AI trust | 52 % of women "not OK" with AI models; 31 % trust less on noticing AI | Doc 47 §2 | [v] |
| D17 | Before/after policy | Meta exempts "cosmetics, hair extensions… hair products" from the side-by-side ban if no negative self-perception; hair *loss* products are treated more strictly | [Meta Health & Wellness](https://transparency.meta.com/policies/ad-standards/restricted-goods-services/health-wellness); [AuditSocials](https://www.auditsocials.com/blog/hair-loss-ads-2026-platform-line-meta-tiktok-google-pinterest-finasteride-minoxidil-prescription-policy) [v] | P + [v] |

### 3.1 What this means, by sub-niche [inf]

**Hair tools ($60–600).**
- **What sells:** demo plus before/after, proven by a clock and a split head.
- **Who sells it:** creators with *difficult* hair (type 4, very long, very thick), because the hardest case sells the claim.
- **What is missing:** brands run thousands of near-identical demos, so **pattern-interrupt hooks are scarce**. That is VXO's job: AI hook modules (0–3 s) bolted onto the demos, plus a 15 s cinematic "world" cut for the Offer-banner slot that Dyson fills 28 % of the time.
- **Length:** 3 s hook module · 15 s cutdown · client demo body to 30–60 s.

**Haircare ($20–75).**
- **What sells:** graphic design and headline images score highest (Benly 74; K18 64 % headlines). Discounts are everywhere.
- **What VXO adds:** **motion-graphic "statistic" films**, for example "2× shinier" on a 3D hair strand (Gisou runs Statistic 12 %), **texture/sensory loops** (oil drop, honey, dropper; 11 §4) and **POV gags** (Gisou).
- **Rule:** never AI hair "results". Use claims with units and the client's test (§5).

**Nails ($8–100).**
- **What sells:** the salon price comparison, days of wear, a real-hand ordeal, quick application, and seasonal or licensed drops.
- **The re-buy driver:** drops monthly (Halloween, holiday, Valentine's, vacation, Mother's Day). **Every drop needs a new 6–15 s film.** This is the most "Season-shaped" sub-niche in all of VXO's research.
- **What VXO adds:** drop films (the world of the theme), "salon vs home" comedies, and nail-art "impossible" macros. Shade accuracy is ΔE-checked (doc 47 §3).

**UGC vs cinematic.**
- UGC wins hair tools (Benly UGC top-performance rate 73.8 %) and creator demos win TikTok.
- Cinematic wins only as (a) a hook module, (b) a graphic/statistic film, or (c) a short POV or comedy gag.
- **Do not sell a 30 s cinematic film as the main ad in this niche.**

**AI ads and disclosure.**
- No hair or nail brand AI campaign with published results was found. XMondo used AI models for a hair-colour campaign in 2023 ([Beauty Independent](https://www.beautyindependent.com/?p=112418)); no results were published.
- The backlash cases are beauty-wide (Guess, Utena 2026 IP copying), and Dove pledged never to use AI women.
- Rule: **AI people only as comedy characters, disclosed** (NY synthetic-performer law). **Never AI hair or nails as the result.**

---

## 4. AI realism pitfalls for this niche, and the fixes

Routing follows 43 §1.
- **Kling 3.0 Pro i2v:** single-move label, tool and nail inserts, from a **real photo** of the client's tool or the client's hand set.
- **Cinema Studio 4.0:** the hero tool one-take.
- **Seedance 2.5 r2v:** multi-shot comedy and action with people.
- **Wan 3.0 480p:** previs.
- **Real client footage:** every hair or nail *result*.
- Stills come first. Every motion shot starts from an approved still.

| Pitfall | What goes wrong | Fix (prompt / reference / post) |
|---|---|---|
| **Hair length drifts between cuts** | Hair grows or shrinks across shots, **and that can become a false claim** (*Dyson v. Dreame*) | Put a length lock in every shot: "hair ends exactly at the collarbone in every shot, never longer, never shorter". Use one hair reference (back + side). QC the length at each cut on the 2 fps strip. **The length on screen must be ≤ the claim's tested length** |
| **Wet/dry state jumps** | Hair goes dry → wet → dry, or wet hair shows volume | Script the state per shot ("damp ends, darker colour, clumped in 1 cm ribbons"). Script its fate (43 rule 12): it only gets drier |
| **Strands fuse into a sheet ("helmet hair")** | No flyaways; a rubbery swing | Backlight for the shine band and flyaways (11 §4). Use 1–2 swings max, Seedance 720p. "Individual strands separate at the ends; 3–5 frame lag behind the head" |
| **Hair clips through the tool** | Barrels and plates pass through hair; curls wind in both directions at once | **Never generate hair-on-barrel contact as proof.** For a failure gag (tangle), write the wind direction and stop point: "the lock wraps clockwise 3 turns and stops 3 cm from the scalp". Use Kling first/last frame from two real stills. Cut on contact |
| **Heated plates glow or smoke** | Models add an orange glow or smoke, which reads as **burning or heat damage** (the opposite of every claim) | "Ceramic plates matte grey, never glowing; no smoke; a thin steam wisp only on wet hair, gone within 0.5 s" |
| **Visible "wind lines" and dust from dryers** | A CG airflow look | Show airflow through what it moves: "hair ends lift 4 cm and flutter", "a tissue 30 cm away bends". No stylised streaks |
| **Cords and hoses teleport** | The cord vanishes, forks, or passes through an arm | One cord in the reference; "the cord exits the base, falls to the floor behind the stool, never crosses the arm". Crop it out of inserts if needed. RevAir-type hoses are rigid ribbed tubes, 1.5–2 m: "ribbed hose keeps its diameter" |
| **Tool redesign** | Button layout, LED ring and logo change shape | Text and logo come only from the real-photo still (Kling). "Exact button positions as reference; the LED is the only light source on the tool". Run QC on the button count |
| **Hands: finger count, fused grips** | Six fingers, or the thumb merges with the tool | 43 §5 hands rules + Higgsfield hands guide: lead with the hand, give start and end poses, use a pose ref ([B-HANDS](https://higgsfield.ai/blog/ai-video-hands-faces)). Write "exactly five fingers per hand". Prefer one hand per shot |
| **Nails: shape, length, count and colour drift** | Almond becomes coffin, lengths vary per finger, the shade shifts, a nail disappears | **Use a client hand-set plate: a real photo of the real set on a hand model as the identity ref.** Name the shape, length class and colour hex. Make each shade its own still. **ΔE ≤ 3 vs the client swatch** (47 §3). Use one hand pose per shot and no finger interlacing |
| **Nail art misrendered** | Patterns melt or mirror; 3D charms float off | Use macro stills from the real set, Kling single move (tilt 10°), "pattern fixed to the nail surface, no movement relative to the nail" |
| **Press-on application** | The nail slides into place but bends or sinks into the finger | Don't generate application. **Use real footage** (the measured winners all show it real) |
| **Wet polish behaviour** | The brush stroke paints itself; polish behaves like water | Show "press and lift", not the stroke (47 §3). Viscosity: "polish levels in 1 s, glossy, a single bubble pops". Cut on the stroke |
| **Magnetic cat-eye effect** | The light band jumps randomly | "A magnet held 5 mm above the wet nail for 3 s draws a silver band toward the magnet; the band then shifts 2 mm as the hand tilts 15°". Real pigment physics |
| **Gel/UV lamp** | The lamp glows white; hands go inside wrong | "LED lamp interior glows violet (≈365–405 nm look), fingers flat on the base, 60 s timer display" (copy the client lamp's real timer) |
| **Mirrors in bathrooms** | The reflection is wrong or the crew is missing | Avoid mirrors, or "mirror shows only the tiled wall". Shoot from the doorway (a real rig) |
| **Steam and humidity** | Fog renders as smoke | "Thin steam, rises and pools at the ceiling, condensation beads on tile" (47 C5) |
| **Hair and skin results on AI people** | Reads as a mock-up (FTC Colgate) and can trigger backlash | **Never**. AI people appear only in comedy beats, and their hair is styled *before* the film begins (not changed by the product). Results = client footage in the proof slot |

**Model per shot type (niche summary):**

| Shot type | Model | Settings | Why |
|---|---|---|---|
| Tool packshot / label insert | Kling 3.0 Pro i2v | 5 s, sound off, `last_image_url` = packshot | Holds text and buttons from the input image (43 §1) |
| Hero tool orbit / push | Cinema Studio 4.0 | `dolly-in`, `single-shot`, 720p | Retains the most constraints |
| Comedy and action with people (rescue crew, pit crew, chase) | Seedance 2.5 r2v | 15 s, 6–9 shots, "EXACTLY N SHOTS", `generate_audio:true` | Multi-shot coverage (41, 43 §7.1–7.2) |
| Hair swing or back-of-head mood | Seedance 2.5 r2v 720p | ≤2 swings; real hair ref | Best hair physics (11 §4) |
| Nail macro / hand pose | Kling 3.0 Pro i2v from the real hand-set photo | One micro-move (tilt, light sweep) | Identity from the photo; minimal motion = minimal morph |
| POV carry gag (Gisou class) | Seedance 2.5 r2v one-take or Kling i2v 5 s | "one continuous take, no cuts", rigid bottles | Rigid objects are easy; write the bottle count |
| Previs | Wan 3.0 r2v 480p | Seed | $0.05/s |
| Result / proof | **Client footage** | — | Law + trust |

**Style header delta for this niche (add to 11 §4):** "Hair-tool product film, 50 mm and 100 mm, real bathroom or salon with lived-in clutter, matte ceramic plates never glowing, one power cord exiting the base and falling out of frame, hair length locked to [X] in every shot, damp-to-dry state only moves one way, exactly five fingers per hand, nails [shape] [length] [hex] from the reference plate, no wind lines, no smoke, label and button layout from the reference only, all other text unreadable."

---

## 5. Policy and legal (US first; the client's counsel has the final word)

### 5.1 FDA: the cosmetic/drug line

| Claim | Status | Safe alternative |
|---|---|---|
| "Grows hair", "regrowth", "stops/reduces hair loss or shedding", "thicker hair" (as growth), "promotes growth" | **Drug claims** ([FDA cosmetics law](https://www.fda.gov/cosmetics/laws-regulations/cosmetics-us-law); minoxidil is the OTC drug) | "Fuller-*looking*", "the *look* of density", "less breakage from brushing" (with a test), "scalp feels balanced" |
| "Treats dandruff", "anti-dandruff" | **OTC drug** (dandruff monograph actives only) | "Flake-free *look*", "soothes the *feel* of a dry scalp" |
| "Repairs damage" | OK as a cosmetic claim *about the hair fibre* if substantiated (K18 does this). Not OK as a medical "repair" | Say what was tested: "after 1 use, [x]% less breakage in lab test" |
| Supplements (hair gummies) | DSHEA structure/function + FTC substantiation; NAD has repeatedly cut "encourages hair growth" claims (Hairfinity, CVS Nourishing Hair, Hair La Vie) ([NAD](https://bbbprograms.org/media-center/dd/nad-recommends-brock-beauty-discontinue-certain-claims-for-hairfinity-dietary-supplement)) | "Supports *existing* healthy hair" (NAD accepted this narrower form) |
| Chemical straighteners (formaldehyde) | FDA's proposed ban has been repeatedly delayed (target Dec 2025, missed) ([SEJ](https://www.sej.org/node/51902)); **MD, CA and WA** ban formaldehyde in hair products | Avoid the category, or require written compliance |
| MoCRA (2022) | Safety substantiation, adverse-event records, facility registration | Ask whether the client is registered; it's a seriousness signal |

### 5.2 Hair tools: NAD case law that shapes every film

| Case | Holding | VXO rule |
|---|---|---|
| ***Dyson v. Dreame*** (NAD Fast-Track SWIFT #7600, 2026-08-07) | Models with **hair longer than shoulder length** contradicted "dries shoulder-length hair in 2 minutes"; "**a disclosure cannot contradict or be used to cure an unsupported message**" ([Mondaq](https://www.mondaq.com/nad-says-a-disclosure-cant-fix-a-misleading-product-demonstration/1837024)) | Hair length, density and type on screen must match the tested condition. "Dramatization" doesn't save it |
| **Dyson v. SharkNinja, Glossi "fastest blowout"** (2026) | Shark **permanently modified** the claim to state it rests on comparative dry-time testing, not air velocity alone ([Cosmetics Business](https://www.cosmeticsbusiness.com/sharkninja-modifies-marketing-claims-voluntarily-following-nad-challenge); [BBB](https://bbbprograms.org/media/newsroom/decisions/sharkninja-glossi)) | Superlatives need the right test. Ask for the test basis before writing "fastest" |
| **Dyson v. SharkNinja, HyperAir** (2022) | "Frizz-free / no frizz / forget frizz" **unsupported**; Dyson comparison "faster and easier" **unsupported**; "135 % faster air velocity" supported but disclosure fixes needed ([Personal Care Insights](https://www.personalcareinsights.com/news/nad-calls-out-sharkninjas-inaccurate-hair-drying-advertising-claims-amid-heated-hair-device-concerns-in-uk.html)) | Never "frizz-free". Write "less frizz [vs X, test]" |
| Product safety (context) | UK OPSS urged people to stop using certain heated brushes that caught fire in testing (2022, same source). In the US, hand-held hair dryers without immersion protection are a CPSC substantial product hazard [unverified, check 16 CFR 1120]; UL 859 is the US safety standard [unverified] | Never show a tool near water in a way that implies safe immersion (bathtub gags = no). Never show the tool left on unattended as "fine" unless it has auto-off |

### 5.3 Nails

| Topic | Rule | VXO rule |
|---|---|---|
| **EU TPO ban** | TPO (a gel-polish photoinitiator) reclassified CMR 1B; **banned in EU cosmetics from 1 Sep 2025**; still legal in the US ([Smarter Sorting](https://www.smartersorting.com/post/why-the-eu-banned-tpo-in-gel-nail-polish----and-why-the-u-s-hasnt-yet), [Khaleej Times](https://www.khaleejtimes.com/world/eu-gel-nail-polish-tpo-ban)) | "TPO-free" is a live claim for US gel brands *if true*. Never imply the client's TPO product is unsafe or safe |
| UV lamps | Public concern about UV nail lamps; no US ban | Don't claim "safe UV"; show LED lamps as the client's real model only |
| "Non-toxic", "10-free", "clean" | Vague; green-claim class actions are common | Use specific "made without [list]" only from the client's formula |
| "Damage-free", "no damage to natural nails" | An objective claim; needs support | "Glue-free tabs" / "removes with [x]" are factual alternatives |
| Durability ("2 weeks", "30 days", "waterproof") | Objective claims; need wear tests | Use the client's tested days; "water-resistant" over "waterproof" unless tested |
| "Car-accident proof" (Glamnetic review read, 2023) | A testimonial implying a safety or extreme durability outcome; the FTC treats a testimonial as the advertiser's claim | VXO never stages an extreme ordeal as proof. Ordeals stay obviously comedic, and real proof sits in the slot |

### 5.4 Platforms and FTC

- **Meta:**
  - Hair products and extensions are exempt from the before/after ban *without* negative self-perception.
  - "Your hairline looks like your boyfriend's" (Bondi H18) is the kind of second-person appearance attack the policy targets ([Meta](https://transparency.meta.com/policies/ad-standards/restricted-goods-services/health-wellness)).
  - Hair-loss Rx products need LegitScript.
  - Write problem hooks about **objects and situations** (the vacuum roll, the tangled brush), not about the viewer's body.
- **TikTok:**
  - No claims to "treat hair loss" (Healthcare & Pharma policy, doc 47 §4.4).
  - Branded content needs the toggle.
  - AIGC label is required.
  - Trending sounds are not licensed for ads: use the Commercial Music Library.
- **FTC:**
  - The Endorsement Guides apply. The measured creators mostly disclose ("#ad", "#DysonPartner", "#gisoupartner"); "not sponsored" must be true (Static H16).
  - The Fake Reviews Rule (2024) bans AI testimonials.
  - The mock-up doctrine (Colgate 1965) applies.
  - **New York synthetic-performer disclosure** (in force 9 Jun 2026) applies to any AI human in an ad (45 §5.3).
- **IP:**
  - Licensed collabs (Grinch × Kitsch, Mandalorian × O&J, Harry Potter × Glamnetic) are the brand's licence, not ours. **Spec films never reference real IP.**
  - Never mimic Dyson's grey-sweep visual identity closely (trade dress) [inf].
- **Age:**
  - Teen nail buyers are common (H8 is a teen). Keep teen-coded characters out of anything with "salon" adult contexts, and never generate minors (LESSONS).

### 5.5 Pre-flight checklist for this niche (add to 45 §5.4, 46 §7 and 47 §4.5)

1. **Hair length, type and density** on screen are within the claim's tested condition (*Dyson v. Dreame*).
2. **No AI hair, skin or nail result.** The proof slot holds client footage (with its date and "unretouched" if true).
3. No growth, loss, shedding or dandruff verbs. No "frizz-free", "no heat damage" or "fastest" without the matching test.
4. No glowing plates, smoke or burn cues. No tool near water.
5. Time on screen (clock, "10 minutes") equals a tested time **for the hair shown**.
6. Nails: ΔE ≤ 3 vs the swatch on the hero frame; shape and length per the reference; five fingers.
7. No negative self-perception address. Problem hooks are about objects and situations.
8. No real IP, no real agency (fire, rescue, security: fictional and unbadged), no real-person lookalikes.
9. AI people are disclosed (NY), the AIGC toggle is on, and the music is commercially licensed.

---

## 6. The buyer

### 6.1 Who signs a $1,200–3,500 film

| Brand size | Decider | Also in the room | How they buy | Evidence |
|---|---|---|---|---|
| <$5M (RevAir, TYME, Static, Mooncat class) | **Founder**, often the face (Ann McFerran still films for Glamnetic) | Contract media buyer | Card; fast; per-launch budgets | Static self-funded; founders on camera [m] |
| $5–20M (Crown Affair, Nailboo, Rizos class) | Founder + **Head of Growth** | **Creative strategist**, **TikTok Shop / affiliate manager** (new; owns Shop GMV and affiliate seeding), retail marketing (co-op) | Test-led; monthly creative budget | Nailboo: a quarter of the business is wholesale [c]; Wavytalk-style Shop GMV |
| $20M+ (Gisou, Divi, Kitsch) | Creative Director / Brand | In-house content team, agency | Vendor onboarding; IP licensing reviews | Volumes in D9 |

### 6.2 What they fear (in order of pain) [inf, grounded in §2–5]

1. **"AI hair looks fake, and the comments will roast us."** Hair is the hardest material; the audience is expert ("hairtok").
2. **"A false demo gets us an NAD or Dyson letter."** *Dyson v. Dreame* 2026 and the Shark cases are well known in tools.
3. **"It won't beat our UGC."** It probably won't as a standalone, and the measured data agrees (§0.1).
4. **Shade or nail mismatch → returns.** Nails are bought on colour and shape.
5. **Volume and cost.** They need 10–40 new creatives per week. One pretty film doesn't move their account.
6. **Drop timing.** Nail and hair-perfume drops are dated; late creative is worthless.

### 6.3 What proof makes them pay

- **Five free frames built on *their* real assets**: their real tool photo, their real nail set or shade, their real UGC still in the proof slot. Show where the AI part ends.
- **A "hook transplant" demo**: VXO's 3 s AI hook stitched onto *their own* best public UGC (with permission later; for the pitch, a mock-up on frames only). This shows the incremental value with zero risk to their winners.
- **The compliance gate (§5.5)** shown up front, citing *Dyson v. Dreame*: "we keep hair length inside your tested claim".
- **The variant math**: per film, 3 hook modules + a 15 s cutdown + a 6 s loop + 3 offer end-cards + stills. That adds 10–15 creatives to their weekly pipeline.
- **A test plan**: hook-transplanted UGC vs the original UGC, same body, same audience. Judge on hook rate (3 s views) and CPA. The cleanest A/B in performance marketing.

### 6.4 Re-buy triggers (what makes them rebook monthly)

| Trigger | Sub-niche | Cadence |
|---|---|---|
| **Collection drops** (seasonal, licensed, colourways) | Nails, hair perfume, tool colourways (T3 "Lemon Drop", Shark "Orchid") | Monthly to quarterly |
| **Creative fatigue** | All; median haircare creative lives 23 d and none reach 90 d (D2) | Every 3–4 weeks |
| **Retail launches** (Ulta, Target, Walmart, Sephora resets) | All | 2–4 per year |
| **Sales tentpoles** | Tools: Mother's Day, Prime Day, BFCM; haircare: 63 % discount ads | 4–6 per year |
| **A winning gag becomes a series** | Gisou POV repeated (H13 → H14) | Monthly "episode" |

**Package [inf]:**
- **Season ($3,500/mo)** = 1 drop film + 6 hook modules + 3 offer cards + 10 stills each month.
- **Premiere ($2,500)** = launch hero + modules.
- **Short ($1,200)** = hook modules only, the cheapest way to show lift.

### 6.5 Best outreach angle and a sample first DM (never sent)

**Angle:** "Your demos are good. Your first second isn't doing them justice." Lead with a *specific* public creative of theirs and a measured fact from this doc. Offer 5 frames, one of which is a hook transplant on their own tool or set.

**Sample first DM (founder of an invented reverse-air-dryer brand; NOT SENT):**
> Hi [Name], your salon one-take with the timer on screen is one of the strongest hair-tool ads I've seen this year: one shot, no tricks, the clock does the arguing. I run VXO, a small AI film studio. We don't replace demos like that; we build the 2-second opener that makes people stop on them (think "a roommate trying to rescue someone from your hose") and keep your real footage as the proof. Want 5 free concept frames on your actual dryer? If none of them beats your current first second, bin them. No call needed.

*(Rules: only after a dossier per `vxo-leads` §1.5; the owner approves; never claim knowledge of their metrics.)*

---

## 7. Lead signals: the niche scoring add-on for `.claude/skills/vxo-leads/SKILL.md`

Use the base 100-point score, then apply this **niche modifier (−25 to +20)**. HOT stays ≥70 after the modifier.

| Signal | Points | How to check (public) |
|---|---|---|
| **Drop calendar**: a collection, colourway or licensed drop in the next 45 days (nails, hair perfume, tool colours) | **+6** | Shopify `/products.json` (new handles, `published_at`), IG and TikTok "coming soon" posts, email sign-up pages |
| **Demo-heavy but hook-poor**: their creator demos open on a face or "hi guys" (no failure, result or object hook in second 1) | **+5** | Watch 5 of their public TikToks; tally the second-1 type |
| **Low creative volume for their ad count**: <10 new Meta creatives per week, or >50 % static/headline images | **+4** | Motion public page (motionapp.com/library/<brand>) or the Meta Ad Library |
| **TikTok Shop storefront active** with affiliate videos, but brand-made Shop videos are slideshows | **+3** | shop.tiktok.com/us/… listing; the brand's TikTok "Shop" tab |
| **New retail door** (Ulta, Target, Walmart, Sephora, Sally) announced in the last 90 days | **+3** | Trade press (Modern Retail, Glossy, Beauty Independent, Chain Drug Review) |
| **Tentpole within 6 weeks**: Mother's Day, Prime Day, BFCM for tools; Halloween, holiday, Valentine's for nails | **+2** | Calendar |
| **Hiring**: "UGC coordinator", "creative strategist", "TikTok Shop / affiliate manager" | **+2** | LinkedIn, Indeed, Shopify careers page |
| **Core claim is growth, loss, shedding or dandruff** (hero product) | **−10** | Product page and ads; we can't make their main claim |
| **Active NAD or competitor-claims dispute**, or a recall | **−8** | BBB National Programs search; CPSC recalls |
| **Mass China-based tool brands** (factory-direct, 100s of creatives per week, no founder) | **−7** | Motion volume (TYMO 688/wk), About page |
| **Formaldehyde straighteners / relaxers** | **−25 (exclude)** | Ingredient list |

**Very hot pattern for this niche [inf]:** a founder-led $2–15M nail or hair-tool brand with a drop in ≤45 days, ≥20 active Meta ads, <10 new creatives per week, creator demos that start with a face, and a TikTok Shop listing. Example *type* (not a target): "reusable press-on brand, Halloween drop on 10/1, 47 active ads, 3 new per week."

---

## 8. Ten ready film concepts (invented brands, VXO spec)

House rules for all ten:
- Invented brands and packs. No real-brand look-alikes.
- **No AI hair or nail result.** Every "it works" moment is the client's **proof slot** (marked PROOF) with real footage.
- AI people appear only as comedy characters, with the NY disclosure line.
- All rescue, security or crew uniforms are fictional and unbadged.
- Every camera is a real rig. Physics numbers are approximate real-world values [approx].
- Otto and Vee do not appear (client-style specs).
- Costs use 43 §6 list prices:
  - Seedance 2.5 r2v 15 s: 480p test $3.09, 720p ×3 takes $20.79; 10 s: $2.06 / ×3 $13.86;
  - Kling 3.0 Pro i2v 5 s, sound off: $0.48 per take;
  - Cinema Studio 4.0 720p: ≈$0.46/s;
  - Wan 3.0 480p previs: $0.05/s;
  - stills: ≈$0.30 product-ref, ≈$0.01 world.

---

### C1 ★ · STRAYT (flat iron with 60-min auto shut-off) — "Next Stop" (15 s) — foot-chase grammar, zero AI hair

**Logline:** on a commuter train a woman remembers the straightener. She sprints back home across the city. At home the iron has already switched itself off. It was never her problem.

**Hook (0–1 s):** the train doors are closing. A hand slams between them and she is already squeezing out, sprinting before her second foot lands. Super: "**8:14 a.m. Did I turn off the straightener?**"

**Punchline (product-caused):** she bursts into the bathroom, out of breath. The iron lies on the counter with its LED reading "**OFF · 0:00**". The cat is asleep beside it, unbothered. She touches the plate (cool), sits on the edge of the tub, and checks her phone: "**Late for work**". Super: "**Shuts itself off after 60 minutes. You can't.**" (The auto-off spec must be the client's real one.)

| # | Time | Shot (real rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.4 | Platform-level tripod, 35 mm, locked | Doors closing; she squeezes through, already running (motion at frame 0) |
| 2 | 1.4–3.0 | Handheld chase (operator running behind, gimbal) | Down the station stairs, two steps at a time, bag swinging |
| 3 | 3.0–4.6 | Long-lens static from a footbridge (200 mm) | She crosses a park diagonal, pigeons scatter |
| 4 | 4.6–6.0 | Low dolly / Steadicam side-tracking at hip height | She hurdles a low hedge, lands, keeps going |
| 5 | 6.0–7.4 | Insert, Kling i2v (bathroom counter, locked macro) | The STRAYT iron on stone; the LED countdown "0:01 → OFF" clicks; a 1 s cool-down chime |
| 6 | 7.4–9.0 | Stairwell, wide, tripod looking up | She takes the apartment stairs, hand on the rail |
| 7 | 9.0–10.6 | Bathroom doorway, tripod (no mirror in frame) | The door flies open; she freezes |
| 8 | 10.6–12.4 | Close, locked | Her hand hovers over the plate, then touches it: nothing. The cat opens one eye |
| 9 | 12.4–15.0 | Packshot, Cinema Studio dolly-in on the counter | Iron with "OFF" LED; super + CTA; optional 1.5 s PROOF slot of the client's real auto-off test |

**Physics/realism check:**
- A sprinter covers ≈7 m/s, and a commuter running in shoes ≈4–5 m/s. Write her pace as 4 m/s, with "bag strap slips off the shoulder once".
- Stairs: 2 steps per stride, about 0.35 s per stride.
- A hedge hurdle is ≤60 cm high, with a two-foot landing and knees absorbing.
- Ceramic plates cool from ≈200 °C to touchable (<45 °C) in ≈20–30 min [approx]. So after 60 min off, a cool plate is true.
- The cat is one animal, ≤5 s, from a real photo (LESSONS).
- No reckless crossing of roads; she uses a footbridge and a park (TikTok: no dangerous vehicle or road behaviour).
- No hair on screen except her ponytail in the chase.

**Audio map:**
- 0.0 door chime + pneumatic hiss;
- 0.6 a hand thump on the door;
- 1.4 a running-shoe slap rhythm (≈2.5 steps/s) begins and stays as the bed;
- 3.2 pigeon wing flaps;
- 4.9 the hedge rustle and a landing thud;
- 6.0 a soft electronic "click-chime" on the LED;
- 7.4 a stairwell echo;
- 9.0 the door bangs the wall stopper;
- 9.2 **silence** (the joke beat);
- 11.0 a cat purr;
- 12.4 bed in (dry, plucky bass, 96 bpm);
- 13.5 VO tagline (locked brand voice) "STRAYT. It remembers.";
- 14.6 sonic logo.
- No music under the chase (shoes are the rhythm).

**Model/template:** 43 §7.2 adapted (a human action multi-shot, Seedance 2.5 r2v, 10 s, shots 1–4 + 6–8 split into two clips); shot 5 Kling 3.0 Pro i2v from the client's real iron photo; shot 9 Cinema Studio 43 §7.3.

**Est. cost:** 8 stills $1.50 + Wan previs $0.75 + Seedance 2 × 10 s at 480p $4.12 + 720p × 3 takes × 2 clips $27.72 + Kling 2 × 2 $1.92 + CS 3 s × 2 $2.77 ≈ **$39**.

**Why best:**
- "Did I leave the straightener on?" is the category's universal anxiety.
- It is a *real* product feature (auto-off), and it causes the punchline.
- The film needs **no AI hair at all**.
- It matches the owner's bar (Red Light: grounded action + deadpan reversal + the product at the centre).
- It sells to *every* heated-tool brand with auto-off.

---

### C2 ★ · TWIRLA (auto-rotating curler with one-tap reverse) — "Jaws of Life" (15 s) — rescue-crew deadpan

**Logline:** a rotating curler eats a lock of hair and stops at the scalp. She calls for help. A three-person rescue crew arrives with hydraulic spreaders. She presses one button.

**Hook (0–1 s):** macro: the barrel is winding a lock, motor whining, and stops 3 cm from the scalp with a click. Super: "**Day 1 with a rotating curler.**" (This copies the measured hook class: Wavytalk "why is it stuck", 6.2M.)

**Punchline:** as the crew chief lowers the spreader toward her head, she taps "REVERSE". The barrel unwinds two turns and the curl slides free (**PROOF: the client's real footage of the reverse**). The chief stops, lowers the jaws, and his colleague silently picks up a traffic cone from the bath mat. Super: "**One-tap reverse. Every tangle has an exit.**"

| # | Time | Shot (real rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.2 | Macro on a slider, 100 mm | Barrel winds clockwise, stops 3 cm from the scalp; hair pulled taut (failure, not result) |
| 2 | 1.2–2.6 | Bathroom doorway, tripod, medium | She sits frozen on a stool, tool hanging at her temple, phone at her ear |
| 3 | 2.6–4.0 | Across-street tripod, wide | An unmarked red rescue truck stops (nose dips), three crew hop out with a hydraulic spreader and cones |
| 4 | 4.0–5.6 | Steadicam leading through the hallway | The crew walk in single file, carrying the 20 kg spreader two-handed |
| 5 | 5.6–7.2 | Medium, locked | The chief kneels, sets a cone on the bath mat; the spreader hisses open 5 cm |
| 6 | 7.2–8.6 | Insert, Kling i2v from the real tool photo | Her thumb taps the REVERSE icon; the LED blinks twice |
| 7 | 8.6–10.6 | **PROOF: client footage** | The real barrel reverses, the real curl releases and bounces |
| 8 | 10.6–12.6 | Two-shot, locked | The chief lowers the jaws slowly; the colleague picks up the cone without a word |
| 9 | 12.6–15.0 | Packshot, Cinema Studio dolly-in | Tool on the counter beside one orange cone; super + CTA |

**Physics:**
- A 25 mm barrel wraps ≈7.9 cm of hair per turn, so a 30 cm lock needs ≈4 turns. The film shows 3 turns, a stop, then a 2-turn release.
- Auto curlers rotate ≈1 turn per 0.8–1 s [approx], so write "1 turn per second".
- A hydraulic spreader weighs ≈18–22 kg: shoulders drop and both hands carry it.
- The truck stops with a ≈2° nose dip.
- No sirens (no false-emergency cue). No agency names.
- The hair is never shown "free" in AI. Shot 7 is real.

**Audio map:**
- 0.0 motor whine rising;
- 0.9 a hard motor-stall click;
- 1.4 a phone dial tone;
- 2.8 an air-brake hiss + door slams;
- 4.0 boots on floorboards (3 people, out of step);
- 5.8 the cone tap on tile;
- 6.4 a hydraulic pump hiss;
- 7.4 a button "tick" + 2 LED beeps;
- 8.6 the real reverse-motor sound from the proof clip;
- 10.6 silence;
- 11.8 the cone lifted (plastic scrape);
- 12.6 bed in (deadpan brass stab, 90 bpm);
- 13.6 VO "TWIRLA. Undo, on demand.";
- 14.6 logo sting.

**Model/template:** Seedance 2.5 r2v 15 s multi-shot (shots 2–5, 8; refs: woman sheet, crew sheet, bathroom plate clean of mirrors, truck sheet unbranded); 43 §7.5 comedic-reveal structure for 8; Kling for 1 and 6; CS for 9.

**Est. cost:** 9 stills $1.80 + Wan $0.75 + Seedance 480p $3.09 + 720p ×3 $20.79 + Kling 2×2 $1.92 + CS $3.70 ≈ **$32**.

---

### C3 ★ · CLAWSET (2-week press-on nails) — "Pit Crew" (15 s) — motorsport grammar for a soda can

**Logline:** a woman with a fresh $90 salon gel manicure won't risk opening her can of sparkling water. A four-person pit crew slides in and opens it in 2.1 seconds. At the next table, a CLAWSET wearer flicks hers open with one nail.

**Hook (0–1 s):** a low dolly at floor level as four crew in race suits slide on their knees into frame around a café table (motion at frame 0). Super: "**Fresh gel. Can of seltzer.**"

**Punchline:** the timer board flips to "**2.1 s**", the crew bump fists, and then they hear *pshh* from the next table: a woman opens her can with one press-on nail, without looking up. All four crew turn their heads in sync. Super: "**Press-ons that work. [Client's tested wear: 14 days]**". PROOF: the client's real tab-flick and day-14 hand.

| # | Time | Shot (real rig) | Action |
|---|---|---|---|
| 1 | 0.0–1.2 | Floor-level dolly, 24 mm | Four crew knee-slide in, about 0.5 m each on polished concrete |
| 2 | 1.2–2.4 | Overhead locked (arm) | Hands lay out tools on the table: a tab lifter (spudger), a towel, a can-cooler "jack" |
| 3 | 2.4–3.6 | Close on the woman's hands (Kling from the real gel-mani plate) | Ten glossy nails hover, refusing to touch the can |
| 4 | 3.6–5.0 | 50 mm, handheld | The crew chief raises a lollipop sign "**OPEN**" |
| 5 | 5.0–6.4 | Macro, locked (Kling) | The spudger under the tab; the tab lifts; carbonation hiss and a tiny foam crown |
| 6 | 6.4–7.6 | Insert, locked | A flip timer board clacks to "2.1" |
| 7 | 7.6–9.0 | Medium, tripod | Fist bumps |
| 8 | 9.0–10.6 | **PROOF: client footage** | The real CLAWSET hand flicks a can tab open with one nail |
| 9 | 10.6–12.4 | Wide, tripod | Four heads turn in sync toward the next table |
| 10 | 12.4–15.0 | Packshot (Cinema Studio), the CLAWSET pack beside an open can | Super + CTA |

**Physics:**
- A can tab needs ≈20–30 N at the tip [approx], so write "the tab resists, then pops with a crack".
- Can pressure ≈2–3 bar: the hiss lasts ≈0.3 s and the foam crown is <5 mm (seltzer, not soda).
- Knee slides on race suits over polished concrete: ≈0.4–0.6 m.
- The crew do not touch the woman (no contact).
- The flip board is a real mechanical clack.
- Nail ΔE and shape come from the client's set (§4).

**Audio map:**
- 0.0 four knee-slide scuffs staggered by 80 ms;
- 1.4 tool clatter on laminate;
- 3.8 an air-horn "go" (short, quiet, diegetic);
- 5.2 the tab crack + hiss;
- 6.4 the flap-board clack ×2;
- 7.8 fist bumps;
- 9.0 a single *pshh* off-screen (the joke);
- 10.6 a café room tone swell;
- 12.4 bed in (synth-funk 110 bpm);
- 13.8 VO "CLAWSET. No crew required.";
- 14.7 sting.

**Model/template:** Seedance 2.5 r2v 15 s, "EXACTLY TEN SHOTS AND NINE HARD CUTS" (43 rule 2; split into 2 × 8 s clips if the shot count fails); Kling for 3 and 5; CS for 10.

**Est. cost:** 10 stills $2.10 + Wan $0.75 + Seedance 2 × 8 s at 480p $3.30 + 720p ×3 × 2 $22.18 + Kling 2×2 $1.92 + CS $3.70 ≈ **$34**.

---

### C4 · PEELGEL (semi-cured gel strips) — "Hands Up" (15 s) — the wet-polish penguin

**Logline:** fifteen minutes of wet polish turn a woman into a hands-up penguin: she opens doors with her elbow, wears her coat by gravity, signs for a parcel with her nose. Her neighbour does her nails in the hallway with gel strips and a 60 s lamp and takes the parcel for her.

**Hook (0–1 s):** she freezes mid-step in a hallway, fingers splayed like a surgeon after scrubbing. Super: "**Wet polish. Minute 3 of 15.**"

**Punchline:** the courier hands the scanner to the neighbour, who signs with a perfect gel nail; the lamp behind her clicks "60". Super: "**Peel. Press. Cure 60 s. Done.**" (PROOF: the client's real strip application.)

**Shots (8):**
1. 0–1.2: corridor, tripod: the freeze.
2. 1.2–2.8: close: an elbow presses the elevator button.
3. 2.8–4.4: medium: she shrugs into a coat without hands (it slides on half-way).
4. 4.4–6.0: doorway: the courier offers a stylus; she leans to sign with her nose (stops short).
5. 6.0–8.0: **PROOF**: the neighbour's real strip peel and press.
6. 8.0–9.4: Kling insert: the violet LED lamp, timer "60 → 0".
7. 9.4–11.2: two-shot: the neighbour signs and takes the parcel.
8. 11.2–15: packshot.

**Physics:**
- Regular polish is touch-dry in ≈10–15 min [approx].
- Semi-cured gel strips need ≈60 s under LED [c-typical].
- Coat physics: the sleeve catches on the elbow, half-on.
- The lamp interior glows violet.

**Audio map:**
- room tone;
- 1.4 the elevator ding;
- 3.0 coat fabric swish;
- 4.6 the courier scanner beep;
- 6.0 a strip peel "tck";
- 8.0 the lamp fan + a 60 s beep (time-compressed);
- 9.6 the stylus scratch;
- 11.2 bed in;
- 13.5 VO tagline.

**Model:** Seedance 15 s r2v + Kling ×2 + CS.

**Est. cost:** ≈ **$27**.

---

### C5 · VOLTA (magnetic cat-eye polish) — "Laser" (10 s) — loopable

**Logline:** a magnet wand draws a silver light band across a wet nail. The band slides as the hand tilts, and the house cat tracks it like a laser pointer.

**Hook (0–1 s):** macro: a silver band "pours" across a deep-plum nail as the magnet passes 5 mm above it. Super: "**Magnetic. Literally.**"

**Punchline:** she tilts her hand. The cat's head follows. The cat pounces gently onto her wrist (paws only, no claws). Super: "**Your cat will notice first.**"

**Shots (6):**
1. 0–1.5: macro from a real nail-set photo (Kling): the band forms.
2. 1.5–3: close: the hand tilts 15°, the band shifts 2 mm.
3. 3–4.5: Kling from a real cat photo: the cat's eyes and head track left-right.
4. 4.5–6: medium, locked: the hand tilts back; the cat crouches, hind legs wiggle.
5. 6–7.5: soft pounce; paws land on the wrist; she laughs (face cropped).
6. 7.5–10: packshot: bottle + magnet wand on a velvet tray; loop point back to shot 1.

**Physics:**
- The magnet is held 3–5 s, 3–5 mm away; the band appears within 2 s.
- The band position follows the viewing angle (a 2 mm shift per 15° tilt).
- One animal, ≤5 s per shot, from a real photo (LESSONS).
- No claws on skin.

**Audio map:**
- 0.0 a soft magnetic "thrum" (designed);
- 1.6 a cat chirp;
- 3.2 tail swish;
- 5.0 a hind-leg wiggle on a rug;
- 6.2 a paw thump;
- 6.5 one laugh breath;
- 7.5 a sparkly bed (100 bpm);
- 9.0 a sting that loops into the 0.0 thrum.

**Model:** Kling 3.0 Pro i2v ×5 shots (first/last frames for 2 and 4) + CS packshot.

**Est. cost:** 6 stills $1.80 + Kling 5 × 2 takes $4.80 + CS 2.5 s × 2 $2.30 ≈ **$9**. The cheapest concept to show range.

---

### C6 · ROAMER (dual-voltage multi-styler) — "Bag Check" (15 s) — the clown-car suitcase

**Logline:** at a fictional airport security belt, an officer pulls an impossible number of hair tools out of one carry-on. The traveller behind has one ROAMER case.

**Hook (0–1 s):** gloved hands pull a hair dryer from a carry-on, then a straightener, then a curling wand, without pause. Super: "**Carry-on. Hair 'essentials'.**"

**Punchline:** the line behind lengthens. The next traveller's small case opens to show one styler and 3 attachments. The officer waves her through without touching it, and the first bag keeps producing (a diffuser, a plug-adapter tower). Super: "**One tool. Five styles. 110–240 V.**" (Use the client's real voltage and attachment count.)

**Shots (8):**
1. Overhead locked on the tray (items stacking).
2. Medium on the officer (deadpan; unbadged "SECURITY").
3. Wide, long lens: the queue snaking.
4. Close: the adapter tower pulled out (the comic peak).
5. Medium: the second traveller places the small case.
6. Kling insert: the ROAMER case opens (real product photo).
7. Two-shot: the wave-through.
8. Packshot in a hotel-bathroom plate, Cinema Studio.

**Physics:**
- Items are drawn in order of size, and the bag visibly sags as it empties (cloth physics).
- Each tool has its cord coiled with a Velcro tie.
- The count stays ≤8 items so it remains "almost possible" (comic exaggeration, no claim).
- No TSA or real agency names (FTC impersonation rule, 45 §5.2).

**Audio map:**
- belt rollers;
- 0.4, 1.2, 2.0, 2.8: four "clunk"s on the tray (accelerating comic rhythm);
- 4.0 a queue murmur;
- 6.0 a case zip;
- 7.0 a soft "ding";
- 9.0 a gate beep;
- 11.0 bed in;
- 13.5 VO.

**Model:** Seedance 15 s r2v + Kling ×2 + CS.

**Est. cost:** ≈ **$30**.

---

### C7 · HUSH (quiet high-speed dryer) — "Quiet Zone" (12 s) — library deadpan

**Logline:** a woman dries her towel-wrapped hair in a silent library. Nobody looks up. The librarian walks over, pauses, and shushes the student opening a crisp packet instead.

**Hook (0–1 s):** an ECU of a turning page with an absurdly loud paper crackle. A "QUIET" sign is in soft focus. Super: "**Quiet zone.**"

**Punchline:** the librarian holds a handheld sound-level meter toward the dryer: it reads the client's tested number (e.g. "**59 dB**"). She turns to the crisp packet: "**71 dB**". "Shh." Super: "**HUSH. [Client's tested dB at 1 m].**"

**Shots (7):**
1. The page macro.
2. Wide, symmetric tripod: the reading room.
3. Medium: she unwinds the towel partway, the dryer on (hair stays mostly in the towel, so no hair-result shot).
4. The librarian walks, Steadicam.
5. Kling insert: the meter display.
6. Reverse: the crisp packet, the meter, "Shh".
7. Packshot.

**Physics and claim check:**
- **The picture is the claim.** The meter numbers must be the client's tested values at a stated distance.
- A crisp packet opening measures ≈70–75 dB at close range [approx]; the student is 1 m from the meter.
- The library ambience is ≈35–40 dB.
- No implication that the dryer is silent.

**Audio map:**
- a 38 dB room tone;
- 0.2 a page crackle (exaggerated);
- 3.0 a *quiet* dryer whoosh, mixed low;
- 5.0 footsteps on carpet;
- 6.5 meter beeps;
- 8.0 the crisp crackle;
- 8.6 "Shh";
- 9.5 bed in (soft piano);
- 11.0 VO.

**Model:** Seedance 10 s r2v + Kling ×2.

**Est. cost:** ≈ **$19**.

---

### C8 · HALO (hair perfume) — "The Fraud" (15 s) — elevator deadpan

**Logline:** everyone in the elevator compliments her perfume, and she keeps saying "thank you". Then we see where she sprays it: her hair. A man asks the name; she hands him the bottle; he sprays his beard.

**Hook (0–1 s):** a close-up of a stranger leaning in slightly and inhaling. Super: "**Floor 3. Compliment No. 4.**"

**Punchline:** the floor counter keeps rising; the bottle passes hand to hand; the man mists his beard; the elevator doors open on a lobby full of people turning their heads. Super: "**Scent lives in hair. [Client's tested wear hours].**"

**Shots (8):**
1. The inhale close-up.
2. Medium, locked from the elevator corner (a real rig: a corner clamp).
3. The floor-indicator insert (generic numbers).
4. Flashback insert (Kling): the mist cone over hair in a bathroom (a 25 cm cone, backlit, droplets settle in 1 s, no hair "result").
5. The man asks.
6. The beard mist.
7. The doors open, lobby heads turn.
8. Packshot.

**Physics:**
- An aerosol mist forms a ≈25 cm cone that dissipates in 1 s.
- Elevator doors take ≈3 s to open.
- No AI hair change. Real hair shows only in the optional PROOF slot (a creator's real use).

**Audio map:**
- elevator hum;
- 0.3 an inhale;
- 1.5 a "ding" per floor;
- 4.0 a mist spritz ×2;
- 7.0 "What is it?" (lips visible → Seedance dialogue block, 43 §7.4 B);
- 9.0 the beard spritz;
- 10.5 doors + lobby murmur;
- 11.5 bed;
- 13.5 VO.

**Model:** Seedance 15 s r2v (dialogue) + Kling ×2 + CS.

**Est. cost:** ≈ **$30**.

Measured analogue: Gisou × Alysia "I think I'm actually a fraud" (613K, paid) [m].

---

### C9 · VORTA (reverse-air dryer) — "Rescue Attempt" (15 s) — the scary-looking machine

**Logline:** a roommate walks in and sees her friend's head "being eaten" by a hose. She lunges to save her and pulls the plug. Then she sees the dry, stretched half. She sits down and feeds her own hair in.

**Hook (0–1 s):** a doorway POV: a ribbed hose leads from a humming canister to a woman's head, the hair disappearing into it. A mug drops from the roommate's hand (mid-fall at frame 0). Super: "**What the roommate saw.**"

**Punchline:** after the plug is pulled, a half-and-half reveal: one side dry and stretched, the other side wet. (**PROOF: the client's real half-dry footage**, the measured RevAir device H17.) The roommate's face: a slow blink. Next shot: she is sitting on the floor with *her own* hair in the wand. Super: "**It looks strange. It dries in [client time] for [client hair length].**"

**Shots (8):**
1. The doorway POV + the mug falling.
2. The roommate lunging, Steadicam.
3. Kling insert: the plug pulled from the wall socket (a real plug photo).
4. Medium: the hum dies; the user looks up, annoyed.
5. **PROOF**: the real split hair.
6. Close: the roommate's slow blink.
7. Wide: both on the floor, the roommate's head in the wand (hair hidden by the hose; no AI result).
8. Packshot (Cinema Studio orbit of the canister).

**Physics:**
- A ceramic mug falls 1 m in ≈0.45 s and shatters into 3–5 pieces.
- The hose is ribbed, 1.5–2 m long, and keeps its diameter.
- The suction-on/off hum cuts within 0.2 s.
- Hair length in the proof slot = the claim length (*Dyson v. Dreame*).

**Audio map:**
- 0.0 a canister hum (low, steady);
- 0.45 the mug shatter;
- 1.0 a gasp (off-mic);
- 2.4 the plug yank + the hum dropping in pitch;
- 4.0 "Seriously?";
- 5.0 a silence beat;
- 7.0 the hum restarting;
- 8.5 bed;
- 13.5 VO.

**Model:** Seedance 15 s r2v + Kling + CS.

**Est. cost:** ≈ **$29**.

---

### C10 · DAYTHREE (dry shampoo) — "Do Not Disturb" (12 s) — the abandoned shower tableau

**Logline:** the shower has been abandoned for three days. A spider has spun a web across the showerhead, the loofah hangs like a retired flag, and a tiny "Out of office" card is taped to the tile. In the next room she sprays dry shampoo and leaves.

**Hook (0–1 s):** a macro of a dew-dotted spider web across a dry showerhead, light raking. Super: "**Day 3.**"

**Punchline:** the front door clicks shut (she's gone, fresh). In the bathroom the loofah finally drops off its hook onto the tray. Super: "**Skip the wash. Not the plans.**"

**Shots (7):**
1. The web macro (Kling).
2. A slow push on the loofah (Kling).
3. The "Out of office" card (a post supers the text; the card is blank in generation).
4. Bedroom, medium, locked: she sprays at the roots from 30 cm (a white plume settles in 2 s); the face turned away.
5. Brush-out, a back-of-head close (Seedance 720p; no before/after).
6. The door closes, from the hallway.
7. The loofah drops; packshot on the vanity.

**Physics:**
- Spray from 25–30 cm; the powder plume is visible ≈1–2 s, then settles downward.
- The web is dry (no dew if the room is dry; a light dust instead).
- The loofah falls ≈20 cm onto the tray with one bounce.

**Audio map:**
- a bathroom drip (single, slow);
- 0.5 a fly buzz far off;
- 3.6 an aerosol hiss 1.2 s;
- 5.0 brush strokes ×3;
- 7.0 keys + door click;
- 8.0 silence;
- 8.6 the loofah thud;
- 9.0 bed;
- 10.8 VO.

**Model:** Kling ×5 tableau shots + Seedance 5 s (shots 4–5) + CS.

**Est. cost:** ≈ **$15**.

---

### 8.1 Concept scorecard

| Concept | Sub-niche | Hook class (measured analogue) | Proof route | Claim risk | AI difficulty (1 easy–5 hard) | Est. spend |
|---|---|---|---|---|---|---|
| **C1 Next Stop ★ (best)** | Hair tool (auto-off) | Category anxiety + action | Feature spec + optional real test | Low | 3 (no hair) | $39 |
| **C2 Jaws of Life ★** | Rotating curler | Tangle (Wavytalk 6.2M) | Real reverse clip | Low | 3 | $32 |
| **C3 Pit Crew ★** | Press-ons | Salon-gel fear + ordeal (apple test 2.3M) | Real tab flick + day-14 hand | Medium (wear claim) | 4 (crew + nails) | $34 |
| C4 Hands Up | Gel strips | Wet-polish failure | Real application | Low | 3 | $27 |
| C5 Laser | Magnetic polish | Visual intrigue | Real nail macro | Low | 2 | $9 |
| C6 Bag Check | Travel multi-styler | Clown-car gag | Spec (voltage) | Low | 3 | $30 |
| C7 Quiet Zone | Quiet dryer | Sound gag | Tested dB | **High if dB untested** | 2 | $19 |
| C8 The Fraud | Hair perfume | "I'm a fraud" (Gisou 613K) | Wear-hours test | Low | 3 (dialogue) | $30 |
| C9 Rescue Attempt | Reverse-air dryer | Weird machine (RevAir 26.3M) | Real split hair | Medium (time and length) | 3 | $29 |
| C10 Do Not Disturb | Dry shampoo | Tableau | None needed | Low | 2 | $15 |

**The single best concept: C1 "Next Stop" (STRAYT flat iron with auto shut-off).**
- It turns the category's most universal anxiety into a grounded foot chase with a deadpan reversal.
- The punchline is caused by a real feature, not a depicted result. That makes it legally clean and needs no proof-slot dependency.
- It needs **no AI hair**, the niche's hardest material.
- It can be re-cut for any heated-tool brand that has auto-off.

**Spec order:** C1 first. Then C5 as the $9 nail loop to show range. Then C2 to show the "failure hook" class the data favours.

---

## 9. Ten surprising insights nobody asked for (that would make VXO better)

1. **Sell "hook transplants", not films.** In this niche the body of the ad (a real creator demo) already works, and the measured losers are brand-made polish. VXO's highest-ROI product is a **3 s AI hook module** stitched onto the client's existing winning UGC. Test it as hooked vs original, same body. It is cheap (one Kling or Seedance shot), fast, measurable on hook rate, and needs a new one every 3–4 weeks. Add it as a SKU under the Short tier: "6 hook modules = $1,200".
2. **A winning gag becomes a series.** Gisou ran the same POV staircase carry twice: 1.6M organic, then 1.3M paid, 5 months apart [m]. Pitch a **"format franchise"**: one gag skeleton, re-shot per drop (new bottles, new season). AI makes the re-shoot nearly free, because the location, camera move and timing are locked by the first episode. This is the strongest Season argument in VXO's research.
3. **The niche's paid winners are long, so VXO must deliver modules.** The paid median here is ≈43 s; beauty's is 11 s (47). A 15 s film is the wrong unit. The right deliverable is **hook (3 s) + world/turn (6–8 s) + offer card (2 s)**, designed to sandwich the client's demo. Update the `vxo-film` templates with a "sandwich" layout for tool brands.
4. **The best proof device is a clock, and AI can't fake it.** Sorry: AI *can* fake it, and that's the problem. RevAir's "12:39" and Shark's "three minutes" are trusted because they're one-take footage. **A clock inside an AI scene is a claim** (*Dyson v. Dreame*). Rule: VXO never puts a time on screen that isn't the client's tested time for the hair shown.
5. **Before/after is the scarcest hook (0.1 % of haircare videos) and the longest-living (1.9×).** Brands avoid it out of fear. Meta explicitly allows hair-product before/after without negative self-perception. VXO can offer a **"compliant before/after kit"**: real client footage in a designed split-frame with test captions and an AI-built frame world (a ruler, a stopwatch, a lab tray). It is compliant and rare, so it stands out.
6. **Hair is the hardest AI material, so design films with no hair in them.** C1, C5, C6 and C10 barely show hair. The niche-wide trick is to tell hair stories through **objects**: the iron, the cord, the vacuum roll, the cone, the clock. This avoids the hardest render and the legal trap at once.
7. **The second buyer is the TikTok Shop / affiliate manager.** Haircare on TikTok Shop is +118 %, and Wavytalk did $15M in one quarter. Affiliates copy "seed videos". VXO can sell **affiliate brief films**: a 15 s AI "how it should look" reference plus a shot list that hundreds of affiliates imitate. One film, hundreds of derivative ads. This is a new sales channel none of the earlier niche docs found.
8. **Loudness betrays the splice.** Brand-mastered posts measured −12 to −16 LUFS (Dyson clipped at +3.2 dBFS); creator-native posts sat at −25 to −36 [m]. When a VXO hook is stitched onto UGC, ride the hook down to the UGC's level at the seam, then master the whole to −14 LUFS / −2 dBTP (46). Otherwise the jump announces "ad here". Add a "splice loudness" check to `qc_report.py`.
9. **Founder-led brands make ~3–7 new creatives per week; the leaders make 37–688.** Static (3/wk), Nailboo (7/wk), JVN (5/wk) and K18 (5/wk) vs Glamnetic (37), Kitsch (173) and TYMO (688). The founder-led bottleneck is *volume*, not quality, so pitch the Season plan as "+12–20 creatives a month". The measured volume gap is the evidence, and it's checkable for each lead on Motion's public page in 30 seconds (§7).
10. **The EU TPO ban created a content wave the US hasn't noticed.** Gel brands that are TPO-free (or reformulating) have a new, *factual* claim and a reason to re-shoot their whole library. A drop film with "made without TPO" (if true), in a clinical-chic world, is a ready pitch for US gel-kit brands (Gelcare / Le Mini Macaron class) [inf].

*Bonus:*
- **Weird devices sell themselves.** The stranger the tool looks (RevAir: 26.3M, 1.0M), the less the ad has to explain. VXO's AI is best used for the **"inside the machine" cutaway**: an x-ray of the airflow, or a cross-section of the barrel. Viewers have no realism expectation for these, and AI renders them cleanly.
- **The Nimble robot shows that nail *devices* travel as tech** (1 % share rate). Pitch nail devices with gadget grammar (51), not beauty grammar.

---

## 10. QA gate additions for this niche (run with 46 §7 and 45 §5.4)

- [ ] Hair length, type and density on screen ≤ the tested claim condition (*Dyson v. Dreame*), checked at every cut on the 2 fps strip.
- [ ] No AI hair or nail result. The proof slot is filled with dated client footage, or the film runs as awareness only.
- [ ] Plates never glow or smoke. Cords are continuous. The button layout matches the reference.
- [ ] Nails: count, shape and length per finger match the hand plate; ΔE ≤ 3 on the hero frame.
- [ ] Any clock, timer, dB, voltage or "minutes" on screen = the client's spec, with the source noted in the job file.
- [ ] Problem hooks address objects and situations, never the viewer's body ("your hairline…").
- [ ] Rescue, security and crew are fictional and unbadged. No real IP. Music is cleared.
- [ ] Splice loudness: the hook-to-UGC seam step is ≤3 dB before the final master.

---

## Sources

**Measured (scratchpad only, not committed)** — TikTok posts by URL in §2.1: @myrevair 7596389334874443021, 7236414907824999722; @abigaillinnn 7273892789786643755; @briannenhowey 7528092738940718367; @mo__styles 7608692379591249165; @k18hair 7393403629849300255; @alysialoo 7390075205349068074; @valeria_deldinova 7336920067810102560; @chelseygobbo 7429060659708431662; @glamzilla 7647739109007445256; @dyson_usa 7475815898503220510; @anggwells 7328440181575421230; @uptin 7345177050333990177; @gisou 7466921889588399382, 7525532113102277920, 7525210652365933857, 7369709172767673633; @golloria 7431011606303083818; @sammypur 7327827381610122538; @bondiboost 7528185552521170207, 7486868882792402222; @annmcferran 7512626566317378862; @glamnetic 7299259191313616171, 7533887976552549645, 7574527786950397198, 7515547712318770478, 7249919956194823467; @nailboo 7560832929048415519; @salomeandreaa 7387450501551443230; @kitsch 7573775017108983070; @sharkbeauty 7608222442540092702. Views and likes are from a `yt-dlp` metadata snapshot on 2026-10-09.

**Meta creative activity (public snapshot, ~Jun 2026):** Motion Inspo Library pages for [tymo-beauty](https://motionapp.com/library/tymo-beauty), [shark-beauty](https://motionapp.com/library/shark-beauty), [k18-hair](https://motionapp.com/library/k18-hair), [static-nails](https://motionapp.com/library/static-nails), [glamnetic](https://motionapp.com/library/glamnetic), [olive-and-june](https://motionapp.com/library/olive-and-june), [kitsch](https://motionapp.com/library/kitsch), [gisou](https://motionapp.com/library/gisou), [switch-nails](https://motionapp.com/library/switch-nails), [doonails](https://motionapp.com/library/doonails), plus amika, bellami-hair, bondiboost, briogeo, chillhouse, divi, dyson, ghd, jvn-hair, kiss-nails, luxy-hair, moroccanoil, nailboo, nutrafol, olaplex, ouai, prose and vegamour at motionapp.com/library/<slug>. The Meta Ad Library itself returned 403 to automated fetches.

**Benchmarks:** [Benly haircare Q1 2026](https://benly.ai/benchmarks/q1-2026/beauty-personal-care/haircare) · [Benly makeup Q1 2026](https://benly.ai/benchmarks/q1-2026/beauty-personal-care/makeup-cosmetics) · [Beauty Independent: TikTok Shop Q2 2026](https://www.beautyindependent.com/tiktok-shop-nears-1b-beauty-sales-second-straight-quarter/) · [Beauty Independent: TikTok Shop Q1 2026](https://www.beautyindependent.com/?p=188868) · [Beauty Independent: holiday haircare](https://www.beautyindependent.com/?p=180109) · [Beauty Independent: haircare hottest category](https://www.beautyindependent.com/haircare-prestige-beauty-hottest-category/) · [BeautyMatter H1 2025](https://beautymatter.com/articles/us-beauty-industry-grows-in-h1-2025) · doc 47 (Billo, AI trust).

**Companies:** [SharkNinja 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm) · [Helen of Troy Q3 FY26](https://s2.q4cdn.com/117307772/files/doc_financials/2026/q3/Helen-of-Troy-Limited-Reports-Third-Quarter-Fiscal-2026-Results-2026.pdf) · [Digital Commerce 360: Olive & June](https://www.digitalcommerce360.com/2024/11/25/helen-of-troy-acquires-olive-june/) · [CEW: KISS](https://cew.org/?p=92953) · [Glossy: Static Nails](https://www.glossy.co/beauty/how-static-nails-hopes-to-carve-out-a-niche-in-the-9-billion-nail-market) · [Grips: staticnails.com](https://gripsintelligence.com/insights/retailers/staticnails.com) · [Modern Retail: Crown Affair](https://www.modernretail.co/operations/how-crown-affairs-ceo-took-the-brand-into-sephora-and-beyond-to-capture-more-of-hair-cares-market/) · [Modern Retail: Nailboo](https://www.modernretail.co/operations/nailboo-is-tripling-its-presence-in-walmart-amid-an-at-home-nail-care-boom/) · [Dallas Innovates: Divi](https://dallasinnovates.com/dallas-based-scalp-hair-health-brand-divi-snags-minority-investment-from-california-vc-firm/) · [Growjo: RevAir](https://growjo.com/company/RevAir) · [ZoomInfo: TYME](https://www.zoominfo.com/c/tyme/351827449) · [Prospeo: Mooncat](https://prospeo.io/c/mooncat) · [Cosmetics Business: press-ons](https://cosmeticsbusiness.com/press-on-nails-are-having-a-sustainable-makeover) · [Fortune Business Insights: press-ons](https://www.fortunebusinessinsights.com/de/press-on-nails-market-117086) · [Beauty Independent: XMondo AI models](https://www.beautyindependent.com/?p=112418).

**Law and policy:** [NAD Dyson v. Dreame (Mondaq)](https://www.mondaq.com/nad-says-a-disclosure-cant-fix-a-misleading-product-demonstration/1837024) · [Cosmetics Business: Shark "fastest blowout"](https://www.cosmeticsbusiness.com/sharkninja-modifies-marketing-claims-voluntarily-following-nad-challenge) · [BBB: SharkNinja Glossi](https://bbbprograms.org/media/newsroom/decisions/sharkninja-glossi) · [Personal Care Insights: Shark HyperAir NAD 2022 + UK OPSS](https://www.personalcareinsights.com/news/nad-calls-out-sharkninjas-inaccurate-hair-drying-advertising-claims-amid-heated-hair-device-concerns-in-uk.html) · [NAD Hairfinity](https://bbbprograms.org/media-center/dd/nad-recommends-brock-beauty-discontinue-certain-claims-for-hairfinity-dietary-supplement) · [NAD CVS Nourishing Hair](https://bbbprograms.org/media-center/dd/nad-recommends-lang-pharma-discontinue-certain-claims-for-cvs-nourishing-hair-dietary-supplements-following-lifes2good-challenge-finds-product-name-is-not-misleading) · [FDA cosmetics law](https://www.fda.gov/cosmetics/laws-regulations/cosmetics-us-law) · [SEJ: FDA formaldehyde delay](https://www.sej.org/node/51902) · [Smarter Sorting: TPO](https://www.smartersorting.com/post/why-the-eu-banned-tpo-in-gel-nail-polish----and-why-the-u-s-hasnt-yet) · [Khaleej Times: EU TPO ban](https://www.khaleejtimes.com/world/eu-gel-nail-polish-tpo-ban) · [Meta Health & Wellness](https://transparency.meta.com/policies/ad-standards/restricted-goods-services/health-wellness) · [AuditSocials: hair-loss ads 2026](https://www.auditsocials.com/blog/hair-loss-ads-2026-platform-line-meta-tiktok-google-pinterest-finasteride-minoxidil-prescription-policy) (vendor) · TikTok Healthcare & Pharma, FTC rules and NY synthetic-performer law: 45 §5 and 47 §4.

**AI craft:** [Higgsfield: hands and faces](https://higgsfield.ai/blog/ai-video-hands-faces) · doc 43 (all model behaviour, prices and templates) · doc 11 §4 (haircare style header) · doc 47 §3 (shade ΔE, viscosity, mist).
