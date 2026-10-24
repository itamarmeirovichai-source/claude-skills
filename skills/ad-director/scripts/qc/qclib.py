"""Shared helpers for the ad-director QC tools (qc_report, lipsync_check, continuity_check).

Pure measurement code: ffmpeg/ffprobe for decoding, numpy/scipy/OpenCV for analysis.
Nothing here calls a paid API. Optional ONNX models (YuNet face detector, SFace face
embedding, DINOv2-small image embedding) are downloaded once into ~/.cache/ad-director-qc
(override with AD_QC_MODELS) and every caller degrades gracefully when they are missing.
"""
from __future__ import annotations

import base64
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

try:
    import cv2  # opencv-python-headless
except ImportError:  # pragma: no cover
    sys.exit("qc tools need OpenCV: pip install -r skills/ad-director/scripts/qc/requirements.txt")

from scipy import signal as sps

# ----------------------------------------------------------------------------- probing / decoding


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def probe(path: str) -> dict:
    out = run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path]).stdout
    info = json.loads(out)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    if v is None:
        raise SystemExit(f"{path}: no video stream")
    num, den = (v.get("avg_frame_rate") or v.get("r_frame_rate") or "24/1").split("/")
    fps = float(num) / float(den) if float(den) else 24.0
    if not (1 < fps < 241):
        num, den = v.get("r_frame_rate", "24/1").split("/")
        fps = float(num) / float(den)
    dur = float(info["format"].get("duration") or v.get("duration") or 0)
    return {"path": path, "width": int(v["width"]), "height": int(v["height"]), "fps": fps,
            "duration": dur, "has_audio": a is not None,
            "audio_rate": int(a["sample_rate"]) if a else None,
            "audio_channels": int(a.get("channels", 0)) if a else 0,
            "vcodec": v.get("codec_name"), "acodec": a.get("codec_name") if a else None}


def read_frames(path: str, width: int = 160, fps: float | None = None, gray: bool = False,
                start: float | None = None, duration: float | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Decode frames scaled to `width` (height keeps aspect, even). Returns (frames, times)."""
    info = probe(path)
    h = int(round(info["height"] * width / info["width"] / 2) * 2)
    vf = []
    if fps:
        vf.append(f"fps={fps}")
    vf.append(f"scale={width}:{h}:flags=area")
    cmd = ["ffmpeg", "-v", "error"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}"]
    cmd += ["-i", path]
    if duration is not None:
        cmd += ["-t", f"{duration:.3f}"]
    pix = "gray" if gray else "rgb24"
    cmd += ["-vf", ",".join(vf), "-f", "rawvideo", "-pix_fmt", pix, "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    ch = 1 if gray else 3
    n = len(raw) // (width * h * ch)
    frames = np.frombuffer(raw[: n * width * h * ch], np.uint8).reshape(n, h, width, *(() if gray else (3,)))
    rate = fps or info["fps"]
    times = (start or 0.0) + np.arange(n) / rate
    return frames, times


def read_audio(path: str, sr: int = 16000, mono: bool = True) -> np.ndarray | None:
    """Decode the first audio stream to float32 in [-1, 1]. None when there is no audio."""
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-map", "0:a:0", "-ac", "1" if mono else "2",
           "-ar", str(sr), "-f", "f32le", "-"]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0 or not p.stdout:
        return None
    x = np.frombuffer(p.stdout, np.float32)
    return x if mono else x.reshape(-1, 2)


# ----------------------------------------------------------------------------- loudness


def loudness(path: str) -> dict | None:
    """EBU R128 integrated loudness, LRA, true peak and max short-term loudness via ffmpeg ebur128."""
    p = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-map", "0:a:0", "-af", "ebur128=peak=true:framelog=verbose",
                        "-f", "null", "-"], capture_output=True, text=True)
    err = p.stderr
    if "Summary:" not in err:
        return None
    summ = err[err.rindex("Summary:"):]
    def grab(label):
        m = re.search(label + r"\s*(-?[\d.]+|-inf)", summ)
        return None if not m or m.group(1) == "-inf" else float(m.group(1))
    st = [float(m) for m in re.findall(r"S:\s*(-?[\d.]+)", err[: err.rindex("Summary:")])]
    return {"integrated_lufs": grab("I:"), "lra_lu": grab("LRA:"), "true_peak_dbtp": grab("Peak:"),
            "max_short_term_lufs": max(st) if st else None}


# ----------------------------------------------------------------------------- audio features


def rms_envelope(x: np.ndarray, sr: int, hop_s: float = 0.01, win_s: float = 0.03) -> tuple[np.ndarray, np.ndarray]:
    hop, win = int(sr * hop_s), int(sr * win_s)
    if len(x) < win:
        return np.zeros(0), np.zeros(0)
    n = 1 + (len(x) - win) // hop
    idx = np.arange(win)[None, :] + hop * np.arange(n)[:, None]
    rms = np.sqrt(np.mean(x[idx] ** 2, axis=1) + 1e-12)
    t = (np.arange(n) * hop + win / 2) / sr
    return t, 20 * np.log10(rms + 1e-9)


def onset_strength(x: np.ndarray, sr: int, hop: int = 256, n_fft: int = 1024) -> tuple[np.ndarray, np.ndarray]:
    """Log-magnitude spectral flux (half-wave rectified), the standard onset novelty curve."""
    if len(x) < n_fft:
        return np.zeros(0), np.zeros(0)
    f, t, Z = sps.stft(x, fs=sr, nperseg=n_fft, noverlap=n_fft - hop, boundary=None, padded=False)
    S = np.log1p(100 * np.abs(Z))
    # weight 60 Hz - 8 kHz, which is where impacts, steps and clinks live
    band = (f >= 60) & (f <= 8000)
    flux = np.maximum(0, np.diff(S[band], axis=1)).sum(axis=0)
    flux = np.concatenate([[0], flux])
    return t, flux


def detect_onsets(x: np.ndarray, sr: int, min_gap: float = 0.08, sensitivity: float = 1.0) -> list[dict]:
    t, flux = onset_strength(x, sr)
    if len(flux) < 5:
        return []
    dt = t[1] - t[0]
    # adaptive threshold: local mean (+-0.15 s) plus a global floor from median/MAD
    w = max(3, int(0.15 / dt))
    local = np.convolve(flux, np.ones(2 * w + 1) / (2 * w + 1), mode="same")
    med = np.median(flux)
    mad = np.median(np.abs(flux - med)) + 1e-9
    floor = med + 4.0 * mad / sensitivity
    peaks, props = sps.find_peaks(flux, distance=max(1, int(min_gap / dt)))
    out = []
    peak_max = flux.max() + 1e-9
    for p in peaks:
        if flux[p] > floor and flux[p] > local[p] * (1 + 0.5 / sensitivity):
            # backtrack to the rise start (where flux first exceeds 30 % of the peak)
            q = p
            while q > 0 and flux[q - 1] > 0.3 * flux[p] and p - q < int(0.05 / dt):
                q -= 1
            out.append({"t": float(t[q]), "strength": float(flux[p] / peak_max)})
    return out


# ----------------------------------------------------------------------------- video features


def hsv_content_delta(frames_rgb: np.ndarray) -> np.ndarray:
    """PySceneDetect-style content value: mean |dH|+|dS|+|dV| / 3 between consecutive frames (0-255)."""
    hsv = np.stack([cv2.cvtColor(f, cv2.COLOR_RGB2HSV_FULL) for f in frames_rgb]).astype(np.int16)
    d = np.abs(np.diff(hsv, axis=0))
    d[..., 0] = np.minimum(d[..., 0], 256 - d[..., 0])  # hue is circular
    cv = d.reshape(len(d), -1, 3).mean(axis=1).mean(axis=1)
    return np.concatenate([[0.0], cv])


def luma(frames_rgb: np.ndarray) -> np.ndarray:
    return (0.299 * frames_rgb[..., 0] + 0.587 * frames_rgb[..., 1] + 0.114 * frames_rgb[..., 2]).astype(np.float32)


def detect_cuts(frames_rgb: np.ndarray, times: np.ndarray, fps: float, threshold: float = 22.0,
                ratio: float = 2.5, min_shot: float = 0.35) -> tuple[list[dict], np.ndarray]:
    """Hard-cut detection: content value above an absolute floor AND `ratio` x the local average
    (adaptive, so whip pans and fast motion do not fire). Single-frame flashes are excluded."""
    cv = hsv_content_delta(frames_rgb)
    n = len(cv)
    Y = luma(frames_rgb)
    cuts = []
    last = -1e9
    for i in range(1, n):
        lo, hi = max(1, i - 3), min(n, i + 4)
        neigh = np.concatenate([cv[lo:i], cv[i + 1:hi]])
        base = neigh.mean() if len(neigh) else 0.0
        if cv[i] < threshold or cv[i] < ratio * max(base, 1.0):
            continue
        # flash guard: frame i differs from both neighbours while i-1 ~ i+1
        if 1 <= i < n - 1:
            d_prev_next = np.abs(Y[i + 1] - Y[i - 1]).mean()
            d_i_prev = np.abs(Y[i] - Y[i - 1]).mean()
            if d_prev_next < 0.35 * d_i_prev:
                continue
        if times[i] - last < min_shot:
            continue
        cuts.append({"t": float(times[i]), "frame": int(i), "score": float(cv[i])})
        last = times[i]
    return cuts, cv


def shots_from_cuts(cuts: list[dict], duration: float) -> list[dict]:
    edges = [0.0] + [c["t"] for c in cuts] + [duration]
    return [{"index": k, "start": edges[k], "end": edges[k + 1], "length": edges[k + 1] - edges[k]}
            for k in range(len(edges) - 1)]


def motion_energy(frames_rgb: np.ndarray, cut_frames: set[int]) -> dict:
    """Dense optical flow (Farneback) per frame. Returns global (camera) and local (subject) motion,
    in pixels/frame at the analysis width. Cut frames are interpolated over."""
    g = [cv2.cvtColor(f, cv2.COLOR_RGB2GRAY) for f in frames_rgb]
    n = len(g)
    glob = np.zeros(n, np.float32)
    loc = np.zeros(n, np.float32)
    for i in range(1, n):
        if i in cut_frames:
            glob[i] = np.nan
            loc[i] = np.nan
            continue
        flow = cv2.calcOpticalFlowFarneback(g[i - 1], g[i], None, 0.5, 3, 13, 3, 5, 1.1, 0)
        med = np.median(flow.reshape(-1, 2), axis=0)
        glob[i] = float(np.hypot(*med))
        resid = flow - med
        mag = np.hypot(resid[..., 0], resid[..., 1])
        loc[i] = float(np.mean(mag))
    for arr in (glob, loc):
        bad = np.isnan(arr)
        if bad.any() and (~bad).any():
            arr[bad] = np.interp(np.flatnonzero(bad), np.flatnonzero(~bad), arr[~bad])
        arr[0] = arr[1] if n > 1 else 0
    return {"global": glob, "local": loc}


def visual_events(times: np.ndarray, local: np.ndarray, fps: float, cuts: list[dict]) -> list[dict]:
    """Candidate on-screen events: motion peaks, abrupt stops (contact/impact) and abrupt starts,
    plus hard cuts. Times are frame times (s)."""
    if len(local) < 5:
        return []
    m = sps.medfilt(local, 3)
    sd = float(np.std(m)) + 1e-6
    dist = max(1, int(0.2 * fps))
    ev = []
    pk, _ = sps.find_peaks(m, prominence=0.6 * sd, distance=dist)
    ev += [{"t": float(times[p]), "kind": "motion_peak", "value": float(m[p])} for p in pk]
    dm = np.diff(m, prepend=m[0])
    sdd = float(np.std(dm)) + 1e-6
    st, _ = sps.find_peaks(-dm, height=1.5 * sdd, distance=dist)
    ev += [{"t": float(times[p]), "kind": "stop/impact", "value": float(-dm[p])} for p in st]
    go, _ = sps.find_peaks(dm, height=1.5 * sdd, distance=dist)
    ev += [{"t": float(times[p]), "kind": "start", "value": float(dm[p])} for p in go]
    ev += [{"t": c["t"], "kind": "cut", "value": c["score"]} for c in cuts]
    return sorted(ev, key=lambda e: e["t"])


def flash_frames(frames_rgb: np.ndarray, times: np.ndarray) -> list[dict]:
    Y = luma(frames_rgb)
    mean = Y.reshape(len(Y), -1).mean(axis=1)
    sd = Y.reshape(len(Y), -1).std(axis=1)
    out = []
    for i in range(len(Y)):
        kind = None
        if mean[i] < 14 and sd[i] < 10:
            kind = "black"
        elif mean[i] > 236 and sd[i] < 14:
            kind = "white"
        elif 0 < i < len(Y) - 1:
            dpn = np.abs(Y[i + 1] - Y[i - 1]).mean()
            dip = np.abs(Y[i] - Y[i - 1]).mean()
            din = np.abs(Y[i] - Y[i + 1]).mean()
            if dip > 25 and din > 25 and dpn < 0.35 * min(dip, din):
                kind = "single-frame glitch"
        if kind:
            out.append({"t": float(times[i]), "frame": i, "kind": kind, "luma": float(mean[i])})
    return merge_runs(out, 1.5 / max(1e-6, (times[1] - times[0]) if len(times) > 1 else 1 / 24))


def merge_runs(items: list[dict], max_gap_frames: float) -> list[dict]:
    runs: list[dict] = []
    for it in items:
        if runs and runs[-1]["kind"] == it["kind"] and it["frame"] - runs[-1]["end_frame"] <= max_gap_frames:
            runs[-1]["end"] = it["t"]
            runs[-1]["end_frame"] = it["frame"]
            runs[-1]["frames"] += 1
        else:
            runs.append({"start": it["t"], "end": it["t"], "start_frame": it["frame"], "end_frame": it["frame"],
                         "frames": 1, "kind": it["kind"]})
    return runs


def frozen_runs(frames_rgb: np.ndarray, times: np.ndarray, fps: float, eps: float = 0.6,
                min_frames: int = 6) -> tuple[list[dict], int]:
    """Runs of (near-)identical consecutive frames. Also returns the count of single duplicates
    (a sign of frame-rate conversion or a stalled generator)."""
    Y = luma(frames_rgb)
    d = np.abs(np.diff(Y, axis=0)).reshape(len(Y) - 1, -1).mean(axis=1) if len(Y) > 1 else np.zeros(0)
    still = d < eps
    runs, dups = [], 0
    i = 0
    while i < len(still):
        if still[i]:
            j = i
            while j < len(still) and still[j]:
                j += 1
            length = j - i + 1  # frames in the run
            if length >= min_frames:
                runs.append({"start": float(times[i]), "end": float(times[j]), "frames": int(length),
                             "seconds": float(length / fps)})
            else:
                dups += j - i
            i = j
        else:
            i += 1
    return runs, dups


def luma_flicker(frames_rgb: np.ndarray, times: np.ndarray, shots: list[dict]) -> list[dict]:
    """Per shot: std of the frame-mean luma after removing slow trends (5-frame median). AI clips
    'breathe' in exposure; > ~1.5 levels (0-255) is usually visible on a phone."""
    Y = luma(frames_rgb).reshape(len(frames_rgb), -1).mean(axis=1)
    out = []
    for s in shots:
        idx = np.flatnonzero((times >= s["start"]) & (times < s["end"]))
        if len(idx) < 7:
            continue
        y = Y[idx[1:-1]]  # skip frames adjacent to cuts
        trend = sps.medfilt(y, 5)
        res = (y - trend)[2:-2]
        out.append({"shot": s["index"], "start": s["start"], "end": s["end"],
                    "flicker": float(np.std(res)), "max_jump": float(np.max(np.abs(res))) if len(res) else 0.0})
    return out


# ----------------------------------------------------------------------------- optional ONNX models

MODEL_DIR = Path(os.environ.get("AD_QC_MODELS", Path.home() / ".cache" / "ad-director-qc"))
MODEL_URLS = {
    "yunet.onnx": "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/"
                  "face_detection_yunet/face_detection_yunet_2023mar.onnx",
    "sface.onnx": "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/"
                  "face_recognition_sface/face_recognition_sface_2021dec.onnx",
    "dinov2s.onnx": "https://huggingface.co/Xenova/dinov2-small/resolve/main/onnx/model_quantized.onnx",
}


def model_path(name: str, download: bool = True) -> Path | None:
    p = MODEL_DIR / name
    if p.exists() and p.stat().st_size > 10000:
        return p
    if not download or os.environ.get("AD_QC_OFFLINE"):
        return None
    try:
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".part")
        print(f"[qc] downloading {name} (one-time) ...", file=sys.stderr)
        urllib.request.urlretrieve(MODEL_URLS[name], tmp)
        if tmp.stat().st_size < 10000:  # an LFS pointer or an error page
            tmp.unlink()
            return None
        tmp.rename(p)
        return p
    except Exception as e:  # pragma: no cover - network dependent
        print(f"[qc] could not download {name}: {e}", file=sys.stderr)
        return None


class FaceModel:
    """YuNet detector (+ SFace embeddings when available). Falls back to a Haar cascade."""

    def __init__(self, want_embed: bool = True, score: float = 0.6):
        self.det = None
        self.rec = None
        p = model_path("yunet.onnx")
        if p:
            self.det = cv2.FaceDetectorYN.create(str(p), "", (320, 320), score, 0.3, 50)
        else:
            self.haar = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml"))
        if want_embed:
            q = model_path("sface.onnx")
            if q:
                self.rec = cv2.FaceRecognizerSF.create(str(q), "")
        self.backend = "yunet" if self.det is not None else "haar"

    def detect(self, bgr: np.ndarray) -> list[dict]:
        """Faces as dicts: box (x,y,w,h), score, landmarks (5x2: r-eye, l-eye, nose, r-mouth, l-mouth) or None."""
        h, w = bgr.shape[:2]
        if self.det is not None:
            self.det.setInputSize((w, h))
            _, faces = self.det.detect(bgr)
            if faces is None:
                return []
            return [{"box": f[:4].astype(float).tolist(), "score": float(f[14]),
                     "lm": f[4:14].reshape(5, 2).astype(float), "raw": f} for f in faces]
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        rects = self.haar.detectMultiScale(gray, 1.1, 5, minSize=(40, 40))
        return [{"box": [float(x), float(y), float(a), float(b)], "score": 1.0, "lm": None, "raw": None}
                for (x, y, a, b) in rects]

    def embed(self, bgr: np.ndarray, face: dict) -> np.ndarray | None:
        if self.rec is None or face.get("raw") is None:
            return None
        crop = self.rec.alignCrop(bgr, face["raw"])
        e = self.rec.feature(crop).flatten().astype(np.float32)
        return e / (np.linalg.norm(e) + 1e-9)


SFACE_SAME = 0.363  # OpenCV's published cosine threshold for "same identity" with SFace


class Embedder:
    """DINOv2-small CLS embedding (VBench uses DINO for subject consistency). Falls back to a
    colour+edge descriptor when onnxruntime or the model is unavailable."""

    def __init__(self):
        self.sess = None
        try:
            import onnxruntime as ort  # noqa
            p = model_path("dinov2s.onnx")
            if p:
                so = ort.SessionOptions()
                so.log_severity_level = 3
                self.sess = ort.InferenceSession(str(p), so, providers=["CPUExecutionProvider"])
        except ImportError:
            pass
        self.backend = "dinov2-small" if self.sess is not None else "hist+edges"

    def __call__(self, rgb_list: list[np.ndarray]) -> np.ndarray:
        if self.sess is None:
            return np.stack([fallback_descriptor(x) for x in rgb_list])
        mean = np.array([0.485, 0.456, 0.406], np.float32)
        std = np.array([0.229, 0.224, 0.225], np.float32)
        batch = []
        for x in rgb_list:
            im = cv2.resize(x, (224, 224), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
            batch.append(((im - mean) / std).transpose(2, 0, 1))
        out = []
        for i in range(0, len(batch), 16):
            h = self.sess.run(None, {"pixel_values": np.stack(batch[i:i + 16])})[0]
            cls = h[:, 0, :]
            out.append(cls / (np.linalg.norm(cls, axis=1, keepdims=True) + 1e-9))
        return np.concatenate(out)


def fallback_descriptor(rgb: np.ndarray) -> np.ndarray:
    im = cv2.resize(rgb, (64, 64), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [12, 8], [0, 180, 0, 256]).flatten()
    g = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY).astype(np.float32)
    gx, gy = cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1)
    edges = cv2.resize(np.hypot(gx, gy), (8, 8), interpolation=cv2.INTER_AREA).flatten()
    v = np.concatenate([hist / (hist.sum() + 1e-9), edges / (edges.sum() + 1e-9)]).astype(np.float32)
    return v / (np.linalg.norm(v) + 1e-9)


def phash(rgb: np.ndarray) -> np.ndarray:
    """64-bit DCT perceptual hash (same construction as imagehash.phash)."""
    g = cv2.resize(cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY), (32, 32), interpolation=cv2.INTER_AREA).astype(np.float32)
    d = cv2.dct(g)[:8, :8]
    return (d > np.median(d)).flatten()


def hamming(a: np.ndarray, b: np.ndarray) -> int:
    return int(np.count_nonzero(a != b))


def hs_hist_distance(a: np.ndarray, b: np.ndarray) -> float:
    def h(x):
        hsv = cv2.cvtColor(x, cv2.COLOR_RGB2HSV)
        hh = cv2.calcHist([hsv], [0, 1], None, [18, 8], [0, 180, 0, 256])
        return cv2.normalize(hh, hh).flatten()
    return float(cv2.compareHist(h(a), h(b), cv2.HISTCMP_BHATTACHARYYA))


# ----------------------------------------------------------------------------- report helpers


def fmt_t(t: float) -> str:
    return f"{t:6.2f}s"


def tile(images: list[np.ndarray], labels: list[str], cols: int = 10, border: list[tuple] | None = None,
         label_scale: float = 0.4) -> np.ndarray:
    """Grid of RGB thumbnails with a timestamp label on each."""
    if not images:
        return np.zeros((10, 10, 3), np.uint8)
    h, w = images[0].shape[:2]
    rows = math.ceil(len(images) / cols)
    sheet = np.full((rows * (h + 4), cols * (w + 4), 3), 20, np.uint8)
    for k, (im, lab) in enumerate(zip(images, labels)):
        r, c = divmod(k, cols)
        y, x = r * (h + 4) + 2, c * (w + 4) + 2
        tile_im = im.copy()
        if border and border[k] is not None:
            cv2.rectangle(tile_im, (0, 0), (w - 1, h - 1), border[k], 4)
        cv2.rectangle(tile_im, (0, 0), (int(len(lab) * 9 * label_scale / 0.4) + 6, int(16 * label_scale / 0.4)), (0, 0, 0), -1)
        cv2.putText(tile_im, lab, (3, int(12 * label_scale / 0.4)), cv2.FONT_HERSHEY_SIMPLEX, label_scale,
                    (255, 255, 255), 1, cv2.LINE_AA)
        sheet[y:y + h, x:x + w] = tile_im
    return sheet


def save_jpg(path: Path, rgb: np.ndarray, q: int = 85) -> None:
    cv2.imwrite(str(path), cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, q])


def svg_series(series: list[dict], duration: float, width: int = 1000, height: int = 120,
               marks: list[dict] | None = None, spans: list[dict] | None = None, title: str = "") -> str:
    """Tiny dependency-free SVG line chart. series: {t, y, color, label}; marks: {t, color, label};
    spans: {start, end, color}."""
    pad_l, pad_b = 40, 18
    W, H = width - pad_l, height - pad_b
    def X(t):
        return pad_l + W * (t / max(duration, 1e-6))
    parts = [f'<svg viewBox="0 0 {width} {height}" width="100%" xmlns="http://www.w3.org/2000/svg" '
             f'style="background:var(--panel);border-radius:6px">']
    for sp in spans or []:
        parts.append(f'<rect x="{X(sp["start"]):.1f}" y="0" width="{max(1.5, X(sp["end"]) - X(sp["start"])):.1f}" '
                     f'height="{H}" fill="{sp["color"]}" opacity="0.25"/>')
    for s in series:
        y = np.asarray(s["y"], float)
        t = np.asarray(s["t"], float)
        if len(y) == 0:
            continue
        lo, hi = (s.get("range") or (float(np.nanmin(y)), float(np.nanmax(y))))
        rng = (hi - lo) or 1.0
        step = max(1, len(t) // 1500)
        pts = " ".join(f"{X(tt):.1f},{H - H * (min(max(yy, lo), hi) - lo) / rng:.1f}"
                       for tt, yy in zip(t[::step], y[::step]))
        parts.append(f'<polyline fill="none" stroke="{s["color"]}" stroke-width="1.2" points="{pts}"/>')
    for m in marks or []:
        x = X(m["t"])
        parts.append(f'<line x1="{x:.1f}" y1="{m.get("y0", 0)}" x2="{x:.1f}" y2="{m.get("y1", H)}" stroke="{m["color"]}" '
                     f'stroke-width="{m.get("w", 1)}"><title>{html.escape(m.get("label", ""))}</title></line>')
    step = 1 if duration <= 20 else 2 if duration <= 40 else 5
    for k in range(0, int(duration) + 1, step):
        parts.append(f'<text x="{X(k):.1f}" y="{height - 4}" font-size="10" fill="var(--muted)" '
                     f'text-anchor="middle">{k}s</text>')
    if title:
        parts.append(f'<text x="4" y="12" font-size="11" fill="var(--fg)">{html.escape(title)}</text>')
    parts.append("</svg>")
    return "".join(parts)


HTML_HEAD = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#fafaf8;--fg:#1b1b1b;--muted:#6b6b6b;--panel:#f0efeb;--pass:#1f7a3a;--warn:#a86b00;--fail:#b3261e}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151515;--fg:#eaeaea;--muted:#9a9a9a;--panel:#222;--pass:#5fc27e;--warn:#e0a340;--fail:#ff6b5e}}}}
body{{background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,sans-serif;margin:0 auto;max-width:1100px;padding:16px}}
table{{border-collapse:collapse;width:100%;margin:8px 0 18px}}td,th{{border-bottom:1px solid var(--panel);padding:4px 6px;text-align:left;font-variant-numeric:tabular-nums}}
.PASS{{color:var(--pass);font-weight:600}}.WARN{{color:var(--warn);font-weight:600}}.FAIL{{color:var(--fail);font-weight:700}}.INFO{{color:var(--muted)}}
img{{max-width:100%;border-radius:6px}}h1{{font-size:20px}}h2{{font-size:16px;margin-top:26px}}code{{background:var(--panel);padding:1px 4px;border-radius:3px}}
.legend span{{margin-right:14px}}
</style></head><body>"""


def verdict_of(checks: list[dict]) -> str:
    levels = [c["level"] for c in checks]
    return "FAIL" if "FAIL" in levels else "WARN" if "WARN" in levels else "PASS"


def md_table(rows: list[list], header: list[str]) -> str:
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def html_table(rows: list[list], header: list[str], level_col: int | None = None) -> str:
    h = "<table><tr>" + "".join(f"<th>{html.escape(str(x))}</th>" for x in header) + "</tr>"
    for r in rows:
        h += "<tr>"
        for i, c in enumerate(r):
            cls = f' class="{c}"' if level_col is not None and i == level_col else ""
            h += f"<td{cls}>{html.escape(str(c))}</td>"
        h += "</tr>"
    return h + "</table>"


def to_jsonable(o):
    if isinstance(o, dict):
        return {k: to_jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [to_jsonable(v) for v in o]
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    return o


def default_out(video: str, suffix: str) -> Path:
    p = Path(video)
    return p.parent / f"{p.stem}_{suffix}"
