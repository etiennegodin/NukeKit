from __future__ import annotations
import json 
import logging
import tempfile
from typing import Self
from pathlib import Path
from .assets import Asset, ASSET_REGISTRY
from .versioning import Version
from ..utils.json import universal_decoder, UniversalEncoder
from ..utils.scanner import Scanner
from ..utils.paths import UserPaths

from pprint import pprint


logger = logging.getLogger(__name__)


class Manifest:
    def __init__(self, data:dict = None, root:Path = None):
        self.ROOT = root 
        self.decoder = universal_decoder
        self.encoder = UniversalEncoder
        self._ensure_manifest()
        self.data = data
        
    @classmethod
    def from_file(cls, path:Path):
        logger.debug(path)
        """Create Manifest from a file path"""
        root = path
        try:
            open(root, 'r')
        except FileNotFoundError:
            logger.error(f"Manifest file {root} not found")
            data = {}
        else:
            with open(root, 'r') as file:
                data = json.load(file, object_hook=universal_decoder) 
        return cls(data=data, root=root)
    
    @classmethod
    def from_scanner(cls, context:Context):
        userPaths = context.user_paths
        """Create Manifest from scanner results"""
        scanner = Scanner(context)
        scanner.scan_local()
        data = scanner.data
        return cls(data=data, root = userPaths.STATE_FILE)

    def _ensure_manifest(self)->bool:
        def new_manifest():
            data = {}
            for type in ASSET_REGISTRY.keys():
                data[type] = {}
            with open(self.ROOT, "w") as json_file:
                json.dump(data, json_file, indent= 4)
            return True
        try:
            with open(self.ROOT, 'r') as file:
                data = json.load(file, object_hook=self.decoder)
        except FileNotFoundError:
            return new_manifest()
        except json.decoder.JSONDecodeError:
            return new_manifest()
        else:
            return False

    def read_manifest(self)->dict:
        try:
            open(self.ROOT, 'r')
        except FileNotFoundError:
            logger.error(f"Manifest file {self.ROOT} doesn't exist")
            return None
        else:
            with open(self.ROOT, 'r') as file:
                return json.load(file, object_hook=self.decoder)

    def get_latest_asset_version(self, asset:Asset|str)->Version:
        data = self.read_manifest()
        if isinstance(asset,Asset):
            if asset.name in data[asset.type].keys():
                return Version(data[asset.type][asset.name]['latest_version'])
            
            # New asset pubish 
            #logger.info(f"Asset '{asset.name}' not found in {self.ROOT} manifest")
            return None
            
        elif isinstance(asset, str):
            # Asset type undefined, looping through options
            for asset_category, asset_names in data.items():
                if asset in asset_names.keys():
                    return Version(data[asset_category][asset]['latest_version'])

                logger.error(f"Asset '{asset}' not found in {self.ROOT} manifest")
        else:
            # Handle unexpected type 
            msg = f"{type(asset)} type for get_latest_asset_versions is not supported"
            logger.error(msg)
            raise NotImplementedError(msg)
    
    def write_manifest(self, data: dict = None, verbose: bool = False):
        if data is None:
            data = self.data
        with open(self.ROOT, "w") as json_file:
            json.dump(data, json_file, indent=4, cls=self.encoder)
        
        if verbose:
            logger.info(f"Successfully wrote {self.ROOT}")
            
    def update(self, asset:Asset):
        data = self.read_manifest()
        version = str(asset.version)
        if asset.type not in data:
            raise Exception('manifest')

        if asset.name not in data[asset.type]:
            data[asset.type][asset.name] = {"versions" : {version: asset},
                                        "latest_version" : version}
        else:
            data[asset.type][asset.name]['versions'][version] = asset  
            data[asset.type][asset.name]['latest_version'] = version

        self.write_manifest(data)
        logger.info(f"Successfully added {asset.name} v{version} to repo manifest")

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




