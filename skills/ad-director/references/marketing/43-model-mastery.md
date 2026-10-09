# 43 — Model mastery: how Seedance 2.5, Kling 3.0, Wan 3.0 and Cinema Studio 4.0 really behave

Researched 2026-10-09. No generation money was spent. Parameters and prices come from the free `hfgen.py schemas` / `estimate` calls against the live Higgsfield API [EST]. Behaviour comes from the Higgsfield docs and blog, ByteDance and Kling pages, 23 YouTube tutorial transcripts (listed in §10), creator prompt libraries, and our own paid-run ledger [LEDGER].
This doc builds on 12 (endpoints and prices), 37 (action execution), 41 (action realism) and 44 (action and comedy craft). It does not repeat them.
**Tags:** each claim carries a source key. The keys resolve to URLs or transcripts in §10. `YT:<id>@mm:ss` points to a transcript timestamp. **[unverified]** means we found no primary evidence. **[inf]** means our own inference from the evidence.

---

## 0. The 12 rules that would have prevented our failures

1. **Action is coverage, not one camera move.** Higgsfield's tested action prompt uses **9 shots in 15 s**, with "snap and whip-pan cuts" landing on impacts and "no transitions" [B-SD25G]. Our F09 heist crammed a BASE jump, a chute, a landing in a moving car and a police stop into one 15 s unbroken drone take [LEDGER/F09 plan]. That is the failure 41 documents.
2. **Fix the shot count in writing.** Seedance adds cuts unless told otherwise. The cure is "Exactly five shots and four cuts — no more, no fewer, no extra inserts" [B-CAR; YT:GNxmt_4IifA]. For one-takes, write "one continuous take… no cuts" explicitly; otherwise "it will just come up with any type of camera angle" [YT:lkL8mlpVScY@18:24].
3. **One reference per thing that must not change, and give each one a job.** Write "identity and wardrobe locked to the reference, ignore the reference backdrop", "Location, as-is from the reference", "The product, inherited exactly from the reference" [B-SD25G]. For video refs: "camera-motion reference ONLY… Nothing else is inherited" [B-SD25VS]. Keep it to about 1–8 distinct subjects [YT:UxwV16jDglA@09:59; ATLAS-SD25].
4. **The tighter the frame, the less slop.** Car shots work as rigged close angles. Wide aerials over traffic fail: cars leave lanes and 120 km/h reads as 60 [YT:GNxmt_4IifA; B-CAR].
5. **Clean the plate.** Remove signage, background clutter and any vehicle that resembles the hero car before animating. Distant cars "were constantly turning into clones of our red car" [YT:GNxmt_4IifA].
6. **No seeds on Seedance, Kling or Cinema Studio via our API** [EST]. A 480p take cannot be re-rendered at 720p. A 480p test validates the *prompt*, not the *take* (§6).
7. **Seedance 2.5 adds music even when told "no music",** above all in fight scenes. Plan to replace the bed, or keep a dominant diegetic sound such as an engine [YT:RpsEdtUJCnU@05:56].
8. **Kling lip-sync and identity degrade after about 10 s.** Put the dialogue in the first 10 s and the action after it [YT:b_RghITuQQM].
9. **For a fixed brand voice, drive the lips with the real audio** (Wan 3.0 r2v `audio_urls`, $0.10/s at 720p). Then re-measure the offset: Wan lags 0.12 s and Seedance led by about 0.3 s in our runs [LEDGER].
10. **Name the physics.** Two tons behaves like two tons: nose dive, body roll, tyre grip. "Realistic controlled slides, never arcade drifting" [B-CAR]. Bodies get "weight transfer, hip shift, toe push-off" [B-SD25G].
11. **Describe start and end positions, not motion adjectives.** "Running" is ambiguous; two body positions are not [B-DIST; B-HANDS; B-MIST].
12. **Script every object's fate.** A cap that flies off disappears unless you write where it lands [YT:GNxmt_4IifA]. A cookie must "only shrink… never regrowing" [B-SD25G]. A drink level must drop [LEDGER].

---

## 1. Model-by-task decision table

| Task | First choice | Settings | Backup | Why (evidence) |
|---|---|---|---|---|
| **Product macro insert** (one move, label must hold) | Kling 3.0 Pro i2v | 5 s, `sound:"off"`, `cfg_scale` 0.5, `last_image_url` to land the packshot | Seedance 2.5 i2v 480p→720p | Kling: one move per shot, and it "keeps signs, captions and logos from an uploaded image" [K-GUIDE]. Our Kling product inserts passed [LEDGER]. Seedance "softened some named on-screen text" [B-ADH] |
| **Product hero one-take** (orbit or push with refs) | Cinema Studio 4.0 | `camera_movement` enum, `pacing:"single-shot"`, `camera_lens:"clean-sharp"`, 720p | Seedance 2.5 r2v | Retained "the most requested constraints overall" [B-ADH]. Camera, lens and light are parameters, not prose [B-CAM] |
| **Multi-angle product story / UGC ad** | Seedance 2.5 r2v | 9:16, 15–30 s, product = first ref | Kling O3 image-reference | "Strongest at multi-angle coverage and keeping object detail across camera positions" [B-ADH]. UGC template held 8 shots in 30 s [B-SD25G] |
| **Human action / fight / stunt** | Seedance 2.5 r2v, multi-shot with hard cuts | 10–15 s, 6–9 shots, `generate_audio:true` as a sync guide | Kling 3.0 first+last frame per key pose | 2.5 holds anatomy through transformations; 2.0 "cuts away and hopes you won't notice" [B-SD25VS]. Kling start/end frames chain choreographed poses [YT:4zu2CclB-EI@10:57] |
| **Car driving / chase** | Seedance 2.5 (or 2.0) r2v | 3–4 s shots, tight rigged angles, CAR PHYSICS block, clean plates | Kling 3.0 Pro i2v for single inserts (wheel, badge) | The full car spot was built on Seedance 2.0 [B-CAR]. Seedance 2.0 beat Happy Horse on a car ad [YT:luz_IRSzlDo@04:04] |
| **Dialogue scene, 2–3 people** | Seedance 2.5 r2v | dialogue in `{ }` + a dialogue block, ≤3 speakers | Kling 3.0 multi-shot (`multi_prompt`) | 2.5 lip-sync "fantastic"; on 2.0 "get close and the lipsync is off" [B-SD25VS]. Seedance gets glitchy past 3 characters [YT:lkL8mlpVScY@13:14] |
| **Lip-sync to a fixed VO or song** | Wan 3.0 r2v + `audio_urls` | 720p, ≤12 s, nonzero `seed`, locked framing | Seedance 2.5 r2v + `audio_urls` + exact transcript | Cheapest real lip-sync, PASS in our runs [LEDGER]. Third parties say Wan is weak on *music* lip-sync [BFA-WAN], so use Seedance with isolated vocals for songs [YT:XJnpH0XtgXM@00:58] |
| **Long one-take (15–30 s)** | Seedance 2.5 r2v or Cinema Studio `pacing:"single-shot"` | write "no cuts"; optional camera-path video ref | Wan 3.0 i2v (identity-faithful) | Seedance and Cinema Studio run 30 s natively [D-SD25-R2V; B-CS4]. Wan "sometimes cuts to a new camera angle even when the prompt asks for one continuous shot" and dissolved at 15–17 s [ATLAS-WAN] |
| **Extend an approved take** | Seedance 2.5 video-extend | trim the source to its last 4–6 s first [inf] | r2v with the previous clip as `video_urls` | Extend bills input + output seconds [EST]. Using the previous video as a reference carries camera energy better than a last-frame still [YT:SvhFnN-axJw] |
| **Fix one region or object** | Seedance 2.5 video-edit | duration = source; say "keep everything else exactly" | Genjutsu object-swap | Region edit fixes one spot without a full re-render [B-SD25HF]. It can glitch [YT:2a_rRtFSRec@14:30] |
| **Comedic reveal** | Seedance 2.5 r2v | 8–10 s, 4–5 shots, last shot about half the runtime | Cinema Studio `genre:"comedy"` | Toll-booth punchline: "the long-held final shot with the pause IS the joke" [B-CAR] |
| **Previs / blocking** | Wan 3.0 r2v/i2v 480p | $0.05/s, seed | Seedance 2.5 480p | Cheapest per second [EST] |

---

## 2. Prompt structure that works

### 2.1 Seedance 2.5 / Cinema Studio: labeled blocks (Higgsfield's tested shape)
Order: **GLOBAL STYLE → SCENE (one-line logline) → CHARACTERS → LOCATION → FIRST FRAME AND BLOCKING → Shot 1…N, each ending "Hard cut." → OPTICS → CAMERA → PHYSICS → LIGHTING → AUDIO** [B-SD25G]. Additional rules:
- "Skip a section and the output tends to fail in a specific, predictable way." A vague LOCATION is "the most common reason a multi-shot sequence starts drifting between cuts" [B-SD25G].
- "One visual rule at the top, one sound rule at the bottom, and everything in between broken into shots." Exclusions prevent more failures than extra positive description [B-SD25G].
- Add a RULES block for your scene logic, for example freeze rules for a time-freeze gag. "I didn't know about this before and it simply ruined some of my generations" [YT:2b3Z4rW5VJc@02:35]. Add a rule after any repeated failure, e.g. "the selected card must always be the ace of hearts" [YT:lkL8mlpVScY@08:43].
- Add a closing **POSITIVE LOCKS / Consistency** block covering the same face, the same seat, screen direction, the object's fate, "exactly five fingers per hand" and "all text unreadable" [B-SD25G]. Restate what stays unchanged at the start of each stage [ATLAS-SD25].
- **Length:** Higgsfield's working prompts run several hundred to 1,000+ words [B-SD25G]. One third-party guide prefers "two or three sentences" for 2.0 [SEG-SD25]. The two reconcile: short prompts when references carry the look, long prompts for multi-shot. On Higgsfield web the prompt caps at about 5,000 characters [YT:UxwV16jDglA@19:47] [unverified for the API].
- **Brackets** (ByteDance convention, via third parties): `( )` music, `< >` SFX, `{ }` dialogue, `【 】` subtitles. A line in `{ }` does not appear on screen. SFX written as plain text may get voiced [SEG-SD25; ATLAS-SD25]. Creators confirm that symbols help separate speech from sound [YT:Zo8KaTs0l6k@10:43; @16:21] [unverified as official BytePlus syntax].
- **Write the language first:** "Dialogue language: English, unhurried Kingston accent, natural, not a comedy voice", then the line. Lyrics written in the target language give the right accent; translated lyrics give "an accent doing an impression" [YT:2b3Z4rW5VJc@06:27; YT:Zo8KaTs0l6k@10:43].

### 2.2 Kling 3.0: subject-action-camera per shot
- The formula is camera, subject, action, environment, lighting, texture, audio [YT:b_RghITuQQM].
- In multi-shot, each shot gets its own `multi_prompt` (≤512 chars, 1–15 s, ≤6 shots). The total is summed and billed. A non-empty top-level prompt is still required, and is truncated after 2,500 chars [D-K3]. Higgsfield web shows up to 5 shots [B-K3].
- With a start image, "there's no need to describe the environment again. Focus the prompt on the action and camera" [YT:6qyDrGjOJQs@04:09].
- Dialogue format: `Name (tone, language): line`, e.g. `Mom (softly, in a surprised tone): Wow, I didn't expect this.` [K-GUIDE].
- Use "…" for pauses, and size the shot duration to the line (2 s for a short line, 7 s for a long one) [YT:HE9HJY2SLl0@01:52].
- **Shot/reverse-shot:** set two angles in shots 1–2, then write "return to the close-up shot of [X]" for the later shots [YT:HE9HJY2SLl0@05:29].

### 2.3 Camera vocabulary the models obey
- **Name the move, state speed and end framing, and rule out the rival move.** Example: "a purely OPTICAL zoom out… NOT a dolly out, NOT a pull-back… ZERO parallax". Another: "decelerating smoothly into a static hold… No pan, no tilt, no crane" [B-CAM]. Text-only camera prompts vary run to run because "speed, path, and end position stay unspecified" [B-CAM].
- **Cinema Studio enum moves (API, guaranteed field):** `dolly-in/out, crane-up/down, tracking, side-tracking, whip-pan, drone-orbit, helicopter-shot, aerial-pullback, pov, snorricam, robot-arm, bullet-time, dolly-zoom, crush-zoom, handheld, rack-focus…` [EST]. On web, `#craneup`-style hashtags at the prompt's end run in the order typed [YT:mJD-1QSDKPQ@02:57; @14:38]. In one test, though, only the rack focus out of three hashtag moves was honoured [YT:2a_rRtFSRec@13:11]. **Use one enum move per generation**, and write any second move into the prose.
- **Chase-car / rigged mounts read best when the rig is named:** "hard-mounted rigged camera locked to the car body, inches above the asphalt… the camera does not move, it is bolted to the car"; "static locked-off roadside camera… the car passes through the fixed frame" [B-CAR].
- **FPV:** describing a fly-around "as if shot with an FPV drone" worked on Seedance with a video ref [YT:ikPGQGoUjQ0]. FPV *over traffic* failed every time [YT:GNxmt_4IifA].
- **Whip pan:** works as a cut device in action ("whip-pan cuts", "whip-pan through white fabric transitions out") [B-SD25G; B-K3].
- **Camera-path reference:** a Blender or Cinema 4D blocking render (`video_urls`) transfers camera path and timing for simple, smooth moves. Complex dance plus camera fails [YT:StX3eflYq_o@12:24; YT:ikPGQGoUjQ0].
- **Model limit:** "Editing gluing: turning the steering wheel, switching to turning the front wheel… Seedance has no idea what it is." Do match-cuts in the edit [YT:GNxmt_4IifA].

### 2.4 Hard cuts inside one generation, and beats per duration
Evidence from tested prompts:

| Source | Duration | Shots/beats | Avg per beat |
|---|---|---|---|
| Higgsfield action (cargo-hold fight) | 15 s | 9 shots | 1.7 s (theft 1.2–1.8 s, held slow-mo 2.0 s) [B-SD25G] |
| Higgsfield multi-character dance | — | avg beat ≈1.25 s on the music [B-SD25G] | 1.25 s |
| Higgsfield dramatic exterior | 15 s | 5 segments | 3 s [B-SD25G] |
| Higgsfield commercial (headphones) | 20 s | 5 segments, cuts at 4.0/8.0/10.5/16.5 s | 4 s [B-SD25G] |
| Higgsfield noir | 30 s | 5 segments | 6 s [B-SD25G] |
| Higgsfield UGC | 30 s | 8 shots, speech ends by 25 s | 3.75 s [B-SD25G] |
| Car spot, dealership | 12 s | 7 shots | 1.7 s [B-CAR] |
| Car spot, toll punchline | 8 s | 5 shots, last ≈ half | 1 s ×4 + 4 s [B-CAR] |
| Car spot, highway | 15 s | 4 cuts | 3.5–4 s [B-CAR] |
| Replicate examples | 15 s | 4 segments | 3–4 s [REP] |
| Dan Kieft heist test | 15 s | 10 shots | too dense: "we couldn't really do all of that" [YT:lkL8mlpVScY@06:33] |

**Working budget [inf from the table]:**

| Clip length | Dialogue / drama | Product / commercial | Action |
|---|---|---|---|
| **5 s** | 1 shot, 1 line | 1 shot, 1 move, 1 action | 2–3 cuts |
| **10 s** | 2–3 shots | 3 shots | 5–6 cuts |
| **15 s** | 3–5 shots | 4–5 shots | 8–9 cuts |
| **30 s** | 5–8 segments, speech ends about 5 s early | 5–8 segments | Split into two 15 s clips: fight clips carry music you can't cut around (§4) |

Other limits:
- Never several actions inside one second [ATLAS-SD25].
- A single camera move needs ≥3 s to read [inf from B-CAR, B-K3].
- Escalate shot scale (wide → medium → close → ECU) [REP; YT:tZReV23ncuc@02:05].

---

## 3. References, identity and product fidelity

**How references are weighted (observed):**
- References beat text for identity. "Once a face or a product is locked as a reference, it survives hard cuts, lighting changes, and camera moves" [B-SD25G]. With prompt text alone, the same description gave three different faces [YT:ZsrhdgG0I1E@01:15].
- References carry *appearance only*, not hand motion, light changes or the camera's end position. Those must be written [B-MIST].
- Clutter lowers coherence. "A smaller, deliberate set beats a cluttered one" [B-SD25G]. On Kling Omni, more refs meant more glitches (a dog grew a tail) [YT:b_RghITuQQM]. Stay at about 1–8 subjects [ATLAS-SD25].
- Kling Elements identity weakens when the character is far from camera [YT:tqZ0JuUevwA]. Seedance needs a close, detailed face: a full-body photo from too far "does not look like me" [YT:lkL8mlpVScY@20:40].

**Building references that hold:**
- **Character:** use a three-panel sheet on flat grey. Left: full body front, headless. Middle: back. Right: face close-up. That leaves one face to copy. Grey keeps exposure neutral [YT:ZsrhdgG0I1E@03:29–04:47; YT:mJD-1QSDKPQ@07:53; B-CAR].
  - The alternative is separate images per angle (4 face + 4 body, grouped as one subject) instead of a collage [YT:UxwV16jDglA@10:40; ATLAS-SD25].
  - Real selfies beat generated sheets for photoreal humans [YT:lkL8mlpVScY@23:31].
  - Change outfits with image-to-image off the base sheet ("keep face, hair, body; only wardrobe") [YT:mJD-1QSDKPQ@08:34].
  - Drop tiny accessories (a small hat); the model can't hold them [YT:Zo8KaTs0l6k@05:15].
  - If sheet faces disagree, crop the best face and use it as the identity source [B-CAR].
- **Product:** generate it on neutral grey [YT:GNxmt_4IifA]. Put it as the first ref. Write the exact label text and "unbranded, no logos" except the product label [B-SD25G].
- **Position and trajectory:** attach a hand-drawn diagram ("blue line is the trajectory") or a location photo with a red mark at the stop point. Say the marks must not render [B-CAR; YT:GNxmt_4IifA].
- **Interior or prop continuity:** generate one locked-off "statics" video of the set, then screenshot frames as elements. "Every frame of your video, by definition, matches the others" [YT:GNxmt_4IifA]. The steering wheel kept changing shape until locked this way [YT:GNxmt_4IifA].
- **Storyboard or script as a reference image:** "Based on the script from Image 1, generate advertising content for the perfume product in Image 2" [GH-ZERO, @BFAVicky]. Keep storyboard grids at ≤15 panels with a clear reading order [ATLAS-SD25].
- **Role phrasing that works:** "character appearance only. Reference." [B-CAR]; "Image one is used for his identity… do not recast, do not beautify, do not use as an image background" [YT:Zo8KaTs0l6k@05:55]; "Do not use its sky or the parked cars" [SEG-SD25]. Avoid vague mappings like "images 1 through 4 define four characters" [ATLAS-SD25].
- **Tag syntax:**
  - Cinema Studio API documents `<<<image_1>>>`, `<<<video_1>>>`, `<<<audio_1>>>` [D-CS4].
  - Higgsfield web uses `@[Image 1](image_1)` / `@element` [B-SD25VS; B-CAR].
  - Replicate uses `[Image1]`; ComfyUI Wan uses `@Image1` [REP; COMFY-WAN].
  - **The raw Seedance 2.5 and Wan 3.0 endpoints don't document a token [unverified].** Belt and braces: tag `@image1` *and* describe each ref in words in upload order. That is what our passing F08/F09 prompts did [LEDGER].

**First/last frame chaining:**
- Kling: `image_url` + `last_image_url` (3.0) or `first_frame_url`/`last_frame_url` (O3). Describe only the path between the frames [D-K3; D-KO3].
- On web, multi-shot is unavailable with start + end frame, and Kling multi-shot takes a start image but not an end image [YT:b_RghITuQQM; YT:6qyDrGjOJQs@03:15]. The API schema accepts both fields; whether multi-shot honours `last_image_url` is [unverified].
- Seedance i2v: framing and ratio follow `image_url`. `end_image_url` is optional [D-SD25-I2V]. Mismatched first/last ratios stretch the last frame [ATLAS-SD25].
- Last-frame screenshots carry the look but not the motion. "The camera might suddenly change direction." Pass the previous *clip* as a video reference instead [YT:SvhFnN-axJw].
- To re-roll one bad shot of a Kling multi-shot, screenshot its first frame, regenerate only that shot, and splice it in [YT:HE9HJY2SLl0@06:53].

**Video-extend for long continuous shots:**
- Seedance 2.5 `video-extend`: 4–30 s added. Framing follows the source. Up to 9 extra `video_urls` [D-SD25-EXT].
- **Billing counts input + generated seconds** at 0.6× the token rate: 720p ≈ $0.277/s × (in + out) [EST]. The `estimate` endpoint shows only the output part, so a 10 s source + 10 s extend costs ≈$5.55, not $2.77 [inf].
- Trim the source to the last 4–6 s before extending [inf].
- Risks:
  - Extended clips may have audio levels that don't match [SEG-SD25].
  - Backward extensions can make characters appear too early [ATLAS-SD25].
  - Identity drift and repeated expressions appear past about 30 s [B-DIST].
- The web "Long video mode" (180 s) is six 30 s clips stitched from one prompt. Skip it and chain by reference [YT:UxwV16jDglA@19:47–20:29].

---

## 4. Native audio: prompting, sync, limits, replacement

- **It is always there.** In Seedance, "a prompt that says nothing about audio still produces audio" [YT:2b3Z4rW5VJc@01:21].
  - Seedance `generate_audio` doesn't change the price [EST; B-CAM]. Keep it **on** as a free sync guide even when you'll replace it [inf].
  - Kling `sound:"on"` adds 50 % (10 s Pro $1.428 vs $0.952) [EST].
- **How to prompt it:**
  - Audio comes **last**, as timed events: "one distant thunder roll at 5.0s", "heels click… from 15.0s to 19.0s", "AUDIO: no score, no added music, no narration" [B-SD25G].
  - Write two or three concrete SFX, not a paragraph of sound design [SEG-SD25]. Make each specific ("the metallic clink of a coin hitting a stone") [YT:tZReV23ncuc@04:04].
  - Give each sound an in and an out time; "the engine fades away with it" [YT:2b3Z4rW5VJc@04:51].
  - Write lines inside the shot *and* again in a dialogue block in spoken order [YT:2b3Z4rW5VJc@04:13].
  - Separate diegetic from non-diegetic sound ("a hard non-diegetic sub-bass hit… on the exact frame the light goes dark") [YT:Zo8KaTs0l6k@17:15].
- **How well it syncs:**
  - Seedance: "synced at the millisecond level" [REP]. Our F08 snap landed at 1.75 s with audio at 1.76 s [LEDGER].
  - Seedance 2.5 lip-sync holds even on screams [B-SD25VS]. Our 30 s audio-driven duo led by about 0.3 s, corrected in the mix [LEDGER].
  - Kling lip-sync breaks after about 10 s [YT:b_RghITuQQM].
  - Wan lip-sync lags 0.12 s [LEDGER]. Third parties report Wan problems on performance-heavy and music scenes [BFA-WAN].
  - During sung pauses, mouths may keep moving to the beat [YT:lkL8mlpVScY@24:14].
- **Known failure:** Seedance 2.5 ignores "no background music / no BGM" most of the time [YT:RpsEdtUJCnU@00:00–05:56].
  - Dialogue scenes: music at the head, then it stops.
  - Engine-dominant scenes: no music.
  - Fight scenes: music "pretty much 100% of the time".
  - Editing the music out of a 29 s clip returned only 14 s at 195 credits, and was not repeatable [YT:RpsEdtUJCnU@08:42–09:24].
  - ByteDance claims 2.5 "minimizes uncontrolled… background music" [YT:RpsEdtUJCnU@02:46] [unverified].
  - Happy Horse also adds music when told not to [YT:luz_IRSzlDo@02:09].
- **When to replace (house rule):**
  - **Music:** always replace. Each clip's bed differs and chops badly at cuts [YT:RpsEdtUJCnU@12:28].
  - **Brand VO:** replace with the locked ElevenLabs voice (13), and keep the generated track only as timing reference.
  - **Dialogue on visible lips:** keep the generated voice, or drive the lips with the final audio (§7.4). Never lay a new voice over moving lips that don't match [LEDGER].
  - **SFX/foley:** keep when it lands. Re-place every hit on the *measured* frame [LEDGER].
  - When native music bleeds under SFX you need, use stem separation (vocals/music/effects) before the edit [inf] [unverified quality].

---

## 5. Failure mode → fix table

| Failure | Likely cause | Fix (evidence) |
|---|---|---|
| Extra cuts appear; shot count wrong | Seedance improvises coverage | "Exactly N shots and N−1 cuts, no extra inserts" [B-CAR]. For one-takes: "one continuous take, no cuts, every camera change happens physically inside the shot" [B-SD25VS] |
| Cut appears in a requested one-take | Wan/Seedance hide hard motion with a cut | Simplify the motion; trim around the cut [ATLAS-WAN]; or shoot it as deliberate coverage (41) |
| Face drifts between shots or clips | Text-only identity | One clean close face ref or sheet per character; Soul ID / Elements; change one variable at a time between shots [B-DIST; YT:ZsrhdgG0I1E] |
| Character duplicated for a split second | Busy action, many refs | Region edit / video-edit on that window [YT:2b3Z4rW5VJc@11:24]; fewer subjects (≤3) [YT:lkL8mlpVScY@13:14] |
| Morphing / rubbery bodies in fast action | Speed vs. consistency trade-off | Slower moves, fewer simultaneous actions, Kling ≤10 s; "the more motions… the more likely it's going to warp" [YT:4zu2CclB-EI@13:16; YT:b_RghITuQQM]. Kling `cfg_scale` 0.35–0.4 if over-cooked [inf, 12] |
| Rigid object bends (jet hull, car body) | Motion described as an adjective | Write the path with start, end and sharpness, plus "rigid hull" [B-MIST]; CAR PHYSICS block [B-CAR] |
| Floaty physics, cloth "underwater" | Physics unspecified | PHYSICS block: mass, inertia, "no floaty wire-fu", "strikes connect with genuine weight" [B-SD25G; B-FAIL] |
| Camera passes through glass, walls or cars | Impossible camera path | Name a real rig and its side ("the camera never crosses to the north side", "camera stays on the landward side") [B-SD25G]; build energy with cuts instead of chaotic moves [B-DIST]; 41 physics gate |
| Wrong move (zoom instead of dolly), inconsistent speed or end point | Underspecified move | Name the move, speed, easing, end framing and hold; negate the rival move [B-CAM]; Cinema Studio `camera_movement` enum [D-CS4] |
| Screen direction flips; actors teleport | No blocking | FIRST FRAME AND BLOCKING with x/y %, facing, "never swap sides" [B-SD25G]; open on a plain frontal "positions" shot [YT:GNxmt_4IifA]; Kling mirrored "point left" into screen-right [LEDGER] |
| Extra / fused fingers | Contact points unspecified | Name every contact finger by finger; give start and end hand states; add a hand-pose ref; "exactly five fingers per hand" [B-MIST; B-HANDS; B-SD25G] |
| Text or logo garbled, mirrored, softened | Video models redraw text | Text only from the ref or first frame; close, stable framing; "all signage unreadable"; pre-blurred props; supers in post [B-ADH; YT:lkL8mlpVScY@10:07; B-CAR] |
| Traffic lights wrong, lanes ignored, dashboard numbers garbage | World-rule knowledge missing | Remove intersections, keep tight frames, lock the dashboard via a screenshot element [YT:GNxmt_4IifA] |
| Background car or extra becomes a clone of the hero | Plate contains look-alikes | Clean the plate before generating [YT:GNxmt_4IifA] |
| Object vanishes or regrows | Fate unscripted | Write its landing and state ("cap lands on asphalt in front of camera"; "only shrinks") [B-CAR; B-SD25G] |
| Product vessel changes between shots | Each keyframe invents its own | Name the same vessel in every keyframe [LEDGER] |
| Strong opening, drift later | Long clip, constraints not restated | Restate locks per stage; put hero beats early; shorter clips chained by reference [ATLAS-SD25; B-DIST] |
| Unwanted music | Seedance 2.5 default bias | §4; plan a music-free edit or a dominant diegetic sound [YT:RpsEdtUJCnU] |
| Wrong accent or language | Unspecified | "Dialogue language: X, accent Y, pace, energy" before `{line}` [YT:Zo8KaTs0l6k@10:43; ATLAS-SD25] |
| Name misspelled (spoken or typography) | Model guesses spelling | "Name spelling lock: Dan. Not Dann, not Dane" [YT:StX3eflYq_o@15:30] |
| Slow-motion added unasked; feels fake | Genre bias toward drama | "Real-time playback, natural 1:1 speed, no slow motion" [B-CAR]; trim in edit [YT:Zo8KaTs0l6k@19:55] |
| Over-acted or under-acted | Mood words only | Emotion as visible action ("eyes widen… a tiny stunned blink… corners of mouth lift a millimeter"); intensity scale ("sweating, 9/10") [B-CAR; B-MIST]. Change one variable per retake [YT:GNxmt_4IifA] |
| Plastic skin | Over-clean refs or generation | Unretouched-skin lock; real-photo refs; add grain in post [B-SD25G; YT:Zo8KaTs0l6k@21:23] |
| Faces soften after repeated edits | Generational loss | Edit from originals; keep refs at 2–4K [YT:4zu2CclB-EI@16:42; YT:mJD-1QSDKPQ@07:53] |
| Cinema Studio preset has no visible effect | Preset weaker than prompt | Treat presets as nudges; restate the key look in prose [YT:2a_rRtFSRec@13:11] |
| **Safety: prompt flagged** | An LLM reads the whole prompt as one scene; youth words raise scrutiny [MORPHIC] | Don't strip the action; give it production context, setting and purpose. State a harmless outcome ("nobody is hurt", "brakes harmlessly"). Use adults. Swap real weapons for props that fit the story (our F09 used a foam-spraying can) [MORPHIC; LEDGER] |
| **Safety: reference rejected** | Higgsfield eligibility check: real identifiable faces, named IP, public figures [YT:SvhFnN-axJw; MORPHIC] | Use original characters, our own talent with consent, or face away / wide. No celebrity or IP lookalikes. Ad policy also applies (45) |
| **Stunts, falls, jumps** | Filter + realism | Write them as professional stunt craft with real gear (canopy, rigging, crash mats), a controlled landing, and the camera cutting on impact. No injury or gore shown [inf from MORPHIC + 41]. Failed or NSFW API requests are not charged [D-BILL] |

---

## 6. Resolution, seeds and the cost ladder

**Facts:**
- **No `seed` on Seedance 2.x, Kling 3.0/O3/Omni or Cinema Studio 4.0** in the Higgsfield API schemas [EST].
- Wan 3.0 has `seed`, but only a nonzero seed is forwarded [D-WAN3].
- Even with a seed, changing resolution changes the noise tensor and token grid, so the composition will not carry over [inf; search summary in §10 under SEED].
- Higgsfield's own tip: test at 480p/720p and about 5 s first [B-FAIL]. "Movement, focus shifts, and pacing all render correctly at [720p]" [B-CAM].

**What this means [inf]:**
- A 480p generation is a **prompt test**: blocking, beat timing, shot count, physics, filter pass. It is not a take preview.
- For i2v, the first frame anchors composition, so 480p results transfer better than for r2v or t2v.
- If a 480p take is *the* take, keep it and upscale. Re-rolling at 720p gives a different take.
- Higgsfield web has a Topaz upscaler [YT:SvhFnN-axJw]. The API upscale endpoint is not live (12 §2).
- Feeding the 480p winner to `video-edit` at 720p with "keep everything exactly" is an untested way to keep the performance [unverified].

**Hit rates to budget for:**
- The car spot got 1 usable of 4 attempts on hard driving shots and took fragments from several takes [YT:GNxmt_4IifA].
- Pros "generate a bunch of different times, then pick the best shots" [YT:lkL8mlpVScY@11:39].
- Budget **3 takes** for action or dialogue and **1–2** for simple inserts [inf].

**Price per 10 s, list USD, 16:9 [EST]:**

| Model / mode | 480p | 720p | 1080p | Notes |
|---|---|---|---|---|
| Wan 3.0 r2v/i2v | **$0.50** | $1.00 | $2.00 | Default resolution is **1080p**, so always set it. Seed available |
| Wan 3.0 Prime r2v | — | ≈$1.19 | $2.38 | |
| Kling 3.0 std i2v | — | — | — | $0.71 sound off / $1.07 on (std vs pro output resolution [unverified]) |
| Kling 3.0 pro i2v | — | — | — | $0.95 off / **$1.43 on** |
| Kling 3.0 4K i2v | — | — | — | $3.57 |
| Kling O3 / Omni pro | — | — | — | $0.95; sound defaults to off on O3 |
| Seedance 2.0 i2v | ≈$1.36 | $3.02 | ≈$6.80 | Max 15 s, 9 img / 3 vid / 3 audio refs |
| **Seedance 2.5** i2v / r2v | **$2.06** | **$4.62** | **$11.37** | Audio free; ≤30 s; no seed |
| Cinema Studio 4.0 | $2.08 | $4.62 | n/a (API 480/720 only) | Same engine pricing |
| Seedance 2.5 extend / edit | $1.23 | $2.77 | $6.82 | **Per 10 s of input + output** |

**Cost ladder for one finished 15 s action or dialogue beat:**

| Rung | What | Spend |
|---|---|---|
| 0 | Script, shot list, physics read (41), references built and plates cleaned | images only (~$0.3–2) |
| 1 | **Blocking previs:** Wan 3.0 480p, 15 s, fixed seed; iterate the prompt | $0.75 per try |
| 2 | **Prompt proof:** Seedance 2.5 480p, 15 s, 1 take; check shot count, adherence, filters, music | $3.08 |
| 3 | **Production:** Seedance 2.5 720p, 15 s, ×3 takes; cut the best fragments across takes | $20.80 |
| 4 | **Repairs:** video-edit on one region (5 s source) or Kling inserts | $2.77 / $0.48 |
| 5 | **Hero only:** re-render 1–2 hero shots at 1080p, or upscale the 720p take | +$17 per 15 s at 1080p; prefer upscale |
| — | Product inserts | Kling 3.0 pro i2v 5 s, sound off, ×2 | $0.95 |

For social 9:16 delivery, 720p is acceptable. "Most Instagram, YouTube Shorts, TikTok… you barely notice if it's 720p" [YT:StX3eflYq_o@02:16]. Note that every Seedance 2.5 example in Higgsfield's comparison was 720p, and "the moment you push into a wide shot, faces go soft" [B-SD25VS].

---

## 7. Copy-paste templates

Conventions:
- Fill `[brackets]`.
- Upload references in the order listed.
- Run the hfgen JSON through `estimate` before `batch`.
- Seedance templates use the labeled-block shape (§2.1).

### 7.1 Car chase, multi-shot (Seedance 2.5 r2v, 15 s, 8 shots)
```json
{"model":"bytedance/seedance-2.5/reference-to-video",
 "args":{"image_urls":["<car_sheet grey bg>","<driver close face/sheet>","<loc plate: CLEAN, no signage, no other cars like ours>","<police car sheet>"],
  "duration":15,"resolution":"480p→720p","aspect_ratio":"9:16","generate_audio":true,
  "prompt":"GLOBAL STYLE: photoreal car-commercial action, 35mm, Kodak 500T grain, organic colour, soft contrast, real-time 1:1 speed, NO slow motion, NO CGI, no music. 9:16.\nREFERENCES: @image1 = THE CAR, exact body, paint [colour], wheels, badge — vehicle appearance only. @image2 = THE DRIVER, identity and wardrobe only, ignore the backdrop. @image3 = LOCATION, as-is: [road type], match this layout in every shot, all signage unreadable. @image4 = POLICE CRUISER, vehicle appearance only, no real insignia.\nFIXED GEOGRAPHY (identical in every cut): the car travels [direction] in the [lane]; the police cruiser always behind it, same lane side; sun from high [left/right], shadows toward [lower right]; no intersections, no traffic lights, light traffic each locked to its own lane.\nCAR PHYSICS: the car weighs two tons and always behaves like it — nose dives under braking, body rolls onto the outside wheels in turns, tyres grip visibly, contact shadows stay planted; on hard steering the tail steps out a few degrees and is caught — realistic controlled slides, never arcade drifting.\nEXACTLY EIGHT SHOTS AND SEVEN HARD CUTS — no more, no fewer, no extra inserts.\nShot 1 (0–1.5s): low roadside camera locked off at knee height; the car rips past left-to-right in the near foreground, motion blur, dust and debris swirl. Hard cut.\nShot 2 (1.5–3.0s): rigged camera bolted to the front fender inches above the asphalt, the front wheel spinning, road streaming; the camera does not move relative to the car. Hard cut.\nShot 3 (3.0–4.5s): in-car, three-quarter front close-up of @image2 gripping the wheel, eyes flick to the mirror; red-blue lights sweep across his face. Hard cut.\nShot 4 (4.5–6.5s): chase-car tracking at bumper height behind @image1; the car brakes, nose dives, then a handbrake turn into a side street, tyre smoke. Hard cut.\nShot 5 (6.5–8.0s): low nose-on of @image4 fishtailing through the same turn, siren lights strobing. Hard cut.\nShot 6 (8.0–10.5s): ground-level side tracking, the car weaves between two slower vehicles with a clean legal lane change, body rolling and catching. Hard cut.\nShot 7 (10.5–12.5s): static wide from a pedestrian bridge, both cars pass under, the police car falls back. Hard cut.\nShot 8 (12.5–15.0s): rigged low over the hood, the badge sharp in the foreground, the world streaming behind, horizon gently tilted, strong engine vibration in the frame; hold to end.\nPOSITIVE LOCKS: same car, same driver face and wardrobe in every shot; car never changes colour or shape; screen direction never flips; the camera never passes through glass or vehicles; nobody is hurt; no readable text anywhere.\nAUDIO: <engine at full song> dominant throughout, <tyre squeal> at 4.8s, <siren doppler> from 5.0s, <wind-blast on Shot 8>. No score, no music, no dialogue."}}
```
Notes:
- The engine-dominant track lowers the risk of an unwanted music bed [YT:RpsEdtUJCnU@05:07].
- Swap Shots 6–7 for more inserts if traffic misbehaves. Never use a wide aerial over traffic [YT:GNxmt_4IifA].

### 7.2 Action stunt (Seedance 2.5 r2v, 10 s, 6 shots; Kling fallback per pose)
```text
GLOBAL STYLE: photoreal stunt cinema, practical, gritty, real weight, imperfect optics, 24fps real-time, no slow motion except where stated, no music, no gore. 9:16.
REFERENCES: @image1 = THE PERFORMER, a professional stunt performer: identity and wardrobe only. @image2 = LOCATION as-is, clean plate.
FIRST FRAME AND BLOCKING: performer at x 40% y 60% on the [rooftop edge / ledge], facing screen-right, [gear: harness / canopy pack / pads] visible.
EXACTLY SIX SHOTS AND FIVE HARD CUTS.
Shot 1 (0–1.5s) medium, locked off: START — knees bent, arms back, weight on toes. END — airborne, arms forward. Hard cut.
Shot 2 (1.5–3.0s) low wide from below: the body travels in one clean ballistic arc, limbs tucked; [canopy opens with a jolt at 2.4s]. Hard cut.
Shot 3 (3.0–4.5s) close on the hands/feet: [toggles pulled / hands reach the rail], exact contact points: [describe each finger/foot]. Hard cut.
Shot 4 (4.5–6.5s) side tracking: controlled landing — heels strike, knees absorb, a roll across the shoulder onto [crash mat / grass], momentum carries one more step. Hard cut.
Shot 5 (6.5–8.0s) medium close: performer rises unhurt, chest heaving, one breath out. Hard cut.
Shot 6 (8.0–10s) wide, locked off: [payoff / product beat]; hold.
PHYSICS: real mass and inertia; no floaty wire-fu; cloth and hair lag 3–5 frames behind the body; the landing surface flexes.
POSITIVE LOCKS: same face and wardrobe; exactly five fingers per hand; the camera never passes through walls or glass; nobody is injured; no weapons.
AUDIO: <wind rush> 1.5–3s, <canopy snap> 2.4s, <thud and fabric scuff> 5.2s, <one exhale> 7.0s. No music.
```
Fallback:
- For a pose that keeps failing, make a start still and an end still (stick-figure pose → image edit [YT:4zu2CclB-EI@05:19]).
- Run Kling 3.0 Pro i2v with `last_image_url`, 5 s, `sound:"off"`, prompt = the path only.

### 7.3 Product hero one-take (Cinema Studio 4.0; Kling landing variant)
```json
{"model":"higgsfield/cinema-studio/4.0",
 "args":{"image_urls":["<product, grey bg>","<location plate>"],"duration":8,"resolution":"480p→720p","aspect_ratio":"9:16",
  "camera_movement":"dolly-in","camera_lens":"clean-sharp","camera_aperture":"f4-moderate","camera_model":"modern","light":"window","pacing":"single-shot","generate_audio":true,
  "prompt":"<<<image_1>>> is the exact product: [shape, material, cap], label text \"[TEXT]\" — the only readable text in the video; never redesigned. <<<image_2>>> is the location, as-is; ignore any objects in it except the [surface].\nOne continuous take, no cuts. First frame: the product already on the [surface] at x 35% y 65%, three-quarter view, not centred.\nCamera: one decisive dolly-in on rails at constant speed from 1.2 m to 0.4 m, decelerating into a static hold for the last 1.5 s; NOT a zoom, no pan, no orbit, no handheld.\nAction: [one physical event: a bead of condensation slides 3 cm and stops at the label edge].\nPhysics: the product is rigid and never moves or deforms; liquid has real surface tension.\nLight: single window key from frame-left, 5000K, hard edge, falloff to shadow on the right; contact shadow under the base.\nAudio: <room tone>, <one soft glass tick> at the hold. No music, no voice."}}
```
- Omit any enum you don't want; `"auto"` is rejected [D-CS4].
- Kling variant: `kling-video/v3.0/pro/image-to-video`, `image_url` = keyframe, `last_image_url` = packshot, `duration` 5, `sound:"off"`, `cfg_scale` 0.5. Prompt only the path: "camera arcs 20° right at constant radius and settles exactly on the end frame; product still" (12 §4 D).

### 7.4 Character dialogue with lip-sync
**A. Exact VO (brand voice) → Wan 3.0 r2v:**
```json
{"model":"alibaba/wan-3.0/reference-to-video",
 "args":{"image_urls":["<character close portrait, same framing you want>"],"audio_urls":["<final ElevenLabs line, WAV/MP3, ≤12 s>"],
  "duration":"<audio length rounded up>","resolution":"720p","aspect_ratio":"9:16","seed":4242,"generate_audio":true,
  "prompt":"@Image1 is the speaker: identity, hair and wardrobe exactly as the reference. @Audio1 is the exact speech: lip-sync every syllable to it; do not change the words. Same camera distance as the reference, chest-up, hands visible at the bottom edge, do not zoom in, one continuous shot, no cuts. Natural blinks, small head motion following the speech rhythm, eyebrows lift on the stressed word. Background: [location], soft key from [side]. Words spoken: \"[exact transcript]\"."}}
```
- Then replace the audio with the master and shift by the measured lag. Our runs measured 0.12 s [LEDGER].
- For songs, isolate the vocals first and cut them into model-length chunks with exact lyrics in the prompt [YT:XJnpH0XtgXM@00:58–03:26].

**B. Scene with generated voices → Seedance 2.5 r2v (≤3 speakers):**
```text
GLOBAL STYLE: [look]. No music, no subtitles.
REFERENCES: @image1 = MARA, identity and wardrobe only. @image2 = THEO, identity and wardrobe only. @image3 = LOCATION as-is.
FIRST FRAME AND BLOCKING: Mara screen-left facing right, Theo screen-right facing left, kitchen table between them; they never swap sides.
Shot 1 (0–3s) two-shot. Shot 2 (3–6s) close-up of Mara. Shot 3 (6–9s) close-up of Theo. Shot 4 (9–12s) return to the close-up of Mara.
Dialogue language: English, American, low-key, unhurried.
Shot 2: Mara (dry, eyes on her cup): {You said ten minutes.}
Shot 3: Theo (half-beat late, guilty smile): {I said about ten minutes.}
Shot 4: Mara (one slow blink, corner of mouth lifts a millimetre): {...Sure.}
DIALOGUE BLOCK (order spoken): Mara — "You said ten minutes." / Theo — "I said about ten minutes." / Mara — "...Sure."
AUDIO: <fridge hum>, <cup set down> at 2.6s. All speech ends by 11s.
POSITIVE LOCKS: same faces and seats every shot; only the speaker's lips move.
```
**C. Kling 3.0 multi-shot equivalent:** use `multi_prompt` shots of 2–4 s, with `Name (tone): line` per shot [K-GUIDE]. Total ≤10 s for clean lip-sync [YT:b_RghITuQQM]. Set `sound:"on"`.

### 7.5 Comedic reveal (Seedance 2.5 r2v, 8 s, 5 shots, the held last shot is the joke)
```text
GLOBAL STYLE: photoreal deadpan comedy, natural light, real-time, no music, no subtitles. 9:16.
REFERENCES: @image1 = [STRAIGHT MAN], appearance only. @image2 = [DEADPAN CHARACTER], appearance only. @image3 = LOCATION as-is, clean plate. @image4 = [PRODUCT], exact; label "[TEXT]" is the only readable text.
EXACTLY FIVE SHOTS AND FOUR CUTS — the first four are brief and rapid; the fifth is the longest, about half the runtime.
Shot 1 (0–1.0s): [the inciting chaos] — e.g. a gust tears the cap off @image1; he stays in frame. Cut.
Shot 2 (1.0–2.0s): close-up @image1, restrained: brows lift slightly, eyes track the cause to the horizon; nothing theatrical. Cut.
Shot 3 (2.0–2.8s): wide; the [cap] lands on the ground right in front of camera with a soft bounce. Cut.
Shot 4 (2.8–4.0s): close-up @image1 turns to his colleague, genuinely curious: {Who was that??} Cut.
Shot 5 (4.0–8.0s, held): @image2 utterly still, [holding @image4]; flat: {Here we go again.} — a long uncomfortable pause, a slow nasal exhale, eyes lift over the [object] — {just [name] doing his thing.} — eyes drop back; hold to the end.
Dialogue language: English, dry, unhurried. AUDIO: <whoosh> 0.4s, <cap lands> 2.5s, <paper rustle> 7.2s.
```
Adapted from [B-CAR, Scene 4 Part 2]. The comedy lives in the held final shot. Write the pause as an event with its own sound.

---

## 8. Settings cheat-sheet

| Setting | Model | Use | Evidence |
|---|---|---|---|
| `cfg_scale` 0–1 (default 0.5) | Kling 3.0 only | Higher means stricter prompt adherence and less freedom. Try 0.6–0.7 if the move is ignored, 0.3–0.4 for natural motion or rubbery output | [KCFG; 12 §3] heuristic |
| No cfg / guidance | Seedance, Cinema Studio, Wan | Steer with references, locks and enums | [EST] |
| `enable_thinking` | Wan 3.0 | Auto-on with `file_url` / `link_url` doc refs. Effect on visuals [unverified] | [D-WAN3] |
| `duration` | Seedance 4–30, Kling 3–15 (shots ≥1 s, sum billed), Wan 2–30, Cinema Studio 4–30 | Shortest that fits the beats (§2.4). Kling ≤10 s for dialogue | [EST; YT:b_RghITuQQM] |
| `aspect_ratio` | Seedance r2v / Cinema Studio default **16:9**; Wan default `adaptive`; Seedance i2v and Kling i2v follow the image | Always send `9:16` on r2v for reels. Make the keyframe 9:16 for i2v | [EST; D-SD25-I2V] |
| `resolution` | Seedance 480/720/1080; Cinema Studio 480/720; Wan default 1080 | §6 ladder | [EST] |
| `generate_audio` / `sound` | Seedance free; Kling +50 % (O3 defaults off) | Seedance on (sync guide); Kling off unless it has dialogue | [EST] |
| `bitrate_mode` | Seedance 2.5 (`high` default) | Leave `high`; price effect [unverified] | [EST] |
| `pacing` / `genre` | Cinema Studio | Genre "shifts pacing, contrast, and camera behavior even when the written scene description stays identical". `single-shot` for one-takes, `chaotic` for action | [B-SD25G; B-CS4] |
| Prompt length | Kling ≤2,500 top-level (+≤512 per shot); Seedance web ≈5,000 chars | Over-length is truncated | [D-K3; YT:UxwV16jDglA@19:47] |

---

## 9. Model profiles (one paragraph each)

**Seedance 2.5:**
- 4–30 s, up to 30 images, 10 videos and 10 audio (50 total; 30 s budget per media type), 480p/720p/1080p on the API. No seed [D-SD25-R2V; EST].
- Strengths: multi-angle object fidelity [B-ADH], anatomy through transformations, lip-sync, reflections [B-SD25VS], realism at 720p [YT:UxwV16jDglA@17:17], the best editor tested [YT:UxwV16jDglA@21:12], and about 20 % better adherence than 2.0 [B-SD25HF] (vendor claim).
- Weaknesses: uncontrolled music [YT:RpsEdtUJCnU], softened text [B-ADH], >3 characters [YT:lkL8mlpVScY@13:14], 2.4× the price of 720p at 1080p [EST].

**Seedance 2.0:**
- 4–15 s, 9 img / 3 vid / 3 audio. Native 480p/720p per ByteDance [BD-SD2]. Higgsfield offers 1080p and 4K [EST], probably upscaled [unverified].
- About 35 % cheaper than 2.5. It obeyed "no BGM" [YT:RpsEdtUJCnU@01:47].
- On 15 s scenes it "rushes" and hides failures with cuts [B-SD25VS].

**Cinema Studio 4.0:**
- Seedance 2.5 underneath [YT:mJD-1QSDKPQ@00:00]. Typed enums for camera, lens, aperture, light, genre, era (1960s–2020s on the API), pacing, 50 palettes. `<<<image_N>>>` tokens. 480/720 on the API [D-CS4; EST].
- Most constraints retained [B-ADH].
- Web-only extras: Emotion Wheel (`@name Joy`), hex palettes, forward/backward extend [B-CS4; YT:mJD-1QSDKPQ].
- Presets are sometimes ignored [YT:2a_rRtFSRec@13:11].

**Kling 3.0:**
- 3–15 s; multi-shot ≤6 (API) with per-shot prompts; start/end frames; Elements (web-created IDs only).
- Native audio in five languages with `Name (tone): line` [D-K3; K-GUIDE].
- Strengths: emotion and expressions [YT:b_RghITuQQM], single-move product inserts [LEDGER], text preservation from the input image [K-GUIDE].
- Weaknesses: lip-sync and morphing beyond about 10 s, and glitches with many Omni references [YT:b_RghITuQQM]. "Point left" can mirror [LEDGER].

**Wan 3.0:**
- 2–30 s; r2v up to 10 img / 5 vid / 5 audio (WAV/MP3; ≤30 s each type on Higgsfield), document or link refs, nonzero seed, default 1080p [D-WAN3; EST].
- Strengths: identity lock and physics (glass, billiards) [ATLAS-WAN], the cheapest real audio-driven lip-sync [LEDGER].
- Weaknesses: unrequested cuts and dissolves in long takes, image-prompt conflicts, on-screen text, and music lip-sync [ATLAS-WAN; BFA-WAN].

---

## 10. Sources

**Live API (free) [EST]:** `HF_AUTH_VIA_PROXY=1 python3 skills/ad-director/scripts/hfgen.py schemas|estimate`, run 2026-10-09. Prices are list USD before the account's 15 % Kling/Wan-Prime discount.

**Higgsfield docs:**
- D-SD25-R2V https://docs.higgsfield.ai/docs/models/seedance-2-5/reference-to-video
- D-SD25-I2V https://docs.higgsfield.ai/docs/models/seedance-2-5/image-to-video
- D-SD25-EXT https://docs.higgsfield.ai/docs/models/seedance-2-5/video-extend
- D-SD25-EDIT https://docs.higgsfield.ai/docs/models/seedance-2-5/video-edit
- D-K3 https://docs.higgsfield.ai/docs/models/kling-3/pro-image-to-video
- D-KO3 https://docs.higgsfield.ai/docs/models/kling-o3/image-reference and /first-last-frame
- D-WAN3 https://docs.higgsfield.ai/docs/models/wan-3/reference-to-video
- D-CS4 https://docs.higgsfield.ai/docs/models/cinema-studio-4/generate
- D-BILL https://docs.higgsfield.ai/docs/concepts/billing-and-retention

**Higgsfield blog:**
- B-SD25G https://higgsfield.ai/blog/seedance-2-5-prompting-guide
- B-SD25VS https://higgsfield.ai/blog/seedance-2-5
- B-SD25HF https://higgsfield.ai/blog/seedance-2-5-on-higgsfield-2026
- B-CS4 https://higgsfield.ai/blog/cinema-studio-4-0
- B-ADH https://higgsfield.ai/blog/ai-video-prompt-adherence-comparison
- B-FAIL https://higgsfield.ai/blog/why-ai-video-generations-fail
- B-DIST https://higgsfield.ai/blog/how-to-avoid-distortions-ai-videos
- B-HANDS https://higgsfield.ai/blog/ai-video-hands-faces
- B-MIST https://higgsfield.ai/blog/ai-video-prompt-mistakes
- B-CAM https://higgsfield.ai/blog/ai-video-camera-control
- B-K3 https://higgsfield.ai/blog/Kling-3.0-is-on-Higgsfield-User-Guide-AI-Video-Generation
- B-CAR https://higgsfield.ai/blog/ai-car-commercial-youtube-guide
- B-LIP https://higgsfield.ai/blog/make-ai-lipsync-videos

**Model makers:**
- BD-SD2 https://arxiv.org/abs/2604.14148 (Seedance 2.0 report)
- K-GUIDE https://kling.ai/quickstart/klingai-video-3-model-user-guide
- K-AUDIO https://kling.ai/blog/kling-video-3-omni-native-lip-sync-audio-guide
- COMFY-WAN https://docs.comfy.org/tutorials/partner-nodes/wan/wan3-0 (partner docs for Alibaba Wan 3.0)

**Third-party tests and guides (vendor-authored; treat as indicative):**
- REP https://replicate.com/blog/seedance-2
- ATLAS-WAN https://www.atlascloud.ai/blog/guides/wan-3-0-review
- ATLAS-SD25 https://www.atlascloud.ai/blog/tips/how-to-write-seedance-2.5-prompts
- SEG-SD25 https://blog.segmind.com/the-official-seedance-2-5-prompt-guide-bytedances-six-part-formula-explained-with-examples/
- BFA-WAN https://blog.buildfastwithai.com/wan-3-0-review-accuracy-price-is-it-worth-it-2026
- MORPHIC https://morphic.com/resources/how-to/seedance-2-prompts-flagged-how-to-fix
- KCFG https://www.segmind.com/models/kling-2/api and https://claudeskills.info/ko/skills/prime-skills/runcomfy-agent-skills/kling-3-0/
- SEED: there is no primary source on seed vs resolution, so the reasoning is our inference. Context: https://www.atlascloud.ai/blog/guides/wan-3-0-review (fixed-seed tests at a single resolution).

**Creator prompt libraries:**
- GH-ZERO https://github.com/ZeroLu/awesome-seedance (incl. @BFAVicky script-image prompt https://x.com/BFAVicky/status/2020267913316561195 and @johnAGI168 racing prompt https://x.com/johnAGI168/status/2020515830874636716)
- GH-YOU https://github.com/YouMind-OpenLab/awesome-seedance-2-prompts (No. 6 street-racing time-coded prompt)

**YouTube transcripts** (fetched with yt-dlp auto-subs; `@mm:ss` = transcript time):
- UxwV16jDglA — Dan Kieft, "Seedance 2.5 is an ABSOLUTE MONSTER"
- FqZ1CqJZZIs — AI Guy, "Seedance 2.5 Full Tutorial"
- 2b3Z4rW5VJc — Youri van Hofwegen, "STOP Wasting Credits & Master Seedance 2.5"
- StX3eflYq_o — Dan Kieft, "10+ Seedance 2.5 Prompts"
- Zo8KaTs0l6k — Dan Kieft, "Ultra Realistic AI Videos using Seedance 2.5"
- lkL8mlpVScY — Dan Kieft, "Master Seedance 2.0 in 25 min"
- tZReV23ncuc — Noble Goose, "ULTIMATE Seedance 2.0 Prompting Guide"
- HE9HJY2SLl0 — TommyGuywithAI, "AI Video Dialogue with Kling 3.0"
- 6qyDrGjOJQs — Magnific, "Kling 3.0 Multi Shot Mode"
- mJD-1QSDKPQ — Creating with Conor, "Cinema Studio 4.0"
- 2a_rRtFSRec — Aaron Randall, "Higgsfield Cinema Studio 4.0"
- luz_IRSzlDo — AI Creator Tools, "Best AI Tool for Car Ads? Seedance vs Happy Horse"
- 4zu2CclB-EI — Tao Prompts, "EPIC Fight Scene With AI"
- RpsEdtUJCnU — The AI Filmmaking Advantage, "Seedance 2.5 fight scenes… until they fix THIS"
- XJnpH0XtgXM — Oga AI, "PERFECT AI Lip-Sync Music Videos (Seedance 2.0)"
- ZsrhdgG0I1E — Youri van Hofwegen, "Consistent AI Characters in Higgsfield"
- GNxmt_4IifA — Higgsfield AI, "How I Built a Car Commercial With AI (Every Prompt I Used)"
- SvhFnN-axJw — Creating with Conor, "Stop Wasting Credits on Seedance 2.0"
- b_RghITuQQM — Dan Kieft, "Master Kling 3.0 in 25 Minutes"
- HTBfxEqDCdU — Sebastien Jefferies, "Kling 3.0 Like A PRO"
- tqZ0JuUevwA — Jack Vs. AI, "Kling 3.0 for AI Filmmaking"
- KrEO2Hzv-PY — Rourke Heath, "Cinematic AI Films With Kling 3.0"
- ikPGQGoUjQ0 — Yaroflasher, "Seedance 2.0 Video Reference Tutorial"

URL form: `https://youtu.be/<id>`. Transcripts without timestamps (the last six) are cited by video.

**Internal evidence [LEDGER]:**
- `research/ai-video-reels/lab/experiments/W01_site_films/ledger.md` (paid runs and measured sync offsets)
- `research/ai-video-reels/lab/experiments/F09_heist/plan_heist15.json` (the rejected one-take heist prompt)
