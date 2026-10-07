"""Search YouTube and save English transcripts for study (transcripts are git-ignored; only notes are committed)."""
import json, subprocess, sys, pathlib
from concurrent.futures import ThreadPoolExecutor
from youtube_transcript_api import YouTubeTranscriptApi
THEMES = {
 "A_realism": ["how to make AI video look real not AI", "make AI generated video look less AI cinematic tips", "AI video realism film grain color grading tutorial",
               "why your AI videos look fake fix", "AI filmmaking realism tips Kling Seedance Veo"],
 "B_product_ai": ["AI product commercial tutorial Kling 3.0", "Seedance 2.0 product ad tutorial", "Higgsfield product ad tutorial",
                  "AI perfume commercial tutorial", "AI luxury product commercial workflow Nano Banana Kling"],
 "C_post": ["product commercial editing tutorial speed ramp sound design", "color grading AI footage davinci resolve tutorial",
            "sound design for product commercials tutorial", "how to edit a cinematic commercial premiere pro tutorial"],
 "D_cinematography": ["product commercial cinematography tutorial lighting", "perfume commercial lighting breakdown",
                      "how to shoot a cinematic product commercial", "beverage commercial behind the scenes macro tabletop"],
}
out = pathlib.Path("transcripts"); out.mkdir(exist_ok=True)
api = YouTubeTranscriptApi()
def search(q, n=8):
    r = subprocess.run(["yt-dlp","--flat-playlist","--print","%(id)s\t%(title)s\t%(channel)s\t%(duration)s",f"ytsearch{n}:{q}"],capture_output=True,text=True,timeout=120)
    return [l.split("\t") for l in r.stdout.strip().splitlines() if l.count("\t")==3]
def grab(item):
    vid, title, ch, dur, theme = item
    p = out/f"{theme}__{vid}.txt"
    if p.exists(): return "skip"
    try:
        import re, glob, time, os
        tmp = f"/tmp/claude-0/yt_{vid}"
        subprocess.run(["yt-dlp","--skip-download","--write-subs","--write-auto-subs","--sub-langs","en.*,en","--sub-format","vtt",
                        "-o",tmp,f"https://youtu.be/{vid}"],capture_output=True,timeout=120)
        fs = glob.glob(tmp+"*.vtt")
        if not fs: return "fail nosubs"
        lines, last = [], None
        for l in open(fs[0], encoding="utf-8", errors="ignore"):
            l = re.sub(r"<[^>]+>", "", l).strip()
            if not l or "-->" in l or l.startswith(("WEBVTT","Kind:","Language:")) or l == last: continue
            lines.append(l); last = l
        text = " ".join(dict.fromkeys(lines))
        for f in fs: os.remove(f)
        p.write_text(f"TITLE: {title}\nCHANNEL: {ch}\nURL: https://youtu.be/{vid}\nDURATION_S: {dur}\n\n{text}", encoding="utf-8")
        return f"ok {len(text)}"
    except Exception as e:
        return f"fail {type(e).__name__}"
items, seen = [], set()
for theme, qs in THEMES.items():
    for q in qs:
        for vid, title, ch, dur in search(q):
            try: d = float(dur)
            except: d = 0
            if vid in seen or d < 180 or d > 3600: continue
            seen.add(vid); items.append((vid, title, ch, dur, theme))
print("videos:", len(items))
with ThreadPoolExecutor(3) as ex:
    res = list(ex.map(grab, items))
print({k: sum(1 for r in res if r.startswith(k)) for k in ("ok","fail","skip")})
json.dump([dict(zip(["id","title","channel","duration","theme"], i)) for i in items], open("index.json","w"), indent=1)
