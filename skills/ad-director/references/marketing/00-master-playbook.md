# Master playbook: from product to an ad that SELLS (read before every brief)

This synthesises 01-fundamentals, 02-niches, 03-platforms and 04-ai-craft, plus the lessons from the lab NOTEBOOK (F01 AURUM).

## The client's taste (proven by feedback)
- **Aesthetic, clean, premium. The brand is recognisable in every shot.** No comedy sketches unless asked.
- **No talking heads or lip-sync.** If a voice is used, it is a VO (off-screen), short and elegant.
- **Everything moves.** Product stills are at Celsius level (colour world, props, cold or sensory proof, mirror surface, hard light).
- Avoid monotony: vary shot sizes, include a consumer scene (hands or body, no face), keep **one** colour world per film, pay off a mechanism, end on a CTA.

## The BIG IDEA rule (learned on F02)
Before any shot list, design **one big-idea shot**: the single-minded claim made *literally visible* in one impossible-but-elegant image (VESPER: "Wear the golden hour" → the sun sets into the bottle). It is the hook in 0–3 s and is paid off once more later. A film without it reads like a beautiful catalogue: "good, not enough".


## Library map (read the relevant file before every brief)
| File | Use it for |
|---|---|
| 01-fundamentals | why people buy, 15 gates |
| 02-niches / 11-niche-* | niche visual grammar, formats, BIG IDEAs, **ready recipes with our tools** (beauty, food-drink, fashion-luxury, tech-home) |
| 03-platforms | Reels/TikTok/Shorts numbers |
| 04/07-ai-craft, workflows | how working AI ad studios produce |
| 05-real-dp | real-shoot prompt vocabulary |
| 06-anti-ai-realism | top 15 fixes for "looks AI" |
| 08-post-production | edit, grade, sound recipes |
| 09/10/12-higgsfield | official guides, visual study of 29 clips, **85 verified API endpoints + prices + templates** |
| 14-rourke-heath-study | a top AI-ad educator's real workflows: Seedance timecoded single-shot 'build' prompts with in-generation speed ramps, @-scoped refs, Kling start/end chaining + product-lock line, voice pipeline, hook factory, spec-to-prospect sales loop |
| 13-elevenlabs-mastery | eleven_v4, voices per niche, music_v2_5 composition plans, SFX library, mix levels |
| 15-concept-engine-and-pretesting | idea generation at volume, 6 twist templates, zero-cost synthetic-panel + Swiss-tournament pre-testing, 3-storyline client page |
| 16-seamless-flow | continuous "one-run" films: keyframe-anchored Kling chain, no-settle motion prompts, push-through seams, 8 tested ffmpeg seam recipes |
| 17-hero-stills-mastery | product-fidelity still pipeline, niche prompt blocks, off-centre methods, automatable QC gates + pairwise selection |
| 18-automation-pipeline | the machine's architecture: stages S0–S11, human checkpoints, JSON artefacts, budget guards, QC gates |
| 19-great-ads-storytelling | 49 annotated award/Effie films, 14 twist patterns with AI recipes, storyline card + 100-pt rubric |
| 20-youtube-gapfill | Rourke's sales playbook + workflows, strategist talks, label-fidelity protocol, automation walkthroughs |

## Hard rules learned the expensive way
- Kling product-lock sentence on every product move: "nothing in the frame moves except the camera" (or name the one thing that moves).
- Design "frame 0" (the scroll-stopping first frame) before the shot list; ≥5 shot types per 20 s.
- Turn `sound`/`generate_audio` OFF explicitly on Kling/Seedance (defaults ON = +50% cost).
- Soul Cinema ignores product references → use it for plates/locations/people only; put the exact product in with Flare (`image_urls:[plate, product]`, explicit 9:16), then animate with Kling.
- Flare/Nano-Banana skew symmetrical-centred: always write off-centre blocking + the anti-gloss suffix.
- No AI footage as the product's functional proof; show proof as metaphor/spec line/"dramatization".
- Generate logos/dials/labels blank or simple; set exact type and glints in post.
- Music: composition plan with music_v2_5; hard hits only on chunk boundaries (≥3 s chunks), doubled with an SFX hit.

## The 10-step pipeline
1. **Niche and product.**
   - Pick a niche where AI excels (02-niches "Top 5": fragrance, leather/luxury goods, coffee, candles, watches/jewelry/sneakers).
   - Invent a fictional brand.
2. **Brand bible (asset kit).** Name, signature colour + secondary, typeface (serif for luxury), sonic logo (1–2 s plus a recurring motif), signature device or gesture, end-card layout.
3. **Strategy card:**
   - awareness level
   - job-to-be-done or category entry point (situation)
   - single-minded claim (≤7 words)
   - filmable mechanism
   - top objection plus its visual answer
   - CTA fitting the tier (e.g. "Discover the sample set")
4. **Beat map (15–25 s), with a visual change every 1.5–3 s:**
   - 0–2 s: hook — the sensory moment, brand visible, sonic cue.
   - Body: mechanism and proof shots, then the consumer scene, then the emotional peak.
   - Last 2–3 s: hero packshot, logo, tagline, CTA.
   - Product shown ≥3 times.
5. **Run the 15 gates** (01-fundamentals §7). Any fail → rewrite before spending.
6. **Hero stills.** Product reference first, then one still per shot with the prompt lock and the add-no list. Approve all stills (rubric ≥ 8/10).
7. **Motion.** Kling 3.0 Pro i2v, 5 s, sound off: one camera move per shot, "only X moves", logo legible. Avoid pours, hands touching mechanisms, and faces.
8. **Sound.**
   - ElevenLabs score with timestamped structure (ASMR intro, a hit on the reveal, a breath before the logo).
   - Foley per action, plus the sonic logo.
   - A short VO line at the end (+71% recognition vs ASMR-only; speech + music gives 2.1× purchase intent).
9. **Edit.**
   - Cut on the beat; speed ramps.
   - One grade; type set in post (serif, wide tracking).
   - Captions for the VO.
   - Safe zones (top 14%, bottom 35%, sides 6%).
   - End card 2–3 s with the CTA.
   - Cut a 6 s and a 15 s version from the master.
10. **QC + retro.** Run `director.py qc`, a cold-viewer test ("what is it, why want it, what do I do?"), then a NOTEBOOK retro.

## Budget template (≈ $10 per flagship)
| Item | Cost |
|---|---|
| Product reference stills (2) | $0.60 |
| Shot stills (8 × Flare 2k) | $2.40 |
| Motion (8 × Kling Pro 5 s, sound off, $0.476) | $3.81 |
| Retakes reserve | ~$2.50 |
| Music, SFX, VO | ElevenLabs credits |
