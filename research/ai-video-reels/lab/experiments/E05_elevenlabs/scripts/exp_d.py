import json, numpy as np
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from el import call
from ana import dec, loud, centroid, stt
OUT = Path("/home/user/claude-skills/research/ai-video-reels/lab/experiments/E05_elevenlabs/d_sfx"); OUT.mkdir(exist_ok=True)
F = "Close-mic'd studio foley, dry, no music: "
S = {
 "glass_cap": (1.5, "glass perfume bottle cap", F+"heavy faceted glass stopper set down onto a glass perfume bottle, one crisp clink with a short bright ring"),
 "spray_mist": (1.5, "perfume spray", F+"one short perfume atomizer spray, soft pump click then a fine pressurized mist hiss"),
 "can_crack": (2.0, "soda can opening", F+"aluminium can tab cracked open, sharp metallic snap followed by carbonation fizz hiss"),
 "pour": (3.0, "pouring drink", F+"sparkling soda poured into a tall glass over ice, liquid glug and rising fizzing bubbles"),
 "ice": (2.0, "ice cubes", F+"three ice cubes dropped one by one into an empty crystal tumbler, bright clinks and a short crackle"),
 "fabric": (2.0, "fabric movement", F+"a single slow sweep of heavy silk satin, soft airy swish"),
 "click": (0.8, "button click", F+"one premium tactile click of a small machined aluminium button, ultra short and crisp"),
 "whoosh": (1.2, "whoosh", "Cinematic transition whoosh, fast air pass-by with a deep low-end swell, clean, no music"),
}
jobs = []
for k, (d, plain, pro) in S.items():
    jobs += [(f"{k}__plain_i03", plain, 0.3, d), (f"{k}__pro_i03", pro, 0.3, d), (f"{k}__pro_i08", pro, 0.8, d)]
def run(j):
    name, text, inf, d = j; f = OUT/f"{name}.mp3"
    if not f.exists():
        r = call("POST", "/v1/sound-generation", {"text": text, "prompt_influence": inf, "duration_seconds": d}, {"output_format": "mp3_44100_128"}, raw=True)
        if isinstance(r, dict): return name, {"err": r}
        f.write_bytes(r[0])
    x, sr = dec(str(f), 22050); h = int(0.01*sr)
    env = np.array([np.sqrt((x[i:i+h]**2).mean()) for i in range(0, len(x)-h, h)]); pk = env.max()
    on = int(np.argmax(env > pk*0.1)); act = (env > pk*0.03).sum()*0.01
    crest = 20*np.log10(np.abs(x).max()/(np.sqrt((x**2).mean())+1e-9))
    t = stt(str(f))
    return name, {"text": text, "influence": inf, "dur": round(len(x)/sr,2), "onset_s": round(on*0.01,2), "active_s": round(float(act),2),
                  "peak_t": round(int(np.argmax(env))*0.01,2), "crest_db": round(float(crest),1), "centroid_hz": centroid(x, sr), **loud(str(f)), "stt_events": t.get("text") if isinstance(t, dict) else None}
with ThreadPoolExecutor(4) as ex: res = dict(ex.map(run, jobs))
for k, v in res.items(): print(k, {a: v.get(a) for a in ("dur","onset_s","active_s","peak_t","crest_db","centroid_hz","LUFS","stt_events","err")})
json.dump(res, open(OUT/"results.json", "w"), indent=1)
