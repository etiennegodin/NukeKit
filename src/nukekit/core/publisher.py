from __future__ import annotations
import shutil
from pathlib import Path
from ..utils import Context
from ..utils.paths import get_repo_subdir_path, list_subdirs
from ..core import Gizmo


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
        
        gizmo.set_destination_path(self.context)

        if self.copy(gizmo):
            self.context.logger.info(f"Successfully saved {gizmo.name} to {gizmo.destination_path} ")


    def copy(self, gizmo:Gizmo)-> bool:
        
        try:
            shutil.copy2(gizmo.source_path, gizmo.destination_path)
            return True
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