from __future__ import annotations
from ..core import Version
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class Gizmo():
    name:str 
    path:str
    version: Version
    changelog:str
    author: str = NotImplemented


