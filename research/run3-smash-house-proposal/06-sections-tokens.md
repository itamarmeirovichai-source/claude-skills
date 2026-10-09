CHATGPT MESSAGE 6 of 8 — THE EXAMPLE SITE. Continue applying the spec exactly. Don't build yet — wait until you have all 8 parts.

# 13. SECTION-BY-SECTION SPEC

## HOME — `/`

**H0 · Preloader.** Sees: a raw beef ball on a dark griddle, flattening as load progresses; the logo above it; a thin `#E51144` progress line. Interaction: none, skippable by scrolling. Tech: GSAP timeline driven by real asset progress. Timing: capped at 1.5s hard; exits in 400ms with a wipe. Mobile: identical. Reduced motion: a static logo with the progress line only.

**H1 · Hero.** Sees: near-black ground, a giant "SMASH HOUSE" in the display face with the live status line under it ("OPEN UNTIL 11 PM" / "CLOSED — BACK SATURDAY AT 8:42 PM"), Kong at the right edge, heat haze rising off a griddle strip at the bottom, sticky Order button. Interaction: fluid sauce trail follows the cursor; Kong's eyes track it; the headline squashes with scroll velocity; the Order button is magnetic. Tech: SplitText masked line reveal, quarter-res fluid FBO, Rive, `gsap.quickTo`. Timing: headline chars stagger 0.04, 900ms total; status line fades at +300ms. Mobile: no fluid trail, no cursor; Kong tracks the last touch; heat haze at half amplitude. Reduced motion: everything static, status line still live.

**H2 · The signature sequence.** The pinned 620vh / 420vh section specified in message 2. Sees: the eight beats. Interaction: scroll only; the Order button stays clickable throughout. Tech: ScrollTrigger pin + scrub 1, canvas image sequence, DOM overlays on the same progress, Flip match-cut at the end. Timing: beats per the contract. Mobile: 420vh, portrait frame set. Reduced motion: the four-key-frame crossfade.

**H3 · The menu teaser.** Sees: six hero items on a broken asymmetric grid over the near-black ground, prices from the CMS. Interaction: hover/tap mini-explodes an item into its ingredients; a second tap opens it full-screen. Tech: 12-frame alpha sequences, GSAP Flip. Timing: explode 420ms `back.out(1.5)`; Flip open 600ms. Mobile: two columns, first tap explodes with a visible hint, second opens. Reduced motion: cross-fade to the ingredient still.

**H4 · The smash press.** Sees: a raw beef ball on the griddle, the instruction "PRESS AND HOLD", a filling progress ring. Interaction: press and hold — the spatula descends, the patty flattens, crust darkens, sizzle swells, grease sparks fly, Android buzzes. Release in the 0.62–0.78 window for the "PERFECT CRUST" badge. Tech: rAF accumulator, volume-preserving scale, particle burst, Howler gain mapped to hold. Timing: full hold 1.4s; badge slams in over 260ms with squash. Mobile: identical long-press, `touch-action: none` on the ball only. Reduced motion: a tap plays the whole smash at once; badge still awarded.

**H5 · Hunger-meter.** Sees: "HOW HUNGRY ARE YOU?" with a draggable slider and a plate that stacks patties. Interaction: drag; past the threshold the tower wobbles and topples; a real menu item is recommended with a link. Tech: Draggable + Inertia, Matter.js (24 bodies desktop / 12 mobile, sleeping). Timing: topple runs its own physics, ~1.2s. Mobile: 12 bodies, larger. Reduced motion: stack grows, no topple, recommendation still shown.

**H6 · Kong climbs out of the app.** Sees: a phone rising into frame, Kong climbing over the bezel, a QR code resolving behind him, a loyalty stamp card filling with smash stamps. Interaction: scroll-scrubbed; buttons to the app stores. Tech: Rive state machine driven by a ScrollTrigger progress input. Timing: 80vh of scroll. Mobile: platform-detected store button replaces the QR. Reduced motion: Kong beside the phone, stamps fade in.

**H7 · Catering strip.** Sees: a wide catering spread with the guests slider and "PLAN A PARTY". Interaction: the slider fills the screen with a physics pile of burgers and fries; releasing opens the catering form with the count prefilled. Tech: Matter.js (90 / 40 bodies), form prefill via URL state. Timing: spawn rate scales with count; settle within 900ms. Mobile: 40 bodies. Reduced motion: a static pile image scaled to the count.

**H8 · Gift card.** Sees: a floating 3D card in red and yellow under holographic foil. Interaction: tilt with mouse or gyroscope; tap to flip; buy link. Tech: R3F plane with a Fresnel × iridescence shader; `DeviceOrientationEvent` behind a tap on iOS. Timing: flip 700ms `power3.inOut`. Mobile: a "tilt me" button requests motion permission. No WebGL: a CSS conic-gradient card with `rotate3d`.

**H9 · Ticket-printer reviews.** Sees: a steel printer; real Google reviews printing out line by line, the paper curling as it lengthens. Interaction: drag the paper to scroll through more. Tech: server-cached Places API, `clip-path: inset()` line reveal, Draggable. Timing: 45ms per line. Mobile: shorter paper, swipe. Reduced motion: reviews appear as a plain list. **Ships only if real reviews can be sourced.**

**H10 · Locations globe.** Sees: a slowly turning globe with a burger pin per real location; Boca's pin glows and pulses. Interaction: drag to spin, tap a pin for directions. Tech: MapLibre globe or three-globe with instanced pins. Mobile: a flat US map, no spin. No WebGL: a static map with positioned links.

**H11 · Instagram wall.** Sees: their real posts as scattered, rotated polaroids on an infinite canvas. Interaction: drag and throw; tap opens the post. Tech: modulo-wrapped translate, Draggable + Inertia. Mobile: a swipeable row. Reduced motion: a static grid.

**H12 · Griddle footer.** Sees: a hot steel footer with hours, address, phone, links, the kosher lockup, the sound toggle, and the small tag "Concept proposal for Smash House Burgers". Interaction: the cursor or finger leaves glowing grill marks that sizzle, cool and fade. Tech: WebGL trail render target at quarter res; canvas2D `lighter` fallback. Mobile: touch draws the marks. Reduced motion: no trail, static steel.

## MENU — `/menu`

**M1 · Header + filters.** Sees: "THE MENU" in display type, filter pills (All / Burgers / Chicken / Sides / Kids / Desserts), a search button, and the kosher lockup. Interaction: filters re-flow the grid; ⌘K or the button opens fuzzy search. Tech: Flip on filter change, `cmdk` + Fuse.js, filter state in the URL. Timing: Flip 500ms. Mobile: horizontally scrollable pills, full-screen search sheet.

**M2 · The ticket rail.** Sees: order tickets clipped to a steel rail, each with a dish name, description, price and photo — all real DOM text. Interaction: pull a ticket down to open it; it swings on its clip. Tech: Draggable `type:'y'` with bounds + inertia, sine pendulum idle with per-ticket phase, Flip to full-screen. Timing: idle 3.2s period; open 600ms. Mobile: the rail becomes a vertical list; tap opens. Reduced motion: no swing; tap opens with a cross-fade.

**M3 · THE PASS.** Sees: a sticky pass window holding the live 3D burger, with an order ticket beside it. Interaction: tapping a menu item builds it in the window and adds a real text line to the ticket; the finished ticket flies to Toast at the end. Tech: the real-time glTF, GSAP flight path, Toast hand-off per brand moment #18. Mobile: a bottom sheet that expands on tap. Reduced motion: items appear without the flight.

**M4 · Item detail (full-screen).** Sees: a large photo or mini-explode, the full description, allergen and tag chips, price, and an Order button. Interaction: Esc or swipe down to close; arrow keys move between items. Tech: Flip expand with `absolute: true`, focus trap, scroll lock. Mobile: full-screen sheet with a drag handle.

**M5 · Menu footer CTA.** Sees: a giant "ORDER NOW" slab that squashes on press. Interaction: navigates to Toast immediately, animation second.

## CATERING — `/catering`

**C1 · Hero.** Sees: the catering spread, the line "FEED EVERYBODY" `[TO CONFIRM copy]`, and the guest slider. Interaction: the physics pile from H7, at full scale. Mobile: reduced body count.
**C2 · What we bring.** Sees: three or four real catering formats `[TO CONFIRM the real offerings]` as cards. Interaction: 3D tilt, image scale on hover. Reduced motion: static.
**C3 · Inquiry form.** Sees: name, phone, email, date, guest count (prefilled), notes. Interaction: floating labels, validation on blur, a checkmark that draws, success morphs the button and fires confetti in brand colours. Tech: Next.js route handler → Resend; Turnstile + honeypot + 2s time-trap. **No prices anywhere.**
**C4 · FAQ.** Sees: real catering questions `[TO CONFIRM]` in smooth accordions with `FAQPage` schema. Tech: `grid-template-rows: 0fr → 1fr`, MorphSVG chevron.

## BOCA RATON — `/locations/florida/boca-raton`

**B1 · Neon status hero.** Sees: the neon "SMASH HOUSE — OPEN" sign against the near-black ground, the real address and phone, and the live status sentence. Interaction: the sign's state is real; tapping the phone dials. Tech: SVG tube + glow, server-computed state. Reduced motion: no flicker, correct steady state.
**B2 · Hours table.** Sees: Sun–Thu 11:00 AM–11:00 PM · Friday CLOSED · Saturday opens one hour after Shabbat until 12:00 AM, with today highlighted and the computed Saturday time shown. Tech: server-rendered from the Hebcal-derived data, with `openingHoursSpecification` schema.
**B3 · Motzei Shabbat countdown.** Sees: a live countdown to opening, in yellow on near-black. Only rendered when relevant. Tech: server timestamp, client tick, page state refresh at zero.
**B4 · Map + flyover.** Sees: a static map that, on tap, flies to The Shops at Boca Grove and drops a bouncing burger pin. Interaction: directions and call buttons. Tech: Mapbox Static → GL JS `flyTo` 2.4s, pin drop `back.out(2)`. Reduced motion: cross-fade to the zoomed static view.
**B5 · Storefront + interior.** Sees: real photographs of the Boca location. **Never generated.**
**B6 · Order strip.** Sees: the sticky Order slab and the app download row.

## 404 — `/404`
Sees: a page with a bitten edge and tooth marks, crumbs falling and piling at the bottom, Kong chewing, and a large, obvious set of links home, to the menu and to ordering. Interaction: flick the crumbs. Tech: SVG bite mask, Matter.js (40 crumbs). Sound: a burp, only if on. Reduced motion: the bitten edge is static, no crumbs. **The navigation works regardless.**

---

# 14. DESIGN TOKENS

```css
:root {
  /* Brand — exact, no new hues */
  --smash-red:#E51144; --deep-red:#C20F3A; --deeper-red:#BA0C36;
  --near-black:#13110C; --yellow:#FEEB13;
  --blue:#0083B0; --blue-deep:#007198;
  --white:#FFFFFF; --brown:#401C10;

  /* Tints & shades (derived only) */
  --red-90:#F7405F; --red-70:#FA7B90; --red-20:#FBD0D8;
  --black-90:#1E1B14; --black-80:#2A261C; --black-60:#4A443A;
  --yellow-dark:#D6C50F; --brown-light:#5E2D1B;

  /* Type */
  --font-display:"Smash Dollars","Londrina Solid",system-ui,sans-serif;
  --font-display-alt:"Londrina Solid",system-ui,sans-serif;
  --font-body:"Poppins",system-ui,-apple-system,sans-serif;
  --step--1:clamp(.8rem,.76rem + .2vw,.9rem);
  --step-0: clamp(1rem,.95rem + .25vw,1.125rem);
  --step-1: clamp(1.25rem,1.15rem + .5vw,1.5rem);
  --step-2: clamp(1.56rem,1.4rem + .8vw,2rem);
  --step-3: clamp(1.95rem,1.7rem + 1.25vw,2.66rem);
  --step-4: clamp(2.44rem,2rem + 2vw,3.55rem);
  --display: clamp(3rem,10vw,11rem);   /* scale ratio 1.25 */

  /* Spacing — 4px base */
  --s-1:4px; --s-2:8px; --s-3:12px; --s-4:16px; --s-6:24px;
  --s-8:32px; --s-12:48px; --s-16:64px; --s-24:96px; --s-32:128px;

  /* Grid */
  --grid-cols:12; --gutter:var(--s-6); --max:1440px;
  --page-pad:clamp(16px,4vw,64px);

  /* Motion — the 12 principles, as tokens */
  --ease-out:power2.out; --ease-in-out:power2.inOut;
  --ease-spring:back.out(1.6); --ease-impact:expo.in;
  --ease-settle:elastic.out(1,.5);
  --dur-micro:.18s; --dur-base:.36s; --dur-slow:.72s; --dur-cine:1.2s;
  --stagger:.06; --overshoot:1.6;
  --anticipation:.12s;      /* the counter-move before every impact */
  --follow-through:.06s;    /* per depth level of children */
  --shake-decay:.3s;
  --squash-y:.82;           /* --squash-x is 1/sqrt(--squash-y) */
}
html[data-shabbat="true"]{
  --smash-red:#7A2233; --yellow:#8C7F1E; --white:#CFC9BD; --near-black:#0D0C09;
}
html[data-shabbat="true"] *,
@media (prefers-reduced-motion:reduce){*{
  animation-duration:.01ms!important; animation-iteration-count:1!important;
  transition-duration:.01ms!important; scroll-behavior:auto!important;
}}
```

**Contrast rules that are not negotiable:** red on white 4.67:1 ✓ body OK · red on near-black 4.04:1 ✗ body, large text only · yellow on near-black 15.4:1 ✓ · yellow on white 1.23:1 ✗ never · blue `#0083B0` on white 4.31:1 ✗ body — use `#007198` (5.50:1) ✓.

**Grid:** 12 columns, deliberately broken. Never centre everything. Alternate a dense screen with an empty one — the pacing between sections is as much a part of the design as the sections.
