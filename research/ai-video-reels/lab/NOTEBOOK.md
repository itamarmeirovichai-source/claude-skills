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
