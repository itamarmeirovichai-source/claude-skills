#!/usr/bin/env python3
"""beatcut.py - cut a list of clips to the beat of a music track (CapCut "Auto beat" equivalent).

usage: python3 beatcut.py MUSIC OUT.mp4 clip1.mp4 clip2.mp4 ... [--every 2] [--start 0] [--max 15]
               [--punch] [--flash-downbeats] [--band low]
- runs beats.py, takes every Nth beat as a cut point, fills each interval with the next clip
  (cycling; each clip continues from where it was last used), scales/crops to 1080x1920@30.
- --punch: 1.0->1.08 zoom punch at every cut;  --flash-downbeats: 2-frame white flash on bar starts.
- audio = the music (trimmed, 0.3s fade-out). Mix SFX/voice afterwards.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", p]).strip())


def main():
    a = sys.argv[1:]
    def opt(k, d):
        return a[a.index(k) + 1] if k in a else d
    flags = {"--punch", "--flash-downbeats"}
    pos = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in
                                                                   ("--every", "--start", "--max", "--band"))]
    music, out, clips = pos[0], pos[1], pos[2:]
    every, start, mx = int(opt("--every", 2)), float(opt("--start", 0)), float(opt("--max", 15))
    bj = json.loads(subprocess.check_output([sys.executable, os.path.join(HERE, "beats.py"), music,
                                             "--every", str(every), "--band", opt("--band", "low")]))
    cuts = [c - start for c in bj["cuts"] if start <= c <= start + mx]
    if not cuts or cuts[0] > 0.05:
        cuts = [0.0] + cuts
    end = min(start + mx, dur(music)) - start
    cuts = [c for c in cuts if c < end - 0.2] + [end]
    cuts = sorted(set(round(c * 30) / 30 for c in cuts))  # snap to the 30 fps frame grid -> no drift
    down = set(round(d - start, 3) for d in bj["downbeats"])
    pos_in = {c: 0.0 for c in clips}
    parts, fg = [], []
    for i, (t0, t1) in enumerate(zip(cuts, cuts[1:])):
        c = clips[i % len(clips)]
        L = t1 - t0
        ss = pos_in[c]
        if ss + L > dur(c):
            ss = 0.0
        pos_in[c] = ss + L
        f = (f"[{clips.index(c)}:v]trim=start={ss:.3f}:duration={L:.3f},setpts=PTS-STARTPTS,"
             f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1")
        if "--punch" in a:
            f += (",scale=w='iw*(1+0.08*max(0,1-t/0.18))':h=-2:eval=frame,crop=1080:1920")
        if "--flash-downbeats" in a and any(abs(t0 - d) < 0.06 for d in down):
            f += ",eq=brightness=0.5:contrast=0.7:enable='lt(t,0.066)'"
        fg.append(f + f"[p{i}]")
        parts.append(f"[p{i}]")
    n = len(parts)
    fg.append("".join(parts) + f"concat=n={n}:v=1:a=0[v]")
    fg.append(f"[{len(clips)}:a]atrim=start={start}:duration={end:.3f},asetpts=PTS-STARTPTS,"
              f"afade=t=out:st={max(0, end - 0.3):.3f}:d=0.3[a]")
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    for c in clips:
        cmd += ["-i", c]
    cmd += ["-i", music, "-filter_complex", ";".join(fg), "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", out]
    subprocess.run(cmd, check=True)
    print(json.dumps({"bpm": bj["bpm"], "engine": bj["engine"], "cuts": [round(c, 3) for c in cuts], "segments": n}))


if __name__ == "__main__":
    main()
