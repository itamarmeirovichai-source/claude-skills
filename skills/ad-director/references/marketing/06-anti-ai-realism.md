# Making AI films stop looking "too AI" (from 23 YouTube tutorials, read in full)

On 2026-10-07 the client said VESPER v2 "looks too AI". Our tells: glossy CGI, perfect symmetry, over-saturated golden glow, plastic surfaces, too-smooth slow motion, a centred hero packshot every shot, uniform slow push-ins.

## Sources
- S3 Dan Kieft, "Why my AI videos look ultra realistic": https://youtu.be/0B_xyflXrwc
- S4 Higgsfield, "3-step ultra-realistic AI ads": https://youtu.be/3rDs6FhFoUQ
- S9 Youri van Hofwegen, "AI videos free": https://youtu.be/I9EvujHJm3o
- S11 Youri van Hofwegen, "Master Higgsfield": https://youtu.be/M73BrFnVPA8
- S12 "Kling 4.0 vs Seedance 2.5": https://youtu.be/YH1LLoBPx0Y
- S13 Kieft, Seedance 2.5 realism: https://youtu.be/Zo8KaTs0l6k
- S14 Kling 3.0 tutorial: https://youtu.be/c8huoAtXGew
- S17 Waqas Qazi, "digital grain looks awful": https://youtu.be/hlaf4V_9C_4
- S18 Grow With Miz: https://youtu.be/mSIQZGZm4c8
- S19 Creating with Conor, "7 things": https://youtu.be/pZRROwTYDqk
- S20 Scott Burchell, digital to film: https://youtu.be/rTvqPoQ3FpQ
- S21 Martin Bue: https://youtu.be/sCaPrLBQMEs
- S1 film grain: https://youtu.be/-tA8JoOVQt4
- S2 Dehancer: https://youtu.be/066tDE9AT-A
- S10 4 steps: https://youtu.be/LsfcOoCc88I

## Core ideas
- **Realism comes from imperfection.** Too symmetrical, too polished and evenly sharp all read as uncanny (S13, S21).
- **Spend 99% of the effort on the still**, because the video model only moves it (S3, S13).

## Stills
- **Ban the AI look by name** (S11): "no HDR, no oversaturation, no digital sharpening, no plastic/waxy surfaces, no beauty smoothing, natural film grain, gentle vignette". Banning things works better than asking for a look.
- **Describe light physically:** hard, motivated, directional light that falls off fast (not soft hazy glow), with a warm key against a cool background (S3, S11, S19). Prefer daylight around 5600 K and avoid HDR contrast (S21).
- **Camera language:** "shot on a 35mm lens, aperture 1.8, shallow depth of field, visible fine film grain, muted desaturated color grade" (S13), or "shot on a Canon EOS R5" (S21). Vary lenses: a 16 mm wide (proves the space is real), macro, a low 24 mm, an 85 mm shallow (S11).
- **Composition:** rule of thirds ("left third", "slightly off center") (S3), three-quarter angles rather than head-on (S4), foreground/mid/background layers.
- **Lived-in detail:** name specific imperfections (a fingerprint, a dust mote, a water ring, a creased card). "Make it messy" doesn't work (S19, S21).
- **Texture:** every edit pass softens detail, so mask the original high-detail still back in, then run an enhancer pass (S4, S21). Keep small text out of generations and comp labels in post (S11).
- **References:** a product sheet (front + three-quarter view) on grey with flat light, because baked-in light carries over. Instruct the model to *relight* the product to match the scene. A layout map image locks position and scale (S4, S11).

## Motion
- **Never use a locked-off camera.** Prompt "handheld, breathing with tiny corrective movements, barely noticeable push" and put "locked off static camera" in the negative (S9).
- **Describe movement, not gear.** "FPV drone" renders a drone (S11).
- **Subtle motion.** Presence, not animation (S21).
- **Kill AI slow-mo.** "already at full speed, no deceleration", and trim the model's dramatic slow-mo (S11, S13). Start and end frames ease in and settle, so cut before the settle.
- **Intentional camera.** Rack focus triggered by an action, a slow dolly arc, a snorricam locked on the product with the world whipping past (S4, S13). Worm's-eye, top-down.
- **Models:** Seedance 2.5 looks more real and holds consistency through motion; Kling showed "a bit of plastic look" (S11, S12). Draft at 480p, then upscale the winner (S11). Change one variable per test, and write hard cuts inside one prompt for multiple angles (S9, S14).

## Post (film emulation)
- **Grain sits IN the image.** Soften first (defocus/MTF/blur), then add grain, then a light sharpen. Never put grain over a razor-sharp frame (S17, S20). Remove grain from deep shadows (S1).
- **The S20 film chain:**
  1. log
  2. correct
  3. blur
  4. film-stock colour
  5. grain
  6. subtle halation and bloom
  7. dirt
  8. **flicker**
  9. sharpen
  10. gate weave
  11. Kodak 2383 print LUT
- **Grade down:** −contrast, −highlights, −saturation, slightly muted (S18). Never sharpen or smooth. Use HSV-style saturation (S2).
- **Edit-level imperfection:** slow 100→120% punch-ins, subtle camera shake only where it's motivated, 2.39 bars optional (S13, S18).
- **Cut from many takes:** "the finished ad is the best few seconds out of 100 tries". Match cuts and cut on action (S4).
- **Sound:** layer at different distances (close, mid, far), with a sub hit on the cut (S9, S13, S21).

## ffmpeg translation (ours)
Order the filters: `fps=24` → `gblur=sigma=0.6` (or `unsharp` with a negative amount) → `eq=contrast=0.94:saturation=0.86` + `curves` (lift blacks slightly, roll off highlights) → glow/halation (low) → `noise=alls=7:allf=t` → `unsharp=3:3:0.3` → slight `vignette` → a 2–3% luma flicker → encode with `-tune grain`, high bitrate.

## Top 15 fixes, ranked
1. Ban list in every prompt (no HDR, oversaturation, sharpening, plastic).
2. Hard, motivated light falling off fast; warm key, cool fill.
3. Grade down: contrast, highlights, saturation.
4. Softening → grain → light sharpen, never grain on razor-sharp.
5. Subtle halation and bloom plus gentle flicker.
6. No locked-off camera: handheld micro-moves.
7. Kill AI slow-mo.
8. Break the centred packshot: thirds, three-quarter angle, depth layers.
9. Shot variety: 16 mm wide, macro, low 24 mm, 85 mm shallow, top-down, snorricam.
10. Named real-world imperfections on surfaces.
11. Protect texture: mask original detail back in.
12. Lens and depth of field on every still.
13. Product reference sheets plus a layout map; comp labels in post.
14. Best seconds of many takes, match cuts, slow punch-ins.
15. Layered diegetic sound at distances, plus a sub hit.
