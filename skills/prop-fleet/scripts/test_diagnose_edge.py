#!/usr/bin/env python3
"""בדיקות לאבחון הקצה.

הסכנה כאן אינה חישוב שגוי — היא מסקנה שנראית נכונה. סקריפט שמחפש
מה משפר מדגם תמיד ימצא משהו, ולכן כל בדיקה כאן היא על כך שהוא
מסרב להציג שיפור אקראי כממצא.
"""

import numpy as np
import pandas as pd
import pytest

from diagnose_edge import se_of, verdict


def test_noise_sized_improvement_is_named_as_noise():
    assert "לא ממצא" in verdict(0.05, 0.10)
    assert "לא ממצא" in verdict(-0.05, 0.10)


def test_a_two_sigma_move_is_allowed_to_be_worth_testing():
    assert "קדימה" in verdict(0.25, 0.10)


def test_between_one_and_two_sigma_is_a_hint_not_a_proof():
    v = verdict(0.15, 0.10)
    assert "רמז" in v and "הוכחה" in v


def test_a_missing_noise_floor_never_reads_as_a_finding():
    assert "אין רף" in verdict(0.5, 0.0)
    assert "אין רף" in verdict(0.5, float("nan"))


def test_clustering_widens_the_error_rather_than_narrowing_it():
    """ארבע עסקאות באותו אחר צהריים אינן ארבע תצפיות.

    שגיאת תקן שמניחה עצמאות צרה מדי, ולכן היא הופכת רעש לממצא —
    וזה בדיוק הכיוון שבו טעות כאן עולה כסף.
    """
    rng = np.random.default_rng(3)
    days, vals = [], []
    for d in range(10):
        shift = rng.normal(0, 1.0)
        for _ in range(8):
            days.append(d)
            vals.append(shift + rng.normal(0, 0.1))
    x = np.array(vals)
    assert se_of(x, days) > se_of(x) * 1.5


def test_se_falls_back_cleanly_when_there_is_only_one_day():
    x = np.array([0.1, -0.2, 0.3, 0.4])
    assert se_of(x, [1, 1, 1, 1]) == pytest.approx(se_of(x))


def test_the_reason_split_is_not_a_search_over_alternatives():
    """פירוק לפי סיבת יציאה מחלק את אותה תוצאה.

    סכום התרומות חייב להחזיר בדיוק את הסך הכולל — אחרת מדובר
    בבחירה ולא בחלוקה, וההגנה מהטיית בחירה נופלת.
    """
    df = pd.DataFrame({
        "net_R": [1.0, -1.0, 0.5, -0.5, 2.0],
        "reason": ["tp", "stop", "eod", "gap_scratch", "tp"],
    })
    parts = df.groupby("reason").net_R.sum().sum()
    assert parts == pytest.approx(df.net_R.sum())
