"""Batch-1b plumbing shared by Q-0007, Q-0008, Q-0009 (Dept D, 2026-11-06). No rule content lives here.

HistData CFD bars (corrected clock `histdata_rule`, D-019): ts = bar OPEN in UTC, bid quotes. Local wall-clock times are
obtained per bar with zoneinfo (pandas tz_convert), so every rule time is applied per day in its own zone.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from qe import gateway  # noqa: E402

NY, HK = "America/New_York", "Asia/Hong_Kong"
TARGET_DAILY = 0.10 / math.sqrt(252)


@dataclass
class Prepared:
    """One instrument's bars with local tags. Arrays are aligned and sorted by ts."""
    ts: np.ndarray        # int64 ns UTC (bar open)
    date: np.ndarray      # datetime64[D] local calendar date
    minute: np.ndarray    # int local minute of day (0..1439)
    open: np.ndarray
    high: np.ndarray
    low: np.ndarray
    close: np.ndarray
    tz: str

    def __len__(self):
        return self.ts.size

    def head_until(self, ts_ns: int) -> "Prepared":
        """Bars whose open is <= ts_ns (the truncation harness)."""
        k = int(np.searchsorted(self.ts, ts_ns, side="right"))
        return Prepared(self.ts[:k], self.date[:k], self.minute[:k], self.open[:k], self.high[:k], self.low[:k], self.close[:k], self.tz)

    def perturbed_after(self, ts_ns: int, rng, eps: float = 0.01) -> "Prepared":
        """Bars whose open is > ts_ns get multiplicative noise (the perturbation harness); OHLC kept consistent."""
        k = int(np.searchsorted(self.ts, ts_ns, side="right"))
        n = self.ts.size - k
        o, h, l, c = (x.copy() for x in (self.open, self.high, self.low, self.close))
        if n > 0:
            z = np.exp(rng.standard_normal(n) * eps)
            for a in (o, h, l, c):
                a[k:] *= z
            h[k:] = np.maximum.reduce([o[k:], h[k:], c[k:]])
            l[k:] = np.minimum.reduce([o[k:], l[k:], c[k:]])
        return Prepared(self.ts, self.date, self.minute, o, h, l, c, self.tz)


def prepare(bars: pd.DataFrame, tz: str) -> Prepared:
    t = pd.DatetimeIndex(bars["ts"])
    loc = t.tz_convert(tz)
    date = loc.tz_localize(None).normalize().to_numpy().astype("datetime64[D]")
    minute = (loc.hour * 60 + loc.minute).to_numpy().astype(np.int64)
    return Prepared(t.as_unit("ns").asi8.copy(), date, minute, *(bars[c].to_numpy(float).copy() for c in ("open", "high", "low", "close")), tz)


def load(id_: str, dataset: str, window: str) -> pd.DataFrame:
    b = gateway.load(id_, window, dataset=dataset)
    return b[["ts", "open", "high", "low", "close"]].reset_index(drop=True)


def load_is_oos(id_: str, dataset: str) -> pd.DataFrame:
    """IS history + exactly one OOS read of the dataset (the OOS stage)."""
    a, b = load(id_, dataset, "is"), load(id_, dataset, "oos")
    return pd.concat([a, b], ignore_index=True).drop_duplicates("ts").sort_values("ts").reset_index(drop=True)


def day_slices(p: Prepared) -> dict:
    """local date (datetime64[D]) -> (lo, hi) index range."""
    if len(p) == 0:
        return {}
    u, first = np.unique(p.date, return_index=True)
    last = np.r_[first[1:], len(p)]
    return {d: (int(a), int(b)) for d, a, b in zip(u, first, last)}


def hhmm(m: int) -> str:
    return f"{m // 60:02d}:{m % 60:02d}"


def local_ns(date, minute: int, tz: str) -> int:
    """UTC ns of local wall-clock `minute` on calendar `date` in `tz`."""
    ts = pd.Timestamp(pd.Timestamp(date).date()) + pd.Timedelta(minutes=int(minute))
    return int(ts.tz_localize(tz).tz_convert("UTC").as_unit("ns").value)
