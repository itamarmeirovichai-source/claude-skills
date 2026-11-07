"""hfgen against a local mock of the Higgsfield API (no network, no cost)."""
import json
import sys
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import hfgen as H  # noqa: E402

PNG = (b"\x89PNG\r\n\x1a\n" + b"0" * 64)


class Mock:
    def __init__(self):
        self.requests = {}       # id -> {"polls": n, "kind": "video"|"image", "fail": bool}
        self.by_key = {}         # idempotency key -> id
        self.submits = 0
        self.uploads = {}
        self.auth_seen = []
        self.estimates = []       # (path, body) of every /estimate call
        self.bodies = []          # (path, body) of every paid submit
        self.estimate_override = {}   # endpoint path -> estimate response


def make_server(mock: Mock):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _json(self, code, obj):
            body = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _body(self):
            n = int(self.headers.get("Content-Length") or 0)
            return self.rfile.read(n) if n else b""

        def do_PUT(self):
            mock.uploads[self.path] = self._body()
            self.send_response(200); self.end_headers()

        def do_GET(self):
            base = f"http://127.0.0.1:{self.server.server_port}"
            if self.path.startswith("/media/"):
                data = b"fakevideo" if self.path.endswith(".mp4") else PNG
                self.send_response(200); self.send_header("Content-Length", str(len(data))); self.end_headers()
                self.wfile.write(data); return
            mock.auth_seen.append(self.headers.get("Authorization"))
            if self.headers.get("Authorization") != "Key kid:ksecret":
                return self._json(401, {"detail": "Invalid credentials"})
            rid = self.path.split("/")[2]
            r = mock.requests.get(rid)
            if not r:
                return self._json(404, {"detail": "Not found"})
            r["polls"] += 1
            if r["polls"] < 2:
                return self._json(200, {"status": "in_progress", "request_id": rid})
            if r["fail"]:
                return self._json(200, {"status": "failed", "request_id": rid, "error": "Generation failed"})
            out = ({"video": {"url": f"{base}/media/{rid}.mp4"}} if r["kind"] == "video"
                   else {"images": [{"url": f"{base}/media/{rid}.png"}]})
            return self._json(200, {"status": "completed", "request_id": rid, **out})

        def do_POST(self):
            base = f"http://127.0.0.1:{self.server.server_port}"
            body = json.loads(self._body() or b"{}")
            if self.headers.get("Authorization") != "Key kid:ksecret":
                return self._json(401, {"detail": "Invalid credentials"})
            if self.path == "/files/generate-upload-url":
                name = uuid.uuid4().hex
                return self._json(200, {"public_url": f"{base}/media/{name}.png",
                                        "upload_url": f"{base}/put/{name}",
                                        "upload_headers": {"Content-Type": body["content_type"]}})
            if self.path.startswith("/estimate/"):
                mock.estimates.append((self.path, body))
                ep = self.path[len("/estimate/"):]
                if ep in mock.estimate_override:
                    return self._json(200, mock.estimate_override[ep])
                usd = "0.50" if "video" in self.path else "0.02"
                return self._json(200, {"credits": "8", "usd": usd})
            mock.bodies.append((self.path, body))
            key = self.headers.get("Idempotency-Key")
            if key in mock.by_key:
                rid = mock.by_key[key]
            else:
                mock.submits += 1
                rid = str(uuid.uuid4())
                mock.by_key[key] = rid
                mock.requests[rid] = {"polls": 0, "kind": "video" if "video" in self.path else "image",
                                      "fail": "FAIL" in body.get("prompt", "")}
            return self._json(200, {"status": "queued", "request_id": rid,
                                    "status_url": f"{base}/requests/{rid}/status"})
    srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


@pytest.fixture
def api(monkeypatch):
    mock = Mock()
    srv = make_server(mock)
    monkeypatch.setattr(H, "API", f"http://127.0.0.1:{srv.server_port}")
    monkeypatch.setenv("HF_KEY", "kid:ksecret")
    monkeypatch.setattr(H.time, "sleep", lambda s: None)
    yield mock
    srv.shutdown()


def test_credentials_variants():
    assert H.credentials({"HF_KEY": "a:b"}) == "a:b"
    assert H.credentials({"HF_API_KEY_ID": "a", "HF_API_KEY_SECRET": "b"}) == "a:b"
    assert H.credentials({"HF_API_KEY": "a", "HF_API_SECRET": "b"}) == "a:b"
    assert H.credentials({"HIGGSFIELD_API_KEY": "a:b"}) == "a:b"
    with pytest.raises(SystemExit):
        H.credentials({"HIGGSFIELD_API_KEY": "no-secret"})


def test_idem_key_stable_and_distinct():
    a = H.idem_key("s1", 1, "m", {"p": 1})
    assert a == H.idem_key("s1", 1, "m", {"p": 1})
    assert a != H.idem_key("s1", 2, "m", {"p": 1})
    assert a != H.idem_key("s1", 1, "m", {"p": 1}, salt="x")
    assert len(a) < 255 and " " not in a


def write_plan(tmp_path, jobs):
    (tmp_path / "frames").mkdir()
    (tmp_path / "frames" / "r1.png").write_bytes(PNG)
    p = tmp_path / "plan.json"
    p.write_text(json.dumps({"defaults": {"takes": 2}, "jobs": jobs}))
    return p


JOBS = [
    {"id": "frame1", "model": "higgsfield-ai/soul/standard", "takes": 1, "args": {"prompt": "dog in hallway"}},
    {"id": "shot1", "model": "kling-video/v2.5-turbo/pro/image-to-video",
     "args": {"prompt": "slow push in", "image_url": "@file:frames/r1.png", "duration": 5}},
]


def test_batch_dry_run_estimates_without_submitting(api, tmp_path):
    p = write_plan(tmp_path, JOBS)
    res = H.cmd_batch(p, budget=10, dry_run=True, yes=True, concurrency=2, out=None, salt="", only=None)
    assert res["estimated_usd"] == pytest.approx(0.02 + 2 * 0.50)
    assert api.submits == 0 and not api.uploads


def test_batch_refuses_over_budget(api, tmp_path):
    p = write_plan(tmp_path, JOBS)
    with pytest.raises(SystemExit, match="over budget"):
        H.cmd_batch(p, budget=0.5, dry_run=False, yes=True, concurrency=2, out=None, salt="", only=None)
    assert api.submits == 0


def test_batch_runs_downloads_and_resumes(api, tmp_path):
    p = write_plan(tmp_path, JOBS)
    res = H.cmd_batch(p, budget=10, dry_run=False, yes=True, concurrency=2, out=None, salt="", only=None)
    assert res["completed"] == 3 and api.submits == 3
    clips = tmp_path / "clips"
    assert (clips / "shot1_t01.mp4").read_bytes() == b"fakevideo"
    assert (clips / "frame1_t01.png").exists()
    assert len(api.uploads) == 1                      # the @file ref was uploaded once
    man = json.loads((clips / "manifest.json").read_text())
    assert man["summary"]["estimated_spend_usd"] == pytest.approx(1.02)
    assert len((clips / "gen_log.jsonl").read_text().splitlines()) == 3
    # re-run: everything completed -> nothing new submitted, no new uploads
    H.cmd_batch(p, budget=10, dry_run=False, yes=True, concurrency=2, out=None, salt="", only=None)
    assert api.submits == 3 and len(api.uploads) == 1


def test_failed_take_recorded_and_retried_with_same_key(api, tmp_path):
    jobs = [{"id": "bad", "model": "kling-video/v2.5-turbo/pro/text-to-video", "takes": 1, "args": {"prompt": "FAIL"}}]
    p = write_plan(tmp_path, jobs)
    res = H.cmd_batch(p, budget=10, dry_run=False, yes=True, concurrency=1, out=None, salt="", only=None)
    assert res["completed"] == 0 and res["failed"] == 1
    man = json.loads((tmp_path / "clips" / "manifest.json").read_text())
    assert man["takes"]["bad#1"]["status"] == "failed"
    # same key -> API returns the same (failed) request, no double charge
    H.cmd_batch(p, budget=10, dry_run=False, yes=True, concurrency=1, out=None, salt="", only=None)
    assert api.submits == 1
    # --fresh forces a brand-new generation
    H.cmd_batch(p, budget=10, dry_run=False, yes=True, concurrency=1, out=None, salt="retry1", only=None)
    assert api.submits == 2


def test_bad_credentials_raise(api, monkeypatch):
    monkeypatch.setenv("HF_KEY", "wrong:creds")
    with pytest.raises(H.HFError) as ei:
        H.estimate("kling-video/x/text-to-video", {"prompt": "x"})
    assert ei.value.status == 401


def test_check_command(api, capsys):
    assert H.main(["check"]) == 0
    assert "OK" in capsys.readouterr().out


def test_missing_ref_file_is_caught(api, tmp_path):
    p = write_plan(tmp_path, [{"id": "x", "model": "m/video", "args": {"image_url": "@file:frames/nope.png"}}])
    with pytest.raises(SystemExit, match="missing reference"):
        H.cmd_batch(p, budget=10, dry_run=True, yes=True, concurrency=1, out=None, salt="", only=None)


def test_price_from_description_video_and_image():
    d = ("For 16:9 video without video input, your request costs roughly $0.2056 per second of generated video "
         "at 480p, $0.4622 at 720p, and $1.1372 at 1080p. Each 1,000 video tokens costs $0.0214 at 480p or 720p "
         "and $0.0234 at 1080p.")
    assert H.price_from_description(d, {"resolution": "480p", "duration": 4}) == pytest.approx(0.8224)
    assert H.price_from_description(d, {"duration": 5}) == pytest.approx(2.311)
    img = "Per 1M tokens: text input $5, image input $8, image output $30."
    assert H.price_from_description(img, {"resolution": "1k"}) == 0.12
    assert H.price_from_description("unknown pricing", {}) is None


def test_proxy_mode_sends_no_key(monkeypatch):
    monkeypatch.delenv("HF_KEY", raising=False)
    assert H.credentials({"HF_AUTH_VIA_PROXY": "1"}) is None
    with pytest.raises(SystemExit):
        H.credentials({})


# ───────────── money guards: schema check, unpriced jobs, safe defaults, price formats ─────────────

KLING3 = "kling-video/v3.0/pro/image-to-video"
SEED25 = "bytedance/seedance-2.5/image-to-video"
QWEN = "alibaba/qwen-image-3/edit"


def test_unknown_field_refused_before_any_upload_estimate_or_submit(api, tmp_path):
    jobs = [{"id": "bridge", "model": KLING3, "takes": 1,
             "args": {"prompt": "arc", "image_url": "@file:frames/r1.png", "end_image_url": "@file:frames/r1.png"}}]
    p = write_plan(tmp_path, jobs)
    with pytest.raises(SystemExit, match=r"end_image_url.*did you mean last_image_url"):
        H.cmd_batch(p, budget=10, dry_run=False, yes=True, concurrency=1, out=None, salt="", only=None)
    assert api.submits == 0 and not api.uploads and not api.estimates


def test_dry_run_reports_schema_problems_and_is_not_ok(api, tmp_path):
    jobs = [{"id": "bridge", "model": KLING3, "takes": 1,
             "args": {"prompt": "arc", "image_url": "https://x.y/a.png", "duration": 99}}]
    res = H.cmd_batch(write_plan(tmp_path, jobs), budget=10, dry_run=True, yes=True, concurrency=1,
                      out=None, salt="", only=None)
    assert res["ok"] is False and any("maximum 15" in pr for pr in res["problems"])
    assert res["unpriced"] == ["bridge"] and res["estimated_usd"] == 0
    assert api.submits == 0


def test_validate_args_types_enums_required_and_nested():
    assert H.validate_args(KLING3, {"prompt": "x", "image_url": "https://a/b.png", "sound": "off"}) == []
    errs = H.validate_args(KLING3, {"prompt": "x", "sound": "loud", "cfg_scale": "0.5",
                                    "multi_prompt": [{"prompt": "a" * 600, "duration": 2}]})
    joined = " | ".join(errs)
    assert "image_url: required" in joined and "'loud' not in" in joined
    assert "cfg_scale: expected number" in joined and "maxLength 512" in joined
    # Seedance i2v has no aspect_ratio field: a template that adds one would 400
    assert any("aspect_ratio: unknown" in e for e in H.validate_args(SEED25, {"image_url": "https://a/b.png",
                                                                               "aspect_ratio": "9:16"}))
    assert H.validate_args("vendor/made-up-model", {"prompt": "x"})[0].startswith("no known schema")


def test_qwen_rule_prompt_extend_off_needs_thinking_off():
    # prompt_extend false alone 400s upstream ("True was expected"): enable_thinking defaults to true
    errs = H.validate_args(QWEN, {"prompt": "fix label", "image_urls": ["https://a/b.png"], "prompt_extend": False})
    assert errs and "prompt_extend" in errs[0]
    args, inj = H.apply_safe_defaults(QWEN, {"prompt": "fix label", "image_urls": ["https://a/b.png"]})
    assert args["prompt_extend"] is False and args["enable_thinking"] is False
    assert H.validate_args(QWEN, args) == []


def test_safe_defaults_never_override_explicit_values():
    a, inj = H.apply_safe_defaults(KLING3, {"prompt": "x", "image_url": "https://a/b.png"})
    assert a["sound"] == "off" and inj == {"sound": "off"}          # no aspect_ratio field on Kling i2v
    a, inj = H.apply_safe_defaults(KLING3, {"prompt": "x", "image_url": "https://a/b.png", "sound": "on"})
    assert a["sound"] == "on" and inj == {}
    a, inj = H.apply_safe_defaults(SEED25, {"image_url": "https://a/b.png"})
    assert a == {"image_url": "https://a/b.png", "generate_audio": False}
    a, _ = H.apply_safe_defaults("bytedance/seedance-2.5/reference-to-video", {"image_urls": ["https://a/b.png"]})
    assert a["aspect_ratio"] == "9:16" and a["generate_audio"] is False
    a, _ = H.apply_safe_defaults("marketing-studio/image/flare", {"prompt": "x"})
    assert a["enhance_prompt"] is False and a["aspect_ratio"] == "9:16"


def test_batch_submits_safe_defaults(api, tmp_path):
    jobs = [{"id": "k", "model": KLING3, "takes": 1, "args": {"prompt": "push", "image_url": "@file:frames/r1.png"}},
            {"id": "s", "model": SEED25, "takes": 1, "args": {"prompt": "drift", "image_url": "@file:frames/r1.png"}},
            {"id": "q", "model": QWEN, "takes": 1, "args": {"prompt": "fix", "image_urls": ["@file:frames/r1.png"]}}]
    H.cmd_batch(write_plan(tmp_path, jobs), budget=10, dry_run=False, yes=True, concurrency=1,
                out=None, salt="", only=None)
    sent = {path.strip("/"): body for path, body in api.bodies}
    assert sent[KLING3]["sound"] == "off"
    assert sent[SEED25]["generate_audio"] is False and "aspect_ratio" not in sent[SEED25]
    assert sent[QWEN]["prompt_extend"] is False and sent[QWEN]["enable_thinking"] is False
    est = {path[len("/estimate/"):]: body for path, body in api.estimates}
    assert est[KLING3]["sound"] == "off"          # the estimate prices what will actually be sent


def test_unpriced_job_is_refused_not_counted_as_zero(api, tmp_path):
    api.estimate_override[SEED25] = {"type": "description", "pricing_description": "Contact sales for pricing."}
    jobs = [{"id": "k", "model": KLING3, "takes": 1, "args": {"prompt": "push", "image_url": "https://a/b.png"}},
            {"id": "s", "model": SEED25, "takes": 2, "args": {"prompt": "drift", "image_url": "https://a/b.png"}}]
    p = write_plan(tmp_path, jobs)
    res = H.cmd_batch(p, budget=10, dry_run=True, yes=True, concurrency=1, out=None, salt="", only=None)
    assert res["ok"] is False and res["unpriced"] == ["s"] and res["estimated_usd"] == pytest.approx(0.5)
    assert H.main(["batch", str(p), "--budget", "10", "--dry-run"]) == 2
    with pytest.raises(SystemExit, match="cannot price s"):
        H.cmd_batch(p, budget=10, dry_run=False, yes=True, concurrency=1, out=None, salt="", only=None)
    assert api.submits == 0


def test_unknown_model_needs_allow_unvalidated(api, tmp_path):
    jobs = [{"id": "x", "model": "vendor/new-video-model", "takes": 1, "args": {"prompt": "x"}}]
    p = write_plan(tmp_path, jobs)
    with pytest.raises(SystemExit, match="no known schema"):
        H.cmd_batch(p, budget=10, dry_run=False, yes=True, concurrency=1, out=None, salt="", only=None)
    res = H.cmd_batch(p, budget=10, dry_run=False, yes=True, concurrency=1, out=None, salt="", only=None,
                      allow_unvalidated=True)
    assert res["completed"] == 1


def test_run_command_refuses_unpriced_and_bad_fields(api):
    api.estimate_override[SEED25] = {"type": "description", "pricing_description": "n/a"}
    with pytest.raises(SystemExit, match="UNPRICED"):
        H.main(["run", SEED25, "--args", json.dumps({"image_url": "https://a/b.png"}), "--yes"])
    with pytest.raises(SystemExit, match="unknown field"):
        H.main(["run", KLING3, "--args", json.dumps({"image_url": "https://a/b.png", "bogus_param": 1}), "--yes"])
    assert api.submits == 0


def test_multishot_estimate_uses_summed_durations(api):
    args = {"prompt": "triptych", "image_url": "https://a/b.png", "multi_shots": True,
            "multi_prompt": [{"prompt": "a", "duration": 3}] * 3}
    e = H.estimate(KLING3, args)                       # mock /estimate says $0.50 for the 5 s default
    assert float(e["usd"]) == pytest.approx(0.9) and e["est_source"] == "multishot-summed"
    assert H.billed_seconds(args) == 9 and H.billed_seconds({"duration": 4}) == 4


WAN_DESC = ("Priced per generated second by resolution: 480p $0.05, 720p $0.10, or 1080p $0.20. "
            "Rates shown are before any applicable customer discount.")
S20_DESC = ("Token-metered pricing. Billable video tokens = ceil(generated video seconds × output width "
            "× output height × 24 fps / 1024). Image and audio references do not count as video input. "
            "Per 1,000 video tokens: 480p/720p/1080p $0.014, 4K $0.008. Rates shown are before any "
            "applicable customer discount.")
CS_DESC = ("Token-metered pricing. Billable video tokens = ceil((input video seconds + generated video seconds) "
           "× output width × output height × 24 fps / 1024). At 480p or 720p, each 1,000 video "
           "tokens cost $0.0214 without video input or $0.01284 with video input (0.6× the standard rate).")


def test_price_formats_wan_and_token_metered():
    assert H.price_from_description(WAN_DESC, {"duration": 5, "resolution": "480p"}) == pytest.approx(0.25)
    assert H.price_from_description(WAN_DESC, {"duration": 5}, default_res="1080p") == pytest.approx(1.0)
    # Seedance 2.0: ceil(5 s x 720x1280 x 24 / 1024) = 108,000 tokens x $0.014/1k
    assert H.price_from_description(S20_DESC, {"duration": 5, "resolution": "720p"}) == pytest.approx(1.512)
    assert H.price_from_description(S20_DESC, {"duration": 5, "resolution": "4k"}) == pytest.approx(7.776)
    assert H.price_from_description(CS_DESC, {"duration": 5, "resolution": "720p"}) == pytest.approx(2.3112)
    # unknowable input seconds / unsupported resolution -> None (refuse), never $0
    assert H.price_from_description(CS_DESC, {"duration": 5, "resolution": "720p", "video_urls": ["v"]}) is None
    assert H.price_from_description(CS_DESC, {"duration": 5, "resolution": "1080p"}) is None
    # token-priced images: references are billed too
    img = "Per 1M tokens: text input $5, image input $8, image output $30."
    assert H.price_from_description(img, {"resolution": "2k", "image_urls": ["a", "b"]}) == pytest.approx(0.34)


def test_wan_estimate_uses_schema_default_resolution(api):
    api.estimate_override["alibaba/wan-3.0/image-to-video"] = {"type": "description", "pricing_description": WAN_DESC}
    e = H.estimate("alibaba/wan-3.0/image-to-video", {"prompt": "x", "image_url": "https://a/b.png", "duration": 4})
    assert float(e["usd"]) == pytest.approx(0.8) and e["est_source"] == "description"   # default 1080p


def test_extract_schemas_from_docs_bundle():
    doc = ("# Thing API\nSource: x\n\n**Endpoint ID:** `vendor/thing`\n\n"
           "<Accordion title=\"Complete JSON schema\">\n  ```json theme={}\n"
           '  {"type": "object", "title": "T", "required": ["prompt"], "properties": '
           '{"prompt": {"type": "string", "description": "d"}}, "additionalProperties": false}\n  ```\n</Accordion>\n'
           "# Other page\nno schema here\n")
    sch = H.extract_schemas(doc)
    assert sch == {"vendor/thing": {"type": "object", "required": ["prompt"],
                                    "properties": {"prompt": {"type": "string"}}}}


def test_shipped_schemas_cover_the_router_models():
    for m in (KLING3, SEED25, QWEN, "marketing-studio/image/flare", "higgsfield-ai/soul/cinema",
              "kling-video/omni/first-last-frame", "bytedance/seedance-2.5/reference-to-video",
              "alibaba/wan-3.0/image-to-video", "higgsfield-ai/soul/v2/image-to-image"):
        assert H.schema_for(m) is not None, m
    assert "last_image_url" in H.schema_for(KLING3)["properties"]


def test_lint_cli(capsys):
    assert H.main(["lint", KLING3, "--args", json.dumps({"image_url": "https://a/b.png"})]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["ok"] and out["defaults_applied"] == {"sound": "off"}
    assert H.main(["lint", KLING3, "--args", json.dumps({"image_url": "https://a/b.png", "end_image_url": "x"})]) == 2
