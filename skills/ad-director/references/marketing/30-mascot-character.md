# 30 — Mascot Character: a weird, consistent "AI influencer" as the studio's face

Researched 2026-10-08. This file builds on 12 (Higgsfield API), 13 (ElevenLabs), 17 (stills factory), 22 (backlash) and 26 (world bible), and does not repeat them.
Our own inferences are marked **[inf]**. **[T]** = tested on this machine today. Prices are free `/estimate` calls from 2026-10-08 (list USD, before the 15 % Kling discount) or 12 §1. We spent no money.

## 0. The ten rules

1. **A mascot is a fluent device.** Campaigns with one are ~30 % more likely to grow profit and 37 % share (System1/IPA, vendor data); only ~4 % of US ads use one [S1].
2. **One exaggerated feature, everything else ordinary.** The weird part is the brand code. Ordinary skin, clothes and posture keep it "human-looking" and stop it reading as a cheap filter [inf, from H1 "Distinctive beats polished in the feed"].
3. **Pick a feature that hides the mouth, or is not human.** Mouths are where lip-sync breaks (teeth blur, smudged lips [L1][L2]) and human faces are where AI backlash starts (Toys"R"Us smile, McDonald's grandma; 22 §5). A giant moustache or a frog head dodges both [inf].
4. **Personality before pixels.** Duo is "sassy and fiercely loyal" with a split persona: "unhinged" on social, a "helpful coach" in-app [D1][D2]. Write the want, the flaw and one behaviour (26 §2.7) before generating anything.
5. **Lock identity in three layers.** (a) a master sheet (turnaround + expressions), (b) a verbatim anchor block in every prompt, (c) a trained ID (Soul ID) and start frames for every video. No single layer holds on its own [inf].
6. **No text-only video.** Every clip starts from an approved still; loops end on it (`last_image_url`).
7. **Generate on a flat key colour, ship with alpha.** WebM VP9 alpha (Chrome/Firefox) + HEVC alpha or stacked alpha (Safari). Tested here in §5.
8. **One voice ID forever.** Design the voice once, save it, freeze the settings and write a voice bible. The voice survives redesigns; the face may not.
9. **Disclose.** EU AI Act Art. 50 transparency applies from Aug 2026 [E1]; hidden-AI reveals drew backlash [M1][H4]. Say "AI character" in bio and site.
10. **Rules beat taste.** Freddie "always faces right, and he always winks" [F1]. Police five never-break rules in QC.

## 1. What makes mascots last

| Case | What worked | What we steal |
|---|---|---|
| **Old Spice Man** (W+K, 2010) | Direct-to-camera absurd escalation aimed at the real buyer (60 % of body wash bought by women) [O1]; sales +60 % by May, doubled by July 2010 (agency claim) [O2]; 186 reply videos in 2.5 days [O1]. | Deadpan absurd to camera; a repeatable **reply-video format** for social. |
| **Duolingo Duo** | Influencer-like: trend sounds, feuds, the 2025 "death" stunt [D1][D3]; "wholesome unhinged": wacky on social, coach in-app [D2]. | Two registers, one stable design. |
| **Mailchimp Freddie** | Simplified in the 2018 rebrand; hard usage rules [F1][F2]. | A rule sheet; a silhouette that reads at 64 px. |
| **Lil Miquela** (Brud) | Novelty, then backlash over the "fake" reveal and borrowed trauma stories; engagement faded [M1][M2]. | **Never claim real experiences**; openly AI. |
| **Higgsfield AI Influencer** | Menu-built studio: Average/Bold/Extreme unusual features ("jug ears", "hair horns", "gold grill"), human or non-human; returns close-up + full body; animated via Genjutsu and Lipsync Studio [H1][H2][H3]. Its shock-led launch marketing drew backlash [H4]. | A **$0.05 sketchpad**, not the pipeline. Weird ≠ offensive. |

**Recurring components [inf]:** a silhouette that reads in black fill (the weird feature *is* the silhouette); a want; a flaw that powers jokes; one signature gesture (Freddie's wink); 3–5 catchphrases, max one per piece; a voice bible (timbre, wps, vocabulary, banned words, brand-name read, laugh).

## 2. Consistency: the identity stack

### 2.1 The tools on our API (verified 2026-10-08)

| Job | Endpoint | Price | Notes |
|---|---|---|---|
| Concept sheets | `higgsfield/ai-influencer` | **$0.05** per sheet (estimate; `GET /models`: "Human and animal modes") | `input_schema: null`, not in public docs: use the web studio or probe first [T] |
| Identity training | `POST /v1/custom-references` (Soul ID) | 40 cr ≈ **$2.50** | `model_version` **cinema**, 1–100 images, poll to `completed` [H5]; "20 or more photos" [H2] |
| Plates with the character | `higgsfield-ai/soul/cinema` + `custom_reference_id` | $0.022 per batch 4 @1080p | Soul ignores image refs (12), so Soul ID is the only way in |
| Sheet / pose edits | `marketing-studio/image/flare` | ≈$0.14 (1k medium) – $0.30 (2k high) | 16 refs, holds identity (12) |
| Cheap surgical edits | `alibaba/qwen-image-3/edit` | **$0.040** (estimate today; 12 listed $0.075) | `prompt_extend:false` (17) |
| Clip from still | `kling-video/v3.0/std/image-to-video` | 3 s $0.215 · 4 s $0.286 · 5 s $0.357 (sound off) | `last_image_url` for loops; pro $0.476 for hands |
| Refs + first/last frame | `kling-video/o3/image-reference` | std 5 s $0.357 | sheet in `image_urls` + first/last frame |
| Talking, audio-driven | `bytedance/seedance-2.5/reference-to-video` | $0.206/s 480p · $0.462/s 720p | `audio_urls` ≤10, `image_urls` ≤30, no seed |
| Cheaper talking | `bytedance/seedance-2.0/reference-to-video` | ≈$0.136/s 480p · $0.302/s 720p (12) | refs ≤9 img/3 vid/3 audio |
| Founder's motion → character | `higgsfield/genjutsu/motion-transfer/v1.0` | **$0.318/0.681/1.632 per input s** | source ≥4 s, 1–8 refs, keeps source audio [H5] |
| Same, Kling | `kling-video/v3/motion-control/{std,pro}` | estimate → HTTP 500; priced on a real call | video 3–30 s; `character_orientation` video (≤30 s); `keep_original_sound:"no"` [H5][K1] |
| Previs | `alibaba/wan-3.0/image-to-video` | $0.05/s 480p | blocking only |

Web only (no `/models` slug [T]): **Lipsync Studio** (Speak 2.0, Kling Lipsync, Sync Lipsync 3, InfiniteTalk, Kling Avatars 2.0) [H3] and **Kling Elements** (12 §2).

### 2.2 Workflow: from concept to locked identity

1. **Concept** (web AI Influencer, or `ai-influencer`):
   - 2 sheets per concept at "Bold". "Extreme" for the one weird feature only.
   - Keep the base ordinary: a scar or asymmetric freckles read as "someone specific" [H2].
2. **Master still.** Pick one. Re-render it at 2k with Flare on plain mid-grey: full body, neutral A-pose, flat even light. This is **image M**, the source of truth.
3. **Turnaround sheet** (Flare 2k, 16:9, ref M): 5 views, same scale, one baseline.
4. **Expression sheet** (Flare, ref M): a 3×3 grid as in 17 §2:
   - The weird feature must *act* in each panel (tips droop, spring up): a performer, not a prop [inf].
5. **Training set** (20–30 images). Vary angle, expression, light, framing; **never** wardrobe or the feature, or the ID learns drift [inf].
   - Sheet crops + 12–16 Qwen edits of M (angle, expression, 3 lights, close/medium/full).
6. **Soul ID** `model_version:"cinema"`.
   - Test one Soul Cinema batch of 4; judge vs M (17 §5): face, feature ratio, wardrobe. Retrain once if < 3/4 pass.
7. **Asset registry** (in the bible):
   - M, sheets, Soul ID `id`, seeds, `voice_id`. Download at once: outputs live ≥7 days (12).

### 2.3 Prompt anchoring

One **CHARACTER LOCK** block, verbatim, first in every prompt; only the action line changes:
- Use physical nouns plus proportions ("moustache span = 1.6× shoulder width"), not adjectives ("huge").
- Name wardrobe materials and colours (26 §2.1).
- List 3–5 things that never change.
- Add "same person as the reference images; do not restyle" and, for refs, "<<<image_1>>> = identity and wardrobe ONLY, NOT lighting, NOT background" (12 F).

Keep it ≤60 words; long locks crowd out the action [inf].

### 2.4 Motion transfer from the founder (no face)

The founder records the performance on a phone: points, reach, wave, peek. Two routes:
- **Kling 3 motion-control:** the character image plus the founder's video.
  - Kling/Runway guidance: one person, continuous shot, no cuts, no camera moves, not too fast, "upper body or full body including all limbs and head" [K1][K2].
  - The Element library for motion control "only uses facial information" [K2].
- **Genjutsu motion transfer:** image refs plus the founder's video. It costs 5 s × $0.318 = **$1.59 at 480p** and $3.41 at 720p, and it keeps the source audio.

**Facelessness.** The models want a head in frame [K1], so film the founder with the face covered (plain mask/balaclava) or from behind; or crop at the chin and test one clip first [inf]. The character image supplies the face; delete the source after use. (A face-visible private read would carry real mouth motion [Y2], but uploads the founder's face: explicit consent only.)

**Worth it** only for timed gestures (the reach, UI-synced beats); idles, nods and waves are cheaper prompted from a start frame [inf].

**Phone capture [inf]:** 1080p30 on a tripod, plain wall, even light, a vest like Otto's, 6–8 s per move with 1 s of stillness at each end (loop handles).

### 2.5 Lip-sync: options, risks, alternatives

| Option | Where | Risk |
|---|---|---|
| Seedance 2.5/2.0 r2v with the ElevenLabs file in `audio_urls` | API | The voice may be re-performed or drift; no seed. Practitioners: lines of 5–10 words, a mushy mouth past ~8 s, keep the head still and the camera locked [L3] |
| Lipsync Studio (Speak 2.0, Kling Lipsync, Sync 3, InfiniteTalk) | Web only | Mouth added "after the fact" [H3]. Typical failures: blurry or frozen teeth, smudged lips when the face is <10 % of frame, tracking loss when a hand or hair crosses the mouth [L1][L2] |
| Kling motion-control driven by a private founder read | API | The founder's face is uploaded to the vendor. Mouth shapes follow the driver video, not the VO, so align them in the edit [Y2][inf] |
| Native Seedance/Veo dialogue voice | API/web | Not our ElevenLabs voice. Breaks rule 8 |

**Alternatives that avoid the risk (rank order) [inf]:**
1. **Mouth hidden by design.** A Kling "talking" body loop (gestures, cheek bob, moustache bounce on beats) under the ElevenLabs VO; viewers read sync from rhythm, not visemes.
2. **Non-human mouth.** A frog's wide lipless mouth only needs open/close. Lip-sync errors look like character, not glitches.
3. **Off-screen VO + reaction cuts.** The character listens, reacts and points while the voice runs; this is the Old Spice cadence of action beats.
4. **Real lip-sync only for social talking-heads**, ≤8 s per generation, face 15–40 % of frame, stitched at cuts. Always QC at 100 % on the teeth.

### 2.6 How creators keep 20+ clips consistent (transcripts + web)

Common thread: **build assets first, then reference them in every generation**: "build three assets first and once those are locked in, every generation we run is going to reference them directly… the part… most people skip"; train on a clear front or ¾ portrait; use multi-shot Seedance to cut seams [Y1].

Our earlier studies (22 §3.8) say the same: PJ Ace took "6 hours to lock two realistic characters" and builds "a sheet once and reference[s] it in Seedance r2v". Kling 3.0 Elements bind a multi-angle/emotion set so the face stays "recognizable… even when the action involves full head turns" [K2]. The Elements route is web only for us.

Kling motion-control tutorials (fetched today): 3.0's upgrade is "facial consistency and quality", with "real lip sync with incredible facial expressions" carried from the driver [Y2]; build the character still to **match the driver's pose, framing and clothing**, orientation = video (≤30 s) [Y3]; Elements auto-make "three completely new angles" [Y2].

**Our protocol for 15+ clips [inf]:** every start frame is an edit of M; one light, one lens (50 mm, chest height); 4–5 s, one move, trim to the best 2–3 s; one session; then a **contact-sheet QC** (first/middle/last frame of every clip side by side).

## 3. Web delivery with transparency

### 3.1 Generate on a key colour
- Green `#00B140`; **blue `#0047BB`** for a frog or green wardrobe. Restate the backdrop in every video prompt ("background stays perfectly flat and unchanged"): video models reinvent backgrounds [inf].
- Ask for a **soft rim light** to separate hair/moustache edges from the key; `despill` removes skin spill [T].

### 3.2 Matting (tested: 4 CPU, no GPU, onnxruntime 1.30; no rembg/torch/OpenCV installed) [T]

| Method | Speed (CPU, 720×1280) | Use |
|---|---|---|
| ffmpeg `chromakey=0x00B140:0.12:0.06,despill=type=green` | ~5 fps including VP9 encode | Default. Tune similarity 0.08–0.15 per clip |
| **RobustVideoMatting** mobilenetv3 ONNX (15 MB) | **130 ms/frame** → a 5 s 24 fps clip in ~16 s | Hair/moustache edges, non-key backgrounds; temporal, so no flicker [inf] |
| rembg `u2netp` ONNX | 306 ms/frame at 320² | Stills (flickers on video) [inf] |
| BiRefNet-lite (swin-tiny) ONNX | **20 s/frame** at 1024² | Stills: sheets, posters |

Hybrid [inf]: chromakey core alpha, RVM `max`-merged on the hair band. `rembg` 2.0.85 is pip-installable.

### 3.3 Encode (all commands tested here [T])

```bash
# VP9 alpha (Chrome/Edge/Firefox)
ffmpeg -i clip_green.mp4 -vf "chromakey=0x00B140:0.12:0.06,despill=type=green,format=yuva420p" \
  -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 34 -row-mt 1 -auto-alt-ref 0 -an clip.webm
# Verify: ffprobe shows TAG:alpha_mode=1. Decode with -c:v libvpx-vp9; the native decoder drops alpha.

# Stacked alpha (colour on top, alpha below) for Safari/any browser via WebGL
ffmpeg -i clip_green.mp4 -filter_complex "chromakey=0x00B140:0.12:0.06,despill=type=green,format=yuva444p,\
split[m][a];[a]alphaextract[a];[m][a]vstack,format=yuv420p" -c:v libx265 -crf 30 -preset slow -tag:v hvc1 -an clip_stacked.mp4

# Masters: ProRes 4444 (yuva444p10le) keeps alpha for editors; animated WebP keeps alpha for tiny pop-ups
ffmpeg -i clip_green.mp4 -vf "chromakey=…,despill=type=green,fps=12,scale=360:-2" -c:v libwebp_anim -q:v 70 -loop 0 pop.webp
```

**No HEVC-alpha from this Linux box:** ffmpeg 6.1 `libx265` accepts `yuva420p` then **silently writes `yuv420p`** [T]. FFmpeg 8.0 added HEVC alpha [W4] (encoder/Safari playback unconfirmed); Apple-native files come from macOS (Compressor, `avconvert`, `hevc_videotoolbox`, the last ~2× Compressor's size [W1]). Default plan: **VP9 WebM + stacked-alpha** (the `<stacked-alpha-video>` web component; stacked AV1 460 kB vs VP9 1.1 MB vs HEVC-alpha 3.4 MB in his test) [W1].

**Markup** (HEVC first when you have it; Safari plays VP9 but not its alpha) [W1][W2]:
```html
<video autoplay loop muted playsinline poster="idle.webp">
  <source src="idle.mov" type='video/quicktime; codecs="hvc1"'>
  <source src="idle.webm" type="video/webm">
</video>
```

**Size targets [inf, W2 + our encodes]:** idle 5 s 720×1280 ≤1.5 MB; pop-ups 360–480 px ≤300 kB, lazy-loaded; no audio track (VO via `<audio>` after a click). Our 4 s synthetic test: VP9 71 kB, stacked HEVC 37 kB, stacked AV1 14 kB (far simpler than real footage), APNG 13.9 MB (never).

### 3.4 Seamless loops
1. `image_url` = `last_image_url` = same keyframe; drop the final frame [inf].
2. Seam left? Crossfade tail into head, `xfade=fade:duration=0.5` (4 s → 3.5 s loop) [T][W3].
3. Ping-pong only for breathing idles; reversed gestures look wrong [inf].

The idle clip is the hub. Every pointing and talking clip **starts and ends on the idle keyframe**, so the site can cut between clips on any loop boundary with no pop [inf].

## 4. Character bible template (copy per character)

```
NAME / ROLE: [name], the studio's [role]. One-line: "[who they are in 12 words]"
STATUS: openly AI character. Bio line: "AI-generated director at [studio]."
SILHOUETTE: [black-fill description that reads at 64 px]
THE ONE WEIRD FEATURE: [what] · size ratio [x× head/shoulder] · colour/material · how it moves/acts per emotion
CHARACTER LOCK (≤60 words, verbatim in every prompt): [...]
NEVER CHANGES: face shape · feature size · wardrobe items/colours · [prop] · handedness
WARDROBE: [items as materials + colours]; social variants allowed: [list]; banned: logos, other greens/blues (key colour)
PALETTE: dominant / secondary / accent (accent = only on [feature/prop])
PERSONALITY: want · flaw · 3 tone words / 3 anti-words · signature gesture · how they react to failure
REGISTERS: website (helpful, ≤12 words a line) vs social (chaotic, trend-aware)
VOICE BIBLE: voice_id · model eleven_v4 (or v3) · stability/similarity · 1.7–2.2 wps · pronunciations · allowed tags · banned words · laugh
CATCHPHRASES (≤5) + rotation rule (max 1 per piece, never 2 pieces in a row)
DO / DON'T (5 each)
ASSET REGISTRY: M url · sheet urls · Soul ID id · seeds · keyframe set · voice_id · key colour
QC GATES: lock matches M (face, feature ratio, wardrobe) · hands 5 fingers · no text/logos · edge halo < 2 px · loop seam invisible · disclosure present
```

## 5. Three concept directions

### A. "OTTO" — the weird director (recommended)
- **Look.** Tall, lean man in his mid-50s. Long pale face, deep-set grey eyes, heavy brows, swept-back salt-and-pepper hair, real skin texture.
- **Weird feature.** An ENORMOUS charcoal-black waxed handlebar moustache, 1.6× shoulder width, **fully covering the mouth**. It acts: droops in disappointment, springs up for "CUT!".
- **Wardrobe.** Black ribbed turtleneck, tan waxed-canvas many-pocket vest, silver viewfinder on a lanyard, dark trousers; signal-red accent only on a tiny tally-light pin.
- **Personality.** Theatrical auteur who treats a 6-second ad like an epic. Want: cinema in every frame. Flaw: vanity about the moustache. Tone: deadpan, generous, exacting; NOT smug, mean, hype. Gesture: finger-frames the viewer.
- **Voice.** Low resonant baritone, dry gravel, slow with theatrical pauses, warm underneath.
- **ElevenLabs Voice Design.** `POST /v1/text-to-voice/design`:
  - `model_id:"eleven_ttv_v3"`, `guidance_scale:5`, `loudness:0.5`, a fixed `seed`.
  - `voice_description`: "Native English speaker, male, mid-fifties. Low, resonant baritone with a dry, slightly gravelly texture. Slow, deliberate pacing with long theatrical pauses before key words; deadpan and wry, warm underneath, like a film director calmly addressing a crew. Studio-quality recording."
  - `text` (100+ chars): "Quiet on set. ... Six seconds. That's all we get. So every frame has to mean something. Again — with feeling. ... Cut. That's the ad."
  - TTS v4, stability 0.5, `...` at cuts; avoid the word "accent" (dialect drift) [V1].
- **Catchphrases:** "Again. With feeling." · "Cut. That's the ad." · "Six seconds. Make them feel it." · "Frame it." (finger-frame)
- **Do:** finger-frame and point; move the moustache on emphasis; speak ≤12 words a line on the site; react to the UI as if it were a set.
- **Don't:** show his mouth; let the moustache change size or colour; dress him in a beret, cliché accents or a megaphone; mock clients' ads; claim real film credits.

### B. "MARGO" — the producer with the tower wig
- **Look.** A woman in her late 30s with a sharp, friendly face, freckles and reading glasses on a chain.
- **Weird feature.** A **1.2 m sculpted platinum beehive wig** that stores things: pencils, a clapper, a tiny drone that flies out of it.
- **Wardrobe.** Cobalt boiler suit, white trainers, a headset.
- **Personality.** Hyper-competent fixer, warm-sarcastic. Want: ship on time. Flaw: compulsive multitasking.
- **Voice.** Bright, quick, crisp mid-range female voice, 2.3 wps, a smile in the voice.
- **Voice Design:** "Native English speaker, female, late thirties. Bright, crisp mid-range voice, quick confident pacing, playful and warmly sarcastic, clear articulation, like a film producer talking fast on set. Studio-quality recording." `guidance_scale` 5.
- **Catchphrases:** "Locked. Next." · "It's in the wig." · "We ship Friday."
- **Do:** pull a prop from the wig. **Don't:** change wig height; use green/blue; lip-sync >8 s (visible mouth = **highest lip-sync risk**).

### C. "HOPPER" — frog head, perfect suit
- **Look.** Human body and hands; tailored oatmeal linen suit, cream shirt, knit tie. Key on **blue**.
- **Weird feature.** A **realistic tree-frog head**: wet olive skin, gold eyes, slow nictitating blinks.
- **Personality.** Serene, unblinking client-success rep: polite, precise, faintly eerie. Want: calm clients. Flaw: takes everything literally.
- **Voice.** Soft, warm, low-mid male voice with precise diction, unhurried at 1.6 wps; one tiny throat-click allowed via SFX, never a "ribbit".
- **Voice Design:** "Native English speaker, male, forties. Soft, warm, low-mid voice with very precise diction; calm, unhurried, polite and slightly uncanny stillness, like a luxury hotel concierge. Studio-quality recording." `guidance_scale` 4.
- **Catchphrases:** "Breathe. We've got this." · "Leap when ready." · "Noted."
- **Do:** long still stare, one slow blink. **Don't:** go cartoon-cute; >1 frog pun per piece; show the tongue. Non-human mouth forgives lip-sync errors (rule 3).

**Recommendation: Otto.** The studio's job as a person; the moustache is the 64 px silhouette and removes lip-sync; deadpan absurd is the tone AI carries best (22 §3.15). Hopper is the non-human fallback.

## 6. Generation plan for Otto (15 clips, ≈$15)

**Shared CHARACTER LOCK (A1)**
> CHARACTER LOCK: Otto, tall lean man, mid-50s, long pale face, deep-set grey eyes, heavy dark brows, swept-back salt-and-pepper hair, real unretouched skin; ENORMOUS charcoal-black waxed handlebar moustache 1.6× shoulder width, tips curled up, fully covering the mouth; black ribbed turtleneck, tan waxed-canvas many-pocket vest, silver viewfinder on black lanyard. Same person as references; do not restyle.

**Shared BACKDROP + motion line**
> Plain flat chroma-green (#00B140) studio backdrop, evenly lit, no floor line, no shadows on backdrop; soft frontal key, subtle cool rim on hair and moustache; 50mm, chest-height, static locked-off camera; background stays perfectly flat and unchanged.

### Stage A — identity ($3.93)

| # | What | Endpoint | Qty × price | $ |
|---|---|---|---|---|
| A1 | Concept sheets (Otto, Margo, Hopper × 2) | `higgsfield/ai-influencer` (web studio if the API schema is unresolved) | 6 × 0.05 | 0.30 |
| A2 | Master M + turnaround sheet | Flare 2k high, 16:9, ref = chosen sheet | 1 × 0.30 | 0.30 |
| A3 | 3×3 expression sheet | Flare 2k high, ref M | 1 × 0.30 | 0.30 |
| A4 | 12 training variants (angle/expression/light) | Qwen-3 edit, ref M, `prompt_extend:false` | 12 × 0.04 | 0.48 |
| A5 | Soul ID (cinema) on ~22 images | `/v1/custom-references` | 1 × 2.50 | 2.50 |
| A6 | Location test (for later social) | Soul Cinema + `custom_reference_id`, batch 4 | 2 × 0.022 | 0.05 |

**A2 prompt (Flare).** "Image 1 is the character: identity, proportions and wardrobe ONLY. [LOCK]. Character turnaround sheet: five full-body views in one row — front, three-quarter left, left profile, back, three-quarter right — identical scale, feet on one baseline, neutral A-pose, plain mid-grey background, flat even light, no text, no labels."

**A3 prompt.** "[LOCK]. 3×3 expression sheet, chest-up, thin white grid lines, same light: neutral; smug (moustache tips raised); delighted (tips spring up); shocked (moustache flares); sceptical (one brow up); conspiratorial whisper (hand beside moustache); shouting 'cut' (arm chopping); pointing at camera; deadpan stare. Mouth never visible."

### Stage B — keyframes on green ($2.10)

- 15 keyframes plus retakes: Qwen-3 edit, ref M + one sheet panel, 9:16, [LOCK] + [BACKDROP] + pose line. 30 × $0.04 = **$1.20**.
- 3 Flare fixes for hands or the feature ratio: **$0.90**.
- Poses: K0 idle (hands loosely clasped, weight on one leg); K1–K3 point L/R/down; K4 conspiratorial lean; K5 arm extended to lens; K6–K11 pop-up poses; K12 thinking; K13 step-in; K14 nod.

### Stage C — clips ($7.16 + $2.14 buffer)

Every prompt = [LOCK] + [BACKDROP] + an action line. `sound:"off"`, `cfg_scale` 0.5.

| # | Clip | Endpoint | Frames | Action line | $ |
|---|---|---|---|---|---|
| C1 | Idle loop | Kling 3 std 5 s | K0 → K0 | "Breathes slowly, weight shifts once, moustache tips twitch, one slow blink; returns exactly to the start pose." | 0.357 |
| C2–C4 | Point L / R / down | Kling 3 std 5 s ×3 | K0 → K0 | "Raises right arm and points firmly toward frame-left at shoulder height, holds 1 s with a raised brow, lowers arm back to the start pose." | 1.07 |
| C5 | "Talking" body loop (VO over) | Kling 3 std 5 s | K0 → K0 | "Speaks expressively under the moustache: cheeks and moustache bob on beats, open-palm gestures, small nods; mouth never visible; ends in start pose." | 0.357 |
| C6 | Reach out & pull up the site | Kling 3 **pro** 5 s | K0 → K5 | "Steps forward and reaches his right hand straight toward the lens until the open palm fills the lower frame and blurs, fingers close as if grabbing the frame edge and pulling down." | 0.476 |
| C7–C12 | Pop-ups: peek from right edge, rise from bottom, offer hand, wave, finger-frame, thumbs-up + wink | Kling 3 std 4 s ×6 | Kn → Kn | One action each; the entrance/exit is done in CSS (`transform`) so the clips can loop | 1.72 |
| C13–C15 | Thinking loop, step-in, approving nod | Kling 3 std 5 s ×3 | Kn → K0 | as named | 1.07 |
| C16 | Talking hero (social/home hero, 6 s) | Seedance 2.0 r2v 720p 6 s, `image_urls:[M, sheet]`, `audio_urls:[otto_line.mp3]` | — | "<<<image_1>>> is Otto: identity and wardrobe only… locked-off medium shot, he delivers the line with gestures; moustache moves with the words; head mostly still." | 1.81 |
| C16a | Previs for C16 | Wan 3.0 480p 6 s | — | blocking | 0.30 |
| — | Retake buffer | 6 Kling std retakes | | | 2.14 |

**Totals.** A $3.93 + B $2.10 + C $7.16 + buffer $2.14 = **$15.33 list**; with the 15 % Kling discount on this account (≈$1.08) **≈$14.25**.

**Cuts if needed:** defer A5 Soul ID to the social phase (−$2.50); replace C16 with C5 + VO (−$2.11).

**Optional:** C6 via founder's masked reach (5 s): Genjutsu 480p +$1.59, or Kling motion-control (priced on a real call).
**Voice** (ElevenLabs credits, outside the $15): Voice Design → save one; ~20 site lines on v4 (≈0.13 cr/char, 13); `stt-check` each.
**Post (local, free):** trim → `chromakey`+`despill` (RVM on the moustache band if it haloes) → VP9-alpha WebM + stacked HEVC → seam check → contact-sheet QC vs M.
**Order:** A1 → pick → A2/A3 → **human approval** → A4/A5 → K0 → **C1 first** (the hub frame) → C2–C15 in one `hfgen batch` → C16 last.

## Sources

**Brand and mascot**
- [S1] System1 on fluent devices: https://system1group.com/blog/creating-memorable-characters-in-advertising · https://martechseries.com/analytics/behavioral-marketing/memorable-characters-ads-boost-chances-profit-30-just-4-us-brands-using-says-system1/
- [O1] Adweek, Old Spice by the numbers: https://www.adweek.com/agencyspy/the-old-spice-campaign-by-the-numbers/
- [O2] W+K case: https://www.wk.com/work/old-spice-smell-like-a-man-man/
- [D1] Digiday on Duo: https://digiday.com/marketing/how-duolingo-is-using-its-unhinged-content-with-duo-the-owl-to-make-people-laugh-on-tiktok/
- [D2] Campaign, "wholesome unhinged": https://campaignlive.com/article/duolingo-comms-head-sam-dalsimer-leads-wholesome-unhinged-strategy/1910699
- [D3] The Drum: https://www.thedrum.com/news/2025/02/25/duolingo-s-tiktok-mastermind-its-unhinged-social-strategy-and-killing-its-mascot
- [F1] Brandastic, quoting Freddie's guide (second-hand): https://brandastic.com/?p=11121
- [F2] Brand New Mag, 2018 rebrand: https://www.brandknewmag.com/see-mailchimps-weird-new-branding/
- [M1] Elle SG, "the fall of the AI influencer": https://elle.com.sg/life-culture/lil-miquela-the-fall-of-the-ai-influencer/
- [M2] Big Think: https://bigthink.com/?p=46878

**Higgsfield and Kling**
- [H1] Higgsfield, AI Influencer update: https://higgsfield.ai/blog/new-ai-influencer
- [H2] https://higgsfield.ai/blog/how-to-create-ai-influencer · https://higgsfield.ai/creator-hub/help-center/tools/how-do-i-use-ai-influencer
- [H3] Lipsync Studio: https://higgsfield.ai/creator-hub/help-center/ai-models/how-do-i-use-lipsync-voiceover-and-aspect-ratios
- [H4] Forbes on Higgsfield's marketing backlash: https://www.forbes.com.au/?p=177110
- [H5] Higgsfield API docs (Soul ID, Genjutsu, Kling 3 motion control): https://docs.higgsfield.ai/docs/llms-full.txt
- [K1] Runway, Kling 3.0 Motion Control: https://help.runwayml.com/hc/en-us/articles/50280558448147-Creating-with-Kling-3-0-Motion-Control
- [K2] Kling motion-control guide: https://kling.ai/quickstart/motion-control-user-guide · Vercel FAQ https://vercel.com/ai-gateway/models/kling-v3.0-motion-control/faq

**Lip-sync, voice and regulation**
- [L1] HighSync (arXiv): https://arxiv.org/pdf/2605.16918
- [L2] Lip-sync artefact guide (vendor): https://dubly-ai.support.site/article/lip-sync-artifacts-fix-guide
- [L3] Seedance 2.0 audio guide (practitioner): https://www.cutout.pro/learn/blog-seedance-2-0-audio-guide/
- [V1] ElevenLabs Voice Design: https://elevenlabs.io/docs/eleven-api/guides/how-to/voices/voice-design · https://elevenlabs.io/blog/voice-design-v3
- [E1] EU AI Act Art. 50 code of practice: https://www.jonesday.com/de/insights/2026/01/european-commission-publishes-draft-code-of-practice-on-ai-labelling-and-transparency · https://www.medianama.com/2026/06/223-eu-ai-act-deepfake-labeling-rules/

**Web delivery**
- [W1] Jake Archibald, "Video with alpha transparency on the web": https://jakearchibald.com/2024/video-with-transparency/
- [W2] Rotato: https://rotato.app/blog/transparent-videos-for-the-web
- [W3] Video-loop skill (crossfade): https://skills.sh/coroboros/agent-skills/video-loop
- [W4] FFmpeg trac #7965 (HEVC alpha, FFmpeg 8.0): https://ffmpeg.org/pipermail/ffmpeg-trac/2025-August/074238.html

**YouTube**
- [Y1] Isa does AI, "How to Make Long AI Videos with Consistent Characters (2026)": https://youtu.be/dOmKYJoRboE
- [Y2] Sebastien Jefferies, "Kling Motion Control 3.0 Full Tutorial": https://youtu.be/Utono2euM24
- [Y3] Geek Savvy, "How to Create Perfect Kling 3.0 Motion Control Videos?": https://youtu.be/HMDIuf4K7Yk
- Fetched with 45–120 s spacing.
- 4 of 7 attempts had no captions; a third success (Snowball AI, https://youtu.be/sqG1zRyKCO0) only repeated "train once, reference always". Failed: https://youtu.be/4yRZ6X4LF-o (Kling Elements), https://youtu.be/7EcAixgmwUo.
- Transcripts are not committed.

**Our tests**
- `/estimate` and `GET /models` on 2026-10-08.
- Encode/matting benchmarks in the session scratchpad (not committed).
