# Frames

The scroll sequence is a pre-rendered Blender Cycles sequence, not a real-time
render. These files are produced by
`.github/workflows/render-burger-frames.yml`, which shards
`research/run4-blender-handoff/scripts/photoreal/pr_render.py` across runners
and commits the result.

- `desktop/smash_0001.webp` … `smash_0108.webp` — 1440×810, RGBA, transparent film
- `mobile/smash_0001.webp` … `smash_0054.webp` — 810×1080, RGBA
- `labels.desktop.json`, `labels.mobile.json` — where each layer's label sits on
  screen, per frame, in 0..1 view space. Generated in under a second with
  `pr_render.py --no-render`, because it is only projection, not rendering.
- `poster.webp` — one still, shown by CSS if the sequence cannot load.

Regenerate the label tracks alone after any change to the choreography:

    cd research/run4-blender-handoff/scripts/photoreal
    python3 pr_render.py --variant desktop --no-render --labels ../../../../site/frames/labels.desktop.json
    python3 pr_render.py --variant mobile  --no-render --labels ../../../../site/frames/labels.mobile.json
