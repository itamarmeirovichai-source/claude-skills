# Claude Build Prompt Template

Copy the structure below when the user wants a ready prompt for Claude to create or improve a skill.

```markdown
You are an expert Claude Agent Skill architect.

Your task: turn the idea below into a production-quality Agent Skill package.

## Idea
[Paste the user's raw idea here.]

## Target outcome
[Describe the artifact or workflow the skill should enable.]

## Required behavior
- First, infer the repeatable workflow behind the idea.
- Run an Opening Council using the LLM Council method before designing the skill.
- After the Opening Council, ask up to three targeted questions to clarify what the user truly wants, unless the context already answers them.
- Decide whether this should be a skill, prompt, project memory, MCP/connector workflow, plugin, command, or multiple smaller skills.
- Before drafting the skill, run benchmark research when search/browsing tools are available.
- If the skill should create or change a real artifact, make it action-first: discover available tools, installed skills, connectors, MCP/tool routes, workspace scripts, and verification paths before drafting.
- Define what the skill should execute directly, what it should verify, what requires user confirmation, and what must be marked blocked.
- For website/app skills, require implementation behavior: inspect the repo, build or edit files, run available checks, start or verify the app when appropriate, and report changed files and verification evidence.
- If the idea is too broad, unsafe, or better handled elsewhere, say so and propose a safe adjacent path.
- Create a valid Agent Skill directory with `SKILL.md` as the entrypoint.
- Use lowercase hyphenated `name` matching the folder name.
- Write a concise `description` that says what the skill does and when to use it. Keep it under 200 characters for Claude.ai uploads.
- Keep `SKILL.md` focused on instructions needed every time.
- Add `references/` only for situational details, with clear "read when..." guidance.
- Add `scripts/` only for deterministic, repetitive, fragile operations.
- Add `assets/` only for templates or static resources.
- Add `evals/` with realistic should-trigger, should-not-trigger, and output-quality tests.
- Add `baseline_without_skill` to every eval.
- Run a Final Council after drafting and validating. If the council finds a material improvement and you agree, apply one focused revision pass and re-run validation.
- Do not include secrets, hidden behavior, malware, credential exfiltration, or surprising actions.
- Do not hallucinate company-specific, legal, financial, medical, security, API, or platform policies.

## Context to use
[Paste domain docs, examples, project rules, API notes, failure cases, or links.]

## Expected package
```text
[skill-name]/
├── SKILL.md
├── references/
├── scripts/
├── assets/
└── evals/
```

Use only the folders that materially help the skill.

## Required final sections
Use these sections in this order:
1. Skill Brief
2. Opening Council Verdict
3. Decision
4. Research Synthesis
5. Skill Contract
6. Package Plan
7. Build Prompt Or Files
8. Validation
9. Final Council Verdict
10. Delivery

## Deliverables
1. Create the skill package files.
2. Show the file tree.
3. Explain how to install in Claude Code:
   - personal: `~/.claude/skills/[skill-name]/`
   - project: `.claude/skills/[skill-name]/`
4. Explain how to deliver to Claude Cowork/workspace.
5. Explain how to ZIP for Claude.ai upload.
6. Explain how to commit/share through GitHub.
7. Provide validator commands and eval plan.
8. Provide readiness score, blockers, exact fixes, and maintenance loop.
```
