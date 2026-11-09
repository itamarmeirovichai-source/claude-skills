"""qe.engine.run — the only way market data enters the engine: run_registered(id, window, ...) -> qe.gateway.load.

The frame returned by the gateway is tagged and marked with attrs["registered_id"], ["window"], ["dataset"]; simulate()
refuses frames without that mark (or the synthetic mark). An OOS read is logged by the gateway itself
(registry_reads.log); this module adds nothing to the log and never reads a file.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

from .. import gateway, registry
from . import bars as _bars
from . import pnl as _pnl
from . import rules as _rules


def load_registered(id_: str, window: str = "is", *, dataset: Optional[str] = None, root: Optional[str] = None,
                    daily: bool = False, **gateway_kwargs) -> pd.DataFrame:
    """gateway.load + tagging + provenance mark. `root` defaults to the registry row's first instrument token."""
    row = registry.get(id_, gateway_kwargs.get("registry_path"))
    df = gateway.load(id_, window, dataset=dataset, **gateway_kwargs)
    root = root or _root_from_row(row)
    if "open" not in df.columns and "close" in df.columns:      # a close-only daily series
        df = df.assign(open=df["close"], high=df["close"], low=df["close"])
    frame = _bars.tag_daily(df, root) if daily else _bars.tag(df, root)
    frame = _drop_straddling_days(frame, row, window, daily)
    frame.attrs["registered_id"] = id_
    frame.attrs["window"] = window
    frame.attrs["dataset"] = dataset or (row.datasets[0] if row.datasets else None)
    frame.attrs["registry_row"] = dict(row.raw)
    return frame


def _drop_straddling_days(frame: pd.DataFrame, row: registry.Row, window: str, daily: bool) -> pd.DataFrame:
    """A registry window is a UTC calendar-date window on bar-open timestamps, while a futures trading day starts at
    18:00 ET the evening before its label. The trading day that straddles a window boundary is therefore partial on
    both sides; it is dropped from both (one trading day is lost at each IS/OOS boundary, none is shared).
    Intraday: keep start_date < trading_day <= end_date. Daily frames: keep start_date <= trading_day <= end_date."""
    w = row.windows.get("oos" if window == "crosscheck" else window)
    if w is None or "trading_day" not in frame.columns:
        return frame
    td = pd.DatetimeIndex(frame["trading_day"])
    start = pd.Timestamp(w.start)
    keep = (td >= start) if daily else (td > start)
    if w.end:
        keep &= td <= pd.Timestamp(w.end)
    out = frame.loc[keep].reset_index(drop=True)
    out.attrs.update(frame.attrs)
    if not daily and "day_id" in out.columns:
        out["day_id"] = _bars._day_ids(out["trading_day"]).astype(np.int32)
    return out


def _root_from_row(row: registry.Row) -> str:
    tok = (row.raw.get("instruments") or "ES").replace(";", ",").split(",")[0].strip().upper()
    return tok or "ES"


def config_from_row(row: dict, **overrides) -> _pnl.RunConfig:
    """RunConfig from the registry row's firm_structure, guard_fraction and instruments (overrides win)."""
    fs = (row.get("firm_structure") or "").strip()
    firm = {"intraday-futures": "topstep", "overnight-session-futures": "topstep"}.get(fs)
    kw = dict(root=_root_from_row(registry.Row(row.get("id", ""), "", "program", (), {}, 0, "", row)),
              firm=firm, intraday_only=fs in ("intraday-futures", "overnight-session-futures", "ftmo-intraday-cfd"))
    try:
        kw["guard_fraction"] = float(row.get("guard_fraction") or 0.7)
    except ValueError:
        pass
    kw.update(overrides)
    return _pnl.RunConfig(**kw)


def run_registered(id_: str, window: str, rule, config: Optional[_pnl.RunConfig] = None, *, dataset: Optional[str] = None,
                   scaler: Optional[_rules.VolScaler] = None, daily: bool = False, **gateway_kwargs) -> _pnl.Result:
    """Load through the door, apply the row's vol scaler (or the one given), simulate. Refuses unregistered ids
    because gateway.load does."""
    frame = load_registered(id_, window, dataset=dataset, daily=daily, **gateway_kwargs)
    row = frame.attrs["registry_row"]
    config = config or config_from_row(row)
    if scaler is None:
        scaler = _rules.parse_vol_scaler(row.get("vol_scaler", ""))
    scale = scaler.scale_bars(frame) if (scaler is not None and rule.mode == "target") else None
    res = _pnl.simulate(frame, rule, config, scale=scale)
    res.provenance.update({"registry_row": row, "scaler": scaler.describe() if scaler else "none"})
    return res
