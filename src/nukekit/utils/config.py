import yaml 
from pathlib import Path
from .paths import ROOT_FOLDER

def load_config():
    path = Path(f"{ROOT_FOLDER}/config/setting.yaml")
    try:
        with open(path, 'r') as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError as e:
        #logger
        raise(e)
    
        
