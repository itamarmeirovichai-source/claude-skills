"""Shared ingestion plumbing: polite fetch, sha256 pins, parquet/CSV writers, manifest rows, fetch log.

Conventions (briefs/C-data-run.md):
  * every dataset carries a tz-aware UTC `ts` column = bar OPEN time (daily bars: 00:00 UTC of the trading date, so a
    registry window `IS=a..b` on calendar dates slices exactly);
  * data live under DATA_ROOT (~/quant-edge-data), never in the repository; the manifest row
    (quant-edge/data/manifest.csv) is written the moment a file lands, then MANIFEST.md is re-rendered;
  * a large dataset is a DIRECTORY of parquet parts (root/year=YYYY/part.parquet); pandas reads it as one frame; its
    sha256 is the sha256 of the sorted "relpath  sha256" lines of its parts (`sha256_tree`);
  * one request at a time, Retry-After honoured, stop on HTTP 429 (RateLimited) and record it in the fetch log.
"""
from __future__ import annotations

import csv
import hashlib
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional
from urllib import request as _urlreq, error as _urlerr, parse as _urlparse

import pandas as pd

from qe import paths

DATA_ROOT: Path = paths.DATA_ROOT
RAW = DATA_ROOT / "raw"
DERIVED = DATA_ROOT / "derived"
CALENDARS = DATA_ROOT / "calendars"
FETCH_LOG = DATA_ROOT / "fetch_log.csv"
MANIFEST_COLS = ["dataset_id", "path", "source", "licence_status", "resolution", "tz", "start", "end", "sha256", "rows", "notes"]
BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
MIN_GAP_S = 1.0     # politeness: at least this long between two requests to any host
_last_request_ts = 0.0


class RateLimited(RuntimeError):
    """HTTP 429 (or a Retry-After we will not wait for): the caller stops and records it; never retried in a loop."""


class Blocked(RuntimeError):
    """Host refused (403/5xx/connection reset): reported, never routed around (D-007)."""


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ----------------------------------------------------------------------------------------------------------------- hashes
def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_tree(root: Path) -> str:
    """Deterministic digest of a directory dataset: sha256 over sorted 'relpath  sha256(part)' lines."""
    lines = []
    for p in sorted(root.rglob("*")):
        if p.is_file():
            lines.append(f"{p.relative_to(root).as_posix()}  {sha256_file(p)}")
    return hashlib.sha256("\n".join(lines).encode()).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_tree(path) if path.is_dir() else sha256_file(path)


# ----------------------------------------------------------------------------------------------------------------- fetch log
def _log_fetch(url: str, dest: Optional[Path], status: str, nbytes: int, sha: str, note: str = "") -> None:
    FETCH_LOG.parent.mkdir(parents=True, exist_ok=True)
    new = not FETCH_LOG.exists() or FETCH_LOG.stat().st_size == 0
    with open(FETCH_LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["ts_utc", "url", "dest", "status", "bytes", "sha256", "note"])
        w.writerow([utc_now(), url, str(dest) if dest else "", status, nbytes, sha, note])


def _polite_wait() -> None:
    global _last_request_ts
    gap = time.monotonic() - _last_request_ts
    if gap < MIN_GAP_S:
        time.sleep(MIN_GAP_S - gap)
    _last_request_ts = time.monotonic()


def fetch(url: str, dest: Path, *, post: Optional[dict] = None, headers: Optional[dict] = None, ua: str = BROWSER_UA,
          timeout: int = 120, overwrite: bool = False, dry_run: bool = False, http1: bool = True) -> dict:
    """Download `url` to `dest` (one request, polite). Returns {path, sha256, bytes, status, cached}.

    Idempotent: an existing non-empty `dest` is reused unless `overwrite`. 429 -> RateLimited (recorded, no retry loop).
    403/5xx/connection errors -> Blocked (recorded). Uses curl via the agent proxy (HTTP/1.1 by default: several hosts
    reset HTTP/2 streams here).
    """
    dest = Path(dest)
    if dest.exists() and dest.stat().st_size > 0 and not overwrite:
        return {"path": dest, "sha256": sha256_file(dest), "bytes": dest.stat().st_size, "status": "cached", "cached": True}
    if dry_run:
        print(f"[dry-run] would fetch {url} -> {dest}")
        return {"path": dest, "sha256": "", "bytes": 0, "status": "dry-run", "cached": False}
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    cmd = ["curl", "-sS", "-L", "--max-time", str(timeout), "-A", ua, "-o", str(tmp), "-w", "%{http_code}", "-D", str(tmp) + ".hdr"]
    if http1:
        cmd.append("--http1.1")
    for k, v in (headers or {}).items():
        cmd += ["-H", f"{k}: {v}"]
    if post is not None:
        cmd += ["--data", _urlparse.urlencode(post)]
    cmd.append(url)
    _polite_wait()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    code = proc.stdout.strip()[-3:] if proc.stdout else "000"
    hdr_path = Path(str(tmp) + ".hdr")
    retry_after = ""
    if hdr_path.exists():
        for line in hdr_path.read_text(errors="replace").splitlines():
            if line.lower().startswith("retry-after:"):
                retry_after = line.split(":", 1)[1].strip()
        hdr_path.unlink()
    if proc.returncode != 0 or code == "000":
        if tmp.exists():
            tmp.unlink()
        _log_fetch(url, dest, f"error:{proc.returncode}", 0, "", proc.stderr.strip()[:200])
        raise Blocked(f"{url}: curl exit {proc.returncode}: {proc.stderr.strip()[:200]}")
    if code == "429":
        if tmp.exists():
            tmp.unlink()
        _log_fetch(url, dest, "429", 0, "", f"Retry-After={retry_after!r}; stopped (politeness rule)")
        raise RateLimited(f"{url}: HTTP 429 (Retry-After={retry_after!r}); stopped")
    if not code.startswith("2"):
        if tmp.exists():
            tmp.unlink()
        _log_fetch(url, dest, code, 0, "", "blocked or missing")
        raise Blocked(f"{url}: HTTP {code}")
    n = tmp.stat().st_size
    sha = sha256_file(tmp)
    os.replace(tmp, dest)
    _log_fetch(url, dest, code, n, sha)
    return {"path": dest, "sha256": sha, "bytes": n, "status": code, "cached": False}


def fetch_text(url: str, **kw) -> str:
    """Small helper for pages we parse but do not keep as a dataset (tokens, schedules). Still logged."""
    _polite_wait()
    req = _urlreq.Request(url, headers={"User-Agent": kw.get("ua", BROWSER_UA), **kw.get("headers", {})})
    try:
        with _urlreq.urlopen(req, timeout=kw.get("timeout", 60)) as r:
            b = r.read()
            _log_fetch(url, None, str(r.status), len(b), sha256_bytes(b), "page")
            return b.decode(kw.get("encoding", "utf-8"), errors="replace")
    except _urlerr.HTTPError as e:
        _log_fetch(url, None, str(e.code), 0, "", "page error")
        if e.code == 429:
            raise RateLimited(f"{url}: HTTP 429") from e
        raise Blocked(f"{url}: HTTP {e.code}") from e
    except Exception as e:  # noqa: BLE001
        _log_fetch(url, None, "error", 0, "", str(e)[:200])
        raise Blocked(f"{url}: {e}") from e


# ----------------------------------------------------------------------------------------------------------------- writers
def ensure_ts_utc(df: pd.DataFrame, col: str = "ts") -> pd.DataFrame:
    if col not in df.columns:
        raise ValueError("dataset must carry a 'ts' column")
    ts = pd.to_datetime(df[col], utc=True)
    out = df.copy()
    out[col] = ts.astype("datetime64[ns, UTC]")
    out = out.sort_values(col, kind="mergesort").reset_index(drop=True)
    return out


def write_parquet(df: pd.DataFrame, rel_path: str, *, dry_run: bool = False) -> dict:
    """Write one parquet file at DATA_ROOT/rel_path (ts in UTC, sorted). Returns {path, sha256, rows, start, end}."""
    df = ensure_ts_utc(df)
    path = DATA_ROOT / rel_path
    info = {"path": rel_path, "rows": int(len(df)), "start": df["ts"].iloc[0].strftime("%Y-%m-%d") if len(df) else "",
            "end": df["ts"].iloc[-1].strftime("%Y-%m-%d") if len(df) else ""}
    if dry_run:
        print(f"[dry-run] would write {len(df)} rows -> {path}")
        return {**info, "sha256": ""}
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".parquet.part")
    df.to_parquet(tmp, index=False, compression="zstd")
    os.replace(tmp, path)
    return {**info, "sha256": sha256_file(path)}


def write_parquet_partitioned(df: pd.DataFrame, rel_dir: str, *, dry_run: bool = False) -> dict:
    """Write DATA_ROOT/rel_dir/year=YYYY/part.parquet per UTC year (idempotent: each year file is replaced whole)."""
    df = ensure_ts_utc(df)
    root = DATA_ROOT / rel_dir
    info = {"path": rel_dir, "rows": int(len(df)), "start": df["ts"].iloc[0].strftime("%Y-%m-%d") if len(df) else "",
            "end": df["ts"].iloc[-1].strftime("%Y-%m-%d") if len(df) else ""}
    if dry_run:
        print(f"[dry-run] would write {len(df)} rows in {df['ts'].dt.year.nunique()} year parts -> {root}")
        return {**info, "sha256": ""}
    written = set()
    for year, part in df.groupby(df["ts"].dt.year):
        d = root / f"year={int(year)}"
        d.mkdir(parents=True, exist_ok=True)
        tmp = d / "part.parquet.part"
        part.reset_index(drop=True).to_parquet(tmp, index=False, compression="zstd")
        os.replace(tmp, d / "part.parquet")
        written.add(d.name)
    # a re-land that no longer covers a year must not leave that year's old part behind (it would be read and hashed)
    for d in root.glob("year=*"):
        if d.is_dir() and d.name not in written:
            for f in d.iterdir():
                f.unlink()
            d.rmdir()
    return {**info, "sha256": sha256_tree(root)}


def write_csv(df: pd.DataFrame, rel_path: str, *, dry_run: bool = False) -> dict:
    df = ensure_ts_utc(df)
    path = DATA_ROOT / rel_path
    info = {"path": rel_path, "rows": int(len(df)), "start": df["ts"].iloc[0].strftime("%Y-%m-%d") if len(df) else "",
            "end": df["ts"].iloc[-1].strftime("%Y-%m-%d") if len(df) else ""}
    if dry_run:
        print(f"[dry-run] would write {len(df)} rows -> {path}")
        return {**info, "sha256": ""}
    path.parent.mkdir(parents=True, exist_ok=True)
    out = df.copy()
    out["ts"] = out["ts"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    tmp = path.with_suffix(".csv.part")
    out.to_csv(tmp, index=False)
    os.replace(tmp, path)
    return {**info, "sha256": sha256_file(path)}


# ----------------------------------------------------------------------------------------------------------------- manifest
def manifest_rows(manifest: Optional[Path] = None) -> list:
    manifest = manifest or paths.MANIFEST_CSV
    if not manifest.exists():
        return []
    with open(manifest, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def manifest_upsert(dataset_id: str, *, path: str, source: str, licence_status: str, resolution: str, tz: str,
                    start: str, end: str, sha256: str, rows: int, notes: str, manifest: Optional[Path] = None,
                    render: bool = True, dry_run: bool = False) -> dict:
    """Insert or replace the manifest row for dataset_id (idempotent), then re-render MANIFEST.md."""
    row = {"dataset_id": dataset_id, "path": path, "source": source, "licence_status": licence_status,
           "resolution": resolution, "tz": tz, "start": start, "end": end, "sha256": sha256, "rows": str(rows),
           "notes": notes.replace("\n", " ").replace(",", ";")}
    if dry_run:
        print(f"[dry-run] manifest row: {row}")
        return row
    manifest = manifest or paths.MANIFEST_CSV
    existing = manifest_rows(manifest)
    out = [r for r in existing if r.get("dataset_id") != dataset_id] + [row]
    out.sort(key=lambda r: r["dataset_id"])
    tmp = manifest.with_suffix(".csv.tmp")
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=MANIFEST_COLS)
        w.writeheader()
        for r in out:
            w.writerow({k: r.get(k, "") for k in MANIFEST_COLS})
    os.replace(tmp, manifest)
    if render and manifest == paths.MANIFEST_CSV:
        subprocess.run([sys.executable, str(paths.PROGRAM_ROOT / "tools" / "render_manifest.py")], check=False,
                       capture_output=True)
    return row


def land(dataset_id: str, df: pd.DataFrame, rel_path: str, *, source: str, licence_status: str, resolution: str,
         tz_note: str, notes: str, fmt: str = "parquet", dry_run: bool = False, manifest: Optional[Path] = None) -> dict:
    """Write the dataset (parquet file / partitioned dir / csv) and its manifest row in one step."""
    if fmt == "parquet":
        info = write_parquet(df, rel_path, dry_run=dry_run)
    elif fmt == "partitioned":
        info = write_parquet_partitioned(df, rel_path, dry_run=dry_run)
    elif fmt == "csv":
        info = write_csv(df, rel_path, dry_run=dry_run)
    else:
        raise ValueError(fmt)
    manifest_upsert(dataset_id, path=info["path"], source=source, licence_status=licence_status, resolution=resolution,
                    tz=tz_note, start=info["start"], end=info["end"], sha256=info["sha256"], rows=info["rows"],
                    notes=notes, dry_run=dry_run, manifest=manifest)
    print(f"landed {dataset_id}: {info['rows']} rows {info['start']}..{info['end']} sha256={info['sha256'][:12]} -> {info['path']}")
    return info


def pin_check(path: Path, expected_sha256: Optional[str]) -> str:
    """Return the file's sha256; refuse (raise) on a mismatch with an expected pin."""
    sha = sha256_file(path)
    if expected_sha256 and sha != expected_sha256:
        raise RuntimeError(f"{path}: sha256 {sha} != pinned {expected_sha256}; refusing (inherited loader rule)")
    return sha
