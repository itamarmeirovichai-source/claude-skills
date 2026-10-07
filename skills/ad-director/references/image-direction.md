# Image direction: think like a product photographer + set designer

The start frame decides 80% of the final video. A weak still makes a weak clip, whatever the video model.
**Rule: no still goes to video unless it scores ≥ 8/10 on the rubric (§6). Below that, rewrite the prompt and regenerate.**

## 1. Why the reference (CELSIUS watermelon) works and our TIDEWATER test did not
| Element | CELSIUS reference (campaign) | Our A1 can (catalog) |
|---|---|---|
| Story in the frame | The flavor is the set: watermelon slabs, wet surface, "summer" | Can on an empty backdrop. No story |
| Surface | **Mirror acrylic** with a perfect reflection, so the product appears twice | Flat paper sweep |
| Liquid detail | **Condensation beads on the can** plus **juice-tinted droplets/puddles on the floor** that refract the background | None |
| Color | **One gradient (coral → peach)** echoing the flavor, plus complementary green rind accents | Beige, neutral, and the turquoise can doesn't relate to it |
| Light | Hard key from top-left (glints on the drops), soft fill, backlit translucency in the watermelon flesh | Soft even light, no specular highlights |
| Lens/angle | Slightly low, ~70–100mm, shallow depth of field. Props in the foreground blur and frame the can (depth layers) | Eye level, everything in focus, no depth |
| Composition | Can slightly off-center, props cut by the frame edges (the world continues), diagonal lines | Centered, isolated |
| Imperfection | Organic irregular puddles, a few seeds, real texture | Sterile |

**The formula:** product hero + **flavor/benefit-as-set** + **reflective or wet surface** + **liquid detail** + **one bold gradient** + **hard specular key and rim** + **foreground blur layers**.

## 2. The studio vocabulary that changes results
- **Light setups:**
  - hard key 45° top-left + white bounce fill
  - rim/edge lights on both sides (glass and can edges)
  - backlight through liquid (translucency)
  - gobo shadows (palm leaves, window blinds)
  - colored gels (teal rim / magenta fill)
  - softbox reflection stripe on cylindrical products
  - a "light painting" glow underneath
- **Surfaces:**
  - mirror acrylic
  - wet black slate
  - shallow water with ripples
  - crushed ice bed
  - sand with footprints
  - terrazzo
  - brushed steel
  - colored seamless paper with a hard horizon
  - stacked fruit
  - a cracked-earth heat texture
- **Liquid and particle details:**
  - condensation beads (macro, varied sizes)
  - single rolling drops leaving trails
  - frost bloom
  - splash crown (frozen at 1/8000s)
  - suspended droplets
  - fizz bubbles
  - mist and steam
  - flying ingredient slices
  - powder bursts
- **Camera:**
  - 100mm macro (details)
  - 85mm (hero)
  - 24mm low angle (scale and power)
  - top-down flat-lay
  - Dutch tilt 10° (energy)
  - f/2.8 (dreamy) vs f/11 (sharp commercial)
  - high-speed freeze
- **Color theory:**
  - one dominant gradient from the flavor
  - complementary accent (watermelon red vs rind green)
  - avoid neutral beige unless the brand is "minimal luxury"
- **Composition:**
  - rule of thirds
  - leading diagonals
  - foreground props cut by the frame
  - negative space at the top for supers (safe zones!)
  - reflection doubling
  - scale contrast (tiny product, huge prop, or the reverse)

## 3. 16 hero-shot recipes (pick by brief, rotate, never repeat for the same client)
1. **Reflection pool:** product on mirror acrylic, flavor props, juice droplets, gradient sky.
2. **Ingredient explosion:** product center, ingredients frozen mid-air radiating out, high-speed.
3. **Splash crown:** product dropping into its own liquid, crown splash, backlit.
4. **Ice cave:** product embedded in a cracked ice block, blue rim light, frost bloom.
5. **Heat vs cold:** half the frame cracked desert / half frost, product on the border.
6. **Levitation:** product floating above its surface with a perfect shadow, ingredients orbiting.
7. **Monochrome set:** everything (props, background, floor) in the product's color, product pops by material.
8. **Miniature world:** tiny people/vehicles interacting with a giant product (scale play).
9. **Architectural pedestal:** product on a sculptural plinth, hard sun, long shadows, Bauhaus shapes.
10. **Liquid portrait:** pour stream frozen into a sculptural shape (a wave, a spiral).
11. **Nature fusion:** product growing from its source (only if true: no "made from fruit" claims for flavored products).
12. **Lifestyle macro:** hand (no face) holding the product, sweat or condensation, sun flare, shallow DOF.
13. **Stacked/grid:** many units in a graphic pattern with one hero breaking the pattern.
14. **Retro/print ad:** 1970s magazine look, grain, warm flash, bold set dressing.
15. **Night neon:** wet street reflections, neon color spill on the product edges.
16. **Surreal juxtaposition:** product where it shouldn't be (in a snow globe, on the moon, in a museum vitrine).

## 4. Prompt formats per image model (Higgsfield API endpoints)
### Marketing Studio Image 2.5 Flare (`marketing-studio/image/flare`): GPT-Image-class, best for text on packaging
- Write like a **creative brief to a photographer**, full sentences.
- Order: **scene/set → product (with exact label text in quotes) → light → lens/angle → mood/color → constraints**.
- Exact on-pack text goes **in quotes with font and placement**: `the word "TIDEWATER" in bold black condensed caps on a white band`.
- Add `quality: "high"`, `resolution: "2k"` for heroes (1k for drafts). Use `image_urls` for product references (pass B).
- **Two-pass rule:**
  - **Pass A** builds the art-directed scene with a generic product.
  - **Pass B** (`image_urls=[packshot, passA]`): "Replace the can in image 2 with the exact can from image 1 (same label, colors, proportions); match the lighting, reflections and condensation; change nothing else."

### Soul v2 (`higgsfield-ai/soul/v2/standard`): photoreal people and lifestyle, $0.006
- Short, photographic, people-first. Name the **camera/film look** ("shot on Portra 400, 35mm, natural window light").
- Use it for **faces, hands and lifestyle plates**. Not for exact label text (composite the real label later).
- Use `batch_size: 4` for cheap exploration, then pick the best.

### Universal hero template (copy, fill in, keep the order)
```
[SET] {surface} with {props tied to flavor/benefit}, {background: gradient/location}, {atmosphere: mist/heat haze/dust}.
[PRODUCT] {exact product description}; label reads "{TEXT}" in {font}, {placement}; {material: matte/glossy/brushed}; {liquid detail}.
[LIGHT] hard key from {direction} creating specular glints on the droplets, {rim/backlight}, {fill}; {gel colors if any}.
[CAMERA] {lens}mm, {angle}, f/{stop}, {depth layers: blurred foreground props}, {motion freeze if any}.
[COLOR & MOOD] dominant {gradient}, accent {complementary}, {mood words: refreshing, punchy, premium}.
[COMPOSITION] 9:16, product at {position}, negative space top 20% for text, props cut by frame edges.
[CONSTRAINTS] photorealistic commercial photography, no extra text or logos, label legible and unchanged, natural imperfections.
```

## 5. Worked rewrite: TIDEWATER (fictional electrolyte water, "Florida heat")
**Before (catalog):** "Studio packshot of a single slim can on a seamless pale-sand backdrop…"
**After (campaign), recipe 1 + 5:**
```
A sun-scorched Florida sidewalk slab split diagonally: the left half is cracked, bleached concrete with heat haze, the right half is glassy turquoise ice with frost feathers spreading toward the left. Standing exactly on the border: a slim 12 oz aluminum can, matte turquoise with a crisp white band reading "TIDEWATER" in bold black condensed capitals and "ELECTROLYTE WATER" in small caps beneath; dense condensation beads and two rolling drops on the can, a thin frost ring at its base. A small puddle of meltwater mirrors the can. Hard late-afternoon sun from the upper left throws long palm-frond gobo shadows across the hot side and sparkles on the ice; cool cyan rim light on the right edge of the can. 90mm, low angle 15°, f/5.6, a blurred palm frond crossing the top-left foreground. Dominant palette: bleached coral-to-turquoise, accent lime. Vertical 9:16, can on the right third, empty sky gradient in the top 20%. Photorealistic high-end beverage advertising photography, real textures, no extra text or logos, label perfectly legible.
```

## 6. Image QC rubric (score each still, regenerate if < 8/10 or any hard fail)
| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| **Label/product fidelity** (hard fail if wrong text) | wrong | small drift | exact |
| **Light realism** (specular, shadows, rim) | flat/CG | ok | studio-grade |
| **Material and liquid realism** | plastic | ok | tactile |
| **Story/set** (flavor or benefit visible) | none | generic | specific and clever |
| **Composition** (depth layers, safe zones, 9:16) | flat/centered | ok | magazine-grade |

**Regenerate protocol:**
1. Write the 2 weakest criteria as fix instructions ("add rim light from right", "props must cut the frame edge").
2. Change only those.
3. Regenerate 2–4 variants.
4. Max 3 rounds. Then change the recipe, not the seed.
