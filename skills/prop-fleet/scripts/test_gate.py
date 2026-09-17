"""בדיקות ללוגיקת השער. המספרים הם ההחלטה, אז הם צריכים בדיקה."""

import numpy as np
import pytest

from gate import LADDER, bootstrap_ci, longest_losing_run, permitted


def seq(n, avg_R, rr=2.0, seed=0):
    rng = np.random.default_rng(seed)
    p = (avg_R + 1) / (rr + 1)
    return np.where(rng.random(n) < p, rr, -1.0)


# ── הסולם ────────────────────────────────────────────────────────

def test_no_evidence_permits_nothing():
    assert permitted(0, 0.50)[1] == 0, "אפס עסקאות -> אפס חשבונות"


def test_trade_count_alone_is_not_enough():
    """אלף עסקאות עם גבול תחתון שלילי עדיין לא מצדיקות חשבון."""
    assert permitted(1000, -0.05)[1] == 0


def test_expectancy_alone_is_not_enough():
    """גבול תחתון מצוין על 20 עסקאות לא מצדיק עשרים חשבונות."""
    assert permitted(20, 0.60)[1] == 0


def test_both_gates_must_open():
    assert permitted(100, 0.01)[1] == 1
    assert permitted(250, 0.11)[1] == 3
    assert permitted(500, 0.21)[1] == 10
    assert permitted(900, 0.21)[1] == 20


def test_gate_is_strict_not_inclusive():
    """בדיוק על הסף זה לא מעל הסף."""
    assert permitted(100, 0.00)[1] == 0
    assert permitted(250, 0.10)[1] == 1
    assert permitted(500, 0.20)[1] == 3


def test_ladder_runs_downward():
    """הראיות נחלשות -> השלב יורד. זה הכיוון שקל להתעלם ממנו."""
    assert permitted(600, 0.25)[1] == 10
    assert permitted(600, 0.15)[1] == 3
    assert permitted(600, 0.05)[1] == 1
    assert permitted(600, -0.01)[1] == 0


def test_stage_is_monotone_in_evidence():
    prev = 0
    for lo in (-0.1, 0.0, 0.05, 0.11, 0.21, 0.40):
        acc = permitted(1000, lo)[1]
        assert acc >= prev
        prev = acc


def test_ladder_table_is_ordered_and_sane():
    accs = [s[1] for s in LADDER]
    ns = [s[2] for s in LADDER]
    assert accs == sorted(accs), "חשבונות מותרים חייבים לעלות"
    assert ns == sorted(ns), "מינימום עסקאות חייב לעלות"
    assert accs[-1] == 20, "התקרה של Apex"


# ── רווח סמך ─────────────────────────────────────────────────────

def test_ci_brackets_the_mean():
    r = seq(500, 0.30, seed=3)
    lo, hi = bootstrap_ci(r)
    assert lo < r.mean() < hi


def test_ci_narrows_with_more_trades():
    small = bootstrap_ci(seq(60, 0.30, seed=4))
    large = bootstrap_ci(seq(2000, 0.30, seed=4))
    assert (large[1] - large[0]) < (small[1] - small[0]) / 3


def test_small_sample_ci_spans_zero_even_with_a_real_edge():
    """הטעות שעשיתי: מדגם קטן עם קצה אמיתי עדיין לא מוכיח כלום."""
    lo, hi = bootstrap_ci(seq(20, 0.30, seed=11))
    assert lo < 0 < hi
    assert permitted(20, lo)[1] == 0


def test_ci_is_deterministic():
    r = seq(200, 0.25, seed=7)
    assert bootstrap_ci(r) == bootstrap_ci(r), "אותה רשומה -> אותה החלטה"


def test_a_true_edge_is_confirmed_at_scale():
    r = seq(1500, 0.35, seed=5)
    lo, _ = bootstrap_ci(r)
    assert lo > 0.10
    assert permitted(len(r), lo)[1] >= 10


def test_no_edge_never_opens_the_first_gate():
    for s in range(6):
        r = seq(800, 0.0, seed=100 + s)
        lo, _ = bootstrap_ci(r)
        assert permitted(len(r), lo)[1] <= 1


# ── רצפים ────────────────────────────────────────────────────────

@pytest.mark.parametrize("r,want", [
    ([], 0),
    ([2.0, 2.0], 0),
    ([-1, -1, -1], 3),
    ([-1, 2.0, -1, -1], 2),
    ([-1, -1, 2.0, -1], 2),
])
def test_longest_losing_run(r, want):
    assert longest_losing_run(np.array(r, dtype=float)) == want
