"""Fast unit tests: no rendering."""
import pytest

from conftest import rs


def test_fnum_and_even():
    assert rs.fnum(1.50000) == "1.5"
    assert rs.fnum(-0.00001) == "0"
    assert rs.even(1079) == 1080 and rs.even(1080) == 1080


@pytest.mark.parametrize("v,exp", [(3.5, 3.5), ("3.5", 3.5), ("0:03.5", 3.5), ("00:01:02", 62.0)])
def test_sec(v, exp):
    assert rs.sec(v) == pytest.approx(exp)


def test_sec_bad():
    with pytest.raises(rs.SpecError):
        rs.sec("abc")


def test_colors():
    assert rs.parse_color("white") == (255, 255, 255, 255)
    assert rs.parse_color("#00000080")[3] == 128
    assert rs.parse_color("black@0.5")[3] == 128
    assert rs.ass_color("#FF8000") == "&H0080FF&"  # ASS is BGR
    assert rs.ff_color("#112233") == "0x112233"
    with pytest.raises(rs.SpecError):
        rs.parse_color("notacolor")


def test_rtl_fix_prefixes_rlm_only_for_hebrew():
    assert rs.is_rtl("שלום") and not rs.is_rtl("hello")
    he = rs.rtl_fix("AI שלום\\Nשורה 2")
    assert all(line.startswith(rs.RLM) for line in he.split("\\N"))
    assert rs.rtl_fix("hello") == "hello"
    assert rs.rtl_fix("hello", "rtl").startswith(rs.RLM)


def test_ass_escape_and_time():
    assert rs.ass_escape("a{b}\nc") == "a(b)\\Nc"
    assert rs.ass_time(62.345) == "0:01:02.35" or rs.ass_time(62.345) == "0:01:02.34"


@pytest.mark.parametrize("speed", [4.0, 0.25, 3.0, 0.7, 1.25])
def test_atempo_chain_splits_extreme_speeds(speed):
    assert rs.atempo_chain(1.0) == ""
    vals = [float(f.split("=")[1]) for f in rs.atempo_chain(speed).split(",")]
    assert all(0.5 <= v <= 2.0 for v in vals)
    prod = 1.0
    for v in vals:
        prod *= v
    assert prod == pytest.approx(speed, rel=1e-3)


def test_clip_pieces_speed_ramp_duration():
    info = {"is_image": False, "duration": 4.0}
    c = {"path": "x.mp4", "ramps": [{"from": 1, "to": 2, "speed": 2.0}]}
    pieces = rs.clip_pieces(c, info)
    assert pieces == [(0.0, 1.0, 1.0), (1.0, 2.0, 2.0), (2.0, 4.0, 1.0)]
    assert sum((b - a) / s for a, b, s in pieces) == pytest.approx(3.5)


def test_clip_pieces_rejects_overlapping_ramps():
    info = {"is_image": False, "duration": 4.0}
    c = {"path": "x.mp4", "ramps": [{"from": 1, "to": 3, "speed": 2}, {"from": 2, "to": 3.5, "speed": 2}]}
    with pytest.raises(rs.SpecError):
        rs.clip_pieces(c, info)


def test_transitions():
    assert rs.norm_transition(None)["dur"] == 0
    assert rs.norm_transition("whip")["dur"] == pytest.approx(0.28)
    assert rs.norm_transition({"type": "circleopen", "dur": 0.7})["dur"] == pytest.approx(0.7)
    with pytest.raises(rs.SpecError):
        rs.norm_transition("explode")


def test_presets_and_aliases():
    for name in ("instagram", "reels", "tiktok", "shorts", "feed", "4:5", "draft", "master"):
        assert rs.resolve_preset(name, {}) in rs.PRESETS
    assert rs.resolve_preset(None, {"export": "tt"}) == "tiktok"
    with pytest.raises(rs.SpecError):
        rs.resolve_preset("vhs", {})
    spec = rs.apply_preset_canvas({"canvas": {"fps": 25}}, "feed")
    assert spec["canvas"] == {"fps": 25, "width": 1080, "height": 1350}
    assert rs.apply_preset_canvas({}, "instagram") == {}


def test_piecewise_expr_is_valid_shape():
    e = rs.piecewise_expr([[0, 0], [1, 0], [2, 1]])
    assert e.startswith("if(lt(t,0),0,") and e.count("(") == e.count(")")


def test_graph_sink_unused():
    g = rs.Graph("t")
    a, v = g.label("a"), g.label()
    g.add(f"anullsrc[{a}]")
    g.add(f"color=c=black[{v}]")
    g.sink_unused([v])
    assert g.lines[-1] == f"[{a}]anullsink"


@pytest.mark.parametrize("mode,layout", [("wipe", "split_wipe"), ("slider", "before_after_slider"),
                                         ("split", "split_horizontal"), ("split_vertical", "split_vertical"),
                                         ("cut", "split_wipe")])
def test_expand_reveal(mode, layout):
    s = rs.expand_reveal({"layout": "reveal", "mode": mode, "blockout": "b.mp4", "real": "r.mp4",
                          "at": 1.0, "glitch": True, "flash": True})
    assert s["layout"] == layout
    types = [e["type"] for e in s["effects"]]
    assert "glitch" in types and "flash" in types


def test_expand_reveal_errors():
    with pytest.raises(rs.SpecError):
        rs.expand_reveal({"mode": "wipe", "blockout": "b.mp4"})
    with pytest.raises(rs.SpecError):
        rs.expand_reveal({"mode": "zoom", "blockout": "b.mp4", "real": "r.mp4"})


def _ctx():
    return rs.Ctx({"canvas": {"width": 1080, "height": 1920}, "timeline": [1]}, rs.Path("."))


def test_hebrew_text_event():
    ev = rs.text_overlay_events({"type": "text", "text": "וילה בבוקה רטון", "position": "top",
                                 "highlight": ["וילה"]}, _ctx(), 3.0)[0]
    assert "\\fnHeebo" in ev.text and rs.RLM in ev.text and "\\pos(540,330)" in ev.text
    assert ev.start == 0 and ev.end == 3.0


def test_text_event_validation():
    with pytest.raises(rs.SpecError):
        rs.text_overlay_events({"type": "text", "text": ""}, _ctx(), 3)
    with pytest.raises(rs.SpecError):
        rs.text_overlay_events({"type": "text", "text": "x", "anim": "spin"}, _ctx(), 3)
    with pytest.raises(rs.SpecError):
        rs.text_overlay_events({"type": "text", "text": "x", "position": "nowhere"}, _ctx(), 3)


@pytest.mark.parametrize("style", list(rs.CAPTION_STYLES))
def test_caption_styles(style):
    words = rs.lines_to_words([{"start": 0, "end": 2, "text": "שלום לכולם זה AI"},
                               {"start": 2.5, "end": 4, "text": "hello world"}])
    evs = rs.caption_events({"style": style}, words, _ctx(), 10)
    assert evs and all(e.end > e.start for e in evs)
    assert any(rs.RLM in e.text for e in evs)
    doc = rs.ass_document(_ctx(), evs)
    assert "PlayResX: 1080" in doc and "Dialogue:" in doc


def test_parse_srt(tmp_path):
    p = tmp_path / "a.srt"
    p.write_text("1\n00:00:00,500 --> 00:00:02,000\nשלום עולם\n\n2\n00:00:02,500 --> 00:00:03,000\nhi\n",
                 encoding="utf-8")
    lines = rs.parse_srt(str(p))
    assert lines[0] == {"start": 0.5, "end": 2.0, "text": "שלום עולם"} and len(lines) == 2


def test_write_cube(tmp_path):
    p = rs.write_cube(tmp_path / "a.cube", "warm", n=5)
    rows = open(p).read().strip().splitlines()
    assert rows[1] == "LUT_3D_SIZE 5" and len(rows) == 2 + 125


def test_unknown_effect_and_layout_errors(media):
    ctx = rs.Ctx({"timeline": [1]}, media)
    with pytest.raises(rs.SpecError, match="unknown effect"):
        rs.build_segment({"clip": {"path": "media/clip1.mp4", "effects": ["explode"]}}, ctx)
    with pytest.raises(rs.SpecError, match="unknown layout"):
        rs.build_segment({"layout": "grid9", "clip": "media/clip1.mp4"}, ctx)
    with pytest.raises(rs.SpecError, match="file not found"):
        rs.build_segment({"clip": "media/missing.mp4"}, ctx)


def test_plan_timeline_overlaps_transitions(media):
    spec = {"canvas": {"fps": 25}, "timeline": [
        {"clip": {"path": "media/clip1.mp4", "out": 2}},
        {"clip": {"path": "media/clip2.mp4", "out": 2}, "transition": {"type": "fade", "dur": 0.4}},
        {"clip": {"path": "media/clip3.mp4", "out": 1}, "transition": "cut"}]}
    plans = rs.plan_timeline(spec, rs.Ctx(spec, media))
    assert [round(p["start"], 2) for p in plans] == [0.0, 1.6, 3.6]


def test_user_xy_are_reference_coords_scaled_to_canvas():
    feed = rs.Ctx({"canvas": {"width": 1080, "height": 1350}, "timeline": [1]}, rs.Path("."))
    assert rs.resolve_xy({"x": 540, "y": 960}, feed)[:2] == (540, 675)
    assert rs.resolve_xy({"x": 0.25, "y": 0.5}, feed)[:2] == (270, 675)
    assert rs.resolve_xy({"x": 10, "y": 20, "_px": True}, feed)[:2] == (10, 20)
    assert rs.resolve_xy({"position": "top"}, feed)[1] == round(330 * 1350 / 1920)
