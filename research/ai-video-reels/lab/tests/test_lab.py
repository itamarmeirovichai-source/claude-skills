import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import lab as L


def test_aggregate_winner_and_confidence():
    plan = {"jobs": [{"id": "T1__a", "tags": {"test": "T1", "model": "a"}},
                     {"id": "T1__b", "tags": {"test": "T1", "model": "b"}},
                     {"id": "T2__a", "tags": {"test": "T2", "model": "a"}},
                     {"id": "T2__b", "tags": {"test": "T2", "model": "b"}}]}
    key = {"X1": {"job": "T1__a", "est_usd": 1.0}, "X2": {"job": "T1__b", "est_usd": 0.4},
           "X3": {"job": "T2__a", "est_usd": 1.0}, "X4": {"job": "T2__b", "est_usd": 0.4}}
    s = lambda b, q, k: {"blind_id": b, **{c: q for c in L.SCORE_COLS}, "keep": k}
    scores = [s("X1", "5", "1"), s("X2", "3", "0"), s("X3", "4", "1"), s("X4", "3.8", "1")]
    agg = L.aggregate(scores, key, plan)
    assert agg["winners"]["T1"]["winner"] == "a" and agg["winners"]["T1"]["confident"]
    assert agg["winners"]["T2"]["winner"] == "a" and not agg["winners"]["T2"]["confident"]
    assert agg["by"]["model"]["b"]["usd_per_keeper"] == 0.8
    assert agg["by"]["model"]["a"]["keep_rate"] == 1.0


def test_plans_are_valid_and_refs_resolve():
    lab = Path(L.__file__).parent
    for p in lab.glob("experiments/*/plan.json"):
        plan = json.loads(p.read_text())
        ids = [j["id"] for j in plan["jobs"]]
        assert len(ids) == len(set(ids)), p
        for j in plan["jobs"]:
            for v in json.dumps(j["args"]).split('"'):
                if v.startswith("@file:"):
                    ref = (p.parent / v[6:]).resolve()
                    assert ref.parent == (lab / "assets").resolve(), (p, v)
