import json, sys
from pathlib import Path
from el import call
OUT = Path("/home/user/claude-skills/research/ai-video-reels/lab/experiments/E05_elevenlabs/c_music"); OUT.mkdir(exist_ok=True)
PLAN = {"chunks": [
 {"text": "[Hook]\n{near silence}", "duration_ms": 3000,
  "positive_styles": ["minimal electronic", "dark luxury energy drink ad", "near silence", "single sub-bass hum and faint vinyl room tone", "very quiet", "124 BPM", "F minor", "instrumental", "pristine modern production"],
  "negative_styles": ["vocals", "drums", "melody", "loud", "full band"], "context_adherence": "high"},
 {"text": "[Build]\n{filtered riser}", "duration_ms": 6000,
  "positive_styles": ["low-pass filtered four-on-the-floor kick fading in", "rising white-noise riser", "pulsing sidechained synth bass", "building tension", "filter slowly opening"],
  "negative_styles": ["vocals", "full drop", "breakdown"], "context_adherence": "high"},
 {"text": "[Drop]\n{full energy}", "duration_ms": 6000,
  "positive_styles": ["full drop", "punchy kick and clap", "wide distorted synth stabs", "maximum energy", "sidechained bass"],
  "negative_styles": ["vocals", "quiet", "ambient", "fade"], "context_adherence": "high"},
 {"text": "[Breath]\n{everything stops}", "duration_ms": 3000,
  "positive_styles": ["sudden full stop", "silence", "only a short reverb tail decaying", "dead air before the logo"],
  "negative_styles": ["drums", "bass", "melody", "vocals", "riser"], "context_adherence": "low"},
 {"text": "[Resolve]\n{logo sting}", "duration_ms": 4000,
  "positive_styles": ["single big final hit", "resolving F minor chord ringing out", "long reverb tail", "clean ending"],
  "negative_styles": ["vocals", "new groove", "abrupt cut"], "context_adherence": "medium"}]}
which = sys.argv[1]
if which == "plan":
    body = {"composition_plan": PLAN, "model_id": "music_v2_5"}
    f = OUT/"plan_v25_beverage_22s.mp3"
else:
    body = {"prompt": ("Dark luxury energy drink ad, minimal electronic, 124 BPM, F minor, instrumental. "
            "0:00-0:03 near silence, just a sub-bass hum. 0:03-0:09 build: filtered kick fades in with a white-noise riser. "
            "0:09-0:15 full drop, punchy kick, distorted synth stabs. 0:15-0:18 everything stops dead, silence, only a reverb tail. "
            "0:18-0:22 one big final hit and a resolving chord ringing out."), "music_length_ms": 22000, "model_id": "music_v2_5", "force_instrumental": True}
    f = OUT/"prompt_v25_beverage_22s.mp3"
r = call("POST", "/v1/music", body, {"output_format": "mp3_44100_128"}, raw=True, timeout=900)
if isinstance(r, dict): print(r); sys.exit(1)
f.write_bytes(r[0]); print(f, {k: v for k, v in r[1].items() if k.lower().startswith(("song","character","x-","request"))})
json.dump(body, open(f.with_suffix(".request.json"), "w"), indent=1)
