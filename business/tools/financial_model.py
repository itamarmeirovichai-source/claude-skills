#!/usr/bin/env python3
"""
Unit economics and sensitivity model for the vacation rental video business.

Authoritative narrative: business/15-financial-model.md
Run:  python3 business/tools/financial_model.py
      python3 business/tools/financial_model.py --hours 4.0 --price 199

Every input is tagged MEASURED / PUBLISHED / ESTIMATE. As of writing, NOTHING is
MEASURED. The point of this script is to be re-run as real numbers replace guesses,
so that a decision is never made on a number nobody checked.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace

# --------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------

TAGS = {
    "price": "HYPOTHESIS (A-07, D-04)",
    "gen_seconds": "ESTIMATE (A-09)",
    "gen_cost_per_second": "PUBLISHED (E-22: Kling $0.09-0.14/s)",
    "attempt_ratio": "ESTIMATE (A-09) - least-known number in the model",
    "music_monthly": "PUBLISHED (E-18: Epidemic Sound Pro $203.88/yr)",
    "stripe_pct": "PUBLISHED (E-25: 2.9% + $0.30)",
    "hours_per_order": "ESTIMATE (A-10) - DOMINANT VARIABLE",
    "revision_rate": "ESTIMATE (A-11)",
    "refund_rate": "ESTIMATE (A-12)",
    "conversion_rate": "PLACEHOLDER (A-13) - not a forecast",
}


@dataclass(frozen=True)
class Inputs:
    # Revenue
    price: float = 279.00                 # Standard package

    # Generation
    gen_seconds: float = 50.0             # seconds of usable footage per order
    gen_cost_per_second: float = 0.12     # midpoint of E-22 Kling range
    attempt_ratio: float = 2.5            # attempts per ACCEPTED clip

    # Other variable cash costs
    music_monthly: float = 17.00
    orders_per_month: float = 10.0
    storage_per_order: float = 0.50
    stripe_pct: float = 0.029
    stripe_fixed: float = 0.30

    # Time
    hours_per_order: float = 2.53
    founder_opportunity_cost: float = 50.00   # $/h, for the profit line only

    # Behaviour
    revision_rate: float = 0.35
    refund_rate: float = 0.05
    conversion_rate: float = 0.25             # qualified conversation -> order

    # Fixed monthly
    fixed_monthly: float = 117.00

    # Acquisition
    target_cac: float = 75.00


# --------------------------------------------------------------------------
# Model
# --------------------------------------------------------------------------


def generation_cost(i: Inputs) -> tuple[float, float]:
    """Return (successful_cost, wasted_cost)."""
    successful = i.gen_seconds * i.gen_cost_per_second
    wasted = successful * (i.attempt_ratio - 1.0)
    return successful, wasted


def cash_cost_per_order(i: Inputs) -> dict[str, float]:
    successful, wasted = generation_cost(i)
    music = i.music_monthly / i.orders_per_month if i.orders_per_month else 0.0
    stripe = i.price * i.stripe_pct + i.stripe_fixed
    lines = {
        "Generation (accepted clips)": successful,
        "Generation (failed attempts)": wasted,
        "Music licence (amortised)": music,
        "Editing software": 0.00,
        "Storage & delivery": i.storage_per_order,
        "Payment processing": stripe,
    }
    lines["TOTAL"] = sum(lines.values())
    return lines


def contribution_margin(i: Inputs) -> float:
    return i.price - cash_cost_per_order(i)["TOTAL"]


def effective_hourly(i: Inputs) -> float:
    if i.hours_per_order <= 0:
        return float("inf")
    return contribution_margin(i) / i.hours_per_order


def margin_after_refunds(i: Inputs) -> float:
    """Refund reverses revenue; costs already incurred are not recovered.

    Stripe's percentage fee is generally returned on a refund but the fixed
    portion and the production cost are not. Modelled conservatively.
    """
    cm = contribution_margin(i)
    cost = cash_cost_per_order(i)["TOTAL"]
    loss_per_refund = cost  # full cost sunk, zero revenue retained
    return cm * (1 - i.refund_rate) - loss_per_refund * i.refund_rate


def break_even_cac(i: Inputs) -> float:
    return contribution_margin(i)


def break_even_cac_with_time(i: Inputs) -> float:
    return contribution_margin(i) - i.hours_per_order * i.founder_opportunity_cost


def monthly(i: Inputs, orders: float, ad_spend: float = 0.0) -> dict[str, float]:
    revenue = orders * i.price
    variable = orders * cash_cost_per_order(i)["TOTAL"]
    hours = orders * i.hours_per_order
    cash_profit = revenue - variable - i.fixed_monthly - ad_spend
    return {
        "orders": orders,
        "revenue": revenue,
        "variable_costs": variable,
        "fixed_costs": i.fixed_monthly,
        "ad_spend": ad_spend,
        "cash_profit_before_founder_pay": cash_profit,
        "founder_hours": hours,
        "effective_hourly": cash_profit / hours if hours else 0.0,
    }


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------


def money(x: float) -> str:
    return f"${x:,.2f}"


def rule(title: str = "", width: int = 78) -> None:
    if title:
        print(f"\n{title}")
        print("=" * width)
    else:
        print("-" * width)


def report(i: Inputs) -> None:
    rule("INPUT PROVENANCE")
    for key, tag in TAGS.items():
        val = getattr(i, key, None)
        shown = "n/a" if val is None else f"{val}"
        print(f"  {key:<24} {shown:<10} {tag}")
    print("\n  *** NOTHING IS CURRENTLY MEASURED. All figures below are provisional. ***")

    rule(f"UNIT ECONOMICS - one order at {money(i.price)}")
    for name, amount in cash_cost_per_order(i).items():
        marker = "  " if name != "TOTAL" else "  = "
        print(f"{marker}{name:<34} {money(amount):>10}")
    cm = contribution_margin(i)
    print(f"\n  Contribution margin (cash)         {money(cm):>10}"
          f"   ({cm / i.price * 100:.1f}%)")
    print(f"  Founder hours per order            {i.hours_per_order:>10.2f}")
    print(f"  EFFECTIVE HOURLY EARNINGS          {money(effective_hourly(i)):>10}")
    print(f"  Margin after refunds at {i.refund_rate:.0%}        {money(margin_after_refunds(i)):>10}")

    rule("ACQUISITION")
    print(f"  Break-even CAC (cash only)         {money(break_even_cac(i)):>10}")
    print(f"  Break-even CAC (incl. founder time){money(break_even_cac_with_time(i)):>10}")
    print(f"  Target CAC                         {money(i.target_cac):>10}")
    print(f"  -> implied max cost per qualified lead at {i.conversion_rate:.0%} conversion: "
          f"{money(i.target_cac * i.conversion_rate)}")
    print(f"  Fixed costs covered by             "
          f"{i.fixed_monthly / cm:>10.2f} orders/month")

    rule("TIME SENSITIVITY - the dominant variable")
    print(f"  {'hours/order':>12}  {'effective hourly':>18}")
    for h in (1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0):
        v = effective_hourly(replace(i, hours_per_order=h))
        flag = ""
        if v < 60:
            flag = "   <-- below tripwire ($60/h): stop selling, fix delivery"
        print(f"  {h:>12.1f}  {money(v):>18}{flag}")

    rule("SINGLE-VARIABLE SHOCKS")
    shocks = [
        ("Base case", i),
        ("Attempt ratio 2.5 -> 7.5", replace(i, attempt_ratio=7.5)),
        ("Revision rate 35% -> 70%", replace(i, revision_rate=0.70,
                                             hours_per_order=i.hours_per_order + 0.15)),
        ("Price 279 -> 199", replace(i, price=199.0)),
        ("Price 279 -> 149", replace(i, price=149.0)),
        ("Hours 2.53 -> 4.0", replace(i, hours_per_order=4.0)),
        ("Hours 2.53 -> 5.0", replace(i, hours_per_order=5.0)),
        ("Refunds 5% -> 20%", replace(i, refund_rate=0.20)),
    ]
    print(f"  {'scenario':<28} {'margin':>10} {'post-refund':>13} {'eff. hourly':>13}")
    for name, s in shocks:
        print(f"  {name:<28} {money(contribution_margin(s)):>10} "
              f"{money(margin_after_refunds(s)):>13} {money(effective_hourly(s)):>13}")

    rule("COMPOUND BAD CASE - the one that kills the business")
    bad = replace(i, price=199.0, hours_per_order=4.0, refund_rate=0.15,
                  attempt_ratio=5.0)
    bad_cac = 150.0
    net = margin_after_refunds(bad) - bad_cac
    print(f"  Price {money(bad.price)}, 4.0h/order, 15% refunds, 5x attempts, "
          f"CAC {money(bad_cac)}")
    print(f"  Margin after refunds:              {money(margin_after_refunds(bad)):>10}")
    print(f"  Net of CAC:                        {money(net):>10}")
    print(f"  Effective hourly net of CAC:       "
          f"{money(net / bad.hours_per_order):>10}")
    print("  -> Every one of these four shifts is individually survivable.")
    print("     Together they are fatal. Watch the combination, not the components.")

    rule("MONTHLY SCENARIOS")
    scenarios = [
        ("Conservative", replace(i, price=220.0), 4.0, 0.0),
        ("Base", i, 10.0, 300.0),
        ("Optimistic", replace(i, price=310.0), 18.0, 750.0),
    ]
    print(f"  {'':<14}{'orders':>7}{'revenue':>11}{'cash profit':>13}"
          f"{'hours':>8}{'eff/h':>10}")
    for name, s, orders, ads in scenarios:
        m = monthly(s, orders, ads)
        print(f"  {name:<14}{m['orders']:>7.0f}{money(m['revenue']):>11}"
              f"{money(m['cash_profit_before_founder_pay']):>13}"
              f"{m['founder_hours']:>8.1f}{money(m['effective_hourly']):>10}")
    print("\n  Note: the optimistic hourly rate is barely better than base.")
    print("  Volume does not fix the hourly ceiling. Only fewer hours per order does.")

    rule("PORTFOLIO PRICING CHECK - do not quote before measuring")
    per_prop_price = 199.0
    n = 5
    for label, per_prop_hours in (("reuse works", 1.4), ("reuse fails", i.hours_per_order)):
        rev = per_prop_price * n
        cost = cash_cost_per_order(replace(i, price=per_prop_price))["TOTAL"] * n
        hrs = per_prop_hours * n
        print(f"  {label:<14} revenue {money(rev):>9}  hours {hrs:>5.1f}  "
              f"eff/h {money((rev - cost) / hrs):>9}")
    print(f"  Compare: {n} separate Standard orders -> "
          f"eff/h {money(effective_hourly(i))}")
    print("  -> If reuse fails, portfolio work EARNS LESS PER HOUR than single orders.")
    print("     That is growth into a loss. Measure one 5-property job first.")

    rule("TRIPWIRES")
    ehr = effective_hourly(i)
    checks = [
        ("Effective hourly >= $60/h", ehr >= 60, f"{money(ehr)}"),
        ("Contribution margin >= $100", cm >= 100, money(cm)),
        ("Refund rate <= 15%", i.refund_rate <= 0.15, f"{i.refund_rate:.0%}"),
        ("Revision rate <= 70%", i.revision_rate <= 0.70, f"{i.revision_rate:.0%}"),
        ("Price >= $149 floor", i.price >= 149, money(i.price)),
    ]
    for label, ok, val in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:<34} {val}")
    print()


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--price", type=float, help="order price")
    p.add_argument("--hours", type=float, help="founder hours per order")
    p.add_argument("--attempts", type=float, help="generation attempts per accepted clip")
    p.add_argument("--refunds", type=float, help="refund rate, e.g. 0.05")
    p.add_argument("--orders", type=float, help="orders per month")
    args = p.parse_args()

    i = Inputs()
    if args.price:
        i = replace(i, price=args.price)
    if args.hours:
        i = replace(i, hours_per_order=args.hours)
    if args.attempts:
        i = replace(i, attempt_ratio=args.attempts)
    if args.refunds is not None:
        i = replace(i, refund_rate=args.refunds)
    if args.orders:
        i = replace(i, orders_per_month=args.orders)

    report(i)


if __name__ == "__main__":
    main()
