#!/usr/bin/env python3
"""Validate an Agent Skill package. Dependency-free."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PATH_RE = re.compile(r"`((?:references|scripts|assets|evals)/[^`]+)`")


def add(result, level, message):
    result[level].append(message)


def parse_frontmatter(text, result):
    if not text.startswith("---\n"):
        add(result, "errors", "SKILL.md must start with YAML frontmatter.")
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        add(result, "errors", "SKILL.md frontmatter is missing closing --- marker.")
        return {}
    fields = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        if ":" not in line:
            add(result, "warnings", f"Unparsed frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip("\"'")
    return fields


def referenced_paths(text):
    paths = set()
    for match in LINK_RE.findall(text):
        if match.startswith(("http://", "https://", "#", "mailto:")):
            continue
        paths.add(match.split("#", 1)[0])
    for match in PATH_RE.findall(text):
        paths.add(match)
    return paths


def validate_skill(skill_dir, max_description, max_lines, warn_lines,
                   min_negative_evals, require_baselines, require_eval_runner,
                   require_100_gate, require_export_script):
    result = {"errors": [], "warnings": [], "info": []}

    if not skill_dir.exists():
        add(result, "errors", f"Skill directory does not exist: {skill_dir}")
        return result
    if not skill_dir.is_dir():
        add(result, "errors", f"Skill path is not a directory: {skill_dir}")
        return result

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(result, "errors", "Missing SKILL.md.")
        return result

    text = skill_md.read_text(encoding="utf-8")
    fields = parse_frontmatter(text, result)
    name = fields.get("name", "")
    description = fields.get("description", "")

    if not name:
        add(result, "errors", "Frontmatter is missing required `name`.")
    elif not NAME_RE.match(name):
        add(result, "errors", "`name` must use lowercase letters, numbers, and single hyphens only.")
    elif name != skill_dir.name:
        add(result, "errors", f"`name` ({name}) must match directory name ({skill_dir.name}).")

    if not description:
        add(result, "errors", "Frontmatter is missing required `description`.")
    else:
        if len(description) > 1024:
            add(result, "errors", "`description` exceeds 1024 characters.")
        if len(description) > max_description:
            add(result, "warnings", f"`description` is {len(description)} chars; target is {max_description}.")
        if "use when" not in description.lower() and "when" not in description.lower():
            add(result, "warnings", "`description` should say when to use the skill.")

    line_count = len(text.splitlines())
    if line_count > warn_lines:
        add(result, "warnings", f"SKILL.md has {line_count} lines; release target is <= {warn_lines}.")
    if line_count > max_lines:
        add(result, "warnings", f"SKILL.md has {line_count} lines; target is <= {max_lines}.")
    else:
        add(result, "info", f"SKILL.md line count OK: {line_count}.")

    for rel in sorted(referenced_paths(text)):
        candidate = skill_dir / rel
        if not candidate.exists():
            add(result, "errors", f"Referenced file is missing: {rel}")

    evals = skill_dir / "evals" / "evals.json"
    if evals.exists():
        try:
            data = json.loads(evals.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            add(result, "errors", f"evals/evals.json is invalid JSON: {exc}")
        else:
            cases = data.get("evals")
            if not isinstance(cases, list):
                add(result, "errors", "evals/evals.json must contain an `evals` list.")
            else:
                add(result, "info", f"Eval case count: {len(cases)}.")
                if len(cases) < 10:
                    add(result, "warnings", "Fewer than 10 eval cases.")
                negative_count = sum(1 for case in cases if case.get("should_trigger") is False)
                add(result, "info", f"Negative eval count: {negative_count}.")
                if negative_count < min_negative_evals:
                    add(result, "warnings", f"Only {negative_count} should-not-trigger evals; target is >= {min_negative_evals}.")
                for idx, case in enumerate(cases):
                    for key in ("id", "prompt", "expected_output", "assertions", "should_trigger"):
                        if key not in case:
                            add(result, "errors", f"Eval case {idx} missing `{key}`.")
                    if require_baselines and "baseline_without_skill" not in case:
                        add(result, "errors", f"Eval case {case.get('id', idx)} missing `baseline_without_skill`.")
                    if not isinstance(case.get("assertions", []), list):
                        add(result, "errors", f"Eval case {case.get('id', idx)} assertions must be a list.")
    else:
        add(result, "warnings", "No evals/evals.json found.")

    eval_runner = skill_dir / "scripts" / "run_eval_harness.py"
    if evals.exists() and eval_runner.exists():
        add(result, "info", "Eval harness found: scripts/run_eval_harness.py.")
    elif evals.exists() and require_eval_runner:
        add(result, "errors", "Eval harness required but missing: scripts/run_eval_harness.py.")

    scorecard_template = skill_dir / "assets" / "scorecard-template.json"
    if scorecard_template.exists():
        try:
            scorecard = json.loads(scorecard_template.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            add(result, "errors", f"assets/scorecard-template.json is invalid JSON: {exc}")
        else:
            dimensions = scorecard.get("dimensions")
            if not isinstance(dimensions, list) or len(dimensions) < 5:
                add(result, "errors", "assets/scorecard-template.json must contain at least 5 scoring dimensions.")
            for dim in dimensions or []:
                if not all(key in dim for key in ("name", "weight", "description")):
                    add(result, "errors", "Each scorecard dimension must include name, weight, and description.")
            if require_100_gate and "blockers" not in scorecard:
                add(result, "errors", "assets/scorecard-template.json must include `blockers` for the 100/100 gate.")

    if require_100_gate:
        required_100_files = [
            "references/world-class-100-gate.md",
            "references/benchmarking-and-scorecards.md",
            "assets/scorecard-template.json",
            "scripts/run_eval_harness.py",
        ]
        for rel in required_100_files:
            if not (skill_dir / rel).exists():
                add(result, "errors", f"100/100 gate file is missing: {rel}")
        if "100/100" not in text:
            add(result, "errors", "SKILL.md must describe the 100/100 target standard when --require-100-gate is used.")

    export_script = skill_dir / "scripts" / "build_all_in_one.py"
    if export_script.exists():
        add(result, "info", "Canonical export script found: scripts/build_all_in_one.py.")
    elif require_export_script:
        add(result, "errors", "Canonical export script required but missing: scripts/build_all_in_one.py.")

    for optional_dir in ("references", "scripts", "assets", "evals"):
        path = skill_dir / optional_dir
        if path.exists() and not path.is_dir():
            add(result, "errors", f"{optional_dir}/ exists but is not a directory.")

    return result


def validate_zip(zip_path, skill_name, result):
    if not zip_path.exists():
        add(result, "errors", f"ZIP does not exist: {zip_path}")
        return
    try:
        with zipfile.ZipFile(zip_path) as archive:
            names = archive.namelist()
    except zipfile.BadZipFile:
        add(result, "errors", f"Invalid ZIP file: {zip_path}")
        return

    prefix = f"{skill_name}/"
    if not any(name == prefix or name.startswith(prefix) for name in names):
        add(result, "errors", f"ZIP must contain {prefix} at the root.")
    if f"{skill_name}/SKILL.md" not in names:
        add(result, "errors", f"ZIP missing {skill_name}/SKILL.md.")
    add(result, "info", f"ZIP entry count: {len(names)}.")


def main():
    parser = argparse.ArgumentParser(description="Validate an Agent Skill package.")
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument("--zip", dest="zip_path", type=Path)
    parser.add_argument("--max-description", type=int, default=200)
    parser.add_argument("--max-lines", type=int, default=500)
    parser.add_argument("--warn-lines", type=int, default=400)
    parser.add_argument("--min-negative-evals", type=int, default=8)
    parser.add_argument("--require-baselines", action="store_true")
    parser.add_argument("--require-eval-runner", action="store_true")
    parser.add_argument("--require-100-gate", action="store_true")
    parser.add_argument("--require-export-script", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    require_baselines = args.require_baselines or args.strict
    result = validate_skill(
        args.skill_dir, args.max_description, args.max_lines, args.warn_lines,
        args.min_negative_evals, require_baselines, args.require_eval_runner,
        args.require_100_gate, args.require_export_script,
    )
    skill_name = args.skill_dir.name
    if args.zip_path:
        validate_zip(args.zip_path, skill_name, result)

    ok = not result["errors"] and not (args.strict and result["warnings"])
    if args.json:
        print(json.dumps({"ok": ok, **result}, indent=2))
    else:
        print("OK" if ok else "FAILED")
        for level in ("errors", "warnings", "info"):
            if result[level]:
                print(f"\n{level.upper()}:")
                for message in result[level]:
                    print(f"- {message}")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
