#!/usr/bin/env python3
"""qc_report.py - one-page technical + sync QC report for a rendered ad or a generated clip.

    python3 qc_report.py VIDEO [--out DIR] [--events events.csv] [--audio-stem sfx.wav]
                               [--lufs -14] [--tp -1] [--strip-step 0.5] [--top-onsets 30]

Writes DIR/report.html, DIR/report.md, DIR/report.json, DIR/strip.jpg (default DIR = <video>_qc/):
  * frame strip every 0.5 s (cuts outlined in red, flash frames in yellow, frozen spans in blue);
  * hard cuts with timestamps and shot lengths;
  * audio RMS envelope (SVG) + onset list (spectral flux);
  * motion energy (dense optical flow, camera motion removed) + motion peaks / stops / starts;
  * event-alignment table: every audio onset paired with the nearest visual event, offset in ms
    and frames (negative = sound leads picture);
  * loudness (EBU R128 integrated LUFS, true peak, LRA) vs the social target (-14 LUFS, <= -1 dBTP);
  * black / white / single-frame flash frames; frozen (repeated) frames; per-shot luma flicker.
  * --events: planned visual events ("t,label" per line, from the preflight sound list): each must
    have an audio onset within the sync window, otherwise it is reported as a missing/late sound.

Exit code: 0 PASS, 1 WARN, 2 FAIL (so it can gate a pipeline).
No paid API is called. Needs ffmpeg, numpy, scipy, opencv-python-headless.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qclib as q  # noqa: E402

# Sync windows for a sound against its visual event (offset = audio - picture, ms).
# Netflix QC: effects 1 frame early/late = FYI, >= 2 frames = issue. Editors put hard SFX on the
# contact frame or 1-2 frames early; sound that lands late reads as "rubbery".
# PASS: from 2 frames early to 1 frame late. WARN: up to 4 frames early / 2 frames late.


def sync_level(off_ms: float, fps: float) -> str:
    fr = 1000.0 / fps
    if -2 * fr - 1 <= off_ms <= 1 * fr + 1:
        return "PASS"
    if -4 * fr - 1 <= off_ms <= 2 * fr + 1:
        return "WARN"
    return "FAIL"


def load_events(path: str | None) -> list[dict]:
    if not path:
        return []
    txt = Path(path).read_text(encoding="utf-8").strip()
    if txt.startswith("[") or txt.startswith("{"):
        data = json.loads(txt)
        data = data.get("events", data) if isinstance(data, dict) else data
        return [{"t": float(e["t"]), "label": str(e.get("label", ""))} for e in data]
    out = []
    for line in txt.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        t, _, lab = line.partition(",")
        out.append({"t": float(t), "label": lab.strip()})
    return out


def analyse(video: str, args) -> dict:
    info = q.probe(video)
    fps = info["fps"]
    dur = info["duration"]
    frames, times = q.read_frames(video, width=160)
    if len(times):
        dur = max(dur, float(times[-1] + 1 / fps)) if dur <= 0 else dur

    cuts, content = q.detect_cuts(frames, times, fps)
    shots = q.shots_from_cuts(cuts, dur)
    mot = q.motion_energy(frames, {c["frame"] for c in cuts})
    vev = q.visual_events(times, mot["local"], fps, cuts)
    flashes = q.flash_frames(frames, times)
    frozen, dups = q.frozen_runs(frames, times, fps)
    # a held black/white frame is reported as a flash hold, not twice as "frozen"
    frozen = [f for f in frozen if not any(fl["start"] - 0.1 <= f["start"] and f["end"] <= fl["end"] + 0.1
                                           for fl in flashes if fl["kind"] in ("black", "white"))]
    flicker = q.luma_flicker(frames, times, shots)

    # audio
    asrc = args.audio_stem or (video if info["has_audio"] else None)
    audio = q.read_audio(asrc, 22050) if asrc else None
    loud = q.loudness(video) if info["has_audio"] else None
    env_t, env_db, onsets = np.zeros(0), np.zeros(0), []
    if audio is not None and len(audio):
        env_t, env_db = q.rms_envelope(audio, 22050)
        onsets = q.detect_onsets(audio, 22050)
        # keep the strongest N onsets (music beats would otherwise flood the table)
        onsets = sorted(sorted(onsets, key=lambda o: -o["strength"])[: args.top_onsets], key=lambda o: o["t"])

    # alignment: each audio onset -> nearest visual event within +-0.5 s
    align = []
    for o in onsets:
        cands = [e for e in vev if abs(e["t"] - o["t"]) <= 0.5]
        if not cands:
            align.append({"audio_t": o["t"], "strength": o["strength"], "visual_t": None, "kind": "-",
                          "offset_ms": None, "offset_frames": None, "level": "INFO",
                          "note": "no visual event within 0.5 s (music/ambience, or an orphan SFX)"})
            continue
        e = min(cands, key=lambda e: abs(e["t"] - o["t"]))
        off = (o["t"] - e["t"]) * 1000
        align.append({"audio_t": o["t"], "strength": o["strength"], "visual_t": e["t"], "kind": e["kind"],
                      "offset_ms": off, "offset_frames": off * fps / 1000, "level": sync_level(off, fps),
                      "note": "sound leads" if off < 0 else "sound lags" if off > 0 else "on the frame"})

    # planned events (from preflight): each needs an onset in the window
    planned = []
    for ev in load_events(args.events):
        near = [o for o in (q.detect_onsets(audio, 22050, sensitivity=1.6) if audio is not None else [])
                if abs(o["t"] - ev["t"]) <= 0.5]
        if not near:
            planned.append({**ev, "audio_t": None, "offset_ms": None, "level": "FAIL",
                            "note": "no sound onset within 0.5 s of this event"})
            continue
        o = min(near, key=lambda o: abs(o["t"] - ev["t"]))
        off = (o["t"] - ev["t"]) * 1000
        planned.append({**ev, "audio_t": o["t"], "offset_ms": off, "level": sync_level(off, fps),
                        "note": "sound leads" if off < 0 else "sound lags"})

    return {"video": video, "info": info, "fps": fps, "duration": dur, "cuts": cuts, "shots": shots,
            "motion_t": times, "motion_local": mot["local"], "motion_global": mot["global"],
            "visual_events": vev, "flashes": flashes, "frozen": frozen, "duplicate_frames": dups,
            "flicker": flicker, "loudness": loud, "env_t": env_t, "env_db": env_db, "onsets": onsets,
            "alignment": align, "planned": planned, "content": content}


def checks(r: dict, args) -> list[dict]:
    c = []
    info = r["info"]
    c.append({"level": "INFO", "check": "format",
              "detail": f'{info["width"]}x{info["height"]} {r["fps"]:.2f} fps {r["duration"]:.2f} s, '
                        f'audio: {"yes" if info["has_audio"] else "NONE"}'})
    L = r["loudness"]
    if not info["has_audio"]:
        c.append({"level": "INFO" if args.stage == "take" else "FAIL", "check": "audio",
                  "detail": "no audio stream (fine for a raw take, FAIL for a deliverable)"})
    elif L and L["integrated_lufs"] is not None:
        d = L["integrated_lufs"] - args.lufs
        lvl = "PASS" if abs(d) <= 1.0 else "WARN" if abs(d) <= 3.0 else "FAIL"
        if args.stage == "take" and lvl != "PASS":
            lvl = "INFO"
        c.append({"level": lvl, "check": "loudness",
                  "detail": f'{L["integrated_lufs"]:.1f} LUFS integrated (target {args.lufs:+.0f} +-1), LRA {L["lra_lu"]} LU'})
        tp = L["true_peak_dbtp"]
        if tp is not None:
            c.append({"level": "PASS" if tp <= args.tp else "INFO" if args.stage == "take" else "FAIL", "check": "true peak",
                      "detail": f"{tp:+.1f} dBTP (max {args.tp:+.1f})"})
    n_shots = len(r["shots"])
    longest = max((s["length"] for s in r["shots"]), default=0)
    c.append({"level": "INFO", "check": "shots",
              "detail": f"{n_shots} shots, {len(r['cuts'])} hard cuts, longest {longest:.1f} s, "
                        f"first cut at {r['cuts'][0]['t']:.2f} s" if r["cuts"] else f"one continuous shot ({longest:.1f} s)"})
    if args.max_shot:
        long_shots = [s for s in r["shots"] if s["length"] > args.max_shot]
        c.append({"level": "WARN" if long_shots else "PASS", "check": "coverage (--max-shot)",
                  "detail": ("; ".join(f'shot {s["index"]} {s["start"]:.1f}-{s["end"]:.1f}s = {s["length"]:.1f} s'
                                       for s in long_shots) + f" > {args.max_shot:.1f} s: action reads as real through "
                             "coverage (6-10 cut shots per 30 s), not one camera move") if long_shots
                  else f"all shots <= {args.max_shot:.1f} s"})
    fl = r["flashes"]
    short = [f for f in fl if f["frames"] <= 2]
    if short:
        c.append({"level": "FAIL", "check": "flash frames",
                  "detail": "; ".join(f'{f["kind"]} {f["start"]:.2f}s ({f["frames"]} fr)' for f in short)})
    long_ = [f for f in fl if f["frames"] > 2]
    if long_:
        c.append({"level": "WARN", "check": "black/white holds",
                  "detail": "; ".join(f'{f["kind"]} {f["start"]:.2f}-{f["end"]:.2f}s' for f in long_)
                            + " (intended transition? a seam must land on full white/black)"})
    if not fl:
        c.append({"level": "PASS", "check": "flash frames", "detail": "none"})
    if r["frozen"]:
        worst = max(f["seconds"] for f in r["frozen"])
        c.append({"level": "FAIL" if worst >= 1.0 else "WARN", "check": "frozen frames",
                  "detail": "; ".join(f'{f["start"]:.2f}-{f["end"]:.2f}s ({f["frames"]} fr)' for f in r["frozen"])})
    else:
        c.append({"level": "PASS", "check": "frozen frames", "detail": "none"})
    if r["duplicate_frames"] > 0.05 * len(r["motion_t"]):
        c.append({"level": "WARN", "check": "duplicate frames",
                  "detail": f'{r["duplicate_frames"]} single repeated frames (frame-rate conversion? judder)'})
    bad_fl = [f for f in r["flicker"] if f["flicker"] > 1.5 or f["max_jump"] > 6]
    if bad_fl:
        c.append({"level": "WARN", "check": "luma flicker",
                  "detail": "; ".join(f'shot {f["shot"]} {f["start"]:.1f}-{f["end"]:.1f}s sd {f["flicker"]:.2f}, '
                                      f'jump {f["max_jump"]:.1f}' for f in bad_fl)})
    else:
        c.append({"level": "PASS", "check": "luma flicker", "detail": "no shot above sd 1.5 / jump 6"})
    al = [a for a in r["alignment"] if a["offset_ms"] is not None]
    if al:
        n_fail = sum(a["level"] == "FAIL" for a in al)
        n_warn = sum(a["level"] == "WARN" for a in al)
        c.append({"level": "WARN" if n_fail else "PASS", "check": "onset/motion alignment",
                  "detail": f"{len(al)} onsets paired: {len(al) - n_fail - n_warn} in window, {n_warn} borderline, "
                            f"{n_fail} off by > 4 frames early / 2 late. Heuristic: LOOK at the flagged times "
                            f"(a motion peak is not always the contact frame)."})
    if r["planned"]:
        n_bad = sum(p["level"] == "FAIL" for p in r["planned"])
        n_warn = sum(p["level"] == "WARN" for p in r["planned"])
        c.append({"level": "FAIL" if n_bad else "WARN" if n_warn else "PASS", "check": "planned sound events",
                  "detail": f"{len(r['planned'])} planned: {n_bad} missing/off, {n_warn} borderline"})
    return c


def build_strip(video: str, r: dict, step: float, out: Path) -> Path:
    frames, times = q.read_frames(video, width=160, fps=1.0 / step)
    cut_t = [c["t"] for c in r["cuts"]]
    borders, labels = [], []
    for t in times:
        b = None
        if any(t - step < ct <= t for ct in cut_t):
            b = (230, 40, 40)
        if any(f["start"] - step < t <= f["end"] + 1e-6 for f in r["flashes"]):
            b = (240, 200, 0)
        if any(f["start"] <= t <= f["end"] for f in r["frozen"]):
            b = (40, 120, 255)
        borders.append(b)
        labels.append(f"{t:.1f}s")
    sheet = q.tile(list(frames), labels, cols=10, border=borders)
    p = out / "strip.jpg"
    q.save_jpg(p, sheet, 82)
    return p


def build_onset_zoom(video: str, r: dict, out: Path, n: int = 10, half: int = 4) -> Path | None:
    """For the strongest onsets: the frames from -half to +half around the onset at native fps,
    the onset frame outlined in purple and the paired visual event in orange. This is how a
    human (or Claude) confirms the contact frame by eye - the measured lesson from AURUM v3."""
    al = sorted([a for a in r["alignment"]], key=lambda a: -a["strength"])[:n]
    al = sorted(al, key=lambda a: a["audio_t"])
    if not al:
        return None
    fps = r["fps"]
    frames, times = q.read_frames(video, width=120)
    imgs, labels, borders = [], [], []
    for a in al:
        k0 = int(round(a["audio_t"] * fps))
        kv = None if a["visual_t"] is None else int(round(a["visual_t"] * fps))
        for k in range(k0 - half, k0 + half + 1):
            kk = min(max(k, 0), len(frames) - 1)
            imgs.append(frames[kk])
            labels.append(f"{k / fps:.2f}" + (" A" if k == k0 else "") + (" V" if k == kv else ""))
            borders.append((150, 60, 230) if k == k0 else (240, 140, 40) if k == kv else None)
    sheet = q.tile(imgs, labels, cols=2 * half + 1, border=borders, label_scale=0.35)
    p = out / "onset_zoom.jpg"
    q.save_jpg(p, sheet, 80)
    return p


def write_reports(r: dict, cks: list[dict], out: Path, strip: Path) -> str:
    verdict = q.verdict_of(cks)
    fps = r["fps"]
    name = Path(r["video"]).name
    # ---------- markdown
    md = [f"# QC report: {name}", "", f"**Verdict: {verdict}**", "",
          q.md_table([[c["level"], c["check"], c["detail"]] for c in cks], ["Level", "Check", "Detail"]), "",
          f"![frame strip]({strip.name})", "", "![onset zoom](onset_zoom.jpg)", "", "## Shot cuts",
          q.md_table([[s["index"], f'{s["start"]:.2f}', f'{s["end"]:.2f}', f'{s["length"]:.2f}'] for s in r["shots"]],
                     ["shot", "start s", "end s", "length s"]), "",
          "## Event alignment (audio onset -> nearest visual event)",
          "Offset = audio minus picture. Negative = the sound leads (good up to 2 frames). "
          f"1 frame = {1000 / fps:.1f} ms.", "",
          q.md_table([[f'{a["audio_t"]:.3f}', f'{a["strength"]:.2f}',
                       "-" if a["visual_t"] is None else f'{a["visual_t"]:.3f}', a["kind"],
                       "-" if a["offset_ms"] is None else f'{a["offset_ms"]:+.0f}',
                       "-" if a["offset_frames"] is None else f'{a["offset_frames"]:+.1f}', a["level"], a["note"]]
                      for a in r["alignment"]],
                     ["audio s", "strength", "visual s", "visual kind", "offset ms", "frames", "level", "note"])]
    if r["planned"]:
        md += ["", "## Planned sound events (--events)",
               q.md_table([[f'{p["t"]:.2f}', p["label"], "-" if p["audio_t"] is None else f'{p["audio_t"]:.3f}',
                            "-" if p["offset_ms"] is None else f'{p["offset_ms"]:+.0f}', p["level"], p["note"]]
                           for p in r["planned"]], ["event s", "label", "onset s", "offset ms", "level", "note"])]
    md += ["", "## Audio onsets", ", ".join(f'{o["t"]:.2f}' for o in r["onsets"]) or "none",
           "", "## Motion peaks / stops / starts",
           ", ".join(f'{e["t"]:.2f}({e["kind"][0]})' for e in r["visual_events"] if e["kind"] != "cut") or "none",
           "", "## Flicker per shot",
           q.md_table([[f["shot"], f'{f["start"]:.1f}-{f["end"]:.1f}', f'{f["flicker"]:.2f}', f'{f["max_jump"]:.1f}']
                       for f in r["flicker"]], ["shot", "span s", "luma sd", "max jump"])]
    (out / "report.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # ---------- html
    dur = r["duration"]
    cut_marks = [{"t": c["t"], "color": "#d33", "w": 1.5, "label": f'cut {c["t"]:.2f}s'} for c in r["cuts"]]
    spans = [{"start": f["start"], "end": f["end"] + 1 / fps, "color": "#e0b000"} for f in r["flashes"]]
    spans += [{"start": f["start"], "end": f["end"], "color": "#2a7bff"} for f in r["frozen"]]
    env_svg = q.svg_series([{"t": r["env_t"], "y": np.maximum(r["env_db"], -60), "color": "#2a9d8f", "range": (-60, 0)}],
                           dur, marks=cut_marks + [{"t": o["t"], "color": "#8a2be2", "label": f'onset {o["t"]:.3f}s',
                                                    "y0": 0, "y1": 25} for o in r["onsets"]],
                           spans=spans, title="Audio RMS (dBFS, -60..0)  | purple ticks = onsets, red = cuts")
    mot_svg = q.svg_series([{"t": r["motion_t"], "y": r["motion_local"], "color": "#e76f51"},
                            {"t": r["motion_t"], "y": r["motion_global"], "color": "#999"}], dur,
                           marks=cut_marks + [{"t": e["t"], "color": {"motion_peak": "#e76f51", "stop/impact": "#264653",
                                                                      "start": "#f4a261"}.get(e["kind"], "#d33"),
                                               "label": f'{e["kind"]} {e["t"]:.3f}s', "y0": 0, "y1": 20}
                                              for e in r["visual_events"] if e["kind"] != "cut"],
                           spans=spans, title="Motion energy: orange = subject (local flow), grey = camera (global flow)")
    cv_svg = q.svg_series([{"t": r["motion_t"], "y": r["content"], "color": "#555"}], dur, marks=cut_marks,
                          title="HSV content change per frame (cut detector input)", height=90)
    H = [q.HTML_HEAD.format(title=f"QC {html.escape(name)}"),
         f"<h1>QC report: {html.escape(name)} <span class='{verdict}'>{verdict}</span></h1>",
         q.html_table([[c["level"], c["check"], c["detail"]] for c in cks], ["Level", "Check", "Detail"], level_col=0),
         "<h2>Frame strip (every %.1f s)</h2><p class='legend'><span style='color:#d33'>red = cut inside the interval</span>"
         "<span style='color:#e0b000'>yellow = flash frame</span><span style='color:#2a7bff'>blue = frozen</span></p>" % (
             r.get("strip_step", 0.5)),
         f"<img src='{strip.name}' alt='frame strip'>",
         "<h2>Timeline</h2>", env_svg, mot_svg, cv_svg,
         "<h2>Onset zoom (strongest onsets, native frames; purple = audio onset frame A, orange = paired visual event V)</h2>"
         "<img src='onset_zoom.jpg' alt='onset zoom'>",
         "<h2>Shot cuts</h2>",
         q.html_table([[s["index"], f'{s["start"]:.2f}', f'{s["end"]:.2f}', f'{s["length"]:.2f}'] for s in r["shots"]],
                      ["shot", "start s", "end s", "length s"]),
         f"<h2>Event alignment</h2><p>Offset = audio minus picture; negative = sound leads. 1 frame = {1000 / fps:.1f} ms. "
         "PASS = 2 frames early to 1 frame late. This pairing is a heuristic (like AV-Align): look at every WARN/FAIL row.</p>",
         q.html_table([[a["level"], f'{a["audio_t"]:.3f}', f'{a["strength"]:.2f}',
                        "-" if a["visual_t"] is None else f'{a["visual_t"]:.3f}', a["kind"],
                        "-" if a["offset_ms"] is None else f'{a["offset_ms"]:+.0f}',
                        "-" if a["offset_frames"] is None else f'{a["offset_frames"]:+.1f}', a["note"]]
                       for a in r["alignment"]],
                      ["level", "audio s", "strength", "visual s", "visual kind", "offset ms", "frames", "note"], level_col=0)]
    if r["planned"]:
        H += ["<h2>Planned sound events</h2>",
              q.html_table([[p["level"], f'{p["t"]:.2f}', p["label"], "-" if p["audio_t"] is None else f'{p["audio_t"]:.3f}',
                             "-" if p["offset_ms"] is None else f'{p["offset_ms"]:+.0f}', p["note"]] for p in r["planned"]],
                           ["level", "event s", "label", "onset s", "offset ms", "note"], level_col=0)]
    L = r["loudness"] or {}
    H += ["<h2>Loudness</h2>",
          q.html_table([[k, v] for k, v in L.items()] or [["audio", "none"]], ["measure", "value"]),
          "<h2>Flicker per shot</h2>",
          q.html_table([[f["shot"], f'{f["start"]:.1f}-{f["end"]:.1f}', f'{f["flicker"]:.2f}', f'{f["max_jump"]:.1f}']
                        for f in r["flicker"]], ["shot", "span s", "luma sd", "max jump"]),
          "</body></html>"]
    (out / "report.html").write_text("\n".join(H), encoding="utf-8")
    return verdict


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--out", help="output folder (default <video>_qc/)")
    ap.add_argument("--events", help="planned visual events: CSV 't,label' lines or JSON [{t,label}]")
    ap.add_argument("--audio-stem", help="analyse onsets on this file instead of the mix (e.g. the SFX stem)")
    ap.add_argument("--lufs", type=float, default=-14.0)
    ap.add_argument("--tp", type=float, default=-1.0)
    ap.add_argument("--strip-step", type=float, default=0.5)
    ap.add_argument("--top-onsets", type=int, default=30)
    ap.add_argument("--max-shot", type=float, help="WARN when a shot is longer (use 4 for action/chase films)")
    ap.add_argument("--stage", choices=["take", "deliverable"], default="deliverable",
                    help="take = a raw generated clip: loudness/no-audio are INFO, not FAIL")
    ap.add_argument("--json-only", action="store_true")
    a = ap.parse_args(argv)
    out = Path(a.out) if a.out else q.default_out(a.video, "qc")
    out.mkdir(parents=True, exist_ok=True)
    r = analyse(a.video, a)
    r["strip_step"] = a.strip_step
    cks = checks(r, a)
    strip = build_strip(a.video, r, a.strip_step, out) if not a.json_only else out / "strip.jpg"
    if not a.json_only:
        build_onset_zoom(a.video, r, out)
    verdict = write_reports(r, cks, out, strip) if not a.json_only else q.verdict_of(cks)
    slim = {k: v for k, v in r.items() if k not in ("motion_t", "motion_local", "motion_global", "env_t", "env_db", "content")}
    (out / "report.json").write_text(json.dumps(q.to_jsonable({"verdict": verdict, "checks": cks, **slim}), indent=1),
                                     encoding="utf-8")
    print(f"{verdict}  {a.video}")
    for c in cks:
        print(f"  {c['level']:4s} {c['check']}: {c['detail']}")
    print(f"  -> {out / 'report.html'}")
    return {"PASS": 0, "WARN": 1, "FAIL": 2}[verdict]


if __name__ == "__main__":
    sys.exit(main())
