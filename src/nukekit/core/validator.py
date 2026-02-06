from __future__ import annotations
from typing import Literal
from .manifest import Manifest
from .assets import Asset
import logging
logger = logging.getLogger(__name__)


class Validator():
    def __init__(self):
        pass




def format_metadata(asset:Asset):
    return f"""Version: {asset.version}\tAuthor: {asset.author}\tTime: {asset.time}\tMessage" {asset.changelog}"""


