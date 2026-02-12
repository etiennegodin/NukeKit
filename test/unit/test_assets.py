import pytest
from nukekit.core import Asset, AssetType
from nukekit.workflows import get_context


def test_assets_create_gizmo():
    context = get_context()
    asset_path = "/home/etienne/projects/pipetd/NukeKit/examples/my_gizmo.gizmo"
    asset = Asset.from_path(context, asset_path)
    assert asset.type == AssetType.GIZMO


def test_assets_create_script():
    context = get_context()
    asset_path = "/home/etienne/projects/pipetd/NukeKit/examples/my_gizmo.nk"
    asset = Asset.from_path(context, asset_path)
    assert asset.type == AssetType.SCRIPT


def test_assets_wrong_file_type():
    context = get_context()
    asset_path = "/home/etienne/projects/pipetd/NukeKit/examples/my_gizmo.wrong_type"
    with pytest.raises(TypeError):  # Catches any Exception type
        Asset.from_path(context, asset_path)
