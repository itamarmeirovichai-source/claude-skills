# 14 — Rourke Heath study: how he makes AI videos and ads, what he teaches

Researched 2026-10-07. Rourke Heath (legal name **Rourke Sefton-Minns**) has about 266k followers on TikTok and 975k on Instagram. He founded **GenHQ** (Skool, about $97/month); his mission is "100,000 jobs for creatives". All numbers are his own claims or third-party estimates.

## Sources

**Downloaded, watched and transcribed: 19 TikToks.** Frames are in `research/ai-video-reels/youtube/frames/rourke/` (git-ignored). Each video has a 12-frame sheet `<id>.jpg` and a 0–3 s hook strip `<id>_hook.jpg`. URL pattern: `https://www.tiktok.com/@rourke.heath/video/<id>`.

| id | views | what it is |
|---|---|---|
| 7644992952732847382 | 71.8M | Gemini Omni at Google I/O (paid) |
| 7598684896940526871 | 66.8M | Artlist casino transitions (NB Pro + Kling start/end) |
| 7594831767220129046 | 1.0M | Fake webcam UGC (Freepik, NB Pro, Veo 3.1) |
| 7554308385525648662 | 413k | 3D product transition (NB, Kling 2.1, AE ramps) |
| 7672883155010866454 | 381k | "AI Agents" skit |
| 7595884825744018710 | 362k | Higgsfield × Kling prompt cards |
| 7668365334692384022 | 333k | "AI looks too perfect" skit |
| 7640207147153804566 | 271k | Claude + Higgsfield CLI prospecting pipeline |
| 7677204754371513622 | 172k | "Slopwarts" parody (Seedance 2.5) |
| 7563602837712719126 | 154k | Arcads + WAN Animate ads |
| 7541706819090025750 | 92k | Annotated keyframe → Veo |
| 7670572625147694338 | 88k | Dreamina Seedance 2.5 long ad |
| 7624076873278016790 | 48k | Seedance product ads from phone snapshots |
| 7690767051098672387 | 35k | Kling 4.0 skit |
| 7576597210339511574 | 31k | Block prompting (Sora 2) |
| 7690206803308678422 | 26k | 34 shot types |
| 7668075872590531862 | 26k | Hook factory (Claude MCP) |
| 7686175102009953558 | 24k | Consistent voices (ElevenLabs) |
| 7667213190861688086 | 7k | $1 vs $1,000 commercial |

**Also read:** the captions and stats of all 239 public TikToks (May 2025 to Sep 2026; median 46 s, about 63k views), plus 5 Instagram captions.

**Podcasts, transcribed with faster-whisper:**
- *The AI Download* (Shira Lazar), "How This Creator Publishes 97 Posts a Month…", 16 Oct 2025, full: https://media.transistor.fm/9ff9f6fa/eb7fbced.mp3
- *Fast Hours* Ep 78, "He Built an 8 Figure AI Business in One Year", Jul 2026, 33:00 to the end, plus the show-note chapters. Feed: https://anchor.fm/s/f84d7f94/podcast/rss

**Articles and profiles:**
- https://www.netinfluencer.com/how-rourke-sefton-minns-built-genhq-into-a-creative-learning-hub/
- https://www.skool.com/genhq/about
- https://creatordb.app/creatorstats/rourke/
- https://motionapp.com/creator/rourke-heath/

**Could NOT access:**
- **YouTube** (bot-blocked for video and subtitles): "From Freelancer to AI Agency: How to Get Clients, Price Work & Scale" (Uuvlqe2R06M), the Seedance 2.5 film tutorials (MY6f9xnYOwU, H0Ahmz2xuvs), the Upscale Conf talk "Get Hired. Get Paid." (iuC7s-nm1TA), the Bad Decisions Studio interview, and the Fast Hours video (its audio was used instead). Y0TnC-uZ6k8 is unavailable.
- **Instagram:** reels, stories, and the ManyChat-gated prompt PDFs.
- **GenHQ paid modules:** pricing and negotiation, contract templates.
- **alici.ai:** 403.
- **Fast Hours 0–33 min:** biography; I used its chapters only.

## His formats (what the frames show)

1. **Talking head at the bottom, visuals on top (the default).** He sits in a rounded cut-out in the bottom ~35% with the result or UI above; the cap and white tee are a recognisable "uniform". Visuals are edited FIRST, unscripted. He then narrates while the timeline plays under the camera, matching its tempo. Each reel takes 8–11 h, done in one day.
2. **Result first, method second.** 0–3 s is the finished AI result, often with him inserted, plus a sticker ("This is AI? 😳", "AI is getting too realistic 😳"). Then the tool UI, the prompt card and the start/end frames, then a big "Comment 'AI'" card over the PDF.
3. **Side-by-side proof.** "Original / AI", "Image Reference / output" and "Start Frame / End Frame / Final Product" labels stay on screen while the clip plays.
4. **Narrative skits (the 2026 shift).** Short films with him and friends, a warm film grade, and small yellow serif subtitles. Some are real footage ("AI looks too perfect", "AI Agents"); some are fully AI with him as the lead (Seedance beach ad, Kling 4.0 cop scene, Slopwarts). They use a **narrative loop**: the ending explains the opening, and the tool is the punchline ("You were using three references, Kling 4.0 lets you do 15"). He says this format cured his burnout and he is hiring a scriptwriter.
5. **Listicles** ("34 shot types": a numbered list builds while example images flash in an inset).
6. **Price-ladder hook:** "$1 vs $100 vs $1,000 AI commercial". A real pizza box reveals AI floating ingredients.
7. **Event reportage:** a Google I/O keynote filmed from the audience, with his face cam below. This was his biggest post (71.8M, paid).

**Pacing and CTA:**
- A new visual every ~2–4 s; dense speech (a "30-second" tutorial runs 40–55 s).
- Inspiration pieces are "generations with subtitles, sound design, a slight colour grade".
- Clean top titles; no word-by-word captions on tutorials.
- Almost every post ends "Comment 'AI'". ManyChat then DMs a PDF of "all our prompts and images", which pushes to YouTube or GenHQ. Stories with a keyword get up to 8,000 replies and about 100k views on 600k followers.

## His workflows, step by step

**A. Start/end-frame product move** ("Kling first/last frame in almost all our videos").
1. Hero image: Midjourney or Nano Banana Pro with a product ref plus a background ref.
2. Feed that image back to Nano Banana for a second angle or a macro of the same scene. This is the END frame.
3. Kling (2.1, then 2.5, then 3.0) with start and end frames. To chain, the last frame becomes the next first frame.
4. In After Effects, join the clips and speed-ramp the seams. This makes the "3D product transition" (the Sony camera exploding into parts).

Kling prompt card, verbatim (a pendant):

> "The camera orbits from left to right, keeping the pendant in the centre of the frame at all times. the pendant does not move, it does not wobble, it does not change direction or spin. nothing in the frame moves except from the camera."

**B. Product into a scene with annotated keyframes** (Veo / Google Flow).
1. Midjourney scene, plus a photo of the product (Google Images or your own phone), plus a photo of the packaging.
2. In Photoshop, composite them on one board and **draw red arrows and handwritten instructions on the image**. On screen: "The drone flys down from the top of the frame and then the camera pans down revealing the DJI neo box on the table. Remove all arrows and white…"
3. Upload that annotated board to Flow, "Frames to Video", with a basic prompt.

**C. Seedance product commercial from a phone snapshot** (Higgsfield Seedance 2.0).
The only ref is a casual phone photo of the product in a hand. The output is a black-void hero film. Prompt, verbatim (sneaker):

> Camera Simulation: 65mm IMAX film, ultra-wide Panavision anamorphic lens. Strong film grain throughout. Horizontal anamorphic lens flares triggered by reflections on rubber, mesh fabric, and the glossy logo. Hard directional key light from camera-right — punchy, high-contrast. Deep black void. Cool blue rim light from behind creates edge separation. Lighting shifts from cool and clinical on raw materials to warm golden as the shoe completes.
> Single continuous 7-second shot. No cuts. The camera spirals, dives, and pulls back constantly as the shoe builds itself from raw material to finished product.
> 00:00–00:01 · Raw Thread — Extreme macro — a single polyester thread floats in the void, multiplies, and begins weaving itself into a hexagonal knit pattern. The camera spirals slowly around the forming mesh.
> 00:01–00:02.5 · The Upper — Speed ramps to 150%. The upper wraps into a three-dimensional foot form — toe box tightens, midfoot panel forms with visible density gradients, heel counter locks rigid. Colour bleeds through the mesh from toe to heel. The camera sweeps underneath as the foam footbed materialises, thousands of tiny bubbles inflating simultaneously.
> [00:02.5–00:04 Midsole, "Speed drops to 30%…"; 00:04–00:05.5 Outsole, "Speed ramps to 120%…"]
> 00:05.5–00:06.5 · The Reveal — Speed drops to 20%. The camera settles into a classic three-quarter angle — shoe floating fully built. The lace ties itself in slow motion as warm golden light washes over. Every material reads clearly. Hold.
> 00:06.5–00:07 · End Card — Hard cut to black. Minimal white logo fades in, centred. Below it: "Built in motion." Film grain. Hold.

Lovart variant: cheap Nano Banana 2 refs, then "Use these reference images to create a cinematic advert for a burger…" (Seedance, 9:16, 5 s, 1080p).

**D. Multi-reference Seedance scene with @-tags** (from his Claude prompt-log.md). Every reference is declared with a scope, then the scene, then a CUT list:

> @m1_charsheet - Character ref. Lanky male model, shoulder-length shaggy dark curls… Character only.
> @m1_detail - Detail ref. Oversized structural hybrid parka… Character and outfit only.
> @env_crimson_spires - Environment ref. Alien crimson red volcanic spire formations… Environment only.
> Scene: A field of alien crimson volcanic spires… @m1_charsheet moves through them — scrambling, climbing…
> CUT — extreme wide low angle… @m1_charsheet is a small figure weaving between them at the mid-ground, the scale crushing.
> CUT — extreme close face… He looks like he belongs here.

**E. Consistent character voice** (ElevenLabs + Seedance 2.5).
1. Claude reads the character sheet and writes a voice persona. Verbatim: "A woman in her late thirties with a low, gravel-scarred voice — raspy from years of dust, smoke and cheap liquor. British-tinged accent, slightly clipped Victorian cadence worn down by rough living. Dry, wry, unhurried delivery…"
2. Paste it into ElevenLabs Voice Design and pick one of 3 voices.
3. TTS a **phonetic pangram** so the reference covers every English sound ("That quick beige fox jumped in the air over each thin dog. Look out, I shout, for he's foiled…").
4. Claude turns the mp3 plus the character and location refs into timecoded SHOTs. Verbatim: "SHOT 3 (00:04.6–00:05.0) – Resolve. EFFECT: Stillness hold + subtle screen bloom pulse… Camera still locked. No movement. Real time. The shot simply ends – no fade, no flourish."
5. End the prompt with: "@voice1 is the voice of @character. @voice1 is a reference only, match this female voice's timbre, tone and accent."

**F. Realistic AI UGC.**
1. Freepik Spaces character from a mundane prompt ("A photorealistic video-style shot recorded in the evening, of a girl, 22, seated…"): posters, a plush toy, a phone showing the real time.
2. Nano Banana Pro puts the product in her hand ("keep the scene the same but give the girl the makeup pen…").
3. Veo 3.1 start/end frames, chained ("like adding makeup layer by layer").
4. Arcads variant: film yourself holding the product, screenshot it to create a new actor, then WAN 2.2 Animate drives it with your performance.

**G. Hook factory** (Claude + Higgsfield MCP). Screenshot frame 1 of a real iPhone intro. Ask Nano Banana 2 to "restyle it with an element of danger inside the scene but keep the composition the same". Seedance 2.0 animates it with the original clip as the motion reference, "for under $5".

**H. Automated spec-ad prospecting** (Claude + Higgsfield CLI).
1. Feed in a location, a character and a product. Claude makes hundreds of image variations, logged to a spreadsheet as Pending/Approved/Rejected, and "learns from your feedback".
2. Approved frames become Seedance 2.0 adverts.
3. Claude drafts and sends a Gmail with the video attached to prospects.
4. His caveat: "Claude needs very specific instructions to create content tastefully" (two weeks of build, two years of prompting knowledge).

**I. Block prompting.** A custom GPT turns a product image into a structured "block prompt" for Sora 2 Pro on Artlist. Visible (Apple Watch Ultra):

> "APPLE WATCH ULTRA — Subject / Scene Settings - Audience: {locale:"GLOBAL"; tone_note:"premium athletic grit; crisp kinetic elegance"} - Reference images: [] - Subject type: product + human … - Key features: extreme-close titanium chassis glide; gloved hands cinching tight; … final pristine hero float; Scale: human against colossal mountain; Motion: slow macro dolly; glove flex; … - Lighting: sunrise gold key; cold blue rim from snow; soft macro speculars on titanium; … - Grade: cool arctic blues + sunrise amber + signature Ultra orange; restrained bloom; ultra-fine grain - Visual taste: hyper-polished realism; luxury documentary tone - Camera: ECU↔WS interplay; center→rule-of-thirds; product-friendly parallax; gimbal glide …" followed by Audio (BGM/SFX with timed cues) and Dialogue/Subtitles blocks.

**J. Long single-prompt ads.** Dreamina Seedance 2.5 takes up to 50 refs and runs 30 s to 3 min "from opening hook to final logo without stitching". Kling 4.0 Flash takes 15 refs, start + 8 mid + end frames, and runs 30 s.

## Prompt patterns he uses again and again

- **Scope every reference** ("Character only", "Environment only", "reference only, match timbre…") and give it an @handle.
- **Timecoded beats with speed instructions inside the prompt** ("Speed ramps to 150% / drops to 20%"), and an explicit "Hold" on the reveal.
- **Lead with a camera simulation:** format, lens and grain ("65mm IMAX film, Panavision anamorphic, strong film grain"). Name the key light's direction, the rim colour and a lighting arc (cool to warm as the product completes).
- **Product lock for camera moves:** "nothing in the frame moves except the camera" and "does not wobble… spin".
- **An "end card" beat inside the generation:** hard cut to black, logo, a 3-word line.
- **Mundane-realism prompts for UGC:** a time of day, a real age, a cluttered room, a phone showing the clock.
- **Shot vocabulary list** (34 types, PDF via comment): beyond the standard sizes and angles it includes prism reflection, inside-a-hole, hoop-level, foreground occlusion, magnifying glass and inside-the-fridge.

## Business lessons (what he says)

- **Revenue (self-reported, Jul 2026):**
  - Brand partnerships with AI-tool companies: $350–600k/month, "+20% month on month".
  - GenHQ: about $150k/month, mostly reinvested. About $40k/month of Meta ads only holds the member count, because churn is high.
  - Consulting (Vans, The North Face, Timberland), client ads (a team of 12), and a coming hiring marketplace with $500–10k gigs.
  - He declines 90–95% of deals and anything off his "100k jobs" North Star, which he uses as a cut rule.
- **Production tiers:**
  - A: 1 day, ~15 person-hours, no filming.
  - B: 2 days, filmed, with After Effects.
  - C: up to a week of R&D on a new tool.
  - Ideas go on a vibe-coded "raw ideas" board where **the first frame** and the flow are sketched first. The goal: "the minimal easiest thing to explain verbally and visually".
- **First-client playbook:**
  - "Find the bloody client first", then figure it out.
  - Make 2 spec commercials a week for 12 weeks (24 ads), each tagged "made on Higgsfield/Magnific…", then apply to that tool's **creative partner program** for subsidised credits.
  - Post a LinkedIn "how I made it" for each ad. He calls LinkedIn the most untapped source of gen-AI work.
- **Jab, jab, jab, hook:** make 4 spec pieces for one brand, then DM a decision-maker on LinkedIn. Connect with the brand's employees first, and mirror their job listings.
- **Boring categories win:** vacuums, blenders, fishing, water (Dyson explosion).
- **Brands:** they don't know what they want ("just make a video about Gemini"), and "they always have budget". Reliability on 24–48 h deadlines brings repeat work.
- **Skills that get you hired:** editing and "what shot comes next", over tool knowledge. GenHQ runs weekly fake-client briefs ("I'm Renault") with $100–1k prizes.
- **Taste is the moat:** "Making something good has never been easier, which is exactly why it stopped feeling like an achievement… let the imperfections do the work."
- **Untapped opportunity:** brand-sanctioned AI fan content, with royalties.

## On specific tools

- **Higgsfield:** his main paid partner (Kling 3.0/4.0, Seedance 2.0 4K, Soul Cinema, Mood Boards, Color Transfer, Shots, speed ramps, relight, a Premiere/After Effects plugin, MCP/CLI).
- **Seedance:** "leads the field on motion realism, acting nuance and camera control". He uses it for long prompts, multi-ref, audio-referenced voices and video-to-video restyles.
- **Kling:** start/end since 2.1; Multi-Shot in 3.0; 15 refs, mid-frames and 30 s in 4.0.
- **ElevenLabs:** Voice Design.

## 15 things we should copy now (mapped to our pipeline)

1. **Timecoded single-shot "build" prompt** (C): camera simulation → beats with % speed → Hold → end card. Make it a template in 12-higgsfield-mastery §4 for `seedance-2.5/reference-to-video`, so the speed ramps happen in-generation.
2. **Casual phone-snapshot product refs** for Seedance hero shots. Benchmark the cost against Flare stills.
3. **@-scoped reference declarations** ("Character only / Environment only / reference only, match…") in every multi-ref prompt and in the hfgen plan templates.
4. **The Kling product-lock sentence** on every orbit, with start and end frames as two angles of the same still.
5. **Chained start/end frames**, with reel-studio speed ramps at the seams. One continuous "impossible camera" BIG IDEA move.
6. **Annotated keyframes:** arrows and notes on the still, plus "remove all arrows and text". Test on Kling and Seedance.
7. **Voice pipeline (E):** persona → Voice Design → pangram TTS → Seedance audio ref. Add it to 13-elevenlabs-mastery.
8. **A "lighting arc" line** (cool/clinical → warm/golden as the claim completes) in every beat map.
9. **Shot-variety QC** in `director.py`: ≥5 shot types per 20 s, including one odd angle (foreground occlusion, inside-the-fridge, prism).
10. **A "frame 0" sketch** in brief step 4. Design the scroll-stopping first frame; don't pick it afterwards.
11. **Hook factory (G):** one opening plate, 5–10 composition-locked "danger/wonder" restyles, animated at 480p, A/B tested, then the winner at 1080p.
12. **Spec-to-prospect loop (H):** 4 spec pieces per target brand plus LinkedIn "how it was made" posts, then a DM on the 4th. Start with boring categories.
13. **Per-image approval log** (Pending/Approved/Rejected plus a reason) in each job folder, fed back into the prompt lock.
14. **Narrative-loop BTS reels for our own channel**, with a comment-keyword CTA and a DM'd prompt PDF as the lead magnet. Portfolio only.
15. **Imperfection on purpose:** mundane-realism prompts for UGC, plus one real iPhone plate where it helps (matches 06).

**Don't copy:** the talking-head tutorial format (our client bans talking heads), or the "hyper-polished realism" look without our film chain.
