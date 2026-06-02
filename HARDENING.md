# Hardening Report: pypa--gh-action-pypi-publish/v1.14.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `ff50f15e4b79bfbf764dafdfd2579175a6ea9771`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **pypa--gh-action-pypi-publish/v1.14.0** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

In the 'Create Docker container action' step of action.yml, the GitHub Actions expression `${{ github.action_path }}` is interpolated directly inside a `run:` shell command string. Per the security check rules, all `github.*` expressions are considered attacker-controlled and must be assigned to an environment variable via `env:` before being referenced in a `run:` block. The safe pattern would be to set `ACTION_PATH: ${{ github.action_path }}` in the step's `env:` block and then reference `$ACTION_PATH` in the shell command.

Locations:

- `action.yml:108`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed script injection in the 'Create Docker container action' step of action.yml. Moved `${{ github.action_path }}` from the `run:` shell command into the step's `env:` block as `ACTION_PATH: ${{ github.action_path }}`, and updated the shell command to reference it safely as `"${ACTION_PATH}/create-docker-action.py"` instead of `'${{ github.action_path }}/create-docker-action.py'`.

