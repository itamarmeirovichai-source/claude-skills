---
name: vxo-film
description: VXO funnel stage 4–9. Turns a client's brand + product name + product photo into a finished, QC'd ad of up to 30 s that sells (hook, punchline, synced sound, lip-sync when a character speaks). Also used for the free "5 concept frames" stage. Use whenever the owner brings a business/product/photo or asks for a client film, frames, storyboard, or ad.
---

# VXO film: brand + product + photo → finished ad

**Read first, every time:**
- `research/ai-video-reels/lab/LESSONS.md`: the owner's corrections. Breaking one is a failure.
- `skills/ad-director/references/marketing/41`–`46`:
  - realism (41);
  - viral teardowns (42);
  - model mastery (43);
  - action and comedy craft (44);
  - what sells (45);
  - sound and QC (46).
- The niche doc for the product's category, `47`–`52`, if one exists.
- The latest daily notes: `research/ai-video-reels/daily/` (newest file).

**Money rule:** show the cost and get the owner's approval before every paid step.

The ladder:
1. Storyboard stills (≈$0.04–1.50).
2. 480p test (Seedance 30 s ≈ $6.17).
3. Final (720p 30 s ≈ $13.87), OR keep the approved 480p take and upscale it.

Log every spend in `research/ai-video-reels/lab/experiments/W01_site_films/ledger.md`.

## Step 0: Client research after approval/payment (owner rule, 2026-10-09)
Before any concept, extend the lead's dossier (`research/ai-video-reels/leads/dossiers/<brand>.md`) into a client brief. Check that everything is in order:
- the business is real and active;
- the product, claims and labels are what we think;
- there are no legal or claims landmines.

Then understand the business and the person in depth:
- the product page, reviews (what customers love and complain about, in their own words), competitors' ads;
- their past ads and which ones they kept running;
- brand voice, colours and fonts;
- the founder's taste from their posts;
- what success means to THEM (sales, launch buzz, retail pitch).

End with:
- what they need from this film;
- what would make them come back (next film, Season plan, seasonal calendar, new SKUs);
- how we'll show results (deliverables, cut-downs, a test plan) so they buy again.

## Step 1: Intake (from the owner)
Collect:
- the brand, product name, product photo(s) and product page URL;
- the price;
- who buys it;
- what the brand already runs (Meta Ad Library);
- the placement (Reels/TikTok/site) and the tier.

Fill in `skills/ad-director/scripts/qc/preflight.md` as you go.

## Step 2: Think like the best creative director, copywriter and media buyer at once
Answer in writing:
1. **The one selling truth:** why this product, why now. Use the product plus a reason (Meta/Toluna: 5.3× purchase intent, doc 45).
2. **The hook in second 1:** motion already happening, sound-first, or an offer/newness hook. Pick from doc 38 and doc 42.
3. **The turn and punchline, CAUSED by the product.** Test: does the joke die without the product? It must.
4. **Format by genre:**
   - action/chase → multi-shot, 6–10 hard cuts;
   - sensory product → one take;
   - talking → selfie or doc framing (doc 42).
5. **Policy:** a paid cut must have no weapons, no police and no unsafe driving, and no health claims (doc 45).

Write 3 concepts, score them (docs 36, 38 and 45 rubrics), and recommend one. The owner picks.

## Step 3: Shot list + physics read
6–10 shots, each with:
- timecode;
- camera rig (only positions a real crew could rig);
- action;
- the physics check (doc 44 numbers);
- the sound event and its timecode;
- the product's state: the same vessel and label everywhere; if "drinks", the level drops.

## Step 4: Storyboard frames (the free "5 frames" offer uses this step)
- One still per shot.
- Cheap composition sketches: `higgsfield-ai/soul/cinema`, $0.004 each.
- Hero frames with the real product: `marketing-studio/image/flare` (product photo as `@Image`), ~$0.35 each.
- Make a contact sheet with timecodes and captions using a font file, never `:` inside drawtext text.
- Send it to the owner.

## Step 5: The video prompt
Use doc 43 §7 templates. For multi-shot, use ONE Seedance 2.5 r2v generation containing:
- GLOBAL STYLE;
- REFERENCES (one job each);
- FIXED GEOGRAPHY;
- PHYSICS;
- "EXACTLY N SHOTS AND N−1 HARD CUTS";
- the shots with timecodes;
- POSITIVE LOCKS;
- FORBIDDEN;
- AUDIO with timecoded events;
- `generate_audio:true`.

Keep it under 5,000 characters. Run at 480p first.

Product rules for every video prompt (doc 64; on 2026-10-09 only 5 of 19 films showed a legible product by 2 s):
- **Frame 0 is the product, in motion and making a sound.** It is opening, pouring, spraying or snapping, fills ≥ 30 % of frame height, and the label is legible (template: `test_native_sound_hook`). The cast and the action are the body of the film, never the first second. An action film opens on a ≤ 1.5 s flash-forward of the product beat.
- **The label comes only from the client's real photo.** The model never draws it from memory. Any shot where the label must be read is a **Kling 3.0 Pro i2v insert**:
  - the start frame is the checked still, with `last_image_url`;
  - 5 s, `sound:"off"`, `cfg_scale` 0.5;
  - ONE move: a push-in or ≤ 30° of rotation;
  - the label faces the lens and no hand or liquid crosses it.

  In wide or action shots the product is a silhouette or colour only.
- **Hands:** name the grip ("right thumb on the front edge, fingers wrapped behind, label to lens"), one action, and the hand enters already holding the product. No pick-ups, no fast wrist turns.
- Add to FORBIDDEN: "no readable text, signage, plates or logos except the product label from @Image1".
- Add to POSITIVE LOCKS: the vessel and the liquid colour. A drink is shown in its own can or in a clear glass; never amber on ice in a tumbler (an alcohol cue, doc 57).
- Final resolution: 720p, then a true upscale (doc 64 §3.1; SeedVR2 or ByteDance `aigc` after the owner-approved A/B). Never a plain resize labelled 1080p. If a 480p take is kept, its product shots are replaced by native inserts or a planar-tracked label composite.

## Step 6: Speech
- If a character is on screen AND speaks: render that exact line with **Wan 3.0 r2v plus the ElevenLabs audio file**. Measure the lag (`lipsync_check.py`) and bake the audio into that clip.
- Otherwise the line is a voiceover over a frame with no visible lips, or on-screen text.
- Locked voices: Otto `IbpG1IF3UdxPgaDKhwsd`, Vee `cLFf1Dc8DlgFwZ62rdPg`. For a client voice, design one per brand and record its ID in the job folder.

## Step 7: Edit + finish
- Keep the native sound effects.
- Add the voiceover tagline (2 lines, at the end), the logo card and the "AI-generated" super.
- Loudness: `loudnorm=I=-14:TP=-2`, then measure the ENCODED file: −14 ±1 LUFS and true peak ≤ −1.0 dBTP (doc 46).
- Deliver 9:16, plus 4:5 and a 6–8 s cut-down when the tier includes them.
- Supers (doc 64 §3.5):
  - inside y 240–1,260 and x 120–840 of 1,080×1,920;
  - font ≥ 60 px, sans or heavy serif, with a 3–4 px dark stroke or a 40 % scrim;
  - ≤ 7 words, on screen for at least (words ÷ 3) + 1 s;
  - one message-bearing super by 1.0 s.

  No thin italics over sky or cream.
- **Loudness is a hard gate.** On 2026-10-09, 11 of 19 films missed it and 2 clipped above 0 dBTP. If the encoded file reads > −1.0 dBTP, re-master (`loudnorm` two-pass, plus `alimiter=limit=0.8`) and measure again. Never deliver on a "close enough".
- End card: a **packshot of the product itself** plus the logo plus a swappable offer/CTA line. The product appears at least twice in the film.
- Upscale only after the picture lock. Re-check the label at a 100 % crop after the upscale, because generative upscalers invent letters.

## Step 8: QC, mandatory before anyone sees it (doc 46)
Run `skills/ad-director/scripts/qc/qc_report.py`, `continuity_check.py` and `lipsync_check.py` when someone speaks. Then check manually:
- a 2 fps frame strip of the whole film;
- 6–10 fps around every action;
- every sound onset against its action within 2 frames;
- every cut;
- character locks (Otto's mouth hidden, Vee has ONE stopwatch);
- the product label and vessel stay the same;
- no camera clipping through objects;
- no floating.

Then the doc 64 §4 pre-delivery checklist. Any FAIL blocks delivery:
- **Founder 3-second sheet** (frames 0, 0.5, 1, 1.5, 2, 3 s with the safe-zone box): motion at frame 0, the product legible and ≥ 30 % by 2.0 s, a super by 1.0 s inside the box, a sound transient in 0–0.5 s.
- **Label truth:** compare a 100 % crop of the label at the start, at every cut and at the end against the client photo, letter by letter. Colour ΔE ≤ 3.
- **Hands:** count the fingers on every frame where a hand touches the product (6–10 fps). The grip is the same across cuts.
- **Real resolution:** SSIM against a 480-wide round trip must be < 0.985 for a "1080p" file. 0.99 or above means 480p detail; say so or upscale properly.
- **`qc_report.py --stage deliverable` has no FAIL.** Frozen spans ≤ 6 frames unless they are a deliberate freeze-frame, and no unintended white or black hold. All 8 finals of 2026-10-09 failed it, Red Light included (a 2.9 s frozen hold).
- **AI tells:** no frozen rain or smoke, no garbled background text, no waxy face in a close-up.

List every fault found. Fix it, or report it honestly with the film.

## Step 9: Deliver
- Send it to the owner with a short Hebrew summary: what's in it, what was checked, known limits, and the cost.
- The owner sends to the client.
- Record the owner's reaction in `LESSONS.md` the same day.
