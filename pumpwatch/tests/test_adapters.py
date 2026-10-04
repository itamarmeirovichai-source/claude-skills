"""Offline tests for pumpwatch.adapters against recorded SEC / Yahoo fixtures.

Fixtures in tests/fixtures/ are real responses recorded on 2026-10-04 and
trimmed to a few rows (see ``_fixture_note`` keys in the Yahoo files; the
AREB chart has one row deliberately nulled to mimic Yahoo's incomplete rows).
"""

from __future__ import annotations

import io
import json
from datetime import date, datetime, timezone
from pathlib import Path

from pumpwatch.adapters import edgar, market_csv
from pumpwatch.engine import Engine
from pumpwatch.models import Bar, Dataset, Filing

FIX = Path(__file__).parent / "fixtures"


def load(name: str):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# EDGAR
# ---------------------------------------------------------------------------
def test_company_tickers_map_and_padding():
    m = edgar.parse_company_tickers(load("sec_company_tickers.json"))
    assert m["AAPL"] == "0000320193"
    assert m["AREB"] == m["AREBW"] == "0001648087"
    assert edgar.cik10("320193") == "0000320193"


def test_company_tickers_exchange_layout():
    obj = {"fields": ["cik", "name", "ticker", "exchange"], "data": [[320193, "Apple Inc.", "aapl", "Nasdaq"]]}
    assert edgar.parse_company_tickers(obj) == {"AAPL": "0000320193"}


def test_item_codes_translated_and_filing_date_used():
    filings = edgar.parse_submissions(load("edgar_submissions_areb.json"), "areb")
    jan = [f for f in filings if f.form == "8-K" and f.day == date(2017, 1, 10)]
    assert len(jan) == 1  # reportDate is 2017-01-06; filingDate 2017-01-10 is the public day
    t = jan[0].title
    assert t.startswith("FORM 8-K CURRENT REPORT: entry into a material definitive agreement")
    assert "unregistered sales of equity securities" in t
    assert "amendments to articles of incorporation or bylaws; change in fiscal year" in t
    assert "name change" not in t  # never invented from item codes
    control = [f for f in filings if f.day == date(2016, 6, 15)][0]
    assert "change in control of registrant" in control.title
    assert all(f.ticker == "AREB" for f in filings)


def test_forms_verbatim_and_items_only_for_current_reports():
    filings = edgar.parse_submissions(load("edgar_submissions_areb.json"), "AREB")
    forms = {f.form for f in filings}
    assert {"S-1", "S-1/A", "424B3", "PRE 14C", "8-K"} <= forms
    effect = [f for f in filings if f.form == "EFFECT"][0]
    assert effect.title == ""  # EFFECT's items field holds "S-1,,..." - not 8-K items
    s1 = [f for f in filings if f.form == "S-1" and f.day == date(2015, 8, 4)][0]
    assert s1.title == "S-1 REGISTRATION STATEMENT"
    assert [f for f in filings if f.form == "S-1" and f.day == date(2026, 4, 3)][0].title == ""


def test_former_names_become_name_change_filing():
    filings = edgar.parse_submissions(load("edgar_submissions_areb.json"), "AREB")
    nc = [f for f in filings if f.form == edgar.NAME_CHANGE_FORM]
    assert nc == [Filing("AREB", date(2017, 1, 6), "NAME-CHANGE", "name change from CUBESCAPE INC to AMERICAN REBEL HOLDINGS INC")]


def test_cosmetic_name_change_skipped():
    obj = {"name": "Genius Group Ltd", "formerNames": [{"name": "Genius Group Limited", "from": "2021-04-06T00:00:00.000Z", "to": "2021-04-06T00:00:00.000Z"}]}
    assert edgar.name_change_filings(obj, "GNS") == []


def test_window_dedupe_and_sort():
    obj = load("edgar_submissions_areb.json")
    filings = edgar.parse_submissions(obj, "AREB", date(2016, 1, 1), date(2016, 12, 31))
    assert filings and all(date(2016, 1, 1) <= f.day <= date(2016, 12, 31) for f in filings)
    assert [f.day for f in filings] == sorted(f.day for f in filings)
    doubled = edgar.merge_filings(filings, filings)
    assert doubled == filings


def test_older_pages():
    obj = load("edgar_submissions_aapl.json")
    assert edgar.extra_page_names(obj) == ["CIK0000320193-submissions-001.json"]
    assert edgar.extra_page_names(obj, start=date(2016, 1, 1)) == []  # page ends 2015-09-08
    assert edgar.recent_coverage_start(obj) == date(2015, 9, 9)
    assert edgar.earliest_filing_date(obj) == date(1994, 1, 26)
    page = edgar.parse_submissions_page(load("edgar_submissions_aapl_page001.json"), "AAPL")
    assert len(page) == 6 and page[0].form == "CORRESP"
    assert edgar.parse_submissions_page(load("edgar_submissions_aapl_page001.json"), "AAPL", end=date(2000, 1, 1)) == [
        Filing("AAPL", date(1994, 1, 26), "424B5", "APPLE 424B5"),
        Filing("AAPL", date(1994, 1, 26), "10-Q", ""),
    ]


# ---------------------------------------------------------------------------
# Yahoo
# ---------------------------------------------------------------------------
def test_yahoo_dates_match_known_trading_days():
    bars = market_csv.parse_yahoo_chart(load("yahoo_chart_aapl.json"), "aapl")
    # First trading days of 2023 (Jan 2 was a market holiday).
    assert [b.day for b in bars] == [date(2023, 1, d) for d in (3, 4, 5, 6, 9, 10)]
    assert bars[0].ticker == "AAPL" and bars[0].volume > 1e7


def test_yahoo_null_row_skipped():
    bars = market_csv.parse_yahoo_chart(load("yahoo_chart_areb.json"), "AREB")
    days = [b.day for b in bars]
    assert len(bars) == 10 and date(2022, 2, 14) not in days
    assert days[0] == date(2022, 2, 7) and days[-1] == date(2022, 2, 22)


def test_local_date_not_utc_date():
    # 20:00 New York on 2023-01-03 (EST, UTC-5) is 01:00 UTC on 2023-01-04.
    ts = datetime(2023, 1, 4, 1, 0, tzinfo=timezone.utc).timestamp()
    assert market_csv.local_date(ts, "America/New_York") == date(2023, 1, 3)
    assert market_csv.local_date(ts, None, -18000) == date(2023, 1, 3)
    # Midnight New York = 05:00 UTC same day stays on that day.
    ts = datetime(2023, 1, 3, 5, 0, tzinfo=timezone.utc).timestamp()
    assert market_csv.local_date(ts, "America/New_York") == date(2023, 1, 3)
    # Tokyo morning is the previous UTC evening.
    ts = datetime(2023, 1, 4, 0, 0, tzinfo=timezone.utc).timestamp()
    assert market_csv.local_date(ts, "Asia/Tokyo") == date(2023, 1, 4)
    assert market_csv.local_date(ts - 1, None, 32400) == date(2023, 1, 4)


def test_yahoo_meta_and_errors():
    meta = market_csv.yahoo_meta(load("yahoo_chart_areb.json"))
    assert meta["currency"] == "USD"
    assert meta["long_name"] == "American Rebel Holdings, Inc."
    assert meta["first_trade_date"] == date(2022, 2, 7)
    assert market_csv.yahoo_error(load("yahoo_chart_areb.json")) is None
    dead = load("yahoo_chart_delisted.json")
    assert market_csv.parse_yahoo_chart(dead, "ZZZQX") == []
    assert market_csv.yahoo_meta(dead) == {}
    assert "delisted" in market_csv.yahoo_error(dead)


def test_validation_drops_bad_bars():
    d = date(2024, 1, 2)
    bars = [
        Bar("X", d, 1, 2, 0.5, 1.5, 100),
        Bar("X", d, 1, 2, 0.5, 1.5, 999),  # duplicate day
        Bar("X", date(2024, 1, 3), 1, 0.5, 2, 1, 10),  # high < low
        Bar("X", date(2024, 1, 4), 0, 1, 0, 1, 10),  # non-positive
        Bar("X", date(2024, 1, 5), 1, 1, 1, 1, -5),  # negative volume
    ]
    kept, problems = market_csv.validate_bars(bars)
    assert kept == [bars[0]]
    assert len(problems) == 4 and any("high < low" in p for p in problems)


# ---------------------------------------------------------------------------
# CSV + engine smoke test
# ---------------------------------------------------------------------------
def test_csv_round_trip(tmp_path):
    bars = market_csv.parse_yahoo_chart(load("yahoo_chart_aapl.json"), "AAPL")
    filings = edgar.parse_submissions(load("edgar_submissions_areb.json"), "AREB")
    buf = io.StringIO()
    market_csv.write_bars_csv(bars, buf)
    buf.seek(0)
    assert market_csv.read_bars_csv(buf) == bars
    path = tmp_path / "filings.csv"
    market_csv.write_filings_csv(filings, path)
    assert market_csv.read_filings_csv(path) == filings
    assert path.read_text(encoding="utf-8").splitlines()[0] == "ticker,day,form,title"


def test_load_dataset_runs_through_engine(tmp_path):
    bars = market_csv.parse_yahoo_chart(load("yahoo_chart_areb.json"), "AREB")
    bars += market_csv.parse_yahoo_chart(load("yahoo_chart_aapl.json"), "AAPL")
    filings = edgar.parse_submissions(load("edgar_submissions_areb.json"), "AREB")
    market_csv.write_bars_csv(bars, tmp_path / "bars.csv")
    market_csv.write_filings_csv(filings, tmp_path / "filings.csv")
    ds = market_csv.load_dataset(tmp_path / "bars.csv", tmp_path / "filings.csv")
    assert isinstance(ds, Dataset) and ds.tickers() == ["AAPL", "AREB"]
    runs = Engine().run(ds)
    assert set(runs) == {"AAPL", "AREB"}
    assert len(runs["AAPL"].scores) == 6
