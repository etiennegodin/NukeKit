from pathlib import Path
import os 
from .context import Context
ROOT_FOLDER = Path(os.getcwd())
        
def create_central_repo(context:Context):
    try:
        repo = context.config['repository']
        root = Path(repo['root'])
        root.mkdir(exist_ok= True)
        for s in repo['subfolder']:
            Path(f"{root}/{s}").mkdir(exist_ok= True)
    except Exception as e:
        raise(e)

