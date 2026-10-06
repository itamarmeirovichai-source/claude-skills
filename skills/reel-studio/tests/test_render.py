"""Integration tests: real ffmpeg renders of synthetic clips (low-res canvas for speed)."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import (SKILL, duration, ffprobe, frame_rgb, integrated_lufs, rs, small, vstream,
                      write_spec)

SCRIPT = SKILL / "scripts" / "reelstudio.py"


def render(media: Path, name: str, spec: dict, preset: str = "draft", **kw) -> Path:
    p = write_spec(media, name, spec)
    out = media / "out" / f"{name}.mp4"
    return Path(rs.render(str(p), preset, str(out), fast=True, **kw))


def has_audio(path) -> bool:
    return any(s["codec_type"] == "audio" for s in ffprobe(path)["streams"])


def test_trim_concat_cuts(media):
    spec = small({"timeline": [
        {"clip": {"path": "media/clip1.mp4", "in": 0.5, "out": 2.0}},
        {"clip": {"path": "media/clip2.mp4", "in": "0:01", "out": "0:02.5"}},
        {"clip": {"path": "media/noaudio.mp4", "duration": 1.0}},
        {"clip": {"path": "media/logo.png", "duration": 1.0, "fit": "contain", "bg": "#202020"}},
        {"clip": {"color": "#FF0000", "duration": 0.5}}],
        "audio": {"loudnorm": False}})
    out = render(media, "concat", spec)
    assert duration(out) == pytest.approx(1.5 + 1.5 + 1.0 + 1.0 + 0.5, abs=0.1)
    v = vstream(out)
    assert (v["width"], v["height"]) == (480, 854) and v["pix_fmt"] == "yuv420p"
    assert has_audio(out)
    # last segment is a solid red card
    px = frame_rgb(out, 5.3)
    r, g, b = px[0], px[1], px[2]
    assert r > 200 and g < 60 and b < 60


def test_xfade_transitions_and_speed_ramp(media):
    spec = small({"timeline": [
        {"clip": {"path": "media/clip1.mp4", "out": 2}},
        {"clip": {"path": "media/clip2.mp4", "out": 3, "ramps": [{"from": 1, "to": 2, "speed": 2}]},
         "transition": {"type": "fade", "dur": 0.5}},
        {"clip": {"path": "media/clip3.mp4", "out": 2}, "transition": "whip"},
        {"clip": {"path": "media/clip1.mp4", "out": 2, "speed": 0.5}, "transition": "glitch"},
        {"clip": {"path": "media/clip2.mp4", "out": 1.5}, "transition": {"type": "circleopen", "dur": 0.4}},
        {"clip": {"path": "media/clip3.mp4", "out": 1.5}, "transition": "zoom"},
        {"clip": {"path": "media/clip1.mp4", "out": 1.5}, "transition": "flash"},
        {"clip": {"path": "media/clip2.mp4", "out": 1.5}, "transition": "dip"}],
        "audio": {"loudnorm": False}})
    ctx = rs.Ctx(spec, media)
    plans = rs.plan_timeline(spec, ctx)
    assert plans[1]["plan"].dur == pytest.approx(2.5, abs=0.05)   # 1 + 1/2 + 1
    assert plans[3]["plan"].dur == pytest.approx(4.0, abs=0.05)   # slow-mo 0.5x
    total = plans[-1]["start"] + plans[-1]["plan"].dur
    out = render(media, "transitions", spec)
    assert duration(out) == pytest.approx(total, abs=0.1)


ALL_EFFECTS = [
    {"type": "zoom_punch", "at": [0.2, 1.0], "dur": 0.4},
    {"type": "ken_burns", "from": 1.0, "to": 1.2, "pan": "left"},
    {"type": "shake", "start": 0.5, "end": 1.2, "intensity": 10},
    {"type": "glitch", "start": 1.0, "end": 1.5},
    {"type": "rgb_split", "start": 0, "end": 0.4},
    {"type": "flash", "at": [0.0, 1.5]},
    {"type": "dip", "at": 1.8, "dur": 0.2},
    {"type": "film_grain", "strength": 12},
    {"type": "vignette"},
    {"type": "letterbox", "bars": 0.08},
    {"type": "lut", "path": "media/grade.cube", "mix": 0.7},
    {"type": "lut", "path": "media/grade.cube"},
    {"type": "color", "preset": "teal_orange"},
    {"type": "color", "contrast": 1.1, "saturation": 1.2, "start": 0.5, "end": 1.5},
    {"type": "blur", "sigma": 6, "start": 1.9, "end": 2.0},
    {"type": "sharpen"},
    {"type": "fade", "in": 0.2, "out": 0.3},
    {"type": "mirror"},
]


def test_every_effect_renders(media):
    spec = small({"timeline": [{"clip": {"path": "media/clip1.mp4", "out": 2.2, "effects": ALL_EFFECTS}}],
                  "effects": [{"type": "film_grain", "strength": 4}, {"type": "color", "preset": "film"}],
                  "audio": {"loudnorm": False}})
    out = render(media, "effects", spec)
    assert duration(out) == pytest.approx(2.2, abs=0.1)


@pytest.mark.parametrize("preset", sorted(rs.COLOR_PRESETS))
def test_color_presets_valid(media, preset):
    spec = small({"timeline": [{"clip": {"path": "media/clip3.mp4", "out": 0.5,
                                         "effects": [{"type": "color", "preset": preset}]}}],
                  "audio": {"loudnorm": False}}, w=270, h=480)
    render(media, f"color_{preset}", spec)


def test_lut_changes_pixels(media):
    """A warm LUT must change the image (red up / blue down) vs. no LUT."""
    rs.write_cube(media / "media" / "warm.cube", "warm")
    base = {"timeline": [{"clip": {"color": "#808080", "duration": 0.5}}], "audio": {"loudnorm": False}}
    a = render(media, "lut_off", small(base, 270, 480))
    graded = json.loads(json.dumps(base))
    graded["timeline"][0]["effects"] = []
    graded["effects"] = [{"type": "lut", "path": "media/warm.cube"}]
    b = render(media, "lut_on", small(graded, 270, 480))
    pa, pb = frame_rgb(a, 0.2), frame_rgb(b, 0.2)
    assert pb[0] > pa[0] + 5 and pb[2] < pa[2] - 5


LAYOUT_SEGMENTS = [
    {"layout": "split_vertical", "top": "media/clip1.mp4", "bottom": "media/clip2.mp4", "duration": 1.5,
     "labels": {"top": "לפני", "bottom": "אחרי"}},
    {"layout": "split_horizontal", "left": "media/clip1.mp4", "right": "media/noaudio.mp4", "duration": 1.5,
     "ratio": 0.4, "audio": "mix"},
    {"layout": "split_wipe", "before": "media/boca_villa_blockout.mp4", "after": "media/boca_villa_ai.mp4",
     "duration": 2, "at": 0.4, "wipe_dur": 0.8, "direction": "left", "labels": {"before": "A", "after": "B"}},
    {"layout": "split_wipe", "before": "media/clip1.mp4", "after": "media/clip2.mp4", "duration": 1.5,
     "direction": "down"},
    {"layout": "before_after_slider", "before": "media/boca_villa_blockout.mp4",
     "after": "media/boca_villa_ai.mp4", "duration": 2},
    {"layout": "pip", "main": "media/clip3.mp4", "inset": "media/clip1.mp4", "duration": 1.5,
     "corner": "bottom_left", "inset_label": "ME"},
    {"layout": "input_prompt_result", "input": "media/logo.png", "result": "media/clip2.mp4", "duration": 2,
     "prompt": "[0:00] drone push-in over a white villa\n[0:01] golden hour, palm trees", "title": "Seedance"},
]


@pytest.mark.parametrize("seg", LAYOUT_SEGMENTS, ids=lambda s: s["layout"] + "_" + s.get("direction", ""))
def test_layouts(media, seg):
    spec = small({"timeline": [seg], "audio": {"loudnorm": False}})
    out = render(media, "layout_" + seg["layout"] + seg.get("direction", ""), spec)
    assert duration(out) == pytest.approx(float(seg["duration"]), abs=0.1)


@pytest.mark.parametrize("mode", rs.REVEAL_MODES)
def test_blocks_to_reality_reveal(media, mode):
    seg = {"layout": "reveal", "mode": mode, "blockout": {"path": "media/boca_villa_blockout.mp4", "out": 3},
           "real": {"path": "media/boca_villa_ai.mp4", "out": 3}, "at": 1.0, "glitch": True, "flash": True}
    spec = small({"timeline": [seg], "audio": {"loudnorm": False}})
    out = render(media, f"reveal_{mode}", spec)
    assert duration(out) == pytest.approx(3.0, abs=0.1)


def test_wipe_reveal_shows_before_then_after(media):
    """split_wipe: frame 0 is the BEFORE clip, last frame is the AFTER clip."""
    spec = small({"timeline": [{"layout": "split_wipe", "duration": 2, "at": 0.5, "wipe_dur": 0.5,
                                "before": {"color": "#0000FF"}, "after": {"color": "#00FF00"}, "line": False}],
                  "audio": {"loudnorm": False}}, 270, 480)
    out = render(media, "wipe_colors", spec)
    p0, p1 = frame_rgb(out, 0.1), frame_rgb(out, 1.8)
    assert p0[2] > 180 and p0[1] < 80     # blue
    assert p1[1] > 180 and p1[2] < 80     # green


def test_hebrew_text_and_captions(media, fonts_ok):
    if not fonts_ok:
        pytest.skip("Heebo could not be downloaded")
    wd = media / "work_heb"
    spec = small({"timeline": [{"clip": {"color": "#000000", "duration": 2.5},
                                "overlays": [{"type": "title", "text": "וילה בבוקה רטון 2025", "position": "top"}]}],
                  "overlays": [{"type": "cta", "text": "לפרטים ← DM", "position": "cta", "box": True},
                               {"type": "text", "text": "typewriter", "anim": "typewriter", "position": "upper"}],
                  "captions": {"style": "karaoke", "lines": [{"start": 0.2, "end": 2.2, "text": "שלום לכולם זה AI"}]},
                  "audio": {"loudnorm": False}})
    out = render(media, "hebrew", spec, workdir=str(wd))
    ass = (wd / "overlay.ass").read_text(encoding="utf-8")
    assert "Heebo" in ass and rs.RLM in ass and "\\k" in ass and "וילה בבוקה רטון 2025" in ass
    # text was actually burned in: the top band of a black card now has bright pixels
    px = frame_rgb(out, 1.0)
    w = 54
    top_band = px[w * 3 * 12: w * 3 * 22]  # rows ~12..22 of 96 (title at y=330/1920)
    assert max(top_band) > 120


def test_captions_from_srt_and_json(media):
    (media / "subs.srt").write_text("1\n00:00:00,100 --> 00:00:01,000\nשלום עולם\n", encoding="utf-8")
    (media / "words.json").write_text(json.dumps([{"start": 0.1, "end": 0.5, "text": "hi"},
                                                  {"start": 0.5, "end": 0.9, "text": "there"}]),
                                      encoding="utf-8")
    for src in ("subs.srt", "words.json"):
        spec = small({"timeline": [{"clip": {"color": "#333333", "duration": 1.2}}],
                      "captions": {"source": src, "style": "bold_pop"}, "audio": {"loudnorm": False}}, 270, 480)
        render(media, "caps_" + src.replace(".", "_"), spec)


def test_logo_and_packshot_overlay(media):
    spec = small({"timeline": [{"clip": {"color": "#000000", "duration": 1.5},
                                "overlays": [{"type": "image", "path": "media/logo.png", "y": 960,
                                              "width": 400, "fade": 0}]}],
                  "overlays": [{"type": "image", "path": "media/logo.png", "x": 900, "y": 150, "width": 150,
                                "opacity": 0.8, "start": 0.2, "end": 1.2}],
                  "audio": {"loudnorm": False}}, 270, 480)
    out = render(media, "logo", spec)
    px = frame_rgb(out, 0.8, 54, 96)
    center = px[(48 * 54 + 27) * 3: (48 * 54 + 27) * 3 + 3]  # middle of the frame: logo body
    assert sum(center) > 120


def test_music_sfx_ducking_loudnorm(media):
    spec = small({"timeline": [
        {"clip": {"path": "media/talk.mp4", "out": 4}},
        {"clip": {"path": "media/clip2.mp4", "out": 2}, "transition": {"type": "whip", "sfx": "whoosh"}},
        {"clip": {"path": "media/clip1.mp4", "out": 2}, "transition": "flash"}],
        "audio": {"original_volume": 1.0,
                  "music": {"path": "media/music.wav", "volume": 0.5, "duck": {"threshold": 0.02}},
                  "sfx_on_cuts": "auto",
                  "sfx": [{"type": "riser", "at": 3.5}, {"type": "impact", "at": 3.8}, {"type": "pop", "at": 0.2},
                          {"type": "click", "at": 1}, {"type": "glitch", "at": 2}, {"type": "swish", "at": 2.5},
                          {"type": "hit", "at": 5}, {"path": "media/music.wav", "at": 6, "volume": 0.2}],
                  "loudnorm": -14}})
    out = render(media, "audio", spec)
    assert integrated_lufs(out) == pytest.approx(-14, abs=1.0)


def test_synth_music_and_custom_loudness(media):
    spec = small({"timeline": [{"clip": {"path": "media/noaudio.mp4", "duration": 3}}],
                  "audio": {"music": {"synth": "bed", "volume": 0.8, "duck": False}, "loudnorm": -16}}, 270, 480)
    out = render(media, "synth_music", spec)
    assert integrated_lufs(out) == pytest.approx(-16, abs=1.0)


def test_silent_reel_does_not_crash(media):
    spec = small({"timeline": [{"clip": {"path": "media/noaudio.mp4", "duration": 1}}]}, 270, 480)
    out = render(media, "silent", spec)
    assert has_audio(out)


@pytest.mark.parametrize("preset,size", [("instagram", (1080, 1920)), ("tiktok", (1080, 1920)),
                                         ("shorts", (1080, 1920)), ("feed", (1080, 1350))])
def test_export_presets(media, preset, size):
    spec = {"timeline": [{"clip": {"path": "media/clip2.mp4", "out": 1},
                          "overlays": [{"type": "text", "text": "בדיקה", "position": "bottom"}]}],
            "audio": {"loudnorm": -14}}
    out = render(media, f"preset_{preset}", spec, preset=preset)
    v = vstream(out)
    assert (v["width"], v["height"]) == size
    assert v["codec_name"] == "h264" and v["pix_fmt"] == "yuv420p"
    a = next(s for s in ffprobe(out)["streams"] if s["codec_type"] == "audio")
    assert a["codec_name"] == "aac" and a["sample_rate"] == "48000"


def test_draft_preview_keeps_feed_aspect(media):
    spec = {"export": "feed", "timeline": [{"clip": {"path": "media/clip1.mp4", "out": 0.5}}],
            "audio": {"loudnorm": False}}
    v = vstream(render(media, "feed_draft", spec, preset="draft"))
    assert (v["width"], v["height"]) == (480, 600)


def test_dry_run_writes_nothing(media):
    p = write_spec(media, "dry", small({"timeline": [{"clip": "media/clip1.mp4"}]}))
    out = media / "out" / "dry_should_not_exist.mp4"
    rs.render(str(p), "draft", str(out), dry=True)
    assert not out.exists()


def run_cli(*args, cwd=None):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, cwd=cwd)


def test_cli_plan_probe_and_errors(media):
    p = write_spec(media, "cli", small({"timeline": [{"clip": {"path": "media/clip1.mp4", "out": 2}},
                                                     {"clip": "media/clip2.mp4", "transition": "fade"}]}))
    r = run_cli("plan", str(p))
    assert r.returncode == 0 and "total:" in r.stdout
    r = run_cli("probe", str(media / "media" / "clip1.mp4"))
    info = json.loads(r.stdout)
    assert info["width"] == 720 and info["has_audio"]
    bad = write_spec(media, "bad", {"timeline": [{"clip": "media/nope.mp4"}]})
    r = run_cli("plan", str(bad))
    assert r.returncode == 2 and "spec error" in r.stderr
    r = run_cli("plan", str(write_spec(media, "bad2", {"timeline": [{"clip": "media/clip1.mp4",
                                                                       "effects": ["nope"]}]})))
    assert r.returncode == 2


def test_cli_grid_and_cuts(media):
    src = media / "out" / "transitions.mp4"
    if not src.exists():
        src = media / "media" / "clip1.mp4"
    r = run_cli("grid", str(src), "--cols", "3", "--rows", "2", "--width", "600", "--out", str(media / "g.jpg"))
    assert r.returncode == 0 and (media / "g.jpg").stat().st_size > 1000
    r = run_cli("cuts", str(src), "--json")
    assert r.returncode == 0 and "shots" in json.loads(r.stdout)


@pytest.mark.parametrize("example", sorted(p.name for p in (SKILL / "examples").glob("*.json")))
def test_examples_render(media, example):
    """Every shipped example spec renders against the synthetic demo media (draft preset)."""
    spec = json.loads((SKILL / "examples" / example).read_text(encoding="utf-8"))
    p = write_spec(media, "example_" + example[:-5], spec)
    out = media / "out" / ("example_" + example[:-5] + ".mp4")
    rs.render(str(p), "draft", str(out), fast=True)
    assert duration(out) > 3


def _have_bpy() -> bool:
    return subprocess.run([sys.executable, "-c", "import bpy"], capture_output=True).returncode == 0


@pytest.mark.skipif(not _have_bpy(), reason="bpy (Blender as a module) not installed")
def test_blockout_preview_feeds_reveal(media, tmp_path):
    """blockout.py (single-frame preview, tiny res) -> reveal against a fake AI clip."""
    out = tmp_path / "blk.mp4"
    env = dict(os.environ, EGL_PLATFORM="surfaceless")
    r = subprocess.run([sys.executable, str(SKILL / "scripts" / "blockout.py"),
                        str(SKILL / "examples" / "blockout" / "boca_villa.json"), str(out), "--res", "180x320",
                        "--preview"], capture_output=True, text=True, env=env, timeout=300)
    assert r.returncode == 0, r.stderr[-2000:]
    assert out.exists()
    spec = small({"timeline": [{"layout": "reveal", "mode": "wipe", "duration": 2,
                                "blockout": {"path": str(out), "duration": 2},
                                "real": {"path": "media/boca_villa_ai.mp4", "out": 2}}],
                  "audio": {"loudnorm": False}}, 270, 480)
    o = render(media, "blockout_reveal", spec)
    assert duration(o) == pytest.approx(2.0, abs=0.1)
