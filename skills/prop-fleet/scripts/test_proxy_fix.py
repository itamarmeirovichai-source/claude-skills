"""בדיקות ל-proxy_fix. הראשונה משחזרת את הבאג המקורי."""

import pytest

from proxy_fix import (
    ProxyConversionError,
    assert_levels_preserved,
    convert_levels,
)

# ES סביב 7,500 מול SPY סביב 700 — סדרי הגודל מהרשומות האמיתיות.
FUT, ETF = 7500.00, 700.00
RATIO = FUT / ETF


def test_the_original_bug_is_caught():
    """ratio = entry / etf_price מכריח את הכניסה להיות מחיר השוק.

    האינווריאנטה חייבת לדחות את זה.
    """
    entry, stop, tp = 7492.50, 7484.00, 7509.50
    buggy_ratio = entry / ETF
    buggy_entry = round(entry / buggy_ratio, 4)
    buggy_sl = round(stop / buggy_ratio, 4)
    buggy_tp = round(tp / buggy_ratio, 4)

    assert buggy_entry == pytest.approx(ETF), "הבאג אמור להחזיר בדיוק את מחיר השוק"

    with pytest.raises(ProxyConversionError, match="entry"):
        assert_levels_preserved(entry, stop, tp,
                                buggy_entry, buggy_sl, buggy_tp, FUT, ETF)


def test_entry_below_market_stays_below_market():
    entry, stop, tp = 7492.50, 7484.00, 7509.50
    pe, ps, pt = convert_levels(entry, stop, tp, FUT, ETF)
    assert pe < ETF, "כניסת לונג מתחת לשוק חייבת להישאר מתחת לשוק"
    assert pe == pytest.approx(entry / RATIO, abs=1e-4)
    assert ps == pytest.approx(stop / RATIO, abs=1e-4)
    assert pt == pytest.approx(tp / RATIO, abs=1e-4)


def test_short_entry_above_market_stays_above_market():
    entry, stop, tp = 7508.00, 7516.50, 7491.00
    pe, ps, pt = convert_levels(entry, stop, tp, FUT, ETF)
    assert pe > ETF
    assert ps > pe, "הסטופ של שורט מעל הכניסה"
    assert pt < pe


def test_risk_reward_survives_conversion():
    entry, stop, tp = 7492.50, 7484.00, 7509.50
    pe, ps, pt = convert_levels(entry, stop, tp, FUT, ETF)
    before = abs(tp - entry) / abs(entry - stop)
    after = abs(pt - pe) / abs(pe - ps)
    assert after == pytest.approx(before, rel=1e-3)


def test_entry_at_market_is_the_degenerate_case():
    """כשהאסטרטגיה נכנסת בשוק, הבאג והתיקון מסכימים.

    בדיוק המקרה שהסתיר את הבאג.
    """
    pe, _, _ = convert_levels(FUT, 7491.50, 7517.00, FUT, ETF)
    assert pe == pytest.approx(ETF, abs=1e-4)


def test_take_profit_may_be_absent():
    pe, ps, pt = convert_levels(7492.50, 7484.00, None, FUT, ETF)
    assert pt is None
    assert pe > 0 and ps > 0


def test_direction_survives_conversion():
    """שמירת המיקום היחסי כבר מחייבת את זה — כאן זה מאומת במפורש."""
    long_e, long_s = 7492.50, 7484.00
    pe, ps, _ = convert_levels(long_e, long_s, None, FUT, ETF)
    assert pe > ps, "לונג: הכניסה מעל הסטופ"

    short_e, short_s = 7508.00, 7516.50
    pe, ps, _ = convert_levels(short_e, short_s, None, FUT, ETF)
    assert pe < ps, "שורט: הכניסה מתחת לסטופ"


def test_a_stop_moved_by_hand_is_caught():
    """סטופ שעבר המרה שגויה נתפס גם כשהכניסה תקינה."""
    with pytest.raises(ProxyConversionError, match="stop_loss"):
        assert_levels_preserved(7492.50, 7484.00, None,
                                699.30, 699.50, None, FUT, ETF)


@pytest.mark.parametrize("fut,etf", [(0, 700.0), (-1, 700.0), (None, 700.0),
                                     (7500.0, 0), (7500.0, -5), (7500.0, None)])
def test_non_positive_reference_prices_rejected(fut, etf):
    with pytest.raises(ProxyConversionError):
        convert_levels(7492.50, 7484.00, 7509.50, fut, etf)


@pytest.mark.parametrize("entry,stop", [(0, 7484.0), (-1, 7484.0), (None, 7484.0),
                                        (7492.5, 0), (7492.5, None)])
def test_non_positive_levels_rejected(entry, stop):
    with pytest.raises(ProxyConversionError):
        convert_levels(entry, stop, 7509.50, FUT, ETF)


def test_absurd_ratio_is_rejected():
    """יחס שגוי בסדר גודל -> מחיר מחוץ לטווח השפוי."""
    with pytest.raises(ProxyConversionError, match="שפוי"):
        convert_levels(7492.50, 7484.00, 7509.50, 7500.0, 700_000.0)


def test_qqq_scale_also_works():
    fut, etf = 25_400.00, 610.00
    entry, stop, tp = 25_380.00, 25_346.00, 25_448.00
    pe, ps, pt = convert_levels(entry, stop, tp, fut, etf)
    assert pe < etf
    assert pe / etf == pytest.approx(entry / fut, rel=1e-6)
