#!/usr/bin/env python3
"""Seed quant-edge/registry.csv from the inherited MeiroX ledger (105 rows, count sum 280).

Usage: python3 quant-edge/tools/seed_registry.py <inherited_ledger.csv> <out registry.csv>
Inherited rows keep their id, date, owner, hypothesis, count, rules_fixed_before_test, data,
result_mean_R, result_p5_R, passed_gate and notes verbatim; the new columns are filled with
'inherited' or left blank. Nothing in an inherited row is ever edited afterwards.
"""
import csv, sys, re

COLUMNS = [
    "id", "date", "owner", "source", "family", "lane", "status", "hypothesis", "rules",
    "parameters", "grid", "sign", "instruments", "holding", "firm_structure", "data",
    "data_sha256", "split", "vol_scaler", "guard_fraction", "decay_haircut", "cost_model",
    "decision_rule", "count", "rules_fixed_before_test", "result_mean_R", "result_p5_R",
    "result_units", "passed_gate", "registered_commit", "notes",
]

FAMILY = {
    "H0001": "bot-smc-tjr", "H0002": "bot-smc-tjr", "H0003": "bot-smc-tjr", "H0004": "bot-smc-tjr",
    "H0010": "bot-smc-tjr", "H0016": "bot-smc-tjr",
    "H0005": "noise-area-intraday-momentum", "H0011": "noise-area-intraday-momentum",
    "H0006": "last-half-hour-momentum", "H0019": "last-half-hour-momentum",
    "H0007": "multi-day-trend-futures",
    "H0012": "overnight-gap-fade", "H0017": "overnight-gap-fade",
    "H0013": "intraday-ibs-reversal", "H0014": "intraday-ibs-reversal",
    "H0018": "insider-purchases",
    "H0020": "orb-5min", "H0021": "vwap-trend-intraday", "H0022": "vwap-trend-intraday",
    "H0023": "turn-of-month",
}
PREFIX_FAMILY = {
    "D1": "economics-ftmo-lottery", "D2": "fx-cfd-daily-trend-carry", "D3": "crypto-binance",
    "D4": "intraday-breadth-cfd", "E1": "stock-cfd-anomalies", "E2": "macro-events-intraday",
    "F1": "ensemble-near-misses", "F2": "economics-stress-model", "G2": "buy-the-dip-index-cfd",
}

def family_of(id_, hyp):
    if id_ in FAMILY:
        return FAMILY[id_]
    p = id_.split("-")[0]
    if p in PREFIX_FAMILY:
        return PREFIX_FAMILY[p]
    h = hyp.lower()
    if "stack" in h or "ensemble" in h:
        return "inherited-stack"
    if "trend" in h:
        return "multi-day-trend-futures"
    return f"inherited-misc"

def units_of(notes):
    m = re.search(r"result fields\s*=\s*([^;.]+)", notes or "")
    return m.group(1).strip() if m else ""

def main(src, dst):
    rows = list(csv.DictReader(open(src, newline="", encoding="utf-8")))
    out = []
    total = 0
    for r in rows:
        c = (r.get("count") or "").strip()
        n = int(c) if c.isdigit() else 0
        total += n
        econ = r["id"].startswith(("D1", "F2"))
        out.append({
            "id": r["id"], "date": r["date"], "owner": r["owner"], "source": "inherited",
            "family": family_of(r["id"], r["hypothesis"]), "lane": "inherited",
            "status": "inherited-economics" if econ else "inherited-closed",
            "hypothesis": r["hypothesis"], "rules": "inherited: see skills/prop-fleet ledger/prereg",
            "parameters": "inherited", "grid": "inherited", "sign": "inherited", "instruments": "inherited",
            "holding": "inherited", "firm_structure": "inherited", "data": r["data"], "data_sha256": "inherited",
            "split": "inherited", "vol_scaler": "inherited", "guard_fraction": "", "decay_haircut": "",
            "cost_model": "inherited", "decision_rule": "inherited", "count": c,
            "rules_fixed_before_test": r["rules_fixed_before_test"], "result_mean_R": r["result_mean_R"],
            "result_p5_R": r["result_p5_R"], "result_units": units_of(r.get("notes", "")),
            "passed_gate": r["passed_gate"], "registered_commit": "e0f5e59 (origin/claude/friendly-galileo-eakzlm)",
            "notes": r["notes"],
        })
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, quoting=csv.QUOTE_MINIMAL)
        w.writeheader(); w.writerows(out)
    print(f"wrote {len(out)} rows, count sum {total}")
    fams = {}
    for o in out:
        fams.setdefault(o["family"], []).append(o["id"])
    for k, v in sorted(fams.items()):
        print(f"  {k:32s} {len(v):3d}  {', '.join(v[:6])}{' ...' if len(v) > 6 else ''}")
    for o in out:
        if o["family"] == "inherited-misc":
            print("  MISC:", o["id"], o["hypothesis"][:110])

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
