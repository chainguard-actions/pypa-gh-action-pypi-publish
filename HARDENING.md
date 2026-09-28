<!-- markdownlint-disable -->

# Hardening Report: pypa--gh-action-pypi-publish/v1.13.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pypa--gh-action-pypi-publish/v1.13.0** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

The 'Create Docker container action' step in action.yml directly interpolates GitHub Actions expressions inside a `run:` shell command string (rule a). Specifically: `${{ steps.pre-installed-python.outputs.python-path }}`, `${{ steps.new-python.outputs.python-path }}`, and `${{ github.action_path }}` are all embedded directly in the shell command. These values flow through YAML template substitution before the shell processes them, allowing an attacker-controlled value (e.g. a crafted python-path output from a prior step, or a manipulated action_path) to inject arbitrary shell commands. The offending lines are:
  - `${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }}` used as the Python interpreter command
  - `'${{ github.action_path }}/create-docker-action.py'` used as the script path argument
These should be moved to `env:` variables and then referenced as quoted shell variables (e.g. `"$PYTHON_PATH"`, `"$ACTION_PATH"`).

Locations:

- `action.yml:109`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed script injection in the 'Create Docker container action' step of action.yml. Moved the two ${{ }} expressions from the run: shell command into the env: block: (1) the Python path ternary expression (${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }}) is now set as PYTHON_PATH env var, and (2) ${{ github.action_path }} is now set as ACTION_PATH env var. The run: command now uses "$PYTHON_PATH" and "$ACTION_PATH/create-docker-action.py" as quoted shell variable references, preventing shell injection.

