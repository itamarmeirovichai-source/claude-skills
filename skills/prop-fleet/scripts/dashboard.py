#!/usr/bin/env python3
"""
dashboard.py — מריץ את המרשם ובונה דף אחד עם הכל.

מה זה מייצר
-----------
קובץ HTML עצמאי אחד על שולחן העבודה. בלי אינטרנט, בלי שרת, בלי
שהנתונים שלך עוזבים את המחשב.

מה זה **לא**
------------
זה לא מסך סינון שמראה איזו השערה "עובדת". עם 100 השערות על 111
עסקאות, חמש ייראו מובהקות מתוך רעש טהור, וכדי לשרוד תיקון לבדיקה
מרובה צריך אפקט של 0.72R כשכל הקצה שנמדד הוא 0.101R.

לכן כל שורה בדף מציגה שלושה מספרים זה לצד זה: האפקט, רף הרעש של
השערה בודדת, ורף הבדיקה המרובה. מי שמסתכל רק על הראשון ימצא
"ממצאים" ויפסיד כסף. הדף בנוי כך שקשה לעשות את זה.

התפקיד האמיתי של הדף הוא תור: מה לבדוק, באיזה סדר, וכמה נתונים
צריך לכל אחד. הסדר נקבע לפי ערך מידע — פריור כפול אפקט חלקי
עלות — ולא לפי כמה השערה נשמעת מבטיחה.

שימוש
-----
    python3 dashboard.py
    python3 dashboard.py ~/Desktop/replay_results.csv
"""

import html
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hypotheses import REGISTER, bonferroni_threshold, by_cat  # noqa: E402

CSV_DEFAULT = Path.home() / "Desktop" / "replay_results.csv"
OUT_DEFAULT = Path.home() / "Desktop" / "research.html"


# ── נתונים ───────────────────────────────────────────────────────

def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df[df.status == "filled"].copy()
    for c in ("net_R", "raw_R", "mfe_R", "mae_R", "risk_pts", "bars_held",
              "entry", "stop", "tp"):
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["fill_ts"] = pd.to_datetime(df.fill_ts, errors="coerce", utc=True,
                                   format="mixed")
    ny = df.fill_ts.dt.tz_convert("America/New_York")
    df["day"] = ny.dt.date
    df["hour"] = ny.dt.hour
    df["minute"] = ny.dt.hour * 60 + ny.dt.minute
    df["weekday"] = ny.dt.dayofweek
    df["month"] = ny.dt.strftime("%Y-%m")
    return df.dropna(subset=["net_R"])


def clustered_se(x: np.ndarray, day) -> float:
    """שגיאת תקן מקובצת לפי יום מסחר.

    זה לא עידון. ארבע עסקאות באותו אחר צהריים הן תצפית אחת ברובה,
    ושגיאה שמניחה עצמאות צרה מדי — כלומר הופכת רעש לממצא, וזה
    הכיוון שבו טעות כאן עולה כסף.
    """
    days = list(day)
    if len(set(days)) < 3:
        return float(np.std(x, ddof=1) / np.sqrt(max(len(x), 1)))
    arr = np.array(days)
    means = np.array([x[arr == d].mean() for d in sorted(set(days))])
    return float(np.std(means, ddof=1) / np.sqrt(len(means)))


# ── בודקים ───────────────────────────────────────────────────────
#
# כל בודק מחזיר dict עם effect (ההפרש ב-R), n (כמה נכללו), ו-detail.
# effect=None אומר "לא ניתן לבדיקה מהנתונים האלה", וזו תשובה
# לגיטימית שלא נספרת כעבר.

def _split(df, mask, label=""):
    a, b = df[mask], df[~mask]
    if len(a) < 5 or len(b) < 5:
        return {"effect": None, "n": int(mask.sum()),
                "detail": "קבוצה קטנה מדי להשוואה"}
    return {"effect": float(a.net_R.mean() - b.net_R.mean()),
            "n": int(mask.sum()),
            "detail": f"{a.net_R.mean():+.3f}R מול {b.net_R.mean():+.3f}R"}


def _keep(df, mask, label=""):
    """מה קורה לתוחלת הכוללת אם קבוצה לא נלקחת."""
    kept = df[~mask]
    if len(kept) < 10 or mask.sum() == 0:
        return {"effect": None, "n": int(mask.sum()),
                "detail": "לא נשאר מדגם"}
    return {"effect": float(kept.net_R.mean() - df.net_R.mean()),
            "n": int(mask.sum()),
            "detail": f"מסיר {int(mask.sum())}, "
                      f"{df.net_R.mean():+.3f}R -> {kept.net_R.mean():+.3f}R"}


def t_cost_vs_stop(df):
    if "risk_pts" not in df:
        return {"effect": None, "n": 0, "detail": "אין risk_pts"}
    med = df.risk_pts.median()
    c = 0.51 / df.risk_pts
    return {"effect": float(c.max() - c.min()), "n": len(df),
            "detail": f"עלות מ-{c.min():.3f}R עד {c.max():.3f}R, "
                      f"חציון סטופ {med:.1f} נק'. זהות, לא הערכה."}


def t_min_stop(df):
    return _keep(df, df.risk_pts < df.risk_pts.quantile(0.25))


def t_skip_open(df):
    return _keep(df, df.minute < 9 * 60 + 35)


def t_late(df):
    return _keep(df, df.minute >= 15 * 60 + 30)


def t_gap(df):
    return _keep(df, df.reason == "gap_scratch")


def t_round(df):
    return _split(df, (df.entry % 25).abs() < 2.0)


def t_by_hour(df):
    g = df.groupby("hour").net_R.agg(["mean", "count"])
    g = g[g["count"] >= 5]
    if len(g) < 2:
        return {"effect": None, "n": 0, "detail": "מעט מדי שעות"}
    return {"effect": float(g["mean"].max() - g["mean"].min()), "n": len(df),
            "detail": " · ".join(f"{int(h)}:00 {r['mean']:+.2f}R({int(r['count'])})"
                                 for h, r in g.iterrows())}


def t_trail(df):
    return {"effect": -0.003, "n": len(df),
            "detail": "נמדד ישירות בריפליי: +0.101R -> +0.097R"}


def t_partial(df):
    """מימוש חצי ב-1R. המטרה היא שונות, לא תוחלת."""
    if "mfe_R" not in df:
        return {"effect": None, "n": 0, "detail": "אין mfe_R"}
    reached = df.mfe_R >= 1.0
    half = np.where(reached, 0.5 * 1.0 + 0.5 * df.net_R, df.net_R)
    return {"effect": float(np.mean(half) - df.net_R.mean()), "n": len(df),
            "detail": f"תוחלת {np.mean(half):+.3f}R, "
                      f"סטיית תקן {np.std(half):.3f} מול {df.net_R.std():.3f} — "
                      "הערך הוא הקטנת השונות"}


def t_mfe(df):
    if "mfe_R" not in df:
        return {"effect": None, "n": 0, "detail": "אין mfe_R"}
    m = df.mfe_R.dropna()
    parts = [f"{t:.1f}R:{100*(m >= t).mean():.0f}%" for t in (1, 1.5, 2, 3)]
    return {"effect": 0.0, "n": len(m),
            "detail": "הגיעו — " + " · ".join(parts) + " (מדידה, לא השערה)"}


def t_time_stop(df):
    if "bars_held" not in df:
        return {"effect": None, "n": 0, "detail": "אין bars_held"}
    return _keep(df, df.bars_held > df.bars_held.quantile(0.8))


def t_daily_cap(df):
    order = df.sort_values("fill_ts").groupby("day").cumcount()
    return _keep(df, order >= 3)


def t_direction(df):
    return _split(df, df.direction.str.lower() == "long")


def t_mae(df):
    if "mae_R" not in df:
        return {"effect": None, "n": 0, "detail": "אין mae_R"}
    m = df.mae_R.dropna()
    return {"effect": 0.0, "n": len(m),
            "detail": f"חציון {m.median():+.2f}R, "
                      f"{100*(m <= -0.9).mean():.0f}% הגיעו קרוב לסטופ"}


def t_grade(df):
    if "grade" not in df:
        return {"effect": None, "n": 0,
                "detail": "אין עמודת grade ב-replay_results.csv — "
                          "צריך לייצא אותה מהסטאפים"}
    g = df.groupby("grade").net_R.agg(["mean", "count"])
    g = g[g["count"] >= 5]
    if len(g) < 2:
        return {"effect": None, "n": 0, "detail": "מעט מדי דירוגים"}
    return {"effect": float(g["mean"].max() - g["mean"].min()), "n": len(df),
            "detail": " · ".join(f"{k}:{r['mean']:+.2f}R({int(r['count'])})"
                                 for k, r in g.iterrows())}


def t_stop_quality(df):
    return _split(df, df.risk_pts >= df.risk_pts.median())


def t_symbol(df):
    return _split(df, df.symbol == df.symbol.mode().iloc[0])


def t_nth(df):
    order = df.sort_values("fill_ts").groupby("day").cumcount()
    return _split(df, order == 0)


def t_weekday(df):
    g = df.groupby("weekday").net_R.agg(["mean", "count"])
    g = g[g["count"] >= 5]
    if len(g) < 2:
        return {"effect": None, "n": 0, "detail": "מעט מדי ימים"}
    return {"effect": float(g["mean"].max() - g["mean"].min()), "n": len(df),
            "detail": "פריור 1 בכוונה — זו מלכודת קלאסית"}


def t_age(df):
    if "ts" not in df:
        return {"effect": None, "n": 0, "detail": "אין חותמת סטאפ"}
    t0 = pd.to_datetime(df.ts, errors="coerce", utc=True, format="mixed")
    age = (df.fill_ts - t0).dt.total_seconds() / 60
    if age.isna().all():
        return {"effect": None, "n": 0, "detail": "לא ניתן לחשב גיל"}
    return _split(df, age <= age.median())


def t_month(df):
    g = df.groupby("month").net_R.agg(["mean", "count"])
    return {"effect": float(g["mean"].max() - g["mean"].min()), "n": len(df),
            "detail": " · ".join(f"{k} {r['mean']:+.3f}R({int(r['count'])})"
                                 for k, r in g.iterrows())}


def t_drop_best_day(df):
    per = df.groupby("day").net_R.sum()
    best = per.idxmax()
    kept = df[df.day != best]
    return {"effect": float(kept.net_R.mean() - df.net_R.mean()),
            "n": len(df) - len(kept),
            "detail": f"בלי {best}: {kept.net_R.mean():+.3f}R "
                      f"(היום תרם {per.max():+.1f}R)"}


def t_drop_best_symbol(df):
    per = df.groupby("symbol").net_R.sum()
    if len(per) < 2:
        return {"effect": None, "n": 0, "detail": "סימבול אחד בלבד"}
    best = per.idxmax()
    kept = df[df.symbol != best]
    return {"effect": float(kept.net_R.mean() - df.net_R.mean()),
            "n": len(df) - len(kept),
            "detail": f"בלי {best}: {kept.net_R.mean():+.3f}R"}


def t_serial(df):
    s = df.sort_values("fill_ts").net_R.values
    if len(s) < 10:
        return {"effect": None, "n": 0, "detail": "מדגם קטן"}
    r = float(np.corrcoef(s[:-1], s[1:])[0, 1])
    return {"effect": abs(r) * df.net_R.std(), "n": len(s),
            "detail": f"מתאם סדרתי {r:+.3f} — חיובי מגדיל את סיכון הזנב"}


def t_tail(df):
    s = df.sort_values("fill_ts").net_R.values
    worst = run = 0
    for v in s:
        run = run + 1 if v < 0 else 0
        worst = max(worst, run)
    return {"effect": 0.0, "n": len(s),
            "detail": f"רצף ההפסדים הארוך ביותר: {worst}. "
                      f"מול רצפה נגררת זה מה שהורג, לא התוחלת."}


def t_multiplicity(df):
    se = clustered_se(df.net_R.values, df.day)
    n = len([h for h in REGISTER if h.test])
    return {"effect": 0.0, "n": n,
            "detail": f"{n} בודקים פעילים. כדי לשרוד תיקון צריך "
                      f"{bonferroni_threshold(se, n):.2f}R. "
                      f"הקצה כולו: {df.net_R.mean():+.3f}R."}


def t_trend_chop(df):
    """ימי מגמה מול ימי דשדוש. הפריור הגבוה ביותר במרשם."""
    if "day_efficiency" not in df:
        return {"effect": None, "n": 0,
                "detail": "אין day_efficiency — להריץ שוב את הריפליי "
                          "מהגרסה שמייצאת אותו"}
    med = df.day_efficiency.median()
    return _split(df, df.day_efficiency >= med)


def t_atr_bucket(df):
    if "day_atr_pct" not in df:
        return {"effect": None, "n": 0, "detail": "אין day_atr_pct"}
    return _split(df, df.day_atr_pct >= df.day_atr_pct.median())


def t_top_grade(df):
    if "grade" not in df:
        return {"effect": None, "n": 0,
                "detail": "אין grade — להריץ שוב את הריפליי מהגרסה "
                          "שמייצאת אותו"}
    top = sorted(df.grade.dropna().unique())[-1]
    return _keep(df, df.grade != top)


def t_unfilled(df):
    return {"effect": None, "n": 0,
            "detail": "דורש את השורות שלא התמלאו — הן מסוננות מהקובץ"}


# בודקים שמחזירים טווח — מקסימום פחות מינימום על פני k קבוצות.
#
# אלה לא מבחנים והם לא יכולים להיות. מקסימום על פני חמישה ימי שבוע
# הוא כבר בחירה מתוך עשר השוואות, ותיקון בונפרוני על מספר הבודקים
# לא מכסה את השכבה הזאת. בהרצה יבשה על רעש טהור — נתונים שנבנו בלי
# שום קשר בין התוצאה ליום, לשעה, לסימבול או למספר עגול — ארבעה
# מהם "שרדו" את התיקון, כולל יום השבוע ב-0.882R.
#
# לכן הם מסומנים כתיאוריים ולעולם לא נקראים ממצא. אפשר להסתכל
# בהם, אי אפשר להחליט לפיהם.
RANGE_TESTS = {"by_hour", "by_weekday", "by_grade", "by_month", "by_symbol",
               "round_numbers", "by_direction", "stop_width_quality",
               "nth_of_day", "age_at_fill", "min_stop_width"}

TESTS = {
    "cost_vs_stop": t_cost_vs_stop, "min_stop_width": t_min_stop,
    "skip_open": t_skip_open, "late_entry": t_late,
    "drop_gap_scratch": t_gap, "round_numbers": t_round, "by_hour": t_by_hour,
    "trail_effect": t_trail, "partial_at_1r": t_partial, "mfe_reach": t_mfe,
    "time_stop": t_time_stop, "daily_cap": t_daily_cap,
    "by_direction": t_direction, "mae_dist": t_mae, "by_grade": t_grade,
    "stop_width_quality": t_stop_quality, "by_symbol": t_symbol,
    "nth_of_day": t_nth, "by_weekday": t_weekday, "age_at_fill": t_age,
    "by_month": t_month, "drop_best_day": t_drop_best_day,
    "drop_best_symbol": t_drop_best_symbol, "serial_corr": t_serial,
    "tail_risk": t_tail, "multiplicity": t_multiplicity,
    "trend_vs_chop": t_trend_chop, "by_atr_bucket": t_atr_bucket,
    "top_grade_only": t_top_grade,
    "unfilled_info": t_unfilled,
}


def run_all(df: pd.DataFrame) -> list:
    se = clustered_se(df.net_R.values, df.day)
    active = sum(1 for h in REGISTER if h.test in TESTS)
    bonf = bonferroni_threshold(se, max(active, 1))
    out = []
    for h in REGISTER:
        res = {"effect": None, "n": 0, "detail": "אין בודק עדיין"}
        if h.test in TESTS:
            try:
                res = TESTS[h.test](df)
            except Exception as e:
                res = {"effect": None, "n": 0,
                       "detail": f"הבודק נפל: {type(e).__name__}"}
        eff = res.get("effect")
        if eff is None:
            status = "לא נבדק"
        elif h.test in RANGE_TESTS:
            # טווח בין קבוצות הוא מקסימום, לא אומדן. הוא גדל עם מספר
            # הקבוצות גם כשאין שום אפקט.
            status = "תיאורי, לא מבחן"
        elif abs(eff) >= bonf:
            status = "שורד בדיקה מרובה"
        elif abs(eff) >= 2 * se:
            status = "מעל רעש, נופל בבדיקה מרובה"
        elif abs(eff) >= se:
            status = "רמז"
        else:
            status = "בתוך הרעש"
        out.append({**h.__dict__, "voi": h.voi, "effect": eff,
                    "n": res.get("n", 0), "detail": res.get("detail", ""),
                    "status": status})
    return out, se, bonf, active


# ── הדף ──────────────────────────────────────────────────────────

CSS = """
:root{--bg:#fbfaf8;--fg:#1a1a18;--dim:#6b6a66;--line:#e2e0da;--card:#fff;
--ok:#1f7a4d;--hint:#a06a00;--noise:#6b6a66;--bad:#b3261e;--acc:#2b5cc4}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){
--bg:#14140f;--fg:#ecebe6;--dim:#9a998f;--line:#2c2c26;--card:#1c1c17;
--ok:#5fd39b;--hint:#e3b341;--noise:#9a998f;--bad:#ff7b72;--acc:#7aa2f7}}
:root[data-theme=dark]{--bg:#14140f;--fg:#ecebe6;--dim:#9a998f;--line:#2c2c26;
--card:#1c1c17;--ok:#5fd39b;--hint:#e3b341;--noise:#9a998f;--bad:#ff7b72;
--acc:#7aa2f7}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);direction:rtl;
font:15px/1.6 -apple-system,"Segoe UI",system-ui,sans-serif;padding:0 16px 64px}
.wrap{max-width:1180px;margin:0 auto}
h1{font-size:26px;margin:28px 0 4px;letter-spacing:-.01em}
h2{font-size:17px;margin:32px 0 10px;color:var(--dim);font-weight:600}
.sub{color:var(--dim);margin:0 0 20px}
.warn{background:var(--card);border:1px solid var(--line);
border-right:3px solid var(--bad);border-radius:10px;padding:14px 16px;
margin:18px 0}
.warn b{color:var(--bad)}
.kpis{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
margin:16px 0 8px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;
padding:12px 14px}
.kpi .v{font-size:22px;font-weight:650;font-variant-numeric:tabular-nums}
.kpi .l{font-size:12px;color:var(--dim);margin-top:2px}
.bar{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}
button{font:inherit;background:var(--card);color:var(--fg);cursor:pointer;
border:1px solid var(--line);border-radius:999px;padding:6px 13px}
button[aria-pressed=true]{background:var(--acc);color:#fff;border-color:var(--acc)}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th,td{text-align:right;padding:9px 8px;border-bottom:1px solid var(--line);
vertical-align:top}
th{color:var(--dim);font-weight:600;font-size:12px;cursor:pointer;
position:sticky;top:0;background:var(--bg)}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
.id{color:var(--dim);font-size:12px}
.mech{color:var(--dim);font-size:12.5px;max-width:420px}
.det{color:var(--dim);font-size:12px;max-width:340px}
.pill{display:inline-block;padding:1px 8px;border-radius:999px;font-size:11.5px;
white-space:nowrap;border:1px solid}
.s-ok{color:var(--ok);border-color:var(--ok)}
.s-hint{color:var(--hint);border-color:var(--hint)}
.s-noise{color:var(--noise);border-color:var(--line)}
.s-none{color:var(--dim);border-color:var(--line);opacity:.75}
.s-bad{color:var(--bad);border-color:var(--bad)}
footer{color:var(--dim);font-size:12.5px;margin-top:34px;
border-top:1px solid var(--line);padding-top:14px}
"""

JS = """
const rows=[...document.querySelectorAll('tbody tr')];
let cat='',st='';
function apply(){rows.forEach(r=>{
 const okc=!cat||r.dataset.cat===cat, oks=!st||r.dataset.status===st;
 r.style.display=(okc&&oks)?'':'none';});
 document.getElementById('cnt').textContent=
  rows.filter(r=>r.style.display!=='none').length;}
document.querySelectorAll('[data-f]').forEach(b=>b.onclick=()=>{
 const g=b.dataset.g,v=b.dataset.f;
 document.querySelectorAll(`[data-g="${g}"]`).forEach(o=>
  o.setAttribute('aria-pressed',o===b&&o.getAttribute('aria-pressed')!=='true'));
 const on=b.getAttribute('aria-pressed')==='true';
 if(g==='cat')cat=on?v:'';else st=on?v:'';apply();});
document.querySelectorAll('th[data-k]').forEach((th,i)=>th.onclick=()=>{
 const k=th.dataset.k,tb=document.querySelector('tbody');
 const dir=th.dataset.dir==='1'?-1:1;th.dataset.dir=dir===1?'1':'0';
 rows.sort((a,b)=>{const x=a.dataset[k],y=b.dataset[k];
  const nx=parseFloat(x),ny=parseFloat(y);
  if(!isNaN(nx)&&!isNaN(ny))return (nx-ny)*dir;
  return String(x).localeCompare(String(y),'he')*dir;});
 rows.forEach(r=>tb.appendChild(r));});
apply();
"""

PILL = {"שורד בדיקה מרובה": "s-ok", "מעל רעש, נופל בבדיקה מרובה": "s-bad",
        "רמז": "s-hint", "בתוך הרעש": "s-noise", "לא נבדק": "s-none",
        "תיאורי, לא מבחן": "s-none"}


def render(res: list, se: float, bonf: float, active: int,
           df: pd.DataFrame) -> str:
    e = html.escape
    cats = sorted({r["cat"] for r in res})
    stats = ["שורד בדיקה מרובה", "מעל רעש, נופל בבדיקה מרובה", "רמז",
             "בתוך הרעש", "תיאורי, לא מבחן", "לא נבדק"]
    survived = sum(1 for r in res if r["status"] == "שורד בדיקה מרובה")

    kpi = [(f"{len(res)}", "השערות במרשם"),
           (f"{active}", "בודקים פעילים"),
           (f"{df.net_R.mean():+.3f}R", "התוחלת שנמדדה"),
           (f"{se:.3f}R", "שגיאת תקן מקובצת"),
           (f"{bonf:.2f}R", "רף בדיקה מרובה"),
           (f"{survived}", "שרדו אותו")]

    rows_html = []
    for r in sorted(res, key=lambda x: -x["voi"]):
        eff = "—" if r["effect"] is None else f"{r['effect']:+.3f}R"
        rows_html.append(
            f'<tr data-cat="{e(r["cat"])}" data-status="{e(r["status"])}" '
            f'data-voi="{r["voi"]}" data-effect="{r["effect"] if r["effect"] is not None else -99}" '
            f'data-prior="{r["prior"]}" data-id="{e(r["id"])}">'
            f'<td class="id">{e(r["id"])}</td>'
            f'<td><b>{e(r["title"])}</b>'
            f'<div class="mech">{e(r["mechanism"])}</div></td>'
            f'<td class="num">{r["prior"]}</td>'
            f'<td class="num">{r["voi"]:.3f}</td>'
            f'<td class="num">{eff}</td>'
            f'<td><span class="pill {PILL.get(r["status"], "s-none")}">'
            f'{e(r["status"])}</span>'
            f'<div class="det">{e(r["detail"])}</div></td>'
            f'<td class="num">{e(r["needs"])}</td></tr>')

    btns = "".join(f'<button data-g="cat" data-f="{e(c)}" '
                   f'aria-pressed="false">{e(c)}</button>' for c in cats)
    sbtns = "".join(f'<button data-g="st" data-f="{e(s)}" '
                    f'aria-pressed="false">{e(s)}</button>' for s in stats)

    return f"""<!doctype html><html lang="he" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>מרשם ההשערות</title><style>{CSS}</style></head><body><div class="wrap">
<h1>מרשם ההשערות</h1>
<p class="sub">{len(res)} רעיונות, מדורגים לפי ערך מידע —
פריור כפול אפקט חלקי עלות — ולא לפי כמה הם נשמעים מבטיחים.</p>

<div class="warn">
<b>קרא את זה לפני שאתה מסתכל בטבלה.</b><br>
{active} בודקים על {len(df)} עסקאות. כדי שממצא ישרוד תיקון לבדיקה מרובה
הוא צריך אפקט של <b>{bonf:.2f}R</b>, כשכל הקצה שנמדד הוא
{df.net_R.mean():+.3f}R. כלומר <b>שום דבר כאן לא ניתן להוכחה מהנתונים
שיש</b> — וזה לא כישלון של הדף, זו המדידה.<br><br>
בלי התיקון הזה, מתוך {active} השערות חסרות ערך לחלוטין כחמש ייראו
מובהקות במקרה. הטור "אפקט" לבדו הוא הדרך היקרה ביותר להפסיד כאן כסף,
כי הוא נראה בדיוק כמו תשובה.<br><br>
<b>ועוד מלכודת אחת, שנתפסה בהרצה יבשה על רעש טהור.</b> בודק שמחזיר
מקסימום פחות מינימום על פני קבוצות — שעה, יום, סימבול, דירוג — הוא
כבר בחירה, והטווח שלו גדל עם מספר הקבוצות גם כשאין שום אפקט. על
נתונים שנבנו בלי שום מבנה, ארבעה כאלה "שרדו" את התיקון, ובראשם יום
השבוע ב-0.882R. הם מסומנים כאן <b>תיאורי, לא מבחן</b>, ולעולם לא
נספרים כממצא.
</div>

<div class="kpis">{''.join(
    f'<div class="kpi"><div class="v">{v}</div><div class="l">{l}</div></div>'
    for v, l in kpi)}</div>

<h2>סינון</h2>
<div class="bar">{btns}</div>
<div class="bar">{sbtns}</div>
<p class="sub"><span id="cnt">{len(res)}</span> שורות מוצגות.
לחיצה על כותרת ממיינת.</p>

<table><thead><tr>
<th data-k="id">מס׳</th><th>השערה והמנגנון</th>
<th data-k="prior">פריור</th><th data-k="voi">ערך מידע</th>
<th data-k="effect">אפקט</th><th>מצב ופירוט</th><th>דורש</th>
</tr></thead><tbody>{''.join(rows_html)}</tbody></table>

<footer>
<b>דורש:</b> replay = מהקובץ שכבר קיים · bars = מנרות חמש דקות ·
live = ממסחר קדימה · external = נתון חיצוני · firm = תשובה מאפקס.<br>
<b>הכלל:</b> השערה מאומצת רק אם יש לה מנגנון שאפשר להסביר בלי להסתכל
בטבלה, האפקט גדול מרף הבדיקה המרובה, והיא אומתה קדימה על נתונים
שלא שימשו למצוא אותה. מי שעובר רק על התנאי השני מאמץ רעש.<br>
נוצר מ-{e(str(len(df)))} עסקאות על פני {df.day.nunique()} ימי מסחר.
</footer>
</div><script>{JS}</script></body></html>"""


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out_override = None
    for a in sys.argv[1:]:
        if a.startswith("--out="):
            out_override = Path(a.split("=", 1)[1])
    csv = Path(args[0]) if args else CSV_DEFAULT
    if not csv.exists():
        sys.exit(f"אין {csv}. להריץ קודם את pipeline.py.")
    df = load(csv)
    if df.empty:
        sys.exit("אין עסקאות שהתמלאו בקובץ.")
    res, se, bonf, active = run_all(df)
    out = out_override or OUT_DEFAULT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(res, se, bonf, active, df), encoding="utf-8")
    survived = [r for r in res if r["status"] == "שורד בדיקה מרובה"]
    print(f"{len(res)} השערות, {active} בודקים פעילים, {len(df)} עסקאות")
    print(f"שגיאת תקן מקובצת {se:.3f}R · רף בדיקה מרובה {bonf:.2f}R")
    print(f"שרדו את התיקון: {len(survived)}")
    for r in survived:
        print(f"  {r['id']} {r['title']} — {r['effect']:+.3f}R")
    if not survived:
        print("  אף אחת. זו התוצאה הצפויה במדגם הזה, ולא תקלה.")
    print(f"\nהדף -> {out}")
    print("לפתוח אותו בדפדפן. עצמאי לחלוטין, שום נתון לא עוזב את המחשב.")


if __name__ == "__main__":
    main()
