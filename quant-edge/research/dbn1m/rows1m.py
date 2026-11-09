"""Event computations for Q-0017..Q-0021, exactly as registered at commit 56c0f6f (research/prereg/Q-00nn.json).

Each compute_* takes {root: Frame}, the list of full XNYS days and a parameter dict, and returns one row per traded
event with: key, date, root, side, entry_et, gross (log return x side, or weighted for Q-0021), cost1 (1x round-trip
cost as a fraction of notional or of account), and the decision columns used by the harness.
`plant=True` builds a deliberately look-ahead version (the harness must catch it).
"""
import numpy as np
import pandas as pd

import kit
import kit1m as K

MIN = np.timedelta64(1, "m")


def _sigma_prev(values, days, com, kind="rms"):
    s = pd.Series(values, index=days)
    return kit.ewma_prev(s, com, kind, min_periods=40, index=days).to_numpy(float)


def _day_frame(ev):
    return pd.DataFrame(ev) if ev else pd.DataFrame(columns=["key", "date", "root", "side", "entry_et", "gross", "cost1"])


# ------------------------------------------------------------------ Q-0017 ES post-close fade
Q17 = dict(k=1.0, entry="16:01", exit_T="16:07", com=60, slip=0.50)


def compute_q17(F, days, p=Q17, plant=False, decide=False):
    es = F["ES"]
    a, ia = es.P(K.at(days, "15:50"))
    b, ib = es.P(K.at(days, "16:00"))
    m = np.where(ia == ib, np.log(b / a), np.nan)
    if plant:  # look-ahead: signal uses the 16:07 price
        c, ic = es.P(K.at(days, "16:07"))
        m = np.where(ia == ic, np.log(c / a), np.nan)
    sig = _sigma_prev(m, days, p["com"])
    e, ie = es.open_at(K.at(days, p["entry"]))
    x, ix = es.P(K.at(days, p["exit_T"]))
    ev = []
    for i, d in enumerate(days):
        if not (np.isfinite(m[i]) and np.isfinite(sig[i]) and abs(m[i]) > p["k"] * sig[i]):
            continue
        if not decide and not (np.isfinite(e[i]) and np.isfinite(x[i]) and ie[i] == ix[i]):
            continue
        side = -np.sign(m[i])
        ev.append(dict(key=str(d), date=d, root="ES", side=side, entry_et=K.at([d], p["entry"])[0],
                       gross=side * np.log(x[i] / e[i]), cost1=K.cost(e[i], p["slip"], "ES") + K.cost(x[i], p["slip"], "ES")))
    return _day_frame(ev)


# ------------------------------------------------------------------ Q-0018 prop-flatten extension fade
Q18 = dict(k=0.5, entry="16:10", exit_T="16:14", com=60, slip=0.50)


def compute_q18(F, days, p=Q18, plant=False, decide=False):
    es = F["ES"]
    o, io = es.open_at(K.at(days, "09:30"))
    c0, i0 = es.P(K.at(days, "16:00"))
    c1, i1 = es.P(K.at(days, "16:10" if not plant else "16:14"))
    D = np.where(io == i0, np.log(c0 / o), np.nan)
    X = np.where(i0 == i1, np.log(c1 / c0), np.nan)
    sig = _sigma_prev(X, days, p["com"])
    e, ie = es.open_at(K.at(days, p["entry"]))
    x, ix = es.P(K.at(days, p["exit_T"]))
    ev = []
    for i, d in enumerate(days):
        if not (np.isfinite(D[i]) and np.isfinite(X[i]) and np.isfinite(sig[i])):
            continue
        if not (np.sign(X[i]) == np.sign(D[i]) and np.sign(D[i]) != 0 and abs(X[i]) > p["k"] * sig[i]):
            continue
        if not decide and not (np.isfinite(e[i]) and np.isfinite(x[i]) and ie[i] == ix[i]):
            continue
        side = -np.sign(D[i])
        ev.append(dict(key=str(d), date=d, root="ES", side=side, entry_et=K.at([d], p["entry"])[0],
                       gross=side * np.log(x[i] / e[i]), cost1=K.cost(e[i], p["slip"], "ES") + K.cost(x[i], p["slip"], "ES")))
    return _day_frame(ev)


def mes_footprint(F, days):
    """Information only: MES share of 16:05-16:09 volume relative to its prior-20-day median."""
    if "MES" not in F:
        return pd.Series(dtype=float)
    v = F["MES"].vol_between(K.at(days, "16:05"), K.at(days, "16:10"))
    s = pd.Series(v, index=days)
    return s / s.rolling(20, min_periods=10).median().shift(1)


# ------------------------------------------------------------------ Q-0020 micro-share open-thrust fade
Q20 = dict(k=1.0, entry="09:35", exit_T="10:00", com=60, q=0.67, slip=0.30, arm="top")


def compute_q20(F, days, p=Q20, plant=False, decide=False):
    es, mes = F["ES"], F["MES"]
    o, io = es.open_at(K.at(days, "09:30"))
    c, ic = es.P(K.at(days, "09:35" if not plant else "09:50"))
    r5 = np.where(io == ic, np.log(c / o), np.nan)
    ve = es.vol_between(K.at(days, "09:30"), K.at(days, "09:35"))
    vm = mes.vol_between(K.at(days, "09:30"), K.at(days, "09:35"))
    s = np.where(ve + vm / 10 > 0, (vm / 10) / (ve + vm / 10), np.nan)
    ss = pd.Series(s, index=days)
    ok_mes = vm > 0
    thr_hi = ss.where(ok_mes).rolling(60, min_periods=40).quantile(p["q"]).shift(1).to_numpy(float)
    thr_lo = ss.where(ok_mes).rolling(60, min_periods=40).quantile(1 / 3).shift(1).to_numpy(float)
    sig = _sigma_prev(r5, days, p["com"])
    e, ie = es.open_at(K.at(days, p["entry"]))
    x, ix = es.P(K.at(days, p["exit_T"]))
    ev = []
    for i, d in enumerate(days):
        if not (np.isfinite(r5[i]) and np.isfinite(sig[i]) and ok_mes[i] and abs(r5[i]) >= p["k"] * sig[i]):
            continue
        gate = (s[i] >= thr_hi[i]) if p["arm"] == "top" else (s[i] <= thr_lo[i])
        if not (np.isfinite(thr_hi[i]) and gate):
            continue
        if not decide and not (np.isfinite(e[i]) and np.isfinite(x[i]) and ie[i] == ix[i]):
            continue
        side = -np.sign(r5[i])
        ev.append(dict(key=str(d), date=d, root="ES", side=side, entry_et=K.at([d], p["entry"])[0],
                       gross=side * np.log(x[i] / e[i]), cost1=K.cost(e[i], p["slip"], "ES") + K.cost(x[i], p["slip"], "ES")))
    return _day_frame(ev)


# ------------------------------------------------------------------ Q-0021 hedging-overshoot reversal (ES, GC)
CLOSE_T = {"ES": "16:00", "GC": "13:30"}
SLIP21 = {"ES": (0.50, 0.30), "GC": (0.20, 0.10)}
Q21 = dict(k=1.5, entry="18:00", com=60, exit_mode="close")


def _minus30(hhmm):
    t = pd.Timestamp("2000-01-01 " + hhmm) - pd.Timedelta(minutes=30)
    return t.strftime("%H:%M")


def compute_q21(F, days, p=Q21, plant=False, all_days=None, decide=False):
    """days = full XNYS sessions; the previous/next session must also be full (all_days gives the calendar order)."""
    cal = list(all_days) if all_days is not None else list(days)
    full = set(days)
    pos = {d: i for i, d in enumerate(cal)}
    ev = []
    for root in ("ES", "GC"):
        if root not in F:
            continue
        f = F[root]
        ct = CLOSE_T[root]
        prev = [cal[pos[d] - 1] if pos[d] > 0 else None for d in days]
        nxt = [cal[pos[d] + 1] if pos[d] + 1 < len(cal) else None for d in days]
        okpn = np.array([pv in full and nx in full for pv, nx in zip(prev, nxt)])
        pc, ipc = f.P(K.at([pv if pv else d for pv, d in zip(prev, days)], ct))
        a, ia = f.P(K.at(days, _minus30(ct)))
        c, ic = f.P(K.at(days, ct))
        rLH = np.where(ia == ic, np.log(c / a), np.nan)
        rROD = np.where(ipc == ia, np.log(a / pc), np.nan)
        e, ie = f.open_at(K.at(days, p["entry"]))
        nx_days = [nx if nx else d for nx, d in zip(nxt, days)]
        xT = ct if p["exit_mode"] == "close" else "10:30"
        x, ix = f.P(K.at(nx_days, xT))
        if plant:  # look-ahead: trigger uses the next-day exit price
            rLH = np.where(ia == ix, np.log(x / a), np.nan)
        hold = np.where((ie == ix) & okpn, np.log(x / e), np.nan)   # every day's 18:00 -> next close, for sigma_h
        sig = _sigma_prev(rLH, days, p["com"], "rms")
        sig_h = _sigma_prev(hold, days, 60, "std")
        slip_in, slip_out = SLIP21[root]
        for i, d in enumerate(days):
            if not okpn[i]:
                continue
            if not (np.isfinite(rLH[i]) and np.isfinite(rROD[i]) and np.isfinite(sig[i]) and np.isfinite(sig_h[i]) and sig_h[i] > 0):
                continue
            if not (np.sign(rLH[i]) == np.sign(rROD[i]) and abs(rLH[i]) > p["k"] * sig[i]):
                continue
            if not decide and not (np.isfinite(e[i]) and np.isfinite(x[i]) and ie[i] == ix[i]):
                continue
            side = -np.sign(rLH[i])
            w = kit.VOL_TARGET / sig_h[i]
            ev.append(dict(key=f"{d}|{root}", date=d, root=root, side=side, entry_et=K.at([d], p["entry"])[0],
                           gross=w * side * np.log(x[i] / e[i]),
                           cost1=w * (K.cost(e[i], slip_in, root) + K.cost(x[i], slip_out, root))))
    return _day_frame(ev)


# ------------------------------------------------------------------ Q-0019 drift-burst fade (ES, GC), long only
Q19 = dict(z=-4.0, vr=2.0, hold=15, delay=1, cool=60)
RTH = {"ES": ("09:30", "16:00", 0.30, 0.50), "GC": ("08:20", "13:30", 0.10, 0.20)}


def burst_features(f):
    """Per-bar z10 and volume ratio for one root (prior-20-session slot RMS and same-minute V10 median)."""
    et = pd.DatetimeIndex(f.et)
    n = len(et)
    gap_ok = np.zeros(n, bool)
    gap_ok[1:] = (np.diff(f.et) == MIN) & (f.iid[1:] == f.iid[:-1])
    r = np.full(n, np.nan)
    r[1:] = np.log(f.close[1:] / f.close[:-1])
    r[~gap_ok] = np.nan
    # session date: bars from 18:00 ET belong to the next calendar day's session
    sess = (et + pd.Timedelta(hours=6)).normalize()
    slot = (et.hour * 2 + et.minute // 30).to_numpy()
    mod = (et.hour * 60 + et.minute).to_numpy()
    df = pd.DataFrame({"sess": sess, "slot": slot, "r2": r ** 2, "rn": np.isfinite(r).astype(float)})
    df["r2"] = df["r2"].fillna(0.0)
    g = df.groupby(["sess", "slot"])[["r2", "rn"]].sum()
    r2 = g["r2"].unstack().fillna(0.0)
    rn = g["rn"].unstack().fillna(0.0)
    has = (rn > 0).astype(float)
    r2s = r2.rolling(20, min_periods=1).sum().shift(1)
    rns = rn.rolling(20, min_periods=1).sum().shift(1)
    hs = has.rolling(20, min_periods=1).sum().shift(1)
    sig_tab = np.sqrt(r2s / rns).where(hs >= 10)
    sess_idx = sig_tab.index.get_indexer(sess)
    slot_idx = sig_tab.columns.get_indexer(slot)
    sig_slot = sig_tab.to_numpy()[sess_idx, slot_idx]
    # 10-bar windows of consecutive valid returns
    valid = np.isfinite(r)
    run = np.zeros(n, int)
    for i in range(1, n):  # numpy loop is fine at ~6M bars
        run[i] = run[i - 1] + 1 if valid[i] else 0
    cs = np.concatenate([[0.0], np.cumsum(np.where(valid, r, 0.0))])
    sum10 = np.full(n, np.nan)
    idx = np.arange(n)
    ok = run >= 10
    sum10[ok] = cs[idx[ok] + 1] - cs[idx[ok] + 1 - 10]
    z10 = sum10 / (sig_slot * np.sqrt(10))
    cv = np.concatenate([[0.0], np.cumsum(f.vol)])
    v10 = np.full(n, np.nan)
    v10[ok] = cv[idx[ok] + 1] - cv[idx[ok] + 1 - 10]
    vt = pd.DataFrame({"sess": sess, "mod": mod, "v": v10}).dropna()
    vp = vt.pivot_table(index="sess", columns="mod", values="v", aggfunc="last")
    med = vp.rolling(20, min_periods=10).median().shift(1)
    mi = med.index.get_indexer(sess)
    mj = med.columns.get_indexer(mod)
    medv = np.where((mi >= 0) & (mj >= 0), med.to_numpy()[np.clip(mi, 0, None), np.clip(mj, 0, None)], np.nan)
    vr = v10 / medv
    return {"z10": z10, "vr": vr, "sess": sess}


def compute_q19(F, days=None, p=Q19, plant=False, feats=None, roots=("ES", "GC"), decide=False):
    ev = []
    for root in roots:
        if root not in F:
            continue
        f = F[root]
        ft = feats[root] if feats is not None else burst_features(f)
        z10, vr = ft["z10"], ft["vr"]
        if plant:  # look-ahead: trigger on the burst measured 10 bars later
            z10 = np.concatenate([z10[10:], np.full(10, np.nan)])
        cand = np.where((z10 <= p["z"]) & (vr >= p["vr"]))[0]
        last_entry = None
        rs, re_, sin, sout = RTH[root]
        for t in cand:
            ti = t + p["delay"]
            if decide:  # decision only: the nominal entry instant, no use of bars at/after it
                ent = f.et[t] + p["delay"] * MIN
            else:
                if ti >= len(f.et):
                    continue
                ent = f.et[ti]
                if f.et[ti] - f.et[t] > 5 * MIN:
                    continue
            ets = pd.Timestamp(ent)
            hm = ets.hour * 60 + ets.minute
            if 16 * 60 <= hm < 18 * 60 + 30:
                continue
            if ets.weekday() == 4 and hm >= 16 * 60:
                continue
            if last_entry is not None and ent - last_entry < p["cool"] * MIN:
                continue
            T_exit = f.et[t] + (p["hold"] + 1) * MIN
            if decide:
                last_entry = ent
                ev.append(dict(key=f"{root}|{str(ent)}", date=ets.date(), root=root, side=1.0, entry_et=ent, gross=np.nan, cost1=np.nan))
                continue
            x, ix = f.exit_px(np.array([T_exit]))
            e, ie = f.open[ti], f.iid[ti]
            if not (np.isfinite(x[0]) and ix[0] == ie):
                continue
            xt = pd.Timestamp(T_exit)

            def inside(ts):
                m = ts.hour * 60 + ts.minute
                a = int(rs[:2]) * 60 + int(rs[3:]); b = int(re_[:2]) * 60 + int(re_[3:])
                return a <= m < b
            c1 = K.cost(e, sin if inside(ets) else sout, root) + K.cost(x[0], sin if inside(xt) else sout, root)
            last_entry = ent
            ev.append(dict(key=f"{root}|{str(ent)}", date=ets.date(), root=root, side=1.0, entry_et=ent,
                           gross=np.log(x[0] / e), cost1=c1, burst_et=f.et[t]))
    return _day_frame(ev)
