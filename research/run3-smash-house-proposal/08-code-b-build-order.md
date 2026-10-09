CHATGPT MESSAGE 8 of 8 — THE EXAMPLE SITE. This is the last part. You now have all 8. Build in the order given in section 18 below, and after each step state what you built and what's next.

## 17.3 — The real-time procedural fallback (`src/sections/sequence-fallback.js`)
Plays the same 8 beats with primitives and clipping-plane caps. **Every value is a pure function of `p`** — no accumulation, no `once`, no state — so scrubbing backwards is exact. Ship this until the Blender frames exist; swapping is a one-flag change.

```js
import * as THREE from 'three'
import { gsap, ScrollTrigger, debounce, isMobile, dprCap } from '../lib/scroll.js'

const BEATS = {
  toss:[0,.11], bullet:[.11,.21], closeup:[.21,.31], explode:[.31,.50],
  turn:[.50,.59], smash:[.59,.69], cut:[.69,.86], slice:[.86,1],
}
const local = (p,[a,b]) => THREE.MathUtils.clamp((p - a) / (b - a), 0, 1)
const easeBack = gsap.parseEase('back.out(1.6)')
const easeExpoIn = gsap.parseEase('expo.in')
// deterministic pseudo-noise: the shake is identical when scrubbed backwards
const noise = (x) => { const s = Math.sin(x * 127.1) * 43758.5453; return (s - Math.floor(s)) - 0.5 }

// bottom to top, matching the asset contract
const LAYERS = [
  { name:'bun_bottom',        r:1.00, h:0.22, color:0xC98A4B },
  { name:'patty_lower',       r:1.05, h:0.16, color:0x5A3220 },
  { name:'cheese_lower',      r:1.02, h:0.05, color:0xE8B44A },
  { name:'patty_upper',       r:1.05, h:0.16, color:0x5A3220 },
  { name:'cheese_upper',      r:1.02, h:0.05, color:0xE8B44A },
  { name:'bacon_beef',        r:0.95, h:0.07, color:0x8C2A1E },
  { name:'onion_caramelized', r:0.92, h:0.08, color:0xA9701F },
  { name:'sauce_chef',        r:0.94, h:0.04, color:0xD9782B },
  { name:'bun_top',           r:1.00, h:0.42, color:0xD59A57 },
]
const STACK_H = LAYERS.reduce((s, L) => s + L.h, 0)
const CENTER_I = (LAYERS.length - 1) / 2
const INTERIOR = 0xB4644A

function buildStack(clipPlane) {
  const g = new THREE.Group()
  let y = 0
  const meshes = LAYERS.map((L) => {
    const mat = new THREE.MeshStandardMaterial({ color: L.color, roughness: 0.55 })
    if (clipPlane) { mat.clippingPlanes = [clipPlane]; mat.clipShadows = true }
    const m = new THREE.Mesh(new THREE.CylinderGeometry(L.r, L.r * 0.97, L.h, 48), mat)
    m.name = L.name
    m.position.y = y + L.h / 2
    m.userData.restY = m.position.y
    y += L.h
    g.add(m)
    return m
  })
  return { group: g, meshes }
}

// The cut face: one unclipped plane per layer, sitting a hair off the cut so it never z-fights.
function buildCaps(sign) {
  const g = new THREE.Group()
  const mat = new THREE.MeshStandardMaterial({ color: INTERIOR, roughness: 0.45, side: THREE.DoubleSide })
  let y = 0
  LAYERS.forEach((L) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(L.r * 2, L.h), mat)
    m.rotation.y = sign * Math.PI / 2      // the plane's +Z normal turns to face ±X
    m.position.set(sign * 0.001, y + L.h / 2, 0)
    y += L.h
    g.add(m)
  })
  return g
}

export function initSequenceFallback(root) {
  const stage = root.querySelector('[data-seq-stage]')
  const canvas = root.querySelector('[data-seq-canvas]')
  const scene = new THREE.Scene()
  scene.background = new THREE.Color(0x13110C)

  const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100)
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: 'high-performance' })
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, dprCap))
  renderer.localClippingEnabled = true
  renderer.toneMapping = THREE.ACESFilmicToneMapping

  scene.add(new THREE.AmbientLight(0xffffff, 0.35))
  const key  = new THREE.DirectionalLight(0xfff0dd, 3.2); key.position.set(-3, 4, -3);  scene.add(key)
  const rim  = new THREE.DirectionalLight(0xFEEB13, 1.1); rim.position.set(2, 3, -4);   scene.add(rim)
  const fill = new THREE.DirectionalLight(0xE51144, 0.5); fill.position.set(3, .5, 3);  scene.add(fill)

  // --- five tossed burgers; index 2 is the hero ---
  const burgers = []
  for (let i = 0; i < 5; i++) {
    const { group, meshes } = buildStack(null)
    group.userData = {
      meshes,
      v0: 4.2 + i * 0.4,
      phase: i * 0.06,
      driftX: (i - 2) * 0.55,
      driftZ: (i % 2 ? 1 : -1) * 0.3,
      spinAxis: new THREE.Vector3(noise(i + 1), 1, noise(i + 7)).normalize(),
      w0: 5.5 + i * 0.8,
      startPos: new THREE.Vector3(0, -4, 0),
    }
    scene.add(group)
    burgers.push(group)
  }
  const hero = burgers[2]

  // --- the two halves, each clipped to its own side of x = 0 ---
  // THREE keeps fragments where normal·p + constant >= 0.
  const planeR = new THREE.Plane(new THREE.Vector3( 1, 0, 0), 0)  // keeps x >= -constant
  const planeL = new THREE.Plane(new THREE.Vector3(-1, 0, 0), 0)  // keeps x <=  constant
  const right = buildStack(planeR); right.group.name = 'burger_half_right'
  const left  = buildStack(planeL); left.group.name  = 'burger_half_left'
  const capsR = buildCaps(-1); capsR.name = 'cut_face_right'   // faces back toward the gap
  const capsL = buildCaps( 1); capsL.name = 'cut_face_left'
  right.group.add(capsR); left.group.add(capsL)
  right.group.visible = left.group.visible = false
  scene.add(right.group, left.group)

  // --- knife ---
  const knife = new THREE.Group()
  const blade = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.9, 2.6),
    new THREE.MeshStandardMaterial({ color: 0xcfd6dd, roughness: 0.18, metalness: 0.95 }))
  blade.name = 'knife_blade'
  const handle = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.22, 0.9),
    new THREE.MeshStandardMaterial({ color: 0x241a14, roughness: 0.7 }))
  handle.name = 'knife_handle'; handle.position.z = -1.7
  knife.add(blade, handle); knife.visible = false
  scene.add(knife)

  const target = new THREE.Vector3(0, STACK_H / 2, 0)
  const heroRest = new THREE.Vector3(0, 0, 0)
  const faceCam = new THREE.Quaternion()
  const tmpPos = new THREE.Vector3()

  function update(p) {
    // ---------- camera first: every object that needs to face the lens reads it ----------
    const tToss = local(p, BEATS.toss)
    const orbit = local(p, BEATS.bullet) * Math.PI * 0.5
    const push  = local(p, BEATS.closeup)
    const pull  = local(p, BEATS.explode)
    const smashT = local(p, BEATS.smash)
    const impact = easeExpoIn(THREE.MathUtils.clamp((smashT - 0.3) / 0.2, 0, 1))
    const recoil = THREE.MathUtils.clamp((smashT - 0.5) / 0.5, 0, 1)
    const shake  = impact * (1 - recoil)

    const radius = 7.5 - push * 2.6 + pull * 1.1
    const height = 0.6 + tToss * 1.4 + pull * 0.7
    camera.position.set(
      Math.sin(orbit) * radius + noise(p * 900) * 0.12 * shake,
      height + noise(p * 770) * 0.10 * shake,
      Math.cos(orbit) * radius)
    camera.lookAt(target)
    camera.rotation.z = noise(p * 610) * 0.024 * shake
    camera.getWorldQuaternion(faceCam)

    // ---------- beat 1: ballistic toss (frozen automatically once tToss hits 1) ----------
    const settle = local(p, BEATS.closeup)
    burgers.forEach((g, i) => {
      const d = g.userData
      const tt = Math.max(0, (tToss - d.phase) / (1 - d.phase)) * 1.25
      tmpPos.set(d.driftX * tt, -4 + d.v0 * tt - 0.5 * 9.8 * tt * tt * 0.35, d.driftZ * tt)
      if (i === 2) {
        // beat 3: the hero settles to centre — lerp between two CONSTANTS, never from itself
        g.position.lerpVectors(tmpPos, heroRest, settle)
      } else {
        g.position.copy(tmpPos)
        g.position.y -= settle * 8              // the others fall away
        g.visible = settle < 0.95
      }
      // spin decays naturally, then slerps onto the camera-facing quaternion
      const angle = (d.w0 / 2.4) * (1 - Math.exp(-2.4 * (tToss + settle)))
      g.quaternion.setFromAxisAngle(d.spinAxis, angle)
      if (i === 2 && settle > 0.85) g.quaternion.slerp(faceCam, (settle - 0.85) / 0.15)
    })

    // ---------- beats 4 + 6: explode, anticipate, slam ----------
    const eRaw  = local(p, BEATS.explode)
    const antic = THREE.MathUtils.clamp(smashT / 0.3, 0, 1)
    hero.userData.meshes.forEach((m, i) => {
      const stagger = THREE.MathUtils.clamp((eRaw - i * 0.05) / (1 - i * 0.05), 0, 1)
      const spread = easeBack(stagger) * (1 + antic * 0.08) * (1 - impact)
      m.position.y = m.userData.restY + (i - CENTER_I) * 0.85 * spread
      m.rotation.x = ((i % 2) ? 0.06 : -0.06) * spread
      m.rotation.z = ((i % 3) ? -0.04 : 0.04) * spread
    })

    // ---------- beat 5: half turn ----------
    hero.rotation.y = local(p, BEATS.turn) * Math.PI

    // ---------- beat 6: volume-preserving impact squash ----------
    const sy = 1 - 0.18 * shake
    hero.scale.set(1 / Math.sqrt(sy), sy, 1 / Math.sqrt(sy))

    // ---------- beat 7: the cut ----------
    const t7 = local(p, BEATS.cut)
    knife.visible = t7 > 0 && t7 < 0.95
    knife.position.set(0, 3.4 - t7 * 4.2, 0)
    knife.rotation.z = 0.25 - t7 * 0.25

    const cutting = THREE.MathUtils.clamp((t7 - 0.15) / 0.35, 0, 1)
    const open    = THREE.MathUtils.clamp((t7 - 0.55) / 0.45, 0, 1)
    // swap whole burger -> two halves at the instant the blade covers the seam
    const split = cutting > 0.5
    hero.visible = !split
    right.group.visible = left.group.visible = split
    if (!split) {
      const under = THREE.MathUtils.clamp(1 - Math.abs(cutting - 0.5) * 4, 0, 1)
      hero.userData.meshes.forEach((m) => { m.scale.y = 1 - 0.06 * under })  // squash under the blade
    } else {
      const gap = open * 0.22
      right.group.position.x =  gap; right.group.rotation.y =  open * 0.18
      left.group.position.x  = -gap; left.group.rotation.y  = -open * 0.18
      // the clip plane travels with its half, or it would re-cut it as the halves part
      planeR.constant = -gap
      planeL.constant = -gap
    }
  }

  const resize = () => {
    const w = stage.clientWidth, h = stage.clientHeight
    renderer.setSize(w, h, false)
    camera.aspect = w / h
    camera.updateProjectionMatrix()
  }

  let visible = false
  new IntersectionObserver(([e]) => { visible = e.isIntersecting }, { rootMargin: '20%' }).observe(stage)

  let lastP = 0
  ScrollTrigger.create({
    trigger: root, start: 'top top',
    end: () => `+=${isMobile ? 420 : 620}%`,
    pin: stage, anticipatePin: 1, pinSpacing: true, invalidateOnRefresh: true, scrub: 1,
    onRefresh: resize,
    onUpdate: (self) => { lastP = self.progress },
  })

  gsap.ticker.add(() => {
    if (!visible || document.hidden) return
    update(lastP)
    renderer.render(scene, camera)
  })

  window.addEventListener('resize', debounce(resize, 200), { passive: true })
  resize()
}
```

**Two notes on the fallback.** The half-swap at `cutting > 0.5` happens on the frame the blade sits directly over the seam, so the transition is hidden — if you retime the knife, retime the swap with it. And the caps are deliberately unclipped and offset by 1mm; clipping them would remove the very face you are trying to show.

## 17.4 — glTF loader for the interactive moments (`src/lib/loadHero.js`)
Looks meshes up by the **exact contract names**. Fails loudly if a name is missing — a silently absent layer is how a configurator ships broken.

```js
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js'
import { KTX2Loader } from 'three/examples/jsm/loaders/KTX2Loader.js'
import { MeshoptDecoder } from 'three/examples/jsm/libs/meshopt_decoder.module.js'

export const HERO_LAYERS = ['bun_bottom','patty_lower','cheese_lower','patty_upper',
  'cheese_upper','bacon_beef','onion_caramelized','sauce_chef','bun_top']
export const HALF_MESHES = ['burger_half_left','burger_half_right','cut_face_left',
  'cut_face_right','knife_blade','knife_handle']

export async function loadHero(renderer, url = '/models/hero.glb', names = HERO_LAYERS) {
  const draco = new DRACOLoader().setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.7/')
  const ktx2 = new KTX2Loader().setTranscoderPath('/basis/').detectSupport(renderer)
  const loader = new GLTFLoader()
    .setDRACOLoader(draco)
    .setKTX2Loader(ktx2)
    .setMeshoptDecoder(MeshoptDecoder)

  const gltf = await loader.loadAsync(url)
  const root = gltf.scene
  const byName = new Map()
  root.traverse((o) => { if (o.isMesh) byName.set(o.name, o) })

  const missing = names.filter((n) => !byName.has(n))
  if (missing.length) {
    throw new Error(`glTF is missing contract meshes: ${missing.join(', ')}. ` +
      `Re-export from Blender without renaming objects.`)
  }
  // Origins are authored at each layer's own centre; the stack axis is +Y here,
  // because the exporter converts Blender's +Z up to glTF's +Y up.
  names.forEach((n) => { byName.get(n).userData.restY = byName.get(n).position.y })
  draco.dispose(); ktx2.dispose()
  return { root, layers: names.map((n) => byName.get(n)), byName }
}
```

---

# 18. BUILD ORDER

**Phase 1 — foundations (nothing visual ships before this is done).**
1. Next.js App Router project, TypeScript, the design tokens from section 14 as CSS custom properties, fonts preloaded with the `size-adjust` fallback.
2. Sanity schemas: `location`, `menuCategory`, `menuItem`, `modifier`, `promo`, `faq`. Seed with the real menu, marking every `[TO CONFIRM]` field.
3. The server-side open/closed engine: Hebcal fetch by Boca Raton coordinates, 6-hour cache, returning `isOpen / opensAt / closesAt / isShabbat / isHoliday / holidayName`. Render the status sentence into the HTML. **Unit-test it against a Friday, a Saturday afternoon, a Saturday night and a Yom Tov.**
4. Page shells and routes, semantic HTML, heading hierarchy, skip link, focus styles, `noindex` + robots disallow, the concept footer tag.
5. Image pipeline (AVIF/WebP, `srcset`, `sizes`, `aspect-ratio`, ThumbHash), schema markup, OG image endpoint, sitemap.
6. Forms: catering + newsletter with Turnstile, honeypot, time-trap, Resend, real success and error states.
7. Analytics events, cookie consent that gates the scripts, Sentry.
8. **Ship a fully working, accessible, fast site with zero animation.** Run Lighthouse and axe here. If it is not excellent at this point, no effect will save it.

**Phase 2 — the motion system.**
9. `src/lib/scroll.js` (section 17.0) — Lenis on the GSAP ticker, one loop.
10. The micro-interaction layer from section 11 applied to every interactive element.
11. Page transitions (bun wipe), the preloader, the spatula cursor, the sound toggle (off by default).

**Phase 3 — the signature sequence.**
12. The real-time fallback (17.3) wired into the pinned section. Verify all 8 beats scrub cleanly forwards **and backwards**.
13. The frame player (17.2) behind a flag, with the reduced-motion branch.
14. Profile on a real mid-range Android. Fix before continuing.

**Phase 4 — the brand moments** (section 9), in this order: smash press → squashed type → Kong alive → Motzei Shabbat countdown → ticket rail → bun transition → menu mini-explode → kosher stamp → sauce trail → heat haze → fries rain → blooming onion → build your smash → AR → location flyover → order hand-off → Kong catch.

**Phase 5 — the show-stoppers** (section 8), in this order: neon sign → Shabbat Mode → holiday modes → THE PASS → hunger-meter → party planner → gift card → Kong climbs out → locations globe → griddle footer → craving search → jukebox → reviews → Instagram wall → selfie → 404 → type "KONG".

**Phase 6 — the swap and the QA.**
15. When the rendered frames and the glTF arrive named exactly per the asset contract, flip the flag from the fallback to the frames. Nothing else changes.
16. Run the full QA checklist: foundations, wow, smoothness, realism. Profile again on real devices.
17. Produce the rights ledger and the list of every remaining `[TO CONFIRM]`.

**Standing rules for the whole build:** never invent a price, a review, an award, a promotion or a quote. Keep every `[TO CONFIRM]` visible in the build until it is resolved. The Order button is never covered, never disabled, and never waits for an animation.
