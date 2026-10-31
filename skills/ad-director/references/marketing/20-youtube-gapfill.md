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

---

## 7. Round 2 (2026-10-08)

Same method as §1–4, with the same `fetch_yt.py` settings. Transcripts are saved as `research/ai-video-reels/youtube/transcripts/r2__<id>.txt` (git-ignored). **20 transcripts** were read: 3 of the IDs listed in §5 plus 17 new ones. 16 are written up below; 4 are old, teasers or covered elsewhere and are listed only briefly. YouTube returned HTTP 429 (an IP block) for most of the run, so §7.5 lists what is still missing. As before, **all numbers are the speakers' claims**, `[inf]` marks our own inference, and sponsored or affiliate videos are flagged.

### 7.1 Seedance 2.5: long takes, references, prompt structure

**V1 · `H0Ahmz2xuvs` · Rourke · [Seedance 2.5 tutorial: cinematic AI video from start to finish](https://youtu.be/H0Ahmz2xuvs) · 2026-09-25 · 66 min.** Unedited, with the mistakes left in.
- **Prompts up to 10,000 characters.** Paste the whole script plus refs into Claude: *"Now create a Seedance 2.5 prompt with this… You have 10,000 characters to get as descriptive as you can with the acting performances and nuances."* The result was 9,963 characters; that platform's limit is 10k.
- **Don't overfill a take.** A 1-minute script crammed into 30 s "went haywire" (garbled lines). Split it into **2 × 30 s prompts**. If speech speeds up, there is too much dialogue for the duration: add another generation.
- **A 30 s take holds continuity across its own internal cuts** (character positions, light). Separate 6 s generations drift. It is still a gamble: two people on a bench swapped left and right, so **state positions explicitly**.
- **Look comes from ShotDeck.** Give Claude a ShotDeck frame plus its data panel (camera body, lens, film stock, hex palette). Claude writes the MJ prompt, then a **fixed camera header for every video prompt** ("35 mm… ARRICAM"). Use the ShotDeck feed as a dummy social feed: which frame cuts through?
- **Grade transfer for real photos:** own photo + ShotDeck ref → NB Pro *"keep the composition, framing, geometry, architecture the same, adjust to 35 mm grain / cinematic grade"* → use the result as a location ref.
- **Direction details:**
  - the **surface** each sound lands on ("lands on the grass", or you get concrete);
  - an **origin or accent for the second character every time** ("my friend is Australian"), which keeps the voice consistent;
  - micro-acting (lip bite, eyebrow, shoulders drop);
  - the duration of each hold ("camera holds for 2 seconds").
- **Voice reference:** record a pangram (*"That quick beige fox jumped in the air over each thin dog…"*), export it as a **black MP4** and attach it as a video ref: *"use @video1 as reference of man A"*.
- **Feedback loop:** watch muted and dictate timestamped notes ("at 2 s bite lip earlier; at 5 s wide not close-up; at 7 s no dead pause") → Claude revises → rerun the same prompt, changing only the acting.
- **Mining:** keep only the parts of each 30 s take that move the story. Premiere *Scene Edit Detection → clip marker at each cut* splits a multi-shot generation automatically.
- **Post:**
  - Open on action and pull the first line's audio over the opening frame.
  - Use 3–4 music changes in the first 15 s.
  - Apply the same light Lumetri grade to every clip and add captions.
  - For a Suno track, Claude reads the time-coded prompt and sets the hits ("slow piano 62 BPM C minor").
- **Do not adopt:** he generated on an unofficial Chinese Seedance build and renamed a trademarked prop to get past filters. That is an IP and ToS risk `[inf]`.

**V2 · `2b3Z4rW5VJc` · Youri van Hofwegen · [STOP wasting credits & master Seedance 2.5](https://youtu.be/2b3Z4rW5VJc) · 2026-08-21 · affiliate.**
- **Prompt sections:** FIRST FRAME · CHARACTERS (group the extras, e.g. "frozen tableau") · ACTION (the most detail) · **RULES** (world and physics rules; without a "freeze rules" block, the frozen petals and birds moved) · CAMERA · LIGHT & COLOUR · DIALOGUE · AUDIO.
- **Audio is always generated jointly, so always direct it.**
- **Dialogue:** put each line where it is spoken in the shot, **and** repeat all lines in order in a DIALOGUE block at the bottom, with delivery and language ("English, short, and shouted").
- **Sound timing:** say when each sound comes in and goes out; the engine then fades with distance.
- **Music:** separate MUSIC & LYRICS (BPM, instruments) from SOUND CHARACTER (reverb, crowd, close-mic). Write lyrics in the target language, because translating produces a fake accent.
- **Video-to-video:** the first line is an instruction (*"Transform the footage into … while keeping the camera and the gestures exactly as I filmed them"*), followed by the replacements: environment, specific objects, figures, audio.
- **Limits:** 2.5 accepts 30 images + 10 videos + 10 audio refs (2.0 took 9 + 3); 720p max; 4–30 s. Occasionally a character duplicates for a split second; fix it in the edit.

**V3 · `AvB-dfxTMgE` · Teacher's Tech · [The prompting technique that makes Seedance 2.5 work](https://youtu.be/AvB-dfxTMgE) · 2026-08-08 · Higgsfield-sponsored.**
- **Timeline prompting:** each timestamped beat states subject, action, camera, audio. **"Treat each beat like a budget."** A beat with breach + churn + line + camera drop in 6 s failed; splitting it into two beats fixed it.
- **Stage every action** ("breaches 30 ft off the port side, crossing behind the boat left to right"): *"the model will not guess your blocking."*
- **Name the camera move** (push in, tracking, aerial pull back). "Cinematic" says nothing.
- **Never describe a person by text alone.** "Rugged 40s fisherman" came back with a famous actor's face. Use a photo ref plus a short voice clip, and keep the wardrobe text, because a headshot shows no clothes. *"Reference anything you can show, describe only what you can't."*
- **Product spot:** @-mention the pack ref wherever it appears, plus *"labels stay sharp and unchanged in every shot"*.
- **Credits:** draft at a shorter duration, confirm the beats and staging, then **render the full 30 s once**, with bitrate set to HIGH for finals.

**V4 · `YM_2PYIy0FA` · Jack Vs. AI · [How to use Seedance 2.5 for AI filmmaking](https://youtu.be/YM_2PYIy0FA) · 2026-08-07 · Higgsfield promo.**
- **Workflow:** story paragraph → list of characters, props and locations → sheets → a Claude skill writes a timestamped multi-shot prompt and **@-tags each ref at its first appearance**.
- **A 30 s fight scene in one generation worked** (weight of hits, prop orientation). The faults were eye-colour drift on the last shot and morphing in heavy motion blur.
- **The model doesn't foreshadow:** in a chase it cut straight to the cliff edge. Prompt the setups explicitly `[inf]`.
- **Too many refs** (wall photos, TV video, a Suno song, his own dialogue): run 1 swapped the character variant and dropped the music. **Rerun 2 of the same prompt** got the music and the prop. The voice match was hit-or-miss even on run 3.
- **"The 30-second trap":** don't generate 30 s just because you can, because retries get expensive. A whole 30 s TV ad in one generation *is* possible. Otherwise break at natural cut points. "You don't need 50 refs: a few sheets, location stills and a few audio refs."
- **720p cap:** use Topaz for pro delivery.

**V5 · `FJfMTvZvX7w` · Dan Kieft · [Seedance 2.5 transforms iPhone footage](https://youtu.be/FJfMTvZvX7w) · 2026-09-06 · Higgsfield affiliate.**
- **Video-to-video:** raw clip + new character image + up to 3 prop refs. His Claude skill views screenshots of the raw clip and writes the prompt.
- **The model fills gaps from the refs** (it added a light bulb, and the actor entered from the wrong side), so prompt everything that must match. Plain backgrounds help.
- **When recording:** use a tripod, show objects clearly, and **exaggerate the acting** (the model mutes it). Write physical events ("driver brakes, both passengers lunge forward"). One person can play two characters with a split-screen self-overlay.
- **Credit trick:** pre-edit 6 raw shots into one 30 s sequence and convert it in **one** generation. Redo a single bad shot with raw clip + ref + new direction.
- **Resolution:** test at 480p, deliver at 720p.

### 7.2 Higgsfield Cinema Studio and Marketing Studio

**V6 · `w3ntgJwdXKE` · Youri van Hofwegen · [How to actually use Higgsfield Cinema Studio](https://youtu.be/w3ntgJwdXKE) · 2026-04-22 · affiliate.**
- **Character mode menus:** genre, a **budget slider** ($10M–$500M sets polish vs raw), era, archetype, identity, build, hair, details, outfit. He quotes ~1/8 credit per character image vs 4 for NB Pro.
- **Recurring props** (cars) are made in General mode *before* any video.
- **Chaining:** the next clip uses the same 5 assets + **the previous clip as a video reference** + a short "what happens next". Mood and light carry over; 5 clips are stitched in CapCut.
- Speed-ramp presets: slow for tension, fast for urgency.

**V7 · `fmgVm-fxPDM` · Higgsfield (vendor) · [10+ beauty ads in 1 hour](https://youtu.be/fmgVm-fxPDM) · 2026-05-18.**
- **Chain:** logo (GPT Image 2, 4 versions) → product line with the logo attached → **brand-kit sheet** (palette, type, logo variants, texture, pattern, voice, tagline) → posters and billboard using the kit as a ref → Marketing Studio video.
- **Presets:** Hyper Motion (product + a Soul Cinema location as the 2nd input), Wildcard (character + product, "slightly uncanny"), TV Spot (character + location + ~5-word prompt; 16:9, 15 s).
- **Two avatars:** pick one and attach the second as a reference.
- The vendor claims ~$9 per commercial.

**V8 · `mAq_q4xs_aw` · Diego Galvão · [Product videos with Higgsfield Marketing Studio](https://youtu.be/mAq_q4xs_aw) · 2026-04-16.**
- **9 formats:** UGC, Tutorial, Unboxing, Hyper Motion, Product Review, TV Spot, Wildcard, UGC and Pro Virtual Try-On. 4–15 s, 4 credits/s, ≈$1.70 per 8 s clip on his plan.
- **Paste the product URL:** it pulls the name, features, price and all page photos. Add your own photos for **scale** (pouch, box). PDFs are accepted.
- **A blank prompt often works.** Unboxing failed twice (refunded) until *"Unboxes the headphones ASMR style. No dialogue or music."*
- **QC small physical details:** a stereo cable was plugged in on one side only.

**V9 · `cquR3FRWnzc` · Creating with Conor · [Marketing Studio is insane for UGC](https://youtu.be/cquR3FRWnzc) · 2026-05-18 · affiliate.**
- An Amazon link + preset avatar + empty prompt gave a 15 s UGC clip matching the listing. "Without owning the product" raises claims and legal risk `[inf]`.
- **Hyper Motion with no avatar** suits products the audience already knows.
- **Custom avatar** from a detailed text prompt (light direction, freckles, chain), saved as "Hugo" for reuse.
- **Product still in NB Pro** with exact angle, backdrop, light and **contact shadow**: "you're art directing a product shoot".
- **Same assets × 3 styles:** an Unboxing with **one dialogue line that carries the key selling point**; a Wildcard to *test a cinematic direction before a real shoot*; a Pro Try-On (multi-angle, multi-location in one clip).

### 7.3 Kling, voice, music

**V10 · `b_RghITuQQM` · Dan Kieft · [Master Kling 3.0 in 25 minutes](https://youtu.be/b_RghITuQQM) · 2026-02-24 · OpenArt affiliate.**
- **Prompt order:** camera → subject → action → environment → (light, texture, audio).
- **Multi-shot:** up to 6 shots inside 15 s from **one start frame**, with movement carrying across cuts. Multi-shot is not available with start + end frames.
- **Omni:** up to 7 refs; a 3-angle character ref from one NB prompt; *"image 1 and image 2 are in the location of image 3"*. **More refs mean more glitches.**
- **Lip-sync drifts after ~10 s:** put dialogue in the first 10 s and action in the last 5. An LLM loaded with the Kling guide can draft prompts, but rewrite them by hand (consistent with R6 in §1.3).

**V11 · `QKBwA8VWMAY` · AiHustleGame · [Kling AI 4.0: cinematic AI commercial](https://youtu.be/QKBwA8VWMAY) · 2026-10-04 · Kling creative partner.**
- **Spec ad with a twist** (the "intruder" a robot fights is the late boyfriend).
- **Refs for every recurring object** (headphones, couch, coffee machine, cup, phone) + the apartment + start images for key moments.
- **Ref declaration**, verbatim: *"reference one is the woman, keep her face and outfit consistent. Reference two is the robot, keep its armor and visor design. Reference three is the apartment, follow this layout. Reference four is the headphones, keep their color and shape."* Then state where each enters, where she looks, what the camera shows first and what the end reveals. *"If I leave those relationships vague, I'm giving up control."*
- **Editing:** 10 s generations, of which ~1–3 s are used. Review each before the next. Watch the full edit muted before adding sound.
- **Sound:** two sound worlds (her light music vs door, power-on, impacts, police) plus small sounds (machine finishing, cup set down, phone buzz).

**V12 · `WEyI3KL16Fs` · ElevenLabs (vendor) · [Eleven v4 is here](https://youtu.be/WEyI3KL16Fs) · 2026-09-30.**
- **v4 is for produced VO and dubbing;** v4 Turbo (~100 ms) is for agents.
- **Multi-speaker lines are generated in context** (overlap, timing, reactive energy).
- **Stacked tags are followed far more reliably than in v3.** Rule: **"write the script as prose first, then direct it"**. v4 reads punctuation and sentence length, so add tags only where the text gives no direction.
- **Instant clone from ~10 s of clean audio.** Speaker identity holds at any length and across regenerations.
- **Existing Professional Voice Clones must be retrained on v4** (Voice → My Voices → settings → Eleven v4).

**V13 · `vcpM4MRupNE` · ElevenLabs (vendor) · [Music v2](https://youtu.be/vcpM4MRupNE) · 2026-05-29.**
- Licensed training data, cleared for commercial use.
- Section-by-section composition, **inpainting any section**, SFX embedded in the track, mid-track genre changes.
- **Video-to-music** (upload the cut → a fitting bed); edit by instruction ("rework first 40 s…").
- "Residual roots persist": start with the genre you want.

### 7.4 Production business and strategy

**V14 · `ttgNFJ25xfU` · PJ Accetturo (Genre) · [Full AI film production workshop](https://youtu.be/ttgNFJ25xfU) · Wonder Studios · 2026-05-10 · 76 min.** The subject is a sci-fi trailer, but the process is his agency's.
- **Team:**
  - One pod per project: writer, director, several real DPs ("you can teach tools, not taste"), animators and one editor.
  - ~8 Midjourney artists work on **separate** boards; 2 are picked.
  - About 1 % of frames are used, and some become anchor images.
- **Image models:**
  - MJ for wides and odd worlds; NB Pro at **2K** for ingredients ("4K too smooth, strips grain").
  - GPT Image 2 is "most intelligent but crunchy and dark".
  - Compare by batching 20/20/20 across models.
- **Character sheet:** 3 panes at 16:9, with a **crisp close-up + outfit panes with heads cropped off**. The model takes the face from the close-up and the outfit from the body. Add movement and **voice descriptors**: Seedance has ~30 stock voices, and the descriptors pick one.
- **Voice lock:** upload a 15 s clip with every prompt ("this is how Adam sounds… make him say the text below"); a black-video version is more consistent. **Lip-sync to uploaded audio holds ~7–8 s, then hallucinates, so write dialogue in 8 s chunks.**
- **Two-person dialogue scene minimum:** 1 wide with both characters and their blocking + 2 reverse close-ups (OTS). Alternative: the empty room + character sheets.
- **Blocking trick:** the shortest Seedance generation (3 s) from the wide → screenshot the blocking → upscale in NB Pro → feed it back as the master blocking. Other ways to get location angles: a 360 equirectangular still, or a Seedance "slow 360 turn".
- **Claude project** holds the style guide and splits every script into **15 s Seedance segments**.
- **Rendering cost:** iterate ~5× at 720p, finals 2–3× at 1080p. His figures: **~$13–15 per 15 s at 1080p vs ~$3 at 720p**. Upscaling 720p→1080p never matches native. Avoid "fast" modes.
- **The opening shot is the hardest** (3 days, ~$1k). A hook is something known + something unknown.
- **Sound:** 90 % comes baked in from Seedance, always with "no music, sound design only"; music is added from stock.
- **Legal:** approval images in NB Pro (Google indemnification); run a copyright/lookalike check on the final; carry insurance.
- **Business:**
  - Cost-plus with a **~30 % margin** ("most AI studios ~30 %"), paid in deposits of 4 × 25 % or 50/50.
  - Artists cost $50–150/h.
  - "Ads will get automated", so he is moving to series and IP.

**V15 · `4wM-i1cxtAM` · Dara Denney · [I made 10,000 ads: what works (2026)](https://youtu.be/4wM-i1cxtAM) · 2026-09-28 · Modash-sponsored.**
- **Diagnosis before formats:** personas (who the ads target vs who writes the reviews) → a 1–2 sentence **diagnosis** of *why*. "Without it you only have testing."
- **Checks:** awareness mix (usually too little unaware or problem-aware); spend mix (images, video, carousel, partnership); 3–4 messaging pillars **carried through to the landing page**; whether creators match the personas.
- **Partnership ads should be 30–50 % of spend;** many brands are under 25 %.
- **Old problem-solution UGC "feels like an ad".** Formats scaling in Sep 2026:
  - personal-story "yappers";
  - authority;
  - educational breakdowns;
  - **investigative-journalism ads** (a creator investigates competitors and ends at the product), made fully with AI, with a claimed 77 % hook rate;
  - transformation and comparison (split screen, list of failed attempts).

**V16 · `t_a3rkBbVq8` · AI Foundations · [Claude + Higgsfield: automated marketing system](https://youtu.be/t_a3rkBbVq8) · 2026-07-08 · Higgsfield-sponsored.**
- **Set up Higgsfield MCP as a Claude connector.** Uploads become Higgsfield assets with media IDs; Higgsfield publishes downloadable Claude skills.
- **Project layout:** `CLAUDE.md`, `context/` (business overview, a POV doc written via "interview me", stories, voice samples), `templates/`, `.claude/skills/`, and routines.
- **A template = master prompt with placeholders + the model used + anchor images.** Build templates from past winners (the top 4 thumbnails all had a logo upper-left, so the template got a logo slot).
- **Iterate in plain language** ("orbs too present… subtle in and out").

**Skipped or brief:**
- `b-GhMZ_rcJM`: ElevenLabs v3 (Jun 2025), superseded by V12. It is still useful for its stability modes (Creative / Natural / Robust).
- `i-Y9I33e_WA`: Kling, 2024 (old).
- `zXlVQ8rMJM0`: Music v2.5 teaser.
- `iSrjS7jzREk`: video-to-music basics, covered by V13.

### 7.5 Not fetched (HTTP 429 / "IP blocked", 2026-10-08 02:20–05:00 UTC; two retries this session also hit 429)

**Still open from §5:** `W45T919iFxM`, `Z5HLzd97EKw`, `_r7NUcM41Kc`, `yRgPbqywUJ8`, `76KH-GZZ5w4`, `VkSOHGT_AMc`, `YUMg-1ArPvE`, `6eG3T-Esp4E`, `v_VICKllPLE`, `iOwKylW8c5Q`.

**New high-value candidates** (only the descriptions were read):
- Higgsfield `kFKpcCHkuPI`, 2026-10-07. Chapters include "stop characters switching seats", "fix scenes with blocking maps", "the 4-second product shot" and "widescreen → vertical without cropping the action".
- Higgsfield `jvkdHdeWICM`: 2.5 vs 2.0, every 2.5 clip a single 30 s generation, with a "catch" for 4K.
- Lundström `RwhsE-GydKc`: a donut commercial built with a "Shotlist Director" skill, with chapters on a "location flip" and a "music bug fix".
- PJ Accetturo on Wrapbook `kvDke-9Ifkk`: economics, margins, failed campaigns.
- Higgsfield `iOwKylW8c5Q`: a 24 h agency build including "a website that actually sells".
- Joseph Martin `T4NxZguv2dg`: Cinema Studio 4.0 at 1080p.
- Higgsfield `gVPZU1btFA8`: PROOF/QUEST copy frameworks and Reels as a free lead test.
- Theoretically Media `4wFBA9-KyzY`: a Seedance 2.5 short film with dialogue.

**Gap: website conversion for a creative studio.** No 2026 transcript on this was fetched in either round. Docs 29, 31 and 33 still rest on web sources. Fetch `iOwKylW8c5Q` first next time.

### 7.6 Adopt now (→ file each extends)

**30 s one-take product films (Seedance 2.5)**
1. **Prompt skeleton:** fixed camera header (body, lens, grain) → CAST block with @-tags at first appearance → FIRST FRAME → RULES (world and physics) → timestamped beats (subject / action / camera / audio, each staged in space) → DIALOGUE block → AUDIO block (in/out times, surfaces, "no music, sound design only"). → **16** §2.2 (raise the one-take from 12–15 s to 30 s) / **14** §1.3
2. **Beat budget:** at most one major action per beat; fill ≤ ~70 % of the duration with dialogue `[inf]`; if speech speeds up or lines garble, split into 2 × 30 s. → **16** / **22** §2
3. **Credit ladder:** draft at a shorter duration or 480p to check beats and staging → full 30 s at 720p once → **rerun the same prompt before rewriting it** → finals at high bitrate (1080p where offered). Budget $40–60 per 30 s (§1.3) and expect 3 runs to be mined. → **18** / **21** §4
4. **Mine, don't hope:** auto-split each take at its internal cuts (scene-detect) and cut the best parts of 3 runs. Open on action; same light grade and grain on every clip. → **16** §3 / **08**
5. **Label lock in long takes:** pack ref @-tagged where it appears + *"labels stay sharp and unchanged in every shot"*; still composite the real logo for the end card (§6 item 16). → **17** §2 / **16**

**Character consistency, Soul ID, two-character talking reels**

6. **Never cast by text alone:** every human needs a photo ref, because text-only descriptions drift toward celebrity faces. Keep wardrobe as text because headshots show no clothes. Sheets have a crisp close-up + headless outfit panes. Keep the existing Soul ID / M / anchor-block stack. → **30** §2 / **17**
7. **Voice lock per character:** a ≥10 s pangram per voice, exported as a **black MP4** and attached as a video ref (*"use @video1 as the voice of man A"*). Repeat each character's origin or accent in every prompt. For mascot VO, retrain any Professional Voice Clone on Eleven v4 and write "prose first, tags only where the text gives no direction". → **30** / **13**
8. **Two-character reel recipe:**
   - 1 blocking wide with both characters (a 3 s generation → screenshot → upscale → master blocking) + 2 reverse close-ups.
   - State left/right positions in every prompt.
   - Dialogue in 8–10 s chunks (lip-sync drifts after ~8 s in Seedance, ~10 s in Kling).
   - Cut between speakers to hide drift.

   → **30** / **16** / **14**
9. **Ref declaration sentence** for every ref ("reference N is X, keep Y"), plus an explicit relationship (who enters where, eyeline, reveal order). Cap refs at a few sheets + location stills + 1–2 audio refs. → **18** prompt builder / **16**
10. **Chaining fallback:** when one 30 s take fails, chain clips using the same assets + the previous clip as a video ref + "what happens next". → **16** §1

**Pipeline and product**

11. **Brand-kit sheet first** (palette, type, logo variants, texture, voice, tagline) as the ref for every still and poster in a client job. → **26** §2 / **17**
12. **Product-URL ingestion** into the asset registry (name, features, price, all page photos + an owner photo for scale). Marketing Studio blank-prompt runs serve only as cheap direction tests; QC small physical details. → **18** §4 / **15** §3
13. **Template = master prompt + model + anchor images**, built from past winners and stored as a skill. Set up `context/` with a POV doc written via "interview me". → **18**
14. **Iterate by timestamped notes:** muted watch → dictated notes → revised prompt → same-prompt rerun. → **18** QC loop / **21**

**Strategy, pricing, studio**

15. **Diagnosis sentence before concepts** (persona gap, awareness mix, pillars carried to the landing page). Add investigative-journalism and personal-story formats to the concept menu, and drop generic problem-solution UGC. → **15** stage 0–1 / **23** §6
16. **Pricing:** cost-plus with a ~30 % margin and 50/50 or 4 × 25 % deposits as a cross-check on our rates. Approval stills from an indemnified model, a lookalike/copyright check before delivery, insurance. → **28** §8 / **32** §2 / **34**
17. **Website (studio):** no new transcript evidence this round. Keep 29/33 as they are, and carry forward one rule from V15 `[inf]`: **the 3–4 messaging pillars in the ads must reappear on the landing page**, so the hero reel's promise and the first screen's headline should match. → **29** §2 / **33** §2
18. **Do not adopt:** unofficial model builds, renaming trademarked props to pass filters, or "without owning the product" UGC claims. → **21** §1
