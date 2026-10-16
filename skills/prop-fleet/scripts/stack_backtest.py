#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stack_backtest.py — ערימה של קצוות לא-מתואמים, כמו שהגדולים עושים.

למה זה קיים
-----------
`what-the-giants-do.md` הראה ש-20% בשנה עם דרודאון של 15% הוא, בהגדרה,
תוצאה של שארפ 2, ושמגיעים לשארפ 2 לא עם קצה אחד טוב יותר אלא עם כמה
קצוות לא-מתואמים (שארפ ערימה ≈ שארפ יחיד × √N). הסקריפט הזה בונה את
הערימה מרכיבים שיש להם ראיות אקדמיות, בודק כל אחד לבד באותו גבול תחתון,
ומודד מה הערימה נותנת.

הרכיבים, כולם במפרט שנקבע מראש מהספרות
--------------------------------------
חוזים (54, 1984–2016, `data/futures.csv`):
  tsmom  מומנטום סדרתי — Moskowitz, Ooi & Pedersen 2012 (trend_backtest.py).
  xsmom  מומנטום חתך-רוחבי — Asness, Moskowitz & Pedersen 2013: תשואת 12
         חודשים בלי החודש האחרון, דירוג בתוך כל מחלקת נכסים.
  value  ערך — אותו מאמר: היפוך 5 שנים, log(ממוצע המחיר לפני 4.5–5.5
         שנים / המחיר היום), דירוג בתוך כל מחלקה. במאמר זה המדד של
         סחורות; למטבעות/אג"ח/מדדים המאמר משתמש ב-PPP, תשואה ריאלית
         ו-B/M, שאין לנו. כאן הוא proxy לכולם, וזה נאמר.
נכסים סחירים (2010–2026):
  6040      60% S&P / 40% IEF — הבטא, הרכיב החינמי.
  trend     מומנטום סדרתי לונג בלבד על תשעת הנכסים, אות עודף (trend_backtest).
  overnight לונג S&P מהסגירה לפתיחה כל לילה — Cliff, Cooper & Gulen 2008;
            Lou, Polk & Skouras 2019. במחירי מדד; ראה ON_START.

מה לא נבדק ולמה
---------------
carry: דורש עקום חוזים (מחיר החוזה הקרוב והבא). בנתונים יש רק תשואות.
פרמיית הטווח של אג"ח — ה-carry הפשוט — כבר בתוך רגל האג"ח של 60/40.

כללי הערימה
-----------
כל רכיב מנורמל ל-10% תנודתיות לפי תנודתיות **עבר** בלבד (252 יום,
מתעדכן בסוף חודש, מופעל בחודש הבא, תקרה ×5). הערימה = ממוצע שווה של
הרכיבים המנורמלים, ואז שוב מנורמלת ל-10% באותה שיטה. אין כאן נרמול לפי
התנודתיות של כל המדגם — זו הייתה הצצה קדימה קטנה בהרצה של
`what-the-giants-do.md`, והיא הוחלפה.
"""
from __future__ import annotations

import sys

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from trend_backtest import (DATA_DIR, TDAYS, load_asset_classes,  # noqa: E402
                            load_futures, portfolio, prop_survival,
                            stationary_bootstrap_sharpe, stats,
                            tsmom_positions)

TARGET_VOL = 0.10
SCALE_WINDOW = 252
SCALE_MIN = 126
SCALE_CAP = 5.0
VOL_WINDOW = 60
COST_BPS = 10.0            # לכל יחידת מחזור, כמו ב-trend_backtest
XSMOM_LOOKBACK = 252       # 12 חודשים
XSMOM_SKIP = 21            # בלי החודש האחרון
VALUE_NEAR = int(4.5 * TDAYS)
VALUE_FAR = int(5.5 * TDAYS)

# פתיחות המדד לפני 2010 מזויפות: ב-64%–92% מהימים הן שוות לסגירה של
# אתמול (נבדק לפי עשור, ראה data/README.md). מ-2010: 6% ואז 0.1%.
ON_START = "2010-01-01"
# ES: עמלה 0.85$ + עמלות 1.40$ לצד, החלקה 0.25 טיק (3.125$) לצד, על
# נומינל של כ-300 אלף$ → כ-0.4 נקודות בסיס הלוך-חזור. 0.5 כבסיס שמרני.
ON_COST_BPS = 0.5


# ── כלים ──────────────────────────────────────────────────────────────
def month_end_rows(idx: pd.DatetimeIndex) -> pd.DatetimeIndex:
    s = idx.to_series()
    return pd.DatetimeIndex(s.groupby(idx.to_period("M")).max().values)


def hold_monthly(month_end_values: pd.DataFrame, idx) -> pd.DataFrame:
    """ערך שנקבע בסגירת יום המסחר האחרון בחודש מוחזק מהיום שאחריו."""
    return month_end_values.reindex(idx, method="ffill").shift(1)


def vol_scale(r: pd.Series, target=TARGET_VOL, window=SCALE_WINDOW,
              min_periods=SCALE_MIN, cap=SCALE_CAP) -> pd.Series:
    """מנרמל סדרת תשואות לתנודתיות יעד לפי תנודתיות *עבר* בלבד.

    המכפיל נקבע בסוף כל חודש מהתנודתיות הממומשת עד אותו יום, ומופעל
    מהיום שאחריו. תשואה של יום t לא משפיעה על המכפיל של יום t.
    """
    r = r.dropna()
    vol = r.rolling(window, min_periods=min_periods).std() * np.sqrt(TDAYS)
    k = (target / vol).clip(upper=cap)
    me = k.loc[k.index.isin(month_end_rows(k.index))]
    k_held = me.reindex(r.index, method="ffill").shift(1)
    return (r * k_held).dropna()


def rank_weights(sig: pd.Series) -> pd.Series:
    """משקלי דירוג בתוך קבוצה: דירוג פחות ממוצע, סכום |w| = 1."""
    s = sig.dropna()
    if len(s) < 2:
        return pd.Series(np.nan, index=sig.index)
    rk = s.rank()
    w = rk - rk.mean()
    tot = w.abs().sum()
    w = w / tot if tot > 0 else w * 0.0
    return w.reindex(sig.index)


# ── רכיבי החוזים ──────────────────────────────────────────────────────
def classes_of(labels: dict) -> dict:
    """{מכשיר: מחלקה} מהתווית 'שם — מחלקה'."""
    return {k: v.split(" — ")[-1].strip() for k, v in labels.items()}


def xs_component(px: pd.DataFrame, cls: dict, signal: pd.DataFrame,
                 cost_bps=COST_BPS) -> pd.Series:
    """תשואה יומית של אסטרטגיה חתך-רוחבית.

    בכל סוף חודש: משקלי דירוג לפי `signal` בתוך כל מחלקה, כפול היפוך
    התנודתיות של כל נכס (כך שנכס תנודתי לא שולט), כל מחלקה מנורמלת
    לתנודתיות יעד לפי עבר, ואז ממוצע שווה של המחלקות.
    """
    rets = px.pct_change()
    vol = rets.rolling(VOL_WINDOW).std() * np.sqrt(TDAYS)
    me = month_end_rows(px.index)
    sig_me = signal.reindex(me)
    inv_me = (1.0 / vol).reindex(me)
    out = {}
    for c in sorted(set(cls.values())):
        cols = [t for t in px.columns if cls.get(t) == c]
        w = sig_me[cols].apply(rank_weights, axis=1) * inv_me[cols]
        # סכום |w| = 1 אחרי הנרמול לתנודתיות, כדי שהמחזור יהיה במונחי הון
        w = w.div(w.abs().sum(axis=1).replace(0, np.nan), axis=0)
        wd = hold_monthly(w, px.index).fillna(0.0)
        gross = (wd * rets[cols].fillna(0.0)).sum(axis=1)
        turn = wd.diff().abs().sum(axis=1).fillna(0.0)
        net = gross - turn * cost_bps / 1e4
        first = wd.abs().sum(axis=1).gt(0).idxmax()
        out[c] = vol_scale(net.loc[first:])
    df = pd.DataFrame(out)
    return df.mean(axis=1, skipna=True).dropna()


def xsmom_signal(px: pd.DataFrame) -> pd.DataFrame:
    """12 חודשים עד לפני חודש."""
    return px.shift(XSMOM_SKIP) / px.shift(XSMOM_LOOKBACK) - 1.0


def value_signal(px: pd.DataFrame) -> pd.DataFrame:
    """log(ממוצע המחיר לפני 4.5–5.5 שנים / המחיר היום). חיובי = זול."""
    lp = np.log(px)
    past = lp.shift(VALUE_NEAR).rolling(VALUE_FAR - VALUE_NEAR).mean()
    return past - lp


def futures_components(px, labels) -> pd.DataFrame:
    cls = classes_of(labels)
    ts = portfolio(px, tsmom_positions(px))["net"]
    comps = {
        "tsmom": vol_scale(ts),
        "xsmom": xs_component(px, cls, xsmom_signal(px)),
        "value": xs_component(px, cls, value_signal(px)),
    }
    return pd.DataFrame(comps)


# ── רכיבים סחירים ─────────────────────────────────────────────────────
def load_spx(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    d = pd.read_csv(data_dir / "spx_open_close.csv", index_col="Date",
                    parse_dates=True).sort_index()
    return d


def overnight_returns(spx: pd.DataFrame, start=ON_START,
                      cost_bps=ON_COST_BPS) -> pd.Series:
    """לונג מהסגירה של אתמול לפתיחה של היום, נטו מעלות הלוך-חזור."""
    r = spx["Open"] / spx["Close"].shift(1) - 1.0
    return (r - cost_bps / 1e4).loc[start:].dropna()


def investable_components(start=ON_START) -> pd.DataFrame:
    px, _ = load_asset_classes()
    r = px[["USLCAP", "ITT"]].pct_change()
    bh = (0.6 * r["USLCAP"] + 0.4 * r["ITT"]).dropna()
    tr = portfolio(px, tsmom_positions(px, long_only=True, cash="STT"))["net"]
    on = overnight_returns(load_spx(), start="1990-01-01")
    df = pd.DataFrame({"6040": vol_scale(bh), "trend": vol_scale(tr)})
    # הלילה מנורמל מתחילת הנתונים כדי שהמכפיל יהיה מוכן ב-2010, אבל
    # נכנס לערימה רק מ-ON_START: לפני כן הפתיחות מזויפות.
    df["overnight"] = vol_scale(on).loc[start:]
    return df.loc[start:]


# ── הערימה ────────────────────────────────────────────────────────────
def stack(comps: pd.DataFrame, cols=None) -> pd.Series:
    cols = list(cols or comps.columns)
    c = comps[cols].dropna(how="any")
    return vol_scale(c.mean(axis=1), min_periods=SCALE_MIN)


def row(name: str, d: pd.Series, n_boot=5000) -> str:
    st = stats(d)
    b = stationary_bootstrap_sharpe(st["monthly"], n=n_boot)
    cagr = (1 + d).prod() ** (TDAYS / len(d)) - 1
    return (f"  {name:<30}{st['years']:5.1f}y  שארפ {st['sharpe']:5.2f}  "
            f"א5 {np.percentile(b, 5):5.2f}  CAGR {cagr * 100:+5.1f}%  "
            f"תנ' {st['ann_vol'] * 100:4.1f}%  DD {st['max_dd'] * 100:+6.1f}%  "
            f"גרועה {st['worst_year'] * 100:+6.1f}%")


def levered(d: pd.Series, k: float) -> pd.Series:
    return d * k


# ── מה Apex דורש ──────────────────────────────────────────────────────
def required_sharpe_table(daily_vol_usd=(150, 300, 500),
                          sharpes=(0.5, 1.0, 2.0, 3.0, 5.0),
                          dd=2_000.0, horizon=21, n=4000, seed=0):
    """אסטרטגיה סינתטית (נורמלית, בלי אוטוקורלציה) בשארפ נתון, דרך
    הערכה של 21 ימי מסחר: יעד 3,000$, דרודאון נגרר 2,000$ לפי סגירה."""
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2000-01-03", periods=TDAYS * 20)
    out = {}
    for sr in sharpes:
        z = rng.standard_normal(len(idx))
        z = (z - z.mean()) / z.std()
        base = pd.Series(z / np.sqrt(TDAYS) * 0.10 + sr * 0.10 / TDAYS,
                         index=idx)                   # 10% תנודתיות, שארפ sr
        for dv in daily_vol_usd:
            notional = dv / (0.10 / np.sqrt(TDAYS))
            r = prop_survival(base, notional, dd=dd, horizon_days=horizon,
                              n=n, mean_block=1, seed=seed)
            out[(sr, dv)] = r
    return out


# ── דוח ───────────────────────────────────────────────────────────────
def main() -> int:
    pd.options.mode.chained_assignment = None
    print("=" * 78)
    print("  ערימה א': חוזים עתידיים, 54 מכשירים, 1984–2016 (תשואה עודפת)")
    print("=" * 78)
    px, labels = load_futures()
    fc = futures_components(px, labels)
    common = fc.dropna(how="any")
    print(f"  תקופה משותפת: {common.index[0].date()} עד {common.index[-1].date()}"
          f" (value צריך 5.5 שנים של היסטוריה לפני האות הראשון)")
    print("\n  כל רכיב לבד, מנורמל ל-10% לפי עבר:")
    for c in fc:
        print(row(c, fc[c].dropna()))
    print("\n  קורלציות (ימים משותפים):")
    print("  " + common.corr().round(2).to_string().replace("\n", "\n  "))
    print("\n  ערימות, 10% תנודתיות יעד:")
    for cols in (["tsmom"], ["tsmom", "xsmom"], ["xsmom", "value"],
                 ["tsmom", "value"], ["tsmom", "xsmom", "value"]):
        print(row(" + ".join(cols), stack(fc, cols)))
    s3 = stack(fc)
    print("\n  הערימה המלאה במינוף גבוה יותר (אותה סדרה × k):")
    for tv in (0.15, 0.20):
        print(row(f"3 רכיבים @ {int(tv * 100)}%", levered(s3, tv / TARGET_VOL)))
    print("  לפי תקופה (10%):")
    for a, b in (("1990", "1999"), ("2000", "2009"), ("2010", "2016")):
        seg = s3.loc[a:b]
        st = stats(seg)
        print(f"    {a}–{b}: שארפ {st['sharpe']:.2f}  תשואה {st['ann_ret'] * 100:+.1f}%"
              f"  DD {st['max_dd'] * 100:+.1f}%")

    print("\n" + "=" * 78)
    print("  ערימה ב': מה שאפשר לקנות — 2010–2026")
    print("=" * 78)
    ic = investable_components()
    raw_on = overnight_returns(load_spx())
    st_on = stats(raw_on)
    print(f"  לילה גולמי, 1× נומינל, נטו {ON_COST_BPS} נ\"ב: תשואה "
          f"{st_on['ann_ret'] * 100:+.1f}%/שנה, תנ' {st_on['ann_vol'] * 100:.1f}%, "
          f"שארפ {st_on['sharpe']:.2f}, DD {st_on['max_dd'] * 100:+.1f}%")
    for cb in (0.0, 1.0, 2.0):
        s_ = stats(overnight_returns(load_spx(), cost_bps=cb))
        print(f"    רגישות לעלות {cb:.1f} נ\"ב: שארפ {s_['sharpe']:.2f}  "
              f"תשואה {s_['ann_ret'] * 100:+.1f}%")
    intraday = (load_spx()["Close"] / load_spx()["Open"] - 1).loc[ON_START:]
    si = stats(intraday)
    print(f"    ייחוס — אותו מדד מהפתיחה לסגירה: שארפ {si['sharpe']:.2f}, "
          f"תשואה {si['ann_ret'] * 100:+.1f}%")
    for a, b in (("2010", "2014"), ("2015", "2019"), ("2020", "2022"),
                 ("2023", "2026")):
        s_ = stats(raw_on.loc[a:b])
        print(f"    {a}–{b}: שארפ {s_['sharpe']:.2f}  תשואה {s_['ann_ret'] * 100:+.1f}%")
    print("\n  כל רכיב לבד, 10%:")
    for c in ic:
        print(row(c, ic[c].dropna()))
    cm = ic.dropna(how="any")
    print("\n  קורלציות:")
    print("  " + cm.corr().round(2).to_string().replace("\n", "\n  "))
    print("\n  ערימות, 10%:")
    for cols in (["6040"], ["6040", "trend"], ["6040", "overnight"],
                 ["trend", "overnight"], ["6040", "trend", "overnight"]):
        print(row(" + ".join(cols), stack(ic, cols)))
    si3 = stack(ic)
    for tv in (0.15, 0.20):
        print(row(f"3 רכיבים @ {int(tv * 100)}%", levered(si3, tv / TARGET_VOL)))

    print("\n" + "=" * 78)
    print("  הלילה בתוך Apex 50K EOD: יעד 3,000$, דרודאון 2,000$ לפי סגירה")
    print("=" * 78)
    spx = load_spx().loc[ON_START:]
    lvl = float(spx["Close"].iloc[-1])
    for n_mes in (1, 2, 4, 6, 10):
        notional = n_mes * 5 * lvl
        pnl = raw_on * notional
        big = (pnl < -1_000).mean()
        for h in (21, 252):
            r = prop_survival(raw_on, notional, dd=2_000, horizon_days=h, n=3000)
            print(f"  {n_mes:>2} MES (${notional:>9,.0f})  {h:>3} ימים: עוברים "
                  f"{r['pass_rate'] * 100:3.0f}%  נשרפים {r['blowup_rate'] * 100:3.0f}%  "
                  f"פוקעים {r['neither'] * 100:3.0f}%"
                  + (f"   לילות עם הפסד > 1,000$: {big * 100:.1f}%" if h == 21 else ""))
    print("  המודל לפי סגירה נכון לחשבון EOD. במגבלה היומית של 1,000$ לא ידוע")
    print("  אם נגיעה בה סוגרת את היום או את החשבון — השורה שלה מודפסת.")

    print("\n" + "=" * 78)
    print("  איזה שארפ ההערכה דורשת — אסטרטגיה סינתטית, 21 ימי מסחר")
    print("=" * 78)
    tbl = required_sharpe_table()
    dvs = sorted({k[1] for k in tbl})
    print("  שארפ שנתי " + "".join(f"   $vol/יום {dv:>3}: עובר/נשרף" for dv in dvs))
    for sr in sorted({k[0] for k in tbl}):
        cells = "".join(f"{tbl[(sr, dv)]['pass_rate'] * 100:>19.0f}%/"
                        f"{tbl[(sr, dv)]['blowup_rate'] * 100:<3.0f}%" for dv in dvs)
        print(f"  {sr:>9.1f} {cells}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
