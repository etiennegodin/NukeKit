import pytest


@pytest.fixture
def sample_gizmo_path(tmp_path):
    asset = tmp_path / "tool_v0.1.0.gizmo"
    asset.write_text("Test")
    return asset


@pytest.fixture
def sample_config(tmp_path) -> dict:
    return {"repository": {"root": tmp_path, "subfolder": ["Gizmo", "Script"]}}
