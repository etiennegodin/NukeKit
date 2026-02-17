from nukekit.core import Manifest


def test_manifest_empty():
    manifest = Manifest()
    manifest.data == {"Gizmo": {}, "Script": {}}


def test_manifest_from_dict():
    data = {"key": "value"}
    Manifest.from_dict(data)


def test_manifest_add_asset(sample_asset):
    manifest = Manifest()
    manifest.add_asset(sample_asset)
    # assert manifest.has_asset(sample_asset)


def test_manifest_has_asset(sample_asset):
    manifest = Manifest()
    manifest.add_asset(sample_asset)
    assert manifest.has_asset(sample_asset)


def test_manifest_get_asset(sample_asset):
    manifest = Manifest()
    manifest.add_asset(sample_asset)
    assert manifest.get_asset(sample_asset) == sample_asset


def test_manifest_len(sample_asset):
    manifest = Manifest()
    manifest.add_asset(sample_asset)
    assert len(manifest) == 1


def test_manifest_latest_asset_version(sample_asset):
    asset2 = sample_asset
    asset2.version.version_up("minor")
    manifest = Manifest()
    manifest.add_asset(sample_asset)
    manifest.add_asset(asset2)
    assert manifest.get_latest_asset_version(sample_asset) == asset2.version
