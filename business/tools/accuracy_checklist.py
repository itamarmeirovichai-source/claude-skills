#!/usr/bin/env python3
"""
Pre-delivery gate runner.

Walks Gate 1 (accuracy, business/26-property-accuracy-rules.md) and Gate 2
(quality, business/27-quality-rubric.md) for one order, and refuses to emit a
PASS unless every hard requirement is met.

The point is not the arithmetic. The point is that the gate cannot be skipped
silently at 11pm on a deadline, and that its outcome is written to a file that
can be produced later if a platform or a customer asks what we checked.

Run:  python3 business/tools/accuracy_checklist.py --order ORD-0001
      python3 business/tools/accuracy_checklist.py --order ORD-0001 --self-test
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Gate 1 - accuracy. Binary. Any NO fails the video.
# ---------------------------------------------------------------------------

GATE1 = [
    ("provenance", "Every clip maps to a named source photograph"),
    ("no_chaining", "No clip derived from another clip"),
    ("no_new_content", "No frame contains content absent from its source photo"),
    ("room_order", "Room order matches the property's real layout"),
    ("no_false_adjacency", "No implied adjacency that does not exist"),
    ("no_invented_openings", "No invented doorway, window, corridor or opening"),
    ("proportions", "Proportions consistent with the source photograph"),
    ("straight_lines", "Straight architectural lines remain straight"),
    ("numbers_from_factsheet", "Every on-screen number traces to the signed fact sheet"),
    ("capacity_reconciles", "Capacity reconciles to visible sleeping surfaces"),
    ("amenities_verified", "Every claimed amenity is visible or fact-sheet confirmed"),
    ("distances_stated", "Distances and times are stated values, not inferences"),
    ("no_accessibility_implication", "No accessibility implication unless verified"),
    ("views_from_photos", "Every window view traces to a supplied photograph"),
    ("no_view_extension", "No extension of a view beyond the photo's frame"),
    ("outdoor_extent", "Outdoor space shown at its real extent"),
    ("no_damage_removed", "No damage, wear or hazard removed"),
    ("no_generative_repair", "No generative cleaning or repair"),
    ("lighting_plausible", "Lighting plausible for orientation and stated time"),
    ("no_generated_ambience", "No generated ambience implying a sensory fact"),
    ("captions_factual", "Captions factually correct against the fact sheet"),
    ("claims_permitted", "No claim outside the claim register (21)"),
]

GATE1_VRBO = [
    ("vrbo_duration", "Vrbo cut is 15-60 seconds"),
    ("vrbo_no_music", "Vrbo cut has NO added music"),
    ("vrbo_no_contact", "No contact details anywhere in frame on the Vrbo cut"),
    ("vrbo_area_ratio", "Area footage <= 20% of Vrbo cut runtime (timed)"),
]

# Records that must exist before production even started.
PREREQS = [
    ("factsheet_signed", "Property Fact Sheet signed/confirmed by the customer"),
    ("rights_confirmed", "Written rights confirmation for the photography"),
    ("owner_authority", "Owner authority confirmed (PM orders; N/A -> yes for direct owners)"),
]

# ---------------------------------------------------------------------------
# Gate 2 - quality. Scored, with hard rejects that override the score.
# ---------------------------------------------------------------------------

GATE2 = [
    ("Q1", "Image artifacts", 2),
    ("Q2", "Geometry (straight lines stay straight)", 3),
    ("Q3", "Texture stability", 2),
    ("Q4", "Flicker", 2),
    ("Q5", "Object continuity", 3),
    ("Q6", "Lighting continuity", 2),
    ("Q7", "Motion plausibility", 2),
    ("Q8", "Camera movement", 1),
    ("Q9", "Framing / cropping", 1),
    ("Q10", "Text legibility (checked ON A PHONE)", 2),
    ("Q11", "Caption accuracy", 2),
    ("Q12", "Audio quality", 1),
    ("Q13", "Brand consistency", 1),
    ("Q14", "Export correctness", 2),
]

MAX_SCORE = sum(w for _, _, w in GATE2) * 5  # 130

HARD_REJECTS = [
    ("HR-1", "Architectural geometry warps (wall/doorframe/window/counter bends)"),
    ("HR-2", "An object appears, disappears, or morphs between frames"),
    ("HR-3", "A person, animal, or reflection is generated"),
    ("HR-4", "Text illegible on a phone at arm's length"),
    ("HR-5", "A caption states a fact absent from the fact sheet"),
    ("HR-6", "Audio clips, or music present on the Vrbo cut"),
    ("HR-7", "Contact details in frame on the Vrbo cut"),
    ("HR-8", "A file exceeds its platform spec (GBP >75MB/>30s; Vrbo >2min/<15s)"),
    ("HR-9", "Silent loop first and last frames do not match"),
    ("HR-10", "Motion so strong the source photograph is unrecognisable"),
]

DELIVER_THRESHOLD = 110
REBUILD_THRESHOLD = 90


@dataclass
class Result:
    order_id: str
    reviewer: str
    timestamp: str
    prereqs: dict = field(default_factory=dict)
    gate1: dict = field(default_factory=dict)
    gate2_scores: dict = field(default_factory=dict)
    hard_rejects: dict = field(default_factory=dict)
    gate2_total: int = 0
    outcome: str = "INCOMPLETE"
    blocking: list = field(default_factory=list)


def ask_yes_no(prompt: str, auto: str | None = None) -> bool:
    if auto is not None:
        return auto == "y"
    while True:
        a = input(f"  {prompt} [y/n] ").strip().lower()
        if a in ("y", "n"):
            return a == "y"
        print("    answer y or n")


def ask_score(label: str, weight: int, auto: int | None = None) -> int:
    if auto is not None:
        return auto
    while True:
        a = input(f"  {label} (x{weight}) [0-5] ").strip()
        if a.isdigit() and 0 <= int(a) <= 5:
            return int(a)
        print("    enter 0-5")


def run(order_id: str, reviewer: str, has_vrbo: bool, auto: dict | None = None) -> Result:
    a = auto or {}
    res = Result(
        order_id=order_id,
        reviewer=reviewer,
        timestamp=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    )

    print("\n" + "=" * 74)
    print(f"PRE-PRODUCTION RECORDS - order {order_id}")
    print("=" * 74)
    for key, text in PREREQS:
        ok = ask_yes_no(text, a.get(key))
        res.prereqs[key] = ok
        if not ok:
            res.blocking.append(f"PREREQ FAILED: {text}")

    print("\n" + "=" * 74)
    print("GATE 1 - ACCURACY (binary; any NO fails the video)")
    print("Open each clip beside its source photograph before answering.")
    print("=" * 74)
    items = GATE1 + (GATE1_VRBO if has_vrbo else [])
    for key, text in items:
        ok = ask_yes_no(text, a.get(key))
        res.gate1[key] = ok
        if not ok:
            res.blocking.append(f"GATE 1 FAILED: {text}")

    print("\n" + "=" * 74)
    print("GATE 2 - HARD REJECTS (any YES blocks delivery, whatever the score)")
    print("=" * 74)
    for code, text in HARD_REJECTS:
        present = ask_yes_no(f"{code}: {text} -- PRESENT?", a.get(code))
        res.hard_rejects[code] = present
        if present:
            res.blocking.append(f"HARD REJECT {code}: {text}")

    print("\n" + "=" * 74)
    print("GATE 2 - QUALITY SCORE")
    print("=" * 74)
    total = 0
    for code, label, weight in GATE2:
        s = ask_score(f"{code} {label}", weight, a.get(code))
        res.gate2_scores[code] = s
        total += s * weight
    res.gate2_total = total

    # ---- outcome ----
    if res.blocking:
        res.outcome = "BLOCKED - DO NOT DELIVER"
    elif total < REBUILD_THRESHOLD:
        res.outcome = f"REBUILD (score {total}/{MAX_SCORE}, below {REBUILD_THRESHOLD})"
        res.blocking.append("Score below rebuild threshold - rebuild from storyboard, do not patch")
    elif total < DELIVER_THRESHOLD:
        res.outcome = f"FIX AND RE-REVIEW (score {total}/{MAX_SCORE})"
        lowest = sorted(res.gate2_scores.items(), key=lambda kv: kv[1])[:3]
        res.blocking.append("Fix lowest-scoring criteria then re-run: "
                            + ", ".join(f"{k}={v}" for k, v in lowest))
    else:
        res.outcome = f"PASS - DELIVER (score {total}/{MAX_SCORE})"

    return res


def report(res: Result) -> None:
    print("\n" + "=" * 74)
    print(f"OUTCOME: {res.outcome}")
    print("=" * 74)
    print(f"  Order:     {res.order_id}")
    print(f"  Reviewer:  {res.reviewer}")
    print(f"  Timestamp: {res.timestamp}")
    print(f"  Gate 2:    {res.gate2_total}/{MAX_SCORE}")
    if res.blocking:
        print("\n  BLOCKING ITEMS:")
        for b in res.blocking:
            print(f"    - {b}")
        print("\n  A blocked video is not delivered. If it cannot be fixed, the")
        print("  deadline moves and the customer is told why (26 section 7).")
    else:
        print("\n  Both gates passed. Proceed to export.")
    print()


def save(res: Result, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{res.order_id}-review.json"
    path.write_text(json.dumps(asdict(res), indent=2))
    return path


def self_test() -> int:
    """Non-interactive checks that the gate actually blocks what it should."""
    print("Running self-test (non-interactive)...\n")
    failures = 0

    all_good: dict = {k: "y" for k, _ in PREREQS + GATE1 + GATE1_VRBO}
    all_good.update({c: "n" for c, _ in HARD_REJECTS})
    all_good.update({c: 5 for c, _, _ in GATE2})

    r = run("TEST-PASS", "self-test", True, all_good)
    if not r.outcome.startswith("PASS"):
        print(f"  FAIL: perfect input should PASS, got {r.outcome}")
        failures += 1
    else:
        print(f"  ok: perfect input -> {r.outcome}")

    one_hr = dict(all_good, **{"HR-1": "y"})
    r = run("TEST-HR", "self-test", True, one_hr)
    if not r.outcome.startswith("BLOCKED"):
        print(f"  FAIL: hard reject should BLOCK even at full score, got {r.outcome}")
        failures += 1
    else:
        print(f"  ok: HR-1 at full score -> {r.outcome}")

    one_g1 = dict(all_good, **{"no_view_extension": "n"})
    r = run("TEST-G1", "self-test", True, one_g1)
    if not r.outcome.startswith("BLOCKED"):
        print(f"  FAIL: a Gate 1 NO should BLOCK, got {r.outcome}")
        failures += 1
    else:
        print(f"  ok: single Gate 1 failure at full score -> {r.outcome}")

    no_prereq = dict(all_good, **{"rights_confirmed": "n"})
    r = run("TEST-PRE", "self-test", True, no_prereq)
    if not r.outcome.startswith("BLOCKED"):
        print(f"  FAIL: missing rights confirmation should BLOCK, got {r.outcome}")
        failures += 1
    else:
        print(f"  ok: missing rights confirmation -> {r.outcome}")

    # all 3s = 78/130, below the rebuild threshold
    poor = dict(all_good, **{c: 3 for c, _, _ in GATE2})
    r = run("TEST-POOR", "self-test", True, poor)
    if "REBUILD" not in r.outcome:
        print(f"  FAIL: all-3s (78/130) should REBUILD, got {r.outcome}")
        failures += 1
    else:
        print(f"  ok: all-3s (78/130) -> {r.outcome}")

    # all 4s = 104/130, in the 90-109 fix-and-re-review band
    mediocre = dict(all_good, **{c: 4 for c, _, _ in GATE2})
    r = run("TEST-MID", "self-test", True, mediocre)
    if "FIX AND RE-REVIEW" not in r.outcome:
        print(f"  FAIL: all-4s (104/130) should need FIX AND RE-REVIEW, got {r.outcome}")
        failures += 1
    else:
        print(f"  ok: all-4s (104/130) -> {r.outcome}")

    print(f"\n{'ALL SELF-TESTS PASSED' if not failures else f'{failures} SELF-TEST FAILURE(S)'}")
    return 1 if failures else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--order", help="order id, e.g. ORD-0001")
    p.add_argument("--reviewer", default="founder")
    p.add_argument("--no-vrbo", action="store_true",
                   help="order has no Vrbo cut (Starter package)")
    p.add_argument("--out", default="reviews", help="directory for the review record")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()

    if args.self_test:
        return self_test()

    if not args.order:
        p.error("--order is required (or use --self-test)")

    res = run(args.order, args.reviewer, not args.no_vrbo)
    report(res)
    path = save(res, Path(args.out))
    print(f"  Review record written to {path}\n")
    return 0 if res.outcome.startswith("PASS") else 2


if __name__ == "__main__":
    sys.exit(main())
