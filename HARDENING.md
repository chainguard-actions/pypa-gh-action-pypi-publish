# Hardening Report: pypa--gh-action-pypi-publish/v1.13.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `ff50f15e4b79bfbf764dafdfd2579175a6ea9771`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **pypa--gh-action-pypi-publish/v1.13.0** was hardened automatically. 0 finding(s) were identified and resolved across 1 iteration(s).

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

Fixed script injection in action.yml at the 'Create Docker container action' step (line 136). Moved `${{ github.action_path }}` from the run: shell command into the env: block as `ACTION_PATH: ${{ github.action_path }}`, and updated the shell command to reference it as `"$ACTION_PATH/create-docker-action.py"` instead of `'${{ github.action_path }}/create-docker-action.py'`.

