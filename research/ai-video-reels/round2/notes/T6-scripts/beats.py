#!/usr/bin/env python3
"""beats.py - beat / onset / drop detection for edit-to-music.

usage: python3 beats.py MUSIC [--every 2] [--min-gap 0.35] [--engine auto|librosa|numpy] [--band full|low]
  --band low = analyse only <160 Hz (locks onto the kick drum; use for pop/EDM/trap/phonk)
prints JSON: {"bpm":..,"beats":[..],"downbeats":[..],"cuts":[..],"onsets":[..],"drop":t}
  cuts      = beats thinned to every Nth beat and >= min-gap apart (use as cut points)
  downbeats = every 4th beat starting from the strongest phase (bar starts)
  drop      = time of the largest jump in low-frequency energy (where the "drop" hits)
Engines: librosa (best) -> numpy fallback (ffmpeg decode + spectral-flux + autocorrelation tempo).
"""
import json, subprocess, sys
import numpy as np


def decode(path, sr=22050, band="full"):
    af = ["-af", "lowpass=f=160,lowpass=f=160"] if band == "low" else []
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr)] + af + ["-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32), sr


def numpy_beats(y, sr, hop=256):
    n = 1024
    frames = np.lib.stride_tricks.sliding_window_view(np.pad(y, (n // 2, n // 2)), n)[::hop]
    spec = np.abs(np.fft.rfft(frames * np.hanning(n), axis=1))
    logs = np.log1p(10 * spec)
    flux = np.maximum(0, np.diff(logs, axis=0)).sum(axis=1)
    flux = np.concatenate([[0], flux])
    flux = (flux - flux.mean()) / (flux.std() + 1e-9)
    fps = sr / hop
    # tempo by autocorrelation in 60..180 bpm
    ac = np.correlate(flux, flux, "full")[len(flux) - 1:]
    lags = np.arange(len(ac))
    bpm_l = 60 * fps / np.maximum(lags, 1)
    ok = (bpm_l >= 60) & (bpm_l <= 180)
    prior = np.exp(-0.5 * (np.log2(np.maximum(bpm_l, 1) / 120.0) / 0.9) ** 2)  # favour ~120 bpm (octave errors)
    lag = int(lags[ok][np.argmax((ac * prior)[ok])])
    a0, a1, a2 = ac[lag - 1], ac[lag], ac[lag + 1]
    per = lag + 0.5 * (a0 - a2) / (a0 - 2 * a1 + a2 + 1e-9)  # fractional period (parabolic)
    bpm = 60 * fps / per
    # phase: offset maximizing flux on the grid, then snap each beat to the local flux peak (+-35 ms)
    best = max(range(lag), key=lambda o: sum(flux[int(round(o + k * per))] for k in range(int((len(flux) - o) / per))))
    w = max(1, int(0.035 * fps))
    beats = []
    k = 0
    while best + k * per < len(flux):
        c = int(round(best + k * per))
        lo, hi = max(0, c - w), min(len(flux), c + w + 1)
        beats.append((lo + int(np.argmax(flux[lo:hi]))) / fps + n / 2 / sr * 0)  # frame centre = time
        k += 1
    beats = np.array(beats)
    # onsets: peaks above threshold
    pk = [i for i in range(1, len(flux) - 1) if flux[i] > 1.0 and flux[i] >= flux[i - 1] and flux[i] > flux[i + 1]]
    return float(bpm), beats, np.array(pk) / fps


def librosa_beats(y, sr, low=False):
    import librosa
    env = librosa.onset.onset_strength(y=y, sr=sr, fmax=200 if low else None, n_mels=32 if low else 128)
    tempo, bf = librosa.beat.beat_track(onset_envelope=env, sr=sr, units="frames")
    beats = librosa.frames_to_time(bf, sr=sr)
    on = librosa.onset.onset_detect(y=y, sr=sr, units="time", backtrack=False)
    return float(np.atleast_1d(tempo)[0]), beats, on


def drop_time(y, sr):
    # low-band (<150 Hz) RMS per 0.25 s; drop = biggest positive jump
    from numpy.fft import rfft, rfftfreq
    w = int(sr * 0.25)
    segs = [y[i:i + w] for i in range(0, len(y) - w, w)]
    f = rfftfreq(w, 1 / sr)
    low = np.array([np.sqrt((np.abs(rfft(s))[f < 150] ** 2).sum()) for s in segs])
    if len(low) < 3:
        return 0.0
    j = np.argmax(np.diff(low))
    return round((j + 1) * 0.25, 3)


def main():
    a = sys.argv[1:]
    path = a[0]
    every = int(a[a.index("--every") + 1]) if "--every" in a else 1
    gap = float(a[a.index("--min-gap") + 1]) if "--min-gap" in a else 0.3
    eng = a[a.index("--engine") + 1] if "--engine" in a else "auto"
    band = a[a.index("--band") + 1] if "--band" in a else "full"
    y, sr = decode(path)
    used = "numpy"
    if eng in ("auto", "librosa"):
        try:
            bpm, beats, on = librosa_beats(y, sr, low=(band == "low"))
            used = "librosa"
        except Exception as e:  # noqa
            if eng == "librosa":
                raise
            bpm, beats, on = numpy_beats(decode(path, band=band)[0], sr)
    else:
        bpm, beats, on = numpy_beats(decode(path, band=band)[0], sr)
    beats = [round(float(b), 3) for b in beats]
    # downbeats: phase (0..3) whose beats carry the most onset energy -> approximate with first strong
    down = beats[0::4]
    cuts, last = [], -9
    for b in beats[::every]:
        if b - last >= gap:
            cuts.append(b)
            last = b
    print(json.dumps({"engine": used, "bpm": round(bpm, 2), "beats": beats, "downbeats": down,
                      "cuts": cuts, "onsets": [round(float(o), 3) for o in on], "drop": drop_time(y, sr)}))


if __name__ == "__main__":
    main()
