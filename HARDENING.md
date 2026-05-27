# Hardening Report: pypa--gh-action-pypi-publish/v1.13.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `ff50f15e4b79bfbf764dafdfd2579175a6ea9771`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **pypa--gh-action-pypi-publish/v1.13.0** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

In the 'Create Docker container action' step of action.yml, the GitHub Actions expression `${{ github.action_path }}` is directly interpolated inside a `run:` shell command string. Per security best practices, all `github.*` context values must be assigned to an environment variable via `env:` and then referenced as `$ENV_VAR` in the shell command, rather than being interpolated directly. A malicious value in `github.action_path` could allow shell command injection. The offending line is: `}} '${{ github.action_path }}/create-docker-action.py'`

Locations:

- `action.yml:121`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed script injection in the 'Create Docker container action' step of action.yml (line 121). Moved `${{ github.action_path }}` from the `run:` shell command into the step's `env:` block as `ACTION_PATH: ${{ github.action_path }}`, and updated the shell command to reference it as `"$ACTION_PATH/create-docker-action.py"` instead of `'${{ github.action_path }}/create-docker-action.py'`.

