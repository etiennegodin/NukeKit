from __future__ import annotations
from ..core.context import Context
from pathlib import Path
from typing import Literal, List

path_types = Literal['str', 'Path']


class UserPaths:
    """All user paths."""

    BASE_DIR = Path.home() / ".nukekit"
    NUKE_GIZMO_DIR = Path.home() / ".nuke" / "gizmos"
    STATE_FILE = BASE_DIR / "local_state.json"
    LOG_FILE = BASE_DIR / "nukekit.log"
    CACHED_MANIFEST = BASE_DIR / "cached_manifest.json"

    @classmethod
    def ensure(cls):
        """Create local dirs if thy don't exist. Called once"""
        cls.BASE_DIR.mkdir(exist_ok=True)
        cls.NUKE_GIZMO_DIR.mkdir(parents=True, exist_ok=True)

        
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



