"""qe.engine.rules — the declarative rule interface and the ex-ante volatility scaler.

A rule is any object with
    name: str
    params: dict                                   (every tunable, so the neighbourhood runner can move them)
    signal(bars) -> np.ndarray                     target position per bar (float; 0 = flat), OR
    orders(bars) -> fills.BracketOrders            discrete bracket entries,
    with_params(**changes) -> Rule                 a copy with changed parameters (neighbourhood runner)
    variants() -> dict[str, Rule]                  optional: {"ex_ante": rule_ex_ante, "as_written": rule} for the lag harness

Information convention (asserted by qe.engine.harness.future_truncation_test): `target[i]` is the position held over bar i
(from open[i] to open[i+1]) and may depend only on bars 0..i-1 (closed before open[i]) and on day-level values of
earlier trading days. `orders(bars).entry_idx = i` likewise means "decided at the information set of open[i]", with the
reference price open[i]. Nothing about day d may change when every bar after the entry minute of day d is deleted.

Vol scaler: `VolScaler(window, cap, floor, target_vol)` multiplies the base position by
clip(target_vol / ex_ante_vol, floor, cap) where ex_ante_vol is the annualised standard deviation of the previous `window`
daily close-to-close returns (days d-window .. d-1 only; `bars.ex_ante_daily_vol`). Registry field format:
"window=20;cap=3;floor=0.3;target=0.15" (also accepts the Day-1 prose "ex-ante 20d realized, cap 3x, floor 0.3x").
"""
from __future__ import annotations

import copy
import math
import re
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional

import numpy as np
import pandas as pd

from . import bars as _bars
from . import fills as _fills


@dataclass
class VolScaler:
    window: int = 20
    cap: float = 3.0
    floor: float = 0.3
    target_vol: float = 0.15          # annualised
    periods_per_year: int = 252

    def scale_days(self, daily_ret: np.ndarray) -> np.ndarray:
        """Multiplier per trading day from the previous `window` daily returns; NaN (-> 0 exposure) until enough history."""
        vol = _bars.ex_ante_daily_vol(daily_ret, self.window) * math.sqrt(self.periods_per_year)
        with np.errstate(divide="ignore", invalid="ignore"):
            s = self.target_vol / vol
        s = np.clip(s, self.floor, self.cap)
        return np.where(np.isfinite(s), s, 0.0)

    def scale_bars(self, bars: pd.DataFrame, daily: Optional[pd.DataFrame] = None) -> np.ndarray:
        """Multiplier per bar (constant inside a trading day; known at the day's open)."""
        if bars.attrs.get("daily"):
            r = np.log(bars["close"].to_numpy(float))
            r = np.r_[np.nan, np.diff(r)]
            return self.scale_days(r)
        daily = daily if daily is not None else _bars.daily_from_bars(bars)
        s_day = pd.Series(self.scale_days(daily["ret"].to_numpy(float)), index=daily.index)
        return s_day.reindex(bars["day_id"].to_numpy()).fillna(0.0).to_numpy(float)

    def describe(self) -> str:
        return f"ex-ante {self.window}d realized vol, target {self.target_vol:.0%}, cap {self.cap}x, floor {self.floor}x"


def parse_vol_scaler(text: str) -> Optional[VolScaler]:
    """Parse the registry `vol_scaler` field. Returns None for 'none'/'fixed'/'1 contract'."""
    t = (text or "").strip().lower()
    if not t or t in ("none", "fixed", "no", "1 contract", "constant"):
        return None
    kw: Dict[str, float] = {}
    for k, v in re.findall(r"(window|cap|floor|target)\s*=\s*([0-9.]+)", t):
        kw[k] = float(v)
    if not kw:
        m = re.search(r"(\d+)\s*d", t)
        if m:
            kw["window"] = float(m.group(1))
        m = re.search(r"cap\s*([0-9.]+)", t)
        if m:
            kw["cap"] = float(m.group(1))
        m = re.search(r"floor\s*([0-9.]+)", t)
        if m:
            kw["floor"] = float(m.group(1))
        m = re.search(r"target\s*([0-9.]+)\s*%?", t)
        if m:
            kw["target"] = float(m.group(1)) / (100 if float(m.group(1)) > 1 else 1)
    if not kw:
        raise ValueError(f"cannot parse vol_scaler field {text!r}")
    return VolScaler(window=int(kw.get("window", 20)), cap=kw.get("cap", 3.0), floor=kw.get("floor", 0.3),
                     target_vol=kw.get("target", 0.15))


def apply_scaler(target: np.ndarray, scale: np.ndarray, round_contracts: bool = True) -> np.ndarray:
    out = np.asarray(target, float) * np.asarray(scale, float)
    return np.round(out) if round_contracts else out


# ----------------------------------------------------------------------------------------------------- rule base
class Rule:
    """Base class; subclass and implement signal() or orders(). `params` holds every tunable."""
    name: str = "rule"
    params: dict = {}
    continuous: tuple = ()     # parameter names moved +-25% by the neighbourhood runner
    discrete: tuple = ()       # parameter names moved one step each way (step = params[name + "_step"] or 1)

    def __init__(self, **params):
        self.params = {**self.__class__.params, **params}

    def with_params(self, **changes) -> "Rule":
        r = copy.copy(self)
        r.params = {**self.params, **changes}
        return r

    def signal(self, bars: pd.DataFrame) -> np.ndarray:
        raise NotImplementedError

    def orders(self, bars: pd.DataFrame) -> _fills.BracketOrders:
        raise NotImplementedError

    @property
    def mode(self) -> str:
        return "brackets" if type(self).orders is not Rule.orders else "target"

    def variants(self) -> Dict[str, "Rule"]:
        return {}

    def describe(self) -> str:
        return f"{self.name} {self.params}"


class FuncRule(Rule):
    """Wrap a function f(bars, **params) -> target array (mode='target') or BracketOrders (mode='brackets')."""

    def __init__(self, name: str, fn: Callable, mode: str = "target", continuous=(), discrete=(), **params):
        self.name = name
        self.fn = fn
        self._mode = mode
        self.continuous = tuple(continuous)
        self.discrete = tuple(discrete)
        self.params = dict(params)

    @property
    def mode(self) -> str:
        return self._mode

    def signal(self, bars):
        if self._mode != "target":
            raise NotImplementedError
        return np.asarray(self.fn(bars, **self.params), float)

    def orders(self, bars):
        if self._mode != "brackets":
            raise NotImplementedError
        return self.fn(bars, **self.params)


# ------------------------------------------------------------------------------------------- helpers for rules
def minute_mask(bars: pd.DataFrame, start_tday: int, end_tday: int, rth_only: bool = True) -> np.ndarray:
    """Bars whose tday_minute is in [start, end) (minutes since the 18:00 ET reopen), optionally RTH only."""
    t = bars["tday_minute"].to_numpy()
    m = (t >= start_tday) & (t < end_tday)
    if rth_only:
        m &= bars["is_rth"].to_numpy(bool)
    return m


def first_bar_of_day_at_or_after(bars: pd.DataFrame, tday: int) -> np.ndarray:
    """Index of the first bar per trading day with tday_minute >= tday (one per day that has such a bar)."""
    t = bars["tday_minute"].to_numpy()
    d = bars["day_id"].to_numpy()
    ok = t >= tday
    df = pd.DataFrame({"d": d[ok], "i": np.nonzero(ok)[0]})
    return df.groupby("d")["i"].min().to_numpy()
