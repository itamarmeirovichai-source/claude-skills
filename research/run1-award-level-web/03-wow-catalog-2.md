CHATGPT MESSAGE 3 of 7 — RESEARCH RESULTS. These are the results of deep research into how award-level interactive websites (Awwwards / FWA level) are built. Study them carefully — this is your knowledge base from now on. Don't build anything yet. Reply only: "Got it — send the next part."

# B. WOW CATALOG (part 2 of 2 — W11–W22)

## W11 — STORYTELLING & GAMIFICATION
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| Scrollytelling | Pinned stage + a beat timeline; content states driven by one progress value | 5 | 3 | 2 | Y |
| Choose-your-path | State machine (XState or a reducer) + route or view transitions per branch | 4 | 3 | 1 | Y |
| Mini-game | Matter.js or Rapier loop inside a bounded canvas, lazy-loaded on interaction | 5 | 4 | 3 | Y |
| Keyboard easter egg | Buffer the last N `keydown` codes, compare to a word/Konami sequence | 3 | 1 | 1 | N |
| Explorable 3D world | Physics vehicle + camera follow + collision meshes (Bruno Simon's portfolio model) | 5 | 5 | 5 | Partial |
| Progress & achievements | `localStorage` badge state, revealed with a burst; never gate content behind it | 3 | 2 | 1 | Y |
| Scroll-driven data viz | D3 scales + GSAP-scrubbed path/bar values; always keep a data table for a11y | 4 | 3 | 2 | Y |
| 3D map / globe | Mapbox GL JS `flyTo`, MapLibre (open), or three-globe with instanced pins | 5 | 3 | 3 | Y (low zoom) |
| Interactive timeline | Horizontal pinned scroll + scrubbed milestone reveals | 3 | 2 | 1 | Y |
| Quiz / finder | 3–5 questions → weighted score → a real product recommendation | 4 | 2 | 1 | Y |
| Live configurator | State object → 3D layer visibility + price/summary; deep-linkable via URL | 5 | 4 | 3 | Y |
| Shareable creation | Render the user's config to a canvas → `toBlob` → Web Share API / OG image endpoint | 5 | 3 | 2 | Y |
| Try-it-yourself demo | Let the user operate the actual product mechanic in miniature | 5 | 4 | 3 | Y |

## W12 — SOUND & SENSES
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| Ambient soundtrack | Howler.js, muted by default, visible toggle, unlock on first gesture, fade on tab blur | 4 | 2 | 1 | Y |
| UI sound design | One sprite sheet, ≤80ms clips, ±3% random pitch to avoid machine-gun repetition | 4 | 2 | 1 | Y |
| Intensity-reactive sound | Map scroll velocity or hold duration to gain/playback rate (sizzle gets louder) | 5 | 3 | 1 | Y |
| Audio-reactive visuals | Web Audio `AnalyserNode` → frequency bins → shader uniforms | 4 | 3 | 2 | Y |
| Spatial audio | `PannerNode` positioned with the 3D camera | 3 | 3 | 2 | Y |
| Haptics | `navigator.vibrate()`; Android only — design so its absence changes nothing | 2 | 1 | 1 | Partial |

## W13 — ALIVE & PERSONAL
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| Time-of-day theme | Local hour (or venue timezone) → CSS variable palette + different hero lighting | 4 | 2 | 1 | Y |
| Weather-reactive | Server-fetch a weather API by venue coords, cache 30min → visual state | 4 | 2 | 1 | Y |
| Mascot reacts to real state | Rive inputs bound to open/closed/holiday booleans computed server-side | 5 | 3 | 1 | Y |
| Live signage | Neon/sign element whose animation state equals real business state | 5 | 2 | 1 | Y |
| Animated theme toggle | View Transitions circular wipe from the toggle's coordinates | 3 | 1 | 1 | Y |
| Live counters / real data | Server component revalidating on an interval; never fake a number | 3 | 2 | 1 | Y |
| Multiplayer presence | PartyKit / Liveblocks cursors — only where a crowd feels right | 4 | 3 | 2 | N |
| Returning-visitor memory | `localStorage` last-order or last-viewed → a different greeting and CTA | 4 | 2 | 1 | Y |
| Personalised content | UTM/referrer-driven hero copy variant, server-rendered | 3 | 2 | 1 | Y |

## W14 — CAMERA, AR & EMERGING
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| AR product view | `<model-viewer ar>` with GLB + USDZ pair → Scene Viewer / AR Quick Look | 5 | 2 | 2 | Y |
| WebXR | `three/webxr` immersive-ar session for custom AR | 5 | 5 | 4 | Partial |
| Face / hand tracking | MediaPipe Tasks Vision FaceLandmarker — attach props to landmark indices | 5 | 4 | 4 | Y (tap-to-start only) |
| Voice control | Web Speech API `SpeechRecognition` — Chrome/Safari only, always a typed fallback | 3 | 2 | 1 | Partial |
| Device motion | `DeviceOrientationEvent` with iOS permission gesture | 4 | 2 | 1 | Y |
| WebGPU compute | TSL `Fn` compute nodes for particles/physics at 10× WebGL counts | 5 | 5 | 3 | Y (fallback) |
| Real-time AI visuals | Edge model or streamed generation — still slow/expensive; treat as experimental | 4 | 5 | 5 | N |

## W15 — ART DIRECTION & CRAFT (what looks $100k with animation OFF)
- **Type pairing & scale:** one display face + one workhorse UI face. A real scale ratio (1.25 or 1.333). Display sizes big enough to feel like a poster (clamp up to 8–14vw).
- **Grid & composition:** a 12-column grid you deliberately break. Asymmetry, overlap, one dominant focal point per screen.
- **Whitespace & pacing:** alternate dense and empty screens; a full-bleed image after a quiet type screen reads as a cut.
- **Colour system:** 1 brand hero, 1 accent, 1 near-black, 1 paper. Tints/shades only — never invent new hues. Check every pair for 4.5:1.
- **Texture & grain:** a 2–4% noise overlay and paper/metal textures kill the "default Tailwind" look instantly.
- **Photo & 3D art direction:** one light direction, one lens language, one colour grade across every asset. Mixed sources are the #1 tell of a cheap site.
- **Copywriting:** the brand's actual voice, short lines, verbs, no "Welcome to our website".
- **Brand motion language:** one ease, one duration scale, one stagger — written down and obeyed.
- **Details:** animated favicon, custom scrollbar, `::selection` colour, designed 404, designed loading/empty states, a footer worth reaching.

## W16 — ENGINEERING & PERFORMANCE FOR THE WOW
| Item | Practice |
|---|---|
| Stack | Next.js (App Router) / Nuxt / Astro (content-heavy) / SvelteKit; Webflow+GSAP when the client must edit; Framer for speed-to-market |
| GPU tiering | `detect-gpu` → tier 0/1 = static poster, tier 2 = reduced scene, tier 3 = full |
| Lazy heavy scenes | `IntersectionObserver` + dynamic `import()` ~1 viewport ahead; never in the initial bundle |
| Code splitting | Route-level + component-level; keep first-load JS under ~150KB gzip |
| Compression | Draco for geometry, Meshopt for animation-heavy meshes, KTX2/Basis for textures, AVIF for frames |
| Off-screen | Pause `renderer.setAnimationLoop` when the canvas leaves the viewport or the tab blurs |
| Workers | `OffscreenCanvas` + worker for physics/particles; `createImageBitmap` decoding off the main thread |
| Reduced motion | Every timeline has a `matchMedia("(prefers-reduced-motion: reduce)")` branch that still tells the story |
| SEO under WebGL | Real DOM headings and copy behind or above the canvas; canvas gets `aria-hidden` + a text alternative |
| Core Web Vitals | LCP <2.5s, INP <200ms, CLS <0.1 — measured on a mid-range Android, not a MacBook |
| Safari/iOS quirks | Low Power Mode throttles rAF and blocks autoplay; `svh/lvh/dvh` for the address bar; no `100vh` |
| Touch parity | Every hover effect has a tap/scroll-into-view equivalent; no functionality behind hover |

## W17 — CONVERSION
- The signature moment must **end** on the CTA — the last frame of the sequence resolves into the order button.
- An interactive demonstration of the product outsells decoration: let people build, stack, configure, taste with their eyes.
- Sticky CTA on mobile from the first scroll; never covered by the effect layer.
- Animated social proof (real reviews, real counts) beats claims.
- Never hide value behind a long preloader — show the hero and CTA the moment they're ready.
- Never delay an order click for an animation: open the destination immediately, play the flourish on the page being left.

## W18 — 3D PRODUCT STORYTELLING, EXPLODED VIEWS & CROSS-SECTIONS
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| Multi-object toss | Per-object ballistic arc (`y = v0·t − ½g·t²`) with distinct v0, spin axis, phase offset | 5 | 3 | 3 | Y |
| Decaying spin | Angular velocity × `exp(-k·t)`, then blend to a target quaternion so it lands facing camera | 5 | 3 | 1 | Y |
| Exploded view | Per-layer offset along a shared axis × `progress`, staggered `delay`, `back.out(1.6)` overshoot, small per-layer tilt | 5 | 3 | 2 | Y |
| Pinned 3D callouts | drei `<Html occlude>` or project world→screen each frame and position DOM labels | 4 | 2 | 2 | Y (fewer) |
| Cross-section cut | Blade + clipping plane with a stencil cap pass, OR pre-modelled halves with real interior faces | 5 | 4 | 3 | Y |
| Turntable / orbit | Camera on a circle, `lookAt` target, eased angle from progress | 3 | 1 | 1 | Y |
| Reversibility | Everything is a pure function of `progress` — no `once`, no accumulated state | 5 | 2 | 1 | Y |

**The four ways to build a whole sequence** (detail in message 5):
| | Realism | Smoothness | Size | Build time | Mobile |
|---|---|---|---|---|---|
| (a) Real-time glTF, named layer meshes | Medium | High | 2–8MB | Medium | Good |
| (b) Blender Cycles image sequence on canvas | **Highest** | **Highest** | 8–30MB | High | Good (fewer frames) |
| (c) Layered transparent PNGs + CSS 3D/GSAP | Low–Medium | High | 1–4MB | Low | Good |
| (d) Gaussian splats | High (captured) | Medium | 15–80MB | Medium | Poor |

**The rule:** path-traced renders beat real-time WebGL for food — subsurface buns, glossy sauce, melted cheese and volumetric steam are exactly what real-time can't fake. Deterministic scroll sequences (the user only controls time) should use rendered frames. Interactive moments (the user controls state) need real-time, baked from the same Blender scene so the look matches.

## W19 — SMOOTHNESS ENGINEERING
| Rule | Setting |
|---|---|
| One rAF loop | Lenis driven by `gsap.ticker`; `gsap.ticker.lagSmoothing(0)`; R3F `frameloop` also ticked from it or left to drei |
| Scrub smoothing | `scrub: 1` (≈1s catch-up) for cinematic scrubs; `scrub: true` only for hard-locked bars |
| Damping | `lerp(current, target, 1 - Math.pow(0.001, dt))` — frame-rate independent, never a raw `0.1` factor |
| Animate only | `transform` and `opacity`. Never `top/left/width/height/margin/filter` in a scroll loop |
| `will-change` | Only on the 1–3 elements actually animating, removed afterwards |
| No layout thrash | Read all geometry once in `ScrollTrigger.refresh`/`onResize`, cache it, write only in the loop |
| Listeners | `{passive: true}` on wheel/touch; never `preventDefault` on scroll unless truly pinning |
| Preload ahead | Decode heavy assets ≥1 viewport before entry; `createImageBitmap()` off-thread |
| DPR cap | `Math.min(devicePixelRatio, 2)` desktop, `1.5` mobile; drop to 1 under load |
| Render on demand | Only render when something changed; pause off-screen and on tab blur |
| No GC spikes | Reuse `Vector3`/`Quaternion`/arrays; no allocation inside the frame loop |
| Textures | KTX2/Basis, mipmaps on, power-of-two where it matters |
| Fonts | `font-display: swap` + `<link rel="preload" as="font" crossorigin>` + `size-adjust` fallback to kill shift |
| Viewport units | `dvh`/`svh`/`lvh`, never `100vh`, on iOS |
| Long pages | `content-visibility: auto` + `contain-intrinsic-size` on far-below sections |
| 120Hz | Never assume 16.7ms — use real `delta`; ProMotion budget is 8.3ms |
| Reduced motion | A designed alternative (crossfades, static key frames), not "animations off" |
| Measure | Chrome Performance panel (look for long tasks >50ms and dropped frames), Lighthouse + real INP, a real iPhone and a mid-range Android, not a simulator |

## W20 — FOOD & BRAND PLAYFULNESS
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| Sauce drip | Rendered in Blender (fluid/metaball) for hero; 2D metaball shader for interactive | 5 | 4 | 3 | Y |
| Cheese pull | Blender cloth/softbody for hero; a stretched shader plane with noise UVs real-time | 5 | 4 | 3 | Y |
| Fries / crumbs / sesame | `InstancedMesh` + Rapier rigid bodies, or Matter.js in 2D; sleep on rest | 4 | 3 | 3 | Y (cap) |
| Steam & smoke | Cycles volumetrics for renders; animated soft sprites + noise for real-time | 5 | 3 | 3 | Y |
| Heat haze | Screen-space UV distortion masked to the griddle, intensity from scroll speed | 4 | 2 | 2 | Y |
| Sizzle sound design | Layered real recordings, gain mapped to interaction intensity | 5 | 2 | 1 | Y |
| Hold-to-interact | rAF accumulator → deformation amount + audio gain + haptic; a "perfect" window | 5 | 3 | 1 | Y |
| Stamp / slam | Scale 3→1 with `expo.in`, 1-frame squash, dust particles, camera shake, thud | 5 | 2 | 1 | Y |
| Product-themed transitions & cursors | Brand objects as the transition shape and the cursor | 5 | 2 | 1 | Partial |
| Rive mascot | State machine with `hover`, `click`, `isOpen`, `isShabbat` inputs | 5 | 3 | 1 | Y |
| Branded mini-game | Bounded canvas, lazy-loaded, skippable, no prize claims without approval | 4 | 4 | 3 | Y |

## W21 — ANIMATION PRINCIPLES (Disney's 12, mapped to code)
| Principle | Web implementation |
|---|---|
| Squash & stretch | Non-uniform `scaleX/scaleY` preserving volume (`sx = 1/√sy`) at impact and peak speed |
| Anticipation | A 60–120ms counter-move before the main action (`back.in` prefix, pull back before a slam) |
| Staging | One focal point per beat; dim/blur/desaturate everything else (DOF, `filter` on a static layer only) |
| Follow-through & overlap | Child elements lag the parent by 40–80ms; `stagger` plus a slightly longer duration per depth level |
| Slow in / slow out | Never `linear` except for constant motion; default `power2.out` in, `power2.inOut` for moves |
| Arcs | `MotionPathPlugin` or a quadratic bezier; nothing organic travels in a straight line |
| Secondary action | Sesame seeds shake while the burger spins; the badge wobbles after the stamp lands |
| Timing | Small/light = 150–250ms; medium = 300–450ms; hero/cinematic = 600–1200ms |
| Exaggeration | Push scale/rotation 15–25% past the "correct" value at the peak, then settle |
| Solid drawing | Consistent perspective and light direction across DOM, 3D and rendered frames |
| Appeal | Character in the motion: a mascot's idle loop, an overshoot with personality |
| Straight-ahead vs pose-to-pose | Physics sims = straight-ahead; scroll beats = pose-to-pose keyframes at labelled beats |

## W22 — CINEMATIC CAMERA LANGUAGE & FOOD-COMMERCIAL DIRECTION
| Move | Implementation |
|---|---|
| Speed ramp / slow motion | Remap scroll progress through a non-linear curve so the action's peak occupies more scroll distance (`t' = CustomEase(t)`) |
| Bullet time | Freeze object animation time while the camera angle keeps advancing with progress |
| Push-in | Move the camera on its forward axis, do **not** change FOV (that's a zoom, it flattens) |
| Macro close-up | Short focus distance + wide aperture → `bokehScale`; in Blender, real DOF with a 100mm macro |
| Rack focus | Animate `focusDistance` between two targets over 400–700ms |
| Whip pan | Fast yaw + directional motion blur + a 2-frame smear; hides a cut |
| Dolly zoom | Move camera back while increasing FOV so the subject stays the same size |
| Camera shake | Perlin noise on position + rotation, amplitude decaying over ~300ms, scaled by impact force |
| One continuous take | A single camera path across all beats of a pinned section — never cut inside the hero sequence |
| Match cut | Shape/position continuity: a round cut face becomes a round button (GSAP Flip) |
| Food vocabulary | Toss, flip, splash, drip, pull, steam rise, cross-section reveal, hero rotation, pour, sear |

---
## Verified reference sites (checked; awards as reported on Awwwards)
- **Lando Norris official site** — Awwwards Site of the Year 2025, built by OFF+BRAND.
- **Messenger** — Awwwards Site of the Year 2025; a small real-time WebGL planet with a delivery character.
- **Crav Burgers** — Awwwards Site of the Day; playful burger-ordering concept, immersive visuals + motion design. https://www.awwwards.com/sites/crav-burgers
- **Promeat** — Awwwards Honorable Mention; meat brand, editorial + WebGL storytelling. https://www.awwwards.com/sites/promeat
- **Good Meat** — Awwwards-featured digital food experience; tagged 3D, WebGL, Three.js, GLSL, Vue, sound design, storytelling.
- **EverSwap (Lusion)** — Awwwards Site of the Day + Developer Award, June 2026.
- **Apechain (makemepulse)** — Awwwards Site of the Day + Developer Award.
- **The Power of Storytelling (Noomo Agency)** — Awwwards Site of the Day + Developer Award.
- **Steven.com (OFF+BRAND)** — Awwwards Site of the Day + Developer Award.
- **Hubtown (Unseen Studio)** — Awwwards Site of the Day + Developer Award.
- **Springs (Vide Infra)** — Awwwards Site of the Day + Developer Award, March 2026.

Treat any stack attribution for these as **inferred** unless the studio published a case study.
