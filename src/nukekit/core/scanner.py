from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from .assets import ASSET_SUFFIXES, Asset

if TYPE_CHECKING:
    from .context import Context

logger = logging.getLogger(__name__)


class Scanner:
    def __init__(self, context: Context):
        self.context = context
        self.user_paths = context.user_paths

    def _scan(self, path: Path) -> dict:
        logger.debug(path)
        assets = {}
        for suffix, obj in ASSET_SUFFIXES.items():
            asset_paths = list(path.rglob(f"*{suffix}"))
            asset_subtype: dict[str, dict] = {}
            for path in asset_paths:
                asset = Asset.from_path(self.context, path)
                if asset.name not in asset_subtype.keys():
                    asset_subtype[asset.name] = {}
                if asset.version not in asset_subtype[asset.name].keys():
                    asset_subtype[asset.name][asset.version] = asset
            assets[obj.type] = asset_subtype

        
        print(assets)

        assets = self._sort(assets)
        return assets

    def _sort(self, d: dict):
        return {
            k: self._sort(v) if isinstance(v, dict) else v
            for k, v in sorted(d.items(), reverse=True)
        }

    def scan_local(self, verbose: bool = False) -> dict:
        self.data = self._scan(self.user_paths.NUKE_DIR)
        return self.data

    def scan_folder(self, path) -> dict:
        return self._scan(path)
