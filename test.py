from typing import Literal, get_args
import ast

ASSET_SUFFIXES = {".gizmo": "GIZMO", ".nk": "SCRIPT"}


x = ast.literal_eval(ASSET_SUFFIXES)

print(x)