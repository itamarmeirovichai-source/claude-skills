import json, base64, sys
from pathlib import Path
from el import call
from ana import speech_report
OUT = Path("/home/user/claude-skills/research/ai-video-reels/lab/experiments/E05_elevenlabs/a_voices")
LINES = {
 "fragrance": "Some things are never said... only remembered. Noir Vesper. The scent of after midnight.",
 "beverage": "Crack it open. Feel the cold hit. VOLT. Zero sugar. All charge.",
 "tech": "Your day, quietly organised. Halo listens, learns, and gets out of the way.",
}
CANDS = {
 "fragrance": [("goT3UYdM9bhm0n2lmKQx","Edward-british-dark-seductive"),("Se2Vw1WbHmGbBbyWTuu4","Allison-velvety-british-F"),
               ("qFjcP4hHD9WIdODvuJOJ","Jenna-soft-sultry-F"),("pFZP5JQG7iQjIQuC4Bku","Lily-premade-velvety-F"),("j9jfwdrw7BRfcR43Qohk","Frederick-smooth-velvety-M")],
 "beverage": [("BuaKXS4Sv1Mccaw3flfU","Christina-energetic-commercial-F"),("IKne3meq5aSn9XLyUdCD","Charlie-premade-hyped-M"),
              ("TX3LPaxmHKxFdv7VOQHJ","Liam-premade-energetic-M"),("xctasy8XvGp2cVO9HL9k","Allison-bubbly-F")],
 "tech": [("OYTbf65OHHFELVut7v2H","Hope-natural-calm-F"),("rNzVNTrvSffyxdrTbLKv","Miles-technical-british-M"),("SAz9YHcvj6GT2YYXdXww","River-premade-neutral"),
          ("CXoGcuszI2UkuF6sqV8W","EmilyE-premium-british-F"),("HaUDdkOAoitiVjpiet1i","Lucius-calm-reassuring-M")],
}
SET = {"fragrance": dict(stability=0.5, similarity_boost=0.75, style=0.0, use_speaker_boost=True, speed=0.9),
       "beverage": dict(stability=0.5, similarity_boost=0.75, style=0.0, use_speaker_boost=True, speed=1.05),
       "tech": dict(stability=0.5, similarity_boost=0.75, style=0.0, use_speaker_boost=True, speed=1.0)}
res = {}
for niche, cands in CANDS.items():
    for vid, name in cands:
        f = OUT / f"{niche}_{name}.mp3"
        if not f.exists():
            r = call("POST", f"/v1/text-to-speech/{vid}", {"text": LINES[niche], "model_id": "eleven_v3", "voice_settings": SET[niche], "seed": 7},
                     {"output_format": "mp3_44100_128"}, raw=True)
            if isinstance(r, dict): print(name, r); continue
            f.write_bytes(r[0]); cost = r[1].get("Character-Cost")
        else: cost = None
        rep = speech_report(str(f), LINES[niche]); rep["voice_id"] = vid; rep["cost"] = cost
        res[f"{niche}/{name}"] = rep
        print(niche, name, {k: rep.get(k) for k in ("dur","speech_dur","wps","pauses","LUFS","LRA","f0_med","f0_range_st","centroid_hz","wer","cost")}, flush=True)
json.dump(res, open(OUT/"results.json","w"), indent=1)
