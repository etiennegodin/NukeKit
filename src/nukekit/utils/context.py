from dataclasses import dataclass, field
from typing import Any, Dict
from pathlib import Path
import logging 

from .paths import ROOT_FOLDER, create_central_repo
from .config import load_config
from .logger import setup_logger

@dataclass
class Context():
    config: Dict[str, Any ] = field(default_factory=dict)
    logger: logging.Logger = None

def set_context():
    CONFIG = load_config()
    LOGGER = setup_logger('main', log_file= f'{ROOT_FOLDER}/test.log')
    return Context(CONFIG, LOGGER)
