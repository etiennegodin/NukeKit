import os
import yaml
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ConfigLoader:
    """
    Resolve and load config for this session
    """

    ENV_VAR = "NUKEKIT_CONFIG_PATH"

    @classmethod
    def resolve(cls)->Path:
        env_path = Path(os.getenv(cls.ENV_VAR))
        if env_path.exists():
            return Path(env_path)
        
        package_root = Path(__file__).parents[3] 
        adjacent = package_root / "config" / "settings.yaml"
        if adjacent.exists():
            return adjacent
        
        raise FileNotFoundError(f"NukeKit could not find studio config.\n"
            f"  → Set the {cls.ENV_VAR} env var to your config path\n"
            f"  → Or place studio_settings.yaml in {package_root / 'config'}")
        
    @classmethod
    def load(cls)->dict:
        path = cls.resolve()
        with open(path, "r") as file:
            return yaml.safe_load(file)


class ConfigValidator:
    """Validate configuration against schema."""

    REQUIRED_KEYS = {
        'repository': ['root', 'subfolder'],
        'user': ['nuke_dir'],
    }

    @classmethod
    def validate(cls, config: dict) -> tuple[bool, list[str]]:
        """Validate config. Returns (is_valid, errors)."""
        errors = []
        
        # Check required sections
        for section, keys in cls.REQUIRED_KEYS.items():
            if section not in config:
                errors.append(f"Missing required section: {section}")
                continue
            
            for key in keys:
                if key not in config[section]:
                    errors.append(f"Missing required key: {section}.{key}")
        
        # Validate paths
        if 'repository' in config:
            root = Path(config['repository'].get('root', ''))
            if not root.is_absolute():
                errors.append(f"Repository root must be absolute path: {root}")
        
        return len(errors) == 0, errors
    