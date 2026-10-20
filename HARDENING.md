<!-- markdownlint-disable -->

# Hardening Report: pypa--gh-action-pypi-publish/v1.14.3

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pypa--gh-action-pypi-publish/v1.14.3** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): the 'Create Docker container action' step puts GitHub expressions straight into its run: script. The lines are `${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }} '${{ github.action_path }}/create-docker-action.py'`. The steps.*.outputs.* and github.action_path values are pasted into the script before the shell runs it. They should be passed in through env: variables and expanded with double quotes, for example "$PYTHON_PATH" "$GITHUB_ACTION_PATH/create-docker-action.py".

Locations:

- `action.yml:129`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

In the 'Create Docker container action' step, the Python-path expression now lives in env as PYTHON_PATH. The script runs "$PYTHON_PATH" "$GITHUB_ACTION_PATH/create-docker-action.py" instead of pasting in steps outputs and github.action_path. The existing REF/REPO/REPO_ID env entries are unchanged, and the shell is still bash.

