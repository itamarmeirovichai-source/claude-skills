---
name: ad-director
description: End-to-end AI ad direction for a single product - brief intake, ledger-aware creative dice so concepts never repeat for a client, insight -> concepts -> scored finalists, script, timecoded shot list, per-shot model routing (Seedance / Kling / Veo / Runway / image models), production prompts, take QC, automated render QC (loudness, pacing, black/frozen/flicker, brand-colour fidelity vs packshot, safe-zone sheet) and a 100-point visual rubric. Use when the user hands over a product (photo, link, name) and wants an ad or reel planned, prompted, and quality-checked; pair with reel-studio for the edit.
---

# Ad Director

Turns "here is a product" into a finished, quality-checked ad plan:
**brief → fresh concept seeds → 3 scored concepts → script → shot list with a model per shot → prompts → takes → edit (reel-studio) → QC.**

The creative method (insight mining, 6 mechanisms, scoring gates, psychology checklist) lives in
`research/ai-video-reels/chapters/17-creative-director-system.md`. This skill packages it as a procedure with tools, adding three things:
- **Anti-repetition:** concept dice plus a ledger, so no client gets the same idea twice and the studio does not drift into one style.
- **A model router:** for each shot, which model is used and why.
- **A QC gate:** at the take level, the render level and the visual level.

## When to use
- The user sends a product (photo, URL, name, packshot) and asks for an ad, reel, concept, script or prompts.
- The user asks "which model should I use for this shot?" or "is this video good enough to send?"
- The user wants to benchmark video models on their own products.

## Tools
```bash
D=skills/ad-director/scripts/director.py
python3 $D new jobs/driftline-heat --product "Driftline Citrus" --client "Driftline"   # job folder
python3 $D dice --client "Driftline" -n 5               # 5 fresh, mutually different seeds
python3 $D dice --client "Driftline" --lock format=asmr_macro -n 3   # explore inside one format
python3 $D log --client "Driftline" --title "Heat Index" --seed-json '<seed JSON>' --result "chosen"
python3 $D history --client "Driftline"
python3 $D qc final.mp4 --packshot packshot.png --duration 15 [--one-take] --out qc/
python3 $D bench --out bench/ --models seedance25,kling30pro,veo31   # model test matrix
python3 $D bench-summary bench/bench_matrix.csv
```
The ledger defaults to `~/.ad-director/ledger.jsonl`; override it with `--ledger` or `AD_DIRECTOR_LEDGER`. Keep one ledger per studio and back it up, because it is the memory that prevents repeats.

## Procedure (follow in order and show the output of each step)

### 1. Intake (5 min)
Run `new` and fill `01-brief.md`. Look at the product photo: describe the shape, colours (hex if possible), label text exactly as written, material, and size. Collect:
- 3 facts the client can substantiate.
- The distinctive brand assets.
- The audience's own words.
- One action you want them to take.
- Where the ad runs (state matters for legal).

When an input is missing, make an assumption and mark it `[ASSUMED]`. Ask at most 2 questions.

### 2. Insight + clichés (chapter 17 §2, steps 1–3)
- Write 12 candidate insights and pick 1.
- List the 5 category clichés. They are banned unless twisted.

### 3. Roll seeds, then think (the anti-repetition step)
Run `dice --client <client> -n 5`. Each seed combines:
- mechanism × format × hook × emotion × structure × look × sonic
- plus one creative **constraint**

Seeds are *provocations, not orders*. For each seed, write the best idea it provokes for this product and insight. You may swap one dimension when it clearly fights the product; say so if you do. Also write 2 "free" ideas that ignore the dice. The aim is a range of 7 ideas that look nothing alike.
- Kill test: if two ideas share a key visual, replace one.
- AI-cliché ban (unless twisted): floating product with particles, a splash crown, a slow orbit on black, logo morph, "cinematic" drone over a city.

### 4. Score and pick (chapter 17 §2 step 7 table)
- Score each idea on originality, brand linkage, emotion, AI-feasibility, cost and legal.
- Gates: legal ≤2, AI-feasibility ≤2 (with no hybrid fix) or brand ≤2 → killed.
- Pick 3 finalists from at least 2 mechanisms. One of them must be "safe-but-sharp" (legal 5, cost ≥4).
- Present all 3 to the user with a recommendation. After the choice, `log` it (also log rejected finalists with `--result rejected` when the client saw them).

### 5. Script (`03-script.md`)
- Beats: Hook / Setup / Turn / Proof / Payoff+brand / CTA.
- VO at about 2.5 words per second, or no VO.
- Supers are added in post.
- Write 5 hook variants for testing.
- Default length: a 15 s master, with 6 s and 30 s cutdowns planned at script time.

### 6. Shot list + model routing (`04-shots.csv`)
For every shot:
- size/angle/lens, light, **one** camera move with an end state, method (T2V / I2V / KF / V2V / LIVE / POST), **model + backup**, risk A–D and mitigation, and a takes budget.
- Route with `references/model-router.md`.

Production rules:
- **Start-frame first** for every product shot. Generate the still with an image model, check the label against the packshot, then animate (I2V).
- **Cut on contact.** Never show a hand gripping the label for more than about 1 s.
- **Composite the real packshot** on the end card and on any frame where the label must be readable (chapter 16).
- Humans in beauty, health or food get "natural skin texture, visible pores, no smoothing".
- One location per shot, and at most one broken physics law per ad.

### 7. Prompts (`05-prompts.md`)
- Use the grammar card for the routed model from `references/model-router.md`.
- Every product shot carries a PRODUCT LOCK line: exact label text, colours, shape, "label stays sharp and unchanged; no extra text".
- Keep negatives to 6 or fewer, and in plain words.
- Never write "stunning / epic / 8K / masterpiece". Use verbs and physical light.

### 8. Takes + take QC
- Generate within budget and apply rubric layer 1 (K1–K8) to every take.
- Log keeper ratios per model in the bench CSV. This gives you real data on which model wins for which shot.

### 9. Edit with reel-studio
- Use beat-synced cuts, supers inside the safe zones, real-packshot end card, sonic logo, -14 LUFS.
- Export the master plus the 6 s cutdown plus 5 hook variants.

### 10. QC gate
- Run `director.py qc`.
- Then **look**: Read `qc/qc_sheet.jpg` and `qc/product_compare.jpg`, and score the 100-point rubric (`references/qc-rubric.md`) into `06-qc.md`.
- Ship only with no FAIL and ≥80.
- When under 80, list the 3 fixes with the biggest point gains, do them, and re-run.

## Benchmarking models (do this whenever a model updates)
1. Run `bench` to get a matrix of 12 standard ad tests × models × 2 takes. The tests are: label rotation, pour, hand pick-up, macro texture, food bite, lip-sync, FOOH scale, fast camera, multi-shot consistency, text in scene, V2V blockout, stylised world.
2. Use **the same start frame and the same prompt intent** per test (adapted to each model's grammar).
3. Score each take 1–5 on adherence, product fidelity, artifacts, motion/physics and aesthetic, and record cost and takes-to-keeper.
4. Run `bench-summary` and update the router table with the winners. Data beats opinions. Re-run every quarter, or when a major model version ships.

## Legal lines (never skip)
- No fake testimonials or AI "customers" giving reviews (FTC 16 CFR 465).
- No AI before/after images for medical or beauty results.
- Disclose AI where the platform requires it.
- Real people need written consent for face and voice.
- Category rules are in chapter 17 §8 (alcohol, med-spa FL, real estate FL).
- Never use a real brand in a public spec ad without permission. Use fictional brands for demos.
