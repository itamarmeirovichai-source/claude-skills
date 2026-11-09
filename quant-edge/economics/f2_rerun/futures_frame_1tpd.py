"""Supplement to futures_frame.py: at 1 trade a day the inherited trade-level
model never pays out at 4% of drawdown on the 50K plans, because a single
winning trade (+$157 on 50K-2026, +$197 on legacy 50K) is below the plan's
$200 qualifying-day minimum (qmin), so no day ever qualifies for a payout.
This re-runs 1 and 2 trades a day with the funded account at 8% of drawdown
(two wins a day clear qmin; one win at 8% = +$317 on 50K-2026) so the 1/day
row has a number. Same frame otherwise. Writes futures_frame_1tpd.json."""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from futures_frame import R_GRID, TAXES, crossing, trade_cell  # noqa: E402

OUT = HERE / "futures_frame_1tpd.json"


def main():
    t0 = time.process_time()
    out = dict(trade={}, thresholds={})
    for plan in ("50K-2026", "150K"):
        for tpd, risk in ((1, 0.08), (2, 0.08), (3, 0.08)):
            rows = []
            for R in R_GRID:
                r = trade_cell(plan, R, tpd, risk_pct=risk)
                rows.append(r)
                print(f"trade {plan} tpd={tpd} risk={risk:.2f} R={R:+.2f}: pre-tax {r['pct_nominal_tax0']*100:5.1f}% "
                      f"| 25% {r['pct_nominal_tax25']*100:5.1f}% | 47% {r['pct_nominal_tax47']*100:5.1f}% "
                      f"| S_eq {r['equiv']['S_net']:.2f} | burn/slot-yr {r['burned_per_slot_yr']:.1f}", flush=True)
                if r["pct_nominal_tax0"] > 0.60:
                    break
            key = f"{plan}|{tpd}|risk{int(risk*100)}"
            out["trade"][key] = rows
            xs = [r["avg_R"] for r in rows]
            th = {f"tax{int(round(t*100))}": crossing(xs, [r[f"pct_nominal_tax{int(round(t*100))}"] for r in rows])
                  for t in TAXES}
            out["thresholds"][key] = th
            print(f"THRESHOLD {key}: " + ", ".join(f"{k} {v}" for k, v in th.items()), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    out["meta"] = dict(cpu_s=time.process_time() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"done cpu {out['meta']['cpu_s']/60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
