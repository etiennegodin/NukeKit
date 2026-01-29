from __future__ import annotations
import shutil
from typing import get_args
from ..core.assets import Asset
from ..core.versioning import Version
from .context import Context
from ..utils import manifest 
from ..utils import paths 
from ..utils.logger import setup_logger 
from ..utils.ux import user_input
class Publisher():
    def __init__(self, context:Context):
        """
        Docstring for __init__
        
        :param self: Description
        :param context: Description
        :type context: Context
        """
        #context.logger = setup_logger('Publisher', context.log_file )
        self.context = context
        self.context.logger = setup_logger('Publisher', context.log_file)

    def publish_asset(self, asset:Asset
                    )-> bool:
        
        if not isinstance(asset, Asset):
            error = 'Provided object is not at Asset'
            self.context.logger.error(error)
            raise TypeError(error)
        
        if asset.type == 'script':
            raise NotImplementedError
        
        asset.destination_path = paths.set_asset_destination_path(asset, self.context)
        latest_version = manifest.get_latest_asset_version(self.context, asset)

        if latest_version is None:
            #New asset not published in repo
            self._publish_to_repo(asset)
        elif latest_version == asset.version:
            if user_input(f'{asset} already exists in repo. \nDo you want to publish a new version?'):
                self._version_up(asset)
            else:
                self.context.logger.info(f'Aborted publishing {asset}')
        elif latest_version > asset.version:
            if user_input(f'A newer version of {asset} already exists in repo ({latest_version}). \nDo you want to update it?'):
                asset.version = latest_version
                self._version_up(asset)
            else:
                self.context.logger.info(f'Aborted publish of {asset}')
        else:
            self._publish_to_repo(asset)

    def _version_up(self,asset):
        version_update = user_input('Which type of update', Version.classes, type='str')
        asset.version.version_up(version_update)
        self.publish_asset(asset)

    def _publish_to_repo(self, asset:Asset)-> bool:
        try:
            shutil.copy2(asset.source_path, asset.destination_path)
            self.context.logger.info(f"Successfully saved {asset} to {asset.destination_path} ")
            manifest.update_manifest(self.context, asset)

            return True
        except shutil.SameFileError as e :
            print("Source and destination represent the same file.")
        except PermissionError:
            print("Permission denied.")
        except FileNotFoundError:
            print("The source file or destination directory was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
