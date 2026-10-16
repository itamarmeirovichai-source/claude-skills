# Claude Code Skills

Four Claude Code skills, ready to install:

- **`/minds`** — all the model-minds in one: decisive (Fable), engineering (Sol), synthesis (Gemini), plus a debate mode and a 4-mind forge. Applies the right mind(s) to any question, decision, code task, or project.
- **`/skill-prompt-architect`** — turns vague or messy ideas into complete Claude Agent Skills or build prompts. Designs, validates, packages, and tunes skills end to end.
- **`/live-results`** — reports numbers from something still running (forward test, A/B test, campaign) in one screenful, and closes on the base rate that says whether the number means anything yet.
- **`/prop-fleet`** — sizing, payout and scaling rules for a fleet of funded futures prop accounts: two-speed sizing, the capped payout ladder, the evidence gate that decides how many accounts you are allowed to run, and a trade-record validator.

## Install (one line)

**Easiest — any OS:** paste this into Claude Code itself (its shell is bash on every platform, including Windows via Git Bash):

```bash
curl -fsSL https://raw.githubusercontent.com/itamarmeirovichai-source/claude-skills/main/install.sh | bash
```

**Windows PowerShell** (if you prefer a regular terminal instead of Claude Code):

```powershell
irm https://raw.githubusercontent.com/itamarmeirovichai-source/claude-skills/main/install.ps1 | iex
```

**macOS / Linux terminal:** same `curl` line as above.

Both installers copy the skills into `~/.claude/skills/`. If you already have a skill with the same name, it's backed up first (`<name>.bak.*`), never silently overwritten.

Then open a **new** Claude Code session and type `/minds`, `/skill-prompt-architect`, `/live-results` or `/prop-fleet`.

## Manual install

```bash
git clone --depth 1 https://github.com/itamarmeirovichai-source/claude-skills
cp -R claude-skills/skills/* ~/.claude/skills/
```
