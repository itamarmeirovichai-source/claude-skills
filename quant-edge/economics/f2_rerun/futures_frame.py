"""Futures-firm frame, FIRST PASS ONLY (task 3 of briefs/F-economist-f2-12.md).

Runs the UNMODIFIED inherited D1 model in ./w1-prop (prop_model.py, firms.py,
parameters fetched 2026-10-11) in two frames:

A. Trade-level frame (the Apex-era `simulate`: 1:2 reward/risk, trailing
   drawdown that locks at start+$100, 30-day evaluation clock, payout ladder,
   50% consistency, MES contracts at $1.30 round trip + 0.25 pt slippage on
   stopped exits). 20 copy-traded slots onboarded one a month; evaluation sized
   at 10% of the drawdown, funded account at 4% (the inherited recommendation).
   Grid over R per trade x trades per day for plans 50K-2026 ($2,000 drawdown,
   the size Topstep / MyFundedFutures / Lucid use), 150K and legacy 50K
   ($2,500). Steady state = years 3-5 of a 5-year run (all 20 slots are on
   after month 20). Tax applied after the run at 0 / 25 / 47 / 53 %, so one
   simulation serves every tax reading. "20% of nominal" = mean steady-state
   net per year / (slots x account size) >= 0.20.
B. Daily Sharpe/vol frame (D1 `economics`, t5 shocks, 4 checks a day) for
   the five bot-allowed futures programs in firms.py, S in {1,1.5,2,3,4,6},
   sigma grid <= 20%, read at vol caps 12% and 20%; 20% of nominal = $10k per
   50K slot-year.

Also prints, for every trade-level cell, the annual Sharpe the cell implies
(i.i.d. trades, costs as modelled), to tie this frame to the FTMO table.
Writes futures_frame.json. No market data is read.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "w1-prop"))

import prop_model as PM  # noqa: E402
from firms import FIRMS  # noqa: E402
from prop_model import (COMM_RT, MES_PT, PLANS, SIGMAS, SLIP_PTS, STOP_PTS,  # noqa: E402
                        economics, simulate)

OUT = HERE / "futures_frame.json"
TAXES = (0.0, 0.25, 0.47, 0.53)
TPDS = (1, 2, 3, 5)
R_GRID = [round(x, 3) for x in np.arange(0.05, 1.001, 0.05)]
FUT_FIRMS = ["Topstep XFA 50K", "Bulenox Master 50K", "Lucid Flex 50K",
             "Tradeify Select 50K", "MFFU Rapid EOD 50K"]
S_LIST = [1.0, 1.5, 2.0, 3.0, 4.0, 6.0]


def sharpe_equiv(plan, avg_R, tpd, risk_pct=0.04, rr=2.0, days=250):
    """Annual Sharpe and vol implied by i.i.d. trades with the model's payoff
    and cost conventions (funded sizing)."""
    P = PLANS[plan]
    risk = risk_pct * P["dd"]
    k = max(1, round(risk / (STOP_PTS * MES_PT)))
    comm, slip = k * COMM_RT, k * SLIP_PTS * MES_PT
    p = (avg_R + 1.0) / (rr + 1.0)
    win, loss = rr * risk - comm, -risk - comm - slip
    m = p * win + (1 - p) * loss
    v = p * win ** 2 + (1 - p) * loss ** 2 - m ** 2
    mg = avg_R * risk
    vg = p * (rr * risk) ** 2 + (1 - p) * risk ** 2 - mg ** 2
    sd_day = np.sqrt(tpd * v)
    return dict(S_net=float(tpd * m / sd_day * np.sqrt(days)) if sd_day > 0 else float("nan"),
                S_gross=float(tpd * mg / np.sqrt(tpd * vg) * np.sqrt(days)) if vg > 0 else float("nan"),
                vol_pct_nominal=float(sd_day * np.sqrt(days) / P["start"]),
                vol_pct_dd=float(sd_day * np.sqrt(days) / P["dd"]),
                cost_R=float((comm + (1 - p) * slip) / risk), contracts=int(k), risk_usd=float(risk))


def trade_cell(plan, avg_R, tpd, n=400, years=5, slots=20, seed=11, risk_pct=0.04, risk_pct_eval=0.10):
    PM.TRADES_DAY = tpd                       # read by simulate() at call time
    w0, c0 = time.time(), time.process_time()
    d = simulate(plan=plan, slots=slots, avg_R=avg_R, risk_pct=risk_pct, years=years, n=n,
                 seed=seed, tax=0.0, risk_pct_eval=risk_pct_eval)
    pre = d["net_year"]                       # tax=0: gross - fees, (n, years)
    ss = pre[:, 2:]                           # steady state: years 3..years
    nominal = slots * PLANS[plan]["start"]
    res = dict(plan=plan, avg_R=avg_R, tpd=tpd, n=n, years=years, slots=slots, nominal=nominal,
               dd=PLANS[plan]["dd"], risk_usd=float(d["risk"]), contracts=int(d["k"]),
               risk_eval_usd=float(d["risk_e"]), contracts_eval=int(d["ke"]),
               burned_per_slot_yr=float(d["burned"].mean() / years / slots),
               evals_per_slot_yr=float(d["attempts"].mean() / years / slots),
               gross_ss_per_slot_yr=float(d["gross"][:, 2:].mean() / slots),
               fees_ss_per_slot_yr=float(d["fees"][:, 2:].mean() / slots),
               cpu_s=time.process_time() - c0, wall_s=time.time() - w0)
    for tax in TAXES:
        taxed = np.where(ss > 0, ss * (1 - tax), ss)
        per_year = taxed.mean(1)
        t = int(round(tax * 100))
        res[f"pct_nominal_tax{t}"] = float(per_year.mean() / nominal)
        res[f"p10_pct_nominal_tax{t}"] = float(np.percentile(per_year, 10) / nominal)
        res[f"se_pct_nominal_tax{t}"] = float(per_year.std(ddof=1) / np.sqrt(len(per_year)) / nominal)
    res["equiv"] = sharpe_equiv(plan, avg_R, tpd, risk_pct)
    return res


def crossing(xs, ys, target=0.20):
    if ys[0] >= target:
        return f"<= {xs[0]:.2f}"
    for (x0, y0), (x1, y1) in zip(zip(xs, ys), zip(xs[1:], ys[1:])):
        if y0 < target <= y1:
            return f"{x0 + (target - y0) / (y1 - y0) * (x1 - x0):.3f}"
    return f"> {xs[-1]:.2f}"


def daily_cell(name, S, n=2000, sigmax=0.20):
    F = FIRMS[name]
    sig = SIGMAS[SIGMAS <= sigmax + 1e-9]
    w0, c0 = time.time(), time.process_time()
    e = economics(F, S, n=n, sigmas=sig)      # D1 defaults: seeds 11/12, t5, sub 4
    caps = {}
    for cap in (0.12, 0.20):
        m = sig <= cap + 1e-9
        sub = np.where(m[:, None] & m[None, :], e["grid"], -np.inf)
        i, j = np.unravel_index(np.argmax(sub), sub.shape)
        caps[f"{cap:.2f}"] = dict(net=float(sub[i, j]), sig_e=float(sig[i]), sig_f=float(sig[j]),
                                  pct_nominal=float(sub[i, j] / F["start"]))
    return dict(firm=name, S=S, n=n, caps=caps, p_pass=float(e["p_pass"]), t_eval=float(e["t_eval"]),
                life=float(e["life"]), pay=float(e["pay"]), net_yr=float(e["net_yr"]),
                sig_e=float(e["sig_e"]), sig_f=float(e["sig_f"]), fees_yr=float(e["fees_yr"]),
                cpu_s=time.process_time() - c0, wall_s=time.time() - w0)


def main():
    t0, c0 = time.time(), time.process_time()
    out = dict(trade={}, daily={}, thresholds={}, daily_need={})
    # ---- A. trade-level frame
    for plan in ("50K-2026", "150K", "50K"):
        tpds = TPDS if plan != "50K" else (3,)
        for tpd in tpds:
            rows = []
            for R in R_GRID:
                r = trade_cell(plan, R, tpd)
                rows.append(r)
                print(f"trade {plan} tpd={tpd} R={R:+.2f}: pct nominal pre-tax {r['pct_nominal_tax0']*100:5.1f}% "
                      f"| 25% {r['pct_nominal_tax25']*100:5.1f}% | 47% {r['pct_nominal_tax47']*100:5.1f}% "
                      f"| S_eq {r['equiv']['S_net']:.2f} | burn/slot-yr {r['burned_per_slot_yr']:.1f} "
                      f"| {r['cpu_s']:.1f}s", flush=True)
                if r["pct_nominal_tax0"] > 0.60:      # far past every threshold: stop the grid here
                    break
            out["trade"][f"{plan}|{tpd}"] = rows
            xs = [r["avg_R"] for r in rows]
            th = {}
            for tax in TAXES:
                t = int(round(tax * 100))
                th[f"tax{t}"] = crossing(xs, [r[f"pct_nominal_tax{t}"] for r in rows])
            out["thresholds"][f"{plan}|{tpd}"] = th
            print(f"THRESHOLD {plan} tpd={tpd}: R for 20% of nominal: " +
                  ", ".join(f"{k} {v}" for k, v in th.items()), flush=True)
            OUT.write_text(json.dumps(out, indent=1))
    # ---- B. daily Sharpe/vol frame for futures firms
    for name in FUT_FIRMS:
        rows = []
        for S in S_LIST:
            r = daily_cell(name, S)
            rows.append(r)
            print(f"daily {name} S={S}: cap12 {r['caps']['0.12']['net']:,.0f} "
                  f"({r['caps']['0.12']['pct_nominal']*100:.1f}% of nominal) | cap20 "
                  f"{r['caps']['0.20']['net']:,.0f} ({r['caps']['0.20']['pct_nominal']*100:.1f}%) "
                  f"| pass {r['p_pass']:.2f} life {r['life']:.0f} | {r['cpu_s']:.1f}s", flush=True)
        out["daily"][name] = rows
        need = {}
        for cap in ("0.12", "0.20"):
            need[cap] = crossing([r["S"] for r in rows], [r["caps"][cap]["pct_nominal"] for r in rows])
        out["daily_need"][name] = need
        print(f"NEED {name}: S for 20% of nominal at cap 12% {need['0.12']}, cap 20% {need['0.20']}", flush=True)
        OUT.write_text(json.dumps(out, indent=1))
    out["meta"] = dict(cpu_s=time.process_time() - c0, wall_s=time.time() - t0)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"futures_frame done: cpu {out['meta']['cpu_s']/60:.1f} min wall {out['meta']['wall_s']/60:.1f} min",
          flush=True)


if __name__ == "__main__":
    main()
