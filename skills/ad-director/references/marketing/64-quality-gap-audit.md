# 64 · Quality-gap audit: our films against what actually sells

Date: 2026-10-09. Zero generation spend. Nothing was generated, uploaded or sent.

**Scope.** All 19 films in the session scratchpad `films/` folder (media is never committed). Each one was checked with ffmpeg: format, the real detail behind the 1080p label, hard cuts, freezedetect, and EBU R128 loudness and true peak. Each also got a 2 fps strip and a first-3-seconds tile, which I looked at frame by frame. The eight newest finals also went through `qc_report.py`. The bar comes from docs 41–46 and the measured winners in 53–62.

**The question:** what does a paying US DTC founder notice in the first 3 seconds, and does it make them say no?

---

## 0. Verdict

The films are good at the thing the owner likes: cinematic action, a deadpan twist, our recurring cast. They are weak at what a founder pays for: **their product, readable, early, big, and correct**. Our own rule #1 in doc 45 says "Frame 1 = the product, legible, ≥30 % of the frame". Only 5 of 19 films meet it. The three newest action films (Heist, Dive, Red Light) meet it least.

- In **Red Light**, the film the owner called "the bar", the product first appears at **19.5 s**. It fills about 4 % of the frame, and the label is illegible blobs.
- **All 8 newest finals FAIL `qc_report`.**
- **No 1080p film has 1080p detail.** They are 480p takes resized with plain lanczos (measured below).

A founder judges in 3 seconds. Today those seconds show our characters, not their product.

---

## 1. Measured audit, all 19 films

"Detail" is the SSIM between the delivered frame and the same frame squeezed to 480 px wide and scaled back. **≥ 0.99 means there is no detail above 480p.** Product = legible product in frame by 2.0 s. Text = a message-bearing super by 1.0 s. TP = true peak. Freeze = freezedetect spans of 0.25 s or more.

| Film | Delivered | Detail | LUFS / TP | Cuts | Product ≤2 s | Text ≤1 s | Freezes |
|---|---|---|---|---|---|---|---|
| aurum_30s | 480×850 | native | −15.0 / −2.0 ✔ | 1 | ✔ label fills frame | ✘ | 26.6–29.8 s (5 spans) |
| aurum_heist_14s | 720×1280 | native 720 | −14.2 / **−0.7 ✘** | 1 (morph one-take) | ✘ (7 s) | ✘ | — |
| **aurum_red_light_30s** | 1080×1920 | **0.994 → 480p** | −14.7 / −1.5 ✔ | 9 | ✘ (19.5 s, ~4 %, label illegible) | ✘ | **15.67–18.50 s, 69 fr FAIL** |
| aurum_topshelf_30s | 1080×1920 | ≈480p | −16.2 / **−0.6 ✘** | 0 | ✘ can <5 % | ✘ | 14.4, 20.1–21.0 s |
| aurum_topshelf_30s_v2 | 1080×1920 | ≈480p | −16.2 / **−0.6 ✘** | 0 | ✘ | ✘ | 20.1 s (1.0 s) |
| aurum_v3 | 1080×1920 | 0.990 | −16.6 / **−0.5 ✘** | 0 | ✘ can <5 % | ✘ | 13.5–15.3 s, 25.0–26.0 s **FAIL**; white hold 21.8–22.3 s |
| dive_from_the_top_14s | 720×1280 | native 720 | −14.6 / **−0.9 ✘** | 1 | ✘ product never shown as a can | ✘ | **0.21–0.79 s (static open)** |
| otto_30s | 480×850 | native | **−20.4** / −3.4 | 0 | ✘ | ✘ | — |
| otto_tabletop_30s | 1080×1920 | ≈480p | −13.6 / **+0.1 ✘ clips** | 0 | ✔ can centred, legible | ✘ | 19.4 s |
| red_light_test480 | 480×854 | native | −23.2 / −6.0 (take) | 9 | ✘ | ✘ | 15.7–18.5 s |
| reel_01_otto_vee | 480×854 | native, mono | −17.5 / −1.2 | 0 | ✘ candle small | ✔ caption | 25–28 s (6 spans) |
| reel_02_cafe | 480×854 | native, mono | −17.7 / **−0.5 ✘** | 0 | ✘ | ✔ caption | 23.6–29.7 s (6 spans) |
| sol_30s | 480×850 | native | **−22.8** / −4.9 | 0 | ~ candle 8 %, static | ✘ | 12.3–13.3 s |
| tabletop_v2 | 1080×1920 | 0.992 | −13.6 / **−0.5 ✘** | 0 | ✔ | ✘ | 19.4–20.0 s |
| test_native_sound_hook | 480×850 | native | −25.4 / −2.6 (test) | 0 | ✔ **can opening at frame 0** | ✘ | — |
| vesper_23min_30s | 1080×1920 | ≈480p | −15.9 / **−0.9 ✘** | 0 | ✘ bottle at side, label soft | ✘ (2.5 s) | — |
| vesper_30s | 480×850 | native | −17.1 / −1.3 | 1 | ✔ bottle hero | ✘ | 17–29 s (7 spans) |
| vesper_keep_the_light_30s | 1080×1920 | ≈480p | −15.8 / **−0.5 ✘** | 0 | ✘ | ✘ (2.5 s) | 5.1–6.7 s |
| vesper_v3 | 1080×1920 | 0.987 | −16.3 / **+1.7 ✘ clips** | 0 | ✘ | ✘ (2.5 s) | 5.1–6.7 s |

**Totals:**
- Product legible by 2 s: **5 / 19 (26 %)**. Benchmarks: our long runners 83 % (doc 45 D43); grooming paid winners 12/23 at frame 0 (doc 53); NA drinks paid winners always (doc 57 N14).
- Text by 1 s: **2 / 19**. Benchmarks: 89 % (D43); ~16/23 (doc 53); 35/55 in apps (doc 62).
- Both loudness gates (−14 ±1 LUFS and ≤ −1 dBTP): **2 / 19** (aurum_30s, red_light). Two finals clip above 0 dBTP (vesper_v3 +1.7, otto_tabletop +0.1).
- Freezes of 0.25 s or more: **14 / 19**.
- No 6–15 s cut-down and no 4:5 version exists for any film. Paid winners in drinks, beauty and food run 6–15 s (docs 45, 57).

`qc_report.py` on the 8 newest finals: **8 / 8 FAIL**. Red Light fails on a 2.9 s frozen hold, plus 40 single repeated frames (judder). Heist, Dive, aurum_v3, tabletop_v2, keep_the_light and vesper_v3 fail on true peak, and aurum_v3 also on freezes. Every one also has a WARN on onset alignment: 4–12 onsets per film more than 4 frames off. These must be confirmed on `onset_zoom.jpg`.

---

## 2. What a founder notices in the first 3 seconds (ranked)

1. **"Where is my product?"** (14 / 19). We open on Otto's moustache, Vee's glasses, a taxi or a skyline. Doc 45 rule 1 and rule 6 ("never an AI human face as the lead") are both broken by our own best films. A spec film for a founder is judged as "what would mine look like"; showing our mascots first says "this is about the studio".
2. **"That's not my label."** The label holds only when the product is a large static hero (tabletop, aurum_30s, vesper_30s). It breaks as soon as the product is small or moving:
   - Red Light: illegible blobs.
   - tabletop_v2 at 16 s: "SPARKLING YUZU" becomes **"SPARKFOL IUIN"**.
   - Dive: the product is served as an amber drink on ice in a tumbler. It reads as whiskey (an alcohol cue, Meta rule, doc 57) and the can never appears.

   Founders check the label first. Cuisinart rejected AI ads over a wrong green (doc 56).
3. **"It's soft."** Every 1080×1920 delivery is 480p detail in a 1080 container. The Red Light frame is pixel-identical in character to a plain lanczos resize of the 480p test. On a phone, the can and every face are waxy and posterised. Higgsfield's own showcase reels are native 1080p (doc 42 #1), and founders compare against those.
4. **"Nothing is happening."** Several films open on a static or held pose:
   - Dive: frozen 0.2–0.8 s.
   - All vesper films: a woman sitting.
   - topshelf and aurum_v3: a man standing far away.
   - otto_30s, sol.

   Doc 42: "Frame 0 is never static in the hits." The one film that does it right is the cheapest test we made: **test_native_sound_hook**. The can is opening at frame 0, with the hiss, label legible and big. That is the template.
5. **"I can't read it" / "it's under the UI."** Supers are thin italic serif, white with a light shadow, often over bright sky or a cream jacket. Their baseline sits at y ≈ 1,450–1,600 of 1,920. TikTok's bottom ~660 px and Reels' ~672 px are covered by caption and username UI (safe-zone checker, 2026-09). Red Light's only line, "Some things are worth stopping for.", sits at y ≈ 1,550: under the caption on both apps.
6. **AI tells a founder (or their customer) spots instantly:**
   - Garbled background text ("DUICE" on the police door, unreadable street signs).
   - Rain that freezes during the 2.9 s red-light hold.
   - The same golden-hour skyline in 15/19 films, and the same two generated faces in 17/19. Across a portfolio this reads as "one prompt, re-skinned".
   - A 1 s blown-white flash (aurum_v3, 21.8–22.3 s).
7. **"Too long, no offer."** Every film is 14 or 30 s. None has an offer end card or a CTA. Red Light ends on the wordmark with no can in the packshot. Paid DTC needs "show the product twice, swappable offer card" (doc 45 rule 3).
8. **Sound.** 11 / 19 exceed −1 dBTP or miss −14 ±1 LUFS. A founder won't measure it, but a clipped hiss on an iPhone speaker sounds cheap. We also list mastered sound as a selling point in DMs (doc 63), so every delivered file must pass.

What is *not* a gap: Red Light's cutting (9 cuts, longest shot 6.2 s, first cut 3.75 s) matches the doc 42 hits. Hands are mostly clean: Vesper's spray grip and the Aurum pour are acceptable at 1080 crops. The disclosure super is present on every film.

---

## 3. Fixes researched (zero research spend; prices are for the owner's decision, nothing was called)

### 3.1 Upscaling 480p/720p → 1080p

**What we do now:** a plain resize. It is free and adds zero detail (SSIM 0.994 against 480p).

| Option | Type | Price for 30 s at 1080×1920 | Notes |
|---|---|---|---|
| ByteDance Video Upscaler (fal), `aigc` preset | generative, AI-footage preset | **$0.0072/s → ≈ $0.22** (Pro 10× ≈ $2.16) | Cheapest. Has a preset built for AI-generated sources |
| SeedVR2 (fal; open weights) | one-step diffusion, temporal | **$0.001/MP → ≈ $1.49** | Recommended for AI clips. Strongest on detail; light flicker reported on very poor input. Free locally on a ≥24 GB GPU |
| FlashVSR (fal) | streaming VSR, temporal | $0.0005/MP → ≈ $0.75 | More conservative. Handles small text a little better than SeedVR2 (vendor blog) |
| Topaz Proteus (fal) | non-generative | $0.20/10 s → ≈ $0.60 | Won't invent detail. Safe for labels, but less gain |
| Topaz Starlight Precise 2.6 / Fast 2 | diffusion realism pass | $1.20 / $0.60 per 10 s → **$3.60 / $1.80** | One production rated it best on faces and fabric. Heavy compute |
| FLUX 3 Video Upscaler (precise) | generative | $0.14/s → $4.20 | Input ≤ 20 s, so split the film |
| Topaz Astra 2 | creative, invents detail | $3.00/10 s → $9.00 | **Avoid on labels.** Invention is the point of this model |
| Re-render the hero shots at native 1080p | — | ≈ 2.4× the 720p price (doc 43 §6) | A different take (no seeds). Only for product shots |

Hard truths:
- **No upscaler can recover a label that is 5 px tall at 480p.** A generative upscaler will *invent* letters (round3 X1 §upscale). A conservative one leaves the blob.
- Label fidelity therefore has to be solved *before* the upscale, by the shot design (§3.2), never by the upscaler.
- Every upscaled film gets the label re-checked afterwards.
- The fal prices come from a vendor blog (2026-08-23) and the Upsampler comparison (2026-04-20), not independent benchmarks. Before adopting one, run a ≤ $2 A/B on the same 10 s slice of the Red Light 480p take (ByteDance `aigc`, SeedVR2, Proteus) and compare 100 % crops of the face, the can and the police door. **This needs owner approval.**

Recommended default (pending that test): Seedance at 720p for the final; SeedVR2 (or ByteDance `aigc` if it holds up) to 1080p; product inserts native from Kling. A 480p take that "is the one" (LESSONS) can still be kept, but its product shots must be replaced by native inserts or composites.

### 3.2 Product-label fidelity

In order of reliability:

1. **A real photo is the only source of the label.** Get the client's flat, front-lit, uncropped packshot (≥ 2,000 px). Make the hero still with Flare `@Image` and check it letter by letter.
2. **Kling 3.0 Pro i2v product inserts** (doc 43 §2):
   - start frame = the checked still, `last_image_url` = the same still or the end pose;
   - 5 s, `sound:"off"`, `cfg_scale` 0.5;
   - **one move**: a slow push-in or ≤ 30° of rotation;
   - the label faces the lens for the whole shot, and no hand or liquid passes over it.
3. **The product is big when it is on screen:** ≥ 30 % of frame height in the hero and packshot shots. In wide action shots the product is a *silhouette or colour* and must never be the frame where the label is read. If the story needs the label in a wide shot, cut to an insert.
4. **Post composite as the fallback.** Track the real label artwork onto the generated can or bottle with a planar track (Blender's free Movie Clip plane track, or Resolve/Fusion; check that your edition has the planar tracker). This gives exact text whatever the model does. Use it for any shot where the model's label differs from the photo.
5. **Forbid all other readable text** in every video prompt: "no readable text, signage, plates or logos except the product label from @Image1". It removes the "DUICE" tells and the rival-trademark risk.
6. **Product state lock:** the drink is shown *in its own can or in a clear glass with the brand's real liquid colour*. Never an amber liquid on ice in a tumbler (it reads as alcohol). This is the LESSONS "one vessel" rule plus doc 57.

### 3.3 Hands and product interaction

- Vendor tests claim Seedance 2 renders correct hands in ~85 % of takes against ~70 % for Kling (Alici, self-run, unverified). So plan for ~1 in 5 takes having a hand fault, and check at 6–10 fps.
- Name the grip, not "holds": "right thumb on the front edge, four fingers wrapped behind the can, label facing the lens".
- One action per shot.
- The hand enters *already holding* the product. Avoid pick-ups, rotations above 30° and fast wrist turns, which is where fingers fuse.
- Close-ups of hands go through Kling i2v from a still in which the hand is already correct (5 fingers counted on the still).
- Short i2v prompts work better: ≤ 80 words, one action (Alici guide).
- QC: count the fingers on every frame where a hand touches the product (6–10 fps strip). Check that the grip doesn't change between cuts and that the product doesn't pass through a finger.

### 3.4 First 3 seconds

The test_native_sound_hook template:
- **Frame 0:** the product in motion and causing a sound (opening, pouring, spraying, snapping). It fills ≥ 30 %, label legible.
- **By 1.0 s:** a 3–7 word super in the safe zone.
- **By 3 s:** the world and the story begin.

The cinematic action can still be the body of the film. Red Light's taxi burnout can follow a 1.5 s cold open of the can being handed through the window, which is a flash-forward to the punchline (doc 44 plant/payoff).

### 3.5 Text legibility

- Keep supers inside **y 240–1,260 and x 120–840** of 1,080×1,920. That is the strictest TikTok/Reels envelope, including the right action rail.
- Font ≥ 60 px (48–55 px is the floor quoted in 2026 guides).
- Sans or heavy serif, not thin italics.
- A 3–4 px dark stroke or a 40 % scrim behind the text, contrast ≥ 4.5 : 1.
- ≤ 7 words per super, on screen for at least (words ÷ 3) + 1 s.
- Check by overlaying a safe-zone mask on the frames before export (§4 one-liner).

### 3.6 Sound

The doc 46 rule is unchanged. The evidence shows it isn't being applied to finals, so it becomes a hard gate in Step 7 (see the SKILL rules).

---

## 4. Pre-delivery checklist (all must pass before the owner sees a film)

Run the commands, read the numbers, look at the sheets. One FAIL means no delivery; fix it or disclose it.

**A. The founder's 3-second test** (sheet of frames 0, 0.5, 1, 1.5, 2, 3 s)
- [ ] Frame 0 has motion (no freeze in 0–1 s) and the product is in frame.
- [ ] The product is legible and ≥ 30 % of frame height by 2.0 s.
- [ ] A message-bearing super is on screen by 1.0 s, inside the safe zone.
- [ ] A diegetic sound transient falls in 0–0.5 s.

**B. Product truth** (every shot where the product is visible)
- [ ] The label matches the client photo letter by letter (100 % crop at the start, at every cut and at the end).
- [ ] Colour ΔE ≤ 3 against the swatch.
- [ ] One vessel, and the liquid has the correct colour. There are no alcohol cues unless the brand is alcohol (doc 57).
- [ ] No other readable text in frame, or it is real and cleared.

**C. Hands** (6–10 fps around every touch)
- [ ] 5 fingers, no fusion, the grip is the same across cuts, and the product never passes through a hand.

**D. Picture**
- [ ] Detail check: `ssim` against a 480-wide round trip is < 0.985 for a "1080p" delivery, or a true upscale (§3.1) was used and the label was re-checked after it.
- [ ] `qc_report.py --stage deliverable` has no FAIL. Frozen spans ≤ 6 frames unless they are a deliberate freeze-frame with sound over them. No unintended white or black hold.
- [ ] AI tells: no frozen weather, no garbled signage, no faces lingering in a 1080 close-up with a waxy look.

**E. Sound**
- [ ] The encoded file measures −14 ±1 LUFS and **≤ −1.0 dBTP**.
- [ ] Every hard hit is within 2 frames of its action (onset zoom).

**F. Selling package**
- [ ] The product is shown at least twice, and the end card has a packshot (the product, not only the wordmark) and a swappable offer or CTA.
- [ ] 9:16 plus 4:5, plus a 6–15 s cut-down, when the tier includes them.
- [ ] A disclosure super is present.

One-liners:
```bash
F=final.mp4
# A: first-3-seconds sheet with the safe-zone box (y 240-1260, x 120-840 at 1080x1920)
ffmpeg -v error -i $F -vf "select='eq(n,0)+eq(n,12)+eq(n,24)+eq(n,36)+eq(n,48)+eq(n,72)',drawbox=x=120:y=240:w=720:h=1020:color=red@0.8:t=6,scale=270:-2,tile=6x1" -vsync 0 -frames:v 1 first3s.jpg
# D: real detail (>= 0.99 means 480p detail)
ffmpeg -t 6 -i $F -filter_complex "[0:v]split[a][b];[b]scale=480:-2:flags=area[c];[c][a]scale2ref=flags=bicubic[c2][a2];[a2][c2]ssim" -f null - 2>&1 | grep -o "All:[0-9.]*"
# E: loudness and true peak of the encoded file
ffmpeg -nostats -i $F -af ebur128=peak=true -f null - 2>&1 | grep -A20 Summary | grep -E "I:|Peak:"
# D: freezes
ffmpeg -i $F -vf freezedetect=n=0.003:d=0.25 -map 0:v -f null - 2>&1 | grep freeze_
```

---

## 5. What this means for the funnel

Nothing changes in the direction or the funnel. The fix is inside stages 4–8:
- **Free 5 frames:** frame 1 of 5 is always "the product, legible, ≥ 30 %, already moving" from the lead's real photo. The founder sees their own label first.
- **Concept:** our cast and the action are the body of the film, never the first second.
- **Film:** product inserts are native Kling i2v from the real photo (or a composite). Then a true upscale, then the §4 checklist.

---

## Sources

- fal, "10 Best Video-to-Video Upscalers in 2026" (2026-08-23): https://fal.ai/learn/tools/video-to-video-upscalers
- Upsampler, "SeedVR2 vs FlashVSR" (2026-04-20): https://upsampler.com/blog/seedvr-vs-flashvsr-ai-video-super-resolution-2026
- ComfyUI video-upscale tutorial: https://docs.comfy.org/tutorials/utility/video-upscale
- Topaz Starlight on AI video (invideo): https://invideo.io/faq/what-is-topaz-starlight-25-and-why-is-it-used-for-ai/
- Safe-zone checker, TikTok/Reels/Shorts px margins (2026-09-23): https://www.upload-post.com/tools/safe-zone-checker/
- Caption size 2026: https://blitzcutai.com/blog/best-caption-size-tiktok-2026
- Seedance hand tests and the short-prompt guide (vendor, unverified): https://alici.ai/blog/seedance-2-is-here ; https://alici.ai/blog/how-to-use-seedance-2-guide-2026
- Kling 3.0 start/end-frame and text-preservation claims (vendor): https://docs.pletor.ai/ai-model-library/video-models/kling-3.0 ; https://www.cliprise.app/learn/guides/model-guides/kling-3-0-tutorial-2026
- Internal: docs 42 §hooks, 43 §2/§6, 45 §3 rules 1/3/6, 46, 53 §2, 56, 57 N14, 62; round3 X1 (upscale invents letters); LESSONS.md.
