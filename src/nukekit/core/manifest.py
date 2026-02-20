from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from ..utils import deep_merge
from .assets import Asset, AssetType
from .versioning import Version

logger = logging.getLogger(__name__)


@dataclass
class Manifest:
    """
    Domain object representing a collection of versioned assets.
    """

    data: dict[str, dict[str, dict[str, Asset]]] = field(
        default_factory=lambda: {t.value: {} for t in AssetType}
    )

    # Metadata about this manifest (optional)
    source_path: Path | None = None

    @classmethod
    def from_dict(cls, data: dict, source_path: Path | None = None) -> "Manifest":
        """Create manifest from dictionary."""
        return cls(data=data, source_path=source_path)

    def add_asset(self, asset: Asset) -> None:
        """Add or update an asset in the manifest."""

        if asset.name not in self.data[asset.type]:
            # New asset
            self.data[asset.type][asset.name] = {}

        self.data[asset.type][asset.name][asset.version] = asset

    def get_latest_asset_version(self, asset: Asset) -> Version | None:
        try:
            self.data[asset.type][asset.name]
        except Exception:
            # Asset is not in manifest.
            return None
        else:
            # Asset is in manifest, get list of all versions.
            asset_versions_list = list(self.data[asset.type][asset.name].keys())
            if len(asset_versions_list) > 1:
                # If list has at least two version, sort and return highest value
                return Version.highest_version(asset_versions_list)
            else:
                # Only one version
                return asset_versions_list[0]

    def merge(self, other: "Manifest") -> "Manifest":
        """
        Merge another manifest into this one.
        Returns a NEW manifest (immutable operation).
        """
        merged_data = deep_merge(self.data, other.data)
        return Manifest(data=merged_data)

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
        return self.data

    def get_asset(
        self,
        asset: Asset,
    ) -> Asset | None:
        """Get specific asset by name and version."""
        try:
            return self.data[asset.type.value][asset.name][asset.version]
        except KeyError:
            return None

    def has_asset(
        self,
        asset: Asset,
    ) -> bool:
        """Check if asset exists in manifest."""
        try:
            asset_dict = self.data[asset.type.value][asset.name]
            if asset.version is None:
                return True  # Any version exists
            return asset.version in asset_dict
        except KeyError:
            return False

    def __len__(self) -> int:
        """Return total number of asset versions."""
        return sum(
            len(versions)
            for asset_type in self.data.values()
            for versions in asset_type.values()
        )

    def __repr__(self) -> str:
        return f"Manifest(assets={len(self)}, source={self.source_path})"
