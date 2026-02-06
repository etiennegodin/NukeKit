from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Literal, TypeAlias
import logging 
from .repository import Repository
from ..core.manifest import Manifest
from ..utils.paths import UserPaths 
from ..utils.scanner import Scanner

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

    def compare_to_remote(self):
        self.repo_manifest.compare(self.local_manifest)

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



