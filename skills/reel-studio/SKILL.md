---
name: reel-studio
description: Assemble AI video clips into finished 9:16 reels and ads from a JSON edit spec rendered with ffmpeg - cuts, transitions, speed ramps, effects, split-screen and blocks-to-reality reveals, Hebrew RTL text and captions, logo/packshot, music with ducking, -14 LUFS, Reels/TikTok/Shorts/4:5 exports. Use when editing or exporting short-form video; not for generating the clips themselves.
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
- Python 3.10+, standard library only.
- Fonts are downloaded at runtime from github.com/google/fonts into `~/.cache/reel-studio/fonts`: Heebo (the default, with Hebrew), Rubik, Secular One and JetBrains Mono. If the download fails, libass falls back to DejaVu, which also covers Hebrew.
- Optional: `faster-whisper` for `captions.source: "auto"`. Optional: `pip install bpy==4.5.0` (Python 3.11) for blockouts.

## Quick start
```bash
S=skills/reel-studio/scripts/reelstudio.py
python3 $S fonts                                  # one-time font cache (render also does this)
python3 $S demo-media --out work/media            # synthetic placeholder clips (optional smoke test)
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
5. Blocks → reality: `EGL_PLATFORM=surfaceless python3 scripts/blockout.py examples/blockout/boca_villa.json media/boca_villa_blockout.mp4 --res 540x960 --fps 24` (about 2 minutes on CPU; add `--preview` for a single still). Feed the blockout to the AI model as the V2V guide, then cut both with `layout: "reveal"` using the same `in`/`out` so the geometry lines up. See `examples/blocks_to_reality.json`.

## Commands
| command | purpose |
|---|---|
| `render SPEC [--preset P] [--out F] [--dry-run] [--keep] [--workdir D] [--fast] [-v]` | render. `--dry-run` prints every ffmpeg command. `--workdir` keeps intermediates, including `overlay.ass` |
| `plan SPEC [--preset P]` | validate and print the timeline (start, duration, layout, transition) |
| `probe FILE...` | media info as JSON |
| `grid VIDEO [--cols --rows --width --start --end]` | timestamped contact sheet JPEG (≤190 KB) |
| `cuts VIDEO [--threshold 0.3] [--json]` | scene-cut detection, to split a generated multi-shot clip |
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
| `audio` | music, SFX and loudness (below) |

### Clip (`clip`, `before`, `after`, `left`, `top`, `main`, `inset`, `blockout`, `real`, ...)
A path string, or an object with:
`path` (video or image) or `color` (solid card) · `in`, `out` (source trim) · `duration` (images, cards, or a forced length) · `speed` (0.5 = slow motion) · `ramps: [{from, to, speed}]` (speed ramp; times relative to `in`) · `fit`: `cover` | `contain` | `blur_bg` | `stretch` · `focus: [x, y]` crop anchor 0-1 · `bg` (padding color) · `volume`, `mute` · `effects: [...]`.

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
`cut` (default) · `fade` and every ffmpeg xfade type (`wipeleft`, `slideup`, `circleopen`, `radial`, `pixelize`, `zoomin`, `fadeblack`, `fadewhite`, `smoothleft`, `dissolve`, `hblur`, `coverleft`, `revealright`, ...) · custom: `whip` (`whip_left`/`_right`/`_up`/`_down`, with motion blur), `zoom`, `glitch`, `flash`, `dip`, `slide`.
As an object: `{"type":"fade","dur":0.4,"sfx":"whoosh","sfx_volume":0.7}`. A transition overlaps the two segments, so the timeline gets shorter by its length. Durations are clamped to 90% of the shorter neighbor.

### Effects (per clip, per segment, or global)
All effects accept `start`/`end` for a time window where it makes sense; times are local to the clip.
| type | params |
|---|---|
| `zoom_punch` | `at` (number or list), `scale` 1.15, `dur` (hold; default to the end), `ease` 0.06 |
| `ken_burns` | `from` 1.0, `to` 1.15, `pan` center/left/right/up/down |
| `shake` | `intensity` 12 px, `speed`, `start`, `end` |
| `glitch` / `rgb_split` | `amount`, `rate`, `start`, `end` |
| `flash` / `dip` | `at` (list ok), `dur`, `color`, `strength` |
| `film_grain` | `strength` 10 |
| `vignette` | `angle` 0.55 |
| `letterbox` | `bars` (fraction or px), `color` |
| `lut` | `path` (.cube), `mix` 0-1 |
| `color` | `preset` teal_orange/warm/cool/bw/vibrant/film/moody/flat_original and/or `contrast`, `saturation`, `brightness`, `gamma` |
| `blur`, `sharpen`, `mirror`, `fade` (`in`, `out`, `color`) | |
| `speed_ramp` | sugar for clip `ramps` (`from`, `to`, `speed`) |
| `blur_bg` | sugar for `fit: blur_bg` |

### Text and image overlays
`type`: `text` | `title` | `cta` | `chip` (label box) | `image`.
Text keys: `text`, `start`, `end` or `dur`, `position` (top/upper/center/lower/bottom/title/cta) or `x`,`y`, `align` (ASS numpad, default 5 = centered), `size`, `weight`, `font`, `color`, `stroke`, `stroke_color`, `shadow`, `box`, `box_color`, `pad`, `rotate`, `spacing`, `anim` (fade/pop/slide_up/zoom_in/typewriter/none), `highlight: ["word"]`, `highlight_color`, `dir` (auto/rtl/ltr), `layer`.
Image keys: `path`, `x`, `y`, `width` (reference px), `opacity`, `fade`, `align`, `start`, `end`. Use these for a logo bug or a packshot logo.
**Coordinates** are in the 1080×1920 reference frame and scale to the real canvas (4:5 feed, draft). A float in (0, 1] means a fraction of the canvas.

### Captions
```json
"captions": {"style": "highlight_word", "lines": [{"start": 0.2, "end": 2.0, "text": "שלום לכולם"}]}
```
`source`: `auto` (whisper on the edited audio; `lang` he, `model` small) | `.srt` | `.json` (words) | `.ass` (burned in as is). Alternatively give `lines` (phrase timings; word timings are approximated).
`style`: `clean` | `bold_pop` | `highlight_word` | `karaoke`. Overrides: `size`, `weight`, `max_words`, `max_chars`, `stroke`, `color`, `highlight_color`, `stroke_color`, `position`, `x`, `y`, `uppercase`, `offset`, `box`, `font`, `save_words` (writes the whisper words to edit).

### Audio
```json
"audio": {"original_volume": 1.0,
          "music": {"path": "track.mp3", "in": 0, "volume": 0.35, "fade_in": 0.3, "fade_out": 1.2,
                    "duck": {"threshold": 0.025, "ratio": 10, "attack": 15, "release": 350}},
          "sfx": [{"type": "riser", "at": 2.6}, {"path": "boom.wav", "at": 5, "volume": 0.8, "anchor": 0}],
          "sfx_on_cuts": "auto", "loudnorm": -14, "true_peak": -1.5}
```
Ducking is a sidechain compressor keyed by the clips' own audio (voice and dialogue). Set `duck: false` to turn it off. `music.synth: "bed"` creates a placeholder bed. The built-in SFX are synthesized, with no assets needed: `whoosh`, `swish`, `riser` (its peak lands on `at`), `hit`, `impact`, `pop`, `click`, `glitch`. `sfx_on_cuts: "auto"` picks a sound per transition. A name forces one sound on every cut. Loudness uses two-pass `loudnorm` to `-14` LUFS with a true peak of `-1.5` dBTP; set `false` to skip it.

### Export presets
| preset (aliases) | canvas | video | audio |
|---|---|---|---|
| `instagram` (`reels`, `ig`) | 1080×1920 | H.264 High 4.2, 12 Mb/s | AAC 192k 48 kHz |
| `tiktok` (`tt`) | 1080×1920 | 13 Mb/s | AAC 192k |
| `shorts` (`yt`, `youtube`) | 1080×1920 | 12 Mb/s | AAC 320k |
| `feed` (`4:5`, `4x5`, `feed45`, `ig_feed`, `facebook`) | **1080×1350** | 10 Mb/s | AAC 192k |
| `master` | spec canvas | CRF 16 | AAC 320k |
| `draft` (`preview`) | 480 px wide, keeps the spec's aspect | CRF 27 veryfast | AAC 96k |

All presets output yuv420p, BT.709, 48 kHz stereo and `+faststart`. Keep titles inside the safe zone: the reference y between 250 and 1500 clears the platform UI. `top` (330) and `cta` (1480) are already safe.

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
| זום פתאומי, פאנץ', קפיצת זום על הביט | effect `zoom_punch` with `at: [..beats]` |
| זום איטי, דחיפה פנימה, קן ברנס | effect `ken_burns` (`from` 1, `to` 1.15) |
| רעידה, שייק, מצלמה רועדת | effect `shake` (`intensity` 8-20) |
| גליץ', תקלה דיגיטלית | effect `glitch`; light version: `rgb_split` |
| פלאש, הבזק | effect `flash` with `at` |
| גרעין, מראה של פילם, רטרו | `film_grain` + `color` preset `film` |
| צבע קולנועי, טיל-אורנג' | `color` preset `teal_orange`, or `lut` with a `.cube` |
| חם יותר / קר יותר | `color` preset `warm` / `cool` |
| שחור-לבן | `color` preset `bw` |
| מסגרת קולנועית, פסים שחורים | `letterbox` |
| הכהיה בשוליים, וינייט | `vignette` |
| טשטוש | `blur` (with `start`/`end`) |
| הילוך איטי, סלואו מושן | clip `speed: 0.5` |
| האצה, ספיד ראמפ, להאיץ באמצע | clip `ramps: [{from, to, speed: 2-4}]` |
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
| לוגו בפינה | global overlay `image` (`x`:960, `y`:150, `width`:180, `opacity`:0.85) |
| פאקשוט, סיום עם לוגו וקריאה לפעולה | last segment: image or color clip + `image` logo + `cta` with `box:true` |
| מוזיקה ברקע שיורדת כשמדברים | `audio.music` with `duck` (default on) |
| סאונד בכל מעבר, וושש | `audio.sfx_on_cuts: "auto"` |
| רייזר לפני הדרופ, בום | `sfx` `riser` (lands on `at`) + `impact` |
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
- Renders run segment by segment and keep intermediates lossless-ish (CRF 12-14 MKV). A 30 s 1080p reel takes about 1-3 minutes on CPU. Use `--preset draft` while iterating.

## Files
- `scripts/reelstudio.py`: the engine and CLI (stdlib only).
- `scripts/blockout.py`: Blender blockout generator (JSON scene → greybox MP4).
- `examples/blocks_to_reality.json`: Boca villa blockout → AI reveal (wipe + glitch + flash, a split before/after, a slow-motion LUT shot, a packshot).
- `examples/hebrew_ad.json`: 15 s Hebrew ad (hook, punch-ins, speed ramp, captions, split, logo bug, packshot, ducked music).
- `examples/feed_4x5.json`: 4:5 feed export with PiP.
- `examples/blockout/boca_villa.json`: blockout scene for the villa. `examples/previews/`: a still preview.
- `tests/`: pytest suite. Every test uses synthetic `testsrc`/`sine` media generated on the fly; nothing is downloaded except fonts. Run it with `python3 -m pytest skills/reel-studio/tests -q` (about 4 minutes).

To try an example without real footage: `cd examples && python3 ../scripts/reelstudio.py demo-media --out media && python3 ../scripts/reelstudio.py render hebrew_ad.json --preset draft`. Rendered media goes to `examples/media/` and `examples/out/`, both git-ignored.
