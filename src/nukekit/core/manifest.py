from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Self

from ..utils import _sort_dict
from .assets import Asset, AssetType
from .scanner import scan_folder
from .serialization import dump_json, load_json
from .versioning import Version

if TYPE_CHECKING:
    from ..utils import UserPaths

logger = logging.getLogger(__name__)


class Manifest:
    def __init__(self, data: dict, root: Path):
        self.ROOT = root
        self.data = data
        self.write_manifest()

    @classmethod
    def from_json(cls, path: Path) -> Self:
        """Create Manifest from a file path"""
        if isinstance(path, str):
            path = Path(path)
        root = path
        data = cls.read_manifest(self=cls, path=root)
        return cls(data=data, root=root)

    @classmethod
    def from_local_state(cls, user_paths: UserPaths) -> Self:
        """Create Manifest from scanner results"""
        data = scan_folder(user_paths.NUKE_DIR)
        return cls(data=data, root=user_paths.STATE_FILE)

    @classmethod
    def _new_empty_manifest(cls) -> dict:
        return {a.value: {} for a in AssetType}

    def read_manifest(self, path: Path | None = None) -> dict:
        """Read and return manifest data. Returns empty dict if file doesn"t exist.

        :param path: Optionnal path to read manifest. Defaults to manifest root
        :type path: Path
        :return: Data from manifest json file. Defaults to empty if not found.
        :rtype: dict
        """
        if path is not None:
            manifest_path = path
        else:
            manifest_path = self.ROOT

        if not manifest_path.exists():
            logger.warning(f"{manifest_path} does not exist, returning empty manifest")
            return self._new_empty_manifest()
        try:
            with open(manifest_path):
                data = load_json(manifest_path)

                return _sort_dict(data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse manifest {manifest_path}: {e}")
            return self._new_empty_manifest()
        except Exception as e:
            logger.error(f"Unexpected error reading manifest: {e}")
            raise

    def write_manifest(self, data: dict | None = None, verbose: bool = False) -> bool:
        """
        Write manifest data to disk.

        :param data: Data to write on disk. If empty defaults to manifest"s data.
        :type data: dict
        :param verbose: Add a logger liner confirming successfull write
        :type verbose: bool
        :return: Confirmation of successfull write
        :rtype: bool
        """

        if data is None:
            try:
                data = self.data
            except Exception as e:
                logger.error(f"Error loading manifest data from {self.ROOT}: {e}")
                raise

        # Sort outgoing dict
        data = _sort_dict(data)

        # Write to disk
        dump_json(data, self.ROOT)

        if verbose:
            logger.info(f"Successfully wrote {self.ROOT}")
        return True

    def add(self, asset: Asset) -> bool:
        """
        Reads current manifest, adds asset and writes out updated manifest.

        :param asset: Asset object to add to manifest
        :type asset: Asset
        :return: Confirmation of successfull add
        :rtype: bool
        """

        data = self.read_manifest()

        if asset.name not in data[asset.type]:
            # New asset
            data[asset.type][asset.name] = {asset.version: asset}
        else:
            # Existing asset, add to asset"s dict
            data[asset.type][asset.name][asset.version] = asset

        if self.write_manifest(data):
            # Updates current status
            self.data = data
            logger.debug(
                f"Successfully added {asset.name} v{asset.version} to {self.ROOT}"
            )
            return True
        else:
            return False

    def get_latest_asset_version(self, asset: Asset) -> Version | None:
        """
        Parses the manifest and returns the highest version for this asset.

        :param asset: Asset to return latest version
        :type asset: Asset
        :return: Version instance of latest asset"s version
        :rtype: Version
        """

        data = self.read_manifest()

        try:
            data[asset.type][asset.name]
        except Exception:
            # Asset is not in manifest.
            return None
        else:
            # Asset is in manifest, get list of all versions.
            asset_versions_list = list(data[asset.type][asset.name].keys())
            if len(asset_versions_list) > 1:
                # If list has at least two version, sort and return highest value
                return Version.highest_version(asset_versions_list)
            else:
                # Only one version
                return asset_versions_list[0]
