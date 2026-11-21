# Video realism: how to get believable motion out of each model

Round 1 (lab E01) failed on realism for predictable reasons:
- one-shot clips with no camera language
- vague actions ("rotates", "rises")
- no physical cause and effect
- flat start frames
- low resolution
- no sound design

The references (Seedance 2.5 1080p, Genjutsu hybrid) are realistic because:
- they start from **real footage** or **rich reference images**
- the camera is described like a DoP would describe it
- every action has a physical cause

## 1. Ten realism rules (apply to every video prompt)
1. **Physical cause → effect, with weight.** Not "frost spreads". Write "she sets the ice-cold can down; frost crystals crackle outward from its base across the hot concrete, a thin vapor rising".
2. **Name the camera like a DoP.** Body and lens ("handheld 35mm", "gimbal", "drone", "locked tripod"), the move with speed and **end state** ("slow 2-second push-in ending on the label"), and micro-imperfections ("subtle handheld micro-drift, natural focus breathing").
3. **One primary action per shot, 2–4 s per shot.** Long single shots drift and morph. Many short timed shots look edited and real.
4. **Timecode every shot** (Seedance 2.5 / Kling multi-shot): `0:00-0:02 …`, `0:02-0:04 …`. That's exactly the "steal my prompt" style that went viral.
5. **Light continuity:** state the light source and keep it identical across shots ("same hard 4 PM sun from the left in every shot").
6. **Real-world texture cues:** sweat sheen, skin pores, fabric wrinkles, dust in light beams, lens flare, sensor grain, motion blur on fast objects, rolling-shutter feel for phone POV.
7. **Lock identities with references:**
   - Product = an @Image with exact label text written in the prompt.
   - Person = an @Image plus wardrobe written out.
   - Location = an @Image.
   - Say "never changes" once.
8. **Hands:** grip on the lower half of the product, label facing the lens, no finger contact on text. Or cut before contact. Or **film real hands** (hybrid).
9. **Liquids:** keep pours ≤ 2 s and macro. Describe the stream ("a clean ribbon of water folds into the glass, bubbles climbing"). Or film the real pour.
10. **Sound is half the realism:**
    - Write the foley per shot ("crisp aluminum pop, fizz, ice clink, distant traffic").
    - Seedance generates audio. For Kling and Hailuo, add ElevenLabs SFX in the edit.

## 2. Model cards (what to use for what, from our lab + references)
| Need | Use | Why / settings |
|---|---|---|
| **Hero multi-shot ad 10–30 s, people + product** | **Seedance 2.5 reference-to-video** | up to 30 s, 50 refs, native audio, timecoded shots. 720p to test ($0.46/s), 1080p final ($1.14/s) |
| Exact label in motion (rotation, hand pick-up) | **Kling 3.0 Pro I2V** | best label hold in E01 (T01, T03). `multi_shots` + `multi_prompt` up to 6 shots, ≈ $0.14/s |
| Food / liquid texture, cheap | Hailuo 2.3 | won T04 and T06 on motion, $0.04/s, **no audio, 768p, invents text**. Never use it on labels |
| Transform real footage (location / outfit / style) | **Genjutsu** (Higgsfield) | hybrid realism, $0.27/s. Needs a phone clip ≥ 4 s |
| New camera angles from one real clip | **Seedance 2.5 reference-to-video with `video_urls`** | "infinite angles". Cost includes the input video duration |

## 3. Seedance 2.5 master format (copy, fill in)
```
Vertical 9:16 cinematic commercial, {N} seconds, {k} shots in one continuous edit.
@Image1 is the exact product: {exact description + label text}; label and shape never change.
@Image2 is {person}: keep face, hair and {wardrobe} identical in every shot. @Image3 is the location.
0:00-0:02 {shot size + angle + lens}, {subject} {one physical action with cause/effect}; {camera move + end state}.
0:02-0:04 ...
...
Global look: {light source & direction, constant}, {film/lens look}, {palette}, realistic skin and material texture, subtle handheld micro-drift.
Audio: {foley per beat}; {music: none / genre}; {VO: none, added in edit}. No on-screen text, no subtitles, no extra logos.
```

## 4. Kling 3.0 multi-shot format
- `image_url` = the strongest start frame (art-directed, §image-direction).
- `multi_shots: true`, `multi_prompt`: up to 6 items, each ≤ 512 chars, `duration` per shot; the durations sum to the total.
- Each shot prompt is self-contained: subject + action + camera + light + "label stays identical".
- Add `negative_prompt`: "warped text, extra letters, melting, morphing hands, flicker".

## 5. Realism QC (on top of K1–K8)
- R1: Does any frame look CG (plastic skin, perfect symmetry, floaty motion)? → add texture and imperfection cues, use a real plate.
- R2: Does motion have weight (acceleration, settle, overshoot)? → describe the physics.
- R3: Is the light consistent between shots? → restate the light per shot.
- R4: Would a viewer screenshot it as an "AI fail"? → cut it or regenerate.
