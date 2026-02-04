from typing import Literal
from .manifest import Manifest
import logging
from pprint import pprint

ASSET_STATUS = Literal['Latest', 'Outdated', 'Unpublished']

logger = logging.getLogger(__name__)


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
    latest_assets = {}

    for asset_category, asset_list in child_data.items():

        if asset_category not in unpublished_assets.keys(): unpublished_assets[asset_category] = []
        if asset_category not in outdated_assets.keys(): outdated_assets[asset_category] = []
        if asset_category not in latest_assets.keys(): latest_assets[asset_category] = []

        parent_repo_asset_type_dict = parent_data[asset_category]

        for a in asset_list:
            asset_name = a.name
            if asset_name not in parent_repo_asset_type_dict.keys():
                unpublished_assets[asset_category].append(a)
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
                latest_assets[asset_category].append(child_repo_asset)
        
    print('unpublished_assets')
    pprint(unpublished_assets)
    print('outdated_assets')
    pprint(outdated_assets)
    print('latest_assets')
    pprint(latest_assets)