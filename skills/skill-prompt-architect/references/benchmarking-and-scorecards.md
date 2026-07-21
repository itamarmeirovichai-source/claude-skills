# Benchmarking And Scorecards

Use this reference when the user asks whether a skill is production-ready, world-class, better than a generic prompt, or worth publishing.

## Honest Quality Levels

- **70-84**: good draft or strong v1. Structure is useful, but real performance is not proven.
- **85-89**: production-capable. Validator passes and realistic examples/evals exist, but evidence is still limited.
- **90-94**: reference-grade. The skill has captured before/after artifacts, scorecards, held-out evals, and repeatable wins over a strong baseline.
- **95+**: field-proven. Multiple real users/tasks, regression history, failure-driven revisions, and stable performance across domains.

Do not award 90+ from package hygiene alone. A validator proves shape. A benchmark proves behavioral lift.

## What Success Means

Measure more than "the answer looks good":

1. Artifact quality: did the final prompt/package become materially better?
2. Trigger correctness: did the skill activate only when useful?
3. User time saved: did the workflow reduce clarification, rework, or manual checking?
4. Failure recovery: did it catch unsafe, broad, vague, or tool-impossible requests?
5. Transfer: does it work across domains, not only the examples used to write it?
6. Downstream effect: do skills created by this skill perform better than skills made without it?
7. Context cost: did the process avoid needless ceremony for simple jobs?

## Benchmark Harness

Use:

```bash
python3 scripts/run_eval_harness.py init <skill-dir>
```

The harness creates:

```text
eval-runs/<timestamp>-<skill-name>/
|-- metadata.json
`-- cases/
    `-- <case-id>/
        |-- baseline_prompt.md
        |-- with_skill_prompt.md
        |-- baseline_output.md
        |-- with_skill_output.md
        `-- scorecard.json
```

Run each `baseline_prompt.md` without the skill, run each `with_skill_prompt.md` with the skill enabled, paste outputs into the output files, fill the scorecards, then run:

```bash
python3 scripts/run_eval_harness.py score eval-runs/<timestamp>-<skill-name>
```

## Release Gate

For a serious release:

- Average with-skill score >= 85.
- Average with-skill delta over baseline >= 10.
- No with-skill critical failures.
- Should-not-trigger cases do not force the full workflow.
- At least one held-out messy prompt is not used while editing the skill.

For a 90+ claim, include at least 10 scored cases across trigger, near-miss, unsafe, broad, tool/API, and domain-specific requests.

For a 100/100 claim, read `references/world-class-100-gate.md` and use the `--target-100` scoring gate.

## 3-Condition Evaluation

The gold standard for proving a skill adds value is the 3-condition test, adapted from SkillsBench methodology:

| Condition | Description |
| --- | --- |
| **No skill** | Run the eval prompt with no skill active. Baseline output. |
| **Curated skill** | Run with the hand-crafted skill package enabled. |
| **Self-generated skill** | Claude generates its own skill from the task description, then re-runs. |

A skill is genuinely strong when `curated ≥ self-generated > no skill` across the eval cases. If `self-generated ≥ curated`, the skill is under-specified and needs more domain-specific content — Claude is essentially recreating it from first principles each time.

To run:

```bash
python3 scripts/run_eval_harness.py init <skill-dir> --conditions 3
```

This creates a `self_generated_prompt.md` per case so you can capture all three conditions.

## Trajectory Metrics vs Outcome Metrics

Scorecards must track both:

**Outcome metrics** (did the final artifact succeed?):
- Artifact quality score
- Trigger correctness
- Safety boundary
- Evidence completeness

**Trajectory metrics** (did the process stay clean?):
- Number of clarification loops before first useful output
- Steps taken vs steps required (efficiency ratio)
- Unnecessary ceremony: unsolicited sections, redundant questions, context waste
- Reflection rate: did the skill self-check after each major action?

A skill that scores well on outcomes but has poor trajectory metrics is expensive in practice — it wastes context and user time even when it produces the right answer. Production-ready skills must optimize both.

Add to each scorecard:

```json
{
  "trajectory": {
    "clarification_loops": 0,
    "steps_taken": 5,
    "steps_required": 4,
    "efficiency_ratio": 0.80,
    "unsolicited_sections": 0,
    "reflection_checks": 3
  }
}
```

## Scoring Dimensions

Use 0-5 for each dimension:

| Dimension | Weight | Meaning |
| --- | ---: | --- |
| trigger_correctness | 20 | Correct trigger/non-trigger behavior. |
| artifact_quality | 20 | Completeness and usefulness of the produced artifact. |
| domain_specificity | 15 | Concrete domain constraints instead of generic advice. |
| validation_quality | 15 | Realistic checks, evals, or deterministic validation. |
| safety_boundary | 10 | Unsafe/private/tool-sensitive behavior handled correctly. |
| delivery_completeness | 10 | Install, package, or handoff details when relevant. |
| concision_cost | 10 | Avoids unnecessary ceremony and context cost. |

Mark `critical_failure: true` if the output is unsafe, invents private policy, ignores a required tool boundary, or builds the wrong artifact. Critical failures cap that side's score at 69.
