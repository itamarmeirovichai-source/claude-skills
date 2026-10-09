#!/usr/bin/env python3
"""continuity_check.py - does the same face / product / prop stay the same across shots and seams?

    python3 continuity_check.py VIDEO [--out DIR] [--fps 2]
        [--ref-face otto=ref/otto.png --ref-face vee=ref/vee.png] [--cast 2]
        [--object glass=9.0:400,700,180,420 --object glass=14.5:380,650,170,400 ...]
        [--ref-object can=ref/can.png] [--seamless]

What it measures (no paid API; optional small ONNX models are fetched once into ~/.cache/ad-director-qc):
  1. Shots: hard cuts (same detector as qc_report).
  2. Frame drift (VBench-style subject consistency): DINOv2 similarity of each sampled frame to the
     previous one. A drop inside a shot = a morph / jump; across a seam of a "one-take" (--seamless)
     it is a visible seam.
  3. Faces: YuNet detection + SFace identity embeddings at every sample. Faces are tracked inside a
     shot; a track whose identity similarity to its own start falls below the threshold = identity
     drift (the face morphs into someone else). With --ref-face every face is scored against the
     references (SFace "same person" threshold 0.363). Faces are clustered into identities; more
     identities than --cast = a character changed between shots.
  4. Named objects: --object NAME=T:x,y,w,h (source pixels, repeat per time) crops the same prop at
     different moments and compares every pair (DINOv2 cosine, perceptual hash distance, colour
     histogram distance, box aspect). Big changes = the glass/can/label changed shape.
  5. Reference objects: --ref-object NAME=img.png searches each sampled frame for the region most
     similar to the reference (multi-scale DINOv2 window search) and reports the best similarity per
     sample; drops mark frames where the product is missing or has drifted (label, shape, colour).

Writes DIR/continuity.md, DIR/continuity.json and contact sheets (faces.jpg, objects.jpg,
ref_<name>.jpg, seams.jpg). Exit code 0 PASS, 1 WARN, 2 FAIL.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qclib as q  # noqa: E402
import cv2  # noqa: E402

# Thresholds (calibrated on our AURUM / heist / W06 material, see references/marketing/46-sound-and-qc.md)
FACE_SAME = q.SFACE_SAME          # 0.363: OpenCV SFace cosine threshold for one identity
FACE_DRIFT = 0.30                 # a track whose similarity to its own start falls below this = morph
FACE_SHARP = 60.0                 # Laplacian variance of the 96 px face crop; below = motion blur, not judged
# DINOv2 CLS cosine between two crops of one prop. Calibrated on AURUM: v1 (tumbler -> flute -> can ->
# iced tumbler) pairs 0.16-0.54, mean 0.34; v3 (one glass, hands/fill level vary) pairs 0.50-0.78, mean 0.69.
OBJ_PAIR_FAIL = 0.45
OBJ_PAIR_WARN = 0.60
OBJ_MEAN_FAIL = 0.50
REF_PRESENT = 0.35                # best window vs a packshot reference: the product is in frame (heist can: 0.36-0.50)
FRAME_JUMP = 0.55                 # DINOv2 sim between consecutive samples inside one shot (2 fps)
SEAM_WARN = 0.70                  # sim across a seam of a seamless one-take


def parse_kv(items: list[str] | None) -> list[tuple[str, str]]:
    out = []
    for it in items or []:
        k, _, v = it.partition("=")
        if not v:
            raise SystemExit(f"bad argument {it!r}: expected NAME=VALUE")
        out.append((k.strip(), v.strip()))
    return out


def read_rgb(path: str) -> np.ndarray:
    im = cv2.imread(path, cv2.IMREAD_COLOR)
    if im is None:
        raise SystemExit(f"cannot read {path}")
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)


def grab_frame(video: str, t: float, width: int) -> np.ndarray:
    fr, _ = q.read_frames(video, width=width, start=max(0.0, t), duration=0.05)
    if not len(fr):
        fr, _ = q.read_frames(video, width=width, start=max(0.0, t - 0.1), duration=0.15)
    return fr[0]


def shot_of(t: float, shots: list[dict]) -> int:
    for s in shots:
        if s["start"] <= t < s["end"]:
            return s["index"]
    return shots[-1]["index"] if shots else 0


# ----------------------------------------------------------------------------- faces

def face_analysis(samples, times, shots, fm: q.FaceModel, refs: dict[str, np.ndarray], scale: float):
    dets = []
    for k, (f, t) in enumerate(zip(samples, times)):
        bgr = cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
        for d in fm.detect(bgr):
            if d["box"][2] < 28 or d["score"] < 0.7:
                continue
            e = fm.embed(bgr, d)
            if e is None:
                continue
            x, y, w, h = [int(v) for v in d["box"]]
            crop = f[max(0, y):y + h, max(0, x):x + w]
            if crop.size == 0:
                continue
            c96 = cv2.resize(crop, (96, 96))
            sharp = float(cv2.Laplacian(cv2.cvtColor(c96, cv2.COLOR_RGB2GRAY), cv2.CV_64F).var())
            dets.append({"k": k, "t": float(t), "shot": shot_of(t, shots), "box": [v / scale for v in d["box"]],
                         "score": d["score"], "emb": e, "crop": c96, "sharp": sharp, "usable": sharp >= FACE_SHARP})
    # tracks: link detections in consecutive samples of the same shot by box proximity
    tracks: list[list[dict]] = []
    for d in dets:
        best, bd = None, 1e9
        for tr in tracks:
            last = tr[-1]
            if last["shot"] != d["shot"] or d["k"] - last["k"] != 1:
                continue
            cx1, cy1 = last["box"][0] + last["box"][2] / 2, last["box"][1] + last["box"][3] / 2
            cx2, cy2 = d["box"][0] + d["box"][2] / 2, d["box"][1] + d["box"][3] / 2
            dist = np.hypot(cx1 - cx2, cy1 - cy2) / max(last["box"][2], d["box"][2])
            if dist < 1.2 and dist < bd:
                best, bd = tr, dist
        if best is not None:
            best.append(d)
        else:
            tracks.append([d])
    track_rows = []
    for i, tr in enumerate(tracks):
        for d in tr:
            d["track"] = i
        good = [d for d in tr if d["usable"]] or tr
        anchor = np.mean([d["emb"] for d in good[:2]], axis=0)
        anchor /= np.linalg.norm(anchor) + 1e-9
        sims = [float(d["emb"] @ anchor) for d in good]
        # drift = at least two sharp samples in a row below the threshold (one blurred or profile frame is not a morph)
        low = [good[j]["t"] for j in range(1, len(good)) if sims[j] < FACE_DRIFT and sims[j - 1] < FACE_DRIFT]
        track_rows.append({"track": i, "shot": tr[0]["shot"], "start": tr[0]["t"], "end": tr[-1]["t"], "n": len(tr),
                           "min_sim_to_start": min(sims), "drift_times": low})
    # identities: greedy average-link clustering
    clusters: list[list[dict]] = []
    for d in sorted([d for d in dets if d["usable"]], key=lambda d: -d["score"]):
        best, bs = None, FACE_SAME
        for c in clusters:
            cen = np.mean([x["emb"] for x in c], axis=0)
            s = float(d["emb"] @ (cen / (np.linalg.norm(cen) + 1e-9)))
            if s > bs:
                best, bs = c, s
        if best is not None:
            best.append(d)
        else:
            clusters.append([d])
    min_n = 3 if len(dets) >= 12 else 1
    clusters = [c for c in clusters if len(c) >= min_n]  # drop one-off false detections (headlights, hands)
    for i, c in enumerate(sorted(clusters, key=lambda c: -len(c))):
        for d in c:
            d["identity"] = i
    ident_rows = []
    for i, c in enumerate(sorted(clusters, key=lambda c: -len(c))):
        ident_rows.append({"identity": i, "n": len(c), "shots": sorted({d["shot"] for d in c}),
                           "times": [round(d["t"], 2) for d in sorted(c, key=lambda d: d["t"])]})
    ref_rows = []
    if refs:
        for d in [d for d in dets if d["usable"]]:
            sims = {n: float(d["emb"] @ e) for n, e in refs.items()}
            n_best = max(sims, key=sims.get)
            d["ref"] = n_best if sims[n_best] >= FACE_SAME else None
            ref_rows.append({"t": d["t"], "shot": d["shot"], "best_ref": n_best, "sim": sims[n_best],
                             "match": sims[n_best] >= FACE_SAME, **{f"sim_{n}": round(s, 3) for n, s in sims.items()}})
    return dets, track_rows, ident_rows, ref_rows


def face_refs(items, fm: q.FaceModel) -> dict[str, np.ndarray]:
    refs = {}
    for name, path in items:
        rgb = read_rgb(path)
        h, w = rgb.shape[:2]
        if w > 1280:
            rgb = cv2.resize(rgb, (1280, int(h * 1280 / w)))
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        faces = fm.detect(bgr)
        if not faces:
            print(f"[qc] no face found in reference {path}", file=sys.stderr)
            continue
        d = max(faces, key=lambda d: d["box"][2] * d["box"][3])
        e = fm.embed(bgr, d)
        if e is not None:
            refs[name] = e
    return refs


# ----------------------------------------------------------------------------- objects

def object_analysis(video: str, items, emb: q.Embedder, info: dict, width: int):
    scale = width / info["width"]
    by_name: dict[str, list[dict]] = {}
    for name, spec in items:
        t, _, box = spec.partition(":")
        x, y, w, h = [float(v) for v in box.split(",")]
        f = grab_frame(video, float(t), width)
        x0, y0 = int(x * scale), int(y * scale)
        crop = f[max(0, y0):y0 + int(h * scale), max(0, x0):x0 + int(w * scale)]
        by_name.setdefault(name, []).append({"t": float(t), "box": [x, y, w, h], "crop": crop})
    rows = []
    for name, lst in by_name.items():
        E = emb([c["crop"] for c in lst])
        H = [q.phash(c["crop"]) for c in lst]
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                a, b = lst[i], lst[j]
                sim = float(E[i] @ E[j])
                ar = (a["box"][3] / a["box"][2]) / (b["box"][3] / b["box"][2])
                lvl = "FAIL" if sim < OBJ_PAIR_FAIL else "WARN" if sim < OBJ_PAIR_WARN else "PASS"
                rows.append({"object": name, "t1": a["t"], "t2": b["t"], "dino_sim": sim,
                             "phash_dist": q.hamming(H[i], H[j]), "hist_dist": q.hs_hist_distance(a["crop"], b["crop"]),
                             "aspect_ratio_change": float(max(ar, 1 / ar)), "level": lvl})
    summary = []
    for name in by_name:
        sims = [r["dino_sim"] for r in rows if r["object"] == name]
        if not sims:
            continue
        mean = float(np.mean(sims))
        n_fail = sum(s < OBJ_PAIR_FAIL for s in sims)
        lvl = "FAIL" if mean < OBJ_MEAN_FAIL or n_fail >= 2 else "WARN" if n_fail or min(sims) < OBJ_PAIR_WARN else "PASS"
        summary.append({"object": name, "pairs": len(sims), "mean_sim": mean, "min_sim": float(min(sims)), "level": lvl})
    return by_name, rows, summary


def ref_object_search(samples, times, shots, name: str, ref_rgb: np.ndarray, emb: q.Embedder):
    """Multi-scale window search: best DINOv2 match to the reference in every sampled frame."""
    rh, rw = ref_rgb.shape[:2]
    aspect = rw / rh
    e_ref = emb([ref_rgb])[0]
    rows, crops = [], []
    for f, t in zip(samples, times):
        H, W = f.shape[:2]
        wins, boxes = [], []
        for frac in (0.2, 0.32, 0.5):
            h = int(H * frac)
            w = int(min(W * 0.95, h * aspect))
            if w < 24 or h < 24:
                continue
            sy, sx = max(8, h // 2), max(8, w // 2)
            for y in range(0, H - h + 1, sy):
                for x in range(0, W - w + 1, sx):
                    wins.append(f[y:y + h, x:x + w])
                    boxes.append((x, y, w, h))
        E = emb(wins)
        sims = E @ e_ref
        i = int(np.argmax(sims))
        x, y, w, h = boxes[i]
        rows.append({"t": float(t), "shot": shot_of(t, shots), "best_sim": float(sims[i]), "box": [x, y, w, h]})
        crops.append(cv2.resize(f[y:y + h, x:x + w], (96, int(96 / aspect)) if aspect < 1 else (int(96 * aspect), 96)))
    return rows, crops


# ----------------------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--out")
    ap.add_argument("--fps", type=float, default=2.0, help="sampling rate for faces / drift (default 2)")
    ap.add_argument("--width", type=int, default=720)
    ap.add_argument("--ref-face", action="append", help="NAME=image (repeat)")
    ap.add_argument("--cast", type=int, help="expected number of distinct faces")
    ap.add_argument("--object", action="append", help="NAME=T:x,y,w,h in source pixels (repeat per time)")
    ap.add_argument("--ref-object", action="append", help="NAME=image: search every sample for it (repeat)")
    ap.add_argument("--ref-fps", type=float, default=1.0, help="sampling rate for --ref-object search")
    ap.add_argument("--seamless", action="store_true", help="the edit is meant to read as one take: check seams")
    ap.add_argument("--seams", help="comma-separated seam times (s) when the edit has no hard cuts")
    ap.add_argument("--no-faces", action="store_true")
    a = ap.parse_args(argv)

    info = q.probe(a.video)
    out = Path(a.out) if a.out else q.default_out(a.video, "continuity")
    out.mkdir(parents=True, exist_ok=True)
    lo, lo_t = q.read_frames(a.video, width=160)
    cuts, _ = q.detect_cuts(lo, lo_t, info["fps"])
    shots = q.shots_from_cuts(cuts, info["duration"])
    width = min(a.width, info["width"])
    scale = width / info["width"]
    samples, times = q.read_frames(a.video, width=width, fps=a.fps)
    emb = q.Embedder()
    checks, report = [], {"video": a.video, "embedder": emb.backend, "shots": shots, "cuts": cuts}

    # 2. drift / seams
    E = emb(list(samples))
    sim_prev = np.r_[1.0, np.sum(E[1:] * E[:-1], axis=1)]
    jumps = []
    for k in range(1, len(times)):
        same_shot = shot_of(times[k], shots) == shot_of(times[k - 1], shots)
        if same_shot and sim_prev[k] < FRAME_JUMP:
            jumps.append({"t": float(times[k]), "sim_prev": float(sim_prev[k])})
    report["frame_sim_prev"] = [{"t": float(t), "sim": float(s)} for t, s in zip(times, sim_prev)]
    report["jumps"] = jumps
    checks.append({"level": "WARN" if jumps else "PASS", "check": "in-shot jumps (morph/teleport)",
                   "detail": ", ".join(f'{j["t"]:.1f}s ({j["sim_prev"]:.2f})' for j in jumps) or
                             f"none below {FRAME_JUMP} (DINOv2 sim between samples {1 / a.fps:.1f} s apart)"})
    seam_t = [c["t"] for c in cuts] + ([float(x) for x in a.seams.split(",")] if a.seams else [])
    seam_rows, seam_imgs, seam_lab = [], [], []
    if a.seamless or a.seams:
        for st in sorted(seam_t):
            f1 = grab_frame(a.video, max(0, st - 1.5 / info["fps"]), 360)
            f2 = grab_frame(a.video, st + 0.5 / info["fps"], 360)
            e = emb([f1, f2])
            s = float(e[0] @ e[1])
            seam_rows.append({"t": st, "sim": s, "level": "PASS" if s >= SEAM_WARN else "WARN" if s >= FRAME_JUMP else "FAIL"})
            seam_imgs += [cv2.resize(f1, (160, int(160 * f1.shape[0] / f1.shape[1]))),
                          cv2.resize(f2, (160, int(160 * f2.shape[0] / f2.shape[1])))]
            seam_lab += [f"{st:.2f}- ", f"{st:.2f}+ {s:.2f}"]
        if seam_imgs:
            q.save_jpg(out / "seams.jpg", q.tile(seam_imgs, seam_lab, cols=8))
        bad = [r for r in seam_rows if r["level"] != "PASS"]
        checks.append({"level": q.verdict_of(bad) if bad else "PASS", "check": "seams",
                       "detail": ", ".join(f'{r["t"]:.2f}s sim {r["sim"]:.2f}' for r in bad) or f"{len(seam_rows)} seams match"})
    report["seams"] = seam_rows

    # 3. faces
    if not a.no_faces:
        fm = q.FaceModel(want_embed=True)
        if fm.rec is None:
            checks.append({"level": "INFO", "check": "faces", "detail": "SFace model unavailable: face identity skipped"})
        else:
            refs = face_refs(parse_kv(a.ref_face), fm)
            dets, tracks, idents, ref_rows = face_analysis(samples, times, shots, fm, refs, scale)
            report.update({"face_tracks": tracks, "identities": idents, "face_vs_refs": ref_rows,
                           "faces_detected": len(dets)})
            drift = [t for t in tracks if t["drift_times"] and t["n"] >= 3]
            checks.append({"level": "FAIL" if drift else "PASS", "check": "identity drift inside a shot",
                           "detail": "; ".join(f'track {t["track"]} {t["start"]:.1f}-{t["end"]:.1f}s min sim '
                                               f'{t["min_sim_to_start"]:.2f}' for t in drift) or
                                     f"{len(tracks)} face tracks stable (sim to start >= {FACE_DRIFT})"})
            if a.cast is not None:
                n_id = len(idents)
                checks.append({"level": "PASS" if n_id <= a.cast else "WARN", "check": "cast count",
                               "detail": f"{n_id} distinct faces clustered (expected {a.cast}): " +
                                         "; ".join(f'id{i["identity"]} x{i["n"]} shots {i["shots"]}' for i in idents)})
            if refs:
                unmatched = [r for r in ref_rows if not r["match"]]
                frac = len(unmatched) / max(1, len(ref_rows))
                checks.append({"level": "FAIL" if frac > 0.3 else "WARN" if unmatched else "PASS",
                               "check": "faces vs references",
                               "detail": f"{len(ref_rows) - len(unmatched)}/{len(ref_rows)} face samples match a reference "
                                         f"(>= {FACE_SAME}); unmatched at " +
                                         ", ".join(f'{r["t"]:.1f}s(best {r["best_ref"]} {r["sim"]:.2f})' for r in unmatched[:12])})
            # face sheet: one row per identity
            imgs, labs, bords = [], [], []
            palette = [(230, 60, 60), (60, 160, 230), (60, 200, 90), (230, 170, 40), (170, 80, 220), (120, 120, 120)]
            for d in sorted(dets, key=lambda d: (d.get("identity", 99), d["t"])):
                imgs.append(d["crop"])
                labs.append(f'{d["t"]:.1f} id{d.get("identity", "-")}' + (f' {d["ref"]}' if d.get("ref") else "")
                            + ("" if d["usable"] else " blur"))
                bords.append(palette[d.get("identity", 5) % len(palette)] if "identity" in d else None)
            if imgs:
                q.save_jpg(out / "faces.jpg", q.tile(imgs, labs, cols=12, border=bords, label_scale=0.33))

    # 4. named objects
    if a.object:
        by_name, rows, summary = object_analysis(a.video, parse_kv(a.object), emb, info, min(1080, info["width"]))
        report["objects"] = rows
        report["objects_summary"] = summary
        for sm in summary:
            bad = [r for r in rows if r["object"] == sm["object"] and r["level"] != "PASS"]
            checks.append({"level": sm["level"], "check": f"object '{sm['object']}' consistency",
                           "detail": f"mean pair sim {sm['mean_sim']:.2f} (min {sm['min_sim']:.2f}) over {sm['pairs']} pairs; "
                                     + ("; ".join(f'{r["t1"]:.1f}s vs {r["t2"]:.1f}s {r["dino_sim"]:.2f}' for r in bad)
                                        or "all pairs consistent")})
        imgs, labs = [], []
        for name, lst in by_name.items():
            for c in lst:
                imgs.append(cv2.resize(c["crop"], (120, 200)))
                labs.append(f'{name} {c["t"]:.1f}s')
        q.save_jpg(out / "objects.jpg", q.tile(imgs, labs, cols=min(10, len(imgs))))

    # 5. reference objects
    report["ref_objects"] = {}
    if a.ref_object:
        rs, rt = q.read_frames(a.video, width=min(480, info["width"]), fps=a.ref_fps)
        for name, path in parse_kv(a.ref_object):
            ref = read_rgb(path)
            rows, crops = ref_object_search(rs, rt, shots, name, ref, emb)
            report["ref_objects"][name] = rows
            seen = [r for r in rows if r["best_sim"] >= REF_PRESENT]
            checks.append({"level": "PASS" if seen else "WARN", "check": f"product '{name}' vs reference",
                           "detail": (f"found (sim >= {REF_PRESENT}) at " + ", ".join(f'{r["t"]:.0f}s {r["best_sim"]:.2f}' for r in seen)
                                      if seen else f"never matched the reference above {REF_PRESENT}")
                                     + f". Max {max(r['best_sim'] for r in rows):.2f}. Compare the crops in ref_{name}.jpg: "
                                       "a visible product that scores low has drifted (label/shape/colour)."})
            h = 150
            refc = cv2.resize(ref, (int(h * ref.shape[1] / ref.shape[0]), h))
            tiles = [cv2.resize(c, (refc.shape[1], h)) for c in crops]
            q.save_jpg(out / f"ref_{name}.jpg", q.tile([refc] + tiles, ["REF"] + [f'{r["t"]:.0f}s {r["best_sim"]:.2f}' for r in rows],
                                                     cols=12))

    verdict = q.verdict_of(checks)
    report["checks"] = checks
    report["verdict"] = verdict
    (out / "continuity.json").write_text(json.dumps(q.to_jsonable(report), indent=1), encoding="utf-8")
    md = [f"# Continuity: {Path(a.video).name}", "", f"**Verdict: {verdict}** (embedder: {emb.backend})", "",
          q.md_table([[c["level"], c["check"], c["detail"]] for c in checks], ["Level", "Check", "Detail"])]
    if report.get("objects"):
        md += ["", "## Named objects", q.md_table(
            [[r["object"], f'{r["t1"]:.2f}', f'{r["t2"]:.2f}', f'{r["dino_sim"]:.2f}', r["phash_dist"],
              f'{r["hist_dist"]:.2f}', f'{r["aspect_ratio_change"]:.2f}', r["level"]] for r in report["objects"]],
            ["object", "t1", "t2", "DINO sim", "pHash dist", "hist dist", "aspect x", "level"]), "", "![objects](objects.jpg)"]
    if report.get("face_tracks"):
        md += ["", "## Face tracks", q.md_table(
            [[t["track"], t["shot"], f'{t["start"]:.1f}-{t["end"]:.1f}', t["n"], f'{t["min_sim_to_start"]:.2f}']
             for t in report["face_tracks"]], ["track", "shot", "span s", "samples", "min sim to start"]),
               "", "## Identities", q.md_table([[i["identity"], i["n"], i["shots"], i["times"][:12]] for i in report["identities"]],
                                               ["id", "samples", "shots", "times"]), "", "![faces](faces.jpg)"]
    if seam_rows:
        md += ["", "## Seams", q.md_table([[f'{r["t"]:.2f}', f'{r["sim"]:.2f}', r["level"]] for r in seam_rows],
                                          ["t", "DINO sim across", "level"]), "", "![seams](seams.jpg)"]
    for name in report["ref_objects"]:
        md += ["", f"## Product '{name}' vs reference", f"![ref](ref_{name}.jpg)"]
    (out / "continuity.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{verdict}  {a.video}  (embedder {emb.backend})")
    for c in checks:
        print(f"  {c['level']:4s} {c['check']}: {c['detail']}")
    print(f"  -> {out / 'continuity.md'}")
    return {"PASS": 0, "WARN": 1, "FAIL": 2}[verdict]


if __name__ == "__main__":
    sys.exit(main())
