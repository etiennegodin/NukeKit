from nukekit.utils import set_context, create_central_repo 
from .core import publisher
from pathlib import Path
import os 

ROOT_FOLDER = Path(os.getcwd())

def main():
    context = set_context(ROOT_FOLDER)
    create_central_repo(context)
    publisher.main(context)