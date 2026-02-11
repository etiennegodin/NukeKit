from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from .assets import Asset
from .console import user_input_choice
from .installer import Installer
from .versioning import VERSION_CLASSES

if TYPE_CHECKING:
    from .context import Context


logger = logging.getLogger(__name__)


class Publisher:
    def __init__(self, context: Context):
        self.context = context

    def publish_asset(self, asset: Path | Asset) -> bool:
        """
        Publish an asset to the remote repository.

        Args:
            asset: Path to asset file or Asset instance

        Returns:
            True if publish successful, False if aborted

        Raises:
            NotImplementedError: If asset type is Script
        """

        if isinstance(asset, Path):
            asset = Asset.from_path(self.context, asset)

        if asset.type == "Script":
            raise NotImplementedError

        asset = self._resolve_version(asset)

        # Ensures message
        asset.ensure_message()

        # Ensures metadata
        asset.ensure_metadata()

        if self._publish_to_repo(asset):
            # Sync and install published asset to local assets
            return self._sync_after_publish(asset)

        return False

    def _sync_after_publish(self, asset) -> bool:
        """Install asset locally after successful publish."""
        installer = Installer(self.context)
        return installer.install_asset(asset)

    def _resolve_version(self, asset: Asset) -> Asset:
        while True:
            latest_version = self.context.repo_manifest.get_latest_asset_version(asset)
            logger.debug(latest_version)
            # New asset or newer than repo nothing to resolve
            if latest_version is None or asset.version > latest_version:
                logger.info(f"{asset.name} is a new publish")
                break

            # Version Logic: Conflict/Exists
            to_update = False

            # If same version ask to update
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

            # If lower version ask to update
            elif latest_version > asset.version:
                if user_input_choice(
                    f"A newer version of {asset} already exists in repo"
                    f"({latest_version}). \n"
                    "Do you want to update it?"
                ):
                    # Promote current asset version to latest version and flag to update
                    asset.version = latest_version
                    to_update = True
                else:
                    raise UserWarning(
                        "Cannot publish a lower version than existing asset,"
                        "aborting publish"
                    )

            # Handle the Decision
            if to_update:
                asset = self._version_up(asset)
                continue

        return asset

    def _version_up(self, asset: Asset) -> Asset:
        """Increment asset version based on user choice."""
        version_update = user_input_choice(
            "Which type of update", VERSION_CLASSES, type="str"
        )
        asset.version.version_up(version_update)
        return asset

    def _publish_to_repo(self, asset: Asset) -> bool:
        """
        Copy asset file to repository.

        Returns:
            True if successful, False otherwise
        """
        published = False
        destination_path = asset.get_remote_path(self.context.repo)

        try:
            asset.set_publish_status("published")
            shutil.copy2(asset.source_path, destination_path)
            logger.info(f"Successfully saved {asset} to {destination_path} ")
            self.context.repo_manifest.update(asset)
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
