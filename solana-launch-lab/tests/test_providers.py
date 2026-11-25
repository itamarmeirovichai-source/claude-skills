"""Provider adapters against scripted HTTP responses: errors, rate limits, missing fields, bad data."""

import pytest
from conftest import FakeClock, FakeTransport

from launchlab.providers import dexscreener, geckoterminal, solana_rpc
from launchlab.providers.base import HttpClient, ProviderError, num

MINT = "CUfphqswgDK3VP3FX7CiShVCTdGQneFusYRFViABpump"
CURVE = "ACUSZ93rMjtPKGwZFkWa9tBNKjYSCeQeexsJYc84tY41"
POOL = "5q1eZo7m3NjacXmSuM8BZZ8iqzGt8eqU9FtqTNus7aoJ"


def client(script, **kw):
    clock = FakeClock()
    transport = FakeTransport(script)
    c = HttpClient(provider="test", min_interval_s=1.0, transport=transport, sleep=clock.sleep, clock=clock.time, **kw)
    return c, transport, clock


def test_success_and_rate_limit_spacing():
    c, _, clock = client([(200, {}, {"ok": 1}), (200, {}, {"ok": 2})])
    assert c.request_json("https://example.test/a").data == {"ok": 1}
    assert c.request_json("https://example.test/b").data == {"ok": 2}
    assert clock.sleeps == [1.0]                       # second call waited for the minimum interval


def test_429_backs_off_then_succeeds_and_honours_retry_after():
    c, transport, clock = client([(429, {"Retry-After": "7"}, b""), (200, {}, {"ok": True})])
    assert c.request_json("https://example.test/").data == {"ok": True}
    assert 7.0 in clock.sleeps and len(transport.calls) == 2


def test_persistent_429_raises_and_sets_a_cooldown_without_hammering():
    c, transport, clock = client(lambda m, u, b: (429, {}, b""), max_retries=2)
    with pytest.raises(ProviderError) as err:
        c.request_json("https://example.test/")
    assert err.value.kind == "rate_limited" and err.value.retry_at > clock.time()
    calls = len(transport.calls)
    with pytest.raises(ProviderError) as again:
        c.request_json("https://example.test/")
    assert again.value.kind == "rate_limited" and len(transport.calls) == calls   # refused locally, no new request


def test_http_errors_timeouts_and_bad_json():
    c, _, _ = client([(404, {}, b"")])
    with pytest.raises(ProviderError) as e:
        c.request_json("https://example.test/")
    assert e.value.kind == "not_found"
    c, transport, _ = client([(503, {}, b""), (500, {}, b""), (200, {}, {"ok": 1})])
    assert c.request_json("https://example.test/").data == {"ok": 1} and len(transport.calls) == 3
    c, _, _ = client([(200, {}, b"<html>not json</html>")])
    with pytest.raises(ProviderError) as e:
        c.request_json("https://example.test/")
    assert e.value.kind == "bad_json"
    c, _, _ = client(lambda m, u, b: TimeoutError("slow"), max_retries=1)
    with pytest.raises(ProviderError) as e:
        c.request_json("https://example.test/")
    assert e.value.kind == "timeout"
    c, transport, _ = client([(200, {}, {})], enabled=False)
    with pytest.raises(ProviderError) as e:
        c.request_json("https://example.test/")
    assert e.value.kind == "disabled" and transport.calls == []           # demo mode: no request leaves the process


def test_num_never_guesses():
    assert num("1.5") == 1.5 and num(2) == 2.0
    for bad in (None, "", "abc", True, float("nan"), float("inf"), [], {}):
        assert num(bad) is None


def test_dexscreener_normalisation_keeps_definitions_and_flags_missing_fields():
    pair = {"dexId": "pumpswap", "pairAddress": POOL, "url": "https://dexscreener.com/solana/x",
            "baseToken": {"address": MINT, "name": "BartCoin", "symbol": "BTC"}, "quoteToken": {"symbol": "SOL"},
            "priceNative": "0.00000002062", "priceUsd": "0.000001448", "fdv": 1444, "marketCap": 1444,
            "liquidity": {"usd": 1572.35, "base": 971816856, "quote": 2.3441}, "volume": {"h24": 40.78}, "pairCreatedAt": 1795207513000}
    out = dexscreener.normalize_response([pair], MINT)[0]
    assert out["price_sol"] == 2.062e-8 and out["venue"] == "pool" and out["missing"] == []
    assert out["sol_usd"] == pytest.approx(70.22, abs=0.01)
    assert "undefined in provider docs" in out["market_cap_definition"] and out["fdv_usd"] == 1444
    assert out["pair_created_at"] == 1795207513.0
    curve = {**pair, "dexId": "pumpfun", "liquidity": None, "fdv": None}
    out = dexscreener.normalize_response([curve], MINT)[0]
    assert out["venue"] == "curve" and out["liquidity_usd"] is None and set(out["missing"]) == {"fdv_usd", "liquidity_usd"}
    # a pair where our mint is the QUOTE side, or a different token with the same ticker, is not this token
    other = {**pair, "baseToken": {"address": "SomeOtherMint1111111111111111111111111111111", "symbol": "BTC"}}
    assert dexscreener.normalize_response([other], MINT) == []
    assert dexscreener.normalize_response({"unexpected": "shape"}, MINT) == []
    assert dexscreener.normalize_response([None, 5, "x"], MINT) == []


def test_geckoterminal_pools_and_candles():
    data = {"data": [
        {"attributes": {"address": POOL, "name": "BTC / SOL", "pool_created_at": "2026-11-20T20:45:13Z", "base_token_price_usd": "0.0000014",
                        "fdv_usd": "1433.96", "market_cap_usd": None, "reserve_in_usd": "1568.04"},
         "relationships": {"dex": {"data": {"id": "pumpswap"}}, "base_token": {"data": {"id": "solana_" + MINT}}}},
        {"attributes": {"address": CURVE, "name": "BTC / SOL", "pool_created_at": "2026-11-20T20:45:13Z", "reserve_in_usd": "0.0"},
         "relationships": {"dex": {"data": {"id": "pump-fun"}}, "base_token": {"data": {"id": "solana_" + MINT}}}},
        {"attributes": {"address": "x", "name": "babymaya / BTC"},
         "relationships": {"dex": {"data": {"id": "pump-fun"}}, "base_token": {"data": {"id": "solana_other"}}}},
    ]}
    pools = geckoterminal.normalize_pools(data, MINT)
    assert [p["venue"] for p in pools] == ["pool", "curve"]                 # the pool where our mint is only the quote is dropped
    assert pools[0]["market_cap_usd"] is None and "null unless verified" in pools[0]["market_cap_definition"]
    assert pools[0]["pool_created_at"] == 1795207513.0
    candles = geckoterminal.normalize_ohlcv({"data": {"attributes": {"ohlcv_list": [
        [120, 2, 3, 1, 2.5, 10], [60, 1, 2, 0.5, 2, 5], [180, None, 1, 1, 1, 1], [240, 1, 1, 0, 1, 1], "junk", [300, 1]]}}})
    assert [c["t"] for c in candles] == [60, 120]                           # sorted; null, non-positive and short rows dropped
    assert geckoterminal.normalize_ohlcv({}) == [] and geckoterminal.normalize_ohlcv(None) == []
    with pytest.raises(ValueError):
        geckoterminal.fetch_ohlcv(None, POOL, timeframe="second")


def test_rpc_allowlist_refuses_anything_that_could_write():
    c, transport, _ = client([(200, {}, {"result": "ok"})])
    for method in ("sendTransaction", "sendRawTransaction", "simulateTransaction", "requestAirdrop", "signTransaction", "getProgramAccountsX"):
        with pytest.raises(ProviderError) as err:
            solana_rpc.call(c, "https://rpc.test", method, [])
        assert err.value.kind == "forbidden_method"
    assert transport.calls == []                                            # refused before any request is built
    assert not any(m.startswith(("send", "sign", "simulate", "request")) for m in solana_rpc.READ_METHODS)
    assert solana_rpc.call(c, "https://rpc.test", "getHealth", []).data == {"result": "ok"}
    assert transport.calls[0][2]["method"] == "getHealth"


def test_rpc_error_payloads_become_provider_errors():
    c, _, _ = client([(200, {}, {"error": {"code": -32015, "message": "Transaction version (1) is not supported"}})])
    with pytest.raises(ProviderError) as err:
        solana_rpc.call(c, "https://rpc.test", "getTransaction", ["sig"])
    assert err.value.kind == "http" and "version" in err.value.message
    c, _, _ = client([(200, {}, {"error": {"code": 429, "message": "Too many requests"}})])
    with pytest.raises(ProviderError) as err:
        solana_rpc.call(c, "https://rpc.test", "getSlot", [])
    assert err.value.kind == "rate_limited"


def tx(signers, deltas, logs, inner=None, block_time=1795207513):
    keys = [{"pubkey": s, "signer": True} for s in signers] + [{"pubkey": CURVE, "signer": False}]
    post = [{"mint": MINT, "owner": owner, "uiTokenAmount": {"uiAmountString": str(amount)}} for owner, amount in deltas.items()]
    return {"blockTime": block_time, "slot": 471875967, "transaction": {"message": {"accountKeys": keys}},
            "meta": {"err": None, "logMessages": [f"Program log: Instruction: {name}" for name in logs],
                     "preTokenBalances": [], "postTokenBalances": post, "innerInstructions": inner or []}}


def test_launch_structure_is_read_from_creation_slot_transactions():
    sigs = [{"signature": "later", "slot": 471876109, "err": None}, {"signature": "failed", "slot": 471875967, "err": {"x": 1}},
            {"signature": "migrate", "slot": 471875967, "err": None}, {"signature": "buy2", "slot": 471875967, "err": None},
            {"signature": "create", "slot": 471875967, "err": None}]          # newest first, as the RPC returns them
    txs = {
        "create": tx(["creator", "w1", MINT], {"creator": 1_410_000, "w1": 2_110_000, CURVE: 996_480_000}, ["CreateV2", "BuyV3"]),
        "buy2": tx(["w2", "w3"], {"w2": 395_000_000, "w3": 394_580_000}, ["BuyV3"]),
        "migrate": tx(["creator", "w4"], {"w4": 36_120_000, POOL: 170_780_000}, ["MigrateV2", "CreatePool"],
                      inner=[{"instructions": [{"parsed": {"type": "mintTo", "info": {"amount": "4193388282504"}}},
                                               {"parsed": {"type": "burn", "info": {"amount": "4193388282504"}}}]}]),
    }

    def script(method, url, body):
        if body["method"] == "getSignaturesForAddress":
            return 200, {}, {"result": sigs}
        return 200, {}, {"result": txs[body["params"][0]]}

    c, transport, _ = client(script)
    out = solana_rpc.read_launch_structure(c, "https://rpc.test", CURVE, MINT)
    assert out["status"] == "known" and out["creation_slot"] == 471875967 and out["creator"] == "creator"
    assert out["creation_time"] == 1795207513
    assert out["slot0_tokens_bought"] == pytest.approx(829_220_000) and out["slot0_share"] == pytest.approx(0.82922)
    assert out["creator_share_at_launch"] == pytest.approx(0.00141)
    assert sorted(len(g) for g in out["cosigner_groups"]) == [2, 2]          # co-signers of one transaction
    assert out["migrated_in_creation_slot"] is True and out["lp_burned_at_migration"] is True
    assert out["slot0_failed_tx_count"] == 1
    assert {b["wallet"] for b in out["slot0_buyers"]} == {"creator", "w1", "w2", "w3", "w4"}   # pool and curve are not buyers
    assert all(call[2]["params"][0] != "later" for call in transport.calls if call[2]["method"] == "getTransaction")


def test_launch_structure_says_unknown_when_history_is_too_long_or_missing():
    page = [{"signature": f"s{i}", "slot": 10_000 - i, "err": None} for i in range(1000)]
    c, _, _ = client(lambda m, u, b: (200, {}, {"result": page}))
    out = solana_rpc.read_launch_structure(c, "https://rpc.test", CURVE, MINT, max_pages=2)
    assert out["status"] == "unknown" and "not reached" in out["reason"] and "slot0_share" not in out
    c, _, _ = client(lambda m, u, b: (200, {}, {"result": []}))
    assert solana_rpc.read_launch_structure(c, "https://rpc.test", CURVE, MINT)["status"] == "unknown"


def test_first_funders_are_one_hop_and_only_shared_ones_are_reported():
    def script(method, url, body):
        if body["method"] == "getSignaturesForAddress":
            wallet = body["params"][0]
            if wallet == "busy":
                return 200, {}, {"result": [{"signature": f"s{i}", "slot": i} for i in range(1000)]}   # too long to trace
            return 200, {}, {"result": [{"signature": "last-" + wallet, "slot": 9}, {"signature": "first-" + wallet, "slot": 1}]}
        wallet = body["params"][0].split("-", 1)[1]
        payer = {"w1": "funderA", "w2": "funderA", "w3": "funderB", "self": "self"}[wallet]
        return 200, {}, {"result": {"transaction": {"message": {"accountKeys": [{"pubkey": payer, "signer": True}, {"pubkey": wallet}]}}}}

    c, transport, _ = client(script)
    out = solana_rpc.read_first_funders(c, "https://rpc.test", ["w1", "w2", "w3", "self", "busy"])
    assert out["first_funders_checked"] == 4 and out["first_funders_skipped"] == 1
    assert out["shared_first_funders"] == [{"funder": "funderA", "count": 2, "wallets": ["w1", "w2"]}]   # single-use funders are not "links"
    assert all(call[2]["params"][0].startswith("first-") for call in transport.calls if call[2]["method"] == "getTransaction")
