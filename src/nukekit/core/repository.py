from __future__ import annotations
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class Repository:

    def __init__(self, config:dict):
        """
        Object representation of remote repository 
        
        :param repo_dict: Dictionnary from config to configure repository
        :type repo_dict: dict
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
        subdir = Path(f"{self.ROOT}/{asset_type}")
        if not subdir.exists():
            raise FileNotFoundError(f"Path {subdir} does not exists")
        return subdir

