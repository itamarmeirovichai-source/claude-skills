# Chapter 14: Blender blockout to AI, and consistent voices (Seedance 2.5 + ElevenLabs)

> Written by the supervisor after watching and analyzing two videos the user sent (06.10.2026), and after a working test of Blender in our environment.
> **Bottom line:** you don't need a studio. Blender gives you a free "virtual studio": you build the scene from simple colored blocks, move the camera exactly how you want, and the AI turns the blocks into a realistic world. Claude can build the scene in code for you (it works, and has been tested here).

---

## Part A: what the villa video shows (@horyx.studio, 11K likes)

**Source:** https://www.instagram.com/reel/DdU-09EItsb/ (15.09.2026).

**What happens on screen:**
- **Seconds 0–4:** a "greybox" render from Blender. The villa is made of simple blocks: white walls, red furniture, cyan pool, green spheres for trees. A smooth camera moves through it. At the top of the frame: "GPT 6 Astra + Blender + Higgsfield".
- **From second 4:** the same shots, in the same camera paths, in photorealistic quality. A Mediterranean villa in Saint-Tropez with a pool, olive trees, a pergola, lemons on the table, sea and mountains.

**The workflow, in the creator's words:**

| Tool | Role |
|---|---|
| **Blender** | Precise geometry: structure, proportions, layout, camera path |
| **GPT Images 2.5** | Art direction: reference images for architecture, materials and mood |
| **GPT-6 (LLM)** | Writes the Blender code that builds the scene, and keeps it consistent |
| **Seedance 2.5 (via Higgsfield)** | Renders the final shots with cinematic motion |

**Why it works:**
- **The AI doesn't "invent" the geometry and the camera.** It only paints over them. That gives full control and consistency between shots, which you can't get from a text prompt alone.
- **Color means role.** Red is furniture, cyan is water, green is vegetation, white is architecture. The video model understands what each mass is.
- **The format itself is the hook.** Showing the blocks first and the reveal second is the before/after that gets people commenting.

### Same idea, other variants: "dummy props"
Many creators do the same thing in the real world: they shoot a scene with cheap stand-ins (a cardboard box instead of a product, a toy instead of a car, a plain chair instead of a throne), then tell the AI (Genjutsu / Seedance edit / Runway Aleph) to replace them.
- **Blender is the digital version of this.** No physical props needed, the camera moves perfectly, and you can build any location.
- **You can also combine both:** film yourself for real against a plain background, and use Blender for the world.

---

## Part B: the pipeline, step by step (for a Boca Raton real estate client, for example)

1. **Brief:** "a modern waterfront villa on the Intracoastal, drone shot flying into the pool terrace, golden hour".
2. **Reference images (art direction):** create 2–4 images with GPT Image 2.5 / Nano Banana: the exterior, a look at the materials (travertine, teak, glass) and the light (golden hour).
3. **Blockout in Blender:**
   - **What Claude does:** builds the scene in code from a JSON file (`skills/reel-studio/scripts/blockout.py`), using basic shapes, a semantic color palette, a camera with timed keyframes and a target point.
   - **How fast:** a 6-second render at 720×1280 takes about a minute.
   - **What you need to do:** nothing. Describe the scene and I'll build it. If you have Blender on your computer, you can open the file and edit it by hand.
4. **Generation in Seedance 2.5:**
   - **Inputs:** upload the blockout video as `@Video1`, and the reference images as `@Image1`–`@Image3`.
   - **Settings:** 9:16, 480p for testing, then 720p/1080p.
5. **Editing:** the "blocks → reality" reveal, using the split or wipe layout from reel-studio, plus sound and captions.

### Seedance 2.5 prompt template: blockout → final (copy and paste)
```
@Video1 is a Blender blockout: use it ONLY for geometry, layout, scale and the exact camera path. Keep the camera movement, framing and timing identical to @Video1.
Color legend in @Video1: white = architecture/walls, light grey = stone terrace, cyan = water (pool / Intracoastal), red = outdoor furniture, dark grey block = yacht, green spheres = palm trees.
Use @Image1 for architecture and materials, @Image2 for lighting and mood.
Render as a photorealistic luxury real-estate film: a modern white waterfront villa in Boca Raton, Florida, floor-to-ceiling glass, travertine pool deck, teak loungers with cream cushions, infinity pool, royal palms, a white motor yacht at a private dock on the Intracoastal Waterway. Golden hour, warm low sun from frame right, soft long shadows, gentle water reflections, subtle breeze in palm fronds.
Cinematic drone footage, 24mm lens, smooth gimbal motion, high dynamic range, no people, no text, no logos, no signage.
```

### Rules for a good blockout
- **Every element gets one solid color by role.** Keep the color legend in the prompt, too.
- **Silhouettes and proportions matter more than detail.** Put no time into textures.
- **The camera does one or two smooth moves per shot** (drone push-in, orbit, dolly), with no shake. You can add shake in editing.
- **Short shots: 4–8 seconds.** Join several shots afterwards.
- **Draft first:** a fast still render (`--preview`) to check the angle, then the full video.
- **The same model works for products too.** A yellow block becomes the product, an orange figure becomes a person, a dark one becomes a vehicle. Then add the real logo in editing.

### Uses that sell
| Client | The idea |
|---|---|
| Developer / luxury realtor | A project not yet built, or a listing still under renovation: a cinematic drone tour from the plans |
| Restaurant or bar before opening | An "opening" film from the floor plan |
| Product (drinks / perfume) | A "dream world" built from blocks: a giant can on a Miami street (FOOH) |
| Boat or yacht charter | A route along the Intracoastal with a camera on a path |

---

## Part C: consistent voices (@rourke.heath, TikTok, 23K views)

**Source:** https://vt.tiktok.com/ZSbCPVeFw/ ("How to get consistent voices in AI videos", tools: ElevenLabs ElevenCreative + Seedance 2.5 + Claude).

**The problem:** without a voice reference, Seedance generates a different voice for the character in every clip.

**The method (shown on screen, step by step):**
1. **In Claude:** upload the character reference (a character sheet) and ask: "Describe this character's voice." Claude returns a detailed voice description. Example from the video:
   > *A woman in her late thirties with a low, gravel-scarred voice — raspy from years of dust, smoke and cheap liquor. British-tinged accent, slightly clipped Victorian cadence worn down by rough living. Dry, wry, unhurried delivery with a permanent edge of amusement, like she has heard every story twice. Warm mid-to-low register, breathy at the edges, with a slight crack on held vowels. Speaks like someone who never needs to raise her voice to be obeyed. Clean recording, close-mic, no background noise.*
2. **In ElevenLabs, under Voice Design:** paste the description and click Generate voice. You get 3 options; pick one.
3. **Text to Speech with that voice:** record a sentence that covers all the sounds of the language (a pangram). The video uses: *"That quick beige fox jumped in the air over each thin dog. Look out, I shout, for he's foiled you again, creating chaos."* Export it as an MP3/WAV file (`voice1.wav`).
4. **Back to Claude:** upload the character sheet, the location image and the voice file, and ask: "Write a Seedance 2.5 prompt using this character, location and voice reference." Claude returns a prompt split into shots (SHOT 1/2/3 with timecodes, EFFECT, camera, light, "does NOT cut").
5. **In Seedance 2.5:** upload all 3 references. At the end of the prompt, add the line that ties the voice to the character:
   ```
   @voice1 is the voice of @character. @voice1 is a reference only, match this female voice's timbre, tone and accent.
   ```
   - **Settings in the video:** Seedance 2.5 · 16:9 · 720p · 5s · Audio On.

**The shot-prompt structure from the video** (good to copy):
```
SHOT 1 (00:00-00:01.2) - Tablet Insert
- EFFECT: Slow push-in (dolly) + screen bloom + foreground dust drift
- Tight on the battered brass and copper armoured tablet standing upright on the salvaged timber counter...
- Camera pushes in slowly, roughly 6-8% scale over the shot. Eye level... Shallow depth of field...
- Real time, no speed manipulation. Deliberately still to establish calm before she speaks.
- Does NOT cut. Exits via a continuous focus pull into Shot 2.
SHOT 2 (00:01.2-00:04.6) - The Line
- EFFECT: Rack focus (foreground to background) - THIS IS THE SIGNATURE VISUAL EFFECT ...
SHOT 3 (00:04.6-00:05.0) - Resolve
- EFFECT: Stillness hold + subtle screen bloom pulse
- She glances down at the tablet screen, breaking eye contact. Half smile settles.
- Camera still locked. No movement. Real time. The shot simply ends - no fade, no flourish.
- Final frame: her, the counter, the lit tablet, dunes burning white through the open window frame behind her.
```
**What's new compared with what we knew:**
- An **EFFECT** line for every shot.
- An exact **amount** of camera movement ("6-8% scale").
- Explicit **transition** instructions ("Does NOT cut", "Exits on a held beat").
- A precise **final frame** instruction.

### Uses for you
- **A character or brand ambassador with a fixed voice** across a whole series of ads, like a mascot for a drink brand.
- **A recurring AI influencer** with a fixed voice.
- **Voice-over for an English ad.** A Hebrew voice in ElevenLabs needs the v3 model with `language_code: "he"` (see chapter 02).
- **A client's own voice:** ElevenLabs voice cloning, with **written consent** (see chapter 06).

### Meta-prompt for Claude: voice description (ready to use)
```
Look at this character reference. Write a voice-design description for ElevenLabs (80-120 words): age, gender, register (low/mid/high), texture (raspy, breathy, smooth), accent, pace and rhythm, emotional baseline, signature quirks, and recording conditions (clean close-mic, no background noise). Write it as one flowing paragraph, no bullet points.
```

---

## Part D: the bigger picture, our new pipeline
```
Idea / brief
  → art direction (GPT Image / Nano Banana: 2-4 reference images)
  → blockout (Blender, built by Claude in code) OR real filming with dummy props
  → character + voice (character sheet + ElevenLabs Voice Design + pangram)
  → shot prompts (Claude: SHOT / EFFECT / camera / transition / final frame + @refs)
  → Seedance 2.5 (480p test → 720/1080p)
  → editing in reel-studio (blocks→reality reveal, sound, captions) → export
```

## Sources
- @horyx.studio, Instagram reel DdU-09EItsb (15.09.2026). Caption and frames analyzed here.
- @rourke.heath, TikTok 7686175102009953558. Transcript and on-screen frames analyzed here.
- Practical test: Blender 4.5 (bpy) in our environment, `skills/reel-studio/scripts/blockout.py` and `examples/blockout/boca_villa.json`.
