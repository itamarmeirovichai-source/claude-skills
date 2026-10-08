# 24 · Free courses, studied end to end (Oct 2026)

**Scope.** These are official, free, no-login courses and guides for the AI tools and ad platforms we use. Each entry gives the URL, what it covers, and only the lessons **not already in 00–23**. Verbatim rules and prompts are in code blocks. [inf] marks our inference. No money was spent and no accounts were created. Fetched pages were treated as data.

**Access.** Open and studied: Higgsfield Academy catalogue, syllabi and Prompt Bank (lesson players need sign-up; 3 courses studied via their public YouTube twins); Kling Quick Start; Google Veo/Gemini Omni/Nano Banana/Flow docs; Runway prompting guide + all 10 "AI for Advertising" lessons; ElevenLabs best practices; Krea docs; Topaz Learn; Google ABCD Playbook PDF; Meta's public Creative Strategy study guide PDF (Blueprint lessons need a Facebook login); TikTok's public creative help article (Academy lessons need registration); Pinterest. Not extractable: BytePlus Seedance guides (JS-rendered), Freepik Academy (403), Leonardo (API docs only), Snap (official page 404; [3P] only), Runway help-center guide (403).

---

## Part A · AI-tool courses

### A1. Higgsfield Academy: Prompt Bank + ad courses
**URL:** https://higgsfield.ai/academy · Prompt Bank: https://higgsfield.ai/academy/apps/prompt-bank (46 camera moves on 2 pages).
**Covers:** courses on movie-making, UGC/social and automation. The ones relevant to us:
- "The 3-Step Realistic AI Ad Workflow" (16 lessons, already in 06 as S4).
- "Make a Cinematic Ad End-to-End" (10 lessons, 46 min).
- "Direct a Cinematic AI Car Commercial" (11 lessons).
- "Build a Brand's Visuals with AI" (9 lessons).
- "Build an AI Ad Agency with Claude + Higgsfield" (12 lessons).

The Prompt Bank is the part not covered by our library.

**Prompt Bank pattern [new].** Every move is written **scene-agnostic**, so it can be appended to any shot. Each one gives:
1. the move;
2. a numeric geometry (metres, degrees, FOV);
3. an exhaustive "no-X" list of every *neighbouring* move;
4. an end state.

Examples, verbatim:
```
Static: The camera stays planted in one immovable position from the first frame to the last. Zero motion — no drift, no shake, no breathing, no stabilization float, no micro-drift; absolute rock-solid stillness throughout. Angle, elevation, distance to the scene and the overall composition are frozen and never altered; every ounce of motion comes from the scene itself, never from the camera. The clip closes on precisely the framing it began with, identical down to the pixel.

Arc right: One continuous arc right — the camera travels along a circular path around the subject through about [60] degrees on a locked constant radius of [2.5] meters at a locked constant height, panning continuously to keep the subject dead-center at constant size while the background sweeps behind them. … the subject stays planted, facing one fixed direction in the world — it is the camera that travels. No radius drift, no height change, no zoom, no turntable effect where the subject rotates in place.

Push past: One continuous forward travel on a lane offset about 0.6 meters to the subject's right — the camera approaches at constant speed and constant height, the subject growing in frame, then slides past their shoulder: the subject exits cleanly at the left frame edge while the camera continues WITHOUT stopping toward the reveal beyond, focus racking from the subject to the far point at the moment of the pass. The camera passes BESIDE the subject, never through them, never stopping at them. No pan correction, no zoom, no tilt.


Zoom in: Locked tripod, zero rotation, zero travel — the entire move is optical, a focal-length change only: one slow perfectly even continuous zoom in from [84] degrees to [29 or 18] degrees … perspective stays constant and there is no parallax.

Whip pan: The camera holds composition A perfectly static, then executes ONE violent horizontal whip pan to the left — a 0.4-second full-blur smear — landing hard on composition B with a 2-degree overshoot-and-settle, then holds composition B perfectly static.



Robot arm: The camera flies one fast, perfectly smooth stabilized motion-control path through four positions — [front eye-level medium close-up] → [side arc at eye level] → [sinking into a low angle with a slight dutch tilt] → [craning up and over into a top-down 3/4 view]. Each glide takes about [1] second with soft ease-in/out and brief readable holds at every position; machined gimbal/crane quality — no shake, no whip pans, no speed ramps, no motion blur.


Low tracking: Extreme slow motion throughout — a ~1000fps look with no speed ramps and no real-time moments — the camera at ground height below knee level … The track never stops: the shot ends mid-motion on a live frame — no cut to black, no fade, no freeze.

```
- **Zoom vs dolly.** The bank names the physics: zoom = no parallax; dolly = parallax, FOV fixed. [inf] Use it to stop models from substituting a zoom for a push-in on product moves.
- **"Robot arm" with ~1 s holds** is the motion-control product move we lack. It is cheaper than an orbit and safer for labels. [inf]

**Course "Make a Cinematic Ad End-to-End"** (YouTube twin: https://youtu.be/ODNzk5x2tR4, 46 min, Seedance 2.0 + Claude skill). New lessons:
- **Test the character × location pair before locking either.** One 5 s, 1-take Seedance test. The test clip later became the film's opening.
- **Location is "the most important image".** "The video grabs the textures and the lighting from the given images." Make it in Soul Cinema with "anamorphic lens, shallow depth of field, film grain".
- **Every prompt carries "no music, only environmental sound effects"** (music is laid in post).
- **Director-notes loop.** Never hand-edit prompts. Watch, list the failures as notes, and Claude rewrites:
  ```
  you should keep moving fast during the transformation. Add creative camera movements, handheld, some Dutch angles. Also, the point important, he runs forward not backwards. And fix the face. Natural smile. Alive eyes. No color change.
  ```
- **When a scene is flat, switch from "what happens" to "what the camera sees", shot by shot.** For example, "start with a close-up on the rival's leg… cut to an over-the-shoulder… cut to a robot already dropped into a ready stance… handheld with shake, cinematic low-angle shots."
- **Physics notes must name weight and material.** "fall with real weight and a hard impact… armor should break into heavy metal pieces. No smooth breaks." Also forbid automatic actions: "The can should not open on its own. He opens it himself with a clear action."
- **Mechanics-heavy scenes.** "Don't run just two batches. Run a ton, then take different phases from each generation and cut them together." Harvest the unused phases into later scenes.
- **Objects seen once don't need an asset sheet** (the model invented the watch).
- **Pack-shot notes.** Add a dolly-in; "match [sunlight] to scene one"; the name builds from parts, pull back, end on an energy hit.
- Motto: "the final film is just the best 3 seconds of 100 tries cut together."

**Course "Direct a Cinematic AI Car Commercial"** (YouTube twin: https://youtu.be/GNxmt_4IifA, 36 min). New lessons:
- **"The narrower the frame, the less waste you will get."** These failed every time:
  - wide FPV over traffic (cars cross lanes; 120 km/h reads as 60);
  - traffic lights (red and green together);
  - overtaking in traffic;
  - the classic steering-wheel → front-wheel match cut ("Seedance has no idea what it is");
  - dashboard numerals.

  The fix: many unique *narrow* angles, cut in the edit.
- **"Clean your plate."** Remove signage text and distant clutter from the location still. Distant cars "were constantly turning into clones of our red car." This takes two passes, sometimes literally "with an eraser".
- **Use Seedance as a consistent image editor.** Generate a slow static video of an interior or set, screenshot each angle, and save each one as an element. "Most image models change lighting or details between frames… every frame of your video… matches the others."
- **Position anchor first.** In multi-person or vehicle scenes, generate the frame that fixes "who sits where" first and reference it from every later shot. Shoot the **dialogue beat before** the arrival and departure: it decides where the car stops.
- **Cut-count discipline.** The model added inserts, so this went into the prompt:
  ```
  exactly five frames and four splices, no extra inserts
  ```
- **Script where thrown props land** (the cap falls "right in front of the camera"). Generate small-text props separately and **pre-blurred**. A face mismatch inside a character sheet is fixed by cutting the close-up face out by hand, not by regenerating.
- **Always generate the product on neutral grey.** Lock one palette for the whole film with Color Transfer.
- Append this to any over-packed shot request:
  ```
  If it's too much for one prompt, split it into two.
  ```

**Course "Build a Brand's Visuals with AI"** (https://youtu.be/sXgWhKwiUdc) is mostly a Marketing Studio demo (not on our API, 12 §2). Keep: "keep your logo memorable, not clever"; one **hero item** per collection; the "Hyper Motion" grammar (element-by-element build-up → clean pack shot).

### A2. Kling Quick Start (Kuaishou official)
**URLs:** https://app.klingai.com/global/quickstart/klingai-video-3-model-user-guide · …/klingai-video-3-omni-model-user-guide · …/text-to-video-prompt-guide · …/image-to-video-guide
**Covers:** the 3.0 / 3.0 Omni features, the prompt formulas and pricing.

Formulas, verbatim:
```
T2V: Prompt = Subject (Subject Description) + Subject Movement + Scene (Scene Description) + (Camera Language + Lighting + Atmosphere)
I2V: Prompt = Subject + Movement, Background + Movement ······
```

**New to us:**
- **I2V needs "subject + verb", never a bare verb.** "wear sunglasses" fails; "Mona Lisa puts on sunglasses with her hand" works. A still that the model reads as a *painting or photo* tends to yield a static pan "which is also the reason why photos are prone to generating static videos" [inf: name the product as a physical object in the scene].
- **Custom Multi-Shot syntax** (shot-level duration, framing, camera):
  ```
  Shot 1 (2s): Wide shot, @Boxer A and @Boxer B face off in the center of the rooftop… Shot 2 (2s): … Shot 5 (2s): A bird's-eye view…
  ```
  - With Multi-Shot ON but not Custom, the model may still return a single shot "if the described scene is better suited to a single shot".
- **Native-text ad example.** This is Kling's own perfume prompt; its text-preservation feature is pitched "for e-commerce advertising":
  ```
  …the gilded afternoon sunlight filters through the shutters onto the perfume bottle… The camera pans slowly in from the scattered rose petals, shifting focus to the faceted cut of the Kling perfume bottle. Voiceover (lazy French female voice, British accent, slow pace): Bathe in the golden hour. The camera orbits the perfume bottle in slow motion, capturing the play of light and shadow on the golden lettering and bottle body…
  ```
- **Timecoded 15 s long take:** "At the 4th second… At the 8th second… In the final 3 seconds…" + "a single unbroken shot with no edited transitions".
- **Elements 3.0:** a 3–8 s video creates a character element *with its voice* (or 2–4 images + ≥3 s audio). "If you choose a subject with a pre-bound voice tone, it's not recommended to set the tone again in the prompt."
- **Price:** native audio 12 vs 8 credits/s at 1080p (9 vs 6 at 720p), confirming our "sound off" rule.

### A3. Google: Veo / Gemini Omni best practices, Nano Banana guide, Flow help
**URLs:**
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/best-practice
- https://ai.google.dev/gemini-api/docs/image-generation
- https://support.google.com/flow/answer/16353334
- https://blog.google/technology/ai/flow-video-tips/

**New to us:**
- **Dialogue without on-screen text: use a colon, no quotes.**
  ```
  Not recommended: A woman says: "My name is Clara."   Recommended: A woman says: My name is Clara.
  ```
- **Negative prompts list nouns, not instructions.** "Not recommended: 'no walls' or 'don't show walls'. Recommended: 'wall, frame'."
- **Short clips = one moment.** "Trying to chain multiple distinct events (A then B then C) in one prompt for a short video often leads to muddled or incomplete videos."
- **I2V: prompt motion only, and call the subject "the subject / the woman / he".** "Re-describe the character, the background, or the lighting depicted in the image. Redundant prompts confuse the model." The three motion layers:
  - **Camera motion** "the simplest and most reliable way to add dynamism".
  - **Subject animation** "best for subtle, lifelike actions".
  - **Environmental animation**.
- **Character + voice consistency.** Name the character. Paste the *identical* description block (face, hair, wardrobe **and** voice: "In a voice that is crisp and clear, with a thoughtful, analytical tone and a standard American accent") into every prompt, and reuse the same `seed`.
- **Gemini as reviewer.** "After your video is generated, Gemini Omni can evaluate the final output, check it against company or brand guidelines, and flag any potentially problematic areas." [inf] This is a free QC pass for 18 S10.
- **Nano Banana templates**, verbatim:
  ```
  A high-resolution, studio-lit product photograph of a [product description] on a [background surface/description]. The lighting is a [lighting setup, e.g., three-point softbox setup] to [lighting purpose]. The camera angle is a [angle type] to showcase [specific feature]. Ultra-realistic, with sharp focus on [key detail]. [Aspect ratio].

  A minimalist composition featuring a single [subject] positioned in the [bottom-right/top-left/etc.] of the frame. The background is a vast, empty [color] canvas, creating significant negative space. Soft, subtle lighting. [Aspect ratio].

  Using the provided images, place [element from image 2] onto [element from image 1]. Ensure that the features of [element from image 1] remain completely unchanged. The added element should [description of how the element should integrate].
  ```
  - Also: "When generating text for an image, Gemini works best if you first generate the text and then ask for an image with the text."
  - Also: "semantic negative prompts" ("an empty, deserted street with no signs of traffic").
  - Limits: NB 2.1 holds **10 objects + 4 characters**; NB Pro holds 6 objects + 5 characters + 3 style refs (14 total).
  - Video-to-image: NB 2.1 accepts a video/YouTube URL as the reference [inf: poster or thumbnail from our own cut].
- **Flow ingredients.**
  - "provide subject or product references on a plain or segmented background."
  - Location and style refs "don't contain extra subjects".
  - "Your text prompt should complement, not contradict, your visual inputs."
  - "A consistent look and feel across all your ingredient images helps the model blend them."
  - Speech is less likely if the line "doesn't fit in the 8-second clip".
  
### A4. Runway Academy: Prompting Guide + "AI for Advertising" (10 lessons, ~20 min)
**URLs:** https://academy.runwayml.com/guides/prompting-guide · https://academy.runwayml.com/course/ai-advertising (lessons are YouTube embeds, e.g. https://youtu.be/Cucu3i-v3s0, https://youtu.be/FGrtzZrYnDA).
**Covers:**
- moodboard;
- concept exploration;
- brand manifesto → VO;
- storyboard → previs;
- product shots;
- content calendar;
- casting and wardrobe;
- talent and product placement;
- B-roll and VFX.

**Prompting guide, new to us:**
- **Over-specification warning.** "Extremely complex, multi-paragraph prompts reduce the room for creative freedom… This over-specification can paradoxically lead to unexpected or unnatural results, as the model struggles to honor every detail simultaneously." (Contradiction, see C1.)
- **Implied-motion check.** A start frame containing motion blur, dust clouds or mid-action poses fights a "parked/still" prompt. Remove those cues in an image edit first.
- **Unwanted cut** = the duration is too short for the action. Lengthen it first, then add:
  ```
  Continuous, seamless shot
  ```
- **Still-shot reinforcement:**
  ```
  The locked-off camera remains perfectly still.
  The camera must start and end on the exact same frame to create a perfect loop.
  Minimal subject motion only.
  ```
  Or use the same image as both start and end frame.
- **Structures:**
  ```
  T2V: [Camera] shot of [a subject/object] [action] in [environment]. [Supporting component descriptions]
  I2V: The camera [motion description] as the subject [action]. [Additional descriptions]
  Timestamps: [00:01] X occurs. [00:03] Y occurs. [00:04] Z occurs.
  ```

**Course, new to us** (lessons are light tool demos):
- **Previs:** a B&W hand-drawn storyboard frame + **a real photo used only for colour and mood** → photoreal frame with the same composition.
- **Concept exploration in one call:** four *different treatments* of one idea (photoreal / watercolour / placement / one wild idea); branch from the most original.
- **Manifesto → VO:** one-sentence ethos → manifesto → VO "less salesy" → have the model extract "the sentence it believes is key" as the image prompt.
- **Placement is incremental:** one change per generation; re-prompt "the correct anatomy" rather than restart.

### A5. ElevenLabs: TTS best practices (v4 section)
**URL:** https://elevenlabs.io/docs/best-practices/prompting/eleven-v3 (13 covers parameters, IPA and tags.) **New:**
- **Tag/SFX ambiguity.** "a tag can occasionally be interpreted as a request for a sound effect rather than a delivery instruction". Write voice-quality tags like `[low, gravelly voice]`.
- v4/v3 **ignore SSML `<break>`**. Use ellipses, capitals and text structure instead.
- **Match tags to the voice.** "A meditative voice shouldn't shout; a hyped voice won't whisper convincingly."
- **The UI "Enhance" system prompt is published.** Core directives, verbatim:
  ```
  * DO NOT alter, add, or remove any words from the original dialogue text itself. Your role is to *prepend* **audio tags**, not to *edit* the speech.
  * DO NOT use tags such as [standing], [grinning], [pacing], [music].
  * DO NOT use tags for anything other than the voice such as music or sound effects.
  4. **Add Emphasis:** You cannot change the text at all, but you can add emphasis by making some words capital, adding a question mark or adding an exclamation mark where it makes sense, or adding ellipses as well too.
  ```
  [inf] Use it as a no-rewrite guard when Claude tags our VO lines.
- Stacked direction tags work for narration: `[Low, steady voice, restrained urgency] … [Brief pause] … [Softening, reflective]`.

### A6. Krea docs: Seedance Studio + Elements (the clearest public Seedance guidance found)
**URLs:** https://www.krea.ai/docs/user-guide/features/seedance-studio · …/elements
**New:**
- **"Seedance orders references by where they are first mentioned."** Mention each element in the sentence where it acts.
- **Element guidelines**, ≤400 chars, cover identity only:
  ```
  Woman in her early thirties with a sharp jet-black bob, pale skin, and deep burgundy lipstick. Keep the haircut and the black turtleneck in every shot; lighting and setting can change.
  ```
  - The prompt it produces: `Maria walks slowly into the empty warehouse. Maria: the character shown in @Image1, @Image2 and @Image3. …`
  - Use varied angles, "rather than eight near-identical frames".
  - Put the best images first: they are kept when truncating.
- **Ref caps (image/total):** Seedance 2.5 30/50 · Seedance 2 9/12 · Gemini Omni Flash 10/11.
- **3D camera path → video reference:** keyframe a camera through a grey-box scene (1–10 s), render, attach as a video reference. [inf] Exact orbit radius and timing without words; buildable locally in Blender.
- **Custom Look.** Studio reads a reference frame into *editable notes* (camera, lighting, colour, texture, composition). The image itself is not sent. [inf] This matches our style-header practice.

### A7. Topaz Labs Learning Center
**URLs:** https://www.topazlabs.com/learn/how-to-enhance-video-quality-resolution · …/how-to-use-frame-interpolation-in-topaz-video · …/preserving-artistic-continuity-with-higgsfield-ai
**New:**
- **Model by footage:** **Rhea** for "minimal movement, interviews, product shots, and textures"; Starlight Precise 2 for faces/skin; **Astra** (Creative mode) allows "certain levels of creative freedom", so not for labels [inf]. Precise mode "prioritiz[es] the original look".
- **Interpolation:** Apollo ≤8× (default slow-mo); Aion ≤16× but "can produce slight patterns or artifacts when trying to lock onto high-resolution details like text" [inf: keep off label shots].
- **New-angle trick.** Run a short camera-preset orbit of the approved still, extract the best intermediate frame, and use it as the next shot's start frame. This keeps the style continuous.

---

## Part B · Ad-craft courses

### B1. Google "ABCD" Playbook (Ipsos, with Nielsen and Kantar as reviewers)
**URL:** https://www.thinkwithgoogle.com/_qs/documents/15987/ABCDs_PDFPlaybook_April2022_Final.pdf
03 has the headline numbers. **New: the per-objective rewrite of each letter.**

| Objective | A | B | C | D |
|---|---|---|---|---|
| Core | Start big: in the middle of the action or on a close-up; bright colour and contrast | Brand early, often, richly | Help people think or feel; "avoid doing too much… Focus the message" | Clear, simple next step |
| Awareness | "Pump up the volume": VO, music and SFX amplify the on-screen message | **"Frequency plus variety"**: logo, tagline, mascot, pack shot | "Make people core to your story": people using the product | Simple instructions |
| Consideration | Immersive hook | **"Hero the product"**: tight beauty shots; "keep up your branding, especially in the last five seconds" | "Be relatable and demonstrative": show how it works, in context | **"Plant the seed of urgency"**: time frame or limited release, reinforced in audio |
| Action | Immersive hook | **"Make the product the ad"**: visible from start to finish, extreme close-ups; branding must not distract from the product | "Depict a use case": "upfront, precise, credible" | **"Contextualize and incentivize"**: a CTA tied to an offer |

Also: "The ABCD principles are not a formula for generating creative ideas". They come *after* the big idea.

### B2. Meta Blueprint: Creative Strategy Professional study guide (July 2026)
**URL:** https://www.facebookblueprint.com/student/page/210605-creative-strategy-study-guide (the PDF link sits on the page). The lessons themselves are login-gated.
**New to us:**
- **First-frame rules:** lead with brand ID; "Treat the beginning as the summary, not the conclusion"; use motion and contrast; "Design for the thumbnail"; avoid slow intros:
  ```
  Fade-ins, title cards or long brand animations delay the core content and increase the chance someone scrolls past before the message lands.
  ```
- **Branding cadence:** "Highlight the brand, logo or product within the first 3 seconds of a video **and again at the end**."
- **Length:** "People are more likely to watch to the end of video ads that are less than 15-seconds in duration". Longer messages go to in-stream with sound.
- **Text limits:** primary text 125 characters · headline 40 · description 25. Use shorter text on Reels and Stories.
- **Creative volume:** "Supply at least 3 to 10 creatives per ad set. For Advantage+ sales and app campaigns, supply 20 or more." Mix video and static. "consolidated campaigns need more creative variations, not fewer".
- **Partnership ads** (both handles): −19% CPA, +71% brand lift, +22% conversion when ≥30% of assets are partnership creatives [O].
- **Fatigue signals:** a "Creative fatigue / Creative limited" status, falling CTR, rising cost per result. Add new varied ads to the fatigued ad set rather than pausing winners.
- **Nine-point creative evaluation checklist** (verbatim criteria). [inf] Add it as a QC gate:
  ```
  1 Brand identification — Is the brand identifiable within the first 2 to 3 seconds? Are the logo, brand colors and product also visible upfront?
  2 Key brand message — Would someone who sees only the first few seconds still understand what is being advertised?
  3 Attention immediacy — Does the opening frame use motion, contrast, bold visuals or an unexpected element? Is the creative visually distinct from surrounding organic content?
  4 Sound-on and sound-off suitability — text overlays and visual storytelling; also benefits from music, voiceover and audio effects?
  5 Mobile framing and safe zones — designed in 9:16 and 1:1? essential content within safe zones?
  6 Call to action — Is the next step obvious?
  7 Lift study alignment — does it clearly reinforce the specific metric being tested?
  8 Complementary assets — Would performance improve by pairing video with image formats?
  9 Audience relevance — Does the creative reflect the interests and visual expectations of the intended audience?
  ```
  Its worked example fails a shoe Reel for: logo at 8 s ("too late"), benefit at 12 s, no captions, text in the Reels UI zone, a CTA "only in the final second" (fix: "pair it with a visual cue like an arrow or button-style graphic"), one asset only, and a runner too young for the target.
- **Brief rule:** use the same terms across media, strategy and creative ("conversions" vs "sales" vs "lower-funnel actions"). Write hypotheses into the brief, e.g. *"Creator-style vertical video with text overlays will outperform polished brand video for our awareness campaign."*

### B3. TikTok: "Creative best practices for performance ads" + Academy creative path
**URLs:** https://ads.tiktok.com/help/article/creative-best-practices · Academy path "Creative as a Growth Engine" (login).
**New:**
- **Hook and proposition timing:** "Prioritize your hook in the first 6 seconds… Introduce your content proposition in the first 3 seconds for better recall."
- **Account structure:** "3-5 different creatives per ad group and 3-5 diversified ad groups per campaign… always better to use creatives with big differences, especially when testing."
- **Refresh:** "add new creatives to an existing ad group instead of creating a new ad group to extend its lifetime." Refresh when delivery shows "a consistently declining trend".
- **Basics:** sound on; 9:16; ≥720p; people on camera; "a DIY or not overly polished style" (see C3).

### B4. Pinterest and Snap
- **Pinterest** (https://business.pinterest.com/creative-best-practices/):
  - 2:3 (1000×1500); "Larger aspect ratios may get cut off".
  - Logo "clearly visible on every ad… [but not] overtake the ad".
  - "Stay clear of abstract images or lifestyle imagery that doesn't show your brand".
  - Layout: visual in the middle, key text overlay on top, details at the bottom.
  - Headline 100 characters, of which the first 40 show.
- **Snap** [3P only]: "wow moment… no later than 2 seconds"; CTA in the first 2 s +71% swipe-ups (VidMob CPG); 3–6 s Snap Ads.

### B5. Free talks: Curious Refuge, D&AD, Cannes Lions, ad schools — not yet studied
Identified but **not transcribed**: the fetcher returned "Only images are available" (YouTube EJS challenge) and the session restarted twice. Queue for the next pass:
- Curious Refuge "This Is Where Filmmaking Is Headed Next (Full Tutorial)" https://youtu.be/HVeHHAfiR44
- Monks (Dave Carey) on AI product accuracy, Cannes Lions 2026 https://youtu.be/zwkXQJqUk-I
- Miami Ad School "Concepting: What Is It Really?" https://youtu.be/2DXs5-2XxVY · "Google's Minimum Viable Brief" https://youtu.be/-KYnb0bKzTE
- D&AD Awards Insights: writing (https://youtu.be/wh_X6sOBhXQ), craft/editing (https://youtu.be/5b7ZE1KybVQ)

---

## Part C · Synthesis

### C-NEW. Rules new to our library (→ file to extend)
1. Camera-move blocks name geometry **and forbid neighbouring moves**; zoom = no parallax, dolly = parallax (A1) → 12 §5, 16.
2. Robot-arm product move: 4 positions, ~1 s each, readable holds (A1) → 11 recipes [inf].
3. "The narrower the frame, the less waste": no wide traffic, FPV, intersections, overtaking, match cuts, dashboards (A1) → 06.
4. Clean the plate: strip text and distant look-alikes before video (A1) → 17 QC.
5. Seedance statics-video as a consistent multi-angle image editor (A1) → 17.
6. "exactly N frames and N−1 splices, no extra inserts" (A1) → 12 templates.
7. One cheap 5 s character × location test before locking assets (A1) → 18 S6.
8. Director-notes loop; when flat, switch to shot-by-shot camera language (A1) → 18 §4.8.
9. I2V = motion only, "the subject", never re-describe the still (A3, A4) → 12.
10. Strip implied motion (blur, dust, mid-action poses) from start frames (A4) → 17.
11. Unwanted cut ⇒ lengthen, then "Continuous, seamless shot" (A4) → 16.
12. Veo/Omni dialogue with a colon, no quotes; negatives as noun lists (A3) → 04.
13. Identical character + voice block + same seed; don't restate a bound Kling voice (A2, A3) → 13.
14. Seedance reference order = first-mention order; element guidelines = identity only, ≤400 chars (A6) → 12 §3.
15. Gemini Omni as a post-render brand-guideline reviewer (A3) → 18 S10 [inf].
16. ElevenLabs "Enhance" prompt as a no-rewrite VO tagger; voice-quality tags avoid SFX misreads (A5) → 13.
17. Topaz: Rhea for product, Precise ≠ Astra, Aion artefacts on text (A7) → 08, 17.
18. ABCD by objective: Action = product on screen start to finish; Consideration = branding strongest in last 5 s + urgency in audio; Awareness = brand frequency *and variety* (B1) → 03 r12.
19. Meta 9-point checklist; brand in first 3 s **and** at the end; CTA + visual cue; no fade-in/title card/long logo animation (B2) → 18 QC, 01.
20. Volume: Meta 3–10 creatives/ad set (20+ Advantage+); TikTok 3–5 × 3–5 ad groups; refresh inside the existing set/group (B2, B3) → 03 r15–16.
21. Text limits: Meta 125/40/25; Pinterest 100 (40 visible) (B2, B4) → 03.
22. TikTok: hook within 6 s, proposition within 3 s (B3) → 03 r1.

### C-CONTRA. Contradictions with our files

| # | Course says | Our files say | Reading |
|---|---|---|---|
| C1 | Runway: multi-paragraph prompts over-specify and cause "unnatural results". Veo: one moment per short clip. | 10/12/20: long treatment prompts (sippo, Rourke's ≈4,000-char Seedance), several cuts per prompt. | Model-dependent. Seedance 2.5 with refs tolerates treatments (NOTEBOOK). Keep Kling/Veo/Runway prompts short and one-moment [inf]. |
| C2 | Higgsfield Prompt Bank: most moves "decelerat[e] into a static hold" / "settle on a clear final composition and hold". | 21 C2: only the final packshot settles; every other clip runs "already at full speed… does not slow or settle". | Keep 21's ruling. Strip the bank's end clauses except on the packshot. |
| C3 | Higgsfield 360 orbit and drone orbit "~200-degree arc". | 21 C5: orbits ≤60°, ≤2.5 s. | The bank's own Arc left/right use 60°, consistent with us. Use the 360/200° blocks only for plates without a label. |
| C4 | TikTok: "DIY or not overly polished". Meta: "Authenticity over polish… creator-inspired style often see stronger performance." | 00 client taste: premium, clean, polished; 03 rule 14: low-fi can erode luxury. | Not a real conflict. Platform averages are DR-weighted. For premium briefs, keep polish but borrow *native grammar* (captions, people, POV first frame) [inf]. |
| C5 | Meta: viewers more likely to finish **<15 s**. | 03: conversion 15–34 s; TikTok top ads 21–34 s. | Deliver the 15 s cut as the Meta default and keep 20–30 s for TikTok and in-stream [inf]. |
| C6 | Meta first frame: "Lead with brand identification" in the first moments. | 03 rule 1: "never open on a logo sting". | Compatible: brand *cues* (colour, product, pack) in frame 0, no sting or title card. |
| C7 | Veo: dialogue without quotes (quotes render as text). | Kling guide and 14 Seedance prompts put dialogue in quotes. | Model-specific: Kling/Seedance quotes OK; Veo/Omni colon form. |
| C8 | Topaz: generative (Astra/Creative) upscale for AI video. | 21 C9: no generative upscale in v1. | Keep 21; if Topaz is added, Precise/Rhea on product only. |
| C9 | Higgsfield: "run a ton" of 15 s 1080p batches per scene. | 12: ~$10/film, Seedance ≤720p. | Subscription economics; we batch only the beat that matters [inf]. |
