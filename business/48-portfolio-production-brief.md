# 48 — Illustrative Portfolio Production Brief

**Scope: a property that does not exist.** Generated from scratch for the public portfolio
([34](34-website-specification.md)) and for OD-3 ([46](46-open-decisions.md)).

**Why this is permitted here and forbidden everywhere else.** [26](26-property-accuracy-rules.md)
prohibits inventing rooms, views, amenities and geometry — because a guest arrives at a real
property and a real listing gets penalised (E-11, E-12). **None of that applies to a property
that has no address, no guests and no listing.** Nothing can be misrepresented.

Two conditions, both absolute:
1. Labelled **"Illustrative. Not a client property."** wherever it appears
   ([21](21-claim-register.md)).
2. **These prompts must never be run on a client's photographs.** For real property the prompt
   library in [23](23-scripts-and-storyboards.md) applies: camera behaviour only, never content.
3. Vendor output-rights terms still apply before publishing — V-0.6
   ([47](47-v0-verification-worksheet.md)).

**On "viral":** we design for attention, not for virality. [29](29-content-calendar.md) forbids
promising it. These prompts aim to make someone stop scrolling — which is craft, not a guarantee.

---

## 1. The consistency system

The hardest part of a generated property is that it must be **the same property in every frame**.
Models drift. Three mechanisms, used together:

| Mechanism | How |
|---|---|
| **Property Bible** | The block in §2 is pasted **verbatim, unchanged, into every single prompt**. Do not paraphrase it between shots — paraphrase is how drift starts |
| **Seed locking** | Where the tool exposes a seed, fix it and keep it across the set |
| **Reference image** | Generate the hero exterior first. Feed it as a style/subject reference for every later shot (Midjourney `--cref` / `--sref`, Runway reference image, Veo reference) |
| **Recurring signature objects** | The chess set, the brass candelabra, the worn boots (§2). Repeated objects do more for perceived continuity than repeated adjectives |

**Order of generation matters:** exterior hero first (it defines the building), then the main
interior (it defines the material palette), then everything else with both as references.

---

## 2. The Property Bible — paste into every prompt

```
THE RIDGE HOUSE: a single-storey cantilevered cabin clad in charred black
shou-sugi-ban timber, projecting out over a steep pine ridge above a deep
blue fjord. Floor-to-ceiling black-framed glass on the valley side.
Interior: pale wide-plank oak floors, lime-plaster walls in warm off-white,
solid walnut joinery, unlacquered brass fittings aged to a dull gold,
charcoal linen upholstery. A blackened steel wood burner with a visible
stack of split birch. Signature details that appear throughout: a long
live-edge walnut dining table with a half-finished chess game and a single
tarnished brass candelabra; a pair of worn tan leather boots by the door;
one hardback book left open face-down. Nordic, quiet, expensive but not
flashy. Photorealistic architectural photography.
```

**Global negative, append to every prompt:**
```
no people, no text, no logos, no watermarks, no clutter, no plastic,
no oversaturation, no HDR halos, no fisheye distortion, no warped
straight lines, no duplicated furniture, no impossible geometry
```

---

## 3. Image prompts — ten shots of one property

Each = **Property Bible + shot line + negative.**

### IMG-1 — Hero exterior *(generate first; this is the reference for everything else)*
```
Wide exterior architectural shot at blue hour, low drone altitude, the
cantilevered black timber volume projecting out over the ridge with warm
interior light glowing through the full-height glass, mist sitting in the
fjord below, dark pines in silhouette, a single lit window reflecting on
wet rock. Shot on 24mm tilt-shift, verticals perfectly corrected, long
exposure, deep cool blue sky against warm 2700K interior light.
Cinematic, photorealistic, high dynamic range handled naturally.
```

### IMG-2 — Main living space
```
Interior wide of the open living space, camera low at 1.1m, looking toward
the full-height glass and the fjord beyond, late afternoon sun raking across
the pale oak floor in long bands, dust suspended in the light shafts, the
blackened steel wood burner lit with a low orange flame, charcoal linen sofa
with one deliberately creased cushion, the open book face-down on the arm.
Shot on 35mm, f/4, natural contrast, warm neutral grade.
```

### IMG-3 — The dining table *(the scroll-stopper)*
```
Three-quarter view of the long live-edge walnut dining table, the half-
finished chess game mid-move with one black knight lying on its side beside
the board, the tarnished brass candelabra with three unlit beeswax candles
and old wax runs down the stems, two clay cups with cold coffee, low winter
sun cutting across the grain of the wood and catching the edge of the
brass. Shot on 50mm, f/2, shallow depth of field, the far end of the table
falling gently out of focus.
```

### IMG-4 — Kitchen
```
Kitchen detail, solid walnut cabinetry with unlacquered brass pulls showing
fingerprint patina, honed black soapstone counter, a single copper pan
hanging, fresh rosemary in a chipped ceramic jug, one lemon cut in half on
a wooden board, morning light from the left through the tall glass.
Shot on 35mm, f/2.8, soft natural shadows, warm neutral grade.
```

### IMG-5 — Principal bedroom
```
Bedroom at dawn, bed dressed in rumpled oatmeal linen with the duvet folded
back on one side only, black-framed glass filling the wall with the fjord
still in blue shadow, a brass reading lamp still switched on, the worn tan
leather boots visible just inside the doorway. Shot on 35mm, f/2.8,
cool ambient light balanced against a single warm practical.
```

### IMG-6 — Bathroom
```
Freestanding blackened-steel bathtub positioned directly against the
floor-to-ceiling glass, steam rising and fogging the lower third of the
pane, a folded grey linen towel over the rim, unlacquered brass filler,
the fjord visible through the clear upper glass, overcast diffused light.
Shot on 28mm, f/4, muted cool palette with warm brass accents.
```

### IMG-7 — Entry
```
Entry hall looking back toward the closed front door, the worn tan leather
boots placed neatly on dark slate, a charcoal wool coat on a single brass
hook, a narrow shaft of light under the door, everything else in soft
shadow. Shot on 35mm, f/2.8, low-key, quiet.
```

### IMG-8 — The cantilever from below
```
Dramatic low-angle exterior looking up at the underside of the cantilevered
volume, charred timber texture in raking side light showing the alligator
grain of the burn, exposed blackened steel structure, pine trunks framing
the edges, overcast sky. Shot on 20mm, verticals corrected, high detail
in the black textures, no crushed shadows.
```

### IMG-9 — Terrace at night
```
Exterior terrace at night, a sunken firepit with low flame, two empty
chairs angled toward the fjord with a wool blanket thrown over one arm, warm
firelight on the charred black timber wall behind, the valley completely
dark below, stars faintly visible. Shot on 35mm, f/1.8, long exposure,
firelight as the only source.
```

### IMG-10 — Detail macro
```
Extreme close-up of the brass candelabra base on the walnut grain, old wax
runs, a fingerprint in the patina, one fallen chess piece just in frame and
out of focus behind. Shot on 90mm macro, f/2.8, razor-thin focal plane,
warm low light.
```

---

## 4. The hero video prompt

**Reality check first.** Current models reliably produce **5–10 seconds** of coherent motion. A
full drone choreography — approach, orbit, hold, push in, pull out — **will not survive one
generation**. Attempting it in a single prompt produces drift, morphing architecture, and warped
lines. **Generate it as four segments and cut them together.** That is how the shot actually gets
made.

### SEG-1 — The approach (6s)
```
[PROPERTY BIBLE]

Aerial drone shot, slow forward push at low altitude, rising gently from
below the ridge line to reveal the cantilevered black timber house
projecting out over the fjord, golden hour, long shadows from the pines,
warm interior light just becoming visible through the glass.
Smooth gimbal, no shake, constant slow speed, cinematic 24fps motion blur.
Architecture completely static and structurally consistent.
```

### SEG-2 — The orbit (8s) — *the money shot*
```
[PROPERTY BIBLE]

Aerial drone orbit, camera circles the house slowly from left to right at
constant radius and constant altitude, keeping the cantilevered corner
centred in frame, the fjord rotating behind it, sun flaring briefly through
the pines at the midpoint of the arc. Perfectly smooth circular motion,
no altitude change, no speed change.
Architecture completely static, straight lines remain straight,
proportions unchanged throughout.
```

### SEG-3 — The hold and push (6s)
```
[PROPERTY BIBLE]

Drone holds completely still facing the full-height glass wall, then begins
a very slow push in toward the lit interior, the living space and the
walnut dining table with the brass candelabra becoming visible through the
glass, interior warm 2700K against cool blue exterior dusk.
Locked-off start, then smooth linear push. No rotation.
```

### SEG-4 — The pull out (8s)
```
[PROPERTY BIBLE]

Drone pulls back and climbs steadily, the house receding and shrinking
against the vast dark fjord and ridge line, one warm lit window remaining
visible as the final point of light, mist filling the valley below.
Smooth continuous reverse motion, steady climb, no rotation.
End wide and still.
```

**Assembly:** SEG-1 → SEG-2 → SEG-3 → SEG-4 ≈ 28s. Cut on motion. Grade all four to one LUT so
the segments match — mismatched grade between segments is the most visible seam.

---

## 5. Hooks — the first 1.5 seconds

A video without a hook does not get watched, whatever the production quality. Ten openings for
this property:

| # | Hook | Mechanism |
|---|---|---|
| 1 | Open on the **fallen chess knight**, pull back to reveal the whole house | Curiosity from a detail |
| 2 | Black frame → hard cut to the cantilever from below | Scale shock |
| 3 | Steam fogging the bath glass, wiped clear to reveal the fjord | Reveal |
| 4 | The boots by the door, then the view they came back from | Story implied |
| 5 | Start mid-orbit, already moving | No setup, instant motion |
| 6 | One lit window in total darkness, push in | Isolation |
| 7 | Firelight on charred black timber, pull back to the terrace | Texture then context |
| 8 | Top-down of the house on the ridge edge, tilt up to the fjord | Vertigo |
| 9 | The candle being lit, cut wide as the room warms | Cause and effect |
| 10 | Rain on the glass, rack focus to the fire inside | Contrast: cold out, warm in |

**Rules that survive contact with a feed:** meaning in frame one, legible with sound off, no
title card, no logo, no slow build. Hooks 1, 3 and 10 are the strongest — each opens on a small
thing and widens.

---

## 6. Production order

1. IMG-1 (hero exterior) → lock the seed, save as reference
2. IMG-2 (living space) → defines the material palette; save as second reference
3. IMG-3 → IMG-10, each with both references attached
4. Cull: keep only frames where the building and palette match. **Expect to discard a lot**
5. SEG-1 to SEG-4, using IMG-1 as the reference image
6. Assemble, grade to one LUT, add hooks
7. Export the 7 package formats — `tools/template_motion.py` handles the stills-derived cuts
8. **Label every published frame "Illustrative. Not a client property."**

**Log every attempt**: prompt, model, seed, accepted or rejected. That is what converts A-09 and
A-10 from estimates into measurements ([15](15-financial-model.md)).
