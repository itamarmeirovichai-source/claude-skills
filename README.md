# Claude Code Skills — minds + skill-prompt-architect

Two Claude Code skills, ready to install:

- **`/minds`** — all the model-minds in one: decisive (Fable), engineering (Sol), synthesis (Gemini), plus a debate mode and a 4-mind forge. Applies the right mind(s) to any question, decision, code task, or project.
- **`/skill-prompt-architect`** — turns vague or messy ideas into complete Claude Agent Skills or build prompts. Designs, validates, packages, and tunes skills end to end.

## Install (one line)

Paste this into Claude Code (or any terminal):

```bash
curl -fsSL https://raw.githubusercontent.com/itamarmeirovichai-source/claude-skills/main/install.sh | bash
```

This copies both skills into `~/.claude/skills/`. If you already have a skill with the same name, it's backed up first (`<name>.bak.*`), never silently overwritten.

Then open a **new** Claude Code session and type `/minds` or `/skill-prompt-architect`.

## Manual install

```bash
git clone --depth 1 https://github.com/itamarmeirovichai-source/claude-skills
cp -R claude-skills/skills/* ~/.claude/skills/
```
