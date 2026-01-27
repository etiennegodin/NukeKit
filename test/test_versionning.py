# tests/test_versioning.py
import pytest
from nukekit.core.versioning import Version

def test_version_comparison_gt():
    v1 = Version("1.2.0")
    v2 = Version("1.1.5")
    assert v1 > v2


def test_version_from_tuple():
    v = Version.from_tuple((1,2,3))
    assert v.major == 1
    assert v.minor == 2
    assert v.patch == 3

def test_version_parsing():
    v = Version("2.10.3")
    assert v.major == 2
    assert v.minor == 10
    assert v.patch == 3

def test_invalid_version():
    with pytest.raises(ValueError):
        Version("1.2")  # Missing patch