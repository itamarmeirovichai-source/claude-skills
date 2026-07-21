# Gold Standard Examples

Use these examples when a skill-design output feels generic, when the user asks for world-class quality, or when building benchmark cases. These are compact patterns, not full packages.

## Example 1: Tool Workflow Skill

Weak request:

```text
Make a skill that manages Stripe refunds.
```

Gold direction:

```markdown
Decision: Skill plus connector/API workflow, not a standalone magic account actor.
Trigger: refund triage, payment dispute handling, Stripe customer remediation.
Must not do: issue refunds, email customers, or update CRM without explicit confirmation.
Package shape:
- SKILL.md: read-only triage workflow, confirmation gate, output contract.
- references/stripe-refund-policy.md: user-provided company policy only.
- evals/evals.json: failed payment, disputed charge, partial refund, unsafe auto-refund.
- scripts/validate_refund_batch.py: deterministic CSV/schema validation if batches are used.
```

Why this is strong: it separates procedure from account access, prevents unauthorized writes, and asks for private policy instead of inventing it.

## Example 2: Creative Workflow Skill

Weak request:

```text
Make a skill for better ad prompts.
```

Gold direction:

```markdown
Decision: Focus on one repeatable ad creative workflow, not all marketing.
Trigger: image-generation prompts for a defined channel, offer, and audience.
Output: concept angle, visual composition, text constraints, negative prompt, variants, compliance notes.
References:
- offer-positioning.md
- platform-ad-rules.md if supplied or researched from official docs
Evals:
- vague offer
- banned claim
- mismatch between image and offer
- near miss: ordinary caption writing should not trigger
```

Why this is strong: it turns taste into repeatable artifact constraints and adds near-miss trigger protection.

## Example 3: Regulated-Domain Skill

Weak request:

```text
Build a legal contract review skill for my company.
```

Gold direction:

```markdown
Decision: Limited review-assistant skill only after source material is provided.
Required intake: sample contracts, playbook, clause library, risk tolerance, jurisdiction, escalation rules.
Must not do: present legal conclusions as advice, invent company policy, or approve contracts.
Output: issue table, clause references, risk severity, questions for counsel, missing-source warnings.
Validation: evals for missing policy, conflicting clause, unsafe approval request, jurisdiction ambiguity.
```

Why this is strong: the skill is useful while refusing to hallucinate authority.

## Example 4: Coding Skill

Weak request:

```text
Make a skill that improves React apps.
```

Gold direction:

```markdown
Decision: Split broad idea into focused skills.
First skill: React component review for accessibility, state boundaries, rendering cost, and design-system conformity.
Trigger: review or refactor React/TSX components.
References: local design-system rules, component library conventions, framework docs.
Scripts: optional lint/a11y command wrapper if the repo has tools.
Evals: overloaded component, missing labels, prop drilling, should-not-trigger general JavaScript question.
```

Why this is strong: broad "improve apps" becomes a testable, triggerable workflow.

## Example 5: Skill Factory Itself

Weak output:

```markdown
Create SKILL.md with best practices, add examples, test it.
```

Gold output:

```markdown
Skill Contract:
- User outcome
- Repeatable workflow
- Trigger and non-trigger contexts
- Inputs and outputs
- Tools and dependencies
- Gotchas and safety boundaries
- Validation method

Package Plan:
- SKILL.md only for always-needed workflow
- references for domain variants
- scripts for deterministic checks
- assets for templates
- evals for trigger/output cases

Benchmark:
- baseline prompt
- with-skill prompt
- captured outputs
- scorecard
- release decision
```

Why this is strong: it makes quality auditable instead of relying on confident prose.

## Common Gold Signals

- The skill rejects, splits, or reroutes a bad idea instead of blindly building it.
- Trigger and non-trigger contexts are both explicit.
- The package contains only files that affect runtime behavior or validation.
- Any private, legal, financial, medical, security, or company-specific claim is sourced or marked as an assumption.
- Validation includes near-misses, unsafe cases, and messy real-world prompts.
- Serious quality claims are backed by benchmark artifacts, not vibes.
