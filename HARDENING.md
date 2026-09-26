<!-- markdownlint-disable -->

# Hardening Report: pypa--gh-action-pypi-publish/v1.14.1

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pypa--gh-action-pypi-publish/v1.14.1** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

The 'Create Docker container action' step in action.yml directly interpolates ${{ }} expressions inside the run: shell command string (rule a). Specifically, the run block uses `${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }}` and `${{ github.action_path }}` directly in the shell command. All ${{ }} expressions inside run: blocks are script-injection risks because they are substituted by the YAML/Actions template engine before the shell ever sees them, allowing any attacker-controlled or unexpected value to break out of the intended command structure. The offending lines are the run: block of the 'Create Docker container action' step (around line 123-129 of action.yml).

Locations:

- `action.yml:123`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed the 'Create Docker container action' step in action.yml by moving both ${{ }} expressions out of the run: shell command and into the env: block. Specifically: (1) the conditional Python path expression (${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }}) is now stored in PYTHON_PATH env var; (2) ${{ github.action_path }} is now stored in ACTION_PATH env var. The run: block now uses "$PYTHON_PATH" "$ACTION_PATH/create-docker-action.py" with plain shell variable references. The existing REF, REPO, and REPO_ID env vars were merged into the single env: block.

