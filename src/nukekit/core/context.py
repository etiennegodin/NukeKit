from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Literal, TypeAlias
import logging 
from datetime import date
from ..core.repo import CentralRepo
from ..utils.paths import UserPaths 
from ..core.manifest import Manifest

logger = logging.getLogger(__name__)

@dataclass
class Context():
    repo: CentralRepo
    user_paths: UserPaths
    config: Dict[str, Any ]
    repo_manifest: Dict[str, Any]
    local_manifest: Dict[str, Any]
    date: str
    asset_types: TypeAlias = Literal['gizmo', 'script']

def init_context(REPO:CentralRepo, CONFIG:dict, USER_PATHS:UserPaths):

    REPO_MANIFEST = Manifest(REPO.MANIFEST).read_manifest()
    LOCAL_MANIFEST = Manifest(UserPaths.STATE_FILE).read_manifest()

    try:
        context = Context(REPO,
                USER_PATHS,
                CONFIG,
                REPO_MANIFEST,
                LOCAL_MANIFEST,
                str(date.today())
                )
    except Exception as e:
        raise e 
    
    return context