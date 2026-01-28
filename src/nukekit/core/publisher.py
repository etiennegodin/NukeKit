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

        repo_subdir = get_repo_subdir_path(self.context, 'gizmos')
        gizmos_subdirs = list_subdirs(repo_subdir, output_type='str')
        if gizmo.name not in gizmos_subdirs:
            Path(repo_subdir / gizmo.name).mkdir()



    def copy(self, gizmo:Gizmo)-> bool:
        shutil.copy(gizmo.path, )



        pass    

    def metadata():
        pass