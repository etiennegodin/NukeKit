from __future__ import annotations
import json 
from dataclasses import asdict
from pathlib import Path
from .assets import Asset, ASSET_REGISTRY
from .versioning import Version
import logging

logger = logging.getLogger(__name__)

class UniversalEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__dataclass_fields__"):
            # asdict() recursively converts nested dataclasses to dicts
            d = asdict(obj)
            d["__type__"] = type(obj).__name__
            return d
        if isinstance(obj, Path):
            return str(obj)
        elif isinstance(obj, Version):
            return str(obj)
        return super().default(obj)


def universal_decoder(dct):
    # Dynamic: Convert any key that ends with '_path' into a Path object
    for k, v in dct.items():
        if isinstance(v, str) and k.endswith('_path'):
            dct[k] = Path(v)

    # After fixing paths, handle dataclass reconstruction
    if "__type__" in dct:
        type_name = dct.pop("__type__")
        cls = ASSET_REGISTRY.get(type_name)
        if cls:
            return cls(**dct)
    return dct

class Manifest:
    def __init__(self, path:Path):
        self.ROOT = path 
        self._ensure_manifest()
        self.decoder = universal_decoder
        self.encoder = UniversalEncoder

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
