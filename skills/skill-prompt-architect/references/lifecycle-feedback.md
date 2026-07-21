# Lifecycle And Feedback

Use this reference when a skill will be reused, shared, versioned, published, or improved after real use.

## Maintenance Loop

A serious skill should improve from real failures:

1. Save the generated package or final output.
2. Record whether the skill triggered correctly.
3. Record user corrections.
4. Record validation failures.
5. Turn repeated failures into new examples, evals, gotchas, or scripts.
6. Re-run regression tests before publishing updates.
7. Keep benchmark summaries so quality claims are based on measured deltas, not memory.

## Release Checklist

Before marking a version production-ready:

- Run the validator in strict mode.
- Run prior should-trigger and should-not-trigger evals.
- Run or update the benchmark harness for serious releases.
- Add at least one eval for any repeated real failure.
- Check whether official platform docs changed.
- Confirm no company-specific, legal, financial, medical, security, API, or platform claims were invented without sources.
- Record the version, validation command, and known limitations.

## Suggested Tracking Files

Keep these outside the skill package unless the user asks to include them:

```text
skill-workspace/
|-- benchmark-history.json
|-- benchmark-scorecards/
|-- CHANGELOG.md
|-- feedback-log.md
|-- failed-runs/
|-- eval-runs/
|-- generated-packages/
`-- skill-snapshots/
```

Do not clutter the final skill package with process logs.

## Versioning

Use semantic-ish versions:

- Patch: wording fixes, typo fixes, small examples.
- Minor: new references, evals, templates, validator checks.
- Major: changed output contract, trigger scope, safety posture, or package architecture.

For each release, record:

```markdown
## Version
Date:
Changed:
Why:
Validation run:
Known limitations:
```

## Regression Tests

Keep a fixed set of tests:

- Should-trigger prompts.
- Should-not-trigger near misses.
- Unsafe requests.
- Overbroad ideas that must split.
- Tool/API requests that must route to MCP/connector guidance.
- Existing bad skill rewrites.
- GitHub packaging requests.

A release is not ready if it improves one scenario but breaks a previous one.

## Stale Reference Check

For platform-dependent guidance, periodically verify:

- Claude Skills docs.
- Agent Skills specification.
- Claude Code skills docs.
- Claude Code on the web docs.
- Claude Code GitHub Actions docs.

If these change, update `references/github-delivery.md`, evals, and the one-shot prompt.
