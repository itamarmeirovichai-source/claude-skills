"""Design a permanent ElevenLabs voice per character (text-to-voice design -> 3 previews).
Usage: ELEVEN_AUTH_VIA_PROXY=1 python3 design.py otto|vee   (writes previews/<char>_<n>.mp3 + <char>_design.json)"""
import base64, json, sys
from pathlib import Path
sys.path.insert(0, "/home/user/claude-skills/skills/ad-director/scripts")
import elevenlabs as el

CHAR = {
 "otto": {"desc": "A man in his mid-fifties with a deep, dry, velvety baritone and a subtle continental European accent, somewhere between French and Italian. Slow, deadpan, theatrical timing; amused and knowing, like a legendary film director who finds everything slightly funny. Warm low resonance, crisp consonants, intimate close-mic studio recording.",
          "text": "Quiet on set. This candle has never been filmed. Watch the light crawl across the glass, slowly, like it is remembering summer. One take. No cuts. Then we roll."},
 "vee":  {"desc": "A woman in her late thirties with a crisp, confident, slightly husky mid-Atlantic voice. Quick, precise and dry-witted, like a top film producer who runs every project on a stopwatch. Bright, clear, warm when she smiles, close-mic studio recording.",
          "text": "How much did your last product shoot cost? Don't answer. Send us one photo, we send back five frames, free. Frames by Thursday. I'm counting. Link in bio."},
}
c = sys.argv[1]
r = json.loads(el._call("POST", "/v1/text-to-voice/design", {"voice_description": CHAR[c]["desc"], "text": CHAR[c]["text"], "model_id": "eleven_ttv_v3"})[0])
out = Path("previews"); out.mkdir(exist_ok=True)
prev = r.get("previews") or []
meta = []
for i, p in enumerate(prev, 1):
    (out / f"{c}_{i}.mp3").write_bytes(base64.b64decode(p["audio_base_64"]))
    meta.append({"n": i, "generated_voice_id": p["generated_voice_id"], "duration": p.get("duration_secs")})
Path(f"{c}_design.json").write_text(json.dumps({"description": CHAR[c]["desc"], "text": CHAR[c]["text"], "previews": meta}, indent=1))
print(c, len(meta), "previews")
