# 26 — Art Direction: see like a commercial AD, director and photographer

Researched 2026-10-08. The layer above the shot: **one idea, one world, one colour arc, one composition plan per ad.** Execution lives in 05 (light/lens), 06 (ban list), `image-direction.md` (recipes), 17 (stills factory, judge). Inferences are marked **[inf]**.
Source limits: real treatments are confidential, so §1 uses directors walking through their own (one next to the finished spot [T2]) plus guides; Behance mostly lists treatment-design *services*; YouTube hit HTTP 429 after 4 transcripts, so some quotes come via search snippets.

## 0. The ten rules

1. **One thesis per ad, one idea per frame.** In [T2], "clean air is volume and space" led to "no paintings, no rugs, no nothing, just empty space". Every later choice follows from it.
2. **Write the world before the shots.** Palette, shape, texture, light logic and a signature device go into a *world bible* (§2). Shots sample that world.
3. **Constraints make style.** Lubezki: "Art is made of constraints. When you don't have any, you go crazy, because everything is possible" [L5]. Write rules and a never-list for every ad.
4. **Colour is a script, not a swatch.** Plan how colour *changes* across the 8 shots (§3), the way Pixar colour scripts map "the emotional beats of a story" [A2].
5. **Compose with contrast and affinity.** More visual contrast means more intensity, more affinity means less [A1]. Ramp contrast up to the reveal and resolve to affinity on the end card (§4).
6. **Every light needs a source you could point to.** Deakins rejects "two shadows from one sun" and a "multitude of colour lights with no justification" [L1].
7. **Pretty is not the goal.** "People confuse pretty with good cinematography." Adding kicker after card after bounce turns a frame into "some piece of confectionery instead of something that's really simple and direct" [L1].
8. **Heroes carry the world, inserts carry one property.** Never ask a frame to do both (§5).
9. **Moodboard frames are evidence, not inputs.** Each frame gets one job, and that job is translated into words (§6; 17 rule 3).
10. **The generic AI look is the average.** Models drift to "shiny, bright, waxy-skin, and over-use of bokeh", partly because averaging tastes is "almost adversarial" to aesthetics [M2]. An opinionated world bible is the counterweight.

## 1. How commercial directors write treatments (and what we steal)

A treatment is a 5–12 page pitch: 5–15 slides and about 3–4 days of work [T3][T6]. It shows the agency *your* version of their script and answers "why you" [T3][T4][T5]. "Visuals should back the director's idea, not the other way around" [T6].

**Consolidated section order** [T1–T7]:

| # | Section | What pros put in it | Our AI equivalent |
|---|---|---|---|
| 1 | Intro/hook | A one-liner, a quote, or a callback to the briefing call [T1] | **Thesis line** (≤15 words) |
| 2 | Brief echo | Restate the objectives for "people who don't read the brief", e.g. the production designer and DP [T2] | Objective, audience, SMP, mandatories |
| 3 | Story/beats | A plot summary. Add a storyboard only if the client "isn't very visual" [T1][T2] | 8-shot beat sheet |
| 4 | Casting | Archetypes, "bare minimum" backstory, voice type for VO [T1][T2] | Character card plus one behaviour |
| 5 | Visual style/camera | Light mood, colour, camera movement *and why* [T1][T5] | World bible (§2) plus camera rule |
| 6 | Art direction/sets | What the place says about the character. Details that "show, not tell" [T1] | Set plus signature device |
| 7 | Wardrobe | The brief's wardrobe, plus the director's own preferences and exclusions [T2] | Palette-locked wardrobe |
| 8 | Sound | Planned from the start. Opening without music means it "doesn't immediately scream commercial" [T2] | 13-elevenlabs plan |
| 9 | Edit/post | Quick cuts, match cuts, grade. Often a single linked pacing reference instead of prose [T1][T2] | Rhythm line plus graphic matches (§4.4) |
| 10 | References | Frames "cinematic, yet ultimately feel like you" [T4], with how we differ [T2] | Moodboard with jobs (§6) |
| 11 | Gear/outro | Format and lenses, and how they make the look [T3] | Model choice (`model-router.md`) |

**Lessons from one real treatment against the finished spot** (Samsung AC [T2]):
- **Camera follows the thesis.** Minimalism meant "no sliders, dollies or gimbals ... static locked-off shots", because "directing is ... taking conscious decisions and knowing what kind of effect that decision is going to make." For AI, "locked-off" means the composition is still while micro-breath stays in (06) [inf].
- **When the camera is still, light carries the story.** "When it's super hot the lighting is all bright and orange, but when it's nice and cool it's all soft and dim and airy." That is a two-state colour script.
- **The signature device came from the product.** The walls were "perforated to echo the AC units with 23,000 micro dots", and the client "really loved" it. **This is the most transferable move: lift one physical feature of the product and make it the world's texture.**
- **Say what you won't do.** The client wanted neon. The director answered with "super saturated neon colours but with soft lighting and no neon tubes in the frame."
- **Show the tone, don't just name it.** References and prose must both match the stated tone [T4][T5][T7]. Use **3 tone words plus 3 anti-words**, e.g. "tactile, sun-struck, wry; NOT glossy, epic, cute" [inf].

## 2. Building a visual world: the world bible

Art direction is subtraction plus repetition: pick a few elements and repeat them until they become a language [inf].

**2.1 Palette discipline**
- **Structure:** dominant ≈60% of the frame area, secondary ≈30%, dark ≈10%, plus **one accent reserved for meaning**. The accent usually marks the product or the payoff and appears nowhere else [inf, 60-30-10 heuristic].
- **Production designers police the palette.** On *The Day the Earth Stood Still*, one red tomato in a stadium got questioned: "We don't do red!" An earlier film's rule was "no brown!" The spread was fixed only after "ten or fifteen rounds" [A3].
- **Rare colours carry meaning.** *The Last Jedi* used red "very sparingly ... a very specific application", until the Crait battlefield [A3]. A USC designer works with few colours "so that when a new or more vibrant colour appears, it amplifies a certain emotional beat" [A3]. That is the accent rule.
- **Write colours as materials** ("oxblood lacquer, bone-white plaster, smoked oak"). Models render materials better than hex codes. Keep hex for the grade and the end card [inf].

**2.2 Shape language**
- Pick one dominant basic shape and one opposing shape for the turn. Block's basic shapes are the circle, square and triangle [A1].
- Common readings: the circle is soft and whole, the square stable and institutional, the triangle or diagonal dynamic and tense [A1 summaries; verify].
- Derive the shape from the product silhouette: a can gives circles, a tall bottle verticals, a sneaker wedges [inf].
- Echo the shape in props, set openings, gobo shadows and the type lockup.
- Shape is part of the colour script. Romano's *Incredibles* script used "abstract geometric shapes" [A2].

**2.3 Texture**
- Choose **two contrasting textures**, e.g. matte plaster vs wet glass, or brushed steel vs raw linen, and name both in every prompt.
- Texture is the cheapest anti-AI cue, because the AI default is "overly soft textures" [M2].
- Campaign devices [A4]: backlit textured plexiglass, controlled spills, scanner-flattened objects, printed backdrops, **incomplete backdrops** ("showing the artifice instead of hiding it"), colour blocking, overheads.

**2.4 Light logic**
- Choose one world light, e.g. "low winter sun through a single west window", and give it a time-of-day arc.
- Lubezki: "different times of the day express different emotions". Light is "like the broth that contains the soup ... it does determine the mood and the atmosphere of a scene more than anything" [L4].
- Inserts may add a *motivated* kicker, never a new sun [L1].

**2.5 Lens family and camera rules**
- Model on the *Tree of Life* dogma [L5]: "backlight for continuity and depth", "negative fill to avoid 'light sandwiches'", "never front light", "avoid white and primary colors in frame", "Z-axis moves instead of pans or tilts", "no zooming", plus an "Article E" exception.
- Deakins: close on 21–27 mm feels intimate, 100 mm from afar observational [L1].

**2.6 Signature device**
- **Definition:** one recurring visual idea that makes the ad ownable.
- **Test:** with the logo cropped out, can you still tell whose ad it is? [inf]
- **Sources:** a product feature as world texture (micro-perforation [T2]); a brand shape reused as framing (can-top circle as sun, porthole, puddle); an accent colour that only touches the product; one recurring action.
- **Frequency:** the device appears in **≥3 of 8 shots** and on the end card.

**2.7 Casting and wardrobe**
- Cast by archetype with only the "bare minimum" backstory [T2].
- Lock wardrobe to the palette: no off-palette garments, no logos, one texture from §2.3.
- Give each character one behaviour ("chews the straw"). In AI images, a behaviour sells realism better than an adjective [inf].

## 3. Colour script (Pixar method → 8-shot ad)

**What it is**
- A row of small abstract thumbnails, made early. Their purpose is "mostly the emotional tone of each scene", shown in "pure abstract shapes and colour". Romano likens reading one to reading sheet music [A2].
- **Origin:** Eggleston drew the first for *Toy Story* in chalk pastel on long strips of black paper. Lasseter: colours "intensified with the emotions and turned muted during somber moments". Pixar has made one for every film since [A2].
- *Toy Story*'s pastels go "bleak and muddy when something sinister occurs"; *Up*'s opening runs "beat by emotional beat" with no dialogue [A2].

**Making one for an ad [inf]:**
1. Write each shot's **emotional beat** in one word (friction, friction, curiosity, contact, release, delight, pride, sign-off).
2. Give each beat four values:
   - **dominant hue**
   - **value key** (low/mid/high)
   - **saturation** (1–5)
   - **temperature**
3. Apply three rules:
   - **The turn gets the colour shift:** the cut from problem to solution flips hue or temperature, as in [T2]'s hot orange → cool airy.
   - **Saturation peaks at the payoff** (S6–S7). The accent appears at full strength first on the reveal.
   - **The end card returns to the brand palette at mid key** (affinity).
4. Make the **strip**: 8 flat colour blocks plus the main silhouette. Generate it cheaply (Z-Image Turbo, 17 §1: "flat abstract colour study, no detail, [shape] silhouette, [hue/key]") or draw it in code. Approve it *before* any hero generation.
5. **Grayscale check:** desaturated, the strip must still show the arc in value alone.

**Row template:** `S3 | curiosity | teal-grey dominant, amber accent 5% | mid-low key | sat 2 | cool | circle top-right`

## 4. Composition with Bruce Block's *The Visual Story*

**Framework** [A1]
- Seven basic components: **space, line, shape, tone, colour, movement, rhythm**.
- Each component is pushed toward **contrast** (difference, more visual intensity) or **affinity** (similarity, less).
- By controlling these, the picture-maker "stirs an audience's emotions, creates a visual style and gives structure and unity".
- The practice: **graph the story's intensity, then shape visual intensity to match it.**

**4.1 Components as ad decisions** [Block's categories; ad mappings are inf]

| Component | Contrast (raise) | Affinity (calm) | Ad use |
|---|---|---|---|
| **Space** | Deep against flat. Pushed depth cues (overlap, size change, haze, focus falloff) | One space type. Block's four: **deep, flat, limited, ambiguous** | Problem in limited/ambiguous space. Reveal in deep space. End card flat (it's a graphic) |
| **Line** | Diagonals against verticals | All horizontal (calm) or all vertical (formal) | Product verticals against a diagonal action at the turn |
| **Shape** | Circle against triangle | One shape family | §2.2. The shape match becomes the graphic match |
| **Tone** | Wide brightness range, hard falloff | Narrow range | Low-key problem, high-key payoff (or inverse for luxury) |
| **Colour** | Complementary, warm vs cool, saturated vs grey | Analogous, matched saturation | Follows the colour script (§3) |
| **Movement** | Opposed screen directions, still against fast | Same direction and speed | Hold screen direction until the turn, then reverse [inf] |
| **Rhythm** | Irregular cut lengths, accents | Even tempo | Even 1.5 s setup, staccato turn, held final beat |

**Point of attention.** Know where the eye ends in shot N. Start N+1's subject in the same zone for a smooth cut (affinity), or the opposite zone for a jolt (contrast) [A1 concept; inf]. In 9:16 this matters more, because the eye mostly travels vertically [inf].

**4.2 Intensity graph (8 shots, 15–20 s) [inf]**
- **Curve:** `S1 4 · S2 5 · S3 6 · S4 7 · S5 9 (turn) · S6 10 (reveal) · S7 6 · S8 3 (end card)`.
- **High shots:** a shot rated 9–10 needs contrast on **≥3 components**.
- **Low shots:** a shot rated ≤4 is mostly affinity.
- **Hook exception:** S1 still has to stop the scroll. Give it **one** strong contrast (tone or scale) inside an otherwise calm frame (03).

**4.3 Negative space for type**
- Fix the type zone *before* composing. A headline printed over a busy photo competes with it [M4].
- Describe the zone physically: "the upper third is an empty, evenly lit [colour] plaster wall with nothing on it". Don't write "copy space": models ignore layout jargon but obey described emptiness [inf; cf. 17 §4.5].
- Point the product's eye-trace at the zone (a gaze, a diagonal, a pour).
- Respect platform safe zones (03).
- The end card is flat space: a frontal plane, no converging lines, one tone.

**4.4 Graphic matches**
- **Definition:** a cut where the "shapes, colours, or overall movement" of two shots line up. Classic examples are *2001*'s bone → satellite and the opening of *Citizen Kane* [M3].
- **Why it matters for AI:** clips are generated in isolation, so cuts "feel assembled". A repeated shape or colour carries continuity across them [M3, vendor claim, plausible].
- **How many:** plan 1–2 per ad, built from the signature device (can top → sun disc, ice-cube edge → building edge).
- **Execution:** generate S(N) first. Build S(N+1)'s start frame from a layout map that keeps S(N)'s last silhouette position, scale and tone, and change everything else (17 §4.5).

## 5. Light and the one idea: how masters decide

**Deakins** [L1][L2][L3]
- Feeling comes before light. "You don't ever want to go on a location scout thinking first primarily 'where's the light coming from'... that's death." Ask what the audience should feel.
- "My lighting's really minimal"; he'd give up lighting before framing [L2]; light "as though somebody sitting in a room by a lamp is being lit by that lamp" [L3].
- Justify the light on screen: "within the scene somewhere... see that practical or see the window to know the justification for the light" [L1].
- **One idea:** the best stills "strip away all the things ... on the periphery and concentrate on that one little image that says more than you would if you showed it in a big wide shot". And: "you shouldn't love a shot ... it should all be part of a whole" [L1].

**Lubezki** [L4][L5][L6]
- He scouts at different hours, because places "make you feel sad... lonely... joyful".
- He uses wide lenses even in close-ups, so "you still feel the light changes ... the wind and the cold" [L4].
- He uses backlight with negative fill. "We want the blacks; we don't like milky images" [L5].
- "Instead of bringing in lights, we would rewrite the scene and reassemble it outside" [L6]. *For us:* when a prompt fights its light, re-stage (move the subject to the window) rather than adding light words [inf].

**Still-life photographers**
- **Carl Kleiner** builds one graphic idea in camera. He rigs "in order to only show what I want to show", uses two-centimetre mirrors to place single highlights, and makes "as much as possible in camera". [P1]. *For us:* write one placed highlight instead of generic "studio lighting" [inf].
- **Jonathan Mauloubier** first works out "what needs to be depicted". He tests light "to reveal the essence of the subjects", and holds that "it is definitely the stage that does it" [P2]. Set first.
- **Henry Leutwyler:** still life "doesn't run away... so you better know what you're doing". [P3]. Plan fully, don't over-iterate.
- **Jonathan Knowles** is about "slicing and isolating the subject matter" [P4], which is the logic of the insert.
- **TikTok product shooters** [P5]: two lights (product + separate backdrop light); "light the product, not the room"

**5.1 The one-idea test (per frame)**
- Write the frame as **subject + one property + one feeling**: "the bottle's frost feels dangerous-cold". If you need "and" twice, split it into two frames [inf].
- The sharpest area, the brightest area and the accent colour must all land on the idea. Tone and colour contrast pull the eye first; a saturated yellow "will always attract a viewer's eye first" [A1].

**5.2 Hero vs insert [inf, from 05 production practice plus the sources above]**

| | **Hero** | **Insert** |
|---|---|---|
| Job | Establish the world plus product identity | Prove one property (texture, mechanism, cold, crunch) |
| Space | Deep, with the world light visible (window, sun, practical) | Limited or flat. The world light is implied only by its colour |
| Composition | Product at 30–55% of frame height, type zone reserved, device in frame | The property fills the frame. The product edge may be cropped |
| Light | World light plus one motivated accent | One placed highlight or backlight that reveals the property |
| Intensity | Peak or resolution | Rising action. Contrast on 1–2 components |
| Count per 8 shots | 2 (reveal and end) | 4–5 |
| Duration | 1.5–3 s | 0.4–1.2 s |
| Pipeline | Product-exact path (17) | Plate/texture path. The label need not be legible |

## 6. Moodboards and lookbooks → prompt blocks

**Where to find references**
- **ShotDeck:** DP Lawrence Sher's tagged library of 1.4M+ film stills (framing, lighting, colour, lens) [M1].
- **FrameSet:** commercials and music videos, searchable by colour and lighting [T1].
- **Pinterest** [T2], **FilmGrab** [T4], Behance and muz.li for trends [T6], and art-direction newsletters [A4].
- **Never moodboard with AI images.** They feed the average back in [inf; M2].

**Deconstruct the board; don't paste it into the prompt**
1. Use 12–20 frames, each tagged with **one job**: light, palette, composition, texture, casting, set or device. Cut any frame without a job.
2. Write one sentence of physical fact per frame:
   - "low sun from frame-left, hard, warm; long shadows; face in shade, rim on hair"
   - "70% flat sage wall; subject small lower right"
   - "1–2 mm condensation beads on brushed steel, one drip track"
3. Merge the sentences by job into the world bible. That merged text *is* the lookbook.
4. Feed images to the model **only for identity** (product, character), with a stated job and "DISCARD its lighting/background" (17 rules 3–4). Mood frames are for humans.
5. Add 2–3 **anti-references**, usually the category cliché (perfume on black with gold sparkles). Their traits become the anti-words and the never-list.

**Escaping the generic AI aesthetic** (adds to 06)

The default look comes from aesthetic scorers "highly biased towards ... blurry backgrounds, overly soft textures, and bright images" [M2]. BFL pitches FLUX.1 Krea as escaping "the oversaturated 'AI look'" [M2]. Counter-moves [inf]:
- **Commit to a key:** low or high, never "balanced bright".
- **Compose in depth** [L5]: use bokeh only when the one-idea test needs isolation.
- **Use asymmetry and cropping:** props cut by the frame edge, and a layout map to place the subject off-centre.
- **Keep one discord:** AI harmonises every colour, while real art direction keeps one accent.
- **Delete stock adjectives** ("cinematic, 8K, hyper-realistic, stunning, epic"). Replace each with a physical fact.
- **Show the artifice deliberately** where the brand allows it (incomplete backdrop, visible rig edge) [A4]. Deliberate construction reads as human authorship.

## 7. The Art Director Protocol (run for every ad)

**Step 0: Inputs.** Brief, product sheet (17 step 1), platform (03), concept (15).

**Step 1: One-page mini-treatment**
```
THESIS: <≤15 words, the visual metaphor>
SMP: <one benefit>   AUDIENCE: <who, and their mood while scrolling>
TONE: <3 words>   NOT: <3 anti-words>
CAMERA PHILOSOPHY: <one rule + why, e.g. "locked frames, life moves inside them">
EDIT RHYTHM: <e.g. "even 1.5s setup, staccato turn 0.4–0.6s, held 2.5s end">
SOUND IDEA: <e.g. "no music until the reveal; ambience only">
REFERENCES: <3 frames with jobs + 1 anti-reference>
```

**Step 2: World bible** (fill it in, then freeze it)
```
PALETTE: dominant <material+colour> 60 | secondary 30 | dark 10 | ACCENT <colour> = product/payoff only
BANNED: <e.g. no pure white, no neon tubes in frame, no gold glitter>
SHAPE: dominant <family, from product> vs opposing <shape for the turn>
TEXTURES: <A> vs <B>
WORLD LIGHT: <one source, direction, time of day; arc across the ad>
LENS/CAMERA: <e.g. 24–35mm close for people, 90–100mm macro inserts; movement rule>
SIGNATURE DEVICE: <what; which shots (≥3); how it sits on the end card>
CASTING/WARDROBE: <archetype, one behaviour, palette-locked wardrobe>
NEVER LIST: <5 items>
```

**Step 3: Colour script.** Write 8 rows (§3), make the thumbnail strip, run the grayscale check, approve.

**Step 4: Composition plan.** One row per shot:

| Shot | Beat | Hero/insert | Intensity | Space | Line | Shape | Tone key | Colour | Eye-trace in → out | Type zone | Device | Graphic match |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Checks: the number of contrasting components matches intensity (§4.2); eye-trace out of S(N) is planned against eye-trace into S(N+1); 1–2 graphic matches; the device appears in ≥3 rows.

**Step 5: Style block.** Paste it verbatim into every image prompt, after the shot content and before the preserve block (17).
```
WORLD: <dominant material+colour> world with <secondary>; <dark> shadows; the only <ACCENT> in frame is on the product.
SHAPE: <shape> forms echoed in <props/set/shadows>.
TEXTURE: <A> against <B>, visible at full resolution.
LIGHT: single <world source, direction, quality, colour temp>, motivated and visible as <window/practical/sun edge>; negative fill on the shadow side; one placed highlight on <property>. No second sun, no unmotivated coloured light.
LENS: <focal length, distance, deep focus or shallow on <x>>.
GRADE: <low/high key>, <saturation>, true blacks, no milky shadows, fine grain.
AVOID: <anti-words>, <never list>, waxy skin, generic bokeh, symmetrical stock composition.
```
Keep it ≤90 words so it doesn't drown the shot content (17 §4.1). Adapt the syntax per model (`image-direction.md` §4).

**Step 6: Generate** via the stills factory (17 §2), in this order: heroes, then inserts, then the end card.

**Step 7: Review** with §8 first, then the 17 §5 judge.

## 8. Review checklist

**Contact sheet: all 8 frames side by side at thumbnail size**
- [ ] **Squint:** rhythm matches the approved script; the turn reads as a shift.
- [ ] **Grayscale:** arc still reads; product is the highest-contrast point in each hero.
- [ ] **Palette police:** no off-palette colour; accent only on product/payoff.
- [ ] **Device:** ≥3 frames plus end card; identifiable with the logo cropped.
- [ ] **Shape:** dominant family repeats; opposing shape only at the turn.
- [ ] **Light:** every frame passes "point to the source". No double shadows, no unmotivated rims or gels [L1].
- [ ] **Intensity:** contrast counts follow §4.2; no flat middle, no adjacent equal frames unless a deliberate hold.
- [ ] **Eye-trace:** at speed, the eye lands where the next frame expects it (except planned jolts).
- [ ] **Graphic match:** position, scale and tone align when overlaid at 50%.
- [ ] **Balance:** 2 heroes, 4–5 inserts, 1 end card.

**Per frame**
- [ ] One-idea sentence written; sharpest, brightest and accent coincide on it.
- [ ] Type zone clean; product points into it.
- [ ] **Anti-AI:** no waxy skin, bokeh soup, all-harmonised palette or centred stock pose; real texture at 100%; 06 ban list.
- [ ] **Deakins test:** remove anything there only because it's "pretty" [L1].
- [ ] Both named textures read correctly (17 rule 7). Then run the 17 §5 gates and the pairwise judge.

**Fix order [inf]:** idea → staging/composition → light logic → palette → texture → finish. Never fix a composition with grade words.

## 9. Worked mini-example (fictional "KOLD" canned cold brew, 9:16, 15 s)

- **Thesis:** "Inside the can it's always 6 a.m. in winter."
- **Tone:** crisp, hushed, wry. **NOT:** glossy, energetic, cosy.
- **Palette:** frost-blue plaster 60, raw concrete grey 30, espresso-black 10. Accent is copper, used only on the ring-pull and logo.
- **Shape:** circles (can top, ring-pull) against one diagonal (the pour) at the turn.
- **Textures:** hoar-frost crystals against matte concrete.
- **Light:** low blue dawn through one high round window, arcing to a copper sunrise edge at the reveal.
- **Device:** the ring-pull circle recurs as the window, a frost ring on the counter, and the end-card logo holder.
- **Script:**
  - S1 hook: frost-bloom macro (insert, 4, ambiguous space, cool, saturation 1).
  - S5 turn: the ring-pull cracks, diagonal spray (insert, 9; contrast on line, tone and movement).
  - S6 reveal: the can in deep space, window circle behind, first copper rim (hero, 10, saturation 4).
  - Graphic match: can top → window circle.
  - S8 end card: flat frost-blue plane, copper logo, type zone in the upper third (3).

## Sources

- [T1] Nur Niaz, "How To Write Better Commercial Treatments" (transcript): https://youtu.be/IYqJ20UnMQw
- [T2] Nur Niaz, "Samsung Commercial: Director's Treatment vs. End Result" (transcript; treatment PDF in description): https://youtu.be/COBIBIJU8HU
- [T3] No Film School: https://nofilmschool.com/commercial-treatment
- [T4] Assemble: https://www.onassemble.com/blog/how-to-write-a-winning-directors-treatment
- [T5] Robin Piree: https://robinpiree.com/blog/how-to-write-a-directors-treatment-for-a-tv-commercial
- [T6] Readymag / Anastasia Mokhan (Snapchat treatment): https://blog.readymag.com/how-to-jump-start-into-directors-treatments-insider-shares-the-desired-skills-tools-fddab816fc35/
- [T7] PremiumBeat: https://www.premiumbeat.com/blog/tips-write-better-commercial-treatments/
- [A1] Bruce Block, *The Visual Story*, 3rd ed., Routledge 2020. Read via the publisher listing (https://shop.elsevier.com/books/the-visual-story/block/978-0-08-052073-5), the O'Reilly ch. 2–3 previews (paywalled; titles and snippets only) and student applications (https://blogs.bgsu.edu/srohen/?p=200, https://blogs.bgsu.edu/jamstew/?p=80). Shape-emotion readings come from unofficial summaries.
- [A2] Hyperallergic on *The Art of Pixar*: https://hyperallergic.com/610771/the-art-of-pixar-chronicle-books/ ; MoMA "Pixar: 20 Years of Animation" audio guide (via search snippet, page returned 403): https://www.moma.org/audio/playlist/192/2575
- [A3] Palette rules (via search summaries): https://www.comingsoon.net/?p=532006 ; https://theasc.com/article/the-last-jedi-production-design/ ; https://worldbuilding.usc.edu/?p=899
- [A4] Art Direction newsletter: https://artdirection.substack.com/p/simple-art-direction-techniques-to
- [L1] AlterCine, Deakins compilation (transcript): https://youtu.be/p6zWyxNrHO0
- [L2] Filmhounds 2026, Roger & James Deakins: https://filmhounds.co.uk/2026/02/17/roger-deakins-and-james-ellis-deakins-chat-reflections-on-cinematography-cinema-is-not-literal/
- [L3] NPR 2009 (via search snippet; page returned 503): https://www.npr.org/2009/10/29/114249616/roger-deakins-keeping-an-eye-on-the-small-things
- [L4] Gold Derby, Lubezki on *The Revenant* (transcript): https://youtu.be/Im8MaR6R0u8
- [L5] Filmdetail, *Tree of Life* dogma and AC quotes: https://filmdetail.com/tag/emmanuel-lubezki/
- [L6] PremiumBeat on Lubezki: https://www.premiumbeat.com/blog/cinematography-insights-emmanuel-lubezki/
- [P1] It's Nice That, Carl Kleiner: https://www.itsnicethat.com/features/carl-kleiner-on-the-tools-behind-the-perfect-image-arjowiggins-tooled-up-300316
- [P2] Cherrydeck, Jonathan Mauloubier: https://cherrydeck.com/blog/material-matters-exploring-still-life-photography-with-jonathan-mauloubier/
- [P3] Graphis, Henry Leutwyler (via search snippet): https://blog.graphis.com/things-have-a-soul-henry-leutwyler-featured-in-graphis-journal-375/
- [P4] Cherrydeck, Jonathan Knowles: https://cherrydeck.com/blog/jonathan-knowles-stilllife-photographer/
- [P5] TikTok discover summaries. Individual posts were not opened, because the page exposes no video IDs without JavaScript: https://www.tiktok.com/discover/how-to-set-up-lighting-for-product-photography
- [M1] ShotDeck / Lawrence Sher: https://broadcastbeat.com/news/shotdeck-and-canva-introduce-integration-to-empower-filmmakers-and-creatives-to-bring-their-vision-to-life-2
- [M2] Breunig, "The rise of opinionated models": https://www.dbreunig.com/2025/08/04/the-rise-of-opinionated-models.html ; Krea: https://www.krea.ai/blog/new-krea ; BFL: https://bfl.ai/blog/flux-1-krea-dev
- [M3] https://en.wikipedia.org/wiki/Match_cut ; https://www.studiobinder.com/blog/match-cuts-creative-transitions-examples/ ; InVideo FAQ (vendor): https://invideo.io/faq/what-are-graphic-matches-in-video-ads-and-how-do-they/
- [M4] Ad layout basics (overprinting): https://www.slideshare.net/slideshow/creative-execution/189556
