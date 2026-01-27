from nukekit.utils import *
from .core import publisher
from pprint import pprint



def main():
    CONFIG = load_config()
    LOGGER = setup_logger('main', log_file= f'{ROOT_FOLDER}/test.log')
    print(LOGGER)
    if not to_Path(CONFIG['repository']['root']).exists():
        create_central_repo(CONFIG)

    pprint(CONFIG)
    publisher.main(CONFIG)

