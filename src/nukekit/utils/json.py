from __future__ import annotations
import json
from dataclasses import asdict
from pathlib import Path

from ..core.assets import ASSET_REGISTRY
from ..core.versioning import Version
from ..core.assets import AssetStatus


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
        elif isinstance(obj, AssetStatus):
            return str(obj.name)
        return super().default(obj)


def universal_decoder(dct):
    # Dynamic: Convert any key that ends with '_path' into a Path object
    for k, v in dct.items():
        if isinstance(v, str) and k.endswith('_path'):
            dct[k] = Path(v)
        if isinstance(v,str) and k == 'version':
            dct[k] = Version(v)
        if isinstance(v,str) and k == 'status':
            dct[k] = AssetStatus(v)

    # After fixing paths, handle dataclass reconstruction
    if "__type__" in dct:
        type_name = dct.pop("__type__")
        cls = ASSET_REGISTRY.get(type_name)
        if cls:
            return cls(**dct)
    return dct