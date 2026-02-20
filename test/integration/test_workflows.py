from pathlib import Path

import pytest
from nukekit.core import Asset, Repository
from nukekit.workflows import publish_workflow


@pytest.mark.dependency(name="publish")
def test_publish_asset(sample_asset: Asset, sample_deps):
    publish_workflow.execute(sample_deps, interactive=False, asset=sample_asset)


@pytest.mark.dependency(depends=["publish"])
def test_install_asset_from_repo(
    tmp_path: Path, sample_asset: Asset, sample_repo: Repository
):
    pass
