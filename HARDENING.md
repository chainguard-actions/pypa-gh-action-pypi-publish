<!-- markdownlint-disable -->

# Hardening Report: pypa--gh-action-pypi-publish/v1.13.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **pypa--gh-action-pypi-publish/v1.13.0** was hardened automatically. 5 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Multiple `uses:` references are pinned to mutable tags or branch names rather than full 40-character commit SHAs, making the workflow vulnerable to supply-chain attacks.

.github/workflows/build-and-push-docker-image.yml:
- `uses: re-actors/alls-green@release/v1` (branch ref, line 31)
- `uses: actions/checkout@v4` (tag ref, line 42)

.github/workflows/reusable-smoke-test.yml:
- `uses: actions/checkout@v4` (tag ref, line 46 in fail-fast job)
- `uses: actions/checkout@v4` (tag ref, line 80 in smoke-test job)

Locations:

- `.github/workflows/build-and-push-docker-image.yml:31`
- `.github/workflows/build-and-push-docker-image.yml:42`
- `.github/workflows/reusable-smoke-test.yml:46`
- `.github/workflows/reusable-smoke-test.yml:80`

### hardcoded-credentials (severity: high)

A literal hardcoded password value `abcd1234` is assigned to `devpi-password` in the top-level `env:` block of reusable-smoke-test.yml. Even though this is a test/devpi credential, it matches the hardcoded-credentials pattern (`password: abcd1234`) and should be stored as a secret reference instead of a plaintext literal.

Locations:

- `.github/workflows/reusable-smoke-test.yml:9`

### permissions (severity: medium)

reusable-smoke-test.yml has no top-level `permissions:` key and none of its three jobs (`legit-pr`, `fail-fast`, `smoke-test`) define job-level `permissions:` blocks. This means the workflow runs with the default (potentially broad) token permissions granted by the repository or organization settings.

Locations:

- `.github/workflows/reusable-smoke-test.yml:1`

### script-injection (severity: high)

Sub-rule (a): GitHub Actions expressions (`${{ ... }}`) are interpolated directly inside `run:` shell command strings, bypassing shell quoting and enabling script injection.

1. action.yml, 'Create Docker container action' step (line ~119): The run: block directly interpolates `${{ steps.pre-installed-python.outputs.python-path }}`, `${{ steps.new-python.outputs.python-path }}`, and `${{ github.action_path }}` as part of the shell command. An attacker-controlled or unexpected value in these expressions could inject arbitrary shell commands.
   Offending lines:
   ```
   ${{ steps.pre-installed-python.outputs.python-path == '' && steps.new-python.outputs.python-path || steps.pre-installed-python.outputs.python-path }} '${{ github.action_path }}/create-docker-action.py'
   ```

2. .github/workflows/build-and-push-docker-image.yml, 'Log in to GHCR' step (line 71): `echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u $GITHUB_ACTOR --password-stdin` — a `${{ }}` expression is interpolated directly in the run: block. The safe pattern is to use the env: block to pass the token as an environment variable.

Locations:

- `action.yml:119`
- `.github/workflows/build-and-push-docker-image.yml:71`

### github-env-injection (severity: high)

In the 'Build Docker image' step of build-and-push-docker-image.yml, the env var `DOCKER_TAG` is set from `${{ inputs.tag || github.ref_name }}` (attacker-controllable via `workflow_dispatch` input or branch/tag name). This value is used — without sanitization (`printf '%s' ... | tr -d '\n\r'`) — to construct `IMAGE`, `IMAGE_MAJOR`, `IMAGE_MAJOR_MINOR`, and `IMAGE_SHA` strings that are then written to `$GITHUB_ENV`. A newline-containing value in `inputs.tag` or `github.ref_name` could inject arbitrary environment variables into subsequent steps.

Offending writes (lines 53–56):
```
echo "IMAGE=$IMAGE" >> "$GITHUB_ENV"
echo "IMAGE_MAJOR=$IMAGE_MAJOR" >> "$GITHUB_ENV"
echo "IMAGE_MAJOR_MINOR=$IMAGE_MAJOR_MINOR" >> "$GITHUB_ENV"
echo "IMAGE_SHA=$IMAGE_SHA" >> "$GITHUB_ENV"
```
where `DOCKER_TAG` (and thus all IMAGE variables) derives from `${{ inputs.tag || github.ref_name }}` (line 68).

Locations:

- `.github/workflows/build-and-push-docker-image.yml:53`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, hardcoded-credentials, permissions, script-injection, github-env-injection

**Notes:**

Fixed all 5 findings across 3 files:

1. **unpinned-uses** (build-and-push-docker-image.yml lines 31, 42; reusable-smoke-test.yml lines 46, 80): Pinned re-actors/alls-green@release/v1 to SHA 05ac9388f0aebcb5727afa17fcccfecd6f8ec5fe and actions/checkout@v4 to SHA 11d5960a326750d5838078e36cf38b85af677262 in all 4 locations.

2. **hardcoded-credentials** (reusable-smoke-test.yml line 9): Replaced hardcoded `devpi-password: abcd1234` with `devpi-password: ${{ secrets.devpi-password }}` and declared the secret in the workflow_call secrets block.

3. **permissions** (reusable-smoke-test.yml): Added `permissions: {}` top-level block.

4. **script-injection** (action.yml line ~119; build-and-push-docker-image.yml line 71): Moved ${{ }} expressions out of run: blocks into env: blocks. In action.yml, PYTHON_PATH and ACTION_PATH env vars now hold the expressions; in build-and-push-docker-image.yml, GITHUB_TOKEN env var holds secrets.GITHUB_TOKEN.

5. **github-env-injection** (build-and-push-docker-image.yml line 53): Added `printf '%s' "$DOCKER_TAG" | tr -d '\n\r'` sanitization before using DOCKER_TAG to construct IMAGE variables written to $GITHUB_ENV.

