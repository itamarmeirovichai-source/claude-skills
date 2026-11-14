# R1 — Model Router + Prompt Grammar for Product/Commercial Ads (as of 2026-10-06)

Scope: which AI video and image model to use for each kind of ad shot, how each model wants to be prompted, how they fail and how to fix it, the workflow, and prices. Every claim has a source tag `[Sx]` that maps to the list at the end.
Confidence tags: **[OFFICIAL]** = from the vendor's own docs. **[3P]** = from a third-party guide or test. **[UNVERIFIED]** = single or low-quality source, or my own inference. Check these before you spend budget on them.

---

## 0. What changed since early 2026 (read first)

- **New leaders.** The top of the Artificial Analysis (AA) blind-vote arenas is now held by **Wan 3.0** (Aug 2026, API-only), **MiniMax H3 / H3 Max** (Jul–Aug 2026), **Seedance 2.5** (Jul 2026), **FLUX 3 Video** (Jul–Aug 2026) and **Gemini Omni Flash** (May 2026). Kling 3.0 and Veo 3.1 have dropped to the middle of the table [S1][S2].
- **Kling 4.0 is not generally available.** Only "Flash" is live, and only for Ultra-yearly subscribers. Kuaishou expects the full model and API in October 2026 [S20]. Nobody has verified a "Kling 3.5" release [S19].
- **Runway's current models** are Gen-4.5 (generation) and Aleph 2.0 (in-context video editing, Jun 2026) [S23][S24]. Gen-5 does not exist.
- **Luma's current model** is Ray3.2 (Jun 2026). Ray4 does not exist [S27].
- **Midjourney video is still V1** (released 19 Jun 2025): image-to-video only, no audio, extendable to about 21 s [S30][S31]. No V2 has been released.
- **Wan's only open-weights flagship is still Wan 2.2.** Wan 2.5, 2.6, 2.7 and 3.0 are API-only [S18].
- **Image leaderboard (AA, Oct 2026).** GPT Image 2.5 (Sunburst/Flare, 8 Sep 2026) is #1 for both text-to-image and editing. Next are GPT Image 2, Grok Imagine Image 2.0, MAI-Image-2.6 and Nano Banana 2. Nano Banana Pro is #11 [S3][S4][S35].
- **Nano Banana 2.1** appears in Google Flow builds and in the Gemini pricing page excerpt, but it was not documented as a public model as of 29 Sep 2026 [S37][S12]. **[UNVERIFIED]**: confirm before use.

---

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

## 3. Per-model prompt grammar cards (video)

### 3.1 Seedance 2.0 / 2.5 (ByteDance) — multimodal "director"
- **Official order** [S5][OFFICIAL]: `subject + action details + scene/environment + lighting & color tone + camera movement + visual style + image quality + constraints`.
- **Reference syntax** [S5]: `Reference <Subject_1> in <Image_1> as <Subject_1>`; `Reference <camera_movement> in <Video_1>`; `Reference the timbre in <Audio_1>`. Creator shorthand that also works: `@image1 = …` [S8].
- **Multi-shot**: `Shot 1 / Shot 2 / Shot 3`, in chronological order [S5]. Timecodes ("0–3 seconds") are "unstable" according to ByteDance [S5]. Third-party guides still report that per-second blocks help on clips of 8 s or more [S8] **[3P]**.
- **Audio markup** [S5][OFFICIAL]: music `（fast-paced rock music in background）`, SFX `< dog barking in distance >`, dialogue `{Hello, world}`, subtitle `【Title】`. Don't mix Chinese and English in dialogue.
- **On-screen text** [S5]: `[text] + [timing] + [position] + [entrance style]`. Suppress text with "avoid generating any text or subtitles".
- **Editing/extension** [S5]: `Replace [X] in <Video_1> with [Y]`, `Extend <Video_1> forward…`, `Remove [element] from <Video_1>, keeping the rest unchanged`.
- **Limits.**
  - 2.0: 9 img + 3 vid + 3 audio, 15 s max, 720p native, no real faces [S5b].
  - 2.5: up to 30 s and about 50 refs (30/10/10), 480p/720p native with some platforms at 1080p, plus region edit [S9][S10][S11][S45].
  - Reference strength sweet spot is 70–80% [S8] **[3P]**.
- **Ad strengths.** Multi-shot coherence, references fused across modalities, talking shots, aspect ratios from 9:16 to 21:9 [S45][S43b].
- **Weaknesses.** Resolution is 720p native, so you need an upscale. Liquids fail [S46]. Fine label text garbles with mixed languages or rare glyphs [S8].
- **Example ad prompt (I2V + refs, 10 s, 9:16):**
```
Reference the bottle in <Image_1> as the product: rigid amber glass, black cap, cream label stays unchanged.
Reference the kitchen light in <Image_2>.
Shot 1: macro close-up, the bottle stands on wet slate, a single water droplet slides down the glass; fixed shot.
Shot 2: medium shot, a hand lifts the bottle by its lower body and tilts it toward camera; slow push-in ending on the label.
Warm morning side light, soft shadows, realistic commercial photography.
< glass clink, soft room tone > （no music）. Avoid generating any text or subtitles.
```

### 3.2 Kling 3.0 / 3.0 Omni / 3.0 Turbo (Kuaishou)
- **Structure.** Natural language: scene, action, camera, style. Kling's 3.0 user guide gives no rigid formula [S7][OFFICIAL].
- **Multi-shot.** "Custom Multi-Shot" prose (`Shot 1, profile shot…, Shot 2, frontal macro…`) [S7], or the API `multi_prompt` JSON array `[{"time":0,"prompt":…},{"time":5,"prompt":…}]` [S21]. Up to 6 cuts [S19].
- **Dialogue** [S7][OFFICIAL]: `**Mom** (softly, surprised): Wow, I didn't expect this.` Supported languages are EN, ZH, JA, KO and ES, plus dialect tags ("in Cantonese").
- **Elements** (bind subject for consistency) are built in an Element Library and attached to the shot [S7]. Kling also supports Start & End Frames, and Start Frame + Element [S7].
- **Controls.** On fal you get CFG scale and negative prompt [S43b]. 3–15 s; 720p/1080p; a 4K mode on some APIs [S7][S21].
- **Ad strengths.** Identity preservation of labels, caps and shapes during rotation [S40]. Motion-control transfer from a reference video [S43b]. Voice binding [S44].
- **Weaknesses.** Audio is weaker than Veo's [S44]. Liquids look real but don't conserve volume [S46]. Overlapping voices with 3 or more speakers [S44].
- **Example (start frame = approved packshot, end frame = 3-tube lineup), modelled on the fooh SKIMS case [S39b]:**
```
Fast cinematic push-in on the matte nude toothpaste tube standing on a cream plinth; the tube makes one slow 360° turn
while two more tubes rotate into view from behind it, ending on the three-tube lineup of the end frame.
Soft diffused studio light, gloss highlight on the base, seamless beige backdrop.
The tubes are rigid; logo, typography and crimp stay identical throughout.
Negative prompt: warped text, extra objects, bending, melting, flicker.
```

### 3.3 Google Veo 3.1 (Standard / Fast / Lite)
- **Official formula** [S6][OFFICIAL]: `[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]`.
- **Audio** [S6]: dialogue as `A woman says, "We have to leave now."`, sound effects as `SFX: …`, background as `Ambient noise: …`.
- **Timestamp prompting** [S6][OFFICIAL]: `[00:00-00:02] … [00:02-00:04] …` inside one 8 s clip.
- **Other features.** Ingredients-to-video takes up to 3 reference images and forces 8 s output [S13]. First+last frame interpolation [S6]. Clips are 4/6/8 s at 720p/1080p/4K. 4K is 8 s only [S6][S13]. Audio defaults to off on some API surfaces [S43].
- **Ad strengths.** Best audio polish, 4K masters, enterprise indemnity on Vertex [S44]. Its physics read as more natural than Seedance 2.5 in Krea's test [S45].
- **Weaknesses.** Short clips. Only 16:9 or 9:16 [S45]. Mid-table on AA (#18 T2V) [S1].
- **Example (8 s, 9:16, timestamped):**
```
[00:00-00:03] Extreme close-up, macro lens: a frosted aluminum soda can on crushed ice, condensation beads rolling down
the printed logo. SFX: ice crackle.
[00:03-00:06] Slow dolly-in as a hand pulls the tab; a crisp fizz of carbonation. SFX: tab crack, fizz.
[00:06-00:08] Medium shot, the can lifts out of frame, revealing the logo sharp and centered. Ambient noise: quiet bar.
Bright high-key commercial lighting, cool blue palette, shallow depth of field. No music.
```

### 3.4 Gemini Omni Flash (Google, May 2026; v1.1 Aug 2026)
- **Five dimensions** in the DeepMind guide [S28]: shot framing & motion, style, lighting, scene ("you don't need to describe every detail"), action & interaction.
- **Inputs and specs.** Up to 7 reference images, 4–10 s, 720p to 4K, prompts up to 20k characters [S28] **[3P summary of official guide]**.
- **Conversational edit.** Change one variable per turn and state what stays the same [S28]. A third-party structure that works well for ads: *source role → preserve list → change list → motion/camera → audio → delivery intent* [S29].
- **Ad strengths.** Keeps brand details (logo, shape, finish) from reference photos, edits without regenerating, renders animated on-screen text [S28][S29]. #3 on AA I2V; $0.10/s on the Gemini API at 720p [S2][S12].
- **Weaknesses.** Text-only prompting under-uses the model [S29].
- **Example:**
```
Image 1 is the exact serum bottle (preserve: glass shape, gold dropper, label text and position).
Image 2 is the bathroom set and light. Change: place the bottle on the marble ledge in Image 2.
Close-up, slow orbit of 15 degrees to the right; morning window light, soft caustics on marble;
a single drop falls from the dropper back into the bottle. Audio: quiet room tone, one soft drip. Intended use: 9:16 Reels ad.
```

### 3.5 MiniMax H3 / H3 Max (Hailuo, Jul–Aug 2026)
- **Simple formula** [S16]: visual direction & style → reference roles → opening scene → action (in order) → camera → dialogue & sound → ending state.
- **Advanced structured format** [S16]: `subject_definitions / summary / retention_analysis (fully_preserved | partially_preserved | attribute_transfer | weak_reference) / detailed_description / overall_soundscape / non_diegetic_music: N/A`.
- **References.** `Image 1 defines…`, or the tags `<Picture 1>`, `<Video 1>`, `<Audio 1>`. Up to about 5 ref images and one main reference video [S16].
- **Frame alignment** [S16]: `Picture 1 aligns with 0.00-second mark; Picture 2 aligns with 8.00-second mark.`
- **Dialogue.** `<d>[English] exact words.</d>`; `The voice heard in Video 1 guides Speaker 1` [S16].
- **Specs.** 5–15 s; 768p or 2K at 24 fps; stereo native audio; 21:9 supported [S15].
- **Ad strengths.** #1 on AA I2V (H3 Max); #1 on AA editing per [S43]. Cheap: fal camera-control pricing is $0.05/$0.08/$0.16 per second at 480/768/1080p [S17].
- **Example:**
```
Cinematic live-action product video, warm sunrise light, restrained contrast.
Image 1 defines the sneaker (fully_preserved: shape, colorway, logo). Image 2 defines the rooftop.
Picture 1 aligns with 0.00-second mark. The sneaker rests on a concrete ledge; a gust lifts the laces slightly.
Camera arcs left at slow speed, ending on a side profile. Scene sound: wind, distant traffic. non_diegetic_music: N/A.
```

### 3.6 Wan 3.0 (API) / Wan 2.2 (open)
- **Wan 3.0.** T2V, I2V and reference-to-video (any mix of image/video/audio refs), 2–30 s at 480/720/1080p, native audio [S18]. #1 on AA T2V v2.0 at $12/min [S1]. Official Alibaba rates are ¥0.3/0.6/1.2 per second (480/720/1080p) [S18].
- **Multi-shot.** On Wan 2.6, set the API flag `shot_type: "multi"` with `prompt_extend: true` [S49]. Wan 3.0's prompt syntax is not documented in sources I could reach **[UNVERIFIED]**. Use the universal grammar plus "Shot N".
- **Wan 2.2 open (Apache-2.0).** LoRA-trainable on your own product. Self-host it, or use Replicate at about $0.45/generation [S18][S50].
- **Example:** use the universal grammar. Add `Shot 1… Shot 2…` and an explicit `Audio:` line.

### 3.7 Runway Gen-4.5 + Aleph 2.0
- **Gen-4.5 is motion-first** [S25][S26]. Start with how the camera and the subject move, then add lighting, mood and film style one detail at a time. Film terms such as "dolly zoom" are honored.
- **Specs.** 2–10 s; First Frame input; seed field; aspect ratios from 21:9 to 9:16. Third-party docs show **no native audio** [S26] **[3P]**.
- **Price.** About $0.12/s [S40] **[3P]**.
- **Aleph 2.0.** In-context editing: add or remove objects, relight, change angles, localized edits with single-frame guidance [S24]. Use it to fix an approved take instead of re-rolling.
- **Example (Gen-4.5 I2V):**
```
Slow dolly-in at product height as warm honey glaze slowly ribbons over the edge of the ceramic cake stand, catching
a hard backlight rim; steam curls upward. Shallow depth of field, 85mm, rich amber tones, food-commercial lighting.
```

### 3.8 Luma Ray3.2
- **Specs.** Up to 20 s at 1080p; **up to 16 keyframes**; 16-bit HDR/EXR export; reframe/extend; tracks up to 8 faces [S27].
- **API price.** About $0.06/s at 720p and $0.24/s at 1080p. HDR costs ×2 and HDR+EXR ×3 [S27].
- **Grammar.** Describe the motion between keyframes. Put the product's exact states into the keyframe images, not the text **[inference]**.

### 3.9 FLUX 3 Video (Black Forest Labs)
- Up to 20 s at 1080p with synced ambient audio. Early access opened 4 Aug 2026 [S22]. #6 on AA T2V at $17.40/min [S1].
- No prompt guide exists yet **[UNVERIFIED for prod]**. Test it on brand-color-critical work.

### 3.10 Midjourney Video V1
- Image-to-video only. `--motion low` gives subtle motion with a static camera; `--motion high` gives dramatic motion. Loop or end-frame option. 5 s base, extendable +4 s up to about 21 s. No audio. About 480p [S30][S31].
- Use it only for mood b-roll from MJ stills.

### 3.11 Higgsfield (platform features, not a model)
- **What's in it.** 50+ models on one credit pool: Seedance, Kling, Veo, Nano Banana and others. **Soul ID** for trained character identity, **Cinema Studio** for lens and camera presets, **Marketing Studio / Click-to-Ad** (URL → ad, built on Seedance 2.0, pulls up to 8 product photos and the logo) [S11][S51].
- **Seedance 2.5 credit cost.** 10 s costs 30 credits at 480p, 70 at 720p and 120 at 1080p, which is $1.50/$3.50/$6.00 [S10].

---

## 4. Image (start-frame) grammar cards

**GPT Image 2 / 2.5 (OpenAI).** Order: **background/scene → subject → key details → constraints**. Put literal text in quotes or ALL CAPS and add font, size and placement [S32]. Two variants: Sunburst (quality and edit precision) and Flare (about 50% faster). Up to 3840 px. New quality tiers `xhigh` and `max` [S35].
```
Seamless warm-beige studio sweep, soft top light and a gentle floor shadow. A matte nude squeeze tube stands upright, slightly
angled 15°. Label reads "SKIMS" in tall condensed sans serif, centered 2 cm below the crimp; micro text "FOR EVERY SMILE" beneath.
Matte tube body, glossy base cap. Constraints: no extra text, no props, label perfectly legible, 4:5.
```

**Nano Banana Pro / Nano Banana 2 (Gemini image).** Write full sentences, "like briefing a photographer". Put the most important detail first, because earlier words carry more weight. When editing, say what changes and what stays [S38]. Pro holds 5 characters and 6 objects at up to 4K [S38]. Use it as the **product-lock pass**: drop the real product photo into the GPT-Image composition [S41].
```
Using the attached product photo exactly as-is (same label, cap, proportions), place the bottle into the attached kitchen scene
on the left third of the counter, matching the scene's warm window light and adding a soft contact shadow. Change nothing else.
```

**FLUX.2 [max].** Use JSON-structured prompts (subject/composition/lighting/camera), HEX codes ("color #02eb3c"), up to 10 refs [S48].

**Seedream 5.0 (Lite/Pro).** Up to 14 reference images. Strong face and identity preservation. Pro adds reasoning and web search. Lite costs about $0.026–0.035/img [S34][S47].

**Ideogram 4.0.** Open weights, but the license is non-commercial. Bounding-box layout, JSON prompting, hex palette conditioning, up to 2048 px. Use it for **end cards and type-led frames** [S39].

---

## 5. Head-to-head evidence (who wins what)

| Source (date) | Finding |
|---|---|
| AA T2V v2.0 leaderboard (Oct 2026) [S1] | 1 Wan 3.0 (1156), 2 Utopai X (H3-based), 3 Seedance 2.5 (1143), 4 MiniMax H3 (1137), 6 FLUX 3, 7 Seedance 2.0, 8 Gemini Omni Flash 1.1, 15 Kling 3.0 Omni, 18 Veo 3.1 (962). Wide CIs of ±99–109, so ranks 1–8 are statistically close. |
| AA I2V leaderboard (Oct 2026) [S2] | 1 MiniMax H3 Max (1195), 2 H3 (1181), 3 Gemini Omni Flash (1178), 4 Seedance 2.0 720p (1176), 6 Wan 3.0, 11 Veo 3.1, 19 Kling 3.0 Pro (1055). |
| AA with-audio arena (Aug 2026, via [S44]) | Omni Flash 1245 > H3 1242 > Seedance 2.0 1225 … Kling 3.0 1113 > Veo 3.1 1098. |
| Krea: Seedance 2.5 vs Veo 3.1 (5 Sep 2026) [S45] | Seedance wins speaking shots, duration, aspect ratios and cost. Veo wins resolution, audio quality and physics. Speed is a tie. |
| fal: Seedance 2.0 vs Kling 3.0 [S43b] | Kling wins prompt control (CFG and negatives), character consistency (elements) and budget. Seedance wins audio-included pricing, multimodal refs and 21:9. |
| invideo: Kling 3 vs Veo 3.1 (Aug 2026) [S44] | Kling wins duration, voice cloning, multi-shot and motion transfer. Veo wins 4K, audio polish, refs and indemnity. |
| Krea ecommerce roundup [S40] | Kling for packaging-sensitive motion. Seedance for multi-variant social. Gen-4.5 for material accuracy. Veo for lifestyle with audio. PixVerse for budget catalog. |
| HumanSignal physics test (23 Sep 2026) [S46] | Seedance 2.5, Veo 3.1 and Kling 3.0 Pro **all fail** the water pour. Cloth is improved. Mechanical geometry warps. Character consistency through references is the "manageable part". |

**Caveat.** AA arenas measure general preference. None of them measures label or brand fidelity specifically. Run your own 5-shot product test before you commit **[inference]**.

---

## 6. Failure mode → fix table

| Failure | Cause | Prompt / workflow fix | Src |
|---|---|---|---|
| **Label text morphs / gibberish** | Small text destabilizes under motion | Minimize motion near the label. Use a slow push-in, not an orbit. "label stays unchanged". **Composite the approved label plate in post** (motion-track). Add logo and CTA in the editor. | [S42][S52][S8] |
| **Product silhouette warps (cap diameter, bottle taper)** | Loose reference, aggressive camera | "Product is rigid and does not bend, stretch, taper, duplicate or redesign". Risk ladder: locked frame < push-in < slide < 10° orbit < full spin. Use a cleaner 3/4 hero reference. | [S42] |
| **Product melts / warps** | Low-res or busy start frame | Use a sharp start frame of 1080p or more with a simple backdrop | [S52] |
| **Extra fingers / grip changes the product** | Hand interaction on critical surfaces | Grip low on broad surfaces. One action per clip (lift, turn or place). Put the hand in the start frame. | [S42] |
| **Liquid creates or loses volume, fake pours** | Model physics limit | Keep it short (≤3 s) and macro, use cuts to hide the transfer, or use a real or CG liquid plate. Prefer Kling or Veo for the look. | [S46] [inference] |
| **Camera drift / jitter / mid-clip direction change** | Stacked camera moves | One move per shot plus an end state. Use "cut to" or Shot N for the next move. | [S5][S8][S16] |
| **Scene smear / morphing between locations** | Too many beats for the duration | Match complexity to duration. Use timelines or Shot N for clips of 8 s or more. | [S8] |
| **Reference bleed (wrong lighting or framing copied)** | Reference with no assigned role | Give each ref a job: "Image 2 = lighting only" | [S8][S16] |
| **"Cardboard" or plastic characters** | Reference strength maxed | Keep strength at 70–80% | [S8] |
| **Start image transforms instead of anchoring** | Image used as a loose ref | Use Start-Frame mode plus an alignment line ("Picture 1 aligns with 0.00 s") | [S16] |
| **Random music / wrong audio** | Empty audio slot | "no music" / `non_diegetic_music: N/A`. Keep SFX next to their actions. | [S8][S16] |
| **Wrong speaker / original words reused** | Voice ref not mapped | "Video 1 supplies timbre only; Speaker 1 says: <d>…</d>" | [S16] |
| **Garbled on-screen text in video** | Mixed languages, rare glyphs | Use one language and common words, or do subtitles and supers in post | [S8][S5] |
| **Failure appears only in the last frames** | Drift late in the clip | Trim the clip instead of regenerating it | [S42] |
| **Over-editing in conversational edits** | Vague edit | Change one variable per turn and list what stays | [S28] |
| **Flicker / texture crawl on skin and fabric** | Low native res (480–720p) | Diffusion upscale (Topaz Starlight Precise 2.5/2.6) to 1080p/4K | [S53] |
| **Inconsistent takes** | Sampling variance | Lock the seed where supported (Runway, Veo, Kling API). Batch-select. | [S26][S43][S52] |

---

## 7. Workflow used by top AI ad creators (2026)

1. **Brief → shot list.** Many teams use an LLM project with brand docs to lock the script and visual direction first [S41b] **[3P]**.
2. **Start-frame-first (two-stage image).** GPT Image 2/2.5 builds composition, environment and light. Then Nano Banana runs a "product lock" pass that inserts the exact product [S41]. Keep design specs explicit (logo shape, kerning, placement relative to features, material) and add hard negatives. For variant frames, say: "Keep the exact same design, typography, layout, lighting, camera angle, background" [S39b].
3. **Approved hero frame gate.** Don't start motion until a hero still is signed off [S42].
4. **Animate.**
   - Packshots: start+end frame on Kling or H3 [S7][S16][S39b].
   - Multi-shot reels: Seedance with named references [S5].
   - Lifestyle with dialogue: Veo or Seedance [S45].
   - One action per clip, 5 s clips first [S42][S52].
5. **Iteration ratio.** Generate **3–4 variants per shot and pick 1** [S52]. Budget for about 5× the final duration in generated seconds (a 30 s cut ≈ 150 s generated) [S14]. Use binary accept/reject per unit and rerun only failed units [S42].
6. **Fix, don't re-roll.** Use region or element edits (Aleph 2.0, Seedance 2.5 region edit, Omni conversational edit) on otherwise-approved takes [S24][S10][S28].
7. **Post.**
   - Composite the real label or logo plate.
   - Add supers, CTA and captions in the editor (feeds autoplay muted).
   - Export 1080×1920.
   - Upscale with Topaz Starlight Precise 2.5/2.6, or Astra 2 for 4K [S52][S53][S42].
8. **Scale variants.** Put 3–5 copy and hook variants over one hero clip to amortize generation cost [S52]. Keep reference photos, candidate clips and the approved frame together to catch identity drift before media buying [S40].

---

## 8. Prices & access (USD, Oct 2026; verify at checkout)

**Direct / official API, per second of output**

| Model | Price | Src |
|---|---|---|
| Veo 3.1 Standard | $0.40 (720/1080p), $0.60 (4K) | [S12] OFFICIAL |
| Veo 3.1 Fast | $0.10 (720p) → $0.30 (4K) | [S12] OFFICIAL |
| Veo 3.1 Lite | $0.05 (720p), $0.08 (1080p) | [S12] OFFICIAL |
| Gemini Omni Flash 1.1 | ≈$0.10/s at 720p ($17.50 per 1M video tokens) | [S12] OFFICIAL |
| Wan 3.0 (Alibaba) | ¥0.3 / 0.6 / 1.2 per second (480/720/1080p) ≈ $0.04/0.08/0.17 | [S18] |
| Kling 3.0 Turbo (CN) | from ¥0.8/s at 720p | [S19][S44] |
| Luma Ray3.2 | ≈$0.06 (720p), $0.24 (1080p); HDR ×2 | [S27] |
| Runway Gen-4.5 | ≈$0.12/s | [S40] 3P |

**fal.ai (pay per second)**
- Kling 3.0 Pro: $0.112/s without audio, $0.168 with audio, $0.196 with voice control, $0.336 with elements. Kling 3.0 Std: $0.084 [S43b].
- Seedance 2.0: $0.3034/s standard, $0.2419/s fast. Video input multiplies cost by 0.6 [S43b].
- Seedance 2.5: about $0.22/s at 480p and $0.47/s at 720p [S54] **[3P]**. Krea quotes "$0.0645/s" via another API, so prices vary a lot by host [S45].
- MiniMax H3 Max Camera: $0.05/0.08/0.16 per second. H3 standard from $0.10/s [S17].
- GPT Image 2.5 is live on fal [S35].

**AA cost per minute** (1080p default) is a useful cross-host comparison [S1][S2]. Examples: H3 $4.80, Omni Flash $6–9, Kling 3.0 Pro $10–20, Wan 3.0 $12, Seedance 2.5 $34, Veo 3.1 $24.

**Images (per image)**
- Nano Banana 2 (Gemini 3.1 Flash Image): $0.067 at 1K, $0.101 at 2K, $0.151 at 4K [S12].
- Flash-Lite image: $0.034 [S12].
- GPT Image 2/2.5 max/high: about $0.21 [S3].
- Seedream 5.0 Pro: about $0.09 [S3]. Seedream 5.0 Lite: about $0.026–0.035 [S47].

**Subscriptions / aggregators**

| Platform | Plans | Notes | Src |
|---|---|---|---|
| Higgsfield | Starter $15 (200 cr), Plus $49 (1,000), Ultra $129 (3,000) | Seedance 2.5 requires Plus or above. 10 s at 1080p = 120 cr. Soul ID, Cinema Studio, Click-to-Ad. | [S11][S10] |
| Dreamina (CapCut) | Seedance 2.5 ≈ $0.097/s (annual Advanced). Seedance 2.0 ≈ $0.046–0.055/s. | Cheapest first-party Seedance | [S14] |
| Kling (direct) | Standard $10, Pro $37, Premier $92, Ultra $180 /mo | Kling 4.0 Flash is Ultra-yearly only | [S44][S20] |
| Freepik | Premium $20, Premium+ $45, Pro $280 /mo | "Unlimited" covers only about 10 image models. Video burns credits (80–3,000 per clip). | [S55] |
| Krea | Basic $9 (5k CU), Pro $35 (20k), Max $105 (60k), Business $200 | Pro and above for all video models | [S56] |
| Figma Weave (ex-Weavy) | Free 150 cr, Starter $24, Professional $45, Team $60 | Node-based pipelines. Video only on paid plans. Video costs about 15× image credits. | [S57] |
| Luma Dream Machine | Plus $30/mo (10k credits) | Ray3.2 | [S27] |
| Midjourney | Basic $10, Pro $60, Mega $120 | Video V1 included | [S31] |
| Replicate | Wan 2.2 ≈ $0.45/gen | Open models | [S50] |

**Routing rule of thumb.** Run iteration on fal or Dreamina per-second (Veo Lite, H3, Kling Std). Run finals on the best-fit model at target resolution. Run subscription platforms (Higgsfield, Krea, Weave) when you need many models with one UI or one credit pool, or node pipelines **[inference]**.

---

## 9. Open questions / to verify before production
- Did the MiniMax H3 open weights actually ship, and under what license? [S15]
- What is Wan 3.0's official prompt syntax (Shot markers, audio tags)?
- When will Kling 4.0 reach the API (expected Oct 2026)? Specs to check: 30 s, 10 keyframes, 15 refs, 4K [S20].
- Is Nano Banana 2.1 public?
- Does Runway Gen-4.5 have native audio? (The third-party page says no.)
- Seedance 2.5 per-second price varies by host from $0.06 to $0.47/s, so the actual cost depends on which host you use.

---

## Sources
- [S1] AA Text-to-Video leaderboard — https://artificialanalysis.ai/video/leaderboard/text-to-video
- [S2] AA Image-to-Video leaderboard — https://artificialanalysis.ai/video/leaderboard/image-to-video
- [S3] AA Text-to-Image leaderboard — https://artificialanalysis.ai/image/leaderboard/text-to-image
- [S4] AA Image Editing leaderboard — https://artificialanalysis.ai/image/leaderboard/editing
- [S5] BytePlus ModelArk, Dreamina Seedance 2.0 Prompt Guide (official) — https://docs.byteplus.com/en/docs/ModelArk/seedance-2-0-prompt-guide (zh: https://docs.byteplus.com/zh-CN/docs/modelark/seedance-2-0-prompt-guide)
- [S5b] Seedance 2.0 limits summary — https://docs.byteplus.com/zh-CN/docs/modelark/seedance-2-0-prompt-guide (via search summary; datacamp: https://www.datacamp.com/tutorial/seedance-2-0-api-guide)
- [S6] Google Cloud, Ultimate prompting guide for Veo 3.1 (official) — https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- [S7] Kling VIDEO 3.0 Model User Guide (official) — https://kling.ai/quickstart/klingai-video-3-model-user-guide
- [S8] Seedance 2.0 Prompt Guide: Best Practices & Failure Modes (Jul 2026) — https://www.heyuan110.com/posts/ai/2026-07-11-seedance-2-prompt-guide/
- [S9] Seedance 2.5 overview — https://www.miracamp.com/learn/content-creation/seedance-2-5-bytedance ; https://news.ainauten.com/de/story/bytedance-reveals-seedance-25-the-ai-video-generator-redefining-cinematic-storytelling
- [S10] Higgsfield, Seedance 2.5 on Higgsfield — https://higgsfield.ai/blog/seedance-2-5-on-higgsfield-2026
- [S11] Higgsfield plans/Seedance 2.5 tiering — https://kive.ai/learn/is-higgsfield-worth-it ; https://www.pippit.ai/resource/pippit-vs-higgsfield-seedance-2-5-price
- [S12] Gemini API pricing (official) — https://ai.google.dev/gemini-api/docs/pricing
- [S13] Veo 3.1 features (Atlas Cloud) — https://www.atlascloud.ai/blog/guides/google-veo-3.1-features
- [S14] Dreamina Seedance price guide — https://dreamina.capcut.com/seedance/seedance-price
- [S15] MiniMax H3 launch — https://pasqualepillitteri.it/en/news/9204/minimax-h3-2k-ai-video-open-weights ; https://unifically.com/models/minimax-hailuo-h3
- [S16] RunDiffusion, MiniMax H3 Prompt Guide — https://www.rundiffusion.com/minimax-h3-prompt-guide
- [S17] fal, H3 Max Camera Controls — https://fal.ai/learn/tools/what-is-h3-max-camera-controls
- [S18] Atlas Cloud, Is Wan 3.0 open source? — https://www.atlascloud.ai/blog/tips/is-wan-3.0-open-source ; https://openrouter.ai/alibaba/wan-3.0
- [S19] Kling 3.0 release / no official 3.5 — https://gaga.art/blog/kling-3-0/ ; https://anikuku.com/zh-Hans/blog/kling-4-release-date-latest-version-2026
- [S20] WaveSpeed, Kling 4.0 release status (1 Oct 2026) — https://wavespeed.ai/blog/ai-news/kling-4-0-release-date/
- [S21] Apiframe Kling 3.0 API guide — https://apiframe.ai/guides/kling-3-0-guide
- [S22] FLUX 3 release — https://datanorth.ai/news/black-forest-labs-releases-flux-3 ; https://gigazine.net/gsc_news/en/20260805-flux-3-video
- [S23] Runway Gen-4.5 — https://www.eweek.com/news/runway-ai-video-model/ ; https://openrouter.ai/runway/gen-4.5-20260729
- [S24] Runway Aleph 2.0 (via search summary) — https://runware.ai/collections/family-runway **[UNVERIFIED primary]**
- [S25] Runway help center Gen-4.5 section (official, blocked to fetch) — https://help.runwayml.com/hc/en-us/sections/47297541368595-Gen-4-5
- [S26] Scenario, Runway Gen4.5 essentials — https://help.scenario.com/articles/5854126955-runway-gen4-5-the-essentials
- [S27] Luma Ray3.2 — https://itbrief.news/story/luma-launches-ray3-2-with-tighter-ai-video-control ; https://picsart.com/ai-models/luma-ray-3-2/
- [S28] Gemini Omni prompt guide summary — https://www.atlascloud.ai/blog/guides/gemini-omni-prompt-guide ; official: https://deepmind.google/models/gemini-omni/prompt-guide
- [S29] Cliprise, Gemini Omni Flash guide — https://www.cliprise.app/learn/guides/model-guides/gemini-omni-flash-complete-guide
- [S30] Midjourney V1 video — https://kod.ru/midjourney-new-video-model ; https://docs.midjourney.com/docs/video
- [S31] Midjourney video review 2026 — https://www.flowjam.com/blog/midjourney-video-review-2026 ; https://www.cined.com/midjourney-video-generator-announced-can-it-compete/
- [S32] GPT Image 2 prompt guide (cites OpenAI cookbook) — https://www.atlascloud.ai/blog/gpt-image-2-prompts-guide ; https://crepal.ai/blog/aiimage/image-how-to-use-gpt-image-2-for-product-mockups/
- [S33] GPT Image 2 launch — https://fal.ai/learn/tools/what-is-gpt-image-2 ; https://neurohive.io/en/news/chatgpt-images-2-0-openai-launches-image-generation-model-with-reasoning-2k-resolution-and-multilingual-text/
- [S34] Seedream 5.0 — https://www.mindstudio.ai/models/seedream-v5-0-lite ; https://pexo.ai/blog/what-is-seedream-5-0-pro-5247
- [S35] GPT Image 2.5 Flare/Sunburst — https://docs.apiyi.com/en/news/gpt-image-2-5-launch ; https://fal.ai/gpt-image-2.5
- [S36] Kling 3.0 Turbo — https://www.atlascloud.ai/blog/guides/kling-3.0-review-features-pricing-ai-alternatives
- [S37] Nano Banana 2.1 status — https://testingcatalog.com/new-google-flow-build-now-points-to-nano-banana-2-1 ; https://www.piclumen.com/blog/nano-banana-2-1/
- [S38] Nano Banana Pro official-guide summaries — https://pasqualepillitteri.it/en/news/856/nano-banana-prompt-official-google-guide ; https://www.techradar.com/ai-platforms-assistants/gemini/3-advanced-strategies-for-making-the-most-of-nano-banana-pro ; https://morphic.com/kr/resources/models/nano-banana-pro
- [S39] Ideogram 4.0 — https://noqta.tn/en/news/ideogram-4-open-weight-image-model-design-2026 ; https://comfyui-wiki.com/en/models/ideogram/ideogram-4
- [S39b] fooh, SKIMS toothpaste AI ad (NB Pro + Kling 3.0) — https://www.fooh.com/blog/skims-toothpaste-ai-ad
- [S40] Krea, Top 6 AI video models for ecommerce ads 2026 — https://www.krea.ai/blog/top-6-ai-video-models-for-ecommerce-ads-in-2026
- [S41] invideo, two-stage GPT Image + Nano Banana — https://invideo.io/faq/how-does-the-two-stage-gpt-image-and-nano-banana/
- [S41b] Creator workflow (LLM project → NB Pro/GPT Image → Kling) — https://alexcooper.beehiiv.com/p/inside-our-ai-animation-ad-process-at-adcrate **[3P, not fetched]**
- [S42] Seedance.tv, keep product shape consistent — https://www.seedance.tv/blog/how-to-keep-product-shape-consistent-in-ai-video-ads ; label plate compositing: https://dreamina.capcut.com/ai-video/fix-product-details-in-ai-video
- [S43] Atlas Cloud, MiniMax H3 vs Veo 3.1 — https://www.atlascloud.ai/blog/guides/minimax-h3-vs-veo-3.1
- [S43b] fal, Seedance 2.0 vs Kling 3.0 — https://fal.ai/learn/tools/seedance-2-0-vs-kling-3-0
- [S44] invideo, Kling 3 vs Veo 3.1 (Aug 2026) — https://invideo.io/blog/kling-3-vs-veo-3-1/
- [S45] Krea, Seedance 2.5 vs Veo 3.1 (5 Sep 2026) — https://www.krea.ai/blog/seedance-2-5-vs-veo-3-1-which-is-better-full-comparison-2026
- [S46] HumanSignal physics test summary (23 Sep 2026) — https://novoads.ai/en/blog/ai-video-physics-test
- [S47] Atlas Cloud, best AI image models 2026 — https://www.atlascloud.ai/blog/best-ai-image-generation-models-2026
- [S48] FLUX.2 prompting (JSON/HEX/multi-ref) — https://fal.ai/learn/devs/flux-2-prompt-guide ; https://docs.together.ai/docs/quickstart-flux-2
- [S49] Wan 2.6/2.7 — https://evolink.ai/blog/wan-2-6-api-guide ; https://apiframe.ai/guides/wan-2.7-guide
- [S50] Replicate Wan — https://replicate.com/collections/wan-video ; https://www.flowjam.com/blog/wan-ai-review-2026
- [S51] Higgsfield Click-to-Ad / Marketing Studio — https://geo.higgsfield.ai/higgsfield-ai-features-guide ; https://higgsfield.ai/blog/best-ai-platforms-create-ads-from-url
- [S52] Creative AI News, product photo → video ad 2026 — https://www.creativeainews.com/blog/ai-product-photo-to-video-ad-2026/
- [S53] Topaz Starlight for AI video — https://docs.comfy.org/tutorials/partner-nodes/topaz/video-enhance-starlight-precise-2-5/workflow ; https://invideo.io/faq/what-is-topaz-starlight-25-and-why-is-it-used-for-ai/ ; https://fal.ai/learn/tools/video-to-video-upscalers
- [S54] Seedance 2.5 fal pricing — https://www.atlascloud.ai/blog/tips/seedance-2-5-api-transparent-pricing-no-enterprise-contract ; https://melies.co/seedance-2-5-pricing
- [S55] Freepik pricing 2026 — https://eesel.ai/blog/freepik-ai-pricing ; https://dailyaifixs.com/blog/freepik-ai-pricing-2026-the-unlimited-catch
- [S56] Krea pricing — https://www.hooked.so/compare/krea-ai-pricing ; https://www.costbench.com/software/ai-image-generators/krea/
- [S57] Figma Weave pricing — https://weave.figma.com/pricing ; https://help.weavy.ai/en/articles/12267070-figma-weave-s-subscription-plans
