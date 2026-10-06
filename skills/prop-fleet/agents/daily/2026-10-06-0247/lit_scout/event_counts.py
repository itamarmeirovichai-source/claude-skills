"""Literature scout 2026-10-06: EVENT FREQUENCY and SCALE only. No strategy P&L.

Nothing here conditions a forward return on a signal direction, so nothing here
spends N. It answers one screening question per candidate: how many trades a
year would the published rule produce on ES, and how big are the moves in ES
points next to the board's 0.6 pt round trip and >=15 pt stop screen.

Input: ES 1m RTH 2008-01-02..2026-04-10 (FirstRate via jimmuell/mes-orb-strategy@48993b9,
       sha256 093596df077abd90feac0c6f18d65626c718580969a3c36e97116e01b4737b9e,
       fetched by daily/2026-10-05/data_hunter/data_fetch_more.py). Licence: research only.

C1 Shum-Hejazi-Haryanto-Rodier (RoF 2016) LETF late-day rule: days where the S&P
   move from the PRIOR session's last bar close to the 14:44 bar close is >= 2% in
   absolute value (the paper's 2% threshold at 2:45 pm). Counts per year only.
C2 Kurov-Sancetta-Strasser-Wolfe (JFQA 2019) 10:00 ET releases, approximated by
   rule (NOT a verified calendar): ISM manufacturing = first session of the month,
   ISM services = third session of the month, Conference Board consumer
   confidence = last Tuesday of the month. Counts per year; median |09:30->09:59|
   and |10:00->10:29| in ES points on those days vs all other days (unsigned scale).
C3 Christensen-Oomen-Reno (JoE 2022) drift-burst statistic, CRUDE 1m PROXY:
   left-sided exponential kernel, mean bandwidth 5 (and 15) bars, variance bandwidth 5x that,
   no pre-averaging, T = sqrt(h_mu / K2) * mu_hat / sigma_hat. Episodes = first bar of a
   run with |T| > 4.5 (paper's critical value), at most one per 30 minutes per day.
   Counts per year, split by sign. Not the paper's tick-data test.
Usage: python event_counts.py <es_1m_rth.parquet>
"""
import hashlib
import sys

import numpy as np
import pandas as pd

P = sys.argv[1]
h = hashlib.sha256(open(P, "rb").read()).hexdigest()
assert h.startswith("093596df"), h
es = pd.read_parquet(P)
es = es[es.index.dayofweek < 5]
es["day"] = es.index.normalize()
tm = es.index.strftime("%H:%M")
print("ES 1m RTH rows %d, sessions %d, %s..%s" % (len(es), es["day"].nunique(), es.index[0].date(), es.index[-1].date()))

g = es.groupby("day")
last = g["Close"].last()
prev_last = last.shift(1)

# C1
c1444 = es[tm == "14:44"].set_index("day")["Close"]
r = (c1444 / prev_last.reindex(c1444.index) - 1).dropna()
big = r[r.abs() >= 0.02]
yrs = r.index.year
print("\nC1 |prior close -> 14:44| >= 2%%: %d of %d sessions (%.1f%%)" % (len(big), len(r), 100 * len(big) / len(r)))
print("   by year:", big.groupby(big.index.year).size().reindex(sorted(set(yrs)), fill_value=0).to_dict())
print("   up %d / down %d" % ((big > 0).sum(), (big < 0).sum()))

# C2
days = pd.Series(sorted(es["day"].unique()))
ym = days.dt.to_period("M")
rank = days.groupby(ym).cumcount() + 1
ism_m = set(days[rank == 1])
ism_s = set(days[rank == 3])
tues = days[days.dt.dayofweek == 1]
cb = set(tues.groupby(tues.dt.to_period("M")).max())
ev = ism_m | ism_s | cb
o930 = es[tm == "09:30"].set_index("day")["Open"]
c959 = es[tm == "09:59"].set_index("day")["Close"]
o1000 = es[tm == "10:00"].set_index("day")["Open"]
c1029 = es[tm == "10:29"].set_index("day")["Close"]
pre = (c959 - o930).abs().dropna()
post = (c1029 - o1000).abs().dropna()
isev = pd.Series(pre.index.isin(list(ev)), index=pre.index)
isev_p = pd.Series(post.index.isin(list(ev)), index=post.index)
print("\nC2 rule-based 10:00 release days: ISM-M %d, ISM-S %d, CB %d, union %d over %d sessions" % (len(ism_m), len(ism_s), len(cb), len(ev), len(days)))
print("   union per year mean %.1f" % (len(ev) / (len(days) / 252)))
print("   median |09:30->09:59| ES pt: event %.2f  other %.2f" % (pre[isev].median(), pre[~isev].median()))
print("   median |10:00->10:29| ES pt: event %.2f  other %.2f" % (post[isev_p].median(), post[~isev_p].median()))
for y0, y1 in [(2008, 2014), (2015, 2019), (2020, 2026)]:
    m = (pre.index.year >= y0) & (pre.index.year <= y1)
    mp = (post.index.year >= y0) & (post.index.year <= y1)
    print("   %d-%d median |pre| event %.2f other %.2f ; |post| event %.2f other %.2f" % (
        y0, y1, pre[m & isev].median(), pre[m & ~isev].median(), post[mp & isev_p].median(), post[mp & ~isev_p].median()))

# C3
# Paper's estimators (exponential left kernel, K2 = int K^2 = 1/2):
#   mu_hat = (1/h) sum_j exp(-(i-j)/h) r_j ; s2_hat = (1/h') sum_j exp(-(i-j)/h') r_j^2
#   T = sqrt(h / K2) * mu_hat / sqrt(s2_hat)
# h_mu = 5 bars mirrors the paper's 300 s mean bandwidth with h_var = 5 h_mu, but on
# 1m bars without pre-averaging; h_mu = 15 bars is a second, coarser stand-in.
# Both are frequency-only proxies, NOT the paper's tick-data test.
lr = np.log(es["Close"]).groupby(es["day"]).diff()


def episodes(hm, hv, crit=4.5):
    am, av = np.exp(-1 / hm), np.exp(-1 / hv)
    out = []
    for d, x in lr.groupby(es["day"]):
        v = x.fillna(0.0).to_numpy()
        Sm = Sv = 0.0
        last_ep = -10**9
        prev_hit = False
        idx = x.index
        for i, ri in enumerate(v):
            Sm = am * Sm + ri
            Sv = av * Sv + ri * ri
            if i < hv or Sv <= 0:
                continue
            T = np.sqrt(hm / 0.5) * (Sm / hm) / np.sqrt(Sv / hv)
            hit = abs(T) > crit
            if hit and not prev_hit and i - last_ep >= 30:
                out.append((idx[i], np.sign(T)))
                last_ep = i
            prev_hit = hit
    E = pd.DataFrame(out, columns=["t", "sign"])
    E["t"] = pd.to_datetime(E["t"])
    return E


for hm, hv in [(5, 25), (15, 75)]:
    E = episodes(hm, hv)
    print("\nC3 drift-burst proxy h_mu=%d h_var=%d bars, |T|>4.5: %d episodes over %d sessions (%.1f/yr)" % (hm, hv, len(E), len(days), len(E) / (len(days) / 252)))
    if len(E):
        print("   positive %d negative %d" % ((E.sign > 0).sum(), (E.sign < 0).sum()))
        print("   by year:", E.groupby(E.t.dt.year).size().to_dict())
