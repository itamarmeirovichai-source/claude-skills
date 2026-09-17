"""בדיקות לזיהוי הבאג ב-doctor.

הלוגיקה הזאת אומרת אם הבאג המרכזי תוקן. טעות בכיוון האחד היא אזעקת שווא
מעצבנת; טעות בכיוון השני היא בוט שבור שנראה תקין. כבר היו בה שני באגים —
סריקת טקסט שסימנה את הקובץ המתוקן כפגום, ואז התאמה לבלוק הדגמה שמחשב את
הבאג בכוונה. שתיהן נעולות כאן.
"""

from pathlib import Path

import pytest

from doctor import _proxy_verdict

BUGGY = "ratio = entry / etf_price"
FIXED = "ratio = futures_price / etf_price"


def verdict(src):
    return _proxy_verdict(src)


# ── הבאג ─────────────────────────────────────────────────────────

def test_the_original_bug_is_found():
    buggy, fixed = verdict(f"{BUGGY}\nproxy_entry = round(entry / ratio, 4)\n")
    assert buggy and not fixed


def test_the_bug_is_found_wherever_it_sits():
    src = (
        "def convert(entry, stop_loss, etf_price):\n"
        "    if etf_price <= 0:\n"
        "        raise ValueError\n"
        "    r = entry / etf_price\n"
        "    return round(entry / r, 4)\n"
    )
    assert verdict(src)[0]


def test_whitespace_does_not_hide_it():
    assert verdict("ratio   =   entry   /   etf_price\n")[0]


# ── התיקון ───────────────────────────────────────────────────────

def test_the_live_reference_pair_reads_as_fixed():
    buggy, fixed = verdict(f"{FIXED}\nproxy_entry = round(entry / ratio, 4)\n")
    assert fixed and not buggy


def test_the_invariant_call_reads_as_fixed():
    src = "assert_levels_preserved(e, s, t, pe, ps, pt, fut, etf)\n"
    assert verdict(src)[1]


@pytest.mark.parametrize("name", ["futures_price", "contract_price", "fut_price"])
def test_reference_price_naming_variants(name):
    assert verdict(f"ratio = {name} / etf_price\n")[1]


# ── אזעקות השווא שכבר קרו ────────────────────────────────────────

def test_the_bug_quoted_in_a_docstring_is_not_the_bug():
    """אזעקת השווא הראשונה: proxy_fix.py מצטט את הבאג כדי להסביר אותו."""
    src = (
        '"""התיקון.\n'
        "\n"
        "    ratio       = entry / etf_price\n"
        "    proxy_entry = round(entry / ratio, 4)\n"
        "\n"
        'זה מה שהיה שגוי."""\n'
        f"{FIXED}\n"
    )
    buggy, fixed = verdict(src)
    assert not buggy, "ציטוט בתיעוד אינו קוד שרץ"
    assert fixed


def test_the_bug_in_a_comment_is_not_the_bug():
    src = f"# היה פעם: ratio = entry / etf_price\n{FIXED}\n"
    assert not verdict(src)[0]


@pytest.mark.parametrize("target", ["buggy_ratio", "demo_ratio", "old_ratio",
                                    "before_ratio", "wrong_ratio"])
def test_a_deliberate_demonstration_is_not_the_bug(target):
    """אזעקת השווא השנייה: ההדגמה מחשבת את הבאג בכוונה."""
    src = f"{target} = entry / etf_price\n{FIXED}\n"
    buggy, fixed = verdict(src)
    assert not buggy and fixed


def test_the_real_proxy_fix_file_reads_as_fixed():
    """הבדיקה שתופסת רגרסיה אמיתית: הקובץ שאנחנו מחלקים."""
    src = (Path(__file__).resolve().parent / "proxy_fix.py").read_text()
    buggy, fixed = verdict(src)
    assert fixed, "הקובץ המתוקן חייב להיקרא כמתוקן"
    assert not buggy, "ובלי לסמן את בלוק ההדגמה שבו"


# ── מקרים שבהם עדיף לשאול מאשר לנחש ──────────────────────────────

def test_both_present_is_reported_as_both():
    """ניתוח סטטי לא יודע איזה מסלול רץ. עדיף לומר מאשר להכריע."""
    src = f"{FIXED}\nstale = entry / etf_price\nassert_levels_preserved(1,2,3,4,5,6,7,8)\n"
    buggy, fixed = verdict(src)
    assert buggy and fixed


def test_an_unrelated_file_is_neither():
    assert verdict("x = 1\ny = x + 2\n") == (False, False)


def test_broken_python_returns_no_verdict():
    assert verdict("def f(:\n") is None


def test_an_empty_file_is_neither():
    assert verdict("") == (False, False)


# ── דברים שלא אמורים להיתפס ──────────────────────────────────────

def test_a_division_by_something_else_is_not_the_bug():
    assert not verdict("ratio = entry / quantity\nx = entry / 2\n")[0]


def test_multiplication_is_not_the_bug():
    assert not verdict("ratio = entry * etf_price\n")[0]
