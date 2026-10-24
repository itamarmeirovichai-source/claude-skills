# Red Light v4 re-cut: QC notes (2026-10-09)

$0 re-cut (ffmpeg + OpenCV, no generation), owner decision 7. Fixes WEAKNESSES #5, #13 (freeze, duplicate frames) and #24, per doc 64 and `vxo-film` Steps 7-8. Build: `python3 assemble_v4.py --scratch <scratchpad>`. Media stays in the scratchpad `films/` folder and is never committed.

Sources: the native-sound take `clips/RL30_480_t01.mp4` (480x854, 24 fps), `audio/vo1.mp3` and `audio/vo2.mp3`, and `ref/can.png` (the product photo, the only legible label source). The film's own can is a blank gold cylinder at about 4% of frame, so its frames cannot carry a legible label.

## Outputs (scratchpad `films/`)
| File | Format | Frames | LUFS (I) | True peak | LRA | qc_report |
|---|---|---|---|---|---|---|
| VXO_red_light_v4_30s.mp4 | 1080x1920, 30.000 s | 720 | -14.2 | -1.8 dBTP | 7.7 | WARN (onset heuristic only), 0 FAIL |
| VXO_red_light_v4_15s.mp4 | 1080x1920, 15.000 s | 360 | -14.2 | -1.9 dBTP | 3.7 | WARN (onset heuristic only), 0 FAIL |
| VXO_red_light_v4_15s_4x5.mp4 | 1080x1350, 15.000 s | 360 | -14.2 | -1.9 dBTP | 3.7 | WARN (onset heuristic only), 0 FAIL |

Loudness: two-pass `loudnorm=I=-14:TP=-2`, AAC 256k. The figures above were measured on the encoded files with `ebur128=peak=true`. The limiter fallback was not needed.

## Before / after (30 s)
| Check | v3 (VXO_aurum_red_light_30s) | v4 |
|---|---|---|
| qc_report verdict | FAIL | WARN |
| Frozen frames | 15.67-18.50 s (69 fr) + 20.50-20.71 s (6 fr) | none |
| Duplicate single frames | 40 (WARN) | below the 5% threshold (no WARN) |
| Product first legible | 19.5 s, about 4% of frame, illegible | 0.67 s; the can is 1500 px tall (78% of height, about 37% of area); label taken from the client photo |
| Product on screen | once | 0-1.5 s, 17.1-21.1 s, 24.1-30 s |
| Super by 1.0 s | none | "Worth stopping for." from 0.08 s |
| Super position | y about 1550 (under the platform UI) | every super has its glyphs between y 244 and 630; box 240-1260 |
| End | wordmark only | can packshot + AURUM wordmark, then the offer card |
| LUFS / TP | -14.7 / -1.5 | -14.2 / -1.8 |
| SSIM vs a 480-wide round trip | 0.987-0.994 (doc 64) | 0.982 (Y 0.911). This passes the < 0.985 gate only because of the photo cards and the grain. The chase shots still carry 480p detail; see decision 9. |

## Edit decision list (30 s master)
| Timeline (s) | Source | Note |
|---|---|---|
| 0.000-0.667 | raw 20.292-20.958 s, 4x punch-in on the hand-off | flash-forward: motion at frame 0; grab (onset 0.42 s) and fizz mist (onset 0.57 s, picture 0.58 s) with their own synced sound |
| 0.667-1.500 | can hero: ref photo cut-out over a blurred hand-off plate, 1.00 to 1.07 push, red/blue light sweep | fizz onset (raw 21.08 s) lands on the cut at 0.708 s; QC paired it at 0 ms |
| 1.500-17.125 | raw 0.000-15.625 s (shots 1-7) | the overhead stop ends at raw frame 374, before the 2.9 s freeze (raw 15.71-18.50 s) |
| 17.125-21.125 | raw 18.542-22.542 s | the hand-off (payoff of the cold open) |
| 21.125-24.125 | raw 23.042-26.042 s | light turns green, pull-away. VO1 at 21.425 s, two-line super 21.125-24.125 s |
| 24.125-27.000 | packshot: can 1080 px tall + "AURUM" wordmark | VO2 "AURUM. Sparkling yuzu." at 24.455 s |
| 27.000-30.000 | offer card: "Your first case, 20% off." + "AI-generated film" + can | swappable: `--offer "..."` (at most 7 words) |

15 s cut: the same cold open (0-1.5 s), then the burnout, handbrake turn, the cruiser, the red light, the overhead stop and the hand-off. From 12.25 s an end card shows the wordmark, the offer, the disclosure and the can. VO1 plays at 10.41 s. The 4:5 version is the same edit, centre-cropped from the 9:16 picture. Its supers and cards are laid out again for 1080x1350, with text at y 64-667.

## Native sound sync
- Every raw segment's audio is cut on the same frame as its picture (2000 samples per frame, with a 6 ms fade only at non-contiguous joins). So every native SFX keeps the generator's own sync, and no SFX was moved.
- The qc_report onset table flags these rows, and I checked each one:
  - 0.418 s: the hand closing on the can, the grip sound. It happens about 0.33-0.46 s on the 8 fps strip. QC paired it with the 0.667 cut instead.
  - 1.707 s: the raw 0.21 s siren whoop at the start of the burnout. This is native, and the same in v3.
  - 12.910 s and 16.057 s: raw 11.41 s and 14.56 s. These are native and were flagged identically in v3. The screech at 16.06 s lags the overhead stop by about 6 frames. That lag is the generator's, and only a regenerate or a hand-placed SFX fixes it.
  - 21.5-22.3 s and 24.54 s: the VO words, not SFX.
  - 15 s cut: 8.150 s (the same native screech) and 12.18/12.38 s (VO1 words).

## Manual checks done
- I looked at a 2 fps strip of all three files, with safe-box lines on the 30 s. All text is inside y 240-1260, x 120-960.
- I looked at an 8 fps crop strip of the hand-off (raw 20-22 s).
- 100% crops of the hero can (1.2 s) and the packshot (25.5 s) read "AURUM / SPARKLING YUZU" letter for letter. It is the client photo, so ΔE is 0 apart from the deliberate 0.86 grade.
- Super sizes: open 96 px, disclosure 60 px, VO line 88 px, wordmark 150 px, offer 96 px. Every super is at most 7 words. On-screen times meet the (words ÷ 3) + 1 s rule: open 2.1 s for 3 words, VO line 3.0 s for 6 words, offer 3.0 s for 5 words.

## Known limits (honest)
- The chase picture is still 480p detail, upscaled with lanczos and a mild unsharp mask. A real temporal upscaler is owner decision 9 (an A/B of at most $2).
- The can hero and the end cards are composites of the client photo, not filmed shots. They look like a product insert, not like a can inside the scene.
- File sizes (CRF 16 with grain) are 80 MB (30 s), 42 MB (15 s) and 31 MB (4:5). These are upload masters. Make a CRF 22 copy for the website.
- The "AI-generated film" super is shown for 0-3 s and on the end card, not for the whole film. Also switch on the platform's own AI label when posting.
- The offer "Your first case, 20% off." is a placeholder for an invented brand. A real client supplies a real offer.
