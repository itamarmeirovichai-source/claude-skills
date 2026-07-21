# GitHub Delivery

Use this reference when the user wants to store, share, install, or run a skill through GitHub, Claude Code, or Claude Cowork/workspace.

## Choose A Delivery Path

```markdown
Personal reuse across projects -> install in ~/.claude/skills/
Repo-specific workflow -> commit under .claude/skills/
Claude.ai manual use -> ZIP and upload
Claude Cowork/workspace use -> install through the provided workspace path, connector, or ZIP upload/import workflow
Public sharing -> GitHub repo with README outside the skill package
Automated PR/issue work -> Claude Code on the web or GitHub Actions
```

## Local Claude Code Installation

Personal skill, available across projects:

```bash
mkdir -p ~/.claude/skills
cp -R skill-prompt-architect ~/.claude/skills/
```

Project skill, committed with a repository:

```bash
mkdir -p .claude/skills
cp -R skill-prompt-architect .claude/skills/
git add .claude/skills/skill-prompt-architect
git commit -m "Add skill prompt architect skill"
```

## Claude.ai Upload

Package the skill as a ZIP that contains the skill directory at the ZIP root:

```bash
zip -r skill-prompt-architect.zip skill-prompt-architect
```

Expected structure:

```text
skill-prompt-architect.zip
└── skill-prompt-architect/
    ├── SKILL.md
    ├── references/
    ├── assets/
    └── evals/
```

Upload through Claude's Skills settings and enable the skill. Then test with prompts that should trigger it and near-misses that should not.

## Claude Cowork Or Workspace Delivery

When the user asks to create a skill package, include Claude Cowork/workspace delivery in the handoff.

Use this order:

1. If the user provides a Claude Cowork/workspace skills path, copy or commit the skill there.
2. If an environment variable such as `CLAUDE_COWORK_SKILLS_DIR` is present, use it as the target path after confirming it points to a skills directory.
3. If no local target is known, create the ZIP and provide upload/import instructions.
4. Do not invent a local Claude Cowork path. Mark the target as `Needs user-provided Cowork path or upload access`.

Example local-path flow:

```bash
mkdir -p "$CLAUDE_COWORK_SKILLS_DIR"
cp -R skill-prompt-architect "$CLAUDE_COWORK_SKILLS_DIR/"
```

Example no-path handoff:

```markdown
Claude Cowork/workspace delivery:
- Package: skill-prompt-architect.zip
- Status: ready for upload/import
- Blocker: no local Cowork skills path was provided
- Next step: upload/import the ZIP in the Cowork/workspace skill settings, or provide the target skills directory for direct install
```

For generated skills, always include both Claude Code delivery and Claude Cowork/workspace delivery unless the user explicitly asks for one target only.

## GitHub Repository Sharing

Recommended repo layout for a single skill:

```text
my-skill-repo/
├── skill-prompt-architect/
│   ├── SKILL.md
│   ├── references/
│   ├── assets/
│   └── evals/
├── README.md
└── LICENSE
```

## Claude Code On The Web

Claude Code on the web works from GitHub repositories. Typical flow:

1. Connect GitHub in Claude Code on the web.
2. Select the repository and branch.
3. Submit a task.
4. Claude clones the repo into an isolated environment.
5. Claude works, runs checks, and pushes a branch.
6. Review the diff and create a PR.

If the skill is committed under `.claude/skills/<skill-name>/`, Claude Code can discover it in that project context.

## GitHub Actions With Claude Code

Use GitHub Actions when you want Claude to respond to issues, PR comments, or scheduled tasks.

Minimum concepts:
- Install the Claude GitHub App or configure an app/token with least privilege.
- Store `ANTHROPIC_API_KEY` as a GitHub Actions secret.
- Use `anthropics/claude-code-action@v1`.
- Keep project standards in `CLAUDE.md`.
- Store project skills under `.claude/skills/` if the action should use them.

Security rules:
- Never commit API keys.
- Prefer GitHub Secrets.
- Limit permissions to the workflow's actual needs.
- Review Claude's PRs before merging.
- Audit downloaded skills before enabling them, especially skills with scripts.
- Re-run validation after changing `SKILL.md`, references, scripts, or evals.
