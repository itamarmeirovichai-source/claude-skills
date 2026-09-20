#!/usr/bin/env python3
"""בדיקות למרשם ולדשבורד.

הבדיקה המרכזית כאן היא כיול על רעש. דשבורד שמריץ מאה השערות הוא
מכונה לייצור ממצאי שווא, והשאלה היחידה שחשובה עליו היא כמה הוא
מייצר כשאין שום דבר למצוא. התשובה חייבת להיות אפס.
"""

import numpy as np
import pandas as pd
import pytest

import dashboard as D
import hypotheses as HY


def noise_frame(seed=11, n=111, per_day=4) -> pd.DataFrame:
    """נתונים בלי שום מבנה אמיתי.

    התוצאה נקבעת רק מסיבת היציאה. שעה, יום בשבוע, סימבול, כיוון,
    רוחב סטופ ומחיר הכניסה מוגרלים בנפרד ואין להם שום קשר ל-net_R.
    כל "ממצא" שיצוץ כאן הוא שווא לפי הבנייה.
    """
    rng = np.random.default_rng(seed)
    base = pd.Timestamp("2026-06-01 09:30", tz="America/New_York")
    rows = []
    for i in range(n):
        ts = (base + pd.Timedelta(days=i // per_day)
              + pd.Timedelta(minutes=45 * (i % per_day) + 15))
        reason = rng.choice(["stop", "tp", "eod", "gap_scratch"],
                            p=[.36, .29, .22, .13])
        r = {"stop": -0.92, "tp": 1.36, "eod": 0.21,
             "gap_scratch": -0.07}[reason]
        rows.append(dict(
            status="filled", reason=reason, net_R=r + rng.normal(0, .12),
            raw_R=r, mfe_R=abs(rng.normal(1.0, .7)),
            mae_R=-abs(rng.normal(.6, .3)), risk_pts=rng.uniform(12, 38),
            bars_held=int(rng.integers(2, 45)),
            entry=float(rng.uniform(5000, 5400)), stop=0.0, tp=0.0,
            symbol=rng.choice(["ES", "NQ"]),
            direction=rng.choice(["long", "short"]),
            ts=(ts - pd.Timedelta(minutes=20)).isoformat(),
            fill_ts=ts.isoformat()))
    return D.load(pd.DataFrame(rows).pipe(lambda d: d)) if False else _load(rows)


def _load(rows):
    import tempfile
    import pathlib
    p = pathlib.Path(tempfile.mkdtemp()) / "r.csv"
    pd.DataFrame(rows).to_csv(p, index=False)
    return D.load(p)


# ── המרשם ────────────────────────────────────────────────────────

def test_the_register_has_a_hundred_hypotheses():
    assert len(HY.REGISTER) == 100


def test_every_hypothesis_states_a_mechanism():
    """השערה בלי מנגנון היא כריית נתונים עם שם."""
    for h in HY.REGISTER:
        assert len(h.mechanism) > 20, h.id


def test_ids_are_unique():
    ids = [h.id for h in HY.REGISTER]
    assert len(set(ids)) == len(ids)


def test_the_strategy_itself_is_registered_as_off_limits():
    z = [h for h in HY.REGISTER if h.id == "Z01"][0]
    assert z.prior == 0
    assert "אסור" in z.note


def test_the_weekday_trap_carries_the_lowest_prior():
    """נרשמה בכוונה כדי שלא תיבדק בטעות כאילו יש לה מנגנון."""
    w = [h for h in HY.REGISTER if h.id == "C10"][0]
    assert w.prior == 1


def test_value_of_information_penalises_expensive_tests():
    cheap = HY.H("X", "c", "t", "m" * 30, "replay", 4, 0.1, 1)
    dear = HY.H("Y", "c", "t", "m" * 30, "replay", 4, 0.1, 5)
    assert cheap.voi > dear.voi


def test_the_multiple_testing_threshold_grows_with_the_count():
    one = HY.bonferroni_threshold(0.2, 1)
    many = HY.bonferroni_threshold(0.2, 100)
    assert many > one * 1.5


# ── הכיול ────────────────────────────────────────────────────────

def test_pure_noise_produces_no_survivors():
    """הבדיקה שכל הדשבורד עומד עליה.

    הנתונים נבנו בלי שום קשר בין התוצאה לשעה, ליום, לסימבול או
    לכיוון. אם משהו "שורד בדיקה מרובה" כאן, הדשבורד הוא מכונה
    לייצור ממצאי שווא ואין להשתמש בו.

    הגרסה הראשונה נכשלה בזה: ארבעה שרדו, ובראשם יום השבוע ב-0.882R.
    הסיבה הייתה בודקים שמחזירים מקסימום פחות מינימום על פני קבוצות
    — טווח כזה הוא כבר בחירה, והוא גדל עם מספר הקבוצות גם באפס
    אפקט.
    """
    df = noise_frame()
    res, se, bonf, active = D.run_all(df)
    survivors = [r for r in res if r["status"] == "שורד בדיקה מרובה"]
    assert survivors == [], [(r["id"], r["effect"]) for r in survivors]


@pytest.mark.parametrize("seed", [1, 7, 23, 99])
def test_no_survivors_across_seeds(seed):
    """זרע אחד יכול להיות מזל. ארבעה הם כיול."""
    res, _, _, _ = D.run_all(noise_frame(seed=seed))
    assert not [r for r in res if r["status"] == "שורד בדיקה מרובה"]


def test_range_statistics_are_never_called_a_finding():
    df = noise_frame()
    res, _, _, _ = D.run_all(df)
    for r in res:
        if r["test"] in D.RANGE_TESTS and r["effect"] is not None:
            assert r["status"] == "תיאורי, לא מבחן", r["id"]


def test_a_planted_effect_is_still_visible_as_more_than_noise():
    """בקרה חיובית: הדשבורד לא סתם משתיק הכל.

    בלי זה, דשבורד שמחזיר 'בתוך הרעש' על כל דבר היה עובר את כל
    הבדיקות שלמעלה ולא שווה כלום.
    """
    df = noise_frame()
    df.loc[df.reason == "gap_scratch", "net_R"] -= 3.0
    res, se, bonf, _ = D.run_all(df)
    gap = [r for r in res if r["test"] == "drop_gap_scratch"][0]
    assert gap["effect"] is not None and gap["effect"] > se


def test_clustering_widens_the_error():
    rng = np.random.default_rng(5)
    days, vals = [], []
    for d in range(12):
        shift = rng.normal(0, 1.0)
        for _ in range(8):
            days.append(d)
            vals.append(shift + rng.normal(0, 0.1))
    x = np.array(vals)
    naive = float(np.std(x, ddof=1) / np.sqrt(len(x)))
    assert D.clustered_se(x, days) > naive * 1.5


def test_a_tester_that_crashes_is_reported_not_swallowed():
    df = noise_frame()
    D.TESTS["by_month"] = lambda d: 1 / 0
    try:
        res, _, _, _ = D.run_all(df)
        row = [r for r in res if r["test"] == "by_month"][0]
        assert row["status"] == "לא נבדק"
        assert "נפל" in row["detail"]
    finally:
        D.TESTS["by_month"] = D.t_month


# ── הדף ──────────────────────────────────────────────────────────

def test_the_page_is_self_contained():
    df = noise_frame()
    res, se, bonf, active = D.run_all(df)
    page = D.render(res, se, bonf, active, df)
    assert "<script" in page and "src=" not in page
    assert "http://" not in page and "https://" not in page


def test_the_page_leads_with_the_multiplicity_warning():
    df = noise_frame()
    res, se, bonf, active = D.run_all(df)
    page = D.render(res, se, bonf, active, df)
    head = page[:page.index("<table")]
    assert "בדיקה מרובה" in head
    assert "תיאורי, לא מבחן" in head


def test_every_hypothesis_appears_on_the_page():
    df = noise_frame()
    res, se, bonf, active = D.run_all(df)
    page = D.render(res, se, bonf, active, df)
    for h in HY.REGISTER:
        assert f'data-id="{h.id}"' in page, h.id
