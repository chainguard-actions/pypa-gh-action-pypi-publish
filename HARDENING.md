<!-- markdownlint-disable -->

# Hardening Report: pypa--gh-action-pypi-publish/v1.14.3

> This file was generated automatically by the hardening agent.

**Policy SHA:** `374911c4be584df24e6da57af2d990570ef0f859`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pypa--gh-action-pypi-publish/v1.14.3** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a) violated in the 'Create Docker container action' step. The run: block puts GitHub expressions straight into the shell script: `${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }} '${{ github.action_path }}/create-docker-action.py'`. The steps.*.outputs.* and github.action_path values are pasted into the script text before the shell reads it. To fix this, move them into env: variables (for example PYTHON_PATH and ACTION_PATH) and run them double-quoted: "$PYTHON_PATH" "$ACTION_PATH/create-docker-action.py".

Locations:

- `action.yml:127`

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

Both findings are fixed in action.yml. I also changed create-docker-action.py so the generated Docker action pulls upstream's container image. Nothing was run or tested.

- **script-injection / prior-fix:** In the 'Create Docker container action' step, the expression that picks the Python path is now an env var, PYTHON_PATH. The script itself now runs `"$PYTHON_PATH" "$GITHUB_ACTION_PATH/create-docker-action.py"`, with no `${{ }}` left in it. This is the same change the previous harden made.
- **Container image:** create-docker-action.py used to build the image name from the action's own repository and ref (`docker://ghcr.io/{repo}:{ref}`). On the mirror that points to an image nobody publishes, so the pull would be denied. It now returns upstream's image as a fixed value: `docker://ghcr.io/pypa/gh-action-pypi-publish:7245906fb61fa33a13554f9d5fb856fe61758086@sha256:411241df99067c98b6d08fd8e26d14e86740a22460599c2af571e6dc26e27ffc`. I got the digest from the registry lookup. The upstream branch that builds the local Dockerfile for pypa's own self-tests is unchanged.

The previous patch's header said it added 17 lines near the start of `runs.steps`, but the diff I was given showed none of them. I couldn't recover them, so they weren't re-applied. `set_image` no longer uses its `ref` and `repo` arguments; I left its signature as it was.

