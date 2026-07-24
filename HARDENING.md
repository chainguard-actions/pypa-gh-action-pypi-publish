<!-- markdownlint-disable -->

# Hardening Report: pypa--gh-action-pypi-publish/v1.14.1

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pypa--gh-action-pypi-publish/v1.14.1** was hardened automatically. 5 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### hardcoded-credentials (severity: high)

A literal hardcoded password value `abcd1234` is assigned to `devpi-password` in the workflow-level `env:` block. Although this appears to be a test credential for a local devpi instance, it is a non-expression literal value matching the hardcoded-credentials pattern and must not appear in workflow files.

Locations:

- `.github/workflows/reusable-smoke-test.yml:9`

### unpinned-uses (severity: high)

Multiple `uses:` references are pinned to mutable tags or branch names instead of immutable 40-character commit SHAs, making the workflow vulnerable to supply-chain attacks if the referenced tag or branch is moved or compromised.

Failing references in build-and-push-docker-image.yml:
- `re-actors/alls-green@release/v1` (branch ref, line 34)
- `actions/checkout@v4` (tag ref, line 44)

Failing references in reusable-smoke-test.yml:
- `actions/checkout@v4` (tag ref, line 44)
- `actions/checkout@v4` (tag ref, line 76)

Locations:

- `.github/workflows/build-and-push-docker-image.yml:34`
- `.github/workflows/build-and-push-docker-image.yml:44`
- `.github/workflows/reusable-smoke-test.yml:44`
- `.github/workflows/reusable-smoke-test.yml:76`

### missing-permissions (severity: medium)

`reusable-smoke-test.yml` has no top-level `permissions:` key, and none of its jobs (`legit-pr`, `fail-fast`, `smoke-test`) define a job-level `permissions:` block. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be overly broad.

Locations:

- `.github/workflows/reusable-smoke-test.yml:1`

### script-injection (severity: high)

GitHub Actions expressions (`${{ ... }}`) are interpolated directly inside `run:` shell command strings, which allows the expression value to be parsed as shell syntax before the shell ever sees it.

(a) In `action.yml` ("Create Docker container action" step): `${{ steps.pre-installed-python.outputs.python-path }}` and `${{ github.action_path }}` are interpolated directly into the shell command. An attacker who can influence `github.action_path` or the step output could inject arbitrary shell commands.

(a) In `build-and-push-docker-image.yml` ("Log in to GHCR" step, line 67): `echo ${{ secrets.GITHUB_TOKEN }} | docker login ...` interpolates the token expression directly into the shell command string. Even though `secrets.GITHUB_TOKEN` is GitHub-controlled, any `${{ ... }}` inside a `run:` block is a script-injection finding — the value should be passed via an `env:` variable and referenced as `$ENV_VAR` instead.

Locations:

- `action.yml:113`
- `.github/workflows/build-and-push-docker-image.yml:67`

### github-env-injection (severity: high)

In the "Build Docker image" step of `build-and-push-docker-image.yml`, the env var `DOCKER_TAG` is sourced from `${{ inputs.tag || github.ref_name }}` (an attacker-controllable value via `workflow_dispatch` input or branch/tag name). The script then derives `IMAGE`, `IMAGE_MAJOR`, `IMAGE_MAJOR_MINOR`, and `IMAGE_SHA` from `DOCKER_TAG` and writes them to `$GITHUB_ENV` without the required sanitization step (`printf '%s' "$VAR" | tr -d '\n\r'`). A newline injected into `inputs.tag` or `github.ref_name` could allow an attacker to inject arbitrary environment variable assignments into subsequent steps.

Locations:

- `.github/workflows/build-and-push-docker-image.yml:57`

## Iteration Notes

### Iteration 1

**Fixes applied:** hardcoded-credentials, unpinned-uses, missing-permissions, script-injection, github-env-injection

**Notes:**

Fixed all 5 findings:
1. hardcoded-credentials: Replaced literal 'abcd1234' in reusable-smoke-test.yml env block with ${{ secrets.DEVPI_PASSWORD }}.
2. unpinned-uses: Pinned re-actors/alls-green@release/v1 to SHA 05ac9388f0aebcb5727afa17fcccfecd6f8ec5fe and all three actions/checkout@v4 references to SHA 11d5960a326750d5838078e36cf38b85af677262.
3. missing-permissions: Added 'permissions: {}' top-level block to reusable-smoke-test.yml.
4. script-injection: In action.yml, moved python-path expression and github.action_path into PYTHON_PATH/ACTION_PATH env vars. In build-and-push-docker-image.yml, moved secrets.GITHUB_TOKEN into GHCR_TOKEN env var.
5. github-env-injection: In build-and-push-docker-image.yml Build Docker image step, sanitized all DOCKER_TAG-derived values with printf+tr before writing to GITHUB_ENV.

### Iteration 2

**Fixes applied:** script-injection

**Notes:**

Fixed two script-injection findings in .github/workflows/build-and-push-docker-image.yml by double-quoting all unquoted variable expansions of attacker-controllable data:
1. 'Build Docker image' step: Added double quotes around $IMAGE in --cache-from and --tag arguments, and around all arguments to docker tag commands.
2. 'Push Docker image to GHCR' step: Added double quotes around $IMAGE, $IMAGE_MAJOR, $IMAGE_MAJOR_MINOR, and $IMAGE_SHA in all docker push commands.
This prevents shell word-splitting and glob expansion on values derived from the attacker-controllable `inputs.tag || github.ref_name` expression.

