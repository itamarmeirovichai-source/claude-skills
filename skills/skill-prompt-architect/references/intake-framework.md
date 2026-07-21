# Intake Framework

Use this reference when the user gives an idea that is broad, vague, complex, or emotionally described rather than operationally specified.

## Fast Intake

Ask only what is necessary. If the conversation already contains the answer, infer it and state the assumption.

If the user is vague or non-technical, ask at most three questions, then produce a draft anyway:

```markdown
1. What should the skill help Claude do repeatedly?
2. What should the final output look like?
3. What should Claude never do in this workflow?
```

Use plain language. Define terms like "skill", "eval", "trigger", and "reference file" the first time they matter.

## Deep Intake For Difficult Ideas

Use this when the user says the idea is hard, strategic, high-stakes, or "world class."

```markdown
## Outcome
- What business, creative, technical, or personal outcome does the skill create?
- What decision or artifact should exist at the end?
- What does "excellent" mean here?

## Workflow
- What are the repeated steps a human expert would take?
- Which steps are fragile, boring, or easy to get wrong?
- Which decisions need judgment?

## Context
- What domain facts, company rules, project conventions, or examples does Claude not know?
- Which of those facts must be always loaded?
- Which can stay in references and be loaded only when needed?

## Inputs and outputs
- What file types, links, text snippets, screenshots, data, or code may appear?
- What exact output formats are expected?
- Should the skill create files, edit files, answer in chat, run tools, or all of these?

## Boundaries
- When should the skill trigger?
- What near-miss tasks should not trigger it?
- Which adjacent workflows should become separate skills?

## Risk
- Could the skill expose secrets, delete data, make purchases, publish content, or change production systems?
- Does it need dry-run behavior or explicit user confirmation?

## Validation
- How can we test whether the skill improved the outcome?
- What realistic prompts should pass?
- What near-miss prompts should not activate the skill?
```

## Turning Answers Into A Skill Contract

After intake, summarize the result:

```markdown
Skill name:
One-sentence purpose:
Trigger description:
Core workflow:
Inputs:
Outputs:
Always-loaded guidance:
Reference files:
Scripts:
Assets:
Safety rules:
Eval prompts:
GitHub/share plan:
```

Ask for confirmation only when a wrong assumption would change the package shape, tool permissions, safety posture, or output format.

## Mini Glossary

- Skill: A reusable folder of instructions and optional resources that Claude loads for a specific workflow.
- Trigger: The kind of user request that should make Claude use the skill.
- Eval: A test prompt used to check whether the skill activates and improves output.
- Reference file: Extra documentation loaded only when needed.
- Script: Deterministic code the agent can run instead of improvising a fragile task.
- MCP/connector: A tool integration for live access to external services.
