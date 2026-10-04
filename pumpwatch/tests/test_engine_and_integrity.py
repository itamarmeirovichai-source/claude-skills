import json
import subprocess
import sys
from pathlib import Path

from helpers import dataset, flat_bars, promo_posts, with_spike

from pumpwatch.audit import AuditLog, config_fingerprint
from pumpwatch.backtest import Case, calibrate_and_test, evaluate, split_cases
from pumpwatch.config import Config
from pumpwatch.engine import Engine, available_signals
from pumpwatch.io import load_dir, save_dir
from pumpwatch.models import Alert, Dataset, Filing
from pumpwatch.synth import SynthSpec, generate


# --- convergence ---------------------------------------------------------
def test_single_family_never_alerts():
    bars = with_spike(flat_bars("ABC", 80), 70, vol_mult=200)
    runs = Engine(Config(alert_threshold=1)).run(dataset(bars))
    assert runs["ABC"].alerts == []


def test_market_plus_social_alerts_with_reasons():
    bars = with_spike(flat_bars("ABC", 80), 70, vol_mult=40)
    runs = Engine().run(dataset(bars, posts=promo_posts("ABC", bars[70].day, 8)))
    alerts = runs["ABC"].alerts
    assert len(alerts) == 1
    a = alerts[0]
    assert set(a.families) == {"market", "social"}
    assert any("S1_abnormal_volume" in r for r in a.reasons)
    assert any("S5_coordinated_promotion" in r for r in a.reasons)


def test_real_news_move_is_not_flagged():
    bars = with_spike(flat_bars("ABC", 80), 70, vol_mult=40, price_mult=2)
    news = Filing("ABC", bars[70].day, "8-K", "FDA approval")
    runs = Engine().run(dataset(bars, [news], promo_posts("ABC", bars[70].day, 2)))
    assert runs["ABC"].alerts == []


def test_renormalisation_ignores_missing_sources():
    bars = flat_bars("ABC", 10)
    assert available_signals(dataset(bars)) == {"S1_abnormal_volume", "S2_quiet_accumulation"}


def test_cooldown_suppresses_repeat_alerts():
    bars = flat_bars("ABC", 90)
    for i in range(70, 75):
        bars = with_spike(bars, i, vol_mult=40)
    posts = [p for i in range(70, 75) for p in promo_posts("ABC", bars[i].day, 6)]
    alerts = Engine().run(dataset(bars, posts=posts))["ABC"].alerts
    assert len(alerts) == 1


# --- no look-ahead -------------------------------------------------------
def test_scores_do_not_depend_on_future_data():
    data, _ = generate(SynthSpec(n_pump=3, n_legit=3, n_noise=2, days=200, seed=3))
    cut = sorted({b.day for b in data.bars})[150]
    past = Dataset(
        bars=[b for b in data.bars if b.day <= cut],
        filings=[f for f in data.filings if f.day <= cut],
        posts=[p for p in data.posts if p.day <= cut],
    )
    # Source availability must match, otherwise renormalisation differs for reasons unrelated to look-ahead.
    if not past.filings:
        past.filings = [Filing("ZZZZ", cut, "10-K")]
        data.filings.append(Filing("ZZZZ", cut, "10-K"))
    full = Engine().run(data)
    part = Engine().run(past)
    for t, run in part.items():
        a = {s.day: s.score for s in run.scores}
        b = {s.day: s.score for s in full[t].scores if s.day <= cut}
        assert a == b, t


# --- backtest ------------------------------------------------------------
def _alert(t, d, score=50.0):
    return Alert(t, d, score, ("market", "social"), ())


def test_evaluate_counts_only_alerts_before_collapse():
    from datetime import date

    c = Case("ABC", "pump", date(2025, 3, 10), date(2025, 3, 20))
    late = evaluate({"ABC": [_alert("ABC", date(2025, 3, 21))]}, [c], 40)
    assert late.caught == 0 and late.false_alerts == 1
    early = evaluate({"ABC": [_alert("ABC", date(2025, 3, 15))]}, [c], 40)
    assert early.caught == 1 and early.lead_days == [5] and early.false_alerts == 0


def test_evaluate_counts_legit_and_background_alerts_as_false():
    from datetime import date

    legit = Case("GOOD", "legit", date(2025, 3, 10), date(2025, 3, 20))
    m = evaluate({"GOOD": [_alert("GOOD", date(2025, 3, 11))], "NOISE": [_alert("NOISE", date(2025, 1, 1))]}, [legit], 40)
    assert m.legit_flagged == 1 and m.false_alerts == 2


def test_split_is_deterministic_and_disjoint():
    data, cases = generate(SynthSpec(n_pump=6, n_legit=6, n_noise=0, days=200))
    a1, b1 = split_cases(cases)
    a2, b2 = split_cases(list(reversed(cases)))
    assert [c.ticker for c in a1] == [c.ticker for c in a2]
    assert not {c.ticker for c in a1} & {c.ticker for c in b1}


def test_synthetic_pipeline_end_to_end():
    data, cases = generate(SynthSpec(n_pump=8, n_legit=8, n_noise=8, days=220))
    eng = Engine()
    rep = calibrate_and_test(eng, eng.run(data), cases)
    assert rep.holdout.pumps == 4 and rep.holdout.legit == 4
    assert rep.overall.recall >= 0.5  # plumbing check only, not a performance claim


# --- audit log -----------------------------------------------------------
def test_audit_log_detects_tampering(tmp_path: Path):
    from datetime import date

    log = AuditLog(tmp_path / "audit.jsonl")
    fp = config_fingerprint(Config())
    for i in range(3):
        log.append(_alert("ABC", date(2025, 1, 1 + i)), "test", fp)
    assert log.verify().ok and log.verify().records == 3
    lines = log.path.read_text().splitlines()
    rec = json.loads(lines[1])
    rec["alert"]["score"] = 1.0
    lines[1] = json.dumps(rec)
    log.path.write_text("\n".join(lines) + "\n")
    res = log.verify()
    assert not res.ok and res.broken_at == 2


def test_audit_log_detects_deleted_record(tmp_path: Path):
    from datetime import date

    log = AuditLog(tmp_path / "audit.jsonl")
    for i in range(3):
        log.append(_alert("ABC", date(2025, 1, 1 + i)), "test", "x")
    lines = log.path.read_text().splitlines()
    log.path.write_text("\n".join([lines[0], lines[2]]) + "\n")
    assert not log.verify().ok


# --- io + cli ------------------------------------------------------------
def test_io_roundtrip(tmp_path: Path):
    data, cases = generate(SynthSpec(n_pump=2, n_legit=2, n_noise=1, days=200))
    save_dir(data, tmp_path)
    back = load_dir(tmp_path)
    assert len(back.bars) == len(data.bars)
    assert len(back.filings) == len(data.filings)
    assert len(back.posts) == len(data.posts)


def test_cli_demo_and_verify(tmp_path: Path):
    src = Path(__file__).resolve().parents[1] / "src"
    env = {"PYTHONPATH": str(src)}
    out = tmp_path / "demo"
    r = subprocess.run([sys.executable, "-m", "pumpwatch", "demo", "--out", str(out)], capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    assert "SYNTHETIC" in (out / "report.md").read_text()
    log = tmp_path / "audit.jsonl"
    r = subprocess.run([sys.executable, "-m", "pumpwatch", "scan", str(out / "data"), "--log", str(log)], capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    r = subprocess.run([sys.executable, "-m", "pumpwatch", "verify-log", str(log)], capture_output=True, text=True, env=env)
    assert r.returncode == 0 and "intact" in r.stdout
