import pytest
from nukekit.core import Asset, Gizmo
from nukekit.core.context import get_context


def test_assets_create_gizmo():
    context = get_context()
    asset_path = "/home/etienne/projects/pipetd/NukeKit/examples/my_gizmo.gizmo"
    asset = Asset.from_path(context, asset_path)
    print(type(asset))
    assert isinstance(asset, Gizmo)


def test_assets_wrong_file_type():
    context = get_context()
    asset_path = "/home/etienne/projects/pipetd/NukeKit/examples/my_gizmo.wrong_type"
    with pytest.raises(TypeError):  # Catches any Exception type
        Asset.from_path(context, asset_path)
