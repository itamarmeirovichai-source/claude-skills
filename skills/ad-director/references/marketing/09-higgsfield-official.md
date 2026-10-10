# 09 — Higgsfield Official Knowledge Base: What They Actually Recommend

Distilled from ~55 official Higgsfield blog and Creator Hub pages, read October 2026. Citations like [S3] point to the source list at the bottom.

## 1. Why output looks "AI" (their diagnosis)

- **Three tells:** "Light without a named source… flattens a scene"; "Motion that doesn't carry weight reads as animated"; "A camera that's too stable and too smooth is one of the clearest signs that a shot was generated." [S1]
- **Mood words don't work.** "'cinematic'… 'realistic'… 'high quality'. These are not instructions… Physics… gives it something specific." [S1]
- **Anything left unspecified gets invented.** "Something in the prompt was left open, and the model closed it on its own". This is how two suns and fused hands appear. [S2]
- **Nano Banana Pro centres things.** On the same brief, it "made it more symmetrical", while Soul 2.0 kept the asymmetric high angle. [S3] This explains our "too centred" feedback.
- **Keep flaws in on purpose.** "Nothing real is clean… we leave the flaws in on purpose." [S4]

## 2. Prompt structures to copy

**Seedance 2.5 master template.** One block with labelled sections, in this order [S5]:
`GLOBAL STYLE` (genre, grade, stock, aspect, shutter, exclusions) → `SCENE` (logline) → `CHARACTERS` → `LOCATION` ("A vague location is the most common reason a multi-shot sequence starts drifting") → `FIRST FRAME AND BLOCKING` → `Shot 1… Hard cut.` → `OPTICS/CAMERA` → `PHYSICS` → `LIGHTING` (motivated source, direction, falloff) → `AUDIO` ("No music, no discernible dialogue").

What their testing found [S5]:
- "Genre and lighting settings do more work than most of the prompt text."
- "Explicitly excluding what shouldn't appear… prevents more failures than adding more positive description."
- A cluttered reference set "produces a less coherent result."

**Realism blocks they reuse** [S1][S5]:
- **Blocking:** screen coordinates ("she sits at x 60%, y 50%"), plus "The first visible frame already contains the full staging — no empty establishing frame."
- **Optics:** stated as field of view plus distance: 84° wide, 47° "natural human-eye perspective", 29° short tele at about 4 m, 18° tele. Add "No lens drift mid-segment."
- **Texture locks:** "Kodak Vision3 250D texture: fine organic film grain, gentle halation… filmic highlight roll-off… a real film frame, not digital video"; "Skin unretouched… No beauty retouch, no digital smoothing, no CGI sheen"; "NOT glossy synthetic… gate weave… faint chromatic aberration… lens breathing."

**Help-centre six blocks** [S6]: Style & mood → Camera → Lighting & colour → Action beats → Audio → Shot list. Their example uses:
- "NOT CGI-looking, NOT plastic, NOT a commercial."
- "60% amber and ochre, 30% deep shadow, 10% accents… NOT teal-orange, NOT saturated, NOT digital-clean."
- "real weathered matte skin, NOT glossy."
- Spherical primes ("35mm for the room, 75mm for faces, NO fisheye"), with "dolly, Steadicam, or sticks."

Once a frame exists, the prompt "stops describing what things look like and starts describing what happens". Don't contradict the frame. [S6]

**Style header from the Claude Skill.** One fixed prefix on every shot prompt; change it once and every shot updates [S7]:
"Photorealistic — no 3D render, no game engine… Natural light only… Key light from sky and windows only… Color: 60:30:10… Physical cine lens. 180° shutter motion blur. Skin: Pore-level realism — vellus hair, asymmetric moles, capillary flush… Acting: micro-pauses before reactions… Physics: …correct contact shadows. No floating props. Composition: Rule of thirds + golden ratio. Every person moving from frame one… Audio: Environmental SFX only. No music." [S7][S8]
Music is added during the edit.

**Seedance 2.0 basics:**
- Order: subject + action → setting + light → camera → mood.
- Put "Total: 15s / 6 shots / 16:9" at the top. [S9][S10]
- Product template: "@product sits on [surface] in [setting], [lighting], camera [move], [atmosphere]. No people, no text, no logos." [S10]

**Anti-gloss suffix for stills** (used in the $350k ad) [S11]:
"preserve original color grade, preserve original grain, preserve original exposure… no beauty grade, no skin smoothing, no sharpening, no HDR, no contrast push, no saturation boost, photorealistic, this is a film frame not an advertisement."

**Negatives: their guidance conflicts.**
- Seedance 2.5 and Kling prompts are full of "No…/NOT…" lists. [S5][S12]
- The Santiago breakdown says the opposite: "Seedance doesn't get negative prompts — write 'he is NOT crying' and it does the opposite. Tell it what you WANT instead." [S13]
- **Our rule:** put look and artifact exclusions in a lock block. Write actions and emotions only in positive terms.

## 3. Model-specific tips

**Seedance 2.5**
- 4–30 s, 9:16 to 21:9, up to 1080p, Pro plans and above. [S14]
- References: up to 30 images, 10 videos and 10 audio files.
- Selectors for genre, lighting angle and physics (realistic, superhero, hyperbolic). [S1]
- Their test found 2.5 renders at 720p, where "faces go soft" on wide shots; 2.0 goes up to 4K. [S15]

**Seedance 2.0**
- 4–15 s, up to 4K, 9 images, 3 videos and 3 audio files.
- Start with image-to-video at 720p from "a sharp, front-facing, well-lit reference". Change one variable at a time. Run the final at higher resolution "with the identical prompt". [S14]
- "Most quality problems appear at the 5 to 8 second mark." [S10]
- Camera terms it reads: "dolly in, truck left, arc shot, push in, pull back wide, handheld follow, crane up, orbital move." [S14]
- Reference roles: `@character`, `@style` (lighting and palette from a film still), `@motion`, `@audio`. [S10]
- Motion reference wording: "@video: camera-motion reference ONLY… Nothing else is inherited." [S15]
- Against plastic skin: "add 'no 3D, no cartoon, no VFX'". [S9]

**Kling 3.0** [S12][S16]
- 3–15 s, up to 4K. Up to 5 shots in Auto or Custom mode. Start frame, end frame, or both.
- `@elements`: "Tag the same element in every shot… Describe only the element's action."
- Pitfalls they list:
  - more than one action or camera move per shot;
  - "Fighting your own end frame";
  - too many shots for the clip length;
  - iterating in 4K (costs 3× 720p).
- "If it drifts, simplify the prompt and let the frames carry more of the direction."
- Recommended for "macro and product shots". [S12]
- Their macro prompt: "Slow hypnotic dolly-in… precision-slider smoothness… Warm tungsten-amber key from upper left, raking low so every scratch… casts a tiny shadow… no flat front light." [S12]

**Soul family** [S17][S18][S3]
- Soul Cinema "avoids the typical AI aesthetic". Use it for keyframes going into Kling or Seedance.
- Attaching a reference image disables the prompt.
- Soul HEX: palette transfer from 1–20 reference photos.
- Moodboards: 20+ cohesive images, no faces.
- Soul ID: 20+ photos from the same period and lighting.
- Risk: it can clone the trained face onto people in the background. [S3]

**Nano Banana Pro** [S19][S3][S20]
- Up to 14 references; state each reference's role.
- Give explicit counts ("exactly 3 bottles on the left side") and quote any text.
- Best for packaging text and edits. Faces drift over long series.
- Gives better depth than GPT Image 2: "the remote got depth, highlights, and realistic tapered edges." [S20]

## 4. Camera and Cinema Studio vocabulary

**Cinema Studio 4.0** (runs on Seedance 2.5; up to 30 s and 50 references) [S22][S23]
- Genre: General, Action, Epic, Drama, Comedy, Horror, Noir.
- Era: 60s to 2020s.
- Tempo: Chaotic, Dynamic, Calm, Single Shot. "Single Shot for a product reveal."
- Camera: Modern, 35mm Film, 8mm Film, DV Camcorder.
- Lens: Clean Sharp, Anamorphic, Vintage Anamorphic, Warm Vintage, Halation Vintage.
- Aperture: f/1.4, f/4, f/11. Moves: 30+, incl. POV, Robot Arm, Helicopter, pedestal down.
- Emotion Wheel (`@char Joy`). Without it, characters "default to a neutral, unreadable expression."

**Cinema Studio 3.5** [S24]
- MoveSet styles: Classic Static, Silent Machine, One Take, Epic Scale, Intimate Observer, Documentary Snap, Raw Chaos, Dreamy Flow.

**Lighting presets change the scene, not just the mood** [S25]:
- Soft Cross: half the face in shadow.
- Window: falloff with distance.
- Practicals: only sources in frame, "No hidden fill".
- Contre-jour: rim light and flare.
- Overhead Fall: eyes in shadow.
- Silhouette.
- Choosing the wrong one adds "a hidden off-camera source that removes the… atmosphere."

**Move wording** (from [S24]): state path, speed, easing and end framing, and rule out the rival move.
- Dolly: "constant speed… decelerating smoothly into a static hold… no zoom… strong parallax."
- Zoom: "NOT a dolly out… ZERO parallax."
- Orbit (their example is a perfume bottle): "locked constant radius… no turntable effect where the subject spins in place." Use Clinical Sharp lens for a clean product read, Anamorphic for theatrical.

**Avoiding distortion** [S26][S27]:
- "Avoid extreme camera moves… build [energy] through editing rhythm."
- Describe actions as start and end positions.
- Test the hardest shot first.
- "the tighter the frame, the less slop you get."

## 5. Consistency workflow

- **Build assets first:** product, character, location, props. [S7][S20]
- **Sheets on grey.** "character sheets on grey perform way better than on white or black". Product sheets show "front and 3/4 perspective views." [S20][S7]
- **One face per sheet.** "Erase the face from the full-body shot." Make separate sheets for each state (dry vs sweaty). [S7]
- **Locations:** empty, 3/4 angle, with film grain. "Your video quality depends mostly on this one image." "Video inherits its textures and lighting from this still." [S20][S8]
- **Location as style only:** "STYLE REFERENCE ONLY, not a fixed keyframe… Do not reproduce the reference frame 1:1." [S8]
- **Spatial control:** top-down location maps, hand-drawn trajectory diagrams, red-arrow contact marks, and a "statics video" whose screenshots become position locks. [S8][S20][S27]
- **Approved still first:** "our AI artists always work from an approved keyframe… Text-to-video is the exception." [S4]
- **Chain clips** by using the last frame of one as the start frame of the next. [S16][S10]

## 6. Post: relight, grade, upscale, edit

- **Video Relight:** 6 presets or 2 custom lights. Example: "Window left, cool blue, medium brightness, soft diffused. Fill: camera right, neutral white, low." [S28]
- **Color Palette:** 50+ grades, or grade to match a reference image. [S28]
- **Image Relight:** soft/hard light, direction pad, hex colour. "Flat lighting makes products look cheap. Add a Top or Side light." [S29]
- **Finishing order:** "clean flicker and exposure, then run weak resolution through Higgsfield Upscale." [S30]
- **Edit, don't regenerate.** Use Seedance 2.5 Edit "Draw to Edit" or Genjutsu Object Swap. Regenerating risks losing "the exact opening moment that made the ad work". [S31]

## 7. Ad specifics

- **Food and drink** [S32]:
  - Shot types: hero, macro, pour, steam, slow motion.
  - "Name the specific texture… 'glossy caramel drizzle'".
  - "sauce pouring slowly from top left".
  - "Call out steam, condensation, or moisture explicitly".
  - Describe the light identically in every shot.
- **Brief rule:** give every shot one job. The bike ad "ended on the rider instead of the bike it was selling." [S2]

---

## Top 12 things to change in our pipeline

1. **Hero stills:** Soul Cinema for keyframes and locations, Soul 2.0 with HEX and a Moodboard for colour. Nano Banana Pro only for label text and edits, and check its framing for symmetry. [S3][S17]
2. **No adjective prompts.** Remove "cinematic, premium, 8k". Specify a named light with direction and Kelvin, a field of view in degrees, a distance and rig, and a film stock. [S1][S2]
3. **One motivated key light per shot.** Use Practicals, Window or Soft Cross. Write "no flat front light". Allow flare only when the source is in frame. [S25][S2]
4. **Imperfect camera.** Handheld "breathing sway… never gimbal-smooth", or a slider move with easing and an end hold. No perfectly centred turntable orbits. [S1][S24]
5. **Off-centre blocking.** Give x/y coordinates, use the rule of thirds, and add blurred foreground occlusion. [S1][S7]
6. **Anti-gloss suffix** on every still, plus texture locks: halation, grain, dust, fingerprints, condensation. [S11][S5]
7. **One campaign style header** (GLOBAL STYLE + AUDIO) reused on every Seedance and Kling call. [S7][S5]
8. **Assets on grey with 3/4 views**, saved as named Elements. Locations empty, 3/4 angle, with grain. [S20]
9. **One action and one move per shot.** Iterate at 720p, check the 5–8 s mark, then render the final with the identical prompt. [S12][S10]
10. **Negatives:** exclusions go in the lock block; actions and emotions are written positively, or set with the Emotion Wheel. [S13][S22]
11. **Grade in Higgsfield first** (Color Palette / Relight with a reference). Then add grain and halation in ffmpeg. Upscale last. [S28][S30]
12. **Fix, don't reroll.** Use region edit or Object Swap, chain clips by last frame → start frame, and approve stills before motion. [S31][S4][S16]

### Sources
B = https://higgsfield.ai/blog/ · H = https://higgsfield.ai/creator-hub/

S1 B ai-video-look-real-2026 · S2 B ai-video-prompt-mistakes · S3 B soul-2-vs-nano-banana-pro · S4 H case-studies/sinecera-hybrid-production-higgsfield · S5 B seedance-2-5-prompting-guide · S6 H help-center/getting-started/how-do-i-write-a-good-prompt · S7 B cinematic_headphones · S8 B cinematic · S9 B seedance-prompting-guide · S10 B generating-with-seedance-2-0 · S11 B ai-commercial-youtube-guide · S12 B Kling-3.0-is-on-Higgsfield-User-Guide-AI-Video-Generation · S13 B Santiago-breakdown · S14 H help-center/ai-models/how-do-i-use-seedance · S15 B seedance-2-5 · S16 H help-center/ai-models/how-do-i-use-kling · S17 H help-center/ai-models/how-do-i-use-soul-cinema · S18 B create-custom-ai-moodboard-soul-2, B hex-codes-ai-image-generation-color-control-soul · S19 H help-center/ai-models/how-do-i-use-nano-banana · S20 B seedance4k-breakdown · S22 B cinema-studio-4-0 · S23 H help-center/tools/how-do-i-use-cinema-studio · S24 B ai-video-camera-control · S25 B cinema-studio-3.5-full-tutorial · S26 B how-to-avoid-distortions-ai-videos · S27 B ai-car-commercial-youtube-guide · S28 B video-relight-color-palette-higgsfield · S29 B Relight-Director-Style-Cinematic-Lighting · S30 B Product-Videos-TikTok-Reels-Without-Filming · S31 B edit-ai-video-without-regenerating · S32 B food-product-video-ad-ai-2026
