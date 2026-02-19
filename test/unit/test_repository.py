from nukekit.core import AssetType, Repository


def test_repo_from_config(sample_config):
    repository = Repository.from_config(sample_config)
    assert repository


def test_repo_creation(tmp_path):
    repository = Repository(tmp_path / "repository", [a for a in AssetType])
    assert repository


def test_repo_folder_creation(sample_config):
    repository = Repository.from_config(sample_config)
    folder = repository.root / "Gizmo"
    assert folder.exists()
    assert folder.is_dir()


def test_repo_build_asset_path(sample_config, sample_asset):
    repository = Repository.from_config(sample_config)
    path = repository.get_asset_path(sample_asset)
    assert path == repository.root / "Gizmo" / "tool" / f"{sample_asset}.gizmo"


def test_repo_list_asset_directories(sample_config):
    repository = Repository.from_config(sample_config)
    assert repository.list_asset_directories("Gizmo") == []
