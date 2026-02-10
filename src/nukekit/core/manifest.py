from __future__ import annotations
from typing import TYPE_CHECKING, Self
import json 
import logging
from pathlib import Path

from .assets import ASSET_REGISTRY
from .versioning import Version
from .serialization import dump_json, load_json
from ..utils.scanner import Scanner

if TYPE_CHECKING:
    from .context import Context
    from .assets import Asset

logger = logging.getLogger(__name__)

def _sort(d:dict):
    return {
            k: _sort(v) if isinstance(v, dict) else v
            for k, v in sorted(d.items(), reverse=True)
    }

class Manifest:

    def __init__(self, data:dict = None, root:Path = None):
        self.ROOT = root 
        self.data = data
        self.write_manifest()

        
    @classmethod
    def from_file(cls, path:Path) -> Self:
        """Create Manifest from a file path"""
        root = path
        data = cls.read_manifest(self = cls,path = root)
        return cls(data = data,root = root)

    @classmethod
    def from_scanner(cls, context:Context) -> Self:
        """Create Manifest from scanner results"""
        scanner = Scanner(context)
        scanner.scan_local()
        return cls(data=scanner.data, root = context.user_paths.STATE_FILE)
    
    @classmethod
    def _new_empty_manifest(self) -> dict:
        return {type_: {} for type_ in ASSET_REGISTRY.keys()}

    def read_manifest(self, path:Path = None) -> dict:
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
            with open(manifest_path, "r") as file:
                data = load_json(manifest_path)
                return _sort(data)        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse manifest {manifest_path}: {e}")
            return self._new_empty_manifest()
        except Exception as e:
            logger.error(f"Unexpected error reading manifest: {e}")
            raise

    def write_manifest(self, data: dict = None, verbose: bool = False) -> bool:
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
                logger.error(f"Error loading manifest data from {self.name}: {e}")
                raise

        # Sort outgoing dict
        data = _sort(data)

        # Write to disk 
        try:
            dump_json(data, self.ROOT)
        except Exception as e:
            logger.exception(f"Error writing manifest to {self.ROOT}: {e}")
        else:
            if verbose:
                logger.info(f"Successfully wrote {self.ROOT}")
            
    def update(self, asset:Asset) -> bool:
        """
        Reads current manifest, adds asset and writes out updated manifest. 

        :param asset: Asset object to add to manifest 
        :type asset: Asset
        :return: Confirmation of successfull update
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
            logger.info(f"Successfully added {asset.name} v{asset.version} to repo manifest")
            return True
        else:
            return False

    def get_latest_asset_version(self, asset:Asset) -> Version:
        """
        Parses the manifest and returns the highest version for this asset.
        
        :param asset: Asset to return latest version
        :type asset: Asset
        :return: Version instance of latest asset"s version
        :rtype: Version
        """
        data = self.read_manifest()

        if isinstance(asset,Asset):
            try:
                asset_versions_list = list(asset.name in data[asset.type].keys())
            except Exception as e:
                logger.error(f"Could not find {asset.name} in {self.name} manifest")
                raise
            else:
                return Version.highest_version(asset_versions_list)
            
        else:
            # Handle unexpected type 
            msg = f"{type(asset)} type for get_latest_asset_versions is not supported"
            logger.error(msg)
            raise NotImplementedError(msg)
 


