from __future__ import annotations
from .versioning import Version
from typing import Optional
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Asset():
    name:str 
    source_path:str
    version: Version = NotImplemented
    changelog:str = NotImplemented
    author: str = NotImplemented
    destination_path: Path = NotImplemented
    time:str = str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

    def __post_init__(self):
        #Convert to path if string
        if isinstance(self.source_path, str):
            self.source_path  = Path(self.source_path)




@dataclass
class Gizmo(Asset):
    type:str = 'gizmo'

@dataclass
class Script(Asset):
    type:str = 'script'




