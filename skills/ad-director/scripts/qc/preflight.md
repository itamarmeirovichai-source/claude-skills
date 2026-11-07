# Preflight: fill this in BEFORE any paid generation

Copy this file into the job folder as `preflight.md` and fill every section. If a box cannot be ticked,
do not generate: fix the plan first. Each section exists because a past film failed on it:

| Section | The film that taught it |
|---|---|
| 1 shot list | F09 heist: one camera move carried the whole chase ("not a real chase") |
| 2 physics read | F09: the canopy opened at roof height, the car never turned, an impossible landing |
| 3 sound events | AURUM v1/v2: sounds placed on the plan's timings, not on the measured frames |
| 4 identity & product | AURUM v1: tumbler -> flute -> can -> iced tumbler between shots |
| 5 voice & lips | W06: one global +125 ms audio delay for every line (only v3 needed a delay, and it needed +280 ms) |
| 6 budget | Every failure above was found only after we had paid for the generation |
| 7 success criteria | "Looks good" is not a criterion: every gate below is a number a tool prints |

Job: ____________  Brand / product: ____________  Length: ___ s  Aspect: 9:16  Platform: Reels / TikTok / Shorts
Concept in one line: ______________________________________________

---

## 1. Shot list (the edit, not the prompt)

Genre grammar: product sensory films can be one continuous take. **Action, chase and stunt films need
6-10 shots with hard cuts** (see `references/marketing/41-action-realism.md`).

| # | t in-out (s) | Framing / lens | Camera move (a real rig?) | Action: start state -> end state | Model + mode | Key/ref image |
|---|---|---|---|---|---|---|
| 1 | 0.0-1.5 | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

- [ ] The hook lands in the first 1.0 s (an action or a sound, not a logo).
- [ ] Every seam of a "one-take" lands on a matched keyframe, or on full white/black, and never mid-flare.
- [ ] No shot is longer than the model's clean window (Kling orbit <= 2.5 s or <= 60 degrees; Seedance one-take <= 15 s).
- [ ] Each shot states its **end state**, because the next shot starts from it (the glass is full or empty, which hand holds it, where the can stands).

## 2. Physics read (ask of every shot: could a stunt crew film this?)

| # | Physical event | Real-world rule written into the prompt | Could a crew film it? (Y/N, how) | Rewrite if N |
|---|---|---|---|---|
| | e.g. drink | the level drops, the throat moves, the same vessel throughout | Y, locked-off medium | |
| | e.g. BASE jump | 150 m+ building, 2-4 s freefall, then the pilot chute and a jolt | Y, helmet cam + ground wide | |

- [ ] Gravity, timing and scale are plausible (falls take time, a liquid pours from above, cars weigh 1.5 t).
- [ ] Contacts are visible: the hand touches the can before it moves, and the glass touches the box before it stops.
- [ ] Nothing passes through glass, a wall or a body. No hands with extra fingers or duplicated props in the frame.
- [ ] Model filters: no person "falling" or "stepping off" a roof in Seedance (use Kling and a cabled stunt dive), and no real guns.

## 3. Sound events (which on-screen events need a sound, and who makes it)

One row per visible contact or action. This table becomes `events.csv` (`t,label`) for `qc_report.py --events`.

| t (s, planned) | Visual event (contact frame) | Sound | Source: native / Foley SFX / music hit / VO | Layering (transient + body + tail) | Must land |
|---|---|---|---|---|---|
| | can tab opens | pssht + click | SFX | click transient + hiss body | 0-2 frames before the contact |
| | glass set on the box | wood-glass knock | SFX | | on the frame |
| | cut to the packshot | music button / riser end | music | | on the cut |

Rules (see `references/marketing/46-sound-and-qc.md`):
- A hard SFX sits on the contact frame or 1-2 frames early, and never late. A sound two or more frames late reads as rubbery (Netflix QC flags >= 2 frames).
- The music is edited to the picture: cut on the downbeat, a hit point on the reveal, a button ending (not a fade), and 0.3-0.7 s of silence before the punchline.
- No voice on a face whose lips are not visible and synced. Use VO with the mouth off-screen, or a super.
- Native audio (Seedance / Veo): **keep** it for ambience and incidental contacts whose sync is verified. **Replace** it for brand VO, music, the sonic logo, anything that crosses a cut, and any event that `qc_report` shows more than 2 frames off.
- [ ] Every row above has a planned frame AND will be re-measured on the render (the onset-zoom sheet).
- [ ] Mix target: -14 LUFS integrated (+-1), true peak <= -1 dBTP, VO 6-10 dB above the music bed.

## 4. Identity and product references (lock them before generating)

| Asset | Reference file(s) | Locked descriptor (paste into EVERY prompt that shows it) | Must not change |
|---|---|---|---|
| Hero character | `ref/otto.png` | "same man as image 1: black waxed handlebar moustache, slicked dark hair, black turtleneck, charcoal blazer" | face, hair, moustache, wardrobe |
| Second character | `ref/vee.png` | | |
| Product | `ref/can.png` | "gold AURUM can, serif wordmark, matte finish" | label text, colour, proportions |
| Vessel / prop | `ref/glass.png` | "tall straight-sided plain glass, no stem, no ice" | shape, fill level continuity |

- [ ] Every keyframe that shows the product **in use** names the same vessel (AURUM lesson).
- [ ] Label-facing shots use push / rise / drift moves, not an orbit (an orbit morphs the label).
- [ ] The cast is counted: `--cast N` for `continuity_check.py`.
- [ ] Object boxes are noted per shot (`NAME=t:x,y,w,h`) so continuity can be measured after the render.

## 5. Voice and lips (only if someone speaks on camera)

- [ ] The mouth is visible in the shot that carries the line (a moustache or a hand over the mouth means VO only).
- [ ] The line audio is final BEFORE the lip-sync render (the render follows the audio, so a re-voice means a re-render).
- [ ] Test the cheapest path first (Wan 3.0 r2v with audio_urls, ~$0.10/s at 720p), with one clip before the batch.
- [ ] Plan to measure **each clip**: `lipsync_check.py clip.mp4 --audio line.wav`. Apply that clip's own offset, never a global one.

## 6. Budget (price it before spending)

| Stage | Model | Unit price | Takes | Subtotal | Gate before the next stage |
|---|---|---|---|---|---|
| Keyframes | | | | | the stills pass the identity/product check |
| Motion test (480p) | | | | | blocking + physics OK on the frame strip |
| Final takes (720p/1080p) | | | | | qc_report + continuity PASS |
| Lip-sync | | | | | lipsync PASS |
| Retake reserve (20-30 %) | | | | | |
| **Cap** | | | | | |

- [ ] `hfgen.py batch plan.json --dry-run` priced every job (no UNPRICED rows).
- [ ] Generate at 480p first for blocking; only takes that pass go to 720p/1080p.
- [ ] A kill rule is written down: after N failed takes of one shot, rewrite the shot instead of re-rolling it.

## 7. Success criteria (all numbers, checked by the tools after generation)

| Gate | Tool | Pass |
|---|---|---|
| Loudness | `qc_report.py` | -14 +-1 LUFS, true peak <= -1.0 dBTP |
| Flash / frozen frames | `qc_report.py` | no flash frames of 1-2 frames; no freeze >= 0.25 s that is not designed (a held packshot is OK) |
| Sound sync | `qc_report.py --events events.csv` | every planned event has an onset from 2 frames early to 1 frame late (confirm on `onset_zoom.jpg`) |
| Lip-sync | `lipsync_check.py` | confidence >= 5 and audio lead from -80 to +40 ms |
| Identity | `continuity_check.py --ref-face` | every hero face >= 0.363 to its reference; no drift inside a track; identities <= cast |
| Product / prop | `continuity_check.py --object / --ref-object` | object mean pair similarity >= 0.6, no pair < 0.45 |
| Seams (one-take) | `continuity_check.py --seamless --seams ...` | similarity across each seam >= 0.70 |
| Story | human | the hook, the twist and the brand-in-twist read without sound AND without captions |

Sign-off: plan reviewed by ________ on ________. Estimated spend: $____ (cap $____).
