import sys, json, numpy as np
from ana import dec, loud, silences, stt
def analyse(path, bounds):
    x, sr = dec(path, 22050); dur = len(x)/sr
    hop = int(0.25*sr); env = [20*np.log10(np.sqrt((x[i:i+hop]**2).mean())+1e-9) for i in range(0, len(x)-hop+1, hop)]
    secs = []
    for name, a, b in bounds:
        seg = x[int(a*sr):int(min(b,dur)*sr)]
        if len(seg)==0: continue
        rms = 20*np.log10(np.sqrt((seg**2).mean())+1e-9)
        # spectral flux-ish: low band energy share (<150 Hz) for kick/bass presence
        X = np.abs(np.fft.rfft(seg)); f = np.fft.rfftfreq(len(seg), 1/sr)
        low = X[f<150].sum()/X.sum()
        secs.append({"section": name, "t": f"{a}-{b}", "rms_db": round(float(rms),1), "low_share": round(float(low),2)})
    # BPM via autocorrelation of onset envelope in the loudest 6 s
    h2 = 512; e = np.array([np.sqrt((x[i:i+h2]**2).mean()) for i in range(0, len(x)-h2, h2)]); od = np.maximum(0, np.diff(e))
    fps = sr/h2; ac = np.correlate(od-od.mean(), od-od.mean(), "full")[len(od)-1:]
    lags = np.arange(len(ac)); bpm_l = (lags > fps*60/180) & (lags < fps*60/70)
    bpm = 60*fps/lags[bpm_l][np.argmax(ac[bpm_l])]
    return {"dur": round(dur,2), **loud(path), "bpm_est": round(float(bpm),1), "sections": secs,
            "env_0.25s": [round(float(v)) for v in env], "silences_-40": [(round(a,2), round(b,2) if b else None) for a,b in silences(path, -40, 0.3)]}
if __name__ == "__main__":
    B = [("hook",0,3),("build",3,9),("drop",9,15),("breath",15,18),("resolve",18,22)]
    res = {}
    for p in sys.argv[1:]:
        r = analyse(p, B); t = stt(p); r["stt_text"] = t.get("text") if isinstance(t, dict) else None; res[p] = r
        print(p); print(json.dumps({k:v for k,v in r.items()}, indent=None))
    json.dump(res, open(sys.argv[1].rsplit("/",1)[0]+"/analysis.json","w"), indent=1)
