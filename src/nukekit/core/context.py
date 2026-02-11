from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Literal

from .manifest import Manifest

if TYPE_CHECKING:
    from ..utils.paths import UserPaths
    from .repository import Repository

logger = logging.getLogger(__name__)

class AppMode(str, Enum):
    PUBLISH = "publish"
    INSTALL = "install"
    SCAN = "scan"

APP_MODE = Literal["publish","install","scan"]

@dataclass
class Context:
    """
    Main class for session context
        
    :param repo: Repository instance from this session
    :type repo: Repository
    :param user_paths: UserPaths instance from this session
    :type user_paths: UserPaths
    :param config: Dictionnary read from ConfigLoader class 
    :type config: dict
    :param repo_manifest: Manifest instance from remote repository state
    :type repo_manifest: Manifest
    :param local_manifest: Manifest instance from cached local state
    :type local_manifest: Manifest
    :param local_state: Manifest instance from local state 
    :type local_state: Manifest


    """
    repo: Repository
    user_paths: UserPaths
    config: dict[str, Any ]
    repo_manifest: Manifest = None
    local_manifest: Manifest = None
    local_state: Manifest = None
    mode:AppMode = None


    def __post_init__(self):
        # Read cached manifests from disk
        self.repo_manifest = Manifest.from_file(self.repo.MANIFEST)
        self.local_manifest = Manifest.from_file(self.user_paths.CACHED_MANIFEST)

        # Create local state manifest from scanner
        self.local_state = Manifest.from_scanner(self)

        # Set specific install status for repo assets

    def _set_install_status(self):

        data = self.repo_manifest.data
        for asset_category, assets_dict in data.items():
            #Remote data for this category
            local_assets_dict = self.local_state.data[asset_category]
            for asset_name in assets_dict.keys():
                # Edge case, unpublished asset, default version to 0.0.0
                if asset_name not in local_assets_dict.keys():
                    assets_dict[asset_name]["0.0.0"].set_install_status("non_local")
                    continue

                versions = assets_dict[asset_name]
                local_versions = list(assets_dict[asset_name].keys() & local_assets_dict[asset_name].keys())

                for version_key, asset in versions.items():
                    if asset.version in local_versions:
                        assets_dict[asset.name][asset.version].set_install_status("local")
                    else:
                        assets_dict[asset.name][asset.version].set_install_status("non_local")
            data[asset_category] = assets_dict

        self.repo_manifest.data = data

    def _set_publish_status(self):

        data = self.local_state.data
        for asset_category, assets_dict in data.items():
            #Remote data for this category
            remote_assets_dict = self.repo_manifest.data[asset_category]
            for asset_name in assets_dict.keys():
                # Edge case, unpublished asset, default version to 0.0.0
                if asset_name not in remote_assets_dict.keys():
                    assets_dict[asset_name]["0.0.0"].set_publish_status("unpublished")
                    continue

                versions = assets_dict[asset_name]
                local_versions = list(assets_dict[asset_name].keys() & remote_assets_dict[asset_name].keys())

                for versions, asset in versions.items():
                    if asset.version in local_versions:
                        assets_dict[asset.name][asset.version].set_publish_status("synced")
            data[asset_category] = assets_dict

        self.local_state.data = data

    def _update_local_state(self):

        scanned_data = self.local_state.data
        local_data = self.local_manifest.data

        for assets_dict in scanned_data.values():
            for asset_name in assets_dict.keys():
                for asset in assets_dict[asset_name].values():
                    try:
                        asset.name in local_data[asset.type]
                    except KeyError:
                        # Catch Asset
                        msg = f"Error adding {asset.name} to local manifest. Type {asset.type} not supported"
                        logger.error(msg)
                    else:
                        # New asset
                        if asset.name not in local_data[asset.type].keys():
                            scanned_data[asset.type][asset.name] = {"versions": {asset.version : asset}}

                        # Version already in manifest, read from cached
                        elif asset.version in local_data[asset.type][asset.name].keys():
                            scanned_data[asset.type][asset.name][asset.version] = local_data[asset.type][asset.name][asset.version]
                            continue
                        # New version not in local state
                        scanned_data[asset.type][asset.name][asset.version] = asset

        self.local_state.data = scanned_data
        self.local_state.write_manifest()

    def set_mode(self, mode: APP_MODE):
        self.mode = AppMode(mode)

    def get_current_data(self) -> dict[str, Any]:
        if self.mode == AppMode.PUBLISH:
            return self.local_state.data
        elif self.mode == AppMode.INSTALL:
            return self.repo_manifest.data
