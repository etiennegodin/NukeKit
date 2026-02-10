from __future__ import annotations
from typing import TYPE_CHECKING, Self
import json 
import logging
from pathlib import Path

from .assets import ASSET_REGISTRY
from .versioning import Version
from ..utils.json import universal_decoder, UniversalEncoder
from ..utils.scanner import Scanner

if TYPE_CHECKING:
    from .context import Context
    from .assets import Asset

logger = logging.getLogger(__name__)

class Manifest:
    def __init__(self, data:dict = None, root:Path = None):
        self.ROOT = root 
        self.decoder = universal_decoder
        self.encoder = UniversalEncoder
        self.write_manifest()
        self.data = data
        
    @classmethod
    def from_file(cls, path:Path) -> Self:
        """Create Manifest from a file path"""
        root = path
        data = cls.read_manifest(path)
        return cls(data = data,root = root)

    @classmethod
    def from_scanner(cls, context:Context) -> Self:
        """Create Manifest from scanner results"""
        scanner = Scanner(context)
        scanner.scan_local()
        return cls(data=scanner.data, root = context.user_paths.STATE_FILE)
        
    def read_manifest(self, path:Path = None) -> dict:
        """Read and return manifest data. Returns empty dict if file doesn't exist.
    
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
            logger.warning(f"Manifest file {manifest_path} doesn't exist, returning empty manifest")
            return self._new_empty_manifest()
        try:
            with open(manifest_path, 'r') as file:
                data = json.load(file, object_hook=self.decoder)
                return self._sort(data)        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse manifest {manifest_path}: {e}")
            return self._new_empty_manifest()
        except Exception as e:
            logger.error(f"Unexpected error reading manifest: {e}")
            raise

    def write_manifest(self, data: dict = None, verbose: bool = False) -> bool:
        """
        Write manifest data to disk. 
        
        :param data: Data to write on disk. If empty defaults to manifest's data. 
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
        data = self._sort(data)

        # Write to disk 
        try:
            with open(self.ROOT, "w") as json_file:
                json.dump(data, json_file, indent=4, cls=self.encoder)
        except Exception as e:
            logger.error(f"Error writing manifest to {self.ROOT}: {e}")
        else:
            if verbose:
                logger.info(f"Successfully wrote {self.ROOT}")
            
    def update(self, asset:Asset) -> None:
        """
        Reads current manifest, adds asset and writes out updated manifest. 

        :param asset: Asset object to add to manifest 
        :type asset: Asset
        """

        data = self.read_manifest()
        version_string = asset.version

        if asset.type not in data:
            raise Exception('manifest')

        if asset.name not in data[asset.type]:
            data[asset.type][asset.name] = {version_string: asset}
        else:
            data[asset.type][asset.name][version_string] = asset  

        self.write_manifest(data)
        logger.info(f"Successfully added {asset.name} v{version_string} to repo manifest")

    def get_asset(self, id:str):

        def recursive_dict_loop(d):
            for key, value in d.items():
                if isinstance(value, dict):
                    # If the value is a dictionary, recurse into it
                    recursive_dict_loop(value)
                else:
                    # Otherwise, process the key-value pair
                    print(f"Key: {key}, Value: {value}")

        recursive_dict_loop(self.data)

    def get_latest_asset_version(self, asset:Asset|str)->Version:
        data = self.read_manifest()
        if isinstance(asset,Asset):
            if asset.name in data[asset.type].keys():
                versions = list(data[asset.type][asset.name])
                latest = Version.from_tuple((0,0,0))
                for v in versions:
                    v = Version(v)
                    if v > latest:
                        latest = v
                return latest
            # New asset pubish 
            #logger.info(f"Asset '{asset.name}' not found in {self.ROOT} manifest")
            return None
        else:
            # Handle unexpected type 
            msg = f"{type(asset)} type for get_latest_asset_versions is not supported"
            logger.error(msg)
            raise NotImplementedError(msg)
 
    def _new_empty_manifest(self) -> dict:
        return {type_: {} for type_ in ASSET_REGISTRY.keys()}

    def _sort(self, d:dict):
        return {
            k: self._sort(v) if isinstance(v, dict) else v
            for k, v in sorted(d.items(), reverse=True)
        }

