"""pipeline.py: job state, ledger, caps, approvals, checkpoints (mock APIs: no network, no cost)."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import director as D  # noqa: E402
import elevenlabs as E  # noqa: E402
import hfgen as H  # noqa: E402
import pipeline as P  # noqa: E402
from test_hfgen import PNG, api  # noqa: E402,F401  (fixture: local mock of the Higgsfield API)

SOUL = "higgsfield-ai/soul/cinema"
KLING3 = "kling-video/v3.0/pro/image-to-video"


@pytest.fixture
def job(tmp_path):
    return P.cmd_new("SOL Water", "Driftline", root=tmp_path / "jobs", job_id="sol", label_text=["SOL"],
                     colours={"primary": "#C9A65A"}, ledger=str(tmp_path / "ledger.jsonl"))


def jdata(path):
    return json.loads((path / "job.json").read_text())


def put(path: Path, rel: str, obj):
    p = path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj))
    return p


def at(path: Path, stage: str):
    """Jump the job pointer (unit tests of one stage)."""
    d = jdata(path)
    d["stage"] = stage
    (path / "job.json").write_text(json.dumps(d))


SEED = {"mechanism": "m1", "format": "f1", "hook": "h1", "emotion": "e1", "structure": "s1", "look": "l1",
        "sonic": "so1"}


def front_artefacts(path: Path):
    put(path, "10-ideas/ideas.json", [{"title": f"idea {i}"} for i in range(7)])
    drv = {"hook": 4, "curiosity": 3, "emotion": 3, "product_desire": 4}
    put(path, "20-tests/drivers.json", [{"title": "A", "drivers": drv, "mechanism": "literalised"},
                                        {"title": "B", "drivers": {**drv, "hook": 5}, "mechanism": "contrast"},
                                        {"title": "C", "drivers": {**drv, "hook": 2}, "mechanism": "ritual"}])
    put(path, "30-storylines/storylines.json",
        [{"id": s, "title": f"Story {s}", "big_idea_shot": "sun sets into the bottle", "cta": "Shop",
          "seed": {**SEED, "format": f"f{s}"}} for s in "ABC"])


def stills_plan(path: Path, takes=2, model=SOUL, args=None, version=1):
    args = args or {"prompt": "empty marble ledge, window light", "resolution": "720p"}
    return put(path, f"40-shotplan/plan_stills.v{version}.json",
               {"jobs": [{"id": "plate1", "model": model, "takes": takes, "args": args}]})


# ───────────── intake / state ─────────────

def test_new_writes_job_state_and_intake(job, tmp_path):
    d = jdata(job)
    assert d["stage"] == "S0" and d["budget"]["cap_usd"] == 10.0
    assert d["budget"]["stage_caps"] == P.DEFAULT_STAGE_CAPS and d["budget"]["approve_over_usd"] == 2.0
    assert set(d["stages"]) == set(P.ORDER) and {"H1", "H2", "H3"} <= set(d["stages"])
    assert json.loads((job / "00-intake/brand_kit.json").read_text())["colours"] == {"primary": "#C9A65A"}
    assert (job / "01-brief.md").exists()                    # director.py new scaffold
    assert not (job / "spend.jsonl").exists()
    with pytest.raises(SystemExit, match="exists"):
        P.cmd_new("SOL Water", "Driftline", root=tmp_path / "jobs", job_id="sol")


def test_intake_waits_for_exact_label(tmp_path):
    pack = tmp_path / "pack.png"
    pack.write_bytes(PNG)
    path = P.cmd_new("SOL", "Driftline", root=tmp_path / "jobs", packshot=str(pack), ledger=str(tmp_path / "l"))
    assert path.name.startswith("driftline-sol-") and (path / "00-intake/packshot.png").exists()
    res = P.cmd_advance(path)
    assert res["stage"] == "S0" and res["status"] == P.WAIT_AGENT
    prod = json.loads((path / "00-intake/product.json").read_text())
    put(path, "00-intake/product.json", {**prod, "label_text": ["SOL"]})
    assert P.cmd_advance(path)["stage"] == "S1"


def test_free_stages_chain_to_h1_and_approval_logs_ledger(job, tmp_path):
    res = P.cmd_advance(job)
    assert res["stage"] == "S1" and res["status"] == P.WAIT_AGENT
    assert len(json.loads((job / "10-ideas/seeds.json").read_text())) == 5      # dice rolled for the agents
    front_artefacts(job)
    res = P.cmd_advance(job)
    assert [s["stage"] for s in res["steps"]] == ["S1", "S2", "S3", "H1"]
    assert res["stage"] == "H1" and res["status"] == P.WAIT_HUMAN
    tests = json.loads((job / "20-tests/tests.json").read_text())
    assert tests["ranking"][0]["title"] == "B"
    with pytest.raises(SystemExit, match="one of"):
        P.cmd_approve(job, "H1", "Z")
    with pytest.raises(SystemExit, match="not the open checkpoint"):
        P.cmd_approve(job, "H2", "approve")
    P.cmd_approve(job, "H1", "B", notes="less gold")
    d = jdata(job)
    assert d["stage"] == "S4" and d["approvals"][-1]["choice"] == "B"
    assert json.loads((job / "30-storylines/approval_H1.json").read_text())["notes"] == "less gold"
    led = D.read_ledger(tmp_path / "ledger.jsonl")
    assert {e["title"]: e["result"] for e in led} == {"Story A": "rejected at H1",
                                                      "Story B": "client chose at H1 (less gold)",
                                                      "Story C": "rejected at H1"}


def test_s2_needs_two_mechanisms_in_top3(job):
    at(job, "S2")
    drv = {"hook": 4}
    put(job, "20-tests/drivers.json", [{"title": t, "drivers": drv, "mechanism": "same"} for t in "ABC"])
    res = P.cmd_advance(job)
    assert res["status"] == P.BLOCKED and "one mechanism" in res["steps"][-1]["note"]


# ───────────── paid stages: dry-run first, caps, approval ─────────────

def spy_batch(monkeypatch):
    calls = []
    real = H.cmd_batch

    def spy(*a, **kw):
        calls.append(kw.get("dry_run"))
        return real(*a, **kw)
    monkeypatch.setattr(H, "cmd_batch", spy)
    return calls


def test_stills_dry_run_first_then_spend_ledger_then_h2(api, job, monkeypatch):
    calls = spy_batch(monkeypatch)
    at(job, "S4")
    put(job, "40-shotplan/shots.json", [{"id": "plate1", "model": SOUL}])
    stills_plan(job, takes=2)
    res = P.cmd_advance(job)
    assert [s["stage"] for s in res["steps"]] == ["S4", "S5", "H2"] and res["status"] == P.WAIT_HUMAN
    assert calls == [True, True, False]                      # S4 preflight, S5 dry run, S5 spend
    sent = api.bodies[0][1]
    assert sent["aspect_ratio"] == "9:16" and sent["enhance_prompt"] is False   # hfgen safe defaults
    recs = P.read_spend(P.Job(job))
    assert len(recs) == 2 and all(r["stage"] == "S5" and r["tool"] == "hfgen" for r in recs)
    assert [r["est_usd"] for r in recs] == [0.02, 0.02] and all(r["billed_usd"] is None for r in recs)
    assert (job / recs[0]["files"][0]).exists()
    assert jdata(job)["budget"]["spent_usd"] == pytest.approx(0.04)
    # re-running the stage never double-logs or re-pays
    P.record_hfgen_spend(P.Job(job), "S5", job / "50-stills/clips", approved=False)
    assert len(P.read_spend(P.Job(job))) == 2 and api.submits == 2
    P.cmd_approve(job, "H2", "approve")
    assert jdata(job)["stage"] == "S6"
    res = P.cmd_advance(job)
    assert res["stage"] == "S6" and res["status"] == P.WAIT_AGENT


def test_spend_over_threshold_needs_approve(api, job):
    at(job, "S6")
    put(job, "60-motion/plan_motion.v1.json",
        {"jobs": [{"id": "m1", "model": KLING3, "takes": 5, "args": {"prompt": "push", "image_url": "https://a/b.png"}}]})
    res = P.cmd_advance(job)                                  # 5 x $0.50 = $2.50 > $2
    assert res["status"] == P.WAIT_APPROVAL and "--approve" in res["steps"][-1]["note"]
    assert api.submits == 0 and not P.read_spend(P.Job(job))
    res = P.cmd_advance(job, approve=True)
    assert api.submits == 5 and res["steps"][0]["status"] == P.DONE
    recs = P.read_spend(P.Job(job))
    assert len(recs) == 5 and all(r["approved"] for r in recs)
    assert api.bodies[0][1]["sound"] == "off"


def test_single_call_over_threshold_needs_approve(api, job):
    at(job, "S6")
    api.estimate_override[KLING3] = {"usd": "2.40"}
    put(job, "60-motion/plan_motion.v1.json",
        {"jobs": [{"id": "m1", "model": KLING3, "takes": 1, "args": {"prompt": "x", "image_url": "https://a/b.png"}}]})
    assert P.cmd_advance(job)["status"] == P.WAIT_APPROVAL and api.submits == 0


def test_stage_and_job_caps_block_even_with_approve(api, job):
    at(job, "S6")
    put(job, "60-motion/plan_motion.v1.json",
        {"jobs": [{"id": "m1", "model": KLING3, "takes": 12, "args": {"prompt": "x", "image_url": "https://a/b.png"}}]})
    res = P.cmd_advance(job, approve=True)                    # $6 > S6 cap $5
    assert res["status"] == P.BLOCKED and "S6 cap" in res["steps"][-1]["note"]
    P.cmd_budget(job, stage_caps={"S6": 20.0}, cap=5.0)
    res = P.cmd_advance(job, approve=True)                    # $6 > job cap $5
    assert res["status"] == P.BLOCKED and "job cap" in res["steps"][-1]["note"]
    assert api.submits == 0


def test_bad_field_or_unpriced_plan_blocks_before_spend(api, job):
    at(job, "S4")
    put(job, "40-shotplan/shots.json", [{"id": "k"}])
    stills_plan(job, model=KLING3, args={"prompt": "x", "image_url": "https://a/b.png", "end_image_url": "https://a/c.png"})
    res = P.cmd_advance(job)
    assert res["status"] == P.BLOCKED and "last_image_url" in res["steps"][-1]["note"]
    api.estimate_override[SOUL] = {"type": "description", "pricing_description": "call us"}
    stills_plan(job, version=2)
    res = P.cmd_advance(job)
    assert res["status"] == P.BLOCKED and "UNPRICED plate1" in res["steps"][-1]["note"]
    assert api.submits == 0


def test_advance_dry_run_spends_nothing(api, job):
    at(job, "S5")
    stills_plan(job)
    res = P.cmd_advance(job, dry_run=True)
    assert res["stage"] == "S5" and res["status"] == P.PENDING and "would spend $0.04" in res["steps"][0]["note"]
    assert api.submits == 0 and not P.read_spend(P.Job(job))


def test_failed_takes_block_and_are_not_charged(api, job):
    at(job, "S5")
    stills_plan(job, takes=1, args={"prompt": "FAIL please"})
    res = P.cmd_advance(job)
    assert res["status"] == P.BLOCKED and "failed" in res["steps"][-1]["note"]
    recs = P.read_spend(P.Job(job))
    assert len(recs) == 1 and recs[0]["est_usd"] == 0 and recs[0]["status"] == "failed"


def test_h2_reject_reopens_shot_plan(api, job):
    at(job, "S5")
    stills_plan(job, takes=1)
    put(job, "40-shotplan/shots.json", [{"id": "plate1"}])
    assert P.cmd_advance(job)["stage"] == "H2"
    P.cmd_approve(job, "H2", "reject", notes="too centred")
    d = jdata(job)
    assert d["stage"] == "S4" and d["stages"]["S5"]["status"] == P.PENDING
    assert "reopened" in d["stages"]["H2"]["note"]
    with pytest.raises(SystemExit, match="approve' or 'reject"):
        at(job, "H2")
        P.cmd_approve(job, "H2", "maybe")


# ───────────── audio (ElevenLabs) ─────────────

@pytest.fixture
def eleven(monkeypatch):
    calls = []

    def fake(method, path, body=None, query=None, retries=3, timeout=300):
        calls.append((path, body))
        if "with-timestamps" in path:
            al = {"characters": list("Go"), "character_start_times_seconds": [0, .1],
                  "character_end_times_seconds": [.1, .2]}
            import base64
            return json.dumps({"audio_base64": base64.b64encode(b"ID3vo").decode(), "alignment": al}).encode(), \
                {"character-cost": "2"}
        return b"ID3audio", {}
    monkeypatch.setattr(E, "_call_full", fake)
    return calls


def test_audio_stage_estimates_caches_and_logs(job, eleven):
    at(job, "S7")
    plan = {"vo": [{"id": "vo1", "text": "Go", "voice": "v1"}],
            "sfx": [{"id": "pop", "prompt": "can pop", "seconds": 1.5}],
            "music": [{"id": "bed", "prompt": "warm lo-fi", "seconds": 12}]}
    put(job, "70-audio/audio_plan.json", plan)
    res = P.cmd_advance(job)
    assert res["steps"][0] == {"stage": "S7", "status": P.DONE, "note": res["steps"][0]["note"]}
    assert len(eleven) == 3 and eleven[0][1]["model_id"] == "eleven_v4"
    recs = P.read_spend(P.Job(job))
    assert [r["item"] for r in recs] == ["vo:vo1", "sfx:pop", "music:bed"]
    assert recs[0]["credits_billed"] == 2 and recs[0]["billed_usd"] == pytest.approx(2 * E.usd_per_credit())
    assert recs[2]["est_usd"] == pytest.approx(600 * E.usd_per_credit())
    assert (job / "70-audio/vo1.mp3").read_bytes() == b"ID3vo" and (job / "70-audio/vo1.words.json").exists()
    # same plan again: everything comes from the content-hash cache, nothing paid or re-logged
    at(job, "S7")
    P.cmd_advance(job)
    assert len(eleven) == 3 and len(P.read_spend(P.Job(job))) == 3


def test_audio_per_call_cap_and_plan_errors(job, eleven):
    at(job, "S7")
    put(job, "70-audio/audio_plan.json", {"music": [{"id": "bed", "prompt": "long", "seconds": 60,
                                                     "max_credits": 100}]})
    res = P.cmd_advance(job)
    assert res["status"] == P.BLOCKED and "per-call cap" in res["steps"][-1]["note"] and not eleven
    put(job, "70-audio/audio_plan.json", {"vo": [{"id": "x", "text": "hi"}]})        # no voice
    assert P.cmd_advance(job)["status"] == P.BLOCKED


# ───────────── edit / qc / final ─────────────

def test_edit_qc_h3_deliver_to_done(job, monkeypatch):
    at(job, "S8")
    assert P.cmd_advance(job)["status"] == P.WAIT_AGENT
    (job / "80-edit").mkdir(exist_ok=True)
    (job / "80-edit/master_v1.mp4").write_bytes(b"x")
    monkeypatch.setattr(P.shutil, "which", lambda n: "/usr/bin/ffmpeg")
    monkeypatch.setattr(D, "cmd_qc", lambda *a, **k: {"verdict": "FAIL", "findings": [
        {"level": "FAIL", "check": "loudness", "msg": "-20 LUFS"}]})
    res = P.cmd_advance(job)
    assert res["stage"] == "S9" and res["status"] == P.BLOCKED and "-20 LUFS" in res["steps"][-1]["note"]
    monkeypatch.setattr(D, "cmd_qc", lambda *a, **k: {"verdict": "WARN", "findings": []})
    assert P.cmd_advance(job)["stage"] == "H3"
    P.cmd_approve(job, "H3", "approve", by="director")
    assert P.cmd_advance(job)["stage"] == "S10"
    put(job, "99-deliver/delivery.json", {"masters": []})
    res = P.cmd_advance(job)
    assert res["stage"] == P.DONE and jdata(job)["status"] == P.DONE


# ───────────── ledger, reconcile, CLI ─────────────

def test_totals_estimated_vs_billed():
    recs = [{"type": "spend", "id": "sp-0001", "stage": "S5", "est_usd": 0.30, "billed_usd": None},
            {"type": "spend", "id": "sp-0002", "stage": "S6", "est_usd": 0.48, "billed_usd": None},
            {"type": "bill", "ref": "sp-0002", "billed_usd": 0.40}]
    t = P.totals(recs)
    assert t["estimated_usd"] == pytest.approx(0.78) and t["billed_usd"] == pytest.approx(0.40)
    assert t["effective_usd"] == pytest.approx(0.70) and t["unbilled"] == ["sp-0001"]
    assert t["by_stage"]["S6"]["effective_usd"] == pytest.approx(0.40)


def test_bill_over_estimate_puts_job_on_hold(api, job):
    at(job, "S5")
    stills_plan(job, takes=1)
    P.cmd_advance(job)
    P.cmd_bill(job, "sp-0001", 0.021)                         # within 10 %
    assert jdata(job)["hold"] is None
    P.cmd_bill(job, "sp-0001", 0.05)
    assert "billed" in jdata(job)["hold"]
    with pytest.raises(SystemExit, match="on hold"):
        P.cmd_advance(job)
    P.cmd_budget(job, release_hold=True)
    assert jdata(job)["hold"] is None
    lines = (job / "spend.jsonl").read_text().splitlines()
    assert len(lines) == 3                                    # append-only: 1 spend + 2 bills
    assert P.totals(P.read_spend(P.Job(job)))["billed_usd"] == pytest.approx(0.05)


def test_cli_roundtrip(tmp_path, capsys):
    root = str(tmp_path / "jobs")
    assert P.main(["--root", root, "new", "--product", "AURUM", "--client", "Acme", "--id", "au",
                   "--label-text", "AURUM", "--stage-cap", "S6=4", "--cap", "8",
                   "--ledger", str(tmp_path / "l.jsonl")]) == 0
    capsys.readouterr()
    assert P.main(["--root", root, "status", "au", "--json"]) == 0
    st = json.loads(capsys.readouterr().out)
    assert st["budget"]["cap_usd"] == 8 and st["budget"]["stage_caps"]["S6"] == 4
    assert P.main(["--root", root, "advance", "au"]) == 0
    assert "S1" in capsys.readouterr().out
    assert P.main(["--root", root, "spend", "au"]) == 0
    assert "effective $0.00" in capsys.readouterr().out
    with pytest.raises(SystemExit):
        P.main(["--root", root, "new", "--product", "X", "--stage-cap", "S99=1"])
    with pytest.raises(SystemExit, match="job not found"):
        P.main(["--root", root, "status", "nope"])
