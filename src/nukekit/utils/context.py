from dataclasses import dataclass, field
from typing import Any, Dict
import logging 

from .config import load_config
from .logger import setup_logger

@dataclass
class Context():
    config: Dict[str, Any ] = field(default_factory=dict)
    logger: logging.Logger = None

def set_context(ROOT_FOLDER):
    CONFIG = load_config(ROOT_FOLDER)
    LOGGER = setup_logger('main', log_file= f'{ROOT_FOLDER}/test.log')
    return Context(CONFIG, LOGGER)
