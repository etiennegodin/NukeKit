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
        for asset_category, asset_list in assets.items():

            if asset_category not in unpublished_assets.keys(): unpublished_assets[asset_category] = []
            if asset_category not in outdated_assets.keys(): outdated_assets[asset_category] = []
            if asset_category not in latest_assets.keys(): latest_assets[asset_category] = []
            local_repo_asset_type = local_state[asset_category]
            for a in asset_list:
                asset_name = a.name
                if asset_name not in local_repo_asset_type.keys():
                    unpublished_assets[asset_category].append(a)
                    continue

                asset_versions_dict = local_repo_asset_type[asset_name]['versions']
                x= asset_versions_dict.keys()
                latest_version = self.context.local_manifest.get_latest_asset_version(a)
                if a.version < latest_version:
                    outdated_assets[asset_category].append(a)
                    continue
                try:
                    local_repo_asset = asset_versions_dict[str(a.version)]
                except KeyError:
                    ValueError('Local tool higher version than local repo, manifest was not uopdated correctly ') 
                else:
                    latest_assets[asset_category].append(local_repo_asset)

                    
        print('unpublished_assets')
        pprint(unpublished_assets)
        print('outdated_assets')
        pprint(outdated_assets)
        print('latest_assets')
        pprint(latest_assets)


    def scan_local(self)->dict:

        assets = self._scan(self.context.user_paths.NUKE_DIR)
        pprint(assets)
        self._compare_to_local_manifest(assets)

    def scan_folder(self, path)->dict:
        if path is not None:
            return self._scan(path)
