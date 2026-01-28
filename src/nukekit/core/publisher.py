from __future__ import annotations
import shutil
from ..core.assets import Gizmo
from ..core.context import Context
from ..core.manifest import add_asset_to_manifest
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
        

    def publish_gizmo(self, gizmo:Gizmo
                    )-> bool:
        
        if not isinstance(gizmo, Gizmo):
            error = 'Provided object is not at Gizmo'
            self.context.logger.error(error)
            raise TypeError(error)
        
        # if first publish 
        # 
        # else increment  

        paths.set_asset_destination_path(gizmo, self.context)

        self.copy_to_repo(gizmo)
        add_asset_to_manifest(gizmo)
            


    def copy_to_repo(self, gizmo:Gizmo)-> bool:
        try:
            shutil.copy2(gizmo.source_path, gizmo.destination_path)
            self.context.logger.info(f"Successfully saved {gizmo.name} to {gizmo.destination_path} ")
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