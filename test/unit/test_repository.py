from nukekit.core import AssetType, Repository


def test_repo_from_config(sample_config):
    repo = Repository.from_config(sample_config)
    assert repo


def test_repo_creation(tmp_path):
    repo = Repository(tmp_path / "repo", [a for a in AssetType])
    assert repo


def test_repo_folder_creation(sample_config):
    repo = Repository.from_config(sample_config)
    folder = repo.root / "Gizmo"
    assert folder.exists()
    assert folder.is_dir()


def test_repo_build_asset_path(sample_config, sample_asset):
    repo = Repository.from_config(sample_config)
    path = repo.get_asset_path(sample_asset)
    assert path == repo.root / "Gizmo" / "tool" / f"{sample_asset}.gizmo"


def test_repo_list_asset_directories(sample_config):
    repo = Repository.from_config(sample_config)
    assert repo.list_asset_directories("Gizmo") == []
