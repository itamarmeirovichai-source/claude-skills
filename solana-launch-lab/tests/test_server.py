"""The local HTTP API end to end, on an ephemeral loopback port."""

import dataclasses
import json
import threading
import urllib.error
import urllib.request

import pytest

from launchlab import db
from launchlab.server import App, make_server


@pytest.fixture
def api(settings):
    app = App(dataclasses.replace(settings, host="127.0.0.1"), conn=db.connect(":memory:"))
    app.reset_demo(seed=3, n_tokens=30)
    server = make_server(app, port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"

    def call(path, body=None, headers=None, raw=False):
        req = urllib.request.Request(base + path, data=None if body is None else json.dumps(body).encode(),
                                     headers={**({"Content-Type": "application/json"} if body is not None else {}), **(headers or {})},
                                     method="GET" if body is None else "POST")
        try:
            with urllib.request.urlopen(req, timeout=10) as res:
                payload = res.read()
                return res.status, (payload if raw else json.loads(payload)), dict(res.headers)
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read() or b"{}"), dict(exc.headers)

    yield call
    server.shutdown()
    server.server_close()


def test_status_and_static_assets(api):
    status, body, headers = api("/api/status")
    assert status == 200 and body["mode"] == "demo" and body["live_enabled"] is False
    assert body["counts"]["tokens_synthetic"] == 30 and body["counts"]["tokens_live"] == 0
    assert body["event_log"]["ok"] is True and "No wallet is connected" in body["notice"]
    assert headers["Cache-Control"] == "no-store" and "default-src 'self'" in headers["Content-Security-Policy"]
    for path, needle in (("/", b"Solana Launch Lab"), ("/app.js", b"textContent"), ("/styles.css", b"synthetic-banner")):
        status, raw, _ = api(path, raw=True)
        assert status == 200 and needle in raw
    assert api("/../../etc/passwd")[0] == 404 and api("/static/../config.py")[0] == 404 and api("/api/nope")[0] == 404


def test_every_demo_row_is_flagged_synthetic_and_search_is_exact(api):
    _, body, _ = api("/api/tokens")
    assert len(body["tokens"]) == 30 and all(t["is_synthetic"] and t["mint"].startswith("SYNTH") for t in body["tokens"])
    mint = body["tokens"][0]["mint"]
    assert [t["mint"] for t in api(f"/api/tokens?q={mint}")[1]["tokens"]] == [mint]
    assert api(f"/api/tokens?q={body['tokens'][0]['symbol']}")[1]["tokens"] == []        # a ticker never matches
    assert api(f"/api/tokens?q={mint[:10]}")[1]["tokens"] == []                           # nor a prefix
    assert api("/api/tokens?scope=live")[1]["tokens"] == []
    status, detail, _ = api(f"/api/token?mint={mint}")
    assert status == 200 and detail["token"]["is_synthetic"] and detail["risk"]["is_synthetic"]
    assert all(o["is_synthetic"] and o["provider"] == "synthetic" for o in detail["market"])
    assert all(o["payload"]["fdv_definition"] and "market_cap_definition" in o["payload"] for o in detail["market"])
    assert len(detail["risk"]["components"]) == 8 and "Not a buy signal" in detail["risk"]["disclaimer"]
    assert api("/api/token?mint=BTC")[0] == 400
    assert api("/api/token?mint=CUfphqswgDK3VP3FX7CiShVCTdGQneFusYRFViABpump")[0] == 404


def test_replay_shows_only_what_was_known(api):
    mint = api("/api/tokens")[1]["tokens"][0]["mint"]
    full = api(f"/api/token?mint={mint}")[1]
    cut = full["time_range"]["first"] + 30
    early = api(f"/api/token?mint={mint}&as_of={cut}")[1]
    assert early["as_of"] == cut and all(o["observed_at"] <= cut for o in early["market"])
    assert early["risk"]["as_of"] == cut
    assert max(o["observed_at"] for o in full["market"]) > cut


def test_paper_book_lists_every_signal_including_rejections(api):
    _, book, _ = api("/api/paper?book=demo")
    m = book["metrics"]
    assert book["uses_synthetic_tokens"] and len(book["ledger"]) == m["signals"] == 30
    assert sum(r["decision"] == "rejected" for r in book["ledger"]) == m["rejected"] > 0
    assert m["verdict"] == "mechanics demo"
    _, live, _ = api("/api/paper?book=live")
    assert live["metrics"]["verdict"] == "inconclusive" and live["ledger"] == [] and not live["uses_synthetic_tokens"]
    assert api("/api/paper?book=secret")[0] == 404
    status, run, _ = api("/api/paper/run", {"book": "demo"})
    assert status == 200 and run["new_signals"] == 0                                      # idempotent


def test_live_actions_are_refused_in_demo_mode(api):
    for path, body in (("/api/ingest", {"mint": "CUfphqswgDK3VP3FX7CiShVCTdGQneFusYRFViABpump"}), ("/api/discover", {}),
                       ("/api/audit", {"mint": "CUfphqswgDK3VP3FX7CiShVCTdGQneFusYRFViABpump", "alert_time": "2026-11-20T20:52:00Z"})):
        status, out, _ = api(path, body)
        assert status == 503 and out["kind"] == "disabled"
    assert api("/api/ingest", {"mint": "BTC"})[0] == 400
    assert api("/api/status")[1]["counts"]["tokens_live"] == 0


def test_request_guards(api):
    assert api("/api/status", headers={"Host": "evil.example"})[0] == 403                 # DNS rebinding
    assert api("/api/demo/reset", {}, headers={"Origin": "https://evil.example"})[0] == 403   # cross-site POST
    assert api("/api/demo/reset", {}, headers={"Content-Type": "text/plain"})[0] == 415
    assert api("/api/paper/run", [1, 2, 3])[0] == 400
    assert api("/api/nothing", {})[0] == 404
    status, out, _ = api("/api/demo/reset", {"seed": 4, "n_tokens": 12})
    assert status == 200 and out["seeded"]["n_tokens"] == 12
    assert api("/api/events?limit=5")[1]["chain"]["ok"] is True
