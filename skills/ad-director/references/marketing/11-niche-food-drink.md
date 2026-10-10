# 11 — Niche playbook: beverages, coffee & tea, snacks, non-alcoholic spirits

This builds on 00, 02, 05, 06, 09 and 10. Researched 2026-10-07. Frame sheets for 16 real ads are in `research/ai-video-reels/youtube/frames/niches/food-drink/sheet0-3.jpg`.

## What real ads look like (frames we looked at)
- **Liquid Death "Exploding Heads"** ([YT](https://youtu.be/tEh050NGnVM)) parodies a pharma clinic: a "board-certified surgeon" lower third, mannequin heads and a fat purple super. The joke is the category's own clichés.
- **Poppi 2026** ([YT](https://youtu.be/LCZTDi4SCCU)) uses worm's-eye can macros against the sky, heavy condensation and can towers, all in a pastel CG world. **Poppi SB 2025** ([YT](https://youtu.be/4LDn46rb_gc)) is warm 70s-stock lifestyle with an overhead cooler of cans and three bouncing claim words: "5g sugar · prebiotics · no baggage".
- **Seedlip** ([Social](https://youtu.be/cwoTCF97TAs), [Spice 94](https://youtu.be/Pm3Izz02aGw)) uses a sage period set with the bottles on a draped plinth. The recipe film is a lavender-grey seamless, one highball, a hand placing a twist, and a serif recipe on the right third.
- **Blue Bottle Studio** ([YT](https://youtu.be/-eDpglaKrUg)): warm oak, gooseneck pour.
- **KitKat 2025** ([YT](https://youtu.be/w-uoWfFIXtc)) is a red seamless: the bar snaps with crumbs frozen mid-air, then a macro of the wafer layers.
- **Lay's** ([YT](https://youtu.be/D4EkP55njL4)) and **Doritos** ([YT](https://youtu.be/sIAnQwiCpRc)): filmic narrative, teal-green grade, bag as story prop.
- **Coca-Cola "Holidays Are Coming" 2025** was made with AI: 70,000 clips, about 100 people. Viewers spotted trucks with extra wheels and called it slop ([RetailBoss](https://retailboss.co/coca-colas-ai-generated-holiday-campaign-and-the-backlash-that-went-viral)). Never generate mechanical geometry in wide shots.
- **KitKat "Phone Break"** (VML Prague, Cannes Outdoor Grand Prix 2025) replaces phones with KitKats, with no copy ([WPP](https://www.wpp.com/en/case-studies/vml-and-openmind-kitkat-phone-break)).

**Signals**
- On TikTok, 70% of users are likelier to buy when the product is central, and 64% love product sounds ([TikTok](https://ads.tiktok.com/business/en/blog/elevate-your-food-and-drink-ads)).
- Poppi's best YouTube asset was a 9 s Short (5.3M views) built on tapping-and-fizz ASMR. "Limited edition" language drove conversions ([Pixability](https://www.pixability.com/youtube/healthy-soda-wars-on-youtube-what-every-cpg-advertiser-can-learn/)).

## Shared rules

### Liquid physics
In HumanSignal's Sep 2026 test, Seedance 2.5, Veo 3.1 and Kling 3.0 Pro all failed a water pour. Kling filled both glasses, creating water from nothing ([NovoAds](https://novoads.ai/en/blog/ai-video-physics-test)). Workarounds:
1. **Hide the transfer.** Show a stream macro with no source or target level in frame (≤2 s), then cut to the glass already full.
2. **Use states, not events.** Kling `image_url` = the before, `last_image_url` = the after. Cut before the settle.
3. **Lean on reliable liquids:** condensation beads, carbonation, steam, a rim drip, an ice drop with a ring.
4. **Bubbles:** write "distinguishable spherical bubbles". For cola, "dense medium bubbles clinging to glass". Max 3 modifiers ([Hailuo](https://hailuoai.video/pages/knowledge/realistic-beverage-bubble-dynamics-ai-video)).
5. **Splash crowns:** make a Flare still plus 2 s of Kling micro-motion. Never run a 5 s splash; the foam goes uniform.

### Food truth
- The FTC treats a misleading food mock-up as deception (Campbell's marbles precedent). An AI chip or bar that looks better than the real one is the same problem. Generate from the real product photo, and keep the size, colour and inclusions true.
- The FDA's new "healthy" definition took effect Feb 2025, with compliance by Feb 2028, and caps added sugar, sodium and saturated fat ([Hogan Lovells](https://www.hoganlovells.com/en/publications/fda-issues-final-%E2%80%9Chealthy%E2%80%9D-rule)).
- Claims go on screen as **facts** (grams, mg, roast date, 0.0%), never as benefits.

### Ban list (on every prompt)
`no CGI render look, no glossy plastic liquid, no perfect symmetry, no centred product on mirror floor, no floating product without cast shadow, no splash or fruit explosion, no flare unless source in frame, no HDR, no oversaturation, no digital sharpening, no readable text except the label, no extra cans/bottles, label never warps.`

---

## 1. BEVERAGES (energy / soda / water / functional)
**Visual grammar**
- **Shots:** can on ice, condensation macro, worm's-eye can against the sky, tab crack with a vapour puff, overhead cooler, a hand pushing the can into the lens, carbonation in a glass.
- **Light:** hard sun or a single hard backlight, with a black flag behind so the beads read as highlights.
- **Colour:** one flavour colour plus white (Poppi), or black plus one acid colour (Liquid Death).
- **Textures:** frost, matte aluminium, crushed ice, wet concrete.
- **Pacing and type:** 1–1.5 s cuts; bold sans type with at most 3 claim words.
- **Sound:** crack and hiss, a fizz bed, ice clink. This is the most ASMR-dependent category.

**Why people buy:** taste plus a permission fact (zero sugar, mg of caffeine, grams of fibre), limited flavour drops, and identity.

**Traps**
- Poppi paid **$8.9M** over its "gut health" claims ([Brewbound](https://www.brewbound.com/news/poppi-reaches-8-9m-settlement-over-gut-health-claims)). Say "9g fibre", not "fixes your gut".
- Celsius paid $7.8M over "no preservatives" (`research/.../packages/celsius-watermelon-lemonade`). No fat-burn claims either.
- Energy drinks: no minors. ABA members pledge not to market to under-12s ([BeverageDaily](https://beveragedaily.com/Regulation-Safety/energy-drinks-teenagers-adolescents-children-U18-U12-Monster-Red-Bull)). England bans sales of >150 mg/L drinks to under-16s from April 2027 ([ITV](https://www.itv.com/news/2026-07-16/under-16s-in-england-to-be-banned-from-buying-energy-drinks)).
- Never show energy drinks mixed with alcohol.
- Fruit on screen must not imply juice the product doesn't contain.

**Formats**
- **A. Crack & Cool ASMR (15 s):**
  - 0–1.5 s: frosted macro, hiss pre-lap
  - 1.5–3 s: tab crack and puff
  - 3–6 s: carbonation
  - 6–9 s: ice drop
  - 9–12 s: hand lifts the can into the sun
  - 12–15 s: hero, 3 words, CTA
- **B. Category parody (20 s):**
  - 0–3 s: a deadpan cliché
  - 3–12 s: absurd escalation, product visible
  - 12–17 s: straight packshot
  - 17–20 s: dry super
- **C. Flavour world (15 s):**
  - 0–2 s: worm's-eye can
  - 2–8 s: three colour-matched ingredient macros
  - 8–12 s: overhead lifestyle
  - 12–15 s: can row, "limited", CTA

**BIG IDEAs.** The fictional brand is **SOLSTICE**, a sparkling yuzu energy drink with 100 mg of caffeine.
1. **"Bottled dawn."** In a dark 5 a.m. kitchen, the crack of the can sends a gold sunrise slash sweeping across the room.
2. **"Coldest thing in Florida."** The can lands on scorching Boca concrete. Frost creeps outward from its base and the heat shimmer dies.

**Recipe**
- **STYLE HEADER:**
  `9:16 commercial, ARRI Alexa 35, Cooke S4 + 100mm macro, 1/50 shutter, Kodak Vision3 250D look, one hard motivated key (sun or 3200K slash), deep falloff, colour world yuzu-gold #F2B705 + off-white + charcoal, fine grain, slight halation. @image_1 is the exact SOLSTICE can, source of truth: slim 12oz matte white, gold sun-ring logo; never becomes a bottle.` + ban list.
- **Stills.** Use Flare with the product ref for every product shot, and add "subject on left third, three-quarter angle" because Flare centres things. Use Soul Cinema for the empty sets.
  1. "Extreme macro of @image_1 shoulder on crushed ice, uneven beads, two running trails, a dry patch, one smeared fingerprint, hard backlight, black flag."
  2. "Dark tiled kitchen 5 a.m., @image_1 on worn oak, left third, thin warm sunrise slash touching its edge, room in blue predawn, kettle out of focus."
  3. "Highball of pale gold sparkling liquid, distinguishable spherical bubbles in vertical chains, ice with trapped air, wet ring on stone."
  4. "POV adult hand, a few arm hairs, lifting @image_1 toward lens against noon sky and palms, sun visible at frame top."
  5. "@image_1 on rough ice block on sun-bleached concrete, cast shadow, heat shimmer behind."
- **Motion.** Kling 3.0 Pro, 5 s, trimmed to 2–3 s.
  1. "Only condensation moves: two beads slide and merge; handheld breathing; full speed."
  2. Start = the dark kitchen; `last_image_url` = the same kitchen flooded gold. "Light slash sweeps right to left, can fixed, push in 5%."
  3. "Bubbles rise, one ice cube bobs; locked macro."
  4. "Hand lifts can into lens; focus lands a beat late."
  5. "Frost spreads from the base across concrete; slow 10° arc left."
  - For the parody format (people and blocking), use Seedance 720p multi-shot instead.
- **ElevenLabs**
  - **Music:** "0–1.5 s near-silence; downbeat hit on crack; 1.5–12 s minimal house 118 BPM, marimba hook; 12 s breath; 12.5–15 s two-note marimba sonic logo."
  - **SFX:** close can crack and hiss, ice into glass, 6 s fizz bed, frost crackle.
  - **VO:** `[calm, warm] Sunrise. In a can. [short pause] SOLSTICE.`
- **Edit**
  - Cut on the crack, and ramp the ice drop 100→40→100%.
  - Set claim words in Heebo Bold caps, tracking +80, bottom-third safe.
  - Desaturate everything except the gold. Keep the bead highlights unsoftened.
- **Budget:** 5 Flare $1.50 + 2 Soul $0.01 + 5 Kling $2.40 + Seedance 480p 8 s draft $1.68 + $3 retakes ≈ **$8.60**.

**AI weak spots**
- **Label warps:** orbit no more than 15°, and comp the label in post if it drifts.
- **Fingers on the tab:** keep the thumb at the frame edge and cut to the puff.
- **Uniform beads:** add "uneven, dry patch".
- **Can towers:** make them a still with micro-motion only.

---

## 2. COFFEE & TEA
**Visual grammar**
- **Shots:** bean cascade, grinder plume, tiger-striped espresso streams, backlit steam, gooseneck spiral, milk clouding iced coffee, matcha whisking, leaves unfurling, a roast-date stamp, a hand cupping the mug.
- **Light:** one window key (5600K) plus a tungsten practical in frame. Steam is backlit against black.
- **Colour:** umber, oak and cream, plus one accent.
- **Textures:** crema micro-bubbles, chaff, oily bean sheen, a chipped glaze.
- **Pacing and type:** 2–3 s, ritual-paced cuts; refined serif type.
- **Sound:** grinder, tamp knock, steam-wand hiss, spoon on porcelain, rain.

**Why people buy:** ritual and calm, craft identity (origin, freshness), energy, and cost per cup against the café.

**Traps**
- "Organic" and "Fair Trade" need certification marks.
- No antioxidant or metabolism claims.
- Origin must match the real lot.
- No AI "farmer testimonials" (FTC fake-review rule).

**Formats**
- **A. Ritual ASMR (20 s):**
  - 0–2 s: bean cascade
  - 2–5 s: grinder plume
  - 5–9 s: espresso streams
  - 9–13 s: steam by a window
  - 13–16 s: hand cups the mug
  - 16–20 s: bag, roast date, CTA
- **B. Farm → cup (15 s):** misty ridge → cherries in a palm → roaster drum dumping smoking beans → cup steam → end card.
- **C. Café vs home (15 s, split screen):** a $7 café cup against the home pour in the same light → "$1.10 a cup" → bag → CTA.

**BIG IDEAs.** The fictional brand is **OBRA Roasters**: single-origin Huila, roasted to order.
1. **"The mountain in your cup."** The camera rises into the espresso steam, and the steam becomes the dawn cloud over the ridge where the beans grew.
2. **"48 hours from fire."** Beans tumble smoking from the roaster drum into the bag, and the stamp lands: "ROASTED TUE · AT YOUR DOOR THU."

**Recipe**
- **STYLE HEADER:**
  `9:16, Alexa Mini LF, Zeiss Supreme 50mm + 100mm macro, Kodak 5219 look, single window key from left 5600K + 2700K tungsten practical in frame, deep shadows, colour world umber + oat + terracotta #B5532E, visible grain, steam backlit against black. @image_1 = exact OBRA kraft bag with terracotta band.` + ban list.
- **Stills**
  1. "Glossy dark beans falling from top-left into steel hopper, chaff flakes, 1/1000 freeze, hard side light."
  2. "Bottomless portafilter, two tiger-striped streams meeting crema in a small chipped ceramic cup, steam wand blurred behind."
  3. "Black stoneware cup on stained walnut bar, right third, dense steam backlit by rain-streaked window."
  4. (Soul Cinema) "Misty Huila coffee ridge at dawn, clouds pooling in valley, shade trees, no people."
  5. "@image_1 on linen, three-quarter, scoop of beans spilling, roast-date stamp on band, morning slash."
- **Motion**
  1. "Beans keep falling and scatter, full speed."
  2. "Streams flow steadily, crema rises millimetres; cup never fills from empty." Keep it at 2 s.
  3. Start = the cup, end = the ridge: "camera rises into the steam, steam thickens into cloud; one continuous push up."
  5. "Two beans roll off the scoop; slash drifts."
  - **Tea:** leaves unfurling works well. Keep the matcha whisk ≤3 s, because the tines deform.
- **ElevenLabs**
  - **Music:** "0–4 s rain room tone; felt piano 70 BPM; bass at 9 s; 16 s sustained chord; two-note piano logo."
  - **SFX:** burr grinder, portafilter knock, wand hiss, spoon clink.
  - **VO:** `[soft, unhurried] Grown on a mountain. [pause] Roasted Tuesday. [pause] OBRA.`
- **Edit**
  - 2–3 s cuts, with a dissolve only for the steam→mountain transition.
  - Origin set in Cormorant Garamond italic.
  - Warm LUT, halation on the window, full film chain plus gate weave.
- **Budget:** 4 Flare $1.20 + 2 Soul + 5 Kling $2.40 + $2.40 retakes ≈ **$6.00**.

**AI weak spots**
- **Latte-art pours spawn milk:** show the finished rosetta and a spoon breaking it.
- **Cup filling:** show the streams only.
- **Grinder and portafilter geometry warps:** lock the camera, macro only.
- **Mug hands:** one hand, fingers partly out of frame.

---

## 3. SNACKS & FOOD
**Visual grammar**
- **Shots:** the snap with crumbs in mid-air, a cross-section macro (ridges, salt, layers), a bag tear, seasoning dust, a hand pinching from a bowl, a cheese pull, the bag on a couch.
- **Light:** one raking hard key on a brand-colour seamless (KitKat red).
- **Textures:** crumbs, oil sheen, salt crystals.
- **Pacing and type:** the fastest category, 0.8–1.5 s punches; chunky type.
- **Sound:** the crunch is everything, plus the rip and crinkle.

**Why people buy:** a craving trigger, flavour novelty and limited editions, sharing, and permission angles (protein, baked).

**Traps**
- Food truth: size and inclusions must match the product.
- "Healthy" and "high protein" have thresholds.
- Kids' snacks fall under CARU (no pester appeals).
- Avoid bites: AI mouths are uncanny (02 rates this AI risk at 3).

**Formats**
- **A. Snap (15 s):**
  - 0–1 s: snap with frozen crumbs
  - 1–4 s: cross-section
  - 4–7 s: seasoning dust
  - 7–10 s: hand takes one
  - 10–12 s: bag tumble
  - 12–15 s: bag on the seamless, CTA
- **B. Visual swap (15 s, the KitKat "Phone Break" logic):** the snack replaces an everyday object, wordless for 10 s, then the logo and line.
- **C. Flavour build (20 s):** five ingredient macros of 1.5 s, each landing on the chip → crunch → bag → "limited".

**BIG IDEAs.** The fictional brand is **CRAG**: thick-cut kettle chips.
1. **"The loudest chip."** One chip snaps in a hushed library, and concentric ripples cross the water glass on the desk (the Jurassic Park beat). The claim is made visible without mouths.
2. **"One potato, one chip."** One thick slice falls from the knife beside a dirt-flecked potato and lands as a golden, salted, curled chip. Use Kling start and end frames.

**Recipe**
- **STYLE HEADER:**
  `9:16, high-speed look, Laowa 24mm probe + 100mm macro, single hard raking key 3200K from right, black negative fill left, slate seamless with ochre #C8862A accent, salt crystals and oil sheen visible, fine grain. @image_1 = exact CRAG matte black bag, ochre mountain logo; foil creases natural.` + ban list.
- **Stills**
  1. "Thick ridged kettle chip snapping mid-air, exactly 30 jagged crumbs and salt flecks frozen, left third, cast shadow below."
  2. "Extreme macro of chip surface: blistered oil pockets, coarse salt, one paprika fleck, falloff to ochre."
  3. (Soul Cinema) "Hushed old library, green lamps, oak desk, glass of water foreground right."
  4. "Scarred end-grain board, dirt-flecked potato, one thick slice falling from a chef knife."
  5. "@image_1 on its side, a dozen chips spilling across slate, three-quarter."
- **Motion**
  1. "Crumbs fly outward and fall with gravity; halves rotate slightly; no slow-mo easing."
  3. "Concentric ripples spread across the water three times; glass motionless; push in 5%."
  4. Start = the raw slice falling, end = the cooked chip resting; "no hands".
  5. "One chip slides off the pile; tiny handheld drift."
- **ElevenLabs**
  - **Music:** "0–1 s silence; kick synced to crunch; stomping drum + guitar riff 95 BPM; dead stop at 10 s for library silence; riff returns 12 s; two-hit logo."
  - **SFX:** dry close chip snap, bag rip, library hush with a clock tick, water tink.
  - **VO:** `[whisper, deadpan] Sorry. [pause] [normal] CRAG. Thick-cut loud.`
- **Edit**
  - 1 s cuts; ramp the crumbs 30→100%.
  - Oversized Heebo Black, slightly rotated.
  - Boost only the ochre.
- **Budget:** 4 Flare $1.20 + 1 Soul + 5 Kling $2.40 + $2.50 retakes ≈ **$6.10**.

**AI weak spots**
- **Chewing:** avoid it.
- **Cheese pulls go rubbery:** keep them ≤1.5 s and use start and end frames.
- **Crumbs multiply:** give exact counts.
- **Bag text melts when crinkled:** keep the bag still and put the crinkle in the SFX.
- **Hands fuse with chips:** one pinch at the frame edge.

---

## 4. NON-ALCOHOLIC SPIRITS / MOCKTAILS
**Visual grammar**
- **Shots:** the bottle among its botanicals (Seedlip), the recipe build (ice, measure, a twist expressed over the glass), a clear-ice macro, bitters bleeding into tonic, a coupe at dusk, hands clinking, the bottle backlit.
- **Light:** a tungsten backlight so the liquid glows (05), plus a leaf gobo.
- **Colour:** muted botanical palettes (sage, apricot, aperitivo red).
- **Textures:** fractured clear ice, citrus oil mist, frosted rims, linen.
- **Pacing and type:** 2–3 s cuts; a small wide-tracked serif in a recipe-card layout.
- **Sound:** ice in a tin, stir-spoon tinkle, tonic fizz, low jazz.

**Why people buy:** belonging at social moments, adult complexity, a sober-curious identity, and clear mornings (claimed carefully).

**Traps**
- Meta allows NA products "as long as they do not depict alcohol or consumption" ([Meta](https://transparency.meta.com/policies/ad-standards/restricted-goods-services/alcohol/)).
- Retail media networks may treat NA as alcohol ([Kroger Prism](https://prism.8451.com/activation/help/content/resources-faqs/ad-policies/alcohol-beverage-policy.htm)).
- Therefore: no alcohol brands in frame, no visible sipping, target 21+, and no minors.
- No "hangover-free" or health guarantees; say "0.0%".
- No driving imagery, and handle recovery language with care.

**Formats**
- **A. Recipe card (15 s, the Seedlip Spice 94 model):**
  - 0–2 s: clear-ice crack
  - 2–5 s: stream macro
  - 5–8 s: tonic bubbles
  - 8–11 s: twist mist backlit
  - 11–15 s: glass beside the bottle, name of the serve
- **B. Botanical world (20 s):** five root, peel and herb macros in the brand colour → bottle backlit → serve → line.
- **C. Party, sharp (15 s):** dusk-rooftop bokeh → coupes clink (hands only) → bottle passed down the table → hero at sunset → "Order the tasting trio".

**BIG IDEAs.** The fictional brand is **NOCTE**: a bitter-orange aperitivo, 0.0%.
1. **"The whole night, in focus."** Through a coupe of amber NOCTE the party is a bokeh blur. As the glass lifts, a rack focus snaps the room crisp: clear-headed nights as literal optics.
2. **"Garden in the ice."** A clear cube with rosemary and orange peel frozen inside drops into the glass: the ingredient list, suspended in light.

**Recipe**
- **STYLE HEADER:**
  `9:16, Alexa 35, Cooke Panchro/i Classic 75mm, Kodak 5207 look, single 2700K tungsten backlight through the glass making liquid glow, leaf gobo on back wall, negative fill, colour world bitter-orange #D2611C + deep teal shadow + linen, fine grain, gentle halation. @image_1 = exact NOCTE squat apothecary bottle, cream label, orange wax seal, amber liquid.` + ban list + `no alcohol bottles, no wine glasses, no one drinking`.
- **Stills**
  1. "Clear ice cube on dark slate, rosemary sprig and orange peel frozen inside, internal fractures, trapped air, one chipped corner, backlit, right third."
  2. "Coupe of amber liquid foreground left, rooftop party at dusk as oval string-light bokeh, one smudge on rim."
  3. "Highball with clear ice, thin amber stream entering from top left, glass already two-thirds full."
  4. "Adult hand with a ring twisting orange peel over the glass, fine oil mist backlit."
  5. "@image_1 on travertine beside the finished serve, leaf gobo, cast shadow, three-quarter."
- **Motion**
  1. Start = the cube in tongs, end = the cube floating in the amber glass. Cut before the settle.
  2. "Glass lifts 10 cm, rack focus from glass to party which snaps sharp; handheld micro-sway."
  3. "Stream continues, surface ripples, no level change" (≤2 s).
  4. "Peel twists once; mist drifts in the light."
  5. "Gobo leaves sway; push in 5%."
- **ElevenLabs**
  - **Music:** "0–2 s ice cracking in silence; brushed-snare lounge jazz 88 BPM; vibraphone lift 11 s; three-note vibraphone logo."
  - **SFX:** ice into crystal, tonic fizz, peel twist, coupe clink, distant murmur.
  - **VO:** `[low, intimate] Stay for every moment. [pause] NOCTE. Zero proof.`
- **Edit**
  - The recipe super goes in Cormorant Garamond small caps on the right third, with "0.0%" on the end card.
  - Keep the teal-orange muted, and run the full film chain.
- **Budget:** 5 Flare $1.50 + 5 Kling $2.40 + a 6 s Seedance 720p party clip $2.76 + $2 retakes ≈ **$8.70**.

**AI weak spots**
- **Ice comes out as perfect glass:** add fractures and trapped air.
- **Coupe stems warp:** lock the camera.
- **Toasting hands morph:** max 4 hands, top-down, and a hard cut before contact.
- **Label softens:** comp it from the product ref.

---

## Cross-niche checklist
1. The frame-1 product macro, with its sound, is the hook.
2. One liquid event per shot, ≤2 s, with the transfer hidden.
3. One colour world and one sonic logo.
4. Claims as on-screen facts.
5. Build the BIG IDEA from start and end frames, not a physics simulation.
