from __future__ import annotations
from typing import Literal
from .manifest import Manifest
from .assets import Asset
import logging
from pprint import pprint
logger = logging.getLogger(__name__)


class Validator():
    def __init__(self):
        pass


def compare_manifest(parent:Manifest|dict, child:Manifest|dict):

    if isinstance(parent, Manifest):
        parent_data = parent.data
    elif isinstance(parent, dict):
        parent_data = parent

    if isinstance(child, Manifest):
        child_data = child.data
    elif isinstance(child, dict):
        child_data = child
    else:
        raise ValueError(f"Child manifest type {type(child)} not accepted")

    unpublished_assets = {}
    outdated_assets = {}
    synced_assets = {}

    assets = {}

    for asset_category, asset_list in child_data.items():

        if asset_category not in unpublished_assets.keys(): unpublished_assets[asset_category] = []
        if asset_category not in outdated_assets.keys(): outdated_assets[asset_category] = []
        if asset_category not in synced_assets.keys(): synced_assets[asset_category] = []

        parent_repo_asset_type_dict = parent_data[asset_category]
        
        for a in asset_list:
            # Manually set a to Asset to get methods 
            a:Asset
            asset_name = a.name
            if asset_name not in parent_repo_asset_type_dict.keys():
                a.set_status('unpublished')
                #unpublished_assets[asset_category].append(a)
                continue

            parent_repo_asset_versions_dict = parent_repo_asset_type_dict[asset_name]['versions']
            if isinstance(parent, Manifest):
                latest_version = parent.get_latest_asset_version(a)
            else:
                raise NotImplementedError("Cant't find latest version from dict")
            if a.version < latest_version:
                outdated_assets[asset_category].append(a)
                logger.warning(f"Found outdated version of {a} in local folder. Local state manifest is detached from current state")
                continue
            try:
                child_repo_asset = parent_repo_asset_versions_dict[str(a.version)]
            except KeyError:
                ValueError('Local tool higher version than local repo, manifest was not uopdated correctly ') 
            else:
                synced_assets[asset_category].append(child_repo_asset)
        
    print('unpublished_assets')
    pprint(unpublished_assets)
    print('outdated_assets')
    pprint(outdated_assets)
    print('synced_assets')
    pprint(synced_assets)



def format_metadata(asset:Asset):
    return f"""Version: {asset.version}\tAuthor: {asset.author}\tTime: {asset.time}\tMessage" {asset.changelog}"""


