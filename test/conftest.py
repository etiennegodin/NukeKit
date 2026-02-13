import pytest
from nukekit.core import Asset, Manifest, Repository, publisher


@pytest.fixture
def sample_gizmo_path(tmp_path):
    asset_path = tmp_path / "tool_v0.1.0.gizmo"
    asset_path.write_text("Test")
    return asset_path


@pytest.fixture
def sample_config(tmp_path) -> dict:
    repo_root = tmp_path / "repo"
    return {
        "repository": {"root": repo_root, "subfolder": ["Gizmo", "Script"]},
        "user": {"nuke_dir": "~/.nuke"},
    }


@pytest.fixture
def sample_asset(sample_gizmo_path):
    asset = Asset.from_path(sample_gizmo_path)
    return asset


@pytest.fixture
def sample_empty_repo(sample_config):
    repo = Repository(sample_config)
    manifest = Manifest.from_json(repo.MANIFEST_PATH)
    repo.add_manifest(manifest)
    return repo


@pytest.fixture
def sample_repo(sample_empty_repo, sample_asset):
    publisher.publish_asset_to_repo(sample_empty_repo, sample_asset)
    return sample_empty_repo
