# 49 — Niche deep-dive: food, snacks, coffee, sauces and functional beverages (non-alcoholic)

Research brief, 2026-10-09. No generation money was spent. Nobody was contacted.

**What this adds.** Doc `11-niche-food-drink.md` already covers the visual grammar of beverages, coffee and tea, snacks and NA spirits: shot types, light, style headers, the liquid-physics workarounds, the ban list, the Poppi and Celsius claim cases and the FTC mock-up rule. This doc does not repeat that. It adds:
- teardowns of 14 real food and drink TikToks we downloaded and measured, plus metadata for 6 more;
- conversion data for the niche (Benly Q1 2026 food sub-industries, TikTok's F&B study, TikTok Shop growth);
- a realism-pitfall table mapped to doc 43's model rules, with the food-only traps (garnish drift, portion inflation, steam that ignores the camera);
- policy and legal rules beyond doc 11 (FDA claim thresholds, slack fill, allergens, CBD/THC, weight claims, energy drinks 18+, AI testimonials);
- a buyer profile and 20 brand types;
- 8 ready concepts with shot lists, physics checks, audio maps and costs.

**Tags.**
- `[measured]`: we downloaded the file and measured it with ffmpeg (scene cuts at threshold 0.30, audio RMS in 0.5 s windows, 2 fps frame tiles that we looked at).
- `[unverified]`: we found no primary source.
- `[inf]`: our own inference.
- `[vendor]`: the number comes from a company that sells the thing being measured.

**Method and limits.**
- **TikTok:** downloads worked. We pulled 16 public TikToks to `scratchpad/niche/food/`, outside the repo. No media is committed. TikTok profile pages could not be listed (yt-dlp JSON error), so every URL came from a web search.
- **View counts:** yt-dlp metadata snapshot of 2026-10-09. **Like rate** = likes ÷ views.
- **Paid vs organic:** TikTok does not label boosted posts. A very high view count with a like rate under ~1% usually means paid distribution (Spark Ads or boosting), because paid impressions reach people who don't engage `[inf]`. We use that as a flag, not a fact.
- **Motion Creative Analytics MCP:** skipped (returned no workspace before, doc 45 §0). Motion's public vertical page publishes no Food & Nutrition leaderboard.
- **Purchase data:** none of the measured posts publishes CPA. Purchase-side evidence comes from founder statements (doc 45 D38), Benly's longevity index and TikTok's own studies.

---

## 0. The 8 findings that matter most

1. **In this niche the paid winners are short, one-idea, prop-driven films, not beauty shots.** The four posts with the biggest reach and a sub-1% like rate (the paid-distribution signature):
   - Celsius × Ferrari, a 12 s whip-cut garage montage: **130M views**;
   - Poppi's "1 soda a day for 1 week" sugar-bag demo, an 18 s one-take talking head: **7.1M**;
   - Liquid Death "Size matters" 12 oz, a deadpan fake-testimonial: **5.2M**;
   - Liquid Death's Super Bowl spot: **4.7M**.

   Each has one idea you can say in five words `[measured]`.
2. **The same script can earn 32× different reach.** Poppi ran the sugar-bag script twice. The warehouse take got 7.1M views. The can-wall take got 224K `[measured]`. What differs is the first second: the winner opens mid-gesture with the bag already up, the loser opens on a face. **Iterate the hook frame, not the script.**
3. **Comedy built on a real category truth wins organic engagement.** The like-rate leaders:
   - Liquid Death "Kegs for Pregs" with Kylie Kelce: 3.3M views at **7.3%**;
   - Graza's "Devil Wears Prada" office skit: 4.6M at **3.6%**;
   - a Cometeer creator who wipes all his coffee gear off the counter: **5.1%**.

   In each one, **the product causes the punchline** (it's water; it's a squeeze bottle; you need no gear). Polished product-only films from the same niche (Fly By Jing jar macro, Magic Spoon, Momofuku) sat at 1.5K–23K views `[measured]`.
4. **On Meta, studio and lifestyle footage scores lowest in snacks.** Benly Q1 2026 effectiveness index:
   - **Snacks & Confectionery:** Graphic Design 50, UGC 44, Branded/Studio 37, **Lifestyle/Editorial 28**;
   - **Organic & Health Foods:** UGC 69, Product Shot 53, Lifestyle 52, Branded/Studio 46;
   - **F&B overall:** UGC 68, Studio 64.

   A pure cinematic film is the weakest thing VXO can sell here. The film has to arrive **wrapped in a native frame** (text-led, POV, skit) or **cut into graphic-design variants** `[vendor]`.
5. **Snack creatives live long, coffee creatives don't.** Median lifespan:
   - snacks: 28 d median, 71 d average, the longest of any food sub-industry;
   - coffee & tea: 38 d average;
   - F&B overall: 26 d median.

   For VXO a snack film can be a Premiere ($2,500) one-off. Coffee and functional drinks need the Season plan ($3,500/mo), because they refresh about monthly `[vendor]`.
6. **"Visual intrigue" is the top hook in every food sub-industry, and product sound is the second lever.**
   - Visual intrigue opens 29–37% of food video creatives, and in snacks those ads average a 45 d lifespan.
   - TikTok's F&B study: **70% of users like product-centred content**, and **64% love product sounds** (fizz, pour, chop).
   - Their other must-haves: discovery (72%), a light, feel-good mood (72%) and regular people (75%).

   That is VXO's brief in one line: **a strange product image in second 1, a real product sound by second 2, an ordinary person in the frame** `[vendor]`.
7. **AI food fails on liquids, steam and portion truth, not on motion.** The food-specific failures:
   - pours create liquid from nothing (doc 11);
   - steam renders as dry-ice fog and **doesn't rotate with an orbiting camera**;
   - **garnish drifts in** (sesame, nuts, herbs). That is an **allergen claim** the brand never made;
   - **portions inflate** as the camera moves.

   The fix is doc 43's split: Kling 3.0 Pro i2v from the **client's own product photo** for every food or label frame, Seedance 2.5 r2v only for people and world, and a **phone-shot real insert** for any pour, bite or cheese pull.
8. **The claims landmine is "functional".** Live risks:
   - Poppi paid $8.9M over prebiotic-fibre dose (2025), and Olipop was sued on the same theory in Jan 2026;
   - Bloom Nu's energy drinks are in court over "no artificial" (citric acid);
   - TikTok restricts energy drinks to **18+** in North America and bans fat-burn ingestibles in branded content;
   - Meta bans THC ads and requires LegitScript for CBD.

   Rule: **on screen, facts with units ("9 g fibre", "120 mg caffeine"), never effects ("gut health", "focus", "burns")**.

---

## 1. Teardowns: 14 measured ads (2024–2026) plus 2 controls

`[measured]` = downloaded. Cut rate = (cuts + 1) ÷ duration. Hook = what is on screen and in the audio during second 1.

### 1.1 Measured (TikTok)

| # | Ad | Date · views · like rate | Length · cuts · shots/s | Second 1 (hook) | Turn / punchline | Sound | CTA | Why it sold |
|---|---|---|---|---|---|---|---|---|
| F1 | **Celsius × Ferrari "Fueling your high energy moments"** ([link](https://www.tiktok.com/@celsiusofficial/video/7389005924410592543)) | 2024-07-07 · **130M** · 0.46% | 12.4 s · ~30 detected (whip-blur transitions inflate the count) · ~2.5 | Whip-pan blur through the garage, then Leclerc smiling. Motion already under way at frame 1 | None. Silverstone title card, helmet on, car rolls out of the box, can logo on the nose | Music bed flat at −15 dB RMS, no VO | None on screen | Paid reach (0.46%) on borrowed fame. A 12 s energy montage is the format energy drinks scale. The can appears only on the car. **Not reproducible for a DTC client** (licence), but the grammar is: 12 s, whip-cuts, fisheye, one hero object |
| F2 | **Poppi "love soda but hate the sugar?"** ([link](https://www.tiktok.com/@drinkpoppi/video/7597459929271635231)) | 2026-01-20 · **7.1M** · 0.56% | 18.4 s · **0 cuts** · one take | A woman in a warehouse already holding up a zip bag of white sugar labelled "1 SODA/DAY FOR 1 WEEK" | She tosses the sugar bag away and swaps in the can | Voice only, RMS −38 to −45 dB (phone-quiet) | Can in hand | **A physical prop makes the claim visible** (sugar you can see). One take = credible. The claim is a fact (grams of sugar), not a health benefit |
| F3 | **Poppi "your new soda obsession" (same script, control)** ([link](https://www.tiktok.com/@drinkpoppi/video/7630876333496667423)) | 2026-04-20 · 224K · 0.29% | 26.7 s · 0 cuts | A face talking in front of a wall of cans; the bag enters at ~1.5 s | Same | Voice, −34 to −40 dB | Can | Control: **same prop, same script, 8 s longer, prop late → 1/32 the reach** |
| F4 | **Liquid Death "Size matters" (12 oz cans)** ([link](https://www.tiktok.com/@liquiddeath/video/7546266393075928350)) | 2025-09-04 · **5.2M** · 0.84% | 47 s · 7 cuts · 0.17 | A woman on a bed, straight to camera, super "SIZE MATTERS" | Four deadpan "testimonials" (businesswoman, gardening grandma, a 90s kid) play the double entendre straight until the can reveal | Clean dialogue, RMS jumps between −12 and −35 dB at line ends | Smaller cans exist | **Fake-testimonial parody**: the category's own ad cliché, played straight. Product change = the joke. No AI faces (real cast) |
| F5 | **Liquid Death Super Bowl 2025** (repost of the TV spot filmed off a TV) ([link](https://www.tiktok.com/@liquiddeath/video/7469585474768719135)) | 2025-02-10 · 4.7M · 0.61% | 30.7 s · 0 cuts detected (the inner spot has ~10 shots) | A frosted can bursting from ice on the TV, legs-on-sofa POV | People in no-drinking jobs (pilot in the cockpit, surgeon mid-operation, referee on the field, cops in a cruiser) shotgun cans | TV audio −23 to −25 dB | Brand | The **"wrong place to drink" reversal** works because it's water. The POV-of-a-TV frame makes a TV spot feel native |
| F6 | **Liquid Death × Kylie Kelce "Kegs for Pregs"** ([link](https://www.tiktok.com/@liquiddeath/video/7483184893241888046)) | 2025-03-18 · 3.3M · **7.3%** | 60 s · 27 cuts · 0.47 | A heavily pregnant woman shotgunning a can at a bar, head back, frame 1 | A horrified bar patron: "Are you drinking?" — "I've had so many of these today." A song: mini kegs of mountain water "for two" | Captioned dialogue, then a sung chorus at −21 to −25 dB | Limited edition | **Shock image → harmless truth** in 3 s. The product (water) defuses the shock. A real limited SKU (the keg) gives a reason to buy now |
| F7 | **Graza "The Devil may have worn Prada, but Allen squeezes Graza"** ([link](https://www.tiktok.com/@getgraza/video/7634672887470886157)) | 2026-04-30 · 4.6M · **3.6%** | 77.7 s · 23 cuts · 0.31 | Office kitchen, lime-green fridge, staff mid-scene holding bottles | A *Devil Wears Prada* "cerulean" monologue parody about olive oil, played by staff | Room sound, dialogue −22 to −35 dB | None | **Staff skit + film parody + product colour as a character** (the lime fridge matches the bottle). Organic: high like rate, long |
| F8 | **Mid-Day Squares "rare misprint"** ([link](https://www.tiktok.com/@middaysquares/video/7155994836145933574)) | 2022-10-18 (older reference) · **10.8M** · **12%** | 79.7 s · ~45 real cuts (+ a 4 s glitch burst) · 0.6 | Founder at a desk, kinetic captions: "this PROBLEM could RUIN our company" | Factory problem (a wrapper machine fails) → workaround → a packaging misprint becomes a collectable | VO + music at −11 to −17 dB | Find it on shelves | **Founder documentary with stakes**. Motion: founder 8.57% (doc 45 D3). The template that built the brand |
| F9 | **Chomps "We're not like the other guys"** (creator) ([link](https://www.tiktok.com/@gochomps/video/7247912383220436270)) | 2023-06-23 · 792K · 2.0% | 21.4 s · 5 cuts · 0.28 | Green-screen creator over a gas-station jerky display, hand gesture | She walks through the competitor shelf, then holds up the green Chomps pack: ingredient comparison | Voice −17 to −26 dB | Pack in hand | **Us-vs-them on a retail shelf** (D4 6.52%). Comparative-claim risk (§4) |
| F10 | **Fishwife "making the world's tastiest tinned fish"** ([link](https://www.tiktok.com/@eatfishwife/video/7631686145532874015)) | 2026-04-22 · 295K · 1.5% | 65.9 s · 32 cuts · 0.5 | "MEET Becca", a hair-netted worker kissing a fish | Supermarket aisle "for years TINNED FISH… BLAND, DRY" → origin story → served beautifully | Music −13 to −16 dB, very loud and flat | Product | **Category villain (bland canned tuna) → hero**. Big bold-sans + serif-italic captions (Benly's "Graphic Design" style inside video) |
| F11 | **Cometeer × @tannercolson "Making coffee with no gear?"** ([link](https://www.tiktok.com/@tannercolson/video/7532511929458265374)) | 2025-07-29 · 149K · **5.1%** | 75.9 s · 23 cuts · 0.32 | A creator beside an espresso machine, grinder, roaster | He removes each machine, **wipes the empty counter**, then tongs a frozen coffee puck | Voice −21 to −26 dB | #CometeerPartner, discount code | **Removal gag = the benefit** (no gear). The real pours (latte art, espresso into milk) are filmed, not generated |
| F12 | **Olipop "dirtiest soda" (ranch)** ([link](https://www.tiktok.com/@drinkolipop/video/7486902665319075118)) | 2025-03-28 · 16.5K · 2.4%, **90 comments** (0.55% comment rate) | 18.6 s · 10 cuts · 0.59 | Finished glass: cola topped with a ranch cloud, can beside it | Can crack, pour over ice, squeeze bottle of Hidden Valley ranch, stir: a curdled cloud | Music bed, −24 to −30 dB | None | **Absurd brand collab drives comments** (outrage = reach). Every liquid event is real and continuous; an AI model could not hold this level rise (doc 11) |
| F13 | **@crisanvisual "Seedance 2.0 × Higgsfield" (AI Oreo spec)** ([link](https://www.tiktok.com/@crisanvisual/video/7626530087046892801)) | 2026-04-08 · 7.9K · 2.6% | 22.6 s · 5 cuts | A creator's shocked face: "WTF what did I just make?" | Screen recording: an AI Oreo ad (kitchen, child, hand pulling a cookie from the sleeve, cookie twisted) | Voice, then ad audio | "Prompt in comments" | **AI food spec work earns reach as a tool demo, not as an ad.** Note the AI frames hold the pack and cookie (reference-locked) but sit in a generic stock-ad kitchen |
| F14 | **Fly By Jing "Xtra Crunchy" launch** ([link](https://www.tiktok.com/@flybyjing/video/7504351510571011359)) | 2025-05-14 · 1.6K · 1.3% | 41 s · 34 cuts · 0.85 | Stacked jars on a table, one-word supers "MEET EXTRA CRUNCHY" | Spoon macro of the crisp, ingredient words one at a time, jar row | Music + a mouth-crunch, −20 to −30 dB | Shop | **Control: a polished texture montage with no idea.** The niche's most common brand post, and its weakest |

**Two more controls:**
- Magic Spoon "2 bowls? Ain't no thang" ([link](https://www.tiktok.com/@magicspooncereal/video/7514391366185798958)): 2025-06-10, 9.8K views, 1.2%. 13.4 s, 1 cut. A selfie with an empty bowl, a lip-synced line, a bowl smash to the lens. **A meme without a product truth goes nowhere.**
- Celsius "Suspect knows a little too much" ([link](https://www.tiktok.com/@celsiusofficial/video/7431266578152607022)): 2024-10-29, 191K, 1.35%. 23.6 s, 4 cuts. Employee "suspect" meme with captions. **Employee memes hold steady around 1%, never break out.**

### 1.2 Metadata only (not downloaded)

| Ad | Date · views · likes | Note |
|---|---|---|
| Mid-Day Squares "Building a chocolate factory is the hardest thing I've ever done" ([link](https://www.tiktok.com/@middaysquares/video/7219073373291252998)) | 2023-04-06 · 2.5M · 430K (17%) | 201 s founder doc. The sequel format of F8 |
| Liquid Death "it's good for you!" with @shane ([link](https://www.tiktok.com/@liquiddeath/video/7405313762233814303)) | 2024-08-20 · 38.5K · 2.3% | Same brand as F4–F6 with a celebrity but no twist: 1/100 the reach |
| Graza squeeze-bottle launch teaser ([link](https://www.tiktok.com/@getgraza/video/7365864860279672106)) | 2024-05-06 · 2.4K | Same brand as F7: a teaser with no story |
| Cometeer brand explainer ([link](https://www.tiktok.com/@cometeer/video/7375147856027471150)) | 2024-05-31 · 2.2K · 2.2% | Brand-made explainer vs the creator's gag (F11): 1/67 the reach |
| Olipop billboard (creator commentary) ([link](https://www.tiktok.com/@katarinaterentieva/video/7383834097027648811)) | 2024-06-23 · 97K · 5.6% | OOH stunt that earned a second life as creator commentary |
| @nicolestorydent × Olipop "90s soda commercial" ([link](https://www.tiktok.com/@nicolestorydent/video/7466119597276564766)) | 2025-01-31 · 305K · 0.8% | Paid creator pastiche of a 90s soda ad (#olipoppartner) |

### 1.3 What the measured set says `[measured]`

- **Cut rate follows the format, as in doc 48.**
  - Prop demo / talking head: 0 cuts (F2, F3).
  - Deadpan parody: 0.17 shots/s (F4).
  - Skits and founder stories: 0.3–0.6 shots/s (F6–F11).
  - Energy montage: 2.5 shots/s (F1).
  - The fastest *organic* post (F14, 0.85) is the weakest. Speed is not the lever.
- **Second 1 always holds a strange image already in motion.** Pregnant woman chugging (F6), sugar bag already raised (F2), whip-blur (F1), woman kissing a fish (F10). This matches Benly's "Visual Intrigue" hook as the top food hook. The losers open on a face, a static jar row, or an empty bowl.
- **Two of the three highest like rates use shock → harmless truth.** "Are you drinking?" → it's water (F6). "This could ruin our company" → it becomes a collectable (F8). The product resolves the tension.
- **Audio.** Winners are voice-led (F2–F4, F6–F11), or a single bed with no VO (F1). The ASMR-only film (F14) and the music-only meme (Magic Spoon) are the weakest. In food, the **product sound is a beat inside a story**, not the whole film `[inf]`.
- **Real liquids, always.** Every pour in the set (Olipop, Cometeer, Liquid Death) is real and continuous. None of the winners asks a model to raise a liquid level. VXO should plan for a **real insert** whenever a level must change (§3).
- **AI-made food content earns attention as a "how I made this" demo, not as an ad** (F13: 7.9K, and doc 11's Coca-Cola backlash). An AI film has to *pass* as a normal ad in its paid version. Its BTS can be the organic post `[inf]`.

---

## 2. What actually converts in this niche (data)

| # | Finding | Number | Source | Status |
|---|---|---|---|---|
| N1 | F&B on Meta: effectiveness by asset type | UGC/Organic **68**, Branded/Studio **64**, Lifestyle/Editorial 62, Graphic Design 55, Motion/Animation **45**; 17K creatives, 114 brands | [Benly F&B Q1 2026](https://benly.ai/benchmarks/q1-2026/food-beverage) | `[vendor]` index from ad longevity |
| N2 | F&B lifespan | Median **26 d**, avg 36 d; 44% survive 30 d, 21.7% survive 60 d; **54% of creatives are video** | same | `[vendor]` |
| N3 | F&B video hooks | Visual Intrigue **29%** (36 d avg life), Bold Statement 26.3% (39 d), Pattern Interrupt 20.4% (38 d), Pain Point 11.2% (34 d) | same | `[vendor]` |
| N4 | **Snacks & Confectionery** by asset type | Graphic Design **50**, UGC 44, Branded/Studio 37, Motion 36, **Lifestyle/Editorial 28** | [Benly snacks](https://benly.ai/benchmarks/q1-2026/food-beverage/snacks-confectionery) | `[vendor]` |
| N5 | Snacks lifespan and hooks | Median 28 d (+32% vs cross-industry), avg 41 d; 45.9% survive 30 d. Visual Intrigue 36.9% (45 d), Pattern Interrupt 24.1% (**51 d**), Bold Statement 18.1% (**52 d**), UGC-style opening 14.5% (30 d) | same | `[vendor]` |
| N6 | **Organic & Health Foods** by asset type | UGC **69**, Product Shot 53, Lifestyle 52, Branded/Studio 46, Graphic Design 41; video 57.3%; median 23 d | [Benly organic & health](https://benly.ai/benchmarks/q1-2026/food-beverage/organic-health-foods) | `[vendor]` |
| N7 | Sub-industry average lifespans | Snacks **71 d**, Restaurants 56 d, Fast food 47 d, Meal kits 46 d, Coffee & Tea **38 d**, Organic 37 d; top asset is UGC/Organic in every one | [Benly F&B](https://benly.ai/benchmarks/q1-2026/food-beverage) | `[vendor]` |
| N8 | TikTok F&B users: product central / product sounds | **70%** love product-centred content; **64%** love product sounds | TikTok Marketing Science, *Elevating your TikTok ads: F&B 2024* (200 videos, 7,500 users, 5 markets) via [TikTok blog](https://ads.tiktok.com/business/en/blog/elevate-your-food-and-drink-ads) | Primary (platform study, EU markets) |
| N9 | Same study: people, mood, discovery, home | 75% like regular people; 72% want a feel-good, light mood; 72% like discovery; 66% want playful; 53% say home settings make the brand "for someone like them" | same | Primary |
| N10 | TikTok Shop food | Food & beverage sales **more than doubled** since early 2024; trend content leads shop sales by "a couple of weeks"; transformations, ASMR and "popping/opening" moments do well; EZ Bombs hit $19M TikTok Shop sales in a year | [Modern Retail, Oct 2025](https://www.modernretail.co/technology/tiktok-is-talking-to-brands-like-its-a-grocer-now/) | Press |
| N11 | TikTok Shop best-sellers are functional drinks | Mar 2025: 2 of the top 3 US products were drink mixes (Brainista yerba mate instant tea $3.75M; Drink Nello calming mix $2.55M); 2025 risers: protein coffee, loaded tea | [Kalodata via chinesellers](https://chinesellers.substack.com/p/tiktok-marketplace-monitormarch-2025), [FastMoss recap](https://www.fastmoss.com/blog/u-s-tiktok-shop-2025-sales-recap-top-products-creator-trends-fastest-growing-categories/) | `[vendor]` estimates |
| N12 | Meta formats (all verticals) relevant to food | Unboxing 9.83%, ASMR 8.58%, founder 8.57%, demo 8.11%, **cinematic b-roll 6.85%**; hooks: newness 11.37%, sale 11.35%, price anchor 10.89% | Motion 2026, doc 45 D3–D5 | Read |
| N13 | Poppi: founder video still #1 converting ad after ~2 years; 80–90% of commenters bought in store | — | doc 45 D38 | Founder claim |
| N14 | Food & bev Meta ROAS 1.56 (one of the lowest verticals) | — | doc 45 D22 | `[unverified]` |
| N15 | A 15 s food ad typically uses **3–5 shots**: a hook, 1–2 appetite shots, a product payoff; splash/pour works "as a hook or a transition" | — | [Higgsfield food ad guide 2026](https://higgsfield.ai/blog/food-product-video-ad-ai-2026) | `[vendor]` |

### 2.1 What this means, by sub-niche `[inf]`

| Sub-niche | Lead format | Second | Length | Must-have layer |
|---|---|---|---|---|
| **Functional drinks / soda / energy** | Prop demo or parody, one idea, 12–18 s | Founder or creator story | 12–18 s paid; 45–60 s organic skit | A fact with a unit (g sugar, mg caffeine) as a prop or super; "new flavor" or limited-edition hook (N12) |
| **Coffee & tea** | Ritual demo with a twist (removal gag, cost per cup) | Creator recipe | 15–20 s | Cost-per-cup price anchor (N12: 10.89%); refresh monthly (N7: 38 d) |
| **Snacks & candy** | Graphic-design-led video (big type, product, crunch), skit, us-vs-them | UGC taste test | 10–15 s | Crunch or "opening" moment (N10); long-life asset, so one strong film per quarter (N5, N7) |
| **Sauces & condiments** | "Put it on everything" demo with a story (F7, F12) | Absurd collab / recipe | 15–30 s | The squeeze, the drip, the jar opening as the sound beat; the real food from the client's kitchen |
| **Health / organic foods** | UGC-style or founder (N6: 69) | Product shot (53) | 15–30 s | Ingredient proof; no health claims (§4) |

**VXO positioning in this niche** `[inf]`: sell **"a cinematic film that runs as native"**. Each deliverable is:
- a 15 s paid hero with a strange first frame and a product-caused punchline;
- a 6 s "visual intrigue" cutdown;
- 4–6 graphic-design variants (big type over film frames), because snacks rank graphic design first (N4);
- a "how we made it" BTS that the brand can post organically (F13 logic).

---

## 3. AI realism pitfalls for this niche, and the fixes

Builds on doc 11 (liquid physics, ban list) and doc 43 (§1 model table, §5 failure table). New items are marked **NEW**.

| Pitfall | What goes wrong | Fix (prompt / reference / model) |
|---|---|---|
| **Liquid level change** (pour, fill, chug) | Liquid appears from nothing; the level doesn't drop when drinking (doc 11, doc 41) | (1) **Real insert:** the client phones a 3 s pour against a plain wall; VXO grades and matches it. (2) Kling 3.0 Pro i2v with `image_url` = before state and `last_image_url` = after state, cut before the settle. (3) Hide the transfer: stream macro with no source or target level in frame, ≤2 s |
| **Drinking on camera** | Lips don't seal on the can; the throat doesn't move; the can stays full | Avoid frontal sips. Shoot the **can lowered after the sip** (the result), or profile-on with the can covering the mouth. The Liquid Death shotgun (F6) is real footage; don't generate it |
| **NEW: Steam ignores the camera** | In an orbit, the plume stays facing the lens instead of rotating in 3D; steam renders as dense dry-ice fog | No orbit around steam. Locked-off or straight dolly-in only. Prompt: "thin, broken wisps of steam that rise, curl and disappear within 10 cm; backlit; NOT fog, NOT dry ice, NOT a continuous column" ([Metabunk thread](https://www.metabunk.org/goto/post?id=354878); [Atlas](https://www.atlascloud.ai/hi/blog/tips/minimax-h3-food-video-prompt-guide)) |
| **NEW: Garnish drift = allergen claim** | The model adds sesame, nuts or herbs that aren't in the product, implying an ingredient (and an allergen) the brand never declared | Product ref = the client's real photo. Prompt: "food, portion and garnish exactly as in @image1; **no new ingredients**, no seeds, no nuts, no herbs that are not in the reference" ([Flowjam](https://www.flowjam.com/blog/ai-video-for-restaurants-2026)). QC every frame against the ingredient list (§7) |
| **NEW: Portion inflation** | Burgers grow taller and bowls fuller as the camera moves | Kling i2v with `last_image_url` = the same still, so the end frame is locked. Prompt "portion size never changes". Move ≤20°. Same as the FTC mock-up rule in doc 11 |
| **Crumbs / chips / beans multiply** | Counts drift, crumbs regrow | Write exact counts ("exactly 12 chips", "30 crumbs"). Object fate: "crumbs only fall and settle, never reappear" (doc 43 rule 12). Keep falling-piece shots ≤2 s |
| **Bites, chewing, mouths** | Uncanny jaw, food clips through teeth | Never generate a bite. Show **before** (food lifted toward the frame edge) and **after** (half-eaten piece on the plate, real or i2v from a real photo). A real-insert bite from the client if needed |
| **Cheese pull / sauce drip / honey drizzle** | Rubbery stretch, loops, viscosity wrong | ≤1.5 s, start/end frames (doc 11). Prompt viscosity as a speed: "honey falls in one thin ribbon that folds on itself, about 2 cm per second". Prefer a real insert |
| **Carbonation and condensation** | Uniform beads; bubbles too regular | "Uneven beads, two running trails, a dry patch"; "distinguishable spherical bubbles in vertical chains" (doc 11). These are the safest liquid events: use them as the hook instead of a pour |
| **Ice** | Perfect glass cubes | "Fractured clear ice with trapped air, one chipped corner" (doc 11) |
| **Labels, nutrition panels, can text** | Text softens or turns to gibberish, above all in Seedance (doc 43 [B-ADH]) | Label frames only via Kling 3.0 Pro i2v from the real pack photo ("keeps signs, captions and logos", doc 43 §1). In Seedance: "all text unreadable except the label in @image1". **Any number shown (grams, mg) is a post super, never generated.** Nutrition panels never on screen from AI |
| **NEW: Can tab and bottle cap geometry** | The tab bends wrong; the cap re-seals; the can pops twice | One crack per can. Write the fate: "the tab lifts once and stays up; vapour puff for 0.3 s". Shoot the crack in profile at the frame edge, cut to the puff (doc 11). Use the real crack **sound** from a library |
| **Bag crinkle melts the print** | Foil bag text warps when it moves | Keep the bag still in the frame; put the crinkle in the SFX (doc 11). Hero bag shots = Kling i2v from a pack photo, ≤10° move |
| **Hands and utensils** | Extra fingers, bending forks, wrong tine count, chopsticks through food | One hand, part out of frame; name contact points (doc 43 §5). "A four-tine fork, rigid steel, never bends." Utensil in a locked-off frame |
| **Reflections on cans, glass, spoons** | A crew or camera is missing from a mirror surface; impossible highlights | Matte or brushed surfaces when possible. Prompt the reflection source: "a soft window highlight in the shape of a rectangle on the can shoulder; no camera or crew visible in reflections". Doc 43: Seedance 2.5 is strongest on reflections |
| **"Too perfect" food** | Even grill marks, impossible gloss → "AI slop" read | Add imperfections from doc 06: one crumb on the plate, a smear on the rim, a fingerprint on the can. Name the exact gloss: "matte crust, oil only at the edges" ([Higgsfield food guide](https://higgsfield.ai/blog/food-product-video-ad-ai-2026)) |
| **Coffee crema / latte art** | Latte art spawns milk; crema rises from nothing | Finished rosetta only; the spoon breaks it (doc 11). The Cometeer creator (F11) films real pours |
| **Kitchen appliances** (espresso machine, grinder, fridge) | Knobs and dials morph in moves | Locked-off frames; machines as background; doc 43 rule 5 (clean the plate of look-alike objects) |
| **People eating at a table** | Faces drift; too many people → glitches | ≤3 people (doc 43); real talent refs or averted faces (doc 48 finding 3). Group shots as cutaways ≤1.5 s |

**Model routing for food** (from doc 43 §1, applied):

| Shot | Model | Settings | Cost per take |
|---|---|---|---|
| Label / pack / jar / can hero insert | Kling 3.0 Pro i2v | 5 s, `sound:"off"`, `cfg_scale` 0.5, `last_image_url` = same still for lock | $0.48 |
| Food state change (raw → cooked, full → empty, closed → open) | Kling 3.0 Pro i2v, start + end frames | 5 s, describe only the path | $0.48 |
| Product sensory one-take (condensation, steam, dolly-in) | Cinema Studio 4.0 | `pacing:"single-shot"`, `camera_movement:"dolly-in"`, 720p, 8 s | $3.70 |
| People, skit, world, multi-shot | Seedance 2.5 r2v | 9:16, 10–15 s, product = first ref, "exactly N shots" | $4.62 / 10 s at 720p |
| Blocking previs | Wan 3.0 r2v 480p | seed fixed | $0.50 / 10 s |
| Pour, bite, cheese pull, drizzle | **Real insert** (client phone, 4K, 60 fps) | VXO grades and matches | $0 generation |

---

## 4. Ad policy and legal constraints

Beyond doc 11 (Poppi, Celsius, "healthy" rule, energy drinks and minors, FTC mock-ups, NA alcohol) and doc 45 §5 (AI labels):

### 4.1 US law (FDA / FTC / courts)

| Rule | What it means on screen | Source |
|---|---|---|
| **Nutrient content claims** (21 CFR 101.13, 101.54) | "Good source of protein" needs 10–19% DV per serving; "high protein" / "excellent source" needs ≥20% DV. The %DV for protein needs a PDCAAS-corrected value. "Low sugar" is **not** an FDA-defined claim; "sugar-free" (<0.5 g) and "reduced sugar" (−25%) are | [eCFR 101.54](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-101/subpart-D/section-101.54) |
| **"Healthy"** (21 CFR 101.65, final rule) | Effective Feb 2025, compliance Feb 2028; caps added sugar, sodium and saturated fat. Don't super "healthy" unless the product qualifies | doc 11 |
| **Health and structure/function claims** | "Supports digestion", "boosts focus", "immune support": in a food, a structure/function claim must come from the food's nutritive value; on a supplement it needs the FDA disclaimer (21 CFR 101.93). Disease words (cure, treat, prevent) are off-limits | [FDA guidance](https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/structurefunction-claims) |
| **Dose-substantiation suits** | Poppi: $8.9M (May 2025) because the prebiotic dose was too low for "gut health" ([BevNET](https://www.bevnet.com/news/2025/poppi-close-to-8-9m-settlement-over-gut-health-claims)). Olipop: sued on the same theory, Jan 2026 ([Top Class Actions](https://topclassactions.com/lawsuit-settlements/lawsuit-news/olipop-lawsuit-claims-prebiotic-soda-is-sugared-water-with-no-real-digestive-benefits/)) `[unverified: outcome]` | Super the amount ("9 g fibre"), never the effect |
| **"No artificial…" / "natural"** | Bloom Nu energy drinks sued over "no artificial flavors" because of citric acid ([Top Class Actions, Aug 2026](https://topclassactions.com/lawsuit-settlements/lawsuit-news/class-action-claims-bloom-sparkling-energy-drinks-contain-artificial-flavor/); [Benesch](https://www.beneschlaw.com/insight/going-back-to-the-well-plaintiffs-target-wellness-branding-by-attacking-ingredients/pdf/)). "Natural" has no FDA definition | Use the ingredient list, not adjectives |
| **Slack fill** (21 CFR 100.100) | Non-functional empty space in a pack is misbranding. A film showing a bag "full to the top" when it isn't is a claim. Conversely, mocking a rival's slack fill is a comparative claim that must be true | Concept C3 is built on it; the fill shot must be a real insert |
| **Allergens** (FALCPA + FASTER Act: 9 majors incl. sesame since 2023) | AI garnish drift (§3) that shows nuts or sesame on a product without them is a false depiction; on a product *with* them, never imply "allergen-free" | [FDA allergens](https://www.fda.gov/food/food-labeling-nutrition/food-allergies) |
| **Food mock-ups** | FTC: a misleading demonstration is deception (Campbell's marbles). AI food that looks bigger, glossier or fuller than the product is the same thing | doc 11 |
| **Fake reviews and testimonials** (16 CFR 465, in force Oct 2024) | No AI person giving a testimonial or taste verdict as if a real customer. Parody testimonials (F4) are fine when obviously fictional and making no factual claim `[inf]` | doc 48 §4 |
| **Endorsements** (16 CFR 255) | Creator and staff skits need clear #ad / partner disclosure (F11 used #CometeerPartner) | FTC Endorsement Guides |
| **Comparative ads** | "Not like the other guys" (F9) is legal if the comparison is truthful and substantiated; never show a real competitor pack in an AI frame (trademark) | Lanham Act §43(a) |
| **Caffeine** | No "energy that lasts all day" type promises without substantiation; disclose mg; no "safe for kids"; no mixing with alcohol (doc 11) | — |
| **Prop 65 (California)** | Coffee: OEHHA's 2019 regulation exempts acrylamide in coffee from the warning `[unverified: current status]` | — |

### 4.2 Platform rules

| Platform | Rule | Source |
|---|---|---|
| **TikTok** | Energy drinks allowed in North America but **restricted to 18+**; fat-burning or weight-change ingestibles (detox teas, appetite suppressants) **prohibited** in US/CA branded content | [TikTok branded content market requirements](https://ads.tiktok.com/help/article/branded-content-policy-market-specific-requirements-archive) (archived page) |
| **TikTok** | Any weight-loss or muscle-gain claim must target **18+** and promote a healthy lifestyle; weight-loss policy updated May and July 2026 | [Weight Management policy](https://ads.tiktok.com/help/article/tiktok-ads-policy-weight-management) |
| **TikTok** | Products for minors may be advertised but must not speak to minors or look "overly childish"; kids' snacks also fall under CARU (doc 11) | same; [Teen safety](https://ads.tiktok.com/help/article/tiktok-ads-policy-youth-safety) |
| **Meta** | THC ads banned (ingestible and not); CBD needs LegitScript certification + written permission, US only, 18+, no health claims; ingestible CBD effectively excluded `[unverified: exact wording]` | [Meta CBD policy](https://transparency.meta.com/policies/ad-standards/content-specific-restrictions/cbd) |
| **Meta** | Weight-loss/gain products 18+; before/after imagery for weight loss: non-compliant on the page we could read; trackers report a July 2026 rewrite and disagree on whether before/after is now allowed `[unverified]` | [Personal health and appearance](https://transparency.meta.com/policies/ad-standards/objectionable-content/personal-health-and-appearance); [ConductAtlas change log](https://conductatlas.com/change/2026-07-23-meta-ads-meta-advertising-policies-3936/) |
| **Meta / TikTok** | NA spirits and NA beer: no depiction of alcohol or consumption on Meta; retail media may treat NA as alcohol (doc 11) | doc 11 |
| **All** | AI disclosure: Meta's "AI info" and TikTok's AIGC label for realistic AI (doc 45 §5.3). A food film with realistic AI people should expect a label | doc 45 |
| **Regulators** | 35 state AGs (Dec 2025) asked Meta to crack down on AI-generated before/after wellness ads. **Functional-drink films with AI bodies are a target** | [PA AG](https://www.attorneygeneral.gov/?p=32582) |

**Claim-safe phrasing cheat-sheet** `[inf]`:

| Don't | Do |
|---|---|
| "Gut health in a can" | "9 g prebiotic fibre" |
| "Focus all day" | "120 mg caffeine from green tea" |
| "Healthy chips" | "Cooked in avocado oil" (if true) |
| "Burns fat" | (nothing; don't advertise it) |
| "No artificial anything" | "Ingredients: [list]" |
| "Better than [brand]" | "3× the protein of a typical bag of chips" (substantiated, generic) |
| "Hangover-free" | "0.0% alcohol" |

---

## 5. The buyer

### 5.1 Who signs a $1,200–3,500 film

| Brand stage | Who signs | How they buy |
|---|---|---|
| Pre-retail / DTC-first, <$5M revenue | **The founder** (often also the face of the brand, see F8, F10) | A card payment after seeing frames; buys a Short ($1,200) to test |
| $5–30M, in Whole Foods / Target / Sprouts | **Head of Growth / Performance Marketing**, with the founder on final approval | Buys against a creative-testing budget; needs variants and cutdowns; the Season plan fits |
| $30M+ or PE/strategic-owned (Poppi under PepsiCo) | Brand Director + agency of record + legal review | Out of VXO's lane unless through an agency `[inf]` |

Practical note: most emerging food brands earn the majority of revenue **in retail**, not online. Poppi said 80–90% of TikTok commenters bought in store (doc 45 D38). The film's job is often **retail velocity and TikTok Shop**, not website ROAS. Pitch the outcome as "a film that sells in the aisle and on TikTok Shop", not "a DTC conversion ad" `[inf]`.

### 5.2 What they fear (ranked) `[inf]`, with evidence

1. **"It won't look like our product."** Food is the category where the pack and the food *are* the brand. A wrong chip shape or a new garnish is a deception risk (§4) and a retailer-relationship risk.
2. **AI backlash.** Coca-Cola 2025 was called slop over extra truck wheels; McDonald's NL pulled its AI ad (doc 45 D36); AI disclosure lowers credibility for sceptics (D33).
3. **Claims liability.** Poppi $8.9M, Olipop suit, Bloom suit (§4). A small brand can't absorb a class action.
4. **Paying for a pretty film that doesn't sell.** Cinematic b-roll has the lowest format hit rate (N12: 6.85%); lifestyle scores 28 in snacks (N4).
5. **Creative fatigue.** A 26 d median life (N2) means one film is not enough; they need a system.
6. **Brand voice.** Food brands with big personalities (Liquid Death, Graza) fear a generic "stock-ad kitchen" (F13's look).

### 5.3 What proof they need

- **The 5 free frames made from *their* pack photo**, with the label crisp and the food matching the real product. This answers fear 1 directly.
- **One paid-style 15 s hero + one native cut** (POV, skit or prop demo) in the portfolio, so they can see the film run as native.
- **A claims-checked script**: every on-screen number matches the nutrition panel; the doc 4.2 cheat-sheet applied.
- **A real-insert plan**: "you film one 3 s pour on your phone; we do the rest". Founders like it because it keeps their real product in the film.
- **Hook-rate targets** from doc 45 (Meta 25.44% average 3 s hook rate, D16) and a promise of 3 hook variants per film.
- **Turnaround** in days, not weeks, because trend content leads TikTok Shop sales by about two weeks (N10).

### 5.4 Twenty example brand types (no outreach)

1. Prebiotic or low-sugar soda
2. Protein soda / protein coffee (2025 TikTok Shop riser, N11)
3. Yerba mate or matcha energy drink (18+ targeting on TikTok)
4. Electrolyte stick packs / hydration mixes
5. Sleep or calm drink mixes (watch structure/function claims)
6. Cold brew concentrate / frozen coffee pods
7. Single-origin specialty coffee subscription
8. Mushroom coffee (high claim risk)
9. Chili crisp / chili crunch
10. Hot honey / hot sauce
11. Squeeze-bottle olive oil
12. Premium pasta sauce in a jar
13. Tinned fish
14. Meat sticks / jerky
15. Protein or "seed-oil-free" chips and puffs
16. Better-for-you chocolate bars
17. Swedish candy / freeze-dried candy (TikTok-born)
18. High-protein cereal / granola
19. Seasoning blends (EZ Bombs-type, N10)
20. Kombucha / fermented sodas

---

## 6. Eight ready film concepts (invented brands)

Conventions:
- **Formats:** 9:16 master; 4:5 and 1:1 reframes; a 6 s cutdown; 4–6 graphic-design variants from the film's frames (N4).
- **Physics:** each concept passes doc 41 §2 and doc 44's "could a crew rig this?" read.
- **Costs** are list prices from doc 43 §6 [EST]:
  - Seedance 2.5 r2v: $2.06 / $4.62 per 10 s at 480p / 720p. A 15 s scene costs $3.09 to prove at 480p and $6.93 per 720p take; we budget ×3 takes = $20.79;
  - Kling 3.0 Pro i2v, sound off: **$0.48 per 5 s insert**, budgeted ×2;
  - Cinema Studio 4.0 at 720p: $3.70 per 8 s take;
  - stills (Flare / Soul Cinema): ~$0.30 each (doc 11).
- **Brand names** are invented and differ from docs 11 and 48. Clear them on USPTO before use.
- **Real insert:** every liquid-level change, bite or drizzle is filmed for real by the client on a phone, or is cut around (§3).
- **Mascots:** Otto and Vee appear only in VXO's own spec films, so they are absent here. Any of these concepts can become a VXO spec film by casting Otto as the deadpan lead (his mouth is never visible, which also removes the lip-sync risk).

### C1 · FROSTLINE (cold brew concentrate) — "Curb Alert" (15 s)

- **Idea:** a man carries an espresso machine, a burr grinder, a gooseneck kettle and a scale out to the curb under a hand-written sign "FREE". Inside, one bottle of FROSTLINE, a glass of ice, done. Across the street, the neighbour who took the gear is now on his fourth failed shot, covered in grounds.
- **Hook (0–1 s):** the espresso machine lands on the curb with a heavy, metallic thud, a "FREE" sign taped to it. A strange image already in motion.
- **Punchline (product-caused):** the gear's new owner, lit by the morning sun through his window, hammering a portafilter, while our man sips on his porch. The cost of the ritual moved across the street.
- **Built on:** F11 (removal gag, 5.1%) and N12 (price anchor).

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Low locked-off camera on the sidewalk at curb height: the machine lands in frame, the sign flutters | Seedance. Machine is rigid, lands flat, no bounce. Write its fate: it stays |
| 2 | 1.5–3.5 | Wide from across the street on a tripod: he sets down a grinder, kettle and scale beside it, walks back in | Real-time; no other people |
| 3 | 3.5–5.5 | Kitchen counter, top-down locked off: an empty, clean counter; a hand sets down the FROSTLINE bottle and a glass of ice | **Kling i2v** from a pack still; label sharp |
| 4 | 5.5–7.5 | Side macro, slider: dark concentrate stream into the glass, level already two-thirds (hidden transfer) | **Real insert** preferred; else 2 s stream with no level change (doc 11) |
| 5 | 7.5–9 | Insert, locked: oat milk clouds into the coffee | **Real insert** (the milk cloud is the money shot; AI can't hold it) |
| 6 | 9–11 | Porch, medium, tripod: he sits, glass in hand, looks across the street | Face 3/4, no sip on camera |
| 7 | 11–13.5 | Across the street through the neighbour's window, long lens from the sidewalk: the neighbour bangs a portafilter, grounds on his shirt, steam wand hissing | Seedance. ≤2 people per frame |
| 8 | 13.5–15 | End card: bottle on the porch rail, "FROSTLINE. $1.40 a cup." | Real product photo; price super in post |

- **Physics check:** an espresso machine weighs ~20 kg: he carries it with both arms, knees bent, and it lands with a dead thud. The window shot is a long lens from public space (rig-able). No pour level changes in AI. The neighbour's steam wand gets "a thin hiss and a little vapour", not fog.
- **Audio map:**
  - 0.0 s: metal thud + sign paper flap. 0.5 s: a bird, street room tone.
  - 3.5 s: glass on stone. 5.5 s: liquid pour (library SFX on the real insert).
  - 7.5 s: soft ice settle.
  - 11 s: across-street muffled portafilter knock ×3, a steam-wand scream at 12 s.
  - 13.5 s: 0.5 s silence → two-note sonic logo.
  - VO (ElevenLabs, dry): `Gave it all away. [pause] FROSTLINE.`
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v, 15 s scene for shots 1, 2, 6, 7 (template 7.5 adapted): 480p proof $3.09 + 720p ×3 $20.79 | $23.88 |
  | Kling insert (shot 3) ×2 | $0.95 |
  | Stills, 8 | $2.40 |
  | **Total** | **≈ $27** |
- **Claim check:** "$1.40 a cup" must match the bottle price ÷ servings.

### C2 · BRAVA (hot sauce) — "Gone by Friday" (15 s)

- **Idea:** we live inside the fridge door. Monday: a row of half-used condiments and a full BRAVA. Wednesday: the others unchanged, BRAVA half gone. Friday: BRAVA upside down and empty, the others still dusty. Saturday: two new BRAVAs.
- **Hook (0–1 s):** the fridge light snaps on and the door swings open: a hand reaches straight at the lens. POV from inside the fridge door, a classic food-ad rig.
- **Punchline (product-caused):** the empty bottle is tapped on its base by a desperate hand; on the last beat, two new bottles land in its slot. The product's own fate is the joke (rule of three plus callback, doc 44 §8).

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–2 | Camera inside the fridge, locked to the back shelf, looking out at the door rack: light on, door opens, a hand grabs BRAVA. Super "MON" | Seedance 15 s scene, same locked frame for shots 1, 3, 5, 7 |
| 2 | 2–3.5 | Insert, top-down at the table: a few drops of red sauce land on a fried egg | **Kling i2v** from a real photo; drops only (no drizzle) |
| 3 | 3.5–5.5 | Same fridge POV: "WED". BRAVA half full; the mustard and ranch unchanged | State change = start/end frames |
| 4 | 5.5–7 | Insert, side: sauce on tacos, 3 drops | Kling i2v |
| 5 | 7–9.5 | Fridge POV: "FRI". BRAVA empty, upside down on its cap; a hand taps its base twice | Contact points named; one hand |
| 6 | 9.5–11 | Kitchen, medium, tripod: a person in the fridge light, holding the empty bottle up to the light, deadpan | Face 3/4, no dialogue |
| 7 | 11–13.5 | Fridge POV: "SAT". Two new BRAVAs placed in the slot; the dusty mustard behind them | Callback |
| 8 | 13.5–15 | End card: bottle on white, "BRAVA. Goes on everything. Goes fast." | Real photo |

- **Physics check:** the fridge-interior camera is a real rig (a small camera on the back shelf). The fridge light must be a cool white from above. Sauce levels change only between cuts (states, not events). The empty bottle has a sauce smear on the inside, not a clean interior. Drops: "three dark-red drops, glossy, slightly viscous, each lands and spreads 5 mm".
- **Audio map:**
  - 0.0 s: fridge seal unstick + compressor hum + light buzz.
  - 2 s: drop taps on the egg (close foley).
  - 3.5 / 7 / 11 s: the same door-open sound, each time a little faster (rule of three).
  - 8.5 s: two hollow taps on the empty bottle.
  - 11 s: the bottles clink into place.
  - 13.5 s: door thuds shut, darkness, 0.4 s silence, sonic logo.
  - No VO; supers only (graphic-design style, N4).
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v 15 s (fridge POV + kitchen), 480p proof + 720p ×3 | $23.88 |
  | Kling inserts (shots 2, 4) ×2 each; state end-frames via Kling (3 states) | $3.33 |
  | Stills, 10 | $3.00 |
  | **Total** | **≈ $30** |
- **Claim check:** none (a usage joke). Ingredients in the inserts must match the label (no chilli flakes if it's a smooth sauce).

### C3 · STACKED (kettle chips, no slack fill) — "Air Bag" (15 s)

- **Idea:** a hand squeezes a generic, puffy chip bag and it deflates like a whoopee cushion: "pfffft". It's mostly air. Then the STACKED bag is opened and poured into a bowl, and it overflows onto the table. "We fill the bag."
- **Hook (0–1 s):** the generic silver bag being squeezed, a long comic air-release sound. Strange image + sound in second 1 (N3, N8).
- **Punchline (product-caused):** chips spill over the rim of the bowl onto the table; a second hand quietly slides the generic bag into the trash.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–2 | Tabletop, locked off at bag height: a hand squeezes a plain silver bag; it collapses | **Real insert** (cheap, fun; client shoots). Unbranded bag, no logos |
| 2 | 2–3.5 | Top-down: the bag torn open, a sad handful of chips at the bottom | Kling i2v from a real photo; "exactly 9 chips" |
| 3 | 3.5–5 | Same top-down: STACKED bag torn open, packed to the top | Kling i2v; real pack photo; label sharp |
| 4 | 5–8 | Side, slider at bowl height: chips pour from the bag into a bowl, the pile rises and spills over the rim | **Real insert** preferred. AI fallback: Kling start = empty bowl, end = overflowing bowl, "solid pieces only fall and settle" |
| 5 | 8–9.5 | Macro: one chip, blistered, coarse salt, snaps in two (crumbs counted) | Cinema Studio single-shot, doc 11 CRAG prompt |
| 6 | 9.5–11.5 | Wide: a hand slides the generic bag into a trash bin under the counter | Seedance or real; one hand |
| 7 | 11.5–15 | End card: STACKED bag + overflowing bowl, super "We fill the bag." | Real photo + post type |

- **Physics check:** a chip bag holds nitrogen; squeezed, it vents slowly through the seam, not instantly. Chips are rigid and brittle: they slide, tumble and break, never bend. The pile has a natural angle of repose (~30–35°). Crumb count fixed.
- **Audio map:**
  - 0.0–1.8 s: long squeaky air release (the joke), foil crinkle.
  - 3.5 s: a heavier foil tear.
  - 5–8 s: a rising chip-pour rattle into ceramic, the spill onto wood at 7.4 s.
  - 8 s: one dry, close snap (dominant).
  - 10.5 s: trash-bin lid clack.
  - 11.5 s: a single kick-drum hit, logo.
  - VO: `[deadpan] That's air. [pause] This is chips. STACKED.`
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Kling inserts (shots 2, 3, 4 fallback) ×2 | $2.86 |
  | Cinema Studio 8 s macro ×2 | $7.39 |
  | Seedance 2.5 r2v 10 s (shot 6) 480p proof + 720p ×2 | $11.30 |
  | Stills, 6 | $1.80 |
  | **Total** | **≈ $23** |
- **Claim check (critical):** the fill must be the client's real, typical fill (21 CFR 100.100). The rival bag is **generic** and unbranded. Don't say "other brands are 70% air" without data. "We fill the bag" is supportable only if the bag really is near-full; show it with a real insert.

### C4 · NIGHTSHIFT (decaf, Swiss Water) — "Lights Out" (15 s)

- **Idea:** 11:47 p.m. A woman pulls a double espresso at home. Her partner in the doorway stares in horror. She turns the bag: "DECAF". She finishes the cup, sets it down, and the house lights go out one by one as she walks to bed.
- **Hook (0–1 s):** a wall clock at 11:47 (post comp) and the espresso machine's pump roaring in a dark kitchen. Wrong time + loud sound.
- **Punchline (product-caused):** the horrified partner is the one still awake at the end, staring at the ceiling, while she sleeps instantly. A reversal (doc 44 §8.3).

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Kitchen wide, locked: dark room, one under-cabinet light, the machine humming | Seedance. The clock face is a post comp |
| 2 | 1.5–3 | Insert: two espresso streams into a small cup (cup already half-full) | **Real insert** or 2 s stream with no level change |
| 3 | 3–5 | Doorway, medium, tripod: the partner in pyjamas, eyes wide, frozen | Face emotion as action: "eyes widen, one slow blink" |
| 4 | 5–7 | Over-shoulder from behind her: she turns the bag to him | **Kling i2v** for the bag in hand: "DECAF · Swiss Water Process" from the real pack |
| 5 | 7–9 | Medium: she sets the empty cup in the sink, walks out of frame | No sip on camera; the cup is empty (result) |
| 6 | 9–11 | Hallway, wide, locked: lights switch off one by one as she passes (3 clicks) | Practical lights; exact count 3 |
| 7 | 11–13.5 | Bedroom, top-down locked: she asleep instantly; he lies beside her, eyes open, staring | ≤2 people; blanket physics |
| 8 | 13.5–15 | End card: bag on the dark counter, "NIGHTSHIFT. All the coffee. None of the night." | Real photo |

- **Physics check:** domestic lighting off-switch gives an instant cut-to-dark on each fixture, not a fade. Top-down bedroom shots are rigged from a ceiling arm (real). The espresso flow at 25–30 s per shot is shown only as a 1.5 s segment.
- **Audio map:**
  - 0.0 s: vibratory pump roar (loud on purpose), fridge hum under.
  - 1.5 s: the stream trickle.
  - 3 s: dead silence on his face (0.8 s).
  - 5.5 s: a bag crinkle.
  - 9–11 s: three wall-switch clicks, each with a lower room tone.
  - 11 s: a clock tick, one long exhale from him at 12.5 s.
  - 13.5 s: soft two-note logo.
  - No dialogue (lips stay off; Seedance native audio kept only for foley timing, doc 43 §4).
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v 15 s (shots 1, 3, 5, 6, 7) 480p proof + 720p ×3 | $23.88 |
  | Kling insert (shot 4) ×2 | $0.95 |
  | Stills, 8 | $2.40 |
  | **Total** | **≈ $27** |
- **Claim check:** "decaf" in the US has no FDA percent rule; the industry norm is ≥97% removed. Say "Swiss Water decaf", not "caffeine-free". No sleep claims: the joke shows the *partner* awake; she simply goes to bed. Don't super "helps you sleep".

### C5 · MATEO (sparkling yerba mate, 120 mg caffeine) — "The Crack Heard Round the Office" (15 s)

- **Idea:** a silent open-plan office at 2:58 p.m. One person cracks a MATEO. The sound is so crisp that the whole floor stops typing and looks up. Beat. Then a dozen cans crack across the room in unison.
- **Hook (0–1 s):** a macro of the tab lifting, and the loudest, cleanest can-crack you've heard. Product sound as the hook (N8: 64%).
- **Punchline (product-caused):** the office manager, the last holdout, slowly reaches under her desk and cracks hers too, deadpan. Rule of three: one can, a dozen cans, the boss.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Macro, locked, can at the frame edge in profile: the tab lifts once, a 0.3 s vapour puff | **Kling i2v** from the can photo; "the tab lifts once and stays up" |
| 2 | 1.5–3.5 | Wide office, locked from a high corner (security-cam height): every head rises from a screen | Seedance; ≤12 people at a distance, faces soft |
| 3 | 3.5–5 | Medium: the cracker freezes, can halfway to her mouth | No sip |
| 4 | 5–7 | Three quick close-ups (0.6 s each) of coworkers' eyes moving to her | Seedance cuts; averted or 3/4 faces |
| 5 | 7–9 | Wide again: a dozen hands reach for desk drawers; cans crack almost in unison | Hands at distance; cans pre-placed |
| 6 | 9–11.5 | Glass office at the back, long lens through the glass from the floor: the manager, unmoved, typing | Reflections in the glass: name them ("soft overhead fluorescent reflections, no camera visible") |
| 7 | 11.5–13.5 | Same: she reaches under the desk, cracks a can, deadpan, eyes still on her screen | Callback |
| 8 | 13.5–15 | End card: can on a desk, "MATEO. 120 mg caffeine from yerba mate." | Real photo + post super |

- **Physics check:** a can crack makes one vapour puff, not a spray, unless shaken. Office crowd at distance only (doc 43: Seedance glitches beyond 3 characters in focus). The glass-office shot is from outside the glass (a crew can rig a long lens on the floor), never through it.
- **Audio map:**
  - 0.0 s: tab crack + hiss, close and dry (master it to −8 dBFS peak; this is the hook).
  - 0.5–1.5 s: keyboards stop one by one.
  - 1.5–5 s: near-silence, an HVAC hum, one chair creak.
  - 7.2 s: a dozen cracks inside ~0.4 s (stagger them by hand).
  - 11.6 s: the manager's single crack, quieter, through glass (low-pass).
  - 13.5 s: sonic logo.
  - No VO. On-screen type does the claim.
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v 15 s (shots 2–7), 480p proof + 720p ×3 | $23.88 |
  | Kling insert (shot 1) ×2 | $0.95 |
  | Stills, 8 | $2.40 |
  | **Total** | **≈ $27** |
- **Claim check:** 120 mg must match the label. Target **18+ on TikTok** (energy-drink rule). No "focus", "productivity" or "beats the 3 p.m. slump" claims: the film shows a sound, not an effect.

### C6 · TIDE & TIN (tinned fish) — "Lunch Upgrade" (20 s)

- **Idea:** a break-room table. One coworker peels open a generic can of tuna; a grey, flat lunch. Across from him, another peels a TIDE & TIN tin: smoked trout in olive oil, lemon, chilli. She tips it onto sourdough with a twist of pepper. Coworkers drift over like it's a magic trick. The first guy quietly puts the lid back on his can.
- **Hook (0–1 s):** the peel of the tin's key, a metallic rip, in macro, with oil glinting.
- **Punchline (product-caused):** the lid going back on the sad can, with a tiny sad "tink". Category villain → hero (F10's logic as comedy).

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Macro, locked: a hand peels a TIDE & TIN tin; fillets glint in oil | **Kling i2v** from a real opened-tin photo; "exactly 3 fillets, no garnish not in the reference" |
| 2 | 1.5–3.5 | Two-shot across the table, tripod: him with a grey can; her with the tin | Seedance; ≤2 people; faces 3/4 |
| 3 | 3.5–5.5 | Top-down: fillets laid on toasted sourdough, lemon zest, chilli flakes from a pinch | **Kling start/end** frames: bare toast → dressed toast |
| 4 | 5.5–8 | Wide: three coworkers drift into the background, coffee in hand, watching | Seedance; background people soft |
| 5 | 8–10 | Close: his can, grey tuna, a fork stuck upright in it | Locked; rigid fork, four tines |
| 6 | 10–12 | Medium on her: she offers him a piece, slides the toast across | No bite on camera |
| 7 | 12–14 | Insert: his hand presses the lid back onto his can | Real insert or Kling |
| 8 | 14–17 | Wide: the coworkers now crowd her side; he sits alone, slightly smiling | Callback |
| 9 | 17–20 | End card: the tin on linen, "TIDE & TIN. Wild trout, smoked in [state]." | Real photo |

- **Physics check:** oil in a tin moves slowly and clings; fillets flake along lines, never stretch. No eating on camera. Flakes of chilli fall and stay (fate written). The fork stands in packed tuna (it's dense).
- **Audio map:**
  - 0.0 s: tin-key peel, a crisp metallic rip (hook).
  - 1.5 s: break-room hum, microwave beep in the distance.
  - 3.5 s: toast crunch under the knife, a pepper-grinder twist at 4.6 s.
  - 5.5 s: footsteps, a mug set down.
  - 12 s: the sad lid "tink".
  - 14 s: soft guitar sting.
  - VO (optional, female, dry): `Same lunch break. [pause] Better tin.`
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v 15 s (shots 2, 4, 6, 8), 480p proof + 720p ×3 | $23.88 |
  | Kling inserts (1, 3, 5, 7) ×2 | $3.81 |
  | Stills, 10 | $3.00 |
  | **Total** | **≈ $31** |
- **Claim check:** "wild", species, smoke method and origin must match the lot. The rival can is generic. **Allergen:** fish is a major allergen; garnish must match the serving suggestion, and the end card shows "serving suggestion".

### C7 · SALTWELL (electrolyte stick, 1,000 mg sodium) — "Moving Day" (20 s)

- **Idea:** July, a fourth-floor walk-up. Three friends carry a sofa up the stairs. At each landing, two of them collapse; the third tears a SALTWELL stick into her water bottle and shakes it. At the top, it's her alone, still holding the sofa end, and the other two are lying on the landing below.
- **Hook (0–1 s):** a sofa jammed at a stairwell turn, three people grunting, low angle up the stairwell.
- **Punchline (product-caused):** the last landing: she looks down at the two flattened friends, rips a second stick, and drops it down the stairwell to them. It lands on one friend's chest.
- **Note:** the "performance" reading is a joke, but it is still an implied claim. Keep it a dramatization with a super and no words about performance.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Low angle from the bottom of the stairwell, wide lens: sofa jammed at the turn | Seedance; sofa rigid, never bends |
| 2 | 1.5–3.5 | Landing 2, medium, tripod: two of them slump against the wall, sweating | Sweat = "beads on the temple, damp T-shirt collar" |
| 3 | 3.5–5 | Insert: she tears a stick, powder pours into a water bottle (narrow stream) | **Real insert** (powder is a fluid; AI risk) |
| 4 | 5–6.5 | Insert: bottle shaken, the water clouds, then clears pink | Kling start/end: clear → pink |
| 5 | 6.5–10 | Stairwell, handheld follow from below: she pushes up with the sofa end, the others drag behind | Seedance; real weight: "knees bent, sofa tilts, the leading edge scrapes the wall" |
| 6 | 10–12.5 | Landing 4, top-down from the stairwell rail: two friends flat on the landing below | Seedance; locked top-down (a crew can rig a camera over the rail) |
| 7 | 12.5–15 | Medium on her at the top: she rips a second stick, drops it over the rail | Object fate: it falls straight, lands on a chest |
| 8 | 15–17 | Top-down: the stick lands on the friend's chest; he lifts a thumb | Callback |
| 9 | 17–20 | End card: box of sticks, "SALTWELL. 1,000 mg sodium per stick." + small "Dramatization" | Real photo; supers in post |

- **Physics check:** sofas weigh 40–60 kg: two-person lifts, never one-handed. The stick (5 g) falls fast and lands flat. Sweat beads don't flow upward. Top-down over a stairwell rail is a real rig with a safety line (don't show the rig).
- **Audio map:**
  - 0.0 s: the sofa scraping drywall, grunts.
  - 1.5 s: heavy breathing, a fan whirring in an apartment.
  - 3.5 s: paper-stick tear, powder hiss into the bottle.
  - 5 s: four hard bottle shakes.
  - 6.5–10 s: footsteps on wooden stairs, rhythmic.
  - 13 s: the stick drops (falling whistle is too cartoon: use a soft paper tap at 15.2 s).
  - 17 s: sonic logo.
  - VO: none; or `[flat] Salt. [pause] Well.`
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v 15 s (1, 2, 5, 6, 7, 8), 480p proof + 720p ×3 | $23.88 |
  | Kling insert (4) ×2 | $0.95 |
  | Stills, 10 | $3.00 |
  | **Total** | **≈ $28** |
- **Claim check:** sodium amount on screen as a fact only. **No "hydrates you 3× faster", "prevents cramps" or performance claims.** Super "Dramatization." Adults only. No weight or body claims (TikTok/Meta 18+ health rules, §4.2).

### C8 · SUNDAY GRAVY (jarred marinara) — "Customs" (20 s)

- **Idea:** an Italian-American grandmother sits at her kitchen table like a customs officer. Her grandson places a jar of SUNDAY GRAVY in front of her. She inspects it: holds it to the light, reads the ingredient list with glasses on the tip of her nose, opens it, smells it. Long, uncomfortable pause. Then she slides it into her own pantry and closes the door.
- **Hook (0–1 s):** the jar slammed down on the oilcloth table by a hand, a hard glass-on-wood "clunk", and her already-suspicious glare in the background.
- **Punchline (product-caused):** the confiscation. She keeps it, and won't give it back. The held final shot is the joke (doc 43 §7.5).

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Table level, locked: the jar lands in the foreground; her face soft in the background | **Kling i2v** for the jar; Seedance for the scene |
| 2 | 1.5–4 | Medium on her, tripod: she lifts the jar to the window light, tilts it | Real talent reference (licensed) or averted; "liquid in the jar moves slowly, thick" |
| 3 | 4–6.5 | Insert, over her shoulder: reading glasses, the label's ingredient list (post-comped from the real label) | **Kling i2v**; label text from the photo |
| 4 | 6.5–8.5 | Insert: the lid twisted, a soft vacuum pop | Kling; one pop, lid stays off |
| 5 | 8.5–10.5 | Close on her: she smells it, eyes closed | No mouth movement |
| 6 | 10.5–14 | Two-shot, wide, locked: the grandson waits; she says nothing. Long pause | The pause is an event with its own sound |
| 7 | 14–17 | Medium: she stands, opens the pantry, places the jar inside, closes the door, sits back down | Seedance; the pantry has 4 identical old jars (exact count) |
| 8 | 17–20 | End card: the jar on the table, "SUNDAY GRAVY. Nonna-approved. Probably." | Real photo |

- **Physics check:** marinara is thick: tilted, it moves slowly and coats the glass. A vacuum-sealed lid pops once. No sauce pour, no tasting. All movement is a seated elderly person's pace.
- **Audio map:**
  - 0.0 s: glass-on-wood clunk (hook).
  - 1.5 s: kitchen room tone, a clock tick, a radio murmuring Italian far away.
  - 4 s: glasses unfolded.
  - 6.8 s: lid pop.
  - 8.5 s: one long inhale.
  - 10.5–14 s: silence + the clock tick, louder each second.
  - 15.5 s: pantry door creak and click.
  - 17 s: a mandolin sting.
  - VO: none. Optional end super.
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v 15 s (shots 1, 2, 5, 6, 7), 480p proof + 720p ×3 | $23.88 |
  | Kling inserts (3, 4) ×2 | $1.90 |
  | Stills (incl. talent sheet), 10 | $3.00 |
  | **Total** | **≈ $29** |
- **Claim check:** "Nonna-approved. Probably." is puffery, not a testimonial. She gives no verdict in words, so no fake-review issue (16 CFR 465). Ingredients in the post-comped label match the real jar.

### 6.1 Ranking

**The best concept: C2 "Gone by Friday" (BRAVA).**
- The hook is a real, rig-able camera position nobody uses enough (inside the fridge door), and the hand reaching at the lens is a strange image in motion in second 1.
- The punchline is pure product truth (it gets used up), told by the product's own state, so there is **no claim to substantiate**.
- It needs no AI faces for the story, no bites, no pours, and the level changes happen **between cuts** (states, not events), which is exactly where AI is safe (§3).
- It cuts natively into a 6 s loop (MON → FRI → SAT) and into graphic-design variants (the day supers), which is what snacks and condiments reward (N4).
- It can be re-skinned for any condiment, sauce, dressing or drink on the 20-type list: a template the client can order again (Season plan).

**Second: C5 "The Crack Heard Round the Office" (MATEO).** The product sound *is* the hook and the punchline (N8), and it fits the strongest TikTok Shop category (functional drinks, N11).

**Third: C1 "Curb Alert" (FROSTLINE).** It turns a measured winner's gag (F11, 5.1%) into a cinematic film with a price anchor.

For a VXO food spec reel, make **C2 + C5 + C3**: one condiment, one drink and one snack, all claim-light.

---

## 7. QA gate additions for this niche

Run after doc 44 §10, doc 45 §5.4 and doc 48 §7:

1. **Ingredient match:** every frame of food matches the real product and the ingredient list. No added seeds, nuts, herbs or garnish (allergen check).
2. **Portion and fill:** the size, count and fill level never change within a shot and match the real pack (FTC mock-up rule; slack fill).
3. **No generated liquid-level change, bite, sip, drizzle or cheese pull.** Each is a real insert or happens between cuts.
4. **Steam:** wisps, not fog; no orbit around steam.
5. **Text:** label from the real pack photo only. Every number (g, mg, $) is a post super that matches the nutrition panel.
6. **Claims:** run the §4.2 cheat-sheet. No effect words (gut, focus, energy all day, burns, hydrates faster, sleep).
7. **Age gates set:** energy and caffeine products 18+ on TikTok; any weight or body angle 18+ on both platforms.
8. **No AI person gives a taste verdict or testimonial.** Parody characters make no factual claim.
9. **The real product photo closes the film.**
10. **Native wrapper ready:** a 6 s cut, 3 hook variants (first-frame swaps, finding 2) and 4–6 graphic-design variants.

## Sources

All URLs are inline in the tables above. Measured files and their metadata: `scratchpad/niche/food/meta.txt` and `analysis.txt` (not committed). The local script ran ffmpeg scene detection at 0.30, astats RMS per 0.5 s, and 2 fps 8×4 frame tiles. Additional sources read:
- Benly Q1 2026 benchmarks: [F&B](https://benly.ai/benchmarks/q1-2026/food-beverage), [snacks & confectionery](https://benly.ai/benchmarks/q1-2026/food-beverage/snacks-confectionery), [organic & health foods](https://benly.ai/benchmarks/q1-2026/food-beverage/organic-health-foods). The coffee & tea sub-page returned 404.
- [Motion visual formats by vertical](https://motionapp.com/library/research/creative-benchmarks-2026/visual-formats-by-vertical): no Food & Nutrition leaderboard published.
- [TikTok F&B blog / Marketing Science study](https://ads.tiktok.com/business/en/blog/elevate-your-food-and-drink-ads).
- [Higgsfield food product video ad guide 2026](https://higgsfield.ai/blog/food-product-video-ad-ai-2026); [Flowjam AI video for restaurants 2026](https://www.flowjam.com/blog/ai-video-for-restaurants-2026).
- [Modern Retail on TikTok Shop food, Oct 2025](https://www.modernretail.co/technology/tiktok-is-talking-to-brands-like-its-a-grocer-now/); [eightx TikTok Shop food economics](https://eightx.co/blog/tiktok-shop-food-brand-channel-economics).
- Policy pages and lawsuits as linked in §4.
