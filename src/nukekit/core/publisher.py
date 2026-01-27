from __future__ import annotations
from ..utils import Context
from typing import Optional
from .. import core

def copy():
    pass
# Update manifest

def metadata():
    pass



def publish_gizmo(context:Context,
                  path:str,
                  version:core.Version,
                  changelog:str,
                  author: Optional[str])-> bool:
    """
    Docstring for publish_gizmo
    
    :param context: Description
    :type context: Context
    :param version: Description
    :type version: str
    :param changelog: Description
    :type changelog: str
    :param author: Description
    :type author: Optional[str]
    :return: Description
    :rtype: bool
    """
    print(path)

    pass