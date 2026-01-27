from pathlib import Path
import os 

ROOT_FOLDER = Path(os.getcwd())
        
def create_central_repo(config:dict):
    repo = config['repository']
    root = Path(repo['root'])
    root.mkdir(exist_ok= True)
    for s in repo['subfolder']:
        Path(f"{root}/{s}").mkdir(exist_ok= True)
