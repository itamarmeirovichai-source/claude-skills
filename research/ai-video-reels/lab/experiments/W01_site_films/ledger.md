# W01/W02/M03 spend ledger (2026-10-08). Site cap $50 (+$30 only for a researched idea); Vee + reel cap $20.

| Item | Model | $ est | Status |
|---|---|---|---|
| SOL 30 s one-take | Seedance 2.5 i2v 480p 30 s | 6.17 | PASS (no cuts, product stable) |
| VESPER 30 s one-take (orbit) | Seedance 2.5 i2v 480p 30 s | 6.17 | FAIL: orbit morphs bottle, double label at 18-22 s |
| VESPER 30 s retake (push-in only) | Seedance 2.5 i2v 480p 30 s | 6.17 | PASS |
| Otto K0/Kend + AURUM ref | Flare 2k x3 | 0.98 | done |
| AURUM K0/Kend | Flare 2k x2 | 0.64 | done |
| AURUM + OTTO 30 s one-takes | Seedance 2.5 i2v 480p 30 s x2 | 12.34 | PASS both |
| Otto UI green keys | Qwen edit x2 (1 failed take) | 0.15 | done |
| Otto UI clips x8 | Kling 3.0 std x7 + pro x1 | 3.12 | PASS (both points went screen-right: point_L = mirrored) |
| Vee green keys x4 (2 had a duplicate stopwatch) | Qwen edit | 0.16 | done |
| Vee pop clips x2 | Kling 3.0 std | 0.71 | PASS |
| **Site subtotal** | | **36.62** | |
| Vee explore x8 (7 returned) | Soul Cinema 720p | 0.03 | done |
| Vee master x2 | Flare 2k | 0.64 | done (t01 chosen) |
| Duo blocking still x2 | Flare 2k | 0.72 | done (t01) |
| Reel 30 s duo, audio-driven | Seedance 2.5 r2v 480p 30 s | 6.17 | PASS (one take, fast pans; lip-sync ~0.3 s lead corrected in mix) |
| **Vee/reel subtotal** | | **7.56** | |

Audio/voice: ElevenLabs Creator plan credits (music x4, SFX x4, ~25 TTS lines); no extra $.

Lesson: in Seedance one-takes an ORBIT around a glass product breaks product fidelity (shape morph + duplicated label). Use push/rise/drift moves for label shots.

## Round 2 (user: "train the characters, check thoroughly, then the reel")
| Item | Model | $ est | Status |
|---|---|---|---|
| Vee reference pack x12 (4 retried after HF "temporarily unavailable") | Qwen edit 2k ($0.075) | 0.90 | PASS (w09 dropped: duplicate stopwatch) |
| Vee Soul ID (cinema, 12 imgs) id e01fe87b-… | /v1/custom-references | 2.50 | QUEUED (same as Otto's since 04:52 — HF-side) |
| Consistency test x3 (street / office / duo café) | Flare 2k, 8 refs | 1.38 | PASS — identity holds in new scenes |
| Reel 02 café, audio-driven | Seedance 2.5 r2v 480p 30 s | 6.17 | PASS (whip pans, no hard cuts; re-voiced with locked voices) |
| **Vee/reel running total** | | **~18.51 of 20** | |

## Round 3 (user: "videos that raise our impression; rotating ring around Otto; varied lines") — site budget ceiling $80
| Item | Model | $ est | Status |
|---|---|---|---|
| AURUM Top Shelf keyframes K0,K1,K2,K4,K7,K8 + K6 glare | Flare 2k | 2.18 | PASS |
| AURUM motion A/B/C/F/G (5 s each) | Kling 3.0 pro i2v, first+last frame | 2.38 | PASS |
| AURUM E fall (Seedance 10 s) x2 | Seedance 2.5 i2v 480p | 0 (blocked by NSFW filter, not charged) | FAIL: a person leaving a rooftop trips the filter |
| AURUM E dive + E float | Kling 3.0 pro i2v | 0.95 | PASS, float (gold umbrella) chosen |
| Talking/entrance clips x6 (keyed) | Kling 3.0 std 5 s | 2.14 | PASS (otto_peek too low; peek rebuilt from rise) |
| Voice bank 52 lines, AURUM lines/music/SFX | ElevenLabs credits | 0 | PASS |
| **Round 3 subtotal** | | **~7.65** | site total ~$53 of $80 |

Lessons:
- Seedance's filter rejects "steps off the edge / falls" with a person on a rooftop, even if the tone is playful. Kling pro accepts a whimsical float (umbrella) or a cabled stunt dive.
- A one-take can "wipe" through a foreground body (G_pack passes Otto's blazer) and still read as one move.

| Item | Model | $ est | Status |
|---|---|---|---|
| OTTO-1 "Tabletop city" keyframes x6 | Flare 2k | 2.06 | PASS |
| OTTO-1 motion (4x5 s + 1x10 s) | Kling 3.0 pro i2v | 2.86 | PASS |
| VESPER-2 "23 minutes" keyframes x6 | Flare 2k | 2.02 | PASS |
| VESPER-2 motion (4x5 s + 1x10 s) | Kling 3.0 pro i2v | 2.86 | PASS |
| **Round 3 total** | | **~17.45** | **site total ~$63 of $80** |
| AURUM glass continuity: K4/K7/K8 edits (+1 retry) | Qwen edit 2k | 0.30 | PASS: same tall plain glass in every shot |
| AURUM re-render C/E/F/G | Kling 3.0 pro i2v | 1.90 | PASS: seams invisible, drink continuous |
| VESPER re-voice (sun is short, scent lasts) | ElevenLabs credits | 0 | PASS |
| **Site total** | | **~$65.6 of $80** | |

Lesson: every keyframe that shows the product in use must name the SAME vessel ("tall straight-sided plain glass, no stem, no ice"); otherwise each keyframe invents its own (flute, can, iced tumbler) and the drink appears to jump at every seam.
| Lip-sync talking lines x8 (+ test, + 2 retakes for framing/lips) | Wan 3.0 r2v 720p, $0.10/s | ~5.40 | PASS: real lip-sync (mouth lags audio 0.12 s, baked into the clip) |
| **Site total** | | **~$71 of $80** | |

Lesson: Wan 3.0 reference-to-video with audio_urls is the cheapest real lip-sync ($0.10/s at 720p). Framing drifts between takes, so say "same camera distance as the reference, hands visible at the bottom edge, do not zoom in".
| AURUM v3: K5d/K7h/K8j glass edits (+retries) | Qwen edit 2k | 0.45 | PASS |
| AURUM v3: D real drink, E leap, F land, G set-down (+1 G retake) | Kling 3.0 pro i2v | 2.38 | PASS |
| AURUM v3 score composed to picture + gulp/clink SFX | ElevenLabs credits | 0 | PASS |
| **Site total** | | **~$74 of $80** | |

Self-audit lesson (the owner caught these, I should have): place every sound on the MEASURED frame of its action (frame strip at 4-10 fps around each event), never on the plan's timings, and re-measure after every re-render. Never put a voice on a character whose lips are not moving: use text supers or VO only when the mouth is off-screen. Check the action really happens (the level must drop when someone "drinks"). Check a seam lands on full white, not mid-flare.
| F07 native-audio test: H0 macro hook still + Seedance 2.5 i2v 10 s 480p with generated sound | Flare + Seedance | 2.41 | PASS: hook + spire reveal + pour + real drink, sound generated with the picture. Fix: soda reads as beer (foam head) |
| **Site total** | | **~$76.5 of $80** | |
| F08 'From the top' Dubai-style: D0 Flare still + Seedance 2.5 r2v 15 s 720p, native audio | Flare + Seedance | 7.28 | PASS: snap synced (hand 1.75 s / audio 1.76 s), dive, chase, Otto-already-in-car twist. Approved extra budget: $15 |
| **Total** | | **~$83.8 ($80 + $15 approved for this film)** | |
| F09 AURUM heist: R0 Flare still + Seedance 2.5 r2v 15 s 720p, native audio | Flare + Seedance | 7.28 | PASS: BASE jump + chute open (audio 2.25 s), landing in car (7.0 s), foam 'shot' at police (11.5 s), bag of cans punchline. Real guns swapped for a foam-spraying can (ad policy + model filters) |
| **Total** | | **~$91 ($80 + $15 approved)** | |
| F10 'Red Light' storyboard x9 | Soul Cinema 720p | 0.04 | PASS as composition guide (S1/S5 came out rotated, S7 police car beside instead of behind: fix in video prompt) |
| F10 Red Light test 30 s 480p, 9-shot multi-cut prompt (doc 43 §7.1 pattern), native audio | Seedance 2.5 r2v | 6.17 | PASS with notes: real launch/handbrake turn/follow/red-light stop/handoff/pull-away; audio onsets on actions (0.28 launch, 7.25 turn, silence 16-23, 23.85 pull-away). Issues: Vee shows 2 stopwatches in interior, cruiser stops beside not behind, officer never visibly cracks/sips |
| **Total** | | **~$97.3** | |
| Foggy Dog fidelity proof, S3 7.5 s viewfinder dog close-up (req 4500f922) | Flare 2k high, refs = brand packshot + brand lifestyle photo (public CDN) | 0.34 | PASS: 7/7 gingerbread men, twill dE 3.1 (borderline), thread 7.7 L too light, men re-arranged |
| Foggy S4 10.0 s fridge-door punchline (req a0ed04c8) | Flare 2k high | 0.34 | PASS with note: card shows dog alone in the bow tie; the "elbow" reads as a cushion; twill dE 6.4 (photo-of-a-print, darker) |
| Foggy S5 12.5 s end card, bow tie + Evergreen walk set (req 3fc283ce) | Flare 2k high, refs = 2 packshots | 0.34 | PASS: 7/7 men, twill dE 2.0; walk-set collar 5/5 canes, buckle, D-ring, webbing dE 3.9 |
| Foggy S1 0.0 s hook take 1 (req 644cca41) | Flare 1k high | 0.16 | FAIL: one seated adult has no head, another's face is replaced by hair; embroidery glittery at 1k |
| Foggy S2 1.2 s OTS photographer (req fdce1ba9) | Flare 1k high | 0.16 | PASS as sketch: no faces, no camera logo; zoom-ring twist not shown; embroidery glittery at 1k, twill dE 4.1 |
| Foggy S1 hook take 2 (req 3968622e), the one allowed redo | Flare 2k high | 0.34 | FAIL at 9:16 (headless people, room visible above the necks); usable as a $0 4:5 crop cut at the shoulders: 7/7 men, twill dE 2.1 |
| **Foggy fidelity-proof subtotal (cap $2.00)** | | **1.68 est** | 6 calls, 1 redo. Costs are hfgen's conservative estimates (Flare is token-billed); actual billed may be lower |
| **Total** | | **~$99.0** | |
