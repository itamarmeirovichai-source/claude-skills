"""Storage, event log, configuration, synthetic generator and the claim-check analysis."""

import pytest
from conftest import FakeClock, FakeTransport

from launchlab import audit, db, paper
from launchlab.config import is_synthetic_mint, is_valid_mint, load_settings, redact_url
from launchlab.providers import synthetic
from launchlab.providers.base import HttpClient


def test_event_log_chain_detects_edits_and_deletions(conn):
    for i in range(5):
        db.log_event(conn, "test", {"i": i}, ts=1000.0 + i)
    assert db.verify_event_chain(conn) == {"ok": True, "count": 5, "first_bad_id": None}
    conn.execute("UPDATE events SET payload = ? WHERE id = 3", ('{"i":99}',))
    assert db.verify_event_chain(conn)["ok"] is False and db.verify_event_chain(conn)["first_bad_id"] == 3
    conn.execute("UPDATE events SET payload = ? WHERE id = 3", ('{"i":2}',))
    assert db.verify_event_chain(conn)["ok"] is True
    conn.execute("DELETE FROM events WHERE id = 2")
    assert db.verify_event_chain(conn)["first_bad_id"] == 3


def test_upsert_never_overwrites_a_known_value_with_nothing(conn):
    db.upsert_token(conn, "m", is_synthetic=False, now=1.0, symbol="AAA", launch_time=10.0)
    db.upsert_token(conn, "m", is_synthetic=False, now=2.0, symbol=None, launch_time=None, name="Name")
    db.upsert_token(conn, "m", is_synthetic=False, now=3.0, symbol="BBB")
    row = dict(conn.execute("SELECT * FROM tokens").fetchone())
    assert (row["symbol"], row["launch_time"], row["name"], row["first_seen_at"]) == ("AAA", 10.0, "Name", 1.0)
    with pytest.raises(KeyError):
        db.upsert_token(conn, "m", is_synthetic=False, is_admin=1)


def test_observation_query_respects_as_of_and_after(conn):
    for t in (10.0, 20.0, 30.0):
        db.add_observation(conn, "m", "market", "p", t, {"price_sol": t}, is_synthetic=True, missing=["x"] if t == 20 else [])
    assert [o["observed_at"] for o in db.observations(conn, "m", as_of=20.0)] == [10.0, 20.0]   # inclusive
    assert [o["observed_at"] for o in db.observations(conn, "m", after=20.0)] == [30.0]
    assert db.observations(conn, "m", as_of=20.0)[-1]["missing"] == ["x"]


def test_settings_are_local_only_and_never_expose_the_rpc_url(tmp_path):
    s = load_settings(env={}, dotenv_path=tmp_path / "none")
    assert s.mode == "demo" and not s.live_enabled and s.host == "127.0.0.1"
    assert s.store_raw == {"solana_rpc": True, "dexscreener": False, "geckoterminal": False}
    with pytest.raises(ValueError):
        load_settings(env={"LAUNCHLAB_HOST": "0.0.0.0"}, dotenv_path=tmp_path / "none")
    with pytest.raises(ValueError):
        load_settings(env={"LAUNCHLAB_MODE": "trade"}, dotenv_path=tmp_path / "none")
    with pytest.raises(ValueError):
        load_settings(env={"PAPER_FAIL_PROB": "1.5"}, dotenv_path=tmp_path / "none")
    secret = "https://rpc.example.com/v1/abcdef0123456789?api-key=SECRETSECRET"
    s = load_settings(env={"SOLANA_RPC_URL": secret, "LAUNCHLAB_MODE": "live"}, dotenv_path=tmp_path / "none")
    shown = str(s.public_dict())
    assert "SECRET" not in shown and "abcdef" not in shown and "rpc.example.com" in shown
    assert redact_url("https://api.mainnet-beta.solana.com") == "https://api.mainnet-beta.solana.com"
    (tmp_path / ".env").write_text("# comment\nLAUNCHLAB_PORT=9999\nPAPER_SIZE_SOL=0.25\n")
    s = load_settings(env={}, dotenv_path=tmp_path / ".env")
    assert s.port == 9999 and s.paper.size_sol == 0.25
    assert s.config_hash() != load_settings(env={}, dotenv_path=tmp_path / "none").config_hash()


def test_mint_validation():
    assert is_valid_mint("CUfphqswgDK3VP3FX7CiShVCTdGQneFusYRFViABpump")
    for bad in ("BTC", "", "0OIl" * 10, "CUfphqswgDK3VP3FX7CiShVCTdGQneFusYRFViABpump\n", "a" * 50):
        assert not is_valid_mint(bad)


def test_synthetic_data_is_deterministic_labelled_and_cannot_pass_as_real(conn, settings):
    cfg = synthetic.SyntheticConfig(n_tokens=40, seed=11)
    first = synthetic.seed_database(conn, cfg)
    rows = conn.execute("SELECT mint, is_synthetic, launch_source, name FROM tokens").fetchall()
    assert len(rows) == 40 and all(r["is_synthetic"] == 1 for r in rows)
    assert all(is_synthetic_mint(r["mint"]) and not is_valid_mint(r["mint"]) for r in rows)   # impossible as a Solana address
    assert all("synthetic" in r["launch_source"] and r["name"].startswith("Synthetic") for r in rows)
    assert conn.execute("SELECT COUNT(*) FROM observations WHERE is_synthetic = 0").fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(DISTINCT provider) FROM observations").fetchone()[0] == 1
    snapshot = conn.execute("SELECT mint, observed_at, payload FROM observations ORDER BY id").fetchall()
    again = synthetic.seed_database(conn, cfg)                               # same seed -> identical universe
    assert first == again
    assert [tuple(r) for r in conn.execute("SELECT mint, observed_at, payload FROM observations ORDER BY id")] == [tuple(r) for r in snapshot]
    synthetic.seed_database(conn, synthetic.SyntheticConfig(n_tokens=40, seed=12))                # a different seed -> different data
    reseeded = [r["payload"] for r in conn.execute("SELECT payload FROM observations ORDER BY id LIMIT 50")]
    assert reseeded != [r["payload"] for r in snapshot[:50]]


def test_demo_outcomes_are_not_scripted_winners(conn, settings):
    synthetic.seed_database(conn, synthetic.SyntheticConfig(n_tokens=120, seed=5))
    paper.run_book(conn, settings, "demo", synthetic=True)
    m = paper.book_metrics(conn, "demo", settings)
    assert m["signals"] == 120 and m["rejected"] > 0 and m["candidates"] > 0
    assert m["is_synthetic"] and m["verdict"] == "mechanics demo" and "not evidence" in m["verdict_note"]
    losers = sum(b["count"] for b in m["distribution"][:4])
    assert losers > 0                                                         # the ledger shows losses, not only wins
    assert conn.execute("SELECT COUNT(*) FROM signals").fetchone()[0] == conn.execute("SELECT COUNT(*) FROM tokens").fetchone()[0]


def candles_bart():
    # shaped like the audited BartCoin minutes (price = cap / 1e9): alert minute opens at $491,715
    t0 = audit.parse_utc("2026-11-20T20:52:00Z")
    rows = [(t0 - 60, 429_614, 493_590, 395_370, 491_715), (t0, 491_715, 576_754, 441_836, 554_918),
            (t0 + 60, 554_918, 617_527, 483_729, 587_830), (t0 + 2880, 1_800_000, 2_035_864, 1_700_000, 1_856_881),
            (t0 + 6000, 110_000, 120_000, 90_000, 101_908)]
    return [{"t": float(t), "o": o / 1e9, "h": h / 1e9, "l": low / 1e9, "c": c / 1e9, "v": 1.0} for t, o, h, low, c in rows]


def test_claim_check_reproduces_the_audit_arithmetic():
    alert = audit.parse_utc("2026-11-20T20:52:00Z")
    r = audit.analyse_candles(candles_bart(), alert, claimed_cap_usd=58_000, claimed_multiple=24)
    assert r["status"] == "ok" and r["alert_minute"] == "2026-11-20 20:52:00 UTC"
    assert r["alert_candle_cap_usd"]["open"] == pytest.approx(491_715)
    assert r["peak_after_alert"]["cap_usd"] == pytest.approx(2_035_864) and r["peak_after_alert"]["minutes_after_alert"] == 48
    assert r["best_case_multiple_from_alert_open"] == pytest.approx(2_035_864 / 491_715)      # 4.14x, not 24x
    assert r["claim_reproducible_from_alert_time"] is False
    assert r["observed_over_claimed_cap"] == pytest.approx(491_715 / 58_000)                   # 8.5x the claimed cap
    assert r["claimed_cap_seen_in_alert_minute"] is False
    assert r["peak_over_claimed_cap"] == pytest.approx(2_035_864 / 58_000)
    assert r["minutes_closing_at_or_above"]["10x"] == 0
    assert "upper bound" in r["caveats"][0] and "FDV" in r["cap_definition"]
    assert audit.analyse_candles(candles_bart(), alert + 86_400)["status"] == "no_data"         # never extrapolates
    assert audit.analyse_candles([], alert)["status"] == "no_data"


def test_claim_check_uses_the_exact_mint_and_times_are_utc():
    assert audit.parse_utc("2026-11-20T20:52:00Z") == audit.parse_utc("2026-11-20 20:52:00") == audit.parse_utc("2026-11-20T22:52:00+02:00")
    with pytest.raises(ValueError):
        audit.parse_utc("yesterday")
    clock = FakeClock()
    gecko = HttpClient(provider="geckoterminal", min_interval_s=0.0, transport=FakeTransport(lambda m, u, b: (200, {}, {"data": []})),
                       sleep=clock.sleep, clock=clock.time)
    with pytest.raises(ValueError):
        audit.check_claim(gecko, "BTC", 0.0)
    out = audit.check_claim(gecko, "CUfphqswgDK3VP3FX7CiShVCTdGQneFusYRFViABpump", 1795207920.0)
    assert out["status"] == "no_data"
