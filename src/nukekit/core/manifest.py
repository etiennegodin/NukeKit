from __future__ import annotations
import json 
from pprint import pprint
from .assets import Asset
from .context import Context


def load_manifest(context:Context):
    with open('data.json', 'r') as file:
        data = json.load(file)

def add_asset_to_manifest(asset:Asset):

    data = asset.__dict__
    
    with open("data.json", "w") as json_file:
        json.dump(data, json_file, indent=4) # indent for pretty-printing

    pass