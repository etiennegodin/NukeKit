from __future__ import annotations
import shutil
import logging

from ..core.assets import Asset
from ..core.versioning import Version
from ..utils.paths import CentralRepo
from ..utils.manifest import Manifest 
from ..utils.logger import setup_logger 
from ..utils.ux import user_input

logger = logging.getLogger(__name__)

class Publisher():
    def __init__(self):
        """
        Docstring for __init__
        
        :param self: Description
        :param context: Description
        :type context: Context
        """
        #logger = setup_logger('Publisher', context.log_file )

    def publish_asset(self, asset:Asset, repo:CentralRepo)-> bool:
        
        manifest = Manifest(repo.MANIFEST)

        if not isinstance(asset, Asset):
            error = 'Provided object is not at Asset'
            logger.error(error)
            raise TypeError(error)
        
        if asset.type == 'script':
            raise NotImplementedError
        
        while True:
            asset.update_destination_path(repo)
            latest_version = manifest.get_latest_asset_version(asset)

            #New asset or newer than repo
            if latest_version is None or asset.version > latest_version:
                break

            # Version Logic: Conflict/Exists 
            to_update = False
            if latest_version == asset.version:
                to_update = user_input(f'{asset} already exists in repo. \nDo you want to publish a new version?')
            elif latest_version > asset.version:
                if user_input(f'A newer version of {asset} already exists in repo ({latest_version}). \nDo you want to update it?'):
                    asset.version = latest_version
                    to_update = True

            # Handle the Decision
            if to_update:
                asset = self._version_up(asset)
                continue
            logger.info(f'Aborted publish of {asset}')
            return False
    
        return self._publish_to_repo(asset)
    
    def _version_up(self,asset):
        version_update = user_input('Which type of update', Version.classes, type='str')
        asset.version.version_up(version_update)
        return asset 

    def _publish_to_repo(self, asset:Asset)-> bool:
        try:
            shutil.copy2(asset.source_path, asset.destination_path)
            logger.info(f"Successfully saved {asset} to {asset.destination_path} ")
            manifest.update_manifest(context, asset)
            return True
        except shutil.SameFileError as e :
            print("Source and destination represent the same file.")
        except PermissionError:
            print("Permission denied.")
        except FileNotFoundError:
            print("The source file or destination directory was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
