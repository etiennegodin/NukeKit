from dataclasses import dataclass, field
from typing import Any, Dict
import logging 
from pathlib import Path

from .config import load_config
from .logger import setup_logger

@dataclass
class Context():
    root: Path
    config: Dict[str, Any ] = field(default_factory=dict)
    logger: logging.Logger = None

def set_context(ROOT_FOLDER):
    LOGGER = setup_logger('main', log_file= f'{ROOT_FOLDER}/nukekit.log')
    CONFIG = load_config(ROOT_FOLDER, LOGGER)
    return Context(ROOT_FOLDER,CONFIG, LOGGER)
