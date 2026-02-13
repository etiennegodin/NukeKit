from nukekit.core import Manifest, Repository


def test_repo_creation(sample_config):
    repo = Repository(sample_config)
    assert repo


def test_repo_folder_creation(sample_config):
    repo = Repository(sample_config)
    folder = repo.ROOT / "Gizmo"
    assert folder.exists()
    assert folder.is_dir()


def test_repo_add_manifest(tmp_path, sample_config):
    repo = Repository(sample_config)
    manifest = Manifest.from_json(tmp_path / "tmp.json")
    repo.add_manifest(manifest)
    assert repo.manifest == manifest


def test_repo_build_asset_path(sample_config, sample_asset):
    repo = Repository(sample_config)
    path = repo.build_asset_path(sample_asset)
    assert path == repo.ROOT / "Gizmo" / "tool" / f"{sample_asset}.gizmo"
