CHATGPT MESSAGE 7 of 8 — THE EXAMPLE SITE. Continue applying the spec exactly. Don't build yet — wait until you have all 8 parts.

# 15. SMOOTHNESS SPEC
**Target: 60fps sustained, 120fps on ProMotion, zero jank across all 8 beats and every show-stopper, on a mid-range Android.**

| Rule | Requirement |
|---|---|
| One loop | Lenis driven by `gsap.ticker`; `gsap.ticker.lagSmoothing(0)`. No second `requestAnimationFrame` anywhere in the codebase. |
| Properties | `transform` and `opacity` only inside any scroll or pointer loop. Never `width/height/top/left/margin/box-shadow/filter`. |
| DPR | Canvas backing store and any WebGL renderer capped at `min(devicePixelRatio, 2)` desktop, `1.5` mobile. Drop to 1 if two consecutive frames exceed 20ms. |
| Frame decode | Every sequence frame is decoded with `createImageBitmap` **off the main thread** and is in memory **before** the playhead reaches it. A ±20-frame window around the playhead is always prefetched at high priority. |
| Preload | Heavy assets begin loading one viewport before their section. The signature sequence begins loading as soon as the hero is idle. |
| Off-screen | Every WebGL scene stops rendering when its canvas leaves the viewport or the tab blurs. Matter.js worlds stop stepping when off-screen. |
| Allocation | No object allocation inside any frame loop. Reuse vectors, arrays and bitmap references. |
| Layout | Geometry is read once in `ScrollTrigger.refresh` and cached. No `getBoundingClientRect()` inside a loop. |
| Listeners | `{ passive: true }` on every wheel and touch listener. |
| Bodies | Physics capped by GPU tier: desktop 150 total, mobile 60. Sleep enabled. Despawn off-screen. |
| Viewport units | `svh` / `dvh` only. Never `100vh`. |
| Long page | `content-visibility: auto` with `contain-intrinsic-size` on every section below the fold. |
| Fonts | Preloaded with `crossorigin`, `font-display: swap`, and a `size-adjust` fallback so the hero headline never shifts. |
| Reduced motion | A designed alternative, not "animations off" — the four-key-frame crossfade for the sequence, static states elsewhere. |

## Test plan
1. **Chrome Performance panel**, 6-second recording through the whole pinned sequence, 4× CPU throttle. Pass = no frame over 16.7ms, no long task over 50ms, no purple forced-reflow bars, no GC sawtooth.
2. **`renderer.info`** on every WebGL scene: under 150 draw calls on mobile, 300 desktop.
3. **Real iPhone**, including **Low Power Mode** — it throttles `requestAnimationFrame` and blocks video autoplay. The sequence must still scrub.
4. **Real mid-range Android** (roughly a $250 device, not a flagship). This is the acceptance gate: if it stutters there, the feature is simplified, not shipped.
5. **Field INP** via the `web-vitals` library reporting into GA4.
6. Scrub the sequence **backwards, fast, repeatedly**. Anything stuck, desynced or double-fired means a beat was written with state instead of as a function of progress.

# 16. PERFORMANCE BUDGET
| Metric | Budget |
|---|---|
| LCP | < 2.5s on a mid-range phone over 4G |
| INP | < 200ms |
| CLS | < 0.1 |
| Initial JS | ≤ 150KB gzip. Three.js, Rapier, Matter.js, Rive, MediaPipe, Mapbox and the camera code are **all** dynamically imported on entry or on tap. |
| Hero LCP image | Preloaded, `fetchpriority="high"`, never lazy, ≤ 200KB |
| Sequence frames | Loaded progressively — stride 8, then 4, then 2, then 1. Playback starts with one eighth of the frames present. Desktop total ≤ 24MB, mobile ≤ 7MB |
| Any single image | ≤ 200KB hero, ≤ 120KB content, ≤ 40KB thumbnail |
| Fonts | ≤ 3 families, ≤ 5 weights, subset to Latin |
| No-WebGL path | The entire site works with a static poster in place of every 3D scene |

---

# 17. WORKING CODE

Versions: `gsap@3.13.x` (core + ScrollTrigger + SplitText + Flip — all free), `lenis@1.3.26`, `three@^0.180.0`, `@rive-app/canvas@^2`, `matter-js@^0.20`.

## 17.0 — The single scroll loop (`src/lib/scroll.js`)
```js
import Lenis from 'lenis'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { SplitText } from 'gsap/SplitText'
import { Flip } from 'gsap/Flip'

gsap.registerPlugin(ScrollTrigger, SplitText, Flip)
gsap.defaults({ ease: 'power2.out', duration: 0.36 })

export const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
export const isMobile = window.matchMedia('(max-width: 767px)').matches
export const dprCap = isMobile ? 1.5 : 2

export const lenis = new Lenis({
  lerp: 0.1,
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smoothWheel: true,
  syncTouch: false,
})

lenis.on('scroll', ScrollTrigger.update)
gsap.ticker.add((time) => lenis.raf(time * 1000))
gsap.ticker.lagSmoothing(0)
ScrollTrigger.config({ ignoreMobileResize: true })

export { gsap, ScrollTrigger, SplitText, Flip }
```

## 17.1 — The hero (`src/sections/hero.js`)
```js
import { gsap, ScrollTrigger, SplitText, lenis, reduced, isMobile } from '../lib/scroll.js'

export function initHero(root) {
  const headline = root.querySelector('[data-hero-headline]')
  const status   = root.querySelector('[data-hero-status]')
  const orderBtn = root.querySelector('[data-order-btn]')
  const kongEl   = root.querySelector('[data-kong]')

  const split = new SplitText(headline, { type: 'chars,lines', mask: 'lines' })

  if (!reduced) {
    gsap.from(split.chars, {
      yPercent: 120, rotate: 6, opacity: 0,
      duration: 0.9, ease: 'back.out(1.4)', stagger: 0.04,
    })
    gsap.from(status, { opacity: 0, y: 12, duration: 0.5, delay: 0.3 })
  }

  // Velocity squash on the display type — clamped hard at 18%
  if (!reduced) {
    const setY = gsap.quickTo(headline, 'scaleY', { duration: 0.4, ease: 'elastic.out(1,0.5)' })
    const setX = gsap.quickTo(headline, 'scaleX', { duration: 0.4, ease: 'elastic.out(1,0.5)' })
    ScrollTrigger.create({
      trigger: root, start: 'top top', end: 'bottom top', scrub: true,
      onUpdate: (self) => {
        const v = gsap.utils.clamp(-0.18, 0.18, self.getVelocity() / -9000)
        const sy = 1 + v
        setY(sy); setX(1 / Math.sqrt(sy))
      },
      onLeave: () => { setY(1); setX(1) },
      onLeaveBack: () => { setY(1); setX(1) },
    })
  }

  // Magnetic order button — desktop pointer only
  if (window.matchMedia('(hover: hover)').matches && !reduced) {
    const mx = gsap.quickTo(orderBtn, 'x', { duration: 0.4, ease: 'power3.out' })
    const my = gsap.quickTo(orderBtn, 'y', { duration: 0.4, ease: 'power3.out' })
    const onMove = (e) => {
      const r = orderBtn.getBoundingClientRect()
      const dx = e.clientX - (r.left + r.width / 2)
      const dy = e.clientY - (r.top + r.height / 2)
      if (Math.hypot(dx, dy) < 120) { mx(dx * 0.3); my(dy * 0.3) } else { mx(0); my(0) }
    }
    window.addEventListener('pointermove', onMove, { passive: true })
  }

  // Order hand-off: navigate FIRST, animate second. Never the other way round.
  orderBtn.addEventListener('click', (e) => {
    e.preventDefault()
    window.dataLayer?.push({ event: 'order_click', location: 'boca_raton' })
    window.open(orderBtn.href, '_blank', 'noopener')
    if (!reduced) {
      gsap.timeline()
        .to(orderBtn, { scale: 0.94, duration: 0.08, ease: 'power2.in' })
        .to(orderBtn, { scale: 1, duration: 0.3, ease: 'back.out(2)' })
    }
  })

  // Kong: eyes follow the pointer, or the last touch, then idle-wander
  if (kongEl && !reduced) {
    import('@rive-app/canvas').then(({ Rive }) => {
      const r = new Rive({
        src: '/rive/kong.riv', canvas: kongEl, autoplay: true,
        stateMachines: 'KongSM', artboard: 'Kong',
      })
      r.on('load', () => {
        const inputs = r.stateMachineInputs('KongSM')
        const px = inputs.find(i => i.name === 'pointerX')
        const py = inputs.find(i => i.name === 'pointerY')
        const hv = inputs.find(i => i.name === 'hoverOrder')
        window.addEventListener('pointermove', (e) => {
          if (px) px.value = (e.clientX / window.innerWidth) * 100
          if (py) py.value = (e.clientY / window.innerHeight) * 100
        }, { passive: true })
        orderBtn.addEventListener('pointerenter', () => { if (hv) hv.value = true })
        orderBtn.addEventListener('pointerleave', () => { if (hv) hv.value = false })
      })
    })
  }
  return () => split.revert()
}
```

## 17.2 — The 8-beat scroll-scrubbed image-sequence player (`src/sections/sequence.js`)
Reads the asset contract exactly. Canvas playback, progressive loading, `createImageBitmap` ahead of the playhead, DPR-aware cover fit, resize handling, per-device frame sets, and DOM overlays on the same progress value.

```js
import { gsap, ScrollTrigger, Flip, reduced, isMobile, dprCap } from '../lib/scroll.js'

const CONTRACT = {
  desktop: { total: 248, dir: '/frames/desktop', w: 1920, h: 1080,
             labels: '/frames/labels.desktop.json',
             kong: { dir: '/frames/kong/desktop', start: 34, count: 19 } },
  mobile:  { total: 124, dir: '/frames/mobile', w: 1080, h: 1440,
             labels: '/frames/labels.mobile.json',
             kong: { dir: '/frames/kong/mobile', start: 17, count: 10 } },
}
// Beat boundaries as fractions of scroll progress
const BEATS = {
  toss:[0,.11], bullet:[.11,.21], closeup:[.21,.31], explode:[.31,.50],
  turn:[.50,.59], smash:[.59,.69], cut:[.69,.86], slice:[.86,1],
}
const LAYERS = ['bun_top','sauce_chef','onion_caramelized','bacon_beef',
  'cheese_upper','patty_upper','cheese_lower','patty_lower','bun_bottom']

const pad = (n) => String(n).padStart(4, '0')
const local = (p, [a, b]) => gsap.utils.clamp(0, 1, (p - a) / (b - a))

async function detectFormat(dir) {
  try {
    const res = await fetch(`${dir}/smash_0001.avif`)
    if (!res.ok) throw 0
    const bmp = await createImageBitmap(await res.blob())
    bmp.close?.()
    return 'avif'
  } catch { return 'webp' }
}

class FrameStore {
  constructor(dir, total, fmt) {
    this.dir = dir; this.total = total; this.fmt = fmt
    this.bitmaps = new Array(total)
    this.pending = new Set()
    this.loaded = 0
  }
  url(i) {
    const name = `smash_${pad(i + 1)}`
    return this.fmt === 'avif' ? `${this.dir}/${name}.avif` : `${this.dir}/webp/${name}.webp`
  }
  async fetchOne(i, priority = 'auto') {
    if (this.bitmaps[i] || this.pending.has(i)) return
    this.pending.add(i)
    try {
      const res = await fetch(this.url(i), { priority })
      if (!res.ok) throw new Error(res.status)
      this.bitmaps[i] = await createImageBitmap(await res.blob())
      this.loaded++
    } catch { /* a missing frame degrades to the nearest loaded one */ }
    finally { this.pending.delete(i) }
  }
  // stride 8 -> 4 -> 2 -> 1, four at a time so the network is never idle
  async loadProgressively(onProgress) {
    const order = []
    const seen = new Set()
    for (const step of [8, 4, 2, 1])
      for (let i = 0; i < this.total; i += step)
        if (!seen.has(i)) { seen.add(i); order.push(i) }
    for (let i = 0; i < order.length; i += 4) {
      await Promise.all(order.slice(i, i + 4).map((n) => this.fetchOne(n)))
      onProgress?.(this.loaded / this.total)
    }
  }
  prefetchAround(i, radius = 20) {
    for (let d = 0; d <= radius; d++) {
      const a = i + d, b = i - d
      if (a < this.total) this.fetchOne(a, 'high')
      if (b >= 0) this.fetchOne(b, 'high')
    }
  }
  nearest(i) {
    if (this.bitmaps[i]) return this.bitmaps[i]
    for (let d = 1; d < this.total; d++) {
      if (this.bitmaps[i - d]) return this.bitmaps[i - d]
      if (this.bitmaps[i + d]) return this.bitmaps[i + d]
    }
    return null
  }
}

export async function initSequence(root) {
  const cfg = isMobile ? CONTRACT.mobile : CONTRACT.desktop
  const canvas = root.querySelector('[data-seq-canvas]')
  const ctx = canvas.getContext('2d', { alpha: false })
  const poster = root.querySelector('[data-seq-poster]')
  const labelLayer = root.querySelector('[data-seq-labels]')
  const kongEl = root.querySelector('[data-seq-kong]')
  const headline = root.querySelector('[data-seq-headline]')
  const splitTop = root.querySelector('[data-split-top]')
  const splitBottom = root.querySelector('[data-split-bottom]')
  const cutFace = root.querySelector('[data-cut-face]')
  const orderBtn = document.querySelector('[data-order-btn]')

  if (reduced) { initReducedMotion(root); return }

  let W = 0, H = 0, dpr = 1
  const resize = () => {
    dpr = Math.min(window.devicePixelRatio || 1, dprCap)
    W = root.clientWidth; H = root.clientHeight
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr)
    canvas.style.width = W + 'px'; canvas.style.height = H + 'px'
    draw(lastP)
  }

  const fmt = await detectFormat(cfg.dir)
  const store = new FrameStore(cfg.dir, cfg.total, fmt)

  // Labels: positions baked by Blender, normalised 0-1, linearly interpolated
  let labelTrack = null
  fetch(cfg.labels).then(r => r.ok ? r.json() : null).then(j => { labelTrack = j }).catch(() => {})

  const labelEls = new Map()
  LAYERS.forEach((name) => {
    const el = document.createElement('span')
    el.className = 'seq-label'
    el.textContent = LABEL_COPY[name]
    el.style.opacity = '0'
    labelLayer.appendChild(el)
    labelEls.set(name, el)
  })

  let lastP = 0
  let lastIndex = -1

  function draw(p) {
    const idx = Math.round(p * (cfg.total - 1))
    const bmp = store.nearest(idx)
    if (!bmp) return
    const s = Math.max(canvas.width / bmp.width, canvas.height / bmp.height)
    const w = bmp.width * s, h = bmp.height * s
    ctx.drawImage(bmp, (canvas.width - w) / 2, (canvas.height - h) / 2, w, h)
    if (idx !== lastIndex) { store.prefetchAround(idx); lastIndex = idx }
  }

  function positionLabels(p) {
    const inExplode = p >= BEATS.explode[0] && p <= BEATS.turn[1]
    if (!inExplode || !labelTrack) {
      labelEls.forEach((el) => { el.style.opacity = '0' })
      return
    }
    const frame = Math.round(p * (cfg.total - 1)) + 1
    const track = labelTrack.frames[frame] || nearestTrack(labelTrack.frames, frame)
    if (!track) return
    const e = local(p, BEATS.explode)
    LAYERS.forEach((name, i) => {
      const el = labelEls.get(name)
      const xy = track[name]
      if (!xy) { el.style.opacity = '0'; return }
      const appear = gsap.utils.clamp(0, 1, (e - i * 0.08) / 0.25)
      el.style.opacity = String(appear)
      el.style.transform = `translate3d(${xy[0] * W}px, ${xy[1] * H}px, 0)`
    })
  }

  function nearestTrack(frames, frame) {
    for (let d = 1; d < 12; d++) {
      if (frames[frame - d]) return frames[frame - d]
      if (frames[frame + d]) return frames[frame + d]
    }
    return null
  }

  function updateOverlays(p) {
    // Beat 1-2: headline settles, then everything but one line dims
    headline.style.opacity = String(1 - gsap.utils.clamp(0, 1, (p - 0.09) / 0.04))

    // Beat 2: Kong's arm snatches a burger
    const k = local(p, BEATS.bullet)
    const grab = gsap.utils.clamp(0, 1, (k - 0.3) / 0.6)
    kongEl.style.opacity = String(grab > 0 && grab < 1 ? 1 : 0)
    kongEl.style.transform =
      `translate3d(${(1 - grab) * 40}vw, ${grab * -8}vh, 0) rotate(${-8 + grab * 14}deg)`

    // Beat 8: the page splits along the cut line, revealing the menu
    const s = local(p, BEATS.slice)
    splitTop.style.transform = `translate3d(0, ${-s * 55}vh, 0)`
    splitBottom.style.transform = `translate3d(0, ${s * 55}vh, 0)`
  }

  let matchCutDone = false
  function maybeMatchCut(p) {
    if (p > 0.97 && !matchCutDone) {
      matchCutDone = true
      const state = Flip.getState(cutFace)
      cutFace.classList.add('is-order-button')
      Flip.from(state, { duration: 0.7, ease: 'power3.inOut', absolute: true, scale: true })
    } else if (p < 0.95 && matchCutDone) {
      matchCutDone = false
      const state = Flip.getState(cutFace)
      cutFace.classList.remove('is-order-button')
      Flip.from(state, { duration: 0.4, ease: 'power3.inOut', absolute: true, scale: true })
    }
  }

  ScrollTrigger.create({
    trigger: root,
    start: 'top top',
    end: () => `+=${isMobile ? 420 : 620}%`,
    pin: root.querySelector('[data-seq-stage]'),
    anticipatePin: 1,
    pinSpacing: true,
    invalidateOnRefresh: true,
    scrub: 1,
    onRefresh: resize,
    onUpdate: (self) => {
      lastP = self.progress
      draw(lastP); positionLabels(lastP); updateOverlays(lastP); maybeMatchCut(lastP)
    },
  })

  window.addEventListener('resize', gsap.utils.throttle(resize, 200), { passive: true })
  resize()

  await store.fetchOne(0)
  poster.style.opacity = '0'
  draw(0)
  store.loadProgressively()
  // The Order button is clickable the whole time.
  orderBtn.style.pointerEvents = 'auto'
}

const LABEL_COPY = {
  bun_top: 'SESAME BRIOCHE', sauce_chef: 'CHEF SAUCE',
  onion_caramelized: 'CARAMELIZED ONION', bacon_beef: 'BEEF BACON',
  cheese_upper: 'PLANT-BASED CHEESE', patty_upper: 'SMASHED PATTY',
  cheese_lower: 'PLANT-BASED CHEESE', patty_lower: 'SMASHED PATTY',
  bun_bottom: 'TOASTED BASE',
}

function initReducedMotion(root) {
  const keys = ['/frames/key/key_040.avif', '/frames/key/key_118.avif',
                '/frames/key/key_160.avif', '/frames/key/key_205.avif']
  const stage = root.querySelector('[data-seq-stage]')
  const imgs = keys.map((src, i) => {
    const img = new Image()
    img.src = src; img.alt = ''
    img.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .4s linear'
    img.style.opacity = i === 0 ? '1' : '0'
    stage.appendChild(img)
    return img
  })
  ScrollTrigger.create({
    trigger: root, start: 'top top', end: '+=300%', pin: stage,
    onUpdate: (self) => {
      const active = Math.min(3, Math.floor(self.progress * 4))
      imgs.forEach((img, i) => { img.style.opacity = i === active ? '1' : '0' })
    },
  })
}
```
