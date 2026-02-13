import pytest
from nukekit.core import Manifest


def test_manifest_creation_error():
    with pytest.raises(TypeError):
        Manifest()


def test_new_manifest(tmp_path):
    file_path = tmp_path / "temp.json"
    m = Manifest.from_json(file_path)
    assert m.data == {"Gizmo": {}, "Script": {}}
