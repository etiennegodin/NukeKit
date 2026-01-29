import logging
from pathlib import Path

def setup_logger(name: str, log_file: Path = None, level=logging.INFO):
    """Configure logger with file and console handlers."""
    logger = logging.getLogger(name)
    
    # If the logger already has handlers, it's already configured. 
    # Return it immediately to avoid duplicates.
    if logger.handlers:
        return logger

    logger.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Prevent messages from being sent to the root logger (another common double-log source)
    logger.propagate = False
    
    return logger
