import yaml 
from pathlib import Path
import logging

def load_config(ROOT_FOLDER, Logger:logging.Logger):
    path = Path(f"{ROOT_FOLDER}/config/setting.yaml")
    try:
        with open(path, 'r') as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError as e:
        #logger
        Logger.error(e)
        raise(e)
    
        
