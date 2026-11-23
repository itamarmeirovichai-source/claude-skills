"""Paper-trading simulator: hand-checkable PnL, no look-ahead, honest handling of failures."""

import dataclasses
import json

import pytest
from conftest import launch, market, with_paper

from launchlab import paper, policy

MINT = "SYNTH0001test"
EXIT = policy.ExitRule(take_profit=2.0, stop_loss=0.5, max_hold_s=600.0)


def setup_token(conn, t0=1000.0):
    launch(conn, MINT, t0)
    market(conn, MINT, t0 + 50, 100.0, 1_000_000.0)       # seen by the decision at t0+60
    market(conn, MINT, t0 + 75, 100.0, 1_000_000.0)       # first observation after as_of + 10 s latency -> entry
    return t0


def run(conn, settings, exit_rule=EXIT):
    return paper.run_book(conn, settings, "demo", synthetic=True, exit_rule=exit_rule)


def position(conn):
    return dict(conn.execute("SELECT * FROM positions").fetchone())


def test_take_profit_pnl_by_hand_and_the_spike_is_never_used(conn, settings):
    t0 = setup_token(conn)
    market(conn, MINT, t0 + 100, 150.0, 666_666.6667)     # price 2.25e-4 -> 2.2x the fill price -> take-profit trigger
    market(conn, MINT, t0 + 105, 400.0, 250_000.0)        # a spike to 1.6e-3 (the "all-time high") 5 s later
    market(conn, MINT, t0 + 120, 120.0, 833_333.3333)     # first observation after trigger + 10 s latency -> exit here
    assert run(conn, settings)["simulated"] == {"closed": 1}
    pos = position(conn)
    tokens = 1_000_000.0 * 1.0 / 101.0                    # 9,900.990099 tokens for 1 SOL
    expected_out = 120.0 * tokens / (833_333.3333 + tokens)  # 1.40898 SOL
    assert pos["tokens"] == pytest.approx(tokens)
    assert pos["cost_sol"] == pytest.approx(1.0)
    assert pos["proceeds_sol"] == pytest.approx(expected_out, rel=1e-6)
    assert pos["net_pnl_sol"] == pytest.approx(expected_out - 1.0, rel=1e-6)
    assert pos["exit_reason"] == "take_profit"
    spike_value = 400.0 * tokens / (250_000.0 + tokens)   # what selling into the spike would have paid: ~15.2 SOL
    assert spike_value > 10 and pos["proceeds_sol"] < 2    # the later high is not the exit
    fills = [dict(r) for r in conn.execute("SELECT * FROM fills ORDER BY filled_at")]
    assert [f["side"] for f in fills] == ["buy", "sell"]
    assert fills[0]["filled_at"] == t0 + 75 and fills[1]["filled_at"] == t0 + 120


def test_fees_and_network_costs_are_all_counted(conn, settings):
    settings = with_paper(settings, venue_fee_override=0.01, base_fee_sol=0.001, priority_fee_sol=0.002, token_account_rent_sol=0.003)
    t0 = setup_token(conn)
    market(conn, MINT, t0 + 100, 150.0, 666_666.6667)
    market(conn, MINT, t0 + 120, 120.0, 833_333.3333)
    run(conn, settings)
    pos = position(conn)
    tokens = 1_000_000.0 * 0.99 / 100.99                  # 1% fee comes off the 1 SOL input
    gross_out = 120.0 * tokens / (833_333.3333 + tokens)
    out = gross_out * 0.99                                # 1% fee comes off the output
    cost = 1.0 + 0.003 + 0.003                            # stake + one network attempt + rent
    proceeds = out - 0.003                                # one network attempt on the way out
    fees = 0.01 + gross_out * 0.01 + 0.003 + 0.003 + 0.003
    assert pos["cost_sol"] == pytest.approx(cost)
    assert pos["proceeds_sol"] == pytest.approx(proceeds, rel=1e-6)
    assert pos["fees_sol"] == pytest.approx(fees, rel=1e-6)
    assert pos["net_pnl_sol"] == pytest.approx(proceeds - cost, rel=1e-6)
    assert pos["gross_pnl_sol"] == pytest.approx(pos["net_pnl_sol"] + pos["fees_sol"])


def test_stop_loss_and_time_stop(conn, settings):
    t0 = setup_token(conn)
    market(conn, MINT, t0 + 90, 60.0, 1_666_666.667)      # price 3.6e-5 -> 0.36x -> stop
    market(conn, MINT, t0 + 101, 50.0, 2_000_000.0)       # exit one latency later, at an even lower price
    run(conn, settings)
    pos = position(conn)
    assert pos["exit_reason"] == "stop_loss" and pos["net_pnl_sol"] < -0.7
    for table in ("fills", "positions", "signals"):
        conn.execute(f"DELETE FROM {table}")
    conn.execute("DELETE FROM observations WHERE observed_at > ?", (t0 + 80,))
    market(conn, MINT, t0 + 400, 100.0, 1_000_000.0)      # flat
    market(conn, MINT, t0 + 700, 100.0, 1_000_000.0)      # > 600 s after entry at t0+75 -> time stop
    market(conn, MINT, t0 + 715, 100.0, 1_000_000.0)
    run(conn, settings)
    pos = position(conn)
    assert pos["exit_reason"] == "time_stop"
    assert pos["net_pnl_sol"] == pytest.approx(-(1.0 - 100.0 * pos["tokens"] / (1_000_000.0 + pos["tokens"])))  # round-trip impact only


def test_unsellable_when_no_exit_data_and_not_filled_when_no_entry_data(conn, settings):
    t0 = setup_token(conn)
    market(conn, MINT, t0 + 100, 150.0, 666_666.6667)     # trigger, then the data stops
    run(conn, settings)
    pos = position(conn)
    assert pos["status"] == "unsellable" and pos["proceeds_sol"] == 0 and pos["net_pnl_sol"] == pytest.approx(-1.0)

    other = "SYNTH0002test"
    launch(conn, other, 5000.0)
    market(conn, other, 5050.0, 100.0, 1_000_000.0)       # decision sees this; nothing afterwards
    run(conn, settings)
    row = dict(conn.execute("SELECT * FROM positions WHERE mint = ?", (other,)).fetchone())
    assert row["status"] == "not_filled" and row["tokens"] == 0 and "no usable market data" in row["exit_reason"]


def test_exit_refused_when_depth_is_below_the_minimum(conn, settings):
    settings = with_paper(settings, min_exit_liquidity_sol=5.0)
    t0 = setup_token(conn)
    market(conn, MINT, t0 + 100, 150.0, 666_666.6667)
    market(conn, MINT, t0 + 120, 120.0, 833_333.3333, liquidity=0.4)
    run(conn, settings)
    pos = position(conn)
    assert pos["status"] == "unsellable" and "exit depth" in pos["exit_reason"]


def test_failed_attempts_cost_money_and_can_prevent_a_fill(conn, settings):
    settings = with_paper(settings, fail_prob=0.999, base_fee_sol=0.001)
    setup_token(conn)
    run(conn, settings)
    pos = position(conn)
    assert pos["status"] == "not_filled" and pos["failed_attempts"] == 3
    assert pos["net_pnl_sol"] == pytest.approx(-0.003) and pos["exit_reason"] == "every attempt failed"


def test_partial_fill_is_capped_by_pool_share(conn, settings):
    settings = with_paper(settings, max_pool_share=0.005)  # at most 0.5 SOL against a 100 SOL reserve
    t0 = setup_token(conn)
    market(conn, MINT, t0 + 700, 100.0, 1_000_000.0)
    market(conn, MINT, t0 + 715, 100.0, 1_000_000.0)
    run(conn, settings)
    pos = position(conn)
    assert pos["partial"] == 1 and pos["cost_sol"] == pytest.approx(0.5)


def test_stale_observations_are_never_used_for_fills(conn, settings):
    t0 = 1000.0
    launch(conn, MINT, t0)
    market(conn, MINT, t0 + 50, 100.0, 1_000_000.0)
    market(conn, MINT, t0 + 72, 1.0, 100_000_000.0, stale=True)   # a stale, absurdly cheap print
    market(conn, MINT, t0 + 80, 100.0, 1_000_000.0)
    market(conn, MINT, t0 + 800, 100.0, 1_000_000.0)
    market(conn, MINT, t0 + 815, 100.0, 1_000_000.0)
    run(conn, settings)
    buy = dict(conn.execute("SELECT * FROM fills WHERE side = 'buy'").fetchone())
    assert buy["filled_at"] == t0 + 80


def test_signal_features_ignore_everything_after_as_of(conn, settings):
    t0 = setup_token(conn)
    as_of = t0 + 60
    before = paper.build_features(conn, MINT, as_of)
    market(conn, MINT, t0 + 61, 9_999.0, 10.0)            # the future: an enormous price
    market(conn, MINT, t0 + 5000, 0.001, 1e9)
    launch(conn, MINT, t0 + 61, slot0_share=0.99)         # a later launch record must not leak either
    after = paper.build_features(conn, MINT, as_of)
    assert before == after
    assert policy.decide(before) == policy.decide(after)


def test_signal_is_recorded_before_its_outcome_and_rejections_are_kept(conn, settings):
    t0 = setup_token(conn)
    market(conn, MINT, t0 + 100, 150.0, 666_666.6667)
    market(conn, MINT, t0 + 120, 120.0, 833_333.3333)
    launch(conn, "SYNTH0003bundle", 9000.0, slot0_share=0.8, buyers=[{"wallet": "a", "share": 0.4}, {"wallet": "b", "share": 0.4}], groups=[["a", "b"]])
    market(conn, "SYNTH0003bundle", 9050.0, 100.0, 1_000_000.0)
    run(conn, settings)
    events = [(r["id"], r["type"], json.loads(r["payload"])) for r in conn.execute("SELECT * FROM events ORDER BY id")]
    sig_id = conn.execute("SELECT id FROM signals WHERE mint = ?", (MINT,)).fetchone()["id"]
    recorded = next(i for i, t, p in events if t == "signal_recorded" and p["signal_id"] == sig_id)
    outcome = next(i for i, t, p in events if t.startswith("position_") and p["signal_id"] == sig_id)
    assert recorded < outcome
    rejected = dict(conn.execute("SELECT * FROM signals WHERE mint = 'SYNTH0003bundle'").fetchone())
    assert rejected["decision"] == "rejected"
    codes = {r.split(":")[0] for r in json.loads(rejected["reasons"])}
    assert {"slot0_concentration", "cosigned_supply"} <= codes
    assert conn.execute("SELECT COUNT(*) FROM positions WHERE mint = 'SYNTH0003bundle'").fetchone()[0] == 0
    m = paper.book_metrics(conn, "demo", settings)
    assert m["signals"] == 2 and m["candidates"] == 1 and m["rejected"] == 1
    assert m["verdict"] == "mechanics demo"               # synthetic results are never called evidence


def test_rerun_is_idempotent_and_one_signal_per_token(conn, settings):
    t0 = setup_token(conn)
    market(conn, MINT, t0 + 100, 150.0, 666_666.6667)
    market(conn, MINT, t0 + 120, 120.0, 833_333.3333)
    run(conn, settings)
    first = position(conn)
    again = run(conn, settings)
    assert again["new_signals"] == 0 and again["simulated"] == {}
    assert position(conn)["net_pnl_sol"] == first["net_pnl_sol"]
    assert conn.execute("SELECT COUNT(*) FROM signals").fetchone()[0] == 1


def test_live_book_waits_for_data_instead_of_inventing_an_outcome(conn, settings):
    t0 = 1000.0
    launch(conn, "So11111111111111111111111111111111111111112", t0, synthetic=False)
    mint = "So11111111111111111111111111111111111111112"
    market(conn, mint, t0 + 50, 100.0, 1_000_000.0, synthetic=False)
    too_early = paper.run_book(conn, settings, "live", synthetic=False, exit_rule=EXIT, now=t0 + 10)
    assert too_early["new_signals"] == 0                  # never decide before the decision time has passed
    res = paper.run_book(conn, settings, "live", synthetic=False, exit_rule=EXIT, now=t0 + 65)
    assert res["new_signals"] == 1 and res["simulated"] == {"pending": 1}
    assert conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0] == 0
    market(conn, mint, t0 + 75, 100.0, 1_000_000.0, synthetic=False)
    res = paper.run_book(conn, settings, "live", synthetic=False, exit_rule=EXIT, now=t0 + 80)
    assert res["simulated"] == {"open": 1}
    m = paper.book_metrics(conn, "live", settings)
    assert m["verdict"] == "inconclusive" and m["open"] == 1 and m["resolved"] == 0
    assert m["open_marked_to_zero_sol"] == pytest.approx(-1.0)


def test_metrics_helpers_on_hand_checked_numbers():
    assert paper.max_drawdown([1.0, -2.0, 0.5, -1.0]) == pytest.approx(2.5)   # peak +1, trough -1.5
    assert paper.max_drawdown([]) == 0 and paper.max_drawdown([1, 1, 1]) == 0
    assert paper.bootstrap_mean_ci([0.1]) is None
    lo, hi = paper.bootstrap_mean_ci([-0.5, -0.4, -0.6, -0.5, -0.45, -0.55] * 5, seed=3)
    assert lo < -0.5 < hi and hi < 0
    assert paper.bootstrap_mean_ci([1, 2, 3, 4], seed=9) == paper.bootstrap_mean_ci([1, 2, 3, 4], seed=9)
    u = [paper.det_uniform(1, "mint", "buy", k) for k in range(200)]
    assert all(0 <= x < 1 for x in u) and len(set(u)) == 200
    assert paper.det_uniform(1, "m", "buy", 0) == paper.det_uniform(1, "m", "buy", 0)


def test_metrics_count_every_outcome_in_expectancy(conn, settings):
    t0 = setup_token(conn)
    market(conn, MINT, t0 + 100, 150.0, 666_666.6667)     # unsellable: -100%
    launch(conn, "SYNTH0004win", 20_000.0)
    market(conn, "SYNTH0004win", 20_050.0, 100.0, 1_000_000.0)
    market(conn, "SYNTH0004win", 20_075.0, 100.0, 1_000_000.0)
    market(conn, "SYNTH0004win", 20_100.0, 150.0, 666_666.6667)
    market(conn, "SYNTH0004win", 20_120.0, 120.0, 833_333.3333)
    run(conn, settings)
    m = paper.book_metrics(conn, "demo", settings)
    win = 120.0 * (1e6 / 101.0) / (833_333.3333 + 1e6 / 101.0) - 1.0
    assert m["resolved"] == 2 and m["unsellable"] == 1
    assert m["expectancy"] == pytest.approx((win - 1.0) / 2, rel=1e-6)
    assert m["win_rate"] == 0.5
    assert m["net_pnl_sol"] == pytest.approx(win - 1.0, rel=1e-6)
    assert sum(b["count"] for b in m["distribution"]) == 2
    assert m["max_drawdown_sol"] == pytest.approx(1.0)
    assert dataclasses.asdict(settings.paper)["size_sol"] == 1.0


def test_own_position_stays_in_the_pool_by_default(conn, settings):
    """Buy into a pool nobody else touches, sell later: with our own SOL counted you get the stake back
    (no fees here); priced as if it had never been there you would lose to your own price impact twice."""
    assert settings.paper.own_liquidity is False and paper.PaperConfig().own_liquidity is True   # fixture is the conservative variant
    t0 = setup_token(conn)
    market(conn, MINT, t0 + 700, 100.0, 1_000_000.0)      # the recorded history never changes
    market(conn, MINT, t0 + 715, 100.0, 1_000_000.0)
    run(conn, with_paper(settings, own_liquidity=True))
    pos = position(conn)
    tokens = 1_000_000.0 / 101.0
    assert pos["tokens"] == pytest.approx(tokens)
    assert pos["proceeds_sol"] == pytest.approx(100.0 * tokens / (1_000_000.0 - tokens))        # Q·x / (B − x)
    assert pos["net_pnl_sol"] == pytest.approx(0.0, abs=1e-4)                                    # round trip in a quiet pool
    sell = dict(conn.execute("SELECT * FROM fills WHERE side = 'sell'").fetchone())
    assert "own position kept in the pool" in sell["model"]


def test_own_liquidity_model_still_loses_when_the_pool_is_drained(conn, settings):
    cfg = with_paper(settings, own_liquidity=True)
    t0 = setup_token(conn)                                # entry at 100 SOL / 1,000,000 tokens
    market(conn, MINT, t0 + 90, 2.0, 50_000_000.0, liquidity=0.01)   # everyone else left: price down 99.96%
    market(conn, MINT, t0 + 101, 2.0, 50_000_000.0, liquidity=0.01)
    run(conn, cfg)
    pos = position(conn)
    assert pos["exit_reason"] == "stop_loss" and pos["status"] == "closed"
    assert pos["proceeds_sol"] == pytest.approx(2.0 * pos["tokens"] / (50_000_000.0 - pos["tokens"]))
    assert pos["net_pnl_sol"] < -0.99                     # nearly the whole stake is gone
    huge = {"payload": {"price_sol": 1e-6, "quote_reserve_sol": 1.0, "base_reserve": 1_000.0, "venue": "pool"}, "stale": False}
    assert paper.sell_fill(huge, 5_000.0, cfg.paper)["sellable"] is False


def test_second_ruleset_gets_its_own_book_and_label(conn, settings):
    setup_token(conn)
    everything = policy.DecisionRule(max_slot0_share=2.0, max_creator_share=2.0, max_cosigned_share=2.0, serial_min_launches=10**9,
                                     min_liquidity_sol=0.0, max_data_age_s=1e12, require_launch_structure=False)
    launch(conn, "SYNTH0009bundle", 3000.0, slot0_share=0.9)
    market(conn, "SYNTH0009bundle", 3050.0, 100.0, 1_000_000.0)
    paper.run_book(conn, settings, "strict", synthetic=True)
    paper.run_book(conn, settings, "all", synthetic=True, decision_rule=everything, ruleset="enter-all-v1")
    strict = {r["mint"]: r["decision"] for r in conn.execute("SELECT mint, decision FROM signals WHERE book = 'strict'")}
    loose = {r["mint"]: (r["decision"], r["ruleset"]) for r in conn.execute("SELECT mint, decision, ruleset FROM signals WHERE book = 'all'")}
    assert strict["SYNTH0009bundle"] == "rejected" and loose["SYNTH0009bundle"] == ("candidate", "enter-all-v1")
    assert paper.book_metrics(conn, "all", settings)["ruleset"] == "enter-all-v1"
    assert paper.book_metrics(conn, "strict", settings)["ruleset"] == policy.RULESET


def test_exit_never_pays_more_sol_than_the_venue_holds(settings):
    cfg = with_paper(settings, own_liquidity=True).paper
    # a Mayhem-style state: high virtual SOL, almost no real SOL; selling 10% of the token reserve
    obs = {"payload": {"price_sol": 1e-7, "quote_reserve_sol": 100.0, "base_reserve": 1e9, "liquidity_sol": 0.3, "venue": "curve"}, "stale": False}
    uncapped = paper.sell_fill(obs, 1e8, cfg)
    capped = paper.sell_fill(obs, 1e8, cfg, own_quote_sol=0.49)
    assert uncapped["out_sol"] == pytest.approx(100.0 * 1e8 / 9e8)                     # 11.1 SOL that is not there
    assert capped["out_sol"] == pytest.approx(0.79) and "capped" in capped["model"]
    roomy = {"payload": {**obs["payload"], "liquidity_sol": 70.0}, "stale": False}       # a standard curve: cap does not bind
    assert paper.sell_fill(roomy, 1e8, cfg, own_quote_sol=0.49)["out_sol"] == pytest.approx(uncapped["out_sol"])
