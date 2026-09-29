#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trend_backtest.py — מומנטום סדרתי על סל קרנות סל, לפי מוסקוביץ-אווי-פדרסן.

למה זה קיים
-----------
האסטרטגיה שבבוט נבחנה שלוש פעמים ולא הראתה קצה. זה בקטסט של משהו אחר:
קצה שהוא פרמיית סיכון מתועדת (Moskowitz, Ooi & Pedersen 2012, JFE) ולא
דפוס בגרף. מה שנמדד כאן הוא **גבול תחתון**, לא תוחלת. אם הגבול התחתון
של השארפ חיובי על עשרים שנה, יש לראשונה משהו שאפשר לבנות עליו.

מה זה, בדיוק
------------
- אות: סימן התשואה של 12 החודשים האחרונים. חיובי → לונג, שלילי → שורט.
- גודל: הפוך לתנודתיות הממומשת (60 יום), כך שכל נכס תורם סיכון שווה.
- איזון: חודשי, על סגירת יום המסחר האחרון, מוחזק חודש שלם.
- תיק: ממוצע שווה של הפוזיציות המנורמלות על פני הנכסים הזמינים.
- עלות: 10 נקודות בסיס על כל יחידת מחזור — שמרני לקרנות סל.

הפרמטרים נקבעו **מראש מהמאמר** ולא מהנתונים. רגישות מוצגת בנפרד
ומסומנת ככזו. זה ההבדל בין בקטסט לחיפוש.

למה קרנות סל ולא חוזים
----------------------
חוזים רציפים מ-Yahoo לא מתואמים לאחור: בכל גלגול יש פער מחיר שנראה
כמו תשואה. על סדרות תשואה זה כמה תשואות מזויפות בשנה. קרנות סל הן מה
שאפשר לקנות, עלות הגלגול כבר בתוכן, ואין פערים. המספר ייצא נמוך
מהאקדמי — וזה המספר הכן.

מה זה לא מודד
-------------
לא איך זה מתנהג בתוך דרודאון נגרר של חברת פרופ. זו שאלה נפרדת, והיא
בסוף הקובץ: prop_survival מריץ את סדרת התשואות דרך חשבון 50K עם
2,500$ דרודאון נגרר ומודד כמה מהנתיבים שורדים.

שימוש
-----
    python3 trend_backtest.py            # מושך (עם מטמון), מריץ, מדפיס
    python3 trend_backtest.py --offline  # רק מהמטמון
"""
from __future__ import annotations

import os
import sys

from pathlib import Path

import numpy as np
import pandas as pd

# ── פרמטרים, קבועים מראש ─────────────────────────────────────────────
LOOKBACK_DAYS = 252      # 12 חודשי מסחר — האות מהמאמר
VOL_WINDOW = 60          # ימי מסחר לתנודתיות ממומשת
TARGET_VOL = 0.10        # יעד תנודתיות שנתית לכל נכס
COST_BPS = 10.0          # לכל יחידת מחזור
TDAYS = 252

# סל מפוזר עם היסטוריה ארוכה. התאריך בסוגריים הוא תחילת הסדרה.
UNIVERSE = {
    "SPY": "מניות ארה\"ב גדולות (1993)",
    "QQQ": "נאסד\"ק 100 (1999)",
    "IWM": "מניות ארה\"ב קטנות (2000)",
    "EFA": "מפותחות מחוץ לארה\"ב (2001)",
    "EEM": "מתפתחות (2003)",
    "TLT": "אג\"ח ממשלת ארה\"ב 20+ (2002)",
    "IEF": "אג\"ח ממשלת ארה\"ב 7–10 (2002)",
    "LQD": "אג\"ח קונצרני דירוג השקעה (2002)",
    "HYG": "אג\"ח זבל (2007)",
    "GLD": "זהב (2004)",
    "SLV": "כסף (2006)",
    "DBC": "סל סחורות (2006)",
    "USO": "נפט (2006)",
    "UUP": "דולר מול סל (2007)",
    "FXE": "אירו (2005)",
    "VNQ": "נדל\"ן מניב ארה\"ב (2004)",
}

SCRATCH = Path(os.environ.get(
    "PF_SCRATCH",
    "/tmp/claude-0/-home-user-claude-skills/"
    "83e06ccf-6299-5e6f-ac94-4ff79d8a5049/scratchpad"))
CACHE = SCRATCH / "data"


# ── נתונים ────────────────────────────────────────────────────────────
def load_prices(tickers=None, offline=False) -> pd.DataFrame:
    """מחירי סגירה מתואמים, יומיים. מטמון ב-CSV; yfinance רק כשחסר."""
    tickers = list(tickers or UNIVERSE)
    CACHE.mkdir(parents=True, exist_ok=True)
    frames = {}
    missing = []
    for t in tickers:
        f = CACHE / f"{t}.csv"
        if f.exists():
            s = pd.read_csv(f, index_col=0, parse_dates=True).iloc[:, 0]
            frames[t] = s
        else:
            missing.append(t)
    if missing and not offline:
        import yfinance as yf                                   # noqa: WPS433
        raw = yf.download(missing, start="1990-01-01", auto_adjust=True,
                          progress=False, group_by="ticker", threads=True)
        for t in missing:
            try:
                s = raw[t]["Close"].dropna() if len(missing) > 1 \
                    else raw["Close"].dropna()
            except (KeyError, TypeError):
                continue
            if len(s) < LOOKBACK_DAYS + VOL_WINDOW:
                continue
            s.name = t
            s.to_csv(CACHE / f"{t}.csv")
            frames[t] = s
    if not frames:
        raise SystemExit("אין נתונים. להריץ בלי --offline, או לבדוק רשת.")
    px = pd.DataFrame(frames).sort_index()
    px.index = pd.to_datetime(px.index)
    if getattr(px.index, "tz", None) is not None:
        px.index = px.index.tz_localize(None)
    return px


# ── האסטרטגיה ─────────────────────────────────────────────────────────
def tsmom_positions(px: pd.DataFrame,
                    lookback=LOOKBACK_DAYS, vol_window=VOL_WINDOW,
                    target_vol=TARGET_VOL, long_only=False) -> pd.DataFrame:
    """פוזיציה לכל נכס לכל יום, ביחידות של הון.

    האות נקרא בסגירת יום המסחר האחרון בחודש ומוחזק לאורך החודש הבא.
    אין הצצה קדימה: הפוזיציה ביום t נגזרת ממידע עד סגירת t-1 בלבד,
    והבדיקה test_no_lookahead אוכפת את זה.
    """
    rets = px.pct_change()
    lb = px / px.shift(lookback) - 1.0
    vol = rets.rolling(vol_window).std() * np.sqrt(TDAYS)
    sig = np.sign(lb)
    if long_only:
        sig = sig.clip(lower=0.0)
    raw = sig * (target_vol / vol)
    raw = raw.where(np.isfinite(raw))
    # האות של יום המסחר האחרון בכל חודש → מוחזק בחודש שאחריו. shift(1)
    # על הימים מבטיח שסגירת היום עצמו לא משמשת לפוזיציה של אותו יום.
    #
    # לא resample("ME"): התווית שלו היא סוף החודש הקלנדרי, וכשזה נופל
    # על סוף שבוע היא מאוחרת מיום המסחר האחרון. ffill אז מחמיץ את האות
    # ביום אחד והפוזיציה מתחלפת ביום השני של החודש במקום בראשון.
    # test_position_is_constant_within_a_month תפס את זה.
    me = raw.groupby(raw.index.to_period("M")).tail(1)
    pos = me.reindex(px.index, method="ffill").shift(1)
    return pos


def portfolio(px: pd.DataFrame, pos: pd.DataFrame,
              cost_bps=COST_BPS) -> dict:
    rets = px.pct_change()
    n_avail = pos.notna().sum(axis=1).replace(0, np.nan)
    w = pos.div(n_avail, axis=0).fillna(0.0)
    gross = (w * rets.fillna(0.0)).sum(axis=1)
    turnover = w.diff().abs().sum(axis=1).fillna(0.0)
    net = gross - turnover * cost_bps / 1e4
    first = pos.notna().any(axis=1).idxmax()
    net, gross, turnover, w = (x.loc[first:] for x in (net, gross, turnover, w))
    return dict(net=net, gross=gross, turnover=turnover, weights=w)


# ── סטטיסטיקה ─────────────────────────────────────────────────────────
def stats(daily: pd.Series) -> dict:
    d = daily.dropna()
    ann_ret = d.mean() * TDAYS
    ann_vol = d.std() * np.sqrt(TDAYS)
    cum = (1 + d).cumprod()
    dd = cum / cum.cummax() - 1
    # משך הדרודאון הארוך ביותר, בימי מסחר
    under = (dd < 0).astype(int)
    runs = under.groupby((under != under.shift()).cumsum()).cumsum()
    yrs = d.groupby(d.index.year).apply(lambda s: (1 + s).prod() - 1)
    monthly = (1 + d).resample("ME").prod() - 1
    return dict(
        years=len(d) / TDAYS, ann_ret=ann_ret, ann_vol=ann_vol,
        sharpe=ann_ret / ann_vol if ann_vol > 0 else np.nan,
        max_dd=dd.min(), longest_dd_days=int(runs.max()),
        calmar=ann_ret / abs(dd.min()) if dd.min() < 0 else np.nan,
        worst_year=yrs.min(), best_year=yrs.max(),
        pct_pos_months=(monthly > 0).mean(), n_months=len(monthly),
        monthly=monthly, cum=cum, dd=dd,
    )


def stationary_bootstrap_sharpe(monthly: pd.Series, n=5000,
                                mean_block=6, seed=0) -> np.ndarray:
    """Politis–Romano. בלוקים באורך גאומטרי, ממוצע mean_block חודשים,
    כדי לשמר אוטוקורלציה. מחזיר התפלגות של שארפ שנתי."""
    x = monthly.dropna().values
    T = len(x)
    rng = np.random.default_rng(seed)
    out = np.empty(n)
    p = 1.0 / mean_block
    for i in range(n):
        idx = np.empty(T, dtype=int)
        k = 0
        while k < T:
            start = rng.integers(0, T)
            L = rng.geometric(p)
            L = min(L, T - k)
            idx[k:k + L] = (start + np.arange(L)) % T
            k += L
        s = x[idx]
        sd = s.std(ddof=1)
        out[i] = s.mean() / sd * np.sqrt(12) if sd > 0 else 0.0
    return out


# ── התאמה למבנה הפרופ ─────────────────────────────────────────────────
def prop_survival(daily: pd.Series, notional: float, start=50_000.0,
                  dd=2_500.0, target=3_000.0, n=3000, horizon_days=252,
                  mean_block=20, seed=0) -> dict:
    """מריץ נתיבי bootstrap של התשואה היומית דרך חשבון עם דרודאון נגרר.

    הרצפה עוקבת אחרי השיא עד שהשיא מגיע ל-start+dd+100, ואז ננעלת
    ב-start+100 לתמיד (כללי Apex, כמו ב-apex_model). המדד: כמה נתיבים
    עוברים את יעד ההערכה לפני שנוגעים ברצפה, וכמה שורדים שנה שלמה.
    """
    x = daily.dropna().values
    T = len(x)
    rng = np.random.default_rng(seed)
    p = 1.0 / mean_block
    passed = np.zeros(n, bool)
    blown = np.zeros(n, bool)
    days_to_pass = np.full(n, np.nan)
    for i in range(n):
        idx = np.empty(horizon_days, dtype=int)
        k = 0
        while k < horizon_days:
            s0 = rng.integers(0, T)
            L = min(rng.geometric(p), horizon_days - k)
            idx[k:k + L] = (s0 + np.arange(L)) % T
            k += L
        pnl = notional * x[idx]
        eq = start + np.cumsum(pnl)
        peak = np.maximum.accumulate(np.concatenate([[start], eq]))[1:]
        floor = np.where(peak >= start + dd + 100.0, start + 100.0, peak - dd)
        hit_floor = np.argmax(eq <= floor) if (eq <= floor).any() else -1
        hit_target = np.argmax(eq >= start + target) \
            if (eq >= start + target).any() else -1
        if hit_target >= 0 and (hit_floor < 0 or hit_target < hit_floor):
            passed[i] = True
            days_to_pass[i] = hit_target + 1
        if hit_floor >= 0 and not passed[i]:
            blown[i] = True
    return dict(pass_rate=passed.mean(), blowup_rate=blown.mean(),
                neither=1 - passed.mean() - blown.mean(),
                median_days_to_pass=np.nanmedian(days_to_pass)
                if passed.any() else np.nan)


# ── דוח ───────────────────────────────────────────────────────────────
def _pct(x):
    return f"{x * 100:+.1f}%"


def report(px: pd.DataFrame) -> dict:
    print("=" * 66)
    print("  מומנטום סדרתי על קרנות סל — מוסקוביץ-אווי-פדרסן")
    print("=" * 66)
    print(f"  נכסים: {px.shape[1]}   "
          f"{px.index[0].date()} עד {px.index[-1].date()}")
    for t in px:
        s = px[t].dropna()
        print(f"    {t:<5} {UNIVERSE.get(t, ''):<38} מ-{s.index[0].date()}")

    out = {}
    for label, lo in (("לונג/שורט, כמו במאמר", False), ("לונג בלבד", True)):
        pos = tsmom_positions(px, long_only=lo)
        pf = portfolio(px, pos)
        st = stats(pf["net"])
        boot = stationary_bootstrap_sharpe(st["monthly"])
        lo5, lo25, hi95 = np.percentile(boot, [5, 25, 95])
        out[label] = dict(stats=st, boot=boot, pf=pf)
        print(f"\n{'─' * 66}\n  {label}\n{'─' * 66}")
        print(f"  {st['years']:.1f} שנים, {st['n_months']} חודשים")
        print(f"  תשואה שנתית : {_pct(st['ann_ret'])}   "
              f"תנודתיות: {st['ann_vol'] * 100:.1f}%")
        print(f"  שארפ        : {st['sharpe']:.2f}")
        print(f"  bootstrap   : אחוזון 5 = {lo5:.2f}   "
              f"אחוזון 25 = {lo25:.2f}   אחוזון 95 = {hi95:.2f}")
        print(f"  P(שארפ ≤ 0) : {(boot <= 0).mean() * 100:.1f}%")
        print(f"  דרודאון מרבי: {_pct(st['max_dd'])}   "
              f"הארוך ביותר: {st['longest_dd_days']} ימי מסחר "
              f"({st['longest_dd_days'] / TDAYS:.1f} שנים)")
        print(f"  שנה גרועה   : {_pct(st['worst_year'])}   "
              f"טובה: {_pct(st['best_year'])}   "
              f"חודשים חיוביים: {st['pct_pos_months'] * 100:.0f}%")
        print(f"  מחזור שנתי  : {pf['turnover'].mean() * TDAYS:.1f}x   "
              f"עלות שנתית: {(pf['gross'] - pf['net']).mean() * TDAYS * 100:.2f}%")

        # תת-תקופות: לפני/אחרי 2009 (קריסת המומנטום), והעשור האחרון
        print("  לפי תקופה:")
        d = pf["net"]
        for a, b in (("2007", "2009"), ("2010", "2019"), ("2020", "2026")):
            seg = d.loc[a:b]
            if len(seg) > TDAYS:
                s2 = stats(seg)
                print(f"    {a}–{b}: {_pct(s2['ann_ret']):>7}  "
                      f"שארפ {s2['sharpe']:.2f}  דרודאון {_pct(s2['max_dd'])}")

    # ייחוס: 60/40 קנה-והחזק על אותה תקופה
    if {"SPY", "IEF"} <= set(px.columns):
        r = px[["SPY", "IEF"]].pct_change().dropna()
        bh = (0.6 * r["SPY"] + 0.4 * r["IEF"]).loc[out["לונג בלבד"]["pf"]["net"].index[0]:]
        s3 = stats(bh)
        print(f"\n{'─' * 66}\n  ייחוס: 60/40 קנה-והחזק, אותה תקופה\n{'─' * 66}")
        print(f"  תשואה שנתית : {_pct(s3['ann_ret'])}   שארפ {s3['sharpe']:.2f}   "
              f"דרודאון {_pct(s3['max_dd'])}")

    # רגישות לחלון האות — מסומנת ככזו
    print(f"\n{'─' * 66}\n  רגישות לחלון האות (לונג/שורט) — לא לבחור מכאן\n{'─' * 66}")
    print(f"  {'חלון':>8}{'תשואה':>10}{'שארפ':>8}{'דרודאון':>10}")
    for lb in (63, 126, 189, 252, 378):
        pf2 = portfolio(px, tsmom_positions(px, lookback=lb))
        s4 = stats(pf2["net"])
        mark = "  ← המאמר" if lb == LOOKBACK_DAYS else ""
        print(f"  {lb // 21:>6}m {_pct(s4['ann_ret']):>9} {s4['sharpe']:>7.2f} "
              f"{_pct(s4['max_dd']):>9}{mark}")

    # התאמה למבנה הפרופ
    print(f"\n{'─' * 66}\n  בתוך חשבון 50K עם 2,500$ דרודאון נגרר\n{'─' * 66}")
    print("  הנומינל נבחר כך שתנודתיות ה-P&L היומית תהיה שבר מהדרודאון.")
    d = out["לונג/שורט, כמו במאמר"]["pf"]["net"]
    dvol = d.std()
    print(f"  {'נומינל':>10}{'$vol/יום':>10}{'עוברים':>9}{'נשרפים':>9}"
          f"{'לא זה ולא זה':>14}{'ימים ליעד':>11}")
    for frac in (0.02, 0.04, 0.06, 0.08):
        notional = frac * 2500.0 / dvol
        r = prop_survival(d, notional)
        print(f"  {notional:>10,.0f}{frac * 2500:>10,.0f}"
              f"{r['pass_rate'] * 100:>8.0f}%{r['blowup_rate'] * 100:>8.0f}%"
              f"{r['neither'] * 100:>13.0f}%{r['median_days_to_pass']:>11.0f}")
    print("  'עוברים' = מגיעים ל-+3,000$ לפני שנוגעים ברצפה, בתוך שנה.")
    print("  'נשרפים' = נוגעים ברצפה קודם. הרצפה ננעלת ב-+100$ אחרי +2,600$.")
    return out


def main() -> int:
    offline = "--offline" in sys.argv
    px = load_prices(offline=offline)
    report(px)
    return 0


if __name__ == "__main__":
    sys.exit(main())
