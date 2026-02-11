from __future__ import annotations

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class Repository:

    def __init__(self, config:dict):
        """
        Initialize repository from config dictionary.
        
        Args:
            config: Dictionary from config to configure repository
        """
        root = config['repository']['root']
        root = os.path.expandvars(root)
        root = os.path.expanduser(root)

        self.ROOT = Path(root)
        self.SUBFOLDERS = config['repository']["subfolder"]
        self.MANIFEST = self.ROOT / "manifest.json"
        self.ensure()

    def ensure(self) -> bool:
        if not self.ROOT.exists():
            self.ROOT.mkdir(exist_ok= True)
            for s in self.SUBFOLDERS:
                (self.ROOT / s).mkdir(exist_ok=True, parents=True)

            logger.info(f"Created central repo at {self.ROOT}")
            return True
        return False

    def get_asset_subdir(self,asset_type:str) -> Path:
        """
        Get subdirectory for given asset type.
        
        Args:
            asset_type: Type of asset (e.g., 'Gizmo', 'Script')
            
        Returns:
            Path to the subdirectory
            
        Raises:
            FileNotFoundError: If subdirectory doesn't exist
        """
        subdir = self.ROOT / {asset_type}
        if not subdir.exists():
            raise FileNotFoundError(f"Path {subdir} does not exists")
        return subdir

