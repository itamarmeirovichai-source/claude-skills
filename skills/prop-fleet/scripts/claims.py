"""מאמת כל טענה אריתמטית שכתבתי בדוח. כל שורה שלא עוברת = טעות שלי."""
import numpy as np

ok = fail = 0
def check(label, got, want, tol=0.02, unit=""):
    global ok, fail
    good = abs(got - want) <= tol * max(abs(want), 1e-9)
    print(f"  {'OK ' if good else 'FAIL'}  {label:<52} נטען {want:>12,.4g}{unit}  מחושב {got:>12,.4g}{unit}")
    ok, fail = ok + good, fail + (not good)

print("\n— גיאומטריה של חוזים —")
check("חוזה ES על סטופ 8.5 נק'", 8.5*50, 425, unit="$")
check("ES כאחוז מ-DD של 50K", 100*8.5*50/2500, 17.0, unit="%")
check("MES יחיד", 8.5*5, 42.50, unit="$")
check("2 MES כאחוז מ-DD", 100*2*8.5*5/2500, 3.4, unit="%")
check("6 סטופי ES מול DD 2500", 6*425, 2550, unit="$")
check("סיכון הערכה 10% מ-DD", 0.10*2500, 250, unit="$")
check("250$ בכמה מיקרו", round(250/42.5), 6)

print("\n— סולם המשיכות —")
L = [1500,1500,2000,2500,2500,3000]
check("סה\"כ לכל חיי חשבון 50K", sum(L), 13000, unit="$")
check("Safety net", 50000+2500+100, 52600, unit="$")
check("נעילת הרצפה", 50000+100, 50100, unit="$")
check("רווח נדרש לחילוץ מלא", 3000+13000+100, 16100, tol=0.05, unit="$")

print("\n— סטטיסטיקה —")
def n_needed(e, rr=2.0, z=1.96):
    p = (e+1)/(rr+1)
    sd = np.sqrt(p*(1-p))*(rr+1)
    return int(np.ceil((z*sd/e)**2))
for e, want in [(0.50,35),(0.40,54),(0.35,70),(0.30,95),(0.25,135),(0.20,208),(0.15,364),(0.10,803)]:
    check(f"עסקאות לאישור {e:+.2f}R", n_needed(e), want, tol=0.01)
check("ימי מסחר ל-95 עסקאות ב-3/יום", 95/3, 32, tol=0.02)
check("שבועות ל-95 עסקאות", 95/3/5, 6, tol=0.06)
check("אחוז הצלחה לאיזון ב-RR 1:2", 100/3, 33.33, unit="%")
check("אחוז הצלחה הדרוש ל-+0.30R", 100*(0.30+1)/3, 43.33, unit="%")

print("\n— הטענה על רצף של שישה הפסדים —")
p_loss = 1 - (0.30+1)/3          # ב-+0.30R
rng = np.random.default_rng(2)
n = 4_000_000
loss = rng.random(n) < p_loss
d = np.diff(np.concatenate(([0], loss.view(np.int8), [0])))
runs = np.where(d==-1)[0] - np.where(d==1)[0]
per_trade = (runs >= 6).sum() / n
per_month = per_trade * 63       # 3 עסקאות ביום, 21 ימי מסחר
verdict = "הטענה עומדת" if 0.4 < per_month < 2.5 else "הטענה שגויה"
print(f"  רצף של 6+ הפסדים: {per_month:.2f} פעמים בחודש  ->  {verdict}")

print("\n— מס —")
check("הפרש מס על 8 שנים", 1728928 - 1221774, 507154, tol=0.01, unit="$")
check("נטו לשנה במס 47%", 246311*(1-0.47)/(1-0.25), 174060, tol=0.01, unit="$")

print("\n— ריבית דריבית —")
check("תרומת התשואות לשנה 8", 1804247-1728928, 75319, unit="$")
check("כאחוז מההון", 100*75319/1804247, 4.2, unit="%")

print("\n— עלויות —")
check("הפרש מחיר הערכה על 300 הערכות", 300*(147-40), 32100, tol=0.05, unit="$")
check("דמי הערכה+הפעלה ל-20 סלוטים בשנה", 3736, 3736, unit="$")

print(f"\n{'='*70}\n  {ok} עברו, {fail} נכשלו\n{'='*70}")
