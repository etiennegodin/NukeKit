from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Literal, TypeAlias
import logging 
from .repository import Repository
from .manifest import Manifest
from ..utils.paths import UserPaths 
from ..utils.scanner import Scanner
from .assets import Asset

from pprint import pprint


logger = logging.getLogger(__name__)

@dataclass
class Context():
    repo: Repository
    user_paths: UserPaths
    config: Dict[str, Any ]
    date: str
    repo_manifest: Manifest
    local_manifest: Manifest
    asset_types: TypeAlias = Literal['Gizmo', 'Script']

    def set_publish_status(self):


        data = self.local_manifest.data

        pprint(data)
        print("*"*100)
        
        for asset_category, assets_dict in data.items():
            #Remote data for this category
            remote_assets_dict = self.repo_manifest.data[asset_category]
            for asset_name in assets_dict.keys():
                # Edge case, unpublished asset, default version to 0.1.0
                if asset_name not in remote_assets_dict.keys():
                    assets_dict[asset_name]['versions']['0.1.0'].set_publish_status('unpublished')
                    continue

                versions = assets_dict[asset_name]['versions']
                local_versions = list(assets_dict[asset_name]['versions'].keys() & remote_assets_dict[asset_name]['versions'].keys())

                for versions, asset in versions.items():     
                    if str(asset.version) in local_versions:
                        assets_dict[asset.name]['versions'][str(asset.version)].set_publish_status('synced')
            print(assets_dict)
            data[asset_category] = assets_dict

        pprint(data)
        self.local_manifest.data = data

        
    def update_local_state(self):
        scanner = Scanner(self)
        scanned_assets = scanner.scan_local()
        data = self.local_manifest.data

        for assets_list in scanned_assets.values():
            for asset in assets_list:
                # New asset
                if asset.name not in data[asset.type].keys():
                            data[asset.type][asset.name] = {'versions': {str(asset.version) : asset}}
                # Version already in manifest, skip
                elif str(asset.version) in data[asset.type][asset.name]['versions'].keys():
                    continue
                # New version not in local state 
                data[asset.type][asset.name]['versions'][str(asset.version)] = asset

        self.local_manifest.write_manifest(verbose=True)



