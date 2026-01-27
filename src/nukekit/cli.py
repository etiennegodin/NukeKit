from nukekit.utils import *
from .core import publisher
from pprint import pprint



def main():
    context = set_context()
    publisher.main(context)