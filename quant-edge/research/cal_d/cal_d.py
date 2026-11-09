#!/usr/bin/env python3
"""CAL-D: daily-pipeline calibration (registry row CAL-D, commit a9ddfcd). MOP 12-month TSMOM on 54 futures.

Reads data only through qe.gateway.load. IS (1984-1989) is read for signal warm-up only; the headline is OOS 1990-2016.
Usage: python3 quant-edge/research/cal_d/cal_d.py  -> writes quant-edge/research/results/CAL-D.md and cal_d_yearly.csv
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from qe import gateway, stats  # noqa: E402

ID = "CAL-D"
LOOKBACK_D, COM, TARGET = 252, 60, 0.40


def frame(window):
    df = gateway.load(ID, window).set_index("ts")
    return df.drop(columns=[c for c in ("VF",) if c in df.columns]).astype(float)


def run(rets):
    ewvar = (rets ** 2).ewm(com=COM, min_periods=COM).mean()
    vol = np.sqrt(ewvar * 261)
    cum = np.log1p(rets.fillna(0.0))
    hist = rets.notna().cumsum()
    mom = cum.rolling(LOOKBACK_D, min_periods=LOOKBACK_D).sum()
    month = rets.index.tz_localize(None).to_period("M")
    is_month_end = pd.Series(month, index=rets.index) != pd.Series(month, index=rets.index).shift(-1)
    ends = rets.index[is_month_end.values]
    w = pd.DataFrame(np.nan, index=rets.index, columns=rets.columns)
    for t in ends:
        ok = (hist.loc[t] >= LOOKBACK_D) & vol.loc[t].notna() & (vol.loc[t] > 0) & mom.loc[t].notna()
        row = pd.Series(0.0, index=rets.columns)
        row[ok] = np.sign(mom.loc[t, ok]) * TARGET / vol.loc[t, ok]
        w.loc[t] = row                                # assets not eligible at t hold 0 for the month
    w = w.ffill()                                     # weights decided at month-end t ...
    w = w.shift(1)                                    # ... applied from the next day (no look-ahead)
    contrib = w * rets
    n = ((w.fillna(0) != 0) & rets.notna()).sum(axis=1)
    port = contrib.sum(axis=1, min_count=1) / n.replace(0, np.nan)
    turnover = (w.fillna(0).diff().abs().sum(axis=1) / n.replace(0, np.nan)).fillna(0)
    return port.dropna(), turnover


def main():
    is_df, oos_df = frame("is"), frame("oos")
    full = pd.concat([is_df, oos_df]).sort_index()
    port, turn = run(full)
    oos = port[port.index >= pd.Timestamp("1990-01-01", tz="UTC")]
    cost1 = turn.reindex(oos.index).fillna(0) * 1e-4      # 1 bp per side on traded notional
    res = {}
    for name, x in (("gross", oos), ("net1x", oos - cost1), ("net2x", oos - 2 * cost1)):
        x = x.values
        tmin, ti, tn = stats.gate_t(x, longest_hold_days=21)
        res[name] = dict(sharpe=stats.sharpe(x, 261), t_min=tmin, t_iid=ti, t_nw=tn, mean_ann=x.mean() * 261, vol_ann=x.std(ddof=1) * np.sqrt(261))
    se = stats.sharpe_se(oos.values, 261)
    yearly = oos.groupby(oos.index.year).sum()
    yearly.to_csv(ROOT / "research" / "cal_d" / "cal_d_yearly.csv", header=["sum_daily_ret"])
    full_p = port[port.index >= pd.Timestamp("1985-01-01", tz="UTC")]
    s_full = stats.sharpe(full_p.values, 261)
    lo, hi = 0.85, 1.45
    ok = lo <= res["gross"]["sharpe"] <= hi
    eq = (1 + oos).cumprod(); dd = (eq / eq.cummax() - 1).min()
    out = ROOT / "research" / "results" / "CAL-D.md"
    lines = [
        "# CAL-D — daily pipeline calibration (MOP 12-month TSMOM, 54 futures)", "",
        f"Registry row CAL-D (registered commit a9ddfcd, count 1). Script `research/cal_d/cal_d.py`. Data `daily_futures_1984_2016` "
        "via `qe.gateway.load` (IS read for 12-month warm-up only; reads logged in `registry_reads.log`).", "",
        "**This is a pipeline calibration, not a strategy test. It never re-opens H0007 and is not an edge claim.**", "",
        "| series (OOS 1990-01-01..2016-10-28) | Sharpe | t_min (iid, NW lag 21) | ann. mean | ann. vol |", "|---|---|---|---|---|",
    ]
    for k, v in res.items():
        lines.append(f"| {k} | {v['sharpe']:.3f} | {v['t_min']:.2f} ({v['t_iid']:.2f}, {v['t_nw']:.2f}) | {v['mean_ann']*100:.2f}% | {v['vol_ann']*100:.2f}% |")
    lines += ["",
              f"- Sharpe s.e. (Mertens/Opdyke, annual): {se['se_annual']:.3f}; 90% CI {se['ci90_annual'][0]:.2f}..{se['ci90_annual'][1]:.2f}; skew {se['skew']:.2f}, kurtosis {se['kurtosis']:.1f}; Lo-adjusted Sharpe {se['sharpe_annual_lo']:.3f}.",
              f"- Max drawdown (gross, uncompounded daily sum compounded): {dd*100:.1f}%. Days: {len(oos)}.",
              f"- 1985-2016 Sharpe of the same run (comparable to the inherited 1.17): {s_full:.3f}.",
              f"- Positive calendar years (OOS): {(yearly > 0).sum()} of {len(yearly)}.",
              "",
              f"## Decision (rule fixed in the row)", "",
              f"OOS gross Sharpe {res['gross']['sharpe']:.3f} {'inside' if ok else 'OUTSIDE'} [{lo}, {hi}] → pipeline calibration **{'PASSES' if ok else 'FAILS: testing halts until the cause is named'}** on criterion (a).",
              "Criterion (b), year-sign agreement with the inherited run, is checked separately against the inherited yearly table (see below).", ""]
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
