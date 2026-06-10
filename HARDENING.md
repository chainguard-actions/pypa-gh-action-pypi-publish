<!-- markdownlint-disable -->

# Hardening Report: pypa--gh-action-pypi-publish/v1.13.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **pypa--gh-action-pypi-publish/v1.13.0** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): The 'Create Docker container action' step in action.yml directly interpolates two ${{ ... }} expressions inside a `run:` shell command string, before the shell ever sees the value. (1) `${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }}` — a `steps.*.outputs.*` expression used as the Python interpreter path in the shell command. (2) `'${{ github.action_path }}/create-docker-action.py'` — the `github.action_path` context value is interpolated directly into the shell command string. Any `${{ ... }}` inside a `run:` block is a script-injection risk because the value is substituted by the Actions runner into the shell script text before the shell parses it, allowing metacharacters to break out of the intended command structure.

Locations:

- `action.yml:116`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed script injection in the 'Create Docker container action' step of action.yml. Moved two ${{ }} expressions out of the run: shell command string and into the env: block: (1) the Python interpreter path expression is now PYTHON_PATH env var, (2) github.action_path is now ACTION_PATH env var. The run: block now uses "$PYTHON_PATH" "$ACTION_PATH/create-docker-action.py" as plain shell variable references, eliminating the risk of shell metacharacter injection from runner-interpolated values.

