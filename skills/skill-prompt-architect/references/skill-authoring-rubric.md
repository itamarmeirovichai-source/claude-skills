# Skill Authoring Rubric

Use this rubric before finalizing a new skill, reviewing an existing skill, or generating a Claude build prompt. The final answer must include the score, blockers, exact fixes, and pass/fail decision.

Score each category from 0 to full points. A strong production-ready skill should score at least 85.

## Rubric

| Category | Points | What excellent looks like |
| --- | ---: | --- |
| Focus and scope | 15 | Solves one coherent repeatable workflow; not a grab bag; clear boundaries. |
| Trigger description | 15 | Describes what the skill does and when to use it; includes likely user phrasing and near concepts; avoids overbroad activation. |
| Procedure and execution quality | 15 | Stepwise, actionable, adaptive, and execution-oriented when the user wants an artifact; uses procedures over generic advice. |
| Domain specificity | 10 | Captures facts, gotchas, constraints, examples, or conventions Claude would not reliably know. |
| Progressive disclosure | 15 | `SKILL.md` is lean; references are focused; file references say when to load each file. |
| Resources, tools, and scripts | 10 | Scripts/assets/tool routes are included only when they materially improve reliability; action skills discover available capabilities and script interfaces are non-interactive and clear. |
| Examples and output format | 10 | Includes concise examples or templates when format matters. |
| Validation | 10 | Includes realistic should-trigger, should-not-trigger, and output-quality tests. |
| Safety and trust | 10 | No secrets; no hidden behavior; dangerous operations require confirmation or dry run. |

## Readiness Gate

```markdown
Score: __ / 100
Decision: PASS / PASS WITH MINOR FIXES / FAIL
Blockers:
- ...
Exact fixes:
- ...
```

- 90-100: ready for serious use.
- 85-89: usable, but list minor fixes.
- 70-84: good draft, not production-ready.
- Below 70: redesign before use.

Do not award 90+ unless the skill has a clear output contract, examples or templates, eval coverage, safety boundaries, a validation path, and benchmark evidence or a concrete before/after benchmark plan.
Do not award 100/100 unless the skill passes the perfect-score benchmark gate in `references/world-class-100-gate.md`.

## High-Value Checks

Ask these questions line by line:

- Would Claude likely get this right without the instruction? If yes, cut it.
- Is this instruction always relevant when the skill triggers? If no, move it to a reference file.
- Is this a procedure or only a desired result?
- If the user wants an artifact, does the skill build/edit/run/verify instead of only planning?
- Does the skill discover available tools, connectors, MCP routes, scripts, and verification paths before acting?
- Does the description make the skill discoverable without triggering on unrelated tasks?
- Are the gotchas concrete and non-obvious?
- Are there examples of expected output where format matters?
- Are scripts documented by command, input, output, and failure behavior?
- Can the skill be validated with real prompts?
- Does anything in the skill surprise the user or exceed the stated purpose?
- Is there a split/reject decision when the idea is too broad or unsafe?
- Is there a maintenance path for learning from failed real runs?

## Common Problems And Fixes

| Problem | Fix |
| --- | --- |
| Description is too vague | Add what the skill does, when to use it, and 2-4 relevant trigger concepts. |
| Description triggers too often | Add precise workflow boundary and near-miss exclusions in tests. |
| `SKILL.md` is huge | Move situational details to `references/` and link with "read when..." instructions. |
| Skill is generic | Add real project artifacts, examples, schemas, failure cases, or reviewer corrections. |
| Too many options | Pick a default tool or method and mention alternatives only as escape hatches. |
| No validation | Add eval prompts, baseline comparison, and assertion-style success criteria. |
| Plans but does not act | Add an execution contract, capability discovery, concrete file/tool actions, verification commands, and confirmation boundaries. |
| Script may hang | Remove prompts; require flags/stdin; add `--help`; use clear errors. |
| Hidden risk | Add safety boundaries, dry-run mode, and explicit user confirmation. |
| No output contract | Require stable sections in a fixed order so outputs can be reviewed and tested. |
| No lifecycle | Add versioning, feedback capture, regression tests, and stale-doc checks. |

## Final Review Template

```markdown
## Review Result
Score: __ / 100

Strengths:
- ...

Blocking issues:
- ...

Recommended edits:
- ...

Validation plan:
- should-trigger:
- should-not-trigger:
- output-quality:
- baseline comparison:
- validator command:

Maintenance:
- versioning:
- feedback loop:
- regression tests:
```
