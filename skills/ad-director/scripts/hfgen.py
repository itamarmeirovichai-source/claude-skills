#!/usr/bin/env python3
"""hfgen: Higgsfield API runner for ad-director (stdlib only).

Commands
  check                         verify credentials (no generation, no cost)
  estimate MODEL --args JSON    price one request (no generation)
  run MODEL --args JSON --out DIR [--yes]
                                one generation: submit -> poll -> download
  batch PLAN.json --budget USD [--dry-run] [--yes] [--concurrency N]
                                a whole shot list: uploads local refs, estimates the total,
                                refuses above budget, runs takes in parallel, downloads,
                                writes manifest.json + gen_log.jsonl (resumable)
  status REQUEST_ID             current status of a request
  upload FILE                   upload a local image/video/audio -> public URL
  lint MODEL --args JSON        schema check + safe defaults for one request (free, offline)
  schemas [MODEL] [--import llms-full.txt]
                                list the known endpoint schemas, or rebuild hf_schemas.json from
                                https://docs.higgsfield.ai/docs/llms-full.txt

Credentials (environment only, never on the command line):
  HF_KEY="key_id:key_secret"   or   HF_API_KEY_ID + HF_API_KEY_SECRET
  or HF_AUTH_VIA_PROXY=1 when a network secret injects "Authorization: Key ..." for api.higgsfield.ai
  (also accepted: HF_API_KEY + HF_API_SECRET, or HIGGSFIELD_API_KEY="id:secret")

Model ids are endpoint paths from https://console.higgsfield.ai (for example
"kling-video/v2.5-turbo/pro/image-to-video"). Arguments are the model's JSON body.

Plan file (batch):
{
  "defaults": {"model": "kling-video/v2.5-turbo/pro/image-to-video", "takes": 2},
  "jobs": [
    {"id": "s1_hook", "model": "...", "takes": 3,
     "args": {"prompt": "...", "image_url": "@file:frames/r1.png", "duration": 5}}
  ]
}
"@file:<path>" values are uploaded first (path relative to the plan) and replaced by URLs.
Idempotency keys are derived from (job id, take, args), so re-running a batch after a crash
returns the same requests instead of paying twice. Use --fresh to force new generations.

Money guards (run before any upload or submit):
  * every job is checked against the endpoint's schema (scripts/hf_schemas.json, extracted from the
    public docs). Unknown fields are refused: /estimate silently ignores them, so a typo such as
    `end_image_url` on Kling (real name `last_image_url`) would be billed without the end frame.
    Models with no known schema are refused unless --allow-unvalidated.
  * safe defaults are injected unless the job sets the field: sound "off", generate_audio false,
    enhance_prompt / prompt_extend / enable_thinking / prompt_optimizer false, aspect_ratio "9:16".
  * a job that cannot be priced is refused (a dry run reports it as UNPRICED and exits 2) instead of
    being counted as $0. Kling multi-shot is priced on the summed shot durations.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import difflib
import hashlib
import json
import math
import mimetypes
import os
import random
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

API = os.environ.get("HF_API_BASE", "https://api.higgsfield.ai").rstrip("/")
TERMINAL = {"completed", "failed", "nsfw", "canceled"}
UPLOAD_TYPES = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp",
                ".gif": "image/gif", ".wav": "audio/wav", ".mp4": "video/mp4"}
_print_lock = threading.Lock()


class HFError(RuntimeError):
    def __init__(self, status: int, detail: str):
        super().__init__(f"HTTP {status}: {detail}")
        self.status, self.detail = status, detail


def log(*a):
    with _print_lock:
        print(*a, file=sys.stderr, flush=True)


# ───────────────────────── credentials / http ─────────────────────────

def credentials(env: dict | None = None, required: bool = True) -> str | None:
    """Key from the environment, or None when HF_AUTH_VIA_PROXY=1 (a network secret injects the header)."""
    e = os.environ if env is None else env
    if e.get("HF_KEY") and ":" in e["HF_KEY"]:
        return e["HF_KEY"].strip()
    for a, b in (("HF_API_KEY_ID", "HF_API_KEY_SECRET"), ("HF_API_KEY", "HF_API_SECRET")):
        if e.get(a) and e.get(b):
            return f"{e[a].strip()}:{e[b].strip()}"
    if e.get("HIGGSFIELD_API_KEY") and ":" in e["HIGGSFIELD_API_KEY"]:
        return e["HIGGSFIELD_API_KEY"].strip()
    if e.get("HF_AUTH_VIA_PROXY") == "1" or not required:
        return None
    raise SystemExit("No Higgsfield credentials. Set HF_KEY='key_id:key_secret' in the environment settings "
                     "(or HF_API_KEY_ID + HF_API_KEY_SECRET). Never paste keys into chat.")


def _request(method: str, url: str, body: dict | None = None, headers: dict | None = None,
             auth: bool = True, retries: int = 4, timeout: float = 60) -> dict:
    h = {"Accept": "application/json"}
    if auth:
        cred = credentials()
        if cred:
            h["Authorization"] = "Key " + cred
    if body is not None:
        h["Content-Type"] = "application/json"
    h.update(headers or {})
    data = json.dumps(body).encode() if body is not None else None
    delay = 1.5
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=data, method=method, headers=h),
                                        timeout=timeout) as r:
                raw = r.read()
                return json.loads(raw) if raw.strip() else {}
        except urllib.error.HTTPError as ex:
            try:
                detail = json.loads(ex.read() or b"{}").get("detail", "")
            except Exception:
                detail = ex.reason
            detail = detail if isinstance(detail, str) else json.dumps(detail)
            retryable = ex.code >= 500 or ex.code == 423 or (ex.code == 400 and "concurrent" in detail.lower())
            if retryable and attempt < retries:
                time.sleep(delay + random.random())
                delay *= 2
                continue
            raise HFError(ex.code, detail) from None
        except (urllib.error.URLError, TimeoutError) as ex:
            if attempt < retries:
                time.sleep(delay + random.random())
                delay *= 2
                continue
            raise HFError(0, f"network: {ex}") from None
    raise HFError(0, "unreachable")


# ───────────────────────── API wrappers ─────────────────────────

# ───────────────────────── schemas / safe defaults ─────────────────────────

SCHEMA_PATH = Path(__file__).resolve().parent / "hf_schemas.json"
_schemas_cache: dict | None = None

# Fields that are easy to confuse across endpoints: suggested first when a key is unknown.
FIELD_ALIASES = {
    "end_image_url": ["last_image_url", "last_frame_url"],
    "last_image_url": ["end_image_url", "last_frame_url"],
    "last_frame_url": ["last_image_url", "end_image_url"],
    "first_frame_url": ["image_url"],
    "image_url": ["first_frame_url", "image_urls"],
    "image_urls": ["image_url"],
    "start_image_url": ["image_url", "first_frame_url"],
    "sound": ["generate_audio"],
    "generate_audio": ["sound"],
    "audio": ["sound", "generate_audio"],
    "enhance_prompt": ["prompt_extend", "prompt_optimizer"],
    "prompt_extend": ["enhance_prompt", "prompt_optimizer"],
    "image_reference_url": ["image_urls", "image_url"],
    "negative": ["negative_prompt"],
}

# Injected only when the field exists on the endpoint AND the job does not set it.
# sound/generate_audio default ON upstream (+50 % cost); the prompt rewriters invented real
# trademarks (NOTEBOOK); aspect_ratio defaults to square/16:9 on most endpoints.
SAFE_DEFAULTS = (("sound", "off"), ("generate_audio", False), ("enhance_prompt", False),
                 ("prompt_extend", False), ("enable_thinking", False), ("prompt_optimizer", False),
                 ("aspect_ratio", "9:16"))


def load_schemas(path: Path | None = None) -> dict:
    """{endpoint id: JSON schema} from hf_schemas.json (keys starting with '_' are metadata)."""
    global _schemas_cache
    if path is None and _schemas_cache is not None:
        return _schemas_cache
    p = path or SCHEMA_PATH
    data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    out = {k: v for k, v in data.items() if not k.startswith("_")}
    if path is None:
        _schemas_cache = out
    return out


def schema_for(model: str) -> dict | None:
    return load_schemas().get(model.strip("/"))


_SCHEMA_KEEP = {"type", "enum", "const", "default", "minimum", "maximum", "minLength", "maxLength",
                "minItems", "maxItems", "format", "items", "properties", "required", "anyOf", "allOf",
                "if", "then", "pattern", "multipleOf"}


def _slim(o):
    if isinstance(o, dict):
        return {k: (_slim(v) if k != "properties" else {pk: _slim(pv) for pk, pv in v.items()})
                for k, v in o.items() if k in _SCHEMA_KEEP}
    if isinstance(o, list):
        return [_slim(x) for x in o]
    return o


def extract_schemas(text: str) -> dict:
    """Endpoint schemas from the public docs bundle (llms-full.txt): one per '**Endpoint ID:**' section."""
    out = {}
    for sec in re.split(r"\n(?=# )", text):
        m = re.search(r"\*\*Endpoint ID:\*\* `([^`]+)`", sec)
        j = re.search(r"Complete JSON schema\">\s*```json[^\n]*\n(.*?)```", sec, re.S)
        if m and j:
            out[m.group(1).strip("/")] = _slim(json.loads(j.group(1)))
    return out


def _type_ok(t: str, v) -> bool:
    if t == "string":
        return isinstance(v, str)
    if t == "integer":
        return isinstance(v, int) and not isinstance(v, bool)
    if t == "number":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    if t == "boolean":
        return isinstance(v, bool)
    if t == "array":
        return isinstance(v, list)
    if t == "object":
        return isinstance(v, dict)
    if t == "null":
        return v is None
    return True


def _check(name: str, sch: dict, v) -> list[str]:
    if "anyOf" in sch:
        if not any(not _check(name, alt, v) for alt in sch["anyOf"]):
            return [f"{name}: {v!r} matches none of the allowed forms"]
        return []
    t = sch.get("type")
    if t and not _type_ok(t, v):
        return [f"{name}: expected {t}, got {type(v).__name__} {v!r}"]
    errs = []
    if "const" in sch and v != sch["const"]:
        errs.append(f"{name}: must be {sch['const']!r}")
    if "enum" in sch and v not in sch["enum"]:
        errs.append(f"{name}: {v!r} not in {sch['enum']}")
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        if "minimum" in sch and v < sch["minimum"]:
            errs.append(f"{name}: {v} < minimum {sch['minimum']}")
        if "maximum" in sch and v > sch["maximum"]:
            errs.append(f"{name}: {v} > maximum {sch['maximum']}")
    if isinstance(v, str):
        if "minLength" in sch and len(v) < sch["minLength"]:
            errs.append(f"{name}: shorter than {sch['minLength']} chars")
        if "maxLength" in sch and len(v) > sch["maxLength"]:
            errs.append(f"{name}: {len(v)} chars > maxLength {sch['maxLength']}")
        if sch.get("format") == "uri" and not re.match(r"^(https?://|@file:)", v):
            errs.append(f"{name}: expected a public https URL or @file:path, got {v[:60]!r}")
    if isinstance(v, list):
        if "minItems" in sch and len(v) < sch["minItems"]:
            errs.append(f"{name}: {len(v)} items < minItems {sch['minItems']}")
        if "maxItems" in sch and len(v) > sch["maxItems"]:
            errs.append(f"{name}: {len(v)} items > maxItems {sch['maxItems']}")
        if isinstance(sch.get("items"), dict):
            for i, x in enumerate(v):
                errs += _check(f"{name}[{i}]", sch["items"], x)
    if isinstance(v, dict) and "properties" in sch:
        errs += _check_object(name, sch, v)
    return errs


def _suggest(key: str, props) -> str:
    cands = [a for a in FIELD_ALIASES.get(key, []) if a in props]
    cands += [c for c in difflib.get_close_matches(key, list(props), n=2, cutoff=0.6) if c not in cands]
    return f" (did you mean {' / '.join(cands)}?)" if cands else ""


def _check_object(name: str, sch: dict, obj: dict) -> list[str]:
    props = sch.get("properties", {})
    pre = f"{name}." if name else ""
    errs = [f"{pre}{k}: unknown field for this endpoint{_suggest(k, props)}" for k in obj if k not in props]
    errs += [f"{pre}{k}: required" for k in sch.get("required") or [] if k not in obj]
    for k, v in obj.items():
        if k in props:
            errs += _check(f"{pre}{k}", props[k], v)
    # if/then rules (e.g. Qwen: enable_thinking=true requires prompt_extend=true), on effective values
    eff = {**{k: p["default"] for k, p in props.items() if isinstance(p, dict) and "default" in p}, **obj}
    for rule in sch.get("allOf") or []:
        cond = rule.get("if") or {}
        hit = all(k in eff for k in cond.get("required", [])) and all(
            k in eff and ("const" not in c or eff[k] == c["const"])
            for k, c in (cond.get("properties") or {}).items())
        if hit and rule.get("then"):
            then = rule["then"]
            for k in then.get("required", []):
                if k not in eff:
                    errs.append(f"{pre}{k}: required when {json.dumps(cond.get('properties'))}")
            for k, c in (then.get("properties") or {}).items():
                if k in eff:
                    errs += [e + f" (because {json.dumps(cond.get('properties'))})"
                             for e in _check(f"{pre}{k}", c, eff[k])]
    return errs


def validate_args(model: str, args: dict) -> list[str]:
    """Problems that would waste money or 400 at submit; [] when the request is safe to price and run."""
    sch = schema_for(model)
    if sch is None:
        return [f"no known schema for {model}: refusing (rebuild with `hfgen.py schemas --import "
                f"llms-full.txt`, or pass --allow-unvalidated after checking the model page)"]
    return _check_object("", sch, args)


def apply_safe_defaults(model: str, args: dict) -> tuple[dict, dict]:
    """(args with safe defaults, {field: injected value}). Never overrides a field the job sets."""
    sch = schema_for(model)
    if sch is None:
        return dict(args), {}
    props = sch.get("properties", {})
    out, injected = dict(args), {}
    for k, v in SAFE_DEFAULTS:
        if k in props and k not in out:
            enum = props[k].get("enum") if isinstance(props[k], dict) else None
            if enum is not None and v not in enum:
                continue
            out[k] = injected[k] = v
    return out, injected


# ───────────────────────── pricing ─────────────────────────

IMAGE_TOKEN_FALLBACK_USD = {"1k": 0.12, "2k": 0.30, "4k": 0.80}
IMAGE_REF_FALLBACK_USD = 0.02      # token-priced image input, per reference image (conservative)
RES_PIXELS = {"480p": 480 * 864, "540p": 540 * 960, "720p": 720 * 1280, "1080p": 1080 * 1920,
              "4k": 3840 * 2160, "2160p": 3840 * 2160}
_RES = r"(?:\d{3,4}p|4[kK])"
_RES_LIST = rf"{_RES}(?:\s*(?:/|,|or|and)\s*{_RES})*"
_USD = r"(\d+(?:\.\d+)?)"


def _res_rates(text: str) -> dict:
    """{'480p': 0.05, ...} from '$X at 480p[, $Y at 720p]' or '480p $X' / '480p/720p $X' wordings."""
    rates: dict = {}
    for v, rl in re.findall(rf"\${_USD}(?: per second of generated video)? at ({_RES_LIST})", text):
        for r in re.findall(_RES, rl):
            rates.setdefault(r.lower(), float(v))
    for rl, v in re.findall(rf"({_RES_LIST})[^$]{{0,60}}?\${_USD}", text):
        for r in re.findall(_RES, rl):
            rates.setdefault(r.lower(), float(v))
    return rates


def multishot_seconds(args: dict) -> float | None:
    """Kling multi-shot bills the SUM of the multi_prompt durations (docs), not `duration`."""
    mp = args.get("multi_prompt")
    if args.get("multi_shots") and isinstance(mp, list) and mp:
        return float(sum(float(x.get("duration") or 0) for x in mp if isinstance(x, dict)))
    return None


def billed_seconds(args: dict, default: float = 5.0) -> float:
    return multishot_seconds(args) or float(args.get("duration", default))


def _has_video_input(args: dict) -> bool:
    return bool(args.get("video_url") or args.get("video_urls"))


def price_from_description(desc: str, args: dict, default_res: str | None = None) -> float | None:
    """Conservative USD for models whose /estimate returns text instead of a number, or None (= refuse).
    1. per second: '$X per second ... at 480p, $Y at 720p' or 'by resolution: 480p $0.05, 720p $0.10'
    2. token-metered video: 'Billable video tokens = ceil(seconds x W x H x 24 fps / 1024)',
       'Per 1,000 video tokens: 480p/720p/1080p $0.014' (Seedance 2.0, Cinema Studio)
    3. token-priced images: fixed conservative fallback by resolution + per reference image."""
    res = str(args.get("resolution") or default_res or "720p").lower()
    secs = billed_seconds(args)
    tok = re.search(r"(?i)(?:each|per) ([\d,]+) video tokens", desc)
    metered = re.search(r"(?i)token-metered|billable video tokens", desc)
    per_second = desc[:tok.start()] if tok else desc
    if metered and (not tok or metered.start() < tok.start()):
        per_second = ""                                       # the whole description is a token formula
    rates = _res_rates(per_second) if "$" in per_second and "image output" not in per_second.lower() else {}
    if rates:
        rate = rates.get(res) or max(rates.values())
        return round(rate * secs, 4)
    if tok:
        if _has_video_input(args) and re.search(r"(?i)input video seconds|with video input", desc):
            return None                                       # input seconds are billable but unknown here
        trates = _res_rates(desc[max(0, tok.start() - 120):])
        unit = int(tok.group(1).replace(",", ""))
        fps = float((re.search(r"([\d.]+)\s*fps", desc) or [None, 24])[1])
        if res not in trates or res not in RES_PIXELS or not unit:
            return None
        tokens = math.ceil(secs * RES_PIXELS[res] * fps / 1024)
        return round(tokens / unit * trates[res], 4)
    if "image output" in desc.lower():
        n = max(1, int(args.get("batch_size", 1)))
        refs = len(args.get("image_urls") or []) + (1 if args.get("image_url") else 0)
        base = IMAGE_TOKEN_FALLBACK_USD.get(str(args.get("resolution") or default_res or "2k").lower(), 0.80)
        return round(base * n + IMAGE_REF_FALLBACK_USD * refs, 4)
    return None


def estimate(model: str, args: dict) -> dict:
    """/estimate (free). Returns the API dict with a numeric-string `usd` when a price is known,
    `est_source` = api | description | multishot-summed; `usd` stays None when it can't be priced."""
    e = _request("POST", f"{API}/estimate/{model.strip('/')}", args)
    sch = schema_for(model) or {}
    default_res = ((sch.get("properties") or {}).get("resolution") or {}).get("default")
    if e.get("usd") is None and e.get("pricing_description"):
        usd = price_from_description(e["pricing_description"], args, default_res)
        if usd is not None:
            e = {**e, "usd": f"{usd}", "est_source": "description"}
    elif e.get("usd") is not None:
        e = {**e, "est_source": "api"}
        ms = multishot_seconds(args)
        req = float(args.get("duration", 5))
        if ms and ms > req:     # /estimate prices the top-level duration; billing uses the sum
            e["usd"] = f"{round(float(e['usd']) * ms / req, 4)}"
            e["est_source"] = "multishot-summed"
    return e


def price_of(model: str, args: dict) -> tuple[float | None, str]:
    """(usd or None, reason). Never turns an unpriceable request into $0."""
    try:
        e = estimate(model, args)
    except HFError as ex:
        return None, f"estimate failed: {ex}"
    try:
        usd = float(e.get("usd"))
    except (TypeError, ValueError):
        return None, "UNPRICED: " + (e.get("pricing_description") or "no usd in estimate")[:160]
    if not math.isfinite(usd) or usd < 0:
        return None, f"UNPRICED: bad usd {e.get('usd')!r}"
    return usd, e.get("est_source", "api")


def submit(model: str, args: dict, idem: str) -> dict:
    return _request("POST", f"{API}/{model.strip('/')}", args, {"Idempotency-Key": idem}, retries=4)


def status(request_id: str) -> dict:
    return _request("GET", f"{API}/requests/{request_id}/status")


def poll(sub: dict, timeout_s: float = 1800, first: float = 4.0, cap: float = 20.0) -> dict:
    url = sub.get("status_url") or f"{API}/requests/{sub['request_id']}/status"
    t0, wait = time.time(), first
    st = sub
    while st.get("status") not in TERMINAL:
        if time.time() - t0 > timeout_s:
            raise HFError(0, f"timeout waiting for {sub.get('request_id')}")
        time.sleep(wait)
        wait = min(cap, wait * 1.5)
        st = _request("GET", url)
    return st


def upload(path: Path) -> str:
    ctype = UPLOAD_TYPES.get(path.suffix.lower()) or mimetypes.guess_type(str(path))[0]
    if ctype not in UPLOAD_TYPES.values():
        raise SystemExit(f"unsupported upload type for {path}")
    u = _request("POST", f"{API}/files/generate-upload-url", {"content_type": ctype})
    req = urllib.request.Request(u["upload_url"], data=path.read_bytes(), method="PUT",
                                 headers=u.get("upload_headers") or {"Content-Type": ctype})
    with urllib.request.urlopen(req, timeout=300):
        pass
    return u["public_url"]


def outputs(st: dict) -> list[str]:
    urls = [i["url"] for i in st.get("images") or [] if i.get("url")]
    for k in ("video", "audio"):
        if isinstance(st.get(k), dict) and st[k].get("url"):
            urls.append(st[k]["url"])
    urls += [a["url"] for a in st.get("audios") or [] if a.get("url") and a["url"] not in urls]
    return urls


def download(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=600) as r, open(dest, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    return dest


def _ext(url: str, default: str) -> str:
    suf = Path(url.split("?")[0]).suffix.lower()
    return suf if suf in {".png", ".jpg", ".jpeg", ".webp", ".mp4", ".mov", ".wav", ".mp3", ".gif"} else default


def idem_key(job_id: str, take: int, model: str, args: dict, salt: str = "") -> str:
    blob = json.dumps({"j": job_id, "t": take, "m": model, "a": args, "s": salt}, sort_keys=True)
    return "adr-" + hashlib.sha256(blob.encode()).hexdigest()[:40]


# ───────────────────────── plan / batch ─────────────────────────

def load_plan(path: Path) -> list[dict]:
    plan = json.loads(path.read_text(encoding="utf-8"))
    d = plan.get("defaults", {})
    jobs = []
    seen = set()
    for j in plan["jobs"]:
        job = {"model": d.get("model"), "takes": d.get("takes", 1), **j}
        job["args"] = {**d.get("args", {}), **j.get("args", {})}
        if not job.get("id") or not job.get("model"):
            raise SystemExit(f"job needs id and model: {j}")
        if job["id"] in seen:
            raise SystemExit(f"duplicate job id {job['id']}")
        seen.add(job["id"])
        jobs.append(job)
    return jobs


def file_refs(obj) -> list[str]:
    if isinstance(obj, str):
        return [obj[6:]] if obj.startswith("@file:") else []
    if isinstance(obj, list):
        return [r for x in obj for r in file_refs(x)]
    if isinstance(obj, dict):
        return [r for x in obj.values() for r in file_refs(x)]
    return []


def resolve_refs(obj, urls: dict):
    if isinstance(obj, str) and obj.startswith("@file:"):
        return urls[obj[6:]]
    if isinstance(obj, list):
        return [resolve_refs(x, urls) for x in obj]
    if isinstance(obj, dict):
        return {k: resolve_refs(v, urls) for k, v in obj.items()}
    return obj


def run_take(job: dict, take: int, args: dict, out: Path, salt: str, est_usd: float | None) -> dict:
    key = idem_key(job["id"], take, job["model"], args, salt)
    rec = {"job": job["id"], "take": take, "model": job["model"], "idempotency_key": key,
           "est_usd": est_usd, "started": time.strftime("%Y-%m-%dT%H:%M:%S")}
    try:
        sub = submit(job["model"], args, key)
        rec["request_id"] = sub.get("request_id")
        log(f"  ▸ {job['id']} take {take}: {sub.get('status')} {rec['request_id']}")
        st = poll(sub)
        rec["status"] = st["status"]
        rec["error"] = st.get("error")
        files = []
        for i, u in enumerate(outputs(st)):
            ext = _ext(u, ".mp4" if "video" in st else ".png")
            name = f"{job['id']}_t{take:02d}" + (f"_{i}" if i else "") + ext
            files.append(str(download(u, out / name)))
        rec["files"] = files
        log(f"  ✓ {job['id']} take {take}: {st['status']} -> {', '.join(Path(f).name for f in files) or '-'}")
    except HFError as ex:
        rec["status"], rec["error"] = "error", str(ex)
        log(f"  ✗ {job['id']} take {take}: {ex}")
    rec["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    return rec


def prepare_jobs(jobs: list[dict], allow_unvalidated: bool = False) -> list[str]:
    """Inject safe defaults and schema-check every job in place. Returns the problems (refuse if any)."""
    problems = []
    for j in jobs:
        j["args"], j["defaults_applied"] = apply_safe_defaults(j["model"], j["args"])
        errs = validate_args(j["model"], j["args"])
        if allow_unvalidated and schema_for(j["model"]) is None:
            log(f"  ! {j['id']}: {j['model']} has no known schema; running UNVALIDATED (--allow-unvalidated)")
            errs = []
        j["schema_errors"] = errs
        problems += [f"{j['id']} ({j['model']}): {e}" for e in errs]
    return problems


def cmd_batch(plan_path: Path, budget: float, dry_run: bool, yes: bool, concurrency: int,
              out: Path | None, salt: str, only: list[str] | None, allow_unvalidated: bool = False) -> dict:
    jobs = load_plan(plan_path)
    if only:
        jobs = [j for j in jobs if j["id"] in only]
    base = plan_path.parent
    out = out or base / "clips"
    manifest_path = out / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"takes": {}}

    refs = sorted({r for j in jobs for r in file_refs(j["args"])})
    missing = [r for r in refs if not (base / r).exists()]
    if missing:
        raise SystemExit(f"missing reference files: {missing}")
    total_takes = sum(int(j["takes"]) for j in jobs)
    log(f"plan: {len(jobs)} jobs, {total_takes} takes, {len(refs)} local refs")

    # schema + safe defaults BEFORE any upload, estimate or submit
    problems = prepare_jobs(jobs, allow_unvalidated)
    for j in jobs:
        if j["defaults_applied"]:
            log(f"  · {j['id']}: safe defaults {json.dumps(j['defaults_applied'])}")
    for pr in problems:
        log(f"  ✗ schema: {pr}")
    if problems and not dry_run:
        raise SystemExit("refusing to spend: plan fails the schema check:\n  " + "\n  ".join(problems))
    out.mkdir(parents=True, exist_ok=True)

    upl = manifest.setdefault("uploads", {})
    if dry_run:
        urls = {r: upl.get(r, f"https://upload.pending/{r}") for r in refs}
    else:
        for r in refs:
            if r not in upl:
                log(f"  ↑ uploading {r}")
                upl[r] = upload(base / r)
        urls = upl

    # estimate every job once (cost is per request; takes multiply it). Unpriced = refused, never $0.
    est, total, unpriced, per_job = {}, 0.0, [], {}
    for j in jobs:
        todo = [t for t in range(1, int(j["takes"]) + 1)
                if manifest["takes"].get(f"{j['id']}#{t}", {}).get("status") != "completed"]
        if j["schema_errors"]:
            usd, src = None, "schema errors"
        else:
            usd, src = price_of(j["model"], resolve_refs(j["args"], urls))
        if usd is None and todo:
            unpriced.append(j["id"])
            if not dry_run:
                raise SystemExit(f"refusing to spend: cannot price {j['id']} ({j['model']}): {src}")
        est[j["id"]] = usd
        per_job[j["id"]] = {"model": j["model"], "takes": len(todo), "usd_each": usd, "source": src,
                            "defaults_applied": j["defaults_applied"]}
        if usd is not None:
            total += usd * len(todo)
        log(f"  $ {j['id']:<18} {j['model']:<48} {len(todo)} takes x "
            f"{'UNPRICED (' + src + ')' if usd is None else f'${usd:.3f}'}")
    log(f"estimated total for remaining takes: ${total:.2f}  (budget ${budget:.2f})"
        + (f"  + {len(unpriced)} UNPRICED job(s): {', '.join(unpriced)}" if unpriced else ""))
    if dry_run:
        max_take = max([v["usd_each"] for v in per_job.values() if v["usd_each"] is not None and v["takes"]],
                       default=0.0)
        return {"dry_run": True, "ok": not problems and not unpriced and total <= budget,
                "estimated_usd": round(total, 2), "jobs": len(jobs), "unpriced": unpriced,
                "problems": problems, "over_budget": total > budget, "max_take_usd": round(max_take, 4),
                "per_job": per_job}
    if total > budget:
        raise SystemExit(f"over budget: ${total:.2f} > ${budget:.2f}. Lower takes/duration or raise --budget.")
    if not yes:
        ans = input(f"Spend up to ${total:.2f}? [y/N] ").strip().lower()
        if ans != "y":
            raise SystemExit("cancelled")

    work = []
    for j in jobs:
        a = resolve_refs(j["args"], urls)
        for t in range(1, int(j["takes"]) + 1):
            k = f"{j['id']}#{t}"
            if manifest["takes"].get(k, {}).get("status") == "completed":
                continue
            work.append((j, t, a))
    log_path = out / "gen_log.jsonl"
    with cf.ThreadPoolExecutor(max_workers=max(1, concurrency)) as ex:
        futs = [ex.submit(run_take, j, t, a, out, salt, est[j["id"]]) for j, t, a in work]
        for fu in cf.as_completed(futs):
            rec = fu.result()
            manifest["takes"][f"{rec['job']}#{rec['take']}"] = rec
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec) + "\n")
            manifest_path.write_text(json.dumps(manifest, indent=2))
    done = [r for r in manifest["takes"].values() if r.get("status") == "completed"]
    spent = sum(r.get("est_usd") or 0 for r in done)
    summary = {"completed": len(done), "failed": sum(1 for r in manifest["takes"].values()
                                                     if r.get("status") not in ("completed", None)),
               "estimated_spend_usd": round(spent, 2), "out": str(out)}
    manifest["summary"] = summary
    manifest_path.write_text(json.dumps(manifest, indent=2))
    return summary


# ───────────────────────── CLI ─────────────────────────

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="hfgen.py", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    e = sub.add_parser("estimate"); e.add_argument("model"); e.add_argument("--args", required=True)
    r = sub.add_parser("run"); r.add_argument("model"); r.add_argument("--args", required=True)
    r.add_argument("--out", default="clips"); r.add_argument("--yes", action="store_true")
    r.add_argument("--max-usd", type=float, default=5.0)
    b = sub.add_parser("batch"); b.add_argument("plan"); b.add_argument("--budget", type=float, required=True)
    b.add_argument("--dry-run", action="store_true"); b.add_argument("--yes", action="store_true")
    b.add_argument("--concurrency", type=int, default=3); b.add_argument("--out", default=None)
    b.add_argument("--fresh", default="", help="salt to force new generations instead of resuming")
    b.add_argument("--only", default=None, help="comma-separated job ids")
    b.add_argument("--allow-unvalidated", action="store_true",
                   help="run models that have no known schema (checked by hand)")
    r.add_argument("--allow-unvalidated", action="store_true")
    li = sub.add_parser("lint"); li.add_argument("model"); li.add_argument("--args", required=True)
    sc = sub.add_parser("schemas"); sc.add_argument("model", nargs="?")
    sc.add_argument("--import", dest="import_path", default=None, help="llms-full.txt from the docs")
    s = sub.add_parser("status"); s.add_argument("request_id")
    u = sub.add_parser("upload"); u.add_argument("file")
    a = ap.parse_args(argv)

    def parse_args_json(x: str) -> dict:
        p = Path(x)
        return json.loads(p.read_text()) if p.exists() else json.loads(x)

    if a.cmd == "check":
        if credentials() is None:
            print("no key in env: relying on the agent proxy network secret (HF_AUTH_VIA_PROXY=1)")
        try:
            status("00000000-0000-0000-0000-000000000000")
        except HFError as ex:
            if ex.status == 401:
                print("credentials REJECTED (401)"); return 1
            print(f"credentials OK (probe returned {ex.status}, expected 404)"); return 0
        print("credentials OK"); return 0
    if a.cmd == "estimate":
        print(json.dumps(estimate(a.model, parse_args_json(a.args)))); return 0
    if a.cmd == "status":
        print(json.dumps(status(a.request_id), indent=2)); return 0
    if a.cmd == "upload":
        print(upload(Path(a.file))); return 0
    if a.cmd == "lint":
        args, injected = apply_safe_defaults(a.model, parse_args_json(a.args))
        errs = validate_args(a.model, args)
        print(json.dumps({"ok": not errs, "problems": errs, "defaults_applied": injected, "args": args}, indent=2))
        return 0 if not errs else 2
    if a.cmd == "schemas":
        if a.import_path:
            sch = extract_schemas(Path(a.import_path).read_text(encoding="utf-8"))
            old = json.loads(SCHEMA_PATH.read_text()) if SCHEMA_PATH.exists() else {}
            manual = {k: v for k, v in old.items() if isinstance(v, dict) and v.get("_manual")}
            meta = {"_source": "https://docs.higgsfield.ai/docs/llms-full.txt",
                    "_extracted": time.strftime("%Y-%m-%d"), "_count": len(sch)}
            SCHEMA_PATH.write_text(json.dumps({**meta, **sch, **manual}, indent=1, sort_keys=False) + "\n")
            print(f"wrote {len(sch)} schemas (+{len(manual)} manual) to {SCHEMA_PATH}"); return 0
        if a.model:
            sch = schema_for(a.model)
            if sch is None:
                print(f"no schema for {a.model}"); return 1
            print(json.dumps(sch, indent=1)); return 0
        for k, v in sorted(load_schemas().items()):
            print(f"{k:<52} {', '.join(sorted(v.get('properties', {})))}")
        return 0
    if a.cmd == "run":
        args, injected = apply_safe_defaults(a.model, parse_args_json(a.args))
        errs = [] if (a.allow_unvalidated and schema_for(a.model) is None) else validate_args(a.model, args)
        if errs:
            raise SystemExit("refusing to spend: " + "; ".join(errs))
        if injected:
            print(f"safe defaults: {json.dumps(injected)}", file=sys.stderr)
        usd, src = price_of(a.model, args)
        if usd is None:
            raise SystemExit(f"refusing to spend: {src}")
        print(f"estimate: ${usd:.3f} ({src})", file=sys.stderr)
        if not usd <= a.max_usd:
            raise SystemExit(f"estimate ${usd} exceeds --max-usd {a.max_usd}")
        if not a.yes and input("Run? [y/N] ").strip().lower() != "y":
            raise SystemExit("cancelled")
        rec = run_take({"id": "run", "model": a.model}, int(time.time()), args, Path(a.out), "", usd)
        print(json.dumps(rec, indent=2)); return 0 if rec["status"] == "completed" else 1
    if a.cmd == "batch":
        res = cmd_batch(Path(a.plan), a.budget, a.dry_run, a.yes, a.concurrency,
                        Path(a.out) if a.out else None, a.fresh, a.only.split(",") if a.only else None,
                        a.allow_unvalidated)
        print(json.dumps(res, indent=2))
        return 2 if res.get("dry_run") and not res.get("ok") else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
