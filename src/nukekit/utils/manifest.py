from __future__ import annotations
import json 
from pprint import pprint
from ..core.context import Context
from ..core.assets import Asset, Gizmo, Scripts
from ..core.versioning import Version
from dataclasses import asdict

from pathlib import Path

CLASS_REGISTRY = {"Gizmos": Gizmo, "Scripts": Scripts, "Asset": Asset}

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
        cls = CLASS_REGISTRY.get(type_name)
        if cls:
            return cls(**dct)
    return dct

def read_manifest(context:Context):
    with open(context.manifest, 'r') as file:
        return json.load(file, object_hook=universal_decoder)


def load_latest_asset_version(contetx:Context,asset_name, asset_type:Context.asset_types):

    with open('data.json', 'r') as file:
        data = json.load(file, object_hook=universal_decoder)
    
    print(data)

def update_manifest(context:Context, asset:Gizmo|Scripts):
    data = read_manifest(context)

    category = f"{asset.type}s"
    version = str(asset.version)
    if category not in data:
        data[category] = {}

    if asset.name not in data[category]:
        data[category][asset.name] = {"versions" : {version: asset},
                                    "latest_version" : version}
    else:
        data[category][asset.name]['versions'][version] = asset  
        data[category][asset.name]['latest_version'] = version
    
    pprint(data)

    with open(context.manifest, "w") as json_file:
        json.dump(data, json_file, indent=4, cls=UniversalEncoder) # indent for pretty-printing
        context.logger.info(f"Successfully added {asset.name} v{version} to repo")
    



def init_manifest(manifest_path:Path)->bool:
    if manifest_path.exists():
        return False
    else:
        data = {
            "gizmos" : {},
            "scripts" : {}}
        with open(manifest_path, "w") as json_file:
            json.dump(data, json_file, indent= 4)
        return True