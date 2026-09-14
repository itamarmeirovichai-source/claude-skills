# Smash House Burgers — Boca Raton (concept proposal)

A working site, not a mockup. **Zero dependencies**: no GSAP, no Three.js, no CDN. The
scroll damping, matrix maths, WebGL renderer, split-text, sunset calculation and physics
are all in this folder. That means it runs offline, it was testable here, and nothing can
break because a CDN changed.

| File | What |
|---|---|
| `smash-house-boca-raton.html` | **The whole site in one file.** Open it in a browser. |
| `index.html` + `css/` + `js/` | The same site as editable source |
| `build.cjs` | Inlines the source into the single file |
| `shot.cjs`, `qa.cjs`, `mobile.cjs` | The screenshot harnesses used to check the work |

## What's in it
- **The 8-beat signature sequence** in hand-written WebGL: the toss on ballistic arcs,
  bullet time (object time freezes, the camera keeps orbiting), the close-up, the explode
  with nine DOM labels projected from 3D, the half turn, the smash with squash and camera
  shake, the cut with two halves opening on real interior faces, and the page splitting
  along the cut line into the menu.
- **Live opening state**, computed from a real sunset calculation for Boca Raton
  (lat 26.3683, lon -80.1289): Sun–Thu 11:00–23:00, Friday closed, Saturday opening one
  hour after Shabbat ends. It drives the header pill, the hero line, the hours table and
  the neon sign together.
- Hero with split-text, scroll-velocity squash and a canvas heat haze; the menu as a
  ticket rail; press-and-hold to smash a patty with a perfect-crust window; a neon sign
  that is lit only when the restaurant actually is; a griddle footer that takes grill
  marks from the pointer; a custom cursor; `prefers-reduced-motion` throughout.

## Honest limits
- **No real brand assets.** Their logo, Kong and food photography are on a CDN this
  environment cannot reach, so the site is built on typography and the brand palette.
  Drop the real assets in and it gets substantially better.
- **The burger is procedural WebGL, not the Blender render.** The asset contract and the
  Blender scene for the photoreal frame sequence are in `research/run4-blender-handoff/`.
  This is the real-time fallback the spec calls for — correct and smooth, not photoreal.
- **Fonts load from Google Fonts.** Offline you get the fallback stack.
- Every unverified fact is tagged `[TO CONFIRM]` on the page itself. No invented prices.

## QA hook
Add `#qa` to the URL and `window.__setP(0.83)` drives the sequence straight to any beat,
bypassing scroll and damping. That is how every beat in this build was inspected.

## Not published
This page carries a real restaurant's name, address, phone and live ordering links. It is
`noindex` and carries a "not affiliated" footer, and it is delivered as a file rather than
a public URL on purpose — putting it on a shareable link is the owner's call, not mine.
