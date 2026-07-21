# Trigger Best Practices

Use this reference when writing or reviewing a skill `description`, trigger boundary, or should-not-trigger evals.

## Description Formula

Good descriptions answer three questions:

```markdown
What does the skill do?
When should Claude use it?
What nearby tasks should not trigger it?
```

Strong pattern:

```markdown
description: Turn [specific input] into [specific output]. Use when [trigger contexts]. Do not use for [near misses].
```

Keep descriptions concise, specific, and action-oriented. The description is activation metadata, not marketing copy.

## Good Examples

```markdown
description: Review landing page copy for offer clarity, objections, proof, CTA strength, and conversion risks. Use for landing page or sales page critiques.
```

```markdown
description: Turn vague or messy ideas into Claude Agent Skills or build prompts. Use for skill design, validation, packaging, evals, or trigger tuning; not ordinary writing tasks.
```

## Weak Examples

```markdown
description: Helps with marketing.
```

Too broad. No workflow, no trigger boundary.

```markdown
description: Uses best practices to make things better.
```

Generic. Does not say what artifact is produced.

```markdown
description: Writes prompts.
```

Too broad. Would trigger on ordinary prompt-writing tasks that are not skill architecture.

## Near-Miss Boundaries

Add should-not-trigger tests for tasks that share vocabulary but are not the workflow:

- Ordinary email writing.
- Summarization.
- One-off prompt writing.
- General coding tasks.
- Basic factual questions.
- Generic research requests.
- App/page creation where the user did not ask for a reusable skill.
- Casual "should I" questions without a real skill-design decision.

## Tuning Rules

- If the skill fails to trigger, add category language, not exact test phrases.
- If the skill over-triggers, add sharper boundaries and more negative evals.
- Avoid stuffing the description with every synonym.
- Prefer one clear workflow over several adjacent workflows.
- Do not use "world-class", "best", or "elite" as trigger anchors; convert those into quality gates inside the skill.
