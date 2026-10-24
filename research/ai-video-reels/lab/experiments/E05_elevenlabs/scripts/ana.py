"""Audio analysis helpers: loudness, pitch, brightness, pauses, STT check."""
import subprocess, re, json, uuid, urllib.request, numpy as np
def dec(path, sr=16000):
    b = subprocess.run(["ffmpeg","-v","error","-i",path,"-ac","1","-ar",str(sr),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(b, np.float32), sr
def loud(path):
    e = subprocess.run(["ffmpeg","-nostats","-i",path,"-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr
    s = e[e.rfind("Summary:"):]
    g = lambda k: float(re.search(k+r":\s+(-?[\d.]+)", s).group(1)) if re.search(k+r":\s+(-?[\d.]+)", s) else None
    return {"LUFS": g("I"), "LRA": g("LRA"), "TP": g("Peak")}
def silences(path, db=-35, d=0.12):
    e = subprocess.run(["ffmpeg","-i",path,"-af",f"silencedetect=n={db}dB:d={d}","-f","null","-"],capture_output=True,text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", e)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", e)]
    return list(zip(st, en + [None]*(len(st)-len(en))))
def f0_stats(x, sr):
    fr = int(0.04*sr); hop = int(0.01*sr); f0=[]
    for i in range(0, len(x)-fr, hop):
        w = x[i:i+fr]*np.hanning(fr)
        if np.sqrt((w**2).mean()) < 0.01: continue
        ac = np.correlate(w, w, "full")[fr-1:]
        lo, hi = int(sr/400), int(sr/60)
        k = lo + np.argmax(ac[lo:hi])
        if ac[k] > 0.45*ac[0]: f0.append(sr/k)
    f0 = np.array(f0); nact = sum(1 for i in range(0, len(x)-fr, hop) if np.sqrt(((x[i:i+fr]*np.hanning(fr))**2).mean()) >= 0.01)
    if len(f0) < 5: return {"voiced": round(len(f0)/max(1,nact),2)}
    st = 12*np.log2(f0/np.median(f0))
    return {"voiced": round(len(f0)/max(1,nact),2), "f0_med": round(float(np.median(f0)),1), "f0_range_st": round(float(np.percentile(st,95)-np.percentile(st,5)),1)}
def centroid(x, sr):
    X = np.abs(np.fft.rfft(x[:sr*30]*1.0)); f = np.fft.rfftfreq(len(x[:sr*30]), 1/sr)
    return round(float((X*f).sum()/X.sum()))
def onset_env(path, sr=22050, hop=512):
    x,_ = dec(path, sr); n = len(x)//hop
    e = np.array([np.sqrt((x[i*hop:(i+1)*hop]**2).mean()+1e-12) for i in range(n)])
    return 20*np.log10(e+1e-9), hop/sr
def stt(path):
    bnd = uuid.uuid4().hex; body = b""
    def part(name, val, fn=None, ct=None):
        h = f'--{bnd}\r\nContent-Disposition: form-data; name="{name}"' + (f'; filename="{fn}"' if fn else "") + "\r\n" + (f"Content-Type: {ct}\r\n" if ct else "") + "\r\n"
        return h.encode() + val + b"\r\n"
    body += part("model_id", b"scribe_v2") + part("tag_audio_events", b"true") + part("file", open(path,"rb").read(), "a.mp3", "audio/mpeg") + f"--{bnd}--\r\n".encode()
    req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=body, method="POST", headers={"Content-Type": f"multipart/form-data; boundary={bnd}"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e: return {"_error": e.code, "_detail": e.read()[:300].decode(errors="replace")}
def wer(ref, hyp):
    n = lambda s: re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()
    r, h = n(ref), n(hyp); d = list(range(len(h)+1))
    for i in range(1, len(r)+1):
        p, d[0] = d[0], i
        for j in range(1, len(h)+1):
            p, d[j] = d[j], min(d[j]+1, d[j-1]+1, p+(r[i-1]!=h[j-1]))
    return round(d[len(h)]/max(1,len(r)),2)
def speech_report(path, ref=None, do_stt=True):
    x, sr = dec(path); dur = len(x)/sr
    sil = silences(path)
    lead = sil[0][1] if sil and sil[0][0] <= 0.01 and sil[0][1] else 0.0
    tail = (dur - sil[-1][0]) if sil and sil[-1][1] is None else 0.0
    inner = [(round(a,2), round(b-a,2)) for a,b in sil if b and a > 0.01]
    r = {"dur": round(dur,2), "lead_sil": round(lead,2), "tail_sil": round(tail,2), "speech_dur": round(dur-lead-tail,2),
         "pauses": inner, **loud(path), **f0_stats(x, sr), "centroid_hz": centroid(x, sr)}
    if ref:
        words = len(re.findall(r"[A-Za-z0-9']+", re.sub(r"\[[^\]]*\]", "", ref)))
        r["wps"] = round(words/max(0.1, r["speech_dur"]), 2)
    if do_stt and ref:
        t = stt(path); r["stt"] = t.get("text", t); r["wer"] = wer(re.sub(r"\[[^\]]*\]", "", ref), t.get("text","")) if "text" in t else None
    return r
