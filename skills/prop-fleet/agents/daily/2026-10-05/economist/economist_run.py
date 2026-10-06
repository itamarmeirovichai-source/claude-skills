"""Economist, 2026-10-05. 20-account fleet over the firms the board lists:
Bulenox 5 + Lucid 5 (Tier A) + Topstep Express 5 (Tier B) + Tradeify 5 (on hold;
the only listed firm whose verified 50K cap allows 5 funded and whose payout
rules are verified). Expectancy +0.10R / +0.25R / +0.40R, 2:1, 3 trades/day and
1 trade/day.

CONDITIONAL ON AN EDGE WE DO NOT HAVE. Nothing here is an edge claim.

Inputs: every plan number carries a tag:
  V   = firm help-center snippet via domain-restricted WebSearch (rules_keeper
        2026-10-05 rules_matrix.csv, or today's economist search)  -- still a
        search summary, not a fetched page; firm pages are EGRESS_BLOCKED
  C   = third-party site only (corroborated)
  A   = ASSUMED, no source found
Model constants (commission $1.30/MES RT, 0.25 pt slippage on stops, 8.5 pt
stop, 250 days/yr, 21 days/month, 25% tax, one new account per month, perfect
copy correlation) come from scripts/apex_model.py and are ASSUMED (A).
"""
import sys, os, copy
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../../scripts"))
import fleet_model as fm                       # today's copy
import apex_model as am                        # original, untouched
import importlib.util
_s = importlib.util.spec_from_file_location("fm_prev", os.path.join(HERE, "../../2026-10-04/fleet_model.py"))
fm_prev = importlib.util.module_from_spec(_s); _s.loader.exec_module(fm_prev)
_e = importlib.util.spec_from_file_location("er_prev", os.path.join(HERE, "../../2026-10-04/economist_run.py"))
er_prev = importlib.util.module_from_spec(_e); _e.loader.exec_module(er_prev)
PLANS_1004 = er_prev.FIRM_PLANS                     # yesterday's plans (data only)

FIRM_PLANS = {
  # Bulenox Master 50K, Qualification EOD option.
  #  dd $2,500 EOD (V bulenox.com/accounts-pricing); EOD option has $1,100 DLL (V) -- not
  #  modeled; at $80/$200 risk x3 trades the max daily loss is < $1,100 so it does not bind.
  #  target $3,000 (V bulenox.com search 2026-10-05); qualification fee $175 one-time (V same),
  #  Master activation $148 one-time (V bulenox.com/help-center/master search 2026-10-05).
  #  [2026-10-04 used $115 + $98 from thedesk.onrender.com (C) -> CHANGED]
  #  no min/max trading days (V). max withdrawal $1,500 per payout on 50K Master (V);
  #  "uncapped after 3 payouts", $1,000 min, 10 trading days, 40% consistency (C tradingfinder,
  #  quantvps); payouts processed weekly on Wednesday (V) -> cycle 10 kept (C), sensitivity below.
  #  first $10,000 100% then 90/10 (V). +$100/month 3rd-party Rithmic API (V; per account or per
  #  user UNKNOWN -> per firm here, per account in sensitivity). keep_off 2,600 (A). lock_off 100 (A).
  "Bulenox": dict(name="Bulenox 50K", start=50_000., dd=2_500., dd_mode="eod",
       target=3_000., qmin=0., evalfee=175., activation=148., eval_days=None,
       payout="frac", frac=1.0, keep_off=2_600.,
       cap_first=1_500., n_cap_first=3, cap=1e9, min_payout=1_000., cycle_days=10,
       qual_days=0, consist=0.40, split=0.90, split_full_until=10_000.,
       lock_off=100., fixed_year=1_200.),
  # LucidFlex 50K.
  #  dd $2,000 EOD, trail starts $52,100, locks $50,100 (V support 12945815) -> lock_off 100 (V).
  #  target $3,000, eval consistency 50% (V support 12945790, search 2026-10-05; one third
  #  party says $2,000 -> CONFLICT, firm text wins). eval consistency NOT modeled (A: ignored).
  #  fee $140 one-time, no activation (C proptradingvibes / daytradingz). 50% of profit up to
  #  $2,000/request, 5 payouts then live (V support 12945796). 5 qualifying days (C); $150 per
  #  day (A). min $500 (C). split 90 (C). After 5 payouts the slot is replaced (A: LucidLive
  #  automation unknown).
  "Lucid": dict(name="LucidFlex 50K", start=50_000., dd=2_000., dd_mode="eod",
       target=3_000., qmin=150., evalfee=140., activation=0., eval_days=None,
       payout="frac", frac=0.5, cap=2_000., min_payout=500., max_payouts=5,
       qual_days=5, consist=None, split=0.90, lock_off=100.),
  # Topstep 50K Standard path, Express Funded.
  #  $2,000 MLL trailing EOD, enforced real time, locks at start, set to $0 after first payout
  #  (V help.topstep 8284204) -> dd_mode eod (V, was A), lock_off 0, floor_after_payout 0.
  #  no time limit, rebills $49 every 30 days, $149 activation (V help.topstep 9208217 search
  #  2026-10-05). XFA 50K: 50% of balance up to $2,000 Standard (V 8284233)
  #  [2026-10-04 used $5,000 -> CORRECTED]. 5 winning days >= $150 (V). min $125 (C).
  #  split 90 (C). API $29/month (C pickmytrade) -> fixed_year 348.
  #  Move to Live Funded: Risk Team discretion, no payout count (V search 2026-10-05);
  #  Live has no API (V) -> base: never called up (A); sensitivity: leaves after 3 or 5 payouts (A).
  "Topstep": dict(name="Topstep 50K XFA", start=50_000., dd=2_000., dd_mode="eod",
       target=3_000., qmin=150., evalfee=49., eval_monthly=True, activation=149.,
       eval_days=None, payout="frac", frac=0.5, cap=2_000., min_payout=125.,
       qual_days=5, consist=None, split=0.90, lock_off=0., floor_after_payout=0.,
       fixed_year=348.),
  # Tradeify Select 50K, Select Flex payout.
  #  $2,000 EOD, locks $52,100 -> lock_off 100 (V 12853921/12853966). no time limit (V).
  #  eval min 3 days, 40% eval consistency (V) -- not modeled (A: ignored).
  #  fee $107 one-time (V-ish: help.tradeify/tradeify.co search 2026-10-05 "as of 15 Jul
  #  2026"; another source $111) [2026-10-04 used $109]; no activation (V 10468246).
  #  Flex: 50% of profits up to $2,500 for accounts bought after 1 Sep 2026 (V), 5 winning days
  #  >= $150 (V), no min balance (V), positive net each cycle after the first (V).
  #  [2026-10-04 used Select Daily $1,000 -> CHANGED]. min payout (A: 250). split 90 (C).
  #  'Same bot at other firms is against policy' (V) -> this firm is ON HOLD on the board.
  "Tradeify": dict(name="Tradeify Select Flex", start=50_000., dd=2_000., dd_mode="eod",
       target=3_000., qmin=150., evalfee=107., activation=0., eval_days=None,
       payout="frac", frac=0.5, cap=2_500., min_payout=250., cycle_positive=True,
       qual_days=5, consist=None, split=0.90, lock_off=100.),
}
FLEET = {"Bulenox": 5, "Lucid": 5, "Topstep": 5, "Tradeify": 5}
CAPITAL = 50_000. * sum(FLEET.values())
RS = (0.10, 0.25, 0.40)
# Board 2026-10-04: "size every firm at equal dollar risk". $80 funded / $200 eval
# = 4% / 10% of a $2,000 drawdown, the sizing of the $2,000-dd firms yesterday.
RISK_F, RISK_E = 80., 200.
BASE = dict(years=4, n=600, seed=11, tax=0.25)
SS = slice(1, 4)            # steady state: years 2-4


def kw_for(P, **over):
    k = dict(BASE, risk_pct=RISK_F / P["dd"], risk_pct_eval=RISK_E / P["dd"])
    k.update(over); return k


def checks():
    a = am.simulate("50K-2026", slots=4, avg_R=0.25, years=2, n=200, seed=3, risk_pct_eval=0.10)
    b = fm.simulate("50K-2026", slots=4, avg_R=0.25, years=2, n=200, seed=3, risk_pct_eval=0.10)
    assert np.array_equal(a["net_year"], b["net_year"]), "copy diverged from apex_model"
    for key in ("Bulenox", "Lucid", "Topstep", "Tradeify"):
        P = PLANS_1004[key]
        x = fm_prev.simulate(P, slots=3, avg_R=0.25, years=2, n=100, seed=5, risk_pct=0.04, risk_pct_eval=0.10)
        y = fm.simulate(P, slots=3, avg_R=0.25, years=2, n=100, seed=5, risk_pct=0.04, risk_pct_eval=0.10)
        assert np.array_equal(x["net_year"], y["net_year"]), key
    print("checks: today's copy == scripts/apex_model.py on 50K-2026, and == 2026-10-04 fleet_model on its 4 plans: OK")


def firm(key, R, P=None, slots=None, **over):
    P = P or FIRM_PLANS[key]
    d = fm.simulate(P, slots=slots or FLEET[key], avg_R=R, **kw_for(P, **over))
    return d


def table(R, trades_day=3, plans=None, label=""):
    plans = plans or FIRM_PLANS
    print(f"\n=== {R:+.2f}R, 2:1, {trades_day} trade(s)/day, $80 funded / $200 eval risk, "
          f"net after 25% tax, mean yrs 2-4 {label}===")
    print(f"{'firm':22} {'n':>2} {'gross/yr':>10} {'fees/yr':>9} {'net/yr':>10} {'p10':>9} {'blown/yr':>8}")
    tot = 0
    for key, P in plans.items():
        d = firm(key, R, P=P, trades_day=trades_day)
        ny = d["net_year"][:, SS].mean(axis=1); tot = tot + ny
        print(f"{P['name']:22} {FLEET[key]:>2} {d['gross'][:, SS].mean():>10,.0f} {d['fees'][:, SS].mean():>9,.0f} "
              f"{ny.mean():>10,.0f} {np.percentile(ny,10):>9,.0f} {d['burned'].mean()/4:>8.1f}")
    print(f"{'FLEET':22} {sum(FLEET.values()):>2} {'':>10} {'':>9} {tot.mean():>10,.0f} {np.percentile(tot,10):>9,.0f}"
          f"   = {100*tot.mean()/CAPITAL:.1f}% of ${CAPITAL/1e6:.0f}M nominal (p90 {np.percentile(tot,90):,.0f})")
    return tot


def r_needed(trades_day):
    for R in np.arange(0.10, 1.01, 0.02):
        R = round(float(R), 2)
        tot = sum(firm(k, R, trades_day=trades_day)["net_year"][:, SS].mean(axis=1) for k in FIRM_PLANS)
        if tot.mean() >= 0.20 * CAPITAL:
            return R, tot.mean()
    return None, None


def main():
    checks()
    res = {}
    for td in (3, 1):
        for R in RS:
            res[(td, R)] = table(R, trades_day=td)

    print("\n=== R needed for 20% of nominal ($200K/yr net), 20-acct fleet, grid step 0.02 ===")
    for td in (3, 1):
        R, v = r_needed(td)
        sr = None
        if R is not None:
            p = (R + 1) / 3; sd = np.sqrt(p * 4 + (1 - p) * 1 - R * R)
            sr = R / sd * np.sqrt(250 * td)
        print(f"  {td} trade(s)/day: first R >= 20%: {R}  (fleet net {v:,.0f}); "
              f"per-trade R sd at 2:1 -> annual Sharpe {sr:.2f}" if R else f"  {td}/day: none up to 1.0R")

    print("\n=== sensitivities at 3 trades/day (fleet net/yr) ===")
    def fleet_with(mod):
        out = []
        for R in RS:
            tot = 0
            for key, P in FIRM_PLANS.items():
                P2 = mod(key, copy.deepcopy(P))
                tot = tot + firm(key, R, P=P2)["net_year"][:, SS].mean(axis=1)
            out.append(tot.mean())
        return " | ".join(f"{R:+.2f}R {v:>9,.0f}" for R, v in zip(RS, out))
    def topstep_leave(n):
        def m(k, P):
            if k == "Topstep": P["max_payouts"] = n
            return P
        return m
    def bulenox_capped(k, P):
        if k == "Bulenox": P["cap"] = 1_500.
        return P
    def bulenox_api_per_acct(k, P):
        if k == "Bulenox": P["fixed_year"] = 0.; P["acct_month"] = 100.
        return P
    def bulenox_cycle5(k, P):
        if k == "Bulenox": P["cycle_days"] = 5
        return P
    def lucid_t2000(k, P):
        if k == "Lucid": P["target"] = 2_000.
        return P
    def acct_cost(c):
        def m(k, P):
            P["acct_month"] = P.get("acct_month", 0.) + c
            return P
        return m
    print(f"  {'base':46}", fleet_with(lambda k, P: P))
    print(f"  {'Topstep XFA leaves to Live after 5 payouts (A)':46}", fleet_with(topstep_leave(5)))
    print(f"  {'Topstep XFA leaves to Live after 3 payouts (A)':46}", fleet_with(topstep_leave(3)))
    print(f"  {'Bulenox cap stays $1,500 forever (firm text)':46}", fleet_with(bulenox_capped))
    print(f"  {'Bulenox API $100/month per account':46}", fleet_with(bulenox_api_per_acct))
    print(f"  {'Bulenox weekly payout cycle (5 days)':46}", fleet_with(bulenox_cycle5))
    print(f"  {'Lucid target $2,000 (third-party figure)':46}", fleet_with(lucid_t2000))
    print(f"  {'+$50/month per funded account, all firms (A)':46}", fleet_with(acct_cost(50.)))

    print("\n=== Tier A+B only (15 accounts, no on-hold firm), 3 trades/day ===")
    for R in RS:
        tot = sum(firm(k, R)["net_year"][:, SS].mean(axis=1) for k in ("Bulenox", "Lucid", "Topstep"))
        print(f"  {R:+.2f}R  {tot.mean():>9,.0f} = {100*tot.mean()/750_000:.1f}% of $750K nominal (p10 {np.percentile(tot,10):,.0f})")

    print("\n=== 2026-10-04 plan inputs vs today (same equal-$ risk, 3/day, 5 per firm, fleet net) ===")
    for R in RS:
        old = sum(fm.simulate(PLANS_1004[k], slots=5, avg_R=R, **kw_for(PLANS_1004[k]))["net_year"][:, SS].mean(axis=1)
                  for k in FIRM_PLANS)
        print(f"  {R:+.2f}R  yesterday's plans {old.mean():>9,.0f}   today's {res[(3, R)].mean():>9,.0f}")


if __name__ == "__main__":
    main()
