# 16 — Seamless flow: a 15–25 s ad that plays as one continuous film

Researched 2026-10-07: 19 YouTube transcripts, official/vendor guides, commercial making-ofs; ffmpeg recipes tested on 6.1 with synthetic clips. Builds on 07, 08, 12 and 14 without repeating them. [inf] = inference; [V3]-style keys are listed at the end.

**Client brief:** "Our ads feel like scene after scene. I want a film that RUNS."

---

## 0. Why our ads read as a slideshow, and the fix for each cause [inf, from the sources below]

| # | Cause | Fix |
|---|---|---|
| 1 | Every i2v clip **starts from rest and ends settling**. The model eases in from a still image and eases out onto the end frame | §2 "already moving" wording; trim 6–10 frames at each end; ramp through the seam (§4 R3, R7) |
| 2 | **Camera direction resets** each shot (push, then orbit left, then tilt) | One "impossible camera" path, written into the seam sheet (§5) |
| 3 | **Per-clip AI audio** (room tone and music change at every cut) | Generate with sound off. Lay one continuous bed with a riser across the seams (§3.5) |
| 4 | **Exposure or colour pops** at the join | Seam colour match (§4 R4) [V5] |
| 5 | **Uniform 5 s shots** | Vary lengths and accelerate toward the reveal (§3.6) |
| 6 | **Cuts land on still frames** with unrelated compositions | Shared keyframes, occlusion seams, match cuts, eye-trace (§1–3) |

---

## 1. Four ways to get continuity from AI (choose one per ad)

**A. One generation, one take.** Seedance 2.5 i2v/r2v (4–30 s) or Kling 3.0 (3–15 s, multi-shot off).
- *Pro:* true continuity of motion, light and sound inside the clip.
- *Con:* product fidelity drifts over long moves (12 §7). One bad second ruins the whole take.
- Kling wording: "This is a 15-second cinematic long take, a single unbroken shot with no edited transitions" / "one continuous long take without any cuts" [W1].
- Seedance adds cuts the longer and more plural the prompt ("cinematic camera angles", "trailer"); write "continuous single shot" [V2]. A sequence of framings makes it invent cuts or "average them into a long messy pan" [W7].

**B. Keyframe-anchored chain (our default for product ads) [inf].**
- Make **every seam frame up front as a Flare still**: K0 … Kn, each one derived from the master still.
- Then make each clip with Kling 3.0 pro i2v: `image_url = K_i`, `last_image_url = K_{i+1}`.
- Two neighbouring clips share a pristine, identical frame. Clips render in parallel. The product is re-anchored at every seam.
- Avoids the "VHS copy" decay of sequential re-grabs, where after about 6 hops the character is "a completely different person" [V1]. Identical seam frames let clips "chain infinitely" [V6].

**C. Sequential chain (last frame → next first frame), or Seedance continuation.**
- Use it when you can't pre-plan every frame, for example a character walking through spaces [V1, V19].
- Better variant: give Seedance the **whole previous clip as a video reference**, not a screenshot. A frozen frame "builds the next clip from that frozen image… the camera might suddenly change direction". With the video reference, the model reads "the camera speed, the direction of movement, the trajectory… the way lighting changes" [V7].
- On Higgsfield that is `seedance-2.5/reference-to-video` with `video_urls`. Input seconds become billable, at a ×0.6 token rate (12 §1).
- Or use `seedance-2.5/video-extend` ($0.277/s at 720p, input plus output).

**D. Connected multi-shot (a "seamlessly connected commercial", not a one-take).**
- Kling 3.0 Custom Multi-Shot sets the content and duration of each shot, and "the model will strictly follow the prompts" [W1].
- Real cuts, consistent light and subject. Sweet spot 5–7 shots per 15 s [V2]. Use it for a match-cut burst: "three rapid match cuts" in 2 s "felt a little bit more continuous" [V2].
- Billed on the sum of the shot durations (12).

**Rule of thumb [inf]:**
- Hero product move under 15 s → A, then land with a Kling `last_image_url` packshot.
- 15–25 s journey through spaces → B.
- Character or story continuity → C.
- Energy bursts → D, inside B.

---

## 2. Prompt wording that works

### 2.1 The bridge clip (Kling 3.0 pro i2v, mid-chain seam)
Template D in 12 ("settles exactly on the end frame") is right **only for the final packshot**. A mid-chain clip must *pass through* its end frame at speed [inf]:

```json
{"image_url":"<K2>","last_image_url":"<K3>","duration":5,"sound":"off","cfg_scale":0.5,
 "prompt":"Single continuous shot, one physical camera move, no cuts. The camera is already moving right at a slow walking pace from the first frame and keeps a constant speed until the last frame; it does not slow down, pause or settle. Path: the camera arcs 30° right around the amber bottle at constant radius while rising slightly, so the window light slides across the glass from left shoulder to label. The bottle never moves or deforms; label text \"SOL\" stays sharp. Light stays warm from upper left throughout."}
```

Why each part is there:
- **Name the mover.** Write "the camera". A vague "360" in Kling made the model spin the subject instead of the camera (Artlist case study). Stalman says to name what moves and how it moves [V5].
- **Constant speed.** "Keep the camera speed constant through the whole shot… so we can do our own speed ramping" [V5]. It also removes the stop-start of §0.1.
- **Describe the process, not the result.** Add pacing words ("gradually", "smoothly" versus "sudden pop") and say what stays fixed [W6].
- **Make the move physically compatible with both frames.** Stalman's zoom seam failed because the real footage *panned down* while the prompt said *forward* [V5].
- **Keep the frames similar.** Kling's official advice is that start and end frames "should be as similar as possible… significant differences may cause a lens switch" [W2]. That is the main cause of unwanted cuts in a bridge.
- **Write it one-by-one for transformations.** "Each piece of furniture pops up and falls into place one by one… super important to write one by one" [V8].

### 2.2 The one-take (Seedance 2.5 i2v/r2v, 12–15 s)
This combines Kling's "At the Nth second" beats [W1], Hedra's timed beats [W3], Opus's physical-bridge rules [W4] and 14's speed percentages:

```
One continuous 15-second take: a single unbroken camera move, no cuts, no jump cuts, no scene changes. Smooth gimbal, no shake.
@Image1 is the exact product: amber glass dropper bottle, gold cap, label "SOL" — the only readable text.
[0–3 s] The camera glides forward low over wet black stone at walking pace toward a single amber drop.
[3–5 s] Without cutting, the camera decelerates and pushes into the drop until amber light fills the frame, then accelerates out the other side.
[5–9 s] It emerges in a sunlit bathroom, drifting right in a slow arc around @Image1 on the shelf; light warms as the camera crosses the window.
[9–12 s] A hand enters frame right and lifts the bottle; the camera rises with it, bottle in the centre third.
[12–15 s] The camera eases back and settles; bottle centred, label to camera; hold still for the final second.
Show the bottle exactly once; never a second bottle. Audio: no music, no dialogue; soft room tone and glass taps only.
```

Key wording [W4]: "One continuous, flowing movement with no cuts. Steadicam-style smooth float"; "Without cutting, the camera moves through [doorway/curtain]".
- Always name a **physical transition mechanism** (doorway, corner, curtain, fog). Abstract environment morphing "requires more specific prompting" [W4].
- At thresholds: "decelerates as it approaches the doorway, then smoothly accelerates into the next room", and describe the light change as the camera crosses [W4].
- "exactly once" stops repeated shots. Always specify the audio, or Seedance defaults to Mandarin dialogue and Chinese-sounding music [W3].
- Match the duration setting to the timecodes [V2].

### 2.3 Flying *through* the product into the next scene
Combine an occlusion seam with a bridge clip:
1. Clip A ends pushing into a surface that fills the frame: the black cap, the amber liquid, a backlit label, a foam bubble.
2. Make that fill frame a still (Kseam).
3. Clip B starts from Kseam and pulls back into the new world.

This is the *Rope* trick: dolly into a dark jacket until one colour fills the frame, cut, dolly out [V11]. Our most reliable seam [inf]: identity can't drift in plain amber.

The prompt pattern comes from the "camera pushes through the phone screen" transition [V4] and the watch-dial dive [V6]: "the camera slowly pushes forward into [object] and transitions seamlessly into [environment]".

### 2.4 FPV / drone one-takes
- Draw the route on the start still as a coloured line. Prompt "the drone strictly follows the pink path", then "Remove all pink guide lines, arrows, and drawn markings from the final video". Negatives: no cuts, teleporting, warped architecture [W5].
- Name the style so a stylised scene doesn't drift to photoreal [W5].
- Write the route as a sequence of camera actions, not "high-speed, cinematic" [W4].

### 2.5 Failure modes and fixes

| Symptom | Cause | Fix |
|---|---|---|
| Unwanted cut mid-clip | Frames too different [W2]; long or plural Seedance prompt [V2] | Closer keyframes, "continuous single shot", a physical bridge, a shorter clip |
| Crossfade or blob morph instead of camera motion | End-state-only prompt; mismatched light | Describe the process and the mover [W6]; same light in both frames; Stalman found Kling 2.5 Turbo moved where Veo "just creates a fade" [V5] |
| Speed dip at every seam | i2v ease-in/settle | "already moving… constant speed"; trim the ends; ramp the seam (§4) |
| Character stops walking after a hand-off | The hand-off frame looked static, so the model "didn't know that she was in motion" [V1] | Pick a mid-stride frame; state the motion; or use a Seedance video reference [V7] |
| Camera reverses direction across a seam | A frozen frame carries no velocity [V7] | The same motion clause in both prompts; video reference; seam sheet |
| Gradual identity or product drift | Sequential re-grabs [V1] | Keyframe-anchored chain (B); grab a sharper frame a few frames before the end [V1] |
| Weird middle frames in a transition | Model interpolation | Speed-ramp through the seam to 400–500 % and add motion blur. It "hides that kind of weird AI Tyler in between" [V5, V4] |
| Guide lines bleed into the video | Path-drawing workflow | Tighten the removal wording and regenerate [W5] |

---

## 3. Editing craft that makes cuts disappear

### 3.1 Priority order (Murch's Rule of Six)
Emotion > story > rhythm > eye-trace > 2D screen plane > 3D space. **Eye-trace** means keeping the object of interest in the same part of the frame across the cut. This "reduces the friction of a cut" and is the basis of the match cut [V13].

Match the subject's screen position (eye position for people); a few frames earlier or later "can really make the difference" [V15].

### 3.2 Match cuts
There are three kinds: graphic (shape), movement, and audio [V14].

- **Graphic.** Circle → circle: watch, bike wheel, can, pasta.
  - Shoot dead-on and parallel at the circle's centre height so it stays circular.
  - Step the cut 1–2 frames for a "shutter" feel [V18].
  - For AI, generate both stills with the shape at identical x, y and size [inf].
- **Movement.** The hand goes up, then the next shot continues upward. "Your eyes just keep going effortlessly" [V15].
- **Audio.** Helicopter → ceiling fan (*Apocalypse Now*) [V14].

### 3.3 Hidden-cut toolbox (from long-take cinema)
All four are from Vox [V11]:
- **Colour block or occlusion:** *Rope*, *Birdman*.
- **Foreground wipe:** *Children of Men* is six shots joined behind a dark car frame.
- **Whip pan:** cut at the fastest, blurriest moment (*Snake Eyes*).
- **Stacked tricks:** *Spectre*'s opening uses CGI plus motion blur, a black-jacket colour match, then a foreground object.

In-camera versions [V12]: shutter-drag whip (~1/10 s), rack-focus out/in, crash zoom continued across the cut, matched pan direction, motivated foreground wipe.

### 3.4 Momentum and direction
- Keep screen direction constant through the whole film [inf; supports 08].
- A single abrupt high-energy whip makes the shots around it feel calmer. Between energetic shots it "maintains a really good flow" [V12].
- Ramps should be subtle: "even a slight acceleration makes the sequence feel more dynamic, while heavy speed ramping can quickly become distracting" [V6].

### 3.5 Sound is the glue
- An L-cut drags a scene longer. A J-cut adds urgency, because you hear the next scene first (*Baby Driver*'s horn) [V16].
- For a continuous film [inf]:
  1. One music bed and **one room-tone bed** across all clips. Native per-clip audio off.
  2. One long **riser spanning the two biggest seams**.
  3. Whooshes timed to the motion, not the cut.
  4. The hit on the reveal.
- SFX are "completely essential" to sell AI transitions [V5]; a reverse-cymbal riser before the landing [V3].

### 3.6 Rhythm
- Don't give every shot 4–5 s. Use a long → long → short-short-short → long hold structure.
- The hold lands on the reveal (08: 1.5–2.5 s).
- Cut the jump and match bursts on the beat [V15] [inf].

### 3.7 Commercials to show the client

| Film | What flows | How (verified) | Lesson for us |
|---|---|---|---|
| **Honda "Cog"** (2003, 120 s) | One chain reaction | **Two** ~60 s technocrane takes joined by a hidden cut as a muffler rolls across the floor. The studio was too small for one take. The "606 takes" was a clapperboard joke ([Campaign](https://www.campaignlive.co.uk/article/feature-making-honda-cog/181579), [Snopes](https://www.snopes.com/fact-check/cog/)) | Even the canonical "one take" is stitched. Hide the seam on a moving object |
| **Old Spice "The Man Your Man…"** (2010) | Shower → boat → horse in one take | Practical transitions: a set pulled away on a crane, a shirt dropped from a rig, an actor lowered onto the horse as the camera pulls back ([Wikipedia](https://en.wikipedia.org/wiki/The_Man_Your_Man_Could_Smell_Like), [Creative Review](https://www.creativereview.co.uk/an-oral-history-of-the-old-spice-ads/)) | The *world changes around a continuous camera*. Seedance one-takes do exactly this |
| **Johnnie Walker "The Man Who Walked Around the World"** (2009, 6 min) | A true single take | Steadicam on a rickshaw. Built so "no invisible cuts" could hide; take 40 was the last one ([Campaign](https://www.campaignlive.com/article/johnnie-walker-the-man-walked-around-world-bbh-london/926327), [Muse](https://musebyclios.com/advertising/inside-johnnie-walker-and-robert-carlyles-brand-film-for-the-ages/)) | One walking pace and one direction make 6 minutes feel short |
| **Guinness "noitulovE"** (2005) | Continuous backwards journey through evolution | Mixed sources (location, studio, stock, stills, CG) unified in post by Framestore ([Wikipedia](https://en.wikipedia.org/wiki/NoitulovE)) | Continuity is made in post from mixed sources. That is our situation |
| **Nike "You Can't Stop Us"** (2020) | 36 split-screen match cuts | About 4,000 clips searched, 72 sequences chosen; editors "eye-matched" pairs ([Working Not Working](https://magazine.workingnotworking.com/creative-work-blog/you-cant-stop-us-nike-ad)) | Motion matching alone creates flow between unrelated scenes |
| **Apple HomePod "Welcome Home"** (2018) | One apartment that stretches and transforms | Hydraulic, practical set; little CGI ([PetaPixel](https://petapixel.com/2018/03/26/how-apples-welcome-home-ad-was-made-with-practical-effects-not-cgi/)) | One space transforming beats cutting between spaces |

---

## 4. ffmpeg recipes for the pipeline (tested on ffmpeg 6.1)

`reel-studio` already has `whip`, `zoom_through`, `spin`, `velocity` ramps and `sfx_on_cuts`; use them. Below is only what it lacks for **AI chains**. Assume 24 fps; one frame = 0.0417 s. Normalise every clip first with `fps=24` and the same size.

**R1. Exact hand-off frame, plus the sharpest frame among the last ten** (for sequential chains):
```bash
N=$(ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -of csv=p=0 A.mp4)
ffmpeg -i A.mp4 -vf "select=eq(n\,$((N-1)))" -frames:v 1 -update 1 A_last.png        # lossless PNG, never JPG
ffmpeg -sseof -0.5 -i A.mp4 -vf "blurdetect=block_width=32:block_height=32,metadata=print:file=blur.txt" -f null -
```
- Lower `lavfi.blur` means sharper. If the sharpest frame is not the last one, cut A at that frame and use it as B's start [V1].

**R2. Join without the double frame.** In a shared-keyframe chain, B's first frame repeats A's last frame and causes a one-frame hitch [inf]. Drop it:
```bash
ffmpeg -i A.mp4 -i B.mp4 -filter_complex "[1:v]trim=start_frame=1,setpts=PTS-STARTPTS[b];[0:v][b]concat=n=2:v=1:a=0[v]" -map "[v]" AB.mp4
```
- In a reel-studio spec, the same thing is `"in": 0.042` on clip B.

**R3. Find and trim dead holds** (the settle at the end, the static start):
```bash
ffmpeg -i A.mp4 -vf "freezedetect=n=0.003:d=0.3" -f null - 2>&1 | grep freeze_
```
- Test: a 2 s clip plus a 1 s hold reported `freeze_start: 1.958`. Cut there; mid-chain also trim 0.2–0.4 s of ease-in from B [inf].

**R4. Seam colour match.** Measure the last six frames of A and the first six of B:
```bash
ffmpeg -sseof -0.25 -i A.mp4 -vf "signalstats,metadata=print:file=-" -f null - | grep -E "YAVG|UAVG|VAVG|SATAVG"
```
Then correct B at the seam and **fade the correction out over 1 s**, so B ends on its own grade without a visible shift:
```bash
ffmpeg -i B.mp4 -vf "eq=brightness='-0.04*max(0,1-t/1.0)':saturation='1-0.1*max(0,1-t/1.0)':eval=frame" Bfix.mp4
```
- Convert the YAVG difference to `brightness` with ΔY/255 [inf]. For hue shifts, use `colorbalance`.

**R5. Heal a seam with motion interpolation.** Delete the frames around the join and let `minterpolate` synthesise new ones from both sides. The gap in the timestamps is what it fills:
```bash
# AB.mp4: A = frames 0-71, B starts at 72. Remove 70-73 and regenerate them.
ffmpeg -i AB.mp4 -vf "select='not(between(n,70,73))',minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1:scd=none" healed.mp4
```
- Keep `scd=none`, or the scene-change detector refuses to interpolate across the cut.
- This works for small mismatches (position or scale off by a few percent). For large ones it smears, so cover it with R6 or R7 [inf].

**R6. Whip seam.** Use reel-studio `"transition":"whip"`. Raw variant:
```bash
ffmpeg -i A.mp4 -i B.mp4 -filter_complex "[0:v][1:v]xfade=transition=slideleft:duration=0.25:offset=2.75,dblur=angle=0:radius=40:enable='between(t,2.62,3.12)'[v]" -map "[v]" whip.mp4
```
- Avoid `tmix` with `enable=`. reel-studio's T6 notes record chroma corruption; window it with trim+concat instead.
- Pro version: 10 frames centred on the cut, eased keyframes, mirrored edges, motion blur [V17]; direction matches the camera motion [inf].

**R7. Continuous speed ramp through a seam.** For one-off renders outside reel-studio, the exact `setpts` integral for 1× → S× → 1× with linear ramps:
```python
def ramp_expr(t0,t1,t2,t3,S):          # source seconds; output time = ∫ dt / speed
    a=(S-1)/(t1-t0); b=(1-S)/(t3-t2)
    o1=f"({t0}+log({S})/{a})"; o2=f"({o1}+({t2}-{t1})/{S})"; o3=f"({o2}+log(1/{S})/{b})"
    return (f"if(lt(T,{t0}),T,if(lt(T,{t1}),{t0}+log(1+{a}*(T-{t0}))/{a},if(lt(T,{t2}),{o1}+(T-{t1})/{S},"
            f"if(lt(T,{t3}),{o2}+log(1+{b}*(T-{t2})/{S})/{b},{o3}+(T-{t3})))))/TB")
```
```bash
ffmpeg -i AB.mp4 -vf "minterpolate=fps=96:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,setpts='<expr>',fps=24" ramped.mp4
```
- Tested: a 3 s clip with a 4× peak became 2.083 s, as predicted.
- Centre the peak on the seam. Typical settings are 400–500 % for 4–8 frames [V4, V5], with directional blur keyed only while moving (2–3 % in Premiere) [V4].

**R8. Seam QC.** Compare A's last frame with B's first frame:
```bash
ffmpeg -i A_last.png -i B_first.png -lavfi "ssim;[0:v][1:v]psnr" -f null -
```
- In a shared-keyframe chain, expect SSIM above about 0.9 [inf]. Unrelated frames scored 0.24.
- Add this to G-continuity in 18.

---

## 5. Blueprint: a 20 s "continuous film" for one product (9:16)

### 5.1 Plan the seams before any prompt: the seam sheet
For each seam K_i record: frame content; subject position (x, y, size); **camera velocity** ("right, walking pace"); light direction and colour; focus; seam type (shared keyframe / occlusion / whip / match cut). The velocity clause is pasted word for word into *both* adjacent prompts: "…arriving moving right at walking pace" and "already moving right at walking pace from the first frame" [inf].

### 5.2 Shot plan: one impossible camera, five clips, six keyframes

| t (s) | Clip | Start → end frame | Camera (one direction family) | Seam into the next |
|---|---|---|---|---|
| 0–4 | 1 | K0 wet stone, drop in the distance → K1 amber fill (inside the drop) | Glides forward, accelerates into the drop | **Occlusion.** K1 is plain amber blur, so the seam is invisible |
| 4–8 | 2 | K1 → K2 bottle on a bathroom shelf, mid-frame left | Pulls back out of amber, drifts right | Shared keyframe, moving right |
| 8–11 | 3 | K2 → K3 hand mid-lift, bottle centre | Continues the right arc, rises | Shared keyframe plus a **ramp peak** (R7) |
| 11–15 | 4 | K3 → K4 dropper at the skin, macro | Tilts up with the bottle, push-in | **Match cut** on the drop shape (an echo of K0) |
| 15–20 | 5 | K4 → K5 packshot (`last_image_url`) | Eases back and **settles**; hold 1.5 s for the logo | End |

Reversing direction at 4 s is allowed inside the occlusion (*Rope*'s dolly-in → dolly-out) [V11].

### 5.3 Steps
1. **Stills.** Generate the master still with Flare. Derive K0–K5 from it with Flare i2i, including "keep identical light, lens and grade". K1 can be an ffmpeg-graded solid or blur frame from K2.
2. **Previs at about $1.25.** Run `alibaba/wan-3.0/image-to-video` at 480p, $0.05/s, with `end_image_url` for each pair. Check direction, timing and the seam idea, then fix the sheet.
3. **Hero clips.** Run Kling 3.0 pro i2v per clip with prompt 2.1, `sound:"off"`, duration 5 s (trimmed to about 4 s later). Run clips in parallel. Make 2 takes of the two hardest clips.
4. **Assemble.** R3 trim → R2 dedupe → R4 colour → R5 heal → R7 ramp the two biggest seams (or use reel-studio `velocity`) → R8 QC. Grade (08) and run the film chain (06).
5. **Sound.** One bed, one room tone, a riser across 7–9 s, a hit on the packshot, whooshes on the ramps (13 for ElevenLabs).
6. **Alternative A (one-take).** A single Seedance 2.5 i2v from K0 with prompt 2.2 (15 s, 720p). Then take its last sharp frame to K5 with a Kling `last_image_url` landing. Generate both versions and A/B them with the client [inf].

### 5.4 Costs (list prices from 12; no money was spent on this research)

| Item | B: keyframe chain | A: Seedance one-take |
|---|---|---|
| Stills: master + 5–6 keyframes, about 2 tries each, Flare ≈ $0.30 | ≈ $3.60 | ≈ $1.20 (start + packshot) |
| Previs: Wan 3.0 480p | 5 × 5 s = $1.25 | 15 s = $0.75 |
| Hero video | Kling pro 5 × $0.476 = $2.38, + 2 retakes ≈ $0.95 → **$3.33** | Seedance 2.5 720p 15 s = $6.93 × 2 takes = **$13.86**, + Kling packshot landing $0.48 |
| Optional: Seedance video-extend to fix one second | — | about $0.277/s in + out |
| **Total** | **≈ $8–9** | **≈ $16–17** |

The B chain is cheaper and keeps the product exact at every seam. A gives the most organic motion, at about twice the cost and with more risk to product fidelity. 1080p Seedance ($1.137/s) more than doubles A, so upscale in post instead (12) [inf].

---

## 6. Flow QC (run on the assembled cut before the client sees it)
1. Watch muted at 1×: no stop-start at any seam (R3 found no freeze inside the film).
2. Watch at 0.25× around each seam: no one-frame hitch (R2), no colour click (R4), SSIM at the seam ≥ 0.9 (R8).
3. Draw the camera direction per shot on the seam sheet: no unexplained reversals.
4. Eye-trace: the subject's centre moves less than about 15 % of the frame width across each cut [inf].
5. Audio: one bed, with no room-tone change at the cuts.
6. Rhythm: shot lengths are not all equal, and the hold lands on the reveal.
7. Product: identical label and cap in K0–K5 (18 G-continuity).

---

## Sources
**YouTube (transcripts read in full or searched by passage):**
[V1] https://youtu.be/6iBc4aoiwf4 · [V2] https://youtu.be/jeYMKuce00k · [V3] https://youtu.be/JjDk5Rp7lqU · [V4] https://youtu.be/eKC4z7OGw60 · [V5] https://youtu.be/4N_rE8N8O_M · [V6] https://youtu.be/bxmMTa905_8 · [V7] https://youtu.be/SvhFnN-axJw · [V8] https://youtu.be/aMLKJQYr1Pk · [V9] https://youtu.be/ikPGQGoUjQ0 · [V10] https://youtu.be/aOmK_qwX_WQ · [V11] https://youtu.be/lFZGmzsvSlg · [V12] https://youtu.be/F8Qx3XKvvpw · [V13] https://youtu.be/zK-S_ZCdeQE · [V14] https://youtu.be/ptXlYulVAsM · [V15] https://youtu.be/J0ydlAqg6_8 · [V16] https://youtu.be/eyH-a964kAs · [V17] https://youtu.be/EhuzWg7XsF0 · [V18] https://youtu.be/ZFolxPFgU8A · [V19] https://youtu.be/KrEO2Hzv-PY

**Web:**
[W1] https://kling.ai/quickstart/klingai-video-3-model-user-guide · [W2] https://kling.ai/quickstart/ai-video-start-end-frames · [W3] https://www.hedra.com/blog/directing-seedance-2-5-with-beats · [W4] https://www.opus.pro/blog/one-shot-continuous-video-seedance · [W5] https://mer.vin/2026/06/draw-camera-paths-on-images-flora-seedance-fpv-drone-motion-control/ · [W6] https://help.descript.com/hc/en-us/articles/40593605735309 · [W7] https://chatcut.io/blog/seedance-2-0-prompts-examples
- Artlist 360 case study (search snippet only): https://artlist.io/blog/
- ffmpeg filter docs (xfade, minterpolate, dblur, blurdetect, freezedetect, signalstats, eq, ssim): https://ffmpeg.org/ffmpeg-filters.html

**Tooling note:** `fetch_yt.py` now hits YouTube's bot check; adding `--extractor-args youtube:player_client=web_embedded --ignore-no-formats-error` to its yt-dlp call restores subtitles (51/66 fetched).
