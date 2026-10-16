"""מתי הריבית דריבית מתחילה באמת לעבוד."""
import numpy as np

NET = 246_777.0      # נטו לשנה במצב יציב, 20x50K ב-+0.30R, מס 25%
RAMP = [53_194, 198_858, 247_552, 245_366]   # ארבע השנים הראשונות
START_EXTRACT = 4    # מהשנה החמישית

def run(years, port_r, biz_r, net=NET, ramp=RAMP):
    res = port = biz = 0.0
    hist = []
    for y in range(years):
        port *= (1 + port_r); biz *= (1 + biz_r)
        cash = ramp[y] if y < len(ramp) else net
        if y >= START_EXTRACT:
            a = cash * 0.25
            port += a; biz += a; res += cash - 2*a
        else:
            res += cash
        hist.append((y+1, res, port, biz))
    return hist

for pr, br, label in [(0.07, 0.12, "7% / 12%"), (0.05, 0.08, "5% / 8%"), (0.0, 0.0, "אפס")]:
    h = run(20, pr, br)
    print(f"\n=== תשואות {label} ===")
    print(f"{'שנה':>5} {'רזרבה':>12} {'תיק':>12} {'עסקים':>12} {'הון':>13} {'מזה תשואות':>12}")
    contributed = 0.0
    for y, res, port, biz in h:
        cash_in = sum(RAMP[:min(y,4)]) + max(0, y-4)*NET
        tot = res+port+biz
        if y in (4, 8, 12, 15, 20):
            print(f"{y:>5} {res:>12,.0f} {port:>12,.0f} {biz:>12,.0f} "
                  f"{tot:>13,.0f} {tot-cash_in:>12,.0f}")

print("\n\nחלק התשואות מתוך ההון, לאורך זמן (7%/12%):")
h = run(25, 0.07, 0.12)
print(f"{'שנה':>5} {'הון':>13} {'מזומן שנכנס':>14} {'מהתשואות':>12} {'%':>7}")
for y, res, port, biz in h:
    if y % 5 == 0 or y == 8:
        cash_in = sum(RAMP[:min(y,4)]) + max(0, y-4)*NET
        tot = res+port+biz
        g = tot - cash_in
        print(f"{y:>5} {tot:>13,.0f} {cash_in:>14,.0f} {g:>12,.0f} {100*g/tot:>6.1f}%")
