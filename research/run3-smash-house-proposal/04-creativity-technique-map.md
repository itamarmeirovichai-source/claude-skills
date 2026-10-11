CHATGPT MESSAGE 4 of 8 — THE EXAMPLE SITE. Continue applying the spec exactly. Don't build yet — wait until you have all 8 parts.

# 10. CREATIVITY PASS
Five more ideas invented at the signature sequence's level, rated, then the best two added to the build.

| # | Idea | WOW | Effort | Perf risk |
|---|---|---|---|---|
| 1 | **THE PASS** — a fixed "kitchen pass" window follows you down the menu. Every item you tap is built in front of you and clipped to a live order ticket. At the bottom, a hand slides the finished ticket through the pass and it flies to Toast. | 5 | 4 | 2 |
| 2 | **SMASH CAM** — the hero is framed as a fixed overhead griddle camera with a timestamp and a faint scanline; on scroll it cuts to a second angle with a one-frame glitch, like a kitchen security feed. | 3 | 3 | 2 |
| 3 | **THE WEIGHT** — scroll inertia varies by section: heavy sections (the burger) resist slightly more than light ones (text). The site has mass. | 4 | 3 | 1 |
| 4 | **SHABBAT MODE** — on Shabbat the entire site becomes a different site: colour drains to a warm dimmed palette, all motion stops, the neon is dark, Kong sleeps, and one line glows — the countdown to Motzei Shabbat. | 5 | 2 | 1 |
| 5 | **THE ORDER OF OPERATIONS** — a horizontally pinned assembly line: griddle, press, cheese, bun, bag. Each station is a real control you operate. Your burger comes out the end in a bag, and the bag is the order button. | 5 | 5 | 3 |

## Added to the build: #4 SHABBAT MODE and #1 THE PASS

**Why #4.** It is the highest-value idea in this document relative to its cost. No competitor has it and none can copy it credibly. It converts the brand's single biggest commercial constraint — closed Friday, closed Saturday until after dark — into the thing people screenshot. It costs almost nothing: the state is already computed for the neon sign and Kong, and "stop everything" is cheaper than any animation. And it is the most honest possible expression of a Glatt kosher brand: the site keeps Shabbat too.
*Built:* one `data-shabbat="true"` attribute on `<html>`, set server-side. It swaps the token palette to dimmed values, sets a global CSS rule that disables every animation and transition (the same branch `prefers-reduced-motion` uses — so it is already tested), pauses all WebGL rendering, and reveals the countdown panel. Nothing is disabled that would break navigation, the menu, or Sunday's ordering.
*Rejected variant:* actually blocking the order button. Do not — the Toast link must stay available for people planning ahead, and blocking it would be a commercial decision that is the owner's to make, not ours. `[TO CONFIRM with the owner whether they want ordering suppressed on Shabbat.]`

**Why #1.** Every other moment on this site is spectacle; this one is spectacle that *is* the conversion path. It's an interactive demonstration of the product — the research is unambiguous that this beats decoration — and it removes the worst moment in any restaurant site, the cold jump from browsing to a third-party ordering page. By the time the visitor reaches Toast they have already assembled an order and watched it built.
*Built:* a `position: sticky` pass window on the menu page holding the real-time glTF; tapping a menu item animates that item into the window and adds a line to the ticket (real DOM text, not an image); the ticket is a GSAP Draggable element on the rail; the final hand-off uses brand moment #18 — Toast opens first, the ticket flies second. *Mobile:* the pass collapses to a bottom sheet that expands on tap. *Reduced motion:* items appear in the window without the flight; the ticket still fills.

**Rejected and why:** #3 THE WEIGHT is genuinely lovely but it is scroll-jacking without a story reason — variable scroll resistance is indistinguishable from lag on a slow phone, which is the one thing this site cannot afford. #5 is the best idea here and the most expensive; it is the natural phase two. #2 fights the signature sequence for the same real estate.

---

# 11. TECHNIQUE MAP

## Per section
| Section | Techniques from the research |
|---|---|
| Preloader | Scrubbed real-progress animation (W9) · hard 1.5s cap (W17) |
| Hero | Split-text char reveal with masked lines (W5) · velocity-squash type (W5) · fluid cursor trail (W3) · heat haze (W3/W20) · Rive mascot with pointer inputs (W8/W13) · sticky CTA (W17) |
| Signature sequence | Pinned scrubbed timeline (W1) · Apple-style image sequence on canvas (W1) · ballistic arcs + decaying spin (W18) · speed ramp + bullet time (W22) · push-in + rack focus (W22) · exploded view with projected DOM callouts (W18) · squash on impact + camera shake (W21/W22) · clipping-plane cross-section (W18) · split-screen cut transition (W9) · shape match-cut with Flip (W9) |
| Menu | Real-world metaphor UI — ticket rail (W10) · Draggable + Inertia physics (W8) · FLIP card-to-fullscreen (W10) · filterable grid with Flip (W10) · ⌘K command palette (W9) · mini-explode (W18) · THE PASS sticky configurator (W11) |
| Catering | Matter.js physics pile (W8/W20) · slider with physical feedback (W7) · form with inline validation (F6) |
| Locations | Map flyover (W11) · globe with instanced pins (W11) · live status signage (W13) · neon flicker (W3) |
| App / loyalty | Rive state machine climbing out of the phone (W8) · scroll-driven stamp fill (W1) |
| Gift card | Holographic foil shader + gyroscope tilt (W3/W6) |
| Reviews | Clip-path reveal (W4) · real data only (W13) |
| Social | Infinite drag canvas (W10) |
| Footer | WebGL trail texture griddle marks (W3/W20) · jukebox sound toggle (W12) |
| 404 | SVG mask + 2D physics crumbs (W8) |
| Site-wide | Lenis + GSAP single loop (W19) · View Transitions bun wipe (W9) · custom spatula cursor (W6) · magnetic buttons (W7) · GPU tiering with fallbacks (W16) · Shabbat Mode global state (W13) |

## The micro-interaction layer — every interactive element, without exception
| Element | Micro-interaction |
|---|---|
| Primary button | Magnetic pull 0.3× within 80px · fill wipe from the pointer's entry edge · `scale 0.96` press with spring release · 40ms haptic tick on Android |
| Secondary / text link | Underline draws from the entry side · label text-roll on hover |
| Menu ticket | Pendulum idle · lifts 4px and shadow deepens on hover · mini-explode on tap |
| Form field | Floating label · focus ring `2px #FEEB13` at 2px offset · inline validation on blur only · shake + red border on error · a checkmark that draws on valid |
| Slider / stepper | Detent tick every step (sound + haptic) · handle overshoots 6% and settles |
| Toggle | Knob overshoots with a spring · track colour crossfades |
| Card | 3D tilt to ±6° from pointer · image scales 1.04 inside an overflow-hidden frame |
| Tab / filter | Active pill morphs between tabs with Flip · results re-flow with Flip |
| Accordion | `grid-template-rows: 0fr → 1fr` · chevron morphs with MorphSVG |
| Image | Blur-up from a ThumbHash placeholder, cross-faded on `decode()` |
| Quantity / counter | Number rolls vertically, old digit out, new digit in |
| Nav item | Staggered reveal on menu open · hover-preview image follows the cursor (desktop) |
| Sound toggle | Record spins up / slows to a stop |
| Anything that loads | Skeleton matching the final layout exactly — never a spinner |
| Anything that succeeds | Morph from loading to a drawn checkmark, then a confetti burst in brand colours for a completed order or form |
| Every hover above | Has a defined tap, focus and scroll-into-view equivalent. No exceptions. |

## Simplification order — if the budget is breached, cut in exactly this order
1. KONG CATCH mini-game (#19)
2. KONG SHADES SELFIE (#10) — highest effort-to-conversion ratio on the list
3. INSTAGRAM WALL (#9) → a simple static grid
4. LOCATIONS GLOBE (#8) → a static map with pins
5. THE PASS (creativity #1) → menu items still deep-link, just without the live build
6. FRIES RAIN (#12) and HUNGER-METER (#3) → keep one, cut the other
7. HOLOGRAPHIC GIFT CARD (#5) → the CSS conic-gradient version
8. SAUCE TRAIL (#10) and HEAT HAZE (#11) → the CSS/canvas2D versions
9. BUILD YOUR SMASH (#6) → a 2D layer picker
10. TICKET-PRINTER REVIEWS (#7) → a clean review grid, still real reviews
11. MENU MINI-EXPLODE (#14) → hover scale only

**Never cut, at any budget:** the signature sequence · the live open/closed status and Shabbat logic · Shabbat Mode · the order hand-off · the foundations in item 4 · the accessibility and smoothness specs. Those are the proposal. Everything above them is the show.
