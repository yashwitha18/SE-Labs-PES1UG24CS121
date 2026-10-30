# Reflection: Lab 5 Static Code Analysis

## 1. Which issues were the easiest and hardest to fix?

The easiest were mechanical ones: removing the unused `sys` and `random` imports, stripping trailing whitespace, and changing `!= None` to `is not None`. The tools point at the exact line and the fix is obvious.

The hardest were the ones needing judgment. Replacing `eval()` on line 92 meant working out what input it was meant to handle and choosing a safe conversion. Replacing the bare `except: pass` on line 24 meant deciding which exception to catch and what to do with it. [EDIT: add one sentence on whichever fix took you the longest.]

## 2. Did the tools report any false positives?

Mostly no. Every Bandit finding was real. Some Pylint findings are matters of opinion, such as the `global` statement warning and "too many arguments", which are design suggestions rather than bugs. Pylint and Flake8 also use different line-length limits (100 vs 79), so a line can pass one tool and fail the other. That is a configuration mismatch, not a defect.

## 3. How could you integrate static analysis into a real workflow?

Run Pylint and Flake8 live in the editor while coding. Add a pre-commit hook so commits with violations are blocked. Add a CI step (for example GitHub Actions) that runs all three tools on every pull request, failing the build on any Bandit finding or a Pylint score below a threshold such as 9.5.

## 4. What improvements did you see in the code after the fixes?

Pylint went from 5.00/10 to 10.00/10, Bandit from 2 issues to 0, and Flake8 from 12 issues to 0. Removing `eval()` and the silent `except: pass` made the code safer. Fixing the mutable default argument, using `with open(...)`, and handling missing ticket IDs made it more robust. Docstrings, snake_case names and PEP 8 formatting made it easier to read.

## Bug found by hand

Closing a ticket with an ID that does not exist crashed the program with a `KeyError`, and no tool flagged it. The fix is to check whether the ID exists before accessing it and print a "ticket not found" message. This shows static analysis complements testing and manual review rather than replacing them.