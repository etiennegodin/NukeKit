import pytest
from nukekit.core import Asset, AssetType


def test_assets_create_gizmo(tmp_path):
    asset_path = tmp_path / "my_gizmo.gizmo"
    asset = Asset.from_path(asset_path)
    assert asset.type == AssetType.GIZMO


def test_assets_create_script(tmp_path):
    asset_path = tmp_path / "my_gizmo.nk"
    asset = Asset.from_path(asset_path)
    assert asset.type == AssetType.SCRIPT


def test_assets_wrong_file_type(tmp_path):
    asset_path = tmp_path / "my_gizmo.wrong_type"
    with pytest.raises(TypeError):  # Catches any Exception type
        Asset.from_path(asset_path)


def test_asset_to_dict(sample_gizmo_path):
    assert isinstance(Asset.from_path(sample_gizmo_path).to_dict(), dict)


def test_asset_no_version(tmp_path):
    assert Asset.from_path(tmp_path / "asset.gizmo")


def test_asset_same(sample_gizmo_path):
    a1 = Asset.from_path(sample_gizmo_path)
    a2 = Asset.from_path(sample_gizmo_path)
    assert a1 == a2
