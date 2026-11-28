#!/usr/bin/env python3
"""K0 poster: first frame of a stacked-alpha clip (premultiplied colour on top, alpha below) → RGBA WebP.
Usage: python3 scripts/otto-poster.py <clip.mp4> <out.webp> [width=540]"""
import subprocess, sys
import numpy as np
src, out = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 540
h = w * 16 // 9
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-frames:v', '1', '-vf', f'scale={w}:{h*2}:flags=lanczos,format=rgb24', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
img = np.frombuffer(raw, np.uint8).reshape(h * 2, w, 3).astype(np.float32)
col, a = img[:h], img[h:, :, :1] / 255.0
rgb = np.clip(col / np.maximum(a, 1e-3), 0, 255) * (a > 0.004)  # un-premultiply
rgba = np.concatenate([rgb, a * 255], axis=2).astype(np.uint8)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{w}x{h}', '-i', '-', '-c:v', 'libwebp', '-quality', '82', out], input=rgba.tobytes(), check=True)
print('poster', out)
