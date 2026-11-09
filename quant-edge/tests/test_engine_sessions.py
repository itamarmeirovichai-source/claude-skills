"""qe.sessions on the stub: half days have 210 RTH bars, the DST day, the 17:59 vs 18:01 ET trading-day boundary,
roll weeks and the firm deadlines (these must stay green when Department C replaces the internals)."""
import numpy as np
import pandas as pd
import pytest

from qe import sessions
from qe.engine import bars


def _minute_grid(day_utc_start, day_utc_end):
    return pd.date_range(day_utc_start, day_utc_end, freq="1min", tz="UTC", inclusive="left")


@pytest.mark.parametrize("day", ["2024-07-03", "2024-11-29"])
def test_half_days_have_210_rth_bars(day):
    ts = _minute_grid(f"{day}T00:00:00Z", f"{day}T23:59:00Z")
    t = sessions.tag_minutes(ts, "ES")
    sel = t[t["trading_day"] == pd.Timestamp(day)]
    assert int(sel["is_rth"].sum()) == 210
    assert bool(sel["is_half_day"].all())
    assert int(sel["rth_close_minute"].iloc[0]) == 13 * 60


def test_full_day_has_390_rth_bars_and_1380_session_bars():
    ts = _minute_grid("2024-06-03T00:00:00Z", "2024-06-05T00:00:00Z")
    t = sessions.tag_minutes(ts, "ES")
    sel = t[t["trading_day"] == pd.Timestamp("2024-06-04")]
    assert int(sel["is_rth"].sum()) == 390
    assert int(sel["in_session"].sum()) == 23 * 60      # 18:00 ET to 17:00 ET


def test_dst_day_keeps_ny_minutes():
    # the trading day 2024-03-11 opens Sunday 2024-03-10 18:00 EDT = 22:00 UTC (DST began at 02:00 that morning)
    ts = _minute_grid("2024-03-10T20:00:00Z", "2024-03-11T00:00:00Z")
    t = sessions.tag_minutes(ts, "ES")
    i = int(np.argmax(t["in_session"].to_numpy()))
    assert str(ts[i]) == "2024-03-10 22:00:00+00:00"
    assert int(t["ny_minute"].iloc[i]) == 18 * 60 and int(t["tday_minute"].iloc[i]) == 0
    assert t["trading_day"].iloc[i] == pd.Timestamp("2024-03-11")
    # the Friday before (standard time): 18:00 EST = 23:00 UTC
    ts2 = _minute_grid("2024-03-07T22:00:00Z", "2024-03-08T00:00:00Z")
    t2 = sessions.tag_minutes(ts2, "ES")
    j = int(np.argmax(t2["in_session"].to_numpy()))
    assert str(ts2[j]) == "2024-03-07 23:00:00+00:00" and int(t2["ny_minute"].iloc[j]) == 18 * 60


def test_trading_day_boundary_1759_vs_1801_et():
    ts = pd.DatetimeIndex([pd.Timestamp("2024-06-04 17:59", tz=sessions.TZ_NY), pd.Timestamp("2024-06-04 18:01", tz=sessions.TZ_NY),
                           pd.Timestamp("2024-06-04 16:59", tz=sessions.TZ_NY)]).tz_convert("UTC")
    t = sessions.tag_minutes(ts, "ES")
    assert t["trading_day"].iloc[0] == pd.Timestamp("2024-06-04") and not bool(t["in_session"].iloc[0])   # after the 17:00 ET close
    assert t["trading_day"].iloc[1] == pd.Timestamp("2024-06-05") and bool(t["in_session"].iloc[1])
    assert t["trading_day"].iloc[2] == pd.Timestamp("2024-06-04") and bool(t["in_session"].iloc[2])
    assert list(t["tday_minute"]) == [1439, 1, 1379]


def test_roll_week_and_flat_by():
    d = pd.DatetimeIndex(["2024-03-11", "2024-03-15", "2024-03-18", "2024-03-19", "2024-04-15", "2024-06-21"])
    assert list(sessions.is_roll_week(d)) == [True, True, True, False, False, True]
    days = sessions.day_table("2024-11-25", "2024-11-29", "ES")
    fb = sessions.flat_by_tminute("topstep", days)
    assert fb[days.index.get_loc(pd.Timestamp("2024-11-26"))] == 1330      # 15:10 CT = 16:10 ET
    assert fb[days.index.get_loc(pd.Timestamp("2024-11-29"))] == 1140      # half day: 13:00 ET early close
    assert sessions.flat_by_tminute("mffu", days)[1] == 1330 and sessions.flat_by_tminute("bulenox", days)[1] == 1379   # 15:59 CT = 16:59 ET
    with pytest.raises(KeyError):
        sessions.flat_by_tminute("unknown-firm", days)


def test_resample_labels_by_open_and_complete_ts_is_after_last_constituent():
    b = bars.synthetic_walk("2024-06-03", "2024-06-04", sigma_per_min=0.3, seed=1, rth_only=True)
    r = bars.resample_intraday(b, 5)
    assert (r["n_bars"] == 5).all()
    assert (r["complete_ts"] - r["ts"] == pd.Timedelta(minutes=5)).all()
    assert int(r["tday_minute"].iloc[0]) == 930 and str(r["ts"].iloc[0].tz_convert(sessions.TZ_NY).time()) == "09:30:00"
    d = bars.daily_from_bars(b)
    f = bars.prior_day_features(b, d)
    assert np.isnan(f["prev_close"].iloc[0]) and f["prev_close"].iloc[-1] == d["close"].iloc[0]
    with pytest.raises(ValueError):
        bars.prior_day_features(b, d, lag=0)
