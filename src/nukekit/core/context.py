from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Literal, TypeAlias
import logging 
from pathlib import Path
from datetime import date
from ..utils.paths import CentralRepo, UserPaths

logger = logging.getLogger(__name__)

@dataclass
class Context():
    repo: CentralRepo
    user_paths: UserPaths
    config: Dict[str, Any ]
    date: str
    asset_types: TypeAlias = Literal['gizmo', 'script']

def init_context(REPO:CentralRepo, CONFIG:dict, USER_PATHS:UserPaths):
    try:
        context = Context(REPO,
                USER_PATHS,
                CONFIG,
                str(date.today())
                )
    except Exception as e:
        raise e 
    
    return context