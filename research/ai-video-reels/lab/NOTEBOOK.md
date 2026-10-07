# Lab notebook

Every entry has a date, an experiment, a finding, the supporting number and a decision. Reports are appended automatically by `lab.py report`.

### 2026-10-07 · setup
- Protocol, hypotheses H1–H6 and caps written **before** any generation (PROTOCOL.md).
- Budget: lab cap $45; gates at $10 / $20 / $35 / $45.
- Endpoints verified in Higgsfield docs: Seedance 2.5 (i2v/t2v/ref), Kling 3.0 (pro i2v, std t2v), Hailuo 2.3 (std i2v/t2v), Marketing Studio Flare, Soul v2.

### 2026-10-07 · F01 AURUM: the DESIRE breakthrough (user: "וואו עכשיו אנחנו מדברים", "wow, now we're talking")
- **What failed:** the still animatic had a good joke (Florida man vs alligator over a cooler) but **zero product desire**. The bottle appeared at 0:20, inside story scenes. User verdict: "it doesn't make people buy" + "it's just pictures, nothing moves".
- **What won:** three Celsius-standard crave stills (Flare 2k, $0.30 each) + one 5 s Kling 3.0 Pro i2v motion clip (sound off, $0.47). The user reacted with immediate excitement. Prompts: `experiments/F01_florida_man/plan_1d_crave.json`, `plan_1e_motion.json`.
- **Why it works (Celsius anatomy, now in creative-brain §1b):**
  - A brand colour world: AURUM = champagne gold + glacier teal (gradient backdrop).
  - A glossy mirror surface doubles the product.
  - Cold proof: dense droplets, one drop running through the logo, vapour.
  - Real props: ice spheres, lime, mint.
  - Hard key + rim light with crisp speculars.
  - The product is centred and fills 50–55% of the frame height.
- **Motion finding:** Kling Pro i2v from a macro still kept the embossed AURUM logo stable for the full 5 s, with a drop slide, vapour and a light sweep. The "slow push-in + droplets + light sweep" recipe is the safe default for crave shots.
- **Decision (permanent rules):**
  1. Law 5 DESIRE in creative-brain: crave shots ≥ 30% of runtime, the product in the first 2 s, every product shot moves.
  2. Every flagship starts with 3 hero recipes (studio colour world / macro cold proof / action splash) **before** story shots.
  3. Show the user a moving crave clip early. Stills-only animatics confuse the client; label them clearly as a timing test or skip them for clients.
- **Spend:** F01 total $4.14 of $17.

### 2026-10-07 · F01 AURUM v1 delivered (video)
- **Model mix:** 3 dialogue shots on Seedance 2.5 reference-to-video, with the ElevenLabs lines as `audio_urls` (standoff 480p 8 s $1.65; anchor and reporter 720p 8 s $3.70 each). Crave and action shots on Kling 3.0 Pro i2v (5 s, sound off, $0.48 each).
- **Spend:** F01 total $15.09 of $17.
- **Findings:**
  - Lip-sync from audio refs looks right on the anchor and reporter; the clean ElevenLabs audio is re-laid in the edit.
  - One 8 s anchor take covered two lines (the opener and the "Back to you, Gary" button). Combine a character's lines into one ref to save a clip.
  - The Kling cooler burst rendered the bottle small and gold (reads like a can). Next time pass the bottle as an end frame or a reference.
  - QC: -14 LUFS. The 5.6 s reporter shot is too long for Reels. The runtime is 34 s; the target was 30.
- **Edit:** music silence placed by cutting the bed (0–14 s, 19–26.6 s, 3 s silence, then the 19 s+ section again). The tagline captions were removed so they don't duplicate the AURUM title.
- Spec: `experiments/F01_florida_man/F01_AURUM_v1.json`, plan `plan_2_video.json`.

### 2026-10-07 · F01 pivot: the user rejected the comedy concept and wants clean aesthetic brand films
- **User verdict on v1:** "really bad". They did not like the concept. They want something aesthetic and clean, where you recognise the brand. They also said the speech does not match the video's speed: Seedance audio-ref lip-sync drifted, and the 480p and 720p shots clash with the 1080p crave shots.
- **Delivered instead:** `F01_AURUM_clean.json`, a 20 s brand film with no dialogue, built from 7 crave shots:
  1. macro drop
  2. cap twist with vapour
  3. splash
  4. ice drop on the mirror
  5. orbit on marble
  6. studio push-in
  7. serif end card: "AURUM / Cold. Pure. Gold."
  - Sound: ElevenLabs luxury score (92 BPM, with a breath of silence before the logo) plus ASMR SFX (cap twist, ice drop, soft whoosh, logo boom).
  - Extra spend: 3 Kling shots, $1.43. **F01 total $16.52 of $17.**
- **Standing preferences of this client (apply by default):**
  1. Premium and aesthetic beats comedy sketches. Brand recognition first: the logo is legible in most shots, plus a colour world and a serif end card.
  2. Avoid talking heads and lip-sync unless asked. If dialogue is needed, use 1080p and check the sync before the edit.
  3. Everything in motion, Celsius-level product stills as the base.
- **Brain change:** before writing jokes, ask (or infer) the **tone**: aesthetic brand film / ASMR ritual / comedy / UGC. This client's default is the aesthetic brand film.

### 2026-10-07 · User on the AURUM clean film: "better, but still not perfect"
Self-critique against the new research briefs (marketing/01, 02):
1. **Monotony:** 7 shots with the same centred bottle and similar framing. No shot-size variety (wide, mid, macro), no scale and no context.
2. **Inconsistent colour world:** the backgrounds jump between a teal/gold gradient, black marble and dark bokeh. One set and one palette per film.
3. **No consumer scene or ritual:** no hand, glass, pour or sip. Research shows craft plus a consumer scene raises purchase intent.
4. **No mechanism or single-minded claim:** "SOURCE 1987" is never paid off. The film never shows *why* this water.
5. **No CTA and no sonic logo designed as a brand asset.** Pacing is uniform, with no speed ramp and no peak.
→ Next flagship must pass the 15 gates in `marketing/01-fundamentals.md` §7 before generation.

### 2026-10-07 · F02 VESPER (fragrance) delivered: first flagship built from the marketing master playbook
- **Why this niche:** fragrance is the #1 niche for AI in `marketing/02-niches.md`. It needs no literal proof, and glass, mist and visualised notes play to AI's strengths. It is a new niche (F01 was a beverage).
- **Brand kit:**
  - Colours: oxblood burgundy #4A0E17, black and amber gold #E8C27A.
  - Type: Liberation Serif with wide tracking.
  - Sonic logo: a crystal chime. Recurring motif: glass clink and spray.
  - Claim: "Wear the golden hour."
  - Mechanism: 3 notes shown on screen.
  - Entry point: "For the hour after sunset".
  - CTA: "Discover the sample set", which de-risks a blind buy.
- **Pipeline that worked:**
  1. 2 product refs (Flare, text-only) → pick one.
  2. 8 stills with a **prompt lock + colour-world line + negatives**, all referencing the product image. The bottle stayed identical across every still.
  3. Kling 3.0 Pro i2v, 5 s, sound off: one move per shot, "only X moves".
  4. Music with a timestamped structure, ASMR SFX, and a whispered VO line only at the end (Lily voice, eleven_v3 tags).
- **Failures and fixes:**
  - The neck/bare-shoulder prompt hit the Flare safety filter. A hand holding the bottle against a blazer passed.
  - The Kling 90° orbit drained the juice colour and morphed the label after ~2.5 s. Keep orbits under 2.5 s, or limit them to ≤60°.
  - Kling push-ins grow the product into the title space. For type, cut to the **still** end frame (gentle zoom-out) instead of the moving clip.
  - Supers over busy areas need a soft dark box.
- **Cost: $6.81** (refs $0.60, stills $2.40, the failed S6 still was not billed, the S6 retake $0.30, motion $3.81). Under the $10 cap.
- Spec: `experiments/F02_vesper/F02_VESPER_v1.json`.

### 2026-10-07 · F02 VESPER v2: "good but not enough" → add ONE BIG IDEA
- **Diagnosis of v1:** it was beautiful but a "catalogue". It had no single visual idea that stops the scroll or that people retell.
- **Fix:** literalise the claim. "Wear the golden hour" became **the sun sets into the bottle**.
  - Flare start/end key frames: W1 has the sun aligned behind the cap; W2 is blue hour with the bottle glowing.
  - Kling 3.0 Pro i2v with `last_image_url` timelapse. Excellent: the sun passes through the cap and the city refracts inside the juice. ($0.48)
  - Payoff shot: a tiny sun swirling inside the perfume, "A sunset, captured."
- **Finish upgrades:**
  - Downloaded Google Fonts Cinzel (logo) and Cormorant Garamond (copy) into `~/.cache/reel-studio/fonts` via the fonts.googleapis CSS API with UA "Wget" (returns .ttf).
  - Global glow/halation 0.35, film grain overlay, vignette.
  - light_leak transitions only (max 2 transition types).
  - Notes shots cut to 1.6 s.
- **Rule for the brain:** every flagship needs a **"big idea shot"**: the claim made literally visible in one impossible-but-elegant image. It opens the film and gets paid off later. Design it FIRST, then the rest.
- **Cost:** v2 added $1.85, so F02 total is **$8.66** of $10.

### 2026-10-07 · "Looks too AI" → studied 80 YouTube tutorials (17.7 h of transcripts) → VESPER v3
- **Method:** `youtube/fetch_yt.py` (yt-dlp search plus auto-subs). youtube-transcript-api is IP-blocked here; yt-dlp subtitles work. 80 of 114 videos had transcripts. 4 parallel readers, one per theme.
- **New references:**
  - `marketing/05-real-dp-cinematography.md`: how real DPs light glass, plus a real-shoot prompt vocabulary
  - `06-anti-ai-realism.md`: top 15 fixes for "too AI"
  - `07-ai-product-ad-workflows.md`: what working AI ad studios do
  - `08-post-production.md`: edit, grade and sound recipes
- **v3 changes (free, post-only):**
  - Film chain (`experiments/F02_vesper/film_chain.txt`), in this order: 24 fps → 30% soft-blur mix → lifted-black curve → mild warm balance → vibrance −0.12 → highlight-only halation at 16% → temporal grain → light unsharp → vignette → luma flicker → gate weave.
  - Encode with `-tune grain`. Web versions need a bitrate cap (~2.8 Mb/s at 720p), otherwise grain inflates the file.
  - Sound bed in 6 layers (room tone and city bed, rooftop wind, layered foley, riser + boom), with SFX J-cut ~0.2 s ahead of the picture.
  - Cuts only; no light-leak transitions.
- **Lesson:** a teal-shadow split tone on a burgundy world turns everything purple. Keep the split tone inside the brand's palette.
- **Still AI, and post can't fix it:** the *source generations* are perfectly symmetrical, centred and glossy, with one soft glow light. The real fix is regenerating with the 05/06 vocabulary:
  - one hard snooted sliver of light that falls off fast
  - off-centre three-quarter angles
  - named imperfections (dust, micro-scratches, fingerprints)
  - a ban list (no HDR, no oversaturation, no CG perfection)
  - handheld micro-movement and no locked-off camera
  - lens variety (16 mm wide, macro, 85 mm)
  
  This needs budget beyond F02's $10 cap.

### 2026-10-07 · Deep study round 2: niche playbooks + Higgsfield + ElevenLabs mastery
- **Six parallel studies, all saved under `skills/ad-director/references/marketing/`:**
  - 11-niche-{beauty, food-drink, fashion-luxury, tech-home}
  - 12-higgsfield-mastery: 85 live endpoints, verified prices
  - 13-elevenlabs-mastery: eleven_v4, music_v2_5 composition plans
- **Real-ad frames were viewed** via adsoftheworld's video host (17 luxury ads) and YouTube storyboard/thumbnail frames. Full YouTube downloads are bot-blocked from this IP.
- **`elevenlabs.py` upgraded:**
  - music now defaults to `music_v2_5`
  - `--plan` composition plans
  - SFX `prompt_influence` default changed to 0.3
- **E06 lookboard:** 16 niches, Soul Cinema, $0.06 total. The film-still realism is excellent, with real light falloff and lived-in sets.
- **Caveats:**
  - Several frames are underexposed. Add "exposed for the subject".
  - The sneaker came out with a swoosh-like mark. **Soul Cinema renders real trademarks unprompted**, so every output needs a logo screen and a "plain unbranded" line.
