# 22 — Viral AI ads teardown: what the top 5% do at the frame level

Researched 2026-10-08. It builds on 14 (Rourke Heath), 16 (seamless flow), 17 (hero stills) and 19 (storytelling) and does not repeat them.
- **[inf]** marks my inference.
- `~` marks a count read off a YouTube storyboard. Storyboards sample about 1 frame per second, so cuts shorter than 1 s are under-counted.
- No generation API was used.

## Method and limits

- **33 ads watched as frames.**
  - **YouTube:** video download is bot-blocked, but the `sb0` storyboard mosaics (160×90, about 1 fps) still download with `yt-dlp --extractor-args youtube:player_client=web_embedded -f sb0`. That gave 29 contact sheets.
  - **X:** 4 posts at 720p, each with a 16-frame sheet, a 0–3 s hook strip, scene-cut detection (0.30) and R128 loudness. Videos deleted after analysis.
- **Creator accounts read:** two PJ Accetturo talk transcripts (IM8 workflow, Wonder Sessions), breakdowns in YouTube descriptions and X posts, trade press.
- **Not accessed:** Ads of the World (WAF), TikTok discovery pages, 2 of 5 talk transcripts (HTTP 429), the Adathon winner's video, Cannes 2026 results for the Luma Dream Brief. Fetched pages are unverified creator or vendor claims.

---

## 1. The corpus (measured)

Columns:
- **Len / shots / ASL:** length in seconds, shot count (excluding the end card), average shot length.
- **Frame 0:** the first frame.
- **Product:** the share of screen time with the product or brand device visible, and how big it is.
- **Real / tell:** what sells it as real, and what gives it away as AI.

### A. Comedy and format hijacks (the most viral group)

| Ad (tool, year) | Len / shots / ASL | Frame 0 | Product | Light / grade | Real / tell |
|---|---|---|---|---|---|
| **Kalshi "NBA Finals"**, PJ Accetturo (Veo 3, Jun 2025) [X](https://x.com/PJaccetturo/status/1932893260399456513), 1.14M views on X | 30 / 14 / **2.1 s** (measured). Cuts at 1.8, 5.3, 7.2 … 27.5 s | A shirtless old man in a US-flag cape, frog-marched by police past a courtside reporter, **already mid-action**, mic in frame | The brand lives in a **lower-third market ticker** ("OKC wins Championship? $1,000 → $5,623") on ~70% of shots. Logo card only in the last 1.5 s | Flat daylight "local news" exposure, wide lens, saturated Florida palette. −13.9 LUFS (loud) | **Real:** vox-pop grammar (reporter mic, eyeline to camera, sunburnt regional casting), a readable sign ("FRESH MANATEE"). **Tell:** waxy young skin, over-clean crowd |
| **Kalshi "YOLO"**, Genre.ai, director Theo Dudley (Veo 3, Jul 2025) [youtu.be/mzXFURkcCt4](https://youtu.be/mzXFURkcCt4) | 47 / ~22 / ~1.7 s | Back-of-head OTS of a man watching the crucifixion: an "historical footage" pastiche | The odds overlay ("Will Jesus rise again? Odds: 0%") on every shot, then a 9 s end card | 2.39:1 letterbox, warm sepia day, cold-blue night inserts | **Real:** an epic-movie register (smoke, backlight, anamorphic framing). **Tell:** plastic armour faces in the Sparta battle |
| **Puppramin** fake pharma ad, PJ Accetturo (Veo 3 t2v, May 2025) [youtu.be/MWJMzZLmoYk](https://youtu.be/MWJMzZLmoYk) | 82 / ~25 cuts / ~3 s. Creator: "13 shots, 5–10 gens per shot, ~$500, < 1 day" | A depressed man on a bed in a dark room (the pharma cliché opening) | A pill bottle in 1 shot, plus a persistent pharma disclaimer bar | Golden-hour suburbia, then side effects escalate to night, fire and a satanic pentagram | **Real:** a pitch-perfect genre parody with on-camera testimonial dialogue. **Tell:** the dog-to-raccoon gag hides the morph by design |
| **Popeyes "(w)Rap Battle"**, PJ Accetturo and Dawit (Veo 3 t2v, Suno + human lyrics, Jul 2025) [youtu.be/V8dU3ZMxugg](https://youtu.be/V8dU3ZMxugg) | 65 / ~48 / **~1.2 s** | A clown silhouetted in a dark doorway | The wrap in hands, small, in ~30% of shots. 6 s orange end card | Night, sodium and neon practicals, handheld music-video look | **Real:** crowd energy, practical-light falloff. **Tell:** viewers asked why no real actors and musicians were used ([AOL](https://www.aol.com/articles/popeyes-first-ai-generated-commercial-150300650.html)) |
| **Liquid Death spec** (Veo 3, "Made with AI" on the end card) [youtu.be/FYFNJZMpaes](https://youtu.be/FYFNJZMpaes) | 62 / ~30 / ~1.8 s | Ultra-wide snowy road: a cop car and a sedan at a traffic stop | The can in 4 drinking shots, then an **8 s packshot on white** | *Fargo*-flat overcast, a desaturated snow palette, a colourist credited | **Real:** shot/reverse-shot dialogue with deadpan casting (moustache, ear-flap hat). **Tell:** the background gag inserts are cleaner than the dialogue plates |
| **WinRAR spec**, Burak Tuyan (Seedance 2.5, 2026) [X](https://x.com/buraktuyan/status/2092008235075084363), 676k views | 30 / 15 / **2.0 s** (measured) | Two adult torsos carrying a cardboard box. Hook at 1.5 s: a beige CRT emerges from bubble wrap, subtitle "We bought your first computer" | The product UI on one monitor insert. 4 s end card "Trial is 40 days. Not until you're 40." | Soft north-window light, John Lewis-style warm domestic grade, shallow DOF | **Real:** ordinary faces, clutter, steam, practical lamps; the kid ages to 39 with the same parents. **Tell:** almost none at 720p |

### B. Big-brand spectacle, and the backlash group

| Ad | Len / shots / ASL | Frame 0 | Product | Light / grade | Real / tell and reaction |
|---|---|---|---|---|---|
| **Coca-Cola "Holidays Are Coming" 2024** (Silverside / Secret Level / Wild Card) [youtu.be/8m0Y-GisSeM](https://youtu.be/8m0Y-GisSeM) | 65 / ~35 / ~1.8 s | An ECU of a red truck grille with snow | Truck livery ~60% of the time. The bottle appears in 2 shots | Blue-hour snow, warm string lights | Called "soulless", "creepy", "dystopian". "Real Magic" mocked ([the-decoder](https://the-decoder.com/ai-generated-holidays-are-coming-coca-cola-ad-looks-festive-but-feels-artificial-critics-say/)) |
| **Coca-Cola 2025** (Silverside + Secret Level) [youtu.be/Yy6fByUmPuE](https://youtu.be/Yy6fByUmPuE) | 61 / ~28 / ~2.1 s | Santa's hand sets a **Coke bottle** into a miniature snow village (the product is in frame 0) | Bottle 0–3 s only. Then trucks plus 5 s of logo | The same warm/blue split. Mostly animal close-ups looking into the lens | **Tell:** extra wheels and misplaced axles ([TechRadar](https://www.techradar.com/ai-platforms-assistants/coca-cola-faces-backlash-again-for-missing-the-spirit-of-the-holidays-with-another-ai-slop-ad)). Animals instead of people sidestep uncanny faces [inf] |
| **McDonald's NL Christmas** (TBWA\Neboko + The Sweetshop, Dec 2025; **pulled after 3 days**) [youtu.be/E-YwjXEVGo8](https://youtu.be/E-YwjXEVGo8) | 45 / ~30 / ~1.4 s | A car interior, a family stuck in traffic in the snow | No food shown. Restaurant and logo only in the last 8 s | Cold, desaturated Dutch winter | **Tell:** a fisheye laughing grandma and rubbery chaos. Critics: "cynical and unfun", "creepy" ([NBC](https://www.nbcnews.com/world/europe/mcdonalds-ai-generated-christmas-advert-social-media-backlash-rcna248590)) |
| **Toys"R"Us origin** (Native Foreign, Sora, 2024) [youtu.be/ywxFszydgqY](https://youtu.be/ywxFszydgqY) | 61 / ~22 / ~2.4 s | A 1950s storefront exterior | Geoffrey the giraffe throughout, then a 10 s logo | Warm Americana, then a blue starfield dream | **Tell:** the boy's face changes between shots, and the smile is uncanny ([TechRadar](https://www.techradar.com/computing/artificial-intelligence/watch-the-ai-produced-film-toysrus-made-using-openais-sora-and-get-misty-about-the-ai-return-of-geoffrey-the-giraffe)) |
| **Svedka "Shake Your Bots Off"** (Silverside, ComfyUI, Super Bowl LX) [youtu.be/pkeWRI2yJGM](https://youtu.be/pkeWRI2yJGM) | 31 / ~9 / ~3.4 s, including one ~10 s locked dance shot | A robot face peeking from behind a hand | Bottle only in the last 7 s | Blue/red club light, haze | **Real:** robots can't be uncanny humans. Adweek creatives: "AI is a tool, not a concept" ([Adweek](https://www.adweek.com/creativity/creatives-react-svedkas-forgettable-super-bowl-ad-proves-ai-isnt-an-idea/)) |
| **Under Armour × A. Joshua** (Wes Walker, 2024) [youtu.be/-VrOv982U4A](https://youtu.be/-VrOv982U4A) | 61 / ~45 / ~1.2 s | A B&W low FPV over sand dunes | A UA chest logo in 1 shot, then end cards | **Monochrome** throughout, which hides texture errors [inf] | Backlash over uncredited reuse of another director's footage ([TechCrunch](https://techcrunch.com/2024/03/14/ai-powered-ad-ignites-creator-controversy-on-instagram/amp/)) |
| **Valentino DeVain** "digital creative project" (Dec 2025) [youtu.be/UjsFVdIZ7ws](https://youtu.be/UjsFVdIZ7ws) | 30 / ~5 / ~6 s | The "DeVain" title over an aquarium room | The bag is small, carried by a model | Lurid purple and pink, low-fi video art | Bodies morphing into the logo. Called "disturbing", "AI slop" ([eWeek](https://www.eweek.com/news/valentino-ai-misfire/)) |

### C. Premium-niche product films (craft benchmark)

| Ad | Len / shots / ASL | Frame 0 | Product | Light / grade | Real / tell |
|---|---|---|---|---|---|
| **IM8 (Beckham) "Red or Green"**, Genre.ai (NB Pro on Ideogram, licensed likeness of Aryna Sabalenka) [youtu.be/ER5P_wH0E9Q](https://youtu.be/ER5P_wH0E9Q). "233M views in 3 days" (claim) | 51 / ~38 / **~1.2 s** | A red molecular ring on black | The tin in hand ×6 plus a lifestyle pack: ~15%. 9 s end card | A **two-colour code**: healthy red/orange vs teal and toxic green. Low key throughout | **Real:** Nike-style punch cuts, ECU eye and heart inserts. Darkness hides faces [inf] |
| **Changan Deepal S07**, official ad (László Gaál for EQ / i-DAC; trained car + driver models into Runway) [youtu.be/d1ATmPCzo4o](https://youtu.be/d1ATmPCzo4o) | 80 / ~60 / ~1.2 s | Black, then a headlight glint in fog | The car in ~85% of shots, usually 10–30% of frame width, always the same orange | Dawn fog → tropical teal → golden city | **Real:** the product never drifts (trained). Logo "easter eggs" hidden in a waterfall and a reef. **Tell:** postcard-perfect landscapes |
| **Runway "The Watch"** (single creative, one afternoon, 2026) [youtu.be/X1HNsMGa648](https://youtu.be/X1HNsMGa648) | 37 / ~26 / ~1.2 s | A B&W London schoolboy street, handheld | The watch on wrists in ~6 inserts. Then a 2 s packshot on white | **B&W documentary**, available light | **Real:** candid street casting and age-range faces. B&W kills colour-sheen tells [inf] |
| **Loewe spec**, Burak Tuyan (NB Pro → Veo 3.1 / Kling 3.0 / Seedance 1.5, music bed first) [X](https://x.com/buraktuyan/status/2020014386794864671) | 62 / 18 / **3.5 s** (measured) | An underwater model in a chiffon gown holding the bag among coral | The bag or shoe is the hero in 5 of the first 8 shots, at 25–40% of frame | Muted teal, a fashion-editorial grade | **Real:** editorial stillness suits AI. **Tell:** floaty hair physics |
| **Sephora "Pure Edge" spec** (Veo 2, 2025) [youtu.be/ZoEvwdlIl5M](https://youtu.be/ZoEvwdlIl5M) | 30 / ~20 / ~1.3 s | The SEPHORA wordmark on black | Mascara, lipstick and gel macros ~70% of the time | B&W plus one accent colour (crimson), 2.39:1 | **Real:** macro texture (bristles, droplets). Faces only in the last 6 s |
| **Nike JA3 spec**, Dime Labs (Higgsfield / Kling, NB) [youtu.be/-wNXboIhlSU](https://youtu.be/-wNXboIhlSU) | 21 / ~10 / ~1.7 s | The JA logo in a dark jungle | A pink dino morphs into the shoe ~50% of the way in | God rays in the jungle | Creator: "300 photos and 500 videos" for 21 s |
| **Nike "It has no name"**, Wide Silvente (MJ / Flux / Imagen 3 → Veo 2 / Kling 2.0, Suno, ElevenLabs) [youtu.be/RFGfkOLGsEM](https://youtu.be/RFGfkOLGsEM), 256k | 41 / ~35 / **~1.0 s** | A hand gripping a rope, ECU | Swoosh on gear, small, ~40% | Teal shadows, warm skin, sweat macro | **Real:** the classic training montage hides individual frames |
| **Ferrari spec**, Adverto (MJ, Kling, Magnific) [youtu.be/2h8hrL7ozJI](https://youtu.be/2h8hrL7ozJI) | 48 / ~35 / ~1.3 s | A black car under dark forest canopy | Car ~60% | Backlit golden forest | Parallel editing with a cheetah and an eagle (an animal metaphor). The watch-on-wrist insert hints at a premium-tie-in grammar |
| Dave Clark: **Grok Imagine Super Bowl** (2nd place, $500k) [youtu.be/BD8P27nlI2M](https://youtu.be/BD8P27nlI2M) · **Nike Seedance 2.5** (50 refs, hand-drawn → NB / GPT images) [youtu.be/f9o640Xjqsg](https://youtu.be/f9o640Xjqsg) · **Adidas "coffee break"** [youtu.be/bzWOyzM3RSs](https://youtu.be/bzWOyzM3RSs) | 31 / ~14 / 2.2 s · 77 / ~45 / 1.6 s · 31 / ~22 / 1.3 s | A boy's back watching a rocket launch · lacing shoes on a street · neon sneakers in puddles | The Grok app on a phone in 1 shot · shoe 2 shots · shoe ~50% | Teal-orange film · pink/teal neon anime-3D · neon studio | Grok: a sincere story that works *because* it is a child's dream (stylised) [inf] |
| **Luma "Pizza Baby"** (Dream Brief promo, 660k) [youtu.be/zrdS6u2e_rw](https://youtu.be/zrdS6u2e_rw) | 35 / ~15 / ~2.3 s | A delivery-room POV between the stirrups | The Luma pizza box in 6 shots | 1970s mint-green hospital, film grain | Absurdist deadpan. A locked, symmetrical comedic framing |
| **Artlist "Seedance 2.0"** (paid launch film, 19M views) [youtu.be/77FAnT935IE](https://youtu.be/77FAnT935IE) | 52 / ~35 / ~1.3 s | An aerial of a desert railway diner at golden hour | n/a (a platform ad) | Hard golden window light, haze | Hollywood ensemble dialogue. A flying-saucer reveal at the end |
| **Average baselines:** Dior Sauvage spec [youtu.be/ujUFZDza_18](https://youtu.be/ujUFZDza_18), Miss Dior spec [youtu.be/rJ4QEpssFYg](https://youtu.be/rJ4QEpssFYg), "AETHER" fragrance [youtu.be/Xvde1evLoTw](https://youtu.be/Xvde1evLoTw) (all < 1k views) | 31 / **7 / 4.4 s** · 41 / ~22 / 1.8 s · 40 / ~14 / 2.5 s | A slow empty landscape · a woman walking in Paris · black | A **centred bottle at 30–60% of frame for half the film** · bottle in a flower bed under the Eiffel Tower · bottle in crystal ribbons | Blue-hour desert · golden Paris · cold chrome | No idea, no stakes; imitates the house film; centred packshots on loop |

**Also seen:** IKEA Veo 3 spec, 13 s, **one locked-off shot**, box bursts into a furnished room ([youtu.be/4Rpi1ZMKy74](https://youtu.be/4Rpi1ZMKy74)); Svedka "Thirst Trap", 16 s, ~8 shots, 5.4M views ([youtu.be/vdcj0gVUov4](https://youtu.be/vdcj0gVUov4)); a one-generation 20 s Seedance 2.5 scene with ~5 internal cuts that threshold 0.30 missed in low key (use 0.2) ([X](https://x.com/sebatheepan/status/2104706252131725372)).

### What the numbers say [inf, from the tables]

- **ASL** of winners: **1.0–2.2 s** (editorial fashion ~3.5 s). Low-view specs hold 4+ s shots or loop a centred packshot.
- **Frame 0** of winners: **a person mid-action or a graphic**, never a logo or empty landscape. Even Coke 2025 opens on a hand *placing the product*.
- **Product time** is low in the most viral spots (0–30%: Kalshi, Popeyes, McDonald's, Coke 2025); the brand rides a **device** (ticker, odds, disclaimer bar, livery). Premium product films invert it (Deepal ~85%, Sephora ~70%) with short macros or in-context heroes, never 5 s centred holds.
- **End cards run 4–9 s** in brand spots (YOLO, IM8, Liquid Death, Toys"R"Us), longer than 04's 1.5–3 s default [inf].

---

## 2. Effort: generations per final second, hours, cost

| Ad | Inputs → output | Gens per final second [inf, arithmetic] | Time / team / cost |
|---|---|---|---|
| Kalshi NBA | 300–400 Veo 3 gens → 15 clips → 30 s ([MPR/NPR](https://www.mprnews.org/story/2025/06/23/npr-ai-video-ad-kalshi-advertising-nba-finals)) | **10–13** | 2 days, 1 person, < $2k prompting |
| Puppramin | 13 shots × 5–10 gens ([desc.](https://youtu.be/MWJMzZLmoYk)) | ~1–1.5 (t2v with dialogue) | < 1 day, ~$500 |
| Kalshi YOLO | writer + director + alt-line pitches ([desc.](https://youtu.be/mzXFURkcCt4)) | n/a | 1 week |
| Popeyes | scrapped i2v, Veo 3 t2v only | n/a | 3 days, music in 1 day |
| Nike JA3 | 300 stills + 500 videos → 21 s | **~24 video gens/s** | promo-unlimited credits |
| WinRAR | 20+ Seedance 2.5 tests at 480p, finals at 720p, Topaz → 1080p, one shot redone in Seedance 2.0 | **~1** (whole-spot generations) | one creator, a 14,000-char prompt |
| PJ workshop rule | per shot: ~5 gens at 720p, then 2–3 at 1080p. Seedance ~$3 per 15 s at 720p vs ~$13–15 at 1080p. "Burned $1,000 of credits in a day" | 0.5–1 per shot-second | 6 h to lock two realistic characters |
| Coke 2024 (Silverside) | 10,000 images + 5,000 video segments → 100+ assets ([eWeek](https://www.eweek.com/news/coca-cola-ai-ads/)). One Secret Level squirrel scene took "a couple hundred" iterations | ~80 per final second of the master [inf] | ~2 months |
| Coke 2025 | 70,000 clips, 5 AI specialists, ~100 people total ([TechRadar](https://www.techradar.com/ai-platforms-assistants/coca-cola-faces-backlash-again-for-missing-the-spirit-of-the-holidays-with-another-ai-slop-ad)) | ~1,100 (all versions) | ~1 month |
| McDonald's NL | "thousands of takes", 10 people, 5–7 weeks ([TechRadar](https://www.techradar.com/ai-platforms-assistants/mcdonalds-pulls-ai-generated-christmas-ad-after-backlash-over-soulless-visuals-and-holiday-chaos)) | ~50+ | 5–7 weeks |
| Toys"R"Us | "hundreds of iterative shots → a couple of dozen" plus corrective VFX ([VentureBeat](https://venturebeat.com/ai/toys-r-us-unveils-first-commercial-made-with-openais-sora)) | ~5–10 | a few weeks |
| Deepal S07 | separately trained exterior, interior and driver models → Runway | n/a | 5 weeks, +2 for the Thai cut |
| Svedka | ComfyUI pipeline; characters, world and choreography kept separately controllable ([Comfy](https://comfy.org/customers/svedka-silverside)) | n/a | < 1 month of production (vendor); ~4 months of rebuild (WSJ via eMarketer) |
| Runway "The Watch" | "one creative, one afternoon" | n/a | hours |

**Planning numbers [inf]:** Kling start/end product ads, **8–15 video gens per final second** (3–5 seeds per shot, ~2 s used of 5 s, retakes). Long Seedance takes, **1–2 full-length 480p gens per final second**, then 2–3 finals at 720p. Labour, 2–3 person-days per 30 s social spot; brand work adds approvals ("take over a month… the approvals process", PJ).

---

## 3. The 15 craft moves of the top 5%, with recipes

The recipes use our stack: Higgsfield **Flare** (product-exact stills), **Soul Cinema** (plates and people), **Kling 3.0 pro** i2v with `image_url` / `last_image_url`, **Seedance 2.5** (i2v / r2v, up to 50 refs, timestamped prompts), **ElevenLabs**, and **ffmpeg**. Prices and endpoints are in 12. The seam mechanics are in 16 and are not repeated here.

**1. Borrow a format the audience already trusts as "real footage".**
- *Examples:* local-news vox pop (Kalshi), pharma spot (Puppramin), historical epic (YOLO), *Fargo* cop drama (Liquid Death), John Lewis family drama (WinRAR), documentary B&W (Runway Watch).
- *Why it works:* the viewer's brain checks the genre's grammar, not the pixels [inf].
- *Recipe:* add `format_skin` to the strategy card and lock its grammar before prompting (news = eyeline to lens, mic in frame, lower third, 24 mm, flat daylight). Put it in the Seedance GLOBAL STYLE header.

**2. The idea must need AI, or be impossible to shoot.**
- *Examples:* Kalshi was written around who was *actually* in the Finals, days before tip-off; WinRAR spans 28 years of one life; IKEA furnishes a room in one take.
- *Recipe:* every storyline from 19 must pass the question "could a $500k shoot do this?" If yes, add a time-jump, a scale-jump or a cultural-moment hook.

**3. Frame 0 is a human mid-action, or a graphic, and the payoff lands by 1.5 s.**
- *Examples:* Kalshi at 0.0 s, a frog-marched flag-caped man; WinRAR, the CRT out of bubble wrap at 1.5 s; IM8, a red molecule. Losers open on an empty landscape or a centred bottle.
- *Recipe:* frame 0 as a Soul Cinema still with the action in progress ("already moving", 16 §2); Kling 3.0 pro 3 s trimmed from frame 6; QC that the 0–3 s strip shows a state change by 1.5 s.

**4. Cut at 1.2–2.2 s ASL. Hold exactly one longer shot.**
- *Examples:* top-group ASL is 1.0–2.2 s; Svedka's 10 s dance hold and the IKEA one-take are the single "breath". AI flaws accumulate with exposure time, so short shots show only each generation's best 1–2 s [inf].
- *Recipe:* use 1.2–2.2 s from the middle of 5 s Kling clips; plan one 4–8 s hero; run `select='gt(scene,0.30)'` (0.2 for dark spots) on our export and flag ASL > 2.5 s outside the hero.

**5. Continuity through a device, not only through the camera.**
- *Examples:* Kalshi's ticker, YOLO's odds overlay and Puppramin's disclaimer bar connect unrelated shots; IM8's red/green code; Runway's watch passing wrist to wrist; WinRAR's one subtitle voice. This is the *editorial* glue that 16 lacks.
- *Recipe:* one device per ad (ticker, recurring object, line or colour code). Overlays in post with `ffmpeg drawtext`/`overlay`, never generated in-model.

**6. One grade logic, ideally a two-colour code or monochrome.**
- *Examples:* IM8 red vs teal/green; Coke warm practicals vs blue snow; Sephora B&W + crimson; Under Armour and Runway full B&W; Loewe muted teal.
- *Benefits:* monochrome or limited palettes hide the "AI sheen" and per-clip colour drift [inf].
- *Recipe:* write the palette into every Flare and Soul prompt ("palette limited to oxblood and slate teal"); one pass over the timeline: `colorbalance=…,eq=saturation=0.85,lut3d=brand.cube`; B&W = `hue=s=0` + curve + grain.

**7. Motivated, imperfect light: window, overcast, sodium, practicals.**
- *Examples:* WinRAR's north window; Liquid Death's overcast snow; Popeyes' sodium and neon; Kalshi's flat TV-news daylight. Averages use glossy beauty light everywhere.
- *Recipe:* name the source and its flaw in every plate prompt ("single north window camera-left, warm ceiling-bulb practical, shadows unfilled, slightly under"). Ban "studio lighting, rim light, softbox" on people; product heroes keep 17's recipes.

**8. Cast against AI beauty.**
- *Examples:* Kalshi's sunburnt seniors and pot-bellies; Puppramin's ordinary suburbanites; Liquid Death's moustache-and-mullet; WinRAR's plain family.
- PJ: AI "over-beautifies" women; it took **6 hours** to lock two realistic characters, and he avoids 4K because it "looks plasticky".
- *Recipe:* Soul Cinema character prompts give age, weight, skin and wardrobe wear ("62, sun-damaged skin, crooked lower teeth, faded tank top with a sweat stain"). Build a sheet once and reference it in Seedance r2v.

**9. Product truth: exact when shown, short when shown, always in context.**
- *Examples:* Deepal trained car and driver models, so the car never drifts across ~60 shots; Loewe and Sephora use many short macro or in-hand moments; Coke's extra wheels became the headline.
- *Recipe:* every product shot starts and ends on a Flare still from the product reference (17), via Kling 3.0 pro i2v with `last_image_url`. Product shots ≤ 2 s except the packshot (4–6 s, start = end). Screen-share targets: comedy/device spots 10–30%, premium product films 50–80%.

**10. Hide what AI does badly; feature what it does well.**
- *Strengths:* macro texture (Sephora), non-humans (Svedka robots, Coke animals), epic scale (Deepal, YOLO), stylised worlds, low key (IM8), B&W. *Weaknesses:* smiling children, morphing bodies, long human close-ups (Toys"R"Us, Valentino, McDonald's grandma).
- *Recipe:* no human close-up over 1.5 s unless it carries the line; morph objects (dino → shoe, box → room), never faces; talking faces only via Seedance with an audio reference.

**11. Sound sells "real" more than pixels do.**
- *Examples:* Veo 3 dialogue carried Kalshi and Puppramin. WinRAR used a Seed Audio voice reference, a solo-instrument library track and added SFX. PJ: "90% of sound design baked into Seedance… 'no music, sound design only'", then stock music; bad AI audio is "tinny thin". Coke's Secret Level cut used live musicians.
- *Recipe:* clips with SFX on and music off (or ElevenLabs SFX per beat); one ElevenLabs voice ID; licensed music chosen first and cut to (Loewe started "with a music bed"). Measured winners ran −14 to −22 LUFS; deliver `loudnorm=I=-14:TP=-1.5`.

**12. Draft low, finish selectively, keep the grain.**
- *Examples:* WinRAR went 480p tests → 720p → Topaz 1080p, and the upscaler destroyed on-screen text, so that shot was regenerated. PJ: Nano Banana Pro 2K/medium keeps grain while 4K "strips it… plasticky"; "crappy lower bitrate… looks like real footage".
- *Recipe:* Seedance 480p blocking, 720p finals; Kling pro only on approved stills; faithful upscale, never across labels (17 rule 9); finish with `noise=alls=6:allf=t` + light `unsharp`.

**13. Over-generate and select: coverage, not one-shotting.**
- *Benchmarks:* Kalshi 10–13 gens per final second; Nike JA3 ~24; Toys"R"Us "hundreds → two dozen"; Coke squirrel "a couple hundred".
- *Recipe:* budget seeds per shot up front (3 drafts → 1–2 finals); pick with 17 §5's pairwise judge on video (best 2 s window, product fidelity, motion); log the ratio per project.

**14. Script and team before tools; pre-viz with references.**
- *Examples:* Genre.ai splits **writer, director, cinematographer(s), animator(s), editor**; Figma or Luma boards where an LLM turns director-picked film stills into prompt language; YOLO's ex-Comedy Central head writer plus "writers in our network pitch alt lines"; Clark blocks "every beat" with 50 Seedance refs; WinRAR used a 14,000-character prompt.
- *Recipe:* script first; 3 alt punchlines from separate prompts; a 6–12 frame Soul Cinema storyboard; Seedance 2.5 r2v with `@image_n` per beat and timestamped sections (09 template).

**15. Choose a tone AI can carry: absurd, self-aware or stylised, not sentimental realism.**
- PJ: "Do not make a Dove commercial about moms… make it like an Old Spice commercial… or cool like Nike, Porsche".
- Every backlash case (Coke, McDonald's, Toys"R"Us, Valentino) tried warmth, heritage or luxury artistry. The viral ones are funny or knowingly over the top.
- Sincere stories survive when they are stylised (Grok's space dream) or documentary-real with a product truth (WinRAR, Runway Watch).
- *Recipe:* default tones are deadpan comedy, mock-genre and stylised myth. Sincere drama only with moves 7, 8, 11 and 12 plus a twist (19).

---

## 4. "Real" vs "AI" at the frame level (checklist for QC)

| Sells it as real (seen in the winners) | Gives it away (seen in losers and backlash) |
|---|---|
| Eyeline to lens plus a mic in frame (reportage) | The same face shape and lighting on every extra (crowd clones) |
| Ordinary bodies, specific wardrobe wear | Over-beautified, waxy young women |
| Light from a named source; unfilled shadows | Global soft "beauty" light on every shot |
| Hand-held micro-shake, focus breathing | Floaty camera that eases in and out of every clip (16 §0) |
| Readable but sparse in-world text, added in post | Gibberish signage; text melting after upscale (WinRAR's fix) |
| Short shots that only show the best 2 s | Long holds on faces and hands; smiles that "turn" (Toys"R"Us) |
| Consistent product geometry | Extra wheels or axles (Coke 2025); a morphing bag or logo (Valentino) |
| Grain, mild compression, limited palette | 4K plastic smoothness, uniform saturation |
| Diegetic sound, room tone, a real music track | "Tinny thin" AI audio, a different room tone per clip |

---

## 5. What critics and audiences reacted against

- **Replacing heart in heritage rituals:** Coke 2024/2025 "soulless, creepy, dystopian"; "Real Magic" mocked; Alex Hirsch: "made from the blood of out-of-work artists" ([the-decoder](https://the-decoder.com/ai-generated-holidays-are-coming-coca-cola-ad-looks-festive-but-feels-artificial-critics-say/)).
- **Cynical tone plus glitches:** McDonald's NL pulled after 3 days despite the "thousands of takes" defence ([NBC](https://www.nbcnews.com/world/europe/mcdonalds-ai-generated-christmas-advert-social-media-backlash-rcna248590)). **Body horror in luxury:** Valentino "disturbing", even though disclosed.
- **Credit and labour:** Under Armour's uncredited footage; Popeyes viewers wanted real actors and musicians.
- **"AI is not an idea."** Svedka was called "forgettable", "low-budget" and "derivative" of Chris Cunningham's Björk video ([Adweek](https://www.adweek.com/creativity/creatives-react-svedkas-forgettable-super-bowl-ad-proves-ai-isnt-an-idea/)). Meltwater found ~50% of Super Bowl LX AI-ad conversation negative ("uninspired", "low-quality") ([Meltwater](https://www.meltwater.com/en/news/ai-ads-face-skepticism)).
- **Clarity.** On Kalshi, an analyst needed several viewings to understand what was advertised (MPR/NPR).
- **Measured:** NIQ (2,000+ viewers, EEG ~150) found most AI ads spotted and rated more "annoying, boring, confusing" ([NIQ](https://nielseniq.com/global/en/news-center/2024/niq-research-uncovers-hidden-consumer-attitudes-toward-ai-generated-ads/)); IAB 2024, only 48% of Gen-Z/millennials positive (via MPR); Truescope, 83% "neutral" on Coke, so the loud minority is creatives and press [inf].
- **What judges reward.** The Higgsfield × Adweek Adathon scored idea, storytelling and effectiveness, craft (camera and sound) and **realism** equally. The winner (AI-R Studio) was self-aware satire about AI itself ([completeaitraining](https://completeaitraining.com/news/ai-r-studio-wins-higgsfields-ai-adathon-competition-at/), [Higgsfield](https://higgsfield.ai/contests/adathon)).

**Rules [inf]:** no AI sentimental-heritage films unless the client accepts the press risk; disclose ("Made with AI", as Liquid Death did) on comedic concepts; credit every human; a viewer must name product and benefit after one view.

---

## 6. Changes to adopt

- **00/04:** end card 4–6 s for brand spots, 2–3 s for cutdowns; add `format_skin` and `continuity_device` to the strategy card.
- **15:** add the 0–3 s strip test, the ASL check, product-share targets, and "name the product after one view".
- **16:** add editorial devices (move 5) as continuity method E. **17/06:** counter-casting tokens; 2K-not-4K grain.
- **18:** log gens per final second and person-hours; use `-f sb0` storyboards for competitor references.

## Sources not cited inline

- PJ Accetturo: IM8 workflow (Marketing Against the Grain) [youtu.be/yUdE9oj3sWk](https://youtu.be/yUdE9oj3sWk); Wonder Sessions workshop [youtu.be/ttgNFJ25xfU](https://youtu.be/ttgNFJ25xfU); Kalshi cost ([getcoai](https://getcoai.com/news/kalshis-nba-finals-ad-costs-just-2k-using-googles-ai-video-tool/)); Popeyes ([getcoai](https://getcoai.com/news/popeyes-uses-ai-to-create-mcdonalds-diss-track-in-just-3-days)).
- Coke 2025 survey ([Tom's Guide](https://www.tomsguide.com/ai/ai-image-video/coca-cola-turns-to-ai-for-its-christmas-ad-in-2025-sparking-mixed-reactions)); Svedka ([Adweek](https://www.adweek.com/creativity/svedka-bets-on-ai-and-its-fembot-to-make-super-bowl-history/), [eMarketer](https://www.emarketer.com/content/svedka-bets-on-ai-super-bowl-brands-gauge-consumer-sentiment)); Super Bowl LX AI ads ([Hellowarrant](https://www.hellowarrant.com/blog/super-bowl-2026-ai-ads-backlash), [Artlist blog](https://new-blog.artlist.io/blog/super-bowl-2026-ai-ads/)).
- Luma Dream Brief finalists ([LBB](https://lbbonline.com/news/21-AI-Spots-Lumas-Dream-Brief-Cannes-Lions)); Deepal credits ([AotW](https://www.adsoftheworld.com/campaigns/deepal-s07-ai-product-video)); Under Armour ([Euronews](https://euronews.com/next/2024/03/15/massively-concerning-under-armours-ai-powered-sports-commercial-sparks-controversy)).
