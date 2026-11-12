"""Phase 0 goal arithmetic: compounding from $2,000 with cash lag and the program's scaling cap.

Every input is listed with its source id from sources.md. Inputs marked INFERRED are assumptions
the program must replace with per-product measurements in Phase 1.
Run: python3 -I dropshipping/phase0/goal_math.py
"""
import math

# ---- inputs (see sources.md ids) ----
EXTERNAL_CAP = 2000.0          # fill-in block
M0_SPEND = 250.0               # Shopify $1x3 months + AutoDS ~$40 + domain ~$15 + samples ~$60 + misc; cap in ladder is $300 (S-03,S-05,S-24)
FIXED_MONTHLY = 39.0 + 39.9 + 15.0/12   # Shopify Basic monthly (S-03), AutoDS Starter monthly (S-24, secondary), domain/yr (S-25)
COGS_SHARE = 0.30              # INFERRED: product+shipping as share of price; replace per product in Phase 1
FEE_SHARE = 0.034 + 0.02 + 0.01  # PayPal IL 3.4% (S-10) + Shopify 3rd-party 2% Basic (S-03) + ~1% intl surcharge (S-10); fixed 1.20 ILS ignored
REFUND_SHARE = 0.08            # overlay example allowance; INFERRED until observed
CONTRIB = 1 - COGS_SHARE - FEE_SHARE - REFUND_SHARE   # contribution before ads, as share of revenue
BREAKEVEN_ROAS = 1 / CONTRIB
HOLD_DAYS_NEW = 21             # PayPal new-seller hold up to 21 days (S-11, S-12)
HOLD_DAYS_LATER = 3            # INFERRED: after release limits; PayPal says "sooner" without a figure (S-12)
HOLD_SWITCH_DAY = 60           # INFERRED
RESERVE_MIN = 200.0            # overlay section 6
STEP_UP = 1.25                 # overlay section 6: 20-30% per step
STEP_DAYS = 7                  # INFERRED: one step per week after holding above breakeven
START_DAILY = 20.0             # overlay section 4 example test cap
DAYS = 24 * 30

def simulate(roas, failed_tests=0, days=DAYS, roas_decay=0.0):
    """Daily sim. roas_decay: ROAS multiplier exponent vs budget (0 = constant ROAS)."""
    cash = EXTERNAL_CAP - M0_SPEND - failed_tests * 120.0
    pending = {}            # day -> cash arriving
    daily = START_DAILY
    last_step = 0
    month_rev, month_profit, rows = 0.0, 0.0, []
    for d in range(1, days + 1):
        cash += pending.pop(d, 0.0)
        eff_roas = roas * (daily / START_DAILY) ** (-roas_decay) if roas_decay else roas
        # affordability: must pay ads + COGS now, revenue arrives later; keep reserve
        hold = HOLD_DAYS_NEW if d < HOLD_SWITCH_DAY else HOLD_DAYS_LATER
        spend_now_per_ad_dollar = 1 + eff_roas * COGS_SHARE
        affordable = max(0.0, (cash - RESERVE_MIN) / (spend_now_per_ad_dollar * min(hold, 7)))
        spend = min(daily, affordable)
        rev = spend * eff_roas
        cash -= spend + rev * COGS_SHARE + FIXED_MONTHLY / 30
        pending[d + hold] = pending.get(d + hold, 0.0) + rev * (1 - FEE_SHARE - REFUND_SHARE)
        month_rev += rev
        month_profit += rev * CONTRIB - spend - FIXED_MONTHLY / 30
        if eff_roas > BREAKEVEN_ROAS and d - last_step >= STEP_DAYS and spend >= daily * 0.99:
            daily *= STEP_UP; last_step = d
        if d % 30 == 0:
            rows.append((d // 30, month_rev, month_profit, daily, cash))
            month_rev = month_profit = 0.0
    return rows

def first_month_at(rows, level):
    for m, rev, *_ in rows:
        if rev >= level: return m
    return None

if __name__ == "__main__":
    print(f"contribution before ads = {CONTRIB:.3f}  -> breakeven ROAS = {BREAKEVEN_ROAS:.2f}")
    print(f"ad spend needed for $200k/month at ROAS 2.19 (S-15 median) = ${200000/2.19:,.0f}")
    print(f"working capital at $200k/mo, 21-day lag: ${200000*(1+COGS_SHARE/2.19*2.19)/30*21:,.0f} (ads+COGS paid before cash in)")
    cases = [("good: ROAS 3.0 constant", 3.0, 0, 0.0), ("base: ROAS 2.5 constant", 2.5, 0, 0.0),
             ("base, first 3 products fail", 2.5, 3, 0.0), ("base with ROAS decay 0.15/budget doubling", 2.5, 0, 0.15),
             ("thin: ROAS 2.0", 2.0, 0, 0.0)]
    for name, r, f, dec in cases:
        rows = simulate(r, f, roas_decay=dec)
        print(f"\n== {name} ==")
        print("month | revenue | profit | daily budget | cash")
        for m, rev, pr, dly, cash in rows[:24]:
            if m <= 12 or m % 6 == 0:
                print(f"{m:>5} | {rev:>9,.0f} | {pr:>8,.0f} | {dly:>8,.0f} | {cash:>9,.0f}")
        print("first month >= $10k rev:", first_month_at(rows, 10000), "| >= $50k:", first_month_at(rows, 50000), "| >= $200k:", first_month_at(rows, 200000))
    print("\nP(at least one product passes M1) with 5 serial $120 tests under the $900 M1 cap:")
    for p in (0.05, 0.10, 0.20, 0.30):
        print(f"  p={p:.2f}: {1-(1-p)**5:.2f}")


def plateau(roas0, k, b0=START_DAILY * 30):
    """If ROAS(B) = roas0*(B/b0)^-k per month, profit is maximised where marginal ROAS = breakeven.
    Returns (optimal monthly ad budget, revenue, profit) at that plateau, or None if never above breakeven."""
    if k <= 0:
        return None
    x = CONTRIB * roas0 * (1 - k)
    if x <= 1:
        return (0.0, 0.0, 0.0)
    b = b0 * x ** (1 / k)
    r = roas0 * (b / b0) ** (-k)
    return (b, b * r, b * (CONTRIB * r - 1) - FIXED_MONTHLY)


if __name__ == "__main__":
    print("\nProfit plateau if ROAS decays as a power of budget (k = fractional ROAS loss per budget doubling ~ k*0.69):")
    print("ROAS0 | k    | optimal ad $/mo | revenue $/mo | profit $/mo")
    for r in (3.0, 2.5, 2.2):
        for k in (0.05, 0.10, 0.15, 0.20):
            b, rev, pr = plateau(r, k)
            print(f"{r:>5} | {k:.2f} | {b:>14,.0f} | {rev:>12,.0f} | {pr:>10,.0f}")
