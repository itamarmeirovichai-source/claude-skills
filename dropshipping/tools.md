# Tools (iron law 15, overlay §5)

## 1. Inventory of what the session has (2026-11-10)

| Tool | Kind | Status | Touches credentials? | Note |
|---|---|---|---|---|
| WebSearch, WebFetch | search / fetch | working | no | Several primary pages block fetches (gov.il, kolzchut, Meta Business Help, Namecheap, Triple Whale, Higgsfield pricing). Playwright rendering of bot-protected pages was refused by the session's permission policy and is not retried |
| Bash + Python 3 | code execution | working | no | `goal_math.py` runs with `python3 -I` |
| Playwright + Chromium | browser automation | present | no | usable for the program's own store pages and screenshots, not for bypassing bot checks |
| GitHub MCP (`mcp__github__*`) | repo, PRs | working, scoped to this repo | repo token (session) | PR creation, no search |
| Motion Creative Analytics MCP (`mcp__Motion_Creative_Analytics__*`) | Meta creative analytics (Meta-only data) | `get_auth_context` called 2026-11-10 (read-only): no organizations, no workspace → brand/inspo tools unusable | would read a connected Meta ad workspace | Unusable on this account; re-check only if the operator later creates a Motion workspace |
| Canva, Adobe Express, Figma, Gamma MCPs | design / video | present, not called | Canva/Adobe accounts | Candidate creative tools; vet rights and cost before use |
| Gmail, Google Drive, Calendar MCPs | connectors | present, not called | operator's Google account | Not needed in Phase 0. Any use is logged here first |
| `anthropic-skills:meta-ad-prompt-architect` | skill | present | no | Candidate for creative briefs; vet in the Phase 1 tooling unit |
| `firecrawl:*` skills | scraping | CLI not installed (`firecrawl: command not found`) | would need API key | Not installed; WebFetch suffices for now |
| `dataviz`, `xlsx`, `docx`, `pdf` skills | reporting | present | no | For the weekly report if needed |
| Claude Docs, Artifact | publishing | present | no | Not used; deliverable is the repo |

## 2. Candidate search (overlay §5 step 2)
Not started. Next tooling unit: search official integrations (Shopify Admin API / MCP, Meta Marketing API, AutoDS API, Higgsfield API), then GitHub (shopify mcp, meta ads mcp, facebook marketing api agent, dropshipping automation, ad creative generation, higgsfield api), then marketplaces. Log each candidate below before installing anything.

## 3. Vetting log

| Date | Tool | Source / version | Purpose | Code/manifest read | Maintenance | Permissions and credential path | Phones home? | License | First-party alternative? | Smoke test | Approval needed | Decision |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (none yet) | | | | | | | | | | | | |

## 4. Installed

| Name | Source | Version | Purpose | Vetting ref | Approval | Installed | Last re-vet | Remove-by (unused 30 days) |
|---|---|---|---|---|---|---|---|---|
| (none) | | | | | | | | |
