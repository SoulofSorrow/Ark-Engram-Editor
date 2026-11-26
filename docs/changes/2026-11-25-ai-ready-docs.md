---
date: 2026-11-25
type: docs
scope: docs, agent tooling
files: [AGENTS.md, CLAUDE.md, .claude/settings.json, .claude/skills/document-change/SKILL.md, docs/README.md, docs/architecture.md, docs/changes/2026-11-25-ai-ready-docs.md, README.md, README.de.md]
breaking: false
---
# Agent-ready documentation and project skills

## Context

- The repository had no `docs/` folder and no instructions for AI coding
  agents.
- The application is a single file (`start.py`); docs are sized accordingly.

## Change

- `docs/README.md`: index of docs and change records, maintenance rules.
- `docs/architecture.md`: file map, functions of `start.py`, row model, file
  formats, known behaviour.
- `AGENTS.md`: tool-agnostic agent instructions (commands, definition of done,
  hard rules, language table, skill list).
- `CLAUDE.md`: imports `AGENTS.md` via `@AGENTS.md`, Claude Code notes.
- `.claude/settings.json`: allows the `ast.parse` syntax check, `make help`,
  `make check-git`, `make info`; asks before `git push` and the `make` targets
  that write files, hooks or git config; denies reading `.env`.
- `.claude/skills/document-change/SKILL.md`: change record template.
- `README.md`, `README.de.md`: section pointing to `docs/` and `AGENTS.md`.

## Decisions

- Only the `document-change` skill: no other recurring multi-step task exists
  in this single-file tool.
- No application code, build files or dependencies changed.

## Usage / Verification

```bash
python3 -m json.tool .claude/settings.json
python3 -c "import ast; ast.parse(open('start.py', encoding='utf-8').read())"
ls docs docs/changes .claude/skills
```

## Follow-ups

- Bug: `save_data_to_file()` writes `True`/`False`, `extract_and_add_data()`
  only matches lowercase `true`; `EngramHidden` and `RemoveEngramPreReq` are
  lost on reload.
- Comments in `start.py` mention a double-click; the code binds
  `<<TreeviewSelect>>` (single selection). `README.md` mentions a button
  "Load Data"; the GUI labels differ (German).
- `start.exe` is a committed binary without a build script or provenance.
- `.gitignore` only contains `test/`; `Makefile` contains a personal e-mail in
  `GIT_EMAIL` and emojis in the `info` target.
- `Makefile` has no build, test or tag targets.
- Missing standard files: `.editorconfig`, `CHANGELOG.md`, `CONTRIBUTING.md`,
  `.pre-commit-config.yaml`.
