# T01 · Paid validation test (21 §4), 2026-10-08

**What this is:** the minimal paid test plan from `skills/ad-director/references/marketing/21-validation-audit.md` §4, run as written: T1–T5, E1, E2, and the optional reserve (not used).

**Inputs:** F03 `SOL.png` and `S3A.png` (= K0).

**Spend:** **$3.13 estimated / $3.51 cap-accounting** of the $4.00 hard cap. The Flare line is unverifiable, see §3. The full per-job table is in `ledger.md`.

**Files:** media is git-ignored and stays local in `clips/`, `frames/` and `out/`. Plans: `plan_T1…T5_*.json`. The metric scripts live in the session scratchpad (`paidtest/tools/`: `schema.py`, `lintplan.py`, `metrics.py`, `clipqc.py`, `lowmad.py`, `labelsheet.py`, `onset.py`, `scribe.py`).

**Every paid job was checked first** with a schema lint against `llms-full.txt` (unknown keys, enums, ranges), a free `/estimate` and `hfgen batch --dry-run`.
- All six plans linted clean.
- Settings: `sound:"off"` on every Kling job; `generate_audio:false` and no `aspect_ratio` on Seedance; `prompt_extend:false` + `enable_thinking:false` on Qwen; `enhance_prompt:false` on Flare.
- Kling used `last_image_url` and Seedance used `end_image_url`.
- No Seedance clip has an audio stream. Every job completed on its first take.

## 1. Results

| Test | Job | Cost (est.) | Verdict | Evidence |
|---|---|---|---|---|
| **T1** | Flare 2k high ×2: K1 (crane up / small arc), K2 (arc + ~10 % closer) from S3A + SOL | $0.60 (unverified) | **Visual PASS; metric FAIL** (the metric is miscalibrated) | **Visual:** the SOL deboss is legible and correct in K0, K1 and K2. The vessel shape and texture match. The light is unchanged (cold window from the right, warm small flame). The scene objects are kept; the linen re-drapes. **Metric:** luma SSIM K0↔K1 on the registered product crop = **0.466** (K2 0.472) vs ≥0.85. **Control:** K0 against itself shifted by 3 px = **0.447**, so full-resolution SSIM on a re-rendered textured surface cannot pass 0.85 even for a perfect re-photograph. At a 43 px crop width SSIM rises to 0.76 / 0.81. **Outputs:** 1520×2688. **Reconciliation:** impossible through the API (§3). |
| **T2** | Kling 3.0 Pro i2v K0→K1, 5 s, cfg 0.5, A = 12 template D "settles exactly on the end frame", B = 16 §2.1 "already moving… does not slow, pause or settle". The prompts are identical except the speed clause. | $0.952 | **B FAIL; A ≈ B, so the wording does nothing** | **Freeze ≥0.25 s:** none in A or B. **Cuts (`reelstudio cuts`):** none. **Tail ratio** (mean abs frame diff over the last 12 frames ÷ frames 24–96): **A 0.908, B 0.495** (B needs ≥0.50, and A was expected to be well below B; the result is the opposite). **Denoised check** (blur, 1/4 scale, flame masked): A 0.843, B 0.515; per-second motion B 0.32→0.09, A 0.28→0.13. Both land on K1: last frame vs K1 luma SSIM **A 0.911 / B 0.916**. The first frame vs its own input still is 0.928, the ceiling for this pipeline. B's prompt is 108 words, over the 90-word slot cap. |
| **T3** | Kling K1→K2 with the measured T2 winner's clause (A, "moves smoothly and settles exactly on the end frame"), joined to T2-B with R2 (dedupe) | $0.476 | **PARTIAL:** identity seam PASS, landing metric FAIL, velocity seam FAIL | **Clip 1 last frame vs K1:** **0.916** (needs ≥0.95; the i2v ceiling is 0.928, so it lands within 0.012 of the best possible). **Clip 1 last vs clip 2 first:** **0.972** PASS. **Blind seam:** the seam frame-pair difference is the *smallest of all 240 pairs* (0.24 vs a local median of 0.79), so there is no positional jump. But the speed jumps **~4×** across the seam (denoised diff 0.08→0.37), because T2-B decelerates and T3 accelerates. **T3 alone:** tail ratio 0.974 (denoised 1.64): the "settle" wording produced *acceleration* into the end frame. **Label:** "SOL" legible in **41/41** tiles (every 6th frame, registered crops, `out/T2B_T3_labels.jpg`). No cuts, no freeze. The cold-subagent blind view was **not run**: this agent has no subagent tool (21 §3: spawn depth 1). Use the preview. |
| **T4** | Blur K2's deboss in ffmpeg (box 140×56 at 970,1690), then Qwen 3 edit 2k 9:16, both rewrite flags false | $0.075 | **Word PASS; preservation FAIL** | **Word:** reads "SOL" in thin serif capitals, correctly placed. It looks slightly more printed than debossed. **Luma SSIM outside the label box:** **0.678** (needs ≥0.97); 0.70 / 0.80 / 0.92 at 1/2, 1/4 and 1/8 scale. **Control:** K2 vs itself shifted 1 px = 0.877. Qwen re-renders the whole frame: throwing rings softened, output 1152×2048 from a 1520×2688 input. The request with both flags false was accepted. |
| **T5** | Seedance 2.5 i2v 480p 5 s, K0→K2 one-take | $1.023 (token-exact) | **PASS** (schema, cuts, shape); **wins on flow**, loses on label fidelity | **Request:** accepted with `end_image_url`, `generate_audio:false` and no `aspect_ratio`; output 480×850, 24 fps, no audio. **Cuts:** none. **Freeze:** none. **Speed:** constant or slightly accelerating (tail ratio 1.32; denoised per second 0.37/0.32/0.32/0.35/0.38) with **no settle**. **Product:** shape identical in frames 0/60/120. **Label:** "SOL" readable but soft at 480p (`out/T5_labels.jpg`). **Comparison** with T2-B+T3 (not blind, see the preview): **T5 is smoother** (one continuous move, no speed break); **Kling is sharper**, with a crisp label at 1080p. |
| Reserve | One Kling retake | $0 | **Not used** | Neither T2 nor T3 failed for a non-wording reason (no morph or drift). Their failures are about wording/velocity and the metric ceiling, which a retake of the same request cannot fix. The cap-accounting total with the reserve would be $3.98: inside the cap, but only by $0.02 on an unverified Flare price. |
| **E1** | v4 TTS, Jenna, `[softly] Light it once, and the long winter remembers what summer felt like.` | 11 credits | **PASS** | `chars_to_words` strips the v4 tag: 12/12 words. `scribe_v2` returns the same 12 words. Word-start deltas: mean 0.04 s, max 0.12 s ("winter"). Duration 4.72 s (2.5 wps). |
| **E2** | `/v1/music/plan` (free) → 2 chunks (3,000 + 17,000 ms), rendered with `music_v2_5` | 275 credits | **Silent head PASS; boundary hit FAIL** | **Head:** 0–3 s RMS −55.7 dBFS (peak −48.4) vs −23.4 dBFS after. **First onset** (spectral flux and the RMS +20 dB crossing): **4.022 s**, i.e. **+1.02 s late** vs the 3.000 s boundary (needs ±50 ms). The piano "hit on the downbeat" was written into the *styles* of chunk 2, not as its own cue chunk. |

## 2. Decisions (21 §4 decision rules)

1. **"T2-B + T3 pass → 16's method B is the default":** **not met.**
2. **"T2 fails → hide seams in post (R3/R5/R7, occlusion, match cuts) and drop shared-keyframe bridges":** **triggered.** The settle/no-settle wording does not control Kling's speed profile (n=1 each).
   - B decelerated more than A.
   - T3's "settle" accelerated.
   - The rule's own sub-clause applies: "rely on trims and ramps, and remove the claim from 16".
   - **Caveat from the evidence:** shared keyframes *did* give a pixel-continuous seam (SSIM 0.972, the smallest frame difference in the clip) and kept the label. What breaks is **velocity**, which post can repair (R3 trim + R7 ramp).
   - Recommendation: keep shared keyframes only as an identity anchor in post-heavy seams, never as a "free seamless bridge", and always budget an R7 ramp per seam.
3. **"T5 wins → Seedance one-takes allowed for label-free beats only":** **adopted.** T5 wins on smoothness; at 480p the label is soft. Seedance one-takes are approved for beats where the label is not the subject. Kling stays the default for label shots.
4. **T4:** Qwen 3 edit is **not a local edit**. Use its output only as a **patch source**: composite the label box back into the original with a feathered mask (ffmpeg overlay, free). That makes everything outside the box identical by construction. The T4 criterion then reduces to "the word is correct", which passes.
5. **E2:** put a hard hit on a chunk boundary only as **its own short chunk** whose text is the cue (13's verified pattern). Plan-drafted styles alone landed 1 s late. Keep doubling hits with an SFX in the edit (13).

## 3. Flare price reconciliation

**Result: not reconcilable through the API.**
- No balance endpoint exists: every guessed path returns 405, and the docs list none.
- The completed `status` payload has no cost field.
- Flare's `/estimate` returns only token rates: image out $30/1M, image in $8/1M, text in $5/1M. "The initial charge is an estimate reconciled on completion."
- hfgen's **$0.30 is still a guess**.
- An upper-bound guess of $0.49 per 2k-high image [inf] was used for cap accounting.

**Action:** read the charges for requests `8a953000-…` and `5000b6b0-…` in the Higgsfield console. Until then:
- keep $0.30 marked *provisional* in 12/16/21;
- budget Flare at **$0.50** per 2k-high image in caps.

**Other price facts confirmed:**
- **Kling** `/estimate` `usd` is *after* a 15 % account discount: 7.616 credits = $0.476, list $0.56, 16 credits = $1.
- **Seedance** 480p 9:16 bills on the real output size, 480×850: $1.023 for 5 s.
- **Qwen** 2k: $0.075.

## 4. Recommended doc updates

**12-higgsfield-mastery.md**
- §1 Flare row: "≈$0.30" is hfgen's fallback, not an API figure; no balance or cost API exists; budget $0.50 until console-reconciled. A Flare re-frame from one still plus the product ref keeps the deboss and light (T1); output is 1520×2688 at 2k 9:16.
- §1 Kling row: `/estimate` usd already includes the account discount (list $0.56).
- §1 Qwen edit row: 2k 9:16 returns 1152×2048 and **re-renders the whole frame** (SSIM 0.68 outside the edit box). Use it as a patch source and composite back.
- §1 Seedance i2v: 480p 9:16 = 480×850, $1.023 per 5 s (token formula verified to the cent).
- §4 template D: "settles exactly on the end frame" does **not** control the speed profile (T2-A ended faster than T2-B; T3 accelerated into the end). Keep D for packshots only, and land them with a cut to the still or an R3 trim, not with the wording.

**16-seamless-flow.md**
- §2.1: delete the claim that "already moving… does not slow, pause or settle" prevents the settle. T2-B decelerated (tail ratio 0.50) more than the settle wording did (0.91). Replace it with: the speed profile is uncontrolled; measure it per take and fix it in post (R3 trims, R7 ramp centred on the seam).
- §2.5: add the symptom **"speed break at a shared-keyframe seam"** (T2-B→T3: ~4× speed jump with zero positional jump). Fix with an R7 ramp, or by picking takes with matching tail and head speeds.
- §2.1 bullet "keep the frames similar": with very close keyframes (K0→K1), most of the camera move happened in the first ~3 s (denoised motion fell from 0.32 to 0.09 per frame by second 5). Size the keyframe delta to the clip length.
- R8: use **luma** SSIM. For landing, compare `last vs end keyframe` with `first vs start keyframe` of the same clip; the i2v ceiling at 1080p vs a 2k still is ≈0.93, so a fixed 0.95 cannot pass. Clip-to-clip seams can keep ≥0.95 (measured 0.972).
- §2.2: Seedance one-takes are approved for label-free beats (T5: no cut, constant speed, shape held; label soft at 480p).

**21-validation-audit.md**
- §4 T1/T3/T4 thresholds are miscalibrated for generated imagery: full-resolution SSIM of a re-rendered textured surface is ≈0.45 even for a 3 px self-shift. Replace them with:
  - T1: a registered-crop NCC ≥0.85 plus a VLM read of the label;
  - T3: relative landing (≥ first-frame ceiling − 0.02);
  - T4: "outside-box identical after mask composite".
- Settle detection: plain frame-difference ratios are contaminated by grain, rain and flame flicker. Use the denoised, flame-masked version (`lowmad.py`).
- C2: answered. Kling ignores settle/no-settle wording with `last_image_url` (n=1); decide by role in post.
- C16 / G2: there is no billed-cost API. `spend.jsonl` needs a manual or console reconciliation step, and the Flare rate stays provisional.
- G1 note: the run used the pre-G1 hfgen. The free schema lint (`lintplan.py` against `llms-full.txt`) is the missing G1(b) piece and should move into hfgen.
- §3: the cold-subagent blind seam test cannot run from inside a subagent. Run it from the main agent.
- E2 result: plan-drafted hits drift (+1.02 s). Verified pattern: a dedicated cue chunk at the boundary.

## 5. Preview
A side-by-side MP4 (15 s) sits in the session scratchpad: `paidtest/T01_paidtest_preview.mp4`.
- **0–5 s:** T2-A vs T2-B.
- **5–15 s:** T2-B+T3 (seam at 5.0 s in that clip) vs T5, which holds its last frame after 5 s.
