"""Verifier S2: H0022 (30-min VWAP trend) on NQ, re-implemented from the ledger row H0022,
references/vwap30-H0022.md and F1-00 only. Writes per-session gross P&L (points), units, first
entry price, position flag to a parquet in the scratchpad (data never committed).

usage: python3 s2_nq.py <scratch_dir>
"""
import sys
import numpy as np
import pandas as pd

SCR = sys.argv[1]
SPLIT_LAST_1M = pd.Timestamp("2025-11-21").date()   # 1m through here, 5m afterwards (F1-00)


def roll_excluded(years):
    out = set()
    for y in years:
        for m in (3, 6, 9, 12):
            first = pd.Timestamp(y, m, 1)
            fri3 = first + pd.Timedelta(days=(4 - first.weekday()) % 7 + 14)
            mon = fri3 - pd.Timedelta(days=4)
            for i in range(5):
                out.add((mon + pd.Timedelta(days=i)).date())
            out.add((fri3 + pd.Timedelta(days=3)).date())
    return out


def rth(d, bar_minutes):
    t = d.index
    hm = t.hour * 100 + t.minute
    last = 1559 if bar_minutes == 1 else 1555
    r = d[(hm >= 930) & (hm <= last) & (t.dayofweek < 5)].copy()
    r["date"] = r.index.date
    return r


def session(df):
    """df: one session's RTH bars (o,h,l,c,v) sorted. Returns gross pts, units, first entry px, any_pos."""
    t = df.index
    o, h, l, c, v = (df[k].to_numpy(float) for k in "ohlcv")
    tp = (h + l + c) / 3.0
    cv = np.cumsum(v)
    vwap = np.where(cv > 0, np.cumsum(tp * v) / np.where(cv > 0, cv, 1), np.nan)
    mins = (t.hour * 60 + t.minute).to_numpy() - 570          # minutes since 09:30
    slot = np.where(mins < 360, mins // 30, -1)                 # 09:30..15:29 -> 0..11
    n = len(df)
    pos = np.zeros(n)                                           # position held during bar j
    cur = 0.0
    for j in range(n):
        pos[j] = cur
        # is bar j the last bar of its slot? (next bar outside the slot, or no next bar)
        if slot[j] >= 0 and (j == n - 1 or slot[j + 1] != slot[j]):
            if j == n - 1:
                continue                                       # session's last bar: flat anyway
            if c[j] > vwap[j]:
                cur = 1.0
            elif c[j] < vwap[j]:
                cur = -1.0
        # cur takes effect at the next bar's open
    # P&L: within-bar + gap between bars; flat at last close
    pnl = np.sum(pos * (c - o)) + np.sum(pos[:-1] * (o[1:] - c[:-1])) if n > 1 else pos[0] * (c[0] - o[0])
    # units: changes in position at bar opens, plus the final exit
    ext = np.concatenate([[0.0], pos, [0.0]])
    units = np.sum(np.abs(np.diff(ext)))
    nz = np.nonzero(pos)[0]
    first_px = o[nz[0]] if len(nz) else np.nan
    return pnl, units, first_px, float(len(nz) > 0)


def run(d, bar_minutes, keep):
    r = rth(d, bar_minutes)
    rows = []
    for dt, g in r.groupby("date", sort=True):
        if not keep(dt):
            continue
        pnl, u, px, anyp = session(g)
        rows.append((dt, pnl, u, px, anyp, g["c"].iloc[-1], len(g)))
    return pd.DataFrame(rows, columns=["date", "gross_pts", "units", "px", "anypos", "close", "nbars"]).set_index("date")


def main():
    m1 = pd.read_parquet(f"{SCR}/data/intraday/nq_1m.parquet")
    m1 = m1.rename(columns={"DateTime_ET": "dt", "Open": "o", "High": "h", "Low": "l", "Close": "c", "Volume": "v"})
    m1 = m1.set_index("dt").sort_index()
    m1 = m1[~m1.index.duplicated()][list("ohlcv")].astype(float)
    m5 = pd.read_csv(f"{SCR}/data/intraday/nq_5m.csv")
    t = pd.to_datetime(m5["datetime"], utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
    m5 = m5.rename(columns={"open": "o", "high": "h", "low": "l", "close": "c", "volume": "v"})
    m5.index = t
    m5 = m5.sort_index()
    m5 = m5[~m5.index.duplicated()][list("ohlcv")].astype(float)

    a = run(m1, 1, lambda d: d <= SPLIT_LAST_1M)
    a["src"] = "1m"
    b = run(m5, 5, lambda d: d > SPLIT_LAST_1M)
    b["src"] = "5m"
    chk = run(m5, 5, lambda d: d <= SPLIT_LAST_1M)          # data check: 5m over the 1m period
    s = pd.concat([a, b])
    rx = roll_excluded(range(2020, 2027))
    s["roll"] = [d in rx for d in s.index]
    chk["roll"] = [d in rx for d in chk.index]
    s.to_parquet(f"{SCR}/verify_s2.parquet")
    chk.to_parquet(f"{SCR}/verify_s2_5mcheck.parquet")
    print(s.groupby("src").size(), s.roll.sum(), s.index.min(), s.index.max())
    print("5m-check sessions", len(chk), chk.index.min(), chk.index.max())


if __name__ == "__main__":
    main()
