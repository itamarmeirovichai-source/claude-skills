# Evaluation Playbook

Use this reference when creating test prompts, checking trigger quality, or improving a skill after trial runs.

## Acceptance Harness

For serious use, do not rely on Claude's self-assessment. Use this harness:

1. Run the same hidden or held-out messy prompts without the skill.
2. Run them with the skill.
3. Save the produced artifacts.
4. Run deterministic validation where possible.
5. Score both outputs with the rubric.
6. Compare pass rate, correctness, specificity, and token/time cost.
7. Add failures to future evals.

Minimum acceptance:

```markdown
with_skill score >= 85
with_skill beats baseline on specificity, package correctness, and validation quality
no critical validator errors
no unsafe behavior
```

For release-grade comparisons, use `scripts/run_eval_harness.py` to create artifact folders, scorecards, and `summary.json`. Read `references/benchmarking-and-scorecards.md` for the scoring dimensions and 90+ gate.

## Trigger Evaluation

Create two sets:

```json
[
  {
    "query": "Turn this messy onboarding workflow into a reusable Claude skill",
    "should_trigger": true
  },
  {
    "query": "Write me a general motivational prompt",
    "should_trigger": false
  }
]
```

Good should-trigger prompts:
- Use casual language and typos.
- Mention real file paths, tools, or business context.
- Include direct and indirect phrasing.

Good should-not-trigger prompts:
- Are near misses, not obvious unrelated tasks.
- Share keywords but require a different workflow.

Run each query multiple times if the client supports it. Track the trigger rate and revise descriptions based on categories of failures, not by stuffing exact test phrases into the description.

## Output Quality Evaluation

For each test case, compare:

1. Output without the skill.
2. Output with the skill.
3. Output from the previous skill version, if improving an existing skill.

Use assertions that can be checked from the output:

```json
{
  "id": "complex-idea-to-skill",
  "prompt": "I have a complicated idea for a skill that helps founders turn chaotic product notes into launch plans.",
  "expected_output": "A structured skill contract, a proposed file layout, a Claude build prompt, and validation tests.",
  "assertions": [
    "Identifies trigger and non-trigger contexts",
    "Proposes SKILL.md plus references only where needed",
    "Includes at least three realistic eval prompts",
    "Includes safety or boundary considerations"
  ]
}
```

## Artifact Checks

When the skill creates or modifies a skill package, check:

- Directory name matches frontmatter `name`.
- `SKILL.md` exists and starts with frontmatter.
- Description says what the skill does and when to use it.
- Referenced files exist.
- `evals/evals.json` parses.
- `SKILL.md` is not overloaded.
- ZIP package has the skill directory at root.

Use `scripts/validate_skill_package.py <skill-dir>` when available.

## Iteration Loop

1. Draft the skill.
2. Run 3-5 realistic tasks with and without the skill.
3. Grade outputs with concrete assertions.
4. Read failures and transcripts if available.
5. Revise only the instructions that explain the failure.
6. Repeat until the skill improves quality enough to justify its token and time cost.

For serious releases, expand the loop to at least 10 scored cases before claiming reference-grade quality.

## What To Improve Based On Failure

| Failure | Likely cause | Edit |
| --- | --- | --- |
| Skill did not trigger | Description too narrow or missing task language | Broaden the category and add natural trigger concepts. |
| Skill triggered on wrong task | Description too broad | Add sharper boundary and near-miss tests. |
| Output format inconsistent | Missing template | Add a short output template in `SKILL.md` or `assets/`. |
| Claude reinvents helper code | Missing script | Add a reusable script and command usage. |
| Claude reads irrelevant docs | References poorly routed | Add "read this when..." guidance and split reference files. |
| Claude makes same mistake repeatedly | Missing gotcha | Add the concrete correction to `SKILL.md`. |
| Skill passes easy evals but fails real use | Eval set too shallow | Add held-out messy prompts, baseline comparison, and stricter assertions. |
| Quality drifts after edits | No regression loop | Keep benchmark history and rerun prior evals before release. |

## Evidence Ladder

Use this ladder when assigning a readiness score:

| Evidence | Maximum honest score |
| --- | ---: |
| Good instructions only | 74 |
| Good instructions plus examples/evals | 84 |
| Validator passes and near-miss evals exist | 89 |
| Captured before/after benchmark run beats baseline | 94 |
| Multiple real-world runs, regression history, and failure-driven revisions | 98 |

Do not let a clean validator push a score above the evidence level.
