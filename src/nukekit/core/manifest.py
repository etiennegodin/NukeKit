from __future__ import annotations
import json 
import logging
import tempfile
from typing import Self
from pathlib import Path
from .assets import Asset, ASSET_REGISTRY, AssetStatus
from .versioning import Version
from ..utils.json import universal_decoder, UniversalEncoder

from pprint import pprint


logger = logging.getLogger(__name__)


class Manifest:
    def __init__(self, path:Path = None):
        self.ROOT = path 
        self._ensure_manifest()
        self.decoder = universal_decoder
        self.encoder = UniversalEncoder
        self.data = self.read_manifest()

    def _ensure_manifest(self)->bool:
        if self.ROOT is None:
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".txt") as tmp_file:
                tmp_path = Path(tmp_file.name)
                tmp_file.write("Temporary content")
                # Content is written, but the file is still open.
                # We can now use 'tmp_path' as a pathlib object.


        elif self.ROOT.exists():
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

    def read_manifest(self)->dict:
        try:
            open(self.ROOT, 'r')
        except FileNotFoundError:
            logger.error(f"Manifest file {self.ROOT} doesn't exist")
            return None
        else:
            with open(self.ROOT, 'r') as file:
                return json.load(file, object_hook=self.decoder)

    def get_latest_asset_version(self, asset:Asset|str):
        data = self.read_manifest()
        
        if isinstance(asset,Asset):
            try:
                asset.name in data[asset.type]
            except KeyError:
                logger.error(f"Asset {asset.name} not found in manifest")
                raise KeyError
            
            return Version(data[asset.type][asset.name]['latest_version'])
            
        elif isinstance(asset, str):
            asset_name = asset
            for asset_category, asset_names in data.items():
                try: 
                    asset_name in asset_names.keys()
                except KeyError:
                    logger.error(f"Asset {asset.name} not found in manifest")
                    raise KeyError
                
                return Version(data[asset_category][asset_name]['latest_version'])
        else:
            msg = f"{type(asset)} type for get_latest_asset_versions is not supported"
            logger.error(msg)
            raise NotImplementedError(msg)
                

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
        
        with open(self.ROOT, "w") as json_file:
            json.dump(data, json_file, indent=4, cls=self.encoder)
            logger.info(f"Successfully added {asset.name} v{version} to repo manifest")


    def compare(self, against:Manifest|dict):

        print(type(self))
        print(type(against))

        pprint(self.data)

        if isinstance(against, Manifest):
            against_data = against.data
        elif isinstance(against, dict):
            #against = Manifest()
            against_data = against
        else:
            raise ValueError(f"Child manifest type {type(against)} not accepted")
        
        updated_assets = {}
        pprint(updated_assets)


        for asset_category, assets_dict in self.data.items():
            # Create empty list for each category
            if asset_category not in updated_assets.keys(): updated_assets[asset_category] = []

            against_assets_dict = against_data[asset_category]

            for asset_name in assets_dict.keys():

                # Edge case, unpublished asset, default version to 0.1.0
                if asset_name not in against_assets_dict.keys():
                    asset = assets_dict[asset_name]['versions']['0.1.0']
                    asset.setstatus('unpublished')
                    updated_assets[asset_category].append(asset)
                    continue

                # Define latest version of this asset in the against manifest 
        
                latest_version = against.get_latest_asset_version(asset_name)
                print(latest_version)

                        
                versions = assets_dict[asset_name]['versions']
                for asset in versions.values():
                    asset:Asset

                    








        #Assign status  through against manifest 
        for asset_category, against_assets_dict in against_data.items():
            # Create empty list for each category
            if asset_category not in updated_assets.keys(): updated_assets[asset_category] = []

            #Define list of asset for this category from this
            self_assets_list = self.data[asset_category]

            
            for against_asset_name, against_asset_versions in against_assets_dict.items():
                # Manually set against_asset to Asset to get methods 
                against_asset:Asset

                # Check if against asset 
                if against_asset.name not in self_assets_list.keys():
                    against_asset.set_status('unpublished')
                    updated_assets[asset_category].append(against_asset)
                    continue
                
                self_asset_versions = self_assets_list[against_asset.name]['versions']

                if isinstance(against, Manifest):
                    latest_version = against.get_latest_asset_version(against_asset)
                else:
                    raise NotImplementedError("Cant't find latest version from dict")
                
                if against_asset.version < latest_version:
                    against_asset.set_status('outdated')
                    assets[asset_category].append(against_asset)
                    logger.warning(f"Found outdated version of {against_asset} in against folder.")
                    continue
                try:
                    against_repo_asset = remote_repo_asset_versions_dict[str(against_asset.version)]
                    against_repo_asset: Asset
                except KeyError:
                    ValueError('Local tool higher version than against repo, manifest was not uopdated correctly ') 
                else:
                    against_repo_asset.set_status('synced')
                    assets[asset_category].append(against_repo_asset)

            
        pprint(assets)


