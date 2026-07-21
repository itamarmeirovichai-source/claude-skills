# Council Quick Protocol

Use this lightweight protocol before loading the full `llm-council-method.md`. Load the full method when the decision is high-stakes, ambiguous, contentious, or when the user explicitly asks for the full council.

## Opening Council

Frame the user's idea as:

```markdown
What skill, if any, should be built from this idea? Should it be built, split, rejected, researched further, or handled as a prompt/project memory/MCP workflow instead?
```

Analyze from five lenses:

- Contrarian: What will fail, over-trigger, or become unsafe?
- First Principles: What problem are we actually solving?
- Expansionist: What larger opportunity or stronger version is available?
- Outsider: What is confusing to a non-expert or unsupported by the context?
- Executor: What is the fastest practical build path?

Synthesize:

```markdown
Opening Council Verdict:
- Best direction:
- What not to do:
- Research needed:
- Questions to ask next:
- First build move:
```

Ask up to three questions from `Questions to ask next`, then continue.

## Final Council

Review the draft skill package from five lenses:

- Contrarian: trigger false positives, missing safety, weak evals, brittle assumptions.
- First Principles: whether this is truly the right mechanism.
- Expansionist: high-upside improvements that do not bloat the core.
- Outsider: clarity for non-experts.
- Executor: exact changes needed before release.

Synthesize:

```markdown
Final Council Verdict:
- Keep:
- Change:
- Do not change:
- Release blockers:
- One focused revision:
```

Apply only one focused revision if the reasoning is material, then re-run validation.
