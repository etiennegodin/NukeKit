import pytest
from nukekit.core import Manifest


def test_manifest_creation_error():
    with pytest.raises(TypeError):
        Manifest()


def test_new_manifest(tmp_path):
    file_path = tmp_path / "temp.json"
    m = Manifest.from_json(file_path)
    assert m.data == {"Gizmo": {}, "Script": {}}


def test_manifest_local_state(tmp_path):
    local = tmp_path / "local"
    local.mkdir()
    manifest = Manifest.from_local_state(local)
    assert manifest.ROOT == local / "local_state.json"
