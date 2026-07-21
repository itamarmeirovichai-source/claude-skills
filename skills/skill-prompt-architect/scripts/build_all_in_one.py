#!/usr/bin/env python3
"""Build the canonical all-in-one dossier for skill-prompt-architect."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


FILE_ORDER = [
    "SKILL.md",
    "references/council-quick-protocol.md",
    "references/llm-council-method.md",
    "references/intake-framework.md",
    "references/decision-framework.md",
    "references/research-enrichment.md",
    "references/action-execution.md",
    "references/trigger-best-practices.md",
    "references/skill-authoring-rubric.md",
    "references/evaluation-playbook.md",
    "references/benchmarking-and-scorecards.md",
    "references/world-class-100-gate.md",
    "references/github-delivery.md",
    "references/worked-examples.md",
    "references/gold-standard-examples.md",
    "references/lifecycle-feedback.md",
    "assets/claude-build-prompt-template.md",
    "assets/eval-template.json",
    "assets/scorecard-template.json",
    "scripts/validate_skill_package.py",
    "scripts/run_eval_harness.py",
    "scripts/build_all_in_one.py",
    "evals/evals.json",
]

DEFAULT_OUTPUTS = [
    "docs/skill-prompt-architect-complete-build-dossier.en.md",
]


def language_for(path):
    suffix = Path(path).suffix.lower()
    if suffix == ".json":
        return "json"
    if suffix == ".py":
        return "python"
    return "markdown"


def read_required(skill_dir, rel):
    path = skill_dir / rel
    if not path.exists():
        raise SystemExit(f"Missing source file: {path}")
    return path.read_text(encoding="utf-8").rstrip() + "\n"


def build_document(skill_dir):
    parts = ["# skill-prompt-architect — All-In-One Dossier\n\n"]
    for rel in FILE_ORDER:
        parts.append(f"## FILE: skill-prompt-architect/{rel}\n\n```{language_for(rel)}\n")
        parts.append(read_required(skill_dir, rel))
        parts.append(f"```\n\n")
    return "".join(parts)


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_output(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    digest = sha256_text(text)
    path.with_suffix(path.suffix + ".sha256").write_text(f"{digest}  {path.as_posix()}\n", encoding="utf-8")
    return digest


def main():
    parser = argparse.ArgumentParser(description="Build canonical all-in-one skill dossier.")
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path("."))
    parser.add_argument("--out", action="append", default=[])
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    skill_dir = args.skill_dir.resolve()
    project_root = args.project_root.resolve()
    outputs = [Path(item) for item in args.out] if args.out else [project_root / item for item in DEFAULT_OUTPUTS]
    text = build_document(skill_dir)
    digest = sha256_text(text)

    changed = []
    written = []
    for output in outputs:
        output = output if output.is_absolute() else project_root / output
        current = output.read_text(encoding="utf-8") if output.exists() else None
        if current != text:
            changed.append(str(output))
        if not args.check:
            write_output(output, text)
            written.append(str(output))

    result = {
        "ok": not changed if args.check else True,
        "sha256": digest,
        "outputs": [str(p) for p in outputs],
        "changed": changed,
        "written": written,
        "file_count": len(FILE_ORDER),
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("OK" if result["ok"] else "FAILED")
        print(f"sha256: {digest}")
        if args.check and changed:
            for path in changed:
                print(f"would change: {path}", file=sys.stderr)

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
