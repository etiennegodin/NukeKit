from __future__ import annotations

import json
import logging
from enum import Enum
from pathlib import Path

from .assets import ASSET_REGISTRY, AssetStatus
from .versioning import Version

logger = logging.getLogger(__name__)


def dataclass_to_dict(obj):
    """Small dataclass serializer to avoid recursive"""
    result = {}
    for field in obj.__dataclass_fields__:
        value = getattr(obj, field)

        # Handle Version here
        if isinstance(value, Version):
            result[field] = str(value)
        else:
            result[field] = value

    result["__type__"] = type(obj).__name__
    return result


def stringify_keys(obj):
    if isinstance(obj, dict):
        return {
            str(k) if isinstance(k, Version) else k: stringify_keys(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [stringify_keys(i) for i in obj]
    return obj


def universal_decoder(dct):
    # Dynamic: Convert any key that ends with "_path" into a Path object
    for k, v in dct.items():
        if isinstance(v, str) and k.endswith("_path"):
            dct[k] = Path(v)
        elif (isinstance(v, str)) and k == "version":
            dct[k] = Version.from_string(v)
        elif isinstance(v, str) and k == "status":
            dct[k] = AssetStatus(v)

    # After fixing paths, handle dataclass reconstruction
    if "__type__" in dct:
        type_name = dct.pop("__type__")
        cls = ASSET_REGISTRY.get(type_name)
        if cls:
            return cls(**dct)
    return dct


class UniversalEncoder(json.JSONEncoder):
    def default(self, obj):
        # Handle Version as str rather than dict
        if isinstance(obj, Version):
            return str(obj)
        # Handle dataclasses
        if hasattr(obj, "__dataclass_fields__"):
            return dataclass_to_dict(obj)
        if isinstance(obj, Path):
            return str(obj)
        elif isinstance(obj, Enum):
            return str(obj.name)
        elif obj is NotImplemented:
            return None
        return super().default(obj)


def dump_json(data, path: Path):
    """_summary_

    Args:
        data (_type_): _description_
        path (Path): _description_

    Raises:
        e: _description_
    """
    data = stringify_keys(data)
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4, cls=UniversalEncoder)
    except Exception as e:
        logger.exception(f"Error writing manifest to {path}: {e}")
        raise e


def dumps_json(data) -> str:
    """_summary_

    Args:
        data (_type_): _description_

    Raises:
        e: _description_

    Returns:
        str: _description_
    """
    data = stringify_keys(data)
    try:
        out = json.dumps(data, indent=4, cls=UniversalEncoder)
    except Exception as e:
        logger.exception(e)
        raise e
    else:
        return out


def load_json(path: Path) -> dict:
    """_summary_

    Args:
        path (Path): _description_

    Raises:
        e: _description_

    Returns:
        dict: _description_
    """
    try:
        with open(path) as file:
            return json.load(file, object_hook=universal_decoder)
    except Exception as e:
        logger.exception(e)
        raise e
