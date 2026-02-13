import pytest
from nukekit.core import ConfigLoader, ConfigValidator


def test_read_config(tmp_path):
    config = ConfigLoader().load()
    assert config


def test_validate_config(sample_config):
    ConfigValidator.validate(sample_config)


def test_wrong_config():
    config = {}
    with pytest.raises(KeyError):  # Catches any Exception type
        ConfigValidator.validate(config)
