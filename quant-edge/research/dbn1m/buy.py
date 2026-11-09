"""Buy the three 1-minute datasets registered for Q-0017..Q-0021 (D-028) through the steward (estimate row first)."""
import sys, json
import databento as db
sys.path.insert(0, "src")
from qe import steward
PLAN = [("ES", "2010-06-06", "Q-0017;Q-0018;Q-0019;Q-0020;Q-0021"),
        ("GC", "2010-06-06", "Q-0019;Q-0021"),
        ("MES", "2019-05-06", "Q-0018;Q-0020")]
c = db.Historical(); credit = steward.load_credit(); jobs = {}
for root, start, rid in PLAN:
    kw = dict(dataset="GLBX.MDP3", symbols=[f"{root}.v.0"], schema="ohlcv-1m", start=start, end="2026-11-01", stype_in="continuous")
    est = steward.estimate(c, **kw)
    sub = lambda cl, kw=kw: cl.batch.submit_job(encoding="dbn", compression="zstd", **kw)["id"]
    r = steward.request(c, registered_id=rid, mode="batch", est=est, credit=credit, submit=sub)
    jobs[root] = r["job_id"]; print(root, f"est ${est['est_usd']:.3f}", "job", r["job_id"], "room before", r["room_usd"], flush=True)
json.dump(jobs, open("research/dbn1m/jobs.json", "w"), indent=1)
print(steward.ledger_state(month="2026-11"))
