# tests/test_versioning.py
import pytest
from nukekit.core.versioning import Version

def test_version_comparison_gt():
    v1 = Version("1.2.0")
    v2 = Version("1.1.5")
    assert v1 > v2

def test_version_up_major():
    v1 = Version("1.1.13")
    v1.version_up('major')

    assert v1.major == 2
    assert v1.minor == 1
    assert v1.patch == 0

def test_version_up_minor():
    v1 = Version("1.1.13")
    v1.version_up('minor')

    assert v1.major == 1
    assert v1.minor == 2 
    assert v1.patch == 0

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

def test_version_invalid():
    with pytest.raises(ValueError):
        Version("1.2")  # Missing patch

def test_version_dict_hash():
    version= Version("0.1.0")
    value = "my_version"
    d = {version:value}
    assert d[version] == value