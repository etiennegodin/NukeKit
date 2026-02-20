import logging

import pytest
from nukekit.app import Dependencies
from nukekit.core import Asset, AssetType, Repository


@pytest.fixture
def sample_gizmo_path(tmp_path):
    asset_path = tmp_path / "tool_v0.1.0.gizmo"
    asset_path.write_text("Test")
    return asset_path


@pytest.fixture
def sample_config(tmp_path) -> dict:
    repo_root = tmp_path / "repository"
    return {
        "repository": {"root": repo_root, "subfolder": ["Gizmo", "Script"]},
        "user": {"nuke_dir": "~/.nuke"},
    }


@pytest.fixture
def sample_asset(sample_gizmo_path) -> Asset:
    return Asset.from_path(sample_gizmo_path)


@pytest.fixture
def sample_repo(tmp_path_factory) -> Repository:
    repo_dir = tmp_path_factory.mktemp("shared_repository")
    return Repository(repo_dir, list(AssetType))


@pytest.fixture
def sample_deps(sample_config) -> Dependencies:
    return Dependencies.create(sample_config, logger=logging.Logger)
