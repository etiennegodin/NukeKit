from __future__ import annotations
import shutil
import logging

from ..core.assets import Asset
from .context import Context
from ..core.versioning import Version
from .manifest import Manifest 
from ..utils.ux import user_input_choice

logger = logging.getLogger(__name__)

class Publisher():
    def __init__(self, context:Context):
        self.context = context

    def publish_asset(self, asset:Asset)-> bool:

        if not isinstance(asset, Asset):
            error = 'Provided object is not at Asset'
            logger.error(error)
            raise TypeError(error)
        
        if asset.type == 'script':
            raise NotImplementedError
        
        asset_resolved = self._resolve_version(asset)
        asset_with_changelog = self._ensure_changelog(asset_resolved)
        asset_with_metadata = asset.ensure_metadata()

        self._publish_to_repo(asset_with_metadata)
        return self.context
    

    
    def _ensure_changelog(self, asset:Asset):
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
            asset.update_destination_path(self.context.repo)
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

            # Handle the Decision
            if to_update:
                asset = self._version_up(asset)
                continue
            logger.info(f'Aborted publish of {asset}')
            return False
        
        return asset
        
    def _version_up(self,asset:Asset):
        version_update = user_input_choice('Which type of update', Version.classes, type='str')
        asset.version.version_up(version_update)
        return asset 

    def _publish_to_repo(self, asset:Asset)-> bool:
        try:
            shutil.copy2(asset.source_path, asset.destination_path)
            logger.info(f"Successfully saved {asset} to {asset.destination_path} ")
            self.context.repo_manifest.update_manifest(asset)
            return True
        except shutil.SameFileError as e :
            print("Source and destination represent the same file.")
        except PermissionError:
            print("Permission denied.")
        except FileNotFoundError:
            print("The source file or destination directory was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
