from __future__ import annotations
from pathlib import Path
from typing import Literal
import logging

path_types = Literal['str', 'Path']

logger = logging.getLogger(__name__)


class CentralRepo:
    def __init__(self, repo_dict:dict):
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

    def get_subdir(self,asset_type:Context.asset_types)->Path:
        subdir = Path(f"{self.ROOT}/{asset_type}s")
        if subdir.exists():
            return subdir

    def list_assets(self, asset_type:Context.asset_types, output_type:path_types = 'Path'):
        subdir = self.get_subdir(asset_type)
        assets_dir = [p for p in subdir.iterdir() if p.is_dir()]
        if output_type == 'str':
            return [folder.name for folder in assets_dir]
        else:
            return assets_dir





