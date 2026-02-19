from __future__ import annotations

import logging
from pathlib import Path

from ..utils import _sort_dict
from .manifest import Manifest
from .scanner import scan_folder
from .serialization import dump_json, load_json

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
    def load_from_filesystem(
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


# Convenience functions (optional)
def load_manifest(path: Path) -> Manifest:
    """Load manifest from JSON file."""
    return ManifestStore.load_from_json(path)


def save_manifest(manifest: Manifest, path: Path) -> None:
    """Save manifest to JSON file."""
    ManifestStore.save_to_json(manifest, path)
