# AI product-commercial workflows (24 YouTube tutorials read in full, 2026-10-07)

Key sources:
- JA, Seedance 2.0 full ad workflow: https://youtu.be/ClIaRcvwnTQ
- DK2, Seedance 2.5 full guide: https://youtu.be/kGku3TTiYO8
- DK1, Nano Banana + Kling: https://youtu.be/P7pH_1zFKbE
- MI, Seedance Hollywood ads: https://youtu.be/_hVqSGOWo3U
- TL1, AI B-roll commercial: https://youtu.be/fXkgoXOJaF8
- TL2, Kling 3.0 product: https://youtu.be/57p18lLpNEg
- TL3, 3 steps product animation: https://youtu.be/bxzZXYpTS64
- CP, Kling 3.0 honest review: https://youtu.be/Yo9XLnpMcaw
- AQ, cinematic perfume: https://youtu.be/WAeINRupB5U
- ON, luxury perfume: https://youtu.be/m48mIRYRtus
- SA, luxury perfume: https://youtu.be/42DrLkMlQYY
- HF, $1M ad: https://youtu.be/AdjllfZuqYM
- JE, premium product: https://youtu.be/esAfAQV7p9I
- JF, fashion: https://youtu.be/J_u-XYM1Mng
- ML, Seedance commercial: https://youtu.be/80Fsrbo2t9w
- AI, Seedance 2.5 + CapCut: https://youtu.be/MJbxZ4kZ8Vg

## Pipeline
1. **Concept first.** Have a human idea and a feeling the ad should create. If an LLM writes the brief alone, the result is generic [DK2, ET].
2. **Use real ads as the storyboard.** Screenshot a real category ad shot by shot, then restyle it to the brand [MI, TL1].
3. **Key visual first.** It informs everything. Generate the final product scene first [JA].
4. **Asset lock.** Build a product reference sheet (4 views plus a logo/texture close-up plus approximate real size) and character sheets. "The step most skip, which is why AI ads fall apart" [MI, DK2, AQ].
5. **Style block.** Build a lookbook (Pinterest/ShotDeck), have an LLM describe the light and colours, and paste that **one block into every prompt**, so the film shows one grade and not "four styles" [DK2].
6. **Make every shot a still first** at 2K–4K, generating 2–4 per prompt. 21:9 framing looks more cinematic [MI, HF].
7. **Animate:** i2v, start and end frames, or multi-shot.
8. **Upscale and interpolate** (Topaz at 4K, interpolate to 30 fps to remove hitching), then **grain**, edit to music, speed ramps, SFX [JA, MI].

## Label consistency
- Generate a separate **close-up of the label** with the correct text. Prompt: "image 2 is the front-label close-up. Use it as the authority for the exact wording, typeface, weight, colour, line breaks and layout", and spell out the exact text. It works best on close shots [DK2].
- **Kling 3.0 Elements:** bind 2–8 product angles on top of the start frame for maximum consistency [CP, JG].
- Add "maintain the exact appearance and design of the bottle throughout" [SA]. Brief label warping can hide inside motion blur [TL3].

## Prompts
- **Still:** "promotional shot, shot on RED, anamorphic", "Sony A7R, rich bokeh, dark moody aesthetic, deep contrast", "fashion editorial, analog photography", "realistic textures, shallow depth of field" [HF, DK1, JF, JE].
- **Video formula:** subject → action → camera → style → constraints. Direct it like a camera operator: "keep the camera almost still with a slight natural handheld motion" [DK1, ML].
- **Luxury restraint** [ON, AQ, NS]:
  - "one simple camera movement and subtle environmental motion"
  - "lighting gradually exposing the product while the bottle stays perfectly still"
  - "spray particles in slow motion, product stationary"
  - "rotating in the exact same place, centre of mass does not move"
- **Ask for "super slow motion"** and re-time in the edit. Normal-speed clips can't be slowed down cleanly [TL1].
- **No music in generations** [JA].
- **Add a negative constraint after each failure** [TL3, DK1].

## Start and end frames, multi-shot
- **Start/end frames:** generate the end frame *from* the start frame plus the product image. The model then has less room to hallucinate [TL3].
  - Loop: wide→close, then close→wide.
  - Reveal: back of the product → front. All 3 takes were usable [JE].
  - Chain clips by using the last frame of one as the first frame of the next [DK1].
  - When an action keeps failing, lock it with start and end frames rather than re-prompting [TL1].
- **Kling multi-shot** works best as a single prompt: "Shot 1 (3 seconds): …; Shot 2 (3 seconds): The camera cuts to…". Always write "the camera cuts" [CP].
- **Seedance 2.x/2.5** is strongest at connected multi-cut sequences (5 cuts in 15 s), with up to 50 references. 2.5 supports timestamp-targeted edits [JA, MI, AI].
- **Model choice:**
  - Seedance: dynamic, connected sequences.
  - Kling: single hero shots, labels, start/end frames, 4K [JA, TL2].

## Making it feel like a real shoot
- **Treat generations as takes.** Make 3–4 per shot (draft at 720p) and keep the best 1–3 s slices [JA, TL1, CP].
- **Grain kills the plastic look.** Re-grain anything you blur so it beds in [MI, JA].
- **Small human reactions sell it:** a blink, a breath, a flinch [MI, DK1].
- **Cut like a DP.**
  - Music first, cut on the beat.
  - Speed ramps, subtle zooms.
  - **Directional match cuts:** a shot ends moving the same way the next one starts.
  - Hold a shot through a riser.
  - Reverse a failed take if the reverse works.
  - Crop in to hide errors [TL1, J7, JA].
- **End card:** background blurred, product masked sharp, minimal type that never covers the product [JA, ON].

## Structure
- Hook within 5 s [DK2].
- **Perfume beat sheet** [AQ]: macro droplet → bottle emerging from darkness → spray-particle burst → spotlight hero → logo card.
- **Narrative version** [SA]: she enters unnoticed → finds the bottle → sprays → transformation → everyone notices → bottle hero.
- Premium VO: 1–2 short sentences [JE].

## Mistakes to avoid
- No product sheet; vague prompts.
- Forcing retries.
- Using whole clips just because you paid for them.
- Music baked into generations.
- Unchecked artefacts (a hand through glass, colour shifts).
- Mixed grades across shots.
- Letting the LLM invent the concept.

## Adopt now (ranked)
1. Grain + upscale + interpolation on every clip.
2. One shared style block in every prompt.
3. Restraint: one move, the product perfectly still, slight handheld.
4. Takes mindset: 3–4 per shot, keep the best 1–3 s, match cuts on the beat.
5. Product sheet + label close-up "as authority".
6. Start/end keyframes for every product move.
7. "Super slow motion" generation, re-timed in the edit.
8. Real camera/lens tokens + 21:9 stills.
9. Our own sound bed; no music in generations.
10. Small human imperfections.
