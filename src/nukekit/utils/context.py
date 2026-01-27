from .paths import ROOT_FOLDER, to_Path, create_central_repo
from .config import load_config
from .logger import setup_logger
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Union, Callable

@dataclass
class Context():
    config: Dict[str, Any ] = field(default_factory=dict)
    logger: 

def set_context():

    CONFIG = load_config()
    LOGGER = setup_logger('main', log_file= f'{ROOT_FOLDER}/test.log')
    print(LOGGER)
    if not to_Path(CONFIG['repository']['root']).exists():
        create_central_repo(CONFIG)