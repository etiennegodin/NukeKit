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

    def publish_asset(self, asset:Path|Asset)-> bool:
        if isinstance(asset, Path):
            asset = Asset.from_path(self.context, asset)
        
        if asset.type == 'Script':
            raise NotImplementedError
        
        asset = self._resolve_version(asset)

        if not asset :
            return 
        
        asset = self._ensure_changelog(asset)
        asset.ensure_metadata()
            
        self._publish_to_repo(asset)

        self._sync_after_publish(asset)

        return True
    
    def _sync_after_publish(self, asset):
        installer = Installer(self.context)
        installer.install_asset(asset)
    
    def _ensure_changelog(self, asset:Asset)-> Asset:
        while True:
            message = input(f'No message found for {asset.name}, please enter a message: \n')
            if message:
                break
            else:
                print("\033[1A\033[K", end="") 

        asset.message = message
        return asset

    def _resolve_version(self,asset)-> Asset:

        while True:
            latest_version = self.context.repo_manifest.get_latest_asset_version(asset)
            #latest_version = None
            #New asset or newer than repo
            if latest_version is None or asset.version > latest_version:
                break
            # Version Logic: Conflict/Exists 
            to_update = False
            if latest_version == asset.version:
                to_update = user_input_choice(f'{asset} already exists in repo. \nDo you want to publish a new version?')
            elif latest_version > asset.version:
                if user_input_choice(f'A newer version of {asset} already exists in repo ({latest_version}). \nDo you want to update it?'):
                    asset.version = latest_version
                    to_update = True
                else:
                    return False
            # Handle the Decision
            if to_update:
                asset = self._version_up(asset)
                continue
            logger.info(f'Aborted publish of {asset}') 
        return asset
        
    def _version_up(self,asset:Asset):
        version_update = user_input_choice('Which type of update', Version.classes, type='str')
        asset.version.version_up(version_update)
        return asset 

    def _publish_to_repo(self,asset:Asset)-> bool:
        
        destination_path = asset.get_remote_path(self.context.repo) 

        try:
            shutil.copy2(asset.source_path, destination_path)
            logger.info(f"Successfully saved {asset} to {destination_path} ")
            asset.set_publish_status('published')
            self.context.repo_manifest.update(asset)

            return True
        except shutil.SameFileError as e :
            print("Source and destination represent the same file.")
        except PermissionError:
            print("Permission denied.")
        except FileNotFoundError:
            print("The source file or destination directory was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
