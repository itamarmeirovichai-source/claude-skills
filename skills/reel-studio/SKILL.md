---
name: reel-studio
description: Assemble AI video clips into finished 9:16 reels and ads from a JSON edit spec rendered with ffmpeg - cuts, transitions, smooth velocity speed ramps, beat-synced cuts, effects, split-screen and blocks-to-reality reveals, Hebrew RTL text and kinetic captions, platform safe zones, logo/packshot, music with ducking and layered SFX, -14 LUFS, Reels/TikTok/Shorts/4:5 exports. Use when editing or exporting short-form video; not for generating the clips themselves.
---

# Reel Studio

A programmatic reel editor. You write one JSON edit spec; `scripts/reelstudio.py` renders it with ffmpeg into a finished H.264/AAC reel. Every edit decision lives in the spec, so a revision means editing JSON and re-rendering, never re-cutting by hand.

`scripts/blockout.py` (Blender, `bpy` 4.5) renders flat-colored greybox "blockout" videos that lock layout and camera for AI video-to-video models. Pair the blockout with the AI render and reel-studio cuts the "blocks → reality" reveal.

## When to use
- The user has clips (AI-generated, stock, phone) and wants a reel, ad, teaser, or before/after.
- The user asks for a cut, transition, zoom, shake, glitch, captions, Hebrew titles, logo, music, or a platform export.
- The user wants a blockout → AI-render reveal (architecture, real estate, product, VFX breakdowns).

Do not use it to generate footage (that is the AI video model's job) or for long-form edits over about 3 minutes.

## Requirements
- `ffmpeg` and `ffprobe` on PATH, built with libass, libx264, and the `xfade`, `lut3d`, `loudnorm` and `sidechaincompress` filters (stock Ubuntu ffmpeg ≥ 6 has all of them).
- Python 3.10+, standard library only. Optional for `beats` / `beat_sync`: `librosa` (best; first run 30-50 s of numba JIT) or `numpy` (fast spectral flux); without either a pure-stdlib beat tracker is used.
- Fonts are downloaded at runtime from github.com/google/fonts into `~/.cache/reel-studio/fonts`: Heebo (the default, with Hebrew), Rubik, Secular One and JetBrains Mono. If the download fails, libass falls back to DejaVu, which also covers Hebrew.
- Optional: `faster-whisper` for `captions.source: "auto"`. Optional: `pip install bpy==4.5.0` (Python 3.11) for blockouts.

## Quick start
```bash
S=skills/reel-studio/scripts/reelstudio.py
python3 $S fonts                                  # one-time font cache (render also does this)
python3 $S demo-media --out work/media            # synthetic placeholder clips (optional smoke test)
python3 $S beats music.mp3 --every 2              # BPM, beats, downbeats, cut grid, drop (JSON)
python3 $S plan  spec.json                        # validate + print the resolved timeline
python3 $S render spec.json --preset draft        # fast 480p preview -> <output>_draft.mp4
python3 $S grid  out/reel_draft.mp4 --cols 6 --rows 3   # contact sheet: LOOK at it before final
python3 $S render spec.json                       # final, preset from spec.export (default instagram)
python3 $S render spec.json --preset feed --out out/reel_4x5.mp4
```
Minimal spec:
```json
{
  "output": "out/reel.mp4",
  "timeline": [
    {"clip": {"path": "clips/a.mp4", "in": 0.5, "out": 3.0, "effects": [{"type": "zoom_punch", "at": 0.4}]},
     "overlays": [{"type": "title", "text": "וילה על המים", "position": "top", "anim": "pop"}]},
    {"clip": "clips/b.mp4", "transition": "whip"}
  ],
  "audio": {"music": "music/track.mp3", "sfx_on_cuts": "auto", "loudnorm": -14}
}
```
Paths are relative to the spec file. Times accept `3.5`, `"3.5"`, `"0:03.5"`.

## Workflow Claude follows
1. Run `probe` on every source clip to get its duration, size, fps and audio. Never guess `out` points.
2. Write the spec and run `plan` to catch errors early. Exit code 2 means a spec error, and the message names the field.
3. Render with `--preset draft`, run `grid` on the result, and inspect the contact sheet image: text placement, Hebrew direction, reveal timing, black frames.
4. Fix the spec, then render the final with the target preset. Report the path, duration, size and loudness to the user.
5. Music-driven edit: set `audio.beat_sync` (cuts snap to the beat grid, one cut lands on the drop) and `audio.drop: "auto"` (riser into the drop + impact on it). Run `plan` to see the snapped cuts. Use `"at": "downbeats"` / `"beats"` / `"drop"` in global `effects` for flashes, punches and hit-shakes on the music.
6. Blocks → reality: `EGL_PLATFORM=surfaceless python3 scripts/blockout.py examples/blockout/boca_villa.json media/boca_villa_blockout.mp4 --res 540x960 --fps 24` (about 2 minutes on CPU; add `--preview` for a single still). Feed the blockout to the AI model as the V2V guide, then cut both with `layout: "reveal"` using the same `in`/`out` so the geometry lines up. See `examples/blocks_to_reality.json`.

## Commands
| command | purpose |
|---|---|
| `render SPEC [--preset P] [--out F] [--dry-run] [--keep] [--workdir D] [--fast] [-v]` | render. `--dry-run` prints every ffmpeg command. `--workdir` keeps intermediates, including `overlay.ass` |
| `plan SPEC [--preset P]` | validate and print the timeline (start, duration, layout, transition) |
| `probe FILE...` | media info as JSON |
| `grid VIDEO [--cols --rows --width --start --end]` | timestamped contact sheet JPEG (≤190 KB) |
| `cuts VIDEO [--threshold 0.3] [--json]` | scene-cut detection, to split a generated multi-shot clip |
| `beats MUSIC [--band low\|full] [--every N] [--min-gap 0.3] [--engine auto\|librosa\|numpy\|stdlib]` | JSON: `bpm`, `beats`, `downbeats`, `cuts` (every Nth beat), `onsets`, `drop`. `--band low` (<160 Hz, default) locks on the kick (pop/EDM/trap); `full` for acoustic music |
| `captions VIDEO [--lang he] [--style bold_pop]` | whisper → `.words.json`, `.srt`, styled `.ass` (edit the words, then use them as `captions.source`) |
| `fonts`, `sfx [--out DIR]`, `lut OUT.cube [--kind warm]`, `demo-media [--out DIR]` | font cache, synthetic SFX library, simple LUT, placeholder media |

## Spec reference

### Top level
| key | meaning |
|---|---|
| `canvas` | `{width:1080, height:1920, fps:30, background:"#000000"}`. The `feed` preset forces 1080×1350 |
| `defaults` | `{fit:"cover", font:"Heebo"}` |
| `export` | preset name (below). `--preset` overrides it |
| `output` | output path, relative to the spec. The draft preset appends `_draft` |
| `timeline` | list of segments (required) |
| `overlays` | global text/image overlays on the final timeline (times are global) |
| `effects` | global effects on the joined video, such as grain, a LUT or a vignette |
| `captions` | caption track (below) |
| `audio` | music, SFX, beat sync and loudness (below) |
| `safe_zone` | default `true`: text stays out of the top 14 %, bottom 35 % and 6 % sides (Meta Reels / TikTok UI). `false` turns it off, or `{top, bottom, side}` fractions |

### Clip (`clip`, `before`, `after`, `left`, `top`, `main`, `inset`, `blockout`, `real`, ...)
A path string, or an object with:
`path` (video or image) or `color` (solid card) · `in`, `out` (source trim) · `duration` (images, cards, or a forced length) · `speed` (0.5 = slow motion) · `ramps: [{from, to, speed}]` (hard-step speed ramp; times relative to `in`) · `velocity` (smooth CapCut-style ramp, below) · `freeze` · `boomerang` · `fit`: `cover` | `contain` | `blur_bg` | `stretch` · `focus: [x, y]` crop anchor 0-1 · `bg` (padding color) · `volume`, `mute` · `effects: [...]`.

- `velocity`: speed eased (cosine) between points and integrated into one `setpts`, so the clip accelerates and decelerates smoothly instead of jumping. A preset scaled to the clip (`montage`: normal → 3x → 0.4x → normal; `hero`: 1.5x → 0.35x hold → 1.5x; `bullet`: 3x → 0.3x → 3x; `rush`: normal → 4x), a string `"0:1,1.0:1,1.3:3,2.2:3,2.5:0.4,3.2:0.4,3.5:1"` (source seconds from `in` : speed), `[[t, speed], ...]`, or `{"points"|"preset": .., "steps": 8, "blur": true}`. A 3-frame `tmix` hides duplicated frames in slow parts (`blur: false` to skip). The clip's own audio is dropped; put music and SFX under it. Not combinable with `ramps`; `speed` multiplies it. Effect sugar: `{"type": "velocity", "preset": "montage"}`.
- `freeze`: `{"at": 1.5, "dur": 1.5, "zoom": 1.12, "saturation": 0.2}` (or just the `at` number) inserts a held frame at `at` (clip time) with a punch-in and desaturation (the "this is the client" intro). The clip gets `dur` longer and the audio pauses; add a title overlay with `start` = `at` and an `sfx` `scratch`.
- `boomerang: true`: plays the trimmed clip forward then backward (double length). `reverse` buffers the clip in memory, so keep it to about 3 s.

### Segment
`layout` (default `full`) · `transition` (into this segment) · `duration` · `effects` (applied to the composed segment) · `overlays` (times relative to the segment) · `label_style` (chip style override).

| layout | keys |
|---|---|
| `full` | `clip` |
| `split_vertical` / `split_horizontal` | `top`/`bottom` or `left`/`right`, `ratio`, `divider:{width,color}` or `false`, `labels:{top:..}`, `audio`: side name, `mix` or `none` |
| `split_wipe` | `before`, `after`, `at`, `wipe_dur`, `direction` right/left/down/up, `keys:[[t,p],..]` (custom path), `line:{width,color,glow}` or `false`, `labels`, `audio` |
| `before_after_slider` | like `split_wipe`, but the line sweeps back and forth (or follows custom `keys`) |
| `reveal` | **blocks → reality**: `blockout`, `real`, `mode` wipe/slider/split/split_vertical/cut, `at`, `wipe_dur`, `direction`, `glitch:true`, `flash:true`, `labels:{blockout, real}` |
| `pip` | `main`, `inset`, `size` (0.38), `inset_aspect`, `corner` top_right/bottom_left/…, `border`, `border_color`, `inset_label`, `audio` |
| `input_prompt_result` | `result`, `input` (image), `prompt` (string or `{text|file, scroll:auto|timecodes|none}`), `title`, `labels`, `background:"blur"` or a color |

### Transitions
`cut` (default) · `fade` and every ffmpeg xfade type (`wipeleft`, `slideup`, `circleopen`, `radial`, `pixelize`, `zoomin`, `fadeblack`, `fadewhite`, `smoothleft`, `dissolve`, `hblur`, `coverleft`, `revealright`, ...) · custom: `whip` (`whip_left`/`_right`/`_up`/`_down`, with motion blur), `zoom`, `glitch`, `flash`, `dip`, `slide`, `light_leak` (aliases `leak`, `film_burn`: crossfade with a warm gradient blob screen-blended over it, 0.6 s) · hard-cut window transitions: `spin` (A rotates out 45°, B rotates in, zoomed to hide corners, blurred; 0.4 s) and `zoom_through` (Premiere crash zoom: 100 → 300 % into the cut, 300 → 100 % out of it, blurred; 0.34 s).
As an object: `{"type":"fade","dur":0.4,"sfx":"whoosh","sfx_volume":0.7}`. A crossfade-type transition overlaps the two segments, so the timeline gets shorter by its length; `spin` and `zoom_through` are cuts with an effect window of `dur` centred on the cut and do not shorten it. Durations are clamped to 90% of the shorter neighbor. Taste: at most two transition types per reel; no glitch/spin/VHS for luxury, real estate or food.

### Effects (per clip, per segment, or global)
All effects accept `start`/`end` for a time window where it makes sense; times are local to the clip. In the global `effects` list, `at` can also be `"beats"`, `"downbeats"`, `"cuts"` or `"drop"` (from the music analysis; `max` caps the count), e.g. `{"type":"flash","at":"downbeats","dur":0.07}`. More than 3 flashes per second triggers a photosensitivity warning: flash on every 2nd or 4th beat.
| type | params |
|---|---|
| `zoom_punch` | `at` (number or list), `scale` 1.15, `dur` (hold; default to the end), `ease` 0.06 |
| `ken_burns` | `from` 1.0, `to` 1.15, `pan` center/left/right/up/down |
| `shake` | `intensity` 12 px, `speed`, `start`, `end` |
| `glitch` / `rgb_split` | `amount`, `rate`, `start`, `end` |
| `flash` / `dip` | `at` (list ok), `dur`, `color`, `strength` |
| `film_grain` | `strength` 10 (luma noise). `mode: "overlay"`: real film grain, monochrome, `size` 2 (grain px), `opacity` 0.35 (0.2 subtle, 0.5 heavy); survives IG compression better |
| `vignette` | `angle` 0.55 |
| `letterbox` | `bars` (fraction or px), `color` |
| `lut` | `path` (.cube), `mix` 0-1 |
| `color` | `preset` teal_orange/warm/cool/bw/vibrant/film/moody/flat_original and/or `contrast`, `saturation`, `brightness`, `gamma`, `temperature` (Kelvin: 3000 warm, 6500 neutral, 9000 cool), `vibrance` (-2..2, protects skin), `curves` (vintage/cross_process/darker/lighter/increase_contrast/linear_contrast/medium_contrast/strong_contrast/negative/color_negative) |
| `blur`, `sharpen`, `mirror`, `fade` (`in`, `out`, `color`) | |
| `impact_shake` | decaying hit shake: `at` (list ok), `intensity` 28 px, `decay` 9, `freq` 70. Pair with `zoom_punch` 1.08 and a `hit` SFX on the same time |
| `handheld` | subtle drift that makes a static AI shot look filmed: `intensity` 18 px, `speed` 1, `start`, `end` |
| `motion_blur` | `frames` 5 (3-9), `start`, `end`. Hides AI morphing in fast moves. Windows use trim+concat (tmix with `enable` turns chroma green) |
| `echo` | light trails (`lagfun`): `decay` 0.94 (0.90 short, 0.97 very long), `start`, `end` |
| `glow` | highlight bloom / 35mm halation: `threshold` 0.7, `sigma` 25, `strength` 0.6, `tint` (default red-orange halation; `white` = bloom). Blended in RGB so it never goes magenta |
| `vhs` | camcorder look: low-res, chroma bleed, noise, tracking band, scanlines, `start`, `end`. Add a date stamp as a text overlay (Heebo has no ▶) |
| `duotone` | brand colors: `shadows` (#0B1E4D), `highlights` (#FF9A3C), `start`, `end` |
| `speed_ramp` | sugar for clip `ramps` (`from`, `to`, `speed`) |
| `velocity` | sugar for clip `velocity` (`preset` or `points`, `steps`, `blur`) |
| `blur_bg` | sugar for `fit: blur_bg` |

### Text and image overlays
`type`: `text` | `title` | `cta` | `chip` (label box) | `image`.
Text keys: `text`, `start`, `end` or `dur`, `position` (top/upper/center/lower/bottom/title/cta) or `x`,`y`, `safe` (default true, see safe zone), `align` (ASS numpad, default 5 = centered), `size`, `weight`, `font`, `color`, `stroke`, `stroke_color`, `shadow`, `box`, `box_color`, `pad`, `rotate`, `spacing`, `anim` (fade/pop/slide_up/zoom_in/typewriter/none), `highlight: ["word"]`, `highlight_color`, `dir` (auto/rtl/ltr), `layer`.
Image keys: `path`, `x`, `y`, `width` (reference px), `opacity`, `fade`, `align`, `start`, `end`. Use these for a logo bug or a packshot logo.
**Coordinates** are in the 1080×1920 reference frame and scale to the real canvas (4:5 feed, draft). A float in (0, 1] means a fraction of the canvas.

### Captions
```json
"captions": {"style": "highlight_word", "lines": [{"start": 0.2, "end": 2.0, "text": "שלום לכולם"}]}
```
`source`: `auto` (whisper on the edited audio; `lang` he, `model` small) | `.srt` | `.json` (words) | `.ass` (burned in as is). Alternatively give `lines` (phrase timings; word timings are approximated).
`style`: `clean` | `bold_pop` | `highlight_word` | `karaoke` (Primary = sung color, Secondary = not yet) | `pop` (CapCut bounce 40 → 118 → 100 % in 160 ms, 1-3 words) | `slide` (each group slides in from the reading side: right for Hebrew, in 180 ms) | `stack` (hierarchy: the key word big, highlighted and popping in the centre, the other words small above and below; the key word is the first match of `emphasis: ["word"]`, else the longest word; `big_size` 160). Overrides: `size`, `weight`, `max_words`, `max_chars`, `stroke`, `color`, `highlight_color`, `stroke_color`, `position`, `x`, `y`, `uppercase`, `offset`, `box`, `font`, `emphasis`, `big_size`, `safe`, `save_words` (writes the whisper words to edit).

### Audio
```json
"audio": {"original_volume": 1.0,
          "music": {"path": "track.mp3", "in": 0, "volume": 0.35, "fade_in": 0.3, "fade_out": 1.2,
                    "duck": {"threshold": 0.025, "ratio": 10, "attack": 15, "release": 350}},
          "sfx": [{"type": "riser", "at": 2.6}, {"path": "boom.wav", "at": 5, "volume": 0.8, "anchor": 0}],
          "sfx_on_cuts": "auto", "loudnorm": -14, "true_peak": -1.5}
```
More audio keys:
- `beat_sync`: `true` or `{every: 1, band: "low", engine: "auto", snap: "floor", min_len: 0.4, drop: true, drop_segment: N, end: true, offset: 0, beats: [..]}`. Analyses `music` (respecting its `in`) and rewrites segment durations so every cut (the midpoint of a crossfade) lands on the beat grid (`every` 2 = every other beat). `snap: "floor"` only shortens clips (never holds a last frame); `"nearest"` may lengthen. With `drop` (default true) the cut nearest the detected drop (within 2.5 s) lands exactly on it, or the start of segment `drop_segment`. `end` snaps the reel end to a beat. A segment with `"beat_sync": false` keeps its length. `beats` (music seconds) skips the analysis. `plan` prints the snapped cuts.
- `drop`: `"auto"` (detected: biggest jump in bass energy) or seconds on the timeline. With `drop_sfx` (default true, or `{riser, impact, riser_volume, impact_volume}`) a `riser` peaks on the drop and an `impact` hits on it.
- `sfx_on_cuts: "layered"` (or `{"type": "layered", "hit": true, "volume": 0.7}`): every cut gets a `whoosh` whose peak lands on the cut plus a `whoosh_low` sub layer, and optionally a `hit`. A transition's own `sfx` wins; `"sfx": "none"` silences one cut.
- `sfx_library`: a folder of `<name>.wav` (whoosh.wav, hit.wav, riser.wav, ...) or `{name: path}`. Files replace the synthetic sound of that name; `whoosh`/`whoosh_low`/`swish`/`riser` files are placed by their loudest point (peak on the cut), others by their start. Any `sfx` item also takes `"align": "peak"` or an explicit `anchor`.

Ducking is a sidechain compressor keyed by the clips' own audio (voice and dialogue). Set `duck: false` to turn it off. `music.synth: "bed"` creates a placeholder bed. The built-in SFX are synthesized, with no assets needed: `whoosh` (peak lands on `at`), `whoosh_low` (sub layer), `swish`, `riser` (its peak lands on `at`), `hit`, `impact`, `pop`, `click`, `glitch`, `scratch` (record scratch). `sfx_on_cuts: "auto"` picks a sound per transition. A name forces one sound on every cut. Loudness uses two-pass `loudnorm` to `-14` LUFS with a true peak of `-1.5` dBTP; set `false` to skip it.

### Export presets
| preset (aliases) | canvas | video | audio |
|---|---|---|---|
| `instagram` (`reels`, `ig`) | 1080×1920 | H.264 High 4.2, 12 Mb/s | AAC 192k 48 kHz |
| `tiktok` (`tt`) | 1080×1920 | 13 Mb/s | AAC 192k |
| `shorts` (`yt`, `youtube`) | 1080×1920 | 12 Mb/s | AAC 320k |
| `feed` (`4:5`, `4x5`, `feed45`, `ig_feed`, `facebook`) | **1080×1350** | 10 Mb/s | AAC 192k |
| `master` | spec canvas | CRF 16 | AAC 320k |
| `draft` (`preview`) | 480 px wide, keeps the spec's aspect | CRF 27 veryfast | AAC 96k |

All presets output yuv420p, BT.709, 48 kHz stereo and `+faststart`.

### Safe zone (on by default)
The platform UI covers the top ~14 % (account bar), the bottom ~35 % (caption, CTA button, music) and ~6 % on each side (Meta Reels ads / TikTok guidance). With `safe_zone` on, every text overlay and caption block is measured (approximate box from size, characters and lines) and moved inside the zone. Named positions are placed silently (`lower`, `bottom`, `cta` end up just above the 65 % line); an explicit `x`/`y` that had to move prints a warning with the old and new reference coordinates. `"safe": false` on one overlay or caption track, or `"safe_zone": false` at the top level, keeps the exact position. Layout labels (chips) and image overlays are not moved.

## Hebrew phrase → spec mapping
Users often brief in Hebrew. Translate their words directly into spec entries:

| the user says | spec |
|---|---|
| חיתוך חד, קאט, בלי מעבר | `"transition": "cut"` |
| מעבר רך, פייד, דיזולב | `"transition": {"type": "fade", "dur": 0.4}` (`dissolve`) |
| מעבר מהיר, וויפ, סוויש | `"transition": "whip"` (+ `"sfx": "whoosh"`) |
| מעבר זום | `"transition": "zoom"` |
| מעבר לבן, הבזק במעבר | `"transition": "flash"` |
| ירידה לשחור, דיפ לשחור | `"transition": "dip"` or `fadeblack` |
| מעבר גליץ', מעבר תקלה | `"transition": "glitch"` |
| מעבר סיבוב, ספין | `"transition": "spin"` |
| צלילה פנימה, קראש זום, מעבר זום אמיתי | `"transition": "zoom_through"` |
| דליפת אור, פילם ברן | `"transition": "light_leak"` |
| זום פתאומי, פאנץ', קפיצת זום על הביט | effect `zoom_punch` with `at: [..beats]` |
| זום איטי, דחיפה פנימה, קן ברנס | effect `ken_burns` (`from` 1, `to` 1.15) |
| רעידה, שייק, מצלמה רועדת | effect `shake` (`intensity` 8-20) |
| שירעד כשהוא נוחת, רעידה על המכה | effect `impact_shake` with `at` (+ `zoom_punch` 1.08 + `hit`) |
| שייראה מצולם ולא AI, פחות סטרילי, מצלמת יד | `handheld` + `film_grain` `mode: "overlay"` 0.3 + `glow` 0.4 |
| מושן בלר, טשטוש תנועה | `motion_blur` (with `start`/`end` for the fast part) |
| טריילים, אפקט אקו, שובל אורות | `echo` (`decay` 0.94) |
| גליץ', תקלה דיגיטלית | effect `glitch`; light version: `rgb_split` |
| פלאש, הבזק | effect `flash` with `at` |
| גרעין, מראה של פילם, רטרו | `film_grain` + `color` preset `film` |
| גרעין אמיתי, גריין של פילם | `film_grain` with `mode: "overlay"`, `opacity` 0.25-0.4 |
| לוק וינטג', רטרו חם | `color` with `curves: "vintage"` + `film_grain` overlay + `vignette` |
| VHS, כמו קלטת, שנות ה-90 | `vhs` |
| דואוטון, בצבעי המותג | `duotone` (`shadows`, `highlights` = brand colors) |
| הילה, בלום, היילייטים זוהרים, האלביישן | `glow` (`tint` white = bloom, default = red halation) |
| לוק חם, שקיעה | `color` with `temperature: 4500`, `vibrance: 0.15` |
| צבע קולנועי, טיל-אורנג' | `color` preset `teal_orange`, or `lut` with a `.cube` |
| חם יותר / קר יותר | `color` preset `warm` / `cool` |
| שחור-לבן | `color` preset `bw` |
| מסגרת קולנועית, פסים שחורים | `letterbox` |
| הכהיה בשוליים, וינייט | `vignette` |
| טשטוש | `blur` (with `start`/`end`) |
| הילוך איטי, סלואו מושן | clip `speed: 0.5` |
| האצה, ספיד ראמפ, להאיץ באמצע | clip `ramps: [{from, to, speed: 2-4}]` |
| וולוסיטי, ספיד ראמפ חלק, שיאיץ ואז יאט | clip `velocity: "montage"` (or points `"0:1,1:1,1.3:3,2.2:3,2.5:0.4"`) |
| רגע הירואי באיטי, סלואו באמצע | clip `velocity: "hero"` |
| תקפיא ותכתוב מי זה, פריז פריים | clip `freeze: {"at": 1.5, "dur": 1.5}` + title overlay at `at` + `sfx` `scratch` |
| בומרנג, הלוך-חזור | clip `boomerang: true` (≤ 3 s) |
| שיהיה על הביט, תסנכרן למוזיקה, חיתוך על הביט | `audio.beat_sync: {"every": 2}` (`beats` command to inspect) |
| תחתוך מהר יותר | `beat_sync.every: 1` |
| שה-reveal ייכנס על הדרופ | `beat_sync` (drop on by default) or `drop_segment: N` + `audio.drop: "auto"` |
| פלאשים על הביט, הבזקים על הביט | global effect `flash` with `"at": "downbeats"`, `dur` 0.07 (max 3/s) |
| זום על כל ביט | global effect `zoom_punch` with `"at": "beats"` |
| מסך מפוצל, אחד מעל השני / זה ליד זה | `split_vertical` / `split_horizontal` |
| לפני-אחרי, וילון, מחיקה | `split_wipe` |
| סליידר לפני-אחרי | `before_after_slider` |
| מבלוקים למציאות, מהבלוקאאוט ל-AI, חשיפה | `layout: "reveal"` (`mode` wipe/split/cut, `glitch`, `flash`) |
| תמונה בתוך תמונה, חלון קטן בפינה | `pip` |
| פרומפט על המסך, מה כתבתי ומה יצא | `input_prompt_result` |
| כותרת, טקסט קופץ | overlay `title` with `anim: "pop"` |
| טקסט שנכתב אות-אות, מכונת כתיבה | `anim: "typewriter"` |
| להדגיש מילה בצהוב | `highlight: ["מילה"]` |
| כתוביות, תמלול | `captions` (`auto` = whisper, or `lines`) |
| כתוביות מילה-מילה, קריוקי | caption `style` `highlight_word` / `karaoke` |
| כתוביות גדולות של 1-2 מילים | caption `style: "bold_pop"` |
| כתוביות קופצות, באונס של קאפקאט | caption `style: "pop"` |
| כתוביות שנכנסות מהצד | caption `style: "slide"` |
| להדגיש את המילה החשובה, מילה גדולה באמצע | caption `style: "stack"` (+ `emphasis: ["מילה"]`) |
| שהטקסט לא יוסתר ע"י הכפתורים, אזור בטוח | `safe_zone` (on by default); `"safe": false` to place exactly |
| לוגו בפינה | global overlay `image` (`x`:960, `y`:150, `width`:180, `opacity`:0.85) |
| פאקשוט, סיום עם לוגו וקריאה לפעולה | last segment: image or color clip + `image` logo + `cta` with `box:true` |
| מוזיקה ברקע שיורדת כשמדברים | `audio.music` with `duck` (default on) |
| סאונד בכל מעבר, וושש | `audio.sfx_on_cuts: "auto"` |
| סאונד עשיר, שכבות סאונד, שהמעברים יישמעו מקצועי | `audio.sfx_on_cuts: "layered"` (whoosh peak on the cut + sub, `hit: true`) |
| יש לי קבצי סאונד משלי | `audio.sfx_library: "sfx/"` (whoosh.wav, hit.wav, riser.wav...) |
| רייזר לפני הדרופ, בום | `audio.drop: "auto"` (riser into the drop + impact), or `sfx` `riser` (lands on `at`) + `impact` |
| לנרמל ווליום, עוצמה לאינסטגרם | `audio.loudnorm: -14` (default) |
| לרילס / לטיקטוק / לשורטס / לפיד 4:5 | `--preset instagram` / `tiktok` / `shorts` / `feed` |
| טיוטה מהירה לבדיקה | `--preset draft` |

## Hebrew and RTL rules
- Text goes through libass with complex shaping (HarfBuzz + FriBidi). Every Hebrew line gets an RLM prefix, so lines that start with "AI", digits or English still lay out right-to-left, and punctuation lands on the correct (left) side. Use `"dir": "ltr"` to opt out.
- Write Hebrew in logical order, exactly as typed. Never pre-reverse it.
- Emoji do not render (libass has no color glyphs). Use words or `→ ←` arrows instead.
- `\N` or a newline inside `text` breaks the line.

## Gotchas
- Source clips are normalized: scaled and cropped (`fit`), resampled to the canvas fps, with 48 kHz stereo audio. A clip without audio gets silence. Images loop for `duration`.
- Text and segment overlays start at the segment start, which falls inside the incoming transition. Add `start: 0.3` if the text must appear after the transition.
- For a reveal, both clips must come from the same timeline: the same `in`/`out`, and an AI render made from that blockout. Otherwise the wipe exposes misaligned geometry.
- `before_after_slider` is a looping sweep, so give it ≥3 s. `split_wipe` hides the line once the wipe finishes.
- Velocity clips are silent (the speed curve would warble the audio): put music and SFX under them. `velocity` and `ramps` cannot be combined.
- Beat sync rewrites segment `duration`s. In `floor` mode a clip only gets shorter; a cut moved onto the drop may hold the last frame (warned), so give that clip a later `out`. Downbeats are every 4th beat from the strongest bass phase, an approximation: if a flash lands mid-bar, shift `beat_sync.offset`.
- `--band low` beat tracking needs a kick drum; for acoustic music use `band: "full"`. The first librosa call compiles for 30-50 s; `engine: "numpy"` is near-instant.
- Never put Hebrew in `drawtext`: mixed Hebrew/English/digits comes out in the wrong order. Everything here goes through ASS with `Encoding=-1` and an RLM at the start of every line (verified pixel-by-pixel in research T6).
- Renders run segment by segment and keep intermediates lossless-ish (CRF 12-14 MKV). A 30 s 1080p reel takes about 1-3 minutes on CPU. Use `--preset draft` while iterating.

## Files
- `scripts/reelstudio.py`: the engine and CLI (stdlib only).
- `scripts/blockout.py`: Blender blockout generator (JSON scene → greybox MP4).
- `examples/blocks_to_reality.json`: Boca villa blockout → AI reveal (wipe + glitch + flash, a split before/after, a slow-motion LUT shot, a packshot).
- `examples/hebrew_ad.json`: 15 s Hebrew ad (hook, punch-ins, speed ramp, captions, split, logo bug, packshot, ducked music).
- `examples/feed_4x5.json`: 4:5 feed export with PiP.
- `examples/blockout/boca_villa.json`: blockout scene for the villa. `examples/previews/`: a still preview.
- `tests/`: pytest suite. Every test uses synthetic `testsrc`/`sine` media generated on the fly; nothing is downloaded except fonts. `test_t6.py` covers velocity, beats and beat sync, the T6 effects/transitions, layered SFX, kinetic captions and the safe zone. Run it with `python3 -m pytest skills/reel-studio/tests -q` (about 5 minutes; the librosa test is skipped if librosa is missing).

To try an example without real footage: `cd examples && python3 ../scripts/reelstudio.py demo-media --out media && python3 ../scripts/reelstudio.py render hebrew_ad.json --preset draft`. Rendered media goes to `examples/media/` and `examples/out/`, both git-ignored.
