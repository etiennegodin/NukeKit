from __future__ import annotations

import logging
import os
from pathlib import Path

from .assets import ASSET_SUFFIXES, Asset, AssetType

logger = logging.getLogger(__name__)


class Repository:
    """
    Represents the physical repository directory structure.

    Responsibilities:
    - Manage directory structure
    - Build asset paths
    - Ensure directories exist

    Does NOT:
    - Manage manifest (that's ManifestStore)
    - Track what's installed (that's Manifest)
    """

    def __init__(self, root: Path, asset_types: list[str]):
        """
        Initialize repository.

        Args:
            root: Root directory of repository
            asset_types: List of asset type subdirectories (e.g., ["Gizmo", "Script"])
        """
        self.root = Path(root).resolve()
        self.asset_types = asset_types
        self.manifest_path = self.root / "manifest.json"

        # Ensure structure exists
        self._ensure_structure()

    @classmethod
    def from_config(cls, config: dict) -> "Repository":
        """Create repository from config dictionary."""

        root = config["repository"]["root"]
        root = os.path.expandvars(root)
        root = os.path.expanduser(root)

        asset_types = config["repository"]["subfolder"]

        return cls(root=Path(root), asset_types=asset_types)

    def _ensure_structure(self) -> None:
        """Ensure repository directory structure exists."""
        # Create root
        self.root.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for each asset type
        for asset_type in self.asset_types:
            (self.root / asset_type).mkdir(exist_ok=True)

        logger.debug(f"Ensured repository structure at {self.root}")

    def get_asset_path(self, asset: Asset) -> Path:
        if asset.type not in self.asset_types:
            raise FileNotFoundError(f"Path {self.root / asset.type} not found in repo")

        # Force asset subfolder creation
        (self.root / asset.type / asset.name).mkdir(exist_ok=True)

        suffix = next(
            (key for key, val in ASSET_SUFFIXES.items() if val == asset.type), None
        )
        return self.root / asset.type / asset.name / f"{asset}{suffix}"

    def get_type_directory(self, asset_type: AssetType) -> Path:
        """Get directory for given asset type."""
        return self.root / asset_type.value

    def list_asset_directories(self, asset_type: AssetType) -> list[Path]:
        """
        List all asset directories of given type.

        Returns list of directories (one per asset name).
        """
        type_dir = self.get_type_directory(asset_type)
        if not type_dir.exists():
            return []

    def exists(self) -> bool:
        """Check if repository root exists."""
        return self.root.exists()

    def __repr__(self) -> str:
        return f"Repository(root={self.root})"
