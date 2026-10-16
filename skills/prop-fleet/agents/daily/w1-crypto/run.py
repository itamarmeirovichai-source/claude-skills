"""Run all pre-registered D3 variants; write results.json and results.md."""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, __import__("os").path.dirname(__file__))
from d3lib import *

BAR = 3.5504


def build(data):
    """Returns {id: (legs, hourly)} using decision weights only."""
    S, P = data.ret, data.pret
    w1 = g_tsmom(data)
    w5 = g_xsmom(data, 28)
    w7 = g_carry(data)
    v = {
        "D3-01": ([(w1, S, C_PERP, True)], False),
        "D3-02": ([(g_tsmom(data, longflat=True), S, C_PERP, True)], False),
        "D3-03": ([(g_tsmom(data, coins=["BTC", "ETH"]), S, C_PERP, True)], False),
        "D3-04": ([(g_intraday(data), data.h_ret, C_PERP, True)], True),
        "D3-05": ([(w5, S, C_PERP, True)], False),
        "D3-06": ([(g_xsmom(data, 7), S, C_PERP, True)], False),
        "D3-07": ([(w7, P, C_PERP, True)], False),
    }
    ws, wp = g_cashcarry(data)
    v["D3-08"] = ([(ws, S, C_SPOT, False), (wp, P, C_PERP, True)], False)
    v["D3-09"] = ([(g_hour(data), data.h_ret, C_PERP, True)], True)

    def m(D, R, tgt):
        g = evaluate([(D, R, 0.0, False)], data=data).gross
        sd = g.rolling(60, min_periods=60).std() * np.sqrt(365)
        return (tgt / sd).clip(upper=3).fillna(0.0)
    m1, m5, m7 = m(w1, S, 0.10), m(w5, S, 0.10), m(w7, P, 0.10)
    v["D3-10"] = ([(w1.mul(m1, axis=0) + w5.mul(m5, axis=0), S, C_PERP, True),
                   (w7.mul(m7, axis=0), P, C_PERP, True)], False)
    v["D3-11"] = ([(w1.mul(m(w1, S, 0.20), axis=0), S, C_PERP, True)], False)
    return v


def run(data):
    res = {}
    for k, (legs, hourly) in build(data).items():
        res[k] = evaluate(legs, hourly=hourly, data=data)
    return res


if __name__ == "__main__":
    data = load(sys.argv[1])
    out = sys.argv[2] if len(sys.argv) > 2 else "."
    res = run(data)
    rows = {}
    for k, df in res.items():
        r = {}
        isr = df.loc[IS[0]:IS[1]]
        oos = df.loc[OOS[0]:OOS[1]]
        is_sd = isr.net.std()
        scale = 1.0 if k == "D3-09" or is_sd == 0 else 0.20 / (is_sd * np.sqrt(365))
        for name, x in (("IS", isr), ("OOS", oos)):
            r[name] = stats(x.net.values)
            r[name + "_x2"] = stats(x.net2.values)
            r[name + "_gross"] = stats(x.gross.values)
            r[name + "_scaled"] = stats(x.net.values * scale)
            r[name + "_turnover_per_day"] = float(x.to.mean())
            r[name + "_fund_bp"] = float(x.fund.mean() * 1e4)
            r[name + "_cost_bp"] = float(x.cost.mean() * 1e4)
        r["scale"] = scale
        r["years"] = {str(y): float(g.net.mean() * 1e4) for y, g in df.loc[IS[0]:].groupby(df.loc[IS[0]:].index.year)}
        o = r["OOS"]
        r["gate_stat"] = bool(o["mean_bp"] > 0 and o["t"] >= BAR and o["p5_bp"] > 0)
        rows[k] = r
        df.to_csv(f"{out}/daily_{k}.csv.gz", float_format="%.7g")
    json.dump(rows, open(f"{out}/results.json", "w"), indent=1, default=float)
    print(f"{'id':6} {'OOSmean':>8} {'t_iid':>6} {'t_nw':>6} {'p5':>7} {'Shrp':>5} {'x2mean':>7} {'x2t':>6} {'gross':>7} {'cost':>6} {'fund':>6} {'TO':>5} | {'ISmean':>7} {'ISt':>6} {'ISShrp':>6} | sCAGR sMDD gate")
    for k, r in rows.items():
        o, i = r["OOS"], r["IS"]
        print(f"{k:6} {o['mean_bp']:8.2f} {o['t_iid']:6.2f} {o['t_nw']:6.2f} {o['p5_bp']:7.2f} {o['sharpe']:5.2f} "
              f"{r['OOS_x2']['mean_bp']:7.2f} {r['OOS_x2']['t']:6.2f} {r['OOS_gross']['mean_bp']:7.2f} {r['OOS_cost_bp']:6.2f} "
              f"{r['OOS_fund_bp']:6.2f} {r['OOS_turnover_per_day']:5.2f} | {i['mean_bp']:7.2f} {i['t']:6.2f} {i['sharpe']:6.2f} | "
              f"{r['OOS_scaled']['cagr']:5.2f} {r['OOS_scaled']['maxdd']:5.2f} {r['gate_stat']}")
