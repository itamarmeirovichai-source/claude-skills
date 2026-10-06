"""Economist, 2026-10-04: 20-account fleet, 4 x 50K at each of the five firms the
board lists, at +0.10R / +0.25R / +0.40R. Every plan number is cited in
FIRM_PLANS below; ASSUMED means no source was found and the value is a guess.
Same seed for every firm -> identical trade sequence -> the fleet is fully
copy-trade correlated, as in the original model."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../scripts"))
import fleet_model as fm
import apex_model as am

FIRM_PLANS = {
  # MFFU Flex 50K. dd/EOD: help.myfundedfutures.com/.../14290805 (rules_matrix verified)
  # price $107 list, no activation fee since Jul 2025, target $3,000: fundedtrading.com (search)
  # payout 50% of profit, 5 days >= $150, 80/20: propfirmsfinder/h2tfunding (search)
  # cap $2,000/request: help-center snippet (rules_matrix)
  "MFFU": dict(name="MFFU Flex 50K", start=50_000., dd=2_000., dd_mode="eod",
       target=3_000., qmin=150., evalfee=107., activation=0., eval_days=None,
       payout="frac", frac=0.5, cap=2_000., min_payout=250.,   # min ASSUMED
       qual_days=5, consist=None, split=0.80, lock_off=100.),    # lock_off, consist ASSUMED
  # Bulenox Master 50K Option 1 (EOD). dd $2,500: bulenox.com (rules_matrix)
  # $115 fee + $98 activation, split 90%, 40% consistency: thedesk.onrender.com (search)
  # (thegodfunded.com says recurring eval subscriptions were removed -> charged once per attempt)
  # $1,500 first 3 payouts then uncapped, min $1,000, 10 trading days, 100% of first $10k:
  #   tradingfinder.com / quantvps.com (rules_matrix, corroborated)
  # +$100/month Rithmic API: bulenox.com FAQ (rules_matrix)
  "Bulenox": dict(name="Bulenox 50K", start=50_000., dd=2_500., dd_mode="eod",
       target=3_000., qmin=0., evalfee=115., activation=98., eval_days=None,
       payout="frac", frac=1.0, keep_off=2_600.,                # keep_off ASSUMED (Apex-style buffer)
       cap_first=1_500., n_cap_first=3, cap=1e9, min_payout=1_000., cycle_days=10,
       qual_days=0, consist=0.40, split=0.90, split_full_until=10_000.,
       lock_off=100., fixed_year=1_200.),                      # lock_off ASSUMED
  # Tradeify Select 50K. dd $2,000 EOD, 5 funded: help.tradeify.co (rules_matrix)
  # $109 one-time, target $3,000, no activation, 90/10: blog.traderspost.io (search)
  # Select Daily $1,000 per cycle: tradetanto.com (rules_matrix)
  "Tradeify": dict(name="Tradeify Select 50K", start=50_000., dd=2_000., dd_mode="eod",
       target=3_000., qmin=150., evalfee=109., activation=0., eval_days=None,
       payout="frac", frac=0.5, cap=1_000., min_payout=250.,   # frac, min ASSUMED
       qual_days=5, consist=None, split=0.90, lock_off=100.),    # qual rule ASSUMED
  # Lucid Flex 50K. $140, target $3,000, $2,000 EOD MLL, 90%, no funded consistency:
  #   proptradingvibes.com / tradingfunder.com (search)
  # $2,000/request, 50% of balance, min $500, 5 payouts then live review:
  #   proptradingvibes.com (rules_matrix). After 5 the model closes and replaces the account.
  "Lucid": dict(name="LucidFlex 50K", start=50_000., dd=2_000., dd_mode="eod",
       target=3_000., qmin=150., evalfee=140., activation=0., eval_days=None,  # activation ASSUMED 0
       payout="frac", frac=0.5, cap=2_000., min_payout=500., max_payouts=5,
       qual_days=5, consist=None, split=0.90, lock_off=100.),    # qual rule, lock_off ASSUMED
  # Topstep 50K Standard path. $2,000 MLL trailing, locks at start; no time limit,
  # rebills every 30 days; 50% up to $5,000, 5 days >= $150: help.topstep.com (rules_matrix)
  # $49/month, $149 activation, 90/10, min $125: blog.traderspost.io (search)
  # API $29/month: blog.pickmytrade.io (rules_matrix, third party)
  "Topstep": dict(name="Topstep 50K", start=50_000., dd=2_000., dd_mode="eod",  # EOD ASSUMED
       target=3_000., qmin=150., evalfee=49., eval_monthly=True, activation=149.,
       eval_days=None, payout="frac", frac=0.5, cap=5_000., min_payout=125.,
       qual_days=5, consist=None, split=0.90, lock_off=0., fixed_year=348.),
}

KW = dict(years=4, n=600, seed=11, risk_pct=0.04, risk_pct_eval=0.10, tax=0.25)
SS = slice(1, 4)            # steady state: years 2-4 (4 slots fully onboarded by month 4)
CAPITAL = 20 * 50_000.

def check_reproduces_original():
    a = am.simulate("50K-2026", slots=4, avg_R=0.25, years=2, n=200, seed=3, risk_pct_eval=0.10)
    b = fm.simulate("50K-2026", slots=4, avg_R=0.25, years=2, n=200, seed=3, risk_pct_eval=0.10)
    assert np.array_equal(a["net_year"], b["net_year"]), "copy diverged from original"
    print("copy reproduces original apex_model on 50K-2026: OK")

def main():
    check_reproduces_original()
    for R in (0.10, 0.25, 0.40):
        print(f"\n=== expectancy {R:+.2f}R, 4 accounts per firm, net after 25% tax, mean of years 2-4 ===")
        print(f"{'firm':22} {'gross/yr':>10} {'fees/yr':>9} {'net/yr':>10} {'dead/yr':>9} {'evals/yr':>8}")
        tot = 0
        for key, P in FIRM_PLANS.items():
            d = fm.simulate(P, slots=4, avg_R=R, **KW)
            ny = d["net_year"][:, SS].mean(axis=1)
            tot = tot + d["net_year"][:, SS].mean(axis=1)
            print(f"{P['name']:22} {d['gross'][:, SS].mean():>10,.0f} {d['fees'][:, SS].mean():>9,.0f} "
                  f"{ny.mean():>10,.0f} {d['burned'].mean()/4:>9.1f} {d['attempts'].mean()/4:>8.1f}")
        print(f"{'FLEET 20 accounts':22} {'':>10} {'':>9} {tot.mean():>10,.0f}  "
              f"= {100*tot.mean()/CAPITAL:.1f}% of $1M nominal; p10 {np.percentile(tot,10):,.0f} "
              f"p90 {np.percentile(tot,90):,.0f}")
        ap = am.simulate("50K-2026", slots=20, avg_R=R, **KW)
        print(f"{'ref: Apex 50K-2026 x20':22} {'':>10} {'':>9} {ap['net_year'][:, SS].mean():>10,.0f}"
              f"  (excluded: bans automation)")

if __name__ == "__main__":
    main()
