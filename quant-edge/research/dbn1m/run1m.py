"""Runner for Q-0017..Q-0021 (registered at 56c0f6f).

  python3 run1m.py is  <ID>    IS only: events, neighbours, harnesses (truncation / perturbation / planted). No OOS read.
  python3 run1m.py oos <ID>    the single OOS run: one IS read (warm-up) + one OOS read per dataset, Gate v2, result file.
"""
import json
import math
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "dbn1h"))
sys.path.insert(0, str(HERE.parents[1] / "src"))
import kit  # noqa: E402
import kit1m as K  # noqa: E402
import rows1m as R  # noqa: E402

DATASETS = {"Q-0017": ["dbn_glbx_1m_ES"], "Q-0018": ["dbn_glbx_1m_ES", "dbn_glbx_1m_MES"],
            "Q-0019": ["dbn_glbx_1m_ES", "dbn_glbx_1m_GC"], "Q-0020": ["dbn_glbx_1m_ES", "dbn_glbx_1m_MES"],
            "Q-0021": ["dbn_glbx_1m_ES", "dbn_glbx_1m_GC"]}


def split(rid):
    s = json.load(open(ROOT / "research" / "prereg" / f"{rid}.json"))["split"]
    d = dict(p.split("=") for p in s.split(";"))
    is0, is1 = d["IS"].split("..")
    oos0, oos1 = d["OOS"].split("..")
    return date.fromisoformat(is0), date.fromisoformat(is1), date.fromisoformat(oos0), date.fromisoformat(oos1)


def variants(rid):
    """(name, compute kwargs) for base, neighbours and the one-bar delay, exactly as listed in the registration."""
    if rid == "Q-0017":
        b = R.Q17
        nb = [("k0.75", dict(b, k=0.75)), ("k1.25", dict(b, k=1.25)), ("exit16:04bar", dict(b, exit_T="16:05")),
              ("exit16:07bar", dict(b, exit_T="16:08")), ("com45", dict(b, com=45)), ("com75", dict(b, com=75))]
        return R.compute_q17, b, nb, dict(b, entry="16:02")
    if rid == "Q-0018":
        b = R.Q18
        nb = [("k0.375", dict(b, k=0.375)), ("k0.625", dict(b, k=0.625)), ("exit16:12bar", dict(b, exit_T="16:13")),
              ("exit16:14bar", dict(b, exit_T="16:15")), ("com45", dict(b, com=45)), ("com75", dict(b, com=75))]
        return R.compute_q18, b, nb, dict(b, entry="16:11")
    if rid == "Q-0019":
        b = R.Q19
        nb = [("z-3", dict(b, z=-3.0)), ("z-5", dict(b, z=-5.0)), ("vr1.5", dict(b, vr=1.5)), ("vr2.5", dict(b, vr=2.5)),
              ("hold11", dict(b, hold=11)), ("hold19", dict(b, hold=19))]
        return R.compute_q19, b, nb, dict(b, delay=2)
    if rid == "Q-0020":
        b = R.Q20
        nb = [("k0.75", dict(b, k=0.75)), ("k1.25", dict(b, k=1.25)), ("exit09:53bar", dict(b, exit_T="09:54")),
              ("exit10:05bar", dict(b, exit_T="10:06")), ("q0.60", dict(b, q=0.60)), ("q0.75", dict(b, q=0.75))]
        return R.compute_q20, b, nb, dict(b, entry="09:36")
    if rid == "Q-0021":
        b = R.Q21
        nb = [("k1.125", dict(b, k=1.125)), ("k1.875", dict(b, k=1.875)), ("exit10:30", dict(b, exit_mode="10:30")),
              ("com45", dict(b, com=45)), ("com75", dict(b, com=75))]
        return R.compute_q21, b, nb, dict(b, entry="18:30")
    raise KeyError(rid)


def run_compute(rid, fn, F, days, all_days, p, feats=None, **kw):
    if rid == "Q-0021":
        return fn(F, days, p, all_days=all_days, **kw)
    if rid == "Q-0019":
        return fn(F, days, p, feats=feats, **kw)
    return fn(F, days, p, **kw)


def series(ev, mult=1.0, pooled=False):
    """Net per-event series (or per-date pooled for Q-0021) and its dates."""
    if ev.empty:
        return np.array([]), []
    net = ev["gross"].to_numpy(float) - mult * ev["cost1"].to_numpy(float)
    if pooled:
        s = pd.Series(net, index=ev["date"].values).groupby(level=0).sum().sort_index()
        return s.to_numpy(float), list(s.index)
    return net, list(ev["date"])


def vol_measure(F, days, rid):
    """Volatility-tercile variable per day: trailing 20-day s.d. of daily close-to-close log returns (ES 16:00; GC 13:30)."""
    out = {}
    for root in ("ES", "GC"):
        if root in F:
            c, _ = F[root].P(K.at(days, R.CLOSE_T[root]))
            out[root] = K.trailing_sd_daily(pd.Series(c, index=days))
    return out


def harness(rid, fn, F, days, all_days, p, sample=30, seed=0):
    rng = np.random.default_rng(seed)
    feats = None
    if rid == "Q-0019":
        base_all = None
    base = run_compute(rid, fn, F, days, all_days, p, decide=True) if rid != "Q-0019" else None
    res = {"n": 0, "truncation": 0, "perturbation": 0}
    if rid != "Q-0019":
        keys = list(base["key"])
        pick = sorted(rng.choice(len(keys), size=min(sample, len(keys)), replace=False))
        bmap = base.set_index("key")["side"]
        for j in pick:
            k = keys[j]
            t0 = base.loc[base["key"] == k, "entry_et"].iloc[0]
            for name in ("truncation", "perturbation"):
                G = {}
                for r, f in F.items():
                    if name == "truncation":
                        G[r] = f.subset(f.et < t0)
                    else:
                        g = f.subset(np.ones(len(f.et), bool))
                        post = g.et >= t0
                        g.open = np.where(post, g.open * (1 + 0.01 * rng.standard_normal(len(g.et))), g.open)
                        g.close = np.where(post, g.close * (1 + 0.01 * rng.standard_normal(len(g.et))), g.close)
                        G[r] = g
                ev = run_compute(rid, fn, G, days, all_days, p, decide=True)
                m = ev.set_index("key")["side"] if not ev.empty else pd.Series(dtype=float)
                if not (k in m.index and m.loc[k] == bmap.loc[k]):
                    res[name] += 1
            res["n"] += 1
        return res
    # Q-0019: slice 30 sessions before each sampled event (the features use 20 prior sessions)
    full = fn(F, days, p, decide=True)
    keys = list(full["key"])
    pick = sorted(rng.choice(len(keys), size=min(sample, len(keys)), replace=False))
    for j in pick:
        row = full.iloc[j]
        t0 = np.datetime64(row["entry_et"])
        lo = t0 - np.timedelta64(30 * 24 * 60 * 2, "m")
        Fs = {r: f.subset((f.et >= lo) & (f.et < t0 + np.timedelta64(3, "D"))) for r, f in F.items()}
        b = fn(Fs, days, p, decide=True, roots=(row["root"],))
        bm = set(b["key"])
        for name in ("truncation", "perturbation"):
            G = {}
            for r, f in Fs.items():
                if name == "truncation":
                    G[r] = f.subset(f.et < t0)
                else:
                    g = f.subset(np.ones(len(f.et), bool))
                    post = g.et >= t0
                    g.open = np.where(post, g.open * (1 + 0.01 * rng.standard_normal(len(g.et))), g.open)
                    g.close = np.where(post, g.close * (1 + 0.01 * rng.standard_normal(len(g.et))), g.close)
                    G[r] = g
            ev = fn(G, days, p, decide=True, roots=(row["root"],))
            if (row["key"] in bm) != (row["key"] in set(ev["key"])) or row["key"] not in bm:
                res[name] += 1
        res["n"] += 1
    return res


def main(phase, rid):
    is0, is1, oos0, oos1 = split(rid)
    windows = ("is",) if phase == "is" else ("is", "oos")
    F = K.load(rid, DATASETS[rid], windows)
    end = is1 if phase == "is" else oos1
    days, early, all_days = K.full_days(is0, end)
    fn, base_p, nbs, delay_p = variants(rid)
    feats = {r: R.burst_features(F[r]) for r in ("ES", "GC")} if rid == "Q-0019" else None
    pooled = rid == "Q-0021"
    ev = run_compute(rid, fn, F, days, all_days, base_p, feats=feats)
    out = {"id": rid, "phase": phase, "events_total": int(len(ev))}
    lo_d = is0 if phase == "is" else oos0
    hi_d = is1 if phase == "is" else oos1
    sel = lambda e: e[(pd.to_datetime(e["date"]) >= pd.Timestamp(lo_d)) & (pd.to_datetime(e["date"]) <= pd.Timestamp(hi_d))] if not e.empty else e
    E = sel(ev)
    x1, d1 = series(E, 1.0, pooled)
    x2, _ = series(E, 2.0, pooled)
    xg, _ = series(E, 0.0, pooled)
    out["n_obs"] = int(len(x1))
    if len(x1) < 10:
        out["note"] = "fewer than 10 observations in the window"
        print(json.dumps(out, default=str, indent=1)); return out
    g1 = kit.gate(x1, d1, clusters=np.array([str(d) for d in d1]))
    out["gate_net1"] = g1
    out["mean_gross"] = float(xg.mean()); out["mean_net2"] = float(x2.mean())
    out["power"] = kit.power_line((pd.Timestamp(hi_d) - pd.Timestamp(lo_d)).days / 365.25)
    nb_means = {}
    for name, p in nbs:
        e2 = sel(run_compute(rid, fn, F, days, all_days, p, feats=feats if rid != "Q-0019" or p.get("z") is not None else feats))
        xx, _ = series(e2, 1.0, pooled)
        nb_means[name] = float(xx.mean()) if len(xx) else float("nan")
    ed = sel(run_compute(rid, fn, F, days, all_days, delay_p, feats=feats))
    xd, _ = series(ed, 1.0, pooled)
    delay_mean = float(xd.mean()) if len(xd) else float("nan")
    vm = vol_measure(F, days, rid)
    is_days = [d for d in days if is0 <= d <= is1]
    if pooled:
        tv_root = "ES"
    else:
        tv_root = None
    bounds = kit.tercile_bounds(vm["ES" if "ES" in vm else list(vm)[0]].reindex(is_days))
    if pooled:
        tv = vm["ES"].reindex(d1).to_numpy(float)
    else:
        tv = np.array([vm[r].get(d, np.nan) for r, d in zip(E["root"], E["date"])], float)
        if rid == "Q-0019":  # per-root IS bounds
            bnds = {r: kit.tercile_bounds(vm[r].reindex(is_days)) for r in vm}
            # map each event's value to a common tercile index by its own root's bounds
            idx = []
            for r, v in zip(E["root"], tv):
                lo_, hi_ = bnds[r]
                idx.append(0 if v <= lo_ else (1 if v <= hi_ else 2) if np.isfinite(v) else np.nan)
            tv = np.array(idx, float); bounds = (0.5, 1.5)
    ok7, det7 = K.crit7(x1, d1, tv, bounds, nb_means, delay_mean)
    out["crit7_ok"] = ok7; out["crit7"] = det7
    out["verdict"] = kit.verdict(g1, float(x2.mean()), ok7)
    yt = kit.years_table(x1, d1)
    out["years"] = {int(k): [float(v["sum"]), int(v["count"])] for k, v in yt.iterrows()}
    if rid in ("Q-0018",):
        fp = R.mes_footprint(F, days)
        out["mes_footprint_median_on_events"] = float(fp.reindex(list(E["date"])).median())
    if rid == "Q-0020":
        e_ctrl = sel(run_compute(rid, fn, F, days, all_days, dict(base_p, arm="bottom")))
        xc, _ = series(e_ctrl, 1.0)
        out["control_arm_bottom_tercile"] = {"n": int(len(xc)), "mean_net1": float(xc.mean()) if len(xc) else None}
    if rid == "Q-0019":
        for r in ("ES", "GC"):
            xr, _ = series(E[E["root"] == r], 1.0)
            out[f"leg_{r}"] = {"n": int(len(xr)), "mean_net1": float(xr.mean()) if len(xr) else None}
    if rid == "Q-0021":
        for r in ("ES", "GC"):
            xr, _ = series(E[E["root"] == r], 1.0)
            out[f"leg_{r}"] = {"n": int(len(xr)), "mean_net1": float(xr.mean()) if len(xr) else None}
    if phase == "is":
        h = harness(rid, fn, F, days, all_days, base_p)
        hp = harness(rid, fn, F, days, all_days, base_p, sample=30, seed=1) if False else None
        out["harness"] = h
        # planted look-ahead must FAIL truncation
        def planted(F_, d_, p_, decide=False, **kw):
            return fn(F_, d_, p_, plant=True, decide=decide, **kw)
        out["planted"] = harness(rid, planted, F, days, all_days, base_p)
    (HERE / f"{rid}_{phase}.json").write_text(json.dumps(out, default=str, indent=1))
    print(json.dumps({k: out[k] for k in out if k not in ("years",)}, default=str, indent=1))
    return out


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
