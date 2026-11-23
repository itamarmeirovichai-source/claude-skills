"""Backtest data collection against a small fake chain: unselected sampling, no look-ahead, honest gaps."""

import base64
import dataclasses
import hashlib
import struct

import pytest
from conftest import FakeClock, FakeTransport, with_paper

from launchlab import amm, backfill, db, paper
from launchlab.providers.base import HttpClient, ProviderError

PUMP_COIN = "pumpCmXqMfrsAkQ5r49WcJnRayYRqmXz6ae8H7H9Dfn"
SOL_NATIVE = "1" * 32


def addr(name):
    """A valid-looking 32-byte address derived from a readable name."""
    return backfill.b58encode(hashlib.sha256(name.encode()).digest())


AGENT = addr("mayhem-agent")


class FakeChain:
    """Transactions in ledger order. `getSignaturesForAddress(addr, before=sig)` returns addr's transactions
    that precede `sig`, newest first — the behaviour the backtest relies on."""

    def __init__(self):
        self.txs = []

    def add(self, sig, t, accounts, *, tx=None, err=None):
        self.txs.append({"signature": sig, "blockTime": t, "slot": int(t * 4), "accounts": set(accounts), "err": err, "tx": tx})
        self.txs.sort(key=lambda x: (x["blockTime"], x["signature"]))

    def tx(self, sig):
        return next(x["tx"] for x in self.txs if x["signature"] == sig)

    def __call__(self, method, url, body):
        m, params = body["method"], body["params"]
        if m == "getSignaturesForAddress":
            address, opts = params[0], params[1]
            rows = self.txs
            if opts.get("before"):
                idx = next(i for i, x in enumerate(rows) if x["signature"] == opts["before"])
                rows = rows[:idx]
            hits = [x for x in reversed(rows) if address in x["accounts"]][: opts.get("limit", 1000)]
            return 200, {}, {"result": [{"signature": x["signature"], "blockTime": x["blockTime"], "slot": x["slot"], "err": x["err"]} for x in hits]}
        if m == "getTransaction":
            return 200, {}, {"result": self.tx(params[0])}
        raise AssertionError(m)


def bal(owner, mint, amount):
    return {"owner": owner, "mint": mint, "uiTokenAmount": {"uiAmountString": str(amount)}}


def log(raw):
    return "Program data: " + base64.b64encode(raw).decode()


def create_event(mint, curve, creator, *, quote=SOL_NATIVE, mayhem=False, virtual_quote=30_000_000_000, supply=1e9):
    def text(value):
        return struct.pack("<I", len(value)) + value.encode()

    return log(backfill.CREATE_EVENT + text("Name") + text("SYM") + text("https://example.test/meta.json")
               + backfill.b58decode(mint) + backfill.b58decode(curve) + backfill.b58decode(creator) + backfill.b58decode(creator)
               + struct.pack("<qQQQQ", 1, int(1_073_000_000e6), 30_000_000_000, int(793_100_000e6), int(supply * 1e6))
               + b"\7" * 32 + bytes([mayhem, 0]) + backfill.b58decode(quote) + struct.pack("<QQ", virtual_quote, 30) + b"\0\0")


def trade_event(mint, state, *, is_buy=True):
    """A TradeEvent carrying the curve reserves after the trade."""
    return log(backfill.TRADE_EVENT + backfill.b58decode(mint) + struct.pack("<QQ", 1, 1) + bytes([is_buy]) + b"\5" * 32 + struct.pack("<q", 1)
               + struct.pack("<QQQQ", round(state["virtual_sol"] * 1e9), round(state["virtual_tokens"] * 1e6), round(state["real_sol"] * 1e9),
                             round(state["real_tokens"] * 1e6)) + b"\0" * 200)


def after_sold(sold):
    """Reserves of a standard curve once `sold` tokens have been bought from launch."""
    res = amm.curve_state_after_sold(sold)
    return {"virtual_sol": res.quote, "virtual_tokens": res.base, "real_sol": res.quote - 30.0, "real_tokens": amm.CURVE_TOKENS_FOR_SALE - sold}


def make_tx(t, signers, balances, names, events=()):
    return {"blockTime": t, "slot": int(t * 4), "transaction": {"message": {"accountKeys": [{"pubkey": s, "signer": True} for s in signers]}},
            "meta": {"err": None, "logMessages": [f"Program log: Instruction: {n}" for n in names] + list(events), "preTokenBalances": [],
                     "postTokenBalances": balances, "innerInstructions": []}}


def launch(chain, name, t, *, creator_buy=5_000_000.0, extra_slot0=(), quote=SOL_NATIVE, mayhem=False, virtual_quote=30_000_000_000):
    """A creation transaction (with the creator's own buy) and optional further buys in the same slot.
    Returns (mint, curve, tokens sold so far)."""
    mint, curve, creator = addr(name + "mint"), addr(name + "curve"), addr(name + "creator")
    balances = [bal(curve, mint, 1e9 - creator_buy), bal(creator, mint, creator_buy)] + ([bal(AGENT, mint, 1e9)] if mayhem else [])
    events = [create_event(mint, curve, creator, quote=quote, mayhem=mayhem, virtual_quote=virtual_quote, supply=2e9 if mayhem else 1e9)]
    if creator_buy:
        events.append(trade_event(mint, after_sold(creator_buy)))
    chain.add(f"{name}-create", t, {backfill.MINT_AUTHORITY, curve, mint}, tx=make_tx(t, [creator, mint], balances, ["CreateV2", "BuyV2"], events))
    sold = creator_buy
    for i, (wallets, amount) in enumerate(extra_slot0):
        sold += amount * len(wallets)
        balances = [bal(curve, mint, 1e9 - sold), *[bal(w, mint, amount) for w in wallets]]
        chain.add(f"{name}-slot0-{i}", t, {curve}, tx=make_tx(t, list(wallets), balances, ["BuyV3"], [trade_event(mint, after_sold(sold))]))
    return mint, curve, sold


def trade(chain, name, curve, t, state, n, *, is_buy=True):
    event = trade_event(addr(name + "mint"), state, is_buy=is_buy)
    chain.add(f"{name}-trade-{n}", t, {curve}, tx=make_tx(t, [addr(f"trader{n}")], [], ["BuyV3" if is_buy else "SellV2"], [event]))


def filler(chain, start, end, step=2.0):
    """Other activity signed by the mint authority: it is the clock of signatures the backtest uses as cursors."""
    t = start
    while t <= end:
        chain.add(f"clock-{t:.0f}", t, {backfill.MINT_AUTHORITY, f"other{t:.0f}"}, tx=make_tx(t, [addr("x")], [], ["BuyExactQuoteIn"]))
        t += step


def plan(conn, client, launch_time=1000.0):
    return backfill.plan_backfill(conn, client, "https://rpc.test", hours=1, sample=10_000, now=launch_time + 2 * backfill.OUTCOME_WINDOW_S + 100)


def read(conn, settings, client, signature):
    row = conn.execute("SELECT * FROM backfill_queue WHERE signature = ?", (signature,)).fetchone()
    return backfill.backfill_launch(conn, settings, client, "https://rpc.test", row, backfill.Clock(conn))


@pytest.fixture
def world(conn, settings):
    chain = FakeChain()
    clock = FakeClock(100_000.0)
    client = HttpClient(provider="solana_rpc", min_interval_s=0.0, transport=FakeTransport(chain), sleep=clock.sleep, clock=clock.time, max_retries=0)
    live = dataclasses.replace(with_paper(settings, decision_delay_s=90.0, own_liquidity=True), mode="live")   # the real defaults
    return chain, client, live, conn


def test_sample_is_every_kth_launch_and_ignores_content():
    rows = [{"signature": f"s{i}", "blockTime": i, "slot": i} for i in range(1000)]
    picked = backfill.systematic_sample(rows, 100)
    assert len(picked) == 100 and [r["signature"] for r in picked[:3]] == ["s5", "s15", "s25"]
    assert backfill.systematic_sample(rows, 5000) == rows and backfill.systematic_sample([], 10) == [] and backfill.systematic_sample(rows, 0) == []
    grid = backfill.observation_grid(90.0)
    assert grid[0] == 85 and grid[1] == 100 and grid == sorted(grid) and grid[-1] <= backfill.OUTCOME_WINDOW_S


def test_events_are_decoded_exactly_and_foreign_data_is_ignored():
    mint = addr("m")
    state = {"virtual_sol": 32.2126, "virtual_tokens": 999_299_851.53, "real_sol": 2.2126, "real_tokens": 719_399_851.53}   # a real reading
    tx = make_tx(1.0, [addr("t")], [], ["BuyV3"], [trade_event(addr("other"), after_sold(1e6)), trade_event(mint, after_sold(2e6)), trade_event(mint, state),
                                                    log(b"\1" * 300), "Program data: not-base64!!", "Program log: hello"])
    got = backfill.last_trade_state(tx, mint)
    assert got == pytest.approx(state)                                     # the LAST trade of this mint in the transaction
    assert backfill.last_trade_state(tx, addr("absent")) is None
    payload = backfill.curve_payload(got, 5.0, "sig", "trade event")
    assert payload["price_sol"] == pytest.approx(32.2126 / 999_299_851.53) and payload["liquidity_sol"] == pytest.approx(2.2126)
    assert payload["quote_reserve_sol"] == pytest.approx(32.2126) and "exact curve reserves" in payload["reserve_model"]
    for text in ("CUfphqswgDK3VP3FX7CiShVCTdGQneFusYRFViABpump", "So11111111111111111111111111111111111111112", "1" * 32):
        assert backfill.b58encode(backfill.b58decode(text)) == text
    assert backfill.parse_create_event(b"too short", mint) is None
    assert backfill.parse_create_event(base64.b64decode(trade_event(mint, state)[14:]), mint) is None      # wrong event type


def test_launch_is_read_over_the_whole_window_without_looking_ahead(world):
    chain, client, settings, conn = world
    mint, curve, sold = launch(chain, "good", 1000.0)
    trade(chain, "good", curve, 1040.0, after_sold(sold + 120e6), 1)          # ~4.6 SOL of real depth before the decision
    trade(chain, "good", curve, 1087.0, after_sold(sold + 180e6), 2)          # AFTER the 85 s snapshot, before the decision at 90 s
    trade(chain, "good", curve, 1500.0, after_sold(sold + 320e6), 3)
    chain.add("good-sweep", 1600.0, {curve}, tx=make_tx(1600.0, [addr("keeper")], [], ["SweepProtocolFee"]))   # touches the curve, no trade
    filler(chain, 990.0, 1000.0 + backfill.OUTCOME_WINDOW_S + 20)
    p = plan(conn, client)
    assert p["window_fully_listed"] and p["sample_size"] == p["launches_in_window"]
    status, got_mint, note = read(conn, settings, client, "good-create")
    assert (status, got_mint) == ("read", mint), note
    obs = db.observations(conn, mint, "market")
    assert len(obs) == len(backfill.observation_grid(90.0))
    assert all(o["payload"]["state_time"] <= o["observed_at"] for o in obs)          # a state is never newer than its timestamp
    first = obs[0]
    assert first["observed_at"] == 1085.0 and first["payload"]["state_time"] == 1040.0  # the 1087 trade is not visible at 1085
    assert first["payload"]["liquidity_sol"] == pytest.approx(after_sold(sold + 120e6)["real_sol"])
    assert obs[1]["payload"]["state_time"] == 1087.0
    assert obs[-1]["payload"]["state_time"] == 1500.0                                 # the later fee sweep is stepped over
    assert first["payload"]["venue"] == "curve" and "trade event" in first["payload"]["reserve_model"]
    structure = db.observations(conn, mint, "launch")[-1]["payload"]
    assert structure["status"] == "known" and structure["slot0_share"] == pytest.approx(0.005) and structure["creator"] == addr("goodcreator")
    token = dict(conn.execute("SELECT * FROM tokens WHERE mint = ?", (mint,)).fetchone())
    assert token["is_synthetic"] == 0 and token["launch_time"] == 1000.0 and "backtest sample" in token["launch_source"]
    fetched = sum(1 for c in client.transport.calls if c[2]["method"] == "getTransaction")
    assert fetched <= 8, fetched                                                      # unchanged stretches are not re-read point by point


def test_untraded_launch_is_priced_from_its_creation_event(world):
    chain, client, settings, conn = world
    mint, _, _ = launch(chain, "quiet", 1000.0, creator_buy=0.0)
    filler(chain, 990.0, 1000.0 + backfill.OUTCOME_WINDOW_S + 20)
    plan(conn, client)
    status, _, note = read(conn, settings, client, "quiet-create")
    assert status == "read", note
    obs = db.observations(conn, mint, "market")
    assert len(obs) == len(backfill.observation_grid(90.0))
    assert all(o["payload"]["price_sol"] == pytest.approx(amm.initial_curve().price) and o["payload"]["liquidity_sol"] == 0.0 for o in obs)
    assert "creation event" in obs[0]["payload"]["reserve_model"]
    assert sum(1 for c in client.transport.calls if c[2]["method"] == "getTransaction") == 1     # only the creation transaction itself


def test_bot_noise_on_a_standard_curve_is_read_through_its_token_balance(world):
    chain, client, settings, conn = world
    mint, curve, sold = launch(chain, "noisy", 1000.0)
    trade(chain, "noisy", curve, 1030.0, after_sold(sold + 90e6), 1)
    for i in range(12):                                   # a bot touches the curve's token account without trading
        t = 1035.0 + i * 4
        chain.add(f"noisy-bot-{i:02d}", t, {curve}, tx=make_tx(t, [addr("bot")], [bal(curve, mint, 1e9 - sold - 90e6)], []))
    filler(chain, 990.0, 1000.0 + backfill.OUTCOME_WINDOW_S + 20)
    plan(conn, client)
    assert read(conn, settings, client, "noisy-create")[0] == "read"
    first = db.observations(conn, mint, "market")[0]["payload"]
    assert first["price_sol"] == pytest.approx(amm.curve_state_after_sold(sold + 90e6).price)     # same as the trade event would give
    assert first["liquidity_sol"] == pytest.approx(after_sold(sold + 90e6)["real_sol"]) and "token balance" in first["reserve_model"]
    assert backfill.state_from_balance(1e9 - 16_690_000.0, {"virtual_sol": 30.0, "virtual_tokens": 1_073e6, "real_sol": 0.0, "real_tokens": 793.1e6}) \
        == pytest.approx(after_sold(16_690_000.0))


def test_bundle_structure_is_recorded_from_the_creation_slot(world):
    chain, client, settings, conn = world
    wallets = [addr(f"w{i}") for i in range(7)]
    mint, curve, sold = launch(chain, "bund", 1000.0, extra_slot0=[(wallets, 60_000_000.0)])   # 42% of supply in the creation slot
    trade(chain, "bund", curve, 1300.0, after_sold(sold + 100e6), 1)
    filler(chain, 990.0, 1000.0 + backfill.OUTCOME_WINDOW_S + 20)
    plan(conn, client)
    assert read(conn, settings, client, "bund-create")[0] == "read"
    structure = db.observations(conn, mint, "launch")[-1]["payload"]
    assert structure["slot0_share"] == pytest.approx(0.425) and [len(g) for g in structure["cosigner_groups"]] == [7]
    assert structure["is_mayhem"] is False


def test_curves_not_quoted_in_sol_are_recorded_as_unreadable_not_approximated(world):
    chain, client, settings, conn = world
    mint, _, _ = launch(chain, "coinq", 1000.0, quote=PUMP_COIN, virtual_quote=1_287_448_596_925)
    filler(chain, 990.0, 1000.0 + backfill.OUTCOME_WINDOW_S + 20)
    plan(conn, client)
    status, _, note = read(conn, settings, client, "coinq-create")
    assert status == "unsupported" and "not SOL" in note
    assert db.observations(conn, mint, "market") == []
    assert db.observations(conn, mint, "launch")[-1]["payload"]["status"] == "unknown"
    with pytest.raises(ValueError):
        backfill.parse_creation(make_tx(1.0, [addr("a")], [], ["BuyExactQuoteIn"]))
    no_event = make_tx(1.0, [addr("c"), addr("m")], [bal(addr("curve"), addr("m"), 1e9)], ["CreateV2"])
    assert backfill.parse_creation(no_event)["why_not_standard"] == "creation event not readable in the transaction logs"


def test_mayhem_launch_uses_the_reserves_the_chain_reports_never_a_formula(world):
    chain, client, settings, conn = world
    mint, curve, sold = launch(chain, "may", 1000.0, mayhem=True, creator_buy=2_455_214.0)
    info = backfill.parse_creation(chain.tx("may-create"))
    assert info["standard"] and info["is_mayhem"] and info["curve"] == curve          # the curve, not the agent that also holds 1e9
    assert info["start"] == pytest.approx({"virtual_sol": 30.0, "virtual_tokens": 1_073_000_000.0, "real_sol": 0.0, "real_tokens": 793_100_000.0})
    trade(chain, "may", curve, 1030.0, after_sold(sold + 150e6), 1)
    # the automated agent then sells part of its extra billion into the curve: real SOL is drained and the
    # price falls far below the launch price — something the standard-curve formula cannot represent
    drained = {"virtual_sol": 0.1896, "virtual_tokens": 939_010_663.26, "real_sol": 0.0204, "real_tokens": 659_110_663.26}
    trade(chain, "may", curve, 1060.0, drained, 2, is_buy=False)
    chain.add("may-bot", 1070.0, {curve}, tx=make_tx(1070.0, [addr("bot")], [bal(curve, mint, 866_010_663.26)], []))   # noise with a balance
    filler(chain, 990.0, 1000.0 + backfill.OUTCOME_WINDOW_S + 20)
    plan(conn, client)
    assert read(conn, settings, client, "may-create")[0] == "read"
    seen = db.observations(conn, mint, "market")[0]["payload"]
    assert seen["price_sol"] == pytest.approx(0.1896 / 939_010_663.26) and seen["price_sol"] < amm.initial_curve().price / 100
    assert seen["liquidity_sol"] == pytest.approx(0.0204) and "trade event" in seen["reserve_model"]   # the bot's balance was not used
    structure = db.observations(conn, mint, "launch")[-1]["payload"]
    assert structure["is_mayhem"] is True and AGENT not in {b["wallet"] for b in structure["slot0_buyers"]}


def test_full_run_applies_both_rulebooks_to_every_sampled_launch_and_resumes(world):
    chain, client, settings, conn = world
    now = 1000.0 + 2 * backfill.OUTCOME_WINDOW_S + 100
    good, curve, sold = launch(chain, "good", 1000.0)
    trade(chain, "good", curve, 1040.0, after_sold(sold + 120e6), 1)
    trade(chain, "good", curve, 1400.0, after_sold(sold + 420e6), 2)      # price more than doubles -> take-profit
    trade(chain, "good", curve, 1450.0, after_sold(sold + 430e6), 3)
    bund, _, _ = launch(chain, "bund", 1010.0, extra_slot0=[([addr(f"w{i}") for i in range(7)], 60_000_000.0)])
    dud, _, _ = launch(chain, "dud", 1020.0)                         # nobody ever trades it
    filler(chain, 1025.0, 1020.0 + backfill.OUTCOME_WINDOW_S + 20)   # later activity: the clock
    with pytest.raises(ProviderError):
        backfill.run_backfill(conn, dataclasses.replace(settings, mode="demo"), client, "https://rpc.test", now=now)
    out = backfill.run_backfill(conn, settings, client, "https://rpc.test", hours=1, sample=10_000, now=now)
    sampled = {r["signature"]: r["status"] for r in conn.execute("SELECT signature, status FROM backfill_queue")}
    assert (sampled["good-create"], sampled["bund-create"], sampled["dud-create"]) == ("read", "read", "read")
    assert all(status == "skipped" for sig, status in sampled.items() if sig.startswith("clock-"))   # signed by the authority, but not launches
    strict, loose = out["books"]["backtest"]["metrics"], out["books"]["backtest-all"]["metrics"]
    assert (strict["ruleset"], loose["ruleset"]) == ("baseline-v1", "enter-all-v1")
    assert strict["signals"] == 3 and strict["candidates"] == 1 and strict["rejected"] == 2 and not strict["is_synthetic"]
    assert strict["rejection_reasons"]["low_liquidity"] == 1 and strict["rejection_reasons"]["slot0_concentration"] == 1
    assert strict["verdict"] == "inconclusive" and "descriptive only" in strict["verdict_note"]      # one day of data is never a verdict
    assert loose["signals"] == 3 and loose["candidates"] == 3 and loose["rejected"] == 0             # the baseline enters everything priced
    by_mint = {r["mint"]: dict(r) for r in conn.execute("SELECT * FROM positions WHERE book = 'backtest-all'")}
    assert by_mint[good]["exit_reason"] == "take_profit" and by_mint[good]["net_pnl_sol"] > 0
    assert by_mint[dud]["exit_reason"] == "time_stop" and by_mint[dud]["net_pnl_sol"] == pytest.approx(-0.0, abs=1e-3)   # quiet curve: stake comes back
    assert by_mint[bund]["status"] == "closed"
    strict_pos = dict(conn.execute("SELECT * FROM positions WHERE book = 'backtest'").fetchone())
    assert strict_pos["mint"] == good and strict_pos["net_pnl_sol"] == pytest.approx(by_mint[good]["net_pnl_sol"])
    calls_before = len(client.transport.calls)
    again = backfill.run_backfill(conn, settings, client, "https://rpc.test", hours=1, sample=10_000, now=now)
    assert again["queue"] == out["queue"] and again["books"]["backtest"]["run"]["new_signals"] == 0
    assert len(client.transport.calls) == calls_before                # nothing is re-read, nothing is re-decided
    assert paper.book_metrics(conn, "backtest-all", settings)["net_pnl_sol"] == loose["net_pnl_sol"]


def test_parallel_readers_give_the_same_ledger_as_one_reader(world, tmp_path):
    chain, _, settings, _ = world
    now = 1000.0 + 2 * backfill.OUTCOME_WINDOW_S + 100
    for i in range(12):                                             # a dozen launches of three kinds
        name, t = f"t{i}", 1000.0 + i
        if i % 3 == 0:
            _, curve, sold = launch(chain, name, t)
            trade(chain, name, curve, t + 40, after_sold(sold + 120e6), 1)
            trade(chain, name, curve, t + 400, after_sold(sold + (420e6 if i % 2 else 60e6)), 2)
        elif i % 3 == 1:
            launch(chain, name, t, extra_slot0=[([addr(f"{name}w{k}") for k in range(7)], 60_000_000.0)])
        else:
            launch(chain, name, t, creator_buy=0.0)
    filler(chain, 1015.0, 1012.0 + backfill.OUTCOME_WINDOW_S + 20)

    def run(path, workers):
        cfg = dataclasses.replace(settings, db_path=path)
        conn = db.connect(path)

        def setup():
            clock = FakeClock(100_000.0)
            return db.connect(path), HttpClient(provider="solana_rpc", min_interval_s=0.0, transport=FakeTransport(chain), sleep=clock.sleep,
                                                clock=clock.time, max_retries=0)

        out = backfill.run_backfill(conn, cfg, setup()[1], "https://rpc.test", hours=1, sample=10_000, now=now, workers=workers, worker_setup=setup)
        ledger = [tuple(r) for r in conn.execute("SELECT book, mint, decision, reasons FROM signals ORDER BY book, mint")]
        pnl = [(r["book"], r["mint"], r["status"], round(r["net_pnl_sol"], 12)) for r in conn.execute("SELECT * FROM positions ORDER BY book, mint")]
        return out["queue"], ledger, pnl

    serial, parallel = run(tmp_path / "one.sqlite3", 1), run(tmp_path / "four.sqlite3", 4)
    assert serial == parallel
    assert serial[0]["read"] == 12 and len(serial[1]) == 24 and len([p for p in serial[2] if p[0] == "backtest"]) == 4
