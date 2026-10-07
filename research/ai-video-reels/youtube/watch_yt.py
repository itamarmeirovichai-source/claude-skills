"""Download a tutorial at low res, extract one frame per scene change (min every 20 s), tile into timestamped contact sheets."""
import subprocess, sys, pathlib, json, glob, os
ids = sys.argv[1:]
for vid in ids:
    out = pathlib.Path("frames")/vid; out.mkdir(parents=True, exist_ok=True)
    if list(out.glob("sheet_*.jpg")): print(vid, "skip"); continue
    src = f"/tmp/claude-0/ytv/{vid}.mp4"
    subprocess.run(["yt-dlp","-f","bv*[height<=480][ext=mp4]/bv*[height<=480]/best[height<=480]","--no-audio","-o",src,f"https://youtu.be/{vid}"],capture_output=True,timeout=900)
    if not os.path.exists(src):
        c = glob.glob(f"/tmp/claude-0/ytv/{vid}.*"); src = c[0] if c else None
    if not src: print(vid, "download failed"); continue
    # scene-change frames plus a frame at least every 20 s, with burnt-in timestamp
    vf = ("select='gt(scene,0.32)+isnan(prev_selected_t)+gte(t-prev_selected_t,20)',"
          "scale=320:-2,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='%{pts\\:hms}':x=4:y=4:fontsize=14:fontcolor=yellow:box=1:boxcolor=black@0.6")
    subprocess.run(["ffmpeg","-v","error","-i",src,"-vf",vf,"-vsync","vfr","-q:v","4",str(out/"f_%04d.jpg")],timeout=900)
    fs = sorted(out.glob("f_*.jpg"))
    for i in range(0, len(fs), 20):
        chunk = fs[i:i+20]
        subprocess.run(["ffmpeg","-v","error","-y","-pattern_type","glob","-i",str(out/"f_*.jpg"),"-vf",
                        f"select='between(n\\,{i}\\,{i+len(chunk)-1})',tile=5x4:padding=4",
                        "-frames:v","1","-q:v","5",str(out/f"sheet_{i//20+1:02d}.jpg")])
    for f in fs: f.unlink()
    os.remove(src)
    print(vid, len(fs), "frames ->", len(list(out.glob('sheet_*.jpg'))), "sheets")
