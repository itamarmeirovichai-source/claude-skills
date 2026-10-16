#!/usr/bin/env python3
"""D4 data check (outcome-free: no strategy returns).

1. Clock: for each market, mean |1m log return| by UTC minute-of-day, separately for Jan-Feb
   (no DST anywhere north) and Jul-Aug (DST in US/EU). The exchange open of each market should
   show a spike at its local open converted to UTC. We print the top-3 spike minutes per
   season and the expected UTC minute of the open in that season.
2. Gaps: per market, valid sessions per year (spec definition), median bars inside [O, C),
   share of sessions with < 50% of the minutes present.

    python3 data_check.py > data_check.txt
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import MARKETS, load, sessions


def spikes(d: pd.DataFrame, months):
    x = d[d.index.month.isin(months) & (d.index.weekday < 5)]
    r = np.log(x.c).diff().abs()
    r[(x.index.to_series().diff() != pd.Timedelta(minutes=1)).values] = np.nan
    g = r.groupby(x.index.hour * 60 + x.index.minute).mean()
    return g.sort_values(ascending=False)


def expected_open_utc(m, month):
    o, _, tz = MARKETS[m][0], MARKETS[m][1], MARKETS[m][2]
    t = pd.Timestamp(f"2015-{month:02d}-15 {o}").tz_localize(tz).tz_convert("UTC")
    return t.hour * 60 + t.minute


def hm(x):
    return f"{int(x)//60:02d}:{int(x)%60:02d}"


def main():
    for m in MARKETS:
        d = load(m)
        line = [f"{m:11s}"]
        for name, mo, em in (("JanFeb", [1, 2], 1), ("JulAug", [7, 8], 7)):
            s = spikes(d, mo)
            e = expected_open_utc(m, em)
            top = [hm(k) for k in s.index[:3]]
            ratio = s.get(e, np.nan) / s.median()
            line.append(f"{name}: open exp {hm(e)} UTC (|r|/median {ratio:.1f}) top3 {top}")
        print(" | ".join(line), flush=True)
    print()
    print("market       valid sessions/yr (spec), median bars in [O,C), share <50% bars, years")
    for m in MARKETS:
        s = sessions(m)
        v = s[s.valid]
        per = v.groupby(v.index.year).size()
        print(f"{m:11s} {int(per.min()):4d}..{int(per.max()):4d}/yr  median bars {v.nbars.median():5.0f} of "
              f"{v.nmin.median():4.0f}  thin {(v.nbars < 0.5 * v.nmin).mean():.3f}  "
              f"{per.index.min()}..{per.index.max()} n={len(v)}", flush=True)


if __name__ == "__main__":
    main()
