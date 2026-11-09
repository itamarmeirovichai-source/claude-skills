#!/usr/bin/env python3
"""Joint power of the Gate v2 criteria that a synthetic strategy with a KNOWN true Sharpe can be run through.

Simulated: daily net P&L with Student-t(4) innovations (unit variance), true net Sharpe S at 1x cost, cost drag d
such that costs are a share `cost_share` of gross (net2x = S - d, d = S * cost_share / (1 - cost_share)).
Criteria simulated: 3 (2x cost: net mean > 0 and t >= 1.65), 4 (t_min(iid, NW lag 10) >= 3.6807 and the normal
lower bound at 0.05/430 > 0), 7 (>= 70% of calendar years positive; no year > 50% and no month > 50% of total profit;
2 of 3 random terciles positive; four +-25% neighbours (corr 0.9, mean x0.85) all net positive; one-minute delay
(corr 0.95, mean x0.6) keeps >= half the edge). Criteria 6 (nulls) are implied by 4 for an uncorrelated benchmark;
1, 2, 5, 8, 9, 10, 11, 12 are process criteria and are taken as passed. The bootstrap lower bound is approximated by
the normal lower bound (same quantile), which is what a 430,000-draw bootstrap converges to for t-distributed P&L.
Usage: python3 quant-edge/tools/joint_power.py [n_paths]
"""
import sys
import numpy as np
from statistics import NormalDist

Z = NormalDist().inv_cdf(1 - 0.05 / 430)


def nw_t(x, lag=10):
    n = x.shape[1]
    e = x - x.mean(1, keepdims=True)
    s = (e * e).sum(1)
    for k in range(1, lag + 1):
        s += 2 * (1 - k / (lag + 1)) * (e[:, k:] * e[:, :-k]).sum(1)
    return x.mean(1) / np.sqrt(s / n / n)


def run(S, years, cost_share, n_paths, rng):
    n = 252 * years
    d = S * cost_share / (1 - cost_share)
    s_daily = S / np.sqrt(252)
    eps = rng.standard_t(4, size=(n_paths, n)) / np.sqrt(2.0)   # unit variance
    net = s_daily + eps
    net2x = (S - d) / np.sqrt(252) + eps
    # criterion 4
    t_iid = net.mean(1) / (net.std(1, ddof=1) / np.sqrt(n))
    t_nw = nw_t(net)
    c4 = (np.minimum(t_iid, t_nw) >= Z) & (net.mean(1) - Z * net.std(1, ddof=1) / np.sqrt(n) > 0)
    # criterion 3
    t2 = net2x.mean(1) / (net2x.std(1, ddof=1) / np.sqrt(n))
    c3 = (net2x.mean(1) > 0) & (t2 >= 1.65)
    # criterion 7
    yr = net.reshape(n_paths, years, 252).sum(2)
    tot = net.sum(1)
    c7_years = (yr > 0).sum(1) >= int(np.ceil(0.7 * years - 1e-9 + 0.5 - 0.5)) if False else (yr > 0).sum(1) >= np.floor(0.7 * years + 0.5)
    c7_year50 = (yr.max(1) / np.where(tot > 0, tot, np.nan)) <= 0.5
    mo = net[:, : (n // 21) * 21].reshape(n_paths, -1, 21).sum(2)
    c7_month50 = (mo.max(1) / np.where(tot > 0, tot, np.nan)) <= 0.5
    perm = rng.permutation(n)
    terc = np.stack([net[:, perm[i::3]].sum(1) for i in range(3)], 1)
    c7_terc = (terc > 0).sum(1) >= 2
    neigh_ok = np.ones(n_paths, bool)
    for _ in range(4):
        e2 = rng.standard_t(4, size=(n_paths, n)) / np.sqrt(2.0)
        nb = 0.85 * s_daily + 0.9 * eps + np.sqrt(1 - 0.81) * e2
        neigh_ok &= nb.mean(1) > 0
    e3 = rng.standard_t(4, size=(n_paths, n)) / np.sqrt(2.0)
    delayed = 0.6 * s_daily + 0.95 * eps + np.sqrt(1 - 0.9025) * e3
    c7_delay = delayed.mean(1) >= 0.5 * net.mean(1)
    c7 = c7_years & np.nan_to_num(c7_year50, nan=False) & np.nan_to_num(c7_month50, nan=False) & c7_terc & neigh_ok & c7_delay
    joint = c3 & c4 & c7
    return dict(c4=c4.mean(), c3=c3.mean(), c7=c7.mean(), c7_years=c7_years.mean(), c7_conc=(np.nan_to_num(c7_year50, nan=False) & np.nan_to_num(c7_month50, nan=False)).mean(),
                neigh=neigh_ok.mean(), delay=c7_delay.mean(), joint=joint.mean())


if __name__ == "__main__":
    n_paths = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    rng = np.random.default_rng(20261103)
    print(f"joint power, {n_paths} paths per cell, t(4) daily P&L, bar z={Z:.4f}")
    print("S_true | years | cost_share | crit4 | crit3(2x) | crit7 | years>=70% | conc | neigh | delay | JOINT")
    for cost_share in (1 / 3, 1 / 2):
        for years in (5, 8, 10):
            for S in (1.5, 2.0, 2.4, 3.0):
                r = run(S, years, cost_share, n_paths, rng)
                print(f"{S:5.1f} | {years:5d} | {cost_share:9.2f} | {r['c4']:.2f} | {r['c3']:.2f} | {r['c7']:.2f} | {r['c7_years']:.2f} | {r['c7_conc']:.2f} | {r['neigh']:.2f} | {r['delay']:.2f} | {r['joint']:.2f}")
