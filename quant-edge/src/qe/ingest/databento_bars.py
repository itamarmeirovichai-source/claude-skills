"""Download finished Databento batch jobs and land GLBX ohlcv-1h continuous bars (one dataset per root).

- raw DBN files: DATA_ROOT/raw/databento/<job_id>/ (sha256 of the tree in the manifest as raw_<job_id>)
- IS/OOS rows (ts < 2025-01-01): DATA_ROOT/derived/dbn_glbx_1h_<ROOT>.parquet
- hold-out rows (ts >= 2025-01-01): DATA_ROOT/holdout/dbn_glbx_1h_<ROOT>_holdout.parquet (never read for P&L)
- ts = bar OPEN in UTC (Databento ts_event of an ohlcv bar); prices in exchange display units; instrument_id kept for the roll rule.
The key is read by the databento client from DATABENTO_API_KEY; this module never touches it.
"""
import argparse
from pathlib import Path

import databento as db
import pandas as pd

from .. import paths
from . import common

HOLD = pd.Timestamp(paths.HOLDOUT_START, tz="UTC")


def download(job_id: str) -> Path:
    out = paths.DATA_ROOT / "raw" / "databento"
    out.mkdir(parents=True, exist_ok=True)
    c = db.Historical()
    c.batch.download(job_id=job_id, output_dir=out)
    d = out / job_id
    common.manifest_upsert(f"raw_{job_id}", path=f"raw/databento/{job_id}", source=f"Databento batch job {job_id}",
                           licence_status="licensed", resolution="raw dbn.zst", tz="UTC (ts_event)", start="", end="",
                           sha256=common.sha256_tree(d), rows=0, notes="raw purchase; see databento_spend_ledger.csv")
    return d


def read_job(d: Path, schema_hint: str = "ohlcv-1h") -> pd.DataFrame:
    frames = []
    for f in sorted(d.rglob("*.dbn.zst")):
        store = db.DBNStore.from_file(f)
        df = store.to_df(pretty_ts=True, price_type="float", map_symbols=True)
        if len(df):
            frames.append(df.reset_index())
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def land_ohlcv(d: Path, job_id: str, tag: str = "1h") -> dict:
    df = read_job(d)
    df = df.rename(columns={"ts_event": "ts"})
    out = {}
    for sym, g in df.groupby("symbol"):
        root = sym.split(".")[0]
        g = g[["ts", "open", "high", "low", "close", "volume", "instrument_id"]].sort_values("ts")
        g = g.drop_duplicates("ts", keep="last")
        ds = f"dbn_glbx_{tag}_{root}"
        note = (f"Databento GLBX.MDP3 ohlcv-{tag} stype continuous {sym}; job {job_id}; ts = bar open UTC; "
                f"bars only for intervals with trades; instrument_id kept (roll rule)")
        out[ds] = common.land(ds, g[g["ts"] < HOLD], f"derived/{ds}.parquet", source=f"Databento job {job_id}",
                              licence_status="licensed", resolution=tag, tz_note="ts = bar open UTC", notes=note)
        out[ds + "_holdout"] = common.land(ds + "_holdout", g[g["ts"] >= HOLD], f"holdout/{ds}_holdout.parquet",
                                          source=f"Databento job {job_id}", licence_status="licensed", resolution=tag,
                                          tz_note="ts = bar open UTC", notes=note + "; HOLD-OUT: never read before HOLDOUT_UNLOCK")
    return out


def land_definitions(d: Path, job_id: str) -> dict:
    df = read_job(d)
    keep = [c for c in ["ts_event", "instrument_id", "raw_symbol", "symbol", "min_price_increment", "unit_of_measure_qty",
                        "display_factor", "expiration", "currency", "asset", "security_type"] if c in df.columns]
    df = df[keep].rename(columns={"ts_event": "ts"}).drop_duplicates(["instrument_id", "raw_symbol"])
    return {"dbn_glbx_definitions": common.land("dbn_glbx_definitions", df, "derived/dbn_glbx_definitions.parquet",
                                                source=f"Databento job {job_id}", licence_status="licensed",
                                                resolution="event", tz_note="ts = definition ts_event UTC",
                                                notes="instrument definitions (tick size, multiplier, expiry) for QA and costs")}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("job_id")
    ap.add_argument("--definitions", action="store_true")
    ap.add_argument("--tag", default="1h")
    a = ap.parse_args(argv)
    d = download(a.job_id)
    print(land_definitions(d, a.job_id) if a.definitions else land_ohlcv(d, a.job_id, a.tag))


if __name__ == "__main__":
    main()
