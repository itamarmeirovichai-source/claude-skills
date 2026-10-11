CHATGPT MESSAGE 5 of 7 — RESEARCH RESULTS. These are the results of deep research into how award-level interactive websites (Awwwards / FWA level) are built. Study them carefully — this is your knowledge base from now on. Don't build anything yet. Reply only: "Got it — send the next part."

# E. 3D PRODUCT SEQUENCE DEEP DIVE
Target sequence: **toss → bullet time → close-up → exploded view → cross-section cut**, entirely driven by scroll, perfectly reversible.

## E.1 The four build approaches, compared
| | (a) Real-time glTF | (b) Cycles image sequence | (c) Layered PNGs + CSS 3D | (d) Gaussian splats |
|---|---|---|---|---|
| Realism | Medium — no true SSS, no volumetric steam, fake caustics | **Photoreal** — path-traced SSS, volumetrics, real DOF | Low–Medium | High but "captured", can't be relit or re-lit |
| Smoothness | High if budgeted | **Highest** — drawing a decoded bitmap is ~1ms | High | Medium — huge buffers |
| File size | 2–8MB | 8–30MB (AVIF, 2 device sets) | 1–4MB | 15–80MB |
| Build time | Medium | High (modelling + render farm hours) | Low | Medium (capture + cleanup) |
| Mobile | Good | Good (half-res, half the frames) | Good | Poor |
| Interactivity | **Full** — any state, any angle | None — time only | Limited | Orbit only |
| Best for | Configurators, AR, "build your own" | The hero cinematic | Simple parallax explodes | Scanned environments |

**Decision rule:** if the user only controls *time*, render it (b). If the user controls *state*, run it live (a) — and bake that glTF out of the same Blender scene so the two look identical. (c) is the low-budget fallback, (d) is a specialty.

## E.2 The animation math
**Ballistic arc (the toss).** Each object gets its own `v0`, launch phase and horizontal drift:
```js
// t is 0..1 local to the toss beat
const g = 9.8, v0 = 4.2 + i * 0.35, phase = i * 0.06
const tt = Math.max(0, (t - phase) / (1 - phase)) * 1.25
obj.position.y = startY + v0 * tt - 0.5 * g * tt * tt
obj.position.x = startX + driftX * tt
obj.position.z = startZ + driftZ * tt
```
Give each object a different `v0` and `phase` so they never read as a rigid formation. Peak height for object `i` is at `tt = v0/g`.

**Spin with natural decay, landing face-on.**
```js
const w0 = 6.5                       // rad/s initial
const k  = 2.4                       // decay constant
const angle = (w0 / k) * (1 - Math.exp(-k * t))   // integral of w0*e^(-kt)
obj.quaternion.setFromAxisAngle(spinAxis, angle)
// final 15% of the beat: blend to the camera-facing target
if (t > 0.85) obj.quaternion.slerp(faceCameraQuat, (t - 0.85) / 0.15)
```
The `slerp` blend is what makes it feel choreographed rather than random — it lands, it doesn't stop.

**Speed ramp (bullet time).** Don't slow the clock — remap scroll progress so the peak occupies more scroll:
```js
// CustomEase drawn so the middle 20% of output spans 45% of input
const ramp = CustomEase.create('ramp', 'M0,0 C0.15,0 0.25,0.42 0.5,0.5 0.75,0.58 0.85,1 1,1')
const objectTime = ramp(progress)   // objects use this
const cameraAngle = progress * Math.PI * 0.5   // camera keeps moving linearly → the freeze-and-orbit look
```
Bullet time = **object time nearly stops while camera time keeps running.** That contrast is the whole effect.

**Exploded layers with stagger and overshoot.**
```js
layers.forEach((layer, i) => {
  const delay = i * 0.05
  const local = gsap.utils.clamp(0, 1, (p - delay) / (1 - delay))
  const eased = gsap.parseEase('back.out(1.6)')(local)
  layer.position.z = restZ[i] + gapPerLayer * (i - centerIndex) * eased
  layer.rotation.x = tiltPerLayer[i] * eased        // small, ±0.06 rad, different per layer
})
```
Rules: the gap must be large enough that the eye reads *separate objects* (≥0.6× layer thickness). Stagger from the centre outward, or top-down — never all at once. Overshoot 8–12% then settle. Every layer keeps its own origin at its own centre so it rotates in place.

**Blade + clipping plane (the cut).**
```js
const plane = new THREE.Plane(new THREE.Vector3(1, 0, 0), 0)
renderer.localClippingEnabled = true
material.clippingPlanes = [plane]
plane.constant = THREE.MathUtils.lerp(startX, endX, bladeProgress)
```
A clipped mesh is hollow — you must draw a **stencil cap**: render backfaces into the stencil buffer, then draw a full-screen-ish quad clipped to the plane with the interior material, then clear. In Blender for the hero frames you skip all of this: pre-model the halves with real interior faces and animate them apart.

**Halves opening.** Rotate each half about a hinge sitting *on the cut plane*, not about the object centre, or the halves interpenetrate:
```js
halfL.position.x = -gap * p; halfL.rotation.y = -0.18 * p
halfR.position.x =  gap * p; halfR.rotation.y =  0.18 * p
```
Keep `gap` small (2–4cm scale). "Pressed close, turned toward camera" reads as appetising; wide apart reads as a diagram.

## E.3 Camera choreography for the eight-beat take
| Beat | Camera | Why |
|---|---|---|
| Toss | Low, wide (35mm), tilting up, slight handheld noise | Puts the viewer on the griddle |
| Bullet time | Orbit ~90° on a fixed radius, subject locked centre-frame | The freeze is only legible if the camera moves |
| Close-up | Push-in on the forward axis (never FOV), rack focus from the falling burgers to the hero | Declares the hero |
| Explode | Pull back 15% and rise 10° so the gaps are legible; stop all rotation | Information beat — camera must calm down |
| Half turn | Slow orbit 180°, labels billboard to camera | Shows the back without losing the read |
| Smash | Anticipation pull-back 8%, then a 3-frame shove in + decaying shake | Impact is sold by the camera, not the object |
| Cut | Macro (85–100mm), focus on the blade edge, then rack to the cut face | The money shot |
| Slice-through | Camera holds; the *page* moves | Hands the energy to the UI |

Pitfalls: never cut inside a pinned hero sequence (it breaks the "one take" illusion); never orbit and push at the same time (nauseating); keep the horizon stable during the explode; keep the subject at or just above centre — food below centre reads as a leftover.

## E.4 Reversibility
Every property must be a **pure function of progress**. No `once: true`, no "if progress > x then play", no accumulated velocity, no particle systems whose state depends on history (bake those, or make them deterministic from a seed + progress). Test by scrubbing the scrollbar up and down fast — if anything is stuck, desynced or double-triggered, the beat is written wrong.

## E.5 Image-sequence playback that never janks
```js
// 1. Build the frame list per device
const total = 240, dir = isMobile ? '/frames/mobile' : '/frames/desktop'
const url = i => `${dir}/smash_${String(i + 1).padStart(4, '0')}.avif`

// 2. Progressive load: every 8th frame first, then fill the gaps
const bitmaps = new Array(total)
async function load(i) {
  if (bitmaps[i]) return
  const res = await fetch(url(i)); const blob = await res.blob()
  bitmaps[i] = await createImageBitmap(blob)        // decoded off the main thread
}
const order = []
for (let step = 8; step >= 1; step >>= 1)
  for (let i = 0; i < total; i += step) if (!order.includes(i)) order.push(i)

// 3. Draw: nearest already-loaded frame, never block
function draw(p) {
  let i = Math.round(p * (total - 1))
  while (i > 0 && !bitmaps[i]) i--                  // graceful during progressive load
  const bmp = bitmaps[i]; if (!bmp) return
  // DPR-aware cover-fit
  const s = Math.max(canvas.width / bmp.width, canvas.height / bmp.height)
  const w = bmp.width * s, h = bmp.height * s
  ctx.drawImage(bmp, (canvas.width - w) / 2, (canvas.height - h) / 2, w, h)
}
```
Plus: prefetch a window of ±20 frames around the playhead with higher priority; cap the canvas backing store at `min(devicePixelRatio, 2)`; resize with a debounced handler that re-reads `clientWidth/Height` once; and hold a `poster` frame in the DOM until frame 0 is decoded.

**Sizing budget:** desktop 1920×1080 AVIF q45 ≈ 60–110KB/frame → 240 frames ≈ 18–26MB. Mobile 960×1080 (portrait crop) at 120 frames ≈ 5–8MB. That is acceptable *only* because it streams progressively and starts playing at frame 0 with 1/8 of the frames present. If it can't, cut the frame count, not the resolution.

## E.6 Food detail effects, done smoothly
| Effect | Hero (rendered) | Interactive (real-time) |
|---|---|---|
| Sauce drip | Blender fluid sim or an animated metaball chain along the bun edge; render with high roughness variation and a clearcoat | A 2D metaball SDF shader on a plane hugging the bun silhouette; drip position = `progress` |
| Cheese pull | Cloth sim with high stretch, or a lofted mesh between two points with a noise-driven taper | A stretched plane with vertical UV scroll + noise thinning; alpha-tested edges |
| Steam | Cycles volumetric domain, low density, strong forward scattering, lit from behind | 4–8 soft sprite planes, additive, rising with per-sprite noise, opacity fading with height; **never** a real-time volumetric |
| Heat haze | Rendered directly into the frames | Screen-space UV distortion sampled from scrolling noise, masked to the griddle region, amplitude from scroll velocity |
| Sesame / crumbs | Geometry Nodes scatter on the bun surface; a handful as rigid bodies for the shake | `InstancedMesh` + Rapier, ≤300 desktop / ≤80 mobile, `sleep` enabled, despawned after 4s |

**The smoothness trap:** particles and physics are what kill mid-range Androids. Cap counts by GPU tier, sleep bodies aggressively, and pre-bake anything that doesn't need to react to the user.

---

# F. ANIMATION & CAMERA CHEAT SHEET
Each principle and camera move → a code pattern with defaults.

## The 12 principles
| Principle | Pattern |
|---|---|
| Squash & stretch | `gsap.to(el, {scaleY: 0.82, scaleX: 1.12, duration: 0.08, yoyo: true, repeat: 1, ease: 'power2.out'})` — volume-preserving: `sx = 1/Math.sqrt(sy)` |
| Anticipation | `tl.to(el, {y: 12, duration: 0.12, ease: 'power2.in'}).to(el, {y: -180, duration: 0.5, ease: 'power3.out'})` |
| Staging | Animate the focal element; on everything else set `opacity: 0.35` and, in 3D, raise `bokehScale`. One focus per beat. |
| Follow-through / overlap | `gsap.to(children, {y: 0, stagger: {each: 0.06, from: 'start'}, ease: 'back.out(1.4)'})` — trailing parts arrive 40–80ms late |
| Slow in / slow out | `gsap.defaults({ease: 'power2.out'})`; moves `power2.inOut`; exits `power2.in` |
| Arcs | `motionPath: {path: [{x:0,y:0},{x:120,y:-90},{x:240,y:0}], curviness: 1.25, autoRotate: true}` |
| Secondary action | A second, shorter tween on a child, offset by 80ms and 40% amplitude, on a different property |
| Timing | micro 150–250ms · standard 300–450ms · cinematic 600–1200ms · beat length in a scroll take 8–18% of section progress |
| Exaggeration | Overshoot 15–25% at the peak: `back.out(1.7)`, or key a 1.18 scale before settling to 1.0 |
| Solid drawing | One light direction and one lens across DOM, WebGL and rendered frames; shadows always fall the same way |
| Appeal | A 2–4s idle loop on every character; nothing on screen is ever perfectly still |
| Pose-to-pose | `tl.addLabel('toss', 0).addLabel('bullet', 0.12).addLabel('cut', 0.70)` — beats are labels, not magic numbers |

## Camera moves (Three.js / R3F defaults)
```js
// Push-in (NOT a zoom): move along the camera's forward axis
const fwd = new THREE.Vector3(); camera.getWorldDirection(fwd)
camera.position.copy(startPos).addScaledVector(fwd, 0.9 * p)

// Orbit / bullet time
const a = startAngle + Math.PI * 0.5 * p, r = 3.4
camera.position.set(Math.cos(a) * r, 1.1, Math.sin(a) * r); camera.lookAt(target)

// Rack focus (postprocessing DepthOfField)
gsap.to(dof, { focusDistance: 0.032, duration: 0.6, ease: 'power2.inOut' })   // 0.02–0.06 typical
// Blender equivalent: keyframe camera.data.dof.focus_distance, f-stop 2.0–2.8, 85–100mm

// Dolly zoom (subject size constant)
const h = 2 * dist * Math.tan(THREE.MathUtils.degToRad(fov) / 2)   // keep h constant
camera.fov = 2 * THREE.MathUtils.radToDeg(Math.atan(h / (2 * newDist))); camera.updateProjectionMatrix()

// Impact shake, decaying
let shake = 1.0
function tick(dt) {
  shake *= Math.pow(0.02, dt)               // ~300ms to nothing
  camera.position.x += (noise(t * 40) - 0.5) * 0.06 * shake
  camera.rotation.z += (noise(t * 37) - 0.5) * 0.015 * shake
}

// Whip pan: fast yaw + directional blur, 120-180ms, hides a transition
gsap.to(camera.rotation, { y: '+=0.9', duration: 0.16, ease: 'power3.inOut' })

// Speed ramp: remap progress, don't touch the clock
const ramp = CustomEase.create('ramp', 'M0,0 C0.15,0 0.25,0.42 0.5,0.5 0.75,0.58 0.85,1 1,1')

// Match cut: DOM ↔ DOM
const state = Flip.getState('.cut-face')
document.body.classList.add('is-ordering')            // .cut-face becomes the Order button
Flip.from(state, { duration: 0.7, ease: 'power3.inOut', absolute: true, scale: true })
```

## Motion tokens (one language for a whole site)
```
--ease-out: power2.out          --ease-in-out: power2.inOut
--ease-spring: back.out(1.6)    --ease-impact: expo.in
--dur-micro: 0.18s   --dur-base: 0.36s   --dur-slow: 0.72s   --dur-cine: 1.2s
--stagger: 0.06      --overshoot: 1.6    --shake-decay: 0.3s
```
Write these into the design tokens file and never hand-tune a one-off value again — consistency of ease and duration is most of what people read as "expensive".
