# 20 · YouTube gap-fill: Rourke Heath long-form, strategists, stills, automation

Researched 2026-10-07. Earlier rounds (14, 15, 17, 18) were blocked from YouTube. This round read **34 full transcripts** using the yt-dlp settings in `research/ai-video-reels/youtube/fetch_yt.py`. The transcripts are saved as `research/ai-video-reels/youtube/transcripts/gapfill__<id>.txt`, which is git-ignored.

- Nothing already in 14/15/17/18 is repeated here.
- `[inf]` marks our own inference.
- Sponsored and vendor videos are flagged. All numbers are the speakers' own claims.
- About a third of fetch requests hit HTTP 429 (see §5).

---

## 1. Rourke Heath: YouTube long-form

**Sources.** All are on his channel unless noted. R1 [Freelancer → AI agency: clients, pricing, scale](https://youtu.be/Uuvlqe2R06M), with Billy Boman, Dec 2025; R2 [Get Hired. Get Paid.](https://youtu.be/iuC7s-nm1TA), Upscale Conf, Jun 2026; R3 [Professional AI projects for clients](https://youtu.be/y0TnC-uZ6k8), Feb 2026; R4 [Claude + Higgsfield CLI](https://youtu.be/FQqkDXq1WEQ), May 2026; R5 [Seedance 2.0 prompting](https://youtu.be/tYJQusOS2jI), Apr 2026; R6 [Kling 3.0 cinematic films](https://youtu.be/KrEO2Hzv-PY), Artlist-sponsored, Apr 2026; R7 [Kling 3.0 $500 test](https://youtu.be/Rme22R7a9O8), Feb 2026; R8 [PJ Ace podcast](https://youtu.be/twUp-qTLkS8), Aug 2025; the pricing segment is paywalled; R9 [Weavy with Rory Flynn](https://youtu.be/c1W48MfoXok), Nov 2025; partly paywalled; R10 [Products into Veo 3](https://youtu.be/hSqznXKbp9Y), Aug 2025; R11 [AI UGC (Arcads)](https://youtu.be/QZ5u4Nt3g9w), Jan 2026; R12 [NB Pro hidden features](https://youtu.be/eqf_TT1g8ws), Nov 2025; R13 [Seedance 2.5 full film workflow](https://youtu.be/MY6f9xnYOwU), Higgsfield-sponsored, Aug 2026.

### 1.1 Clients, pricing, sales scripts

**Where the money is** (R2, data from 3,500 students):
- **Hero spots:** $95–250k per 30–60 s at the top end (~20 days, ~5 people at ~$1k/day, 30–40 % margin). One spec landed a €75k job.
- **Retainers:** $14k/month; a 6-hour spec won a five-figure retainer.
- **Local walk-ins** ("easiest yes", e.g. a bakery at $3k/month); niche specialists earn +22 %/h.
- **Workshops** (20 × $200, filled with ~$500 of local ads); productised Weavy workflows ~$6k + maintenance (R9: $5–70k).
- **Prediction:** one-off fees fall to "$10–15k for the best creatives" as performance marketers branch 100 one-shot ads.

**Outreach scripts.**
- **The rule:** *"finding the clients first and then learn how to fulfill what they want"* (R2)
- **Jab, jab, right hook** (R2). Post a spec for a brand you love and tag them, three times. With the third, DM "someone who works in marketing… they hold the credit card".
- **Custom sample** (R2), verbatim: "create five images for a brand, go on their website, find out what their brand identity is… create one short generation, send it to someone who matters at that company. Just get on a call." R1's version: 4–5 brand-tone images, a Calendly link, and a retainer pitch.
- **Find the decision-maker** (Billy Boman, R1). Pick 3–5 industries. On LinkedIn, go to the company → People → search "marketing manager", and ask an LLM which titles to target. LinkedIn DMs get read; Instagram and X DMs land in filtered inboxes.
- **Match the category:** clients "don't have imagination", so the sample must look like their category.
- **Paid reach:** ~$100 of Instagram ads on the showreel bought ~250 film/agency followers in key cities, beating LinkedIn ads (R1).
- **LinkedIn:** "every post is a job interview"; post how-tos with full prompts (R9). BTS breakdowns often beat the spec (R8).
- **Timing** (R8): release specs on model-launch day (PJ Ace: 3M views); sell brands the **"story about the story"** (first AI NFL spot = earned press).

**Pricing.**
- **Floor rule** (R2): "$2,500 is a great starting block… that now becomes your floor… tell people 'I'm too busy.'" Charge rush fees for 48 h.
- **Don't undercharge:** "'$37k, is that good?' – 'No, go 75K.' Landed it the same week." First jobs are "paid to learn" (€300 → $40k later).
- **Billy Boman** (R1): "never say yes… without seeing the script"; no fixed packages (revision hell); studio + personal day rates; **credits expensed, never billed**; price = time × complexity × scope.
- **Upsell:** 100 variants or localisation, +$2.5–5k on a $5–50k ad.
- **Objections** (R2): *"Can we legally use AI?"* → a lawyer's research memo you can hand over (Wonder Studios). *"AI looks fake"* → know every new model.

### 1.2 Pre-production (R3, R1, R13)

Milanote is the hub (inline video, full-quality downloads, pinned comments, green = approved / red = changes).

1. **Casting:** Pinterest ref → ChatGPT *"extract data from this image and write a prompt… head-and-shoulders portrait against a white studio background with soft white light"*. Make 3 candidates and keep the one "with a story". R13 builds character sheets with **GPT Image 2** because NB Pro gives "plastic" skin.
2. **Character sheet** (R3): profile, back, eyes, full-length, hands, emotions; wardrobe fix *"replace the collared shirt… with Russian-style clothing from the full-length shot"*. Composite **one Photoshop sheet** (face enlarged) and attach it to every generation.
3. **Location:** pick the set with the most **interactable story props**. Ask the LLM for 7 angle prompts from one master frame (top-down, prop close-up, bulb POV, outside-window-looking-in, low angle), each run with the master attached "to lock lighting and placement". **The location ref sets the project's grade** (R13): *"create a sandy beach in the same environment with the same colour correction, but with a wooden beach hut… no people"*. Fix fake signage in Photoshop, not by regenerating ("quality degrades").
4. **Lighting master prompt:** NB "change the lighting in this scene to 6 am" ×6 → pick → ChatGPT *"pull the data from this image… create a consistent prompt I could apply to many different images to adjust their lighting… include time of day, lighting style, shadows… begin with 'Adjust the lighting in this image to'"* → apply to every angle.
5. **Integration** ×4: *"add this woman into the scene from the back as she walks away… She is out of focus, while the room is in focus."*
6. **Client rounds** (R1): a beat timeline with options under each beat; round 1 options → round 2 brand colours → round 3 storyboard.

**NB Pro tips** (R12, R6): generate at **2K** (video models reject 4K); keep **one camera preset (ARRI Alexa + Signature Prime) on every still**; attach screenshots of a written brand or **style brief** as refs (*"change the design of this poster to match the brand identity outlined"*), which acts like an sref; storyboard grid → *"take the first scene… generate a shot list of eight shots"* → rectangle-select a panel → *"generate this frame in full 16:9"*; misspelt small labels → shoot closer.

### 1.3 Seedance and Kling prompting

**Seedance 2.0 via his Claude skill** (R5): sections for lighting with **HEX codes**, palette, camera, particles, character, environment arc and mood, broken into 2 s chunks. "Seamless" prompts end *"No cut, no end card. The frame rests on…"*. Paste only the shot list. Character limits: Seedance ≈4,000, Higgsfield ≈3,000. **Omni-reference ingredients** (sheets + location instead of a start frame) allow character reveals and in-generation cuts. 3D type: location + 3D-text image, *"add this text floating in 3D inside the scene. There should be a shadow underneath the text where it's floating."* iPhone hybrid: generate from a screenshot of your own clip at the action beat, then splice.

**Seedance 2.5** (R13): 30 s generations, 50 refs including video and audio, 720p max, **~$40–60 per 30 s generation**.
1. Write a **~1.5-page director's script**: shot size first, actions, ambient sound, focus, accent, dialogue.
2. Give **exact timings** ("laughs disgustingly for *half a second*", or it laughs for 2 s).
3. Demand **background motion** ("people moving around behind us… otherwise Seedance won't do it").
4. Claude converts it to a time-coded prompt opening with a **fixed camera header** (body, lens, focal length, depth of field, halation, "subtle organic grain") and a **CAST block** naming the tagged refs.
5. **Run three generations and cut the best parts together**, then add subtitles, music and a light grade with grain so it isn't "too slick". A Blender blocking video works as a camera ref.

**Kling 3.0: the opposite rule** (R6): *"Do not ever try to prompt Kling with AI… it will mess up nearly 90 % of your generations"* (symptoms: slow motion, morphing). Write short human prompts and iterate by hand. In February (R7) he still used a Gemini gem `[inf: a Kling-only heuristic]`.

Acting iteration, verbatim (R6):
```
v1  The man looks nervous and he raises his hand as the camera pans down to the control panel and clicks the red button and the button lights up red. He is trembling slightly from his nerves.
v3  The man shouts back, "Okay!" and his head shakes in anger and frustration. He pauses, closes his eyes in disbelief and he swallows, which makes a loud noise. He sighs and says, "Here goes nothing."…
v4  The man looks to the left and shouts, "Okay!" in an anxious tone…   (eyeline took 3 more takes)
```

Other verbatim prompts (R7):
```
SFX: a massive power up sound effect like a turbine spinning at max speed that cuts the silence of the final frame.
Camera performs a fast lateral pass left to right, then a brief crash push into the face [0.5–0.8 s], then a quick pull back and a fast pass back right to left. No circular motion around the object. Robotic arm/camera control. Very snappy accelerations, but no shake. Stable face. Braids intact. Outfit artifact free.
Interior dash-level profile on driver's cheekbone, rack focus from eyelashes catching dashboard LEDs in windshield bokeh… speed ramp from 40% to 100%… finishing on a macro push into the pupil.
Shaky documentary handheld style camera motion where the camera walks in and gets a close-up of the man's face.
```

**Kling technique** (R6):
- **Multi-shot without new stills:** start frame + *"cut to a close-up of the scientist's face… cut to the man wearing glasses in the background"*. Screenshot the invented angles and reuse them as refs.
- **Repair kit:** borrow a line from another take's audio; **J-cut** to hide a wrong eyeline; mask a second take into the window only; cut between speakers to hide voice drift.
- **Inserts:** 25 Claude-written "things switching on" prompts sharing one lighting ref.
- **Edit:** cut in at 1 s inside a 2 s clip; keep the eye-trace centred; music last.

**Frame 0** (R6, R8): "dead or alive based on the first 4 seconds". Design it like a MrBeast thumbnail (subject right, object left, low angle, mid-action); "the first 8 h [of 13] is the first 5 seconds".

**PJ Ace's method** (R8): list wild visuals → list talking-point line variants → marry lines to locations → the LLM writes prompts **one at a time** ("it will condense the crap out of this if it gives you 10"). Opener `cinematic handheld medium shot` + person + action + dialogue ("handheld offsets the AI mystique"; medium shots morph less). "JSON prompts are overrated." Use i2v when the client must pre-approve; otherwise expect "~6×" regeneration.

### 1.4 Claude + Higgsfield CLI machine (R4; extends 14-H)
- **CLI over MCP:** the CLI uploads local refs and downloads and names outputs.
- **Folder:** `environments/` + `environment_descriptors.md` (UUID, text, and *when to use text vs the image*: "NB Pro uses the environment image as gospel", so use text for new angles); `model_refs/`, `product_refs/` (sheet + material notes such as "obsidian, shiny, light refracts"); `prompt_log.md`, `reference_ids.md`, `seedance_failure_log.md`, `handoff.md` (rules), `outputs/`.
- **Rule:** *"character sheet + trainer sheet only. Never use detail/editorial images as a reference: Seedance copies them as a literal frame into the video."*
- **Product sheet:** `white background, create a product sheet that covers all of the angles of this product. Create six separate images all inside of one photo.`
- **Run log:** Claude checked cost first, then logged "**Creator plan caps concurrent Seedance jobs at 8**" and switched to chunks of 6. It flagged "product too large compared to the models". Generated end cards were "pretty crappy", so upload your own PNG card. The Google Sheet tracker (status + notes) is read before each batch.
- **Result (R2):** "150 ads overnight… ~10 sales × $97 = $970 vs $671 spend", excluding Seedance cost.

### 1.5 Annotated frames and UGC (R10, R11; adds to 14-B/F)
- **Annotated frames:** make the product photo as large as possible on the board. To fix white-canvas bleed, start the on-image text with `No white background. The camera zooms into the image on the left to make it full screen,`. `rises into the air with zero gravity` helps assembly shots. Build the plate without the product. Drop the clip's first 1–2 s.
- **UGC prompts:** use **film-stock** tokens ("Kodak Portra 400") and repeat one exact accent line in every Veo prompt for a consistent voice. For Kling Motion Control, film yourself in the *same composition* as the image.

---

## 2. Creative strategists (full talks)

**Sources.** S1 Savannah Sanchez, [200+ ads/week](https://youtu.be/MT2MzrTGC5w), Motion, Jan 2026; S2 Dara Denney, [Strategists set up to fail](https://youtu.be/hchtNL80d2g), Motion, Oct 2025; S3 Denney + Alex Cooper, [Creative Strategy AI mastery](https://youtu.be/ITM4faRVzF8), Motion, May 2025; auto-dubbed transcript; S4 Denney, [AI creative strategist](https://youtu.be/Uh0TE6nZs5A), Perplexity-sponsored, Jun 2026; S5 Denney, [Testing at every budget](https://youtu.be/7knQyPYLmfo), Mar 2025; S6 Cooper + Barry Hott, [Biggest mistakes 2026](https://youtu.be/mpj0A4Prxu4), Apr 2026; S7 Hott, [Pretty ads suck](https://youtu.be/YuS18wnD_bc), 2023; S8 Cooper, [Claude Code strategist](https://youtu.be/aD7vKl1nkcE), Parker plug, Jul 2026.

### 2.1 Concepts, angles, hooks
- **Frame 1 is where ads die** (S6): Meta quickly learns "this video means nothing". The under-rated lever is the **setting**: a symmetrical perfume shelf felt "not for me" to a viewer who expected a loft, so you may need "10 videos with 10 settings for 10 types of people". Briefs must specify the hook visual (phone on the counter vs tripod vs fisheye).
- **"I did X → got desired result Y"** (S2): *"I threw a spoonful of this into my noodles and my husband swore I picked up takeout"* beat *"I've been using this bone broth…"*, which gives away the plot. Also: strong reactions, **contradictions** (*"Contrary to popular belief, alcohol is not actually toxic"*), and YouTube titles, which have to earn an opt-in click.
- **Mine organic content:** Denney's "viral ads SOP" searches niche keywords for **high-view, low-follower** posts. Sanchez takes more from organic TikTok edits than from ad libraries and keeps a **transitions database** (S1).
- **Persona × value driver** (S1): A/B less- vs more-specific openers per hook; spread the drivers (paint kit: blank-page fear, identity "become a painter", outcome "I made this", gift, connection); swap demographics.
- **Plain language** (S2): Reddit said "colourful sheets", not "aesthetic", and the plain wording won. Naming the founder and attacking the #1 objection gave a 52 % hook rate vs 9 %.
- **Image-gen statics** (S3): **deliberately unrealistic visualisations** of the value prop (*"12 years of nerve pain gone in minutes"*).
- **Ugly levers** (S7, S6): change at least one of talent, light, camera, angle, script, story or setting; drop the most expensive component; keep the hook relevant. In 2026 that means "the way the audience expects it to look" (creators holding lav mics).

### 2.2 Production, testing, AI's role

**Sanchez's factory** (S1): 40 creators, ~10 editors, 50 clients, 200+ ads/week. Mon–Tue shoot, Wed–Thu edit, Fri review; strategist, creator (raw footage only) and editor are never combined. The creator brief is a shot-list checklist with hook V1/V2. The editor brief gives VO line / caption / visual, line by line. QC covers HDR off, lens smudges, safe zones, a sound-off typo pass, ≥3 s per text frame, and "is it better than the inspiration?"

**Variants and iteration** (S1):
- **Meta treats variants as distinct only if the first 3–5 s *visual* differs**; text-only changes don't count. Weekly minimum: 2 inspirations × 2 hooks × 2 opening visuals.
- **Cross-client hook test** (a fake-poll hook run across brands) → winners go into a **winning-concept library**.
- Iterate a winner with the same creator on a new hook, another creator on the same script (isolates the creator variable), reshuffled clips, and 30 → 15 s cuts.

**Budget ladder** (S5): $5–15k/month = one Advantage+ campaign with ~10 mostly static ads; $30–50k = add a test campaign, one ad set per concept (3–6 ads, $100–200/day), winners duplicated to scale; $1M+ = ~$200/day × 7 days per test, 10–20+ tests a week.

**Metrics** (S6): **hit rate is a bad KPI; judge by cumulative spend**; don't kill a top spender on CPA alone (breakdown effect). From March 2026 Meta counts click attribution on **link clicks only**. Cadence: a winner slide (hypothesis → analysis → "what else to pressure-test", S2); monthly retro and roadmap, weekly sprint (S3).

**AI's role.**
- **Prioritising stays human:** "the problem isn't 'I can't come up with ideas', it's 'I have too many'". "AI makes people extraordinarily mediocre" (S3, S6).
- **The headline prompt that found a winner** (S3): reviews + the last 5 winning headlines **with why each worked** → "10 more for 40+ buyers". The human picked *"Your wrinkles will thank you for this."*
- **Prompt rules** (S3):
  - Write it for "an intern who leaves tomorrow".
  - Include good and bad examples. Good ones weigh more, and 10 good ones should each be chosen for a *different* reason.
  - Name 4 angles to stop angle collapse.
  - A/B the prompt itself.
  - Keep a shared prompt library.
  - Hacks: "this is a 4/10"; "what should I have asked?"; make Claude and GPT critique each other.

**Research agents.** Denney's "Recon Report" (S4) gives an executive POV, a sentiment verdict ("loved but distrusted"), reputation by source along the shopper's path (Google page 1, press, Trustpilot, Reddit, YouTube reviews), per-SKU reputation, and personas with **verbatim VOC lines**, JTBD, triggers and objections. Cooper's Claude Code brand brain (S8) ingests the Slack feedback history and runs a Monday routine that turns charged review/comment phrases plus untested personas into 25 statics. An ad comment ("he's like my newborn, 16 years old") revealed an untested senior-dog angle.

---

## 3. AI product-photo and still tutorials (2026)

**Sources.** P1 [Magnific: text consistency NB Pro + Kling Omni](https://youtu.be/XLHTLJhzDyQ), Mar 2026; P2 [AI for Creators: directing product photos](https://youtu.be/gdZGS8Pfd8M), Aug 2026; P3 [Chris Rawlings: NB Pro Amazon set](https://youtu.be/12pQ0W2bCDE), Dec 2025; P4 [Lundström: GPT Image 2 vs NB Pro](https://youtu.be/IHK_KavtN_c), Higgsfield-sponsored, Apr 2026; P5 [ComfyUI: 3×3 product grid](https://youtu.be/o6zPwB5U4Gg), Dec 2025; P6 [Soul ID catalogue](https://youtu.be/BtZDql-bTSA), Feb 2026; P7 [Escapism: why AI product images fail (NB Pro + FLORA)](https://youtu.be/R7Eml0ttQtg), Sep 2026, affiliate, auto-dubbed.

### Prompt order (P1)

Order beats length. Magnific's sequence:
```
1 COMPOSITION FIRST: editorial still life with diagonal placement and controlled directional lighting
2 IDENTITY: the product must match the provided references exactly, including proportions, silhouette, stitching, panel geometry, sole curvature, and overall construction
3 TYPOGRAPHY BLOCK: exact words · where · alignment · orientation — no misspellings, no extra letters, no warped glyphs
4 TRUE COLOUR: deep cobalt blue upper, neon lime laces, off-white midsole, mint heel lining
5 LIGHTING & HARMONY
6 OPTICS: shallow depth of field, tack-sharp focus on the shoe and its typography, refined tonal balance, no oversaturation
7 NEGATIVES: no extra logos, no duplicated text, no invented branding, no distorted lettering
```
- **Video:** in Kling 3.0 Omni, give the **same white-studio refs** as multi-refs, not the still as a start frame.
- Keep the video prompt minimal and **don't restate the typography**. Small text held in close-up.

### Label protocol (P7, agency work)

**Capture:**
- ~6 iPhone shots;
- shape as a **length:width ratio** plus an in-hand photo;
- HEX colours;
- **one true-size in-hand photo**;
- the label text typed out.

**Reference mistakes:**
- Too many refs. Use one ref per product *state*.
- Putting the label close-up first. **The model takes its shape from the first image**, so you get "perfect text on the completely wrong product".

**Frame share:**
- Product under 35 % of the frame: small-print errors are tolerable.
- 70 % or more: everything must be exact.
- For small-in-frame shots, paste:
```
Every line of text smaller than the main logo falls outside the physical resolution of the frame. Render these lines as a soft, natural optical blur without trying to make the letters legible.
```

**QC and fixes:**
- Use JSON-style prompts for heroes and close-ups.
- Pick at thumbnail size, then **read every line aloud, smallest badges first**.
- **Fix, don't reroll:** "everything stays the same except [area]; the text should read [exact]". Rerolling loses the scene.

### Model choice
GPT Image 2 got a dense whiskey label word-perfect where NB Pro failed, but **leaves a repeating noise pattern in wide landscapes, bubbles and liquids**; NB Pro is more photoreal (P4). P7 rates NB Pro best for integration ("Sunburst" looks pasted in). Lundström builds commercials **backwards from the hero end frame**.

### Direct before generating (P2)
1. **Context:** brand, buyer, materials, tone, "what I don't want to see", logo and photos, then "don't write anything yet, just confirm".
2. **Moodboard analysis:** repeating colours, light, framing, *which refs don't fit*.
3. **Three directions** (name, belief, feeling, recurring detail, 3 rules) with **one test image each, judged against the real product**; the human picks.
4. **Style lock:** one paragraph (message, motif, camera/film, colour + accent, light, finish, realism rules) **appended unchanged to every prompt**.
5. **Shot jobs:** hero, stand-in macro, evidence, product in use, tactile detail.

### Phone-photo repair loop (P3)
Inputs are 3–4 phone shots with engraving close-ups and a **scale cue**. A plain prompt works: `Create a clean product photo rendering of this product to be used as the primary image on an Amazon listing.` Failures: product **too big** in lifestyle shots (priors from bigger competitors), invented glow, mismatched proportions. Fixes: **one issue per turn**; name the glow source exactly; **start a new chat when a thread degrades** (one turned the product black). For graphics: "simple, modern and clean style, mobile optimized".

### Grid economics (P5)
**One NB Pro 4K call = a 3×3 sheet** (≈1K per cell, cell aspect ratio = the call's) with numbered per-cell prompts and "no margin, gutter, borders". Fix the seed, select a cell → `upscale image one, use the product from image two as reference`. A stale product description beats the ref (a can became a glass bottle with a corkscrew). Animatics: cells → 3 s Seedance Pro Fast clips at 480p ("≈$0.03/run").

### Outfit swap (P6)

`put the outfit from image one on the model from image two. Do not change the model, her appearance and her face.`

---

## 4. Agency automation walkthroughs

**Sources.** A1 [Nate Herk: Claude + Higgsfield agency](https://youtu.be/xn6Z5PYyAIE), May 2026; A2 [Higgsfield: MCP content factory](https://youtu.be/l7W3QzU8w5s), vendor, May 2026; A3 [Mulcahy: 100 statics in Weavy](https://youtu.be/PsetOePzzW4), Jan 2026; A4 [Nastišin: photos → video ads in Weavy](https://youtu.be/ePuIGGQ9IWE), Nov 2025; A5 [Dylan Michael: n8n + Veo UGC](https://youtu.be/eh18AWUq3mk), Jan 2026; A6 [Joshua Mayo: Marketing Studio](https://youtu.be/itv4Xljkbqw), May 2026.

- **Reference lock is the #1 failure** (A1). The agent wrote "a blue bottle that says sleep support" and Higgsfield invented generic bottles. Fix: *"This is our actual product image… it has to appear as shown in this reference image every single time. Same colours, same text. Don't change anything."* If the label still drifts in i2v, simplify the video label to logo + name.
- **Policy blocks** (A1, R4): "why was that denied? show me the prompt" → strip the triggers → **write the banned phrases into the skill or failure log**.
- **Knowledge + matrix** (A1): a deep-research `advertising_masterclass.md` read before ideation; a Sheet "creative slate" (value prop × headline × avatar × style × angle) with a **status column** so routines never duplicate work (Sunday "add 50 ideas", Monday "generate 30 blank-status rows"). Turn the best output into a `.claude/skills` skill.
- **Vendor content factory** (A2): research → 20 idea cards → 100-row plan → **per-batch approval gates** → Meta MCP. It claims 100 UGC videos for ≈$900 (vendor claim); visible flaws included fake tiny sips. Hook bank: chained street interview ("the last person I talked to said…"), "rate this out of 10", blind taste test, a random object in the unboxing.
- **Weavy statics** (A3): Gemini turns brand refs into a **"visual bible"** → "10 diverse prompts separated by `*`" → iterator → NB Pro; a separate LLM pass mines reviews into **motivation buckets × 40 headlines** overlaid in Figma. Ladder: static (cheap angle test) → animated → video **only for winners**. The same system-prompt rule recurs in R9: "**only provide the prompt, no additional context**".
- **Keep text and logos out of generation** (A4): style description ("do not reference any product") + "no text on the ad" → NB → outpaint/crop to 9:16 → Seedance `product animation, camera slowly moving sideways and zooming in, product is still in focus` → Weavy's video **Compositor** layers the real logo and text.
- **n8n chain** (A5): sheet row → UGC image agent ("small imperfections, loose hairs… selfie stick, mirrors") → NB edit → poll → **vision model describes the still** → Veo-prompt agent → Veo 3 → link to sheet. There is no QC gate.
- **Marketing Studio** (A6): splice an unboxing hook onto a tutorial with the same avatar for longer ads.

---

## 5. Not fetched (HTTP 429 after retries at 25–90 s spacing)
Rourke `H0Ahmz2xuvs`, `W45T919iFxM`, `Z5HLzd97EKw`; Motion workshop cited in 17 `_r7NUcM41Kc`; Denney `yRgPbqywUJ8`, `4wM-i1cxtAM`; Sanchez `76KH-GZZ5w4`; Cooper/Pawliw `VkSOHGT_AMc`; Motion review-mining `YUMg-1ArPvE`; Rawlings GPT Images 2 `6eG3T-Esp4E`; Seedream 5 `v_VICKllPLE`; Higgsfield `iOwKylW8c5Q`, `kFKpcCHkuPI`; `t_a3rkBbVq8`. The block was partial, not total.

---

## 6. New things to adopt (→ file each extends)

1. **Pricing kit:** $2.5k floor, rush fee, see the script before yes, variant/localisation upsell, legal memo. → **14**
2. **Custom-sample outreach:** 5 brand-tone stills + 1 clip to a named marketing decision-maker. → **14**
3. **Kling prompts written by hand;** LLM builders for Seedance only (≤3,000 chars). → **14**
4. **Seedance 2.5 director's script:** exact timings, required background motion, fixed camera header + CAST block, 3 generations cut together; budget ~$40–60 per 30 s. → **14** / **18**
5. **Reference scope:** never feed editorial/detail images to Seedance; text vs image environment chosen per shot. → **14** / **18**
6. **Lighting master prompt** across all angles; location ref sets the grade; fix signage in Photoshop. → **17**
7. **Magnific 7-part prompt order** as the default composite template. → **17**
8. **Label protocol:** shape image first; one ref per state; typed label; frame-share rule + "soft optical blur" sentence; read every line aloud; targeted fixes. → **17** §2/§5
9. **Model split + check:** GPT Image 2 for dense labels and skin, NB Pro for photoreal integration; zoom-check GPT Image 2 for noise in environments, bubbles, liquids. → **17** §1/§5
10. **One issue per turn; new session after 2 failed fixes.** → **17**
11. **Style lock + 3 test-image directions** judged against the real product; every shot gets a job. → **15** stage 5 / **17**
12. **3×3 grid previews** (fixed seed → select → upscale with product ref); 480p 3 s animatics. → **15** / **18**
13. **Failure log + policy loop:** banned phrases baked into the skill. → **18**
14. **Seedance concurrency cap:** batches of 6. → **18**
15. **Status-column test matrix + ideas/generate routines**, keeping per-batch approval. → **18**
16. **Composite real logo/text** over generated clips and end cards. → **17** / **18**
17. **Frame-0 setting relevance:** name the setting and its audience; 2+ setting variants. → **15**
18. **"I did X → got Y" and contradiction hooks; high-views/low-followers mining.** → **15** §1.3
19. **Variants count only if the first 3–5 s visual differs;** less- vs more-specific opener pairs. → **15**
20. **Headline prompts seeded with past winners + why they worked;** 4 named angles; human picks. → **15** stage 1
21. **Judge creative by cumulative spend, not hit rate.** → **15** §3.3
22. **Recon report** (reputation by source + verbatim VOC) as the Stage-0 artefact. → **15** stage 0
