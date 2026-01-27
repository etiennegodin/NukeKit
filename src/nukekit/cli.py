from nukekit.utils import set_context, create_central_repo 
from .core import publisher
from pprint import pprint



def main():
    context = set_context()
    create_central_repo(context)
    publisher.main(context)