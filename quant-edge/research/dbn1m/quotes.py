"""Free Databento cost quotes (metadata only, no purchase) for the remaining Databento queue, 1-minute bars."""
import json, sys
import databento as db
sys.path.insert(0, "src")
from qe import steward
c = db.Historical()
roots = sys.argv[1].split(",") if len(sys.argv) > 1 else ["ES","MES","NQ","MNQ","GC","SI","CL","NG","ZN"]
out = {}
for r in roots:
    start = "2019-05-06" if r in ("MES","MNQ") else "2010-06-06"
    e = steward.estimate(c, dataset="GLBX.MDP3", symbols=[f"{r}.v.0"], schema="ohlcv-1m", start=start, end="2026-11-01")
    out[r] = {"usd": round(e["est_usd"], 3), "records": e["est_records"], "start": start}
    print(r, out[r], flush=True)
json.dump(out, open("research/dbn1m/quotes_1m.json", "w"), indent=1)
