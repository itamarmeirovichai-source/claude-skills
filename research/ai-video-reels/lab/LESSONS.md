# LESSONS: the owner's feedback, kept forever

Read this file **before every film, every outreach and every research run**. Each line is a mistake that cost money or trust, and the rule that prevents it. Add new lines the same day the owner gives feedback. Never delete a line; mark it superseded if a later rule replaces it.

Format: `date · what the owner said (translated) · root cause · RULE`

## Picture and physics
- 2026-10-08 · "the camera passes through buildings" · I let the model fly the camera through glass · RULE: every camera position must be one a real crew could rig (drone, chase car, tripod, handheld, hard mount). Write "the camera never passes through glass, walls or vehicles" in every prompt.
- 2026-10-09 · "the parachute can't open like that, there are no turns with the car, it's not a real chase" · I put 5 big action beats into one unbroken 15 s take · RULE: action and chase films use 6–10 hard-cut shots, written as ONE multi-shot prompt ("EXACTLY N SHOTS AND N−1 HARD CUTS"). Write real physics per shot: nose dive, body roll, tyre smoke, a 2–4 s freefall before the canopy opens. Docs 41, 43 §7, 44.
- 2026-10-09 · "it's not realistic" · No physics check before spending · RULE: do a physics read per shot in the preflight, and never land a person in a moving car.
- 2026-10-08 · "the glass changes, he doesn't really drink" · Each keyframe invented its own vessel, and the drink level never dropped · RULE: name ONE vessel in every prompt. "Drinks" means the level visibly drops. Check every object's fate across every cut.

## Sound
- 2026-10-08 · "sounds aren't in sync, they come at the wrong time" · I placed SFX by the plan's timings, not the picture · RULE: place every sound on the MEASURED frame of its action (frame strip at 4–10 fps plus an audio onset check).
- 2026-10-09 · "maybe create the sound through Higgsfield" · Post-dubbed SFX never matched · RULE: generate the sound together with the picture (Seedance `generate_audio:true`). Add only the voiceover and the final music in post.
- 2026-10-08 · "the lips don't move with the words" · A generic talking loop played under different lines · RULE: if a character is on screen and speaks, render THAT line with lip-sync (Wan 3.0 r2v plus the audio file) and bake the audio into the same clip. If the lips can't be synced, the line becomes a voiceover with the mouth off-screen, or on-screen text.

## Story and selling
- 2026-10-08 · "the films are pretty but have no punchline" · I made mood films · RULE: every film needs a hook in second 1, a turn, and a punchline CAUSED by the product. If the joke works without the product, the concept fails.
- 2026-10-09 · "there are no hooks" · Slow openings · RULE: motion already happening in frame 0, or a sound-first hook. No slow aerial reveal as the opening.
- 2026-10-09 · Positive: "wow, I loved the ad, it's really cool" (Red Light) · Real chase grammar, a twist at a red light, the product hand-off · RULE: this is the bar. A grounded action plus a deadpan reversal plus the product at the centre.
- 2026-10-09 · "add an English voiceover with a cool slogan at the end" · RULE: end every spec film with a 2-line voiceover tagline in a locked voice, over a frame where no lips are visible, plus the logo card.

## Process and money
- 2026-10-09 · "we're wasting a lot of money because you don't research what really works" · I generated before researching · RULE: research first (zero spend), then a storyboard (~$0.05), then a 480p test, then the final. Get the owner's approval at each paid step.
- 2026-10-09 · "I shouldn't have to tell you these things, you must know everything" · I relied on the owner to find faults · RULE: run the full QC before sending anything (docs 46, 42): frame strip, cuts, the sound/action table, lips, continuity, and the forbidden list. Report every fault I find myself, before the owner does.
- 2026-10-09 · 480p test vs final · No seeds on Seedance/Kling · RULE: if a 480p take is the one, keep it and upscale it. A re-render is a different take.

## Characters
- Otto's mouth is never visible and his eyes are never wide. Vee has exactly ONE stopwatch. Check it in every frame; it drifted to 2 in F10.
- Locked voices: Otto `IbpG1IF3UdxPgaDKhwsd`, Vee `cLFf1Dc8DlgFwZ62rdPg`.

## Policy
- No real guns. Props replace weapons (the foam can). Police imagery is fine organically, but paid ads need a police-free cut (Meta/TikTok, doc 45). Use invented brands for spec work. Disclose AI.
- No face-swaps onto famous videos (owner asked on 2026-10-09; declined because of rights and impersonation).

## From the QC tools (doc 46, 2026-10-09) [self]
- Every final we delivered peaked above −1 dBTP after AAC encoding. RULE: master with `loudnorm=I=-14:TP=-2` (two-pass when possible), then MEASURE true peak on the encoded file. It must be ≤ −1.0 dBTP.
- Raw Seedance native audio sits at −22 to −25 LUFS. Always add gain plus a limiter.
- The fixed +125 ms lip offset was wrong. RULE: measure each talking clip separately with `lipsync_check.py` and bake its own offset. Otto's moustache can't be verified (SyncNet confidence < 1), so treat his lines as voiceover.
- Frozen frames hide in one-takes when a clip that ends on a held pose is slowed down. RULE: run `qc_report.py` and fix any freeze longer than 6 frames.
- Hard hits more than 2 frames off in native audio need re-placing; keep the ambience.

## Funnel (owner, 2026-10-09)
- "Part of finding leads is researching them: understanding how to make them buy, and buy again." RULE: no message without a dossier (why hot, the business, the person, fit/red flags, the buying path, the re-buy path). Filter to only the very hottest. After approval/payment, research the business and the person again in depth before any concept (`vxo-film` Step 0).
