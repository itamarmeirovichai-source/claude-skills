# Decision Framework

Use this reference when deciding whether a user idea should become a skill, a prompt, project memory, MCP connector, plugin, command, or several smaller skills.

## First Decision

```markdown
Is this a repeatable workflow?
- Yes: continue.
- No: make a one-time prompt or answer instead.

Does Claude need specialized procedure, local conventions, examples, or resources to do this well?
- Yes: skill may fit.
- No: prompt or project instruction may be enough.

Does the task require live external access or actions in another service?
- Yes: use MCP/connector/plugin guidance, then optionally create a skill for the procedure around that tool.
- No: skill can be self-contained.
```

## Choose The Right Mechanism

| User need | Best mechanism | Why |
| --- | --- | --- |
| One-time output | Prompt | No reusable workflow. |
| Broad always-on preference | Custom instruction or project memory | Skills should load on demand, not constantly. |
| Static project facts | `CLAUDE.md` or project knowledge | Facts are needed across many tasks. |
| Repeatable procedure | Skill | The agent needs a workflow it can invoke. |
| External service access | MCP/connector/plugin | Skills should not fake access to APIs or accounts. |
| Repo-specific automation | Project skill under `.claude/skills/` | Keeps workflow versioned with the repo. |
| Fragile deterministic transform | Skill plus `scripts/` | Scripts reduce repeated model improvisation. |

## Split Rules

Split one idea into multiple skills when:

- It has two or more distinct trigger contexts.
- Different users would invoke different parts independently.
- The skill needs unrelated tools or file types.
- `SKILL.md` would become a long menu of workflows.
- Safety posture differs between parts.

Example:

```markdown
Bad: "marketing-automation" handles ad prompts, landing pages, analytics, email campaigns, and CRM sync.
Better:
- meta-ad-prompt-writer
- landing-page-critic
- campaign-analytics-summarizer
- crm-sync-runbook
```

## Reject Or Redesign

Reject or redesign a requested skill when it:

- Hides behavior from the user.
- Attempts credential theft, secret discovery, unauthorized access, surveillance, or data exfiltration.
- Automates destructive actions without explicit confirmation and recovery path.
- Claims to use tools or integrations that do not exist.
- Depends on current facts but refuses verification.
- Is so broad that no trigger description can be precise.

When rejecting, offer a safe adjacent skill design.

## Skill vs Tool: The One-Call Rule

A workflow that requires exactly one tool call with no follow-up check is a **tool use**, not a skill.
A workflow that requires more than one tool call **plus** at least one verification step is a **skill candidate**.

Use this test before deciding:

```markdown
Does the workflow involve:
1. More than one distinct tool call?         → Yes: continue
2. At least one check/verify step?           → Yes: skill candidate
3. A repeatable trigger context?             → Yes: build the skill
Any "No"? → Prompt or direct tool use instead
```

Examples:

| Request | Verdict | Reason |
| --- | --- | --- |
| "Search the web for X" | Tool | One call, no check |
| "Research X, compare 3 sources, summarize" | Skill | Multiple calls + synthesis |
| "Create a GitHub PR" | Tool (via MCP) | One API call |
| "Review branch, run checks, create PR if clean" | Skill | Multiple steps + conditional |
| "Convert this file to PDF" | Tool | One call |
| "Build site, lint, screenshot, report issues" | Skill | Full execution loop |

The boundary matters because skills carry overhead (context load, trigger cost). Only package a workflow as a skill when the multi-step procedure provides consistent lift over ad-hoc tool use.

## Script-Mandatory Signals

Add a script when:

- A check must be deterministic.
- The same helper code would be rewritten in many runs.
- Output must be machine-readable.
- The task validates files, schemas, links, archives, or package structure.
- The workflow has clear pass/fail conditions.

For skill packages, include or recommend a validator script that checks frontmatter, folder shape, references, JSON, length limits, and ZIP layout.
