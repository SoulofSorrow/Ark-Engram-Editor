# Architecture

## Files

| Path | Purpose |
| --- | --- |
| `start.py` | Whole application: module-level tkinter GUI and handler functions |
| `start.exe` | Prebuilt Windows GUI executable (PE32+, x86-64); no build script in the repository |
| `requirements.txt` | Empty (stdlib only) |
| `Makefile` | Repository setup helpers only (`setup`, `install-editorconfig`, `install-gitignore`, `install-dockerignore`, `install-hooks`, `set-git-local`, `check-git`, `test-hook`, `info`, `clean`) |
| `README.md`, `README.de.md` | User docs (English, German) |
| `LICENSE.md` | GPL-3.0 |

## Structure of `start.py`

- Module-level state: `data` (list of rows), widgets `tree`, `engram_entry`,
  `hidden`, `points_cost`, `level_requirement`, `remove_pre_req`.
- GUI is built at import time and ends with `root.mainloop()`; there is no
  `if __name__ == "__main__"` guard, so importing the module opens the window.

| Function | Trigger | Behaviour |
| --- | --- | --- |
| `update_table()` | internal | Rebuild `tree` from `data` |
| `add_data()` | button "Hinzufügen" | Append row from input fields |
| `edit_data()` | button "Bearbeiten" | Replace selected row |
| `delete_data()` | button "Löschen" | Remove selected row |
| `load_data(event)` | `<<TreeviewSelect>>` | Copy selected row into input fields |
| `clear_entries()` | internal | Reset input fields |
| `extract_and_add_data(input_string)` | internal | Parse one `OverrideNamedEngramEntries` line with `re` |
| `load_data_from_file()` | button "Entrys laden \"OverrideNamedEngramEntries\"" | Parse every line of a chosen file |
| `load_additional_data_from_file()` | button "Engram Entrys laden \"EngramEntry_Campfire_C\"" | One engram class name per line, defaults applied |
| `save_data_to_file()` | button "Daten Speichern" | Write all rows to a `.txt` file |

## Row model

`[EngramClassName, EngramHidden, EngramPointsCost, EngramLevelRequirement, RemoveEngramPreReq]`

- Empty `EngramPointsCost` / `EngramLevelRequirement` default to `2`.
- Non-integer values show an error dialog and the row is not added/changed.

## File formats

Input for `load_data_from_file()` and output of `save_data_to_file()`, one
entry per line:

```text
OverrideNamedEngramEntries=(EngramClassName="<name>",EngramHidden=<bool>,EngramPointsCost=<int>,EngramLevelRequirement=<int>,RemoveEngramPreReq=<bool>)
```

Input for `load_additional_data_from_file()`: one engram class name per line
(e.g. `EngramEntry_Campfire_C`).

## Known behaviour

- `save_data_to_file()` writes booleans with Python `str()` (`True`/`False`),
  while `extract_and_add_data()` only recognises lowercase `EngramHidden=true`
  and `RemoveEngramPreReq=true`. Reloading a saved file therefore resets both
  flags to `False`.
- Values taken back from the table via `load_data` are strings.
- Files are opened with the platform default encoding.
