#!/usr/bin/env python3
"""בדיקות ל-replay.py.

כל בדיקה כאן בנויה סביב טעות שמטה בקטסט לטובת מי שכתב אותו:
מילוי שלא היה אמור לקרות, הפסד שנרשם קטן מדי, נר שמכיל גם סטופ וגם
יעד ונספר כיעד, או סטאפ שלא התמלא ונספר כאפס. כל אחת מהן לבדה
מספיקה כדי להפוך תוחלת שלילית לחיובית.
"""

from datetime import time as dtime

import numpy as np
import pandas as pd
import pytest

from replay import (MIN_RISK_PTS, clustered_interval, cost_R, interval,
                    load_clean_setups, pick_column, replay, walk)

ET = "America/New_York"


def bars(rows, day="2026-06-01", start="09:30"):
    """rows הם רביעיות (open, high, low, close), נר לכל חמש דקות."""
    t0 = pd.Timestamp(f"{day} {start}", tz=ET)
    ts = [t0 + pd.Timedelta(minutes=5 * i) for i in range(len(rows))]
    df = pd.DataFrame(rows, columns=["open", "high", "low", "close"])
    df["ts"] = ts
    df["session"] = df.ts.dt.date
    return df


T0 = pd.Timestamp("2026-06-01 09:30", tz=ET)


# ---------- מילוי ----------

def test_a_limit_fills_when_the_bar_reaches_the_level():
    b = bars([(100, 101, 99, 100.5), (100.5, 101, 100, 100.8)])
    r = walk(b, "long", 99.5, 98.5, 101.5, T0)
    assert r["status"] == "filled"
    assert r["fill_px"] == pytest.approx(99.5)


def test_a_gap_through_the_limit_fills_at_the_better_open():
    """הנר נפתח מתחת ללימיט. לימיט קונה שם, לא ברמה."""
    b = bars([(98.0, 99.0, 97.5, 98.5)])
    r = walk(b, "long", 99.5, 98.0, 102.0, T0)
    assert r["fill_px"] == pytest.approx(98.0)


def test_a_setup_that_never_reaches_its_level_is_not_a_zero():
    b = bars([(100, 100.4, 99.8, 100.1)] * 5)
    r = walk(b, "long", 95.0, 94.0, 97.0, T0)
    assert r["status"] == "no_fill"
    assert "raw_R" not in r


def test_bars_before_the_setup_cannot_fill_it():
    """נר מתויג בתחילתו. נר שהתחיל לפני הסטאפ מכסה גם את העבר."""
    b = bars([(100, 101, 90, 100)] + [(100, 100.2, 99.9, 100)] * 4)
    late = T0 + pd.Timedelta(minutes=5)
    r = walk(b, "long", 95.0, 94.0, 97.0, late)
    assert r["status"] == "no_fill", r


# ---------- יציאה ----------

def test_the_target_pays_its_multiple():
    b = bars([(100, 100.2, 99.0, 100), (100, 103.0, 100, 102.5)])
    r = walk(b, "long", 99.5, 98.5, 101.5, T0)
    assert r["reason"] == "tp"
    assert r["raw_R"] == pytest.approx(2.0)


def test_a_gap_below_the_stop_exits_at_the_open_not_the_stop():
    """הטעות שמקטינה הפסדים: סטופ הוא שוק, והפער מבוצע בפתיחה."""
    b = bars([(100, 100.2, 99.4, 100), (96.0, 96.5, 95.0, 95.5)])
    r = walk(b, "long", 99.5, 98.5, 102.5, T0)
    assert r["reason"] == "stop"
    assert r["exit_px"] == pytest.approx(96.0)
    assert r["raw_R"] == pytest.approx(-3.5)


def test_a_stop_inside_the_bar_exits_at_the_stop():
    b = bars([(100, 100.2, 99.4, 100), (99.4, 99.5, 98.0, 98.2)])
    r = walk(b, "long", 99.5, 98.5, 102.5, T0)
    assert r["exit_px"] == pytest.approx(98.5)
    assert r["raw_R"] == pytest.approx(-1.0)


def test_an_unresolved_setup_closes_at_the_end_of_the_day():
    b = bars([(100, 100.2, 99.4, 100), (100, 100.3, 99.8, 100.5)])
    r = walk(b, "long", 99.5, 98.5, 105.0, T0)
    assert r["reason"] == "eod"
    assert r["exit_px"] == pytest.approx(100.5)


# ---------- הנר הדו-משמעי ----------

def test_a_bar_holding_both_levels_is_counted_as_the_stop():
    b = bars([(100, 100.2, 99.4, 100), (100, 102.0, 98.0, 99.0)])
    r = walk(b, "long", 99.5, 98.5, 101.5, T0)
    assert r["ambiguous"] is True
    assert r["reason"] == "stop"


def test_the_optimistic_reading_is_available_and_differs():
    b = bars([(100, 100.2, 99.4, 100), (100, 102.0, 98.0, 99.0)])
    p = walk(b, "long", 99.5, 98.5, 101.5, T0, pessimistic=True)
    o = walk(b, "long", 99.5, 98.5, 101.5, T0, pessimistic=False)
    assert p["raw_R"] < 0 < o["raw_R"]
    assert p["ambiguous"] and o["ambiguous"]


# ---------- שורט, כתמונת ראי ----------

def test_a_short_fills_on_a_rise_and_pays_on_a_fall():
    b = bars([(100, 100.6, 99.8, 100.3), (100.3, 100.4, 98.0, 98.2)])
    r = walk(b, "short", 100.5, 101.5, 98.5, T0)
    assert r["fill_px"] == pytest.approx(100.5)
    assert r["reason"] == "tp"
    assert r["raw_R"] == pytest.approx(2.0)


def test_a_short_gapping_up_through_its_stop_exits_at_the_open():
    b = bars([(100, 100.6, 99.8, 100.3), (103.0, 104.0, 102.5, 103.5)])
    r = walk(b, "short", 100.5, 101.5, 98.5, T0)
    assert r["exit_px"] == pytest.approx(103.0)
    assert r["raw_R"] == pytest.approx(-2.5)


# ---------- סיכון, עלות, MFE ----------

def test_risk_is_the_planned_distance_not_the_filled_one():
    """מילוי טוב יותר מגדיל את ה-R. הוא לא מקטין את הסיכון.

    הנר נפתח ב-99.0, מתחת ללימיט שב-99.5 אבל מעל הסטופ שב-98.5.
    הסיכון המתוכנן נשאר נקודה אחת, והמילוי העדיף הוא רווח.
    """
    b = bars([(99.0, 99.4, 98.8, 99.2), (99.2, 101.5, 99.1, 101.0)])
    r = walk(b, "long", 99.5, 98.5, 101.5, T0)
    assert r["risk_pts"] == pytest.approx(1.0)
    assert r["fill_px"] == pytest.approx(99.0)
    assert r["raw_R"] == pytest.approx(2.5)


def test_a_gap_past_both_levels_is_flagged_as_a_scratch():
    """הפער עבר גם את הלימיט וגם את הסטופ. נכנסים ויוצאים כמעט
    באותו מחיר, וזה אמיתי — אבל זה הפסד שנמחק, ולכן הוא מסומן."""
    b = bars([(98.0, 99.0, 97.5, 98.5), (98.5, 101.5, 98.4, 101.0)])
    r = walk(b, "long", 99.5, 98.5, 101.5, T0)
    assert r["gapped"] is True
    assert r["reason"] == "gap_scratch"
    assert r["raw_R"] == pytest.approx(0.0)


def test_a_short_gapping_past_both_levels_is_flagged_too():
    b = bars([(102.0, 102.5, 101.0, 101.5)])
    r = walk(b, "short", 100.5, 101.5, 98.5, T0)
    assert r["gapped"] is True
    assert r["reason"] == "gap_scratch"


def test_an_ordinary_stop_is_never_called_a_scratch():
    b = bars([(100, 100.2, 99.4, 100), (99.4, 99.5, 98.0, 98.2)])
    r = walk(b, "long", 99.5, 98.5, 102.5, T0)
    assert r["gapped"] is False
    assert r["reason"] == "stop"


def test_a_gap_on_a_later_bar_is_a_stop_not_a_scratch():
    """הפער חייב להיות בנר המילוי עצמו. פער ביום אחרי הוא הפסד מלא."""
    b = bars([(99.6, 99.8, 99.3, 99.5), (96.0, 96.2, 95.0, 95.5)])
    r = walk(b, "long", 99.5, 98.5, 102.5, T0)
    assert r["reason"] == "stop"
    assert r["raw_R"] < -3


def test_cost_shrinks_as_the_stop_widens():
    assert cost_R("ES", 8.5) > cost_R("ES", 17.0)
    assert cost_R("ES", 8.5) == pytest.approx((0.25 + 1.30 / 5.0) / 8.5)


def test_the_two_instruments_do_not_share_a_point_value():
    assert cost_R("NQ", 30.0) != cost_R("ES", 30.0)


def test_excursions_cover_only_the_holding_window():
    """זינוק אחרי היציאה אינו MFE. זה הפיתוי הגדול בבקטסט."""
    b = bars([(100, 100.2, 99.4, 100), (99.4, 99.5, 98.0, 98.2),
              (98.2, 130.0, 98.0, 129.0)])
    r = walk(b, "long", 99.5, 98.5, 105.0, T0)
    assert r["reason"] == "stop"
    assert r["mfe_R"] < 1.0, r


def test_the_adverse_excursion_is_never_positive():
    b = bars([(100, 100.2, 99.4, 100), (99.4, 102.0, 99.3, 101.8)])
    r = walk(b, "long", 99.5, 98.5, 105.0, T0)
    assert r["mae_R"] <= 0


# ---------- ההרצה המלאה ----------

def make_setups(n=12, day="2026-06-01"):
    t = pd.Timestamp(f"{day} 09:30", tz=ET)
    return pd.DataFrame({
        "ts": [t] * n,
        "symbol": ["ES"] * n,
        "market": ["ES"] * n,
        "direction": ["long"] * n,
        "entry": [99.5] * n,
        "stop_loss": [98.5] * n,
        "take_profit": [101.5] * n,
    })


def test_a_whole_run_nets_the_cost_off_the_gross():
    b = {"ES": bars([(100, 100.2, 99.0, 100), (100, 103.0, 100, 102.5)])}
    res = replay(make_setups(), b, "stop_loss", "take_profit")
    f = res[res.status == "filled"]
    assert len(f) == 12
    assert f.raw_R.iloc[0] == pytest.approx(2.0)
    assert f.net_R.iloc[0] < f.raw_R.iloc[0]


def test_a_stop_closer_than_the_floor_is_dropped():
    s = make_setups(3)
    s["stop_loss"] = 99.5 - MIN_RISK_PTS / 2
    b = {"ES": bars([(100, 100.2, 99.0, 100)])}
    assert replay(s, b, "stop_loss", "take_profit").empty


def test_a_day_with_no_bars_yields_no_rows():
    s = make_setups(3, day="2026-06-02")
    b = {"ES": bars([(100, 100.2, 99.0, 100)], day="2026-06-01")}
    assert replay(s, b, "stop_loss", "take_profit").empty


def test_the_rr_grid_overrides_the_recorded_target():
    b = {"ES": bars([(100, 100.2, 99.0, 100), (100, 100.9, 100, 100.8)])}
    at2 = replay(make_setups(), b, "stop_loss", None, tp_rr=2.0)
    at05 = replay(make_setups(), b, "stop_loss", None, tp_rr=0.5)
    assert at2.reason.iloc[0] == "eod"
    assert at05.reason.iloc[0] == "tp"


# ---------- טעינה ----------

def test_the_clean_window_excludes_the_poisoned_era(tmp_path):
    p = tmp_path / "s.csv"
    pd.DataFrame({
        "timestamp": ["2026-03-01 10:00:00-05:00", "2026-06-01 10:00:00-04:00",
                      "2026-08-01 10:00:00-04:00"],
        "market": ["ES"] * 3, "direction": ["long"] * 3,
        "entry": [5000.0, 5100.0, 5200.0],
    }).to_csv(p, index=False)
    s = load_clean_setups(p)
    assert len(s) == 1
    assert s.entry.iloc[0] == 5100.0


def test_etf_scale_rows_never_enter_a_futures_replay(tmp_path):
    p = tmp_path / "s.csv"
    pd.DataFrame({
        "timestamp": ["2026-06-01 10:00:00-04:00", "2026-06-02 10:00:00-04:00"],
        "market": ["ES", "ES"], "direction": ["long", "long"],
        "entry": [560.0, 5100.0],
    }).to_csv(p, index=False)
    assert list(load_clean_setups(p).entry) == [5100.0]


def test_setups_keep_their_timezone(tmp_path):
    p = tmp_path / "s.csv"
    pd.DataFrame({
        "timestamp": ["2026-06-01 10:00:00-04:00"],
        "market": ["ES"], "direction": ["long"], "entry": [5100.0],
    }).to_csv(p, index=False)
    assert load_clean_setups(p).ts.dt.tz is not None


@pytest.mark.parametrize("name", ["stop_loss", "STOP", "  sl  "])
def test_the_stop_column_is_found_however_it_is_spelled(name):
    df = pd.DataFrame({name: [1.0], "entry": [2.0]})
    assert pick_column(df, ("stop_loss", "stop", "sl")) == name


def test_a_missing_stop_column_is_reported_not_invented():
    df = pd.DataFrame({"entry": [1.0], "grade": ["A"]})
    assert pick_column(df, ("stop_loss", "stop", "sl")) is None


def test_the_interval_widens_as_the_sample_shrinks():
    x = np.array([1.0, -1.0] * 30)
    m, lo, hi = interval(x)
    m2, lo2, hi2 = interval(x[:6])
    assert hi - lo < hi2 - lo2
    assert m == pytest.approx(0.0)


def test_one_trade_has_no_interval():
    m, lo, hi = interval(np.array([0.5]))
    assert m == 0.5 and np.isnan(lo) and np.isnan(hi)


# ---------- כיול: המבחן היחיד שבאמת סוגר בקטסט ----------
#
# בקטסט שדולף מידע מהעתיד מייצר יתרון יש מאין. הדרך לגלות את זה היא
# להריץ אותו על שוק שאין בו יתרון בכלל — הילוך מקרי — ולדרוש שהוא
# יחזיר אפס. בדיקת האפס לבדה לא מספיקה, כי מנוע תקוע שמחזיר אפס
# תמיד יעבור אותה; לכן יש גם בקרה חיובית עם מגמה שתולה.
#
# שתי מלכודות בבניית הנתונים עצמם, ששתיהן הפילו את הגרסה הראשונה
# של הבדיקות האלה:
#
#   פתילות מזויפות. אם מדביקים רעש על הגבוה והנמוך במקום לגזור
#   אותם ממסלול רציף, כל מילוי על פתילה "מתאושש" לסגירה בחינם.
#   זה לבדו נתן 0.26R יתרון מדומה. כאן הנרות נבנים מהילוך בדקה
#   אחת שמקובץ לחמש, ולכן הגבוה והנמוך הם נקודות אמיתיות במסלול.
#
#   מחיר מהעתיד. אם הסטאפ נוצר בתחילת הנר אבל הרמה נגזרת ממחיר
#   הסגירה שלו, הרמה יודעת מה יקרה בחמש הדקות הבאות, והמנוע נראה
#   רווחי בלי שיהיה. המחיר הידוע ב-t0 הוא הפתיחה, וזה מה שמשמש.


def walk_day(rng, n=78, drift=0.0, px0=5000.0, sigma=0.0006):
    """נר חמש דקות שנבנה מחמישה צעדים של דקה — מסלול רציף אמיתי."""
    step = rng.normal(drift / 5.0, sigma / np.sqrt(5), n * 5)
    m = px0 * np.exp(np.cumsum(step)).reshape(n, 5)
    return m[:, 0], m.max(axis=1), m.min(axis=1), m[:, -1]


def synthetic(seed, days=120, per_day=3, drift=0.0, sigma=0.0006,
              risk=8.5, only=None):
    rng = np.random.default_rng(seed)
    rows, sets = [], []
    for d in range(days):
        t0 = (pd.Timestamp("2026-01-05", tz=ET)
              + pd.Timedelta(days=d)).replace(hour=9, minute=30)
        o, hi, lo, c = walk_day(rng, drift=drift, sigma=sigma)
        for i in range(len(o)):
            rows.append({"ts": t0 + pd.Timedelta(minutes=5 * i), "open": o[i],
                         "high": hi[i], "low": lo[i], "close": c[i]})
        for i in rng.choice(40, size=per_day, replace=False):
            i = int(i)
            long = bool(rng.integers(0, 2)) if only is None else (only == "long")
            px = float(o[i])          # מה שידוע ב-t0, לא הסגירה
            e = px - risk * 0.3 if long else px + risk * 0.3
            sets.append({"ts": t0 + pd.Timedelta(minutes=5 * i), "symbol": "ES",
                         "direction": "long" if long else "short", "entry": e,
                         "stop_loss": e - risk if long else e + risk,
                         "take_profit": e + 2 * risk if long else e - 2 * risk})
    b = pd.DataFrame(rows)
    b["session"] = b.ts.dt.date
    return pd.DataFrame(sets), {"ES": b}


def null_run(seed):
    s, b = synthetic(seed)
    f = replay(s, b, "stop_loss", "take_profit")
    return f[f.status == "filled"]


@pytest.mark.parametrize("seed", [99, 7, 1234, 41])
def test_a_random_walk_never_yields_a_positive_edge(seed):
    """הילוך מקרי עם יעד 2R וסטופ 1R חייב לתת אפס, ומעט מתחתיו
    בגלל סגירת סוף יום שקוטעת פוזיציות שלא הוכרעו."""
    f = null_run(seed)
    assert len(f) >= 200, len(f)
    m, lo, hi = interval(f.raw_R.values)
    assert m <= 0.12, (seed, m, lo, hi)
    assert lo <= 0.0 <= hi or hi < 0, (seed, m, lo, hi)


@pytest.mark.parametrize("seed", [99, 7, 1234])
def test_the_target_is_reached_at_roughly_its_geometric_odds(seed):
    """יעד 2R מול סטופ 1R נפגע בשליש מהמקרים בהילוך מקרי. סטייה
    כלפי מעלה משם היא בדיוק החתימה של דליפה מהעתיד."""
    f = null_run(seed)
    rate = (f.reason == "tp").mean()
    assert rate <= 1 / 3 + 0.03, (seed, rate)


def test_a_planted_uptrend_is_recovered_as_a_long_edge():
    """בקרה חיובית: בלעדיה, מנוע שמחזיר אפס תמיד עובר את בדיקת האפס."""
    sl, bl = synthetic(7, drift=0.0002, sigma=0.0006, only="long")
    ss, bs = synthetic(7, drift=0.0002, sigma=0.0006, only="short")
    fl = replay(sl, bl, "stop_loss", "take_profit")
    fs = replay(ss, bs, "stop_loss", "take_profit")
    ml = fl[fl.status == "filled"].net_R.mean()
    ms = fs[fs.status == "filled"].net_R.mean()
    assert ml > 0 > ms, (ml, ms)


def test_shifting_every_setup_later_breaks_its_link_to_the_bars():
    """הסטאפ קשור לרגע שלו, לא לנרות בכלל.

    מזיזים כל סטאפ חצי שעה קדימה ומריצים על אותם נרות בדיוק. מנוע
    שמתעלם מ-t0 היה מחזיר בערך אותו דבר.
    """
    s, b = synthetic(7, drift=0.0002, sigma=0.0006, only="long")
    real = replay(s, b, "stop_loss", "take_profit")
    moved = s.copy()
    moved["ts"] = moved.ts + pd.Timedelta(minutes=30)
    fake = replay(moved, b, "stop_loss", "take_profit")
    rf = real[real.status == "filled"]
    ff = fake[fake.status == "filled"]
    assert len(rf) >= 50, len(rf)
    assert ff.net_R.sum() < 0.6 * rf.net_R.sum(), (ff.net_R.sum(), rf.net_R.sum())


def test_the_clustered_interval_counts_days_not_trades():
    r = np.array([0.5] * 12)
    day = np.repeat(np.arange(3), 4)
    _, _, _, k = clustered_interval(r, day)
    assert k == 3


# ---------- חלון המסחר ----------

def session_setups(times, day="2026-06-01"):
    rows = []
    for hh, mm in times:
        rows.append({
            "ts": pd.Timestamp(f"{day} {hh:02d}:{mm:02d}", tz=ET),
            "symbol": "ES", "market": "ES", "direction": "long",
            "entry": 99.5, "stop_loss": 98.5, "take_profit": 101.5,
        })
    return pd.DataFrame(rows)


def all_day_bars(day="2026-06-01"):
    t0 = pd.Timestamp(f"{day} 00:00", tz=ET)
    n = 288
    rows = [(100.0, 100.2, 99.0, 100.0)] * n
    df = pd.DataFrame(rows, columns=["open", "high", "low", "close"])
    df["ts"] = [t0 + pd.Timedelta(minutes=5 * i) for i in range(n)]
    df["session"] = df.ts.dt.date
    return {"ES": df}


def test_a_setup_outside_the_session_is_not_a_trade():
    """20:00 הוא מסחר ערב. הבוט לא שולח שם, והריפליי לא ימציא מילוי."""
    res = replay(session_setups([(20, 0)]), all_day_bars(),
                 "stop_loss", "take_profit")
    assert list(res.status) == ["outside_session"]


def test_a_setup_inside_the_session_still_trades():
    res = replay(session_setups([(10, 0)]), all_day_bars(),
                 "stop_loss", "take_profit")
    assert res.status.iloc[0] == "filled"


def test_the_flat_time_is_the_boundary_not_midnight():
    """15:58 היא השעה שבה eod_force_close רץ אצלו בפועל."""
    late = replay(session_setups([(15, 55)]), all_day_bars(),
                  "stop_loss", "take_profit")
    past = replay(session_setups([(16, 0)]), all_day_bars(),
                  "stop_loss", "take_profit")
    assert late.status.iloc[0] == "filled"
    assert past.status.iloc[0] == "outside_session"


def test_a_position_cannot_be_held_into_the_evening():
    """סגירת סוף יום היא בסגירה, לא בנר האחרון של היממה."""
    res = replay(session_setups([(15, 0)]), all_day_bars(),
                 "stop_loss", "take_profit")
    r = res.iloc[0]
    assert r.status == "filled"
    assert r.exit_ts.time() < dtime(15, 58), r.exit_ts


# ---------- רווח הסמך המקובץ ----------

def test_the_interval_contains_its_own_estimate():
    """הבאג שנמצא בהרצה האמיתית: +0.172R עם רווח [-0.061, +0.830].

    זה קורה כשהרוחב נלקח סביב ממוצע הימים והנקודה היא ממוצע
    העסקאות. לימים עם מספר עסקאות שונה השניים לא שווים.
    """
    r = np.concatenate([np.full(20, -0.5), np.full(2, 3.0)])
    day = np.concatenate([np.zeros(20), np.ones(2)])
    m, lo, hi = clustered_interval(r, day)[:3]
    assert lo <= m <= hi, (m, lo, hi)
    assert m == pytest.approx(r.mean())


def test_one_trade_per_day_reduces_to_the_ordinary_interval():
    r = np.random.default_rng(11).normal(0.2, 1.0, 40)
    day = np.arange(40)
    _, clo, chi, _ = clustered_interval(r, day)
    _, ilo, ihi = interval(r)
    assert clo == pytest.approx(ilo, abs=1e-9)
    assert chi == pytest.approx(ihi, abs=1e-9)


def test_trades_moving_together_widen_the_interval():
    day = np.repeat(np.arange(25), 4)
    rng = np.random.default_rng(3)
    together = np.repeat(rng.normal(0, 1, 25), 4)
    apart = rng.normal(0, 1, 100)
    _, lo_t, hi_t, _ = clustered_interval(together, day)
    _, lo_a, hi_a, _ = clustered_interval(apart, day)
    assert (hi_t - lo_t) > (hi_a - lo_a)


def test_the_reported_timestamps_keep_their_timezone():
    """חותמת שאיבדה אזור זמן נכתבת ל-CSV כ-UTC בלי סימון, ונקראת
    כאילו היא מקומית. ארבע שעות הפרש, בשקט."""
    b = bars([(100, 100.2, 99.0, 100), (100, 103.0, 100, 102.5)])
    r = walk(b, "long", 99.5, 98.5, 101.5, T0)
    assert r["fill_ts"].tz is not None, r["fill_ts"]
    assert r["exit_ts"].tz is not None, r["exit_ts"]
    assert r["fill_ts"].hour == 9 and r["fill_ts"].minute == 30
