<!-- markdownlint-disable -->

# Hardening Report: pypa--gh-action-pypi-publish/v1.14.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **pypa--gh-action-pypi-publish/v1.14.0** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): The 'Create Docker container action' step in action.yml directly interpolates ${{ }} expressions inside a `run:` shell command string. Specifically, the shell command is constructed using `${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }}` and `'${{ github.action_path }}/create-docker-action.py'`. Any ${{ ... }} expression interpolated directly into a run: block undergoes YAML template substitution before the shell parses it, allowing shell metacharacters to be injected. The `steps.*.outputs.*` values are workflow-controllable and `github.action_path` flows through the same unsafe substitution path.

Locations:

- `action.yml:125`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed the script-injection vulnerability in the 'Create Docker container action' step of action.yml. The two ${{ }} expressions that were directly interpolated into the run: shell command have been moved to the env: block as PYTHON_PATH (containing the Python interpreter path expression) and ACTION_PATH (containing github.action_path). The run: block now uses "$PYTHON_PATH" "$ACTION_PATH/create-docker-action.py" as plain shell variable references, preventing shell metacharacter injection.

