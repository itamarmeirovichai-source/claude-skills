# 12 — Higgsfield Mastery: API catalogue, verified prices, templates, workflow

Verified 2026-10-07 against the live API using `hfgen.py estimate` (free) and `GET /models` (85 live slugs). We also ran 11 paid Soul Cinema tests ($0.044 in total). Prices are **list USD before discount**. On this account the estimate showed a 15 % discount on Kling. One credit costs $0.0625. Re-check before big runs: the docs say "availability and access can change" [D1].
This file builds on 09/10 and does not repeat them.

## 0. What's new (read this first)

1. **Several models we assumed are not on the API:** Nano Banana Pro/2.1, Seedream, Veo, GPT-Image-2.5 by name, Flux 3, Relight, Color Palette, Upscale, Ad Multiplier, Virality Predictor and Marketing Studio *video/templates* (§2). Do these in post or on the web.
2. **Soul Cinema ignores image references.** We tested `image_reference_url`, `image_urls` and `image_url`. All three returned a frame pixel-identical to the no-ref control. Seeds are deterministic (same seed + same prompt = same frame).
3. **`enhance_prompt: true` invented a real trademark.** Our tests got a Smirnoff bottle. Keep it `false` on every Soul call.
4. **Soul Cinema can't spell.** "MAREA" came out as "MAERA". Put label text in with Flare, never Soul.
5. **Hidden useful endpoints:**
   - `higgsfield-ai/soul/v2/image-to-image` ($0.004; requires `image_url` + `prompt`; undocumented).
   - `higgsfield/ads-studio/v1.0`.
   - `higgsfield/cinema-studio/4.0`, whose Cinema Studio presets are **real JSON enums**.
   - `higgsfield-ai/dop/{lite,turbo,standard}`.
   - `higgsfield/ai-influencer`.
6. **Seedance 2.0 is about 35 % cheaper per second than 2.5** at the same resolution, and it is the only Seedance with 4K. Wan 3.0 costs $0.05–0.20/s and is the cheapest blocking/previs model.
7. **Kling `sound` defaults to `on`, which adds +50 % cost.** Seedance/Cinema Studio `generate_audio` also defaults to `true`. Always send `"sound":"off"` / `"generate_audio":false`.
8. **The fix for "Flare = symmetrical/centred":**
   - Let **Soul Cinema build the off-centre, lived-in plate**.
   - Then **Flare composites the product into that plate** (edit mode, `image_urls:[plate, product]`).
   - Then Kling animates the result.

## 1. Verified endpoint / price table (9:16; list price)

| Use in ads | Endpoint | Price (verified) | Key params / limits |
|---|---|---|---|
| Lookboards, locations, hands, props (no product) | `higgsfield-ai/soul/cinema` | 720p **$0.004**; 1080p $0.006; batch 4 @1080p $0.022 | `prompt, aspect_ratio, resolution 720p/1080p, seed 1–1e6, batch_size 1/4, custom_reference_id` (Soul ID). 720p 9:16 = 960×1696 |
| Stylised realism stills | `higgsfield-ai/soul/v2/standard` | $0.004 / $0.006 | + `style_id` (33 styles via `GET /v1/text2image/soul-styles/v2`); docs say `style_strength` has no effect |
| Re-style / de-gloss an existing image | `higgsfield-ai/soul/v2/image-to-image` | $0.004 | `prompt*`, `image_url*`. Undocumented; behaviour untested |
| Legacy Soul v1 | `higgsfield-ai/soul/standard` | **$0.188** | Has `image_reference_url`; 47× the price of Soul 2. Skip |
| Product keyframes with real product (GPT Image 2.5 Flare) | `marketing-studio/image/flare` | Token-metered (img out $30/1M tok); ≈$0.30 @2k-high in our runs | `prompt, image_urls ≤16, resolution 1k/2k/4k, quality low…max, aspect_ratio` (auto→**square**), `preset_id`, `enhance_prompt` |
| Precise multi-step edits (Sunburst) | `marketing-studio/image/sunburst` | Same pricing as Flare, slower | Same schema [B1] |
| Older MS image | `marketing-studio/image` | $0.21 @2k-high | quality ≤high |
| Static ad concepts (copy + layout) | `higgsfield/ads-studio/v1.0` | ≈$0.084/img (docs, illustrative) | `prompt ≤8000, image_urls ≤10, niche, target_audience, language, batch_size 1–8, aspect_ratio` (no auto) |
| Character/product identity training | `POST /v1/custom-references` | Catalogue lists 40 cr ≈ $2.50 | `model_version v1/v2/cinema`, 1–100 images |
| Macro / product-fidelity I2V | `kling-video/v3.0/pro/image-to-video` | 5 s **$0.476** off / $0.714 on; 10 s $0.952 | `image_url*, last_image_url, prompt ≤2500, duration 3–15, cfg_scale 0–1 (0.5), sound, multi_shots, multi_prompt ≤6×{prompt ≤512, duration}, elements` |
| Drafts | `kling-video/v3.0/std/image-to-video` | 5 s $0.357 off / $0.536 on | same |
| 4K Kling | `kling-video/v3.0/4k/image-to-video` | 5 s **$1.785** (sound on or off) | Don't. Upscale in post |
| Kling Turbo | `kling-video/v3.0-turbo/image-to-video` | 720p $0.476, 1080p $0.595 | No sound, end frame, elements or multi-shot. No saving |
| Multi-image refs + first/last frame | `kling-video/o3/image-reference` | std $0.357, pro $0.476 (sound on $0.595); **4k → 409 unavailable** | `image_urls, first_frame_url, last_frame_url, mode, shot_type customize/intelligent, multi_prompt, elements` |
| First/last frame (O3) | `kling-video/o3/first-last-frame` | std $0.357 / pro $0.476 | Uses `first_frame_url/last_frame_url` (≠ Kling 3 names) |
| Video-guided Kling | `kling-video/o3/video-reference` | pro 5 s $0.714 | 1 video ≤, 4 imgs, 3–10 s |
| Kling edit / Motion Control | `kling-video/o3/video-edit`, `kling-video/v3/motion-control/{std,pro}` | Estimate returns 500 with placeholder URLs; price on a real call | Edit: source 3–15.5 s, ≤200 MB |
| Dynamic sequences, many refs | `bytedance/seedance-2.5/reference-to-video` | **$0.206/s 480p, $0.462/s 720p, $1.137/s 1080p** | `image_urls ≤30, video_urls ≤10, audio_urls ≤10 (≤50 total), duration 4–30, aspect_ratio, bitrate_mode, generate_audio`. **No seed** |
| Seedance I2V (+end frame) | `bytedance/seedance-2.5/image-to-video` | Same per-second rates | `image_url*, end_image_url`; framing follows the image |
| Fix a region / continue a clip | `bytedance/seedance-2.5/video-edit`, `/video-extend` | $0.123/0.277/0.682 per s of **input + output** | Edit derives duration from source; extend 4–30 s |
| Cheaper Seedance / 4K | `bytedance/seedance-2.0/{image,reference}-to-video` | ≈$0.136/s 480p, **$0.302/s 720p**, $0.680/s 1080p, $1.555/s 4K (token-computed) | 4–15 s; refs ≤9 img/3 vid/3 audio |
| Preset-driven Seedance 2.5 | `higgsfield/cinema-studio/4.0` | Same as Seedance 2.5 (480p/720p only) | Enums: `camera_movement` (33), `camera_lens`, `camera_model`, `camera_aperture`, `light`, `genre`, `era`, `pacing`, `color_palette` (50); refs `<<<image_1>>>`. Omit a field for "auto" |
| Swap product into existing video | `higgsfield/genjutsu/object-swap/v1.0` | **$0.318/0.681/1.632 per input s** (480/720/1080) | `video_url*` (4–30 s, ≥409,600 px/frame), `image_urls* ≤8`, `prompt` optional |
| Re-drive motion | `higgsfield/genjutsu/motion-transfer/v1.0` | Same | Same |
| Whole-clip style | `higgsfield/genjutsu/restyle/v1.0` | Same | `preset_id` (20 animation styles; none photoreal) |
| Cheap previs / blocking | `alibaba/wan-3.0/{image,reference}-to-video` | **$0.05/0.10/0.20 per s** | 2–30 s, `end_image_url`, r2v 10 img/5 vid/5 audio + `file_url/link_url`, `seed` |
| Wan premium | `alibaba/wan-3.0-prime/image-to-video` | 5 s $0.595 (720p) / $1.19 (1080p) | Same |
| DoP camera presets | `higgsfield-ai/dop/{lite,turbo,standard}` | $0.125 / $0.407 / $0.563 | `prompt*, image_url*`. Any `motions` value except `[]` → HTTP 500; the 121 presets work on web/MCP only |
| Others live | `wan/v2.6|v2.7` (1080p 5 s $0.638), `alibaba/happy-horse/v1.1` ($0.765), `minimax/h3` ($0.553), `pixverse/v6` ($0.255), `xai/grok-imagine-video/v1.5/reference-to-video` ($0.41), `lightricks/ltx-2.5` (has `camera_movement` enum), Kling 2.5-turbo/2.6 pro ($0.298), `alibaba/qwen-image-3/edit` ($0.075), `xai/grok-imagine-image-2.0` ($0.06), `z-image/turbo` ($0.015) | | |

**Billing traps:**
- Kling multi-shot is billed on the **sum** of the `multi_prompt` durations [D2]. The estimate wrongly returned the 5 s price for 3×3 s, so budget for 9 s ($0.857).
- On Seedance/Cinema Studio, `video_urls` cut the token rate to ×0.6, but the input seconds become billable.
- Failed and NSFW requests aren't charged. Outputs live for ≥7 days [D3].
- Free catalogue GETs:
  - `GET /models`
  - `GET /marketing-studio/image/presets` (75 presets, paged with `?cursor=50`)
  - `GET /models/higgsfield/genjutsu/restyle/v1.0/presets`
  - `GET /v1/motions` (121 DoP moves)
  - `GET /v1/text2image/soul-styles[/v2]`

## 2. Not on the API, and what to use instead

| Web tool | API status | Use instead |
|---|---|---|
| Nano Banana Pro / 2.1 | `nano-banana-pro` → **503 model_disabled**; others 404 | Flare/Sunburst (16 refs) or `qwen-image-3/edit` ($0.075) for text/label edits |
| Seedream 4/4.5/5, Veo 3/3.1, Flux 3, Popcorn | 404 | Soul Cinema (realism), Flare (product), Seedance/Kling (video) |
| Marketing Studio video templates, Click-to-Ad, UGC, Hypermotion | 404. Docs: "isn't available through Supercomputer, MCP… yet" [B2] | Seedance 2.5 r2v with our own treatment prompt |
| Relight, Color Palette, Upscale, Virality Predictor | 404 | Our ffmpeg LUT/grade + film chain; restyle via Soul 2 i2i (untested) |
| Ad Multiplier (in Ads Studio) | 404 | Genjutsu object-swap + Seedance video-edit |
| Kling Elements creation, Kling speed ramps (Flash In/Out, Bullet Time, Impact…) [B3] | `elements` accepts only account-owned IDs created on web | Start frame + O3 `image_urls`; ramps in reel-studio |
| Kling 3.0 Omni 4K | O3 `mode:"4k"` → 409 | `mode:"pro"` + upscale |

## 3. Model playbook for ads (beyond 09)

**Soul Cinema: the realism engine.** In our tests it gave off-centre composition by default, real wood grain, window falloff and believable skin and hands.
Weaknesses:
- It ignores image refs.
- Label text comes out misspelled.
- `enhance_prompt` injects real brands.
- Colour words get over-applied: "lime plaster" became an acid-green room.
- Prompts with film language ("35mm film") produce **black rounded gate corners** (pixel value 0–1). Crop about 3 % before animating, or Kling will animate the vignette.
- Changing the subject under a locked seed changes the whole composition. A seed only reproduces the identical prompt.
Use it for plates, hands, props and lookboards in batch 4 ($0.022 at 1080p).

**Flare (GPT Image 2.5).**
- It keeps "subjects from a reference photo… when moved into a new scene", edits "only what got asked for", and holds edits across multiple steps [B1].
- Send `aspect_ratio:"9:16"` explicitly, because `auto` returns square.
- For `quality`, use `high` for keyframes. `xhigh/max` only add cost.
- Preset mode (`enhance_prompt:true` + `preset_id` + 1–2 images, product first) gives template looks such as "In-Hand Detail" or "Sand Dune Plinth". These are centred catalogue looks. Use them for the end card, not the story.
- **Sunburst** is for the label-fix pass when edits keep drifting.

**Ads Studio API.** It generates concept + copy + layout in one call, 1–8 per batch. It is good for static cutdowns and for testing angles. Product preservation "is not guaranteed" [D4].

**Kling 3.0 Pro I2V: hero product fidelity.**
- One move and one action per shot.
- Use `last_image_url` for a locked packshot landing.
- Keep `cfg_scale` 0.5. Go to 0.6–0.7 when the move is ignored, and 0.35–0.4 when motion looks over-cooked or rubbery (heuristic: the range is 0–1).
- Multi-shot (`multi_shots:true`, ≤6 shots, each prompt ≤512 chars, top-level prompt still required) works for macro triptychs within one lighting world.
- There is no seed, so variance comes only from takes.

**Kling O3 image-reference.**
- Use it when you need the product **and** a location/hand reference with no keyframe: `image_urls:[product, plate]` plus an optional `first_frame_url`.
- `shot_type:"intelligent"` lets it cut for you, but it still needs `multi_prompt`.
- Same price as Kling 3 Pro, and `sound` defaults to off.

**Seedance 2.5 r2v.**
- In Higgsfield's own test it was best at "commercial and multi-angle work… maintaining product and object details across changing camera positions" [B4].
- Iterate at 480p ($1.03 for 5 s) and finish at 720p.
- 1080p costs $1.14/s, so keep it for one hero beat at most.
- Tag references with `<<<image_N>>>` (the documented API token [D5]) **and** describe each one in words.

**Cinema Studio 4.0 API.** This is Seedance 2.5 with presets as typed enums. It "retained the most constraints" in Higgsfield's adherence test [B4]. Use it when a shot needs a named move/lens/light that prompts alone don't hold. The limit is 720p.

**Genjutsu.** Repurposes an approved clip. It is expensive per second, so use 480p or 720p and keep source clips to 4–6 s. Object Swap with product refs turns one master ad into SKU variants [B5].

**Wan 3.0.** Animatic/previs at $0.05/s (480p) to test blocking and timing before paying for Seedance. It also accepts a brief document via `file_url`.

## 4. Prompt templates (copy, fill the brackets)

Use one **campaign lock** across every call (look and exclusions only, per 09 §2):
`LOCK: one motivated key light [source, side, Kelvin], falloff into shadow; Kodak Vision3 250D grain, gentle halation; unretouched skin; product shape, label and colour never change; no readable text except the product label; no logos, no real brands; no CGI sheen, no turntable spin, no fisheye.`

**A. Soul Cinema plate (no product).**
```json
{"prompt":"Vertical frame. [Empty|hands-only] [location], seen from a three-quarter angle at [height]. [3 lived-in details: chipped edge, water spots, folded linen]. [Single light: late sun through small window from frame left, hard rectangle on the wall]. Negative space at [lower-left third] where an object will stand. 35mm lens, Kodak Portra 400, fine grain. No people, no products, no text.",
 "aspect_ratio":"9:16","resolution":"1080p","batch_size":4,"enhance_prompt":false}
```
Name colours as materials ("pale limestone", "sun-faded sage linen"), not bare hues. Bare hues get over-saturated.

**B. Flare composite (product into plate).**
```json
{"prompt":"Image 1 is the scene and the source of truth for light, grain, lens and composition. Image 2 is the exact product: preserve its silhouette, proportions, cap, label text \"[TEXT]\" and colour. Place the product from image 2 standing at the lower-left third of image 1 (x 30%, y 68%), turned 20° toward the window, resting on the counter with a soft contact shadow falling right. Relight the product only with image 1's window light: warm highlight on the left shoulder of the glass, darker right side. Keep everything else in image 1 unchanged. Not centred, not symmetrical, no added props, no new text.",
 "image_urls":["<plate>","<product>"],"aspect_ratio":"9:16","resolution":"2k","quality":"high"}
```
If it re-centres the product, add "the frame's centre stays empty; product touches the left third line".

**C. Kling 3.0 Pro macro (single move).**
```json
{"image_url":"<keyframe>","duration":5,"sound":"off","cfg_scale":0.5,
 "prompt":"Macro product insert. Camera: slow dolly-in on a precision slider, constant speed, decelerating into a static hold for the last second; no zoom, no orbit. Action: one bead of condensation slides down the left side of the bottle and stops at the label edge. Light: warm key raking from upper left reveals micro-scratches and fingerprints; the right side falls to shadow. The label stays sharp and unchanged; the bottle never moves or deforms."}
```

**D. Kling start→end packshot landing.**
Add `"last_image_url":"<packshot>"`. Write only the path between the frames: "Camera arcs 25° right at constant radius and settles exactly on the end frame; the product stays still; light shifts across the glass as the angle changes." Don't describe anything that contradicts either frame (09: "fighting your own end frame").

**E. Kling multi-shot triptych (one lighting world).**
```json
{"image_url":"<keyframe>","sound":"off","multi_shots":true,"prompt":"Three macro inserts of the same amber serum bottle in one sunlit bathroom; identical light and grade throughout.",
 "multi_prompt":[{"prompt":"Extreme close-up on the dropper tip, a golden drop swells and falls; locked-off.","duration":3},
                 {"prompt":"Fingertips with short unpolished nails twist the cap open; handheld, subtle breathing sway.","duration":3},
                 {"prompt":"Rack focus from the drop on skin to the bottle behind; static.","duration":3}]}
```
This is billed as 9 s.

**F. Seedance 2.5 reference-to-video (the BIG IDEA shot).**
Use the block order from 09 §2, plus the reference key from Higgsfield's own ad prompts [B6][B4]:
```
REFERENCE KEY (attach in this order):
<<<image_1>>> = THE PRODUCT ([material, shape, cap, label text]) — PRODUCT reference: exact shape, colour, geometry, label; this label is the ONLY readable text in the video.
<<<image_2>>> = LOCATION — reference only for architecture, materials and light; do not reproduce the frame 1:1.
<<<image_3>>> = HAND/CAST — identity and wardrobe ONLY, NOT lighting, NOT backdrop.
RELIGHT every reference natively in the location's light; soft contact shadows; never composited.
GLOBAL STYLE: [LOCK]. Total: 6 s, 9:16, real time, no speed ramps.
FIRST FRAME: product already in the extreme foreground at x 30% y 65%; no establishing shot.
0.0–2.5 | [claim made literal: e.g. a dry, cracked clay slab beside the bottle drinks one drop and turns supple]. Cam: 50mm, static, f/2.8.
2.5–6.0 | Cam: slow push-in, decelerating to a hold on the label. PHYSICS: [material behaviour stated explicitly].
AUDIO: none.
```
Settings: `{"image_urls":[...],"duration":6,"resolution":"480p"→"720p","aspect_ratio":"9:16","generate_audio":false}`.
Keep ≤5 refs: a cluttered set "produces a less coherent result" (09).

**G. Cinema Studio 4.0 (enums carry the camera).**
```json
{"prompt":"<<<image_1>>> is the product... [action only]","image_urls":["<product>","<plate>"],"duration":5,"resolution":"720p","aspect_ratio":"9:16",
 "camera_movement":"dolly-in","camera_lens":"halation-vintage","camera_model":"35mm-film","camera_aperture":"f4-moderate","light":"window","pacing":"single-shot","generate_audio":false}
```
Leave `genre`/`era`/`color_palette` out unless they're wanted. "auto" is rejected, so omit the field instead.

**H. Genjutsu object swap (SKU variant).**
`{"video_url":"<approved 5 s clip, 720p>","image_urls":["<new product front>","<3/4>"],"prompt":"Replace only the bottle with the product in the references; keep hands, timing, light and camera identical.","resolution":"720p"}` costs about $3.41.

## 5. Camera vocabulary each model obeys

- **Cinema Studio 4.0 (enum, guaranteed):**
  - Moves: `static-shot, dolly-in/out, slow-zoom-in/out, crush-zoom, dolly-zoom, truck-left/right, slider-left/right, side-tracking, tracking, arc-left/right, drone-orbit, crane-up/down, pedestal-up/down, tilt-up/down, pan-left/right, whip-pan, rack-focus, handheld, snorricam, pov, robot-arm, bullet-time, aerial-pullback, helicopter-shot`.
  - Lenses: `clean-sharp | anamorphic | vintage-anamorphic | warm-vintage | halation-vintage`.
  - Light: `silhouette | practicals | window | overhead-fall | contre-jour | soft-cross`.
- **LTX-2.5 (enum):** `dolly_in/out/left/right, jib_up/down, static, focus_shift`.
- **DoP (web/MCP preset names; 3 or 5 s):** Dolly In, Super Dolly In, Crash Zoom In, Lazy Susan, 3D Rotation, Robo Arm, Through Object In, Push To Glass, Focus Change, Levitation, Object POV, Whip Pan.
- **Kling 3.0 (prompt):** one move per shot. State path + speed + easing + end-hold, and rule out the rival move.
  - Reliable: "slow dolly-in on slider", "locked-off static", "arc 20–30° at constant radius", "rack focus from A to B", "handheld breathing sway", "crane up revealing", "rigid robot-bolt push-in, no easing" (10 §B).
  - Avoid: full 360 orbits, fast zooms.
- **Seedance 2.x (prompt):** time-coded beats (`0.0–2.5 |`). "dolly in, truck left, arc shot, push in, pull back wide, handheld follow, crane up, orbital move" (09). It can carry 2–3 moves per clip if each beat is timed. Cut on matched direction.

## 6. Production workflow: 20 s premium ad (+6 s cutdown) for ≤$10

| # | Step | Model | Qty | Cost |
|---|---|---|---|---|
| 1 | Lookboard + 4 location plates + hand/prop studies | Soul Cinema 1080p, batch 4 | 6 batches | $0.13 |
| 2 | Product keyframes: composite product into plates (template B) | Flare 2k high | 7 (5 + 2 fixes) | ≈$2.10 |
| 3 | Optional de-gloss of Flare frames | Soul 2 i2i | 5 | $0.02 |
| 4 | Previs the BIG IDEA beat (blocking/timing) | Wan 3.0 480p 6 s | 1 | $0.30 |
| 5 | Hook macro, texture insert, hands-in-use, lifestyle | Kling 3.0 Pro I2V 5 s, sound off | 4 + 1 retake | $2.38 |
| 6 | End packshot with start→end landing | Kling 3.0 Pro I2V + `last_image_url` | 1 | $0.48 |
| 7 | BIG IDEA shot | Seedance 2.5 r2v 720p 6 s (draft first at 480p only if previs failed: +$1.23) | 1 | $2.77 |
| | **Total** | | | **≈$8.18** (buffer $1.80) |

Order of work:
1. Approve plates.
2. Approve keyframes, checking label spelling and the off-centre rule.
3. Generate the hardest shot first (the BIG IDEA).
4. Generate Kling inserts in one parallel `hfgen batch`.
5. Trim every clip to its best 2–3 s; avoid the 5–8 s drift zone (09).
6. Grade, grain and halation in our film chain. Music, SFX and VO in ElevenLabs.
7. For the 6 s cutdown, re-edit the hook + BIG IDEA + packshot. No new generations.

If the budget is tighter, swap step 7 for Seedance 2.0 720p ($1.81).

## 7. Failure modes and fixes

| Symptom | Cause | Fix |
|---|---|---|
| Soul output ignores the product photo | Soul Cinema/2 have no image-ref input (verified) | Soul for plates only; product via Flare composite or Kling/Seedance refs |
| Real brand appears (Smirnoff) | `enhance_prompt:true` rewrites the prompt | Always `false`; add "unbranded, no real brands" |
| Misspelled label | Soul/video models redraw text | Text only from Flare/Sunburst frames; keep labels in close shots; Qwen edit ($0.075) to repair |
| Black rounded corners in the still | Film-language vignette | Crop 3 % and rescale before I2V |
| Acid colour cast | Bare colour words over-applied | Materials + "muted", or name the grade |
| Flare returns a square, centred image | `aspect_ratio:auto` → square; model centres | Explicit `9:16`; x/y placement; composite into a Soul plate |
| Bill 50 % higher than planned | Kling `sound` default on | `"sound":"off"`; Seedance `"generate_audio":false` |
| Multi-shot costs more than estimated | Billed on the summed `multi_prompt` durations | Budget the sum; prompts ≤512 chars; top-level prompt required |
| 400 on Seedance refs | `asset://` or private URLs | `hfgen upload` → public CDN URL |
| 409 "temporarily unavailable" | O3 `mode:4k` | Use `pro` |
| 500 on DoP | `motions` param broken | Cinema Studio `camera_movement` enum instead |
| Cinema Studio 400 | `"auto"` value | Omit the field |
| Genjutsu rejects video | <4 s or <409,600 px/frame (480×854 is barely OK) | Source ≥720p, 4–30 s |
| Product morphs mid-clip | Long clip, many moves, cluttered refs | 5 s, one move, ≤5 refs, product as the first reference |
| Composite look on subject | Reference's studio light carried over | "RELIGHT natively in the location; NOT the reference lighting" [B6] |
| Kling `elements` rejected | IDs must be created on web in the same account | Start frame + O3 `image_urls` |
| Files vanish | Retention ≥7 days only | hfgen downloads immediately |

## Sources

**API docs**
- D1 https://docs.higgsfield.ai/docs/models
- D2 https://docs.higgsfield.ai/docs/models/kling-3/pro-image-to-video
- D3 https://docs.higgsfield.ai/docs/concepts/billing-and-retention
- D4 https://docs.higgsfield.ai/docs/models/ads-studio/generate
- D5 https://docs.higgsfield.ai/docs/models/cinema-studio-4/generate
- Full schemas: https://docs.higgsfield.ai/docs/llms-full.txt
- Others: https://docs.higgsfield.ai/docs/models/soul-cinema/generate, https://docs.higgsfield.ai/docs/models/marketing-studio-image/flare, https://docs.higgsfield.ai/docs/models/seedance-2-5/reference-to-video, https://docs.higgsfield.ai/docs/models/kling-o3/image-reference, https://docs.higgsfield.ai/docs/models/genjutsu/object-swap

**Blog and help pages**
- B1 https://higgsfield.ai/blog/gpt-image-2-5-higgsfield
- B2 https://higgsfield.ai/creator-hub/help-center/tools/how-do-i-use-marketing-studio-to-create-video-ads
- B3 https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-kling
- B4 https://higgsfield.ai/blog/ai-video-prompt-adherence-comparison
- B5 https://higgsfield.ai/blog/higgsfield-genjutsu
- B6 https://higgsfield.ai/blog/ai-ecommerce-ads-2026
- Also: https://higgsfield.ai/blog/higgsfield-ads-studio, https://higgsfield.ai/blog/new-marketing-studio-higgsfield, https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-dop, https://higgsfield.ai/blog/ai-video-hands-faces, https://higgsfield.ai/blog/why-ai-video-generations-fail, https://higgsfield.ai/creator-hub/changelog

**Our own data**
- Live estimates, 2026-10-07.
- Soul Cinema tests: 11 images, seed 424242 and 777–780.
