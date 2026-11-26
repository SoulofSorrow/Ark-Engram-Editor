# AGENTS.md

Instructions for AI coding agents working in this repository. Tool-agnostic;
`CLAUDE.md` imports this file.

## Project

Ark Engram Editor: small tkinter desktop GUI (`start.py`, single file, Python
stdlib only) to edit ARK `OverrideNamedEngramEntries` lines: load, add, edit,
delete and save engram entries. `start.exe` is a prebuilt Windows binary.
License GPL-3.0 (`LICENSE.md`).

## Read first

1. `docs/README.md` (index).
2. `docs/architecture.md`: code structure, input and output file formats,
   known behaviour.

## Commands

```bash
python start.py      # start the GUI (needs a display and tkinter)
```

There is no test suite, no linter config and no build script for
`start.exe` in the repository. `Makefile` only contains repository setup
helpers (`.editorconfig`, `.gitignore`, `.dockerignore`, git hook, git
identity); it has no build or test targets.

Cheap syntax check without side effects:

```bash
python3 -c "import ast; ast.parse(open('start.py', encoding='utf-8').read())"
```

## Definition of done

- `start.py` still parses and the GUI starts.
- Output format of `save_data_to_file()` unchanged unless the change asks for
  it (ARK reads these lines).
- Affected doc in `docs/` updated.
- New file `docs/changes/YYYY-MM-DD-<slug>.md` (template in
  `.claude/skills/document-change/SKILL.md`), listed in `docs/README.md`.
- User-visible change: update `README.md` and `README.de.md` together.

## Hard rules

- Python stdlib only (`tkinter`, `re`); `requirements.txt` is empty.
- Do not rebuild or replace `start.exe` unless the user asks; there is no
  build script in the repository.
- Do not run `make set-git-local` or `make install-hooks`: they change local
  git config and hooks.
- No emojis in new code, logs or docs.

## Language

| Artifact | Language |
| --- | --- |
| Code identifiers | English |
| Code comments, GUI labels, error dialogs | German (existing) |
| `README.md`, `docs/`, `AGENTS.md`, commit messages | English |
| `README.de.md` | German |

Commits: imperative subject, no tool attribution trailers.

## Project skills

Located in `.claude/skills/<name>/SKILL.md`.

| Skill | Use for |
| --- | --- |
| `document-change` | Writing the `docs/changes/` record |
