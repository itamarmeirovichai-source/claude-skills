"""Shared fixtures: synthetic media only (ffmpeg testsrc/sine/lavfi), nothing downloaded except fonts."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

import reelstudio as rs  # noqa: E402

if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
    pytest.skip("ffmpeg/ffprobe not installed", allow_module_level=True)


@pytest.fixture(scope="session")
def media(tmp_path_factory) -> Path:
    """Synthetic placeholder media under <tmp>/media (same names the examples use)."""
    root = tmp_path_factory.mktemp("rs_media")
    rs.cmd_demo_media(str(root / "media"))
    # a short clip with NO audio track and an odd size, to exercise padding / silent paths
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "smptebars=s=500x700:r=25:d=3", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    str(root / "media" / "noaudio.mp4")], check=True)
    return root


@pytest.fixture(scope="session")
def fonts_ok() -> bool:
    rs.download_fonts(quiet=True)
    return (rs.FONT_DIR / "Heebo[wght].ttf").exists()


def write_spec(root: Path, name: str, spec: dict) -> Path:
    p = root / f"{name}.json"
    p.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    return p


def small(spec: dict, w: int = 540, h: int = 960, fps: int = 24) -> dict:
    """Low-res canvas so integration renders stay fast."""
    spec = dict(spec)
    spec.setdefault("canvas", {"width": w, "height": h, "fps": fps})
    return spec


def ffprobe(path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams",
                          str(path)], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def vstream(path) -> dict:
    return next(s for s in ffprobe(path)["streams"] if s["codec_type"] == "video")


def duration(path) -> float:
    return float(ffprobe(path)["format"]["duration"])


def integrated_lufs(path) -> float:
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    import re
    vals = re.findall(r"I:\s+(-?[\d.]+) LUFS", p.stderr)
    return float(vals[-1])


def frame_rgb(path, t: float, w: int = 54, h: int = 96) -> bytes:
    """Downscaled RGB24 frame at time t (for coarse pixel assertions)."""
    return subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t), "-i", str(path), "-frames:v", "1",
                           "-vf", f"scale={w}:{h}:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                          capture_output=True, check=True).stdout
