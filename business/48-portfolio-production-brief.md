# 48 — Illustrative Portfolio Production Brief (ChatGPT / GPT-4o)

**Scope: a property that does not exist.** Generated for the public portfolio
([34](34-website-specification.md)) and for OD-3 ([46](46-open-decisions.md)).

**Why invention is permitted here and nowhere else.** [26](26-property-accuracy-rules.md) forbids
inventing rooms, views, amenities and geometry — because a guest arrives at a real property and a
real listing gets penalised (E-11, E-12). **A property with no address, no guests and no listing
cannot be misrepresented.** Conditions: label every published frame **"Illustrative. Not a client
property."** ([21](21-claim-register.md)); **never run these prompts on a client's photographs**
(there, camera-motion prompts only — [23](23-scripts-and-storyboards.md)); check vendor output
rights before publishing (V-0.6, [47](47-v0-verification-worksheet.md)).

**On "viral":** we design for attention. [29](29-content-calendar.md) forbids promising virality.

---

## 1. Why the first draft of these prompts underperformed

Two diagnosable faults, both fixed below.

**Fault 1 — wrong dialect.** They were written as Midjourney-style comma-separated fragments
(`35mm, f/2, shallow depth of field, warm grade`). **GPT-4o is a language model driving an image
model. It rewards full natural sentences and explicit instruction**, and it degrades on keyword
salad. It also has no negative-prompt parameter — exclusions must be written as plain sentences.

**Fault 2 — soft vocabulary.** Words like *subtle*, *slightly*, *gently* are **ignored by image
models**. "Subtle 5% zoom" produces no visible zoom. Commanding language is obeyed:

| Ignored | Obeyed |
|---|---|
| "slightly tilted" | "OBVIOUSLY tilted 4–6°, the tilt MUST be the first thing the eye notices" |
| "a bit larger" | "DRAMATICALLY larger — at least 130% of everything around it" |
| "softly lit" | "ONE hard light source from frame left, deep shadows on the right, DO NOT lift them" |
| "propped against" | "RESTING ON the sill, physically supported, gravity-correct, casting a real contact shadow" |

**The physical-realism corollary:** every object must be told **what it rests on**. Unanchored
props float, and a floating object is the single clearest "this is AI" tell.

---

## 2. Consistency in ChatGPT specifically

The hard problem is that all images must show **the same house**. ChatGPT solves this differently
from Midjourney:

| Mechanism | How |
|---|---|
| **One conversation, start to finish** | ChatGPT holds image context. Generate every shot in a single thread — never start a new chat mid-set |
| **Reference the previous image explicitly** | "Same house as the previous image. Same oak floor, same brass, same black window frames. Now show the kitchen." This is the strongest lever available and it does not exist in Midjourney |
| **Paste the Identity Block into shot 1, then re-paste on any drift** | §3 below |
| **Signature objects** | The chess set, the brass candelabra, the tan boots. **Repeated objects carry continuity better than repeated adjectives** |
| **Correct, don't restart** | When it drifts: "The window frames went silver. They are MATTE BLACK. Regenerate with black frames, everything else identical." |

**Generation order matters:** exterior hero first (defines the building) → main living space
(defines the material palette) → everything else.

---

## 3. The Identity Block

Paste this into the first prompt, and again any time the model drifts.

```
We are photographing one specific house, and every image in this set must show
the SAME house. Here is what it is:

THE RIDGE HOUSE. A single-storey cabin clad in charred black shou-sugi-ban
timber, cantilevered so one end projects out into open air over a steep pine
ridge above a fjord. The valley-facing wall is floor-to-ceiling glass in MATTE
BLACK frames — never silver, never bronze.

Interior materials, and these never change between shots: pale wide-plank oak
floors, lime-plaster walls in warm off-white, solid walnut joinery, unlacquered
brass fittings aged to dull gold with visible fingerprints, charcoal linen
upholstery, and a blackened steel wood burner beside a stack of split birch.

Three objects recur across the set and must look identical every time: a long
live-edge walnut dining table carrying a half-finished chess game and a
tarnished brass candelabra; a pair of worn tan leather boots by the door; one
hardback book left open face-down.

The mood is Nordic and quiet. Expensive, but never flashy. Photorealistic
architectural photography, never a 3D render.
```

**Universal exclusion line, append to every prompt:**
```
Do not include any people, text, letters, logos or watermarks. Do not produce a
3D render, a video-game look, or an HDR illustration — this must read as a real
photograph. Keep every straight architectural line perfectly straight with no
lens warping. Do not duplicate furniture or invent extra windows. Every object
must rest on a real surface and cast a real contact shadow.
```

---

## 4. The image prompts

Each = **Identity Block (first shot only) + the prompt + the exclusion line.**

### IMG-1 — Hero exterior · *generate first, it anchors the whole set*
```
Create a photorealistic architectural photograph, 4:5 vertical, high resolution.

The subject is The Ridge House seen from a drone hovering slightly BELOW the
level of the cantilever, looking up and across at it. The projecting black
timber volume MUST DOMINATE the frame — it should occupy at least 60% of the
image and read as genuinely heavy, a solid mass suspended over nothing.

Time and light: blue hour, about twenty minutes after sunset. The sky is deep
cool blue, almost navy. Every interior light in the house is on, and that warm
2700K light pours out through the full-height glass in hard rectangles. The
colour contrast between the cold blue exterior and the warm interior MUST BE
EXTREME — this contrast is the entire point of the photograph.

Below and behind: mist sitting low in the fjord, dark pines in near-silhouette,
wet rock in the foreground catching one reflection of a lit window.

Shoot it like a 24mm tilt-shift architectural lens. All vertical lines are
PERFECTLY vertical with zero keystone distortion. Long exposure, so the mist is
smooth and the water is glassy.

[exclusion line]
```

### IMG-2 — Main living space
```
Same house as the previous image, photographed from inside. Same oak floor,
same matte black window frames, same charcoal linen.

Photorealistic interior photograph, 4:5 vertical.

Put the camera LOW — about 1.1 metres from the floor, roughly seated eye
height, NOT standing height — looking through the open living space toward the
full-height glass and the fjord beyond.

Light: late afternoon sun entering hard from frame right and raking ACROSS the
pale oak floor in long bright bands. The bands of light MUST BE CLEARLY VISIBLE
as distinct shapes on the floor, with sharp edges. Dust hangs visibly in the
light shafts. Deep shadow in the left third of the frame — DO NOT lift it.

The blackened steel wood burner is lit with a low orange flame. The charcoal
linen sofa has ONE cushion visibly creased and pushed out of place. The hardback
book lies open and face-down ON the sofa arm, physically resting on it, tilted
slightly, casting a real contact shadow.

What just happened: someone was sitting here reading ten minutes ago and got up
to put another log on the fire. The room should feel recently occupied, never
staged.

[exclusion line]
```

### IMG-3 — The dining table · *the scroll-stopper*
```
Same house. Photorealistic interior photograph, 4:5 vertical.

The long live-edge walnut dining table, shot from a three-quarter angle at
seated eye height. The table MUST DOMINATE the frame, filling at least 70% of
it, running diagonally from the lower-left corner toward the upper right so the
grain leads the eye.

On the table, and all of these are RESTING on the wood with real contact
shadows, nothing floating:
- A chess game abandoned mid-move. One black knight is LYING ON ITS SIDE on the
  board. This fallen piece MUST be clearly visible and in sharp focus — it is
  the detail the whole photograph is built around.
- A tarnished brass candelabra holding three unlit beeswax candles, with old
  wax runs frozen down the stems.
- Two clay cups of coffee gone cold, with a thin skin visible on the surface.

Light: hard low winter sun entering from a window at frame left at a sharp
angle, raking ACROSS the walnut grain so the timber texture is DRAMATICALLY
pronounced, and catching ONE hot specular highlight on the brass. The far end of
the table falls into soft shadow and gentle defocus.

What just happened: two people were playing an hour ago and walked away
mid-game. Nobody has tidied up.

[exclusion line]
```

### IMG-4 — Kitchen
```
Same house. Photorealistic interior photograph, 4:5 vertical.

Walnut cabinetry with unlacquered brass pulls that show REAL fingerprint patina
— the brass must look touched, not polished. Honed black soapstone counter with
a visible matte, slightly uneven surface.

Resting ON the counter, each casting a contact shadow: a wooden board with one
lemon cut cleanly in half, cut faces up and glistening; a chipped ceramic jug
holding fresh rosemary; a single copper pan. Hang one more copper pan from a
brass rail — it must hang from a VISIBLE hook, gravity-correct, not floating.

Light: cool morning light from tall glass at frame left, soft and directional,
with long gentle shadows running to the right. No overhead artificial light.

[exclusion line]
```

### IMG-5 — Principal bedroom at dawn
```
Same house. Photorealistic interior photograph, 4:5 vertical.

The bed is dressed in oatmeal linen and is CLEARLY SLEPT IN — the duvet folded
back on one side only, pillows dented, the whole surface rumpled. It must not
look hotel-made.

The matte black glass wall fills the background and the fjord beyond is still in
deep blue pre-dawn shadow. A single brass reading lamp on the bedside table is
STILL SWITCHED ON, and it is the only warm light in an otherwise cold blue
frame. That one warm point against all that cold MUST be the strongest contrast
in the image.

Just inside the doorway at the frame edge, the worn tan leather boots sit on the
floor, slightly askew, resting flat with real contact shadows.

What just happened: someone woke early, turned on the lamp, and went to make
coffee. They have not come back yet.

[exclusion line]
```

### IMG-6 — Bathroom
```
Same house. Photorealistic interior photograph, 4:5 vertical.

A freestanding blackened-steel bathtub positioned so its long side sits
DIRECTLY against the floor-to-ceiling glass, with no gap. The tub is full and
steam is rising from it.

The steam has FOGGED THE LOWER THIRD of the glass into opacity, while the upper
two thirds stay clear and show the fjord. This split — opaque below, clear above
— MUST be obvious and is the composition of the photograph.

A folded grey linen towel hangs OVER the rim of the tub, draping with real
weight and a visible fold. An unlacquered brass filler arcs over the end.

Light: flat overcast daylight from outside. Cool, muted, desaturated — with the
brass as the only warm element in the frame.

[exclusion line]
```

### IMG-7 — The cantilever from below
```
Same house, exterior again. Photorealistic architectural photograph, 4:5
vertical.

Stand directly beneath the projecting end and shoot steeply UPWARD at the
underside of the cantilever. The dark mass MUST fill the top two thirds of the
frame and feel genuinely heavy and slightly threatening overhead.

The charred shou-sugi-ban timber is lit by hard raking side light so the
alligator-crackle texture of the burn is DRAMATICALLY visible across the whole
surface. Exposed blackened steel structure runs along the underside. Pine trunks
frame both edges of the image. Overcast white sky beyond.

Critical: hold full detail inside the black timber. DO NOT crush the shadows to
solid black — the texture must remain readable everywhere.

[exclusion line]
```

### IMG-8 — Terrace at night
```
Same house. Photorealistic exterior photograph, 4:5 vertical.

A sunken firepit on the terrace with a low, real flame. Two empty chairs angled
toward the fjord, with a heavy wool blanket thrown over one arm — draped with
real weight, falling naturally, not placed.

The firelight is the ONLY light source in the entire image. It must throw warm
flickering light onto the charred black timber wall behind, picking out that
crackle texture, and leave the valley below COMPLETELY DARK. Faint stars in the
sky. No moonlight, no lamps, no other source.

What just happened: two people were sitting here and went inside for more wine.
The fire is still going.

[exclusion line]
```

---

## 5. The hero drone video

**Reality check.** Current video models hold coherent motion for **5–10 seconds**. The full
choreography you want — approach, orbit, hold, push in, pull out — **will not survive one
generation**; it drifts, the architecture morphs, straight lines bend. **Generate four segments
and cut them together.** That is how the shot is actually made.

Use IMG-1 as the reference image for all four.

### SEG-1 — The approach (6s)
```
Aerial drone shot. The camera starts BELOW the ridge line looking at bare rock
and pine, then rises steadily and pushes forward, and as it clears the ridge the
cantilevered black timber house is REVEALED projecting out over the fjord.
The reveal must feel earned — the house is hidden at the start of the shot and
unmistakable by the end.

Golden hour, long shadows from the pines, warm interior light just becoming
visible through the glass.

Motion: smooth gimbal, ONE constant speed, no acceleration, no shake, no
rotation. The architecture is completely static and structurally identical from
first frame to last. Every straight line stays straight.
```

### SEG-2 — The orbit (8s) · *the money shot*
```
Aerial drone orbit. The camera circles the house from left to right at a FIXED
radius and a FIXED altitude, keeping the cantilevered corner locked in the
centre of frame while the fjord and ridge rotate behind it.

At the midpoint of the arc the sun flares briefly through the pine trunks.

Motion: perfectly smooth circular travel at ONE constant speed. The altitude
MUST NOT change. The radius MUST NOT change. No zoom during the orbit.
The building's proportions must remain absolutely identical throughout — no
warping, no morphing, every straight edge straight in every frame.
```

### SEG-3 — Hold, then push in (6s)
```
The drone holds COMPLETELY STILL for the first two seconds, facing the
full-height glass wall straight on — a locked-off shot, zero movement.

Then it begins a slow, steady push straight forward toward the lit interior.
Through the glass, the living space and the walnut dining table with the brass
candelabra become progressively visible.

Warm 2700K interior light against cool blue dusk outside.

Motion: dead still, then smooth linear forward travel. No rotation at any point,
no drift sideways, no altitude change.
```

### SEG-4 — The pull out (8s)
```
The drone pulls backward and climbs at the same time, steadily and continuously.
The house recedes and shrinks against the vast dark fjord and ridge line.

By the final frame the house is small in the frame and ONE warm lit window
remains as the last point of light in an otherwise dark landscape. Mist fills
the valley below.

Motion: smooth continuous reverse travel with a steady climb, ONE constant
speed, no rotation. End wide and completely still.
```

**Assembly:** SEG-1 → SEG-2 → SEG-3 → SEG-4 ≈ 28s. Cut on motion. **Grade all four to one LUT** —
a grade mismatch between segments is the most visible seam in the finished piece.

---

## 6. Hooks — the first 1.5 seconds

| # | Hook | Mechanism |
|---|---|---|
| 1 | The **fallen chess knight** in macro, pull back to the whole house | Small thing → huge thing |
| 2 | Black frame, hard cut to the cantilever from below | Scale shock |
| 3 | Fogged bath glass **wiped clear** to reveal the fjord | Reveal |
| 4 | Rain on glass, **rack focus** to the fire inside | Cold out, warm in |
| 5 | The boots by the door, then the view they came back from | Story implied |
| 6 | Start **mid-orbit**, already moving | No setup |
| 7 | One lit window in total darkness, push in | Isolation |
| 8 | A match struck, the candelabra lights, cut wide as the room warms | Cause and effect |
| 9 | Top-down on the ridge edge, tilt up to the fjord | Vertigo |
| 10 | Firelight on charred timber, pull back to the terrace | Texture → context |

**1, 3 and 4 are the strongest** — each opens on one small thing and widens. Meaning in frame one,
legible with sound off, no title card, no logo, no slow build.

---

## 7. Post-generation checklist

An image generator produces a base layer, not a finished asset.

- [ ] **Check every object rests on something.** Floating props are the clearest AI tell
- [ ] **Check straight lines.** Any bowed window frame or wall — regenerate, do not retouch
- [ ] **Check the set is one house.** Lay all eight side by side. Wrong floor, wrong frame colour, wrong brass → regenerate, don't keep it
- [ ] **Check for text.** GPT-4o inserts stray lettering; any text present means regenerate
- [ ] **Check the signature objects** are identical across every frame they appear in
- [ ] Export PNG, not JPG
- [ ] **Label "Illustrative. Not a client property."**
- [ ] **Log every attempt**: prompt, model, seed, accepted or rejected — this is what turns A-09
      and A-10 into measurements ([15](15-financial-model.md))

## 8. Production order

1. IMG-1, in a fresh ChatGPT conversation, with the Identity Block
2. IMG-2 — "same house as the previous image" — locks the material palette
3. IMG-3 → IMG-8, same thread, correcting drift rather than restarting
4. Cull hard. Expect to discard a lot
5. SEG-1 to SEG-4 with IMG-1 as reference
6. Assemble, single LUT, add a hook
7. `tools/template_motion.py` for the stills-derived package cuts
