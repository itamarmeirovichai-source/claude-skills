#!/usr/bin/env python3
"""ad-director: product -> concept seeds -> job folder -> automated QC.

Commands
  dice     draw N concept seeds that are different from each other AND from what
           this client (and the studio overall) already got (ledger-aware)
  log      record the seed that was produced, so it is not repeated
  history  show what a client already received
  new      scaffold a job folder (brief, concepts, script, shots, prompts, qc)
  qc       automated technical + pacing + product-fidelity checks on a render,
           plus a contact sheet with safe-zone overlay for the visual review
  bench    write the model benchmark matrix (tests x models) and a score sheet

Standard library + ffmpeg/ffprobe. `qc` also uses numpy and Pillow when present
(product-fidelity and flicker checks are skipped without them).
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
MATRIX_PATH = SKILL / "references" / "creative_matrix.json"
DEFAULT_LEDGER = Path(os.environ.get("AD_DIRECTOR_LEDGER", Path.home() / ".ad-director" / "ledger.jsonl"))
DIMS = ("mechanism", "format", "hook", "emotion", "structure", "look", "sonic")
# How much a repeat on each dimension hurts. Mechanism + format are the "idea";
# look/sonic are execution and may repeat more freely.
DIM_WEIGHT = {"mechanism": 3.0, "format": 3.0, "hook": 1.5, "emotion": 1.0,
              "structure": 1.0, "look": 0.75, "sonic": 0.75}
CLIENT_WINDOW = 8          # a client's last N jobs are "recent"


# ───────────────────────────── matrix / ledger ─────────────────────────────

def load_matrix(path: Path = MATRIX_PATH) -> dict:
    m = json.loads(Path(path).read_text(encoding="utf-8"))
    for d in DIMS:
        ids = [o["id"] for o in m[d]]
        if len(ids) != len(set(ids)):
            raise ValueError(f"duplicate ids in matrix dimension {d}")
    return m


def read_ledger(path: Path) -> list[dict]:
    if not Path(path).exists():
        return []
    out = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def append_ledger(path: Path, entry: dict) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ───────────────────────────── dice ─────────────────────────────

def _incompatible(seed: dict, rules: list[list[str]]) -> bool:
    vals = set(seed[d] for d in DIMS)
    return any(a in vals and b in vals for a, b in rules)


def novelty_penalty(seed: dict, ledger: list[dict], client: str | None) -> float:
    """Lower is fresher. Client-recent repeats cost a lot; studio-wide frequency costs a little."""
    pen = 0.0
    cl = _norm(client) if client else None
    recent = [e for e in ledger if cl and _norm(e.get("client", "")) == cl][-CLIENT_WINDOW:]
    for e in recent:
        s = e.get("seed", {})
        for d in DIMS:
            if s.get(d) == seed[d]:
                pen += DIM_WEIGHT[d]
        if s.get("mechanism") == seed["mechanism"] and s.get("format") == seed["format"]:
            pen += 20.0  # same idea skeleton for the same client: practically banned
    n = max(len(ledger), 1)
    for d in DIMS:
        freq = sum(1 for e in ledger if e.get("seed", {}).get(d) == seed[d]) / n
        pen += DIM_WEIGHT[d] * freq
    return pen


def distance(a: dict, b: dict) -> float:
    return sum(DIM_WEIGHT[d] for d in DIMS if a[d] != b[d])


def roll(matrix: dict, n: int = 5, client: str | None = None, ledger: list[dict] | None = None,
         seed: int | None = None, locks: dict | None = None, pool: int = 3000) -> list[dict]:
    """Return n concept seeds: fresh vs the ledger, mutually distant, never incompatible."""
    rng = random.Random(seed)
    ledger = ledger or []
    locks = locks or {}
    rules = matrix.get("_rules", {}).get("incompatible", [])
    for d, v in locks.items():
        if d not in DIMS or v not in [o["id"] for o in matrix[d]]:
            raise ValueError(f"bad lock {d}={v}")
    cands, seen = [], set()
    for _ in range(pool):
        s = {d: locks.get(d) or rng.choice(matrix[d])["id"] for d in DIMS}
        key = tuple(s[d] for d in DIMS)
        if key in seen or _incompatible(s, rules):
            continue
        seen.add(key)
        s["_pen"] = novelty_penalty(s, ledger, client) + rng.random() * 0.5
        cands.append(s)
    if not cands:
        raise ValueError("no valid combination (locks conflict with incompatibility rules?)")
    cands.sort(key=lambda s: s["_pen"])
    picks = [cands[0]]
    top = cands[: max(200, n * 40)]
    while len(picks) < n and len(picks) < len(top):
        # greedy max-min diversity, tie-broken by freshness
        best = max((c for c in top if c not in picks),
                   key=lambda c: (min(distance(c, p) for p in picks) - 0.3 * c["_pen"]))
        picks.append(best)
    constraints = list(matrix.get("constraint", []))
    rng.shuffle(constraints)
    out = []
    for i, p in enumerate(picks):
        p = {d: p[d] for d in DIMS}
        if constraints:
            p["constraint"] = constraints[i % len(constraints)]
        out.append(p)
    return out


def describe(seed: dict, matrix: dict) -> dict:
    idx = {d: {o["id"]: o for o in matrix[d]} for d in DIMS}
    out = {}
    for d in DIMS:
        o = idx[d][seed[d]]
        out[d] = o["label"] + (f" - {o['how']}" if o.get("how") else "")
    if seed.get("constraint"):
        out["constraint"] = seed["constraint"]
    return out


# ───────────────────────────── new job ─────────────────────────────

JOB_FILES = {
    "01-brief.md": """# Brief: {product}

Client: {client}    Date: {date}    Runs in: (US / FL / NY / IL ...)

## Product (verifiable facts only)
- Name / SKU:
- 3 facts the client can substantiate:
  1.
  2.
  3.
- Price tier:  | Where sold:
- Packshot files (front/side/back, transparent PNG):

## Brand
- Distinctive assets (colour, shape, sound, character, tagline):
- Tone (3 words):            | Never (3 words):
- Competitors and what their ads always show (cliches to ban):

## Audience
- Who:            | Mindset at the moment of viewing:
- What they do instead of buying:
- Their own words (reviews, comments, DMs):

## Goal & delivery
- One action:              | Platform(s):            | Lengths: 15s master + 6s + 30s?
- Budget (generation credits + hours):
- Mandatories / legal lines:
- Assumptions made [ASSUMED]:
""",
    "02-concepts.md": """# Concepts: {product}

Seeds rolled with `director.py dice --client "{client}"` (paste them here).
For each seed write: title (<=5 words) - one line (<=25 words) - key visual (<=15 words) - why it works.

| # | Seed (mechanism / format / hook) | Idea | Orig | Brand | Emotion | AI-feas | Cost | Legal | Total |
|---|---|---|---|---|---|---|---|---|---|

Gates: Legal <=2, AI-feasibility <=2 without hybrid fix, Brand <=2 -> killed.
Finalists (3): ... -> chosen: ...   Then: `director.py log --client "{client}" ...`
""",
    "03-script.md": """# Script: {product} - {{chosen concept}}

Length: 15s master (cutdowns 6s / 30s)    VO: yes/no (~2.5 words/s)
Turn (the one sentence the ad pivots on):

| Beat | Time | Picture | VO / dialogue | Super (post) | Sound |
|---|---|---|---|---|---|
| Hook | 0.0-1.5 | | | | |
| Setup | | | | | |
| Turn | | | | | |
| Proof | | | | | |
| Payoff + brand | | | | | |
| CTA | | | | | |

5 hook variants (first 2 s): anomaly / text-tension / sound-led / POV / payoff-first
""",
    "04-shots.csv": "shot,start,end,beat,description,size_angle_lens,light,camera_move_end_state,method,model,backup_model,risk,mitigation,takes_budget\n",
    "05-prompts.md": """# Prompts: {product}

Per shot: start-frame prompt (image model) -> video prompt (model from the router) -> notes.
Rules: one camera move with an end state, named light + direction, verbs over adjectives,
PRODUCT LOCK on product shots, cut on contact, no on-screen text, natural skin, <=6 negatives.

## Shot 1
- Start frame ({{image model}}):
- Video ({{video model}}):
- Keep / reject criteria:
""",
    "06-qc.md": """# QC: {product}

Automated: `director.py qc final.mp4 --packshot packshot.png --duration 15 --out qc/`
then fill the visual rubric (references/qc-rubric.md). Ship only if: no FAIL, score >= 80.

| Area | Score | Notes |
|---|---|---|
| Hook (0-2 s) | /15 | |
| Idea & brand linkage | /15 | |
| Product fidelity | /20 | |
| AI artifacts | /15 | |
| Motion & physics | /10 | |
| Sound | /10 | |
| Edit & text | /10 | |
| Legal & platform | /5 | |
| **Total** | /100 | |
""",
}


def cmd_new(job: Path, product: str, client: str) -> list[Path]:
    job.mkdir(parents=True, exist_ok=True)
    (job / "frames").mkdir(exist_ok=True)
    (job / "clips").mkdir(exist_ok=True)
    (job / "qc").mkdir(exist_ok=True)
    written = []
    for name, tpl in JOB_FILES.items():
        p = job / name
        if p.exists():
            continue
        p.write_text(tpl.format(product=product, client=client, date=_dt.date.today().isoformat()),
                     encoding="utf-8")
        written.append(p)
    return written


# ───────────────────────────── QC ─────────────────────────────

PLATFORM = {
    "reels": {"w": 1080, "h": 1920, "max_s": 90, "lufs": -14.0},
    "tiktok": {"w": 1080, "h": 1920, "max_s": 600, "lufs": -14.0},
    "shorts": {"w": 1080, "h": 1920, "max_s": 180, "lufs": -14.0},
    "feed45": {"w": 1080, "h": 1350, "max_s": 240, "lufs": -14.0},
}
SAFE = {"top": 0.14, "bottom": 0.35, "side": 0.06}


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path: str) -> dict:
    r = _run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path])
    if r.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {r.stderr.strip()}")
    return json.loads(r.stdout)


def _fps(stream: dict) -> float:
    num, _, den = stream.get("avg_frame_rate", "0/1").partition("/")
    try:
        return float(num) / float(den or 1)
    except ZeroDivisionError:
        return 0.0


def loudness(path: str) -> dict:
    r = _run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"])
    txt = r.stderr
    summ = txt[txt.rfind("Summary:"):] if "Summary:" in txt else txt
    i = re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", summ)
    tp = re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", summ)
    f = lambda m: (float(m.group(1)) if m and m.group(1) != "-inf" else None)
    return {"integrated_lufs": f(i), "true_peak_dbfs": f(tp)}


def scene_cuts(path: str, thr: float = 0.3) -> list[float]:
    r = _run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-an", "-vf",
              f"select='gt(scene,{thr})',showinfo", "-f", "null", "-"])
    return [round(float(m), 3) for m in re.findall(r"pts_time:([\d.]+)", r.stderr)]


def detect_intervals(path: str, filt: str, start_key: str, end_key: str, audio: bool = False) -> list[list[float]]:
    args = ["ffmpeg", "-hide_banner", "-nostats", "-i", path]
    args += (["-vn", "-af", filt] if audio else ["-an", "-vf", filt])
    r = _run(args + ["-f", "null", "-"])
    starts = [float(x) for x in re.findall(start_key + r":\s*(-?[\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(end_key + r":\s*(-?[\d.]+)", r.stderr)]
    out = []
    for i, s in enumerate(starts):
        out.append([round(s, 3), round(ends[i], 3) if i < len(ends) else None])
    return out


def sample_frames(path: str, fps: float, width: int = 160):
    """Return (times, list of HxWx3 uint8 arrays) or (None, None) without numpy."""
    try:
        import numpy as np
    except ImportError:
        return None, None
    info = probe(path)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    w, h = int(v["width"]), int(v["height"])
    hh = int(round(width * h / w / 2) * 2)
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={width}:{hh}",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    buf = np.frombuffer(r.stdout, dtype=np.uint8)
    n = buf.size // (width * hh * 3)
    frames = buf[: n * width * hh * 3].reshape(n, hh, width, 3)
    return [round(i / fps, 3) for i in range(n)], frames


def flicker_events(times, frames, cuts: list[float], jump: float = 14.0) -> list[float]:
    """Luma jumps between consecutive samples that are NOT at a scene cut (AI flicker / exposure pops)."""
    import numpy as np
    luma = frames.astype(np.float32).mean(axis=(1, 2, 3))
    ev = []
    for i in range(1, len(luma)):
        if abs(luma[i] - luma[i - 1]) > jump:
            t = times[i]
            if not any(abs(t - c) < 0.25 for c in cuts):
                ev.append(t)
    return ev


def _hist(img) -> "object":
    import numpy as np
    from PIL import Image
    im = Image.fromarray(img).convert("HSV").resize((96, 96))
    a = np.asarray(im).reshape(-1, 3)
    mask = a[:, 1] > 40  # ignore greys / white backdrops; brand colour lives in saturated pixels
    sel = a[mask] if mask.sum() > 50 else a
    h, _ = np.histogramdd(sel[:, :2], bins=(18, 4), range=((0, 256), (0, 256)))
    h = h.flatten()
    return h / (h.sum() or 1)


def product_match(packshot: str, times, frames, top: int = 3) -> list[dict]:
    """Rough brand-colour fidelity: hue/sat histogram intersection packshot vs each frame."""
    import numpy as np
    from PIL import Image
    ps = Image.open(packshot).convert("RGBA")
    bg = Image.new("RGBA", ps.size, (255, 255, 255, 255))
    ps = np.asarray(Image.alpha_composite(bg, ps).convert("RGB"))
    hp = _hist(ps)
    scores = [float(np.minimum(hp, _hist(f)).sum()) for f in frames]
    order = sorted(range(len(scores)), key=lambda i: -scores[i])[:top]
    return [{"t": times[i], "score": round(scores[i], 3)} for i in order]


def qc_sheet(path: str, out_jpg: Path, n: int = 12, safe: dict = SAFE) -> None:
    """Contact sheet; each tile has the platform UI safe zones shaded red."""
    dur = float(probe(path)["format"]["duration"])
    step = dur / n
    rate = 1 / (step * 0.98)  # slightly faster than 1/step so exactly n tiles fill
    tile = "fps={:.5f},scale=270:-2,drawbox=x=0:y=0:w=iw:h=ih*{t}:color=red@0.28:t=fill," \
           "drawbox=x=0:y=ih*(1-{b}):w=iw:h=ih*{b}:color=red@0.28:t=fill," \
           "drawbox=x=0:y=0:w=iw*{s}:h=ih:color=red@0.28:t=fill," \
           "drawbox=x=iw*(1-{s}):y=0:w=iw*{s}:h=ih:color=red@0.28:t=fill," \
           "drawtext=text='%{{pts\\:hms}}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6," \
           "tile=6x{rows}:padding=4".format(1 / step, t=safe["top"], b=safe["bottom"], s=safe["side"],
                                            rows=math.ceil(n / 6))
    tile = tile.replace("fps={:.5f}".format(1 / step), "fps={:.5f}".format(rate), 1)
    r = _run(["ffmpeg", "-v", "error", "-y", "-ss", f"{step / 2:.3f}", "-i", path, "-vf", tile,
              "-frames:v", "1", str(out_jpg)])
    if r.returncode != 0:  # drawtext may lack a font; retry without timestamps
        tile2 = re.sub(r"drawtext=[^,]*,", "", tile)
        _run(["ffmpeg", "-v", "error", "-y", "-ss", f"{step / 2:.3f}", "-i", path, "-vf", tile2,
              "-frames:v", "1", str(out_jpg)])


def compare_sheet(path: str, packshot: str, ts: list[float], out_jpg: Path) -> None:
    from PIL import Image
    tiles = [Image.open(packshot).convert("RGBA")]
    bg = Image.new("RGBA", tiles[0].size, (255, 255, 255, 255))
    tiles[0] = Image.alpha_composite(bg, tiles[0]).convert("RGB")
    tmp = out_jpg.parent
    for i, t in enumerate(ts):
        f = tmp / f"_cmp{i}.png"
        _run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", str(f)])
        if f.exists():
            tiles.append(Image.open(f).convert("RGB"))
    H = 640
    tiles = [im.resize((max(1, int(im.width * H / im.height)), H)) for im in tiles]
    sheet = Image.new("RGB", (sum(t.width for t in tiles) + 8 * (len(tiles) - 1), H), "black")
    x = 0
    for t in tiles:
        sheet.paste(t, (x, 0))
        x += t.width + 8
    sheet.save(out_jpg, quality=88)
    for f in tmp.glob("_cmp*.png"):
        f.unlink()


def evaluate(m: dict, platform: str = "reels", duration: float | None = None) -> list[dict]:
    """Turn raw measurements into PASS/WARN/FAIL findings. Pure function (unit-tested)."""
    P = PLATFORM[platform]
    F = []
    add = lambda level, check, msg: F.append({"level": level, "check": check, "msg": msg})
    w, h = m["width"], m["height"]
    if (w, h) != (P["w"], P["h"]):
        lvl = "WARN" if abs(w / h - P["w"] / P["h"]) < 0.01 else "FAIL"
        add(lvl, "resolution", f"{w}x{h}, expected {P['w']}x{P['h']}")
    else:
        add("PASS", "resolution", f"{w}x{h}")
    if m["fps"] < 23.5:
        add("FAIL", "fps", f"{m['fps']:.2f} fps")
    else:
        add("PASS", "fps", f"{m['fps']:.2f} fps")
    if m["vcodec"] != "h264" or m.get("acodec") not in ("aac", None):
        add("WARN", "codec", f"{m['vcodec']}/{m.get('acodec')} (h264/aac is safest for upload)")
    d = m["duration"]
    if duration is not None and abs(d - duration) > 0.5:
        add("FAIL", "duration", f"{d:.2f}s, target {duration}s")
    elif d > P["max_s"]:
        add("FAIL", "duration", f"{d:.1f}s exceeds {platform} max {P['max_s']}s")
    else:
        add("PASS", "duration", f"{d:.2f}s")
    if m.get("acodec") is None:
        add("WARN", "audio", "no audio track (sound-on platforms reward sound)")
    else:
        L, tp = m.get("lufs"), m.get("true_peak")
        if L is None:
            add("FAIL", "loudness", "silent audio")
        elif abs(L - P["lufs"]) > 1.5:
            add("WARN", "loudness", f"{L:.1f} LUFS, target {P['lufs']} +-1.5")
        else:
            add("PASS", "loudness", f"{L:.1f} LUFS")
        if tp is not None and tp > -1.0:
            add("WARN", "true_peak", f"{tp:.1f} dBTP > -1.0 (clipping after platform transcode)")
        if m.get("silence_at_start", 0) > 0.6:
            add("WARN", "audio_hook", f"first {m['silence_at_start']:.1f}s silent - the hook has no sound")
    cuts = [c for c in m["cuts"] if c > 0.05]
    first_change = cuts[0] if cuts else d
    if first_change > 3.0 and not m.get("one_take"):
        add("WARN", "hook_pacing", f"first cut at {first_change:.1f}s - nothing changes in the first 3s")
    else:
        add("PASS", "hook_pacing", f"first cut at {first_change:.1f}s")
    bounds = [0.0] + cuts + [d]
    shots = [round(b - a, 2) for a, b in zip(bounds, bounds[1:]) if b - a > 0.05]
    longest = max(shots) if shots else d
    if longest > 4.5 and not m.get("one_take"):
        add("WARN", "shot_length", f"longest shot {longest:.1f}s (>4.5s drags on Reels unless it is a one-take)")
    add("INFO", "shots", f"{len(shots)} shots, avg {sum(shots) / max(len(shots), 1):.2f}s")
    for s, e in m.get("black", []):
        if s < 0.2 or (e is not None and e < d - 0.3):
            add("FAIL" if s < 0.2 else "WARN", "black_frames", f"black {s}-{e}s")
    for s, e in m.get("freeze", []):
        if (e is None or e >= d - 0.3) and s >= d - 3.0:
            add("INFO", "end_card", f"held frame {s}-{e}s (end card / packshot hold)")
        else:
            add("WARN", "frozen", f"frozen picture {s}-{e}s (stalled AI clip or held frame?)")
    if m.get("flicker"):
        add("WARN", "flicker", f"{len(m['flicker'])} luma jumps outside cuts at {m['flicker'][:6]} - check AI flicker")
    pm = m.get("product_match")
    if pm is not None:
        best = pm[0]["score"] if pm else 0
        if best < 0.35:
            add("FAIL", "product_colour", f"best brand-colour match {best:.2f} - packaging colour drifted or product missing")
        elif best < 0.5:
            add("WARN", "product_colour", f"best brand-colour match {best:.2f} - verify label/colour in compare sheet")
        else:
            add("PASS", "product_colour", f"best brand-colour match {best:.2f} at {pm[0]['t']}s")
    return F


def cmd_qc(path: str, packshot: str | None, duration: float | None, platform: str, out: Path,
           one_take: bool = False) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    info = probe(path)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    m = {"file": path, "width": int(v["width"]), "height": int(v["height"]), "fps": _fps(v),
         "vcodec": v.get("codec_name"), "acodec": a.get("codec_name") if a else None,
         "duration": float(info["format"]["duration"]), "one_take": one_take}
    if a:
        m.update({"lufs": None, "true_peak": None})
        L = loudness(path)
        m["lufs"], m["true_peak"] = L["integrated_lufs"], L["true_peak_dbfs"]
        sil = detect_intervals(path, "silencedetect=n=-45dB:d=0.3", "silence_start", "silence_end", audio=True)
        m["silence_at_start"] = (sil[0][1] or m["duration"]) if sil and sil[0][0] <= 0.05 else 0.0
    m["cuts"] = scene_cuts(path)
    m["black"] = detect_intervals(path, "blackdetect=d=0.15:pix_th=0.10", "black_start", "black_end")
    m["freeze"] = detect_intervals(path, "freezedetect=n=0.003:d=0.8", "freeze_start", "freeze_end")
    times, frames = sample_frames(path, fps=6)
    if frames is not None and len(frames):
        m["flicker"] = flicker_events(times, frames, m["cuts"])
        if packshot:
            try:
                m["product_match"] = product_match(packshot, times, frames)
            except ImportError:
                pass
    findings = evaluate(m, platform, duration)
    qc_sheet(path, out / "qc_sheet.jpg")
    if packshot and m.get("product_match"):
        compare_sheet(path, packshot, [p["t"] for p in m["product_match"]], out / "product_compare.jpg")
    verdict = "FAIL" if any(f["level"] == "FAIL" for f in findings) else \
              "WARN" if any(f["level"] == "WARN" for f in findings) else "PASS"
    report = {"verdict": verdict, "measurements": m, "findings": findings}
    (out / "qc_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = [f"# Automated QC - {Path(path).name}", "", f"**Verdict: {verdict}**", "",
             "| Level | Check | Detail |", "|---|---|---|"]
    lines += [f"| {f['level']} | {f['check']} | {f['msg']} |" for f in findings]
    lines += ["", "Visual review next: open `qc_sheet.jpg` (red = platform UI zones; no text/logo/face there)"
              + (" and `product_compare.jpg` (packshot vs best frames)." if packshot else "."),
              "Then score `references/qc-rubric.md`."]
    (out / "qc_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


# ───────────────────────────── bench ─────────────────────────────

BENCH_TESTS = [
    ("T01", "label_lock_rotate", "I2V", "Product packshot as start frame; slow 90-degree orbit; label must stay legible and unchanged."),
    ("T02", "pour_liquid", "I2V", "Pour into a glass, ice, bubbles; liquid volume and physics must be plausible; no glass morph."),
    ("T03", "hand_pickup", "I2V", "Hand enters, picks product up and lifts to camera; 5 fingers, no clipping, label intact."),
    ("T04", "macro_texture", "T2V", "Macro of cream/serum texture spreading; no plastic look."),
    ("T05", "food_bite", "T2V", "Person bites a burger/pastry; crumbs, believable chewing, natural skin."),
    ("T06", "talking_human_lipsync", "T2V+audio", "Person says one 8-word line to camera; lip-sync, teeth, eyes, natural skin."),
    ("T07", "scale_fooh", "I2V", "Giant product in a real street/beach (Boca/Miami look); correct perspective, shadows, scale."),
    ("T08", "fast_action_camera", "T2V", "Fast FPV/dolly through a scene ending on product; no warping, coherent geometry."),
    ("T09", "multi_shot_consistency", "T2V multi-shot", "3-shot sequence with the same character and product; identity and wardrobe hold."),
    ("T10", "text_in_scene", "T2V", "A neon sign with a 2-word brand name in the background; spelling correct."),
    ("T11", "v2v_blockout", "V2V", "Blender blockout to photoreal; layout and camera respected."),
    ("T12", "stylised_world", "I2V", "Claymation/miniature world with the product as a character; style consistent all clip."),
]
BENCH_MODELS = ["seedance25", "kling30pro", "veo31", "minimax_h3", "wan30", "omni_flash", "runway45"]
SCORE_COLS = ["prompt_adherence", "product_fidelity", "artifacts", "motion_physics", "aesthetic",
              "audio", "time_to_keeper_takes", "cost_usd"]


def cmd_bench(out: Path, models: list[str]) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    m = out / "bench_matrix.csv"
    with open(m, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["test", "name", "mode", "goal", "model", "take", "seed"] + SCORE_COLS + ["notes", "clip_path"])
        for tid, name, mode, goal in BENCH_TESTS:
            for mod in models:
                for take in (1, 2):
                    wr.writerow([tid, name, mode, goal, mod, take, ""] + [""] * len(SCORE_COLS) + ["", ""])
    return [m]


def summarize_bench(csv_path: Path) -> dict:
    """Per test: best model by mean quality (1-5 cols), with cost as tiebreak. Returns {test: ranking}."""
    qual = ["prompt_adherence", "product_fidelity", "artifacts", "motion_physics", "aesthetic"]
    agg: dict = {}
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            vals = [float(row[c]) for c in qual if row.get(c, "").strip()]
            if not vals:
                continue
            k = (row["test"], row["model"])
            a = agg.setdefault(k, {"q": [], "cost": []})
            a["q"].append(sum(vals) / len(vals))
            if row.get("cost_usd", "").strip():
                a["cost"].append(float(row["cost_usd"]))
    res: dict = {}
    for (t, mod), a in agg.items():
        q = sum(a["q"]) / len(a["q"])
        c = sum(a["cost"]) / len(a["cost"]) if a["cost"] else float("inf")
        res.setdefault(t, []).append({"model": mod, "quality": round(q, 2), "cost": c})
    for t in res:
        res[t].sort(key=lambda r: (-r["quality"], r["cost"]))
    return res


# ───────────────────────────── CLI ─────────────────────────────

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="director.py", description=__doc__.splitlines()[0])
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("dice", help="draw fresh, mutually different concept seeds")
    d.add_argument("--client", default=None)
    d.add_argument("-n", type=int, default=5)
    d.add_argument("--seed", type=int, default=None)
    d.add_argument("--lock", action="append", default=[], help="dim=id, e.g. --lock format=heist")
    d.add_argument("--json", action="store_true")
    lg = sub.add_parser("log", help="record a produced concept in the ledger")
    lg.add_argument("--client", required=True)
    lg.add_argument("--title", required=True)
    lg.add_argument("--seed-json", required=True, help='the seed object from dice, as JSON')
    lg.add_argument("--product", default="")
    lg.add_argument("--result", default="", help="e.g. client chose / hook rate 38%% / rejected")
    hi = sub.add_parser("history", help="what a client already received")
    hi.add_argument("--client", default=None)
    nw = sub.add_parser("new", help="scaffold a job folder")
    nw.add_argument("job")
    nw.add_argument("--product", required=True)
    nw.add_argument("--client", default="spec")
    q = sub.add_parser("qc", help="automated QC of a rendered ad")
    q.add_argument("video")
    q.add_argument("--packshot", default=None)
    q.add_argument("--duration", type=float, default=None)
    q.add_argument("--platform", choices=sorted(PLATFORM), default="reels")
    q.add_argument("--one-take", action="store_true", help="don't flag long shots / late first cut")
    q.add_argument("--out", default=None)
    b = sub.add_parser("bench", help="write the model benchmark matrix")
    b.add_argument("--out", default="bench")
    b.add_argument("--models", default=",".join(BENCH_MODELS))
    bs = sub.add_parser("bench-summary", help="rank models per test from a filled matrix")
    bs.add_argument("csv")
    a = ap.parse_args(argv)
    ledger_path = Path(a.ledger)

    if a.cmd == "dice":
        mx = load_matrix()
        locks = dict(x.split("=", 1) for x in a.lock)
        seeds = roll(mx, a.n, a.client, read_ledger(ledger_path), a.seed, locks)
        if a.json:
            print(json.dumps(seeds, indent=2))
        else:
            for i, s in enumerate(seeds, 1):
                print(f"\n── Seed {i} ── {json.dumps(s, ensure_ascii=False)}")
                for k, v in describe(s, mx).items():
                    print(f"  {k:<10} {v}")
    elif a.cmd == "log":
        seed = json.loads(a.seed_json)
        missing = [x for x in DIMS if x not in seed]
        if missing:
            ap.error(f"seed missing {missing}")
        append_ledger(ledger_path, {"date": _dt.date.today().isoformat(), "client": a.client,
                                    "product": a.product, "title": a.title, "seed": seed, "result": a.result})
        print(f"logged to {ledger_path}")
    elif a.cmd == "history":
        rows = [e for e in read_ledger(ledger_path) if not a.client or _norm(e["client"]) == _norm(a.client)]
        for e in rows:
            s = e["seed"]
            print(f"{e['date']}  {e['client']:<18} {e['title']:<28} {s['mechanism']}/{s['format']}/{s['hook']}  {e.get('result', '')}")
        if not rows:
            print("(no entries)")
    elif a.cmd == "new":
        for p in cmd_new(Path(a.job), a.product, a.client):
            print(p)
    elif a.cmd == "qc":
        if not shutil.which("ffmpeg"):
            ap.error("ffmpeg not found")
        out = Path(a.out) if a.out else Path(a.video).with_suffix("").parent / "qc"
        rep = cmd_qc(a.video, a.packshot, a.duration, a.platform, out, a.one_take)
        print((out / "qc_report.md").read_text())
        return 1 if rep["verdict"] == "FAIL" else 0
    elif a.cmd == "bench":
        for p in cmd_bench(Path(a.out), [m.strip() for m in a.models.split(",") if m.strip()]):
            print(p)
    elif a.cmd == "bench-summary":
        for t, ranks in sorted(summarize_bench(Path(a.csv)).items()):
            print(t, "  ".join(f"{r['model']}={r['quality']}" for r in ranks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
