#!/usr/bin/env python3
"""Red Light v4 re-cut ($0, ffmpeg + OpenCV only, no generation).

Builds three deliverables from the one native-sound Seedance take (clips/RL30_480_t01.mp4),
the two ElevenLabs VO lines (audio/vo1.mp3, audio/vo2.mp3) and the product reference
photo (ref/can.png, the only source of the legible label):

  <out>/VXO_red_light_v4_30s.mp4      9:16 master, 30.0 s
  <out>/VXO_red_light_v4_15s.mp4      9:16 cut-down, 15.0 s
  <out>/VXO_red_light_v4_15s_4x5.mp4  4:5 version of the 15 s

Fixes vs the v3 final (WEAKNESSES #5/#13/#24, doc 64, vxo-film Steps 7-8):
  * 1.5 s flash-forward cold open: punch-in on the real hand-off (with its own synced
    grab/fizz sound), then the can hero (ref photo cut-out, >=30 % of frame, legible).
  * the 2.9 s frozen red-light hold (raw 15.71-18.50 s) is cut out (overhead shot ends at
    raw frame 374, before the freeze starts).
  * no frame-rate conversion: every raw frame is used 1:1 at 24 fps, so no duplicate frames.
  * native sound is cut on the same frame boundaries as the picture (sample-exact,
    2000 samples per frame at 48 kHz), so every onset stays where the generator put it.
  * supers inside the safe box (9:16: y 240-1260, x 120-960 text width <= 720), >= 60 px,
    <= 7 words, Instrument Serif regular with a 4 px dark stroke + soft shadow; rendered with
    PIL as overlays, so no drawtext escaping (no ':' problem at all).
  * end: can packshot + AURUM wordmark, then a swappable offer card (OFFER below, or
    --offer "..." on the command line).
  * two-pass loudnorm I=-14:TP=-2, then the ENCODED file is measured (ebur128, true peak);
    if TP > -1.0 dBTP it re-masters with a limiter and measures again.

Usage (paths default to this experiment folder and the session scratchpad):
  python3 assemble_v4.py --scratch /path/to/scratchpad [--offer "Your first case, 20% off."]
"""
import argparse
import json
import os
import re
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 24
SR = 48000
SPF = SR // FPS  # audio samples per video frame

# Swappable offer line (<= 7 words, no claims). The owner edits this or passes --offer.
OFFER = "Your first case, 20% off."
OPEN_SUPER = "Worth stopping for."
VO1_SUPER = ["Some things are", "worth stopping for."]
DISCLOSURE = "AI-generated film"
WORDMARK = "AURUM"

# Raw shot boundaries in the 480p take (frame index, 24 fps), measured with
# select='gt(scene,0.12)': 90, 121, 173, 221, 288, 343, 445, 553.
# Freeze in the raw take: 15.71-18.50 s (qc_report), i.e. frames 377-444.

FORMATS = {
    "9x16": dict(W=1080, H=1920, text_top=250, text_x0=120, text_w=720, text_bottom=1260,
                 ff_crop=(270, 480)),
    "4x5": dict(W=1080, H=1350, text_top=70, text_x0=120, text_w=840, text_bottom=1290,
                ff_crop=(300, 375)),
}

# Hand-off can position in the raw take around 20.3-21.0 s (raw px, 480x854).
FF_CENTER = (268, 440)


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


# ----------------------------------------------------------------------------- inputs
def read_raw_frames(path):
    cap = cv2.VideoCapture(path)
    frames = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        frames.append(f)
    return frames


def read_audio(path, start=None, dur=None):
    cmd = ["ffmpeg", "-v", "error"]
    if start is not None:
        cmd += ["-ss", str(start)]
    cmd += ["-i", path]
    if dur is not None:
        cmd += ["-t", str(dur)]
    cmd += ["-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    a = np.frombuffer(subprocess.run(cmd, check=True, capture_output=True).stdout, np.float32)
    return a.reshape(-1, 2).copy()


def can_cutout(ref_path):
    """Product cut-out from the client photo: flood-fill the plain studio background."""
    im = cv2.imread(ref_path)
    h, w = im.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    for p in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1),
              (0, h // 2), (w - 1, h // 2)]:
        cv2.floodFill(im.copy(), mask, p, 0, (6, 6, 6), (6, 6, 6),
                      cv2.FLOODFILL_MASK_ONLY | (255 << 8) | 4)
    fg = ((mask[1:-1, 1:-1] == 0).astype(np.uint8)) * 255
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg)
    k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    fg = (lab == k).astype(np.uint8) * 255
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    x, y, ww, hh, _ = st[k]
    a = cv2.GaussianBlur(cv2.erode(fg, np.ones((3, 3), np.uint8)), (5, 5), 0)
    rgba = np.dstack([im, a])[max(0, y - 4):y + hh + 4, max(0, x - 4):x + ww + 4]
    return rgba.astype(np.float32)


# ----------------------------------------------------------------------------- text
class Fonts:
    def __init__(self, font_dir):
        self.regular = os.path.join(font_dir, "InstrumentSerif.ttf")

    def get(self, size):
        return ImageFont.truetype(self.regular, size)


def text_sprite(fonts, lines, size, max_w, tracking=0, min_size=60, color=(246, 242, 232)):
    """RGBA sprite for 1-2 centred lines; shrinks to max_w but never below min_size."""
    while True:
        font = fonts.get(size)
        widths = [line_width(font, ln, tracking) for ln in lines]
        if max(widths) <= max_w or size <= min_size:
            break
        size -= 2
    if max(widths) > max_w:
        raise SystemExit(f"super does not fit at {min_size}px: {lines}")
    asc, desc = font.getmetrics()
    lh = int((asc + desc) * 1.02)
    pad = 24
    W = max(widths) + 2 * pad
    H = lh * len(lines) + 2 * pad
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # soft shadow / scrim
    sh_ = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sh_)
    for i, ln in enumerate(lines):
        x = (W - widths[i]) // 2
        draw_line(d, x + 3, pad + i * lh + 4, ln, font, tracking, (0, 0, 0, 170), stroke=8,
                  stroke_fill=(0, 0, 0, 170))
    sh_ = sh_.filter(ImageFilter.GaussianBlur(7))
    img.alpha_composite(sh_)
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        x = (W - widths[i]) // 2
        draw_line(d, x, pad + i * lh, ln, font, tracking, color + (255,), stroke=4,
                  stroke_fill=(12, 10, 10, 255))
    return np.array(img).astype(np.float32), size


def line_width(font, text, tracking):
    if not tracking:
        return int(font.getlength(text)) + 8
    return int(sum(font.getlength(c) for c in text) + tracking * (len(text) - 1)) + 8


def draw_line(d, x, y, text, font, tracking, fill, stroke, stroke_fill):
    if not tracking:
        d.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
        return
    for c in text:
        d.text((x, y), c, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
        x += font.getlength(c) + tracking


# ----------------------------------------------------------------------------- compositing
def over(dst, src_rgba, x, y, alpha_mul=1.0):
    """Alpha-composite float RGBA sprite (RGB in BGR order for frames) onto uint8/float dst."""
    H, W = dst.shape[:2]
    h, w = src_rgba.shape[:2]
    x0, y0 = max(0, int(round(x))), max(0, int(round(y)))
    x1, y1 = min(W, int(round(x)) + w), min(H, int(round(y)) + h)
    if x1 <= x0 or y1 <= y0:
        return
    sx0, sy0 = x0 - int(round(x)), y0 - int(round(y))
    s = src_rgba[sy0:sy0 + (y1 - y0), sx0:sx0 + (x1 - x0)]
    a = s[..., 3:4] / 255.0 * alpha_mul
    region = dst[y0:y1, x0:x1].astype(np.float32)
    dst[y0:y1, x0:x1] = region * (1 - a) + s[..., :3] * a


def upscale(fr, W, H, crop=None):
    """480p raw -> 1080 wide (lanczos + mild unsharp); then crop to the format height."""
    if crop is not None:
        cx, cy, cw, ch = crop
        fr = fr[cy:cy + ch, cx:cx + cw]
        up = cv2.resize(fr, (W, H), interpolation=cv2.INTER_LANCZOS4)
    else:
        up = cv2.resize(fr, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
        if H != 1920:
            y0 = (1920 - H) // 2
            up = up[y0:y0 + H]
    bl = cv2.GaussianBlur(up, (0, 0), 1.2)
    return cv2.addWeighted(up, 1.35, bl, -0.35, 0)


def blurred_plate(fr, W, H, dark=0.42):
    small = cv2.resize(fr, (120, int(120 * fr.shape[0] / fr.shape[1])), interpolation=cv2.INTER_AREA)
    small = cv2.GaussianBlur(small, (0, 0), 3)
    big = cv2.resize(small, (W, 1920 * W // 1080), interpolation=cv2.INTER_CUBIC)
    y0 = (big.shape[0] - H) // 2
    big = big[y0:y0 + H].astype(np.float32) * dark
    # vignette
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2)
    big *= np.clip(1.15 - 0.55 * r, 0.35, 1.0)[..., None]
    return big


_GLOW = {}


def police_glow(img, t, amp=38.0, hz=1.2):
    """Two soft red/blue light pools (left/right) pulsing in quadrature, like the cruiser's bar
    off-screen. Keeps end cards alive (no frozen frames) without moving the product."""
    H, W = img.shape[:2]
    if (W, H) not in _GLOW:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        gl = np.exp(-(((xx - 0.05 * W) / (0.45 * W)) ** 2 + ((yy - 0.7 * H) / (0.35 * H)) ** 2))
        gr = np.exp(-(((xx - 0.95 * W) / (0.45 * W)) ** 2 + ((yy - 0.7 * H) / (0.35 * H)) ** 2))
        _GLOW[(W, H)] = (gl[..., None], gr[..., None])
    gl, gr = _GLOW[(W, H)]
    a = 0.5 * (1 + np.sin(2 * np.pi * hz * t))
    b = 0.5 * (1 + np.cos(2 * np.pi * hz * t))
    img += gl * (a * amp) * np.array([0.25, 0.2, 1.0], np.float32)   # BGR red
    img += gr * (b * amp) * np.array([1.0, 0.35, 0.15], np.float32)  # BGR blue
    return img


def place_can(dst, can, height, cx, top, t, sweep=True, scale_from=1.0, scale_to=1.05, p=0.0):
    """Can scaled to `height` (times a slow push-in), red/blue police-light sweep."""
    s = scale_from + (scale_to - scale_from) * p
    hh = height * s
    ww = hh * can.shape[1] / can.shape[0]
    spr = cv2.resize(can, (int(round(ww)), int(round(hh))), interpolation=cv2.INTER_AREA)
    rgb = spr[..., :3] * 0.86
    if sweep:
        ph = np.sin(2 * np.pi * 2.5 * t)
        x = np.linspace(-1, 1, spr.shape[1])[None, :, None]
        red = np.clip(-x, 0, 1) * max(ph, 0) * 0.22
        blue = np.clip(x, 0, 1) * max(-ph, 0) * 0.22
        tint = np.concatenate([1 + blue * 1.2, np.ones_like(x) * 1.0 - 0.05 * (red + blue),
                               1 + red * 1.3], axis=2)  # BGR
        rgb = np.clip(rgb * tint, 0, 255)
    spr = np.concatenate([rgb, spr[..., 3:4]], axis=2)
    # contact glow / shadow under the can
    over(dst, spr, cx - spr.shape[1] / 2, top - (hh - height) / 2)


def grain(img, rng, sigma=3.0):
    n = rng.normal(0, sigma, img.shape[:2]).astype(np.float32)[..., None]
    return img + n


# ----------------------------------------------------------------------------- edit
def segments(cut):
    """Edit decision list. Each segment: kind, frames, and its audio source.
    raw: (raw_first_frame, n)  -> picture and sound from the same raw frames
    ff:  punch-in on the hand-off (raw frames, crop) with its own sound
    hero/pack/offer: product cards; audio from `aud` raw seconds (bed)"""
    if cut == "30":
        return [
            dict(kind="ff", raw=487, n=16),                      # 0.000-0.667 grab + fizz mist
            dict(kind="hero", n=20, aud=505),                     # 0.667-1.500 can hero; fizz onset (raw 21.08 s) lands 1 frame after the cut
            dict(kind="raw", raw=0, n=375),                       # 1.500-17.125 shots 1-7, freeze cut
            dict(kind="raw", raw=445, n=96),                      # 17.125-21.125 hand-off
            dict(kind="raw", raw=553, n=72),                      # 21.125-24.125 green, pull away
            dict(kind="pack", n=69, aud=625, bg=626),             # 24.125-27.000 packshot + wordmark
            dict(kind="offer", n=72, aud=None, bg=649),           # 27.000-30.000 offer card
        ]
    if cut == "15":
        return [
            dict(kind="ff", raw=487, n=16),                       # 0.000-0.667
            dict(kind="hero", n=20, aud=505),                      # 0.667-1.500 (fizz onset on the cut)
            dict(kind="raw", raw=10, n=36),                        # burnout
            dict(kind="raw", raw=176, n=44),                       # handbrake turn
            dict(kind="raw", raw=248, n=36),                       # cruiser follows
            dict(kind="raw", raw=306, n=37),                       # light turns red
            dict(kind="raw", raw=343, n=32),                       # overhead stop (pre-freeze)
            dict(kind="raw", raw=466, n=73),                       # hand-off
            dict(kind="endcard", n=66, aud=539, bg=600),           # packshot + wordmark + offer
        ]
    raise ValueError(cut)


def build_audio(raw_audio, segs, vo, total_frames, vo_events):
    out = np.zeros((total_frames * SPF, 2), np.float32)
    pos = 0
    fade = int(0.006 * SR)
    ramp_in, ramp_out = np.linspace(0, 1, fade)[:, None], np.linspace(1, 0, fade)[:, None]
    prev_end_src = None
    for s in segs:
        n = s["n"] * SPF
        if s["kind"] in ("raw", "ff"):
            src0 = s["raw"] * SPF
        else:
            src0 = None if s.get("aud") is None else s["aud"] * SPF
        if src0 is None:
            # continue the previous segment's bed seamlessly
            src0 = prev_end_src
        chunk = raw_audio[src0:src0 + n].copy() if src0 is not None else np.zeros((n, 2), np.float32)
        if len(chunk) < n:
            short = len(chunk)
            chunk = np.concatenate([chunk, np.zeros((n - short, 2), np.float32)])
            if short > SR // 2:
                f = min(short, SR)
                chunk[short - f:short] *= np.linspace(1, 0, f)[:, None]
        contiguous = prev_end_src is not None and src0 == prev_end_src
        if not contiguous and pos > 0:
            out[pos - fade:pos] *= ramp_out
            chunk[:fade] *= ramp_in
        out[pos:pos + n] = chunk
        pos += n
        prev_end_src = src0 + n
    # end fade on the bed (last 0.9 s)
    f = int(0.9 * SR)
    out[-f:] *= np.linspace(1, 0.15, f)[:, None]
    # duck the bed under the VO, then lay the VO
    gain = np.ones(len(out), np.float32)
    bed_rms = np.sqrt(np.mean(out ** 2)) + 1e-9
    for name, t0 in vo_events:
        a = vo[name]
        i0 = int(round(t0 * SR))
        i1 = min(len(out), i0 + len(a))
        r = int(0.08 * SR)
        g = 10 ** (-7 / 20)
        seg = np.full(i1 - i0, g, np.float32)
        gain[i0:i1] = np.minimum(gain[i0:i1], seg)
        gain[max(0, i0 - r):i0] = np.minimum(gain[max(0, i0 - r):i0], np.linspace(1, g, i0 - max(0, i0 - r)))
        e = min(len(out), i1 + r)
        gain[i1:e] = np.minimum(gain[i1:e], np.linspace(g, 1, e - i1))
    out *= gain[:, None]
    for name, t0 in vo_events:
        a = vo[name]
        act = a[np.abs(a).max(axis=1) > 0.02]
        vo_rms = np.sqrt(np.mean(act ** 2)) + 1e-9
        a = a * (bed_rms * 2.4 / vo_rms)  # VO ~ +7.6 dB over the average bed
        i0 = int(round(t0 * SR))
        i1 = min(len(out), i0 + len(a))
        out[i0:i1] += a[:i1 - i0]
    return out


def render(cut, fmt, args, raw, raw_audio, can, fonts, vo):
    F = FORMATS[fmt]
    W, H = F["W"], F["H"]
    segs = segments(cut)
    total = sum(s["n"] for s in segs)
    assert total == (720 if cut == "30" else 360), total
    rng = np.random.default_rng(7)

    # --- supers (sprites + timing) ---
    top, tw = F["text_top"], F["text_w"]
    open_spr, open_sz = text_sprite(fonts, [OPEN_SUPER], 96, tw)
    disc_spr, disc_sz = text_sprite(fonts, [DISCLOSURE], 60, tw, color=(232, 228, 220))
    word_spr, word_sz = text_sprite(fonts, [WORDMARK], 150, tw, tracking=34)
    offer_lines = wrap_offer(args.offer)
    offer_spr, offer_sz = text_sprite(fonts, offer_lines, 96, tw)
    vo1_spr, vo1_sz = text_sprite(fonts, VO1_SUPER, 88, tw)
    sizes = dict(open=open_sz, disclosure=disc_sz, wordmark=word_sz, offer=offer_sz, vo1=vo1_sz)

    def cx(spr):
        return (W - spr.shape[1]) / 2

    pad = 24  # sprite padding: glyph box top = y + pad
    starts = np.cumsum([0] + [s["n"] for s in segs])
    supers = []  # (f0, f1, sprite, x, y)
    supers.append((2, 53, open_spr, cx(open_spr), top - pad))
    supers.append((0, 72, disc_spr, cx(disc_spr), top - pad + open_spr.shape[0] - 18))
    if cut == "30":
        i_pack, i_offer = 5, 6
        supers.append((starts[4] - 0, starts[4] + 72, vo1_spr, cx(vo1_spr), top - pad))
        supers.append((starts[i_pack] + 3, starts[i_pack + 1], word_spr, cx(word_spr), top - pad))
        supers.append((starts[i_offer], total, offer_spr, cx(offer_spr), top - pad))
        supers.append((starts[i_offer], total, disc_spr, cx(disc_spr), top - pad + offer_spr.shape[0] - 10))
    else:
        i_end = 8
        supers.append((starts[i_end] + 2, total, word_spr, cx(word_spr), top - pad))
        supers.append((starts[i_end] + 2, total, offer_spr, cx(offer_spr), top - pad + word_spr.shape[0] - 20))
        supers.append((starts[i_end] + 2, total, disc_spr, cx(disc_spr),
                       top - pad + word_spr.shape[0] + offer_spr.shape[0] - 40))

    # box check (glyph tops/bottoms inside the safe box)
    box = []
    for f0, f1, spr, x, y in supers:
        y_top, y_bot = y + pad - 6, y + spr.shape[0] - pad + 6
        box.append(dict(t0=round(f0 / FPS, 3), t1=round(f1 / FPS, 3), y_top=round(y_top), y_bottom=round(y_bot),
                        x_left=round(x + pad), x_right=round(x + spr.shape[1] - pad)))

    # lowest glyph bottom of the supers on screen in each segment (cans are placed below it)
    seg_text_bottom = []
    for si in range(len(segs)):
        f = starts[si] + min(4, segs[si]["n"] - 1)
        bots = [b["y_bottom"] for (f0, f1, *_), b in zip(supers, box) if f0 <= f < f1]
        seg_text_bottom.append(max(bots) if bots else 0)

    def can_box(si, hgt, topc):
        topc = max(topc, seg_text_bottom[si] + 30)
        hgt = min(hgt, H - 70 - topc)
        return hgt, topc

    # --- video ---
    out_v = args.work / f"v_{cut}_{fmt}.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow",
                            "-crf", "16", "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
                            "-color_trc", "bt709", "-colorspace", "bt709", str(out_v)], stdin=subprocess.PIPE)
    fi = 0
    cw, ch = F["ff_crop"]
    ff_crop = (FF_CENTER[0] - cw // 2, FF_CENTER[1] - ch // 2, cw, ch)
    for si, s in enumerate(segs):
        for k in range(s["n"]):
            t = fi / FPS
            p = k / max(1, s["n"] - 1)
            if s["kind"] == "raw":
                img = upscale(raw[s["raw"] + k], W, H).astype(np.float32)
            elif s["kind"] == "ff":
                # slow push on the crop so the punch-in breathes
                zc = 1.0 - 0.06 * p
                cw2, ch2 = int(cw * zc), int(ch * zc)
                crop = (FF_CENTER[0] - cw2 // 2, FF_CENTER[1] - ch2 // 2 + 6, cw2, ch2)
                img = upscale(raw[s["raw"] + k], W, H, crop=crop).astype(np.float32)
                img = grain(img, rng, 2.0)
            elif s["kind"] == "hero":
                img = blurred_plate(raw[s["aud"] + k], W, H, dark=0.5)
                hgt = 1500 if fmt == "9x16" else 1150
                topc = 400 if fmt == "9x16" else 200
                hgt = max(hgt, 0)
                topc = max(topc, seg_text_bottom[si] + 20)
                place_can(img, can, hgt, W / 2, topc, t, p=p, scale_from=1.0, scale_to=1.07)
                img = grain(img, rng, 3.0)
            elif s["kind"] in ("pack", "endcard"):
                img = police_glow(blurred_plate(raw[min(len(raw) - 1, s["bg"] + k)], W, H, dark=0.38), t)
                if fmt == "9x16":
                    hgt, topc = (1080, 430) if s["kind"] == "pack" else (1100, 560)
                else:
                    hgt, topc = 900, 520
                hgt, topc = can_box(si, hgt, topc)
                place_can(img, can, hgt, W / 2, topc, t, sweep=False, p=p, scale_from=1.0, scale_to=1.10)
                img = grain(img, rng, 3.0)
            elif s["kind"] == "offer":
                img = police_glow(blurred_plate(raw[min(len(raw) - 1, s["bg"] + k)], W, H, dark=0.32), t)
                hgt, topc = can_box(si, 900, 520)
                place_can(img, can, hgt, W / 2, topc, t, sweep=False, p=p, scale_from=1.0, scale_to=1.10)
                img = grain(img, rng, 3.0)
            for f0, f1, spr, x, y in supers:
                if f0 <= fi < f1:
                    a = min(1.0, (fi - f0 + 1) / 4, (f1 - fi) / 4)
                    over(img, spr, x, y, a)
            enc.stdin.write(np.clip(img, 0, 255).astype(np.uint8).tobytes())
            fi += 1
    enc.stdin.close()
    enc.wait()

    # --- audio ---
    if cut == "30":
        vo_events = [("vo1", starts[4] / FPS + 0.30), ("vo2", starts[5] / FPS + 0.33)]
    else:
        vo_events = [("vo1", starts[7] / FPS + 1.20)]
    mix = build_audio(raw_audio, segs, vo, total, vo_events)
    mix_path = args.work / f"a_{cut}_{fmt}.wav"
    write_wav(mix_path, mix)
    final = args.out / f"VXO_red_light_v4_{cut}s{'' if fmt == '9x16' else '_4x5'}.mp4"
    meas = master(out_v, mix_path, final, args.work)
    edl = [dict(kind=s["kind"], t0=round(starts[i] / FPS, 3), t1=round(starts[i + 1] / FPS, 3),
                raw_t0=round(s["raw"] / FPS, 3) if "raw" in s else None,
                raw_t1=round((s["raw"] + s["n"]) / FPS, 3) if "raw" in s else None)
           for i, s in enumerate(segs)]
    return dict(file=str(final), fmt=fmt, cut=cut, frames=total, edl=edl, supers=box, super_px=sizes,
                vo=[dict(line=n, t=round(t, 3)) for n, t in vo_events], loudness=meas)


def wrap_offer(text):
    words = text.split()
    if len(words) > 7:
        raise SystemExit("offer line must be <= 7 words")
    if len(text) <= 16:
        return [text]
    best = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
    return [" ".join(words[:best]), " ".join(words[best:])]


def write_wav(path, a):
    pcm = (np.clip(a, -1, 1) * 32767).astype("<i2")
    sh(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-", str(path)],
       input=pcm.tobytes())


def ebur128(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = r[r.rfind("Summary:"):]
    I = float(re.search(r"I:\s+(-?[\d.]+) LUFS", tail).group(1))
    LRA = float(re.search(r"LRA:\s+(-?[\d.]+) LU", tail).group(1))
    TP = float(re.search(r"Peak:\s+(-?[\d.inf]+) dBFS", tail).group(1))
    return dict(I=I, LRA=LRA, TP=TP)


def master(video, wav, final, work):
    def two_pass(extra=""):
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(wav), "-af",
                            "loudnorm=I=-14:TP=-2:LRA=11:print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        m = json.loads(r[r.rfind("{"):r.rfind("}") + 1])
        af = ("loudnorm=I=-14:TP=-2:LRA=11:measured_I={input_i}:measured_TP={input_tp}:"
              "measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}:"
              "linear=true:print_format=summary").format(**m)
        af += extra + ",aresample=48000"
        sh(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(wav), "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
            "-movflags", "+faststart", "-shortest", str(final)])
        return ebur128(final)

    m = two_pass()
    m["pass"] = "loudnorm two-pass"
    if m["TP"] > -1.0 or abs(m["I"] + 14) > 1:
        m = two_pass(",alimiter=limit=0.8:level=false")
        m["pass"] = "loudnorm two-pass + alimiter 0.8"
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True, help="session scratchpad (fonts/, films/)")
    ap.add_argument("--raw", default=os.path.join(HERE, "clips", "RL30_480_t01.mp4"))
    ap.add_argument("--offer", default=OFFER)
    ap.add_argument("--only", default="", help="e.g. 30 or 15 or 15_4x5")
    args = ap.parse_args()
    from pathlib import Path
    args.work = Path(args.scratch) / "rl4" / "work"
    args.work.mkdir(parents=True, exist_ok=True)
    args.out = Path(args.scratch) / "films"
    fonts = Fonts(os.path.join(args.scratch, "fonts"))
    raw = read_raw_frames(args.raw)
    raw_audio = read_audio(args.raw)
    can = can_cutout(os.path.join(HERE, "ref", "can.png"))
    vo = {k: read_audio(os.path.join(HERE, "audio", f"{k}.mp3")) for k in ("vo1", "vo2")}
    jobs = [("30", "9x16"), ("15", "9x16"), ("15", "4x5")]
    if args.only:
        jobs = [j for j in jobs if f"{j[0]}{'' if j[1] == '9x16' else '_4x5'}" == args.only]
    res = [render(c, f, args, raw, raw_audio, can, fonts, vo) for c, f in jobs]
    out = args.work / f"build{('_' + args.only) if args.only else ''}.json"
    out.write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
