"""G2 full run: every variant, both fills, costs 0/1x/2x/spread-only, benchmark, per-year,
5% daily-loss breaches, look-ahead tests. Writes results.csv and prints run.txt.

usage: G2_CACHE=<dir> python3 report.py [--no-lookahead]
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import meanrev as M

HERE = Path(__file__).resolve().parent


def main(do_la=True):
    data = M.load()
    for n in M.NAMES:
        df = data[n]
        print(f"{n:7s} {df.index[0].date()} -> {df.index[-1].date()}  n={len(df)}")
    res = M.run_all(data)
    rows = []
    for (v, mode), r in res.items():
        for per in ("IS", "OOS", "OOS2", "OOS0", "OOSns"):
            rows.append(dict(id=v, fill=mode, period=per, **r[per]))
    df = pd.DataFrame(rows)
    df.to_csv(HERE / "results.csv", index=False, float_format="%.5g")

    pd.set_option("display.width", 250, "display.max_columns", 40)
    print("\n== In sample (to 2012), net 1x ==")
    print(df[df.period == "IS"][["id", "fill", "sharpe", "t", "ret_yr", "vol", "trades_yr", "expo"]]
          .round(3).to_string(index=False))

    # decisive version per variant = lower OOS t
    dec = {}
    for v in M.VARIANTS:
        tc, to = res[(v, "close")]["OOS"]["t"], res[(v, "open")]["OOS"]["t"]
        dec[v] = "close" if tc <= to else "open"
    is_worse = {v: min(res[(v, m)]["IS"]["sharpe"] for m in ("close", "open")) for v in M.VARIANTS}
    head = max(is_worse, key=is_worse.get)
    print("\nIS net Sharpe (worse fill):", {k: round(x, 3) for k, x in is_worse.items()})
    print("HEADLINE (highest IS net Sharpe, worse fill):", head)

    print("\n== Out of sample 2013-2026, both fills ==")
    cols = ["id", "fill", "period", "sharpe", "t", "p5_bp", "alpha_t", "beta", "resid_sharpe",
            "ret_yr", "vol", "mdd", "worst", "expo", "bench_sharpe", "matched_ret_yr", "bench_t",
            "trades_yr", "gross_sharpe", "swap_yr", "cost_yr"]
    print(df[df.period.isin(["OOS"])][cols].round(3).to_string(index=False))
    print("\n== OOS cost x2 / zero cost / spread only (no swap) ==")
    print(df[df.period.isin(["OOS2", "OOS0", "OOSns"])][["id", "fill", "period", "sharpe", "t", "p5_bp",
                                                         "alpha_t", "ret_yr"]].round(3).to_string(index=False))

    print("\n== Gate (decisive = worse fill by OOS t) ==")
    gate = {}
    la = {}
    for v in M.VARIANTS:
        m = dec[v]
        o = res[(v, m)]["OOS"]
        if do_la:
            la[v] = {mm: M.lookahead(data, v, mm) for mm in ("close", "open")}
        lat = all(a == 20 and b == 20 for a, b in la.get(v, {"x": (20, 20)}).values())
        ok = o["t"] >= M.BAR and o["p5_bp"] > 0 and o["alpha_t"] >= M.BAR and lat
        gate[v] = ok
        print(f"{v} fill={m:5s} t={o['t']:+.2f} p5={o['p5_bp']:+.2f}bp alpha_t={o['alpha_t']:+.2f} "
              f"Sharpe={o['sharpe']:+.2f} (bench matched Sharpe {o['bench_sharpe']:+.2f}) "
              f"x2 t={res[(v, m)]['OOS2']['t']:+.2f} lookahead={la.get(v)} -> {'PASS' if ok else 'FAIL'}")

    # per-year + breaches for every variant (decisive fill)
    print("\n== Per year, decisive fill, net 1x: return % (Sharpe) ==")
    yt = {}
    for v in M.VARIANTS:
        b = res[(v, dec[v])]["book"]
        yt[v] = M.per_year(b.loc[M.OOS_START:])
    years = yt[head].index
    print("year  " + "  ".join(f"{v:>14s}" for v in M.VARIANTS))
    for y in years:
        print(f"{y}  " + "  ".join(f"{yt[v].ret[y]*100:+6.2f} ({yt[v].sharpe[y]:+5.2f})" for v in M.VARIANTS))

    print("\n== Scaled book (scale fixed on IS close-fill vol): breaches of -5% day, maxDD, worst day ==")
    for v in M.VARIANTS:
        is_vol = res[(v, "close")]["IS"]["vol"]
        b = res[(v, dec[v])]["book"].loc[M.OOS_START:]
        for tgt in (0.15, 0.20):
            x = b.net.values * tgt / is_vol
            print(f"{v} target {tgt:.0%}: realised OOS vol {x.std()*np.sqrt(252):.1%}, "
                  f"days < -5%: {(x < -0.05).sum()}, worst {x.min():+.2%}, maxDD {M.maxdd(x):+.1%}, "
                  f"ret/yr {x.mean()*252:+.1%}")
    return res, dec, head, gate


if __name__ == "__main__":
    main(do_la="--no-lookahead" not in sys.argv)
