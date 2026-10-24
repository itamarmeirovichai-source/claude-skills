#!/usr/bin/env python3
"""pipeline: ad-production state machine for ad-director (stdlib only).

One job = one folder: jobs/<job_id>/job.json (stage, approvals, budget, history) plus an
append-only spend.jsonl ledger (estimated vs billed USD for every paid call). Any session can
resume from disk. Money only moves through hfgen.py and elevenlabs.py; every paid stage dry-runs
(estimates) first and is checked against the job cap, the stage cap and the approval threshold.

Commands
  new --product NAME [--client C] [--label-text TXT ...] [--colour primary=#C9A65A ...]
      [--packshot FILE] [--url URL] [--cap 10] [--stage-cap S6=5 ...] [--id ID] [--root jobs]
                                 product intake -> jobs/<id>/ (job.json, 00-intake/*.json, brief files)
  status JOB [--json]            stage table, budget, what to do next
  advance JOB [--approve] [--dry-run]
                                 run the current stage (and the following ones) until something needs
                                 an agent artefact, a human checkpoint or a spend approval.
                                 --approve: allow ONE paid step whose estimate (or any single call)
                                 is over $2 (job.json budget.approve_over_usd). Caps are never bypassed.
                                 --dry-run: estimate the next paid step only; spend nothing.
  approve JOB H1|H2|H3 CHOICE [--notes TXT] [--by NAME]
                                 H1 CHOICE = storyline id (or "reject"); H2/H3 CHOICE = approve|reject
  spend JOB [--bill ID USD] [--json]
                                 ledger with estimated vs billed totals; --bill records the billed
                                 amount for a ledger entry (appended; >10 % over estimate puts the job on hold)
  budget JOB [--cap USD] [--stage-cap S6=5 ...] [--approve-over USD] [--release-hold]

Stages (references/marketing/18-automation-pipeline.md §4.3)
  S0 intake  S1 ideas  S2 zero-cost test  S3 storylines  [H1 storyline pick]  S4 shot plan
  S5 stills  [H2 stills approval]  S6 motion  S7 audio  S8 edit  S9 QC  [H3 final]  S10 deliver  S11 learn

Agent artefacts the stages wait for (Claude/subagents write them; the pipeline validates):
  10-ideas/ideas.json            [{"title", ...}] >= 7 (seeds.json is rolled for you)
  20-tests/drivers.json          [{"title", "drivers": {...}, "mechanism"?}] >= 3 -> director rank
  30-storylines/storylines.json  3 x {"id", "title", "big_idea_shot", "cta", "seed"?}
  30-storylines/plan_plates.vN.json  optional Soul mood plates (hfgen plan, S3 cap)
  40-shotplan/shots.json + plan_stills.vN.json (hfgen plan)
  60-motion/plan_motion.vN.json  (hfgen plan, after H2)
  70-audio/audio_plan.json       {"vo":[{"id","text","voice","model"?}], "sfx":[{"id","prompt","seconds"}],
                                  "music":[{"id","prompt","seconds"} | {"id","plan":{...}}]}
  80-edit/master*.mp4            (reel-studio render)
  99-deliver/delivery.json
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import os
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import director as D  # noqa: E402
import elevenlabs as E  # noqa: E402
import hfgen as H  # noqa: E402

STAGES = {
    "S0": ("intake", "00-intake"), "S1": ("ideas", "10-ideas"), "S2": ("zero-cost test", "20-tests"),
    "S3": ("storylines", "30-storylines"), "S4": ("shot plan", "40-shotplan"), "S5": ("stills", "50-stills"),
    "S6": ("motion", "60-motion"), "S7": ("audio", "70-audio"), "S8": ("edit", "80-edit"),
    "S9": ("qc", "90-qc"), "S10": ("deliver", "99-deliver"), "S11": ("learn", "99-deliver"),
}
CHECKPOINTS = {  # human gates: where they sit, what a rejection sends the job back to
    "H1": {"name": "storyline pick", "after": "S3", "reject_to": "S3", "dir": "30-storylines"},
    "H2": {"name": "stills approval", "after": "S5", "reject_to": "S4", "dir": "50-stills"},
    "H3": {"name": "final approval", "after": "S9", "reject_to": "S8", "dir": "90-qc"},
}
ORDER = ["S0", "S1", "S2", "S3", "H1", "S4", "S5", "H2", "S6", "S7", "S8", "S9", "H3", "S10", "S11"]
PAID_STAGES = {"S3", "S5", "S6", "S7"}
DEFAULT_CAP = 10.0
DEFAULT_STAGE_CAPS = {"S3": 0.10, "S5": 2.50, "S6": 5.00, "S7": 1.00}   # the rest of $10 is retake reserve
APPROVE_OVER_USD = 2.0
RECONCILE_TOLERANCE = 0.10
MIN_IDEAS, MIN_RANKED, N_STORYLINES = 7, 3, 3
DONE, PENDING = "done", "pending"
WAIT_AGENT, WAIT_HUMAN, WAIT_APPROVAL, BLOCKED = "awaiting_agent", "awaiting_human", "awaiting_approval", "blocked"


def now() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "x"


def _read_json(p: Path, default=None):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def _write_json(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, p)


# ───────────────────────── job state ─────────────────────────

class Job:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.data = _read_json(self.path / "job.json")
        if self.data is None:
            raise SystemExit(f"no job.json in {self.path}")

    @property
    def ledger(self) -> Path:
        return self.path / "spend.jsonl"

    def d(self, key: str) -> Path:
        return self.path / (STAGES[key][1] if key in STAGES else CHECKPOINTS[key]["dir"])

    def save(self) -> None:
        t = totals(read_spend(self))
        self.data["budget"]["spent_usd"] = t["effective_usd"]
        self.data["budget"]["estimated_usd"] = t["estimated_usd"]
        self.data["budget"]["billed_usd"] = t["billed_usd"]
        st = self.data["stages"].get(self.data["stage"], {})
        self.data["status"] = DONE if self.data["stage"] == DONE else st.get("status", PENDING)
        _write_json(self.path / "job.json", self.data)

    def event(self, stage: str, event: str, **kw) -> None:
        self.data["history"].append({"at": now(), "stage": stage, "event": event, **kw})

    def set(self, stage: str, status: str, note: str = "", **kw) -> None:
        self.data["stages"][stage] = {"status": status, "note": note, "at": now(), **kw}

    def status(self, stage: str) -> str:
        return self.data["stages"].get(stage, {}).get("status", PENDING)


def resolve_job(job: str, root: str = "jobs") -> Path:
    p = Path(job)
    if (p / "job.json").exists():
        return p
    q = Path(root) / job
    if (q / "job.json").exists():
        return q
    raise SystemExit(f"job not found: {job} (looked in {p} and {q})")


# ───────────────────────── spend ledger ─────────────────────────

def read_spend(job: Job) -> list[dict]:
    if not job.ledger.exists():
        return []
    return [json.loads(x) for x in job.ledger.read_text(encoding="utf-8").splitlines() if x.strip()]


def append_spend(job: Job, rec: dict) -> dict:
    n = sum(1 for r in read_spend(job) if r.get("type") == "spend")
    rec = {"type": "spend", "id": f"sp-{n + 1:04d}", "at": now(), "billed_usd": None, **rec}
    with open(job.ledger, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def totals(records: list[dict]) -> dict:
    """estimated / billed / effective (billed when known, else estimated), overall and per stage."""
    bills = {}
    for r in records:
        if r.get("type") == "bill":
            bills[r["ref"]] = float(r["billed_usd"])
    est = billed = eff = 0.0
    by_stage: dict = {}
    for r in records:
        if r.get("type") != "spend":
            continue
        e = float(r.get("est_usd") or 0)
        b = bills.get(r["id"], r.get("billed_usd"))
        x = float(b) if b is not None else e
        est += e
        billed += float(b or 0)
        eff += x
        s = by_stage.setdefault(r["stage"], {"estimated_usd": 0.0, "effective_usd": 0.0})
        s["estimated_usd"] = round(s["estimated_usd"] + e, 4)
        s["effective_usd"] = round(s["effective_usd"] + x, 4)
    return {"estimated_usd": round(est, 4), "billed_usd": round(billed, 4), "effective_usd": round(eff, 4),
            "by_stage": by_stage, "unbilled": [r["id"] for r in records if r.get("type") == "spend"
                                               and r["id"] not in bills and r.get("billed_usd") is None
                                               and float(r.get("est_usd") or 0) > 0]}


def headroom(job: Job, stage: str) -> tuple[float, float]:
    """(left in the stage cap, left in the job cap)."""
    t = totals(read_spend(job))
    b = job.data["budget"]
    job_left = b["cap_usd"] - t["effective_usd"]
    cap = b["stage_caps"].get(stage)
    stage_left = (cap - t["by_stage"].get(stage, {}).get("effective_usd", 0.0)) if cap is not None else 0.0
    return round(stage_left, 4), round(job_left, 4)


def spend_gate(job: Job, stage: str, est_total: float, max_single: float, approve: bool) -> tuple[str, str] | None:
    """None when the spend may go ahead, else (status, reason)."""
    stage_left, job_left = headroom(job, stage)
    if stage not in job.data["budget"]["stage_caps"]:
        return BLOCKED, f"{stage} has no stage cap; set one with `budget --stage-cap {stage}=USD`"
    if est_total > stage_left + 1e-9:
        return BLOCKED, (f"estimate ${est_total:.2f} > {stage} cap headroom ${stage_left:.2f}: cut takes/duration, "
                         f"or a human raises it with `budget --stage-cap {stage}=USD`")
    if est_total > job_left + 1e-9:
        return BLOCKED, f"estimate ${est_total:.2f} > job cap headroom ${job_left:.2f} (`budget --cap USD`)"
    thr = job.data["budget"].get("approve_over_usd", APPROVE_OVER_USD)
    if (est_total > thr or max_single > thr) and not approve:
        return WAIT_APPROVAL, (f"estimate ${est_total:.2f} (largest single call ${max_single:.2f}) is over "
                               f"${thr:.2f}: a human re-runs `advance --approve` to spend it")
    return None


# ───────────────────────── paid steps ─────────────────────────

def latest_version(d: Path, stem: str) -> Path | None:
    best = None
    for p in d.glob(f"{stem}.v*.json"):
        m = re.fullmatch(rf"{re.escape(stem)}\.v(\d+)\.json", p.name)
        if m and (best is None or int(m.group(1)) > best[0]):
            best = (int(m.group(1)), p)
    return best[1] if best else None


def hfgen_preflight(plan: Path, out: Path) -> dict:
    return H.cmd_batch(plan, budget=math.inf, dry_run=True, yes=False, concurrency=3, out=out, salt="", only=None)


def run_hfgen_stage(job: Job, stage: str, plan: Path, out: Path, approve: bool, dry_run: bool) -> tuple[str, str]:
    pre = hfgen_preflight(plan, out)                          # always estimate first (free)
    job.event(stage, "preflight", plan=plan.name, estimated_usd=pre["estimated_usd"],
              ok=pre["ok"], unpriced=pre["unpriced"], problems=pre["problems"][:10])
    if not pre["ok"]:
        why = "; ".join(pre["problems"][:5] + [f"UNPRICED {u}" for u in pre["unpriced"]])
        return BLOCKED, f"{plan.name} fails the dry run: {why}"
    est = float(pre["estimated_usd"])
    if est > 0:
        gate = spend_gate(job, stage, est, float(pre["max_take_usd"]), approve)
        if gate:
            return gate
    if dry_run:
        return PENDING, f"dry run OK: {plan.name} would spend ${est:.2f}; run `advance` to spend it"
    stage_left, job_left = headroom(job, stage)
    try:
        res = H.cmd_batch(plan, budget=max(0.0, min(stage_left, job_left)), dry_run=False, yes=True,
                          concurrency=3, out=out, salt="", only=None)
    except SystemExit as ex:
        record_hfgen_spend(job, stage, out, approved=approve)
        return BLOCKED, f"hfgen refused or stopped: {ex}"
    record_hfgen_spend(job, stage, out, approved=approve)
    job.event(stage, "spent", plan=plan.name, **{k: res.get(k) for k in ("completed", "failed")})
    if res.get("failed"):
        return BLOCKED, (f"{res['failed']} take(s) failed (not charged). Re-run `advance` to retry the same "
                         f"requests, or write the next plan version with retakes")
    return DONE, f"{res['completed']} take(s) in {out.relative_to(job.path)}"


def record_hfgen_spend(job: Job, stage: str, out: Path, approved: bool) -> None:
    """One ledger line per finished take (idempotent: keyed by the hfgen idempotency key)."""
    man = _read_json(out / "manifest.json", {"takes": {}})
    seen = {r.get("idempotency_key") for r in read_spend(job) if r.get("type") == "spend"}
    for k, rec in sorted(man.get("takes", {}).items()):
        if rec.get("idempotency_key") in seen or rec.get("status") is None:
            continue
        if rec.get("status") == "error" and not rec.get("request_id"):
            continue                                              # never reached the API: nothing to bill
        # failed / nsfw requests are not billed; an "error" with a request id (e.g. a poll timeout) may
        # still complete upstream, so it is counted at the estimate until reconciled with `spend --bill`
        charged = rec.get("status") in ("completed", "error")
        append_spend(job, {"stage": stage, "tool": "hfgen", "item": k, "model": rec.get("model"),
                           "idempotency_key": rec.get("idempotency_key"), "request_id": rec.get("request_id"),
                           "est_usd": float(rec.get("est_usd") or 0) if charged else 0.0,
                           "status": rec.get("status"), "approved": approved,
                           "files": [str(Path(f).relative_to(job.path)) if Path(f).is_relative_to(job.path)
                                     else f for f in rec.get("files") or []]})


AUDIO_KINDS = ("vo", "sfx", "music")


def _audio_request(item: dict, kind: str) -> tuple[str, dict, str]:
    """(elevenlabs kind, body, cache endpoint) — the same body/key elevenlabs.py will use."""
    if kind == "vo":
        model = item.get("model", E.DEFAULT_TTS_MODEL)
        return "tts", E.tts_body(item["text"], model, item.get("stability", 0.5), 0.75,
                                 item.get("style"), item.get("speed")), f"tts/{item['voice']}"
    if kind == "sfx":
        return "sfx", E.sfx_body(item["prompt"], item.get("seconds"), item.get("loop", False),
                                 item.get("influence", 0.3)), "/v1/sound-generation"
    return "music", E.music_body(item.get("prompt"), item.get("seconds"), not item.get("with_vocals", False),
                                 item.get("model", "music_v2_5"), item.get("plan")), "/v1/music"


def run_audio_stage(job: Job, approve: bool, dry_run: bool) -> tuple[str, str]:
    d = job.d("S7")
    plan = _read_json(d / "audio_plan.json")
    if plan is None:
        return WAIT_AGENT, "write 70-audio/audio_plan.json (vo / sfx / music items with ids)"
    cache = d / "cache"
    items, problems = [], []
    for kind in AUDIO_KINDS:
        for it in plan.get(kind) or []:
            try:
                ek, body, ep = _audio_request(it, kind)
                pv = E.preview(ek, body, ep, cache)
            except (KeyError, TypeError, SystemExit) as ex:
                problems.append(f"{kind} {it.get('id', '?')}: {ex}")
                continue
            if not it.get("id"):
                problems.append(f"{kind} item without id")
                continue
            items.append((kind, it, pv))
    if problems:
        return BLOCKED, "audio_plan.json: " + "; ".join(problems)
    est = round(sum(pv["usd"] for _, _, pv in items if not pv["cached"]), 4)
    max_single = max([pv["usd"] for _, _, pv in items if not pv["cached"]], default=0.0)
    job.event("S7", "preflight", estimated_usd=est, calls=len(items),
              cached=sum(1 for _, _, pv in items if pv["cached"]))
    if est > 0:
        gate = spend_gate(job, "S7", est, max_single, approve)
        if gate:
            return gate
    if dry_run:
        return PENDING, f"dry run OK: audio would spend ~${est:.3f} ({len(items)} calls); run `advance`"
    manifest = _read_json(d / "audio_manifest.json", {})
    for kind, it, pv in items:
        out = d / f"{it['id']}.mp3"
        cap = it.get("max_credits", E.DEFAULT_MAX_CREDITS)
        try:
            if kind == "vo":
                r = E.tts(it["text"], it["voice"], out, it.get("model", E.DEFAULT_TTS_MODEL), it.get("stability", 0.5),
                          0.75, it.get("style"), it.get("speed"), cap, cache)
            elif kind == "sfx":
                r = E.sfx(it["prompt"], it.get("seconds"), out, it.get("loop", False), it.get("influence", 0.3),
                          cap, cache)
            else:
                r = E.music(it.get("prompt"), it.get("seconds"), out, not it.get("with_vocals", False),
                            it.get("model", "music_v2_5"), it.get("plan"), cap, cache)
        except (SystemExit, E.ElevenError) as ex:
            return BLOCKED, f"{kind} {it['id']}: {ex}"
        billed = (r["credits_billed"] * E.usd_per_credit()) if r.get("credits_billed") is not None else None
        logged = {x.get("cache_key") for x in read_spend(job) if x.get("type") == "spend"}
        if not (r["cached"] and r["cache_key"] in logged):        # a re-run of cached audio is not news
            append_spend(job, {"stage": "S7", "tool": "elevenlabs", "item": f"{kind}:{it['id']}",
                               "cache_key": r["cache_key"], "cached": r["cached"],
                               "est_usd": 0.0 if r["cached"] else float(r.get("est_usd") or 0),
                               "est_credits": r.get("est_credits"), "credits_billed": r.get("credits_billed"),
                               "billed_usd": 0.0 if r["cached"] else (round(billed, 6) if billed is not None else None),
                               "status": "completed", "approved": approve,
                               "files": [str(out.relative_to(job.path))]})
        manifest[it["id"]] = {k: v for k, v in r.items() if k != "audio"} | {"file": out.name, "kind": kind}
    _write_json(d / "audio_manifest.json", manifest)
    return DONE, f"{len(items)} audio file(s) in 70-audio/ (cache: 70-audio/cache)"


# ───────────────────────── stage handlers ─────────────────────────
# Each returns (status, note). DONE moves the job on; anything else stops `advance`.

def s0_intake(job: Job, **_) -> tuple[str, str]:
    prod = _read_json(job.d("S0") / "product.json", {})
    kit = _read_json(job.d("S0") / "brand_kit.json")
    if not prod.get("name"):
        return BLOCKED, "00-intake/product.json needs a name"
    if not [t for t in prod.get("label_text") or [] if str(t).strip()]:
        return WAIT_AGENT, ("transcribe the label EXACTLY into 00-intake/product.json label_text "
                            "(vision read of the packshot); it is the QC oracle for OCR")
    if kit is None:
        return BLOCKED, "00-intake/brand_kit.json missing"
    return DONE, f"label {prod['label_text']}"


def s1_ideas(job: Job, **_) -> tuple[str, str]:
    d = job.d("S1")
    if not (d / "seeds.json").exists():
        ledger = Path(job.data["ledger"])
        seeds = D.roll(D.load_matrix(), 5, job.data["client"], D.read_ledger(ledger),
                       seed=sum(job.data["job_id"].encode()))
        _write_json(d / "seeds.json", seeds)
        job.event("S1", "dice", n=len(seeds))
    ideas = _read_json(d / "ideas.json")
    if not isinstance(ideas, list) or len([i for i in ideas if isinstance(i, dict) and i.get("title")]) < MIN_IDEAS:
        return WAIT_AGENT, (f"write >= {MIN_IDEAS} ideas to 10-ideas/ideas.json (one idea subagent per seed in "
                            f"seeds.json + 2 free); each needs a title; apply the kill test and cliche ban")
    return DONE, f"{len(ideas)} ideas"


def s2_test(job: Job, **_) -> tuple[str, str]:
    d = job.d("S2")
    drivers = _read_json(d / "drivers.json")
    if not isinstance(drivers, list) or len(drivers) < MIN_RANKED:
        return WAIT_AGENT, (f"a sceptical media-buyer subagent scores >= {MIN_RANKED} ideas into 20-tests/drivers.json "
                            f"[{{title, drivers:{{hook:0-5,...}}, mechanism}}]")
    try:
        ranking = D.rank(drivers, job.data.get("goal", "balanced"))
    except (KeyError, ValueError) as ex:
        return BLOCKED, f"20-tests/drivers.json: {ex}"
    top = ranking[:MIN_RANKED]
    mech = {c.get("title"): c.get("mechanism") for c in drivers}
    mechs = {mech.get(r["title"]) for r in top if mech.get(r["title"])}
    _write_json(d / "tests.json", {"goal": job.data.get("goal", "balanced"), "ranking": ranking,
                                   "note": "relative ordering only; never a forecast"})
    if len(mechs) == 1 and all(mech.get(r["title"]) for r in top):
        return BLOCKED, "top 3 share one mechanism: re-score or swap in an idea from another mechanism"
    return DONE, "top 3: " + ", ".join(f"{r['title']} ({r['total']})" for r in top)


def s3_storylines(job: Job, approve: bool = False, dry_run: bool = False, **_) -> tuple[str, str]:
    d = job.d("S3")
    plates = latest_version(d, "plan_plates")
    if plates and not job.data["stages"].get("S3", {}).get("plates_done") == plates.name:
        st, note = run_hfgen_stage(job, "S3", plates, d / "plates", approve, dry_run)
        if st != DONE:
            return st, f"mood plates: {note}"
        job.data["stages"].setdefault("S3", {})["plates_done"] = plates.name
    sl = _read_json(d / "storylines.json")
    if not isinstance(sl, list) or len(sl) != N_STORYLINES:
        return WAIT_AGENT, (f"write {N_STORYLINES} storylines to 30-storylines/storylines.json "
                            f"[{{id, title, big_idea_shot, cta, seed?}}] (+ the private client page)")
    bad = [s.get("id", "?") for s in sl if not all(s.get(k) for k in ("id", "title", "big_idea_shot", "cta"))]
    if bad or len({s["id"] for s in sl if s.get("id")}) != N_STORYLINES:
        return BLOCKED, f"storylines need unique id + title + big_idea_shot + cta (check {bad or 'ids'})"
    return DONE, "storylines " + ", ".join(s["id"] for s in sl)


def s4_shotplan(job: Job, **_) -> tuple[str, str]:
    d = job.d("S4")
    shots = _read_json(d / "shots.json")
    plan = latest_version(d, "plan_stills")
    if not isinstance(shots, list) or not shots or plan is None:
        return WAIT_AGENT, ("write 40-shotplan/shots.json (one row per shot: id, model, backup, takes, "
                            "product_lock) and plan_stills.v1.json (hfgen plan)")
    pre = hfgen_preflight(plan, job.d("S5") / "clips")
    job.event("S4", "preflight", plan=plan.name, estimated_usd=pre["estimated_usd"], ok=pre["ok"])
    if not pre["ok"]:
        return BLOCKED, f"{plan.name}: " + "; ".join(pre["problems"][:5] + [f"UNPRICED {u}" for u in pre["unpriced"]])
    stage_left, job_left = headroom(job, "S5")
    if pre["estimated_usd"] > min(stage_left, job_left) + 1e-9:
        return BLOCKED, (f"{plan.name} estimates ${pre['estimated_usd']:.2f} > S5 headroom "
                         f"${min(stage_left, job_left):.2f}: fewer takes or lower resolution")
    return DONE, f"{len(shots)} shots; stills estimate ${pre['estimated_usd']:.2f} ({plan.name})"


def s5_stills(job: Job, approve: bool = False, dry_run: bool = False, **_) -> tuple[str, str]:
    plan = latest_version(job.d("S4"), "plan_stills")
    if plan is None:
        return WAIT_AGENT, "40-shotplan/plan_stills.vN.json missing"
    return run_hfgen_stage(job, "S5", plan, job.d("S5") / "clips", approve, dry_run)


def s6_motion(job: Job, approve: bool = False, dry_run: bool = False, **_) -> tuple[str, str]:
    plan = latest_version(job.d("S6"), "plan_motion")
    if plan is None:
        return WAIT_AGENT, ("write 60-motion/plan_motion.v1.json (i2v from the H2-approved stills, "
                            "one move per shot, sound off)")
    return run_hfgen_stage(job, "S6", plan, job.d("S6") / "clips", approve, dry_run)


def s7_audio(job: Job, approve: bool = False, dry_run: bool = False, **_) -> tuple[str, str]:
    return run_audio_stage(job, approve, dry_run)


def _master(job: Job) -> Path | None:
    ms = sorted(job.d("S8").glob("master*.mp4"))
    return ms[-1] if ms else None


def s8_edit(job: Job, **_) -> tuple[str, str]:
    m = _master(job)
    if m is None:
        return WAIT_AGENT, "render the edit with reel-studio into 80-edit/master_v1.mp4 (spec 80-edit/edit.v1.json)"
    return DONE, f"master {m.name}"


def s9_qc(job: Job, **_) -> tuple[str, str]:
    m = _master(job)
    if m is None:
        return BLOCKED, "no master in 80-edit"
    if not shutil.which("ffmpeg"):
        return BLOCKED, "ffmpeg not found (needed for director.py qc)"
    pack = _read_json(job.d("S0") / "brand_kit.json", {}).get("packshot")
    pack = str(job.d("S0") / pack) if pack and (job.d("S0") / pack).exists() else None
    rep = D.cmd_qc(str(m), pack, None, "reels", job.d("S9"))
    if rep["verdict"] == "FAIL":
        return BLOCKED, "director qc FAIL: " + "; ".join(f["msg"] for f in rep["findings"] if f["level"] == "FAIL")
    return DONE, f"qc {rep['verdict']} (90-qc/qc_report.md); next: QC subagent + rubric >= 80, then H3"


def s10_deliver(job: Job, **_) -> tuple[str, str]:
    if not (job.d("S10") / "delivery.json").exists():
        return WAIT_AGENT, "package masters/cutdowns + AI-disclosure + licences into 99-deliver/delivery.json"
    return DONE, "delivered"


def s11_learn(job: Job, **_) -> tuple[str, str]:
    return DONE, "log live results with `director.py log --result` when they arrive"


def checkpoint(job: Job, key: str, **_) -> tuple[str, str]:
    ap = [a for a in job.data["approvals"] if a["gate"] == key]
    if ap and ap[-1]["choice"] != "reject":
        return DONE, f"approved: {ap[-1]['choice']}"
    cp = CHECKPOINTS[key]
    hint = {"H1": "storyline id", "H2": "approve|reject", "H3": "approve|reject"}[key]
    return WAIT_HUMAN, f"{cp['name']}: `pipeline.py approve JOB {key} <{hint}>`"


HANDLERS = {"S0": s0_intake, "S1": s1_ideas, "S2": s2_test, "S3": s3_storylines, "S4": s4_shotplan,
            "S5": s5_stills, "S6": s6_motion, "S7": s7_audio, "S8": s8_edit, "S9": s9_qc,
            "S10": s10_deliver, "S11": s11_learn}


# ───────────────────────── commands ─────────────────────────

def cmd_new(product: str, client: str = "spec", root: Path = Path("jobs"), job_id: str | None = None,
            label_text: list[str] | None = None, colours: dict | None = None, packshot: str | None = None,
            url: str | None = None, cap: float = DEFAULT_CAP, stage_caps: dict | None = None,
            ledger: str | None = None, goal: str = "balanced", notes: str = "") -> Path:
    job_id = job_id or f"{slug(client)}-{slug(product)}-{_dt.date.today():%Y%m%d}"
    path = Path(root) / job_id
    if (path / "job.json").exists():
        raise SystemExit(f"job exists: {path}")
    D.cmd_new(path, product, client)                       # brief/concepts/script/... markdown views
    intake = path / "00-intake"
    intake.mkdir(parents=True, exist_ok=True)
    pack_name = None
    if packshot:
        src = Path(packshot)
        if not src.exists():
            raise SystemExit(f"packshot not found: {packshot}")
        pack_name = "packshot" + src.suffix.lower()
        shutil.copyfile(src, intake / pack_name)
    _write_json(intake / "product.json", {"name": product, "client": client, "url": url,
                                          "label_text": label_text or [], "notes": notes,
                                          "assumed": [] if label_text else ["label_text"]})
    _write_json(intake / "brand_kit.json", {"name": product, "label_text": label_text or [],
                                            "colours": colours or {}, "typeface": None, "sonic_logo": None,
                                            "forbidden_marks": ["swoosh", "three stripes"],
                                            "packshot": pack_name, "label_crop": None, "colour_world": None})
    caps = {**DEFAULT_STAGE_CAPS, **(stage_caps or {})}
    if sum(caps.values()) > cap + 1e-9:
        print(f"note: stage caps sum to ${sum(caps.values()):.2f} > job cap ${cap:.2f}; the job cap still rules",
              file=sys.stderr)
    data = {"job_id": job_id, "client": client, "product": product, "created": now(),
            "stage": "S0", "status": PENDING, "goal": goal,
            "ledger": str(ledger or D.DEFAULT_LEDGER),
            "budget": {"cap_usd": cap, "stage_caps": caps, "approve_over_usd": APPROVE_OVER_USD,
                       "spent_usd": 0.0, "estimated_usd": 0.0, "billed_usd": 0.0},
            "taste": {"tone": "aesthetic_brand_film", "no_talking_heads": True},
            "stages": {k: {"status": PENDING, "note": "", "at": None} for k in ORDER},
            "approvals": [], "hold": None,
            "history": [{"at": now(), "stage": "S0", "event": "created"}]}
    _write_json(path / "job.json", data)
    job = Job(path)
    job.save()
    return path


def cmd_advance(path: Path, approve: bool = False, dry_run: bool = False) -> dict:
    job = Job(path)
    if job.data.get("hold"):
        raise SystemExit(f"job on hold: {job.data['hold']} (a human clears it with `budget --release-hold`)")
    approval_left = approve
    steps = []
    while job.data["stage"] != DONE:
        key = job.data["stage"]
        was_paid = key in PAID_STAGES
        if key in CHECKPOINTS:
            status, note = checkpoint(job, key)
        else:
            status, note = HANDLERS[key](job, approve=approval_left, dry_run=dry_run)
        job.set(key, status, note, **{k: v for k, v in job.data["stages"].get(key, {}).items()
                                      if k == "plates_done"})
        steps.append({"stage": key, "status": status, "note": note})
        if status != DONE:
            job.event(key, status, note=note)
            break
        job.event(key, "done", note=note)
        nxt = ORDER.index(key) + 1
        job.data["stage"] = ORDER[nxt] if nxt < len(ORDER) else DONE
        if was_paid and approve:
            approval_left = False                    # --approve covers one paid step, not the whole run
        job.save()
    job.save()
    return {"stage": job.data["stage"], "status": job.data["status"], "steps": steps}


def cmd_approve(path: Path, gate: str, choice: str, notes: str = "", by: str = "client") -> dict:
    job = Job(path)
    if gate not in CHECKPOINTS:
        raise SystemExit(f"unknown checkpoint {gate}; use H1, H2 or H3")
    if job.data["stage"] != gate:
        raise SystemExit(f"{gate} is not the open checkpoint (job is at {job.data['stage']}: run `advance`)")
    cp = CHECKPOINTS[gate]
    reject = choice.lower() == "reject"
    rec = {"gate": gate, "by": by, "at": now(), "choice": "reject" if reject else choice, "notes": notes}
    if gate == "H1" and not reject:
        sl = _read_json(job.d("S3") / "storylines.json", [])
        ids = [s.get("id") for s in sl]
        if choice not in ids:
            raise SystemExit(f"H1 choice must be one of {ids} or 'reject'")
        rec["approved"] = "30-storylines/storylines.json#" + choice
        log_storylines(job, sl, choice, notes)
    elif gate != "H1" and not reject and choice.lower() != "approve":
        raise SystemExit(f"{gate} choice must be 'approve' or 'reject'")
    if gate == "H2" and not reject:
        plan = latest_version(job.d("S4"), "plan_stills")
        rec["approved"] = plan.name if plan else None
    job.data["approvals"].append(rec)
    _write_json(job.path / cp["dir"] / f"approval_{gate}.json", rec)
    if reject:
        back = cp["reject_to"]
        for k in ORDER[ORDER.index(back):ORDER.index(gate) + 1]:
            job.set(k, PENDING, f"reopened by {gate} rejection")
        job.data["stage"] = back
        job.event(gate, "rejected", by=by, notes=notes, back_to=back)
    else:
        job.set(gate, DONE, f"approved: {rec['choice']}")
        job.data["stage"] = ORDER[ORDER.index(gate) + 1]
        job.event(gate, "approved", by=by, choice=rec["choice"], notes=notes)
    job.save()
    return rec


def log_storylines(job: Job, storylines: list[dict], choice: str, notes: str) -> None:
    """H1 -> creative ledger (chosen and rejected), so the dice never repeat them for this client."""
    ledger = Path(job.data["ledger"])
    for s in storylines:
        seed = s.get("seed")
        if not isinstance(seed, dict) or any(d not in seed for d in D.DIMS):
            continue
        res = f"client chose at H1 ({notes})" if s["id"] == choice else "rejected at H1"
        D.append_ledger(ledger, {"date": _dt.date.today().isoformat(), "client": job.data["client"],
                                 "product": job.data["product"], "title": s.get("title", s["id"]),
                                 "seed": seed, "result": res.replace(" ()", "")})


def cmd_bill(path: Path, entry_id: str, usd: float) -> dict:
    job = Job(path)
    recs = read_spend(job)
    ent = next((r for r in recs if r.get("type") == "spend" and r["id"] == entry_id), None)
    if ent is None:
        raise SystemExit(f"no ledger entry {entry_id}")
    bill = {"type": "bill", "ref": entry_id, "billed_usd": float(usd), "at": now()}
    with open(job.ledger, "a", encoding="utf-8") as f:
        f.write(json.dumps(bill) + "\n")
    est = float(ent.get("est_usd") or 0)
    if usd > est * (1 + RECONCILE_TOLERANCE) + 1e-9:
        job.data["hold"] = (f"{entry_id} billed ${usd:.3f} vs estimate ${est:.3f} (> {RECONCILE_TOLERANCE:.0%}): "
                            f"fix the price model before spending more")
        job.event(ent["stage"], "over_estimate", entry=entry_id, est_usd=est, billed_usd=usd)
    job.save()
    return bill


def cmd_budget(path: Path, cap: float | None = None, stage_caps: dict | None = None,
               approve_over: float | None = None, release_hold: bool = False) -> dict:
    job = Job(path)
    b = job.data["budget"]
    if cap is not None:
        b["cap_usd"] = cap
    if stage_caps:
        b["stage_caps"].update(stage_caps)
    if approve_over is not None:
        b["approve_over_usd"] = approve_over
    if release_hold:
        job.data["hold"] = None
    job.event(job.data["stage"], "budget", cap=cap, stage_caps=stage_caps, approve_over=approve_over,
              release_hold=release_hold)
    job.save()
    return b


def status_report(path: Path) -> dict:
    job = Job(path)
    t = totals(read_spend(job))
    return {"job_id": job.data["job_id"], "stage": job.data["stage"], "status": job.data["status"],
            "hold": job.data.get("hold"), "budget": job.data["budget"], "spend": t,
            "stages": [{"stage": k, "name": (STAGES.get(k) or (CHECKPOINTS[k]["name"],))[0],
                        **job.data["stages"].get(k, {})} for k in ORDER],
            "approvals": job.data["approvals"]}


def print_status(rep: dict) -> None:
    b, t = rep["budget"], rep["spend"]
    print(f"job {rep['job_id']}  stage {rep['stage']}  status {rep['status']}"
          + (f"  HOLD: {rep['hold']}" if rep.get("hold") else ""))
    print(f"budget ${b['cap_usd']:.2f}  spent ${t['effective_usd']:.2f} (estimated ${t['estimated_usd']:.2f}, "
          f"billed ${t['billed_usd']:.2f}, {len(t['unbilled'])} unreconciled)  approve over ${b['approve_over_usd']:.2f}")
    for s in rep["stages"]:
        cap = b["stage_caps"].get(s["stage"])
        used = t["by_stage"].get(s["stage"], {}).get("effective_usd", 0.0)
        money = f"${used:.2f}/${cap:.2f}" if cap is not None else ""
        mark = "▶" if s["stage"] == rep["stage"] else " "
        print(f"{mark} {s['stage']:<4} {s['name']:<16} {s.get('status', PENDING):<18} {money:<14} {s.get('note') or ''}")


def _kv(items: list[str], what: str) -> dict:
    out = {}
    for x in items:
        if "=" not in x:
            raise SystemExit(f"{what} must look like KEY=VALUE, got {x!r}")
        k, v = x.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="pipeline.py", description=__doc__.splitlines()[0])
    ap.add_argument("--root", default="jobs", help="folder holding jobs/<job_id>/ (default ./jobs)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", help="product intake: create jobs/<id>/")
    n.add_argument("--product", required=True); n.add_argument("--client", default="spec")
    n.add_argument("--id", default=None); n.add_argument("--label-text", action="append", default=[])
    n.add_argument("--colour", action="append", default=[], help="name=#hex")
    n.add_argument("--packshot", default=None); n.add_argument("--url", default=None)
    n.add_argument("--notes", default="")
    n.add_argument("--cap", type=float, default=DEFAULT_CAP, help="job budget cap in USD (default 10)")
    n.add_argument("--stage-cap", action="append", default=[], help="S6=5 (USD)")
    n.add_argument("--ledger", default=None, help="director creative ledger (default ~/.ad-director/ledger.jsonl)")
    n.add_argument("--goal", choices=sorted(D.GOALS), default="balanced")
    s = sub.add_parser("status", help="stage table + budget"); s.add_argument("job"); s.add_argument("--json", action="store_true")
    a = sub.add_parser("advance", help="run stages until an agent, human or approval is needed")
    a.add_argument("job"); a.add_argument("--approve", action="store_true",
                                          help="human approval for ONE paid step over the $2 threshold")
    a.add_argument("--dry-run", action="store_true", help="estimate the next paid step; spend nothing")
    p = sub.add_parser("approve", help="record a human checkpoint decision")
    p.add_argument("job"); p.add_argument("checkpoint", choices=sorted(CHECKPOINTS)); p.add_argument("choice")
    p.add_argument("--notes", default=""); p.add_argument("--by", default="client")
    sp = sub.add_parser("spend", help="ledger: estimated vs billed"); sp.add_argument("job")
    sp.add_argument("--bill", nargs=2, metavar=("ENTRY_ID", "USD"), default=None)
    sp.add_argument("--json", action="store_true")
    bu = sub.add_parser("budget", help="change caps (human only)"); bu.add_argument("job")
    bu.add_argument("--cap", type=float, default=None); bu.add_argument("--stage-cap", action="append", default=[])
    bu.add_argument("--approve-over", type=float, default=None); bu.add_argument("--release-hold", action="store_true")
    x = ap.parse_args(argv)

    if x.cmd == "new":
        caps = {k: float(v) for k, v in _kv(x.stage_cap, "--stage-cap").items()}
        bad = [k for k in caps if k not in STAGES]
        if bad:
            ap.error(f"unknown stage(s) {bad}")
        path = cmd_new(x.product, x.client, Path(x.root), x.id, x.label_text, _kv(x.colour, "--colour"),
                       x.packshot, x.url, x.cap, caps, x.ledger, x.goal, x.notes)
        print(path)
        return 0
    path = resolve_job(x.job, x.root)
    if x.cmd == "status":
        rep = status_report(path)
        print(json.dumps(rep, indent=2)) if x.json else print_status(rep)
        return 0
    if x.cmd == "advance":
        res = cmd_advance(path, x.approve, x.dry_run)
        for st in res["steps"]:
            print(f"{st['stage']:<4} {st['status']:<18} {st['note']}")
        print(f"-> now at {res['stage']} ({res['status']})")
        return 0 if res["status"] in (DONE, PENDING, WAIT_AGENT, WAIT_HUMAN) or res["stage"] == DONE else 3
    if x.cmd == "approve":
        print(json.dumps(cmd_approve(path, x.checkpoint, x.choice, x.notes, x.by), indent=2))
        return 0
    if x.cmd == "spend":
        if x.bill:
            print(json.dumps(cmd_bill(path, x.bill[0], float(x.bill[1]))))
        job = Job(path)
        recs = read_spend(job)
        t = totals(recs)
        if x.json:
            print(json.dumps({"entries": recs, "totals": t}, indent=2))
            return 0
        for r in recs:
            if r.get("type") == "spend":
                b = r.get("billed_usd")
                print(f"{r['id']}  {r['stage']:<3} {r['tool']:<10} {r['item']:<24} est ${float(r.get('est_usd') or 0):.3f}"
                      f"  billed {'-' if b is None else f'${b:.3f}'}  {r.get('status', '')}"
                      + ("  (cache)" if r.get("cached") else ""))
            else:
                print(f"bill  {r['ref']}  ${r['billed_usd']:.3f}")
        print(f"total: estimated ${t['estimated_usd']:.2f}  billed ${t['billed_usd']:.2f}  "
              f"effective ${t['effective_usd']:.2f} of ${job.data['budget']['cap_usd']:.2f}")
        return 0
    if x.cmd == "budget":
        caps = {k: float(v) for k, v in _kv(x.stage_cap, "--stage-cap").items()}
        print(json.dumps(cmd_budget(path, x.cap, caps, x.approve_over, x.release_hold), indent=2))
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
