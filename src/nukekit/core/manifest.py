from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from ..utils import _sort_dict, deep_merge
from .assets import Asset, AssetType
from .scanner import scan_folder
from .serialization import dump_json, load_json
from .versioning import Version

logger = logging.getLogger(__name__)


class ManifestStore:
    """
    Persistence layer for manifests.

    Handles loading/saving manifests from/to various sources:
    - JSON files
    - Filesystem scanning
    - Merging cached data
    """

    @staticmethod
    def load_from_json(path: Path) -> Manifest:
        """Create Manifest from a file path"""
        if not path.exists():
            logger.warning(f"Manifest file {path} not found, returning empty")
            return Manifest(source_path=path)

        try:
            data = load_json(path)
            return Manifest.from_dict(data)
        except Exception as e:
            logger.error(f"Failed to load manifest from {path}: {e}")
            raise

    @staticmethod
    def save_to_json(manifest: Manifest, path: Path) -> None:
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # Sort for consistent output
        sorted_data = _sort_dict(manifest.to_dict())

        # Write to disk
        dump_json(sorted_data, path)
        logger.debug(f"Saved manifest to {path}")

    @staticmethod
    def from_local_state(
        scan_path: Path,
        cached_manifest: Manifest | None = None,
    ) -> Manifest:
        """
        Create manifest by scanning filesystem.

        If cached_manifest is provided, merges metadata from cache
        (like author, changelog, etc.) with newly scanned assets.

        Args:
            scan_path: Directory to scan for assets
            cached_manifest: Optional cached manifest to merge with

        Returns:
            Manifest created from filesystem scan
        """

        # Allow for custom output path from
        if isinstance(scan_path, Path):
            if not scan_path.is_dir():
                raise TypeError("Provided path for scanner is not a dir")
        scanned_data = scan_folder(scan_path)
        scanned_manifest = Manifest.from_dict(scanned_data)

        # If we have cached data, merge it
        if cached_manifest:
            scanned_manifest = scanned_manifest.merge(cached_manifest)

        return scanned_manifest

    @staticmethod
    def ensure_manifest_file(path: Path) -> Manifest:
        """
        Load manifest or create empty one if it doesn't exist.

        Args:
            path: Path to manifest file

        Returns:
            Loaded or new empty manifest
        """
        if path.exists():
            return ManifestStore.load_from_json(path)
        else:
            # Create new empty manifest and save it
            manifest = Manifest(source_path=path)
            ManifestStore.save_to_json(manifest, path)
            logger.info(f"Created new manifest at {path}")
            return manifest


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

    def add(self, asset: Asset) -> bool:
        """
        Reads current manifest, adds asset and writes out updated manifest.

        :param asset: Asset object to add to manifest
        :type asset: Asset
        :return: Confirmation of successfull add
        :rtype: bool
        """

        data = self.read_manifest()

        if asset.name not in data[asset.type]:
            # New asset
            data[asset.type][asset.name] = {asset.version: asset}
        else:
            # Existing asset, add to asset"s dict
            data[asset.type][asset.name][asset.version] = asset

        if self.write_manifest(data):
            # Updates current status
            self.data = self.read_manifest()
            logger.debug(
                f"Successfully added {asset.name} v{asset.version} to {self.ROOT}"
            )
            return True
        else:
            return False

    def get_latest_asset_version(self, asset: Asset) -> Version | None:
        """
        Parses the manifest and returns the highest version for this asset.

        :param asset: Asset to return latest version
        :type asset: Asset
        :return: Version instance of latest asset"s version
        :rtype: Version
        """

        data = self.read_manifest()

        try:
            data[asset.type][asset.name]
        except Exception:
            # Asset is not in manifest.
            return None
        else:
            # Asset is in manifest, get list of all versions.
            asset_versions_list = list(data[asset.type][asset.name].keys())
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
            return self.data[asset.type.name][asset.name][asset.version]
        except KeyError:
            return None

    def has_asset(
        self,
        asset: Asset,
    ) -> bool:
        """Check if asset exists in manifest."""
        try:
            asset_dict = self.data[asset.type.name][asset.name]
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


# Convenience functions (optional)
def load_manifest(path: Path) -> Manifest:
    """Load manifest from JSON file."""
    return ManifestStore.load_from_json(path)


def save_manifest(manifest: Manifest, path: Path) -> None:
    """Save manifest to JSON file."""
    ManifestStore.save_to_json(manifest, path)
