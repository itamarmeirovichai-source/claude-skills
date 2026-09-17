"""בדיקות לסריקה שמפרידה בין פיגור בזמן לפיגור באינדקס.

הכלי הזה אמור להכריע איזה באג לחפש, אז הוא נבדק על נתונים מושתלים
שהתשובה שלהם ידועה מראש — בשני הכיוונים, ועל מקרה נקי. בנוסף נבדקת
הבעיה המתודית שהפילה את הגרסה הקודמת: חציון על קבוצה מתכווצת.
"""

import numpy as np
import pandas as pd
import pytest

from lag_refine import (SESSION_BARS, cohort, lock_cohort, scan_bars,
                        scan_time, summarize)

PER_DAY_TIME = 24.0          # רשת של שעה
PER_DAY_BARS = SESSION_BARS * 5 / 7

ET = "America/New_York"
PER_DAY = 78          # נרות של חמש דקות בסשן רגיל
RNG = np.random.default_rng(20260917)


def make_bars(days=60, start="2026-02-02", sigma=0.0011) -> pd.DataFrame:
    """מהלך אקראי על ימי חול בלבד. סופי השבוע הם מה שמפריד בין
    היחידות, אז הם חייבים להיות אמיתיים."""
    sessions = pd.bdate_range(start, periods=days, tz=ET)
    ts = [d + pd.Timedelta(minutes=570 + 5 * i)     # 09:30 ואילך
          for d in sessions for i in range(PER_DAY)]
    n = len(ts)
    mid = 600 * np.exp(np.cumsum(RNG.normal(0, sigma, n)))
    return pd.DataFrame({"ts": pd.DatetimeIndex(ts), "mid": mid})


def make_setups(bars, k=300, symbol="SPY", first=None, last=None) -> pd.DataFrame:
    """k סטאפים בזמנים אקראיים, בתוך טווח הנרות שנבחר."""
    first = first if first is not None else len(bars) // 3
    last = last if last is not None else len(bars)
    idx = np.sort(RNG.choice(np.arange(first, last), k, replace=False))
    return pd.DataFrame({"ts": bars.ts.values[idx], "symbol": symbol,
                         "_idx": idx}).assign(
        ts=lambda d: pd.to_datetime(d.ts, utc=True).dt.tz_convert(ET))


def price_before(bars, when):
    j = np.searchsorted(bars.ts.values, np.asarray(when), side="right") - 1
    return np.where(j >= 0, bars.mid.values[np.maximum(j, 0)], np.nan)


# ── הכיוון הראשון: היסט קבוע באינדקס ─────────────────────────────

def test_a_planted_bar_offset_is_found_in_bars():
    b = make_bars()
    s = make_setups(b)
    K = 200
    s["entry"] = b.mid.values[s._idx.values - K]

    B = {"SPY": b}
    c = cohort(s, B, max_days=12.0, max_bars=600)
    got = summarize(scan_bars(c, B, 0, 600), per_day=PER_DAY_BARS)
    assert got["at"] == K, f"ציפיתי {K} נרות, קיבלתי {got['at']}"
    assert got["err"] < 0.01, "התאמה מדויקת אמורה לתת שגיאה אפסית"


def test_a_planted_bar_offset_beats_the_time_scan():
    """היסט נרות מדלג על סופי שבוע, אז בזמן לוח הוא נמרח."""
    b = make_bars()
    s = make_setups(b)
    s["entry"] = b.mid.values[s._idx.values - 200]

    B = {"SPY": b}
    c = cohort(s, B, max_days=12.0, max_bars=600)
    bars_min = summarize(scan_bars(c, B, 0, 600))["err"]
    time_min = summarize(scan_time(c, B, 0.5, 12.0, 2.0))["err"]
    assert bars_min < time_min, "יחידת הנרות היא הנכונה כאן"


# ── הכיוון השני: משך זמן קבוע ────────────────────────────────────

def test_a_planted_time_lag_is_found_in_days():
    b = make_bars()
    s = make_setups(b)
    D = 3.0
    s["entry"] = price_before(b, (s.ts - pd.Timedelta(days=D)).values)
    s = s.dropna(subset=["entry"])

    B = {"SPY": b}
    c = cohort(s, B, max_days=12.0, max_bars=600)
    got = summarize(scan_time(c, B, 0.5, 12.0, 1.0), per_day=PER_DAY_TIME)
    assert abs(got["at"] - D) < 0.05, f"ציפיתי {D} ימים, קיבלתי {got['at']}"
    assert got["err"] < 0.01


def test_a_planted_time_lag_beats_the_bar_scan():
    """משך זמן נופל לתוך סופי השבוע, אז במספר נרות הוא נמרח."""
    b = make_bars()
    s = make_setups(b)
    s["entry"] = price_before(b, (s.ts - pd.Timedelta(days=3.0)).values)
    s = s.dropna(subset=["entry"])

    B = {"SPY": b}
    c = cohort(s, B, max_days=12.0, max_bars=600)
    time_min = summarize(scan_time(c, B, 0.5, 12.0, 1.0))["err"]
    bars_min = summarize(scan_bars(c, B, 0, 600))["err"]
    assert time_min < bars_min, "יחידת הזמן היא הנכונה כאן"


# ── מקרה נקי: אסור להמציא פיגור ──────────────────────────────────

def test_clean_data_shows_no_lag():
    b = make_bars()
    s = make_setups(b)
    s["entry"] = b.mid.values[s._idx.values]

    B = {"SPY": b}
    c = cohort(s, B, max_days=12.0, max_bars=600)
    got = summarize(scan_bars(c, B, 0, 600), per_day=PER_DAY_BARS)
    assert got["at"] == 0
    assert got["sharpness"] > 2.0, "מינימום אמיתי באפס הוא עדיין מינימום חד"


def test_clean_data_has_no_trough_anywhere():
    """על נתונים נקיים העקומה רק עולה — אין שום שוקת פנימית.

    לא מספיק לבדוק את המינימום הגלובלי: הוא באפס וממילא חסר לו צד
    שמאל, אז המבחן היה יוצא טריוויאלי. כאן נבדקת כל נקודה פנימית.
    """
    b = make_bars()
    s = make_setups(b)
    s["entry"] = b.mid.values[s._idx.values]

    c = cohort(s, {"SPY": b}, max_days=16.0, max_bars=900)
    e = scan_bars(c, {"SPY": b}, 0, 900).median_err_pct.values
    w = max(1, int(round(4.0 * PER_DAY_BARS)))
    ratios = [min(e[i - w], e[i + w]) / e[i]
              for i in range(w, len(e) - w) if e[i] > 0]
    assert ratios, "צריכות להיות נקודות פנימיות לבדוק"
    assert max(ratios) < 2.0, \
        f"נמצאה שוקת ({max(ratios):.2f}) בנתונים שאין בהם פיגור"


# ── הבעיה המתודית שהפילה את lag_scan ─────────────────────────────

def _trap():
    """שתי קבוצות ששגיאתן קבועה בכל היסט, כדי שכל שינוי בחציון
    יוכל לנבוע רק מנשירה. סדרה שטוחה היא מה שמאפשר את זה."""
    b = make_bars(sigma=0.0)
    early = make_setups(b, k=200, first=0, last=380)
    late = make_setups(b, k=60, first=len(b) // 2)
    early["entry"] = b.mid.values[early._idx.values] * 1.20   # 20% תמיד
    late["entry"] = b.mid.values[late._idx.values] * 1.05     # 5% תמיד
    s = pd.concat([early, late]).sort_values("ts").reset_index(drop=True)
    return b, s


def test_a_shrinking_population_can_fake_a_minimum():
    """הוכחה שהחשש אמיתי, לא תיאורטי.

    אף קבוצה לא מתאימה טוב יותר באף היסט — השגיאות קבועות. ובכל זאת,
    כשהמוקדמים נושרים כי אין מספיק נרות לפניהם, החציון צונח מ-20%
    ל-5%. זה בדיוק המינימום המדומה: הוא מודד מי נשר, לא מה התאים.
    """
    b, s = _trap()
    loose = scan_bars(s, {"SPY": b}, 0, 380)
    assert loose.n.iloc[-1] < loose.n.iloc[0], "הנשירה אכן קורית"
    assert loose.median_err_pct.iloc[0] > 15, "בהתחלה שולטים הרועשים"
    assert loose.median_err_pct.iloc[-1] < 10, "ובסוף הם פשוט איננו"


def test_locking_the_cohort_removes_the_fake_minimum():
    b, s = _trap()
    c = cohort(s, {"SPY": b}, max_days=12.0, max_bars=380)
    tight = scan_bars(c, {"SPY": b}, 0, 380)
    assert tight.n.nunique() == 1, "הקבוצה נעולה: אותו n בכל היסט"
    assert tight.median_err_pct.std() < 1e-9, \
        "עם קבוצה קבועה העקומה שטוחה — אין מה לגלות, וזו האמת"
    assert summarize(tight, per_day=PER_DAY_BARS)["two_sided"] < 2.0, "ובלי שוקת אין פסק דין"


def test_the_cohort_keeps_only_measurable_setups():
    b = make_bars()
    s = make_setups(b, k=200, first=0)
    s["entry"] = b.mid.values[s._idx.values]
    c = cohort(s, {"SPY": b}, max_days=12.0, max_bars=600)
    assert len(c) < len(s), "סטאפים מוקדמים מדי חייבים לנשור"
    assert (c._idx >= 600).all()


# ── חדות: מספר, לא סף שרירותי ────────────────────────────────────

def test_sharpness_is_flat_when_nothing_is_planted():
    """הנקודה שבגללה זרקתי את הסף המוחלט של 0.5%."""
    d = pd.DataFrame({"offset": range(50), "n": 200,
                      "median_err_pct": np.full(50, 3.0),
                      "within_0_5pct": 1.0})
    assert summarize(d)["sharpness"] == pytest.approx(1.0)


def test_sharpness_rises_with_a_real_trough():
    err = np.full(50, 3.0)
    err[20] = 0.6
    d = pd.DataFrame({"offset": range(50), "n": 200,
                      "median_err_pct": err, "within_0_5pct": 1.0})
    got = summarize(d)
    assert got["at"] == 20
    assert got["sharpness"] == pytest.approx(5.0)
    assert got["width"] == 1, "שוקת צרה היא בדיוק מה שמחפשים"


def test_a_half_percent_minimum_is_not_dismissed():
    """0.500% בשיפור פי 8 הוא מינימום אמיתי. הסף הישן פסל אותו."""
    err = np.full(40, 4.0)
    err[15] = 0.5
    d = pd.DataFrame({"offset": range(40), "n": 285,
                      "median_err_pct": err, "within_0_5pct": 49.8})
    assert summarize(d)["sharpness"] == pytest.approx(8.0)


# ── שכפול המצב האמיתי, בשני הכיוונים ─────────────────────────────
#
# 60 ימי נרות כמו שיש לאיתמר, סטאפים בפילוח החודשי שלו, ורעש של 0.3%
# שמייצג את זה שה-entry הוא רמת FVG מחושבת ולא ציטוט. השאלה היא אם
# הכלי מוציא פסק דין נכון על כמות הנתונים הזאת, או נחנק.

def _his_shape(rng):
    def series():
        ss = pd.bdate_range("2026-02-20", periods=60, tz=ET)
        ts = [d + pd.Timedelta(minutes=570 + 5 * i) for d in ss for i in range(PER_DAY)]
        return pd.DataFrame({"ts": pd.DatetimeIndex(ts),
                             "mid": 600 * np.exp(np.cumsum(rng.normal(0, 0.0011, len(ts))))})
    return {"SPY": series(), "QQQ": series()}


def test_his_data_volume_recovers_a_planted_time_lag():
    rng = np.random.default_rng(7)
    B = _his_shape(rng)
    b = B["SPY"]
    idx = np.sort(rng.choice(np.arange(1200, len(b)), 300, replace=False))
    s = pd.DataFrame({"ts": b.ts.values[idx], "symbol": "SPY"})
    s["ts"] = pd.to_datetime(s.ts, utc=True).dt.tz_convert(ET)
    LAG = 15.16
    s["entry"] = price_before(b, (s.ts - pd.Timedelta(days=LAG)).values) \
        * (1 + rng.normal(0, 0.003, len(s)))

    c, hi_d, hi_b = lock_cohort(s, B, 20.0, 1114)
    assert len(c) >= 200, f"הקבוצה קרסה ל-{len(c)} — אין על מה לפסוק"
    st = summarize(scan_time(c, B, 0.0, hi_d, 1.0), per_day=PER_DAY_TIME)
    sb = summarize(scan_bars(c, B, 0, hi_b), per_day=PER_DAY_BARS)
    assert abs(st["at"] - LAG) < 0.2, f"פוספס הפיגור: {st['at']}"
    assert st["err"] < sb["err"], "יחידת הזמן חייבת לנצח כאן"
    assert st["two_sided"] >= 2.0, "ובשוקת מספיק ברורה כדי לפסוק"


def test_his_data_volume_recovers_a_planted_bar_offset():
    """הביקורת ההפוכה. בלעדיה הכלי יכול פשוט תמיד לומר 'זמן'."""
    rng = np.random.default_rng(7)
    B = _his_shape(rng)
    b = B["SPY"]
    idx = np.sort(rng.choice(np.arange(1200, len(b)), 300, replace=False))
    s = pd.DataFrame({"ts": b.ts.values[idx], "symbol": "SPY", "_i": idx})
    s["ts"] = pd.to_datetime(s.ts, utc=True).dt.tz_convert(ET)
    K = 889
    s["entry"] = b.mid.values[idx - K] * (1 + rng.normal(0, 0.003, len(s)))

    c, hi_d, hi_b = lock_cohort(s, B, 20.0, 1114)
    st = summarize(scan_time(c, B, 0.0, hi_d, 1.0), per_day=PER_DAY_TIME)
    sb = summarize(scan_bars(c, B, 0, hi_b), per_day=PER_DAY_BARS)
    assert sb["at"] == K, f"פוספס ההיסט: {sb['at']}"
    assert sb["err"] < st["err"], "יחידת הנרות חייבת לנצח כאן"


def test_the_time_scan_alone_would_have_misled_on_a_bar_offset():
    """למה ההשוואה בין היחידות היא העיקר.

    כשהפיגור נעול על אינדקס, סריקת הזמן עדיין מוצאת "פיגור" של כ-15
    יום. רק ההשוואה מגלה שהיא הפסידה.
    """
    rng = np.random.default_rng(7)
    B = _his_shape(rng)
    b = B["SPY"]
    idx = np.sort(rng.choice(np.arange(1200, len(b)), 300, replace=False))
    s = pd.DataFrame({"ts": b.ts.values[idx], "symbol": "SPY"})
    s["ts"] = pd.to_datetime(s.ts, utc=True).dt.tz_convert(ET)
    s["entry"] = b.mid.values[idx - 889] * (1 + rng.normal(0, 0.003, len(s)))

    c, hi_d, hi_b = lock_cohort(s, B, 20.0, 1114)
    st = summarize(scan_time(c, B, 0.0, hi_d, 1.0), per_day=PER_DAY_TIME)
    assert 10 < st["at"] < 20, "סריקת הזמן אכן מצביעה על פיגור שאינו קיים"
    assert st["err"] > summarize(scan_bars(c, B, 0, hi_b),
                                 per_day=PER_DAY_BARS)["err"]


# ── הרעש הוא שקובע אם אפשר להפריד בין היחידות ────────────────────
#
# הכלי הכריז "נעול על נרות" ביחס 1.04 על הנתונים האמיתיים. זו הייתה
# טעות: הקוד בחר מנצח לפי < בלי מרווח. הבדיקות כאן נועלות גם את
# המרווח וגם את הסיבה שהוא תלוי-רעש.

from lag_refine import (RESOLVABLE_RESIDUAL, SHARP_RATIO, TROUGH_BLIND_RESIDUAL,
                        UNIT_MARGIN, divergence_table)


def _planted(kind, seed, noise, n=300):
    rng = np.random.default_rng(seed)
    def ser():
        ss = pd.bdate_range("2026-02-20", periods=60, tz=ET)
        ts = [d + pd.Timedelta(minutes=570 + 5 * i) for d in ss for i in range(PER_DAY)]
        return pd.DataFrame({"ts": pd.DatetimeIndex(ts),
                             "mid": 600 * np.exp(np.cumsum(rng.normal(0, 0.0011, len(ts))))})
    B = {"SPY": ser()}
    b = B["SPY"]
    idx = np.sort(rng.choice(np.arange(1300, len(b)), n, replace=False))
    s = pd.DataFrame({"ts": b.ts.values[idx], "symbol": "SPY"})
    s["ts"] = pd.to_datetime(s.ts, utc=True).dt.tz_convert(ET)
    if kind == "bars":
        s["entry"] = b.mid.values[idx - 906] * (1 + rng.normal(0, noise, n))
    elif kind == "time":
        j = np.searchsorted(b.ts.values,
                            (s.ts - pd.Timedelta(days=15.04)).values, side="right") - 1
        s["entry"] = b.mid.values[j] * (1 + rng.normal(0, noise, n))
    else:
        s["entry"] = b.mid.values[idx] * (1 + rng.normal(0, noise, n))
    c, hd, hb = lock_cohort(s, B, 25.0, 1350)
    st = summarize(scan_time(c, B, 0.0, hd, 1.0), limit=20.0, per_day=PER_DAY_TIME)
    sb = summarize(scan_bars(c, B, 0, hb), limit=1114, per_day=PER_DAY_BARS)
    return {
        "ratio": max(st["err"], sb["err"]) / min(st["err"], sb["err"]),
        "residual": min(st["err"], sb["err"]),
        "trough": max(st["two_sided"], sb["two_sided"]),
        "winner": "time" if st["err"] < sb["err"] else "bars",
        "c": c, "B": B, "st": st, "sb": sb,
    }


def test_at_low_noise_the_unit_is_decidable():
    got = _planted("bars", 7, 0.003)
    assert got["winner"] == "bars"
    assert got["ratio"] >= UNIT_MARGIN, "ברעש נמוך ההכרעה חייבת לעבור את הסף"


def test_at_the_real_noise_level_the_unit_is_not_decidable():
    """הליבה של התיקון.

    פיגור אמיתי הנעול על נרות, ברעש שמייצר את השארית שנמדדה בפועל,
    נותן יחס מתחת לסף. כלומר יחס נמוך על הנתונים האמיתיים אינו ראיה
    נגד היסט נרות — הוא רק אומר שאין הפרדה.
    """
    got = _planted("bars", 7, 0.006)
    assert got["residual"] > RESOLVABLE_RESIDUAL
    assert got["ratio"] < UNIT_MARGIN, (
        f"יחס {got['ratio']:.2f} — אם זה עובר את הסף, הסף מרשה "
        "להכריע במקום שבו הכיול אומר שאי אפשר")


def test_the_trough_still_finds_the_lag_at_that_noise():
    """מה שכן נשאר תקף: עצם קיום הפיגור."""
    got = _planted("bars", 7, 0.006)
    assert got["trough"] >= SHARP_RATIO


def test_no_lag_is_separated_by_the_trough_not_by_the_ratio():
    """בלי פיגור, היחס גם הוא ~1.0 — רק השוקת מבדילה."""
    got = _planted("none", 7, 0.006)
    assert got["ratio"] < UNIT_MARGIN, "היחס לא מבדיל כאן"
    assert got["trough"] < SHARP_RATIO, "השוקת כן"


def test_very_high_noise_hides_even_the_lag():
    """הגבול של הכלי, מתועד ולא מוסתר."""
    got = _planted("bars", 7, 0.009)
    assert got["residual"] > TROUGH_BLIND_RESIDUAL
    assert got["trough"] < SHARP_RATIO, (
        "ברעש כזה פיגור אמיתי נעלם — ולכן שלילה שם חייבת להיאמר כחלשה")


def test_the_divergence_set_is_too_small_when_time_is_the_truth():
    """למה מבחן ההפרדה לא תמיד עוזר.

    פיגור של 15 ימי לוח מתורגם כמעט תמיד לאותם 11 ימי מסחר, אז
    הסטאפים שבהם שתי ההשערות נחלקות הם מיעוט קטן. זו תכונה של
    הנתונים, לא תקלה — וצריך לומר אותה במקום להכריע בלעדיה.
    """
    got = _planted("time", 7, 0.003)
    d = divergence_table(got["c"], got["B"], got["st"]["at"], int(got["sb"]["at"]))
    assert len(d[d.gap_bars >= SESSION_BARS]) < 20


def test_the_divergence_set_is_usable_when_bars_is_the_truth():
    got = _planted("bars", 7, 0.003)
    d = divergence_table(got["c"], got["B"], got["st"]["at"], int(got["sb"]["at"]))
    hi = d[d.gap_bars >= SESSION_BARS]
    assert len(hi) >= 20
    assert hi.err_bars.median() < hi.err_time.median()
