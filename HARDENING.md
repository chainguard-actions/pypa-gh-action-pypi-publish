<!-- markdownlint-disable -->

# Hardening Report: pypa--gh-action-pypi-publish/v1.13.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pypa--gh-action-pypi-publish/v1.13.0** was hardened automatically. 1 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): the run: block in step 'Create Docker container action' puts GitHub Actions expressions straight into the shell command: `${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }} '${{ github.action_path }}/create-docker-action.py'`. The YAML template is filled in before the shell parses the line, so these values are never safely quoted. Move them into env: variables (e.g. PYTHON_PATH, ACTION_PATH) and reference them in the script as "$PYTHON_PATH" "$ACTION_PATH/create-docker-action.py".

Locations:

- `action.yml:122`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection

**Notes:**

I moved the two expressions in the 'Create Docker container action' step of action.yml out of the run: line and into the step's env: block. The step now runs: "$PYTHON_PATH" "$ACTION_PATH/create-docker-action.py".

- PYTHON_PATH holds the same expression as before: the pre-installed Python path, or the setup-python path if none was found.
- ACTION_PATH holds github.action_path.

The step runs under shell: bash, so the "$VAR" syntax is right. The new names don't clash with the variables create-docker-action.py reads (REF, REPO, REPO_ID). I haven't run the action or re-run the analysis to confirm the finding is gone.

