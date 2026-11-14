import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import director as D  # noqa: E402

MX = D.load_matrix()


def test_matrix_ids_unique_and_rules_reference_real_ids():
    all_ids = {o["id"] for d in D.DIMS for o in MX[d]}
    for a, b in MX["_rules"]["incompatible"]:
        assert a in all_ids and b in all_ids


def test_roll_is_deterministic_distinct_and_compatible():
    a = D.roll(MX, 6, "acme", [], seed=7)
    b = D.roll(MX, 6, "acme", [], seed=7)
    assert a == b
    keys = {tuple(s[d] for d in D.DIMS) for s in a}
    assert len(keys) == 6
    rules = MX["_rules"]["incompatible"]
    assert not any(D._incompatible(s, rules) for s in a)
    # the idea skeleton (mechanism+format) never repeats inside one roll
    assert len({(s["mechanism"], s["format"]) for s in a}) == 6


def test_roll_avoids_client_history():
    first = D.roll(MX, 3, "acme", [], seed=1)
    ledger = [{"client": "Acme", "seed": s} for s in first]
    second = D.roll(MX, 3, "acme", ledger, seed=1)
    used = {(s["mechanism"], s["format"]) for s in first}
    assert not used & {(s["mechanism"], s["format"]) for s in second}
    used_formats = {s["format"] for s in first}
    assert not used_formats & {s["format"] for s in second}


def test_other_clients_history_matters_less():
    first = D.roll(MX, 1, "acme", [], seed=3)[0]
    led = [{"client": "acme", "seed": first}]
    own = D.novelty_penalty(first, led, "acme")
    other = D.novelty_penalty(first, led, "zeta")
    assert own > other > 0


def test_lock_respected_and_bad_lock_rejected():
    seeds = D.roll(MX, 3, None, [], seed=2, locks={"format": "heist"})
    assert all(s["format"] == "heist" for s in seeds)
    with pytest.raises(ValueError):
        D.roll(MX, 1, None, [], locks={"format": "nope"})


def base_m(**kw):
    m = {"width": 1080, "height": 1920, "fps": 30.0, "vcodec": "h264", "acodec": "aac",
         "duration": 15.0, "lufs": -14.2, "true_peak": -1.5, "silence_at_start": 0.0,
         "cuts": [1.2, 3.0, 5.1, 7.0, 9.5, 12.0], "black": [], "freeze": [], "flicker": []}
    m.update(kw)
    return m


def levels(findings, check):
    return [f["level"] for f in findings if f["check"] == check]


def test_evaluate_clean_master_passes():
    F = D.evaluate(base_m(), "reels", 15)
    assert not [f for f in F if f["level"] in ("FAIL", "WARN")]


def test_evaluate_flags_common_problems():
    F = D.evaluate(base_m(width=720, height=1280, lufs=-20.0, true_peak=0.2, cuts=[4.2],
                          silence_at_start=1.4, black=[[0.0, 0.4]], product_match=[{"t": 3, "score": 0.2}]),
                   "reels", 15)
    assert levels(F, "resolution") == ["WARN"]          # right aspect, low res
    assert levels(F, "loudness") == ["WARN"]
    assert levels(F, "true_peak") == ["WARN"]
    assert levels(F, "audio_hook") == ["WARN"]
    assert levels(F, "hook_pacing") == ["WARN"]
    assert levels(F, "shot_length") == ["WARN"]
    assert levels(F, "black_frames") == ["FAIL"]
    assert levels(F, "product_colour") == ["FAIL"]


def test_evaluate_wrong_aspect_and_duration_fail():
    F = D.evaluate(base_m(width=1920, height=1080, duration=21.0), "reels", 15)
    assert levels(F, "resolution") == ["FAIL"]
    assert levels(F, "duration") == ["FAIL"]


def test_one_take_and_end_card_not_penalised():
    F = D.evaluate(base_m(cuts=[], one_take=True, freeze=[[13.2, 15.0]]), "reels", 15)
    assert levels(F, "hook_pacing") == ["PASS"]
    assert not levels(F, "shot_length")
    assert levels(F, "end_card") == ["INFO"]
    F2 = D.evaluate(base_m(freeze=[[4.0, 6.0]]), "reels", 15)
    assert levels(F2, "frozen") == ["WARN"]


def test_new_job_scaffold(tmp_path):
    written = D.cmd_new(tmp_path / "job", "Driftline Citrus", "spec")
    names = {p.name for p in written}
    assert {"01-brief.md", "04-shots.csv", "06-qc.md"} <= names
    assert "Driftline Citrus" in (tmp_path / "job" / "01-brief.md").read_text()
    assert D.cmd_new(tmp_path / "job", "x", "y") == []   # never overwrites


def test_bench_matrix_and_summary(tmp_path):
    (p,) = D.cmd_bench(tmp_path, ["kling", "veo"])
    rows = list(__import__("csv").DictReader(open(p)))
    assert len(rows) == len(D.BENCH_TESTS) * 2 * 2
    for r in rows:
        if r["test"] == "T01":
            good = r["model"] == "veo"
            for c in ("prompt_adherence", "product_fidelity", "artifacts", "motion_physics", "aesthetic"):
                r[c] = "5" if good else "3"
            r["cost_usd"] = "1"
    with open(p, "w", newline="") as f:
        w = __import__("csv").DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    res = D.summarize_bench(p)
    assert res["T01"][0]["model"] == "veo"


def test_cli_dice_log_history(tmp_path):
    led = tmp_path / "l.jsonl"
    S = str(Path(D.__file__))
    out = subprocess.run([sys.executable, S, "--ledger", str(led), "dice", "--client", "A", "-n", "2",
                          "--seed", "4", "--json"], capture_output=True, text=True, check=True).stdout
    seed = json.loads(out)[0]
    subprocess.run([sys.executable, S, "--ledger", str(led), "log", "--client", "A", "--title", "T",
                    "--seed-json", json.dumps(seed)], check=True, capture_output=True)
    h = subprocess.run([sys.executable, S, "--ledger", str(led), "history", "--client", "a"],
                       capture_output=True, text=True, check=True).stdout
    assert seed["format"] in h


@pytest.mark.skipif(not __import__("shutil").which("ffmpeg"), reason="ffmpeg missing")
def test_qc_on_synthetic_clip(tmp_path):
    v = tmp_path / "v.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=1080x1920:r=30:d=4",
                    "-f", "lavfi", "-i", "sine=f=440:d=4", "-shortest", "-c:v", "libx264", "-pix_fmt",
                    "yuv420p", "-c:a", "aac", str(v)], check=True)
    rep = D.cmd_qc(str(v), None, 4.0, "reels", tmp_path / "qc")
    assert rep["measurements"]["width"] == 1080
    assert (tmp_path / "qc" / "qc_sheet.jpg").exists()
    assert (tmp_path / "qc" / "qc_report.md").exists()


def test_predict_and_rank():
    viral = {"hook": 5, "curiosity": 4, "emotion": 5, "novelty": 5, "rewatch": 4, "identity": 5,
             "comment_bait": 4, "utility": 1, "product_desire": 3, "offer_clarity": 2, "brand_early": 2, "trust": 2}
    seller = {"hook": 3, "curiosity": 3, "emotion": 2, "novelty": 2, "rewatch": 2, "identity": 2,
              "comment_bait": 1, "utility": 3, "product_desire": 5, "offer_clarity": 5, "brand_early": 5, "trust": 5}
    cs = [{"title": "viral", "drivers": viral}, {"title": "seller", "drivers": seller}]
    assert D.rank(cs, "awareness")[0]["title"] == "viral"
    assert D.rank(cs, "conversion")[0]["title"] == "seller"
    assert D.predict({**viral, "ai_backlash": 5})["shares"] < D.predict(viral)["shares"]
    assert all(0 <= v <= 100 for v in D.predict(viral).values())
    with pytest.raises(ValueError):
        D.predict({"virality": 5})
