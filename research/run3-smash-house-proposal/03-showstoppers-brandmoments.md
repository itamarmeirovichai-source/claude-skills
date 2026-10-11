CHATGPT MESSAGE 3 of 8 — THE EXAMPLE SITE. Continue applying the spec exactly. Don't build yet — wait until you have all 8 parts.

**Rules for everything in this message:** lazy-load each one about one viewport before its section; every one has a mobile version and a reduced-motion version; sound is OFF by default with a visible toggle; anything that cannot hold 60fps on a mid-range Android gets simplified, not shipped slow. **The signature sequence is never cut.**

# 8. SHOW-STOPPERS BEYOND THE SCROLL — build all fifteen

**1. NEON SIGN THAT TELLS THE TRUTH.** A neon "SMASH HOUSE — OPEN" sign in `#E51144`, mounted in the Boca section. It **flickers on when they are actually open** (two false starts then steady, a 900ms tube-warm ramp), fizzles down to a dead grey tube when closed, and on Shabbat reads "BACK AFTER SHABBAT" in the same tube style.
*Built:* SVG tube paths + `feGaussianBlur` glow + a CSS custom-property intensity driven by a keyframed flicker curve; state comes from the server-computed booleans, so it is correct with JS off. *Mobile:* same, smaller tube. *Reduced motion:* no flicker, just the correct steady state.

**2. HOLIDAY MODES.** Hebcal-aware. Holiday closures appear automatically with the holiday's name. Kong wears a Purim costume on Purim; a menorah beside him gains a candle per night of Chanukah; Pesach shows a `[TO CONFIRM]` note about menu changes.
*Built:* the server component returns `holidayKey`; a map of `holidayKey → Rive input + CSS theme class`. Never hard-code dates — they move every year. *Fallback:* unknown holiday key → the normal state, never a broken one.

**3. HUNGER-METER.** "How hungry are you?" — drag the slider and patties stack higher on a plate. Past a threshold the tower wobbles, leans and topples with physics. It then **recommends a real menu item** matched to the level.
*Built:* GSAP Draggable + Inertia on the handle; Matter.js for the stack (cap 24 bodies desktop / 12 mobile, sleep on rest). Recommendation is a lookup into the real CMS menu — never an invented item. *Reduced motion:* the stack grows without the topple; the recommendation still appears.

**4. CATERING PARTY PLANNER.** A guests slider fills the screen with a physics pile of burgers and fries. Releasing it opens the catering inquiry with the guest count prefilled.
*Built:* Matter.js, bodies spawned on a rate proportional to guest count, capped at 90 desktop / 40 mobile, despawned off-screen. **No prices anywhere** — the output is "we'll quote you", and the form posts the count. *Mobile:* fewer, larger bodies.

**5. HOLOGRAPHIC GIFT CARD.** A 3D card in their red and yellow that tilts with the mouse, or with the gyroscope on mobile, under a holographic foil shader. Flip it to see the back, then buy.
*Built:* a single R3F plane with a Fresnel × iridescent-gradient shader; `DeviceOrientationEvent` on mobile (iOS needs `requestPermission()` fired from a tap — show a "tilt me" button). *No WebGL:* a CSS `background: conic-gradient` card with a `rotate3d` tilt.

**6. KONG CLIMBS OUT OF THE APP.** A phone rises into frame, Kong climbs out of its screen and over the bezel, and the QR code scans in behind him. The loyalty stamp card fills with smash-shaped stamps as you scroll.
*Built:* Rive state machine driven by a ScrollTrigger progress input; the QR is a real generated code pointing at the app store links `[TO CONFIRM URLs]`. *Reduced motion:* Kong sits beside the phone; the stamps appear without the climb.

**7. TICKET-PRINTER REVIEWS.** Real Google reviews print out of a kitchen ticket printer, line by line, with the paper curling.
*Built:* Google Places API fetched **server-side** and cached, rendered per Google's attribution requirements. Paper revealed with `clip-path: inset()` plus a per-line reveal; printer chatter only if sound is on. **Only real reviews — never a written example, never a placeholder star rating.** `[TO CONFIRM Places ID and API access]` *If reviews cannot be sourced, the section does not ship.*

**8. LOCATIONS GLOBE.** A spinning globe or US map with a burger pin for every real location. The Boca pin glows and pulses; tapping it opens directions.
*Built:* MapLibre GL globe projection, or three-globe with an `InstancedMesh` of pins. Locations come from the CMS `[TO CONFIRM the full location list]`. *Mobile:* a flat US map, no globe rotation. *No WebGL:* a static map image with positioned pin links.

**9. INSTAGRAM WALL.** Their real posts as a draggable infinite canvas of polaroids, scattered and rotated, that you can throw around.
*Built:* server-fetched feed into your own grid (never the official embed — it is heavy and unstyleable); modulo-wrapped translate + Draggable with Inertia. `[TO CONFIRM feed access and rights to re-display]` *Mobile:* a swipeable row, not an infinite canvas.

**10. KONG SHADES SELFIE.** The camera opens **only on an explicit tap**, puts Kong's sunglasses on your face, and lets you save or share the shot.
*Built:* MediaPipe Tasks Vision `FaceLandmarker`, glasses anchored to the eye landmark indices and scaled to the interpupillary distance. Loaded lazily on tap, torn down on exit, with a visible "camera is on" indicator and a privacy line stating nothing is uploaded. *No camera / denied:* a static "Kong-ify a photo" upload path instead.

**11. "WHAT ARE YOU CRAVING?" SEARCH.** ⌘K (and a visible search button for touch) opens instant fuzzy search over the menu with FLIP-animated results.
*Built:* `cmdk` + Fuse.js over the CMS items and their tags; results animate with GSAP Flip; each result deep-links to the item.

**12. JUKEBOX SOUND TOGGLE.** A tiny vinyl record in the corner that spins while sound is on and slows to a stop when muted.
*Built:* Howler with a single shared gain node; state in `localStorage`; **off by default, always.** The spin is a CSS rotation that pauses, so it costs nothing.

**13. GRIDDLE FOOTER.** The cursor — or a finger — leaves glowing grill marks on a hot steel footer. They sizzle, brighten, then cool and fade.
*Built:* a WebGL plane with a trail texture (a render target advected and decayed each frame, quarter resolution), heat colour ramped from `#FEEB13` through `#E51144` to `#401C10`. *Mobile:* touch draws the same marks. *No WebGL:* a canvas2D trail with `globalCompositeOperation = 'lighter'`.

**14. "KONG ATE THIS PAGE" 404.** The page has a bitten edge with tooth marks; crumbs fall and pile at the bottom with physics; a burp plays if sound is on; a big obvious way home.
*Built:* an SVG bite mask on the content edge, Matter.js crumbs (cap 40), and a real navigation menu underneath — a designed 404 still has to work as a 404.

**15. TYPE "KONG".** A keyboard easter egg: buffer the last four keys; on "KONG" the screen shakes, Kong roars if sound is on, and a banana falls past the viewport.
*Built:* a keydown buffer, a GSAP shake with 300ms decay, and `document.body` transform only. Desktop only; harmless if never found.

---

# 9. BRAND MOMENTS — build all nineteen. Each one echoes THE SMASH.

**1. THE SMASH PRESS.** Press and hold a raw beef ball on a griddle; a 3D spatula comes down and smashes it flat. Longer hold = flatter patty, deeper crust, louder sizzle, grease sparks, a haptic buzz on Android. Release in the perfect window and you get a "PERFECT CRUST" badge in `#FEEB13`.
*Built:* a rAF accumulator on `pointerdown`; the patty deforms with a volume-preserving scale (`sx = 1/√sy`) and its crust texture mixes darker; the perfect window is 0.62–0.78 of full hold, shown as a filling ring so it never feels unfair. *Touch:* identical (long-press), with `touch-action: none` only on the ball itself so the page still scrolls. *Reduced motion:* a tap plays the full smash at once and still awards the badge.

**2. SQUASHED TYPE.** A giant "SMASH" in the display face, squashed and stretched by scroll velocity, springing back when you stop.
*Built:* `ScrollTrigger.getVelocity()` normalised and clamped to ±18%, applied via `gsap.quickTo` to `scaleY` (and the `wght` axis if a variable face is available), released with `elastic.out(1, 0.5)`. Clamp hard — uncapped, it reads as a bug.

**3. KONG ALIVE.** A Rive state machine. His eyes follow the cursor. His sunglasses slide down his nose when you hover "Order Now". He beats his chest on the impact beat of the signature sequence. On Shabbat he rests beside the line "Shabbat Shalom — grill fires up tonight at [computed time]". On Saturday night he greets "Shavua Tov!".
*Built:* inputs `pointerX`, `pointerY`, `hoverOrder`, `smashImpact`, `isShabbat`, `isMotzeiShabbat`, fed from the same server booleans as the neon sign. Eyes clamp to the socket radius via `Math.atan2`. An idle loop always runs — he is never frozen. *Mobile:* eyes track the last touch, then return to an idle wander.

**4. MOTZEI SHABBAT COUNTDOWN.** A live countdown to opening, from real sunset times.
*Built:* the server returns the exact opening timestamp (Shabbat end + 60 minutes) from Hebcal; the client counts down to it and refreshes the page state at zero. The static sentence is in the HTML, so it is correct without JS.

**5. KITCHEN TICKET RAIL.** The menu as order tickets clipped to a steel rail. Pull one down to open the item; it swings on its clip with real physics.
*Built:* Draggable `type:'y'` with bounds and inertia; a sine-driven pendulum idle with a per-ticket phase offset; opening uses GSAP Flip into a full-screen card. **The dish name, description and price stay real DOM text** — the metaphor never hides the content from search or screen readers.

**6. BUILD YOUR SMASH.** Stack your own burger from the real layer set. Each layer drops in with physics and squishes on landing. Ends with a shareable image and "Order the closest match".
*Built:* the real-time glTF (`/models/hero.glb`) with the contract's mesh names; drop uses a short fall plus a squash-and-settle; the share image is rendered to a canvas and offered through the Web Share API with an OG-image endpoint fallback. "Order the closest match" maps the stack to a real menu item and deep-links to Toast — **only if Toast item deep-links are supported; verify before building, otherwise link to the menu category.** `[TO CONFIRM]`

**7. BUN TRANSITION.** The top and bottom buns close over the screen and open again on the new page.
*Built:* the View Transitions API with two pseudo-element halves, or GSAP if the API is unavailable. Total 620ms. The incoming page's content is already rendered behind them — the transition never delays readiness.

**8. SMASH PRELOADER.** A patty being smashed flatter as load progresses.
*Built:* tied to real asset progress, **capped at 1.5s**, and it never blocks content that is already ready. If everything loads in 300ms, it plays for 300ms and leaves.

**9. SPATULA CURSOR.** The cursor is a spatula. It reads "SMASH" over the burger and "FLIP" over menu tickets.
*Built:* a fixed element on `gsap.quickTo`, label swapped from a `data-cursor` attribute. Hidden entirely on touch — and every hover it carries has a tap equivalent.

**10. SAUCE TRAIL.** A mouse-reactive fluid trail in the chef-sauce colour across the hero.
*Built:* a quarter-resolution ping-pong fluid simulation, tinted, opacity capped at 0.5 so the headline stays legible. Disabled below GPU tier 2, on touch, and whenever the hero is off-screen.

**11. HEAT HAZE.** Griddle heat distortion whose intensity follows scroll speed.
*Built:* screen-space UV distortion sampled from scrolling noise, masked to the griddle region only, amplitude from scroll velocity, clamped. Off under reduced motion.

**12. FRIES RAIN.** Fries fall with 2D physics and pile up; flick them away; brisket and chef sauce drip over the top of the pile.
*Built:* Matter.js, cap 70 desktop / 30 mobile, bodies sleeping once settled and despawned when off-screen; flick velocity from pointer delta. The drip is a metaball SDF shader over the pile.

**13. BLOOMING ONION.** The petals unfold like a flower as the section enters.
*Built:* a scrubbed timeline on per-petal rotation and scale, staggered from the centre out, `back.out(1.4)`. Either the real-time model or a short rendered sequence — **whichever the asset plan delivers; do not fake it with a rotating photo.**

**14. MENU MINI-EXPLODE.** Hovering or tapping a menu item mini-explodes it into its ingredients; tapping again expands it full-screen with FLIP.
*Built:* the same explode maths as beat 4 at a smaller scale, on a lightweight per-item model or a pre-rendered 12-frame sequence. *Touch:* first tap explodes, second opens — with a visible affordance so the two-tap behaviour is never a surprise.

**15. KOSHER STAMP.** The kosher mark slams onto the page with squash, a puff of dust and a thud.
*Built:* scale 3 → 1 on `expo.in`, a one-frame squash, a dust particle burst, a camera-style shake on the containing section. **Uses the real certification mark only once the agency and permission are confirmed** `[TO CONFIRM]` — until then the brand-lockup text "Glatt Kosher" gets the same treatment.

**16. BURGER ON YOUR TABLE (AR).** The baked glTF placed in your room.
*Built:* `<model-viewer ar ar-modes="webxr scene-viewer quick-look">` with `/models/hero.glb` + `/models/hero.usdz`, real-world scale in metres — a three-metre burger is the classic failure here.

**17. LOCATION FLYOVER.** A 3D map flies to The Shops at Boca Grove; a burger pin drops and bounces.
*Built:* Mapbox GL `flyTo` with a `curve` and `speed` tuned to ~2.4s, then a pin drop with `back.out(2)`. *No WebGL / reduced motion:* a static map that cross-fades to the zoomed view.

**18. ORDER HAND-OFF.** A ≤400ms burger-into-the-bag animation — **while Toast is already opening.**
*Built:* on click, fire the analytics event, call `window.open(toastUrl, '_blank')` immediately, and only then play the animation on the page being left. **There is no version of this where the animation runs first.**

**19. KONG CATCH.** Tap Kong five times and a falling-burger mini-game opens.
*Built:* a bounded canvas with Matter.js, lazy-loaded on the fifth tap, skippable, with a score. **Any prize, discount or reward is shown only if the owner approves it** `[TO CONFIRM]` — until then the game ends on a share button and a link to order, never on an offer.
