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

from replay import (MIN_RISK_PTS, _tcrit, clustered_interval, cost_R, interval,
                    load_clean_setups, pick_column, replay, report_drift, walk)

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
    """הגבול הוא ההשטחה ב-15:58, לא חצות.

    הבדיקה הזאת קודם טענה שסטאפ ב-15:55 מתמלא, וזו הייתה הטעות
    עצמה. נר מתויג בתחילתו, ולכן הנר היחיד שיכול למלא סטאפ כזה
    הוא זה שמתחיל ב-15:55 ונסגר ב-16:00 — שתי דקות אחרי שהבוט
    כבר שטוח. מילוי כזה הוא פוזיציה שלא הייתה קיימת, והסגירה
    שלו היא מחיר שהחשבון לא יכול היה לקבל.
    """
    late = replay(session_setups([(15, 55)]), all_day_bars(),
                  "stop_loss", "take_profit")
    past = replay(session_setups([(16, 0)]), all_day_bars(),
                  "stop_loss", "take_profit")
    ok = replay(session_setups([(15, 50)]), all_day_bars(),
                "stop_loss", "take_profit")
    assert ok.status.iloc[0] == "filled", "הנר האחרון שנסגר לפני ההשטחה"
    assert late.status.iloc[0] == "outside_session"
    assert past.status.iloc[0] == "outside_session"


def test_a_position_cannot_be_held_into_the_evening():
    """סגירת סוף יום היא בסגירה, לא בנר האחרון של היממה."""
    res = replay(session_setups([(15, 0)]), all_day_bars(),
                 "stop_loss", "take_profit")
    r = res.iloc[0]
    assert r.status == "filled"
    assert r.exit_ts.time() < dtime(15, 58), r.exit_ts


def test_end_of_day_exit_is_observable_before_the_flatten():
    """מחיר היציאה נצפה עד 15:55, לא בסגירת 16:00.

    ברזולוציה של חמש דקות אין מחיר של 15:58. הדבר האחרון שנצפה
    בוודאות לפני ההשטחה הוא סגירת הנר של 15:50, כלומר המחיר
    ב-15:55. כל מה שאחריו הוא זכייה או חיסכון בשתי דקות שהחשבון
    האמיתי לא היה בהן.
    """
    res = replay(session_setups([(14, 0)]), all_day_bars(),
                 "stop_loss", "take_profit")
    r = res.iloc[0]
    if r.reason == "eod":
        assert r.exit_ts.time() <= dtime(15, 50), r.exit_ts


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


# ---------- בקרת החוזה ----------

def drift_rows(pts_by_month, symbol="ES", n=100, risk=8.5):
    return (pd.DataFrame([
        {"symbol": symbol, "month": m, "n": n,
         "drift_pct": abs(p) / 7500 * 100, "signed_pts": p}
        for m, p in pts_by_month.items()]),
        pd.DataFrame({"status": ["filled"] * 3, "risk_pts": [risk] * 3}))


def test_a_carry_offset_is_reported_in_R_not_only_in_percent(capsys):
    """שתי נקודות נשמעות כלום. מול סטופ 8.5 הן רבע R."""
    d, res = drift_rows({"2026-05": 2.2, "2026-06": 0.05})
    report_drift(d, res)
    out = capsys.readouterr().out
    assert "0.26" in out, out
    assert "רצפת" in out, out


def test_a_negligible_offset_is_not_dressed_up_as_a_problem(capsys):
    d, res = drift_rows({"2026-05": 0.2, "2026-06": 0.05})
    report_drift(d, res)
    out = capsys.readouterr().out
    assert "קטנה מספיק" in out, out


def test_the_months_are_not_averaged_into_one_number():
    """חציון כולל מדלל את התקופה שלפני הגלגול בזו שאחריה."""
    d, _ = drift_rows({"2026-05": 2.2, "2026-06": 0.0, "2026-07": 0.0})
    assert len(d) == 3
    assert d.signed_pts.max() == pytest.approx(2.2)


def test_an_empty_drift_table_prints_nothing(capsys):
    report_drift(pd.DataFrame(), pd.DataFrame({"status": [], "risk_pts": []}))
    assert capsys.readouterr().out == ""


def test_a_corrected_residual_is_not_called_invalid(capsys):
    """0.11R אחרי תיקון אינו אותו דבר כמו 13.87R לפניו."""
    d, res = drift_rows({"2026-05": 2.5}, symbol="NQ", risk=23.5)
    report_drift(d, res)
    out = capsys.readouterr().out
    assert "לא תקף" not in out
    assert "רצפת" in out


def test_an_uncorrected_shift_is_still_called_invalid(capsys):
    d, res = drift_rows({"2026-05": 279.0}, symbol="NQ", risk=20.1)
    report_drift(d, res)
    assert "לא תקף" in capsys.readouterr().out


# ---------- גרירת הסטופ ----------
#
# הבוט מזיז את הסטופ לנקודת האיזון כשהרווח מגיע לטריגר. הוא עושה
# את זה מתוך סריקה כל 300 שניות, על המחיר האחרון החי באותו רגע.
# כל בדיקה כאן היא מקום שבו ריפליי היה יכול לגרור בחינם ולהחזיר
# תוחלת שהחשבון לא יראה.

def test_trailing_does_not_fire_on_a_touch_between_scans():
    """הטעות המרכזית. הנר נגע ב-1R וחזר; הבוט לא ראה את הנגיעה.

    כניסה 100, סטופ 99, כלומר 1R = 101. הנר השני מגיע ל-101.5
    בתוך החלון אבל נסגר ב-100.2. סריקה שמסתכלת על המחיר האחרון
    רואה 100.2 — מתחת לטריגר — ולא גוררת. אחר כך המחיר יורד
    לסטופ המקורי, וזה הפסד מלא. ריפליי שבודק את ה-high היה גורר
    כאן והופך את ההפסד לאפס, בחינם.
    """
    b = bars([(100, 100.1, 99.9, 100.0),
              (100.0, 101.5, 99.95, 100.2),
              (100.2, 100.3, 98.5, 98.6)])
    r = walk(b, "long", 100.0, 99.0, None, T0, trail_trigger=1.0, trail_to=0.0)
    assert r["status"] == "filled"
    assert r["trailed"] is False, "נגיעה בין סריקות אינה אירוע"
    assert r["reason"] == "stop"
    assert r["raw_R"] == pytest.approx(-1.0)


def test_trailing_fires_when_the_scan_price_itself_reaches_the_trigger():
    """אותו מבנה, אבל הפעם הנר נסגר מעל הטריגר. הבוט כן רואה."""
    b = bars([(100, 100.1, 99.9, 100.0),
              (100.0, 101.5, 99.95, 101.2),
              (101.2, 101.3, 98.5, 98.6)])
    r = walk(b, "long", 100.0, 99.0, None, T0, trail_trigger=1.0, trail_to=0.0)
    assert r["trailed"] is True
    assert r["reason"] == "trail"
    assert r["final_stop"] == pytest.approx(100.0)
    assert r["raw_R"] == pytest.approx(0.0), "נעצר בנקודת האיזון"


def test_a_trailed_stop_cannot_close_the_bar_that_created_it():
    """ההחלטה נופלת בסגירה, ולכן היא שייכת לנר הבא.

    בלי זה אותו נר גם מרים את הסטופ וגם נעצר בו לפי השפל שלו —
    שפל שקרה, אולי, לפני שהמחיר הגיע לטריגר בכלל.
    """
    b = bars([(100, 100.1, 99.9, 100.0),
              (100.0, 101.4, 99.5, 101.2),
              (101.2, 101.4, 101.0, 101.3)])
    r = walk(b, "long", 100.0, 99.0, None, T0, trail_trigger=1.0, trail_to=0.0)
    assert r["trailed"] is True
    assert r["reason"] == "eod", "השפל של נר הגרירה לא סוגר את הפוזיציה"


def test_trailing_never_moves_the_stop_backwards():
    b = bars([(100, 100.1, 99.9, 100.0),
              (100.0, 101.4, 99.9, 101.2),
              (101.2, 101.4, 100.5, 100.6),
              (100.6, 100.8, 100.4, 100.5)])
    r = walk(b, "long", 100.0, 99.0, None, T0, trail_trigger=0.5, trail_to=0.0)
    assert r["final_stop"] == pytest.approx(100.0), "לא חוזר אחורה"


def test_trailing_is_off_by_default():
    """ברירת המחדל היא המדידה בלי גרירה, כדי שאפשר יהיה להשוות."""
    b = bars([(100, 100.1, 99.9, 100.0),
              (100.0, 101.5, 99.95, 101.2),
              (101.2, 101.3, 98.5, 98.6)])
    r = walk(b, "long", 100.0, 99.0, None, T0)
    assert r["trailed"] is False
    assert r["raw_R"] == pytest.approx(-1.0)


def test_trailing_works_the_same_way_short():
    """אותה בדיקה הפוכה. סימן שנשמט בצד אחד הוא באג שקט."""
    touch = bars([(100, 100.1, 99.9, 100.0),
                  (100.0, 100.05, 98.5, 99.8),
                  (99.8, 101.5, 99.7, 101.4)])
    r = walk(touch, "short", 100.0, 101.0, None, T0,
             trail_trigger=1.0, trail_to=0.0)
    assert r["trailed"] is False
    assert r["raw_R"] == pytest.approx(-1.0)

    seen = bars([(100, 100.1, 99.9, 100.0),
                 (100.0, 100.05, 98.5, 98.8),
                 (98.8, 101.5, 98.7, 101.4)])
    r2 = walk(seen, "short", 100.0, 101.0, None, T0,
              trail_trigger=1.0, trail_to=0.0)
    assert r2["trailed"] is True
    assert r2["raw_R"] == pytest.approx(0.0)


def test_R_denominator_stays_the_planned_risk_after_trailing():
    """אחרי גרירה לנקודת האיזון המרחק לסטופ הוא אפס.

    אם המכנה היה הסטופ הפעיל, R היה חלוקה באפס — וזה בדיוק
    ה-zero_risk שהבוט נופל עליו. המכנה חייב להישאר הסיכון
    המתוכנן, שהוא גם מה שהחשבון באמת סיכן.
    """
    b = bars([(100, 100.1, 99.9, 100.0),
              (100.0, 102.2, 99.9, 102.1),
              (102.1, 102.2, 98.0, 98.1)])
    r = walk(b, "long", 100.0, 98.0, None, T0, trail_trigger=1.0, trail_to=0.0)
    assert r["risk_pts"] == pytest.approx(2.0)
    assert r["final_stop"] == pytest.approx(100.0)
    assert r["raw_R"] == pytest.approx(0.0)


def test_trailing_can_only_reduce_a_loss_never_create_one():
    """גרירה לנקודת האיזון לא יכולה להפוך רווח להפסד גדול יותר.

    זו בדיקת שפיות על הכיוון: על אותם נרות, התוצאה עם גרירה
    חייבת להיות גדולה או שווה לתוצאה בלעדיה כשהיציאה היא סטופ.
    """
    b = bars([(100, 100.1, 99.9, 100.0),
              (100.0, 101.4, 99.9, 101.2),
              (101.2, 101.3, 98.5, 98.6)])
    plain = walk(b, "long", 100.0, 99.0, None, T0)
    trailed = walk(b, "long", 100.0, 99.0, None, T0,
                   trail_trigger=1.0, trail_to=0.0)
    assert trailed["raw_R"] >= plain["raw_R"]


@pytest.mark.parametrize("seed", [99, 7, 1234, 41])
def test_trailing_on_a_random_walk_still_yields_nothing(seed):
    """הכיול: הגרירה לא הוסיפה תוחלת יש מאין.

    הזזת סטופ היא זמן עצירה, ועצירה של הילוך מקרי חסר סחיפה לא
    יכולה לייצר תוחלת חיובית — לא משנה כמה חכם כלל העצירה. אם
    הגרירה מחזירה כאן רווח, נשבר משהו בסיסי במנוע.

    ומה שהיא לא מוכיחה, כי נבדק: היא לא תופסת גרירה לפי השיא של
    הנר במקום לפי הסגירה. הרצתי את הווריאנט הזה והבדיקה הזאת
    עברה בכל ארבעת הזרעים. זה הגיוני בדיעבד — גם גרירה שנשענת על
    השיא היא עדיין כלל עצירה שפועל על נרות עתידיים, ולכן המרטינגל
    נשמר והתוחלת נשארת אפס. היא פשוט מתארת בוט אחר, כזה שרואה את
    מה שהבוט האמיתי לא רואה, וזה לא נראה בדולרים.

    מה שכן תופס את זה הוא
    test_trailing_does_not_fire_on_a_touch_between_scans, ישירות.
    בדיקת כיול על הילוך מקרי היא כלי חזק מאוד לדליפות שמייצרות
    כסף, וכלי עיוור לדליפות שרק מחליפות מכשיר אחד באחר.
    """
    s, b = synthetic(seed)
    t = replay(s, b, "stop_loss", "take_profit",
               trail_trigger=1.0, trail_to=0.0)
    f = t[t.status == "filled"]
    assert len(f) >= 200, len(f)
    assert f.trailed.sum() > 0, "בלי אף גרירה הבדיקה לא בודקת כלום"
    m, lo, hi = interval(f.raw_R.values)
    assert m <= 0.12, (seed, m, lo, hi, int(f.trailed.sum()))
    assert lo <= 0.0 <= hi or hi < 0, (seed, m, lo, hi)


def test_the_dollar_line_sizes_the_evaluation_separately():
    """הבאג שהפך תוחלת חיובית למינוס בשורה שהוא באמת קורא.

    project() הריץ את המודל בלי risk_pct_eval, כלומר הערכות ב-4%
    כמו החשבון הממומן. היעד של ההערכה הופך אז ל-35.3R מתוך 63
    עסקאות — בלתי אפשרי — והמודל שורף דמי הערכה לנצח בלי לעבור
    אף פעם. על +0.101R שנמדד בפועל זה היה ההפרש בין 7,372$- לבין
    200,677$+, ואת השורה הזאת קוראים כדי להחליט.

    זו הפעם השלישית שאותו פרמטר נשמט בשלושה מקומות שונים, ולכן
    יש עליו בדיקה בכל אחד מהם.
    """
    seen = {}

    def spy(**kw):
        seen.update(kw)
        n = kw.get("n", 10)
        return {"net_year": np.zeros((n, 8))}

    import replay as rp
    real = rp.simulate if hasattr(rp, "simulate") else None
    import apex_model
    orig = apex_model.simulate
    apex_model.simulate = spy
    try:
        rp.project({"n": 111, "days": 28, "mean": 0.101, "lo": -0.184},
                   pd.DataFrame())
    finally:
        apex_model.simulate = orig
        if real is not None:
            rp.simulate = real
    assert seen.get("risk_pct_eval") == 0.10, seen
    assert seen.get("risk_pct") == 0.04, seen


def test_trailing_changes_the_shape_of_the_outcomes():
    """בקרה חיובית לגרירה עצמה.

    תוחלת שלא זזה היא גם מה שהיינו רואים אילו הגרירה לא הייתה
    מחוברת בכלל. הראיה שהיא כן פועלת היא שההפסדים המלאים מתחלפים
    ביציאות סביב האפס — אותה תוחלת, פיזור אחר.
    """
    s, b = synthetic(99)
    plain = replay(s, b, "stop_loss", "take_profit")
    trail = replay(s, b, "stop_loss", "take_profit",
                   trail_trigger=1.0, trail_to=0.0)
    pf = plain[plain.status == "filled"]
    tf = trail[trail.status == "filled"]
    full_loss = lambda f: (f.raw_R < -0.95).mean()
    assert full_loss(tf) < full_loss(pf), "הגרירה אמורה לחתוך הפסדים מלאים"
    assert (tf.reason == "tp").mean() < (pf.reason == "tp").mean(), \
        "והיא אמורה לקטוע גם חלק מהזוכות בדרך ליעד"


def test_regime_measures_separate_a_trend_from_a_chop():
    """יחס היעילות חייב להפריד מגמה מדשדוש, אחרת הוא לא מודד כלום.

    D04 הוא הפריור הגבוה ביותר במרשם ההשערות, והוא תלוי לגמרי
    במדד הזה. מדד שלא מפריד בין שני המקרים הקיצוניים לא יפריד
    גם בין המקרים האמיתיים.
    """
    n = 60
    up = np.arange(n, dtype=float) * 2.0 + 5000.0
    chop = 5000.0 + np.tile([0.0, 3.0], n // 2)
    for arr, name in ((up, "מגמה"), (chop, "דשדוש")):
        pass
    trend = replay_mod_regime(up)
    flat = replay_mod_regime(chop)
    assert trend["day_efficiency"] > 0.9, trend
    assert flat["day_efficiency"] < 0.1, flat


def replay_mod_regime(closes):
    from replay import regime_of
    df = pd.DataFrame({"close": closes,
                       "high": closes + 1.0, "low": closes - 1.0})
    return regime_of(df)


def test_regime_is_empty_on_a_session_too_short_to_measure():
    assert replay_mod_regime(np.array([1.0, 2.0])) == {}


def test_a_flat_session_does_not_divide_by_zero():
    out = replay_mod_regime(np.full(30, 5000.0))
    assert out["day_efficiency"] == 0.0


def test_few_clusters_use_t_not_the_normal_quantile():
    """עם 28 ימים, 1.96 מכסה 93-94% ולא 95%.

    מעט אשכולות, והשונות עצמה נאמדת מהם. נמדד בסימולציה: הקוונטיל
    הנורמלי מחזיר כיסוי 93.0%, ו-t עם k-1 דרגות חופש מחזיר אותו
    ל-95%. ההפרש כאן הוא 4.7% ברוחב — הוא לא הופך החלטה, אבל
    רווח סמך שמסומן 95% ומכסה 93% הוא פשוט מסומן לא נכון.
    """
    assert _tcrit(27) == pytest.approx(2.052, abs=1e-3)
    assert _tcrit(1) > 12          # מדגם זעיר — רחב מאוד, כמו שצריך
    assert _tcrit(500) == pytest.approx(1.96, abs=1e-3)
    # מונוטוני יורד: יותר דרגות חופש, רווח צר יותר
    vals = [_tcrit(d) for d in (5, 10, 27, 60, 120, 500)]
    assert all(a > b for a, b in zip(vals, vals[1:])), vals
