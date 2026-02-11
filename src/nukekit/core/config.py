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
        env_path = Path(os.getenv(cls.NUKEKIT_CONFIG_PATH))
        if env_path.exists():
            return Path(env_path)

        # Read from this package as fallback
        package_root = Path(__file__).parents[3]
        adjacent = package_root / "config" / "settings.yaml"
        if adjacent.exists():
            return adjacent

        raise FileNotFoundError(f"NukeKit could not find studio config.\n"
            f"  → Set the {cls.NUKEKIT_CONFIG_PATH} env var to your config path\n"
            f"  → Or place studio_settings.yaml in {package_root / 'config'}")

    @classmethod
    def load(cls) -> dict:
        path = cls.resolve()
        with open(path) as file:
            return yaml.safe_load(file)


class ConfigValidator:
    """Validate configuration against schema."""

    REQUIRED_KEYS = {
        'repository': ['root', 'subfolder'],
        'user': ['nuke_dir'],
    }

    @classmethod
    def validate(cls, config: dict) -> bool:
        """Validate config. Returns (is_valid, errors)."""
        warnings = []
        # Check required sections
        for section, keys in cls.REQUIRED_KEYS.items():
            if section not in config:
                logger.error(f"Missing required section in config: {section}")
                quit()
                continue

            for key in keys:
                if key not in config[section]:
                    logger.error(f"Missing required key in config: {section}.{key}")
                    quit()

        # Validate paths
        if 'repository' in config:
            root = Path(config['repository'].get('root', ''))
            if not root.is_absolute():
                warnings.append(f"Repository root must be absolute path: {root}")

        if len(warnings) == 0:
            return True
        [logger.warning(w) for w in warnings]
        return False
