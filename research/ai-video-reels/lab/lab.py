#!/usr/bin/env python3
"""lab.py: budget control, blind evaluation and reports for the generation lab.

  status                  spend per experiment vs caps (from every clips/manifest.json) + gate state
  blind EXP               copy completed takes to EXP/blind/<random id>, write a hidden key,
                          contact sheets and an empty scores.csv (evaluator never sees model/style)
  report EXP              unblind scores, aggregate by tag (model/style/test), cost per keeper,
                          winners per test -> EXP/REPORT.md and a NOTEBOOK.md entry

Spend numbers come from the /estimate price recorded per completed take (hfgen manifest).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import random
import shutil
import string
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

LAB = Path(__file__).resolve().parent
ROOT = LAB.parent
REEL = ROOT.parents[1] / "skills" / "reel-studio" / "scripts" / "reelstudio.py"
CAPS = json.loads((LAB / "caps.json").read_text()) if (LAB / "caps.json").exists() else {}
SCORE_COLS = ["adherence", "fidelity", "artifacts", "motion", "aesthetic"]


def manifests() -> dict[str, Path]:
    out = {}
    for p in sorted(LAB.glob("experiments/*/clips/manifest.json")):
        out[p.parents[1].name] = p
    for p in sorted((ROOT / "packages").glob("*/clips/manifest.json")):
        out["prod:" + p.parents[1].name] = p
    return out


def spend(man: Path) -> tuple[float, int, int]:
    m = json.loads(man.read_text())
    takes = m.get("takes", {}).values()
    done = [t for t in takes if t.get("status") == "completed"]
    return sum(t.get("est_usd") or 0 for t in done), len(done), sum(1 for t in takes if t.get("status") != "completed")


def cmd_status() -> dict:
    total, rows = 0.0, []
    for name, man in manifests().items():
        usd, ok, bad = spend(man)
        total += usd
        cap = CAPS.get("experiments", {}).get(name)
        rows.append((name, usd, ok, bad, cap))
    lab_cap = CAPS.get("lab_cap_usd", 45)
    print(f"{'experiment':<28}{'spent':>9}{'ok':>5}{'fail':>6}{'cap':>8}")
    for n, u, ok, bad, cap in rows:
        flag = "  ⚠ OVER" if cap is not None and u > cap else ""
        print(f"{n:<28}{u:>9.2f}{ok:>5}{bad:>6}{(f'{cap:.2f}' if cap is not None else '-'):>8}{flag}")
    print(f"{'TOTAL':<28}{total:>9.2f}{'':>11}{lab_cap:>8.2f}")
    gates = CAPS.get("gates_usd", [10, 20, 35, 45])
    passed = [g for g in gates if total >= g]
    nxt = next((g for g in gates if total < g), None)
    print(f"gates passed: {passed or 'none'}; next stop-and-report at ${nxt}" if nxt else "LAB CAP REACHED: stop")
    return {"total": round(total, 2), "next_gate": nxt}


def _rid(n=5) -> str:
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def cmd_blind(exp: str, seed: int | None = None) -> Path:
    ed = LAB / "experiments" / exp
    man = json.loads((ed / "clips" / "manifest.json").read_text())
    bd = ed / "blind"
    if (bd / ".key.json").exists():
        raise SystemExit(f"{bd} already blinded; delete it to re-blind")
    bd.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    random.seed(seed)
    key, items = {}, []
    for k, t in man["takes"].items():
        if t.get("status") != "completed":
            continue
        for f in t.get("files", []):
            src = Path(f)
            if not src.is_absolute():
                src = (Path.cwd() / src)
            bid = _rid()
            while bid in key:
                bid = _rid()
            dst = bd / f"{bid}{src.suffix}"
            shutil.copy2(src, dst)
            key[bid] = {"take": k, "job": t["job"], "file": str(src), "est_usd": t.get("est_usd")}
            items.append(bid)
    rng.shuffle(items)
    (bd / ".key.json").write_text(json.dumps(key, indent=1))
    plan = json.loads((ed / "plan.json").read_text())
    tests = {j["id"]: j.get("tags", {}).get("test", "") for j in plan["jobs"]}
    with open(ed / "scores.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["blind_id", "test"] + SCORE_COLS + ["keep", "notes"])
        for bid in sorted(items, key=lambda b: (tests.get(key[b]["job"], ""), b)):
            w.writerow([bid, tests.get(key[bid]["job"], "")] + [""] * (len(SCORE_COLS) + 2))
    if REEL.exists():
        for bid in items:
            p = next(bd.glob(f"{bid}.*"))
            if p.suffix == ".mp4":
                subprocess.run([sys.executable, str(REEL), "grid", str(p), "--cols", "4", "--rows", "2",
                                "--out", str(bd / f"{bid}_sheet.jpg")], capture_output=True)
    print(f"blinded {len(items)} outputs -> {bd} ; fill {ed/'scores.csv'} (test is shown, model/style are hidden)")
    return bd


def aggregate(scores: list[dict], key: dict, plan: dict) -> dict:
    """Pure: returns per-tag means, keep rate, cost/keeper and per-test winners."""
    tags = {j["id"]: j.get("tags", {}) for j in plan["jobs"]}
    rows = []
    for s in scores:
        vals = [float(s[c]) for c in SCORE_COLS if str(s.get(c, "")).strip()]
        if not vals:
            continue
        k = key[s["blind_id"]]
        t = tags.get(k["job"], {})
        rows.append({"q": sum(vals) / len(vals), "keep": str(s.get("keep", "")).strip() in ("1", "y", "yes", "true"),
                     "usd": k.get("est_usd") or 0.0, **t})
    out: dict = {"n": len(rows), "by": {}, "winners": {}}
    dims = [d for d in ("model", "style") if any(d in r for r in rows)]
    for d in dims:
        g = defaultdict(list)
        for r in rows:
            g[r.get(d)].append(r)
        out["by"][d] = {}
        for v, rs in g.items():
            keeps = sum(r["keep"] for r in rs)
            usd = sum(r["usd"] for r in rs)
            out["by"][d][v] = {"n": len(rs), "quality": round(sum(r["q"] for r in rs) / len(rs), 2),
                               "keep_rate": round(keeps / len(rs), 2),
                               "usd": round(usd, 2), "usd_per_keeper": round(usd / keeps, 2) if keeps else None}
    if dims:
        d = dims[-1] if "style" in dims else dims[0]
        bt = defaultdict(lambda: defaultdict(list))
        for r in rows:
            bt[r.get("test")][r.get(d)].append(r["q"])
        for test, by in bt.items():
            ranked = sorted(((sum(q) / len(q), v) for v, q in by.items()), reverse=True)
            margin = ranked[0][0] - ranked[1][0] if len(ranked) > 1 else None
            out["winners"][test] = {"winner": ranked[0][1], "quality": round(ranked[0][0], 2),
                                    "margin": round(margin, 2) if margin is not None else None,
                                    "confident": margin is not None and margin >= 0.75}
    return out


def cmd_report(exp: str) -> dict:
    ed = LAB / "experiments" / exp
    key = json.loads((ed / "blind" / ".key.json").read_text())
    plan = json.loads((ed / "plan.json").read_text())
    scores = list(csv.DictReader(open(ed / "scores.csv")))
    agg = aggregate(scores, key, plan)
    L = [f"# {exp}: report ({dt.date.today()})", "", f"Scored outputs: {agg['n']} (blind)", ""]
    for d, vals in agg["by"].items():
        L += [f"## By {d}", "", f"| {d} | n | quality (1-5) | keep rate | $ | $/keeper |", "|---|---|---|---|---|---|"]
        for v, s in sorted(vals.items(), key=lambda kv: -kv[1]["quality"]):
            L.append(f"| {v} | {s['n']} | {s['quality']} | {s['keep_rate']:.0%} | {s['usd']} | {s['usd_per_keeper'] or '-'} |")
        L.append("")
    if agg["winners"]:
        L += ["## Winners per test", "", "| test | winner | quality | margin | confident? |", "|---|---|---|---|---|"]
        for t, w in sorted(agg["winners"].items()):
            L.append(f"| {t} | **{w['winner']}** | {w['quality']} | {w['margin']} | {'yes' if w['confident'] else 'no, replicate'} |")
    (ed / "REPORT.md").write_text("\n".join(L) + "\n")
    with open(LAB / "NOTEBOOK.md", "a") as fh:
        fh.write(f"\n### {dt.datetime.now():%Y-%m-%d %H:%M} · {exp} report\n")
        for t, w in sorted(agg["winners"].items()):
            fh.write(f"- {t}: {w['winner']} ({w['quality']}, margin {w['margin']}{'' if w['confident'] else ', NOT confident'})\n")
    print("\n".join(L))
    return agg


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="lab.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    b = sub.add_parser("blind"); b.add_argument("exp"); b.add_argument("--seed", type=int)
    r = sub.add_parser("report"); r.add_argument("exp")
    a = ap.parse_args(argv)
    if a.cmd == "status":
        cmd_status()
    elif a.cmd == "blind":
        cmd_blind(a.exp, a.seed)
    elif a.cmd == "report":
        cmd_report(a.exp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
