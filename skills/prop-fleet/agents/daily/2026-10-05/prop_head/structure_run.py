"""Head of Prop Structure, 2026-10-05.
Question: which firms satisfy BOTH unchangeable rules (fully automatic; many funded
accounts can be bought), with how many accounts, and what does it pay at each expectancy?

CONDITIONAL ON AN EDGE WE DO NOT HAVE. Nothing here is an edge claim.
Re-uses today's economist plans and simulator UNCHANGED (economist/economist_run.py,
economist/fleet_model.py). New here: (1) firm subsets by rule-1 status after today's
rules-keeper and red-team findings, (2) exit stresses for the documented discretionary
exits (Bulenox Master->Funded after 3 payouts; Topstep call-up to Live closes all XFAs),
modelled with the existing max_payouts key (account leaves, slot buys a fresh eval),
(3) the same tables with commission and slippage set to 0, so a backtest R that is
ALREADY net of costs is not charged twice (economist finding: ~0.05R/trade).
"""
import sys, os, copy
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "economist"))
import economist_run as er
fm = er.fm

RS = (0.10, 0.25, 0.40)
SS = er.SS

def stress(key, P, mode):
    P = copy.deepcopy(P)
    if mode == "exit3":
        if key == "Bulenox": P["max_payouts"] = 3     # Master closed or moved to Funded (unknown automation terms)
        if key == "Topstep": P["max_payouts"] = 3     # proxy for a call-up at an unknown time (ASSUMED count)
    return P

def run(keys, R, td, mode="base"):
    tot = 0; fees = 0
    for k in keys:
        P = stress(k, er.FIRM_PLANS[k], mode)
        d = er.firm(k, R, P=P, trades_day=td)
        tot = tot + d["net_year"][:, SS].mean(axis=1); fees += d["fees"][:, SS].mean()
    return tot, fees

FLEETS = {
    "P1 Bulenox5+Topstep5 (10)": ["Bulenox", "Topstep"],
    "P2 +Lucid5 if approved (15)": ["Bulenox", "Topstep", "Lucid"],
    "Bulenox5 alone (5)": ["Bulenox"],
    "Tradeify5 alone, own instance (5)": ["Tradeify"],
}

def block(cost_label):
    print(f"\n##### {cost_label}")
    for name, ks in FLEETS.items():
        cap = 50_000. * 5 * len(ks)
        for mode in ("base", "exit3"):
            if mode == "exit3" and not any(k in ("Bulenox", "Topstep") for k in ks):
                continue
            for td in (3, 1):
                cells = []
                for R in RS:
                    net, fees = run(ks, R, td, mode)
                    cells.append(f"{R:+.2f}R {net.mean():>8,.0f} ({100*net.mean()/cap:4.1f}%, p10 {np.percentile(net,10):>8,.0f}, fees {fees:>6,.0f})")
                print(f"  {name:34} {mode:5} {td}/day | " + " | ".join(cells))

def r_needed(ks, td, mode):
    cap = 50_000. * 5 * len(ks)
    for R in np.arange(0.10, 1.52, 0.02):
        R = round(float(R), 2)
        net, _ = run(ks, R, td, mode)
        if net.mean() >= 0.20 * cap:
            return R, net.mean()
    return None, None

def main():
    print("net/yr after 25% tax, mean yrs 2-4, $80 funded / $200 eval risk, 2:1, n=600 seed 11; % = of 50K x accounts nominal")
    block("A. model R is BEFORE costs (economist default: $1.30/MES RT + 0.25 pt slip on losers)")
    fm.COMM_RT, fm.SLIP_PTS = 0.0, 0.0
    block("B. model R is AFTER costs (commission and slippage set to 0 in the simulator; use for backtest net R)")
    print("\n##### R needed for 20% of nominal (grid 0.02), costs-in-R view (B)")
    for name, ks in list(FLEETS.items())[:2]:
        for mode in ("base", "exit3"):
            for td in (3, 1):
                R, v = r_needed(ks, td, mode)
                print(f"  {name:34} {mode:5} {td}/day: " + (f"R {R:+.2f} net {v:,.0f}" if R else "none up to +1.50R"))

if __name__ == "__main__":
    main()
