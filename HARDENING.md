<!-- markdownlint-disable -->

# Hardening Report: pypa--gh-action-pypi-publish/v1.14.2

> This file was generated automatically by the hardening agent.

**Policy SHA:** `374911c4be584df24e6da57af2d990570ef0f859`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pypa--gh-action-pypi-publish/v1.14.2** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a), direct expression interpolation. The run: block of the 'Create Docker container action' step puts GitHub Actions expressions straight into the shell script: `${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }} '${{ github.action_path }}/create-docker-action.py'`. Both steps.*.outputs.* and github.action_path are filled in by the template before the shell runs, so any shell metacharacters in them get executed. Fix: pass them through env: variables (for example PYTHON_PATH and ACTION_PATH) and call them double-quoted as "$PYTHON_PATH" "$ACTION_PATH/create-docker-action.py". The runner already provides $GITHUB_ACTION_PATH for the second one.

Locations:

- `action.yml:128`

### prior-fix (severity: high)

Carried forward from this version's previous harden, which fixed it; fix it again unless the code no longer has the problem. The previous harden changed action.yml without recording a finding for it, and this analysis reported nothing there. Re-apply its security changes unless the code no longer needs them. The previous patch:
```diff
diff --git a/action.yml b/action.yml
index f0b2c50..4b13f5d 100644
--- a/action.yml
+++ b/action.yml
@@ -1,4 +1,3 @@
----
 name: pypi-publish
 description: Upload Python distribution packages to PyPI
 inputs:
@@ -9,81 +8,68 @@ inputs:
   password:
     description: Password for your PyPI user or an access token
     required: false
-  repository-url:  # Canonical alias for `repository_url`
+  repository-url: # Canonical alias for `repository_url`
     description: The repository URL to use
     required: false
-  repository_url:  # DEPRECATED ALIAS; TODO: Remove in v3+
+  repository_url: # DEPRECATED ALIAS; TODO: Remove in v3+
     description: >-
-      [DEPRECATED]
-      The repository URL to use
+      [DEPRECATED] The repository URL to use
     deprecationMessage: >-
-      The inputs have been normalized to use kebab-case.
-      Use `repository-url` instead.
+      The inputs have been normalized to use kebab-case. Use `repository-url` instead.
     required: false
     default: https://upload.pypi.org/legacy/
-  packages-dir:  # Canonical alias for `packages_dir`
+  packages-dir: # Canonical alias for `packages_dir`
     description: The target directory for distribution
     required: false
     # default: dist  # TODO: uncomment once alias removed
-  packages_dir:  # DEPRECATED ALIAS; TODO: Remove in v3+
+  packages_dir: # DEPRECATED ALIAS; TODO: Remove in v3+
     description: >-
-      [DEPRECATED]
-      The target directory for distribution
+      [DEPRECATED] The target directory for distribution
     deprecationMessage: >-
-      The inputs have been normalized to use kebab-case.
-      Use `packages-dir` instead.
+      The inputs have been normalized to use kebab-case. Use `packages-dir` instead.
     required: false
     default: dist
-  verify-metadata:  # Canonical alias for `verify_metadata`
+  verify-metadata: # Canonical alias for `verify_metadata`
     description: Check metadata before uploading
     required: false
     # default: 'true'  # TODO: uncomment once alias removed
-  verify_metadata:  # DEPRECATED ALIAS; TODO: Remove in v3+
+  verify_metadata: # DEPRECATED ALIAS; TODO: Remove in v3+
     description: >-
-      [DEPRECATED]
-      Check metadata before uploading
+      [DEPRECATED] Check metadata before uploading
     deprecationMessage: >-
-      The inputs have been normalized to use kebab-case.
-      Use `verify-metadata` instead.
+      The inputs have been normalized to use kebab-case. Use `verify-metadata` instead.
     required: false
     default: 'true'
-  skip-existing:  # Canonical alias for `skip_existing`
+  skip-existing: # Canonical alias for `skip_existing`
     description: >-
-      Do not fail if a Python package distribution
-      exists in the target package index
+      Do not fail if a Python package distribution exists in the target package index
     required: false
     # default: 'false'  # TODO: uncomment once alias removed
-  skip_existing:  # DEPRECATED ALIAS; TODO: Remove in v3+
+  skip_existing: # DEPRECATED ALIAS; TODO: Remove in v3+
     description: >-
-      [DEPRECATED]
-      Do not fail if a Python package distribution
-      exists in the target package index
+      [DEPRECATED] Do not fail if a Python package distribution exists in the target package index
     deprecationMessage: >-
-      The inputs have been normalized to use kebab-case.
-      Use `skip-existing` instead.
+      The inputs have been normalized to use kebab-case. Use `skip-existing` instead.
     required: false
     default: 'false'
   verbose:
     description: Show verbose output.
     required: false
     default: 'true'
-  print-hash:  # Canonical alias for `print_hash`
+  print-hash: # Canonical alias for `print_hash`
     description: Show hash values of files to be uploaded
     required: false
     # default: 'false'  # TODO: uncomment once alias removed
-  print_hash:  # DEPRECATED ALIAS; TODO: Remove in v3+
+  print_hash: # DEPRECATED ALIAS; TODO: Remove in v3+
     description: >-
-      [DEPRECATED]
-      Show hash values of files to be uploaded
+      [DEPRE
... (truncated)
```

Locations:

- `action.yml`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, prior-fix

**Notes:**

In the 'Create Docker container action' step of action.yml, the Python path expression now sits in a new PYTHON_PATH entry under env: with the same fallback logic. The command is now "$PYTHON_PATH" "$GITHUB_ACTION_PATH/create-docker-action.py", so github.action_path is no longer pasted into the script. No other script uses a PYTHON_PATH variable. The earlier patch was cut off; the visible part only changed formatting (YAML re-wrapping, dropping '---'), so those edits were not redone, and its security change is assumed to be the same injection fix applied here. Not run or re-analysed.

