# Lab 5: Static Code Analysis (Pylint, Bandit, Flake8)

**Script analysed:** support_ticket_tracker.py

## Results Summary

| Tool | Before | After |
|---|---|---|
| Bandit | 2 issues | 0 issues |
| Pylint | 5.00/10 | 10.00/10 |
| Flake8 | 12 issues | 0 issues |

## Issues Table

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Use of `eval()` | Bandit B307, Pylint W0123 (Security) | 92 | `eval()` can execute arbitrary code, which allows code injection. | Replace with `ast.literal_eval()` or an explicit `int()`/`float()` conversion. |
| Bare `except` with `pass` | Bandit B110, Pylint W0702, Flake8 E722 (Security, Error handling) | 24 | Catches every exception, including `KeyboardInterrupt`, and silently hides errors. | Catch a specific exception and log or handle it instead of `pass`. |
| Dangerous default argument `[]` | Pylint W0102 (Bug risk) | 10 | A mutable default list is shared across calls, so state leaks between calls. | Use `=None` and create a new list inside the function. |
| Too many arguments | Pylint R0913, R0917 (Design) | 10 | The function takes 6 arguments (limit 5). | Group related parameters or reduce the argument count. |
| Missing docstrings | Pylint C0114, C0116 (Documentation) | 1, 10, 20, 29, 34, 45, 51, 58, 66, 70, 77 | The module and ten functions have no docstrings. | Added a short docstring to the module and each function. |
| Function naming `closeTicket` | Pylint C0103 (Naming) | 66 | camelCase violates PEP 8 snake_case. | Renamed to `close_ticket` and updated all call sites. |
| Unused imports (`sys`, `random`) | Pylint W0611, Flake8 F401 (Clean code) | 4, 5 | Imported but never used. | Removed both imports. |
| Unused variable / argument | Pylint W0612, W0613, Flake8 F841 (Clean code) | 84 (`count`), 20 (`notify`) | Dead variable and an argument that is never used. | Removed `count`; removed or used `notify`. |
| Comparison to `None` with `!=` | Pylint C0121, R1714, Flake8 E711 (Correctness) | 37 | Should use identity for `None`, and the comparisons can be merged. | Changed to `is not None` and simplified the condition. |
| `open()` without encoding or `with` | Pylint W1514, R1732 (Resource handling) | 46, 53 | Files are opened with the platform default encoding and may never be closed. | Use `with open(..., encoding="utf-8") as f:`. |
| Global statement | Pylint W0603 (Design) | 52 | Using `global` makes state hard to track and test. | Refactor to pass or return state, or document and minimize its use. |
| String formatting style | Pylint C0209, W1203 (Style) | 16, 85 | `%`-formatting where an f-string fits, and an f-string inside a logging call. | Use an f-string on line 16; use lazy `%s` formatting in logging on line 85. |
| Redundant code patterns | Pylint C1802, R1703, R1705 (Simplification) | 60, 71 | `len()` used as a truth test, an `if` that could be `return bool(...)`, and `else` after `return`. | Use `if not seq:`, return the boolean directly, and drop the `else`. |
| Lines too long | Pylint C0301 (limit 100), Flake8 E501 (limit 79) | 10, 14, 63, 71, 79, 80 | Pylint flags only lines 10 and 14. Flake8's stricter limit flags six lines. | Split across lines with parentheses or implicit string concatenation. |
| Trailing whitespace | Pylint C0303, Flake8 W291 (Style) | 84 | Stray spaces at the end of a line. | Stripped the whitespace. |
| KeyError on non-existent ticket ID (manual finding) | Logic bug, flagged by no tool | `close_ticket` (originally line 66) | Closing an ID that doesn't exist crashes with `KeyError`. | Check `if ticket_id in tickets` first and print a "ticket not found" message. |

