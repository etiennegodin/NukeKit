from __future__ import annotations
import shutil
import logging

from ..core.assets import Asset, asset_factory
from .context import Context
from ..core.versioning import Version
from .manifest import Manifest 
from ..utils.ux import user_input_choice
from pathlib import Path

logger = logging.getLogger(__name__)

class Publisher():
    def __init__(self, context:Context):
        self.context = context

    def publish_asset(self, asset_path:Path)-> bool:

        asset = asset_factory(asset_path)
        
        if asset.type == 'script':
            raise NotImplementedError
        
        asset = self._resolve_version(asset)
        if asset == False:
            return 
        asset = self._ensure_changelog(asset)
        asset.ensure_metadata()
            

        self._publish_to_repo(asset_path, asset)
        return self.context
    
    def _ensure_changelog(self, asset:Asset)-> Asset:
        if asset.changelog is None:
            while True:
                changelog = input(f'No changelog found for {asset.name}, please enter a message: \n')
                if changelog:
                    break
                else:
                    print("\033[1A\033[K", end="") 

            asset.changelog = changelog
            return asset

    def _resolve_version(self,asset)-> Asset:

        while True:
            latest_version = self.context.repo_manifest.get_latest_asset_version(asset)

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

    def _publish_to_repo(self, asset_path, asset:Asset)-> bool:
        
        destination_path = asset.get_remote_path(self.context.repo)

        logger.debug(asset_path)
        logger.debug(asset_path)
        try:
            shutil.copy2(asset_path, destination_path)
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
