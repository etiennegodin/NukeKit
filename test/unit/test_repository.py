from nukekit.core import Asset, Manifest, Repository


def test_repo_creation(sample_config):
    repo = Repository(sample_config)
    assert repo


def test_repo_add_manifest(tmp_path, sample_config):
    repo = Repository(sample_config)
    manifest = Manifest.from_json(tmp_path / "tmp.json")
    repo.add_manifest(manifest)
    assert repo.manifest == manifest


def test_asset_no_version(tmp_path):
    assert Asset.from_path(tmp_path / "asset.gizmo")


def test_asset_same(sample_gizmo_path):
    a1 = Asset.from_path(sample_gizmo_path)
    a2 = Asset.from_path(sample_gizmo_path)
    assert a1 == a2
