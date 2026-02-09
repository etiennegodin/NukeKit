from __future__ import annotations
import logging
from pathlib import Path

from ..core.assets import ASSET_SUFFIXES
from ..core.assets import Asset

logger = logging.getLogger(__name__)

class Scanner:
    def __init__(self, context:Context):
        self.context = context
        self.user_paths = context.user_paths

    def _scan(self,path:Path)->dict:
        assets = {}
        for suffix, obj in ASSET_SUFFIXES.items():
            asset_paths = list(path.rglob(f"*{suffix}"))
            asset_subtype = {}
            for path in asset_paths:
                asset = Asset.from_path(self.context,path)
                logger.debug(type(asset.version))
                logger.debug(asset.version)
                if asset.name not in asset_subtype.keys():
                    asset_subtype[asset.name] = {"versions" : {}}
                if str(asset.version) not in asset_subtype[asset.name]['versions'].keys():
                    asset_subtype[asset.name]['versions'][str(asset.version)] = asset
            assets[obj.type] = asset_subtype
        return assets
    
    def scan_local(self, verbose:bool = False)->dict:
        self.data = self._scan(self.user_paths.NUKE_DIR)
        return self.data

    def scan_folder(self, path)->dict:
        if path is not None:
            return self._scan(path)
