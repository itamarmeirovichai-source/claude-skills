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

---

## Appendix — second pass: 60 more videos (7 Oct 2026)

**Method.** TikTok's web `api/creator/item_list` (paged by `cursor`, `type=1`, with the profile `secUid`) returned **597 posts (25 Feb 2024 to 29 Sep 2026)**; the 2024 ones are mostly Photoshop tutorials. I ranked the 2025–26 posts and processed 60. Each got a 12-frame sheet and a 0–3 s hook strip (in `frames/rourke/`), a faster-whisper `small` transcript, and prompts read from the sharpest 1080p frame, which recovered prompts flashed for under 0.5 s. Videos were deleted afterwards.

**Still inaccessible:**
- The ManyChat/GenHQ PDFs. I only saw pages that flash on screen.
- Prompt text cut off by scrolling or blur (marked "…").
- YouTube, Instagram and the paid GenHQ modules (same as the first pass).

### A1. Per-video notes (views; ★ = fully AI narrative skit)

| id | views | teaches |
|---|---|---|
| 7584133570223000854 | 21.2M | Meta AI app: free image of yourself plus lip-sync. kinetic one-word titles over a striking still |
| 7490631159525739798 | 9.9M | Artlist video generator (paid). **his own name on products** ("ROURKE" whiskey) |
| 7613917806354074902 | 9.4M | Luma agent motion graphics from storyboard frames; the agent self-critiques and regenerates |
| 7559508562632772886 | 2.9M | WAN 2.2 Animate: 3 synced rows (him / two celebrity look-alikes) |
| 7643610189072993558 | 1.9M | Google Omni hotel-room edits. **48 s of Omni/Original stack, no UI, no face cam** |
| 7532781319512673558 | 1.8M | JSON prompting for Veo 3 ads (Dyson, Rolex, Nespresso) |
| 7472782506345893142 | 1.6M | Midjourney `--cref` with `--cw 100` (lower = more drift) |
| 7599707454561176854 | 1.2M | Lovart 3D posters: NB Pro, text edits, Expand, then video "the man leans out of the white frame…" |
| 7545424480265325846 | 1.2M | Nano Banana in Photoshop (selection → File › Scripts) |
| 7474895772232846614 | 1.1M | Spec ads for real brands: Pinterest → MJ style-ref → Magnific → Kling → AE logo |
| 7614164104609139990 | 1.0M | Beeble SwitchX: Smart Select, NB Pro relights frame 1, feed it back |
| 7680953903596293398 | 674k | Higgsfield **Genjutsu**: source video plus char sheet swaps person or place |
| 7644675286654651670 | 652k | Beeble nodes: Exact Frame → GPT Image 2 restyle → Video Matte → SwitchX |
| 7683918425810324758 | 525k | GPT-6 Astra builds editable AE motion graphics (Higgsfield plugin) |
| 7647600662200487190 | 462k | Higgsfield Premiere/AE plugin: draw-to-replace, floating text |
| 7657598688323292448 | 327k | Gemini Omni Flash on Higgsfield: London "snap-finger" VFX walk |
| 7573741609867611414 | 326k | Midjourney still → NB angles → Kling 2.5 Turbo start/end |
| 7689501229155732758 | 316k | CCTV → cinema (Seedance 2.5 in Magnific plus Claude shot list) |
| 7608223175020793110 | 258k | Spaces + chained Kling 3.0 start/end day-in-life; assistant node lists shots |
| 7596241319811484950 | 257k | Arcads UGC → NB Pro → chained Veo 3 start/end |
| 7568799569803365654 | 239k | Freepik Spaces node basics |
| 7636798596867837206 | 229k | HyperFrames + Claude Code motion graphics (`npx hyperframes add instagram-follow`) |
| 7677215712053644566 | 204k | ★ Magnific **3D Scenes** grey-box blockout → Seedance 2.5 |
| 7600452922362596630 | 174k | Spaces: plain prompt → auto-JSON → Kling FPV one-take |
| 7603035402626174230 | 165k | ★ Kling 3.0: multi-speaker from one image, 15 s |
| 7636426497107987734 | 148k | ★ "ROURKE HEATH: AI DOCUMENTARY" Netflix parody |
| 7522834362191121686 | 138k | MJ moodboard codes for brand consistency |
| 7684717461681261846 | 117k | GPT-6 grades in DaVinci (node order below) |
| 7673921613997378838 | 114k | Zombie v2v (Original / AI / BTS); "$25/gen, $400 total" |
| 7628589780246252822 | 109k | Spaces + Seedance 2.0 McDonald's car-vlog UGC |
| 7642432421480221974 | 105k | Grok extend: paper-plane-to-dog one-take, 30 s |
| 7647063839963401494 | 98k | Higgsfield CLI in Claude Code: 100s of labelled product videos |
| 7627157538995211542 | 94k | ★ OpenArt Seedance 2.0 short, features as title cards |
| 7630932381842574614 | 91k | ★ Artlist rocket skit; "out of credits" punchline |
| 7624496288658165015 | 88k | Dreamina first/last-frame transitions from iPhone footage |
| 7575196783576452374 | 85k | NB Pro → Kling 2.5 football ad; Premiere seam trick |
| 7658984648751582497 | 84k | Magnific MCP connector inside Claude |
| 7668836781755829536 | 83k | ★ Seedance 2.5 Roman skit; "50 refs" gag |
| 7679103370690317590 | 81k | Lovart Seedance 2.5 re-angling one locked shot |
| 7629295347210128662 | 67k | Claude Code drives Arcads → Seedance UGC |
| 7603468163963096322 | 64k | Kling 3.0 Multi-Shot and image binding |
| 7687263863380757782 | 56k | v2v composite master prompt; $1.40 per 480p test |
| 7611608282507037974 | 56k | Higgsfield Color Transfer (extracts hex palette) |
| 7521667636879494422 | 56k | ElevenLabs Voice Design: Loudness and Guidance sliders |
| 7501306492352728322 | 154k | Tool stack with prices (MJ $15, Kling $15, Magnific $40/mo) |
| 7597930221542575382 | 51k | Camera moves: macro zoom, snorricam, rack focus, crash zoom |
| 7613422952138198294 | 47k | Kling 3.0 "moon landing" selfie UGC, green-screen twist |
| 7621994474574548246 | 46k | Artlist music; funk-prompt PDF |
| 7529894056332184854 | 45k | Regional Nike ads (Veo 3 variables) |
| 7637534150773181718 | 43k | Seedance 2.0 creature short, prompt under every shot |
| 7606037021659811094 | 38k | Spaces product pipeline: components → persona → location |
| 7606677879937617174 | 31k | Cinema Studio 2 in-generation speed ramps |
| 7642049151227759894 | 24k | Seedance voice lock via "black video" audio ref |
| 7670279584813714721 | 19k | Claude writes the sound design → Seedance 2.0 audio pass |
| 7581426097229729046 | 16k | Kling O1 label swap for localized variants |
| 7668075636015090966 | 15k | depth map + restyle + char sheet → Seedance |
| 7642811995997228291 | 12k | Essay: "AI is a mirror" |
| 7640808921422220566 | 12k | "Claude on trial" skit (anti-doom) |
| 7583004980689358102 | 115k | Higgsfield Shots: 9 angles for 4 credits |
| 7592277750224801046 | 73k | "Go inside the product" (Pixel); Veo 3 plus AE time-remap |

### A2. Verbatim prompt templates

**Seedance 2.0 / 2.5: video-to-video composite (master-footage lock)** (7687263863380757782)
> "Create an 8-second, 16:9 cinematic video in one continuous shot. video1 is the master: this is a VFX composite ON TOP of video1. Camera, framing, angle, perspective, distance, handheld drift and every movement of the man are exactly video1, frame by frame — nothing about him or the camera is changed, added or re-timed. The room stays the room of video1… except for the changes below. No cuts, no mirroring. THE ONLY CHANGES from video1: 1. The bed and the furniture on the right are removed… 2. The whole front wall with the window and curtains is gone, smashed open… Through the opening, right where the window was and at the same distance, a floodlit football stadium at night in the look of image1… 3. The man wears the kit from image2… Cap, face and hair stay exactly as in video1. 4. … 5. The crowd… erupts when the ball hits the net… Realistic, never looking at camera. video1 @IMG_5103 = master footage: camera, perspective, distance, room and performance preserved exactly. image1 @[location reference] = look reference ONLY for the stadium, goal, keeper, crowd and lighting. NOT a start frame: its angle, perspective, distance and composition are never used… image2 @[character sheet] = kit reference only (face and cap from video1). Photoreal, seamless compositing, matched lighting and grain… no digital sharpness. AUDIO: original sounds from video1, plus stadium ambience… NO music."

**Seedance: camera package plus named grade** (zombie, 7673921613997378838)
> "Arricam LT, Cooke S4/i primes, 35mm Kodak Vision3 500T, 1.85:1 spherical, T2.8, shallow depth of field, halation on highlights, fine organic grain, lifted milky blacks, low contrast, no sharpening, no HDR. Ash Rust grade: sun-bleached rust-red as the hero tone, bleached concrete-beige field, cracked grey asphalt base, warm brown falloff shadows that never reach pure black, dry drifting dust haze in harsh sun. Handheld with micro-drift, never locked off. Naturalistic performance, real dialogue sync, no music."

It also uses prop guards ("it never leaves his grip, never floats free"), a dialogue lock ("same words, same cadence, same tone") and paced threat ("closing gradually and visibly… rather than arriving all at once"). Settings: refs @img1–5 plus @vid1, 720p, **duration = source + 1 s**, 16:9.

**Seedance 2.5: re-angle one locked shot** (Claude output, 7679103370690317590). The input is a timecode list ("00:00 Tracking shot to Rourke / 03:07 Close up slow motion / 05:03 Low angle / 06:14 Top down shot / 08:14 Extreme close up / 14:00 Camera inside the cup / 15:22 tracking shot of the lemonade jug / 20:06 Dolly zoom / Keep the location, dialogue, and actions identical"). Claude's output:
> "[00:00-02.37] Shot 1: Rourke from @Video1 speaks to camera behind the lemonade stand, same performance and dialogue. Straight-on eye level, slow zoom in. Standard prime. Harsh midday sun. Handheld micro-drift easing forward. Hard cut to Shot 2. … [13.07-15.40] Shot 6: The lemon wedge from @Video1 squeezes toward the lens… as if the camera sits inside the cup. Extreme macro POV. Handheld micro-drift. Hard cut to Shot 7."

The CCTV version says per shot: "SHOT 1 (0:00–0:0X) — [TITLE]. [Camera position, lens, blurred foreground elements, what the subject does EXACTLY as in video1, where the focus goes.]".

**Seedance 2.0 / Dreamina: first/last-frame transformation** (7624496288658165015)
> "SHOT 1 (00:00–00:02) — Key Drop EFFECT: Speed ramp (acceleration) + shallow depth of field. … Keys land on the rug at approximately 30% speed. SHOT 2 (00:02–00:04) — First Transformation Pulse EFFECT: Morphological growth (mechanical assembly) + digital zoom (scale-in) + light refraction… SHOT 3 (00:04–00:06) — Macro Assembly Detail EFFECT: Extreme close-up macro + slow-motion (approximately 20% speed) + shallow focus… This is the SIGNATURE VISUAL EFFECT — precision engineering assembling itself from nothing. … SHOT 5 — … The colour of the original keys carries through into the motorcycle's yellow livery — visual continuity from the original object… SHOT 6 (00:10–00:13) — Final Hold EFFECT: Slow-motion settle (approximately 40% speed) + shallow depth of field + ambient light bloom."

**Seedance 2.0: multi-shot character short** (7637534150773181718; Seedance 2.0, 16:9, 1080)
> "10s cinematic CGI, multi-shot, awakening and first contact. CREATURE: palm-sized tarsier, powder-blue fur, golden-yellow chest, massive amber eyes that can well with tears, pink ears, tiny pink hands, ringed tail. ROCKY: 32, curly brown hair, full beard, white t-shirt, cream-sage VANS cap. LOCATION: ancient rainforest, soft golden morning light, ferns. (0–1.5s) REVERSE CLOSE: opposite-angle lick — creature with tongue extended on Rocky's bearded cheek, eyes closed in trust… (1.5-2.5s)…"

The brand plant: a notebook with a gold "GEN HQ" cover.

**Seedance 2.0 UGC (Arcads, written by Claude Code)** (7629295347210128662)
> "OPENS on girl slightly off-center, right arm already reaching outside frame — t-shirt not yet visible. She pulls arm back in one smooth continuous motion → yellow Vans t-shirt enters frame with her hand → she glances at it briefly → eyes back to camera. Natural smile building. Delivers casually, energetic: "Fuck, I can't believe Claude and Arcads made all of this!" Slight head movement with the words, not locked to camera. No overacting. ENDS holding t-shirt close to face → slight wink + kiss expression."

The character sheet is "Six views arranged in a clean grid on a pure white background".

**Seedance 2.0 audio-only pass (sound design written by Claude)** (7670279584813714721). The settings are the cheapest: 480p, 15 s, 9:16, bitrate High, the source video uploaded.
> "A premium event-recap reel, 10 seconds, vertical 9:16, 30fps… Tone: cinematic, confident, expensive, energetic but controlled… The source file carries no audio; every element is built from scratch. SHOT-BY-SHOT MAP — every audio event lands on the frame stated. SHOT 2 — 1.85 to 3.20 — Cut on 1.85 with a soft low thump and a light high transient over it. Ground foley drops away instantly — he is off the deck… SHOT 3 — … Impact carries weight and stops clean — no long tail, no boom. … SHOT 7 — Cut on 6.85 and drop the floor out — the mix pulls in close and quiet… Let the near-silence do work here. LAYERS TO BUILD: AMBIENCE BED… MOVEMENT DESIGN… TRANSITION HITS… PERFORMANCE FOLEY… No sound implying movement that is not onscreen… Each cut carries exactly one transition hit, no stacking. Interior and exterior ambiences never overlap; the changeover happens on the cut frame."

**Seedance voice lock.** Strip the picture from a clip of the character talking, leaving a black video with audio. Upload it as a reference next to the character image, then prompt the model to use the voice from the black video (7642049151227759894).

**Kling (Spaces auto-JSON, FPV one-take, 10 s, 1080p, 800 credits)** (7600452922362596630)
> {"sequence_type": "text_to_video", "duration_seconds": 10, "camera": {"perspective": "embodied_flying_pov", "lens": "ultra_wide_angle", "stability": "controlled_instability", "motion_style": "fast_aggressively_piloted", "platform_visibility": "none"}, "motion_rules": {"constant_speed": "extremely_fast", "no_hovering": true, "no_stopping": true, "no_ease_in_out": true, "always_moving_forward": true, "banking_includes_roll_and_pitch": true, "micro_corrections_and_overshoot": true}, "movement": {"start_action": "very high speed nighttime entry above a busy city street, immediate dive between lanes of traffic", "path_beats": ["squeeze between two speeding cars, headlights streaking, inches from bumpers", …], "end_action": "…"}, "environment": {"space_variety": "multiple distinct spaces within one shot", "geometry_proximity": "frequent inch level near misses with walls, vehicles, signs, windows and doorways", "avoid_empty_air": true}, …}

**Nano Banana / Freepik / Higgsfield image nodes**
- UGC frame: "Front-facing smartphone video shot, morning in-car recording. Camera fixed at dashboard height, propped against the windshield, pointing back toward the driver's seat with a slight upward angle… Low-to-mid smartphone video quality — mild softness, slight compression, no filters. Casual, bright, intimate morning feel. No phone visible."
- Product insert: "keep the photo the same but have the girl holding a large mcdonalds takeaway bag with 2 hands. the bag is a little creased, and has some subtle grease staining at the bottom. she has an expressive look on her face, almost like a surprise / shock look…"
- Selfie fantasy: "A cheerful selfie of the girl from the reference image inside a spacecraft cockpit, positioned between two astronauts with name patches reading Armstrong and Aldrin… Balanced cinematic lighting, photorealistic detail." The twist frame is a green-screen "behind-the-scenes selfie".
- Product breakdown (assistant node): "Write me a list of the 10 components that make up this product. Describe each one in extreme detail, being specific about it's sizing, colour and material used. Give reference at the end of each component to what product it is from."

**Veo 3**
- Regional variants (7529894056332184854): "A black and white video. The sound of rain as it starts raining, handheld camera filming close up as a man zips up his nike jacket, he says to the camera: This was made by ai. The man is [black] and has an [american] accent. His hand does not cover the white nike logo, the nike logo is clearly visible on the jacket. The man is wearing a nike cap underneath the hood." His tips: B&W, close-up, **no face in the start image**.
- Inside the product (first/last frame, 7592277750224801046): "Start on a stable bottom view of the phone, centered on the charging port. The camera begins a gentle FPV-style glide toward the opening, with subtle micro-movements and no harsh motion. …the camera aligns and slips inside. The interior reveals a dense network of blue circuitry… blue light streaks activate connectors…, creating a sequential startup effect. The camera flows through multiple interior levels, fast but stable, guided by illuminated pathways reacting to its movement."
- JSON for ads (ChatGPT → Veo 3 Fast): `title`, `style`, `sequence[]` of {`stage`, `description`, `camera`, `lighting`, `effects`, `sound_effects`}, `mood`, `color_palette`, `style_reference` ("Apple product intro meets high-end beverage cinematography").

**Gemini Omni Flash (Higgsfield)** (7657598688323292448). Clips max 10 s, so longer footage is chunked. Start with "keep this video the same but…".
> "Modify the reference video. The structural geometry of the bridge, the London Eye, and the background buildings must remain completely identical… …a hyperlapse effect is applied strictly to the lighting, sky, and pedestrians. The speaking man remains in real-time… lighting cycle instantly… becoming a dark night scene by the 2-second mark. …smoothly locking back to normal real-time by the 5.5-second mark."

**ElevenLabs.** Voice Design (v3) has a **Guidance scale** (prompt adherence) and a Loudness slider (7521667636879494422).

**Claude / GPT-6 as operator**
- DaVinci (GenHQ page, 7684717461681261846): "…skin at 55–65 IRE, strong teal/cyan shadows, warm highlights." **Node order:** CST In → Noise Reduction → Balance & Exposure → Contrast & Density → Color Compressor → Split Toning → Magic Mask (Subject) → Depth Map → Face Refinement → Skin Protection → Vignette → Halation → Glow → Film Look Creator → Film Grain → CST Out. "GPT-6 should report the settings it actually applies, not just describe a look."
- Mass production: `npm install -g @higgsfield/cli`, then "Use /Claude reference images folder. Follow instructions.md".

### A3. Editing and sound techniques (new)

- **Source + 1 s.** Set the v2v generation 1 s longer than the source clip so the end isn't clipped.
- **Iterate cheaply.** Test at 480p ($1.40 each, about 10 gens = $14), finish at 1080p. A 21 s 720p hero shot costs about $25 per gen; a finished skit about $400.
- **Speed ramps** three ways: in the prompt (% speed per beat), in the generator (Cinema Studio 2), or in AE (pre-compose → Enable Time Remapping → 4 keys → F9 Easy Ease → shape the graph).
- **Premiere seam punch:** trim 2 frames from each side of every AI seam, then stack two transition effects (Kling 2.5 football ad).
- **Real footage → AI restyle as the default 2026 shoot.** Film on a phone with real props and friends, build a character sheet, a location still and a prop sheet, then run v2v. Optional: a depth-map pass (Depth Scanner 2) or a grey-box 3D blockout (Magnific 3D Scenes) for camera control.
- **Sound as its own pass.** Claude watches the cut and writes a frame-accurate SFX map; Seedance re-renders the same picture with audio. Rules worth stealing: one hit per cut, weighted to the picture; no foley for off-screen motion; ambience swaps on the cut frame; a "near-silence" beat before the craft moment.
- **Two-world proof layout.** A 2- or 3-tier stack (Original / AI / BTS or Depth / Alpha), labelled in the corner and synced.

### A4. Business, clients and pricing (new)

- **Paid-partner content performs:** posts tagged ad or partnership have a median of about 110k views against about 68k for all 2025–26 posts. The tool is written into the story, not bolted on.
- **Ad use cases he names for clients:** localized variants (label swap, accent and ethnicity variables), "one advert, three products", mass product loops via the CLI, and Genjutsu swaps for "endless paid ads".
- **Lead magnets get more specific:** a GenHQ page per workflow (Workflow Overview, Full Prompt, "Join GenHQ"), shared Spaces boards, free Claude skills ("SFX skill") and `instructions.md` files.
- **Credibility moves:** "I paid a professional motion-graphics artist to test this", "spent 48 hours refining it", and cost reveals at the end.

### A5. Patterns in his best performers

1. **Views per post are falling as he gets more skilled.** The quarterly median went 2k (2024 Q1) → 99k (2025 Q3) → 39k (2026 Q3), while posting fell from about 30 to 13 a month.
2. **The biggest hits are consumer-legible.** "FREE", a big brand (Meta, Google, Artlist) and **his own face or name in the result**. Little UI, and 1–3 words of kinetic title per beat.
3. **Pure proof beats tutorial.** Omni hotel (1.9M) has no UI at all; WAN (2.9M) is just 3 synced rows.
4. **An escalation ladder:** "but it gets crazier" ×3–4, or a snap of the fingers per effect, shot on location.
5. **2026 skits** (★) get 80–200k, beating the 15–60k of plain tool demos in the same months.
6. **Seedance and Claude topics** have lower medians (38k and 50k) than Google or Kling (80–96k); niche workflows trade reach for authority.

### A6. New things to copy now (new)

16. **The v2v "master-footage lock" prompt** (A2) as a Seedance template: the list of THE ONLY CHANGES, plus "NOT a start frame" scoping for look refs.
17. **Duration = source + 1 s and the 480p-first test ladder** in hfgen cost plans.
18. **SFX-map pass.** Have Claude write a frame-accurate sound brief, using the rules in A3, before ElevenLabs or Seedance audio. Add it to 13-elevenlabs-mastery as a "sound design brief" step.
19. **DaVinci 16-node order plus "report actual settings"** as our grade checklist for AI plates, with skin at 55–65 IRE.
20. **"SHOT n — Name EFFECT: a + b + c"** beat syntax, with a named SIGNATURE beat and colour carry-over from the source object, for transformation ads.
21. **Spaces-style auto-JSON** for kinetic one-takes: `motion_rules` booleans (no_hovering, no_ease_in_out, always_moving_forward) plus `path_beats[]`.
22. **Localization variables in one prompt** ([ethnicity], [accent], product line), with a faceless start frame so one plate serves every market.
23. **Re-angle from one take.** Shoot once, then have Claude emit timecoded "Hard cut to Shot N" re-angles. Iterate on sub-clips.
24. **Grey-box blockout or depth map as layout reference** when camera path matters (Magnific 3D Scenes / Depth Scanner 2).
25. **Product breakdown → persona → location** assistant chain for new-brand pitches, with the vacuum components as end frames.
26. **Two-tier synced proof** (Original / AI) as our standard portfolio cut-down. Faceless, so the talking-head ban still holds.
