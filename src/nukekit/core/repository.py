from __future__ import annotations
import logging

from pathlib import Path
from typing import Literal

path_types = Literal['str', 'Path']

logger = logging.getLogger(__name__)

class Repository:

    def __init__(self, repo_dict:dict):
        """
        Object representation of remote repository 
        
        :param repo_dict: Dictionnary from config to configure repository
        :type repo_dict: dict
        """
        
        self.ROOT = Path(repo_dict['root'])
        self.SUBFOLDERS = repo_dict['subfolder']
        self.MANIFEST = self.ROOT / "manifest.json"
        self.ensure()
    
    def ensure(self)->bool:
        if not self.ROOT.exists():
            self.ROOT.mkdir(exist_ok= True)
            logger.info(f'Created central repo at {self.ROOT}')
            for s in self.SUBFOLDERS:
                Path(f"{self.ROOT}/{s}").mkdir(exist_ok= True)
            return True
        return False
    
    def build_from_manifest():
        pass

    def get_subdir(self,asset_type:str)->Path:
        subdir = Path(f"{self.ROOT}/{asset_type}")
        if not subdir.exists():
            raise FileNotFoundError(f"Path {subdir} does not exists")
        return subdir

    def list_assets(self, asset_type:str, output_type:path_types = 'Path'):
        if asset_type:
            subdir = self.get_subdir(asset_type)
            assets_dir = [p for p in subdir.iterdir() if p.is_dir()]
            if output_type == 'str':
                return [folder.name for folder in assets_dir]
            else:
                return assets_dir
        else:
            raise Exception
