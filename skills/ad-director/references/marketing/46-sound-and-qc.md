# 46: Sound design, lip-sync and automated QC (catch it before we pay, prove it after we render)

Why this exists: our films were rejected for four kinds of fault:
- sound that does not match the action;
- lips that do not match the words;
- continuity breaks (AURUM v1: the glass changed shape between shots);
- seams and physics errors (the F09 heist).

Each fault was found only after we had paid for the generation. This doc has the research, then the tools in
`scripts/qc/` that measure each fault, then the proof that the tools catch our real failures.

**Workflow:** fill in `scripts/qc/preflight.md`, then generate, then run `qc_report.py` (on every take and every
final), `lipsync_check.py` (on every talking clip) and `continuity_check.py` (on every multi-shot film). Ship only
when the numbers in preflight section 7 pass.

---

## 1. The 8 findings that matter most

1. **Every final we delivered fails true peak, and two are 2.5 LU too quiet.**
   - True peak: AURUM v3 -0.5 dBTP, F05 Tabletop -0.5, F06 VESPER **+1.7** (clipping), F08 dive -0.9, F09 heist -0.7.
     The target is ≤ -1.0 dBTP.
   - Loudness: AURUM v3 is -16.6 LUFS and VESPER is -16.3 LUFS.
   - Cause: `alimiter=limit=0.9` is a sample-peak limiter. AAC encoding then overshoots.
   - Fix: master with `loudnorm=I=-14:TP=-1.5:LRA=11` (two-pass), or follow alimiter with a true-peak check in `qc_report`.
2. **Instagram plays reels at about -14 LUFS, and we measured this ourselves.**
   - 10 viral reels downloaded from Instagram measure -14.1 to -15.2 LUFS integrated (8 of the 10 are within 0.1 LU of -14.1).
   - Their true peaks run from -2.9 to +2.2 dBTP. Normalization is a gain change, not a limiter, so our own true
     peak survives as delivered.
   - Raw native audio from Seedance sits at -22 to -25 LUFS (F07 -25.4, F09 -22.7, F08 -22.4). It always needs
     8-11 dB of gain plus limiting.
3. **One global lip-sync delay was wrong for 4 of our 5 checked lines.**
   - We baked +125 ms into every W06 line because "the mouth lags 0.12 s".
   - SyncNet measured each raw Wan render on its own:
     - v1, v2 and v4c are within -40 ms (fine as rendered);
     - **v3 is 280 ms late**, consistent in all five 2 s windows, and confirmed by eye: the lips stay closed for the
       "B" of "Black" until +0.28 s.
   - So the shipped keyed clips are off in both directions:
     - v1, v2 and v4 have their audio **160 ms late**, past the BT.1359 detectability limit of 125 ms;
     - v3 has its audio **160 ms early**, past the 45 ms limit.
   - Fix: measure each clip and apply its own offset. A lip-sync model's output is not uniformly late.
4. **SyncNet confidence separates a speaking mouth from a mismatched or hidden one.**
   - Vee lines that are correct score 6.7-7.7, like real video (Wav2Lip reports LRS2 real-video LSE-C ≈ 7.8).
   - The right face with the wrong line scores 1.5-1.9.
   - The rejected take v4_old scores 2.65, so the tool independently agrees with the human reject.
   - Otto's moustache-covered mouth scores 0.4-0.85. That clip cannot be verified, so treat it as VO-style and
     never claim lip-sync for it.
5. **The AURUM v1 vessel change is measurable before anyone watches it.**
   - DINOv2 similarity of the "glass" crops across shots: v1 (tumbler, flute, can, iced tumbler) scores a mean of
     **0.34**, and 4 of its 6 pairs are below 0.45.
   - v3 (one glass) scores a mean of **0.69**. Its only low pair (0.50) is a hand covering the empty glass, which
     is the reason to score the whole set and not single pairs.
6. **Native audio puts sounds early, and sometimes late.**
   - F09: the foam-"shot" burst starts at 11.21 s, but the spray only appears at 11.42-11.46 s (**5-6 frames early**).
   - F09: the landing thud is at 7.175 s, but the seat contact is at 6.96-7.00 s (**4-5 frames late**).
   - Netflix QC treats 2 frames or more as an issue, and editors place hard SFX on the contact frame or 1-2 frames
     early. Keep native ambience. Re-place or replace every hard SFX that is more than 2 frames off.
7. **The heist's real fault is coverage and physics, not identity.**
   - The cut detector finds **one camera move of 13.9 s**, with its only hard cut at the packshot.
   - Frame drift flags a "teleport" at 2.2-3.0 s, where the shot goes from the rooftop to the canopy to an aerial
     street view within one second.
   - SFace says Otto's identity **held**: 25 of 28 face samples match the reference, and the misses are blur and
     false detections.
   - So the tool confirms the owner's note ("not a real chase"). Use `qc_report --max-shot 4` for action films.
8. **Frozen frames hide inside our "finished" one-takes.**
   - AURUM v3 shows a 34-frame freeze during the drink (13.96-15.33 s), so the gulp plays over a still picture.
   - VESPER has three short freezes at 5.1-6.7 s. F08 has a 0.6 s held opening.
   - AURUM v1 had 32 frames frozen at the same beat, so this is the model stalling under a slowdown (`setpts`
     ×1.15). It is not a one-off.
   - Rule: never slow a Kling clip that already ends on a hold. Trim the hold instead.

---

## 2. Research: sound design for 15-30 s social ads

### 2.1 Layering
A designed hit is three layers on one frame:
- a **transient** (click, snap or tick, 0-30 ms) that sells the sync;
- a **body** (thud, pour or whoosh) that sells weight;
- a **tail** (room, reverb or ring-out) that sells the space.

Commercial hits add a sub or bass layer and often a pre-roll riser that *ends* on the frame
([general practice; RouteNote, MusicTech hit-point guides](https://licensing.routenote.com/blog/editing-music-for-video-content/)).

Foley editors keep **each prop on its own track** so it can be nudged and levelled alone (Pop Tips ep. 2,
[YT:l1C1ogCG8Lg](https://www.youtube.com/watch?v=l1C1ogCG8Lg)). Cloth is mixed "very faint". Steps are layered
from 2-3 recordings to get one character ([YT:5m1I5_J1Bu4](https://www.youtube.com/watch?v=5m1I5_J1Bu4) @0:26-12:41).

For our 15-30 s format, the hierarchy is: VO/dialogue, then the hero SFX on the product, then music, then ambience.
- Duck the music 6-10 dB under VO.
- Leave 0.3-0.7 s of silence before the punchline or packshot. Silence is the loudest cue in a reel.

### 2.2 Foley timing (where the sound sits relative to the contact frame)
- **Netflix QC** classifies an effect 1 frame early or late as "FYI" and **≥ 2 frames as an "Issue"**
  ([Netflix partner help, Sync Effects](https://partnerhelp.netflixstudios.com/hc/en-us/articles/115000533952-Sync-Effects)).
- Editors' consensus: put it on the contact frame or 1-2 frames early.
  - Sound-early is tolerated; sound-late reads as "rubbery".
  - When an effect "feels late" it is because the visual peak comes after contact, so nudge 1-2 frames earlier
    ([Morphic](https://morphic.com/resources/how-to/how-to-sync-sound-effects-to-video),
    [Gearspace](https://gearspace.com/threads/sync-issues.1192176/),
    [Krotos](https://webflow.krotos.studio/blog/sound-to-picture)).
  - This is practice, not a written standard. I found no studio style guide that codifies "N frames early".
- Perception thresholds (speech-based, so the closest proxy):
  - ITU-R BT.1359 detectability is **+45 ms audio early / -125 ms audio late**, and acceptability is +90 / -185 ms.
  - EBU R37 is tighter, at +40 / -60 ms end to end
    ([Wikipedia: A/V sync](https://en.wikipedia.org/wiki/Audio-to-video_synchronization),
    [TV Tech](https://www.tvtechnology.com/opinions/av-synchronization-how-bad-is-bad)).
  - Note the asymmetry: viewers tolerate *late* audio more (sound travels slower than light). But for a designed
    hard hit, late is what reads as fake, and that is why editors cheat early.
- **Our window** (`qc_report.py`): PASS from 2 frames early to 1 frame late (-83 to +42 ms at 24 fps). WARN out to
  4 frames early or 2 frames late. Beyond that is FAIL.

### 2.3 Music editing to picture
- Cut on the beat, never mid-beat. Edit on full bars or phrase ends.
- Put a **hit point** (a chord change, drop or stab) on the reveal, the text super or the product moment.
- If a hit point falls off the grid, move it with a small tempo change (≤ 1-2 BPM), with a time-signature trick, or
  by placing a stab on the frame
  ([RouteNote](https://licensing.routenote.com/blog/editing-music-for-video-content/),
  [MusicTech hit points](https://www.musictech.net/tutorials/logic-tutorial-producing-music-to-picture-part-two-working-with-hit-points/)).
- Ads need a **button ending** (a final chord that rings out), not a fade. A cutdown keeps the tempo of the full cue
  ([Taxi forum](https://forums.taxi.com/post521555.html)).
- Do not chase every beat: cut to the story and let the beat support it.

### 2.4 Loudness for Reels / TikTok / Shorts
- No platform publishes an official number. Vendor guides quote -14 LUFS, and some quote -10 to -13
  ([Opus](https://opus.pro/blog/best-loudness-normalizers), [OpenClip](https://openclip.app/learn/audio-normalization)).
- **Our measurement is the evidence:** Instagram-delivered reels sit at -14.1 LUFS (see finding 2).
- Deliver **-14 LUFS integrated ±1, true peak ≤ -1 dBTP** (-1.5 dBTP if the platform re-encodes to AAC, and it does).
- Check the mix on a phone speaker: under ~200 Hz is gone, so the "body" layer of a hit must have some 1-4 kHz content.

### 2.5 Native audio (Seedance 2.x, Veo 3): when to keep it and when to replace it
What native audio does well:
- It times ambience and incidental contacts (footsteps on gravel, cloth) to the picture.
- It renders diegetic sound with no prompt.
- It follows audio cues in the prompt; the more specific the prompt, the better the result
  ([cutout.pro guide](https://www.cutout.pro/learn/blog-seedance-2-0-audio-guide/),
  [ugccopilot](https://ugccopilot.ai/blog/seedance-2-native-audio-generation-guide/)).

Creators use symbols to separate diegetic sound from non-diegetic sound (music, added bass) inside the prompt
([YT:Zo8KaTs0l6k](https://www.youtube.com/watch?v=Zo8KaTs0l6k) @16:12-18:20). They also say: "if the sound effects
from Seedance aren't good enough", go to the edit, trim and re-time. In practice:

| Keep native | Replace / layer over |
|---|---|
| Room tone, wind, city bed, crowd | Brand VO, exact or legal script lines, any line in a second language |
| Incidental contacts whose sync `qc_report` confirms (≤ 2 frames) | Hard hero SFX more than 2 frames off (F09 foam: 5-6 frames early; landing: 4-5 frames late) |
| Speech in a single-shot talking take whose `lipsync_check` passes | The sonic logo, licensed music, the music bed (native music is uncontrollable and changes at every seam) |
| Rough-cut temp sound during blocking tests | Anything that must stay consistent across cuts generated separately |

Native audio is also mixed far too low (-22 to -25 LUFS), so it is always re-gained and limited in the master.

---

## 3. Research: lip-sync evaluation
- **SyncNet** (Chung & Zisserman, ACCV-W 2016, "Out of time") is a two-stream network that embeds 5 video frames of
  the mouth and 0.2 s of MFCC audio into a shared space.
  - It slides the audio ±15 frames: the shift with the minimum distance is the **AV offset**, and median minus
    minimum distance is the **confidence**.
  - The Wav2Lip paper turned these into the metrics LSE-D (lower is better) and LSE-C (higher is better). Real LRS2
    video scores about LSE-C 7.8 and LSE-D 6.7
    ([Wav2Lip, arXiv 2008.10010](https://arxiv.org/pdf/2008.10010)).
- Caveats from the literature:
  - LSE-C/D correlate weakly with human judgement, and they are sensitive to mouth cropping, brightness and image
    quality ([arXiv 2403.06421](https://arxiv.org/pdf/2403.06421)).
  - Errors in generated video are not always a single global offset ([FATE, arXiv 2608.01310](https://arxiv.org/pdf/2608.01310)).
  - So `lipsync_check --windows` also reports per-2 s offsets.
- **Mouth openness vs the audio envelope** (the classic landmark method, without a learned model): our prototype on
  the W06 clips with landmark-stabilized mouth crops was **not reliable**.
  - On 4-7 s clips, the correlation between a wrong line and the mouth (0.3-0.5) overlapped with the correct line.
  - In natural speech the mouth also moves 100-300 ms before the sound at phrase onsets.
  - It survives in the tool only as a no-torch fallback that can flag gross failures and never certifies PASS.
- For non-speech audio-visual sync (generated SFX):
  - **Synchformer/DeSync** tracks offsets best.
  - **AV-Align**, the energy-peak vs motion-peak IoU that our onset/motion table resembles, is the weakest standalone
    metric: about 0.53 AUROC in JavisDiT's test, and a 0.16 correlation with humans
    ([JavisDiT, arXiv 2503.23377](https://arxiv.org/pdf/2503.23377);
    ["What do A/V sync metrics measure", arXiv 2608.25157](https://arxiv.org/pdf/2608.25157)).
  - That is why `qc_report` treats its alignment table as a pointer and always produces `onset_zoom.jpg` for a
    by-eye check.

## 4. Research: automated video QC
- **Shot boundaries:**
  - PySceneDetect's ContentDetector averages HSV pixel change. Its AdaptiveDetector divides that change by a rolling
    average, which suppresses false cuts from fast camera moves (defaults: ratio 3.0, min content 15)
    ([PySceneDetect docs](https://www.scenedetect.com/docs/head/api/detectors.html)).
  - TransNetV2 is the learned state of the art (F1 77.9 on ClipShots) ([arXiv 2008.04838](https://arxiv.org/pdf/2008.04838)).
  - We implement the adaptive HSV method plus a flash guard, with no model download.
- **Flicker / temporal consistency:**
  - VBench "temporal flickering" is the mean absolute frame difference.
  - "Subject consistency" is the DINO feature similarity of each frame to the first and previous frames.
  - "Background consistency" uses CLIP features, but it penalises legitimate camera moves
    ([VBench++](https://arxiv.org/pdf/2411.13503), [EntityBench](https://arxiv.org/pdf/2605.15199)).
  - We use DINOv2-small (VBench's choice of family) for drift and seams, and frame-mean luma residuals for flicker.
- **Identity drift:**
  - Face embeddings, specifically SFace in OpenCV's model zoo, with a cosine threshold of 0.363 for "same person".
  - The faces are tracked inside a shot and compared to their own start, to the references, and clustered across shots.
- **Product / label drift:**
  - DINOv2 crops of a named prop, compared as a set.
  - A multi-scale window search against a packshot to find where the product is visible.
  - OCR of the label would be the next step (no Tesseract was available here).
- **Frozen / flash frames:** these are simple pixel statistics, but AI pipelines produce both. Freezes come from slowed
  holds, and flashes from glare seams.

---

## 5. The tools (`skills/ad-director/scripts/qc/`)

Install with `pip install -r scripts/qc/requirements.txt`, plus optional torch CPU for SyncNet. The small models
download into `~/.cache/ad-director-qc`. Full usage is in `scripts/qc/README.md`.

| Tool | Catches | Key outputs |
|---|---|---|
| `preflight.md` | physically impossible shots, unplanned sounds, unlocked identity/vessel, unpriced takes, no pass criteria | a filled checklist; `events.csv` for qc_report |
| `qc_report.py VIDEO [--events events.csv] [--stage take] [--max-shot 4]` | loudness/TP, cuts and coverage, flash frames, frozen frames, flicker, SFX early/late | `report.html/.md/.json`, `strip.jpg` (every 0.5 s), `onset_zoom.jpg` (±4 frames per strong onset), SVG timelines |
| `lipsync_check.py VIDEO [--audio line.wav] [--audio-delay s] [--windows] [--box x,y,w,h]` | mouth offset in ms, mismatched/hidden mouths, drift | `lipsync.json`, `crops.jpg` (what the model saw) |
| `continuity_check.py VIDEO [--ref-face n=img] [--cast N] [--object n=t:x,y,w,h] [--ref-object n=img] [--seamless --seams ...]` | prop/vessel shape changes, identity morphs, extra faces, product presence, bad seams, in-shot teleports | `continuity.md/.json`, `objects.jpg`, `faces.jpg`, `seams.jpg`, `ref_<name>.jpg` |
| `validate_past_films.sh OUT` | reproduces everything in section 6 from the local lab media | reports under OUT (never commit) |

Thresholds and why:

| Gate | Value | Source / calibration |
|---|---|---|
| Loudness | -14 ±1 LUFS, TP ≤ -1 dBTP | our IG measurement (-14.1); vendor guides |
| SFX sync | PASS -2..+1 frames, WARN -4..+2, else FAIL | Netflix QC (≥ 2 frames = issue), editors' early bias |
| Lip offset | PASS -80..+40 ms, WARN to -125/+90, FAIL beyond | BT.1359 detectability +45/-125 ms; SyncNet step is 40 ms |
| Lip confidence | PASS ≥ 5, WARN 3-5, FAIL < 3 | W06: synced 6.7-7.7, wrong line 1.5-1.9, rejected take 2.65 |
| Face identity | SFace cosine ≥ 0.363; drift < 0.30 on 2 sharp samples in a row | OpenCV SFace threshold; blur filter (Laplacian var < 60) |
| Object set | mean pair DINOv2 ≥ 0.50 and < 2 pairs below 0.45 (WARN below 0.60) | AURUM v1 mean 0.34 vs v3 mean 0.69 |
| Product present | window search ≥ 0.35 vs the packshot | heist can in hand 0.50, cans in bag 0.36, absent ≈ 0.1 |
| Frozen | ≥ 6 identical frames WARN, ≥ 1 s FAIL | a held packshot is allowed: read the strip |

---

## 6. Validation on our films (proof)

All runs are local, with zero generation spend. The media and reports stay out of git.

### AURUM Top Shelf
| Version | Check | Result |
|---|---|---|
| v1 (rebuilt from the v1 clips in the original assemble order) | `continuity --object glass` at 9.5/13.0/23.5/29.0 s | **FAIL**: pairs 0.16-0.54, mean 0.34. The `objects.jpg` sheet shows tumbler → flute → can → iced tumbler |
| v1 | `qc_report --stage take` | frozen 13.71-15.00 s (32 frames) and 24.12-25.00 s; white hold 19.67-21.08 s (the glare seam) |
| v3 (shipped) | `continuity --object glass` | **WARN**, mean 0.69 (one hand-occluded pair at 0.50). Identity: 2 faces, 55/55 samples match the Otto/Vee refs. Seams: 6 of 6 match (≥ 0.70) |
| v3 (shipped) | `qc_report` | **FAIL**: TP -0.5 dBTP, -16.6 LUFS, frozen drink 13.96-15.33 s (34 frames), Vee freeze 25.12-25.96 s. White hold 21.79-22.29 s (designed seam) |

### F09 heist (Seedance 2.5 r2v, native audio)
| Check | Result |
|---|---|
| `qc_report --max-shot 4` | **one 13.9 s camera move**, with the only hard cut at the packshot (13.88 s) → coverage WARN. Raw audio -22.7 LUFS. Final: TP -0.7 dBTP FAIL |
| `--events` (chute 2.25, landing 7.0, foam hit 11.46) | chute +14 ms PASS. **Landing +175 ms FAIL** (seat contact at 6.96-7.00 s; thud at 7.175 s). Foam: nearest onset -82 ms, but `onset_zoom.jpg` shows the burst starting at 11.21 s, 5-6 frames before the spray |
| `continuity --fps 4 --ref-face otto,vee --cast 2` | in-shot jumps at 2.2-3.0 s (rooftop → canopy → aerial street within 1 s). Identity held: 2 identities, 25/28 samples match the refs (the misses are a blurred profile and two non-face detections) |
| `continuity --ref-object can` | can found at 11 s (0.50, in hand) and 13 s (0.36, in the bag). ≈ 0.1 everywhere else: the product reads in only 2 of 15 one-second samples |

### F07 native-audio test (known good)
`qc_report --stage take`: one continuous shot, no flash frames, no freezes, no flicker, TP -2.6 dBTP. Loudness is
-25.4 LUFS (INFO for a take; it needs +11 dB in the master).
- Strongest onset (the can "pssht") at 0.14 s, with the spray already visible in frame 1.
- The 7.28 s onset is the pour cutting off as the can tilts back. That frame has no motion peak, so the table
  flags it: this is a known limit of motion-peak pairing, and the zoom sheet confirms the sync by eye.

### W06 lip-sync (Wan 3.0 r2v driven by our TTS lines)
| Clip | Raw render + its line | Shipped keyed clip (+125 ms baked) |
|---|---|---|
| v1 Vee | -40 ms, conf 6.88 PASS | **-160 ms** (audio late) FAIL |
| v2 Vee | -40 ms, conf 6.92 PASS | **-160 ms** FAIL |
| v3 Vee | **+280 ms** (mouth late; every window +280..+320) FAIL | **+160 ms** FAIL |
| v4c Vee (chosen) | -40 ms, conf 7.74 PASS | **-160 ms** FAIL |
| v4b Vee (retake) | -80 ms, conf 7.72 PASS | - |
| v4_old Vee (rejected) | conf **2.65** FAIL (lips do not follow the line) | - |
| o1-o4 Otto (moustache) | conf 0.56-0.77: no visible mouth, cannot be verified | conf 0.44-0.85 |

Controls:
- v2 face with the v3 line: conf 1.54 FAIL. v4c face with the v2 line: conf 1.88 FAIL.
- v4c with its own line delayed +200 / -200 / +80 ms: measured -240 / +160 / -120 ms. Each shift is recovered
  within 1 frame of the -40 ms baseline.
- The heuristic engine on the same clips: v4c WARN (conf 3.2), v4_old FAIL, wrong line FAIL. It catches the gross
  cases but never certifies a PASS.
- **Action:** re-bake v1/v2/v4 with a delay of 0 (or -40 ms) and v3 with +280 ms, then re-run
  `lipsync_check keyed/*.mp4` until PASS.

### Synthetic identity morph (control)
A Vee → Otto dissolve in a locked frame gives `continuity_check`:
- **FAIL identity drift**: track min sim 0.08;
- **FAIL faces vs reference**: 8 of 18 samples below 0.363.

Known limit: the centroid clustering chained both people into one "identity" (the cast count passed), so rely on the
drift and reference checks for morphs.

### Other finals (qc_report)
| Film | Loudness | True peak | Other |
|---|---|---|---|
| F05 Tabletop | -13.6 PASS | **-0.5 FAIL** | frozen 19.38-19.96 s (15 frames) |
| F06 VESPER | -16.3 WARN | **+1.7 FAIL** | 3 short freezes 5.1-6.7 s |
| F08 Dubai dive | -14.6 PASS | **-0.9 FAIL** | frozen 0.21-0.79 s at the hook; flicker jump 12.6 |
| Reference reels (10, from Instagram) | -14.1 … -15.2 | -2.9 … +2.2 | - |

---

## 7. Operating rules (add to every job)
1. **Before generating:** fill in `preflight.md`. No paid call while any box is unticked, and every sound event
   needs a planned frame.
2. **After every take:** run `qc_report.py --stage take`. Read `strip.jpg` and `onset_zoom.jpg` before choosing.
3. **Talking clips:** measure each clip with `lipsync_check.py --audio line.wav --windows`. Bake that clip's own
   offset, then re-run the check on the baked file.
4. **Multi-shot or seamed films:** run `continuity_check.py` with the refs, `--cast` and the prop boxes from the
   preflight. Object mean below 0.6 or identity drift = re-key the shot before paying for motion.
5. **Final:** `qc_report.py final.mp4 --events events.csv` must PASS on loudness, true peak, flash and sync.
   Every remaining WARN gets a by-eye note in `06-qc.md`.
6. **Never** put a voice on a face whose `lipsync_check` confidence is below 3. Use VO with the mouth off-screen,
   or a super.
