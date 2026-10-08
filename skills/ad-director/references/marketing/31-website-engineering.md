# 31 · Website engineering: the studio's video-first marketing site

Research brief, 2026-10-08. It covers how to build the studio site: a centre-screen character in transparent video, a 3D ring of 6–10 looping ads, a pick-and-play flow with sound, ElevenLabs speech with captions, a "continue" clip that pulls the site up over the hero, then scroll pop-ups, a portfolio, before/after sliders, pricing, an FAQ and a lead form with photo upload. Mobile comes first.

**Evidence.** Official docs (Cloudflare, MDN, web.dev, WebKit, Chrome, W3C APG/WCAG, GSAP, Lenis, Astro, Playwright, Lighthouse CI, ElevenLabs), Jake Archibald's alpha-video study and its README, and 3 YouTube transcripts fetched with 60 s spacing (no 429s this time). Encoders were **tested locally** (§4.2). `[inf]` marks our inference. No money was spent, no accounts were created, nothing was committed. Fetched pages were treated as data.

---

## 1. Decision in one screen

| Area | Choice | Why (short) |
|---|---|---|
| Framework | **Astro (static output) + vanilla TypeScript modules**, no UI framework runtime | Zero JS by default, islands only where needed ([Astro islands](https://docs.astro.build/en/concepts/islands/)); content collections for portfolio/pricing/FAQ; deploys as plain static files |
| Motion | **GSAP 3** (core, ScrollTrigger, Flip, SplitText) + **Lenis** | GSAP is now "100% free for all users", plugins included ([GSAP pricing](https://gsap.com/pricing/)); Lenis keeps native scroll, so sticky, anchors and a11y still work ([Lenis](https://github.com/darkroomengineering/lenis)) |
| Ring | **CSS 3D transforms**, not Three.js/R3F | 6–10 flat cards need no lighting or shaders; native `<video>` decoding beats uploading textures every frame [inf] |
| Transparent character | **Stacked-alpha video** (AV1 + HEVC) drawn by WebGL (`stacked-alpha-video`, ~2 kB) | Half the size or less of VP9/HEVC alpha, and it avoids native alpha bugs ([Archibald](https://jakearchibald.com/2024/video-with-transparency/)) |
| Hero logic | **Hand-rolled, typed state machine** (pure reducer + effect layer), shaped like a statechart | ~10 states. Zero dependencies and easy to unit-test. Move to XState v5 if it grows past ~15 states or gains parallel regions [inf] |
| Hosting | **New Cloudflare Pages project** on the same repo, root `site/`. Media on Pages first, then R2 behind a custom domain | Free; Functions + R2 + Turnstile on one platform. Do **not** reuse `peakform-qtzvm` (§2) |
| Form backend | Pages Function `/api/lead` + R2 (photos + lead JSON) + Turnstile + email through a service-bound Worker (`send_email`) or Resend | Pages Functions lack a `send_email` binding (§7) |
| Analytics | Cloudflare Web Analytics (free, cookieless pageviews + RUM) + a first-party event beacon into **Workers Analytics Engine** | No third-party scripts and no consent banner [inf] |
| Quality | TS strict+, ESLint type-checked, Prettier, Vitest, Playwright (WebKit + Chromium, mobile first), axe, visual snapshots, Lighthouse CI budgets | §9–10 |

---

## 2. What the existing Cloudflare project deploys (repo check)

The repo does not mention the name `peakform-qtzvm`. It matches the setup in `peakform/INSTALL_ON_IPHONE.md` (project name "`peakform-` followed by a few random letters"). That project is:

- **Git-connected Cloudflare Pages.** Root directory `peakform`, build `npm run build` (`tsc -b && vite build && node scripts/check-dist.mjs dist`), output `dist`, Node from `peakform/.node-version` (22), production branch `main`. Every pushed branch gets a preview deployment, so this branch's PR builds PeakForm, not anything under `skills/`.
- **No wrangler.toml.** Settings live in the dashboard. Functions come from `peakform/functions/_middleware.ts`, a same-origin **password gate** (`edge/gate.ts`, `PEAKFORM_PASSWORD`, `X-Robots-Tag: noindex`) on **every** request.
- **Private by design.** A PWA service worker scoped to `/`, a CSP with `form-action 'none'`, and a release gate (`check-dist.mjs`) that **fails the build if `plausible.io`** or other trackers appear.
- **CI:** `.github/workflows/peakform-ci.yml` (typecheck, lint, Vitest, build, Playwright on Chromium with iPhone viewports).

**Decision: reuse the platform and pattern, not the project.** A public site can't sit behind a gate that blocks every path and sends `noindex`, and the PWA service worker and CSP would clash [inf]. Create a second free Pages project (`studio-site`) on the same repo, root `site/`, with **build watch paths** so each project rebuilds only for its own folder [inf: verify the setting]. Copy what works: Node 22 pin, strict TS, a `check-dist` gate, phone-viewport Playwright, a path-filtered workflow. Free limits: **25 MiB/file, 20,000 files, 500 builds/month, 1 concurrent build, unlimited previews** ([limits](https://developers.cloudflare.com/pages/platform/limits/)). Cloudflare is pushing Workers static assets (Email Workers, rate limiting and logs are Workers-only). Pages keeps branch controls and non-Cloudflare custom domains ([guide](https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/)). Stay on Pages for now; the output is plain static files, so a later move is cheap [inf].

---

## 3. Stack comparison

| | **Astro 5/6 static** | **Next.js** | **Vite + vanilla TS** |
|---|---|---|---|
| JS shipped by default | 0; per-island opt-in | React runtime on every page | Only what you write |
| Content (portfolio, FAQ, pricing) | Content collections with zod schemas, MD/MDX | Fine, but heavier | Hand-rolled |
| Cloudflare | Static `dist/` with no adapter; SSR adapter optional ([guide](https://developers.cloudflare.com/workers/framework-guides/web-apps/astro/)) | Cloudflare now recommends **vinext (beta)**; OpenNext for legacy; image optimisation "partially supported" ([guide](https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/)) | Static `dist/` |
| Fit for GSAP/DOM/video orchestration | Excellent; plain `<script>` modules | React reconciliation fights imperative media and GSAP; needs refs and cleanup discipline [inf] | Excellent |
| SEO/OG/sitemap | Built in (`@astrojs/sitemap`) | Built in | Manual |
| Verdict | **Choose** | Overkill, with runtime and adapter risk | Good, but you rebuild Astro's page and content layer by hand |

Astro 6+ needs Node ≥ 22.12 (local: 22.22). Codrops covered an Astro + GSAP + Lenis portfolio in Feb 2026; the article returned 403, so we read only the search summary.

**Motion alternatives:** Motion (ex-Framer Motion) has no ScrollTrigger-grade pinning or Flip, and CSS scroll-driven animations can't sync to video time [inf]. Use **GSAP as the one timeline engine**, with `gsap.matchMedia()` (`ScrollTrigger.matchMedia` is deprecated) and `ScrollTrigger.refresh()` after layout changes ([ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)). Drive Lenis from the GSAP ticker so there is **one RAF loop**:

```ts
const lenis = new Lenis();            // respectReducedMotion defaults to true
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((t) => lenis.raf(t * 1000));
gsap.ticker.lagSmoothing(0);
```

Lenis caveats: no CSS scroll-snap (use `lenis/snap`), a 60 fps cap on Safari, and `syncTouch` is off by default and flaky below iOS 16. Keep touch scrolling native and mark modals `data-lenis-prevent`.

**Ring: CSS 3D is enough.** Radius `tz = round((cardWidth/2) / tan(π/n))` ([Desandro](https://3dtransforms.desandro.com/carousel)). Use a `preserve-3d` ring with one animated `rotateY`, and cards at `rotateY(i·360/n) translateZ(tz)`. Three.js only earns its weight for reflections, depth of field or curved screens [inf]. The ring exposes `setAngle()`/`onSelect()`, so a WebGL renderer could replace it later.

**Gotcha:** Flip "does not accommodate 3D transforms" ([Flip](https://gsap.com/docs/v3/Plugins/Flip/)). To enlarge a card, read its **projected** `getBoundingClientRect()`, put a flat 2D clone there, hide the 3D card, and `Flip.fit` the clone to the stage (`scale: true`).

---

## 4. Video

### 4.1 Format strategy

| Asset | Primary | Fallback | Notes |
|---|---|---|---|
| Character (alpha) | **Stacked AV1 MP4** (colour on top, alpha as luma below) | **Stacked HEVC** (`hvc1`), older Apple | WebGL `<stacked-alpha-video>`. AV1 plays in Chrome, Firefox and Safari on iPhone 15 Pro / M3+. Same clip: stacked AV1 460 kB vs VP9-alpha 1.1 MB vs HEVC-alpha 3.4 MB ([Archibald](https://jakearchibald.com/2024/video-with-transparency/)) |
| Native alpha (optional) | VP9-alpha WebM | HEVC-alpha `.mov` (Mac) | Not primary: no VP9 alpha in Safari, **wrong alpha on Chrome Android**, stalls on Firefox Android (same source) |
| Ring loops (muted) | AV1 MP4 | H.264 MP4 | `<source>` with `codecs=` in `type` ([MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video)) |
| Featured ad (sound) | AV1 + Opus/AAC MP4 | H.264 + AAC MP4 | Progressive. Use HLS only for spots > 30 s [inf] |
| Posters | AVIF | WebP / JPEG via `<picture>` | Hero poster is the LCP candidate. Never lazy-load it |

Pick codecs at runtime with `navigator.mediaCapabilities.decodingInfo()`. Use AV1 only if `smooth && powerEfficient`, because software AV1 drains phones [inf].

**Level trap:** stacking doubles the height, and 720×2560 exceeds AV1 level 4.x's max height of 2176 [inf, AV1 spec]. Use **540×960 → 540×1920** on mobile and 720×2560 (level 5.0) on desktop only.

### 4.2 Encoders available here (tested 2026-10-08)

ffmpeg 6.1.1 (Ubuntu) has `libsvtav1` 1.7.0, `libaom-av1`, `librav1e`, `libx264`, `libx265`, `libvpx-vp9`, `prores_ks`, `libopus`, `aac` and `libwebp`. It has **no `hevc_videotoolbox`**. Tests on a synthetic 720×1280 RGBA clip:

- **Works:** VP9 alpha (`yuva420p`; tagged `alpha_mode=1`; decodes back to `rgba`), stacked AV1 (libsvtav1, 720×2560), stacked HEVC (`libx265 -tag:v hvc1`), and a WebP poster with alpha.
- **Fails:** libx265 alpha ("Incompatible pixel format 'yuva420p'", `alpha=1` unknown) and libsvtav1 alpha (dropped).

So the primary pipeline runs on Linux. Only a native HEVC-alpha `.mov` needs a Mac.

### 4.3 Commands (masters: ProRes 4444 or PNG sequence with alpha)

```bash
# Stacked-alpha filter (unpremultiply if the AI matte is premultiplied; else use the 'premultipliedalpha' attribute)
F='[0:v]format=pix_fmts=yuva444p[m];[m]split[m][a];[a]alphaextract[a];[m][a]vstack'

# Character, stacked AV1 (two-pass libaom per Archibald; CRF 40-48, cpu-used 3-4)
ffmpeg -y -i char_point_L.mov -filter_complex "$F" -pix_fmt yuv420p -an \
  -c:v libaom-av1 -cpu-used 4 -crf 45 -pass 1 -f null /dev/null && \
ffmpeg -y -i char_point_L.mov -filter_complex "$F" -pix_fmt yuv420p -an \
  -c:v libaom-av1 -cpu-used 4 -crf 45 -pass 2 -movflags +faststart char_point_L.av1.mp4

# Character, stacked HEVC fallback (needs lower CRF than AV1)
ffmpeg -y -i char_point_L.mov -filter_complex "$F" -pix_fmt yuv420p -an \
  -c:v libx265 -preset slow -crf 28 -tag:v hvc1 -movflags +faststart char_point_L.hevc.mp4

# Ring loop (muted, no audio track): AV1 via SVT-AV1 (tune=0 = visual), then H.264 fallback
ffmpeg -y -i ad03.mov -vf "scale=-2:720,fps=30" -an -c:v libsvtav1 -preset 5 -crf 38 -g 60 \
  -svtav1-params tune=0 -pix_fmt yuv420p -movflags +faststart ad03.loop.av1.mp4
ffmpeg -y -i ad03.mov -vf "scale=-2:720,fps=30" -an -c:v libx264 -preset slow -crf 24 \
  -profile:v high -pix_fmt yuv420p -g 60 -movflags +faststart ad03.loop.h264.mp4

# Featured ad with sound: same two commands at scale=-2:1080, CRF 34 / 21,
# without -an, plus -c:a libopus -b:a 128k (AV1) or -c:a aac -b:a 160k (H.264)

# Posters (character: decode with libvpx-vp9 to keep alpha) and speech
ffmpeg -y -ss 1.5 -i ad03.mov -frames:v 1 -vf scale=-2:720 ad03.poster.png  # then avifenc/sharp
ffmpeg -y -i vo_intro.mp3 -c:a aac -b:a 96k -movflags +faststart vo_intro.m4a
```

Checks: `ffprobe -show_entries stream=codec_name,profile,level,width,height` on every output, and fail the build if a "muted" loop has an audio stream.

### 4.4 Asset spec table

| ID | Use | Res (mobile / desktop) | Dur | Codecs | Size budget | Preload |
|---|---|---|---|---|---|---|
| `char_idle` | hero idle loop, LCP-adjacent | 540×960 / 720×1280 (stacked ×2 height) | 3–4 s, seamless | stacked AV1 + HEVC | ≤ 350 kB / 600 kB | poster `fetchpriority=high`; video `preload=auto` after first paint |
| `char_point_{L2,L1,C,R1,R2}` | point toward the picked card (nearest of 5 angles) | same | 1.2–1.8 s | same | ≤ 250 kB each | fetch on first ring interaction |
| `char_talk` | speaking loop | same | 2–3 s loop | same | ≤ 300 kB | with point clips |
| `char_reach` | "continue" hand reach | same | 1.5–2.5 s | same | ≤ 400 kB | when the visitor scrolls or hovers near Continue [inf] |
| `adNN.loop` ×6–10 | ring cards, muted | 360×640 / 540×960 (9:16) | 4–6 s | AV1 + H.264, **no audio track** | ≤ 400 kB each | `preload=none`; poster only until the card nears the front |
| `adNN.full` | enlarged player with sound | 720p / 1080p | 15–30 s | AV1+Opus, H.264+AAC | ≤ 4 MB / 8 MB | `preload=metadata` on hover/focus |
| `adNN.poster` | card poster | 360×640 / 540×960 | — | AVIF / WebP / JPEG | ≤ 25 kB | front 3 eager, rest lazy |
| `vo_*` | ElevenLabs lines | — | 2–8 s | AAC `.m4a` | ≤ 80 kB | after first interaction |
| `vo_*.vtt`, `adNN.vtt` | captions | — | — | WebVTT | tiny | with media |
| `portfolio/*` | grid previews | 480p | 3–5 s | AV1 + H.264 | ≤ 300 kB | IntersectionObserver |
| `ba/*` | before/after stills | 1200 px | — | AVIF/WebP | ≤ 120 kB | lazy |

Every clip in the character set starts and ends on the **same hub pose**. That lets any clip follow any other with no visible cut, and the state machine can cut between clips at any end [inf: standard sprite-animation practice]. Keep everything under the 25 MiB Pages limit with a wide margin.

### 4.5 Autoplay, decoders, playback rules

- **Autoplay:** muted + `playsinline` autoplays everywhere. iOS pauses it off-screen, **pauses playback if unmuted without a gesture**, and needs a gesture to `play()` a `display:none` video ([WebKit](https://webkit.org/blog/6784/new-video-policies-for-ios/)). Chrome: "Muted autoplay is always allowed"; "Don't ever assume a video will play" ([Chrome](https://developer.chrome.com/blog/autoplay)).
- **Sound on select:** in the click handler, **synchronously** set `muted = false` and `play()` the featured video and speech audio. Never `await` first [inf]. Handle `play()` rejection with a "Tap for sound" button.
- **Device risk:** `stacked-alpha-video` hides its inner `<video>` with `display:none`, which WebKit's rule above may block. Test on an iPhone. The fallback is `opacity:0; width:1px` [inf].
- **Decoder budget:** there is no official limit. Reports range from ~7 to 32 iOS players, and paused videos may still hold a decoder ([WebKit 193449](https://bugs.webkit.org/show_bug.cgi?id=193449)). Allow **≤ 3 decoding on phones and ≤ 5 on desktop** [inf]. One `MediaManager` gives sources to cards near the front and releases the rest (`pause(); removeAttribute('src'); load()`).
- **Seamless clip switching:** use A/B players. Preload the next clip, start it from `requestVideoFrameCallback` near the current clip's end (fallback `ended`), and swap in the same frame [inf].
- **Lazy:** below-fold media gets `preload="none"` + a poster. Ring loops start on `requestIdleCallback` after LCP. With `saveData`, show posters only [inf].
- **HLS vs progressive:** faststart MP4 covers anything up to ~30 s. HLS needs hls.js outside Safari, so use it only for long reels [inf]. **Stream** is paid ($5/1,000 min stored, $1/1,000 min delivered; [pricing](https://developers.cloudflare.com/stream/pricing/)), so it is out. **R2:** 10 GB free, **zero egress** ([pricing](https://developers.cloudflare.com/r2/pricing/)). But `r2.dev` is rate-limited and dev-only; production needs a custom domain on a Cloudflare zone, which also enables caching ([public buckets](https://developers.cloudflare.com/r2/buckets/public-buckets/)). Serve media from Pages (≤ ~40 MB) until a domain exists, then move it to `media.<domain>` [inf].
- **Range:** Safari probes `bytes=0-1` and rejects a plain 200 (WebKit bugs). No doc states Pages' behaviour, so smoke-test with `curl -sI -r 0-1 <preview>/media/x.mp4` and expect `206` [inf].
- **Caching:** in `_headers`, set `/media/*` and `/_astro/*` to `public, max-age=31536000, immutable`, with hashed filenames ([headers](https://developers.cloudflare.com/pages/configuration/headers/)).

---

## 5. Hero architecture

### 5.1 Layers (back to front)

1. Background (CSS gradient / grain; no video).
2. **Ring** `<section aria-roledescription="carousel">` with a `preserve-3d` container of N `<button class="card">` (poster `<img>` + optional `<video muted playsinline loop>`).
3. **Character** `<stacked-alpha-video>` in two A/B instances, centred, `aspect-ratio` reserved.
4. Captions box (custom-rendered from VTT cues).
5. Controls: Pause motion, Sound, Captions, Continue.
6. **Stage**: `<dialog>` for the enlarged ad (flat 2D clone + full player).

### 5.2 State machine (text diagram)

```
                 ┌───────────── REDUCED_MOTION / SAVE_DATA ──────────────┐
                 ▼                                                        │
[boot] ──assets ok──► [intro] ──speech end/skip──► [idle] ◄──────────────┘
  │ poster shown        char "hello" + vo_intro       │ ring auto-rotates (pausable)
  │                     (muted until first gesture)   │ char_idle loops
  └─error──► [fallback: static hero, list of ads]     │
                                                      │ SELECT(i)  (click / Enter / tap)
                                                      ▼
                                              [pointing(i)] ── ring eases card i to front
                                                      │        char_point_{dir(i)} plays once
                                                      │ clip end (or 1.8 s timeout)
                                                      ▼
                                              [enlarging(i)] ── Flip clone → stage; unmute + play()
                                                      │ tween end
                                                      ▼
                                              [playing(i)] ── char_talk + vo_ad_i + captions
                                               │  │   │
                         SELECT(j) ────────────┘  │   └── CLOSE / Esc / ended ──► [shrinking(i)] ──► [idle]
                         (→ shrinking → pointing(j))
                                                  │ CONTINUE
                                                  ▼
[idle] ──CONTINUE──►  [reaching] ── char_reach plays; at hand-contact frame:
                          │          sheet translateY 100%→0 driven by video time
                          ▼
                     [revealed] ── hero unpinned, Lenis on, ScrollTrigger refresh,
                                   focus → <main> heading;  BACK_TO_TOP → [idle]
```

Rules: the reducer is pure, `(state, event) → {state, effects[]}`, with an exhaustive `switch` on a discriminated union, so TS catches any missing case. Effects (play clip, tween, track event) run in one `effects.ts` that cancels in-flight effects on every transition, which avoids stale `ended` handlers. Every media wait has a **timeout** so a stalled decoder never strands the visitor [inf]. Events get dropped while `enlarging`/`shrinking` run, or queued with depth 1.

### 5.3 Key choreography details

- **Pointing:** the ring brings the picked card to the front first, then the character plays the nearest of 5 pointing clips. In practice `C`/`L1`/`R1` cover most cases, which saves render cost [inf].
- **Speech + captions:** call ElevenLabs **at build time only**, so the key and cost stay off the client (see `13-elevenlabs-mastery.md`). `POST /v1/text-to-speech/{voice_id}/with-timestamps` returns `audio_base64` + per-character `alignment` start/end times ([API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps)). A script groups the characters into ≤ 42-char, ≤ 2-line cues and writes `.vtt` + `.m4a`. At runtime a hidden `<track>` fires `cuechange`, and we render our own caption box. Lip-synced talk clips (one per line) cost more than a generic mouth loop.
- **Continue / pull-up:** `<main>` is a fixed "sheet" at `translateY(100%)`. During `char_reach`, a `requestVideoFrameCallback` loop sets `tl.progress(map(mediaTime, contactT, endT))` on a paused GSAP timeline, so the sheet edge stays locked to the hand even if the video stutters. If rVFC is missing or the video stalls, fall back to a time-based tween. At the end, return `<main>` to the flow and call `ScrollTrigger.refresh()`. Only transforms move, so no CLS ([CLS](https://web.dev/articles/optimize-cls)).
- **Scroll pop-ups:** stacked-alpha clips triggered once by ScrollTrigger `onEnter`, one at a time through the MediaManager, `aria-hidden`.
- **Before/after:** `<input type="range">` driving `clip-path: inset()`, so keyboard support is native [inf].
- **View Transitions** suit small UI swaps, not the live-video enlarge [inf]. We could not read MDN's compat table.

---

## 6. Performance, Core Web Vitals, accessibility, SEO

### 6.1 Budgets (p75 field, mobile)

| Metric | "Good" threshold | Our target |
|---|---|---|
| LCP | ≤ 2.5 s ([web.dev](https://web.dev/articles/lcp)) | ≤ 2.0 s on 4G mid-range |
| INP | ≤ 200 ms ([web.dev](https://web.dev/articles/inp)) | ≤ 150 ms |
| CLS | ≤ 0.1 ([web.dev](https://web.dev/articles/optimize-cls)) | ≤ 0.02 |
| JS before interaction (gz) | — | ≤ 90 kB (GSAP core + ScrollTrigger + app) [inf] |
| CSS (gz) | — | ≤ 25 kB, critical inlined by Astro |
| Fonts | — | ≤ 2 WOFF2, ≤ 80 kB, `font-display: swap` + metric overrides |
| Bytes before first gesture | — | ≤ 1.5 MB mobile, ≤ 3 MB desktop |

- **LCP:** for `<video>`, LCP uses the earlier of the poster load or first frame ([web.dev LCP](https://web.dev/articles/lcp)). Make the **character poster** a real `<img>` (AVIF, ≤ 40 kB) with `fetchpriority="high"` and a `<link rel="preload">`, never `loading="lazy"`. Cloud Four's talk shows lazy-loaded hero images as a classic cause of a 13.9 s lab LCP ([video](https://youtu.be/PDrQAAdcqrk)). The stacked-alpha canvas fades in over it once the first frame is ready.
- **INP:** keep the click handler small. It dispatches to the reducer, calls `play()` synchronously, and schedules tweens. Defer heavy work with `requestAnimationFrame`/`scheduler.yield()` where available. Never read layout after writing it in the same frame. Use `content-visibility: auto` for sections below the fold [inf].
- **CLS:** `width`/`height` or `aspect-ratio` on all media and on `stacked-alpha-video`. Animate only `transform`/`opacity`/`clip-path`.

### 6.2 Reduced motion

Per [web.dev](https://web.dev/articles/prefers-reduced-motion): reduce motion rather than removing everything, and do not autoplay video. Under `prefers-reduced-motion: reduce` (checked with `gsap.matchMedia()` and a live `change` listener):

- The ring becomes a static, scroll-snapping 2D row of posters.
- The character shows its poster.
- Speech plays only on request.
- Continue jumps with a 200 ms fade.
- Lenis already disables smoothing ([Lenis](https://github.com/darkroomengineering/lenis)).

A visible **Pause motion** toggle is required anyway, because looping content longer than 5 s that starts by itself needs a pause/stop/hide mechanism (WCAG 2.2.2, [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)). Persist the choice in `localStorage`.

### 6.3 Accessibility

- **Carousel** ([APG](https://www.w3.org/WAI/ARIA/apg/patterns/carousel/)): `role="region"` + `aria-roledescription="carousel"` + a label without the word "carousel". Each slide is `role="group"` + `aria-roledescription="slide"` + `aria-label="3 of 8: Serum launch, 15 s"`. The **rotation control is the first tab stop**, and rotation stops on focus or hover. Keyboard: one tab stop on the front card, Left/Right rotate, Enter/Space select [inf].
- **Player:** `<dialog>.showModal()` gives a focus trap and Esc. Return focus to the card on close. Keep native `controls`, and give every ad with dialogue a captions `<track>`.
- **Speech:** captions on by default. Set the caption box `aria-hidden` so screen readers don't read over the audio, and put a transcript in a `<details>` [inf]. Sound only after a gesture (WCAG 1.4.2).
- Touch targets ≥ 44 px, visible `:focus-visible` rings, contrast ≥ 4.5:1 over video (use a scrim), and no hover-only affordances.
- **No-JS / failure path:** the server-rendered HTML lists every ad as a link with poster + title, so the page is complete without the hero.

### 6.4 SEO and Open Graph

- Static HTML with one `<h1>` in the hero, real text for services, pricing and FAQ. `@astrojs/sitemap`, `robots.txt`, canonical URL.
- JSON-LD: `Organization`, `Service`/`Offer` for pricing tiers, `FAQPage`, and `VideoObject` for each portfolio ad (`name`, `description`, `thumbnailUrl`, `uploadDate`, `contentUrl`, `duration`). Google mostly indexes video that is the main content of a page, so give each portfolio ad its own `/work/<slug>` page [inf].
- OG: per-page `og:title`, `og:description`, `og:image` 1200×630 (≤ 300 kB JPEG), `twitter:card=summary_large_image`. Generate the images at build time (e.g. Satori), or design them in the art-direction pass.

---

## 7. Lead form (Cloudflare, free tier)

```
browser ──(1) GET Turnstile token (explicit render when form scrolls into view)
        ──(2) resize photos client-side (createImageBitmap → canvas → WebP/JPEG ≤ 2048 px, ≤ 1.5 MB each, ≤ 5 files)
        ──(3) POST /api/lead/start   {turnstileToken, name, email, ... }  → Function: zod-validate, siteverify,
                                                                          honeypot/time check, rate-limit → {leadId, uploadTokens[]}
        ──(4) PUT  /api/lead/:id/photo/:n  (raw body, Content-Type image/*) → Function: check token, size, magic bytes
                                                                          → env.UPLOADS.put(`leads/${id}/${n}.webp`, request.body)
        ──(5) POST /api/lead/:id/finish → write leads/<id>/lead.json to R2 (or a D1 row) → notify → 200 {ok}
```

- **Why this shape:** the Free plan gives **10 ms CPU**, **128 MB memory** and a **100 MB body** per request ([limits](https://developers.cloudflare.com/workers/platform/limits/)). Streaming a raw body into R2 costs almost no CPU, while parsing big multipart bodies risks both limits [inf]. Presigned R2 PUTs (≤ 7 days, S3 keys as secrets, the `r2.cloudflarestorage.com` domain only, bucket CORS; [presigned](https://developers.cloudflare.com/r2/api/s3/presigned-urls/)) are for files over ~20 MB.
- **Bindings:** Pages supports `wrangler.toml` with `pages_build_output_dir` and bindings for `r2_buckets`, `kv_namespaces`, `d1_databases`, `services`, `analytics_engine_datasets` and others. `send_email` is **not listed** ([Pages wrangler config](https://developers.cloudflare.com/pages/functions/wrangler-configuration/)).
- **Email notification:** (a) a tiny Worker with a `send_email` binding (`env.EMAIL.send({to, from, subject, text})`) called through a **service binding**. It needs a sending domain verified on Cloudflare, and recipients can be limited with `allowed_destination_addresses` ([send email](https://developers.cloudflare.com/email-routing/email-workers/send-email-workers/)). Or (b) Resend's free plan, 3,000/month and **100/day** ([Resend](https://resend.com/pricing)), but that needs an account, so ask the user. Until either exists, leads land in R2 and the owner checks a gated `/admin` route. Reuse the PeakForm `edge/gate.ts` pattern on `/admin/*` only [inf].
- **Turnstile:** load `https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit` (never proxy or cache it) only when the form nears the viewport, so it does not cost LCP. Use `appearance: 'interaction-only'` ([client](https://developers.cloudflare.com/turnstile/get-started/client-side-rendering/)). **Server-side siteverify is mandatory.** Tokens last 300 s and are single-use. Send an `idempotency_key` on retries ([server](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/)). Test keys: site `1x00000000000000000000AA` (pass) / `2x00000000000000000000AB` (fail), secret `1x0000000000000000000000000000000AA` (pass) / `2x…AA` (fail) / `3x…AA` (duplicate) ([testing](https://developers.cloudflare.com/turnstile/troubleshooting/testing/)).
- **Validation:** one zod schema in `src/lib/lead-schema.ts`, imported by the form (inline errors, `aria-describedby`, `aria-invalid`, error summary focused on submit) **and** by the Function. Server checks: email format, length caps, an allow-list for budget/timeline enums, `image/jpeg|png|webp|heic` by **magic bytes** not by extension, ≤ 5 files, ≤ 4 MB each after client resize. Strip EXIF location: client re-encoding via canvas drops it [inf]. Add a honeypot field and reject submits faster than 3 s.
- **Privacy:** private bucket, a consent checkbox for using the photos to make samples, and a 90-day retention note. Delete after that, either by hand or with a cron Worker [inf]. Disclose it in the privacy page.
- **CSP** (via `_headers`): `script-src 'self' https://challenges.cloudflare.com https://static.cloudflareinsights.com; frame-src https://challenges.cloudflare.com; media-src 'self' https://media.<domain> blob:; connect-src 'self' https://cloudflareinsights.com; form-action 'self'` [inf: confirm hosts in devtools].

---

## 8. Analytics and event plan

- **Cloudflare Web Analytics:** free, "does not collect or use your visitors' personal data", gives pageviews and Web Vitals from the Performance API ([about](https://developers.cloudflare.com/web-analytics/about/)). It does not offer custom events.
- **Custom events:** `navigator.sendBeacon('/api/e', JSON)` → a Pages Function → `env.EVENTS.writeDataPoint({blobs, doubles, indexes})` (Analytics Engine binding). No cookies, no IDs, IP not stored. Query it with SQL later [inf: confirm Analytics Engine free-tier quota].
- **Alternatives:** Plausible (cookieless, `plausible('Event',{props})`, paid or self-hosted; [docs](https://plausible.io/docs/custom-event-goals)). PostHog with `cookieless_mode: 'always'` (server-side hash, no cookies or storage; [docs](https://posthog.com/docs/privacy/data-collection)) if funnels and session replay are wanted later. Its script is heavier: load it on idle.

| Event | Props (no PII) | Question it answers |
|---|---|---|
| `hero_ready` | `ms_to_first_char_frame`, `codec` (av1/hevc/poster) | Is the hero fast, and which path ran? |
| `ring_interact` | `method` (drag/arrow/click) | Do people engage with the ring? |
| `ad_select` | `ad_id`, `index` | Which ads pull clicks? |
| `ad_sound_on` / `ad_play_failed` | `ad_id`, `reason` | Autoplay/gesture problems |
| `ad_progress` | `ad_id`, `pct` (25/50/100) | Watch depth |
| `captions_toggle` / `motion_pause` | `on` | A11y usage |
| `continue_click` | `from_state` | Hero → site conversion |
| `section_view` | `section` (portfolio/pricing/faq/form) | Scroll depth |
| `ba_slider_used` | `item` | Proof engagement |
| `pricing_cta` | `tier` | Purchase intent |
| `faq_open` | `q_id` | Objections |
| `form_start` / `form_upload` / `form_submit` | `files`, `kb_total` / `ok`, `error_code` | Funnel and failure points |
| `rm_active`, `save_data` | bool | How many visitors get fallbacks |

---

## 9. Code: structure and standards

### 9.1 Folder tree

```
site/
├─ astro.config.ts            # output: 'static', sitemap, build.assets hashing
├─ wrangler.toml              # pages_build_output_dir="dist"; r2_buckets UPLOADS; analytics_engine EVENTS; services MAILER
├─ package.json  .node-version(22)  tsconfig.json  eslint.config.js  .prettierrc
├─ lighthouserc.json  playwright.config.ts  vitest.config.ts
├─ public/
│  ├─ _headers  _redirects  robots.txt  og/…
│  └─ media/                  # encoded output only (hash-named); masters never committed
├─ media-src/                 # gitignored masters (ProRes 4444, WAV)
├─ scripts/
│  ├─ encode.ts               # masters → renditions (§4.3), ffprobe checks, manifest.json
│  ├─ voice.ts                # ElevenLabs with-timestamps → .m4a + .vtt (build-time, cost-capped, cached)
│  └─ check-dist.mjs          # budgets: bytes per route, no audio in loops, no secrets, required files
├─ src/
│  ├─ pages/  index.astro  work/[slug].astro  privacy.astro  404.astro
│  ├─ layouts/Base.astro      # head, SEO, OG, JSON-LD, CSP-safe scripts
│  ├─ components/             # markup only: Hero.astro Ring.astro Character.astro Stage.astro
│  │                          # Portfolio.astro BeforeAfter.astro Pricing.astro Faq.astro LeadForm.astro
│  ├─ content/  ads/*.md  work/*.md  faq/*.md  pricing.json   # + content.config.ts zod schemas
│  ├─ hero/
│  │  ├─ machine.ts           # pure reducer: State, Event, Effect unions
│  │  ├─ effects.ts           # runs effects; cancellation; timeouts
│  │  ├─ ring.ts              # CSS-3D ring: layout math, drag/inertia, keyboard, setAngle()
│  │  ├─ character.ts         # A/B stacked-alpha players, clip queue, rVFC sync
│  │  ├─ stage.ts             # flat clone + Flip, <dialog>, focus return
│  │  ├─ pullup.ts            # continue choreography driven by video time
│  │  └─ captions.ts          # VTT cue → caption box
│  ├─ media/  manager.ts (decoder budget)  pick-codec.ts (MediaCapabilities)  manifest.ts
│  ├─ motion/ ticker.ts (gsap.ticker + Lenis)  reduced.ts (matchMedia)  reveal.ts
│  ├─ lib/    lead-schema.ts  analytics.ts  dom.ts
│  └─ styles/ tokens.css  base.css  hero.css
├─ functions/api/
│  ├─ lead/start.ts  lead/[id]/photo/[n].ts  lead/[id]/finish.ts
│  ├─ e.ts                    # analytics beacon
│  └─ _shared/ turnstile.ts  rate-limit.ts  magic-bytes.ts
├─ tests/   machine.test.ts  ring-math.test.ts  vtt.test.ts  lead-schema.test.ts  functions/*.test.ts
└─ e2e/     hero.spec.ts  a11y.spec.ts  form.spec.ts  visual.spec.ts  reduced-motion.spec.ts
mailer-worker/                # optional: send_email Worker behind a service binding
.github/workflows/site-ci.yml
```

### 9.2 Standards

- **TypeScript:** `astro/tsconfigs/strictest` plus `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `verbatimModuleSyntax`. No `any`. Discriminated unions for machine states/events. `satisfies` for config objects. Function types from `@cloudflare/workers-types` (or `wrangler types`).
- **Lint/format:** ESLint flat config with `typescript-eslint` `strictTypeChecked` + `stylisticTypeChecked`, `eslint-plugin-astro`, `eslint-plugin-jsx-a11y` rules for Astro, `no-floating-promises` (catches unhandled `play()`). Prettier + `prettier-plugin-astro`. Stylelint optional.
- **Component boundaries:** `.astro` files own markup and content only. Every behaviour module exports `mount(root: HTMLElement, deps): () => void` and returns its teardown. One orchestrator (`hero/index.ts`) wires machine ↔ effects ↔ modules. Modules never import each other, only receive callbacks [inf]. One ticker, one MediaManager, one analytics sink. Design tokens as CSS custom properties.
- **Creative-studio pattern** [inf, common "experience" boilerplates; no fetched case study confirmed it]: one `Experience` owns `resources` (manifest + preloader), `sizes`, `time` (one RAF) and scene modules with `init/resize/update/destroy`. A `?debug` flag mounts lil-gui for timing and easing. Motion tokens live in one file. Prototype the hardest interaction (the pull-up sync) first, in code. Bjarne Christensen (Awwwards Amsterdam) argues for prototyping core functionality early and staying "on the actual platforms" ([talk](https://youtu.be/d1ljyNgjT0g)). Gil Huybrecht's SOTD breakdown hands off type scales and a 12-col/6-col grid, then QAs with the developer ([video](https://youtu.be/3yZ3ifVsh74)).

---

## 10. Test plan

| Layer | Tool | Cases |
|---|---|---|
| Unit | Vitest | Machine: every state × event (table-driven, includes illegal events and timeouts); ring math (`tz`, nearest-front index, wrap-around); angle → pointing clip; ElevenLabs alignment → VTT (cue length, line breaks, timing monotonic); lead schema (valid/invalid); magic-byte sniffing; Turnstile helper with the test secrets |
| Functions | Vitest + `wrangler pages dev` / Miniflare | `/api/lead/*` happy path; bad token; duplicate token; oversize body (413); wrong MIME; rate limit; R2 object written; mailer called once |
| E2E | Playwright, projects: **WebKit iPhone 13**, **Chromium Pixel 7**, Desktop Chrome, Desktop Safari (WebKit installs on GitHub-hosted Ubuntu with `--with-deps`; it could not install in this sandbox [inf]) | Hero loads poster then video (`!paused`, `currentTime` advances); no audio before gesture; select → dialog open, `muted === false`, captions cue shows; keyboard-only path (Tab to ring → arrows → Enter → Esc → focus back on card); Continue → `<main>` heading focused, hero unpinned; decoder budget (≤ 3 `video[src]` playing on mobile projects); `saveData`/codec fallback via `?codec=h264`; form with test sitekey + mocked upload |
| Reduced motion | `page.emulateMedia({ reducedMotion: 'reduce' })` | No autoplaying video, no ring rotation, Continue instant, Lenis smoothing off |
| A11y | `@axe-core/playwright` (already used in PeakForm) | Zero serious/critical violations on every route and in the open dialog; carousel roles/labels asserted |
| Visual | `expect(page).toHaveScreenshot()` with `?still=1` (app hook that seeks all videos to a fixed frame and pauses) + masks on live media; baselines made in CI's Linux image only ([snapshots](https://playwright.dev/docs/test-snapshots)) | Hero, ring at 3 angles, stage open, each section at 375/390/430/1440 widths, light/dark if themed |
| Perf | Lighthouse CI (`staticDistDir: dist`, 3 runs, mobile) ([config](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md)) | `largest-contentful-paint ≤ 2500`, `cumulative-layout-shift ≤ 0.05`, `total-blocking-time ≤ 200`, `resource-summary:script:size ≤ 92160`, `resource-summary:font:count ≤ 2`, `resource-summary:third-party:count ≤ 3`; `lighthouse:recommended` for a11y/SEO/best practices |
| Release gate | `scripts/check-dist.mjs` | Bytes per route, no file > 20 MiB, no secrets/keys, no audio stream in `*.loop.*`, every `<video>` has a poster + `playsinline`, every ad has a `.vtt` |
| Field | CF Web Analytics RUM + `hero_ready` | p75 LCP/INP/CLS per device weekly; alert if LCP p75 > 2.5 s [inf] |
| Device lab (manual, before launch) | Real iPhone (older non-AV1 model + 15 Pro+), a mid Android, iPad, Firefox desktop | Alpha edges (premultiplied?), clip seams, autoplay in Low Power Mode, sound on first tap, Range `206` probe |

---

## 11. Build and deploy steps

1. **Scaffold** (no accounts needed): `npm create astro@latest site -- --template minimal --typescript strictest`, then add `gsap lenis stacked-alpha-video zod` and dev deps (`@astrojs/sitemap`, `typescript-eslint`, `eslint-plugin-astro`, `prettier-plugin-astro`, `@playwright/test`, `@axe-core/playwright`, `vitest`, `@lhci/cli`, `wrangler`). Pin `.node-version` to 22.
2. **Media:** put masters in `site/media-src/` (gitignored) → `npm run encode` → `public/media/*` + `manifest.json` (hashes, sizes, codecs). Commit encoded output while the total is ≤ ~40 MB. After that, `wrangler r2 object put` to the media bucket and set `PUBLIC_MEDIA_BASE`.
3. **Voice:** `npm run voice` (build-time ElevenLabs with the existing cost cap and cache; see `18-automation-pipeline.md`) → `.m4a` + `.vtt`.
4. **Local:** `npm run dev`; full stack with Functions: `npm run build && npx wrangler pages dev dist` (secrets in gitignored `.dev.vars`, as PeakForm does). Use the Turnstile test keys.
5. **Verify:** `npm run verify` = typecheck → lint → vitest → build → check-dist → playwright → lhci.
6. **CI:** `.github/workflows/site-ci.yml`, `on.pull_request.paths: ['site/**', '.github/workflows/site-*.yml']`, same shape as `peakform-ci.yml`, plus `npx playwright install --with-deps chromium webkit` and `lhci autorun`. Upload traces and the LH report on failure.
7. **Cloudflare (user does this in a browser, free):** Workers & Pages → Create → Pages → Connect to Git → `claude-skills`. Project `studio-site`, production branch `main`, framework preset Astro, build `npm run build`, output `dist`, **root `site`**, build watch paths `site/**`. Add the same exclusion (`site/**`) to PeakForm's project so it stops rebuilding for site changes [inf]. Create the R2 bucket `studio-uploads` (private) and a Turnstile widget. Set encrypted vars `TURNSTILE_SECRET`, plus `RESEND_API_KEY` or the mailer service binding. Bindings live in `wrangler.toml`.
8. **Previews:** each PR gets a `*.studio-site.pages.dev` preview. Run the smoke test against it: HTTP 200 on `/`, `206` on a media Range probe, `/api/lead/start` with the test key → 200.
9. **Production:** merge to `main`. Roll back from the Pages dashboard (Deployments → Rollback). Add a custom domain when bought. That also unlocks R2 custom-domain media and `send_email`.

---

## 12. Open risks

1. iOS autoplay of the hidden inner `<video>` in `stacked-alpha-video`: test on a device first (§4.5).
2. Range/206 behaviour of Pages for MP4: probe on the first preview.
3. The decoder ceiling on low-end Android is unknown: the MediaManager budget is a guess and needs a device check.
4. Email needs a domain or a Resend account. Both need the user.
5. Character art: all clips need one hub pose and a clean (un)premultiplied matte. Check edges on dark and light backgrounds.

## Sources

Cloudflare: [Pages limits](https://developers.cloudflare.com/pages/platform/limits/) · [Pages wrangler config](https://developers.cloudflare.com/pages/functions/wrangler-configuration/) · [Pages bindings](https://developers.cloudflare.com/pages/functions/bindings/) · [Pages headers](https://developers.cloudflare.com/pages/configuration/headers/) · [Pages→Workers guide](https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/) · [Workers limits](https://developers.cloudflare.com/workers/platform/limits/) · [R2 pricing](https://developers.cloudflare.com/r2/pricing/) · [R2 public buckets](https://developers.cloudflare.com/r2/buckets/public-buckets/) · [R2 presigned URLs](https://developers.cloudflare.com/r2/api/s3/presigned-urls/) · [Stream pricing](https://developers.cloudflare.com/stream/pricing/) · [Send email](https://developers.cloudflare.com/email-routing/email-workers/send-email-workers/) · [Turnstile server](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/) · [client](https://developers.cloudflare.com/turnstile/get-started/client-side-rendering/) · [testing](https://developers.cloudflare.com/turnstile/troubleshooting/testing/) · [Web Analytics](https://developers.cloudflare.com/web-analytics/about/) · [Astro on Cloudflare](https://developers.cloudflare.com/workers/framework-guides/web-apps/astro/) · [Next.js on Cloudflare](https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/).
Media: [Archibald, video with transparency](https://jakearchibald.com/2024/video-with-transparency/) · [stacked-alpha-video README](https://github.com/jakearchibald/stacked-alpha-video) · [WebKit iOS video policies](https://webkit.org/blog/6784/new-video-policies-for-ios/) · [Chrome autoplay](https://developer.chrome.com/blog/autoplay) · [MDN video](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video) · WebKit bug [193449](https://bugs.webkit.org/show_bug.cgi?id=193449) (concurrent decoders) · [webrtcHacks on WebMediaPlayer limits](https://webrtchacks.com/srcobject-intervention/).
Web quality: [LCP](https://web.dev/articles/lcp) · [INP](https://web.dev/articles/inp) · [CLS](https://web.dev/articles/optimize-cls) · [prefers-reduced-motion](https://web.dev/articles/prefers-reduced-motion) · [APG carousel](https://www.w3.org/WAI/ARIA/apg/patterns/carousel/) · [WCAG 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html) · [MDN View Transitions](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API).
Libraries: [GSAP ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) · [Flip](https://gsap.com/docs/v3/Plugins/Flip/) · [GSAP pricing](https://gsap.com/pricing/) · [Lenis](https://github.com/darkroomengineering/lenis) · [Astro islands](https://docs.astro.build/en/concepts/islands/) · [XState](https://stately.ai/docs/xstate) · [Desandro 3D carousel](https://3dtransforms.desandro.com/carousel) · [Playwright snapshots](https://playwright.dev/docs/test-snapshots) · [Lighthouse CI config](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/configuration.md) · [ElevenLabs with-timestamps](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps) · [Plausible events](https://plausible.io/docs/custom-event-goals) · [PostHog cookieless](https://posthog.com/docs/privacy/data-collection) · [Resend pricing](https://resend.com/pricing).
Talks (transcripts, 60 s spacing): [Gil Huybrecht, Award-winning website process](https://youtu.be/3yZ3ifVsh74) · [Bjarne Christensen, Awwwards Amsterdam](https://youtu.be/d1ljyNgjT0g) · [Cloud Four, lazy-loaded LCP image](https://youtu.be/PDrQAAdcqrk). Search summary only (article 403): [Codrops, Joffrey Spitzer Astro+GSAP portfolio](https://tympanus.net/codrops/2026/02/18/joffrey-spitzer-portfolio-a-minimalist-astro-gsap-build-with-reveals-flip-transitions-and-subtle-motion/).
