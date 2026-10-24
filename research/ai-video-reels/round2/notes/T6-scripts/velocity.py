#!/usr/bin/env python3
"""velocity.py - build an ffmpeg setpts expression for a smooth speed ramp (CapCut "Velocity"/"Montage" curve).

usage: python3 velocity.py "0:1,1.2:1,1.5:4,2.3:4,2.6:0.35,3.4:0.35,3.6:1" [--steps 8]
  points = source_time:speed pairs (speed 1 = normal, 4 = 4x fast, 0.35 = slow-mo).
  Between points the speed is eased (cosine) and integrated into piecewise-linear PTS.
prints: the setpts expression and the output duration.
"""
import math, sys


def build(points, steps=8):
    pts = sorted(points)
    # sample source time densely with eased speed, integrate dt/speed -> output time
    knots = [(pts[0][0], 0.0)]
    out = 0.0
    for (t0, s0), (t1, s1) in zip(pts, pts[1:]):
        n = steps if s0 != s1 else 1
        for i in range(n):
            a, b = t0 + (t1 - t0) * i / n, t0 + (t1 - t0) * (i + 1) / n
            m = (i + 0.5) / n
            e = (1 - math.cos(math.pi * m)) / 2  # ease in-out
            s = s0 + (s1 - s0) * e
            out += (b - a) / s
            knots.append((b, out))
    # nested if(): PTS*TB = source seconds (T); output seconds piecewise-linear
    expr = None
    for (a, oa), (b, ob) in reversed(list(zip(knots, knots[1:]))):
        k = (ob - oa) / (b - a)
        seg = f"{oa:.4f}+(T-{a:.4f})*{k:.4f}"
        expr = seg if expr is None else f"if(lt(T,{b:.4f}),{seg},{expr})"
    return f"({expr})/TB", out


if __name__ == "__main__":
    spec = sys.argv[1]
    steps = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    pts = [tuple(map(float, p.split(":"))) for p in spec.split(",")]
    e, d = build(pts, steps)
    print(e)
    print(f"# output duration ~ {d:.3f}s", file=sys.stderr)
