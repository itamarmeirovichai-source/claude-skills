# ad-director QC tools: catch it before we pay, prove it after we render

Four pieces. None of them calls a paid API.

| File | When | What it answers |
|---|---|---|
| `preflight.md` | **before** any generation | Is the plan physically filmable? Which events need a sound? Which identity, product and vessel references are locked? What is the budget, and what are the numeric pass gates? |
| `qc_report.py` | after every render (takes and finals) | Cuts, a frame strip, audio envelope and onsets, motion peaks, onset-to-motion alignment in ms, LUFS and true peak, flash frames, frozen frames, flicker |
| `lipsync_check.py` | every talking clip | The audio-to-mouth offset in ms, and whether the mouth follows this line at all (SyncNet confidence) |
| `continuity_check.py` | every multi-shot / multi-seam film | Does the same face, product and glass stay the same across shots and seams? |

Background, thresholds and the validation on our own films are in
`references/marketing/46-sound-and-qc.md`. The older `director.py qc` (loudness, pacing, packshot colour,
safe-zone sheet) still works; these tools go deeper on sync and continuity.

## Install (once)

```bash
python3 -m venv ~/.venvs/adqc && . ~/.venvs/adqc/bin/activate
pip install -r skills/ad-director/scripts/qc/requirements.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu   # optional: SyncNet engine
```
ffmpeg and ffprobe must be on PATH. The first run downloads the small models into `~/.cache/ad-director-qc`
(set `AD_QC_MODELS` to move them, or `AD_QC_OFFLINE=1` to forbid downloads):
YuNet face detector (0.2 MB), SFace face embedding (37 MB), DINOv2-small quantized (24 MB) and SyncNet v2 (54 MB, from
the authors' site; loaded with `weights_only=True`). Every tool degrades gracefully: without DINOv2 it uses
colour/edge descriptors, without YuNet a Haar cascade, and without torch the heuristic lip engine.
Model files are never committed.

## Usage

```bash
Q=skills/ad-director/scripts/qc

# 1. Technical + sync report (HTML/MD/JSON + strip.jpg + onset_zoom.jpg). Exit code 0/1/2 = PASS/WARN/FAIL.
python3 $Q/qc_report.py final.mp4                       # deliverable: loudness and true peak are gates
python3 $Q/qc_report.py clips/T1_t01.mp4 --stage take   # raw take: loudness is INFO
python3 $Q/qc_report.py final.mp4 --events events.csv   # planned events from preflight (t,label per line)
python3 $Q/qc_report.py final.mp4 --audio-stem sfx.wav  # measure onsets on the SFX stem, not the mix

# 2. Lip-sync (SyncNet when torch is installed; otherwise a coarse heuristic that never certifies PASS)
python3 $Q/lipsync_check.py clips/v2_t01.mp4 --audio audio/v2.wav --windows
python3 $Q/lipsync_check.py keyed/v2.mp4                 # the clip's own (baked) audio
python3 $Q/lipsync_check.py clip.mp4 --audio line.wav --audio-delay 0.04   # try the fix before baking it
python3 $Q/lipsync_check.py clip.mp4 --box 300,200,260,300                  # force the face box (source px)

# 3. Continuity
python3 $Q/continuity_check.py final.mp4 --cast 2 \
    --ref-face otto=ref/otto.png --ref-face vee=ref/vee.png \
    --object glass=9.5:390,1095,180,390 --object glass=12.0:330,615,225,460 \
    --seamless --seams 4,9,13,17.35,22,26
python3 $Q/continuity_check.py heist.mp4 --no-faces --ref-object can=ref/can.png   # product search per second
```

Reading the outputs:
- `qc_report`: start with `strip.jpg` (red outline = a cut inside the interval, yellow = flash, blue = frozen), then
  `onset_zoom.jpg`. That sheet shows ±4 native frames around the strongest onsets, with the audio onset frame in purple
  and the paired motion event in orange. The alignment table is a **pointer**, not a verdict: motion peaks are not
  always contact frames (the same weakness the research found in AV-Align), so confirm every WARN/FAIL row by eye on
  the zoom sheet.
- `lipsync_check`: `audio_lead_ms > 0` means the sound comes before the mouth (the mouth is late), so delay the audio by
  that amount. Confidence < 3 means that this face does not speak this line (wrong audio, a hidden or static mouth).
  With `--windows` it reports per-2 s offsets, which shows drift and dead stretches.
- `continuity_check`: `objects.jpg`, `faces.jpg` (one colour per clustered identity), `seams.jpg` and `ref_<name>.jpg`
  are the evidence. Object consistency is scored on the whole set of crops (mean pair similarity), because hands and
  fill level legitimately change single pairs.

## Validation on our films (summary; details in doc 46)

| Film | Tool | Result |
|---|---|---|
| AURUM v1 (tumbler -> flute -> can -> iced tumbler) | continuity `--object glass` | FAIL: mean pair sim 0.34, 4 of 6 pairs < 0.45 |
| AURUM v3 (one glass) | continuity `--object glass` | WARN: mean 0.69. The one low pair (0.50) is a hand covering the empty glass |
| AURUM v3 final | qc_report | FAIL: true peak -0.5 dBTP, -16.6 LUFS, a frozen drink 13.96-15.33 s (34 frames) |
| F09 heist | qc_report | one camera move for 13.9 s (1 hard cut, at the packshot); foam "shot" sound 2-6 frames before the spray |
| F07 native-audio test | qc_report `--stage take` | clean picture (no flash/freeze/flicker); native audio at -25.4 LUFS needs +11 dB |
| W06 Vee raw renders | lipsync | v1/v2/v4c within -40 ms (PASS, confidence 6.9-7.7); **v3 mouth 280 ms late** (consistent in every window) |
| W06 shipped keyed clips (+125 ms baked) | lipsync | v1/v2/v4 audio 160 ms late (FAIL), v3 still 160 ms early (FAIL). The global delay was wrong |
| W06 v4_old (rejected) | lipsync | confidence 2.65 (FAIL): the lips do not follow the line |
| W06 Otto (moustache covers the mouth) | lipsync | confidence 0.6-0.8: cannot be verified by SyncNet (correctly reported as no visible sync) |
| Controls | lipsync | wrong line on the right face: confidence 1.5-1.9 (FAIL); +200/-200/+80 ms shifts recovered to within 1 frame |

Reproduce: `bash skills/ad-director/scripts/qc/validate_past_films.sh OUT_DIR` (reads the local lab media and writes
reports to OUT_DIR. The media and the reports are never committed).
