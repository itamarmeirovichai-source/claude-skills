#!/usr/bin/env python3
"""lipsync_check.py - does the mouth follow the voice, and by how many ms is it off?

    python3 lipsync_check.py VIDEO [--audio line.wav] [--audio-delay 0.125] [--box x,y,w,h]
                             [--engine auto|syncnet|heuristic] [--start S --end E] [--out DIR]

Engines
  syncnet   (default when torch is installed) the pretrained SyncNet of Chung & Zisserman 2016,
            evaluated exactly like syncnet_python: 25 fps face crops vs MFCC, +-15 frames (+-600 ms).
            Outputs AV offset (frames of 40 ms) and confidence (median - min distance).
  heuristic (no torch) mouth-region motion of a landmark-stabilised crop (YuNet) cross-correlated
            with the speech-band envelope. Coarse: use it to catch gross failures only.

Face: auto-detected with YuNet (largest face, smoothed); --box x,y,w,h forces a face box (in source
pixels) for stylised characters the detector misses. --audio replaces the clip's own audio (e.g. the
TTS line that drove a silent Wan/Kling lip-sync render); --audio-delay shifts it like the edit will.

Sign convention (ITU-R BT.1359): audio_lead_ms > 0 means the sound comes BEFORE the mouth (the mouth
is late). Fix it by delaying the audio by audio_lead_ms (or advancing it when negative).

Verdict
  confidence: PASS >= 5, WARN 3-5, FAIL < 3 (no reliable sync: wrong line, mouth hidden or not moving)
  offset:     PASS -80..+40 ms, WARN up to -125 / +90 ms, FAIL beyond (BT.1359 detectability is
              +45 ms audio-early / -125 ms audio-late; SyncNet resolution is one 40 ms frame).
Exit code 0 PASS, 1 WARN, 2 FAIL.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy import signal as sps

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qclib as q  # noqa: E402
import cv2  # noqa: E402

CONF_PASS, CONF_WARN = 5.0, 3.0


def offset_level(lead_ms: float) -> str:
    if -80 <= lead_ms <= 40:
        return "PASS"
    if -125 <= lead_ms <= 90:
        return "WARN"
    return "FAIL"


def track_faces(frames_rgb: np.ndarray, box: list[float] | None, fm: q.FaceModel) -> tuple[np.ndarray, np.ndarray, float]:
    """Per-frame face box and 5 landmarks (NaN where missing), smoothed. Returns boxes, lms, coverage."""
    n = len(frames_rgb)
    B = np.full((n, 4), np.nan)
    L = np.full((n, 5, 2), np.nan)
    prev = None
    for i, f in enumerate(frames_rgb):
        bgr = cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
        faces = fm.detect(bgr)
        if box is not None:
            # keep the detection inside the forced box, else use the box itself
            bx = box
            inside = [d for d in faces if abs((d["box"][0] + d["box"][2] / 2) - (bx[0] + bx[2] / 2)) < bx[2] / 2
                      and abs((d["box"][1] + d["box"][3] / 2) - (bx[1] + bx[3] / 2)) < bx[3] / 2]
            if inside:
                d = max(inside, key=lambda d: d["score"])
                B[i] = d["box"]
                if d["lm"] is not None:
                    L[i] = d["lm"]
            else:
                B[i] = bx
            continue
        if not faces:
            continue
        if prev is None:
            d = max(faces, key=lambda d: d["box"][2] * d["box"][3])
        else:  # follow the same person
            d = min(faces, key=lambda d: np.hypot(d["box"][0] - prev[0], d["box"][1] - prev[1]))
        B[i] = d["box"]
        prev = d["box"]
        if d["lm"] is not None:
            L[i] = d["lm"]
    cover = float(np.mean(~np.isnan(B[:, 0])))
    for arr in (B.reshape(n, -1), L.reshape(n, -1)):
        for j in range(arr.shape[1]):
            v = arr[:, j]
            bad = np.isnan(v)
            if bad.all():
                continue
            if bad.any():
                v[bad] = np.interp(np.flatnonzero(bad), np.flatnonzero(~bad), v[~bad])
            arr[:, j] = sps.medfilt(v, 5) if n >= 5 else v
    return B, L, cover


def load_audio(video: str, audio: str | None, delay: float, sr: int = 16000) -> np.ndarray | None:
    x = q.read_audio(audio or video, sr)
    if x is None:
        return None
    n = int(round(abs(delay) * sr))
    if delay > 0:
        x = np.concatenate([np.zeros(n, np.float32), x])
    elif delay < 0:
        x = x[n:]
    return x


def run_syncnet(frames_rgb, boxes, audio16k, start_t: float):
    import syncnet_engine as se
    crops = [se.face_crop(cv2.cvtColor(f, cv2.COLOR_RGB2BGR), b) for f, b in zip(frames_rgb, boxes)]
    a0 = int(round(start_t * 16000))
    r = se.evaluate(crops, audio16k[a0:a0 + int(len(crops) / 25 * 16000) + 1600])
    if not r.get("ok"):
        return r
    r["audio_lead_ms"] = r["offset_frames"] * 40.0
    r["engine"] = "syncnet"
    r["crops_preview"] = crops[:: max(1, len(crops) // 12)][:12]
    return r


def run_heuristic(frames_rgb, lms, boxes, audio16k, fps: float, start_t: float):
    n = len(frames_rgb)
    crops = []
    for f, l, b in zip(frames_rgb, lms, boxes):
        g = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY)
        if np.isnan(l).any():
            x, y, w, h = b
            x0, x1, y0, y1 = x + 0.2 * w, x + 0.8 * w, y + 0.6 * h, y + 1.05 * h
        else:
            reye, leye, nose, rm, lm = l
            mc = (rm + lm) / 2
            s = max(np.linalg.norm(lm - rm), 0.6 * np.linalg.norm(leye - reye))
            x0, x1, y0, y1 = mc[0] - s, mc[0] + s, (nose[1] + mc[1]) / 2, mc[1] + 1.3 * s
        H, W = g.shape
        c = g[int(max(0, y0)):int(min(H, y1)), int(max(0, x0)):int(min(W, x1))]
        crops.append(cv2.resize(c, (48, 48)).astype(np.float32) if c.size else np.zeros((48, 48), np.float32))
    C = np.stack(crops)
    mot = np.r_[0, np.abs(np.diff(C[:, 10:38, 10:38], axis=0)).mean(axis=(1, 2))]
    t_v = start_t + np.arange(n) / fps
    b, a = sps.butter(4, [300 / 8000, 3000 / 8000], "band")
    x = sps.filtfilt(b, a, audio16k)
    t_a, db = q.rms_envelope(x, 16000, 0.01, 0.04)
    db = np.maximum(db, db.max() - 40)
    T = np.arange(max(t_v[0], t_a[0]) + 0.3, min(t_v[-1], t_a[-1]) - 0.3, 0.01)
    if len(T) < 100:
        return {"ok": False, "reason": "too short"}
    aa = np.interp(T, t_a, db)
    vv = np.interp(T, t_v, sps.medfilt(mot, 3))
    lags = np.arange(-0.6, 0.601, 0.01)
    cs = np.array([np.corrcoef(np.interp(T + L, t_v, sps.medfilt(mot, 3)), aa)[0, 1] for L in lags])
    i = int(np.nanargmax(cs))
    conf = float(cs[i] - np.nanmedian(cs))
    return {"ok": True, "engine": "heuristic", "audio_lead_ms": float(lags[i] * 1000), "corr": float(cs[i]),
            "confidence": conf * 10, "curve": cs.tolist(),
            "crops_preview": [cv2.cvtColor(c.astype(np.uint8), cv2.COLOR_GRAY2BGR) for c in C[:: max(1, n // 12)][:12]],
            "note": "heuristic engine: offset is coarse (+-80 ms); install torch for SyncNet"}


def windows(frames_rgb, boxes, audio16k, start_t, win_s=2.0, hop_s=1.0):
    """SyncNet on sliding windows: catches drift and dead stretches inside a longer take."""
    import syncnet_engine as se
    out = []
    n = len(frames_rgb)
    w, h = int(win_s * 25), int(hop_s * 25)
    for s in range(0, max(1, n - w + 1), h):
        crops = [se.face_crop(cv2.cvtColor(f, cv2.COLOR_RGB2BGR), b) for f, b in zip(frames_rgb[s:s + w], boxes[s:s + w])]
        t0 = start_t + s / 25
        a0 = int(round(t0 * 16000))
        r = se.evaluate(crops, audio16k[a0:a0 + int(win_s * 16000) + 1600], vshift=10)
        if r.get("ok"):
            out.append({"start": t0, "end": t0 + win_s, "audio_lead_ms": r["offset_frames"] * 40.0,
                        "confidence": r["confidence"]})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--audio", help="external audio (the line that drove the render); default: the clip's own")
    ap.add_argument("--audio-delay", type=float, default=0.0, help="seconds to delay (+) or advance (-) the audio")
    ap.add_argument("--box", help="x,y,w,h face box in source pixels (skip auto detection)")
    ap.add_argument("--engine", choices=["auto", "syncnet", "heuristic"], default="auto")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float)
    ap.add_argument("--windows", action="store_true", help="also report per-2 s window offsets (drift)")
    ap.add_argument("--out", help="output folder (default <video>_lipsync/)")
    a = ap.parse_args(argv)

    info = q.probe(a.video)
    out = Path(a.out) if a.out else q.default_out(a.video, "lipsync")
    out.mkdir(parents=True, exist_ok=True)
    audio = load_audio(a.video, a.audio, a.audio_delay)
    if audio is None:
        print("FAIL  no audio: pass --audio line.wav for a silent lip-sync render")
        return 2
    end = a.end or info["duration"]
    width = min(720, info["width"])
    scale = width / info["width"]
    frames, _ = q.read_frames(a.video, width=width, fps=25, start=a.start, duration=end - a.start)
    box = [float(v) * scale for v in a.box.split(",")] if a.box else None
    fm = q.FaceModel(want_embed=False)
    boxes, lms, cover = track_faces(frames, box, fm)
    if np.isnan(boxes).all():
        print("FAIL  no face found: pass --box x,y,w,h")
        return 2

    engine = a.engine
    if engine == "auto":
        try:
            import syncnet_engine as se
            engine = "syncnet" if se.AVAILABLE else "heuristic"
        except Exception:
            engine = "heuristic"
    if engine == "syncnet":
        r = run_syncnet(frames, boxes, audio, a.start)
    else:
        r = run_heuristic(frames, lms, boxes, audio, 25.0, a.start)
    if not r.get("ok"):
        print(f"FAIL  {r.get('reason')}")
        return 2

    lead = r["audio_lead_ms"]
    conf = r["confidence"]
    c_level = "PASS" if conf >= CONF_PASS else "WARN" if conf >= CONF_WARN else "FAIL"
    o_level = offset_level(lead) if c_level != "FAIL" else "INFO"
    if engine == "heuristic":
        c_level = "WARN" if c_level == "PASS" else c_level  # never certify with the coarse engine
    levels = [c_level, o_level]
    verdict = "FAIL" if "FAIL" in levels else "WARN" if "WARN" in levels else "PASS"
    advice = ""
    if c_level == "FAIL":
        advice = ("No reliable lip sync: the mouth is hidden/static or this is not the line it speaks. "
                  "Do not put a voice on this face: use VO with the mouth off-screen, or re-render.")
    elif o_level != "PASS":
        advice = (f"Shift the audio by {lead:+.0f} ms (delay it {'more' if lead > 0 else 'less'}) "
                  f"and re-run; measured mouth is {'late' if lead > 0 else 'early'} vs the sound.")
    wins = windows(frames, boxes, audio, a.start) if (a.windows and engine == "syncnet") else []
    if wins:
        leads = [w["audio_lead_ms"] for w in wins if w["confidence"] >= CONF_WARN]
        dead = [w for w in wins if w["confidence"] < CONF_WARN]
        if leads and (max(leads) - min(leads)) > 120:
            verdict = "FAIL" if verdict != "FAIL" else verdict
            advice += f" Offset drifts across the take ({min(leads):+.0f}..{max(leads):+.0f} ms)."
        if dead:
            advice += " Weak-sync windows: " + ", ".join(f'{w["start"]:.1f}-{w["end"]:.1f}s' for w in dead) + "."

    # preview sheet: the crops SyncNet actually saw
    prev = [cv2.cvtColor(cv2.resize(c, (112, 112)), cv2.COLOR_BGR2RGB) for c in r.pop("crops_preview")]
    q.save_jpg(out / "crops.jpg", q.tile(prev, [f"#{i}" for i in range(len(prev))], cols=12), 80)
    res = {"video": a.video, "audio": a.audio or a.video, "audio_delay_s": a.audio_delay, "engine": engine,
           "face_coverage": cover, "audio_lead_ms": lead, "confidence": conf, "confidence_level": c_level,
           "offset_level": o_level, "verdict": verdict, "advice": advice.strip(), "windows": wins,
           **{k: v for k, v in r.items() if k not in ("ok",)}}
    (out / "lipsync.json").write_text(json.dumps(q.to_jsonable(res), indent=1), encoding="utf-8")
    print(f"{verdict}  {Path(a.video).name}  engine={engine}  audio_lead={lead:+.0f} ms  "
          f"confidence={conf:.2f}  face_coverage={cover:.0%}")
    if advice:
        print("  " + advice.strip())
    return {"PASS": 0, "WARN": 1, "FAIL": 2}[verdict]


if __name__ == "__main__":
    sys.exit(main())
