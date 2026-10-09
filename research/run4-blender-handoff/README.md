# Run 4 — handoff package (the run itself cannot execute here)

Phase 4 builds the Blender scene through a Blender MCP. It requires the Mac with Blender open and an MCP connected; this cloud Linux container has neither, so the run was not attempted.

**`out/` now contains a pre-built scene** made headless with the `bpy` Python module in this container — contract-correct, but built from procedural stand-in geometry, not scans. `PART-F-build-log.md` is the honest build log. Open `out/smash_v04.blend` on the Mac and continue from it; everything that needed your hardware (the scans, the final render) is still yours to do.

`RUN4-PROMPT.md` is the complete, ready-to-paste input for the full run: the Run 4 instructions and steps, plus exactly the four things the master prompt says to carry over from Run 3 — the 8-beat sequence, the asset contract, the motion tokens, and the 3D part of the asset plan. It was assembled programmatically from the Run 3 files, not retyped, so the spec and the scene cannot drift apart.

## How to run it
1. Open Blender on the Mac and connect the Blender MCP.
2. Start Claude Code (or the Claude desktop app) in that session.
3. Fill in the two paths at the top of `RUN4-PROMPT.md` (scans folder, Blender project folder).
4. Paste the whole file, then type `RUN MODE: 4`.

The run may span several fresh sessions — state lives in the saved `smash_vXX.blend`, and each session starts with the MCP connection check.

## One addition Run 4 owes the website
Step 11: export `/frames/labels.desktop.json` and `/frames/labels.mobile.json` — per-frame projected screen positions of each layer origin across beats 4–5, in normalised 0–1 viewport coordinates. Pre-rendered frames give the site's code no 3D positions, so without this file the ingredient labels cannot track their layers.
