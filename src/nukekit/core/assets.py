from __future__ import annotations
from .. import core
from ..utils import get_repo_subdir_path, list_subdirs, Context
from typing import Optional
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class Gizmo():
    name:str 
    source_path:Path | str
    version: core.Version
    changelog:str
    author: str = NotImplemented
    destination_path: Path = NotImplemented

    def __post_init__(self):
        #Convert to path if string
        if isinstance(self.source_path, str):
            self.source_path  = Path(self.source_path)


    def set_destination_path(self, context:Context):
        gizmos_folder = get_repo_subdir_path(context, 'gizmos')
        gizmos_list = list_subdirs(gizmos_folder)
        gizmo_subdir = Path(gizmos_folder / self.name)
        gizmo_path = Path(gizmo_subdir/ f"{self.name}_{self.version}")
        # Create folder if not existing 
        if gizmo_subdir not in gizmos_list:
            gizmo_subdir.mkdir()
        self.destination_path = gizmo_path


@dataclass
class Scripts():
    name:str 
    path:Path | str
    version: core.Version
    changelog:str
    author: str = NotImplemented

    def __post_init__(self):
        #Convert to path if string
        if isinstance(self.path, str):
            self.path  = Path(self.path)



