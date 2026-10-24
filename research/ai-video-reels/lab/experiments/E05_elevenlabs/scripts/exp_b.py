import json
from pathlib import Path
from el import call
from ana import speech_report
OUT = Path("/home/user/claude-skills/research/ai-video-reels/lab/experiments/E05_elevenlabs/b_tags"); OUT.mkdir(exist_ok=True)
V = "qFjcP4hHD9WIdODvuJOJ"  # Jenna soft sultry
VAR = [
 ("01_plain", "eleven_v3", 0.5, "Noir Vesper. The scent of after midnight."),
 ("02_whispers", "eleven_v3", 0.5, "[whispers] Noir Vesper. The scent of after midnight."),
 ("03_softly", "eleven_v3", 0.5, "[softly] Noir Vesper. The scent of after midnight."),
 ("04_ellipses", "eleven_v3", 0.5, "Noir Vesper... the scent of... after midnight."),
 ("05_caps", "eleven_v3", 0.5, "Noir Vesper. The scent of AFTER midnight."),
 ("06_combo", "eleven_v3", 0.5, "[softly] Noir Vesper... [whispers] the scent of after MIDNIGHT."),
 ("07_descriptive", "eleven_v3", 0.5, "[breathy, intimate, slow] Noir Vesper... the scent of after midnight."),
 ("08_combo_creative0", "eleven_v3", 0.0, "[softly] Noir Vesper... [whispers] the scent of after MIDNIGHT."),
 ("09_combo_robust1", "eleven_v3", 1.0, "[softly] Noir Vesper... [whispers] the scent of after MIDNIGHT."),
 ("10_exhale", "eleven_v3", 0.5, "[exhales] Noir Vesper. [pause] The scent of after midnight."),
 ("11_v4_whispers", "eleven_v4", 0.5, "[whispers] Noir Vesper. The scent of after midnight."),
 ("12_v4_combo", "eleven_v4", 0.5, "[softly] Noir Vesper... [whispers] the scent of after MIDNIGHT."),
 ("13_v4_descriptive", "eleven_v4", 0.5, "[low, breathy, intimate voice, slow] Noir Vesper... the scent of after midnight."),
]
res = {}
for name, model, st, text in VAR:
    f = OUT / f"{name}.mp3"; cost=None
    if not f.exists():
        r = call("POST", f"/v1/text-to-speech/{V}", {"text": text, "model_id": model, "seed": 11,
                 "voice_settings": {"stability": st, "similarity_boost": 0.75}}, {"output_format": "mp3_44100_128"}, raw=True)
        if isinstance(r, dict): print(name, r); continue
        f.write_bytes(r[0]); cost = r[1].get("Character-Cost")
    rep = speech_report(str(f), text); rep.update(text=text, model=model, stability=st, cost=cost); res[name] = rep
    print(name, {k: rep.get(k) for k in ("dur","pauses","LUFS","voiced","f0_med","f0_range_st","centroid_hz","wer","cost")}, "|", rep.get("stt"), flush=True)
json.dump(res, open(OUT/"results.json","w"), indent=1)
