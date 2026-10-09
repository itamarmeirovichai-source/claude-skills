CHATGPT MESSAGE 6 of 7 — RESEARCH RESULTS. These are the results of deep research into how award-level interactive websites (Awwwards / FWA level) are built. Study them carefully — this is your knowledge base from now on. Don't build anything yet. Reply only: "Got it — send the next part."

# G. DEEP DIVE — THE 15 HIGHEST-IMPACT WOW TECHNIQUES FOR A FOOD BRAND

**1. The pinned hero product sequence (rendered frames).**
*Feels like:* the product is being made for you, right now, and you control the projector.
*Build:* pin a section ~500–700vh · one GSAP timeline with labelled beats · progress → frame index on a canvas · DOM overlays (labels, UI) read the same progress · preload every 8th frame then fill.
*Pitfalls:* frames not decoded ahead (stutter), no poster (white flash), non-reversible beats, mobile served the desktop set.
*Gimmick when:* the sequence has no story — it's just a rotating object.

**2. Exploded view with pinned ingredient labels.**
*Feels like:* "I now know exactly what I'm ordering." It converts because it's information disguised as spectacle.
*Build:* per-layer offset × eased progress, staggered by 0.05, `back.out(1.6)` · labels as DOM positioned by projecting world→screen (or drei `<Html>`), billboarded, fading in on a 0.08 stagger behind their layer.
*Pitfalls:* gaps too small to read as separate; labels colliding; labels rotating with the object.
*Gimmick when:* the product has 3 parts and everyone already knows them.

**3. Cross-section cut.**
*Feels like:* a bite. It's the single most appetising shot in food advertising.
*Build:* pre-modelled halves with real interior geometry, rendered · knife enters on an arc with a specular glint sweep (animated anisotropic highlight) · 2-frame squash under the blade · halves separate 2–4cm and rotate 10° toward camera · steam from the cut faces + one slow sauce drip.
*Pitfalls:* a flat boolean face (instantly fake); halves opened too wide (diagram, not food); no steam (dead).
*Gimmick when:* used on something with no interesting interior.

**4. Press-and-hold "smash" mechanic.**
*Feels like:* you cooked it. Hold mechanics create ownership, and ownership converts.
*Build:* `pointerdown` starts a rAF accumulator → deformation amount (scaleY down, scaleX up, volume-preserving) + crust darkening (a texture mix or emissive ramp) + sizzle gain + `navigator.vibrate` ticks on Android · a "perfect window" (e.g. 0.62–0.78) that awards a badge on release · always a tap fallback that runs the full animation.
*Pitfalls:* no visual progress indicator; a window so tight it feels unfair; blocking scroll on touch.
*Gimmick when:* it gates content.

**5. Live "open now" signage tied to real business state.**
*Feels like:* the site is the restaurant, not a brochure about it.
*Build:* compute state server-side from real opening hours plus, for a kosher business, real sunset times (Hebcal's Shabbat/holiday JSON API with the venue's lat/long) · pass booleans to a neon element and to the mascot's Rive state machine · revalidate hourly · render the resulting text into the HTML so it works without JS.
*Pitfalls:* client-side timezone maths (wrong for out-of-state visitors), hard-coded holiday lists that expire.
*Gimmick when:* never. This is the highest trust-per-pixel feature a restaurant site can have.

**6. Menu as a physical object (ticket rail, griddle, board).**
*Feels like:* stepping into the kitchen.
*Build:* CSS-textured tickets hanging from a rail · `Draggable` with `type:'y'`, `bounds`, `inertia` · pull-down opens the item with Flip into a full-screen card · gentle pendulum idle (a sine on `rotation` with per-item phase).
*Pitfalls:* real content buried under metaphor — the dish name, price and photo must still be plain readable text and in the DOM for SEO.
*Gimmick when:* it adds a click to ordering.

**7. Velocity-reactive type ("SMASH" squashing as you scroll).**
*Feels like:* the page has weight.
*Build:* `ScrollTrigger.getVelocity()` → normalised → `scaleY`/variable-font `wght` via `gsap.quickTo`, spring back to rest with `elastic.out(1, 0.5)` when velocity decays. Clamp hard (±18%) or it reads as a bug.
*Pitfalls:* uncapped values, layout-affecting properties, running on every text node on the page.

**8. Physics pile (fries, patties, burgers).**
*Feels like:* abundance. Perfect for catering and "how hungry are you".
*Build:* Matter.js (2D, cheap) for a screen-edge pile; Rapier for 3D · spawn on a timer capped by GPU tier · sleep bodies · flick-to-throw via pointer velocity · despawn off-screen.
*Pitfalls:* unbounded body count; bodies never sleeping; running while off-screen.

**9. Mascot with a state machine.**
*Feels like:* someone's home.
*Build:* Rive `.riv` with inputs for `hover`, `click`, `isOpen`, `isHoliday`, `scrollVelocity` · eyes track the pointer via `Math.atan2` clamped to the socket · idle loop always running · a reaction at the hero sequence's impact beat.
*Pitfalls:* Lottie instead of Rive (no interactivity, bigger, CPU-bound); no idle state (dead-eyed); reacting to everything (annoying).

**10. Match-cut into the CTA.**
*Feels like:* inevitability — the story ends on "Order".
*Build:* GSAP Flip from the final 3D/frame element (a round cut face) to the sticky order button; `absolute: true`, `scale: true`, 0.7s `power3.inOut`.
*Pitfalls:* the button being non-clickable during the transition. It must be clickable the entire time.

**11. Fluid / sauce cursor trail.**
*Feels like:* the page is edible.
*Build:* quarter-res ping-pong FBO fluid sim (or a cheap advected-trail texture), tinted to the sauce colour, additive over the hero, opacity capped ~0.5 so text stays readable · disabled below GPU tier 2 and on touch.
*Pitfalls:* full-res simulation (instant 30fps); running when the hero is off-screen.

**12. Ticket-printer reviews.**
*Feels like:* proof, delivered with theatre.
*Build:* real reviews only (Google Places API, cached server-side, attribution per Google's terms) · paper strip revealed with `clip-path: inset()` + a per-character reveal · printer chatter SFX gated on the sound toggle.
*Pitfalls:* fabricated reviews (legally dangerous); scraping without terms compliance.

**13. AR "on your table".**
*Feels like:* scale and reality — enormously effective for catering platters.
*Build:* `<model-viewer ar ar-modes="webxr scene-viewer quick-look">` with a GLB + USDZ pair baked from the same Blender scene, ≤5MB, real-world scale set correctly in metres.
*Pitfalls:* wrong scale (a 3m burger); no USDZ (no iOS AR); shipping the hero-poly model.

**14. ⌘K craving search.**
*Feels like:* competence. Power users love it; everyone else gets the tap version.
*Build:* `cmdk` + Fuse.js over menu items with tags (`vegan-cheese`, `spicy`, `kids`) · results animate with Flip · a visible search button for touch · results deep-link to the item.

**15. Order hand-off animation that never delays the order.**
*Feels like:* polish, with zero cost.
*Build:* on click, immediately `window.open(orderUrl)` (or set `location`), then play a ≤400ms burger-into-bag animation on the page being left. Fire the analytics event before the animation.
*Pitfalls:* any pattern where the animation runs first and the navigation second. That is a lost order.

---

# H. DECONSTRUCTION — 8 REAL AWARD-WINNING SITES
Awards below were verified as reported on Awwwards. Studio attributions are as reported. **Technical stacks are inferred unless the studio published a case study — treat them as hypotheses, not facts.**

**1. Lando Norris official site — OFF+BRAND. Awwwards Site of the Year 2025.**
- Signature idea: the whole site moves at race pace — speed is the interface, not a decoration.
- Three carrying techniques (inferred): scrubbed WebGL scenes with velocity-reactive motion; aggressive kinetic typography; route transitions that read as camera cuts.
- Stack: inferred WebGL (Three.js) + GSAP on a JS framework.
- Lesson we steal: pick one physical property of the brand (speed, heat, weight) and make *every* interaction obey it.

**2. Messenger — Awwwards Site of the Year 2025.**
- Signature idea: a tiny real-time WebGL planet you can spin, with a delivery character navigating its geography.
- Three carrying techniques: a low-poly stylised real-time world; a character with pathing and personality; a camera that always orbits one legible object.
- Stack: inferred Three.js/WebGL, real-time (not rendered frames).
- Lesson we steal: a *single object you can turn* beats a long scroll. Give the visitor one toy.

**3. Crav Burgers — Awwwards Site of the Day.** https://www.awwwards.com/sites/crav-burgers
- Signature idea (from its own description): burger ordering as a playful, immersive experience — motion design in service of ordering fast.
- Three carrying techniques: immersive product visuals; dynamic motion design; an ordering flow that stays fast under the spectacle.
- Stack: inferred.
- Lesson we steal: for a restaurant, the award-level move is to make *ordering itself* the experience, not to bury a menu under effects.

**4. Promeat — Awwwards Honorable Mention.** https://www.awwwards.com/sites/promeat
- Signature idea: a meat brand told editorially — magazine art direction with WebGL storytelling and crafted UI.
- Three carrying techniques: editorial type and grid; WebGL-driven narrative sections; restrained, crafted micro-UI.
- Stack: inferred WebGL + a JS framework.
- Lesson we steal: art direction carries a food site further than effects. The typography would win with animation off.

**5. Good Meat — Awwwards-featured food brand experience.**
- Signature idea: scroll navigation as the spine of a digital food brand experience.
- Carrying techniques: tagged on Awwwards as 3D, WebGL, Three.js, GLSL, Vue, sound design and storytelling — i.e. custom shaders plus a designed audio layer.
- Lesson we steal: **sound design is a listed award criterion in practice.** A food site with a sizzle layer (off by default) reads as more finished than one without.

**6. EverSwap — Lusion. Awwwards Site of the Day + Developer Award (June 2026).**
- Signature idea: a mock product launch treated as a real launch film.
- Carrying techniques (inferred, consistent with Lusion's published work): heavy custom GPU work, physically-motivated motion, obsessive frame-time discipline.
- Lesson we steal: Developer Awards go to sites whose *performance* is the achievement. Smoothness is a category, not a chore.

**7. Apechain — makemepulse. Awwwards Site of the Day + Developer Award.**
- Signature idea: a branded world with character-led interaction.
- Carrying techniques (inferred): real-time 3D characters, GPU particles, sequenced scroll storytelling.
- Lesson we steal: a mascot given real-time behaviour is worth more than five static illustrations.

**8. Springs — Vide Infra. Awwwards Site of the Day + Developer Award (March 2026).**
- Signature idea: motion built on spring physics as the site's entire personality.
- Carrying techniques (inferred): spring-based motion system, interruptible animation, consistent easing language.
- Lesson we steal: a *named, consistent motion system* is itself a signature idea. You don't need 3D to win.

*Also verified as SOTD + Developer Award winners worth studying: Steven.com (OFF+BRAND), Hubtown (Unseen Studio).*

**What all eight share:** one idea, ruthlessly repeated; typography that works with animation off; motion with physical logic; and no visible frame drops. None of them win on effect count.

---

# I. $5k vs $20k vs $100k

| | **$5k** | **$20k** | **$100k+** |
|---|---|---|---|
| Who builds it | One generalist | A designer + a developer | Creative director, designer, 3D artist, motion dev, front-end dev, PM |
| Timeline | 1–2 weeks | 4–8 weeks | 3–6 months |
| Design | A good template, brand colours applied | Custom design, real grid and type scale, designed 404/empty states | Full art direction: custom type treatment, photo direction, a motion language document, a named concept |
| Assets | Stock photos, client's existing images | A half-day photo shoot + retouching | A shoot + 3D scanning + Blender production + rendered sequences + custom illustration + sound design |
| Motion | CSS transitions, fade-ins on scroll | GSAP + ScrollTrigger, split text, a custom cursor, page transitions | A directed multi-beat cinematic sequence, real-time 3D, shaders, a mascot state machine, audio |
| Foundations | Responsive, a contact form, basic SEO | + CMS, schema, analytics events, accessibility pass, performance budget | + full WCAG 2.2 AA audit, GPU tiering, device-lab QA, monitoring, documented handover |
| Content | Client supplies text | Copy edited and structured | Copy written to the concept; every line is part of the idea |
| What the client is actually buying | A working presence | A site that looks designed | **A reason to talk about them** — a site people screenshot, share, and remember |
| The tell | Looks like the theme it came from | Looks good, feels ordinary | Has one idea you can describe in a sentence, and nothing stutters |

**The uncomfortable truth:** the $100k tier is not "more effects on top of the $20k tier". It's the $20k tier *plus* original assets, plus one directed idea, plus performance engineering — and any one of those missing drops it straight back to $20k, no matter how many shaders are running.
