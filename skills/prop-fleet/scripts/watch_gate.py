#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""watch_gate.py — הדוח היומי על השער, בלי שאף אחד יקליד כלום.

למה זה קיים
-----------
איסוף הראיות לוקח שבועות, והוא נכשל בשתי דרכים שקורות בשקט: הבוט
מת בלילה ואף אחד לא מבחין, או שהוא חי וכותב שורות פגומות. שתיהן
נראות בדיוק אותו דבר מבחוץ — עוד יום בלי התקדמות — ולכן צריך משהו
שמסתכל כל יום ואומר מה קרה.

הסקריפט הזה קורא בלבד. הוא לא נוגע בבוט, לא שולח פקודות לברוקר,
ולא כותב שום דבר אל תוך תיקיית הבוט. הוא כותב קובץ אחד לשולחן
העבודה ושולח הודעה לטלגרם, אם הוא מוצא אישורים.

הסוד לא נדפס ולא נכתב לשום מקום. הוא נקרא מ-.env אל תוך הזיכרון,
משמש לקריאת HTTPS אחת, ולא מופיע בדוח, בלוג או בהודעת שגיאה.
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
import urllib.parse
import urllib.request

from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paper_check import (FIX_LANDED, MIN_TRADES, sign_verdict,  # noqa: E402
                         split_eras, verdict_for)

HOME = Path.home()
BOT_DEFAULT = HOME / "Desktop" / "meirox-ai" / "MeiroX-AI - בוט מסחר"
OUT_DEFAULT = HOME / "Desktop" / "prop-fleet-status.txt"
EST = timezone(timedelta(hours=-4))

# הבוט ישן בין המושבים, ולכן לוג ישן אינו כשל בפני עצמו. מה שכן
# כשל הוא לוג שלא זז במשך מושב מסחר שלם.
STALE_HOURS = 20


def read_rows(db: Path) -> list:
    if not db.exists():
        return []
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    try:
        return list(con.execute("SELECT * FROM trades ORDER BY id"))
    finally:
        con.close()


def todays_decisions(log: Path, day: str) -> dict:
    """ספירה גסה של מה שהבוט עשה היום, מתוך הלוג שלו."""
    out = {"scans": 0, "approved": 0, "placed": 0, "cap": False, "alive": False}
    if not log.exists():
        return out
    try:
        text = log.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return out
    for line in text.splitlines():
        if day not in line:
            continue
        out["alive"] = True
        if "run_once —" in line:
            out["scans"] += 1
        if "✅ APPROVED" in line and "[Decision]" in line:
            out["approved"] += 1
        if "Order submitted" in line:
            out["placed"] += 1
        if "Daily trade cap hit" in line:
            out["cap"] = True
    return out


def read_risk_state(bot) -> dict | None:
    """מצב מתג ההרג. None כשאין קובץ או שאי אפשר לקרוא אותו."""
    try:
        s = json.loads((Path(bot) / "logs" / "risk_state.json")
                       .read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    accounts = s.get("accounts") or {}
    if not accounts:
        return None
    # חשבון אחד בפועל. אם יהיו כמה, הנעול הוא זה שחשוב.
    for a in accounts.values():
        if a.get("drawdown_latched"):
            return a
    return next(iter(accounts.values()))


def build_report(rows, decisions, log_age_h, now_str, cutoff=FIX_LANDED,
                 risk=None) -> str:
    """הדוח עצמו. פונקציה טהורה — מקבלת נתונים, מחזירה טקסט."""
    before, after = split_eras(rows, cutoff)
    good, bad, unknown = [], [], []
    for row in after:
        ok, why = verdict_for(row)
        (good if ok else unknown if ok is None else bad).append((row, why))
    orphan = [r for r in after if not r["analysis_id"]]
    sign_bad = []
    for r in after:
        if r["status"] == "closed" and r["pnl"] is not None:
            if sign_verdict(r)[0] is False:
                sign_bad.append(r)

    L = [f"prop-fleet — {now_str}", ""]

    # 1. האם המכונה בכלל חיה. זה קודם לכל מספר.
    if log_age_h is None:
        L.append("✗ אין לוג בוט. הוא לא רץ.")
    elif log_age_h > STALE_HOURS:
        L.append(f"✗ הלוג לא זז {log_age_h:.0f} שעות — הבוט כנראה מת.")
        L.append("  להריץ: launchctl kickstart -k gui/$(id -u)/com.meiroxai.bot")
    else:
        L.append(f"✓ הבוט חי (לוג בן {log_age_h:.1f} שעות)")

    # 2. מתג ההרג. זה חייב לבוא לפני המונה, כי מתג נעול הוא הסיבה
    #    לאפס עסקאות — והוא נראה בדיוק כמו יום שקט.
    if risk is not None:
        if risk.get("drawdown_latched"):
            reason = str(risk.get("drawdown_reason") or "")[:80]
            L.append(f"✗ מתג ההרג נעול — הבוט לא ייקח עסקאות. {reason}")
            L.append("  דורש איפוס ידני. המונה לא יזוז עד אז.")
        elif risk.get("broker_baseline_equity") is None:
            L.append("! בסיס ההון עוד לא אותחל — update_broker_equity")
            L.append("  לא נקרא מאז העלייה. נורמלי לפני המושב, לא אחריו.")
        else:
            dd = float(risk.get("drawdown_pct") or 0.0)
            L.append(f"✓ מתג ההרג פתוח (דרודאון {dd:.1f}%)")

    # 3. מה הוא עשה היום.
    d = decisions
    if not d["alive"]:
        L.append("· היום עוד לא נרשמה פעילות בלוג")
    else:
        line = f"· היום: {d['scans']} סריקות, {d['approved']} אושרו"
        if d["placed"]:
            line += f", {d['placed']} נשלחו"
        if d["cap"]:
            line += " (תקרה יומית נוצלה)"
        L.append(line)

    # 4. המונה — הדבר היחיד שמזיז את התאריך.
    L.append("")
    L.append(f"מונה הראיות: {len(good)}/{MIN_TRADES} עסקאות בנות-השוואה")
    if after:
        L.append(f"  {len(after)} עסקאות מאז {cutoff}, "
                 f"{len(unknown)} לא ניתנות להשוואה")
    else:
        L.append(f"  אפס עסקאות מאז {cutoff}. המונה לא זז.")
    if before:
        L.append(f"  ({len(before)} מלפני כן — מחוץ לפסק הדין, לא נמחקו)")

    # 5. כשלים. אלה עוצרים הכול.
    L.append("")
    if bad:
        L.append(f"✗ {len(bad)} עם יחס המרה שנחלק — חתימת באג ההמרה")
        for row, why in bad[:3]:
            L.append(f"    id={row['id']}: {why}")
    if orphan:
        L.append(f"✗ {len(orphan)} בלי analysis_id — תיקון סדר הרישום לא עבד")
        L.append(f"    id={', '.join(str(r['id']) for r in orphan[:5])}")
    if sign_bad:
        L.append(f"✗ {len(sign_bad)} שהרווח בהן סותר את הכיוון")

    clean = not bad and not orphan and not sign_bad
    if clean and len(good) >= MIN_TRADES:
        L.append("✓ נתיב הביצוע נקי והמונה מלא.")
        L.append("  תנאי השער מתקיים. אפשר לשקול רכישת הערכה אחת.")
    elif clean and after:
        L.append("✓ אין כשלים. ממשיכים לאסוף.")
    elif clean:
        L.append("· אין עדיין מה לבדוק. זה לא 'נקי', זה 'לא ידוע'.")
    else:
        L.append("✗ יש כשל. אין לקנות חשבון על המצב הזה.")

    return "\n".join(L)


# ── טלגרם ─────────────────────────────────────────────────────────
# הסוד נקרא לזיכרון ולא נדפס. שם המשתנה מזוהה בתבנית ולא בניחוש,
# כי אני לא יודע איך הוא נקרא אצלו.
TOKEN_RE = re.compile(r"^\s*(?:export\s+)?([A-Z0-9_]*TELEGRAM[A-Z0-9_]*"
                      r"(?:TOKEN|KEY)[A-Z0-9_]*)\s*=\s*(.+?)\s*$", re.I | re.M)
CHAT_RE = re.compile(r"^\s*(?:export\s+)?([A-Z0-9_]*TELEGRAM[A-Z0-9_]*"
                     r"CHAT[A-Z0-9_]*)\s*=\s*(.+?)\s*$", re.I | re.M)


def _strip(v: str) -> str:
    v = v.split(" #", 1)[0].strip()
    return v.strip('"').strip("'")


def find_telegram(paths) -> tuple:
    """(token, chat_id) או (None, None). שום ערך לא נדפס בשום מצב."""
    for p in paths:
        try:
            text = Path(p).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        t = TOKEN_RE.search(text)
        c = CHAT_RE.search(text)
        if t and c:
            return _strip(t.group(2)), _strip(c.group(2))
    return None, None


def send_telegram(token: str, chat: str, text: str) -> str:
    data = urllib.parse.urlencode({"chat_id": chat, "text": text}).encode()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        with urllib.request.urlopen(url, data=data, timeout=20) as r:
            return "נשלח" if r.status == 200 else f"קוד {r.status}"
    except Exception as e:                                   # noqa: BLE001
        # רק סוג השגיאה. גוף התשובה של טלגרם מחזיר את הטוקן בחלק
        # מהמקרים, ולכן הוא לא נכנס לכאן.
        return f"נכשל ({type(e).__name__})"


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    bot = Path(args[0]) if args else BOT_DEFAULT
    out = Path(os.environ.get("PF_STATUS_OUT", OUT_DEFAULT))

    now = datetime.now(tz=EST)
    log = bot / "logs" / "bot.log"
    try:
        age_h = (now.timestamp() - log.stat().st_mtime) / 3600.0
    except OSError:
        age_h = None

    report = build_report(
        read_rows(bot / "logs" / "trades.db"),
        todays_decisions(log, now.strftime("%Y-%m-%d")),
        age_h,
        now.strftime("%d/%m %H:%M"),
        risk=read_risk_state(bot),
    )

    out.write_text(report + "\n", encoding="utf-8")
    token, chat = find_telegram([bot / ".env", HOME / ".meirox_env"])
    if token and chat:
        status = send_telegram(token, chat, report)
    else:
        status = "לא נמצאו אישורי טלגרם — הדוח נכתב לקובץ בלבד"
    print(report)
    print(f"\n[{status}]  ->  {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
