from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Literal, TypeAlias
import logging 
from pathlib import Path
from datetime import date

from ..utils.config import load_config
from ..utils.logger import setup_logger

@dataclass
class Context():
    root: Path
    repo: str
    manifest:Path
    date: str
    config: Dict[str, Any ] = field(default_factory=dict)
    logger: logging.Logger = None
    log_file:str = None
    asset_types: TypeAlias = Literal['gizmos', 'Script']

def init_context(ROOT_FOLDER):
    base_log_path = f'{ROOT_FOLDER}/nukekit.log'
    LOGGER = setup_logger('root', log_file= base_log_path)
    CONFIG = load_config(ROOT_FOLDER)
    REPO_PATH = CONFIG['repository']['root']
    MANIFEST_PATH = Path(REPO_PATH + "/manifest.json")
    
    return Context(ROOT_FOLDER,
                    REPO_PATH,
                    MANIFEST_PATH,
                    str(date.today()),
                    CONFIG,
                    LOGGER,
                    log_file= base_log_path)
