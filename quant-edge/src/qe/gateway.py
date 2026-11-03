"""The single door to market data: load(id, window).

- Refuses any id without a registry row (non-negotiable 3).
- Slices to the row's in-sample window unless window is "oos" or "holdout".
- "holdout" is refused unless quant-edge/HOLDOUT_UNLOCK exists AND lists the id (Hold-out rule).
- Every call appends (ts_utc, id, window, script, commit) to quant-edge/registry_reads.log.
- Datasets come from quant-edge/data/manifest.csv -> files under DATA_ROOT (parquet or csv, a `ts` column in UTC).
"""
import csv
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pandas as pd

from . import paths, registry

WINDOWS = ("is", "oos", "holdout")


class HoldoutLockedError(PermissionError):
    pass


class DatasetNotInManifestError(FileNotFoundError):
    pass


def _git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=paths.PROGRAM_ROOT,
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return "unknown"


def _script_name() -> str:
    main = sys.modules.get("__main__")
    return os.path.basename(getattr(main, "__file__", "interactive"))


def _append_read(id_: str, window: str, log_path: Optional[Path] = None) -> None:
    log_path = log_path or paths.READS_LOG
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new = not log_path.exists() or log_path.stat().st_size == 0
    with open(log_path, "a", encoding="utf-8") as f:
        if new:
            f.write("ts_utc,registered_id,window,script,commit\n")
        f.write(f"{ts},{id_},{window},{_script_name()},{_git_commit()}\n")


def _manifest(manifest_path: Optional[Path] = None) -> dict:
    manifest_path = manifest_path or paths.MANIFEST_CSV
    out = {}
    with open(manifest_path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[r["dataset_id"]] = r
    return out


def _holdout_unlocked_for(id_: str, unlock_path: Optional[Path] = None) -> bool:
    unlock_path = unlock_path or paths.HOLDOUT_UNLOCK
    if not unlock_path.exists():
        return False
    ids = {line.strip().split()[0] for line in unlock_path.read_text(encoding="utf-8").splitlines()
           if line.strip() and not line.startswith("#")}
    return id_ in ids


def _read_file(path: Path) -> pd.DataFrame:
    if path.suffix == ".parquet":
        df = pd.read_parquet(path)
    else:
        df = pd.read_csv(path)
    if "ts" not in df.columns:
        raise ValueError(f"{path}: dataset must carry a 'ts' column (UTC)")
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    return df.sort_values("ts").reset_index(drop=True)


def load(id_: str, window: str = "is", *, dataset: Optional[str] = None,
         registry_path=None, manifest_path=None, data_root=None, log_path=None, unlock_path=None) -> pd.DataFrame:
    """Return the dataset rows inside the registered window for hypothesis `id_`.

    window: "is" (default), "oos", or "holdout". The read is logged before any data is returned.
    """
    if window not in WINDOWS:
        raise ValueError(f"window must be one of {WINDOWS}, got {window!r}")
    row = registry.get(id_, registry_path)
    if row.source != "program":
        raise registry.UnregisteredHypothesisError(f"{id_} is an inherited row; register a new program row")
    if window not in row.windows:
        raise ValueError(f"{id_}: registry row has no {window.upper()} window in its split field: {row.raw.get('split')!r}")
    if window == "holdout" and not _holdout_unlocked_for(id_, unlock_path):
        _append_read(id_, "holdout-REFUSED", log_path)
        raise HoldoutLockedError(f"{id_}: hold-out is locked (quant-edge/HOLDOUT_UNLOCK missing or does not list {id_})")
    ds_id = dataset or (row.datasets[0] if row.datasets else None)
    if ds_id is None or ds_id not in row.datasets:
        raise ValueError(f"{id_}: dataset {ds_id!r} is not named in the registry row's data field {row.datasets}")
    man = _manifest(manifest_path)
    if ds_id not in man:
        raise DatasetNotInManifestError(f"dataset {ds_id!r} is not in {manifest_path or paths.MANIFEST_CSV}")
    root = Path(data_root or paths.DATA_ROOT)
    _append_read(id_, window, log_path)
    df = _read_file(root / man[ds_id]["path"])
    w = row.windows[window]
    start = pd.Timestamp(w.start, tz="UTC")
    mask = df["ts"] >= start
    if w.end:
        end = pd.Timestamp(w.end, tz="UTC") + pd.Timedelta(days=1)  # inclusive end date
        mask &= df["ts"] < end
    # a hold-out row never leaks into IS or OOS whatever the registry says
    if window != "holdout":
        mask &= df["ts"] < pd.Timestamp(paths.HOLDOUT_START, tz="UTC")
    return df.loc[mask].reset_index(drop=True)
