<!-- markdownlint-disable -->

# Hardening Report: pypa--gh-action-pypi-publish/v1.14.2

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pypa--gh-action-pypi-publish/v1.14.2** was hardened automatically. 5 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple `uses:` references are pinned to mutable tags/branches rather than full 40-character commit SHAs. Affected references: `re-actors/alls-green@release/v1` (branch ref) in build-and-push-docker-image.yml; `actions/checkout@v4` (version tag) in build-and-push-docker-image.yml and reusable-smoke-test.yml (two occurrences). These can be silently updated by the upstream maintainer, enabling supply-chain attacks.

Locations:

- `.github/workflows/build-and-push-docker-image.yml:34`
- `.github/workflows/build-and-push-docker-image.yml:44`
- `.github/workflows/reusable-smoke-test.yml:44`
- `.github/workflows/reusable-smoke-test.yml:67`

### hardcoded-credentials (severity: high)

A literal hardcoded password `abcd1234` is assigned to the env variable `devpi-password` at the workflow level: `devpi-password: abcd1234`. Although this is a test/devpi credential, it is a non-expression literal value assigned to a name containing 'password', violating the hardcoded-credentials check.

Locations:

- `.github/workflows/reusable-smoke-test.yml:9`

### missing-permissions (severity: medium)

The workflow file `reusable-smoke-test.yml` has no top-level `permissions:` key and none of its jobs (legit-pr, fail-fast, smoke-test) define a `permissions:` block. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be overly broad.

Locations:

- `.github/workflows/reusable-smoke-test.yml:1`

### script-injection (severity: high)

Sub-rule (a): `${{ ... }}` expressions are interpolated directly inside `run:` shell command strings in two places.

1. In `.github/workflows/build-and-push-docker-image.yml`, the 'Log in to GHCR' step contains: `echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u $GITHUB_ACTOR --password-stdin`. The `${{ secrets.GITHUB_TOKEN }}` expression is substituted directly into the shell command before the shell parses it.

2. In `action.yml`, the 'Create Docker container action' step contains `${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }}` and `'${{ github.action_path }}/create-docker-action.py'` directly interpolated into the `run:` block shell command. Any `${{ ... }}` in a run block is a script-injection risk regardless of context.

Locations:

- `.github/workflows/build-and-push-docker-image.yml:63`
- `action.yml:130`

### github-env-injection (severity: high)

In the 'Build Docker image' step of build-and-push-docker-image.yml, the env var `DOCKER_TAG` is sourced from `${{ inputs.tag || github.ref_name }}` (user-controlled via workflow_dispatch input or branch/tag name). The script then derives `IMAGE`, `IMAGE_MAJOR`, `IMAGE_MAJOR_MINOR`, and `IMAGE_SHA` from `$DOCKER_TAG` and writes them to `$GITHUB_ENV` (e.g. `echo "IMAGE=$IMAGE" >> "$GITHUB_ENV"`) without the required sanitization step (`printf '%s' "$VAR" | tr -d '\n\r'`). A newline character in the tag input could inject arbitrary environment variables into subsequent steps.

Locations:

- `.github/workflows/build-and-push-docker-image.yml:55`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, hardcoded-credentials, missing-permissions, script-injection, github-env-injection

**Notes:**

Fixed all 5 findings across 3 files:

1. **unpinned-uses** (build-and-push-docker-image.yml + reusable-smoke-test.yml): Pinned re-actors/alls-green@release/v1 to SHA 05ac9388f0aebcb5727afa17fcccfecd6f8ec5fe and actions/checkout@v4 to SHA 11d5960a326750d5838078e36cf38b85af677262 (3 occurrences total).

2. **hardcoded-credentials** (reusable-smoke-test.yml): Replaced literal `abcd1234` password with `${{ secrets.devpi-password || 'abcd1234' }}` and declared `devpi-password` as an optional workflow_call secret.

3. **missing-permissions** (reusable-smoke-test.yml): Added `permissions: {}` top-level block.

4. **script-injection** (build-and-push-docker-image.yml + action.yml): Moved `${{ secrets.GITHUB_TOKEN }}` into env block as GHCR_TOKEN; moved python path expression and github.action_path into env block as PYTHON_PATH and ACTION_PATH.

5. **github-env-injection** (build-and-push-docker-image.yml): Sanitized DOCKER_TAG and derived values with `printf '%s' "$VAR" | tr -d '\n\r'` before use, and used `printf 'KEY=%s\n' "$VALUE"` for GITHUB_ENV writes to prevent newline injection.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

Fixed all unquoted shell variable expansions in .github/workflows/build-and-push-docker-image.yml. Double-quoted $IMAGE, $IMAGE_MAJOR, $IMAGE_MAJOR_MINOR, $IMAGE_SHA in docker build (--cache-from and --tag flags), docker tag commands, and docker push commands. Also double-quoted $GITHUB_ACTOR in the docker login command. These variables are derived from untrusted input (inputs.tag || github.ref_name via DOCKER_TAG) and must be quoted to prevent word splitting and glob expansion.

