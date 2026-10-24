import json, sys
from pathlib import Path
from el import call
OUT = Path("/home/user/claude-skills/research/ai-video-reels/lab/experiments/E05_elevenlabs/c_music")
BEV2 = {"chunks": [
 {"text": "[Intro]\n{near silence}", "duration_ms": 3000,
  "positive_styles": ["minimal electronic", "premium energy drink commercial", "124 BPM", "F minor", "instrumental", "single sub-bass hum only", "very quiet", "pristine modern production"],
  "negative_styles": ["vocals", "drums", "melody", "loud"], "context_adherence": "high"},
 {"text": "[Build]\n{filtered kick}\n{riser}\n{drop gap}", "duration_ms": 6000,
  "positive_styles": ["low-pass filtered kick", "white-noise riser", "tension building fast", "ends with a half-beat of silence"],
  "negative_styles": ["vocals", "full drop"], "context_adherence": "high"},
 {"text": "[Drop]\n{drop hits on the first beat}", "duration_ms": 6000,
  "positive_styles": ["drop starts immediately on beat one", "punchy kick and clap", "distorted synth stabs", "maximum energy"],
  "negative_styles": ["vocals", "intro", "build-up", "fade in"], "context_adherence": "high"},
 {"text": "[Break]\n{silence}", "duration_ms": 3000,
  "positive_styles": ["hard stop", "total silence", "tape stop"],
  "negative_styles": ["drums", "bass", "melody", "vocals"], "context_adherence": "low"},
 {"text": "[Outro]\n{one huge impact}\n{chord rings out}", "duration_ms": 4000,
  "positive_styles": ["one massive cinematic impact on the downbeat", "loud", "F minor stab chord with long reverb tail", "brand sonic logo"],
  "negative_styles": ["vocals", "silence", "fade in", "quiet"], "context_adherence": "low"}]}
FRAG = {"chunks": [
 {"text": "[Intro]\n{room tone}", "duration_ms": 3000,
  "positive_styles": ["luxury fragrance commercial", "cinematic neo-classical", "72 BPM", "D minor", "instrumental", "felt piano single notes", "close-mic'd, intimate", "tape warmth", "very sparse"],
  "negative_styles": ["vocals", "drums", "EDM", "bright pop"], "context_adherence": "high"},
 {"text": "[Swell]", "duration_ms": 8000,
  "positive_styles": ["low cello drone enters", "slow string swell", "breathy pads", "growing warmth"],
  "negative_styles": ["vocals", "percussion", "fast tempo"], "context_adherence": "high"},
 {"text": "[Peak]", "duration_ms": 5000,
  "positive_styles": ["full lush strings", "deep timpani-like low pulse", "emotional peak", "wide cinematic reverb"],
  "negative_styles": ["vocals", "EDM drop", "trap drums"], "context_adherence": "high"},
 {"text": "[Resolve]\n{final chord}", "duration_ms": 4000,
  "positive_styles": ["single sustained piano and string chord", "D major resolution", "long natural decay"],
  "negative_styles": ["vocals", "new melody", "abrupt cut"], "context_adherence": "medium"}]}
which = sys.argv[1]; plan = {"bev2": BEV2, "frag": FRAG}[which]
r = call("POST", "/v1/music", {"composition_plan": plan, "model_id": "music_v2_5"}, {"output_format": "mp3_44100_128"}, raw=True, timeout=900)
if isinstance(r, dict): print(r); sys.exit(1)
f = OUT / f"plan_v25_{which}.mp3"; f.write_bytes(r[0]); json.dump(plan, open(f.with_suffix(".request.json"), "w"), indent=1); print(f, r[1].get("Song-Id"))
