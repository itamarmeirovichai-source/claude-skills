#!/usr/bin/env python3
"""ElevenLabs client for the ad pipeline (stdlib only): voiceover + word timings, SFX, music.

  check                                  plan + remaining credits (free)
  voices [--search Q]                    list voices (id, name, labels)
  tts "TEXT" --voice ID --out vo.mp3     voiceover + vo.words.json (word timings for reel-studio captions)
        [--model eleven_v3] [--stability 0.5] [--style 0.3] [--speed 1.0]
  sfx "PROMPT" --seconds 2.5 --out boom.mp3 [--loop] [--influence 0.4]
  music "PROMPT" --seconds 15 --out bed.mp3 [--instrumental]

Auth: ELEVENLABS_API_KEY in the environment, or ELEVEN_AUTH_VIA_PROXY=1 when a network secret
injects the `xi-api-key` header for api.elevenlabs.io (the key never reaches this process).
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = os.environ.get("ELEVEN_API_BASE", "https://api.elevenlabs.io").rstrip("/")


class ElevenError(RuntimeError):
    def __init__(self, status: int, detail: str):
        super().__init__(f"HTTP {status}: {detail}")
        self.status = status


def _headers(json_body: bool) -> dict:
    h = {"Accept": "*/*"}
    key = os.environ.get("ELEVENLABS_API_KEY")
    if key:
        h["xi-api-key"] = key
    elif os.environ.get("ELEVEN_AUTH_VIA_PROXY") != "1":
        raise SystemExit("No ElevenLabs key: set ELEVENLABS_API_KEY, or ELEVEN_AUTH_VIA_PROXY=1 with a network "
                         "secret (header xi-api-key) for api.elevenlabs.io. Never paste keys into chat.")
    if json_body:
        h["Content-Type"] = "application/json"
    return h


def _call(method: str, path: str, body: dict | None = None, query: dict | None = None,
          retries: int = 3, timeout: float = 300) -> tuple[bytes, str]:
    url = f"{API}{path}" + (("?" + urllib.parse.urlencode(query)) if query else "")
    data = json.dumps(body).encode() if body is not None else None
    delay = 2.0
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, data=data, method=method, headers=_headers(body is not None))
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read(), r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as ex:
            raw = ex.read() or b""
            try:
                det = json.loads(raw).get("detail")
                det = det if isinstance(det, str) else json.dumps(det)
            except Exception:
                det = raw[:300].decode(errors="replace") or str(ex.reason)
            if (ex.code == 429 or ex.code >= 500) and attempt < retries:
                time.sleep(delay); delay *= 2
                continue
            raise ElevenError(ex.code, det) from None
        except (urllib.error.URLError, TimeoutError) as ex:
            if attempt < retries:
                time.sleep(delay); delay *= 2
                continue
            raise ElevenError(0, f"network: {ex}") from None
    raise ElevenError(0, "unreachable")


def chars_to_words(alignment: dict, offset: float = 0.0) -> list[dict]:
    """ElevenLabs character alignment -> [{start, end, text}] words (pure, unit-tested)."""
    chars = alignment.get("characters") or []
    st = alignment.get("character_start_times_seconds") or []
    en = alignment.get("character_end_times_seconds") or []
    words, cur, s0, e0 = [], "", None, None
    in_tag = False  # eleven_v3 audio tags like [sighs] are spoken directions, not caption words
    for c, a, b in zip(chars, st, en):
        if c == "[":
            in_tag = True
            continue
        if in_tag:
            in_tag = c != "]"
            continue
        if c.isspace():
            if cur:
                words.append({"start": round(s0 + offset, 3), "end": round(e0 + offset, 3), "text": cur})
            cur, s0, e0 = "", None, None
            continue
        if not cur:
            s0 = a
        cur += c
        e0 = b
    if cur:
        words.append({"start": round(s0 + offset, 3), "end": round(e0 + offset, 3), "text": cur})
    return words


def tts(text: str, voice: str, out: Path, model: str = "eleven_v3", stability: float = 0.5,
        similarity: float = 0.75, style: float = 0.3, speed: float = 1.0) -> dict:
    body = {"text": text, "model_id": model,
            "voice_settings": {"stability": stability, "similarity_boost": similarity, "style": style,
                               "use_speaker_boost": True, "speed": speed}}
    raw, _ = _call("POST", f"/v1/text-to-speech/{urllib.parse.quote(voice)}/with-timestamps", body,
                   {"output_format": "mp3_44100_128"})
    r = json.loads(raw)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(base64.b64decode(r["audio_base64"]))
    words = chars_to_words(r.get("normalized_alignment") or r.get("alignment") or {})
    wj = out.with_suffix(".words.json")
    wj.write_text(json.dumps({"words": words}, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"audio": str(out), "words": str(wj), "n_words": len(words),
            "duration": words[-1]["end"] if words else None}


def sfx(prompt: str, seconds: float | None, out: Path, loop: bool = False, influence: float = 0.4) -> str:
    body = {"text": prompt, "prompt_influence": influence, "loop": loop}
    if seconds:
        body["duration_seconds"] = seconds
    raw, _ = _call("POST", "/v1/sound-generation", body, {"output_format": "mp3_44100_128"})
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    return str(out)


def music(prompt: str, seconds: float, out: Path, instrumental: bool = True) -> str:
    body = {"prompt": prompt, "music_length_ms": int(seconds * 1000), "force_instrumental": instrumental}
    raw, _ = _call("POST", "/v1/music", body, {"output_format": "mp3_44100_128"}, timeout=600)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    return str(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="elevenlabs.py", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    v = sub.add_parser("voices"); v.add_argument("--search", default=None)
    t = sub.add_parser("tts"); t.add_argument("text"); t.add_argument("--voice", required=True)
    t.add_argument("--out", required=True); t.add_argument("--model", default="eleven_v3")
    t.add_argument("--stability", type=float, default=0.5); t.add_argument("--style", type=float, default=0.3)
    t.add_argument("--speed", type=float, default=1.0)
    s = sub.add_parser("sfx"); s.add_argument("prompt"); s.add_argument("--seconds", type=float)
    s.add_argument("--out", required=True); s.add_argument("--loop", action="store_true")
    s.add_argument("--influence", type=float, default=0.4)
    m = sub.add_parser("music"); m.add_argument("prompt"); m.add_argument("--seconds", type=float, required=True)
    m.add_argument("--out", required=True); m.add_argument("--with-vocals", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "check":
        raw, _ = _call("GET", "/v1/user/subscription")
        d = json.loads(raw)
        print(json.dumps({k: d.get(k) for k in ("tier", "status", "character_count", "character_limit",
                                                "next_character_count_reset_unix")}, indent=1))
    elif a.cmd == "voices":
        raw, _ = _call("GET", "/v2/voices", query={"search": a.search, "page_size": 50} if a.search else {"page_size": 50})
        for vv in json.loads(raw).get("voices", []):
            lab = vv.get("labels") or {}
            print(f"{vv['voice_id']}  {vv['name']:<28} {lab.get('gender','')}/{lab.get('age','')}/{lab.get('accent','')} {lab.get('description') or lab.get('descriptive','')}")
    elif a.cmd == "tts":
        print(json.dumps(tts(a.text, a.voice, Path(a.out), a.model, a.stability, 0.75, a.style, a.speed), indent=1))
    elif a.cmd == "sfx":
        print(sfx(a.prompt, a.seconds, Path(a.out), a.loop, a.influence))
    elif a.cmd == "music":
        print(music(a.prompt, a.seconds, Path(a.out), not a.with_vocals))
    return 0


if __name__ == "__main__":
    sys.exit(main())
