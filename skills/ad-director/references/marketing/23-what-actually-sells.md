# 23 · What actually sells: evidence from long-running ads and 2025–26 studies

Research brief, 2026-10-08. It checks our creative rules (01, 02, 03, 15) against **what advertisers keep paying for**, not against opinion. `[inf]` marks our own inference. Every sample size is stated. Findings already in 01/03 (ABCD, Meta×Toluna 1.7×, VidMob text speed, Motion format hit rates) are not repeated unless new data changes them.

---

## 0. Method, sources and limits (read first)

| Source | What we got | n | Status |
|---|---|---|---|
| **Own coded sample**: Meta Ad Library ads mirrored by [brandmov.com](https://brandmov.com/watchlist/skincare/) (watchlists + `/watch/<brand>/` pages, which carry the ad's run-days, video file, hook/angle tags) | 51 videos downloaded, contact-sheeted (15 frames each), transcribed with Whisper base.en, shot-counted with ffmpeg scene detection, **then deleted** | **50 unique creatives** (one Bellroy ad ran under 2 IDs), 30 brands; **35 ran ≥60 days** | Done |
| Brandmov hook/angle tags across all watchlists | Tag share for long vs short runners | **872 ads** (275 ran ≥60 d, 417 <30 d) | Done |
| [Benly Creative DNA, Q1 2026](https://benly.ai/benchmarks/q1-2026) (Meta) | Hook types, asset types, lifespan per vertical | 271K creatives, 1.6K brands | Done |
| [Motion 2026 Creative Benchmarks](https://motionapp.com/thumbstop-pulse/creative-benchmarks-2026) + LLM data appendix | Hit rates by visual style / hook / asset | 550K+ ads, 6K advertisers, $1.3B | Done |
| [System1 × TikTok, Aug 2025](https://chiefmarketer.com/system1-tiktok-study-branding-elements-and-creator-led-content-improve-short-form-video-ads/) | Early-branding effects | 887 ads, 92K viewers, 8 markets | Done |
| [Ipsos "Short-Form Social Misfits" 2025](https://www.ipsos.com/en/misfits/short-form-social-misfits-0) | What drives memory/behaviour on TikTok/Reels/Shorts | ~500 ads (n=489; TikTok subset 289) | Done |
| [TikTok "Power Creative Elements"](https://ads.tiktok.com/business/creativecenter/quicktok/online/Power_Creative_Elements/pc/en) | Element prevalence and lifts | ~4,000 ads (2021 data) | Done, old |
| **TikTok Creative Center Top Ads** | — | — | **Not obtained.** The list API returns `40101 no permission` without a signed session header; the page is client-rendered. We did not try to reverse-engineer the signing. |
| **Meta Ad Library (direct)** | — | — | **Not obtained.** facebook.com returns a JS bot challenge (403) to scripts; the official API needs a token we don't have. The brandmov mirror replaced it. |
| **Motion Creative Analytics MCP** | — | — | **Not usable.** `get_auth_context` returned no organisation or workspace, and every Inspo/brand tool requires a workspace ID. |

**What "long-running" means here.** Meta shows no spend or ROAS. An ad still live after 60+ days is a *profitability proxy*: brands pause losers within ~2–4 weeks. [Benly](https://benly.ai/benchmarks/q1-2026) puts the cross-industry median lifespan at **22 days**, and only **13–21 %** of creatives pass 60 days. So our ≥60-day set is roughly the top fifth by survival. It is still a proxy: the ad could be running at low spend `[inf]`.

**Sample bias.** Brandmov tracks particular DTC brands, so mass-premium DTC is over-represented (Face Reality, HexClad and similar) and luxury houses under-represented. Most luxury fragrance and coffee brands had only 1–2 ads indexed. Treat per-niche counts under 10 as anecdotes.

---

## 1. What the large datasets say (2025–26)

### 1.1 Hook types that survive (Benly Q1 2026, Meta, video creatives)
| Vertical (n creatives) | Top hook (share of video) | Second | Note |
|---|---|---|---|
| Beauty & personal care (50.8K, 311 brands) | Bold statement 31.7 % | Visual intrigue 27.8 % | Pattern interrupt lives longest (31 d vs 28 d) |
| Food & beverage (16.5K, 114 brands) | Visual intrigue 29 % | Bold statement 26.3 % | Bold statement lives longest (39 d) |
| Fashion & apparel (76.9K, 419 brands) | **Visual intrigue 58.6 %** | Pattern interrupt 15.6 % | Watches, jewelry, footwear and luxury fashion all: top hook = visual intrigue, top asset = **Lifestyle/Editorial** |
| Home & living (18.6K, 136 brands) | Visual intrigue 40.4 % | Bold statement 22.4 % | — |

Sources: [beauty](https://benly.ai/benchmarks/beauty-personal-care), [food](https://benly.ai/benchmarks/q1-2026/food-beverage), [fashion](https://benly.ai/benchmarks/q1-2026/fashion-apparel), [home](https://benly.ai/benchmarks/q1-2026/home-living).

**Asset type by vertical** (Benly "effectiveness" 0–100; estimated from longevity, not advertiser KPIs):
- **Beauty:** UGC 55 ≈ Branded/Studio 54 ≈ Product shot 52 > Lifestyle/Editorial 46. Studio has the best 30-day survival (37 %).
- **Food & beverage:** UGC 68 > Studio 64 > Lifestyle 62.
- **Fashion:** UGC 73 > Lifestyle 66 > Product shot 63 > Studio 59. But Lifestyle is used **5×** more (41K vs 7.9K creatives).
- **Home:** **Product shot 66** > UGC 62 >> Lifestyle 30. Pure mood ("lifestyle") scores worst in home.

**Lifespan by sub-niche:** watches 48 d, jewelry 43 d, footwear 43 d, coffee & tea 38 d, luxury fashion 29 d, fragrance 27 d, skincare 31 d. Fragrance creatives **refresh fastest** among our niches; plan more variants there `[inf]`.

### 1.2 Motion 2026 (550K ads, Meta): winners = ≥10× account-median spend
- **Styles:** unconventional text placement 9.6 %, behind-the-scenes 8.6 %, **ASMR 8.6 %**, POV 8.3 %, demo 8.1 %, testimonial 6.6 %, listicle 5.3 %.
- **Hooks:** newness 11.4 %, sale 11.4 %, price anchor 10.9 %, confession 8.7 %, curiosity 7.8 %, bold claim 7.2 %, storytelling 6.2 %, question 5.5 %.
- **Assets:** text-only 11.6 %, product image + text 8.8 %, UGC 7.6 %, **high production 7.0 %**, animation 4.6 %.
- **Verticals:** fashion's top styles include "stylized product shot", "product shot" and ASMR. In home, "demonstration and process matter more than anything else."

UGC (7.6 %) barely beats high production (7.0 %), so "polished loses" is not supported at Meta scale. **A clear message in text, plus novelty or an offer, wins.**

### 1.3 Brand-effect studies
- **System1 × TikTok (887 ads):** sonic asset in the first 2 s = **+191 %** brand-awareness lift; **logo in context** (on the pack, in the scene) = +182 %; fluent character = +57 %. **Logo overlays reduced lift.** Exceptional early branding = 57 % more happiness, 48 % less negative sentiment, 19 % less attention decay. Creator-led ads got 39 % more attention.
- **Ipsos (~500 short-form ads):** high performers on memory were **1.4× more likely to have a unique visual profile**. "Visually unique ads are 1.5× more effective than ads that simply showcase the brand." Brand time on screen helped less (+7 % to +17 % index). Creator-led TikTok ads: +13 % memory encoding, +19 % behaviour change. Ads that **show how-to, give a recipe or unbox** delivered **1.5× the behaviour change**.
- **TikTok elements (~4K ads, 2021):** text overlays in 71 %, music in 63 %, VO in 39 %. **Faces filling <20 % of the frame: +31 % consideration**; surprising transitions +53 % recall.

---

## 2. Our coded sample: 50 Meta ads from premium-leaning DTC brands

### 2.1 Coding of the 35 long runners (days = days live at brandmov's last fetch, Apr–Jul 2026)
P2 = product, or product in use, visible by 2.0 s. Txt = text overlay carries the message. Talk = a person speaks to camera as the main visual. Audio: S = speech (VO or dialogue), M = music, A = ASMR, — = silent.

| # | Brand (niche) | Days | Len s | Format | P2 | Txt | Talk | Audio | Hook (first 3 s) |
|---|---|---|---|---|---|---|---|---|---|
| 35 | Kuru (shoes) | 377 | 11 | graphic + reviews | Y | Y | N | S | "Do they work?" + review pop-ups |
| 20 | HexClad (cookware) | 327 | 68 | hands/process | Y | Y | N | S | food hero + "worth every penny" VO |
| 0 | Kora Organics (skincare) | 292 | 15 | studio aesthetic | Y | Y | N | M | dropper macro + "80 % saw pores minimized" |
| 16 | Oats Overnight (food) | 287 | 47 | founders skit | N | Y | Y | S | "making an oatmeal ad with AI" |
| 23 | Brilliant Earth (jewelry) | 268 | 17 | CGI render | Y | Y | N | — | rotating ring render + collection title |
| 36 | American Giant (denim) | 261 | 95 | host + archive doc | Y | Y | Y | S | contrarian: "America doesn't make the best jeans anymore" |
| 10 | Omnilux (LED skincare) | 242 | 50 | expert + mashup | Y | Y | Y | S | myth question: "Do LED masks really work?" |
| 32 | Cobbler Union (shoes) | 212 | 31 | craft B-roll | N | Y | N | S | "Handcrafted… but just words until…" |
| 24 | Brilliant Earth (jewelry) | 210 | 10 | wrist macro | Y | Y | N | M | iMessage bubbles debating bracelets |
| 14 | Mid-Day Squares (snack) | 205 | 20 | creator + VO | Y | Y | N | S | "POV:" text + "What if your cheat snack…" |
| 25 | Bellroy (travel) | 183 | 30 | top-down stop-motion | N | Y | N | M | "NEAT?" over a messy suitcase |
| 15 | Mid-Day Squares | 173 | 136 | founder selfie | Y | Y | Y | S | scarcity: "selling like hotcakes" |
| 9 | Izil (skincare) | 153 | 15 | studio aesthetic | Y | Y | N | M | heritage ritual imagery, ingredients as text |
| 50 | Master & Dynamic (audio) | 153 | 24 | hands ASMR | Y | N | N | A | hands cleaning headphones |
| 8 | Goop Beauty (eye masks) | 152 | 77 | expert + editorial | Y | Y | Y | S | surgeon intro, wearing the product |
| 7 | RMS Beauty (makeup) | 147 | 64 | founder tutorial | N | Y | Y | S | founder origin story |
| 12 | Pique (tea) | 138 | 29 | doctor + press | N | Y | Y | S | "As a longevity doctor…" |
| 21 | Crate & Barrel (registry) | 138 | 15 | lifestyle + perks | Y | Y | N | M | store + benefit list text |
| 47 | Daniel Wellington (watches) | 137 | 8 | editorial model | Y | Y | N | M | watch on wrist, "Refined Icons" |
| 37 | Dossier (fragrance) | 134 | 13 | lifestyle, licensed song | Y | Y | N | M | hand picks bottle; "The summer I wore IT FACTOR" |
| 46 | Boy Smells (candles) | 123 | 20 | editorial bodies | Y | Y | N | M | "Spa Smells" title over product |
| 13 | Pique (tea) | 104 | 6 | studio pour loop | Y | N | N | — | champagne-tower pour on black |
| 33 | Monta (watches) | 104 | 21 | gloved-hands demo | Y | Y | N | M | "Can your clasp do this?" |
| 3 | Dermalogica | 103 | 47 | UGC talk | N | Y | Y | S | "There has been a breakthrough…" |
| 4 | Dermalogica | 103 | 16 | UGC routine | Y | Y | N | M | routine steps as text |
| 31 | Sarah Flint (shoes) | 99 | 4 | fake cart UI | Y | Y | N | — | "Your Cart: $100 off unlocked" |
| 18 | SkinnyDipped (snack) | 98 | 7 | trend meme | Y | Y | N | M | trend dance in a store aisle |
| 22 | Bed Threads (bedding) | 97 | 37 | cinematic room | Y | Y | N | M | sunlit bedroom, slow |
| 30 | Calpak (bags) | 93 | 45 | UGC story + VO | Y | Y | N | S | "Traveling with my first baby was a NIGHTMARE" |
| 5 | Merit (makeup) | 92 | 62 | UGC talk | Y | Y | Y | S | "Just watch how quickly this works" |
| 34 | Vessi (sneakers) | 86 | 27 | UGC talk | Y | Y | Y | S | "If you thought waterproof shoes had to look ugly…" |
| 1 | Kora Organics | 85 | 21 | founder | Y | N | Y | S | founder holds product to camera |
| 6 | Merit | 78 | 45 | UGC talk | Y | Y | Y | S | "It says right on the box, you can't mess this up" |
| 27 | Charlotte Chesnais (jewelry) | 60 | 3 | hand editorial | Y | N | N | — | three ring-on-hand cuts |
| 28 | Demellier (bags) | 60 | 15 | editorial model | Y | Y | N | M | kinetic product name over bag |

**The 15 short runners (<60 d)** are mainly:
- creator or founder talk: La Mer 21 d, Summer Fridays, Maison Louis Marie, Henry Rose, Cometeer, Olaplex;
- studio/CGI: Tatcha 55 d, Augustinus Bader before/after, Lindberg render, Salomon surreal CGI 24 d;
- offers and native: Winc offer, Joanna Vargas still, Hint, Poppi ASMR, Mejuri BTS.

### 2.2 Aggregates

| Metric | All (n=50) | **Long ≥60 d (n=35)** | Short <60 d (n=15) |
|---|---|---|---|
| Product visible by 2 s | 74 % | **83 %** (29/35) | 53 % (8/15) |
| Message-bearing text overlay | 84 % | **89 %** (31/35) | 73 % |
| Talking head (person speaks to camera) | 36 % | **34 %** (12/35) | 40 % |
| No talking head *and* no speech | — | **51 %** (18/35) | — |
| Speech present (VO or dialogue) | 48 % | 49 % (17/35) | 47 % |
| …of which VO over visuals, no talking face | — | 5/35 (HexClad, Cobbler Union, Calpak, Mid-Day, Kuru) | — |
| Music-only / silent / ASMR | 34 / 14 / 4 % | 37 / 11 / 3 % | — |
| Median length | 20 s | **21 s** (IQR 15–47) | 12 s |
| Length bands ≤15 / 15–30 / 30–60 / >60 s | 17/16/10/7 | **9/13/7/6** | 8/3/3/1 |
| Aspect 9:16 / 1:1 / 4:5 / 16:9 | 41/4/4/1 | 29/4/2/0 | — |
| AI/CGI-looking | 3 | 1 (Brilliant Earth render, 268 d) | 2 |

**By niche group (all ages)** `[small n]`:
- **Beauty (n=19):** 63 % talking heads; median 32 s; 6/19 >60 s, all UGC/founder/expert. The no-face winners (Kora 292 d, Izil 153 d, Tatcha, Dermalogica routine) all carry **a claim or ingredient in text over macro/texture**.
- **Food/beverage/coffee (n=10):** 40 % talking heads; median 21 s. Long runners split between authority/founder (Pique, Mid-Day, Oats) and sensory/native (Pique pour loop 104 d, SkinnyDipped trend 98 d).
- **Fashion/accessories/watches/jewelry/shoes (n=16):** **12 % talking heads**; median 13 s; 50 % music-only. Hands, editorial and render formats dominate: Brilliant Earth 268/210 d, Monta 104 d, DW 137 d, Bellroy 183 d.
- **Home/candles/audio (n=5):** 0 % talking heads; 100 % product by 2 s.

**Brandmov tag analysis (872 ads; tags are brandmov's).** Shares among ads live ≥60 d vs <30 d:
- Hooks that **over-index** in long runners: feature-breakdown 12.4 vs 7.9 %, "the secret" 9.8 vs 5.5 %, "x tips" 9.5 vs 6.0 %, "you're doing it wrong" 7.3 vs 5.3 %.
- Hooks that **under-index**: sale 5.1 vs 9.1 %, "now available" 3.6 vs 8.9 %, social-proof 6.2 vs 9.1 %, "you should never" 5.5 vs 8.9 %.
- Angle "benefit-stack" 55.6 vs 45.1 %.
- Video share was the same (47 vs 45 %).
- Reading `[inf]`: offer and launch hooks are short-lived by design (promos end), and **mechanism/benefit-explaining hooks keep earning**. Caveat: a few brands (Face Reality has 33 ads) skew it.

### 2.3 What the contact sheets show
1. **Frame 1 is the product or the product in use**, not a mood shot. Even the most aesthetic long runners (Kora, Izil, DW, Dossier, Brilliant Earth) open with the bottle, ring or watch filling ≥30 % of the frame.
2. **Aesthetic winners still "talk" in text:**
   - Kora repeats one claim + one stat on every frame;
   - Izil names four ingredients;
   - Monta asks a challenge question;
   - Brilliant Earth uses iMessage bubbles.

   The only text-free long runners are under 6 s, or ASMR.
3. **Hands are the default human.** 8/50 ads are hands-only; 6 of those 8 ran ≥98 d.
4. **Craft or mechanism as proof:** Cobbler Union's artisans (212 d), Cometeer's liquid-nitrogen freeze, Monta's tool-less clasp.
5. **Premium talking heads are authorities** (doctor, surgeon, dermatologist, founder, story host). They last when line 1 is a **myth, contrarian claim or category question**.

---

## 3. Per-niche: what winners do

Counts are from our sample; benchmarks from §1.

- **Fragrance** (n=4 videos: Dossier, Henry Rose, Maison Louis Marie, Summer Fridays). The only fragrance video past 60 d (Dossier, 134 d, 13 s) is **lifestyle + licensed song + persistent "The summer I wore [NAME]" text + bottle in hand by 0.1 s**. Creator talk pieces (28–37 d) live shorter. Benly: fragrance lifespan 27 d, the shortest of our niches, so it needs a refresh every ~4 weeks. → **Mood is fine, but name the moment in text from frame 1.**
- **Skincare** (n=12). Two winning modes:
  - (a) an authority or creator explaining a mechanism with a question/myth hook (Omnilux 242 d, Goop 152 d, Dermalogica 103 d);
  - (b) a **texture/dropper macro with a numeric claim on screen** (Kora 292 d, Izil 153 d, Tatcha 55 d).

  Benly: beauty studio ≈ UGC on effectiveness (54 vs 55). → Our style is viable *if* it carries a number or ingredient.
- **Makeup** (n=3): demo-on-face UGC wins (Merit 92/78 d, RMS 147 d), 45–64 s, single take. Faces are the proof. → Hard to do faceless `[inf]`; use swatch/texture as the hero and accept lower fit.
- **Beverages / tea / coffee** (n=6). Long runners:
  - doctor authority (Pique 138 d);
  - a **5.7 s silent pour loop** (Pique 104 d);
  - a trend meme (SkinnyDipped 98 d).

  ASMR pours and hands-with-VO (Hint, Poppi) are cheap native variants. Coffee: Cometeer leads with **social proof plus a visible mechanism** (liquid nitrogen). Benly: coffee & tea 38 d average life; visual intrigue is the top hook. → A sensory loop plus a mechanism cut.
- **Candles / home fragrance** (n=1 video: Boy Smells 123 d; Otherland 236 d static): editorial bodies + product + one-phrase title ("Spa Smells"), 20 s, music. Benly home: **product shot (66) and UGC (62) beat lifestyle (30)**. → Keep the product big; mood alone underperforms in home.
- **Watches** (n=3): DW 137 d (8 s editorial + title), Monta 104 d (21 s gloved-hands demo + challenge question). Benly watches: 48 d average life (longest), lifestyle/editorial dominant. → **A short editorial plus a mechanism demo**, both faceless.
- **Jewelry** (n=4): Brilliant Earth render (268 d, silent, 17 s single shot) and wrist macro + iMessage (210 d, 10 s); Charlotte Chesnais 3 s hand editorial (60 d). → Our strongest evidence that **faceless, aesthetic, even CGI-looking** product films survive; add a conversational text layer for the DR cut.
- **Sneakers / shoes** (n=6). Faceless proof (Cobbler Union craft 212 d, Kuru reviews 377 d) and objection-flip UGC (Vessi 86 d). The pure-aesthetic CGI piece (Salomon, 6 s, 16:9) ran only 24 d. → For DR, aesthetic needs a proof layer.
- **Audio** (n=1): Master & Dynamic 153 d, a **hands-only ASMR care tutorial**, no VO. → "How-to" content is a premium-friendly faceless format (Ipsos: how-to/unbox = 1.5× behaviour change).
- **Bags / leather / travel** (n=3): Bellroy 183 d (problem → solution stop-motion, text-led), Calpak 93 d (VO story), Demellier 60 d (editorial).

---

## 4. Where the data contradicts our current rules

| Our rule (file) | What the data says | Verdict |
|---|---|---|
| **"Aesthetic, slow, negative space, one line" for premium** (01 §4, 02) | Aesthetic long runners exist in every premium hard-goods niche (jewelry, watches, candles, skincare). But **all of them put the product in frame 1 and a claim, number, question or named moment in text**, not one closing line. Benly home: lifestyle-only scored 30 vs product shot 66. | **Amend:** aesthetic ≠ mood. Aesthetic + product-first + persistent claim text. |
| **"No talking heads"** (client style; 15 gate 2 kills talking-head concepts) | In fashion/accessories/home, faceless is the **norm** (12 % and 0 % talking heads). In **beauty (63 %), makeup and functional food, the long runners are mostly experts, founders or creators talking**. Speech appears in 49 % of long runners; 5 of 35 used **VO over faceless visuals**. | **Keep for luxury hard goods. For skincare/bev, add VO (no face) and an "authority line" in text.** We give up the best-evidenced beauty format, so expect lower hit rates there `[inf]`. |
| **15–25 s length** (01 §3, 15 beat sheet) | Long-runner median 21 s, but bimodal: 9/35 ≤15 s (editorial, loops, offers), 13/35 15–30 s, **13/35 >30 s** (all speech-led explainers). Short editorial (6–15 s) fits faceless aesthetic; 30–90 s works only with VO/dialogue carrying information. | **Keep 15–25 s as the hero.** Always add a **6–10 s loop**. A 30–45 s version only when there is a VO mechanism story. |
| "Brand by 3 s; logo legible by 3 s" (01 §5) | System1: **logo overlays reduce** awareness lift; **logo in context** (on the pack in shot) +182 %; sonic asset in 2 s +191 %. Our winners brand via the pack in frame 1, and the logo card comes only at the end. | **Amend:** brand = pack in hand/frame by 1 s + sonic cue; no floating logo bug. |
| "One emotional peak; slower pace for premium" (01 §4) | Long runners cut faster than short ones (median 0.41 vs 0.12 detected shots/s); single takes only in UGC talk. Ipsos: *unique* visuals beat brand time on screen. | Keep the peak; cut every 1.5–3 s even in aesthetic; prioritise a **visually ownable** look. |
| "Low-fi UGC can erode luxury" (03 §14) | Benly fashion: UGC effectiveness 73 vs lifestyle 66; Motion: UGC 7.6 % vs high production 7.0 %. Premium brands run creator content heavily (La Mer, Summer Fridays, Henry Rose). But those creator ads ran *shorter* in our sample (21–37 d). | Neutral. Native ≠ ugly. The client's style is defensible; add native *layers* (text bubbles, POV captions). |
| "Offer only in the last 3 s" (01 §1) | Offer-first works for conversion (Motion: sale 11.4 %, offer-first 8.7 %; Winc, Sarah Flint offer UIs ran 46–99 d) but under-indexes in long-runner tags (sale 5.1 vs 9.1 %); offer ads are short-lived by design. | Keep for brand cuts. Make one **offer-first static/loop** per campaign when the client has an offer. |
| Hook = "sensory moment, mystery, beauty" (01 §4) | Benly: visual intrigue leads fashion (58.6 %) and home; **bold statement leads beauty (31.7 %)**. Brandmov long runners over-index **mechanism/feature, "the secret", tips, "doing it wrong"**. | Pair a sensory first frame **with** a bold or mechanism line (Motion's "two triggers"). |

---

## 5. What the client's style (clean, aesthetic, no talking faces) should add to sell harder

Each item is seen in ≥2 long runners or backed by a large study.

1. **Product in frame within 1 s, big** (83 % of long runners by 2 s; TikTok product on screen +65 % brand affinity, per 03). No atmospheric establishing shot first.
2. **A persistent proof line on screen:** a number, ingredient, process or test ("80 % saw pores minimized", "Cold-pressed at 4 °C", "Tool-less. Seamless."). Kora ran 292 d on one line + one stat. Keep it as a *design element* in the brand typeface, inside the safe zone.
3. **A question or challenge hook in text** ("Can your clasp do this?", "Neat?"). Make it two triggers: a sensory frame + a curiosity/contrarian line.
4. **Hands as the human.** Hands give scale, touch and use with no face, lip-sync or uncanny-face risk. Gloves, wrists and top-down all worked. TikTok: small faces (<20 % of frame) also beat big faces (+31 % consideration) if a person is needed.
5. **VO without a face** for beauty and food. It recovers most of the explainer power of talking heads (HexClad 327 d, Cobbler Union 212 d, Calpak 93 d). Meta: speech + music = 2.1× intent (03). Use ElevenLabs (13) with a real-sounding, not announcer, voice.
6. **A visible mechanism/craft beat** (process macro, before/after slider, texture swatch). This is how Cobbler, Cometeer, Tatcha and Augustinus Bader justify price.
7. **One native layer** for the DR cut: iMessage bubbles, a cart/offer UI, review cards, or a "POV:" caption. It costs nothing in post and over-indexes (Meta 2.5×, Motion "unconventional text placement" 9.6 %).
8. **Sonic logo in the first 2 s + logo in context** (on the pack) rather than an overlay (System1 +191 % / +182 %).
9. **An ownable visual signature** (Ipsos 1.4–1.5×): a recurring colour field, prop or camera move. The surreal "AI-able" look is fine *if* it is the brand's, but pure surreal with no proof ran shortest (Salomon 24 d) `[inf]`.
10. **A how-to / ritual / care format** (M&D 153 d, Dermalogica routine 103 d; Ipsos how-to/unbox 1.5×). It is faceless-friendly and natural for AI B-roll.

**Where the client style is weakest (be honest with them):** makeup, actives skincare with efficacy claims, and functional food. Winners there are people explaining results. If the client sells in these niches, propose **VO + hands + text**, and test it against one creator/expert cut sourced from a real person (never an AI human posing as a customer: FTC rule, 01 §3).

---

## 6. Recommended variant strategy per deliverable

Base unit: **one locked body, 3 hooks, 3 lengths, 2 ratios** (Andromeda needs *different concepts*; this is the iteration layer on each concept, per 03 §16).

### 6.1 Hero film (brand / awareness; Reels, TikTok, Shorts)
- **Lengths:** 20 s hero; **8 s loop cut** (product-first, title text, sonic logo; the DW/Dossier/Pique-loop pattern); 6 s bumper for YouTube.
- **Hooks (swap the first 2–3 s only):**
  - H1 sensory product macro + named-moment text ("The summer I wore…");
  - H2 mechanism/claim text over texture ("48-hour cold infusion");
  - H3 question/challenge ("Can your [X] do this?").
- **Ratios:** 9:16 master. 4:5 crop for Feed (keep the product centre-safe). 1:1 only if the client buys Feed-heavy; 3/35 long runners were square.

### 6.2 Performance/DR cut (same assets)
- **Lengths:** 15 s and **30 s VO-mechanism** version (the >30 s long runners were all speech-led).
- **Hooks:**
  - H1 contrarian/myth line ("Most [category] is just…");
  - H2 benefit-stack listicle text (3 benefits, 1 per 2 s);
  - H3 native-UI layer (iMessage, cart, review cards).
- Add a price or offer end card only if real. Add an **offer-first 6 s** variant when there's a promo; expect a short life.
- **Ratios:** 9:16 + 4:5.

### 6.3 Static/loop companions (cheap, high hit-rate per Motion: text-only 11.6 %, product image + text 8.8 %)
- 3 stills from the hero (product + one-line claim) and 1 animated 4–6 s loop per concept. Use the hero-stills pipeline (17).

### 6.4 Per-niche emphasis
| Niche | Hero length | Must-have layer | Best extra variant |
|---|---|---|---|
| Fragrance | 10–15 s | named moment/mood line + bottle in hand at 0 s | 6 s loop; refresh hooks every ~4 weeks |
| Skincare | 15–20 s | numeric/ingredient claim + texture macro | 30 s VO "how it works" |
| Beverage / coffee | 8–15 s | pour/condensation ASMR + one mechanism line | trend-native loop; VO cost-per-cup cut |
| Candles | 15–20 s | big product + scent-note title | 6 s match-strike loop |
| Watches / jewelry | 8–15 s | hand/wrist macro + editorial title | mechanism demo (clasp, setting); iMessage gifting cut |
| Sneakers | 15 s | craft or stress-test proof | objection-flip text cut ("think waterproof looks ugly?") |
| Audio | 15–25 s | hands-on detail / care how-to | ANC sound-design cut with VO |

### 6.5 Changes to propose for 01/03/15 (not applied here)
- Gate 5 (01): "Hook in 0–2 s" → **"product or product-in-use in frame by 1 s, plus a text line with a claim, question or named moment."**
- Gate 6: replace "logo legible by 3 s" with **"pack/logo in context by 1 s; sonic cue by 2 s; no floating logo bug."**
- 15 Stage 2 kill rule: replace "needs talking heads" with **"needs a talking AI human."** Allow VO-over-hands and real-creator inserts.
- 15 rubric: add **"proof line present (number, ingredient, process)"** to criterion 6.
- Deliverable spec: every concept ships **20 s + 8 s loop + (DR) 30 s VO** × 3 hooks × 9:16/4:5.

---

## 7. Confidence and next steps
- **High confidence:** product-first opening; text overlay carrying the message; faceless formats fit premium hard goods; early in-context branding.
- **Medium:** length bands, beauty needing voice, native-UI layers. Our n is 35 long runners, and Benly scores are longevity-based.
- **Low:** per-niche fragrance, coffee and candle patterns (n = 1–5 videos each).
- **To close the gaps** `[inf]`:
  1. Get a Motion workspace (the Inspo tools need one) to pull fragrance and coffee brands' full ad sets.
  2. Open TikTok Creative Center Top Ads in a real browser session and code 20 ads per industry by hand.
  3. Log our own live hook/hold rates per variant (15 §3.3) to replace proxies with KPIs.
