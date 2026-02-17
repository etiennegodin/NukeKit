from __future__ import annotations

import logging
import shutil
from typing import TYPE_CHECKING

from .assets import Asset
from .console import user_input_choice
from .versioning import VERSION_CLASSES

if TYPE_CHECKING:
    from . import Manifest


logger = logging.getLogger(__name__)


def publish_asset_to_repo(source_path, destination_path) -> bool:
    published = False

    try:
        shutil.copy2(source_path, destination_path)
        logger.info(f"Successfully saved {destination_path}")
        published = True

    except shutil.SameFileError:
        logger.error("Source and destination represent the same file.")
    except PermissionError:
        logger.error("Permission denied.")
    except FileNotFoundError:
        logger.error("The source file or destination directory was not found.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

    return published


def resolve_version(repo_manifest: Manifest, asset: Asset) -> Asset:
    while True:
        latest_version = repo_manifest.get_latest_asset_version(asset)
        # New asset or newer than repo nothing to resolve
        if latest_version is None or asset.version > latest_version:
            logger.info(f"{asset.name} not found in repo. New publish.")
            break

        # Version Logic: Conflict/Exists
        to_update = False

        # If same version ask to add
        if latest_version == asset.version:
            if user_input_choice(
                f"{asset} already exists in repo. \n"
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
                f"A newer version of {asset} already exists in repo"
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
