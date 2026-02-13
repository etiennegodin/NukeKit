from __future__ import annotations

import logging
import os
from pathlib import Path

from .assets import ASSET_SUFFIXES, Asset
from .manifest import Manifest

logger = logging.getLogger(__name__)


class Repository:
    def __init__(self, config: dict):
        """
        Initialize repository from config dictionary.

        Args:
            config: Dictionary from config to configure repository
        """
        root = config["repository"]["root"]
        root = os.path.expandvars(root)
        root = os.path.expanduser(root)

        self.ROOT = Path(root)
        self.SUBFOLDERS = config["repository"]["subfolder"]
        self.MANIFEST_PATH = self.ROOT / "manifest.json"
        self.ensure()

    def add_manifest(self, manifest: Manifest):
        self.manifest = manifest

    def ensure(self) -> bool:
        ensured = False
        if not self.ROOT.exists():
            self.ROOT.mkdir(exist_ok=True)
            logger.info(f"Created central repo at {self.ROOT}")
            ensured = True
        for s in self.SUBFOLDERS:
            (self.ROOT / s).mkdir(exist_ok=True, parents=True)

        return ensured

    def build_asset_path(self, asset: Asset) -> Path:
        if asset.type not in self.SUBFOLDERS:
            raise FileNotFoundError(f"Path {self.ROOT / asset.type} not found in repo")

        # Force asset subfolder creation
        (self.ROOT / asset.type / asset.name).mkdir(exist_ok=True)

        suffix = next(
            (key for key, val in ASSET_SUFFIXES.items() if val == asset.type), None
        )
        return self.ROOT / asset.type / asset.name / f"{asset}{suffix}"
