CHATGPT MESSAGE 4 of 7 — RESEARCH RESULTS. These are the results of deep research into how award-level interactive websites (Awwwards / FWA level) are built. Study them carefully — this is your knowledge base from now on. Don't build anything yet. Reply only: "Got it — send the next part."

# C. ASSET TOOLKIT
For every asset type: best source · commercial status · a reusable prompt/capture formula · how to match an existing brand's style.

## The style contract (write once, paste into every prompt)
Before generating anything, extract from the client's existing photos and write a fixed block reused verbatim:
`[LENS] 85mm macro, f/2.8, slight top-down 30° angle · [LIGHT] one large soft key from back-left at 45°, white bounce front-right, deep falloff · [PALETTE] #E51144 accents, #13110C background, warm #FEEB13 rim · [SURFACE] matte black stone, subtle crumbs · [GRADE] high contrast, deep blacks, warm highlights, slight vignette · [GRAIN] fine 35mm grain 3%`
Everything — AI images, real photos, Blender renders — must obey that one block. Mixed lighting across assets is the single loudest signal of an amateur site.

## 1. Photography (general)
- **Source:** real shoot. Phone in ProRAW/RAW, tripod, 2s timer, manual WB locked to one Kelvin value for the whole shoot.
- **Commercial:** yours outright if you shoot it; get a property/model release for people and interiors.
- **Formula:** one big soft source (window or a 60cm softbox) at 45–135° behind the subject, white foamcore bounce opposite, black flag to deepen the shadow side. Never on-camera flash, never overhead fluorescents.
- **Match a brand:** sample 5 of their existing photos in a colour picker, note background, light direction and crop ratio, then reproduce exactly.

## 2. Food shots (hero)
- **Source:** real shoot with a stand-in "hero" build, plus a backup AI/CG version for angles you couldn't get.
- **Formula:** back-side key light so sauce and grease read as specular highlights; a spray bottle of water for freshness on veg; brush oil on the crust; shoot within 90 seconds of assembly; f/4–5.6 and focus-stack 3–5 frames for a fully sharp burger; 50–85mm equivalent to avoid bulging.
- **Prompt (AI fallback):** `Photorealistic macro food photograph of [dish, exact real build listed ingredient by ingredient], [STYLE CONTRACT], steam rising subtly, glossy sauce catching the rim light, sesame seeds sharply defined, shallow depth of field, commercial food photography, no text, no logos, no hands`
- **Kosher constraint:** for a kosher meat brand, never generate melted dairy cheese, cream sauces, butter sheen or pork/bacon of pig origin. Specify: `plant-based cheese with a matte melt, beef bacon (dark red, thick-cut, no marbled white fat strips)`.

## 3. Illustration
- **Source:** the brand's existing illustration library first; then a vector artist; then AI with the brand's own art as reference.
- **Prompt:** `Flat vector illustration, thick uniform outline 4px, limited palette [hex list], [brand character] in [pose], bold retro-cartoon style, flat fills, no gradients, transparent background, SVG-like`
- **Match:** trace one existing brand illustration to derive stroke weight, corner radius and palette, then state those numbers in the prompt.

## 4. Icons
- **Source:** Lucide / Phosphor (MIT, free commercial) for UI; custom-drawn for brand moments. Always SVG, 24px grid, 1.5–2px stroke.
- **AI:** unreliable for icon sets — inconsistent stroke and optical size. Draw or buy.

## 5. Video
- **Source:** real capture (phone 4K60, ND filter, gimbal or tripod slider) → graded in Resolve (free).
- **AI:** Veo 3.x for realism and native audio; Kling 3.0 for motion and 4K; Runway when you need clear ownership on a paid plan. Commercial rights exist on paid tiers of all of these, but **rights differ by provider and change** — read the terms on the day you generate and save a copy.
- **Prompt:** `[STYLE CONTRACT] Slow-motion 120fps macro shot of [action], camera pushes in 20cm over 3 seconds, shallow depth of field, one large soft key from back-left, black background, no text, no people`
- **Rule:** AI video is for atmosphere and B-roll. The hero product shot is real or path-traced — AI food video still fails on cheese physics and bite continuity.

## 6. Animated stills (cinemagraph)
- **Source:** shoot a static frame + mask the moving region (steam, drip) and loop only that. Or Blender: render 60–120 frames of just the steam layer as a transparent AVIF sequence over a still.
- **Format:** AVIF sequence or an 8-bit WebM with alpha; never a GIF.

## 7. 3D model (general)
- **Source:** Blender, modelled or scanned. Poly Haven (CC0) for HDRIs, textures and props. Sketchfab only with a licence explicitly allowing commercial use.
- **AI 3D:** Meshy, Hunyuan3D, Rodin — acceptable for background props, never for a hero close-up (topology and UVs are unusable).
- **Web export:** glTF 2.0 → Draco (geometry) → `gltf-transform` Meshopt + KTX2 (textures) → target ≤3MB for a hero object.

## 8. Layered 3D model (for exploded views)
- Model each layer as a **separate object with its own origin at its own centre**, named per a written contract (`bun_top`, `sauce`, `onion`, `bacon`, `cheese_a`, `patty_a`, `cheese_b`, `patty_b`, `bun_bottom`).
- Keep the stack axis exactly +Z so one offset vector drives the whole explode.
- Export all layers in **one glTF** with the names preserved (`Export → Include → Custom Properties`, and don't let the exporter rename duplicates).

## 9. 3D model with a cut interior
- **Best:** pre-model both halves with real interior geometry — a separate material for the cut face, with the seared crust, patty fibres, melted cheese and sauce actually modelled/textured. A boolean at render time produces a flat, fake-looking face.
- **Real-time alternative:** `THREE.Plane` clipping + a stencil cap pass so the hollow doesn't show; the cap gets a flat interior material. Acceptable for interactive, not for the hero.

## 10. Animated mascot
- **Source:** the brand's existing character art → rigged in **Rive** (state machine, tiny `.riv`, GPU-cheap, JS-drivable inputs). Lottie only for non-interactive illustration.
- Inputs to expose: `hover`, `click`, `scrollVelocity`, and real-world booleans (`isOpen`, `isClosedForShabbat`, `isHoliday`).

## 11. Music
- **Source:** licensed library (Musicbed, Artlist, Epidemic — check the plan covers client work) or a composer.
- **AI:** Suno/Udio on a commercial tier; verify the tier grants commercial rights before shipping.
- **Rule:** off by default, with a visible toggle. Loop points must be sample-accurate or the loop is worse than silence.

## 12. SFX
- **Source:** record them. A sizzle is a frying pan and a phone 30cm away. A thud is a book on a table. This is 20 minutes of work and beats any library.
- **Library:** Freesound (check each file's CC licence individually — they differ per file), Epidemic SFX.
- **Processing:** trim to ≤80ms for UI, normalise to −6dBFS, high-pass at 80Hz, export as a single Howler sprite.

## 13. Voice
- ElevenLabs on a commercial tier, or a real VO artist for anything customer-facing. Always ship captions.

## Rights ledger (required deliverable)
One table shipped with every project: `asset path | type | source (shoot/scan/Blender/stock/AI) | tool + plan tier | date | licence text or URL | where used`. An asset with no row does not ship.

---

# D. SMOOTHNESS PLAYBOOK

## The single-loop rule
```js
import Lenis from 'lenis'                    // 1.3.x
import gsap from 'gsap'
import ScrollTrigger from 'gsap/ScrollTrigger'
gsap.registerPlugin(ScrollTrigger)

const lenis = new Lenis({
  lerp: 0.1,              // default; 0.075 feels heavier, 0.15 snappier
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smoothWheel: true,
  syncTouch: false,       // leave native touch scrolling alone unless you need infinite scroll
  touchInertiaExponent: 1.7,
})
lenis.on('scroll', ScrollTrigger.update)
gsap.ticker.add((time) => lenis.raf(time * 1000))
gsap.ticker.lagSmoothing(0)
```
`syncTouch: true` is only for infinite-scroll, and it is unstable on iOS < 16.

## Default settings
| Thing | Default |
|---|---|
| Lenis lerp / duration | 0.1 / 1.2s; `wheelMultiplier` 1, `touchMultiplier` 1.5 |
| ScrollTrigger scrub | `1` for cinematic, `0.5` for tight UI, `true` only for progress bars |
| ScrollTrigger pin | `anticipatePin: 1`, `pinSpacing: true`, `invalidateOnRefresh: true` |
| ScrollTrigger refresh | `ScrollTrigger.config({ ignoreMobileResize: true })` — stops iOS address-bar refreshes |
| GSAP defaults | `gsap.defaults({ ease: 'power2.out', duration: 0.6 })` |
| Stagger | `{ each: 0.06, from: 'start' }` |
| Overshoot | `back.out(1.6)` for springy arrivals; `elastic.out(1, 0.4)` only for playful brands |
| R3F | `dpr={[1, 2]}` desktop / `[1, 1.5]` mobile, `frameloop="demand"` where nothing moves by itself, `gl={{ antialias: false, powerPreference: 'high-performance' }}` + FXAA/SMAA in post |
| Renderer | `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`, shadows off unless baked, `toneMapping: ACESFilmicToneMapping` |
| Physics | Rapier `timeStep: 1/60`, `sleepThreshold` on, bodies capped (desktop 150 / mobile 60) |
| Frame damping | `const k = 1 - Math.pow(0.001, dt); v += (target - v) * k` — never a fixed 0.1 |

## Anti-patterns (each one visibly cheapens a site)
1. Two rAF loops (Lenis's own + GSAP's) — guarantees micro-jitter.
2. Animating `width`, `height`, `top`, `left`, `margin`, `box-shadow` or `filter: blur()` in a scroll handler.
3. Reading `getBoundingClientRect()` inside the loop (layout thrash). Cache on refresh.
4. `will-change: transform` on dozens of elements — exhausts GPU memory and slows everything.
5. Decoding the next image sequence frame on the main thread at draw time. Decode ahead with `createImageBitmap`.
6. `100vh` on iOS; use `100svh`/`100dvh`.
7. Uncapped DPR on a 3× phone screen — 9× the pixels for nothing.
8. Rendering the WebGL scene while it's off-screen or the tab is hidden.
9. Allocating `new THREE.Vector3()` per frame → GC sawtooth every few seconds.
10. Loading all 300 sequence frames before showing anything — loads slowly and janks anyway.
11. Adding `scroll` listeners without `{passive:true}`.
12. `prefers-reduced-motion` handled by disabling everything, leaving a broken empty section.
13. Big `blur()`/`backdrop-filter` regions on mobile — the cheapest way to drop to 30fps.
14. Fonts without preload → FOUT shift on the LCP text.

## How to measure
1. **Chrome Performance panel** — record a 6s scroll through the section. Look for: frames >16.7ms (>8.3ms on ProMotion), long tasks >50ms (yellow), forced reflows (purple "Layout" inside "Recalculate Style"), and GC sawtooth in the memory track.
2. **Lighthouse (mobile preset)** for LCP/CLS, plus **real INP** from field data (CrUX / `web-vitals` library reporting to analytics).
3. **`renderer.info`** — draw calls (target <150 mobile / <300 desktop), triangles, texture memory.
4. **Real devices, always:** one real iPhone (also test in Low Power Mode — it throttles rAF and blocks autoplay) and one mid-range Android (a ~$250 phone, not a flagship). Emulated throttling is not a substitute.
5. **Acceptance gate:** the section is not done until a mid-range Android holds 60fps through the whole scroll and the CPU-throttled (4×) profile has no long task over 50ms.
