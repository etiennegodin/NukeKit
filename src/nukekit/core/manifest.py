from __future__ import annotations
import json 
from pprint import pprint
from .assets import Asset, Gizmo, Scripts
from .context import Context
from .versioning import Version
from dataclasses import asdict

from pathlib import Path

CLASS_REGISTRY = {"Gizmos": Gizmo, "Scripts": Scripts, "Asset": Asset}

class UniversalEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__dataclass_fields__"):
            # Add metadata so we know how to rebuild it later
            d = asdict(obj)
            d["__type__"] = type(obj).__name__
            return d
        if isinstance(obj, Path):
            return str(obj)
        elif isinstance(obj, Version):
            return obj.__repr__()
        return super().default(obj)


def universal_decoder(dct):
    # Dynamic: Convert any key that ends with '_path' into a Path object
    for k, v in dct.items():
        if isinstance(v, str) and k.endswith('_path'):
            dct[k] = Path(v)

    # After fixing paths, handle dataclass reconstruction
    if "__type__" in dct:
        type_name = dct.pop("__type__")
        cls = CLASS_REGISTRY.get(type_name)
        if cls:
            return cls(**dct)
    return dct

def load_latest_asset_version(contetx:Context,asset_name, asset_type:Context.asset_types):

    with open('data.json', 'r') as file:
        data = json.load(file, object_hook=universal_decoder)
    with open('data.json', 'r') as file:
        data = json.load(file, object_hook=universal_decoder)
    
    print(data)

def add_asset_to_manifest(asset:Asset):        
    with open("data.json", "w") as json_file:
        json.dump(asset, json_file, indent=4, cls=UniversalEncoder) # indent for pretty-printing


    pass


def init_manifest(ROOT_FOLDER):
    manifest_path = Path(ROOT_FOLDER/f"data/manifest.json")
    if manifest_path.exists():
        return manifest_path
    else:
        data = {'gizmos' : {}, "scripts" : {}}
        with open(manifest_path, "w") as json_file:
            json.dumps(data, json_file, indent= 4)
        return manifest_path