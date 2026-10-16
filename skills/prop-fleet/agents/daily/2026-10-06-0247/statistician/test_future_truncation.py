"""Future-truncation test (statistician, 2026-10-06; board 'Tomorrow' task).

Property: deleting every bar of day d after the entry minute must not change day d's
eligibility, side, entry time, entry price or stop. Any decision that changes is reading the
future (the IBS / H0012-line-18 pattern: requiring the trade day's own 15:59 bar or a full
session bar count).

`truncation_violations(decide, days)` is the reusable harness: `decide(day_bars)` returns None
(no trade) or a dict with at least 'entry_ts'. Only synthetic data is used here; no market
data is read and no outcome is computed on real bars.

Applied to:
  - today's builder script hypothesis.py (ORB30, prereg sha256 1e99c775): must pass.
  - a negative control written from H0012's prereg line 18 as written ("all of 09:30, 09:31,
    15:59 bars exist"): must be caught.
  - the H0017 companion form (15:59 not required): must pass.
Run:  python3 -m pytest -q skills/prop-fleet/agents/daily/2026-10-06-0247/statistician/test_future_truncation.py
"""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("orb30", HERE.parent / "hypothesis.py")
orb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(orb)

PRE_ENTRY_KEYS = ("side", "entry_ts", "entry", "stop")


def truncation_violations(decide, days):
    """Return the list of (day, full_decision, truncated_decision) that differ."""
    bad = []
    for g in days:
        full = decide(g)
        if full is None:
            # a no-trade day must stay no-trade under every truncation point
            for cut in g.index[::37]:
                if decide(g.loc[:cut]) is not None:
                    bad.append((g.index[0].date(), None, "trade appears on truncation"))
                    break
            continue
        cut = full["entry_ts"]
        trunc = decide(g.loc[:cut])
        key = lambda r: None if r is None else tuple(r.get(k) for k in PRE_ENTRY_KEYS)
        if key(full) != key(trunc):
            bad.append((g.index[0].date(), key(full), key(trunc)))
    return bad


def synthetic_days(n=300, seed=0, drop_frac=0.02):
    """Random-walk RTH sessions 09:30..15:59 with random missing bars (as in SPXUSD D1)."""
    rng = np.random.default_rng(seed)
    out = []
    for i, d in enumerate(pd.bdate_range("2015-01-05", periods=n)):
        idx = pd.date_range(f"{d.date()} 09:30", f"{d.date()} 15:59", freq="1min")
        c = 2000 + np.cumsum(rng.normal(0, 0.8, len(idx)))
        o = np.r_[c[0], c[:-1]]
        h = np.maximum(o, c) + rng.uniform(0, 0.5, len(idx))
        l = np.minimum(o, c) - rng.uniform(0, 0.5, len(idx))
        g = pd.DataFrame(dict(o=o, h=h, l=l, c=c), index=idx)
        keep = rng.uniform(size=len(idx)) > drop_frac
        keep[0] = True
        if i % 7 == 0:                      # some days lose their last bars (feed gap)
            keep[-rng.integers(1, 30):] = False
        out.append(g[keep])
    return out


# -- decision functions under test --------------------------------------------
def orb30_decide(variant):
    def decide(g):
        orr = orb.opening_range(g)
        if orr is None:
            return None
        r = orb.trade_day(g, orr[0], orr[1], variant)
        if r is None:
            return None
        hm = g.index.strftime("%H:%M")
        win = g[(hm >= "10:00") & (hm <= "11:59")]
        trig = next(ts for ts, c in zip(win.index, win["c"]) if c > orr[0] or c < orr[1])
        entry_ts = g.index[g.index > trig][0]
        return dict(side=r["side"], entry_ts=entry_ts, entry=r["entry"], stop=r["stop"])
    return decide


def h0012_as_written(g):
    """Prereg line 18 eligibility, as written: requires today's 09:30, 09:31 AND 15:59 bars."""
    hm = set(g.index.strftime("%H:%M"))
    if not {"09:30", "09:31", "15:59"} <= hm:
        return None
    e = g[g.index.strftime("%H:%M") == "09:31"].iloc[0]
    side = -1 if g["o"].iloc[0] > 2000 else 1          # stand-in for -sign(gap)
    return dict(side=side, entry_ts=e.name, entry=float(e.o), stop=float(e.o) - side * 3)


def h0017_form(g):
    """H0017: 15:59 not required; only 09:30 and 09:31 must exist."""
    hm = set(g.index.strftime("%H:%M"))
    if not {"09:30", "09:31"} <= hm:
        return None
    e = g[g.index.strftime("%H:%M") == "09:31"].iloc[0]
    side = -1 if g["o"].iloc[0] > 2000 else 1
    return dict(side=side, entry_ts=e.name, entry=float(e.o), stop=float(e.o) - side * 3)


@pytest.mark.parametrize("variant", ["A", "B"])
@pytest.mark.parametrize("seed", [0, 1, 2])
def test_orb30_is_future_free(variant, seed):
    days = synthetic_days(seed=seed)
    decide = orb30_decide(variant)
    assert sum(decide(g) is not None for g in days) > 50       # the test exercises trades
    assert truncation_violations(decide, days) == []


def test_orb30_variant_c_filter_uses_only_prior_days():
    """C's median-W filter: deleting the future of day d (and all later days) leaves day d's
    C decision unchanged."""
    days = synthetic_days(seed=3)
    m1 = pd.concat(days)
    full, _ = orb.run(m1, "C")          # synthetic only
    assert len(full) > 10
    for d in full["day"].iloc[::5]:
        dd = days[[g.index[0].normalize() for g in days].index(d)]
        entry_ts = orb30_decide("A")(dd)["entry_ts"]
        t, _ = orb.run(m1.loc[:entry_ts], "C")
        row_full = full[full.day == d].iloc[0]
        row_t = t[t.day == d].iloc[0]
        assert (row_t.side, row_t.entry, row_t.stop) == (row_full.side, row_full.entry, row_full.stop)


def test_harness_catches_h0012_as_written():
    days = synthetic_days(seed=0)
    bad = truncation_violations(h0012_as_written, days)
    assert len(bad) > 0                                        # look-ahead detected


def test_h0017_form_passes():
    days = synthetic_days(seed=0)
    assert truncation_violations(h0017_form, days) == []
