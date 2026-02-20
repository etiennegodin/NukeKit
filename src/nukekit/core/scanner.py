from __future__ import annotations

import logging
from pathlib import Path

from ..utils import _sort_dict
from .assets import Asset, AssetType

logger = logging.getLogger(__name__)


def scan_folder(path: Path) -> dict:
    logger.debug(path)
    assets = {}
    for asset_type in list(AssetType):
        asset_paths = list(path.rglob(f"*{asset_type.suffix}"))
        asset_subtype: dict[str, dict] = {}
        for path in asset_paths:
            asset = Asset.from_path(path)
            if asset.name not in asset_subtype.keys():
                asset_subtype[asset.name] = {}
            if asset.version not in asset_subtype[asset.name].keys():
                asset_subtype[asset.name][asset.version] = asset
        assets[asset_type] = asset_subtype

    # Compare against
    assets = _sort_dict(assets)

    return assets
