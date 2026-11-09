"""Outcome-free cross-source QA: daily returns of a gateway-loaded FX series against a second source.

`second_source_returns` reads a manifest dataset directly (allowed for qe.qa) restricted to the dates the caller
passes (the caller passes in-sample dates only), and `compare` reports the correlation at lags -1, 0, +1 (a date
misalignment shows up as the peak away from lag 0) and the ratio of standard deviations. Nothing about any strategy
is computed."""
from __future__ import annotations

import csv

import numpy as np
import pandas as pd

from .. import paths


def _path(dataset_id: str):
    with open(paths.MANIFEST_CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["dataset_id"] == dataset_id:
                return paths.DATA_ROOT.joinpath(r["path"]), r
    raise KeyError(dataset_id)


def second_source_returns(dataset_id: str, column: str, start: str, end: str) -> pd.Series:
    p, _ = _path(dataset_id)
    df = pd.read_parquet(p, columns=["ts", column])
    s = df.set_index(pd.to_datetime(df["ts"], utc=True).dt.tz_localize(None).dt.normalize())[column]
    return s[(s.index >= pd.Timestamp(start)) & (s.index <= pd.Timestamp(end))].astype(float)


def available_columns(dataset_id: str) -> list:
    p, _ = _path(dataset_id)
    import pyarrow.parquet as pq
    return [c for c in pq.read_schema(p).names if c != "ts"]


def compare(fx_ret: pd.Series, other: pd.Series) -> dict:
    """fx_ret: date-indexed daily log returns (17:00 NY closes); other: date-indexed daily returns."""
    out = {}
    for lag in (-1, 0, 1):
        o = other.shift(lag)
        j = pd.concat([fx_ret, o], axis=1, join="inner").dropna()
        out[f"corr_lag{lag:+d}"] = float(j.iloc[:, 0].corr(j.iloc[:, 1])) if len(j) > 10 else float("nan")
        if lag == 0:
            out["n"] = int(len(j))
            out["sd_ratio_other_over_fx"] = float(j.iloc[:, 1].std() / j.iloc[:, 0].std()) if len(j) > 10 else float("nan")
    return out
