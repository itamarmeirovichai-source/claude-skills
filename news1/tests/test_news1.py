from __future__ import annotations

import ast
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest

from news1 import config, core, ledger, sessions, sources, universe
from news1.http import FetchError, Http, urllib_transport

ET = sessions.ET
DAY = date(2026, 11, 30)  # a Monday; the previous trading day is Friday 2026-11-27


def et(day: date, hour: int, minute: int = 0) -> datetime:
    return datetime(day.year, day.month, day.day, hour, minute, tzinfo=ET)


def news_item(ticker: str, when: datetime, title: str, related: list[str] | None = None) -> dict:
    return {
        "uuid": f"id-{ticker}-{int(when.timestamp())}",
        "title": title,
        "providerPublishTime": int(when.timestamp()),
        "publisher": "Wire",
        "link": f"https://example.test/{ticker}/{int(when.timestamp())}",
        "relatedTickers": related if related is not None else [ticker],
    }


def bars_payload(rows: list[tuple[date, float | None, float | None, int]]) -> dict:
    return {
        "chart": {
            "result": [
                {
                    "timestamp": [int(et(d, 9, 30).timestamp()) for d, *_ in rows],
                    "indicators": {
                        "quote": [
                            {
                                "open": [r[1] for r in rows],
                                "close": [r[2] for r in rows],
                                "volume": [r[3] for r in rows],
                            }
                        ]
                    },
                }
            ]
        }
    }


class FakeHttp:
    """Answers by ticker: news[ticker] / bars[ticker]; a ticker in `fail` raises."""

    def __init__(self, news=None, bars=None, screener=None, fail=()):
        self.news, self.bars, self.screener, self.fail = news or {}, bars or {}, screener, set(fail)
        self.calls = 0

    def get_json(self, url: str):
        self.calls += 1
        if "screener" in url:
            return self.screener
        ticker = re.search(r"(?:q=|chart/)([A-Z]+)", url).group(1)
        if ticker in self.fail:
            raise FetchError("down")
        if "search" in url:
            return {"news": self.news.get(ticker, [])}
        return self.bars[ticker]


def pending_for(tickers: dict[str, list[dict]], fetched: datetime) -> dict:
    http = FakeHttp(news=tickers)
    return core.open_fetch(http, sorted(tickers), fetched)


# ---------------------------------------------------------------- log


def test_log_chain_detects_edits_and_deletions(tmp_path):
    path = tmp_path / "ledger.jsonl"
    ledger.append(path, [{"type": "batch", "date": "2026-11-30"}, {"type": "signal", "date": "2026-11-30", "verdict": 1}])
    ledger.append(path, [{"type": "batch", "date": "2026-12-01"}])
    assert ledger.verify(path) == (True, 3, "ok")

    lines = path.read_text().splitlines()
    path.write_text("\n".join([lines[0], lines[1].replace('"verdict":1', '"verdict":-1'), lines[2]]) + "\n")
    ok, _, message = ledger.verify(path)
    assert not ok and "line 2" in message

    path.write_text("\n".join([lines[0], lines[2]]) + "\n")
    ok, _, message = ledger.verify(path)
    assert not ok and "broken link" in message


def test_log_rejects_reserved_fields(tmp_path):
    with pytest.raises(ValueError):
        ledger.append(tmp_path / "l.jsonl", [{"hash": "x"}])


# ---------------------------------------------------------------- time


def test_trading_days_and_window():
    assert not sessions.is_trading_day(date(2026, 11, 26))  # Thanksgiving
    assert not sessions.is_trading_day(date(2026, 11, 28))  # Saturday
    start, end = sessions.window(DAY)
    assert start == et(date(2026, 11, 27), 16) and end == et(DAY, 9)
    start, _ = sessions.window(date(2026, 11, 27))
    assert start == et(date(2026, 11, 25), 16)  # skips the holiday


# ---------------------------------------------------------------- fetch


def test_fetch_keeps_only_window_items_about_the_ticker():
    friday = date(2026, 11, 27)
    items = [
        news_item("AAA", et(friday, 15, 59), "before the window"),
        news_item("AAA", et(friday, 16, 1), "in 1"),
        news_item("AAA", et(DAY, 6), "in 2"),
        news_item("AAA", et(DAY, 7), "in 3"),
        news_item("AAA", et(DAY, 8), "in 4"),
        news_item("AAA", et(DAY, 8, 50), "after the fetch"),
        news_item("AAA", et(DAY, 7, 30), "about another company", related=["ZZZ"]),
    ]
    http = FakeHttp(news={"AAA": items, "BBB": []}, fail=["CCC"])
    pending = core.open_fetch(http, ["AAA", "BBB", "CCC"], et(DAY, 8, 40))
    assert [i["title"] for i in pending["tickers"]["AAA"]] == ["in 4", "in 3", "in 2"]
    assert "BBB" not in pending["tickers"] and pending["errors"] == ["CCC"]
    assert pending["date"] == "2026-11-30" and pending["universe_size"] == 3


def test_fetch_never_reads_past_nine_even_if_run_late():
    items = [news_item("AAA", et(DAY, 8, 59), "in"), news_item("AAA", et(DAY, 9, 5), "late")]
    pending = core.open_fetch(FakeHttp(news={"AAA": items}), ["AAA"], et(DAY, 9, 20))
    assert [i["title"] for i in pending["tickers"]["AAA"]] == ["in"]


def test_fetch_refuses_closed_days():
    with pytest.raises(core.Refused):
        core.open_fetch(FakeHttp(), ["AAA"], et(date(2026, 11, 28), 8, 40))


# ---------------------------------------------------------------- record


@pytest.fixture
def pending():
    return pending_for(
        {"AAA": [news_item("AAA", et(DAY, 7), "AAA wins contract")], "BBB": [news_item("BBB", et(DAY, 7), "BBB recalls product")]},
        et(DAY, 8, 40),
    )


def test_record_writes_batch_and_signals_without_titles(tmp_path, pending):
    path = tmp_path / "ledger.jsonl"
    written = core.record(pending, {"AAA": 1, "BBB": -1}, "model-x", et(DAY, 8, 45), path, "sha")
    assert [e["type"] for e in written] == ["batch", "signal", "signal"]
    assert written[0]["model"] == "model-x" and written[0]["prompt_sha"] == "sha"
    assert {e["ticker"]: e["verdict"] for e in written[1:]} == {"AAA": 1, "BBB": -1}
    assert "wins contract" not in path.read_text()
    assert ledger.verify(path)[0]


def test_record_refused_from_the_deadline(tmp_path, pending):
    with pytest.raises(core.Refused, match="too late"):
        core.record(pending, {"AAA": 1, "BBB": -1}, "m", et(DAY, 9, 25), tmp_path / "l.jsonl", "sha")
    assert not (tmp_path / "l.jsonl").exists()


def test_record_refused_for_stale_duplicate_or_future_files(tmp_path, pending):
    path = tmp_path / "l.jsonl"
    with pytest.raises(core.Refused, match="another day"):
        core.record(pending, {"AAA": 1, "BBB": -1}, "m", et(DAY + timedelta(days=1), 8, 45), path, "sha")
    with pytest.raises(core.Refused, match="future"):
        core.record(pending, {"AAA": 1, "BBB": -1}, "m", et(DAY, 8, 30), path, "sha")
    core.record(pending, {"AAA": 1, "BBB": -1}, "m", et(DAY, 8, 45), path, "sha")
    with pytest.raises(core.Refused, match="already"):
        core.record(pending, {"AAA": 1, "BBB": -1}, "m", et(DAY, 8, 50), path, "sha")


@pytest.mark.parametrize("verdicts", [{"AAA": 1}, {"AAA": 1, "BBB": 0, "CCC": 1}, {"AAA": 2, "BBB": 0}, {"AAA": True, "BBB": 0}, {"AAA": "1", "BBB": 0}])
def test_record_refuses_incomplete_or_invalid_verdicts(tmp_path, pending, verdicts):
    with pytest.raises(core.Refused):
        core.record(pending, verdicts, "m", et(DAY, 8, 45), tmp_path / "l.jsonl", "sha")


# ---------------------------------------------------------------- settle and statistics


def recorded(tmp_path, verdicts: dict[str, int], day: date = DAY) -> Path:
    path = tmp_path / "ledger.jsonl"
    pend = pending_for({t: [news_item(t, et(day, 7), "x")] for t in verdicts}, et(day, 8, 40))
    core.record(pend, verdicts, "m", et(day, 8, 45), path, "sha")
    return path


def test_settle_uses_open_to_close_and_signs_shorts(tmp_path):
    path, results = recorded(tmp_path, {"AAA": 1, "BBB": -1, "CCC": 0}), tmp_path / "results.jsonl"
    bars = {
        "AAA": bars_payload([(DAY, 100.0, 102.0, 1)]),
        "BBB": bars_payload([(DAY, 50.0, 49.0, 1)]),
    }
    assert core.settle(FakeHttp(bars=bars), path, results, et(DAY, 16, 19)) == []  # day not over
    rows = core.settle(FakeHttp(bars=bars), path, results, et(DAY, 16, 20))
    assert {r["ticker"]: round(r["ret"], 4) for r in rows} == {"AAA": 0.02, "BBB": -0.02}
    assert core.settle(FakeHttp(bars=bars), path, results, et(DAY, 17)) == []  # nothing twice

    s = core.stats(path, results)
    assert s["settled_trades"] == 2 and s["unclear"] == 1
    assert s["gross"]["mean"] == pytest.approx((0.02 + 0.02) / 2)  # the short gained 2%
    assert s["net"]["mean"] == pytest.approx(0.02 - 2 * config.COST_PER_SIDE)
    assert s["net_high_cost"]["mean"] == pytest.approx(0.02 - 2 * 0.001)
    assert s["decision"].startswith("stage 1 running: 1 of 60")


def test_settle_waits_for_prices_and_marks_missing_sessions(tmp_path):
    path, results = recorded(tmp_path, {"AAA": 1, "BBB": 1}), tmp_path / "results.jsonl"
    friday, tuesday = date(2026, 11, 27), date(2026, 12, 1)
    bars = {
        "AAA": bars_payload([(friday, 10.0, 10.0, 1)]),  # Monday's bar not published yet
        "BBB": bars_payload([(friday, 10.0, 10.0, 1), (tuesday, 10.0, 11.0, 1)]),  # Monday missing for good
    }
    rows = core.settle(FakeHttp(bars=bars), path, results, et(tuesday, 17))
    assert [(r["ticker"], r["status"]) for r in rows] == [("BBB", "no_bar")]
    assert core.stats(path, results)["no_bar"] == 1


def test_settle_retries_after_a_failed_fetch(tmp_path):
    path, results = recorded(tmp_path, {"AAA": 1}), tmp_path / "results.jsonl"
    assert core.settle(FakeHttp(fail=["AAA"]), path, results, et(DAY, 17)) == []
    rows = core.settle(FakeHttp(bars={"AAA": bars_payload([(DAY, 10.0, 10.5, 1)])}), path, results, et(DAY, 17))
    assert rows[0]["status"] == "ok"


def write_days(tmp_path, daily: list[float]) -> tuple[Path, Path]:
    path, results = tmp_path / "ledger.jsonl", tmp_path / "results.jsonl"
    bodies, rows = [], []
    for i, ret in enumerate(daily):
        day = f"d{i:03d}"
        bodies += [{"type": "batch", "date": day}, {"type": "signal", "date": day, "ticker": "AAA", "verdict": 1}]
        rows.append({"date": day, "ticker": "AAA", "verdict": 1, "status": "ok", "ret": ret})
    ledger.append(path, bodies)
    results.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return path, results


def test_stage_decisions(tmp_path):
    cost = 2 * config.COST_PER_SIDE
    losing = core.stats(*write_days(tmp_path / "a", [cost] * 60))  # exactly zero after costs
    assert losing["decision"].startswith("CLOSED: stage 1")
    winning = core.stats(*write_days(tmp_path / "b", [0.004, 0.002] * 40))
    assert winning["decision"].startswith("stage 2 running: 80 of 250")
    strong = core.stats(*write_days(tmp_path / "c", [0.004, 0.002] * 125))
    assert strong["decision"].startswith("PASSED") and strong["net"]["t"] > config.STAGE2_T
    weak = core.stats(*write_days(tmp_path / "d", [0.03, -0.0265] * 125))
    assert weak["net"]["mean"] > 0 and weak["decision"].startswith("CLOSED: t below")


def test_stage_one_is_judged_on_the_first_sixty_days_only(tmp_path):
    s = core.stats(*write_days(tmp_path, [-0.01] * 60 + [0.05] * 40))
    assert s["net"]["mean"] > 0 and s["decision"].startswith("CLOSED: stage 1")


# ---------------------------------------------------------------- universe


def row(symbol, name, price=50.0, volume=1_000_000, country="United States"):
    return {"symbol": symbol, "name": name, "price": price, "volume": volume, "country": country}


def test_universe_first_pass():
    rows = [
        row("UAL", "United Airlines Holdings, Inc. Common Stock"),
        row("ABCW", "ABC Corp Warrants"),
        row("ABCU", "ABC Corp Units, each consisting of one Common Stock and one Warrant"),
        row("FOR", "Foreign Corp Common Stock", country="Israel"),
        row("PEN", "Penny Corp Common Stock", price=4.99),
        row("THIN", "Thin Corp Common Stock", volume=100_000),
        row("BRK/B", "Berkshire Class B Common Stock"),
        row("ADR", "Some Corp American Depositary Shares each representing Common Shares"),
        row("NOPX", "Nameless Corp", price=None),
    ]
    assert [r["symbol"] for r in universe.eligible(rows)] == ["UAL"]


def test_universe_order_is_fixed_by_the_seed_only():
    symbols = ["AAA", "BBB", "CCC", "DDD", "EEE"]
    assert universe.ordered(symbols) == universe.ordered(list(reversed(symbols)))
    assert universe.ordered(symbols, "other seed") != universe.ordered(symbols)


def test_universe_build_confirms_liquidity_on_bars():
    days = [date(2026, 10, 1) + timedelta(days=i) for i in range(25)]
    liquid = bars_payload([(d, 50.0, 50.0, 1_000_000) for d in days])
    thin = bars_payload([(d, 50.0, 50.0, 100_000) for d in days])
    short = bars_payload([(d, 50.0, 50.0, 1_000_000) for d in days[:5]])
    names = {s: f"{s} Corp Common Stock" for s in ("AAA", "BBB", "CCC", "DDD")}
    screener = {"data": {"rows": [{"symbol": s, "name": n, "country": "United States", "lastsale": "$50.00", "volume": "1,000,000"} for s, n in names.items()]}}
    http = FakeHttp(bars={"AAA": liquid, "BBB": thin, "CCC": short}, screener=screener, fail=["DDD"])
    built = universe.build(http)
    assert [t["symbol"] for t in built["tickers"]] == ["AAA"]
    assert built["first_pass"] == 4 and built["checked"] == 4 and built["tickers"][0]["adv_usd"] == 50_000_000


# ---------------------------------------------------------------- http and safety


def test_http_retries_then_gives_up():
    answers = iter([(429, b""), (200, b'{"ok": 1}')])
    waits: list[float] = []
    http = Http(transport=lambda *_: next(answers), sleep=waits.append, clock=lambda: 0.0)
    assert http.get_json("https://x.test/a") == {"ok": 1} and http.calls == 2 and 2.0 in waits
    with pytest.raises(FetchError, match="404"):
        Http(transport=lambda *_: (404, b""), sleep=lambda _: None).get_json("https://x.test/a")
    always = Http(transport=lambda *_: (503, b""), sleep=lambda _: None)
    with pytest.raises(FetchError, match="503"):
        always.get_json("https://x.test/a")
    assert always.calls == 4


def test_transport_is_https_only():
    with pytest.raises(ValueError):
        urllib_transport("http://x.test", {}, 1.0)


def test_sources_parse_provider_payloads():
    http = FakeHttp(news={"AAA": [news_item("AAA", et(DAY, 7), "t"), {"title": None}]}, bars={"AAA": bars_payload([(DAY, 1.0, 2.0, 3)])})
    assert sources.news(http, "AAA")[0]["related"] == ["AAA"] and len(sources.news(http, "AAA")) == 1
    assert sources.bars(http, "AAA") == [{"date": "2026-11-30", "open": 1.0, "close": 2.0, "volume": 3}]


ALLOWED_IMPORTS = {
    "__future__", "argparse", "collections", "datetime", "hashlib", "json", "math", "os", "pathlib", "re",
    "statistics", "sys", "time", "typing", "urllib", "zoneinfo",
}  # fmt: skip
FORBIDDEN = re.compile(r"api[_-]?key|secret|password|private[_-]?key|seed phrase|method=\"(POST|PUT|DELETE|PATCH)\"|submit_order|place_order", re.I)


def test_source_has_no_keys_orders_or_third_party_imports():
    for path in sorted((config.ROOT / "news1").glob("*.py")):
        text = path.read_text(encoding="utf-8")
        assert not FORBIDDEN.search(text), path.name
        for node in ast.walk(ast.parse(text)):
            if isinstance(node, ast.Import):
                roots = {alias.name.split(".")[0] for alias in node.names}
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                roots = {(node.module or "").split(".")[0]}
            else:
                continue
            assert roots <= ALLOWED_IMPORTS, f"{path.name}: {roots - ALLOWED_IMPORTS}"
