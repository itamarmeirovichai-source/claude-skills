"""
tests/test_integrity.py

כל טסט פה משחזר שורה אמיתית מ-logs/trades.db.
אם טסט נופל, זו לא תקלה תיאורטית — זו עסקה שקרתה.
"""
import pytest
from integrity import (
    IntegrityError, compute_dollar_risk, assert_pnl_sign,
    calc_pnl_r, validate_trade_record, point_value,
)


# ── סיכון בדולרים ────────────────────────────────────────────────

def test_futures_risk_uses_point_value():
    # trades id 48: NQ, entry 30645, stop 30545 (100 נק'), חוזה אחד
    assert compute_dollar_risk("NQ", 30645.0, 30545.0, 1) == 2000.00


def test_stock_risk_is_shares_times_points():
    # trades_archive id 29: ES-proxy long, entry 705.59, stop ~703.62
    assert compute_dollar_risk("SPY", 705.59, 703.62, 10) == 19.70


def test_same_trade_always_gives_same_risk():
    """הבאג המקורי: חמש נוסחאות, חמישה ערכים לאותה עסקה."""
    args = ("ES", 7592.25, 7583.75, 1)
    assert len({compute_dollar_risk(*args) for _ in range(5)}) == 1


def test_zero_stop_distance_raises_not_returns_zero():
    # trades_archive id 28: entry == exit == 710.36, נרשם pnl_r=0.0
    with pytest.raises(IntegrityError, match="entry == stop_loss"):
        compute_dollar_risk("ES", 710.36, 710.36, 1)


def test_missing_quantity_raises():
    with pytest.raises(IntegrityError):
        compute_dollar_risk("ES", 7592.25, 7583.75, None)


# ── שומר הסימן ───────────────────────────────────────────────────

def test_archive_id_18_inverted_short_is_rejected():
    """ES A+ short: entry 653.06 -> exit 656.17 (המחיר עלה),
    אבל pnl נרשם +62.91. שורט מפסיד כשהמחיר עולה."""
    with pytest.raises(IntegrityError, match="הסימן סותר"):
        assert_pnl_sign("ES", "short", 653.06, 656.172361, 62.91)


def test_archive_id_27_inverted_long_is_rejected():
    """NQ B long: entry 641.28 -> exit 673.40 (המחיר עלה 32 נק'),
    אבל pnl נרשם -31.89. לונג מרוויח כשהמחיר עולה."""
    with pytest.raises(IntegrityError, match="הסימן סותר"):
        assert_pnl_sign("NQ", "long", 641.28, 673.40, -31.89)


def test_archive_id_29_correct_long_passes():
    """אותו קובץ, שורה תקינה: long, המחיר ירד, הפסד. עובר."""
    assert_pnl_sign("ES", "long", 705.59, 703.62, -91.25)


def test_archive_id_16_correct_short_passes():
    """short, המחיר ירד, רווח. עובר."""
    assert_pnl_sign("ES", "short", 675.51, 671.93, 93.02)


def test_flat_trade_is_not_flagged():
    assert_pnl_sign("ES", "long", 710.36, 710.36, 0.0)


# ── pnl_r ────────────────────────────────────────────────────────

def test_archive_id_30_winner_is_not_erased():
    """+$115.20 על סיכון של ~$38 נרשם כ-0.0R. זה מחק מנצח של 3R."""
    r = calc_pnl_r(115.20, 38.47)
    assert r is not None
    assert r == pytest.approx(2.9945, abs=1e-3)


def test_unknown_risk_returns_none_not_zero():
    """0.0 פירושו breakeven. 'לא ידוע' חייב להיות None."""
    assert calc_pnl_r(115.20, 0) is None
    assert calc_pnl_r(115.20, None) is None
    assert calc_pnl_r(None, 38.47) is None


def test_real_breakeven_is_zero_not_none():
    assert calc_pnl_r(0.0, 38.47) == 0.0


def test_archive_id_32_stop_overrun_is_preserved():
    """-5.14R זה חריגת סטופ אמיתית. אסור לעגל או לחתוך אותה."""
    assert calc_pnl_r(-197.76, 38.47) == pytest.approx(-5.140, abs=1e-3)


# ── שער הכתיבה ───────────────────────────────────────────────────

def test_analysis_id_zero_is_rejected():
    """כל 20 העסקאות ב-DB נרשמו עם analysis_id=0."""
    with pytest.raises(IntegrityError, match="analysis_id"):
        validate_trade_record("ES", "long", 0, 7592.25, 7583.75, 1)


def test_valid_open_returns_dollar_risk():
    dr = validate_trade_record("ES", "long", 3773, 7592.25, 7583.75, 1)
    assert dr == 425.00


def test_close_without_exit_reason_is_rejected():
    """10 עסקאות סגורות ב-DB עם exit_reason ריק."""
    with pytest.raises(IntegrityError, match="exit_reason"):
        validate_trade_record("ES", "long", 3773, 7592.25, 7583.75, 1,
                              exit_price=7583.75, pnl=-425.0,
                              exit_reason=None, closing=True)


def test_close_with_inverted_sign_is_rejected():
    with pytest.raises(IntegrityError, match="הסימן סותר"):
        validate_trade_record("NQ", "long", 3700, 641.28, 673.40, 1,
                              exit_price=673.40, pnl=-31.89,
                              exit_reason="stop", closing=True)


def test_full_valid_close_passes():
    dr = validate_trade_record("ES", "long", 3773, 7592.25, 7583.75, 1,
                               exit_price=7583.75, pnl=-425.0,
                               exit_reason="stop", closing=True)
    assert dr == 425.00
    assert calc_pnl_r(-425.0, dr) == -1.0


# ── ערכי נקודה ───────────────────────────────────────────────────

def test_point_values():
    assert point_value("ES") == 50.0
    assert point_value("MES") == 5.0
    assert point_value("NQ") == 20.0
    assert point_value("SPY") == 1.0      # מניה
    assert point_value("SPYM") == 1.0
