from __future__ import annotations
from ..core.context import Context
from ..core.assets import Asset
from pathlib import Path
from typing import Literal, List
import os 

path_types = Literal['str', 'Path']
        
def init_central_repo(context:Context):
    try:
        repo = context.config['repository']
        try:
            root = Path(repo['root'])
        except KeyError:
            context.logger.error('Root folder for central repository not specified')
    except KeyError as e:
        context.logger.error('Repository setting not found in user settings')

    if not root.exists():
        root.mkdir(exist_ok= True)
        context.logger.info(f'Created central repo at {root}')
        for s in repo['subfolder']:
            Path(f"{root}/{s}").mkdir(exist_ok= True)
        return True
    return False


def get_repo_subdir_path(context:Context, asset_type:Context.asset_types)->Path:
    subdir = Path(f"{context.repo}/{asset_type}")
    if subdir.is_dir():
        return subdir
    else:
        error = f"Repo subdir {asset_type} not found"
        context.logger.error(error)
        raise FileExistsError(error)

def list_subdirs(parent_path:Path, output_type:path_types = 'Path')->List[Path|str]:
    if not isinstance(parent_path, Path):
        parent_path= Path(parent_path)
    subdirs = [p for p in parent_path.iterdir() if p.is_dir()]

    if output_type == 'str':
        return [folder.name for folder in subdirs]
    else:
        return subdirs

def set_asset_destination_path(asset:Asset, context:Context)->Path:
    from ..utils import get_repo_subdir_path, list_subdirs
    gizmos_folder = get_repo_subdir_path(context, 'gizmos')
    gizmos_list = list_subdirs(gizmos_folder)
    gizmo_subdir = Path(gizmos_folder / asset.name)
    gizmo_path = Path(gizmo_subdir/ f"{asset.name}_v{asset.version}.gizmo")
    # Create folder if not existing 
    if gizmo_subdir not in gizmos_list:
        gizmo_subdir.mkdir()
    return gizmo_path

