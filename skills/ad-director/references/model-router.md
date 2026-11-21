# Model router (condensed)

Full evidence, per-model grammar cards, failure→fix table, workflow, prices and sources are in
`research/ai-video-reels/round5/R1-model-router-and-prompt-grammar.md` (as of 2026-10-06; tags [OFFICIAL]/[3P]/[UNVERIFIED]).
Read the model's grammar card there (§3–4) before writing its prompt. When `director.py bench`
results exist, **our own bench data overrides this table**.

House rules on top of the router:
- Product shots: approved still first (GPT Image 2.5 for look → Nano Banana for exact product), then I2V with start (+end) frame.
- Label must be readable → plan a composited label plate in post, whatever the model.
- Liquids: no model is reliable → ≤3 s macro pours, cut-heavy, or real/CG liquid plate.
- Test at 5 s/cheap tier (Veo 3.1 Lite, H3 Max Camera) before paying for the hero tier.
- 3–4 takes per shot budget; past 3× budget change the method, not the seed.

## 1. TL;DR ROUTER (shot type → best → backup → why)

| # | Shot type (ad) | Best | Backup | Why |
|---|---|---|---|---|
| 1 | **Packshot hero / label must stay exact** (rotation, push-in) | **Kling 3.0 Pro I2V** (start+end frame) | MiniMax H3 (Start+End frame) | Kling is the one creators recommend most for keeping label, cap and shape identity during rotation [S40]. Start+End frames pin both ends of the clip [S7]. H3 is #1–2 on the AA image-to-video board and supports start/end frames [S2][S16]. **Always plan to composite the label plate in post** [S42]. |
| 2 | **Multi-shot social reel, 15–30 s, many SKUs/variants** | **Seedance 2.5** | Seedance 2.0 / Wan 3.0 | Up to 30 s and about 50 refs (30 img/10 vid/10 aud). Audio comes in the same pass. Region edit lets you swap the product without a re-render [S9][S10][S11]. Wan 3.0 also goes to 30 s, is #1 on AA T2V and costs about $0.17/s at 1080p [S1][S18]. |
| 3 | **Talking UGC / spokesperson with lip-sync** | **Seedance 2.5** | Veo 3.1 (4K, 8 s) / Kling 3.0 (voice binding) | In Krea's test, Seedance 2.5 won "speaking shots" [S45]. Veo has the best audio polish and documented indemnity [S44]. Kling offers voice cloning (5–30 s sample) [S44]. |
| 4 | **Premium hero, 4K master, 8 s** | **Veo 3.1 (4K)** | Kling 3.0 4K mode | Veo 3.1 is the only "true 4K" generator, but 4K forces 8 s clips [S44][S13]. Kling 3.0 has a native 4K mode [S21]. |
| 5 | **Reference-locked product in a lifestyle scene** (product photo + set + model) | **Gemini Omni Flash** | MiniMax H3 / Seedance 2.5 | Omni takes up to 7 reference images and lets you fix things by conversational edit. It is #3 on AA I2V at $0.10/s on the API [S2][S12][S29]. H3 gives explicit reference roles [S16]. |
| 6 | **Liquids / pours / splashes** | **None reliable.** Try Kling 3.0 Pro, then Veo 3.1 | Hybrid: real liquid plate or CG + AI background | In HumanSignal's Sep 2026 test, Seedance 2.5, Veo 3.1 and Kling 3.0 Pro all failed the water pour. Kling looked most realistic but created water from nothing [S46]. Keep pours short (≤3 s), close up and cut-heavy **[inference]**. |
| 7 | **Hands holding / using product** | **Kling 3.0 Pro I2V** (start frame shows grip) | Seedance 2.x with a hand reference | Grip on broad non-critical surfaces; one action per clip [S42]. Hand continuity is a general weak spot [S29]. |
| 8 | **Food / cosmetics texture macro** (cream swirl, glaze, steam) | **Runway Gen-4.5** I2V | Veo 3.1 / Luma Ray3.2 (HDR) | Gen-4.5 is recommended for "material-accurate" product scenes (ceramics, metal reflections) [S40]. Ray3.2 outputs 16-bit HDR/EXR for grading [S27]. **[3P]** |
| 9 | **Swap product / colorway / background in an approved clip** | **Runway Aleph 2.0** | Seedance 2.5 region edit / MiniMax H3 (AA editing #1) | Aleph 2.0 does localized edits with single-frame guidance [S24]. Seedance 2.5 region edit [S10]. H3 is #1 on the AA video-editing board per [S43]. |
| 10 | **Precise camera choreography / many keyframes** | **Luma Ray3.2** | Kling 3.0 multi-shot | Up to 16 keyframes per clip, 20 s, 1080p [S27]. |
| 11 | **Cheap concept / animatic iterations** | **Veo 3.1 Lite** ($0.05/s 720p) | MiniMax H3 Max Camera ($0.05/s 480p), Kling 3.0 Std | Lowest per-second prices in this research [S12][S17][S36]. |
| 12 | **Self-hosted / LoRA-trained product** | **Wan 2.2** (open, Apache-2.0) | MiniMax H3 (open weights *announced*) | Wan 2.2 is the only open flagship [S18]. MiniMax said it would release H3 weights "within days" **[UNVERIFIED that it shipped]** [S15]. |
| 13 | **Animate a Midjourney still (art-directed mood)** | Midjourney Video V1 | Kling / Seedance I2V | Cheap and keeps the MJ aesthetic, but ≈480p and no audio, so mood-only b-roll [S30][S31]. |

**Start-frame (image) router**

| Need | Best | Backup | Why |
|---|---|---|---|
| Overall look / composition / lighting | **GPT Image 2.5 (Sunburst)** | GPT Image 2 | #1 on AA T2I and editing; up to 3840 px [S3][S4][S35] |
| Exact product insertion / product consistency | **Nano Banana Pro / Nano Banana 2** | Seedream 5.0 (14 refs) | Creator benchmark: "GPT-Image-2 best aesthetic, Nano Banana best product consistency" [S41]. NB Pro handles 6 objects and 4K [S38]. Seedream 5 takes 14 refs [S34]. |
| Typography-heavy end card / packaging copy | **GPT Image 2/2.5** | Ideogram 4.0 (open-weights, bbox layout) | About 99% text accuracy claimed by OpenAI-sourced reports [S33]. Ideogram 4 has bounding-box layout, hex palette and ~90% text accuracy, but a non-commercial weights license [S39]. |
| Brand-color-exact / JSON-controlled layouts | **FLUX.2 [max]** | Ideogram 4 | Accepts JSON prompts and HEX colors; up to 10 refs [S48] |
| Budget bulk variants | **Seedream 5.0 Lite** (~$0.026–0.035/img) | Nano Banana 2 Lite ($0.034) | [S47][S12] |

---

## 2. Universal prompt grammar (works across models)

Every vendor guide, official or third-party, comes down to the same skeleton. Order matters because instruction adherence drops with position in the prompt [S8][S38].

```
[REFS/ROLES]  Image1 = exact product (geometry+label). Image2 = set/lighting. Video1 = camera move only.
[SHOT]        framing + lens  (e.g., "macro close-up, 100mm, shallow DOF")
[SUBJECT]     product + 1–2 concrete attributes (material, color, finish)
[ACTION]      ONE verb chain with physical consequence ("condensation beads roll down the can")
[SCENE]       location + light in one sentence
[CAMERA]      ONE primary move + end state ("slow push-in, ending on label close-up")
[PRESERVE]    "Product is rigid; keeps silhouette, cap, label position; text does not change."
[AUDIO]       Dialogue in quotes / SFX: / Ambient: / music or "no music"
[TEXT]        none in-model (add in post), OR exact string + timing + position + entry style
```

Rules supported by multiple sources:
- **Length.** About 60–100 words for Seedance-class models [S8]. MiniMax H3's advanced structured prompts can run 350–500 words in the detailed-description section [S16]. Veo uses a 5-part sentence formula [S6].
- **One camera move per shot.** This is official for Seedance [S5] and for MiniMax H3 [S16]. Use "cut to" or Shot N for a second move [S8].
- **Every reference gets a job.** A reference with no assigned role leaks its lighting and framing into the shot [S8][S16].
- **Negatives.** Veo's official guidance is to phrase exclusions positively ("a desolate landscape with no buildings") [S6]. Kling on fal has negative_prompt and CFG controls [S43b]. Veo has a negative_prompt parameter and seeds on the API [S43].
- **Silence must be requested explicitly.** If you leave audio unspecified, you get random music [S8].
- **Verbs beat adjectives.** "8K, stunning, epic" does nothing [S8].

---

