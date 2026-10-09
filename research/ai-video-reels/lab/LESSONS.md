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

## From niche research 47–52 (2026-10-09) [self]
- AI never plays the "result" or the proof (a face after skincare, a dog loving food, a test survived). Every client film keeps a short PROOF SLOT for the client's real footage or certificate. The FTC bans AI or invented testimonials.
- The picture is the claim (Dyson v. Dreame, NAD 2026): a "dramatization" label doesn't cure an AI scene that overstates the product. Keep every visual within the product's real specs (IP rating, battery, dB, SPF wording).
- Generated people are the biggest backlash risk in fashion and beauty. Build the world and the stunt with AI; show hands or backs, or licensed real people. Never generate babies. One animal per shot, 5 s or less, from a real photo (Kling).
- Physics traps: vacuum-insulated tumblers never sweat; dial text, stone counts and logos come from a real-photo still (Kling i2v); dimensions within ±3% and colour checked against a swatch.
- Ship 6–10 stills with every film (furniture ads are 70% images; plain product shots score highest in home). The winning ad length in beauty, food and fashion is often 8–15 s, so always deliver a short cut.
- Ad lifespans set the plan: outdoor and fashion ads die in ~20 days → sell the monthly Season plan; pets and furniture last 40–74 days → sell a Premiere one-off.
- Proven formats: the product surviving an ordeal (Stanley); a giant product with a real hand for scale (Jacquemus); product-as-food (The Ordinary); the fridge-door POV with the product's own fate as the joke.

## From niche research 53–54 (2026-10-09) [self]
- The real competitor is the brand's own $400 in-house AI team (DSC). Sell what they get wrong: physics-checked, QC-measured, claims-checked. Say it on the site and in DMs.
- Sell MODULES, not only films: a 3–5 s AI hook head (plus a 2–4 s mechanism insert) grafted onto the client's existing winning UGC body. Test hooked vs original, same body. Paid winners in tools/oral care run 43–78 s, so a 15 s film is often the wrong unit.
- A splice must not be audible: ride the hook down to the UGC's loudness at the seam (step ≤ 3 dB), then master the whole to −14 LUFS / ≤ −1 dBTP.
- A clock, timer, dB or "minutes" on screen is a claim. Only the client's tested number, with its source in the job file.
- Hair, skin and teeth results are the hardest AI renders and the biggest legal trap: tell those stories through objects (the tool, the cord, the cross-section) and keep the proof slot for real footage.
- "Inside the machine" cutaways (airflow x-ray, a hair cut under the skin) are cheap, AI-safe and have no realism expectation. Build a 6-insert mechanism library per niche.
- A winning gag becomes a franchise: lock the skeleton, re-shoot per drop. This is the strongest Season-plan argument.
- Volume is the founder-led bottleneck (3–7 creatives/week vs 37–688 for leaders). Check it per lead on Motion's public library page and pitch "+12–20 creatives a month".
- New buyer: TikTok Shop affiliate managers. A 15 s "how it should look" seed film plus a shot list that hundreds of affiliates copy.
- 2026-10-09 · "we're not changing direction, what are you talking about" (owner, after the 53–54 summary) · I presented research ideas (hook modules, affiliate films, a "new product") as if they were a pivot · RULE: the direction is fixed: original AI product films (Short/Premiere/Season) through the agreed funnel. Research findings are ways to make THOSE films sell better, or optional add-ons only if the owner asks. Never phrase a finding as "a new product" or "a new buyer" to sell to.
