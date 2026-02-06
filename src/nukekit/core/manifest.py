from __future__ import annotations
import json 
import logging
import tempfile
from typing import Self
from pathlib import Path
from .assets import Asset, ASSET_REGISTRY
from .versioning import Version
from ..utils.json import universal_decoder, UniversalEncoder

from pprint import pprint


logger = logging.getLogger(__name__)


class Manifest:
    def __init__(self, path:Path):
        self.ROOT = path 
        self.decoder = universal_decoder
        self.encoder = UniversalEncoder
        self._ensure_manifest()
        self.data = self.read_manifest()

    

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
        logger.debug(asset.name)
        logger.debug(data[asset.type.name].keys())
        logger.debug(asset.name in data[asset.type.name].keys())
        if isinstance(asset,Asset):
            if asset.name in data[asset.type.name].keys():
                return Version(data[asset.type.name][asset.name]['latest_version'])
            logger.info(f"Asset '{asset.name}' not found in {self.ROOT} manifest")
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
        if asset.type.name not in data:
            raise Exception('manifest')

        if asset.name not in data[asset.type.name]:
            data[asset.type.name][asset.name] = {"versions" : {version: asset},
                                        "latest_version" : version}
        else:
            data[asset.type.name][asset.name]['versions'][version] = asset  
            data[asset.type.name][asset.name]['latest_version'] = version

        self.write_manifest(data)
        logger.info(f"Successfully added {asset.name} v{version} to repo manifest")




