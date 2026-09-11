CHATGPT MESSAGE 5 of 8 — THE EXAMPLE SITE. Continue applying the spec exactly. Don't build yet — wait until you have all 8 parts.

# 12. ASSET PLAN

## Priority order — never break it
1. **Their real assets.** Logo, the "Kong Arm" cut-out, and every food photo and illustration on their CDN.
2. **Rendered in Blender** from real scans of a real Loaded Smashed: the hero burger and its nine layers, the cut halves, the knife, the steam, the sauce drip.
3. **Real photography** — a phone shoot of the Boca location and the food, shot to the style contract below.
4. **AI generation**, only for what 1–3 cannot cover, with the prompt recorded.
5. **Licensed stock** — last resort, never in a hero.

**No placeholders ship. Every asset gets a row in the rights ledger: path, type, source, tool and plan tier, date, licence, where used.**

## THE STYLE CONTRACT — paste this block into every image prompt, unchanged
```
[LENS] 85mm macro equivalent, f/3.2, camera slightly above the subject at a 25-30 degree angle
[LIGHT] one large soft key from back-left at 120 degrees, white bounce front-right at 15 percent, deep falloff into shadow
[PALETTE] near-black #13110C ground, Smash Red #E51144 accents only, warm #FEEB13 rim light on the top edge
[SURFACE] matte dark stone or seasoned black steel, a few real crumbs and sesame seeds scattered
[GRADE] high contrast, deep blacks, warm specular highlights, slight vignette
[GRAIN] fine 35mm grain at 3 percent
```
Every asset — photographed, rendered or generated — obeys this one block. Mixed lighting across assets is the loudest possible signal of an amateur site.

## THE KOSHER CONTRACT — paste into every food prompt, unchanged
```
Kosher meat restaurant. No dairy anywhere: all cheese is plant-based, with a matte melt and slightly less stringy pull than dairy cheese, never a glossy dairy sheen. No pork: "beef bacon" is deep red, thick-cut, with no white marbled fat strips. No butter, no cream, no milk products, no shellfish. Never show meat and cheese described as dairy in the same frame.
```

---

## A. Their existing assets — collect and optimise these first
| Asset | Source | Treatment |
|---|---|---|
| Logo | `https://cdn.smashhouseburgers.com/wp-content/uploads/2024/07/29163847/Logo_new2.webp` | Re-export as SVG if obtainable `[TO CONFIRM]`; otherwise AVIF at 2×, 3 sizes |
| Kong Arm cut-out | `https://cdn.smashhouseburgers.com/wp-content/uploads/2026/07/07175624/kong_part.webp` | Clean the alpha edge, re-export AVIF with alpha at 1200×1200 and 800×1000 |
| Food photos + illustrations | `cdn.smashhouseburgers.com` — **lazy-loaded on their current site**, so read the rendered page or the `data-lazy-src` attributes, not the raw HTML | Re-encode to AVIF/WebP, regenerate the full `srcset`, colour-match to the style contract |
| Kong full character art | Their existing illustration `[TO CONFIRM source file]` | This is the source art for the Rive rig — request layered source (AI/PSD/SVG) from the client; do not redraw him |

---

## B. From Blender — the 3D pipeline (real scans first)
| Asset | Output |
|---|---|
| Hero burger, 9 named layers | `/frames/desktop/smash_0001–0248.avif` · `/frames/mobile/smash_0001–0124.avif` · `/models/hero.glb` (≤3MB) · `/models/hero.usdz` |
| Cut halves + knife | Included in the sequence · `/models/halves.glb` (≤5MB) |
| Steam, sauce drip, loose sesame | Rendered into the frames; approximated in real-time as sprites/shaders |
| Kong arm pass | `/frames/kong/desktop/kong_0001–0019.avif` (alpha) · mobile equivalent |
| Poster + reduced-motion keys | `/frames/poster.avif`, `/frames/key/key_040|118|160|205.avif` |
| Blooming Onion | A 40-frame unfold sequence at 1200×1200, alpha, OR a real-time model — **whichever is produced; do not substitute a rotating photograph** |
| Menu mini-explode | 12-frame sequences at 800×800, alpha, one per featured item |

Capture instructions for the scans (what the client or photographer does by hand): buy three Loaded Smashed — one intact, one disassembled, one cut in half. Photograph each separately on a matte grey or black surface under flat, shadowless light. Use **photo/photogrammetry mode, not LiDAR** — LiDAR cannot resolve sesame seeds. Turntable plus a fixed phone on a tripod: three orbits at roughly 15°, 45° and 70° elevation, 40–60 photos each, 120–180 total per layer. Lock exposure, focus and white balance. Let the steam stop completely before shooting, and dull the shine on the sacrificial burger only — glossy highlights break photogrammetry.

---

## C. Everything else — source, spec and a ready-to-paste prompt

| # | Asset | Where | Spec | Source |
|---|---|---|---|---|
| 1 | Griddle surface (hero + footer) | Hero backdrop, griddle footer | 2400×1350, AVIF, seamless-tileable variant at 1024² | **Photo** — shoot their actual flat-top after service, or AI if access isn't possible |
| 2 | Boca storefront at dusk | Location page hero | 2400×1350, 16:9 | **Photo, must be real.** Never generate a storefront — it is the one image a local customer can disprove |
| 3 | Interior / counter | Location page, About | 1600×1200, 4:3 | **Photo, must be real** |
| 4 | Menu item photos (full menu) | Menu page | 1200×1200 square, AVIF, ThumbHash placeholder each | **Photo first** (their CDN photos, or a shoot); AI only to fill gaps, flagged in the ledger |
| 5 | Dirty Fries hero | Menu, hero rotation | 2000×2000 | Photo or AI |
| 6 | Blooming Onion hero | Menu | 2000×2000 + the 40-frame unfold | Photo + Blender |
| 7 | Catering spread | Catering page | 2400×1350 | **Photo of a real catering setup** `[TO CONFIRM they have one]`; AI only as a clearly-labelled concept image |
| 8 | Gift card face | Gift card moment | 1600×1000, plus a flat vector for the 3D card | **Design it** in their brand kit — not generated |
| 9 | App screenshots | App section | Real device frames | **From the client** `[TO CONFIRM]` — never mock up a fake app UI |
| 10 | Kosher certification mark | Header, footer, menu | SVG | **From the certifying agency, with permission** `[TO CONFIRM]`. Until then, text lockup only |
| 11 | OG share images | Every page | 1200×630 | Generated per page with `@vercel/og` from real photos + the logo |
| 12 | Favicon / app icons | Site-wide | SVG + 180px + 192/512 maskable | From the logo |
| 13 | Ticket paper texture | Menu rail | 1024×1536 tileable | Scan a real receipt, or AI |
| 14 | Grain / noise overlay | Site-wide | 256×256 tileable PNG | Generate procedurally, 3% opacity |

### Ready-to-paste prompts (each already includes where to insert the two contracts)

**Griddle surface**
```
[STYLE CONTRACT] [KOSHER CONTRACT]
Photorealistic top-down macro photograph of a well-seasoned commercial flat-top griddle surface, black carbon-seasoned steel, faint circular scouring marks, a thin sheen of hot oil catching the rim light, a few loose sesame seeds and crumbs, no food, no hands, no text, no logos, seamless texture, high detail
```

**Dirty Fries hero**
```
[STYLE CONTRACT] [KOSHER CONTRACT]
Photorealistic macro food photograph of loaded fries: crisp golden shoestring fries piled high, topped with shredded pulled beef brisket, a drizzle of glossy amber chef sauce, thinly sliced scallion, served in a black paper tray on matte dark stone, steam rising subtly, sauce catching the back light, no cheese, no sour cream, no text, no logos, no hands, shallow depth of field
```

**Blooming Onion**
```
[STYLE CONTRACT] [KOSHER CONTRACT]
Photorealistic macro food photograph of a whole battered blooming onion, petals fully open like a flower, deep golden-brown crisp coating with visible craggy batter texture, a small ramekin of dipping sauce beside it, matte black stone surface, back-lit so the crisp edges glow, faint steam, no cheese, no dairy dip, no text, no logos, no hands
```

**Catering spread (concept only, must be labelled as such)**
```
[STYLE CONTRACT] [KOSHER CONTRACT]
Photorealistic overhead photograph of a kosher burger catering spread on matte black steel: two large trays of smashed burgers in paper wrappers, a tray of shoestring fries, a tray of popcorn chicken, small sauce ramekins, stacked black napkins, no people, no cheese pull, no dairy items, no text, no logos, even soft back-light, slight steam
```

**Menu item gap-fill (substitute the real item name and its real ingredient list, nothing invented)**
```
[STYLE CONTRACT] [KOSHER CONTRACT]
Photorealistic macro food photograph of [EXACT ITEM NAME], built exactly as: [REAL INGREDIENT LIST IN ORDER]. Plant-based cheese with a matte melt. Served on matte dark stone, three-quarter view, sesame seeds sharply defined, sauce glossy under the back light, subtle steam, no text, no logos, no hands, shallow depth of field
```

**Ticket paper texture**
```
Photorealistic flat scan of a blank thermal kitchen order ticket, slightly curled at one edge, faint horizontal print banding, warm off-white paper with a subtle fibre texture, one small grease spot, no text, no printing, no logos, seamless vertical tile, evenly lit, no shadows
```

---

## D. Sound
| Sound | Source |
|---|---|
| Sizzle (hero bed, smash press) | **Record it.** A pan on a hob, phone 30cm away, 20 seconds. This beats any library. |
| Thud / slam (beat 6, kosher stamp) | Record: a heavy book dropped on a wooden table, pitched down 3 semitones |
| Griddle scrape (beat 1) | Record: a metal spatula on a pan |
| Blade shear (beat 7) | Record: a knife through a firm vegetable, plus a light metallic ring layered under it |
| Whoosh ×5 (the toss) | Record or licensed; pitch each ±3% so they never sound identical |
| Printer chatter | Record a real receipt printer, or licensed |
| UI ticks, button presses | Record or licensed; ≤80ms each |
| Kong roar, burp | **Licensed or performed** — do not generate a realistic animal sound without clear commercial rights |
| Ambient bed | Licensed (check the plan covers client work) or composed |

Processing: trim UI clips to ≤80ms, normalise to −6dBFS, high-pass at 80Hz, export as **one Howler sprite sheet**, randomise playback rate ±3% so repeated clips never machine-gun. **Off by default. Visible toggle. Unlock on the first user gesture. Fade out on tab blur.**

## E. Kong for Rive
Rig the client's **existing** character art — request the layered source file. Do not redraw him; a redrawn mascot is the fastest way to lose a pitch. State machine inputs: `pointerX`, `pointerY`, `hoverOrder`, `smashImpact`, `isShabbat`, `isMotzeiShabbat`, `holidayKey`, `tapCount`. States: idle (always running, 3s loop), eye-track, shades-down, chest-beat, sleeping (Shabbat), costume variants per holiday. Target ≤180KB `.riv`.

## F. Rights ledger — ship this table with the build
`path | type | source (client CDN / photo / scan+Blender / AI / licensed) | tool + plan tier | date | licence text or URL | where used`
An asset with no row does not ship. For every AI-generated asset, the exact prompt goes in the ledger too.
