CHATGPT MESSAGE 2 of 7 — RESEARCH RESULTS. These are the results of deep research into how award-level interactive websites (Awwwards / FWA level) are built. Study them carefully — this is your knowledge base from now on. Don't build anything yet. Reply only: "Got it — send the next part."

# B. WOW CATALOG (part 1 of 2 — W1–W10)
Columns: **WOW** 1–5 (impact) · **Eff** 1–5 (build effort) · **Perf** 1–5 (performance risk) · **Mob** = works on mobile. Verified example links are listed at the end of message 3.

## W1 — SCROLL & SCROLLYTELLING
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| Inertial smooth scroll | Lenis 1.3.x, lerp 0.1, driven by `gsap.ticker`, `lagSmoothing(0)` | 3 | 1 | 2 | Y (leave native touch) |
| Scroll-scrubbed timeline | GSAP ScrollTrigger `scrub: 1`, one master timeline per pinned section | 5 | 2 | 2 | Y |
| Native CSS scroll animation | `animation-timeline: scroll()/view()` — zero JS, main-thread-free | 3 | 1 | 1 | Y (Chrome/Safari 26; Firefox flagged) |
| Pinned sections | `ScrollTrigger {pin, anticipatePin:1, pinSpacing:true}` | 4 | 2 | 2 | Y |
| Horizontal scroll section | Pin + `x: -(width - innerWidth)` scrubbed | 4 | 2 | 2 | Y |
| Scroll-snap | CSS `scroll-snap-type: y mandatory` + `scroll-snap-align` | 2 | 1 | 1 | Y |
| Apple-style image sequence | Canvas + preloaded `ImageBitmap` array, frame index from scroll progress | 5 | 3 | 3 | Y (fewer frames) |
| Scrubbed video | `video.currentTime` from progress — fragile; prefer frames | 3 | 2 | 4 | N (iOS seeks badly) |
| Multi-layer parallax | Different `y` speeds per layer in one scrubbed timeline; transform only | 3 | 1 | 1 | Y |
| Velocity skew / stretch | `ScrollTrigger.getVelocity()` → `skewY`, quickTo back to 0 | 4 | 2 | 2 | Y |
| Reveal on enter | ScrollTrigger `once:true` + stagger; never animate more than 1 screen ahead | 3 | 1 | 1 | Y |
| Number counters | GSAP tween on a proxy object + `Intl.NumberFormat` in `onUpdate` | 2 | 1 | 1 | Y |
| Text fills as you read | SplitText chars + `background-clip: text` mask width scrubbed | 4 | 2 | 1 | Y |
| Stacking cards | Sticky positioning + scale/`y` per index, last card on top | 4 | 2 | 1 | Y |
| Zoom-through transition | Scale one element to 20× while fading siblings, next scene behind | 5 | 3 | 3 | Y |
| Infinite loop scroll | Modulo-wrapped positions + `ScrollTrigger` proxy; `syncTouch:true` needed | 4 | 4 | 3 | Y |
| SVG path draw | DrawSVG (free) or `stroke-dashoffset` scrubbed | 3 | 1 | 1 | Y |
| Scroll progress indicator | `scaleX` from `ScrollTrigger` progress, or pure CSS `scroll()` timeline | 2 | 1 | 1 | Y |

## W2 — 3D & WEBGL
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| Three.js scene | r180+, `WebGPURenderer` with automatic WebGL2 fallback, TSL for shaders | 5 | 4 | 4 | Y (capped) |
| React Three Fiber + drei | Declarative scene graph; drei for `<Html>`, `useGLTF`, `Environment` | 5 | 3 | 4 | Y |
| OGL / lightweight | ~10KB alternative when you only need a full-screen shader plane | 3 | 3 | 2 | Y |
| Babylon.js / PlayCanvas | Engine-grade: physics, editor, better for game-like sites | 4 | 4 | 4 | Y |
| Spline | Designer-built 3D, exports a runtime — fast to make, heavy to ship | 3 | 1 | 4 | Y |
| `<model-viewer>` | One tag, GLB + USDZ, free AR on iOS/Android | 3 | 1 | 2 | Y |
| Scroll camera path | Theatre.js or a CatmullRom curve sampled by scroll progress | 5 | 3 | 3 | Y |
| Product viewer / configurator | OrbitControls with damping + material swap on state | 4 | 3 | 3 | Y |
| PBR + HDRI | `.hdr`→`.exr`→KTX2 env map, `MeshPhysicalMaterial`, `envMapIntensity` | 4 | 2 | 3 | Y |
| Glass / transmission | `transmission`, `thickness`, `ior`, `roughness` — expensive, use one object | 4 | 2 | 5 | N (fallback) |
| Baked lighting | Bake Cycles light into textures → `MeshBasicMaterial`; near-zero GPU cost | 5 | 3 | 1 | Y |
| Instancing | `InstancedMesh` above ~50 copies; one draw call for 10k sesame seeds | 4 | 2 | 1 | Y |
| GPU particles / GPGPU | Positions in a FloatTexture, ping-pong FBO, morph targets between shapes | 5 | 5 | 4 | Y (fewer) |
| 3D physics | Rapier (Rust/WASM, fast) > cannon-es; sleep bodies aggressively | 5 | 4 | 4 | Y (cap bodies) |
| 3D text | Troika-three-text (SDF, crisp, cheap) not extruded geometry | 3 | 2 | 2 | Y |
| Gaussian splats | `.ply`/`.splat` via a splat renderer — photoreal capture, no relighting | 5 | 3 | 5 | N |
| WebGPU + TSL | Compute shaders, MRT post stack; ~95% coverage with WebGL2 fallback | 4 | 4 | 3 | Y |
| Blender → web pipeline | glTF → Draco (geometry) → Meshopt → KTX2/Basis (textures) + LODs | 5 | 3 | 1 | Y |

## W3 — SHADERS & GENERATIVE VISUALS
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| Animated mesh gradient | Simplex noise displacing a subdivided plane's vertex colours | 4 | 2 | 2 | Y |
| Grain / film noise | Cheap hash noise in the fragment shader or a tiled PNG overlay | 3 | 1 | 1 | Y |
| Mouse-reactive fluid | Navier–Stokes ping-pong FBO simulation at quarter resolution | 5 | 5 | 4 | Y (half-res) |
| Metaballs / blobs | 2D signed-distance smooth-min in a fragment shader | 4 | 3 | 2 | Y |
| Liquid / ripple distortion | UV offset by a displacement texture, decayed each frame | 4 | 2 | 2 | Y |
| Heat haze | Animated noise offsetting screen UVs in a masked region | 4 | 2 | 2 | Y |
| Holographic / foil | Fresnel × iridescent gradient driven by view angle + device tilt | 5 | 3 | 2 | Y |
| Neon glow + flicker | Emissive material + `UnrealBloomPass` + a noise-driven intensity curve | 4 | 2 | 3 | Y |
| Displacement maps | `MeshStandardMaterial.displacementMap` or vertex shader offset | 3 | 2 | 2 | Y |
| Raymarching / SDF | Full-screen quad, distance functions, sphere tracing — very GPU heavy | 5 | 5 | 5 | N |
| Dither / halftone / ASCII | Bayer matrix or glyph atlas sampled in a post pass | 4 | 2 | 2 | Y |
| Pixel sorting | Compute or multi-pass sort on the framebuffer | 4 | 4 | 4 | N |
| Flow fields | Curl noise advecting particle positions | 4 | 3 | 3 | Y |
| Reaction–diffusion | Gray–Scott ping-pong at low res, upsampled | 4 | 4 | 4 | N |
| Generative canvas art | p5.js or raw canvas2D, seeded per visitor | 3 | 2 | 2 | Y |
| Post-processing | `postprocessing` (pmndrs) EffectComposer: bloom, DOF, motion blur, CA, vignette, grain — merge into one pass | 4 | 2 | 4 | Y (bloom off) |

## W4 — IMAGE & VIDEO EFFECTS
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| WebGL hover distortion | Two textures + displacement map, `progress` uniform tweened by GSAP | 4 | 3 | 2 | N (tap version) |
| Cursor image trail | Pool of ~12 images, `quickTo` follow with per-index delay | 4 | 2 | 2 | N |
| Clip-path / curtain reveal | `clip-path: inset()` or `polygon()` animated; GPU-friendly | 4 | 1 | 1 | Y |
| Scale-on-scroll images | Image at 1.2 scale inside `overflow:hidden`, scrubbed to 1.0 | 3 | 1 | 1 | Y |
| Depth-map fake 3D photo | Grayscale depth map offsets UVs by mouse/gyro parallax | 5 | 3 | 2 | Y (gyro) |
| Image → particles | Sample pixel colours into an `InstancedMesh` / GPGPU texture | 5 | 4 | 4 | Y (fewer) |
| Before/after slider | `clip-path: inset(0 X% 0 0)` + draggable handle, pointer events | 3 | 1 | 1 | Y |
| Hover-to-play video | `preload="none"`, play on pointerenter, pause+reset on leave | 3 | 1 | 2 | N |
| 360° panorama | Equirectangular texture on an inverted sphere | 3 | 2 | 2 | Y |
| FLIP lightbox expand | GSAP Flip: record state → change DOM → `Flip.from()` | 5 | 2 | 1 | Y |
| Video masked in text | SVG `<mask>` with text, or `background-clip:text` over a video | 4 | 2 | 2 | Y |
| WebGL slider transition | Render-target crossfade with a noise/wave mask | 4 | 3 | 3 | Y |

## W5 — TYPOGRAPHY & TEXT MOTION
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| Split-text reveals | GSAP SplitText (free since 2025; rewritten, ~50% smaller) `type:"lines,words,chars"` + `mask:"lines"` | 4 | 1 | 1 | Y |
| Scramble / decode | ScrambleTextPlugin (free), charset matched to brand | 3 | 1 | 1 | Y |
| Typewriter | TextPlugin with a blinking caret pseudo-element | 2 | 1 | 1 | Y |
| Variable font axes | Animate `font-variation-settings` `wght`/`wdth` on hover/scroll | 4 | 2 | 2 | Y |
| Velocity squash type | Scroll velocity → `scaleY`/`wdth` axis, spring back to rest | 5 | 2 | 1 | Y |
| Kinetic typography | Timeline of word-level transforms synced to audio or scroll | 4 | 3 | 2 | Y |
| Text on a path | SVG `<textPath>` + animated `startOffset` | 3 | 1 | 1 | Y |
| Giant marquee | Duplicated track, `xPercent:-50` infinite, direction flips with scroll velocity | 3 | 1 | 1 | Y |
| Rotating words | Stack in a clipped box, `y` stagger with overlap | 3 | 1 | 1 | Y |
| Per-letter hover physics | Per-char magnetic offset via `quickTo`, neighbours falling off by distance | 4 | 2 | 2 | N |
| Gooey / dripping letters | SVG `feGaussianBlur` + `feColorMatrix` goo filter, or SDF shader | 4 | 3 | 3 | Y (limit) |
| Outline → fill | Two stacked copies, top one `clip-path` animated | 3 | 1 | 1 | Y |
| Fluid type | `clamp(1.5rem, 4vw + 0.5rem, 6rem)` — no breakpoints needed | 2 | 1 | 1 | Y |

## W6 — CURSOR & POINTER
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| Custom cursor | Fixed div, `gsap.quickTo` x/y, `mix-blend-mode: difference` | 3 | 1 | 1 | N (hide) |
| Themed object cursor | Swap the cursor element to a brand object (spatula, knife) per hover zone | 4 | 2 | 1 | N |
| Context-aware label | Cursor grows and shows "VIEW"/"DRAG"/"PLAY" from a `data-cursor` attribute | 4 | 1 | 1 | N |
| Cursor trail | Pooled elements with staggered lerp, or a WebGL trail texture | 3 | 2 | 2 | N |
| Spotlight reveal | Radial-gradient mask following the pointer over a hidden layer | 4 | 1 | 1 | N |
| 3D tilt cards | `rotateX/Y` from pointer offset, `perspective` on the parent, spring back | 4 | 1 | 1 | Y (gyro) |
| Mouse-parallax scene | Layers offset by normalised pointer position × depth factor | 3 | 1 | 1 | Y (gyro) |
| Repel / attract elements | Distance-based force per item, capped, `quickTo` applied | 4 | 2 | 2 | N |
| Eyes follow pointer | `Math.atan2` to pupil offset, clamped to the socket radius | 4 | 1 | 1 | Y (idle loop) |
| Gyroscope tilt | `DeviceOrientationEvent` — iOS needs `requestPermission()` from a user gesture | 4 | 2 | 1 | Y |

## W7 — BUTTONS & MICRO-INTERACTIONS
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| Magnetic button | Pointer offset × 0.3 via `quickTo`, elastic return on leave | 4 | 1 | 1 | N |
| Fill / wipe hover | Pseudo-element `scaleY` from the entry edge, origin set per pointer side | 3 | 1 | 1 | Y |
| Text roll label | Two stacked label copies, `y: -100%` together on hover | 3 | 1 | 1 | Y |
| Gooey / liquid button | SVG goo filter over blob children, or an SDF shader | 4 | 3 | 3 | Y |
| Click ripple | Circle scaled from the click point, fade out, pointer-events none | 3 | 1 | 1 | Y |
| Spring press | `scale: 0.96` on pointerdown, spring overshoot on release | 3 | 1 | 1 | Y |
| Press-and-hold + progress | `requestAnimationFrame` accumulator → conic-gradient ring; commit at 100% | 5 | 2 | 1 | Y |
| Physical slider | Draggable + InertiaPlugin (both free), snap points, haptic tick | 4 | 2 | 1 | Y |
| Morphing icons | MorphSVG (free) between two paths with matched node counts | 4 | 2 | 1 | Y |
| Loading → success morph | One timeline: spinner → checkmark DrawSVG, label crossfade | 4 | 2 | 1 | Y |
| Confetti / particle burst | `canvas-confetti` or a pooled DOM burst; brand-shaped particles | 3 | 1 | 2 | Y |
| Physics toggle | Matter.js or a spring; knob overshoots and settles | 3 | 2 | 1 | Y |
| Animated form fields | Floating label, inline validation on blur, shake + colour on error | 3 | 1 | 1 | Y |
| Like / heart burst | Scale pop + radial particles + haptic | 3 | 1 | 1 | Y |
| UI sounds | Howler sprite, ≤80ms clips, muted by default, one shared gain node | 4 | 2 | 1 | Y |
| Haptics | `navigator.vibrate([10])` — Android only, ignored on iOS Safari | 2 | 1 | 1 | Partial |

## W8 — MOTION ENGINEERING
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| GSAP core + timelines | One timeline per scene; labels for beats; `defaults` for shared ease | 5 | 1 | 1 | Y |
| CustomEase | Draw the curve in GSAP's ease visualiser, paste the SVG path | 4 | 1 | 1 | Y |
| Flip | Record → mutate DOM → `Flip.from({absolute, nested, spin})` | 5 | 2 | 1 | Y |
| Draggable + Inertia | Throwable carousels and knobs with real momentum and snap | 4 | 2 | 1 | Y |
| MorphSVG / DrawSVG / MotionPath | All free since April 2025; path-driven logos and routes | 4 | 2 | 1 | Y |
| Motion (Framer Motion) springs | `type:"spring", stiffness, damping, mass`; `layout` prop for FLIP | 4 | 1 | 1 | Y |
| react-spring | Physics-first React animation when you need interruptible springs | 3 | 2 | 1 | Y |
| Shared-element transition | View Transitions API `view-transition-name`, or Flip across routes | 5 | 3 | 1 | Y |
| Stagger system | `stagger: {each: 0.06, from: "start"}` — one value reused sitewide | 3 | 1 | 1 | Y |
| Matter.js 2D physics | Falling fries, wobbling stacks; sleep bodies, cap at ~150 | 4 | 3 | 3 | Y (cap 60) |
| Gestures | `@use-gesture/react` for drag/pinch/wheel unified with pointer events | 3 | 2 | 1 | Y |
| Rive state machines | Designer-authored interactive mascot; tiny `.riv`, GPU-cheap, inputs from JS | 5 | 3 | 1 | Y |
| Lottie / dotLottie | `@lottiefiles/dotlottie-web` — use only for illustration, never UI physics | 3 | 1 | 2 | Y |

## W9 — NAVIGATION, TRANSITIONS & LOADING
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| View Transitions API | `document.startViewTransition()`; cross-document via `@view-transition` | 5 | 2 | 1 | Y |
| Barba.js / Swup | Classic AJAX page transitions for non-framework sites | 4 | 2 | 1 | Y |
| Framework route transitions | Next.js App Router + View Transitions, or Nuxt page transitions | 4 | 2 | 1 | Y |
| Product-themed transition | Brand shapes (buns, patties) close over the viewport and reopen | 5 | 3 | 2 | Y |
| Split-screen cut | Page halves slide apart along a line; next page revealed through the gap | 5 | 3 | 2 | Y |
| Shape match-cut | Flip an object into the next page's UI element (round patty → round button) | 5 | 3 | 1 | Y |
| Story preloader | Brand animation tied to real `progress` events; hard cap ~1.5s | 4 | 2 | 1 | Y |
| Intro sequence | Plays once per session (`sessionStorage`), always skippable | 4 | 2 | 1 | Y |
| Full-screen menu | Clip-path circle from the button + staggered link reveal; focus trap | 4 | 2 | 1 | Y |
| Hide-on-scroll header | Direction from `ScrollTrigger.direction`, `y:-100%`, always shows at top | 3 | 1 | 1 | Y |
| Link hover preview | Image follows cursor, fades in on hover with scale from 1.1 | 4 | 2 | 1 | N |
| Section nav dots | IntersectionObserver → active state, `scrollIntoView({behavior:"smooth"})` | 2 | 1 | 1 | Y |
| ⌘K command palette | `cmdk` + Fuse.js fuzzy search over menu items and pages | 4 | 2 | 1 | Y (button) |
| Instant navigation | Speculation Rules API `prerender` on hover, or `next/link` prefetch | 4 | 1 | 1 | Y |

## W10 — LAYOUTS & GALLERIES
| Technique | How it's built | WOW | Eff | Perf | Mob |
|---|---|---|---|---|---|
| Bento grid | CSS grid areas + hover `grid-row/column` expansion with Flip | 4 | 2 | 1 | Y (stack) |
| Infinite drag canvas | Modulo-wrapped translate on a tile grid, Draggable + Inertia | 5 | 4 | 3 | Y |
| Drag / throw carousel | Draggable `type:"x"`, `inertia:true`, `snap` to item width | 4 | 2 | 1 | Y |
| Card → full screen | GSAP Flip with `absolute:true`, scroll lock, Esc to reverse | 5 | 2 | 1 | Y |
| Filterable grid | State change + `Flip.from()` on the surviving items, URL-synced filter | 4 | 2 | 1 | Y |
| Sticky split-screen | One column `position:sticky`, the other scrolls; swap content on enter | 4 | 2 | 1 | Y (stack) |
| Stacked cards | Sticky + per-index scale/`y`; scale down as the next covers it | 4 | 2 | 1 | Y |
| Hover list → image | List row hover swaps a fixed preview image with a mask reveal | 4 | 1 | 1 | N (tap) |
| Smooth accordion | `grid-template-rows: 0fr → 1fr` transition (no height hacks) | 2 | 1 | 1 | Y |
| Broken / asymmetric grid | 12-col grid with deliberate offsets and overlaps; never centre everything | 4 | 2 | 1 | Y |
| Real-world metaphor UI | Tickets on a rail, a printer, a griddle — physics + texture sell it | 5 | 4 | 2 | Y |
