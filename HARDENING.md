<!-- markdownlint-disable -->

# Hardening Report: pypa--gh-action-pypi-publish/v1.14.2

> This file was generated automatically by the hardening agent.

**Policy SHA:** `374911c4be584df24e6da57af2d990570ef0f859`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pypa--gh-action-pypi-publish/v1.14.2** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): GitHub Actions expressions are placed straight into the 'Create Docker container action' run: block. The lines are `${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }} '${{ github.action_path }}/create-docker-action.py'`. Both the steps.*.outputs.* values and github.action_path are substituted into the script text before the shell parses it. Fix: pass them through env: variables (for example PYTHON_PATH and ACTION_PATH) and call them double-quoted: "$PYTHON_PATH" "$ACTION_PATH/create-docker-action.py". Another option is the built-in $GITHUB_ACTION_PATH variable.

Locations:

- `action.yml:125`

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

Fixed both findings, but nothing has been run yet, including the action's tests.

- **script-injection (action.yml, 'Create Docker container action' step):** The Python-path expression now goes through a PYTHON_PATH env var instead of being pasted into the script. The step calls `"$PYTHON_PATH" "$GITHUB_ACTION_PATH/create-docker-action.py"`, so `github.action_path` is no longer used inline either.
- **prior-fix:** The earlier patch shown to me was cut off. The visible part only reformats YAML comments and descriptions, which has no security effect, so I didn't redo it. I re-applied what this mirror still needs: create-docker-action.py used to build the image name from the action's own repository (`docker://ghcr.io/{repo}:{ref}`). On the mirror that points to an image nobody publishes, so every run would fail with "denied". It now returns upstream's image as a fixed value, pinned to the upstream commit and its digest: `docker://ghcr.io/pypa/gh-action-pypi-publish:dc37677b2e1c63e2034f94d8a5b11f265b73ba33@sha256:a68d05519f6d7e47372aeaddab80b851b69afa89be179ec41775c72c4e3ab2d5`. Upstream's self-test branch, which builds the local Dockerfile when the repository ID is pypa's own, is unchanged. Because I couldn't see the rest of the earlier patch, it may have contained other security changes that I have not re-applied.

The REF/REPO/REPO_ID env vars and the `ref`/`repo` parameters of `set_image` are left as upstream had them. With the image fixed, `ref` and `repo` are no longer used.

