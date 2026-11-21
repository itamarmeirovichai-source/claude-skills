# How the best AI product commercials are made (2025–2026)

Research brief (2026-10-07). Sources: Fooh, Morphic, Opus, Masonry, NovoAds, ChatCut, Higgsfield. These are mostly vendor blogs, so treat rankings as soft.

## 1. Pipeline used by working AI ad studios
1. **Still first, motion second.** Approve the hero frames like print, then animate them with Kling/Seedance. Fooh's SKIMS and TirTir×Murakami spots were made this way ([fooh](https://www.fooh.com/blog/skims-toothpaste-ai-ad)).
2. **Start and end frames** for controlled reveals. Frame B changes only one variable from frame A, and Kling interpolates with one camera move.
3. **Long image prompts with hard negatives.** Use 300+ words, exact numbers, and lines like "No extra objects. No pedestal. No bending".
4. **Multi-angle product references.** Use front, side and logo close-up; 2–4 strong refs beat a cluttered stack.
5. **Prompt lock.** Paste the identical product description into every shot (Kling Elements / Character ID).
6. **Over-generate and select.** Track cost per accepted clip. Generate long, then use the best 2–3 s.
7. **Mix models.** Seedance for action, sound and multi-reference shots; Kling for static, material-detail and product-fidelity shots.

**Logos and labels:** don't trust the model to render brand text. Composite the real logo and end-card type in post.
- Keep labels front-facing and limit orbits to about 90–120°, otherwise models invent side copy.
- Add "logo remains legible, text intact".
- Use an explicit **add-no list**: "Add no hand, person, prop, ingredient, droplet, splash, mist, bubble, extra text" (drop the items the shot needs).

## 2. Shot vocabulary models obey
- **Camera moves:**
  - slow push-in, pull-back reveal
  - 180/360° orbit (state the degrees and speed)
  - macro / extreme macro
  - top-down flat-lay, low-angle hero
  - tracking, parallax slide
  - crash zoom, whip-pan
  - bullet-time spin, FPV sweep
  - robo-arm move (fast with a hard stop)
  - rack focus
  - locked-off camera with only the object moving
  - handheld drift
- **Time:** "120fps slow motion", droplets frozen mid-air. Do speed ramps in the edit.
- **Light:**
  - chiaroscuro on a dark void with a single sharp beam
  - rim light on glass and metal
  - high-key soft light for beauty
  - pastel seamless
  - golden hour through blinds
  - black acrylic reflections
  - "light catches the facets"
  - Portra 400 skin
- **Restraint:** one camera move per shot, slow reveals, realistic material behaviour.

## 3. Templates
**Hero still:**
```
Premium studio product photograph of [exact product, material, finish, colour HEX], logo "[BRAND]" [position].
Surface [black acrylic / velvet / wet stone]. Lighting [key + rim + fill]. Details [condensation / brushed grain / facets].
85mm f/8, tack sharp, commercial retouching. Exactly one product. No extra objects, no props, no hands, label unchanged.
```

**Kling i2v (start/end):**
```
[one camera move] + [what moves, and only that] + "product shape, logo and label identical to reference; logo legible"
+ Negative: morphing, warping, text distortion, extra objects, floating objects, background shifting.
```

**Kling multi-shot (up to 6 shots, 3–15 s):** for each shot, give the size, the move, the light and the action, plus the prompt lock.

**Seedance 2.x:**
```
@Image1 front, @Image2 side, @Image3 logo; @Audio1 music.
Timecoded beats; one reference for the camera, one for light; "keep text spelled and intact"; add-no list.
```

**Physics-first:** with an anchor image, describe only the forces and the action, not the product.

## 4. Failures and fixes
| Failure | Fix |
|---|---|
| Logo or text morphs on rotation | Composite in post. Orbit ≤120°, front label, logo close-up as a ref. |
| Invented props, steam, copy | Add-no list; one subject per frame. |
| **Liquid pours** (no model passed a Sept 2026 test) | Avoid pours. Use splash or freeze moments, droplets and condensation, and cut around the transfer. |
| Mechanisms warp | Static camera, "only the object moves". |
| Hands and faces | Hands-only interactions; avoid faces; keep hands out of packshots. |
| Drift between shots | Prompt lock, the same reference stack, generate from the previous shot's last frame. |
| Plastic skin | Film-stock language, "visible pores", neutral documentary grade. |

## 5. Editing craft
- **Arc:** slow and mysterious opening → tension → faster detail inserts on the beat → slow final reveal → still hero hold.
- **Speed ramps:** fast-into-slow at impact. Plan matching move directions for match cuts and whip transitions.
- **Sound:** about 3 beats of ASMR or ambience only, then the music hits on a cut. Layer foley (cap click, clink, rustle, tick, whoosh into ramps) and exaggerate impacts.
- **Type:** luxury uses a high-contrast serif, wide tracking, negative space and small sizes. DR uses a bold sans, big benefit and CTA. Always set type in post.
- **End card:** 1.5–3 s on a still hero frame (leave empty space in the last shot), with logo, tagline and CTA.
- **Grade:** one LUT across all models, matched blacks, light grain or halation to hide AI sheen.

## 6. Spec ads that worked, and why
- Liquid Death (Veo 3) spec ad
- Samsung "Ostrich" remake, which led to a paid campaign
- Genre.ai Kalshi/Lindy (100M+ views; the viral moment is tied to the value proposition)
- Fooh SKIMS / TirTir ("what if brand X launched Y")
- Margiela REPLICA AI film

**Shared traits:**
- a concept, not a tech demo
- brand-tone match
- no dialogue, or stylised dialogue
- shots chosen around AI's strengths
- pro finishing: foley, music, real logo, one grade
