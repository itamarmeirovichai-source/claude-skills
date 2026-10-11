# Pre-built Blender scene (Run 4, partial)

Built headless with the `bpy` 5.0.1 Python module in a cloud container — **not** through a Blender MCP on the Mac, and **not** from real scans. It is a contract-correct scene to open and continue from, not a finished photoreal render.

| Path | What |
|---|---|
| `smash_v04.blend` | The scene: 9 named layers, cut halves, knife, 5 toss burgers, 248 keyed frames, the continuous camera take, lighting, Cycles settings |
| `models/hero.glb` | The 9 layers, Draco — all contract names verified inside the file |
| `models/halves.glb` | `burger_half_left/right`, `cut_face_left/right`, `knife_blade/handle` |
| `frames/labels.desktop.json` · `labels.mobile.json` | The label anchor track, frames 78–147, normalised 0–1, origin top-left |
| `tests/test_0040.png` · `0118` · `0205` | Low-sample test frames from beats 2, 4 and 7 — 1280×720, 96 samples, CPU |

Reproduce everything from scratch: `scripts/build_01_layers.py` → `build_02_cut_knife.py` → `build_03_anim_camera_light.py` → `build_04_export_gltf.py`, with `render_tests.py` for the check renders.

**Realism verdict: this does not look like real food, and is not meant to yet.** The geometry is procedural stand-in. Replace each layer's mesh with a scan, keeping every object name unchanged, and the animation, camera and label track keep working.
