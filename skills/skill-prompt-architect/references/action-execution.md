# Action Execution

Use this reference when a generated skill should produce a real artifact or take real steps, not just plan or advise.

## Action-First Rule

If the user asks for an outcome, design the skill to execute the outcome within the available environment.

Examples:

- Website skill -> inspect the project, build or edit pages/components/styles, run checks, start or verify the app, and report changed files.
- Design skill -> use available design tools/connectors when present, generate or modify real assets, and verify output dimensions or previews.
- GitHub skill -> inspect repo state, create branches/commits/PRs only when requested or approved, and report exact diffs.
- Data skill -> load the actual files or connector data, transform/analyze it, write outputs, and validate row counts/schema.
- Deployment skill -> prepare and validate deploy config, deploy only through available approved tools, and report deployment URL/status.

If the environment cannot perform the action, the skill must produce the closest useful artifact and state the exact blocker.

## Capability Discovery

At the start of an action-capable run, map what is actually available:

1. Active tools in the current session.
2. Installed Claude skills shown in context.
3. Connectors/apps explicitly available or mentioned by the user.
4. MCP/tool discovery exposed by the environment. Prefer the environment's tool-discovery mechanism when available.
5. Workspace files, package managers, scripts, framework config, tests, and environment variables.
6. Existing server processes, browser targets, deployment config, or repo remotes when relevant.

Do not claim that a connector, MCP server, account, API, browser session, or deployment target exists unless it is exposed in the current environment or supplied by the user.

## Execution Contract

Every action skill should define:

```markdown
## Execution Contract
Primary artifact to create or modify:
Capabilities to discover first:
Tools/connectors/MCP routes to prefer:
Filesystem actions:
Commands to run:
Browser/app/API checks:
External actions requiring confirmation:
Verification evidence:
Fallback if a capability is unavailable:
```

## Tool Routing

Choose the strongest available route:

- Existing repo scripts before new scripts.
- Existing framework conventions before new architecture.
- Official connectors/MCP tools before manual browser or API work.
- Browser/app verification when the user-facing result matters.
- Deterministic scripts for repeatable parsing, packaging, validation, or scoring.
- Web research for current best practices when the domain changes over time or the user asks for world-class execution.

If multiple routes exist, use the one with the best verification path and lowest risk.

## Confirmation Boundary

Execute local, reversible, non-destructive work directly when the user asked for implementation.

Ask or require explicit approval before:

- Sending emails, messages, posts, comments, invites, forms, or notifications.
- Purchasing, publishing, deploying to production, deleting data, changing billing, or modifying external accounts.
- Exposing private data or secrets.
- Running destructive commands or migrations without a rollback path.
- Installing broad dependencies when the repo has no package manager context or the install changes many files unexpectedly.

When blocked by confirmation, prepare the exact command, draft, PR, or deploy artifact and mark it `ready for approval`.

## Website/App Skill Minimum

A generated website or app-building skill should include this execution loop:

1. Inspect the repo: framework, package manager, scripts, routing, styling system, components, assets, and existing design patterns.
2. Research the target domain or UX pattern when current or domain-specific quality matters.
3. Implement the requested page/component/app using existing conventions.
4. Run formatting, lint, typecheck, unit tests, build, or the closest available checks.
5. Start or use the dev server when needed.
6. Verify with browser/screenshot/DOM/canvas/API checks when available.
7. Fix observed issues and re-run the failing check.
8. Report changed files, commands run, verification result, and remaining blockers.

The skill should not stop at a package plan when the user asked it to build.

## ReAct + Reflection Loop

Action skills that produce artifacts should follow a self-correcting loop rather than a single linear pass:

```
Observe → Reason → Act → Reflect → Repeat
```

1. **Observe**: Read the actual environment state (files, tool output, error messages).
2. **Reason**: Based on what was observed, decide the next action.
3. **Act**: Execute exactly one meaningful action.
4. **Reflect**: After the action, check: did it produce the expected change? If not, diagnose before proceeding.
5. **Repeat**: Loop until the verification evidence confirms success or a blocker requires escalation.

A skill that acts once and declares success without reflection is not production-ready. Require at least one reflection check per major step — not a paragraph of meta-commentary, but a concrete check: run a test, inspect the output, diff the file, verify the response code.

## Evidence Requirements

Every action skill must end with concrete, non-interpretable evidence of success. Plans and explanations are not evidence.

**Valid evidence:**
- Test output with pass count
- Build output with zero errors
- `diff` showing the specific lines changed
- HTTP response code from a real request
- Screenshot or DOM snapshot of the rendered result
- Row/record count before and after a data operation

**Invalid evidence:**
- "The implementation looks correct"
- "This should work based on the code"
- "All steps were completed"

If the environment cannot produce evidence (no test runner, no browser, no build tool), the skill must say so explicitly and name the exact missing capability rather than substituting an assertion.

## Anti-Rationalization Table

Agents reliably invent reasons to skip the verification step. A skill must pre-empt the most common excuses:

| Excuse | Counter |
| --- | --- |
| "The code looks right, no need to run tests" | Run the tests. Looking right is not evidence. |
| "I can't run the dev server in this environment" | Identify the exact blocker and report it; do not silently skip verification. |
| "The user only asked for the code, not a check" | If the user asked for an outcome, the check is part of the outcome. |
| "Running the build would take too long" | Run the fastest available check (lint, typecheck, unit tests) instead. |
| "This is a simple change, it obviously won't break anything" | Simple changes break things. Run the check. |
| "I already checked the logic mentally" | Mental checks are not evidence. Execute the check. |
| "The framework guarantees correctness" | The framework guarantees syntax, not behavior. Test the behavior. |

Include this table in any skill whose primary output is a code artifact, configuration file, or deployed service.

## Anti-Overreach

Action-first does not mean reckless. A strong action skill is aggressive about local implementation and conservative about irreversible or externally visible actions.

Never:

- Invent access to unavailable connectors or MCP tools.
- Pretend web research, browser verification, deployment, or account updates happened when they did not.
- Hide failed commands or skipped checks.
- Treat a plan as equivalent to execution.
- Use "best practices" as a substitute for inspecting the actual project and verifying the result.
