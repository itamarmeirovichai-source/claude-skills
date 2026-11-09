"""Databento Steward: the only code path allowed to touch paid endpoints.

Money controls (resources_and_budget, operating rules 1-4):
- The key is read from DATABENTO_API_KEY by the databento client itself; this module never reads, prints or stores it.
- No paid call before `quant-edge/data/databento_credit.json` exists with Itamar's confirmed credit, expiry, signup date and
  the portal monthly limit (written by the Director from his message, never assumed).
- Before every paid request: get_cost, get_record_count, get_billable_size with identical arguments; start/end aligned to
  10-minute multiples; an estimate row is written to the spend ledger BEFORE the request; a row without an actual counts at
  its estimate. Submit only if est_usd <= min(ceiling - cumulative, monthly_limit - month_to_date) - 1.
- Every purchase above $1 goes through batch.submit_job; streaming only for probes under $1 and the per-day window plan.
"""
import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from . import paths

LEDGER = paths.PROGRAM_ROOT / "data" / "databento_spend_ledger.csv"
CREDIT_FILE = paths.PROGRAM_ROOT / "data" / "databento_credit.json"
LEDGER_COLS = ["ts_utc", "registered_id", "mode", "job_id", "dataset", "stype_in", "symbols", "schema", "start", "end",
               "est_records", "est_bytes", "est_usd", "billed_bytes", "billed_usd", "status", "billing_month",
               "month_to_date_usd", "cumulative_usd", "portal_credit_remaining_usd", "manifest_path"]
PLAN_CEILING_MAX = 94.0
HARD_CAP_MAX = 105.0
SAFETY_MARGIN_USD = 1.0


class SpendBlocked(RuntimeError):
    pass


class CreditUnconfirmed(SpendBlocked):
    pass


def key_present() -> bool:
    return bool(os.environ.get("DATABENTO_API_KEY"))


def load_credit(credit_file: Optional[Path] = None) -> dict:
    """Itamar's confirmation, as written by the Director: {"remaining_credit_usd", "expiry_date", "signup_date",
    "portal_monthly_limit_usd", "confirmed_on", "pay_as_you_go": "off|on|unknown"}."""
    credit_file = credit_file or CREDIT_FILE
    if not credit_file.exists():
        raise CreditUnconfirmed("databento_credit.json is missing: Day-0 items (a) and (b) are not confirmed; no paid call allowed")
    c = json.loads(credit_file.read_text())
    for k in ("remaining_credit_usd", "expiry_date", "signup_date", "portal_monthly_limit_usd", "confirmed_on"):
        if k not in c:
            raise CreditUnconfirmed(f"databento_credit.json lacks {k!r}")
    return c


def ceilings(credit: dict) -> dict:
    rem = float(credit["remaining_credit_usd"])
    plan = min(PLAN_CEILING_MAX, rem - 20.0)
    hard = min(HARD_CAP_MAX, 0.85 * rem)
    monthly = float(credit["portal_monthly_limit_usd"])
    if monthly > hard + 1e-9:
        raise SpendBlocked(f"portal monthly limit {monthly} exceeds DATABENTO_HARD_CAP_USD {hard:.2f}; ask Itamar to lower it")
    if plan <= 0:
        raise SpendBlocked(f"plan ceiling {plan:.2f} <= 0: remaining credit {rem} is too small for any paid plan")
    return {"plan_ceiling_usd": plan, "hard_cap_usd": hard, "monthly_limit_usd": monthly}


def _rows(ledger: Path):
    if not ledger.exists():
        return []
    with open(ledger, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _request_key(r: dict) -> tuple:
    return (r.get("ts_utc"), r.get("registered_id"), r.get("dataset"), r.get("schema"), r.get("symbols"), r.get("start"), r.get("end"))


def ledger_state(ledger: Optional[Path] = None, month: Optional[str] = None) -> dict:
    """Cumulative and month-to-date spend. The ledger is append-only: a request appears as an `estimated` row and is
    later superseded by a `submitted` / `done` / `failed` row with the same request key (oldest open estimate first).
    Each request counts once, at its last row; an estimate never superseded counts at its estimate; failed rows count 0."""
    ledger = ledger or LEDGER
    final = []
    open_est = {}
    for r in _rows(ledger):
        k = _request_key(r)
        if r.get("status") == "estimated":
            final.append(r)
            open_est.setdefault(k, []).append(len(final) - 1)
        else:
            q = open_est.get(k)
            if q:
                final[q.pop(0)] = r
            else:
                final.append(r)
    cum = 0.0
    mtd = 0.0
    for r in final:
        if r.get("status") == "failed":
            continue
        amt = float(r.get("billed_usd") or r.get("est_usd") or "0")
        cum += amt
        if month and r.get("billing_month") == month:
            mtd += amt
    return {"cumulative_usd": round(cum, 4), "month_to_date_usd": round(mtd, 4)}


def _aligned_10min(ts: str) -> bool:
    t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return t.minute % 10 == 0 and t.second == 0 and t.microsecond == 0


def estimate(client, *, dataset: str, symbols, schema: str, start: str, end: str, stype_in: str = "continuous") -> dict:
    """Free metadata calls with identical arguments. `client` is a databento.Historical (or a test double)."""
    for ts in (start, end):
        if "T" in ts and not _aligned_10min(ts):
            raise ValueError(f"{ts} is not aligned to a 10-minute multiple")
    kw = dict(dataset=dataset, symbols=symbols, schema=schema, start=start, end=end, stype_in=stype_in)
    cost = float(client.metadata.get_cost(**kw))
    recs = int(client.metadata.get_record_count(**kw))
    size = int(client.metadata.get_billable_size(**kw))
    return {"est_usd": cost, "est_records": recs, "est_bytes": size, **kw}


def allowed(est_usd: float, credit: dict, ledger: Optional[Path] = None, month: Optional[str] = None) -> dict:
    c = ceilings(credit)
    st = ledger_state(ledger, month)
    room = min(c["plan_ceiling_usd"] - st["cumulative_usd"], c["monthly_limit_usd"] - st["month_to_date_usd"]) - SAFETY_MARGIN_USD
    ok = est_usd <= room
    return {"ok": ok, "room_usd": round(room, 4), "est_usd": est_usd, **c, **st,
            "reason": "" if ok else f"est {est_usd:.4f} > room {room:.4f}: shrink the request (fewer roots, shorter range, narrower windows)"}


def write_row(row: dict, ledger: Optional[Path] = None) -> None:
    ledger = ledger or LEDGER
    new = not ledger.exists() or ledger.stat().st_size == 0
    with open(ledger, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_COLS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in LEDGER_COLS})


def request(client, *, registered_id: str, mode: str, est: dict, credit: dict, ledger: Optional[Path] = None,
            now: Optional[datetime] = None, submit=None, portal_credit_remaining: str = "") -> dict:
    """Write the estimate row, check the ceilings, then (and only then) call `submit(client)` which must return a job_id
    or a stream handle. mode: 'batch' (>= $1) or 'stream' (< $1 probes / per-day windows)."""
    ledger = ledger or LEDGER
    if not registered_id:
        raise SpendBlocked("a paid request needs the registry row id (or CAL) that names this data")
    if mode == "stream" and est["est_usd"] >= 1.0:
        raise SpendBlocked(f"est {est['est_usd']:.2f} >= $1 must go through batch.submit_job, not streaming")
    now = now or datetime.now(timezone.utc)
    month = now.strftime("%Y-%m")
    chk = allowed(est["est_usd"], credit, ledger, month)
    base = {"ts_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "registered_id": registered_id, "mode": mode,
            "dataset": est["dataset"], "stype_in": est["stype_in"], "symbols": ";".join(est["symbols"]) if isinstance(est["symbols"], (list, tuple)) else est["symbols"],
            "schema": est["schema"], "start": est["start"], "end": est["end"], "est_records": est["est_records"],
            "est_bytes": est["est_bytes"], "est_usd": f"{est['est_usd']:.6f}", "billing_month": month,
            "month_to_date_usd": f"{chk['month_to_date_usd']:.4f}", "cumulative_usd": f"{chk['cumulative_usd']:.4f}",
            "portal_credit_remaining_usd": portal_credit_remaining}
    if not chk["ok"]:
        write_row({**base, "status": "failed", "job_id": "", "manifest_path": chk["reason"]}, ledger)
        raise SpendBlocked(chk["reason"])
    write_row({**base, "status": "estimated"}, ledger)     # the estimate row exists before any paid call
    if submit is None:
        return {"status": "estimated", **chk}
    job_id = submit(client)
    write_row({**base, "status": "submitted", "job_id": str(job_id),
               "cumulative_usd": f"{chk['cumulative_usd'] + est['est_usd']:.4f}",
               "month_to_date_usd": f"{chk['month_to_date_usd'] + est['est_usd']:.4f}"}, ledger)
    return {"status": "submitted", "job_id": job_id, **chk}
