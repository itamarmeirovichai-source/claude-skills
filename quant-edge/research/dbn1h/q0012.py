"""Q-0012 CME cross-index CO-OC reversal (ES NQ YM EMD NKD, 1h). Usage: q0012.py --stage is|oos"""
import argparse, json, math, sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit

RID = "Q-0012"
U = ["ES", "NQ", "YM", "EMD", "NKD"]
DS = [f"dbn_glbx_1h_{r}" for r in U]
PV = {"ES": 50.0, "NQ": 20.0, "YM": 5.0, "EMD": 100.0, "NKD": 5.0}
SLIP = {"ES": 0.30, "NQ": 0.25, "YM": 1.2, "EMD": 0.20, "NKD": 6.0}
OUT = Path(__file__).resolve().parent


def compute(bars, days, early, entry_h=10, exit_h=15, com=60, cost_mult=1.0, ex_ante=False):
    full = [d for d in days if d not in early]
    prev = {}
    for a, b in zip(days[:-1], days[1:]):
        prev[b] = a
    per = {}
    for i in U:
        b = bars[i]
        rows = []
        for d in full:
            p = prev.get(d)
            if p is None or p in early:
                continue
            C = b.get((p, 15)); S = b.get((d, 9)); E = b.get((d, entry_h)); X = b.get((d, exit_h))
            co = r = np.nan; iid = None
            if C and S and C[2] == S[2]:
                co = math.log(S[1] / C[1]); iid = S[2]
            if E and X and E[2] == X[2]:
                r = math.log(X[1] / E[0])
            tradable = (not np.isnan(r)) and (not np.isnan(co)) and E[2] == iid
            ok = (not np.isnan(co)) if ex_ante else tradable
            rows.append((d, co, r, E[0] if E else np.nan, X[1] if X else np.nan, ok, tradable))
        f = pd.DataFrame(rows, columns=["d", "co", "r", "pin", "pout", "ok", "tradable"]).set_index("d")
        f["s"] = kit.ewma_prev(f["co"], com, "rms", index=f.index).to_numpy()
        f["sig"] = kit.ewma_prev(f["r"], com, "std", index=f.index).to_numpy()
        f["z"] = f["co"] / f["s"]
        f["elig"] = f["ok"] & f["s"].notna() & f["sig"].notna()
        per[i] = f
    allx = sorted(set().union(*[set(f.index) for f in per.values()]))
    out = []
    for d in allx:
        el = [(i, per[i].loc[d]) for i in U if d in per[i].index and per[i].loc[d, "elig"]]
        if len(el) < 4:
            continue
        zs = [(x["z"], k, i, x) for k, (i, x) in enumerate(el)]
        L = min(zs, key=lambda t: (t[0], t[1])); S = max(zs, key=lambda t: (t[0], -t[1]))
        res = {"d": d, "n_elig": len(el), "L": L[2], "S": S[2]}
        if not (L[3]["tradable"] and S[3]["tradable"]):
            if ex_ante:
                res.update(wL=kit.VOL_TARGET / L[3]["sig"], wS=kit.VOL_TARGET / S[3]["sig"], gross=np.nan, cost=np.nan, net=np.nan)
                out.append(res)
            continue
        tot_g = 0.0; cst = 0.0
        for side, t in ((1, L), (-1, S)):
            i, x = t[2], t[3]
            w = kit.VOL_TARGET / x["sig"]
            tot_g += side * w * x["r"]
            cst += w * (kit.cost_frac(x["pin"], SLIP[i], PV[i], mult=cost_mult) + kit.cost_frac(x["pout"], SLIP[i], PV[i], mult=cost_mult))
            res["w" + ("L" if side == 1 else "S")] = w
        res.update(gross=tot_g, cost=cst, net=tot_g - cst)
        out.append(res)
    return pd.DataFrame(out)


def run(stage, dry=False):
    CUT = "2013-01-01" if dry else "2015-01-01"
    windows = ("is",) if (stage == "is" or dry) else ("is", "oos")
    bars, frames = kit.load_bars(RID, DS, windows)
    end = "2014-12-31" if (stage == "is" or dry) else "2024-12-31"
    days, early = kit.sessions("2010-06-07", end)
    res = {}
    base = compute(bars, days, set(early))
    if stage == "is":
        isd = base
        h = kit.harness(lambda bb: compute(bb, days, set(early)), bars, "d", lambda row, k: (k, 10),
                        30, ["L", "S", "wL", "wS", "n_elig"])
        hx = kit.harness(lambda bb: compute(bb, days, set(early), ex_ante=True), bars, "d", lambda row, k: (k, 10),
                         30, ["L", "S", "wL", "wS", "n_elig"])
        # planted look-ahead: z uses the 15:00 bar close of d instead of 09:00
        def planted(bb):
            b2 = {i: {(d, h): (bb[i].get((d, 15), v) if h == 9 else v) for (d, h), v in bb[i].items()} for i in bb}
            return compute(b2, days, set(early))
        hp = kit.harness(planted, bars, "d", lambda row, k: (k, 10), 30, ["L", "S"])
        es = bars["ES"]; esd = pd.Series({d: es[(d, 15)][1] for d in days if (d, 15) in es}).sort_index()
        vol = np.log(esd).diff().rolling(20).std().shift(1)
        b1, b2 = kit.tercile_bounds(vol.reindex(isd["d"]))
        res = {"harness": h, "harness_ex_ante": hx, "planted": hp, "is_days": len(isd), "is_net_bp": 1e4 * isd["net"].mean(),
               "is_t": kit.stats.iid_t(isd["net"].to_numpy()), "terciles": [b1, b2]}
        json.dump(res, open(OUT / "Q-0012_is.json", "w"), indent=1, default=str)
        print(json.dumps(res, indent=1, default=str)); return
    is_info = json.load(open(OUT / "Q-0012_is.json"))
    oos = base[pd.to_datetime(base["d"]) >= CUT].reset_index(drop=True)
    xa = compute(bars, days, set(early), ex_ante=True); xa = xa[(pd.to_datetime(xa["d"]) >= CUT)].dropna(subset=["net"])
    gx = kit.gate(xa["net"], xa["d"], nw_lag=10, mean_block=20, per_year=252)
    n2 = compute(bars, days, set(early), cost_mult=2.0); n2 = n2[pd.to_datetime(n2["d"]) >= CUT]
    g1 = kit.gate(oos["net"], oos["d"], nw_lag=10, mean_block=20, per_year=252)
    gg = kit.gate(oos["gross"], oos["d"], nw_lag=10, mean_block=20, per_year=252)
    g2 = kit.gate(n2["net"], n2["d"], nw_lag=10, mean_block=20, per_year=252)
    yt = kit.years_table(oos["net"], oos["d"])
    es = bars["ES"]; esd = pd.Series({d: es[(d, 15)][1] for d in days if (d, 15) in es}).sort_index()
    vol = np.log(esd).diff().rolling(20).std().shift(1)
    b1, b2 = is_info["terciles"]
    tv = vol.reindex(oos["d"]).to_numpy()
    terc = pd.Series(np.where(tv < b1, 0, np.where(tv < b2, 1, 2)), index=oos.index); terc[np.isnan(tv)] = -1
    tt = oos.groupby(terc)["net"].agg(["count", "sum", "mean"])
    pair = oos.apply(lambda r: "/".join(sorted([r["L"], r["S"]])), axis=1)
    pt = oos.groupby(pair)["net"].agg(["count", "sum", "mean"]).sort_values("sum", ascending=False)
    neigh = {}
    for name, kw in (("entry 11:00 (hold 5 h)", dict(entry_h=11)), ("exit 14:00 bar close (hold 5 h)", dict(exit_h=14)),
                     ("EWMA com 45", dict(com=45)), ("EWMA com 75", dict(com=75))):
        z = compute(bars, days, set(early), **kw); z = z[pd.to_datetime(z["d"]) >= CUT]
        neigh[name] = (len(z), z["net"].sum(), 1e4 * z["net"].mean(), kit.stats.iid_t(z["net"].to_numpy()))
    # random-pair null and sign-flip null on gross
    rng = np.random.default_rng(0)
    # random pair: per day choose two distinct eligible instruments: approximate with the realised legs' universe via recompute
    gross = oos["gross"].to_numpy()
    flips = np.array([np.mean(gross * rng.choice([-1, 1], size=gross.size)) for _ in range(10000)])
    p_flip = float((flips >= gross.mean()).mean())
    sub = {}
    for nm, a, b in (("2015-2019", CUT, "2019-12-31"), ("2020-03..2022-04", "2020-03-01", "2022-04-30"), ("2022-05..2024", "2022-05-01", "2024-12-31")):
        m = (pd.to_datetime(oos["d"]) >= a) & (pd.to_datetime(oos["d"]) <= b)
        sub[nm] = (int(m.sum()), 1e4 * oos.loc[m, "net"].mean(), kit.stats.iid_t(oos.loc[m, "net"].to_numpy()))
    yrs_pos = int((yt["sum"] > 0).sum())
    net_pos = oos["net"].sum() > 0
    crit7 = (net_pos and yrs_pos >= 7 and (tt.loc[[0, 1, 2], "sum"] > 0).sum() >= 2 and all(v[1] > 0 for v in neigh.values())
             and (pt["sum"].max() <= 0.5 * oos["net"].sum()))
    v = kit.verdict(g1, g2["mean"], crit7)
    res = dict(g1=g1, gross=gg, g2=g2, ex_ante=gx, ex_ante_days=len(xa), delay_note='one-bar delay = entry 11:00 (neighbour row)', years=yt.to_dict(), terc=tt.to_dict(), pairs=pt.head(10).to_dict(), neigh=neigh,
               p_flip=p_flip, sub=sub, crit7=bool(crit7), verdict=v, n_days=len(oos), legs=oos[["L", "S"]].stack().value_counts().to_dict(),
               univ=oos["n_elig"].value_counts().to_dict())
    tag = "dry" if dry else "oos"
    json.dump(res, open(OUT / f"Q-0012_{tag}.json", "w"), indent=1, default=str)
    oos.to_csv(OUT / f"Q-0012_{tag}_days.csv", index=False)
    print(json.dumps({k: res[k] for k in ("g1", "g2", "verdict", "crit7", "n_days")}, indent=1, default=str))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--stage", required=True); ap.add_argument("--dry", action="store_true"); a = ap.parse_args(); run(a.stage, a.dry)
