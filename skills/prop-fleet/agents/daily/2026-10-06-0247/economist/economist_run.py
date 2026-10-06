"""Economist, 2026-10-06. Net yearly income of a 20-account fleet split over the firms
the board lists, at +0.10R / +0.25R / +0.40R per trade (2:1), plus the board's
2026-10-05 economist tasks (cost_in_R view, P1 at 0.12/0.3/1/3 trades/day, exit band
after 1..6 payouts for Bulenox and Topstep, Bulenox $1,100 DLL, funded-risk grid
$60-$160 on P1).

CONDITIONAL ON AN EDGE WE DO NOT HAVE. Nothing here is an edge claim. No firm page
could be fetched (every firm host EGRESS_BLOCKED, rules_keeper/host_probe.txt today);
"firm snippet" = a domain-restricted search summary, not a fetched page.

Simulator: ./fleet_model.py, a COPY of daily/2026-10-05/economist/fleet_model.py
(itself a copy chain from scripts/apex_model.py, which is untouched; checks() proves
the copy reproduces it on Apex 50K-2026 and reproduces yesterday's copy).

Which 20: every listed non-Apex firm caps funded accounts at 5 (Bulenox, Topstep, Lucid,
Tradeify: firm snippets, rules_keeper/rules_matrix.csv 2026-10-06) and MFFU allows at
most 3 Rapid EOD 50K (firm snippet) with no sourced fee/target for that plan (its Flex
plan, modelled on 10-04, is Legacy). So the only 20 from listed firms is
Bulenox 5 + Topstep 5 + Lucid 5 + Tradeify 5. Lucid and Tradeify are ON HOLD on the
board; Tradeify's own text says running the same bot at other firms is against policy,
so this 20 breaks a firm rule as written. P1 (Bulenox 5 + Topstep 5) is the board's
planning fleet and is reported beside it.
"""
import sys, os, copy
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../../scripts"))
import fleet_model as fm                       # today's copy
import apex_model as am                        # original, untouched
import importlib.util
_s = importlib.util.spec_from_file_location("fm_1005", os.path.join(HERE, "../../2026-10-05/economist/fleet_model.py"))
fm_prev = importlib.util.module_from_spec(_s); _s.loader.exec_module(fm_prev)

# Tags: FS = firm snippet (domain-restricted search summary; firm hosts blocked)
#       TP = third-party site only;  A = ASSUMED, no source
FIRM_PLANS = {
  "Bulenox": dict(name="Bulenox 50K Master", start=50_000., dd=2_500., dd_mode="eod",   # dd EOD: FS accounts-pricing
       target=3_000.,                 # FS (economist search 10-05; not re-checked today)
       qmin=0., evalfee=175., activation=148.,   # FS 10-05 (board-confirmed correction)
       eval_days=None,                # FS no min/max days
       payout="frac", frac=1.0, keep_off=2_600.,   # keep_off A
       cap_first=1_500., n_cap_first=3,          # FS $1,500 max withdrawal 50K Master
       cap=1e9,                       # TP "uncapped after 3 payouts"
       min_payout=1_000., cycle_days=10, consist=0.40,   # TP (tradingfinder, quantvps)
       qual_days=0, split=0.90, split_full_until=10_000.,  # FS first $10K 100% then 90/10
       lock_off=100.,                 # A
       fixed_year=1_200.,             # FS +$100/mo Rithmic API; per firm = A (per account unknown)
       dll=1_100.),                   # FS for Qualification EOD option; applied to Master = A
  "Topstep": dict(name="Topstep 50K XFA", start=50_000., dd=2_000., dd_mode="eod",      # FS 8284204
       target=3_000.,                 # UNSOURCED in 10-05 file (carried); unverified
       qmin=150., qual_days=5,        # FS 5 winning days >= $150 (10-05)
       evalfee=49., eval_monthly=True, activation=149.,  # FS 9208217 (10-05)
       eval_days=None,                # FS no time limit
       payout="frac", frac=0.5, cap=2_000.,   # FS 8284233 Standard
       min_payout=125.,               # TP
       consist=None, split=0.90,      # split TP
       lock_off=0., floor_after_payout=0.,    # FS MLL locks at start, $0 after 1st payout
       fixed_year=348.),              # FS API $29/mo (verified 10-06); per firm = A
  "Lucid": dict(name="LucidFlex 50K", start=50_000., dd=2_000., dd_mode="eod",          # FS 12945815
       target=3_000.,                 # FS 12945790 (TP says $2,000: conflict)
       qmin=150.,                     # A
       evalfee=140., activation=0.,   # TP
       eval_days=None,                # FS (upgraded 10-06)
       payout="frac", frac=0.5, cap=2_000., max_payouts=5,   # FS 12945796
       min_payout=500., qual_days=5, consist=None, split=0.90,  # TP
       lock_off=100.),                # FS locks $50,100
  "Tradeify": dict(name="Tradeify Select Flex", start=50_000., dd=2_000., dd_mode="eod",  # FS 12853921
       target=3_000.,                 # UNSOURCED in 10-05 file (carried); unverified
       qmin=150., qual_days=5,        # FS 5 winning days >= $150
       evalfee=107., activation=0.,   # FS-ish (another source $111) / FS 10468246
       eval_days=None,                # FS
       payout="frac", frac=0.5, cap=2_500., cycle_positive=True,   # FS 12853966
       min_payout=250.,               # A
       consist=None, split=0.90,      # TP
       lock_off=100.),                # FS locks $52,100
}
FLEET20 = {"Bulenox": 5, "Topstep": 5, "Lucid": 5, "Tradeify": 5}
P1 = {"Bulenox": 5, "Topstep": 5}
RS = (0.10, 0.25, 0.40)
RISK_F, RISK_E = 80., 200.          # board 2026-10-04/05 equal-$ sizing
BASE = dict(years=4, n=600, seed=11, tax=0.25)
SS = slice(1, 4)                     # steady state: mean of years 2-4


def kw_for(P, risk_f=RISK_F, risk_e=RISK_E, **over):
    k = dict(BASE, risk_pct=risk_f / P["dd"], risk_pct_eval=risk_e / P["dd"])
    k.update(over); return k


def checks():
    a = am.simulate("50K-2026", slots=4, avg_R=0.25, years=2, n=200, seed=3, risk_pct_eval=0.10)
    b = fm.simulate("50K-2026", slots=4, avg_R=0.25, years=2, n=200, seed=3, risk_pct_eval=0.10)
    assert np.array_equal(a["net_year"], b["net_year"]), "copy diverged from apex_model"
    for key, P in FIRM_PLANS.items():
        Q = {k: v for k, v in P.items() if k != "dll"}
        x = fm_prev.simulate(Q, slots=3, avg_R=0.25, years=2, n=100, seed=5, risk_pct=0.04, risk_pct_eval=0.10)
        y = fm.simulate(Q, slots=3, avg_R=0.25, years=2, n=100, seed=5, risk_pct=0.04, risk_pct_eval=0.10)
        assert np.array_equal(x["net_year"], y["net_year"]), key
    print("checks: copy == scripts/apex_model.py (50K-2026) and == 2026-10-05 fleet_model on all 4 plans: OK")


def firm(key, R, slots, P=None, td=3, cost_in_R=True, risk_f=RISK_F, seed=None):
    P = P or FIRM_PLANS[key]
    over = dict(trades_day=td, cost_in_R=cost_in_R)
    if seed is not None: over["seed"] = seed
    return fm.simulate(P, slots=slots, avg_R=R, **kw_for(P, risk_f=risk_f, **over))


def fleet(fl, R, td, cost_in_R=True, mod=None, risk_f=RISK_F, seed=None):
    tot = 0; rows = []
    for key, s in fl.items():
        P = FIRM_PLANS[key]
        if mod: P = mod(key, copy.deepcopy(P))
        d = firm(key, R, s, P=P, td=td, cost_in_R=cost_in_R, risk_f=risk_f, seed=seed)
        ny = d["net_year"][:, SS].mean(axis=1); tot = tot + ny
        rows.append((P["name"], s, d["gross"][:, SS].mean(), d["fees"][:, SS].mean(), ny, d["burned"].mean() / 4))
    return tot, rows


def cap_of(fl):
    return 50_000. * sum(fl.values())


def table(fl, R, td, cost_in_R, label):
    tot, rows = fleet(fl, R, td, cost_in_R)
    view = "B: R after costs" if cost_in_R else "A: R before costs"
    print(f"\n=== {label}  {R:+.2f}R  {td} trade/day  ({view}) ===")
    print(f"{'firm':22} {'n':>2} {'gross/yr':>10} {'fees/yr':>9} {'net/yr':>10} {'p10':>9} {'blown/yr':>8}")
    for name, s, g, f, ny, b in rows:
        print(f"{name:22} {s:>2} {g:>10,.0f} {f:>9,.0f} {ny.mean():>10,.0f} {np.percentile(ny,10):>9,.0f} {b:>8.1f}")
    C = cap_of(fl)
    print(f"{'FLEET':22} {sum(fl.values()):>2} {'':>10} {'':>9} {tot.mean():>10,.0f} {np.percentile(tot,10):>9,.0f}"
          f"   = {100*tot.mean()/C:.1f}% of ${C/1e3:,.0f}K nominal (p90 {np.percentile(tot,90):,.0f})")
    return tot


def r_needed(fl, td, mod=None, hi=1.50):
    C = cap_of(fl)
    for R in np.arange(0.10, hi + 1e-9, 0.02):
        R = round(float(R), 2)
        tot, _ = fleet(fl, R, td, True, mod)
        if tot.mean() >= 0.20 * C:
            return R, tot.mean()
    return None, None


def exit_mod(k):
    def m(key, P):
        if key == "Bulenox": P["max_payouts"] = k          # each Master leaves after k payouts; slot re-buys (A)
        if key == "Topstep": P["firm_exit_payouts"] = k     # call-up after k-th payout closes ALL XFAs (A on k)
        return P
    return m


def main():
    checks()
    print("\nAll $ are net after 25% tax, mean of years 2-4, n=600 paths seed 11, 2:1 win/loss, "
          "$80 funded / $200 eval risk per trade, perfectly correlated copies, 1 new account per firm per month.")

    print("\n################ 1. The asked 20-account fleet (Bulenox5 + Topstep5 + Lucid5 + Tradeify5)")
    res20 = {}
    for cost_in_R in (True, False):
        for td in (3, 1, 0.3):
            for R in RS:
                res20[(cost_in_R, td, R)] = table(FLEET20, R, td, cost_in_R, "FLEET-20")

    print("\n=== summary FLEET-20 (net/yr; % of $1,000K nominal) ===")
    for cost_in_R in (True, False):
        v = "B (R after costs)" if cost_in_R else "A (R before costs)"
        for td in (3, 1, 0.3):
            print(f"  {v:20} {td:>4}/day | " + " | ".join(
                f"{R:+.2f}R {res20[(cost_in_R, td, R)].mean():>9,.0f} ({100*res20[(cost_in_R, td, R)].mean()/1e6:5.1f}%)" for R in RS))

    print("\n=== check vs 2026-10-05 economist_run.txt (view A, 3/day): expected 25,378 / 126,427 / 247,924 ===")
    print("  today: " + " / ".join(f"{res20[(False, 3, R)].mean():,.0f}" for R in RS))

    print("\n=== Monte Carlo error: FLEET-20 view B, seed 12 vs seed 11 ===")
    for td in (3, 1, 0.3):
        print(f"  {td:>4}/day | " + " | ".join(
            f"{R:+.2f}R s11 {res20[(True, td, R)].mean():>9,.0f} s12 {fleet(FLEET20, R, td, True, seed=12)[0].mean():>9,.0f}" for R in RS))

    print("\n################ 2. P1 planning fleet (Bulenox5 + Topstep5), view B")
    for td in (3, 1, 0.3, 0.12):
        cells = []
        for R in RS:
            t, _ = fleet(P1, R, td)
            cells.append(f"{R:+.2f}R {t.mean():>9,.0f} ({100*t.mean()/5e5:5.1f}%, p10 {np.percentile(t,10):>8,.0f})")
        print(f"  P1 {td:>4}/day | " + " | ".join(cells))

    print("\n=== R per trade (after costs) needed for 20% of nominal, grid 0.02 up to +1.50R ===")
    for name, fl in (("FLEET-20", FLEET20), ("P1", P1)):
        for td in (3, 1, 0.3, 0.12):
            R, v = r_needed(fl, td)
            print(f"  {name:8} {td:>4}/day: " + (f"R {R:+.2f} (net {v:,.0f})" if R else "none up to +1.50R"))

    print("\n################ 3. Exit band: Bulenox Master leaves after k payouts (slot re-buys);"
          " Topstep call-up after the k-th payout of any XFA closes all 5 for good. View B.")
    for name, fl in (("FLEET-20", FLEET20), ("P1", P1)):
        for td in (3, 1):
            print(f"  {name} {td}/day")
            for k in (None, 1, 2, 3, 4, 5, 6):
                mod = exit_mod(k) if k else None
                cells = []
                for R in RS:
                    t, _ = fleet(fl, R, td, True, mod)
                    cells.append(f"{R:+.2f}R {t.mean():>9,.0f} ({100*t.mean()/cap_of(fl):5.1f}%)")
                print(f"    exit {('none' if k is None else k):>4} | " + " | ".join(cells))
    print("  R needed for 20%, P1, exit after 3:")
    for td in (3, 1):
        R, v = r_needed(P1, td, exit_mod(3))
        print(f"    P1 exit3 {td}/day: " + (f"R {R:+.2f} (net {v:,.0f})" if R else "none up to +1.50R"))

    print("\n################ 4. Bulenox $1,100 DLL: with vs without (Bulenox 5 alone, view B)")
    nodll = lambda key, P: {k: v for k, v in P.items() if k != "dll"}
    for rf in (80., 160., 400.):
        for td in (3, 1):
            cells = []
            for R in RS:
                a, _ = fleet({"Bulenox": 5}, R, td, True, risk_f=rf)
                b, _ = fleet({"Bulenox": 5}, R, td, True, nodll, risk_f=rf)
                cells.append(f"{R:+.2f}R dll {a.mean():>8,.0f} none {b.mean():>8,.0f}")
            print(f"  funded risk ${rf:.0f} {td}/day | " + " | ".join(cells))

    print("\n################ 5. Funded-risk grid on P1 (eval risk stays $200), view B")
    for td in (3, 1):
        print(f"  P1 {td}/day")
        for rf in (60., 80., 100., 120., 140., 160.):
            cells = []
            for R in RS:
                t, rows = fleet(P1, R, td, True, risk_f=rf)
                bl = sum(r[5] for r in rows)
                cells.append(f"{R:+.2f}R {t.mean():>9,.0f} (p10 {np.percentile(t,10):>8,.0f}, blown {bl:4.1f}/yr)")
            print(f"    ${rf:>4.0f} | " + " | ".join(cells))

    print("\n################ 6. Topstep option: voluntary DLL doubles XFA cap to $4,000 (FS 8284233);"
          " DLL size unknown, so only the cap is changed (upper bound). P1 view B")
    def ts4000(key, P):
        if key == "Topstep": P["cap"] = 4_000.
        return P
    for td in (3, 1):
        print(f"  P1 {td}/day | " + " | ".join(
            f"{R:+.2f}R cap2000 {fleet(P1, R, td)[0].mean():>9,.0f} cap4000 {fleet(P1, R, td, True, ts4000)[0].mean():>9,.0f}" for R in RS))


if __name__ == "__main__":
    main()
