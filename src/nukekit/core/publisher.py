from __future__ import annotations
from typing import TYPE_CHECKING
import shutil
import logging
from pathlib import Path

from .assets import Asset
from .installer import Installer
from ..utils.ux import user_input_choice

if TYPE_CHECKING:
    from .versioning import Version
    from .context import Context

logger = logging.getLogger(__name__)

class Publisher():
    def __init__(self, context:Context):
        self.context = context

    def publish_asset(self, asset:Path|Asset) -> bool:
        """
        Publish and asset to remote repository
        
        :param asset: Asset to publish. Asset will be reconstructed if given a path path
        :type asset: Path | Asset
        :return: Description
        :rtype: bool
        """

        if isinstance(asset, Path):
            asset = Asset.from_path(self.context, asset)

        if asset.type == 'Script':
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
        installer = Installer(self.context)
        return installer.install_asset(asset)
    
    def _resolve_version(self, asset:Asset) -> Asset:
        while True:
            latest_version = self.context.repo_manifest.get_latest_asset_version(asset)

            # New asset or newer than repo nothing to resolve
            if latest_version is Version("0.0.0") or asset.version > latest_version:
                break

            # Version Logic: Conflict/Exists 
            to_update = False

            # If same version ask to update
            if latest_version == asset.version:
                if user_input_choice(f'{asset} already exists in repo. \nDo you want to publish a new version?'):
                    to_update = True
                else:
                    raise UserWarning('Cannot publish over existing asset, aborting publish')

            # If lower version ask to update 
            elif latest_version > asset.version:
                if user_input_choice(f'A newer version of {asset} already exists in repo ({latest_version}). \nDo you want to update it?'):
                    # Promote current asset version to latest version and flag to update 
                    asset.version = latest_version
                    to_update = True
                else:
                    raise UserWarning('Cannot publish a lower version than existing asset, aborting publish')
            
            # Handle the Decision
            if to_update:
                asset = self._version_up(asset)
                continue

        return asset
        
    def _version_up(self,asset:Asset) -> Asset:
        version_update = user_input_choice('Which type of update', Version.classes, type='str')
        asset.version.version_up(version_update)
        return asset 

    def _publish_to_repo(self,asset:Asset)-> bool:
        published = False

        destination_path = asset.get_remote_path(self.context.repo) 

        try:
            shutil.copy2(asset.source_path, destination_path)
            logger.info(f"Successfully saved {asset} to {destination_path} ")
            asset.set_publish_status('published')
            self.context.repo_manifest.update(asset)
            published = True
        except shutil.SameFileError as e :
            logger.error("Source and destination represent the same file.")
        except PermissionError:
            logger.error("Permission denied.")
        except FileNotFoundError:
            logger.error("The source file or destination directory was not found.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        finally:   
            return published
