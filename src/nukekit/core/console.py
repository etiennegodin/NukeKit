import logging
import shutil
import subprocess
from typing import Any, Literal, get_args, get_origin

from rich import print
from rich.tree import Tree
from simple_term_menu import TerminalMenu

from .assets import Asset
from .exceptions import InvalidAssetError
from .serialization import stringify_keys

logger = logging.getLogger(__name__)

RETURN_TYPES = Literal["bool", "str"]


def _flatten_manifest_to_choices(
    data: dict,
) -> list[tuple[str, Asset]]:
    """Flatten manifest data
    (type -> name -> version -> Asset) to (display_line, asset) list."""
    choices: list[tuple[str, Asset]] = []
    for type_key, names in data.items():
        type_str = getattr(type_key, "value", type_key) if type_key else ""
        for name, versions in names.items():
            for version_key, value in versions.items():
                if isinstance(value, Asset):
                    version_str = str(version_key)
                    display = f"[{type_str}] {name} · {version_str}"
                    choices.append((display, value))
    return choices


def choose_asset_fzf(manifest_data: dict, prompt: str = "Select asset") -> Asset | None:
    """
    Let the user pick one asset via fzf (fuzzy finder). Requires the `fzf` binary.

    If fzf is not installed or the subprocess fails, falls back to choose_menu().

    Args:
        manifest_data: Nested dict from Manifest.to_dict()
        (type -> name -> version -> Asset).
        prompt: Optional prompt shown in fzf.

    Returns:
        Selected Asset, or None if user aborted.
    """
    choices = _flatten_manifest_to_choices(manifest_data)
    if not choices:
        return None

    if not shutil.which("fzf"):
        logger.debug("fzf not found, falling back to nested menu")
        return choose_menu(manifest_data, level_name=prompt)

    lines = [display for display, _ in choices]
    try:
        result = subprocess.run(
            ["fzf", "--no-multi", f"--prompt={prompt}> ", "--height", "~50%"],
            input="\n".join(lines),
            capture_output=True,
            text=True,
            timeout=300,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        logger.warning("fzf failed: %s, falling back to nested menu", e)
        return choose_menu(manifest_data, level_name=prompt)

    selected = (result.stdout or "").strip()
    if not selected or result.returncode != 0:
        return None

    for display, asset in choices:
        if display == selected:
            return asset
    return None


def choose_menu(d: dict, level_name: str = "Main menu") -> Asset | None:
    value = None
    while True:
        d = stringify_keys(d)
        options = list(d.keys())

        options.append("Return")
        terminal_menu = TerminalMenu(options, title=level_name)
        menu_entry_index = terminal_menu.show()

        if options[menu_entry_index] == "Return":
            break
        try:
            key = options[menu_entry_index]
            value = d[key]
        except (ValueError, IndexError):
            print("Invalid selection")
        else:
            if isinstance(value, Asset):
                return value
            elif isinstance(value, dict):
                value = choose_menu(value, level_name=key)
        if value is not None:
            return value
    if value is not None:
        if isinstance(value, Asset):
            return value
        raise InvalidAssetError("Selection is not a valid asset", {value: type(value)})

    else:
        return None


def print_data(data: dict, label: str = "Manifest"):
    """
    Print input dictionnary as tree in terminal

    :param data: Data to displauy
    :type data: dict
    :param label: Top level label for this branch of the tree
    :type label: str
    """

    format_string = "| {:<12} | {:<8} | {:<10} |"

    def recursive_tree(d: dict, t: Tree):
        t.add(format_string.format("Status", "Version", "Id"))
        for versions, asset in d.items():
            t.add(format_string.format(asset.status.name, asset.version, str(asset.id)))

    # Initilize tree
    tree = Tree(label)

    # Loop through asset categories and create a tree from recursive exploration
    for category, assets_dict in data.items():
        tree.add(category)
        for asset_name, _asset_data in assets_dict.items():
            asset_tree = tree.add(asset_name)
            recursive_tree(_asset_data, asset_tree)

    print(tree)


def _add_question_mark(question: str) -> str:
    if not question.endswith("?"):
        question += "?"
    return question


def _format_options_list(options: Any):
    if get_origin(options) is Literal:
        options = list(get_args(options))
    return options


def user_input_choice(
    question: str, options: list[str] | None = None, type: RETURN_TYPES = "bool"
) -> bool | str:
    """Ask user a question with options answers in terminal.


    Args:
        question (str): _description_
        options (list[str] | None, optional): _description_. Defaults to None.
        type (RETURN_TYPES, optional): _description_. Defaults to "bool".

    Returns:
        bool | str: _description_
    """
    if options is None:
        options = ["y", "n"]
    correct = False
    question = _add_question_mark(question)
    options = _format_options_list(options)

    while not correct:
        user_input_choice = input(f"{question} {list(options)} ")
        if user_input_choice in options:
            correct = True
        else:
            print("\033[1A\033[K", end="")

    if type == "bool":
        return user_input_choice == "y"
    return user_input_choice
