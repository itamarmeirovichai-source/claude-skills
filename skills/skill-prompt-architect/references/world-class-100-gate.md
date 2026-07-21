# World-Class 100 Gate

Use this reference whenever the user asks for 100/100 quality, "best in the world", "perfect", "world-class", or asks that every generated skill score 100/100.

## Core Rule

Every generated skill must be designed to target 100/100. Do not claim it is verified 100/100 unless the evidence supports that exact score.

This is the difference:

- **100/100 target-ready**: the package is designed with the full 100-point protocol, but benchmark runs are not complete.
- **Verified 100/100**: every scored benchmark case receives 100, no critical failures exist, no required source material is missing, and no blocker remains open.

## Evidence Caps

Use these caps when assigning a final score:

| Evidence available | Maximum honest score |
| --- | ---: |
| Strong written prompt only | 74 |
| Valid skill package with examples/evals | 84 |
| Strict validator passes with negative evals and baselines | 89 |
| Benchmark harness exists but outputs are not captured | 89 |
| Captured before/after outputs and scorecards beat baseline | 94 |
| 10+ scored benchmark cases average 95+ with no critical failures | 97 |
| All scored benchmark cases are 100, held-out cases pass, no blockers remain | 100 |

Never bypass the cap because the writing feels impressive.

## 100/100 Skill Checklist

A 100/100 skill must satisfy all of these:

1. **Scope**: one coherent repeatable workflow, no grab bag.
2. **Trigger**: description clearly states what/when/not-use and has near-miss tests.
3. **Procedure**: stepwise, adaptive, and concise.
4. **Domain specificity**: includes non-obvious constraints, examples, policies, schemas, or failure modes.
5. **Progressive disclosure**: `SKILL.md` stays lean; references are routed with "read when" guidance.
6. **Resources**: scripts/assets are included only when they improve reliability.
7. **Examples**: includes gold-standard before/after examples when output quality matters.
8. **Validation**: includes should-trigger, should-not-trigger, unsafe, messy, and held-out cases.
9. **Benchmark**: captures baseline and with-skill outputs with scorecards.
10. **Safety**: rejects hidden, unsafe, unauthorized, or unsourced behavior.
11. **Delivery**: install, ZIP, GitHub, and maintenance steps are clear.
12. **Maintenance**: has regression, stale-doc, and failed-run feedback loops.

If any item is missing, report the score honestly and list exact fixes.

## Perfect-Score Benchmark Gate

Run:

```bash
python3 scripts/run_eval_harness.py init <skill-dir> --min-score 100 --min-delta 10
```

After outputs are captured and scorecards are filled, run:

```bash
python3 scripts/run_eval_harness.py score eval-runs/<timestamp>-<skill-name> --target-100 --json
```

The perfect-score gate passes only when:

- every with-skill case score is exactly 100;
- average with-skill score is 100;
- no with-skill critical failures exist;
- average delta over baseline meets the configured threshold;
- baseline and with-skill outputs are present;
- every scorecard is complete;
- no blocker is listed in `metadata.json` or the scorecards.

## Required Final Language

When evidence is incomplete, say:

```markdown
Score: __ / 100
Status: 100/100 target-ready, not verified 100/100 yet.
Why not verified:
- ...
Exact path to 100:
- ...
```

When evidence passes:

```markdown
Score: 100 / 100
Status: Verified 100/100.
Evidence:
- Benchmark run:
- Cases:
- Average baseline:
- Average with-skill:
- Average delta:
- Critical failures: none
```

## What Not To Do

- Do not guarantee that every future skill will be perfect.
- Do not inflate a score because the user asked for 100.
- Do not treat validator success as behavioral proof.
- Do not hide missing source material, unrun benchmarks, or platform limitations.
- Do not create extra files only to look comprehensive.

The highest-quality answer is honest about what is proven and ruthless about closing the gap.
