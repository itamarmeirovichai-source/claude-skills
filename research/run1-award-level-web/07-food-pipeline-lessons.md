CHATGPT MESSAGE 7 of 7 — RESEARCH RESULTS. These are the results of deep research into how award-level interactive websites (Awwwards / FWA level) are built. Study them carefully — this is your knowledge base from now on. Don't build anything yet. Reply only: "Got it — send the next part."

# J. PHOTOREAL FOOD PIPELINE — real burger → web

## J.1 Capture: scanning a real burger, layer by layer
1. **Buy two** — one to scan intact, one to take apart. Buy a third for the cut half.
2. **Disassemble onto a matte, non-reflective surface** (grey card or black felt). Scan each layer separately: top bun, sauce-covered bun face, caramelised onion clump, beef bacon strips, plant-based cheese slice (melted, from the real burger), each patty, bottom bun. Also scan one **cut half**, cut face up.
3. **App:** Polycam (iOS/Android/web; LiDAR + photogrammetry; Gaussian splats; free tier exports glTF only, paid tiers export OBJ/FBX/USDZ/PLY and more), Scaniverse (free Classic mode, unlimited on-device splats and mesh export), KIRI Engine (strong on Android and on featureless objects), RealityScan. For small food objects use **photo/photogrammetry mode, not LiDAR** — LiDAR resolution is too coarse for sesame seeds.
4. **Capture formula:** turntable (a lazy Susan) + fixed phone on a tripod. 3 orbits at ~15°, ~45° and ~70° elevation, 40–60 photos per orbit → 120–180 total. Lock exposure, focus and white balance. Diffuse, shadowless light (overcast window or two big softboxes) — baked-in shadows ruin the albedo.
5. **Fight the shine:** food is glossy and photogrammetry hates specular highlights. Use a circular polariser on the lens if you have one, cross-polarise the lights if you can, or dull the surface with a light dusting of matting spray / cornstarch **on the sacrificial burger only**. Let steam fully stop before capturing.
6. **Deliver:** OBJ or glTF + textures per layer into the scans folder, named `scan_bun_top`, `scan_patty_a`, `scan_half_left`, etc.

## J.2 Cleanup & retopology in Blender
- Import → **Decimate (Collapse)** to ~5–10% for a 300k-tri scan, or use Quadriflow/Remesh for a clean quad cage where you'll deform.
- Target budgets: hero render layers 80–200k tris each (Cycles doesn't care much); real-time export 8–20k tris per layer.
- **Origins:** `Object → Set Origin → Origin to Geometry (Bounds Centre)` on every layer, then move each origin to the layer's own centre so the explode and rotation happen in place.
- **UVs:** scans arrive with usable UVs from the app; for procedural detail add a second UV set with Smart UV Project.
- **Bake the scan's texture** into a clean 4K albedo, then hand-build roughness/normal on top — raw scan textures have baked lighting that must be flattened (Photoshop/Affinity: subtract a heavy-blur version to remove low-frequency shading).

## J.3 Materials that make food read as real (Cycles, Principled BSDF)
| Layer | Recipe |
|---|---|
| Bun | Subsurface (Random Walk), radius ~(2.0, 1.2, 0.8)mm scaled to scene, weight 0.15–0.25; base albedo warm tan; roughness 0.55 broken up by a fine noise; a subtle bump from a crumb texture; **top crust darker and glossier** than the sides |
| Sesame | Geometry Nodes: `Distribute Points on Faces` (density weighted by a vertex-paint mask on the crown) → `Instance on Points` a low-poly seed with random scale 0.85–1.15 and random rotation → `Realize` only for the handful that need physics |
| Sauce | Roughness 0.12–0.25 with a noise-driven variation, Coat weight 0.3, IOR 1.45, slight transmission; drips modelled as geometry, never a texture |
| Caramelised onion | Translucent (thin), high roughness variance, a strong normal map for the fibre, darker at the edges via a gradient in the shader |
| Beef bacon | Deep red base with a darker sear, anisotropic-ish streaks from a stretched noise, roughness 0.3, a light specular sheen (never white marbled fat — that reads as pork) |
| Plant-based cheese melt | Roughness 0.35, Coat 0.15, **no transmission**; the melt shape is modelled (a soft-body drape or sculpted), not painted; slightly matter and less stringy than dairy — that's the honest look and it still reads delicious |
| Patty, seared crust | Base dark brown; **Displacement (Displacement + Bump, adaptive subdivision)** from a high-frequency noise + a crust mask; roughness 0.4 with wet, low-roughness pooling in the crevices; a thin emissive-free grease sheen from a second glossy layer |
| Cut interior faces | A separate material: pinker centre, visible meat fibre via an anisotropic stretched noise, juice pooling (very low roughness patches), cheese cross-section with a soft edge, sauce smear. **This face is where realism is won or lost.** |

## J.4 The cut
Pre-model the halves: duplicate the assembled burger, apply a Boolean with a thin cube, then **manually rebuild the cut face geometry** — inset, extrude slightly inward, sculpt the interior irregularity, and assign the interior material. A raw Boolean face is flat, perfectly planar and instantly reads as CG. Model the chef's knife with a real bevel (0.2mm) and a slightly anisotropic steel material; the "glint" is an area light streaked across the blade, animated, not a texture.

## J.5 Simulations
- **Steam:** a Quick Smoke domain with low density, high dissipation, `Principled Volume` with scatter ~0.6, lit from **behind** the subject. Blender 5.0 runs smoke/fire on NanoVDB, which improves volumetric quality and memory use. Bake to `.vdb` before the final render — never simulate during a render job.
- **Sauce drip:** for one or two drips, animate a modelled blob along a curve with a squash-and-stretch shape key. A full fluid sim is slower to art-direct and rarely looks better at this scale.
- **Sesame rigid bodies:** convert ~30 seeds to rigid bodies for the shake beat, bake to keyframes (`Object → Rigid Body → Apply Transformation` / bake to Action), then delete the sim.

## J.6 Lighting & camera (food-commercial grammar)
- **Key:** one large area light *behind and above* at 120–140° from camera — backlight is what makes sauce, grease and steam glow. Size it ~2× the subject.
- **Fill:** a white plane (or a low-intensity area light) front-left at ~15% of key.
- **Rim/brand light:** a small coloured area light in the brand's accent hue at low intensity, just enough to tint the edge. This is how you put a brand into a render without tinting the food.
- **World:** dark (near-black) with a low-strength HDRI for reflection detail only — Poly Haven (CC0) studio HDRIs.
- **Camera:** 85–100mm, f/2.0–2.8, DOF on, focus on the front third of the cut face. Real motion blur enabled (shutter 0.5) for the toss beats.
- **Colour:** Blender 5.0 ships ACES colour management. Use AgX or ACES view transform — the default Standard view clips highlights and is the fastest way to make food look plasticky.

## J.7 Rendering on Apple Silicon
- Blender 5.0+ requires Apple Silicon (M1 or newer) and macOS 13+. Cycles renders via **Metal** GPU with unified memory — large food scenes that would exhaust a discrete GPU's VRAM often fit comfortably on 16GB+ of shared memory.
- **Denoising:** use **OpenImageDenoise** (OptiX is NVIDIA-only). Enable it for the final pass, and enable the Denoising Data passes (Albedo + Normal) for better edge retention on sesame and crust.
- **Samples:** 512–1024 with adaptive sampling (noise threshold 0.01) for hero frames; 24–64 for look-dev test frames.
- **Render-time estimate (treat as an estimate, measure on your own machine):** a 1920×1080 food frame with SSS, volumetrics and DOF typically lands in the **30s–3min** range per frame on an M-series GPU at production samples. 240 frames therefore = roughly **2–12 hours**. Cut it by: baking volumetrics to VDB, reducing volume step size only where needed, lowering adaptive threshold to 0.02, disabling motion blur on static beats, rendering at 1600px and upscaling, and using persistent data (`--enable-autoexec` + `Render → Performance → Persistent Data`).
- Blender 5.0's Cycles also adds a **Render Time pass** — render one frame with it to find which objects are actually costing you.

## J.8 Rendering scroll image sequences
| Parameter | Recommendation |
|---|---|
| Frame count | 200–280 desktop for an 8-beat sequence (25–35 frames per beat); 100–140 mobile |
| Frame rate | The sequence isn't played at a frame rate — it's indexed by scroll. But author the Blender timeline at 30fps so easing curves feel right |
| Resolution | Desktop 1920×1080; mobile 1080×1350 (portrait crop of a separately-framed camera, not a squeeze) |
| Background | **Rendered background**, not alpha, for the hero — it lets you use real volumetrics, bounce light and DOF on the backdrop. Use alpha (`Film → Transparent`) only for elements that must composite over live DOM (a Kong arm, a floating layer) |
| Format | AVIF q45–55 (≈60–110KB/frame at 1080p). WebP q80 as a fallback for older Safari |
| Naming | `/frames/desktop/smash_0001.avif` … zero-padded to 4, 1-indexed, one flat folder per device |
| Colour space | Render in Filmic/AgX or ACES, **export sRGB** with the view transform applied. Tag the files sRGB — untagged AVIF on Safari shifts colour |
| Budget | Desktop 18–26MB total, mobile 5–8MB — acceptable only with progressive loading (every 8th frame first) |
| Progressive loading | Load stride 8 → 4 → 2 → 1; play from whatever is loaded; prefetch ±20 frames around the playhead |

## J.9 Baking a lightweight real-time glTF from the same scene
1. Duplicate the collection → `Decimate` each layer to 8–20k tris.
2. **Bake** Combined (or Diffuse+Glossy with Direct+Indirect) lighting from the Cycles scene into a 2K texture per layer → assign to an unlit/`MeshBasicMaterial`-friendly setup, or bake Diffuse-only and keep a light PBR setup with one baked env map.
3. Export glTF 2.0 with **Draco** compression, `+Y up`, apply modifiers, and **preserve object names exactly** as the asset contract specifies.
4. Post-process on the command line:
```bash
npx @gltf-transform/cli optimize hero.glb hero.opt.glb \
  --compress meshopt --texture-compress ktx2 --texture-size 2048
```
5. Verify names survived: `npx @gltf-transform/cli inspect hero.opt.glb`.
6. Target: ≤3MB for the full layered burger, ≤5MB including the halves and knife.

## J.10 The mistakes that make CG food look fake
1. **Everything is uniformly clean.** Real food is asymmetric, crumby, smeared. Add mess.
2. **No subsurface on the bun** — bread without SSS looks like painted foam.
3. **Uniform roughness.** Grease pools; crust is dry. Roughness must vary across every surface via a noise or mask.
4. **A flat boolean cut face.** Model the interior.
5. **Front-lit.** Backlight is the entire language of food photography. Front light kills gloss and steam.
6. **No steam / no motion.** Hot food that isn't steaming reads as plastic.
7. **Perfectly stacked layers.** Real burgers lean, slide and squash under their own weight.
8. **Too-perfect sesame distribution** — scatter with density variation and a bald patch.
9. **Wrong scale on the SSS radius** — subsurface set in "Blender units" on a scene modelled in centimetres makes the bun glow like wax.
10. **Standard view transform** — use AgX/ACES or the highlights clip to white plastic.
11. **No contact shadows / floating objects** — food sits *in* its surface, slightly compressing.
12. **Cheese modelled as a flat slice.** Melt is drape, sag, and edges that follow the patty's contour.
13. **Too much DOF.** Macro blur that hides 80% of the burger looks like a cover-up. f/2.8, not f/1.2.
14. **Over-saturated red meat.** Real seared beef is brown on the outside; keep the pink only in the cross-section.
15. **Identical objects in a multi-object shot** — vary each burger's tilt, sesame pattern and sauce smear, or the toss reads as a clone army.

---

# K. THE 25 LESSONS (ordered by impact)
1. One idea, described in one sentence, that every section echoes — this is the entire difference between expensive and busy.
2. Nothing may stutter. One dropped frame on a real phone undoes every other decision on this list.
3. Foundations are part of "insane": a 5MB hero image or a broken form kills a $100k site instantly.
4. Art direction must survive with animation off — if the static screenshot isn't beautiful, motion won't save it.
5. Original assets beat effects. Real photos, real scans, path-traced renders. Stock food photography is visible from orbit.
6. Direct every signature moment like a film: setup → action → payoff, with one surprise the visitor didn't expect.
7. Motion needs physics and intent — anticipation, squash, follow-through, arcs. Decorative motion reads as cheap.
8. One motion language sitewide: one ease, one duration scale, one stagger value, written down.
9. Deterministic scroll sequences should be rendered frames; only interactive moments need real-time 3D — and bake both from the same scene.
10. Every animated property must be a pure function of scroll progress, so scrubbing backwards is perfect.
11. Cap DPR, run one rAF loop, animate only transform and opacity, and decode heavy assets before their section arrives.
12. The wow must end on the CTA, and a conversion click must never wait for an animation.
13. Design the 390px view first. Most visitors, and most of your risk, live there.
14. Every hover has a touch equivalent, and every effect has a low-GPU and a reduced-motion version that still tells the story.
15. Real DOM text and headings behind every canvas — for SEO, for screen readers, and for the day WebGL fails.
16. Accessibility is a craft constraint, not a compliance checkbox: contrast, focus rings, keyboard paths, captions, 24px targets.
17. Make the site reflect the real world — live hours, weather, holidays, a mascot that knows the shop is closed. Highest trust per pixel there is.
18. The client must be able to edit content without you. A site they can't update is a site that dies in six months.
19. Sound design, off by default with a visible toggle, makes a site feel finished — and it's the cheapest wow on the list.
20. Every asset needs a defined source and a licence row. No placeholders ever ship.
21. Never invent facts for a client: no fake prices, reviews, awards or quotes. Mark unknowns and ask.
22. Preloaders are a tax — cap at ~1.5s, never block content that's already ready, always show real progress.
23. Measure on a real mid-range Android and a real iPhone in Low Power Mode, not on your laptop.
24. Invent more than you need, then cut — the best moments come from the fifth idea, not the first.
25. Details finish the illusion: the favicon, the scrollbar, the selection colour, the 404, the empty state, the footer.

---
Now reply with the 10 most important lessons you learned.
