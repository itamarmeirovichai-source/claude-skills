"""Operating characteristics of the $120 product test (sweep 4, statistics).

Model: purchases in a tranche ~ Poisson(spend / true CPA). "Good" product: true CPA at or below
0.8 x breakeven CPA (contribution margin covers ads with room). "Bad" product: true CPA at 2 x
breakeven. Breakeven CPA = price x contribution share (sweep 1: 0.556; price assumption $40 -> $22.2).
Inputs are assumptions to be replaced by per-product numbers; the point is the shape of the rule,
not the exact numbers. No peeking: each tranche is read once at its end (Evan Miller, S-90; Johari et al., S-91).
Run: python3 -I dropshipping/phase1/test_stop_rule.py
"""
import math

PRICE = 40.0
CONTRIB = 0.556
BE_CPA = PRICE * CONTRIB            # $22.24
GOOD_CPA = 0.8 * BE_CPA             # $17.8
BAD_CPA = 2.0 * BE_CPA              # $44.5

def pois_cdf(k, lam):
    return sum(math.exp(-lam) * lam**i / math.factorial(i) for i in range(k + 1))

def p_at_least(k, lam):
    return 1 - pois_cdf(k - 1, lam) if k > 0 else 1.0

def two_tranche(t1, k1, t2, k2):
    """Pass tranche 1 if purchases >= k1; then pass tranche 2 if purchases >= k2 (fresh count)."""
    out = {}
    for name, cpa in (("good", GOOD_CPA), ("bad", BAD_CPA)):
        p1 = p_at_least(k1, t1 / cpa)
        p2 = p_at_least(k2, t2 / cpa)
        exp_spend = t1 + p1 * t2
        out[name] = (p1, p1 * p2, exp_spend)
    return out

if __name__ == "__main__":
    print(f"price ${PRICE:.0f}, contribution {CONTRIB:.3f}, breakeven CPA ${BE_CPA:.2f}; good CPA ${GOOD_CPA:.2f}, bad CPA ${BAD_CPA:.2f}")
    print("tranche1 $ | k1 | tranche2 $ | k2 | P(pass T1|good) | P(pass both|good) | P(pass T1|bad) | P(pass both|bad) | E[spend|bad]")
    best = None
    for t1 in (120.0,):
        for k1 in (2, 3, 4, 5):
            for t2 in (120.0, 180.0, 240.0):
                for k2 in (3, 4, 5, 6, 8):
                    r = two_tranche(t1, k1, t2, k2)
                    g1, g12, _ = r["good"]; b1, b12, bs = r["bad"]
                    ok = g12 >= 0.70 and b12 <= 0.10
                    print(f"{t1:>9.0f} | {k1:>2} | {t2:>9.0f} | {k2:>2} | {g1:>15.2f} | {g12:>17.2f} | {b1:>14.2f} | {b12:>16.2f} | {bs:>12.0f} {'<- meets 70/10' if ok else ''}")
                    if ok and (best is None or bs < best[0]):
                        best = (bs, t1, k1, t2, k2, g12, b12)
    if best:
        bs, t1, k1, t2, k2, g12, b12 = best
        print(f"\nChosen rule (lowest expected spend on a bad product among rules with P(pass|good)>=0.70 and P(pass|bad)<=0.10):")
        print(f"  T1 ${t1:.0f}: continue only if purchases >= {k1}; T2 ${t2:.0f}: pass M1-candidate only if purchases >= {k2}.")
        print(f"  P(pass|good)={g12:.2f}, P(pass|bad)={b12:.2f}, expected spend on a bad product ${bs:.0f}, max spend ${t1+t2:.0f}.")
    # single-read false-positive rate for the naive rule "any purchase = keep going"
    print(f"\nNaive rule 'kill only if zero purchases in $120': P(keep|bad)={p_at_least(1,120/BAD_CPA):.2f}, P(keep|good)={p_at_least(1,120/GOOD_CPA):.2f}")
    # peeking illustration: reading daily and stopping on the first day with >=1 purchase
    lam_bad_day = 20 / BAD_CPA
    print(f"Peeking daily and 'confirming' on the first purchase: P(a bad product shows >=1 purchase within 6 days)={1-math.exp(-6*lam_bad_day):.2f}")
