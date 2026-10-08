import base64, json, sys, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import elevenlabs as E  # noqa: E402


def test_chars_to_words_groups_and_offsets():
    al = {"characters": list("Hi there"), "character_start_times_seconds": [0, .1, .2, .3, .4, .5, .6, .7],
          "character_end_times_seconds": [.1, .2, .3, .4, .5, .6, .7, .8]}
    w = E.chars_to_words(al, offset=1.0)
    assert [x["text"] for x in w] == ["Hi", "there"]
    assert w[0]["start"] == 1.0 and w[1]["end"] == pytest.approx(1.8)


@pytest.fixture
def api(monkeypatch, tmp_path):
    seen = {"posts": 0}

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a): pass

        def _send(self, code, body, ctype="application/json"):
            self.send_response(code); self.send_header("Content-Type", ctype)
            self.send_header("character-cost", "7")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

        def do_POST(self):
            seen["key"] = self.headers.get("xi-api-key")
            seen["posts"] += 1
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            seen[self.path.split("?")[0]] = body
            if "with-timestamps" in self.path:
                al = {"characters": list("Go now"), "character_start_times_seconds": [0, .1, .2, .3, .4, .5],
                      "character_end_times_seconds": [.1, .2, .3, .4, .5, .6]}
                return self._send(200, json.dumps({"audio_base64": base64.b64encode(b"ID3fake").decode(),
                                                   "alignment": al}).encode())
            return self._send(200, b"ID3audio", "audio/mpeg")
    srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    monkeypatch.setattr(E, "API", f"http://127.0.0.1:{srv.server_port}")
    monkeypatch.setenv("ELEVENLABS_API_KEY", "k123")
    monkeypatch.setenv("ELEVEN_CACHE_DIR", str(tmp_path / "cache"))
    yield seen
    srv.shutdown()


def test_tts_writes_audio_and_words(api, tmp_path):
    r = E.tts("Go now", "voiceX", tmp_path / "vo.mp3")
    assert (tmp_path / "vo.mp3").read_bytes() == b"ID3fake"
    words = json.loads((tmp_path / "vo.words.json").read_text())["words"]
    assert [w["text"] for w in words] == ["Go", "now"] and r["duration"] == pytest.approx(0.6)
    body = api["/v1/text-to-speech/voiceX/with-timestamps"]
    assert api["key"] == "k123" and body["model_id"] == "eleven_v4"          # v4 is the default (audit C10)
    assert "style" not in body["voice_settings"] and "speed" not in body["voice_settings"]
    assert r["credits_billed"] == 7 and r["est_credits"] == 6 and r["cached"] is False


def test_sfx_and_music(api, tmp_path):
    E.sfx("can pop", 1.5, tmp_path / "pop.mp3")
    E.music("warm lo-fi", 12, tmp_path / "bed.mp3")
    assert api["/v1/sound-generation"]["duration_seconds"] == 1.5
    assert api["/v1/music"]["music_length_ms"] == 12000 and api["/v1/music"]["force_instrumental"]


def test_proxy_mode_and_missing_key(monkeypatch):
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    monkeypatch.setenv("ELEVEN_AUTH_VIA_PROXY", "1")
    assert "xi-api-key" not in E._headers(True)
    monkeypatch.delenv("ELEVEN_AUTH_VIA_PROXY")
    with pytest.raises(SystemExit):
        E._headers(True)


def test_audio_tags_are_not_caption_words():
    text = "[sighs] Hi [short pause] there"
    al = {"characters": list(text), "character_start_times_seconds": [i * .1 for i in range(len(text))],
          "character_end_times_seconds": [i * .1 + .1 for i in range(len(text))]}
    assert [w["text"] for w in E.chars_to_words(al)] == ["Hi", "there"]



# ───────────── v4 default, estimate, per-call cap, content-hash cache ─────────────

def test_v3_keeps_style_and_v4_warns_on_style(capsys):
    b3 = E.tts_body("Hi", "eleven_v3")
    assert b3["voice_settings"]["style"] == 0.3 and b3["voice_settings"]["speed"] == 1.0
    b4 = E.tts_body("Hi", "eleven_v4", style=0.5)
    assert "ignores style" in capsys.readouterr().err
    assert b4["voice_settings"]["style"] == 0.5          # sent as asked, but warned


def test_estimates():
    assert E.estimate("tts", E.tts_body("x" * 100, "eleven_v4"))["credits"] == 100
    assert E.estimate("tts", E.tts_body("x" * 100, "eleven_v4_turbo"))["credits"] == 50
    assert E.estimate("sfx", E.sfx_body("boom", 2.5))["credits"] == 100
    assert E.estimate("sfx", E.sfx_body("boom", None))["credits"] == 1200      # unset -> assume 30 s
    plan = {"chunks": [{"duration_ms": 3000}, {"duration_ms": 14000}, {"duration_ms": 3000}]}
    assert E.estimate("music", E.music_body(None, None, plan=plan))["credits"] == 1000
    e = E.estimate("music", E.music_body("warm", 12))
    assert e["credits"] == 600 and e["usd"] == pytest.approx(600 * E.usd_per_credit())
    with pytest.raises(SystemExit):
        E.estimate("music", E.music_body(None, None, plan={"chunks": []}))


def test_cache_key_hashes_only_output_defining_fields():
    a = E.cache_key("tts/v1", E.tts_body("Go now", "eleven_v4"))
    assert a == E.cache_key("tts/v1", E.tts_body("Go now", "eleven_v4")) and a.startswith("sha256:")
    assert a != E.cache_key("tts/v2", E.tts_body("Go now", "eleven_v4"))
    assert a != E.cache_key("tts/v1", E.tts_body("Go now!", "eleven_v4"))
    assert a != E.cache_key("tts/v1", E.tts_body("Go now", "eleven_v3"))
    assert a != E.cache_key("tts/v1", E.tts_body("Go now", "eleven_v4"), output_format="pcm_44100")


def test_identical_requests_do_not_pay_twice(api, tmp_path):
    r1 = E.tts("Go now", "voiceX", tmp_path / "a" / "vo.mp3")
    r2 = E.tts("Go now", "voiceX", tmp_path / "b" / "other_name.mp3")     # output path is not in the key
    assert api["posts"] == 1 and r2["cached"] and r2["cache_key"] == r1["cache_key"]
    assert (tmp_path / "b" / "other_name.mp3").read_bytes() == b"ID3fake"
    words = json.loads((tmp_path / "b" / "other_name.words.json").read_text())["words"]
    assert [w["text"] for w in words] == ["Go", "now"]
    E.tts("Go later", "voiceX", tmp_path / "c.mp3")
    assert api["posts"] == 2
    E.sfx("can pop", 1.5, tmp_path / "p1.mp3"); E.sfx("can pop", 1.5, tmp_path / "p2.mp3")
    E.music("warm", 12, tmp_path / "m1.mp3"); E.music("warm", 12, tmp_path / "m2.mp3")
    assert api["posts"] == 4
    E.sfx("can pop", 1.5, tmp_path / "p3.mp3", cache_dir=False)              # --no-cache really calls
    assert api["posts"] == 5


def test_per_call_cap_refuses_before_calling(api, tmp_path):
    with pytest.raises(SystemExit, match="per-call cap"):
        E.tts("x" * 500, "voiceX", tmp_path / "vo.mp3", max_credits=100)
    with pytest.raises(SystemExit, match="per-call cap"):
        E.music("long bed", 60, tmp_path / "bed.mp3", max_credits=1000)
    assert api["posts"] == 0
    # a cached result is free, so the cap does not block it
    E.tts("Go now", "voiceX", tmp_path / "vo.mp3")
    E.tts("Go now", "voiceX", tmp_path / "vo2.mp3", max_credits=0)
    assert api["posts"] == 1


def test_cli_estimate_makes_no_call(api, tmp_path, capsys):
    assert E.main(["sfx", "whoosh", "--seconds", "2", "--out", str(tmp_path / "w.mp3"), "--estimate"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["credits"] == 80 and out["cached"] is False and api["posts"] == 0
