from __future__ import annotations

import logging
import re

from .assets import Asset, AssetType
from .console import user_input_choice
from .exceptions import AssetError
from .versioning import VERSION_CLASSES, Version

logger = logging.getLogger(__name__)


class AssetValidator:
    """Validate assets before operations."""

    # Rules
    MAX_NAME_LENGTH = 100
    VALID_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")
    MAX_FILE_SIZE_MB = 100

    @classmethod
    def validate_asset(cls, asset: Asset) -> tuple[bool, list[str]]:
        """
        Validate asset. Returns (is_valid, errors).

        Args:
            asset: Asset to validate

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Validate name
        if not asset.name:
            errors.append("Asset name cannot be empty")
        elif not cls.VALID_NAME_PATTERN.match(asset.name):
            errors.append(
                f"Asset name contains invalid characters: {asset.name}. "
                "Use only letters, numbers, hyphens, and underscores."
            )
        elif len(asset.name) > cls.MAX_NAME_LENGTH:
            errors.append(f"Asset name too long (max {cls.MAX_NAME_LENGTH} chars)")

        # Validate source path
        if not asset.source_path:
            errors.append("Asset source path is required")
        elif not asset.source_path.exists():
            errors.append(f"Asset file not found: {asset.source_path}")
        else:
            # Check file size
            size_mb = asset.source_path.stat().st_size / (1024 * 1024)
            if size_mb > cls.MAX_FILE_SIZE_MB:
                errors.append(
                    f"Asset file too large: {size_mb:.1f}MB "
                    f"(max {cls.MAX_FILE_SIZE_MB}MB)"
                )

        # Validate version
        if not asset.version:
            errors.append("Asset version is required")

        # Validate type
        if asset.type not in [AssetType.GIZMO, AssetType.SCRIPT]:
            errors.append(f"Invalid asset type: {asset.type}")

        return len(errors) == 0, errors

    @classmethod
    def validate_and_raise(cls, asset: Asset) -> None:
        """Validate asset and raise AssetError if invalid."""
        is_valid, errors = cls.validate_asset(asset)
        if not is_valid:
            raise AssetError("Invalid asset:\\n" + "\\n".join(errors))


class VersionValidator:
    pass


def resolve_version(latest_version: Version, asset: Asset) -> Asset:
    while True:
        # New asset or newer than repository nothing to resolve
        if latest_version is None or asset.version > latest_version:
            logger.info(f"{asset.name} not found in repository. New publish.")
            break

        # Version Logic: Conflict/Exists
        to_update = False

        # If same version ask to add
        if latest_version == asset.version:
            if user_input_choice(
                f"{asset} already exists in repository. \n"
                "Do you want to publish a new version?"
            ):
                to_update = True
            else:
                raise UserWarning(
                    "Cannot publish over existing asset, aborting publish"
                )

        # If lower version ask to add
        elif latest_version > asset.version:
            if user_input_choice(
                f"A newer version of {asset} already exists in repository"
                f"({latest_version}). \n"
                "Do you want to add it?"
            ):
                # Promote current asset version to latest version and flag to add
                asset.version = latest_version
                to_update = True
            else:
                raise UserWarning(
                    "Cannot publish a lower version than existing asset,"
                    "aborting publish"
                )

        # Handle the Decision
        if to_update:
            asset = _version_up(asset)
            continue

    return asset


def _version_up(asset: Asset) -> Asset:
    """Increment asset version based on user choice."""
    version_update = user_input_choice("Which type of add", VERSION_CLASSES, type="str")
    asset.version.version_up(version_update)
    return asset
