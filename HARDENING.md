<!-- markdownlint-disable -->

# Hardening Report: pypa--gh-action-pypi-publish/v1.14.3

> This file was generated automatically by the hardening agent.

**Policy SHA:** `374911c4be584df24e6da57af2d990570ef0f859`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pypa--gh-action-pypi-publish/v1.14.3** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): the 'Create Docker container action' step's run: block puts GitHub Actions expressions straight into the shell script: `${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }} '${{ github.action_path }}/create-docker-action.py'`. Values from steps.*.outputs.* and github.action_path are substituted into the script text before the shell parses it. Move them into env: variables and use them double-quoted (for example "$PYTHON_PATH" "$GITHUB_ACTION_PATH/create-docker-action.py").

Locations:

- `action.yml:129`

### prior-fix (severity: high)

Carried forward from this version's previous harden, which fixed it; fix it again unless the code no longer has the problem. The previous harden changed action.yml without recording a finding for it, and this analysis reported nothing there. Re-apply its security changes unless the code no longer needs them. The previous patch:
```diff
diff --git a/action.yml b/action.yml
index f0b2c50..73444e3 100644
--- a/action.yml
+++ b/action.yml
@@ -92,6 +92,23 @@ branding:
 runs:
   using: composite
   steps:
   - name: Fail-fast in unsupported environments
     if: runner.os != 'Linux'
     run: |
@@ -120,18 +137,20 @@ runs:
     if: steps.pre-installed-python.outputs.python-path == ''
     id: new-python
     # yamllint disable-line rule:line-length
     uses: actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405  # v6.2.0
     with:
       python-version: 3.x
   - name: Create Docker container action
     run: |
       # Create Docker container action
-      ${{
-        steps.pre-installed-python.outputs.python-path == ''
-        && steps.new-python.outputs.python-path
-        || steps.pre-installed-python.outputs.python-path
-      }} '${{ github.action_path }}/create-docker-action.py'
+      "$PYTHON_PATH" "$GITHUB_ACTION_PATH/create-docker-action.py"
     env:
+      PYTHON_PATH: >-
+        ${{
+          steps.pre-installed-python.outputs.python-path == ''
+          && steps.new-python.outputs.python-path
+          || steps.pre-installed-python.outputs.python-path
+        }}
       # Set repo and ref from which to run Docker container action
       # to handle cases in which `github.action_` context is not set
       # https://github.com/actions/runner/issues/2473

```

Locations:

- `action.yml`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, prior-fix

**Notes:**

In the 'Create Docker container action' step, I moved the python-path expression into env as PYTHON_PATH. The script now runs "$PYTHON_PATH" "$GITHUB_ACTION_PATH/create-docker-action.py" instead of pasting github.action_path into it. This is the same change the previous harden made. That patch also seemed to add 17 lines near the top of runs.steps, but the diff never shows what they were, so I didn't add anything there. Nothing has been run to test this.

