# 17 — Hero Stills Mastery: product-exact, non-AI start/end frames

Researched 2026-10-07. Builds on `image-direction.md` (recipes, studio vocabulary, 10-point rubric), 05 (DP light vocabulary), 06 (ban list, imperfection, film chain), 10 (Higgsfield frame study) and 12 (API catalogue, templates A/B). It does not repeat them. Read those first.
Inferences are marked **[inf]**. YouTube transcripts were **IP-blocked (HTTP 429 / "sign in to confirm you're not a bot")** on this run, so video sources are cited from their published pages and summaries only.

## 0. The ten rules (read this if nothing else)

1. **A still is built, not generated.** Use separate passes: product asset → plate → composite → relight → repair → finish. Every 2025–26 workflow that holds labels splits the work into steps. "Asking for many things at once lowers prompt adherence", and skipping steps "produced distorted labels and invented details" [M1].
2. **Pick by job, not by brand.** Multimodal editors (GPT Image 2/2.5, Nano Banana Pro, Seedream 4.5/5, Qwen Edit) hold text and identity. Diffusion-aesthetic models (Midjourney, Flux, Soul) "optimise for aesthetics and won't hold these details" [M1]. On our API that means **Soul for plates, Flare/Sunburst for the product, Qwen Edit for surgical repair** (§1).
3. **Each reference gets one job, stated by index.** It also needs an explicit ban on what it must *not* contribute, such as its lighting or background [G1][H2].
4. **Throw away the reference's lighting by name.** Write "DISCARD the flat studio lighting of image 2". Then re-derive every light from the plate [H2].
5. **Put the preserve list in every pass**, verbatim, even when it repeats [O1].
6. **Make off-centre placement mechanical.** Use coordinates, a stand-in object, or an expand-canvas step (§4.5). Adjectives don't move the product.
7. **Name the material response, not "quality".** "Brushed metal streaks along the grain, polished glass shows caustics, matte cotton almost no sheen" [K1].
8. **Contact shadow and a single light logic** are the two cheapest realism wins. A floating product and a highlight that disagrees with its shadow are "the clearest sign of a composite" [K1].
9. **Never trust a creative upscaler with a label.** Upscale faithfully, then mask the real label back in (§2 step 7).
10. **Select pairwise, not by score alone.** Use n=4–8 candidates per shot, a hard-fail gate, then swap-order pairwise picks (§5).

## 1. Model landscape 2025–26 and what our Higgsfield API actually exposes

| Model (web name) | Strength for product stills | On our API? (per 12 §1–2, `GET /models` 2026-10-07) |
|---|---|---|
| **GPT Image 2 / 2.5** (Higgsfield "Flare", "Sunburst") | Label text, editing that "edits only what got asked for", 16 refs. Reviewers rate its metal/glass/fabric realism highly, but its liquids, splashes and smoke "fall behind" [R1]. It approximates fine-line logos [R2] | **Yes**: `marketing-studio/image/flare` and `/sunburst` (≤16 `image_urls`, 1k/2k/4k, explicit `aspect_ratio`) |
| **Nano Banana Pro** (Gemini 3 Pro Image) | Product consistency. 14 refs (≈6 objects at high fidelity) [G1][G3]. Creators: "GPT-Image best aesthetic, NB best product consistency" (router S41) | **No**: `503 model_disabled`. Web only |
| **Seedream 4.5 / 5** | 6–14 refs, batches of up to 9 consistent images, native 2K/4K [S1][S2] | **No** (404) |
| **FLUX.1 Kontext → FLUX.2** | Surgical edits. Text syntax `Replace '[old]' with '[new]'`. Colored annotation boxes mark the edit region [B1] | **No** |
| **Qwen Image 3 Edit** | 1–3 ordered refs, `seed`, `negative_prompt`. The 2511 line has low drift in unedited regions, built-in lighting control, and "industrial design / geometric reasoning" [Q1][Q2] | **Yes**: `alibaba/qwen-image-3/edit`, ≈$0.075. **Set `prompt_extend:false`** (default `true` rewrites prompts; risk of injected brands like Soul's `enhance_prompt`) [inf] |
| **Z-Image Turbo** | Fast, clean drafts [H3] | **Yes**: `z-image/turbo`, ≈$0.015, good for composition thumbnails [inf] |
| **Soul Cinema / Soul 2** | Off-centre, lived-in realism. Ignores image refs and can't spell (12 §0) | **Yes**: plates only |
| **Higgsfield web apps** (Product Photography: Relight & Shadow, Background Swap, Multi-Angle, Variant Sets, Upscaler 2K/4K, Outpaint resizer) [H3] | Useful one-click tools | **No** (12 §2: Relight/Upscale 404). Use them manually on the web, or replicate them as below |

**Tools inside this agent session [inf, connector-dependent, not tested here]:** the Adobe connector exposes `image_generative_expand` (outpaint), `image_fill_area` (inpaint), `image_select_subject`, `image_remove_background`, `image_apply_lens_blur`, `image_add_grain`. These cover the expand-canvas, repair, depth and grain steps when Higgsfield has no endpoint. Check the cost before you use them.

## 2. The stills factory (per shot)

**Step 1. Asset lock (once per product).**
- Shoot or obtain a **flat-lit packshot**: front, ¾, back, top, plus a **front-label crop as a separate PNG** (07 already covers the reference sheet).
- Add a **material card** in words: "frosted glass 3 mm wall, matte black PP cap with 24 vertical ridges, gold hot-foil wordmark, label paper uncoated".
- If you only have the label artwork, make a blank vessel first ("remove all design, plain matte black canister"). Then apply the label PNG in a separate step, specifying "label height, margins, text colour, finish, and how the label catches light" [M1].
- Store the **preserve block** (verbatim, reused everywhere):
  `PRESERVE: exact silhouette, proportions, cap, colours and every printed character of the product in image P; text reads "[EXACT TEXT]" spelled [E-X-A-C-T]; do not redraw, restyle, re-letter, mirror or add text; no other readable text, logos or watermarks.`
  Spelling tricky brand names letter by letter is OpenAI's own advice [O1].

**Step 2. Composition thumbnail (cheap).**
- Use Z-Image Turbo or Soul at 720p, batch 4, with no product, or with a **stand-in object of the same visual weight** (a matte black candle for a supplement jar) [M1].

**Step 3. Plate.**
- Use Soul Cinema 1080p (12 template A): off-centre and lived-in by default.
- Leave the stand-in in the plate where the product will go. "Replace the stand-in" inherits its shadow, perspective and scale. A lazy insert "can produce a sticker-like overlay" [M1].

**Step 4. Composite (Flare/Sunburst, `image_urls:[plate, packshot, label-crop]`).** The wording that works across vendors:
```
Image 1 is the scene: source of truth for composition, lens, light, colour and grain.
Image 2 is the product: source of truth for shape, materials and colours ONLY — DISCARD its studio lighting and white background, do not reproduce them.
Image 3 is the front-label close-up: authority for wording, typeface, weight, line breaks and layout.
Replace the [stand-in object] in image 1 with the product from image 2, same position (x 32%, y 66%), same scale (product height ≈ 38% of frame), turned 15° toward the window.
Relight the product only with image 1's light: [key source, side, Kelvin]; [rim]; soft contact shadow and a faint reflection on the [surface]; the product looks physically present, not composited.
[PRESERVE block]. Keep everything else in image 1 unchanged.
```
- The discard/relight phrasing comes from Higgsfield's own e-commerce prompt [H2].
- Run **2–4 variants at 1k/`medium`** first, then the chosen one at 2k/`high` (OpenAI: use `medium`/`high` for "small or dense text… identity-sensitive edits") [O1].

**Step 5. Relight / mood pass (only if needed).** There's no Relight endpoint, so do one of two things:
- (a) A Sunburst edit: "Keep composition, product and label identical; change only the light: …".
- (b) Local IC-Light (ComfyUI), with **frequency separation**: keep the low-frequency light from the relit result and the high-frequency texture and edges from the original. Known issue: IC-Light "may lose details at low denoising" [C1].
- Change one variable per pass. Kontext guidance warns against "drastic lighting adjustments" combined with other edits [B2].

**Step 6. Repair (surgical).**
- Use Qwen Image 3 Edit with refs `[still, label-crop]`, `negative_prompt`, a fixed `seed`, and `prompt_extend:false`.
- Text fixes use the Kontext-style literal: `Replace 'MAERA' with 'MAREA', same font, size, colour, curvature and position; change nothing else` [B1].
- For a hand, a contact shadow or a stray object, inpaint a masked area (Adobe `image_fill_area`) rather than regenerating the frame [inf].

**Step 7. Finish.**
- **Upscale faithfully.** Use Topaz Gigapixel or an equivalent faithful upscaler. Magnific "hallucinates… logos or product details can change", and Topaz itself steers Bloom away from photos [U1][U2].
- Then **mask the step-4 label region back in** at the original pixels (06 "mask original detail back in").
- Re-grain after any blur (06). Crop 3 % if Soul's gate corners appear (12).
- Export the exact video AR (9:16 at 1080×1920 or higher). Video models inherit the framing.

**Step 8. End frame.**
- Generate the end frame **from the approved start frame** plus the packshot, never from scratch (07). Use the same plate, seed and light.
- Wording: "Same scene and light as image 1; camera has moved [25° right / 30 cm closer]; product identical."

**Consistent multi-shot sets.** Two options:
- One shared plate family and one **LOCK** line (12 §4) across every shot.
- A **3×3 contact sheet** in one call ("9 distinct shots, consistent style across all 9 frames, thin white grid lines"). Split it, upscale each tile, and re-composite the product per tile, because the model "can still drift in product details" [N1].

## 3. What award-level product photography looks like, per niche → prompt blocks

Common to all niches: **one key logic, controlled reflections, the product separated by edge light, negative space planned for type, props that carry meaning, and nothing else.** Each block below plugs into `[LIGHT]/[SET]/[COMPOSITION]` of the universal template in `image-direction.md` §4.

### Fragrance
- **Real practice.** Build the background first ("off-white graduated glow"), then light the bottle [P2]. Add a **diffused strip for a linear gradient** on the glass, a **backlight flagged in the middle so two bright edges trace the bottle**, and a small top softbox for the cap and wordmark [P1][P3]. Glass reflects even soft sources as hard-edged shapes, which is why strips beat octaboxes [P1].
- **2026 campaigns.** Monochrome sets with *meaningful* sculptural props: Margiela's still lifes use "crushed paper set aflame, brittle tobacco leaves… roses pierced with silver pins". Gaultier used couture tools (scissors, thimbles, thread) under strobe [F1].
- **Block:** `Single vertical strip light behind diffusion camera-left drawing one clean linear gradient down the glass; backlight flagged at centre so both bottle edges glow; small top light lifting the cap; graduated [ivory→stone] backdrop lit separately; one symbolic raw-material prop ([note ingredient]) half out of frame; monochrome set in the juice colour; bottle on the left third, upper 35% clean for the line.`

### Drinks (glass, can, bottle)
- **Real practice.** "The majority of beverage ads… use backlighting" [D1].
- *Bright field* (lit background, dark cards define the edges) for translucent liquids. *Dark field* (black centre, lights at the edges) for bubbles and clear spirits. The two are often combined, with bright field at the rim and dark field on the body [D2].
- Studio condensation is a sprayed matte base plus syrup beads, and the ice is acrylic or silicone. **Prompt for "irregular beads of varied size, a few merged runs"**, not "perfect droplets" [D1][inf].
- **Block:** `Liquid backlit through a diffused panel so it glows from within; dark-field edges: black cards either side, thin white rim lines on the glass; condensation in irregular varied beads with two merged runs and a dry patch under the thumb-grip; clear acrylic-looking ice with trapped micro-bubbles; one clean vertical specular on the can, 1–2 small uneven hotspots left in.`

### Food
- **Real practice.** Key from behind at **10–11 o'clock** to rake texture and light translucent elements. Front light makes food flat. Shape with **subtractive black cards**, fill with a small white card, and use a mirror for one specular on a sauce or rim [FD1].
- **Block:** `Soft diffused window light from behind-left (10 o'clock) raking across the crust and glaze; black card deepening the near side; small white card filling; one specular glint on the sauce; crumbs, a torn edge, a drip on the plate rim; 45° or top-down; hero on the right third, cutlery cut by frame.`

### Beauty / skincare
- **Real practice.** Texture is the product: swatches, smears and macro sharpness, with fingerprints "magnified" [BT1]. In 2025–26 the trend moved from isolated packshots to context. Products sit on glass blocks, use asymmetric matte "brutalist" layouts with one pop colour, and get "less retouching" [BT2].
- **Block:** `A single smear of the [cream/serum] with visible ridges and an air bubble beside the jar, macro-sharp; jar on a frosted glass block; asymmetric matte set in [skin-tone neutral] with one [brand colour] accent; soft wrap light with a hard shadow edge from a small window gobo; real skin (if any) with pores, vellus hair, no beauty smoothing.`

### Tech
- **Real practice ("Apple look").** Hard directional light where "it goes exactly where you want it, and nowhere else" [T1]. Rim lights behind each side give bright edges, the background is pushed far back so it stays black, and flare is killed with flags [T1][T2]. Gradients come from placement and a white reflector, not from special modifiers [T2].
- **Block:** `Black seamless far behind; two gridded strip lights behind-left and behind-right drawing razor rim lines along the chamfers; one large reflector giving a soft gradient across the screen glass; screen content dim and plausible; micro-dust on the glass, one fingerprint smudge near a corner; 85mm, low ¾ angle; device on the lower-left third.`

### Fashion / accessories
- **Real practice** (from 10/11-fashion, adding): gesture over props. Let "skin, fabric, and light carry the story" [J1].
- **Block:** `Product worn or held mid-gesture, fabric with real creases and lint, stitching sharp; overcast-soft key with a hard sun slash across the background; editorial crop cutting the face at the mouth; 50mm, standing eye height; logo panel facing camera.`

### Jewelry
- **Real practice.** A large soft feathered key ("never aim it directly at the jewelry") and a white tent for clean metal reflections. **Black flags** define the metal edges. **Small hard snooted accent lights**, moved in millimetres, give the gem sparkle ("a whisper, not a scream"). Cross-polarise but keep some reflection. Use 5200–5600 K, minimal props, and a "best side" [J1][J2].
- **Block:** `Feathered large soft key, white surround reflected in the polished metal with two black flag lines defining the band edges; tiny hard pin lights from behind-above creating 3–5 crisp facet sparkles, not glitter everywhere; neutral 5500K; dark slate or warm stone, generous negative space; macro 100mm f/11, focus-stacked look, piece on the right third.`

## 4. Prompt-engineering specifics

### 4.1 Structure and length
- Google and Seedream converge on **scene sentences, most important first**. Use subject → setting → light → camera/composition → style, then constraints [G2][S1][P4]. Several guides report that earlier tokens weigh more (single-source claims, [P4][S3]).
- Google's commercial template: "A high-resolution, studio-lit product photograph of a [product] on [surface]. [Lighting setup] to [purpose]. Shot from [angle] to showcase [feature]. Ultra-realistic, sharp focus on [key detail]. [AR]" [G2].
- Length: **80–180 words for a generation, 40–90 for an edit** [inf]. Flare accepts ≤5,000 chars and Qwen ≈4,500 tokens [H1][Q1], but extra length mostly adds conflicts.

### 4.2 Reference-image wording (copy)
- `Image N is [role]: use it ONLY for [x]; do NOT take its [lighting/background/framing].` (Roles by index: Google, Seedream, OpenAI [G1][S1][O1].)
- `Match lighting, perspective, scale and shadows so the composite reads as a single capture.` [O1]
- `Change only [X]. Keep everything else in the image exactly the same.` [G2][O1]
- Text edits: `Replace '[old]' with '[new]'`, using the output casing [B1].
- Order the refs as they are named, product first [H1][M1]. Keep **≤5 refs** per call. More refs dilute identity (12 §4, Seedance) [inf for stills].

### 4.3 Negatives / ban list (stills-specific; 06 holds the generic one)
- Use hard bans only for: extra text, logos, watermarks, duplicate products, mirrored text, floating product, CGI sheen, chrome spheres.
- OpenAI's photoreal guidance explicitly says to **avoid** "cinematic lighting, dramatic color grading, or stylized composition" and to add "No glamorization, no heavy retouching" [O1]. Use this for the realism tier, and drop it for the glossy beauty/drinks tier.
- Qwen has a real `negative_prompt` field. Flare and Grok don't, so put bans in the prompt.

### 4.4 Aspect ratio
- Always send AR explicitly. Flare `auto` gives a square, Qwen defaults to 1:1, Grok defaults to `auto` [H1][Q1].
- Generate at the **video AR**. A 1:1 frame cropped to 9:16 loses the negative space you planned.
- For 16:9 + 9:16 deliverables, compose 9:16 first, then outpaint sideways [inf].

### 4.5 Getting off-centre compositions (escalating)
1. Coordinates plus a proportion: "product at x 30% y 66%, height 38% of frame; the frame centre stays empty" (12 B).
2. Name the empty area and what it is for: "large empty area of [surface] on the right for headline" (Google's negative-space advice [G2]).
3. Use a stand-in object in the plate (§2). The compositor replaces it in place.
4. **Expand canvas.** Generate tight and centred, then outpaint on one side so the product lands on a third. Outpainting adds space but doesn't move the subject, and extensions should be modest [X1]. Use Adobe `image_generative_expand` or the Higgsfield web Outpaint [H3].
5. Use a foreground occluder cut by the frame (a hand, a leaf, a glass rim). It breaks symmetry and adds depth.

### 4.6 Imperfection tokens that survive (name the object, the place, the amount)
- Use "one fingerprint smudge on the lower-right shoulder", "two merged condensation runs", "a dry patch where the thumb was", "dust motes in the backlight", "a crumb on the rim", "lint on the knit", "a hairline scratch on the cap", "1–2 uneven hotspots left in".
- Vague "imperfect/messy" fails (06).
- Put imperfections **off the label**. Text stays pristine.

### 4.7 Camera / lens tokens: what the evidence says
- Controlled tests are scarce. A fixed-seed Midjourney study found many camera terms do little, and recommends plain "photo of…" [L1]. OpenAI says camera specs are "interpreted loosely… for overall look" [O1].
- Anecdotally, **aperture (f/8 vs f/1.8) and focal-length class (macro/wide/telephoto)** change depth of field and perspective. ISO and shutter do nothing [L1].
- **Our rule [inf]:**
  - Keep focal class + aperture + camera height/angle + distance.
  - Write the *visible result* too ("background melts into soft blur, label razor-sharp").
  - Drop ISO, shutter, sensor names and "8K".
  - Camera body names help Soul's film look but bring gate corners (12).

## 5. QC rubric (vision-model automatable) and selection protocol

Run it **before** any video spend. It extends `image-direction.md` §6 (taste/story) and `qc-rubric.md` (clips) with still-specific forensic checks.

### 5.1 Inputs to the judge
For each candidate send the still, the packshot, the label crop, the shot brief and a **2× crop of the label region** (the judge must check the text at 200 % [K1]). The judge must also **transcribe the label text** before scoring. Transcription-then-compare catches near-misses ("MAERA") that a holistic glance misses [inf].

### 5.2 Hard gates (any FAIL → discard, no score)

| Gate | Check (judge answers yes/no with evidence) |
|---|---|
| G1 Text | Transcribed label == reference string (case, accents, line breaks). No mirrored, duplicated or extra text anywhere |
| G2 Geometry | Silhouette, cap, proportions match the packshot (overlay at the same scale; IoU of the masks ≥0.9 if run in code [inf]) |
| G3 Colour | Brand colour ΔE ≤ 5 vs packshot on the label area, after white-balance compensation [inf] |
| G4 Count | Exactly the intended number of products. No ghost duplicate in reflections |
| G5 Anatomy | If hands: 5 fingers, nails, plausible grip, no fingers through the product |
| G6 IP | No real third-party logos or brands in the background |

### 5.3 Scored criteria (0–2 each, /20; ship ≥16 for heroes, ≥14 for inserts)
1. **Light logic.** One direction across the highlights, shadows and reflections. Shadow softness fits the stated modifier [K1].
2. **Contact and grounding.** A contact shadow and/or a reflection where the product meets the surface. No hover [K1].
3. **Material response.** Glass, metal, paper and liquid behave correctly. No plastic sheen on matte surfaces [K1].
4. **Reflections.** They show the scene, not a different one, and there's one clean specular per surface [K2][05].
5. **Focus logic.** Label sharp. Depth of field consistent between product and scene [K2].
6. **AI tells absent.** No waxy skin, no repeated textures, no nonsense objects in the background, no perfect symmetry, no uniform droplets [K2][10].
7. **Composition.** Placement matches the brief. Negative space for type sits inside the platform safe zones.
8. **Niche craft.** The §3 block is visibly achieved (gradient strip, dark-field edges, 10 o'clock rake…).
9. **Story / brand-swap.** Props carry meaning (`image-direction` §6).
10. **Animatability [inf].** Clear space for the planned move. Nothing cropped that the move will reveal. No fine text near the edges that video will smear.

### 5.4 Selection protocol
1. **Generate n per shot:**
   - Heroes: n = 8 (2 prompt variants × 4).
   - Inserts: n = 4.
   - End frames: n = 4, derived from the winning start frame.
2. **Gate:** run §5.2. If fewer than 2 survive, fix the cause (§2 steps 4–6), not the seed. After 3 rounds change the recipe (`image-direction` rule).
3. **Score:** run §5.3 for each survivor and keep the top 4.
4. **Pairwise tournament.** For the top 4, run the judge on each pair **in both orders**. Pairwise judging beats pointwise for image generation (GenArena: 49.1 → 60.5 % accuracy for the same VLM) [E1]. But pairwise has position bias (≈23 % in one benchmark), so keep a verdict only if it agrees across the swap, and count the rest as ties [E2][E3].
5. **Robustness.** Judges can be swayed by distractors such as embedded text and stylisation [E4]. So the gates (deterministic checks) always run before taste, and the pairwise prompt says "ignore overlay text and grading; judge product fidelity, light logic and believability first".
6. **Human final** for heroes: top 2 at 100 % plus the label at 200 %; log why.

### 5.5 Judge prompt (pairwise, paste)
```
You are a commercial photo editor. Image P = product packshot; Image L = label crop (exact text: "[TEXT]").
Candidates A and B are proposed start frames for: [shot brief].
1) Transcribe the label text visible in A and in B exactly.
2) For each: list any physics errors (light direction, contact shadow, reflections, focus), any AI tells, any product deviations vs P.
3) Ignore colour grading and any text overlays when judging quality.
Answer JSON: {"A_text":..,"B_text":..,"A_fail":[..],"B_fail":[..],"winner":"A|B|tie","reason":"<25 words"}
```

## Sources

- **[G1]** Google, 7 tips for Nano Banana Pro: https://blog.google/products/gemini/prompting-tips-nano-banana-pro/
- **[G2]** Gemini API image-generation guide (templates, negative space, edits): https://ai.google.dev/gemini-api/docs/image-generation
- **[G3]** Nano Banana Pro ref capacity (14 / 6 objects): https://upsampler.com/ai-models/nano-banana-pro
- **[O1]** OpenAI image-gen prompting guide (gpt-image-2): https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- **[B1]** BFL Kontext image editing: https://docs.bfl.ai/kontext/kontext_image_editing
- **[B2]** Kontext edit-boundary practice (3P): https://eastondev.com/blog/en/posts/ai/20260821-comfyui-flux-kontext-character-consistency/
- **[S1]** Segmind, Seedream prompt guide: https://blog.segmind.com/mastering-seedream-prompt-engineering-guide/
- **[S2]** VEED, Seedream 4: https://www.veed.io/learn/seedream-4-prompting-guide
- **[S3]** Cliprise, Seedream 4: https://www.cliprise.app/learn/guides/model-guides/seedream-4-0-complete-guide
- **[Q1]** Higgsfield docs, Qwen Image 3 edit schema: https://docs.higgsfield.ai/docs/models/qwen-image-3/edit
- **[Q2]** Qwen-Image-Edit-2511 model card: https://huggingface.co/Qwen/Qwen-Image-Edit-2511
- **[H1]** Higgsfield Flare API: https://docs.higgsfield.ai/docs/models/marketing-studio-image/flare
- **[H2]** Higgsfield, AI e-commerce ads 2026: https://higgsfield.ai/blog/ai-ecommerce-ads-2026
- **[H3]** Higgsfield product photography page: https://higgsfield.ai/ai-product-photography
- **[M1]** Motion workshop, "AI product photography that doesn't look fake (Nano Banana Pro & GPT Image 2)": https://motionapp.com/library/talk/how-to-make-ai-product-photography-that-doesn-t-look-fake-nano-banana-pro-gpt/ (video https://youtu.be/_r7NUcM41Kc)
- **[R1]** Kittl GPT Image 2 test: https://www.kittl.com/blogs/?p=21226
- **[R2]** Crepal, GPT Image 2 mockups: https://crepal.ai/blog/aiimage/image-how-to-use-gpt-image-2-for-product-mockups/
- **[N1]** 3×3 grid technique (3P): https://help.apiyi.com/ja/nano-banana-pro-grid-image-cost-optimization-9-images-1-call-ja.html
- **[C1]** RunComfy IC-Light product/video relighting: https://www.runcomfy.com/comfyui-workflows/comfyui-product-relighting-workflow
- **[U1]** Chase Jarvis, Topaz vs Magnific: https://chasejarvis.com/blog/topaz-vs-magnific-best-ai-image-scaler/
- **[U2]** Topaz, Bloom vs Magnific: https://topazlabs.com/learn/bloom-vs-magnific
- **[K1]** Kive, 7-point realism checklist: https://kive.ai/learn/make-ai-product-photos-look-real
- **[K2]** AI-tell checklists: https://www.rewarx.com/blogs/why-your-ai-product-photos-look-fake
- **[P1]** PetaPixel, gradients of light: https://petapixel.com/how-to-create-gradients-of-light-product-photography/
- **[P2]** Karl Taylor, Mugler Angel: https://visualeducation.com/?p=72205
- **[P3]** Karl Taylor, Clinique: https://visualeducation.com/class/clinique-style-advertising-photography-2/
- **[P4]** Nano Banana prompt guides (3P): https://www.pixelbin.io/blog/nano-banana-prompt-guide
- **[F1]** Margiela Scentsorium SS26: https://theimpression.com/maison-margiela-spring-2026-ad-campaign-review/
- **[D1]** Beverage styling and condensation: https://www.squareshot.com/post/how-to-make-photos-of-beverages-for-ecommerce
- **[D2]** Bright and dark field: https://www.uniquephoto.com/community/qa/what-is-dark-field-lighting-and-how-do-you-use-it-for-photographing-glass
- **[FD1]** Food backlight and clock: https://twolovesstudio.com/blog/how-to-use-a-backlight-to-create-a-wow-effect-in-your-food-photos/
- **[BT1]** Cosmetics photography: https://retines.fr/en/blog/what-is-cosmetic-product-photography/
- **[BT2]** 2025 trends: https://retines.fr/en/blog/2025-trends-in-product-photography/
- **[T1]** broncolor black-on-black: https://broncolor.swiss/news/how-to-set-up-lights-for-stunning-black-on-black-product-photography
- **[T2]** Karl Taylor EarPods: https://visualeducation.com/?p=53209
- **[J1]** Don Giannatti, jewelry assignment: https://dongiannatti.substack.com/p/twenty-assignments-to-build-your-a4a
- **[J2]** Nikon jewelry tips: https://m.nikonusa.com/learn-and-explore/c/tips-and-techniques/bright-ideas-tips-and-techniques-for-photographing-jewelry
- **[L1]** whytryai, camera-term test: https://www.whytryai.com/p/midjourney-photography-terms
- **[X1]** Outpainting guidance: https://help.scenario.com/en/articles/expand-outpainting
- **[E1]** GenArena (pairwise vs pointwise): https://arxiv.org/pdf/2602.06013
- **[E2]** Multi-screen app benchmark (23.3 % position bias): https://arxiv.org/pdf/2607.28645
- **[E3]** De-biased VLM-as-3D-judge (swap-consistency): https://arxiv.org/pdf/2606.20364
- **[E4]** Fooling LVLM judges: https://arxiv.org/pdf/2505.15249
- **Internal:** `model-router.md`, `marketing/07`, `marketing/12`, `qc-rubric.md`.
