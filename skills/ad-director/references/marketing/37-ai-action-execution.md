# 37 — Executing action and product beats with AI video (punchline ads in one take)

Researched 2026-10-08. This file covers how to **execute** story beats: a hand opens a can, liquid pours, a character drinks, someone jumps, and the joke lands. It assumes 12 (Higgsfield API and prices), 16 (seamless flow and hidden cuts), 11-niche-food-drink (liquids), 08 (post), 13 (ElevenLabs) and `../mascot/OTTO.md`, and does not repeat them.

Our own inferences are tagged **[inf]**. Internal refs read "16 §2.5" (section) or "07 l.44" (line number in that file). Prices are list USD from 12 §1 (before the 15 % Kling discount). We spent no money.

**Research limits.** YouTube returned HTTP 429 on the first transcript request (`SdtaDI8plF4`), so we stopped as instructed. The fight and action tutorials we found are listed in §6 by title only, and nothing in this file quotes them. Most web sources on Seedance 2.5 and Kling 3.0 prompting are third-party blogs, not ByteDance or Kuaishou docs. Treat them as community practice.

---

## 0. The ten execution rules

1. **Every product interaction runs from a start frame to an end frame.** Nothing is text-only. The hand, the can and the label are drawn correctly in a Flare still before any motion exists (12, 16 §1B).
2. **One beat per clip: one action and one camera move.** Each extra hand, liquid or camera event is another failure point, and the risks compound [E1][F1].
3. **Never show liquid volume transfer.** All three top models failed a simple pour test in Sep 2026, and Kling "created water from nowhere" [N1]. Start with the glass already partly filled, keep the stream under 2 s, and let the fizz carry the beat.
4. **Lock the label to camera and keep the orbit under about 15° while hands touch the product.** Label drift hides in motion blur. If the label still drifts, comp it back in post (04, 11-food-drink l.107).
5. **Slow motion is a phrase at the front of the prompt, not a setting.** Use "captured in extreme slow motion, high frame rate capture" first, then the subject, then a slow camera move. No whips or snap zooms inside slow motion [S1].
6. **Big motion breaks identity. Design the beat so identity is carried by the silhouette.** For Otto that is the moustache and the blazer. Keep the waxed moustache rigid in wind; it is a gag and an identity anchor at the same time [inf].
7. **A 30 s "oner" is 5–7 generations joined at hidden seams.** One-generation 30 s takes cut on their own; no documented setting prevents it [A1]. Put the seams on identical keyframes, motion blur, glare or occlusion (16 §3.3).
8. **Silence is the setup; the hit lands on the frame of the reveal.** Never early. Kill the music for 0.5–1 s before the payoff, and end the tagline about 1 s before the last frame [H1][SO1].
9. **Fantasy must be undeniable, not claimed.** The ASA rejected a "fantastical" defence when nothing in the ad showed super-human powers [ASA1]. The twist has to visibly reveal that the danger was never real: a film set, an airbag, or a crew.
10. **Disclose, and keep the mascot's rules.** Add an "AI-generated" super or platform label on realistic footage [P1]. Never break `OTTO.md`: the mouth is never visible, and he is never wide-eyed. Both rules change how the drink and reaction beats are written (§1.4).

---

## 1. Product-interaction shots

### 1.1 What fails, and the fix

| Beat | Typical failure | Fix (prompt and frame strategy) |
|---|---|---|
| **Tab pop** | The finger merges with the tab, or the tab appears twice. The can dents or rescales. The puff comes from the wrong place. | Start frame: the thumb is already under the tab and the label faces the camera. End frame: the tab is up and a small vapour puff sits at the opening. Prompt only the path between them: "the thumb lifts the tab in one short motion, a small vapour puff escapes from the opening, the can does not move or deform." Keep it to 3–4 s and add "already moving at frame 1" (11-fashion-luxury l.195) [inf]. |
| **Pour** | Volume appears from nothing [N1]. Liquid passes through the glass or melts [HL1]. Droplets float upward [HL1]. | Show no level change: the glass starts ⅓ full and the stream lasts 1.5–2 s. Wording: "liquid contained within the glass, surface tension at the rim, pouring downward" [HL1]. Use soft or diffused light on the liquid to stop specular flicker [HL1]. One liquid event per shot (11-food-drink l.309). |
| **Fizz and condensation** | It rarely fails. These are the reliable liquids. | Lean on them: "spherical bubbles rising in vertical chains, condensation beads, one bead slides" (11-food-drink l.21–27). |
| **Drinking** | The glass passes through the face. The liquid level doesn't drop. The hand loses its grip [EL1]. Lips and teeth smear (30 §0.3). | Hide the mouth and the level: shoot a three-quarter profile with the glass occluding the lower face, cut on the rim's contact, and let the sip SFX sell it. For Otto, see §1.4. |
| **Perfume spray** | Mist comes out of the wrong place. The bottle shape drifts. | "Spray particles in slow motion, product stationary" (07 l.42). Backlight the mist and keep a finger partly occluding the label (11-beauty l.61). |
| **Lighting a candle** | Flame appears before the match touches the wick. The flame is a uniform loop. | Start frame: the match flame is already lit near the wick. End frame: the wick is lit. Prompt "the flame transfers on contact", with no hand rotation [inf, no source tested]. |

### 1.2 Wording that holds the product

- **Reference key.** `<<<image_1>>>` is THE PRODUCT (exact shape, colour, label); this label is the ONLY readable text. Describe the product in words as well as tagging it (12 §F).
- **Containment.** "Maintain the exact appearance and design of the can throughout" (07 l.34). "Show the can exactly once; never a second can" [H1].
- **Hands.** Show the hand at the frame edge with fingers partly occluding the product. It kills the floating-render look (10 l.52). Keep finger motion small [EL1].
- **Ban list (drinks).** Use 11-food-drink l.35, and add "can never dents, label never warps, no extra cans".

### 1.3 Slow motion and "high-speed camera" phrasing

- No model in our stack has an fps parameter: "you control speed with language, not a slider" [S1].
- Put the speed cue first: "captured in extreme slow motion" / "ultra slow-mo at high frame rate" / "high frame rate capture". Stack "time stretched" if the result is too fast. Soften the cue if the frame freezes [S1].
- Real-DP numbers are useful as style words, not as settings: 240 fps at 1/500 for flying ingredients, and 600 fps for pours (05 l.26). Writing "Phantom high-speed camera, 240 fps" is **[inf]**: it is plausible as a style cue, but untested by us.
- In-generation ramps ("begins at normal speed, then ramps into dramatic slow motion as…") work, but "will not always nail the exact ramp point". Roll several takes [S1]. Safer: ask for "super slow motion" and retime in the edit, because normal-speed clips can't be slowed cleanly (07 l.44).
- Slow motion exposes texture crawl on water and fabric, and warps fast limbs [S1]. Keep slow-motion beats to simple whole-body motion.

### 1.4 Otto drinks without a mouth (house rule)

`OTTO.md` says the mouth is never shown and that he is never wide-eyed or startled. The founder's "eyes widen" beat therefore becomes:

- **Sip:** a three-quarter profile. The glass rim rises and disappears **under the moustache**, and the glass tilts 20°. The moustache never parts. The sip SFX does the work.
- **Reaction ("eyes widen"):** one brow lifts higher than usual, and **the two waxed spiral tips spring upward one notch**. This is the signature reaction, and it keeps identity because the moustache *is* the silhouette [inf].
- In Kling, end-frame the reaction (tips up), so the model only interpolates a small shape change.

---

## 2. Action and stunt beats

### 2.1 What the sources say

- **Beats with timecodes past 15 s; one action and one camera move per beat.** Use a 3-part arc for 30 s: open (≈0–5 s, subject and world), main action, close (lock the final frame) [F1][J1]. Use 3–5 beats in 30 s; more than 5 leaves each beat too short to read [A1].
- **Name the camera move and its speed.** Push-in, track, orbit or crane, at a stated speed. Seedance 2.5 reportedly holds perspective better through moves than 2.0 [F1] (vendor-adjacent claim).
- **Add a CONSTANTS line** listing what must not change (wardrobe, light direction, set). It "matters more" in multi-beat clips [A1].
- **Seedance is built to cut.** "One take" means one generation pass, and "no documented setting prevents cuts" [A1]. Plural or long prompts invite cuts. "Continuous single shot" helps but does not guarantee anything (16 §1A).
- **Kling 3.0: plan passes, not one lucky prompt.** It is strongest when image-anchored and weakest at long-form continuity [E1]. Change one variable at a time, and start subtle before strong motion [E1]. Use physical verbs ("fall", "run") so the model knows which physics to simulate [G1].
- **Jumps:** "captured in slow motion at the peak of the jump" is a known template. "Be cautious with rapid limb movement" [S1].
- **Previs before paying.** HumanSignal fixed an impossible near-miss shot by feeding a crude clay previs as a motion and camera reference [N1]. Our cheapest previs is Wan 3.0 at $0.05/s (12).

### 2.2 Execution pattern for a leap and fall [inf, built on the above]

| Phase | Frame strategy | Prompt notes |
|---|---|---|
| Edge / take-off | A Kling still of him at the edge with weight on the front foot, **mid-motion** (16 §2.5: static hand-off frames stall). | "Steps off the edge in one calm motion, body upright, arms slightly out; the camera holds, then tilts down after him." |
| Fall | Seedance 2.5 i2v, start = the take-off frame, `end_image_url` = a mid-fall frame (or a glare frame, §2.4). | "Captured in extreme slow motion. The camera free-falls with him at the same speed, 2 m in front, face to camera. Glass windows stream upward past him, his reflection sliding across them. Far below, traffic streams along the avenue, headlights and taillights. Blazer and hair ripple in the wind; the waxed moustache stays perfectly rigid." |
| Wind and crowds | Name the mover and its direction: "cars move away from camera in both lanes". | Haze and depth of field hide mistakes in background crowds and cars [inf]. |
| Reveal / landing | A Kling still of the landing world. | Write only the path between frames. Never fight the end frame (12 l.153). |

**Identity through the fall [inf]:**
- Keep the face to camera only in the first and last 2 s of the fall. In between, use a three-quarter or back view where the silhouette carries identity.
- Re-anchor with the Otto reference pack on every call (master, three-quarter, profile, full body; `OTTO.md`).
- Keep the face larger than about 15 % of frame height when it is visible. This is an assumption, not tested.

### 2.3 When a single take is impossible

A true one-generation take is unrealistic when any of these is true [inf]:
- more than 30 s (the Seedance 2.5 cap [A1]);
- a precise product interaction **and** big body motion in the same generation;
- three or more failure-prone beats. If each beat comes out clean about half the time, five beats in one take succeed about 3 % of the time, which is why gens per final second run 10–24 (22 l.156).

### 2.4 Faking the oner (how it must still feel continuous)

Use 16 §3.3, mapped to action:

| Seam | Where in an action ad | How |
|---|---|---|
| **Identical keyframe** | Between any two calm beats | Clip N ends on K_i; clip N+1 starts on K_i (16 §1B). Trim the ease-in, use "already moving… constant speed" (16 §2.5). |
| **Glare whiteout** | Mid-fall, as the sun flashes off the glass façade | Clip ends in a gold-white glare frame; the next clip starts from the same glare. Identity can't drift in a flat colour (16 §2.3). |
| **Occlusion / foreground wipe** | A window mullion, a cloud layer, the can filling the lens | *Rope* and *Children of Men* tricks [V11 in 16]. |
| **Motion-blur ramp** | Step-off, landing impact | Ramp 400–500 % through the seam and add blur. It hides the in-between frames (16 §2.5). |
| **Sound bridge** | All seams | One continuous wind and music bed across every seam (16 §3.5). The ear decides continuity before the eye [inf]. |

Rule: never two seams within 3 s. Keep screen direction and camera direction constant through every seam (16 §3.4).

---

## 3. Timing the punchline in audio

| Element | Rule | Source |
|---|---|---|
| **Opening silence** | Near-silence from 0–1.5 s, then the downbeat hits on the can crack. | 11-food-drink l.97 |
| **Can pop and hiss** | This is the category's own sonic brand: Coca-Cola's pop, pour and fizz date back to Suzanne Ciani's late-1970s sound design, and its "Refreshment" work used "a bottle cap popping open, a bottle pouring, a thirst quenching gulp" [CK1]. Use 3–5 Foley layers per action, split low/mid/high (08 l.61). | [CK1], 08 |
| **Sip** | Record or generate it close and dry. It is the only proof of drinking when the mouth is hidden (§1.4). ElevenLabs SFX prompt: "close-mic single sip from a glass, soft carbonation, dry room". | [EL2] terms |
| **Silence before the payoff** | A short gap builds anticipation. A sound before the visual break reveals the joke early. If picture and performance already land the beat, silence may be the funniest choice. Check on phone speakers. | [SO1] |
| **The drop** | Use a "braam" or impact on the take-off frame, then low-pass the music to about 1.8 kHz and pitch the SFX down for slow motion (08 l.63). | [EL2], 08 |
| **Twist hit** | Hard cut to 6–10 frames of silence on the glare seam, then one dry real-world sound (an airbag thump, a clapperboard), then a line. | [inf] from [SO1] |
| **VO tag** | Otto's locked voice (`OTTO.md`), deadpan and slow. Finish the tagline about 1 s before the end, with music only after it [H1]. Respell the brand phonetically if it is misread [H1]. | [H1] |
| **Seedance audio** | Always state the audio, or set `generate_audio:false` and build the sound in post. Unspecified audio defaults to Mandarin dialogue and Chinese-sounding music [H1]. | [H1], 12 |

---

## 4. Safety and brand rules for stunt gags

- **Social responsibility and emulation.** The ASA banned Mountain Dew's snowboarding stunt over child emulation. It held that a warning was "insufficient as a deterrent" in a 2024 motorcycle ruling. It found JD Sports' stunts "unsafe and irresponsible" if copied on a public road [ASA2]. We could not retrieve the current CAP clause text, so check rule numbers on the CAP site before citing them.
- **"Fantasy" is not a defence by assertion.** For Macallan, the ASA said there was "no suggestion that the male character had any super-human attributes or powers, or that he was part of a mythical world". Clearcast had earlier cleared the same ad, so clearance and ASA rulings can differ [ASA1]. Australia's board did accept fantasy for Dare Iced Coffee [ASA1]. **House rule [inf]:** the twist must *show* that the stunt was never real (a set, an airbag, a crew, a miniature). A super saying "don't try this" is not enough.
- **Alcohol-free is still a soft drink, and that is a plus.** AURUM is non-alcoholic, so the alcohol-and-daring rule that sank Macallan [ASA1] does not apply directly. Never use alcohol cues (coupe toasts, "proof", bar backs). Words like "zero-proof" invite the alcohol reading; prefer "sparkling yuzu soda" [inf].
- **Do not glamorise the jump itself.** Keep Otto calm and deadpan, with no thrill-seeking framing. No real-world landmark that a viewer could climb. Present the city as a generic skyline [inf].
- **AI disclosure.** TikTok requires an AIGC label on realistic AI scenes and checks C2PA credentials. Meta shows "AI info". YouTube moved its label onto the player in May 2026. EU AI Act Art. 50 transparency applies from 2 Aug 2026 [P1] (03 §17, 30 §0.9). Burn in "AI-generated film" for 1 s on the end card, and set the platform label too.
- **Mascot integrity.** No mouth, never startled (`OTTO.md`). Otto is fictional, so no real-person likeness issue arises. Vee may speak, because her mouth is visible (`VEE.md`).

---

## 5. AURUM rooftop recipe ("Top Shelf"), 30 s, 9:16

**Concept.** Otto stands on top of a skyscraper spire at golden hour. He opens an AURUM can (ASMR pop), pours, sips, and the moustache tips spring up. He sets the can down, label to camera, and calmly steps off. He falls in slow motion past windows, with traffic far below. The sun flares off the glass. Out of the glare he lands softly on a stunt airbag in a studio: the skyline was a set. Vee clicks her stopwatch: "It's perfect. Ship it." End on the packshot.

The twist does three jobs: it is the punchline, it makes the fantasy visible (§4), and it hides the hardest seam (§2.4) [inf].

**Product.** The `brand_kit.json` colours are champagne gold #C9A65A and glacier teal #0E6E73, with the label text "AURUM" (18). The can artwork must come from the approved AURUM pack still. **[inf]** The yuzu soda can design is not in the repo yet; make it first as a Flare still and use it as `<<<image_1>>>`.

### 5.1 Beat sheet and seams

| t (s) | Beat | Source clip | Seam into next |
|---|---|---|---|
| 0–4.5 | **Hook.** A drone orbit closes in on Otto on top of the spire. The city is golden below, the wind moves his blazer, and he holds the can. | A: Kling K0→K1, 5 s | identical K1 |
| 4.5–8 | **Pop.** A close, low angle: thumb under the tab, *pop + hiss*, a vapour puff, label to camera. | B: Kling K1→K2, 4 s | identical K2 |
| 8–11.5 | **Pour.** The glass starts ⅓ full; a 1.5 s stream, fizz rising, condensation. | C: Kling K2→K3, 4 s | identical K3 |
| 11.5–14.5 | **Sip.** Three-quarter profile, the rim under the moustache, *sip*. **0.7 s of silence.** Moustache tips spring up and one brow lifts. | D: Kling K3→K4, 3 s | identical K4 (mid-motion) |
| 14.5–24 | **Jump.** He sets the can on the spire tip, label to camera, and steps off (*braam* on take-off). Slow-motion free-fall with him past windows; traffic below; glass still in hand, not a drop spilled. Ends flying into a sun glare off the façade. | E: Seedance 2.5 i2v K4→K6, 10 s | **glare whiteout K6**, 8 frames of silence |
| 24–27 | **Twist.** Out of the glare, he lands softly on a stunt airbag (*thump*). The camera pulls back: a soundstage, a painted skyline backdrop, crew. Vee clicks the stopwatch: "It's perfect. Ship it." | F: Kling K6→K7, 4 s | identical K7 |
| 27–30 | **Packshot.** The AURUM can and glass on an apple box, label to camera. Otto VO: "AURUM. Sparkling yuzu. Taste from the top." It ends at 29 s. Super: "AI-generated film." | G: Kling K7→K8, 3 s | — |

The raw clips total 33 s; trim the ease-ins and ease-outs to 30 s. Speed-ramp the step-off (100→40 %) and the landing (40→100 %) in the edit (08 l.32).

### 5.2 Keyframes (Flare, Otto reference pack + AURUM can, `OTTO.md` anchor block + ban list)

Header for every still:

```
9:16, golden hour 20 min before sunset, warm low key from camera-left, soft haze over the city, editorial film grade, fine grain. [OTTO ANCHOR BLOCK]. <<<image_1>>> = AURUM can: slim 355 ml can, brushed champagne gold #C9A65A, glacier-teal #0E6E73 band, wordmark "AURUM" — the only readable text. [BAN LIST + no extra cans, can never dents, label never warps]
```

| K | Still prompt (after the header) |
|---|---|
| K0 | Wide aerial: Otto stands on a small flat platform at the tip of a skyscraper spire, far above a generic golden city grid, can in his right hand at chest height, label to camera. Small in frame (lower third). |
| K1 | Medium-close, low angle: Otto holds the can at chest height, label to camera, left thumb under the tab; city haze behind; blazer edge lifted by wind. |
| K2 | Same framing: the tab is up, a faint vapour puff at the opening, can tilted 30° over a clear highball glass in his left hand, glass ⅓ full of pale gold sparkling soda, bubbles in vertical chains. |
| K3 | Three-quarter profile: the glass ¾ full at chest height, condensation, can lowered at his side, label still readable. |
| K4 | Three-quarter profile: the glass rim lifted under the moustache, glass tilted, the waxed spiral tips sprung up one notch, one brow raised higher, eyes amused (not wide). His weight is shifting toward the edge. |
| K5 | (Not generated; optional mid-fall control frame.) Otto mid-fall, upright, face to camera, glass in hand, glass façade with his reflection, traffic far below, motion blur on the windows. |
| K6 | Full-frame warm gold-white sun glare off glass, no subject. Make it with ffmpeg as a flat gradient plus grain (free) [inf]. |
| K7 | Wide, soundstage: Otto sitting upright on a large grey stunt airbag, glass in hand; a painted golden skyline backdrop behind; crew silhouettes, a C-stand; Vee at frame-right with a stopwatch raised. |
| K8 | Packshot: the AURUM can (label to camera) and the full glass on a wooden apple box, studio haze, warm rim light, the brass viewfinder resting beside them. |

### 5.3 Motion prompts (sound off; all audio built in post)

- **A (Kling 3.0 pro i2v, 5 s, K0→K1).** "One continuous drone move. The camera glides forward and descends in a slow arc toward the man on the spire, at constant speed, and settles exactly on the end frame. Wind ripples his blazer; the waxed moustache stays rigid. The can does not move in his hand. No cuts."
- **B (4 s, K1→K2).** "Already moving at frame 1. His thumb lifts the tab in one short motion; a small vapour puff escapes; he tilts the can over the glass and the first stream starts. The can never dents; the label stays facing camera. Camera static-handheld."
- **C (4 s, K2→K3).** "Captured in slow motion. A short stream of pale gold soda pours downward into the glass, liquid contained within the glass, bubbles rising in vertical chains; he lowers the can. Diffused golden light. One pour only."
- **D (3 s, K3→K4).** "He lifts the glass; the rim goes under his moustache; the moustache does not part; the two waxed tips spring upward slightly; one brow rises. Camera holds."
- **E (Seedance 2.5 i2v, 10 s, 480p for iteration, then 720p; `image_url`=K4', `end_image_url`=K6, `generate_audio:false`).** Here K4' is a "can placed on spire, weight on front foot" variant of K4.

  ```
  One continuous take, a single unbroken camera move, no cuts. CONSTANTS: Image 1 man (Otto anchor), black turtleneck, charcoal blazer, oxblood pocket square, brass viewfinder; glass of gold soda in his left hand; golden-hour light from camera-left.
  [0–2 s] He steps calmly off the spire edge, upright, arms slightly out; the camera holds, then drops with him.
  [2–8 s] Captured in extreme slow motion, high frame rate capture. The camera free-falls with him at the same speed, 2 m in front of him. Mirrored windows stream upward behind him, his reflection sliding across them. Far below, traffic streams along the avenue, headlights and taillights moving away from camera. His blazer ripples in the wind; the waxed moustache stays perfectly rigid; not a drop leaves the glass. He looks calm, one brow raised.
  [8–10 s] He drops past a corner of the façade into a blinding warm sun glare that fills the whole frame.
  ```

- **F (Kling, 4 s, K6→K7).** "The glare fades as he drops the last metre onto the airbag and sinks softly; the camera pulls back at constant speed to reveal the soundstage; the woman at right raises her stopwatch. One continuous move."
- **G (Kling, 3 s, K7→K8).** "The camera cranes down and pushes in to the can and glass on the apple box and settles; condensation bead slides; label sharp."

### 5.4 Sound map (ElevenLabs; Otto and Vee voices locked)

- **0 s:** wind bed at roof height, no music.
- **4.8 s:** close tab *pop* + hiss (3 layers), then a minimal music downbeat.
- **8–11 s:** fizz bed and ice tick.
- **12.5 s:** dry *sip*, then **music cut and 0.7 s of wind only**, then a tiny "spring" tick on the moustache tips.
- **14.5 s:** *braam* on the step-off. The music returns low-passed with whoosh layers. Pitch the wind down through the slow motion.
- **24 s:** hard cut to silence for 8 frames, then the airbag *thump* and the stopwatch click.
- **25.5 s:** Vee: "It's perfect. Ship it."
- **27.2–29 s:** Otto VO tagline, then the sonic logo and 1 s of music tail.

### 5.5 Cost estimate (list prices, 12 §1)

| Item | Calc | USD |
|---|---|---|
| Previs: Wan 3.0 480p, 2 × 30 s blocking passes | 60 s × $0.05 | 3.00 |
| Keyframes: 8 Flare stills × 3 candidates (K6 is free) | 24 × $0.34 | 8.16 |
| Kling 3.0 pro i2v, A+B+C+D+F+G = 23 s, 3 takes each | 69 s × $0.0952 | 6.57 |
| Seedance 2.5 i2v fall at 480p, 10 s × 3 takes | 30 s × $0.206 | 6.18 |
| Seedance fall final at 720p, 10 s × 1 | 10 s × $0.462 | 4.62 |
| **Base total** | | **≈ $28.5** |
| Optional "true oner" lottery: one 30 s Seedance 2.5 i2v at 480p, K0→K8, full beat prompt | | +6.17 |
| Contingency (~25 %) | | +7 |
| **Planning number** | | **≈ $36–42** |

Audio uses ElevenLabs subscription credits; we assume no marginal spend [inf]. Upscaling and grain run locally (06, 08).

### 5.6 Fallback plan

1. **Product beats fail (B–D).** Drop the pour: the glass starts full, and only the tab pop and the sip remain. The sip is sold by occlusion and SFX. If the label drifts, comp it from the pack still (11-food-drink l.107).
2. **Identity breaks in the fall (E).** Re-prompt as a back or three-quarter view with the camera above him. If that also fails, split E into two Kling clips (K4→K5 and K5→K6, 5 s each, ≈ $0.95 per pass) with the K5 mid-fall still as the anchor.
3. **The fall is unusable, or a safety review wants less.** Use the off-screen gag. Hold on the empty spire: the can stands alone, label to camera, with 1.5 s of wind and silence. Then a distant *thump* and an off-screen "Cut! Print it." Crane down through the haze (a glare seam) into the soundstage reveal (F). Cost: −$10.8 (no Seedance) +$0.95 (one extra Kling clip).
4. **The oner reads as cuts in the test screening.** Add a sound bridge, ramp every seam to 400 %, and move any seam that falls within 3 s of another (§2.4).
5. **Budget hard cap of $20.** Skip previs, use 2 candidates per still and 2 takes per clip, and finish the fall at 480p with upscaling. That comes to ≈ $14 (5.44 + 4.38 + 4.12), leaving $6 of slack.

### 5.7 QC before the client sees it

- Label OCR reads "AURUM" on every product frame (18, `brand_kit.json`).
- The mouth is never visible, and the eyes are never wide (`OTTO.md`).
- No liquid level jumps.
- The glass is never duplicated.
- No seam is visible at full speed on a phone.
- The twist reads as "set" within 1 s for a cold viewer.
- The disclosure super is present and the platform AI label is set.

---

## 6. Sources

- **[A1]** AI Video Sensei, "Seedance 2.5 multi-shot guide": https://aivideosensei.com/guides/seedance-2-5-multi-shot-guide
- **[F1]** ForVideo, "Seedance 2.5 Prompt Guide: 12 Prompts That Actually Work": https://forvideo.ai/blog/seedance-2-5-prompt-guide
- **[J1]** JXP, "Seedance 2.5 Prompt Guide" (30 s three-segment structure, via search summary): https://www.jxp.com/seedance/blog/seedance-2-5-prompt-guide
- **[S1]** Seedance.tv, "Seedance slow motion video guide 2026": https://www.seedance.tv/blog/seedance-slow-motion-video-guide-2026
- **[H1]** Hedra, "Directing Seedance 2.5 with beats": https://mkt.hedra.com/blog/directing-seedance-2-5-with-beats
- **[E1]** Elser AI, "Kling 3.0 Complete Guide" (EN/IT/DE): https://www.elser.ai/blog/kling-3-0-complete-guide
- **[G1]** GlobalGPT, "How to use Kling 3.0 like a pro" (DE): https://www.glbgpt.com/hub/de/how-to-use-kling-3-0-like-a-pro/
- **[N1]** NovoAds summary of HumanSignal's physics test (23 Sep 2026): https://novoads.ai/en/blog/ai-video-physics-test
- **[HL1]** Hailuo, "Troubleshooting fluid artifacts": https://hailuoai.video/knowledge/fix-fluid-artifacts-ai-video-troubleshooting
- **[EL1]** Elser AI, "Why AI video generators mess up hands and faces": https://www.elser.ai/blog/why-ai-video-generators-mess-up-hands-and-faces
- **[EL2]** ElevenLabs Sound Effects docs (impact, whoosh, braam; 0.1–30 s): https://elevenlabs.io/docs/capabilities/sound-effects
- **[SO1]** Sonilo, "Funny sound effects for videos" (silence and timing): https://sonilo.com/blog/guides/funny-sound-effects-for-videos
- **[CK1]** WeAreListen, "Brand spotlight: Coca-Cola": https://wearelisten.com/blog-brand-spotlight-coca-cola · Soundcy, "When Coke weaves a sound": https://soundcy.com/article/when-coke-weaves-a-sound
- **[ASA1]** RPC, "ASA ruling on alcohol and social responsibility: Macallan" (page body not retrievable; quotes via search summary): https://www.rpclegal.com/snapshots/advertising-and-marketing/asa-ruling-on-alcohol-and-social-responsibility-macallan/ · Ad Standards AU (Dare Iced Coffee): https://adstandards.com.au/sites/default/files/reports/340-05.pdf
- **[ASA2]** BeverageDaily on Mountain Dew (2012; now 410): https://www.beveragedaily.com/Article/2012/08/01/Dangerous-stunt-in-Mountain-Dew-advert-draws-PepsiCo-apology · British Motorcyclists Federation on the motorcycle ad rulings: https://www.britishmotorcyclists.co.uk/motorcycle-advert-update/ · ASA safety topic: https://www.asa.org.uk/topic/Safety_and_security.html
- **[P1]** CinerAds, "AI ad disclosure requirements 2026": https://www.cinerads.com/blog/ai-ad-disclosure-requirements · AuditSocials cross-platform comparison: https://www.auditsocials.com/blog/cross-platform-ai-content-labeling-requirements-2026-meta-google-tiktok-youtube-comparison
- **Found, transcript not fetched (429):**
  - "3 Techniques to Make AI Fight Scenes Look EPIC (Seedance 2.5)", Meta Instincts, `SdtaDI8plF4`
  - "Create Cinematic AI Ads with Seedance 2.5 — Full guide", Dan Kieft, `kGku3TTiYO8`
  - "I Tested Seedance 2.5 for Product Ads", Thomas Lundström, `y6Zw5WFs62k`
  - "STOP Wasting Credits & Master Kling 3.0 in 25 Minutes", Dan Kieft, `b_RghITuQQM`
  - "3-Step Workflow To Make Ultra-Realistic AI Ads", Higgsfield AI, `3rDs6FhFoUQ`

  These are the next study queue when the rate limit clears.
- **Internal:** 04, 05, 07, 08, 10, 11-beauty, 11-fashion, 11-food-drink, 12, 13, 16, 18, 22, 30, `../mascot/OTTO.md`, `../mascot/VEE.md`.
