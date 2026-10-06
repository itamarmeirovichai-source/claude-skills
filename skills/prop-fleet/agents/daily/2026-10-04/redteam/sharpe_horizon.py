"""Red team 2026-10-04: does the 'required Sharpe ~3' survive when the
evaluation has no 21-day clock? Reuses stack_backtest.required_sharpe_table
unchanged except for horizon (all candidate firms report no eval max time,
see ../rules_matrix.csv). Synthetic normal i.i.d. strategy, target $3,000,
trailing DD $2,000, same function as references/stack.md section 3."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / "scripts"))
from stack_backtest import required_sharpe_table
for h in (21, 63, 252):
    t = required_sharpe_table(daily_vol_usd=(100, 150, 300, 500),
                              sharpes=(0.5, 1.0, 2.0, 3.0), horizon=h, n=2000)
    print(f"horizon {h} trading days: pass/blown/median_days_to_pass")
    for (sr, dv), r in t.items():
        print(f"  SR {sr:3.1f} vol${dv:3d}: pass {r['pass_rate']*100:5.1f}%  blown {r['blowup_rate']*100:5.1f}%  median_days {r['median_days_to_pass']}")
