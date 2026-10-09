# Smash House Burgers — Boca Raton (concept proposal)

A working site, not a mockup. **Zero dependencies**: no GSAP, no Three.js, no CDN. The
scroll damping, matrix maths, WebGL renderer, split-text, sunset calculation and physics
are all in this folder. That means it runs offline, it was testable here, and nothing can
break because a CDN changed.

| File | What |
|---|---|
| `smash-house-boca-raton.html` | **The whole site in one file.** Open it in a browser. |
| `index.html` + `css/` + `js/` | The same site as editable source |
| `build.cjs` | Inlines the source into the single file and into `dist/index.html` |
| `dist/` | What Cloudflare Pages serves: `index.html`, `_headers` (noindex), `robots.txt` |
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
- **Their logo and the Kong arm load from their own CDN in the visitor's browser.** This
  container cannot reach `cdn.smashhouseburgers.com`, so they were wired to the real URLs
  with a graceful fallback rather than fetched: if the image loads it replaces the
  typographic lockup and Kong's hand enters during bullet time; if it does not, the
  wordmark stays and nothing breaks. Verified in both states.
- **Food photography is still missing** for the same reason. Drop real photos into the
  menu tickets and the site gets substantially better.
- **The burger is procedural WebGL, not the Blender render.** The asset contract and the
  Blender scene for the photoreal frame sequence are in `research/run4-blender-handoff/`.
  This is the real-time fallback the spec calls for — correct and smooth, not photoreal.
- **Fonts load from Google Fonts.** Offline you get the fallback stack.
- Every unverified fact is tagged `[TO CONFIRM]` on the page itself. No invented prices.

## QA hook
Add `#qa` to the URL and `window.__setP(0.83)` drives the sequence straight to any beat,
bypassing scroll and damping. That is how every beat in this build was inspected.

## Deploying to Cloudflare Pages
This container's network policy blocks `api.cloudflare.com`, so the deploy runs on GitHub
Actions instead, where there is full internet. `.github/workflows/deploy-proposal-site.yml`
bundles `site/` and pushes `site/dist` to Cloudflare Pages on every push.

It needs two repository secrets, which only you can create
(**Settings -> Secrets and variables -> Actions -> New repository secret**):

| Secret | Where to get it |
|---|---|
| `CLOUDFLARE_API_TOKEN` | Cloudflare dashboard -> My Profile -> API Tokens -> Create Token -> **Cloudflare Pages: Edit** |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare dashboard -> Workers & Pages -> the Account ID in the right sidebar |

Add them, then run the workflow (Actions tab -> Deploy proposal site -> Run workflow).
The URL comes back as `https://smash-house-proposal.pages.dev`.

Manual alternative, no secrets, about a minute: Cloudflare dashboard -> Workers & Pages ->
Create -> Pages -> Upload assets, and drag in `site/dist/`.

## Not published
This page carries a real restaurant's name, address, phone and live ordering links. It is
`noindex` and carries a "not affiliated" footer, and it is delivered as a file rather than
a public URL on purpose — putting it on a shareable link is the owner's call, not mine.
