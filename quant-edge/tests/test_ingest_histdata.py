"""HistData loader (batch 1b extensions) and its outcome-free QA helpers, on synthetic inputs only."""
import io
import zipfile

import numpy as np
import pandas as pd
import pytest

from qe import paths
from qe.ingest import common, histdata
from qe.qa import clock as qclock
from qe.qa import histdata_qa


def test_parse_periods_and_form():
    html = ('<a href="/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/spxusd/2026/10">x</a>'
            '<a href="/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/spxusd/2026/9">x</a>'
            '<a href="/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/spxusd/2025">x</a>'
            '<a href="/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/eurusd/2024">x</a>')
    assert histdata.parse_periods(html, "SPXUSD") == [(2025, None), (2026, 9), (2026, 10)]
    form = histdata.parse_form('<input type="hidden" name="tk" id="tk" value="ab12" />'
                               '<input type="hidden" name="datemonth" id="datemonth" value="202610" />'
                               '<input type="hidden" name="tk" id="tk" value="zz" />')
    assert form == {"tk": "ab12", "datemonth": "202610"}


def test_raw_zip_path_routes_holdout_years(monkeypatch, tmp_path):
    monkeypatch.setattr(common, "DATA_ROOT", tmp_path)
    monkeypatch.setattr(common, "RAW", tmp_path / "raw")
    assert histdata.raw_zip_path("SPXUSD", 2024).parent == tmp_path / "raw" / "histdata" / "SPXUSD"
    p = histdata.raw_zip_path("SPXUSD", 2026, 3)
    assert p.parent == tmp_path / "holdout" / "raw" / "histdata" / "SPXUSD"
    assert p.name == "HISTDATA_COM_ASCII_SPXUSD_M1_202603.zip"


def test_to_utc_histdata_rule_mismatch_weeks():
    local = pd.DataFrame({"local": pd.to_datetime(["2018-03-15 08:30", "2022-03-15 08:30", "2022-07-15 08:30", "2022-01-14 08:30"]),
                          "open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0, "volume": 0})
    ny = histdata.to_utc(local, "ny_dst")["ts"].dt.strftime("%m-%d %H:%M").tolist()
    rule = histdata.to_utc(local, "histdata_rule")["ts"].dt.strftime("%m-%d %H:%M").tolist()
    assert ny == ["03-15 12:30", "03-15 12:30", "07-15 12:30", "01-14 13:30"]
    # 2018 keeps the NY rule; 2022 mismatch week (US on DST, EU not) is UTC-5 on the EU rule; aligned weeks agree
    assert rule == ["03-15 12:30", "03-15 13:30", "07-15 12:30", "01-14 13:30"]


def _spiky_local(spikes_clock_minutes_by_season, years=(2016, 2017), seed=0):
    """Weekday 1m bars on a naive clock with an extra |move| at the given clock minute in winter/summer months."""
    rng = np.random.default_rng(seed)
    idx = pd.date_range(f"{years[0]}-01-01", f"{years[-1]}-12-31 23:59", freq="1min")
    idx = idx[(idx.dayofweek < 5) & idx.month.isin([1, 2, 6, 7])]
    r = rng.normal(0, 1e-4, len(idx))
    mod = idx.hour * 60 + idx.minute
    for season, months in (("winter", (1, 2)), ("summer", (6, 7))):
        m = idx.month.isin(months) & (mod == spikes_clock_minutes_by_season[season])
        r[m] += 30e-4 * rng.choice([-1, 1], m.sum())
    return pd.Series(idx), pd.Series(100 * np.exp(np.cumsum(r)))


def test_diagnose_anchor_asia_and_europe():
    # Hong Kong 09:15 open on a NY-with-DST clock: 20:15 in winter, 21:15 in summer
    loc, close = _spiky_local({"winter": 20 * 60 + 15, "summer": 21 * 60 + 15})
    assert qclock.diagnose_anchor(loc, close, "Asia/Hong_Kong", 9 * 60 + 15)["verdict"] == "ny_dst"
    # the same open on a fixed-EST clock stays at 20:15
    loc, close = _spiky_local({"winter": 20 * 60 + 15, "summer": 20 * 60 + 15})
    assert qclock.diagnose_anchor(loc, close, "Asia/Hong_Kong", 9 * 60 + 15)["verdict"] == "est_fixed"
    # Frankfurt 09:00 on a fixed-EST clock moves to 02:00 in summer
    loc, close = _spiky_local({"winter": 3 * 60, "summer": 2 * 60})
    assert qclock.diagnose_anchor(loc, close, "Europe/Berlin", 9 * 60)["verdict"] == "est_fixed"
    assert qclock.combine({"verdict": "ny_dst"}, {"verdict": "unclear"}) == ("ny_dst", "single")
    assert qclock.combine({"verdict": "ny_dst"}, {"verdict": "est_fixed"}) == ("ny_dst", "conflict")


def test_diagnose_mismatch_events_votes_eu_rule():
    rng = np.random.default_rng(1)
    ev = pd.Series(pd.to_datetime(["2018-03-13 12:30", "2022-03-15 12:30", "2022-11-04 12:30"], utc=True))  # 08:30 EDT
    frames = []
    for e in ev:
        start = e.tz_convert("America/New_York").tz_localize(None) - pd.Timedelta(hours=3)
        idx = pd.date_range(start, periods=360, freq="1min")
        r = rng.normal(0, 1e-4, len(idx))
        # where the file stamps the release: NY clock in 2018, EU-rule clock (one hour earlier) in 2022
        stamp = e.tz_convert("America/New_York").tz_localize(None) - (pd.Timedelta(hours=1) if e.year >= 2019 else pd.Timedelta(0))
        r[idx == stamp] += 50e-4
        r[idx == stamp + pd.Timedelta(minutes=60)] += 30e-4     # the 09:30 cash open, one hour after the release
        frames.append(pd.DataFrame({"local": idx, "close": 100 * np.exp(np.cumsum(r))}))
    d = pd.concat(frames, ignore_index=True)
    mm = qclock.diagnose_mismatch_events(d["local"], d["close"], ev)
    assert mm["years"] == {2018: {"ny_dst": 1, "eu_dst": 0, "none": 0}, 2022: {"ny_dst": 0, "eu_dst": 2, "none": 0}}
    assert qclock.rule_check(mm) == {"agree": 3, "disagree": 0, "undecided": 0, "years_disagreeing": []}


def _zip_bytes(rows):
    csv = "\n".join(f"{t:%Y%m%d %H%M%S};{c};{c + 0.5};{c - 0.5};{c};0" for t, c in rows).encode()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("DAT_ASCII_TEST_M1.csv", csv)
    return buf.getvalue()


def test_ingest_symbol_splits_holdout(monkeypatch, tmp_path):
    monkeypatch.setattr(common, "DATA_ROOT", tmp_path)
    monkeypatch.setattr(common, "RAW", tmp_path / "raw")
    monkeypatch.setattr(common, "CALENDARS", tmp_path / "calendars")
    monkeypatch.setattr(common, "FETCH_LOG", tmp_path / "fetch_log.csv")
    man = tmp_path / "manifest.csv"
    monkeypatch.setattr(histdata, "list_periods", lambda sym: [(2024, None), (2025, None), (2026, 1)])

    def fake_download(sym, y, m=None, dry_run=False):
        p = histdata.raw_zip_path(sym, y, m)
        p.parent.mkdir(parents=True, exist_ok=True)
        start = pd.Timestamp(f"{y}-{m or 12:02d}-{'02' if m else '30'} 09:00")
        p.write_bytes(_zip_bytes([(start + pd.Timedelta(minutes=i), 100 + i * 0.01) for i in range(600)]))
        return {"path": p, "sha256": common.sha256_file(p), "status": "200"}

    monkeypatch.setattr(histdata, "download_period", fake_download)
    monkeypatch.setattr(histdata, "EXCLUDE", {"TSTUSD": [("2024-12-30 14:00", "2024-12-30 14:09", "synthetic mislabelled span")]})
    out = histdata.ingest_symbol("TSTUSD", clock="ny_dst", manifest=man, log=lambda *a: None)
    rows = {r["dataset_id"]: r for r in common.manifest_rows(man)}
    assert set(rows) == {"histdata_cfd_1m_TSTUSD", "histdata_cfd_1m_TSTUSD_holdout"}
    assert rows["histdata_cfd_1m_TSTUSD_holdout"]["path"] == "holdout/histdata_cfd_1m/TSTUSD"
    assert "HOLD-OUT" in rows["histdata_cfd_1m_TSTUSD_holdout"]["notes"]
    is_df = pd.read_parquet(tmp_path / rows["histdata_cfd_1m_TSTUSD"]["path"])
    ho_df = pd.read_parquet(tmp_path / rows["histdata_cfd_1m_TSTUSD_holdout"]["path"])
    cut = pd.Timestamp(paths.HOLDOUT_START, tz="UTC")
    assert (pd.to_datetime(is_df["ts"], utc=True) < cut).all() and len(is_df) == 590
    assert "EXCLUDED 10 bars" in rows["histdata_cfd_1m_TSTUSD"]["notes"]
    assert "EXCLUDED" not in rows["histdata_cfd_1m_TSTUSD_holdout"]["notes"]
    assert (pd.to_datetime(ho_df["ts"], utc=True) >= cut).all() and len(ho_df) == 1200
    assert (tmp_path / "holdout" / "raw" / "histdata" / "TSTUSD" / "HISTDATA_COM_ASCII_TSTUSD_M1_202601.zip").exists()
    assert out["pins"] and out["missing_periods"] == []


def test_gaps_skip_the_weekend():
    ts = pd.Series(pd.to_datetime(["2024-03-01 21:59", "2024-03-03 22:00", "2024-03-06 22:00"], utc=True))  # Fri close, Sun open, Wed
    g = histdata_qa.gaps(ts)
    assert len(g) == 1 and g.loc[0, "after"] == pd.Timestamp("2024-03-03 22:00", tz="UTC")
    assert g.loc[0, "trading_days"] == pytest.approx(3.0)
    assert histdata_qa.missing_months(pd.Series(pd.to_datetime(["2024-01-05", "2024-03-05"], utc=True))) == ["2024-02"]


def test_partitioned_reland_drops_stale_years(monkeypatch, tmp_path):
    monkeypatch.setattr(common, "DATA_ROOT", tmp_path)
    df = pd.DataFrame({"ts": pd.to_datetime(["2020-06-01", "2021-06-01", "2022-06-01"], utc=True), "close": [1.0, 2.0, 3.0]})
    common.write_parquet_partitioned(df, "derived/x")
    info = common.write_parquet_partitioned(df.iloc[[0, 2]], "derived/x")
    assert sorted(p.name for p in (tmp_path / "derived/x").iterdir()) == ["year=2020", "year=2022"]
    assert len(pd.read_parquet(tmp_path / "derived/x")) == 2 and info["sha256"] == common.sha256_tree(tmp_path / "derived/x")
