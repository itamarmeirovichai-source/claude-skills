CHATGPT MESSAGE 2 of 8 — THE EXAMPLE SITE. Continue applying the spec exactly. Don't build yet — wait until you have all 8 parts.

# 6. THE SIGNATURE SEQUENCE — "THE TOSS, THE SMASH, THE CUT"

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
