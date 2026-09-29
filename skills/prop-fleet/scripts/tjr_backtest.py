#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tjr_backtest.py — המודל של TJR, כפי שהוא מתואר בפומבי, על 8 שנים של S&P בדקה.

למה זה קיים
-----------
איתמר ביקש ללמוד את הבוטקמפ של TJR, להרכיב את האסטרטגיה ולבדוק אותה.
יוטיוב חסום מהסביבה הזאת, ולכן הכללים נלקחו מסיכומים כתובים של
השיטה (ראה references/tjr.md) — ולא מהבוט של איתמר, שאת הקוד שלו אין
כאן. זה מבחן עצמאי: נתונים אחרים (2010–2018), מימוש אחר, אותו רעיון.

המודל, בכללים שנקבעו לפני שהורצה שורה אחת
-----------------------------------------
1. טווח אסיה: הגבוה והנמוך של 20:00–00:00 שעון ניו יורק (ערב קודם).
2. חלון מסחר: 03:00–11:00 (לונדון + בוקר ניו יורק).
3. סוויפ: המחיר עובר את גבוה אסיה (או נמוך אסיה) בתוך החלון.
4. שבירת מבנה (MSS): אחרי סוויפ של הגבוה, סגירה של נר 5 דקות מתחת לנמוך
   הסווינג האחרון שאושר (סווינג = פיבוט עם K נרות מכל צד, מאושר רק
   K נרות אחרי שנוצר — בלי הצצה קדימה). הפוך ללונג.
5. כניסה: ה-FVG האחרון בכיוון השבירה, בין נר הקיצון של הסוויפ לנר השבירה.
   פקודת לימיט בקצה הקרוב של הפער, פעילה מהדקה שאחרי סגירת נר השבירה.
6. סטופ: טיק אחד מעבר לקיצון הסוויפ.
7. יעד: פי 2 מהסיכון (ה-1:2 המינימלי של השיטה).
8. עסקה אחת ביום. פקודה שלא מולאה עד 11:00 מבוטלת; פקודה מבוטלת גם אם
   המחיר נוגע ביעד לפני המילוי. עסקה פתוחה נסגרת ב-15:55.
9. עלות: 0.6 נקודות הלוך-חזור (עמלה + חצי טיק החלקה לכל צד ב-ES).
10. נר של דקה שנוגע גם בסטופ וגם ביעד — סטופ. נר המילוי שנוגע בסטופ —
    סטופ. תמיד לחובת האסטרטגיה.

וריאנטים (מודפסים כולם, לא לבחירה): כניסה באמצע הפער, יעד בצד השני של
אסיה, K=1/3, מסנן מגמה יומית, יעד 3R.

הנתונים
-------
SPXUSD דקה, 11/2010–12/2018, מ-HistData דרך github.com/FutureSharks/
financial-data. זה ציטוט CFD על המדד, 24 שעות, לא ES — מבנה המחיר זהה,
הבסיס שונה. הקבצים לא בריפו (60MB); הסקריפט מוריד אותם ל-SCRATCH.
"""
from __future__ import annotations

import os
import sys

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

SCRATCH = Path(os.environ.get(
    "CLAUDE_SCRATCH",
    "/tmp/claude-0/-home-user-claude-skills/"
    "83e06ccf-6299-5e6f-ac94-4ff79d8a5049/scratchpad")) / "tjr"
RAW = ("https://raw.githubusercontent.com/FutureSharks/financial-data/master/"
       "pyfinancialdata/data/stocks/histdata/SPXUSD/DAT_ASCII_SPXUSD_M1_{y}.csv")
YEARS = range(2010, 2019)

TICK = 0.25
COST_PTS = 0.6
MIN_RISK = 1.0            # נקודות. סטופ של פחות מ-4 טיקים אינו בר-ביצוע
ASIA = ("20:00", "23:59")
WINDOW = ("03:00", "11:00")
FLAT = "15:55"


@dataclass(frozen=True)
class Spec:
    name: str
    k: int = 2                 # נרות מכל צד לפיבוט
    entry: str = "edge"        # edge | mid
    target: str = "2R"         # 2R | 3R | asia
    bias: bool = False


VARIANTS = (
    Spec("בסיס: K=2, קצה FVG, 2R"),
    Spec("כניסה באמצע ה-FVG", entry="mid"),
    Spec("יעד: הצד השני של אסיה (≥2R)", target="asia"),
    Spec("K=1", k=1),
    Spec("K=3", k=3),
    Spec("מסנן מגמה יומית (SMA20)", bias=True),
    Spec("יעד 3R", target="3R"),
)


# ── נתונים ────────────────────────────────────────────────────────────
def load_minutes() -> pd.DataFrame:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    frames = []
    for y in YEARS:
        f = SCRATCH / f"SPX_{y}.csv"
        if not f.exists():
            import urllib.request
            urllib.request.urlretrieve(RAW.format(y=y), f)
        frames.append(pd.read_csv(f, sep=";", header=None,
                                  names=["dt", "o", "h", "l", "c", "v"]))
    d = pd.concat(frames)
    d["dt"] = pd.to_datetime(d["dt"], format="%Y%m%d %H%M%S")
    d = d.set_index("dt").sort_index()
    return d[~d.index.duplicated()][["o", "h", "l", "c"]]


def to_5min(m: pd.DataFrame) -> pd.DataFrame:
    return m.resample("5min", label="left", closed="left").agg(
        {"o": "first", "h": "max", "l": "min", "c": "last"}).dropna()


# ── מבנה ──────────────────────────────────────────────────────────────
def confirmed_pivots(h: np.ndarray, l: np.ndarray, k: int):
    """מערכים: הפיבוט האחרון שאושר עד כל נר (כולל). פיבוט בנר p מאושר
    בנר p+k. מחזיר (last_swing_high, last_swing_low), NaN אם אין."""
    n = len(h)
    sh = np.full(n, np.nan)
    sl = np.full(n, np.nan)
    cur_h = cur_l = np.nan
    for t in range(n):
        p = t - k
        if p - k >= 0:
            win_h = h[p - k:p + k + 1]
            win_l = l[p - k:p + k + 1]
            if h[p] == win_h.max() and (win_h == h[p]).sum() == 1:
                cur_h = h[p]
            if l[p] == win_l.min() and (win_l == l[p]).sum() == 1:
                cur_l = l[p]
        sh[t], sl[t] = cur_h, cur_l
    return sh, sl


def find_setup(b5: pd.DataFrame, ah: float, al: float, spec: Spec,
               allow_long=True, allow_short=True):
    """מחפש את הסטאפ הראשון בחלון. b5 = נרות 5 דק' מ-18:00 אתמול עד 11:00.
    מחזיר dict או None. משתמש רק במידע עד סגירת נר השבירה."""
    h, l, c = b5["h"].values, b5["l"].values, b5["c"].values
    idx = b5.index
    sh, sl = confirmed_pivots(h, l, spec.k)
    in_win = (idx.strftime("%H:%M") >= WINDOW[0]) & (idx.strftime("%H:%M") < WINDOW[1])
    swept_h = swept_l = False
    ext_h, ext_h_i, ext_l, ext_l_i = -np.inf, -1, np.inf, -1
    for t in np.where(in_win)[0]:
        if h[t] > ah:
            swept_h = True
        if l[t] < al:
            swept_l = True
        if swept_h and h[t] > ext_h:
            ext_h, ext_h_i = h[t], t
        if swept_l and l[t] < ext_l:
            ext_l, ext_l_i = l[t], t
        # שורט: אחרי סוויפ של הגבוה, סגירה מתחת לסווינג-לואו האחרון
        # שנוצר *לפני* השבירה ואחרי... (הפיבוט האחרון שאושר עד t-1)
        if allow_short and swept_h and t >= 1 and not np.isnan(sl[t - 1]) \
                and c[t] < sl[t - 1] and ext_h_i < t:
            fvg = None
            for i in range(t, max(ext_h_i + 2, 2) - 1, -1):
                if l[i - 2] > h[i]:                     # פער דובי
                    fvg = (h[i], l[i - 2])              # (תחתון, עליון)
                    break
            if fvg:
                entry = fvg[0] if spec.entry == "edge" else (fvg[0] + fvg[1]) / 2
                stop = ext_h + TICK
                return dict(side=-1, entry=entry, stop=stop, t=idx[t],
                            asia_other=al)
        if allow_long and swept_l and t >= 1 and not np.isnan(sh[t - 1]) \
                and c[t] > sh[t - 1] and ext_l_i < t:
            fvg = None
            for i in range(t, max(ext_l_i + 2, 2) - 1, -1):
                if h[i - 2] < l[i]:                     # פער שורי
                    fvg = (h[i - 2], l[i])              # (תחתון, עליון)
                    break
            if fvg:
                entry = fvg[1] if spec.entry == "edge" else (fvg[0] + fvg[1]) / 2
                stop = ext_l - TICK
                return dict(side=+1, entry=entry, stop=stop, t=idx[t],
                            asia_other=ah)
    return None


def simulate(m1: pd.DataFrame, s: dict, spec: Spec, day) -> dict | None:
    side, entry, stop = s["side"], s["entry"], s["stop"]
    risk = (stop - entry) * -side
    if not risk >= MIN_RISK:
        return None
    if spec.target == "asia":
        tgt = s["asia_other"]
        if (tgt - entry) * side < 2 * risk:
            return None
    else:
        mult = 3.0 if spec.target == "3R" else 2.0
        tgt = entry + side * mult * risk
    start = s["t"] + pd.Timedelta(minutes=5)          # אחרי סגירת נר השבירה
    arm_end = pd.Timestamp(f"{day} {WINDOW[1]}")
    flat = pd.Timestamp(f"{day} {FLAT}")
    bars = m1.loc[start:flat]
    filled = False
    for ts, b in bars.iterrows():
        if not filled:
            if ts >= arm_end:
                return None
            # היעד נגעה לפני המילוי — הסטאפ פג
            if (side < 0 and b.l <= tgt) or (side > 0 and b.h >= tgt):
                return None
            if (side < 0 and b.h >= entry) or (side > 0 and b.l <= entry):
                filled = True
                if (side < 0 and b.h >= stop) or (side > 0 and b.l <= stop):
                    return _res(day, side, entry, stop, risk, stop, "stop")
            continue
        hit_s = (side < 0 and b.h >= stop) or (side > 0 and b.l <= stop)
        hit_t = (side < 0 and b.l <= tgt) or (side > 0 and b.h >= tgt)
        if hit_s:
            return _res(day, side, entry, stop, risk, stop, "stop")
        if hit_t:
            return _res(day, side, entry, stop, risk, tgt, "target")
    if not filled:
        return None
    return _res(day, side, entry, stop, risk, float(bars["c"].iloc[-1]), "time")


def _res(day, side, entry, stop, risk, exit_px, why):
    pts = (exit_px - entry) * side - COST_PTS
    return dict(day=pd.Timestamp(day), side=side, entry=entry, stop=stop,
                risk=risk, exit=exit_px, why=why, pts=pts, R=pts / risk)


def run(m1: pd.DataFrame, spec: Spec) -> pd.DataFrame:
    days = sorted(set(m1.index.normalize()))
    daily = m1["c"].resample("1D").last().dropna()
    sma = daily.rolling(20).mean().shift(1)          # עד אתמול
    prev = daily.shift(1)
    out = []
    for d in days:
        if d.weekday() >= 5:
            continue
        day = d.date()
        a0 = pd.Timestamp(day) - pd.Timedelta(days=1) + pd.Timedelta(hours=20)
        asia = m1.loc[a0:a0 + pd.Timedelta(hours=3, minutes=59)]
        if len(asia) < 120:
            continue
        ah, al = asia["h"].max(), asia["l"].min()
        ctx = m1.loc[pd.Timestamp(day) - pd.Timedelta(hours=6):
                     pd.Timestamp(f"{day} {WINDOW[1]}")]
        if len(ctx) < 300:
            continue
        b5 = to_5min(ctx)
        al_long = al_short = True
        if spec.bias:
            if pd.isna(sma.get(d)) or pd.isna(prev.get(d)):
                continue
            up = prev[d] > sma[d]
            al_long, al_short = up, not up
        s = find_setup(b5, ah, al, spec, al_long, al_short)
        if s is None:
            continue
        r = simulate(m1, s, spec, day)
        if r:
            out.append(r)
    return pd.DataFrame(out)


# ── סטטיסטיקה ─────────────────────────────────────────────────────────
def boot_mean(x: np.ndarray, n=5000, seed=0):
    rng = np.random.default_rng(seed)
    means = rng.choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    return np.percentile(means, [5, 50, 95])


def summarize(t: pd.DataFrame, name: str) -> dict:
    x = t["R"].values
    lo, med, hi = boot_mean(x)
    years = (t["day"].max() - t["day"].min()).days / 365.25
    per_year = len(t) / years
    sr = x.mean() / x.std(ddof=1) * np.sqrt(per_year)
    return dict(name=name, n=len(t), per_year=per_year,
                win=(t["why"] == "target").mean(), mean=x.mean(),
                lo=lo, hi=hi, sharpe=sr, med_risk=t["risk"].median(),
                by_year=t.groupby(t["day"].dt.year)["R"].agg(["count", "mean"]))


def main() -> int:
    print("  טוען 8 שנים של S&P בדקה...", flush=True)
    m1 = load_minutes()
    print(f"  {len(m1):,} נרות, {m1.index[0].date()} עד {m1.index[-1].date()}\n")
    rows = []
    for spec in VARIANTS:
        t = run(m1, spec)
        s = summarize(t, spec.name)
        rows.append((spec, t, s))
        print(f"  {s['name']:<32} n={s['n']:4d} ({s['per_year']:.0f}/שנה)  "
              f"זכייה {s['win'] * 100:4.1f}%  ממוצע {s['mean']:+.3f}R  "
              f"[{s['lo']:+.3f}, {s['hi']:+.3f}]  שארפ {s['sharpe']:+.2f}  "
              f"סטופ חציוני {s['med_risk']:.1f} נק'", flush=True)
    spec, t, s = rows[0]
    print(f"\n  הבסיס לפי שנה:")
    for y, r in s["by_year"].iterrows():
        print(f"    {y}: {int(r['count']):3d} עסקאות  {r['mean']:+.3f}R")
    print(f"  יציאות: " + ", ".join(f"{k} {v * 100:.0f}%" for k, v in
                                   t["why"].value_counts(normalize=True).items()))
    print(f"  לונג {int((t.side > 0).sum())} ({t.loc[t.side > 0, 'R'].mean():+.3f}R)  "
          f"שורט {int((t.side < 0).sum())} ({t.loc[t.side < 0, 'R'].mean():+.3f}R)")
    t.to_csv(SCRATCH / "tjr_base_trades.csv", index=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
