from __future__ import annotations
from pathlib import Path
from ..core.assets import ASSET_SUFFIXES
from ..core.assets import asset_factory
from ..core.manifest import Manifest
from ..core.assets import Asset
import logging

logger = logging.getLogger(__name__)

class Scanner:
    def __init__(self, context:Context):
        self.context = context

    def _scan(self,path:Path)->dict:
        assets = {}
        for suffix, obj in ASSET_SUFFIXES.items():
            asset_paths = list(path.rglob(f"*{suffix}"))
            asset_subtype = []
            for path in asset_paths:
                asset = asset_factory(path)
                logger.debug(asset.type)
                asset_subtype.append(asset)
            assets[obj.type] = asset_subtype
        return assets
    
    def scan_local(self)->dict[str,list[Asset]]:
        return self._scan(self.context.user_paths.NUKE_DIR)

    def scan_folder(self, path)->dict:
        if path is not None:
            return self._scan(path)
