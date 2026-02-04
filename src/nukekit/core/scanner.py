from __future__ import annotations
from .context import Context
from pathlib import Path
from .assets import ASSET_SUFFIXES
from typing import get_args
from .assets import asset_factory
from pprint import pprint
from .validator import ASSET_STATUS

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
    
    def _compare_to_local_manifest(self, assets:dict):
        local_state = self.context.local_manifest.data
        unpublished_assets = {}
        outdated_assets = {}
        latest_assets = {}
        print(local_state)
        for asset, asset_list in assets.items():
            if asset not in unpublished_assets.keys(): unpublished_assets[asset] = []
            if asset not in outdated_assets.keys(): outdated_assets[asset] = []
            if asset not in latest_assets.keys(): latest_assets[asset] = []

            for a in asset_list:
                if a not in local_state[asset]:
                    unpublished_assets[asset].append(a)

                local_asset = local_state[asset]



            pass

    def scan_local(self)->dict:

        assets = self._scan(self.context.user_paths.NUKE_DIR)
        self._compare_to_local_manifest(assets)

    def scan_folder(self, path)->dict:
        if path is not None:
            return self._scan(path)
