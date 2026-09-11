# Run 3 — Phase 3: THE EXAMPLE SITE (Smash House Burgers, Boca Raton)

A concept proposal site spec. Not their official site — it ships `noindex` with a "Concept proposal for Smash House Burgers" footer tag.

| File | Contents |
|---|---|
| `00-PART-A-hebrew.md` | PART A — the chosen concept, in Hebrew, for the operator. **Not for ChatGPT.** |
| `01`–`08` | PART D — the spec as 8 self-contained "CHATGPT MESSAGE X of 8" chunks (items 1, 3–18) |
| `09-PART-E-pitch.md` | PART E — the diagnosis, the one-page pitch and the 60-second demo script, for showing the owner. **Not for ChatGPT.** |

## Delivery
Paste `01` → `08` into the same ChatGPT conversation that already has the research (Run 1) and the capabilities (Run 2), one message at a time. Message 1 tells it to wait for all 8 before building.

Later, when Run 4's frames and glTF exist, send:
> The rendered frames and the glTF are ready, named exactly per the asset contract — switch the signature section from the fallback to the frames.

## Honest limits of this run
- **The client's site could not be fetched.** `smashhouseburgers.com` is blocked by this environment's network egress policy, so step 1's re-verification did not happen. Every fact comes from the brief and carries a `[TO CONFIRM]` tag where it matters; the spec instructs the builder to keep those tags visible until resolved.
- **The diagnosis in PART E is therefore a template, not an audit.** Each of the five bullets is written as a claim with the measurement that confirms it. Confirm them before showing the owner.
- Contrast ratios in section 14 were computed from the brand hexes and are exact. Three of them fail WCAG for body text — the spec names which and what to use instead.

## Decisions made in this run
- Concept: **THE SMASH**, chosen over THE GRIDDLE and KONG'S HOUSE.
- Beat timings tightened by 1–2% each; the explode and the cut got the extra room.
- Pinned length 620vh desktop / 420vh mobile; 248 desktop frames / 124 mobile.
- Creativity pass added **SHABBAT MODE** and **THE PASS**; rejected THE WEIGHT as scroll-jacking without a story reason.
- Added to the asset contract: a **label anchor track** (`/frames/labels.*.json`). Pre-rendered frames give the code no 3D positions, so Blender must export the per-frame projected label anchors or the explode labels cannot track their layers.
