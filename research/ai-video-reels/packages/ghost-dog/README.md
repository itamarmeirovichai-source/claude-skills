# The Dog Who Saw the Ghost (PAWSTEAD, fictional brand): first portfolio piece

**The idea:** home security-cam footage at 3:12 AM, night vision. A golden retriever stares at an empty hallway and growls. A translucent ghost beagle appears, and all it wanted was a treat. They share. *"Some treats are worth coming back for."*
**Why it can work:** a Halloween hook with a warm, shareable ending ("whose dog also stares at nothing at 3 AM?"). The night-vision look **hides AI flaws**. Part 1 of a series. Engagement rank: 78/100 (shares 88).

## How to run it (Claude runs it once HF_KEY is in the environment)
```bash
H=../../../../skills/ad-director/scripts/hfgen.py
python3 $H check
python3 $H batch plan_A_hero_frame.json --budget 2 --dry-run && python3 $H batch plan_A_hero_frame.json --budget 2 --yes
#  → Claude reviews clips/F1_hallway_dog_t0*.png, copies the best to frames/F1.png
python3 $H batch plan_B_story_frames.json --budget 3 --yes
#  → best ones to frames/F2.png, F3.png, F4.png
python3 $H batch plan_C_video.json --budget 15 --dry-run   # check the price
python3 $H batch plan_C_video.json --budget 15 --yes
#  → take QC, best ones to clips/pick_S1..S3.mp4 + end card to clips/endcard.png
python3 ../../../../skills/reel-studio/scripts/reelstudio.py render edit.json
python3 ../../../../skills/ad-director/scripts/director.py qc out/ghost_dog_v1.mp4 --duration 14.7 --one-take
```
**Expected budget:** about $1 for images + about $8–15 for video (3 shots × 3 takes) = **about $10–16**. Verify with `--dry-run` before running.

## Edit (edit.json, ~14.7 s)
| Time | Shot | Caption |
|---|---|---|
| 0–5 | S1: the dog stares and growls; a glow takes shape | "Our camera caught this at 3:12 AM" |
| 5–10 | S2: the ghost wags its tail; both look at the jar | — |
| 10–13 | S3: both of them chewing treats | "Some treats are worth coming back for." |
| 13–15 | End card: PAWSTEAD jar | "PAWSTEAD · Part 1" |
Permanent elements: a "CAM 02 · HALLWAY" chip, an "AI-generated" label, -14 LUFS.
**Comment to pin:** "Whose dog also stares at nothing at 3 AM? 👻"

## QC focus
- K4: the dog's face stays identical across shots.
- K8: night-vision flicker is fine as a style, but no morph between the dogs.
- The ghost stays translucent the whole time.
- There's no text in the AI frame.
