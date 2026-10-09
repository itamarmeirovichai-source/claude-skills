# Run 1 — Phase 1: THE RESEARCH (award-level interactive websites)

Output of Run 1 of the 4-run job. Nothing here is a spec or an implementation — it is the knowledge base that Runs 2 and 3 consume, and that gets pasted into ChatGPT first.

## Files

| File | Contents |
|---|---|
| `00-PART-A-hebrew.md` | PART A — 10 key lessons, Hebrew, for the operator only. **Not for ChatGPT.** |
| `01-foundations.md` | CHATGPT MESSAGE 1 of 7 — Section A: Foundations catalog (F1–F15) |
| `02-wow-catalog-1.md` | CHATGPT MESSAGE 2 of 7 — Section B part 1: Wow catalog W1–W10 |
| `03-wow-catalog-2.md` | CHATGPT MESSAGE 3 of 7 — Section B part 2: W11–W22 + verified reference sites |
| `04-assets-smoothness.md` | CHATGPT MESSAGE 4 of 7 — Section C: Asset toolkit · Section D: Smoothness playbook |
| `05-3d-sequence-camera.md` | CHATGPT MESSAGE 5 of 7 — Section E: 3D product sequence deep dive · Section F: Animation & camera cheat sheet |
| `06-deepdive-deconstruction-tiers.md` | CHATGPT MESSAGE 6 of 7 — Section G: 15 highest-impact food techniques · Section H: 8 real award-winning sites · Section I: $5k/$20k/$100k |
| `07-food-pipeline-lessons.md` | CHATGPT MESSAGE 7 of 7 — Section J: Photoreal food pipeline · Section K: The 25 lessons |

## How to deliver

Paste files `01` → `07` into ONE ChatGPT conversation, in order, one message at a time, waiting for "Got it — send the next part." after each. Message 7 ends by asking for the 10 lessons back.

Every chunk is self-contained English, under 20,000 characters, and never refers to this conversation.

## What was verified vs. what is knowledge

- **Verified by search this run:** GSAP is 100% free including all plugins since April 30 2025 (Webflow); SplitText rewritten ~50% smaller. CSS scroll-driven animations ship in Chrome/Edge and Safari 26; Firefox still flagged. Lenis 1.3.26 defaults and the GSAP-ticker integration (read from the Lenis README directly). Three.js WebGPURenderer with automatic WebGL2 fallback, TSL recommended. Blender 5.0 (ACES colour, NanoVDB volumes, Cycles Render Time pass), Apple Silicon only, Metal GPU rendering. Mobile scanning app landscape (Polycam / Scaniverse / KIRI / RealityScan). AI image and video tool landscape and the fact that commercial rights vary by provider and tier. The award status of the reference sites in Section H.
- **Explicitly marked as inferred:** the technical stack of every reference site in Section H, unless the studio published a case study.
- **Marked as estimates:** Cycles render times per frame.
- **Not verified (network egress blocked):** awwwards.com, threejs.org and several blog sources could not be deep-read from this environment; their facts come from search result summaries and are flagged where it matters.

## Search budget used

12 web searches (the cap), 1 successful deep read (Lenis README); 5 further deep-read attempts were blocked by the network egress policy.

## Next runs

- **Run 2** ← paste files `01`–`07` (PART B) → produces PART C, the bot capability module (≤7,500 chars).
- **Run 3** ← paste PART C + sections C, D, E and J from here → produces the Smash House Burgers proposal spec + code.
- **Run 4** ← paste Run 3's 8-beat sequence, asset contract, motion tokens and 3D asset plan → builds the Blender scene over a Blender MCP. Must run on the Mac with Blender open, not here.
