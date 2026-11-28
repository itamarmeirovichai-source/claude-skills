# 21 · Validation audit: will the automated ad routine really work? (2026-10-08)

Scope: the planned flow (product → ideas → zero-cost pre-test → 3 storylines → client pick → shot plan → stills → seamless video → ElevenLabs → edit/grade → QC → deliver), checked against chapters 00–20, `creative-brain.md`, `image-direction.md`, `model-router.md`, the scripts, reel-studio and the NOTEBOOK (F01–F03).

**No money was spent.** Only free calls were made: `/models`, `/estimate`, `hfgen batch --dry-run`, the public docs, ElevenLabs `subscription`/`models`/`voices` and the free `/v1/music/plan` (character count 5,518 before and after). Raw outputs sit in the temporary session scratchpad `validate/`. `[inf]` = inference.

## 0. Verdict

1. **Buildable with today's tools.** Every needed endpoint is live with the documented parameters; all tests pass; every ffmpeg seam recipe and the film chain run.
2. **Three silent traps** (§2.2): `/estimate` accepts unknown keys; `hfgen` dry-runs count unpriced jobs as $0; Qwen edit rewrites prompts unless *two* flags are off.
3. **The seamless-film keystone is untested.** No mid-chain Kling bridge with a camera move and no-settle wording has ever been generated (F02/F03 used `last_image_url` only on near-static shots). Buy this first (§4).
4. **15's pre-test can't run as written:** Claude-only, no embeddings, no temperature. Substitute in §3.
5. **20 contradictions**, each ruled in §1 (NOTEBOOK evidence beats web claims).

---

## 1. Contradictions and rulings

Evidence order: our NOTEBOOK results > live API checks > official docs > practitioner videos > inference.

| # | Topic | Where the chapters disagree | Evidence | **Ruling** |
|---|---|---|---|---|
| C1 | **Who writes Kling prompts** | 20 §1.3 (Rourke): "never prompt Kling with AI", ~90 % failure. 14/18 §4.8: Claude subagents write the prompts. | All 26 Kling prompts in F01–F03 were Claude-written (51–83 words). All were usable except the 90° orbit. | Claude writes Kling prompts **only by filling a fixed slot template**: one camera move, the one thing that moves, the product-lock line, the speed clause and negatives, in 50–90 words. No open-ended LLM expansion; `enhance_prompt`/`prompt_extend` are off everywhere. Each retake changes one clause and gets logged. Long structured treatments are for Seedance only (≤3,000 chars). |
| C2 | **Settle vs no-settle** | 12 templates C/D, 09 and 08 say "decelerating into a static hold" or "fast start, slow settle"; video-realism R2 asks for "settle". 16 §2.1, 06 and 11-fashion say "already moving, constant speed, never settle". | F03 used "Already at full speed, no slow-motion easing" on 5 clips and got no slow-mo. A bridge with an end frame is untested. | **Decide by role.** The final packshot settles and holds, or cuts to the still (F02 lesson). Every other clip uses "already at full speed, constant speed, does not slow or settle". Always trim 6–10 frames at each end (R3). Whether Kling obeys no-settle *with* `last_image_url` is tested in T2. |
| C3 | **Centred vs off-centre** | image-direction §0 and creative-brain §1b: centred, 50–55 % of frame height, "hyper-real, saturated". 00 hard rules, 06, 12 §0.8 and 17 rule 6: off-centre. | F01's centred crave stills got "wow". F02 v3's diagnosis was "too AI = symmetrical, centred, glossy". image-direction's own §1 table says CELSIUS is *off-centre*. | Centred is allowed **for at most 2 shots**: the crave hero and the end packshot. Story, insert and bridge frames are off-centre (Soul plate → Flare composite). Strike "hyper-real, saturated" from the image-direction §0 template. |
| C4 | **Labels: generate or composite?** | 00 ("generate labels blank, set type in post"), model-router ("always composite the label plate") and 20 §4 A4. Against them: 12, 16 and NOTEBOOK (Flare label, Kling keeps it). | AURUM's logo held for 5 s in Kling. VESPER's label morphed only on a 90° orbit after 2.5 s. Soul and the video models misspell. | Flare puts the label into the still. Kling moves stay ≤60° and orbits ≤2.5 s. Composite the real label **only as a fallback**: after two G-take OCR fails, on Seedance shots, and always on the typeset end card. |
| C5 | **Orbit size** | creative-brain: "180° turntable"; 12 LOCK: none; NOTEBOOK: ≤60°. | F02 orbit failure. | ≤60°, ≤2.5 s. |
| C6 | **BIG IDEA model** | 12 §6 step 7 and 16 alt A: Seedance 2.5 r2v 720p ($2.77, or $13.86 for 15 s ×2). Router #1: Kling. | F02 sunset-into-bottle and F03 winter→summer: Kling 3.0 Pro + `last_image_url`, $0.48 each, "excellent". | Kling 3.0 Pro i2v (+`last_image_url`) is the default for every product shot, BIG IDEA included. Use Seedance 2.5 only for a multi-beat one-take Kling can't do, drafted at 480p. |
| C7 | **Previs / animatic** | creative-brain §7.5: still animatic before video. 12/16: Wan 3.0 previs. PROTOCOL H5: Hailuo. Router: Veo Lite. NOTEBOOK: still animatics confuse clients. | Live: Veo is not on the API. `hfgen` cannot price Wan, so a real batch refuses it (§2.2). | Build an **internal-only** timing animatic from stills in reel-studio ($0). No paid previs until hfgen parses Wan pricing. Never show a stills animatic to the client. |
| C8 | **Image models** | Router: Nano Banana Pro/Seedream for product insertion. 20 §3: GPT Image 2 leaves a repeating noise pattern in liquids and bubbles. creative-brain puts splash heroes on Flare. | Today's `/models` (85 slugs) has no NB Pro, Seedream or Veo. | Flare for product frames, Sunburst for edits, Qwen 3 edit for label fixes (see §2.1 flags), Soul Cinema for plates. Add a 100 % zoom "repeating noise" check on liquid stills. Mark the router's image table "web-only". |
| C9 | **Upscaling** | 17: Topaz, then mask the label back. 12/16: "upscale in post". | No upscaler on the API (confirmed). None installed locally. | No generative upscale in v1. Deliver Kling Pro natively. Seedance shots stay ≤720p and only on beats without labels, scaled with ffmpeg lanczos (label-safe). |
| C10 | **TTS model** | creative-brain §5.6 and `elevenlabs.py` default: `eleven_v3` (style 0.3–0.6). 13: v4 is recommended and ignores style/speed. | F03 used v4 (Jenna). `/v1/models` lists `eleven_v4` and a new `eleven_v4_turbo`. | Default to **v4**: true whispers, IPA, ≈0.13 vs 0.45 credits/char. Use v3 only when speed/style is needed. Change the script default and warn when style is sent to v4. |
| C11 | **VO length and pace** | creative-brain and 18 S7: ≤2.5 words/s. 13: 1.6–1.9 wps, 28–35 words per 20 s. 19: VO ≤10 words. 00: a short line at the end. | F02 and F03 each used one closing line. | Aesthetic-film default: **one VO line, ≤12 words, at the end**. A longer VO is capped at 1.6–1.9 wps. 2.5 wps is for comedy only. |
| C12 | **Music timing** | creative-brain §5.8 and 00 step 8: timestamped prompt. 13 and 00 hard rules: composition plan. | E05/c: timestamped prompts were ignored. The F03 plan landed every hit. | Always use a composition plan, with hits on chunk boundaries (chunks ≥3 s). Draft the plan free with `/v1/music/plan` (verified 0 credits). |
| C13 | **Dialogue / lip-sync** | creative-brain §7.6 and router #3: Seedance `audio_urls` lip-sync. NOTEBOOK, 00 and 19: no talking heads. | F01 sync drifted; the client said "really bad". | Excluded by default. `director.py dice` still draws `sonic=dialogue` and has no exclude flag; add one (gap G7). |
| C14 | **Punchline vs aesthetic** | creative-brain laws 1–4 (comedy twist) vs 00 (visual payoff). | Client taste (F01 pivot). | For aesthetic films the "twist" **is** the BIG IDEA, the literalised claim. It is scored with 15 rubric #3 ("the product is the resolution"). |
| C15 | **Pre-test scope and cost** | 15: 60 concepts, mixed-family jury, ~800 calls, SSR, $5.40 stills. 18 §4.10: dice + rank + subagents + $0.02 Soul plates. creative-brain §7.2: 5 role-played viewers. | §3: one model family, no embeddings. | §3 protocol. Pre-H1 stills: Soul plates ($0.004) + ≤3 Flare 1k-low hook frames ($0.12). |
| C16 | **Price assumptions** | Flare "$0.30" everywhere; Seedance 30 s: 12 $13.86 (720p) vs 20 R13 $40–60; Qwen $0.075. | Flare $0.30 is **hfgen's hard-coded fallback**; the API gives token rates only, input images billed, never reconciled. Qwen: $0.040 1k / $0.075 2k. | Budget from live `/estimate`; Flare $0.30 *provisional* until T1; multi-shot = summed durations; Seedance at API rates (20's is a web-plan price). |
| C17 | **Still QC threshold** | image-direction and 18: ≥8/10. 17: hard gates + /20 (heroes ≥16, inserts ≥14). | — | Use 17 (superset). |
| C18 | **Seam identity metric** | 16 R8: RGB SSIM ≥0.9. | Test: the identical frame with a small grade shift scored RGB SSIM **0.83** but luma SSIM **0.99**; after R4 correction it scored 0.92 (§2.4). | Test identity on **luma SSIM ≥0.95**. Measure grade separately (R4 YAVG/SATAVG deltas). |
| C19 | **Keyframe similarity** | 16 §2.1: start and end frames "as similar as possible". | F03 M3 went from a rainy winter window to a summer dusk, a very different light, with no cut. | Similarity is needed in **geometry and camera**, not light or state. Bridge keyframes share composition along the planned move. |
| C20 | **Start frame vs multi-refs** | 20 §3 P1: give Kling Omni the refs, not the still as a start frame. Ours: i2v from an approved still. | Client pre-approval (18 H2; PJ Ace: "i2v when the client must pre-approve"). | Keep i2v from approved stills. Omni r2v is a fallback only. |

---

## 2. Technical verification (free calls only)

### 2.1 Higgsfield endpoints the plan depends on
Auth went through the proxy (`HF_AUTH_VIA_PROXY=1`). `hfgen check` returned "credentials OK (probe 404)". `GET /models` lists 85 slugs. Schemas come from the public docs.

| Endpoint | Live `/estimate` (list USD) | Schema facts that matter |
|---|---|---|
| `marketing-studio/image/flare` (`image_urls`) | $0.30 at 2k-high, $0.12 at 1k-low. **Both are hfgen's fallback, not an API number.** The API returns token rates only, with image input at $8/1M. | `image_urls` ≤16. `aspect_ratio` defaults to **auto (square)**. `enhance_prompt` defaults to false. There is also a `moderation` field (auto/low). Unknown keys are rejected (`additionalProperties:false`). |
| `marketing-studio/image/sunburst` | Same as Flare | Same as Flare. |
| `higgsfield-ai/soul/cinema` | $0.004 at 720p; $0.022 for a batch of 4 at 1080p | **Not in the `/models` list**, but estimate and docs work. Watch for deprecation. The schema has no image-ref field, which confirms "ignores refs". Aspect defaults to 1:1. |
| `soul/v2/standard`, `soul/v2/image-to-image` | $0.004 each | — |
| `kling-video/v3.0/pro/image-to-video` | $0.476 with sound off; $0.714 with sound on **and by default** | `last_image_url` ✓. Duration 3–15 (99 → HTTP 400). `cfg_scale` 0–1. Multi-shot: ≤6 shots × 512 chars. **Unknown keys are accepted:** an estimate with `end_image_url` (the Seedance name) or `bogus_param` returned $0.476 with no error. |
| Kling multi-shot 3×3 s | $0.476 **(wrong)** | The docs say durations are summed for billing, so the real price is ≈$0.857. |
| `kling-video/omni/first-last-frame` | $0.476 | A new slug, missing from 12. Duration is **5 or 10 only**. 9:16 is allowed. |
| `bytedance/seedance-2.5/image-to-video` | 480p 5 s $1.03; 720p 5 s $2.31 | `end_image_url` ✓. **There is no `aspect_ratio` field** and unknown keys are rejected, so a template that adds one will 400. `generate_audio` defaults to true. |
| `bytedance/seedance-2.5/reference-to-video` | 480p 6 s $1.23; 720p 6 s $2.77; 1080p 4 s $4.55 | `image_urls` ≤30, `video_urls` ≤10, `audio_urls` ≤10. Aspect defaults to **16:9**, so always send 9:16. |
| `alibaba/qwen-image-3/edit` | $0.040 at 1k; $0.075 at 2k | `prompt_extend` and `enable_thinking` both **default to true**: LLM prompt rewriting, the same risk as `enhance_prompt`. Sending `prompt_extend:false` alone returns **HTTP 400** ("True was expected"); both false works. Defaults are 1:1 and 1k. `image_urls` ≤3. |
| `alibaba/wan-3.0/image-to-video` | No `usd`: the API returns text only ("480p $0.05…") | hfgen cannot parse it (§2.2). |
| `seedance-2.0/*`, `higgsfield/cinema-studio/4.0` | No `usd` (token formula) | Same problem. |
| Upscaler | **None** among the 85 slugs. `recraft`/`ideogram` are text-to-image. | — |
| Nano Banana Pro, Seedream, Veo | Absent | Confirms 12 §2. |

### 2.2 `hfgen.py` defects (none covered by the 30 passing tests)
1. **Dry-run under-reports:** unpriced jobs print "?" and add $0. Our plan showed "$4.05" with Qwen, Wan and Seedance 2.0 unpriced; a real run then exits on the first unpriceable job.
2. **No schema check before paying:** `/estimate` ignores unknown keys, so a typo (`end_image_url` on Kling) is silently dropped and the clip is billed without an end frame.
3. **Price parser** misses Wan's "480p $0.05" wording and token formulas, so Wan previs and Seedance 2.0 can't run via `batch`.
4. **Multi-shot under-estimated** (billing uses summed durations). 5. **Spend = estimate, not bill.**

### 2.3 ElevenLabs (`ELEVEN_AUTH_VIA_PROXY=1`)
- `check`: creator tier, active, 5,518 / 131,000 characters. `/v1/models`: `eleven_v4`, new `eleven_v4_turbo`, `eleven_v3`…
- Docs confirm 13 and the script: music `model_id` v1/v2/v2_5 (**default v1**), plans need v2/v2_5, `force_instrumental` prompt-only; SFX 0.5–30 s, `eleven_text_to_sound_v2`, influence default 0.3.
- `POST /v1/music/plan` (`music_v2_5`, 20 s) returned 3 chunks (3,000/14,000/3,000 ms) at **0 credits**: plans can be drafted and validated free.
- All **11 voice IDs** in 13 §2 resolve via `GET /v1/voices/{id}` (9 professional, 2 premade).
- Not free to check: TTS/SFX/compose quality. Script gaps: default v3; no seed, cache, `Song-Id` or character estimate.

### 2.4 ffmpeg recipes from 16 and the film chain (ffmpeg 6.1.1, synthetic testsrc2/mandelbrot clips)

| Recipe | Runs | Result |
|---|---|---|
| R1 last frame + blurdetect | ✓ | N=72; last-frame PNG; per-frame `lavfi.blur` printed |
| R2 dedupe join | ✓ | 143 frames, 5.958 s (one duplicate dropped) |
| R3 freezedetect | ✓ | `freeze_start: 1.958`, exactly as 16 reports |
| R4 measure + fading `eq` | ✓ | Seam YAVG 126 vs 138, SATAVG 114 vs 130. The `eval=frame` expression works. |
| R5 minterpolate heal | ✓, with a caveat | 4 frames removed, **3 synthesised**: the clip loses one frame (42 ms of audio drift per heal). Re-check sync after healing. |
| R6 whip (xfade + dblur) | ✓ | 5.75 s as expected |
| R7 exact setpts ramp | ✓ | Predicted 5.539 s, got 5.542 s |
| R8 SSIM/PSNR | ✓ | Unrelated frames 0.24, as in 16. Shared frame with a grade shift: RGB 0.83, luma 0.99 (→ C18). |
| `film_chain_warm.txt` via `-vf` | ✓ | Output 1080×1920, 24 fps, yuv420p, bt709-tagged. **Neutral grey stays neutral** (U 127.0 / V 127.2): no magenta cast, so the F03 fix holds, though it is barely "warm" on neutrals. Centre luma 126→121; **corners 126→67** (vignette −47 %). About 40 Mb/s at crf 18 because of the grain, so a delivery bitrate cap is mandatory. Speed: 14.5 s per 3 s of 1080×1920. |
| `director.py qc` on the chain output | ✓ | Verdict WARN, for loudness only (a sine test tone, as expected) |

### 2.5 Tests and CLIs
`pytest`: ad-director **30 passed**, reel-studio **116 passed** (2 min 54 s), lab **2 passed**. `--help` works for hfgen, elevenlabs, director, reelstudio and lab.py; **`blockout.py --help` crashes** (no argparse). reel-studio has `velocity`, `whip`, `zoom_through` and `in` trims, but no spec hook for `film_chain_warm.txt` (separate post pass) and `velocity` cannot ramp *across* two clips (R7 needs the joined file).

---

## 3. Can zero-cost pre-testing run inside Claude Code?

**What the routine actually has:** only Claude. Agent-tool subagents can use another Claude tier (Opus/Sonnet/Haiku): size diversity, not family. No OpenAI/Gemini/OpenRouter or Anthropic API key is in the environment, so scripts cannot call any LLM directly. Subagent spawn depth is 1 (only the main agent fans out); no temperature control; no embedding model (`sentence-transformers` missing; huggingface.co answers 307, so a local install is probably possible, unverified); numpy 1.26 present, no `choix`. A Figma Weave MCP (`weave_run_model`) might reach other families but needs OAuth and bills; not called.

**Consequences for 15:** the mixed-family jury (PoLL), "generator family never votes", the family-C rewriter and SSR embeddings are impossible as written, and ~480 tournament calls as full subagent turns are too slow.

**Workable substitute: a single-family, controls-first panel [inf]**
1. **Isolation instead of family mixing.** Generator subagents never see judge prompts. A separate normaliser subagent rewrites every card into one fixed template with random IDs (self-preference is driven by familiar style, so this keeps most of 15's protection). Two tiers (e.g. Sonnet and Haiku) judge; disagreements are reported.
2. **A smaller, batched tournament.** 12 post-gate concepts × 3 Swiss rounds = 18 matches. One judge subagent = one persona × one order, voting on all 6 matches of a round (free text first, then a choice): 6 personas × 2 orders × 3 rounds = **36 calls**. Order flips = ties. Bradley-Terry via a 30-line numpy MM fit + bootstrap CI, as a new `director.py tourney`.
3. **Controls become the validity test.** Every bracket holds a weak control, a shuffled control and two known anchors: F01 v1 comedy (rejected) and F03 SOL (accepted). A control in the top half, or inverted anchors, voids the ranking; the client then sees an unranked set.
4. **SSR substitute:** a judge maps each free-text answer to the closest of 5 anchor statements, quoting the phrase. Relative indices only. Add local embeddings if they install.
5. **Keep the cold-viewer comprehension test:** a fresh subagent sees only hook/turn/payoff descriptions or Soul plates. It is the cheapest strong signal.
6. **Honest labelling:** "ranked by one AI model family with controls; strategic strength only".
7. **Humans calibrate.** H1 choices, comments and later live metrics go to `director.py log`; re-weight the rubric after ~20 decisions (15 §3.3).

---

## 4. Riskiest assumptions and a minimal paid test plan (≤ $4, NOT run)

**Untestable for free:** (a) Kling honours "no settle" with `last_image_url`; (b) Kling *lands on* `last_image_url`, so shared-keyframe seams vanish; (c) a ≤30° arc between two keyframes causes no internal cut; (d) labels survive Flare-derived keyframes plus camera motion; (e) Qwen edit with enhancement off fixes only the label; (f) Flare's real billed cost; (g) Seedance 2.5 i2v start→end as a 480p one-take alternative.

**Inputs:** approved F03 assets `lab/experiments/F03_sol/frames/{SOL.png, S3A.png}` (no new refs). Run via `hfgen batch --budget 4`, sound off, after G1.

| # | Exact job | Model / args | Cost | Pass criterion |
|---|---|---|---|---|
| T1 | Derive K1 (camera 15° right and slightly higher) and K2 (30° right, 10 % closer) from S3A. Prompt: "same scene, light, lens and grade; only the camera position changes". | Flare 2k high, `image_urls:[S3A, SOL]`, 9:16, ×2 | ≈$0.60 | Human/VLM: "SOL" deboss and vessel identical; light direction unchanged; luma SSIM K0↔K1 on the product crop ≥0.85. **Reconcile:** account credits before and after vs the $0.60 estimate. If the difference is >10 %, update hfgen's Flare price. |
| T2 | A/B the settle wording on the same pair, K0→K1. **A** = 12 template D ("settles exactly on the end frame"); **B** = 16 §2.1 ("already moving… does not slow, pause or settle"). | Kling 3.0 Pro i2v, 5 s, `last_image_url`, `sound:"off"`, `cfg_scale` 0.5, ×2 | $0.95 | **B passes if:** R3 finds no freeze ≥0.25 s; mean absolute frame difference over the last 12 frames is ≥50 % of the frame 24–96 mean (A should fall well below that); `reelstudio cuts` finds no cut inside the clip. If B ≈ A, the wording does nothing: rely on trims and ramps, and remove the claim from 16. |
| T3 | Chain link K1→K2 with the winning wording; join with R2 to the T2-B clip. | Kling 3.0 Pro i2v, 5 s, `last_image_url`, sound off | $0.48 | Luma SSIM between clip 1's last frame and K1 ≥0.95 (does Kling land on the end frame?) and between clip 1's last frame and clip 2's first frame ≥0.95. A blind viewer (human plus a cold subagent on a 0.25× contact sheet) can't point to the seam. Label legible in every 6th frame. |
| T4 | Damage test: take the worst label frame from T2/T3, or blur the label of K2 in ffmpeg, then repair it. Prompt: "Change only the debossed word to 'SOL' … everything else identical". | Qwen 3 edit, 2k, 9:16, `prompt_extend:false`, `enable_thinking:false` | $0.075 | Word correct. Luma SSIM outside the label box ≥0.97 vs the input. |
| T5 | One-take alternative: K0→K2 in a single clip. | Seedance 2.5 i2v, 480p, 5 s, `end_image_url`, `generate_audio:false`, **no** `aspect_ratio` | $1.03 | Request accepted (schema check). No internal cut. Product shape identical. Compared blind with T2B+T3 on smoothness and fidelity; record which wins. |
| — | Reserve: one retake of whichever of T2/T3 failed for a non-wording reason (e.g. a morph) | Kling | $0.48 | — |
| | **Total** | | **$3.62** (≤$4) | |

Credit-only (no $): **E1** a 12-word v4 TTS line with `[softly]` (does `chars_to_words` strip v4 tags; do words match scribe?); **E2** render the free-drafted 20 s `music_v2_5` plan (silent head; boundary hit within ±50 ms).

**Decisions:** T2-B + T3 pass → 16's method B is the default. T2 fails → hide seams in post (R3/R5/R7, occlusion, match cuts) and drop shared-keyframe bridges. T5 wins → Seedance one-takes allowed for label-free beats only.

---

## 5. Gap list for the build (priority order)

| P | Gap | Source |
|---|---|---|
| G1 | **Fix hfgen money paths:** (a) the dry-run must fail, or flag "UNPRICED", when any job lacks a price; (b) a local schema linter built from `llms-full.txt` that rejects unknown keys before estimate or submit; (c) parse Wan's "480p $0.05" format and the token formulas (Seedance 2.0, Cinema Studio, Flare by pixels and refs); (d) multi-shot = summed duration; (e) inject safe defaults per model: `sound:"off"`, `generate_audio:false`, 9:16 where the field exists (not on Seedance i2v), `enhance_prompt:false`, Qwen `prompt_extend`/`enable_thinking` false. | §2.1–2.2 |
| G2 | `pipeline.py` + `job.json` + `spend.jsonl`, with job, stage and reserve caps; `hfgen --job` writes the ledger; billed-vs-estimate reconciliation. | 18 #1–2 |
| G3 | **Run the §4 paid tests** before writing any shot-plan template. Update 16, 12 and the router from the results. | §4 |
| G4 | Pre-test runner as `director.py tourney` (Swiss pairing, both orders, BT fit, bootstrap, controls, anchors), normaliser and persona prompt files, anchor-match SSR substitute. | §3 |
| G5 | G-still/G-take cheap QC (`director.py qc-take`): luma-SSIM seam check, freeze and tail-motion (settle) detector, first-vs-last product-crop drift, palette continuity. **Label OCR has no engine:** tesseract is not installed, so either add it to the setup script or use a QC-subagent read with a cited crop. | 18 §4.5, C18 |
| G6 | QC-judge and trademark subagent prompts plus evidence contact sheets (`reelstudio grid`). Maker ≠ checker. | 18 #4 |
| G7 | Taste-safe ideation: `dice --exclude sonic=dialogue,format=…` and a client taste profile that `dice` reads (today it draws dialogue, music-video and VHS looks). | C13 |
| G8 | `elevenlabs.py`: default to v4 (warn on style/speed); `--seed`; a `music-plan` command (free); `Song-Id` capture; a cache keyed by sha256; a character estimate before spending; SFX onset-trim and normalise. | C10, C12, 13 §8 |
| G9 | Grade integration: `film_chain` as a reel-studio post stage, with a `vignette` strength parameter (corners −47 % today) and a delivery bitrate cap (e.g. `-maxrate 8M` for a 1080p master, ~2.8 Mb/s web). | §2.4 |
| G10 | A cross-seam velocity ramp in reel-studio (velocity across two adjacent clips), so R7 is not a manual step. Healing (R5) must restore the frame count. | §2.4–2.5 |
| G11 | Client pages (private Artifacts) for H1 storylines and H2 stills; the choice is written to `approval.json`. | 18 #5 |
| G12 | Apply the §1 rulings to the docs (router "web-only", image-direction §0, creative-brain v4/60°/plans/wps, 15 costs; 12 gains Kling Omni, Qwen 1k price, Soul Cinema note). | §1 |
| G13 | Delivery packager (masters, cutdowns, hook variants, AI-disclosure note, licences). | 18 #6 |
| G14 | A Soul Cinema deprecation watch: the slug is missing from `/models`, so `hfgen check` should probe the estimate of every model the router uses. | §2.1 |
| G15 | Minor: give `blockout.py` argparse/`--help`; and the `fetch_yt.py` 429 back-off noted in 20 §5. | §2.5 |
