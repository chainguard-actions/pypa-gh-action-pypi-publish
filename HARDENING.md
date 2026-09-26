<!-- markdownlint-disable -->

# Hardening Report: pypa--gh-action-pypi-publish/v1.14.2

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pypa--gh-action-pypi-publish/v1.14.2** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): The 'Create Docker container action' step in action.yml directly interpolates GitHub Actions expressions inside a `run:` shell command string. Specifically, `${{ steps.pre-installed-python.outputs.python-path }}`, `${{ steps.new-python.outputs.python-path }}`, and `${{ github.action_path }}` are all embedded directly in the shell command. The `steps.*.outputs.*` context is workflow-controllable and `github.*` values flow through YAML template substitution before the shell sees them, making this a script-injection risk. The offending lines are:

      ${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }} '${{ github.action_path }}/create-docker-action.py'

These expressions should be moved into `env:` variables and then referenced as quoted shell variables (e.g., `"$PYTHON_PATH"`) inside the `run:` block.

Locations:

- `action.yml:129`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed script injection in the 'Create Docker container action' step of action.yml. Moved the Python path ternary expression (${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }}) into a new PYTHON_PATH env var, and moved ${{ github.action_path }} into a new ACTION_PATH env var. The run: block now uses "$PYTHON_PATH" and "$ACTION_PATH/create-docker-action.py" as quoted shell variable references, eliminating the script injection risk.

