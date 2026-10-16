#!/usr/bin/env python3
"""D4 independent verifier. Re-implements prereg/D4-spec.md from the text only
(does not read or import breadth.py / strategies.py / common.py).

    python3 verify.py > verify_run.txt
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(os.environ.get(
    "D4_DATA",
    "/tmp/claude-0/-home-user-claude-skills/ab16f964-5383-5ce9-9236-930cb9242b15/scratchpad/w1-breadth"))

# market: (O, C, tz, cost/side bp, source)
MK = {
    "EUR_USD": ("08:00", "16:00", "Europe/London", 0.5, "oanda"),
    "GBP_USD": ("08:00", "16:00", "Europe/London", 0.7, "oanda"),
    "USD_CAD": ("08:00", "16:00", "Europe/London", 0.8, "oanda"),
    "AUD_USD": ("08:00", "16:00", "Europe/London", 0.7, "oanda"),
    "EUR_JPY": ("08:00", "16:00", "Europe/London", 0.8, "oanda"),
    "AUD_JPY": ("08:00", "16:00", "Europe/London", 0.9, "oanda"),
    "SPX500_USD": ("09:30", "16:00", "America/New_York", 1.0, "oanda"),
    "NAS100_USD": ("09:30", "16:00", "America/New_York", 1.0, "oanda"),
    "US2000_USD": ("09:30", "16:00", "America/New_York", 1.5, "oanda"),
    "UK100_GBP": ("08:00", "16:30", "Europe/London", 1.0, "oanda"),
    "FR40_EUR": ("09:00", "17:30", "Europe/Paris", 1.0, "oanda"),
    "NL25_EUR": ("09:00", "17:30", "Europe/Amsterdam", 1.5, "oanda"),
    "JP225_USD": ("09:00", "15:00", "Asia/Tokyo", 1.5, "oanda"),
    "AU200_AUD": ("10:00", "16:00", "Australia/Sydney", 1.2, "oanda"),
    "GRXEUR": ("09:00", "17:30", "Europe/Berlin", 0.8, "histdata"),
    "ETXEUR": ("09:00", "17:30", "Europe/Berlin", 1.5, "histdata"),
    "XAU_USD": ("08:20", "13:30", "America/New_York", 1.0, "oanda"),
    "WTICO_USD": ("09:00", "14:30", "America/New_York", 2.5, "oanda"),
    "NATGAS_USD": ("09:00", "14:30", "America/New_York", 8.0, "oanda"),
    "CORN_USD": ("08:30", "13:15", "America/Chicago", 10.0, "oanda"),
    "SOYBN_USD": ("08:30", "13:15", "America/Chicago", 6.0, "oanda"),
    "WHEAT_USD": ("08:30", "13:15", "America/Chicago", 10.0, "oanda"),
    "SUGAR_USD": ("03:30", "13:00", "America/New_York", 10.0, "oanda"),
}
IS_END = pd.Timestamp("2012-12-31")
OOS_START, OOS_END = pd.Timestamp("2013-01-01"), pd.Timestamp("2020-05-13")
RULES = ["D4-01", "D4-02", "D4-03", "D4-04"]
EPOCH = np.datetime64("1970-01-01T00:00", "m")


def hm(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


class Bars:
    def __init__(self, df):
        self.t = ((df.index.values.astype("datetime64[m]") - EPOCH).astype(np.int64))
        self.o = df["o"].values.astype(float)
        self.h = df["h"].values.astype(float)
        self.l = df["l"].values.astype(float)
        self.c = df["c"].values.astype(float)
        tp = (self.h + self.l + self.c) / 3.0
        self.cum_tp = np.concatenate([[0.0], np.cumsum(tp)])

    def mark(self, T):
        """close of last bar with open in [T-10, T-1]; nan if none (vectorised)."""
        T = np.asarray(T)
        i = np.searchsorted(self.t, T, "left") - 1
        ok = (i >= 0)
        ic = np.clip(i, 0, len(self.t) - 1)
        ok &= self.t[ic] >= T - 10
        return np.where(ok, self.c[ic], np.nan)

    def fill(self, T):
        """open of first bar with open in [T, T+10]; nan if none."""
        T = np.asarray(T)
        i = np.searchsorted(self.t, T, "left")
        ok = i < len(self.t)
        ic = np.clip(i, 0, len(self.t) - 1)
        ok &= self.t[ic] <= T + 10
        return np.where(ok, self.o[ic], np.nan)

    def fill_idx(self, T):
        i = int(np.searchsorted(self.t, T, "left"))
        if i < len(self.t) and self.t[i] <= T + 10:
            return i
        return -1

    def twap(self, O, T):
        a = np.searchsorted(self.t, O, "left")
        b = np.searchsorted(self.t, T, "left")
        n = b - a
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.where(n > 0, (self.cum_tp[b] - self.cum_tp[a]) / np.maximum(n, 1), np.nan)


def utc_minutes(dates, hhmm, tz):
    loc = pd.DatetimeIndex(dates) + pd.Timedelta(minutes=hm(hhmm))
    u = loc.tz_localize(tz, ambiguous="raise", nonexistent="raise").tz_convert("UTC").tz_localize(None)
    return ((u.values.astype("datetime64[m]") - EPOCH).astype(np.int64))


def build_sessions(m):
    Os, Cs, tz, cost, src = MK[m]
    df = pd.read_parquet(DATA / f"{m}.parquet")
    B = Bars(df)
    first = df.index[0].tz_localize("UTC").tz_convert(tz).normalize().tz_localize(None) - pd.Timedelta(days=1)
    last = df.index[-1].tz_localize("UTC").tz_convert(tz).normalize().tz_localize(None) + pd.Timedelta(days=1)
    dates = pd.bdate_range(first, last)  # weekdays only
    O = utc_minutes(dates, Os, tz)
    C = utc_minutes(dates, Cs, tz)
    S = pd.DataFrame(index=dates)
    S["O"], S["C"] = O, C
    S["MO"] = B.mark(O)
    if os.environ.get("D4_MO_FALLBACK"):  # sensitivity only, not the literal spec
        S["MO"] = S["MO"].fillna(pd.Series(B.fill(O), index=dates))
    S["MO30"] = B.mark(O + 30)
    S["MC"] = B.mark(C)
    S["FO30"] = B.fill(O + 30)
    S["FC30"] = B.fill(C - 30)
    S["valid"] = S[["MO30", "MC", "FO30"]].notna().all(axis=1)
    S = S[S.index <= (OOS_END if src == "oanda" else pd.Timestamp("2018-12-31"))]
    # drop dates before any data (they are invalid anyway); keep all for simplicity
    S["lr"] = np.log(S["MC"] / S["MO"])
    V = S[S["valid"]].copy()
    # previous close: M(C) of most recent earlier valid session within 5 calendar days
    prev_mc = V["MC"].shift(1)
    prev_d = pd.Series(V.index, index=V.index).shift(1)
    gap = (pd.Series(V.index, index=V.index) - prev_d).dt.days
    V["Cprev"] = np.where(gap <= 5, prev_mc, np.nan)
    # sigma-hat: sd of lr over previous 60 valid sessions, >=40 non-missing
    V["sig"] = V["lr"].shift(1).rolling(60, min_periods=40).std(ddof=1)
    return B, S, V, cost / 1e4


def trade_rows(B, V, cost, which):
    """Return dict rule -> (net r, gross r) Series indexed by date (trades only)
    and a list of trade records for spot checks."""
    out = {r: {} for r in RULES}
    recs = []
    for d, row in V.iterrows():
        sig = row["sig"]
        if not np.isfinite(sig) or sig <= 0:
            continue
        O, C = int(row["O"]), int(row["C"])
        # D4-01 / D4-02
        if np.isfinite(row["Cprev"]):
            s = np.sign(np.log(row["MO30"]) - np.log(row["Cprev"]))
            if s != 0:
                if np.isfinite(row["FC30"]):
                    g = s * (row["MC"] - row["FC30"]) / row["FC30"]
                    out["D4-01"][d] = (g, 2 * cost, sig)
                    recs.append(("D4-01", d, s, C - 30, row["FC30"], C, row["MC"], g))
                g = s * (row["MC"] - row["FO30"]) / row["FO30"]
                out["D4-02"][d] = (g, 2 * cost, sig)
                recs.append(("D4-02", d, s, O + 30, row["FO30"], C, row["MC"], g))
        # D4-03 TWAP
        Tk = np.arange(O + 30, C - 30 + 1, 30)
        Mk = B.mark(Tk)
        Wk = B.twap(np.full(len(Tk), O), Tk)
        Fk = B.fill(Tk)
        pos, ent, et, g, nsides = 0, np.nan, 0, 0.0, 0
        segs = []
        for T, mk, w, f in zip(Tk, Mk, Wk, Fk):
            if not np.isfinite(mk) or not np.isfinite(w):
                continue
            des = 1 if mk > w else (-1 if mk < w else pos)
            if des == pos or not np.isfinite(f):
                continue
            if pos != 0:
                g += pos * (f - ent) / ent
                nsides += 1
                segs.append((pos, ts(et), float(ent), ts(T), float(f)))
            pos, ent, et = des, f, T
            nsides += 1
        if pos != 0:
            g += pos * (row["MC"] - ent) / ent
            nsides += 1
            segs.append((pos, ts(et), float(ent), "M(" + ts(C) + ")", float(row["MC"])))
        if nsides > 0:
            out["D4-03"][d] = (g, nsides * cost, sig)
            recs.append(("D4-03", d, segs, nsides, g))
        # D4-04 ORB
        a = np.searchsorted(B.t, O, "left")
        b30 = np.searchsorted(B.t, O + 30, "left")
        e = np.searchsorted(B.t, C - 30, "left")
        cE = np.searchsorted(B.t, C, "left")
        if b30 > a and e > b30:
            orh, orl = B.h[a:b30].max(), B.l[a:b30].min()
            cc = B.c[b30:e]
            hit = np.nonzero((cc > orh) | (cc < orl))[0]
            if len(hit):
                k = b30 + hit[0]
                side = 1 if B.c[k] > orh else -1
                fi = B.fill_idx(int(B.t[k]) + 1)
                if fi >= 0:
                    entry = B.o[fi]
                    stop = orl if side == 1 else orh
                    ex, ext, why = np.nan, None, "close"
                    for j in range(fi, cE):
                        if side == 1:
                            if B.o[j] <= stop:
                                ex, ext, why = B.o[j], B.t[j], "gap-stop"; break
                            if B.l[j] <= stop:
                                ex, ext, why = stop, B.t[j], "stop"; break
                        else:
                            if B.o[j] >= stop:
                                ex, ext, why = B.o[j], B.t[j], "gap-stop"; break
                            if B.h[j] >= stop:
                                ex, ext, why = stop, B.t[j], "stop"; break
                    if not np.isfinite(ex):
                        ex, ext = row["MC"], C
                    g4 = side * (ex - entry) / entry
                    out["D4-04"][d] = (g4, 2 * cost, sig)
                    recs.append(("D4-04", d, side, int(B.t[fi]), entry, int(ext), ex, g4, why, orh, orl))
    res = {}
    for r in RULES:
        if out[r]:
            df = pd.DataFrame.from_dict(out[r], orient="index", columns=["g", "c", "sig"])
        else:
            df = pd.DataFrame(columns=["g", "c", "sig"], dtype=float)
        res[r] = df
    return res, recs


def nw_t(x, L=5):
    x = np.asarray(x, float)
    n = len(x)
    e = x - x.mean()
    s = e @ e / n
    for k in range(1, L + 1):
        s += 2 * (1 - k / (L + 1)) * (e[k:] @ e[:-k]) / n
    return x.mean() / np.sqrt(s / n)


def stats(x):
    x = np.asarray(x, float)
    m, sd, n = x.mean(), x.std(ddof=1), len(x)
    return m, m / (sd / np.sqrt(n)), nw_t(x), m / sd * np.sqrt(252), n


def ts(minutes):
    return str(EPOCH + np.timedelta64(int(minutes), "m"))


def main():
    sess = {}
    print("== Eligibility (sec 3) ==")
    elig = []
    for m in MK:
        B, S, V, cost = build_sessions(m)
        sess[m] = (B, S, V, cost)
        Vis = V[V.index <= IS_END]
        n_is = len(Vis)
        sig_is = Vis["lr"].std(ddof=1) * 1e4
        ok = n_is >= 250 and 2 * cost * 1e4 <= 0.10 * sig_is
        print(f"{m:11s} IS valid={n_is:5d} sigma_IS={sig_is:7.1f}bp  RT cost={2*cost*1e4:5.1f}bp "
              f"ratio={2*cost*1e4/sig_is:5.3f}  all valid={len(V):5d}  {'ELIGIBLE' if ok else 'dropped'}")
        if ok:
            elig.append(m)
    elig_oanda = sorted(m for m in elig if MK[m][4] == "oanda")
    draw = list(np.random.default_rng(20261011).choice(elig_oanda, 4, replace=False))
    H = [m for m in ["GRXEUR", "ETXEUR"] if m in elig] + [str(x) for x in draw]
    D = [m for m in elig if m not in H]
    print("eligible:", elig)
    print("H:", H)
    print("D:", D)

    # per-market daily u series
    per = {}  # (m, rule) -> DataFrame with g,c,sig
    allrecs = {}
    for m in elig:
        B, S, V, cost = sess[m]
        Vm = V if m in D else V[V.index >= OOS_START]  # held-out: nothing computed in IS
        res, recs = trade_rows(B, Vm, cost, m)
        allrecs[m] = recs
        for r in RULES:
            per[(m, r)] = res[r]

    def basket(mkts, lo, hi, rule, costmult=1.0, gross=False):
        dates = set()
        for m in mkts:
            V = sess[m][2]
            dates |= set(V.index[(V.index >= lo) & (V.index <= hi)])
        idx = pd.DatetimeIndex(sorted(dates))
        tot = pd.Series(0.0, index=idx)
        rules = RULES if rule == "D4-05" else [rule]
        for rr in rules:
            sub = pd.Series(0.0, index=idx)
            for m in mkts:
                df = per[(m, rr)]
                df = df[(df.index >= lo) & (df.index <= hi)]
                if len(df) == 0:
                    continue
                r = df["g"] - (0 if gross else costmult * df["c"])
                u = r * 0.01 / df["sig"]
                sub = sub.add(u.reindex(idx).fillna(0.0), fill_value=0.0)
            tot += sub / len(mkts)
        return tot / len(rules)

    if os.environ.get("D4_MO_FALLBACK"):
        print("!! SENSITIVITY RUN: missing M(O) replaced by F(O) -- not the literal spec")
    print("\n== Results (x100 = percent per day) ==")
    hdr = (f"{'variant':7s} {'OOS net mean':>12s} {'iid t':>7s} {'NW t':>7s} {'Sharpe':>7s} {'n':>5s} "
           f"{'cost2 mean':>11s} {'cost2 t*':>8s} {'H OOS net':>10s} {'D IS gross':>11s}")
    print(hdr)
    B_all = D + H
    for v in RULES + ["D4-05"]:
        x = basket(B_all, OOS_START, OOS_END, v)
        m, ti, tn, sh, n = stats(x)
        x2 = basket(B_all, OOS_START, OOS_END, v, costmult=2.0)
        m2, ti2, tn2, _, _ = stats(x2)
        h = basket(H, OOS_START, OOS_END, v).mean()
        gi = basket(D, pd.Timestamp("2005-01-01"), IS_END, v, gross=True).mean()
        print(f"{v:7s} {m*100:12.5f} {ti:7.2f} {tn:7.2f} {sh:7.2f} {n:5d} {m2*100:11.5f} "
              f"{min(ti2, tn2):8.2f} {h*100:10.5f} {gi*100:11.5f}")
    print("(cost2 t* = min(iid, NW) t at cost x2)")

    print("\n== trade counts OOS per market ==")
    for m in B_all:
        cnt = [len(per[(m, r)][per[(m, r)].index >= OOS_START]) for r in RULES]
        print(f"{m:11s}", cnt)

    print("\n== Spot checks (bar times UTC = bar OPEN time; M(T) = close of bar opening <= T-1) ==")
    picks = [("EUR_USD", "D4-01", "2015-03-10"), ("SPX500_USD", "D4-02", "2016-06-24"),
             ("FR40_EUR", "D4-04", "2014-10-15"), ("XAU_USD", "D4-03", "2013-04-15"),
             ("UK100_GBP", "D4-04", "2018-02-05")]
    for m, r, ds in picks:
        if m not in allrecs:
            print(m, "not eligible"); continue
        d0 = pd.Timestamp(ds)
        cand = [x for x in allrecs[m] if x[0] == r and x[1] >= d0]
        if not cand:
            print(m, r, "no trade"); continue
        x = cand[0]
        sig = sess[m][2].loc[x[1], "sig"]
        cost = sess[m][3]
        if r in ("D4-01", "D4-02", "D4-04"):
            extra = f" {x[8]} ORH={x[9]} ORL={x[10]}" if r == "D4-04" else ""
            print(f"{m} {r} {x[1].date()} side={int(x[2]):+d} entry {ts(x[3])} @ {x[4]}  exit "
                  f"{'mark M('+ts(x[5])+')' if r!='D4-04' else ts(x[5])} @ {x[6]}  gross={x[7]*1e4:.2f}bp "
                  f"net={(x[7]-2*cost)*1e4:.2f}bp sig={sig:.5f} u={(x[7]-2*cost)*0.01/sig*100:.4f}%{extra}")
        else:
            print(f"{m} {r} {x[1].date()} segments(side,entry t,entry px,exit t,exit px)={x[2]} sides={x[3]} gross={x[4]*1e4:.2f}bp "
                  f"net={(x[4]-x[3]*cost)*1e4:.2f}bp")


if __name__ == "__main__":
    main()
