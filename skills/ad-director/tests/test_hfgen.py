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
                usd = "0.50" if "video" in self.path else "0.02"
                return self._json(200, {"credits": "8", "usd": usd})
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
    jobs = [{"id": "bad", "model": "kling-video/x/text-to-video", "takes": 1, "args": {"prompt": "FAIL"}}]
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
