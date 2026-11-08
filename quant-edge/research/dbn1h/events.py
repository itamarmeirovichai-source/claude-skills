"""Q-0013 (month-end Treasury, UB+ZN), Q-0014 (Crop Progress, ZC/ZS), Q-0015 (NG storage day): event holds on 1h bars.
Usage: events.py Q-00nn --stage is|oos [--dry]   (written after registration commit 4588d6c)"""
import argparse, json, math, sys
from datetime import timedelta
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
import kit
from qe import gateway

OUT = Path(__file__).resolve().parent
PV = {"UB": 1000.0, "ZN": 1000.0, "ZC": 50.0, "ZS": 50.0, "NG": 10000.0}
SLIP = {"UB": 1 / 32, "ZN": 1 / 64, "ZC": 0.50, "ZS": 0.50, "NG": 0.001}
CFG = {
 "Q-0013": dict(insts=["UB", "ZN"], cal=None, entry_h=18, entry_fb=[19, 20, 21], exit_h=15, exit_fb=[14, 13, 12, 11],
                early_skip_exit=True, is_end="2014-12-31", oos_start="2015-01-01", nw=3, block=5.0, terc_inst="ZN"),
 "Q-0014": dict(insts=["ZC", "ZS"], cal="cal_nass_crop_progress", entry_h=20, entry_fb=[], exit_h=12, exit_fb=[11, 10, 9],
                early_skip_exit=False, is_end="2014-12-31", oos_start="2015-01-01", nw=4, block=5.0, terc_inst="ZC"),
 "Q-0015": dict(insts=["NG"], cal="cal_eia_ngsr", entry_h=18, entry_fb=[19, 20, 21], exit_h=14, exit_fb=[13, 12, 11],
                early_skip_exit=False, is_end="2018-12-31", oos_start="2019-01-01", nw=4, block=5.0, terc_inst="NG"),
}


def hold(b, ev_date, s, entry_h, entry_fb, exit_h, exit_fb, skip_exit_main=False):
    """Entry on the evening ev_date (bar open), exit on session s (bar close); same instrument_id or None."""
    E = None
    for h in [entry_h] + list(entry_fb):
        if (ev_date, h) in b:
            E = b[(ev_date, h)]; break
    X = None
    for h in ([] if skip_exit_main else [exit_h]) + list(exit_fb):
        if (s, h) in b:
            X = b[(s, h)]; break
    if E is None or X is None or E[2] != X[2]:
        return None
    return E[0], X[1], math.log(X[1] / E[0])


def events(rid, cfg, days, early, cal):
    nxt = {a: b for a, b in zip(days[:-1], days[1:])}
    ev = []   # (key, evening date, session, side_hint, extra)
    if rid == "Q-0013":
        df = pd.DataFrame({"d": days}); df["m"] = [d.strftime("%Y-%m") for d in days]
        for m, g in df.groupby("m"):
            ds = list(g["d"])
            if len(ds) < 4:
                continue
            T = len(ds) - 1
            for k, lab in ((T - 3, "T-3"), (T - 2, "T-2"), (T - 1, "T-1"), (T, "T")):
                s = ds[k]
                ev.append(dict(key=s, eve=s - timedelta(days=1), s=s, pos=lab, month=m))
    elif rid == "Q-0014":
        for R, g in cal.groupby("date_local"):
            R = pd.Timestamp(R).date()
            s = nxt.get(R) if R in nxt else next((d for d in days if d > R), None)
            if s is None:
                continue
            row = dict(key=R, eve=R, s=s)
            for _, x in g.iterrows():
                row["delta_" + ("ZC" if x["crop"] == "corn" else "ZS")] = x["delta"]
            ev.append(row)
    else:
        for _, x in cal.iterrows():
            R = pd.Timestamp(x["date_local"]).date()
            if bool(x["holiday_week"]) and R.year < 2025:
                continue
            ev.append(dict(key=R, eve=R - timedelta(days=1), s=R))
    return ev


def compute(rid, bars, days, early, cal, com=60, cost_mult=1.0, entry_h=None, exit_h=None, exit_fb=None, pos_set=None,
            min_abs_delta=None, planted=False):
    cfg = CFG[rid]
    eh = cfg["entry_h"] if entry_h is None else entry_h
    efb = cfg["entry_fb"] if entry_h is None else []
    xh = cfg["exit_h"] if exit_h is None else exit_h
    xfb = cfg["exit_fb"] if exit_fb is None else exit_fb
    # sigma: the same hold over ALL sessions, as-of strictly before each event session
    sig = {}
    for i in cfg["insts"]:
        b = bars[i]; vals = {}
        for s in days:
            h = hold(b, s - timedelta(days=1), s, eh, efb, xh, xfb, cfg["early_skip_exit"] and s in early)
            if h:
                vals[s] = h[2]
        sig[i] = pd.Series(vals).sort_index()
    evs = events(rid, cfg, days, early, cal)
    if pos_set is not None:
        evs = [e for e in evs if e.get("pos") in pos_set]
    elif rid == "Q-0013":
        evs = [e for e in evs if e["pos"] in ("T-2", "T-1", "T")]
    keys = [e["s"] for e in evs]
    sg = {i: kit.ewma_prev(sig[i], com, "std", index=keys).to_numpy() for i in cfg["insts"]}
    rows = []
    for j, e in enumerate(evs):
        r = dict(key=e["key"], s=e["s"], eve=e["eve"], pos=e.get("pos", ""), gross=0.0, cost=0.0, legs=0)
        for i in cfg["insts"]:
            if rid == "Q-0014":
                dl = e.get("delta_" + i)
                if dl is None or pd.isna(dl) or dl == 0 or (min_abs_delta and abs(dl) < min_abs_delta):
                    r["side_" + i] = 0; continue
                side = -int(np.sign(dl))
            else:
                side = 1
            w = kit.VOL_TARGET / sg[i][j] if not np.isnan(sg[i][j]) else np.nan
            if planted:   # planted look-ahead: side from the hold's own return
                hh = hold(bars[i], e["eve"], e["s"], eh, efb, xh, xfb, cfg["early_skip_exit"] and e["s"] in early)
                side = int(np.sign(hh[2])) if hh else 0
            r["side_" + i] = side; r["w_" + i] = w
            if np.isnan(w) or side == 0:
                continue
            h = hold(bars[i], e["eve"], e["s"], eh, efb, xh, xfb, cfg["early_skip_exit"] and e["s"] in early)
            if h is None:
                continue
            pin, pout, ret = h
            r["gross"] += w * side * ret
            r["cost"] += w * (kit.cost_frac(pin, SLIP[i], PV[i], mult=cost_mult) + kit.cost_frac(pout, SLIP[i], PV[i], mult=cost_mult))
            r["legs"] += 1; r["g_" + i] = w * side * ret
        r["net"] = r["gross"] - r["cost"]
        rows.append(r)
    return pd.DataFrame(rows)


def run(rid, stage, dry=False):
    cfg = CFG[rid]
    CUT = "2013-01-01" if dry and rid != "Q-0015" else ("2017-01-01" if dry else cfg["oos_start"])
    windows = ("is",) if (stage == "is" or dry) else ("is", "oos")
    ds = [f"dbn_glbx_1h_{i}" for i in cfg["insts"]]
    bars, _ = kit.load_bars(rid, ds, windows)
    cal = None
    if cfg["cal"]:
        cal = pd.concat([gateway.load(rid, w, dataset=cfg["cal"]) for w in windows], ignore_index=True)
    end = cfg["is_end"] if (stage == "is" or dry) else "2024-12-31"
    days, early = kit.sessions("2010-06-07", end); early = set(early)
    C = lambda **kw: compute(rid, bars, days, early, cal, **kw)
    base = C()
    base = base[base["legs"] > 0].reset_index(drop=True)
    tr = lambda df: df[df["legs"] > 0]
    def terc_series():
        b = bars[cfg["terc_inst"]]; vals = {}
        for s in days:
            h = hold(b, s - timedelta(days=1), s, cfg["entry_h"], cfg["entry_fb"], cfg["exit_h"], cfg["exit_fb"])
            if h: vals[s] = h[2]
        v = pd.Series(vals).sort_index()
        return v.rolling(20).std().shift(1)
    if stage == "is":
        dec = ["side_" + i for i in cfg["insts"]] + ["w_" + i for i in cfg["insts"]]
        entry_of = lambda row, k: (row["eve"], cfg["entry_h"])
        full = C().set_index("key").reset_index()
        h = kit.harness(lambda bb: compute(rid, bb, days, early, cal), bars, "key", entry_of, 30, dec)
        hp = kit.harness(lambda bb: compute(rid, bb, days, early, cal, planted=True), bars, "key", entry_of, 30,
                         ["side_" + i for i in cfg["insts"]])
        tv = terc_series().reindex(base["s"])
        b1, b2 = kit.tercile_bounds(tv)
        res = {"harness": h, "planted": hp, "is_obs": int(len(base)), "is_net_bp": 1e4 * base["net"].mean(),
               "is_t": kit.stats.iid_t(base["net"].to_numpy()), "terciles": [b1, b2]}
        json.dump(res, open(OUT / f"{rid}_is.json", "w"), indent=1, default=str); print(json.dumps(res, indent=1, default=str)); return
    is_info = json.load(open(OUT / f"{rid}_is.json"))
    sel = lambda df: tr(df)[pd.to_datetime(tr(df)["s"]) >= CUT].reset_index(drop=True)
    oos = sel(C())
    cl = [str(x)[:7] for x in oos["s"]] if rid == "Q-0013" else None
    g1 = kit.gate(oos["net"], oos["s"], clusters=cl, nw_lag=cfg["nw"], mean_block=cfg["block"])
    gg = kit.gate(oos["gross"], oos["s"], clusters=cl, nw_lag=cfg["nw"], mean_block=cfg["block"])
    n2 = sel(C(cost_mult=2.0)); g2 = kit.gate(n2["net"], n2["s"], clusters=cl, nw_lag=cfg["nw"], mean_block=cfg["block"])
    yt = kit.years_table(oos["net"], oos["s"])
    b1, b2 = is_info["terciles"]
    tv = terc_series().reindex(oos["s"]).to_numpy()
    terc = pd.Series(np.where(tv < b1, 0, np.where(tv < b2, 1, 2)), index=oos.index); terc[np.isnan(tv)] = -1
    tt = oos.groupby(terc)["net"].agg(["count", "sum", "mean"])
    nb = {}
    if rid == "Q-0013":
        nbk = {"events {T-1, T}": dict(pos_set={"T-1", "T"}), "events {T-3..T}": dict(pos_set={"T-3", "T-2", "T-1", "T"}),
               "exit 14:00 bar close": dict(exit_h=14, exit_fb=[13, 12, 11]), "EWMA com 45": dict(com=45), "EWMA com 75": dict(com=75),
               "one-bar delay: entry 19:00 bar open": dict(entry_h=19)}
    elif rid == "Q-0014":
        nbk = {"exit 09:00 bar close (10:00)": dict(exit_h=9, exit_fb=[]), "exit 13:00 bar close (14:00)": dict(exit_h=13, exit_fb=[12, 11, 10, 9]),
               "|Delta| >= 2 only": dict(min_abs_delta=2), "EWMA com 45": dict(com=45), "EWMA com 75": dict(com=75),
               "one-bar delay: entry 21:00 bar open": dict(entry_h=21)}
    else:
        nbk = {"entry 09:00 bar open on R": dict(entry_h=9), "exit 12:00 bar close (13:00)": dict(exit_h=12, exit_fb=[11]),
               "EWMA com 45": dict(com=45), "EWMA com 75": dict(com=75), "one-bar delay: entry 19:00 bar open": dict(entry_h=19)}
    for k, kw in nbk.items():
        z = sel(C(**kw)) if not (rid == "Q-0015" and k.startswith("entry 09:00")) else sel(q15_day_entry(bars, days, early, cal))
        nb[k] = (int(len(z)), float(z["net"].sum()), float(1e4 * z["net"].mean()), float(kit.stats.iid_t(z["net"].to_numpy())))
    # nulls
    rng = np.random.default_rng(0)
    nulls = {}
    if rid == "Q-0014":
        g = oos["gross"].to_numpy()
        fl = np.array([np.mean(g * rng.choice([-1, 1], size=g.size)) for _ in range(10000)])
        nulls["sign_flip_p"] = float((fl >= g.mean()).mean())
    else:
        # same hold on every OOS session (event or not): non-event mean and a random-date null
        allh = []
        for s in days:
            if pd.Timestamp(s) < pd.Timestamp(CUT): continue
            tot = 0.0; ok = False
            for i in CFG[rid]["insts"]:
                h = hold(bars[i], s - timedelta(days=1), s, cfg["entry_h"], cfg["entry_fb"], cfg["exit_h"], cfg["exit_fb"], cfg["early_skip_exit"] and s in early)
                if h: tot += h[2]; ok = True
            if ok: allh.append((s, tot))
        ah = pd.DataFrame(allh, columns=["s", "r"])
        evset = set(oos["s"])
        ev_r = ah[ah["s"].isin(evset)]["r"]; ne_r = ah[~ah["s"].isin(evset)]["r"]
        se = math.sqrt(ev_r.var() / len(ev_r) + ne_r.var() / len(ne_r))
        nulls["event_minus_nonevent_raw_bp"] = float(1e4 * (ev_r.mean() - ne_r.mean())); nulls["welch_t"] = float((ev_r.mean() - ne_r.mean()) / se)
        nulls["nonevent_mean_raw_bp"] = float(1e4 * ne_r.mean()); nulls["event_mean_raw_bp"] = float(1e4 * ev_r.mean())
        draws = np.array([ah["r"].sample(len(ev_r), random_state=int(k)).mean() for k in rng.integers(0, 2**31, 10000)])
        nulls["random_dates_percentile"] = float((draws < ev_r.mean()).mean())
    sub = {}
    if rid == "Q-0013":
        periods = (("2015-01..2019-10", "2015-01-01", "2019-10-31"), ("2019-11..2024-12", "2019-11-01", "2024-12-31"),
                   ("..2021-01-13 (15:00 strike)", "2015-01-01", "2021-01-13"), ("2021-01-14.. (16:00 strike)", "2021-01-14", "2024-12-31"),
                   ("2022-03.. (hiking)", "2022-03-01", "2024-12-31"))
    elif rid == "Q-0014":
        periods = (("2015-2017", "2015-01-01", "2017-12-31"), ("2018-2024", "2018-01-01", "2024-12-31"))
    else:
        periods = (("2019-2021", "2019-01-01", "2021-12-31"), ("2022-02..", "2022-02-01", "2024-12-31"))
    for nm, a, b in periods:
        m = (pd.to_datetime(oos["s"]) >= a) & (pd.to_datetime(oos["s"]) <= b)
        sub[nm] = (int(m.sum()), float(1e4 * oos.loc[m, "net"].mean()) if m.any() else float("nan"),
                   float(kit.stats.iid_t(oos.loc[m, "net"].to_numpy())) if m.sum() > 2 else float("nan"))
    extra = {}
    if rid == "Q-0013":
        extra["by_inst"] = {i: float(oos.get("g_" + i, pd.Series(dtype=float)).sum()) for i in cfg["insts"]}
        extra["by_pos"] = oos.groupby("pos")["net"].agg(["count", "sum"]).to_dict()
    if rid == "Q-0014":
        extra["by_inst"] = {i: float(oos.get("g_" + i, pd.Series(dtype=float)).sum()) for i in cfg["insts"]}
        mo = pd.to_datetime(oos["s"]).dt.month
        extra["jul_aug_net"] = float(oos.loc[mo.isin([7, 8]), "net"].sum()); extra["other_net"] = float(oos.loc[~mo.isin([7, 8]), "net"].sum())
    if rid == "Q-0015":
        extra["best5_share"] = float(oos["net"].nlargest(5).sum() / oos["net"].sum()) if oos["net"].sum() > 0 else None
    net = oos["net"].sum()
    yrs_pos = int((yt["sum"] > 0).sum()); nyr = len(yt)
    crit7 = bool(net > 0 and yrs_pos >= math.ceil(0.7 * nyr) and yt["sum"].max() <= 0.5 * net
                 and (tt.reindex([0, 1, 2])["sum"].fillna(0) > 0).sum() >= 2 and all(v[1] > 0 for v in nb.values()))
    v = kit.verdict(g1, g2["mean"], crit7)
    years_oos = (pd.Timestamp(oos["s"].max()) - pd.Timestamp(CUT)).days / 365.25
    res = dict(g1=g1, gross=gg, g2=g2, years=yt.to_dict(), terc=tt.to_dict(), neigh=nb, nulls=nulls, sub=sub, extra=extra,
               crit7=crit7, verdict=v, n_obs=int(len(oos)), legs=int(oos["legs"].sum()), years_oos=years_oos)
    tag = "dry" if dry else "oos"
    json.dump(res, open(OUT / f"{rid}_{tag}.json", "w"), indent=1, default=str)
    oos.to_csv(OUT / f"{rid}_{tag}_events.csv", index=False)
    print(json.dumps({k: res[k] for k in ("g1", "g2", "verdict", "crit7", "n_obs", "legs", "nulls")}, indent=1, default=str))


def q15_day_entry(bars, days, early, cal):
    """Q-0015 neighbour: entry at the OPEN of the 09:00 ET bar on the release day R (hold 09:00 -> 15:00)."""
    cfg = CFG["Q-0015"]; b = bars["NG"]
    vals = {}
    for s in days:
        h = hold(b, s, s, 9, [], 14, [13, 12, 11])
        if h: vals[s] = h[2]
    sig = pd.Series(vals).sort_index()
    evs = events("Q-0015", cfg, days, early, cal)
    keys = [e["s"] for e in evs]
    sg = kit.ewma_prev(sig, 60, "std", index=keys).to_numpy()
    rows = []
    for j, e in enumerate(evs):
        r = dict(key=e["key"], s=e["s"], eve=e["s"], pos="", gross=0.0, cost=0.0, legs=0, net=0.0)
        h = hold(b, e["s"], e["s"], 9, [], 14, [13, 12, 11])
        if h and not np.isnan(sg[j]):
            w = kit.VOL_TARGET / sg[j]
            r["gross"] = w * h[2]; r["cost"] = w * (kit.cost_frac(h[0], SLIP["NG"], PV["NG"]) + kit.cost_frac(h[1], SLIP["NG"], PV["NG"]))
            r["legs"] = 1; r["net"] = r["gross"] - r["cost"]
        rows.append(r)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("rid"); ap.add_argument("--stage", required=True); ap.add_argument("--dry", action="store_true")
    a = ap.parse_args(); run(a.rid, a.stage, a.dry)
