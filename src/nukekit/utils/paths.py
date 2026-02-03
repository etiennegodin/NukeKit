from __future__ import annotations
from pathlib import Path
from typing import Literal, List
import logging

path_types = Literal['str', 'Path']

logger = logging.getLogger(__name__)

class UserPaths:
    """All user paths."""

    BASE_DIR = Path.home() / ".nukekit"
    NUKE_GIZMO_DIR = Path.home() / ".nuke" / "gizmos"
    STATE_FILE = BASE_DIR / "local_state.json"
    LOG_FILE = BASE_DIR / "nukekit.log"
    CACHED_MANIFEST = BASE_DIR / "cached_manifest.json"

    @classmethod
    def ensure(cls):
        """Create local dirs if thy don't exist. Called once"""
        cls.BASE_DIR.mkdir(exist_ok=True)
        cls.NUKE_GIZMO_DIR.mkdir(parents=True, exist_ok=True)


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





