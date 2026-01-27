from .utils import load_config, init_central_repo
from .core import publisher
from pprint import pprint

def main():
    CONFIG = load_config()
    init_central_repo(CONFIG)
    pprint(CONFIG)
    publisher.main(CONFIG)

