from __future__ import annotations
from .context import Context
from pathlib import Path
from .assets import ASSET_SUFFIXES
from typing import get_args
from .assets import asset_factory
from pprint import pprint
from .validator import compare_manifest
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
                asset_subtype.append(asset)
            assets[obj.type] = asset_subtype
        return assets
    
    def scan_local(self)->dict:
        assets = self._scan(self.context.user_paths.NUKE_DIR)
        compare_manifest(self.context.local_manifest, assets)

    def scan_folder(self, path)->dict:
        if path is not None:
            return self._scan(path)
