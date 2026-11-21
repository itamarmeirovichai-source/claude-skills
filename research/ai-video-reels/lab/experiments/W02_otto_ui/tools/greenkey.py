"""Green-screen key -> stacked-alpha video (colour on top, alpha as grey below).

alpha from green excess e = G - max(R,B): e <= LO -> opaque, e >= HI -> transparent.
Spill: G clamped toward max(R,B) where it leads. Optional --mirror flips horizontally.
Usage: python3 greenkey.py in.mp4 out_stacked.mp4 [--mirror] [--lo 18] [--hi 55]
"""
import argparse, subprocess, numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--mirror", action="store_true")
ap.add_argument("--lo", type=float, default=18); ap.add_argument("--hi", type=float, default=55)
a = ap.parse_args()

probe = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                 "stream=width,height,r_frame_rate", "-of", "csv=p=0", a.inp]).decode().strip().split(",")
w, h, fps = int(probe[0]), int(probe[1]), probe[2]
vf = "hflip" if a.mirror else "null"
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.inp, "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h*2}",
                        "-r", fps, "-i", "-", "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-pix_fmt", "yuv420p",
                        a.out], stdin=subprocess.PIPE)
n = w * h * 3
while True:
    buf = dec.stdout.read(n)
    if len(buf) < n:
        break
    f = np.frombuffer(buf, np.uint8).reshape(h, w, 3).astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    mx = np.maximum(r, b)
    e = g - mx
    alpha = 1.0 - np.clip((e - a.lo) / (a.hi - a.lo), 0, 1)
    g2 = np.where(e > 0, mx + np.minimum(e, 0) , g)  # despill: G <= max(R,B)
    col = np.stack([r, g2, b], -1) * alpha[..., None]  # premultiply toward black
    al = np.repeat((alpha * 255)[..., None], 3, -1)
    out = np.concatenate([col, al], 0).clip(0, 255).astype(np.uint8)
    enc.stdin.write(out.tobytes())
enc.stdin.close(); enc.wait(); dec.wait()
