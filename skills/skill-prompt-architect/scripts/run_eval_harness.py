#!/usr/bin/env python3
"""Create and score before/after benchmark runs for skill packages."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DIMENSIONS = [
    ("trigger_correctness", 20, "Correct trigger/non-trigger behavior for the case."),
    ("artifact_quality", 20, "Completeness and usefulness of the produced artifact."),
    ("domain_specificity", 15, "Uses concrete domain constraints instead of generic advice."),
    ("validation_quality", 15, "Includes realistic checks, evals, or deterministic validation."),
    ("safety_boundary", 10, "Handles unsafe, private, or tool-sensitive behavior correctly."),
    ("delivery_completeness", 10, "Gives install, packaging, or handoff details when relevant."),
    ("concision_cost", 10, "Avoids unnecessary ceremony, verbosity, or context cost."),
]


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Missing file: {path}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from None


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def slug(value):
    cleaned = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in value.lower())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or "case"


def skill_name(skill_dir):
    frontmatter = skill_dir / "SKILL.md"
    if not frontmatter.exists():
        return skill_dir.name
    for line in frontmatter.read_text(encoding="utf-8").splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("'\"") or skill_dir.name
    return skill_dir.name


def load_cases(skill_dir, eval_path, selected):
    path = eval_path if eval_path.is_absolute() else skill_dir / eval_path
    data = read_json(path)
    cases = data.get("evals")
    if not isinstance(cases, list):
        raise SystemExit(f"{path} must contain an `evals` list.")
    if selected:
        cases = [case for case in cases if case.get("id") in selected]
        missing = selected - {case.get("id") for case in cases}
        if missing:
            raise SystemExit(f"Selected case ids not found: {', '.join(sorted(missing))}")
    return cases


def prompt_text(case, mode, name):
    mode_label = "WITHOUT using the skill" if mode == "baseline" else "WITH the skill enabled"
    extra = (
        "Do not load or follow the skill package. Answer as a strong general Claude instance."
        if mode == "baseline"
        else f"Use the `{name}` skill and its bundled resources when applicable."
    )
    return f"""# Benchmark Prompt: {case.get('id', 'case')}

Run this task {mode_label}.

{extra}

## User Prompt

{case.get('prompt', '')}

## Expected Behavior

{case.get('expected_output', '')}

## Assertions To Check Later

{chr(10).join('- ' + str(item) for item in case.get('assertions', []))}
"""


def empty_scorecard(case):
    def side():
        return {
            "critical_failure": False,
            "scores": {name: None for name, _, _ in DIMENSIONS},
            "notes": "",
        }
    return {
        "case_id": case.get("id"),
        "should_trigger": case.get("should_trigger"),
        "expected_output": case.get("expected_output"),
        "baseline_without_skill": case.get("baseline_without_skill"),
        "dimensions": [
            {"name": name, "weight": weight, "description": description}
            for name, weight, description in DIMENSIONS
        ],
        "baseline": side(),
        "with_skill": side(),
        "blockers": [],
        "winner": None,
        "review_notes": "",
    }


def init_run(args):
    skill_dir = args.skill_dir.resolve()
    name = skill_name(skill_dir)
    cases = load_cases(skill_dir, args.evals, set(args.case) if args.case else None)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    out_root = args.out.resolve() if args.out else skill_dir.parent / "eval-runs"
    run_dir = out_root / f"{stamp}-{name}"
    case_dir = run_dir / "cases"
    case_dir.mkdir(parents=True, exist_ok=False)

    metadata = {
        "skill_name": name,
        "skill_dir": str(skill_dir),
        "created_at_utc": stamp,
        "case_count": len(cases),
        "gate": {
            "minimum_with_skill_score": args.min_score,
            "minimum_average_delta": args.min_delta,
            "target_100": args.target_100,
            "no_with_skill_critical_failures": True,
        },
        "blockers": [],
        "workflow": [
            "Run each baseline_prompt.md without using the skill and save baseline_output.md.",
            "Run each with_skill_prompt.md with the skill enabled and save with_skill_output.md.",
            "Fill each scorecard.json with 0-5 scores for baseline and with_skill.",
            "Run this script with `score <run-dir>` to compute summary.json.",
        ],
    }
    write_json(run_dir / "metadata.json", metadata)

    for case in cases:
        case_id = slug(str(case.get("id", "case")))
        folder = case_dir / case_id
        folder.mkdir()
        (folder / "prompt.md").write_text(str(case.get("prompt", "")) + "\n", encoding="utf-8")
        (folder / "baseline_prompt.md").write_text(prompt_text(case, "baseline", name), encoding="utf-8")
        (folder / "with_skill_prompt.md").write_text(prompt_text(case, "with_skill", name), encoding="utf-8")
        (folder / "baseline_output.md").write_text("# Paste baseline output here\n", encoding="utf-8")
        (folder / "with_skill_output.md").write_text("# Paste with-skill output here\n", encoding="utf-8")
        write_json(folder / "scorecard.json", empty_scorecard(case))

    print(run_dir)
    return 0


def weighted_score(side):
    scores = side.get("scores", {})
    total = 0.0
    for name, weight, _ in DIMENSIONS:
        value = scores.get(name)
        if value is None:
            return None
        if not isinstance(value, (int, float)) or not 0 <= value <= 5:
            raise ValueError(f"{name} must be a number from 0 to 5.")
        total += (float(value) / 5.0) * weight
    if side.get("critical_failure"):
        total = min(total, 69.0)
    return round(total, 2)


def filled_output(path):
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8").strip()
    return bool(text and text != "# Paste baseline output here" and text != "# Paste with-skill output here")


def score_run(args):
    run_dir = args.run_dir.resolve()
    metadata = read_json(run_dir / "metadata.json")
    target_100 = bool(args.target_100 or metadata.get("gate", {}).get("target_100"))
    min_score = float(args.min_score if args.min_score is not None else metadata["gate"]["minimum_with_skill_score"])
    if target_100:
        min_score = 100.0
    min_delta = float(args.min_delta if args.min_delta is not None else metadata["gate"]["minimum_average_delta"])

    results = []
    errors = []
    for folder in sorted((run_dir / "cases").iterdir()):
        if not folder.is_dir():
            continue
        card_path = folder / "scorecard.json"
        try:
            card = read_json(card_path)
            baseline = weighted_score(card.get("baseline", {}))
            with_skill = weighted_score(card.get("with_skill", {}))
        except (SystemExit, ValueError) as exc:
            errors.append(f"{folder.name}: {exc}")
            continue

        if baseline is None or with_skill is None:
            errors.append(f"{folder.name}: incomplete scorecard")
            continue
        if not args.allow_missing_outputs:
            if not filled_output(folder / "baseline_output.md"):
                errors.append(f"{folder.name}: missing baseline_output.md")
            if not filled_output(folder / "with_skill_output.md"):
                errors.append(f"{folder.name}: missing with_skill_output.md")
        blockers = card.get("blockers", [])
        if blockers:
            errors.append(f"{folder.name}: unresolved blockers: {', '.join(map(str, blockers))}")

        delta = round(with_skill - baseline, 2)
        winner = "with_skill" if delta > 0 else "baseline" if delta < 0 else "tie"
        results.append({
            "case_id": card.get("case_id", folder.name),
            "should_trigger": card.get("should_trigger"),
            "baseline_score": baseline,
            "with_skill_score": with_skill,
            "delta": delta,
            "winner": winner,
            "with_skill_critical_failure": bool(card.get("with_skill", {}).get("critical_failure")),
        })

    if not results:
        errors.append("No scored cases found.")

    avg_baseline = round(sum(item["baseline_score"] for item in results) / len(results), 2) if results else 0
    avg_with = round(sum(item["with_skill_score"] for item in results) / len(results), 2) if results else 0
    avg_delta = round(avg_with - avg_baseline, 2)
    critical_failures = [item["case_id"] for item in results if item["with_skill_critical_failure"]]
    target_100_failures = [
        item["case_id"] for item in results
        if target_100 and item["with_skill_score"] != 100.0
    ]
    run_blockers = metadata.get("blockers", [])
    if run_blockers:
        errors.append(f"Run metadata has unresolved blockers: {', '.join(map(str, run_blockers))}")
    passed = (
        not errors and avg_with >= min_score and avg_delta >= min_delta
        and not critical_failures and not target_100_failures
    )
    summary = {
        "ok": passed,
        "target_100": target_100,
        "skill_name": metadata.get("skill_name"),
        "case_count": len(results),
        "average_baseline_score": avg_baseline,
        "average_with_skill_score": avg_with,
        "average_delta": avg_delta,
        "minimum_with_skill_score": min_score,
        "minimum_average_delta": min_delta,
        "critical_failures": critical_failures,
        "target_100_failures": target_100_failures,
        "errors": errors,
        "results": results,
    }
    write_json(run_dir / "summary.json", summary)

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print("OK" if passed else "FAILED")
        if target_100:
            print("target 100 gate: enabled")
        print(f"baseline avg: {avg_baseline}")
        print(f"with-skill avg: {avg_with}")
        print(f"delta: {avg_delta}")
        for error in errors:
            print(f"- {error}", file=sys.stderr)
    return 0 if passed else 1


def main():
    parser = argparse.ArgumentParser(description="Run a before/after skill benchmark harness.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a benchmark run directory from evals/evals.json")
    init.add_argument("skill_dir", type=Path)
    init.add_argument("--evals", type=Path, default=Path("evals/evals.json"))
    init.add_argument("--out", type=Path)
    init.add_argument("--case", action="append", default=[])
    init.add_argument("--min-score", type=float, default=85.0)
    init.add_argument("--min-delta", type=float, default=10.0)
    init.add_argument("--target-100", action="store_true")
    init.set_defaults(func=init_run)

    score = sub.add_parser("score", help="Score a benchmark run after outputs and scorecards are filled")
    score.add_argument("run_dir", type=Path)
    score.add_argument("--min-score", type=float)
    score.add_argument("--min-delta", type=float)
    score.add_argument("--allow-missing-outputs", action="store_true")
    score.add_argument("--target-100", action="store_true")
    score.add_argument("--json", action="store_true")
    score.set_defaults(func=score_run)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
