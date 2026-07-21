---
name: skill-prompt-architect
description: Turn vague or messy ideas into Claude Agent Skills or build prompts. Use when designing, validating, packaging, or tuning skills; not ordinary writing tasks.
---

# Skill Prompt Architect

Transform a raw idea into either:
1. A precise build prompt for Claude to create an Agent Skill.
2. A complete skill package with `SKILL.md` and any needed `references/`, `scripts/`, `assets/`, `evals/`.

Identify the repeatable workflow, capture non-obvious expertise, package it for reliable use. Design action skills to act, not just advise — build/edit, run checks, inspect results, verify, hand off files. State blocked external actions honestly.

## Track Selection (decide in Opening Council, state the pick, never offer both)
- **Tiny Skill track** — audience is claude.ai (no Claude Code), skill changes how Claude *answers* (style/format/decision behavior), zero scripts/network/file-ops, exactly one job. Deliverable: ONE short human-readable SKILL.md (≤3 KiB), a `.skill` upload file, a distribution page. Read `references/tiny-skill-pattern.md` — mandatory on this track.
- **Full Package track** — workflows, tools, scripts, references, actions. Everything below applies.

Serious-release rigor holds on both tracks; on the Tiny track the rigor goes into the before/after eval and trigger tuning — never into package size.

## 100/100 Target
Every skill optimized for 100/100, never falsely claimed without evidence.
- Cover: scope, trigger precision, procedure, domain specificity, progressive disclosure, resources, examples, validation, safety, benchmarking, maintenance.
- If benchmark missing → output exact blockers preventing verified 100/100.
- "100/100" request → read `references/world-class-100-gate.md`.
- Label "100/100 target-ready" when full protocol present but benchmark incomplete.
- Label "verified 100/100" only when benchmark summary proves every case = 100 with no critical failures.

## Run Mode: Every Run is Serious Release
No exceptions. Full council gates, capability discovery, research enrichment, strict validation, benchmark planning, final council. No fast-patch downgrade.

Every run: Opening Council → research enrichment (if search available) → 10-section output → validator + eval plan → kill-bloat pass → Final Council (decision: `ship` / `one focused revision` / `reject`) → delivery block (Claude Code + Cowork install).

Vague user → don't stall. Run Opening Council, then ask up to 3 targeted Qs shaped by verdict:
1. What should Claude repeatedly help you do?
2. What should the final output look like?
3. What should Claude avoid doing?
If context sufficient, skip and proceed with assumptions.

## Council Gates
Use `references/llm-council-method.md` (full, not quick protocol) at two points:
1. **Opening Council** — before design. Pressure-test: should this be a skill? best direction? what to avoid? what research needed? first build move?
2. **Final Council** — after draft + validation. Critique quality, missing pieces, safety, eval coverage, trigger clarity, delivery. On material improvement with sound reasoning → one focused revision pass, re-validate. Don't loop.

Sub-agents → run in parallel. No sub-agents → simulate 5 advisor roles independently, keep separate before synthesis.

## Core Workflow

1. **Opening Council** — load council method, frame as decision: what skill (if any) to build? Identify direction, risks, non-skill alternatives, research targets, first move.

2. **Clarify** — up to 3 questions on repeated outcome / final output / inputs+tools / trigger boundary / "must not do". If answers present, state assumptions and continue.

3. **Should this be a skill?**
   - Good fit: repeatable procedure, domain-specific workflow, project conventions, file transform, tool integration, recurring prompt/checklist.
   - Poor fit: one-off answer, broad personality preference, static context-knowledge, direct external access better via MCP/connector.
   - Read `references/decision-framework.md` when broad/risky/tool-heavy or could be prompt/memory/MCP/plugin/command/multi-skill.

4. **Research enrichment** — read `references/research-enrichment.md`. Run focused research before drafting if search available. Find: best-in-class practices, similar skill packages, official docs, OSS examples, mature templates, failure modes. Extract principles — don't copy passages. Capture source links in handoff notes. No search tools → state limitation, ask for sources, mark assumptions.

5. **Action + capability contract** — read `references/action-execution.md` if skill should build/edit/call-tools/connectors/MCP/deploy/verify. Inventory current session capabilities (tools, skills, connectors, files, scripts, env). Don't invent unavailable connectors. Decide: execute directly / prepare for approval / route to MCP / refuse-block. Website/app skills: real implementation behavior (inspect repo, use existing stack, create/edit, install/build/test/lint, start app, capture validation).

6. **Architecture**
   - `SKILL.md` — instructions Claude needs every time.
   - `references/` — situational details.
   - `scripts/` — deterministic/fragile code.
   - `assets/` — templates, samples, brand files.
   - `evals/` — tests, trigger tuning.

7. **Draft package or prompt**
   - Prompt request → full build prompt using `assets/claude-build-prompt-template.md`.
   - Package request → valid skill dir + handoff (install, test, share, Cowork delivery, expected actions).

8. **Auto-install after package creation** — this step is mandatory, not optional.
   After writing all skill files, immediately install the skill so it appears in the `/` command list:

   ```bash
   # Install to Claude Code global skills
   cp -R /path/to/<skill-name> ~/.claude/skills/<skill-name>

   # Install to Cowork too, if present (path contains per-install UUIDs — discover it)
   COWORK=$(ls -d "$HOME/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin"/*/*/skills 2>/dev/null | head -1)
   [ -n "$COWORK" ] && cp -R /path/to/<skill-name> "$COWORK/<skill-name>"
   ```

   After installing, confirm: `ls ~/.claude/skills/<skill-name>/` and verify SKILL.md exists.
   Tell the user: "Skill `<skill-name>` is installed — type `/<skill-name>` to use it."
   If the skill was written to `~/.claude/skills/<skill-name>/` directly (not a temp path), skip the cp and just verify + sync to Cowork.

9. **Validate**
   - Check frontmatter, file refs, package shape, trigger description, examples, edges, safety.
   - Run `python scripts/validate_skill_package.py <skill-dir>` if package local.
   - Should-trigger + should-not-trigger test prompts.
   - Serious releases: create/update benchmarks with `scripts/run_eval_harness.py` (`init <skill-dir>`), capture baseline/with-skill before claiming 90+.
   - 100/100 → `--target-100` scoring gate after real outputs exist. Fail → report missing points (don't inflate).
   - Complex skills: compare with/without skill, revise on failures.
   - Every finished skill includes: readiness score, blockers, exact fixes, pass/fail. Minimum gate for serious use = 85/100.

10. **Final Council** — review draft. Decision: `ship` / `one focused revision` / `reject`. Kill-bloat pass: each advisor names one thing to remove. On material improvement with sound reasoning → one focused revision + re-validate. Include verdict in handoff.

## Required Skill Shape
```
skill-name/
├── SKILL.md
├── references/   # optional
├── scripts/      # optional
├── assets/       # optional
└── evals/        # optional
```

Frontmatter (required):
```
---
name: skill-name
description: What the skill does and when to use it.
---
```

**Name**: lowercase + numbers + hyphens, <64 chars, matches dir, no leading/trailing hyphen, no reserved names.

**Description**: what + when, natural trigger keywords, specific enough to avoid false triggers. Claude.ai uploads: <200 chars unless target supports longer. Tuning → `references/trigger-best-practices.md`.

## Progressive Disclosure: L1 / L2 / L3
Every generated skill follows this token budget — reduces context cost ~90%:

```
L1 — Metadata (~100 tokens)
     YAML frontmatter only. Runtime activation decision.

L2 — Core instructions (<5,000 tokens)
     SKILL.md body. Loaded on trigger. Self-sufficient for ~80% of runs.
     Reference pointers listed but NOT loaded.

L3 — External (unlimited, on-demand)
     references/ + scripts/ + assets/. Loaded only when SKILL.md says
     "read this when <condition>".
```

**Test**: can the skill complete an average run with only L2? If yes → correct. If L2 requires loading multiple refs every run → refactor (promote into L2 or rethink primary workflow).

**L2 must include explicit L3 loading conditions.** Every reference file appears with `"Read references/foo.md when X"`. Never list a reference without a loading condition.

## What goes where
- **SKILL.md (L2)**: procedure, non-obvious gotchas, tool/library defaults, short always-relevant templates, explicit "read references/X.md when..." conditions.
- **references/ (L3)**: detailed docs, policies, schemas, API notes, style guides, large examples, domain variants.
- **scripts/ (L3)**: deterministic/fragile reusable code. Non-interactive, `--help`, useful exit codes, structured stdout, diagnostics to stderr, safe defaults, `--dry-run` for destructive ops. Validator when skill creates/modifies packages.
- **assets/ (L3)**: templates, skeletons, images, brand files.
- **evals/**: realistic test prompts, expected outputs, trigger tests, grading assertions.

## Converting hard ideas

```
## Skill Contract
Working name: / User outcome: / Repeatable workflow: / Inputs: / Outputs:
Trigger contexts: / Non-trigger contexts: / Tools+dependencies:
Capability discovery: / Actions to execute: / Actions requiring confirmation:
Project/domain knowledge Claude lacks: / Gotchas: / Safety constraints:
Validation method: / GitHub/share target:
```

```
## Package Plan
skill-name: / description: / SKILL.md sections: / references: / scripts:
assets: / evals: / install path: / action+verification plan: / GitHub workflow:
```

Too broad → split into multiple skills with explicit boundary.

## Required Output Contract (in order)
1. `Skill Brief` — purpose, target user, target outcome.
2. `Opening Council Verdict`
3. `Decision` — skill vs prompt vs memory vs MCP vs split/reject.
4. `Research Synthesis` — searches, sources, patterns; assumptions if no search.
5. `Skill Contract` — inputs/outputs/triggers/non-triggers/tools/capabilities/actions/gotchas/safety.
6. `Package Plan` — exact files, why each exists, how skill acts (not just advises).
7. `Build Prompt Or Files` — ready prompt or created package, with execution+verification behavior.
8. `Validation` — validator command, eval plan, readiness score, blockers, fixes.
9. `Final Council Verdict` — review + applied changes.
10. `Delivery` — personal Claude Code, project Claude Code, Cowork/workspace, Claude.ai `.skill` (zip skill dir, rename to `.skill`; install: Settings → Capabilities → Skills → upload; fallback: attach in chat + "load this skill and use it from now on"), GitHub. Non-technical audience → also generate a distribution page from `assets/distribution-page-template.md`.

Not applicable → include with `Not needed because...`.

## Writing Quality Rules
- Procedures over declarations.
- Add what Claude lacks; omit what it knows.
- Strong default, not menu of equals.
- **Decisive delivery (smooth-brain rule)**: when a design choice arises (name, structure, track, scope), pick one and commit with a one-line reason. A menu of options is a failure mode. Instead of serving every option — just pick.
- **The response IS the spec**: for behavioral skills, write the exact target answer first, design backwards from it.
- **Before/after demo**: every skill ships a same-prompt stock-Claude vs with-skill pair. No dramatic visible diff → don't ship.
- **When-NOT-to-use is part of the product**: every skill states where its behavior is wrong; the behavior is a feature, not a substitute for judgment.
- **Trust by transparency**: generated skills must be safe to read before loading — no hidden fetches, no surprise code; tell users to read any skill file before loading it.
- Explain reason behind important constraints.
- SKILL.md <500 lines.
- Avoid vague "best practices" — name the specific local practice.
- Include examples when output format matters.
- Include gotchas where Claude makes plausible-but-wrong assumptions.
- No hardcoded secrets/credentials/tokens/personal data.
- Reject skills that hide behavior, exfiltrate data, bypass authorization, automate unauthorized access, do destructive actions without confirmation, or handle secrets.
- Don't invent company/legal/financial/medical/security/API/platform policies without source. Mark assumptions, request sources when private/current facts matter.

## Output Formats
**Prompt-only request** → output: brief + opening verdict + decision/assumptions + research + contract + sources + file structure + detailed build prompt + validation checklist + final verdict + GitHub steps.

**Package request** → create files directly to `~/.claude/skills/<skill-name>/`, then auto-install to Cowork. End with: files created / confirmation that `/<skill-name>` is live in Claude Code / Cowork sync status / validation incl. `validate_skill_package.py` / readiness score + blockers + fixes / source links.

## Quality Gate (score with `references/skill-authoring-rubric.md`)
- 90-100: serious use.
- 85-89: usable with listed fixes.
- 70-84: good draft, not production.
- <70: redesign.

Don't call world-class without: examples + evals + validator/plan + decision gates + safety + maintenance.
Don't score 90+ without benchmark evidence or concrete plan with captured artifacts.
Don't score 100/100 without passing perfect-score gate in `references/world-class-100-gate.md`.
Don't call action skill production-ready without capability discovery + real execution steps + confirmation boundaries + verification.

## Reference loading conditions
- `references/tiny-skill-pattern.md` — Tiny Skill track: claude.ai-only audience, single-behavior skills, `.skill` packaging, distribution pages.
- `references/intake-framework.md` — user has rough idea, needs guided discovery.
- `references/llm-council-method.md` — every council run (always load, never abbreviate).
- `references/decision-framework.md` — deciding skill vs split vs reject vs different mechanism.
- `references/research-enrichment.md` — creating/improving a skill + search tools available.
- `references/action-execution.md` — skill must build/edit/call-tools/MCP/deploy/inspect/verify real artifacts.
- `references/trigger-best-practices.md` — writing/reviewing skill descriptions and should-not-trigger evals.
- `references/skill-authoring-rubric.md` — finalizing or reviewing a skill.
- `references/evaluation-playbook.md` — writing tests, trigger queries, iteration plans.
- `references/benchmarking-and-scorecards.md` — proving quality, before/after, deciding 90+.
- `references/world-class-100-gate.md` — 100/100 quality requests.
- `references/github-delivery.md` — GitHub sharing/install/Actions/PR workflows.
- `references/worked-examples.md` — examples needed or output feels generic.
- `references/gold-standard-examples.md` — world-class quality, richer examples, cross-domain.
- `references/lifecycle-feedback.md` — publishing/versioning/maintaining after real use.
- `assets/claude-build-prompt-template.md` — ready-to-paste prompt for Claude.
- `assets/distribution-page-template.md` — writing a share/landing page for a finished skill (Tiny track: mandatory).
- `scripts/build_all_in_one.py` — regenerate one-file dossiers + checksum files.
