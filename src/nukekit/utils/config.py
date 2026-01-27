import yaml 
from .paths import to_Path, ROOT_FOLDER

def load_config():
    path = to_Path(f"{ROOT_FOLDER}/config/setting.yaml")
    try:
        with open(path, 'r') as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    except Exception as e:
        raise(e)
    
        
