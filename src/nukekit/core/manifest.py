from __future__ import annotations
import json 
from pathlib import Path
from typing import Self
from .assets import Asset, ASSET_REGISTRY
from .versioning import Version
from ..utils.json import universal_decoder, UniversalEncoder
import logging
logger = logging.getLogger(__name__)

class Manifest:
    def __init__(self, path:Path):
        self.ROOT = path 
        self._ensure_manifest()
        self.decoder = universal_decoder
        self.encoder = UniversalEncoder
        self.data = self.read_manifest()

    def _ensure_manifest(self)->bool:
        if self.ROOT.exists():
            #to-do check if empty
            return False
        else:
            # Create empty manifest 
            data = {}
            for type in ASSET_REGISTRY.keys():
                data[type] = {}
            with open(self.ROOT, "w") as json_file:
                json.dump(data, json_file, indent= 4)
            return True

    def read_manifest(self):
        try:
            open(self.ROOT, 'r')
        except FileNotFoundError:
            logger.error(f"Manifest file {self.ROOT} doesn't exist")
            return None
        else:
            with open(self.ROOT, 'r') as file:
                return json.load(file, object_hook=self.decoder)

    def get_latest_asset_version(self, asset:Asset):
        data = self.read_manifest()
        if asset.name in data[asset.type]:
            return Version(data[asset.type][asset.name]['latest_version'])

    def update_manifest(self, asset:Asset):
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
        
        with open(self.ROOT, "w") as json_file:
            json.dump(data, json_file, indent=4, cls=self.encoder)
            logger.info(f"Successfully added {asset.name} v{version} to repo manifest")

    def compare_manifests(self, other:Self):
        pass