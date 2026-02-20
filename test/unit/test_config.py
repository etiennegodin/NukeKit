from nukekit.core import ConfigLoader


def test_read_config(tmp_path):
    config = ConfigLoader().load()
    assert config
