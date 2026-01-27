from pathlib import Path
import os 

ROOT_FOLDER = Path(os.getcwd())

def to_Path(file_path: str):
    if isinstance(file_path, Path):
        return file_path
    if not isinstance(file_path, Path):
        return Path(file_path)