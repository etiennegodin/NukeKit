import logging
from pathlib import Path

def init_logger(log_file: Path = None, level=logging.DEBUG):
    """
    Configure logger with log file path and level
    
    :param log_file: Path to write log file
    :type log_file: Path
    :param level: Log level
    """
    format = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'
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
