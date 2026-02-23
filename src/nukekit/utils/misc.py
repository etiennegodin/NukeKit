from typing import Any


def _sort_dict(d: dict[Any, Any]) -> dict[Any, Any]:
    return {
        k: _sort_dict(v) if isinstance(v, dict) else v
        for k, v in sorted(d.items(), reverse=True)
    }


def deep_merge(source: dict[Any, Any], target: dict[Any, Any]) -> dict[Any, Any]:
    for k, v in source.items():
        if k in target and isinstance(v, dict) and isinstance(target[k], dict):
            deep_merge(v, target[k])
        else:
            target[k] = v

    return target
