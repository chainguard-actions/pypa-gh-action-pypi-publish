<!-- markdownlint-disable -->

# Hardening Report: pypa--gh-action-pypi-publish/v1.14.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pypa--gh-action-pypi-publish/v1.14.0** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): The 'Create Docker container action' step's `run:` block directly interpolates GitHub Actions expressions inside the shell command string. Specifically, `${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }}` is used as the Python interpreter path, and `'${{ github.action_path }}/create-docker-action.py'` is used as a script path argument. Both are `${{ ... }}` expressions embedded directly in the shell command before the shell processes them, enabling script injection if any of these values contain shell metacharacters. The `steps.*.outputs.*` values come from prior steps and `github.action_path` is a GitHub-controlled context, but any `${{ ... }}` directly inside a `run:` block is a script-injection risk regardless of the source context.

Locations:

- `action.yml:124`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed script injection in the 'Create Docker container action' step of action.yml. Moved both ${{ }} expressions from the run: shell command into the env: block: (1) the Python path ternary expression `${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }}` is now the `PYTHON_PATH` env var, and (2) `${{ github.action_path }}` is now the `ACTION_PATH` env var. The run: block now uses `"$PYTHON_PATH" "$ACTION_PATH/create-docker-action.py"` with plain shell variable references, eliminating the injection risk while preserving identical runtime behavior.

