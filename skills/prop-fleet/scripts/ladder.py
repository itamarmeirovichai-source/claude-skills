"""How many trades before we are allowed to believe the edge, and what
being wrong costs at each rung."""
import numpy as np

RR = 2.0
TRADES_DAY = 3


def sd_R(avg_R, rr=RR):
    p = (avg_R + 1) / (rr + 1)
    return np.sqrt(p * (1 - p)) * (rr + 1)


def n_needed(effect, conf=1.96, rr=RR):
    """Trades before a 95% CI around an observed `effect` excludes zero."""
    return int(np.ceil((conf * sd_R(effect, rr) / effect) ** 2))


print("how long until an edge is real (95% confidence, RR 1:2)")
print(f"{'observed':>9} {'trades':>8} {'trading days':>13} {'weeks':>7}")
for e in (0.50, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10):
    n = n_needed(e)
    print(f"{e:>+9.2f} {n:>8,} {n/TRADES_DAY:>13,.0f} {n/TRADES_DAY/5:>7,.0f}")

print()
print("the ladder: exposure only rises when the evidence does")
STAGES = [
    ("0. שקוף", 0, 0, "לתקן את הבאג, להריץ סימולציה מלאה, אפס כסף"),
    ("1. חשבון אחד", 1, 100, "CI תחתון > 0"),
    ("2. שלושה", 3, 250, "CI תחתון > +0.10R"),
    ("3. עשרה", 10, 500, "CI תחתון > +0.20R"),
    ("4. עשרים", 20, 900, "CI תחתון > +0.20R ורבעון רווחי אחד לפחות"),
]
FEE = 125.0
print(f"{'שלב':>14} {'חשבונות':>9} {'טריידים':>9} {'ימים':>7} {'עלות אם אין קצה':>18}")
prev = 0
for name, acc, n, cond in STAGES:
    days = (n - prev) / TRADES_DAY
    # at zero edge an account dies or expires roughly every 25 trading days
    cycles = max(1, days / 25)
    cost = acc * FEE * cycles
    print(f"{name:>14} {acc:>9} {n:>9,} {days:>7,.0f} {cost:>18,.0f}")
    prev = n
print()
print("the point of the gate: the cost of being wrong depends only on where you stop")
print(f"  stop at stage 1 (no edge found)          ~${STAGES[1][1]*FEE*max(1,(STAGES[1][2]/TRADES_DAY)/25):,.0f}")
print("  never gate, run 20 accounts for 8 years   ~$114,000   (see apex_model.py, -0.10R)")
