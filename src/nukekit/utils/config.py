import logging
import os
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


class ConfigLoader:
    """
    Resolve and load config for this session
    """

    NUKEKIT_CONFIG_PATH = "NUKEKIT_CONFIG_PATH"

    @classmethod
    def resolve(cls) -> Path:
        # Read from .env
        config_path = os.getenv(cls.NUKEKIT_CONFIG_PATH)
        if config_path is not None:
            env_path = Path(config_path)
            if env_path.exists():
                return Path(env_path)

        # Read from this package as fallback
        package_root = Path(__file__).parents[3]
        adjacent = package_root / "config" / "settings.yaml"
        if adjacent.exists():
            return adjacent

        raise FileNotFoundError(
            f"NukeKit could not find studio config.\n"
            f"  → Set the {cls.NUKEKIT_CONFIG_PATH} env var to your config path\n"
            f"  → Or place studio_settings.yaml in {package_root / 'config'}"
        )

    @classmethod
    def load(cls) -> dict:
        path = cls.resolve()
        with open(path) as file:
            return yaml.safe_load(file)


class ConfigValidator:
    """Validate configuration against schema."""

    REQUIRED_KEYS = {
        "repository": ["root", "subfolder"],
        "user": ["nuke_dir"],
    }

    @classmethod
    def validate(cls, config: dict) -> None:
        """Validate config. Returns (is_valid, errors)."""
        # Check required sections
        for section, keys in cls.REQUIRED_KEYS.items():
            if section not in config:
                raise KeyError(f"Missing required section in config: {section}")

            for key in keys:
                if key not in config[section]:
                    raise KeyError(f"Missing required key in config: {section}.{key}")

        # Validate paths
        if "repository" in config:
            root = Path(config["repository"].get("root", ""))
            if not root.is_absolute():
                logger.warning(f"Repository root must be absolute path: {root}")
