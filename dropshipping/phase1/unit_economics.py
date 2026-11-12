"""Unit economics for one candidate row (sweeps 1, 2, 4).

Usage:
  python3 -I dropshipping/phase1/unit_economics.py --price 39.9 --landed 14.5 --category home --gateway grow
  python3 -I dropshipping/phase1/unit_economics.py --price 39.9 --landed 14.5 --category pet --gateway paypal --vat 0.18

Every constant carries its source id (sources.md). Outputs: contribution before ads per order and as a share,
breakeven CPA and ROAS, both VAT scenarios, and the two-tranche stop-rule thresholds computed with test_stop_rule.py's model.
"""
import argparse, math, os, sys, importlib.util

FX = 3.17                      # ILS per USD, S-33 (expires 2026-11-17)
SHOPIFY_FEE = 0.02             # third-party gateway fee on Basic, S-03
GATEWAYS = {                   # variable %, fixed USD per order
    'shopify_payments': (0.029, 0.30),       # S-03 Basic online rate; no third-party fee (S-26)
    'grow':   (0.0075 + 0.006, 0.0),          # S-37, S-38 (0.75% + 0.6% Shopify surcharge); ₪59/mo fixed handled separately
    'paypal': (0.034 + 0.01 + 0.025, 1.20 / FX),  # S-10: 3.4% + 1% US buyer + 2.5% FX, ₪1.20 fixed
}
REFUND = {                     # refund + chargeback allowance by category, S-62, S-72 (secondary)
    'home': 0.17, 'pet': 0.10, 'electronics': 0.09, 'car': 0.10, 'apparel': 0.30, 'personal_care': 0.12, 'pod': 0.20,
}
FIXED_MONTHLY = 39.0 + 39.9            # Shopify Basic (S-03) + AutoDS Starter (S-24, secondary); US path has no gateway fixed fee

def run(price, landed, category, gateway, vat, monthly_orders=100):
    pct, fixed = GATEWAYS[gateway]
    fees = price * (pct + (0 if gateway == 'shopify_payments' else SHOPIFY_FEE)) + fixed
    refund_cost = REFUND[category] * price            # conservative: a refunded order loses the full price
    vat_cost = price * vat / (1 + vat) if vat else 0.0  # VAT inside the price if it applies (S-22, Unknown)
    contrib = price - landed - fees - refund_cost - vat_cost
    share = contrib / price
    be_cpa = contrib
    be_roas = price / contrib if contrib > 0 else float('inf')
    return dict(price=price, landed=landed, fees=round(fees, 2), refund_alloc=round(refund_cost, 2), vat=round(vat_cost, 2),
                contribution=round(contrib, 2), share=round(share, 3), breakeven_cpa=round(be_cpa, 2), breakeven_roas=round(be_roas, 2),
                fixed_per_order_at_100=round(FIXED_MONTHLY / monthly_orders, 2))

def stop_rule(contrib_share, price):
    spec = importlib.util.spec_from_file_location('sr', os.path.join(os.path.dirname(__file__), 'test_stop_rule.py'))
    sr = importlib.util.module_from_spec(spec); spec.loader.exec_module(sr)
    sr.PRICE, sr.CONTRIB = price, max(contrib_share, 0.01)
    sr.BE_CPA = price * sr.CONTRIB; sr.GOOD_CPA = 0.8 * sr.BE_CPA; sr.BAD_CPA = 2.0 * sr.BE_CPA
    best = None
    for k1 in (2, 3, 4, 5, 6):
        for t2 in (120.0, 180.0, 240.0):
            for k2 in (2, 3, 4, 5, 6, 8):
                r = sr.two_tranche(120.0, k1, t2, k2)
                g, b = r['good'][1], r['bad'][1]
                if g >= 0.70 and b <= 0.10 and (best is None or r['bad'][2] < best[0]):
                    best = (r['bad'][2], k1, t2, k2, g, b)
    return best

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--price', type=float, required=True); ap.add_argument('--landed', type=float, required=True)
    ap.add_argument('--category', choices=REFUND.keys(), default='home'); ap.add_argument('--gateway', choices=GATEWAYS.keys(), default='shopify_payments')
    ap.add_argument('--vat', type=float, default=None, help='omit to print both 0 and 0.18 scenarios')
    a = ap.parse_args()
    scenarios = [a.vat] if a.vat is not None else [0.0, 0.18]
    for v in scenarios:
        r = run(a.price, a.landed, a.category, a.gateway, v)
        print(f"VAT {v:.0%}: {r}")
        sr = stop_rule(r['share'], a.price)
        if sr:
            spend, k1, t2, k2, g, b = sr
            print(f"  stop rule: T1 $120 continue if purchases >= {k1}; T2 ${t2:.0f} pass if purchases >= {k2}; P(pass|good)={g:.2f}, P(pass|bad)={b:.2f}, E[spend|bad]=${spend:.0f}")
        else:
            print("  stop rule: no rule reaches P(pass|good)>=0.70 and P(pass|bad)<=0.10 within $360; product too thin to test at $20/day")
