import os
import yaml
import logging
from pathlib import Path
from typing import Optional

class ConfigLoader:

    ENV_VAR = "NUKEKIT_CONFIG_PATH"

    @classmethod
    def resolve(cls)->Path:
        env_path = os.getenv(cls.ENV_VAR)
        if env_path and Path(env_path).exists():
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
        with open(path, 'r') as file:
            return yaml.safe_load(file)

        
