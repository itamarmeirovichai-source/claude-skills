#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trend_backtest.py — מומנטום סדרתי, לפי מוסקוביץ-אווי-פדרסן.

למה זה קיים
-----------
האסטרטגיה שבבוט נבחנה שלוש פעמים ולא הראתה קצה. זה בקטסט של משהו אחר:
קצה שהוא פרמיית סיכון מתועדת (Moskowitz, Ooi & Pedersen 2012, JFE) ולא
דפוס בגרף. מה שנמדד כאן הוא **גבול תחתון**, לא תוחלת. אם הגבול התחתון
של השארפ חיובי על שלושים שנה, יש לראשונה משהו שאפשר לבנות עליו.

מה זה, בדיוק
------------
- אות: סימן התשואה של 12 החודשים האחרונים. חיובי → לונג, שלילי → שורט.
- גודל: הפוך לתנודתיות הממומשת (60 יום), כך שכל נכס תורם סיכון שווה.
- איזון: חודשי, על סגירת יום המסחר האחרון, מוחזק חודש שלם.
- תיק: ממוצע שווה של הפוזיציות המנורמלות על פני הנכסים הזמינים.
- עלות: 10 נקודות בסיס על כל יחידת מחזור.

הפרמטרים נקבעו **מראש מהמאמר** ולא מהנתונים. רגישות מוצגת בנפרד
ומסומנת ככזו. זה ההבדל בין בקטסט לחיפוש.

שני יקומים
----------
--futures (ברירת המחדל כשהקובץ קיים): 54 חוזים עתידיים, 1984–2016, תשואות
יומיות עודפות, מריפו שחזור של המאמר. זה היקום של המאמר עצמו.
ראה data/README.md על המקור, מה נבדק, ומה חסר (2017 ואילך).

--etf: תשעה נכסים סחירים — S&P 500, מניות עולם, שלושה אג"ח ארה"ב, שני
אג"ח עולם, זהב, סחורות — במחירים הכוללים של הקרנות עצמן (SPY, VT, SHY,
IEF, TLT, BND/BWX, GLD, DBC), 1991–2026, מ-data/asset_classes.csv. רק
הקטעים ה"נצפים" (קרן או מדד אמיתיים) נכנסים; ההיסטוריה המדוגמת של
המאגר (1970–1991) מסומנת ב-asset_classes_observed.csv ומושמטת.
--etf-all מכניס גם אותה, כבדיקה בלבד. --excess מחשב את האות על
התשואה העודפת מעל אג"ח 1–3 שנים (ההגדרה של המאמר) במקום על התשואה
הכוללת; שני המספרים מדווחים, והאמת ביניהם. זה מה שאפשר לקנות מחר בחשבון
IBKR רגיל, ולכן זו המדידה שקובעת; היא כוללת גם 2017–2026, שחסרות
ביקום החוזים. --yahoo: המסלול הישן, קרנות סל מ-Yahoo, כשהרשת מאפשרת.
חוזים רציפים מ-Yahoo לא בשימוש בשום מצב — הם לא מתואמים לאחור וכל
גלגול מדפיס תשואה מזויפת.

מה זה לא מודד
-------------
לא איך זה מתנהג בתוך דרודאון נגרר של חברת פרופ. זו שאלה נפרדת, והיא
בסוף: prop_survival מריץ את סדרת התשואות דרך חשבון 50K עם 2,500$
דרודאון נגרר ומודד כמה מהנתיבים שורדים.
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

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "data"
SCRATCH = Path(os.environ.get(
    "PF_SCRATCH",
    "/tmp/claude-0/-home-user-claude-skills/"
    "83e06ccf-6299-5e6f-ac94-4ff79d8a5049/scratchpad"))
CACHE = SCRATCH / "data"

# ── יקום קרנות הסל ────────────────────────────────────────────────────
UNIVERSE = {
    "SPY": "מניות ארה\"ב גדולות (1993)", "QQQ": "נאסד\"ק 100 (1999)",
    "IWM": "מניות ארה\"ב קטנות (2000)", "EFA": "מפותחות מחוץ לארה\"ב (2001)",
    "EEM": "מתפתחות (2003)", "TLT": "אג\"ח ממשלת ארה\"ב 20+ (2002)",
    "IEF": "אג\"ח ממשלת ארה\"ב 7–10 (2002)", "LQD": "אג\"ח קונצרני (2002)",
    "HYG": "אג\"ח זבל (2007)", "GLD": "זהב (2004)", "SLV": "כסף (2006)",
    "DBC": "סל סחורות (2006)", "USO": "נפט (2006)", "UUP": "דולר (2007)",
    "FXE": "אירו (2005)", "VNQ": "נדל\"ן מניב (2004)",
}
ETF_PERIODS = (("2007", "2009"), ("2010", "2019"), ("2020", "2026"))

# ── יקום הנכסים הסחירים — ראה data/README.md ─────────────────────────
ASSET_CLASSES = {
    "USLCAP": "S&P 500 — SPY", "GLSTOCK": "מניות עולם — VT",
    "STT": "אג\"ח ארה\"ב 1–3 — SHY", "ITT": "אג\"ח ארה\"ב 7–10 — IEF",
    "LTT": "אג\"ח ארה\"ב 20+ — TLT", "GLBOND": "אג\"ח עולם — BND/BWX",
    "GLSTBOND": "אג\"ח עולם קצר — SHY/ISHG/BWZ",
    "GOLDPM": "זהב — GLD", "CMDTY": "סחורות — DBC",
}
ASSET_PERIODS = (("1991", "1999"), ("2000", "2009"),
                 ("2010", "2019"), ("2020", "2026"))
# היום הראשון שבו יש *תיק* נצפה: S&P, שלושה אג"ח ארה"ב ומניות עולם —
# חמישה נכסים. לפניו רק ה-S&P (מ-1970) וה-TLT (מ-1986) נצפים, ומומנטום
# על נכס אחד או שניים הוא ניסוי אחר, לא זה.
ASSET_START = "1991-10-29"

# ── יקום החוזים — ניקוי מתועד ─────────────────────────────────────────
# כל שורה כאן היא החלטה שנבדקה, לא ברירת מחדל.
FUTURES_DROP = ("VF",)                      # אין מטא-דאטה — לא ידוע מה זה
FUTURES_ZERO = (("EO", "1999-01-04"),)      # AEX הומר לאירו — ‎-52.6% הוא
                                            # פרט טכני, לא תשואה
FUTURES_REAL_EXTREMES = {                   # נבדקו, נשארים כמות שהם
    "1991-01-17": "תחילת מלחמת המפרץ — CL/CO/HO/QS ‎-29% עד ‎-33%",
    "1994-06-27": "קרה בברזיל — קפה ‎+27%",
    "2003-02-24": "זינוק גז טבעי ‎+38%",
}
FUTURES_PERIODS = (("1984", "1999"), ("2000", "2009"), ("2010", "2016"))


def load_futures(data_dir: Path = DATA_DIR) -> tuple:
    """(מחירים סינתטיים מהתשואות, תוויות). ראה data/README.md."""
    f = pd.read_csv(data_dir / "futures.csv", encoding="utf-8-sig")
    f["Date"] = pd.to_datetime(f["Date"], format="%m/%d/%y")
    f = f.set_index("Date").sort_index()
    f.columns = [c.strip() for c in f.columns]
    f = f.drop(columns=[c for c in FUTURES_DROP if c in f.columns])
    for sym, day in FUTURES_ZERO:
        f.loc[pd.Timestamp(day), sym] = 0.0
    meta = pd.read_csv(data_dir / "futures_list.csv")
    meta["Asset"] = meta["Asset"].str.strip()
    labels = {r.Asset: f"{r.FUTURES} — {r.ASSET_CLASS}"
              for r in meta.itertuples()}
    # אינדקס מחיר מהתשואות: cumprod מהיום התקף הראשון של כל מכשיר.
    # ffill על חורים פנימיים (חגים שונים בבורסות שונות) — יום בלי מסחר
    # הוא תשואה אפס, לא תשואה חסרה.
    px = pd.DataFrame({c: (1.0 + f[c].dropna()).cumprod() for c in f})
    return px.sort_index().ffill(), labels


def load_asset_classes(data_dir: Path = DATA_DIR,
                       observed_only: bool = True, start=None) -> tuple:
    """(מחירים כוללים, תוויות). ראה data/README.md.

    observed_only: רק ימים שהדגל שלהם 'observed' — קרן או מדד אמיתיים.
    ההיסטוריה המדוגמת נעשית NaN ולכן הנכס פשוט "נכנס" ביום הראשון
    שיש לו מחיר אמיתי, כמו חוזה שמתחיל להיסחר. הלוח הוא של NYSE
    (הימים שיש בהם S&P); ימי לונדון בלבד נופלים, והמחיר של יום כזה
    מתקפל לתשואה של יום NYSE הבא — ברמות, לא בתשואות, אז שום דבר
    לא הולך לאיבוד.
    """
    px = pd.read_csv(data_dir / "asset_classes.csv",
                     index_col="Date", parse_dates=True).sort_index()
    obs = pd.read_csv(data_dir / "asset_classes_observed.csv",
                      index_col="Date", parse_dates=True).sort_index()
    obs = obs.reindex(px.index).fillna(0).astype(bool)
    if observed_only:
        px = px.where(obs)
        start = start or ASSET_START
    if start:
        px = px.loc[start:]
    cal = px.index[px["USLCAP"].notna()]
    return px.ffill().reindex(cal), dict(ASSET_CLASSES)


def load_prices(tickers=None, offline=False) -> pd.DataFrame:
    """קרנות סל, מטמון CSV, yfinance רק כשחסר וכשהרשת מאפשרת."""
    tickers = list(tickers or UNIVERSE)
    CACHE.mkdir(parents=True, exist_ok=True)
    frames, missing = {}, []
    for t in tickers:
        f = CACHE / f"{t}.csv"
        if f.exists():
            frames[t] = pd.read_csv(f, index_col=0, parse_dates=True).iloc[:, 0]
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
        raise SystemExit("אין נתוני קרנות סל. הרשת חסומה? להריץ עם --futures.")
    px = pd.DataFrame(frames).sort_index()
    px.index = pd.to_datetime(px.index)
    if getattr(px.index, "tz", None) is not None:
        px.index = px.index.tz_localize(None)
    return px


# ── האסטרטגיה ─────────────────────────────────────────────────────────
def tsmom_positions(px: pd.DataFrame,
                    lookback=LOOKBACK_DAYS, vol_window=VOL_WINDOW,
                    target_vol=TARGET_VOL, long_only=False,
                    cash: str | None = None) -> pd.DataFrame:
    """פוזיציה לכל נכס לכל יום, ביחידות של הון.

    האות נקרא בסגירת יום המסחר האחרון בחודש ומוחזק לאורך החודש הבא.
    אין הצצה קדימה: הפוזיציה ביום t נגזרת ממידע עד סגירת t-1 בלבד,
    והבדיקה test_no_lookahead אוכפת את זה.

    cash: שם עמודה שמשמשת כמזומן. כשניתן, האות והנרמול מחושבים על
    התשואה *העודפת* מעליו — ההגדרה של המאמר (חוזים הם תשואה עודפת
    מלידה; קרנות סל לא). המזומן עצמו יוצא מהיקום. בלי cash, האות הוא
    על התשואה הכוללת — מה שרוב המשקיעים הפרטיים עושים, ומה שמטה אג"ח
    ללונג כשהריבית גבוהה.
    """
    if cash is not None:
        px = px.div(px[cash], axis=0)
        px[cash] = np.nan
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
              cost_bps=COST_BPS, max_gross=None) -> dict:
    """max_gross: תקרה לחשיפה הכוללת (סכום |משקלים|). 1.0 = בלי מינוף —
    בחודש שבו הנרמול מבקש יותר מ-100%, כל המשקלים מוקטנים יחד."""
    rets = px.pct_change()
    n_avail = pos.notna().sum(axis=1).replace(0, np.nan)
    w = pos.div(n_avail, axis=0).fillna(0.0)
    if max_gross is not None:
        g = w.abs().sum(axis=1)
        w = w.mul(np.minimum(1.0, max_gross / g.replace(0, np.nan))
                  .fillna(1.0), axis=0)
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
    under = (dd < 0).astype(int)
    runs = under.groupby((under != under.shift()).cumsum()).cumsum()
    yrs = d.groupby(d.index.year).apply(lambda s: (1 + s).prod() - 1)
    monthly = (1 + d).resample("ME").prod() - 1
    return dict(
        years=len(d) / TDAYS, ann_ret=ann_ret, ann_vol=ann_vol,
        sharpe=ann_ret / ann_vol if ann_vol > 0 else np.nan,
        max_dd=dd.min(), longest_dd_days=int(runs.max()),
        calmar=ann_ret / abs(dd.min()) if dd.min() < 0 else np.nan,
        worst_year=yrs.min(), best_year=yrs.max(), years_by=yrs,
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
            L = min(rng.geometric(p), T - k)
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
    עוברים את יעד ההערכה לפני שנוגעים ברצפה, וכמה נשרפים.
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
        eq = start + np.cumsum(notional * x[idx])
        peak = np.maximum.accumulate(np.concatenate([[start], eq]))[1:]
        floor = np.where(peak >= start + dd + 100.0, start + 100.0, peak - dd)
        hf = np.argmax(eq <= floor) if (eq <= floor).any() else -1
        ht = np.argmax(eq >= start + target) if (eq >= start + target).any() else -1
        if ht >= 0 and (hf < 0 or ht < hf):
            passed[i] = True
            days_to_pass[i] = ht + 1
        elif hf >= 0:
            blown[i] = True
    return dict(pass_rate=passed.mean(), blowup_rate=blown.mean(),
                neither=1 - passed.mean() - blown.mean(),
                median_days_to_pass=np.nanmedian(days_to_pass)
                if passed.any() else np.nan)


# ── דוח ───────────────────────────────────────────────────────────────
def _pct(x):
    return f"{x * 100:+.1f}%"


def report(px: pd.DataFrame, labels=None, periods=ETF_PERIODS,
           ref=("SPY", "IEF"), title="קרנות סל", no_leverage=False,
           cash: str | None = None) -> dict:
    labels = labels or UNIVERSE
    print("=" * 66)
    print(f"  מומנטום סדרתי על {title} — מוסקוביץ-אווי-פדרסן")
    print("=" * 66)
    print(f"  נכסים: {px.shape[1]}   "
          f"{px.index[0].date()} עד {px.index[-1].date()}")
    if cash:
        print(f"  האות: תשואה עודפת מעל {cash} (ההגדרה של המאמר). "
              f"{cash} עצמו לא בתיק.")
    else:
        print("  האות: תשואה כוללת (בלי ניכוי מזומן).")
    for t in px:
        s = px[t].dropna()
        print(f"    {t:<5} {labels.get(t, ''):<44} מ-{s.index[0].date()}")

    out = {}
    variants = [("לונג/שורט, כמו במאמר", False, None), ("לונג בלבד", True, None)]
    if no_leverage:
        variants.append(("לונג בלבד, חשיפה ≤ 100% — בלי מינוף", True, 1.0))
    for label, lo, cap in variants:
        pos = tsmom_positions(px, long_only=lo, cash=cash)
        pf = portfolio(px, pos, max_gross=cap)
        st = stats(pf["net"])
        boot = stationary_bootstrap_sharpe(st["monthly"])
        lo5, lo25, hi95 = np.percentile(boot, [5, 25, 95])
        out[label] = dict(stats=st, boot=boot, pf=pf)
        print(f"\n{'─' * 66}\n  {label}\n{'─' * 66}")
        print(f"  {st['years']:.1f} שנים, {st['n_months']} חודשים")
        print(f"  תשואה שנתית : {_pct(st['ann_ret'])}   "
              f"תנודתיות: {st['ann_vol'] * 100:.1f}%")
        print(f"  שארפ        : {st['sharpe']:.2f}")
        g = pf["weights"].abs().sum(axis=1)
        print(f"  חשיפה כוללת : ממוצע {g.mean() * 100:.0f}%   "
              f"מרבי {g.max() * 100:.0f}%")
        if st["ann_vol"] > 0:
            k = 0.10 / st["ann_vol"]
            print(f"  ב-10% תנודתיות: {_pct(st['ann_ret'] * k)}   "
                  f"(פי {k:.1f} מהחשיפה שלמעלה, דרודאון {_pct(st['max_dd'] * k)})")
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
        print("  לפי תקופה:")
        d = pf["net"]
        for a, b in periods:
            seg = d.loc[a:b]
            if len(seg) > TDAYS:
                s2 = stats(seg)
                print(f"    {a}–{b}: {_pct(s2['ann_ret']):>7}  "
                      f"שארפ {s2['sharpe']:.2f}  דרודאון {_pct(s2['max_dd'])}")
        if not lo:
            yb = st["years_by"]
            neg = yb[yb < 0]
            print(f"  שנים שליליות: {len(neg)} מתוך {len(yb)}  "
                  + ", ".join(f"{y}:{v * 100:+.0f}%" for y, v in neg.items()))

    # ייחוס
    ls_net = out["לונג/שורט, כמו במאמר"]["pf"]["net"]
    if ref[1] and {ref[0], ref[1]} <= set(px.columns):
        r = px[[ref[0], ref[1]]].pct_change().dropna()
        bh = (0.6 * r[ref[0]] + 0.4 * r[ref[1]]).loc[ls_net.index[0]:]
        name = f"60/40 {ref[0]}/{ref[1]} קנה-והחזק"
    elif ref[0] in px.columns:
        bh = px[ref[0]].pct_change().loc[ls_net.index[0]:].dropna()
        name = f"{ref[0]} לונג בלבד, קנה-והחזק"
    else:
        bh = None
    if bh is not None:
        s3 = stats(bh)
        print(f"\n{'─' * 66}\n  ייחוס: {name}, אותה תקופה\n{'─' * 66}")
        print(f"  תשואה שנתית : {_pct(s3['ann_ret'])}   שארפ {s3['sharpe']:.2f}   "
              f"דרודאון {_pct(s3['max_dd'])}")
        j = pd.concat([ls_net, bh], axis=1).dropna()
        print(f"  קורלציה של מומנטום לונג/שורט אליו: {j.corr().iloc[0, 1]:+.2f}")

    # רגישות — מסומנת
    print(f"\n{'─' * 66}\n  רגישות לחלון האות (לונג/שורט) — לא לבחור מכאן\n{'─' * 66}")
    print(f"  {'חלון':>8}{'תשואה':>10}{'שארפ':>8}{'דרודאון':>10}")
    for lb in (63, 126, 189, 252, 378):
        s4 = stats(portfolio(px, tsmom_positions(px, lookback=lb,
                                                 cash=cash))["net"])
        mark = "  ← המאמר" if lb == LOOKBACK_DAYS else ""
        print(f"  {lb // 21:>6}m {_pct(s4['ann_ret']):>9} {s4['sharpe']:>7.2f} "
              f"{_pct(s4['max_dd']):>9}{mark}")

    # התאמה למבנה הפרופ
    print(f"\n{'─' * 66}\n  בתוך חשבון 50K עם 2,500$ דרודאון נגרר\n{'─' * 66}")
    print("  הנומינל נבחר כך שתנודתיות ה-P&L היומית תהיה שבר מהדרודאון.")
    dvol = ls_net.std()
    print(f"  {'נומינל':>10}{'$vol/יום':>10}{'עוברים':>9}{'נשרפים':>9}"
          f"{'לא זה ולא זה':>14}{'ימים ליעד':>11}")
    for frac in (0.02, 0.04, 0.06, 0.08, 0.12):
        notional = frac * 2500.0 / dvol
        r = prop_survival(ls_net, notional)
        print(f"  {notional:>10,.0f}{frac * 2500:>10,.0f}"
              f"{r['pass_rate'] * 100:>8.0f}%{r['blowup_rate'] * 100:>8.0f}%"
              f"{r['neither'] * 100:>13.0f}%{r['median_days_to_pass']:>11.0f}")
    print("  'עוברים' = מגיעים ל-+3,000$ לפני שנוגעים ברצפה, בתוך שנה.")
    print("  'נשרפים' = נוגעים ברצפה קודם. הרצפה ננעלת ב-+100$ אחרי +2,600$.")
    return out


def main() -> int:
    args = set(sys.argv[1:])
    use_etf = bool(args & {"--etf", "--etf-all", "--yahoo"})
    if args & {"--etf", "--etf-all"}:
        observed_only = "--etf-all" not in args
        px, labels = load_asset_classes(observed_only=observed_only)
        print("  נתונים: תשעה נכסים סחירים במחירי הקרנות, ראה data/README.md.")
        print("  " + (f"רק קטעים נצפים — קרן או מדד אמיתיים — ומ-{ASSET_START}, "
                      "היום הראשון עם תיק של חמישה. המודל של 1970–1991 הושמט."
                      if observed_only else
                      "כולל ההיסטוריה המדוגמת 1970–1991 — בדיקה, לא ראיה."))
        print()
        report(px, labels=labels, periods=ASSET_PERIODS,
               ref=("USLCAP", "ITT"), title="נכסים סחירים", no_leverage=True,
               cash="STT" if "--excess" in args else None)
    elif not use_etf and (DATA_DIR / "futures.csv").exists():
        px, labels = load_futures()
        print("  נתונים: 54 חוזים עתידיים, 1984–2016. ראה data/README.md.")
        print("  ניקוי: VF הוסר (אין מטא); EO ב-1999-01-04 אופס (מעבר לאירו).")
        for day, why in FUTURES_REAL_EXTREMES.items():
            print(f"  נשמר כמות שהוא: {day} — {why}")
        print()
        report(px, labels=labels, periods=FUTURES_PERIODS,
               ref=("ES", None), title="חוזים עתידיים")
    else:
        px = load_prices(offline="--offline" in args)
        report(px)
    return 0


if __name__ == "__main__":
    sys.exit(main())
