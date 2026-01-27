import yaml 
from pathlib import Path

def load_config(ROOT_FOLDER):
    path = Path(f"{ROOT_FOLDER}/config/setting.yaml")
    try:
        with open(path, 'r') as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError as e:
        #logger
        raise(e)
    
        
