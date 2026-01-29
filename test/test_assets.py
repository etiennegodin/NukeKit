import pytest
from nukekit.core.assets import asset_factory, Gizmo, Script

def test_assets_create_gizmo():
    asset_path = '/home/etienne/projects/pipetd/NukeKit/examples/my_gizmo.gizmo'
    asset = asset_factory(asset_path)
    assert isinstance(asset, Gizmo)


def test_assets_wrong_file_type():
    
    asset_path = '/home/etienne/projects/pipetd/NukeKit/examples/my_gizmo.wrong_type'
    with pytest.raises(TypeError): # Catches any Exception type
        asset_factory(asset_path)

