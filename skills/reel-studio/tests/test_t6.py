"""Round-2 (T6) features: velocity ramps, beats + beat sync, new effects/transitions, layered SFX,
kinetic caption styles, platform safe zone. Synthetic media only."""
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import SKILL, duration, frame_rgb, rs, small, write_spec

SCRIPT = SKILL / "scripts" / "reelstudio.py"
BEAT_EXPR = ("(0.25+0.75*gte(t,4))*0.9*sin(2*PI*(50*t+60*(1-exp(-30*mod(t,0.5)))/30))*exp(-12*mod(t,0.5))"
             "+0.15*(random(0)*2-1)*exp(-60*mod(t+0.25,0.5))")


@pytest.fixture(scope="session")
def beat_music(media) -> Path:
    """120 BPM kick (every 0.5 s) + off-beat hat, quiet until a drop at 4.0 s."""
    p = media / "media" / "beat120.wav"
    if not p.exists():
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                        f"aevalsrc='{BEAT_EXPR}':s=44100:d=10", str(p)], check=True)
    return p


def render(media: Path, name: str, spec: dict, preset: str = "draft", **kw) -> Path:
    p = write_spec(media, name, spec)
    out = media / "out" / f"{name}.mp4"
    return Path(rs.render(str(p), preset, str(out), fast=True, **kw))


def _ctx(w=1080, h=1920, **extra):
    return rs.Ctx({"canvas": {"width": w, "height": h}, "timeline": [1], **extra}, Path("."))


# ------------------------------------------------------------------ velocity (smooth speed ramp)

def test_velocity_matches_t6_reference_duration():
    """T6 velocity.py: this curve turns a 4.00 s clip into ~4.47 s."""
    pts, steps = rs.velocity_points("0:1,1.0:1,1.3:3,2.2:3,2.5:0.4,3.2:0.4,3.5:1,4:1", 4.0)
    knots, out = rs.velocity_knots(pts, steps)
    assert out == pytest.approx(4.471, abs=0.01)
    assert knots[0] == (0.0, 0.0) and knots[-1][0] == pytest.approx(4.0)
    assert all(b[1] > a[1] for a, b in zip(knots, knots[1:]))  # monotonic output time
    e = rs.velocity_setpts(knots)
    assert e.endswith("/TB") and e.count("(") == e.count(")")


def test_velocity_inputs_and_presets():
    # constant 2x -> half length; base speed multiplies
    assert rs.velocity_knots(*rs.velocity_points([[0, 2], [3, 2]], 3.0))[1] == pytest.approx(1.5)
    assert rs.velocity_knots(*rs.velocity_points([[0, 1], [3, 1]], 3.0, 2.0))[1] == pytest.approx(1.5)
    # points are extended to cover the whole clip
    pts, _ = rs.velocity_points([{"t": 1, "speed": 2}, {"t": 2, "speed": 2}], 4.0)
    assert pts[0] == (0.0, 2.0) and pts[-1] == (4.0, 2.0)
    for name in rs.VELOCITY_PRESETS:
        _, d = rs.velocity_knots(*rs.velocity_points({"preset": name}, 4.0))
        assert 0.5 < d < 15
    for bad in ("nope", [[0, 1]], [[0, 0], [1, 1]], {"points": [[0, 1], [1, 1]], "steps": 0}):
        with pytest.raises(rs.SpecError):
            rs.velocity_points(bad, 4.0)


def test_clip_duration_velocity_freeze_boomerang(media):
    c = rs.norm_clip({"path": "media/clip1.mp4", "out": 4, "velocity": "0:1,1:1,1.3:3,2.2:3,2.5:0.4,3.2:0.4,"
                                                                       "3.5:1,4:1"}, media)
    assert rs.clip_duration(c) == pytest.approx(4.471, abs=0.01)
    sugar = rs.norm_clip({"path": "media/clip1.mp4", "out": 2,
                          "effects": [{"type": "velocity", "points": [[0, 2], [2, 2]]}]}, media)
    assert rs.clip_duration(sugar) == pytest.approx(1.0)
    assert rs.clip_duration(rs.norm_clip({"path": "media/clip1.mp4", "out": 1.5, "boomerang": True}, media)) \
        == pytest.approx(3.0)
    assert rs.clip_duration(rs.norm_clip({"path": "media/clip1.mp4", "out": 2, "freeze": {"at": 0.5, "dur": 1}},
                                         media)) == pytest.approx(3.0)
    with pytest.raises(rs.SpecError, match="not both"):
        rs.clip_duration(rs.norm_clip({"path": "media/clip1.mp4", "out": 3, "velocity": "montage",
                                       "ramps": [{"from": 1, "to": 2, "speed": 2}]}, media))


def test_velocity_freeze_boomerang_render(media):
    spec = small({"timeline": [
        {"clip": {"path": "media/clip1.mp4", "out": 3, "velocity": "montage"}},
        {"clip": {"path": "media/clip2.mp4", "out": 2, "freeze": {"at": 0.5, "dur": 1}}},
        {"clip": {"path": "media/clip3.mp4", "out": 1, "boomerang": True}},
        {"clip": {"path": "media/clip1.mp4", "out": 1, "freeze": 0}}],
        "audio": {"loudnorm": False}}, 270, 480)
    ctx = rs.Ctx(spec, media)
    plans = rs.plan_timeline(spec, ctx)
    total = plans[-1]["start"] + plans[-1]["plan"].dur
    assert plans[1]["plan"].dur == pytest.approx(3.0, abs=0.05)
    assert plans[2]["plan"].dur == pytest.approx(2.0, abs=0.05)
    out = render(media, "t6_velocity", spec)
    assert duration(out) == pytest.approx(total, abs=0.1)
    # freeze in segment 1 is desaturated (hue s=0.2): the frozen frame of the colorful mandelbrot is grayish
    start1 = plans[1]["start"]
    px = frame_rgb(out, start1 + 1.0, 27, 48)
    sat = sum(max(px[i:i + 3]) - min(px[i:i + 3]) for i in range(0, len(px), 3)) / (len(px) / 3)
    px_live = frame_rgb(out, start1 + 2.6, 27, 48)
    sat_live = sum(max(px_live[i:i + 3]) - min(px_live[i:i + 3]) for i in range(0, len(px_live), 3)) / (len(px) / 3)
    assert sat < sat_live * 0.6


# ------------------------------------------------------------------ beats

@pytest.mark.parametrize("engine", ["stdlib", "numpy"])
def test_beats_engines_find_120bpm_and_drop(beat_music, engine):
    if engine == "numpy":
        pytest.importorskip("numpy")
    info = rs.analyze_beats(str(beat_music), "low", 2, 0.3, engine)
    assert info["engine"] == engine
    assert info["bpm"] == pytest.approx(120, abs=2)
    b = info["beats"]
    assert len(b) >= 15
    # every detected beat sits on the 0.5 s kick grid (+-40 ms)
    assert all(abs(t - round(t * 2) / 2) < 0.04 for t in b)
    assert info["drop"] == pytest.approx(4.0, abs=0.26)
    assert info["cuts"] == b[::2]
    assert set(info["downbeats"]) <= set(b) and len(info["downbeats"]) >= 3


def test_beats_librosa_engine(beat_music):
    pytest.importorskip("librosa")
    info = rs.analyze_beats(str(beat_music), "low", 1, 0.3, "librosa")
    assert info["engine"] == "librosa" and 100 < info["bpm"] < 140
    assert all(abs(t - round(t * 2) / 2) < 0.06 for t in info["beats"])


def test_beats_errors(beat_music):
    with pytest.raises(rs.SpecError):
        rs.analyze_beats(str(beat_music), band="mid")
    with pytest.raises(rs.SpecError):
        rs.analyze_beats(str(beat_music), engine="essentia")
    with pytest.raises(rs.SpecError):
        rs.analyze_beats("/nonexistent.wav")


def test_beats_cli(beat_music):
    r = subprocess.run([sys.executable, str(SCRIPT), "beats", str(beat_music), "--engine", "stdlib",
                        "--every", "4"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    info = json.loads(r.stdout)
    assert {"bpm", "beats", "downbeats", "cuts", "drop", "onsets"} <= set(info)
    assert all(b - a >= 1.9 for a, b in zip(info["cuts"], info["cuts"][1:]))


def test_beat_sync_snaps_cuts_to_beats(media):
    """Explicit beat grid: every cut (and the transition midpoint) lands on a beat; floor never lengthens."""
    beats = [0.5 * k for k in range(1, 40)]
    spec = {"canvas": {"fps": 30}, "timeline": [
        {"clip": {"path": "media/clip1.mp4", "out": 1.3}},
        {"clip": {"path": "media/clip2.mp4", "out": 1.9}, "transition": {"type": "fade", "dur": 0.4}},
        {"clip": {"path": "media/clip3.mp4", "out": 2.2}},
        {"clip": {"color": "#FF0000", "duration": 1.6}, "transition": "spin"}],
        "audio": {"beat_sync": {"beats": beats, "every": 1, "end": True}}}
    ctx = rs.Ctx(spec, media)
    info = rs.beat_info_for(spec, media, media, 10)
    new, report = rs.apply_beat_sync(spec, ctx, info)
    plans = rs.plan_timeline(new, ctx)
    for p in plans[1:]:
        cut = p["start"] + rs.tr_overlap(p["trans"]) / 2
        assert min(abs(cut - b) for b in beats) < 0.5 / 30 + 1e-6
    for r in report:
        assert r["to"] <= r["from"] + 1 / 30 + 1e-6  # floor mode
    total = plans[-1]["start"] + plans[-1]["plan"].dur
    assert min(abs(total - b) for b in beats) < 1 / 30 + 1e-6
    assert spec["timeline"][0]["clip"].get("duration") is None  # input spec untouched


def test_beat_sync_drop_segment_and_opt_out(media):
    beats = [0.5 * k for k in range(1, 40)]
    spec = {"canvas": {"fps": 25}, "timeline": [
        {"clip": {"color": "#000000", "duration": 1.2}},
        {"clip": {"color": "#FFFFFF", "duration": 1.2}, "beat_sync": False},
        {"clip": {"color": "#FF0000", "duration": 3}}],
        "audio": {"beat_sync": {"beats": beats, "drop": 2.75, "drop_segment": 2, "end": False}}}
    ctx = rs.Ctx(spec, media)
    new, _ = rs.apply_beat_sync(spec, ctx, rs.beat_info_for(spec, media, media, 10))
    plans = rs.plan_timeline(new, ctx)
    assert plans[1]["start"] == pytest.approx(1.0)       # floor of 1.2 on the 0.5 grid
    assert plans[1]["plan"].dur == pytest.approx(1.2)    # opted out: keeps its length...
    assert new["timeline"][1]["duration"] == pytest.approx(1.2)
    spec["audio"]["beat_sync"]["drop"] = 2.5
    spec["timeline"][1].pop("beat_sync")
    new, rep = rs.apply_beat_sync(spec, ctx, rs.beat_info_for(spec, media, media, 10))
    plans = rs.plan_timeline(new, ctx)
    assert plans[2]["start"] == pytest.approx(2.5, abs=0.5 / 25 + 1e-6) and rep[1]["drop"]  # ...or on the drop


def test_beat_refs_in_global_effects():
    info = {"beats": [0.5, 1.0, 1.5, 2.0, 2.5], "downbeats": [0.5, 2.5], "cuts": [0.5, 1.5, 2.5], "drop": 2.0}
    effs = rs.resolve_beat_refs([{"type": "flash", "at": "downbeats"}, {"type": "zoom_punch", "at": "beats", "max": 2},
                                 {"type": "impact_shake", "at": "drop"}, "vignette"], info)
    assert effs[0]["at"] == [0.5, 2.5] and effs[1]["at"] == [0.5, 1.0] and effs[2]["at"] == [2.0]
    assert effs[3] == {"type": "vignette"}
    with pytest.raises(rs.SpecError):
        rs.resolve_beat_refs([{"type": "flash", "at": "beats"}], None)
    with pytest.raises(rs.SpecError, match="beat analysis"):
        rs._times("beats")


def test_flash_rate_warning(capsys):
    rs.flash_rate_check([0.0, 0.2, 0.4, 0.6, 2.0])
    assert "photosensitivity" in capsys.readouterr().err
    rs.flash_rate_check([0.0, 0.5, 1.0, 1.5])
    assert capsys.readouterr().err == ""


def test_beat_sync_render_cuts_on_beats(media, beat_music):
    """Full render: music analysed (numpy/stdlib), color cards cut exactly on the detected beats, drop auto
    adds a riser + impact, layered whooshes on cuts."""
    engine = "numpy"
    try:
        import numpy  # noqa: F401
    except ImportError:
        engine = "stdlib"
    spec = small({"timeline": [
        {"clip": {"color": "#FF0000", "duration": 1.3}},
        {"clip": {"color": "#00FF00", "duration": 1.7}},
        {"clip": {"color": "#0000FF", "duration": 1.4}},
        {"clip": {"color": "#FFFFFF", "duration": 1.5}}],
        "effects": [{"type": "flash", "at": "drop", "dur": 0.1}],
        "audio": {"music": "media/beat120.wav", "beat_sync": {"engine": engine, "every": 1}, "drop": "auto",
                  "sfx_on_cuts": "layered", "loudnorm": False}}, 270, 480, 30)
    out = render(media, "t6_beatsync", spec, workdir=str(media / "work_beatsync"))
    info = rs.analyze_beats(str(beat_music), "low", 1, 0.0, engine)
    ctx = rs.Ctx(spec, media)
    new, report = rs.apply_beat_sync(spec, ctx, rs.beat_info_for(spec, media, media, 8))
    cuts = [r["cut"] for r in report if r["cut"] is not None]
    assert len(cuts) == 3
    for c in cuts:
        assert min(abs(c - b) for b in info["beats"]) < 1 / 30 + 1e-3
    # the color really changes at each cut: red -> green -> blue -> white
    seq = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
    for k, c in enumerate(cuts):
        before, after = frame_rgb(out, c - 0.06, 8, 8)[:3], frame_rgb(out, c + 0.06, 8, 8)[:3]
        assert all(abs(a - b) < 70 for a, b in zip(before, seq[k])), (c, before)
        assert all(abs(a - b) < 70 for a, b in zip(after, seq[k + 1])), (c, after)
    # the cut closest to the detected drop (4.0) lands on it (cut grid is every beat here)
    assert info["drop"] == pytest.approx(4.0, abs=0.26)
    assert any(abs(c - info["drop"]) < 1 / 30 for c in cuts)


# ------------------------------------------------------------------ effects

T6_EFFECTS = [
    {"type": "impact_shake", "at": [0.2, 1.0]},
    {"type": "handheld", "intensity": 14},
    {"type": "motion_blur", "start": 0.3, "end": 0.8},
    {"type": "motion_blur", "frames": 3},
    {"type": "echo", "start": 0.8, "end": 1.2},
    {"type": "glow", "threshold": 0.6},
    {"type": "vhs", "start": 1.2, "end": 1.6},
    {"type": "duotone", "shadows": "#101060", "highlights": "orange", "start": 1.6, "end": 2.0},
    {"type": "film_grain", "mode": "overlay", "opacity": 0.3},
    {"type": "film_grain", "strength": 6},
    {"type": "color", "temperature": 4500, "vibrance": 0.2},
    {"type": "color", "curves": "vintage"},
]


def test_t6_effects_render(media):
    spec = small({"timeline": [{"clip": {"path": "media/clip1.mp4", "out": 2.2, "effects": T6_EFFECTS},
                                "effects": [{"type": "glow", "tint": "white", "strength": 0.3}]}],
                  "effects": [{"type": "vhs"}, {"type": "impact_shake", "at": 1.0}],
                  "audio": {"loudnorm": False}}, 270, 480)
    out = render(media, "t6_effects", spec)
    assert duration(out) == pytest.approx(2.2, abs=0.1)


def test_effect_validation():
    g = rs.Graph()
    with pytest.raises(rs.SpecError):
        rs.apply_effects(g, "v", [{"type": "motion_blur", "frames": 20}], 270, 480, 24, 2)
    with pytest.raises(rs.SpecError):
        rs.apply_effects(g, "v", [{"type": "glow", "threshold": 1.5}], 270, 480, 24, 2)
    with pytest.raises(rs.SpecError):
        rs.apply_effects(g, "v", [{"type": "color", "curves": "sepia"}], 270, 480, 24, 2)
    with pytest.raises(rs.SpecError):
        rs.apply_effects(g, "v", [{"type": "film_grain", "mode": "big"}], 270, 480, 24, 2)


def test_motion_blur_window_never_uses_enable():
    """tmix + enable= turns chroma green (T6 bug #1): the window must be trim+concat instead."""
    g = rs.Graph()
    rs.apply_effects(g, "v", [{"type": "motion_blur", "start": 0.5, "end": 1.0}], 270, 480, 24, 2)
    script = g.script()
    assert "tmix" in script and "enable" not in script and "concat=n=3" in script


def _neutral(px) -> float:
    """Mean channel spread (0 = perfectly gray)."""
    n = len(px) // 3
    return sum(max(px[i * 3:i * 3 + 3]) - min(px[i * 3:i * 3 + 3]) for i in range(n)) / n


def test_grain_and_motion_blur_keep_color(media):
    """Overlay grain on gray stays gray (no colored noise); windowed motion blur keeps a red card red."""
    spec = small({"timeline": [{"clip": {"color": "#808080", "duration": 1.0,
                                         "effects": [{"type": "film_grain", "mode": "overlay", "opacity": 0.5}]}},
                               {"clip": {"color": "#C81E1E", "duration": 1.0,
                                         "effects": [{"type": "motion_blur", "start": 0.2, "end": 0.8},
                                                     {"type": "echo"}]}}],
                  "audio": {"loudnorm": False}}, 270, 480)
    out = render(media, "t6_colorsafe", spec)
    assert _neutral(frame_rgb(out, 0.5, 27, 48)) < 12
    r, g, b = frame_rgb(out, 1.5, 4, 4)[:3]
    assert r > 150 and g < 70 and b < 70


def test_glow_is_not_magenta(media):
    """Screen blend in YUV goes magenta (T6 bug #2); our glow blends in gbrp: a gray card stays gray."""
    spec = small({"timeline": [{"clip": {"color": "#C0C0C0", "duration": 0.5,
                                         "effects": [{"type": "glow", "tint": "white", "threshold": 0.5}]}}],
                  "audio": {"loudnorm": False}}, 270, 480)
    out = render(media, "t6_glow", spec)
    assert _neutral(frame_rgb(out, 0.25, 27, 48)) < 10


# ------------------------------------------------------------------ transitions

def test_new_transitions_plan():
    assert rs.norm_transition("spin")["dur"] == pytest.approx(0.4)
    assert rs.tr_overlap(rs.norm_transition("spin")) == 0
    assert rs.tr_overlap(rs.norm_transition("zoom_through")) == 0
    assert rs.tr_overlap(rs.norm_transition("light_leak")) == pytest.approx(0.6)
    assert rs.norm_transition("film_burn")["type"] == "film_burn"


def test_new_transitions_render(media):
    spec = small({"timeline": [
        {"clip": {"path": "media/clip1.mp4", "out": 1.5}},
        {"clip": {"path": "media/clip2.mp4", "out": 1.5}, "transition": "spin"},
        {"clip": {"path": "media/clip3.mp4", "out": 1.5}, "transition": "zoom_through"},
        {"clip": {"color": "#000000", "duration": 1.5}, "transition": {"type": "light_leak", "dur": 0.5}},
        {"clip": {"color": "#000000", "duration": 1.0}, "transition": "leak"}],
        "audio": {"loudnorm": False, "sfx_on_cuts": "auto"}}, 270, 480)
    ctx = rs.Ctx(spec, media)
    plans = rs.plan_timeline(spec, ctx)
    assert plans[1]["start"] == pytest.approx(1.5) and plans[2]["start"] == pytest.approx(3.0)  # no overlap
    total = plans[-1]["start"] + plans[-1]["plan"].dur
    out = render(media, "t6_transitions", spec)
    assert duration(out) == pytest.approx(total, abs=0.1)
    # black -> black with a light leak: the only light is the warm leak (screen blend in gbrp)
    lit = frame_rgb(out, plans[4]["start"] + 0.3, 8, 8)
    n = len(lit) // 3
    r, b = sum(lit[0::3]) / n, sum(lit[2::3]) / n
    assert r > 40 and r > b


# ------------------------------------------------------------------ SFX layering

def test_layered_cut_sfx_and_drop_items():
    cuts = [(1.0, {"type": "cut"}), (2.0, {"type": "whip", "sfx": "glitch"}), (3.0, {"type": "fade", "sfx": "none"})]
    items = rs.cut_sfx_items({"sfx_on_cuts": {"type": "layered", "hit": "all", "volume": 0.5}, "drop": 2.5},
                             cuts, 6.0)
    kinds = [(i["type"], i["at"]) for i in items]
    assert ("whoosh", 1.0) in kinds and ("whoosh_low", 1.0) in kinds and ("hit", 1.0) in kinds
    assert ("glitch", 2.0) in kinds and not any(t == 3.0 for _, t in kinds)
    assert ("riser", 2.5) in kinds and ("impact", 2.5) in kinds
    no_drop = rs.cut_sfx_items({"sfx_on_cuts": "auto", "drop": 2.5, "drop_sfx": False}, cuts, 6.0)
    assert not any(i["type"] == "riser" for i in no_drop)
    # auto drop time comes from beat analysis (_drop_time)
    auto = rs.cut_sfx_items({"drop": "auto", "_drop_time": 4.0}, [], 6.0)
    assert {(i["type"], i["at"]) for i in auto} == {("riser", 4.0), ("impact", 4.0)}


def test_synthetic_whoosh_peak_is_its_anchor(tmp_path):
    """The whoosh's loudest moment is SFX anchor -> placed with its peak exactly on the cut."""
    for name in ("whoosh", "whoosh_low"):
        f = rs.render_sfx(name, str(tmp_path / f"{name}.wav"), rs.Runner())
        # envelope peaks at 0.4 s by construction; noise moves the measured peak by up to ~0.08 s
        assert rs.audio_peak_time(f) == pytest.approx(rs.SFX[name][1], abs=0.1)
    assert rs.SFX["riser"][1] == rs.SFX["riser"][0]  # riser peaks at its end


def test_sfx_library_files_align_peak(media, tmp_path):
    lib = tmp_path / "sfxlib"
    lib.mkdir()
    # a 'whoosh' file whose loudest point is at 0.7 s
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "aevalsrc='sin(2*PI*300*t)*exp(-60*(t-0.7)*(t-0.7))':s=48000:d=1.2", str(lib / "whoosh.wav")],
                   check=True)
    got = rs.sfx_library({"sfx_library": str(lib)}, media)
    assert set(got) == {"whoosh"}
    assert rs.audio_peak_time(got["whoosh"]) == pytest.approx(0.7, abs=0.03)
    with pytest.raises(rs.SpecError):
        rs.sfx_library({"sfx_library": str(tmp_path / "missing")}, media)
    spec = small({"timeline": [{"clip": {"color": "#000000", "duration": 1.5}},
                               {"clip": {"color": "#FFFFFF", "duration": 1.5}, "transition": "whip"}],
                  "audio": {"sfx_on_cuts": "layered", "sfx_library": str(lib), "drop": 2.0,
                            "sfx": [{"type": "scratch", "at": 0.2}], "loudnorm": -14}}, 270, 480)
    out = render(media, "t6_sfxlib", spec)
    assert duration(out) == pytest.approx(2.72, abs=0.1)


# ------------------------------------------------------------------ captions

@pytest.mark.parametrize("style", ["pop", "slide", "stack"])
def test_kinetic_caption_styles_keep_rlm_rule(style):
    ctx = _ctx()
    words = rs.lines_to_words([{"start": 0, "end": 2, "text": "אל תשפטו אנשים לפי המילים"},
                               {"start": 2.2, "end": 3.5, "text": "AI זה העתיד"}])
    evs = rs.caption_events({"style": style, "emphasis": ["המילים"]}, words, ctx, 10)
    assert evs
    for e in evs:
        body = re.sub(r"\{[^}]*\}", "", e.text)
        assert body.startswith(rs.RLM), e.text  # RLM right after the override block (T6 5.1)
    doc = rs.ass_document(ctx, evs)
    assert all(ln.rstrip().endswith(",-1") for ln in doc.splitlines() if ln.startswith("Style:"))
    if style == "pop":
        assert "\\fscx40\\fscy40\\t(0,90,\\fscx118\\fscy118)" in evs[0].text
    if style == "slide":
        m = re.search(r"\\move\((-?\d+),\d+,(\d+),", evs[0].text)
        assert m and int(m.group(1)) > 1080 > int(m.group(2))  # Hebrew enters from the right
    if style == "stack":
        big = [e for e in evs if "\\fs160" in e.text]
        assert big and "המילים" in big[0].text and rs.ass_color("#FFE000") in big[0].text
        small_ev = [e for e in evs if "\\fs72" in e.text]
        assert any("אל תשפטו" in e.text for e in small_ev)


def test_kinetic_captions_render(media, fonts_ok):
    spec = small({"timeline": [{"clip": {"color": "#202020", "duration": 3}}],
                  "captions": {"style": "stack", "lines": [{"start": 0.1, "end": 1.4, "text": "אל תשפטו לפי המילים"},
                                                            {"start": 1.5, "end": 2.9, "text": "שלום AI"}]},
                  "overlays": [{"type": "text", "text": "pop", "anim": "pop", "position": "upper"}],
                  "audio": {"loudnorm": False}}, 270, 480)
    out = render(media, "t6_captions", spec)
    px = frame_rgb(out, 0.8, 27, 48)
    assert max(px) > 150  # text burned in


# ------------------------------------------------------------------ safe zone

def test_safe_zone_explicit_position_moves_with_warning(capsys):
    ctx = _ctx()
    ev = rs.text_overlay_events({"type": "text", "text": "קנו עכשיו", "y": 1800}, ctx, 3)[0]
    y = int(re.search(r"\\pos\(\d+,(\d+)\)", ev.text).group(1))
    assert y + 72 * 1.25 / 2 <= 1920 * 0.65 + 1
    assert "UI zone" in capsys.readouterr().err
    ev = rs.text_overlay_events({"type": "text", "text": "top", "y": 100}, ctx, 3)[0]
    y = int(re.search(r"\\pos\(\d+,(\d+)\)", ev.text).group(1))
    assert y - (72 * 1.25 + 12) / 2 >= 1920 * 0.14 - 1
    # left-aligned text at x=10 is pushed in from the edge
    ev = rs.text_overlay_events({"type": "text", "text": "edge", "x": 10, "y": 900, "align": 4}, ctx, 3)[0]
    x = int(re.search(r"\\pos\((\d+),", ev.text).group(1))
    assert x >= 1080 * 0.06 - 1


def test_safe_zone_named_positions_are_silent_and_opt_out(capsys):
    ctx = _ctx()
    ev = rs.text_overlay_events({"type": "cta", "text": "לפרטים", "position": "cta"}, ctx, 3)[0]
    y = int(re.search(r"\\pos\(\d+,(\d+)\)", ev.text).group(1))
    assert y < 1920 * 0.65 and capsys.readouterr().err == ""
    ev = rs.text_overlay_events({"type": "text", "text": "x", "y": 1800, "safe": False}, ctx, 3)[0]
    assert "\\pos(540,1800)" in ev.text
    off = _ctx(safe_zone=False)
    ev = rs.text_overlay_events({"type": "text", "text": "x", "position": "bottom"}, off, 3)[0]
    assert "\\pos(540,1540)" in ev.text
    # top title is already safe -> unchanged
    ev = rs.text_overlay_events({"type": "title", "text": "כותרת", "position": "top"}, ctx, 3)[0]
    assert "\\pos(540,330)" in ev.text
    # internal layout chips (_px) are never moved
    ev = rs.text_overlay_events(rs.chip("A", 20, 20, 0, 1, ctx), ctx, 1)[0]
    assert "\\pos(20,20)" in ev.text
    assert capsys.readouterr().err == ""


def test_safe_zone_custom_fractions_and_captions(capsys):
    with pytest.raises(rs.SpecError):
        rs.parse_safe_zone({"top": 0.7})
    with pytest.raises(rs.SpecError):
        rs.parse_safe_zone("maybe")
    assert rs.parse_safe_zone({"bottom": 0.2})["bottom"] == 0.2
    ctx = _ctx()
    words = rs.lines_to_words([{"start": 0, "end": 1, "text": "שלום עולם"}])
    ev = rs.caption_events({"style": "bold_pop"}, words, ctx, 5)[0]
    y = int(re.search(r"\\pos\(\d+,(\d+)\)", ev.text).group(1))
    assert y < 1920 * 0.65 and capsys.readouterr().err == ""  # default 'lower' clamps silently
    rs.caption_events({"style": "bold_pop", "y": 1700}, words, ctx, 5)
    assert "captions" in capsys.readouterr().err


def test_safe_zone_render_moves_text(media, fonts_ok):
    if not fonts_ok:
        pytest.skip("Heebo could not be downloaded")
    wd = media / "work_safe"
    spec = small({"timeline": [{"clip": {"color": "#000000", "duration": 1.0},
                                "overlays": [{"type": "title", "text": "מבצע 50%", "y": 1750}]}],
                  "audio": {"loudnorm": False}}, 270, 480)
    out = render(media, "t6_safe", spec, workdir=str(wd))
    ass = (wd / "overlay.ass").read_text(encoding="utf-8")
    y = int(re.search(r"\\pos\(\d+,(\d+)\)", ass).group(1))
    assert y < 480 * 0.65
    px = frame_rgb(out, 0.5, 27, 48)
    w = 27
    bottom = px[w * 3 * 32:]  # rows 32..47 (bottom third) stay black
    assert max(bottom) < 60
