from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Literal, TypeAlias
import logging 
from pathlib import Path

from ..utils.config import load_config
from ..utils.logger import setup_logger

@dataclass
class Context():
    root: Path
    repo: str
    config: Dict[str, Any ] = field(default_factory=dict)
    logger: logging.Logger = None
    asset_types: TypeAlias = Literal['gizmos', 'scripts']

def set_context(ROOT_FOLDER):
    LOGGER = setup_logger('main', log_file= f'{ROOT_FOLDER}/nukekit.log')
    CONFIG = load_config(ROOT_FOLDER, LOGGER)
    print(ROOT_FOLDER)
    return Context(ROOT_FOLDER,CONFIG['repository']['root'],CONFIG, LOGGER)
