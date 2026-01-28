from __future__ import annotations
import shutil
from ..core.assets import Asset
from .context import Context
from ..utils import manifest as ma
from ..utils import paths

class Publisher():
    def __init__(self, context:Context):
        """
        Docstring for __init__
        
        :param self: Description
        :param context: Description
        :type context: Context
        """
        self.context = context
        self.repo = context.config['repository']

    def publish_asset(self, asset:Asset
                    )-> bool:
        
        if not isinstance(asset, Asset):
            error = 'Provided object is not at Asset'
            self.context.logger.error(error)
            raise TypeError(error)
        
        if asset.type == 'script':
            raise NotImplementedError
            
        if asset.version is None:
            #version 
            pass

        latest = ma.get_latest_asset_version(self.context, asset)

        print(latest)
        quit()
        paths.set_asset_destination_path(asset, self.context)


        self.copy_to_repo(asset)
        ma.update_manifest(self.context, asset)


    def copy_to_repo(self, asset:Asset)-> bool:
        try:
            shutil.copy2(asset.source_path, asset.destination_path)
            self.context.logger.info(f"Successfully saved {asset.name} to {asset.destination_path} ")
        except shutil.SameFileError:
            print("Source and destination represent the same file.")
        except PermissionError:
            print("Permission denied.")
        except FileNotFoundError:
            print("The source file or destination directory was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def metadata():
        pass