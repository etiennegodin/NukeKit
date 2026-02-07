from __future__ import annotations
from pathlib import Path
from ..core.assets import ASSET_SUFFIXES
from ..core.assets import asset_factory
from ..utils.paths import UserPaths
import logging

logger = logging.getLogger(__name__)

class Scanner:
    def __init__(self, user_paths:UserPaths):
        self.user_paths = user_paths

    def _scan(self,path:Path)->dict:
        assets = {}
        for suffix, obj in ASSET_SUFFIXES.items():
            asset_paths = list(path.rglob(f"*{suffix}"))
            asset_subtype = {}
            for path in asset_paths:
                asset = asset_factory(path)
                if asset.name not in asset_subtype:
                    asset_subtype['asset.name'] = {"versions" : {str(asset.version) : asset}}
                elif str(asset.version) not in asset_subtype['versions']:
                    asset_subtype['asset.name']['versions'] = {str(asset.version) : asset}
                logger.debug(asset.type)
            assets[obj.type] = asset_subtype
        return assets
    
    def scan_local(self)->dict:
        self.data = self._scan(self.user_paths.NUKE_DIR)
        return self.data

    def scan_folder(self, path)->dict:
        if path is not None:
            return self._scan(path)
    
