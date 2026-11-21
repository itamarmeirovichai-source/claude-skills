#!/usr/bin/env python3
"""ElevenLabs client for the ad pipeline (stdlib only): voiceover + word timings, SFX, music.

  check                                  plan + remaining credits (free)
  voices [--search Q]                    list voices (id, name, labels)
  tts "TEXT" --voice ID --out vo.mp3     voiceover + vo.words.json (word timings for reel-studio captions)
        [--model eleven_v4] [--stability 0.5] [--style S] [--speed X]
        (v4 is the default; style/speed are only sent when given, and v4 ignores them -> warning)
  sfx "PROMPT" --seconds 2.5 --out boom.mp3 [--loop] [--influence 0.4]
  music "PROMPT" --seconds 15 --out bed.mp3 [--with-vocals] [--model music_v2_5]
  music --plan plan.json --out bed.mp3   composition plan {"chunks":[{text,duration_ms,positive_styles,negative_styles}]};
                                         hard hits land on chunk boundaries; chunks >= 3 s; put "instrumental" in styles

Money guards (tts / sfx / music):
  --estimate        print the credit + USD estimate and whether the cache already has it; no call
  --max-credits N   per-call cap (default 2000): refuse when the estimate is higher
  cache             identical requests never pay twice: the audio is stored under
                    sha256(endpoint + output-defining fields: text/prompt, voice, model, settings,
                    seconds, plan, output format) in --cache-dir (default $ELEVEN_CACHE_DIR or
                    ~/.cache/ad-director/elevenlabs); the output path is NOT part of the key. --no-cache.
  Estimates use list rates (TTS 1 credit/char, 0.5 on turbo/flash; SFX 40 credits/s; music a
  conservative 50 credits/s) and ELEVEN_USD_PER_CREDIT (default 0.00022 = Creator plan). Billed
  credits are read from the `character-cost` response header when present.

Auth: ELEVENLABS_API_KEY in the environment, or ELEVEN_AUTH_VIA_PROXY=1 when a network secret
injects the `xi-api-key` header for api.elevenlabs.io (the key never reaches this process).
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = os.environ.get("ELEVEN_API_BASE", "https://api.elevenlabs.io").rstrip("/")
DEFAULT_TTS_MODEL = "eleven_v4"
OUTPUT_FORMAT = "mp3_44100_128"
DEFAULT_MAX_CREDITS = 2000
SFX_CREDITS_PER_S = 40.0          # docs, when duration is set
SFX_UNSET_SECONDS = 30.0          # duration chosen by the model: assume the 30 s maximum
MUSIC_CREDITS_PER_S = 50.0        # not published: conservative assumption, reconcile with the account
V3_STYLE, V3_SPEED = 0.3, 1.0


def usd_per_credit() -> float:
    return float(os.environ.get("ELEVEN_USD_PER_CREDIT", "0.00022"))


def tts_credits_per_char(model: str) -> float:
    m = model.lower()
    return 0.5 if ("turbo" in m or "flash" in m) else 1.0


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
    raw, headers = _call_full(method, path, body, query, retries, timeout)
    return raw, headers.get("Content-Type", "")


def _call_full(method: str, path: str, body: dict | None = None, query: dict | None = None,
               retries: int = 3, timeout: float = 300) -> tuple[bytes, dict]:
    url = f"{API}{path}" + (("?" + urllib.parse.urlencode(query)) if query else "")
    data = json.dumps(body).encode() if body is not None else None
    delay = 2.0
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, data=data, method=method, headers=_headers(body is not None))
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read(), {k: v for k, v in r.headers.items()}
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


# ───────────────────────── estimate / cap / cache ─────────────────────────

def estimate(kind: str, body: dict) -> dict:
    """Credits + USD for one request body (list rates, conservative). kind: tts | sfx | music."""
    if kind == "tts":
        credits = len(body.get("text", "")) * tts_credits_per_char(body.get("model_id", DEFAULT_TTS_MODEL))
        basis = f"{len(body.get('text', ''))} chars x {tts_credits_per_char(body.get('model_id', ''))}"
    elif kind == "sfx":
        secs = float(body.get("duration_seconds") or SFX_UNSET_SECONDS)
        credits, basis = secs * SFX_CREDITS_PER_S, f"{secs:g} s x {SFX_CREDITS_PER_S:g}"
    elif kind == "music":
        plan = body.get("composition_plan")
        ms = (sum(float(c.get("duration_ms") or 0) for c in plan.get("chunks") or plan.get("sections") or [])
              if isinstance(plan, dict) else float(body.get("music_length_ms") or 0))
        if not ms:
            raise SystemExit("refusing: music request has no length (music_length_ms or plan durations)")
        credits, basis = ms / 1000 * MUSIC_CREDITS_PER_S, f"{ms / 1000:g} s x {MUSIC_CREDITS_PER_S:g} (assumed)"
    else:
        raise ValueError(kind)
    credits = round(credits, 1)
    return {"credits": credits, "usd": round(credits * usd_per_credit(), 4), "basis": basis}


def cache_key(endpoint: str, body: dict, output_format: str = OUTPUT_FORMAT) -> str:
    """sha256 of the output-defining fields only (no output path, timestamps or retry state)."""
    blob = json.dumps({"endpoint": endpoint, "body": body, "format": output_format},
                      sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(blob.encode()).hexdigest()


def default_cache_dir() -> Path:
    return Path(os.environ.get("ELEVEN_CACHE_DIR") or Path.home() / ".cache" / "ad-director" / "elevenlabs")


def _cache_paths(cache_dir: Path, key: str) -> tuple[Path, Path]:
    h = key.split(":", 1)[1]
    return cache_dir / f"{h}.mp3", cache_dir / f"{h}.json"


def cache_lookup(cache_dir: Path | None, key: str) -> dict | None:
    if not cache_dir:
        return None
    audio, meta = _cache_paths(Path(cache_dir), key)
    if audio.exists() and meta.exists():
        return {"audio": audio, **json.loads(meta.read_text(encoding="utf-8"))}
    return None


def cache_store(cache_dir: Path | None, key: str, audio_bytes: bytes, meta: dict) -> None:
    if not cache_dir:
        return
    audio, mp = _cache_paths(Path(cache_dir), key)
    audio.parent.mkdir(parents=True, exist_ok=True)
    audio.write_bytes(audio_bytes)
    mp.write_text(json.dumps({**meta, "key": key, "at": time.strftime("%Y-%m-%dT%H:%M:%S")}, ensure_ascii=False),
                  encoding="utf-8")


def _guard(kind: str, body: dict, max_credits: float | None) -> dict:
    est = estimate(kind, body)
    if max_credits is not None and est["credits"] > max_credits:
        raise SystemExit(f"refusing to spend: {kind} estimate {est['credits']:g} credits (${est['usd']:.3f}) "
                         f"> per-call cap {max_credits:g} ({est['basis']}). Shorten it or raise --max-credits.")
    return est


def _billed(headers: dict) -> float | None:
    for k, v in headers.items():
        if k.lower() == "character-cost":
            try:
                return float(v)
            except ValueError:
                return None
    return None


def _resolve_cache(cache_dir) -> Path | None:
    if cache_dir is False:
        return None
    return Path(cache_dir) if cache_dir else default_cache_dir()


def tts_body(text: str, model: str = DEFAULT_TTS_MODEL, stability: float = 0.5, similarity: float = 0.75,
             style: float | None = None, speed: float | None = None) -> dict:
    vs = {"stability": stability, "similarity_boost": similarity, "use_speaker_boost": True}
    if model.startswith("eleven_v4"):
        ignored = [n for n, v in (("style", style), ("speed", speed)) if v is not None]
        if ignored:
            print(f"warning: {model} ignores {', '.join(ignored)}; use --model eleven_v3 when you need them",
                  file=sys.stderr)
    vs["style"] = V3_STYLE if style is None and not model.startswith("eleven_v4") else style
    vs["speed"] = V3_SPEED if speed is None and not model.startswith("eleven_v4") else speed
    vs = {k: v for k, v in vs.items() if v is not None}
    return {"text": text, "model_id": model, "voice_settings": vs}


def tts(text: str, voice: str, out: Path, model: str = DEFAULT_TTS_MODEL, stability: float = 0.5,
        similarity: float = 0.75, style: float | None = None, speed: float | None = None,
        max_credits: float | None = DEFAULT_MAX_CREDITS, cache_dir=None) -> dict:
    body = tts_body(text, model, stability, similarity, style, speed)
    key = cache_key(f"tts/{voice}", body)
    cdir = _resolve_cache(cache_dir)
    hit = cache_lookup(cdir, key)
    if hit:
        audio_bytes, alignment, billed, est = hit["audio"].read_bytes(), hit.get("alignment") or {}, None, None
    else:
        est = _guard("tts", body, max_credits)
        raw, headers = _call_full("POST", f"/v1/text-to-speech/{urllib.parse.quote(voice)}/with-timestamps", body,
                                  {"output_format": OUTPUT_FORMAT})
        r = json.loads(raw)
        audio_bytes = base64.b64decode(r["audio_base64"])
        alignment = r.get("normalized_alignment") or r.get("alignment") or {}
        billed = _billed(headers)
        cache_store(cdir, key, audio_bytes, {"kind": "tts", "alignment": alignment, "credits_billed": billed})
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(audio_bytes)
    words = chars_to_words(alignment)
    wj = out.with_suffix(".words.json")
    wj.write_text(json.dumps({"words": words}, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"audio": str(out), "words": str(wj), "n_words": len(words),
            "duration": words[-1]["end"] if words else None, "model": model, "cached": bool(hit),
            "cache_key": key, "est_credits": est and est["credits"], "est_usd": est and est["usd"],
            "credits_billed": billed}


def _simple(kind: str, path: str, body: dict, out: Path, max_credits, cache_dir, timeout: float = 300) -> dict:
    key = cache_key(path, body)
    cdir = _resolve_cache(cache_dir)
    hit = cache_lookup(cdir, key)
    est = billed = None
    if hit:
        data = hit["audio"].read_bytes()
    else:
        est = _guard(kind, body, max_credits)
        data, headers = _call_full("POST", path, body, {"output_format": OUTPUT_FORMAT}, timeout=timeout)
        billed = _billed(headers)
        cache_store(cdir, key, data, {"kind": kind, "credits_billed": billed})
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    return {"audio": str(out), "cached": bool(hit), "cache_key": key, "est_credits": est and est["credits"],
            "est_usd": est and est["usd"], "credits_billed": billed}


def sfx_body(prompt: str, seconds: float | None, loop: bool = False, influence: float = 0.3) -> dict:
    body = {"text": prompt, "prompt_influence": influence, "loop": loop}
    if seconds:
        body["duration_seconds"] = seconds
    return body


def sfx(prompt: str, seconds: float | None, out: Path, loop: bool = False, influence: float = 0.3,
        max_credits: float | None = DEFAULT_MAX_CREDITS, cache_dir=None) -> dict:
    return _simple("sfx", "/v1/sound-generation", sfx_body(prompt, seconds, loop, influence), out,
                   max_credits, cache_dir)


def music_body(prompt: str | None, seconds: float | None, instrumental: bool = True,
               model: str = "music_v2_5", plan: dict | None = None) -> dict:
    # without model_id the API falls back to music_v1; force_instrumental is rejected (422) together with a plan
    if plan is not None:
        return {"composition_plan": plan, "model_id": model}
    return {"prompt": prompt, "music_length_ms": int(seconds * 1000), "force_instrumental": instrumental,
            "model_id": model}


def music(prompt: str | None, seconds: float | None, out: Path, instrumental: bool = True,
          model: str = "music_v2_5", plan: dict | None = None,
          max_credits: float | None = DEFAULT_MAX_CREDITS, cache_dir=None) -> dict:
    return _simple("music", "/v1/music", music_body(prompt, seconds, instrumental, model, plan), out,
                   max_credits, cache_dir, timeout=600)


def preview(kind: str, body: dict, endpoint: str, cache_dir=None) -> dict:
    """What a call would cost and whether the cache already has it (no network)."""
    key = cache_key(endpoint, body)
    return {**estimate(kind, body), "cache_key": key, "cached": cache_lookup(_resolve_cache(cache_dir), key) is not None}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="elevenlabs.py", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    v = sub.add_parser("voices"); v.add_argument("--search", default=None)
    t = sub.add_parser("tts"); t.add_argument("text"); t.add_argument("--voice", required=True)
    t.add_argument("--out", required=True); t.add_argument("--model", default=DEFAULT_TTS_MODEL)
    t.add_argument("--stability", type=float, default=0.5); t.add_argument("--style", type=float, default=None)
    t.add_argument("--speed", type=float, default=None)
    s = sub.add_parser("sfx"); s.add_argument("prompt"); s.add_argument("--seconds", type=float)
    s.add_argument("--out", required=True); s.add_argument("--loop", action="store_true")
    s.add_argument("--influence", type=float, default=0.3)
    m = sub.add_parser("music"); m.add_argument("prompt", nargs="?"); m.add_argument("--seconds", type=float)
    m.add_argument("--plan", default=None); m.add_argument("--model", default="music_v2_5")
    m.add_argument("--out", required=True); m.add_argument("--with-vocals", action="store_true")
    for x in (t, s, m):
        x.add_argument("--max-credits", type=float, default=DEFAULT_MAX_CREDITS, help="per-call cap")
        x.add_argument("--estimate", action="store_true", help="print estimate + cache status; no call")
        x.add_argument("--cache-dir", default=None)
        x.add_argument("--no-cache", action="store_true")
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
    elif a.cmd in ("tts", "sfx", "music"):
        cache = False if a.no_cache else a.cache_dir
        if a.cmd == "tts":
            body, ep = tts_body(a.text, a.model, a.stability, 0.75, a.style, a.speed), f"tts/{a.voice}"
        elif a.cmd == "sfx":
            body, ep = sfx_body(a.prompt, a.seconds, a.loop, a.influence), "/v1/sound-generation"
        else:
            plan = None
            if a.plan:
                plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
                plan = plan.get("composition_plan", plan)
            elif not (a.prompt and a.seconds):
                ap.error("music needs PROMPT --seconds, or --plan")
            body, ep = music_body(a.prompt, a.seconds, not a.with_vocals, a.model, plan), "/v1/music"
        if a.estimate:
            print(json.dumps(preview(a.cmd, body, ep, cache), indent=1))
            return 0
        if a.cmd == "tts":
            r = tts(a.text, a.voice, Path(a.out), a.model, a.stability, 0.75, a.style, a.speed, a.max_credits, cache)
        elif a.cmd == "sfx":
            r = sfx(a.prompt, a.seconds, Path(a.out), a.loop, a.influence, a.max_credits, cache)
        else:
            r = music(a.prompt, a.seconds, Path(a.out), not a.with_vocals, a.model, plan, a.max_credits, cache)
        print(json.dumps(r, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
