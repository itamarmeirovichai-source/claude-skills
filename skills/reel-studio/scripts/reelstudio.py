#!/usr/bin/env python3
"""
reelstudio - an ffmpeg-based edit engine for vertical reels and ads.

Claude (or a human) writes a JSON edit spec; this tool turns it into a finished
1080x1920 H.264 reel: layouts (full / split / wipe / slider / input+prompt+result
/ picture-in-picture), transitions, per-clip and global effects, Hebrew-correct
text and captions (libass + fribidi + harfbuzz), music with ducking, synthetic
SFX on cuts and two-pass loudness normalisation.

Stdlib only. Needs ffmpeg + ffprobe on PATH (built with libass, libx264).
Optional: faster-whisper for automatic captions.

Commands
  render  SPEC.json [--preset P] [--out FILE] [--dry-run] [--keep] [--fast]
  plan    SPEC.json                      print the resolved timeline only
  probe   FILE...                        media info as JSON
  captions VIDEO [--lang he] [--style bold_pop]   whisper -> words.json/.srt/.ass
  grid    VIDEO [--cols 4 --rows 3]      contact sheet jpg with timestamps
  cuts    VIDEO [--threshold 0.3]        scene-cut detection
  fonts                                  download Heebo/Rubik/Secular One/JetBrains Mono
  sfx     [--out DIR]                    write the synthetic SFX library as wav files
  demo-media [--out DIR]                 synthetic placeholder clips for examples/ and smoke tests
  lut     OUT.cube [--kind warm]         write a simple 3D LUT

Run `reelstudio.py <command> -h` for options. Full spec reference: ../SKILL.md
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
import urllib.request
from pathlib import Path

VERSION = "1.0.0"
CACHE_DIR = Path(os.environ.get("REELSTUDIO_CACHE", Path.home() / ".cache" / "reel-studio"))
FONT_DIR = CACHE_DIR / "fonts"
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
HEBREW_RE = re.compile(r"[֐-׿יִ-ﭏ]")
RLM = "‏"

FONT_SOURCES = {
    # file name in cache            -> path under github.com/google/fonts/main/
    "Heebo[wght].ttf": "ofl/heebo/Heebo%5Bwght%5D.ttf",
    "Rubik[wght].ttf": "ofl/rubik/Rubik%5Bwght%5D.ttf",
    "SecularOne-Regular.ttf": "ofl/secularone/SecularOne-Regular.ttf",
    "JetBrainsMono[wght].ttf": "ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
}
FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/"


class SpecError(Exception):
    """Problem in the edit spec (user-fixable)."""


class RenderError(Exception):
    """ffmpeg / environment failure."""


def log(msg: str) -> None:
    print(f"[reelstudio] {msg}", file=sys.stderr, flush=True)


def warn(msg: str) -> None:
    print(f"[reelstudio] WARNING: {msg}", file=sys.stderr, flush=True)


# --------------------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------------------

def fnum(x: float, nd: int = 4) -> str:
    """Compact float for filter strings."""
    s = f"{float(x):.{nd}f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def even(x: float) -> int:
    v = int(round(x))
    return v if v % 2 == 0 else v + 1


def esc_filter_path(p: str) -> str:
    """Escape a value (file path) for use inside a filtergraph option (two levels)."""
    s = str(p)
    for ch in ("\\", "'", ":"):
        s = s.replace(ch, "\\" + ch)
    out = []
    for ch in s:
        if ch in "\\'[],;":
            out.append("\\" + ch)
        else:
            out.append(ch)
    return "".join(out)


def parse_color(c, default="#FFFFFF") -> tuple[int, int, int, int]:
    """'#RRGGBB', '#RRGGBBAA', 'white', 'white@0.5' -> (r,g,b,a) with a=255 opaque."""
    named = {
        "white": "#FFFFFF", "black": "#000000", "yellow": "#FFE000", "red": "#FF2D2D",
        "green": "#2DFF6A", "blue": "#2D7BFF", "cyan": "#00E5FF", "magenta": "#FF2DE0",
        "orange": "#FF8A00", "gray": "#808080", "grey": "#808080", "pink": "#FF5FA2",
        "gold": "#FFC83D", "neon": "#39FF14",
    }
    if c is None:
        c = default
    c = str(c).strip()
    alpha = None
    if "@" in c:
        c, a = c.split("@", 1)
        alpha = int(round(float(a) * 255))
    c = named.get(c.lower(), c)
    if not c.startswith("#") or len(c) not in (7, 9):
        raise SpecError(f"bad color {c!r} (use #RRGGBB, #RRGGBBAA or a name)")
    r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
    a = int(c[7:9], 16) if len(c) == 9 else 255
    if alpha is not None:
        a = alpha
    return r, g, b, a


def ass_color(c, default="#FFFFFF") -> str:
    r, g, b, _ = parse_color(c, default)
    return f"&H{b:02X}{g:02X}{r:02X}&"


def ass_alpha(c, default="#FFFFFF") -> str:
    a = parse_color(c, default)[3]
    return f"&H{255 - a:02X}&"


def ff_color(c, default="#000000") -> str:
    r, g, b, a = parse_color(c, default)
    return f"0x{r:02X}{g:02X}{b:02X}" + (f"@{a / 255:.3f}" if a != 255 else "")


def ass_time(t: float) -> str:
    t = max(0.0, t)
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def ass_escape(text: str) -> str:
    text = str(text).replace("{", "(").replace("}", ")")
    return text.replace("\r", "").replace("\n", "\\N")


def is_rtl(text: str) -> bool:
    return bool(HEBREW_RE.search(text or ""))


def rtl_fix(text: str, direction: str = "auto") -> str:
    """Force an RTL paragraph for Hebrew text: prefix every line with RLM.

    libass resolves the base direction from the first strong character (with
    Encoding=-1); a Hebrew line that starts with 'AI' or a number would otherwise
    be laid out left-to-right. RLM makes the line RTL so punctuation and mixed
    English/numbers land on the correct side.
    """
    if direction == "ltr" or (direction == "auto" and not is_rtl(text)):
        return text
    return "\\N".join(RLM + ln for ln in text.split("\\N"))


def sec(v, name="time") -> float:
    """Accept 3.5, '3.5', '0:03.5', '00:00:03.5'."""
    if v is None:
        raise SpecError(f"missing {name}")
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    try:
        parts = [float(p) for p in s.split(":")]
    except ValueError:
        raise SpecError(f"bad {name}: {v!r}")
    t = 0.0
    for p in parts:
        t = t * 60 + p
    return t


def tail(text: str, n: int = 25) -> str:
    lines = [ln for ln in (text or "").splitlines() if ln.strip()]
    return "\n".join(lines[-n:])


def which_or_die(name: str) -> str:
    p = shutil.which(name)
    if not p:
        raise RenderError(f"{name} not found on PATH. Install ffmpeg (with libass + libx264).")
    return p


# --------------------------------------------------------------------------------------
# ffmpeg runner / probe
# --------------------------------------------------------------------------------------

class Runner:
    def __init__(self, dry: bool = False, verbose: bool = False):
        self.dry = dry
        self.verbose = verbose
        self.env = os.environ.copy()
        conf = FONT_DIR / "fonts.conf"
        if conf.exists():
            self.env["FONTCONFIG_FILE"] = str(conf)
        self.step = 0

    def run(self, cmd: list[str], desc: str, capture: bool = False) -> subprocess.CompletedProcess | None:
        self.step += 1
        if self.dry or self.verbose:
            pretty = " ".join(shlex.quote(c) for c in cmd)
            print(f"\n# [{self.step}] {desc}\n{pretty}", flush=True)
        if self.dry:
            return None
        t0 = time.time()
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                           env=self.env, errors="replace")
        if p.returncode != 0:
            raise RenderError(f"ffmpeg failed during: {desc}\n--- stderr (tail) ---\n{tail(p.stderr)}"
                              f"\n--- command ---\n{' '.join(shlex.quote(c) for c in cmd)}")
        log(f"{desc} ({time.time() - t0:.1f}s)")
        return p


_PROBE_CACHE: dict[str, dict] = {}


def probe(path: str | Path) -> dict:
    path = str(path)
    if not os.path.exists(path):
        raise SpecError(f"file not found: {path}")
    st = os.stat(path)
    key = f"{path}|{st.st_mtime_ns}|{st.st_size}"  # re-probe files that were re-rendered
    if key in _PROBE_CACHE:
        return _PROBE_CACHE[key]
    cmd = [which_or_die("ffprobe"), "-v", "error", "-print_format", "json", "-show_format",
           "-show_streams", path]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        raise SpecError(f"ffprobe cannot read {path}: {tail(p.stderr, 5)}")
    data = json.loads(p.stdout or "{}")
    v = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    a = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), None)
    ext = Path(path).suffix.lower()
    info = {
        "path": path,
        "duration": float(data.get("format", {}).get("duration") or 0) or None,
        "has_video": v is not None,
        "has_audio": a is not None,
        "is_image": ext in IMAGE_EXT,
        "width": None, "height": None, "fps": None, "rotation": 0,
        "vcodec": v.get("codec_name") if v else None,
        "acodec": a.get("codec_name") if a else None,
        "size_bytes": int(data.get("format", {}).get("size") or 0),
        "bitrate": int(data.get("format", {}).get("bit_rate") or 0),
    }
    if v:
        w, h = int(v.get("width") or 0), int(v.get("height") or 0)
        rot = 0
        for sd in v.get("side_data_list", []) or []:
            if "rotation" in sd:
                rot = int(sd["rotation"])
        if "rotate" in (v.get("tags") or {}):
            rot = int(v["tags"]["rotate"])
        if abs(rot) % 180 == 90:
            w, h = h, w
        info.update(width=w, height=h, rotation=rot)
        fr = v.get("avg_frame_rate") or v.get("r_frame_rate") or "0/1"
        try:
            n, d = fr.split("/")
            info["fps"] = round(float(n) / float(d), 3) if float(d) else None
        except (ValueError, ZeroDivisionError):
            pass
        if info["duration"] is None and v.get("duration"):
            info["duration"] = float(v["duration"])
    _PROBE_CACHE[key] = info
    return info


# --------------------------------------------------------------------------------------
# fonts
# --------------------------------------------------------------------------------------

def write_fontconfig() -> Path:
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    conf = FONT_DIR / "fonts.conf"
    conf.write_text(
        '<?xml version="1.0"?>\n<!DOCTYPE fontconfig SYSTEM "fonts.dtd">\n<fontconfig>\n'
        '  <include ignore_missing="yes">/etc/fonts/fonts.conf</include>\n'
        f"  <dir>{FONT_DIR}</dir>\n  <cachedir>{FONT_DIR / 'fc-cache'}</cachedir>\n"
        "</fontconfig>\n", encoding="utf-8")
    return conf


def download_fonts(force: bool = False, quiet: bool = False) -> list[str]:
    """Download Heebo / Rubik / Secular One / JetBrains Mono from github.com/google/fonts."""
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    got = []
    for fname, rel in FONT_SOURCES.items():
        dst = FONT_DIR / fname
        if dst.exists() and dst.stat().st_size > 10000 and not force:
            got.append(fname)
            continue
        url = FONT_URL + rel
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "reelstudio"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            if len(data) < 10000:
                raise RuntimeError("file too small")
            dst.write_bytes(data)
            got.append(fname)
            if not quiet:
                log(f"font: {fname} ({len(data) // 1024} KB)")
        except Exception as e:  # network failures must not kill a render
            # curl fallback (respects proxy env / CA bundles that urllib may not)
            if shutil.which("curl"):
                p = subprocess.run(["curl", "-fsSL", "-o", str(dst), url],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if p.returncode == 0 and dst.exists() and dst.stat().st_size > 10000:
                    got.append(fname)
                    if not quiet:
                        log(f"font: {fname} (curl)")
                    continue
            warn(f"could not download {fname}: {e}")
    write_fontconfig()
    return got


def ensure_fonts(runner: Runner) -> None:
    have = [f for f in FONT_SOURCES if (FONT_DIR / f).exists()]
    if len(have) < 2:
        log("fonts not cached yet - downloading Heebo/Rubik/... (one time)")
        download_fonts(quiet=True)
    conf = write_fontconfig()
    runner.env["FONTCONFIG_FILE"] = str(conf)
    if not (FONT_DIR / "Heebo[wght].ttf").exists():
        warn("Heebo not available - libass will fall back to a system font (DejaVu has Hebrew).")


def mono_font() -> str:
    return "JetBrains Mono" if (FONT_DIR / "JetBrainsMono[wght].ttf").exists() else "DejaVu Sans Mono"


# --------------------------------------------------------------------------------------
# export presets
# --------------------------------------------------------------------------------------

PRESETS = {
    "instagram": {"scale": None, "video": ["-c:v", "libx264", "-profile:v", "high", "-level:v", "4.2",
                                         "-preset", "slow", "-b:v", "12M", "-maxrate", "15M",
                                         "-bufsize", "24M"],
                  "audio": ["-c:a", "aac", "-b:a", "192k", "-ar", "48000"],
                  "inter": ["-preset", "veryfast", "-crf", "14"]},
    "tiktok": {"scale": None, "video": ["-c:v", "libx264", "-profile:v", "high", "-level:v", "4.2",
                                      "-preset", "slow", "-b:v", "13M", "-maxrate", "15M",
                                      "-bufsize", "24M"],
               "audio": ["-c:a", "aac", "-b:a", "192k", "-ar", "48000"],
               "inter": ["-preset", "veryfast", "-crf", "14"]},
    "shorts": {"scale": None, "video": ["-c:v", "libx264", "-profile:v", "high", "-level:v", "4.2",
                                      "-preset", "slow", "-b:v", "12M", "-maxrate", "15M",
                                      "-bufsize", "24M"],
               "audio": ["-c:a", "aac", "-b:a", "320k", "-ar", "48000"],
               "inter": ["-preset", "veryfast", "-crf", "14"]},
    "master": {"scale": None, "video": ["-c:v", "libx264", "-profile:v", "high", "-preset", "slow",
                                      "-crf", "16", "-maxrate", "30M", "-bufsize", "40M"],
               "audio": ["-c:a", "aac", "-b:a", "320k", "-ar", "48000"],
               "inter": ["-preset", "veryfast", "-crf", "12"]},
    "feed": {"scale": None, "canvas": (1080, 1350),
             "video": ["-c:v", "libx264", "-profile:v", "high", "-level:v", "4.2",
                       "-preset", "slow", "-b:v", "10M", "-maxrate", "12M", "-bufsize", "20M"],
             "audio": ["-c:a", "aac", "-b:a", "192k", "-ar", "48000"],
             "inter": ["-preset", "veryfast", "-crf", "14"]},
    "draft": {"scale": (480, -2), "video": ["-c:v", "libx264", "-profile:v", "high", "-preset",
                                            "veryfast", "-crf", "27"],
              "audio": ["-c:a", "aac", "-b:a", "96k", "-ar", "48000"],
              "inter": ["-preset", "ultrafast", "-crf", "22"]},
}
PRESET_ALIASES = {"ig": "instagram", "reels": "instagram", "tt": "tiktok", "yt": "shorts",
                  "youtube": "shorts", "preview": "draft", "feed45": "feed", "4x5": "feed",
                  "4:5": "feed", "ig_feed": "feed", "facebook": "feed"}


def resolve_preset(name: str | None, spec: dict) -> str:
    name = name or spec.get("export") or "instagram"
    name = PRESET_ALIASES.get(name, name)
    if name not in PRESETS:
        raise SpecError(f"unknown export preset {name!r}. Valid: {', '.join(PRESETS)} "
                        f"(aliases: {', '.join(PRESET_ALIASES)})")
    return name


def apply_preset_canvas(spec: dict, preset: str) -> dict:
    """Presets with a fixed aspect (feed 4:5) override the canvas size; layout coords scale with it."""
    cv = PRESETS[preset].get("canvas")
    if cv:
        spec = dict(spec)
        spec["canvas"] = {**(spec.get("canvas") or {}), "width": cv[0], "height": cv[1]}
    return spec


# --------------------------------------------------------------------------------------
# effects
# --------------------------------------------------------------------------------------

COLOR_PRESETS = {
    "teal_orange": "colorbalance=rs=-0.08:gs=-0.02:bs=0.10:rm=0.02:bm=-0.03:rh=0.08:gh=0.02:bh=-0.08,"
                   "eq=contrast=1.06:saturation=1.12",
    "warm": "colorbalance=rs=0.05:bs=-0.05:rm=0.05:bm=-0.06:rh=0.04:bh=-0.05,eq=saturation=1.08",
    "cool": "colorbalance=rs=-0.05:bs=0.06:rm=-0.04:bm=0.05:rh=-0.03:bh=0.04,eq=saturation=0.98",
    "bw": "hue=s=0,eq=contrast=1.12",
    "vibrant": "eq=contrast=1.05:saturation=1.30",
    "film": "curves=all='0/0.05 0.5/0.5 1/0.95',eq=saturation=0.92,colorbalance=rs=0.02:bh=-0.02",
    "moody": "eq=brightness=-0.03:contrast=1.10:saturation=0.85,colorbalance=bs=0.05:bm=0.02",
    "flat_original": "eq=contrast=0.94:saturation=0.85",
}

EFFECTS = ["zoom_punch", "ken_burns", "shake", "glitch", "rgb_split", "flash", "film_grain",
           "vignette", "letterbox", "lut", "color", "blur", "sharpen", "fade", "mirror",
           "speed_ramp", "blur_bg", "dip"]


class Graph:
    """Collects -i inputs and filtergraph lines for one ffmpeg invocation."""

    def __init__(self, prefix: str = "x"):
        self.inputs: list[list[str]] = []
        self.lines: list[str] = []
        self.n = 0
        self.prefix = prefix
        self.kinds: dict[str, str] = {}

    def add_input(self, args: list[str]) -> int:
        self.inputs.append(args)
        return len(self.inputs) - 1

    def label(self, hint: str = "v") -> str:
        self.n += 1
        name = f"{self.prefix}{hint}{self.n}"
        self.kinds[name] = "a" if hint == "a" else "v"
        return name

    def add(self, line: str) -> None:
        self.lines.append(line)

    def chain(self, src: str, filters: str, hint: str = "v") -> str:
        if not filters:
            return src
        out = self.label(hint)
        self.add(f"[{src}]{filters}[{out}]")
        return out

    def script(self) -> str:
        return ";\n".join(self.lines)

    def sink_unused(self, keep: list[str]) -> None:
        """Terminate every produced-but-never-consumed label (ffmpeg rejects dangling outputs)."""
        produced, consumed = [], set()
        for ln in self.lines:
            m_in = re.match(r"^((?:\[[^\]]+\])+)", ln)
            if m_in:
                consumed.update(re.findall(r"\[([^\]]+)\]", m_in.group(1)))
            m_out = re.search(r"((?:\[[^\]]+\])+)$", ln)
            if m_out and (not m_in or m_out.start() > m_in.end()):
                produced += re.findall(r"\[([^\]]+)\]", m_out.group(1))
        for lab in produced:
            if lab not in consumed and lab not in keep:
                sink = "anullsink" if self.kinds.get(lab) == "a" else "nullsink"
                self.add(f"[{lab}]{sink}")

    def cmd_inputs(self) -> list[str]:
        out = []
        for a in self.inputs:
            out += a
        return out


def _times(v) -> list[float]:
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        return [sec(x) for x in v]
    return [sec(v)]


def apply_effects(g: Graph, src: str, effects: list, W: int, H: int, fps: float, dur: float) -> str:
    """Append effect filters to stream `src` (size WxH, local time starts at 0). Returns new label."""
    cur = src
    for eff in effects or []:
        if isinstance(eff, str):
            eff = {"type": eff}
        t = eff.get("type")
        if t not in EFFECTS:
            raise SpecError(f"unknown effect {t!r}. Valid: {', '.join(EFFECTS)}")
        start = sec(eff.get("start", 0))
        end = sec(eff.get("end", dur))
        win = f"between(t,{fnum(start)},{fnum(end)})"

        if t in ("speed_ramp", "blur_bg"):
            continue  # handled at clip level

        if t == "zoom_punch":
            scale = float(eff.get("scale", 1.15))
            ats = _times(eff.get("at", 0)) or [0.0]
            pdur = eff.get("dur")
            ease = float(eff.get("ease", 0.06))
            terms = []
            for a in ats:
                b = a + (sec(pdur) if pdur is not None else dur + 1)
                ramp = f"min(1,(it-{fnum(a)})/{fnum(max(ease, 1e-3))})"
                terms.append(f"between(it,{fnum(a)},{fnum(b)})*{ramp}")
            k = "+".join(terms)
            z = f"1+{fnum(scale - 1)}*min(1,{k})"
            cur = g.chain(cur, f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                               f"d=1:s={W}x{H}:fps={fnum(fps)},setsar=1")

        elif t == "ken_burns":
            z0 = float(eff.get("from", 1.0))
            z1 = float(eff.get("to", 1.15))
            pan = eff.get("pan", "center")
            smooth = float(eff.get("smooth", 1.5))
            p = f"min(1,max(0,(it-{fnum(start)})/{fnum(max(end - start, 0.01))}))"
            z = f"{fnum(z0)}+({fnum(z1 - z0)})*{p}"
            xs = {"left": f"(iw-iw/zoom)*(1-{p})", "right": f"(iw-iw/zoom)*{p}"}
            ys = {"up": f"(ih-ih/zoom)*(1-{p})", "down": f"(ih-ih/zoom)*{p}"}
            x = xs.get(pan, "iw/2-(iw/zoom/2)")
            y = ys.get(pan, "ih/2-(ih/zoom/2)")
            pre = f"scale={even(W * smooth)}:{even(H * smooth)}:flags=bicubic," if smooth > 1 else ""
            cur = g.chain(cur, f"{pre}zoompan=z='{z}':x='{x}':y='{y}':d=1:s={W}x{H}:fps={fnum(fps)},setsar=1")

        elif t == "shake":
            amp = float(eff.get("intensity", 12))
            sp = float(eff.get("speed", 1.0))
            m = int(math.ceil(amp * 1.3)) + 2
            env = win
            xe = f"{m}+{fnum(amp)}*{env}*(0.6*sin(t*{fnum(29 * sp)})+0.4*sin(t*{fnum(13 * sp)}+1.3))"
            ye = f"{m}+{fnum(amp)}*{env}*(0.6*sin(t*{fnum(23 * sp)}+0.7)+0.4*sin(t*{fnum(17 * sp)}))"
            cur = g.chain(cur, f"scale={W + 2 * m}:{H + 2 * m},crop={W}:{H}:x='{xe}':y='{ye}',setsar=1")

        elif t in ("glitch", "rgb_split"):
            amt = int(eff.get("amount", 14 if t == "glitch" else 8))
            if t == "glitch":
                rate = float(eff.get("rate", 7))
                en = f"{win}*gt(sin(t*{fnum(rate * 6.283)})*sin(t*{fnum(rate * 2.71)}+0.5),0.12)"
                en2 = f"{win}*gt(sin(t*{fnum(rate * 4.1)}+2),0.55)"
                cur = g.chain(cur, f"rgbashift=rh=-{amt}:bh={amt}:rv={amt // 3}:bv=-{amt // 3}:edge=smear:"
                                   f"enable='{en}',rgbashift=gh={amt // 2}:edge=wrap:enable='{en2}',"
                                   f"noise=alls=28:allf=t:enable='{en}',"
                                   f"eq=saturation=1.5:contrast=1.15:enable='{en2}',format=yuv420p")
            else:
                cur = g.chain(cur, f"rgbashift=rh=-{amt}:bh={amt}:edge=smear:enable='{win}',format=yuv420p")

        elif t in ("flash", "dip"):
            color = eff.get("color", "white" if t == "flash" else "black")
            fd = float(eff.get("dur", 0.25 if t == "flash" else 0.4))
            strength = float(eff.get("strength", 1.0))
            for a in _times(eff.get("at", 0)) or [0.0]:
                src_l = g.label("fl")
                g.add(f"color=c={ff_color(color)}:s={W}x{H}:r={fnum(fps)}:d={fnum(fd)},format=rgba,"
                      f"colorchannelmixer=aa={fnum(strength)},"
                      f"fade=t=out:st=0:d={fnum(fd)}:alpha=1,setpts=PTS+{fnum(a)}/TB[{src_l}]")
                out = g.label()
                g.add(f"[{cur}][{src_l}]overlay=eof_action=pass:repeatlast=0,format=yuv420p[{out}]")
                cur = out

        elif t == "film_grain":
            s = int(eff.get("strength", 10))
            cur = g.chain(cur, f"noise=c0s={s}:c0f=t+u")

        elif t == "vignette":
            cur = g.chain(cur, f"vignette=angle={fnum(float(eff.get('angle', 0.55)))}")

        elif t == "letterbox":
            b = eff.get("bars", 0.09)
            bpx = int(b * H) if float(b) < 1 else int(b)
            col = ff_color(eff.get("color", "black"))
            cur = g.chain(cur, f"drawbox=x=0:y=0:w=iw:h={bpx}:color={col}:t=fill,"
                               f"drawbox=x=0:y=ih-{bpx}:w=iw:h={bpx}:color={col}:t=fill")

        elif t == "lut":
            path = eff.get("path")
            if not path or not os.path.exists(path):
                raise SpecError(f"lut: .cube file not found: {path}")
            mix = float(eff.get("mix", 1.0))
            if mix >= 0.999:
                cur = g.chain(cur, f"lut3d=file={esc_filter_path(path)},format=yuv420p")
            else:
                a, b, l2, out = g.label(), g.label(), g.label(), g.label()
                g.add(f"[{cur}]split[{a}][{b}]")
                g.add(f"[{b}]lut3d=file={esc_filter_path(path)},format=yuv420p[{l2}]")
                g.add(f"[{l2}][{a}]blend=all_mode=normal:all_opacity={fnum(mix)},format=yuv420p[{out}]")
                cur = out

        elif t == "color":
            preset = eff.get("preset")
            parts = []
            if preset:
                if preset not in COLOR_PRESETS:
                    raise SpecError(f"unknown color preset {preset!r}. Valid: {', '.join(COLOR_PRESETS)}")
                parts.append(COLOR_PRESETS[preset])
            eqp = {k: eff[k] for k in ("contrast", "saturation", "brightness", "gamma") if k in eff}
            if eqp:
                parts.append("eq=" + ":".join(f"{k}={fnum(v)}" for k, v in eqp.items()))
            if not parts:
                raise SpecError("color effect needs a preset or contrast/saturation/brightness/gamma")
            f = ",".join(parts) + ",format=yuv420p"
            if "start" in eff or "end" in eff:  # timeline-limited grade
                f = ",".join(p + f":enable='{win}'" if not p.startswith("curves") else p
                             for p in parts) + ",format=yuv420p"
            cur = g.chain(cur, f)

        elif t == "blur":
            cur = g.chain(cur, f"gblur=sigma={fnum(float(eff.get('sigma', 12)))}:enable='{win}'")

        elif t == "sharpen":
            cur = g.chain(cur, f"unsharp=5:5:{fnum(float(eff.get('amount', 0.8)))}")

        elif t == "fade":
            fi = float(eff.get("in", 0) or 0)
            fo = float(eff.get("out", 0) or 0)
            col = eff.get("color", "black")
            fs = []
            if fi > 0:
                fs.append(f"fade=t=in:st=0:d={fnum(fi)}:color={ff_color(col)}")
            if fo > 0:
                fs.append(f"fade=t=out:st={fnum(max(0, dur - fo))}:d={fnum(fo)}:color={ff_color(col)}")
            cur = g.chain(cur, ",".join(fs))

        elif t == "mirror":
            cur = g.chain(cur, "hflip")
    return cur


# --------------------------------------------------------------------------------------
# clips
# --------------------------------------------------------------------------------------

def norm_clip(c, base: Path, role: str = "clip") -> dict:
    if c is None:
        raise SpecError(f"missing {role}")
    if isinstance(c, str):
        c = {"path": c}
    if not isinstance(c, dict):
        raise SpecError(f"{role} must be a path string or an object")
    c = dict(c)
    if "path" not in c and "color" not in c:
        raise SpecError(f"{role}: needs 'path' (video/image) or 'color' (solid card)")
    if "path" in c:
        p = Path(os.path.expanduser(str(c["path"])))
        if not p.is_absolute():
            p = (base / p).resolve()
        c["path"] = str(p)
        if not p.exists():
            raise SpecError(f"{role}: file not found: {p}")
    effs = []
    for e in c.get("effects", []) or []:
        e = {"type": e} if isinstance(e, str) else dict(e)
        if e.get("type") == "speed_ramp":
            c.setdefault("ramps", e.get("ramps") or [{k: e[k] for k in ("from", "to", "speed") if k in e}])
        elif e.get("type") == "blur_bg":
            c["fit"] = "blur_bg"
        else:
            if e.get("type") == "lut" and e.get("path") and not os.path.isabs(e["path"]):
                e["path"] = str((base / e["path"]).resolve())
            effs.append(e)
    c["effects"] = effs
    return c


def clip_info(c: dict) -> dict:
    if "path" not in c:
        return {"is_image": True, "has_audio": False, "duration": None, "width": None, "height": None}
    return probe(c["path"])


def clip_pieces(c: dict, info: dict) -> list[tuple[float, float, float]]:
    """Source-time pieces (start, end, speed) relative to clip 'in'."""
    t_in = sec(c.get("in", 0), "in")
    if info.get("is_image") or "path" not in c:
        return [(0.0, sec(c.get("duration", 3.0)), 1.0)]
    src_end = sec(c["out"], "out") if c.get("out") is not None else (info.get("duration") or 0)
    if src_end <= t_in:
        raise SpecError(f"clip {c.get('path')}: out ({src_end}) must be > in ({t_in}); file duration "
                        f"{info.get('duration')}")
    L = src_end - t_in
    base_speed = float(c.get("speed", 1.0))
    ramps = sorted(c.get("ramps") or [], key=lambda r: sec(r.get("from", 0)))
    pieces, cur = [], 0.0
    for r in ramps:
        a = max(0.0, sec(r.get("from", 0)) - t_in if r.get("absolute") else sec(r.get("from", 0)))
        b = min(L, sec(r.get("to", L)) - t_in if r.get("absolute") else sec(r.get("to", L)))
        if b <= a or a < cur:
            raise SpecError(f"speed_ramp ranges must be increasing and inside the clip: {r}")
        if a > cur:
            pieces.append((cur, a, base_speed))
        pieces.append((a, b, float(r.get("speed", 2.0))))
        cur = b
    if cur < L:
        pieces.append((cur, L, base_speed))
    return pieces


def clip_duration(c: dict) -> float:
    info = clip_info(c)
    if info.get("is_image") or "path" not in c:
        return sec(c.get("duration", 3.0))
    if c.get("duration") is not None and not c.get("ramps"):
        return sec(c["duration"])
    return sum((b - a) / s for a, b, s in clip_pieces(c, info))


def atempo_chain(speed: float) -> str:
    fs = []
    s = speed
    while s > 2.0:
        fs.append("atempo=2.0")
        s /= 2.0
    while s < 0.5:
        fs.append("atempo=0.5")
        s /= 0.5
    if abs(s - 1.0) > 1e-4:
        fs.append(f"atempo={fnum(s, 5)}")
    return ",".join(fs)


def add_clip(g: Graph, c: dict, bw: int, bh: int, dur: float, ctx: "Ctx", want_audio: bool = True
             ) -> tuple[str, str | None]:
    """Add a clip input, fit it into a bw x bh box, apply its effects, trim/pad to `dur`.
    Returns (video_label, audio_label or None)."""
    fps = ctx.fps
    info = clip_info(c)
    fit = c.get("fit", ctx.default_fit)
    if fit not in ("cover", "contain", "blur_bg", "stretch"):
        raise SpecError(f"fit must be cover/contain/blur_bg/stretch, got {fit!r}")
    bg = c.get("bg", ctx.background)

    if "path" not in c:  # solid color card
        v = g.label("c")
        g.add(f"color=c={ff_color(c['color'])}:s={bw}x{bh}:r={fnum(fps)}:d={fnum(dur)},format=yuv420p[{v}]")
        idx = None
        pieces = [(0, dur, 1.0)]
    elif info["is_image"]:
        idx = g.add_input(["-loop", "1", "-framerate", fnum(fps), "-t", fnum(dur + 0.5), "-i", c["path"]])
        v = g.chain(f"{idx}:v", "setpts=PTS-STARTPTS")
        pieces = [(0, dur, 1.0)]
    else:
        pieces = clip_pieces(c, info)
        t_in = sec(c.get("in", 0))
        src_len = pieces[-1][1] + 0.25
        idx = g.add_input(["-ss", fnum(t_in, 3), "-t", fnum(src_len, 3), "-i", c["path"]])
        if len(pieces) == 1:
            v = g.chain(f"{idx}:v", f"setpts=(PTS-STARTPTS)/{fnum(pieces[0][2], 5)}")
        else:
            labs = [g.label() for _ in pieces]
            g.add(f"[{idx}:v]split={len(pieces)}" + "".join(f"[{x}]" for x in labs))
            outs = []
            for lab, (a, b, s) in zip(labs, pieces):
                outs.append(g.chain(lab, f"trim=start={fnum(a)}:end={fnum(b)},setpts=(PTS-STARTPTS)/{fnum(s, 5)}"))
            v = g.label()
            g.add("".join(f"[{o}]" for o in outs) + f"concat=n={len(outs)}:v=1:a=0[{v}]")
        v = g.chain(v, f"fps={fnum(fps)}")

    # --- fit into the box
    fx, fy = (c.get("focus") or [0.5, 0.5])[:2]
    if "path" in c:
        if fit == "cover":
            v = g.chain(v, f"scale={bw}:{bh}:force_original_aspect_ratio=increase:flags=lanczos,"
                           f"crop={bw}:{bh}:x='(iw-ow)*{fnum(fx)}':y='(ih-oh)*{fnum(fy)}'")
        elif fit == "stretch":
            v = g.chain(v, f"scale={bw}:{bh}:flags=lanczos")
        elif fit == "contain":
            v = g.chain(v, f"scale={bw}:{bh}:force_original_aspect_ratio=decrease:flags=lanczos,"
                           f"pad={bw}:{bh}:(ow-iw)/2:(oh-ih)/2:color={ff_color(bg)}")
        else:  # blur_bg
            a, b = g.label(), g.label()
            g.add(f"[{v}]split[{a}][{b}]")
            bgl = g.chain(a, f"scale={even(bw / 8)}:{even(bh / 8)}:force_original_aspect_ratio=increase,"
                             f"crop={even(bw / 8)}:{even(bh / 8)},boxblur=8:3,"
                             f"scale={bw}:{bh}:flags=bicubic,eq=brightness=-0.07:saturation=1.1")
            fgl = g.chain(b, f"scale={bw}:{bh}:force_original_aspect_ratio=decrease:flags=lanczos")
            v = g.label()
            g.add(f"[{bgl}][{fgl}]overlay=(W-w)/2:(H-h)/2[{v}]")
    v = g.chain(v, "setsar=1,format=yuv420p")
    v = apply_effects(g, v, c.get("effects"), bw, bh, fps, dur)
    v = g.chain(v, f"tpad=stop_mode=clone:stop_duration={fnum(dur + 1)},trim=duration={fnum(dur)},"
                   f"setpts=PTS-STARTPTS,format=yuv420p")

    if not want_audio:
        return v, None
    a = None
    vol = float(c.get("volume", 1.0))
    if idx is not None and info.get("has_audio") and not c.get("mute") and not info.get("is_image") and vol > 0:
        if len(pieces) == 1:
            tempo = atempo_chain(pieces[0][2])
            a = g.chain(f"{idx}:a", "asetpts=PTS-STARTPTS" + ("," + tempo if tempo else ""), "a")
        else:
            labs = [g.label("a") for _ in pieces]
            g.add(f"[{idx}:a]asplit={len(pieces)}" + "".join(f"[{x}]" for x in labs))
            outs = []
            for lab, (s0, s1, s) in zip(labs, pieces):
                tempo = atempo_chain(s)
                outs.append(g.chain(lab, f"atrim=start={fnum(s0)}:end={fnum(s1)},asetpts=PTS-STARTPTS"
                                         + ("," + tempo if tempo else ""), "a"))
            a = g.label("a")
            g.add("".join(f"[{o}]" for o in outs) + f"concat=n={len(outs)}:v=0:a=1[{a}]")
        a = g.chain(a, f"volume={fnum(vol)},aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
                       f"apad,atrim=duration={fnum(dur)}", "a")
    else:
        a = g.label("a")
        g.add(f"anullsrc=channel_layout=stereo:sample_rate=48000,atrim=duration={fnum(dur)},"
              f"aformat=sample_fmts=fltp:channel_layouts=stereo[{a}]")
    return v, a


def silent(g: Graph, dur: float) -> str:
    a = g.label("a")
    g.add(f"anullsrc=channel_layout=stereo:sample_rate=48000,atrim=duration={fnum(dur)},"
          f"aformat=sample_fmts=fltp:channel_layouts=stereo[{a}]")
    return a


def mix_audio(g: Graph, labels: list[str], dur: float) -> str:
    if len(labels) == 1:
        return labels[0]
    out = g.label("a")
    g.add("".join(f"[{x}]" for x in labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,"
          f"atrim=duration={fnum(dur)}[{out}]")
    return out


# --------------------------------------------------------------------------------------
# context & text events
# --------------------------------------------------------------------------------------

class Ctx:
    def __init__(self, spec: dict, base: Path):
        cv = spec.get("canvas", {}) or {}
        self.W = even(cv.get("width", 1080))
        self.H = even(cv.get("height", 1920))
        self.fps = float(cv.get("fps", 30))
        self.background = cv.get("background", "#000000")
        self.default_fit = (spec.get("defaults") or {}).get("fit", "cover")
        self.font = (spec.get("defaults") or {}).get("font", "Heebo")
        self.base = base
        self.sx = self.W / 1080.0
        self.sy = self.H / 1920.0

    def X(self, v: float) -> int:
        return int(round(v * self.sx))

    def Y(self, v: float) -> int:
        return int(round(v * self.sy))


NAMED_Y = {"top": 330, "upper": 560, "center": 960, "middle": 960, "lower": 1340, "bottom": 1540,
           "title": 330, "cta": 1480}


def resolve_xy(ov: dict, ctx: Ctx) -> tuple[int, int, int]:
    """Returns (x, y, ass_alignment). Coordinates are canvas pixels (1080x1920 reference scaled)."""
    an = int(ov.get("align", 5))
    pos = ov.get("position")
    x = ov.get("x")
    y = ov.get("y")
    if pos and isinstance(pos, str):
        if pos not in NAMED_Y:
            raise SpecError(f"unknown text position {pos!r}. Valid: {', '.join(NAMED_Y)} or x/y")
        y = ctx.Y(NAMED_Y[pos]) if y is None else y
    if isinstance(pos, (list, tuple)):
        x, y = pos[0], pos[1]
    x = ctx.W // 2 if x is None else (int(float(x) * ctx.W) if 0 < float(x) <= 1 and isinstance(x, float) else int(x))
    y = ctx.Y(960) if y is None else (int(float(y) * ctx.H) if 0 < float(y) <= 1 and isinstance(y, float) else int(y))
    return x, y, an


class TextEvent:
    __slots__ = ("start", "end", "style", "text", "layer")

    def __init__(self, start, end, style, text, layer=0):
        self.start, self.end, self.style, self.text, self.layer = start, end, style, text, layer

    def shifted(self, dt: float) -> "TextEvent":
        return TextEvent(self.start + dt, self.end + dt, self.style, self.text, self.layer)

    def line(self) -> str:
        return (f"Dialogue: {self.layer},{ass_time(self.start)},{ass_time(self.end)},{self.style},,0,0,0,,"
                f"{self.text}")


ANIMS = ["none", "fade", "pop", "slide_up", "typewriter", "zoom_in"]


def text_overlay_events(ov: dict, ctx: Ctx, seg_dur: float | None = None) -> list[TextEvent]:
    """Overlay spec (type text/chip/cta/title) -> ASS events in the overlay's own time base."""
    t = ov.get("type", "text")
    style_name = {"chip": "Chip", "label": "Chip"}.get(t, "Text")
    raw = str(ov.get("text", ""))
    if not raw:
        raise SpecError(f"{t} overlay needs 'text'")
    start = sec(ov.get("start", 0))
    end = sec(ov["end"]) if ov.get("end") is not None else (
        start + sec(ov["dur"]) if ov.get("dur") is not None else (seg_dur if seg_dur is not None else start + 3))
    if end <= start:
        raise SpecError(f"text overlay {raw[:30]!r}: end must be > start")
    x, y, an = resolve_xy(ov, ctx)
    if t in ("chip", "label") and "align" not in ov and ov.get("x") is not None:
        an = 7
    box = bool(ov.get("box", t in ("chip", "label")))
    if box:
        style_name = "Chip"
    size = ov.get("size", {"chip": 34, "label": 34, "title": 84, "cta": 64}.get(t, 72))
    weight = int(ov.get("weight", 800 if t != "chip" else 700))
    font = ov.get("font", ctx.font)
    color = ov.get("color", "white")
    stroke = ov.get("stroke", 0 if box else 6)
    stroke_color = ov.get("stroke_color", ov.get("box_color", "#000000B0") if box else "black")
    shadow = ov.get("shadow", 0 if box else 2)
    tags = [f"\\an{an}", f"\\fn{font}", f"\\fs{int(size * ctx.sy)}", f"\\b{weight}",
            f"\\1c{ass_color(color)}", f"\\1a{ass_alpha(color)}",
            f"\\3c{ass_color(stroke_color)}", f"\\3a{ass_alpha(stroke_color)}",
            f"\\bord{fnum(stroke * ctx.sy if not box else ov.get('pad', 12) * ctx.sy)}",
            f"\\shad{fnum(shadow)}", f"\\4c&H000000&\\4a&H80&"]
    if ov.get("rotate"):
        tags.append(f"\\frz{fnum(ov['rotate'])}")
    if ov.get("spacing"):
        tags.append(f"\\fsp{fnum(ov['spacing'])}")
    anim = ov.get("anim", "fade")
    if anim not in ANIMS:
        raise SpecError(f"unknown anim {anim!r}. Valid: {', '.join(ANIMS)}")
    ms = int((end - start) * 1000)
    pos = f"\\pos({x},{y})"
    if anim == "fade":
        tags.append(f"\\fad({min(150, ms // 4)},{min(150, ms // 4)})")
    elif anim == "pop":
        tags += ["\\fscx40\\fscy40\\t(0,110,\\fscx112\\fscy112)\\t(110,190,\\fscx100\\fscy100)",
                 f"\\fad(40,{min(120, ms // 4)})"]
    elif anim == "zoom_in":
        tags += [f"\\fscx100\\fscy100\\t(0,{ms},\\fscx118\\fscy118)", f"\\fad(120,{min(150, ms // 4)})"]
    elif anim == "slide_up":
        pos = f"\\move({x},{y + ctx.Y(70)},{x},{y},0,220)"
        tags.append(f"\\fad(120,{min(150, ms // 4)})")
    direction = ov.get("dir", "auto")
    text = ass_escape(raw)
    if ov.get("highlight"):  # words to color with highlight_color
        hc = ass_color(ov.get("highlight_color", "yellow"))
        for wd in ov["highlight"] if isinstance(ov["highlight"], list) else [ov["highlight"]]:
            text = text.replace(wd, f"{{\\1c{hc}}}{wd}{{\\1c{ass_color(color)}}}")
    layer = int(ov.get("layer", 5 if t in ("chip", "label") else 4))
    if anim == "typewriter":
        evs = []
        chars = list(raw)
        n = len(chars)
        tdur = min(float(ov.get("type_dur", 0.05 * n)), (end - start) * 0.8)
        steps = min(n, 60)
        for i in range(1, steps + 1):
            k = int(round(i * n / steps))
            s0 = start + tdur * (i - 1) / steps
            s1 = start + tdur * i / steps if i < steps else end
            part = rtl_fix(ass_escape("".join(chars[:k])), direction)
            evs.append(TextEvent(s0, s1, style_name, "{" + "".join(tags) + pos + "}" + part, layer))
        return evs
    return [TextEvent(start, end, style_name, "{" + "".join(tags) + pos + "}" + rtl_fix(text, direction), layer)]


def chip(text: str, x: int, y: int, start: float, end: float, ctx: Ctx, **kw) -> dict:
    d = {"type": "chip", "text": text, "x": x, "y": y, "start": start, "end": end, "anim": "fade"}
    d.update(kw)
    return d


# --------------------------------------------------------------------------------------
# layouts
# --------------------------------------------------------------------------------------

class SegPlan:
    def __init__(self):
        self.g = Graph("s")
        self.v = ""
        self.a = ""
        self.dur = 0.0
        self.overlays: list[dict] = []        # overlay dicts, times relative to the segment
        self.events: list[TextEvent] = []     # prebuilt ASS events, relative times
        self.layout = ""


LAYOUTS = ["full", "split_vertical", "split_horizontal", "split_wipe", "before_after_slider",
           "input_prompt_result", "pip", "reveal"]
REVEAL_MODES = ["wipe", "slider", "split", "split_vertical", "cut"]


def expand_reveal(seg: dict) -> dict:
    """'reveal' = blocks->reality: a blockout/greybox clip turns into the AI render.

    Keys: blockout, real (clip specs; time-aligned, same 'in'), mode wipe|slider|split|split_vertical|cut,
    at (s, when the reveal starts), wipe_dur, direction, labels {blockout, real}, flash (bool),
    glitch (bool). Expands into one of the other layouts plus effects.
    """
    s = {k: v for k, v in seg.items() if k not in ("blockout", "real", "mode", "flash", "glitch")}
    mode = seg.get("mode", "wipe")
    if mode not in REVEAL_MODES:
        raise SpecError(f"reveal mode must be one of {', '.join(REVEAL_MODES)}, got {mode!r}")
    if seg.get("blockout") is None or seg.get("real") is None:
        raise SpecError("reveal layout needs 'blockout' and 'real' clips")
    lab = seg.get("labels", {"blockout": "BLOCKOUT", "real": "AI RENDER"}) or {}
    effects = list(seg.get("effects") or [])
    at = seg.get("at")
    if mode in ("wipe", "slider"):
        s["layout"] = "split_wipe" if mode == "wipe" else "before_after_slider"
        s["before"], s["after"] = seg["blockout"], seg["real"]
        s["labels"] = {"before": lab.get("blockout"), "after": lab.get("real")}
        s.setdefault("audio", "after")
    elif mode in ("split", "split_vertical"):
        horiz = mode == "split"
        k1, k2 = ("left", "right") if horiz else ("top", "bottom")
        s["layout"] = "split_horizontal" if horiz else "split_vertical"
        s[k1], s[k2] = seg["blockout"], seg["real"]
        s["labels"] = {k1: lab.get("blockout"), k2: lab.get("real")}
        s.setdefault("audio", k2)
    else:  # hard cut from blockout to real at 'at' (same timeline => perfect match cut)
        s["layout"] = "split_wipe"
        s["before"], s["after"] = seg["blockout"], seg["real"]
        a = sec(at if at is not None else 1.0)
        s["keys"] = [[0, 0], [a, 0], [a + 0.001, 1]]
        s["line"] = False
        s["labels"] = {"before": lab.get("blockout"), "after": lab.get("real")}
        s.setdefault("audio", "after")
    if mode != "cut" and at is not None:
        s["at"] = at
    hit = sec(at if at is not None else 1.0)
    if mode in ("split", "split_vertical", "slider"):
        hit = sec(at) if at is not None else 0.0
    if seg.get("glitch"):
        effects.append({"type": "glitch", "start": max(0.0, hit - 0.15), "end": hit + 0.35})
    if seg.get("flash"):
        flash_at = hit + (sec(seg.get("wipe_dur", 0.6)) if mode == "wipe" else 0.0)
        effects.append({"type": "flash", "at": flash_at, "dur": 0.3, "strength": 0.8})
    if effects:
        s["effects"] = effects
    return s


def seg_duration(seg: dict, primary: dict, others: list[dict], fps: float) -> float:
    if seg.get("duration") is not None:
        d = sec(seg["duration"])
    else:
        d = clip_duration(primary)
    frames = max(1, int(round(d * fps)))
    return frames / fps


def piecewise_expr(keys: list, var: str = "t", ease: bool = True) -> str:
    """[[t,p],...] -> ffmpeg expression for a smooth piecewise function of `var`."""
    keys = sorted([(sec(k[0]), float(k[1])) for k in keys])
    if not keys:
        return "0.5"
    expr = fnum(keys[-1][1])
    for (t0, p0), (t1, p1) in reversed(list(zip(keys, keys[1:]))):
        if t1 <= t0:
            continue
        u = f"(({var}-{fnum(t0)})/{fnum(t1 - t0)})"
        e = f"({u}*{u}*(3-2*{u}))" if ease else u
        expr = f"if(lt({var},{fnum(t1)}),{fnum(p0)}+({fnum(p1 - p0)})*{e},{expr})"
    return f"if(lt({var},{fnum(keys[0][0])}),{fnum(keys[0][1])},{expr})"


def build_segment(seg: dict, ctx: Ctx) -> SegPlan:
    layout = seg.get("layout", "full")
    if layout not in LAYOUTS:
        raise SpecError(f"unknown layout {layout!r}. Valid: {', '.join(LAYOUTS)}")
    if layout == "reveal":
        P = build_segment(expand_reveal(seg), ctx)
        P.layout = f"reveal/{seg.get('mode', 'wipe')}"
        return P
    P = SegPlan()
    P.layout = layout
    g = P.g
    W, H, fps = ctx.W, ctx.H, ctx.fps
    base = ctx.base
    label_kw = dict(seg.get("label_style") or {})

    if layout == "full":
        c = norm_clip(seg.get("clip"), base, "clip")
        P.dur = seg_duration(seg, c, [], fps)
        P.v, P.a = add_clip(g, c, W, H, P.dur, ctx)

    elif layout == "pip":
        main = norm_clip(seg.get("main"), base, "main")
        inset = norm_clip(seg.get("inset"), base, "inset")
        P.dur = seg_duration(seg, main, [inset], fps)
        size = float(seg.get("size", 0.38))
        asp = seg.get("inset_aspect", "9:16")
        aw, ah = [float(x) for x in str(asp).split(":")]
        iw = even(W * size)
        ih = even(iw * ah / aw)
        border = int(seg.get("border", 6))
        bcol = seg.get("border_color", "white")
        mv, ma = add_clip(g, main, W, H, P.dur, ctx)
        iv, ia = add_clip(g, inset, iw, ih, P.dur, ctx)
        if border > 0:
            iv = g.chain(iv, f"pad={iw + 2 * border}:{ih + 2 * border}:{border}:{border}:color={ff_color(bcol)}")
        m = ctx.X(int(seg.get("margin", 48)))
        corner = seg.get("corner", "top_right")
        tw, th = iw + 2 * border, ih + 2 * border
        xs = {"left": m, "right": W - tw - m, "center": (W - tw) // 2}
        ys = {"top": ctx.Y(280), "bottom": ctx.Y(1580) - th, "middle": (H - th) // 2}
        try:
            vpos, hpos = corner.split("_") if "_" in corner else ("middle", corner)
            px, py = xs[hpos], ys[vpos]
        except (KeyError, ValueError):
            raise SpecError("pip corner must be top_left/top_right/bottom_left/bottom_right/middle_center")
        if seg.get("x") is not None:
            px, py = int(seg["x"]), int(seg["y"])
        P.v = g.label()
        g.add(f"[{mv}][{iv}]overlay={px}:{py}:shortest=1[{P.v}]")
        am = seg.get("audio", "main")
        P.a = {"main": ma, "inset": ia}.get(am) or mix_audio(g, [ma, ia], P.dur)
        if seg.get("inset_label"):
            P.overlays.append(chip(seg["inset_label"], px + ctx.X(14), py + ctx.Y(14), 0, P.dur, ctx, **label_kw))

    elif layout in ("split_vertical", "split_horizontal"):
        horiz = layout == "split_horizontal"
        k1, k2 = ("left", "right") if horiz else ("top", "bottom")
        c1 = norm_clip(seg.get(k1), base, k1)
        c2 = norm_clip(seg.get(k2), base, k2)
        P.dur = seg_duration(seg, c1, [c2], fps)
        ratio = float(seg.get("ratio", 0.5))
        if horiz:
            w1 = even(W * ratio)
            b1, b2 = (w1, H), (W - w1, H)
        else:
            h1 = even(H * ratio)
            b1, b2 = (W, h1), (W, H - h1)
        v1, a1 = add_clip(g, c1, b1[0], b1[1], P.dur, ctx)
        v2, a2 = add_clip(g, c2, b2[0], b2[1], P.dur, ctx)
        P.v = g.label()
        g.add(f"[{v1}][{v2}]{'hstack' if horiz else 'vstack'}=inputs=2[{P.v}]")
        div = seg.get("divider", {"width": 6, "color": "white"})
        if div:
            dw = int(div.get("width", 6))
            col = ff_color(div.get("color", "white"))
            if horiz:
                P.v = g.chain(P.v, f"drawbox=x={b1[0] - dw // 2}:y=0:w={dw}:h=ih:color={col}:t=fill")
            else:
                P.v = g.chain(P.v, f"drawbox=x=0:y={b1[1] - dw // 2}:w=iw:h={dw}:color={col}:t=fill")
        aud = seg.get("audio", k2)
        P.a = {k1: a1, k2: a2, "none": None}.get(aud, "mix")
        if P.a == "mix":
            P.a = mix_audio(g, [a1, a2], P.dur)
        elif P.a is None:
            P.a = silent(g, P.dur)
        labels = seg.get("labels") or {}
        lx = ctx.X(48)
        if horiz:
            pos1, pos2 = (lx, ctx.Y(290)), (b1[0] + lx, ctx.Y(290))
        else:
            pos1 = (lx, max(ctx.Y(290), ctx.Y(40)) if b1[1] > ctx.Y(600) else ctx.Y(40))
            pos2 = (lx, b1[1] + ctx.Y(36))
        if labels.get(k1):
            P.overlays.append(chip(labels[k1], *pos1, 0, P.dur, ctx, **label_kw))
        if labels.get(k2):
            P.overlays.append(chip(labels[k2], *pos2, 0, P.dur, ctx, **label_kw))

    elif layout in ("split_wipe", "before_after_slider"):
        before = norm_clip(seg.get("before"), base, "before")
        after = norm_clip(seg.get("after"), base, "after")
        P.dur = seg_duration(seg, after, [before], fps)
        vb, ab = add_clip(g, before, W, H, P.dur, ctx)
        va, aa = add_clip(g, after, W, H, P.dur, ctx)
        direction = seg.get("direction", "right")  # where the line travels to
        if direction not in ("right", "left", "down", "up"):
            raise SpecError("direction must be right/left/down/up")
        vertical_line = direction in ("right", "left")
        if layout == "split_wipe":
            at = sec(seg.get("at", min(1.0, P.dur / 3)))
            wd = sec(seg.get("wipe_dur", 0.6))
            keys = seg.get("keys") or [[0, 0], [at, 0], [at + wd, 1]]
        else:
            D = P.dur
            keys = seg.get("keys") or [[0, 0.5], [D * 0.25, 0.12], [D * 0.62, 0.88], [D, 0.5]]
        p = piecewise_expr(keys, "t", ease=seg.get("ease", True))
        # mask: white = AFTER visible. right: after occupies [0, p*W]; left: [(1-p)W, W]
        if direction == "right":
            mx, my, lx_e, ly_e = f"({p}-1)*W", "0", f"({p})*W", None
        elif direction == "left":
            mx, my, lx_e, ly_e = f"(1-{p})*W", "0", f"(1-{p})*W", None
        elif direction == "down":
            mx, my, lx_e, ly_e = "0", f"({p}-1)*H", None, f"({p})*H"
        else:
            mx, my, lx_e, ly_e = "0", f"(1-{p})*H", None, f"(1-{p})*H"
        mb, mw, mask = g.label("m"), g.label("m"), g.label("m")
        g.add(f"color=c=black:s={W}x{H}:r={fnum(fps)}:d={fnum(P.dur)},format=gray[{mb}]")
        g.add(f"color=c=white:s={W}x{H}:r={fnum(fps)}:d={fnum(P.dur)},format=gray[{mw}]")
        g.add(f"[{mb}][{mw}]overlay=x='{mx}':y='{my}':eval=frame,format=gray[{mask}]")
        va2 = g.chain(va, "format=yuva420p")
        am = g.label()
        g.add(f"[{va2}][{mask}]alphamerge[{am}]")
        comp = g.label()
        g.add(f"[{vb}][{am}]overlay=0:0:shortest=1,format=yuv420p[{comp}]")
        line = seg.get("line", {})
        if line is True or line is None:
            line = {}
        if line is not False:
            lw = int(line.get("width", 8))
            lcol = line.get("color", "white")
            glow = line.get("glow", True)
            cur = comp
            # a finished/unstarted wipe parks the line at the frame edge: only show it while moving
            line_en = ""
            if layout == "split_wipe" and not seg.get("keys"):
                line_en = f":enable='between(t,{fnum(max(0, at - 0.04))},{fnum(at + wd + 0.04)})'"
            for gw, ga in ([(lw * 5, 0.22), (lw * 2.5, 0.35)] if glow else []) + [(lw, 1.0)]:
                gw = even(gw)
                r, gg, b, _ = parse_color(lcol)
                bar = g.label("b")
                size = f"{gw}x{H}" if vertical_line else f"{W}x{gw}"
                g.add(f"color=c=0x{r:02X}{gg:02X}{b:02X}@{fnum(ga)}:s={size}:r={fnum(fps)}:d={fnum(P.dur)},"
                      f"format=rgba[{bar}]")
                out = g.label()
                if vertical_line:
                    g.add(f"[{cur}][{bar}]overlay=x='{lx_e}-{gw // 2}':y=0:eval=frame:shortest=1{line_en}[{out}]")
                else:
                    g.add(f"[{cur}][{bar}]overlay=x=0:y='{ly_e}-{gw // 2}':eval=frame:shortest=1{line_en}[{out}]")
                cur = out
            comp = cur
        P.v = g.chain(comp, "format=yuv420p")
        aud = seg.get("audio", "after" if layout == "split_wipe" else "before")
        P.a = {"before": ab, "after": aa}.get(aud) or mix_audio(g, [ab, aa], P.dur)
        labels = seg.get("labels") or {}
        lx = ctx.X(48)
        if vertical_line:
            after_side, before_side = (("left", "right") if direction == "right" else ("right", "left"))
            px = {"left": lx, "right": W - ctx.X(48)}
            ty = ctx.Y(290)
            if labels.get("before"):
                P.overlays.append(chip(labels["before"], px[before_side], ty, 0, P.dur, ctx,
                                       align=9 if before_side == "right" else 7, **label_kw))
            if labels.get("after"):
                P.overlays.append(chip(labels["after"], px[after_side], ty, 0, P.dur, ctx,
                                       align=9 if after_side == "right" else 7, **label_kw))
        else:
            if labels.get("after"):
                P.overlays.append(chip(labels["after"], lx, ctx.Y(290) if direction == "down" else ctx.Y(1000),
                                       0, P.dur, ctx, **label_kw))
            if labels.get("before"):
                P.overlays.append(chip(labels["before"], lx, ctx.Y(1000) if direction == "down" else ctx.Y(290),
                                       0, P.dur, ctx, **label_kw))

    elif layout == "input_prompt_result":
        res = norm_clip(seg.get("result"), base, "result")
        P.dur = seg_duration(seg, res, [], fps)
        # geometry (1080x1920 reference)
        rx, ry, rw, rh = 0, ctx.Y(220), W, even(ctx.Y(880))
        bgmode = seg.get("background", "blur")
        if bgmode == "blur":
            bgc = dict(res)
            bgc["effects"] = []
            bgc["fit"] = "cover"
            bv, _ = add_clip(g, bgc, even(W / 8), even(H / 8), P.dur, ctx, want_audio=False)
            bv = g.chain(bv, f"boxblur=6:3,scale={W}:{H}:flags=bicubic,eq=brightness=-0.22:saturation=0.8")
        else:
            bv = g.label("c")
            g.add(f"color=c={ff_color(bgmode)}:s={W}x{H}:r={fnum(fps)}:d={fnum(P.dur)},format=yuv420p[{bv}]")
        res_v, res_a = add_clip(g, res, rw, rh, P.dur, ctx)
        cur = g.label()
        g.add(f"[{bv}][{res_v}]overlay={rx}:{ry}:shortest=1[{cur}]")
        # input image / video
        ix, iy, isz = ctx.X(48), ctx.Y(1262), ctx.X(int(seg.get("input_size", 320)))
        isz = even(isz)
        if seg.get("input"):
            inp = norm_clip(seg.get("input"), base, "input")
            inp.setdefault("fit", "cover")
            iv, ia = add_clip(g, inp, isz, isz, P.dur, ctx, want_audio=False)
            iv = g.chain(iv, f"pad={isz + 8}:{isz + 8}:4:4:color=white")
            out = g.label()
            g.add(f"[{cur}][{iv}]overlay={ix - 4}:{iy - 4}:shortest=1[{out}]")
            cur = out
            px0 = ix + isz + ctx.X(36)
        else:
            px0 = ctx.X(48)
        # prompt panel background
        pw = W - px0 - ctx.X(40)
        py0, py1 = ctx.Y(1262), ctx.Y(1262) + isz if seg.get("input") else ctx.Y(1262) + ctx.Y(340)
        py1 = max(py1, py0 + ctx.Y(300))
        cur = g.chain(cur, f"drawbox=x={px0 - 14}:y={py0 - 10}:w={pw + 28}:h={py1 - py0 + 20}:"
                           f"color=0x000000@0.55:t=fill")
        P.v = g.chain(cur, "format=yuv420p")
        P.a = res_a
        labels = seg.get("labels", {"input": "INPUT", "prompt": "PROMPT", "result": "RESULT"}) or {}
        chip_y = py0 - ctx.Y(56)
        if labels.get("result"):
            P.overlays.append(chip(labels["result"], ctx.X(48), ry + ctx.Y(28), 0, P.dur, ctx, **label_kw))
        if labels.get("input") and seg.get("input"):
            P.overlays.append(chip(labels["input"], ix, chip_y, 0, P.dur, ctx, **label_kw))
        if labels.get("prompt"):
            P.overlays.append(chip(labels["prompt"], px0 - 14, chip_y, 0, P.dur, ctx, **label_kw))
        if seg.get("title"):
            tov = {"type": "text", "text": seg["title"], "x": W // 2, "y": ctx.Y(1160), "size": 50,
                   "weight": 900, "start": 0, "end": P.dur, "anim": "fade"}
            tov.update(seg.get("title_style") or {})
            P.overlays.append(tov)
        P.events += prompt_scroll_events(seg, ctx, px0, py0, pw, py1, P.dur)

    # segment-level effects on the composed canvas
    if seg.get("effects"):
        effs = []
        for e in seg["effects"]:
            e = {"type": e} if isinstance(e, str) else dict(e)
            if e.get("type") == "lut" and e.get("path") and not os.path.isabs(e["path"]):
                e["path"] = str((base / e["path"]).resolve())
            effs.append(e)
        P.v = apply_effects(g, P.v, effs, W, H, fps, P.dur)
    P.v = g.chain(P.v, f"trim=duration={fnum(P.dur)},setpts=PTS-STARTPTS,format=yuv420p")
    for ov in seg.get("overlays", []) or []:
        P.overlays.append(dict(ov))
    return P


TC_RE = re.compile(r"^\s*\[?\s*(\d{1,2}):(\d{2}(?:[.,]\d+)?)(?:\s*[-–—]\s*(\d{1,2}):(\d{2}(?:[.,]\d+)?))?\s*\]?")


def prompt_scroll_events(seg: dict, ctx: Ctx, x0: int, y0: int, w: int, y1: int, dur: float) -> list[TextEvent]:
    """Scrolling monospace prompt inside a clip rectangle; optional timecode sync."""
    pr = seg.get("prompt")
    if not pr:
        return []
    if isinstance(pr, str):
        pr = {"text": pr}
    text = pr.get("text")
    if pr.get("file"):
        fp = Path(pr["file"])
        fp = fp if fp.is_absolute() else ctx.base / fp
        text = fp.read_text(encoding="utf-8")
    if not text:
        return []
    fs = int(pr.get("font_size", 26) * ctx.sy)
    lh = int(round(fs * float(pr.get("line_height", 1.38))))
    font = pr.get("font", mono_font())
    cw = fs * 0.602
    ncols = max(10, int(w / cw))
    lines: list[tuple[str, float | None]] = []
    for para in text.strip().splitlines():
        m = TC_RE.match(para)
        tc = None
        if m:
            tc = int(m.group(1)) * 60 + float(m.group(2).replace(",", "."))
        wrapped = textwrap.wrap(para, ncols) or [""]
        for i, wl in enumerate(wrapped):
            lines.append((wl, tc if i == 0 else None))
        if pr.get("blank_between", False):
            lines.append(("", None))
    total_h = len(lines) * lh
    win_h = y1 - y0
    max_off = max(0, total_h - lh * 2)
    mode = pr.get("scroll", "auto")
    tscale = float(pr.get("time_scale", 1.0))
    toff = float(pr.get("offset", 0.0))
    keys: list[tuple[float, float]] = [(0.0, 0.0)]
    if mode == "timecodes" and any(tc is not None for _, tc in lines):
        for i, (_, tc) in enumerate(lines):
            if tc is None:
                continue
            t = tc * tscale + toff
            if t <= 0 or t >= dur:
                continue
            target = min(i * lh, max_off)
            t0 = max(keys[-1][0], t - 0.3)
            keys.append((t0, keys[-1][1]))
            keys.append((t, float(target)))
        keys.append((dur, keys[-1][1]))
    elif mode == "none" or total_h <= win_h:
        keys.append((dur, 0.0))
    else:
        hold = min(0.8, dur * 0.1)
        keys += [(hold, 0.0), (max(hold + 0.1, dur - 0.4), float(max(0, total_h - win_h + lh * 0.5))),
                 (dur, float(max(0, total_h - win_h + lh * 0.5)))]
    # merge into intervals
    evs: list[TextEvent] = []
    color = ass_color(pr.get("color", "#E8E8E8"))
    tc_color = ass_color(pr.get("timecode_color", "#FFD84A"))
    clip = f"\\clip({x0 - 6},{y0},{x0 + w + 6},{y1})"
    base_tags = f"\\an7\\fn{font}\\fs{fs}\\b400\\bord0\\shad0\\1c{color}{clip}"
    for (ta, oa), (tb, ob) in zip(keys, keys[1:]):
        if tb - ta < 0.02:
            continue
        for i, (ln, tc) in enumerate(lines):
            ya, yb = y0 + i * lh - oa, y0 + i * lh - ob
            if max(ya, yb) < y0 - lh or min(ya, yb) > y1:
                continue
            body = ass_escape(ln)
            m = TC_RE.match(ln) if tc is not None else None
            if m:
                body = f"{{\\1c{tc_color}\\b700}}{ass_escape(ln[:m.end()])}{{\\1c{color}\\b400}}{ass_escape(ln[m.end():])}"
            if abs(ya - yb) < 0.5:
                pos = f"\\pos({x0},{int(round(ya))})"
            else:
                pos = f"\\move({x0},{int(round(ya))},{x0},{int(round(yb))},0,{int((tb - ta) * 1000)})"
            evs.append(TextEvent(ta, tb, "Prompt", "{" + base_tags + pos + "}" + body, 3))
    if mode == "timecodes" and pr.get("highlight", True):
        evs.append(TextEvent(0, dur, "Prompt",
                             f"{{\\an7\\pos({x0 - 8},{y0 - 2})\\p1\\bord0\\shad0\\1c&HFFFFFF&\\1a&HD8&}}"
                             f"m 0 0 l {w + 16} 0 {w + 16} {lh} 0 {lh}{{\\p0}}", 2))
    return evs


# --------------------------------------------------------------------------------------
# captions
# --------------------------------------------------------------------------------------

CAPTION_STYLES = {
    "clean":          {"size": 58, "weight": 700, "max_words": 7, "max_chars": 30, "stroke": 4, "anim": "fade"},
    "bold_pop":       {"size": 96, "weight": 900, "max_words": 2, "max_chars": 14, "stroke": 8, "anim": "pop"},
    "highlight_word": {"size": 78, "weight": 900, "max_words": 4, "max_chars": 22, "stroke": 7, "anim": "none"},
    "karaoke":        {"size": 76, "weight": 900, "max_words": 4, "max_chars": 22, "stroke": 7, "anim": "none"},
}


def parse_srt(path: str) -> list[dict]:
    txt = Path(path).read_text(encoding="utf-8-sig")
    out = []
    for block in re.split(r"\n\s*\n", txt.strip()):
        lines = [ln for ln in block.splitlines() if ln.strip()]
        for i, ln in enumerate(lines):
            m = re.match(r"(\d+:\d+:\d+[,.]\d+)\s*-->\s*(\d+:\d+:\d+[,.]\d+)", ln)
            if m:
                out.append({"start": sec(m.group(1).replace(",", ".")), "end": sec(m.group(2).replace(",", ".")),
                            "text": " ".join(lines[i + 1:])})
                break
    return out


def lines_to_words(lines: list[dict]) -> list[dict]:
    """Phrase-level lines -> approximate word timings (proportional to word length)."""
    words = []
    for ln in lines:
        toks = ln["text"].split()
        if not toks:
            continue
        total = sum(len(t) + 1 for t in toks)
        t = ln["start"]
        span = ln["end"] - ln["start"]
        for tok in toks:
            d = span * (len(tok) + 1) / total
            words.append({"start": t, "end": t + d, "text": tok, "_line": id(ln)})
            t += d
    return words


def group_words(words: list[dict], max_words: int, max_chars: int, max_gap: float = 0.55) -> list[list[dict]]:
    groups, cur = [], []
    for w in words:
        if cur:
            chars = sum(len(x["text"]) + 1 for x in cur) + len(w["text"])
            brk = (len(cur) >= max_words or chars > max_chars or w["start"] - cur[-1]["end"] > max_gap
                   or re.search(r"[.!?׃:;,]$", cur[-1]["text"])
                   or (w.get("_line") is not None and w.get("_line") != cur[-1].get("_line")))
            if brk:
                groups.append(cur)
                cur = []
        cur.append(w)
    if cur:
        groups.append(cur)
    return groups


def caption_events(cap: dict, words: list[dict], ctx: Ctx, total: float) -> list[TextEvent]:
    style = cap.get("style", "bold_pop")
    if style not in CAPTION_STYLES:
        raise SpecError(f"unknown caption style {style!r}. Valid: {', '.join(CAPTION_STYLES)}")
    st = dict(CAPTION_STYLES[style])
    st.update({k: cap[k] for k in ("size", "weight", "max_words", "max_chars", "stroke") if k in cap})
    font = cap.get("font", ctx.font)
    color = cap.get("color", "white")
    hcol = cap.get("highlight_color", "#FFE000")
    scol = cap.get("stroke_color", "black")
    pos = cap.get("position", "lower")
    y = cap.get("y")
    if y is None:
        y = ctx.Y({"lower": 1340, "middle": 960, "center": 960, "upper": 560, "bottom": 1480}.get(pos, 1340))
    x = int(cap.get("x", ctx.W // 2))
    upper = cap.get("uppercase", False)
    offset = float(cap.get("offset", 0.0))
    ws = []
    for w in words:
        t = w["text"].strip()
        if not t:
            continue
        ws.append({**w, "text": t.upper() if upper else t, "start": w["start"] + offset, "end": w["end"] + offset})
    groups = group_words(ws, int(st["max_words"]), int(st["max_chars"]))
    base = (f"\\an5\\pos({x},{y})\\fn{font}\\fs{int(st['size'] * ctx.sy)}\\b{int(st['weight'])}"
            f"\\1c{ass_color(color)}\\3c{ass_color(scol)}\\bord{fnum(st['stroke'] * ctx.sy)}\\shad2\\4a&H90&")
    if cap.get("box"):
        base += f"\\3c{ass_color(cap.get('box_color', '#000000'))}\\3a{ass_alpha(cap.get('box_color', '#000000B0'))}"
    style_name = "CapBox" if cap.get("box") else "Cap"
    evs = []
    for gi, grp in enumerate(groups):
        g0 = grp[0]["start"]
        g1 = max(grp[-1]["end"], g0 + 0.3)
        nxt = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else None
        if nxt is not None and nxt - g1 < 0.35:
            g1 = nxt
        if nxt is not None:
            g1 = min(g1, nxt)
        g1 = min(g1, total)
        if g1 <= g0:
            continue
        if style in ("clean", "bold_pop"):
            txt = " ".join(ass_escape(w["text"]) for w in grp)
            tags = base
            if style == "bold_pop":
                tags += "\\fscx55\\fscy55\\t(0,90,\\fscx110\\fscy110)\\t(90,160,\\fscx100\\fscy100)"
            else:
                tags += "\\fad(80,60)"
            evs.append(TextEvent(g0, g1, style_name, "{" + tags + "}" + rtl_fix(txt), 6))
        elif style == "highlight_word":
            for j, w in enumerate(grp):
                s0 = g0 if j == 0 else w["start"]
                s1 = grp[j + 1]["start"] if j + 1 < len(grp) else g1
                if s1 <= s0:
                    continue
                parts = []
                for k, w2 in enumerate(grp):
                    t2 = ass_escape(w2["text"])
                    if k == j:
                        parts.append(f"{{\\1c{ass_color(hcol)}\\fscx108\\fscy108}}{t2}{{\\1c{ass_color(color)}\\fscx100\\fscy100}}")
                    else:
                        parts.append(t2)
                evs.append(TextEvent(s0, s1, style_name, "{" + base + "}" + rtl_fix(" ".join(parts)), 6))
        elif style == "karaoke":
            parts = []
            tcur = g0
            for w in grp:
                lead = max(0, int(round((w["start"] - tcur) * 100)))
                if lead:
                    parts.append(f"{{\\k{lead}}}")
                k = max(1, int(round((max(w["end"], w["start"] + 0.05) - max(w["start"], tcur)) * 100)))
                parts.append(f"{{\\k{k}}}{ass_escape(w['text'])} ")
                tcur = max(w["end"], tcur)
            # karaoke: Primary = sung (highlight), Secondary = not yet sung
            tags = base.replace(f"\\1c{ass_color(color)}", f"\\1c{ass_color(hcol)}\\2c{ass_color(color)}")
            evs.append(TextEvent(g0, g1, style_name, "{" + tags + "}" + rtl_fix("".join(parts).strip()), 6))
    return evs


def whisper_words(audio: str, lang: str, model_name: str = "small") -> list[dict]:
    """Transcribe with faster-whisper (cached by audio hash)."""
    h = hashlib.sha1(Path(audio).read_bytes()).hexdigest()[:16]
    cache = CACHE_DIR / "whisper" / f"{h}_{lang}_{model_name}.json"
    if cache.exists():
        log(f"whisper: using cached transcript {cache.name}")
        return json.loads(cache.read_text(encoding="utf-8"))
    try:
        from faster_whisper import WhisperModel  # type: ignore
    except ImportError:
        raise RenderError("auto captions need faster-whisper: pip install faster-whisper "
                          "(or pass captions.source as an .srt/.ass/.json file)")
    log(f"whisper: transcribing ({model_name}, lang={lang}) ...")
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segs, _info = model.transcribe(audio, language=lang, word_timestamps=True, vad_filter=True,
                                   beam_size=5)
    words = []
    for s in segs:
        for w in s.words or []:
            if w.word.strip():
                words.append({"start": round(w.start, 3), "end": round(w.end, 3), "text": w.word.strip(),
                              "p": round(getattr(w, "probability", 1.0), 3)})
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(words, ensure_ascii=False, indent=0), encoding="utf-8")
    return words


def load_caption_words(cap: dict, ctx: Ctx, speech_wav: str | None, runner: Runner) -> list[dict]:
    src = cap.get("source", "auto")
    if cap.get("lines"):
        return lines_to_words([{"start": sec(l["start"]), "end": sec(l["end"]), "text": l["text"]}
                               for l in cap["lines"]])
    if src == "auto":
        if runner.dry:
            log("dry-run: auto captions would run whisper on the edited audio")
            return []
        if not speech_wav:
            raise RenderError("auto captions: no edited audio available")
        return whisper_words(speech_wav, cap.get("lang", "he"), cap.get("model", "small"))
    p = Path(src)
    p = p if p.is_absolute() else ctx.base / p
    if not p.exists():
        raise SpecError(f"captions source not found: {p}")
    if p.suffix.lower() == ".srt":
        return lines_to_words(parse_srt(str(p)))
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("words") or data.get("segments") or []
        if data and "words" in data[0]:
            data = [w for s in data for w in s["words"]]
        return [{"start": sec(w["start"]), "end": sec(w["end"]), "text": w.get("text") or w.get("word", "")}
                for w in data]
    raise SpecError(f"captions source must be auto, .srt, .ass or .json (got {p.name})")


def write_srt(words: list[dict], path: str, max_words: int = 7) -> None:
    out = []
    for i, grp in enumerate(group_words(words, max_words, 42), 1):
        def ts(t):
            ms = int(round(t * 1000))
            h, ms = divmod(ms, 3600000)
            m, ms = divmod(ms, 60000)
            s, ms = divmod(ms, 1000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
        out.append(f"{i}\n{ts(grp[0]['start'])} --> {ts(grp[-1]['end'])}\n{' '.join(w['text'] for w in grp)}\n")
    Path(path).write_text("\n".join(out), encoding="utf-8")


def ass_document(ctx: Ctx, events: list[TextEvent]) -> str:
    f = ctx.font
    mono = mono_font()
    hdr = [
        "[Script Info]", "; generated by reelstudio", "ScriptType: v4.00+",
        f"PlayResX: {ctx.W}", f"PlayResY: {ctx.H}", "WrapStyle: 0", "ScaledBorderAndShadow: yes",
        "YCbCr Matrix: TV.709", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, "
        "Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding",
        # Encoding -1 => libass auto-detects the base direction (needed for correct Hebrew bidi)
        f"Style: Text,{f},72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,6,2,5,"
        f"{ctx.X(70)},{ctx.X(70)},40,-1",
        f"Style: Chip,{f},34,&H00FFFFFF,&H00FFFFFF,&H50000000,&H00000000,0,0,0,0,100,100,0,0,3,12,0,7,"
        f"{ctx.X(70)},{ctx.X(70)},40,-1",
        f"Style: Prompt,{mono},26,&H00E8E8E8,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,"
        "0,0,0,-1",
        f"Style: Cap,{f},80,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,7,2,5,"
        f"{ctx.X(60)},{ctx.X(60)},40,-1",
        f"Style: CapBox,{f},80,&H00FFFFFF,&H00FFFFFF,&H50000000,&H00000000,0,0,0,0,100,100,0,0,3,14,0,5,"
        f"{ctx.X(60)},{ctx.X(60)},40,-1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    evs = sorted(events, key=lambda e: (e.start, e.layer))
    return "\n".join(hdr + [e.line() for e in evs]) + "\n"


# --------------------------------------------------------------------------------------
# SFX (synthetic, no assets needed)
# --------------------------------------------------------------------------------------

# name: (duration, anchor seconds = the moment that should land on the cut, lavfi graph)
SFX = {
    "whoosh": (0.8, 0.45, "anoisesrc=d=0.8:c=pink:r=48000:a=0.9,highpass=f=300,lowpass=f=6000,"
                          "volume='pow(sin(PI*min(t/0.8,1)),3)*1.6':eval=frame,"
                          "aphaser=in_gain=0.7:out_gain=0.9:delay=2.5:decay=0.6:speed=1.8"),
    "swish": (0.3, 0.15, "anoisesrc=d=0.3:c=white:r=48000:a=0.7,highpass=f=1200,lowpass=f=9000,"
                         "volume='pow(sin(PI*min(t/0.3,1)),2)*1.2':eval=frame"),
    "riser": (2.0, 2.0, "aevalsrc='0.32*sin(2*PI*(160*t+700*t*t*t/(3*4)))*pow(t/2,2)"
                        "+0.22*(random(0)*2-1)*pow(t/2,3)':s=48000:d=2,highpass=f=120"),
    "hit": (1.4, 0.0, "aevalsrc='0.95*sin(2*PI*(42*t+(110/16)*(1-exp(-16*t))))*exp(-3.0*t)"
                      "+0.45*(random(0)*2-1)*exp(-45*t)':s=48000:d=1.4,lowpass=f=4000"),
    "impact": (2.0, 0.0, "aevalsrc='0.9*sin(2*PI*(38*t+(120/14)*(1-exp(-14*t))))*exp(-2.4*t)"
                         "+0.35*(random(0)*2-1)*exp(-3.5*t)':s=48000:d=2,lowpass=f=7000"),
    "pop": (0.15, 0.0, "aevalsrc='0.7*sin(2*PI*(950*t-1800*t*t))*exp(-28*t)':s=48000:d=0.15"),
    "click": (0.06, 0.0, "aevalsrc='0.8*(random(0)*2-1)*exp(-180*t)':s=48000:d=0.06,highpass=f=2000"),
    "glitch": (0.45, 0.0, "aevalsrc='(0.35*(random(0)*2-1)+0.25*sgn(sin(2*PI*1350*t)))"
                          "*lt(mod(t*23,1),0.55)*(1-t/0.45)':s=48000:d=0.45"),
    "bed": (8.0, 0.0, "aevalsrc='0.07*(sin(2*PI*220*t)+sin(2*PI*261.63*t)+sin(2*PI*329.63*t))"
                      "*(0.6+0.4*sin(2*PI*0.25*t))+0.6*sin(2*PI*52*mod(t,0.5))*exp(-11*mod(t,0.5))"
                      "+0.05*(random(0)*2-1)*exp(-30*mod(t+0.25,0.5))':s=48000:d=8"),
}
SFX_FOR_TRANSITION = {"whip": "whoosh", "whip_left": "whoosh", "whip_right": "whoosh", "whip_up": "whoosh",
                      "whip_down": "whoosh", "zoom": "whoosh", "flash": "hit", "glitch": "glitch",
                      "cut": "swish", "slide": "swish"}


def render_sfx(name: str, out: str, runner: Runner, dur: float | None = None) -> str:
    if name not in SFX:
        raise SpecError(f"unknown sfx {name!r}. Valid: {', '.join(SFX)} (or give a 'path')")
    d, _anchor, graph = SFX[name]
    if name == "bed" and dur:
        graph = graph.replace("d=8", f"d={fnum(dur)}")
    runner.run([which_or_die("ffmpeg"), "-hide_banner", "-y", "-f", "lavfi", "-i", graph, "-ac", "2",
                "-ar", "48000", "-c:a", "pcm_s16le", out], f"synth sfx '{name}'")
    return out


# --------------------------------------------------------------------------------------
# transitions
# --------------------------------------------------------------------------------------

XFADE = ["fade", "wipeleft", "wiperight", "wipeup", "wipedown", "slideleft", "slideright", "slideup",
         "slidedown", "circlecrop", "rectcrop", "distance", "fadeblack", "fadewhite", "radial", "smoothleft",
         "smoothright", "smoothup", "smoothdown", "circleopen", "circleclose", "vertopen", "vertclose",
         "horzopen", "horzclose", "dissolve", "pixelize", "diagtl", "diagtr", "diagbl", "diagbr", "hlslice",
         "hrslice", "vuslice", "vdslice", "hblur", "fadegrays", "wipetl", "wipetr", "wipebl", "wipebr",
         "squeezeh", "squeezev", "zoomin", "fadefast", "fadeslow", "coverleft", "coverright", "coverup",
         "coverdown", "revealleft", "revealright", "revealup", "revealdown"]
# custom name -> (xfade type, default duration, post-effect)
CUSTOM_TRANS = {
    "whip": ("slideleft", 0.28, "blur_h"), "whip_left": ("slideleft", 0.28, "blur_h"),
    "whip_right": ("slideright", 0.28, "blur_h"), "whip_up": ("slideup", 0.28, "blur_v"),
    "whip_down": ("slidedown", 0.28, "blur_v"), "flash": ("fadewhite", 0.3, None),
    "dip": ("fadeblack", 0.5, None), "zoom": ("zoomin", 0.35, "blur_r"), "glitch": ("pixelize", 0.3, "glitch"),
    "slide": ("slideup", 0.35, None),
}


def norm_transition(tr) -> dict:
    if tr is None:
        return {"type": "cut", "dur": 0.0}
    if isinstance(tr, str):
        tr = {"type": tr}
    tr = dict(tr)
    t = tr.get("type", "cut")
    if t == "cut":
        tr["dur"] = 0.0
    elif t in CUSTOM_TRANS:
        tr.setdefault("dur", CUSTOM_TRANS[t][1])
    elif t in XFADE:
        tr.setdefault("dur", 0.4)
    else:
        raise SpecError(f"unknown transition {t!r}. Valid: cut, {', '.join(CUSTOM_TRANS)}, or xfade types: "
                        f"{', '.join(XFADE)}")
    tr["dur"] = sec(tr["dur"])
    return tr


# --------------------------------------------------------------------------------------
# render pipeline
# --------------------------------------------------------------------------------------

def load_spec(path: str) -> tuple[dict, Path]:
    p = Path(path).resolve()
    if not p.exists():
        raise SpecError(f"spec not found: {p}")
    try:
        spec = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SpecError(f"{p.name}: invalid JSON at line {e.lineno} col {e.colno}: {e.msg}")
    if not isinstance(spec, dict) or not spec.get("timeline"):
        raise SpecError("spec must be an object with a non-empty 'timeline' list")
    return spec, p.parent


def plan_timeline(spec: dict, ctx: Ctx) -> list[dict]:
    """Resolve segment durations, transitions and global start times (no rendering)."""
    plans = []
    t = 0.0
    for i, seg in enumerate(spec["timeline"]):
        if not isinstance(seg, dict):
            raise SpecError(f"timeline[{i}] must be an object")
        P = build_segment(seg, ctx)
        tr = norm_transition(seg.get("transition") if i > 0 else None)
        if i > 0 and tr["dur"] > 0:
            maxd = min(plans[-1]["plan"].dur, P.dur) * 0.9
            if tr["dur"] > maxd:
                warn(f"timeline[{i}]: transition {tr['dur']}s too long, clamped to {maxd:.2f}s")
                tr["dur"] = maxd
            tr["dur"] = max(1, int(round(tr["dur"] * ctx.fps))) / ctx.fps
        start = t - (tr["dur"] if i > 0 else 0)
        plans.append({"i": i, "seg": seg, "plan": P, "trans": tr, "start": start})
        t = start + P.dur
    return plans


def print_plan(plans: list[dict], total: float) -> None:
    print(f"{'#':>2}  {'start':>7}  {'dur':>6}  {'layout':<20} transition-in")
    for p in plans:
        tr = p["trans"]
        trs = "-" if p["i"] == 0 else (tr["type"] + (f" {tr['dur']:.2f}s" if tr["dur"] else ""))
        print(f"{p['i']:>2}  {p['start']:7.2f}  {p['plan'].dur:6.2f}  {p['plan'].layout:<20} {trs}")
    print(f"total: {total:.2f}s")


def render(spec_path: str, preset: str | None = None, out: str | None = None, dry: bool = False,
           keep: bool = False, fast: bool = False, verbose: bool = False, workdir: str | None = None) -> str:
    ffmpeg = which_or_die("ffmpeg")
    which_or_die("ffprobe")
    spec, base = load_spec(spec_path)
    # canvas: the spec's own export preset first (so `--preset draft` previews a feed spec at 4:5),
    # then the requested preset if it forces an aspect
    spec = apply_preset_canvas(spec, resolve_preset(None, spec))
    preset = resolve_preset(preset, spec)
    spec = apply_preset_canvas(spec, preset)
    ctx = Ctx(spec, base)
    runner = Runner(dry=dry, verbose=verbose)
    if not dry:
        ensure_fonts(runner)
    pr = PRESETS[preset]
    inter = pr["inter"]
    if fast:
        pr = dict(pr)
        pr["video"] = [("medium" if x == "slow" else x) for x in pr["video"]]
    out_path = Path(out or spec.get("output") or (Path(spec_path).stem + ".mp4"))
    if not out_path.is_absolute():
        out_path = (Path.cwd() / out_path) if out else (base / out_path)
    if preset == "draft" and not out and "_draft" not in out_path.stem:
        out_path = out_path.with_name(out_path.stem + "_draft.mp4")

    plans = plan_timeline(spec, ctx)
    total = plans[-1]["start"] + plans[-1]["plan"].dur
    print_plan(plans, total)
    if total > 180:
        warn(f"total duration {total:.1f}s is longer than most reel limits")

    tmp = Path(workdir) if workdir else Path(tempfile.mkdtemp(prefix="reelstudio_"))
    tmp.mkdir(parents=True, exist_ok=True)
    log(f"work dir: {tmp}")
    try:
        venc = ["-c:v", "libx264", *inter, "-pix_fmt", "yuv420p", "-g", str(int(ctx.fps * 2))]
        # 1) segments
        seg_files = []
        for p in plans:
            P: SegPlan = p["plan"]
            f = tmp / f"seg_{p['i']:03d}.mkv"
            P.g.sink_unused([P.v, P.a])
            cmd = [ffmpeg, "-hide_banner", "-y", *P.g.cmd_inputs(), "-filter_complex", P.g.script(),
                   "-map", f"[{P.v}]", "-map", f"[{P.a}]", "-r", fnum(ctx.fps), "-frames:v",
                   str(int(round(P.dur * ctx.fps))), *venc, "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2",
                   str(f)]
            runner.run(cmd, f"segment {p['i']} ({P.layout}, {P.dur:.2f}s)")
            seg_files.append(f)

        # 2) join with transitions
        joined = tmp / "joined.mkv"
        cut_points = []  # (time, transition dict)
        if len(seg_files) == 1:
            joined = seg_files[0]
        else:
            g = Graph("j")
            for f in seg_files:
                g.add_input(["-i", str(f)])
            v = g.chain("0:v", "settb=AVTB,format=yuv420p")
            a = g.chain("0:a", "aformat=sample_fmts=fltp:channel_layouts=stereo", "a")
            acc = plans[0]["plan"].dur
            posts = []
            for p in plans[1:]:
                i = p["i"]
                tr = p["trans"]
                vi = g.chain(f"{i}:v", "settb=AVTB,format=yuv420p")
                ai = g.chain(f"{i}:a", "aformat=sample_fmts=fltp:channel_layouts=stereo", "a")
                if tr["type"] == "cut":
                    nv, na = g.label(), g.label("a")
                    g.add(f"[{v}][{vi}]concat=n=2:v=1:a=0[{nv}]")
                    g.add(f"[{a}][{ai}]concat=n=2:v=0:a=1[{na}]")
                    cut_points.append((acc, tr))
                    acc += p["plan"].dur
                else:
                    d = tr["dur"]
                    xt, _dd, post = CUSTOM_TRANS.get(tr["type"], (tr["type"], d, None))
                    off = acc - d
                    nv, na = g.label(), g.label("a")
                    g.add(f"[{v}][{vi}]xfade=transition={xt}:duration={fnum(d)}:offset={fnum(off)}[{nv}]")
                    g.add(f"[{a}][{ai}]acrossfade=d={fnum(d)}:c1=tri:c2=tri[{na}]")
                    if post:
                        posts.append((post, off, d))
                    cut_points.append((off + d / 2, tr))
                    acc = off + d + p["plan"].dur - d
                v, a = nv, na
            for post, off, d in posts:
                win = f"between(t,{fnum(off - 0.02)},{fnum(off + d + 0.02)})"
                if post == "blur_h":
                    v = g.chain(v, f"avgblur=sizeX=48:sizeY=1:enable='{win}'")
                elif post == "blur_v":
                    v = g.chain(v, f"avgblur=sizeX=1:sizeY=48:enable='{win}'")
                elif post == "blur_r":
                    v = g.chain(v, f"gblur=sigma=10:enable='{win}'")
                elif post == "glitch":
                    v = g.chain(v, f"rgbashift=rh=-16:bh=16:edge=smear:enable='{win}',"
                                   f"noise=alls=30:allf=t:enable='{win}',format=yuv420p")
            cmd = [ffmpeg, "-hide_banner", "-y", *g.cmd_inputs(), "-filter_complex", g.script(),
                   "-map", f"[{v}]", "-map", f"[{a}]", "-r", fnum(ctx.fps), "-frames:v",
                   str(int(round(total * ctx.fps))), *venc, "-c:a", "pcm_s16le", str(joined)]
            runner.run(cmd, f"join {len(seg_files)} segments")

        # 3) text events
        events: list[TextEvent] = []
        for p in plans:
            P = p["plan"]
            for ov in P.overlays:
                if ov.get("type", "text") in ("text", "chip", "label", "title", "cta"):
                    events += [e.shifted(p["start"]) for e in text_overlay_events(ov, ctx, P.dur)]
            events += [e.shifted(p["start"]) for e in P.events]
        image_ovs = []
        for p in plans:
            for ov in p["plan"].overlays:
                if ov.get("type") == "image":
                    o = dict(ov)
                    o["start"] = sec(o.get("start", 0)) + p["start"]
                    o["end"] = (sec(o["end"]) + p["start"]) if o.get("end") is not None else p["start"] + p["plan"].dur
                    image_ovs.append(o)
        for ov in spec.get("overlays", []) or []:
            t = ov.get("type", "text")
            if t == "image":
                image_ovs.append(dict(ov))
            elif t in ("text", "chip", "label", "title", "cta"):
                events += text_overlay_events(ov, ctx, total)
            else:
                raise SpecError(f"unknown overlay type {t!r} (text, chip, image)")

        # 4) audio: extract edited speech, captions, music, sfx, loudnorm
        speech = tmp / "speech.wav"
        runner.run([ffmpeg, "-hide_banner", "-y", "-i", str(joined), "-vn", "-ac", "2", "-ar", "48000",
                    "-c:a", "pcm_s16le", str(speech)], "extract edited audio")
        cap = spec.get("captions")
        user_ass = None
        if cap:
            src = str(cap.get("source", "auto"))
            if src.lower().endswith(".ass"):
                pa = Path(src) if Path(src).is_absolute() else base / src
                if not pa.exists():
                    raise SpecError(f"captions .ass not found: {pa}")
                user_ass = str(pa)
            else:
                wav16 = None
                if src == "auto" and not dry and not cap.get("lines"):
                    wav16 = str(tmp / "speech16k.wav")
                    runner.run([ffmpeg, "-hide_banner", "-y", "-i", str(speech), "-ac", "1", "-ar", "16000",
                                str(wav16)], "speech -> 16k mono for whisper")
                words = load_caption_words(cap, ctx, wav16, runner)
                if words and cap.get("save_words"):
                    sw = Path(cap["save_words"])
                    sw = sw if sw.is_absolute() else base / sw
                    sw.write_text(json.dumps(words, ensure_ascii=False, indent=1), encoding="utf-8")
                    log(f"caption words saved to {sw} (edit it and use it as captions.source)")
                events += caption_events(cap, words, ctx, total)
        ass_file = tmp / "overlay.ass"
        if not dry:
            ass_file.write_text(ass_document(ctx, events), encoding="utf-8")

        final_wav = tmp / "final.wav"
        build_audio(spec.get("audio") or {}, ctx, runner, ffmpeg, tmp, speech, total, cut_points,
                    final_wav, base)

        # 5) final encode
        g = Graph("f")
        g.add_input(["-i", str(joined)])
        v = g.chain("0:v", "setpts=PTS-STARTPTS,format=yuv420p")
        geff = []
        for e in spec.get("effects", []) or []:
            e = {"type": e} if isinstance(e, str) else dict(e)
            if e.get("type") == "lut" and e.get("path") and not os.path.isabs(e["path"]):
                e["path"] = str((base / e["path"]).resolve())
            geff.append(e)
        v = apply_effects(g, v, geff, ctx.W, ctx.H, ctx.fps, total)
        for ov in image_ovs:
            pth = Path(ov["path"]) if Path(ov["path"]).is_absolute() else base / ov["path"]
            if not pth.exists():
                raise SpecError(f"image overlay not found: {pth}")
            idx = g.add_input(["-loop", "1", "-framerate", fnum(ctx.fps), "-t", fnum(total), "-i", str(pth)])
            s0 = sec(ov.get("start", 0))
            s1 = sec(ov["end"]) if ov.get("end") is not None else total
            wpx = int(ov.get("width", 220) * ctx.sx)
            op = float(ov.get("opacity", 1.0))
            fade = float(ov.get("fade", 0.2))
            chainf = f"scale={wpx}:-2,format=rgba,colorchannelmixer=aa={fnum(op)}"
            if fade > 0:
                chainf += (f",fade=t=in:st={fnum(s0)}:d={fnum(fade)}:alpha=1,"
                           f"fade=t=out:st={fnum(max(s0, s1 - fade))}:d={fnum(fade)}:alpha=1")
            il = g.chain(f"{idx}:v", chainf)
            x, y, an = resolve_xy({**ov, "align": ov.get("align", 5)}, ctx)
            # anchor: center by default; align 7 = top-left
            xo = f"{x}-w/2" if an in (2, 5, 8) else (f"{x}" if an in (1, 4, 7) else f"{x}-w")
            yo = f"{y}-h/2" if an in (4, 5, 6) else (f"{y}" if an in (7, 8, 9) else f"{y}-h")
            nv = g.label()
            g.add(f"[{v}][{il}]overlay=x={xo}:y={yo}:enable='between(t,{fnum(s0)},{fnum(s1)})':"
                  f"eof_action=pass[{nv}]")
            v = nv
        if events:
            v = g.chain(v, f"ass=filename={esc_filter_path(str(ass_file))}:shaping=complex")
        if user_ass:
            v = g.chain(v, f"ass=filename={esc_filter_path(user_ass)}:shaping=complex")
        if pr["scale"]:
            v = g.chain(v, f"scale={pr['scale'][0]}:{pr['scale'][1]}:flags=bicubic")
        v = g.chain(v, "format=yuv420p")
        ai = g.add_input(["-i", str(final_wav)])
        out_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = [ffmpeg, "-hide_banner", "-y", *g.cmd_inputs(), "-filter_complex", g.script(),
               "-map", f"[{v}]", "-map", f"{ai}:a", "-r", fnum(ctx.fps), "-frames:v", str(int(round(total * ctx.fps))),
               *pr["video"], "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
               "-color_trc", "bt709", "-color_range", "tv", *pr["audio"], "-ac", "2",
               "-movflags", "+faststart", "-metadata", f"comment=reelstudio {VERSION}", str(out_path)]
        runner.run(cmd, f"final encode ({preset})")
        if not dry:
            info = probe(str(out_path))
            log(f"done: {out_path}  {info['width']}x{info['height']} {info['fps']}fps "
                f"{info['duration']:.2f}s {info['size_bytes'] / 1e6:.1f}MB")
            if abs((info["duration"] or 0) - total) > 0.25:
                warn(f"output duration {info['duration']:.2f}s differs from plan {total:.2f}s")
        return str(out_path)
    finally:
        if keep:
            log(f"kept work dir {tmp}")
        elif not workdir:
            shutil.rmtree(tmp, ignore_errors=True)


def build_audio(audio: dict, ctx: Ctx, runner: Runner, ffmpeg: str, tmp: Path, speech: Path, total: float,
                cut_points: list, out_wav: Path, base: Path) -> None:
    g = Graph("a")
    g.add_input(["-i", str(speech)])
    ov = float(audio.get("original_volume", 1.0))
    sp = g.chain("0:a", f"volume={fnum(ov)},aformat=sample_fmts=fltp:channel_layouts=stereo", "a")
    mix = []
    music = audio.get("music")
    sc = None
    if music:
        if isinstance(music, str):
            music = {"path": music}
        if music.get("synth"):
            mp = str(tmp / "music_synth.wav")
            render_sfx(music["synth"], mp, runner, dur=total + 1)
        else:
            mp = music.get("path")
            mp = str(Path(mp) if Path(mp).is_absolute() else base / mp)
            if not os.path.exists(mp):
                raise SpecError(f"music not found: {mp}")
        mi = g.add_input(["-stream_loop", "-1", "-ss", fnum(sec(music.get("in", 0))), "-i", mp])
        mvol = float(music.get("volume", 0.35))
        fi = float(music.get("fade_in", 0.3))
        fo = float(music.get("fade_out", 1.2))
        ml = g.chain(f"{mi}:a", f"atrim=duration={fnum(total)},asetpts=PTS-STARTPTS,"
                                f"aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=48000,"
                                f"volume={fnum(mvol)},afade=t=in:st=0:d={fnum(fi)},"
                                f"afade=t=out:st={fnum(max(0, total - fo))}:d={fnum(fo)}", "a")
        if music.get("duck", True):
            s1, s2 = g.label("a"), g.label("a")
            g.add(f"[{sp}]asplit=2[{s1}][{s2}]")
            sp, sc = s1, s2
            duck = music.get("duck") if isinstance(music.get("duck"), dict) else {}
            ml2 = g.label("a")
            g.add(f"[{ml}][{sc}]sidechaincompress=threshold={fnum(duck.get('threshold', 0.025))}:"
                  f"ratio={fnum(duck.get('ratio', 10))}:attack={fnum(duck.get('attack', 15))}:"
                  f"release={fnum(duck.get('release', 350))}:makeup=1[{ml2}]")
            ml = ml2
        mix.append(ml)
    # sfx list (explicit) + automatic sfx on cuts
    sfx_items = []
    for s in audio.get("sfx", []) or []:
        sfx_items.append(dict(s))
    auto = audio.get("sfx_on_cuts")
    if auto:
        auto = {"type": auto} if isinstance(auto, str) else dict(auto)
        for t, tr in cut_points:
            kind = tr.get("sfx") or (SFX_FOR_TRANSITION.get(tr["type"], "whoosh") if auto["type"] == "auto"
                                     else auto["type"])
            if kind in (None, "none", False):
                continue
            sfx_items.append({"type": kind, "at": t, "volume": auto.get("volume", 0.7)})
    else:
        for t, tr in cut_points:
            if tr.get("sfx"):
                sfx_items.append({"type": tr["sfx"], "at": t, "volume": tr.get("sfx_volume", 0.7)})
    files: dict[str, int] = {}
    for s in sfx_items:
        if s.get("path"):
            pth = Path(s["path"]) if Path(s["path"]).is_absolute() else base / s["path"]
            if not pth.exists():
                raise SpecError(f"sfx file not found: {pth}")
            key, anchor = str(pth), float(s.get("anchor", 0))
        else:
            name = s.get("type", "whoosh")
            if name not in SFX:
                raise SpecError(f"unknown sfx {name!r}. Valid: {', '.join(SFX)} (or give 'path')")
            key = str(tmp / f"sfx_{name}.wav")
            anchor = SFX[name][1]
            if key not in files:
                render_sfx(name, key, runner)
        if key not in files:
            files[key] = g.add_input(["-i", key])
        s["_in"], s["_anchor"] = files[key], anchor
    by_input: dict[int, list] = {}
    for s in sfx_items:
        by_input.setdefault(s["_in"], []).append(s)
    for idx, items in by_input.items():
        labs = [g.label("a") for _ in items]
        g.add(f"[{idx}:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=48000,asplit={len(items)}"
              + "".join(f"[{x}]" for x in labs) if len(items) > 1 else
              f"[{idx}:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=48000[{labs[0]}]")
        for lab, s in zip(labs, items):
            st = sec(s.get("at", 0)) - s["_anchor"]
            vol = float(s.get("volume", 0.8))
            if st >= 0:
                ms = int(round(st * 1000))
                f = f"adelay={ms}|{ms},volume={fnum(vol)}"
            else:
                f = f"atrim=start={fnum(-st)},asetpts=PTS-STARTPTS,volume={fnum(vol)}"
            mix.append(g.chain(lab, f, "a"))
    allm = [sp] + mix
    if len(allm) > 1:
        m = g.label("a")
        g.add("".join(f"[{x}]" for x in allm) + f"amix=inputs={len(allm)}:normalize=0:duration=first[{m}]")
    else:
        m = sp
    m = g.chain(m, f"apad,atrim=duration={fnum(total)}", "a")
    premix = tmp / "premix.wav"
    runner.run([ffmpeg, "-hide_banner", "-y", *g.cmd_inputs(), "-filter_complex", g.script(), "-map", f"[{m}]",
                "-ac", "2", "-ar", "48000", "-c:a", "pcm_f32le", str(premix)], "audio mix (music/ducking/sfx)")
    target = audio.get("loudnorm", -14)
    if target in (None, False):
        if not runner.dry:
            shutil.copy(premix, out_wav)
        return
    tp = float(audio.get("true_peak", -1.5))
    lra = float(audio.get("lra", 11))
    ln = f"loudnorm=I={fnum(target)}:TP={fnum(tp)}:LRA={fnum(lra)}"
    p = runner.run([ffmpeg, "-hide_banner", "-y", "-i", str(premix), "-af", ln + ":print_format=json", "-f",
                    "null", "-"], "loudness measure (pass 1)")
    measured = None
    if p is not None:
        m2 = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p.stderr, re.S)
        if m2:
            measured = json.loads(m2.group(0))
    if measured and measured.get("input_i") not in ("-inf", None) and float(measured["input_i"]) > -70:
        f2 = (f"{ln}:measured_I={measured['input_i']}:measured_TP={measured['input_tp']}:"
              f"measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}:"
              f"offset={measured['target_offset']}:linear=true,aresample=48000")
        runner.run([ffmpeg, "-hide_banner", "-y", "-i", str(premix), "-af", f2, "-ac", "2", "-ar", "48000",
                    "-c:a", "pcm_s16le", str(out_wav)], f"loudnorm to {target} LUFS (pass 2)")
    else:
        if p is not None:
            log("audio is silent - skipping loudnorm")
        runner.run([ffmpeg, "-hide_banner", "-y", "-i", str(premix), "-c:a", "pcm_s16le", str(out_wav)],
                   "audio passthrough")


# --------------------------------------------------------------------------------------
# utility commands
# --------------------------------------------------------------------------------------

def cmd_probe(files: list[str]) -> None:
    out = []
    for f in files:
        try:
            out.append(probe(f))
        except SpecError as e:
            out.append({"path": f, "error": str(e)})
    print(json.dumps(out if len(out) > 1 else out[0], indent=2, ensure_ascii=False))


def cmd_grid(video: str, cols: int, rows: int, width: int, out: str | None, start: float, end: float | None,
             max_kb: int) -> str:
    info = probe(video)
    dur = (end or info["duration"] or 1) - start
    n = cols * rows
    tw = even(width / cols)
    out = out or str(Path(video).with_suffix("")) + "_grid.jpg"
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    step = dur / n
    dt = (f",drawtext=fontfile={esc_filter_path(font)}:text='%{{pts\\:hms\\:{fnum(start + step / 2)}}}':x=6:y=6:"
          f"fontsize={max(12, tw // 14)}:fontcolor=yellow:box=1:boxcolor=black@0.6:boxborderw=4"
          if os.path.exists(font) else "")
    step = dur / n
    vf = (f"fps=1/{fnum(step, 5)}:start_time=0,scale={tw}:-2{dt},"
          f"tile={cols}x{rows}:padding=4:color=0x202020")
    for q in (4, 6, 8, 11, 15, 20):
        cmd = [which_or_die("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y", "-ss", fnum(start + step / 2),
               "-t", fnum(dur), "-i", video, "-vf", vf, "-frames:v", "1", "-q:v", str(q), out]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if p.returncode != 0:
            raise RenderError(f"grid failed: {tail(p.stderr)}")
        if os.path.getsize(out) <= max_kb * 1024:
            break
    log(f"grid: {out} ({os.path.getsize(out) // 1024} KB, {n} frames every {step:.2f}s)")
    return out


def cmd_cuts(video: str, threshold: float, as_json: bool) -> list[float]:
    cmd = [which_or_die("ffmpeg"), "-hide_banner", "-i", video, "-an", "-vf",
           f"scale=320:-2,select='gt(scene,{threshold})',showinfo", "-f", "null", "-"]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="replace")
    times = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", p.stderr)]
    dur = probe(video)["duration"] or 0
    bounds = [0.0] + times + [dur]
    shots = [{"start": round(a, 3), "end": round(b, 3), "dur": round(b - a, 3)} for a, b in zip(bounds, bounds[1:])]
    if as_json:
        print(json.dumps({"cuts": times, "shots": shots}, indent=1))
    else:
        print(f"{len(times)} cuts (threshold {threshold}) in {dur:.2f}s")
        for i, s in enumerate(shots):
            print(f"  shot {i + 1:2d}: {s['start']:7.2f} - {s['end']:7.2f}  ({s['dur']:.2f}s)")
    return times


def cmd_captions(video: str, lang: str, model: str, style: str, out_dir: str | None, size: int | None) -> None:
    ffmpeg = which_or_die("ffmpeg")
    info = probe(video)
    if not info["has_audio"]:
        raise SpecError(f"{video} has no audio track")
    od = Path(out_dir or Path(video).parent)
    od.mkdir(parents=True, exist_ok=True)
    stem = Path(video).stem
    with tempfile.TemporaryDirectory(prefix="reelstudio_cap_") as td:
        wav = str(Path(td) / "a.wav")
        p = subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", video, "-vn", "-ac", "1",
                            "-ar", "16000", wav], stderr=subprocess.PIPE, text=True)
        if p.returncode:
            raise RenderError(tail(p.stderr))
        words = whisper_words(wav, lang, model)
    wj = od / f"{stem}.words.json"
    wj.write_text(json.dumps(words, ensure_ascii=False, indent=1), encoding="utf-8")
    write_srt(words, str(od / f"{stem}.srt"))
    W, H = info["width"] or 1080, info["height"] or 1920
    ctx = Ctx({"canvas": {"width": W, "height": H}, "timeline": [1]}, od)
    cap = {"style": style}
    if size:
        cap["size"] = size
    doc = ass_document(ctx, caption_events(cap, words, ctx, info["duration"] or 1e9))
    (od / f"{stem}.{style}.ass").write_text(doc, encoding="utf-8")
    low = [w for w in words if w.get("p", 1) < 0.5]
    print(f"{len(words)} words -> {wj}, {od / (stem + '.srt')}, {od / (stem + '.' + style + '.ass')}")
    if low:
        print("low-confidence words (check spelling): " + ", ".join(f"{w['text']}@{w['start']:.1f}" for w in low[:30]))


def cmd_sfx(out_dir: str) -> None:
    od = Path(out_dir)
    od.mkdir(parents=True, exist_ok=True)
    r = Runner()
    for name in SFX:
        render_sfx(name, str(od / f"{name}.wav"), r)
    print(f"wrote {len(SFX)} sfx to {od}")


def write_cube(path: str | Path, kind: str = "warm", n: int = 17) -> str:
    """Write a simple 3D LUT (.cube). kinds: warm, cool, teal_orange, identity."""
    rows = [f'TITLE "reelstudio {kind}"', f"LUT_3D_SIZE {n}"]
    for bi in range(n):
        for gi in range(n):
            for ri in range(n):
                r, g, b = ri / (n - 1), gi / (n - 1), bi / (n - 1)
                if kind == "warm":
                    r, g, b = r * 1.06 + 0.02, g * 1.01, b * 0.90
                elif kind == "cool":
                    r, g, b = r * 0.92, g * 1.0, b * 1.06 + 0.02
                elif kind == "teal_orange":
                    lum = 0.299 * r + 0.587 * g + 0.114 * b
                    r, g, b = r + 0.10 * (lum - 0.4), g + 0.02 * (lum - 0.5), b - 0.10 * (lum - 0.6)
                rows.append(" ".join(f"{min(1.0, max(0.0, x)):.5f}" for x in (r, g, b)))
    Path(path).write_text("\n".join(rows) + "\n", encoding="utf-8")
    return str(path)


def cmd_demo_media(out_dir: str, blockout: str | None = None, force: bool = False) -> list[str]:
    """Synthetic placeholder media matching the file names used in examples/*.json.

    Lets every example render without real footage (smoke tests, dry runs). Real AI
    clips simply replace these files. boca_villa_ai.mp4 is faked from the blockout
    (graded + noise) so the blocks->reality reveal stays geometry-aligned.
    """
    ff = which_or_die("ffmpeg")
    od = Path(out_dir)
    od.mkdir(parents=True, exist_ok=True)
    made = []

    def run(args: list[str], dst: Path) -> None:
        if dst.exists() and not force:
            return
        p = subprocess.run([ff, "-hide_banner", "-loglevel", "error", "-y", *args, str(dst)],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if p.returncode:
            raise RenderError(f"demo media {dst.name}: {tail(p.stderr)}")
        made.append(str(dst))

    x264 = ["-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p"]
    aac = ["-c:a", "aac", "-b:a", "128k"]
    run(["-f", "lavfi", "-i", "testsrc2=s=720x1280:r=30:d=5", "-f", "lavfi", "-i",
         "sine=f=330:d=5:sample_rate=48000", *x264, *aac, "-shortest"], od / "clip1.mp4")
    run(["-f", "lavfi", "-i", "mandelbrot=s=1280x720:r=24", "-t", "5", "-f", "lavfi", "-i",
         "sine=f=550:d=5:sample_rate=48000", *x264, *aac, "-shortest"], od / "clip2.mp4")
    run(["-f", "lavfi", "-i", "smptehdbars=s=1080x1920:r=30:d=4", *x264], od / "clip3.mp4")
    # "talking head": tone bursts so ducking/captions have something to react to
    run(["-f", "lavfi", "-i", "testsrc=s=1080x1920:r=30:d=6", "-f", "lavfi", "-i",
         "aevalsrc='0.4*sin(2*PI*180*t)*gt(sin(2*PI*0.7*t),0)':s=48000:d=6", *x264, *aac, "-shortest"],
        od / "talk.mp4")
    if not (od / "music.wav").exists() or force:
        render_sfx("bed", str(od / "music.wav"), Runner(), dur=30)
        made.append(str(od / "music.wav"))
    run(["-f", "lavfi", "-i", "color=c=0x0B3D91@1:s=400x160,format=rgba,"
         "drawbox=x=8:y=8:w=384:h=144:color=white@1:t=6,drawbox=x=40:y=60:w=320:h=40:color=0xFFC83D@1:t=fill",
         "-frames:v", "1"], od / "logo.png")
    run(["-f", "lavfi", "-i", "gradients=s=1080x1920:c0=0x0B3D91:c1=0x111111:d=1", "-frames:v", "1"],
        od / "packshot.png")
    if not (od / "grade.cube").exists() or force:
        made.append(write_cube(od / "grade.cube", "teal_orange"))
    blk = od / "boca_villa_blockout.mp4"
    if blockout and Path(blockout).exists() and (not blk.exists() or force):
        shutil.copy(blockout, blk)
        made.append(str(blk))
    # stand-in for the Blender blockout: flat colored blocks drifting (camera push-in feel)
    run(["-f", "lavfi", "-i", "color=c=0xD9E6FA:s=540x960:r=24:d=6", "-vf",
         "drawbox=x=0:y=560:w=540:h=400:color=0xBFB38C:t=fill,"
         "drawbox=x='60-t*8':y=380:w='300+t*16':h=200:color=0xEBEBEB:t=fill,"
         "drawbox=x=120:y=600:w='220+t*10':h=60:color=0x8CE6D9:t=fill,"
         "drawbox=x=60:y=640:w=40:h=50:color=0xD91414:t=fill,"
         "drawbox=x=0:y=820:w=540:h=140:color=0x8CE6D9:t=fill", *x264], blk)
    run(["-i", str(blk), "-vf", "hue=s=1.6:h=15,eq=contrast=1.25:brightness=0.03,"
         "noise=alls=18:allf=t,gblur=sigma=1.2,unsharp=5:5:1.2", *x264], od / "boca_villa_ai.mp4")
    return made


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="reelstudio", description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("render", help="render a JSON edit spec")
    r.add_argument("spec")
    r.add_argument("--preset", help="instagram|tiktok|shorts|master|draft (default: spec.export or instagram)")
    r.add_argument("--out", help="output file (default: spec.output, relative to the spec)")
    r.add_argument("--dry-run", action="store_true", help="print the plan and every ffmpeg command, run nothing")
    r.add_argument("--keep", action="store_true", help="keep the temp work dir")
    r.add_argument("--workdir", help="use this work dir (kept)")
    r.add_argument("--fast", action="store_true", help="x264 preset medium instead of slow for the final encode")
    r.add_argument("-v", "--verbose", action="store_true", help="print ffmpeg commands while running")

    pl = sub.add_parser("plan", help="validate a spec and print the resolved timeline")
    pl.add_argument("spec")
    pl.add_argument("--preset")

    p = sub.add_parser("probe", help="media info as JSON")
    p.add_argument("files", nargs="+")

    c = sub.add_parser("captions", help="whisper -> words.json + .srt + styled .ass")
    c.add_argument("video")
    c.add_argument("--lang", default="he")
    c.add_argument("--model", default="small", help="faster-whisper model (small, medium, large-v3, ...)")
    c.add_argument("--style", default="bold_pop", choices=list(CAPTION_STYLES))
    c.add_argument("--size", type=int)
    c.add_argument("--out-dir")

    gr = sub.add_parser("grid", help="contact sheet jpg with timestamps")
    gr.add_argument("video")
    gr.add_argument("--cols", type=int, default=4)
    gr.add_argument("--rows", type=int, default=3)
    gr.add_argument("--width", type=int, default=1080, help="total sheet width in px")
    gr.add_argument("--start", type=float, default=0.0)
    gr.add_argument("--end", type=float)
    gr.add_argument("--max-kb", type=int, default=190)
    gr.add_argument("--out")

    cu = sub.add_parser("cuts", help="scene-cut detection")
    cu.add_argument("video")
    cu.add_argument("--threshold", type=float, default=0.3)
    cu.add_argument("--json", action="store_true")

    f = sub.add_parser("fonts", help="download Heebo/Rubik/Secular One/JetBrains Mono to the cache")
    f.add_argument("--force", action="store_true")

    s = sub.add_parser("sfx", help="write the synthetic SFX library as wav files")
    s.add_argument("--out", default="sfx")

    dm = sub.add_parser("demo-media", help="write synthetic placeholder clips used by examples/*.json")
    dm.add_argument("--out", default="media")
    dm.add_argument("--blockout", help="copy this real blockout render in as boca_villa_blockout.mp4")
    dm.add_argument("--force", action="store_true")

    lt = sub.add_parser("lut", help="write a simple .cube LUT (warm/cool/teal_orange/identity)")
    lt.add_argument("out")
    lt.add_argument("--kind", default="warm", choices=["warm", "cool", "teal_orange", "identity"])

    a = ap.parse_args(argv)
    try:
        if a.cmd == "render":
            render(a.spec, a.preset, a.out, a.dry_run, a.keep, a.fast, a.verbose, a.workdir)
        elif a.cmd == "plan":
            spec, base = load_spec(a.spec)
            spec = apply_preset_canvas(spec, resolve_preset(None, spec))
            spec = apply_preset_canvas(spec, resolve_preset(a.preset, spec))
            ctx = Ctx(spec, base)
            plans = plan_timeline(spec, ctx)
            print_plan(plans, plans[-1]["start"] + plans[-1]["plan"].dur)
        elif a.cmd == "probe":
            cmd_probe(a.files)
        elif a.cmd == "captions":
            download_fonts(quiet=True)
            cmd_captions(a.video, a.lang, a.model, a.style, a.out_dir, a.size)
        elif a.cmd == "grid":
            cmd_grid(a.video, a.cols, a.rows, a.width, a.out, a.start, a.end, a.max_kb)
        elif a.cmd == "cuts":
            cmd_cuts(a.video, a.threshold, a.json)
        elif a.cmd == "fonts":
            got = download_fonts(force=a.force)
            print(f"{len(got)}/{len(FONT_SOURCES)} fonts in {FONT_DIR}")
        elif a.cmd == "sfx":
            cmd_sfx(a.out)
        elif a.cmd == "demo-media":
            made = cmd_demo_media(a.out, a.blockout, a.force)
            print(f"{len(made)} files written to {a.out}")
        elif a.cmd == "lut":
            print(write_cube(a.out, a.kind))
    except SpecError as e:
        print(f"spec error: {e}", file=sys.stderr)
        return 2
    except RenderError as e:
        print(f"render error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
