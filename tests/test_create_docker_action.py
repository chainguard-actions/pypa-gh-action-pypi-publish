import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

HELPER = pathlib.Path(__file__).resolve().parents[1] / 'create-docker-action.py'
DOCKERFILE = str(HELPER.with_name('Dockerfile'))
CHAINGUARD_REPO = 'chainguard-actions/pypa-gh-action-pypi-publish'
UPSTREAM_REPO = 'pypa/gh-action-pypi-publish'
PIN = '3281eae6a06d4b96e24616f7821380f05fa50296'


class CreateDockerActionTest(unittest.TestCase):
    def generated_image(
        self,
        repo: str,
        ref: str,
        repo_id: str = '123456789',
        helper: pathlib.Path = HELPER,
    ) -> str:
        environment = {**os.environ, 'REPO': repo, 'REF': ref, 'REPO_ID': repo_id}
        with tempfile.TemporaryDirectory() as workspace:
            subprocess.run(
                [sys.executable, str(helper)],
                cwd=workspace,
                env=environment,
                check=True,
                capture_output=True,
            )
            generated = pathlib.Path(workspace) / (
                '.github/.tmp/.generated-actions/'
                'run-pypi-publish-in-docker-container/action.yml'
            )
            return str(json.loads(generated.read_text())['runs']['image'])

    def test_chainguard_uses_bundled_dockerfile(self) -> None:
        for ref in (PIN, 'v1.14.3', 'release/v1'):
            with self.subTest(ref=ref):
                assert self.generated_image(CHAINGUARD_REPO, ref) == DOCKERFILE
        assert pathlib.Path(DOCKERFILE).is_file()

    def test_chainguard_name_case_is_ignored(self) -> None:
        assert self.generated_image(CHAINGUARD_REPO.upper(), PIN) == DOCKERFILE

    def test_action_path_with_spaces(self) -> None:
        with tempfile.TemporaryDirectory(prefix='action checkout ') as checkout:
            helper = pathlib.Path(checkout).resolve() / HELPER.name
            shutil.copyfile(HELPER, helper)
            shutil.copyfile(DOCKERFILE, helper.with_name('Dockerfile'))
            image = self.generated_image(CHAINGUARD_REPO, PIN, helper=helper)
            assert image == str(helper.with_name('Dockerfile'))

    def test_upstream_consumers_keep_prebuilt_images(self) -> None:
        for ref in (PIN, 'release/v1'):
            with self.subTest(ref=ref):
                expected = f'docker://ghcr.io/{UPSTREAM_REPO}:{ref.replace("/", "-")}'
                assert self.generated_image(UPSTREAM_REPO, ref) == expected

    def test_upstream_self_test_keeps_bundled_build(self) -> None:
        assert self.generated_image(UPSTREAM_REPO, PIN, '178055147') == DOCKERFILE

    def test_other_forks_keep_prebuilt_images(self) -> None:
        image = self.generated_image('example/pypi-publish', 'release/v1')
        assert image == 'docker://ghcr.io/example/pypi-publish:release-v1'
