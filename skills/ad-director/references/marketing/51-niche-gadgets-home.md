# 51 — Niche deep-dive: consumer gadgets, audio, home goods and furniture

Research brief, 2026-10-09. No generation money was spent. Nobody was contacted.

**What this adds.** Doc `11-niche-tech-home.md` already covers the visual grammar of tech/audio, candles/home, kitchen, fitness and pets: shot types, light, the ANC "noise→silence" cut, style headers, the ban list and the "screens simulated" rule. This doc does not repeat that. It adds:
- teardowns of 18 real gadget, audio, home and furniture TikToks that we downloaded and measured, plus metadata for 10 more;
- conversion data for the niche: Benly Q1 2026 Home & Living sub-industries (furniture, home decor, bedding), electronics CPA, returns data, brand ad-mix snapshots;
- a realism-pitfall table mapped to doc 43's model rules, with the niche-only traps: **scale and colour drift (the top two furniture return reasons)**, cable topology, small-object hands, cushion physics, screens and LEDs;
- the legal rules this niche has and others don't: the FTC demonstration rule plus NAD's 2026 "a disclosure cannot cure the visual" decision, FCC pre-authorization marketing, EPA NRR on earplugs, IP ratings, STURDY Act tip-over, Made in USA, Apple/Bluetooth marks;
- a buyer profile and 20 brand types;
- 8 ready concepts with shot lists, physics checks, audio maps and costs.

**Tags.**
- `[measured]`: we downloaded the file and measured it with ffmpeg (scene cuts at threshold 0.30, audio RMS in 0.5 s windows, 2 fps frame tiles that we looked at).
- `[unverified]`: no primary source found.
- `[inf]`: our own inference.
- `[vendor]`: the number comes from a company that sells the thing being measured.

**Method and limits.**
- **TikTok:** downloads worked. We pulled 18 public TikToks to `scratchpad/niche/gadgets/` (outside the repo; no media committed). Profile listing still fails in yt-dlp (JSON error), so every URL came from a web search restricted to tiktok.com.
- **View counts:** yt-dlp metadata snapshot of 2026-10-09. **Like rate** = likes ÷ views.
- **Paid vs organic:** as in doc 49, a big view count with a like rate under ~1% is the paid-distribution signature (Spark Ads, whitelisting, boosting) `[inf]`. A flag, not a fact.
- **Date window:** 13 of 18 measured posts are from the last two years (Oct 2024 – Oct 2026) or the Nov 2023 Stanley moment that still defines the category. Four 2022 posts are kept as long-running references and marked.
- **Motion Creative Analytics MCP:** skipped (no workspace, doc 45 §0).
- **Purchase data:** no measured post publishes CPA. Purchase-side evidence is from earnings calls (Lovesac), vendor case studies (Stanley via CreatorIQ, Loop via Bigblue) and Benly's longevity index (a proxy, doc 45 §0).
- **Gap:** Benly has no consumer-electronics or audio category. For gadgets we use Benly "E-commerce & Retail" (which includes Electronics Retail) and Triple Whale's electronics CPA `[unverified]`.

---

## 0. The 8 findings that matter most

1. **The biggest thing ever to happen in this niche on TikTok was an unplanned torture test.** A burnt-out car, the tumbler still in the cupholder, and the **ice rattle you can hear** when she shakes it: 14.8 s, one take, **98.6M views, 9.4% like rate** (G01) `[measured]`. Stanley's CEO answered within 24 h and offered to replace the car. CreatorIQ credits November 2023 with $7.0M EMV and 251.5M impressions `[vendor]`. Ridge's *staged* parody durability test (hammer, toy cable car, freezer) earned **7.3K** (G17). **In gadgets and drinkware, a real-stakes proof beats everything, and the proof is often a sound.** AI can never *be* that proof, but it can stage a comedic version **only if the claim is literally true and labelled as a dramatization** (§4).
2. **Furniture winners open on the finished room, not on the box.** Both creator furniture hits put the payoff in second 1: three dogs on a 20-seat Lovesac sectional (G04, 2.0M, **11.8%**), a blanket flung over a new Cozey sectional (G10, 663K, 0.43% = paid signature). Both then flash back to the stack of boxes. The brands' own "tool-free assembly ASMR" posts that open on a box sat at **2.9K–37K** (G15, G16, Cozey Atmosphere) `[measured]`. **Assembly is the proof, not the hook.**
3. **Gadgets sell hands-only, with no face.** The paid-signature gadget ads are all hands on a product: Ember's unboxing on a stone table (204K at **0.12%**), Shokz's flex-and-twist demo with feature supers (423K at 0.70%), Ekster's top-down "crispy unboxing" (**5.1M** at 2.2%, 2022) `[measured]`. That is the **cheapest grammar for VXO to own** (no lip-sync, no AI faces, and the OII finding that faces make AI ads read as AI, doc 45 D31) **but the weakest for AI**, because small-object hands are where models fail (§3). The fix is a hybrid: real hands insert from the client, AI for the world and the gag.
4. **On Meta, the product shot is the most effective asset in every home sub-industry.** Benly Q1 2026 effectiveness index `[vendor]`:
   - Home & Living overall: **Product Shot 66**, UGC 62, Branded/Studio 36, Lifestyle 30, Graphic Design 30.
   - Furniture: Product Shot 63, UGC 58, Lifestyle 56, Studio 55. **Image 70% of furniture ads, video only 30%.** Demonstration hooks are 0.3% of creatives but survive **1.8×** longer.
   - Home Decor: Product Shot 63, UGC 56, Lifestyle 36, **Studio 27** (the worst).
   - Bedding & Bath: **Studio 65**, Product Shot 64, Lifestyle 54.
   - E-commerce & Retail (includes electronics retail): Product Shot 69, Studio 57.

   A VXO film here must keep **the product as the hero of most frames**. Moody lifestyle-only films are the weakest thing we can sell in home decor.
5. **Furniture creatives live longer than any other home creative, so they justify a bigger film.** Average lifespan: furniture **56 d**, kitchen 49 d, home decor 41 d, bedding 38 d, smart home 29 d, appliances 17 d `[vendor]`. A furniture film is a Premiere ($2,500) one-off. Gadgets and small home goods refresh about monthly (Season, $3,500/mo).
6. **The #1 business risk of AI in furniture is returns, not taste.** Online furniture returns run ~22.7% (vs 19.3% all-category), and the drivers are **size/space mismatch ~58% and colour/material gap ~44%** (multi-select) `[vendor] [unverified]`, at **$55–108 per large return** `[vendor]`. A model that grows a sofa 10% or warms a "forest green" to olive turns VXO's film into a returns machine. **Scale and colour lock are QA gates, not polish** (§3, §7).
7. **The legal rule that bites this niche is "the picture is the claim".** In *Dyson v. Dreame* (NAD, decided 2026-08-07) NAD held that imagery of longer hair contradicted a "dries shoulder-length hair in 2 minutes" claim and that **"a disclosure cannot contradict or be used to cure an unsupported message."** Google unlisted its Gemini demo video after NAD found "sequences shortened" insufficient. For VXO: an AI scene that *shows* faster assembly, bigger sound, more silence, more battery or a tougher product than the real one is a false demonstration, **and an "AI-generated" or "dramatization" label does not fix it** (§4).
8. **The format that compounds is a character with a running joke, not a polished spot.** "Smokeless Steve" for Solo Stove, a creator skit with the product bag in frame 1 and a recurring character ("Every person with a smokeless fire pit: Part 2"): **2.2M at 5.7%** (G03). simplehuman's sensor can scaled through creator gags ("nothing needs to be ugly", the hands-free lid opening on a wave): 505K and 9.6M (G18, G02). The polished celebrity films (Nothing × V, 1.4M; Nothing × Charli XCX, 130K) live on borrowed fame. **VXO's Otto/Vee deadpan register is the right tool; the joke must come from the product's real behaviour.**

---

## 1. Teardowns: 18 measured posts plus 10 metadata-only

`[measured]` = downloaded. Cut rate = shots ÷ duration. Hook = what is on screen and in the audio during second 1.

### 1.1 Measured (TikTok)

| # | Post | Date · views · like rate | Length · shots · shots/s | Second 1 (hook) | Turn / punchline | Sound | CTA | Why it sold |
|---|---|---|---|---|---|---|---|---|
| G01 | **Stanley car fire, @danimarielettering** ([link](https://www.tiktok.com/@danimarielettering/video/7301724587488759070)) | 2023-11-15 · **98.6M** · **9.4%** | 14.8 s · 1 take · 0.07 | Phone walk-up to a gutted, burnt car interior; the tumbler is a small object in the cupholder already in frame | She lifts the cup out of the wreck and shakes it: **ice still rattles** | Handheld voice and handling, RMS −23 to −38 dB; the ice rattle is the climax | None (organic). The brand's CEO duet was the CTA | **Accidental torture test with real stakes.** One take = credible. The proof is a *sound*. Not reproducible by AI as proof; reproducible as a format (§6 C5) |
| G02 | **simplehuman sensor can unboxing, @margiesosaa** ([link](https://www.tiktok.com/@margiesosaa/video/7354891422014655787)) | 2024-04-06 · **9.6M** · 2.4% | 41.6 s · 18 · 0.43 | **End-first:** the finished matte-black can installed in a white kitchen, then the box | Hands-only peel of the protective film; the wave-to-open lid; the bag-dispenser pull | ASMR, no music, RMS −40 to −64 dB; tape-tear peaks at −22 dB | "Which one do you like better?" (comment bait) | Satisfying film peel on a premium object + a question that drives comments. Organic |
| G03 | **Solo Stove "Smokeless Steve", @mattslyon** ([link](https://www.tiktok.com/@mattslyon/video/7301760492765236523)) | 2023-11-15 · **2.2M** · **5.7%** | 52.5 s · 5 · 0.10 | A character in a backyard already swinging the Solo Stove carry bag, super "Every person with a smokeless fire pit: Part 2" | He treats the fire pit like a status symbol (the series' running gag) | Voice skit, −28 to −40 dB | #ad; product visible from frame 1 | **Paid creator character series** (part 2 = the format already worked). Product is a prop in every shot; the joke is the owner's pride |
| G04 | **Lovesac Sactionals, @alexwarren** ([link](https://www.tiktok.com/@alexwaarren/video/7301599086304627999)) | 2023-11-15 · **2.0M** · **11.8%** | 31.3 s · 15 · 0.48 | **End-first:** selfie, three dogs on a giant grey sectional | Flashback to a hallway stacked with Home-Depot-sized boxes; friends build it | Selfie voice, −20 to −37 dB | #LovesacStealthTech tag | Payoff first, process second. Dogs = "it survives real life". Creator fame helps |
| G05 | **Ember Mug 2 "lukewarm? never heard of her"** (brand) ([link](https://www.tiktok.com/@ember/video/7561864696484072759)) | 2025-10-16 · 204.7K · **0.12%** (paid) | 16.1 s · 8 · 0.50 | Screen of the Ember website on a laptop, UGC-style super "Finally got my hands on the mug that keeps your coffee hot" | Hands-only unboxing on a sunlit stone table; mug lifted off its coaster | **Music bed, flat −15 to −17 dB, a 4 s loop** (RMS pattern repeats every 4 s); no VO | Wide lifestyle end frame: sofa, wood table, mug | **The paid gadget template:** native-UGC text wrapper → premium hands-only unboxing → lifestyle wide. 0.12% likes = bought reach |
| G06 | **Shokz OpenRun Pro 2** (brand) ([link](https://www.tiktok.com/@shokzusa/video/7653429338146098446)) | 2026-06-21 · 423K · 0.70% (paid) | 18.3 s · 1 take · 0.05 | Hands fanning three colourways at the lens | Hands twist and flex the band (durability without saying it); feature supers: "Secure and comfortable fit", "DualPitch", "12-hour battery life", "Open-ear design" | Music only, −20 to −22 dB | Feature supers; sale in caption | **One-take hands demo + four supers.** The flex is the proof. Note "up to"-free battery claim in the super `[inf]` risk (§4) |
| G07 | **Nothing Headphone (1) Pro × V** (brand) ([link](https://www.tiktok.com/@nothing/video/7690732578336197891)) | 2026-09-28 · 1.4M · 33% | 37.2 s · ~6 (dark dissolves under-detected) | Dim BTS: a film crew in silhouette, waiting | V puts the headphones on, presses a button on the cup, the set disappears; he dances alone | Room tone −30 to −46 dB, then music up to −21 dB at 15 s | None | Celebrity fandom (33% likes). The **BTS-as-wrapper** frame is borrowable; the reach is not |
| G08 | **Nothing Headphone (a) × Charli XCX battery test** (brand) ([link](https://www.tiktok.com/@nothing/video/7638950731797597473)) | 2026-05-12 · 130.5K · 4.7% | 60 s · ~20 (glitch transitions inflate count) | Tiny figure in a white void, **9.5 s of near-silence** (−39 dB) | A running timecode counter (00:00 → 11:18:16…) as the battery proof; paint and mess build up around her | Silence, then music at −8 to −14 dB (the loudest in the set) | None | **Proof as a counter** (timecode = battery). But a 9.5 s silent, distant opening cost reach even with a star `[inf]` |
| G09 | **Ridge "What kind of wallet do you have?"** (brand, 2022 reference) ([link](https://www.tiktok.com/@ridge/video/7123379699450973486)) | 2022-07-23 · 1.0M · 2.9% | 27.2 s · 7 · 0.26 | Two guys in a mall, mic out, question super | The interviewee's bulky wallet vs. the Ridge they hand him; unboxing on the spot | Lav-mic voice, −10 to −14 dB (hot) | Gift = implied CTA | **Man-on-the-street + gift.** Pre-2023, but Ridge kept this format alive for years |
| G10 | **Cozey sectional, @belowtheblonde** (2022 reference) ([link](https://www.tiktok.com/@belowtheblonde/video/7162908257235913989)) | 2022-11-06 · 663.5K · **0.43%** (paid/whitelisted) | 31.1 s · 14 · 0.45 | **End-first:** she flings a cable-knit blanket over the finished sectional, dog jumps on | Hard cut back to five Cozey boxes; building montage | Music + VO, −15 to −27 dB | Caption: delivery in a week, tool-free, washable covers | The whitelisted-creator template for furniture: payoff → boxes → build → payoff |
| G11 | **Loop Dream "You might be wearing your Loop Dream earplugs incorrectly"** (brand) ([link](https://www.tiktok.com/@loopearplugs/video/7457969836098997526)) | 2025-01-09 · 149K · 1.5% | 29.9 s · 6 · 0.20 | Red title card with the correction line, then a woman in bed: "I'm sorry to break it to you" | "Press for 5 seconds": a how-to with hands | Quiet voice, −38 to −50 dB | Implicit | **Correction hook** ("you're doing it wrong") for owners and prospects at once. Loop spent ~€1.5M/month on ads with heavy A/B testing `[vendor]` ([Bigblue](https://www.bigblue.co/it/blog/loop-earplugs-from-eu0-to-eu42m-targeting-ads-and-community)) |
| G12 | **Ekster "crispy unboxing"** (brand, 2022 reference) ([link](https://www.tiktok.com/@eksterwallets/video/7135782623074438406)) | 2022-08-25 · **5.1M** · 2.2% | 15.6 s · 4 · 0.26 | Top-down on oak, a hand slaps the boxed wallet into frame; shrink-wrap crackle at −21 dB | Box → tissue → the wallet; cards fan out | ASMR crinkle −29 to −45 dB | "Get yours today at ekster.com!" super | **15 s, top-down, hands-only, one sound (the crinkle).** The cheapest gadget format on record |
| G13 | **Ridge "mystery wallet", @gabbyygonz** ([link](https://www.tiktok.com/@gabbyygonz/video/7371952685400001834)) | 2024-05-22 · 495K · 1.4% | 38.3 s · 4 · 0.10 | Creator mid-rant holding a wallet, super "Viral Ridge Wallet" | "I wish I was making this up": the mystery box gave her a men's wallet | Voice −21 to −34 dB | TikTok Shop tag | **Complaint as hook** (TikTok Shop mystery SKU). Shows the risk side: the brand doesn't control the story |
| G14 | **AI "Gorilla Couch", @cosmicdealheather** ([link](https://www.tiktok.com/@cosmicdealheather/video/7407486064761343262)) | 2024-08-26 · **2.2M** · **9.5%** | 69.5 s · 9 · 0.13 | Green-screen over an Amazon listing of an AI-rendered gorilla-shaped sofa: "Who will be the first to buy the 'grouch'?" | The AI image became a real factory product; reviewers found the real one far worse than the render; scam listings used the AI images ([My Modern Met](https://mymodernmet.com/ai-gorilla-sofas/)) | Voice | Listing | **AI furniture imagery drives curiosity *and* an expectation gap.** The cautionary tale for finding 6 |
| G15 | **Burrow "15 minutes to put this sofa together"** (brand, control) ([link](https://www.tiktok.com/@burrow/video/7185572000822316330)) | 2023-01-06 · 37.3K · 0.23% | 37.3 s · 10 · 0.27 | Flat-lit office, sofa parts on the floor, super "This is our Nomad Loveseat" | Two staff assemble it, latch close-ups, step supers | Music only, flat −15 to −17 dB | None | **Control:** a true, useful proof with no hook. Opens on parts, not the payoff |
| G16 | **Cozey "Gaia Assembly ASMR"** (brand, control) ([link](https://www.tiktok.com/@cozey/video/7493169480751680823)) | 2025-04-14 · 19.1K · 0.50% | 13.5 s · 10 · 0.74 | A white seat base already mid-assembly, no person | Cover zipped on, cushions dropped in | ASMR −30 to −50 dB | None | **Control:** the same brand's creator reveal (G10) got 35× the reach. ASMR assembly without a payoff frame doesn't travel |
| G17 | **Ridge "A very official durability test"** (brand, control) ([link](https://www.tiktok.com/@ridge/video/7226433264284699946)) | 2023-04-26 · 7.3K · 1.3% | 26.9 s · 19 · 0.71 | Staffer waves, holding the wallet: "we get a lot of questions on durability" | Tongue-in-cheek tests: hammer tap, a toy cable car "the sheer weight of vehicles", tossed out a window, a freezer | Voice −25 to −40 dB | None | **Control: a fake torture test.** Wink-wink parody of G01's format without stakes or a gag that pays off |
| G18 | **simplehuman "Nothing needs to be ugly", @thejosephabell** ([link](https://www.tiktok.com/@thejosephabell/video/7247656899238464814)) | 2023-06-22 · 505K · 0.95% (likely paid) | 24.7 s · 14 · 0.57 | Locked-off wide of a kitchen; he walks in and grabs an old white can, caption "One of my best realizations about home design is this" | Unbox, install, then he waves at the new can from further and further away while it opens on its own | Voice + music −15 to −25 dB | None | **Philosophy line + one repeatable physical gag** (the wave). Locked-off tripod camera, like a VXO deadpan tableau |

### 1.2 Metadata only (not downloaded)

| Post | Date · views · like rate | Note |
|---|---|---|
| Stanley follow-up "Thank you so much @Stanley 1913" ([link](https://www.tiktok.com/@danimarielettering/video/7303282746766642478)) | 2023-11-19 · 1.9M · 6.9% | The sequel: 1/50 of G01's reach. The moment was the proof, not the person |
| Ember "study groove" (brand) ([link](https://www.tiktok.com/@ember/video/7423510873102306606)) | 2024-10-08 · 1.4K · 2.0% | Same brand as G05 without paid push or the UGC wrapper |
| James Hoffmann on the Ember mug ([link](https://www.tiktok.com/@jameshoffmanncoffee/video/7187351026809277701)) | 2023-01-11 · 104.5K · 3.7% | A 6.6 min expert review; "a bit ridiculous… just ridiculous enough for me to like it". The trust layer gadget buyers search for |
| Shokz "Open Ear Headphones??" (brand) ([link](https://www.tiktok.com/@shokzusa/video/7399968155977895214)) | 2024-08-06 · 12K · 0.31% | A question hook without a demo. Compare G06 at 35× |
| Burrow Nomad "internet's favorite sofa" (brand) ([link](https://www.tiktok.com/@burrow/video/7398210723438021930)) | 2024-08-01 · 1.7K | Brand claim, no proof, no payoff |
| Cozey Atmosphere tool-free assembly (brand) ([link](https://www.tiktok.com/@cozey/video/7558153520877292808)) | 2025-10-06 · 2.9K · 0.83% | Same as G16 |
| Lovesac × @dylanfauver ([link](https://www.tiktok.com/@dylanfauver/video/7237253448746552622)) | 2023-05-25 · 450K · 11.5% | Second Lovesac creator build: the format repeats |
| Loop "Keep the sound quality? Grab Loop Experience" (brand) ([link](https://www.tiktok.com/@loopearplugs/video/7363766247340756256)) | 2024-04-30 · 66.8K · 1.3% | Concert use case, Eras-tour season |
| Nothing Headphone (1) by Jordan Hemingway (brand) ([link](https://www.tiktok.com/@nothing/video/7529485503582801174)) | 2025-07-22 · 108K · 3.4% | Pure art film, 25 s: 1/13 of the V film |
| BrüMate Era leak-proof creator ad ([link](https://www.tiktok.com/@theshannykate/video/7290949805717802286)) | 2023-10-17 · 30.7K · 0.62% | Leak-proof claim told, not shown; low reach |

### 1.3 What the measured set says `[measured]`

- **Second 1 holds the payoff or the proof, already in frame.** Burnt car with the cup visible (G01), finished can in the kitchen (G02), dogs on the sectional (G04), blanket over the sofa (G10), three colourways at the lens (G06). The flops open on parts, a box, or a staffer introducing himself (G15, G16, G17).
- **Cut rate is format-driven and low.** Proof one-takes 0.05–0.07 shots/s (G01, G06). Skits 0.10 (G03, G13). Unboxings and builds 0.26–0.5. The fastest cuts (0.71–0.74) are the two weakest brand posts (G16, G17). As in docs 48 and 49, **speed is not the lever.**
- **The product appears in frame 1 in 13 of 18 posts.** The five that delay it are BTS/art films (G07, G08), the man-on-the-street (G09), and two controls.
- **No face is needed.** 5 of 18 are hands-only or nearly so (G02, G05, G06, G12, G16). Both paid-signature gadget posts (G05, G06) are in this group.
- **Audio:** product sounds (ice rattle, shrink-wrap crinkle, film peel, lid whirr) carry the organic winners. Paid gadget posts sit on a flat music bed at −15 to −22 dB with feature supers instead of VO. Voice is reserved for skits and creators.
- **Proof devices that recur:** a torture test (G01), a counter or timecode (G08), a flex/twist (G06), "ice still there" (G01), a hands-free gesture (G18), a dog on the sofa (G04, G10; doc 11 Our Place too). Each is a **visible, physical event**, never a stat.
- **Brand-made vs creator-made:** the Cozey creator reveal (G10, 663K) out-reached Cozey's own assembly posts by 35× (G16) to 230× (Atmosphere, 2.9K); Lovesac's creator builds (2.0M, 450K) dwarf every brand-made sofa post we found (Burrow 37K, 1.7K). Brands buy that reach back as whitelisted ads (G10's 0.43%). A VXO film should be **cut to sit inside a creator-style wrapper** (§2.2).

---

## 2. What actually converts in this niche (data)

| # | Finding | Number | Source | Status |
|---|---|---|---|---|
| N1 | Home & Living creative effectiveness (Meta): Product Shot / UGC / Studio / Lifestyle / Graphic | **66 / 62 / 36 / 30 / 30** | [Benly Home & Living Q1 2026](https://benly.ai/benchmarks/q1-2026/home-living), 18.6K creatives, 136 brands | `[vendor]` longevity proxy |
| N2 | Furniture: Product Shot / UGC / Lifestyle / Studio / Graphic; image share | **63 / 58 / 56 / 55 / 35**; **70% image** | [Benly Furniture](https://benly.ai/benchmarks/q1-2026/home-living/furniture), 2.4K creatives | `[vendor]` |
| N3 | Furniture video hooks: Visual Intrigue 51% (39 d), Pattern Interrupt 26.6% (40 d), Bold Statement 12.2%; **Demonstration 0.3% but 1.8× survival** | — | same | `[vendor]` |
| N4 | Home Decor: Product Shot 63, UGC 56, Lifestyle 36, **Studio 27**, Graphic 22. Before/After hooks 0.1% but 2.2× survival | — | [Benly Home Decor](https://benly.ai/benchmarks/q1-2026/home-living/home-decor) | `[vendor]` |
| N5 | Bedding & Bath: **Studio 65**, Product Shot 64, Lifestyle 54, UGC 45. Top hook Bold Statement 31%; Pain Point 16.5% | — | [Benly Bedding & Bath](https://benly.ai/benchmarks/q1-2026/home-living/bedding-bath) | `[vendor]` |
| N6 | Average lifespan: Furniture 56 d, Kitchen 49 d, Home Improvement 48 d, Home Decor 41 d, Bedding 38 d, Smart Home 29 d, Appliances 17 d. Video share: furniture 30%, appliances 63% | — | Benly Home & Living | `[vendor]` |
| N7 | E-commerce & Retail (incl. Electronics Retail): Product Shot 69, Studio 57, Lifestyle 48, UGC 48, Graphic 37; Electronics Retail avg lifespan 33 d | — | [Benly E-com & Retail](https://benly.ai/benchmarks/q1-2026/e-commerce-retail) | `[vendor]` |
| N8 | Meta median CPA: **Electronics $49.48** vs all-industry $38.17 (2025) | — | [Triple Whale](https://triplewhale.com/blog/facebook-ads-benchmarks) via search summary | `[unverified]` (page 403, doc 45 D21) |
| N9 | Motion: "Home & lifestyle: demonstration and process matter most"; unboxing is the #1 format (9.83% hit rate), demo 8.11%, cinematic b-roll 6.85% | — | doc 45 D3, D6 | Read |
| N10 | Furniture online return rate ~22.7% vs 19.3% all categories; drivers: size/space ~58%, colour/material ~44%, transit damage ~31% (multi-select); $55–108 per large return | — | [eightx](https://eightx.co/blog/average-furniture-and-home-return-rate-benchmarks) citing NRF/Happy Returns | `[vendor] [unverified]` |
| N11 | Ridge ad mix snapshot: ~290 active Meta ads, **51% image, 40% dynamic, 9% video**; weekly launches, keep winners; long-runners are split-screen size comparisons and stacked social proof | — | [Foreplay](https://www.foreplay.co/post/the-ridges-ad-auction-analysis) | `[vendor]` |
| N12 | Ridge's founder: influencer marketing was the principal revenue driver; realistic influencer rate $12–20 per 1,000 subscribers | — | [Practical Ecommerce](https://www.practicalecommerce.com/?p=1506456) | Interview |
| N13 | Lovesac moved from linear TV to a "digital-first ecosystem" of social, search, influencer and creator content; media-attributed revenue +13% in the quarter, ROAS up double digits | — | [Nasdaq, Q1 call highlights](https://www.nasdaq.com/articles/lovesac-q1-earnings-call-highlights) | Earnings call |
| N14 | Loop: ~€1.5M/month ad spend split between whitelisting and non-branded ads; A/B testing "at scale"; >3B TikTok search views | — | [Bigblue](https://www.bigblue.co/it/blog/loop-earplugs-from-eu0-to-eu42m-targeting-ads-and-community) | `[vendor]` |
| N15 | Stanley car fire: response within 24 h; Nov 2023 = $7.0M EMV, 251.5M impressions, 15.1M engagements; brand revenue ~$70M → $750M over four years (growth predates the fire) | — | [CreatorIQ](https://creatoriq.com/blog/earned-podcast-ep-111-terence-reilly-stanley-cup-quencher-viral-car-fire-tiktok-influencer-marketing-crocs), [Shorty Awards entry](https://shortyawards.com/16th/the-car-that-set-stanley-on-fire) | `[vendor]` / self-reported |
| N16 | TikTok-run furniture case (Fantastic Furniture, AU): creator content beat repurposed TV ads on CTR (+8%) and CPC (−10%); best creative +108% view-through | — | [TikTok for Business](https://ads.tiktok.com/business/en-US/inspiration/fantastic-furniture-551) | `[vendor]` (platform) |

### 2.1 What this means, by sub-niche `[inf]`

- **Furniture and large home (sofas, beds, desks, outdoor):**
  - Format: **payoff-first reveal → boxes → one assembly beat → payoff**, 20–30 s, plus a 6 s payoff-only cutdown.
  - Proof: a pet or kid on it (durability), a washable cover thrown in a machine, the doorway/stairwell fit. Show real dimensions as a super.
  - Placement: Meta Feed 4:5 and Reels; the PDP video slot (the film doubles as a returns-reducer if scale and colour are exact).
  - Since 70% of furniture ads are images, **always deliver 6–10 product-hero stills from the film's frames.** That is what the Meta account actually runs.
- **Gadgets and EDC (wallets, trackers, chargers, mugs, tumblers):**
  - Format: **15–20 s hands-only demo or unboxing** with 3–4 feature supers, or a 15 s comedic torture test that is true.
  - Proof: a counter, a flex, a drop onto a real surface, a before/after carry (split screen of pocket bulge).
  - Placement: TikTok Spark + Reels; Amazon listing video (same cut, no CTA super).
- **Audio (headphones, earbuds, earplugs, speakers):**
  - Format: **sound-first hook, then the silence or the drop as the punchline.** The ANC cut (doc 11) is the category's signature; the earplug variant is "the noise keeps happening, she doesn't hear it".
  - Proof: never "hear the difference" through a phone speaker. Show it visually (people talking silently, a lamp swinging in silence) and put the measured spec in a super.
  - 15 s master, 6 s silence-cut loop.
- **Home goods (bedding, lighting, kitchen tools, storage):**
  - Bedding is the one sub-niche where **studio/branded wins** (N5). A premium, product-forward VXO film fits.
  - Home decor is the opposite: studio is the worst (27). Use a creator-wrapper or product shot.

### 2.2 The wrapper rule (applies to every VXO film here) `[inf]`

The measured winners are native-looking. VXO's cinematic AI footage should ship in three wrappers:
1. **Clean film** (brand account, Reels/Feed).
2. **UGC-text wrapper:** first 1–1.5 s is a native element (a phone screen, a lowercase super like "finally got my hands on…", a creator-style question), then the film. This is exactly G05's paid structure.
3. **Product-shot stills pack:** 6–10 frames with a single benefit line each (N1, N2, N7).

---

## 3. AI realism pitfalls for this niche, and the fixes

Built on doc 43 §1 (model choice), §3 (references), §5 (failure table). Rule of thumb: **Kling 3.0 Pro i2v from the client's own product photo for every frame where the product must be exact; Seedance 2.5 r2v for people, rooms and gags; Cinema Studio 4.0 for the one-move hero.**

| Pitfall | What goes wrong | Fix (prompt / reference / process) |
|---|---|---|
| **Scale drift** (furniture, speakers, tumblers) | A sofa grows a seat between cuts; a speaker becomes palm-sized; doorways shrink to fit the sofa. This is the #1 return driver (N10) | Write the real dimensions in the prompt ("sofa 224 cm wide, 86 cm deep, seat height 46 cm; the woman is 168 cm and her knees reach the seat front"). Add a human or a standard object (door 203 cm, A4 sheet, 12 oz can) as a scale anchor in the same frame. Product ref first, "rigid, never resized" (doc 43 §3). QC: overlay frame vs. the client's dimension drawing |
| **Colour and material drift** | "Forest green" goes olive under warm light; boucle becomes velvet; walnut becomes oak; matte black gets gloss | Reference = the client's colour-accurate photo **plus** a flat swatch photo under 5600K. Write the material ("bouclé loops 3–4 mm, no sheen", "matte powder-coat, no reflections"). Grade the room, never the product (mask the product in post). QC against the swatch with a colour picker: ΔE < 5 `[inf]` |
| **Cushion, foam and fabric physics** | Cushions don't compress when someone sits; or they compress like water; fabric is "underwater" | PHYSICS block: "the seat cushion sinks about 5 cm under her weight and recovers slowly over 2 s; the cover creases at the front edge; no bounce". Doc 43 rule 10 |
| **Reflections** (anodised aluminium, chrome, glass, piano black, screens off) | Reflections show a crew, a ring light or a different room; or vanish | Prefer matte finishes and angles where the reflection is the room itself. Write "reflections show only this room's window, nothing else". Seedance is strong on reflections but check every frame (doc 43 §9) |
| **Screens, LEDs, app UI** | Garbled digits, animated nonsense, wrong battery percentage | Black or angled-away screens; LEDs as "three small white dots, steady" (doc 11). Comp real UI in post with "screen images simulated" |
| **Cables** | Cables appear from nowhere, pass through objects, end in no plug, or change length | Cordless framings by default. If a cable must show, script both ends and its path ("the braided USB-C cable runs from the mug coaster, behind the laptop, to a wall socket at frame right; it never moves"). Keep it static |
| **Small-object hands** (earbuds into ears, card into wallet, magnet snaps, buttons) | Fused fingers, the card passes through the wallet, a button press that doesn't depress | **Real hands insert** shot by the client on a phone for every functional hand action (G05, G06, G12 grammar). Otherwise Kling i2v with start and end stills, finger-by-finger contact (doc 43 §5) |
| **Earbuds and headphones on heads** | The earbud floats outside the ear; the headband clips through hair; cups resize | Profile or back framing, hair over the ear (doc 11); headphones as their own ref; "headband rests on top of the hair, pressing it flat; cups cover the ears fully" |
| **Assembly sequences** | Parts teleport, latches close themselves, the sofa assembles in one cut | **Never show AI assembly as proof of easy assembly** (that is a demonstration claim, §4). Show states between cuts (boxes → finished), and use the client's real assembly clip for the "how" |
| **Liquids in drinkware** | Level rises from nothing; ice melts and reforms | Doc 49 §3: no generated level changes; states between cuts; the ice rattle is a library or real SFX on a shake that happens off the rim |
| **Water and splashes** (waterproof speakers, tumblers) | Water ignores gravity, splashes freeze, objects float that would sink | Say whether the object floats (and check the real product). Write the splash crown and fall-back time ("droplets fall back within 0.6 s"). Underwater: "muffled, blue-green, particles drift". Short shots ≤3 s |
| **Sound as proof** (ANC, noise reduction, bass) | AI audio exaggerates silence or bass beyond the real product | Show silence visually (people's mouths moving, objects falling) and keep the real spec as a super. Never mix "before/after" audio presented as a measurement |
| **Text and marks** (logos, embossing, packaging) | Warped wordmarks, wrong trademarks (Bluetooth, Hi-Res, MagSafe) invented on the product | Blank product shells in generation; comp the real logo; no third-party marks generated (doc 11; §4.3) |
| **Pets on furniture** (the niche's favourite proof) | Extra legs, dog morphs into the cushion, fur merges with bouclé | One pet, close or medium, ≤3 s, clear colour contrast with the fabric; "exactly four legs"; doc 11 §5 rules |
| **Rooms that can't exist** | Ceilings 4 m high in a "small apartment"; windows that change between cuts | Location plate from Soul Cinema or a real photo, locked as a ref (doc 43 §3 "statics" trick); state ceiling height |

---

## 4. Ad policy and legal constraints

### 4.1 US law and self-regulation

- **FTC demonstrations and mock-ups.** A demonstration must show what the product really does; mock-ups are allowed only if they don't misrepresent the product's performance (FTC v. Colgate-Palmolive, 1965, the classic "sandpaper" case). For AI this means: **a generated scene of the product doing something is a demonstration.** If the real product can't do it in those conditions, the film is deceptive.
- **NAD: imagery is the claim, and labels don't fix it.**
  - *Dyson v. Dreame* (NAD Fast-Track SWIFT #7600, 2026-08-07): models with hair much longer than shoulder length contradicted a "dries shoulder-length hair in two minutes" claim. **"A disclosure cannot contradict or be used to cure an unsupported message."** ([Mondaq](https://www.mondaq.com/nad-says-a-disclosure-cant-fix-a-misleading-product-demonstration/1837024))
  - Google unlisted its Gemini demo after NAD found "sequences shortened throughout" didn't stop the video conveying capabilities the product lacked ([Kelley Drye](https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/google-unlists-gemini-video-after-nad-inquiry)).
  - Practitioners: an "AI-generated" label "doesn't give advertisers permission to show unrealistic product results" ([Advertising Week](https://advertisingweek.com/ai-is-amazing-your-ads-about-it-still-have-to-be-true/)).
  - **VXO rule:** every performance event in a film (silence, battery, waterproofing, durability, temperature, assembly time, sound) must be within the product's tested spec and conditions. "Dramatization" may be added for exaggerated *comedy* (a lamp swinging), never for the *claim* (how quiet, how long, how deep).
- **Battery, temperature and "up to" claims.** State the test conditions in the super ("up to 12 h at 50% volume", "holds 135°F up to 80 min on battery"). The visual must not exceed them (G06 shows "12-hour battery life" with no conditions on screen `[inf]` risk).
- **Water and dust (IP ratings).** IP67 means 1 m for 30 min in fresh water under IEC 60529 test conditions. Don't show the product deeper, longer, in the sea or a pool with chlorine unless tested. **Floating** must be true of the real product.
- **Earplugs and hearing protectors: EPA NRR.** Hearing protection devices sold in the US must carry the EPA Noise Reduction Rating label under 40 CFR Part 211 Subpart B ([eCFR](https://www.law.cornell.edu/cfr/text/40/part-211/subpart-B)). Loop's own sources disagree on "17 dB" vs "20 dB" by model. **Rule: only the labelled NRR (or the brand's documented SNR with its standard named) appears as a number; no visual that implies total silence** `[unverified]` for the exact advertising requirement in § 211.205.
- **FCC equipment authorization (any Bluetooth, Wi-Fi or RF gadget).** 47 CFR § 2.803 defines marketing as including "advertising for sale" and bars it before the device is authorized and labelled, except display with the notice "This device has not been authorized as required by the rules of the Federal Communications Commission…" ([Cornell LII](https://www.law.cornell.edu/cfr/text/47/2.803)). **Pre-launch and crowdfunding gadget films must check FCC status** `[inf]` for crowdfunding specifically.
- **Furniture tip-over (STURDY Act).** Clothing storage units ≥27 in, ≥30 lb, ≥3.2 cu ft made on or after 2023-09-01 must meet ASTM F2057-23 with an anti-tip device ([CPSC FAQ](https://www.cpsc.gov/FAQ/Clothing-Storage-Units)). **Never show a child climbing, pulling or hanging on a dresser or bookcase, and show the dresser against a wall** `[inf]` (consistent with CPSC's anti-tip messaging).
- **Made in USA.** Unqualified claims ("Made in USA", "American-made", "Crafted in USA") need "all or virtually all" US content; civil penalties up to **$53,088 per violation** (2025 adjustment); a March 2026 executive order pushes enforcement, and an April 2026 FTC sweep brought three actions ([Kelley Drye](https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/trump-administration-directs-federal-trade-commission-to-prioritize-made-in-usa-enforcement), [Morgan Lewis](https://www.morganlewis.com/-/media/files/publication/outside-publication/article/2026/ftc-sweep-signals-increased-made-in-usa-claim-scrutiny-law360.pdf)). Furniture and EDC brands use this claim a lot: **no flag, "USA" super or "made here" line without the client's written substantiation.**
- **Reviews and testimonials.** FTC Consumer Reviews and Testimonials Rule (16 CFR 465, effective 2024-10-21): no fake or AI-generated reviews or testimonials. A "customer" character in a VXO film never gives a verdict in words.
- **Price and sale claims.** "Was $X" needs a real former price (16 CFR 233). Lifetime-warranty lines must match the warranty (Magnuson-Moss).

### 4.2 Platform rules

| Topic | Meta | TikTok | Action for VXO |
|---|---|---|---|
| Knives, multi-tools, blades | Weapons policy (doc 45 §5.1) | Blades and knives prohibited, **except** utility knives, knife utility tools and culinary knives; 18+ targeting in Europe and Israel ([TikTok ads policy](https://ads.tiktok.com/help/article/tiktok-ads-policy-dangerous-products-or-services?lang=en)) | EDC brands with blades: show the tool closed or in a culinary/utility use; ask for pre-review |
| Fire (fire pits, heaters, torches, candles) | Allowed; unsafe use can be disapproved `[inf]` | Dangerous activities policy | Show the safe use the manual shows: on a non-flammable base, away from structures, adult supervision (doc 11 candle rule) |
| AI labels | "AI info" label; disclosure rules in doc 45 §5.3 | AIGC label required for realistic AI content | Disclose per platform. **The label does not fix a false demonstration (§4.1)** |
| Misleading / exaggerated claims | Unrealistic outcomes disapproved | "Exaggerated or misleading claims" prohibited | Same as §4.1 |
| Third-party marks | IP policy | IP policy | No Apple, AirTag, MagSafe, Bluetooth, Dolby, Hi-Res, UL marks in generated frames |

### 4.3 Trademark hygiene for gadgets `[inf]`

- "Works with Apple Find My", "Made for MagSafe" and MFi badges belong to licensing programmes; descriptive compatibility lines ("fits AirTag") are a client legal call. **Don't generate the Apple logo, an AirTag, an iPhone or a MagSafe ring in frames**; use a generic tracker disc and a generic phone, or the client's licensed photo.
- Bluetooth and Hi-Res logos (doc 11) only as post comps from the client's licensed files.

---

## 5. The buyer

### 5.1 Who signs a $1,200–3,500 film `[inf]`, with evidence

- **Under ~$10M revenue (most EDC, earplug, mug, lamp, small furniture startups):** the **founder or co-founder** signs, often the one who runs paid social. Ridge's founder talks ad targeting and influencer CPMs himself (N12). Loop's founders ran the creative testing machine (N14).
- **$10–50M (Cozey, Burrow-size, DTC audio):** a **Head of Growth / Performance** owns the budget, a **Brand or Creative Director** owns approval. Cozey's holiday spots were made in-house (LBB) ([LBB](https://lbbonline.com/news/Cozey-for-the-Holidays)), so VXO competes with the in-house team on speed and novelty.
- **Public or large (Lovesac, Solo Stove, Stanley):** an agency of record and a creator programme; a $2,500 film is a test line item, signed by a social/creative lead. Lovesac's spend is moving to creators and digital (N13).

### 5.2 What they fear (ranked) `[inf]`, with evidence

1. **Returns and "not as pictured" complaints.** Size and colour mismatch drive most furniture returns at $55–108 each (N10). The gorilla-couch saga shows how far an AI render can drift from the real product (G14).
2. **Looking fake or cheap.** AI ads lose memory activation and trust when they look AI (doc 45 D31–D33). Gadget buyers are reviewers' audiences (Hoffmann-style scrutiny, §1.2).
3. **Product fidelity:** the wrong colourway, a warped logo, an invented port or button. In electronics, an invented feature is a false claim.
4. **It won't beat UGC.** UGC scores 58–62 on furniture and home vs. lifestyle 30 (N1, N2). Founders have heard "cinematic doesn't convert".
5. **Legal:** FCC status for pre-launch gadgets, NRR for earplugs, Made in USA, IP ratings (§4).
6. **Speed and volume:** brands like Ridge launch ads weekly (N11). One film a month is not enough unless it produces many variants.

### 5.3 What proof they need

- **Their product, colour-exact, in 5 free frames**, with a side-by-side against their own PDP photo and a dimension check. This answers fears 1 and 3 before any call `[inf]`.
- **A variant pack, not a film:** 15 s master + 6 s cutdown + 3 first-frame hook swaps + 6–10 product stills (finding 4; N2 image share 70%).
- **A claims sheet** listing every on-screen number with its source (spec sheet, test report, NRR label, IP certificate). It shows we know §4.
- **One relevant reference in our portfolio** that is product-hero, not mood: a hands-only gadget demo and a payoff-first furniture reveal.
- **A test plan:** 3 hooks × 2 wrappers in week 1, kill or scale by hook rate and CPA against their baseline (doc 45 §6).

### 5.4 Twenty example brand types (no outreach)

1. Modular sofa that ships in boxes (tool-free assembly)
2. Washable-cover sofa or sectional (pets and kids)
3. Sleeper sofa / small-space convertible furniture
4. Ergonomic office chair or standing desk for home offices
5. Outdoor furniture and smokeless fire pits
6. Mattress-in-a-box or cooling bedding/sheets
7. Sunrise alarm / sleep-sound machine
8. Reusable earplugs for concerts, sleep and focus
9. Open-ear or bone-conduction sport headphones
10. Over-ear ANC headphones from a challenger audio brand
11. Waterproof portable speaker
12. Smart temperature mug or self-heating travel mug
13. Insulated tumbler / leak-proof drinkware
14. Minimalist metal wallet and tracker card (EDC)
15. MagSafe-compatible phone accessories (grips, wallets, chargers)
16. Cordless rechargeable table lamps / ambient lighting
17. Sensor trash cans and premium home-organisation tools
18. Countertop appliance with a single hero function (pizza oven, ice maker)
19. Air purifier or humidifier with a design angle
20. Robot or cordless stick vacuum from a challenger brand

---

## 6. Eight ready film concepts (invented brands)

Conventions:
- **Formats:** 9:16 master; 4:5 reframe; a 6 s cutdown; 3 first-frame hook swaps; 6–10 product stills from the film (§2.2).
- **Physics:** each concept passes doc 41 §2 and doc 44's "could a crew rig this?" read. Every camera position below names its rig.
- **Costs** are list prices from doc 43 §6 [EST]:
  - Seedance 2.5 r2v: $2.06 / $4.62 per 10 s at 480p / 720p. A 15 s scene costs $3.09 to prove at 480p and $6.93 per 720p take; we budget ×3 takes = $20.79;
  - Kling 3.0 Pro i2v, sound off: **$0.48 per 5 s insert**, budgeted ×2;
  - Cinema Studio 4.0 at 720p: $3.70 per 8 s take;
  - stills (Flare / Soul Cinema): ~$0.30 each (doc 11).
- **Real insert:** every functional hand action (earplug in, card in, button press), every assembly step and every liquid event is filmed by the client on a phone, or happens between cuts (§3).
- **Brand names** are invented. Clear them on USPTO before use.
- **Mascots:** Otto and Vee appear only in VXO's own spec films, so they are absent here. Any concept can become a VXO spec film by casting Otto as the deadpan lead (mouth never visible, so no lip-sync risk) and Vee as the one with the stopwatch.
- **No dialogue on visible lips** in any concept. VO is the locked ElevenLabs brand voice (doc 13).

### C1 · HUSHWELL (reusable sleep earplugs) — "Band Practice" (15 s)

- **Idea:** 11:40 pm. The upstairs neighbour is drumming. A woman in bed presses in her HUSHWELL plugs. Hard cut to silence. The room keeps shaking, silently, and she sleeps through all of it.
- **Hook (0–1 s):** the bedroom ceiling pendant swinging, plaster dust sifting down through a lamp beam onto a white pillow, a kick drum thumping through the ceiling. A strange image already in motion, with sound.
- **Punchline (product-caused):** the final held wide: the pendant still swinging, a framed print on the wall walks off its nail and drops onto the carpet, **in total silence**, and she doesn't stir.
- **Built on:** G11 (Loop's sleep use case), doc 11's ANC hard-mute signature, doc 44 §8 "the held last shot is the joke".

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Low angle, tripod beside the bed: the pendant swings, dust falls through the lamp beam onto the pillow | Seedance. Pendant on a 70 cm cord swings with a ~1.7 s period |
| 2 | 1.5–3 | Medium, tripod at the foot of the bed: she lies on her back, eyes wide, the duvet trembling at each kick | Face 3/4, no speech |
| 3 | 3–5 | Insert, overhead C-stand arm: her hand opens the charging case, takes a plug | **Real insert** (client) or Kling i2v from a product still; case and plug exact |
| 4 | 5–7 | Profile close, slider: fingertip presses the plug in, holds; super "press 5 s" | **Real insert** preferred (doc 43 hands rule). Hair tucked behind ear |
| 5 | 7–7.5 | Same profile: **audio hard cut** to room tone | The cut is in the audio, not the picture |
| 6 | 7.5–13 | Locked-off wide from the doorway, tripod (held): pendant swinging, the print slides off its nail and lands flat on the carpet; she sleeps | Seedance (template 7.5 adapted). Print weight 1–2 kg, falls 1.2 m, lands flat, one small bounce, stays |
| 7 | 13–15 | End card: the case on the nightstand, "HUSHWELL. NRR [label value] dB." | Real product photo; NRR from the label only |

- **Physics check:** the pendant period matches its cord (T ≈ 2π√(L/g) ≈ 1.7 s for 0.7 m). Dust falls slowly and straight in still air. The print slides, then drops; it doesn't fly. Drum vibration is plausible for a shared joist ceiling; no cracks or collapse (that would be a safety image). She is an adult; no one is hurt.
- **Audio map:**
  - 0.0 s: kick drum through the ceiling (muffled, low-passed at 200 Hz), cymbal wash faint, plaster trickle.
  - 1.5 s: duvet rustle on each kick.
  - 3.0 s: case click (real insert sound). 5.0 s: soft silicone squeak.
  - **7.0 s: hard cut to room tone (−55 dB) for the rest of the film.** No sound for the print landing.
  - 13 s: one soft two-note sonic logo. VO (dry, near-whisper): `Upstairs is still going. [pause] You're not.`
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v 15 s scene for shots 1, 2, 6 (proof $3.09 + 720p ×3 $20.79) | $23.88 |
  | Kling inserts shots 3–4 if no real insert, ×2 each | $1.90 |
  | Stills, 6 | $1.80 |
  | **Total** | **≈ $28** |
- **Claim check:** no dB number except the labelled NRR (§4.1). Silence in the film is a comedic dramatization of "she doesn't wake", not a measurement: add "Dramatization." in small type. If the plug is not rated for sleep, change the setting.

### C2 · UPSTAIR (modular sofa, ships in 5 boxes) — "The Hoist" (20 s)

- **Idea:** a fourth-floor walk-up. Two movers hoist a full-size sofa up the façade on a rope while neighbours watch. Meanwhile the new tenant next door carries five UPSTAIR boxes up the stairs, one at a time, and builds her sofa. When the movers' sofa finally reaches the window, she's lying on hers, waving.
- **Hook (0–1 s):** looking straight up the brick façade from the sidewalk: a sofa dangling on a rope, turning slowly against the sky.
- **Punchline (product-caused):** the dangling sofa arrives at window height; through the neighbouring window we see her already stretched out on the finished UPSTAIR, mug in hand. She waves at the movers.
- **Built on:** G04 and G10 (payoff-first furniture reveal), N3 (demonstration hooks survive 1.8× longer), N10 (doorway fit is the #1 return reason, turned into the joke).

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–2 | Sidewalk, wide lens tilted up, tripod: sofa on a rope turning slowly, 3 floors up | Seedance. Rope from a roof-beam pulley; a tag line held by a mover below |
| 2 | 2–4 | Long lens from across the street, tripod: two movers on the rope, sweating; neighbours on the stoop | ≤4 people, no faces in close |
| 3 | 4–6.5 | Stairwell, low angle from the landing, tripod: she carries one box up, then the next (two cuts of states) | Box dims on the side: real dims as post super |
| 4 | 6.5–9 | Her living room, locked-off wide: five boxes on the floor → (hard cut) → the sofa assembled | **States between cuts**, no AI assembly |
| 5 | 9–11 | Insert, overhead arm: a hand clicks the armrest latch home | **Real insert** from the client's assembly footage |
| 6 | 11–14 | Exterior, long lens, the movers' sofa rises into frame beside her window | Seedance; sofa rigid, slow rotation stops as the tag line pulls |
| 7 | 14–18 | Through her window from the dangling sofa's side (camera on a pole/jib from the street): she's lying on the UPSTAIR, mug in hand, gives a small wave | Held. Cushion sinks ~5 cm under her (physics) |
| 8 | 18–20 | End card: the five boxes flat-packed by the door, "UPSTAIR. Five boxes. Every staircase." | Real product photo |

- **Physics check:** hoisting is a real moving practice: rope through a pulley on a roof beam, two people hauling, one on a tag line to stop rotation; the sofa is wrapped in moving blankets, rigid, never bends. Each UPSTAIR box is carried by one person, so it must be ≤ the real box weight (state it: e.g. 18 kg; adjust to the client's spec). No one stands under the load (safety image).
- **Audio map:**
  - 0.0 s: rope creak, pulley squeal, street ambience, a pigeon.
  - 2 s: movers' grunts (no words). 4 s: stairwell footsteps, box thump on each landing.
  - 6.5 s: tape tear, then silence on the cut to the finished sofa.
  - 9 s: latch click (real). 11 s: rope creak returns.
  - 14 s: through-glass muffled street; she taps the glass once with her ring.
  - 18 s: VO: `Fits through any door. [pause] Even yours.` + sonic logo.
- **Models and cost:**

  | Item | Cost |
  |---|---|
  | Seedance 2.5 r2v, two 10 s scenes (exterior; stairwell/interior): proof 2 × $2.06 + 720p 2 × 3 × $4.62 | $31.84 |
  | Kling insert (shot 5) if no real insert ×2 | $0.95 |
  | Stills, 8 | $2.40 |
  | **Total** | **≈ $35** |
- **Claim check:** "every staircase" must be supported by the box dimensions vs. a standard US stair (36 in width); otherwise use "most staircases". Sofa colour and size from the client's spec (§3 scale and colour gates).

### C3 · NULLA (ANC over-ear headphones) — "Leaf Season" (15 s)

- **Idea:** a man works at a desk by an open ground-floor window. Outside, a gardener starts a leaf blower. He puts on NULLA and turns ANC on. Silence. The gardener, unaware, blows the leaves straight through the open window; the room fills ankle-deep. He keeps typing.
- **Hook (0–1 s):** a leaf blower roars into frame right next to the window, papers on the desk lift and flutter.
- **Punchline (product-caused):** the final wide: leaves drifting in and settling on his shoulders and keyboard; he types on, calm, in complete silence.
- **Built on:** doc 11 "noise → silence", G07's button-on-the-cup gesture, doc 44 "realism as the joke".

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Exterior, tripod in the garden: blower nozzle swings in, the window and the man behind it | Seedance; blower is an adult gardener in ear defenders |
| 2 | 1.5–3 | Interior, over-the-shoulder, tripod: papers lift off the desk | Papers fall back, one slides to the floor (written fate) |
| 3 | 3–5 | Profile close, slider: he puts NULLA on, cups cover ears, hair pressed under the band | Kling i2v from a product still + real-person ref; headband exact |
| 4 | 5–6 | ECU, macro on a C-stand: his finger presses the cup's button | **Real insert** or Kling; no LED digits |
| 5 | 6–6.5 | Same ECU: **audio hard cut** to room tone | |
| 6 | 6.5–12 | Locked-off interior wide from the room corner (held): leaves stream through the window, drift down, pile around his chair; he types | Seedance; leaves flutter and tumble, settle, never rise again |
| 7 | 12–15 | End card: NULLA on the leaf-covered desk, "NULLA. Up to [x] dB less noise*" | *Super only with the brand's tested figure and conditions; else "Hear less of everything." |

- **Physics check:** a leaf blower pushes dry leaves horizontally at ground level; a ground-floor window sill at ~80 cm makes entry plausible with leaves already airborne (gusts). Leaves are light: they tumble and drift; they don't fly in straight lines. Papers on the desk are blown once and stay where they land.
- **Audio map:** 0.0 s blower two-stroke roar (dominant), leaves skittering; 1.5 s paper flutter; 3.0 s headphone pad creak; 5.0 s button click; **6.0 s hard cut** to room tone + keyboard clicks only (the keyboard proves *we* hear the room, he doesn't); 12 s sonic logo. VO: `Not your problem anymore.`
- **Models and cost:** Seedance 15 s scene (shots 1, 2, 6) $23.88 + Kling shots 3–4 ×2 $1.90 + stills $2.10 = **≈ $28**.
- **Claim check:** ANC never removes 100% of sound; the keyboard click is our audio, but "Dramatization." in small type, and any dB number only from the brand's test with conditions (§4.1).

### C4 · TEMPRA (smart temperature mug) — "11:47" (20 s)

- **Idea:** a remote worker pours a coffee at 9:02. Life interrupts: the doorbell, the dog, a call, the kid's school run. Each time he walks back past the mug. At 11:47 he finally sits down and picks it up, still steaming. His partner's normal mug beside it has a skin on top.
- **Hook (0–1 s):** a time super "9:02" and a coffee steaming on a desk, then his hand is pulled out of frame by a ringing doorbell.
- **Punchline (product-caused):** a **thermal-camera** shot of the desk (a real rig: FLIR camera on a tripod): TEMPRA glows orange, the partner's mug is dark blue. He lifts TEMPRA, toasts it to the cold mug.
- **Built on:** G05 (Ember's "lukewarm? never heard of her"), G08 (time as the proof counter).

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–2 | Locked-off desk wide, tripod: mug steaming lightly, "9:02" super, the doorbell, he leaves | Seedance; steam = thin wisps (doc 49 §3) |
| 2 | 2–4 | Hallway, tripod: he signs for a parcel | 2 people, no dialogue |
| 3 | 4–6 | Same desk wide (identical framing), "9:58": the dog runs through, he chases | State change: chair pushed back |
| 4 | 6–8 | Same, "10:41": he paces on the phone behind the desk | Phone screen dark |
| 5 | 8–10 | Same, "11:30": partner sets her plain mug down beside his and leaves | Her mug: plain white ceramic |
| 6 | 10–12 | Same, "11:47": he sits, lifts TEMPRA, still a soft wisp | **Kling i2v** from the real mug still; no sip on camera |
| 7 | 12–16 | Thermal view, same framing (FLIR on the same tripod): TEMPRA orange, her mug blue; he raises his mug toward hers | Label "Thermal camera. Dramatization." Colours: orange ≈ 57°C, blue ≈ 25°C |
| 8 | 16–20 | End card: "TEMPRA. Set it to 135°F. It stays there.*" | *"Up to 80 min on battery; all day on the coaster" (the client's real spec) |

- **Physics check:** the same locked-off camera across five time states (a real time-lapse rig) makes the passage of time credible and keeps AI drift low. Steam from a 57°C coffee is faint, so wisps only. A cold mug in a room shows no steam. The thermal shot is a stylised image of a true spec, so it must match the stated hold time and say "Dramatization."
- **Audio map:** 0.0 s room tone, doorbell ding at 0.8 s; 2 s parcel scanner beep; 4 s dog nails on wood, a bark; 6 s muffled phone voice (no lips); 8 s ceramic clunk; 10 s chair creak, a satisfied exhale; 12 s thermal "hum" (subtle synth); 16 s sonic logo. VO: `Coffee that waits for you.`
- **Models and cost:** Seedance 2.5 r2v 15 s (shots 1–5) $23.88 + Kling shots 6–7 ×2 $1.90 + stills $2.40 = **≈ $28**.
- **Claim check:** the clock times must fit the battery-and-coaster spec (2 h 45 min from 9:02 to 11:47 is only true if the mug sits on its coaster). Write "on its charging coaster" in the super.

### C5 · FORGE & FROST (insulated steel tumbler) — "Shift" (15 s)

- **Idea:** a roofer fills his tumbler with ice at 6:30 am and sets it on a steel beam in the sun. His apprentice sets a gas-station foam cup beside it. Time supers. At 3:30 pm the apprentice's cup is a warm puddle with a floating straw. The roofer shakes his tumbler: ice rattles.
- **Hook (0–1 s):** ice cubes dropping into the tumbler, top-down, loud clatter, sunrise flare on steel.
- **Punchline (product-caused):** the shake and **the ice rattle**, while the apprentice, slowly, peels the lid off his cup to find warm water.
- **Built on:** G01's sound-proof (the ice rattle) and N15. Honest, not staged: the claim is the brand's tested ice-retention hours.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Top-down, overhead arm: ice into the tumbler | **Real insert** (client) |
| 2 | 1.5–3.5 | Wide, tripod on the roof deck: he sets it on the beam, apprentice sets the foam cup next to it, "6:30 AM" | Seedance; harnesses and hard hats on (safety image) |
| 3 | 3.5–6 | Locked-off on the beam (same framing), heat shimmer, "12:15 PM", shadows shorter | States between cuts |
| 4 | 6–8 | Same framing, "3:30 PM", foam cup slumped with condensation ring | Seedance/Kling still → i2v |
| 5 | 8–10 | Medium, tripod: roofer lifts the tumbler, shakes it twice | Seedance; rattle is SFX on the shake |
| 6 | 10–13 | Close, slider: apprentice peels his lid, looks in, deadpan | Held; no liquid motion needed |
| 7 | 13–15 | End card: tumbler on the beam, "FORGE & FROST. Ice at [x] hours.*" | *Brand's test conditions |

- **Physics check:** sun-path shadows shorten towards noon and lengthen after (the three states must agree with the sun direction). Steel beams get hot but the tumbler is set on it, not in it. No liquid level change in AI; condensation ring on the foam cup is a state. Workers wear fall protection (the image must be compliant).
- **Audio map:** 0.0 s ice clatter (close), 1.5 s nail gun in the distance, gulls; 3.5 s cicadas, heat; 6.0 s same; **8.0 s two ice rattles, dry and bright**; 10 s lid peel squeak; 13 s sonic logo. VO: `Still cold. [pause] Still working.`
- **Models and cost:** Seedance 15 s scene (shots 2, 3, 5, 6) $23.88 + Kling shot 4 ×2 $0.95 + stills $1.80 = **≈ $27**.
- **Claim check:** the time span (9 h) must be inside the brand's tested ice-retention claim in similar heat; otherwise shorten the clock.

### C6 · FOLIO NINE (slim card wallet) — "The Wobbly Table" (15 s)

- **Idea:** a café. A man sits; the table wobbles, his espresso trembles. The barista sighs and wedges a folded napkin under a table leg. It still wobbles. He takes his fat bifold out of his back pocket and sits back down: the chair settles, the table is level. It was never the table.
- **Hook (0–1 s):** ECU of an espresso cup rattling on its saucer, crema shivering, as the table rocks.
- **Punchline (product-caused):** the barista pulls the napkin back out from under the leg, deadpan, and slides FOLIO NINE across the counter to him.
- **Built on:** Ridge's split-screen size comparisons (N11), G09's wallet confrontation, doc 44 deadpan tableau.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | ECU, macro on a table clamp: espresso trembling | Kling i2v; liquid surface ripple only, no level change |
| 2 | 1.5–3.5 | Medium, tripod: he shifts on the chair, the table rocks with him | Seedance |
| 3 | 3.5–5.5 | Low, tripod at floor level: barista wedges a folded napkin under the leg | Seedance |
| 4 | 5.5–7.5 | Medium: still rocking; he pulls a thick bifold from his back pocket, sets it on the table | Wallet ~3 cm thick; cards and receipts visible at the edge |
| 5 | 7.5–10 | Same framing: he sits back; the table is level; the espresso is still | Held 1 s of stillness |
| 6 | 10–13 | Low again: barista pulls the napkin out, pockets it, deadpan | Seedance (template 7.5 adapted) |
| 7 | 13–15 | Counter top-down: FOLIO NINE slides into frame, cards fanned | **Real insert** or Kling i2v from product photo |

- **Physics check:** sitting on a 3 cm wallet tilts the pelvis; it doesn't move a table by itself. To keep it true-ish, the table rocks because he leans on it unevenly (his weight shifts with the tilt). Keep the joke as a mild exaggeration with "Dramatization." The espresso shows surface ripples only.
- **Audio map:** 0.0 s cup-on-saucer rattle (rhythmic), café murmur; 3.5 s napkin fold; 5.5 s the wallet lands with a heavy leather thump; **7.5 s rattle stops: silence except the café**; 10 s napkin swipe; 13 s metal-on-stone slide, a card fan click; sonic logo. VO: `Lose the brick.`
- **Models and cost:** Seedance 15 s scene $23.88 + Kling shots 1, 7 ×2 $1.90 + stills $1.80 = **≈ $28**.
- **Claim check:** no health claim (back pain from wallets is a medical claim; don't say it). Card capacity in the super must be the real number.

### C7 · PLUNGE (waterproof, floating Bluetooth speaker) — "Deep End" (15 s)

- **Idea:** a backyard pool party. The speaker is knocked off the edge into the pool. The party freezes. Underwater, the song keeps playing, muffled. A guy dives in, surfaces holding it up, and **the drop hits exactly as it breaks the surface.**
- **Hook (0–1 s):** the speaker tipping off the pool coping in slow real time, a guest's horrified face behind it, splash.
- **Punchline (product-caused):** the surface break with the bass drop; the party erupts. Tag: the speaker floats face-up, still playing, as the end card.
- **Built on:** doc 11 "sound made visible", G01's "it survived" proof, finding 8 (the product's real behaviour is the joke).

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–1.5 | Low on the pool deck, tripod: an elbow knocks the speaker off the coping; it falls 30 cm into the water | Seedance; splash crown, droplets fall back within 0.6 s |
| 2 | 1.5–3 | Medium wide, tripod: the party freezes, music muffles | ≤5 people, no speech |
| 3 | 3–5.5 | **Underwater camera in a housing**, pool floor level: the speaker bobs back up toward the surface (it floats), bubbles | Write "the speaker floats; it never sinks below 50 cm" (must match the real product) |
| 4 | 5.5–7 | Over the edge, handheld from the deck: a guy dives in | Seedance; one diver, real entry splash |
| 5 | 7–10 | Underwater housing, low: he grabs it, kicks upward | |
| 6 | 10–12 | Surface level, camera on a pool-edge slider at water height: he breaks the surface holding it up; **the drop hits** | The cut and the drop share a frame |
| 7 | 12–15 | Top-down from a pole-cam: the speaker floating face-up, playing, the party jumping in around it | End card super: "PLUNGE. IP67. It floats." |

- **Physics check:** IP67 = 1 m, 30 min (§4.1). The speaker falls into the shallow end and never goes below 1 m. It floats (only if the real one does). Underwater audio is muffled and low-passed; above water it's full. The diver dives into the deep end only; pool depth signage unreadable.
- **Audio map:** 0.0 s party track full; 0.8 s splash; **1.0 s the track low-passed at 400 Hz (underwater)**; 1.5 s silence of the guests, a drip; 5.5 s dive splash; 7 s underwater bubbles; **10.0 s surface break: track back to full at the drop**; 12 s cheers, splashes. No VO; the end super carries the claim.
- **Models and cost:** Seedance 2.5 r2v 15 s (all shots, multi-shot with hard cuts) $23.88 + Kling end card from a real product still ×2 $0.95 + stills $2.10 = **≈ $27**. Music: a licensed track or an ElevenLabs bed with a timed drop (doc 13).
- **Claim check:** depth ≤1 m and fresh water (or the brand's chlorine test). "Floats" only if true. No "waterproof" without the IP rating in the same frame.

### C8 · TERRA LUME (cordless rechargeable table lamp) — "Extension" (20 s)

- **Idea:** a couple sets a dinner table on their balcony at dusk. He runs a lamp out there the old way: three extension cords daisy-chained from the kitchen, across the living room, under the balcony door, taped down. Guests trip on it. She picks up TERRA LUME from the sideboard and carries it out.
- **Hook (0–1 s):** a long-lens shot along the floor: an orange extension cord taped across the whole apartment like a runway line, a guest's shoe catching it.
- **Punchline (product-caused):** the final wide from outside: their balcony glows warm under TERRA LUME, while his corded lamp sits unplugged and dark at the end of 15 m of cord, the cat batting the plug.
- **Built on:** N4 (home decor: product shot first), doc 11 home grammar, doc 44 deadpan tableau.

| # | t | Shot (rig) | Notes |
|---|---|---|---|
| 1 | 0–2 | Floor-level long lens, tripod in the hallway: the taped cord runs to the horizon; a shoe snags it | Seedance; cord path scripted end-to-end (§3 cables) |
| 2 | 2–4 | Medium, tripod: he kneels taping the cord under the balcony door | |
| 3 | 4–6 | Insert, overhead arm: three plugs pushed into each other, tape around them | **Real insert** or Kling still; no brand marks on plugs |
| 4 | 6–9 | Living-room wide, tripod: she lifts TERRA LUME off the sideboard, walks past him | Kling i2v from the real lamp still; lamp rigid |
| 5 | 9–12 | Balcony, slider: she sets it down, a touch on the top, warm 2700K glow fills the table | **Real insert** of the touch (light-on moment) preferred |
| 6 | 12–17 | Exterior wide from the street, long lens (held): their balcony glowing; inside, his lamp dark at the end of the cord; the cat bats the plug | Seedance; cat ≤3 s action |
| 7 | 17–20 | End card: TERRA LUME on the table, "TERRA LUME. Light goes where you go. [x] h per charge.*" | *Brand's tested hours and brightness setting |

- **Physics check:** a 2700K lamp at dusk lights a small table, not the whole street; keep the glow local, with falloff. Extension cords lie flat under tape; nothing floats. Dusk sky consistent across exterior shots.
- **Audio map:** 0.0 s tape screech, a guest's "whoa" (off-screen, no lips), stumble; 2 s more tape; 4 s plug clicks; 6 s her footsteps on wood; 9 s balcony door slide, city dusk ambience, a soft touch "tick" at 10.5 s; 12 s distant traffic, cutlery, the cat's paw tapping plastic; 17 s sonic logo. VO: `Skip the cord.`
- **Models and cost:** Seedance two 10 s scenes $31.84 + Kling shots 3–5 ×2 $2.85 + stills $2.40 = **≈ $37**.
- **Claim check:** battery hours with the brightness level stated. If the lamp is not rated for outdoor use, say "covered balcony" and show it under an overhang.

### 6.1 Ranking

**The best concept: C1 "Band Practice" (HUSHWELL).**
- The hook is sound and motion together in second 1 (the swinging pendant, the dust, the kick drum), which the measured winners and Meta×Toluna both reward (doc 45 D14).
- The punchline is the product's real behaviour told visually: the room keeps shaking, she hears nothing. The joke is **silence you can see**, so the claim is never "measured" on screen; the only number is the labelled NRR.
- Every AI shot is a locked-off or slider shot of a room, a pendant and a sleeping adult: the safest things to generate (doc 43). The one hard hand action (pressing the plug in) is a real insert.
- It cuts natively into a 6 s loop (kick → press → silent print drop) and into product stills (case on the nightstand).
- The same skeleton re-skins for every audio client on the 20-type list (earplugs, ANC headphones, sleep machines): a template the client can order again on the Season plan.

**Second: C7 "Deep End" (PLUNGE).** The drop-on-the-surface-break is a sound punchline that only a waterproof speaker can deliver, and the underwater housing shot is a real, rig-able position. Higher AI risk (water), so it needs a 480p proof first.

**Third: C2 "The Hoist" (UPSTAIR).** It turns the #1 furniture return reason (it doesn't fit) into the joke, and it follows the payoff-first grammar of the furniture winners (G04, G10).

For a VXO gadgets-and-home spec reel, make **C1 + C7 + C2**: one audio, one gadget, one furniture. Recast C1 with Otto as the sleeper for the VXO-owned version.

---

## 7. QA gate additions for this niche

Run after doc 44 §10, doc 45 §5.4, doc 48 §7 and doc 49 §7:

1. **Scale:** every product frame matches the client's dimensions within ±3% against a scale anchor (person, door, standard object). Overlay check on the hero frames.
2. **Colour:** product colour within ΔE < 5 of the client's swatch photo; the grade never shifts the product hue.
3. **Geometry:** no invented ports, buttons, seams, legs, cushions or colourways. Count them against the PDP photos.
4. **Performance events are within spec:** battery, temperature hold, ice hours, IP depth/time, noise reduction, assembly time, weight per box. Each on-screen number has a source in the claims sheet.
5. **No AI shot is the proof of a claim.** Assembly, functional hand actions and liquid events are real inserts or happen between cuts. Any exaggeration is comedy and carries "Dramatization."
6. **Screens, LEDs and UI** are dark or comped; "screen images simulated" where UI appears.
7. **Cables** have two ends, a fixed path, and never move or pass through objects.
8. **No third-party marks** (Apple, AirTag, MagSafe, Bluetooth, Dolby, Hi-Res, UL) in generated frames.
9. **Safety images:** no child near an unanchored dresser or bookcase; fire on a safe base; fall protection on roofs; no one under a hoisted load; knives closed or in culinary use.
10. **Regulatory flags checked:** FCC authorization for RF gadgets before any "buy now" CTA; NRR label for earplugs; Made in USA substantiation; IP certificate.
11. **Native wrapper ready:** a 6 s cut, 3 hook swaps, the UGC-text wrapper and 6–10 product stills (§2.2).
12. **The real product photo closes the film.**

---

## Sources

All URLs are inline in the tables above. Measured files (not committed): `scratchpad/niche/gadgets/G01…G18/` with `v.info.json` metadata and `tile.jpg` frame tiles. The analysis script ran ffmpeg scene detection at 0.30, astats RMS per 0.5 s and a 2 fps 8×4 tile of the first 16 s. Additional sources read:
- Benly Q1 2026: [index](https://benly.ai/benchmarks/q1-2026), [Home & Living](https://benly.ai/benchmarks/q1-2026/home-living), [Furniture](https://benly.ai/benchmarks/q1-2026/home-living/furniture), [Home Decor](https://benly.ai/benchmarks/q1-2026/home-living/home-decor), [Bedding & Bath](https://benly.ai/benchmarks/q1-2026/home-living/bedding-bath), [E-commerce & Retail](https://benly.ai/benchmarks/q1-2026/e-commerce-retail), [Technology & Software](https://benly.ai/benchmarks/q1-2026/technology-software) (no consumer-electronics rows). Smart-home, kitchen and electronics-retail sub-pages returned 404.
- Returns: [eightx furniture return benchmarks](https://eightx.co/blog/average-furniture-and-home-return-rate-benchmarks), [Cylindo](https://blog.cylindo.com/decimating-furniture-return-rates-with-360-hd-views) `[vendor]`.
- Brand evidence: [Foreplay on Ridge](https://www.foreplay.co/post/the-ridges-ad-auction-analysis), [Practical Ecommerce interview with Ridge's founder](https://www.practicalecommerce.com/?p=1506456), [Lovesac Q1 call highlights](https://www.nasdaq.com/articles/lovesac-q1-earnings-call-highlights), [Bigblue on Loop](https://www.bigblue.co/it/blog/loop-earplugs-from-eu0-to-eu42m-targeting-ads-and-community), [CreatorIQ on Stanley](https://creatoriq.com/blog/earned-podcast-ep-111-terence-reilly-stanley-cup-quencher-viral-car-fire-tiktok-influencer-marketing-crocs), [HubSpot on the Stanley car fire](https://blog.hubspot.com/marketing/stanley-cup-car-fire), [LBB on Cozey's in-house holiday spots](https://lbbonline.com/news/Cozey-for-the-Holidays), [My Modern Met on the AI gorilla sofa](https://mymodernmet.com/ai-gorilla-sofas/), [TikTok Fantastic Furniture case](https://ads.tiktok.com/business/en-US/inspiration/fantastic-furniture-551).
- Law and policy: [NAD Dyson v. Dreame (Mondaq)](https://www.mondaq.com/nad-says-a-disclosure-cant-fix-a-misleading-product-demonstration/1837024), [Google Gemini NAD inquiry (Kelley Drye)](https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/google-unlists-gemini-video-after-nad-inquiry), [47 CFR 2.803](https://www.law.cornell.edu/cfr/text/47/2.803), [40 CFR 211 Subpart B](https://www.law.cornell.edu/cfr/text/40/part-211/subpart-B), [CPSC clothing storage units FAQ](https://www.cpsc.gov/FAQ/Clothing-Storage-Units), [Made in USA enforcement (Kelley Drye)](https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/trump-administration-directs-federal-trade-commission-to-prioritize-made-in-usa-enforcement), [TikTok dangerous products ad policy](https://ads.tiktok.com/help/article/tiktok-ads-policy-dangerous-products-or-services?lang=en).
- Builds on docs 11, 13, 41, 42, 43, 44, 45, 48, 49 in this folder.
