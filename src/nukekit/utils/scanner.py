from __future__ import annotations
from pathlib import Path
from ..core.assets import ASSET_SUFFIXES
from ..core.assets import asset_factory
from ..core.manifest import Manifest
import logging

logger = logging.getLogger(__name__)


class Scanner:
    def __init__(self, context:Context):
        self.context = context
    
    def scan_local(self, manifest:Manifest)->Manifest:
        """
        Scan for local files and update local state manifest
        
        :param self: Description
        :param manifest: Description
        :type manifest: Manifest
        :return: Description
        :rtype: Manifest
        """
        data = manifest.data
        path = self.context.user_paths.NUKE_DIR
        assets = {}
        
        for suffix, obj in ASSET_SUFFIXES.items():
            asset_paths = list(path.rglob(f"*{suffix}"))
            for path in asset_paths:
                asset = asset_factory(path)
                if asset.name not in data[obj.type].keys():
                    data[obj.type][asset.name] = {'versions': {str(asset.version) : asset}}
                elif str(asset.version) in data[obj.type][asset.name]['versions'].keys():
                    continue
                data[obj.type][asset.name]['versions'][str(asset.version)] = asset

        manifest.data = data
        return manifest
