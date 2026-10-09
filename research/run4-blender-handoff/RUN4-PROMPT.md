# RUN 4 — BUILD THE BLENDER SCENE (paste this whole file, then type: RUN MODE: 4)

**Before you paste this, fill in these two lines:**
- SCANS FOLDER: `[e.g. ~/Desktop/smash-scans/ — leave empty if not scanned yet]`
- BLENDER PROJECT FOLDER: `[e.g. ~/Desktop/smash-blender/]`

**This run must be started in Claude Code or the Claude desktop app on the Mac, with Blender open and a Blender MCP connected.** It cannot run on the claude.ai website or in a cloud container.

## YOUR ROLE
You are a CG food artist at the level of a commercial studio. The goal is MAXIMUM PHOTOREALISM — the food must look real enough to eat. Using the sequence, contract, motion tokens and 3D asset plan below, **BUILD the scene directly in the open Blender through the Blender MCP — don't write a guide.** Follow the contract exactly: frame counts, resolutions, naming, mesh names.

## WORKING RULES
- Use whichever Blender MCP tools are available. **First confirm the connection** with its scene/objects summary tool (e.g. `get_scene_info` or `get_objects_summary`). If no Blender MCP is connected, stop and say exactly how to connect it.
- One `bpy` script per major step via `execute_blender_code` — not many tiny calls. Keep tool output short; never dump the whole scene. When unsure of a `bpy` call, check the MCP's API docs tool (e.g. `search_api_docs`) instead of guessing.
- Verify with the MCP's screenshot tool only at the end of each major step — **max ~15 screenshots total.** Judge each critically ("does this look like real food?") and fix before moving on. **Never claim something looks real without looking at it.**
- Save to the BLENDER PROJECT FOLDER before each major step: `smash_v01.blend`, `smash_v02.blend`, … Never touch files outside the project and scans folders.
- Assets: my scans first. If the MCP has Poly Haven / Sketchfab / Hyper3D / Hunyuan3D tools, use them (Sketchfab only with a licence allowing commercial use; AI 3D only as a fallback). Otherwise tell me exactly which files to download from polyhaven.com (CC0) and where to put them.
- Long renders time out through the MCP — render only low-sample test frames through it.
- State lives in the saved `.blend`, so this run may be split across fresh sessions. Each one starts with the connection check and continues from the latest `smash_vXX.blend`.

## STEPS
1. **Project setup:** units, frame rate and frame range from the contract, one collection per beat, clean naming.
2. **Burger layers:** import and clean my scans (decimate/retopology, UVs, textures). With no scans yet, model each layer procedurally so scans can replace them later without renaming. Exact contract names; origins at each layer's own centre; stack axis exactly +Z.
3. **Photoreal materials per layer:** bun (subsurface), sesame (geometry-nodes scatter), sauce (glossy/clearcoat), caramelised onion, beef bacon, melted plant-based cheese, seared patty crust (displacement), and the cut interior faces.
4. **The cut:** pre-split halves with real interior faces (not a raw boolean) plus the chef's knife and its glint.
5. **The 5-burger toss:** variations of the hero, ballistic arcs, bullet-time speed ramp.
6. **Camera:** one continuous take across all 8 beats, keyed to the contract — orbit, rack focus (DOF), push-in, impact shake. Plus the separate portrait camera for mobile.
7. **Explode, half turn, smash and cut** with the motion tokens' easing: custom F-curves, overshoot, squash.
8. **Simulations:** volumetric steam, the sauce drip, loose sesame seeds. Bake before rendering.
9. **Lighting & world:** food-commercial lighting inside their brand world (red / yellow / near-black); background per the contract.
10. **Render setup:** Cycles on Apple Silicon (Metal), samples, denoising (OpenImageDenoise — OptiX is NVIDIA-only), motion blur, DOF, resolutions and output naming per the contract. **Render 3 low-sample test frames (from beats 2, 4 and 7), show them, and fix until they look real.**
11. **The label anchor track:** export `/frames/labels.desktop.json` and `/frames/labels.mobile.json` — the per-frame projected screen positions of each layer origin across beats 4–5, in normalised 0–1 viewport coordinates. The website's DOM labels cannot track the layers without this.
12. **Real-time glTF:** bake textures, decimate, export with Draco and the exact mesh names; then give me the `gltf-transform` commands for Meshopt/KTX2, and the USDZ for AR.
13. **Hand-off:** the Terminal command for the full overnight render, a realistic render-time estimate and how to cut it, and the ffmpeg/avifenc commands that convert the frames to the contract's names and sizes.
14. **What I do by hand:** buying and taking apart the burger, scanning each layer and a cut half with my phone (app, lighting, turntable, photo count, fighting shine and steam), where to drop the files — plus a real-photo shot list for the rest of the site with phone settings.
15. **The mistakes that make CG food look fake** — check the scene against each and fix: uniform cleanliness, no subsurface in the bun, uniform roughness, a flat boolean cut face, front lighting instead of backlight, no steam, perfectly stacked layers, too-even sesame, wrong SSS radius scale, the Standard view transform instead of AgX/ACES, floating objects with no contact shadow, cheese modelled as a flat slice, too much DOF, over-saturated meat, and identical clones in the toss.

## OUTPUT (PART F, Hebrew, max 1,500 words, Blender names in English)
A build log and hand-off: what you built (with the screenshots and the 3 test frames), which `.blend` versions are saved where, an honest realism verdict, the render and conversion commands in code blocks, and my to-do list.

---
# THE 8-BEAT SIGNATURE SEQUENCE — "THE TOSS, THE SMASH, THE CUT"

One pinned section. **One continuous camera take.** Scrubbed by scroll. Perfectly reversible.

- **Pinned length: 620vh desktop / 420vh mobile.** (620vh gives roughly 5.2 screen-heights of scroll across 8 beats — about 0.65 screen-heights per beat, which is the slowest a beat can run before it feels like the page is stuck. Below ~480vh the explode and the cut collide.)
- **Hero burger: the Loaded Smashed.** Build order bottom to top, per their menu description — `[TO CONFIRM the exact build and whether chef sauce is included]`:
  `bun_bottom → patty_lower → cheese_lower → patty_upper → cheese_upper → bacon_beef → onion_caramelized → sauce_chef → bun_top (with sesame)`
  Nine separable layers. All cheese is plant-based: matte melt, no dairy sheen. Beef bacon is deep red and thick-cut with no white fat marbling.
- **Progress is one number.** `p` ∈ [0,1] from ScrollTrigger. The canvas frame index, every DOM overlay, the Kong arm, the labels, the page split and the match cut all read that same `p`. Nothing keeps its own state.

## Refined beat timings
I tightened the supplied ranges by ~1–2% each: the explode and the cut are the two beats that carry information and appetite, so they get the extra room, taken from the toss and the half turn.

| # | Beat | Range | Desktop frames | Mobile frames |
|---|---|---|---|---|
| 1 | THE TOSS | 0–11% | 1–27 | 1–14 |
| 2 | BULLET TIME | 11–21% | 28–52 | 15–26 |
| 3 | THE CLOSE-UP | 21–31% | 53–77 | 27–38 |
| 4 | THE EXPLODE | 31–50% | 78–124 | 39–62 |
| 5 | THE HALF TURN | 50–59% | 125–146 | 63–73 |
| 6 | THE SMASH | 59–69% | 147–171 | 74–86 |
| 7 | THE CUT | 69–86% | 172–213 | 87–107 |
| 8 | THE SLICE-THROUGH | 86–100% | 214–248 | 108–124 |

## Beat 1 — THE TOSS (0–11%)
Five burgers fly up from below the frame as if flipped off the griddle. Each on its own ballistic arc: `v0` between 4.2 and 5.8, launch phase staggered by 0.06 of the beat, its own spin axis and drift. They must never read as a formation — different heights, different rotation speeds, one tumbling nearly end over end. Loose sesame seeds shake off the buns near the top of each arc and drift.
**Camera:** low and wide (35mm), tilting up to follow, with a faint handheld noise (±0.4°). The viewer is standing at the griddle.
**Overlay:** the headline "EVERYBODY'S A WINNER!" `[TO CONFIRM this line is theirs to use here]` in Smash Dollars, split into characters, each character arriving on its own arc offset from a burger's path, settling by 9%.
**Sound (only if on):** a griddle scrape, then five staggered whooshes pitched to each arc's speed.

## Beat 2 — BULLET TIME (11–21%)
At the apex, object time ramps to a near-freeze while the camera keeps moving — that contrast *is* the effect. The camera orbits ~90° around the frozen cluster on a fixed radius. Sesame seeds hang in the air, individually visible.
At 14–20% **Kong's hand enters from the right edge and snatches one burger out of frame.** This is the "Kong Arm" asset — it is a DOM/CSS layer composited over the canvas (or its own alpha frame sequence), scaled and positioned from `p`, not baked into the main render, so it can be swapped when the client sends better artwork.
**Camera:** pure orbit, subject locked dead centre. No push, no roll.
**Overlay:** everything fades to 15% opacity except a single line, "SMASHED. NOT COOKED." `[TO CONFIRM copy]`
**Sound:** the ambient drops out to a low hum, one deep thud on the grab.

## Beat 3 — THE CLOSE-UP (21–31%)
Rack focus + push-in onto the hero burger. The other four fall away, blurred. The hero keeps the spin it earned in the toss and decays naturally — angular velocity × `exp(-k·t)` — until it faces the camera. The last 15% of the beat slerps it onto an exact camera-facing quaternion, so it *lands* rather than stops.
**Camera:** push in along the forward axis by ~0.9 units. **Never change FOV** — that flattens the burger and reads as a zoom.
**Overlay:** the item name "LOADED SMASHED" fades up, Londrina Solid, letter-spaced, under the burger.
**Sound:** a low rising tone, resolving on the landing.

## Beat 4 — THE EXPLODE (31–50%)
The nine layers pull apart with big gaps — staggered 0.05 apart from the centre outward, `back.out(1.6)`, 8–12% overshoot, each with its own small tilt (±0.06 rad) so the stack reads as hand-built rather than machined. Sesame seeds drift in the gaps. **Gaps must be at least 0.6× each layer's thickness** or the eye reads one object, not nine.
**Labels:** one per layer, in their fonts, appearing beside its layer on an 0.08 stagger *behind* the layer's own arrival. Positioned by projecting the layer's world position to screen each frame and writing a `transform` to a DOM node — they billboard, they never rotate with the burger, and they collision-shift vertically if two would overlap.
Label copy: `SESAME BRIOCHE` · `CHEF SAUCE` `[TO CONFIRM]` · `CARAMELIZED ONION` · `BEEF BACON` · `PLANT-BASED CHEESE` · `SMASHED PATTY` · `PLANT-BASED CHEESE` · `SMASHED PATTY` · `TOASTED BASE`
**Camera:** pull back 15%, rise 10°. All rotation stops. This is the information beat — the camera has to calm down or nothing is readable.
**Sound:** nine soft separations, ascending.

## Beat 5 — THE HALF TURN (50–59%)
The exploded burger rotates a further 180°. Labels stay pinned to their layers and stay readable — they re-anchor to whichever side of the layer now faces the camera, and flip their leader line rather than their text.
**Camera:** holds; the object turns. (If the camera orbits *and* the object turns, the motion cancels and reads as a stutter.)

## Beat 6 — THE SMASH (59–69%)
The nine layers SLAM back together.
- **59–62%:** anticipation — every layer pulls *outward* another 8% and holds for a beat. This is the single most important 3% in the sequence; without it the slam has no weight.
- **62–64%:** impact. Layers converge on `expo.in`. On contact: a 2-frame squash of the whole burger (scaleY 0.82 / scaleX 1.12, volume-preserving), a camera shake decaying over 300ms, a flash of `#E51144` at 12% opacity over the whole viewport for 80ms, sesame seeds jumping off the bun, grease specks flung outward.
- **64–69%:** recoil and settle, steam begins to rise, the burger breathes back to 1.0 with a slight overshoot.
**Sound:** a wet thud layered with a sizzle that swells for ~1.2s.
**Haptic:** `navigator.vibrate([12, 30, 8])` on the impact frame (Android only; the beat must work identically without it).

## Beat 7 — THE CUT (69–86%)
A chef's knife enters from the top right on an arc. A specular glint sweeps along the blade as it comes in — an animated streaked highlight, not a texture flash. It slices down the middle; **the burger squashes slightly under the blade** as it passes, then releases. The two halves separate 2–4 cm and rotate ~10° toward the camera, pressed close, showing the inside: seared crust, juicy patty, melted plant-based cheese, sauce. Steam rises from both cut faces. One slow sauce drip runs off the lower edge and falls out of frame.
**Camera:** macro, 85–100mm equivalent, focused on the blade edge as it enters, then racking to the cut face over ~600ms.
**Do not open the halves wide.** Wide reads as a diagram; pressed close reads as appetite. This is the money shot of the entire site.
**Sound:** a clean blade shear, then the steam.

## Beat 8 — THE SLICE-THROUGH (86–100%)
The cut line continues past the burger and across the whole screen. **The page splits along it** — the upper and lower halves of the viewport slide apart on the cut's angle — and the menu is revealed through the widening gap. As the halves clear, the round cut face of the burger **match-cuts into the sticky "Order Now" button** (GSAP Flip, 0.7s `power3.inOut`, `absolute: true`, `scale: true`).
**The Order button is clickable for the entire duration of this beat.** It is never covered, never `pointer-events: none`, and never waits for the animation to finish.

## Build approach — decided, for maximum realism
- The 8 beats are **rendered in Blender Cycles as an image sequence**, scrubbed on a `<canvas>`.
- **Labels, the Kong arm, the page split and the match cut are DOM/CSS layers** synced to the same `p`. They are never baked into the frames — they must stay editable, translatable, selectable and screen-reader-readable.
- **Interactive moments** elsewhere on the site (Build Your Smash, AR) use a lightweight real-time glTF **baked from the same Blender scene**, so the two never look like different burgers.
- **Until the frames exist, a real-time procedural fallback plays the same 8 beats** with primitives and clipping-plane caps. The site is fully shippable in that state; swapping to frames is a one-flag change.

## Mobile
The same story, re-framed — **not a squeeze.** A separate portrait camera in Blender, 1080×1440, 124 frames. The pin runs 420vh. The Kong arm enters from the bottom right instead of the right edge. Labels in beat 4 stack to alternating sides with a shorter leader line. Physics extras (loose seeds, grease specks) are halved.

## Reduced motion
`prefers-reduced-motion: reduce` gets a **crossfade of 4 key frames** — the apex of the toss (frame 40), the fully exploded burger (frame 118), the moment of impact (frame 160), and the finished cut (frame 205) — each held while its beat's caption is read, advancing on scroll with a 400ms opacity crossfade and no transforms. The story survives completely. It is not "animations off".

---

# 7. ASSET CONTRACT
**This is the single source of truth for the Blender scene and for the code. Neither may deviate.**

## Frames
| Parameter | Desktop | Mobile |
|---|---|---|
| Total frames | **248** | **124** |
| Frame numbering | 1-indexed, zero-padded to 4 | same |
| Authored frame rate | 30fps in Blender (8.27s of animation) — playback is scroll-indexed, not timed | same |
| Resolution | **1920 × 1080** | **1080 × 1440** |
| Camera | `cam_main` | `cam_main_portrait` (separate framing, not a crop) |
| Background | **Rendered** (not alpha) — real bounce light, volumetrics and DOF on the backdrop | same |
| Format | AVIF q50 primary · WebP q80 fallback | same |
| Colour space | Render AgX/ACES, **export sRGB with the view transform applied, tagged sRGB** | same |
| Per-frame target | 60–110 KB | 30–55 KB |
| Total budget | **≤ 24 MB** | **≤ 7 MB** |
| Path | `/frames/desktop/smash_0001.avif` … `smash_0248.avif` | `/frames/mobile/smash_0001.avif` … `smash_0124.avif` |
| WebP fallback path | `/frames/desktop/webp/smash_0001.webp` | `/frames/mobile/webp/smash_0001.webp` |

## Frames per beat
| Beat | Desktop | Mobile |
|---|---|---|
| 1 TOSS | 1–27 | 1–14 |
| 2 BULLET TIME | 28–52 | 15–26 |
| 3 CLOSE-UP | 53–77 | 27–38 |
| 4 EXPLODE | 78–124 | 39–62 |
| 5 HALF TURN | 125–146 | 63–73 |
| 6 SMASH | 147–171 | 74–86 |
| 7 CUT | 172–213 | 87–107 |
| 8 SLICE-THROUGH | 214–248 | 108–124 |

## Kong arm sequence (separate, alpha)
| Parameter | Value |
|---|---|
| Path | `/frames/kong/desktop/kong_0001.avif` … `kong_0019.avif` · `/frames/kong/mobile/…` |
| Covers | Desktop global frames **34–52** (`kongStartFrame = 34`) · mobile **17–26** (`kongStartFrame = 17`, 10 frames) |
| Background | **Alpha / `Film → Transparent`** — it composites over the main canvas |
| Resolution | 1200 × 1200 desktop · 800 × 1000 mobile |

## Label anchor track (required — the DOM labels need it)
The ingredient labels in beats 4–5 are DOM elements, but the frames are pre-rendered, so the code has no 3D positions to project. Blender must therefore export a companion track:
`/frames/labels.desktop.json` and `/frames/labels.mobile.json`, shaped as
`{ "frames": { "78": { "bun_top": [0.61, 0.18], "sauce_chef": [0.60, 0.27], ... }, "79": { ... } } }`
— one entry per frame from the first frame of beat 4 to the last frame of beat 5, values being the layer origin projected to **normalised viewport coordinates** (0–1, origin top-left) by the render camera. Missing frames are linearly interpolated by the client. Without this file the labels cannot track their layers and the beat must not ship.

## Poster + reduced-motion key frames
`/frames/poster.avif` (= desktop frame 1) · `/frames/key/key_040.avif`, `key_118.avif`, `key_160.avif`, `key_205.avif` (desktop numbering; mobile equivalents `key_020`, `key_059`, `key_080`, `key_103`).

## Blender object names = glTF mesh names (exact, case-sensitive)
**Hero layers (bottom to top):**
`bun_bottom` · `patty_lower` · `cheese_lower` · `patty_upper` · `cheese_upper` · `bacon_beef` · `onion_caramelized` · `sauce_chef` · `bun_top`
**Children / detail:** `sesame_scatter` (parented to `bun_top`) · `seed_loose_01` … `seed_loose_30` · `drip_sauce` · `steam_domain`
**Cut halves:** `burger_half_left` · `burger_half_right` · `cut_face_left` · `cut_face_right`
**Knife:** `knife_blade` · `knife_handle` · `knife_glint` (the animated area light, render-only — not exported)
**Toss variants:** `burger_toss_a` · `burger_toss_b` · `burger_toss_c` · `burger_toss_d` · `burger_toss_e` (`burger_toss_c` is the hero)
**Cameras:** `cam_main` · `cam_main_portrait`
**Collections:** `BEAT_01_TOSS` · `BEAT_02_BULLET` · `BEAT_03_CLOSEUP` · `BEAT_04_EXPLODE` · `BEAT_05_TURN` · `BEAT_06_SMASH` · `BEAT_07_CUT` · `BEAT_08_SLICE`

**Origins:** every layer's origin sits at its own geometric centre. **Stack axis is exactly +Z**, so one offset vector drives the whole explode. The half hinges sit **on the cut plane**, not at the object centres, or the halves interpenetrate when they open.

## Real-time glTF (baked from the same scene)
| Parameter | Value |
|---|---|
| Path | `/models/hero.glb` (layered burger) · `/models/halves.glb` (cut halves + knife) |
| Budget | ≤ 3 MB hero · ≤ 5 MB halves+knife |
| Geometry | Draco compressed, 8–20k tris per layer |
| Textures | KTX2/Basis, 2048px, baked lighting from the Cycles scene |
| Names | **Identical to the Blender names above** — the code looks meshes up by name |
| Up axis | +Y (glTF convention); the exporter converts from Blender's +Z |
| AR pair | `/models/hero.usdz` for AR Quick Look, real-world scale in metres |

---

# MOTION TOKENS

```css
:root {
  /* Brand — exact, no new hues */
  --smash-red:#E51144; --deep-red:#C20F3A; --deeper-red:#BA0C36;
  --near-black:#13110C; --yellow:#FEEB13;
  --blue:#0083B0; --blue-deep:#007198;
  --white:#FFFFFF; --brown:#401C10;

  /* Tints & shades (derived only) */
  --red-90:#F7405F; --red-70:#FA7B90; --red-20:#FBD0D8;
  --black-90:#1E1B14; --black-80:#2A261C; --black-60:#4A443A;
  --yellow-dark:#D6C50F; --brown-light:#5E2D1B;

  /* Type */
  --font-display:"Smash Dollars","Londrina Solid",system-ui,sans-serif;
  --font-display-alt:"Londrina Solid",system-ui,sans-serif;
  --font-body:"Poppins",system-ui,-apple-system,sans-serif;
  --step--1:clamp(.8rem,.76rem + .2vw,.9rem);
  --step-0: clamp(1rem,.95rem + .25vw,1.125rem);
  --step-1: clamp(1.25rem,1.15rem + .5vw,1.5rem);
  --step-2: clamp(1.56rem,1.4rem + .8vw,2rem);
  --step-3: clamp(1.95rem,1.7rem + 1.25vw,2.66rem);
  --step-4: clamp(2.44rem,2rem + 2vw,3.55rem);
  --display: clamp(3rem,10vw,11rem);   /* scale ratio 1.25 */

  /* Spacing — 4px base */
  --s-1:4px; --s-2:8px; --s-3:12px; --s-4:16px; --s-6:24px;
  --s-8:32px; --s-12:48px; --s-16:64px; --s-24:96px; --s-32:128px;

  /* Grid */
  --grid-cols:12; --gutter:var(--s-6); --max:1440px;
  --page-pad:clamp(16px,4vw,64px);

  /* Motion — the 12 principles, as tokens */
  --ease-out:power2.out; --ease-in-out:power2.inOut;
  --ease-spring:back.out(1.6); --ease-impact:expo.in;
  --ease-settle:elastic.out(1,.5);
  --dur-micro:.18s; --dur-base:.36s; --dur-slow:.72s; --dur-cine:1.2s;
  --stagger:.06; --overshoot:1.6;
  --anticipation:.12s;      /* the counter-move before every impact */
  --follow-through:.06s;    /* per depth level of children */
  --shake-decay:.3s;
  --squash-y:.82;           /* --squash-x is 1/sqrt(--squash-y) */
}
html[data-shabbat="true"]{
  --smash-red:#7A2233; --yellow:#8C7F1E; --white:#CFC9BD; --near-black:#0D0C09;
}
html[data-shabbat="true"] *,
@media (prefers-reduced-motion:reduce){*{
  animation-duration:.01ms!important; animation-iteration-count:1!important;
  transition-duration:.01ms!important; scroll-behavior:auto!important;
}}
```

---

# 3D ASSET PLAN — THE BLENDER PART

## THE STYLE CONTRACT — paste this block into every image prompt, unchanged
```
[LENS] 85mm macro equivalent, f/3.2, camera slightly above the subject at a 25-30 degree angle
[LIGHT] one large soft key from back-left at 120 degrees, white bounce front-right at 15 percent, deep falloff into shadow
[PALETTE] near-black #13110C ground, Smash Red #E51144 accents only, warm #FEEB13 rim light on the top edge
[SURFACE] matte dark stone or seasoned black steel, a few real crumbs and sesame seeds scattered
[GRADE] high contrast, deep blacks, warm specular highlights, slight vignette
[GRAIN] fine 35mm grain at 3 percent
```
Every asset — photographed, rendered or generated — obeys this one block. Mixed lighting across assets is the loudest possible signal of an amateur site.

## THE KOSHER CONTRACT — paste into every food prompt, unchanged
```
Kosher meat restaurant. No dairy anywhere: all cheese is plant-based, with a matte melt and slightly less stringy pull than dairy cheese, never a glossy dairy sheen. No pork: "beef bacon" is deep red, thick-cut, with no white marbled fat strips. No butter, no cream, no milk products, no shellfish. Never show meat and cheese described as dairy in the same frame.
```

## From Blender — the 3D pipeline (real scans first)
| Asset | Output |
|---|---|
| Hero burger, 9 named layers | `/frames/desktop/smash_0001–0248.avif` · `/frames/mobile/smash_0001–0124.avif` · `/models/hero.glb` (≤3MB) · `/models/hero.usdz` |
| Cut halves + knife | Included in the sequence · `/models/halves.glb` (≤5MB) |
| Steam, sauce drip, loose sesame | Rendered into the frames; approximated in real-time as sprites/shaders |
| Kong arm pass | `/frames/kong/desktop/kong_0001–0019.avif` (alpha) · mobile equivalent |
| Poster + reduced-motion keys | `/frames/poster.avif`, `/frames/key/key_040|118|160|205.avif` |
| Blooming Onion | A 40-frame unfold sequence at 1200×1200, alpha, OR a real-time model — **whichever is produced; do not substitute a rotating photograph** |
| Menu mini-explode | 12-frame sequences at 800×800, alpha, one per featured item |

Capture instructions for the scans (what the client or photographer does by hand): buy three Loaded Smashed — one intact, one disassembled, one cut in half. Photograph each separately on a matte grey or black surface under flat, shadowless light. Use **photo/photogrammetry mode, not LiDAR** — LiDAR cannot resolve sesame seeds. Turntable plus a fixed phone on a tripod: three orbits at roughly 15°, 45° and 70° elevation, 40–60 photos each, 120–180 total per layer. Lock exposure, focus and white balance. Let the steam stop completely before shooting, and dull the shine on the sacrificial burger only — glossy highlights break photogrammetry.
