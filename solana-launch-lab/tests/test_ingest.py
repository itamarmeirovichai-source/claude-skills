"""Live ingestion with every provider faked: provenance, conflicts, partial failure, demo-mode refusal."""

import base64
import dataclasses
import struct

import pytest
from conftest import FakeClock, FakeTransport

from launchlab import amm, db, ingest, risk
from launchlab.providers import solana_rpc
from launchlab.providers.base import HttpClient, ProviderError

MINT = "CUfphqswgDK3VP3FX7CiShVCTdGQneFusYRFViABpump"
CURVE = "ACUSZ93rMjtPKGwZFkWa9tBNKjYSCeQeexsJYc84tY41"
POOL = "5q1eZo7m3NjacXmSuM8BZZ8iqzGt8eqU9FtqTNus7aoJ"

DEX = [{"dexId": "pumpswap", "pairAddress": POOL, "baseToken": {"address": MINT, "name": "BartCoin", "symbol": "BTC"},
        "quoteToken": {"symbol": "SOL"}, "priceNative": "0.00000002062", "priceUsd": "0.000001448", "fdv": 1444, "marketCap": 1444,
        "liquidity": {"usd": 1572.35, "base": 971816856, "quote": 2.3441}, "volume": {"h24": 40.78}, "pairCreatedAt": 1795207513000}]


def gecko_pools(price="0.0000014383", liq="1568.04"):
    rel = {"base_token": {"data": {"id": "solana_" + MINT}}}
    return {"data": [
        {"attributes": {"address": POOL, "name": "BTC / SOL", "pool_created_at": "2026-11-20T20:45:13Z", "base_token_price_usd": price,
                        "fdv_usd": "1433.96", "reserve_in_usd": liq}, "relationships": {**rel, "dex": {"data": {"id": "pumpswap"}}}},
        {"attributes": {"address": CURVE, "name": "BTC / SOL", "pool_created_at": "2026-11-20T20:45:13Z", "reserve_in_usd": "0.0"},
         "relationships": {**rel, "dex": {"data": {"id": "pump-fun"}}}}]}


def make_clients(dex=None, gecko=None, rpc=None, start=1_000_000.0):
    clock = FakeClock(start)

    def mk(name, script):
        return HttpClient(provider=name, min_interval_s=0.0, transport=FakeTransport(script), sleep=clock.sleep, clock=clock.time, max_retries=0)

    def rpc_default(method, url, body):
        if body["method"] == "getSignaturesForAddress":
            return 200, {}, {"result": []}
        return 200, {}, {"error": {"code": 429, "message": "method limit 0"}}   # what the public endpoint does for holder queries

    return ingest.Clients(dex=mk("dexscreener", dex or (lambda m, u, b: (200, {}, DEX))),
                          gecko=mk("geckoterminal", gecko or (lambda m, u, b: (200, {}, gecko_pools()))),
                          rpc=mk("solana_rpc", rpc or rpc_default))


def live(settings):
    return dataclasses.replace(settings, mode="live")


def test_demo_mode_refuses_live_ingest_and_bad_mints_are_rejected(conn, settings):
    with pytest.raises(ProviderError) as err:
        ingest.ingest_mint(conn, settings, MINT, make_clients())
    assert err.value.kind == "disabled"
    for bad in ("BTC", "", "0x1234", "SYNTH00010demo0token0not0real", MINT + "!"):
        with pytest.raises(ValueError):
            ingest.ingest_mint(conn, live(settings), bad, make_clients())
    assert conn.execute("SELECT COUNT(*) FROM tokens").fetchone()[0] == 0


def test_ingest_stores_observations_with_source_time_and_definitions(conn, settings):
    out = ingest.ingest_mint(conn, live(settings), MINT, make_clients(), now=2_000_000.0)
    assert out["stored"]["market"] == 2                         # one per provider; the emptied curve record is skipped
    token = dict(conn.execute("SELECT * FROM tokens WHERE mint = ?", (MINT,)).fetchone())
    assert token["is_synthetic"] == 0 and token["symbol"] == "BTC" and token["launch_time"] == 1795207513.0
    assert "geckoterminal" in token["launch_source"]
    for obs in db.observations(conn, MINT, "market"):
        assert obs["provider"] in ("dexscreener", "geckoterminal") and not obs["is_synthetic"]
        assert obs["observed_at"] > 0 and obs["ingested_at"] == 2_000_000.0
        assert obs["payload"]["fdv_definition"] and obs["payload"]["market_cap_definition"]
    dex = next(o for o in db.observations(conn, MINT, "market") if o["provider"] == "dexscreener")
    # reserves are attached only because pool balances + boost reproduce the quoted price
    assert dex["payload"]["quote_reserve_sol"] == pytest.approx(2.3441 + amm.OBSERVED_POOL_BOOST_SOL)
    assert dex["payload"]["liquidity_sol"] == 2.3441 and "cross-checked" in dex["payload"]["reserve_model"]
    kinds = {e["provider"] + ":" + e["kind"] for e in out["errors"]}
    assert "solana_rpc:rate_limited" in kinds                   # holders refused -> reported, not invented
    report = risk.risk_report(conn, MINT)
    by_name = {c["name"]: c for c in report["components"]}
    assert by_name["ownership_concentration"]["status"] == "unknown"
    assert by_name["launch_slot_concentration"]["status"] == "unknown"
    assert by_name["liquidity"]["level"] == "high"               # 2.34 SOL of real depth
    kept = {r["provider"] for r in conn.execute("SELECT provider FROM raw_snapshots")}
    assert kept == {"solana_rpc"}                                # market providers' raw replies are not stored by default


def test_provider_disagreement_is_recorded_not_averaged(conn, settings):
    clients = make_clients(gecko=lambda m, u, b: (200, {}, gecko_pools(price="0.0000029", liq="1568.04")))
    out = ingest.ingest_mint(conn, live(settings), MINT, clients)
    assert out["stored"]["conflicts"] == 1
    row = dict(conn.execute("SELECT * FROM conflicts").fetchone())
    assert row["field"] == "price_usd" and row["provider_a"] == "dexscreener" and row["provider_b"] == "geckoterminal"
    assert row["rel_diff"] == pytest.approx(1 - 1.448 / 2.9, rel=1e-3)
    prices = sorted(o["payload"]["price_usd"] for o in db.observations(conn, MINT, "market"))
    assert prices == [0.000001448, 0.0000029]                    # both values are kept as reported


def test_one_provider_failing_does_not_block_the_others(conn, settings):
    clients = make_clients(dex=lambda m, u, b: (500, {}, b"oops"), gecko=lambda m, u, b: (200, {}, gecko_pools()))
    out = ingest.ingest_mint(conn, live(settings), MINT, clients)
    assert out["stored"]["market"] == 1
    assert any(e["provider"] == "dexscreener" and e["kind"] == "http" for e in out["errors"])
    health = {r["provider"]: dict(r) for r in conn.execute("SELECT * FROM provider_health")}
    assert health["dexscreener"]["error_count"] == 1 and health["geckoterminal"]["ok_count"] == 1
    clients = make_clients(dex=lambda m, u, b: (200, {}, b"not json"), gecko=lambda m, u, b: (429, {}, b""))
    out = ingest.ingest_mint(conn, live(settings), "So11111111111111111111111111111111111111112", clients)
    assert out["stored"]["market"] == 0 and {e["kind"] for e in out["errors"]} >= {"bad_json", "rate_limited"}


def test_pool_reserves_are_omitted_when_they_do_not_reproduce_the_price_and_curves_are_never_derived():
    payload = {"venue": "pool", "dex_id": "pumpswap", "quote_symbol": "SOL", "price_sol": 9.9e-7, "pool_base_balance": 971816856, "pool_quote_balance": 2.3441}
    ingest.attach_reserves(payload)
    assert "quote_reserve_sol" not in payload and "reserves omitted" in payload["reserve_note"]
    curve = {"venue": "curve", "price_sol": amm.initial_curve().price}
    ingest.attach_reserves(curve)
    assert "quote_reserve_sol" not in curve and "liquidity_sol" not in curve     # a price alone does not reveal a curve's reserves


def curve_account(*, virtual_tokens=1_073_000_000.0, virtual_sol=30.0, real_tokens=793_100_000.0, real_sol=0.0, complete=False, mayhem=False,
                  quote="1" * 32):
    raw = (b"\x17" * 8 + struct.pack("<QQQQQ", round(virtual_tokens * 1e6), round(virtual_sol * 1e9), round(real_tokens * 1e6), round(real_sol * 1e9),
                                      10**15)
           + bytes([complete]) + b"\x09" * 32 + bytes([mayhem, 0]) + solana_rpc.b58decode(quote) + b"\0" * 51)
    return {"data": [base64.b64encode(raw).decode(), "base64"], "owner": "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"}


def test_curve_account_is_decoded_exactly_and_a_mayhem_curve_is_flagged(conn, settings):
    account = curve_account(virtual_tokens=1_117_190_825.18, virtual_sol=2.8352, real_tokens=837_290_825.18, mayhem=True)
    drained = solana_rpc.decode_curve_account(account["data"][0])
    assert drained["virtual_sol"] == pytest.approx(2.8352) and drained["real_sol"] == 0.0 and drained["is_mayhem"] and drained["quote_is_sol"]
    assert solana_rpc.decode_curve_account("AAAA") is None and solana_rpc.decode_curve_account("not base64 !!") is None
    usdc = solana_rpc.decode_curve_account(curve_account(quote="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")["data"][0])
    assert usdc["quote_is_sol"] is False and usdc["virtual_sol"] is None and ingest.curve_observation(usdc, CURVE) is None
    assert ingest.curve_observation({**drained, "complete": True}, CURVE) is None

    def rpc(method, url, body):
        if body["method"] == "getMultipleAccounts" and body["params"][1].get("encoding") == "base64":
            return 200, {}, {"result": {"value": [account]}}
        if body["method"] == "getSignaturesForAddress":
            return 200, {}, {"result": []}
        return 200, {}, {"error": {"code": 429, "message": "method limit 0"}}

    out = ingest.ingest_mint(conn, live(settings), MINT, make_clients(rpc=rpc))
    assert out["stored"]["market"] == 3
    exact = next(o for o in db.observations(conn, MINT, "market") if o["provider"] == "solana_rpc")["payload"]
    assert exact["quote_reserve_sol"] == pytest.approx(2.8352) and exact["liquidity_sol"] == 0.0 and exact["is_mayhem"] is True
    assert exact["price_sol"] == pytest.approx(2.8352 / 1_117_190_825.18) and "account read on-chain" in exact["reserve_model"]
    liquidity = next(c for c in risk.risk_report(conn, MINT)["components"] if c["name"] == "liquidity")
    assert any("Mayhem mode" in e for e in liquidity["evidence"])


def test_discover_imports_only_bonding_curve_pools_and_reports_the_gap(conn, settings):
    data = gecko_pools()
    clients = make_clients(gecko=lambda m, u, b: (200, {}, data))
    out = ingest.discover(conn, live(settings), clients)
    assert out["added"] == 1 and "missed" in out["coverage_note"]
    token = dict(conn.execute("SELECT * FROM tokens").fetchone())
    assert token["mint"] == MINT and "bonding-curve pool" in token["launch_source"]
    with pytest.raises(ProviderError):
        ingest.discover(conn, settings, clients)                 # demo mode


def test_raw_snapshots_follow_the_per_provider_switch_and_redact_the_rpc_url(conn, settings):
    secret_url = "https://rpc.example.com/v1/SECRETTOKEN?api-key=ALSOSECRET"
    on = dataclasses.replace(live(settings), solana_rpc_url=secret_url, store_raw={"solana_rpc": True, "dexscreener": True, "geckoterminal": False})
    clients = make_clients()
    ingest.ingest_mint(conn, on, MINT, clients)
    rows = [dict(r) for r in conn.execute("SELECT provider, url, sha256, body FROM raw_snapshots")]
    assert {r["provider"] for r in rows} == {"dexscreener", "solana_rpc"}          # geckoterminal switch is off
    assert all(len(r["sha256"]) == 64 and r["body"] for r in rows)
    rpc_rows = [r for r in rows if r["provider"] == "solana_rpc"]
    assert rpc_rows and all("SECRET" not in r["url"] and r["url"].startswith("https://rpc.example.com/") for r in rpc_rows)
    assert any(r["url"].endswith("#getSignaturesForAddress") for r in rpc_rows)
    assert clients.rpc.on_fetch is None                                             # hook is removed after the ingest


def test_watch_cycle_discovers_ingests_and_records_a_signal_without_guessing(conn, settings):
    now = 1795207513.0 + 3600                                     # the launch was an hour ago; we only see it now
    out = ingest.watch_cycle(conn, live(settings), make_clients(start=now), max_new=1, now=now)
    assert out["discovered"] == 1 and out["ingested"] == [MINT]
    assert out["paper"]["new_signals"] == 1
    signal = dict(conn.execute("SELECT * FROM signals WHERE book = 'live'").fetchone())
    assert signal["decision"] == "rejected"            # no price was observed at decision time -> not a candidate
    assert "no_price" in signal["reasons"] and "launch_unknown" in signal["reasons"]
    assert conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0] == 0


def test_a_dust_pool_never_describes_the_token(conn, settings):
    rel = {"base_token": {"data": {"id": "solana_" + MINT}}}
    pools = gecko_pools()
    pools["data"].append({"attributes": {"address": "DustPool1111111111111111111111111111111111111", "name": "BTC / SOL", "base_token_price_usd": "0.00104474",
                                         "base_token_price_native_currency": "0.00001311", "fdv_usd": "1040000", "reserve_in_usd": "0.0000003648"},
                          "relationships": {**rel, "dex": {"data": {"id": "meteora-damm-v2"}}}})
    ingest.ingest_mint(conn, live(settings), MINT, make_clients(gecko=lambda m, u, b: (200, {}, pools)))
    dust = next(o for o in db.observations(conn, MINT, "market") if o["payload"]["pool_address"].startswith("DustPool"))
    assert dust["payload"]["negligible_liquidity"] is True and any("usable price" in m for m in dust["missing"])
    chosen = risk.latest_market(conn, MINT, None)
    assert chosen["provider"] == "dexscreener" and chosen["payload"]["price_sol"] == 2.062e-8      # not the $1.04M dust quote
    assert not risk.usable_price(dust)
