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
def api(monkeypatch):
    seen = {}

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a): pass

        def _send(self, code, body, ctype="application/json"):
            self.send_response(code); self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

        def do_POST(self):
            seen["key"] = self.headers.get("xi-api-key")
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
    yield seen
    srv.shutdown()


def test_tts_writes_audio_and_words(api, tmp_path):
    r = E.tts("Go now", "voiceX", tmp_path / "vo.mp3")
    assert (tmp_path / "vo.mp3").read_bytes() == b"ID3fake"
    words = json.loads((tmp_path / "vo.words.json").read_text())["words"]
    assert [w["text"] for w in words] == ["Go", "now"] and r["duration"] == pytest.approx(0.6)
    assert api["key"] == "k123" and api["/v1/text-to-speech/voiceX/with-timestamps"]["model_id"] == "eleven_v3"


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
