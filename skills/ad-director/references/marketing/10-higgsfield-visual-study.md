# 10 — Higgsfield Visual Study (frame-level)

Source: public Higgsfield pages fetched 2026-10-07 (`/seedance-2-5-community`, `/kling-30-community`, `/commercial`, `/motion/*`, `/ai-marketing-video-maker`, `/ai-brand-video-generator`, `/ai-product-video-generator`, `/marketing-studio-intro`). 29 clips were downloaded, cut into 8-frame 4x2 contact sheets, inspected, then deleted. The sheets are in `research/ai-video-reels/youtube/frames/higgsfield/<slug>.jpg` (git-ignored). Prompt text is quoted only as reference data. Several showcase clips carry real brand marks (IWC, Range Rover, NASCAR/Pirelli). Treat these as a legal warning: never generate real trademarks.

Hosts: community clips are on `d8j0ntlcm91z4.cloudfront.net`, presets on `cdn.higgsfield.ai/*_motion/` and `static.higgsfield.ai`, marketing clips on `a.storyblok.com`, and projects are HLS on `cdn.higgsfield.ai/hls/`.

## Per-video notes

### A. Product commercials (prompt visible)

1. **sippo**: Seedance 2.5, 30s, 1080p (`..._23e78b00..._wm3.mp4`). The prompt is a full ad treatment: SCENE CONTEXT, ACTIVE REFERENCE (product image as "source of truth": "remains a carton and never becomes a can"), CHARACTERS, FIRST FRAME ("carton in extreme foreground… no delayed product reveal"), FORMAT MODE (hard, match and whip cuts), per-shot lens spec ("107° wide rectilinear, camera 60 cm above table, 70 cm from product… no fisheye bubble"). *Seen:* the carton is foreground-dominant in frame 1, a 4-women top-down "flower" formation, a fingernail macro on the carton flap, and a hero packshot on a black plinth with a real cherry. One colour world (cherry/powder pink) runs through everything. *Real:* the macro on the matte carton fibre and natural skin. *AI tells:* the corridor symmetry is too perfect and the label typography softens in wide shots.
2. **lipserum** ("Bounce" lip serum): Seedance 2.5, 30s. The structure is an ad inside the ad. It opens looking up through a transparent acrylic surface with four faces looking down while serum is "drawn" on the glass. Then a BTS studio wide, a beauty ECU of the lips, a phone-review moment and a CG-like packshot (chrome spheres, bubbles). *Lesson:* the live-action parts read as real, while the final packshot reads as 3D render. Keep the end card on a physical set.
3. **cruncho** (chips): Seedance 2.5, 30s. Mixes practical miniatures (tilt-shift toy convenience store and street), a macro of chips and onion rings floating in clouds, a 2D anime-shout insert and a clean beige hero shot. The prompt explicitly asks for "the glossy bag compresses naturally, then regains its inflated shape" and "plastic stretches, wrinkles… crisp foil". *Lesson:* mixing media hides AI. The viewer reads the toy world as a deliberate style, not as an error.
4. **mkt-productad** ("BITE" bar, product-video page hero): a 2.39-ish wide-angle bathroom, a superhero transformation gag and a macro of a hand tearing the wrapper with lips on the bar. It has a 35mm, teal-orange grade with a visible halation glow. A kaiju in the window keeps it comedic. The lip/bar macro is the most real-looking frame.
5. **ms-product** ("BIOJUSS" gel, Marketing Studio hero): seamless white cyc with hand-held bottle tilts toward the lens and condensation beads. Full-frame liquid bubbles carry the logo, then swatch-on-cheek and two-model handoff shots. Clean K-beauty language. It looks real because hands occlude the product and the bottle has fingerprints and droplets. The sterile white is the generic part.
6. **ms-ads** ("FIZZO" can): a static banner-style motion graphic, included as a counter-example.
7. **divewatch** (marketing-video-maker). Prompt: *"Premium dive-watch ad where the case bursts into floating layered components and reassembles, soft studio light, minimalist background."* Pale blue-grey sweep, one hard-edged window shadow across the set, exploded view with **cast shadows of every part on the backdrop**, a macro of the bezel and a reassembled hero shot. Small tracking-wide supers ("DEPTH MADE", "EVERY LAYER", "MADE TO HOLD"). *This is the most premium-looking product clip.* The real shadow makes the floating parts believable, and the grade is cool and desaturated rather than glossy. (Shows an IWC logo, which is an IP problem.)
8. **chip-macro** ("SNAPI"). Prompt: *"Extreme macro of ridged potato chip with salt grains… floating dill, onions, milk splashes. Fast cuts, spinning vortex…"* The salt-grain macro is excellent. The sour-cream swoosh has a cyan CG motion trail and the floating bag is plastic CGI. *Lesson:* real-world macro texture looks real, while VFX trails and floating packs look like 3D.
9. **tonic-can** ("fizzi"). Prompt: pool party, golden hour, *"finger pops tab with steam puff, low-angle toast from inflatable floats…"* The half-underwater split-level shot of the pool, the condensation on the can, the shallow-DOF string-light bokeh and the POV hand holding the can to camera all read as real. The animated glowing fruit tiles on the can betray AI. The supers sit cleanly in the lower third.
10. **moto-rain** (brand page). Prompt: *"Cinematic motorcycle ad, 15s, photoreal, light rain throughout… tight detail of the front wheel fanning water… Cool overcast wet look, mirror-like reflections, mist, desaturated."* Brake-caliper and exhaust macros with water beads, a helmet-off close-up, and a final tiny figure on a vast wet runway. *Real:* the flat overcast light, low contrast and wet reflections. *AI tells:* a slightly waxy face and an over-symmetric final wide.
11. **fishing-rod** (brand page): "sturdy hero rod bent under huge load but never breaking", a breaching shark, sun-flare backlight and a reel macro. It reads as a well-made spec spot. The shark is the giveaway, with a uniform foam texture.

### B. Product-adjacent realism (single-subject macro)

12. **watch-macro**: Kling 3.0, 6s. Prompt: *"vintage wristwatch held between two fingers… fine dust particles, micro scratches on the glass, worn metal edges… patina… single warm key light grazing the surface… skin texture of the fingers visible at the edges, slightly out of focus… soft film grain, precise focus breathing."* The sheet shows a slow push from hand-held to a dial macro, with dust, scratches and lume patina all visible. **Nearly indistinguishable from a real insert.** Imperfection is the subject.
13. **kling-macro** (turntable): Kling 3.0. Prompt: static, then a *"fast, rigid robot-bolt push-in… No easing… camera locks onto the needle tip, as if physically bolted to it."* Warm analog room with guitars and tube amp, then an orange cartridge macro with groove texture. A rigid mechanical move plus a locked macro gives a premium tech/craft feel.
14. **tattoo-macro**: Kling 3.0, 2.39:1. Black-gloved hands, arm hair, ink and plasma droplets, warm backlight with heavy foreground blur. Real because of **dirt, fluids and hair**.

### C. Cinematic realism (no product)

15. **korean-lux**: Seedance 2.5, 15s. Prompt: *"Early-2000s consumer DV camcorder… restrained handheld, imperfect horizon, soft focus, brief autofocus hunting, lens breathing, mild exposure pumping… clipped sea highlights, uneven white balance… No stabilization, gimbal, cinematic movement… Exactly five observational shots joined by four hard cuts, one action per shot with pauses."* Location: "lived-in and local rather than touristic… no readable brands". **This is the most photoreal clip in the set.** It looks like a 2003 Korean indie film. The realism comes from *removing* cinema polish.
16. **panavision-walk**: Seedance 2.5, 8s. A Brooklyn brownstone walk with a kraft grocery bag. Prompt: *"Panavision DXL2… C/G/T-series anamorphic primes… slight edge distortion, oval bokeh… no flares… subtle film grain"*, "No zoom: focal length fixed, prime lens", negative locks ("no cuts, horizon always level, does not drop anything, no second character"). Dappled light and natural gait make it read as a real fashion or retail spot.
17. **foodcourt**: Seedance 2.5, 30s. A woman eating spicy noodles, lit from below by an unseen phone, with fluorescent-tube bokeh. The prompt micro-directs the eyes ("pupils constantly move… frequent and natural blinking"). It ends on an empty, stained bowl with chopsticks. Great food-ad energy: **messy, greedy, un-styled**.
18. **ramen**: Seedance 2.5, 30s, 4:3. "Not a tourist spot… many-times-washed denim apron… natural facial asymmetry." Shows a knife on a scarred board, the pot pour and the green-onion garnish. It reads as documentary food B-roll, with yellow-green fluorescent cast left uncorrected.
19-21. **pov-bus / ecu-woman / rain-cigarette** (Seedance, Kling): the POV bus flirt has natural head-sway but glossy beauty skin. The snorricam scream is sold by sweat and performance. The 6-shot motorcycle action has a blue-steel grade with one warm lighter flame.
22. **sedan70s**: Kling 3.0, 4 shots: profile in car, rear-view mirror, gear knob, grille to a "HIGGS" plate. Warm bleached-sun 70s stock and haze. A car-ad structure built from **details (mirror, knob, plate)** instead of a 360 spin.
23. **wheel-rig**: Kling 3.0, a suction-cup rig on the wheel at night and a side-door rig. Real grip language ("rig grip… hard-mounted") produces credible vibration.

### D. Higgsfield presets (no prompt; preset name only)

24. **Road Rush** (Minimax): black luxury SUV, autumn forest, low tracking, ending on a wheel spraying leaves. Strong but generic "stock car ad".
25. **Robo Arm**: a fast robotic orbit at a ramen counter, wide-lens distortion, 90s-film colour.
26. **3D Rotation**: a B&W studio 360 of a model on a stool, in a fashion-editorial style.
27. **Lazy Susan**: a low-angle orbit with sun flare in the desert.
28. **Plate Check**: fisheye at table height, burger foreground, warm tungsten, a UGC look.
29. **Outfit Check**: iPhone-look Paris street style ending on a handbag close-up. It reads as real thanks to overcast light and phone optics.

## Cross-cutting lessons

1. **Prompts are treatments, not sentences.** The best clips (sippo, cruncho, lipserum, korean-lux, ramen) use labelled blocks: SCENE CONTEXT, ACTIVE REFERENCES, CHARACTERS, LOCATION, FIRST FRAME, FORMAT MODE, ACTION/CAMERA per beat, SOUND, NEGATIVE LOCKS.
2. **The product image is declared the "source of truth"**, with explicit material and shape invariants ("never becomes a can").
3. **Frame 1 must already contain the product.** There is no empty establishing shot.
4. **Realism comes from subtracting polish:** DV camcorder, autofocus hunting, exposure pumping, uneven white balance, clipped highlights, imperfect horizon, uncorrected fluorescent cast. The most photoreal clip is the least "cinematic".
5. **Imperfection is the subject in macro:** dust, micro-scratches, patina, fingerprints, condensation, salt grains, ink droplets, arm hair.
6. **Hands occlude the product.** Fingers, nails and skin at the frame edge give scale and kill the floating-render look.
7. **Physical shadows anchor floating objects** (divewatch). If something levitates, give it a cast shadow on a real backdrop.
8. **Lighting is motivated and single-source:** a grazing warm key, a window-shadow slash, a phone glow from below, overcast flat light, golden-hour backlight. No three-point beauty dome.
9. **Grades are restrained:** cool desaturated steel (watch, moto), bleached warm 70s (sedan) or one-colour worlds (sippo pink). Avoid high-saturation teal-orange everywhere.
10. **Name real hardware and grip:** Panavision DXL2 + C/G/T anamorphics, fixed prime, suction-cup rig, side-door rig, snorricam, robot-bolt push-in with "no easing".
11. **Mixed media hides AI** (miniatures, 2D inserts). Uncanny output becomes a style choice.
12. **What still looks AI:** CG packshot end cards (spheres, bubbles, floating bags), VFX motion trails, animated labels, waxy beauty skin, perfectly symmetric corridors and wides, soft small type in wide shots, uniform splash and foam.
13. **How this differs from glossy centred AI product shots:** the product is off-centre and foreground-dominant, often partly cut by frame edge or fingers. It sits in a lived-in context (pool, kitchen, food court) rather than on a void with a reflective floor, and the hero shot is the *only* clean, centred frame, earned at the end.

## 20 prompt phrases / visual rules to copy

1. "`@image_1` is the exact product reference and the visual source of truth; preserve proportions, label, materials; it never becomes a [other container]."
2. "The first visible frame already contains the product in the extreme foreground; no empty establishing shot, no delayed reveal."
3. "Single warm key light grazing the surface, revealing micro-scratches, fine dust, fingerprints and patina."
4. "Fingers visible at the frame edge, slightly out of focus, real skin texture, adding scale."
5. "Condensation beads and a few smeared fingerprints on the glass/can; label stays sharp and readable."
6. "Exploded view: every component casts a soft real shadow on the backdrop; one hard window-shadow slash across the set."
7. "Shot on Panavision DXL2 with C-series anamorphic primes, fixed focal length, oval bokeh, slight edge distortion, no flares, subtle film grain."
8. "Camera rigidly bolted to [object], fast mechanical push-in, no easing, then locks at macro distance with only micro-vibration."
9. "Hard-mounted suction-cup rig on the [car/bottle tray]; raw vibration, background streaks, subject perfectly stable."
10. "107° rectilinear wide, camera 60 cm above table, 70 cm from product; straight lines stay straight, no fisheye bubble."
11. "Lived-in and local, not touristic; no readable brands, no resort décor." (Applies to all background signage.)
12. "Uneven white balance, uncorrected fluorescent cast, clipped highlights left clipped."
13. "Restrained handheld at standing height, imperfect horizon, brief autofocus hunting, lens breathing; no gimbal, no cinematic sweep" (for UGC and lifestyle cut-ins).
14. "Exactly N shots joined by N−1 hard cuts, one action per shot, with pauses."
15. "Negative locks: no zoom, no digital punch-in, horizon always level, product never changes shape, no text unless specified."
16. "Natural facial asymmetry, light makeup, real pores; frequent natural blinking; eyes never still."
17. "Packaging compresses naturally under the grip, then regains its shape; crisp foil wrinkle on tear."
18. "One colour world for the whole film: [brand hue], ivory, small chrome accents. Wardrobe and set follow it."
19. "Cool overcast flat light, wet mirror-like reflections, low contrast, desaturated" (premium tech/auto) **or** "bleached warm sun, haze, period film stock" (heritage).
20. "Final hero packshot on a *physical* plinth with one real ingredient beside it (a cherry, a lime), soft shadow, no CG spheres or bubbles; small, wide-tracked supers in a corner."

**Avoid list:** CG chrome spheres and bubbles, VFX swoosh trails, animated label graphics, floating bag on gradient, waxy beauty skin, mirror-symmetric wides, real brand logos (IWC, Range Rover and NASCAR appear in Higgsfield's own showcase; we must not copy that).
