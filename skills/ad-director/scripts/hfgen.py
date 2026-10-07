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
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
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

IMAGE_TOKEN_FALLBACK_USD = {"1k": 0.12, "2k": 0.30, "4k": 0.80}


def price_from_description(desc: str, args: dict) -> float | None:
    """Conservative USD for models whose /estimate returns text instead of a number.
    Video: '$X per second ... at 480p, $Y at 720p' x duration (list price, before discount).
    Token-priced images: fixed conservative fallback by resolution."""
    per_second = re.split(r"(?i)each [\d,]+ (?:video )?tokens", desc)[0]  # ignore the per-token rates
    rates = {}
    for v, res in re.findall(r"\$([\d.]+)(?: per second of generated video)? at (\d{3,4}p)", per_second):
        rates.setdefault(res, float(v))
    if rates:
        res = str(args.get("resolution", "720p"))
        rate = rates.get(res) or max(rates.values())
        return round(rate * float(args.get("duration", 5)), 4)
    if "image output" in desc.lower():
        return IMAGE_TOKEN_FALLBACK_USD.get(str(args.get("resolution", "2k")).lower(), 0.80) * max(1, int(args.get("batch_size", 1)))
    return None


def estimate(model: str, args: dict) -> dict:
    e = _request("POST", f"{API}/estimate/{model.strip('/')}", args)
    if e.get("usd") is None and e.get("pricing_description"):
        usd = price_from_description(e["pricing_description"], args)
        if usd is not None:
            e = {**e, "usd": f"{usd}", "est_source": "description"}
    return e


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


def cmd_batch(plan_path: Path, budget: float, dry_run: bool, yes: bool, concurrency: int,
              out: Path | None, salt: str, only: list[str] | None) -> dict:
    jobs = load_plan(plan_path)
    if only:
        jobs = [j for j in jobs if j["id"] in only]
    base = plan_path.parent
    out = out or base / "clips"
    out.mkdir(parents=True, exist_ok=True)
    manifest_path = out / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"takes": {}}

    refs = sorted({r for j in jobs for r in file_refs(j["args"])})
    missing = [r for r in refs if not (base / r).exists()]
    if missing:
        raise SystemExit(f"missing reference files: {missing}")
    total_takes = sum(int(j["takes"]) for j in jobs)
    log(f"plan: {len(jobs)} jobs, {total_takes} takes, {len(refs)} local refs")

    upl = manifest.setdefault("uploads", {})
    if dry_run:
        urls = {r: upl.get(r, f"https://upload.pending/{r}") for r in refs}
    else:
        for r in refs:
            if r not in upl:
                log(f"  ↑ uploading {r}")
                upl[r] = upload(base / r)
        urls = upl

    # estimate every job once (cost is per request; takes multiply it)
    est, total = {}, 0.0
    for j in jobs:
        a = resolve_refs(j["args"], urls)
        try:
            e = estimate(j["model"], a)
            usd = float(e.get("usd"))
        except (HFError, TypeError, ValueError) as ex:
            if dry_run:
                usd = None
                log(f"  ? {j['id']}: estimate unavailable ({ex})")
            else:
                raise SystemExit(f"cannot estimate {j['id']} ({j['model']}): {ex}")
        est[j["id"]] = usd
        todo = [t for t in range(1, int(j["takes"]) + 1)
                if manifest["takes"].get(f"{j['id']}#{t}", {}).get("status") != "completed"]
        if usd is not None:
            total += usd * len(todo)
        log(f"  $ {j['id']:<18} {j['model']:<48} {len(todo)} takes x "
            f"{'?' if usd is None else f'${usd:.3f}'}")
    log(f"estimated total for remaining takes: ${total:.2f}  (budget ${budget:.2f})")
    if total > budget:
        raise SystemExit(f"over budget: ${total:.2f} > ${budget:.2f}. Lower takes/duration or raise --budget.")
    if dry_run:
        return {"dry_run": True, "estimated_usd": round(total, 2), "jobs": len(jobs)}
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
    if a.cmd == "run":
        args = parse_args_json(a.args)
        usd = float(estimate(a.model, args).get("usd", "nan"))
        print(f"estimate: ${usd:.3f}", file=sys.stderr)
        if not usd <= a.max_usd:
            raise SystemExit(f"estimate ${usd} exceeds --max-usd {a.max_usd}")
        if not a.yes and input("Run? [y/N] ").strip().lower() != "y":
            raise SystemExit("cancelled")
        rec = run_take({"id": "run", "model": a.model}, int(time.time()), args, Path(a.out), "", usd)
        print(json.dumps(rec, indent=2)); return 0 if rec["status"] == "completed" else 1
    if a.cmd == "batch":
        res = cmd_batch(Path(a.plan), a.budget, a.dry_run, a.yes, a.concurrency,
                        Path(a.out) if a.out else None, a.fresh, a.only.split(",") if a.only else None)
        print(json.dumps(res, indent=2)); return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
