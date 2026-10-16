#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""install_watch_gate.py — מתקין את הבדיקה היומית ואז מסתלק.

אחרי ההתקנה הזאת אין יותר מה להריץ. כל יום חול ב-16:20 שעון ניו
יורק, אחרי שהמושב נסגר, launchd מריץ את הבדיקה ושולח את התוצאה
לטלגרם.

הסקריפטים מועתקים ל-~/prop-fleet-watch כי תיקיית pf שבשולחן
העבודה נמחקת בכל הורדה מחדש, ומשימה שמצביעה על קובץ שנמחק נכשלת
בשקט — וכישלון שקט הוא בדיוק מה שהבדיקה הזאת אמורה למנוע.

מה זה לא עושה: לא נוגע בקוד הבוט, לא משנה את config.yaml, לא
מפעיל ולא עוצר את הבוט, ולא שולח שום פקודה לברוקר.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

from pathlib import Path

HOME = Path.home()
HERE = Path(__file__).resolve().parent
DEST = HOME / "prop-fleet-watch"
LABEL = "com.meiroxai.gatecheck"
PLIST = HOME / "Library" / "LaunchAgents" / f"{LABEL}.plist"
BOT_DEFAULT = HOME / "Desktop" / "meirox-ai" / "MeiroX-AI - בוט מסחר"
NEEDED = ("watch_gate.py", "paper_check.py")


def die(msg: str) -> None:
    print(f"\n  ✗ {msg}")
    print("  שום דבר לא הותקן.")
    sys.exit(1)


def plist_text(python: Path, bot: Path) -> str:
    def esc(s) -> str:
        return (str(s).replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;"))
    days = "".join(
        f"""
    <dict>
      <key>Weekday</key><integer>{d}</integer>
      <key>Hour</key><integer>16</integer>
      <key>Minute</key><integer>20</integer>
    </dict>""" for d in range(1, 6))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>{LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>{esc(python)}</string>
    <string>{esc(DEST / 'watch_gate.py')}</string>
    <string>{esc(bot)}</string>
  </array>
  <key>RunAtLoad</key><false/>
  <key>StartCalendarInterval</key>
  <array>{days}
  </array>
  <key>WorkingDirectory</key><string>{esc(DEST)}</string>
  <key>StandardOutPath</key><string>/tmp/gatecheck.log</string>
  <key>StandardErrorPath</key><string>/tmp/gatecheck_error.log</string>
</dict>
</plist>
"""


def run(*cmd) -> tuple:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    bot = Path(args[0]) if args else BOT_DEFAULT
    print("=" * 62)
    print("  התקנת הבדיקה היומית")
    print("=" * 62)

    if not (bot / "logs").is_dir():
        die(f"לא מצאתי את הבוט ב-{bot}")
    python = bot / "venv" / "bin" / "python"
    if not python.exists():
        die(f"לא מצאתי פייתון ב-{python}")
    for name in NEEDED:
        if not (HERE / name).exists():
            die(f"חסר {name} לצד הסקריפט הזה")

    DEST.mkdir(exist_ok=True)
    for name in NEEDED:
        shutil.copy2(HERE / name, DEST / name)
        print(f"  ✓ הועתק: {name}")

    # מריצים פעם אחת לפני שמתקינים. משימה מתוזמנת שנכשלת בהרצה
    # הראשונה שלה תיכשל בשקט כל יום, ואיש לא יידע.
    print("\n  הרצת ניסיון:")
    code, out = run(str(python), str(DEST / "watch_gate.py"), str(bot))
    if code != 0:
        print(out[-1500:])
        die("הרצת הניסיון נכשלה — לא מתקין משימה שלא עובדת")
    for line in out.splitlines():
        print(f"    {line}")

    PLIST.parent.mkdir(parents=True, exist_ok=True)
    PLIST.write_text(plist_text(python, bot), encoding="utf-8")
    code, out = run("plutil", "-lint", str(PLIST))
    if code != 0:
        PLIST.unlink(missing_ok=True)
        die(f"ה-plist לא תקין: {out}")
    print(f"\n  ✓ נכתב: {PLIST}")

    uid = os.getuid()
    run("launchctl", "bootout", f"gui/{uid}/{LABEL}")
    run("launchctl", "enable", f"gui/{uid}/{LABEL}")
    code, out = run("launchctl", "bootstrap", f"gui/{uid}", str(PLIST))
    if code != 0:
        code, out = run("launchctl", "load", "-w", str(PLIST))
    _, listing = run("launchctl", "list")
    loaded = any(LABEL in ln for ln in listing.splitlines())
    print(f"  {'✓' if loaded else '✗'} המשימה "
          f"{'טעונה' if loaded else 'לא נטענה: ' + out[:120]}")

    print("\n" + "=" * 62)
    if loaded:
        print("  מותקן. כל יום חול ב-16:20 שעון ניו יורק תקבל הודעה.")
        print("  הדוח נשמר גם ב-~/Desktop/prop-fleet-status.txt")
        print(f"\n  להסרה:  launchctl bootout gui/{uid}/{LABEL}")
    else:
        print("  ההעתקה הצליחה אבל launchd סירב. הדוח עדיין רץ ידנית:")
        print(f"    '{python}' ~/prop-fleet-watch/watch_gate.py")
    print("=" * 62)
    return 0 if loaded else 1


if __name__ == "__main__":
    sys.exit(main())
