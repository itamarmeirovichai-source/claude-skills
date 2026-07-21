# Research Enrichment

Use this reference whenever creating or substantially improving a skill. The goal is to avoid building from the user's raw idea alone. Enrich the skill with current, high-quality examples, domain standards, and similar skill patterns before drafting.

## When To Research

Run research automatically when:

- The user asks to create a new skill.
- The user asks for a "world-class", "best", "elite", or "professional" skill.
- The domain has mature external standards or fast-changing best practices.
- The skill depends on tools, APIs, design methods, legal/compliance rules, platform behavior, or GitHub workflows.
- The user names a broad domain such as web design, UX, SEO, sales, analytics, product management, coding, research, writing, or automation.

Do not over-research trivial one-off prompt requests. Use the decision framework first if the task may not be a skill.

## Research Targets

Search for five kinds of material:

1. Domain excellence: best practices, expert frameworks, checklists, style guides, quality rubrics.
2. Existing skills: Claude/Agent Skills, Codex skills, open-source skill packages, prompts, runbooks, or assistants for the same workflow.
3. Official sources: platform docs, API docs, framework docs, standards bodies, vendor guidance.
4. Real examples: GitHub repos, templates, case studies, before/after examples, benchmark artifacts.
5. Failure modes: common mistakes, security risks, usability problems, trigger false positives, edge cases.

## Source Quality Filter

Prefer:

- Official documentation.
- Source repositories with real files.
- Maintained open-source projects.
- Well-known standards or accessibility guidance.
- Reputable practitioners with concrete examples.
- Recent docs for fast-moving tools.

Avoid:

- Thin SEO summaries.
- Unattributed prompt dumps.
- Outdated posts when the tool/framework changes quickly.
- Copying proprietary templates or long copyrighted text.
- Treating popularity as proof of quality.

## Research Output

Include a short synthesis in the final answer or handoff:

```markdown
## Research Synthesis
Searched:
- ...

Strongest sources/examples:
- [source name](url) - why it matters

Patterns extracted:
- ...

Risks/failure modes:
- ...

How this changed the skill design:
- ...

Assumptions:
- ...
```

If browsing/search is unavailable:

```markdown
## Research Synthesis
Search status: unavailable in this environment.
Assumptions:
- ...
Source material needed:
- ...
Fallback: proceeding from the provided context and clearly marking unverified domain assumptions.
```

## How To Use Research In The Skill

- Put only always-needed workflow guidance in `SKILL.md`.
- Put detailed domain research into `references/`.
- Add examples from research to `worked-examples.md` only when they are transformed into original, non-copyrighted examples.
- Add evals for the most important failure modes discovered.
- Add scripts only when research reveals deterministic checks or repeatable validation needs.

## Research Discipline

- Cite source links in handoff notes.
- Use concise paraphrase, not long quotations.
- Prefer patterns over copied text.
- Do not claim research was performed if tools were unavailable.
- Do not let research bloat the core skill. The best findings become constraints, examples, evals, or scripts.
- Do not invent company-specific, legal, financial, medical, security, API, or platform policies. If sources are missing, mark assumptions and ask for source material.
