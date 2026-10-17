import json, numpy as np, subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from el import call
from ana import dec, loud, centroid
OUT = Path("/home/user/claude-skills/research/ai-video-reels/lab/experiments/E05_elevenlabs/e_sonic_logo"); OUT.mkdir(exist_ok=True)
J = [
 ("sfx_fragrance_crystal", "sfx", "Luxury fragrance sonic logo: one crystal glass chime struck once, then a warm low felt-piano note underneath, soft shimmering reverb tail, elegant, no voice, no drums", 0.6),
 ("sfx_beverage_snap", "sfx", "Energy drink sonic logo: sharp can-tab snap, quick rising synth swoosh, landing on one punchy sub-bass hit with a short fizz tail, no voice", 0.6),
 ("sfx_tech_3note", "sfx", "Tech brand sonic logo: three-note ascending glass marimba motif, E then G sharp then B, clean and modern, last note sustains, no voice, no drums", 0.7),
 ("music_tech_3note", "music", "Sonic logo, 3 seconds: three-note ascending glass marimba motif E, G sharp, B, then a soft warm synth pad chord in E major rings out. Clean, modern tech brand. Instrumental, no drums.", None),
]
def note(f):
    n = 12*np.log2(f/440)+69; names = "C C# D D# E F F# G G# A A# B".split(); return f"{names[int(round(n))%12]}{int(round(n))//12-1}"
def run(j):
    name, kind, text, inf = j; f = OUT/f"{name}.mp3"
    if not f.exists():
        if kind == "sfx": r = call("POST", "/v1/sound-generation", {"text": text, "prompt_influence": inf, "duration_seconds": 2.0}, {"output_format": "mp3_44100_128"}, raw=True)
        else: r = call("POST", "/v1/music", {"prompt": text, "music_length_ms": 3000, "model_id": "music_v2_5", "force_instrumental": True}, {"output_format": "mp3_44100_128"}, raw=True, timeout=900)
        if isinstance(r, dict): return name, {"err": r}
        f.write_bytes(r[0])
    x, sr = dec(str(f), 22050); h = int(0.02*sr)
    env = 20*np.log10(np.array([np.sqrt((x[i:i+h]**2).mean()) for i in range(0, len(x)-h, h)])+1e-9)
    pk = env.max(); on = int(np.argmax(env > pk-20))*0.02
    # simple onset list: rises > 6 dB within 40 ms
    ons = [round(i*0.02,2) for i in range(2, len(env)) if env[i]-env[i-2] > 6 and env[i] > pk-30]
    ons2 = [o for k,o in enumerate(ons) if k==0 or o-ons[k-1] > 0.08]
    notes = []
    for o in ons2[:5]:
        seg = x[int((o+0.03)*sr):int((o+0.23)*sr)]
        if len(seg) < 1000: continue
        X = np.abs(np.fft.rfft(seg*np.hanning(len(seg)))); fr = np.fft.rfftfreq(len(seg), 1/sr); m = (fr > 80) & (fr < 3000)
        notes.append(note(fr[m][np.argmax(X[m])]))
    end = len(env)-1-int(np.argmax(env[::-1] > pk-40))
    return name, {"text": text, "dur": round(len(x)/sr,2), "onset": round(on,2), "onsets": ons2, "notes_at_onsets": notes, "decay_to_-40dB_s": round(end*0.02,2), **loud(str(f)), "centroid_hz": centroid(x, sr)}
with ThreadPoolExecutor(4) as ex: res = dict(ex.map(run, J))
for k, v in res.items(): print(k, {a: b for a, b in v.items() if a != "text"})
json.dump(res, open(OUT/"results.json", "w"), indent=1)
