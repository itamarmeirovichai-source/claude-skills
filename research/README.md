# Award-level interactive website job — 4 runs

| Folder | Run | Status |
|---|---|---|
| `run1-award-level-web/` | Phase 1 — the research (PART A + PART B) | Done |
| `run2-bot-capabilities/` | Phase 2 — the bot's capability module (PART C) | Done |
| `run3-smash-house-proposal/` | Phase 3 — the Smash House Burgers proposal (PART A + PART D + PART E) | Done |
| `run4-blender-handoff/` | Phase 4 — build the Blender scene | Handoff prepared; must run on the Mac with Blender + MCP |

## Delivery to ChatGPT — one conversation, in this order
1. `run1-award-level-web/01` → `07`, one message at a time, waiting for "Got it" each time.
2. `run2-bot-capabilities/PART-C-capabilities.md`. (Custom GPT: paste PART C into Instructions and upload the Run 1 files as Knowledge instead.)
3. `run3-smash-house-proposal/01` → `08`, one message at a time.
4. Later, once Run 4's frames and glTF exist: *"The rendered frames and the glTF are ready, named exactly per the asset contract — switch the signature section from the fallback to the frames."*

Not for ChatGPT: the Hebrew `00-PART-A-*.md` files, and `run3-.../09-PART-E-pitch.md`, which is for showing the owner.

## Known limits, stated plainly
- **The client's site could not be fetched** — `smashhouseburgers.com` is blocked by this environment's egress policy. Run 3's step-1 re-verification did not happen; every fact carries a `[TO CONFIRM]` tag, and the PART E diagnosis is written as claims with the measurement that confirms each, not as an audit.
- **Most research sources could not be deep-read** for the same reason (awwwards.com, threejs.org and others). Run 1's README records what was verified by search, what is inferred, and what is an estimate.
- **Run 4 was not executed** — it needs hardware this container does not have.
