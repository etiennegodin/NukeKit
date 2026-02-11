import pytest


@pytest.fixture
def sample_asset(tmp_path):
    asset = tmp_path / "asset"
    asset.mkdir()
    (asset / "tool.gizmo").write_text("dummy")
    return asset
