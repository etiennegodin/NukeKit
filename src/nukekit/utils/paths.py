from pathlib import Path
import os 
        
def create_central_repo(context):
    try:
        repo = context.config['repository']
        try:
            root = Path(repo['root'])
        except KeyError:
            context.logger.error('Root folder for central repository not sepcified')
    except KeyError as e:
        context.logger.error('Repository setting not found in user settings')

    if not root.exists():
        root.mkdir(exist_ok= True)
        context.logger.info(f'Created central repo at {root}')
        for s in repo['subfolder']:
            Path(f"{root}/{s}").mkdir(exist_ok= True)

