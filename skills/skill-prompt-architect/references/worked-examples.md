# Worked Examples

Use these examples to calibrate quality. They show the difference between a vague idea and a usable skill contract.

## Example 1: Chaotic Founder Notes To Launch Plan

Raw idea:

```markdown
I have messy notes from founders and I want Claude to make launch plans from them.
```

Intake assumptions:

- The workflow repeats for multiple founder calls.
- Inputs are raw notes, transcripts, or bullet dumps.
- Output should be an actionable launch plan, not generic strategy.
- The user may not know what information is missing.

Skill contract:

```markdown
Working name: founder-launch-planner
User outcome: Turn chaotic founder notes into a launch-ready plan.
Repeatable workflow:
1. Extract product, audience, offer, constraints, assets, deadlines, and risks.
2. Flag missing launch-critical information.
3. Convert notes into positioning, launch sequence, asset checklist, and first-week actions.
4. Separate facts from assumptions.
Inputs: call notes, transcript, product notes, audience notes.
Outputs: launch brief, launch timeline, asset checklist, risk list, first next step.
Trigger contexts: founder notes, product launch, messy launch plan, launch checklist.
Non-trigger contexts: general business brainstorming or writing a single ad.
Gotchas: Do not invent numbers; mark unknowns.
Safety: Do not claim legal, financial, or compliance certainty.
Validation: evals include messy notes, missing data, conflicting constraints, and near-miss ad copy requests.
```

Package plan:

```text
founder-launch-planner/
|-- SKILL.md
|-- references/
|   |-- launch-plan-template.md
|   `-- missing-info-checklist.md
`-- evals/
    `-- evals.json
```

Why this is good:

- It defines exact inputs and outputs.
- It has missing-information behavior.
- It avoids over-expanding into all marketing tasks.

## Example 2: Bad Skill Rewrite

Weak `SKILL.md`:

```markdown
---
name: marketing-helper
description: Helps with marketing.
---

Use best practices to make marketing better.
```

Problems:

- Description is too broad to trigger precisely.
- No repeatable workflow.
- No output contract.
- No boundaries.
- "Best practices" is generic.

Improved direction:

```markdown
---
name: landing-page-critic
description: Critique landing page copy for offer clarity, buyer objections, proof, CTA strength, and conversion risks. Use when reviewing landing pages or sales pages.
---

# Landing Page Critic

Review landing pages in this order:
1. Identify the offer, audience, promise, proof, CTA, and risk reversal.
2. Flag missing or vague elements.
3. Diagnose the top 3 conversion blockers.
4. Rewrite only the weakest section unless the user asks for a full rewrite.
5. End with one highest-leverage edit.

Use this output:
## Diagnosis
## Top Conversion Blockers
## Suggested Rewrite
## One Edit To Make First
```

Why this is better:

- It is one coherent workflow.
- It has clear trigger language.
- It defines output and first action.
- It can be tested with real landing pages.

## Example 3: Tool/API Skill Decision

Raw idea:

```markdown
Make a skill that checks my Stripe account, finds failed payments, emails users, and updates my CRM.
```

Decision:

This should not be only a skill. It needs external account access and state-changing actions. Use MCP/connectors/API automation for access, and a skill only for the operational procedure and safety gates.

Safe skill contract:

```markdown
Working name: failed-payment-recovery-runbook
User outcome: Guide Claude through failed-payment recovery using approved tools.
Repeatable workflow:
1. Confirm available Stripe, email, and CRM tools.
2. Run read-only checks first.
3. Summarize affected accounts.
4. Draft email actions for user approval.
5. Update CRM only after explicit confirmation.
Inputs: tool outputs, customer IDs, payment status.
Outputs: recovery summary, drafted messages, approved action log.
Safety: no emails or CRM writes without explicit confirmation.
```

Why this is good:

- It does not pretend a skill alone can access accounts.
- It separates procedure from integration.
- It adds confirmation for external actions.

## Example 4: Prompt-Only Request

Raw idea:

```markdown
Write me a prompt that makes Claude brainstorm names for my app.
```

Decision:

Do not create a skill. This is a one-time prompt unless the user repeatedly runs a naming workflow with brand rules, scoring criteria, audience data, and output format.

Output:

```markdown
This should be a prompt, not a skill, because it is a one-time creative task. If you want a reusable naming workflow, I can turn it into a skill with brand criteria, scoring, name filters, and evals.
```
