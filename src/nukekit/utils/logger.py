import logging
from pathlib import Path

def init_logger():
    logging.basicConfig(level= logging.INFO, )

def setup_logger(log_file: Path = None, level=logging.INFO):
    """Configure logger with file and console handlers."""
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        filename=log_file,
        level=level,
        filemode= 'w',
        format=format
    )

    logger = logging.getLogger('root')
    formatter = logging.Formatter(format)
    # Console handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger
